import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RecoveryManifestConsistency(unittest.TestCase):
    def test_authority_files_exist_and_state_matches_manifest(self):
        manifest = json.loads((ROOT / "docs" / "RECOVERY_MANIFEST.json").read_text(encoding="utf-8"))
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))

        self.assertEqual(manifest["project"], state["project"])
        for rel in manifest["authority_order"]:
            self.assertTrue((ROOT / rel).is_file(), rel)
        for key, expected in manifest["required_state"].items():
            self.assertIn(key, state)
            self.assertEqual(state[key], expected, key)

    def test_manifest_points_to_current_authority_files(self):
        manifest = json.loads((ROOT / "docs" / "RECOVERY_MANIFEST.json").read_text(encoding="utf-8"))
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["authority_order"][0], "docs/PROJECT_STATE.json")
        self.assertEqual(state["current_law_index"], manifest["authority_order"][1])
        self.assertEqual(state["current_architecture"], manifest["authority_order"][2])
        self.assertEqual(state["role_bootstrap"], manifest["authority_order"][3])


if __name__ == "__main__":
    unittest.main()
