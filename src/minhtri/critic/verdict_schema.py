"""Strict schema for external critic output."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any

CRITIC_DEFECT_FOUND = "DEFECT_FOUND"
CRITIC_NO_MATERIAL_DEFECT_FOUND = "NO_MATERIAL_DEFECT_FOUND"
ALLOWED_VERDICTS = {CRITIC_DEFECT_FOUND, CRITIC_NO_MATERIAL_DEFECT_FOUND}
ALLOWED_SEVERITIES = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}


class CriticSchemaError(ValueError):
    pass


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


@dataclass(frozen=True)
class CriticFinding:
    target: str
    severity: str
    failure_path: str
    missing_evidence: tuple[str, ...]

    @classmethod
    def from_dict(cls, raw: Any) -> "CriticFinding":
        if not isinstance(raw, dict) or set(raw) != {
            "target", "severity", "failure_path", "missing_evidence"
        }:
            raise CriticSchemaError("finding must have exact required keys")
        for key in ("target", "failure_path"):
            if not isinstance(raw[key], str) or not raw[key].strip():
                raise CriticSchemaError(f"{key} must be nonempty text")
        severity = raw["severity"]
        if severity not in ALLOWED_SEVERITIES:
            raise CriticSchemaError("invalid finding severity")
        missing = raw["missing_evidence"]
        if not isinstance(missing, list) or any(
            not isinstance(v, str) or not v.strip() for v in missing
        ):
            raise CriticSchemaError("missing_evidence must be a text list")
        return cls(
            target=raw["target"].strip(),
            severity=severity,
            failure_path=raw["failure_path"].strip(),
            missing_evidence=tuple(v.strip() for v in missing),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "target": self.target,
            "severity": self.severity,
            "failure_path": self.failure_path,
            "missing_evidence": list(self.missing_evidence),
        }


@dataclass(frozen=True)
class CriticResult:
    findings: tuple[CriticFinding, ...]
    verdict: str
    confidence_note: str

    @classmethod
    def from_json_text(cls, text: str) -> "CriticResult":
        try:
            raw = json.loads(text)
        except json.JSONDecodeError as exc:
            raise CriticSchemaError("critic output is not JSON") from exc
        if not isinstance(raw, dict) or set(raw) != {
            "findings", "verdict", "confidence_note"
        }:
            raise CriticSchemaError("critic output must have exact required keys")
        if raw["verdict"] not in ALLOWED_VERDICTS:
            raise CriticSchemaError("invalid critic verdict")
        if not isinstance(raw["confidence_note"], str) or not raw["confidence_note"].strip():
            raise CriticSchemaError("confidence_note must be nonempty text")
        if not isinstance(raw["findings"], list):
            raise CriticSchemaError("findings must be a list")
        findings = tuple(CriticFinding.from_dict(item) for item in raw["findings"])
        if raw["verdict"] == CRITIC_NO_MATERIAL_DEFECT_FOUND and findings:
            raise CriticSchemaError("NO_MATERIAL_DEFECT_FOUND cannot include findings")
        if raw["verdict"] == CRITIC_DEFECT_FOUND and not findings:
            raise CriticSchemaError("DEFECT_FOUND requires at least one finding")
        return cls(
            findings=findings,
            verdict=raw["verdict"],
            confidence_note=raw["confidence_note"].strip(),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "findings": [finding.to_dict() for finding in self.findings],
            "verdict": self.verdict,
            "confidence_note": self.confidence_note,
        }

    def output_hash(self) -> str:
        return hashlib.sha256(canonical_json(self.to_dict())).hexdigest()
