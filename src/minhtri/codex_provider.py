"""Codex CLI provider adapter for lease-bound candidate generation.

Two phases:
1) read-only planning that must return a JSON object with declared changed_paths;
2) workspace-write execution inside an isolated candidate worktree.

The adapter never uses danger-full-access or bypass flags, never commits, never merges,
and validates actual changed paths after execution. Scope violations leave the worktree
dirty for inspection but return BLOCKED_SCOPE_VIOLATION.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import shutil
import subprocess
from typing import Any

from .generation import enforce_candidate_mutation
from .self_upgrade_runtime import SelfUpgradeSession


class CodexProviderError(RuntimeError):
    pass


@dataclass
class CodexCandidateProvider:
    session: SelfUpgradeSession
    candidate_branch: str
    candidate_root: Path
    codex_executable: str = "codex.cmd"
    model: str | None = None
    timeout_seconds: int = 900

    def _codex(self) -> str:
        found = shutil.which(self.codex_executable)
        if not found:
            raise CodexProviderError("BLOCKED_CODEX_CLI_NOT_FOUND")
        return found

    def _run(self, *, sandbox: str, prompt: str) -> subprocess.CompletedProcess[str]:
        if sandbox not in {"read-only", "workspace-write"}:
            raise CodexProviderError("unsupported sandbox")
        cmd = [
            self._codex(),
            "exec",
            "--ephemeral",
            "--sandbox",
            sandbox,
            "--cd",
            str(self.candidate_root),
            "--color",
            "never",
        ]
        if self.model:
            cmd += ["--model", self.model]
        cmd.append(prompt)
        return subprocess.run(
            cmd,
            cwd=self.candidate_root,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=self.timeout_seconds,
            check=False,
        )

    def _changed_paths(self) -> list[str]:
        proc = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=self.candidate_root,
            capture_output=True,
            text=True,
            timeout=30,
            check=True,
        )
        paths: set[str] = set()
        for raw in proc.stdout.splitlines():
            if len(raw) < 4:
                continue
            path = raw[3:].strip()
            if " -> " in path:
                path = path.split(" -> ", 1)[1]
            if path:
                paths.add(path.replace("\\", "/"))
        return sorted(paths)

    def plan(self, autonomy_packet: dict[str, Any]) -> dict[str, Any]:
        self.session.check()
        prompt = (
            "You are planning one bounded candidate improvement for MINH TRI. "
            "Do not edit files. Return ONLY one JSON object with keys: "
            "summary, hypothesis, changed_paths, tests. changed_paths must be a nonempty "
            "array of repository-relative files. Do not include authority, lease, owner, "
            "canonical state/law/architecture, CI workflow, or guard-test files. "
            "Base your plan on this autonomy packet:\n"
            + json.dumps(autonomy_packet, ensure_ascii=False, sort_keys=True)
        )
        proc = self._run(sandbox="read-only", prompt=prompt)
        if proc.returncode != 0:
            raise CodexProviderError("CODEX_PLAN_FAILED")
        text = proc.stdout.strip()
        try:
            plan = json.loads(text)
        except json.JSONDecodeError as exc:
            raise CodexProviderError("CODEX_PLAN_NOT_JSON") from exc
        paths = plan.get("changed_paths")
        if not isinstance(paths, list) or not paths:
            raise CodexProviderError("CODEX_PLAN_MISSING_CHANGED_PATHS")
        normalized = list(
            enforce_candidate_mutation(
                self.session.guard,
                candidate_branch=self.candidate_branch,
                changed_paths=paths,
            )
        )
        plan["changed_paths"] = normalized
        return plan

    def propose(self, autonomy_packet: dict[str, Any]) -> dict[str, Any]:
        plan = self.plan(autonomy_packet)
        declared = list(plan["changed_paths"])

        def action() -> dict[str, Any]:
            self.session.guard.before_mutation()
            prompt = (
                "Implement exactly this bounded candidate plan in the current candidate worktree. "
                "You may edit ONLY the declared changed_paths. Do not commit, merge, push, alter "
                "git configuration, change authority/security/lease/owner/canonical state files, "
                "or use network credentials. Run relevant local tests if available. Plan:\n"
                + json.dumps(plan, ensure_ascii=False, sort_keys=True)
            )
            proc = self._run(sandbox="workspace-write", prompt=prompt)
            actual = self._changed_paths()
            try:
                enforce_candidate_mutation(
                    self.session.guard,
                    candidate_branch=self.candidate_branch,
                    changed_paths=actual,
                )
            except Exception as exc:
                return {
                    "status": "BLOCKED_SCOPE_VIOLATION",
                    "reason": type(exc).__name__,
                    "declared_paths": declared,
                    "actual_paths": actual,
                    "codex_returncode": proc.returncode,
                }
            undeclared = sorted(set(actual) - set(declared))
            if undeclared:
                return {
                    "status": "BLOCKED_UNDECLARED_PATH",
                    "declared_paths": declared,
                    "actual_paths": actual,
                    "undeclared_paths": undeclared,
                    "codex_returncode": proc.returncode,
                }
            if proc.returncode != 0:
                return {
                    "status": "BLOCKED_CODEX_EXEC_FAILED",
                    "declared_paths": declared,
                    "actual_paths": actual,
                    "codex_returncode": proc.returncode,
                }
            return {
                "status": "CANDIDATE_WORKTREE_MUTATED_PENDING_TEST",
                "declared_paths": declared,
                "actual_paths": actual,
                "codex_returncode": proc.returncode,
                "committed": False,
                "merged": False,
                "pushed": False,
            }

        return {"changed_paths": declared, "action": action, "plan": plan}
