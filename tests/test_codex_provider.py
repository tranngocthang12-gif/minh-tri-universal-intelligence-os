import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from minhtri.codex_provider import CodexCandidateProvider, CodexProviderError
from minhtri.self_upgrade_runtime import SelfUpgradeSession
from minhtri.upgrade_lease import issue_upgrade_lease
from tests.support import TEST_OWNER, TEST_SECRET, owner_config, write_owner_config


class CodexProviderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.config = write_owner_config(root)
        self.work = root / "candidate"
        self.work.mkdir()
        with owner_config(self.config):
            lease = issue_upgrade_lease(
                actor=TEST_OWNER,
                secret=TEST_SECRET,
                duration_seconds=60,
                parent_generation="GEN-1",
                target_generation="GEN-2",
            )
        self.session = SelfUpgradeSession(lease)

    def provider(self):
        return CodexCandidateProvider(
            session=self.session,
            candidate_branch="candidate/GEN-2",
            candidate_root=self.work,
        )

    def test_run_closes_stdin_for_true_noninteractive_exec(self):
        p = self.provider()
        completed = mock.Mock(returncode=0, stdout="{}", stderr="")
        with mock.patch("minhtri.codex_provider.shutil.which", return_value="codex.cmd"),              mock.patch("minhtri.codex_provider.subprocess.run", return_value=completed) as run:
            p._run(sandbox="read-only", prompt="x")
        self.assertIs(run.call_args.kwargs["stdin"], subprocess.DEVNULL)

    def test_plan_is_read_only_and_scope_validated(self):
        plan_json = json.dumps({
            "summary": "x",
            "hypothesis": "x",
            "changed_paths": ["src/minhtri/autonomy.py"],
            "tests": ["unit"],
        })
        proc = mock.Mock(returncode=0, stdout=plan_json, stderr="")
        p = self.provider()
        with mock.patch.object(p, "_run", return_value=proc):
            plan = p.plan({"write_capability": False})
        self.assertEqual(plan["changed_paths"], ["src/minhtri/autonomy.py"])

    def test_plan_cannot_target_protected_path(self):
        plan_json = json.dumps({
            "summary": "x",
            "hypothesis": "x",
            "changed_paths": ["src/minhtri/owner.py"],
            "tests": [],
        })
        p = self.provider()
        with mock.patch.object(p, "_run", return_value=mock.Mock(returncode=0, stdout=plan_json)):
            with self.assertRaises(Exception):
                p.plan({})

    def test_action_blocks_undeclared_actual_path(self):
        plan_json = json.dumps({
            "summary": "x",
            "hypothesis": "x",
            "changed_paths": ["src/minhtri/autonomy.py"],
            "tests": [],
        })
        p = self.provider()
        with mock.patch.object(p, "_run", side_effect=[
            mock.Mock(returncode=0, stdout=plan_json),
            mock.Mock(returncode=0, stdout="done"),
        ]), mock.patch.object(
            p, "_changed_paths", return_value=["src/minhtri/autonomy.py", "README.md"]
        ):
            proposal = p.propose({})
            result = proposal["action"]()
        self.assertEqual(result["status"], "BLOCKED_UNDECLARED_PATH")
        self.assertEqual(result["undeclared_paths"], ["README.md"])

    def test_action_never_claims_commit_merge_or_push(self):
        plan_json = json.dumps({
            "summary": "x",
            "hypothesis": "x",
            "changed_paths": ["src/minhtri/autonomy.py"],
            "tests": [],
        })
        p = self.provider()
        with mock.patch.object(p, "_run", side_effect=[
            mock.Mock(returncode=0, stdout=plan_json),
            mock.Mock(returncode=0, stdout="done"),
        ]), mock.patch.object(p, "_changed_paths", return_value=["src/minhtri/autonomy.py"]):
            proposal = p.propose({})
            result = proposal["action"]()
        self.assertEqual(result["status"], "CANDIDATE_WORKTREE_MUTATED_PENDING_TEST")
        self.assertFalse(result["committed"])
        self.assertFalse(result["merged"])
        self.assertFalse(result["pushed"])


if __name__ == "__main__":
    unittest.main()
