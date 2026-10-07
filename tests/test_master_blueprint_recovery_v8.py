import json
import unittest
from pathlib import Path

from tools.score_master_blueprint_recovery_v8 import score_response

ROOT = Path(__file__).resolve().parents[1]


class RecoveryV8Tests(unittest.TestCase):
    def setUp(self):
        self.challenge = json.loads((ROOT / "eval/recovery/v8/challenge.json").read_text(encoding="utf-8"))
        self.packet = json.loads((ROOT / "eval/recovery/v8/packet.json").read_text(encoding="utf-8"))
        self.schema = json.loads((ROOT / "eval/recovery/v8/response.schema.json").read_text(encoding="utf-8"))
        self.snapshot = json.loads((ROOT / "eval/recovery/v8/historical_snapshot.json").read_text(encoding="utf-8"))

    def valid_response(self):
        return {
            "schema": "minhtri-master-blueprint-recovery-response/v8",
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

    def test_public_contract_names_evidence_membership_requirement(self):
        self.assertTrue(self.challenge["required_rules"]["public_exact_evidence_membership"])
        self.assertGreaterEqual(
            self.schema["properties"]["evidence_refs"]["minItems"],
            len(self.snapshot["required_evidence_refs"]),
        )

    def test_missing_any_required_evidence_ref_fails(self):
        for ref in self.snapshot["required_evidence_refs"]:
            response = self.valid_response()
            response["evidence_refs"] = [x for x in response["evidence_refs"] if x != ref]
            result = score_response(response)
            self.assertEqual(result["status"], "FAIL", ref)
            self.assertIn(ref, result["errors"][0])

    def test_expected_values_remain_out_of_public_contract(self):
        public_text = json.dumps(
            {"challenge": self.challenge, "packet": self.packet, "schema": self.schema},
            sort_keys=True,
        )
        self.assertNotIn(json.dumps(self.snapshot["expected_facts"], sort_keys=True), public_text)

    def test_c7_failure_is_preserved(self):
        score = json.loads((ROOT / "eval/recovery/v7/attempts/C7_score.json").read_text(encoding="utf-8"))
        receipt = json.loads((ROOT / "eval/recovery/v7/attempts/C7_receipt.json").read_text(encoding="utf-8"))
        self.assertEqual(score["status"], "FAIL")
        self.assertEqual(receipt["deterministic_score"], "FAIL")
        self.assertFalse(receipt["completion_eligible"])


if __name__ == "__main__":
    unittest.main()
