import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OPS = ROOT / "ops" / "windows"

class WindowsTunnelPersistenceContract(unittest.TestCase):
    def read(self, name):
        return (OPS / name).read_text(encoding="utf-8")

    def test_provisioner_uses_secure_prompt_and_dpapi(self):
        text = self.read("provision_tunnel_runtime_key.ps1")
        self.assertIn("Read-Host -AsSecureString", text)
        self.assertIn("ConvertFrom-SecureString", text)
        self.assertIn("tunnel.runtime.dpapi", text)
        self.assertIn("plaintext_persisted=$false", text.replace(" ", ""))
        self.assertNotIn("PtrToStringBSTR", text)

    def test_unattended_launcher_unseals_only_in_memory_and_cleans_environment(self):
        text = self.read("run_tunnel_unattended.ps1")
        self.assertIn("ConvertTo-SecureString", text)
        self.assertIn("CONTROL_PLANE_API_KEY", text)
        self.assertIn("runtime_supervisor", text)
        self.assertIn("--health.listen-addr 127.0.0.1:0", text)
        self.assertIn("Remove-Item Env:CONTROL_PLANE_API_KEY", text)
        self.assertIn("ZeroFreeBSTR", text)

    def test_task_installer_contains_no_secret_reference_in_task_arguments(self):
        text = self.read("install_tunnel_logon_task.ps1")
        self.assertIn("New-ScheduledTaskTrigger -AtLogOn", text)
        self.assertIn("-RunLevel Limited", text)
        self.assertIn("BLOCKED_TUNNEL_DPAPI_SECRET_MISSING", text)
        self.assertIn("secret_in_task_arguments=$false", text.replace(" ", ""))
        self.assertNotIn("CONTROL_PLANE_API_KEY", text)
        self.assertNotIn("--control-plane.api-key", text)

    def test_installer_is_fail_closed_on_missing_prerequisites(self):
        text = self.read("install_tunnel_logon_task.ps1")
        self.assertIn("BLOCKED_UNATTENDED_LAUNCHER_MISSING", text)
        self.assertIn("BLOCKED_TUNNEL_DPAPI_SECRET_MISSING", text)

if __name__ == "__main__":
    unittest.main()
