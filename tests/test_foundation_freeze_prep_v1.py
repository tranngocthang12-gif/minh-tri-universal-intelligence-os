import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


class FoundationFreezePrepV1Tests(unittest.TestCase):
    def test_current_state_routes_to_consolidated_law(self):
        current = load("state/current.yaml")
        self.assertEqual(
            current["law_precedence"],
            "docs/vnext/FOUNDATION_LAW_CONSOLIDATED_V1_20261006.md",
        )
        self.assertTrue((ROOT / current["law_precedence"]).is_file())

    def test_retrieval_application_proof_is_durably_done(self):
        tasks = load("state/tasks.yaml")
        task = next(t for t in tasks["tasks"] if t["task_id"] == "ARCH-RETRIEVAL-APPLICATION-PROOF-V1")
        self.assertEqual(task["status"], "DONE")
        self.assertIn("PR#292", task["result_ref"])
        receipt = load("eval/retrieval_application/v1/results/FRESH_SEAT_001_receipt.json")
        self.assertEqual(receipt["deterministic_score"], "PASS")
        self.assertTrue(receipt["completion_eligible"])

    def test_law_consolidation_preserves_source_laws(self):
        text = (ROOT / "docs/vnext/FOUNDATION_LAW_CONSOLIDATED_V1_20261006.md").read_text(encoding="utf-8")
        for rel in [
            "docs/LAW_EVIDENCE_AND_HUMILITY_20261001.md",
            "docs/LAW_DYNAMIC_TOOLS_20261001.md",
            "docs/GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md",
            "docs/LAW_UNIVERSAL_LEARNING_CONTINUITY_20261004.md",
        ]:
            self.assertIn(rel, text)
            self.assertTrue((ROOT / rel).is_file())

    def test_baseline_requires_both_external_red_teams(self):
        baseline = load("docs/vnext/FOUNDATION_BASELINE_V1.json")
        gate = baseline["freeze_gate"]
        self.assertTrue(gate["claude_red_team_required"])
        self.assertTrue(gate["grok_red_team_required"])
        self.assertTrue(gate["material_defects_resolved_required"])
        self.assertEqual(baseline["status"], "CANDIDATE_PENDING_RED_TEAM_AND_FREEZE")

    def test_capability_truth_keeps_autonomous_runtimes_off(self):
        current = load("state/current.yaml")
        self.assertFalse(current["autonomous_learning_runtime"])
        self.assertFalse(current["automatic_self_critique_runtime"])
        self.assertFalse(current["meta_learning_runtime"])
        text = (ROOT / "docs/vnext/FOUNDATION_CAPABILITY_TRUTH_MATRIX_V1_20261006.md").read_text(encoding="utf-8")
        self.assertIn("OFF / NOT PROVEN", text)
        self.assertIn("PROVEN_FOR_FIXTURE_ONLY", text)

    def test_freeze_task_is_not_done_before_red_team(self):
        tasks = load("state/tasks.yaml")
        freeze = next(t for t in tasks["tasks"] if t["task_id"] == "ARCH-FOUNDATION-ACCEPTANCE-FREEZE-V1")
        self.assertEqual(freeze["status"], "IN_PROGRESS")
        self.assertEqual(freeze["blocker"], "CURRENT_BOOT_PATH_FRESH_SEAT_PROOF_AND_TWO_V2_RED_TEAM_RECEIPTS_REQUIRED")

    def test_architecture_reopen_rule_is_bounded(self):
        text = (ROOT / "docs/vnext/FOUNDATION_LAW_CONSOLIDATED_V1_20261006.md").read_text(encoding="utf-8")
        self.assertIn("measured evidence/test failure", text)
        self.assertIn("Owner explicitly changes a foundation objective", text)


if __name__ == "__main__":
    unittest.main()
