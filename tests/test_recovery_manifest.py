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

    def test_transport_state_matches_implemented_capabilities(self):
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        self.assertTrue((ROOT / "src" / "minhtri" / "brain_transport.py").is_file())
        self.assertTrue((ROOT / "src" / "minhtri" / "brain_http.py").is_file())
        self.assertEqual(state["readonly_brain_transport_contract"], "IMPLEMENTED_AND_MERGED")
        self.assertEqual(state["readonly_brain_transport_dispatcher"], "IMPLEMENTED_AND_MERGED")
        self.assertEqual(state["brain_http_host"], "IMPLEMENTED_AND_MERGED")
        self.assertNotEqual(state["chatgpt_to_owner_pc_brain_connector"], "CONNECTED_READONLY")

    def test_published_anchor_state_has_canonical_witness_file(self):
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        if state["external_anchor_publication"]:
            witness = ROOT / state["first_owner_pc_external_anchor"]
            self.assertTrue(witness.is_file(), witness)
            data = json.loads(witness.read_text(encoding="utf-8"))
            self.assertEqual(data["anchor_id"], state["first_owner_pc_external_anchor_id"])
            self.assertEqual(state["first_owner_pc_external_anchor_readback"], "PASS_HISTORICAL_PREFIX_MATCH")

    def test_witness_scope_never_claims_full_device_independence_without_proof(self):
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(
            state["external_witness_independence_scope"],
            "PROCESS_SEPARATED_NOT_FULL_DEVICE_COMPROMISE_PROOF",
        )
        self.assertFalse(state["external_witness_full_device_independence"])
        self.assertIn("PROCESS_SEPARATED_ONLY", state["external_witness_threat_model"])

    def test_research_adapter_remains_blocked_before_runtime_recovery_gates(self):
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(
            state["research_adapter_gate"],
            "BLOCKED_UNTIL_READONLY_CONNECTOR_AND_FRESH_SEAT_PASS",
        )
        self.assertFalse(state["local_brain_connected"])
        self.assertFalse(state["end_to_end_seat_brain_transport"])


if __name__ == "__main__":
    unittest.main()
