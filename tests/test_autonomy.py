import unittest
from datetime import datetime, timezone

from minhtri.autonomy import (
    RESEARCH_GATE_OPEN,
    AutonomyError,
    ProposalOnlyAutonomyRuntime,
    automatic_critique_plan,
    autonomous_learning_plan,
    build_autonomy_packet,
    claims_without_review,
    meta_learning_report,
    structural_critique,
)
from minhtri.core import initial_state


def base_state():
    state = initial_state()
    state["domains"]["d"] = {
        "id": "d", "name": "Domain", "risk_class": "NORMAL",
        "measurement_contract": "measure"
    }
    state["providers"]["maker"] = {"id": "maker", "name": "Maker", "kind": "MODEL"}
    state["providers"]["critic"] = {"id": "critic", "name": "Critic", "kind": "MODEL"}
    state["goals"]["g"] = {
        "id": "g", "domain_id": "d", "objective": "learn",
        "priority": 1, "owner_boundary": "owner", "status": "OPEN"
    }
    state["problems"]["p"] = {
        "id": "p", "goal_id": "g", "domain_id": "d", "reality": "r",
        "conditions": "c", "target": "t", "intervention": "i",
        "unknowns": "u", "control": "c", "influence": "i",
        "responsibility": "r", "harm_checks": "h"
    }
    state["sources"]["s"] = {
        "id": "s", "domain_id": "d", "uri": "internal://s",
        "captured_at": "2026-01-01T00:00:00Z",
        "kind": "FIRST_PARTY", "rights_status": "CLEAR"
    }
    state["evidence"]["e"] = {
        "id": "e", "domain_id": "d", "source_id": "s",
        "statement": "obs", "observed_at": "2026-01-01T00:00:00Z",
        "verification": "DECLARED_UNVERIFIED"
    }
    state["claims"]["c"] = {
        "id": "c", "problem_id": "p", "provider_id": "maker",
        "statement": "claim", "evidence_ids": ["e"],
        "alternative": "other", "falsifier": "test",
        "domain_id": "d", "epistemic_status": "HYPOTHESIS"
    }
    state["learning_focuses"] = {
        "f": {
            "id": "f", "status": "ACTIVE", "domain_id": "d",
            "source_id": "s", "note": "learn", "expected_lesson": "x",
            "uncertainty": "high"
        }
    }
    return state


class AutonomyTests(unittest.TestCase):
    def test_unreviewed_claim_is_detected(self):
        state = base_state()
        self.assertEqual(claims_without_review(state), ["c"])

    def test_structural_critic_never_auto_accepts(self):
        state = base_state()
        proposal = structural_critique(state, "c", "critic")
        self.assertFalse(proposal["automatic_acceptance"])
        self.assertNotEqual(
            proposal["review_command"]["data"]["verdict"],
            "ACCEPT_FOR_TRIAL",
        )

    def test_same_seat_critic_is_blocked(self):
        state = base_state()
        with self.assertRaises(AutonomyError):
            structural_critique(state, "c", "maker")

    def test_missing_critic_seat_blocks_automatic_critique(self):
        state = base_state()
        report = automatic_critique_plan(state, None)
        self.assertEqual(report["status"], "BLOCKED_NO_CRITIC_SEAT")
        self.assertEqual(report["proposals"], [])

    def test_meta_learning_requires_history(self):
        report = meta_learning_report(base_state())
        self.assertEqual(report["status"], "INSUFFICIENT_HISTORY")
        self.assertEqual(report["lesson_candidates"], [])

    def test_meta_learning_only_proposes_candidate(self):
        state = base_state()
        state["resolutions"] = {
            "r1": {"interval_hit": False, "absolute_midpoint_error": 3},
            "r2": {"interval_hit": False, "absolute_midpoint_error": 5},
        }
        report = meta_learning_report(state)
        self.assertEqual(report["status"], "ANALYZED")
        self.assertTrue(report["lesson_candidates"])
        self.assertEqual(
            report["lesson_candidates"][0]["status"],
            "META_LESSON_CANDIDATE",
        )

    def test_research_is_fail_closed_before_gate(self):
        packet = build_autonomy_packet(
            base_state(),
            critic_provider_id="critic",
            research_gate="BLOCKED_UNTIL_FRESH_SEAT_PASS",
        )
        self.assertEqual(packet["research"]["status"], "BLOCKED")
        self.assertFalse(packet["write_capability"])
        self.assertFalse(packet["automatic_verified_promotion"])
        self.assertFalse(packet["automatic_trial_activation"])

    def test_research_open_without_adapter_still_does_not_invent_results(self):
        packet = build_autonomy_packet(
            base_state(),
            critic_provider_id="critic",
            research_gate=RESEARCH_GATE_OPEN,
        )
        self.assertEqual(packet["research"]["status"], "BLOCKED_NO_ADAPTER")

    def test_due_prediction_becomes_read_only_action(self):
        state = base_state()
        state["predictions"]["pred"] = {
            "id": "pred", "claim_id": "c", "procedure_id": "proc",
            "due_at": "2026-01-02T00:00:00Z", "status": "FROZEN"
        }
        actions = autonomous_learning_plan(
            state,
            research_gate="BLOCKED_UNTIL_FRESH_SEAT_PASS",
            now=datetime(2026, 1, 3, tzinfo=timezone.utc),
        )
        due = next(a for a in actions if a["action"] == "AWAIT_OUTCOME_EVIDENCE")
        self.assertFalse(due["write_capability"])

    def test_runtime_tick_only_emits_packet(self):
        emitted = []
        runtime = ProposalOnlyAutonomyRuntime(
            state_loader=base_state,
            report_sink=emitted.append,
            critic_provider_id="critic",
        )
        packet = runtime.tick()
        self.assertEqual(len(emitted), 1)
        self.assertEqual(packet, emitted[0])
        self.assertFalse(packet["write_capability"])


if __name__ == "__main__":
    unittest.main()
