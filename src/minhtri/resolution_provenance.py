"""Offline resolution-provenance audit harness."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
from typing import Any, Iterable


class ResolutionAuditError(ValueError):
    pass


def _utc(value: Any, label: str) -> datetime:
    if not isinstance(value, str):
        raise ResolutionAuditError(f"{label} must be a timestamp string")
    text = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError as exc:
        raise ResolutionAuditError(f"{label} is not valid ISO-8601") from exc
    if parsed.tzinfo is None:
        raise ResolutionAuditError(f"{label} must include timezone")
    return parsed.astimezone(timezone.utc)


def sha256_text(text: str) -> str:
    if not isinstance(text, str):
        raise ResolutionAuditError("evidence content must be text")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate_resolution_provenance(record: dict[str, Any]) -> dict[str, Any]:
    required = (
        "prediction_id",
        "prediction_hash",
        "prediction_created_at",
        "due_at",
        "evidence_id",
        "evidence_content_hash",
        "evidence_cutoff_timestamp",
        "evidence_source_kind",
        "evidence_transform",
        "resolver_input_contract",
        "resolver_saw_original_resolution",
        "resolver_saw_model_trace",
        "resolver_saw_context_capsule",
        "outcome_captured_at",
        "observed_value",
        "resolver_actor",
        "resolver_method",
        "resolution_created_at",
        "interval_hit",
        "absolute_midpoint_error",
    )
    missing = [key for key in required if key not in record]
    if missing:
        return {"status": "INVALID_PROVENANCE", "reasons": ["MISSING_FIELDS:" + ",".join(missing)]}

    reasons: list[str] = []
    try:
        created = _utc(record["prediction_created_at"], "prediction_created_at")
        due = _utc(record["due_at"], "due_at")
        cutoff = _utc(record["evidence_cutoff_timestamp"], "evidence_cutoff_timestamp")
        captured = _utc(record["outcome_captured_at"], "outcome_captured_at")
        resolved = _utc(record["resolution_created_at"], "resolution_created_at")
    except ResolutionAuditError as exc:
        return {"status": "INVALID_PROVENANCE", "reasons": [str(exc)]}

    if created >= due:
        reasons.append("PREDICTION_NOT_FROZEN_BEFORE_DUE")
    if cutoff < due:
        reasons.append("EVIDENCE_CUTOFF_BEFORE_DUE")
    if captured < due:
        reasons.append("OUTCOME_CAPTURED_BEFORE_DUE")
    if resolved < captured:
        reasons.append("RESOLUTION_PRECEDES_OUTCOME_CAPTURE")

    for key in ("prediction_hash", "evidence_content_hash"):
        value = record.get(key)
        if not isinstance(value, str) or len(value) != 64 or any(ch not in "0123456789abcdef" for ch in value):
            reasons.append(f"INVALID_{key.upper()}")

    if record.get("evidence_source_kind") != "RAW_SOURCE_SNAPSHOT":
        reasons.append("EVIDENCE_NOT_RAW_SOURCE_SNAPSHOT")
    if record.get("evidence_transform") != "NONE":
        reasons.append("EVIDENCE_WAS_TRANSFORMED")
    if record.get("resolver_input_contract") != "FROZEN_PREDICTION_PLUS_RAW_SOURCE_ONLY":
        reasons.append("RESOLVER_INPUT_CONTRACT_INVALID")
    if record.get("resolver_saw_original_resolution") is not False:
        reasons.append("RESOLVER_SAW_ORIGINAL_RESOLUTION")
    if record.get("resolver_saw_model_trace") is not False:
        reasons.append("RESOLVER_SAW_MODEL_TRACE")
    if record.get("resolver_saw_context_capsule") is not False:
        reasons.append("RESOLVER_SAW_CONTEXT_CAPSULE")

    if not str(record.get("resolver_actor", "")).strip():
        reasons.append("MISSING_RESOLVER_ACTOR")
    if not str(record.get("resolver_method", "")).strip():
        reasons.append("MISSING_RESOLVER_METHOD")
    if not isinstance(record.get("interval_hit"), bool):
        reasons.append("INVALID_INTERVAL_HIT")
    if not isinstance(record.get("absolute_midpoint_error"), (int, float)):
        reasons.append("INVALID_MIDPOINT_ERROR")

    return {
        "status": "INVALID_PROVENANCE" if reasons else "VALID_PROVENANCE",
        "reasons": reasons,
        "eligible_for_meta_learning": not reasons,
    }


def verify_evidence_content(record: dict[str, Any], raw_evidence_text: str) -> dict[str, Any]:
    expected = record.get("evidence_content_hash")
    actual = sha256_text(raw_evidence_text)
    return {
        "status": "MATCH" if expected == actual else "HASH_MISMATCH",
        "expected_hash": expected,
        "actual_hash": actual,
        "eligible_for_meta_learning": expected == actual,
    }


def compare_independent_resolution(
    original: dict[str, Any],
    blind_resolution: dict[str, Any],
    *,
    midpoint_tolerance: float = 1e-9,
) -> dict[str, Any]:
    if validate_resolution_provenance(original)["status"] != "VALID_PROVENANCE":
        return {"status": "ORIGINAL_INVALID_PROVENANCE", "agreement": False}
    if validate_resolution_provenance(blind_resolution)["status"] != "VALID_PROVENANCE":
        return {"status": "BLIND_INVALID_PROVENANCE", "agreement": False}

    same_prediction = original["prediction_hash"] == blind_resolution["prediction_hash"]
    same_evidence = original["evidence_content_hash"] == blind_resolution["evidence_content_hash"]
    distinct_resolver = original["resolver_actor"] != blind_resolution["resolver_actor"]
    same_hit = original["interval_hit"] == blind_resolution["interval_hit"]
    same_error = abs(
        float(original["absolute_midpoint_error"]) - float(blind_resolution["absolute_midpoint_error"])
    ) <= midpoint_tolerance

    agreement = same_prediction and same_evidence and distinct_resolver and same_hit and same_error
    return {
        "status": "AGREE" if agreement else "DISAGREE",
        "agreement": agreement,
        "same_prediction": same_prediction,
        "same_evidence": same_evidence,
        "distinct_resolver": distinct_resolver,
        "same_interval_hit": same_hit,
        "same_midpoint_error": same_error,
    }



def cohens_kappa_binary(pairs: Iterable[tuple[bool, bool]]) -> float | None:
    rows = list(pairs)
    if not rows:
        return None
    observed = sum(1 for a, b in rows if a == b) / len(rows)
    p_a_true = sum(1 for a, _ in rows if a) / len(rows)
    p_b_true = sum(1 for _, b in rows if b) / len(rows)
    expected = p_a_true * p_b_true + (1 - p_a_true) * (1 - p_b_true)
    if expected == 1.0:
        return 1.0 if observed == 1.0 else 0.0
    return (observed - expected) / (1 - expected)

def audit_batch(
    pairs: Iterable[tuple[dict[str, Any], dict[str, Any]]],
    *,
    preregistered_min_agreement: float,
    preregistered_max_out_rate: float,
) -> dict[str, Any]:
    if not 0.0 <= preregistered_min_agreement <= 1.0:
        raise ResolutionAuditError("preregistered_min_agreement must be between 0 and 1")
    if not 0.0 <= preregistered_max_out_rate <= 1.0:
        raise ResolutionAuditError("preregistered_max_out_rate must be between 0 and 1")

    comparisons = [compare_independent_resolution(a, b) for a, b in pairs]
    total = len(comparisons)
    eligible = [item for item in comparisons if item["status"] in {"AGREE", "DISAGREE"}]
    out_count = total - len(eligible)
    out_rate = (out_count / total) if total else None

    if not eligible:
        return {
            "status": "INSUFFICIENT_VALID_CASES",
            "total_case_count": total,
            "valid_case_count": 0,
            "out_count": out_count,
            "out_rate": out_rate,
            "agreement_rate": None,
            "preregistered_max_out_rate": preregistered_max_out_rate,
            "corpus_eligible_for_meta_learning": False,
            "pass": False,
        }

    agree = sum(1 for item in eligible if item["agreement"])
    agreement_rate = agree / len(eligible)
    kappa_pairs = [
        (bool(a["interval_hit"]), bool(b["interval_hit"]))
        for a, b in pairs
        if validate_resolution_provenance(a)["status"] == "VALID_PROVENANCE"
        and validate_resolution_provenance(b)["status"] == "VALID_PROVENANCE"
    ]
    kappa = cohens_kappa_binary(kappa_pairs)
    out_ok = out_rate is not None and out_rate <= preregistered_max_out_rate
    passed = agreement_rate >= preregistered_min_agreement and out_ok
    return {
        "status": "PASS" if passed else "FAIL",
        "total_case_count": total,
        "valid_case_count": len(eligible),
        "out_count": out_count,
        "out_rate": out_rate,
        "agreement_count": agree,
        "agreement_rate": agreement_rate,
        "cohens_kappa_interval_hit": kappa,
        "preregistered_min_agreement": preregistered_min_agreement,
        "preregistered_max_out_rate": preregistered_max_out_rate,
        "corpus_eligible_for_meta_learning": passed,
        "pass": passed,
    }
