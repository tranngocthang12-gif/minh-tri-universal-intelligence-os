import json
import tempfile
import unittest
from pathlib import Path

from minhtri.critic.packet import CriticPacketError, build_critic_packet, verify_packet_hash
from minhtri.critic.provider_manual import ManualExternalCritic
from minhtri.critic.verdict_schema import CriticResult, CriticSchemaError


# Negative fixtures are assembled at runtime to avoid secret-like literals in history.
class ExternalCriticTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.artifact = self.root / "candidate.py"
        self.artifact.write_text("claim = 'bounded'\n", encoding="utf-8")

    def packet(self, *, test_log="PASS", claims=("bounded claim",)):
        return build_critic_packet(
            candidate_root=self.root,
            candidate_generation_id="GEN-0002",
            lease_id="upgrade-test",
            changed_paths=["candidate.py"],
            test_log=test_log,
            claims=claims,
            eval_packet_hash="a" * 64,
        )

    def test_packet_is_hash_bound_and_blind(self):
        packet = self.packet()
        self.assertTrue(verify_packet_hash(packet))
        self.assertTrue(packet["redaction_applied"])
        self.assertNotIn("learner_reasoning", packet)
        self.assertNotIn("internal_critic", packet)
        tampered = dict(packet)
        tampered["claims"] = ["changed"]
        self.assertFalse(verify_packet_hash(tampered))

    def test_owner_pc_path_is_redacted(self):
        packet = self.packet(test_log=r"C:\Users\trann\secret\test.log")
        self.assertNotIn(r"C:\Users\trann", packet["test_log"])
        self.assertIn("[REDACTED_OWNER_PATH]", packet["test_log"])

    def test_secret_like_material_blocks_packet(self):
        with self.assertRaises(CriticPacketError):
            self.packet(test_log="token " + "sk-" + "1234567890abcdefghijklmnop")

    def test_claims_must_be_one_line(self):
        with self.assertRaises(CriticPacketError):
            self.packet(claims=("line one\nline two",))

    def test_manual_channel_exports_then_waits(self):
        packet = self.packet()
        critic = ManualExternalCritic(
            packet_out_path=self.root / "packet.json",
            response_in_path=self.root / "response.json",
        )
        receipt = critic.critique(packet)
        self.assertEqual(receipt["status"], "PENDING_EXTERNAL_CRITIC")
        self.assertTrue((self.root / "packet.json").is_file())
        envelope = json.loads((self.root / "packet.json").read_text(encoding="utf-8"))
        self.assertEqual(envelope["packet"]["packet_hash"], packet["packet_hash"])
        self.assertEqual(envelope["prompt_version"], "external-critic-v1")

    def test_manual_valid_response_is_partial_independence_evidence(self):
        packet = self.packet()
        critic = ManualExternalCritic(
            packet_out_path=self.root / "packet.json",
            response_in_path=self.root / "response.json",
            critic_provider="gpt-external",
            critic_model="declared-gpt",
            run_id="manual-1",
        )
        response = json.dumps({
            "findings": [],
            "verdict": "NO_MATERIAL_DEFECT_FOUND",
            "confidence_note": "Bounded review only",
        })
        receipt = critic.parse_response(packet, response)
        self.assertEqual(receipt["status"], "RECORDED")
        self.assertEqual(receipt["independence_status"], "PARTIAL")
        self.assertEqual(receipt["blind_or_revealed"], "BLIND")
        self.assertEqual(len(receipt["output_hash"]), 64)
        self.assertFalse(receipt["automatic_verified_promotion"])

    def test_invalid_response_fails_closed(self):
        packet = self.packet()
        critic = ManualExternalCritic(
            packet_out_path=self.root / "packet.json",
            response_in_path=self.root / "response.json",
        )
        receipt = critic.parse_response(packet, '{"verdict":"PASS"}')
        self.assertEqual(receipt["status"], "CRITIC_RUN_INVALID")
        self.assertFalse(receipt["eligible_as_critic_evidence"])

    def test_post_expiry_response_is_evidence_only(self):
        packet = self.packet()
        critic = ManualExternalCritic(
            packet_out_path=self.root / "packet.json",
            response_in_path=self.root / "response.json",
        )
        response = json.dumps({
            "findings": [],
            "verdict": "NO_MATERIAL_DEFECT_FOUND",
            "confidence_note": "Late bounded review",
        })
        receipt = critic.parse_response(packet, response, post_expiry=True)
        self.assertEqual(receipt["status"], "POST_EXPIRY")
        self.assertTrue(receipt["post_expiry"])

    def test_verdict_schema_rejects_pass_and_empty_defect(self):
        with self.assertRaises(CriticSchemaError):
            CriticResult.from_json_text(json.dumps({
                "findings": [],
                "verdict": "PASS",
                "confidence_note": "bad vocabulary",
            }))
        with self.assertRaises(CriticSchemaError):
            CriticResult.from_json_text(json.dumps({
                "findings": [],
                "verdict": "DEFECT_FOUND",
                "confidence_note": "missing finding",
            }))


if __name__ == "__main__":
    unittest.main()
