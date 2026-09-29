"""Goal decomposition and bottleneck governor for MINH TRI R4.

R4 does not optimize a fake numeric score. It builds a dependency graph over an
Owner goal, binds gaps to R3 epistemic state, and uses an explicit ordinal
rubric to select one highest-leverage eligible learning unit or return
WAIT/HOLD_AMBIGUOUS. It grants no external action authority.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

from .core import GateError, Ledger, digest, identifier, need, ref, string
from .epistemic import EpistemicService, MATURITY_LEVELS


TARGET_ROLES = {"BLOCKER", "ENABLER", "OPTIMIZER"}
GAP_KINDS = {"KNOWLEDGE_GAP", "VALIDATION_GAP", "CAPABILITY_GAP", "DECISION_GAP"}
OWNER_IMPACTS = {"CRITICAL", "HIGH", "MEDIUM", "LOW"}
DECISION_SENSITIVITY = {"DECISION_CHANGING", "MEANINGFUL", "INFORMATIONAL"}
INFORMATION_GAIN = {"HIGH", "MEDIUM", "LOW", "UNKNOWN"}
COST_BANDS = {"LOW", "MEDIUM", "HIGH"}
TIME_BANDS = {"SHORT", "MEDIUM", "LONG"}
RISK_BANDS = {"LOW", "MEDIUM", "HIGH"}
REVERSIBILITY = {"REVERSIBLE", "PARTLY_REVERSIBLE"}
UNIT_TYPES = {"LEARN", "READ_ONLY_ANALYSIS", "SHADOW_TEST"}
COMPONENT_STATUS = {"OPEN", "SATISFIED", "HOLD", "NOT_APPLICABLE"}
FOCUS_DECISIONS = {"SELECT", "WAIT", "HOLD_AMBIGUOUS"}

GOVERNOR_FIELDS = {
    "create_plan": {
        "id", "goal_id", "domain_id", "target_state", "success_conditions", "owner_constraints",
    },
    "add_component": {
        "id", "plan_id", "name", "supports_conditions", "dependency_ids", "target_role", "gap_kind",
        "owner_impact", "decision_sensitivity", "information_gain", "cost_band", "time_band",
        "risk_band", "reversibility", "epistemic_item_ids", "unknown_ids", "allowed_evidence_ids",
        "leverage_hypothesis", "disconfirming_condition", "next_unit_type", "next_unit", "acceptance",
    },
    "set_component_status": {"component_id", "status", "reason", "evidence_ids"},
    "record_focus": {
        "plan_id", "decision", "component_id", "reason", "core_head", "epistemic_head",
        "plan_head_before", "candidate_ids", "selection_method", "selection_snapshot_hash",
    },
}

_ROLE_RANK = {"BLOCKER": 3, "ENABLER": 2, "OPTIMIZER": 1}
_IMPACT_RANK = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
_DECISION_RANK = {"DECISION_CHANGING": 3, "MEANINGFUL": 2, "INFORMATIONAL": 1}
_GAP_RANK = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
_INFO_RANK = {"HIGH": 3, "MEDIUM": 2, "LOW": 1, "UNKNOWN": 0}
_REVERSE_RANK = {"REVERSIBLE": 2, "PARTLY_REVERSIBLE": 1}
_LOW_BETTER_RANK = {"LOW": 3, "MEDIUM": 2, "HIGH": 1}
_TIME_RANK = {"SHORT": 3, "MEDIUM": 2, "LONG": 1}


def initial_governor_state() -> dict:
    return {"format_version": 1, "phase": "SHADOW", "plans": {}, "components": {}}


def _ids(values: Any, label: str) -> list[str]:
    if not isinstance(values, list) or any(not isinstance(v, str) for v in values) or len(set(values)) != len(values):
        raise GateError(f"{label} must be a list of distinct IDs")
    for value in values:
        identifier(value, label)
    return values


def _texts(values: Any, label: str, allow_empty: bool = False) -> list[str]:
    if not isinstance(values, list) or any(not isinstance(v, str) or not v.strip() for v in values):
        raise GateError(f"{label} must be a text list")
    if not allow_empty and not values:
        raise GateError(f"{label} must be nonempty")
    return [v.strip() for v in values]


def _plan(state: dict, plan_id: str) -> dict:
    return ref(state, "plans", plan_id)


def _component(state: dict, component_id: str) -> dict:
    return ref(state, "components", component_id)


def governor_evolve(state: dict, command: dict, at: str) -> dict:
    """Pure planning reducer. Semantic leverage claims remain hypotheses."""
    if not isinstance(command, dict) or set(command) != {"type", "data"} or not isinstance(command["data"], dict):
        raise GateError("Command must contain exactly type and data object")
    kind, d = command["type"], copy.deepcopy(command["data"])
    if kind not in GOVERNOR_FIELDS:
        raise GateError(f"Unknown governor command: {kind}")
    extra = set(d) - GOVERNOR_FIELDS[kind]
    if extra:
        raise GateError("Unexpected governor fields: " + ", ".join(sorted(extra)))
    out = copy.deepcopy(state)
    if out["phase"] != "SHADOW":
        raise GateError("Only SHADOW bottleneck governance is implemented")

    if kind == "create_plan":
        need(d, *GOVERNOR_FIELDS[kind])
        plan_id = identifier(d["id"], "plan ID")
        if plan_id in out["plans"]:
            raise GateError(f"Duplicate plan ID: {plan_id}")
        identifier(d["goal_id"], "goal_id")
        identifier(d["domain_id"], "domain_id")
        d["target_state"] = string(d["target_state"], "target_state")
        d["success_conditions"] = _texts(d["success_conditions"], "success_conditions")
        d["owner_constraints"] = _texts(d["owner_constraints"], "owner_constraints", allow_empty=True)
        d["status"] = "OPEN"
        d["focus_history"] = []
        d["created_at"] = at
        out["plans"][plan_id] = d

    elif kind == "add_component":
        need(d, *GOVERNOR_FIELDS[kind])
        component_id = identifier(d["id"], "component ID")
        if component_id in out["components"]:
            raise GateError(f"Duplicate component ID: {component_id}")
        plan = _plan(out, d["plan_id"])
        d["name"] = string(d["name"], "name")
        d["supports_conditions"] = _texts(d["supports_conditions"], "supports_conditions")
        if not set(d["supports_conditions"]).issubset(set(plan["success_conditions"])):
            raise GateError("Component supports_conditions must come from the plan success conditions")
        dependencies = _ids(d["dependency_ids"], "dependency_ids")
        for dep_id in dependencies:
            dep = _component(out, dep_id)
            if dep["plan_id"] != d["plan_id"]:
                raise GateError("Component dependency cannot cross plans")
        if d["target_role"] not in TARGET_ROLES:
            raise GateError("Invalid target_role")
        if d["gap_kind"] not in GAP_KINDS:
            raise GateError("Invalid gap_kind")
        if d["owner_impact"] not in OWNER_IMPACTS:
            raise GateError("Invalid owner_impact")
        if d["decision_sensitivity"] not in DECISION_SENSITIVITY:
            raise GateError("Invalid decision_sensitivity")
        if d["information_gain"] not in INFORMATION_GAIN:
            raise GateError("Invalid information_gain")
        if d["cost_band"] not in COST_BANDS or d["risk_band"] not in RISK_BANDS:
            raise GateError("Invalid cost/risk band")
        if d["time_band"] not in TIME_BANDS:
            raise GateError("Invalid time_band")
        if d["reversibility"] not in REVERSIBILITY:
            raise GateError("R4 accepts only reversible/partly reversible next units")
        if d["next_unit_type"] not in UNIT_TYPES:
            raise GateError("R4 next unit must be LEARN, READ_ONLY_ANALYSIS or SHADOW_TEST")
        d["epistemic_item_ids"] = _ids(d["epistemic_item_ids"], "epistemic_item_ids")
        d["unknown_ids"] = _ids(d["unknown_ids"], "unknown_ids")
        if not d["epistemic_item_ids"] and not d["unknown_ids"]:
            raise GateError("A bottleneck component must link to R3 knowledge or unknown state")
        d["allowed_evidence_ids"] = _ids(d["allowed_evidence_ids"], "allowed_evidence_ids")
        d["leverage_hypothesis"] = string(d["leverage_hypothesis"], "leverage_hypothesis")
        d["disconfirming_condition"] = string(d["disconfirming_condition"], "disconfirming_condition")
        d["next_unit"] = string(d["next_unit"], "next_unit")
        d["acceptance"] = string(d["acceptance"], "acceptance")
        d["status"] = "OPEN"
        d["status_reason"] = "UNRESOLVED_GAP"
        d["status_evidence_ids"] = []
        d["created_at"] = at
        out["components"][component_id] = d

    elif kind == "set_component_status":
        need(d, *GOVERNOR_FIELDS[kind])
        component = _component(out, d["component_id"])
        if d["status"] not in COMPONENT_STATUS:
            raise GateError("Invalid component status")
        d["reason"] = string(d["reason"], "reason")
        evidence_ids = _ids(d["evidence_ids"], "evidence_ids")
        component["status"] = d["status"]
        component["status_reason"] = d["reason"]
        component["status_evidence_ids"] = evidence_ids
        component["status_updated_at"] = at

    elif kind == "record_focus":
        need(d, *GOVERNOR_FIELDS[kind])
        plan = _plan(out, d["plan_id"])
        if d["decision"] not in FOCUS_DECISIONS:
            raise GateError("Invalid focus decision")
        if d["component_id"] is not None:
            component = _component(out, d["component_id"])
            if component["plan_id"] != d["plan_id"]:
                raise GateError("Focus component belongs to another plan")
        string(d["reason"], "reason")
        for key in ("core_head", "epistemic_head", "plan_head_before", "selection_snapshot_hash"):
            if not isinstance(d[key], str) or len(d[key]) != 64 or any(c not in "0123456789abcdef" for c in d[key]):
                raise GateError(f"{key} must be a SHA-256 digest")
        d["candidate_ids"] = _ids(d["candidate_ids"], "candidate_ids")
        for candidate_id in d["candidate_ids"]:
            candidate = _component(out, candidate_id)
            if candidate["plan_id"] != d["plan_id"]:
                raise GateError("Focus candidate belongs to another plan")
        if d["decision"] == "SELECT":
            if d["component_id"] is None or d["component_id"] not in d["candidate_ids"]:
                raise GateError("SELECT requires the selected component in candidate_ids")
        elif d["decision"] == "HOLD_AMBIGUOUS":
            if d["component_id"] is not None or len(d["candidate_ids"]) < 2:
                raise GateError("HOLD_AMBIGUOUS requires at least two tied candidates and no selection")
        elif d["component_id"] is not None:
            raise GateError("WAIT cannot carry a selected component")
        d["selection_method"] = string(d["selection_method"], "selection_method")
        d["recorded_at"] = at
        plan["focus_history"].append(d)
        plan["last_focus"] = d

    return out


def _gap_level(component: dict, epistemic_state: dict) -> str:
    ranks: list[int] = []
    for unknown_id in component["unknown_ids"]:
        unknown = ref(epistemic_state, "unknowns", unknown_id)
        if unknown["status"] == "OPEN":
            ranks.append(_GAP_RANK[unknown["materiality"]])
    for item_id in component["epistemic_item_ids"]:
        item = ref(epistemic_state, "items", item_id)
        if item["status"] == "REOPENED":
            ranks.append(_GAP_RANK["HIGH"])
            continue
        level = item["effective_level"]
        if level in ("L0_MEMORY", "L1_KNOWLEDGE"):
            ranks.append(_GAP_RANK["HIGH"])
        elif level in ("L2_UNDERSTANDING", "L3_PREDICTION"):
            ranks.append(_GAP_RANK["MEDIUM"])
        else:
            ranks.append(_GAP_RANK["LOW"])
    if not ranks:
        return "LOW"
    value = max(ranks)
    return {3: "HIGH", 2: "MEDIUM", 1: "LOW"}[value]


def _rank_tuple(component: dict, epistemic_state: dict) -> tuple[int, ...]:
    gap = _gap_level(component, epistemic_state)
    return (
        _ROLE_RANK[component["target_role"]],
        _IMPACT_RANK[component["owner_impact"]],
        _DECISION_RANK[component["decision_sensitivity"]],
        _GAP_RANK[gap],
        _INFO_RANK[component["information_gain"]],
        _REVERSE_RANK[component["reversibility"]],
        _LOW_BETTER_RANK[component["risk_band"]],
        _LOW_BETTER_RANK[component["cost_band"]],
        _TIME_RANK[component["time_band"]],
    )


def _rubric_snapshot(component: dict, epistemic_state: dict) -> dict:
    return {
        "target_role": component["target_role"],
        "owner_impact": component["owner_impact"],
        "decision_sensitivity": component["decision_sensitivity"],
        "epistemic_gap": _gap_level(component, epistemic_state),
        "information_gain": component["information_gain"],
        "reversibility": component["reversibility"],
        "risk_band": component["risk_band"],
        "cost_band": component["cost_band"],
        "time_band": component["time_band"],
    }


class BottleneckService:
    """Binds Owner goals, R3 epistemic state and an R4 decomposition ledger."""

    SELECTION_METHOD = "ORDINAL_LEXICOGRAPHIC_NO_CALIBRATED_SCORE"

    def __init__(self, core_home: str | Path):
        self.core = Ledger(core_home)
        self.epistemic = EpistemicService(core_home)
        self.ledger = Ledger(Path(core_home) / "governor", reducer=governor_evolve, initial=initial_governor_state)

    def init(self) -> None:
        self.core.verify()
        self.epistemic.ledger.verify()
        self.ledger.init()

    def _assert_goal_open(self, core_state: dict, plan: dict) -> None:
        goal = ref(core_state, "goals", plan["goal_id"])
        if goal["status"] != "OPEN":
            raise GateError("Bottleneck planning is blocked because the Owner goal is not OPEN")

    def _validate_component_refs(self, plan: dict, data: dict, epistemic_state: dict, core_state: dict) -> None:
        for item_id in data["epistemic_item_ids"]:
            item = ref(epistemic_state, "items", item_id)
            if item["domain_id"] != plan["domain_id"]:
                raise GateError("R4 epistemic item cannot cross domain boundaries")
        for unknown_id in data["unknown_ids"]:
            unknown = ref(epistemic_state, "unknowns", unknown_id)
            if unknown["domain_id"] != plan["domain_id"]:
                raise GateError("R4 unknown cannot cross domain boundaries")
        for evidence_id in data["allowed_evidence_ids"]:
            evidence = ref(core_state, "evidence", evidence_id)
            if evidence["domain_id"] != plan["domain_id"]:
                raise GateError("R4 evidence cannot cross domain boundaries")

    def apply(self, command: dict) -> dict:
        self.ledger.acquire_project_lock()
        try:
            core_state, _, _ = self.core.verify()
            epistemic_state, _, _ = self.epistemic.ledger.verify()
            if not isinstance(command, dict) or set(command) != {"type", "data"} or not isinstance(command["data"], dict):
                raise GateError("Command must contain exactly type and data object")
            command = copy.deepcopy(command)
            kind, d = command["type"], command["data"]
            state, _, _ = self.ledger.verify()

            if kind == "create_plan":
                need(d, "id", "goal_id", "target_state", "success_conditions", "owner_constraints")
                if set(d) != {"id", "goal_id", "target_state", "success_conditions", "owner_constraints"}:
                    raise GateError("create_plan input has unexpected fields")
                goal = ref(core_state, "goals", d["goal_id"])
                if goal["status"] != "OPEN":
                    raise GateError("Cannot decompose a blocked or closed Owner goal")
                d["domain_id"] = goal["domain_id"]

            elif kind == "add_component":
                plan = ref(state, "plans", d.get("plan_id"))
                self._assert_goal_open(core_state, plan)
                self._validate_component_refs(plan, d, epistemic_state, core_state)

            elif kind == "set_component_status":
                component = ref(state, "components", d.get("component_id"))
                plan = ref(state, "plans", component["plan_id"])
                self._assert_goal_open(core_state, plan)
                evidence_ids = d.get("evidence_ids", [])
                for evidence_id in evidence_ids:
                    evidence = ref(core_state, "evidence", evidence_id)
                    if evidence["domain_id"] != plan["domain_id"]:
                        raise GateError("Component status evidence cannot cross domain boundaries")
                if d.get("status") == "SATISFIED":
                    if not set(evidence_ids).issubset(set(component["allowed_evidence_ids"])):
                        raise GateError("SATISFIED evidence must come from the component evidence allowlist")
                    unresolved_unknowns = [
                        unknown_id for unknown_id in component["unknown_ids"]
                        if ref(epistemic_state, "unknowns", unknown_id)["status"] == "OPEN"
                    ]
                    if unresolved_unknowns:
                        raise GateError("SATISFIED is blocked while linked component unknowns remain OPEN")
                    mature = any(
                        ref(epistemic_state, "items", item_id)["status"] == "ACTIVE"
                        and MATURITY_LEVELS.index(ref(epistemic_state, "items", item_id)["effective_level"])
                        >= MATURITY_LEVELS.index("L2_UNDERSTANDING")
                        for item_id in component["epistemic_item_ids"]
                    )
                    if not evidence_ids and not mature:
                        raise GateError("SATISFIED requires allowed evidence or an active L2+ linked epistemic item")

            elif kind == "record_focus":
                raise GateError("record_focus is governor-generated; use commit_focus")

            return self.ledger.apply(command, project_lock_held=True)
        finally:
            self.ledger.release_project_lock()

    def _eligible_components(self, plan_id: str, state: dict) -> tuple[list[dict], list[str]]:
        components = [c for c in state["components"].values() if c["plan_id"] == plan_id]
        eligible = []
        blocked = []
        for component in components:
            if component["status"] != "OPEN":
                continue
            unmet = [
                dep_id for dep_id in component["dependency_ids"]
                if state["components"][dep_id]["status"] != "SATISFIED"
            ]
            if unmet:
                blocked.append(component["id"])
            else:
                eligible.append(component)
        return eligible, blocked

    def recommend(self, plan_id: str) -> dict:
        core_state, _, core_head = self.core.verify()
        epistemic_state, _, epistemic_head = self.epistemic.ledger.verify()
        state, _, plan_head = self.ledger.verify()
        plan = ref(state, "plans", plan_id)
        self._assert_goal_open(core_state, plan)

        components = [c for c in state["components"].values() if c["plan_id"] == plan_id]
        eligible, dependency_blocked = self._eligible_components(plan_id, state)

        base = {
            "plan_id": plan_id,
            "goal_id": plan["goal_id"],
            "domain_id": plan["domain_id"],
            "selection_method": self.SELECTION_METHOD,
            "core_head": core_head,
            "epistemic_head": epistemic_head,
            "plan_head": plan_head,
        }

        if not eligible:
            unresolved = [c for c in components if c["status"] in ("OPEN", "HOLD")]
            if not unresolved:
                reason = "ALL_COMPONENTS_SATISFIED_OR_NOT_APPLICABLE"
            elif dependency_blocked:
                reason = "WAIT_DEPENDENCIES_OR_HOLDS"
            else:
                reason = "WAIT_NO_ELIGIBLE_UNIT"
            return {
                **base,
                "decision": "WAIT",
                "component_id": None,
                "candidate_ids": [],
                "reason": reason,
                "task_candidate": None,
            }

        ranked = sorted(eligible, key=lambda c: _rank_tuple(c, epistemic_state), reverse=True)
        best_tuple = _rank_tuple(ranked[0], epistemic_state)
        top = [c for c in ranked if _rank_tuple(c, epistemic_state) == best_tuple]
        if len(top) > 1:
            return {
                **base,
                "decision": "HOLD_AMBIGUOUS",
                "component_id": None,
                "candidate_ids": sorted(c["id"] for c in top),
                "reason": "TOP_CANDIDATES_TIED_UNDER_CURRENT_ORDINAL_RUBRIC",
                "rubric": _rubric_snapshot(top[0], epistemic_state),
                "task_candidate": None,
            }

        selected = ranked[0]
        return {
            **base,
            "decision": "SELECT",
            "component_id": selected["id"],
            "candidate_ids": [c["id"] for c in ranked],
            "reason": "HIGHEST_LEVERAGE_ELIGIBLE_UNIT_UNDER_DECLARED_ORDINAL_RUBRIC",
            "rubric": _rubric_snapshot(selected, epistemic_state),
            "leverage_hypothesis": selected["leverage_hypothesis"],
            "disconfirming_condition": selected["disconfirming_condition"],
            "task_candidate": {
                "goal_id": plan["goal_id"],
                "brief": selected["next_unit"],
                "acceptance": selected["acceptance"],
                "allowed_evidence_ids": copy.deepcopy(selected["allowed_evidence_ids"]),
                "unit_type": selected["next_unit_type"],
            },
        }

    def commit_focus(self, plan_id: str) -> dict:
        self.ledger.acquire_project_lock()
        try:
            recommendation = self.recommend(plan_id)
            snapshot = {
                "decision": recommendation["decision"],
                "component_id": recommendation["component_id"],
                "candidate_ids": recommendation["candidate_ids"],
                "reason": recommendation["reason"],
                "selection_method": recommendation["selection_method"],
                "rubric": recommendation.get("rubric"),
                "task_candidate": recommendation.get("task_candidate"),
            }
            command = {
                "type": "record_focus",
                "data": {
                    "plan_id": plan_id,
                    "decision": recommendation["decision"],
                    "component_id": recommendation["component_id"],
                    "reason": recommendation["reason"],
                    "core_head": recommendation["core_head"],
                    "epistemic_head": recommendation["epistemic_head"],
                    "plan_head_before": recommendation["plan_head"],
                    "candidate_ids": recommendation["candidate_ids"],
                    "selection_method": recommendation["selection_method"],
                    "selection_snapshot_hash": digest(snapshot),
                },
            }
            receipt = self.ledger.apply(command, project_lock_held=True)
            return {"recommendation": recommendation, "receipt": receipt}
        finally:
            self.ledger.release_project_lock()

    def status(self) -> dict:
        state, count, head = self.ledger.verify()
        return {
            "phase": state["phase"],
            "event_count": count,
            "head": head,
            "counts": {
                "plans": len(state["plans"]),
                "components": len(state["components"]),
                "open_components": sum(1 for c in state["components"].values() if c["status"] == "OPEN"),
                "hold_components": sum(1 for c in state["components"].values() if c["status"] == "HOLD"),
                "satisfied_components": sum(1 for c in state["components"].values() if c["status"] == "SATISFIED"),
            },
        }
