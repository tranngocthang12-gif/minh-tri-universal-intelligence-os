import contextlib
import hashlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from minhtri.cli import main
from minhtri.core import GateError, Ledger
from minhtri.owner import config_path

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


class SecurityP0(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = str(Path(self.tmp.name) / "brain")
        self.ledger = Ledger(self.home)
        self.ledger.init()

    def tearDown(self):
        self.tmp.cleanup()

    def test_owner_config_override_fails_closed(self):
        with self.assertRaisesRegex(GateError, "OWNER_CONFIG_OVERRIDE_BLOCKED"):
            config_path(str(Path(self.tmp.name) / "attacker.json"))
        with mock.patch.dict(os.environ, {"MINHTRI_OWNER_CONFIG": str(Path(self.tmp.name) / "attacker.json")}):
            self.assertEqual(config_path(None).name, "owner.json")
            self.assertEqual(config_path(None).parent.name, "config")

    def test_direct_python_write_without_authenticated_boundary_is_blocked(self):
        command = {"type": "register_domain", "data": {
            "id": "alpha", "name": "Alpha", "risk_class": "NORMAL", "measurement_contract": "Log"}}
        with self.assertRaisesRegex(GateError, "Authenticated write boundary"):
            self.ledger.apply(command)
        with self.assertRaisesRegex(GateError, "Authenticated write boundary"):
            self.ledger.apply(command, approved_by="test-owner")
        self.assertEqual(self.ledger.verify()[1], 0)

    def test_direct_snapshot_repair_without_authenticated_boundary_is_blocked(self):
        self.ledger.snapshot.write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(GateError, "Authenticated write boundary"):
            self.ledger.repair_snapshot()
        with self.assertRaisesRegex(GateError, "Authenticated write boundary"):
            self.ledger.repair_snapshot(approved_by="test-owner")

    def test_cli_no_longer_accepts_owner_config_selector(self):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            with self.assertRaises(SystemExit) as raised:
                main(["--owner-config", str(Path(self.tmp.name) / "attacker.json"), "status"])
        self.assertEqual(raised.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
