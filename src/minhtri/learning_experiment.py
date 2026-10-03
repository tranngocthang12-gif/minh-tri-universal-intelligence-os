"""Preregistered experiment contract for behavioral learning trials."""
from __future__ import annotations

import hashlib
from typing import Any

FORBIDDEN_ROUTING_KEYS = frozenset({
    "failure_class",
    "outcome",
    "resolution",
    "critic_verdict",
    "post_outcome_label",
})


class ExperimentContractError(ValueError):
    pass


def validate_preregistration(record: dict[str, Any]) -> dict[str, Any]:
    required = (
        "experiment_id",
        "frozen_at_utc",
        "primary_endpoint",
        "safety_endpoint",
        "coverage_endpoint",
        "coverage_noninferiority_margin",
        "primary_success_rule",
        "safety_failure_rule",
        "rollback_rule",
        "assignment_unit",
        "assignment_seed_hash",
        "control_pipeline_hash",
        "treatment_pipeline_hash",
        "compute_matched_pipeline_hash",
        "frozen_evaluator_hash",
        "gold_labels_hash",
        "baseline_definition",
        "compute_budget_contract",
        "compute_tolerance_fraction",
        "placebo_overlay_id",
        "placebo_overlay_hash",
        "placebo_provenance_hash",
        "arm_mode",
        "primary_window_tasks",
        "rollback_threshold",
        "trial_rule_id",
        "trial_rule_ttl_seconds",
        "routing_keys",
    )
    missing = [key for key in required if key not in record]
    if missing:
        raise ExperimentContractError("missing preregistration fields: " + ",".join(missing))

    if record["assignment_unit"] != "TASK_ID":
        raise ExperimentContractError("assignment_unit must be TASK_ID")
    if len({record["primary_endpoint"], record["safety_endpoint"], record["coverage_endpoint"]}) != 3:
        raise ExperimentContractError("primary, safety and coverage endpoints must be distinct")
    if not isinstance(record["coverage_noninferiority_margin"], (int, float)) or record["coverage_noninferiority_margin"] < 0:
        raise ExperimentContractError("coverage_noninferiority_margin must be nonnegative")
    if not isinstance(record["compute_tolerance_fraction"], (int, float)) or not 0 <= record["compute_tolerance_fraction"] <= 1:
        raise ExperimentContractError("compute_tolerance_fraction must be between 0 and 1")
    if record["arm_mode"] != "PAIRED_FOUR_ARM":
        raise ExperimentContractError("arm_mode must be PAIRED_FOUR_ARM")
    if not isinstance(record["trial_rule_ttl_seconds"], int) or record["trial_rule_ttl_seconds"] <= 0:
        raise ExperimentContractError("trial_rule_ttl_seconds must be positive")

    routing = record["routing_keys"]
    if not isinstance(routing, list) or not routing:
        raise ExperimentContractError("routing_keys must be a nonempty list")
    forbidden = sorted(set(routing) & FORBIDDEN_ROUTING_KEYS)
    if forbidden:
        raise ExperimentContractError("post-outcome or human labels cannot route trial: " + ",".join(forbidden))
    if not set(routing).issubset({"domain_id", "procedure_id"}):
        raise ExperimentContractError("first learning trial may route only on domain_id/procedure_id")

    if record["primary_success_rule"] != "treatment > compute_matched":
        raise ExperimentContractError("primary_success_rule must be treatment > compute_matched")
    if record["baseline_definition"] not in {"NO_ASSURANCE", "V1_3"}:
        raise ExperimentContractError("baseline_definition must be NO_ASSURANCE or V1_3")
    if not isinstance(record["primary_window_tasks"], int) or record["primary_window_tasks"] < 1:
        raise ExperimentContractError("primary_window_tasks must be positive")
    if not isinstance(record["rollback_threshold"], (int, float)):
        raise ExperimentContractError("rollback_threshold must be numeric")
    if not isinstance(record["compute_budget_contract"], dict) or set(record["compute_budget_contract"]) != {"control", "treatment", "compute_matched", "placebo"}:
        raise ExperimentContractError("compute_budget_contract must define control/treatment/compute_matched/placebo")
    if record["compute_budget_contract"]["treatment"] != record["compute_budget_contract"]["compute_matched"]:
        raise ExperimentContractError("treatment and compute_matched declared budgets must match")
    if record["compute_budget_contract"]["treatment"] != record["compute_budget_contract"]["placebo"]:
        raise ExperimentContractError("treatment and placebo declared budgets must match")

    for key in (
        "assignment_seed_hash",
        "control_pipeline_hash",
        "treatment_pipeline_hash",
        "compute_matched_pipeline_hash",
        "frozen_evaluator_hash",
        "gold_labels_hash",
        "placebo_overlay_hash",
        "placebo_provenance_hash",
    ):
        value = record[key]
        if not isinstance(value, str) or len(value) != 64 or any(ch not in "0123456789abcdef" for ch in value):
            raise ExperimentContractError(f"{key} must be lowercase sha256")

    return {
        "status": "PREREGISTERED",
        "experiment_id": record["experiment_id"],
        "primary_endpoint": record["primary_endpoint"],
        "safety_endpoint": record["safety_endpoint"],
        "coverage_endpoint": record["coverage_endpoint"],
        "arm_mode": record["arm_mode"],
        "routing_keys": list(routing),
        "post_outcome_routing_allowed": False,
        "metric_change_after_unblinding_invalidates_run": True,
    }


def assign_arm(task_id: str, assignment_secret: str) -> str:
    if not isinstance(task_id, str) or not task_id:
        raise ExperimentContractError("task_id is required")
    if not isinstance(assignment_secret, str) or not assignment_secret:
        raise ExperimentContractError("assignment_secret is required")
    digest = hashlib.sha256((assignment_secret + "|" + task_id).encode("utf-8")).digest()
    return ("CONTROL", "TREATMENT", "COMPUTE_MATCHED")[digest[0] % 3]


def assign_block_arm(
    task_id: str,
    assignment_secret: str,
    *,
    experiment_id: str,
    preregistration_hash: str,
) -> str:
    """Balanced 2/2/2 allocation for task IDs ending in -T01..-T06."""
    if not isinstance(task_id, str) or "-T" not in task_id:
        raise ExperimentContractError("task_id must encode a block and T01..T06 slot")
    if not isinstance(assignment_secret, str) or not assignment_secret:
        raise ExperimentContractError("assignment_secret is required")
    if not isinstance(experiment_id, str) or not experiment_id:
        raise ExperimentContractError("experiment_id is required")
    if (
        not isinstance(preregistration_hash, str)
        or len(preregistration_hash) != 64
        or any(ch not in "0123456789abcdef" for ch in preregistration_hash)
    ):
        raise ExperimentContractError("preregistration_hash must be lowercase sha256")

    block_id, slot_text = task_id.rsplit("-T", 1)
    if len(slot_text) != 2 or not slot_text.isdigit():
        raise ExperimentContractError("task slot must be T01..T06")
    slot = int(slot_text)
    if slot < 1 or slot > 6:
        raise ExperimentContractError("task slot must be T01..T06")

    seed_material = "|".join(
        (assignment_secret, experiment_id, preregistration_hash, block_id)
    ).encode("utf-8")
    seed = hashlib.sha256(seed_material).digest()

    arms = [
        "CONTROL",
        "CONTROL",
        "TREATMENT",
        "TREATMENT",
        "COMPUTE_MATCHED",
        "COMPUTE_MATCHED",
    ]
    # Deterministic Fisher-Yates driven by domain-separated SHA-256 bytes.
    for i in range(len(arms) - 1, 0, -1):
        h = hashlib.sha256(seed + bytes([i])).digest()
        j = int.from_bytes(h[:8], "big") % (i + 1)
        arms[i], arms[j] = arms[j], arms[i]
    return arms[slot - 1]


def paired_four_arm_order(task_id: str, assignment_secret: str, *, experiment_id: str, preregistration_hash: str) -> list[str]:
    """Return a deterministic randomized presentation/execution order for all four arms."""
    if not all(isinstance(v, str) and v for v in (task_id, assignment_secret, experiment_id)):
        raise ExperimentContractError("task_id, assignment_secret and experiment_id are required")
    if len(preregistration_hash) != 64 or any(ch not in "0123456789abcdef" for ch in preregistration_hash):
        raise ExperimentContractError("preregistration_hash must be lowercase sha256")
    arms = ["CONTROL", "TREATMENT", "COMPUTE_MATCHED", "PLACEBO"]
    seed = hashlib.sha256(
        "|".join((assignment_secret, experiment_id, preregistration_hash, task_id, "paired-four-arm")).encode("utf-8")
    ).digest()
    for i in range(len(arms) - 1, 0, -1):
        h = hashlib.sha256(seed + bytes([i])).digest()
        j = int.from_bytes(h[:8], "big") % (i + 1)
        arms[i], arms[j] = arms[j], arms[i]
    return arms


def validate_compute_telemetry(
    treatment: dict[str, Any],
    comparator: dict[str, Any],
    *,
    tolerance_fraction: float,
) -> dict[str, Any]:
    """Measure actual compute parity after execution; declared budget is not enough."""
    if not 0 <= tolerance_fraction <= 1:
        raise ExperimentContractError("tolerance_fraction must be between 0 and 1")
    exact_keys = ("retrieval_calls", "critic_calls", "generator_calls")
    token_keys = ("input_tokens", "output_tokens", "retrieved_tokens")
    mismatches: list[str] = []
    for key in exact_keys:
        if treatment.get(key) != comparator.get(key):
            mismatches.append(key)
    for key in token_keys:
        a, b = treatment.get(key), comparator.get(key)
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)) or a < 0 or b < 0:
            mismatches.append(key)
            continue
        denom = max(float(a), float(b), 1.0)
        if abs(float(a) - float(b)) / denom > tolerance_fraction:
            mismatches.append(key)
    return {
        "status": "COMPUTE_MATCHED" if not mismatches else "COMPUTE_MISMATCH",
        "mismatched_fields": sorted(set(mismatches)),
        "eligible_for_primary_analysis": not mismatches,
        "tolerance_fraction": tolerance_fraction,
    }
