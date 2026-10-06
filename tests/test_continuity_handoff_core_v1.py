import json
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ContinuityHandoffCoreV1Tests(unittest.TestCase):
    def load_json(self, rel):
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))

    def test_active_task_is_explicit_and_registered(self):
        current = self.load_json("state/current.yaml")
        registry = self.load_json("state/tasks.yaml")
        by_id = {t["task_id"]: t for t in registry["tasks"]}
        self.assertIn(current["active_task_id"], by_id)
        self.assertEqual(by_id[current["active_task_id"]]["status"], "BLOCKED")

    def test_active_task_has_machine_checkable_handoff_contract(self):
        registry = self.load_json("state/tasks.yaml")
        task = next(t for t in registry["tasks"] if t["task_id"] == "ARCH-VNEXT-CONTINUITY-HANDOFF-CORE-V1")
        for field in ["scope", "base_sha", "result_ref", "handoff_ref", "next_action", "blocker"]:
            self.assertIn(field, task)
        self.assertEqual(task["blocker"], "GENUINE_ZERO_CHAT_FRESH_SEAT_RECOVERY_PROOF_REQUIRED")
        self.assertTrue((ROOT / task["handoff_ref"]).exists())

    def test_handoff_task_id_matches_current_active_task(self):
        current = self.load_json("state/current.yaml")
        text = (ROOT / "docs" / "vnext" / "handoff" / "ARCHITECTURE_HANDOFF_20261006.md").read_text(encoding="utf-8")
        self.assertIn(f"**TASK_ID:** {current['active_task_id']}", text)
        for heading in ["## DONE BEFORE THIS TASK", "## NOT DONE", "## CURRENT TASK STATE", "## NEXT ACTION", "## REQUIRED GATES"]:
            self.assertIn(heading, text)

    def test_recovery_entrypoint_is_single_bounded_route(self):
        text = (ROOT / "docs" / "vnext" / "continuity" / "RECOVERY_ENTRYPOINT_V1.md").read_text(encoding="utf-8")
        for token in ["PROJECT_STATE.json", "LAW_INDEX", "state/current.yaml", "state/tasks.yaml", "active_task_id", "handoff_ref", "next_action"]:
            self.assertIn(token, text)
        self.assertNotIn("Local Brain is canonical", text)

    def test_validator_passes_repository_candidate(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "validate_continuity_handoff.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("CONTINUITY_HANDOFF_CORE_V1_PASS", proc.stdout)

    def test_zero_chat_packet_excludes_gold(self):
        packet = self.load_json("eval/recovery/v1/packet.json")
        self.assertTrue(packet["gold_excluded"])
        self.assertNotIn("eval/recovery/v1/gold.json", packet["canonical_inputs"])
        self.assertEqual(packet["questions_ref"], "eval/recovery/v1/questions.json")
        self.assertTrue(packet["authoring_seat_must_not_self_grade"])

    def test_gold_preserves_unproven_truth_boundary(self):
        gold = self.load_json("eval/recovery/v1/gold.json")
        forbidden = gold["required_facts"]["forbidden_claims"]
        self.assertIn("Core v1 COMPLETE before fresh-seat PASS", forbidden)
        self.assertIn("autonomous learning proven", forbidden)

    def test_blocked_architecture_task_has_continuation_metadata(self):
        registry = self.load_json("state/tasks.yaml")
        task = next(t for t in registry["tasks"] if t["task_id"] == "ARCH-VNEXT-PHASE4-GRADED-RUN")
        self.assertEqual(task["status"], "BLOCKED")
        self.assertTrue(task.get("blocker"))
        self.assertTrue(task.get("handoff_ref"))
        self.assertTrue(task.get("next_action"))


if __name__ == "__main__":
    unittest.main()
