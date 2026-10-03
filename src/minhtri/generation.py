"""Candidate-generation lineage and sandbox policy for bounded self-upgrade."""
from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
import re
from typing import Iterable

from .upgrade_lease import LeaseRuntimeGuard

GEN_DRAFT = "DRAFT"
GEN_READY_FOR_TEST = "READY_FOR_TEST"
GEN_TESTING = "TESTING"
GEN_REJECTED = "REJECTED"
GEN_CANDIDATE = "CANDIDATE"
GEN_FROZEN_PENDING_OWNER = "FROZEN_PENDING_OWNER"
GEN_PROMOTED_BY_OWNER = "PROMOTED_BY_OWNER"
GEN_SUPERSEDED = "SUPERSEDED"
GEN_ABANDONED_AT_EXPIRY = "ABANDONED_AT_EXPIRY"

GENERATION_STATUSES = frozenset({
    GEN_DRAFT,
    GEN_READY_FOR_TEST,
    GEN_TESTING,
    GEN_REJECTED,
    GEN_CANDIDATE,
    GEN_FROZEN_PENDING_OWNER,
    GEN_PROMOTED_BY_OWNER,
    GEN_SUPERSEDED,
    GEN_ABANDONED_AT_EXPIRY,
})

CANDIDATE_BRANCH_PREFIXES = ("candidate/", "self-upgrade/")

PROTECTED_EXACT_PATHS = frozenset({
    "src/minhtri/upgrade_lease.py",
    "src/minhtri/generation.py",
    "src/minhtri/evolution.py",
    "src/minhtri/candidate_executor.py",
    "src/minhtri/codex_provider.py",
    "src/minhtri/lease_bound_worker.py",
    "src/minhtri/candidate_lifecycle.py",
    "src/minhtri/owner.py",
    "src/minhtri/core.py",
    "config/owner.json",
    "docs/PROJECT_STATE.json",
    "tests/test_upgrade_lease.py",
    "tests/test_generation.py",
    "tests/test_evolution.py",
    "tests/test_candidate_executor.py",
    "tests/test_codex_provider.py",
    "tests/test_lease_bound_worker.py",
    "tests/test_candidate_lifecycle.py",
    "tests/test_owner_gate.py",
    "tests/test_security_p0.py",
    "ops/windows/self_upgrade_owner_revoke_probe.py",
    "pyproject.toml",
})

PROTECTED_PREFIXES = (
    ".github/",
    "tests/",
    "ops/windows/",
    "config/",
    "src/minhtri/critic/",
    "docs/LAW_INDEX",
    "docs/ARCHITECTURE_NOW",
    "docs/OWNER_DECISION_24H_SELF_UPGRADE_LEASE",
)


class GenerationError(ValueError):
    pass


class CandidateSandboxError(GenerationError):
    pass


@dataclass(frozen=True)
class GenerationManifest:
    generation_id: str
    parent_generation_id: str
    candidate_commit_sha: str
    candidate_branch: str
    created_under_lease_id: str
    mutation_summary: str
    hypothesis: str
    expected_improvement: str
    known_risks: tuple[str, ...]
    files_changed: tuple[str, ...]
    test_plan: str
    benchmark_plan: str
    created_at_utc: str
    status: str = GEN_DRAFT

    def __post_init__(self) -> None:
        if self.status not in GENERATION_STATUSES:
            raise GenerationError("invalid generation status")
        for value, name in (
            (self.generation_id, "generation_id"),
            (self.parent_generation_id, "parent_generation_id"),
            (self.created_under_lease_id, "created_under_lease_id"),
            (self.mutation_summary, "mutation_summary"),
            (self.hypothesis, "hypothesis"),
            (self.expected_improvement, "expected_improvement"),
            (self.test_plan, "test_plan"),
            (self.benchmark_plan, "benchmark_plan"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise GenerationError(f"{name} is required")
        if not re.fullmatch(r"[0-9a-f]{40,64}", self.candidate_commit_sha):
            raise GenerationError("candidate_commit_sha must be a lowercase hex commit digest")
        if not self.known_risks:
            raise GenerationError("known_risks must be nonempty")
        if not self.files_changed:
            raise GenerationError("files_changed must be nonempty")

    def to_dict(self) -> dict:
        return {
            "generation_id": self.generation_id,
            "parent_generation_id": self.parent_generation_id,
            "candidate_commit_sha": self.candidate_commit_sha,
            "candidate_branch": self.candidate_branch,
            "created_under_lease_id": self.created_under_lease_id,
            "mutation_summary": self.mutation_summary,
            "hypothesis": self.hypothesis,
            "expected_improvement": self.expected_improvement,
            "known_risks": list(self.known_risks),
            "files_changed": list(self.files_changed),
            "test_plan": self.test_plan,
            "benchmark_plan": self.benchmark_plan,
            "created_at_utc": self.created_at_utc,
            "status": self.status,
            "automatic_promotion": False,
        }


def _normalized_path(path: str) -> str:
    if not isinstance(path, str) or not path.strip():
        raise CandidateSandboxError("changed path must be nonempty")
    normalized = path.replace("\\", "/").lstrip("/")
    if normalized.startswith("../") or "/../" in normalized or normalized == "..":
        raise CandidateSandboxError("path traversal is forbidden")
    return normalized


def enforce_candidate_mutation(
    guard: LeaseRuntimeGuard,
    *,
    candidate_branch: str,
    changed_paths: Iterable[str],
    now: datetime | None = None,
    monotonic_now: float | None = None,
) -> tuple[str, ...]:
    """Authorize only candidate-branch mutations outside authority/security controls."""
    guard.before_mutation(now=now, monotonic_now=monotonic_now)
    if candidate_branch in {"main", "master"} or not candidate_branch.startswith(CANDIDATE_BRANCH_PREFIXES):
        raise CandidateSandboxError("self-upgrade writes require a candidate/self-upgrade branch")

    normalized = tuple(sorted({_normalized_path(path) for path in changed_paths}))
    if not normalized:
        raise CandidateSandboxError("candidate mutation must name changed paths")

    for path in normalized:
        if path in PROTECTED_EXACT_PATHS:
            raise CandidateSandboxError(f"candidate cannot modify protected authority path: {path}")
        if any(path.startswith(prefix) for prefix in PROTECTED_PREFIXES):
            raise CandidateSandboxError(f"candidate cannot modify protected authority prefix: {path}")
    return normalized


def create_generation_manifest(
    guard: LeaseRuntimeGuard,
    *,
    generation_id: str,
    parent_generation_id: str,
    candidate_commit_sha: str,
    candidate_branch: str,
    mutation_summary: str,
    hypothesis: str,
    expected_improvement: str,
    known_risks: Iterable[str],
    files_changed: Iterable[str],
    test_plan: str,
    benchmark_plan: str,
    now: datetime | None = None,
    monotonic_now: float | None = None,
) -> GenerationManifest:
    changed = enforce_candidate_mutation(
        guard,
        candidate_branch=candidate_branch,
        changed_paths=files_changed,
        now=now,
        monotonic_now=monotonic_now,
    )
    created = (now or datetime.now(timezone.utc)).astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    return GenerationManifest(
        generation_id=generation_id,
        parent_generation_id=parent_generation_id,
        candidate_commit_sha=candidate_commit_sha,
        candidate_branch=candidate_branch,
        created_under_lease_id=guard.lease.lease_id,
        mutation_summary=mutation_summary,
        hypothesis=hypothesis,
        expected_improvement=expected_improvement,
        known_risks=tuple(known_risks),
        files_changed=changed,
        test_plan=test_plan,
        benchmark_plan=benchmark_plan,
        created_at_utc=created,
        status=GEN_DRAFT,
    )


def transition_generation(manifest: GenerationManifest, status: str) -> GenerationManifest:
    allowed = {
        GEN_DRAFT: {GEN_READY_FOR_TEST, GEN_REJECTED},
        GEN_READY_FOR_TEST: {GEN_TESTING, GEN_REJECTED},
        GEN_TESTING: {GEN_CANDIDATE, GEN_REJECTED},
        GEN_CANDIDATE: {GEN_FROZEN_PENDING_OWNER, GEN_REJECTED},
        GEN_FROZEN_PENDING_OWNER: {GEN_REJECTED, GEN_PROMOTED_BY_OWNER},
        GEN_PROMOTED_BY_OWNER: {GEN_SUPERSEDED},
        GEN_REJECTED: set(),
        GEN_SUPERSEDED: set(),
        GEN_ABANDONED_AT_EXPIRY: set(),
    }
    if status not in allowed.get(manifest.status, set()):
        raise GenerationError(f"invalid generation transition: {manifest.status} -> {status}")
    if status == GEN_PROMOTED_BY_OWNER:
        raise GenerationError("promotion requires owner_promote_generation")
    return replace(manifest, status=status)


def freeze_generation(manifest: GenerationManifest) -> GenerationManifest:
    if manifest.status == GEN_CANDIDATE:
        return replace(manifest, status=GEN_FROZEN_PENDING_OWNER)
    if manifest.status == GEN_FROZEN_PENDING_OWNER:
        return manifest
    raise GenerationError("only a CANDIDATE can be frozen pending Owner review")


def owner_promote_generation(
    manifest: GenerationManifest,
    *,
    actor: str | None,
    secret: str | None,
) -> GenerationManifest:
    """Record the Owner promotion decision; this function never merges a branch."""
    from .owner import config_path, require_owner

    require_owner(actor, secret, config_path(None))
    if manifest.status != GEN_FROZEN_PENDING_OWNER:
        raise GenerationError("only a frozen candidate can be promoted")
    return replace(manifest, status=GEN_PROMOTED_BY_OWNER)


def expire_generation(manifest: GenerationManifest) -> GenerationManifest:
    """Finalize one generation when the lease ends without ranking candidates.

    Every generation is handled independently. A completed CANDIDATE is frozen for
    Owner review; unfinished DRAFT/READY_FOR_TEST/TESTING work is marked
    ABANDONED_AT_EXPIRY. No "best candidate" selection occurs here.
    """
    if manifest.status == GEN_CANDIDATE:
        return replace(manifest, status=GEN_FROZEN_PENDING_OWNER)
    if manifest.status in {GEN_DRAFT, GEN_READY_FOR_TEST, GEN_TESTING}:
        return replace(manifest, status=GEN_ABANDONED_AT_EXPIRY)
    if manifest.status in {
        GEN_FROZEN_PENDING_OWNER,
        GEN_REJECTED,
        GEN_PROMOTED_BY_OWNER,
        GEN_SUPERSEDED,
        GEN_ABANDONED_AT_EXPIRY,
    }:
        return manifest
    raise GenerationError("unsupported generation status at expiry")
