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
        if not isinstance(authority, str) or not authority.strip():
            fail(errors, "active task acceptance_authority is missing")
        elif task.get("holder") == authority or authority.strip().lower() in {"builder", "builder/implementer"}:
            fail(errors, "active task holder/Builder cannot self-approve")
        if current.get("active_workstream") == "OWNER_DIRECTED_LEARNING" and task.get("change_class") != "D":
            fail(errors, "learning workstream must route to Class D study task")
        # No Owner-approved Class D delegate exists in this candidate scope.
        if active_id == "BUDDHIST-A173" and authority != "OWNER":
            fail(errors, "A173 acceptance authority lacks verified Owner designation")
        if task.get("next_action") and current.get("next_checkpoint") != task.get("next_action"):
            fail(errors, "current.next_checkpoint does not match active task.next_action")
        if active_id == "BUDDHIST-A173":
            # No branch mutation is authorized by this Class S routing candidate.
            if task.get("branch") is not None:
                fail(errors, "A173 execution branch requires separate Owner-authorized Class D binding")
            if task.get("branch_binding") != "NONE_NO_EXECUTION_REF_UNTIL_OWNER_APPROVED_ASSIGNMENT":
                fail(errors, "A173 unbound routing policy was changed without authorized binding")
            checkpoint = task.get("learning_checkpoint")
            expected = {
                "current_checkpoint_id": "A173",
                "checkpoint_acceptance": "NOT_CURRENT",
                "last_accepted_checkpoint_id": "A172",
                "last_accepted_checkpoint_ref": "docs/learning/BUDDHIST_THOUGHT_CHECKPOINT_A172_20261005.md",
                "acceptance_receipt_ref": None,
            }
            if not isinstance(checkpoint, dict):
                fail(errors, "A173 structured checkpoint state missing")
            else:
                for key, value in expected.items():
                    if checkpoint.get(key) != value:
                        fail(errors, f"A173 checkpoint {key} cannot claim acceptance without Owner receipt")
                checkpoint_ref = checkpoint.get("last_accepted_checkpoint_ref")
                if checkpoint_ref and not (ROOT / checkpoint_ref).is_file():
                    fail(errors, "A172 accepted checkpoint reference is missing")
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


    # No static repository field authenticates an external Owner comment or merge.
    # A post-merge Class S closure needs a separately reviewed receipt-bound change.
    routing = tasks.get("ARCH-BUDDHIST-A173-ROUTING-V1")
    if active_id == "BUDDHIST-A173" and routing is None:
        fail(errors, "A173 routing Class S control task missing")
    if routing is not None:
        gate = routing.get("material_findings_owner_gate")
        witness = routing.get("post_merge_witness")
        if routing.get("change_class") != "S" or routing.get("acceptance_authority") != "OWNER":
            fail(errors, "routing Class S authority mismatch")
        if routing.get("holder") == routing.get("acceptance_authority"):
            fail(errors, "routing Builder cannot be Owner acceptance authority")
        if routing.get("candidate_gate_phase") != "PRE_MERGE_UNACCEPTED_SNAPSHOT":
            fail(errors, "routing Class S candidate phase is not pending")
        if routing.get("status") != "IN_PROGRESS":
            fail(errors, "routing Class S closure requires separate protected evidence")
        if not isinstance(gate, dict) or gate.get("owner_acceptance") != "NOT_GRANTED" or gate.get("status") != "OWNER_PER_FINDING_DISPOSITION_PENDING":
            fail(errors, "routing Class S approval cannot be self-asserted in candidate snapshot")
        if isinstance(gate, dict):
            keys = gate.get("provisional_intake_keys")
            if not isinstance(keys, list) or len(keys) != 8 or len(set(keys)) != 8:
                fail(errors, "routing Class S eight historical material keys must remain open")
            if "OWNER_REPORTED_ORIGINALS_LOST" not in str(gate.get("originals_or_attestation", "")):
                fail(errors, "routing Class S F3 loss limitation cannot be waived")
            if "6076001277" not in str(gate.get("gate_3_build_before_task_authorize", "")):
                fail(errors, "routing Class S historic Gate 3 receipt reference missing")
        if (not isinstance(witness, dict)
                or witness.get("witness_status") != "NOT_CLAIMED_BY_THIS_CANDIDATE"
                or witness.get("witness_holder") is not None
                or witness.get("closure_holder") is not None
                or witness.get("builder_self_certification_allowed") is not False):
            fail(errors, "routing Class S witness/closure cannot be self-certified")
        handoff = routing.get("handoff_ref")
        if not handoff or not (ROOT / handoff).is_file():
            fail(errors, "routing Class S handoff absent")
        else:
            body = (ROOT / handoff).read_text(encoding="utf-8")
            if f"**TASK_ID:** {routing['task_id']}" not in body or "## NOT DONE" not in body:
                fail(errors, "routing Class S handoff contract missing")
            if "## NEXT ACTION\n" + str(routing.get("next_action")) not in body:
                fail(errors, "routing Class S handoff NEXT ACTION mismatch")

    if active_id == "BUDDHIST-A173" and active_id in tasks:
        ref = tasks[active_id].get("handoff_ref")
        if ref and (ROOT / ref).is_file():
            body = (ROOT / ref).read_text(encoding="utf-8")
            expected_handoff = {
                "LAST_ACCEPTED_CHECKPOINT": "A172",
                "CURRENT_CHECKPOINT": "A173",
                "CHECKPOINT_ACCEPTANCE": "NOT_CURRENT",
                "CHECKPOINT_ACCEPTANCE_RECEIPT": "NONE",
            }
            for key, value in expected_handoff.items():
                matches = re.findall(rf"^\*\*{key}:\*\*\s*(\S.*?)\s*$", body, flags=re.MULTILINE)
                if matches != [value]:
                    fail(errors, f"A173 handoff {key} disagrees with unaccepted checkpoint")
            if re.search(r"\bA173\s+(?:checkpoint\s+)?(?:is\s+)?(?:COMPLETED|ACCEPTED|VERIFIED)\b", body, re.IGNORECASE):
                fail(errors, "A173 handoff falsely claims checkpoint completion")

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
