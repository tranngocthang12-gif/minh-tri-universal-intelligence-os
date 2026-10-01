import json
import tempfile
import unittest
from pathlib import Path

from minhtri.anchor import make_anchor, verify_anchor_chain, verify_historical_anchor
from minhtri.core import canonical, digest


class AnchorPrefixTime(unittest.TestCase):
    def _ledger(self, count=3):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "events.jsonl"
        prev = "0" * 64
        heads = []
        rows = []
        for seq in range(1, count + 1):
            body = {
                "seq": seq,
                "prev": prev,
                "at": f"2026-01-0{seq}T00:00:00Z",
                "command": {"type": "register_domain", "data": {
                    "id": f"d{seq}", "name": f"D{seq}", "risk_class": "NORMAL",
                    "measurement_contract": "m"}},
            }
            event = {**body, "hash": digest(body)}
            rows.append(canonical(event).decode())
            prev = event["hash"]
            heads.append(prev)
        path.write_text("\n".join(rows) + "\n", encoding="utf-8")
        return path, heads

    def test_historical_anchor_matches_prefix_of_advanced_ledger(self):
        path, heads = self._ledger()
        anchor = make_anchor(2, heads[1], "2026-02-01T00:00:00Z")
        result = verify_historical_anchor(path, anchor)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["reason"], "HISTORICAL_PREFIX_MATCH")

    def test_historical_anchor_wrong_prefix_fails(self):
        path, _ = self._ledger()
        anchor = make_anchor(2, "f" * 64, "2026-02-01T00:00:00Z")
        self.assertEqual(verify_historical_anchor(path, anchor)["reason"], "LEDGER_HEAD_MISMATCH")

    def test_tampered_ledger_prefix_fails_closed(self):
        path, heads = self._ledger()
        rows = path.read_text().splitlines()
        event = json.loads(rows[0])
        event["prev"] = "f" * 64
        rows[0] = json.dumps(event)
        path.write_text("\n".join(rows) + "\n")
        anchor = make_anchor(2, heads[1], "2026-02-01T00:00:00Z")
        self.assertEqual(verify_historical_anchor(path, anchor)["reason"], "HISTORICAL_PREFIX_UNVERIFIABLE")

    def test_make_anchor_rejects_non_utc_z_timestamp(self):
        with self.assertRaises(ValueError):
            make_anchor(1, "a" * 64, "2026-10-01T01:00:00+01:00")

    def test_chain_requires_strictly_increasing_time(self):
        a1 = make_anchor(1, "a" * 64, "2026-10-01T01:00:00Z")
        a2 = make_anchor(2, "b" * 64, "2026-10-01T01:00:00Z", a1["anchor_id"])
        self.assertEqual(verify_anchor_chain([a1, a2])["reason"], "ANCHOR_TIME_NOT_INCREASING")


if __name__ == "__main__":
    unittest.main()
