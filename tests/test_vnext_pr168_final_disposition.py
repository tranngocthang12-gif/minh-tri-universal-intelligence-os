import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PR168FinalDispositionTests(unittest.TestCase):
    def load(self, rel):
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))

    def test_final_disposition_preserves_truth_boundary(self):
        text = (ROOT / "docs" / "vnext" / "history" / "PR168_FINAL_DISPOSITION_20261006.md").read_text(encoding="utf-8")
        self.assertIn("REJECT_AS_CURRENT_STATE", text)
        self.assertIn("HISTORICAL_SYNTHESIS_ONLY", text)
        self.assertIn("DEFER_EXTRACT_UNTIL_CURRENT_TASK_NEEDS_IT", text)
        self.assertIn("does not mean", text)

    def test_wave4_is_done_and_final_disposition_is_active(self):
        tasks = self.load("state/tasks.yaml")
        by_id = {t["task_id"]: t for t in tasks["tasks"]}
        self.assertEqual(by_id["ARCH-VNEXT-SALVAGE-PR168-WAVE4"]["status"], "DONE")
        self.assertIn(
            by_id["ARCH-VNEXT-SALVAGE-PR168-FINAL-DISPOSITION"]["status"],
            {"IN_PROGRESS", "DONE"},
        )

    def test_pr169_salvage_is_registered_as_followup(self):
        tasks = self.load("state/tasks.yaml")
        by_id = {t["task_id"]: t for t in tasks["tasks"]}
        self.assertEqual(by_id["ARCH-VNEXT-SALVAGE-PR169"]["status"], "READY")

    def test_parent_pr168_task_is_not_marked_verified(self):
        tasks = self.load("state/tasks.yaml")
        by_id = {t["task_id"]: t for t in tasks["tasks"]}
        task = by_id["ARCH-VNEXT-SALVAGE-PR168"]
        self.assertIn(task["status"], {"REPORTED", "DONE"})
        self.assertNotIn("VERIFIED", task["status"])


if __name__ == "__main__":
    unittest.main()
