"""Small, deterministic learning ledger. Evidence quality remains a human judgment."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class GateError(ValueError):
    """An operation fails a contract or governance gate."""


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def parse_time(value: str) -> datetime:
    if not isinstance(value, str):
        raise GateError("Expected ISO 8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise GateError("Invalid ISO 8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise GateError("Timestamp needs a timezone")
    return parsed.astimezone(timezone.utc)


def identifier(value: Any, label: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[a-z][a-z0-9_-]{1,63}", value):
        raise GateError(f"{label} must be a lowercase identifier (2–64 characters)")
    return value


def string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GateError(f"{label} must be nonempty text")
    return value.strip()


def number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise GateError(f"{label} must be a number")
    result = float(value)
    if not (-1e100 < result < 1e100):
        raise GateError(f"{label} must be finite")
    return result


def need(d: dict, *fields: str) -> None:
    missing = [field for field in fields if field not in d]
    if missing:
        raise GateError("Missing: " + ", ".join(missing))


def ref(state: dict, collection: str, key: str) -> dict:
    identifier(key, collection + " ID")
    if key not in state[collection]:
        raise GateError(f"Unknown {collection} ID: {key}")
    return state[collection][key]


def add(state: dict, collection: str, data: dict) -> None:
    key = identifier(data["id"], collection + " ID")
    if key in state[collection]:
        raise GateError(f"Duplicate {collection} ID: {key}")
    state[collection][key] = data


def initial_state() -> dict:
    return {
        "format_version": 1,
        "domains": {}, "providers": {}, "goals": {}, "problems": {}, "sources": {},
        "evidence": {}, "procedures": {}, "claims": {}, "predictions": {},
        "resolutions": {}, "reviews": {}, "adjudications": {}, "lessons": {},
    }


ALLOWED_FIELDS = {
    "register_domain": {"id", "name", "risk_class", "measurement_contract"},
    "register_provider": {"id", "name", "kind"},
    "open_goal": {"id", "domain_id", "objective", "priority", "owner_boundary"},
    "set_goal_status": {"goal_id", "status", "reason"},
    "frame_problem": {"id", "goal_id", "reality", "conditions", "target", "intervention", "unknowns", "control", "influence", "responsibility", "harm_checks"},
    "record_source": {"id", "domain_id", "uri", "captured_at", "kind", "rights_status"},
    "record_evidence": {"id", "domain_id", "source_id", "statement", "observed_at", "value", "metric"},
    "register_procedure": {"id", "domain_id", "provider_id", "version", "method"},
    "propose_claim": {"id", "problem_id", "provider_id", "statement", "evidence_ids", "alternative", "falsifier"},
    "register_prediction": {"id", "claim_id", "procedure_id", "metric", "unit", "lower", "upper", "due_at", "resolution_method"},
    "freeze_prediction": {"prediction_id"},
    "record_resolution": {"id", "prediction_id", "evidence_id"},
    "review_claim": {"id", "claim_id", "critic_provider_id", "verdict", "reason"},
    "adjudicate_claim": {"id", "claim_id", "review_id", "adjudicator_provider_id", "verdict", "reason"},
    "propose_lesson": {"id", "claim_id", "statement", "limits", "prediction_ids", "adjudication_id"},
    "activate_trial_lesson": {"lesson_id", "owner_ack", "scope"},
    "record_external_case": {"id", "domain_id", "evidence_ids", "outcome", "context", "mechanism_hypothesis", "transfer_limits", "uncertainty"},
    "freeze_learning_packet": {"id", "trace_id", "claim_id", "counterevidence_ids", "external_case_ids", "counterevidence_note", "context_contract", "instruction_version", "toolset_fingerprint"},
    "record_critic_execution": {"id", "packet_id", "critic_provider_id", "provider", "model", "run_id", "context_mode", "output_hash", "verdict", "reason", "missing_evidence"},
    "record_negative_control": {"id", "packet_id", "description", "expected", "observed", "result", "evidence_ids"},
    "record_trace_link": {"id", "trace_id", "artifact_type", "artifact_id", "relation"},
    "schedule_lesson_revalidation": {"id", "lesson_id", "review_after", "staleness_conditions", "reason"},
    "record_lesson_revalidation": {"id", "schedule_id", "evidence_ids", "outcome", "reason", "limits", "trigger"},
    "set_learning_focus": {"id", "status", "domain_id", "source_id", "note", "expected_lesson", "uncertainty", "reason"},
}

FOCUS_ACTIVE_FIELDS = {"id", "status", "domain_id", "source_id", "note", "expected_lesson", "uncertainty"}
FOCUS_STOPPED_FIELDS = {"id", "status", "reason"}

TRACE_ARTIFACT_COLLECTIONS = {
    "SOURCE": "sources",
    "EVIDENCE": "evidence",
    "CLAIM": "claims",
    "PREDICTION": "predictions",
    "RESOLUTION": "resolutions",
    "REVIEW": "reviews",
    "ADJUDICATION": "adjudications",
    "LESSON": "lessons",
    "EXTERNAL_CASE": "external_cases",
    "LEARNING_PACKET": "learning_packets",
    "CRITIC_EXECUTION": "critic_executions",
    "NEGATIVE_CONTROL": "negative_controls",
    "LESSON_REVALIDATION": "lesson_revalidations",
}
TRACE_RELATIONS = {
    "ORIGIN", "SUPPORT", "COUNTEREVIDENCE", "PREDICTION", "OUTCOME",
    "CRITIC", "ADJUDICATION", "LESSON", "CONTROL", "REVALIDATION",
}


def _list_of_refs(state: dict, collection: str, values: Any) -> list[str]:
    if not isinstance(values, list) or any(not isinstance(v, str) for v in values) or len(set(values)) != len(values):
        raise GateError(f"{collection} references must be a unique list")
    for value in values:
        ref(state, collection, value)
    return values


def evolve(state: dict, command: dict, event_time: str, *, new_write: bool = True) -> dict:
    """Replay one event. A replay never consults a language model or current time.

    `new_write=False` is used only when replaying an existing ledger. It skips gates added
    after v0.1 shipped (currently: predictor seat separation) so ledgers written earlier
    still verify; every new append is checked with the full rule set.
    """
    if not isinstance(command, dict) or set(command) != {"type", "data"} or not isinstance(command["data"], dict):
        raise GateError("Command must contain exactly type and data object")
    kind, d = command["type"], copy.deepcopy(command["data"])
    if kind not in ALLOWED_FIELDS:
        raise GateError(f"Unknown command type: {kind}")
    extra = set(d) - ALLOWED_FIELDS[kind]
    if extra:
        raise GateError("Unexpected fields: " + ", ".join(sorted(extra)))
    out = copy.deepcopy(state)
    parse_time(event_time)

    if kind == "register_domain":
        need(d, "id", "name", "risk_class", "measurement_contract")
        if d["risk_class"] not in ("NORMAL", "HIGH_STAKES"):
            raise GateError("risk_class must be NORMAL or HIGH_STAKES")
        string(d["name"], "name")
        string(d["measurement_contract"], "measurement_contract")
        add(out, "domains", d)

    elif kind == "register_provider":
        need(d, "id", "name", "kind")
        if d["kind"] not in ("MODEL", "HUMAN", "TOOL"):
            raise GateError("Invalid provider kind")
        string(d["name"], "name")
        add(out, "providers", d)

    elif kind == "open_goal":
        need(d, "id", "domain_id", "objective", "priority", "owner_boundary")
        ref(out, "domains", d["domain_id"])
        string(d["objective"], "objective")
        string(d["owner_boundary"], "owner_boundary")
        if type(d["priority"]) is not int or not 1 <= d["priority"] <= 5:
            raise GateError("priority must be an integer from 1 to 5")
        d["status"] = "OPEN"
        add(out, "goals", d)

    elif kind == "set_goal_status":
        need(d, "goal_id", "status", "reason")
        goal = ref(out, "goals", d["goal_id"])
        if d["status"] not in ("OPEN", "BLOCKED", "CLOSED"):
            raise GateError("Invalid goal status")
        string(d["reason"], "reason")
        goal["status"] = d["status"]
        goal["status_reason"] = d["reason"]

    elif kind == "frame_problem":
        need(d, "id", "goal_id", "reality", "conditions", "target", "intervention", "unknowns",
             "control", "influence", "responsibility", "harm_checks")
        goal = ref(out, "goals", d["goal_id"])
        if goal["status"] != "OPEN":
            raise GateError("Cannot frame a blocked or closed goal")
        for key in ("reality", "target", "intervention", "control", "influence", "responsibility"):
            string(d[key], key)
        for key in ("unknowns", "harm_checks"):
            if not isinstance(d[key], list) or not d[key] or any(not isinstance(v, str) or not v.strip() for v in d[key]):
                raise GateError(f"{key} must be a nonempty text list")
        if not isinstance(d["conditions"], list) or not d["conditions"]:
            raise GateError("conditions must be a nonempty list")
        for condition in d["conditions"]:
            if not isinstance(condition, dict) or set(condition) != {"description", "role", "status"}:
                raise GateError("Condition needs description, role and status")
            string(condition["description"], "condition description")
            if condition["role"] not in ("CAUSE", "CONDITION", "TRIGGER", "MAINTAINER", "AMPLIFIER", "FEEDBACK", "UNKNOWN"):
                raise GateError("Invalid condition role")
            if condition["status"] != "HYPOTHESIS":
                raise GateError("A condition cannot be declared proven in this first version")
        d["domain_id"] = goal["domain_id"]
        d["status"] = "OPEN_HYPOTHESES"
        add(out, "problems", d)

    elif kind == "record_source":
        need(d, "id", "domain_id", "uri", "captured_at", "kind", "rights_status")
        ref(out, "domains", d["domain_id"])
        string(d["uri"], "uri")
        if parse_time(d["captured_at"]) > parse_time(event_time):
            raise GateError("Source capture time cannot be in the future")
        if d["kind"] not in ("FIRST_PARTY", "THIRD_PARTY", "PUBLIC", "SYNTHETIC"):
            raise GateError("Invalid source kind")
        if d["rights_status"] not in ("CLEAR", "UNKNOWN", "RESTRICTED"):
            raise GateError("Invalid rights status")
        add(out, "sources", d)

    elif kind == "record_evidence":
        need(d, "id", "domain_id", "source_id", "statement", "observed_at")
        source = ref(out, "sources", d["source_id"])
        if d["domain_id"] != source["domain_id"]:
            raise GateError("Evidence cannot cross domain boundaries")
        string(d["statement"], "statement")
        if parse_time(d["observed_at"]) > parse_time(event_time):
            raise GateError("Evidence observation time cannot be in the future")
        if "value" in d:
            d["value"] = number(d["value"], "value")
            string(d.get("metric"), "metric")
        d["verification"] = "DECLARED_UNVERIFIED"
        add(out, "evidence", d)

    elif kind == "register_procedure":
        need(d, "id", "domain_id", "provider_id", "version", "method")
        ref(out, "domains", d["domain_id"])
        ref(out, "providers", d["provider_id"])
        string(d["version"], "version")
        string(d["method"], "method")
        add(out, "procedures", d)

    elif kind == "propose_claim":
        need(d, "id", "problem_id", "provider_id", "statement", "evidence_ids", "alternative", "falsifier")
        problem = ref(out, "problems", d["problem_id"])
        if out["goals"][problem["goal_id"]]["status"] != "OPEN":
            raise GateError("Cannot propose under a blocked or closed goal")
        ref(out, "providers", d["provider_id"])
        for key in ("statement", "alternative", "falsifier"):
            string(d[key], key)
        for eid in _list_of_refs(out, "evidence", d["evidence_ids"]):
            if out["evidence"][eid]["domain_id"] != problem["domain_id"]:
                raise GateError("Claim evidence cannot cross domain boundaries")
        d["domain_id"] = problem["domain_id"]
        d["epistemic_status"] = "HYPOTHESIS"
        add(out, "claims", d)

    elif kind == "register_prediction":
        need(d, "id", "claim_id", "procedure_id", "metric", "unit", "lower", "upper", "due_at", "resolution_method")
        claim = ref(out, "claims", d["claim_id"])
        procedure = ref(out, "procedures", d["procedure_id"])
        if procedure["domain_id"] != claim["domain_id"]:
            raise GateError("Procedure cannot predict in another domain")
        if new_write:
            seated = {claim["provider_id"]}
            seated |= {r["critic_provider_id"] for r in out["reviews"].values() if r["claim_id"] == d["claim_id"]}
            seated |= {a["adjudicator_provider_id"] for a in out["adjudications"].values() if a["claim_id"] == d["claim_id"]}
            if procedure["provider_id"] in seated:
                raise GateError("Predictor must not be the proposer, critic or adjudicator of the same claim")
        for key in ("metric", "unit", "resolution_method"):
            string(d[key], key)
        lower, upper = number(d["lower"], "lower"), number(d["upper"], "upper")
        if lower > upper:
            raise GateError("Prediction interval is inverted")
        if parse_time(d["due_at"]) <= parse_time(event_time):
            raise GateError("Prediction due_at must be later than preregistration")
        d["lower"], d["upper"] = lower, upper
        d["domain_id"] = claim["domain_id"]
        d["registered_at"] = event_time
        d["status"] = "REGISTERED"
        add(out, "predictions", d)

    elif kind == "freeze_prediction":
        need(d, "prediction_id")
        prediction = ref(out, "predictions", d["prediction_id"])
        if prediction["status"] != "REGISTERED":
            raise GateError("Prediction must be registered and unresolved")
        prediction["status"] = "FROZEN"
        prediction["frozen_at"] = event_time

    elif kind == "record_resolution":
        need(d, "id", "prediction_id", "evidence_id")
        prediction = ref(out, "predictions", d["prediction_id"])
        evidence = ref(out, "evidence", d["evidence_id"])
        if prediction["status"] != "FROZEN":
            raise GateError("A frozen preregistration is required before resolution")
        if evidence["domain_id"] != prediction["domain_id"] or evidence.get("metric") != prediction["metric"]:
            raise GateError("Outcome evidence domain/metric mismatch")
        if "value" not in evidence:
            raise GateError("Outcome evidence must include a numeric value")
        if parse_time(evidence["observed_at"]) <= parse_time(prediction["frozen_at"]):
            raise GateError("Outcome observation must be after prediction freeze")
        if parse_time(evidence["observed_at"]) < parse_time(prediction["due_at"]):
            raise GateError("Cannot resolve before the preregistered due time")
        actual = evidence["value"]
        d.update({"claim_id": prediction["claim_id"], "domain_id": prediction["domain_id"],
                  "actual": actual, "interval_hit": prediction["lower"] <= actual <= prediction["upper"],
                  "absolute_midpoint_error": abs(actual - (prediction["lower"] + prediction["upper"]) / 2),
                  "scored_at": event_time, "attribution": "NOT_ESTABLISHED"})
        add(out, "resolutions", d)
        prediction["status"] = "RESOLVED"

    elif kind == "review_claim":
        need(d, "id", "claim_id", "critic_provider_id", "verdict", "reason")
        claim = ref(out, "claims", d["claim_id"])
        ref(out, "providers", d["critic_provider_id"])
        predictors = {out["procedures"][p["procedure_id"]]["provider_id"]
                      for p in out["predictions"].values() if p["claim_id"] == d["claim_id"]}
        if d["critic_provider_id"] == claim["provider_id"] or d["critic_provider_id"] in predictors:
            raise GateError("Proposer or predictor cannot critique their own claim")
        if d["verdict"] not in ("ACCEPT_FOR_TRIAL", "HOLD", "REVISE"):
            raise GateError("Invalid review verdict")
        string(d["reason"], "reason")
        d["domain_id"] = claim["domain_id"]
        add(out, "reviews", d)

    elif kind == "adjudicate_claim":
        need(d, "id", "claim_id", "review_id", "adjudicator_provider_id", "verdict", "reason")
        claim = ref(out, "claims", d["claim_id"])
        review = ref(out, "reviews", d["review_id"])
        ref(out, "providers", d["adjudicator_provider_id"])
        if review["claim_id"] != d["claim_id"]:
            raise GateError("Review belongs to another claim")
        predictors = {out["procedures"][p["procedure_id"]]["provider_id"]
                      for p in out["predictions"].values() if p["claim_id"] == d["claim_id"]}
        if d["adjudicator_provider_id"] in (claim["provider_id"], review["critic_provider_id"]) or d["adjudicator_provider_id"] in predictors:
            raise GateError("Adjudicator must occupy a distinct seat")
        if d["verdict"] not in ("ACCEPT_FOR_TRIAL", "HOLD", "REVISE"):
            raise GateError("Invalid adjudication verdict")
        if d["verdict"] == "ACCEPT_FOR_TRIAL" and review["verdict"] != "ACCEPT_FOR_TRIAL":
            raise GateError("An unresolved critical objection blocks acceptance")
        string(d["reason"], "reason")
        d["domain_id"] = claim["domain_id"]
        add(out, "adjudications", d)

    elif kind == "propose_lesson":
        need(d, "id", "claim_id", "statement", "limits", "prediction_ids", "adjudication_id")
        claim = ref(out, "claims", d["claim_id"])
        adj = ref(out, "adjudications", d["adjudication_id"])
        if adj["claim_id"] != d["claim_id"]:
            raise GateError("Adjudication belongs to another claim")
        for key in ("statement", "limits"):
            string(d[key], key)
        pids = _list_of_refs(out, "predictions", d["prediction_ids"])
        if not pids or any(out["predictions"][p]["claim_id"] != d["claim_id"] for p in pids):
            raise GateError("Lesson needs predictions of its claim")
        d["domain_id"] = claim["domain_id"]
        d["status"] = "CANDIDATE"
        add(out, "lessons", d)

    elif kind == "activate_trial_lesson":
        need(d, "lesson_id", "owner_ack", "scope")
        lesson = ref(out, "lessons", d["lesson_id"])
        if lesson["status"] != "CANDIDATE" or d["owner_ack"] != "HUMAN_OWNER_APPROVED":
            raise GateError("Only the human Owner may authorize a candidate trial rule")
        string(d["scope"], "scope")
        adj = out["adjudications"][lesson["adjudication_id"]]
        if adj["verdict"] != "ACCEPT_FOR_TRIAL":
            raise GateError("Adjudication has not accepted this claim for trial")
        pids = lesson["prediction_ids"]
        if len(pids) < 2 or any(out["predictions"][p]["status"] != "RESOLVED" for p in pids):
            raise GateError("At least two resolved preregistered predictions are required")
        outcome_sources = []
        for pid in pids:
            resolution = next(r for r in out["resolutions"].values() if r["prediction_id"] == pid)
            source_id = out["evidence"][resolution["evidence_id"]]["source_id"]
            outcome_sources.append(source_id)
        if len(set(outcome_sources)) < 2 or any(
            out["sources"][sid]["kind"] != "FIRST_PARTY" or out["sources"][sid]["rights_status"] != "CLEAR"
            for sid in outcome_sources
        ):
            raise GateError("Trial rule needs distinct declared first-party outcome sources with clear rights")
        if out["domains"][lesson["domain_id"]]["risk_class"] == "HIGH_STAKES":
            raise GateError("High-stakes domain rules need a separate expert and Owner gate; not implemented in v0.1")
        lesson["status"] = "TRIAL_RULE"
        lesson["scope"] = d["scope"]
        lesson["activated_at"] = event_time
        lesson["validation"] = "DECLARED_DATA_ONLY_NOT_CAUSAL_PROOF"

    elif kind == "record_external_case":
        need(d, "id", "domain_id", "evidence_ids", "outcome", "context",
             "mechanism_hypothesis", "transfer_limits", "uncertainty")
        ref(out, "domains", d["domain_id"])
        if d["outcome"] not in ("SUCCESS", "FAILURE", "MIXED"):
            raise GateError("External case outcome must be SUCCESS, FAILURE or MIXED")
        for key in ("context", "mechanism_hypothesis", "transfer_limits", "uncertainty"):
            string(d[key], key)
        eids = _list_of_refs(out, "evidence", d["evidence_ids"])
        if not eids:
            raise GateError("External case needs at least one evidence record")
        if any(out["evidence"][eid]["domain_id"] != d["domain_id"] for eid in eids):
            raise GateError("External case evidence cannot cross domain boundaries")
        cases = out.setdefault("external_cases", {})
        d["capital_status"] = "EXTERNAL_CASE_CAPITAL_UNVERIFIED"
        d["lesson_eligible"] = False
        d["recorded_at"] = event_time
        add(out, "external_cases", d)

    elif kind == "freeze_learning_packet":
        need(d, "id", "trace_id", "claim_id", "counterevidence_ids", "external_case_ids",
             "counterevidence_note", "context_contract", "instruction_version", "toolset_fingerprint")
        identifier(d["trace_id"], "trace_id")
        claim = ref(out, "claims", d["claim_id"])
        for key in ("counterevidence_note", "context_contract", "instruction_version", "toolset_fingerprint"):
            string(d[key], key)
        counter_ids = _list_of_refs(out, "evidence", d["counterevidence_ids"])
        if any(out["evidence"][eid]["domain_id"] != claim["domain_id"] for eid in counter_ids):
            raise GateError("Counterevidence cannot cross domain boundaries")
        external_cases = out.setdefault("external_cases", {})
        if not isinstance(d["external_case_ids"], list) or any(not isinstance(v, str) for v in d["external_case_ids"]) or len(set(d["external_case_ids"])) != len(d["external_case_ids"]):
            raise GateError("external_case_ids must be a unique list")
        for case_id in d["external_case_ids"]:
            identifier(case_id, "external case ID")
            if case_id not in external_cases:
                raise GateError(f"Unknown external_cases ID: {case_id}")
            if external_cases[case_id]["domain_id"] != claim["domain_id"]:
                raise GateError("Learning packet external cases cannot cross domain boundaries")
        supporting_ids = list(claim["evidence_ids"])
        source_ids = sorted({
            out["evidence"][eid]["source_id"] for eid in supporting_ids + counter_ids
        })
        packet_target = {
            "claim_id": claim["id"],
            "statement": claim["statement"],
            "alternative": claim["alternative"],
            "falsifier": claim["falsifier"],
            "domain_id": claim["domain_id"],
        }
        packet_evidence = {
            "supporting": [out["evidence"][eid] for eid in supporting_ids],
            "counterevidence": [out["evidence"][eid] for eid in counter_ids],
            "sources": [out["sources"][sid] for sid in source_ids],
            "external_cases": [external_cases[cid] for cid in d["external_case_ids"]],
        }
        d["domain_id"] = claim["domain_id"]
        d["supporting_evidence_ids"] = supporting_ids
        d["target_hash"] = digest(packet_target)
        d["evidence_bundle_hash"] = digest(packet_evidence)
        d["status"] = "FROZEN"
        d["frozen_at"] = event_time
        packets = out.setdefault("learning_packets", {})
        add(out, "learning_packets", d)

    elif kind == "record_critic_execution":
        need(d, "id", "packet_id", "critic_provider_id", "provider", "model", "run_id",
             "context_mode", "output_hash", "verdict", "reason", "missing_evidence")
        packets = out.setdefault("learning_packets", {})
        packet = ref(out, "learning_packets", d["packet_id"])
        claim = ref(out, "claims", packet["claim_id"])
        ref(out, "providers", d["critic_provider_id"])
        predictors = {out["procedures"][p["procedure_id"]]["provider_id"]
                      for p in out["predictions"].values() if p["claim_id"] == packet["claim_id"]}
        if d["critic_provider_id"] == claim["provider_id"] or d["critic_provider_id"] in predictors:
            raise GateError("Critic execution must be distinct from proposer and predictors")
        for key in ("provider", "model", "run_id", "output_hash", "reason"):
            string(d[key], key)
        if d["context_mode"] not in ("BLIND", "REVEALED"):
            raise GateError("context_mode must be BLIND or REVEALED")
        if d["verdict"] not in ("FINDINGS", "NO_MATERIAL_DEFECT", "BLOCKED", "ABSTAIN", "REVIEW_INCOMPLETE"):
            raise GateError("Invalid critic execution verdict")
        if not isinstance(d["missing_evidence"], list) or any(not isinstance(v, str) or not v.strip() for v in d["missing_evidence"]):
            raise GateError("missing_evidence must be a text list")
        d["domain_id"] = packet["domain_id"]
        d["target_hash"] = packet["target_hash"]
        d["evidence_bundle_hash"] = packet["evidence_bundle_hash"]
        d["recorded_at"] = event_time
        executions = out.setdefault("critic_executions", {})
        add(out, "critic_executions", d)

    elif kind == "record_negative_control":
        need(d, "id", "packet_id", "description", "expected", "observed", "result", "evidence_ids")
        packets = out.setdefault("learning_packets", {})
        packet = ref(out, "learning_packets", d["packet_id"])
        for key in ("description", "expected", "observed"):
            string(d[key], key)
        if d["result"] not in ("PASS", "FAIL", "INCONCLUSIVE"):
            raise GateError("Negative control result must be PASS, FAIL or INCONCLUSIVE")
        eids = _list_of_refs(out, "evidence", d["evidence_ids"])
        if any(out["evidence"][eid]["domain_id"] != packet["domain_id"] for eid in eids):
            raise GateError("Negative control evidence cannot cross domain boundaries")
        d["domain_id"] = packet["domain_id"]
        d["recorded_at"] = event_time
        controls = out.setdefault("negative_controls", {})
        add(out, "negative_controls", d)

    elif kind == "record_trace_link":
        need(d, "id", "trace_id", "artifact_type", "artifact_id", "relation")
        identifier(d["trace_id"], "trace_id")
        if d["artifact_type"] not in TRACE_ARTIFACT_COLLECTIONS:
            raise GateError("Invalid trace artifact type")
        if d["relation"] not in TRACE_RELATIONS:
            raise GateError("Invalid trace relation")
        collection = TRACE_ARTIFACT_COLLECTIONS[d["artifact_type"]]
        artifact_id = identifier(d["artifact_id"], "artifact ID")
        artifacts = out.get(collection, {})
        if artifact_id not in artifacts:
            raise GateError(f"Unknown traced artifact: {d['artifact_type']}:{artifact_id}")
        d["recorded_at"] = event_time
        d["artifact_digest"] = digest(artifacts[artifact_id])
        links = out.setdefault("trace_links", {})
        add(out, "trace_links", d)

    elif kind == "schedule_lesson_revalidation":
        need(d, "id", "lesson_id", "review_after", "staleness_conditions", "reason")
        lesson = ref(out, "lessons", d["lesson_id"])
        review_after = parse_time(d["review_after"])
        if review_after <= parse_time(event_time):
            raise GateError("review_after must be in the future when scheduled")
        if not isinstance(d["staleness_conditions"], list) or not d["staleness_conditions"] or any(
            not isinstance(v, str) or not v.strip() for v in d["staleness_conditions"]
        ):
            raise GateError("staleness_conditions must be a nonempty text list")
        string(d["reason"], "reason")
        d["domain_id"] = lesson["domain_id"]
        d["scheduled_at"] = event_time
        schedules = out.setdefault("lesson_revalidation_schedules", {})
        add(out, "lesson_revalidation_schedules", d)

    elif kind == "record_lesson_revalidation":
        need(d, "id", "schedule_id", "evidence_ids", "outcome", "reason", "limits", "trigger")
        schedules = out.setdefault("lesson_revalidation_schedules", {})
        schedule = ref(out, "lesson_revalidation_schedules", d["schedule_id"])
        lesson = ref(out, "lessons", schedule["lesson_id"])
        if d["outcome"] not in ("RETAIN", "NARROW", "RETIRE", "INCONCLUSIVE"):
            raise GateError("Invalid lesson revalidation outcome")
        if d["trigger"] not in ("SCHEDULED", "STALE_SIGNAL", "OWNER_REQUEST"):
            raise GateError("Invalid lesson revalidation trigger")
        for key in ("reason", "limits"):
            string(d[key], key)
        eids = _list_of_refs(out, "evidence", d["evidence_ids"])
        if any(out["evidence"][eid]["domain_id"] != lesson["domain_id"] for eid in eids):
            raise GateError("Lesson revalidation evidence cannot cross domain boundaries")
        if d["trigger"] == "SCHEDULED" and parse_time(event_time) < parse_time(schedule["review_after"]):
            raise GateError("Scheduled revalidation cannot run before review_after")
        d["lesson_id"] = lesson["id"]
        d["domain_id"] = lesson["domain_id"]
        d["recorded_at"] = event_time
        d["status"] = "PROPOSAL_ONLY"
        d["automatic_lesson_mutation"] = False
        revalidations = out.setdefault("lesson_revalidations", {})
        add(out, "lesson_revalidations", d)

    elif kind == "set_learning_focus":
        # The collection is created lazily so ledgers written before this type still replay
        # to a state identical to their existing snapshot.
        focuses = out.setdefault("learning_focuses", {})
        if d.get("status") == "ACTIVE":
            if set(d) != FOCUS_ACTIVE_FIELDS:
                raise GateError("ACTIVE focus needs exactly: " + ", ".join(sorted(FOCUS_ACTIVE_FIELDS)))
            ref(out, "domains", d["domain_id"])
            source = ref(out, "sources", d["source_id"])
            if source["domain_id"] != d["domain_id"]:
                raise GateError("Focus source cannot cross domain boundaries")
            for key in ("note", "expected_lesson", "uncertainty"):
                string(d[key], key)
            for previous in focuses.values():
                if previous["status"] == "ACTIVE":
                    previous.update({"status": "SUPERSEDED", "ended_at": event_time, "superseded_by": d["id"]})
            d["started_at"] = event_time
            d["expectation_status"] = "UNTESTED_EXPECTATION"
            add(out, "learning_focuses", d)
        elif d.get("status") == "STOPPED":
            if set(d) != FOCUS_STOPPED_FIELDS:
                raise GateError("STOPPED focus needs exactly: " + ", ".join(sorted(FOCUS_STOPPED_FIELDS)))
            focus = ref(out, "learning_focuses", d["id"])
            if focus["status"] != "ACTIVE":
                raise GateError("Only the active focus can be stopped")
            string(d["reason"], "reason")
            focus.update({"status": "STOPPED", "ended_at": event_time, "stop_reason": d["reason"]})
        else:
            raise GateError("Focus status must be ACTIVE or STOPPED")

    else:
        raise GateError(f"Unknown command type: {kind}")
    return out


class Ledger:
    """Single-writer JSONL hash chain; the state file is a derived cache."""

    def __init__(self, home: str | Path):
        self.home = Path(home)
        self.events = self.home / "events.jsonl"
        self.snapshot = self.home / "state.json"
        self.lock = self.home / ".writer.lock"

    def init(self) -> None:
        if self.home.exists() and any(self.home.iterdir()):
            raise GateError("Home is not empty; refusing to overwrite")
        self.home.mkdir(parents=True, exist_ok=True)
        self.events.write_bytes(b"")
        self._save(initial_state(), 0, "0" * 64)

    def replay(self) -> tuple[dict, int, str]:
        if not self.events.exists():
            raise GateError("Ledger missing; run init")
        state, previous, count = initial_state(), "0" * 64, 0
        with self.events.open("r", encoding="utf-8") as fh:
            for raw in fh:
                count += 1
                try:
                    event = json.loads(raw)
                    if set(event) - {"approved_by"} != {"seq", "prev", "at", "command", "hash"}:
                        raise GateError("Unexpected event fields")
                    # approved_by is optional (absent in ledgers written before it existed) and,
                    # when present, is part of the hashed body so editing it breaks the chain.
                    body = {k: event[k] for k in ("seq", "prev", "at", "command", "approved_by") if k in event}
                    if "approved_by" in event:
                        identifier(event["approved_by"], "approved_by")
                    if event["seq"] != count or event["prev"] != previous or digest(body) != event["hash"]:
                        raise GateError("Event chain mismatch")
                    state = evolve(state, event["command"], event["at"], new_write=False)
                    previous = event["hash"]
                except (ValueError, TypeError, KeyError) as exc:
                    raise GateError(f"Invalid event at line {count}: {exc}") from exc
        return state, count, previous

    def verify(self) -> tuple[dict, int, str]:
        state, count, head = self.replay()
        try:
            cached = json.loads(self.snapshot.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise GateError("Snapshot missing or invalid; run repair_snapshot") from exc
        if cached != {"event_count": count, "head": head, "state": state}:
            raise GateError("Snapshot differs from event ledger; run repair_snapshot after audit")
        return state, count, head

    def _save(self, state: dict, count: int, head: str) -> None:
        contents = {"event_count": count, "head": head, "state": state}
        fd, path = tempfile.mkstemp(prefix="state-", suffix=".tmp", dir=self.home)
        try:
            with os.fdopen(fd, "wb") as fh:
                fh.write(canonical(contents) + b"\n")
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(path, self.snapshot)
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def repair_snapshot(self, *, actor: str | None = None, secret: str | None = None) -> tuple[int, str]:
        """Rebuild derived state only after authenticating against the fixed Owner config."""
        from .owner import config_path, require_owner
        approved_by = require_owner(actor, secret, config_path(None))
        state, count, head = self.replay()
        self._save(state, count, head)
        return count, head

    def apply(self, command: dict, *, actor: str | None = None, secret: str | None = None) -> dict:
        """Append one command only after authenticating against the fixed Owner config.

        The authentication happens inside the mutation boundary, so direct Python callers
        cannot bypass the Owner gate merely by supplying an owner id.
        """
        from .owner import config_path, require_owner
        approved_by = require_owner(actor, secret, config_path(None))
        self.home.mkdir(parents=True, exist_ok=True)
        try:
            fd = os.open(self.lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError as exc:
            raise GateError("Another writer holds the ledger lock") from exc
        try:
            os.close(fd)
            state, count, head = self.verify()
            at = utcnow()
            updated = evolve(state, command, at)
            body = {"seq": count + 1, "prev": head, "at": at, "command": command}
            if approved_by is not None:
                body["approved_by"] = approved_by
            event = {**body, "hash": digest(body)}
            with self.events.open("ab") as fh:
                fh.write(canonical(event) + b"\n")
                fh.flush()
                os.fsync(fh.fileno())
            self._save(updated, count + 1, event["hash"])
            return {"event_count": count + 1, "head": event["hash"], "state": updated}
        finally:
            self.lock.unlink(missing_ok=True)


def current_focus(state: dict) -> dict | None:
    """Return the single ACTIVE learning focus, or None. History is never removed."""
    for focus in state.get("learning_focuses", {}).values():
        if focus["status"] == "ACTIVE":
            return focus
    return None


def next_goal(state: dict) -> dict:
    eligible = [g for g in state["goals"].values() if g["status"] == "OPEN"]
    if not eligible:
        return {"status": "WAIT", "reason": "No eligible open goal"}
    return {"status": "READY", "goal": sorted(eligible, key=lambda g: (-g["priority"], g["id"]))[0]}
