import unittest
from unittest.mock import patch

from minhtri.brain_transport import BrainTransport, BrainTransportError, PROTOCOL


class BrainTransportContract(unittest.TestCase):
    def setUp(self):
        self.transport = BrainTransport("/fixed/brain")

    @patch("minhtri.brain_transport.BrainReader.verify")
    def test_verify_has_no_remote_path(self, verify):
        verify.return_value = {"status": "VALID", "event_count": 1, "head": "a" * 64}
        out = self.transport.dispatch({"protocol": PROTOCOL, "method": "brain.verify", "params": {}})
        self.assertEqual(out["result"]["status"], "VALID")

    def test_path_redirection_is_rejected(self):
        with self.assertRaises(BrainTransportError):
            self.transport.dispatch({"protocol": PROTOCOL, "method": "brain.recovery_packet",
                                     "params": {"home": "/attacker"}})

    def test_mutation_method_is_rejected(self):
        with self.assertRaises(BrainTransportError):
            self.transport.dispatch({"protocol": PROTOCOL, "method": "ledger.apply", "params": {}})

    def test_unknown_protocol_is_rejected(self):
        with self.assertRaises(BrainTransportError):
            self.transport.dispatch({"protocol": "other", "method": "brain.verify", "params": {}})

    def test_query_size_is_bounded(self):
        with self.assertRaises(BrainTransportError):
            self.transport.dispatch({"protocol": PROTOCOL, "method": "brain.recovery_packet",
                                     "params": {"query": "x" * 4097}})


if __name__ == "__main__":
    unittest.main()
