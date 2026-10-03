import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from minhtri.generation import (
    CandidateSandboxError,
    GEN_CANDIDATE,
    GEN_FROZEN_PENDING_OWNER,
    GEN_PROMOTED_BY_OWNER,
    create_generation_manifest,
    freeze_generation,
    owner_promote_generation,
    transition_generation,
)
from minhtri.upgrade_lease import LeaseExpiredError, LeaseRuntimeGuard, issue_upgrade_lease
from tests.support import TEST_OWNER, TEST_SECRET, owner_config, write_owner_config


NOW = datetime(2026, 10, 3, 1, 0, tzinfo=timezone.utc)


class GenerationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.config = write_owner_config(Path(self.tmp.name))
        with owner_config(self.config):
            lease = issue_upgrade_lease(
                actor=TEST_OWNER,
                secret=TEST_SECRET,
                duration_seconds=300,
                parent_generation="GEN-0001",
                target_generation="GEN-0002",
                now=NOW,
                lease_id="upgrade-generation-test",
            )
        self.guard = LeaseRuntimeGuard(lease, monotonic_started=100.0)

    def manifest(self, paths=("src/minhtri/autonomy.py",), branch="candidate/GEN-0002"):
        return create_generation_manifest(
            self.guard,
            generation_id="GEN-0002",
            parent_generation_id="GEN-0001",
            candidate_commit_sha="a" * 40,
            candidate_branch=branch,
            mutation_summary="Improve bounded learning planner",
            hypothesis="Planner change improves task utility without weakening gates",
            expected_improvement="Higher benchmark utility",
            known_risks=["planner regression"],
            files_changed=paths,
            test_plan="Run unit and security tests",
            benchmark_plan="Frozen parent/candidate benchmark",
            now=NOW + timedelta(seconds=10),
            monotonic_now=110.0,
        )

    def test_candidate_branch_allows_non_authority_code(self):
        manifest = self.manifest()
        self.assertEqual(manifest.status, "DRAFT")
        self.assertEqual(manifest.created_under_lease_id, "upgrade-generation-test")

    def test_main_and_authority_paths_are_denied(self):
        with self.assertRaises(CandidateSandboxError):
            self.manifest(branch="main")
        for path in (
            "src/minhtri/upgrade_lease.py",
            "src/minhtri/owner.py",
            "docs/PROJECT_STATE.json",
            "docs/LAW_INDEX_20261003.md",
            ".github/workflows/security.yml",
            "tests/test_upgrade_lease.py",
        ):
            with self.assertRaises(CandidateSandboxError, msg=path):
                self.manifest(paths=(path,))

    def test_expired_lease_blocks_candidate_creation(self):
        with self.assertRaises(LeaseExpiredError):
            create_generation_manifest(
                self.guard,
                generation_id="GEN-0002",
                parent_generation_id="GEN-0001",
                candidate_commit_sha="b" * 40,
                candidate_branch="candidate/GEN-0002",
                mutation_summary="x",
                hypothesis="x",
                expected_improvement="x",
                known_risks=["x"],
                files_changed=["src/minhtri/autonomy.py"],
                test_plan="x",
                benchmark_plan="x",
                now=NOW + timedelta(seconds=300),
                monotonic_now=400.0,
            )

    def test_freeze_then_owner_only_promotion_record(self):
        manifest = self.manifest()
        manifest = transition_generation(manifest, "READY_FOR_TEST")
        manifest = transition_generation(manifest, "TESTING")
        manifest = transition_generation(manifest, GEN_CANDIDATE)
        manifest = freeze_generation(manifest)
        self.assertEqual(manifest.status, GEN_FROZEN_PENDING_OWNER)
        with owner_config(self.config):
            promoted = owner_promote_generation(
                manifest,
                actor=TEST_OWNER,
                secret=TEST_SECRET,
            )
        self.assertEqual(promoted.status, GEN_PROMOTED_BY_OWNER)
        self.assertFalse(promoted.to_dict()["automatic_promotion"])


if __name__ == "__main__":
    unittest.main()
