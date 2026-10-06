import json
import unittest
from pathlib import Path

from tools.score_retrieval_application_eval import score

ROOT = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def valid_response():
    gold = load("eval/retrieval_application/v1/gold.json")
    return {
        "schema": "minhtri-retrieval-application-response/v1",
        "set_id": gold["set_id"],
        "attestations": {
            "fresh_seat": True,
            "used_prior_chat_history": False,
            "read_gold": False,
        },
        "answers": [
            {
                "qid": x["qid"],
                "decision": x["decision"],
                "record_ids": list(x["required_record_ids"]),
                "answer": "Structured application decision from supplied canonical snapshot.",
            }
            for x in gold["answers"]
        ],
    }


class RetrievalApplicationProofV1Tests(unittest.TestCase):
    def test_valid_structured_response_passes(self):
        gold = load("eval/retrieval_application/v1/gold.json")
        result = score(gold, valid_response())
        self.assertEqual(result["status"], "PASS", result)

    def test_superseded_decoy_use_fails(self):
        gold = load("eval/retrieval_application/v1/gold.json")
        value = valid_response()
        a1 = next(x for x in value["answers"] if x["qid"] == "A1")
        a1["record_ids"] = ["decoy:bud:a172:identity-shame-attested"]
        result = score(gold, value)
        self.assertEqual(result["status"], "FAIL")

    def test_pending_review_as_established_support_fails_decision(self):
        gold = load("eval/retrieval_application/v1/gold.json")
        value = valid_response()
        a2 = next(x for x in value["answers"] if x["qid"] == "A2")
        a2["decision"] = "USE_AS_SYNTHESIS"
        result = score(gold, value)
        self.assertEqual(result["status"], "FAIL")

    def test_missing_identification_requirement_fails(self):
        gold = load("eval/retrieval_application/v1/gold.json")
        value = valid_response()
        a3 = next(x for x in value["answers"] if x["qid"] == "A3")
        a3["decision"] = "REQUIRE_REVIEW"
        result = score(gold, value)
        self.assertEqual(result["status"], "FAIL")

    def test_silent_supersession_fails(self):
        gold = load("eval/retrieval_application/v1/gold.json")
        value = valid_response()
        a4 = next(x for x in value["answers"] if x["qid"] == "A4")
        a4["decision"] = "REQUIRE_REVIEW"
        result = score(gold, value)
        self.assertEqual(result["status"], "FAIL")

    def test_disputed_dependency_must_be_rejected(self):
        gold = load("eval/retrieval_application/v1/gold.json")
        value = valid_response()
        a5 = next(x for x in value["answers"] if x["qid"] == "A5")
        a5["decision"] = "REQUIRE_REVIEW"
        result = score(gold, value)
        self.assertEqual(result["status"], "FAIL")

    def test_gold_is_not_embedded_in_packet(self):
        packet = load("eval/retrieval_application/v1/packet.json")
        self.assertNotIn("gold", packet)
        self.assertNotIn("answers", packet)


if __name__ == "__main__":
    unittest.main()
