"""Scan reachable Git history for obvious credential material without printing secrets.

This complements current-tree secret hygiene. Findings report only object/path/rule so CI logs
never echo the suspected secret value.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import PurePosixPath

MAX_BLOB_BYTES = 2 * 1024 * 1024
TEXT_SUFFIXES = {
    ".py", ".md", ".json", ".toml", ".yml", ".yaml", ".txt", ".ps1", ".bat",
    ".ini", ".cfg", ".conf", ".env", ".sh",
}

PATTERNS = {
    "private-key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "openai-key": re.compile(rb"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "github-pat": re.compile(rb"\b(?:github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{20,})\b"),
    "runtime-secret-assignment": re.compile(
        rb"(?i)\b(?:OPENAI_API_KEY|OPENAI_TUNNEL_RUNTIME_API_KEY|RUNTIME_API_KEY|"
        rb"MINHTRI_BRAIN_TOKEN|MINHTRI_OWNER_SECRET|GH_TOKEN|GITHUB_TOKEN)"
        rb"\s*[:=]\s*[\"']?([A-Za-z0-9_./+=:-]{20,})"
    ),
}


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], stderr=subprocess.DEVNULL)


def main() -> int:
    try:
        objects = git("rev-list", "--objects", "--all").decode("utf-8", "replace").splitlines()
    except (OSError, subprocess.CalledProcessError):
        print("history-secret-scan: git history unavailable", file=sys.stderr)
        return 2

    findings: list[tuple[str, str, str]] = []
    seen: set[str] = set()

    for line in objects:
        oid, sep, path = line.partition(" ")
        if not sep or oid in seen:
            continue
        seen.add(oid)
        suffix = PurePosixPath(path).suffix.lower()
        if suffix not in TEXT_SUFFIXES and PurePosixPath(path).name not in {".env", ".env.local"}:
            continue
        try:
            if git("cat-file", "-t", oid).strip() != b"blob":
                continue
            size = int(git("cat-file", "-s", oid).strip())
            if size > MAX_BLOB_BYTES:
                continue
            data = git("cat-file", "-p", oid)
        except (OSError, ValueError, subprocess.CalledProcessError):
            continue
        if b"\x00" in data:
            continue
        for rule, pattern in PATTERNS.items():
            if pattern.search(data):
                findings.append((oid[:12], path, rule))

    if findings:
        print("history-secret-scan: possible secret material found; values are redacted")
        for oid, path, rule in sorted(set(findings)):
            print(f"{oid} {path} [{rule}]")
        return 1

    print("history-secret-scan: no obvious credential patterns in reachable history")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
