import unittest

from minhtri.learning_experiment import (
    ExperimentContractError,
    assign_arm,
    assign_block_arm,
    validate_preregistration,
)


def prereg():
    return {
        "experiment_id": "trial-1",
        "frozen_at_utc": "2026-10-04T00:00:00Z",
        "primary_endpoint": "task_utility",
        "safety_endpoint": "unsupported_claim_rate",
        "primary_success_rule": "treatment > compute_matched",
        "safety_failure_rule": "unsupported_claim_rate must not worsen",
        "rollback_rule": "rollback on safety failure",
        "assignment_unit": "TASK_ID",
        "assignment_seed_hash": "a" * 64,
        "control_pipeline_hash": "b" * 64,
        "treatment_pipeline_hash": "c" * 64,
        "compute_matched_pipeline_hash": "e" * 64,
        "frozen_evaluator_hash": "d" * 64,
        "gold_labels_hash": "f" * 64,
        "baseline_definition": "V1_3",
        "compute_budget_contract": {
            "control": {"retrieval_calls": 1, "critic_calls": 1},
            "treatment": {"retrieval_calls": 2, "critic_calls": 2},
            "compute_matched": {"retrieval_calls": 2, "critic_calls": 2},
        },
        "primary_window_tasks": 30,
        "rollback_threshold": 0.05,
        "trial_rule_id": "rule-1",
        "trial_rule_ttl_seconds": 3600,
        "routing_keys": ["domain_id", "procedure_id"],
    }


class LearningExperimentTests(unittest.TestCase):
    def test_preregistration_requires_primary_and_safety_endpoint(self):
        result = validate_preregistration(prereg())
        self.assertEqual(result["status"], "PREREGISTERED")
        self.assertTrue(result["metric_change_after_unblinding_invalidates_run"])

    def test_failure_class_cannot_route_first_trial(self):
        value = prereg()
        value["routing_keys"] = ["domain_id", "failure_class"]
        with self.assertRaises(ExperimentContractError):
            validate_preregistration(value)

    def test_assignment_is_deterministic_per_task_and_seed(self):
        self.assertEqual(assign_arm("TRIAL001-B01-T01", "seed"), assign_arm("TRIAL001-B01-T01", "seed"))
        self.assertIn(assign_arm("TRIAL001-B01-T02", "seed"), {"CONTROL", "TREATMENT", "COMPUTE_MATCHED"})


if __name__ == "__main__":
    unittest.main()


class TrialRuleRuntimeTests(unittest.TestCase):
    def _state_with_rule(self):
        from minhtri.core import initial_state
        from minhtri.trial_rule_runtime import preregistration_digest
        state = initial_state()
        state["domains"]["media"] = {
            "id": "media", "name": "Media", "risk_class": "NORMAL",
            "measurement_contract": "utility"
        }
        state["providers"]["p"] = {"id": "p", "name": "P", "kind": "MODEL"}
        state["procedures"]["proc"] = {
            "id": "proc", "domain_id": "media", "provider_id": "p",
            "version": "1", "method": "bounded"
        }
        experiment = prereg()
        h = preregistration_digest(experiment)
        state["lessons"]["lesson"] = {
            "id": "lesson",
            "domain_id": "media",
            "status": "TRIAL_RULE",
            "runtime_trial_status": "EXECUTABLE_DECLARATIVE_OVERLAY",
            "trial_spec_hash": "9" * 64,
            "trial_spec": {
                "experiment_id": experiment["experiment_id"],
                "preregistration_hash": h,
                "domain_id": "media",
                "procedure_id": "proc",
                "overlay_id": "COUNTEREVIDENCE_FIRST",
                "expires_at": "2026-10-05T00:00:00Z",
            },
        }
        return state, experiment

    def test_trial_rule_reader_is_read_only_and_arm_specific(self):
        from datetime import datetime, timezone
        from minhtri.trial_rule_runtime import build_trial_execution_plan
        state, experiment = self._state_with_rule()
        task = {"task_id": "TRIAL001-B01-T01", "domain_id": "media", "procedure_id": "proc"}
        plan = build_trial_execution_plan(
            state, task, experiment, assignment_secret="seed",
            now=datetime(2026, 10, 4, 0, 0, tzinfo=timezone.utc),
        )
        self.assertIn(plan["arm"], {"CONTROL", "TREATMENT", "COMPUTE_MATCHED"})
        self.assertFalse(plan["write_capability"])
        self.assertFalse(plan["automatic_verified_promotion"])
        if plan["arm"] == "TREATMENT":
            self.assertEqual(plan["overlay_id"], "COUNTEREVIDENCE_FIRST")
            self.assertTrue(plan["counterevidence_required"])
        else:
            self.assertIsNone(plan["overlay_id"])
            self.assertFalse(plan["counterevidence_required"])

    def test_expired_trial_rule_fails_closed(self):
        from datetime import datetime, timezone
        from minhtri.trial_rule_runtime import TrialRuleRuntimeError, build_trial_execution_plan
        state, experiment = self._state_with_rule()
        with self.assertRaises(TrialRuleRuntimeError):
            build_trial_execution_plan(
                state,
                {"task_id": "TRIAL001-B01-T01", "domain_id": "media", "procedure_id": "proc"},
                experiment,
                assignment_secret="seed",
                now=datetime(2026, 10, 6, 0, 0, tzinfo=timezone.utc),
            )

    def test_treatment_and_compute_matched_must_have_equal_budget(self):
        from datetime import datetime, timezone
        from minhtri.trial_rule_runtime import TrialRuleRuntimeError, build_trial_execution_plan
        state, experiment = self._state_with_rule()
        experiment["compute_budget_contract"]["compute_matched"] = {
            "retrieval_calls": 3, "critic_calls": 2
        }
        from minhtri.trial_rule_runtime import preregistration_digest
        state["lessons"]["lesson"]["trial_spec"]["preregistration_hash"] = preregistration_digest(experiment)
        with self.assertRaises(TrialRuleRuntimeError):
            build_trial_execution_plan(
                state,
                {"task_id": "TRIAL001-B01-T01", "domain_id": "media", "procedure_id": "proc"},
                experiment,
                assignment_secret="seed",
                now=datetime(2026, 10, 4, 0, 0, tzinfo=timezone.utc),
            )


class BlockRandomizationTests(unittest.TestCase):
    def test_each_block_has_exactly_two_of_each_arm(self):
        prereg_hash = "9" * 64
        arms = [
            assign_block_arm(
                f"TRIAL001-B01-T{i:02d}",
                "secret",
                experiment_id="TRIAL-001-COUNTEREVIDENCE-FIRST",
                preregistration_hash=prereg_hash,
            )
            for i in range(1, 7)
        ]
        self.assertEqual(arms.count("CONTROL"), 2)
        self.assertEqual(arms.count("TREATMENT"), 2)
        self.assertEqual(arms.count("COMPUTE_MATCHED"), 2)

    def test_block_assignment_is_reproducible(self):
        kwargs = {
            "experiment_id": "TRIAL-001-COUNTEREVIDENCE-FIRST",
            "preregistration_hash": "8" * 64,
        }
        first = [
            assign_block_arm(f"TRIAL001-B03-T{i:02d}", "secret", **kwargs)
            for i in range(1, 7)
        ]
        second = [
            assign_block_arm(f"TRIAL001-B03-T{i:02d}", "secret", **kwargs)
            for i in range(1, 7)
        ]
        self.assertEqual(first, second)
