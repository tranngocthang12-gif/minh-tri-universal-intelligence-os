import json
import tempfile
import unittest
from pathlib import Path

from minhtri.core import GateError, Ledger, canonical, digest
from tests.support import TEST_OWNER, TEST_SECRET, ledger_apply, write_owner_config


def cmd(command_type, **data):
    return {"type": command_type, "data": data}


DOMAIN = cmd("register_domain", id="alpha", name="Alpha", risk_class="NORMAL", measurement_contract="Log")
SOURCE = cmd("record_source", id="s1", domain_id="alpha", uri="https://example.invalid/a",
             captured_at="2026-01-01T00:00:00Z", kind="THIRD_PARTY", rights_status="UNKNOWN")


class LedgerApprover(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ledger = Ledger(Path(self.tmp.name) / "brain")
        self.config = write_owner_config(self.tmp.name)
        self.ledger.init()

    def tearDown(self):
        self.tmp.cleanup()

    def lines(self):
        return [json.loads(line) for line in self.ledger.events.read_text(encoding="utf-8").splitlines()]

    def rewrite(self, events, rehash_from=None):
        """Write events back; optionally recompute hashes (a smarter forger) from an index on."""
        if rehash_from is not None:
            prev = events[rehash_from - 1]["hash"] if rehash_from else "0" * 64
            for event in events[rehash_from:]:
                event["prev"] = prev
                body = {k: v for k, v in event.items() if k != "hash"}
                event["hash"] = digest(body)
                prev = event["hash"]
        self.ledger.events.write_bytes(b"".join(canonical(e) + b"\n" for e in events))

    def test_approver_is_recorded_hashed_and_verifies(self):
        ledger_apply(self.ledger, DOMAIN, self.config)
        ledger_apply(self.ledger, SOURCE, self.config)
        events = self.lines()
        self.assertEqual(events[0]["approved_by"], TEST_OWNER)
        self.assertEqual(events[1]["approved_by"], TEST_OWNER)
        body = {k: v for k, v in events[1].items() if k != "hash"}
        self.assertEqual(digest(body), events[1]["hash"])
        self.assertEqual(self.ledger.verify()[1], 2)

    def test_old_ledger_without_field_still_verifies(self):
        # Historical ledgers may predate approved_by. Replay remains backward compatible.
        at = "2026-01-01T00:00:00Z"
        first_body = {"seq": 1, "prev": "0" * 64, "at": at, "command": DOMAIN}
        first = {**first_body, "hash": digest(first_body)}
        second_body = {"seq": 2, "prev": first["hash"], "at": at, "command": SOURCE}
        second = {**second_body, "hash": digest(second_body)}
        self.rewrite([first, second])
        state, count, head = self.ledger.replay()
        self.ledger._save(state, count, head)
        self.assertTrue(all("approved_by" not in e for e in self.lines()))
        self.assertEqual(self.ledger.verify()[1], 2)

    def test_editing_removing_or_adding_approver_breaks_the_chain(self):
        ledger_apply(self.ledger, DOMAIN, self.config)
        ledger_apply(self.ledger, SOURCE, self.config)
        original = self.lines()
        for mutate in (
            lambda ev: ev[1].__setitem__("approved_by", "intruder"),
            lambda ev: ev[1].pop("approved_by"),
            lambda ev: ev[0].__setitem__("approved_by", "intruder"),
            lambda ev: ev[1]["command"]["data"].__setitem__("uri", "https://example.invalid/forged"),
        ):
            events = json.loads(json.dumps(original))
            mutate(events)
            self.rewrite(events)
            with self.assertRaisesRegex(GateError, "chain mismatch"):
                self.ledger.verify()
        self.rewrite(original)
        self.assertEqual(self.ledger.verify()[1], 2)

    def test_rehashed_forgery_is_caught_by_snapshot_and_bad_values_rejected(self):
        ledger_apply(self.ledger, DOMAIN, self.config)
        ledger_apply(self.ledger, SOURCE, self.config)
        events = self.lines()
        events[1]["approved_by"] = "intruder"
        self.rewrite(events, rehash_from=1)
        # A full rehash defeats the chain alone; the cached head no longer matches.
        with self.assertRaisesRegex(GateError, "Snapshot differs"):
            self.ledger.verify()
        events[1]["approved_by"] = "Not An ID"
        self.rewrite(events, rehash_from=1)
        with self.assertRaisesRegex(GateError, "approved_by"):
            self.ledger.verify()
        with self.assertRaises(GateError):
            self.ledger.apply(SOURCE, actor="Bad ID", secret=TEST_SECRET)


if __name__ == "__main__":
    unittest.main()
