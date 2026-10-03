import unittest

from minhtri.learning_experiment import (
    ExperimentContractError,
    assign_arm,
    validate_preregistration,
)


def prereg():
    return {
        "experiment_id": "trial-1",
        "frozen_at_utc": "2026-10-04T00:00:00Z",
        "primary_endpoint": "task_utility",
        "safety_endpoint": "unsupported_claim_rate",
        "primary_success_rule": "treatment > control",
        "safety_failure_rule": "unsupported_claim_rate must not worsen",
        "rollback_rule": "rollback on safety failure",
        "assignment_unit": "TASK_ID",
        "assignment_seed_hash": "a" * 64,
        "control_pipeline_hash": "b" * 64,
        "treatment_pipeline_hash": "c" * 64,
        "frozen_evaluator_hash": "d" * 64,
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
        self.assertEqual(assign_arm("task-1", "seed"), assign_arm("task-1", "seed"))
        self.assertIn(assign_arm("task-2", "seed"), {"CONTROL", "TREATMENT"})


if __name__ == "__main__":
    unittest.main()
