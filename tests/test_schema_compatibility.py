import json
import tempfile
import unittest
from pathlib import Path

from minhtri.bottleneck import GOVERNOR_FIELDS
from minhtri.core import ALLOWED_FIELDS, GateError, Ledger, canonical, digest, initial_state
from minhtri.core_migration import verify_legacy_core_family_migration
from minhtri.epistemic import EPISTEMIC_FIELDS
from minhtri.tasking import TASK_FIELDS
from minhtri.workcell import WORKCELL_FIELDS


class SchemaCompatibilityTests(unittest.TestCase):
    def test_r4_5_mutable_schema_tripwires_are_explicit(self):
        self.assertEqual(ALLOWED_FIELDS["register_provider"], {"id", "name", "kind", "family_id"})
        self.assertEqual(TASK_FIELDS, {
            "create_task": {
                "id", "goal_id", "domain_id", "brain_revision", "brain_fingerprint",
                "architecture_law_sha256", "bootstrap_sha256", "core_state_head_at_open",
                "brief", "acceptance", "allowed_evidence_ids", "risk_class",
            },
            "acknowledge_continuation": {"id", "task_id", "worker_id", "continuation_fingerprint"},
            "acquire_lease": {
                "task_id", "worker_id", "lease_id", "expires_at", "expected_checkpoint_seq",
                "continuation_ack_id",
            },
            "checkpoint_task": {
                "task_id", "worker_id", "lease_id", "expected_checkpoint_seq",
                "summary", "artifact_refs", "evidence_ids", "next_action",
            },
            "handoff_task": {
                "task_id", "worker_id", "lease_id", "expected_checkpoint_seq", "decisions",
                "unknowns", "blockers", "verification", "scope", "limitations",
            },
            "release_lease": {"task_id", "worker_id", "lease_id", "reason"},
            "complete_task": {
                "task_id", "worker_id", "lease_id", "expected_checkpoint_seq",
                "completion_summary", "decisions", "unknowns", "blockers", "verification",
                "scope", "limitations",
            },
        })
        self.assertEqual(set(EPISTEMIC_FIELDS), {
            "register_item", "support_item", "demonstrate_understanding", "link_prediction",
            "record_application", "record_validation", "link_critique", "reopen_item",
            "revalidate_item", "register_unknown", "resolve_unknown", "reopen_unknown",
            "record_provider_error",
        })
        self.assertEqual(GOVERNOR_FIELDS, {
            "create_plan": {
                "id", "goal_id", "domain_id", "target_state", "success_conditions", "owner_constraints",
            },
            "add_component": {
                "id", "plan_id", "name", "supports_conditions", "dependency_ids", "target_role",
                "gap_kind", "owner_impact", "decision_sensitivity", "information_gain",
                "cost_band", "time_band", "risk_band", "reversibility", "epistemic_item_ids",
                "unknown_ids", "allowed_evidence_ids", "leverage_hypothesis",
                "disconfirming_condition", "next_unit_type", "next_unit", "acceptance",
            },
            "set_component_status": {"component_id", "status", "reason", "evidence_ids"},
            "record_focus": {
                "plan_id", "decision", "component_id", "reason", "core_head", "epistemic_head",
                "plan_head_before", "candidate_ids", "selection_method", "selection_snapshot_hash",
            },
        })
        self.assertEqual(WORKCELL_FIELDS, {
            "open_session": {
                "id", "arena_task_id", "task_fingerprint", "brain_revision", "brain_fingerprint",
                "architecture_law_sha256", "bootstrap_sha256",
            },
            "assign_slot": {"session_id", "seat_id", "participant_id", "family_id", "model", "version"},
            "replace_slot": {
                "session_id", "seat_id", "old_participant_id", "participant_id", "family_id",
                "model", "version", "reason",
            },
            "submit_blind": {
                "session_id", "seat_id", "participant_id", "contribution_ref", "contribution_sha256",
            },
            "freeze_blind": {"session_id"},
            "reveal": {"session_id"},
        })

    def test_legacy_core_provider_schema_migrates_without_rewriting_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "brain"
            home.mkdir(parents=True)
            commands = [
                {
                    "type": "register_domain",
                    "data": {
                        "id": "media", "name": "Media", "risk_class": "NORMAL",
                        "measurement_contract": "Legacy measurement",
                    },
                },
                {
                    "type": "register_provider",
                    "data": {"id": "maker", "name": "Maker", "kind": "MODEL"},
                },
                {
                    "type": "register_provider",
                    "data": {"id": "critic", "name": "Critic", "kind": "MODEL"},
                },
            ]
            ats = [
                "2026-09-29T06:00:00Z",
                "2026-09-29T06:01:00Z",
                "2026-09-29T06:02:00Z",
            ]
            previous = "0" * 64
            lines = []
            for seq, (cmd, at) in enumerate(zip(commands, ats), start=1):
                body = {"seq": seq, "prev": previous, "at": at, "command": cmd}
                event = {**body, "hash": digest(body)}
                previous = event["hash"]
                lines.append(canonical(event).decode("utf-8"))
            events = home / "events.jsonl"
            events.write_text("\n".join(lines) + "\n", encoding="utf-8")

            legacy_state = initial_state()
            legacy_state["domains"]["media"] = commands[0]["data"].copy()
            legacy_state["providers"]["maker"] = commands[1]["data"].copy()
            legacy_state["providers"]["critic"] = commands[2]["data"].copy()
            snapshot = {
                "event_count": len(commands),
                "head": previous,
                "state": legacy_state,
            }
            state_file = home / "state.json"
            state_file.write_bytes(canonical(snapshot) + b"\n")

            before_events = events.read_bytes()
            before_state = state_file.read_bytes()

            with self.assertRaisesRegex(GateError, "Missing: family_id"):
                Ledger(home).verify()

            report = verify_legacy_core_family_migration(home)
            self.assertEqual(report["status"], "LEGACY_CORE_PROVIDER_FAMILY_MIGRATION_VERIFIED")
            self.assertEqual(report["event_count"], 3)
            self.assertEqual(report["head"], previous)
            self.assertEqual(report["history_policy"], "READ_ONLY_DO_NOT_REWRITE")
            self.assertEqual(events.read_bytes(), before_events)
            self.assertEqual(state_file.read_bytes(), before_state)


if __name__ == "__main__":
    unittest.main()
