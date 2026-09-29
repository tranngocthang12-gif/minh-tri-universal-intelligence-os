import tempfile
import unittest
from pathlib import Path

from minhtri.bottleneck import BottleneckService
from minhtri.core import GateError, Ledger
from minhtri.epistemic import EpistemicService


def command(command_type, **data):
    return {"type": command_type, "data": data}


class BottleneckGovernorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name) / "brain"

        self.core = Ledger(self.home)
        self.core.init()
        self.core.apply(command(
            "register_domain", id="media", name="Media", risk_class="NORMAL",
            measurement_contract="Observed outcome",
        ))
        self.core.apply(command(
            "open_goal", id="goal1", domain_id="media",
            objective="Reach a repeatable profitable media system",
            priority=5, owner_boundary="Research and shadow tests only",
        ))
        self.core.apply(command(
            "record_source", id="source1", domain_id="media", uri="internal://baseline",
            captured_at="2026-01-01T00:00:00Z", kind="FIRST_PARTY", rights_status="CLEAR",
        ))
        self.core.apply(command(
            "record_evidence", id="evidence1", domain_id="media", source_id="source1",
            statement="Baseline observation", observed_at="2026-01-01T00:00:00Z",
        ))

        self.epistemic = EpistemicService(self.home)
        self.epistemic.init()
        self.epistemic.apply(command(
            "register_item", id="audience-item", domain_id="media",
            subject="Audience fit", kind="INFERENCE", scope="Pilot only",
            origin_ref="baseline-note",
        ))
        self.epistemic.apply(command(
            "support_item", item_id="audience-item", evidence_ids=["evidence1"],
            support_note="Observed baseline",
        ))
        self.epistemic.apply(command(
            "register_unknown", id="format-unknown", domain_id="media",
            question="Which format has repeatable fit?", materiality="HIGH",
            owner_impact="Blocks repeatable growth",
        ))
        self.epistemic.apply(command(
            "register_unknown", id="packaging-unknown", domain_id="media",
            question="Which packaging improves discovery?", materiality="MEDIUM",
            owner_impact="May improve reach after format fit",
        ))

        self.governor = BottleneckService(self.home)
        self.governor.init()
        self.governor.apply(command(
            "create_plan", id="plan1", goal_id="goal1",
            target_state="Repeatable profitable media system",
            success_conditions=["format-fit", "packaging-fit", "unit-economics"],
            owner_constraints=["No publishing", "No spending"],
        ))

    def add_component(self, component_id, **overrides):
        data = dict(
            id=component_id,
            plan_id="plan1",
            name=component_id,
            supports_conditions=["format-fit"],
            dependency_ids=[],
            target_role="ENABLER",
            gap_kind="KNOWLEDGE_GAP",
            owner_impact="MEDIUM",
            decision_sensitivity="MEANINGFUL",
            information_gain="MEDIUM",
            cost_band="LOW",
            time_band="SHORT",
            risk_band="LOW",
            reversibility="REVERSIBLE",
            epistemic_item_ids=[],
            unknown_ids=["format-unknown"],
            allowed_evidence_ids=["evidence1"],
            leverage_hypothesis="Resolving this gap should improve the next decision.",
            disconfirming_condition="The decision remains unchanged after the gap is resolved.",
            next_unit_type="READ_ONLY_ANALYSIS",
            next_unit="Analyze the bounded gap.",
            acceptance="Produce evidence and a falsifiable conclusion.",
        )
        data.update(overrides)
        return self.governor.apply(command("add_component", **data))

    def test_selects_blocker_over_lower_role_without_fake_score(self):
        self.add_component(
            "format-blocker",
            target_role="BLOCKER",
            owner_impact="HIGH",
            decision_sensitivity="DECISION_CHANGING",
            information_gain="HIGH",
            cost_band="MEDIUM",
            time_band="MEDIUM",
            unknown_ids=["format-unknown"],
        )
        self.add_component(
            "packaging-optimizer",
            supports_conditions=["packaging-fit"],
            target_role="OPTIMIZER",
            owner_impact="CRITICAL",
            decision_sensitivity="DECISION_CHANGING",
            information_gain="HIGH",
            cost_band="LOW",
            time_band="SHORT",
            unknown_ids=["packaging-unknown"],
        )
        rec = self.governor.recommend("plan1")
        self.assertEqual(rec["decision"], "SELECT")
        self.assertEqual(rec["component_id"], "format-blocker")
        self.assertEqual(rec["selection_method"], "ORDINAL_LEXICOGRAPHIC_NO_CALIBRATED_SCORE")
        self.assertNotIn("score", rec)
        self.assertEqual(rec["task_candidate"]["unit_type"], "READ_ONLY_ANALYSIS")

    def test_dependency_blocks_downstream_until_upstream_is_satisfied(self):
        self.add_component(
            "audience-foundation",
            epistemic_item_ids=["audience-item"],
            unknown_ids=[],
            target_role="ENABLER",
            owner_impact="MEDIUM",
        )
        self.add_component(
            "format-blocker",
            dependency_ids=["audience-foundation"],
            target_role="BLOCKER",
            owner_impact="CRITICAL",
            decision_sensitivity="DECISION_CHANGING",
            information_gain="HIGH",
        )
        first = self.governor.recommend("plan1")
        self.assertEqual(first["component_id"], "audience-foundation")

        self.governor.apply(command(
            "set_component_status", component_id="audience-foundation",
            status="SATISFIED", reason="Baseline evidence is sufficient for this bounded dependency.",
            evidence_ids=["evidence1"],
        ))
        second = self.governor.recommend("plan1")
        self.assertEqual(second["component_id"], "format-blocker")

    def test_equal_top_candidates_hold_instead_of_arbitrary_choice(self):
        common = dict(
            target_role="BLOCKER",
            owner_impact="HIGH",
            decision_sensitivity="DECISION_CHANGING",
            information_gain="HIGH",
            cost_band="LOW",
            time_band="SHORT",
            risk_band="LOW",
            reversibility="REVERSIBLE",
            unknown_ids=["format-unknown"],
        )
        self.add_component("candidate-a", **common)
        self.add_component("candidate-b", **common)
        rec = self.governor.recommend("plan1")
        self.assertEqual(rec["decision"], "HOLD_AMBIGUOUS")
        self.assertIsNone(rec["component_id"])
        self.assertEqual(rec["candidate_ids"], ["candidate-a", "candidate-b"])
        self.assertIsNone(rec["task_candidate"])

    def test_wait_when_nothing_is_eligible_or_all_work_is_done(self):
        self.add_component("foundation", epistemic_item_ids=["audience-item"], unknown_ids=[])
        self.add_component("blocked-next", dependency_ids=["foundation"], target_role="BLOCKER")
        self.governor.apply(command(
            "set_component_status", component_id="foundation",
            status="HOLD", reason="Need a new source", evidence_ids=[],
        ))
        wait = self.governor.recommend("plan1")
        self.assertEqual(wait["decision"], "WAIT")
        self.assertEqual(wait["reason"], "WAIT_DEPENDENCIES_OR_HOLDS")

        self.governor.apply(command(
            "set_component_status", component_id="foundation",
            status="SATISFIED", reason="Evidence now adequate", evidence_ids=["evidence1"],
        ))
        self.governor.apply(command(
            "set_component_status", component_id="blocked-next",
            status="SATISFIED", reason="Gap resolved", evidence_ids=["evidence1"],
        ))
        done = self.governor.recommend("plan1")
        self.assertEqual(done["decision"], "WAIT")
        self.assertEqual(done["reason"], "ALL_COMPONENTS_SATISFIED_OR_NOT_APPLICABLE")

    def test_closed_owner_goal_blocks_recommendation(self):
        self.add_component("format-blocker", target_role="BLOCKER")
        self.core.apply(command(
            "set_goal_status", goal_id="goal1", status="BLOCKED",
            reason="Owner paused the goal",
        ))
        with self.assertRaisesRegex(GateError, "Owner goal is not OPEN"):
            self.governor.recommend("plan1")

    def test_cross_domain_epistemic_reference_is_blocked(self):
        self.core.apply(command(
            "register_domain", id="finance", name="Finance", risk_class="HIGH_STAKES",
            measurement_contract="Financial outcome",
        ))
        self.epistemic.apply(command(
            "register_unknown", id="finance-unknown", domain_id="finance",
            question="Finance question", materiality="HIGH",
            owner_impact="Finance only",
        ))
        with self.assertRaisesRegex(GateError, "cannot cross domain"):
            self.add_component("bad-cross-domain", unknown_ids=["finance-unknown"])

    def test_satisfied_requires_evidence_or_active_l2_plus_item(self):
        self.add_component(
            "weak-item",
            epistemic_item_ids=["audience-item"],
            unknown_ids=[],
            allowed_evidence_ids=[],
        )
        with self.assertRaisesRegex(GateError, "SATISFIED requires"):
            self.governor.apply(command(
                "set_component_status", component_id="weak-item",
                status="SATISFIED", reason="Wishful completion", evidence_ids=[],
            ))

        self.epistemic.apply(command(
            "demonstrate_understanding", item_id="audience-item",
            explanation="Audience response depends on the bounded context.",
            distinction="This is not the same as format fit.",
            expected_pattern="Similar audience signals should repeat in comparable samples.",
            falsifier="Comparable samples consistently show the opposite pattern.",
        ))
        self.governor.apply(command(
            "set_component_status", component_id="weak-item",
            status="SATISFIED", reason="Active L2 evidence chain supports this bounded dependency.",
            evidence_ids=[],
        ))

    def test_commit_focus_records_exact_heads_and_is_replayable(self):
        self.add_component(
            "format-blocker",
            target_role="BLOCKER",
            owner_impact="HIGH",
            decision_sensitivity="DECISION_CHANGING",
            information_gain="HIGH",
        )
        result = self.governor.commit_focus("plan1")
        rec = result["recommendation"]
        state = result["receipt"]["state"]
        focus = state["plans"]["plan1"]["last_focus"]
        self.assertEqual(focus["decision"], "SELECT")
        self.assertEqual(focus["component_id"], "format-blocker")
        self.assertEqual(focus["core_head"], rec["core_head"])
        self.assertEqual(focus["epistemic_head"], rec["epistemic_head"])
        self.assertEqual(focus["plan_head_before"], rec["plan_head"])
        self.assertEqual(len(focus["selection_snapshot_hash"]), 64)
        self.assertEqual(self.governor.ledger.verify()[1], result["receipt"]["event_count"])

    def test_recommendation_creates_task_candidate_but_not_canonical_task(self):
        self.add_component("format-blocker", target_role="BLOCKER")
        rec = self.governor.recommend("plan1")
        self.assertEqual(rec["decision"], "SELECT")
        self.assertIsNotNone(rec["task_candidate"])
        self.assertFalse((self.home / "tasks" / "events.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
