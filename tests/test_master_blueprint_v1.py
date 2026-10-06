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

    def test_master_blueprint_is_accepted_and_recovery_v6_is_active_frontier(self):
        current=load("state/current.yaml")
        tasks=load("state/tasks.yaml")
        self.assertEqual(current["active_task_id"], "ARCH-RECOVERY-PROOF-V6")
        blueprint=next(x for x in tasks["tasks"] if x["task_id"]=="ARCH-MASTER-BLUEPRINT-V1")
        recovery=next(x for x in tasks["tasks"] if x["task_id"]=="ARCH-RECOVERY-PROOF-V6")
        self.assertEqual(blueprint["status"], "DONE")
        self.assertEqual(recovery["status"], "IN_PROGRESS")

    def test_foundation_freeze_is_held(self):
        tasks=load("state/tasks.yaml")
        t=next(x for x in tasks["tasks"] if x["task_id"]=="ARCH-FOUNDATION-ACCEPTANCE-FREEZE-V1")
        self.assertEqual(t["status"], "BLOCKED")
        self.assertEqual(t["blocker"], "RECOVERY_PROOF_V6_PASS_AND_DURABLE_RECEIPT_REQUIRED")
        closure=next(x for x in tasks["tasks"] if x["task_id"]=="ARCH-FOUNDATION-CLOSURE-V1")
        self.assertEqual(closure["status"], "BLOCKED")
        self.assertIn("Recovery Proof v6", closure["next_action"])
        self.assertEqual(closure["handoff_ref"], "docs/vnext/handoff/RECOVERY_PROOF_V6.md")

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

if __name__=="__main__":
    unittest.main()
