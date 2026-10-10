"""Candidate carry-forward fixtures; not proof of actual future chat behavior."""
import copy
import hashlib
import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from minhtri.learning_prior_study import (
    PriorStudyError, make_carry_forward_plan, triage_against_prior,
    validate_working_prior_study,
)

ROOT = Path(__file__).resolve().parents[1]
PR341 = "2119d2bda13f90f08ab00b22aca7d413d3a5a9a1"
PR351 = "5c90bf810f3ff56af73b1046b851e972bfe988c6"
PR249 = "e0bf34be43ca87264914bfb9c25cfeb595815c51"
HEADS = {341: PR341, 351: PR351, 249: PR249}


def context():
    registry = json.loads((ROOT / "state/learning_tracks.json").read_text(encoding="utf-8"))
    track = registry["tracks"][0]
    study = json.loads((ROOT / "state/learning_prior_studies.json").read_text(encoding="utf-8"))
    pos = SimpleNamespace(track_id=track["track_id"],
                          checkpoint_id=track["checkpoint_id"],
                          cursor_id=study["working_cursor_id"],
                          next_question=study["working_question"],
                          proof="PR#341:comment#6096480057")
    return study, track, pos


def attempt(plan, mode="APPLICATION_EXAMPLE"):
    brief = plan["novelty_brief"]
    result = {
        "schema": "minhtri-learning-novelty-attempt/v1",
        "track_id": brief["track_id"],
        "checkpoint_id": brief["checkpoint_id"],
        "cursor_id": brief["cursor_id"],
        "question_sha256": hashlib.sha256(brief["exact_next_question"].encode()).hexdigest(),
        "mode": mode,
        "claim_keys_reused": ["bud:a173:retreat-does-not-prove-fear"],
        "claim_keys_added": [], "claim_keys_corrected": [],
        "new_primary_locators": [],
        "evidence_refs": ["PR#351:source-audit"],
        "application_case_refs": ["case:workplace-reporting"] if mode == "APPLICATION_EXAMPLE" else [],
        "answer_to_question": None, "counter_reading": None,
    }
    return result


class PriorStudyTests(unittest.TestCase):
    def test_01_carry_forward_reads_unmerged_claims_without_promoting(self):
        study, track, pos = context()
        plan = make_carry_forward_plan(study, track, pos, live_pr_heads=HEADS)
        self.assertEqual(plan["status"], "WORKING_STUDY_KNOWN_NOT_ACCEPTED")
        self.assertEqual(len(plan["prior_results"]), 5)
        self.assertEqual(plan["exact_next_question"], pos.next_question)
        self.assertFalse(plan["checkpoint_completed"])
        self.assertFalse(plan["owner_accepted"])

    def test_02_old_study_with_new_example_does_not_move(self):
        study, track, pos = context()
        plan = make_carry_forward_plan(study, track, pos, live_pr_heads=HEADS)
        x = triage_against_prior(study, track, pos, attempt(plan), live_pr_heads=HEADS)
        self.assertEqual(x["novelty"]["status"], "APPLICATION_ONLY_NO_ADVANCEMENT")
        self.assertFalse(x["cursor_may_advance"])

    def test_03_stale_pr_head_refused(self):
        study, track, pos = context()
        heads = dict(HEADS);heads[351] = "f"*40
        with self.assertRaisesRegex(PriorStudyError, "changed or unverified"):
            make_carry_forward_plan(study, track, pos, live_pr_heads=heads)

    def test_04_missing_prior_pr_refused(self):
        study, track, pos = context()
        with self.assertRaisesRegex(PriorStudyError, "changed or unverified"):
            make_carry_forward_plan(study, track, pos, live_pr_heads={341:PR341})

    def test_05_wrong_cursor_refused(self):
        study, track, pos = context()
        pos.cursor_id = "A173-WRONG"
        with self.assertRaisesRegex(PriorStudyError, "wrong working cursor"):
            make_carry_forward_plan(study, track, pos, live_pr_heads=HEADS)

    def test_06_research_from_a177_not_admitted_as_a173(self):
        study, track, pos = context()
        claim = copy.deepcopy(study["claims"][0])
        claim["claim_key"] = "bud:a173:a177-injected"
        claim["source_pr"] = 352
        study["claims"].append(claim)
        with self.assertRaisesRegex(PriorStudyError, "unpinned or mismatched PR"):
            validate_working_prior_study(study, track, pos, live_pr_heads=HEADS)

    def test_07_acceptance_claim_refused(self):
        study, track, pos = context()
        study["claims"][0]["review_status"] = "ACCEPTED"
        with self.assertRaisesRegex(PriorStudyError, "verified authority"):
            validate_working_prior_study(study, track, pos, live_pr_heads=HEADS)

    def test_08_comment_must_match_cursor(self):
        study, track, pos = context()
        study["claims"][0]["source_comment_id"] = 6096412284
        with self.assertRaisesRegex(PriorStudyError, "exact recovered cursor"):
            validate_working_prior_study(study, track, pos, live_pr_heads=HEADS)

    def test_09_empty_prior_inventory_blocked(self):
        study, track, pos = context()
        study["claims"] = []
        with self.assertRaisesRegex(PriorStudyError, "inventory is empty"):
            validate_working_prior_study(study, track, pos, live_pr_heads=HEADS)

    def test_10_loss_of_open_audits_blocked(self):
        study, track, pos = context()
        study["open_audits"] = []
        with self.assertRaisesRegex(PriorStudyError, "unresolved audits"):
            validate_working_prior_study(study, track, pos, live_pr_heads=HEADS)

    def test_11_path_traversal_rejected(self):
        study, track, pos = context()
        study["claims"][1]["source_path"] = "docs/learning/../../state/tasks.yaml"
        with self.assertRaisesRegex(PriorStudyError, "exact GitHub file"):
            validate_working_prior_study(study, track, pos, live_pr_heads=HEADS)

    def test_12_duplicate_claim_key_rejected(self):
        study, track, pos = context()
        study["claims"].append(copy.deepcopy(study["claims"][0]))
        with self.assertRaisesRegex(PriorStudyError, "duplicate or malformed"):
            validate_working_prior_study(study, track, pos, live_pr_heads=HEADS)

    def test_13_claim_blob_sha_must_be_valid(self):
        study, track, pos = context()
        study["claims"][1]["source_blob_sha"] = "UNPINNED"
        with self.assertRaisesRegex(PriorStudyError, "exact GitHub file"):
            validate_working_prior_study(study, track, pos, live_pr_heads=HEADS)

    def test_14_question_guard_remains_exact(self):
        study, track, pos = context()
        plan = make_carry_forward_plan(study, track, pos, live_pr_heads=HEADS)
        a = attempt(plan)
        a["question_sha256"] = "0"*64
        from minhtri.learning_novelty import LearningNoveltyError
        with self.assertRaisesRegex(LearningNoveltyError, "wrong active question"):
            triage_against_prior(study, track, pos, a, live_pr_heads=HEADS)


if __name__ == "__main__":
    unittest.main()
