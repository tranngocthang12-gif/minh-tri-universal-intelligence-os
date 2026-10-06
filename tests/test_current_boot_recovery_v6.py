import copy, json, unittest
from pathlib import Path
from tools.score_current_boot_recovery_v6 import score_response

ROOT=Path(__file__).resolve().parents[1]

def load(rel):
    return json.loads((ROOT/rel).read_text(encoding="utf-8"))

def valid_response():
    ch=load("eval/recovery/v6/challenge.json")
    snap=load("eval/recovery/v6/historical_snapshot.json")
    return {
        "schema":"minhtri-current-boot-recovery-response/v6",
        "challenge_id":ch["challenge_id"],
        "challenge_nonce":ch["challenge_nonce"],
        "attestations":{"separate_zero_chat":True,"used_prior_chat_history":False,"read_snapshot":False},
        "recovered_facts":copy.deepcopy(snap["expected_facts"]),
        "evidence_refs":list(snap["required_evidence_refs"])
    }

class RecoveryV6Tests(unittest.TestCase):
    def test_valid_response_passes(self):
        self.assertEqual(score_response(valid_response())["status"],"PASS")
    def test_wrong_blueprint_status_fails(self):
        v=valid_response()
        v["recovered_facts"]["blueprint"]["status"]="CANDIDATE"
        self.assertEqual(score_response(v)["status"],"FAIL")
    def test_wrong_next_action_fails(self):
        v=valid_response()
        v["recovered_facts"]["active_task"]["next_action"]="freeze now"
        self.assertEqual(score_response(v)["status"],"FAIL")
    def test_missing_blueprint_evidence_fails(self):
        v=valid_response()
        v["evidence_refs"].remove("docs/vnext/MASTER_BLUEPRINT_V1_20261006.md")
        self.assertEqual(score_response(v)["status"],"FAIL")

if __name__=="__main__":
    unittest.main()
