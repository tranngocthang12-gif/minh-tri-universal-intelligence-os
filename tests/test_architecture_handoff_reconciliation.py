import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ArchitectureHandoffReconciliationTests(unittest.TestCase):
    def load_json(self, rel):
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))

    def test_current_state_advances_to_pr169(self):
        current = self.load_json("state/current.yaml")
        self.assertEqual(
            current["active_workstream"],
            "ARCHITECTURE_VNEXT_PR_SALVAGE_PR169_READY",
        )
        self.assertIn("START_CONTROLLED_SALVAGE_PR169", current["next_checkpoint"])

    def test_pr168_lifecycle_is_closed_and_pr169_ready(self):
        reg = self.load_json("state/tasks.yaml")
        by_id = {t["task_id"]: t for t in reg["tasks"]}
        self.assertEqual(by_id["ARCH-VNEXT-SALVAGE-PR168-WAVE4"]["status"], "DONE")
        self.assertEqual(by_id["ARCH-VNEXT-SALVAGE-PR168-FINAL-DISPOSITION"]["status"], "DONE")
        self.assertEqual(by_id["ARCH-VNEXT-SALVAGE-PR168"]["status"], "DONE")
        self.assertEqual(by_id["ARCH-VNEXT-HANDOFF-RECONCILE-20261006"]["status"], "DONE")
        self.assertEqual(by_id["ARCH-VNEXT-SALVAGE-PR169"]["status"], "READY")

    def test_foundation_handoff_law_task_remains_done(self):
        reg = self.load_json("state/tasks.yaml")
        by_id = {t["task_id"]: t for t in reg["tasks"]}
        self.assertEqual(by_id["ARCH-VNEXT-FOUNDATION-HANDOFF-LAW"]["status"], "DONE")
        self.assertIn("PR#275", by_id["ARCH-VNEXT-FOUNDATION-HANDOFF-LAW"]["result_ref"])

    def test_handoff_contains_required_post_closure_fields(self):
        text = (ROOT / "docs" / "vnext" / "handoff" / "ARCHITECTURE_HANDOFF_20261006.md").read_text(encoding="utf-8")
        for required in [
            "TASK_ID",
            "Owner objective",
            "Last verified canonical main SHA",
            "CANONICAL MAIN STATE",
            "DONE",
            "NOT DONE",
            "CURRENT TASK STATE",
            "TRUTH BOUNDARY",
            "NEXT ACTION",
            "REQUIRED GATES",
            "PC / LOCAL BRAIN",
            "ARCH-VNEXT-SALVAGE-PR169",
        ]:
            self.assertIn(required, text)

    def test_handoff_preserves_zero_chat_truth_boundary(self):
        text = (ROOT / "docs" / "vnext" / "handoff" / "ARCHITECTURE_HANDOFF_20261006.md").read_text(encoding="utf-8")
        self.assertIn("Genuine zero-chat continuation proof", text)
        self.assertIn("has not yet passed", text)
        self.assertIn("Closed PR != verified knowledge", text)


if __name__ == "__main__":
    unittest.main()
