import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".py", ".md", ".json", ".toml", ".yml", ".yaml", ".txt", ".ps1", ".bat"}
SECRET_ASSIGNMENT = re.compile(
    r"(?i)\\b(?:OPENAI_API_KEY|OPENAI_TUNNEL_RUNTIME_API_KEY|RUNTIME_API_KEY|"
    r"MINHTRI_BRAIN_TOKEN|MINHTRI_OWNER_SECRET)\\s*[:=]\\s*[\\\"']?"
    r"([A-Za-z0-9_\\-]{20,})"
)
OPENAI_KEY = re.compile(r"\\bsk-[A-Za-z0-9_-]{20,}\\b")
PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----"


class SecretHygiene(unittest.TestCase):
    def test_repository_contains_no_obvious_committed_runtime_secrets(self):
        findings = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            rel = path.relative_to(ROOT)
            if ".git" in rel.parts or rel.as_posix() == "tests/test_secret_hygiene.py":
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if PRIVATE_KEY in text or OPENAI_KEY.search(text) or SECRET_ASSIGNMENT.search(text):
                findings.append(rel.as_posix())
        self.assertEqual(findings, [], f"possible committed secrets: {findings}")


if __name__ == "__main__":
    unittest.main()
