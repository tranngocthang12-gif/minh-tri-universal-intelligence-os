"""Owner-PC reconnect: pull only an immutable, protected-main cache.

This module NEVER writes to GitHub, the Tier-1 ledger, or system configuration;
it never executes downloaded files. It does not run a background service.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import stat
from contextlib import contextmanager
from http.client import HTTPException
import shutil
import tempfile
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

REPO = "tranngocthang12-gif/minh-tri-universal-intelligence-os"
API = "https://api.github.com/repos/" + REPO
SELECTOR = "config/pc_reconnect_sync_selection_v1.json"
CONTINUITY_LAW = "docs/LAW_UNIVERSAL_LEARNING_CONTINUITY_20261004.md"
MAX_FILE_BYTES = 262144
MAX_BUNDLE_BYTES = 3 * 1024 * 1024
MAX_SELECTED = 12
MAX_HTTP_BYTES = 800000
SHA40 = re.compile(r"^[0-9a-f]{40}$")
ALLOWED_ROOTS = frozenset({"state", "config", "docs", "knowledge"})
WINDOWS_RESERVED = frozenset({"CON", "PRN", "AUX", "NUL"} | {f"COM{i}" for i in range(1, 10)} | {f"LPT{i}" for i in range(1, 10)})


class SyncBlocked(ValueError):
    """An unsafe or unverifiable sync MUST leave the last-good cache in place."""


def _safe_path(path):
    if (not isinstance(path, str) or not path or len(path) > 220
            or "\\" in path or ":" in path or path.startswith("/")
            or not path.endswith((".json", ".yaml", ".yml", ".md"))):
        raise SyncBlocked("unsafe repository path")
    parts = path.split("/")
    if (len(parts) < 2 or parts[0] not in ALLOWED_ROOTS
            or any(not part or part.startswith(".") or part != part.rstrip(" .")
                   or part.split(".", 1)[0].upper() in WINDOWS_RESERVED
                   or any(ord(c) < 32 for c in part)
                   for part in parts)):
        raise SyncBlocked("repository path outside safe scope")
    return path


def _sha(value):
    return isinstance(value, str) and bool(SHA40.fullmatch(value))


def _git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def fetch_public_github(endpoint):
    """Read public GitHub REST JSON only; never load a local credential/token."""
    req = Request(
        API + "/" + endpoint,
        headers={"Accept": "application/vnd.github+json",
                 "User-Agent": "MinhTri-PC-Reconnect-V1",
                 "X-GitHub-Api-Version": "2022-11-28"},
    )
    try:
        with urlopen(req, timeout=12) as stream:
            data = stream.read(MAX_HTTP_BYTES + 1)
    except (HTTPError, URLError, HTTPException, TimeoutError, OSError) as exc:
        raise SyncBlocked("GitHub unavailable or unauthorized") from exc
    if len(data) > MAX_HTTP_BYTES:
        raise SyncBlocked("GitHub metadata exceeds size limit")
    try:
        return json.loads(data.decode("utf-8"))
    except (UnicodeError, ValueError) as exc:
        raise SyncBlocked("GitHub response is not valid JSON") from exc


def _fetch_file(fetch, path, commit):
    _safe_path(path)
    obj = fetch("contents/" + quote(path, safe="/") + "?ref=" + commit)
    if not isinstance(obj, dict) or obj.get("type") != "file" or obj.get("path") != path:
        raise SyncBlocked("GitHub path is not a regular file")
    declared_size = obj.get("size")
    if type(declared_size) is not int or not 0 <= declared_size <= MAX_FILE_BYTES:
        raise SyncBlocked("GitHub file outside byte budget")
    if obj.get("encoding") != "base64" or not isinstance(obj.get("content"), str):
        raise SyncBlocked("GitHub content encoding not supported")
    try:
        data = base64.b64decode(obj["content"], validate=False)
    except (ValueError, TypeError) as exc:
        raise SyncBlocked("invalid GitHub base64") from exc
    if len(data) != declared_size or not _sha(obj.get("sha")) or _git_blob(data) != obj["sha"]:
        raise SyncBlocked("GitHub file blob integrity mismatch")
    try:
        data.decode("utf-8")
    except UnicodeError as exc:
        raise SyncBlocked("non-UTF-8 canonical document") from exc
    return data


def _parsed(files, path):
    try:
        value = json.loads(files[path].decode("utf-8"))
    except (KeyError, ValueError, UnicodeError) as exc:
        raise SyncBlocked("invalid canonical JSON") from exc
    if not isinstance(value, dict):
        raise SyncBlocked("canonical document must be an object")
    return value


def build_snapshot(fetch=fetch_public_github):
    """Verify one pin of protected main plus a governed, bounded file selection."""
    branch = fetch("branches/main")
    if not isinstance(branch, dict) or branch.get("protected") is not True:
        raise SyncBlocked("main is not reported protected")
    sha = (branch.get("commit") or {}).get("sha")
    if not _sha(sha):
        raise SyncBlocked("invalid protected main SHA")
    files = {}
    folded_paths = set()

    def add(path):
        _safe_path(path)
        if path.lower() in folded_paths and path not in files:
            raise SyncBlocked("case-folded repository path collision")
        if path not in files:
            files[path] = _fetch_file(fetch, path, sha)
            folded_paths.add(path.lower())
        if sum(map(len, files.values())) > MAX_BUNDLE_BYTES:
            raise SyncBlocked("snapshot exceeds byte budget")

    for path in ("state/bootstrap.json", "state/current.yaml",
                 "state/tasks.yaml", SELECTOR):
        add(path)
    boot = _parsed(files, "state/bootstrap.json")
    current = _parsed(files, "state/current.yaml")
    tasks = _parsed(files, "state/tasks.yaml")
    selection = _parsed(files, SELECTOR)
    if (boot.get("schema") != "minhtri-bootstrap-root/v1"
            or current.get("schema") != "minhtri-current-state/v1"
            or boot.get("durable_continuity_authority") != "GITHUB_PROTECTED_MAIN"
            or current.get("durable_continuity_authority") != "GITHUB_PROTECTED_MAIN"
            or boot.get("project") != current.get("project")):
        raise SyncBlocked("canonical authority mismatch")
    routes = {"boot_root": ("state/bootstrap.json", current.get("boot_root")),
              "current_state": ("state/current.yaml", boot.get("current_state")),
              "task_registry": ("state/tasks.yaml", boot.get("task_registry")),
              "task_registry_current": ("state/tasks.yaml", current.get("task_registry")),
              "master_blueprint": (boot.get("master_blueprint"), current.get("master_blueprint")),
              "law_precedence": (boot.get("law_precedence"), current.get("law_precedence")),
              "role_bootstrap": (boot.get("role_bootstrap"), current.get("role_bootstrap"))}
    if any(not a or a != b for a, b in routes.values()):
        raise SyncBlocked("canonical bootstrap route conflict")
    required = {boot.get("master_blueprint"), boot.get("law_precedence"),
                boot.get("role_bootstrap"), boot.get("recovery_entrypoint"),
                current.get("current_architecture"), CONTINUITY_LAW}
    if current.get("current_architecture") != boot.get("master_blueprint"):
        raise SyncBlocked("current architecture pointer conflict")
    if any(not isinstance(p, str) for p in required):
        raise SyncBlocked("required document pointer missing")
    for path in sorted(required):
        add(path)
    if tasks.get("registry_authority") != "state/tasks.yaml":
        raise SyncBlocked("task registry not authoritative")
    task_rows = tasks.get("tasks")
    if not isinstance(task_rows, list) or not all(isinstance(t, dict) for t in task_rows):
        raise SyncBlocked("task registry invalid")
    ids = [t.get("task_id") for t in task_rows]
    if (not ids or any(not isinstance(x, str) or not x for x in ids)
            or len(set(ids)) != len(ids)
            or current.get("active_task_id") not in ids):
        raise SyncBlocked("active task cannot be recovered")
    if (selection.get("schema") != "minhtri-pc-sync-selection/v1"
            or selection.get("authority") != "PROTECTED_MAIN_ONLY"):
        raise SyncBlocked("ungoverned sync selection")
    selected = selection.get("selected_main_paths")
    if (not isinstance(selected, list) or len(selected) > MAX_SELECTED
            or len(set(map(str, selected))) != len(selected)):
        raise SyncBlocked("invalid selected learning list")
    for path in selected:
        _safe_path(path)
        if (not path.startswith(("docs/learning/", "knowledge/"))
                or re.search(r"(^|[_-])DRAFT([_.-]|$)", path, flags=re.I)):
            raise SyncBlocked("learning snapshot selection invalid")
        add(path)
    active = next(t for t in task_rows if t["task_id"] == current["active_task_id"])
    if not isinstance(active.get("next_action"), str) or current.get("next_checkpoint") != active["next_action"]:
        raise SyncBlocked("active task and current NEXT ACTION disagree")
    handoff_ref = active.get("handoff_ref")
    if not isinstance(handoff_ref, str) or not handoff_ref.startswith("docs/"):
        raise SyncBlocked("active task handoff reference missing or invalid")
    add(handoff_ref)
    handoff = files[handoff_ref].decode("utf-8")
    if "## NEXT ACTION\n" not in handoff:
        raise SyncBlocked("active handoff has no NEXT ACTION section")
    actual_action = handoff.split("## NEXT ACTION\n", 1)[1].strip().splitlines()[0].strip()
    if not actual_action or actual_action != active["next_action"]:
        raise SyncBlocked("active handoff NEXT ACTION disagrees with canonical route")
    warnings = []
    if active.get("status") in ("DONE", "STALE", "BLOCKED", "DRAFT"):
        warnings.append("ACTIVE_TASK_NOT_EXECUTABLE_" + str(active.get("status")))
    manifest = {
        "schema": "minhtri-pc-main-cache/v1",
        "repository": REPO,
        "source": "PINNED_PROTECTED_MAIN",
        "head": sha,
        "files": [{"path": p, "git_blob_sha": _git_blob(b),
                   "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
                  for p, b in sorted(files.items())],
        "route_warnings": warnings,
        "local_brain_written": False,
        "learning_understanding_proven": False,
        "background_learning_enabled": False,
        "unmerged_prs_included": False,
    }
    return {"head": sha, "files": files, "manifest": manifest}


def _safe_cache_root(root):
    path = Path(root)
    if path.name != "pc-reconnect-sync" or path.parent.name != "minhtri-runtime-current":
        raise SyncBlocked("cache destination outside dedicated runtime directory")
    for candidate in (path.parent, path):
        if candidate.is_symlink() or getattr(candidate, "is_junction", lambda: False)():
            raise SyncBlocked("cache destination may not be a link or junction")
    return path


def _verify_stored(directory, manifest):
    if not isinstance(manifest, dict) or not isinstance(manifest.get("files"), list):
        raise SyncBlocked("local cache manifest is invalid")
    for item in manifest["files"]:
        if not isinstance(item, dict):
            raise SyncBlocked("invalid cached file entry")
        path = _safe_path(item.get("path"))
        file = directory / "files" / Path(*path.split("/"))
        if file.is_symlink() or not file.is_file():
            raise SyncBlocked("cached file missing or linked")
        data = file.read_bytes()
        if (len(data) != item.get("bytes")
                or hashlib.sha256(data).hexdigest() != item.get("sha256")
                or _git_blob(data) != item.get("git_blob_sha")):
            raise SyncBlocked("cached file integrity mismatch")


def _atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = None
    try:
        with tempfile.NamedTemporaryFile("w", dir=path.parent, suffix=".tmp",
                                         encoding="utf-8", delete=False) as out:
            handle = Path(out.name)
            json.dump(value, out, ensure_ascii=False, sort_keys=True, indent=2)
            out.flush()
            os.fsync(out.fileno())
        os.replace(handle, path)
    finally:
        if handle is not None and handle.exists():
            handle.unlink()


def apply_snapshot(snapshot, root, fetch=fetch_public_github):
    """Atomic pointer to a versioned *noncanonical* copy; never overwrite Tier-1."""
    root = _safe_cache_root(root)
    manifest = snapshot["manifest"]
    head = snapshot["head"]
    if not _sha(head) or manifest.get("head") != head:
        raise SyncBlocked("snapshot head mismatch")
    pointer = root / "current.json"
    old = None
    if pointer.exists():
        try:
            record = json.loads(pointer.read_text(encoding="utf-8"))
        except (ValueError, OSError, UnicodeError) as exc:
            raise SyncBlocked("local cache pointer corrupted") from exc
        old = record.get("head") if isinstance(record, dict) else None
        if not _sha(old) or record.get("schema") != "minhtri-pc-cache-pointer/v1":
            raise SyncBlocked("local cache pointer invalid")
        old_dir = root / "snapshots" / old
        try:
            old_manifest = json.loads((old_dir / "manifest.json").read_text(encoding="utf-8"))
        except (OSError, ValueError, UnicodeError) as exc:
            raise SyncBlocked("previous snapshot manifest missing") from exc
        if old_manifest.get("head") != old:
            raise SyncBlocked("previous snapshot head altered")
        _verify_stored(old_dir, old_manifest)
        if old != head:
            status = fetch("compare/" + old + "..." + head)
            if not isinstance(status, dict) or status.get("status") != "ahead":
                raise SyncBlocked("non-fast-forward GitHub main; refusing rollback")
    target = root / "snapshots" / head
    root.joinpath("snapshots").mkdir(parents=True, exist_ok=True)
    if target.exists():
        try:
            present = json.loads((target / "manifest.json").read_text(encoding="utf-8"))
        except (OSError, ValueError, UnicodeError) as exc:
            raise SyncBlocked("existing target snapshot corrupt") from exc
        if present != manifest:
            raise SyncBlocked("existing target snapshot metadata differs")
        _verify_stored(target, manifest)
    else:
        temp = Path(tempfile.mkdtemp(prefix="stage-", dir=root / "snapshots"))
        try:
            for path, data in sorted(snapshot["files"].items()):
                _safe_path(path)
                out = temp / "files" / Path(*path.split("/"))
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(data)
            (temp / "manifest.json").write_text(
                json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
                encoding="utf-8")
            _verify_stored(temp, manifest)
            os.replace(temp, target)
        finally:
            if temp.exists():
                shutil.rmtree(temp)
    _atomic_json(pointer, {"schema": "minhtri-pc-cache-pointer/v1",
                           "head": head, "role": "NON_CANONICAL_READ_ONLY_GITHUB_MIRROR",
                           "local_brain_unchanged": True})
    return {"status": "NONCANONICAL_CACHE_UPDATED" if old != head else "CACHE_ALREADY_CURRENT",
            "head": head, "old_head": old, "file_count": len(snapshot["files"]),
            "route_warnings": manifest["route_warnings"],
            "local_brain_written": False}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Protected-main read-only PC reconnect cache")
    parser.add_argument("--apply", action="store_true", help="Write versioned noncanonical cache")
    parser.add_argument("--destination", help="Dedicated .../minhtri-runtime-current/pc-reconnect-sync")
    args = parser.parse_args(argv)
    if args.apply and not args.destination:
        parser.error("--apply requires an explicit dedicated destination")
    try:
        snapshot = build_snapshot()
        result = (apply_snapshot(snapshot, args.destination) if args.apply else
                  {"status": "DRY_RUN_VERIFIED_NO_WRITES", "head": snapshot["head"],
                   "file_count": len(snapshot["files"]),
                   "route_warnings": snapshot["manifest"]["route_warnings"],
                   "local_brain_written": False})
    except (SyncBlocked, OSError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
