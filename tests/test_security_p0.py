import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from minhtri.core import GateError, Ledger
from minhtri.owner import OwnerGateError, config_path

DOMAIN = {"type": "register_domain", "data": {
    "id": "alpha", "name": "Alpha", "risk_class": "NORMAL", "measurement_contract": "Log"}}


class SecurityP0(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name) / "brain"
        self.config = Path(self.tmp.name) / "owner.json"
        self.config.write_text(json.dumps({
            "owner_id": "test-owner",
            "owner_secret_sha256": hashlib.sha256(b"test-secret").hexdigest(),
        }), encoding="utf-8")
        self.ledger = Ledger(self.home)
        self.ledger.init()

    def tearDown(self):
        self.tmp.cleanup()

    def fixed_config(self):
        return mock.patch("minhtri.owner.config_path", return_value=self.config)

    def test_owner_config_override_fails_closed(self):
        with self.assertRaisesRegex(OwnerGateError, "OWNER_CONFIG_OVERRIDE_BLOCKED"):
            config_path(str(Path(self.tmp.name) / "attacker.json"))
        self.assertEqual(config_path(None).name, "owner.json")
        self.assertEqual(config_path(None).parent.name, "config")

    def test_direct_python_write_authenticates_inside_boundary(self):
        with self.fixed_config():
            for actor, secret in ((None, None), ("intruder", "test-secret"), ("test-owner", "wrong")):
                with self.assertRaises(GateError):
                    self.ledger.apply(DOMAIN, actor=actor, secret=secret)
            self.assertEqual(self.ledger.verify()[1], 0)
            result = self.ledger.apply(DOMAIN, actor="test-owner", secret="test-secret")
        self.assertEqual(result["event_count"], 1)
        self.assertEqual(self.ledger.verify()[1], 1)

    def test_snapshot_repair_authenticates_inside_boundary(self):
        self.ledger.snapshot.write_text("{}", encoding="utf-8")
        with self.fixed_config():
            with self.assertRaises(GateError):
                self.ledger.repair_snapshot(actor="test-owner", secret="wrong")
            count, _ = self.ledger.repair_snapshot(actor="test-owner", secret="test-secret")
        self.assertEqual(count, 0)
        self.assertEqual(self.ledger.verify()[1], 0)


if __name__ == "__main__":
    unittest.main()
