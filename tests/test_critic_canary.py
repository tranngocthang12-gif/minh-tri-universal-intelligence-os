import unittest

from minhtri.critic_canary import (
    score_canary_case,
    summarize_canary_scores,
)


class CriticCanaryTests(unittest.TestCase):
    def test_subtle_defect_requires_localization(self):
        case = {
            "case_id": "c1",
            "class": "SUBTLE_EPISTEMIC",
            "ground_truth": {
                "has_defect": True,
                "defect_type": "CAUSAL_OVERCLAIM",
                "target_span": [20, 40],
            },
        }
        result = {
            "verdict": "DEFECT_FOUND",
            "findings": [{
                "defect_type": "CAUSAL_OVERCLAIM",
                "target_span": [25, 35],
                "falsification_reason": "observational evidence does not identify causality",
            }],
        }
        score = score_canary_case(case, result)
        self.assertTrue(score["correct_verdict"])
        self.assertTrue(score["localization_hit"])

    def test_wrong_span_is_not_localization_hit(self):
        case = {
            "case_id": "c1",
            "class": "SUBTLE_EPISTEMIC",
            "ground_truth": {
                "has_defect": True,
                "defect_type": "CAUSAL_OVERCLAIM",
                "target_span": [20, 40],
            },
        }
        result = {
            "verdict": "DEFECT_FOUND",
            "findings": [{
                "defect_type": "CAUSAL_OVERCLAIM",
                "target_span": [100, 120],
                "falsification_reason": "generic criticism",
            }],
        }
        score = score_canary_case(case, result)
        self.assertTrue(score["correct_verdict"])
        self.assertFalse(score["localization_hit"])

    def test_summary_reports_far_and_subtle_detection(self):
        rows = [
            {
                "case_id": "bad",
                "class": "SUBTLE_EPISTEMIC",
                "has_defect": True,
                "correct_verdict": True,
                "localization_hit": True,
                "accepted_bad_case": False,
                "rejected_clean_case": False,
                "subtle_error": True,
            },
            {
                "case_id": "clean",
                "class": "CLEAN",
                "has_defect": False,
                "correct_verdict": True,
                "localization_hit": True,
                "accepted_bad_case": False,
                "rejected_clean_case": False,
                "subtle_error": False,
            },
        ]
        report = summarize_canary_scores(
            rows,
            preregistered_max_far=0.10,
            preregistered_min_subtle_detection=0.80,
        )
        self.assertEqual(report["false_acceptance_rate"], 0.0)
        self.assertEqual(report["subtle_detection_rate"], 1.0)
        self.assertTrue(report["pass"])


if __name__ == "__main__":
    unittest.main()
