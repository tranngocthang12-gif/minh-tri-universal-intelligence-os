import json
import unittest
from pathlib import Path

from tools.score_master_blueprint_recovery_v9 import score_response

ROOT = Path(__file__).resolve().parents[1]


class RecoveryV9Tests(unittest.TestCase):
    def setUp(self):
        self.challenge = json.loads((ROOT / "eval/recovery/v9/challenge.json").read_text(encoding="utf-8"))
        self.packet = json.loads((ROOT / "eval/recovery/v9/packet.json").read_text(encoding="utf-8"))
        self.schema = json.loads((ROOT / "eval/recovery/v9/response.schema.json").read_text(encoding="utf-8"))
        self.snapshot = json.loads((ROOT / "eval/recovery/v9/historical_snapshot.json").read_text(encoding="utf-8"))
        self.current = json.loads((ROOT / "state/current.yaml").read_text(encoding="utf-8"))
        self.tasks = json.loads((ROOT / "state/tasks.yaml").read_text(encoding="utf-8"))

    def active_task(self):
        return next(t for t in self.tasks["tasks"] if t["task_id"] == self.current["active_task_id"])

    def valid_response(self):
        return {
            "schema": "minhtri-master-blueprint-recovery-response/v9",
            "challenge_id": self.snapshot["challenge_id"],
            "challenge_nonce": self.snapshot["challenge_nonce"],
            "attestations": {
                "separate_zero_chat": True,
                "used_prior_chat_history": False,
                "read_snapshot": False,
            },
            "recovered_facts": self.snapshot["expected_facts"],
            "evidence_refs": self.snapshot["required_evidence_refs"],
        }

    def test_valid_response_passes(self):
        self.assertEqual(score_response(self.valid_response())["status"], "PASS")

    def test_all_scorer_required_evidence_refs_are_public(self):
        required = set(self.snapshot["required_evidence_refs"])
        self.assertEqual(required, set(self.challenge["public_required_evidence_refs"]))
        self.assertEqual(required, set(self.packet["public_required_evidence_refs"]))

    def test_hidden_active_task_binding_is_preserved_at_proof_time(self):
        expected = self.snapshot["expected_facts"]["active_task"]
        c9_response = ROOT / "eval/recovery/v9/attempts/C9_response.json"
        c9_receipt = ROOT / "eval/recovery/v9/attempts/C9_receipt.json"

        if c9_response.is_file() and c9_receipt.is_file():
            response = json.loads(c9_response.read_text(encoding="utf-8"))
            receipt = json.loads(c9_receipt.read_text(encoding="utf-8"))
            self.assertEqual(expected, response["recovered_facts"]["active_task"])
            self.assertEqual(receipt["deterministic_score"], "PASS")
            self.assertTrue(receipt["completion_eligible"])
            self.assertEqual(
                receipt["main_sha"],
                self.packet["proof_target_main_sha_before_harness"].replace(
                    "58d3630678f1ac77c1af18fba3c7a66ae6606053",
                    "5c38243166339cd4e745c4e2b4b3ecfc2ae9bd0f",
                ),
            )
        else:
            active = self.active_task()
            self.assertEqual(expected["task_id"], active["task_id"])
            self.assertEqual(expected["status"], active["status"])
            self.assertEqual(expected["handoff_ref"], active["handoff_ref"])
            self.assertEqual(expected["blocker"], active["blocker"])
            self.assertEqual(expected["next_action"], active["next_action"])

    def test_hidden_active_task_uses_current_active_task_id_before_completion(self):
        c9_receipt = ROOT / "eval/recovery/v9/attempts/C9_receipt.json"
        if not c9_receipt.is_file():
            self.assertEqual(
                self.snapshot["expected_facts"]["active_task"]["task_id"],
                self.current["active_task_id"],
            )

    def test_missing_any_required_evidence_ref_fails(self):
        for ref in self.snapshot["required_evidence_refs"]:
            response = self.valid_response()
            response["evidence_refs"] = [x for x in response["evidence_refs"] if x != ref]
            result = score_response(response)
            self.assertEqual(result["status"], "FAIL", ref)
            self.assertTrue(any(ref in e for e in result["errors"]), ref)

    def test_expected_values_remain_out_of_public_contract(self):
        public_text = json.dumps(
            {"challenge": self.challenge, "packet": self.packet, "schema": self.schema},
            sort_keys=True,
        )
        self.assertNotIn(json.dumps(self.snapshot["expected_facts"], sort_keys=True), public_text)

    def test_c8_failure_is_preserved(self):
        score = json.loads((ROOT / "eval/recovery/v8/attempts/C8_score.json").read_text(encoding="utf-8"))
        receipt = json.loads((ROOT / "eval/recovery/v8/attempts/C8_receipt.json").read_text(encoding="utf-8"))
        self.assertEqual(score["status"], "FAIL")
        self.assertEqual(receipt["deterministic_score"], "FAIL")
        self.assertFalse(receipt["completion_eligible"])


if __name__ == "__main__":
    unittest.main()
