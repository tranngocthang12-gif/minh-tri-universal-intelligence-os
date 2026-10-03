import json
import tempfile
import threading
import unittest
from datetime import datetime, timezone
from pathlib import Path

from minhtri.authenticated_worker_handoff import (
    AuthenticatedWorkerHandoffServer,
    HANDOFF_PROTOCOL,
    OP_RUN_CANDIDATE_JOB,
    WorkerHandoffError,
    worker_request_from_bootstrap,
)
from minhtri.generation import CandidateSandboxError
from minhtri.self_upgrade_runtime import SelfUpgradeSession
from minhtri.upgrade_lease import issue_upgrade_lease
from tests.support import TEST_OWNER, TEST_SECRET, owner_config, write_owner_config


class AuthenticatedWorkerHandoffTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.config = write_owner_config(Path(self.tmp.name))
        with owner_config(self.config):
            lease = issue_upgrade_lease(
                actor=TEST_OWNER,
                secret=TEST_SECRET,
                duration_seconds=300,
                parent_generation="GEN-1",
                target_generation="GEN-2",
                now=datetime.now(timezone.utc),
                lease_id="upgrade-handoff-test",
            )
        self.session = SelfUpgradeSession(lease)

    def test_authenticated_worker_gets_parent_enforced_result_without_lease_object(self):
        seen = {}
        def handler(request):
            seen.update(request)
            return {"status": "CANDIDATE_JOB_ACCEPTED"}

        server = AuthenticatedWorkerHandoffServer(
            self.session, "candidate/GEN-2", handler
        )
        bootstrap = server.open()
        secret_bootstrap = server.bootstrap_payload()
        self.assertFalse(bootstrap["worker_holds_lease"])
        self.assertNotIn("authkey_hex", bootstrap)

        out = {}
        thread = threading.Thread(target=lambda: out.setdefault("server", server.serve_one()))
        thread.start()
        response = worker_request_from_bootstrap(
            secret_bootstrap,
            changed_paths=["src/minhtri/__init__.py"],
            objective="bounded candidate",
            nonce="0123456789abcdef",
        )
        thread.join(timeout=3)
        self.assertEqual(response["status"], "HANDOFF_JOB_COMPLETED")
        self.assertTrue(response["parent_enforced"])
        self.assertFalse(response["worker_holds_lease"])
        self.assertEqual(seen["lease_id"], "upgrade-handoff-test")
        self.assertEqual(seen["changed_paths"], ["src/minhtri/__init__.py"])

    def test_wrong_lease_or_operation_fails_closed(self):
        server = AuthenticatedWorkerHandoffServer(
            self.session, "candidate/GEN-2", lambda request: {"status": "NOOP"}
        )
        server.open()
        with self.assertRaises(WorkerHandoffError):
            server._handle({
                "protocol": HANDOFF_PROTOCOL,
                "operation": OP_RUN_CANDIDATE_JOB,
                "lease_id": "wrong",
                "candidate_branch": "candidate/GEN-2",
                "nonce": "0123456789abcdef",
                "changed_paths": ["src/minhtri/__init__.py"],
            })
        server.close()

    def test_protected_path_is_denied_before_parent_handler(self):
        called = []
        server = AuthenticatedWorkerHandoffServer(
            self.session,
            "candidate/GEN-2",
            lambda request: called.append(request) or {"status": "BAD"},
        )
        server.open()
        with self.assertRaises(CandidateSandboxError):
            server._handle({
                "protocol": HANDOFF_PROTOCOL,
                "operation": OP_RUN_CANDIDATE_JOB,
                "lease_id": "upgrade-handoff-test",
                "candidate_branch": "candidate/GEN-2",
                "nonce": "0123456789abcdef",
                "changed_paths": ["src/minhtri/upgrade_lease.py"],
            })
        self.assertEqual(called, [])
        server.close()


if __name__ == "__main__":
    unittest.main()
