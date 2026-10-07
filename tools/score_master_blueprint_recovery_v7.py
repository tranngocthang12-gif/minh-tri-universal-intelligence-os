#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CHALLENGE = ROOT / "eval/recovery/v7/challenge.json"
SNAPSHOT = ROOT / "eval/recovery/v7/historical_snapshot.json"

def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def ref_path(value: Any) -> str:
    return value.split("#", 1)[0] if isinstance(value, str) else ""

def score_response(response: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    challenge = load_json(CHALLENGE)
    snapshot = load_json(SNAPSHOT)
    required_top = {"schema","challenge_id","challenge_nonce","attestations","recovered_facts","evidence_refs"}
    if not isinstance(response, dict):
        return {"status":"FAIL","errors":["response must be a JSON object"]}
    if set(response) != required_top:
        missing = sorted(required_top - set(response))
        extra = sorted(set(response) - required_top)
        if missing:
            errors.append("missing top-level fields: " + ", ".join(missing))
        if extra:
            errors.append("unexpected top-level fields: " + ", ".join(extra))
    if response.get("schema") != "minhtri-master-blueprint-recovery-response/v7":
        errors.append("schema mismatch")
    if response.get("challenge_id") != challenge["challenge_id"]:
        errors.append("challenge_id mismatch")
    if response.get("challenge_nonce") != challenge["challenge_nonce"]:
        errors.append("challenge_nonce mismatch")
    expected_attestations = {"separate_zero_chat": True, "used_prior_chat_history": False, "read_snapshot": False}
    if response.get("attestations") != expected_attestations:
        errors.append("attestations mismatch")
    if response.get("recovered_facts") != snapshot["expected_facts"]:
        errors.append("recovered_facts mismatch")
    evidence = response.get("evidence_refs")
    if not isinstance(evidence, list) or not all(isinstance(x, str) and x for x in evidence):
        errors.append("evidence_refs must be a non-empty string list")
    else:
        if len(evidence) != len(set(evidence)):
            errors.append("evidence_refs must be unique")
        required = {ref_path(x) for x in snapshot["required_evidence_refs"]}
        got = {ref_path(x) for x in evidence}
        missing = sorted(required - got)
        if missing:
            errors.append("missing required evidence refs: " + ", ".join(missing))
    return {
        "schema":"minhtri-master-blueprint-recovery-score/v7",
        "status":"PASS" if not errors else "FAIL",
        "challenge_id":challenge["challenge_id"],
        "active_task_id":snapshot["expected_facts"]["active_task"]["task_id"],
        "errors":errors,
        "historical_snapshot_scoring":True,
        "public_exact_nested_contract":True,
        "hidden_expected_values":True
    }

def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: score_master_blueprint_recovery_v7.py RESPONSE.json", file=sys.stderr)
        return 2
    try:
        result = score_response(load_json(Path(argv[1])))
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        result = {"status":"FAIL","errors":[f"grader error: {exc}"]}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result.get("status") == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
