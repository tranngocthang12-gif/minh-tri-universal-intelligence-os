import json
import unittest
from pathlib import Path

from tools.score_zero_chat_recovery import score_response

ROOT = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def v3_response():
    challenge = load("eval/recovery/v3/challenge.json")
    current = load("state/current.yaml")
    registry = load("state/tasks.yaml")
    task = next(t for t in registry["tasks"] if t["task_id"] == current["active_task_id"])
    return {
        "schema": "minhtri-zero-chat-recovery-response/v3",
        "challenge_id": challenge["challenge_id"],
        "challenge_nonce": challenge["challenge_nonce"],
        "attestations": {
            "separate_zero_chat": True,
            "used_prior_chat_history": False,
            "read_gold": False,
        },
        "recovered_facts": {
            "foundation_law": {
                "source_ref": "docs/GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md#8-project-wide-continuity--mandatory-handoff-law",
                "routed_by_ref": "docs/LAW_INDEX_20261003.md",
            },
            "active_task": {
                "task_id": current["active_task_id"],
                "status": task["status"],
                "handoff_ref": task["handoff_ref"],
                "blocker": task["blocker"],
            },
            "canonicality": {
                "durable_continuity_authority": current["durable_continuity_authority"],
                "unmerged_candidate_authoritative": False,
                "chat_memory_canonical": False,
            },
            "capability_truth": {
                "core_v1_complete": False,
                "fresh_seat_behavioral_recovery_proven": False,
                "autonomous_learning_proven": False,
                "automatic_self_critique_proven": False,
                "meta_learning_proven": False,
            },
            "next_gate": {
                "challenge_ref": "eval/recovery/v3/challenge.json",
                "response_schema_ref": "eval/recovery/v3/response.schema.json",
                "scorer_ref": "tools/score_zero_chat_recovery.py",
                "receipt_schema_ref": "eval/recovery/v2/evidence_receipt.schema.json",
                "deterministic_pass_required": True,
                "independence_provenance_required": True,
                "durable_receipt_required": True,
            },
        },
        "evidence_refs": [
            "docs/GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md#8-project-wide-continuity--mandatory-handoff-law",
            "docs/LAW_INDEX_20261003.md",
            "state/current.yaml",
            "state/tasks.yaml",
            "docs/vnext/continuity/RECOVERY_ENTRYPOINT_V1.md",
            "docs/vnext/handoff/ARCHITECTURE_HANDOFF_20261006.md",
            "eval/recovery/v3/challenge.json",
            "eval/recovery/v3/packet.json",
            "eval/recovery/v3/response.schema.json",
            "tools/score_zero_chat_recovery.py",
        ],
        "answers": {
            "Q1": "Law and route recovered.",
            "Q2": "Task state recovered.",
            "Q3": "Canonical and candidate state distinguished.",
            "Q4": "Completion boundary recovered.",
            "Q5": "Use the evaluator and persist proof before continuation.",
            "Q6": "Unproven capabilities remain unproven.",
        },
    }


class RecoveryProofGateV3Tests(unittest.TestCase):
    def test_v3_valid_structured_facts_pass_without_prose_keywords(self):
        value = v3_response()
        value["answers"]["Q5"] = "Use the evaluator and persist proof before continuation."
        result = score_response(value)
        self.assertEqual(result["status"], "PASS", result)
        self.assertFalse(result["prose_keyword_scoring"])

    def test_v3_same_facts_different_prose_same_result(self):
        a = v3_response()
        b = v3_response()
        a["answers"]["Q1"] = "A"
        b["answers"]["Q1"] = "Completely different wording."
        self.assertEqual(score_response(a)["status"], "PASS")
        self.assertEqual(score_response(b)["status"], "PASS")

    def test_v3_wrong_task_status_fails(self):
        value = v3_response()
        value["recovered_facts"]["active_task"]["status"] = "DONE"
        result = score_response(value)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("active_task mismatch" in x for x in result["errors"]))

    def test_v3_wrong_source_file_fails(self):
        value = v3_response()
        value["recovered_facts"]["foundation_law"]["source_ref"] = "docs/OTHER.md#8-project-wide-continuity"
        result = score_response(value)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("foundation law source_ref mismatch", result["errors"])

    def test_v3_stale_nonce_fails(self):
        value = v3_response()
        value["challenge_nonce"] = "mtc2-6f1e2aa7985b4c4eaa52b4cd5d21d22f"
        result = score_response(value)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("challenge_nonce mismatch", result["errors"])

    def test_v3_false_completion_claim_fails(self):
        value = v3_response()
        value["recovered_facts"]["capability_truth"]["core_v1_complete"] = True
        result = score_response(value)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("capability truth mismatch", result["errors"])

    def test_v3_missing_evidence_fails(self):
        value = v3_response()
        value["evidence_refs"].remove("state/tasks.yaml")
        result = score_response(value)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("missing required evidence refs" in x for x in result["errors"]))

    def test_c2_history_remains_fail(self):
        receipt = load("eval/recovery/v2/attempts/C2_receipt.json")
        self.assertEqual(receipt["deterministic_score"], "FAIL")
        self.assertFalse(receipt["completion_eligible"])

    def test_v3_completion_rule_requires_all_three(self):
        packet = load("eval/recovery/v3/packet.json")
        rule = packet["completion_rule"]
        self.assertTrue(rule["all_required"])
        self.assertEqual(rule["deterministic_score"], "PASS")
        self.assertEqual(rule["independence_provenance"], "PRESENT")
        self.assertTrue(rule["durable_receipt_merged"])


if __name__ == "__main__":
    unittest.main()
