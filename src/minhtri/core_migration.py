"""Compatibility helpers for pre-family Core ledgers.

The migration path verifies the original hash chain and replays an in-memory
normalized command stream. It never rewrites historical events or snapshots.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

from .core import GateError, canonical, digest, evolve, initial_state


CORE_LEGACY_SCHEMA = "core-v1-provider-id-only"
CORE_CURRENT_SCHEMA = "core-v2-provider-family"


def legacy_family_id(provider_id: str) -> str:
    return "legacy-" + digest(provider_id)[:16]


def _normalize_command(command: dict) -> dict:
    command = copy.deepcopy(command)
    if command.get("type") == "register_provider":
        data = command.get("data", {})
        if "family_id" not in data:
            data["family_id"] = legacy_family_id(data["id"])
    return command


def _normalize_legacy_snapshot_state(state: dict) -> dict:
    state = copy.deepcopy(state)
    for provider_id, provider in state.get("providers", {}).items():
        provider.setdefault("family_id", legacy_family_id(provider_id))
    return state


def verify_legacy_core_family_migration(home: str | Path) -> dict:
    """Verify old hash chain and normalized state equivalence without mutation."""
    home = Path(home)
    events = home / "events.jsonl"
    snapshot = home / "state.json"
    if not events.exists() or not snapshot.exists():
        raise GateError("Legacy Core requires events.jsonl and state.json")

    try:
        cached = json.loads(snapshot.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise GateError("Legacy Core snapshot is missing or invalid") from exc

    state = initial_state()
    previous = "0" * 64
    count = 0
    with events.open("r", encoding="utf-8") as fh:
        for raw in fh:
            count += 1
            try:
                event = json.loads(raw)
                if set(event) != {"seq", "prev", "at", "command", "hash"}:
                    raise GateError("Unexpected legacy Core event fields")
                body = {k: event[k] for k in ("seq", "prev", "at", "command")}
                if event["seq"] != count or event["prev"] != previous or digest(body) != event["hash"]:
                    raise GateError("Legacy Core event chain mismatch")
                state = evolve(state, _normalize_command(event["command"]), event["at"])
                previous = event["hash"]
            except (ValueError, TypeError, KeyError) as exc:
                raise GateError(f"Invalid legacy Core event at line {count}: {exc}") from exc

    if cached.get("event_count") != count or cached.get("head") != previous:
        raise GateError("Legacy Core snapshot head/count mismatch")
    normalized_cached = _normalize_legacy_snapshot_state(cached.get("state", {}))
    if normalized_cached != state:
        raise GateError("Legacy Core normalized state differs after family migration replay")

    return {
        "status": "LEGACY_CORE_PROVIDER_FAMILY_MIGRATION_VERIFIED",
        "source_schema": CORE_LEGACY_SCHEMA,
        "target_schema": CORE_CURRENT_SCHEMA,
        "event_count": count,
        "head": previous,
        "normalized_state_digest": digest(state),
        "history_policy": "READ_ONLY_DO_NOT_REWRITE",
        "provider_family_policy": "LEGACY_PROVIDER_IDS_MAP_TO_DETERMINISTIC_UNVERIFIED_FAMILIES",
        "semantic_note": "Structural replay does not prove historical provider-family independence.",
    }
