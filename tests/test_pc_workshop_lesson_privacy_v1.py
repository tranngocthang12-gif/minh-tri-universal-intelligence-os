"""Scope-bounded regression for Owner-approved PC learning; no machine liveness claims."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/learning/PC_WORKSHOP_LEARNING_PROGRAM_V1_20261009.md"
TASKS = ROOT / "state/tasks.yaml"

class PCWorkshopLessonPrivacyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = DOC.read_text(encoding="utf-8")
        registry = json.loads(TASKS.read_text(encoding="utf-8"))
        cls.task = next(t for t in registry["tasks"] if t["task_id"] == "PC-WORKSHOP-LEARNING-V1")

    def test_no_host_identifiers_or_runtime_counters_in_public_learning_doc(self):
        self.assertIsNone(re.search(r"\bWIN-[A-Z0-9]{5,}\b", self.doc))
        self.assertNotRegex(self.doc.lower(), r"event_count\s*[:=]")
        self.assertNotRegex(self.doc.lower(), r"local_brain_focus\s*[:=]")
        self.assertIn("excluded from the public learning record", self.doc)

    def test_theory_is_not_blocked_on_live_pc(self):
        self.assertEqual(self.task["requires"], "none")
        self.assertEqual(self.task["change_class"], "D")
        self.assertEqual(self.task["acceptance_authority"], "OWNER")
        self.assertEqual(self.task["pc_liveness_boundary"], "PC_WORKSHOP_THEORY_NOT_PC_DEPENDENT; LIVE_INVENTORY_SEPARATE_OWNER_DIRECTED_SCOPE")
        self.assertIn("any later read-only hardware inventory", self.task["next_action"])

    def test_truthful_checkpoint_and_recovery_handoff(self):
        self.assertIn("**TASK_ID:** PC-WORKSHOP-LEARNING-V1", self.doc)
        self.assertIn("Status: OWNER APPROVED LEARNING OBJECTIVE / CLASS D IMPLEMENTATION CANDIDATE / NOT YET MAIN", self.doc)
        self.assertIn("## NEXT ACTION\n"+self.task["next_action"], self.doc)
        self.assertIn("MACHINE_LEDGER: NOT WRITTEN.", self.doc)
        self.assertNotIn("LEARNING_PROVEN=TRUE", self.doc)
