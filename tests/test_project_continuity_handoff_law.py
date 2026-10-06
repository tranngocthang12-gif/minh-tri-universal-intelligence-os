from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ProjectContinuityHandoffLawTests(unittest.TestCase):
    def test_bootstrap_has_foundational_handoff_law(self):
        text = (ROOT / "docs" / "GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md").read_text(encoding="utf-8")
        self.assertIn("PROJECT-WIDE CONTINUITY & MANDATORY HANDOFF LAW", text)
        self.assertIn("LAW-FIRST gate", text)
        self.assertIn("NO UNIQUE STATE IN CHAT", text)
        self.assertIn("HANDOFF IS CONTINUOUS, NOT AN END-OF-CHAT CEREMONY", text)
        self.assertIn("MANDATORY HANDOFF CONTRACT", text)
        self.assertIn("NEW-SEAT RECOVERY RULE", text)
        self.assertIn("STALE / MISSING / CONFLICTING HANDOFF — FAIL CLOSED", text)
        self.assertIn("ARCHITECTURE FOUNDATION GATE", text)

    def test_law_index_routes_foundational_handoff(self):
        text = (ROOT / "docs" / "LAW_INDEX_20261003.md").read_text(encoding="utf-8")
        self.assertIn("GitHub First + project-wide continuity/handoff", text)
        self.assertIn("continuous checkpoint", text)
        self.assertIn("NEXT ACTION", text)
        self.assertIn("architecture mutation bị BLOCKED", text)

    def test_law_index_does_not_hardcode_obsolete_architecture_pointer(self):
        text = (ROOT / "docs" / "LAW_INDEX_20261003.md").read_text(encoding="utf-8")
        self.assertIn("state/current.yaml.current_architecture", text)
        current_block = text.split("## Current architecture", 1)[1].split("## Historical / superseded records", 1)[0]
        self.assertNotIn("Read `ARCHITECTURE_NOW_20261003.md`", current_block)

    def test_vnext_cannot_claim_complete_without_zero_chat_recovery(self):
        text = (ROOT / "docs" / "vnext" / "ARCHITECTURE_VNEXT_OWNER_APPROVED_CANDIDATE_20261006.md").read_text(encoding="utf-8")
        self.assertIn("Law-first foundation gate", text)
        self.assertIn("zero-chat seat", text)
        self.assertIn("exact NEXT ACTION", text)

    def test_handoff_contract_contains_minimum_recovery_fields(self):
        text = (ROOT / "docs" / "GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md").read_text(encoding="utf-8")
        for required in [
            "TASK_ID",
            "last verified canonical main SHA",
            "working branch, base SHA, head SHA, and PR number",
            "what is DONE",
            "what is NOT DONE",
            "NEXT ACTION",
            "canonical main state",
            "unmerged branch/candidate state",
        ]:
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
