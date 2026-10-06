import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools.score_zero_chat_recovery import score_response

ROOT = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def valid_response():
    challenge = load("eval/recovery/v1/challenge.json")
    current = load("state/current.yaml")
    registry = load("state/tasks.yaml")
    task = next(t for t in registry["tasks"] if t["task_id"] == current["active_task_id"])
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
            "source_ref": "docs/GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md",
            "routed_by_ref": "docs/LAW_INDEX_20261003.md",
        },
        "active_task": {
            "task_id": current["active_task_id"],
            "status": task["status"],
            "handoff_ref": task["handoff_ref"],
            "blocker": task["blocker"],
        },
        "claims": {
            "core_v1_complete": False,
            "autonomous_learning_proven": False,
            "chat_memory_canonical": False,
        },
        "evidence_refs": [
            "docs/GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md",
            "docs/LAW_INDEX_20261003.md",
            "state/current.yaml",
            "state/tasks.yaml",
            "docs/vnext/continuity/RECOVERY_ENTRYPOINT_V1.md",
            "docs/vnext/handoff/ARCHITECTURE_HANDOFF_20261006.md",
        ],
        "answers": {
            "Q1": "The project-wide continuity and handoff law is in GITHUB_FIRST_ROLE_BOOTSTRAP section 8 and is routed by LAW_INDEX.",
            "Q2": f"{current['active_task_id']} is {task['status']}.",
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

    def test_gold_matches_canonical_active_state(self):
        gold = load("eval/recovery/v1/gold.json")
        current = load("state/current.yaml")
        registry = load("state/tasks.yaml")
        task = next(t for t in registry["tasks"] if t["task_id"] == current["active_task_id"])
        facts = gold["required_facts"]
        self.assertEqual(facts["active_task_id"], current["active_task_id"])
        self.assertEqual(facts["active_status"], task["status"])
        self.assertEqual(facts["handoff_ref"], task["handoff_ref"])
        self.assertEqual(facts["blocker"], task["blocker"])

    def test_valid_structured_response_passes_deterministically(self):
        result = score_response(valid_response())
        self.assertEqual(result["status"], "PASS", result)

    def test_wrong_nonce_fails(self):
        value = valid_response()
        value["challenge_nonce"] = "stale-or-seeded-nonce"
        result = score_response(value)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("challenge_nonce mismatch", result["errors"])

    def test_wrong_active_status_fails(self):
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
        self.assertIn("unproven capability claim or malformed claims object", result["errors"])

    def test_gold_read_attestation_fails(self):
        value = valid_response()
        value["attestations"]["read_gold"] = True
        result = score_response(value)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("read_gold must be false", result["errors"])

    def test_missing_evidence_ref_fails(self):
        value = valid_response()
        value["evidence_refs"].remove("state/tasks.yaml")
        result = score_response(value)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("missing required evidence refs" in x for x in result["errors"]))


if __name__ == "__main__":
    unittest.main()
