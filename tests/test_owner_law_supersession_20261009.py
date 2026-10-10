"""MT Owner law supersession: scenario-aware, proposal-bound checks (LAW-01..LAW-10)."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "docs/vnext/FOUNDATION_LAW_CONSOLIDATED_V1_20261006.md"
BLUEPRINT = ROOT / "docs/vnext/MASTER_BLUEPRINT_V1_20261006.md"
LEARNING = ROOT / "docs/LAW_UNIVERSAL_LEARNING_CONTINUITY_20261004.md"
RECOVERY = ROOT / "docs/vnext/continuity/RECOVERY_ENTRYPOINT_V1.md"
DECISION = ROOT / "docs/vnext/OWNER_DECISION_LAW_SUPERSESSION_20261009.md"
REGISTER = ROOT / "docs/vnext/red_team/OWNER_LAW_SUPERSESSION_CONFLICT_REGISTER_20261009.md"

def resolves(old_rank, new_rank, same_subject, actual_conflict, old_time, new_time, competent=True, promulgated=True):
    """Pure law-case scenario checker. Rank lower integer = higher authority.
    An acceptance receipt is assessed separately; this function is NOT a legal engine."""
    valid = competent and promulgated and new_rank <= old_rank and new_time >= old_time
    return "PARTIAL_SUPERSESSION" if valid and same_subject and actual_conflict else "OLD_RETAINED"

class OwnerLawSupersessionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.router = ROUTER.read_text(encoding="utf-8")
        cls.blueprint = BLUEPRINT.read_text(encoding="utf-8")
        cls.learning = LEARNING.read_text(encoding="utf-8")
        cls.recovery = RECOVERY.read_text(encoding="utf-8")
        cls.decision = DECISION.read_text(encoding="utf-8")
        cls.register = REGISTER.read_text(encoding="utf-8")
        cls.current = json.loads((ROOT/"state/current.yaml").read_text(encoding="utf-8"))
        cls.tasks = json.loads((ROOT/"state/tasks.yaml").read_text(encoding="utf-8"))["tasks"]

    def test_law_01_competent_new_same_level_conflicting_clause_displaced(self):
        self.assertEqual(resolves(2,2,True,True,1,2),"PARTIAL_SUPERSESSION")
        self.assertIn("automatically displaces",self.router)

    def test_law_02_nonconflicting_old_rule_retained(self):
        self.assertEqual(resolves(2,2,True,False,1,2),"OLD_RETAINED")
        self.assertEqual(resolves(2,2,False,True,1,2),"OLD_RETAINED")
        self.assertIn("Nonconflicting older provisions remain valid",self.router)

    def test_law_03_lower_authority_cannot_override_higher(self):
        self.assertEqual(resolves(1,3,True,True,1,2),"OLD_RETAINED")
        self.assertEqual(resolves(1,1,True,True,1,2,competent=False),"OLD_RETAINED")
        self.assertEqual(resolves(1,1,True,True,1,2,promulgated=False),"OLD_RETAINED")
        self.assertEqual(resolves(1,1,True,True,3,2),"OLD_RETAINED")

    def test_law_04_unmerged_pr_not_durable_authority(self):
        boot=json.loads((ROOT/"state/bootstrap.json").read_text(encoding="utf-8"))
        self.assertEqual(boot["law_precedence"],"docs/vnext/FOUNDATION_LAW_CONSOLIDATED_V1_20261006.md")
        self.assertIn("candidate until",self.router)
        self.assertIn("unmerged law PRs",self.recovery)

    def test_law_05_builder_granted_is_not_owner_acceptance(self):
        self.assertIn('Builder-authored "GRANTED"',self.router)
        task=next(t for t in self.tasks if t["task_id"]=="MT-OWNER-LAW-SUPERSESSION-20261009")
        self.assertEqual(task["acceptance_authority"],"OWNER")
        self.assertIn("CANDIDATE_ONLY_NOT_ACCEPTED",task["governance_phase"])

    def test_law_06_historical_text_retained_not_operational(self):
        self.assertIn("Preserve the superseded text",self.router)
        self.assertIn("old git blob remains evidence",self.register.lower())

    def test_law_07_uncertain_scope_blocks_only_affected_mutation(self):
        self.assertIn("affected mutation",self.router)
        self.assertIn("read-only",self.router)
        self.assertIn("read-only learning continues",self.blueprint)

    def test_law_08_recovery_resolves_effective_law_not_candidate(self):
        self.assertIn("sole",self.recovery)
        self.assertIn("unmerged law PRs",self.recovery)
        self.assertIn("fresh-seat recovery",self.router)
        # This unit check is NOT independent post-merge fresh-seat recovery.

    def test_law_09_early_discourse_and_milinda_still_mandatory(self):
        self.assertIn("Milindapañha",self.learning)
        self.assertIn("early discourses",self.learning)
        self.assertIn("NO conflict",self.register)
        self.assertEqual(self.current["foundation_status"],"FROZEN")

    def test_law_10_class_f_gate_and_no_auto_merge(self):
        self.assertIn("Owner acceptance",self.router)
        self.assertIn("Independent Reviewer/Critic",self.router)
        task=next(t for t in self.tasks if t["task_id"]=="MT-OWNER-LAW-SUPERSESSION-20261009")
        self.assertEqual(task["change_class"],"F")
        self.assertEqual(task["acceptance_authority"],"OWNER")
        self.assertIn("NO_MERGE",task["blocker"])
        self.assertIn("FROZEN",self.decision)
