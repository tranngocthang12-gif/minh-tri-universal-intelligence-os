"""Provider-neutral verification for external MINH TRÍ ledger anchors.

Publication/storage is intentionally out of scope: an anchor is only useful when its
write authority is independent from the local ledger writer.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

SCHEMA = "minhtri-ledger-anchor/v1"
PROJECT = "MINH_TRI_UNIVERSAL_INTELLIGENCE_OS"


def _digest(record: dict[str, Any]) -> str:
    payload = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def make_anchor(event_count: int, head: str, created_at: str, previous_anchor: str | None = None) -> dict[str, Any]:
    if type(event_count) is not int or event_count < 0:
        raise ValueError("event_count must be a nonnegative integer")
    if not isinstance(head, str) or len(head) != 64 or any(c not in "0123456789abcdef" for c in head):
        raise ValueError("head must be lowercase sha256 hex")
    if not isinstance(created_at, str) or not created_at:
        raise ValueError("created_at is required")
    if previous_anchor is not None and (
        not isinstance(previous_anchor, str)
        or len(previous_anchor) != 64
        or any(c not in "0123456789abcdef" for c in previous_anchor)
    ):
        raise ValueError("previous_anchor must be sha256 hex or null")
    record = {
        "schema": SCHEMA,
        "project": PROJECT,
        "event_count": event_count,
        "head": head,
        "created_at": created_at,
        "previous_anchor": previous_anchor,
    }
    return {**record, "anchor_id": _digest(record)}


def verify_anchor(local_count: int, local_head: str, anchor: dict[str, Any] | None) -> dict[str, Any]:
    if anchor is None:
        return {"status": "UNKNOWN", "reason": "MISSING_EXTERNAL_ANCHOR"}
    try:
        record = {k: anchor[k] for k in ("schema", "project", "event_count", "head", "created_at", "previous_anchor")}
        expected_id = _digest(record)
        if anchor.get("anchor_id") != expected_id:
            return {"status": "FAIL", "reason": "ANCHOR_DIGEST_MISMATCH"}
        if record["schema"] != SCHEMA or record["project"] != PROJECT:
            return {"status": "FAIL", "reason": "ANCHOR_IDENTITY_MISMATCH"}
        if type(record["event_count"]) is not int or record["event_count"] < 0:
            return {"status": "FAIL", "reason": "MALFORMED_ANCHOR"}
        if local_count < record["event_count"]:
            return {"status": "FAIL", "reason": "LOCAL_LEDGER_ROLLBACK"}
        if local_count == record["event_count"] and local_head != record["head"]:
            return {"status": "FAIL", "reason": "LEDGER_HEAD_MISMATCH"}
        if local_count > record["event_count"]:
            return {"status": "UNKNOWN", "reason": "LOCAL_LEDGER_AHEAD_OF_ANCHOR"}
        return {"status": "PASS", "reason": "EXACT_EXTERNAL_ANCHOR_MATCH", "anchor_id": expected_id}
    except (KeyError, TypeError, ValueError):
        return {"status": "FAIL", "reason": "MALFORMED_ANCHOR"}
