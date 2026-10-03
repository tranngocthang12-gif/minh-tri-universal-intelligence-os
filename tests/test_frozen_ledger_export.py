import json
import tempfile
import unittest
from pathlib import Path

from minhtri.frozen_ledger_export import (
    FrozenLedgerExportError,
    export_verified_ledger_snapshot,
)
from minhtri.core import Ledger


FLAGS = {
    "autonomous_learning_runtime": False,
    "automatic_self_critique_runtime": False,
    "meta_learning_runtime": False,
}


class FrozenLedgerExportTests(unittest.TestCase):
    def test_export_does_not_start_runtime_or_mutate_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ledger = Ledger(root / "brain")
            ledger.init()
            before_events = ledger.events.read_bytes()
            manifest = export_verified_ledger_snapshot(
                ledger.home,
                root / "export",
                runtime_flags=FLAGS,
            )
            self.assertFalse(manifest["brain_service_started"])
            self.assertFalse(manifest["autonomy_runtime_started"])
            self.assertFalse(manifest["source_mutated"])
            self.assertEqual(ledger.events.read_bytes(), before_events)
            saved = json.loads((root / "export" / "manifest.json").read_text())
            self.assertEqual(saved["ledger_head"], manifest["ledger_head"])

    def test_export_refuses_if_learning_runtime_flag_is_true(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ledger = Ledger(root / "brain")
            ledger.init()
            flags = dict(FLAGS)
            flags["meta_learning_runtime"] = True
            with self.assertRaises(FrozenLedgerExportError):
                export_verified_ledger_snapshot(
                    ledger.home,
                    root / "export",
                    runtime_flags=flags,
                )


if __name__ == "__main__":
    unittest.main()
