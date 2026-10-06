from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

from minhtri.semantic_guard import evaluate_semantic_dependencies


ALLOWED_STATUSES = {
    "ACTIVE",
    "PENDING_REVIEW",
    "UNCERTAIN",
    "DISPUTED",
    "SUPERSEDED",
    "REFUTED",
}
ALLOWED_CLASSES = {"ATTESTED", "SYNTHESIS", "SECONDARY", "UNCERTAIN", "REFUTED"}
REQUIRED_FIELDS = {
    "schema",
    "record_type",
    "id",
    "domain",
    "class",
    "status",
    "statement",
    "source_refs",
    "evidence_refs",
    "contradicts",
    "supersedes",
    "depends_on",
    "provenance",
}
LIST_FIELDS = {"source_refs", "evidence_refs", "contradicts", "supersedes", "depends_on"}


@dataclass(frozen=True)
class FastLaneResult:
    allowed: bool
    reasons: tuple[str, ...] = ()
    stale_dependency_ids: tuple[str, ...] = ()


def _record_index(records: Iterable[dict]) -> tuple[dict[str, dict], set[str]]:
    index: dict[str, dict] = {}
    duplicates: set[str] = set()
    for record in records:
        record_id = record.get("id")
        if not isinstance(record_id, str) or not record_id:
            continue
        if record_id in index:
            duplicates.add(record_id)
        else:
            index[record_id] = record
    return index, duplicates


def validate_fast_lane_change(
    *,
    all_records: Sequence[dict],
    changed_record_ids: Sequence[str],
    domain_rule_refs: Mapping[str, Sequence[str]],
    protected_review_required: bool,
    autonomous_merge: bool,
    self_verified: bool,
) -> FastLaneResult:
    """Validate a lightweight learning update without granting merge authority."""

    reasons: list[str] = []
    stale_ids: set[str] = set()

    if not protected_review_required:
        reasons.append("protected-main review must remain required")
    if autonomous_merge:
        reasons.append("autonomous merge is forbidden in Knowledge Fast Lane v1")
    if self_verified:
        reasons.append("self-VERIFIED promotion is forbidden")
    if not changed_record_ids:
        reasons.append("at least one changed knowledge record is required")

    index, duplicates = _record_index(all_records)
    changed = tuple(dict.fromkeys(changed_record_ids))

    for record_id in changed:
        if record_id in duplicates:
            reasons.append(f"changed record id resolves ambiguously: {record_id}")
            continue

        record = index.get(record_id)
        if record is None:
            reasons.append(f"changed record id is missing: {record_id}")
            continue

        missing = sorted(REQUIRED_FIELDS - set(record))
        if missing:
            reasons.append(f"{record_id}: missing required fields: {', '.join(missing)}")
            continue

        for field in LIST_FIELDS:
            if not isinstance(record.get(field), list):
                reasons.append(f"{record_id}: {field} must be a list")

        status = str(record.get("status", "")).upper()
        if status not in ALLOWED_STATUSES:
            reasons.append(f"{record_id}: unsupported status {status!r}")

        record_class = str(record.get("class", "")).upper()
        if record_class not in ALLOWED_CLASSES:
            reasons.append(f"{record_id}: unsupported class {record_class!r}")

        provenance = record.get("provenance")
        if not isinstance(provenance, dict) or not provenance:
            reasons.append(f"{record_id}: provenance must be a non-empty object")

        domain = record.get("domain")
        refs = domain_rule_refs.get(domain, ()) if isinstance(domain, str) else ()
        if not refs or not all(isinstance(ref, str) and ref.strip() for ref in refs):
            reasons.append(f"{record_id}: domain rule reference is required for domain {domain!r}")

        if not isinstance(record.get("statement"), str) or not record["statement"].strip():
            reasons.append(f"{record_id}: statement must be non-empty")

        if record.get("record_type") == "claim":
            if not record.get("source_refs") and not record.get("evidence_refs"):
                reasons.append(f"{record_id}: claim requires source_refs or evidence_refs")

        dependencies = record.get("depends_on")
        if isinstance(dependencies, list):
            if record_id in dependencies:
                reasons.append(f"{record_id}: record cannot depend on itself")
            semantic = evaluate_semantic_dependencies(
                records=all_records,
                dependency_ids=dependencies,
                require_fresh=True,
            )
            if not semantic.allowed:
                stale_ids.update(semantic.stale_dependency_ids)
                details = (
                    list(semantic.stale_dependency_ids)
                    + list(semantic.missing_dependency_ids)
                    + list(semantic.ambiguous_dependency_ids)
                )
                reasons.append(
                    f"{record_id}: semantic dependency freshness failed"
                    + (f": {', '.join(details)}" if details else "")
                )

        supersedes = record.get("supersedes")
        if isinstance(supersedes, list):
            for target_id in supersedes:
                if target_id == record_id:
                    reasons.append(f"{record_id}: record cannot supersede itself")
                    continue
                if target_id in duplicates:
                    reasons.append(f"{record_id}: superseded target is ambiguous: {target_id}")
                    continue
                target = index.get(target_id)
                if target is None:
                    reasons.append(f"{record_id}: superseded target is missing: {target_id}")
                    continue
                if str(target.get("status", "")).upper() != "SUPERSEDED":
                    reasons.append(
                        f"{record_id}: superseded target must be marked SUPERSEDED in the same protected update: {target_id}"
                    )

    return FastLaneResult(
        allowed=not reasons,
        reasons=tuple(reasons),
        stale_dependency_ids=tuple(sorted(stale_ids)),
    )
