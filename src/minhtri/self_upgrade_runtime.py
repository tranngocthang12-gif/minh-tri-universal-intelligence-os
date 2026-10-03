"""Live self-upgrade session controller and short-duration runtime proof.

The controller keeps the authoritative lease in process memory. A restart loses the lease
and therefore loses upgrade authority (fail closed). Audit output is evidence only and is
never an authority source.

This module does not provide an OS sandbox. It proves lease timing/revocation at the
controller boundary only. Candidate execution containment remains a separate gate.
"""
from __future__ import annotations

import argparse
import getpass
import json
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Iterable

from .generation import enforce_candidate_mutation
from .owner import ENV_SECRET, OwnerGateError
from .upgrade_lease import (
    DEFAULT_UPGRADE_SCOPES,
    LeaseClockError,
    LeaseExpiredError,
    LeaseRevokedError,
    LeaseRuntimeGuard,
    LeaseScopeError,
    UpgradeLease,
    guarded_mutation,
    issue_upgrade_lease,
)

SHORT_PROOF_MIN_SECONDS = 60
SHORT_PROOF_MAX_SECONDS = 300
RUNTIME_PROTOCOL = "minhtri-self-upgrade-runtime/v1"


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def stamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass
class SessionAudit:
    events: list[dict[str, Any]] = field(default_factory=list)

    def record(self, event: str, lease_id: str, **fields: Any) -> dict[str, Any]:
        row = {
            "event": event,
            "at_utc": stamp(utcnow()),
            "lease_id": lease_id,
            **fields,
        }
        self.events.append(row)
        return row


class SelfUpgradeSession:
    """One in-memory lease session with no renewal method."""

    def __init__(
        self,
        lease: UpgradeLease,
        *,
        monotonic_started: float | None = None,
        audit: SessionAudit | None = None,
    ):
        self.guard = LeaseRuntimeGuard(
            lease,
            monotonic_started=time.monotonic() if monotonic_started is None else monotonic_started,
        )
        self.audit = audit or SessionAudit()
        self.audit.record(
            "LEASE_ACTIVATED",
            lease.lease_id,
            expires_at_utc=lease.expires_at_utc,
            parent_generation=lease.parent_generation,
            target_generation=lease.target_generation,
        )

    @property
    def lease(self) -> UpgradeLease:
        return self.guard.lease

    def check(self, *, scope: str | None = None) -> None:
        try:
            self.guard.check(scope=scope)
        except LeaseExpiredError:
            self.audit.record("LEASE_EXPIRED", self.lease.lease_id)
            raise
        except (LeaseClockError, LeaseRevokedError) as exc:
            self.audit.record("RIGHTS_REVOKED", self.lease.lease_id, reason=str(exc))
            raise

    def derive_child(self, scope: Iterable[str]) -> dict[str, Any]:
        child = self.guard.derive_child(scope)
        self.audit.record(
            "CHILD_CAPABILITY_DERIVED",
            self.lease.lease_id,
            child_scope=list(child.scope),
            expires_at_utc=child.expires_at_utc,
        )
        return child.to_dict()

    def authorize_candidate_mutation(
        self,
        *,
        candidate_branch: str,
        changed_paths: Iterable[str],
    ) -> tuple[str, ...]:
        paths = enforce_candidate_mutation(
            self.guard,
            candidate_branch=candidate_branch,
            changed_paths=changed_paths,
        )
        self.audit.record(
            "CANDIDATE_MUTATION_AUTHORIZED",
            self.lease.lease_id,
            candidate_branch=candidate_branch,
            changed_paths=list(paths),
        )
        return paths

    def guarded_mutation(self, action: Callable[[], Any]) -> Any:
        try:
            result = guarded_mutation(self.guard, action)
        except LeaseExpiredError:
            self.audit.record("LEASE_EXPIRED", self.lease.lease_id)
            self.audit.record("RIGHTS_REVOKED", self.lease.lease_id, reason="expiry")
            raise
        except (LeaseClockError, LeaseRevokedError) as exc:
            self.audit.record("RIGHTS_REVOKED", self.lease.lease_id, reason=str(exc))
            raise
        self.audit.record("MUTATION_COMPLETED", self.lease.lease_id)
        return result

    def owner_revoke(self, *, actor: str, secret: str, reason: str) -> dict[str, Any]:
        snapshot = self.guard.revoke(actor=actor, secret=secret, reason=reason)
        self.audit.record("LEASE_REVOKED", self.lease.lease_id, reason=reason)
        self.audit.record("RIGHTS_REVOKED", self.lease.lease_id, reason=reason)
        return snapshot


def _secret_from_env_or_prompt() -> str:
    secret = os.environ.pop(ENV_SECRET, None)
    if secret:
        return secret
    secret = getpass.getpass("Owner secret (not shown): ")
    if not secret:
        raise ValueError("Owner secret is required")
    return secret


def run_short_runtime_proof(
    *,
    actor: str,
    secret: str,
    duration_seconds: int,
    parent_generation: str = "GEN-CURRENT",
    target_generation: str = "GEN-SHORT-PROOF",
) -> dict[str, Any]:
    """Run a real-clock expiry proof plus immediate Owner-revoke proof."""
    if type(duration_seconds) is not int or not (
        SHORT_PROOF_MIN_SECONDS <= duration_seconds <= SHORT_PROOF_MAX_SECONDS
    ):
        raise ValueError("short proof duration must be between 60 and 300 seconds")

    lease = issue_upgrade_lease(
        actor=actor,
        secret=secret,
        duration_seconds=duration_seconds,
        parent_generation=parent_generation,
        target_generation=target_generation,
        scope=DEFAULT_UPGRADE_SCOPES,
    )
    session = SelfUpgradeSession(lease)

    marker: list[str] = []
    session.guarded_mutation(lambda: marker.append("before-expiry"))
    child = session.derive_child(("candidate:test", "research:read"))

    started = time.monotonic()
    time.sleep(duration_seconds + 0.2)
    elapsed = time.monotonic() - started

    expired_blocked = False
    try:
        session.guarded_mutation(lambda: marker.append("after-expiry"))
    except LeaseExpiredError:
        expired_blocked = True

    if marker != ["before-expiry"] or not expired_blocked:
        raise RuntimeError("expiry proof failed: mutation was not blocked")

    revoke_lease = issue_upgrade_lease(
        actor=actor,
        secret=secret,
        duration_seconds=SHORT_PROOF_MIN_SECONDS,
        parent_generation=parent_generation,
        target_generation=target_generation + "-REVOKE",
        scope=DEFAULT_UPGRADE_SCOPES,
    )
    revoke_session = SelfUpgradeSession(revoke_lease)
    revoke_session.owner_revoke(actor=actor, secret=secret, reason="short-proof-owner-revoke")
    revoked_blocked = False
    try:
        revoke_session.guarded_mutation(lambda: marker.append("after-revoke"))
    except LeaseRevokedError:
        revoked_blocked = True

    if not revoked_blocked:
        raise RuntimeError("revocation proof failed: mutation was not blocked")

    return {
        "protocol": RUNTIME_PROTOCOL,
        "status": "PASS_SHORT_RUNTIME_PROOF",
        "lease_id": lease.lease_id,
        "issued_at_utc": lease.issued_at_utc,
        "expires_at_utc": lease.expires_at_utc,
        "requested_duration_seconds": duration_seconds,
        "observed_wait_seconds": elapsed,
        "pre_expiry_mutation_completed": True,
        "post_expiry_mutation_blocked": expired_blocked,
        "owner_revoke_mutation_blocked": revoked_blocked,
        "child_same_lease": child["lease_id"] == lease.lease_id,
        "child_same_expiry": child["expires_at_utc"] == lease.expires_at_utc,
        "automatic_renewal": False,
        "automatic_candidate_promotion": False,
        "controller_authority": "IN_MEMORY_FAIL_CLOSED_ON_PROCESS_EXIT",
        "candidate_execution_containment": "NOT_PROVEN_OS_SANDBOX",
        "audit": session.audit.events + revoke_session.audit.events,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="minhtri-self-upgrade",
        description="Owner-gated bounded self-upgrade runtime controller",
    )
    sub = parser.add_subparsers(dest="action", required=True)
    proof = sub.add_parser("short-proof", help="Run a 60-300 second real-clock lease proof")
    proof.add_argument("--duration", type=int, default=60)
    proof.add_argument("--owner-id", required=True)
    proof.add_argument("--parent-generation", default="GEN-CURRENT")
    proof.add_argument("--target-generation", default="GEN-SHORT-PROOF")
    args = parser.parse_args(argv)

    try:
        if args.action == "short-proof":
            secret = _secret_from_env_or_prompt()
            result = run_short_runtime_proof(
                actor=args.owner_id,
                secret=secret,
                duration_seconds=args.duration,
                parent_generation=args.parent_generation,
                target_generation=args.target_generation,
            )
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        raise ValueError("unsupported action")
    except OwnerGateError as exc:
        print(json.dumps({"status": "BLOCKED", "reason": exc.code, "detail": exc.detail}), flush=True)
        return 2
    except (ValueError, RuntimeError, LeaseExpiredError, LeaseRevokedError, LeaseClockError, LeaseScopeError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}), flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
