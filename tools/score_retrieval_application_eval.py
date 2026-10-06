from __future__ import annotations

import json
from pathlib import Path


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def score(gold: dict, response: dict) -> dict:
    errors = []
    if response.get("schema") != "minhtri-retrieval-application-response/v1":
        errors.append("schema mismatch")
    if response.get("set_id") != gold.get("set_id"):
        errors.append("set_id mismatch")
    attest = response.get("attestations")
    if attest != {"fresh_seat": True, "used_prior_chat_history": False, "read_gold": False}:
        errors.append("attestations mismatch")

    answers = response.get("answers")
    if not isinstance(answers, list):
        answers = []
        errors.append("answers must be a list")

    by_qid = {}
    for item in answers:
        if not isinstance(item, dict):
            errors.append("answer item must be an object")
            continue
        qid = item.get("qid")
        if qid in by_qid:
            errors.append(f"duplicate answer: {qid}")
        by_qid[qid] = item

    results = []
    passed = 0
    for expected in gold["answers"]:
        qid = expected["qid"]
        actual = by_qid.get(qid)
        reasons = []
        if actual is None:
            reasons.append("missing answer")
        else:
            if actual.get("decision") != expected["decision"]:
                reasons.append("wrong decision")
            used = set(actual.get("record_ids", []))
            required = set(expected["required_record_ids"])
            forbidden = set(expected["forbidden_record_ids"])
            if not required.issubset(used):
                reasons.append("missing required record")
            if used & forbidden:
                reasons.append("used forbidden record")
            if not isinstance(actual.get("answer"), str) or not actual.get("answer", "").strip():
                reasons.append("answer text missing")
        ok = not reasons
        if ok:
            passed += 1
        results.append({"qid": qid, "pass": ok, "reasons": reasons})

    total = len(gold["answers"])
    return {
        "schema": "minhtri-retrieval-application-score/v1",
        "status": "PASS" if not errors and passed == total else "FAIL",
        "passed": passed,
        "total": total,
        "errors": errors,
        "results": results,
    }
