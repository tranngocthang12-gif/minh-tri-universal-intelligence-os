import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class VNextLexicalSalvageTests(unittest.TestCase):
    def load(self, rel):
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))

    def test_salvaged_lexical_evidence_is_pending_review(self):
        a = self.load("knowledge/buddhist/atoms/bud-atthaka-lex01-evidence.json")
        b = self.load("knowledge/buddhist/atoms/bud-atthaka-lex02-evidence.json")
        self.assertEqual(a["record_type"], "evidence")
        self.assertEqual(b["record_type"], "evidence")
        self.assertEqual(a["status"], "PENDING_REVIEW")
        self.assertEqual(b["status"], "PENDING_REVIEW")
        self.assertEqual(a["provenance"]["source_pr"], 216)
        self.assertEqual(b["provenance"]["source_pr"], 230)

    def test_source_head_and_blob_provenance_is_pinned(self):
        a = self.load("knowledge/buddhist/atoms/bud-atthaka-lex01-evidence.json")
        b = self.load("knowledge/buddhist/atoms/bud-atthaka-lex02-evidence.json")
        self.assertEqual(a["provenance"]["source_head_sha"], "6bc822b3361fbb9fa99622073c08cb369053f121")
        self.assertEqual(a["provenance"]["source_blob_sha"], "d442d90a88cbbf472a36d84d0e430c86bcb7e796")
        self.assertEqual(b["provenance"]["source_head_sha"], "a3a254c3b6598484b7165fb8bff86e5755f740fb")
        self.assertEqual(b["provenance"]["source_blob_sha"], "a1275558b11b3c89993daef8f015507892d552fb")

    def test_active_hubs_do_not_depend_on_pending_lexical_evidence(self):
        index = self.load("knowledge/index.json")
        pending = {
            a["id"]
            for a in index["atoms"]
            if a["status"] == "PENDING_REVIEW"
        }
        for hub in index["hubs"]:
            if hub["status"] == "ACTIVE":
                self.assertTrue(set(hub["depends_on_claims"]).isdisjoint(pending))

    def test_raw_salvage_files_preserve_nonpromotion_boundary(self):
        for rel in [
            "knowledge/buddhist/evidence/PHAT_ATTHAKA_LEX_01_PR216_SALVAGED_20261006.md",
            "knowledge/buddhist/evidence/PHAT_ATTHAKA_LEX_02_PR230_SALVAGED_20261006.md",
        ]:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("PENDING_REVIEW_EVIDENCE", text)
            self.assertIn("not ACTIVE knowledge", text)


if __name__ == "__main__":
    unittest.main()
