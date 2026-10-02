"""Fail-closed validator for separate-chat fresh-seat recovery evidence."""
from __future__ import annotations

from typing import Any

SCHEMA = "minhtri-fresh-seat-validation/v1"
EXPECTED_TOOLS = ("brain.recovery_packet", "brain.verify")


class FreshSeatValidationError(ValueError):
    pass


def _need(record: dict[str, Any], *keys: str) -> None:
    missing = [key for key in keys if key not in record]
    if missing:
        raise FreshSeatValidationError("missing fields: " + ", ".join(missing))


def _read_tuple(value: Any, label: str) -> tuple[int, str]:
    if not isinstance(value, dict):
        raise FreshSeatValidationError(f"{label} must be an object")
    count = value.get("event_count")
    head = value.get("head")
    if type(count) is not int or count < 0:
        raise FreshSeatValidationError(f"{label}.event_count must be a non-negative integer")
    if not isinstance(head, str) or len(head) != 64:
        raise FreshSeatValidationError(f"{label}.head must be a 64-character digest")
    return count, head.lower()


def validate_fresh_seat_evidence(record: dict[str, Any]) -> dict[str, Any]:
    """Validate evidence produced by a genuinely separate chat seat.

    This function does not decide that a UI conversation was separate by itself. The
    evidence record must explicitly attest that property, while runtime outputs must
    independently cross-match so a prose-only claim cannot pass.
    """
    if not isinstance(record, dict):
        raise FreshSeatValidationError("record must be an object")
    _need(
        record,
        "schema",
        "separate_chat_ui",
        "prompt_seeded_expected_values",
        "toolset",
        "mutation_tool_exposed",
        "fresh_verify",
        "fresh_recovery",
        "control_verify",
    )
    if record["schema"] != SCHEMA:
        raise FreshSeatValidationError("unsupported schema")
    if record["separate_chat_ui"] is not True:
        raise FreshSeatValidationError("fresh seat must be a separate chat UI")
    if record["prompt_seeded_expected_values"] is not False:
        raise FreshSeatValidationError("prompt must not seed expected head/count/focus values")
    if record["mutation_tool_exposed"] is not False:
        raise FreshSeatValidationError("mutation capability must not be exposed")

    tools = record["toolset"]
    if not isinstance(tools, list) or tuple(sorted(tools)) != EXPECTED_TOOLS:
        raise FreshSeatValidationError("fresh seat must expose exactly the two read-only brain tools")

    fresh_verify = _read_tuple(record["fresh_verify"], "fresh_verify")
    fresh_recovery = _read_tuple(record["fresh_recovery"], "fresh_recovery")
    control_verify = _read_tuple(record["control_verify"], "control_verify")
    if fresh_verify != fresh_recovery:
        raise FreshSeatValidationError("fresh verify and recovery packet disagree")
    if fresh_verify != control_verify:
        raise FreshSeatValidationError("fresh-seat read does not match independent control read")

    recovery = record["fresh_recovery"]
    if recovery.get("status") != "VALID":
        raise FreshSeatValidationError("fresh recovery status must be VALID")
    if record["fresh_verify"].get("status") != "VALID":
        raise FreshSeatValidationError("fresh verify status must be VALID")
    if record["control_verify"].get("status") != "VALID":
        raise FreshSeatValidationError("control verify status must be VALID")

    return {
        "status": "PASS",
        "schema": SCHEMA,
        "event_count": fresh_verify[0],
        "head": fresh_verify[1],
        "toolset": list(EXPECTED_TOOLS),
        "write_capability": False,
    }
