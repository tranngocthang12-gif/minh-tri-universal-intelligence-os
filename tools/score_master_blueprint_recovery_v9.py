#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "eval/recovery/v9/historical_snapshot.json"


def score_response(response):
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    errors = []
    expected_top = {"schema", "challenge_id", "challenge_nonce", "attestations", "recovered_facts", "evidence_refs"}
    if set(response) != expected_top:
        errors.append("top-level fields mismatch")
    if response.get("schema") != "minhtri-master-blueprint-recovery-response/v9":
        errors.append("schema mismatch")
    if response.get("challenge_id") != snapshot["challenge_id"]:
        errors.append("challenge_id mismatch")
    if response.get("challenge_nonce") != snapshot["challenge_nonce"]:
        errors.append("challenge_nonce mismatch")
    if response.get("attestations") != {
        "separate_zero_chat": True,
        "used_prior_chat_history": False,
        "read_snapshot": False,
    }:
        errors.append("attestations mismatch")
    if response.get("recovered_facts") != snapshot["expected_facts"]:
        errors.append("recovered_facts mismatch")
    evidence = response.get("evidence_refs")
    if not isinstance(evidence, list) or not evidence or not all(isinstance(x, str) and x for x in evidence):
        errors.append("evidence_refs must be a non-empty string list")
    elif len(evidence) != len(set(evidence)):
        errors.append("evidence_refs must be unique")
    else:
        missing = sorted(set(snapshot["required_evidence_refs"]) - set(evidence))
        if missing:
            errors.append("missing required evidence refs: " + ", ".join(missing))
    return {
        "schema": "minhtri-master-blueprint-recovery-score/v9",
        "status": "PASS" if not errors else "FAIL",
        "challenge_id": snapshot["challenge_id"],
        "active_task_id": snapshot["expected_facts"]["active_task"]["task_id"],
        "errors": errors,
        "historical_snapshot_scoring": True,
        "public_exact_nested_contract": True,
        "public_exact_evidence_membership": True,
        "hidden_active_task_bound_to_canonical_registry": True,
        "hidden_expected_values": True,
    }


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: score_master_blueprint_recovery_v9.py RESPONSE.json")
    response = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    result = score_response(response)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
