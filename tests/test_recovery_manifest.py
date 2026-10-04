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
        self.assertEqual(state["universal_learning_continuity_law"], manifest["authority_order"][2])
        self.assertEqual(state["current_architecture"], manifest["authority_order"][3])
        self.assertEqual(state["role_bootstrap"], manifest["authority_order"][4])

    def test_transport_state_matches_implemented_capabilities(self):
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        self.assertTrue((ROOT / "src" / "minhtri" / "brain_transport.py").is_file())
        self.assertTrue((ROOT / "src" / "minhtri" / "brain_http.py").is_file())
        self.assertEqual(state["readonly_brain_transport_contract"], "IMPLEMENTED_AND_MERGED")
        self.assertEqual(state["readonly_brain_transport_dispatcher"], "IMPLEMENTED_AND_MERGED")
        self.assertEqual(state["brain_http_host"], "IMPLEMENTED_AND_MERGED")
        if state["local_brain_connected"]:
            self.assertEqual(state["chatgpt_to_owner_pc_brain_connector"], "CONNECTED_READONLY")

    def test_published_anchor_state_has_canonical_witness_file(self):
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        if state["external_anchor_publication"]:
            witness = ROOT / state["first_owner_pc_external_anchor"]
            self.assertTrue(witness.is_file(), witness)
            data = json.loads(witness.read_text(encoding="utf-8"))
            self.assertEqual(data["anchor_id"], state["first_owner_pc_external_anchor_id"])
            self.assertEqual(state["first_owner_pc_external_anchor_readback"], "PASS_HISTORICAL_PREFIX_MATCH")

    def test_independent_publication_fails_closed_without_independent_authority(self):
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        if not state["external_witness_full_device_independence"]:
            self.assertFalse(state["external_anchor_publication"])
        self.assertTrue(state["same_authority_github_anchor_published"])
        self.assertIn("NOT_INDEPENDENT_WITNESS", state["external_witness_publication_authority"])

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
            "BLOCKED_UNTIL_FRESH_SEAT_PASS",
        )
        self.assertTrue(state["local_brain_connected"])
        self.assertEqual(state["research_adapter_gate"], "BLOCKED_UNTIL_FRESH_SEAT_PASS")
        self.assertFalse(state["end_to_end_seat_brain_transport"])

    def test_runtime_evidence_is_separate_from_liveness(self):
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(state["runtime_state_model_version"], "V2_EVIDENCE_PLUS_LIVENESS")
        self.assertIn("last_proven_runtime_evidence", state)
        self.assertIn("current_runtime_liveness", state)
        self.assertEqual(
            state["last_proven_runtime_evidence"]["persistence"],
            "NOT_PROVEN",
        )
        liveness = state["current_runtime_liveness"]
        self.assertIn(liveness["secure_mcp_tunnel"], {"UP", "DOWN", "UNKNOWN"})
        self.assertIn(liveness["local_brain_connector"], {"UP", "DOWN", "UNKNOWN"})
        self.assertIsInstance(liveness.get("evidence"), list)
        if liveness["secure_mcp_tunnel"] == "UP":
            self.assertEqual(liveness["local_brain_connector"], "UP")
            self.assertGreater(len(liveness["evidence"]), 0)
        if liveness["secure_mcp_tunnel"] == "DOWN":
            self.assertNotEqual(liveness["local_brain_connector"], "UP")
        self.assertEqual(
            state["runtime_liveness_authoritative_field"],
            "current_runtime_liveness",
        )
        self.assertFalse(state["legacy_runtime_current_fields_liveness_authority"])

    def test_research_gate_source_is_canonical_and_fail_closed(self):
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(
            state["research_adapter_gate_source"],
            "CANONICAL_PROJECT_STATE_ONLY_FAIL_CLOSED",
        )
        self.assertEqual(state["research_adapter_gate"], "BLOCKED_UNTIL_FRESH_SEAT_PASS")
        self.assertFalse(state["end_to_end_seat_brain_transport"])

    def test_independent_witness_promotion_is_blocked_without_independent_authority(self):
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        self.assertFalse(state["external_witness_full_device_independence"])
        self.assertEqual(
            state["independent_witness_interface_gate"],
            "BLOCKED_NO_INDEPENDENT_AUTHORITY_PROVIDER_CREDENTIAL",
        )

    def test_secure_mcp_tunnel_is_required_before_chatgpt_connector(self):
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        self.assertTrue(state["secure_mcp_tunnel_required"])
        self.assertIn(
            state["secure_mcp_tunnel_status"],
            {
                "NOT_PROVISIONED",
                "RUNTIME_PRECHECK_FIXED_AWAITING_RERUN",
                "READY",
            },
        )
        if state["secure_mcp_tunnel_status"] != "READY":
            self.assertEqual(
                state["chatgpt_custom_readonly_connector_registration"],
                "BLOCKED_UNTIL_SECURE_MCP_TUNNEL_PROVISIONED",
            )
            self.assertFalse(state["local_brain_connected"])

    def test_runtime_planes_are_separated(self):
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(state["runtime_plane_model"], "FORMALIZED_V1")
        self.assertIn("SECURE_MCP", state["brain_read_plane"])
        self.assertIn("OWNER_GATED_LEDGER_MUTATION", state["brain_write_plane"])
        self.assertIn("BREAK_GLASS", state["maintenance_plane"])
        self.assertFalse(state["desktop_commander_can_prove_readonly_connector"])

    def test_connector_promotion_gates_fail_closed(self):
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        self.assertTrue(state["connector_promotion_requires_secure_path"])
        self.assertTrue(state["end_to_end_promotion_requires_exact_readonly_toolset_and_fresh_seat"])
        if state["local_brain_connected"]:
            self.assertEqual(state["secure_mcp_tunnel_status"], "READY")
            self.assertEqual(
                state["chatgpt_to_owner_pc_brain_connector"],
                "CONNECTED_READONLY",
            )
        if state["end_to_end_seat_brain_transport"]:
            self.assertEqual(state["fresh_chat_seat_validation"], "PASS")
            self.assertEqual(
                state["dedicated_readonly_mcp_tool_allowlist"],
                "PASS_EXACT_TWO_TOOLS",
            )


    def test_current_bootstrap_routes_current_learning_assurance(self):
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        manifest = json.loads((ROOT / "docs" / "RECOVERY_MANIFEST.json").read_text(encoding="utf-8"))
        law = (ROOT / "docs" / "LAW_INDEX_20261003.md").read_text(encoding="utf-8")
        architecture = (ROOT / "docs" / "ARCHITECTURE_NOW_20261003.md").read_text(encoding="utf-8")
        bootstrap = (ROOT / "docs" / "GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md").read_text(encoding="utf-8")
        roadmap = (ROOT / "docs" / "AUTONOMOUS_LEARNING_ROADMAP_20261002.md").read_text(encoding="utf-8")

        self.assertEqual(state["learning_assurance_v14"], "IMPLEMENTED_MERGED_CI_PROVEN_2026-10-03")
        self.assertEqual(manifest["protocols"]["learning_assurance"], "minhtri-learning-assurance/v1.4")
        self.assertIn("adaptive deliberation", law.lower())
        self.assertIn("Learning Assurance v1.4", architecture)
        self.assertIn("LAW_INDEX_20261003.md", bootstrap)
        self.assertIn("ARCHITECTURE_NOW_20261003.md", bootstrap)
        self.assertIn("HISTORICAL ARCHITECTURE ANALYSIS", roadmap)

    def test_current_liveness_is_fresh_observation_not_persistence_claim(self):
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        liveness = state["current_runtime_liveness"]
        self.assertIn(liveness["local_brain_connector"], {"UP", "DOWN", "UNKNOWN"})
        self.assertIn(liveness["secure_mcp_tunnel"], {"UP", "DOWN", "UNKNOWN"})
        self.assertIn(liveness["maintenance_plane"], {"ONLINE", "OFFLINE", "UNKNOWN"})
        if liveness["secure_mcp_tunnel"] == "UP":
            self.assertEqual(liveness["local_brain_connector"], "UP")
        if liveness["secure_mcp_tunnel"] == "DOWN":
            self.assertNotEqual(liveness["local_brain_connector"], "UP")
        self.assertEqual(state["secure_mcp_tunnel_persistence"], "NOT_PROVEN")
        self.assertIn("REBOOT_PROOF_PENDING", state["persistence_probe_latest"])
        self.assertEqual(state["last_proven_runtime_evidence"]["persistence"], "NOT_PROVEN")

    def test_current_workstream_matches_open_gates(self):
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(
            state["active_workstream"],
            "RUNTIME_ASSURANCE_AND_LEARNING_ASSURANCE_EMPIRICAL_VALIDATION",
        )
        self.assertIn("PASS_GENUINE_FRESH_SEAT_VALIDATION", state["open_foundation_gates"])
        self.assertIn("CAPTURE_REAL_EXTERNAL_CRITIC_EXECUTION_EVIDENCE", state["open_foundation_gates"])
        self.assertIn("EMPIRICALLY_VALIDATE_LEARNING_ASSURANCE_V14", state["open_foundation_gates"])
        self.assertFalse(state["autonomy_write_capability"])
        self.assertFalse(state["autonomy_automatic_verified_promotion"])
        self.assertFalse(state["autonomy_automatic_trial_activation"])


    def test_fresh_seat_attempt_remains_fail_closed_without_control_seat(self):
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(
            state["fresh_chat_seat_validation"],
            "BLOCKED_NEEDS_SEPARATE_CHAT_UI_AND_INDEPENDENT_CONTROL_VERIFY",
        )
        self.assertFalse(state["end_to_end_seat_brain_transport"])
        self.assertEqual(state["research_adapter_gate"], "BLOCKED_UNTIL_FRESH_SEAT_PASS")
        self.assertTrue((ROOT / state["fresh_chat_seat_validation_latest_attempt"]).is_file())

    def test_boot_persistence_precheck_is_ready_but_not_promoted_before_reboot_proof(self):
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(state["secure_mcp_tunnel_persistence"], "NOT_PROVEN")
        self.assertEqual(
            state["tunnel_runtime_key_persistence"],
            "PROVISIONED_DPAPI_CURRENT_USER_SECRET_PRESENT",
        )
        self.assertEqual(
            state["tunnel_boot_registration"],
            "INSTALLED_LOGON_TASK_RUNTIME_HARDENED_REBOOT_PROOF_PENDING",
        )
        self.assertIn("READY_FOR_CONTROLLED_REBOOT", state["boot_persistence_precheck_decision"])
        self.assertTrue((ROOT / state["boot_persistence_latest_precheck"]).is_file())
        self.assertTrue((ROOT / state["persistence_diagnosis_latest"]).is_file())

    def test_legacy_live_fields_cannot_override_current_liveness(self):
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(state["runtime_liveness_authoritative_field"], "current_runtime_liveness")
        self.assertFalse(state["legacy_runtime_current_fields_liveness_authority"])
        for key in (
            "local_brain_live_check_latest",
            "owner_pc_maintenance_plane_latest",
            "owner_pc_tunnel_live_check_latest",
            "brain_read_plane_live_check_latest",
        ):
            self.assertIn("HISTORICAL", state[key], key)
        self.assertEqual(state["current_runtime_liveness"]["secure_mcp_tunnel"], "DOWN")
        self.assertEqual(state["current_runtime_liveness"]["local_brain_connector"], "DOWN")

    def test_current_architecture_marks_current_liveness_and_historical_stages(self):
        architecture = (ROOT / "docs" / "ARCHITECTURE_NOW_20261003.md").read_text(encoding="utf-8")
        self.assertIn("Current liveness authoritative — fresh sync observation 2026-10-04", architecture)
        self.assertIn("HISTORICAL — Bounded 24H self-upgrade lease implementation stage", architecture)
        self.assertIn("PROJECT_STATE.current_runtime_liveness", architecture)

    def test_bootstrap_does_not_repeat_closed_ledger_bypass_as_current(self):
        bootstrap = (ROOT / "docs" / "GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md").read_text(encoding="utf-8")
        self.assertIn("CLOSED P0: direct Python", bootstrap)
        self.assertIn("authenticates inside the mutation boundary", bootstrap)

    def test_full_architecture_sync_matches_current_runtime(self):
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        manifest = json.loads((ROOT / "docs" / "RECOVERY_MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual(state["current_runtime_liveness"]["maintenance_plane"], "OFFLINE")
        self.assertEqual(state["current_runtime_liveness"]["secure_mcp_tunnel"], "DOWN")
        self.assertEqual(state["current_runtime_liveness"]["local_brain_connector"], "DOWN")
        self.assertEqual(manifest["current_runtime_liveness"]["maintenance_plane"], "OFFLINE")
        self.assertEqual(manifest["current_runtime_liveness"]["secure_mcp_tunnel"], "DOWN")
        self.assertEqual(manifest["current_runtime_liveness"]["local_brain_connector"], "DOWN")
        self.assertEqual(state["self_upgrade_lease_runtime"], "UNKNOWN_NOT_CURRENTLY_OBSERVED")
        self.assertIn("OPEN_UNTIL_", state["self_upgrade_authorization_window"])

    def test_economics_learning_track_is_routed_everywhere(self):
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        manifest = json.loads((ROOT / "docs" / "RECOVERY_MANIFEST.json").read_text(encoding="utf-8"))
        plan = ROOT / state["owner_learning_track_economics_phd_plan"]
        self.assertTrue(plan.is_file())
        self.assertEqual(state["owner_learning_track_economics_phd_status"], "M0_1_STARTED_UNTESTED")
        self.assertEqual(manifest["owner_learning_track_economics_phd"]["module"], "M0_1_STARTED_UNTESTED")
        self.assertFalse(manifest["owner_learning_track_economics_phd"]["background_runtime"])

    def test_readme_and_security_route_dynamic_liveness_to_project_state(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        self.assertIn("PROJECT_STATE.current_runtime_liveness", readme)
        self.assertIn("PROJECT_STATE.current_runtime_liveness", security)

    def test_architecture_sync_sha_is_not_self_referential(self):
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(state["architecture_sync_merge_sha"], "NOT_SELF_REFERENTIAL_USE_GIT_HISTORY")
        self.assertEqual(
            state["architecture_sync_sha_semantics"],
            "SYNC_RECORD_STORES_SOURCE_MAIN_SHA; RESULTING_MERGE_SHA_IS_DISCOVERED_FROM_GIT_HISTORY",
        )

    def test_claude_review_hardening_is_fail_closed(self):
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        manifest = json.loads((ROOT / "docs" / "RECOVERY_MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual(state["self_learning_system_classification"],
                         "PROPOSAL_GOVERNANCE_PIPELINE_NOT_AUTONOMOUS_BEHAVIOR_ADAPTATION")
        self.assertEqual(state["fresh_chat_seat_protocol_version"], "V2_TTL_BOUND")
        self.assertIsNone(state["fresh_chat_seat_validation_expires_at_utc"])
        self.assertTrue(state["research_gate_requires_current_liveness"])
        self.assertEqual(state["research_ingestion_safety_gate"], "BLOCKED_NOT_IMPLEMENTED")
        self.assertEqual(state["runtime_commit_attestation"], "NOT_PROVEN_CURRENTLY_OFFLINE")
        self.assertTrue(state["negative_control_fail_blocks_lesson_freeze"])
        self.assertIn("src/minhtri/autonomy.py", state["candidate_enforcement_paths_protected"])
        self.assertEqual(
            state["self_upgrade_candidate_a_status"],
            "REJECTED_BY_POLICY_HARDENING_AUTONOMY_PATH_NOW_PROTECTED",
        )
        self.assertEqual(
            manifest["candidate_a"]["status"],
            "REJECTED_BY_POLICY_HARDENING_AUTONOMY_PATH_NOW_PROTECTED",
        )
        self.assertEqual(manifest["fresh_seat_validation"]["protocol"],
                         "minhtri-fresh-seat-validation/v2")

    def test_gemini_review_meta_learning_hardening_is_routed(self):
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        manifest = json.loads((ROOT / "docs" / "RECOVERY_MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual(state["meta_learning_min_candidate_resolutions"], 50)
        self.assertEqual(state["meta_learning_multiplicity_control"], "NOT_IMPLEMENTED")
        self.assertEqual(state["meta_learning_permutation_test"], "REQUIRED_BEFORE_ADAPTATION")
        self.assertEqual(
            manifest["meta_learning_assurance"]["minimum_candidate_resolutions"], 50
        )
        self.assertFalse(manifest["meta_learning_assurance"]["statistical_adaptation_proven"])
        self.assertEqual(
            manifest["self_upgrade"]["candidate_a_status"],
            "REJECTED_BY_POLICY_HARDENING_AUTONOMY_PATH_NOW_PROTECTED",
        )


    def test_universal_learning_continuity_is_routed_and_recoverable(self):
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        manifest = json.loads((ROOT / "docs" / "RECOVERY_MANIFEST.json").read_text(encoding="utf-8"))
        law = ROOT / state["universal_learning_continuity_law"]
        checkpoint = ROOT / state["owner_learning_track_buddhist_thought_checkpoint"]
        law_index = (ROOT / state["current_law_index"]).read_text(encoding="utf-8")
        architecture = (ROOT / state["current_architecture"]).read_text(encoding="utf-8")
        bootstrap = (ROOT / state["role_bootstrap"]).read_text(encoding="utf-8")

        self.assertTrue(law.is_file())
        self.assertTrue(checkpoint.is_file())
        self.assertEqual(state["universal_learning_continuity"], "DURABLY_INTEGRATED")
        self.assertEqual(manifest["universal_learning_continuity"]["status"], "DURABLY_INTEGRATED")
        self.assertTrue(state["universal_learning_prework_bootstrap_required"])
        self.assertTrue(state["universal_learning_durable_checkpoint_required"])
        self.assertFalse(state["chat_memory_is_canonical_project_memory"])
        self.assertEqual(state["owner_learning_track_buddhist_thought_status"], "PHASE_4_A37_COMPLETED")
        self.assertEqual(state["owner_learning_track_buddhist_thought_next_checkpoint"], "PHASE_4_A38")
        self.assertEqual(manifest["universal_learning_continuity"]["law"], state["universal_learning_continuity_law"])
        self.assertEqual(manifest["owner_learning_track_buddhist_thought"]["current"], "PHASE_4_A37_COMPLETED")
        self.assertEqual(manifest["owner_learning_track_buddhist_thought"]["next"], "PHASE_4_A38")
        self.assertIn("LAW_UNIVERSAL_LEARNING_CONTINUITY_20261004.md", law_index)
        self.assertIn("Universal learning continuity invariant", architecture)
        self.assertIn("MANDATORY UNIVERSAL LEARNING BOOTSTRAP", bootstrap)


    def test_buddhist_track_requires_milindapanha_continuously(self):
        state = json.loads((ROOT / "docs" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        manifest = json.loads((ROOT / "docs" / "RECOVERY_MANIFEST.json").read_text(encoding="utf-8"))
        law = (ROOT / state["universal_learning_continuity_law"]).read_text(encoding="utf-8")
        checkpoint = (ROOT / state["owner_learning_track_buddhist_thought_checkpoint"]).read_text(encoding="utf-8")
        law_index = (ROOT / state["current_law_index"]).read_text(encoding="utf-8")
        architecture = (ROOT / state["current_architecture"]).read_text(encoding="utf-8")
        bootstrap = (ROOT / state["role_bootstrap"]).read_text(encoding="utf-8")

        self.assertTrue(state["owner_learning_track_buddhist_thought_milindapanha_required"])
        self.assertEqual(
            state["owner_learning_track_buddhist_thought_milindapanha_scope"],
            "ALL_MATERIAL_CHECKPOINTS_CONTINUOUS",
        )
        self.assertTrue(
            state["owner_learning_track_buddhist_thought_milindapanha_checkpoint_record_required"]
        )
        self.assertTrue(manifest["owner_learning_track_buddhist_thought"]["milindapanha_required"])
        self.assertEqual(
            manifest["owner_learning_track_buddhist_thought"]["milindapanha_scope"],
            "ALL_MATERIAL_CHECKPOINTS_CONTINUOUS",
        )
        self.assertIn("Buddhist-study mandatory Milindapañha rule", law)
        self.assertIn("Mandatory Milindapañha rule for Buddhist study", law_index)
        self.assertIn("Buddhist-study Milindapañha continuity invariant", architecture)
        self.assertIn("MILINDAPAÑHA / MI TIÊN VẤN ĐÁP", bootstrap)
        self.assertIn("Mandatory Milindapañha consultation record", checkpoint)
        self.assertIn("must never be silently promoted to `TEXT_ATTESTED`", checkpoint)


if __name__ == "__main__":
    unittest.main()
