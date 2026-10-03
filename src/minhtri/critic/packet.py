"""Build a blind, redacted, hash-bound external critic packet."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
from typing import Any, Sequence

PACKET_PROTOCOL = "minhtri-external-critic-packet/v1"
MAX_ARTIFACT_CHARS = 200_000
_HASH64 = re.compile(r"^[0-9a-f]{64}$")
_SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{16,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
)
_OWNER_PATH = re.compile(r"(?i)[A-Z]:\\Users\\[^\\\r\n\t ]+")


class CriticPacketError(ValueError):
    pass


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _redact_and_validate(text: str) -> str:
    redacted = _OWNER_PATH.sub("[REDACTED_OWNER_PATH]", text)
    for pattern in _SECRET_PATTERNS:
        if pattern.search(redacted):
            raise CriticPacketError("packet contains secret-like material")
    return redacted


def _artifact_text(root: Path, changed_paths: Sequence[str]) -> str:
    root = root.resolve()
    chunks: list[str] = []
    for raw in sorted(set(changed_paths)):
        rel = Path(raw)
        if rel.is_absolute() or ".." in rel.parts:
            raise CriticPacketError("candidate path traversal is forbidden")
        path = (root / rel).resolve()
        try:
            path.relative_to(root)
        except ValueError as exc:
            raise CriticPacketError("candidate path escapes worktree") from exc
        label = raw.replace("\\", "/")
        if not path.exists():
            body = "[DELETED]"
        elif path.is_dir():
            raise CriticPacketError("candidate artifact path must be a file")
        else:
            data = path.read_bytes()
            if b"\x00" in data:
                body = "[BINARY sha256=" + hashlib.sha256(data).hexdigest() + "]"
            else:
                body = data.decode("utf-8", errors="replace")
        chunks.append(f"=== {label} ===\n{body}")
    joined = "\n\n".join(chunks)
    if len(joined) > MAX_ARTIFACT_CHARS:
        raise CriticPacketError("candidate artifact exceeds external critic packet limit")
    return joined


def build_critic_packet(
    *,
    candidate_root: Path,
    candidate_generation_id: str,
    lease_id: str,
    changed_paths: Sequence[str],
    test_log: str,
    claims: Sequence[str],
    eval_packet_hash: str,
) -> dict[str, Any]:
    if not isinstance(candidate_generation_id, str) or not candidate_generation_id.strip():
        raise CriticPacketError("candidate_generation_id is required")
    if not isinstance(lease_id, str) or not lease_id.strip():
        raise CriticPacketError("lease_id is required")
    if not isinstance(eval_packet_hash, str) or not _HASH64.fullmatch(eval_packet_hash):
        raise CriticPacketError("eval_packet_hash must be pinned sha256")
    if not isinstance(test_log, str):
        raise CriticPacketError("test_log must be text")
    clean_claims: list[str] = []
    for claim in claims:
        if not isinstance(claim, str) or not claim.strip():
            raise CriticPacketError("claims must be nonempty text")
        if "\n" in claim or "\r" in claim:
            raise CriticPacketError("each claim must be exactly one line")
        clean_claims.append(claim.strip())
    if not clean_claims:
        raise CriticPacketError("at least one explicit claim is required")

    payload = {
        "protocol": PACKET_PROTOCOL,
        "packet_id": "critic-" + hashlib.sha256(
            (candidate_generation_id + "|" + lease_id).encode("utf-8")
        ).hexdigest()[:24],
        "candidate_generation_id": candidate_generation_id,
        "lease_id": lease_id,
        "diff_or_artifact": _redact_and_validate(
            _artifact_text(candidate_root, changed_paths)
        ),
        "test_log": _redact_and_validate(test_log),
        "claims": [_redact_and_validate(claim) for claim in clean_claims],
        "eval_packet_hash": eval_packet_hash,
        "redaction_applied": True,
    }
    payload["packet_hash"] = hashlib.sha256(_canonical(payload)).hexdigest()
    return payload


def verify_packet_hash(packet: dict[str, Any]) -> bool:
    if not isinstance(packet, dict):
        return False
    packet_hash = packet.get("packet_hash")
    if not isinstance(packet_hash, str) or not _HASH64.fullmatch(packet_hash):
        return False
    body = dict(packet)
    body.pop("packet_hash", None)
    expected = hashlib.sha256(_canonical(body)).hexdigest()
    return expected == packet_hash and packet.get("redaction_applied") is True
