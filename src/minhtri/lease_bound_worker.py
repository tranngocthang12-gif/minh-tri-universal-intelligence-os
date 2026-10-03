"""Lease-bound self-upgrade worker.

The worker binds proposal-only learning to the candidate executor. A real provider must
be injected to propose a candidate mutation. Without a provider, the worker reports
BLOCKED_NO_PROVIDER and performs no mutation.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Protocol

from .autonomy import build_autonomy_packet
from .candidate_executor import CandidateExecutor
from .self_upgrade_runtime import SelfUpgradeSession


class CandidateProvider(Protocol):
    def propose(self, autonomy_packet: dict[str, Any]) -> dict[str, Any]:
        ...


@dataclass
class LeaseBoundSelfUpgradeWorker:
    session: SelfUpgradeSession
    state_loader: Callable[[], dict[str, Any]]
    candidate_branch: str
    provider: CandidateProvider | None = None
    critic_provider_id: str | None = None

    def tick(self) -> dict[str, Any]:
        self.session.check()
        packet = build_autonomy_packet(
            self.state_loader(),
            critic_provider_id=self.critic_provider_id,
        )
        base = {
            "lease_id": self.session.lease.lease_id,
            "expires_at_utc": self.session.lease.expires_at_utc,
            "autonomy_packet": packet,
            "automatic_renewal": False,
            "automatic_verified_promotion": False,
            "automatic_candidate_promotion": False,
            "canonical_write_capability": False,
        }
        if self.provider is None:
            return {
                **base,
                "status": "BLOCKED_NO_PROVIDER",
                "candidate_mutation_performed": False,
            }

        proposal = self.provider.propose(packet)
        if not isinstance(proposal, dict):
            raise ValueError("provider proposal must be a mapping")
        paths = proposal.get("changed_paths")
        action = proposal.get("action")
        if not isinstance(paths, list) or not paths:
            raise ValueError("provider proposal must declare changed_paths")
        if not callable(action):
            raise ValueError("provider proposal must provide callable action")

        executor = CandidateExecutor(self.session, self.candidate_branch)
        result = executor.mutate(paths, action)
        return {
            **base,
            "status": "CANDIDATE_MUTATION_COMPLETED",
            "candidate_mutation_performed": True,
            "changed_paths": list(executor.authorize(paths)),
            "provider_result": result,
        }
