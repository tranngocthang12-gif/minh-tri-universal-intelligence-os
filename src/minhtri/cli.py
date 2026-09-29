"""Offline CLI for Tier 1. Inputs are explicit JSON commands, not model output."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .arena import ArenaService
from .arena_migration import archive_legacy_arena, verify_legacy_arena
from .bottleneck import BottleneckService
from .core import GateError, Ledger, next_goal
from .epistemic import EpistemicService
from .tasking import TaskService
from .workcell import FourSeatWorkcellService


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
    arena.add_argument("--brain-root", default=".", help="Repository root containing the canonical brain artifacts")
    arena.add_argument("--brain-revision", default=None,
                       help="Pinned 40-character Git SHA; defaults to git rev-parse HEAD in --brain-root")
    arena_sub = arena.add_subparsers(dest="arena_action", required=True)
    arena_sub.add_parser("init", help="Create an arena ledger after core init")
    arena_apply = arena_sub.add_parser("apply", help="Apply one shadow arena command")
    arena_apply.add_argument("json_file", type=Path)
    arena_sub.add_parser("status", help="Show shadow arena status and pinned GitHub brain version")
    arena_sub.add_parser("verify", help="Replay shadow arena ledger")
    arena_sub.add_parser("repair-snapshot", help="Rebuild arena cache from the audited event chain")
    arena_task = arena_sub.add_parser("task", help="Export a current bounded task packet")
    arena_task.add_argument("task_id")

    migration = sub.add_parser("arena-migration", help="Verify/archive a pre-law AI Commons ledger without rewriting history")
    migration_sub = migration.add_subparsers(dest="migration_action", required=True)
    migration_verify = migration_sub.add_parser("verify", help="Replay a legacy PR #2/PR #3 Arena ledger")
    migration_verify.add_argument("legacy_home", type=Path)
    migration_verify.add_argument("--schema", default=None,
                                  choices=["arena-v1-core-constitution", "arena-v2-github-brain"])
    migration_archive = migration_sub.add_parser("archive", help="Verify and copy a legacy Arena ledger to an immutable archive")
    migration_archive.add_argument("legacy_home", type=Path)
    migration_archive.add_argument("archive_root", type=Path)
    migration_archive.add_argument("--schema", default=None,
                                   choices=["arena-v1-core-constitution", "arena-v2-github-brain"])

    tasks = sub.add_parser("tasks", help="Canonical task/checkpoint/lease control plane")
    tasks.add_argument("--brain-root", default=".", help="Repository root containing the canonical brain artifacts")
    tasks.add_argument("--brain-revision", default=None,
                       help="Pinned 40-character Git SHA; defaults to git rev-parse HEAD in --brain-root")
    task_sub = tasks.add_subparsers(dest="task_action", required=True)
    task_sub.add_parser("init", help="Create canonical task ledger after core init")
    task_apply = task_sub.add_parser("apply", help="Apply one canonical task command")
    task_apply.add_argument("json_file", type=Path)
    task_sub.add_parser("status", help="Show canonical task counts and stale tasks")
    task_packet = task_sub.add_parser("packet", help="Export one current task/checkpoint packet")
    task_packet.add_argument("task_id")
    task_sub.add_parser("verify", help="Replay canonical task ledger")
    task_sub.add_parser("repair-snapshot", help="Repair canonical task cache after audit")

    epistemic = sub.add_parser("epistemic", help="Epistemic registry and learning maturity ledger")
    epistemic_sub = epistemic.add_subparsers(dest="epistemic_action", required=True)
    epistemic_sub.add_parser("init", help="Create epistemic ledger after core init")
    epistemic_apply = epistemic_sub.add_parser("apply", help="Apply one epistemic command")
    epistemic_apply.add_argument("json_file", type=Path)
    epistemic_status = epistemic_sub.add_parser("status", help="Show maturity/unknown/review status")
    epistemic_status.add_argument("--now", default=None, help="Optional ISO timestamp for due-review calculation")
    epistemic_item = epistemic_sub.add_parser("item", help="Show one epistemic item")
    epistemic_item.add_argument("item_id")
    epistemic_sub.add_parser("verify", help="Replay epistemic ledger")
    epistemic_sub.add_parser("repair-snapshot", help="Repair epistemic cache after audit")

    governor = sub.add_parser("governor", help="Goal decomposition and bottleneck governor")
    governor_sub = governor.add_subparsers(dest="governor_action", required=True)
    governor_sub.add_parser("init", help="Create bottleneck governor ledger")
    governor_apply = governor_sub.add_parser("apply", help="Apply one decomposition/governor command")
    governor_apply.add_argument("json_file", type=Path)
    governor_recommend = governor_sub.add_parser("recommend", help="Recommend SELECT/WAIT/HOLD for one plan")
    governor_recommend.add_argument("plan_id")
    governor_commit = governor_sub.add_parser("commit-focus", help="Record the current recommendation with source heads")
    governor_commit.add_argument("plan_id")
    governor_sub.add_parser("status", help="Show decomposition counts")
    governor_sub.add_parser("verify", help="Replay bottleneck governor ledger")
    governor_sub.add_parser("repair-snapshot", help="Repair governor cache after audit")

    workcell = sub.add_parser("workcell", help="Four-seat replaceable AI Commons workcell")
    workcell.add_argument("--brain-root", default=".", help="Repository root containing canonical brain artifacts")
    workcell.add_argument("--brain-revision", default=None,
                          help="Pinned 40-character Git SHA; defaults to git rev-parse HEAD")
    workcell_sub = workcell.add_subparsers(dest="workcell_action", required=True)
    workcell_sub.add_parser("init", help="Create four-seat workcell ledger")
    workcell_apply = workcell_sub.add_parser("apply", help="Apply one workcell command")
    workcell_apply.add_argument("json_file", type=Path)
    workcell_status = workcell_sub.add_parser("status", help="Show one workcell session status")
    workcell_status.add_argument("session_id")
    workcell_packet = workcell_sub.add_parser("packet", help="Export one workcell + frozen Arena task packet")
    workcell_packet.add_argument("session_id")
    workcell_sub.add_parser("verify", help="Replay workcell ledger")
    workcell_sub.add_parser("repair-snapshot", help="Repair workcell cache after audit")
    args = parser.parse_args(argv)
    ledger = Ledger(args.home)
    try:
        if args.action == "workcell":
            service = FourSeatWorkcellService(args.home, args.brain_root, args.brain_revision)
            if args.workcell_action == "init":
                service.init()
                result = {"status": "WORKCELL_LEDGER_INITIALIZED", "home": str(service.ledger.home)}
            elif args.workcell_action == "apply":
                payload = json.loads(args.json_file.read_text(encoding="utf-8"))
                receipt = service.apply(payload)
                result = {"status": "WORKCELL_RECORDED", "event_count": receipt["event_count"], "head": receipt["head"]}
            elif args.workcell_action == "status":
                result = service.status(args.session_id)
            elif args.workcell_action == "packet":
                result = service.packet(args.session_id)
            elif args.workcell_action == "repair-snapshot":
                count, head = service.ledger.repair_snapshot()
                result = {"status": "WORKCELL_CACHE_REPAIRED", "event_count": count, "head": head}
            else:
                state, count, head = service.ledger.verify()
                result = {"status": "VALID_WORKCELL_LEDGER", "event_count": count, "head": head, "phase": state["phase"]}
        elif args.action == "governor":
            service = BottleneckService(args.home)
            if args.governor_action == "init":
                service.init()
                result = {"status": "GOVERNOR_LEDGER_INITIALIZED", "home": str(service.ledger.home)}
            elif args.governor_action == "apply":
                payload = json.loads(args.json_file.read_text(encoding="utf-8"))
                receipt = service.apply(payload)
                result = {"status": "GOVERNOR_RECORDED", "event_count": receipt["event_count"], "head": receipt["head"]}
            elif args.governor_action == "recommend":
                result = service.recommend(args.plan_id)
            elif args.governor_action == "commit-focus":
                result = service.commit_focus(args.plan_id)
            elif args.governor_action == "status":
                result = service.status()
            elif args.governor_action == "repair-snapshot":
                count, head = service.ledger.repair_snapshot()
                result = {"status": "GOVERNOR_CACHE_REPAIRED", "event_count": count, "head": head}
            else:
                state, count, head = service.ledger.verify()
                result = {"status": "VALID_GOVERNOR_LEDGER", "event_count": count, "head": head, "phase": state["phase"]}
        elif args.action == "epistemic":
            service = EpistemicService(args.home)
            if args.epistemic_action == "init":
                service.init()
                result = {"status": "EPISTEMIC_LEDGER_INITIALIZED", "home": str(service.ledger.home)}
            elif args.epistemic_action == "apply":
                payload = json.loads(args.json_file.read_text(encoding="utf-8"))
                receipt = service.apply(payload)
                result = {"status": "EPISTEMIC_RECORDED", "event_count": receipt["event_count"], "head": receipt["head"]}
            elif args.epistemic_action == "status":
                result = service.status(args.now)
            elif args.epistemic_action == "item":
                result = service.item(args.item_id)
            elif args.epistemic_action == "repair-snapshot":
                count, head = service.ledger.repair_snapshot()
                result = {"status": "EPISTEMIC_CACHE_REPAIRED", "event_count": count, "head": head}
            else:
                state, count, head = service.ledger.verify()
                result = {"status": "VALID_EPISTEMIC_LEDGER", "event_count": count, "head": head, "phase": state["phase"]}
        elif args.action == "tasks":
            service = TaskService(args.home, args.brain_root, args.brain_revision)
            if args.task_action == "init":
                service.init()
                result = {"status": "TASK_LEDGER_INITIALIZED", "home": str(service.ledger.home)}
            elif args.task_action == "apply":
                payload = json.loads(args.json_file.read_text(encoding="utf-8"))
                receipt = service.apply(payload)
                result = {"status": "TASK_RECORDED", "event_count": receipt["event_count"], "head": receipt["head"]}
                if payload.get("type") == "create_task":
                    task_id = payload["data"]["id"]
                    result["task"] = receipt["state"]["tasks"][task_id]
            elif args.task_action == "status":
                result = service.status()
            elif args.task_action == "packet":
                result = service.packet(args.task_id)
            elif args.task_action == "repair-snapshot":
                count, head = service.ledger.repair_snapshot()
                result = {"status": "TASK_CACHE_REPAIRED", "event_count": count, "head": head}
            else:
                state, count, head = service.ledger.verify()
                result = {"status": "VALID_TASK_LEDGER", "event_count": count, "head": head, "phase": state["phase"]}
        elif args.action == "arena-migration":
            if args.migration_action == "verify":
                result = verify_legacy_arena(args.legacy_home, args.schema)
            else:
                result = archive_legacy_arena(args.legacy_home, args.archive_root, args.schema)
        elif args.action == "arena":
            service = ArenaService(args.home, args.brain_root, args.brain_revision)
            if args.arena_action == "init":
                service.init()
                result = {"status": "SHADOW_INITIALIZED", "home": str(service.ledger.home)}
            elif args.arena_action == "apply":
                payload = json.loads(args.json_file.read_text(encoding="utf-8"))
                receipt = service.apply(payload)
                result = {"status": "SHADOW_RECORDED", "event_count": receipt["event_count"], "head": receipt["head"]}
                if payload.get("type") == "open_task":
                    task_id = payload["data"]["id"]
                    task = receipt["state"]["tasks"][task_id]
                    result["task_fingerprint"] = task["fingerprint"]
                    result["brain_revision"] = task["brain_revision"]
                    result["brain_fingerprint"] = task["brain_fingerprint"]
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
                brain = service.status()
                result = {"status": "VALID_SHADOW_LEDGER", "event_count": count, "head": head,
                          "phase": state["phase"], "brain_revision": brain["brain_revision"],
                          "brain_fingerprint": brain["brain_fingerprint"]}
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
