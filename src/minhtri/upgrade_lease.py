"""Owner-gated, fail-closed 24-hour self-upgrade lease.

The lease grants bounded capability to build and test candidate generations. It does not
grant canonical write, automatic VERIFIED promotion, automatic trial activation, or
automatic Champion promotion.

Lease issuance and early revocation authenticate through the existing fixed Owner gate.
The immutable lease record has no renewal method. A new lease always requires a new
Owner authorization.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from time import monotonic
from typing import Callable, Iterable, TypeVar
from uuid import uuid4

MAX_UPGRADE_LEASE_SECONDS = 24 * 60 * 60
LEASE_ACTIVE = "ACTIVE"
LEASE_EXPIRED = "EXPIRED"
LEASE_REVOKED = "REVOKED"
LEASE_FROZEN = "FROZEN"

DEFAULT_UPGRADE_SCOPES = frozenset({
    "research:read",
    "candidate:write",
    "candidate:test",
    "critic:run",
    "benchmark:run",
})


class LeaseError(ValueError):
    pass


class LeaseExpiredError(LeaseError):
    pass


class LeaseRevokedError(LeaseError):
    pass


class LeaseScopeError(LeaseError):
    pass


class LeaseClockError(LeaseError):
    pass


def _utc(value: datetime) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None:
        raise LeaseError("timestamp must be timezone-aware")
    return value.astimezone(timezone.utc)


def _stamp(value: datetime) -> str:
    return _utc(value).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class UpgradeLease:
    lease_id: str
    issued_at_utc: str
    expires_at_utc: str
    owner_id: str
    scope: tuple[str, ...]
    target_generation: str
    parent_generation: str
    max_duration_seconds: int
    status: str = LEASE_ACTIVE

    def __post_init__(self) -> None:
        if not self.lease_id or not self.owner_id:
            raise LeaseError("lease_id and owner_id are required")
        if self.status != LEASE_ACTIVE:
            raise LeaseError("new immutable lease must start ACTIVE")
        if type(self.max_duration_seconds) is not int:
            raise LeaseError("max_duration_seconds must be an integer")
        if not (1 <= self.max_duration_seconds <= MAX_UPGRADE_LEASE_SECONDS):
            raise LeaseError("lease duration must be between 1 and 86400 seconds")
        issued = parse_utc(self.issued_at_utc)
        expires = parse_utc(self.expires_at_utc)
        actual = int((expires - issued).total_seconds())
        if actual != self.max_duration_seconds:
            raise LeaseError("expires_at must equal issued_at plus max_duration_seconds")
        if not self.scope or len(set(self.scope)) != len(self.scope):
            raise LeaseError("scope must be a nonempty unique capability list")
        unknown = set(self.scope) - DEFAULT_UPGRADE_SCOPES
        if unknown:
            raise LeaseError("unknown upgrade scope: " + ", ".join(sorted(unknown)))
        if not self.target_generation or not self.parent_generation:
            raise LeaseError("parent and target generations are required")

    @property
    def duration_seconds(self) -> int:
        return self.max_duration_seconds

    def to_dict(self) -> dict:
        return {
            "lease_id": self.lease_id,
            "issued_at_utc": self.issued_at_utc,
            "expires_at_utc": self.expires_at_utc,
            "owner_id": self.owner_id,
            "scope": list(self.scope),
            "target_generation": self.target_generation,
            "parent_generation": self.parent_generation,
            "max_duration_seconds": self.max_duration_seconds,
            "status": self.status,
            "automatic_renewal": False,
            "automatic_promotion": False,
        }


def parse_utc(value: str) -> datetime:
    if not isinstance(value, str):
        raise LeaseError("timestamp must be a string")
    text = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError as exc:
        raise LeaseError("invalid timestamp") from exc
    if parsed.tzinfo is None:
        raise LeaseError("timestamp must include timezone")
    return parsed.astimezone(timezone.utc)


def issue_upgrade_lease(
    *,
    actor: str | None,
    secret: str | None,
    duration_seconds: int,
    parent_generation: str,
    target_generation: str,
    scope: Iterable[str] = DEFAULT_UPGRADE_SCOPES,
    now: datetime | None = None,
    lease_id: str | None = None,
) -> UpgradeLease:
    """Issue one immutable lease after authenticating against the fixed Owner gate."""
    from .owner import config_path, require_owner

    if type(duration_seconds) is not int or not (1 <= duration_seconds <= MAX_UPGRADE_LEASE_SECONDS):
        raise LeaseError("duration_seconds must be an integer between 1 and 86400")
    owner_id = require_owner(actor, secret, config_path(None))
    issued = _utc(now or datetime.now(timezone.utc))
    expires = issued + timedelta(seconds=duration_seconds)
    normalized_scope = tuple(sorted(set(scope)))
    return UpgradeLease(
        lease_id=lease_id or f"upgrade-{uuid4().hex}",
        issued_at_utc=_stamp(issued),
        expires_at_utc=_stamp(expires),
        owner_id=owner_id,
        scope=normalized_scope,
        target_generation=target_generation,
        parent_generation=parent_generation,
        max_duration_seconds=duration_seconds,
    )


@dataclass(frozen=True)
class ChildCapability:
    lease_id: str
    expires_at_utc: str
    scope: tuple[str, ...]
    parent_generation: str
    target_generation: str

    def to_dict(self) -> dict:
        return {
            "lease_id": self.lease_id,
            "expires_at_utc": self.expires_at_utc,
            "scope": list(self.scope),
            "parent_generation": self.parent_generation,
            "target_generation": self.target_generation,
            "may_extend_lease": False,
        }


class LeaseRuntimeGuard:
    """Runtime capability guard.

    It combines the immutable UTC expiry with monotonic elapsed time for the current
    process. Any observed wall-clock rollback, monotonic rollback, expiry, revocation,
    or missing scope fails closed. A child capability can only inherit a subset of the
    same lease and exact expiry.
    """

    def __init__(
        self,
        lease: UpgradeLease,
        *,
        monotonic_started: float | None = None,
    ):
        self.lease = lease
        self._status = LEASE_ACTIVE
        self._reason: str | None = None
        self._issued = parse_utc(lease.issued_at_utc)
        self._expires = parse_utc(lease.expires_at_utc)
        self._last_wall = self._issued
        self._mono_started = monotonic_started
        self._last_mono = monotonic_started

    @property
    def status(self) -> str:
        return self._status

    @property
    def reason(self) -> str | None:
        return self._reason

    def _revoke_clock(self, reason: str) -> None:
        self._status = LEASE_REVOKED
        self._reason = reason
        raise LeaseClockError(reason)

    def check(
        self,
        *,
        scope: str | None = None,
        now: datetime | None = None,
        monotonic_now: float | None = None,
    ) -> None:
        if self._status == LEASE_EXPIRED:
            raise LeaseExpiredError(self._reason or "lease expired")
        if self._status in (LEASE_REVOKED, LEASE_FROZEN):
            raise LeaseRevokedError(self._reason or "lease is not active")

        wall = _utc(now or datetime.now(timezone.utc))
        if wall < self._issued:
            self._revoke_clock("wall clock is before lease issuance; fail closed")
        if wall < self._last_wall:
            self._revoke_clock("wall clock moved backward; fail closed")
        if wall >= self._expires:
            self._status = LEASE_EXPIRED
            self._reason = "UTC expiry reached"
            raise LeaseExpiredError(self._reason)

        if self._mono_started is not None:
            current = monotonic() if monotonic_now is None else monotonic_now
            if self._last_mono is not None and current < self._last_mono:
                self._revoke_clock("monotonic clock moved backward; fail closed")
            if current - self._mono_started >= self.lease.duration_seconds:
                self._status = LEASE_EXPIRED
                self._reason = "monotonic duration limit reached"
                raise LeaseExpiredError(self._reason)
            self._last_mono = current

        if scope is not None and scope not in self.lease.scope:
            raise LeaseScopeError(f"scope not granted by lease: {scope}")
        self._last_wall = wall

    def before_mutation(
        self,
        *,
        now: datetime | None = None,
        monotonic_now: float | None = None,
    ) -> None:
        self.check(scope="candidate:write", now=now, monotonic_now=monotonic_now)

    def derive_child(
        self,
        requested_scope: Iterable[str],
        *,
        now: datetime | None = None,
        monotonic_now: float | None = None,
    ) -> ChildCapability:
        self.check(now=now, monotonic_now=monotonic_now)
        requested = tuple(sorted(set(requested_scope)))
        if not requested or not set(requested).issubset(self.lease.scope):
            raise LeaseScopeError("child capability must be a nonempty subset of parent lease scope")
        return ChildCapability(
            lease_id=self.lease.lease_id,
            expires_at_utc=self.lease.expires_at_utc,
            scope=requested,
            parent_generation=self.lease.parent_generation,
            target_generation=self.lease.target_generation,
        )

    def revoke(
        self,
        *,
        actor: str | None,
        secret: str | None,
        reason: str,
    ) -> dict:
        from .owner import config_path, require_owner

        owner_id = require_owner(actor, secret, config_path(None))
        if owner_id != self.lease.owner_id:
            raise LeaseRevokedError("revoker does not match lease owner")
        if not isinstance(reason, str) or not reason.strip():
            raise LeaseError("revocation reason is required")
        self._status = LEASE_REVOKED
        self._reason = reason.strip()
        return self.snapshot()

    def freeze(self, reason: str) -> dict:
        if self._status == LEASE_ACTIVE:
            self._status = LEASE_FROZEN
            self._reason = reason
        return self.snapshot()

    def snapshot(self) -> dict:
        return {
            **self.lease.to_dict(),
            "runtime_status": self._status,
            "runtime_reason": self._reason,
        }


T = TypeVar("T")


def guarded_mutation(
    guard: LeaseRuntimeGuard,
    action: Callable[[], T],
    *,
    now: datetime | None = None,
    monotonic_now: float | None = None,
) -> T:
    """Check the lease immediately before one mutation callback."""
    guard.before_mutation(now=now, monotonic_now=monotonic_now)
    return action()
