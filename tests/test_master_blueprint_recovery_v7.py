import copy, json, unittest
from pathlib import Path
from tools.score_master_blueprint_recovery_v7 import score_response

ROOT = Path(__file__).resolve().parents[1]

def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def valid_response():
    ch = load("eval/recovery/v7/challenge.json")
    snap = load("eval/recovery/v7/historical_snapshot.json")
    return {
        "schema":"minhtri-master-blueprint-recovery-response/v7",
        "challenge_id":ch["challenge_id"],
        "challenge_nonce":ch["challenge_nonce"],
        "attestations":{"separate_zero_chat":True,"used_prior_chat_history":False,"read_snapshot":False},
        "recovered_facts":copy.deepcopy(snap["expected_facts"]),
        "evidence_refs":list(snap["required_evidence_refs"]),
    }

def value_shape(value):
    if isinstance(value, dict):
        return {k:value_shape(v) for k,v in sorted(value.items())}
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    return type(value).__name__

def schema_shape(schema):
    if schema.get("type") == "object":
        required = schema.get("required", [])
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is not False:
            raise AssertionError("all recovered_facts objects must set additionalProperties=false")
        if set(required) != set(props):
            raise AssertionError("all public recovered_facts properties must be required")
        return {k:schema_shape(props[k]) for k in sorted(required)}
    return schema.get("type")

class RecoveryV7Tests(unittest.TestCase):
    def test_valid_response_passes(self):
        self.assertEqual(score_response(valid_response())["status"], "PASS")

    def test_public_schema_exposes_exact_nested_shape(self):
        schema = load("eval/recovery/v7/response.schema.json")
        snap = load("eval/recovery/v7/historical_snapshot.json")
        self.assertEqual(schema_shape(schema["properties"]["recovered_facts"]), value_shape(snap["expected_facts"]))

    def test_public_schema_does_not_embed_expected_values(self):
        text = (ROOT / "eval/recovery/v7/response.schema.json").read_text(encoding="utf-8")
        self.assertNotIn("POST_MERGE_ACCEPTANCE_ORDER_VIOLATION", text)
        self.assertNotIn("RECOVERY_PROOF_V7_FRESH_SEAT_RESPONSE_AND_DURABLE_RECEIPT_REQUIRED", text)

    def test_wrong_blueprint_status_fails(self):
        v = valid_response()
        v["recovered_facts"]["blueprint"]["status"] = "FOUNDATION CANDIDATE"
        self.assertEqual(score_response(v)["status"], "FAIL")

    def test_wrong_next_action_fails(self):
        v = valid_response()
        v["recovered_facts"]["active_task"]["next_action"] = "freeze now"
        self.assertEqual(score_response(v)["status"], "FAIL")

    def test_v6_failure_is_preserved(self):
        score = load("eval/recovery/v6/attempts/C6_score.json")
        self.assertEqual(score["status"], "FAIL")
        self.assertEqual(score["errors"], ["recovered_facts mismatch"])

    def test_v7_has_new_challenge_identity(self):
        old = load("eval/recovery/v6/challenge.json")
        new = load("eval/recovery/v7/challenge.json")
        self.assertNotEqual(old["challenge_id"], new["challenge_id"])
        self.assertNotEqual(old["challenge_nonce"], new["challenge_nonce"])

if __name__ == "__main__":
    unittest.main()
