"""Proposal-only autonomy, automatic critique, and meta-learning runtime.

This module deliberately has no durable mutation path. It may read a verified ledger
snapshot, produce critique commands as proposals, compute historical diagnostics, and
emit a learning plan. A caller must pass any proposed command through the existing
Owner-gated Ledger.apply boundary.

External research is additionally fail-closed behind an explicit runtime gate.
"""
from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Protocol

from .core import Ledger, current_focus

AUTONOMY_PROTOCOL = "minhtri-autonomy/v1"
RESEARCH_GATE_OPEN = "OPEN_AFTER_FRESH_SEAT_PASS"
DEFAULT_INTERVAL_SECONDS = 300.0


class AutonomyError(ValueError):
    pass


class ResearchAdapter(Protocol):
    """Optional research adapter. Implementations must preserve provenance."""

    def research(self, focus: dict[str, Any]) -> list[dict[str, Any]]:
        ...


def _utc_parse(value: str) -> datetime:
    if not isinstance(value, str):
        raise AutonomyError("timestamp must be a string")
    text = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        raise AutonomyError("timestamp must include timezone")
    return parsed.astimezone(timezone.utc)


def claims_without_review(state: dict[str, Any]) -> list[str]:
    reviewed = {r["claim_id"] for r in state.get("reviews", {}).values()}
    return sorted(cid for cid in state.get("claims", {}) if cid not in reviewed)


def _predictor_providers(state: dict[str, Any], claim_id: str) -> set[str]:
    providers: set[str] = set()
    for prediction in state.get("predictions", {}).values():
        if prediction.get("claim_id") != claim_id:
            continue
        procedure = state.get("procedures", {}).get(prediction.get("procedure_id"))
        if procedure and isinstance(procedure.get("provider_id"), str):
            providers.add(procedure["provider_id"])
    return providers


def structural_critique(
    state: dict[str, Any],
    claim_id: str,
    critic_provider_id: str,
) -> dict[str, Any]:
    """Return a deterministic first-pass critique proposal.

    This pre-check never emits ACCEPT_FOR_TRIAL. Semantic acceptance remains a separate
    critic/adjudicator responsibility. That makes automatic critique useful without
    allowing a deterministic heuristic to promote its own claim.
    """
    claim = state.get("claims", {}).get(claim_id)
    if not claim:
        raise AutonomyError(f"unknown claim: {claim_id}")
    if critic_provider_id not in state.get("providers", {}):
        raise AutonomyError(f"unknown critic provider: {critic_provider_id}")
    occupied = {claim.get("provider_id")} | _predictor_providers(state, claim_id)
    if critic_provider_id in occupied:
        raise AutonomyError("critic must be distinct from proposer and predictors")

    reasons: list[str] = []
    verdict = "HOLD"
    evidence_ids = claim.get("evidence_ids", [])
    if not evidence_ids:
        verdict = "REVISE"
        reasons.append("claim has no linked evidence")
    else:
        missing = [eid for eid in evidence_ids if eid not in state.get("evidence", {})]
        if missing:
            verdict = "REVISE"
            reasons.append("claim references missing evidence")
        restricted = []
        for eid in evidence_ids:
            evidence = state.get("evidence", {}).get(eid)
            if not evidence:
                continue
            source = state.get("sources", {}).get(evidence.get("source_id"), {})
            if source.get("rights_status") == "RESTRICTED":
                restricted.append(eid)
        if restricted:
            reasons.append("restricted-rights evidence requires explicit handling")

    if not str(claim.get("alternative", "")).strip():
        verdict = "REVISE"
        reasons.append("alternative explanation is missing")
    if not str(claim.get("falsifier", "")).strip():
        verdict = "REVISE"
        reasons.append("falsifier is missing")

    predictions = [
        p for p in state.get("predictions", {}).values()
        if p.get("claim_id") == claim_id
    ]
    resolved = [p for p in predictions if p.get("status") == "RESOLVED"]
    if predictions and len(resolved) < len(predictions):
        reasons.append("prediction outcomes remain unresolved")
    if len(resolved) < 2:
        reasons.append("fewer than two resolved predictions support trial-rule evaluation")

    if not reasons:
        reasons.append("structural checks passed; semantic critic still required")
    else:
        reasons.append("semantic critic still required before acceptance")

    return {
        "status": "PROPOSAL_ONLY",
        "claim_id": claim_id,
        "review_command": {
            "type": "review_claim",
            "data": {
                "id": f"auto-structural-review-{claim_id}",
                "claim_id": claim_id,
                "critic_provider_id": critic_provider_id,
                "verdict": verdict,
                "reason": "; ".join(reasons),
            },
        },
        "automatic_acceptance": False,
    }


def automatic_critique_plan(
    state: dict[str, Any],
    critic_provider_id: str | None,
) -> dict[str, Any]:
    pending = claims_without_review(state)
    if not pending:
        return {"status": "CLEAR", "pending_claims": [], "proposals": []}
    if not critic_provider_id:
        return {
            "status": "BLOCKED_NO_CRITIC_SEAT",
            "pending_claims": pending,
            "proposals": [],
        }
    proposals = []
    blocked = []
    for claim_id in pending:
        try:
            proposals.append(structural_critique(state, claim_id, critic_provider_id))
        except AutonomyError as exc:
            blocked.append({"claim_id": claim_id, "reason": str(exc)})
    return {
        "status": "PROPOSALS_READY" if proposals else "BLOCKED",
        "pending_claims": pending,
        "proposals": proposals,
        "blocked": blocked,
    }


def meta_learning_report(state: dict[str, Any], minimum_resolutions: int = 2) -> dict[str, Any]:
    resolutions = list(state.get("resolutions", {}).values())
    numeric = [
        r for r in resolutions
        if isinstance(r.get("interval_hit"), bool)
        and isinstance(r.get("absolute_midpoint_error"), (int, float))
    ]
    if not numeric:
        return {
            "status": "INSUFFICIENT_HISTORY",
            "resolution_count": 0,
            "lesson_candidates": [],
        }

    count = len(numeric)
    hits = sum(1 for r in numeric if r["interval_hit"])
    mean_error = sum(float(r["absolute_midpoint_error"]) for r in numeric) / count
    report: dict[str, Any] = {
        "status": "ANALYZED" if count >= minimum_resolutions else "INSUFFICIENT_HISTORY",
        "resolution_count": count,
        "interval_hits": hits,
        "interval_hit_rate": hits / count,
        "mean_absolute_midpoint_error": mean_error,
        "lesson_candidates": [],
    }
    if count < minimum_resolutions:
        return report

    miss_rate = 1.0 - report["interval_hit_rate"]
    if miss_rate >= 0.5:
        report["lesson_candidates"].append({
            "status": "META_LESSON_CANDIDATE",
            "statement": (
                "Historical preregistered intervals miss at least half of resolved outcomes; "
                "inspect assumptions, interval width, and measurement quality before reuse."
            ),
            "limits": (
                "Derived only from declared ledger history; no causal explanation or "
                "generalization beyond the recorded predictions is established."
            ),
            "evidence": {
                "resolution_count": count,
                "interval_hit_rate": report["interval_hit_rate"],
                "mean_absolute_midpoint_error": mean_error,
            },
        })
    else:
        report["lesson_candidates"].append({
            "status": "META_LESSON_CANDIDATE",
            "statement": (
                "Most recorded preregistered intervals contain their outcomes; keep measuring "
                "calibration and check whether intervals are excessively broad."
            ),
            "limits": (
                "Hit rate alone does not establish forecast quality, sharpness, causality, "
                "or transfer to a new domain."
            ),
            "evidence": {
                "resolution_count": count,
                "interval_hit_rate": report["interval_hit_rate"],
                "mean_absolute_midpoint_error": mean_error,
            },
        })
    return report


def autonomous_learning_plan(
    state: dict[str, Any],
    *,
    research_gate: str,
    now: datetime | None = None,
) -> list[dict[str, Any]]:
    now = now or datetime.now(timezone.utc)
    actions: list[dict[str, Any]] = []
    focus = current_focus(state)
    if not focus:
        return [{"action": "WAIT_OWNER_FOCUS", "reason": "no active learning focus"}]

    actions.append({
        "action": "KEEP_FOCUS",
        "focus_id": focus["id"],
        "domain_id": focus["domain_id"],
    })
    pending = claims_without_review(state)
    if pending:
        actions.append({"action": "CRITIQUE_PENDING_CLAIMS", "claim_ids": pending})

    due = []
    for pid, prediction in state.get("predictions", {}).items():
        if prediction.get("status") != "FROZEN":
            continue
        try:
            if _utc_parse(prediction["due_at"]) <= now:
                due.append(pid)
        except (KeyError, AutonomyError, ValueError):
            continue
    if due:
        actions.append({
            "action": "AWAIT_OUTCOME_EVIDENCE",
            "prediction_ids": sorted(due),
            "write_capability": False,
        })

    if research_gate == RESEARCH_GATE_OPEN:
        actions.append({
            "action": "RESEARCH_ALLOWED",
            "mode": "PROVENANCE_REQUIRED_UNVERIFIED_ONLY",
        })
    else:
        actions.append({
            "action": "RESEARCH_BLOCKED",
            "reason": research_gate,
        })

    candidate_lessons = sorted(
        lid for lid, lesson in state.get("lessons", {}).items()
        if lesson.get("status") == "CANDIDATE"
    )
    if candidate_lessons:
        actions.append({
            "action": "OWNER_REVIEW_LESSON_CANDIDATES",
            "lesson_ids": candidate_lessons,
        })
    return actions


def build_autonomy_packet(
    state: dict[str, Any],
    *,
    critic_provider_id: str | None = None,
    research_gate: str = "BLOCKED_UNTIL_FRESH_SEAT_PASS",
    research_adapter: ResearchAdapter | None = None,
) -> dict[str, Any]:
    focus = current_focus(state)
    research: dict[str, Any]
    if research_gate != RESEARCH_GATE_OPEN:
        research = {"status": "BLOCKED", "reason": research_gate, "artifacts": []}
    elif research_adapter is None:
        research = {"status": "BLOCKED_NO_ADAPTER", "artifacts": []}
    elif focus is None:
        research = {"status": "NO_ACTIVE_FOCUS", "artifacts": []}
    else:
        artifacts = research_adapter.research(focus)
        if not isinstance(artifacts, list):
            raise AutonomyError("research adapter must return a list")
        research = {
            "status": "UNVERIFIED_RESEARCH_PROPOSALS",
            "artifacts": artifacts,
        }

    return {
        "protocol": AUTONOMY_PROTOCOL,
        "write_capability": False,
        "automatic_verified_promotion": False,
        "automatic_trial_activation": False,
        "critique": automatic_critique_plan(state, critic_provider_id),
        "meta_learning": meta_learning_report(state),
        "learning_plan": autonomous_learning_plan(
            state, research_gate=research_gate
        ),
        "research": research,
    }


@dataclass
class ProposalOnlyAutonomyRuntime:
    """Background-capable proposal runtime with no ledger mutation method."""

    state_loader: Callable[[], dict[str, Any]]
    report_sink: Callable[[dict[str, Any]], None]
    critic_provider_id: str | None = None
    research_gate: str = "BLOCKED_UNTIL_FRESH_SEAT_PASS"
    research_adapter: ResearchAdapter | None = None

    def tick(self) -> dict[str, Any]:
        packet = build_autonomy_packet(
            self.state_loader(),
            critic_provider_id=self.critic_provider_id,
            research_gate=self.research_gate,
            research_adapter=self.research_adapter,
        )
        self.report_sink(packet)
        return packet

    def run(self, interval_seconds: float = DEFAULT_INTERVAL_SECONDS) -> None:
        if interval_seconds < 1:
            raise AutonomyError("interval must be at least one second")
        try:
            while True:
                self.tick()
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            return


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="minhtri-autonomy",
        description="Proposal-only automatic critique and meta-learning runtime",
    )
    parser.add_argument("--home", default="brain")
    parser.add_argument("--critic-provider-id")
    parser.add_argument(
        "--research-gate",
        default="BLOCKED_UNTIL_FRESH_SEAT_PASS",
        help="External research remains blocked unless explicitly promoted.",
    )
    parser.add_argument("--interval", type=float, default=DEFAULT_INTERVAL_SECONDS)
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args(argv)

    ledger = Ledger(Path(args.home))

    def load_state() -> dict[str, Any]:
        state, _, _ = ledger.verify()
        return state

    def emit(packet: dict[str, Any]) -> None:
        print(json.dumps(packet, ensure_ascii=False, sort_keys=True), flush=True)

    runtime = ProposalOnlyAutonomyRuntime(
        load_state,
        emit,
        critic_provider_id=args.critic_provider_id,
        research_gate=args.research_gate,
    )
    if args.once:
        runtime.tick()
    else:
        runtime.run(args.interval)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
