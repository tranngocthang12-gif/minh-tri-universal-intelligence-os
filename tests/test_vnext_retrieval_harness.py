import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class RetrievalHarnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet_mod = load_module(
            "build_retrieval_packet",
            ROOT / "tools" / "build_retrieval_eval_packet.py",
        )
        cls.scorer_mod = load_module(
            "score_retrieval",
            ROOT / "tools" / "score_retrieval_eval.py",
        )
        cls.questions = json.loads(
            (ROOT / "eval" / "retrieval" / "v1" / "questions.json").read_text(encoding="utf-8")
        )
        cls.gold = json.loads(
            (ROOT / "eval" / "retrieval" / "v1" / "gold.json").read_text(encoding="utf-8")
        )
        cls.decoys = json.loads(
            (ROOT / "eval" / "retrieval" / "v1" / "decoys.json").read_text(encoding="utf-8")
        )

    def test_question_and_gold_sets_match(self):
        qids = [x["qid"] for x in self.questions["items"]]
        gold_qids = [x["qid"] for x in self.gold["answers"]]
        self.assertEqual(qids, gold_qids)
        self.assertEqual(len(qids), len(set(qids)))

    def test_decoys_are_noncanonical_and_outside_knowledge_store(self):
        self.assertTrue(self.decoys["synthetic_noncanonical"])
        for record in self.decoys["records"]:
            self.assertTrue(record["id"].startswith("decoy:"))

    def test_packet_contains_questions_knowledge_and_decoys_but_not_gold(self):
        packet = self.packet_mod.build_packet(ROOT)
        self.assertIn("questions", packet)
        self.assertIn("knowledge_snapshot", packet)
        self.assertIn("decoys", packet)
        self.assertNotIn("gold", packet)

    def test_gold_rejects_forbidden_decoy_use(self):
        fake = {
            "answers": [
                {"qid": "Q1", "answer_status": "SUPPORTED", "record_ids": ["decoy:bud:a172:identity-shame-attested"]},
                {"qid": "Q2", "answer_status": "PENDING_REVIEW", "record_ids": ["bud:a172:hiri-lexical-open"]},
                {"qid": "Q3", "answer_status": "SUPPORTED", "record_ids": ["econ:program:identification-assumptions"]},
                {"qid": "Q4", "answer_status": "UNSUPPORTED", "record_ids": []},
                {"qid": "Q5", "answer_status": "SUPPORTED", "record_ids": ["bud:a172:identity-shame-synthesis"]},
            ]
        }
        result = self.scorer_mod.score(self.gold, fake)
        q1 = next(x for x in result["results"] if x["qid"] == "Q1")
        self.assertFalse(q1["pass"])

    def test_authoring_seat_cannot_claim_memory_pass(self):
        doc = (ROOT / "docs" / "vnext" / "ARCHITECTURE_VNEXT_PHASE4_RETRIEVAL_HARNESS_20261006.md").read_text(encoding="utf-8")
        self.assertIn("NOT A MEMORY PASS", doc)
        self.assertIn("different fresh seat", doc)


if __name__ == "__main__":
    unittest.main()
