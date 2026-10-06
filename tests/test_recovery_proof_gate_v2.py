import json
import unittest
from pathlib import Path

from tools.score_zero_chat_recovery import score_response

ROOT = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def v2_response():
    challenge = load("eval/recovery/v2/challenge.json")
    facts = load("eval/recovery/v1/gold.json")["required_facts"]
    return {
        "schema": "minhtri-zero-chat-recovery-response/v2",
        "challenge_id": challenge["challenge_id"],
        "challenge_nonce": challenge["challenge_nonce"],
        "attestations": {
            "separate_zero_chat": True,
            "used_prior_chat_history": False,
            "read_gold": False,
        },
        "foundation_law": {
            "source_ref": "docs/GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md#8-project-wide-continuity--mandatory-handoff-law",
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
        "evidence_refs": [
            "docs/GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md#8-project-wide-continuity--mandatory-handoff-law",
            "docs/LAW_INDEX_20261003.md",
            "state/current.yaml",
            "state/tasks.yaml",
            "docs/vnext/continuity/RECOVERY_ENTRYPOINT_V1.md",
            "docs/vnext/handoff/ARCHITECTURE_HANDOFF_20261006.md",
        ],
        "answers": {
            "Q1": "The project-wide continuity and handoff law is in GITHUB_FIRST_ROLE_BOOTSTRAP and is routed by LAW_INDEX.",
            "Q2": "ARCH-VNEXT-CONTINUITY-HANDOFF-CORE-V1 is BLOCKED.",
            "Q3": "Canonical main is authoritative; unmerged work is candidate state.",
            "Q4": "DONE: static continuity machinery. NOT DONE: genuine fresh-seat behavioral proof.",
            "Q5": "Run a genuine zero-chat fresh seat and grade the fresh response before continuing.",
            "Q6": "Core v1 and autonomous learning are not proven.",
        },
    }


class RecoveryProofGateV2Tests(unittest.TestCase):
    def test_v2_accepts_section_anchor_on_same_historical_file(self):
        result = score_response(v2_response())
        self.assertEqual(result["status"], "PASS", result)
        self.assertEqual(result["reference_normalization"], "path_with_optional_fragment")

    def test_v2_rejects_different_source_file_even_with_anchor(self):
        value = v2_response()
        value["foundation_law"]["source_ref"] = "docs/OTHER.md#8-project-wide-continuity"
        result = score_response(value)
        self.assertEqual(result["status"], "FAIL")

    def test_v2_rejects_stale_nonce(self):
        value = v2_response()
        value["challenge_nonce"] = "mtc1-8ad4b9d1f0f7419db9c6d5021bb640ce"
        result = score_response(value)
        self.assertEqual(result["status"], "FAIL")

    def test_c1_behavior_is_not_retroactively_regraded(self):
        value = v2_response()
        c1 = load("eval/recovery/v1/challenge.json")
        value["schema"] = "minhtri-zero-chat-recovery-response/v1"
        value["challenge_id"] = c1["challenge_id"]
        value["challenge_nonce"] = c1["challenge_nonce"]
        result = score_response(value)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["reference_normalization"], "exact")

    def test_receipt_completion_rule_requires_both_parts(self):
        packet = load("eval/recovery/v2/packet.json")
        rule = packet["completion_rule"]
        self.assertTrue(rule["both_required"])
        self.assertEqual(rule["deterministic_score"], "PASS")
        self.assertEqual(rule["independence_provenance"], "PRESENT")

    def test_c1_receipt_is_preserved_as_fail(self):
        receipt = load("eval/recovery/v2/attempts/C1_receipt.json")
        self.assertEqual(receipt["deterministic_score"], "FAIL")
        self.assertFalse(receipt["completion_eligible"])
        self.assertEqual(receipt["independence_provenance"], "PRESENT")


if __name__ == "__main__":
    unittest.main()
