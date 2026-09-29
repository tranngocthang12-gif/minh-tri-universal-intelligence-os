import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from minhtri.arena import ArenaService
from minhtri.brain import BRAIN_ARTIFACTS
from minhtri.core import GateError, Ledger
from minhtri.workcell import ElasticWorkcellService


def command(command_type, **data):
    return {"type": command_type, "data": data}


class ElasticWorkcellTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.brain_root = root / "repo"
        for index, relative in enumerate(BRAIN_ARTIFACTS, start=1):
            path_obj = self.brain_root / relative
            path_obj.parent.mkdir(parents=True, exist_ok=True)
            if relative == "PROJECT_LAW.md":
                text_value = "# PROJECT_LAW\n"
            elif relative == "BOOTSTRAP.md":
                text_value = "# BOOTSTRAP\n"
            else:
                text_value = f"artifact-{index}\n"
            path_obj.write_text(text_value, encoding="utf-8")

        self.core = Ledger(root / "brain")
        self.core.init()
        self.core.apply(command(
            "register_domain", id="media", name="Media", risk_class="NORMAL",
            measurement_contract="Synthetic",
        ))
        self.core.apply(command(
            "open_goal", id="goal1", domain_id="media", objective="Elastic AI review",
            priority=4, owner_boundary="Shadow only",
        ))
        self.arena = ArenaService(root / "brain", self.brain_root, "a" * 40)
        self.arena.init()
        participants = [
            ("actor1", "family1", "model-1"),
            ("actor2", "family2", "model-2"),
            ("actor3", "family3", "model-3"),
            ("actor4", "family4", "model-4"),
            ("actor5", "family5", "model-5"),
            ("alias1", "family1", "alias-model"),
        ]
        for participant_id, family_id, model in participants:
            self.arena.apply(command(
                "register_participant", id=participant_id, family_id=family_id,
                model=model, version="test", adapter="MANUAL",
                capabilities=["PROPOSE", "CRITIQUE", "ADJUDICATE"],
            ))
        expiry = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
        task_state = self.arena.apply(command(
            "open_task", id="task1", goal_id="goal1", brief="Review architecture",
            acceptance="All assigned contributions before reveal", allowed_evidence_ids=[], expires_at=expiry,
        ))["state"]
        self.task = task_state["tasks"]["task1"]
        for index, (participant_id, _, _) in enumerate(participants, start=1):
            self.arena.apply(command(
                "acknowledge_brain", id=f"ack{index}", task_id="task1",
                participant_id=participant_id, task_fingerprint=self.task["fingerprint"],
                brain_revision=self.task["brain_revision"],
                brain_fingerprint=self.task["brain_fingerprint"],
                architecture_law_sha256=self.task["architecture_law_sha256"],
                bootstrap_sha256=self.task["bootstrap_sha256"],
            ))
        self.workcell = ElasticWorkcellService(root / "brain", self.brain_root, "a" * 40)
        self.workcell.init()
        self.workcell.apply(command("open_session", id="session1", arena_task_id="task1"))

    def assign(self, seat, actor):
        defaults = {
            "actor1": ("family1", "model-1"),
            "actor2": ("family2", "model-2"),
            "actor3": ("family3", "model-3"),
            "actor4": ("family4", "model-4"),
            "actor5": ("family5", "model-5"),
            "alias1": ("family1", "alias-model"),
        }
        family, model = defaults[actor]
        return self.workcell.apply(command(
            "assign_slot", session_id="session1", seat_id=seat, participant_id=actor,
            family_id=family, model=model, version="test",
        ))

    def submit(self, seat, actor, digit):
        return self.workcell.apply(command(
            "submit_blind", session_id="session1", seat_id=seat, participant_id=actor,
            contribution_ref=f"artifact://{seat.lower()}", contribution_sha256=digit * 64,
        ))

    def test_one_participant_can_freeze_and_reveal(self):
        self.assign("S1", "actor1")
        self.submit("S1", "actor1", "1")
        self.workcell.apply(command("freeze_blind", session_id="session1"))
        self.workcell.apply(command("reveal", session_id="session1"))
        status = self.workcell.status("session1")
        self.assertEqual(status["participant_count"], 1)
        self.assertEqual(status["independent_family_count"], 1)

    def test_three_available_participants_can_freeze_and_reveal(self):
        for n, seat in enumerate(("S1", "S2", "S3"), start=1):
            actor = f"actor{n}"
            self.assign(seat, actor)
            self.submit(seat, actor, str(n))
        self.workcell.apply(command("freeze_blind", session_id="session1"))
        self.workcell.apply(command("reveal", session_id="session1"))
        status = self.workcell.status("session1")
        self.assertEqual(status["round_state"], "REVEALED")
        self.assertEqual(status["participant_count"], 3)
        self.assertEqual(status["independent_family_count"], 3)

    def test_same_family_participants_do_not_fake_independence(self):
        self.assign("S1", "actor1")
        self.assign("S2", "alias1")
        self.submit("S1", "actor1", "1")
        self.submit("S2", "alias1", "2")
        self.workcell.apply(command("freeze_blind", session_id="session1"))
        self.workcell.apply(command("reveal", session_id="session1"))
        status = self.workcell.status("session1")
        self.assertEqual(status["participant_count"], 2)
        self.assertEqual(status["independent_family_count"], 1)
        self.assertEqual(status["independence_status"], "SINGLE_PROVIDER_FAMILY")

    def test_every_assigned_participant_must_submit_before_freeze(self):
        self.assign("S1", "actor1")
        self.assign("S2", "actor2")
        self.submit("S1", "actor1", "1")
        with self.assertRaisesRegex(GateError, "Every assigned participant"):
            self.workcell.apply(command("freeze_blind", session_id="session1"))

    def test_dynamic_slot_label_is_allowed(self):
        self.assign("reviewer-1", "actor1")
        self.submit("reviewer-1", "actor1", "1")
        self.workcell.apply(command("freeze_blind", session_id="session1"))
        self.workcell.apply(command("reveal", session_id="session1"))
        self.assertEqual(self.workcell.status("session1")["participant_count"], 1)

    def test_replacement_before_freeze_discards_old_contribution(self):
        self.assign("S1", "actor1")
        self.submit("S1", "actor1", "1")
        state = self.workcell.apply(command(
            "replace_slot", session_id="session1", seat_id="S1",
            old_participant_id="actor1", participant_id="actor5", family_id="family5",
            model="model-5", version="test", reason="provider unavailable",
        ))["state"]
        self.assertNotIn("S1", state["sessions"]["session1"]["blind_contributions"])

    def test_replacement_after_reveal_is_marked_not_blind(self):
        self.assign("S1", "actor1")
        self.submit("S1", "actor1", "1")
        self.workcell.apply(command("freeze_blind", session_id="session1"))
        self.workcell.apply(command("reveal", session_id="session1"))
        state = self.workcell.apply(command(
            "replace_slot", session_id="session1", seat_id="S1",
            old_participant_id="actor1", participant_id="actor5", family_id="family5",
            model="model-5", version="test", reason="provider failed after reveal",
        ))["state"]
        self.assertTrue(state["sessions"]["session1"]["slots"]["S1"]["joined_after_reveal"])

    def test_workcell_is_bound_to_current_arena_task(self):
        self.assign("S1", "actor1")
        self.core.apply(command(
            "set_goal_status", goal_id="goal1", status="BLOCKED", reason="Owner paused",
        ))
        with self.assertRaisesRegex(GateError, "runtime state is stale|Goal is blocked"):
            self.submit("S1", "actor1", "1")

    def test_official_arena_submission_requires_revealed_workcell(self):
        for n, seat in enumerate(("S1", "S2", "S3"), start=1):
            self.assign(seat, f"actor{n}")
        proposal = command(
            "submit_proposal", id="proposal1", task_id="task1", participant_id="actor1",
            acknowledgement_id="ack1", task_fingerprint=self.task["fingerprint"],
            claim="Bounded proposal", alternative="Alternative",
            uncertainties=["No real outcome"], evidence_ids=[],
            discriminating_test="Compare evidence", method_ref="method@1",
        )
        with self.assertRaisesRegex(GateError, "REVEALED"):
            self.workcell.submit_arena("session1", proposal)

        for n, seat in enumerate(("S1", "S2", "S3"), start=1):
            self.submit(seat, f"actor{n}", str(n))
        self.workcell.apply(command("freeze_blind", session_id="session1"))
        self.workcell.apply(command("reveal", session_id="session1"))
        receipt = self.workcell.submit_arena("session1", proposal)
        self.assertIn("proposal1", receipt["state"]["proposals"])

        outsider = command(
            "submit_proposal", id="proposal2", task_id="task1", participant_id="actor4",
            acknowledgement_id="ack4", task_fingerprint=self.task["fingerprint"],
            claim="Outsider proposal", alternative="Alternative", uncertainties=["Unknown"],
            evidence_ids=[], discriminating_test="Test", method_ref="method@2",
        )
        with self.assertRaisesRegex(GateError, "current participant"):
            self.workcell.submit_arena("session1", outsider)


if __name__ == "__main__":
    unittest.main()
