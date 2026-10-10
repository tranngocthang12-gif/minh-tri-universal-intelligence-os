"""Negative and positive *synthetic* learning novelty probes, not understanding proof."""
import copy
import hashlib
import unittest
from types import SimpleNamespace

from minhtri.learning_novelty import (
    LearningNoveltyError, assess_learning_novelty, make_brief,
    validate_attempt, validate_brief,
)

SHA = "2119d2bda13f90f08ab00b22aca7d413d3a5a9a1"
QUESTION = (
    "Read original Pali MN 4 at the fear-and-posture episode and MN 2 "
    "sections 2-7. Compare exact lexical expressions and two translations, "
    "with a genre-based counter-reading, instead of repeating general summaries."
)
KNOWN = [
    "bud:a173:hiri-ottappa-guardians",
    "bud:a173:mn4-fear-training",
    "bud:a173:mn2-endure-or-avoid",
    "bud:a173:mn61-harm-review",
    "bud:a173:mil-nalagiri-discrepancy",
    "bud:a173:outward-act-not-inner-motive",
]
KNOWN_LOCI = ["mn2:4", "mn2:5", "mn4:fear-posture"]


def brief():
    pos = SimpleNamespace(
        track_id="BUDDHIST_THOUGHT", checkpoint_id="A173",
        cursor_id="A173-MN2-REPETITION-COUNTERREADING-03",
        next_question=QUESTION, proof="PR#341:comment#6096480057",
    )
    return make_brief(
        pos, inventory_source_ref="PR#341:comment#6096480057",
        known_claim_keys=KNOWN, known_primary_locators=KNOWN_LOCI,
        cursor_source_sha=SHA,
    )


def attempt(mode="RESTATEMENT"):
    b = brief()
    return {
        "schema": "minhtri-learning-novelty-attempt/v1",
        "track_id": b["track_id"], "checkpoint_id": b["checkpoint_id"],
        "cursor_id": b["cursor_id"],
        "question_sha256": hashlib.sha256(QUESTION.encode("utf-8")).hexdigest(),
        "mode": mode,
        "claim_keys_reused": [KNOWN[0], KNOWN[-1]],
        "claim_keys_added": [],
        "claim_keys_corrected": [],
        "new_primary_locators": [],
        "evidence_refs": ["PR#341:comment#6096480057"],
        "application_case_refs": [],
        "answer_to_question": None,
        "counter_reading": None,
    }


def new_attempt(mode="NEW_SOURCE_FINDING"):
    x = attempt(mode)
    x["claim_keys_added"] = ["bud:a173:mn4-exact-term-audit"]
    x["new_primary_locators"] = ["mn4:8:lexical-comparison"]
    x["evidence_refs"] = ["suttacentral:mn4:pli:passage8"]
    x["answer_to_question"] = (
        "A candidate passage-level observation compares exact MN 4 expressions "
        "with MN 2 and distinguishes the different speech situations."
    )
    x["counter_reading"] = (
        "The formula may be genre dependent rather than establish different mental mechanisms."
    )
    return x


class NoveltyGateTests(unittest.TestCase):
    def test_01_brief_pins_position_and_inventory(self):
        b = brief()
        self.assertEqual(b["cursor_source_sha"], SHA)
        self.assertEqual(b["cursor_id"], "A173-MN2-REPETITION-COUNTERREADING-03")
        validate_brief(b)

    def test_02_existing_summary_is_repeat(self):
        r = assess_learning_novelty(brief(), attempt())
        self.assertEqual(r["status"], "REPETITION_NO_ADVANCEMENT")
        self.assertFalse(r["candidate_delta_eligible"])
        self.assertEqual(r["next_question_if_no_progress"], QUESTION)

    def test_03_example_only_does_not_advance(self):
        a = attempt("APPLICATION_EXAMPLE")
        a["application_case_refs"] = ["hypothetical:workplace-reporting"]
        r = assess_learning_novelty(brief(), a)
        self.assertEqual(r["status"], "APPLICATION_ONLY_NO_ADVANCEMENT")
        self.assertFalse(r["candidate_delta_eligible"])

    def test_04_new_source_level_finding_is_provisional(self):
        r = assess_learning_novelty(brief(), new_attempt())
        self.assertEqual(r["status"], "NEW_EVIDENCE_CANDIDATE_NEEDS_SEMANTIC_REVIEW")
        self.assertTrue(r["candidate_delta_eligible"])
        self.assertFalse(r["semantic_novelty_verified"])
        self.assertTrue(r["independent_review_required"])

    def test_05_correction_is_not_new_knowledge_autopromotion(self):
        a = new_attempt("CORRECTION")
        a["claim_keys_added"] = []
        a["claim_keys_corrected"] = [KNOWN[2]]
        r = assess_learning_novelty(brief(), a)
        self.assertEqual(r["status"], "CORRECTION_CANDIDATE_NEEDS_SEMANTIC_REVIEW")
        self.assertFalse(r["checkpoint_completed"])

    def test_06_wrong_question_sha_fails(self):
        a = new_attempt()
        a["question_sha256"] = "f" * 64
        with self.assertRaisesRegex(LearningNoveltyError, "wrong active question"):
            assess_learning_novelty(brief(), a)

    def test_07_wrong_cursor_fails(self):
        a = new_attempt()
        a["cursor_id"] = "A177-OTHER"
        with self.assertRaisesRegex(LearningNoveltyError, "wrong recovered cursor"):
            assess_learning_novelty(brief(), a)

    def test_08_relabeling_known_claim_as_new_fails(self):
        a = new_attempt()
        a["claim_keys_added"] = [KNOWN[-1]]
        with self.assertRaisesRegex(LearningNoveltyError, "relabeled as new"):
            assess_learning_novelty(brief(), a)

    def test_09_old_primary_locus_relabeling_fails(self):
        a = new_attempt()
        a["new_primary_locators"] = [KNOWN_LOCI[2]]
        with self.assertRaisesRegex(LearningNoveltyError, "passage relabeled"):
            assess_learning_novelty(brief(), a)

    def test_10_corrected_claim_must_be_known(self):
        a = new_attempt("CORRECTION")
        a["claim_keys_added"] = []
        a["claim_keys_corrected"] = ["bud:a173:nonexistent"]
        with self.assertRaisesRegex(LearningNoveltyError, "previously studied claim"):
            assess_learning_novelty(brief(), a)

    def test_11_new_claim_without_new_locus_insufficient(self):
        a = new_attempt()
        a["new_primary_locators"] = []
        r = assess_learning_novelty(brief(), a)
        self.assertEqual(r["status"], "INSUFFICIENT_NOVELTY_NO_ADVANCEMENT")

    def test_12_new_locus_without_new_claim_insufficient(self):
        a = new_attempt()
        a["claim_keys_added"] = []
        r = assess_learning_novelty(brief(), a)
        self.assertFalse(r["candidate_delta_eligible"])

    def test_13_no_counterreading_insufficient(self):
        a = new_attempt()
        a["counter_reading"] = None
        r = assess_learning_novelty(brief(), a)
        self.assertFalse(r["candidate_delta_eligible"])

    def test_14_short_answer_insufficient(self):
        a = new_attempt()
        a["answer_to_question"] = "same as before"
        r = assess_learning_novelty(brief(), a)
        self.assertFalse(r["candidate_delta_eligible"])

    def test_15_no_evidence_ref_insufficient(self):
        a = new_attempt()
        a["evidence_refs"] = []
        r = assess_learning_novelty(brief(), a)
        self.assertFalse(r["candidate_delta_eligible"])

    def test_16_application_cannot_claim_new_source(self):
        a = new_attempt("APPLICATION_EXAMPLE")
        a["application_case_refs"] = ["hypothetical:workplace-reporting"]
        with self.assertRaisesRegex(LearningNoveltyError, "cannot silently"):
            assess_learning_novelty(brief(), a)

    def test_17_duplicate_claim_ids_rejected(self):
        a = new_attempt()
        a["claim_keys_added"] *= 2
        with self.assertRaisesRegex(LearningNoveltyError, "duplicate"):
            assess_learning_novelty(brief(), a)

    def test_18_empty_history_supported_for_new_program(self):
        b = brief()
        b["known_claim_keys"] = []
        b["known_primary_locators"] = []
        proposed = new_attempt()
        proposed["claim_keys_reused"] = []
        r = assess_learning_novelty(b, proposed)
        self.assertTrue(r["candidate_delta_eligible"])

    def test_19_restatement_with_new_locus_is_contradictory(self):
        a = attempt()
        a["new_primary_locators"] = ["mn4:8:lexical-comparison"]
        with self.assertRaisesRegex(LearningNoveltyError, "restatement cannot"):
            assess_learning_novelty(brief(), a)

    def test_20_new_source_mode_cannot_be_new_example_mode(self):
        a = new_attempt()
        a["application_case_refs"] = ["hypothetical:workplace"]
        with self.assertRaisesRegex(LearningNoveltyError, "confuse a new example"):
            assess_learning_novelty(brief(), a)

    def test_21_hidden_owner_approval_rejected(self):
        a = new_attempt()
        a["owner_accepted"] = True
        with self.assertRaisesRegex(LearningNoveltyError, "shadow"):
            assess_learning_novelty(brief(), a)

    def test_22_imaginary_new_label_does_not_prove_semantic_novelty(self):
        a = new_attempt()
        a["claim_keys_added"] = ["bud:a173:imaginary-new-label"]
        r = assess_learning_novelty(brief(), a)
        self.assertFalse(r["semantic_novelty_verified"])
        self.assertFalse(r["owner_accepted"])

    def test_23_cross_domain_research_attempt_rejected(self):
        a = new_attempt()
        a["track_id"] = "YOUTUBE"
        with self.assertRaisesRegex(LearningNoveltyError, "wrong recovered track_id"):
            assess_learning_novelty(brief(), a)

    def test_24_invalid_source_revision_rejected(self):
        b = brief()
        b["cursor_source_sha"] = "NOT_A_SHA"
        with self.assertRaisesRegex(LearningNoveltyError, "pin a revision"):
            assess_learning_novelty(b, attempt())

    def test_25_broken_question_sha_type_rejected(self):
        a = attempt()
        a["question_sha256"] = None
        with self.assertRaisesRegex(LearningNoveltyError, "SHA256"):
            validate_attempt(a)

    def test_26_no_new_records_do_not_imply_acceptance(self):
        for mode in ("RESTATEMENT", "APPLICATION_EXAMPLE"):
            with self.subTest(mode=mode):
                a = attempt(mode)
                if mode == "APPLICATION_EXAMPLE":
                    a["application_case_refs"] = ["hypothetical:case-02"]
                r = assess_learning_novelty(brief(), a)
                self.assertFalse(r["owner_accepted"])
                self.assertFalse(r["checkpoint_completed"])

if __name__ == "__main__":
    unittest.main()
