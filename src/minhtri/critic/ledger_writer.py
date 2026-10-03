"""Append-only ledger adapter for external critic evidence."""
from __future__ import annotations

from typing import Any

from minhtri.core import Ledger


def external_critic_run_command(
    *,
    record_id: str,
    candidate_generation_id: str,
    lease_id: str,
    receipt: dict[str, Any],
) -> dict[str, Any]:
    return {
        "type": "record_external_critic_run",
        "data": {
            "id": record_id,
            "candidate_generation_id": candidate_generation_id,
            "lease_id": lease_id,
            "critic_provider": receipt["critic_provider"],
            "critic_model": receipt["critic_model"],
            "prompt_version": receipt["prompt_version"],
            "run_id": receipt["run_id"],
            "packet_hash": receipt["packet_hash"],
            "output_hash": receipt["output_hash"],
            "blind_or_revealed": receipt["blind_or_revealed"],
            "channel": receipt["channel"],
            "independence_status": receipt["independence_status"],
            "verdict": receipt["verdict"],
            "findings": receipt["findings"],
            "post_expiry": bool(receipt.get("post_expiry", False)),
        },
    }


def append_external_critic_run(
    ledger: Ledger,
    *,
    record_id: str,
    candidate_generation_id: str,
    lease_id: str,
    receipt: dict[str, Any],
    actor: str,
    secret: str,
) -> dict[str, Any]:
    return ledger.apply(
        external_critic_run_command(
            record_id=record_id,
            candidate_generation_id=candidate_generation_id,
            lease_id=lease_id,
            receipt=receipt,
        ),
        actor=actor,
        secret=secret,
    )
