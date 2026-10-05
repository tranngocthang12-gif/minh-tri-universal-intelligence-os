import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class T1LexicalReviewTests(unittest.TestCase):
    def load(self, rel):
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))

    def test_whole_audit_evidence_remains_pending(self):
        for rel in [
            "knowledge/buddhist/atoms/bud-atthaka-lex01-evidence.json",
            "knowledge/buddhist/atoms/bud-atthaka-lex02-evidence.json",
        ]:
            atom = self.load(rel)
            self.assertEqual(atom["record_type"], "evidence")
            self.assertEqual(atom["status"], "PENDING_REVIEW")

    def test_promoted_claims_are_narrow_t1_reviewed_atoms(self):
        rels = [
            "knowledge/buddhist/atoms/bud-atthaka-sn874-sanna-papancasankha-relation.json",
            "knowledge/buddhist/atoms/bud-atthaka-sn842-mannati-comparison-dispute.json",
            "knowledge/buddhist/atoms/bud-atthaka-sn4-12-view-truth-claim-dispute.json",
        ]
        for rel in rels:
            atom = self.load(rel)
            self.assertEqual(atom["record_type"], "claim")
            self.assertEqual(atom["status"], "ACTIVE")
            self.assertEqual(atom["class"], "ATTESTED")
            self.assertEqual(atom["provenance"]["review_level"], "T1")
            self.assertEqual(atom["depends_on"], [])
            self.assertTrue(any("SALVAGED" in ref for ref in atom["source_refs"]))

    def test_index_contains_promoted_claims_and_pending_audits(self):
        index = self.load("knowledge/index.json")
        atoms = {a["id"]: a for a in index["atoms"]}
        self.assertEqual(atoms["bud:atthaka:lex01:ditthi-sacca-audit-evidence"]["status"], "PENDING_REVIEW")
        self.assertEqual(atoms["bud:atthaka:lex02:sanna-mannati-audit-evidence"]["status"], "PENDING_REVIEW")
        self.assertEqual(atoms["bud:atthaka:sn874:sanna-papancasankha-relation"]["status"], "ACTIVE")
        self.assertEqual(atoms["bud:atthaka:sn842:mannati-comparison-dispute"]["status"], "ACTIVE")
        self.assertEqual(atoms["bud:atthaka:sn4_12:view-truth-claim-dispute"]["status"], "ACTIVE")

    def test_active_claims_do_not_depend_on_pending_atoms(self):
        atoms = {}
        for path in (ROOT / "knowledge").rglob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("schema") == "minhtri-knowledge-atom/v1":
                atoms[data["id"]] = data
        for atom in atoms.values():
            if atom.get("status") != "ACTIVE":
                continue
            for dep_id in atom.get("depends_on", []):
                self.assertIn(dep_id, atoms)
                self.assertNotEqual(atoms[dep_id].get("status"), "PENDING_REVIEW")

    def test_review_document_preserves_open_uncertainties(self):
        text = (ROOT / "docs" / "vnext" / "history" / "BUDDHIST_T1_LEXICAL_REVIEW_216_230_20261006.md").read_text(encoding="utf-8")
        self.assertIn("Remain PENDING_REVIEW / UNCERTAIN", text)
        self.assertIn("NARROW_PASS_FOR_LISTED_CLAIMS", text)
        self.assertIn("does not mean", text)


if __name__ == "__main__":
    unittest.main()
