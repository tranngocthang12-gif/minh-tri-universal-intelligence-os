import unittest

from minhtri.evolution import (
    EVAL_BLOCKED,
    EVAL_ELIGIBLE,
    EVAL_NO_MEASURED_IMPROVEMENT,
    EvaluationSummary,
    compare_parent_candidate,
    frozen_evaluation_digest,
)


class EvolutionTests(unittest.TestCase):
    def packet(self):
        return frozen_evaluation_digest({
            "tasks": ["t1", "t2"],
            "rubric": ["correctness", "unsupported_claims", "utility"],
            "frozen": True,
        })

    def test_improved_candidate_is_only_eligible_for_owner_review(self):
        parent = EvaluationSummary(.80, .70, 3, 2, 1)
        candidate = EvaluationSummary(.85, .72, 2, 1, 0)
        result = compare_parent_candidate(parent, candidate, frozen_packet_digest=self.packet())
        self.assertEqual(result["verdict"], EVAL_ELIGIBLE)
        self.assertTrue(result["owner_decision_required"])
        self.assertFalse(result["automatic_candidate_promotion"])
        self.assertFalse(result["automatic_verified_promotion"])

    def test_any_security_or_boundary_regression_blocks(self):
        parent = EvaluationSummary(.80, .70, 3, 2, 1)
        candidate = EvaluationSummary(.95, .95, 0, 0, 0, security_regressions=1)
        result = compare_parent_candidate(parent, candidate, frozen_packet_digest=self.packet())
        self.assertEqual(result["verdict"], EVAL_BLOCKED)

    def test_quality_regression_blocks_even_if_other_metric_improves(self):
        parent = EvaluationSummary(.80, .70, 3, 2, 1)
        candidate = EvaluationSummary(.90, .60, 1, 1, 0)
        result = compare_parent_candidate(parent, candidate, frozen_packet_digest=self.packet())
        self.assertEqual(result["verdict"], EVAL_BLOCKED)

    def test_equal_candidate_has_no_measured_improvement(self):
        parent = EvaluationSummary(.80, .70, 3, 2, 1)
        result = compare_parent_candidate(parent, parent, frozen_packet_digest=self.packet())
        self.assertEqual(result["verdict"], EVAL_NO_MEASURED_IMPROVEMENT)


if __name__ == "__main__":
    unittest.main()
