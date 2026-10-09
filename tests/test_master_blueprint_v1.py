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

    def test_frozen_blueprint_routes_to_active_open_task(self):
        current=load("state/current.yaml")
        tasks={x["task_id"]:x for x in load("state/tasks.yaml")["tasks"]}
        self.assertEqual(current["foundation_status"],"FROZEN")
        self.assertEqual(tasks["ARCH-MASTER-BLUEPRINT-V1"]["status"],"DONE")
        self.assertIn(current["active_task_id"],tasks)
        active=tasks[current["active_task_id"]]
        self.assertNotEqual(active["task_id"],"ARCH-MASTER-BLUEPRINT-V1")
        self.assertIn(active["status"],{"IN_PROGRESS","BLOCKED","REPORTED","REVIEWED_REVISE","STALE"})
        self.assertIn(active["change_class"],{"F","S","D","O"})
        self.assertTrue(active.get("acceptance_authority"))
        self.assertEqual(current["next_checkpoint"],active["next_action"])
        if current["active_workstream"]=="OWNER_DIRECTED_LEARNING":
            self.assertTrue(any(str(path).startswith("docs/learning/") for path in active.get("scope",[])))
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

    def test_a173_never_uses_obsolete_legacy_execution_branch(self):
        tasks=load("state/tasks.yaml")["tasks"]
        study=next(t for t in tasks if t["task_id"]=="BUDDHIST-A173")
        self.assertEqual(study["change_class"],"D")
        self.assertNotEqual(study.get("branch"),"learning/buddhist-a173-20261005-2205")
        if study.get("branch") is None:
            self.assertEqual(study.get("branch_binding"),"NONE_NO_EXECUTION_REF_UNTIL_OWNER_APPROVED_ASSIGNMENT")
        else:
            self.assertNotEqual(study.get("branch_binding"),"NONE_NO_EXECUTION_REF_UNTIL_OWNER_APPROVED_ASSIGNMENT")
            self.assertTrue(study.get("base_sha"))
        handoff=(ROOT/study["handoff_ref"]).read_text(encoding="utf-8")
        self.assertIn("PR #249",handoff)
    def test_class_s_routing_is_separate_from_class_d_study(self):
        state=load("state/current.yaml")
        records={r["task_id"]:r for r in load("state/tasks.yaml")["tasks"]}
        routing=records["ARCH-BUDDHIST-A173-ROUTING-V1"]
        study=records["BUDDHIST-A173"]
        self.assertEqual(state["foundation_status"],"FROZEN")
        self.assertEqual(routing["change_class"],"S")
        self.assertEqual(routing["acceptance_authority"],"OWNER")
        self.assertIn(routing["status"],{"IN_PROGRESS","DONE"})
        if routing["status"]=="IN_PROGRESS":
            self.assertTrue(routing.get("blocker"))
        self.assertTrue({
            "state/current.yaml", "state/tasks.yaml", "tests/test_master_blueprint_v1.py",
            "tools/validate_continuity_handoff.py", "tests/test_continuity_handoff_core_v1.py",
        }.issubset(set(routing["scope"])))
        self.assertEqual(study["change_class"],"D")
        self.assertEqual(study["acceptance_authority"],"OWNER")
        self.assertNotEqual(study.get("branch"),"learning/buddhist-a173-20261005-2205")
        gate=routing["material_findings_owner_gate"]
        self.assertEqual(len(gate["provisional_intake_keys"]),8)
        self.assertEqual(len(set(gate["provisional_intake_keys"])),8)
        self.assertIn("OWNER_REPORTED_ORIGINALS_LOST",gate["originals_or_attestation"])
        self.assertIn("OWNER_CHAT_ONE_TIME_GATE3_EXCEPTION",gate["gate_3_build_before_task_authorize"])
        witness=routing["post_merge_witness"]
        self.assertEqual(witness["assignment_authority"],"OWNER")
        self.assertEqual(witness["evidence_role"],"Evidence/Validation")
        self.assertFalse(witness["builder_self_certification_allowed"])
        self.assertEqual(witness["merge_commit_evidence"],[
            "reviewed_head_sha", "owner_acceptance_comment_id", "exact_head_ci_run_id"
        ])
        self.assertFalse(state["autonomous_learning_runtime"])
        self.assertFalse(state["automatic_self_critique_runtime"])
        self.assertFalse(state["meta_learning_runtime"])
    def test_bootstrap_route_and_study_predecessor_do_not_promote_drafts(self):
        boot=load("state/bootstrap.json")
        state=load(boot["current_state"])
        tasks={x["task_id"]:x for x in load(boot["task_registry"])["tasks"]}
        active=tasks[state["active_task_id"]]
        self.assertIn(active["status"],{"IN_PROGRESS","BLOCKED","REPORTED","REVIEWED_REVISE","STALE"})
        handoff_path=ROOT/active["handoff_ref"]
        self.assertTrue(handoff_path.is_file())
        handoff=handoff_path.read_text(encoding="utf-8")
        self.assertEqual(handoff.split("## NEXT ACTION",1)[1].strip().splitlines()[0],active["next_action"])
        self.assertEqual(active["next_action"],state["next_checkpoint"])
        self.assertTrue((ROOT/"docs/learning/BUDDHIST_THOUGHT_CHECKPOINT_A172_20261005.md").is_file())
        if active["task_id"]=="BUDDHIST-A173":
            self.assertIsNone(active["branch"])
            self.assertIn("NOT CURRENT",handoff)
            self.assertIn("PR #249",handoff)
            for step in (174,175,176):
                self.assertTrue((ROOT/f"docs/learning/BUDDHIST_THOUGHT_CHECKPOINT_A{step}_DRAFT_20261005.md").is_file())
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

    def test_f3_and_class_s_owner_gate_are_explicit_without_prose_lock(self):
        state=load("state/current.yaml")
        records={r["task_id"]:r for r in load("state/tasks.yaml")["tasks"]}
        study=records["BUDDHIST-A173"]
        routing=records["ARCH-BUDDHIST-A173-ROUTING-V1"]
        dh=(ROOT/study["handoff_ref"]).read_text(encoding="utf-8")
        sh=(ROOT/routing["handoff_ref"]).read_text(encoding="utf-8")
        dispo=(ROOT/"docs/vnext/red_team/BUDDHIST_A173_ROUTING_CLASS_S_FINDINGS_DISPOSITION_20261009.md").read_text(encoding="utf-8")
        self.assertIn("A172",dh)
        self.assertIn("A173",dh)
        self.assertIn("PR #249",dh)
        gate=routing["material_findings_owner_gate"]
        self.assertIn(gate["owner_acceptance"],{"NOT_GRANTED","GRANTED"})
        self.assertTrue(gate["status"])
        self.assertIn("OWNER_REPORTED_ORIGINALS_LOST",gate["originals_or_attestation"])
        self.assertIn("OWNER_CHAT_ONE_TIME_GATE3_EXCEPTION",gate["gate_3_build_before_task_authorize"])
        self.assertIn("6076001277",gate["gate_3_build_before_task_authorize"])
        self.assertIn("HISTORICAL_F3_UNVERIFIED",dispo)
        self.assertEqual(len(gate["provisional_intake_keys"]),8)
        for key in gate["provisional_intake_keys"]:
            self.assertIn(key,dispo)
        self.assertIn("## PHASE-BOUND STATUS",sh)
        self.assertEqual(routing["next_action"],sh.split("## NEXT ACTION",1)[1].strip().splitlines()[0])
        witness=routing["post_merge_witness"]
        for field in ("reviewed_head_sha","owner_acceptance_comment_id","exact_head_ci_run_id"):
            self.assertIn(field,witness["merge_commit_evidence"])
        self.assertFalse(witness["builder_self_certification_allowed"])
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
