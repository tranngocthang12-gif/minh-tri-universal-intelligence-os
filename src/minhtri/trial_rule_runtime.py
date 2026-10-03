"""Fail-closed data-plane reader for bounded TRIAL_RULE experiments.

This module is pure/read-only. It never activates a lesson, writes the ledger, calls a model,
or performs external actions. It compiles one task into a preregistered A/B/C execution plan.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

from .learning_experiment import (
    ExperimentContractError,
    assign_block_arm,
    validate_preregistration,
)

SUPPORTED_TRIAL_OVERLAYS = frozenset({"COUNTEREVIDENCE_FIRST"})


class TrialRuleRuntimeError(ValueError):
    pass


def _utc(value: Any, label: str) -> datetime:
    if not isinstance(value, str):
        raise TrialRuleRuntimeError(f"{label} must be an ISO timestamp")
    text = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError as exc:
        raise TrialRuleRuntimeError(f"{label} must be valid ISO-8601") from exc
    if parsed.tzinfo is None:
        raise TrialRuleRuntimeError(f"{label} must include timezone")
    return parsed.astimezone(timezone.utc)


def preregistration_digest(record: dict[str, Any]) -> str:
    raw = json.dumps(
        record,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _budget_for_arm(experiment: dict[str, Any], arm: str) -> dict[str, Any]:
    key = {
        "CONTROL": "control",
        "TREATMENT": "treatment",
        "COMPUTE_MATCHED": "compute_matched",
    }[arm]
    budget = experiment["compute_budget_contract"][key]
    if not isinstance(budget, dict):
        raise TrialRuleRuntimeError("compute budget must be an object")
    return dict(budget)


def _matching_rules(
    state: dict[str, Any],
    *,
    domain_id: str,
    procedure_id: str,
    experiment_id: str,
    prereg_hash: str,
    now: datetime,
) -> list[dict[str, Any]]:
    rules: list[dict[str, Any]] = []
    for lesson in state.get("lessons", {}).values():
        if lesson.get("status") != "TRIAL_RULE":
            continue
        if lesson.get("runtime_trial_status") != "EXECUTABLE_DECLARATIVE_OVERLAY":
            continue
        spec = lesson.get("trial_spec")
        if not isinstance(spec, dict):
            continue
        if spec.get("domain_id") != domain_id or spec.get("procedure_id") != procedure_id:
            continue
        if spec.get("experiment_id") != experiment_id:
            continue
        if spec.get("preregistration_hash") != prereg_hash:
            continue
        if spec.get("overlay_id") not in SUPPORTED_TRIAL_OVERLAYS:
            raise TrialRuleRuntimeError("unsupported trial overlay")
        if _utc(spec.get("expires_at"), "trial_spec.expires_at") <= now:
            continue
        rules.append(lesson)
    return rules


def build_trial_execution_plan(
    state: dict[str, Any],
    task: dict[str, Any],
    experiment: dict[str, Any],
    *,
    assignment_secret: str,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Compile one task to CONTROL/TREATMENT/COMPUTE_MATCHED without mutating state."""
    try:
        validate_preregistration(experiment)
    except ExperimentContractError as exc:
        raise TrialRuleRuntimeError(str(exc)) from exc

    required_task = {"task_id", "domain_id", "procedure_id"}
    if not isinstance(task, dict) or not required_task.issubset(task):
        raise TrialRuleRuntimeError("task needs task_id, domain_id and procedure_id")

    task_id = task["task_id"]
    domain_id = task["domain_id"]
    procedure_id = task["procedure_id"]
    if not all(isinstance(v, str) and v for v in (task_id, domain_id, procedure_id)):
        raise TrialRuleRuntimeError("task identifiers must be nonempty strings")

    domain = state.get("domains", {}).get(domain_id)
    if not isinstance(domain, dict):
        raise TrialRuleRuntimeError("unknown task domain")
    if domain.get("risk_class") == "HIGH_STAKES":
        raise TrialRuleRuntimeError("high-stakes domains cannot use automatic trial routing")

    procedure = state.get("procedures", {}).get(procedure_id)
    if not isinstance(procedure, dict) or procedure.get("domain_id") != domain_id:
        raise TrialRuleRuntimeError("unknown or cross-domain procedure")

    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    prereg_hash = preregistration_digest(experiment)
    rules = _matching_rules(
        state,
        domain_id=domain_id,
        procedure_id=procedure_id,
        experiment_id=experiment["experiment_id"],
        prereg_hash=prereg_hash,
        now=now,
    )
    if len(rules) != 1:
        raise TrialRuleRuntimeError(
            "exactly one fresh executable TRIAL_RULE must match the task and experiment"
        )
    lesson = rules[0]
    spec = lesson["trial_spec"]

    arm = assign_block_arm(
        task_id,
        assignment_secret,
        experiment_id=experiment["experiment_id"],
        preregistration_hash=prereg_hash,
    )
    budget = _budget_for_arm(experiment, arm)

    treatment_budget = experiment["compute_budget_contract"]["treatment"]
    compute_matched_budget = experiment["compute_budget_contract"]["compute_matched"]
    if treatment_budget != compute_matched_budget:
        raise TrialRuleRuntimeError(
            "treatment and compute-matched budgets must be identical"
        )

    plan = {
        "schema": "minhtri-trial-execution-plan/v1",
        "task_id": task_id,
        "domain_id": domain_id,
        "procedure_id": procedure_id,
        "experiment_id": experiment["experiment_id"],
        "preregistration_hash": prereg_hash,
        "trial_rule_id": lesson["id"],
        "trial_rule_hash": lesson.get("trial_spec_hash"),
        "arm": arm,
        "compute_budget": budget,
        "overlay_id": None,
        "counterevidence_required": False,
        "write_capability": False,
        "automatic_verified_promotion": False,
        "automatic_rule_promotion": False,
    }

    if arm == "TREATMENT":
        plan["overlay_id"] = spec["overlay_id"]
        if spec["overlay_id"] == "COUNTEREVIDENCE_FIRST":
            plan["counterevidence_required"] = True

    # COMPUTE_MATCHED receives the same budget as treatment but no learned overlay.
    return plan
