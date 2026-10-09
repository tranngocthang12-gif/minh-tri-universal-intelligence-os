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

    def test_a173_branch_is_not_stale_legacy_execution_ref(self):
        import json
        current=json.loads((ROOT/"state/current.yaml").read_text(encoding="utf-8"))
        tasks=json.loads((ROOT/"state/tasks.yaml").read_text(encoding="utf-8"))["tasks"]
        active=next(t for t in tasks if t["task_id"]==current["active_task_id"])
        self.assertEqual(active["task_id"],"BUDDHIST-A173")
        self.assertIsNone(active.get("branch"),"No pre-freeze branch may be bound to frozen main")
        self.assertEqual(active.get("branch_binding"),"NONE_NO_EXECUTION_REF_UNTIL_OWNER_APPROVED_ASSIGNMENT")
        self.assertEqual(active.get("blocker"),"OWNER_CLASS_D_EXECUTION_REF_ASSIGNMENT_PENDING_FOR_MUTATION")
        self.assertIn("before any Class D branch mutation including PR #336",active["next_action"])
        self.assertIn("explicit Owner assignment and exact branch/base/head binding",active["next_action"])
        handoff=(ROOT/active["handoff_ref"]).read_text(encoding="utf-8")
        self.assertIn("PR #249 is NOT a current execution branch",handoff)
        self.assertIn("PR #319 remains Draft/Class F HOLD",handoff)
        self.assertIn("PR #336 (head",handoff)
        self.assertIn("Draft/UNBOUND",handoff)
        self.assertIn("NOT YET DURABLY RECORDED",handoff)
        self.assertIn("authorized Class D execution ref and protected merge",handoff)

    def test_class_s_routing_is_separate_from_class_d_study(self):
        state=load("state/current.yaml")
        records=load("state/tasks.yaml")["tasks"]
        by_id={r["task_id"]:r for r in records}
        routing=by_id["ARCH-BUDDHIST-A173-ROUTING-V1"]
        study=by_id["BUDDHIST-A173"]
        self.assertEqual(state["foundation_status"],"FROZEN")
        self.assertEqual(routing["change_class"],"S")
        self.assertEqual(routing["acceptance_authority"],"OWNER")
        self.assertEqual(routing["status"],"IN_PROGRESS")
        self.assertEqual(routing["blocker"],"CLASS_S_LIFECYCLE_OWNER_FINDING_AND_WITNESS_EVIDENCE_REQUIRED_BEFORE_CLOSURE")
        self.assertEqual(routing["base_sha"],"a5ed9d8347a60b95503fe2e5de6b95fd8375eb76")
        self.assertEqual(routing["branch"],"owner/buddhist-a173-learning-routing-20261009")
        self.assertTrue({"state/current.yaml","state/tasks.yaml","tests/test_master_blueprint_v1.py"}.issubset(set(routing["scope"])))
        self.assertEqual(study["change_class"],"D")
        self.assertEqual(study["acceptance_authority"],"OWNER")
        self.assertIsNone(study["branch"])
        self.assertEqual(study["branch_binding"],"NONE_NO_EXECUTION_REF_UNTIL_OWNER_APPROVED_ASSIGNMENT")
        self.assertEqual(study["blocker"],"OWNER_CLASS_D_EXECUTION_REF_ASSIGNMENT_PENDING_FOR_MUTATION")
        self.assertEqual(routing["material_findings_owner_gate"]["status"],"OWNER_PER_FINDING_DISPOSITION_PENDING")
        self.assertEqual(routing["material_findings_owner_gate"]["provisional_intake_keys"],["INTAKE_26D_GROK_HIGH_BRANCH_BASE","INTAKE_26D_CODEX_MEDIUM_BRANCH_BASE","INTAKE_26D_CLAUDE_MEDIUM_BRANCH_BASE","INTAKE_26D_CLAUDE_MEDIUM_DEPENDENT_DRAFTS","INTAKE_26D_CLAUDE_MEDIUM_CLASS_S_AUTHORIZATION","INTAKE_951_CLAUDE_F1_MEDIUM_EXECUTION_REF","INTAKE_951_CLAUDE_F2_MEDIUM_POST_MERGE_RECOVERY","INTAKE_951_CLAUDE_F3_MEDIUM_VERBATIM_INTAKE"])
        self.assertEqual(routing["post_merge_witness"]["assignment_authority"],"OWNER")
        self.assertEqual(routing["post_merge_witness"]["evidence_role"],"Evidence/Validation")
        self.assertIsNone(routing["post_merge_witness"]["witness_holder"])
        self.assertIsNone(routing["post_merge_witness"]["closure_holder"])
        self.assertFalse(routing["post_merge_witness"]["builder_self_certification_allowed"])
        self.assertEqual(routing["post_merge_witness"]["merge_commit_evidence"],["reviewed_head_sha","owner_acceptance_comment_id","exact_head_ci_run_id"])
        self.assertEqual(state["active_task_id"],study["task_id"])
        self.assertFalse(state["autonomous_learning_runtime"])
        self.assertFalse(state["automatic_self_critique_runtime"])
        self.assertFalse(state["meta_learning_runtime"])

    def test_zero_chat_route_recovers_handoff_and_dependent_drafts(self):
        boot=load("state/bootstrap.json")
        state=load(boot["current_state"])
        tasks=load(boot["task_registry"])
        current=next(x for x in tasks["tasks"] if x["task_id"]==state["active_task_id"])
        self.assertEqual(current["task_id"],"BUDDHIST-A173")
        self.assertIsNone(current["branch"],"legacy PR #249 must not be executed")
        handoff_path=ROOT/current["handoff_ref"]
        self.assertTrue(handoff_path.is_file())
        handoff=handoff_path.read_text(encoding="utf-8")
        self.assertIn("## NEXT ACTION",handoff)
        self.assertEqual(handoff.split("## NEXT ACTION",1)[1].strip().splitlines()[0],current["next_action"])
        self.assertEqual(current["next_action"],state["next_checkpoint"])
        self.assertIn("PR #319 remains Draft/Class F HOLD",handoff)
        self.assertIn("BUDDHIST_THOUGHT_COMPLIANCE_AUDIT_20261005.md",handoff)
        self.assertIn("BUDDHIST_THOUGHT_CHECKPOINT_A177_DRAFT_20261005.md",handoff)
        for step in (174,175,176):
            path=ROOT/f"docs/learning/BUDDHIST_THOUGHT_CHECKPOINT_A{step}_DRAFT_20261005.md"
            self.assertTrue(path.is_file(),str(path))
            self.assertIn(f"A{step}",handoff)
        self.assertTrue((ROOT/"docs/learning/BUDDHIST_THOUGHT_CHECKPOINT_A172_20261005.md").is_file())
        draft=(ROOT/"docs/learning/BUDDHIST_THOUGHT_CHECKPOINT_A173_DRAFT_20261005.md").read_text(encoding="utf-8")
        self.assertIn("A173",draft)
        self.assertIn("NOT CURRENT",handoff)

    def test_class_s_handoff_distinct_from_class_d_and_exact_next_action(self):
        records=load("state/tasks.yaml")["tasks"]
        routes={r["task_id"]:r for r in records}
        routing=routes["ARCH-BUDDHIST-A173-ROUTING-V1"]
        study=routes["BUDDHIST-A173"]
        self.assertNotEqual(routing["handoff_ref"],study["handoff_ref"])
        for task in (routing,study):
            handoff=(ROOT/task["handoff_ref"]).read_text(encoding="utf-8")
            self.assertIn("## NEXT ACTION",handoff)
            self.assertEqual(task["next_action"],handoff.split("## NEXT ACTION",1)[1].strip().splitlines()[0])
        self.assertEqual(routing["change_class"],"S")
        self.assertIn("CLASS_S_FINDINGS_DISPOSITION",routing["result_ref"])
        self.assertIn("PR #319 remains", (ROOT/routing["handoff_ref"]).read_text(encoding="utf-8"))
        self.assertEqual(study["change_class"],"D")

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

    def test_n1_n4_owner_gate_post_merge_and_class_d_regressions(self):
        state=load("state/current.yaml")
        records={r["task_id"]:r for r in load("state/tasks.yaml")["tasks"]}
        study=records["BUDDHIST-A173"]
        routing=records["ARCH-BUDDHIST-A173-ROUTING-V1"]
        dh=(ROOT/study["handoff_ref"]).read_text(encoding="utf-8")
        sh=(ROOT/routing["handoff_ref"]).read_text(encoding="utf-8")
        dispo=(ROOT/"docs/vnext/red_team/BUDDHIST_A173_ROUTING_CLASS_S_FINDINGS_DISPOSITION_20261009.md").read_text(encoding="utf-8")
        self.assertEqual(state["next_checkpoint"],study["next_action"])
        self.assertIn("before any Class D branch mutation including PR #336",state["next_checkpoint"])
        self.assertIn("explicit Owner assignment and exact branch/base/head binding",state["next_checkpoint"])
        self.assertIn("PR #336",dh)
        self.assertIn("Draft/UNBOUND",dh)
        self.assertIn("NOT YET DURABLY RECORDED",dh)
        self.assertIn("acceptance by the acceptance_authority recorded in state/tasks.yaml (currently OWNER",dh)
        gate=routing["material_findings_owner_gate"]
        self.assertEqual(gate["owner_acceptance"],"NOT_GRANTED")
        self.assertEqual(gate["status"],"OWNER_PER_FINDING_DISPOSITION_PENDING")
        self.assertIn("OWNER_REPORTED_ORIGINALS_LOST",gate["originals_or_attestation"])
        self.assertIn("OWNER_CHAT_ONE_TIME_GATE3_EXCEPTION",gate["gate_3_build_before_task_authorize"])
        self.assertIn("replacement route",routing["next_action"])
        self.assertIn("residual historical uncertainty",sh)
        self.assertNotIn("durably attest the builder intake summaries are complete and accurate",sh)
        for k in gate["provisional_intake_keys"]:
            self.assertIn(k,dispo)
        self.assertIn("Gate 3 authorization-after-build",dispo)
        self.assertIn("## PHASE-BOUND STATUS",sh)
        self.assertNotIn("STATUS: REVIEW PENDING / NO OWNER ACCEPTANCE / NO MERGE.",sh)
        self.assertNotIn("Independent different-seat review of the EXACT current PR #334 SHA is NOT present.",sh)
        self.assertEqual(routing["next_action"],sh.split("## NEXT ACTION",1)[1].strip().splitlines()[0])
        for label in ("REVIEWED_HEAD_SHA","OWNER_ACCEPTANCE_COMMENT_ID","EXACT_HEAD_CI_RUN_ID"):
            self.assertIn(label,sh)
        self.assertIn("Owner must appoint",sh)
        self.assertIn("Evidence/Validation",sh)
        self.assertIn("separately gate Class S closure",routing["next_action"])
        self.assertFalse(state["autonomous_learning_runtime"])

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
