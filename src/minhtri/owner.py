"""Declared-ID Owner gate for sensitive CLI commands.

This only compares a declared actor ID with a locally configured owner_id. It is not
identity verification: anyone who can edit the config file or pass the flag can match it.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from .core import GateError, identifier

DEFAULT_CONFIG = Path("config") / "owner.json"
ENV_CONFIG = "MINHTRI_OWNER_CONFIG"
PLACEHOLDER_ID = "doi-ten-owner"
SENSITIVE_APPLY_TYPES = frozenset({"activate_trial_lesson", "set_learning_focus"})


class OwnerGateError(GateError):
    def __init__(self, code: str, detail: str):
        super().__init__(f"{code}: {detail}")
        self.code, self.detail = code, detail


def config_path(explicit: str | None) -> Path:
    return Path(explicit or os.environ.get(ENV_CONFIG) or DEFAULT_CONFIG)


def load_owner_id(path: Path) -> str:
    if not path.is_file():
        raise OwnerGateError("MISSING_OWNER_CONFIG", f"{path} not found; copy config/owner.example.json and set owner_id")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise OwnerGateError("INVALID_OWNER_CONFIG", f"{path} is not valid JSON") from exc
    if not isinstance(data, dict) or set(data) != {"owner_id"}:
        raise OwnerGateError("INVALID_OWNER_CONFIG", "config must be exactly {\"owner_id\": \"...\"}")
    try:
        owner_id = identifier(data["owner_id"], "owner_id")
    except GateError as exc:
        raise OwnerGateError("INVALID_OWNER_CONFIG", str(exc)) from exc
    if owner_id == PLACEHOLDER_ID:
        raise OwnerGateError("INVALID_OWNER_CONFIG", "owner_id is still the example placeholder")
    return owner_id


def require_owner(actor: str | None, path: Path) -> str:
    """Fail closed: missing config blocks before the actor is even considered."""
    owner_id = load_owner_id(path)
    if not actor:
        raise OwnerGateError("OWNER_ID_REQUIRED", "pass --owner-id for this command")
    if actor != owner_id:
        raise OwnerGateError("OWNER_MISMATCH", "--owner-id does not match the configured owner_id")
    return owner_id
