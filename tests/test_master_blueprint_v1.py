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

    def test_master_blueprint_is_active_frontier(self):
        current=load("state/current.yaml")
        tasks=load("state/tasks.yaml")
        self.assertEqual(current["active_task_id"], "ARCH-MASTER-BLUEPRINT-V1")
        t=next(x for x in tasks["tasks"] if x["task_id"]=="ARCH-MASTER-BLUEPRINT-V1")
        self.assertEqual(t["status"], "IN_PROGRESS")

    def test_foundation_freeze_is_held(self):
        tasks=load("state/tasks.yaml")
        t=next(x for x in tasks["tasks"] if x["task_id"]=="ARCH-FOUNDATION-ACCEPTANCE-FREEZE-V1")
        self.assertEqual(t["status"], "BLOCKED")
        self.assertEqual(t["blocker"], "MASTER_BLUEPRINT_V1_ACCEPTANCE_AND_RECOVERY_PROOF_REQUIRED")

    def test_role_separation_and_lifecycle_are_durable(self):
        bp=(ROOT/"docs/vnext/MASTER_BLUEPRINT_V1_20261006.md").read_text(encoding="utf-8")
        law=(ROOT/"docs/vnext/FOUNDATION_LAW_CONSOLIDATED_V1_20261006.md").read_text(encoding="utf-8")
        for token in ["Owner","Architect","Builder / Implementer","Supervisor / Inspector","Independent Reviewer / Critic","Evidence / Validation Layer"]:
            self.assertIn(token,bp)
        self.assertIn("DESIGN -> LAW CHECK -> TASK AUTHORIZE -> BUILD -> SUPERVISE -> VALIDATE",bp)
        self.assertIn("Architect: designs and maintains the Master Blueprint but cannot self-accept",law)
        self.assertIn("Builder/Implementer: implements bounded approved work but cannot self-certify",law)

    def test_recovery_entrypoint_reads_blueprint_before_state(self):
        text=(ROOT/"docs/vnext/continuity/RECOVERY_ENTRYPOINT_V1.md").read_text(encoding="utf-8")
        self.assertIn("Read the `master_blueprint` routed by the boot root.",text)

if __name__=="__main__":
    unittest.main()
