import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class VNextBootstrapRootTests(unittest.TestCase):
    def load_json(self, rel):
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))

    def test_single_boot_root_resolves_vnext_state(self):
        boot = self.load_json("state/bootstrap.json")
        current = self.load_json(boot["current_state"])

        self.assertEqual(boot["status"], "CURRENT_BOOT_ROOT")
        self.assertEqual(boot["current_state"], "state/current.yaml")
        self.assertEqual(current["boot_root"], "state/bootstrap.json")
        self.assertEqual(current["task_registry"], "state/tasks.yaml")
        self.assertEqual(boot["task_registry"], current["task_registry"])

        self.assertTrue((ROOT / current["current_architecture"]).is_file())
        self.assertTrue((ROOT / current["law_precedence"]).is_file())
        self.assertTrue((ROOT / current["role_bootstrap"]).is_file())
        self.assertTrue((ROOT / boot["stable_learning_law"]).is_file())

    def test_legacy_surfaces_route_to_vnext_root(self):
        project_state = self.load_json("docs/PROJECT_STATE.json")
        recovery = self.load_json("docs/RECOVERY_MANIFEST.json")

        self.assertEqual(project_state["vnext_boot_root"], "state/bootstrap.json")
        self.assertEqual(project_state["vnext_current_state"], "state/current.yaml")
        self.assertEqual(project_state["vnext_task_registry"], "state/tasks.yaml")
        self.assertIn("COMPATIBILITY", project_state["current_architecture_legacy_pointer_status"])

        self.assertEqual(recovery["vnext_boot_root"], "state/bootstrap.json")
        self.assertEqual(recovery["vnext_current_state"], "state/current.yaml")
        self.assertEqual(recovery["vnext_task_registry"], "state/tasks.yaml")
        self.assertIn("COMPATIBILITY", recovery["legacy_authority_order_status"])

    def test_stable_bootstrap_docs_all_name_vnext_root(self):
        for rel in (
            "README.md",
            "docs/LAW_INDEX_20261003.md",
            "docs/LAW_UNIVERSAL_LEARNING_CONTINUITY_20261004.md",
            "docs/GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md",
        ):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("state/bootstrap.json", text, rel)
            self.assertIn("state/current.yaml", text, rel)

    def test_boot_root_targets_match_current_state(self):
        boot = self.load_json("state/bootstrap.json")
        current = self.load_json("state/current.yaml")
        mapping = boot["resolve_from_current_state"]

        self.assertEqual(mapping["current_architecture"], "current_architecture")
        self.assertEqual(mapping["law_precedence"], "law_precedence")
        self.assertEqual(mapping["role_bootstrap"], "role_bootstrap")

        for key in mapping.values():
            self.assertIn(key, current)
            self.assertTrue((ROOT / current[key]).is_file(), current[key])

    def test_legacy_cannot_override_migrated_state_by_contract(self):
        boot = self.load_json("state/bootstrap.json")
        current = self.load_json("state/current.yaml")
        scope = current["authority_scope"]

        self.assertTrue(boot["legacy_compatibility"]["must_not_override_migrated_current_state"])
        self.assertTrue(scope["duplicate_legacy_values_for_migrated_keys_are_non_authoritative_compatibility_only"])
        self.assertIn("current_architecture", scope["this_file_is_authoritative_for"])
        self.assertIn("law_precedence", scope["this_file_is_authoritative_for"])
        self.assertIn("boot_root", scope["this_file_is_authoritative_for"])
        self.assertIn("task_registry", scope["this_file_is_authoritative_for"])

    def test_boot_root_repair_task_is_registered(self):
        tasks = self.load_json("state/tasks.yaml")
        by_id = {t["task_id"]: t for t in tasks["tasks"]}
        task = by_id["ARCH-VNEXT-BOOT-ROOT"]
        self.assertEqual(task["status"], "REPORTED")
        self.assertEqual(task["branch"], "owner/vnext-boot-root-unification-20261006")
        self.assertEqual(task["requires"], "none")


if __name__ == "__main__":
    unittest.main()
