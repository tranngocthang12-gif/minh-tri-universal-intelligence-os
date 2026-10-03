import tempfile
import unittest
from pathlib import Path

from minhtri.candidate_executor import CandidateExecutor
from minhtri.self_upgrade_runtime import SelfUpgradeSession
from minhtri.upgrade_lease import issue_upgrade_lease
from tests.support import TEST_OWNER, TEST_SECRET, owner_config, write_owner_config


class CandidateExecutorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.config = write_owner_config(Path(self.tmp.name))
        with owner_config(self.config):
            lease = issue_upgrade_lease(
                actor=TEST_OWNER,
                secret=TEST_SECRET,
                duration_seconds=60,
                parent_generation="GEN-1",
                target_generation="GEN-2",
            )
        self.executor = CandidateExecutor(SelfUpgradeSession(lease), "candidate/GEN-2")

    def test_allowed_mutation_executes(self):
        marker = []
        result = self.executor.mutate(
            ["src/minhtri/autonomy.py"],
            lambda: marker.append("ok") or "done",
        )
        self.assertEqual(result, "done")
        self.assertEqual(marker, ["ok"])

    def test_protected_path_is_blocked_before_action(self):
        marker = []
        with self.assertRaises(Exception):
            self.executor.mutate(
                ["src/minhtri/owner.py"],
                lambda: marker.append("bad"),
            )
        self.assertEqual(marker, [])

    def test_status_has_no_auto_promotion(self):
        status = self.executor.status()
        self.assertFalse(status["automatic_renewal"])
        self.assertFalse(status["automatic_candidate_promotion"])
        self.assertFalse(status["automatic_verified_promotion"])


if __name__ == "__main__":
    unittest.main()
