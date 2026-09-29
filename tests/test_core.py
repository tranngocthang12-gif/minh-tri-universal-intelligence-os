import json
import tempfile
import unittest
from pathlib import Path

from minhtri.core import GateError, Ledger, evolve, initial_state, next_goal


def cmd(command_type, **data):
    return {"type": command_type, "data": data}


class CoreGates(unittest.TestCase):
    def setUp(self):
        self.state = initial_state()
        self.at = "2026-01-01T00:00:00Z"

    def apply(self, command_type, at=None, **data):
        self.state = evolve(self.state, cmd(command_type, **data), at or self.at)

    def base(self, risk="NORMAL"):
        self.apply("register_domain", id="media", name="Media", risk_class=risk, measurement_contract="Owner supplied analytics")
        self.apply("open_goal", id="goal1", domain_id="media", objective="Evaluate a possible improvement",
                   priority=3, owner_boundary="No external actions")
        self.apply("frame_problem", id="problem1", goal_id="goal1", reality="Performance is unknown",
                   conditions=[{"description": "Audience mix may change", "role": "CONDITION", "status": "HYPOTHESIS"}],
                   target="Get a reliable measurement", intervention="Run a bounded comparison",
                   unknowns=["Base rate"], control="Test design", influence="Audience exposure",
                   responsibility="Owner decides", harm_checks=["Do not mislead viewers"])
        for pid in ("maker", "critic", "judge"):
            self.apply("register_provider", id=pid, name=pid, kind="MODEL")
        self.apply("register_procedure", id="p1", domain_id="media", provider_id="maker", version="1", method="Range forecast")
        self.apply("propose_claim", id="h1", problem_id="problem1", provider_id="maker", statement="Test hypothesis",
                   evidence_ids=[], alternative="Seasonal audience difference", falsifier="Intervals miss on independent outcomes")

    def predictions_and_outcomes(self):
        self.apply("register_prediction", id="f1", claim_id="h1", procedure_id="p1", metric="rate",
                   unit="percent", lower=5, upper=7, due_at="2026-01-03T00:00:00Z", resolution_method="Read approved report")
        self.apply("register_prediction", id="f2", claim_id="h1", procedure_id="p1", metric="rate",
                   unit="percent", lower=6, upper=8, due_at="2026-01-07T00:00:00Z", resolution_method="Read approved report")
        self.apply("freeze_prediction", prediction_id="f1")
        self.apply("freeze_prediction", prediction_id="f2")
        for n, when, value in ((1, "2026-01-04T00:00:00Z", 6.0), (2, "2026-01-08T00:00:00Z", 6.5)):
            self.apply("record_source", at=when, id=f"s{n}", domain_id="media", uri=f"internal://report/{n}",
                       captured_at=when, kind="FIRST_PARTY", rights_status="CLEAR")
            self.apply("record_evidence", at=when, id=f"e{n}", domain_id="media", source_id=f"s{n}",
                       statement="Recorded measurement", observed_at=when, value=value, metric="rate")
            self.apply("record_resolution", at=when, id=f"r{n}", prediction_id=f"f{n}", evidence_id=f"e{n}")

    def review_and_lesson(self):
        self.apply("review_claim", id="review1", claim_id="h1", critic_provider_id="critic",
                   verdict="ACCEPT_FOR_TRIAL", reason="Alternative remains testable")
        self.apply("adjudicate_claim", id="adj1", claim_id="h1", review_id="review1",
                   adjudicator_provider_id="judge", verdict="ACCEPT_FOR_TRIAL", reason="Bounded trial only")
        self.apply("propose_lesson", id="lesson1", claim_id="h1", statement="Try this narrow method",
                   limits="Two observations; confounding unresolved", prediction_ids=["f1", "f2"], adjudication_id="adj1")

    def test_two_domains_do_not_change_core_and_wait_is_explicit(self):
        self.assertEqual(next_goal(self.state)["status"], "WAIT")
        self.apply("register_domain", id="youtube", name="YouTube", risk_class="NORMAL", measurement_contract="CTR")
        self.apply("register_domain", id="finance", name="Finance", risk_class="HIGH_STAKES", measurement_contract="Returns")
        self.apply("open_goal", id="g1", domain_id="youtube", objective="Measure", priority=3, owner_boundary="Read only")
        self.assertEqual(next_goal(self.state)["goal"]["id"], "g1")
        self.apply("set_goal_status", goal_id="g1", status="BLOCKED", reason="No data permission")
        self.assertEqual(next_goal(self.state)["status"], "WAIT")

    def test_preregistration_three_seats_and_trial_gate(self):
        self.base()
        self.apply("register_prediction", id="f1", claim_id="h1", procedure_id="p1", metric="rate",
                   unit="percent", lower=5, upper=7, due_at="2026-01-03T00:00:00Z", resolution_method="Report")
        self.apply("record_source", id="s1", domain_id="media", uri="internal://early", captured_at=self.at,
                   kind="FIRST_PARTY", rights_status="CLEAR")
        self.apply("record_evidence", id="e1", domain_id="media", source_id="s1", statement="Early metric",
                   observed_at=self.at, value=6, metric="rate")
        with self.assertRaises(GateError):
            self.apply("record_resolution", id="r1", prediction_id="f1", evidence_id="e1")
        with self.assertRaises(GateError):
            self.apply("review_claim", id="bad", claim_id="h1", critic_provider_id="maker", verdict="HOLD", reason="Self-review")
        self.assertEqual(self.state["predictions"]["f1"]["status"], "REGISTERED")

        # Rebuild without the early test prediction, then exercise the full guarded flow.
        self.setUp()
        self.base()
        self.predictions_and_outcomes()
        self.review_and_lesson()
        self.apply("activate_trial_lesson", lesson_id="lesson1", owner_ack="HUMAN_OWNER_APPROVED", scope="One internal pilot")
        self.assertEqual(self.state["lessons"]["lesson1"]["status"], "TRIAL_RULE")
        self.assertEqual(self.state["resolutions"]["r1"]["interval_hit"], True)
        self.assertEqual(self.state["claims"]["h1"]["epistemic_status"], "HYPOTHESIS")

    def test_high_stakes_cannot_activate_even_with_two_outcomes(self):
        self.base(risk="HIGH_STAKES")
        self.predictions_and_outcomes()
        self.review_and_lesson()
        with self.assertRaises(GateError):
            self.apply("activate_trial_lesson", lesson_id="lesson1", owner_ack="HUMAN_OWNER_APPROVED", scope="Trading")

    def test_cross_domain_evidence_and_future_observation_are_blocked(self):
        self.base()
        self.apply("register_domain", id="other", name="Other", risk_class="NORMAL", measurement_contract="Data")
        self.apply("record_source", id="s1", domain_id="media", uri="internal://source", captured_at=self.at,
                   kind="FIRST_PARTY", rights_status="CLEAR")
        with self.assertRaises(GateError):
            self.apply("record_evidence", id="bad", domain_id="other", source_id="s1", statement="Wrong domain", observed_at=self.at)
        with self.assertRaises(GateError):
            self.apply("record_evidence", id="future", domain_id="media", source_id="s1", statement="Future",
                       observed_at="2027-01-01T00:00:00Z")
        with self.assertRaises(GateError):
            self.apply("propose_claim", id="bad", problem_id="problem1", provider_id="maker", statement="Unknown",
                       evidence_ids=[{}], alternative="Other", falsifier="Test")

    def test_hash_chain_and_cache_detect_partial_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Ledger(Path(tmp) / "brain")
            ledger.init()
            ledger.apply(cmd("register_domain", id="youtube", name="YouTube", risk_class="NORMAL", measurement_contract="CTR"))
            self.assertEqual(ledger.verify()[1], 1)
            ledger.snapshot.write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(GateError, "Snapshot differs"):
                ledger.verify()
            ledger.repair_snapshot()
            self.assertEqual(ledger.verify()[1], 1)
            lines = ledger.events.read_text(encoding="utf-8").replace("YouTube", "Finance")
            ledger.events.write_text(lines, encoding="utf-8")
            with self.assertRaisesRegex(GateError, "chain mismatch"):
                ledger.verify()


if __name__ == "__main__":
    unittest.main()
