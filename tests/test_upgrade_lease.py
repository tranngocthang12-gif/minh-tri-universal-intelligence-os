import dataclasses
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from minhtri.upgrade_lease import (
    LeaseClockError,
    LeaseExpiredError,
    LeaseRevokedError,
    LeaseRuntimeGuard,
    LeaseScopeError,
    MAX_UPGRADE_LEASE_SECONDS,
    guarded_mutation,
    issue_upgrade_lease,
)
from tests.support import TEST_OWNER, TEST_SECRET, owner_config, write_owner_config


NOW = datetime(2026, 10, 3, 0, 0, tzinfo=timezone.utc)


class UpgradeLeaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.config = write_owner_config(Path(self.tmp.name))

    def issue(self, seconds=60):
        kwargs = {}
        if seconds > 300:
            kwargs = {
                "owner_authorization_ref": "a" * 40,
                "owner_authorized_at_utc": NOW.isoformat(),
                "eval_packet_hash": "b" * 64,
                "champion_sha": "c" * 40,
                "eval_dataset_hash": "d" * 64,
                "eval_metric": "task_utility",
            }
        with owner_config(self.config):
            return issue_upgrade_lease(
                actor=TEST_OWNER,
                secret=TEST_SECRET,
                duration_seconds=seconds,
                parent_generation="GEN-0001",
                target_generation="GEN-0002",
                now=NOW,
                lease_id="upgrade-test",
                **kwargs,
            )

    def test_owner_gated_immutable_lease_max_24h(self):
        lease = self.issue(MAX_UPGRADE_LEASE_SECONDS)
        self.assertEqual(lease.duration_seconds, 86400)
        self.assertFalse(lease.to_dict()["automatic_renewal"])
        with self.assertRaises(dataclasses.FrozenInstanceError):
            lease.expires_at_utc = "2099-01-01T00:00:00Z"
        with owner_config(self.config), self.assertRaises(ValueError):
            issue_upgrade_lease(
                actor=TEST_OWNER,
                secret=TEST_SECRET,
                duration_seconds=MAX_UPGRADE_LEASE_SECONDS + 1,
                parent_generation="GEN-0001",
                target_generation="GEN-0002",
                now=NOW,
            )

    def test_live_lease_rejects_prearmed_or_unpinned_activation(self):
        with owner_config(self.config), self.assertRaises(ValueError):
            issue_upgrade_lease(
                actor=TEST_OWNER,
                secret=TEST_SECRET,
                duration_seconds=MAX_UPGRADE_LEASE_SECONDS,
                parent_generation="GEN-0001",
                target_generation="GEN-0002",
                now=NOW,
                owner_authorization_ref="a" * 40,
                owner_authorized_at_utc=(NOW - timedelta(minutes=10)).isoformat(),
                eval_packet_hash="b" * 64,
                champion_sha="c" * 40,
                eval_dataset_hash="d" * 64,
                eval_metric="task_utility",
            )
        with owner_config(self.config), self.assertRaises(ValueError):
            issue_upgrade_lease(
                actor=TEST_OWNER,
                secret=TEST_SECRET,
                duration_seconds=MAX_UPGRADE_LEASE_SECONDS,
                parent_generation="GEN-0001",
                target_generation="GEN-0002",
                now=NOW,
                owner_authorization_ref="a" * 40,
                owner_authorized_at_utc=NOW.isoformat(),
            )

    def test_live_lease_pins_owner_authorization_and_eval_packet(self):
        lease = self.issue(MAX_UPGRADE_LEASE_SECONDS)
        data = lease.to_dict()
        self.assertEqual(data["owner_authorization_ref"], "a" * 40)
        self.assertEqual(data["eval_packet_hash"], "b" * 64)
        self.assertEqual(data["champion_sha"], "c" * 40)
        self.assertEqual(data["eval_dataset_hash"], "d" * 64)
        self.assertEqual(data["eval_metric"], "task_utility")
        self.assertFalse(data["automatic_push"])
        self.assertFalse(data["automatic_merge"])
        self.assertFalse(data["canonical_write_capability"])

    def test_expiry_uses_wall_and_monotonic_limits(self):
        guard = LeaseRuntimeGuard(self.issue(60), monotonic_started=100.0)
        guard.check(now=NOW + timedelta(seconds=59), monotonic_now=159.0)
        with self.assertRaises(LeaseExpiredError):
            guard.check(now=NOW + timedelta(seconds=59, milliseconds=500), monotonic_now=160.0)
        self.assertEqual(guard.status, "EXPIRED")

    def test_wall_clock_rollback_fails_closed(self):
        guard = LeaseRuntimeGuard(self.issue(60), monotonic_started=10.0)
        guard.check(now=NOW + timedelta(seconds=20), monotonic_now=20.0)
        with self.assertRaises(LeaseClockError):
            guard.check(now=NOW + timedelta(seconds=19), monotonic_now=21.0)
        self.assertEqual(guard.status, "REVOKED")

    def test_child_capability_keeps_same_expiry_and_only_loses_scope(self):
        lease = self.issue(120)
        guard = LeaseRuntimeGuard(lease, monotonic_started=0.0)
        child = guard.derive_child(
            ["candidate:test", "research:read"],
            now=NOW + timedelta(seconds=1),
            monotonic_now=1.0,
        )
        self.assertEqual(child.lease_id, lease.lease_id)
        self.assertEqual(child.expires_at_utc, lease.expires_at_utc)
        self.assertFalse(child.to_dict()["may_extend_lease"])
        with self.assertRaises(LeaseScopeError):
            guard.derive_child(
                ["candidate:test", "admin:write"],
                now=NOW + timedelta(seconds=2),
                monotonic_now=2.0,
            )

    def test_owner_can_revoke_early_and_mutation_stops(self):
        guard = LeaseRuntimeGuard(self.issue(60))
        with owner_config(self.config):
            snapshot = guard.revoke(actor=TEST_OWNER, secret=TEST_SECRET, reason="owner stop")
        self.assertEqual(snapshot["runtime_status"], "REVOKED")
        with self.assertRaises(LeaseRevokedError):
            guard.before_mutation(now=NOW + timedelta(seconds=1))

    def test_expiry_is_checked_immediately_before_mutation(self):
        guard = LeaseRuntimeGuard(self.issue(10), monotonic_started=5.0)
        called = []
        with self.assertRaises(LeaseExpiredError):
            guarded_mutation(
                guard,
                lambda: called.append("MUTATED"),
                now=NOW + timedelta(seconds=10),
                monotonic_now=15.0,
            )
        self.assertEqual(called, [])


if __name__ == "__main__":
    unittest.main()
