import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ArchitectureHandoffReconciliationTests(unittest.TestCase):
    def load_json(self, rel):
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))

    def test_current_state_no_longer_points_to_completed_wave4(self):
        current = self.load_json("state/current.yaml")
        self.assertEqual(
            current["active_workstream"],
            "ARCHITECTURE_VNEXT_PR168_FINAL_DISPOSITION_RECONCILIATION",
        )
        self.assertIn("CLOSE_STALE_PR273", current["next_checkpoint"])

    def test_wave4_done_and_final_disposition_active(self):
        reg = self.load_json("state/tasks.yaml")
        by_id = {t["task_id"]: t for t in reg["tasks"]}
        self.assertEqual(by_id["ARCH-VNEXT-SALVAGE-PR168-WAVE4"]["status"], "DONE")
        self.assertEqual(by_id["ARCH-VNEXT-SALVAGE-PR168-WAVE4"]["result_ref"], "PR#272")
        self.assertEqual(
            by_id["ARCH-VNEXT-SALVAGE-PR168-FINAL-DISPOSITION"]["status"],
            "IN_PROGRESS",
        )

    def test_foundation_law_and_handoff_tasks_are_registered(self):
        reg = self.load_json("state/tasks.yaml")
        by_id = {t["task_id"]: t for t in reg["tasks"]}
        self.assertEqual(by_id["ARCH-VNEXT-FOUNDATION-HANDOFF-LAW"]["status"], "DONE")
        self.assertEqual(
            by_id["ARCH-VNEXT-HANDOFF-RECONCILE-20261006"]["status"],
            "IN_PROGRESS",
        )
        self.assertIn("PR#273", by_id["ARCH-VNEXT-HANDOFF-RECONCILE-20261006"]["supersedes"])

    def test_handoff_contains_required_continuity_fields(self):
        text = (ROOT / "docs" / "vnext" / "handoff" / "ARCHITECTURE_HANDOFF_20261006.md").read_text(encoding="utf-8")
        for required in [
            "TASK_ID",
            "Owner objective",
            "Last verified canonical main SHA",
            "CANONICAL MAIN STATE",
            "WORKING CANDIDATE STATE",
            "DONE",
            "NOT DONE",
            "STALE / CONFLICTING STATE FOUND",
            "NEXT ACTION",
            "REQUIRED GATES",
            "PC / LOCAL BRAIN",
        ]:
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
