#!/usr/bin/env python3
"""Deterministic grader for MINH TRI zero-chat recovery responses.

This grader checks machine-readable recovery facts against the canonical repository
state. It does not prove that a chat UI was genuinely independent; the response must
attest that separately and the resulting PASS remains behavioral evidence only when
the execution provenance is independently established.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

CHALLENGE = "eval/recovery/v1/challenge.json"
GOLD = "eval/recovery/v1/gold.json"
CURRENT = "state/current.yaml"
TASKS = "state/tasks.yaml"

REQUIRED_TOP_LEVEL = {
    "schema",
    "challenge_id",
    "challenge_nonce",
    "attestations",
    "foundation_law",
    "active_task",
    "claims",
    "evidence_refs",
    "answers",
}
REQUIRED_ANSWERS = {"Q1", "Q2", "Q3", "Q4", "Q5", "Q6"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def norm(text: Any) -> str:
    return " ".join(str(text).lower().split())


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def score_response(response: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    challenge = load_json(ROOT / CHALLENGE)
    gold = load_json(ROOT / GOLD)
    current = load_json(ROOT / CURRENT)
    registry = load_json(ROOT / TASKS)

    if not isinstance(response, dict):
        return {"status": "FAIL", "errors": ["response must be a JSON object"]}

    extra = sorted(set(response) - REQUIRED_TOP_LEVEL)
    missing = sorted(REQUIRED_TOP_LEVEL - set(response))
    if missing:
        fail(errors, "missing top-level fields: " + ", ".join(missing))
    if extra:
        fail(errors, "unexpected top-level fields: " + ", ".join(extra))

    if response.get("schema") != "minhtri-zero-chat-recovery-response/v1":
        fail(errors, "unsupported response schema")
    if response.get("challenge_id") != challenge.get("challenge_id"):
        fail(errors, "challenge_id mismatch")
    if response.get("challenge_nonce") != challenge.get("challenge_nonce"):
        fail(errors, "challenge_nonce mismatch")

    attest = response.get("attestations")
    if not isinstance(attest, dict):
        fail(errors, "attestations must be an object")
    else:
        if attest.get("separate_zero_chat") is not True:
            fail(errors, "separate_zero_chat must be true")
        if attest.get("used_prior_chat_history") is not False:
            fail(errors, "used_prior_chat_history must be false")
        if attest.get("read_gold") is not False:
            fail(errors, "read_gold must be false")
        if set(attest) != {"separate_zero_chat", "used_prior_chat_history", "read_gold"}:
            fail(errors, "attestations fields are not exact")

    active_id = current.get("active_task_id")
    tasks = {t.get("task_id"): t for t in registry.get("tasks", []) if isinstance(t, dict)}
    canonical_task = tasks.get(active_id)
    if canonical_task is None:
        fail(errors, "canonical active task is missing from registry")
        canonical_task = {}

    foundation = response.get("foundation_law")
    expected_law = gold["required_facts"]["law_source_ref"]
    expected_route = gold["required_facts"]["law_routed_by_ref"]
    if not isinstance(foundation, dict):
        fail(errors, "foundation_law must be an object")
    else:
        if foundation.get("source_ref") != expected_law:
            fail(errors, "foundation law source_ref mismatch")
        if foundation.get("routed_by_ref") != expected_route:
            fail(errors, "foundation law routed_by_ref mismatch")
        if set(foundation) != {"source_ref", "routed_by_ref"}:
            fail(errors, "foundation_law fields are not exact")

    active = response.get("active_task")
    expected_active = {
        "task_id": active_id,
        "status": canonical_task.get("status"),
        "handoff_ref": canonical_task.get("handoff_ref"),
        "blocker": canonical_task.get("blocker"),
    }
    if not isinstance(active, dict):
        fail(errors, "active_task must be an object")
    else:
        if active != expected_active:
            fail(errors, f"active_task mismatch: expected {expected_active!r}")

    claims = response.get("claims")
    expected_claims = {
        "core_v1_complete": False,
        "autonomous_learning_proven": False,
        "chat_memory_canonical": False,
    }
    if claims != expected_claims:
        fail(errors, "unproven capability claim or malformed claims object")

    evidence = response.get("evidence_refs")
    required_refs = set(gold["required_facts"]["required_evidence_refs"])
    if not isinstance(evidence, list) or not all(isinstance(x, str) and x for x in evidence):
        fail(errors, "evidence_refs must be a non-empty string list")
    else:
        if len(evidence) != len(set(evidence)):
            fail(errors, "evidence_refs must be unique")
        missing_refs = sorted(required_refs - set(evidence))
        if missing_refs:
            fail(errors, "missing required evidence refs: " + ", ".join(missing_refs))

    answers = response.get("answers")
    if not isinstance(answers, dict):
        fail(errors, "answers must be an object")
    else:
        if set(answers) != REQUIRED_ANSWERS:
            fail(errors, "answers must contain exactly Q1-Q6")
        for qid in sorted(REQUIRED_ANSWERS):
            value = answers.get(qid)
            if not isinstance(value, str) or not value.strip():
                fail(errors, f"{qid} must be a non-empty string")
        for qid, needles in gold["required_facts"]["answer_required_tokens"].items():
            text = norm(answers.get(qid, ""))
            for needle in needles:
                if norm(needle) not in text:
                    fail(errors, f"{qid} missing required token: {needle}")

    return {
        "status": "PASS" if not errors else "FAIL",
        "challenge_id": challenge.get("challenge_id"),
        "active_task_id": active_id,
        "errors": errors,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: score_zero_chat_recovery.py RESPONSE.json", file=sys.stderr)
        return 2
    try:
        response = load_json(Path(argv[1]))
        result = score_response(response)
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        result = {"status": "FAIL", "errors": [f"grader error: {exc}"]}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
