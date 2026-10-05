import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class VNextStateTaskTests(unittest.TestCase):
    def load_json_yaml(self, rel):
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))

    def test_current_state_is_small_and_has_explicit_authority_scope(self):
        current = self.load_json_yaml("state/current.yaml")
        self.assertEqual(current["schema"], "minhtri-current-state/v1")
        self.assertTrue(current["architecture_generation"].startswith("VNEXT_PHASE"))
        self.assertLessEqual(len(current), 20)
        scope = current["authority_scope"]
        self.assertTrue(scope["legacy_project_state_remains_authoritative_for_unmigrated_keys"])
        self.assertTrue(scope["duplicate_legacy_values_for_migrated_keys_are_non_authoritative_compatibility_only"])
        migrated = set(scope["this_file_is_authoritative_for"])
        self.assertIn("active_workstream", migrated)
        self.assertIn("next_checkpoint", migrated)
        self.assertIn("owner_learning_priority_order", migrated)

    def test_task_registry_is_single_vnext_task_truth(self):
        registry = self.load_json_yaml("state/tasks.yaml")
        self.assertEqual(registry["registry_authority"], "state/tasks.yaml")
        ids = [t["task_id"] for t in registry["tasks"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn("ARCH-VNEXT-PHASE2", ids)
        self.assertIn("BUDDHIST-A173", ids)
        self.assertIn("ARCH-VNEXT-PR-SALVAGE", ids)

    def test_every_task_has_minimum_contract(self):
        registry = self.load_json_yaml("state/tasks.yaml")
        allowed = set(registry["task_states"])
        for task in registry["tasks"]:
            self.assertIn(task["status"], allowed)
            self.assertIsInstance(task["scope"], list)
            self.assertGreater(len(task["scope"]), 0)
            self.assertIn("base_sha", task)
            self.assertIn(task["requires"], {"pc", "none"})
            self.assertIn("dependencies", task)
            self.assertIn("supersedes", task)

    def test_pc_bound_work_does_not_block_buddhist_learning(self):
        registry = self.load_json_yaml("state/tasks.yaml")
        tasks = {t["task_id"]: t for t in registry["tasks"]}
        self.assertEqual(tasks["RUNTIME-ASSURANCE-PC"]["status"], "BLOCKED")
        self.assertEqual(tasks["RUNTIME-ASSURANCE-PC"]["requires"], "pc")
        self.assertEqual(tasks["BUDDHIST-A173"]["requires"], "none")
        self.assertNotEqual(tasks["BUDDHIST-A173"]["status"], "BLOCKED")

    def test_vnext_architecture_is_canonical_target(self):
        current = self.load_json_yaml("state/current.yaml")
        self.assertEqual(
            current["current_architecture"],
            "docs/vnext/ARCHITECTURE_VNEXT_OWNER_APPROVED_CANDIDATE_20261006.md",
        )


if __name__ == "__main__":
    unittest.main()
