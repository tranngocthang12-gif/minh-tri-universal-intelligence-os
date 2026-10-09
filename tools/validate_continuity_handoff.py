#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIVE_STATUSES = {"IN_PROGRESS", "BLOCKED", "REPORTED", "REVIEWED_REVISE", "STALE"}

def load_json(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def fail(errors, msg):
    errors.append(msg)

def main():
    errors = []
    current = load_json("state/current.yaml")
    registry = load_json("state/tasks.yaml")
    tasks = {t["task_id"]: t for t in registry["tasks"]}

    active_id = current.get("active_task_id")
    if not active_id:
        fail(errors, "current.active_task_id missing")
    elif active_id not in tasks:
        fail(errors, f"active_task_id not found in registry: {active_id}")
    else:
        task = tasks[active_id]
        if task.get("status") not in ACTIVE_STATUSES:
            fail(errors, f"active task status is not active: {task.get('status')}")
        if task.get("change_class") not in {"F", "S", "D", "O"}:
            fail(errors, "active task change_class is not authorized")
        authority = task.get("acceptance_authority")
        if not isinstance(authority, str) or not authority.strip() or authority.strip().lower() in {"builder", "builder/implementer"}:
            fail(errors, "active task acceptance_authority is missing or self-approving")
        if task.get("next_action") and current.get("next_checkpoint") != task.get("next_action"):
            fail(errors, "current.next_checkpoint does not match active task.next_action")
        if (
            active_id == "BUDDHIST-A173"
            and task.get("branch_binding") == "NONE_NO_EXECUTION_REF_UNTIL_OWNER_APPROVED_ASSIGNMENT"
            and task.get("branch") is not None
        ):
            fail(errors, "active A173 has an execution branch but is marked unbound")
        for field in ("scope", "base_sha", "result_ref", "handoff_ref", "next_action"):
            if task.get(field) in (None, "", []):
                fail(errors, f"active task missing {field}")
        if task.get("status") in {"BLOCKED", "STALE"} and not task.get("blocker"):
            fail(errors, "blocked/stale active task missing blocker")
        handoff_ref = task.get("handoff_ref")
        if handoff_ref:
            handoff_path = ROOT / handoff_ref
            if not handoff_path.exists():
                fail(errors, f"handoff_ref missing file: {handoff_ref}")
            else:
                text = handoff_path.read_text(encoding="utf-8")
                m = re.search(r"\*\*TASK_ID:\*\*\s*([^\s]+)", text)
                if not m:
                    fail(errors, "handoff missing TASK_ID")
                elif m.group(1).strip() != active_id:
                    fail(errors, f"handoff TASK_ID mismatch: {m.group(1).strip()} != {active_id}")
                for heading in ("## DONE", "## NOT DONE", "## NEXT ACTION", "## REQUIRED GATES"):
                    if heading not in text:
                        fail(errors, f"handoff missing heading {heading}")
                sections = text.splitlines()
                next_headings = [i for i, line in enumerate(sections) if line.strip() == "## NEXT ACTION"]
                if len(next_headings) != 1:
                    fail(errors, "active handoff must have exactly one NEXT ACTION heading")
                else:
                    following = sections[next_headings[0] + 1:]
                    first_action = next((line.strip() for line in following if line.strip()), None)
                    if first_action is None or first_action.startswith("## "):
                        fail(errors, "active handoff NEXT ACTION is empty")
                    elif first_action != task.get("next_action"):
                        fail(errors, "active handoff NEXT ACTION does not match task.next_action")

    for field in ("current_architecture", "role_bootstrap"):
        ref = current.get(field)
        if not ref or not (ROOT / ref).exists():
            fail(errors, f"current {field} missing/unreadable: {ref}")

    entry = ROOT / "docs/vnext/continuity/RECOVERY_ENTRYPOINT_V1.md"
    if not entry.exists():
        fail(errors, "recovery entrypoint missing")
    else:
        et = entry.read_text(encoding="utf-8")
        for needle in ("state/current.yaml", "state/tasks.yaml", "active_task_id", "handoff_ref", "next_action"):
            if needle not in et:
                fail(errors, f"recovery entrypoint missing route token: {needle}")

    for t in registry["tasks"]:
        if t.get("status") in {"BLOCKED", "STALE"}:
            if not t.get("next_action"):
                fail(errors, f"{t['task_id']} blocked/stale missing next_action")
            if not t.get("handoff_ref") and t["task_id"].startswith("ARCH-"):
                fail(errors, f"{t['task_id']} blocked/stale architecture task missing handoff_ref")

    if errors:
        print("CONTINUITY_HANDOFF_CORE_V1_FAIL")
        for e in errors:
            print(f"- {e}")
        return 1
    print("CONTINUITY_HANDOFF_CORE_V1_PASS")
    print(f"active_task_id={active_id}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
