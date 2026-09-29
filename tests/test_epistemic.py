import json
import tempfile
import unittest
from pathlib import Path

from minhtri.core import GateError, Ledger, canonical, digest, evolve, initial_state
from minhtri.epistemic import EpistemicService, MATURITY_LEVELS


def command(command_type, **data):
    return {"type": command_type, "data": data}


def build_core_fixture(home: Path) -> None:
    """Create a valid Core ledger with controlled historical timestamps."""
    events = [
        ("2026-01-01T00:00:00Z", command(
            "register_domain", id="media", name="Media", risk_class="NORMAL",
            measurement_contract="Observed rate",
        )),
        ("2026-01-01T00:01:00Z", command("register_provider", id="maker", name="Maker", kind="MODEL")),
        ("2026-01-01T00:02:00Z", command("register_provider", id="critic", name="Critic", kind="MODEL")),
        ("2026-01-01T00:03:00Z", command("register_provider", id="judge", name="Judge", kind="HUMAN")),
        ("2026-01-01T00:04:00Z", command(
            "open_goal", id="goal1", domain_id="media", objective="Learn a testable relationship",
            priority=4, owner_boundary="Research only",
        )),
        ("2026-01-01T00:05:00Z", command(
            "frame_problem", id="problem1", goal_id="goal1", reality="Rate is uncertain",
            conditions=[{"description": "Possible condition", "role": "CONDITION", "status": "HYPOTHESIS"}],
            target="Understand and predict rate", intervention="Observe and test",
            unknowns=["Actual rate"], control="Method", influence="Sampling",
            responsibility="Evidence", harm_checks=["No external action"],
        )),
        ("2026-01-01T00:06:00Z", command(
            "record_source", id="source1", domain_id="media", uri="internal://baseline",
            captured_at="2026-01-01T00:06:00Z", kind="FIRST_PARTY", rights_status="CLEAR",
        )),
        ("2026-01-01T00:07:00Z", command(
            "record_evidence", id="evidence1", domain_id="media", source_id="source1",
            statement="Observed baseline supports a testable relationship",
            observed_at="2026-01-01T00:07:00Z",
        )),
        ("2026-01-01T00:08:00Z", command(
            "register_procedure", id="procedure1", domain_id="media", provider_id="maker",
            version="1", method="Pre-register interval",
        )),
        ("2026-01-01T00:09:00Z", command(
            "propose_claim", id="claim1", problem_id="problem1", provider_id="maker",
            statement="Rate will be between 5 and 7", evidence_ids=["evidence1"],
            alternative="Rate may lie outside the interval", falsifier="Observed rate outside interval",
        )),
        ("2026-01-01T00:10:00Z", command(
            "register_prediction", id="prediction1", claim_id="claim1", procedure_id="procedure1",
            metric="rate", unit="percent", lower=5, upper=7,
            due_at="2026-01-03T00:00:00Z", resolution_method="First-party report",
        )),
        ("2026-01-02T00:00:00Z", command("freeze_prediction", prediction_id="prediction1")),
        ("2026-01-04T00:00:00Z", command(
            "record_source", id="source2", domain_id="media", uri="internal://outcome",
            captured_at="2026-01-04T00:00:00Z", kind="FIRST_PARTY", rights_status="CLEAR",
        )),
        ("2026-01-04T00:01:00Z", command(
            "record_evidence", id="outcome1", domain_id="media", source_id="source2",
            statement="Observed final rate", observed_at="2026-01-04T00:01:00Z",
            value=6.0, metric="rate",
        )),
        ("2026-01-05T00:00:00Z", command(
            "record_resolution", id="resolution1", prediction_id="prediction1", evidence_id="outcome1",
        )),
        ("2026-01-06T00:00:00Z", command(
            "review_claim", id="review1", claim_id="claim1", critic_provider_id="critic",
            verdict="HOLD", reason="One outcome is not enough for a rule",
        )),
    ]

    home.mkdir(parents=True, exist_ok=True)
    state = initial_state()
    previous = "0" * 64
    lines = []
    for seq, (at, cmd) in enumerate(events, start=1):
        state = evolve(state, cmd, at)
        body = {"seq": seq, "prev": previous, "at": at, "command": cmd}
        event = {**body, "hash": digest(body)}
        previous = event["hash"]
        lines.append(canonical(event).decode("utf-8"))
    (home / "events.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    snapshot = {"event_count": len(events), "head": previous, "state": state}
    (home / "state.json").write_bytes(canonical(snapshot) + b"\n")


class EpistemicStateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name) / "brain"
        build_core_fixture(self.home)
        self.service = EpistemicService(self.home)
        self.service.init()

    def register_item(self):
        return self.service.apply(command(
            "register_item",
            id="item1",
            domain_id="media",
            subject="A rate relationship",
            kind="HYPOTHESIS",
            scope="This media pilot only",
            origin_ref="claim1",
            review_due_at="2026-12-31T00:00:00Z",
        ))

    def to_l6(self):
        self.register_item()
        self.service.apply(command(
            "support_item", item_id="item1", evidence_ids=["evidence1"],
            support_note="First-party baseline observation",
        ))
        self.service.apply(command(
            "demonstrate_understanding", item_id="item1",
            explanation="The relationship is conditional on the observed setup.",
            distinction="Correlation alone would not imply the same causal claim.",
            expected_pattern="A repeat should place the rate near the preregistered range.",
            falsifier="Repeated observed outcomes outside the range would defeat the explanation.",
        ))
        self.service.apply(command("link_prediction", item_id="item1", prediction_id="prediction1"))
        self.service.apply(command(
            "record_application", item_id="item1", mode="READ_ONLY_ANALYSIS",
            description="Apply the understanding to a read-only forecast check.",
            artifact_refs=["artifact://forecast-check"],
        ))
        self.service.apply(command(
            "record_validation", item_id="item1", resolution_id="resolution1",
            quality_note="First-party observed outcome; still declared unverified provenance.",
        ))
        self.service.apply(command("link_critique", item_id="item1", review_id="review1"))

    def test_maturity_is_derived_and_cannot_jump_over_evidence(self):
        self.register_item()
        self.assertEqual(self.service.item("item1")["effective_level"], "L0_MEMORY")

        with self.assertRaisesRegex(GateError, "before evidence-supported knowledge"):
            self.service.apply(command(
                "demonstrate_understanding", item_id="item1", explanation="Why",
                distinction="Different", expected_pattern="Pattern", falsifier="Counterexample",
            ))

        self.service.apply(command(
            "support_item", item_id="item1", evidence_ids=["evidence1"], support_note="Observed support",
        ))
        self.assertEqual(self.service.item("item1")["effective_level"], "L1_KNOWLEDGE")

        self.service.apply(command(
            "demonstrate_understanding", item_id="item1",
            explanation="Conditional explanation",
            distinction="Not the nearby alternative",
            expected_pattern="Expected future pattern",
            falsifier="Observed counter-pattern",
        ))
        self.assertEqual(self.service.item("item1")["effective_level"], "L2_UNDERSTANDING")

        self.service.apply(command("link_prediction", item_id="item1", prediction_id="prediction1"))
        self.assertEqual(self.service.item("item1")["effective_level"], "L3_PREDICTION")

    def test_full_r3_path_reaches_l6_but_l7_to_l9_remain_future_gates(self):
        self.to_l6()
        item = self.service.item("item1")
        self.assertEqual(item["effective_level"], "L6_SELF_CRITICISM")
        self.assertEqual(item["highest_demonstrated_level"], "L6_SELF_CRITICISM")
        self.assertEqual(item["future_gates"]["L7_META_LEARNING"], "R5_REQUIRED")
        self.assertEqual(item["future_gates"]["L8_SELF_REPAIR"], "R5_OR_LATER_REQUIRED")
        self.assertEqual(item["future_gates"]["L9_TRANSFER"], "R8_REQUIRED")
        self.assertEqual(set(MATURITY_LEVELS[-3:]), {"L7_META_LEARNING", "L8_SELF_REPAIR", "L9_TRANSFER"})

    def test_reopen_suspends_effective_maturity_but_preserves_history(self):
        self.to_l6()
        self.service.apply(command(
            "reopen_item", item_id="item1", trigger="NEW_EVIDENCE",
            reason="A counterexample needs review",
        ))
        item = self.service.item("item1")
        self.assertEqual(item["effective_level"], "L0_MEMORY")
        self.assertEqual(item["highest_demonstrated_level"], "L6_SELF_CRITICISM")
        self.assertEqual(item["maturity_status"], "SUSPENDED_PENDING_REVALIDATION")

        self.service.apply(command(
            "revalidate_item", item_id="item1", evidence_ids=["evidence1"],
            reason="Rechecked scope against current evidence",
            review_due_at="2027-01-01T00:00:00Z",
        ))
        item = self.service.item("item1")
        self.assertEqual(item["effective_level"], "L6_SELF_CRITICISM")
        self.assertEqual(item["status"], "ACTIVE")

    def test_unknown_registry_resolves_and_reopens_on_valid_trigger(self):
        self.service.apply(command(
            "register_unknown", id="unknown1", domain_id="media",
            question="Will the relationship repeat?", materiality="HIGH",
            owner_impact="Changes whether another pilot is worth doing",
            review_due_at="2026-10-01T00:00:00Z",
        ))
        self.service.apply(command(
            "resolve_unknown", unknown_id="unknown1",
            answer="One observed result exists but repetition remains uncertain.",
            evidence_ids=["outcome1"],
        ))
        state = self.service.ledger.verify()[0]
        self.assertEqual(state["unknowns"]["unknown1"]["status"], "RESOLVED_DECLARED_EVIDENCE")
        self.service.apply(command(
            "reopen_unknown", unknown_id="unknown1", trigger="STALENESS",
            reason="Environment changed",
        ))
        self.assertEqual(self.service.ledger.verify()[0]["unknowns"]["unknown1"]["status"], "OPEN")

    def test_status_surfaces_due_review_and_provider_error_without_fake_score(self):
        self.register_item()
        self.service.apply(command(
            "register_unknown", id="unknown1", domain_id="media",
            question="What changed?", materiality="MEDIUM",
            owner_impact="May change next experiment",
            review_due_at="2026-01-01T00:00:00Z",
        ))
        self.service.apply(command(
            "record_provider_error", id="error1", domain_id="media",
            actor_ref="provider-family/model-version",
            task_class="forecast",
            severity="HIGH",
            description="Missed a material counterexample",
            evidence_ids=["evidence1"],
        ))
        status = self.service.status(now="2027-01-01T00:00:00Z")
        self.assertEqual(status["counts"]["provider_errors"], 1)
        self.assertIn("item1", status["review_due_items"])
        self.assertIn("unknown1", status["review_due_unknowns"])
        error = self.service.ledger.verify()[0]["provider_errors"]["error1"]
        self.assertEqual(error["status"], "OBSERVED_NOT_SCORED")

    def test_cross_domain_evidence_is_blocked(self):
        # Add a second domain/evidence directly to the historical core fixture via a normal ledger append.
        self.service.core.apply(command(
            "register_domain", id="other", name="Other", risk_class="NORMAL",
            measurement_contract="Other",
        ))
        self.service.core.apply(command(
            "record_source", id="other-source", domain_id="other", uri="internal://other",
            captured_at="2026-09-01T00:00:00Z", kind="FIRST_PARTY", rights_status="CLEAR",
        ))
        self.service.core.apply(command(
            "record_evidence", id="other-evidence", domain_id="other", source_id="other-source",
            statement="Other-domain evidence", observed_at="2026-09-01T00:00:00Z",
        ))
        self.register_item()
        with self.assertRaisesRegex(GateError, "cannot cross domain"):
            self.service.apply(command(
                "support_item", item_id="item1", evidence_ids=["other-evidence"],
                support_note="Wrong domain",
            ))

    def test_synthetic_outcome_cannot_claim_l5_validation(self):
        # The service enforces the non-synthetic reality gate. Use an intentionally mismatched
        # resolution reference to show resolution provenance is not caller-controlled.
        self.register_item()
        self.service.apply(command(
            "support_item", item_id="item1", evidence_ids=["evidence1"], support_note="Support",
        ))
        self.service.apply(command(
            "demonstrate_understanding", item_id="item1", explanation="Explain",
            distinction="Distinguish", expected_pattern="Pattern", falsifier="Falsifier",
        ))
        self.service.apply(command("link_prediction", item_id="item1", prediction_id="prediction1"))
        self.service.apply(command(
            "record_application", item_id="item1", mode="SHADOW_TEST",
            description="Bounded no-effect application", artifact_refs=[],
        ))
        with self.assertRaisesRegex(GateError, "Unknown resolutions ID"):
            self.service.apply(command(
                "record_validation", item_id="item1", resolution_id="fake-resolution",
                quality_note="Caller cannot invent outcome provenance",
            ))


if __name__ == "__main__":
    unittest.main()
