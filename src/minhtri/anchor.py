"""Provider-neutral verification for external MINH TRÍ ledger anchors.

Publication/storage is intentionally out of scope: an anchor is only useful when its
write authority is independent from the local ledger writer.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA = "minhtri-ledger-anchor/v1"
PROJECT = "MINH_TRI_UNIVERSAL_INTELLIGENCE_OS"


def _utc_time(value: Any) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError("timestamp must be UTC Z form")
    parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise ValueError("timestamp must be UTC")
    return parsed.astimezone(timezone.utc)


def _digest(record: dict[str, Any]) -> str:
    payload = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def make_anchor(event_count: int, head: str, created_at: str, previous_anchor: str | None = None) -> dict[str, Any]:
    if type(event_count) is not int or event_count < 0:
        raise ValueError("event_count must be a nonnegative integer")
    if not isinstance(head, str) or len(head) != 64 or any(c not in "0123456789abcdef" for c in head):
        raise ValueError("head must be lowercase sha256 hex")
    _utc_time(created_at)
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
        if (type(record["event_count"]) is not int or record["event_count"] < 0
                or not _valid_hex(record["head"])
                or not isinstance(record["created_at"], str) or not record["created_at"]
                or (record["previous_anchor"] is not None and not _valid_hex(record["previous_anchor"]))
                or not _valid_hex(anchor.get("anchor_id"))
                or type(local_count) is not int or local_count < 0
                or not _valid_hex(local_head)):
            return {"status": "FAIL", "reason": "MALFORMED_ANCHOR"}
        try:
            _utc_time(record["created_at"])
        except ValueError:
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


def _valid_hex(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(ch in "0123456789abcdef" for ch in value)


def verify_anchor_chain(anchors: list[dict[str, Any]]) -> dict[str, Any]:
    """Verify anchor schema/digests and exact previous-anchor continuity."""
    if not isinstance(anchors, list) or not anchors:
        return {"status": "UNKNOWN", "reason": "MISSING_EXTERNAL_ANCHOR"}
    previous_id = None
    previous_count = -1
    previous_time = None
    for index, anchor in enumerate(anchors):
        if not isinstance(anchor, dict):
            return {"status": "FAIL", "reason": "MALFORMED_ANCHOR", "index": index}
        try:
            record = {k: anchor[k] for k in ("schema", "project", "event_count", "head", "created_at", "previous_anchor")}
        except KeyError:
            return {"status": "FAIL", "reason": "MALFORMED_ANCHOR", "index": index}
        if record["schema"] != SCHEMA or record["project"] != PROJECT:
            return {"status": "FAIL", "reason": "ANCHOR_IDENTITY_MISMATCH", "index": index}
        if type(record["event_count"]) is not int or record["event_count"] < 0 or record["event_count"] <= previous_count:
            return {"status": "FAIL", "reason": "ANCHOR_COUNT_NOT_INCREASING", "index": index}
        if not _valid_hex(record["head"]):
            return {"status": "FAIL", "reason": "MALFORMED_ANCHOR", "index": index}
        try:
            current_time = _utc_time(record["created_at"])
        except (TypeError, ValueError):
            return {"status": "FAIL", "reason": "MALFORMED_ANCHOR", "index": index}
        if previous_time is not None and current_time <= previous_time:
            return {"status": "FAIL", "reason": "ANCHOR_TIME_NOT_INCREASING", "index": index}
        if index == 0:
            if record["previous_anchor"] is not None:
                return {"status": "FAIL", "reason": "BROKEN_ANCHOR_CHAIN", "index": index}
        elif record["previous_anchor"] != previous_id:
            return {"status": "FAIL", "reason": "BROKEN_ANCHOR_CHAIN", "index": index}
        expected = _digest(record)
        if not _valid_hex(anchor.get("anchor_id")) or anchor["anchor_id"] != expected:
            return {"status": "FAIL", "reason": "ANCHOR_DIGEST_MISMATCH", "index": index}
        previous_id = expected
        previous_count = record["event_count"]
        previous_time = current_time
    return {"status": "PASS", "reason": "ANCHOR_CHAIN_VALID", "anchor_count": len(anchors), "head_anchor_id": previous_id}


def ledger_prefix_head(events_path: str | Path, event_count: int) -> str:
    """Return the verified hash-chain head at an exact historical event count."""
    if type(event_count) is not int or event_count < 0:
        raise ValueError("event_count must be a nonnegative integer")
    previous = "0" * 64
    count = 0
    path = Path(events_path)
    if not path.is_file():
        raise ValueError("ledger events missing")
    from .core import digest, identifier
    with path.open("r", encoding="utf-8") as fh:
        for raw in fh:
            count += 1
            try:
                event = json.loads(raw)
                if set(event) - {"approved_by"} != {"seq", "prev", "at", "command", "hash"}:
                    raise ValueError("unexpected event fields")
                body = {k: event[k] for k in ("seq", "prev", "at", "command", "approved_by") if k in event}
                if "approved_by" in event:
                    identifier(event["approved_by"], "approved_by")
                if event["seq"] != count or event["prev"] != previous or digest(body) != event["hash"]:
                    raise ValueError("event chain mismatch")
                previous = event["hash"]
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError(f"invalid event at line {count}") from exc
            if count == event_count:
                return previous
    if event_count == 0:
        return "0" * 64
    raise ValueError("ledger shorter than requested event_count")


def verify_historical_anchor(events_path: str | Path, anchor: dict[str, Any] | None) -> dict[str, Any]:
    """Verify an anchor against the exact historical prefix of a current ledger."""
    if anchor is None:
        return {"status": "UNKNOWN", "reason": "MISSING_EXTERNAL_ANCHOR"}
    try:
        count = anchor["event_count"]
        prefix = ledger_prefix_head(events_path, count)
    except (KeyError, TypeError, ValueError):
        return {"status": "FAIL", "reason": "HISTORICAL_PREFIX_UNVERIFIABLE"}
    result = verify_anchor(count, prefix, anchor)
    if result.get("status") == "PASS":
        return {**result, "reason": "HISTORICAL_PREFIX_MATCH"}
    return result
