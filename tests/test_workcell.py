import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from minhtri.arena import ArenaService
from minhtri.brain import BRAIN_ARTIFACTS
from minhtri.core import GateError, Ledger
from minhtri.workcell import FourSeatWorkcellService


def command(command_type, **data):
    return {"type": command_type, "data": data}


class FourSeatWorkcellTests(unittest.TestCase):
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
            else:
                text = f"artifact-{index}\n"
            path.write_text(text, encoding="utf-8")

        self.core = Ledger(root / "brain")
        self.core.init()
        self.core.apply(command(
            "register_domain", id="media", name="Media", risk_class="NORMAL",
            measurement_contract="Synthetic",
        ))
        self.core.apply(command(
            "open_goal", id="goal1", domain_id="media", objective="Four AI review",
            priority=4, owner_boundary="Shadow only",
        ))
        self.arena = ArenaService(root / "brain", self.brain_root, "a" * 40)
        self.arena.init()
        for n in range(1, 6):
            self.arena.apply(command(
                "register_participant",
                id=f"actor{n}",
                family_id=f"family{n}",
                model=f"model-{n}",
                version="test",
                adapter="MANUAL",
                capabilities=["PROPOSE", "CRITIQUE", "ADJUDICATE"],
            ))
        expiry = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
        task_state = self.arena.apply(command(
            "open_task", id="task1", goal_id="goal1", brief="Review architecture",
            acceptance="Four blind contributions", allowed_evidence_ids=[], expires_at=expiry,
        ))["state"]
        self.task = task_state["tasks"]["task1"]
        for n in range(1, 6):
            self.arena.apply(command(
                "acknowledge_brain",
                id=f"ack{n}",
                task_id="task1",
                participant_id=f"actor{n}",
                task_fingerprint=self.task["fingerprint"],
                brain_revision=self.task["brain_revision"],
                brain_fingerprint=self.task["brain_fingerprint"],
                architecture_law_sha256=self.task["architecture_law_sha256"],
                bootstrap_sha256=self.task["bootstrap_sha256"],
            ))
        self.workcell = FourSeatWorkcellService(root / "brain", self.brain_root, "a" * 40)
        self.workcell.init()
        self.workcell.apply(command("open_session", id="session1", arena_task_id="task1"))

    def assign(self, seat, actor, family=None):
        n = actor.replace("actor", "")
        return self.workcell.apply(command(
            "assign_slot", session_id="session1", seat_id=seat, participant_id=actor,
            family_id=family or f"family{n}", model=f"model-{n}", version="test",
        ))

    def fill_four(self):
        for seat, actor in zip(("S1", "S2", "S3", "S4"), ("actor1", "actor2", "actor3", "actor4")):
            self.assign(seat, actor)

    def submit_four(self):
        for seat, actor in zip(("S1", "S2", "S3", "S4"), ("actor1", "actor2", "actor3", "actor4")):
            self.workcell.apply(command(
                "submit_blind", session_id="session1", seat_id=seat, participant_id=actor,
                contribution_ref=f"artifact://{seat.lower()}",
                contribution_sha256=(seat[-1] * 64),
            ))

    def test_requires_four_distinct_provider_families(self):
        self.assign("S1", "actor1")
        with self.assertRaisesRegex(GateError, "family_id must match"):
            self.assign("S2", "actor2", family="family1")

        # Alias with same family is blocked even if participant ID differs.
        self.arena.apply(command(
            "register_participant", id="alias1", family_id="family1", model="alias", version="test",
            adapter="MANUAL", capabilities=["PROPOSE", "CRITIQUE", "ADJUDICATE"],
        ))
        self.arena.apply(command(
            "acknowledge_brain", id="ack-alias", task_id="task1", participant_id="alias1",
            task_fingerprint=self.task["fingerprint"], brain_revision=self.task["brain_revision"],
            brain_fingerprint=self.task["brain_fingerprint"],
            architecture_law_sha256=self.task["architecture_law_sha256"],
            bootstrap_sha256=self.task["bootstrap_sha256"],
        ))
        with self.assertRaisesRegex(GateError, "provider family"):
            self.workcell.apply(command(
                "assign_slot", session_id="session1", seat_id="S2", participant_id="alias1",
                family_id="family1", model="alias", version="test",
            ))

    def test_three_of_four_cannot_freeze_or_reveal(self):
        for seat, actor in zip(("S1", "S2", "S3"), ("actor1", "actor2", "actor3")):
            self.assign(seat, actor)
            self.workcell.apply(command(
                "submit_blind", session_id="session1", seat_id=seat, participant_id=actor,
                contribution_ref=f"artifact://{seat.lower()}",
                contribution_sha256=(seat[-1] * 64),
            ))
        with self.assertRaisesRegex(GateError, "Four occupied"):
            self.workcell.apply(command("freeze_blind", session_id="session1"))
        with self.assertRaisesRegex(GateError, "Reveal requires"):
            self.workcell.apply(command("reveal", session_id="session1"))

    def test_four_of_four_blind_round_freezes_before_reveal(self):
        self.fill_four()
        self.submit_four()
        state = self.workcell.apply(command("freeze_blind", session_id="session1"))["state"]
        session = state["sessions"]["session1"]
        self.assertEqual(session["round_state"], "BLIND_FROZEN")
        self.assertEqual(len(session["blind_contributions"]), 4)
        self.assertEqual(len(session["blind_round_fingerprint"]), 64)
        state = self.workcell.apply(command("reveal", session_id="session1"))["state"]
        self.assertEqual(state["sessions"]["session1"]["round_state"], "REVEALED")

    def test_replacement_before_freeze_discards_old_blind_contribution(self):
        self.fill_four()
        self.workcell.apply(command(
            "submit_blind", session_id="session1", seat_id="S1", participant_id="actor1",
            contribution_ref="artifact://old", contribution_sha256="1" * 64,
        ))
        state = self.workcell.apply(command(
            "replace_slot", session_id="session1", seat_id="S1",
            old_participant_id="actor1", participant_id="actor5", family_id="family5",
            model="model-5", version="test", reason="provider unavailable",
        ))["state"]
        session = state["sessions"]["session1"]
        self.assertNotIn("S1", session["blind_contributions"])
        self.assertEqual(session["slots"]["S1"]["participant_id"], "actor5")
        self.assertEqual(session["replacement_history"][-1]["round_state"], "BLIND_OPEN")

    def test_replacement_after_reveal_is_marked_not_blind(self):
        self.fill_four()
        self.submit_four()
        self.workcell.apply(command("freeze_blind", session_id="session1"))
        self.workcell.apply(command("reveal", session_id="session1"))
        state = self.workcell.apply(command(
            "replace_slot", session_id="session1", seat_id="S1",
            old_participant_id="actor1", participant_id="actor5", family_id="family5",
            model="model-5", version="test", reason="provider failed after reveal",
        ))["state"]
        self.assertTrue(state["sessions"]["session1"]["slots"]["S1"]["joined_after_reveal"])

    def test_workcell_is_bound_to_current_arena_task(self):
        self.fill_four()
        # Mutating Core stales the Arena task. Workcell must fail closed too.
        self.core.apply(command(
            "set_goal_status", goal_id="goal1", status="BLOCKED", reason="Owner paused",
        ))
        with self.assertRaisesRegex(GateError, "runtime state is stale|Goal is blocked"):
            self.workcell.apply(command(
                "submit_blind", session_id="session1", seat_id="S1", participant_id="actor1",
                contribution_ref="artifact://s1", contribution_sha256="1" * 64,
            ))


if __name__ == "__main__":
    unittest.main()
