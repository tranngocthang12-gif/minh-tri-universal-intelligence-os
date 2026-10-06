from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


FRESH_STATUSES = {"ACTIVE", "UNCERTAIN"}
STALE_STATUSES = {"SUPERSEDED", "REFUTED", "DISPUTED", "PENDING_REVIEW"}


@dataclass(frozen=True)
class SemanticGuardResult:
    allowed: bool
    reason: str
    stale_dependency_ids: tuple[str, ...] = ()
    missing_dependency_ids: tuple[str, ...] = ()
    ambiguous_dependency_ids: tuple[str, ...] = ()


def _index_records(records: Iterable[dict]) -> tuple[dict[str, dict], set[str]]:
    index: dict[str, dict] = {}
    duplicate_ids: set[str] = set()
    for record in records:
        record_id = record.get("id")
        if not isinstance(record_id, str) or not record_id:
            continue
        if record_id in index:
            duplicate_ids.add(record_id)
        else:
            index[record_id] = record
    return index, duplicate_ids


def evaluate_semantic_dependencies(
    *,
    records: Iterable[dict],
    dependency_ids: Iterable[str],
    require_fresh: bool = True,
) -> SemanticGuardResult:
    """Check semantic knowledge dependencies without auto-following replacements.

    When freshness is required, missing/duplicate dependencies fail closed.
    ACTIVE and UNCERTAIN are not retired states. SUPERSEDED, REFUTED,
    DISPUTED, and PENDING_REVIEW are not valid established dependencies.
    A caller must explicitly refresh lineage rather than silently following
    a supersession.
    """
    deps = tuple(dict.fromkeys(dependency_ids))
    index, duplicates = _index_records(records)

    missing = sorted(dep for dep in deps if dep not in index)
    ambiguous = sorted(dep for dep in deps if dep in duplicates)
    stale = sorted(
        dep for dep in deps
        if dep in index and str(index[dep].get("status", "")).upper() in STALE_STATUSES
    )

    if require_fresh and ambiguous:
        return SemanticGuardResult(False, "semantic dependency resolves ambiguously", (), (), tuple(ambiguous))
    if require_fresh and missing:
        return SemanticGuardResult(False, "semantic dependency is missing", (), tuple(missing), ())
    if require_fresh and stale:
        return SemanticGuardResult(False, "semantic dependency is stale or not established", tuple(stale), (), ())

    return SemanticGuardResult(True, "semantic dependencies satisfy the requested freshness policy")


def dependency_status_map(records: Iterable[dict], dependency_ids: Iterable[str]) -> dict[str, str]:
    index, _ = _index_records(records)
    return {dep: str(index.get(dep, {}).get("status", "MISSING")).upper() for dep in dependency_ids}
