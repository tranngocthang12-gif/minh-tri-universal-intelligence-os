"""A bounded experience/knowledge/procedure memory selector.

Records are untrusted candidate data: this module filters and explains a choice,
but never certifies source truth, runs a procedure or promotes Owner acceptance.
"""
from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any

KINDS = frozenset({"EPISODIC", "SEMANTIC", "PROCEDURAL"})
STATES = frozenset({"CANDIDATE", "SOURCE_AUDITED_CANDIDATE", "ACCEPTED", "CONTESTED", "SUPERSEDED", "RETRACTED"})
SCHEMA = "minhtri-learning-reusable-memory/v1"
SHA = re.compile(r"^[0-9a-f]{40}$")
FIELDS = frozenset({"schema", "memory_id", "track_id", "kind", "status", "revision_sha", "claim", "context_tags", "applicability_tags", "exclusion_tags", "source_refs", "counterevidence_refs", "limits", "supersedes", "procedure_steps", "outcome_ref", "review_receipt_ref"})
class MemorySelectionError(ValueError):
    pass

def _require(ok: bool, message: str) -> None:
    if not ok:
        raise MemorySelectionError(message)

def _str(x: Any) -> bool:
    return isinstance(x, str) and bool(x.strip())

def _list(x: Any) -> bool:
    return isinstance(x, list) and all(_str(y) for y in x) and len(set(x)) == len(x)

def validate_memory(item: Mapping[str, Any]) -> None:
    _require(isinstance(item, dict) and set(item) == FIELDS, "invalid memory fields")
    _require(item["schema"] == SCHEMA, "invalid memory schema")
    for key in ("memory_id", "track_id", "claim", "limits"):
        _require(_str(item[key]), f"missing {key}")
    _require(item["kind"] in KINDS and item["status"] in STATES, "invalid kind/status")
    _require(isinstance(item["revision_sha"], str) and SHA.fullmatch(item["revision_sha"]) is not None, "invalid pinned revision")
    for key in ("context_tags", "applicability_tags", "exclusion_tags", "source_refs", "counterevidence_refs", "procedure_steps"):
        _require(_list(item[key]), f"invalid {key}")
    _require(bool(item["applicability_tags"]) and bool(item["source_refs"]), "memory needs conditions and sources")
    _require(not set(item["applicability_tags"]) & set(item["exclusion_tags"]), "contradictory applicability")
    _require(_list(item["supersedes"]) and item["memory_id"] not in item["supersedes"], "invalid supersedes")
    for key in ("outcome_ref", "review_receipt_ref"):
        _require(item[key] is None or _str(item[key]), f"invalid {key}")
    if item["kind"] == "PROCEDURAL":
        _require(bool(item["procedure_steps"]), "procedure must have steps")
    else:
        _require(not item["procedure_steps"], "non-procedure must not inject executable steps")
    if item["kind"] == "EPISODIC":
        _require(_str(item["outcome_ref"]), "experience must cite outcome")
    if item["status"] == "ACCEPTED":
        _require(_str(item["review_receipt_ref"]), "accepted memory needs review reference (not identity proof)")

def select_memory(memories: Sequence[Mapping[str, Any]], *, track_id: str,
                  context_tags: Sequence[str], permitted_statuses: Sequence[str] = ("ACCEPTED",)) -> dict[str, Any]:
    """Fail closed on contradictions; do not infer tag equivalence from keywords.

    Output is a candidate retrieval, not an instruction or an authority override.
    """
    _require(_str(track_id), "missing requested track")
    _require(_list(list(context_tags)) and bool(context_tags), "context tags required")
    _require(_list(list(permitted_statuses)) and bool(permitted_statuses) and
             set(permitted_statuses) <= STATES - {"SUPERSEDED", "RETRACTED", "CONTESTED"},
             "invalid permitted states")
    index: dict[str, Mapping[str, Any]] = {}
    for item in memories:
        validate_memory(item)
        _require(item["memory_id"] not in index, "duplicate memory ID")
        index[item["memory_id"]] = item
    for item in index.values():
        for older in item["supersedes"]:
            _require(older in index and index[older]["track_id"] == item["track_id"],
                     "broken or cross-track supersession")
        if item["status"] == "ACCEPTED" and item["supersedes"]:
            _require(all(index[old]["status"] in {"SUPERSEDED", "RETRACTED"} for old in item["supersedes"]),
                     "accepted replacement with live predecessor")
    query = set(context_tags)
    considered = []
    rejected = {}
    for item in index.values():
        ident = item["memory_id"]
        if item["track_id"] != track_id:
            rejected[ident] = "WRONG_TRACK"
        elif item["status"] not in permitted_statuses:
            rejected[ident] = "NOT_ELIGIBLE"
        elif set(item["exclusion_tags"]) & query:
            rejected[ident] = "EXPLICIT_EXCLUSION"
        elif not set(item["applicability_tags"]) <= query:
            rejected[ident] = "MISSING_REQUIRED_CONDITIONS"
        else:
            considered.append(item)
    considered.sort(key=lambda x: x["memory_id"])
    return {"status": "RETRIEVAL_CANDIDATES_NOT_TRUTH", "selected_ids": [x["memory_id"] for x in considered],
            "rejected": rejected, "owner_acceptance_created": False, "procedure_executed": False}
