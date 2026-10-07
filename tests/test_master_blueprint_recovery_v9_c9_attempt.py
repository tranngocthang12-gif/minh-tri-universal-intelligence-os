import hashlib
import json
import unittest
from pathlib import Path

from tools.score_master_blueprint_recovery_v9 import score_response

ROOT = Path(__file__).resolve().parents[1]


class RecoveryV9C9AttemptTests(unittest.TestCase):
    def setUp(self):
        self.response = json.loads(
            (ROOT / "eval/recovery/v9/attempts/C9_response.json").read_text(
                encoding="utf-8"
            )
        )
        self.score = json.loads(
            (ROOT / "eval/recovery/v9/attempts/C9_score.json").read_text(
                encoding="utf-8"
            )
        )
        self.receipt = json.loads(
            (ROOT / "eval/recovery/v9/attempts/C9_receipt.json").read_text(
                encoding="utf-8"
            )
        )

    def test_c9_attempt_deterministic_grade(self):
        result = score_response(self.response)
        self.assertEqual(result["status"], "PASS", result)

    def test_c9_persisted_score_matches_scorer(self):
        self.assertEqual(self.score, score_response(self.response))

    def test_c9_receipt_is_completion_eligible(self):
        self.assertEqual(self.receipt["deterministic_score"], "PASS")
        self.assertEqual(self.receipt["independence_provenance"], "PRESENT")
        self.assertTrue(self.receipt["completion_eligible"])

    def test_c9_receipt_hash_matches_response(self):
        canonical = json.dumps(
            self.response,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        digest = hashlib.sha256(canonical).hexdigest()
        self.assertEqual(
            digest,
            self.receipt["response_sha256_canonical_json"],
        )

    def test_c9_receipt_targets_proof_main(self):
        self.assertEqual(
            self.receipt["main_sha"],
            "5c38243166339cd4e745c4e2b4b3ecfc2ae9bd0f",
        )


if __name__ == "__main__":
    unittest.main()
