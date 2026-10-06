import copy, json, unittest
from pathlib import Path
from tools.score_current_boot_recovery_v5 import score_response

ROOT=Path(__file__).resolve().parents[1]

def load(rel):
    return json.loads((ROOT/rel).read_text(encoding="utf-8"))

def valid_response():
    ch=load("eval/recovery/v5/challenge.json")
    snap=load("eval/recovery/v5/historical_snapshot.json")
    return {
        "schema":"minhtri-current-boot-recovery-response/v5",
        "challenge_id":ch["challenge_id"],
        "challenge_nonce":ch["challenge_nonce"],
        "attestations":{"separate_zero_chat":True,"used_prior_chat_history":False,"read_snapshot":False},
        "recovered_facts":copy.deepcopy(snap["expected_facts"]),
        "evidence_refs":list(snap["required_evidence_refs"]),
        "answers":{"Q1":"ok","Q2":"ok","Q3":"ok","Q4":"ok","Q5":"ok","Q6":"ok"}
    }

class RecoveryV5Tests(unittest.TestCase):
    def test_valid_response_passes(self):
        self.assertEqual(score_response(valid_response())["status"],"PASS")
    def test_extra_nested_field_fails_contract(self):
        v=valid_response()
        v["recovered_facts"]["boot"]["extra"]="x"
        self.assertEqual(score_response(v)["status"],"FAIL")
    def test_wrong_next_action_fails(self):
        v=valid_response()
        v["recovered_facts"]["active_task"]["next_action"]="freeze now"
        self.assertEqual(score_response(v)["status"],"FAIL")
    def test_v4_fail_remains_fail(self):
        r=load("eval/recovery/v4/attempts/C4_receipt.json")
        self.assertEqual(r["deterministic_score"],"FAIL")
        self.assertFalse(r["completion_eligible"])

if __name__=="__main__":
    unittest.main()
