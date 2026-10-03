import unittest
from datetime import datetime, timezone

from minhtri.learning_experiment import (
    ExperimentContractError,
    paired_four_arm_order,
    validate_compute_telemetry,
    validate_preregistration,
)


def prereg():
    return {
        "experiment_id": "TRIAL-001-COUNTEREVIDENCE-FIRST",
        "frozen_at_utc": "2026-10-04T00:00:00Z",
        "primary_endpoint": "FACTUAL_ACCURACY",
        "safety_endpoint": "UNSUPPORTED_CLAIM_RATE",
        "coverage_endpoint": "GOLD_CLAIM_COVERAGE",
        "coverage_noninferiority_margin": 0.05,
        "primary_success_rule": "treatment > compute_matched",
        "safety_failure_rule": "unsupported_claim_rate must not worsen",
        "rollback_rule": "rollback on frozen safety threshold",
        "assignment_unit": "TASK_ID",
        "assignment_seed_hash": "a" * 64,
        "control_pipeline_hash": "b" * 64,
        "treatment_pipeline_hash": "c" * 64,
        "compute_matched_pipeline_hash": "d" * 64,
        "frozen_evaluator_hash": "e" * 64,
        "gold_labels_hash": "f" * 64,
        "baseline_definition": "V1_3",
        "compute_budget_contract": {
            "control": {"retrieval_calls": 1, "critic_calls": 1, "generator_calls": 1},
            "treatment": {"retrieval_calls": 2, "critic_calls": 2, "generator_calls": 1},
            "compute_matched": {"retrieval_calls": 2, "critic_calls": 2, "generator_calls": 1},
            "placebo": {"retrieval_calls": 2, "critic_calls": 2, "generator_calls": 1},
        },
        "compute_tolerance_fraction": 0.10,
        "placebo_overlay_id": "SHUFFLED_LEDGER_PLACEBO",
        "placebo_overlay_hash": "1" * 64,
        "placebo_provenance_hash": "2" * 64,
        "arm_mode": "PAIRED_FOUR_ARM",
        "primary_window_tasks": 30,
        "rollback_threshold": 0.05,
        "trial_rule_id": "lesson",
        "trial_rule_ttl_seconds": 3600,
        "routing_keys": ["domain_id", "procedure_id"],
    }


class LearningExperimentTests(unittest.TestCase):
    def test_preregistration_requires_three_endpoints_and_paired_four_arm(self):
        result = validate_preregistration(prereg())
        self.assertEqual(result["status"], "PREREGISTERED")
        self.assertEqual(result["arm_mode"], "PAIRED_FOUR_ARM")
        self.assertEqual(result["coverage_endpoint"], "GOLD_CLAIM_COVERAGE")
        self.assertTrue(result["metric_change_after_unblinding_invalidates_run"])

    def test_failure_class_cannot_route_trial(self):
        value = prereg()
        value["routing_keys"] = ["domain_id", "failure_class"]
        with self.assertRaises(ExperimentContractError):
            validate_preregistration(value)

    def test_paired_order_contains_all_four_arms_once_and_is_reproducible(self):
        kwargs = {
            "experiment_id": "TRIAL-001-COUNTEREVIDENCE-FIRST",
            "preregistration_hash": "9" * 64,
        }
        first = paired_four_arm_order("TASK-001", "secret", **kwargs)
        second = paired_four_arm_order("TASK-001", "secret", **kwargs)
        self.assertEqual(first, second)
        self.assertEqual(set(first), {"CONTROL", "TREATMENT", "COMPUTE_MATCHED", "PLACEBO"})
        self.assertEqual(len(first), 4)

    def test_compute_is_measured_after_execution(self):
        treatment = {
            "retrieval_calls": 2, "critic_calls": 2, "generator_calls": 1,
            "input_tokens": 1000, "output_tokens": 400, "retrieved_tokens": 800,
        }
        close = {
            "retrieval_calls": 2, "critic_calls": 2, "generator_calls": 1,
            "input_tokens": 1040, "output_tokens": 390, "retrieved_tokens": 820,
        }
        far = dict(close)
        far["input_tokens"] = 1400
        self.assertEqual(
            validate_compute_telemetry(treatment, close, tolerance_fraction=0.10)["status"],
            "COMPUTE_MATCHED",
        )
        mismatch = validate_compute_telemetry(treatment, far, tolerance_fraction=0.10)
        self.assertEqual(mismatch["status"], "COMPUTE_MISMATCH")
        self.assertFalse(mismatch["eligible_for_primary_analysis"])


class TrialRuleRuntimeTests(unittest.TestCase):
    def _state_with_rule(self, *, with_provenance=False, risk_class="NORMAL"):
        from minhtri.core import initial_state
        from minhtri.trial_rule_runtime import preregistration_digest
        state = initial_state()
        state["domains"]["media"] = {
            "id": "media", "name": "Media", "risk_class": risk_class,
            "measurement_contract": "utility",
        }
        state["providers"]["p"] = {"id": "p", "name": "P", "kind": "MODEL"}
        state["procedures"]["proc"] = {
            "id": "proc", "domain_id": "media", "provider_id": "p",
            "version": "1", "method": "bounded",
        }
        experiment = prereg()
        h = preregistration_digest(experiment)
        lesson = {
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
        if with_provenance:
            lesson["lesson_provenance"] = {
                "status": "AUDITED_LEDGER_DERIVED",
                "candidate_id": "meta-1",
                "resolution_ids": ["r1", "r2"],
                "strata": ["media/proc"],
                "derived_at": "2026-10-04T00:00:00Z",
            }
        state["lessons"]["lesson"] = lesson
        return state, experiment

    def _task(self):
        return {
            "task_id": "TASK-001",
            "domain_id": "media",
            "procedure_id": "proc",
            "task_content_sha256": "7" * 64,
        }

    def test_reader_compiles_same_task_into_four_isolated_plans(self):
        from minhtri.trial_rule_runtime import build_paired_trial_execution_plans
        state, experiment = self._state_with_rule()
        bundle = build_paired_trial_execution_plans(
            state, self._task(), experiment, assignment_secret="seed",
            now=datetime(2026, 10, 4, 0, 0, tzinfo=timezone.utc),
        )
        self.assertTrue(bundle["paired_same_task"])
        self.assertTrue(bundle["cache_isolation_required"])
        self.assertEqual(set(bundle["plans"]), {"CONTROL", "TREATMENT", "COMPUTE_MATCHED", "PLACEBO"})
        self.assertEqual(bundle["plans"]["TREATMENT"]["overlay_id"], "COUNTEREVIDENCE_FIRST")
        self.assertEqual(bundle["plans"]["PLACEBO"]["overlay_id"], "SHUFFLED_LEDGER_PLACEBO")
        self.assertIsNone(bundle["plans"]["COMPUTE_MATCHED"]["overlay_id"])
        self.assertFalse(bundle["learning_claim_eligible"])
        for plan in bundle["plans"].values():
            self.assertFalse(plan["write_capability"])
            self.assertEqual(plan["task_content_sha256"], "7" * 64)

    def test_learning_claim_requires_audited_lesson_provenance(self):
        from minhtri.trial_rule_runtime import build_paired_trial_execution_plans
        state, experiment = self._state_with_rule(with_provenance=True)
        bundle = build_paired_trial_execution_plans(
            state, self._task(), experiment, assignment_secret="seed",
            now=datetime(2026, 10, 4, 0, 0, tzinfo=timezone.utc),
        )
        self.assertTrue(bundle["learning_claim_eligible"])
        self.assertTrue(bundle["plans"]["TREATMENT"]["learning_claim_eligible"])

    def test_unknown_or_high_stakes_risk_fails_closed(self):
        from minhtri.trial_rule_runtime import TrialRuleRuntimeError, build_paired_trial_execution_plans
        for risk in (None, "HIGH_STAKES"):
            state, experiment = self._state_with_rule(risk_class=risk)
            with self.assertRaises(TrialRuleRuntimeError):
                build_paired_trial_execution_plans(
                    state, self._task(), experiment, assignment_secret="seed",
                    now=datetime(2026, 10, 4, 0, 0, tzinfo=timezone.utc),
                )

    def test_expired_trial_rule_fails_closed(self):
        from minhtri.trial_rule_runtime import TrialRuleRuntimeError, build_paired_trial_execution_plans
        state, experiment = self._state_with_rule()
        with self.assertRaises(TrialRuleRuntimeError):
            build_paired_trial_execution_plans(
                state, self._task(), experiment, assignment_secret="seed",
                now=datetime(2026, 10, 6, 0, 0, tzinfo=timezone.utc),
            )

    def test_single_arm_api_is_disabled(self):
        from minhtri.trial_rule_runtime import TrialRuleRuntimeError, build_trial_execution_plan
        with self.assertRaises(TrialRuleRuntimeError):
            build_trial_execution_plan()


if __name__ == "__main__":
    unittest.main()
