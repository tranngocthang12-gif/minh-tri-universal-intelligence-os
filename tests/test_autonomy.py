import unittest
from datetime import datetime, timezone
from unittest.mock import patch

from minhtri.autonomy import (
    RESEARCH_GATE_OPEN,
    RESEARCH_GATE_BLOCKED,
    AutonomyError,
    ProposalOnlyAutonomyRuntime,
    _derive_research_gate,
    automatic_critique_plan,
    autonomous_learning_plan,
    build_autonomy_packet,
    claims_without_review,
    meta_learning_report,
    learning_assurance_report,
    stratified_meta_learning_report,
    assurance_integrity_report,
    reasoning_context_report,
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

    def test_meta_learning_small_n_does_not_emit_candidate(self):
        state = base_state()
        state["resolutions"] = {
            "r1": {"interval_hit": False, "absolute_midpoint_error": 3},
            "r2": {"interval_hit": False, "absolute_midpoint_error": 5},
        }
        report = meta_learning_report(state)
        self.assertEqual(report["status"], "INSUFFICIENT_HISTORY")
        self.assertEqual(report["minimum_candidate_resolutions"], 50)
        self.assertEqual(report["lesson_candidates"], [])
        self.assertFalse(report["statistical_adaptation_proven"])

    def test_meta_learning_emits_candidate_only_at_conservative_floor(self):
        state = base_state()
        state["resolutions"] = {
            f"r{i}": {"interval_hit": False, "absolute_midpoint_error": 3 + (i % 2)}
            for i in range(50)
        }
        report = meta_learning_report(state, minimum_resolutions=2)
        self.assertEqual(report["status"], "ANALYZED")
        self.assertEqual(report["minimum_candidate_resolutions"], 50)
        self.assertTrue(report["lesson_candidates"])
        self.assertEqual(report["lesson_candidates"][0]["status"], "META_LESSON_CANDIDATE")
        self.assertEqual(report["permutation_test"], "REQUIRED_BEFORE_ADAPTATION")

    def test_learning_assurance_treats_external_cases_as_capital_only(self):
        state = base_state()
        state["external_cases"] = {
            "s": {"outcome": "SUCCESS", "capital_status": "EXTERNAL_CASE_CAPITAL_UNVERIFIED"},
            "f": {"outcome": "FAILURE", "capital_status": "EXTERNAL_CASE_CAPITAL_UNVERIFIED"},
        }
        report = learning_assurance_report(state)
        self.assertEqual(report["external_case_capital"]["count"], 2)
        self.assertEqual(report["external_case_capital"]["by_outcome"]["SUCCESS"], 1)
        self.assertEqual(report["external_case_capital"]["by_outcome"]["FAILURE"], 1)
        self.assertEqual(report["external_case_capital"]["promotion_status"], "CAPITAL_ONLY_NOT_LESSON_PROOF")
        self.assertFalse(report["automatic_verified_promotion"])
        self.assertFalse(report["automatic_trial_activation"])

    def test_autonomy_packet_includes_assurance_without_write_power(self):
        state = base_state()
        state["learning_packets"] = {"p": {"status": "FROZEN"}}
        packet = build_autonomy_packet(state, critic_provider_id="critic")
        self.assertEqual(packet["learning_assurance"]["frozen_learning_packets"], 1)
        self.assertFalse(packet["write_capability"])

    def test_stratified_meta_learning_keeps_domains_separate(self):
        state = base_state()
        state["procedures"]["proc1"] = {
            "id": "proc1", "domain_id": "d", "provider_id": "maker",
            "version": "1", "method": "bounded"
        }
        state["predictions"] = {
            "p1": {"id": "p1", "claim_id": "c", "procedure_id": "proc1"},
            "p2": {"id": "p2", "claim_id": "c", "procedure_id": "proc1"},
        }
        state["resolutions"] = {
            "r1": {
                "prediction_id": "p1", "domain_id": "d", "evidence_id": "e",
                "interval_hit": True, "absolute_midpoint_error": 1.0
            },
            "r2": {
                "prediction_id": "p2", "domain_id": "d", "evidence_id": "e",
                "interval_hit": False, "absolute_midpoint_error": 3.0
            },
        }
        report = stratified_meta_learning_report(state)
        self.assertEqual(report["by_domain"]["d"]["count"], 2)
        self.assertEqual(report["by_domain"]["d"]["status"], "INSUFFICIENT_HISTORY")
        self.assertEqual(report["by_procedure"]["proc1"]["count"], 2)
        self.assertEqual(report["minimum_candidate_resolutions_per_stratum"], 50)
        self.assertEqual(report["lesson_candidates"], [])
        self.assertEqual(report["permutation_test"], "REQUIRED_BEFORE_ADAPTATION")
        self.assertFalse(report["cross_domain_transfer_established"])
        self.assertFalse(report["automatic_rule_change"])

    def test_stratified_meta_learning_counts_failure_classes_without_fixing_them(self):
        state = base_state()
        state["learning_failures"] = {
            "f1": {"domain_id": "d", "failure_class": "CONFIRMATION_BIAS"},
            "f2": {"domain_id": "d", "failure_class": "CONFIRMATION_BIAS"},
            "f3": {"domain_id": "d", "failure_class": "TOOL_ERROR"},
        }
        report = stratified_meta_learning_report(state)
        self.assertEqual(report["failure_counts"]["CONFIRMATION_BIAS"], 2)
        self.assertEqual(report["failure_by_domain"]["d"]["TOOL_ERROR"], 1)
        self.assertFalse(report["automatic_rule_change"])

    def test_assurance_integrity_report_never_claims_full_independence(self):
        state = base_state()
        state["critic_independence_receipts"] = {
            "r1": {"status": "PROCESS_SEPARATED_EXTERNAL_EVIDENCE_RECORDED_NOT_FULL_INDEPENDENCE_PROOF"},
            "r2": {"status": "BLOCKED_SAME_RUNTIME"},
        }
        state["eval_integrity_assessments"] = {
            "e1": {"status": "EVAL_CONTAMINATION_SUSPECTED"},
            "e2": {"status": "CLEAN_NO_SIGNAL_NOT_PROOF"},
        }
        report = assurance_integrity_report(state)
        self.assertEqual(report["critic_independence_receipts"]["count"], 2)
        self.assertFalse(report["critic_independence_receipts"]["full_independence_proven"])
        self.assertFalse(
            report["eval_integrity_assessments"]["automatic_contamination_detection_proven"]
        )
        self.assertFalse(
            report["eval_integrity_assessments"]["automatic_reward_hacking_detection_proven"]
        )
        self.assertFalse(report["write_capability"])

    def test_autonomy_packet_exposes_integrity_without_write_power(self):
        state = base_state()
        state["eval_integrity_assessments"] = {
            "e1": {"status": "REWARD_HACKING_SUSPECTED"}
        }
        packet = build_autonomy_packet(state, critic_provider_id="critic")
        self.assertEqual(
            packet["assurance_integrity"]["eval_integrity_assessments"]["count"], 1
        )
        self.assertFalse(packet["assurance_integrity"]["write_capability"])
        self.assertFalse(packet["write_capability"])

    def test_reasoning_context_report_is_read_only_and_noncanonical(self):
        state = base_state()
        state["deliberation_plans"] = {"d1": {"effective_effort": "HIGH"}}
        state["research_traces"] = {"r1": {"source_role": "PRIMARY"}}
        state["context_capsules"] = {"c1": {"status": "CONTEXT_ONLY_NOT_CANONICAL_TRUTH"}}
        report = reasoning_context_report(state)
        self.assertEqual(report["deliberation_plans"]["by_effective_effort"]["HIGH"], 1)
        self.assertEqual(report["research_traces"]["by_source_role"]["PRIMARY"], 1)
        self.assertFalse(report["context_capsules"]["canonical_truth"])
        self.assertFalse(report["stores_chain_of_thought"])
        self.assertFalse(report["automatic_truth_promotion"])
        self.assertFalse(report["write_capability"])

    def test_autonomy_packet_exposes_reasoning_context_without_write_power(self):
        state = base_state()
        state["context_capsules"] = {"c1": {"status": "CONTEXT_ONLY_NOT_CANONICAL_TRUTH"}}
        packet = build_autonomy_packet(state, critic_provider_id="critic")
        self.assertEqual(packet["reasoning_context"]["context_capsules"]["count"], 1)
        self.assertFalse(packet["reasoning_context"]["write_capability"])
        self.assertFalse(packet["write_capability"])

    def test_research_is_fail_closed_before_gate(self):
        packet = build_autonomy_packet(
            base_state(),
            critic_provider_id="critic",
        )
        self.assertEqual(packet["research"]["status"], "BLOCKED")
        self.assertFalse(packet["write_capability"])
        self.assertFalse(packet["automatic_verified_promotion"])
        self.assertFalse(packet["automatic_trial_activation"])

    def test_research_open_without_adapter_still_does_not_invent_results(self):
        with patch("minhtri.autonomy.canonical_research_gate", return_value=RESEARCH_GATE_OPEN):
            packet = build_autonomy_packet(
                base_state(),
                critic_provider_id="critic",
            )
        self.assertEqual(packet["research"]["status"], "BLOCKED_NO_ADAPTER")

    def test_research_gate_derives_only_from_canonical_proofs(self):
        blocked = {
            "fresh_chat_seat_validation": "PENDING_SEPARATE_CHAT_UI",
            "fresh_chat_seat_validation_expires_at_utc": "2026-10-04T03:00:00Z",
            "end_to_end_seat_brain_transport": False,
            "research_adapter_gate": RESEARCH_GATE_OPEN,
            "current_runtime_liveness": {
                "secure_mcp_tunnel": "UP",
                "local_brain_connector": "UP",
            },
        }
        now = datetime(2026, 10, 4, 2, 0, tzinfo=timezone.utc)
        self.assertEqual(_derive_research_gate(blocked, now=now), RESEARCH_GATE_BLOCKED)

        opened = {
            "fresh_chat_seat_validation": "PASS",
            "fresh_chat_seat_validation_expires_at_utc": "2026-10-04T03:00:00Z",
            "end_to_end_seat_brain_transport": True,
            "research_adapter_gate": RESEARCH_GATE_OPEN,
            "current_runtime_liveness": {
                "secure_mcp_tunnel": "UP",
                "local_brain_connector": "UP",
            },
        }
        self.assertEqual(_derive_research_gate(opened, now=now), RESEARCH_GATE_OPEN)

        stale = dict(opened)
        stale["fresh_chat_seat_validation_expires_at_utc"] = "2026-10-04T01:59:59Z"
        self.assertEqual(_derive_research_gate(stale, now=now), RESEARCH_GATE_BLOCKED)

        down = dict(opened)
        down["current_runtime_liveness"] = {
            "secure_mcp_tunnel": "DOWN",
            "local_brain_connector": "DOWN",
        }
        self.assertEqual(_derive_research_gate(down, now=now), RESEARCH_GATE_BLOCKED)

    def test_cli_cannot_override_research_gate(self):
        from minhtri.autonomy import main

        with self.assertRaises(SystemExit):
            main(["--research-gate", RESEARCH_GATE_OPEN, "--once"])

    def test_due_prediction_becomes_read_only_action(self):
        state = base_state()
        state["predictions"]["pred"] = {
            "id": "pred", "claim_id": "c", "procedure_id": "proc",
            "due_at": "2026-01-02T00:00:00Z", "status": "FROZEN"
        }
        actions = autonomous_learning_plan(
            state,
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
