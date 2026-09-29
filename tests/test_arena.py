import contextlib
import io
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from minhtri.arena import ArenaService
from minhtri.brain import BRAIN_ARTIFACTS
from minhtri.cli import main
from minhtri.core import GateError, Ledger


def command(command_type, **data):
    return {"type": command_type, "data": data}


class ShadowArenaTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.brain_root = root / "repo"
        for index, relative in enumerate(BRAIN_ARTIFACTS, start=1):
            path = self.brain_root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            text = "Owner-approved candidate for shadow test" if relative == "docs/PHILOSOPHY.md" else f"brain-artifact-{index}"
            path.write_text(text, encoding="utf-8")
        self.brain_revision = "a" * 40
        self.core = Ledger(root / "brain")
        self.arena = ArenaService(root / "brain", self.brain_root, self.brain_revision)
        self.expiry = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()

    def ready(self, risk="NORMAL"):
        self.core.init()
        self.core.apply(command("register_domain", id="media", name="Media", risk_class=risk,
                                measurement_contract="Synthetic measurement"))
        self.core.apply(command("open_goal", id="goal1", domain_id="media", objective="Compare proposed methods",
                                priority=3, owner_boundary="Shadow only"))
        self.arena.init()

    def participants(self, count=4):
        for n in range(1, count + 1):
            self.arena.apply(command("register_participant", id=f"actor{n}", family_id=f"family{n}",
                                     model=f"simulated-model-{n}", version="test", adapter="MANUAL",
                                     capabilities=["PROPOSE", "CRITIQUE", "ADJUDICATE"]))

    def task(self):
        state = self.arena.apply(command("open_task", id="task1", goal_id="goal1", brief="Choose a method",
                                         acceptance="Evidence and critique before candidate",
                                         allowed_evidence_ids=[], expires_at=self.expiry))["state"]
        self.task_record = state["tasks"]["task1"]
        return self.task_record["fingerprint"]

    def ack(self, actor, ack_id=None, **overrides):
        task = self.task_record
        data = {
            "id": ack_id or f"ack-{actor}",
            "task_id": "task1",
            "participant_id": actor,
            "task_fingerprint": task["fingerprint"],
            "brain_revision": task["brain_revision"],
            "brain_fingerprint": task["brain_fingerprint"],
            "architecture_law_sha256": task["architecture_law_sha256"],
            "bootstrap_sha256": task["bootstrap_sha256"],
        }
        data.update(overrides)
        return self.arena.apply(command("acknowledge_brain", **data))

    def proposal(self, actor="actor1", fingerprint=None, proposal_id="proposal1", evidence_ids=None, ack_id=None):
        return self.arena.apply(command("submit_proposal", id=proposal_id, task_id="task1",
                                        participant_id=actor, acknowledgement_id=ack_id or f"ack-{actor}",
                                        task_fingerprint=fingerprint or self.fp,
                                        claim="A testable proposal", alternative="Alternative method",
                                        uncertainties=["No real outcome yet"], evidence_ids=evidence_ids or [],
                                        discriminating_test="Compare with baseline", method_ref="method@1"))

    def critique(self, actor="actor2", verdict="NO_MATERIAL_DEFECT_FOUND", critique_id="critique1", ack_id=None):
        return self.arena.apply(command("submit_critique", id=critique_id, proposal_id="proposal1",
                                        participant_id=actor, acknowledgement_id=ack_id or f"ack-{actor}",
                                        task_fingerprint=self.fp, verdict=verdict,
                                        reason="Checked the stated assumptions", evidence_ids=[],
                                        test="Run an independent baseline"))

    def adjudicate(self, critiques, outcome="CANDIDATE_FOR_OWNER_REVIEW", actor="actor3", ack_id=None):
        return self.arena.apply(command("submit_adjudication", id="decision1", proposal_id="proposal1",
                                        participant_id=actor, acknowledgement_id=ack_id or f"ack-{actor}",
                                        task_fingerprint=self.fp, critique_ids=critiques, outcome=outcome,
                                        reason="Only a shadow candidate for Owner review"))

    def test_participant_must_ack_exact_law_and_bootstrap_before_work(self):
        self.ready()
        self.participants()
        self.fp = self.task()
        with self.assertRaisesRegex(GateError, "Unknown acknowledgements"):
            self.proposal()
        with self.assertRaisesRegex(GateError, "must match"):
            self.ack("actor1", ack_id="bad-ack", architecture_law_sha256="0" * 64)
        self.ack("actor1")
        self.proposal()
        self.assertEqual(self.arena.ledger.verify()[0]["proposals"]["proposal1"]["status"], "UNVERIFIED_PROPOSAL")

    def test_acknowledgement_cannot_be_reused_by_another_participant(self):
        self.ready()
        self.participants()
        self.fp = self.task()
        self.ack("actor1")
        with self.assertRaisesRegex(GateError, "does not belong"):
            self.proposal(actor="actor2", ack_id="ack-actor1")

    def test_core_must_exist_before_arena_and_n_participants_are_dynamic(self):
        with self.assertRaises(GateError):
            self.arena.init()
        self.ready()
        self.participants(count=7)
        self.fp = self.task()
        for actor in ("actor7", "actor2", "actor3"):
            self.ack(actor)
        self.proposal(actor="actor7")
        self.critique(actor="actor2")
        result = self.adjudicate(["critique1"], actor="actor3")
        self.assertEqual(result["state"]["adjudications"]["decision1"]["status"], "SHADOW_RECEIPT_ONLY")
        self.assertEqual(len(result["state"]["participants"]), 7)
        self.assertEqual(self.core.verify()[0]["lessons"], {})

    def test_family_independence_and_packet_provenance(self):
        self.ready()
        self.participants()
        self.arena.apply(command("register_participant", id="alias1", family_id="family1", model="another persona",
                                 version="test", adapter="MANUAL", capabilities=["CRITIQUE", "ADJUDICATE"]))
        self.fp = self.task()
        for actor in ("actor1", "actor2", "actor3", "alias1"):
            self.ack(actor)
        with self.assertRaisesRegex(GateError, "fingerprint mismatch"):
            self.proposal(fingerprint="0" * 64)
        with self.assertRaisesRegex(GateError, "outside the task packet"):
            self.proposal(evidence_ids=["unknown"])
        self.proposal()
        with self.assertRaisesRegex(GateError, "another provider family"):
            self.critique(actor="alias1")
        self.critique()
        with self.assertRaisesRegex(GateError, "independent"):
            self.adjudicate(["critique1"], actor="alias1")

    def test_disagreement_and_abstention_are_not_hidden(self):
        self.ready()
        self.participants()
        self.fp = self.task()
        for actor in ("actor1", "actor2", "actor3", "actor4"):
            self.ack(actor)
        self.proposal()
        self.critique(verdict="NO_MATERIAL_DEFECT_FOUND")
        self.critique(actor="actor4", verdict="CHALLENGE", critique_id="critique2")
        with self.assertRaisesRegex(GateError, "every critique"):
            self.adjudicate(["critique1"])
        with self.assertRaisesRegex(GateError, "challenge or abstention"):
            self.adjudicate(["critique1", "critique2"])
        result = self.adjudicate(["critique1", "critique2"], outcome="HOLD")
        self.assertEqual(result["state"]["adjudications"]["decision1"]["outcome"], "HOLD")
        with self.assertRaisesRegex(GateError, "frozen"):
            self.critique(actor="actor4", critique_id="late-critique")

    def test_runtime_or_any_brain_drift_blocks_old_task(self):
        self.ready()
        self.participants()
        self.fp = self.task()
        self.ack("actor1")
        architecture = self.brain_root / "docs" / "ARCHITECTURE.md"
        original = architecture.read_text(encoding="utf-8")
        architecture.write_text("changed architecture", encoding="utf-8")
        with self.assertRaisesRegex(GateError, "brain version is stale"):
            self.proposal()
        architecture.write_text(original, encoding="utf-8")
        self.core.apply(command("set_goal_status", goal_id="goal1", status="BLOCKED", reason="Owner stopped"))
        with self.assertRaisesRegex(GateError, "runtime state is stale"):
            self.proposal()

    def test_project_law_drift_blocks_old_task(self):
        self.ready()
        self.participants()
        self.fp = self.task()
        self.ack("actor1")
        law = self.brain_root / "PROJECT_LAW.md"
        law.write_text("mutated law", encoding="utf-8")
        with self.assertRaisesRegex(GateError, "brain version is stale|architecture law is stale"):
            self.proposal()

    def test_git_revision_drift_blocks_old_task(self):
        self.ready()
        self.participants()
        self.fp = self.task()
        self.ack("actor1")
        self.arena.brain_revision = "b" * 40
        with self.assertRaisesRegex(GateError, "brain version is stale"):
            self.proposal()

    def test_risk_context_and_law_are_derived_from_brain_and_core(self):
        self.ready(risk="HIGH_STAKES")
        self.participants()
        self.fp = self.task()
        task = self.arena.ledger.verify()[0]["tasks"]["task1"]
        self.assertEqual(task["risk_class"], "HIGH_STAKES")
        self.assertEqual(task["budget_cap"], 0)
        self.assertEqual(task["mode"], "SHADOW")
        self.assertEqual(task["sensitivity"], "PUBLIC")
        self.assertEqual(task["brain_revision"], self.brain_revision)
        self.assertEqual(len(task["brain_fingerprint"]), 64)
        self.assertEqual(len(task["architecture_law_sha256"]), 64)
        self.assertEqual(len(task["bootstrap_sha256"]), 64)
        self.assertEqual(len(task["runtime_state_head"]), 64)
        with self.assertRaisesRegex(GateError, "unexpected fields"):
            self.arena.apply(command("open_task", id="task2", goal_id="goal1", brief="Override",
                                     acceptance="No", allowed_evidence_ids=[], expires_at=self.expiry,
                                     risk_class="NORMAL"))

    def test_export_packet_contains_law_bootstrap_and_bounded_evidence(self):
        self.ready()
        observed = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
        self.core.apply(command("record_source", id="source1", domain_id="media", uri="synthetic://demo",
                                captured_at=observed, kind="SYNTHETIC", rights_status="CLEAR"))
        for eid in ("evidence1", "evidence2"):
            self.core.apply(command("record_evidence", id=eid, domain_id="media", source_id="source1",
                                    statement=f"Synthetic statement {eid}", observed_at=observed))
        state = self.arena.apply(command("open_task", id="task1", goal_id="goal1", brief="Scoped comparison",
                                         acceptance="Check evidence", allowed_evidence_ids=["evidence1"],
                                         expires_at=self.expiry))["state"]
        self.task_record = state["tasks"]["task1"]
        packet = self.arena.task_packet("task1")
        self.assertEqual([e["id"] for e in packet["evidence"]], ["evidence1"])
        self.assertIn("PROJECT_LAW", packet["project_law"])
        self.assertIn("BOOTSTRAP", packet["bootstrap"])
        self.assertEqual(packet["acknowledgement_required"]["task_fingerprint"], self.task_record["fingerprint"])
        self.assertEqual(packet["brain"]["manifest"]["brain_revision"], self.brain_revision)
        self.assertEqual([item["path"] for item in packet["brain"]["manifest"]["artifacts"]], list(BRAIN_ARTIFACTS))
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exit_code = main(["--home", str(self.core.home), "arena", "--brain-root", str(self.brain_root),
                              "--brain-revision", self.brain_revision, "task", "task1"])
        self.assertEqual(exit_code, 0)
        self.assertEqual(json.loads(output.getvalue()), packet)


if __name__ == "__main__":
    unittest.main()
