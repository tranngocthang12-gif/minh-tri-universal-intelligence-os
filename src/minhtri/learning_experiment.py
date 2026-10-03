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
    if record["primary_endpoint"] == record["safety_endpoint"]:
        raise ExperimentContractError("primary and safety endpoints must be distinct")
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
    if not isinstance(record["compute_budget_contract"], dict) or set(record["compute_budget_contract"]) != {"control", "treatment", "compute_matched"}:
        raise ExperimentContractError("compute_budget_contract must define control/treatment/compute_matched")

    for key in (
        "assignment_seed_hash",
        "control_pipeline_hash",
        "treatment_pipeline_hash",
        "compute_matched_pipeline_hash",
        "frozen_evaluator_hash",
        "gold_labels_hash",
    ):
        value = record[key]
        if not isinstance(value, str) or len(value) != 64 or any(ch not in "0123456789abcdef" for ch in value):
            raise ExperimentContractError(f"{key} must be lowercase sha256")

    return {
        "status": "PREREGISTERED",
        "experiment_id": record["experiment_id"],
        "primary_endpoint": record["primary_endpoint"],
        "safety_endpoint": record["safety_endpoint"],
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
