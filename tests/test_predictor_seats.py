import tempfile
import unittest
from pathlib import Path

from minhtri.core import GateError, Ledger, canonical, digest, evolve, initial_state


def cmd(command_type, **data):
    return {"type": command_type, "data": data}


SETUP = [
    cmd("register_domain", id="media", name="Media", risk_class="NORMAL", measurement_contract="Data"),
    cmd("open_goal", id="g1", domain_id="media", objective="Learn", priority=3, owner_boundary="Read only"),
    cmd("frame_problem", id="p1", goal_id="g1", reality="Unknown",
        conditions=[{"description": "Mix", "role": "CONDITION", "status": "HYPOTHESIS"}],
        target="Measure", intervention="Compare", unknowns=["Base"], control="Design",
        influence="Exposure", responsibility="Owner", harm_checks=["No deception"]),
    *[cmd("register_provider", id=pid, name=pid, kind="MODEL") for pid in ("maker", "forecaster", "critic", "judge")],
    *[cmd("register_procedure", id=f"proc-{pid}", domain_id="media", provider_id=pid, version="1", method="Range")
      for pid in ("maker", "forecaster", "critic", "judge")],
    cmd("propose_claim", id="h1", problem_id="p1", provider_id="maker", statement="Hypothesis",
        evidence_ids=[], alternative="Chance", falsifier="Misses"),
]


def prediction(pid, procedure):
    return cmd("register_prediction", id=pid, claim_id="h1", procedure_id=procedure, metric="rate", unit="percent",
               lower=5, upper=7, due_at="2026-02-01T00:00:00Z", resolution_method="Report")


class PredictorSeats(unittest.TestCase):
    def setUp(self):
        self.at = "2026-01-01T00:00:00Z"
        self.state = initial_state()
        for command in SETUP:
            self.state = evolve(self.state, command, self.at)

    def apply(self, command):
        self.state = evolve(self.state, command, self.at)

    def test_predictor_equal_to_proposer_is_rejected(self):
        with self.assertRaisesRegex(GateError, "Predictor must not be"):
            self.apply(prediction("f1", "proc-maker"))

    def test_predictor_equal_to_critic_is_rejected(self):
        self.apply(prediction("f1", "proc-forecaster"))
        self.apply(cmd("review_claim", id="rv", claim_id="h1", critic_provider_id="critic", verdict="HOLD", reason="Wait"))
        with self.assertRaisesRegex(GateError, "Predictor must not be"):
            self.apply(prediction("f2", "proc-critic"))

    def test_predictor_equal_to_adjudicator_is_rejected(self):
        self.apply(prediction("f1", "proc-forecaster"))
        self.apply(cmd("review_claim", id="rv", claim_id="h1", critic_provider_id="critic", verdict="HOLD", reason="Wait"))
        self.apply(cmd("adjudicate_claim", id="adj", claim_id="h1", review_id="rv", adjudicator_provider_id="judge",
                       verdict="HOLD", reason="Wait"))
        with self.assertRaisesRegex(GateError, "Predictor must not be"):
            self.apply(prediction("f2", "proc-judge"))

    def test_distinct_forecaster_is_allowed(self):
        self.apply(prediction("f1", "proc-forecaster"))
        self.assertEqual(self.state["predictions"]["f1"]["status"], "REGISTERED")

    def test_ledger_written_before_the_rule_still_verifies_but_new_append_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Ledger(Path(tmp) / "brain")
            ledger.init()
            for command in SETUP:
                ledger.apply(command)
            # Simulate an older ledger line where the proposer also predicted (allowed before this rule).
            state, count, head = ledger.verify()
            body = {"seq": count + 1, "prev": head, "at": "2026-01-01T00:00:00Z", "command": prediction("old", "proc-maker")}
            with ledger.events.open("ab") as fh:
                fh.write(canonical({**body, "hash": digest(body)}) + b"\n")
            ledger.repair_snapshot()
            self.assertEqual(ledger.verify()[1], count + 1)
            with self.assertRaisesRegex(GateError, "Predictor must not be"):
                ledger.apply(prediction("new", "proc-maker"))
            self.assertEqual(ledger.verify()[1], count + 1)


if __name__ == "__main__":
    unittest.main()
