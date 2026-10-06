from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BuddhistMilindaTeacherLearningLawTests(unittest.TestCase):
    def test_canonical_law_retains_teacher_explanation_as_reusable_understanding(self):
        text = (ROOT / "docs" / "LAW_UNIVERSAL_LEARNING_CONTINUITY_20261004.md").read_text(encoding="utf-8")
        self.assertIn("Teacher-explanation learning rule", text)
        self.assertIn("Understanding and source provenance are separate layers", text)
        self.assertIn("LATER_EXPLANATORY_EARLY_COMPATIBLE", text)
        self.assertIn("not understood → explanation → understood model → durable record → reuse → countercheck → correction/supersession when needed", text)

    def test_law_index_routes_same_rule(self):
        text = (ROOT / "docs" / "LAW_INDEX_20261003.md").read_text(encoding="utf-8")
        self.assertIn("teacher-explanation learning rule", text)
        self.assertIn("understanding + provenance separately", text)
        self.assertIn("LATER_EXPLANATORY_EARLY_COMPATIBLE", text)

    def test_early_discourse_priority_is_not_weakened(self):
        text = (ROOT / "docs" / "LAW_UNIVERSAL_LEARNING_CONTINUITY_20261004.md").read_text(encoding="utf-8")
        self.assertIn("early discourses are the main attestation axis", text)
        self.assertIn("does not override early-discourse evidence", text)
        self.assertIn("No later explanation is protected from correction", text)


if __name__ == "__main__":
    unittest.main()
