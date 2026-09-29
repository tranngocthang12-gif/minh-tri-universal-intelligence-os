import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from minhtri.brain import BRAIN_ARTIFACTS
from minhtri.core import GateError, Ledger
from minhtri.tasking import TaskService, continuation_fingerprint, initial_task_state, task_evolve


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

    def ack(self, worker, ack_id=None):
        packet = self.service.packet("task1")
        ack_id = ack_id or f"continue-{worker}-{packet['task']['checkpoint_seq']}-{len(packet['task']['handoffs'])}"
        self.service.apply(command(
            "acknowledge_continuation",
            id=ack_id,
            task_id="task1",
            worker_id=worker,
            continuation_fingerprint=packet["continuation"]["fingerprint"],
        ))
        return ack_id

    def test_task_state_belongs_to_system_not_worker(self):
        self.create()
        expires = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        self.service.apply(command(
            "acquire_lease", task_id="task1", worker_id="worker-a", lease_id="lease-a",
            expires_at=expires, expected_checkpoint_seq=0, continuation_ack_id=self.ack("worker-a"),
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
            expires_at=expires, expected_checkpoint_seq=1, continuation_ack_id=self.ack("worker-b"),
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
            expires_at=expires, expected_checkpoint_seq=0, continuation_ack_id=self.ack("worker-a"),
        ))
        with self.assertRaisesRegex(GateError, "active lease"):
            self.service.apply(command(
                "acquire_lease", task_id="task1", worker_id="worker-b", lease_id="lease-b",
                expires_at=expires, expected_checkpoint_seq=0, continuation_ack_id=self.ack("worker-b"),
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
        fp0 = continuation_fingerprint(state["tasks"]["task1"])
        state = task_evolve(state, command(
            "acknowledge_continuation", id="ack-a", task_id="task1", worker_id="worker-a",
            continuation_fingerprint=fp0,
        ), "2026-09-29T10:05:00+00:00")
        state = task_evolve(state, command(
            "acquire_lease", task_id="task1", worker_id="worker-a", lease_id="lease-a",
            expires_at="2026-09-29T10:15:00+00:00", expected_checkpoint_seq=0,
            continuation_ack_id="ack-a",
        ), at1)
        state = task_evolve(state, command(
            "checkpoint_task", task_id="task1", worker_id="worker-a", lease_id="lease-a",
            expected_checkpoint_seq=0, summary="Checkpoint one", artifact_refs=[],
            evidence_ids=[], next_action="Continue",
        ), "2026-09-29T10:12:00+00:00")
        fp1 = continuation_fingerprint(state["tasks"]["task1"])
        state = task_evolve(state, command(
            "acknowledge_continuation", id="ack-b", task_id="task1", worker_id="worker-b",
            continuation_fingerprint=fp1,
        ), "2026-09-29T10:19:00+00:00")
        state = task_evolve(state, command(
            "acquire_lease", task_id="task1", worker_id="worker-b", lease_id="lease-b",
            expires_at="2026-09-29T11:00:00+00:00", expected_checkpoint_seq=1,
            continuation_ack_id="ack-b",
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
            expires_at=expires, expected_checkpoint_seq=0, continuation_ack_id=self.ack("worker-a"),
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
            expires_at=expires, expected_checkpoint_seq=0, continuation_ack_id=self.ack("worker-a"),
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
                decisions=[], unknowns=[], blockers=[], verification=[], scope="Wrong worker attempt",
                limitations=["Expected to fail before completion."],
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
            expires_at=expires, expected_checkpoint_seq=0, continuation_ack_id=self.ack("worker-a"),
        ))
        state = self.service.apply(command(
            "complete_task", task_id="task1", worker_id="worker-a", lease_id="lease-a",
            expected_checkpoint_seq=0, completion_summary="Accepted bounded result",
            decisions=["Bounded unit accepted."], unknowns=[], blockers=[],
            verification=["Structural task tests passed."], scope="Task fixture",
            limitations=["No real-world effectiveness claim."],
        ))["state"]
        self.assertEqual(state["tasks"]["task1"]["status"], "COMPLETED")
        receipt = state["tasks"]["task1"]["completion_receipt"]
        self.assertEqual(receipt["completion_summary"], "Accepted bounded result")
        self.assertEqual(len(receipt["fingerprint"]), 64)
        packet = self.service.packet("task1")
        self.assertEqual(packet["continuation"]["completion_receipt"]["fingerprint"], receipt["fingerprint"])
        self.assertFalse(packet["continuation"]["acknowledgement_required"])
        with self.assertRaisesRegex(GateError, "terminal"):
            self.service.apply(command(
                "acquire_lease", task_id="task1", worker_id="worker-b", lease_id="lease-b",
                expires_at=expires, expected_checkpoint_seq=0, continuation_ack_id=self.ack("worker-b"),
            ))

    def test_worker_must_ack_current_continuation_before_lease(self):
        self.create()
        expires = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        with self.assertRaisesRegex(GateError, "continuation acknowledgement"):
            self.service.apply(command(
                "acquire_lease", task_id="task1", worker_id="worker-a", lease_id="lease-a",
                expires_at=expires, expected_checkpoint_seq=0, continuation_ack_id="missing",
            ))

        stale_packet = self.service.packet("task1")
        stale_fp = stale_packet["continuation"]["fingerprint"]
        ack_id = self.ack("worker-a")
        self.service.apply(command(
            "acquire_lease", task_id="task1", worker_id="worker-a", lease_id="lease-a",
            expires_at=expires, expected_checkpoint_seq=0, continuation_ack_id=ack_id,
        ))
        self.service.apply(command(
            "checkpoint_task", task_id="task1", worker_id="worker-a", lease_id="lease-a",
            expected_checkpoint_seq=0, summary="Changed checkpoint", artifact_refs=[],
            evidence_ids=[], next_action="Continue",
        ))
        self.assertNotEqual(stale_fp, self.service.packet("task1")["continuation"]["fingerprint"])

    def test_explicit_handoff_preserves_decisions_unknowns_and_requires_successor_ack(self):
        self.create()
        expires = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        ack_a = self.ack("worker-a")
        self.service.apply(command(
            "acquire_lease", task_id="task1", worker_id="worker-a", lease_id="lease-a",
            expires_at=expires, expected_checkpoint_seq=0, continuation_ack_id=ack_a,
        ))
        self.service.apply(command(
            "checkpoint_task", task_id="task1", worker_id="worker-a", lease_id="lease-a",
            expected_checkpoint_seq=0, summary="Implemented bounded unit",
            artifact_refs=["artifact://r45"], evidence_ids=[], next_action="Run semantic review",
        ))
        state = self.service.apply(command(
            "handoff_task", task_id="task1", worker_id="worker-a", lease_id="lease-a",
            expected_checkpoint_seq=1,
            decisions=["Four workcell slots are stable; occupants are replaceable."],
            unknowns=["Provider identity is still self-declared."],
            blockers=["Independent provider review not yet collected."],
            verification=["Unit tests must pass on Python 3.10 and 3.12."],
            scope="R4.5 architecture continuity only",
            limitations=["No external provider connection or real-world effectiveness proof."],
        ))["state"]
        handoff = state["tasks"]["task1"]["handoffs"][-1]
        self.assertEqual(handoff["next_action"], "Run semantic review")
        self.assertEqual(len(handoff["fingerprint"]), 64)
        packet = self.service.packet("task1")
        self.assertEqual(packet["continuation"]["latest_handoff"]["fingerprint"], handoff["fingerprint"])
        with self.assertRaisesRegex(GateError, "continuation acknowledgement"):
            self.service.apply(command(
                "acquire_lease", task_id="task1", worker_id="worker-b", lease_id="lease-b",
                expires_at=expires, expected_checkpoint_seq=1, continuation_ack_id="missing",
            ))
        ack_b = self.ack("worker-b")
        state = self.service.apply(command(
            "acquire_lease", task_id="task1", worker_id="worker-b", lease_id="lease-b",
            expires_at=expires, expected_checkpoint_seq=1, continuation_ack_id=ack_b,
        ))["state"]
        self.assertEqual(state["tasks"]["task1"]["lease"]["worker_id"], "worker-b")

    def test_old_continuation_ack_cannot_be_reused_after_checkpoint_changes(self):
        self.create()
        expires = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        ack_a = self.ack("worker-a", "ack-a")
        self.service.apply(command(
            "acquire_lease", task_id="task1", worker_id="worker-a", lease_id="lease-a",
            expires_at=expires, expected_checkpoint_seq=0, continuation_ack_id=ack_a,
        ))
        self.service.apply(command(
            "checkpoint_task", task_id="task1", worker_id="worker-a", lease_id="lease-a",
            expected_checkpoint_seq=0, summary="One", artifact_refs=[], evidence_ids=[],
            next_action="Two",
        ))
        self.service.apply(command(
            "release_lease", task_id="task1", worker_id="worker-a", lease_id="lease-a", reason="handoff",
        ))
        with self.assertRaisesRegex(GateError, "stale"):
            self.service.apply(command(
                "acquire_lease", task_id="task1", worker_id="worker-a", lease_id="lease-b",
                expires_at=expires, expected_checkpoint_seq=1, continuation_ack_id="ack-a",
            ))


if __name__ == "__main__":
    unittest.main()
