import json
import unittest
from pathlib import Path

from tools.score_master_blueprint_recovery_v9 import score_response

ROOT = Path(__file__).resolve().parents[1]


class RecoveryV9C9AttemptTests(unittest.TestCase):
    def test_c9_attempt_deterministic_grade(self):
        response = json.loads(
            (ROOT / "eval/recovery/v9/attempts/C9_response.json").read_text(
                encoding="utf-8"
            )
        )
        result = score_response(response)
        self.assertEqual(result["status"], "PASS", result)


if __name__ == "__main__":
    unittest.main()
