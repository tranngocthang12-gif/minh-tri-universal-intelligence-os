import json
import tempfile
import unittest
from pathlib import Path

from minhtri.core import Ledger, current_focus
from tests.support import ledger_apply, ledger_repair, write_owner_config

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


class Examples(unittest.TestCase):
    def test_all_examples_apply_in_order_and_verify(self):
        files = sorted(EXAMPLES.glob("*.json"))
        self.assertGreaterEqual(len(files), 8)
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Ledger(Path(tmp) / "brain")
            config = write_owner_config(tmp)
            ledger.init()
            for path in files:
                ledger_apply(ledger, json.loads(path.read_text(encoding="utf-8")), config)
            state, count, _ = ledger.verify()
            self.assertEqual(count, len(files))
            focus = current_focus(state)
            self.assertEqual(state["sources"][focus["source_id"]]["kind"], "THIRD_PARTY")
            self.assertEqual(state["sources"][focus["source_id"]]["rights_status"], "UNKNOWN")
            self.assertEqual(focus["expectation_status"], "UNTESTED_EXPECTATION")
            # Focus examples in file order: the last one is ACTIVE, each earlier one was
            # superseded by the next. No example ID is hard-coded here.
            focus_ids = [json.loads(p.read_text(encoding="utf-8"))["data"]["id"] for p in files
                         if json.loads(p.read_text(encoding="utf-8"))["type"] == "set_learning_focus"]
            self.assertGreaterEqual(len(focus_ids), 3)
            self.assertEqual(focus["id"], focus_ids[-1])
            for earlier, later in zip(focus_ids, focus_ids[1:]):
                record = state["learning_focuses"][earlier]
                self.assertEqual((record["status"], record["superseded_by"]), ("SUPERSEDED", later))


if __name__ == "__main__":
    unittest.main()
