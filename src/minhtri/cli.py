"""Offline CLI for Tier 1. Inputs are explicit JSON commands, not model output."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .arena import ArenaService
from .core import GateError, Ledger, next_goal


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="minhtri", description="MINH TRÍ v0.1 learning ledger")
    parser.add_argument("--home", default="brain", help="Local ledger directory (default: brain)")
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("init", help="Create a new empty ledger")
    command = sub.add_parser("apply", help="Apply one JSON command from a file")
    command.add_argument("json_file", type=Path)
    sub.add_parser("status", help="Show current counts and next eligible goal")
    sub.add_parser("verify", help="Replay the hash chain and compare the state cache")
    sub.add_parser("repair-snapshot", help="Rebuild state cache from the event chain after audit")
    arena = sub.add_parser("arena", help="Shadow-only, provider-neutral AI Commons")
    arena.add_argument("--constitution", default="docs/PHILOSOPHY.md", help="Approved philosophy file to pin")
    arena_sub = arena.add_subparsers(dest="arena_action", required=True)
    arena_sub.add_parser("init", help="Create an arena ledger after core init")
    arena_apply = arena_sub.add_parser("apply", help="Apply one shadow arena command")
    arena_apply.add_argument("json_file", type=Path)
    arena_sub.add_parser("status", help="Show shadow arena status")
    arena_sub.add_parser("verify", help="Replay shadow arena ledger")
    arena_sub.add_parser("repair-snapshot", help="Rebuild arena cache from the audited event chain")
    arena_task = arena_sub.add_parser("task", help="Export a current bounded task packet")
    arena_task.add_argument("task_id")
    args = parser.parse_args(argv)
    ledger = Ledger(args.home)
    try:
        if args.action == "arena":
            service = ArenaService(args.home, args.constitution)
            if args.arena_action == "init":
                service.init()
                result = {"status": "SHADOW_INITIALIZED", "home": str(service.ledger.home)}
            elif args.arena_action == "apply":
                payload = json.loads(args.json_file.read_text(encoding="utf-8"))
                receipt = service.apply(payload)
                result = {"status": "SHADOW_RECORDED", "event_count": receipt["event_count"], "head": receipt["head"]}
                if payload.get("type") == "open_task":
                    task_id = payload["data"]["id"]
                    result["task_fingerprint"] = receipt["state"]["tasks"][task_id]["fingerprint"]
            elif args.arena_action == "status":
                result = service.status()
            elif args.arena_action == "task":
                result = service.task_packet(args.task_id)
            elif args.arena_action == "repair-snapshot":
                count, head = service.ledger.repair_snapshot()
                result = {"status": "SHADOW_CACHE_REPAIRED", "event_count": count, "head": head}
            else:
                state, count, head = service.ledger.verify()
                ledger.verify()
                result = {"status": "VALID_SHADOW_LEDGER", "event_count": count, "head": head, "phase": state["phase"]}
        elif args.action == "init":
            ledger.init()
            result = {"status": "INITIALIZED", "home": str(ledger.home)}
        elif args.action == "apply":
            payload = json.loads(args.json_file.read_text(encoding="utf-8"))
            result = ledger.apply(payload)
            result = {"status": "APPLIED", "event_count": result["event_count"], "head": result["head"]}
        elif args.action == "repair-snapshot":
            count, head = ledger.repair_snapshot()
            result = {"status": "REPAIRED", "event_count": count, "head": head}
        else:
            state, count, head = ledger.verify()
            result = {"status": "VALID", "event_count": count, "head": head}
            if args.action == "status":
                result["next"] = next_goal(state)
                result["counts"] = {key: len(value) for key, value in state.items() if isinstance(value, dict)}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (GateError, OSError, ValueError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
