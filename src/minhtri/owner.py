"""Declared-ID + shared-secret Owner gate for sensitive CLI commands.

This compares a declared actor ID with a locally configured owner_id, then the SHA-256 of a
secret with owner_secret_sha256. It is not identity verification: anyone holding the config
file and the secret passes, and nothing recognises a real person.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
from pathlib import Path

from .core import GateError, identifier

DEFAULT_CONFIG = Path("config") / "owner.json"
ENV_CONFIG = "MINHTRI_OWNER_CONFIG"
ENV_SECRET = "MINHTRI_OWNER_SECRET"
PLACEHOLDER_ID = "doi-ten-owner"
PLACEHOLDER_SECRET_SHA256 = "0" * 64
SENSITIVE_APPLY_TYPES = frozenset({"activate_trial_lesson", "set_learning_focus"})
CONFIG_FIELDS = {"owner_id", "owner_secret_sha256"}


class OwnerGateError(GateError):
    def __init__(self, code: str, detail: str):
        super().__init__(f"{code}: {detail}")
        self.code, self.detail = code, detail


def config_path(explicit: str | None) -> Path:
    return Path(explicit or os.environ.get(ENV_CONFIG) or DEFAULT_CONFIG)


def hash_secret(secret: str) -> str:
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()


def load_owner_config(path: Path) -> dict:
    if not path.is_file():
        raise OwnerGateError("MISSING_OWNER_CONFIG", f"{path} not found; copy config/owner.example.json and fill it in")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise OwnerGateError("INVALID_OWNER_CONFIG", f"{path} is not valid JSON") from exc
    if not isinstance(data, dict) or "owner_id" not in data or set(data) - CONFIG_FIELDS:
        raise OwnerGateError("INVALID_OWNER_CONFIG", "config fields must be owner_id and owner_secret_sha256")
    try:
        identifier(data["owner_id"], "owner_id")
    except GateError as exc:
        raise OwnerGateError("INVALID_OWNER_CONFIG", str(exc)) from exc
    if data["owner_id"] == PLACEHOLDER_ID:
        raise OwnerGateError("INVALID_OWNER_CONFIG", "owner_id is still the example placeholder")
    if "owner_secret_sha256" in data:
        digest = data["owner_secret_sha256"]
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise OwnerGateError("INVALID_OWNER_CONFIG", "owner_secret_sha256 must be 64 lowercase hex characters")
        if digest == PLACEHOLDER_SECRET_SHA256:
            raise OwnerGateError("INVALID_OWNER_CONFIG", "owner_secret_sha256 is still the example placeholder")
    return data


def require_owner(actor: str | None, secret: str | None, path: Path) -> str:
    """Fail closed. Order: config, then declared ID, then secret. Returns the matched owner_id."""
    config = load_owner_config(path)
    if not actor:
        raise OwnerGateError("OWNER_ID_REQUIRED", "pass --owner-id for this command")
    if actor != config["owner_id"]:
        raise OwnerGateError("OWNER_MISMATCH", "--owner-id does not match the configured owner_id")
    if "owner_secret_sha256" not in config:
        raise OwnerGateError("MISSING_OWNER_SECRET", "config has no owner_secret_sha256; run hash-secret and add it")
    if not secret:
        raise OwnerGateError("OWNER_SECRET_REQUIRED", f"pass --owner-secret or set {ENV_SECRET}")
    if not hmac.compare_digest(hash_secret(secret), config["owner_secret_sha256"]):
        raise OwnerGateError("OWNER_SECRET_MISMATCH", "secret does not match owner_secret_sha256")
    return config["owner_id"]
