import json
import unittest
from pathlib import Path

from tools.score_master_blueprint_recovery_v8 import score_response

ROOT = Path(__file__).resolve().parents[1]


class RecoveryV8C8AttemptTests(unittest.TestCase):
    def test_c8_attempt_preserves_deterministic_fail(self):
        response = json.loads(
            (ROOT / "eval/recovery/v8/attempts/C8_response.json").read_text(
                encoding="utf-8"
            )
        )
        result = score_response(response)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["errors"], ["recovered_facts mismatch"])

    def test_c8_persisted_score_matches_scorer(self):
        response = json.loads(
            (ROOT / "eval/recovery/v8/attempts/C8_response.json").read_text(
                encoding="utf-8"
            )
        )
        persisted = json.loads(
            (ROOT / "eval/recovery/v8/attempts/C8_score.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(persisted, score_response(response))

    def test_c8_receipt_is_not_completion_eligible(self):
        receipt = json.loads(
            (ROOT / "eval/recovery/v8/attempts/C8_receipt.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(receipt["deterministic_score"], "FAIL")
        self.assertFalse(receipt["completion_eligible"])
        self.assertEqual(receipt["independence_provenance"], "PRESENT")


if __name__ == "__main__":
    unittest.main()
