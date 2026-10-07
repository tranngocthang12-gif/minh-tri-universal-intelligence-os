import json
import unittest
from pathlib import Path

from tools.score_master_blueprint_recovery_v7 import score_response

ROOT = Path(__file__).resolve().parents[1]


class RecoveryV7C7AttemptTests(unittest.TestCase):
    def test_c7_attempt_preserves_deterministic_fail(self):
        response = json.loads(
            (ROOT / "eval/recovery/v7/attempts/C7_response.json").read_text(
                encoding="utf-8"
            )
        )
        result = score_response(response)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(
            result["errors"],
            ["missing required evidence refs: tools/score_master_blueprint_recovery_v7.py"],
        )

    def test_c7_persisted_score_matches_scorer(self):
        response = json.loads(
            (ROOT / "eval/recovery/v7/attempts/C7_response.json").read_text(
                encoding="utf-8"
            )
        )
        persisted = json.loads(
            (ROOT / "eval/recovery/v7/attempts/C7_score.json").read_text(
                encoding="utf-8"
            )
        )
        result = score_response(response)
        self.assertEqual(persisted, result)

    def test_c7_receipt_is_not_completion_eligible(self):
        receipt = json.loads(
            (ROOT / "eval/recovery/v7/attempts/C7_receipt.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(receipt["deterministic_score"], "FAIL")
        self.assertFalse(receipt["completion_eligible"])
        self.assertEqual(receipt["independence_provenance"], "PRESENT")


if __name__ == "__main__":
    unittest.main()
