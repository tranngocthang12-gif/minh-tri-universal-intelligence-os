"""Learning novelty triage for a recovered, previously studied question.

A strict, read-only candidate guard. It checks claim/source IDs against a
PINNED study inventory; it cannot determine semantic equivalence or whether a
source is true. No case here authorizes checkpoint completion or Owner approval.
"""
from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping
from typing import Any

BRIEF_SCHEMA = "minhtri-learning-resume-brief/v1"
ATTEMPT_SCHEMA = "minhtri-learning-novelty-attempt/v1"
BRIEF_FIELDS = frozenset({
    "schema", "track_id", "checkpoint_id", "cursor_id",
    "exact_next_question", "cursor_source_ref", "cursor_source_sha",
    "inventory_source_ref", "known_claim_keys", "known_primary_locators",
})
ATTEMPT_FIELDS = frozenset({
    "schema", "track_id", "checkpoint_id", "cursor_id",
    "question_sha256", "mode", "claim_keys_reused", "claim_keys_added",
    "claim_keys_corrected", "new_primary_locators", "evidence_refs",
    "application_case_refs", "answer_to_question", "counter_reading",
})
MODES = frozenset({
    "RESTATEMENT", "APPLICATION_EXAMPLE", "NEW_SOURCE_FINDING", "CORRECTION",
})
_ID = re.compile(r"^[a-z][a-z0-9._:-]{2,119}$")
_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class LearningNoveltyError(ValueError):
    """Invalid or contradictory novelty evidence (not semantic disproof)."""


def _need(condition: bool, message: str) -> None:
    if not condition:
        raise LearningNoveltyError(message)


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and len(value) <= 4000


def _items(value: Any, *, identifiers: bool = False) -> bool:
    return (isinstance(value, list) and all(
        _text(x) and (not identifiers or _ID.fullmatch(x) is not None)
        for x in value) and len(value) == len(set(value)))


def _digest(question: str) -> str:
    return hashlib.sha256(question.encode("utf-8")).hexdigest()


def validate_brief(brief: Mapping[str, Any]) -> None:
    _need(isinstance(brief, Mapping) and set(brief) == BRIEF_FIELDS,
          "resume brief missing or shadow fields")
    _need(brief["schema"] == BRIEF_SCHEMA, "unknown resume brief schema")
    for key in ("track_id", "checkpoint_id", "cursor_id",
                "cursor_source_ref", "inventory_source_ref"):
        _need(_text(brief[key]), f"missing {key}")
    _need(_text(brief["exact_next_question"])
          and len(brief["exact_next_question"]) >= 40, "missing actionable next question")
    _need(isinstance(brief["cursor_source_sha"], str)
          and _SHA40.fullmatch(brief["cursor_source_sha"]) is not None,
          "cursor source must pin a revision")
    for key in ("known_claim_keys", "known_primary_locators"):
        _need(_items(brief[key], identifiers=True), f"invalid prior study inventory {key}")


def validate_attempt(attempt: Mapping[str, Any]) -> None:
    _need(isinstance(attempt, Mapping) and set(attempt) == ATTEMPT_FIELDS,
          "novelty attempt missing or shadow fields")
    _need(attempt["schema"] == ATTEMPT_SCHEMA, "unknown novelty attempt schema")
    for key in ("track_id", "checkpoint_id", "cursor_id"):
        _need(_text(attempt[key]), f"missing {key}")
    _need(isinstance(attempt["question_sha256"], str)
          and _SHA256.fullmatch(attempt["question_sha256"]) is not None,
          "invalid question SHA256")
    _need(attempt["mode"] in MODES, "unsupported novelty mode")
    for key in ("claim_keys_reused", "claim_keys_added", "claim_keys_corrected",
                "new_primary_locators", "evidence_refs", "application_case_refs"):
        _need(_items(attempt[key], identifiers=key not in
                     ("evidence_refs", "application_case_refs")),
              f"invalid duplicate or malformed {key}")
    for key in ("answer_to_question", "counter_reading"):
        _need(attempt[key] is None or _text(attempt[key]),
              f"invalid {key}")


def make_brief(position: Any, *, inventory_source_ref: str,
               known_claim_keys: list[str], known_primary_locators: list[str],
               cursor_source_sha: str) -> dict[str, Any]:
    """Build a candidate brief from a separately recovered LearningPosition.

    The caller must independently fresh-read canonical and task/domain sources.
    """
    brief = {
        "schema": BRIEF_SCHEMA,
        "track_id": position.track_id,
        "checkpoint_id": position.checkpoint_id,
        "cursor_id": position.cursor_id,
        "exact_next_question": position.next_question,
        "cursor_source_ref": position.proof,
        "cursor_source_sha": cursor_source_sha,
        "inventory_source_ref": inventory_source_ref,
        "known_claim_keys": list(known_claim_keys),
        "known_primary_locators": list(known_primary_locators),
    }
    validate_brief(brief)
    return brief


def assess_learning_novelty(brief: Mapping[str, Any],
                            attempt: Mapping[str, Any]) -> dict[str, Any]:
    """Return a cautious status; never semantically certify 'new'."""
    validate_brief(brief)
    validate_attempt(attempt)
    for key in ("track_id", "checkpoint_id", "cursor_id"):
        _need(brief[key] == attempt[key], f"wrong recovered {key}")
    _need(attempt["question_sha256"] == _digest(brief["exact_next_question"]),
          "wrong active question: cannot count another lesson as progress")

    known = set(brief["known_claim_keys"])
    known_loci = set(brief["known_primary_locators"])
    reused = set(attempt["claim_keys_reused"])
    added = set(attempt["claim_keys_added"])
    corrected = set(attempt["claim_keys_corrected"])
    new_loci = set(attempt["new_primary_locators"])
    _need(reused <= known, "reused claim IDs not in reviewed study inventory")
    _need(not corrected - known, "correction does not identify a previously studied claim")
    _need(not added & known, "previously studied claim relabeled as new")
    _need(not added & corrected, "new and corrected claim IDs cannot overlap")
    _need(not new_loci & known_loci, "previously studied passage relabeled as new")

    mode = attempt["mode"]
    answer = attempt["answer_to_question"]
    counter = attempt["counter_reading"]
    source_refs = attempt["evidence_refs"]
    examples = attempt["application_case_refs"]
    _need(mode != "RESTATEMENT" or
          not (added or corrected or new_loci or examples),
          "restatement cannot claim novelty")
    _need(mode != "APPLICATION_EXAMPLE" or
          (bool(examples) and not added and not corrected and not new_loci),
          "application example cannot silently claim research novelty")
    _need(mode not in ("NEW_SOURCE_FINDING", "CORRECTION") or
          not examples, "do not confuse a new example with source-level progress")

    status = "REPETITION_NO_ADVANCEMENT"
    if mode == "APPLICATION_EXAMPLE":
        status = "APPLICATION_ONLY_NO_ADVANCEMENT"
    elif mode == "NEW_SOURCE_FINDING":
        if added and new_loci and source_refs and _text(answer) and len(answer) >= 60 and _text(counter):
            status = "NEW_EVIDENCE_CANDIDATE_NEEDS_SEMANTIC_REVIEW"
        else:
            status = "INSUFFICIENT_NOVELTY_NO_ADVANCEMENT"
    elif mode == "CORRECTION":
        if corrected and new_loci and source_refs and _text(answer) and len(answer) >= 60 and _text(counter):
            status = "CORRECTION_CANDIDATE_NEEDS_SEMANTIC_REVIEW"
        else:
            status = "INSUFFICIENT_NOVELTY_NO_ADVANCEMENT"

    eligible = status in {
        "NEW_EVIDENCE_CANDIDATE_NEEDS_SEMANTIC_REVIEW",
        "CORRECTION_CANDIDATE_NEEDS_SEMANTIC_REVIEW",
    }
    return {
        "status": status,
        "question_sha256": _digest(brief["exact_next_question"]),
        "origin_cursor_id": brief["cursor_id"],
        "candidate_delta_eligible": eligible,
        "checkpoint_completed": False,
        "owner_accepted": False,
        "semantic_novelty_verified": False,
        "independent_review_required": eligible,
        "next_question_if_no_progress": None if eligible else brief["exact_next_question"],
    }
