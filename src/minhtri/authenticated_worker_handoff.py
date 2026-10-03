"""Authenticated parent-enforcer to worker handoff.

The authoritative UpgradeLease never leaves the parent process. A worker receives only a
one-time local IPC credential over stdin, then submits a bounded job request. The parent
re-checks the live lease, candidate branch, and declared paths before invoking a
parent-owned handler. The worker cannot renew, widen scope, or reconstruct the lease.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import json
from multiprocessing.connection import Client, Listener
from pathlib import Path
import secrets
import subprocess
import sys
from typing import Any, Callable

from .generation import enforce_candidate_mutation
from .self_upgrade_runtime import SelfUpgradeSession

HANDOFF_PROTOCOL = "minhtri-worker-handoff/v1"
OP_RUN_CANDIDATE_JOB = "RUN_CANDIDATE_JOB"


class WorkerHandoffError(RuntimeError):
    pass


@dataclass
class AuthenticatedWorkerHandoffServer:
    session: SelfUpgradeSession
    candidate_branch: str
    handler: Callable[[dict[str, Any]], dict[str, Any]]
    authkey: bytes = field(default_factory=lambda: secrets.token_bytes(32))
    listener: Listener | None = None

    def open(self) -> dict[str, Any]:
        self.session.check()
        if self.listener is not None:
            raise WorkerHandoffError("handoff listener already open")
        self.listener = Listener(("127.0.0.1", 0), family="AF_INET", authkey=self.authkey)
        host, port = self.listener.address
        return {
            "protocol": HANDOFF_PROTOCOL,
            "transport": "LOOPBACK_AUTHENTICATED_IPC",
            "host": host,
            "port": port,
            "lease_id": self.session.lease.lease_id,
            "expires_at_utc": self.session.lease.expires_at_utc,
            "candidate_branch": self.candidate_branch,
            "worker_holds_lease": False,
            "automatic_renewal": False,
        }

    def bootstrap_payload(self) -> dict[str, Any]:
        if self.listener is None:
            raise WorkerHandoffError("handoff listener is not open")
        host, port = self.listener.address
        return {
            "protocol": HANDOFF_PROTOCOL,
            "host": host,
            "port": port,
            "authkey_hex": self.authkey.hex(),
            "lease_id": self.session.lease.lease_id,
            "candidate_branch": self.candidate_branch,
        }

    def serve_one(self) -> dict[str, Any]:
        if self.listener is None:
            raise WorkerHandoffError("handoff listener is not open")
        conn = self.listener.accept()
        try:
            request = conn.recv()
            response = self._handle(request)
            conn.send(response)
            return response
        finally:
            conn.close()
            self.close()

    def _handle(self, request: Any) -> dict[str, Any]:
        self.session.check()
        if not isinstance(request, dict):
            raise WorkerHandoffError("worker request must be an object")
        if request.get("protocol") != HANDOFF_PROTOCOL:
            raise WorkerHandoffError("worker protocol mismatch")
        if request.get("operation") != OP_RUN_CANDIDATE_JOB:
            raise WorkerHandoffError("worker operation is not allowed")
        if request.get("lease_id") != self.session.lease.lease_id:
            raise WorkerHandoffError("worker lease_id mismatch")
        if request.get("candidate_branch") != self.candidate_branch:
            raise WorkerHandoffError("worker candidate branch mismatch")
        nonce = request.get("nonce")
        if not isinstance(nonce, str) or len(nonce) < 16:
            raise WorkerHandoffError("worker nonce is required")
        changed_paths = request.get("changed_paths")
        if not isinstance(changed_paths, list) or not changed_paths:
            raise WorkerHandoffError("worker changed_paths are required")
        normalized = list(
            enforce_candidate_mutation(
                self.session.guard,
                candidate_branch=self.candidate_branch,
                changed_paths=changed_paths,
            )
        )
        parent_request = {
            "protocol": HANDOFF_PROTOCOL,
            "operation": OP_RUN_CANDIDATE_JOB,
            "lease_id": self.session.lease.lease_id,
            "candidate_branch": self.candidate_branch,
            "nonce": nonce,
            "changed_paths": normalized,
            "objective": request.get("objective", ""),
        }
        result = self.handler(parent_request)
        if not isinstance(result, dict):
            raise WorkerHandoffError("parent handler must return an object")
        return {
            "protocol": HANDOFF_PROTOCOL,
            "status": "HANDOFF_JOB_COMPLETED",
            "lease_id": self.session.lease.lease_id,
            "nonce": nonce,
            "worker_holds_lease": False,
            "parent_enforced": True,
            "result": result,
        }

    def close(self) -> None:
        if self.listener is not None:
            self.listener.close()
            self.listener = None
        self.authkey = b""


def worker_request_from_bootstrap(
    bootstrap: dict[str, Any],
    *,
    changed_paths: list[str],
    objective: str,
    nonce: str | None = None,
) -> dict[str, Any]:
    if bootstrap.get("protocol") != HANDOFF_PROTOCOL:
        raise WorkerHandoffError("bootstrap protocol mismatch")
    auth_hex = bootstrap.get("authkey_hex")
    if not isinstance(auth_hex, str):
        raise WorkerHandoffError("bootstrap authkey missing")
    authkey = bytes.fromhex(auth_hex)
    request = {
        "protocol": HANDOFF_PROTOCOL,
        "operation": OP_RUN_CANDIDATE_JOB,
        "lease_id": bootstrap["lease_id"],
        "candidate_branch": bootstrap["candidate_branch"],
        "nonce": nonce or secrets.token_hex(16),
        "changed_paths": changed_paths,
        "objective": objective,
    }
    conn = Client(
        (bootstrap["host"], int(bootstrap["port"])),
        family="AF_INET",
        authkey=authkey,
    )
    try:
        conn.send(request)
        response = conn.recv()
    finally:
        conn.close()
        authkey = b""
    if not isinstance(response, dict) or response.get("nonce") != request["nonce"]:
        raise WorkerHandoffError("handoff response binding failed")
    return response


def launch_worker_with_stdin_bootstrap(
    *,
    worker_argv: list[str],
    bootstrap: dict[str, Any],
    cwd: Path,
) -> subprocess.Popen[str]:
    """Launch a worker without putting the one-time IPC credential in argv or env."""
    proc = subprocess.Popen(
        worker_argv,
        cwd=cwd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=False,
    )
    assert proc.stdin is not None
    proc.stdin.write(json.dumps(bootstrap, ensure_ascii=False) + "\n")
    proc.stdin.flush()
    proc.stdin.close()
    return proc
