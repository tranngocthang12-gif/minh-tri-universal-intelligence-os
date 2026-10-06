import copy
import json
import unittest
from pathlib import Path

from tools.score_zero_chat_recovery import score_response

ROOT = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def v3_response():
    return copy.deepcopy(load("eval/recovery/v3/attempts/C3_response.json"))


class RecoveryProofGateV3Tests(unittest.TestCase):
    def test_v3_historical_response_still_passes_after_current_task_transition(self):
        current = load("state/current.yaml")
        value = v3_response()
        self.assertNotEqual(
            value["recovered_facts"]["active_task"]["task_id"],
            current["active_task_id"],
        )
        result = score_response(value)
        self.assertEqual(result["status"], "PASS", result)
        self.assertFalse(result["prose_keyword_scoring"])

    def test_v3_same_facts_different_prose_same_result(self):
        a = v3_response()
        b = v3_response()
        a["answers"]["Q1"] = "A"
        b["answers"]["Q1"] = "Completely different wording."
        self.assertEqual(score_response(a)["status"], "PASS")
        self.assertEqual(score_response(b)["status"], "PASS")

    def test_v3_wrong_historical_task_status_fails(self):
        value = v3_response()
        value["recovered_facts"]["active_task"]["status"] = "DONE"
        result = score_response(value)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("active_task mismatch" in x for x in result["errors"]))

    def test_v3_wrong_source_file_fails(self):
        value = v3_response()
        value["recovered_facts"]["foundation_law"]["source_ref"] = "docs/OTHER.md#8-project-wide-continuity"
        result = score_response(value)
        self.assertEqual(result["status"], "FAIL")

    def test_v3_stale_nonce_fails(self):
        value = v3_response()
        value["challenge_nonce"] = "mtc2-6f1e2aa7985b4c4eaa52b4cd5d21d22f"
        result = score_response(value)
        self.assertEqual(result["status"], "FAIL")

    def test_v3_false_completion_claim_at_proof_time_fails(self):
        value = v3_response()
        value["recovered_facts"]["capability_truth"]["core_v1_complete"] = True
        result = score_response(value)
        self.assertEqual(result["status"], "FAIL")

    def test_v3_missing_evidence_fails(self):
        value = v3_response()
        value["evidence_refs"].remove("state/tasks.yaml")
        result = score_response(value)
        self.assertEqual(result["status"], "FAIL")

    def test_historical_snapshot_matches_merged_c3_response(self):
        snapshot = load("eval/recovery/v3/historical_snapshot.json")
        response = load("eval/recovery/v3/attempts/C3_response.json")
        self.assertEqual(snapshot["challenge_id"], response["challenge_id"])
        self.assertEqual(snapshot["challenge_nonce"], response["challenge_nonce"])
        self.assertEqual(snapshot["recovered_facts"], response["recovered_facts"])

    def test_c2_history_remains_fail(self):
        receipt = load("eval/recovery/v2/attempts/C2_receipt.json")
        self.assertEqual(receipt["deterministic_score"], "FAIL")
        self.assertFalse(receipt["completion_eligible"])

    def test_v3_completion_rule_requires_all_three(self):
        packet = load("eval/recovery/v3/packet.json")
        rule = packet["completion_rule"]
        self.assertTrue(rule["all_required"])
        self.assertEqual(rule["deterministic_score"], "PASS")
        self.assertEqual(rule["independence_provenance"], "PRESENT")
        self.assertTrue(rule["durable_receipt_merged"])


if __name__ == "__main__":
    unittest.main()
