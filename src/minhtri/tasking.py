"""Canonical task/checkpoint/lease control plane for replaceable workers.

This module keeps work state in MINH TRI rather than in any chat/model. It is
SHADOW-only: it routes no external provider and grants no external action.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

from .brain import brain_bundle, manifest_artifact_sha
from .core import GateError, Ledger, identifier, need, parse_time, ref, string


TASK_FIELDS = {
    "create_task": {
        "id", "goal_id", "domain_id", "brain_revision", "brain_fingerprint",
        "architecture_law_sha256", "bootstrap_sha256", "core_state_head_at_open",
        "brief", "acceptance", "allowed_evidence_ids", "risk_class",
    },
    "acquire_lease": {"task_id", "worker_id", "lease_id", "expires_at", "expected_checkpoint_seq"},
    "checkpoint_task": {
        "task_id", "worker_id", "lease_id", "expected_checkpoint_seq",
        "summary", "artifact_refs", "evidence_ids", "next_action",
    },
    "release_lease": {"task_id", "worker_id", "lease_id", "reason"},
    "complete_task": {
        "task_id", "worker_id", "lease_id", "expected_checkpoint_seq", "completion_summary",
    },
}

TERMINAL = {"COMPLETED", "CANCELLED"}


def initial_task_state() -> dict:
    return {"format_version": 1, "phase": "SHADOW", "tasks": {}}


def _hex(value: Any, length: int, label: str) -> str:
    if not isinstance(value, str) or len(value) != length or any(c not in "0123456789abcdef" for c in value):
        raise GateError(f"{label} must be a {length}-character lowercase hex digest")
    return value


def _ids(values: Any, label: str) -> list[str]:
    if not isinstance(values, list) or any(not isinstance(v, str) for v in values) or len(set(values)) != len(values):
        raise GateError(f"{label} must be a list of distinct IDs")
    for value in values:
        identifier(value, label)
    return values


def _texts(values: Any, label: str) -> list[str]:
    if not isinstance(values, list) or any(not isinstance(v, str) or not v.strip() for v in values):
        raise GateError(f"{label} must be a text list")
    return [v.strip() for v in values]


def _task(state: dict, task_id: str) -> dict:
    return ref(state, "tasks", task_id)


def _lease(task: dict, worker_id: str, lease_id: str, at: str) -> dict:
    lease = task.get("lease")
    if not lease or lease["worker_id"] != worker_id or lease["lease_id"] != lease_id:
        raise GateError("Worker does not hold the current task lease")
    if parse_time(at) >= parse_time(lease["expires_at"]):
        raise GateError("Task lease has expired")
    return lease


def task_evolve(state: dict, command: dict, at: str) -> dict:
    """Pure reducer for canonical task continuity."""
    if not isinstance(command, dict) or set(command) != {"type", "data"} or not isinstance(command["data"], dict):
        raise GateError("Command must contain exactly type and data object")
    kind, d = command["type"], copy.deepcopy(command["data"])
    if kind not in TASK_FIELDS:
        raise GateError(f"Unknown task command: {kind}")
    extra = set(d) - TASK_FIELDS[kind]
    if extra:
        raise GateError("Unexpected task fields: " + ", ".join(sorted(extra)))
    parse_time(at)
    out = copy.deepcopy(state)
    if out["phase"] != "SHADOW":
        raise GateError("Only SHADOW task routing is implemented")

    if kind == "create_task":
        need(d, *TASK_FIELDS[kind])
        task_id = identifier(d["id"], "task ID")
        if task_id in out["tasks"]:
            raise GateError(f"Duplicate task ID: {task_id}")
        identifier(d["goal_id"], "goal_id")
        identifier(d["domain_id"], "domain_id")
        _hex(d["brain_revision"], 40, "brain_revision")
        _hex(d["brain_fingerprint"], 64, "brain_fingerprint")
        _hex(d["architecture_law_sha256"], 64, "architecture_law_sha256")
        _hex(d["bootstrap_sha256"], 64, "bootstrap_sha256")
        _hex(d["core_state_head_at_open"], 64, "core_state_head_at_open")
        string(d["brief"], "brief")
        string(d["acceptance"], "acceptance")
        _ids(d["allowed_evidence_ids"], "allowed_evidence_ids")
        if d["risk_class"] not in ("NORMAL", "HIGH_STAKES"):
            raise GateError("Invalid risk_class")
        d["status"] = "OPEN"
        d["checkpoint_seq"] = 0
        d["checkpoint"] = {
            "seq": 0,
            "summary": "TASK_CREATED",
            "artifact_refs": [],
            "evidence_ids": [],
            "next_action": d["brief"],
            "worker_id": None,
            "updated_at": at,
        }
        d["lease"] = None
        d["handoffs"] = []
        d["created_at"] = at
        out["tasks"][task_id] = d

    elif kind == "acquire_lease":
        need(d, *TASK_FIELDS[kind])
        task = _task(out, d["task_id"])
        if task["status"] in TERMINAL:
            raise GateError("Cannot lease a terminal task")
        worker = identifier(d["worker_id"], "worker_id")
        lease_id = identifier(d["lease_id"], "lease_id")
        if type(d["expected_checkpoint_seq"]) is not int or d["expected_checkpoint_seq"] != task["checkpoint_seq"]:
            raise GateError("Checkpoint sequence mismatch; refresh task before claiming")
        if parse_time(d["expires_at"]) <= parse_time(at):
            raise GateError("Lease expiry must be in the future")
        previous = task.get("lease")
        if previous and parse_time(at) < parse_time(previous["expires_at"]):
            raise GateError("Task already has an active lease")
        if previous:
            task["handoffs"].append({
                "from_worker": previous["worker_id"],
                "to_worker": worker,
                "reason": "LEASE_EXPIRED",
                "checkpoint_seq": task["checkpoint_seq"],
                "at": at,
            })
        task["lease"] = {
            "worker_id": worker,
            "lease_id": lease_id,
            "acquired_at": at,
            "expires_at": d["expires_at"],
        }
        task["status"] = "IN_PROGRESS"

    elif kind == "checkpoint_task":
        need(d, *TASK_FIELDS[kind])
        task = _task(out, d["task_id"])
        _lease(task, d["worker_id"], d["lease_id"], at)
        if type(d["expected_checkpoint_seq"]) is not int or d["expected_checkpoint_seq"] != task["checkpoint_seq"]:
            raise GateError("Checkpoint sequence mismatch; refusing stale write")
        string(d["summary"], "summary")
        string(d["next_action"], "next_action")
        artifacts = _texts(d["artifact_refs"], "artifact_refs")
        evidence_ids = _ids(d["evidence_ids"], "evidence_ids")
        if not set(evidence_ids).issubset(task["allowed_evidence_ids"]):
            raise GateError("Checkpoint evidence is outside the task allowlist")
        task["checkpoint_seq"] += 1
        task["checkpoint"] = {
            "seq": task["checkpoint_seq"],
            "summary": d["summary"].strip(),
            "artifact_refs": artifacts,
            "evidence_ids": evidence_ids,
            "next_action": d["next_action"].strip(),
            "worker_id": d["worker_id"],
            "updated_at": at,
        }

    elif kind == "release_lease":
        need(d, *TASK_FIELDS[kind])
        task = _task(out, d["task_id"])
        lease = _lease(task, d["worker_id"], d["lease_id"], at)
        reason = string(d["reason"], "reason")
        task["handoffs"].append({
            "from_worker": lease["worker_id"],
            "to_worker": None,
            "reason": reason,
            "checkpoint_seq": task["checkpoint_seq"],
            "at": at,
        })
        task["lease"] = None
        task["status"] = "OPEN"

    elif kind == "complete_task":
        need(d, *TASK_FIELDS[kind])
        task = _task(out, d["task_id"])
        _lease(task, d["worker_id"], d["lease_id"], at)
        if type(d["expected_checkpoint_seq"]) is not int or d["expected_checkpoint_seq"] != task["checkpoint_seq"]:
            raise GateError("Checkpoint sequence mismatch; refusing stale completion")
        task["completion_summary"] = string(d["completion_summary"], "completion_summary")
        task["completed_at"] = at
        task["completed_by"] = d["worker_id"]
        task["status"] = "COMPLETED"
        task["lease"] = None

    return out


class TaskService:
    """Binds the task ledger to current Owner/Core/Brain gates."""

    def __init__(self, core_home: str | Path, brain_root: str | Path = ".", brain_revision: str | None = None):
        self.core = Ledger(core_home)
        self.ledger = Ledger(Path(core_home) / "tasks", reducer=task_evolve, initial=initial_task_state)
        self.brain_root = Path(brain_root)
        self.brain_revision = brain_revision

    def _brain(self) -> dict:
        return brain_bundle(self.brain_root, self.brain_revision)

    def init(self) -> None:
        self.core.verify()
        self._brain()
        self.ledger.init()

    def _assert_task_current(self, task: dict, core_state: dict, brain: dict) -> None:
        goal = ref(core_state, "goals", task["goal_id"])
        if goal["status"] != "OPEN":
            raise GateError("Task goal is blocked or closed")
        manifest = brain["manifest"]
        if task["brain_revision"] != manifest["brain_revision"] or task["brain_fingerprint"] != brain["fingerprint"]:
            raise GateError("Task brain version is stale; reopen from current brain")
        if task["architecture_law_sha256"] != manifest_artifact_sha(manifest, "PROJECT_LAW.md"):
            raise GateError("Task Project Law is stale")
        if task["bootstrap_sha256"] != manifest_artifact_sha(manifest, "BOOTSTRAP.md"):
            raise GateError("Task Bootstrap is stale")

    def apply(self, command: dict) -> dict:
        core_state, _, core_head = self.core.verify()
        brain = self._brain()
        if not isinstance(command, dict) or set(command) != {"type", "data"} or not isinstance(command["data"], dict):
            raise GateError("Command must contain exactly type and data object")
        command = copy.deepcopy(command)
        kind, d = command["type"], command["data"]
        if kind == "create_task":
            need(d, "id", "goal_id", "brief", "acceptance", "allowed_evidence_ids")
            if set(d) != {"id", "goal_id", "brief", "acceptance", "allowed_evidence_ids"}:
                raise GateError("create_task input has unexpected fields")
            goal = ref(core_state, "goals", d["goal_id"])
            if goal["status"] != "OPEN":
                raise GateError("Cannot create a task for a blocked or closed goal")
            domain = ref(core_state, "domains", goal["domain_id"])
            for evidence_id in _ids(d["allowed_evidence_ids"], "allowed_evidence_ids"):
                evidence = ref(core_state, "evidence", evidence_id)
                if evidence["domain_id"] != goal["domain_id"]:
                    raise GateError("Task evidence cannot cross domain boundaries")
            manifest = brain["manifest"]
            d.update({
                "domain_id": goal["domain_id"],
                "brain_revision": manifest["brain_revision"],
                "brain_fingerprint": brain["fingerprint"],
                "architecture_law_sha256": manifest_artifact_sha(manifest, "PROJECT_LAW.md"),
                "bootstrap_sha256": manifest_artifact_sha(manifest, "BOOTSTRAP.md"),
                "core_state_head_at_open": core_head,
                "risk_class": domain["risk_class"],
            })
        else:
            task_state, _, _ = self.ledger.verify()
            task = ref(task_state, "tasks", d.get("task_id"))
            self._assert_task_current(task, core_state, brain)
        return self.ledger.apply(command)

    def status(self) -> dict:
        core_state, _, _ = self.core.verify()
        state, count, head = self.ledger.verify()
        brain = self._brain()
        stale = []
        for task_id, task in state["tasks"].items():
            if task["status"] in TERMINAL:
                continue
            try:
                self._assert_task_current(task, core_state, brain)
            except GateError:
                stale.append(task_id)
        return {
            "phase": state["phase"],
            "event_count": count,
            "head": head,
            "counts": {
                "tasks": len(state["tasks"]),
                "open": sum(1 for t in state["tasks"].values() if t["status"] == "OPEN"),
                "in_progress": sum(1 for t in state["tasks"].values() if t["status"] == "IN_PROGRESS"),
                "completed": sum(1 for t in state["tasks"].values() if t["status"] == "COMPLETED"),
            },
            "stale_tasks": sorted(stale),
        }

    def packet(self, task_id: str) -> dict:
        core_state, _, _ = self.core.verify()
        state, _, _ = self.ledger.verify()
        brain = self._brain()
        task = ref(state, "tasks", task_id)
        self._assert_task_current(task, core_state, brain)
        evidence = [copy.deepcopy(ref(core_state, "evidence", eid)) for eid in task["allowed_evidence_ids"]]
        return {
            "task": copy.deepcopy(task),
            "brain": brain,
            "project_law": (self.brain_root / "PROJECT_LAW.md").read_text(encoding="utf-8"),
            "bootstrap": (self.brain_root / "BOOTSTRAP.md").read_text(encoding="utf-8"),
            "evidence": evidence,
        }
