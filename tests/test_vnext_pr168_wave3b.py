import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PR168Wave3BTests(unittest.TestCase):
    def load(self, rel):
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))

    def test_wave3b_bundle_is_pending_review(self):
        atom = self.load("knowledge/buddhist/atoms/bud-pr168-sn22-sn35-sn45-sn46-structural-index-bundle-wave3b.json")
        self.assertEqual(atom["status"], "PENDING_REVIEW")
        self.assertEqual(atom["record_type"], "evidence")
        self.assertEqual(atom["provenance"]["source_pr"], 168)
        self.assertEqual(atom["provenance"]["salvage_wave"], "3B")

    def test_exact_blob_provenance_is_pinned(self):
        atom = self.load("knowledge/buddhist/atoms/bud-pr168-sn22-sn35-sn45-sn46-structural-index-bundle-wave3b.json")
        locators = {x["locator"] for x in atom["evidence_refs"]}
        expected = {
            "EARLY_BUDDHIST_SN22_ID_INDEX_V0_1.json @ blob 5b2ecaa2f6f81a883a0f4a5c7b5e657e0a969d2d",
            "EARLY_BUDDHIST_SN35_ID_INDEX_V0_1.json @ blob b8de6ffb140e39f70aa1515c49cc6dc0b1dec956",
            "EARLY_BUDDHIST_SN45_ID_INDEX_V0_1.json @ blob 7ee08ed6f94d32b73d4714dd65424f55ce8abb2f",
            "EARLY_BUDDHIST_SN46_ID_INDEX_V0_1.json @ blob cd751aa84a15ad11ef1a67778363f54e644022ca",
        }
        self.assertTrue(expected.issubset(locators))

    def test_structural_coverage_is_not_promoted_to_mastery(self):
        doc = (ROOT / "docs" / "vnext" / "history" / "PR168_CONTROLLED_SALVAGE_WAVE3B_20261006.md").read_text(encoding="utf-8")
        self.assertIn("does not establish completeness", doc)
        self.assertIn("may not by themselves establish doctrinal claims", doc)

    def test_wave4_followup_is_registered(self):
        tasks = self.load("state/tasks.yaml")
        by_id = {t["task_id"]: t for t in tasks["tasks"]}
        task = by_id["ARCH-VNEXT-SALVAGE-PR168-WAVE4"]
        self.assertIn(task["status"], {"READY", "IN_PROGRESS", "DONE"})
        self.assertIn("MILINDAPANHA", " ".join(task["scope"]))

    def test_bundle_is_in_generated_index(self):
        index = self.load("knowledge/index.json")
        atoms = {a["id"]: a for a in index["atoms"]}
        self.assertEqual(
            atoms["bud:pr168:sn22-sn35-sn45-sn46-structural-index-bundle-wave3b"]["status"],
            "PENDING_REVIEW",
        )


if __name__ == "__main__":
    unittest.main()
