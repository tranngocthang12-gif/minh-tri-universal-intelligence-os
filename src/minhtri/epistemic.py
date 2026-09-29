"""Epistemic registry and evidence-derived learning maturity for MINH TRI.

The registry tracks what the system currently treats as known/unknown and what
evidence supports a maturity claim. Maturity is derived, never directly set by
an AI/provider. R3 can structurally demonstrate L0-L6. L7-L9 remain future
gates until meta-learning, self-repair and transfer engines are implemented.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

from .core import GateError, Ledger, identifier, need, parse_time, ref, string


MATURITY_LEVELS = (
    "L0_MEMORY",
    "L1_KNOWLEDGE",
    "L2_UNDERSTANDING",
    "L3_PREDICTION",
    "L4_ACTION",
    "L5_VALIDATION",
    "L6_SELF_CRITICISM",
    "L7_META_LEARNING",
    "L8_SELF_REPAIR",
    "L9_TRANSFER",
)

REOPEN_TRIGGERS = {
    "NEW_EVIDENCE",
    "STALENESS",
    "REGRESSION",
    "OWNER_REOPEN",
    "DEPENDENCY_CHANGE",
    "POLICY_CHANGE",
    "ENVIRONMENT_CHANGE",
}

ITEM_KINDS = {"OBSERVATION", "INFERENCE", "HYPOTHESIS", "OPINION", "METHOD"}
APPLICATION_MODES = {"SHADOW_TEST", "READ_ONLY_ANALYSIS"}
UNKNOWN_MATERIALITY = {"LOW", "MEDIUM", "HIGH"}
ERROR_SEVERITY = {"LOW", "MEDIUM", "HIGH", "SEVERE"}

EPISTEMIC_FIELDS = {
    "register_item": {"id", "domain_id", "subject", "kind", "scope", "origin_ref", "review_due_at"},
    "support_item": {"item_id", "evidence_ids", "support_note", "review_due_at"},
    "demonstrate_understanding": {
        "item_id", "explanation", "distinction", "expected_pattern", "falsifier",
    },
    "link_prediction": {"item_id", "prediction_id", "claim_id"},
    "record_application": {"item_id", "mode", "description", "artifact_refs"},
    "record_validation": {
        "item_id", "resolution_id", "outcome_evidence_id", "verification_status", "quality_note",
    },
    "link_critique": {"item_id", "review_id", "critic_provider_id", "verdict"},
    "reopen_item": {"item_id", "trigger", "reason"},
    "revalidate_item": {"item_id", "evidence_ids", "reason", "review_due_at"},
    "register_unknown": {
        "id", "domain_id", "question", "materiality", "owner_impact", "review_due_at",
    },
    "resolve_unknown": {"unknown_id", "answer", "evidence_ids"},
    "reopen_unknown": {"unknown_id", "trigger", "reason"},
    "record_provider_error": {
        "id", "domain_id", "actor_ref", "task_class", "severity", "description", "evidence_ids",
    },
}


def initial_epistemic_state() -> dict:
    return {
        "format_version": 1,
        "phase": "SHADOW",
        "items": {},
        "unknowns": {},
        "provider_errors": {},
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


def _texts(values: Any, label: str) -> list[str]:
    if not isinstance(values, list) or any(not isinstance(v, str) or not v.strip() for v in values):
        raise GateError(f"{label} must be a text list")
    return [v.strip() for v in values]


def _review_due(value: Any, label: str = "review_due_at") -> str | None:
    if value is None:
        return None
    parse_time(value)
    return value


def _maturity_index(level: str) -> int:
    return MATURITY_LEVELS.index(level)


def _derive_level(item: dict) -> str:
    level = "L0_MEMORY"
    if item.get("knowledge_evidence_ids"):
        level = "L1_KNOWLEDGE"
    if level == "L1_KNOWLEDGE" and item.get("understanding"):
        level = "L2_UNDERSTANDING"
    if level == "L2_UNDERSTANDING" and item.get("prediction"):
        level = "L3_PREDICTION"
    if level == "L3_PREDICTION" and item.get("application"):
        level = "L4_ACTION"
    if level == "L4_ACTION" and item.get("validation"):
        level = "L5_VALIDATION"
    if level == "L5_VALIDATION" and item.get("critique"):
        level = "L6_SELF_CRITICISM"
    return level


def _refresh_maturity(item: dict) -> None:
    derived = _derive_level(item)
    previous = item.get("highest_demonstrated_level", "L0_MEMORY")
    if _maturity_index(derived) > _maturity_index(previous):
        item["highest_demonstrated_level"] = derived
    else:
        item["highest_demonstrated_level"] = previous
    if item.get("status") == "REOPENED":
        item["effective_level"] = "L0_MEMORY"
        item["maturity_status"] = "SUSPENDED_PENDING_REVALIDATION"
    else:
        item["effective_level"] = derived
        item["maturity_status"] = "ACTIVE_DECLARED_EVIDENCE"
    item["future_gates"] = {
        "L7_META_LEARNING": "R5_REQUIRED",
        "L8_SELF_REPAIR": "R5_OR_LATER_REQUIRED",
        "L9_TRANSFER": "R8_REQUIRED",
    }


def _item(state: dict, item_id: str) -> dict:
    return ref(state, "items", item_id)


def epistemic_evolve(state: dict, command: dict, at: str) -> dict:
    """Pure reducer: records epistemic evidence and derives current maturity."""
    if not isinstance(command, dict) or set(command) != {"type", "data"} or not isinstance(command["data"], dict):
        raise GateError("Command must contain exactly type and data object")
    kind, d = command["type"], copy.deepcopy(command["data"])
    if kind not in EPISTEMIC_FIELDS:
        raise GateError(f"Unknown epistemic command: {kind}")
    extra = set(d) - EPISTEMIC_FIELDS[kind]
    if extra:
        raise GateError("Unexpected epistemic fields: " + ", ".join(sorted(extra)))
    parse_time(at)
    out = copy.deepcopy(state)
    if out["phase"] != "SHADOW":
        raise GateError("Only SHADOW epistemic state is implemented")

    if kind == "register_item":
        need(d, "id", "domain_id", "subject", "kind", "scope", "origin_ref")
        identifier(d["domain_id"], "domain_id")
        string(d["subject"], "subject")
        string(d["scope"], "scope")
        string(d["origin_ref"], "origin_ref")
        if d["kind"] not in ITEM_KINDS:
            raise GateError("Invalid epistemic item kind")
        d["review_due_at"] = _review_due(d.get("review_due_at"))
        d["status"] = "ACTIVE"
        d["knowledge_evidence_ids"] = []
        d["understanding"] = None
        d["prediction"] = None
        d["application"] = None
        d["validation"] = None
        d["critique"] = None
        d["reopen_history"] = []
        d["revalidation_history"] = []
        d["created_at"] = at
        d["highest_demonstrated_level"] = "L0_MEMORY"
        d["effective_level"] = "L0_MEMORY"
        d["maturity_status"] = "ACTIVE_DECLARED_EVIDENCE"
        d["future_gates"] = {
            "L7_META_LEARNING": "R5_REQUIRED",
            "L8_SELF_REPAIR": "R5_OR_LATER_REQUIRED",
            "L9_TRANSFER": "R8_REQUIRED",
        }
        _add(out, "items", d)

    elif kind == "support_item":
        need(d, "item_id", "evidence_ids", "support_note")
        item = _item(out, d["item_id"])
        evidence_ids = _ids(d["evidence_ids"], "evidence_ids")
        if not evidence_ids:
            raise GateError("L1 knowledge requires at least one evidence reference")
        string(d["support_note"], "support_note")
        item["knowledge_evidence_ids"] = sorted(set(item["knowledge_evidence_ids"]) | set(evidence_ids))
        item["support_note"] = d["support_note"].strip()
        if "review_due_at" in d:
            item["review_due_at"] = _review_due(d["review_due_at"])
        _refresh_maturity(item)

    elif kind == "demonstrate_understanding":
        need(d, "item_id", "explanation", "distinction", "expected_pattern", "falsifier")
        item = _item(out, d["item_id"])
        if not item["knowledge_evidence_ids"]:
            raise GateError("Understanding cannot be claimed before evidence-supported knowledge")
        for key in ("explanation", "distinction", "expected_pattern", "falsifier"):
            string(d[key], key)
        item["understanding"] = {
            "explanation": d["explanation"].strip(),
            "distinction": d["distinction"].strip(),
            "expected_pattern": d["expected_pattern"].strip(),
            "falsifier": d["falsifier"].strip(),
            "recorded_at": at,
        }
        _refresh_maturity(item)

    elif kind == "link_prediction":
        need(d, "item_id", "prediction_id", "claim_id")
        item = _item(out, d["item_id"])
        if not item.get("understanding"):
            raise GateError("Prediction maturity requires demonstrated understanding first")
        identifier(d["prediction_id"], "prediction_id")
        identifier(d["claim_id"], "claim_id")
        item["prediction"] = {
            "prediction_id": d["prediction_id"],
            "claim_id": d["claim_id"],
            "linked_at": at,
        }
        _refresh_maturity(item)

    elif kind == "record_application":
        need(d, "item_id", "mode", "description", "artifact_refs")
        item = _item(out, d["item_id"])
        if not item.get("prediction"):
            raise GateError("Application maturity requires a linked preregistered prediction")
        if d["mode"] not in APPLICATION_MODES:
            raise GateError("R3 permits only SHADOW_TEST or READ_ONLY_ANALYSIS application modes")
        string(d["description"], "description")
        artifacts = _texts(d["artifact_refs"], "artifact_refs")
        item["application"] = {
            "mode": d["mode"],
            "description": d["description"].strip(),
            "artifact_refs": artifacts,
            "recorded_at": at,
            "external_effect": False,
        }
        _refresh_maturity(item)

    elif kind == "record_validation":
        need(d, "item_id", "resolution_id", "outcome_evidence_id", "verification_status", "quality_note")
        item = _item(out, d["item_id"])
        if not item.get("application"):
            raise GateError("Validation maturity requires bounded application first")
        identifier(d["resolution_id"], "resolution_id")
        identifier(d["outcome_evidence_id"], "outcome_evidence_id")
        string(d["verification_status"], "verification_status")
        string(d["quality_note"], "quality_note")
        item["validation"] = {
            "resolution_id": d["resolution_id"],
            "outcome_evidence_id": d["outcome_evidence_id"],
            "verification_status": d["verification_status"].strip(),
            "quality_note": d["quality_note"].strip(),
            "recorded_at": at,
        }
        _refresh_maturity(item)

    elif kind == "link_critique":
        need(d, "item_id", "review_id", "critic_provider_id", "verdict")
        item = _item(out, d["item_id"])
        if not item.get("validation"):
            raise GateError("Self-criticism maturity requires validated outcome first")
        identifier(d["review_id"], "review_id")
        identifier(d["critic_provider_id"], "critic_provider_id")
        if d["verdict"] not in ("ACCEPT_FOR_TRIAL", "HOLD", "REVISE"):
            raise GateError("Invalid linked critique verdict")
        item["critique"] = {
            "review_id": d["review_id"],
            "critic_provider_id": d["critic_provider_id"],
            "verdict": d["verdict"],
            "linked_at": at,
        }
        _refresh_maturity(item)

    elif kind == "reopen_item":
        need(d, "item_id", "trigger", "reason")
        item = _item(out, d["item_id"])
        if d["trigger"] not in REOPEN_TRIGGERS:
            raise GateError("Invalid reopen trigger")
        reason = string(d["reason"], "reason")
        item["reopen_history"].append({
            "trigger": d["trigger"],
            "reason": reason,
            "previous_effective_level": item["effective_level"],
            "invalidated_chain": {
                "understanding": copy.deepcopy(item.get("understanding")),
                "prediction": copy.deepcopy(item.get("prediction")),
                "application": copy.deepcopy(item.get("application")),
                "validation": copy.deepcopy(item.get("validation")),
                "critique": copy.deepcopy(item.get("critique")),
            },
            "at": at,
        })
        # Preserve historical evidence and highest demonstrated level, but invalidate
        # the active reasoning chain. Revalidation must rebuild each downstream gate.
        item["understanding"] = None
        item["prediction"] = None
        item["application"] = None
        item["validation"] = None
        item["critique"] = None
        item["status"] = "REOPENED"
        _refresh_maturity(item)

    elif kind == "revalidate_item":
        need(d, "item_id", "evidence_ids", "reason")
        item = _item(out, d["item_id"])
        if item["status"] != "REOPENED":
            raise GateError("Only a reopened item can be revalidated")
        evidence_ids = _ids(d["evidence_ids"], "evidence_ids")
        if not evidence_ids:
            raise GateError("Revalidation requires evidence")
        reason = string(d["reason"], "reason")
        item["knowledge_evidence_ids"] = sorted(set(item["knowledge_evidence_ids"]) | set(evidence_ids))
        item["revalidation_history"].append({"evidence_ids": evidence_ids, "reason": reason, "at": at})
        if "review_due_at" in d:
            item["review_due_at"] = _review_due(d["review_due_at"])
        item["status"] = "ACTIVE"
        _refresh_maturity(item)

    elif kind == "register_unknown":
        need(d, "id", "domain_id", "question", "materiality", "owner_impact")
        identifier(d["domain_id"], "domain_id")
        string(d["question"], "question")
        string(d["owner_impact"], "owner_impact")
        if d["materiality"] not in UNKNOWN_MATERIALITY:
            raise GateError("Invalid unknown materiality")
        d["review_due_at"] = _review_due(d.get("review_due_at"))
        d["status"] = "OPEN"
        d["resolution"] = None
        d["reopen_history"] = []
        d["created_at"] = at
        _add(out, "unknowns", d)

    elif kind == "resolve_unknown":
        need(d, "unknown_id", "answer", "evidence_ids")
        unknown = ref(out, "unknowns", d["unknown_id"])
        if unknown["status"] != "OPEN":
            raise GateError("Unknown is not open")
        answer = string(d["answer"], "answer")
        evidence_ids = _ids(d["evidence_ids"], "evidence_ids")
        if not evidence_ids:
            raise GateError("Resolving an unknown requires evidence")
        unknown["status"] = "RESOLVED_DECLARED_EVIDENCE"
        unknown["resolution"] = {"answer": answer, "evidence_ids": evidence_ids, "resolved_at": at}

    elif kind == "reopen_unknown":
        need(d, "unknown_id", "trigger", "reason")
        unknown = ref(out, "unknowns", d["unknown_id"])
        if d["trigger"] not in REOPEN_TRIGGERS:
            raise GateError("Invalid reopen trigger")
        reason = string(d["reason"], "reason")
        unknown["reopen_history"].append({"trigger": d["trigger"], "reason": reason, "at": at})
        unknown["status"] = "OPEN"

    elif kind == "record_provider_error":
        need(d, "id", "domain_id", "actor_ref", "task_class", "severity", "description", "evidence_ids")
        identifier(d["domain_id"], "domain_id")
        string(d["actor_ref"], "actor_ref")
        string(d["task_class"], "task_class")
        string(d["description"], "description")
        if d["severity"] not in ERROR_SEVERITY:
            raise GateError("Invalid provider error severity")
        d["evidence_ids"] = _ids(d["evidence_ids"], "evidence_ids")
        d["status"] = "OBSERVED_NOT_SCORED"
        d["recorded_at"] = at
        _add(out, "provider_errors", d)

    return out


class EpistemicService:
    """Binds epistemic records to current Core evidence, claims and outcomes."""

    def __init__(self, core_home: str | Path):
        self.core = Ledger(core_home)
        self.ledger = Ledger(Path(core_home) / "epistemic", reducer=epistemic_evolve, initial=initial_epistemic_state)

    def init(self) -> None:
        self.core.verify()
        self.ledger.init()

    def _same_domain_evidence(self, core_state: dict, domain_id: str, evidence_ids: list[str]) -> None:
        for evidence_id in evidence_ids:
            evidence = ref(core_state, "evidence", evidence_id)
            if evidence["domain_id"] != domain_id:
                raise GateError("Epistemic evidence cannot cross domain boundaries")

    def apply(self, command: dict) -> dict:
        self.ledger.acquire_project_lock()
        try:
                core_state, _, _ = self.core.verify()
            if not isinstance(command, dict) or set(command) != {"type", "data"} or not isinstance(command["data"], dict):
                raise GateError("Command must contain exactly type and data object")
            command = copy.deepcopy(command)
            kind, d = command["type"], command["data"]
            state, _, _ = self.ledger.verify()

            if kind == "register_item":
                ref(core_state, "domains", d.get("domain_id"))
            elif kind == "support_item":
                item = ref(state, "items", d.get("item_id"))
                self._same_domain_evidence(core_state, item["domain_id"], _ids(d.get("evidence_ids"), "evidence_ids"))
            elif kind == "link_prediction":
                item = ref(state, "items", d.get("item_id"))
                prediction = ref(core_state, "predictions", d.get("prediction_id"))
                claim = ref(core_state, "claims", prediction["claim_id"])
                if prediction["domain_id"] != item["domain_id"] or claim["domain_id"] != item["domain_id"]:
                    raise GateError("Prediction cannot cross epistemic domain boundaries")
                if prediction["status"] not in ("FROZEN", "RESOLVED"):
                    raise GateError("L3 requires a frozen preregistered prediction")
                d["claim_id"] = prediction["claim_id"]
            elif kind == "record_validation":
                item = ref(state, "items", d.get("item_id"))
                if not item.get("prediction"):
                    raise GateError("Validation requires a linked prediction")
                resolution = ref(core_state, "resolutions", d.get("resolution_id"))
                if resolution["prediction_id"] != item["prediction"]["prediction_id"]:
                    raise GateError("Resolution does not belong to the linked prediction")
                evidence = ref(core_state, "evidence", resolution["evidence_id"])
                source = ref(core_state, "sources", evidence["source_id"])
                if evidence["domain_id"] != item["domain_id"]:
                    raise GateError("Validation evidence cannot cross domain boundaries")
                if source["kind"] == "SYNTHETIC":
                    raise GateError("L5 validation requires non-synthetic observed outcome evidence")
                d["outcome_evidence_id"] = evidence["id"]
                d["verification_status"] = evidence.get("verification", "UNKNOWN")
            elif kind == "link_critique":
                item = ref(state, "items", d.get("item_id"))
                if not item.get("prediction"):
                    raise GateError("Critique requires a linked prediction")
                review = ref(core_state, "reviews", d.get("review_id"))
                if review["claim_id"] != item["prediction"]["claim_id"]:
                    raise GateError("Review belongs to another claim")
                if review["domain_id"] != item["domain_id"]:
                    raise GateError("Critique cannot cross domain boundaries")
                d["critic_provider_id"] = review["critic_provider_id"]
                d["verdict"] = review["verdict"]
            elif kind == "revalidate_item":
                item = ref(state, "items", d.get("item_id"))
                self._same_domain_evidence(core_state, item["domain_id"], _ids(d.get("evidence_ids"), "evidence_ids"))
            elif kind == "register_unknown":
                ref(core_state, "domains", d.get("domain_id"))
            elif kind == "resolve_unknown":
                unknown = ref(state, "unknowns", d.get("unknown_id"))
                self._same_domain_evidence(core_state, unknown["domain_id"], _ids(d.get("evidence_ids"), "evidence_ids"))
            elif kind == "record_provider_error":
                ref(core_state, "domains", d.get("domain_id"))
                self._same_domain_evidence(core_state, d["domain_id"], _ids(d.get("evidence_ids"), "evidence_ids"))

            return self.ledger.apply(command, project_lock_held=True)
        finally:
            self.ledger.release_project_lock()

    def status(self, now: str | None = None) -> dict:
        state, count, head = self.ledger.verify()
        due_items = []
        due_unknowns = []
        if now is not None:
            current = parse_time(now)
            for item_id, item in state["items"].items():
                if item.get("review_due_at") and parse_time(item["review_due_at"]) <= current:
                    due_items.append(item_id)
            for unknown_id, unknown in state["unknowns"].items():
                if unknown.get("review_due_at") and parse_time(unknown["review_due_at"]) <= current:
                    due_unknowns.append(unknown_id)
        maturity_counts = {level: 0 for level in MATURITY_LEVELS}
        for item in state["items"].values():
            maturity_counts[item["effective_level"]] += 1
        return {
            "phase": state["phase"],
            "event_count": count,
            "head": head,
            "counts": {
                "items": len(state["items"]),
                "unknowns": len(state["unknowns"]),
                "open_unknowns": sum(1 for u in state["unknowns"].values() if u["status"] == "OPEN"),
                "provider_errors": len(state["provider_errors"]),
            },
            "maturity_counts": maturity_counts,
            "review_due_items": sorted(due_items),
            "review_due_unknowns": sorted(due_unknowns),
        }

    def item(self, item_id: str) -> dict:
        state, _, _ = self.ledger.verify()
        return copy.deepcopy(ref(state, "items", item_id))
