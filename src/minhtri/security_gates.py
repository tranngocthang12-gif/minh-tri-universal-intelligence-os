"""Fail-closed security gates bound to canonical project state."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

RESEARCH_GATE_OPEN = "OPEN_AFTER_FRESH_SEAT_PASS"
RESEARCH_GATE_BLOCKED = "BLOCKED_UNTIL_FRESH_SEAT_PASS"
CANONICAL_PROJECT_STATE = Path(__file__).resolve().parents[2] / "docs" / "PROJECT_STATE.json"


class SecurityGateError(ValueError):
    pass


def load_canonical_project_state() -> dict[str, Any]:
    path = CANONICAL_PROJECT_STATE
    if not path.is_file():
        raise SecurityGateError("canonical PROJECT_STATE.json is unavailable")
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise SecurityGateError("canonical PROJECT_STATE.json is unreadable") from exc
    if not isinstance(state, dict):
        raise SecurityGateError("canonical PROJECT_STATE.json must be an object")
    return state


def research_gate_from_state(state: dict[str, Any]) -> str:
    if (
        state.get("fresh_chat_seat_validation") == "PASS"
        and state.get("end_to_end_seat_brain_transport") is True
        and state.get("research_adapter_gate") == RESEARCH_GATE_OPEN
    ):
        return RESEARCH_GATE_OPEN
    return RESEARCH_GATE_BLOCKED


def canonical_research_gate() -> str:
    try:
        return research_gate_from_state(load_canonical_project_state())
    except SecurityGateError:
        return "BLOCKED_CANONICAL_STATE_UNAVAILABLE"


def validate_independent_witness_target(target: dict[str, Any]) -> dict[str, str]:
    """Reject same-authority or non-independent witness targets.

    This gate validates the declared target contract only; deployment still requires
    real credentials and an external authority that is independently controlled.
    """
    if not isinstance(target, dict):
        raise SecurityGateError("witness target must be an object")
    required = {
        "provider",
        "authority_id",
        "independent_from_owner_pc",
        "independent_from_github",
    }
    if set(target) != required:
        raise SecurityGateError("witness target fields are incomplete or unsupported")
    provider = target["provider"]
    authority_id = target["authority_id"]
    if not isinstance(provider, str) or not provider.strip():
        raise SecurityGateError("witness provider is required")
    if not isinstance(authority_id, str) or not authority_id.strip():
        raise SecurityGateError("witness authority_id is required")
    if provider.strip().lower() in {"github", "local", "owner-pc", "filesystem"}:
        raise SecurityGateError("same-authority witness target is not independent")
    if target["independent_from_owner_pc"] is not True:
        raise SecurityGateError("witness must be independent from Owner-PC authority")
    if target["independent_from_github"] is not True:
        raise SecurityGateError("witness must be independent from GitHub authority")
    return {
        "status": "ELIGIBLE_TARGET_DECLARATION",
        "provider": provider.strip(),
        "authority_id": authority_id.strip(),
    }
