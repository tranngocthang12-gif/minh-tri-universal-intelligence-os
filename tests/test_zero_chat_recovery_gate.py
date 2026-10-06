import json
import unittest
from pathlib import Path

from tools.score_zero_chat_recovery import score_response

ROOT = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def valid_response():
    challenge = load("eval/recovery/v1/challenge.json")
    facts = load("eval/recovery/v1/gold.json")["required_facts"]
    return {
        "schema": "minhtri-zero-chat-recovery-response/v1",
        "challenge_id": challenge["challenge_id"],
        "challenge_nonce": challenge["challenge_nonce"],
        "attestations": {
            "separate_zero_chat": True,
            "used_prior_chat_history": False,
            "read_gold": False,
        },
        "foundation_law": {
            "source_ref": facts["law_source_ref"],
            "routed_by_ref": facts["law_routed_by_ref"],
        },
        "active_task": {
            "task_id": facts["active_task_id"],
            "status": facts["active_status"],
            "handoff_ref": facts["handoff_ref"],
            "blocker": facts["blocker"],
        },
        "claims": {
            "core_v1_complete": False,
            "autonomous_learning_proven": False,
            "chat_memory_canonical": False,
        },
        "evidence_refs": list(facts["required_evidence_refs"]),
        "answers": {
            "Q1": "The project-wide continuity and handoff law is in GITHUB_FIRST_ROLE_BOOTSTRAP section 8 and is routed by LAW_INDEX.",
            "Q2": "ARCH-VNEXT-CONTINUITY-HANDOFF-CORE-V1 is BLOCKED.",
            "Q3": "Canonical main is authoritative; unmerged branch or PR work is candidate state.",
            "Q4": "DONE: static continuity machinery. NOT DONE: the genuine fresh-seat behavioral proof.",
            "Q5": "Run a genuine zero-chat fresh seat, answer from canonical records, and grade the response independently before continuing.",
            "Q6": "Core v1 completion, autonomous learning, and chat memory authority are not proven.",
        },
    }


class ZeroChatRecoveryGateTests(unittest.TestCase):
    def test_challenge_routes_to_structured_gate(self):
        challenge = load("eval/recovery/v1/challenge.json")
        self.assertEqual(challenge["response_schema_ref"], "eval/recovery/v1/response.schema.json")
        self.assertEqual(challenge["grader_ref"], "tools/score_zero_chat_recovery.py")
        self.assertIn("eval/recovery/v1/gold.json", challenge["do_not_read"])
        self.assertTrue(challenge["required_rules"]["return_only_json"])

    def test_gold_is_historical_snapshot_not_current_state_alias(self):
        facts = load("eval/recovery/v1/gold.json")["required_facts"]
        current = load("state/current.yaml")
        self.assertEqual(facts["active_task_id"], "ARCH-VNEXT-CONTINUITY-HANDOFF-CORE-V1")
        self.assertNotEqual(facts["active_task_id"], current["active_task_id"])

    def test_valid_historical_response_passes_after_task_transition(self):
        result = score_response(valid_response())
        self.assertEqual(result["status"], "PASS", result)

    def test_wrong_nonce_fails(self):
        value = valid_response()
        value["challenge_nonce"] = "stale-or-seeded-nonce"
        result = score_response(value)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("challenge_nonce mismatch", result["errors"])

    def test_wrong_historical_status_fails(self):
        value = valid_response()
        value["active_task"]["status"] = "DONE"
        result = score_response(value)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("active_task mismatch" in x for x in result["errors"]))

    def test_unproven_capability_claim_fails(self):
        value = valid_response()
        value["claims"]["core_v1_complete"] = True
        result = score_response(value)
        self.assertEqual(result["status"], "FAIL")

    def test_gold_read_attestation_fails(self):
        value = valid_response()
        value["attestations"]["read_gold"] = True
        result = score_response(value)
        self.assertEqual(result["status"], "FAIL")

    def test_missing_evidence_ref_fails(self):
        value = valid_response()
        value["evidence_refs"].remove("state/tasks.yaml")
        result = score_response(value)
        self.assertEqual(result["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
