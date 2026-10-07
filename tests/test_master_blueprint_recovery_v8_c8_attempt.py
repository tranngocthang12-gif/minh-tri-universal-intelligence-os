import json
import unittest
from pathlib import Path

from tools.score_master_blueprint_recovery_v8 import score_response

ROOT = Path(__file__).resolve().parents[1]


class RecoveryV8C8AttemptTests(unittest.TestCase):
    def test_c8_attempt_deterministic_grade(self):
        response = json.loads(
            (ROOT / "eval/recovery/v8/attempts/C8_response.json").read_text(
                encoding="utf-8"
            )
        )
        result = score_response(response)
        self.assertEqual(
            result["status"],
            "PASS",
            json.dumps(result, ensure_ascii=False, sort_keys=True),
        )


if __name__ == "__main__":
    unittest.main()
