import json
import tempfile
import unittest
import urllib.error
import urllib.request
from pathlib import Path

from minhtri.brain_http import BrainHTTPClient, BrainHTTPError, BrainHTTPHost
from minhtri.core import Ledger
from tests.support import ledger_apply, write_owner_config

TOKEN = "t" * 40


class BrainHTTPE2E(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.home = self.root / "brain"
        self.config = write_owner_config(self.root)
        self.ledger = Ledger(self.home)
        self.ledger.init()
        ledger_apply(self.ledger, {
            "type": "register_domain",
            "data": {"id": "youtube", "name": "YouTube", "risk_class": "NORMAL", "measurement_contract": "views"},
        }, self.config)
        ledger_apply(self.ledger, {
            "type": "record_source",
            "data": {
                "id": "src1", "domain_id": "youtube", "uri": "owner://focus",
                "captured_at": "2026-10-01T00:00:00Z", "kind": "FIRST_PARTY", "rights_status": "CLEAR",
            },
        }, self.config)
        ledger_apply(self.ledger, {
            "type": "set_learning_focus",
            "data": {
                "id": "focus1", "status": "ACTIVE", "domain_id": "youtube", "source_id": "src1",
                "note": "chat quên, sổ không", "expected_lesson": "recover continuity", "uncertainty": "UNTESTED",
            },
        }, self.config)

    def tearDown(self):
        self.tmp.cleanup()

    def test_fresh_client_recovers_verified_focus_over_authenticated_loopback(self):
        with BrainHTTPHost(self.home, TOKEN) as host:
            result = BrainHTTPClient(host.url, TOKEN).call("brain.recovery_packet")
        self.assertEqual(result["status"], "VALID")
        self.assertEqual(result["focus"]["id"], "focus1")
        self.assertEqual(result["focus"]["note"], "chat quên, sổ không")
        self.assertEqual(result["event_count"], 3)
        self.assertEqual(len(result["head"]), 64)

    def test_wrong_token_is_rejected(self):
        with BrainHTTPHost(self.home, TOKEN) as host:
            with self.assertRaises(BrainHTTPError):
                BrainHTTPClient(host.url, "x" * 40).call("brain.verify")

    def test_remote_path_and_mutation_are_rejected_end_to_end(self):
        with BrainHTTPHost(self.home, TOKEN) as host:
            client = BrainHTTPClient(host.url, TOKEN)
            with self.assertRaises(BrainHTTPError):
                client.call("brain.recovery_packet", {"home": "/attacker"})
            with self.assertRaises(BrainHTTPError):
                client.call("ledger.apply", {})

    def test_tampered_snapshot_fails_closed_over_transport(self):
        self.ledger.snapshot.write_text("{}", encoding="utf-8")
        with BrainHTTPHost(self.home, TOKEN) as host:
            with self.assertRaises(BrainHTTPError):
                BrainHTTPClient(host.url, TOKEN).call("brain.verify")

    def test_non_loopback_bind_is_rejected(self):
        with self.assertRaises(BrainHTTPError):
            BrainHTTPHost(self.home, TOKEN, host="0.0.0.0")


if __name__ == "__main__":
    unittest.main()
