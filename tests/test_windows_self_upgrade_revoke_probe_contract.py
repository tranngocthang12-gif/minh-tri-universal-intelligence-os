from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent.parent
PROBE = ROOT / "ops" / "windows" / "self_upgrade_owner_revoke_probe.py"


class WindowsSelfUpgradeRevokeProbeContract(unittest.TestCase):
    def setUp(self):
        self.text = PROBE.read_text(encoding="utf-8")

    def test_uses_dpapi_without_execution_policy_bypass(self):
        self.assertIn("ConvertTo-SecureString", self.text)
        self.assertIn("ZeroFreeBSTR", self.text)
        self.assertIn('"powershell.exe", "-NoProfile", "-Command"', self.text)
        self.assertNotIn("-ExecutionPolicy", self.text)
        self.assertNotIn("Set-ExecutionPolicy", self.text)

    def test_proof_requires_owner_revoke_and_post_revoke_block(self):
        self.assertIn("session.owner_revoke", self.text)
        self.assertIn("LeaseRevokedError", self.text)
        self.assertIn("PASS_OWNER_REVOKE_E2E", self.text)
        self.assertIn('"plaintext_secret_persisted": False', self.text)

    def test_probe_never_prints_secret_variable(self):
        self.assertNotIn("print(secret", self.text)
        self.assertNotIn('"secret": secret', self.text)


if __name__ == "__main__":
    unittest.main()
