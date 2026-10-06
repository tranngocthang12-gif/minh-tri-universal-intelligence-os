import json
import unittest
from pathlib import Path

from tools.score_zero_chat_recovery import score_response

ROOT = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


class TransitionSafeProofV1Tests(unittest.TestCase):
    def test_historical_c3_pass_survives_current_task_transition(self):
        current = load("state/current.yaml")
        response = load("eval/recovery/v3/attempts/C3_response.json")
        self.assertNotEqual(
            current["active_task_id"],
            response["recovered_facts"]["active_task"]["task_id"],
        )
        result = score_response(response)
        self.assertEqual(result["status"], "PASS", result)

    def test_historical_snapshot_is_bound_to_c3_receipt(self):
        snapshot = load("eval/recovery/v3/historical_snapshot.json")
        receipt = load("eval/recovery/v3/attempts/C3_receipt.json")
        self.assertEqual(snapshot["challenge_id"], receipt["challenge_id"])
        self.assertEqual(snapshot["challenge_nonce"], receipt["challenge_nonce"])
        self.assertEqual(snapshot["source_receipt_ref"], "eval/recovery/v3/attempts/C3_receipt.json")

    def test_active_handoff_is_current_not_historical(self):
        current = load("state/current.yaml")
        registry = load("state/tasks.yaml")
        task = next(t for t in registry["tasks"] if t["task_id"] == current["active_task_id"])
        text = (ROOT / task["handoff_ref"]).read_text(encoding="utf-8")
        self.assertIn(f"**TASK_ID:** {current['active_task_id']}", text)


if __name__ == "__main__":
    unittest.main()
