import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


class SingleBootRootV1Tests(unittest.TestCase):
    def test_boot_root_is_bound_to_current_state_and_registry(self):
        boot = load("state/bootstrap.json")
        current = load("state/current.yaml")
        self.assertEqual(boot["status"], "CURRENT_BOOT_ROOT")
        self.assertEqual(boot["durable_continuity_authority"], "GITHUB_PROTECTED_MAIN")
        self.assertEqual(boot["current_state"], current["boot_root"])
        self.assertEqual(boot["task_registry"], current["task_registry"])
        self.assertEqual(boot["task_registry"], "state/tasks.yaml")

    def test_required_boot_targets_exist(self):
        boot = load("state/bootstrap.json")
        for key in ["current_state", "task_registry", "law_index", "role_bootstrap", "recovery_entrypoint"]:
            self.assertTrue((ROOT / boot[key]).is_file(), key)

    def test_dynamic_current_pointers_exist(self):
        boot = load("state/bootstrap.json")
        current = load("state/current.yaml")
        self.assertTrue((ROOT / current["current_architecture"]).is_file())
        self.assertTrue((ROOT / current["law_precedence"]).is_file())
        self.assertEqual(
            boot["resolve_active_task_from"],
            "state/current.yaml:active_task_id",
        )

    def test_legacy_surfaces_cannot_override_migrated_state(self):
        boot = load("state/bootstrap.json")
        current = load("state/current.yaml")
        self.assertTrue(boot["legacy_must_not_override_migrated_state"])
        self.assertTrue(
            current["authority_scope"]["duplicate_legacy_values_for_migrated_keys_are_non_authoritative_compatibility_only"]
        )

    def test_stable_routes_name_single_boot_root(self):
        for rel in [
            "docs/GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md",
            "docs/LAW_INDEX_20261003.md",
            "docs/vnext/continuity/RECOVERY_ENTRYPOINT_V1.md",
        ]:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("state/bootstrap.json", text, rel)

    def test_active_task_resolves_through_registry_and_handoff(self):
        boot = load("state/bootstrap.json")
        current = load(boot["current_state"])
        tasks = load(boot["task_registry"])
        task = next(t for t in tasks["tasks"] if t["task_id"] == current["active_task_id"])
        self.assertTrue((ROOT / task["handoff_ref"]).is_file())
        self.assertTrue(task["next_action"])

    def test_missing_pointer_policy_is_fail_closed(self):
        boot = load("state/bootstrap.json")
        self.assertTrue(boot["fail_closed_on_missing_or_conflicting_required_pointer"])


if __name__ == "__main__":
    unittest.main()
