"""Reusable *unmerged* learning notes; never an acceptance or truth oracle.

Call this after authoritative recovery to assemble a candidate anti-repetition
brief. Source pins protect recorded PR snapshots *if the caller actually
verifies live GitHub HEAD and blob*. We do not network-fetch or grant rights.
"""
from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

from .learning_novelty import make_brief, assess_learning_novelty

SCHEMA = "minhtri-working-prior-study/v1"
STUDY_FIELDS = frozenset({
    "schema", "track_id", "checkpoint_id", "working_cursor_id",
    "working_question", "claims", "open_audits",
})
CLAIM_FIELDS = frozenset({
    "claim_key", "finding", "evidence_class", "review_status",
    "source_pr", "source_head_sha", "source_comment_id",
    "source_path", "source_blob_sha", "primary_locators", "uncertainty",
})
CLASSES = frozenset({
    "TEXT_ATTESTED", "CROSS_TEXT_SYNTHESIS", "LATER/PARACANONICAL",
    "LATER_EXPLANATORY_EARLY_COMPATIBLE", "UNCERTAINTY",
})
REVIEW_STATUSES = frozenset({
    "WORKING_NOTE_NOT_ACCEPTED", "SOURCE_AUDITED_CANDIDATE",
    "DRAFT_NOT_ACCEPTED",
})
_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_ID = re.compile(r"^[a-z][a-z0-9._:-]{2,119}$")
_PATH = re.compile(r"^(docs/learning|knowledge/buddhist/atoms)/[A-Za-z0-9_./-]{1,190}$")


class PriorStudyError(ValueError):
    """Fail closed when candidate prior study is inconsistent or insufficient."""


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise PriorStudyError(message)


def _text(x: Any) -> bool:
    return isinstance(x, str) and bool(x.strip()) and len(x) <= 2000


def _ids(x: Any) -> bool:
    return (isinstance(x, list) and len(x) == len(set(x)) and
            all(isinstance(v, str) and _ID.fullmatch(v) is not None for v in x))


def _path(x: Any) -> bool:
    return (isinstance(x, str) and _PATH.fullmatch(x) is not None and
            all(segment not in ("", ".", "..") for segment in x.split("/")))


def _pins(track: Mapping[str, Any]) -> dict[int, str]:
    """Do not let an arbitrary Draft PR enter the study inventory."""
    src = track["working_cursor_source"]
    known: dict[int, str] = {src["pr_number"]: src["source_head_sha"]}
    for item in track["research_intake"]:
        if item["source_type"] != "PR" or item["checkpoint_id"] != track["checkpoint_id"]:
            continue
        _need(item["may_advance_cursor"] is False and
              item["may_promote_checkpoint"] is False,
              "research intake tries to grant progress authority")
        number = item["number"]
        sha = item["source_head_sha"]
        _need(number not in known or known[number] == sha,
              "conflicting research PR revision pins")
        known[number] = sha
    return known


def validate_working_prior_study(
    study: Mapping[str, Any], track: Mapping[str, Any], position: Any,
    *, live_pr_heads: Mapping[int, str],
) -> None:
    """Require same cursor and checked source versions for a provisional brief."""
    _need(isinstance(study, Mapping) and set(study) == STUDY_FIELDS,
          "prior study missing or shadow fields")
    _need(study["schema"] == SCHEMA, "unknown prior-study schema")
    _need(study["track_id"] == track["track_id"] == position.track_id and
          study["checkpoint_id"] == track["checkpoint_id"] == position.checkpoint_id,
          "prior study not in recovered track/checkpoint")
    _need(study["working_cursor_id"] == position.cursor_id and
          study["working_question"] == position.next_question,
          "prior study stale: cursor/question differs")
    _need(isinstance(study["open_audits"], list) and bool(study["open_audits"]) and
          len(study["open_audits"]) == len(set(study["open_audits"])) and
          all(_text(x) for x in study["open_audits"]),
          "prior work drops unresolved audits")
    _need(isinstance(study["claims"], list) and bool(study["claims"]),
          "research exists but prior claim inventory is empty")
    pins = _pins(track)
    _need(isinstance(live_pr_heads, Mapping), "live PR heads required")
    # Assert HEADs are supplied from live GitHub by the client. The values are
    # not authenticated by this pure function and are never Owner approval.
    _need(all(type(k) is int and k in pins for k in live_pr_heads),
          "unknown PR source in supplied live HEADs")
    _need(all(pr in live_pr_heads and live_pr_heads[pr] == expected
              for pr, expected in pins.items()),
          "prior study source PR changed or unverified")
    seen: set[str] = set()
    for c in study["claims"]:
        _need(isinstance(c, Mapping) and set(c) == CLAIM_FIELDS,
              "prior claim missing or shadow fields")
        key = c["claim_key"]
        _need(isinstance(key, str) and _ID.fullmatch(key) is not None and key not in seen,
              "duplicate or malformed prior claim ID")
        seen.add(key)
        _need(_text(c["finding"]) and _text(c["uncertainty"]),
              "unbounded prior claim or missing uncertainty")
        _need(c["evidence_class"] in CLASSES and
              c["review_status"] in REVIEW_STATUSES,
              "prior study falsely claims verified authority")
        pr, sha = c["source_pr"], c["source_head_sha"]
        _need(type(pr) is int and pr in pins and sha == pins[pr] and
              isinstance(sha, str) and _SHA40.fullmatch(sha) is not None,
              "prior study claim from unpinned or mismatched PR")
        comment = c["source_comment_id"]
        path, blob = c["source_path"], c["source_blob_sha"]
        if pr == track["working_cursor_source"]["pr_number"]:
            _need(type(comment) is int and comment > 0 and
                  f"comment#{comment}" in position.proof,
                  "working cursor claim must cite exact recovered comment")
            _need(path is None and blob is None and
                  c["review_status"] == "WORKING_NOTE_NOT_ACCEPTED",
                  "working cursor comment cannot fake accepted file evidence")
        else:
            _need(comment is None and _path(path) and
                  isinstance(blob, str) and _SHA40.fullmatch(blob) is not None,
                  "Draft study must pin exact GitHub file and blob")
        _need(_ids(c["primary_locators"]), "invalid/duplicate source locators")


def make_carry_forward_plan(
    study: Mapping[str, Any], track: Mapping[str, Any], position: Any,
    *, live_pr_heads: Mapping[int, str],
) -> dict[str, Any]:
    """Explain prior work to next chat BEFORE studying; does not certify truth."""
    validate_working_prior_study(study, track, position,
                                 live_pr_heads=live_pr_heads)
    records = study["claims"]
    brief = make_brief(
        position, inventory_source_ref="candidate:state/learning_prior_studies.json",
        known_claim_keys=[c["claim_key"] for c in records],
        known_primary_locators=sorted({
            locator for c in records for locator in c["primary_locators"]
        }),
        cursor_source_sha=track["working_cursor_source"]["source_head_sha"],
    )
    return {
        "status": "WORKING_STUDY_KNOWN_NOT_ACCEPTED",
        "track_id": position.track_id,
        "checkpoint_id": position.checkpoint_id,
        "cursor_id": position.cursor_id,
        "prior_results": [
            {
                "claim_key": c["claim_key"],
                "finding": c["finding"],
                "evidence_class": c["evidence_class"],
                "review_status": c["review_status"],
                "source_pr": c["source_pr"],
                "source_head_sha": c["source_head_sha"],
                "source_comment_id": c["source_comment_id"],
                "source_path": c["source_path"],
                "source_blob_sha": c["source_blob_sha"],
                "uncertainty": c["uncertainty"],
            }
            for c in records
        ],
        "exact_next_question": position.next_question,
        "open_audits": list(study["open_audits"]),
        "novelty_brief": brief,
        "reuse_policy": (
            "Treat unmerged findings as researched, unverified prior work. "
            "Re-read old texts for audit or correction; never describe the "
            "same inference or a new illustration as new discovery."
        ),
        "cursor_advanced": False,
        "checkpoint_completed": False,
        "owner_accepted": False,
        "semantic_novelty_verified": False,
    }


def triage_against_prior(
    study: Mapping[str, Any], track: Mapping[str, Any], position: Any,
    attempt: Mapping[str, Any], *, live_pr_heads: Mapping[int, str],
) -> dict[str, Any]:
    """Route a study attempt through the *same* pinned prior-study inventory."""
    plan = make_carry_forward_plan(study, track, position,
                                   live_pr_heads=live_pr_heads)
    result = assess_learning_novelty(plan["novelty_brief"], attempt)
    return {
        "learning_plan_status": plan["status"],
        "novelty": result,
        "cursor_may_advance": False,  # separate semantic review + governed commit
        "owner_acceptance_created": False,
    }
