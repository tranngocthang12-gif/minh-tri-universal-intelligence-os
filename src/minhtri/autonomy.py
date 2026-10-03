"""Proposal-only autonomy, automatic critique, and meta-learning runtime.

This module deliberately has no durable mutation path. It may read a verified ledger
snapshot, produce critique commands as proposals, compute historical diagnostics, and
emit a learning plan. A caller must pass any proposed command through the existing
Owner-gated Ledger.apply boundary.

External research is additionally fail-closed behind canonical PROJECT_STATE proof.
A caller cannot open research through a string, CLI flag, or runtime constructor option.
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
RESEARCH_GATE_BLOCKED = "BLOCKED_UNTIL_FRESH_SEAT_PASS"
CANONICAL_PROJECT_STATE = Path(__file__).resolve().parents[2] / "docs" / "PROJECT_STATE.json"
DEFAULT_INTERVAL_SECONDS = 300.0


class AutonomyError(ValueError):
    pass


def _derive_research_gate(project_state: dict[str, Any]) -> str:
    """Derive the research gate only from canonical proof fields.

    This helper is deterministic and intentionally ignores caller wishes. Runtime code
    obtains its input only from CANONICAL_PROJECT_STATE.
    """
    if (
        project_state.get("fresh_chat_seat_validation") == "PASS"
        and project_state.get("end_to_end_seat_brain_transport") is True
        and project_state.get("research_adapter_gate") == RESEARCH_GATE_OPEN
    ):
        return RESEARCH_GATE_OPEN
    return RESEARCH_GATE_BLOCKED


def canonical_research_gate() -> str:
    """Read canonical PROJECT_STATE and fail closed on any error or unmet proof."""
    try:
        data = json.loads(CANONICAL_PROJECT_STATE.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return RESEARCH_GATE_BLOCKED
    if not isinstance(data, dict):
        return RESEARCH_GATE_BLOCKED
    return _derive_research_gate(data)


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


def learning_assurance_report(state: dict[str, Any]) -> dict[str, Any]:
    """Summarize learning capital and assurance artifacts without promoting truth.

    External success/failure cases are capital only. Counts are inventory, never confidence.
    """
    cases = list(state.get("external_cases", {}).values())
    by_outcome = {"SUCCESS": 0, "FAILURE": 0, "MIXED": 0}
    for case in cases:
        outcome = case.get("outcome")
        if outcome in by_outcome:
            by_outcome[outcome] += 1
    controls = list(state.get("negative_controls", {}).values())
    control_results = {"PASS": 0, "FAIL": 0, "INCONCLUSIVE": 0}
    for control in controls:
        result = control.get("result")
        if result in control_results:
            control_results[result] += 1
    executions = list(state.get("critic_executions", {}).values())
    critic_verdicts: dict[str, int] = {}
    for execution in executions:
        verdict = str(execution.get("verdict", "UNKNOWN"))
        critic_verdicts[verdict] = critic_verdicts.get(verdict, 0) + 1
    return {
        "external_case_capital": {
            "count": len(cases),
            "by_outcome": by_outcome,
            "promotion_status": "CAPITAL_ONLY_NOT_LESSON_PROOF",
        },
        "frozen_learning_packets": len(state.get("learning_packets", {})),
        "critic_executions": {
            "count": len(executions),
            "by_verdict": critic_verdicts,
        },
        "negative_controls": {
            "count": len(controls),
            "by_result": control_results,
        },
        "automatic_verified_promotion": False,
        "automatic_trial_activation": False,
    }


def stratified_meta_learning_report(
    state: dict[str, Any],
    minimum_group_resolutions: int = 2,
) -> dict[str, Any]:
    """Analyze historical calibration by bounded strata without causal claims."""
    resolutions = list(state.get("resolutions", {}).values())
    predictions = state.get("predictions", {})
    procedures = state.get("procedures", {})
    evidence = state.get("evidence", {})
    sources = state.get("sources", {})

    def _summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
        numeric = [
            row for row in rows
            if isinstance(row.get("interval_hit"), bool)
            and isinstance(row.get("absolute_midpoint_error"), (int, float))
        ]
        count = len(numeric)
        if not count:
            return {"count": 0, "status": "NO_NUMERIC_HISTORY"}
        hits = sum(1 for row in numeric if row["interval_hit"])
        mean_error = sum(float(row["absolute_midpoint_error"]) for row in numeric) / count
        return {
            "count": count,
            "status": "ANALYZED" if count >= minimum_group_resolutions else "INSUFFICIENT_HISTORY",
            "interval_hits": hits,
            "interval_hit_rate": hits / count,
            "mean_absolute_midpoint_error": mean_error,
        }

    by_domain: dict[str, list[dict[str, Any]]] = {}
    by_procedure: dict[str, list[dict[str, Any]]] = {}
    by_source_kind: dict[str, list[dict[str, Any]]] = {}
    for row in resolutions:
        domain_id = str(row.get("domain_id", "UNKNOWN"))
        by_domain.setdefault(domain_id, []).append(row)

        prediction = predictions.get(row.get("prediction_id"), {})
        procedure_id = prediction.get("procedure_id")
        if isinstance(procedure_id, str):
            by_procedure.setdefault(procedure_id, []).append(row)

        evidence_id = row.get("evidence_id")
        ev = evidence.get(evidence_id, {}) if isinstance(evidence_id, str) else {}
        source = sources.get(ev.get("source_id"), {}) if isinstance(ev, dict) else {}
        source_kind = str(source.get("kind", "UNKNOWN"))
        by_source_kind.setdefault(source_kind, []).append(row)

    failure_counts: dict[str, int] = {}
    failure_by_domain: dict[str, dict[str, int]] = {}
    for failure in state.get("learning_failures", {}).values():
        failure_class = str(failure.get("failure_class", "UNKNOWN"))
        domain_id = str(failure.get("domain_id", "UNKNOWN"))
        failure_counts[failure_class] = failure_counts.get(failure_class, 0) + 1
        domain_map = failure_by_domain.setdefault(domain_id, {})
        domain_map[failure_class] = domain_map.get(failure_class, 0) + 1

    procedure_meta = {}
    for procedure_id, rows in sorted(by_procedure.items()):
        summary = _summary(rows)
        proc = procedures.get(procedure_id, {})
        summary["provider_id"] = proc.get("provider_id")
        summary["version"] = proc.get("version")
        summary["method"] = proc.get("method")
        procedure_meta[procedure_id] = summary

    candidates = []
    for domain_id, summary in sorted((k, _summary(v)) for k, v in by_domain.items()):
        if summary.get("status") == "ANALYZED":
            candidates.append({
                "status": "META_LESSON_CANDIDATE",
                "scope": {"domain_id": domain_id},
                "statement": (
                    "Historical calibration for this domain is now measurable; compare future "
                    "procedure changes against this bounded baseline rather than generalizing "
                    "from global averages."
                ),
                "limits": (
                    "Descriptive historical summary only; no causality or cross-domain transfer "
                    "is established."
                ),
            })

    return {
        "status": "ANALYZED" if resolutions or failure_counts else "INSUFFICIENT_HISTORY",
        "by_domain": {k: _summary(v) for k, v in sorted(by_domain.items())},
        "by_procedure": procedure_meta,
        "by_source_kind": {k: _summary(v) for k, v in sorted(by_source_kind.items())},
        "failure_counts": dict(sorted(failure_counts.items())),
        "failure_by_domain": {k: dict(sorted(v.items())) for k, v in sorted(failure_by_domain.items())},
        "lesson_candidates": candidates,
        "automatic_rule_change": False,
        "cross_domain_transfer_established": False,
    }


def assurance_integrity_report(state: dict[str, Any]) -> dict[str, Any]:
    receipts = list(state.get("critic_independence_receipts", {}).values())
    assessments = list(state.get("eval_integrity_assessments", {}).values())

    receipt_status: dict[str, int] = {}
    for item in receipts:
        status = str(item.get("status", "UNKNOWN"))
        receipt_status[status] = receipt_status.get(status, 0) + 1

    eval_status: dict[str, int] = {}
    for item in assessments:
        status = str(item.get("status", "UNKNOWN"))
        eval_status[status] = eval_status.get(status, 0) + 1

    return {
        "critic_independence_receipts": {
            "count": len(receipts),
            "by_status": dict(sorted(receipt_status.items())),
            "full_independence_proven": False,
        },
        "eval_integrity_assessments": {
            "count": len(assessments),
            "by_status": dict(sorted(eval_status.items())),
            "automatic_contamination_detection_proven": False,
            "automatic_reward_hacking_detection_proven": False,
        },
        "write_capability": False,
    }


def autonomous_learning_plan(
    state: dict[str, Any],
    *,
    now: datetime | None = None,
) -> list[dict[str, Any]]:
    research_gate = canonical_research_gate()
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
    research_adapter: ResearchAdapter | None = None,
) -> dict[str, Any]:
    research_gate = canonical_research_gate()
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
        "learning_assurance": learning_assurance_report(state),
        "stratified_meta_learning": stratified_meta_learning_report(state),
        "assurance_integrity": assurance_integrity_report(state),
        "learning_plan": autonomous_learning_plan(state),
        "research": research,
    }


@dataclass
class ProposalOnlyAutonomyRuntime:
    """Background-capable proposal runtime with no ledger mutation method."""

    state_loader: Callable[[], dict[str, Any]]
    report_sink: Callable[[dict[str, Any]], None]
    critic_provider_id: str | None = None
    research_adapter: ResearchAdapter | None = None

    def tick(self) -> dict[str, Any]:
        packet = build_autonomy_packet(
            self.state_loader(),
            critic_provider_id=self.critic_provider_id,
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
    )
    if args.once:
        runtime.tick()
    else:
        runtime.run(args.interval)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
