"""Offline canary scoring harness for external critics."""
from __future__ import annotations

from typing import Any, Iterable


class CanaryScoringError(ValueError):
    pass


def _span_tuple(value: Any) -> tuple[int, int]:
    if (
        not isinstance(value, (list, tuple))
        or len(value) != 2
        or type(value[0]) is not int
        or type(value[1]) is not int
        or value[0] < 0
        or value[1] <= value[0]
    ):
        raise CanaryScoringError("span must be [start, end] integers with end > start")
    return int(value[0]), int(value[1])


def span_overlap(a: Any, b: Any) -> bool:
    a0, a1 = _span_tuple(a)
    b0, b1 = _span_tuple(b)
    return max(a0, b0) < min(a1, b1)


def _validate_ground_truth(truth: dict[str, Any]) -> None:
    roles = [truth.get("trap_author"), truth.get("rubric_author"), truth.get("adjudicator")]
    if any(not isinstance(role, str) or not role.strip() for role in roles):
        raise CanaryScoringError("trap_author, rubric_author and adjudicator are required")
    if len(set(roles)) != 3:
        raise CanaryScoringError("trap author, rubric author and adjudicator must be distinct")
    if truth.get("human_adjudicated") is not True:
        raise CanaryScoringError("human adjudication is required")
    if truth.get("origin") not in {"HISTORICAL_DEFECT", "INDEPENDENT_TRAP", "CLEAN_HARD_NEGATIVE"}:
        raise CanaryScoringError("ground truth origin is invalid")


def score_canary_case(case: dict[str, Any], critic_result: dict[str, Any]) -> dict[str, Any]:
    truth = case.get("ground_truth")
    if not isinstance(truth, dict):
        raise CanaryScoringError("ground_truth is required")
    _validate_ground_truth(truth)

    has_defect = bool(truth.get("has_defect"))
    verdict = critic_result.get("verdict")
    predicted_defect = verdict == "DEFECT_FOUND"

    correct_verdict = predicted_defect == has_defect
    localization_hit = True
    if has_defect:
        truth_span = truth.get("target_span")
        findings = critic_result.get("findings", [])
        localization_hit = any(
            isinstance(item, dict)
            and item.get("defect_type") == truth.get("defect_type")
            and span_overlap(item.get("target_span"), truth_span)
            for item in findings
        )

    return {
        "case_id": case.get("case_id"),
        "class": case.get("class"),
        "has_defect": has_defect,
        "correct_verdict": correct_verdict,
        "localization_hit": localization_hit,
        "accepted_bad_case": has_defect and not predicted_defect,
        "rejected_clean_case": (not has_defect) and predicted_defect,
        "subtle_error": case.get("class") == "SUBTLE_EPISTEMIC",
        "hard_negative": truth.get("origin") == "CLEAN_HARD_NEGATIVE",
        "historical_defect": truth.get("origin") == "HISTORICAL_DEFECT",
        "human_adjudicated": True,
    }


def summarize_canary_scores(
    scored: Iterable[dict[str, Any]],
    *,
    preregistered_max_far: float,
    preregistered_min_subtle_detection: float,
) -> dict[str, Any]:
    rows = list(scored)
    bad = [r for r in rows if r["has_defect"]]
    clean = [r for r in rows if not r["has_defect"]]
    subtle = [r for r in bad if r["subtle_error"]]

    far = (sum(1 for r in bad if r["accepted_bad_case"]) / len(bad)) if bad else None
    frr = (sum(1 for r in clean if r["rejected_clean_case"]) / len(clean)) if clean else None
    localization = (
        sum(1 for r in bad if r["localization_hit"]) / len(bad)
        if bad else None
    )
    subtle_detection = (
        sum(1 for r in subtle if r["correct_verdict"] and r["localization_hit"]) / len(subtle)
        if subtle else None
    )
    human_coverage = (
        sum(1 for r in rows if r.get("human_adjudicated") is True) / len(rows)
        if rows else None
    )
    hard_negative_count = sum(1 for r in rows if r.get("hard_negative"))
    historical_defect_count = sum(1 for r in rows if r.get("historical_defect"))

    pass_gate = (
        far is not None
        and subtle_detection is not None
        and far <= preregistered_max_far
        and subtle_detection >= preregistered_min_subtle_detection
        and human_coverage == 1.0
        and hard_negative_count > 0
        and historical_defect_count > 0
    )
    return {
        "case_count": len(rows),
        "bad_case_count": len(bad),
        "clean_case_count": len(clean),
        "false_acceptance_rate": far,
        "false_rejection_rate": frr,
        "defect_localization_rate": localization,
        "subtle_detection_rate": subtle_detection,
        "human_adjudication_coverage": human_coverage,
        "hard_negative_count": hard_negative_count,
        "historical_defect_count": historical_defect_count,
        "preregistered_max_far": preregistered_max_far,
        "preregistered_min_subtle_detection": preregistered_min_subtle_detection,
        "pass": pass_gate,
    }
