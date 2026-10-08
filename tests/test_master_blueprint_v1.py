import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

class MasterBlueprintV1Tests(unittest.TestCase):
    def test_boot_routes_to_master_blueprint(self):
        boot=load("state/bootstrap.json")
        current=load("state/current.yaml")
        self.assertEqual(boot["master_blueprint"], "docs/vnext/MASTER_BLUEPRINT_V1_20261006.md")
        self.assertTrue((ROOT/boot["master_blueprint"]).is_file())
        self.assertEqual(current["master_blueprint"], boot["master_blueprint"])
        self.assertIn("master_blueprint", current["authority_scope"]["mirrors_boot_root_pointers"])
        self.assertNotIn("master_blueprint", current["authority_scope"]["this_file_is_authoritative_for"])
        self.assertIn("law_precedence", current["authority_scope"]["mirrors_boot_root_pointers"])
        self.assertNotIn("law_precedence", current["authority_scope"]["this_file_is_authoritative_for"])

    def test_frozen_blueprint_routes_to_active_buddhist_learning(self):
        current=load("state/current.yaml")
        tasks=load("state/tasks.yaml")
        self.assertEqual(current["foundation_status"], "FROZEN")
        blueprint=next(x for x in tasks["tasks"] if x["task_id"]=="ARCH-MASTER-BLUEPRINT-V1")
        self.assertEqual(blueprint["status"], "DONE")
        self.assertEqual(current["active_task_id"], "BUDDHIST-A173")
        learning=next(x for x in tasks["tasks"] if x["task_id"]=="BUDDHIST-A173")
        self.assertEqual(learning["status"], "IN_PROGRESS")
        self.assertEqual(learning["change_class"], "D")
        self.assertEqual(learning["acceptance_authority"], "OWNER")
        self.assertEqual(learning["next_action"], current["next_checkpoint"])
        self.assertIn("A173", learning["handoff_ref"])

    def test_owner_accepted_foundation_freeze(self):
        tasks=load("state/tasks.yaml")
        t=next(x for x in tasks["tasks"] if x["task_id"]=="ARCH-FOUNDATION-ACCEPTANCE-FREEZE-V1")
        self.assertEqual(t["status"], "DONE")
        self.assertIsNone(t["blocker"])
        self.assertEqual(t["acceptance_authority"], "OWNER")
        closure=next(x for x in tasks["tasks"] if x["task_id"]=="ARCH-FOUNDATION-CLOSURE-V1")
        self.assertEqual(closure["status"], "STALE")
        self.assertEqual(closure.get("superseded_by"), "ARCH-FOUNDATION-ACCEPTANCE-FREEZE-V1")
        self.assertEqual(closure["handoff_ref"], "docs/vnext/handoff/FOUNDATION_ACCEPTANCE_FREEZE_V1.md")

    def test_role_separation_and_lifecycle_are_durable(self):
        bp=(ROOT/"docs/vnext/MASTER_BLUEPRINT_V1_20261006.md").read_text(encoding="utf-8")
        law=(ROOT/"docs/vnext/FOUNDATION_LAW_CONSOLIDATED_V1_20261006.md").read_text(encoding="utf-8")
        for token in ["Owner","Architect","Builder / Implementer","Supervisor / Inspector","Independent Reviewer / Critic","Evidence / Validation Layer"]:
            self.assertIn(token,bp)
        self.assertIn("DESIGN -> LAW CHECK -> TASK AUTHORIZE -> BUILD -> SUPERVISE -> VALIDATE",bp)
        self.assertIn("Architect: designs and maintains the Master Blueprint but cannot self-accept",law)
        self.assertIn("Builder/Implementer: implements bounded approved work but cannot self-certify",law)
        self.assertIn("TASK AUTHORIZE", law)
        self.assertIn("CRITICAL/HIGH/MEDIUM", law)

    def test_recovery_entrypoint_reads_blueprint_before_state(self):
        text=(ROOT/"docs/vnext/continuity/RECOVERY_ENTRYPOINT_V1.md").read_text(encoding="utf-8")
        self.assertIn("Read the `master_blueprint` routed by the boot root.",text)

    def test_current_route_mentions_blueprint_before_state(self):
        role=(ROOT/"docs/GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md").read_text(encoding="utf-8")
        law_index=(ROOT/"docs/LAW_INDEX_20261003.md").read_text(encoding="utf-8")
        arch=(ROOT/"docs/vnext/ARCHITECTURE_VNEXT_OWNER_APPROVED_CANDIDATE_20261006.md").read_text(encoding="utf-8")
        self.assertLess(role.index("CURRENT MASTER BLUEPRINT"), role.index("CURRENT STATE + TASK REGISTRY"))
        self.assertIn("state/bootstrap.json -> current Master Blueprint -> authoritative law precedence -> state/current.yaml", law_index)
        self.assertIn("state/bootstrap.json -> current Master Blueprint -> authoritative law precedence -> state/current.yaml -> state/tasks.yaml", arch)

    def test_change_class_is_explicit_for_every_task(self):
        tasks=load("state/tasks.yaml")
        for task in tasks["tasks"]:
            self.assertIn("change_class", task, task["task_id"])

    def test_exact_next_action_is_identical_across_current_task_handoff(self):
        current=load("state/current.yaml")
        tasks=load("state/tasks.yaml")
        active=next(x for x in tasks["tasks"] if x["task_id"]==current["active_task_id"])
        handoff=(ROOT/active["handoff_ref"]).read_text(encoding="utf-8")
        after=handoff.split("## NEXT ACTION",1)[1].lstrip()
        handoff_next=after.splitlines()[0]
        self.assertEqual(current["next_checkpoint"], active["next_action"])
        self.assertEqual(active["next_action"], handoff_next)
        self.assertNotIn("Packet v2", current["next_checkpoint"])

    def test_change_class_and_acceptance_resume_gate(self):
        tasks=load("state/tasks.yaml")
        allowed={"F","S","D","O","UNCLASSIFIED_LEGACY"}
        for task in tasks["tasks"]:
            self.assertIn(task["change_class"], allowed, task["task_id"])
            if task["status"]!="DONE" and task["change_class"]=="UNCLASSIFIED_LEGACY":
                self.assertEqual(task.get("resume_gate"), "MUST_ASSIGN_CHANGE_CLASS_F_S_D_O_AND_ACCEPTANCE_AUTHORITY_BEFORE_RESUMPTION_OR_PROTECTED_MERGE")
            if task["status"]!="DONE" and task["change_class"] in {"F","S","D","O"}:
                self.assertTrue(task.get("acceptance_authority"), task["task_id"])

    def test_role_bootstrap_defers_to_sole_normative_law_router(self):
        role=(ROOT/"docs/GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md").read_text(encoding="utf-8")
        self.assertIn("sole normative precedence ladder", role)
        self.assertIn("FOUNDATION_LAW_CONSOLIDATED_V1_20261006.md", role)

    def test_legacy_control_semantics_are_history_only(self):
        boot=load("state/bootstrap.json")
        self.assertTrue(boot["legacy_must_not_override_migrated_state"])
        self.assertIn("next_checkpoint_or_next_action", boot["legacy_control_semantics_history_only"])
        self.assertIn("capability_or_acceptance_status_for_migrated_scope", boot["legacy_control_semantics_history_only"])

    def test_foundation_recovery_supersession_is_routed_and_live_tasks_are_not_literal_v6_blocked(self):
        bp=(ROOT/"docs/vnext/MASTER_BLUEPRINT_V1_20261006.md").read_text(encoding="utf-8")
        rat=(ROOT/"docs/vnext/OWNER_DECISION_MASTER_BLUEPRINT_V1_POST_MERGE_RATIFICATION_20261007.md").read_text(encoding="utf-8")
        tasks=load("state/tasks.yaml")
        self.assertIn("OWNER_DECISION_RECOVERY_V9_SUPERSEDES_V6_FREEZE_GATE_20261007.md", bp)
        self.assertIn("OWNER_DECISION_RECOVERY_V9_SUPERSEDES_V6_FREEZE_GATE_20261007.md", rat)
        closure=next(x for x in tasks["tasks"] if x["task_id"]=="ARCH-FOUNDATION-CLOSURE-V1")
        self.assertEqual(closure["status"], "STALE")
        self.assertEqual(closure.get("superseded_by"), "ARCH-FOUNDATION-ACCEPTANCE-FREEZE-V1")
        self.assertNotIn("RECOVERY_V6_REQUIRED", closure.get("blocker",""))

    def test_foundation_freeze_state_is_explicit_and_not_frozen_during_repair(self):
        current=load("state/current.yaml")
        self.assertEqual(current["foundation_status"], "FROZEN")
        self.assertIn("foundation_status", current["authority_scope"]["this_file_is_authoritative_for"])
        self.assertEqual(current["phase"], "FOUNDATION_V1_FROZEN_LEARNING_RESUMPTION")

    def test_blueprint_reopen_rule_defers_to_law_router(self):
        bp=(ROOT/"docs/vnext/MASTER_BLUEPRINT_V1_20261006.md").read_text(encoding="utf-8")
        self.assertIn("Normative reopen authority is the consolidated Foundation Law router", bp)
        self.assertIn("Class F state transition requiring Owner acceptance", bp)

    def test_supervisor_gap_is_explicitly_held_not_waived(self):
        disp=(ROOT/"docs/vnext/red_team/FOUNDATION_FREEZE_CLAUDE_V3_DISPOSITION_20261008.md").read_text(encoding="utf-8")
        req=(ROOT/"docs/vnext/supervision/FOUNDATION_V3_POST_RECOVERY_SUPERVISOR_REQUEST_20261008.md").read_text(encoding="utf-8")
        self.assertIn("NOT YET CLOSED", disp)
        self.assertIn("fresh different-seat Supervisor inspection", disp)
        self.assertIn("SUPERVISOR_INSPECTOR_DIFFERENT_SEAT", req)

    def test_debt_register_preserves_v3_and_matrix_points_to_current_v4_gate(self):
        debt=(ROOT/"docs/vnext/FOUNDATION_DEBT_REGISTER_V1_20261006.md").read_text(encoding="utf-8")
        matrix=(ROOT/"docs/vnext/FOUNDATION_CAPABILITY_TRUTH_MATRIX_V1_20261006.md").read_text(encoding="utf-8")
        self.assertIn("Gemini clean; Claude and Grok material findings", debt)
        self.assertIn("MATERIAL_FINDINGS_PRESENT_V4", matrix)
        self.assertIn("C6_C7_C8_HISTORICAL_FAIL__C9_BOUNDED_PASS", matrix)
        self.assertIn("FF-CLAUDE-V4-001/007 MEDIUM", matrix)
        self.assertNotIn("Must complete against the repaired v2 packet before final freeze", debt)
        self.assertNotIn("Claude + Grok v2 red-team receipts still required", matrix)

    def test_grok_v4_intake_is_historical_not_v5_acceptance(self):
        path=ROOT/"docs/vnext/red_team/FOUNDATION_GROK_V4_POST_OWNER_A_VERIFICATION_20261008.json"
        raw=path.read_bytes()
        saved=json.loads(raw)
        receipt=load("docs/vnext/red_team/FOUNDATION_GROK_V4_OWNER_CHAT_INTAKE_RECEIPT_20261008.json")
        sha=hashlib.sha1(f"blob {len(raw)}".encode("ascii") + bytes([0]) + raw).hexdigest()
        self.assertEqual(saved["round"], "FOUNDATION_V4_POST_OWNER_A_VERIFICATION")
        self.assertEqual(saved["verdict"], "MATERIAL_DEFECTS_FOUND")
        self.assertEqual(set(saved["unresolved_material_findings"]), {"FF-CLAUDE-V4-001", "FF-CLAUDE-V4-007"})
        self.assertEqual(sha, receipt["archived_blob_sha"])
        self.assertEqual(receipt["provenance_class"], "OWNER_CHAT_INTAKE_AUTHORING_SEAT")
        self.assertFalse(receipt["independent_receipt"])
        self.assertFalse(receipt["is_v5_critic_review"])

if __name__=="__main__":
    unittest.main()
