import json
import os
import tempfile
import unittest
import sys
from pathlib import Path
from unittest import mock

from minhtri.candidate_lifecycle import (
    CRITIC_MATERIAL_DEFECT,
    CRITIC_NO_MATERIAL_DEFECT,
    CandidateLifecycleRunner,
    CodexReadOnlyCritic,
    CodexSandboxTestRunner,
)
from minhtri.self_upgrade_runtime import SelfUpgradeSession
from minhtri.upgrade_lease import issue_upgrade_lease
from tests.support import TEST_OWNER, TEST_SECRET, owner_config, write_owner_config


class FakeTest:
    def __init__(self, status="PASS", mutate=None):
        self.status = status
        self.mutate = mutate

    def run(self):
        if self.mutate:
            self.mutate()
        return {"status": self.status, "returncode": 0 if self.status == "PASS" else 1}


class FakeCritic:
    def __init__(self, verdict=CRITIC_NO_MATERIAL_DEFECT, mutate=None):
        self.verdict = verdict
        self.mutate = mutate

    def review(self, **kwargs):
        if self.mutate:
            self.mutate()
        return {
            "status": "RECORDED",
            "verdict": self.verdict,
            "independence_status": "SAME_PROVIDER_NOT_INDEPENDENT",
        }


class CandidateLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.config = write_owner_config(root)
        self.work = root / "candidate"
        (self.work / "src" / "minhtri").mkdir(parents=True)
        self.target = self.work / "src" / "minhtri" / "autonomy.py"
        self.target.write_text("x = 1\n", encoding="utf-8")
        self.receipt = root / "freeze.json"
        with owner_config(self.config):
            lease = issue_upgrade_lease(
                actor=TEST_OWNER,
                secret=TEST_SECRET,
                duration_seconds=60,
                parent_generation="GEN-1",
                target_generation="GEN-2",
            )
        self.session = SelfUpgradeSession(lease)

    def runner(self, test_runner=None, critic=None):
        runner = CandidateLifecycleRunner(
            session=self.session,
            candidate_root=self.work,
            candidate_branch="candidate/GEN-2",
            test_runner=test_runner or FakeTest(),
            critic=critic or FakeCritic(),
            freeze_receipt_path=self.receipt,
        )
        runner._current_branch = lambda: "candidate/GEN-2"
        return runner

    def test_test_failure_rejects_without_freeze(self):
        result = self.runner(test_runner=FakeTest("FAIL")).run(["src/minhtri/autonomy.py"])
        self.assertEqual(result["status"], "REJECTED_TEST")
        self.assertFalse(result["eligible_for_freeze"])
        self.assertFalse(self.receipt.exists())
        self.assertEqual(self.session.guard.status, "ACTIVE")

    def test_test_mutating_candidate_is_blocked(self):
        result = self.runner(
            test_runner=FakeTest(mutate=lambda: self.target.write_text("x = 2\n", encoding="utf-8"))
        ).run(["src/minhtri/autonomy.py"])
        self.assertEqual(result["status"], "BLOCKED_TEST_MUTATED_CANDIDATE")
        self.assertFalse(self.receipt.exists())

    def test_material_critic_rejects_without_freeze(self):
        result = self.runner(
            critic=FakeCritic(CRITIC_MATERIAL_DEFECT)
        ).run(["src/minhtri/autonomy.py"])
        self.assertEqual(result["status"], "REJECTED_CRITIC")
        self.assertFalse(result["eligible_for_freeze"])
        self.assertFalse(self.receipt.exists())

    def test_pass_writes_digest_bound_receipt_and_freezes(self):
        result = self.runner().run(["src/minhtri/autonomy.py"])
        self.assertEqual(result["status"], "FROZEN_PENDING_OWNER")
        self.assertEqual(result["runtime_status"], "FROZEN")
        self.assertTrue(self.receipt.is_file())
        data = json.loads(self.receipt.read_text(encoding="utf-8"))
        self.assertEqual(data["status"], "FROZEN_PENDING_OWNER")
        self.assertFalse(data["critic_independence_proven"])
        self.assertFalse(data["automatic_candidate_promotion"])
        self.assertFalse(data["automatic_verified_promotion"])

    def test_sandbox_test_runner_disables_network(self):
        runner = CodexSandboxTestRunner(self.work)
        proc = mock.Mock(returncode=0, stdout="ok", stderr="")
        with mock.patch("minhtri.candidate_lifecycle.shutil.which", return_value="codex.cmd"), \
             mock.patch("minhtri.candidate_lifecycle.subprocess.run", return_value=proc) as run:
            result = runner.run()
        cmd = run.call_args.args[0]
        env = run.call_args.kwargs["env"]
        self.assertIn("sandbox", cmd)
        self.assertIn("--permission-profile", cmd)
        self.assertIn(":workspace", cmd)
        self.assertIn("--sandbox-state-disable-network", cmd)
        self.assertEqual(cmd[cmd.index("-C") + 2], sys.executable)
        self.assertEqual(env["PYTHONPATH"].split(os.pathsep)[0], str((self.work / "src").resolve()))
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(result["network_disabled"])

    def test_codex_critic_is_read_only_and_not_independent(self):
        critic = CodexReadOnlyCritic(self.work)
        payload = json.dumps({
            "verdict": CRITIC_NO_MATERIAL_DEFECT,
            "findings": [],
            "reason": "bounded",
        })
        proc = mock.Mock(returncode=0, stdout=payload, stderr="")
        with mock.patch("minhtri.candidate_lifecycle.shutil.which", return_value="codex.cmd"), \
             mock.patch("minhtri.candidate_lifecycle.subprocess.run", return_value=proc) as run:
            result = critic.review(
                changed_paths=["src/minhtri/autonomy.py"],
                artifact_digest="a" * 64,
                test_receipt={"status": "PASS"},
            )
        cmd = run.call_args.args[0]
        self.assertIn("read-only", cmd)
        self.assertEqual(result["verdict"], CRITIC_NO_MATERIAL_DEFECT)
        self.assertEqual(result["independence_status"], "SAME_PROVIDER_NOT_INDEPENDENT")


if __name__ == "__main__":
    unittest.main()
