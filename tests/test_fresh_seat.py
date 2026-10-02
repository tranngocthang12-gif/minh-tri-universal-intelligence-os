import unittest

from minhtri.fresh_seat import (
    FreshSeatValidationError,
    validate_fresh_seat_evidence,
)


def record():
    read = {
        "status": "VALID",
        "event_count": 3,
        "head": "a" * 64,
    }
    return {
        "schema": "minhtri-fresh-seat-validation/v1",
        "separate_chat_ui": True,
        "prompt_seeded_expected_values": False,
        "toolset": ["brain.verify", "brain.recovery_packet"],
        "mutation_tool_exposed": False,
        "fresh_verify": dict(read),
        "fresh_recovery": {**read, "focus": {"status": "ACTIVE"}},
        "control_verify": dict(read),
    }


class FreshSeatValidationTests(unittest.TestCase):
    def test_valid_record_passes(self):
        result = validate_fresh_seat_evidence(record())
        self.assertEqual(result["status"], "PASS")
        self.assertFalse(result["write_capability"])

    def test_seeded_prompt_is_rejected(self):
        value = record()
        value["prompt_seeded_expected_values"] = True
        with self.assertRaises(FreshSeatValidationError):
            validate_fresh_seat_evidence(value)

    def test_extra_tool_is_rejected(self):
        value = record()
        value["toolset"].append("ledger.apply")
        with self.assertRaises(FreshSeatValidationError):
            validate_fresh_seat_evidence(value)

    def test_mismatched_control_head_is_rejected(self):
        value = record()
        value["control_verify"]["head"] = "b" * 64
        with self.assertRaises(FreshSeatValidationError):
            validate_fresh_seat_evidence(value)

    def test_same_chat_attestation_is_rejected(self):
        value = record()
        value["separate_chat_ui"] = False
        with self.assertRaises(FreshSeatValidationError):
            validate_fresh_seat_evidence(value)

    def test_mutation_exposure_is_rejected(self):
        value = record()
        value["mutation_tool_exposed"] = True
        with self.assertRaises(FreshSeatValidationError):
            validate_fresh_seat_evidence(value)


if __name__ == "__main__":
    unittest.main()
