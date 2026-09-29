"""Versioned GitHub brain manifest for MINH TRI.

The manifest pins repository-level guidance for one task. It does not decide
semantic truth; it only proves which versioned artifacts the task was bound to.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path
from typing import Any

from .core import GateError, digest


BRAIN_SCHEMA_VERSION = 1
BRAIN_ARTIFACTS = (
    "PROJECT_LAW.md",
    "BOOTSTRAP.md",
    "AGENTS.md",
    "docs/PHILOSOPHY.md",
    "docs/ARCHITECTURE.md",
    "docs/CORE_PROTECTION_CONTRACT_V0.1.md",
    "docs/UNIVERSAL_BRAIN_ARCHITECTURE_V0.2_CANDIDATE.md",
    "docs/ARCHITECTURE_MEMORY_AND_CONTINUITY_V0.1.md",
    "docs/AI_COMMONS_ARCHITECTURE_V0.1.md",
    "docs/ARENA_SCHEMA_MIGRATION_V0.1.md",
    "docs/CANONICAL_TASK_HANDOFF_V0.1.md",
    "docs/EPISTEMIC_STATE_LEARNING_MATURITY_V0.1.md",
    "docs/GOAL_DECOMPOSITION_BOTTLENECK_GOVERNOR_V0.1.md",
    "docs/R4_5_ARCHITECTURE_STABILIZATION_GATE.md",
    "docs/LEDGER_SCHEMA_COMPATIBILITY_V0.1.md",
    "docs/PROJECT_STATE.json",
    "docs/ROADMAP.md",
)


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _revision(value: Any) -> str:
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{40}", value) is None:
        raise GateError("brain_revision must be a 40-character lowercase Git SHA")
    return value


def resolve_git_revision(root: str | Path) -> str:
    """Resolve the checked-out Git commit, failing closed outside a Git checkout."""
    try:
        run = subprocess.run(
            ["git", "-C", str(Path(root)), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise GateError("Cannot resolve brain Git revision; provide an explicit pinned revision") from exc
    return _revision(run.stdout.strip())


def build_brain_manifest(root: str | Path, brain_revision: str | None = None) -> dict:
    """Build a deterministic manifest over the current canonical brain artifacts."""
    root = Path(root)
    revision = _revision(brain_revision) if brain_revision is not None else resolve_git_revision(root)
    artifacts = []
    for relative in BRAIN_ARTIFACTS:
        path = root / relative
        try:
            contents = path.read_bytes()
        except OSError as exc:
            raise GateError(f"Required brain artifact is missing: {relative}") from exc
        artifacts.append({"path": relative, "sha256": _sha256_bytes(contents), "size": len(contents)})
    return {
        "schema_version": BRAIN_SCHEMA_VERSION,
        "project": "MINH_TRI_UNIVERSAL_INTELLIGENCE_OS",
        "brain_revision": revision,
        "artifacts": artifacts,
    }


def brain_bundle(root: str | Path, brain_revision: str | None = None) -> dict:
    manifest = build_brain_manifest(root, brain_revision)
    return {"manifest": manifest, "fingerprint": digest(manifest)}


def verify_brain_manifest(root: str | Path, manifest: dict) -> str:
    """Verify a supplied manifest against local brain artifacts and return its fingerprint."""
    if not isinstance(manifest, dict) or set(manifest) != {"schema_version", "project", "brain_revision", "artifacts"}:
        raise GateError("Invalid brain manifest shape")
    if manifest["schema_version"] != BRAIN_SCHEMA_VERSION or manifest["project"] != "MINH_TRI_UNIVERSAL_INTELLIGENCE_OS":
        raise GateError("Unsupported brain manifest")
    revision = _revision(manifest["brain_revision"])
    expected = build_brain_manifest(root, revision)
    if expected != manifest:
        raise GateError("Brain manifest does not match current repository artifacts")
    return digest(manifest)


def manifest_artifact_sha(manifest: dict, path: str) -> str:
    """Return one pinned artifact digest from a validated manifest-shaped object."""
    for artifact in manifest.get("artifacts", []):
        if artifact.get("path") == path:
            return artifact["sha256"]
    raise GateError(f"Brain manifest does not contain required artifact: {path}")
