"""Lease-bound candidate executor for bounded self-upgrade."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, TypeVar

from .generation import enforce_candidate_mutation
from .self_upgrade_runtime import SelfUpgradeSession

T = TypeVar("T")


@dataclass
class CandidateExecutor:
    session: SelfUpgradeSession
    candidate_branch: str

    def authorize(self, changed_paths: Iterable[str]) -> tuple[str, ...]:
        return enforce_candidate_mutation(
            self.session.guard,
            candidate_branch=self.candidate_branch,
            changed_paths=changed_paths,
        )

    def mutate(self, changed_paths: Iterable[str], action: Callable[[], T]) -> T:
        self.authorize(changed_paths)
        return self.session.guarded_mutation(action)

    def status(self) -> dict:
        return {
            "lease_id": self.session.lease.lease_id,
            "expires_at_utc": self.session.lease.expires_at_utc,
            "runtime_status": self.session.guard.status,
            "candidate_branch": self.candidate_branch,
            "automatic_renewal": False,
            "automatic_candidate_promotion": False,
            "automatic_verified_promotion": False,
        }
