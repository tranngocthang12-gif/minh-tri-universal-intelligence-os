"""Owner-mediated external critic channel.

No network call is made. The module exports a blind packet envelope and, if a response
file exists, validates and hashes that response. A late response can be parsed as
POST_EXPIRY evidence but cannot authorize candidate mutation or freeze.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
from typing import Any

from .packet import CriticPacketError, verify_packet_hash
from .verdict_schema import CriticResult, CriticSchemaError

PROMPT_VERSION = "external-critic-v1"
PROMPT_PATH = Path(__file__).with_name("prompt_external_v1.txt")


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


@dataclass
class ManualExternalCritic:
    packet_out_path: Path
    response_in_path: Path
    critic_provider: str = "external-manual"
    critic_model: str = "owner-declared-external-model"
    run_id: str = "manual-run"

    def _prompt(self) -> str:
        return PROMPT_PATH.read_text(encoding="utf-8")

    def export_packet(self, packet: dict[str, Any]) -> None:
        if not verify_packet_hash(packet):
            raise CriticPacketError("external critic packet hash/redaction check failed")
        _atomic_json(
            self.packet_out_path,
            {
                "prompt_version": PROMPT_VERSION,
                "prompt": self._prompt(),
                "packet": packet,
            },
        )

    def parse_response(
        self,
        packet: dict[str, Any],
        response_text: str,
        *,
        post_expiry: bool = False,
    ) -> dict[str, Any]:
        if not verify_packet_hash(packet):
            raise CriticPacketError("external critic packet hash/redaction check failed")
        try:
            result = CriticResult.from_json_text(response_text)
        except CriticSchemaError as exc:
            return {
                "status": "CRITIC_RUN_INVALID",
                "reason": str(exc),
                "channel": "OWNER_MANUAL",
                "prompt_version": PROMPT_VERSION,
                "packet_hash": packet["packet_hash"],
                "post_expiry": bool(post_expiry),
                "eligible_as_critic_evidence": False,
            }
        output_hash = hashlib.sha256(response_text.encode("utf-8")).hexdigest()
        return {
            "status": "POST_EXPIRY" if post_expiry else "RECORDED",
            "critic_provider": self.critic_provider,
            "critic_model": self.critic_model,
            "prompt_version": PROMPT_VERSION,
            "run_id": self.run_id,
            "packet_hash": packet["packet_hash"],
            "output_hash": output_hash,
            "blind_or_revealed": "BLIND",
            "channel": "OWNER_MANUAL",
            "independence_status": "PARTIAL",
            "verdict": result.verdict,
            "findings": [finding.to_dict() for finding in result.findings],
            "confidence_note": result.confidence_note,
            "post_expiry": bool(post_expiry),
            "automatic_verified_promotion": False,
            "owner_decision_required": True,
        }

    def critique(self, packet: dict[str, Any]) -> dict[str, Any]:
        self.export_packet(packet)
        if not self.response_in_path.is_file():
            return {
                "status": "PENDING_EXTERNAL_CRITIC",
                "channel": "OWNER_MANUAL",
                "prompt_version": PROMPT_VERSION,
                "packet_hash": packet["packet_hash"],
                "response_path": str(self.response_in_path),
                "automatic_verified_promotion": False,
            }
        response_text = self.response_in_path.read_text(encoding="utf-8")
        return self.parse_response(packet, response_text)
