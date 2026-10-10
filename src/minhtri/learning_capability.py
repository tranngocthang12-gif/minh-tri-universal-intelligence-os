"""Pure candidate evidence contracts for understanding and novel-case transfer.

These checks enforce record shape and provenance *claims*, not understanding,
truth, independent reviewer identity, actual test secrecy, or Owner acceptance.
"""
from __future__ import annotations

import math
import re
from collections.abc import Mapping, Sequence
from typing import Any


SKELETON_FIELDS = frozenset({
    "core_proposition", "conditions", "mechanism_or_structure", "scope_boundary",
    "non_claims", "uncertainty", "counter_reading", "source_vs_interpretation",
})
TRIAL_FIELDS = frozenset({
    "schema", "track_id", "candidate_cursor_id", "trial_ref", "frozen_case_ref",
    "frozen_case_sha256", "rubric_ref", "rubric_sha256",
    "frozen_before_attempt_ref", "baseline_attempt_ref", "candidate_attempt_ref",
    "independent_review_ref", "generator_seat", "reviewer_seat",
    "baseline_score", "candidate_score", "baseline_safety_violations",
    "candidate_safety_violations", "status",
})
TRIAL_SCHEMA = "minhtri-learning-transfer-trial/v1"
TRIAL_STATUS = "RECORDED_NOT_VERIFIED"
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_REF = re.compile(r"^[a-z][a-z0-9_-]{1,31}:[A-Za-z0-9][A-Za-z0-9._/-]{0,191}$")
_INTERPRETATIONS = {
    "SOURCE_REPORT", "BOUNDED_SYNTHESIS", "UNCERTAIN_INTERPRETATION",
}


class CapabilityEvidenceError(ValueError):
    """A claimed understanding or transfer *record* fails validation."""


def _require(ok: bool, message: str) -> None:
    if not ok:
        raise CapabilityEvidenceError(message)


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _texts(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(_text(v) for v in value)


def _safe_ref(value: Any) -> bool:
    return (isinstance(value, str) and _REF.fullmatch(value) is not None
            and all(part not in ("", ".", "..") for part in value.split(":", 1)[1].split("/")))


def validate_semantic_skeleton(value: Mapping[str, Any]) -> None:
    """Validate a bounded meaning sketch, not whether its claims are true."""
    _require(isinstance(value, Mapping) and set(value) == SKELETON_FIELDS,
             "semantic skeleton requires its exact fields")
    for name in ("core_proposition", "mechanism_or_structure", "scope_boundary",
                 "uncertainty", "counter_reading"):
        _require(_text(value[name]), f"semantic skeleton missing {name}")
    for name in ("conditions", "non_claims"):
        _require(_texts(value[name]), f"semantic skeleton missing {name}")
    _require(value["source_vs_interpretation"] in _INTERPRETATIONS,
             "semantic skeleton cannot self-classify as VERIFIED")


def validate_transfer_trial(trial: Mapping[str, Any]) -> None:
    """Check comparator metadata without attesting real-world authenticity."""
    _require(isinstance(trial, Mapping) and set(trial) == TRIAL_FIELDS,
             "transfer trial missing or shadow fields")
    _require(trial["schema"] == TRIAL_SCHEMA, "unsupported transfer-trial schema")
    for name in ("track_id", "candidate_cursor_id", "generator_seat", "reviewer_seat"):
        _require(_text(trial[name]), f"transfer trial missing {name}")
    for name in ("trial_ref", "frozen_case_ref", "rubric_ref",
                 "frozen_before_attempt_ref", "baseline_attempt_ref",
                 "candidate_attempt_ref", "independent_review_ref"):
        _require(_safe_ref(trial[name]), f"transfer trial unsafe reference {name}")
    for name in ("frozen_case_sha256", "rubric_sha256"):
        _require(isinstance(trial[name], str) and _SHA256.fullmatch(trial[name]) is not None,
                 f"transfer trial malformed {name}")
    _require(trial["generator_seat"] != trial["reviewer_seat"],
             "transfer trial self-reviewed (declared seat)")
    _require(trial["baseline_attempt_ref"] != trial["candidate_attempt_ref"],
             "baseline and candidate must be separate attempts")
    _require(trial["status"] == TRIAL_STATUS,
             "transfer trial may not claim VERIFIED or ACCEPTED")
    for name in ("baseline_score", "candidate_score"):
        score = trial[name]
        _require(type(score) in (float, int) and math.isfinite(score) and 0 <= score <= 1,
                 f"transfer trial invalid score {name}")
    for name in ("baseline_safety_violations", "candidate_safety_violations"):
        score = trial[name]
        _require(type(score) is int and score >= 0,
                 f"transfer trial invalid safety violation count {name}")


def validate_application_trial_binding(delta: Mapping[str, Any],
                                       trial: Mapping[str, Any]) -> None:
    """Bind a separate sealed-case record to a non-accepted learning delta.

    Does not verify that a purported frozen rubric predated an attempt; an
    independent reviewer must examine timestamps, source objects and identity.
    """
    validate_transfer_trial(trial)
    _require(isinstance(delta, Mapping) and isinstance(delta.get("application"), Mapping)
             and isinstance(delta.get("provenance"), Mapping),
             "missing delta application/provenance")
    app = delta["application"]
    _require(app.get("status") in {
        "INDEPENDENT_REVIEW_RECORDED_NOT_VERIFIED",
        "FAILURE_RECORDED_NOT_VERIFIED", "INCONCLUSIVE",
    }, "no externally reviewable application receipt")
    bindings = (
        (trial["track_id"], delta.get("track_id")),
        (trial["trial_ref"], app.get("transfer_trial_ref")),
        (trial["candidate_cursor_id"], delta.get("cursor_id")),
        (trial["generator_seat"], delta["provenance"].get("author_seat")),
        (trial["frozen_case_ref"], app.get("heldout_case_ref")),
        (trial["rubric_ref"], app.get("frozen_rubric_ref")),
        (trial["rubric_sha256"], app.get("frozen_rubric_sha256")),
        (trial["candidate_attempt_ref"], app.get("attempt_ref")),
        (trial["reviewer_seat"], app.get("reviewer_seat")),
        (trial["independent_review_ref"], app.get("review_receipt_ref")),
    )
    _require(all(a is not None and b is not None and a == b for a, b in bindings),
             "transfer trial and delta evidence references do not match")


def transfer_observation(trial: Mapping[str, Any]) -> dict[str, Any]:
    """A paired observation, never proof of causal learning or skill promotion."""
    validate_transfer_trial(trial)
    better = (trial["candidate_score"] > trial["baseline_score"] and
              trial["candidate_safety_violations"] <=
              trial["baseline_safety_violations"])
    return {
        "outcome": "OBSERVED_SIGNAL_NOT_VERIFIED" if better else
                   "NO_ELIGIBLE_SIGNAL_OBSERVED",
        "score_difference": round(trial["candidate_score"] - trial["baseline_score"], 8),
        "owner_acceptance": False,
        "skill_promoted": False,
        "actual_independence_verified": False,
        "heldout_integrity_verified": False,
        "causal_learning_proven": False,
    }


def summarize_transfer_trials(trials: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Aggregate distinct cases; require two, still do not promote abilities."""
    _require(not isinstance(trials, (str, bytes)) and len(trials) >= 2,
             "at least two distinct held-out cases required")
    case_refs = set()
    for item in trials:
        validate_transfer_trial(item)
        _require(item["frozen_case_ref"] not in case_refs,
                 "duplicate held-out case counted twice")
        case_refs.add(item["frozen_case_ref"])
    outcome = [transfer_observation(item) for item in trials]
    delta = sum(item["score_difference"] for item in outcome) / len(outcome)
    any_regression = any(item["candidate_safety_violations"] >
                         item["baseline_safety_violations"] for item in trials)
    return {
        "cases": len(outcome),
        "mean_score_difference": round(delta, 8),
        "all_cases_improved_without_safety_regression":
            all(item["outcome"] == "OBSERVED_SIGNAL_NOT_VERIFIED" for item in outcome),
        "any_safety_regression": any_regression,
        "status": "PROVISIONAL_MULTI_CASE_OBSERVATION_NOT_VERIFIED",
        "owner_acceptance": False,
        "skill_promoted": False,
        "independence_and_causal_effect_verified": False,
    }
