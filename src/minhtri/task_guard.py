from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


WRITABLE_STATES = {"READY", "ASSIGNED", "IN_PROGRESS", "REVIEWED_REVISE", "DRAFT"}


class GuardError(RuntimeError):
    pass


@dataclass(frozen=True)
class GuardResult:
    allowed: bool
    reason: str
    task_id: str
    base_sha: str
    conflicting_paths: tuple[str, ...] = ()


def _norm(path: str) -> str:
    return path.strip().replace("\\", "/").lstrip("./")


def _path_matches_scope(path: str, scope_entry: str) -> bool:
    path = _norm(path)
    scope_entry = _norm(scope_entry)
    if scope_entry.startswith("pull_requests:") or scope_entry.startswith("PR#"):
        return False
    if scope_entry.endswith("/"):
        return path.startswith(scope_entry)
    return path == scope_entry or path.startswith(scope_entry + "/")


def find_task(registry: dict, task_id: str) -> dict:
    matches = [t for t in registry.get("tasks", []) if t.get("task_id") == task_id]
    if len(matches) != 1:
        raise GuardError(f"task_id must resolve exactly once: {task_id}")
    return matches[0]


def evaluate_task_write(
    *,
    registry: dict,
    task_id: str,
    expected_generation: int,
    declared_base_sha: str,
    current_main_sha: str,
    main_changed_paths: Iterable[str],
    proposed_paths: Iterable[str],
) -> GuardResult:
    task = find_task(registry, task_id)
    status = task.get("status")
    if status not in WRITABLE_STATES:
        return GuardResult(False, f"task state {status!r} is not writable", task_id, declared_base_sha)

    generation = int(task.get("generation", 1))
    if generation != expected_generation:
        return GuardResult(False, f"generation mismatch task={generation} seat={expected_generation}", task_id, declared_base_sha)

    task_base = task.get("base_sha")
    if task_base != declared_base_sha:
        return GuardResult(False, f"base_sha mismatch task={task_base} seat={declared_base_sha}", task_id, declared_base_sha)

    if task.get("branch") is None:
        return GuardResult(False, "task has no assigned branch/write seat", task_id, declared_base_sha)

    scope = tuple(task.get("scope", []))
    if not scope:
        return GuardResult(False, "task has empty write scope", task_id, declared_base_sha)

    proposed = {_norm(p) for p in proposed_paths}
    out_of_scope = sorted(p for p in proposed if not any(_path_matches_scope(p, s) for s in scope))
    if out_of_scope:
        return GuardResult(False, "proposed write exceeds task scope", task_id, declared_base_sha, tuple(out_of_scope))

    if declared_base_sha == current_main_sha:
        return GuardResult(True, "base matches current main", task_id, declared_base_sha)

    changed = {_norm(p) for p in main_changed_paths}
    conflicting = sorted(p for p in changed if any(_path_matches_scope(p, s) for s in scope))
    if conflicting:
        return GuardResult(
            False,
            "current main changed inside task write scope since base_sha",
            task_id,
            declared_base_sha,
            tuple(conflicting),
        )
    return GuardResult(True, "main advanced but no in-scope conflict was detected", task_id, declared_base_sha)
