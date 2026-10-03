import tempfile
import unittest
from pathlib import Path

from minhtri.lease_bound_worker import LeaseBoundSelfUpgradeWorker
from minhtri.self_upgrade_runtime import SelfUpgradeSession
from minhtri.upgrade_lease import issue_upgrade_lease
from tests.support import TEST_OWNER, TEST_SECRET, owner_config, write_owner_config


def state():
    return {"learning_focuses": {}}


class Provider:
    def __init__(self, marker):
        self.marker = marker

    def propose(self, packet):
        return {
            "changed_paths": ["src/minhtri/__init__.py"],
            "action": lambda: self.marker.append("mutated") or {"ok": True},
        }


class LeaseBoundWorkerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.config = write_owner_config(Path(self.tmp.name))

    def session(self):
        with owner_config(self.config):
            lease = issue_upgrade_lease(
                actor=TEST_OWNER,
                secret=TEST_SECRET,
                duration_seconds=60,
                parent_generation="GEN-1",
                target_generation="GEN-2",
            )
        return SelfUpgradeSession(lease)

    def test_no_provider_fails_closed_without_mutation(self):
        worker = LeaseBoundSelfUpgradeWorker(
            session=self.session(),
            state_loader=state,
            candidate_branch="candidate/GEN-2",
        )
        result = worker.tick()
        self.assertEqual(result["status"], "BLOCKED_NO_PROVIDER")
        self.assertFalse(result["candidate_mutation_performed"])
        self.assertFalse(result["canonical_write_capability"])

    def test_provider_mutation_passes_candidate_executor(self):
        marker = []
        worker = LeaseBoundSelfUpgradeWorker(
            session=self.session(),
            state_loader=state,
            candidate_branch="candidate/GEN-2",
            provider=Provider(marker),
        )
        result = worker.tick()
        self.assertEqual(result["status"], "CANDIDATE_MUTATION_COMPLETED")
        self.assertEqual(marker, ["mutated"])
        self.assertTrue(result["candidate_mutation_performed"])
        self.assertFalse(result["automatic_candidate_promotion"])

    def test_blocked_provider_result_is_rejected_not_completed(self):
        class Blocked:
            def propose(self, packet):
                return {
                    "changed_paths": ["src/minhtri/__init__.py"],
                    "action": lambda: {
                        "status": "BLOCKED_UNDECLARED_PATH",
                        "actual_paths": ["src/minhtri/__init__.py", "README.md"],
                    },
                }
        worker = LeaseBoundSelfUpgradeWorker(
            session=self.session(),
            state_loader=state,
            candidate_branch="candidate/GEN-2",
            provider=Blocked(),
        )
        result = worker.tick()
        self.assertEqual(result["status"], "CANDIDATE_REJECTED_PROVIDER_BLOCK")
        self.assertFalse(result["eligible_for_candidate"])
        self.assertTrue(result["candidate_mutation_performed"])

    def test_provider_cannot_mutate_protected_path(self):
        class Bad:
            def propose(self, packet):
                return {
                    "changed_paths": ["src/minhtri/owner.py"],
                    "action": lambda: None,
                }
        worker = LeaseBoundSelfUpgradeWorker(
            session=self.session(),
            state_loader=state,
            candidate_branch="candidate/GEN-2",
            provider=Bad(),
        )
        with self.assertRaises(Exception):
            worker.tick()


if __name__ == "__main__":
    unittest.main()
