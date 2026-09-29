"""Non-destructive replay and archival for pre-v3 AI Commons ledgers.

The migration reader intentionally freezes the PR #2 / PR #3 arena contracts.
It never rewrites legacy events. Old open tasks are archival history only and
must be reopened under the current Brain/Law contract before new work continues.
"""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from .core import GateError, Ledger, canonical, digest, identifier, need, parse_time, ref, string


LEGACY_SCHEMA_PR2 = "arena-v1-core-constitution"
LEGACY_SCHEMA_PR3 = "arena-v2-github-brain"
CURRENT_SCHEMA = "arena-v3-law-ack"

LEGACY_COMMON_FIELDS = {
    "register_participant": {"id", "family_id", "model", "version", "adapter", "capabilities"},
    "close_task": {"task_id", "reason"},
    "submit_proposal": {"id", "task_id", "participant_id", "task_fingerprint", "claim", "alternative",
                        "uncertainties", "evidence_ids", "discriminating_test", "method_ref"},
    "submit_critique": {"id", "proposal_id", "participant_id", "task_fingerprint", "verdict", "reason",
                        "evidence_ids", "test"},
    "submit_adjudication": {"id", "proposal_id", "participant_id", "task_fingerprint", "critique_ids",
                             "outcome", "reason"},
}

LEGACY_OPEN_TASK_FIELDS = {
    LEGACY_SCHEMA_PR2: {"id", "goal_id", "domain_id", "core_head", "constitution_sha256", "brief", "acceptance",
                        "allowed_evidence_ids", "expires_at", "risk_class", "sensitivity", "mode", "budget_cap"},
    LEGACY_SCHEMA_PR3: {"id", "goal_id", "domain_id", "runtime_state_head", "brain_revision", "brain_fingerprint",
                        "brief", "acceptance", "allowed_evidence_ids", "expires_at", "risk_class", "sensitivity",
                        "mode", "budget_cap"},
}


def legacy_initial_state() -> dict:
    return {
        "format_version": 1,
        "phase": "SHADOW",
        "participants": {},
        "tasks": {},
        "proposals": {},
        "critiques": {},
        "adjudications": {},
    }


def _add(state: dict, collection: str, data: dict) -> None:
    key = identifier(data["id"], f"{collection} ID")
    if key in state[collection]:
        raise GateError(f"Duplicate {collection} ID: {key}")
    state[collection][key] = data


def _ids(values: Any, label: str) -> list[str]:
    if not isinstance(values, list) or any(not isinstance(v, str) for v in values) or len(set(values)) != len(values):
        raise GateError(f"{label} must be a list of distinct IDs")
    for value in values:
        identifier(value, label)
    return values


def _strings(values: Any, label: str) -> list[str]:
    if not isinstance(values, list) or not values:
        raise GateError(f"{label} must be a nonempty list")
    for value in values:
        string(value, label)
    return values


def _hex(value: Any, length: int, label: str) -> str:
    if not isinstance(value, str) or len(value) != length or any(c not in "0123456789abcdef" for c in value):
        raise GateError(f"{label} must be a {length}-character lowercase hex digest")
    return value


def _participant(state: dict, participant_id: str, role: str) -> dict:
    actor = ref(state, "participants", participant_id)
    if role not in actor["capabilities"]:
        raise GateError(f"Participant lacks {role} capability")
    return actor


def _task(state: dict, task_id: str, fingerprint: str, at: str) -> dict:
    task = ref(state, "tasks", task_id)
    if task["status"] != "OPEN" or parse_time(at) > parse_time(task["expires_at"]):
        raise GateError("Task is closed or expired")
    if fingerprint != task["fingerprint"]:
        raise GateError("Task fingerprint mismatch; use the frozen task packet")
    return task


def _evidence(task: dict, evidence_ids: Any) -> None:
    if not set(_ids(evidence_ids, "evidence_ids")).issubset(task["allowed_evidence_ids"]):
        raise GateError("Evidence reference is outside the task packet")


def legacy_arena_evolve(schema: str, state: dict, command: dict, at: str) -> dict:
    """Replay exactly the pre-acknowledgement PR #2 / PR #3 Arena semantics."""
    if schema not in LEGACY_OPEN_TASK_FIELDS:
        raise GateError(f"Unsupported legacy arena schema: {schema}")
    if not isinstance(command, dict) or set(command) != {"type", "data"} or not isinstance(command["data"], dict):
        raise GateError("Command must contain exactly type and data object")
    kind, d = command["type"], copy.deepcopy(command["data"])
    fields = dict(LEGACY_COMMON_FIELDS)
    fields["open_task"] = LEGACY_OPEN_TASK_FIELDS[schema]
    if kind not in fields:
        raise GateError(f"Unknown legacy arena command: {kind}")
    extra = set(d) - fields[kind]
    if extra:
        raise GateError("Unexpected legacy fields: " + ", ".join(sorted(extra)))
    parse_time(at)
    out = copy.deepcopy(state)
    if out["phase"] != "SHADOW":
        raise GateError("Only shadow mode is implemented")

    if kind == "register_participant":
        need(d, "id", "family_id", "model", "version", "adapter", "capabilities")
        identifier(d["family_id"], "family_id")
        for key in ("model", "version"):
            string(d[key], key)
        if d["adapter"] != "MANUAL":
            raise GateError("Only MANUAL adapter is implemented in legacy SHADOW")
        caps = _strings(d["capabilities"], "capabilities")
        if len(set(caps)) != len(caps) or not set(caps).issubset({"PROPOSE", "CRITIQUE", "ADJUDICATE"}):
            raise GateError("Invalid or duplicate capabilities")
        d["identity_status"] = "SELF_DECLARED_UNVERIFIED"
        d["status"] = "ACTIVE"
        _add(out, "participants", d)

    elif kind == "open_task":
        need(d, *fields[kind])
        identifier(d["goal_id"], "goal_id")
        identifier(d["domain_id"], "domain_id")
        if schema == LEGACY_SCHEMA_PR2:
            _hex(d["core_head"], 64, "core_head")
            _hex(d["constitution_sha256"], 64, "constitution_sha256")
        else:
            _hex(d["runtime_state_head"], 64, "runtime_state_head")
            _hex(d["brain_revision"], 40, "brain_revision")
            _hex(d["brain_fingerprint"], 64, "brain_fingerprint")
        for key in ("brief", "acceptance"):
            string(d[key], key)
        _ids(d["allowed_evidence_ids"], "allowed_evidence_ids")
        if parse_time(d["expires_at"]) <= parse_time(at):
            raise GateError("Task must expire in the future")
        if d["risk_class"] not in ("NORMAL", "HIGH_STAKES"):
            raise GateError("Invalid risk_class")
        if d["sensitivity"] != "PUBLIC" or d["mode"] != "SHADOW":
            raise GateError("Legacy shadow arena accepts PUBLIC task packets only")
        if type(d["budget_cap"]) is not int or d["budget_cap"] != 0:
            raise GateError("Legacy shadow task budget cap must be zero")
        d["fingerprint"] = digest(d)
        d["status"] = "OPEN"
        d["opened_at"] = at
        _add(out, "tasks", d)

    elif kind == "close_task":
        need(d, "task_id", "reason")
        task = ref(out, "tasks", d["task_id"])
        string(d["reason"], "reason")
        if task["status"] != "OPEN":
            raise GateError("Task is already closed")
        task["status"] = "CLOSED"
        task["closed_reason"] = d["reason"]

    elif kind == "submit_proposal":
        need(d, *fields[kind])
        task = _task(out, d["task_id"], d["task_fingerprint"], at)
        _participant(out, d["participant_id"], "PROPOSE")
        for key in ("claim", "alternative", "discriminating_test", "method_ref"):
            string(d[key], key)
        _strings(d["uncertainties"], "uncertainties")
        _evidence(task, d["evidence_ids"])
        d["status"] = "UNVERIFIED_PROPOSAL"
        d["submitted_at"] = at
        _add(out, "proposals", d)

    elif kind == "submit_critique":
        need(d, *fields[kind])
        proposal = ref(out, "proposals", d["proposal_id"])
        if any(a["proposal_id"] == d["proposal_id"] for a in out["adjudications"].values()):
            raise GateError("Review is frozen after adjudication; open a new task to reconsider")
        task = _task(out, proposal["task_id"], d["task_fingerprint"], at)
        critic = _participant(out, d["participant_id"], "CRITIQUE")
        maker = ref(out, "participants", proposal["participant_id"])
        if critic["family_id"] == maker["family_id"]:
            raise GateError("Critic must be from another provider family")
        if d["verdict"] not in ("CHALLENGE", "NO_MATERIAL_DEFECT_FOUND", "ABSTAIN"):
            raise GateError("Invalid critique verdict")
        for key in ("reason", "test"):
            string(d[key], key)
        _evidence(task, d["evidence_ids"])
        d["task_id"] = proposal["task_id"]
        d["submitted_at"] = at
        _add(out, "critiques", d)

    elif kind == "submit_adjudication":
        need(d, *fields[kind])
        proposal = ref(out, "proposals", d["proposal_id"])
        if any(a["proposal_id"] == d["proposal_id"] for a in out["adjudications"].values()):
            raise GateError("Proposal already has an adjudication receipt")
        _task(out, proposal["task_id"], d["task_fingerprint"], at)
        judge = _participant(out, d["participant_id"], "ADJUDICATE")
        relevant = {cid for cid, critique in out["critiques"].items() if critique["proposal_id"] == d["proposal_id"]}
        provided = set(_ids(d["critique_ids"], "critique_ids"))
        if not relevant or provided != relevant:
            raise GateError("Adjudicator must consider every critique of the proposal")
        families = {out["participants"][proposal["participant_id"]]["family_id"]}
        families.update(out["participants"][out["critiques"][cid]["participant_id"]]["family_id"] for cid in relevant)
        if judge["family_id"] in families:
            raise GateError("Adjudicator must be independent of proposer and all critics")
        if d["outcome"] not in ("CANDIDATE_FOR_OWNER_REVIEW", "REVISE", "HOLD", "OWNER_REVIEW_REQUIRED"):
            raise GateError("Invalid adjudication outcome")
        if d["outcome"] == "CANDIDATE_FOR_OWNER_REVIEW" and any(
            out["critiques"][cid]["verdict"] != "NO_MATERIAL_DEFECT_FOUND" for cid in relevant
        ):
            raise GateError("Open challenge or abstention blocks a candidate")
        string(d["reason"], "reason")
        d["task_id"] = proposal["task_id"]
        d["status"] = "SHADOW_RECEIPT_ONLY"
        d["submitted_at"] = at
        _add(out, "adjudications", d)

    return out


def detect_legacy_schema(home: str | Path) -> str:
    """Detect PR #2 or PR #3 schema from the first open_task event."""
    events = Path(home) / "events.jsonl"
    if not events.exists():
        raise GateError("Legacy arena ledger missing events.jsonl")
    with events.open("r", encoding="utf-8") as fh:
        for raw in fh:
            try:
                event = json.loads(raw)
                command = event["command"]
            except (ValueError, TypeError, KeyError) as exc:
                raise GateError("Cannot inspect legacy arena event stream") from exc
            if command.get("type") != "open_task":
                continue
            keys = set(command.get("data", {}))
            if {"core_head", "constitution_sha256"}.issubset(keys):
                return LEGACY_SCHEMA_PR2
            if {"runtime_state_head", "brain_revision", "brain_fingerprint"}.issubset(keys) and                     "architecture_law_sha256" not in keys:
                return LEGACY_SCHEMA_PR3
            if "architecture_law_sha256" in keys or "bootstrap_sha256" in keys:
                raise GateError("Arena ledger already uses the current law-acknowledgement generation")
            raise GateError("Unknown legacy open_task shape")
    raise GateError("Cannot auto-detect legacy schema without an open_task; provide schema_hint")


def verify_legacy_arena(home: str | Path, schema_hint: str | None = None) -> dict:
    """Verify chain + snapshot with the frozen legacy reducer and return a migration report."""
    home = Path(home)
    schema = schema_hint or detect_legacy_schema(home)
    if schema not in LEGACY_OPEN_TASK_FIELDS:
        raise GateError(f"Unsupported schema_hint: {schema}")
    reducer = lambda state, command, at: legacy_arena_evolve(schema, state, command, at)
    state, count, head = Ledger(home, reducer=reducer, initial=legacy_initial_state).verify()
    counts = {key: len(value) for key, value in state.items() if isinstance(value, dict)}
    active_tasks = sorted(task_id for task_id, task in state["tasks"].items() if task["status"] == "OPEN")
    return {
        "status": "LEGACY_ARENA_VERIFIED",
        "source_schema": schema,
        "target_schema": CURRENT_SCHEMA,
        "event_count": count,
        "head": head,
        "state_digest": digest(state),
        "counts": counts,
        "active_tasks": active_tasks,
        "continuation_policy": "REOPEN_ACTIVE_TASKS_UNDER_CURRENT_BRAIN",
        "history_policy": "ARCHIVE_READ_ONLY_DO_NOT_REWRITE",
        "semantic_note": "Replay proves structural continuity only; it does not revalidate old AI outputs.",
    }


def archive_legacy_arena(source_home: str | Path, archive_root: str | Path, schema_hint: str | None = None) -> dict:
    """Verify then copy the immutable legacy ledger into a content-addressed archive directory."""
    source_home = Path(source_home)
    report = verify_legacy_arena(source_home, schema_hint)
    archive_root = Path(archive_root)
    destination = archive_root / f"{report['source_schema']}-{report['head'][:16]}"
    if destination.exists():
        raise GateError("Migration archive already exists; refusing to overwrite")
    destination.mkdir(parents=True, exist_ok=False)
    try:
        for name in ("events.jsonl", "state.json"):
            source = source_home / name
            if not source.exists():
                raise GateError(f"Legacy arena missing {name}")
            shutil.copy2(source, destination / name)
        manifest = {
            **report,
            "archive_format_version": 1,
            "source_files": {
                "events.jsonl_sha256": hashlib.sha256((destination / "events.jsonl").read_bytes()).hexdigest(),
                "state.json_sha256": hashlib.sha256((destination / "state.json").read_bytes()).hexdigest(),
            },
        }
        (destination / "migration_manifest.json").write_bytes(canonical(manifest) + b"\n")
        copied = verify_legacy_arena(destination, report["source_schema"])
        if copied["head"] != report["head"] or copied["state_digest"] != report["state_digest"]:
            raise GateError("Archived legacy arena failed replay equivalence")
        return {
            "status": "LEGACY_ARENA_ARCHIVED",
            "archive_path": str(destination),
            "manifest": manifest,
        }
    except Exception:
        if destination.exists():
            shutil.rmtree(destination)
        raise
