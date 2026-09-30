import json
import tempfile
import unittest
from pathlib import Path

from minhtri.core import Ledger, current_focus

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


class Examples(unittest.TestCase):
    def test_all_examples_apply_in_order_and_verify(self):
        files = sorted(EXAMPLES.glob("*.json"))
        self.assertGreaterEqual(len(files), 7)
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Ledger(Path(tmp) / "brain")
            ledger.init()
            for path in files:
                ledger.apply(json.loads(path.read_text(encoding="utf-8")))
            state, count, _ = ledger.verify()
            self.assertEqual(count, len(files))
            focus = current_focus(state)
            self.assertEqual(state["sources"][focus["source_id"]]["kind"], "THIRD_PARTY")
            self.assertEqual(state["sources"][focus["source_id"]]["rights_status"], "UNKNOWN")
            self.assertEqual(focus["id"], "gia-dinh-suno-studio-mot-bai-tap-third-party")
            self.assertEqual(focus["expectation_status"], "UNTESTED_EXPECTATION")
            previous = state["learning_focuses"]["gia-dinh-tong-hop-2026-yt-mv-ai-third-party"]
            self.assertEqual((previous["status"], previous["superseded_by"]), ("SUPERSEDED", focus["id"]))


if __name__ == "__main__":
    unittest.main()
