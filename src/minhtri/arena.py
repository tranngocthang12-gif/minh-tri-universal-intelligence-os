"""Provider-neutral, shadow-only task arena. Outputs are untrusted proposals."""

from __future__ import annotations

import copy
import hashlib
from pathlib import Path
from typing import Any

from .core import GateError, Ledger, digest, identifier, need, parse_time, ref, string, utcnow


ARENA_FIELDS = {
    "register_participant": {"id", "family_id", "model", "version", "adapter", "capabilities"},
    "open_task": {"id", "goal_id", "domain_id", "core_head", "constitution_sha256", "brief", "acceptance",
                  "allowed_evidence_ids", "expires_at", "risk_class", "sensitivity", "mode", "budget_cap"},
    "close_task": {"task_id", "reason"},
    "submit_proposal": {"id", "task_id", "participant_id", "task_fingerprint", "claim", "alternative",
                        "uncertainties", "evidence_ids", "discriminating_test", "method_ref"},
    "submit_critique": {"id", "proposal_id", "participant_id", "task_fingerprint", "verdict", "reason",
                        "evidence_ids", "test"},
    "submit_adjudication": {"id", "proposal_id", "participant_id", "task_fingerprint", "critique_ids",
                             "outcome", "reason"},
}

CAPABILITIES = {"PROPOSE", "CRITIQUE", "ADJUDICATE"}


def initial_arena_state() -> dict:
    return {"format_version": 1, "phase": "SHADOW", "participants": {}, "tasks": {},
            "proposals": {}, "critiques": {}, "adjudications": {}}


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


def arena_evolve(state: dict, command: dict, at: str) -> dict:
    """Pure reducer: validates structure and seat separation, never semantic truth."""
    if not isinstance(command, dict) or set(command) != {"type", "data"} or not isinstance(command["data"], dict):
        raise GateError("Command must contain exactly type and data object")
    kind, d = command["type"], copy.deepcopy(command["data"])
    if kind not in ARENA_FIELDS:
        raise GateError(f"Unknown arena command: {kind}")
    extra = set(d) - ARENA_FIELDS[kind]
    if extra:
        raise GateError("Unexpected fields: " + ", ".join(sorted(extra)))
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
            raise GateError("Only MANUAL adapter is implemented in SHADOW")
        caps = _strings(d["capabilities"], "capabilities")
        if len(set(caps)) != len(caps) or not set(caps).issubset(CAPABILITIES):
            raise GateError("Invalid or duplicate capabilities")
        d["identity_status"] = "SELF_DECLARED_UNVERIFIED"
        d["status"] = "ACTIVE"
        _add(out, "participants", d)

    elif kind == "open_task":
        need(d, *ARENA_FIELDS[kind])
        identifier(d["goal_id"], "goal_id")
        identifier(d["domain_id"], "domain_id")
        for key in ("core_head", "constitution_sha256"):
            if not isinstance(d[key], str) or len(d[key]) != 64 or any(c not in "0123456789abcdef" for c in d[key]):
                raise GateError(f"{key} must be a SHA-256 hex digest")
        for key in ("brief", "acceptance"):
            string(d[key], key)
        _ids(d["allowed_evidence_ids"], "allowed_evidence_ids")
        if parse_time(d["expires_at"]) <= parse_time(at):
            raise GateError("Task must expire in the future")
        if d["risk_class"] not in ("NORMAL", "HIGH_STAKES"):
            raise GateError("Invalid risk_class")
        if d["sensitivity"] != "PUBLIC" or d["mode"] != "SHADOW":
            raise GateError("Shadow arena accepts PUBLIC task packets only")
        if type(d["budget_cap"]) is not int or d["budget_cap"] != 0:
            raise GateError("Shadow task budget cap must be zero")
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
        need(d, *ARENA_FIELDS[kind])
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
        need(d, *ARENA_FIELDS[kind])
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
        need(d, *ARENA_FIELDS[kind])
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


def constitution_hash(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class ArenaService:
    """Boundary between the canonical core and shadow arena ledger."""

    def __init__(self, core_home: str | Path, constitution_path: str | Path):
        self.core = Ledger(core_home)
        self.ledger = Ledger(Path(core_home) / "arena", reducer=arena_evolve, initial=initial_arena_state)
        self.constitution_path = Path(constitution_path)

    def init(self) -> None:
        self.core.verify()
        constitution_hash(self.constitution_path)
        self.ledger.init()

    def apply(self, command: dict) -> dict:
        core_state, _, core_head = self.core.verify()
        if not isinstance(command, dict) or set(command) != {"type", "data"} or not isinstance(command["data"], dict):
            raise GateError("Command must contain exactly type and data object")
        command = copy.deepcopy(command)
        kind, d = command["type"], command["data"]
        if kind == "open_task":
            need(d, "goal_id", "id", "brief", "acceptance", "allowed_evidence_ids", "expires_at")
            if set(d) != {"goal_id", "id", "brief", "acceptance", "allowed_evidence_ids", "expires_at"}:
                raise GateError("open_task input has unexpected fields")
            goal = ref(core_state, "goals", d["goal_id"])
            if goal["status"] != "OPEN":
                raise GateError("Goal is blocked or closed")
            domain = ref(core_state, "domains", goal["domain_id"])
            for eid in _ids(d["allowed_evidence_ids"], "allowed_evidence_ids"):
                evidence = ref(core_state, "evidence", eid)
                source = ref(core_state, "sources", evidence["source_id"])
                if evidence["domain_id"] != goal["domain_id"] or source["kind"] != "SYNTHETIC" or source["rights_status"] != "CLEAR":
                    raise GateError("Shadow task context must be same-domain synthetic evidence with clear rights")
            d.update({"domain_id": goal["domain_id"], "core_head": core_head,
                      "constitution_sha256": constitution_hash(self.constitution_path),
                      "risk_class": domain["risk_class"], "sensitivity": "PUBLIC", "mode": "SHADOW", "budget_cap": 0})
        elif kind not in ("register_participant",):
            arena_state, _, _ = self.ledger.verify()
            task_id = d.get("task_id")
            if kind in ("submit_critique", "submit_adjudication"):
                task_id = ref(arena_state, "proposals", d.get("proposal_id"))["task_id"]
            task = ref(arena_state, "tasks", task_id)
            if task["core_head"] != core_head or task["constitution_sha256"] != constitution_hash(self.constitution_path):
                raise GateError("Task snapshot is stale; open a new task from current core/constitution")
        return self.ledger.apply(command)

    def status(self) -> dict:
        self.core.verify()
        state, count, head = self.ledger.verify()
        return {"phase": state["phase"], "event_count": count, "head": head,
                "counts": {key: len(value) for key, value in state.items() if isinstance(value, dict)}}

    def task_packet(self, task_id: str) -> dict:
        """Export one current, bounded packet for manual delivery; no model is called."""
        core_state, _, core_head = self.core.verify()
        arena_state, _, _ = self.ledger.verify()
        task = ref(arena_state, "tasks", task_id)
        constitution = self.constitution_path.read_bytes()
        if task["core_head"] != core_head or hashlib.sha256(constitution).hexdigest() != task["constitution_sha256"]:
            raise GateError("Task snapshot is stale; open a new task from current core/constitution")
        _task(arena_state, task_id, task["fingerprint"], utcnow())
        evidence = []
        for eid in task["allowed_evidence_ids"]:
            item = ref(core_state, "evidence", eid)
            source = ref(core_state, "sources", item["source_id"])
            evidence.append({key: item[key] for key in ("id", "statement", "observed_at", "value", "metric")
                             if key in item} | {"source_kind": source["kind"],
                                               "rights_status": source["rights_status"]})
        return {"task": copy.deepcopy(task), "constitution": constitution.decode("utf-8"),
                "evidence": evidence}
