"""Real-clock short lease proof for CI.

This intentionally waits at least 60 seconds and proves the runtime guard blocks a
mutation after actual elapsed wall/monotonic time. It does not prove Owner-PC execution
or OS sandbox containment.
"""
from datetime import datetime, timedelta, timezone
import time

from minhtri.upgrade_lease import LeaseExpiredError, LeaseRuntimeGuard, UpgradeLease, guarded_mutation


def main():
    start_wall = datetime.now(timezone.utc)
    duration = 60
    lease = UpgradeLease(
        lease_id="ci-realtime-60s",
        issued_at_utc=start_wall.isoformat().replace("+00:00", "Z"),
        expires_at_utc=(start_wall + timedelta(seconds=duration)).isoformat().replace("+00:00", "Z"),
        owner_id="ci-proof-owner",
        scope=("candidate:write",),
        target_generation="GEN-CI-PROOF",
        parent_generation="GEN-CURRENT",
        max_duration_seconds=duration,
    )
    guard = LeaseRuntimeGuard(lease, monotonic_started=time.monotonic())
    marker = []
    guarded_mutation(guard, lambda: marker.append("before"))
    mono0 = time.monotonic()
    time.sleep(duration + 0.25)
    blocked = False
    try:
        guarded_mutation(guard, lambda: marker.append("after"))
    except LeaseExpiredError:
        blocked = True
    elapsed = time.monotonic() - mono0
    if marker != ["before"] or not blocked or elapsed < duration:
        raise SystemExit("REALTIME_SHORT_LEASE_PROOF_FAILED")
    print({
        "status": "PASS_REALTIME_SHORT_LEASE_EXPIRY",
        "duration_seconds": duration,
        "observed_elapsed_seconds": elapsed,
        "post_expiry_mutation_blocked": blocked,
        "owner_pc_proven": False,
        "os_sandbox_containment_proven": False,
    })


if __name__ == "__main__":
    main()
