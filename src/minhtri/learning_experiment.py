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
        "frozen_evaluator_hash",
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

    for key in (
        "assignment_seed_hash",
        "control_pipeline_hash",
        "treatment_pipeline_hash",
        "frozen_evaluator_hash",
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
    return "TREATMENT" if digest[0] & 1 else "CONTROL"
