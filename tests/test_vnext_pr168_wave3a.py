import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PR168Wave3ATests(unittest.TestCase):
    def load(self, rel):
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))

    def test_bundle_atom_is_pending_review(self):
        atom = self.load("knowledge/buddhist/atoms/bud-pr168-structural-source-audit-bundle-wave3a.json")
        self.assertEqual(atom["record_type"], "evidence")
        self.assertEqual(atom["status"], "PENDING_REVIEW")
        self.assertEqual(atom["provenance"]["source_pr"], 168)
        self.assertEqual(atom["provenance"]["source_head_sha"], "80889a3e6b83f1cb4742b1abe3e796ddfc42ce76")
        self.assertEqual(atom["provenance"]["salvage_wave"], "3A")

    def test_exact_blob_provenance_is_recorded(self):
        atom = self.load("knowledge/buddhist/atoms/bud-pr168-structural-source-audit-bundle-wave3a.json")
        locators = {x["locator"] for x in atom["evidence_refs"]}
        expected = {
            "EARLY_BUDDHIST_ATTHAKAVAGGA_INDEX_V0_1.json @ blob 8d316bb2d31e4ebb81c9961ce37cb7feceddfdc8",
            "EARLY_BUDDHIST_ATTHAKAVAGGA_VERSE_AUDIT_V0_2.json @ blob ddae5ca5a868b9f86e962b59128d36fc48ba0804",
            "EARLY_BUDDHIST_MN_DIALOGUE_INDEX_V0_1.json @ blob e8e23a0f07272233e9cf7492aa88edfea3723885",
            "EARLY_BUDDHIST_SN36_DISCOURSE_INDEX_V0_1.json @ blob 7ed3cc15d27b56283afb511e78952ec0bd5943f0",
            "EARLY_BUDDHIST_TRANSLATION_CARDS_V0_2.json @ blob 841003cd68b90c6d7d8eebee22c60507b22c021e",
            "EARLY_BUDDHIST_TRANSLATION_CONTRADICTION_LEDGER_V0_1.json @ blob cb56c254f593b6cf3f2c2de5a1250268c04f670e",
            "EARLY_BUDDHIST_WHOLE_CORPUS_INDEX_V0_1.json @ blob 34b1607c7a8494cbbb638193850f1c35df773e7c",
        }
        self.assertTrue(expected.issubset(locators))

    def test_old_project_state_is_not_salvaged_as_current_state(self):
        inventory = (ROOT / "docs" / "vnext" / "history" / "PR168_CONTROLLED_SALVAGE_INVENTORY_20261006.md").read_text(encoding="utf-8")
        self.assertIn("REJECT_AS_CURRENT_STATE", inventory)
        self.assertIn("No status phrase", inventory)

    def test_large_sn_indexes_are_split_into_wave3b(self):
        tasks = self.load("state/tasks.yaml")
        by_id = {t["task_id"]: t for t in tasks["tasks"]}
        task = by_id["ARCH-VNEXT-SALVAGE-PR168-WAVE3B"]
        self.assertIn(task["status"], {"READY", "IN_PROGRESS", "DONE"})
        scope = " ".join(task["scope"])
        for marker in ["SN22", "SN35", "SN45", "SN46"]:
            self.assertIn(marker, scope)

    def test_bundle_is_in_generated_index(self):
        index = self.load("knowledge/index.json")
        atoms = {a["id"]: a for a in index["atoms"]}
        self.assertEqual(
            atoms["bud:pr168:structural-source-audit-bundle-wave3a"]["status"],
            "PENDING_REVIEW",
        )


if __name__ == "__main__":
    unittest.main()
