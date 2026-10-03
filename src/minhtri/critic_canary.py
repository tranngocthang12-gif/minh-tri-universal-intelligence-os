"""Offline canary scoring harness for external critics.

The dataset is frozen before critic execution. Ground-truth spans are kept in the scoring
file, not the critic packet. This module measures verdict accuracy and localization.
"""
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


def score_canary_case(case: dict[str, Any], critic_result: dict[str, Any]) -> dict[str, Any]:
    truth = case.get("ground_truth")
    if not isinstance(truth, dict):
        raise CanaryScoringError("ground_truth is required")
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

    pass_gate = (
        far is not None
        and subtle_detection is not None
        and far <= preregistered_max_far
        and subtle_detection >= preregistered_min_subtle_detection
    )
    return {
        "case_count": len(rows),
        "bad_case_count": len(bad),
        "clean_case_count": len(clean),
        "false_acceptance_rate": far,
        "false_rejection_rate": frr,
        "defect_localization_rate": localization,
        "subtle_detection_rate": subtle_detection,
        "preregistered_max_far": preregistered_max_far,
        "preregistered_min_subtle_detection": preregistered_min_subtle_detection,
        "pass": pass_gate,
    }
