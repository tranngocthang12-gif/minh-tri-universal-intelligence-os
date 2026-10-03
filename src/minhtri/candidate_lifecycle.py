"""Candidate TEST -> CRITIC -> FREEZE lifecycle for bounded self-upgrade.

This module does not promote, push, merge, or mark VERIFIED. A successful lifecycle
produces a digest-bound local freeze receipt and transitions the live lease session to
FROZEN. Owner review remains mandatory.

Candidate tests can be run through Codex' Windows restricted-token sandbox with direct
network disabled. The built-in Codex critic is read-only and explicitly NOT an
independent critic because it uses the same provider family.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any, Protocol, Sequence

from .generation import enforce_candidate_mutation
from .self_upgrade_runtime import SelfUpgradeSession
from .critic.packet import build_critic_packet
from .critic.verdict_schema import (
    CRITIC_DEFECT_FOUND as EXTERNAL_DEFECT_FOUND,
    CRITIC_NO_MATERIAL_DEFECT_FOUND as EXTERNAL_NO_MATERIAL_DEFECT_FOUND,
)

LIFECYCLE_PROTOCOL = "minhtri-candidate-lifecycle/v1"
CRITIC_NO_MATERIAL_DEFECT = "NO_MATERIAL_DEFECT"
CRITIC_MATERIAL_DEFECT = "MATERIAL_DEFECT"
CRITIC_ABSTAIN = "ABSTAIN"


class CandidateLifecycleError(RuntimeError):
    pass


class CandidateTestRunner(Protocol):
    def run(self) -> dict[str, Any]:
        ...


class CandidateCritic(Protocol):
    def review(
        self,
        *,
        changed_paths: Sequence[str],
        artifact_digest: str,
        test_receipt: dict[str, Any],
    ) -> dict[str, Any]:
        ...


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def candidate_artifact_receipt(root: Path, changed_paths: Sequence[str]) -> dict[str, Any]:
    root = root.resolve()
    rows: list[dict[str, Any]] = []
    for raw in sorted(set(changed_paths)):
        rel = Path(raw)
        if rel.is_absolute() or ".." in rel.parts:
            raise CandidateLifecycleError("candidate path traversal is forbidden")
        path = (root / rel).resolve()
        try:
            path.relative_to(root)
        except ValueError as exc:
            raise CandidateLifecycleError("candidate path escapes worktree") from exc
        if path.is_dir():
            raise CandidateLifecycleError("candidate changed path must be a file")
        if path.exists():
            content_hash = _sha256_bytes(path.read_bytes())
            state = "PRESENT"
        else:
            content_hash = _sha256_bytes(b"DELETED")
            state = "DELETED"
        rows.append({"path": raw.replace("\\", "/"), "state": state, "sha256": content_hash})
    canonical = json.dumps(rows, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return {
        "files": rows,
        "artifact_digest": _sha256_bytes(canonical),
    }


@dataclass
class CodexSandboxTestRunner:
    candidate_root: Path
    command: tuple[str, ...] = ("python", "-m", "unittest", "discover", "-s", "tests")
    codex_executable: str = "codex.cmd"
    timeout_seconds: int = 900

    def run(self) -> dict[str, Any]:
        executable = shutil.which(self.codex_executable)
        if not executable:
            return {"status": "BLOCKED_CODEX_SANDBOX_NOT_FOUND"}
        command = list(self.command)
        if command and command[0].lower() in {"python", "python3", "python.exe"}:
            command[0] = sys.executable
        env = os.environ.copy()
        src_root = str((self.candidate_root / "src").resolve())
        existing_pythonpath = env.get("PYTHONPATH")
        env["PYTHONPATH"] = (
            src_root if not existing_pythonpath else src_root + os.pathsep + existing_pythonpath
        )
        proc = subprocess.run(
            [
                executable,
                "sandbox",
                "--permission-profile",
                ":workspace",
                "--sandbox-state-disable-network",
                "-C",
                str(self.candidate_root),
                *command,
            ],
            cwd=self.candidate_root,
            env=env,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=self.timeout_seconds,
            check=False,
        )
        return {
            "status": "PASS" if proc.returncode == 0 else "FAIL",
            "returncode": proc.returncode,
            "sandbox": "WINDOWS_RESTRICTED_TOKEN",
            "network_disabled": True,
            "command": command,
            "stdout_sha256": _sha256_bytes(proc.stdout.encode("utf-8", errors="replace")),
            "stderr_sha256": _sha256_bytes(proc.stderr.encode("utf-8", errors="replace")),
            "external_critic_log": (proc.stdout + "\n" + proc.stderr)[-50000:],
        }


@dataclass
class CodexReadOnlyCritic:
    candidate_root: Path
    codex_executable: str = "codex.cmd"
    model: str | None = None
    timeout_seconds: int = 600

    def review(
        self,
        *,
        changed_paths: Sequence[str],
        artifact_digest: str,
        test_receipt: dict[str, Any],
    ) -> dict[str, Any]:
        executable = shutil.which(self.codex_executable)
        if not executable:
            return {
                "verdict": CRITIC_ABSTAIN,
                "status": "BLOCKED_CODEX_CRITIC_NOT_FOUND",
                "independence_status": "SAME_PROVIDER_NOT_INDEPENDENT",
            }
        prompt = (
            "Review the current candidate worktree diff as a bounded critic. Do not edit files. "
            "Return ONLY JSON with keys verdict, findings, reason. verdict must be one of "
            "NO_MATERIAL_DEFECT, MATERIAL_DEFECT, ABSTAIN. Treat security boundary weakening, "
            "undeclared behavior change, failing tests, or unsupported claims as material defects. "
            "Changed paths: "
            + json.dumps(list(changed_paths), ensure_ascii=False)
            + "\nArtifact digest: "
            + artifact_digest
            + "\nTest receipt: "
            + json.dumps(test_receipt, ensure_ascii=False, sort_keys=True)
        )
        cmd = [
            executable,
            "exec",
            "--ephemeral",
            "--sandbox",
            "read-only",
            "--cd",
            str(self.candidate_root),
            "--color",
            "never",
        ]
        if self.model:
            cmd += ["--model", self.model]
        cmd.append(prompt)
        proc = subprocess.run(
            cmd,
            cwd=self.candidate_root,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=self.timeout_seconds,
            check=False,
        )
        if proc.returncode != 0:
            return {
                "verdict": CRITIC_ABSTAIN,
                "status": "BLOCKED_CODEX_CRITIC_EXEC_FAILED",
                "returncode": proc.returncode,
                "independence_status": "SAME_PROVIDER_NOT_INDEPENDENT",
            }
        try:
            parsed = json.loads(proc.stdout.strip())
        except json.JSONDecodeError:
            return {
                "verdict": CRITIC_ABSTAIN,
                "status": "BLOCKED_CODEX_CRITIC_NOT_JSON",
                "independence_status": "SAME_PROVIDER_NOT_INDEPENDENT",
            }
        verdict = parsed.get("verdict")
        if verdict not in {CRITIC_NO_MATERIAL_DEFECT, CRITIC_MATERIAL_DEFECT, CRITIC_ABSTAIN}:
            verdict = CRITIC_ABSTAIN
        return {
            "status": "RECORDED",
            "verdict": verdict,
            "findings": parsed.get("findings", []),
            "reason": parsed.get("reason", ""),
            "provider": "codex-cli",
            "model_requested": self.model,
            "context_mode": "READ_ONLY_CURRENT_WORKTREE",
            "independence_status": "SAME_PROVIDER_NOT_INDEPENDENT",
            "assurance_label": "AI_CONCUR" if verdict == CRITIC_NO_MATERIAL_DEFECT else "AI_FINDING",
            "proof_value": 0 if verdict == CRITIC_NO_MATERIAL_DEFECT else None,
            "owner_independent_review_required": True,
            "external_critic_independence_status": (
                external_receipt.get("independence_status") if external_receipt else "NOT_RUN"
            ),
            "stdout_sha256": _sha256_bytes(proc.stdout.encode("utf-8", errors="replace")),
        }


@dataclass
class CandidateLifecycleRunner:
    session: SelfUpgradeSession
    candidate_root: Path
    candidate_branch: str
    test_runner: CandidateTestRunner
    critic: CandidateCritic
    freeze_receipt_path: Path
    external_critic: Any | None = None
    external_claims: tuple[str, ...] = ()
    eval_packet_hash: str | None = None

    def _current_branch(self) -> str:
        proc = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=self.candidate_root,
            capture_output=True,
            text=True,
            timeout=30,
            check=True,
        )
        return proc.stdout.strip()

    def run(self, changed_paths: Sequence[str]) -> dict[str, Any]:
        self.session.check()
        if self._current_branch() != self.candidate_branch:
            raise CandidateLifecycleError("candidate worktree branch does not match declared branch")

        normalized = list(
            enforce_candidate_mutation(
                self.session.guard,
                candidate_branch=self.candidate_branch,
                changed_paths=changed_paths,
            )
        )
        before = candidate_artifact_receipt(self.candidate_root, normalized)

        test_receipt = self.test_runner.run()
        self.session.check()
        if test_receipt.get("status") != "PASS":
            return {
                "protocol": LIFECYCLE_PROTOCOL,
                "status": "REJECTED_TEST",
                "changed_paths": normalized,
                "artifact_digest": before["artifact_digest"],
                "test": test_receipt,
                "eligible_for_freeze": False,
                "automatic_promotion": False,
            }

        after_test = candidate_artifact_receipt(self.candidate_root, normalized)
        if after_test["artifact_digest"] != before["artifact_digest"]:
            return {
                "protocol": LIFECYCLE_PROTOCOL,
                "status": "BLOCKED_TEST_MUTATED_CANDIDATE",
                "changed_paths": normalized,
                "artifact_digest_before": before["artifact_digest"],
                "artifact_digest_after": after_test["artifact_digest"],
                "test": test_receipt,
                "eligible_for_freeze": False,
                "automatic_promotion": False,
            }

        critic_receipt = self.critic.review(
            changed_paths=normalized,
            artifact_digest=before["artifact_digest"],
            test_receipt=test_receipt,
        )
        self.session.check()
        after_critic = candidate_artifact_receipt(self.candidate_root, normalized)
        if after_critic["artifact_digest"] != before["artifact_digest"]:
            return {
                "protocol": LIFECYCLE_PROTOCOL,
                "status": "BLOCKED_CRITIC_MUTATED_CANDIDATE",
                "changed_paths": normalized,
                "artifact_digest_before": before["artifact_digest"],
                "artifact_digest_after": after_critic["artifact_digest"],
                "critic": critic_receipt,
                "eligible_for_freeze": False,
                "automatic_promotion": False,
            }

        if critic_receipt.get("verdict") != CRITIC_NO_MATERIAL_DEFECT:
            return {
                "protocol": LIFECYCLE_PROTOCOL,
                "status": "REJECTED_CRITIC",
                "changed_paths": normalized,
                "artifact_digest": before["artifact_digest"],
                "test": test_receipt,
                "critic": critic_receipt,
                "eligible_for_freeze": False,
                "automatic_promotion": False,
            }

        external_receipt = None
        external_packet = None
        if self.external_critic is not None:
            if not self.external_claims:
                raise CandidateLifecycleError("external critic requires explicit one-line claims")
            if not isinstance(self.eval_packet_hash, str):
                raise CandidateLifecycleError("external critic requires pinned eval_packet_hash")
            external_packet = build_critic_packet(
                candidate_root=self.candidate_root,
                candidate_generation_id=self.session.lease.target_generation,
                lease_id=self.session.lease.lease_id,
                changed_paths=normalized,
                test_log=str(test_receipt.get("external_critic_log", "")),
                claims=self.external_claims,
                eval_packet_hash=self.eval_packet_hash,
            )
            external_receipt = self.external_critic.critique(external_packet)
            self.session.check()
            after_external = candidate_artifact_receipt(self.candidate_root, normalized)
            if after_external["artifact_digest"] != before["artifact_digest"]:
                return {
                    "protocol": LIFECYCLE_PROTOCOL,
                    "status": "BLOCKED_EXTERNAL_CRITIC_MUTATED_CANDIDATE",
                    "changed_paths": normalized,
                    "artifact_digest_before": before["artifact_digest"],
                    "artifact_digest_after": after_external["artifact_digest"],
                    "external_critic": external_receipt,
                    "eligible_for_freeze": False,
                    "automatic_promotion": False,
                }
            if external_receipt.get("status") == "PENDING_EXTERNAL_CRITIC":
                return {
                    "protocol": LIFECYCLE_PROTOCOL,
                    "status": "PENDING_EXTERNAL_CRITIC",
                    "changed_paths": normalized,
                    "artifact_digest": before["artifact_digest"],
                    "test": test_receipt,
                    "critic_internal": critic_receipt,
                    "external_critic": external_receipt,
                    "external_packet_hash": external_packet["packet_hash"],
                    "eligible_for_freeze": False,
                    "automatic_promotion": False,
                }
            if external_receipt.get("status") in {"CRITIC_RUN_INVALID", "POST_EXPIRY"}:
                return {
                    "protocol": LIFECYCLE_PROTOCOL,
                    "status": "BLOCKED_EXTERNAL_CRITIC_INVALID_OR_LATE",
                    "changed_paths": normalized,
                    "artifact_digest": before["artifact_digest"],
                    "test": test_receipt,
                    "critic_internal": critic_receipt,
                    "external_critic": external_receipt,
                    "eligible_for_freeze": False,
                    "automatic_promotion": False,
                }
            if external_receipt.get("verdict") == EXTERNAL_DEFECT_FOUND:
                severities = {
                    finding.get("severity")
                    for finding in external_receipt.get("findings", [])
                    if isinstance(finding, dict)
                }
                material = bool(severities & {"MEDIUM", "HIGH", "CRITICAL"})
                return {
                    "protocol": LIFECYCLE_PROTOCOL,
                    "status": "REJECTED_EXTERNAL_CRITIC" if material else "CONTESTED_EXTERNAL_CRITIC",
                    "changed_paths": normalized,
                    "artifact_digest": before["artifact_digest"],
                    "test": test_receipt,
                    "critic_internal": critic_receipt,
                    "external_critic": external_receipt,
                    "eligible_for_freeze": False,
                    "automatic_promotion": False,
                    "owner_decision_required": True,
                }
            if external_receipt.get("verdict") != EXTERNAL_NO_MATERIAL_DEFECT_FOUND:
                return {
                    "protocol": LIFECYCLE_PROTOCOL,
                    "status": "BLOCKED_EXTERNAL_CRITIC_UNKNOWN_VERDICT",
                    "external_critic": external_receipt,
                    "eligible_for_freeze": False,
                    "automatic_promotion": False,
                }

        receipt = {
            "protocol": LIFECYCLE_PROTOCOL,
            "status": "FROZEN_PENDING_OWNER",
            "lease_id": self.session.lease.lease_id,
            "parent_generation": self.session.lease.parent_generation,
            "target_generation": self.session.lease.target_generation,
            "candidate_branch": self.candidate_branch,
            "changed_paths": normalized,
            "artifact": before,
            "test": test_receipt,
            "critic": critic_receipt,
            "external_critic": external_receipt,
            "external_packet_hash": external_packet["packet_hash"] if external_packet else None,
            "critic_independence_proven": False,
            "critic_assurance_label": critic_receipt.get("assurance_label", "AI_CONCUR"),
            "critic_proof_value": critic_receipt.get("proof_value", 0),
            "owner_independent_review_required": True,
            "automatic_verified_promotion": False,
            "automatic_candidate_promotion": False,
            "canonical_write_capability": False,
        }
        self.session.guarded_mutation(lambda: _atomic_json(self.freeze_receipt_path, receipt))
        self.session.guard.freeze("candidate lifecycle frozen pending Owner review")
        return {
            **receipt,
            "runtime_status": self.session.guard.status,
            "freeze_receipt_path": str(self.freeze_receipt_path),
        }
