"""Static routing/contract guard for shared learning method. Does not certify mastery."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")

class UnifiedLearningMethodTests(unittest.TestCase):
    def test_single_existing_normative_learning_law(self):
        law = read("docs/LAW_UNIVERSAL_LEARNING_CONTINUITY_20261004.md")
        self.assertEqual(law.count("## 2A. ONE shared learning method"), 1)
        for marker in ("RECOVER.", "READ THE SOURCES.", "CONSULT THE EXPLANATORY LAYER.",
                       "REASON AND CHALLENGE.", "CONNECT AND TRANSFER.", "RECORD.",
                       "READ BACK AND RECOVER.", "G1 SOURCE ASSURANCE",
                       "G2 UNDERSTANDING ASSURANCE", "G3 DURABLE CONTINUITY"):
            self.assertIn(marker, law)
        self.assertIn("## 7A. Buddhist-study mandatory Milindapañha rule", law)
        self.assertIn("No direct-main mutation", law)

    def test_bootstrap_and_recovery_share_same_law_route(self):
        law_ref = "docs/LAW_UNIVERSAL_LEARNING_CONTINUITY_20261004.md"
        for path in ("docs/GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md",
                     "docs/vnext/continuity/RECOVERY_ENTRYPOINT_V1.md",
                     "docs/learning/LEARNING_SEAT_WORKSHEET_V1.md"):
            text = read(path)
            self.assertIn(law_ref, text)
            self.assertTrue("§2A" in text or "section 2A" in text, path)
        boot = json.loads(read("state/bootstrap.json"))
        self.assertEqual(boot["durable_continuity_authority"], "GITHUB_PROTECTED_MAIN")
        self.assertEqual(boot["task_registry"], "state/tasks.yaml")

    def test_no_status_invention_no_chats_as_authority(self):
        law = read("docs/LAW_UNIVERSAL_LEARNING_CONTINUITY_20261004.md")
        worksheet = read("docs/learning/LEARNING_SEAT_WORKSHEET_V1.md")
        for status in ("PENDING_REVIEW", "ACTIVE", "UNCERTAIN", "DISPUTED", "SUPERSEDED", "REFUTED"):
            self.assertIn(status, law)
        for marker in ("TEXT_ATTESTED", "CROSS_TEXT_SYNTHESIS", "LATER/PARACANONICAL", "UNCERTAINTY"):
            self.assertIn(marker, worksheet)
        self.assertIn("another chat", law.lower())
        self.assertIn("A205/A206", worksheet)
        self.assertIn("zero-chat", law)

    def test_pc_offline_is_not_a_github_learning_blocker(self):
        law = read("docs/LAW_UNIVERSAL_LEARNING_CONTINUITY_20261004.md")
        self.assertIn("## 2B. PC-OFFLINE CONTINUITY", law)
        self.assertIn("GitHub protected main alone remains durable canonical authority", law)
        self.assertIn("NOT YET DURABLY RECORDED", law)
        self.assertIn("LOCAL_BRAIN_MIRROR=NOT_WRITTEN", law)
        worksheet = read("docs/learning/LEARNING_SEAT_WORKSHEET_V1.md")
        recovery = read("docs/vnext/continuity/RECOVERY_ENTRYPOINT_V1.md")
        self.assertIn("PC-offline operating mode", worksheet)
        self.assertIn("PC independence note", recovery)
        current = json.loads(read("state/current.yaml"))
        self.assertEqual(current["pc_local_brain_role"], "NON_CANONICAL_EXECUTION_AND_MIRROR_SIDECAR")

    def test_does_not_mutate_canonical_task_or_checkpoint(self):
        current = json.loads(read("state/current.yaml"))
        registry = json.loads(read("state/tasks.yaml"))
        self.assertEqual(current["foundation_status"], "FROZEN")
        # A Class F learning-law proposal must not fix, prescribe, or freeze
        # operational Class S routing. Compatible with either main or an
        # independently accepted future A173 routing repair.
        self.assertIn(current["active_task_id"], {t["task_id"] for t in registry["tasks"]})
        active = {t["task_id"]: t for t in registry["tasks"]}[current["active_task_id"]]
        self.assertIn(active["status"], registry["task_states"])
        item = {t["task_id"]: t for t in registry["tasks"]}["BUDDHIST-A173"]
        self.assertIn(item["status"], registry["task_states"])
        self.assertIn(item["change_class"], {"UNCLASSIFIED_LEGACY", "D"})
        inventory = read("docs/learning/BUDDHIST_CROSS_CHAT_CHECKPOINT_RECONCILIATION_20261009.md")
        self.assertIn("NOT COMPLETED", inventory)
        self.assertIn("PR #342", inventory)

if __name__ == "__main__":
    unittest.main()
