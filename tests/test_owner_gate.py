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
from minhtri.core import Ledger

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


class OwnerGate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.home = str(root / "brain")
        self.config = root / "owner.json"
        self.config.write_text(json.dumps({
            "owner_id": "test-owner",
            "owner_secret_sha256": hashlib.sha256(b"test-secret").hexdigest(),
        }), encoding="utf-8")
        self.config_patch = mock.patch("minhtri.owner.config_path", return_value=self.config)
        self.config_patch.start()
        self.addCleanup(self.config_patch.stop)
        env = mock.patch.dict(os.environ)
        env.start()
        self.addCleanup(env.stop)
        os.environ.pop("MINHTRI_OWNER_SECRET", None)
        self.cli("init")

    def tearDown(self):
        self.tmp.cleanup()

    def cli(self, *argv, owner=None, secret="test-secret", expect=0):
        prefix = ["--home", self.home]
        if owner is not None:
            prefix += ["--owner-id", owner]
        if secret is not None:
            prefix += ["--owner-secret", secret]
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main([*prefix, *argv])
        self.assertEqual(code, expect, err.getvalue() + out.getvalue())
        return json.loads(out.getvalue() or err.getvalue())

    def events(self):
        return Ledger(self.home).verify()[1]

    def test_every_apply_is_owner_gated(self):
        before = self.events()
        path = EXAMPLES / "01-domain-youtube.json"
        self.assertEqual(self.cli("apply", str(path), owner=None, secret=None, expect=2)["reason"], "OWNER_ID_REQUIRED")
        self.assertEqual(self.cli("apply", str(path), owner="intruder", expect=2)["reason"], "OWNER_MISMATCH")
        self.assertEqual(self.cli("apply", str(path), owner="test-owner", secret="wrong", expect=2)["reason"], "OWNER_SECRET_MISMATCH")
        self.assertEqual(self.events(), before)
        self.assertEqual(self.cli("apply", str(path), owner="test-owner")["status"], "APPLIED")
        self.assertEqual(self.events(), before + 1)

    def test_learn_unfocus_and_repair_are_gated(self):
        self.cli("apply", str(EXAMPLES / "01-domain-youtube.json"), owner="test-owner")
        learn = ("learn", "--domain-id", "youtube", "--uri", "https://example.invalid/x", "--note", "why")
        self.assertEqual(self.cli(*learn, owner=None, secret=None, expect=2)["reason"], "OWNER_ID_REQUIRED")
        self.assertEqual(self.cli(*learn, owner="test-owner")["status"], "FOCUS_SET")
        self.assertEqual(self.cli("unfocus", owner="test-owner")["status"], "FOCUS_STOPPED")
        ledger = Ledger(self.home)
        ledger.snapshot.write_text("{}", encoding="utf-8")
        self.assertEqual(self.cli("repair-snapshot", owner="test-owner", secret="wrong", expect=2)["reason"],
                         "OWNER_SECRET_MISMATCH")
        self.assertEqual(self.cli("repair-snapshot", owner="test-owner")["status"], "REPAIRED")

    def test_read_only_commands_need_no_secret(self):
        for action in ("focus", "status", "verify"):
            self.assertEqual(self.cli(action, owner=None, secret=None)["status"], "VALID")

    def test_secret_from_env(self):
        self.cli("apply", str(EXAMPLES / "01-domain-youtube.json"), owner="test-owner")
        os.environ["MINHTRI_OWNER_SECRET"] = "test-secret"
        result = self.cli("learn", "--domain-id", "youtube", "--uri", "https://example.invalid/x",
                          "--note", "why", owner="test-owner", secret=None)
        self.assertEqual(result["status"], "FOCUS_SET")

    def test_hash_secret_prints_only_hash(self):
        out = io.StringIO()
        with mock.patch("sys.stdin", io.StringIO("test-secret\n")), contextlib.redirect_stdout(out):
            self.assertEqual(main(["hash-secret"]), 0)
        printed = out.getvalue()
        self.assertEqual(json.loads(printed)["owner_secret_sha256"], hashlib.sha256(b"test-secret").hexdigest())
        self.assertNotIn("test-secret", printed)

    def test_mutating_events_record_owner_never_secret(self):
        self.cli("apply", str(EXAMPLES / "01-domain-youtube.json"), owner="test-owner")
        raw = Ledger(self.home).events.read_text(encoding="utf-8")
        events = [json.loads(line) for line in raw.splitlines()]
        self.assertTrue(events)
        self.assertTrue(all(e.get("approved_by") == "test-owner" for e in events))
        self.assertNotIn("test-secret", raw)
        self.assertNotIn(hashlib.sha256(b"test-secret").hexdigest(), raw)


if __name__ == "__main__":
    unittest.main()
