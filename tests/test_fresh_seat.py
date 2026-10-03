import unittest
from datetime import datetime, timezone

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
        "schema": "minhtri-fresh-seat-validation/v2",
        "separate_chat_ui": True,
        "prompt_seeded_expected_values": False,
        "toolset": ["brain.verify", "brain.recovery_packet"],
        "mutation_tool_exposed": False,
        "fresh_verify": dict(read),
        "fresh_recovery": {**read, "focus": {"status": "ACTIVE"}},
        "control_verify": dict(read),
        "observed_at_utc": "2026-10-04T02:00:00Z",
        "control_observed_at_utc": "2026-10-04T02:01:00Z",
        "ttl_seconds": 600,
    }


class FreshSeatValidationTests(unittest.TestCase):
    def test_valid_record_passes(self):
        result = validate_fresh_seat_evidence(
            record(), now=datetime(2026, 10, 4, 2, 2, tzinfo=timezone.utc)
        )
        self.assertEqual(result["status"], "PASS")
        self.assertFalse(result["write_capability"])
        self.assertEqual(result["expires_at_utc"], "2026-10-04T02:10:00Z")

    def test_seeded_prompt_is_rejected(self):
        value = record()
        value["prompt_seeded_expected_values"] = True
        with self.assertRaises(FreshSeatValidationError):
            validate_fresh_seat_evidence(
                value, now=datetime(2026, 10, 4, 2, 2, tzinfo=timezone.utc)
            )

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

    def test_expired_fresh_seat_record_is_rejected(self):
        value = record()
        with self.assertRaises(FreshSeatValidationError):
            validate_fresh_seat_evidence(
                value, now=datetime(2026, 10, 4, 2, 11, tzinfo=timezone.utc)
            )

    def test_control_observation_outside_window_is_rejected(self):
        value = record()
        value["control_observed_at_utc"] = "2026-10-04T02:06:00Z"
        with self.assertRaises(FreshSeatValidationError):
            validate_fresh_seat_evidence(
                value, now=datetime(2026, 10, 4, 2, 7, tzinfo=timezone.utc)
            )


if __name__ == "__main__":
    unittest.main()
