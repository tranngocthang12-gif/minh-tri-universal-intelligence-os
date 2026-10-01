"""External witness receipts for detecting whole-ledger history rewrites.

The receipt is useful only when its bytes are fetched from a write authority that is
independent from the local brain writer. This module does not publish the receipt; it
validates the externally preserved checkpoint against the local ledger prefix.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .anchor import PROJECT, verify_anchor, verify_historical_anchor

SCHEMA = "minhtri-external-witness/v1"


def _digest(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _utc_z(value: Any) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    from datetime import datetime, timezone
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() == timezone.utc.utcoffset(parsed)


def make_witness_receipt(
    anchor: dict[str, Any],
    *,
    authority: str,
    locator: str,
    published_at: str,
) -> dict[str, Any]:
    """Wrap one valid anchor in storage/provenance metadata for remote preservation."""
    if not isinstance(authority, str) or not authority.strip():
        raise ValueError("authority must be nonempty text")
    if not isinstance(locator, str) or not locator.strip():
        raise ValueError("locator must be nonempty text")
    if not _utc_z(published_at):
        raise ValueError("published_at must be UTC Z timestamp")
    result = verify_anchor(anchor.get("event_count", -1), anchor.get("head", ""), anchor)
    if result.get("status") != "PASS":
        raise ValueError("anchor is not self-consistent")
    record = {
        "schema": SCHEMA,
        "project": PROJECT,
        "authority": authority.strip(),
        "locator": locator.strip(),
        "published_at": published_at,
        "anchor": anchor,
    }
    return {**record, "receipt_id": _digest(record)}


def verify_witness_receipt(receipt: dict[str, Any] | None) -> dict[str, Any]:
    if receipt is None:
        return {"status": "UNKNOWN", "reason": "MISSING_EXTERNAL_WITNESS"}
    if not isinstance(receipt, dict):
        return {"status": "FAIL", "reason": "MALFORMED_WITNESS"}
    try:
        record = {
            "schema": receipt["schema"],
            "project": receipt["project"],
            "authority": receipt["authority"],
            "locator": receipt["locator"],
            "published_at": receipt["published_at"],
            "anchor": receipt["anchor"],
        }
    except KeyError:
        return {"status": "FAIL", "reason": "MALFORMED_WITNESS"}
    if record["schema"] != SCHEMA or record["project"] != PROJECT:
        return {"status": "FAIL", "reason": "WITNESS_IDENTITY_MISMATCH"}
    if not isinstance(record["authority"], str) or not record["authority"].strip():
        return {"status": "FAIL", "reason": "MALFORMED_WITNESS"}
    if not isinstance(record["locator"], str) or not record["locator"].strip() or not _utc_z(record["published_at"]):
        return {"status": "FAIL", "reason": "MALFORMED_WITNESS"}
    if receipt.get("receipt_id") != _digest(record):
        return {"status": "FAIL", "reason": "WITNESS_DIGEST_MISMATCH"}
    anchor = record["anchor"]
    if not isinstance(anchor, dict):
        return {"status": "FAIL", "reason": "MALFORMED_WITNESS"}
    result = verify_anchor(anchor.get("event_count", -1), anchor.get("head", ""), anchor)
    if result.get("status") != "PASS":
        return {"status": "FAIL", "reason": "WITNESS_ANCHOR_INVALID"}
    return {
        "status": "PASS",
        "reason": "EXTERNAL_WITNESS_RECEIPT_VALID",
        "receipt_id": receipt["receipt_id"],
        "event_count": anchor["event_count"],
        "head": anchor["head"],
        "authority": record["authority"],
        "locator": record["locator"],
    }


def verify_local_history_against_witness(
    events_path: str | Path,
    receipt: dict[str, Any] | None,
) -> dict[str, Any]:
    """Detect whether the local ledger still contains the externally witnessed prefix."""
    checked = verify_witness_receipt(receipt)
    if checked.get("status") != "PASS":
        return checked
    result = verify_historical_anchor(events_path, receipt["anchor"])
    if result.get("status") == "PASS":
        return {
            **result,
            "reason": "LOCAL_HISTORY_MATCHES_EXTERNAL_WITNESS",
            "receipt_id": receipt["receipt_id"],
            "authority": receipt["authority"],
            "locator": receipt["locator"],
        }
    return {
        **result,
        "reason": "LOCAL_HISTORY_DIVERGES_FROM_EXTERNAL_WITNESS",
        "receipt_id": receipt["receipt_id"],
        "authority": receipt["authority"],
        "locator": receipt["locator"],
    }
