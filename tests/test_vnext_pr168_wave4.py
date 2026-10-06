import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PR168Wave4Tests(unittest.TestCase):
    def load(self, rel):
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))

    def test_parallel_bundle_is_pending_review(self):
        atom = self.load("knowledge/buddhist/atoms/bud-pr168-parallel-translation-lexical-wave4-evidence.json")
        self.assertEqual(atom["record_type"], "evidence")
        self.assertEqual(atom["status"], "PENDING_REVIEW")
        self.assertEqual(atom["provenance"]["source_pr"], 168)

    def test_milinda_is_later_paracanonical_and_pending(self):
        atom = self.load("knowledge/buddhist/atoms/bud-pr168-milindapanha-reasoning-lab-wave4-evidence.json")
        self.assertEqual(atom["status"], "PENDING_REVIEW")
        self.assertEqual(atom["provenance"]["epistemic_layer"], "LATER_PARACANONICAL")

    def test_wave4_does_not_promote_active_claims(self):
        index = self.load("knowledge/index.json")
        ids = {
            "bud:pr168:parallel-translation-lexical-wave4-evidence",
            "bud:pr168:milindapanha-reasoning-lab-wave4-evidence",
        }
        found = {a["id"]: a for a in index["atoms"] if a["id"] in ids}
        self.assertEqual(set(found), ids)
        for atom in found.values():
            self.assertEqual(atom["status"], "PENDING_REVIEW")

    def test_final_disposition_task_is_ready(self):
        tasks = self.load("state/tasks.yaml")
        by_id = {t["task_id"]: t for t in tasks["tasks"]}
        self.assertEqual(by_id["ARCH-VNEXT-SALVAGE-PR168-FINAL-DISPOSITION"]["status"], "READY")

    def test_document_preserves_milinda_boundary(self):
        text = (ROOT / "docs" / "vnext" / "history" / "PR168_CONTROLLED_SALVAGE_WAVE4_20261006.md").read_text(encoding="utf-8")
        self.assertIn("later/paracanonical", text)
        self.assertIn("never overrides early-text evidence", text)
        self.assertIn("does not prove", text)


if __name__ == "__main__":
    unittest.main()
