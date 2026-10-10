"""Bounded, read-only learning continuity and application-evidence contract.

This module verifies candidate records. It does not authorize owner acceptance,
mutate GitHub, select learning topics, or self-grade a model's answers.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence

from .learning_capability import CapabilityEvidenceError, validate_semantic_skeleton


REGISTRY_SCHEMA = "minhtri-learning-tracks/v1"
DELTA_SCHEMA = "minhtri-learning-delta/v1"
TRACK_FIELDS = frozenset({
    "track_id", "task_id", "checkpoint_id", "last_durable_checkpoint_id",
    "latest_delta_id", "latest_delta_path", "working_cursor_source", "research_intake", "status",
})
REGISTRY_FIELDS = frozenset({"schema", "tracks"})
RESEARCH_FIELDS = frozenset({
    "source_type", "number", "checkpoint_id", "record_role",
    "source_head_sha", "may_advance_cursor", "may_promote_checkpoint",
})
RESEARCH_ROLES = frozenset({
    "UNMERGED_LEGACY_DRAFT", "SOURCE_AUDITED_CANDIDATE", "RESEARCH_TRACE_ONLY",
})
SOURCE_FIELDS = frozenset({
    "provider", "pr_number", "author_login", "source_head_sha", "required_label",
})
DELTA_FIELDS = frozenset({
    "schema", "cursor_id", "track_id", "checkpoint_id", "parent_cursor_id",
    "delta_kind", "new_knowledge", "corrections", "source_refs", "model",
    "application", "milindapanha", "open_questions", "exact_next_question",
    "provenance", "status",
})
MODEL_FIELDS = frozenset({"claim", "evidence_class", "counter_reading", "limits", "semantic_skeleton"})
APPLICATION_FIELDS = frozenset({
    "status", "heldout_case_ref", "frozen_rubric_ref", "frozen_rubric_sha256",
    "attempt_ref", "reviewer_seat", "review_receipt_ref", "transfer_trial_ref",
})
MILINDA_FIELDS = frozenset({"consulted", "role", "source_refs"})
PROVENANCE_FIELDS = frozenset({
    "author_seat", "source_head_sha", "recorded_at", "owner_acceptance_receipt",
})
WORKING_STATUS = "WORKING_NOTE_NOT_ACCEPTED"
APPLICATION_STATUSES = {
    "NOT_TESTED", "INDEPENDENT_REVIEW_RECORDED_NOT_VERIFIED",
    "FAILURE_RECORDED_NOT_VERIFIED", "INCONCLUSIVE",
}
EVIDENCE_CLASSES = {
    "TEXT_ATTESTED", "CROSS_TEXT_SYNTHESIS", "LATER/PARACANONICAL",
    "LATER_EXPLANATORY_EARLY_COMPATIBLE", "UNCERTAINTY", "UNTESTED",
}
_ID_RE = re.compile(r"^[A-Z][A-Z0-9_-]{2,99}$")
_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
_HEX256_RE = re.compile(r"^[0-9a-f]{64}$")
_COMMENT_LABEL = "LEARNING_CURSOR_V1"
_REQUIRED_COMMENT_FIELDS = (
    "CURSOR_ID", "SUPERSEDES", "SOURCE_HEAD_SHA", "ALREADY_STUDIED",
    "DELTA", "OPEN", "EXACT_NEXT_QUESTION", "STATUS",
)


class LearningContinuityError(ValueError):
    """A continuity contract failed closed; do not infer a next lesson."""


@dataclass(frozen=True)
class LearningPosition:
    track_id: str
    checkpoint_id: str
    cursor_id: str
    next_question: str
    source_kind: str
    proof: str
    knowledge_status: str = WORKING_STATUS


def _require(condition: bool, why: str) -> None:
    if not condition:
        raise LearningContinuityError(why)


def _no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, val in pairs:
        _require(key not in out, f"duplicate JSON key: {key}")
        out[key] = val
    return out


def read_json(path: Path) -> dict[str, Any]:
    try:
        result = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_no_duplicate_keys)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise LearningContinuityError(f"unreadable record: {path.name}") from exc
    _require(isinstance(result, dict), "root JSON must be an object")
    return result


def _keys(data: Any, expected: frozenset[str], label: str) -> None:
    _require(isinstance(data, dict), f"{label} must be an object")
    _require(set(data) == expected, f"{label} has missing or shadow fields")


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _strings(value: Any, *, allow_empty: bool = True) -> bool:
    return (isinstance(value, list) and (allow_empty or bool(value))
            and all(_nonempty(item) for item in value))


def _valid_path(relative: str, track_id: str) -> bool:
    if not isinstance(relative, str) or "\\" in relative or "%" in relative:
        return False
    path = PurePosixPath(relative)
    return (not path.is_absolute() and ".." not in path.parts
            and str(path) == relative
            and len(path.parts) == 5
            and tuple(path.parts[:3]) == ("docs", "learning", "deltas")
            and path.name.endswith(".json")
            and path.parent.name == track_id)


def validate_registry(registry: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    _keys(registry, REGISTRY_FIELDS, "registry")
    _require(registry["schema"] == REGISTRY_SCHEMA, "unsupported registry schema")
    _require(isinstance(registry["tracks"], list) and registry["tracks"], "tracks required")
    lookup: dict[str, dict[str, Any]] = {}
    for track in registry["tracks"]:
        _keys(track, TRACK_FIELDS, "track")
        name = track["track_id"]
        _require(_nonempty(name) and _ID_RE.fullmatch(name) is not None,
                 "invalid track ID")
        _require(name not in lookup, "duplicate track ID")
        _require(_nonempty(track["task_id"]) and _nonempty(track["checkpoint_id"]),
                 "task and checkpoint required")
        _require(_nonempty(track["last_durable_checkpoint_id"]),
                 "last durable checkpoint required")
        _require(track["status"] == WORKING_STATUS, "working track must not self-accept")
        delta_id, delta_path = track["latest_delta_id"], track["latest_delta_path"]
        _require((delta_id is None) == (delta_path is None),
                 "cursor ID and path must be both present or both absent")
        if delta_id is not None:
            _require(_nonempty(delta_id) and _ID_RE.fullmatch(delta_id) is not None,
                     "invalid delta cursor ID")
            _require(_valid_path(delta_path, name)
                     and PurePosixPath(delta_path).stem == delta_id,
                     "invalid delta path or cursor pointer mismatch")
        source = track["working_cursor_source"]
        _keys(source, SOURCE_FIELDS, "working cursor source")
        _require(source["provider"] == "github_pr_comments", "unknown working cursor provider")
        _require(type(source["pr_number"]) is int and source["pr_number"] > 0,
                 "invalid PR number")
        _require(_nonempty(source["author_login"]), "cursor author required")
        _require(source["required_label"] == _COMMENT_LABEL, "cursor label changed")
        _require(isinstance(source["source_head_sha"], str)
                 and _SHA_RE.fullmatch(source["source_head_sha"]) is not None,
                 "invalid source SHA")
        intake = track["research_intake"]
        _require(isinstance(intake, list), "research intake must be a list")
        seen_refs: set[tuple[str, int]] = set()
        for candidate in intake:
            _keys(candidate, RESEARCH_FIELDS, "research intake source")
            kind = candidate["source_type"]
            number = candidate["number"]
            _require(kind in ("PR", "ISSUE") and type(number) is int and number > 0,
                     "invalid research source reference")
            _require((kind, number) not in seen_refs, "duplicate research source reference")
            seen_refs.add((kind, number))
            _require(_nonempty(candidate["checkpoint_id"]) and
                     re.fullmatch(r"[A-Za-z0-9_-]{2,80}", candidate["checkpoint_id"]) is not None,
                     "research checkpoint identifier malformed")
            _require(candidate["record_role"] in RESEARCH_ROLES,
                     "research role could be promoted or is unsupported")
            _require(candidate["may_advance_cursor"] is False and
                     candidate["may_promote_checkpoint"] is False,
                     "research source must never create canonical authority")
            source_sha = candidate["source_head_sha"]
            _require((kind == "PR" and isinstance(source_sha, str) and
                      _SHA_RE.fullmatch(source_sha) is not None) or
                     (kind == "ISSUE" and source_sha is None),
                     "research source revision pin invalid")
            if candidate["record_role"] == "RESEARCH_TRACE_ONLY":
                _require(kind == "ISSUE", "research trace role requires ISSUE")
        lookup[name] = track
    return lookup


def validate_delta(delta: Mapping[str, Any]) -> None:
    _keys(delta, DELTA_FIELDS, "delta")
    _require(delta["schema"] == DELTA_SCHEMA, "delta schema mismatch")
    for field in ("cursor_id", "track_id"):
        _require(isinstance(delta[field], str)
                 and _ID_RE.fullmatch(delta[field]) is not None, f"invalid {field}")
    _require(_nonempty(delta["checkpoint_id"]), "checkpoint required")
    _require(delta["parent_cursor_id"] is None or
             (isinstance(delta["parent_cursor_id"], str)
              and _ID_RE.fullmatch(delta["parent_cursor_id"]) is not None),
             "invalid parent cursor")
    _require(delta["status"] == WORKING_STATUS, "delta cannot claim Owner acceptance")
    _require(delta["delta_kind"] in {"NEW_EVIDENCE", "CORRECTION", "NO_NEW_KNOWLEDGE"},
             "invalid delta kind")
    for key in ("new_knowledge", "corrections", "source_refs", "open_questions"):
        _require(_strings(delta[key]), f"{key} must contain strings")
    if delta["delta_kind"] == "NEW_EVIDENCE":
        _require(bool(delta["new_knowledge"]) and bool(delta["source_refs"]),
                 "new evidence needs new content and source refs")
    if delta["delta_kind"] == "CORRECTION":
        _require(bool(delta["corrections"]) and bool(delta["source_refs"]),
                 "correction needs corrected claim and sources")
    if delta["delta_kind"] == "NO_NEW_KNOWLEDGE":
        _require(not delta["new_knowledge"] and not delta["corrections"],
                 "NO_NEW_KNOWLEDGE cannot also claim new content")
    _require(_nonempty(delta["exact_next_question"]) and
             len(delta["exact_next_question"].strip()) >= 40,
             "next research question must be actionable, not an ID")
    model = delta["model"]
    _keys(model, MODEL_FIELDS, "understanding model")
    for k in ("claim", "counter_reading", "limits"):
        _require(_nonempty(model[k]), f"model.{k} required")
    _require(model["evidence_class"] in EVIDENCE_CLASSES,
             "unsupported evidence class or self-promotion")
    try:
        validate_semantic_skeleton(model["semantic_skeleton"])
    except CapabilityEvidenceError as exc:
        raise LearningContinuityError(f"understanding record invalid: {exc}") from exc
    label = model["semantic_skeleton"]["source_vs_interpretation"]
    if model["evidence_class"] == "TEXT_ATTESTED":
        _require(label == "SOURCE_REPORT", "attested source cannot silently become synthesis")
    elif model["evidence_class"] == "CROSS_TEXT_SYNTHESIS":
        _require(label == "BOUNDED_SYNTHESIS", "synthesis must be labeled interpretation")
    provenance = delta["provenance"]
    _keys(provenance, PROVENANCE_FIELDS, "provenance")
    _require(_nonempty(provenance["author_seat"]) and _nonempty(provenance["recorded_at"]),
             "provenance requires author seat and date")
    _require(isinstance(provenance["source_head_sha"], str)
             and _SHA_RE.fullmatch(provenance["source_head_sha"]) is not None,
             "source head SHA malformed")
    _require(provenance["owner_acceptance_receipt"] is None,
             "a working delta cannot include Owner acceptance receipt")
    mil = delta["milindapanha"]
    _keys(mil, MILINDA_FIELDS, "Milindapanha")
    _require(type(mil["consulted"]) is bool and _nonempty(mil["role"])
             and _strings(mil["source_refs"]), "invalid Milindapanha consultation log")
    if delta["track_id"] == "BUDDHIST_THOUGHT":
        _require(mil["consulted"], "Buddhist study must consult Milindapanha")
    app = delta["application"]
    _keys(app, APPLICATION_FIELDS, "application evidence")
    _require(app["status"] in APPLICATION_STATUSES,
             "application may not be self-certified VERIFIED or ACCEPTED")
    if app["status"] == "NOT_TESTED":
        _require(all(app[k] is None for k in APPLICATION_FIELDS - {"status"}),
                 "NOT_TESTED cannot contain a false application receipt")
    else:
        for key in APPLICATION_FIELDS - {"status"}:
            _require(_nonempty(app[key]), f"application.{key} is required")
        _require(_HEX256_RE.fullmatch(app["frozen_rubric_sha256"]) is not None,
                 "held-out rubric SHA-256 required")
        _require(app["reviewer_seat"] != provenance["author_seat"],
                 "application cannot be self-reviewed")


def _load_file_chain(root: Path, track: Mapping[str, Any]) -> LearningPosition:
    track_id = track["track_id"]
    delta_dir = root / "docs" / "learning" / "deltas" / track_id
    _require(delta_dir.is_dir(), "recorded delta directory missing")
    for directory in (root / "docs", root / "docs" / "learning",
                      root / "docs" / "learning" / "deltas", delta_dir):
        _require(not directory.is_symlink(), "symlink directory in delta path")
    entries: dict[str, dict[str, Any]] = {}
    for path in delta_dir.iterdir():
        _require(path.suffix == ".json" and path.is_file() and not path.is_symlink(),
                 "unexpected entry in delta directory")
        doc = read_json(path)
        validate_delta(doc)
        _require(doc["cursor_id"] == path.stem and doc["track_id"] == track_id,
                 "delta file is not bound to track/cursor")
        _require(doc["cursor_id"] not in entries, "duplicate delta ID")
        entries[doc["cursor_id"]] = doc
    _require(bool(entries), "pointer references empty delta directory")
    next_by_parent: dict[str | None, str] = {}
    for entry in entries.values():
        parent = entry["parent_cursor_id"]
        _require(parent not in next_by_parent,
                 "two delta children of one cursor; human reconciliation required")
        next_by_parent[parent] = entry["cursor_id"]
    _require(None in next_by_parent, "delta chain has no root")
    seen: set[str] = set()
    position: str | None = next_by_parent[None]
    last: dict[str, Any] | None = None
    while position is not None:
        _require(position not in seen, "delta cycle")
        seen.add(position)
        last = entries[position]
        position = next_by_parent.get(position)
    _require(seen == set(entries), "unlinked or competing delta in track")
    _require(last is not None and last["cursor_id"] == track["latest_delta_id"],
             "track pointer is stale: cannot repeat earlier question")
    expected_path = "docs/learning/deltas/" + track_id + "/" + last["cursor_id"] + ".json"
    _require(track["latest_delta_path"] == expected_path, "path does not match last cursor")
    _require(last["checkpoint_id"] == track["checkpoint_id"], "checkpoint mismatch")
    return LearningPosition(track_id=track_id, checkpoint_id=last["checkpoint_id"],
                            cursor_id=last["cursor_id"],
                            next_question=last["exact_next_question"],
                            source_kind="CANDIDATE_FILE_CHAIN_NOT_ACCEPTED",
                            proof=expected_path)


def _comment_fields(body: str) -> dict[str, str] | None:
    if not isinstance(body, str):
        return None
    first = body.splitlines()[:1]
    if first != [_COMMENT_LABEL]:
        return None
    fields: dict[str, str] = {}
    for line in body.splitlines()[1:]:
        # Only the top header is authority; quoted historical cursors have no effect.
        if line.startswith("=== BEGIN VERBATIM"):
            break
        match = re.match(r"^([A-Z_]+):\s*(.*)$", line)
        if match:
            if match.group(1) in fields:
                return None
            fields[match.group(1)] = match.group(2).strip()
    if any(not fields.get(key) for key in _REQUIRED_COMMENT_FIELDS):
        return None
    if _ID_RE.fullmatch(fields["CURSOR_ID"]) is None:
        return None
    if fields["STATUS"] != "WORKING_NOTE — NOT ACCEPTED":
        return None
    if len(fields["EXACT_NEXT_QUESTION"]) < 40:
        return None
    return fields


def recover_working_comment(track: Mapping[str, Any], comments: Sequence[Mapping[str, Any]],
                            *, live_pr_head_sha: str) -> LearningPosition:
    source = track["working_cursor_source"]
    _require(live_pr_head_sha == source["source_head_sha"],
             "PR HEAD changed: Owner decision needed before more study")
    valid: list[tuple[int, dict[str, str]]] = []
    malformed: set[int] = set()
    for comment in comments:
        identity = comment.get("author")
        if identity is None and isinstance(comment.get("user"), dict):
            identity = comment["user"].get("login")
        if identity != source["author_login"]:
            continue
        body = comment.get("body", "")
        # Never silently fall back to an old cursor if a newer cursor
        # is malformed. Later explicit reconciliation can clear that risk.
        candidate = isinstance(body, str) and body.startswith(_COMMENT_LABEL)
        fields = _comment_fields(body)
        if fields is None and not candidate:
            continue
        ident = comment.get("id")
        _require(type(ident) is int and ident > 0, "cursor comment lacks GitHub ID")
        if fields is None:
            malformed.add(ident)
            continue
        _require(fields["SOURCE_HEAD_SHA"] == live_pr_head_sha,
                 "cursor provenance SHA differs from PR HEAD")
        valid.append((ident, fields))
    _require(bool(valid), "no valid learning cursor: stop; do not repeat old lesson")
    valid.sort(key=lambda item: item[0])
    reconciled: set[int] = set()
    for ident, fields in valid:
        value = fields.get("RECONCILES_INVALID_COMMENT", "")
        if value:
            _require(value.isdecimal(), "invalid cursor reconciliation ID")
            prior = int(value)
            _require(prior in malformed and prior < ident,
                     "cursor reconciliation does not refer to an earlier malformed note")
            reconciled.add(prior)
    _require(not (malformed - reconciled),
             "unreconciled malformed learning cursor: stop; do not replay old lesson")
    for previous, later in zip(valid, valid[1:]):
        supersedes = later[1]["SUPERSEDES"].split(" ", 1)[0]
        _require(supersedes == str(previous[0]),
                 "competing/stale cursor successor: stop; do not pick newest blindly")
    cursor_id = valid[-1][1]["CURSOR_ID"]
    _require(len(set(item[1]["CURSOR_ID"] for item in valid)) == len(valid),
             "duplicate learning cursor IDs")
    return LearningPosition(track_id=track["track_id"],
                            checkpoint_id=track["checkpoint_id"],
                            cursor_id=cursor_id,
                            next_question=valid[-1][1]["EXACT_NEXT_QUESTION"],
                            source_kind="PR_COMMENT_WORKING_NOTE_NOT_CANONICAL",
                            proof=f"PR#{source['pr_number']}:comment#{valid[-1][0]}")



def validate_canonical_learning_route(root: Path, track_id: str, *,
                                      for_mutation: bool = False) -> str:
    """Read active route from canonical project facts, never caller assertions.

    For mutation only: check declared Class D branch binding. This is still
    NOT an Owner authentication, branch CAS, acceptance, or write permission.
    """
    registry = read_json(root / "state" / "learning_tracks.json")
    tracks = validate_registry(registry)
    _require(track_id in tracks, "learning track not registered")
    track = tracks[track_id]
    boot = read_json(root / "state" / "bootstrap.json")
    current = read_json(root / "state" / "current.yaml")
    tasks = read_json(root / "state" / "tasks.yaml")
    _require(boot.get("current_state") == "state/current.yaml"
             and boot.get("task_registry") == "state/tasks.yaml",
             "invalid canonical boot root routing")
    _require(current.get("boot_root") == "state/bootstrap.json"
             and current.get("task_registry") == boot["task_registry"],
             "boot/current authority pointers conflict")
    _require(isinstance(boot.get("law_precedence"), str)
             and bool(boot["law_precedence"])
             and current.get("law_precedence") == boot["law_precedence"],
             "boot/current learning law routing conflict")
    _require(isinstance(boot.get("master_blueprint"), str)
             and bool(boot["master_blueprint"])
             and current.get("master_blueprint") == boot["master_blueprint"]
             and current.get("current_architecture") == boot["master_blueprint"],
             "boot/current blueprint routing conflict")
    _require(current.get("active_workstream") == "OWNER_DIRECTED_LEARNING",
             "canonical active workstream is not learning")
    task_id = track["task_id"]
    _require(current.get("active_task_id") == task_id,
             "canonical active task mismatch: do not infer route from caller data")
    _require(isinstance(tasks.get("tasks"), list),
             "canonical task registry has no task list")
    matched = [task for task in tasks["tasks"]
               if isinstance(task, dict) and task.get("task_id") == task_id]
    _require(len(matched) == 1,
             "canonical active task missing or duplicated")
    task = matched[0]
    _require(task.get("status") == "IN_PROGRESS"
             and task.get("change_class") == "D",
             "canonical active learning task not IN_PROGRESS Class D")
    checkpoint = task.get("learning_checkpoint")
    _require(isinstance(checkpoint, dict)
             and checkpoint.get("current_checkpoint_id") == track["checkpoint_id"]
             and checkpoint.get("last_accepted_checkpoint_id") ==
             track["last_durable_checkpoint_id"],
             "learning checkpoint chain conflicts with canonical task")
    _require(checkpoint.get("checkpoint_acceptance") == "NOT_CURRENT"
             and checkpoint.get("acceptance_receipt_ref") is None,
             "unaccepted study route carries unauthorized checkpoint promotion")
    if for_mutation:
        binding = task.get("branch_binding")
        _require(_nonempty(task.get("branch"))
                 and _nonempty(binding) and not binding.startswith("NONE_"),
                 "Class D study branch is not Owner-bound for mutation")
    return task_id

def recover_learning_position(root: Path, track_id: str, *, active_task_id: str,
                              comments: Sequence[Mapping[str, Any]] | None = None,
                              live_pr_head_sha: str | None = None) -> LearningPosition:
    """Strict read-only recovery; main task routing always outranks working notes."""
    registry = read_json(root / "state" / "learning_tracks.json")
    tracks = validate_registry(registry)
    _require(track_id in tracks, "track not registered; Owner must choose learning work")
    track = tracks[track_id]
    authoritative_id = validate_canonical_learning_route(root, track_id)
    _require(active_task_id == authoritative_id,
             "canonical active task mismatch: caller does not match protected route")
    if track["latest_delta_id"] is not None:
        return _load_file_chain(root, track)
    _require(comments is not None and live_pr_head_sha is not None,
             "live PR comments/HEAD are required for provisional cursor recovery")
    return recover_working_comment(track, comments, live_pr_head_sha=live_pr_head_sha)


def validate_append_intent(root: Path, *, track_id: str, proposed: Mapping[str, Any],
                           expected_parent_cursor_id: str | None,
                           expected_registry_sha256: str) -> str:
    """Validate optimistic preconditions for a protected Git tree update.

    This is NOT a GitHub transaction. The caller must update a non-main branch
    with an expected branch SHA lease, then read the committed result again.
    """
    raw = (root / "state" / "learning_tracks.json").read_bytes()
    _require(hashlib.sha256(raw).hexdigest() == expected_registry_sha256,
             "stale learning registry; re-read before preparing write")
    tracks = validate_registry(json.loads(raw, object_pairs_hook=_no_duplicate_keys))
    _require(track_id in tracks, "learning track missing")
    track = tracks[track_id]
    validate_canonical_learning_route(root, track_id, for_mutation=True)
    validate_delta(proposed)
    _require(proposed["track_id"] == track_id, "delta track mismatch")
    _require(proposed["checkpoint_id"] == track["checkpoint_id"],
             "unapproved checkpoint transition")
    _require(proposed["parent_cursor_id"] == expected_parent_cursor_id,
             "proposed parent differs from expected cursor")
    _require(track["latest_delta_id"] == expected_parent_cursor_id,
             "stale cursor parent / concurrent writer detected")
    _require(proposed["provenance"]["source_head_sha"] ==
             track["working_cursor_source"]["source_head_sha"],
             "delta based on a different source head")
    _require(proposed["cursor_id"] != proposed["parent_cursor_id"],
             "candidate cursor cannot supersede itself")
    relative = f"docs/learning/deltas/{track_id}/{proposed['cursor_id']}.json"
    _require(_valid_path(relative, track_id), "invalid append-only delta path")
    destination = root / relative
    _require(not destination.exists() and not destination.is_symlink(),
             "append-only delta destination already exists")
    for parent in destination.parents:
        if parent == root:
            break
        _require(not parent.is_symlink(), "symlink parent for append-only delta")
    return relative
