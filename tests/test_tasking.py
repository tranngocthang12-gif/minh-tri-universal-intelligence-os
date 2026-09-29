import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from minhtri.brain import BRAIN_ARTIFACTS
from minhtri.core import GateError, Ledger
from minhtri.tasking import TaskService, initial_task_state, task_evolve


def command(command_type, **data):
    return {"type": command_type, "data": data}


class CanonicalTaskTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.brain_root = root / "repo"
        for index, relative in enumerate(BRAIN_ARTIFACTS, start=1):
            path = self.brain_root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            if relative == "PROJECT_LAW.md":
                text = "# PROJECT_LAW\n"
            elif relative == "BOOTSTRAP.md":
                text = "# BOOTSTRAP\n"
            elif relative == "AGENTS.md":
                text = "# AGENTS\n"
            else:
                text = f"artifact-{index}\n"
            path.write_text(text, encoding="utf-8")
        self.brain_revision = "a" * 40
        self.core = Ledger(root / "brain")
        self.core.init()
        self.core.apply(command(
            "register_domain", id="media", name="Media", risk_class="NORMAL",
            measurement_contract="Synthetic measurement",
        ))
        self.core.apply(command(
            "open_goal", id="goal1", domain_id="media", objective="Continue work across replaceable workers",
            priority=4, owner_boundary="Shadow only",
        ))
        self.service = TaskService(root / "brain", self.brain_root, self.brain_revision)
        self.service.init()

    def create(self):
        return self.service.apply(command(
            "create_task",
            id="task1",
            goal_id="goal1",
            brief="Produce a bounded analysis",
            acceptance="Checkpoint must survive worker change",
            allowed_evidence_ids=[],
        ))

    def test_task_state_belongs_to_system_not_worker(self):
        self.create()
        expires = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        self.service.apply(command(
            "acquire_lease", task_id="task1", worker_id="worker-a", lease_id="lease-a",
            expires_at=expires, expected_checkpoint_seq=0,
        ))
        self.service.apply(command(
            "checkpoint_task", task_id="task1", worker_id="worker-a", lease_id="lease-a",
            expected_checkpoint_seq=0, summary="Completed first unit", artifact_refs=["artifact://one"],
            evidence_ids=[], next_action="Continue second unit",
        ))
        self.service.apply(command(
            "release_lease", task_id="task1", worker_id="worker-a", lease_id="lease-a",
            reason="HANDOFF",
        ))
        state = self.service.apply(command(
            "acquire_lease", task_id="task1", worker_id="worker-b", lease_id="lease-b",
            expires_at=expires, expected_checkpoint_seq=1,
        ))["state"]
        task = state["tasks"]["task1"]
        self.assertEqual(task["checkpoint"]["seq"], 1)
        self.assertEqual(task["checkpoint"]["summary"], "Completed first unit")
        self.assertEqual(task["checkpoint"]["next_action"], "Continue second unit")
        self.assertEqual(task["lease"]["worker_id"], "worker-b")

    def test_active_lease_blocks_second_worker(self):
        self.create()
        expires = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        self.service.apply(command(
            "acquire_lease", task_id="task1", worker_id="worker-a", lease_id="lease-a",
            expires_at=expires, expected_checkpoint_seq=0,
        ))
        with self.assertRaisesRegex(GateError, "active lease"):
            self.service.apply(command(
                "acquire_lease", task_id="task1", worker_id="worker-b", lease_id="lease-b",
                expires_at=expires, expected_checkpoint_seq=0,
            ))

    def test_expired_lease_allows_failover_without_losing_checkpoint(self):
        at0 = "2026-09-29T10:00:00+00:00"
        at1 = "2026-09-29T10:10:00+00:00"
        at2 = "2026-09-29T10:20:00+00:00"
        state = initial_task_state()
        state = task_evolve(state, command(
            "create_task", id="task1", goal_id="goal1", domain_id="media",
            brain_revision="a" * 40, brain_fingerprint="b" * 64,
            architecture_law_sha256="c" * 64, bootstrap_sha256="d" * 64,
            core_state_head_at_open="e" * 64, brief="Task", acceptance="Done",
            allowed_evidence_ids=[], risk_class="NORMAL",
        ), at0)
        state = task_evolve(state, command(
            "acquire_lease", task_id="task1", worker_id="worker-a", lease_id="lease-a",
            expires_at="2026-09-29T10:15:00+00:00", expected_checkpoint_seq=0,
        ), at1)
        state = task_evolve(state, command(
            "checkpoint_task", task_id="task1", worker_id="worker-a", lease_id="lease-a",
            expected_checkpoint_seq=0, summary="Checkpoint one", artifact_refs=[],
            evidence_ids=[], next_action="Continue",
        ), "2026-09-29T10:12:00+00:00")
        state = task_evolve(state, command(
            "acquire_lease", task_id="task1", worker_id="worker-b", lease_id="lease-b",
            expires_at="2026-09-29T11:00:00+00:00", expected_checkpoint_seq=1,
        ), at2)
        task = state["tasks"]["task1"]
        self.assertEqual(task["lease"]["worker_id"], "worker-b")
        self.assertEqual(task["checkpoint"]["summary"], "Checkpoint one")
        self.assertEqual(task["handoffs"][-1]["reason"], "LEASE_EXPIRED")
        self.assertEqual(task["handoffs"][-1]["from_worker"], "worker-a")
        self.assertEqual(task["handoffs"][-1]["to_worker"], "worker-b")

    def test_stale_checkpoint_write_is_blocked(self):
        self.create()
        expires = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        self.service.apply(command(
            "acquire_lease", task_id="task1", worker_id="worker-a", lease_id="lease-a",
            expires_at=expires, expected_checkpoint_seq=0,
        ))
        self.service.apply(command(
            "checkpoint_task", task_id="task1", worker_id="worker-a", lease_id="lease-a",
            expected_checkpoint_seq=0, summary="First", artifact_refs=[], evidence_ids=[],
            next_action="Second",
        ))
        with self.assertRaisesRegex(GateError, "sequence mismatch"):
            self.service.apply(command(
                "checkpoint_task", task_id="task1", worker_id="worker-a", lease_id="lease-a",
                expected_checkpoint_seq=0, summary="Stale overwrite", artifact_refs=[],
                evidence_ids=[], next_action="Wrong",
            ))

    def test_wrong_worker_cannot_checkpoint_or_complete(self):
        self.create()
        expires = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        self.service.apply(command(
            "acquire_lease", task_id="task1", worker_id="worker-a", lease_id="lease-a",
            expires_at=expires, expected_checkpoint_seq=0,
        ))
        with self.assertRaisesRegex(GateError, "does not hold"):
            self.service.apply(command(
                "checkpoint_task", task_id="task1", worker_id="worker-b", lease_id="lease-a",
                expected_checkpoint_seq=0, summary="Hijack", artifact_refs=[],
                evidence_ids=[], next_action="No",
            ))
        with self.assertRaisesRegex(GateError, "does not hold"):
            self.service.apply(command(
                "complete_task", task_id="task1", worker_id="worker-b", lease_id="lease-a",
                expected_checkpoint_seq=0, completion_summary="No",
            ))

    def test_goal_closure_and_brain_drift_block_continuation(self):
        self.create()
        self.core.apply(command("set_goal_status", goal_id="goal1", status="BLOCKED", reason="Owner stopped"))
        expires = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        with self.assertRaisesRegex(GateError, "goal is blocked"):
            self.service.apply(command(
                "acquire_lease", task_id="task1", worker_id="worker-a", lease_id="lease-a",
                expires_at=expires, expected_checkpoint_seq=0,
            ))

        # Re-open only for the brain-drift branch of the test.
        self.core.apply(command("set_goal_status", goal_id="goal1", status="OPEN", reason="Resume"))
        (self.brain_root / "docs" / "ROADMAP.md").write_text("changed\n", encoding="utf-8")
        with self.assertRaisesRegex(GateError, "brain version is stale"):
            self.service.apply(command(
                "acquire_lease", task_id="task1", worker_id="worker-a", lease_id="lease-a",
                expires_at=expires, expected_checkpoint_seq=0,
            ))

    def test_complete_task_is_terminal(self):
        self.create()
        expires = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        self.service.apply(command(
            "acquire_lease", task_id="task1", worker_id="worker-a", lease_id="lease-a",
            expires_at=expires, expected_checkpoint_seq=0,
        ))
        state = self.service.apply(command(
            "complete_task", task_id="task1", worker_id="worker-a", lease_id="lease-a",
            expected_checkpoint_seq=0, completion_summary="Accepted bounded result",
        ))["state"]
        self.assertEqual(state["tasks"]["task1"]["status"], "COMPLETED")
        with self.assertRaisesRegex(GateError, "terminal"):
            self.service.apply(command(
                "acquire_lease", task_id="task1", worker_id="worker-b", lease_id="lease-b",
                expires_at=expires, expected_checkpoint_seq=0,
            ))


if __name__ == "__main__":
    unittest.main()
