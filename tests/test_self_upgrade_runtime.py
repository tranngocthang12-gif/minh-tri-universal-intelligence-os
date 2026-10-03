import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

from minhtri.self_upgrade_runtime import SelfUpgradeSession, run_short_runtime_proof
from minhtri.upgrade_lease import LeaseExpiredError, issue_upgrade_lease
from tests.support import TEST_OWNER, TEST_SECRET, owner_config, write_owner_config


class SelfUpgradeRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.config = write_owner_config(Path(self.tmp.name))

    def issue(self, seconds=60):
        with owner_config(self.config):
            return issue_upgrade_lease(
                actor=TEST_OWNER,
                secret=TEST_SECRET,
                duration_seconds=seconds,
                parent_generation="GEN-1",
                target_generation="GEN-2",
            )

    def test_session_has_no_renewal_and_child_cannot_expand_scope(self):
        session = SelfUpgradeSession(self.issue())
        child = session.derive_child(["candidate:test"])
        self.assertEqual(child["lease_id"], session.lease.lease_id)
        self.assertEqual(child["expires_at_utc"], session.lease.expires_at_utc)
        self.assertFalse(child["may_extend_lease"])

    def test_candidate_authorization_is_branch_and_path_guarded(self):
        session = SelfUpgradeSession(self.issue())
        allowed = session.authorize_candidate_mutation(
            candidate_branch="candidate/GEN-2",
            changed_paths=["src/minhtri/autonomy.py"],
        )
        self.assertEqual(allowed, ("src/minhtri/autonomy.py",))

    def test_short_runtime_proof_logic_with_virtual_sleep(self):
        clock = {"mono": 100.0}
        real_monotonic = __import__("time").monotonic

        def fake_sleep(seconds):
            clock["mono"] += seconds

        def fake_monotonic():
            return clock["mono"]

        with owner_config(self.config), \
             mock.patch("minhtri.self_upgrade_runtime.time.sleep", side_effect=fake_sleep), \
             mock.patch("minhtri.self_upgrade_runtime.time.monotonic", side_effect=fake_monotonic), \
             mock.patch("minhtri.upgrade_lease.monotonic", side_effect=fake_monotonic):
            result = run_short_runtime_proof(
                actor=TEST_OWNER,
                secret=TEST_SECRET,
                duration_seconds=60,
            )
        self.assertEqual(result["status"], "PASS_SHORT_RUNTIME_PROOF")
        self.assertTrue(result["post_expiry_mutation_blocked"])
        self.assertTrue(result["owner_revoke_mutation_blocked"])
        self.assertTrue(result["child_same_expiry"])
        self.assertEqual(result["candidate_execution_containment"], "NOT_PROVEN_OS_SANDBOX")


if __name__ == "__main__":
    unittest.main()
