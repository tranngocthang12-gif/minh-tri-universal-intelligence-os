import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class CollisionReviewTests(unittest.TestCase):
    def load(self, rel):
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))

    def test_collision_atoms_have_expected_status(self):
        active = [
            "knowledge/buddhist/atoms/bud-sn35-31-mannati-relations.json",
            "knowledge/buddhist/atoms/bud-sn22-64-mannati-mara-bondage.json",
        ]
        pending = [
            "knowledge/buddhist/atoms/bud-legacy-pr232-papanca-boundary-evidence.json",
            "knowledge/buddhist/atoms/bud-legacy-pr233-nissaya-range-evidence.json",
        ]
        for rel in active:
            atom=self.load(rel)
            self.assertEqual(atom["record_type"], "claim")
            self.assertEqual(atom["status"], "ACTIVE")
            self.assertEqual(atom["class"], "ATTESTED")
            self.assertEqual(atom["provenance"]["review_level"], "T1")
        for rel in pending:
            atom=self.load(rel)
            self.assertEqual(atom["record_type"], "evidence")
            self.assertEqual(atom["status"], "PENDING_REVIEW")

    def test_no_checkpoint_number_identity(self):
        text=(ROOT/"docs/vnext/history/BUDDHIST_A162_A165_COLLISION_T1_REVIEW_20261006.md").read_text(encoding="utf-8")
        self.assertIn("Checkpoint number is therefore chronology only, not semantic identity.", text)
        self.assertIn("No legacy branch is merged wholesale.", text)

    def test_index_contains_collision_review_atoms(self):
        index=self.load("knowledge/index.json")
        atoms={a["id"]:a for a in index["atoms"]}
        self.assertEqual(atoms["bud:sn35.31:mannati-relational-conceiving"]["status"], "ACTIVE")
        self.assertEqual(atoms["bud:sn22.64:mannati-mara-bondage"]["status"], "ACTIVE")
        self.assertEqual(atoms["bud:legacy-pr232:papanca-early-late-boundary-evidence"]["status"], "PENDING_REVIEW")
        self.assertEqual(atoms["bud:legacy-pr233:nissaya-lexical-range-evidence"]["status"], "PENDING_REVIEW")

if __name__ == "__main__":
    unittest.main()
