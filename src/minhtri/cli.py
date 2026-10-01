"""Offline CLI for Tier 1. Inputs are explicit JSON commands, not model output."""

from __future__ import annotations

import argparse
import getpass
import json
import os
import sys
from pathlib import Path

from .core import GateError, Ledger, current_focus, evolve, next_goal, utcnow
from .owner import ENV_SECRET, OwnerGateError, config_path, hash_secret, require_owner

UNSTATED = "CHƯA NÊU"
LEARN_DOMAIN_CONTRACT = "CHƯA ĐẶT: sổ học của Owner, chưa có hợp đồng đo kết quả"


def _learn_commands(state: dict, args: argparse.Namespace, now: str) -> tuple[str, list[dict]]:
    """Translate one Owner `learn` request into existing ledger commands. No network access."""
    if not args.uri and not args.text:
        raise GateError("learn needs --uri or --text")
    focus = current_focus(state)
    domain_id = args.domain_id or (focus["domain_id"] if focus else None)
    if not domain_id:
        raise GateError("No active focus; give --domain-id (and --domain-name for a new domain)")
    commands = []
    if domain_id not in state["domains"]:
        if not args.domain_name:
            raise GateError(f"Unknown domain {domain_id}; add --domain-name to register it")
        commands.append({"type": "register_domain", "data": {
            "id": domain_id, "name": args.domain_name, "risk_class": "NORMAL",
            "measurement_contract": LEARN_DOMAIN_CONTRACT}})
    base = args.id or "learn-" + now.replace("-", "").replace(":", "").lower()
    taken = set(state["sources"]) | set(state["evidence"]) | set(state.get("learning_focuses", {}))
    if args.id and ({base, base + "-src", base + "-ev"} & taken):
        raise GateError(f"ID already used: {base}")
    n, stem = 2, base
    while {base, base + "-src", base + "-ev"} & taken:
        base, n = f"{stem}-{n}", n + 1
    source_id = base + "-src"
    commands.append({"type": "record_source", "data": {
        "id": source_id, "domain_id": domain_id, "uri": args.uri or f"owner-text:{base}",
        "captured_at": now, "kind": args.source_kind, "rights_status": args.rights}})
    if args.text:
        commands.append({"type": "record_evidence", "data": {
            "id": base + "-ev", "domain_id": domain_id, "source_id": source_id,
            "statement": args.text, "observed_at": now}})
    commands.append({"type": "set_learning_focus", "data": {
        "id": base, "status": "ACTIVE", "domain_id": domain_id, "source_id": source_id, "note": args.note,
        "expected_lesson": args.expected_lesson, "uncertainty": args.uncertainty}})
    return base, commands


def _apply_all(ledger: Ledger, state: dict, commands: list[dict], now: str, approved_by: str) -> dict:
    """Dry-run every command first so a rejected request appends nothing."""
    trial = state
    for command in commands:
        trial = evolve(trial, command, now)
    result = {}
    for command in commands:
        result = ledger.apply(command, approved_by=approved_by)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="minhtri", description="MINH TRÍ v0.1 learning ledger")
    parser.add_argument("--home", default="brain", help="Local ledger directory (default: brain)")
    parser.add_argument("--owner-id", help="Declared actor ID for Owner-only commands (not identity verification)")
    parser.add_argument("--owner-secret", help=f"Owner secret (prefer ${ENV_SECRET}; a flag can end up in shell history)")
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("init", help="Create a new empty ledger")
    command = sub.add_parser("apply", help="Apply one JSON command from a file")
    command.add_argument("json_file", type=Path)
    sub.add_parser("status", help="Show current counts and next eligible goal")
    sub.add_parser("verify", help="Replay the hash chain and compare the state cache")
    sub.add_parser("repair-snapshot", help="Rebuild state cache from the event chain after audit")
    learn = sub.add_parser("learn", help="Owner records something to learn and sets it as the focus")
    learn.add_argument("--uri", help="Where it came from; stored only, never fetched")
    learn.add_argument("--text", help="Owner-pasted case or note, stored as declared evidence")
    learn.add_argument("--note", required=True, help="Why the Owner wants to learn this")
    learn.add_argument("--expected-lesson", default=UNSTATED, help="What the Owner expects to learn (untested)")
    learn.add_argument("--uncertainty", default=UNSTATED, help="How unsure the Owner is and why")
    learn.add_argument("--domain-id", help="Domain ID; defaults to the current focus domain")
    learn.add_argument("--domain-name", help="Register --domain-id as a new NORMAL domain with this name")
    learn.add_argument("--source-kind", choices=("THIRD_PARTY", "PUBLIC", "FIRST_PARTY"), default="THIRD_PARTY")
    learn.add_argument("--rights", choices=("UNKNOWN", "CLEAR", "RESTRICTED"), default="UNKNOWN")
    learn.add_argument("--id", help="Optional focus ID (lowercase); generated from time if omitted")
    sub.add_parser("hash-secret", help="Print the SHA-256 of a secret read without echo (or from piped stdin)")
    sub.add_parser("focus", help="Show the current learning focus")
    unfocus = sub.add_parser("unfocus", help="Stop the current focus; history is kept")
    unfocus.add_argument("--reason", default="Owner dừng tập trung", help="Why the focus stops")
    args = parser.parse_args(argv)
    ledger = Ledger(args.home)

    def gate() -> str:
        secret = args.owner_secret or os.environ.get(ENV_SECRET)
        return require_owner(args.owner_id, secret, config_path(None))

    try:
        if args.action == "hash-secret":
            if sys.stdin.isatty():
                secret = getpass.getpass("Owner secret (not shown): ")
            else:
                secret = sys.stdin.readline().rstrip("\r\n")
            if not secret:
                raise GateError("Empty secret")
            print(json.dumps({"owner_secret_sha256": hash_secret(secret)}))
            return 0
        if args.action == "init":
            ledger.init()
            result = {"status": "INITIALIZED", "home": str(ledger.home)}
        elif args.action == "apply":
            payload = json.loads(args.json_file.read_text(encoding="utf-8"))
            approver = gate()
            result = ledger.apply(payload, approved_by=approver)
            result = {"status": "APPLIED", "event_count": result["event_count"], "head": result["head"]}
        elif args.action == "learn":
            approver = gate()
            state, _, _ = ledger.verify()
            now = utcnow()
            focus_id, commands = _learn_commands(state, args, now)
            applied = _apply_all(ledger, state, commands, now, approver)
            result = {"status": "FOCUS_SET", "focus": applied["state"]["learning_focuses"][focus_id],
                      "events_appended": len(commands), "event_count": applied["event_count"],
                      "head": applied["head"]}
        elif args.action == "focus":
            state, count, head = ledger.verify()
            focus = current_focus(state)
            result = {"status": "VALID", "event_count": count, "head": head,
                      "focus": focus if focus else "NO_ACTIVE_FOCUS"}
        elif args.action == "unfocus":
            approver = gate()
            state, _, _ = ledger.verify()
            focus = current_focus(state)
            if not focus:
                raise GateError("No active focus to stop")
            applied = ledger.apply({"type": "set_learning_focus",
                                    "data": {"id": focus["id"], "status": "STOPPED", "reason": args.reason}},
                                   approved_by=approver)
            result = {"status": "FOCUS_STOPPED", "focus": applied["state"]["learning_focuses"][focus["id"]],
                      "event_count": applied["event_count"], "head": applied["head"]}
        elif args.action == "repair-snapshot":
            approver = gate()
            count, head = ledger.repair_snapshot(approved_by=approver)
            result = {"status": "REPAIRED", "event_count": count, "head": head}
        else:
            state, count, head = ledger.verify()
            result = {"status": "VALID", "event_count": count, "head": head}
            if args.action == "status":
                result["next"] = next_goal(state)
                result["counts"] = {key: len(value) for key, value in state.items() if isinstance(value, dict)}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except OwnerGateError as exc:
        print(json.dumps({"status": "BLOCKED", "reason": exc.code, "detail": exc.detail}, ensure_ascii=False), file=sys.stderr)
        return 2
    except (GateError, OSError, ValueError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
