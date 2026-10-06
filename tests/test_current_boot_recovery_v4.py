import copy
import json
import unittest
from pathlib import Path

from tools.score_current_boot_recovery_v4 import score_response

ROOT = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def valid_response():
    challenge = load("eval/recovery/v4/challenge.json")
    snapshot = load("eval/recovery/v4/historical_snapshot.json")
    return {
        "schema": "minhtri-current-boot-recovery-response/v4",
        "challenge_id": challenge["challenge_id"],
        "challenge_nonce": challenge["challenge_nonce"],
        "attestations": {
            "separate_zero_chat": True,
            "used_prior_chat_history": False,
            "read_snapshot": False,
        },
        "recovered_facts": copy.deepcopy(snapshot["expected_facts"]),
        "evidence_refs": list(snapshot["required_evidence_refs"]),
        "answers": {
            "Q1": "Recovered the single boot root and durable authority.",
            "Q2": "Recovered the single authoritative law precedence and catalog boundary.",
            "Q3": "Recovered the exact active task, status, handoff, blocker, and next action.",
            "Q4": "Chat, unmerged candidates, and PC sidecars are non-canonical.",
            "Q5": "Historical C3 does not prove the current repaired boot path.",
            "Q6": "Run current-path fresh-seat proof, then identical Claude/Grok v2 red-team.",
        },
    }


class CurrentBootRecoveryV4Tests(unittest.TestCase):
    def test_valid_response_passes(self):
        result = score_response(valid_response())
        self.assertEqual(result["status"], "PASS", result)
        self.assertTrue(result["historical_snapshot_scoring"])

    def test_wrong_law_route_fails(self):
        value = valid_response()
        value["recovered_facts"]["law"]["law_precedence_ref"] = "docs/LAW_INDEX_20261003.md"
        self.assertEqual(score_response(value)["status"], "FAIL")

    def test_catalog_must_not_gain_precedence(self):
        value = valid_response()
        value["recovered_facts"]["law"]["law_index_catalog_has_independent_precedence"] = True
        self.assertEqual(score_response(value)["status"], "FAIL")

    def test_wrong_next_action_fails(self):
        value = valid_response()
        value["recovered_facts"]["active_task"]["next_action"] = "Freeze now."
        self.assertEqual(score_response(value)["status"], "FAIL")

    def test_historical_c3_cannot_be_promoted_to_current_path_proof(self):
        value = valid_response()
        value["recovered_facts"]["capability_truth"]["historical_c3_current_path_proof"] = True
        self.assertEqual(score_response(value)["status"], "FAIL")

    def test_missing_evidence_fails(self):
        value = valid_response()
        value["evidence_refs"].remove("state/tasks.yaml")
        self.assertEqual(score_response(value)["status"], "FAIL")

    def test_snapshot_is_not_live_current_alias(self):
        snapshot = load("eval/recovery/v4/historical_snapshot.json")
        self.assertEqual(
            snapshot["expected_facts"]["active_task"]["task_id"],
            "ARCH-FOUNDATION-ACCEPTANCE-FREEZE-V1",
        )


if __name__ == "__main__":
    unittest.main()
