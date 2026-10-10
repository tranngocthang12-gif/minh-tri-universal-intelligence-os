"""Negative controls for bounded understanding and independently scored trials."""
import copy
import unittest
from types import MappingProxyType

from minhtri.learning_capability import (
    CapabilityEvidenceError, summarize_transfer_trials, transfer_observation,
    validate_application_trial_binding, validate_semantic_skeleton,
    validate_transfer_trial,
)


def skeleton():
    return {
        "core_proposition": "Choosing whether to endure or avoid requires context.",
        "conditions": ["Identify the specific situation and consequence."],
        "mechanism_or_structure": "Compare context, proposed action and result.",
        "scope_boundary": "No source gives a universal instruction to face danger.",
        "non_claims": ["The source does not prove every withdrawal cowardly."],
        "uncertainty": "Pali parallels and multiple translations remain open.",
        "counter_reading": "Wording differences may come from text genre.",
        "source_vs_interpretation": "BOUNDED_SYNTHESIS",
    }


def trial(case="heldout:case001"):
    return {
        "schema": "minhtri-learning-transfer-trial/v1",
        "trial_ref": "trial:case001",
        "track_id": "BUDDHIST_THOUGHT",
        "candidate_cursor_id": "A173-Q03-01",
        "frozen_case_ref": case,
        "frozen_case_sha256": "a" * 64,
        "rubric_ref": "heldout:rubric001",
        "rubric_sha256": "b" * 64,
        "frozen_before_attempt_ref": "evidence:preregistered-before-responses",
        "baseline_attempt_ref": "evidence:unassisted",
        "candidate_attempt_ref": "evidence:using-recovered-knowledge",
        "independent_review_ref": "evidence:external-judgment",
        "generator_seat": "BUDDHIST_MAIN_SEAT",
        "reviewer_seat": "INDEPENDENT_REVIEWER_OTHER_SEAT",
        "baseline_score": 0.45,
        "candidate_score": 0.75,
        "baseline_safety_violations": 0,
        "candidate_safety_violations": 0,
        "status": "RECORDED_NOT_VERIFIED",
    }


def delta():
    return {
        "track_id": "BUDDHIST_THOUGHT",
        "cursor_id": "A173-Q03-01",
        "provenance": {"author_seat": "BUDDHIST_MAIN_SEAT"},
        "application": {
            "status": "INDEPENDENT_REVIEW_RECORDED_NOT_VERIFIED",
            "heldout_case_ref": "heldout:case001",
            "frozen_rubric_ref": "heldout:rubric001",
            "frozen_rubric_sha256": "b" * 64,
            "attempt_ref": "evidence:using-recovered-knowledge",
            "reviewer_seat": "INDEPENDENT_REVIEWER_OTHER_SEAT",
            "review_receipt_ref": "evidence:external-judgment",
            "transfer_trial_ref": "trial:case001",
        },
    }


class CapabilityEvidenceContractTests(unittest.TestCase):
    def test_01_semantic_skeleton_candidate(self):
        validate_semantic_skeleton(skeleton())

    def test_02_nonclaims_required(self):
        s = skeleton()
        s["non_claims"] = []
        with self.assertRaisesRegex(CapabilityEvidenceError, "non_claims"):
            validate_semantic_skeleton(s)

    def test_03_semantic_verified_self_claim_disallowed(self):
        s = skeleton()
        s["source_vs_interpretation"] = "VERIFIED"
        with self.assertRaisesRegex(CapabilityEvidenceError, "VERIFIED"):
            validate_semantic_skeleton(s)

    def test_04_trial_candidate_valid_schema(self):
        validate_transfer_trial(trial())

    def test_05_trial_cannot_self_review(self):
        t = trial()
        t["reviewer_seat"] = t["generator_seat"]
        with self.assertRaisesRegex(CapabilityEvidenceError, "self-reviewed"):
            validate_transfer_trial(t)

    def test_06_trial_cannot_self_promote(self):
        t = trial()
        t["status"] = "VERIFIED"
        with self.assertRaisesRegex(CapabilityEvidenceError, "VERIFIED"):
            validate_transfer_trial(t)

    def test_07_rubric_hash_required(self):
        t = trial()
        t["rubric_sha256"] = "invalid"
        with self.assertRaisesRegex(CapabilityEvidenceError, "rubric_sha256"):
            validate_transfer_trial(t)

    def test_08_attempts_must_be_distinct(self):
        t = trial()
        t["candidate_attempt_ref"] = t["baseline_attempt_ref"]
        with self.assertRaisesRegex(CapabilityEvidenceError, "separate"):
            validate_transfer_trial(t)

    def test_09_signal_never_promotes_skill(self):
        o = transfer_observation(trial())
        self.assertEqual(o["outcome"], "OBSERVED_SIGNAL_NOT_VERIFIED")
        self.assertFalse(o["skill_promoted"])
        self.assertFalse(o["actual_independence_verified"])
        self.assertFalse(o["causal_learning_proven"])

    def test_10_safety_regression_blocks_eligible_signal(self):
        t = trial()
        t["candidate_safety_violations"] = 1
        self.assertEqual(transfer_observation(t)["outcome"],
                         "NO_ELIGIBLE_SIGNAL_OBSERVED")

    def test_11_nonfinite_negative_and_boolean_scores_fail(self):
        for v in (-0.1, 1.1, float("inf"), float("nan"), True):
            with self.subTest(v=v):
                t = trial()
                t["candidate_score"] = v
                with self.assertRaisesRegex(CapabilityEvidenceError, "score"):
                    validate_transfer_trial(t)

    def test_12_shadow_field_rejected(self):
        t = trial()
        t["owner_approved"] = True
        with self.assertRaisesRegex(CapabilityEvidenceError, "shadow"):
            validate_transfer_trial(t)

    def test_13_trial_delta_evidence_join(self):
        validate_application_trial_binding(delta(), trial())

    def test_14_trial_from_other_cursor_cannot_be_misattached(self):
        t = trial()
        t["candidate_cursor_id"] = "A173-Q99"
        with self.assertRaisesRegex(CapabilityEvidenceError, "do not match"):
            validate_application_trial_binding(delta(), t)

    def test_15_trial_other_review_receipt_cannot_be_misattached(self):
        t = trial()
        t["independent_review_ref"] = "evidence:different-review"
        with self.assertRaisesRegex(CapabilityEvidenceError, "do not match"):
            validate_application_trial_binding(delta(), t)

    def test_16_unreviewed_delta_cannot_be_attached_to_trial(self):
        d = delta()
        d["application"]["status"] = "NOT_TESTED"
        with self.assertRaisesRegex(CapabilityEvidenceError, "no externally"):
            validate_application_trial_binding(d, trial())

    def test_17_two_distinct_cases_still_provisional(self):
        a, b = trial(), trial("heldout:case002")
        a["candidate_score"] = 0.65
        s = summarize_transfer_trials([a, b])
        self.assertEqual(s["cases"], 2)
        self.assertTrue(s["all_cases_improved_without_safety_regression"])
        self.assertFalse(s["skill_promoted"])
        self.assertFalse(s["independence_and_causal_effect_verified"])

    def test_18_duplicate_case_cannot_inflate_progress(self):
        with self.assertRaisesRegex(CapabilityEvidenceError, "duplicate held-out"):
            summarize_transfer_trials([trial(), trial()])

    def test_19_single_case_cannot_claim_multi_case(self):
        with self.assertRaisesRegex(CapabilityEvidenceError, "at least two"):
            summarize_transfer_trials([trial()])

    def test_20_multi_case_safety_regression_disqualifies(self):
        a, b = trial(), trial("heldout:case002")
        b["candidate_safety_violations"] = 1
        s = summarize_transfer_trials([a, b])
        self.assertFalse(s["all_cases_improved_without_safety_regression"])
        self.assertTrue(s["any_safety_regression"])


    def test_21_traversal_refs_rejected(self):
        for value in ("heldout:../key", "heldout:a/../key", "heldout:%2e%2e", "/etc/passwd", "file:///tmp"):
            with self.subTest(value=value):
                t = trial()
                t["frozen_case_ref"] = value
                with self.assertRaisesRegex(CapabilityEvidenceError, "unsafe"):
                    validate_transfer_trial(t)

    def test_22_mappingproxy_supported(self):
        validate_semantic_skeleton(MappingProxyType(skeleton()))
        validate_transfer_trial(MappingProxyType(trial()))

    def test_23_trial_identifier_bound_to_delta(self):
        d = delta()
        d["application"]["transfer_trial_ref"] = "trial:other"
        with self.assertRaisesRegex(CapabilityEvidenceError, "do not match"):
            validate_application_trial_binding(d, trial())

    def test_24_missing_binding_must_not_pass(self):
        d = delta()
        del d["track_id"]
        with self.assertRaisesRegex(CapabilityEvidenceError, "do not match"):
            validate_application_trial_binding(d, trial())

if __name__ == "__main__":
    unittest.main()
