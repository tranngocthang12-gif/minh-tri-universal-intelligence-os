import unittest

from minhtri.core import GateError, evolve, initial_state


def cmd(command_type, **data):
    return {"type": command_type, "data": data}


class PublicSource(unittest.TestCase):
    """PUBLIC is accepted as a declared source kind but can never reach TRIAL_RULE or VERIFIED."""

    def setUp(self):
        self.state = initial_state()
        self.at = "2026-01-01T00:00:00Z"

    def apply(self, command_type, at=None, **data):
        self.state = evolve(self.state, cmd(command_type, **data), at or self.at)

    def build_lesson(self, outcome_kind, rights="CLEAR"):
        self.apply("register_domain", id="media", name="Media", risk_class="NORMAL", measurement_contract="Data")
        self.apply("open_goal", id="g1", domain_id="media", objective="Learn", priority=3, owner_boundary="Read only")
        self.apply("frame_problem", id="p1", goal_id="g1", reality="Unknown",
                   conditions=[{"description": "Mix", "role": "CONDITION", "status": "HYPOTHESIS"}],
                   target="Measure", intervention="Compare", unknowns=["Base"], control="Design",
                   influence="Exposure", responsibility="Owner", harm_checks=["No deception"])
        for pid in ("maker", "forecaster", "critic", "judge"):
            self.apply("register_provider", id=pid, name=pid, kind="MODEL")
        self.apply("register_procedure", id="proc", domain_id="media", provider_id="forecaster", version="1", method="Range")
        self.apply("propose_claim", id="h1", problem_id="p1", provider_id="maker", statement="Hypothesis",
                   evidence_ids=[], alternative="Chance", falsifier="Misses")
        for n, due, obs in ((1, "2026-01-03T00:00:00Z", "2026-01-04T00:00:00Z"),
                            (2, "2026-01-07T00:00:00Z", "2026-01-08T00:00:00Z")):
            self.apply("register_prediction", id=f"f{n}", claim_id="h1", procedure_id="proc", metric="rate",
                       unit="percent", lower=5, upper=7, due_at=due, resolution_method="Report")
            self.apply("freeze_prediction", prediction_id=f"f{n}")
            self.apply("record_source", at=obs, id=f"s{n}", domain_id="media", uri=f"https://example.invalid/{n}",
                       captured_at=obs, kind=outcome_kind, rights_status=rights)
            self.apply("record_evidence", at=obs, id=f"e{n}", domain_id="media", source_id=f"s{n}",
                       statement="Outcome", observed_at=obs, value=6, metric="rate")
            self.apply("record_resolution", at=obs, id=f"r{n}", prediction_id=f"f{n}", evidence_id=f"e{n}")
        self.apply("review_claim", id="rv", claim_id="h1", critic_provider_id="critic",
                   verdict="ACCEPT_FOR_TRIAL", reason="Testable")
        self.apply("adjudicate_claim", id="adj", claim_id="h1", review_id="rv", adjudicator_provider_id="judge",
                   verdict="ACCEPT_FOR_TRIAL", reason="Bounded")
        self.apply("propose_lesson", id="l1", claim_id="h1", statement="Narrow", limits="Two cases",
                   prediction_ids=["f1", "f2"], adjudication_id="adj")

    def all_values(self, node):
        if isinstance(node, dict):
            for value in node.values():
                yield from self.all_values(value)
        elif isinstance(node, list):
            for value in node:
                yield from self.all_values(value)
        else:
            yield node

    def activate(self):
        self.apply("activate_trial_lesson", lesson_id="l1", owner_ack="HUMAN_OWNER_APPROVED", scope="Pilot")

    def test_public_source_is_accepted_and_evidence_stays_unverified(self):
        self.apply("register_domain", id="media", name="Media", risk_class="NORMAL", measurement_contract="Data")
        self.apply("record_source", id="s1", domain_id="media", uri="https://example.invalid/case",
                   captured_at=self.at, kind="PUBLIC", rights_status="UNKNOWN")
        self.apply("record_evidence", id="e1", domain_id="media", source_id="s1", statement="Public case",
                   observed_at=self.at)
        self.assertEqual(self.state["sources"]["s1"]["kind"], "PUBLIC")
        self.assertEqual(self.state["evidence"]["e1"]["verification"], "DECLARED_UNVERIFIED")

    def test_public_outcomes_cannot_activate_trial_lesson(self):
        self.build_lesson("PUBLIC")
        with self.assertRaisesRegex(GateError, "first-party"):
            self.activate()
        self.assertEqual(self.state["lessons"]["l1"]["status"], "CANDIDATE")
        self.assertNotIn("VERIFIED", list(self.all_values(self.state)))

    def test_third_party_and_unclear_rights_still_blocked_first_party_clear_allowed(self):
        self.build_lesson("THIRD_PARTY")
        with self.assertRaises(GateError):
            self.activate()
        self.setUp()
        self.build_lesson("FIRST_PARTY", rights="UNKNOWN")
        with self.assertRaises(GateError):
            self.activate()
        self.setUp()
        self.build_lesson("FIRST_PARTY")
        self.activate()
        lesson = self.state["lessons"]["l1"]
        self.assertEqual(lesson["status"], "TRIAL_RULE")
        self.assertNotIn("VERIFIED", list(self.all_values(self.state)))

    def test_unknown_source_kind_still_rejected(self):
        self.apply("register_domain", id="media", name="Media", risk_class="NORMAL", measurement_contract="Data")
        with self.assertRaises(GateError):
            self.apply("record_source", id="s1", domain_id="media", uri="x", captured_at=self.at,
                       kind="VERIFIED", rights_status="CLEAR")


if __name__ == "__main__":
    unittest.main()
