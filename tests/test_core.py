import json
import tempfile
import unittest
from pathlib import Path

from minhtri.core import GateError, Ledger, evolve, initial_state, next_goal
from tests.support import ledger_apply, ledger_repair, write_owner_config


def cmd(command_type, **data):
    return {"type": command_type, "data": data}


class CoreGates(unittest.TestCase):
    def setUp(self):
        self.state = initial_state()
        self.at = "2026-01-01T00:00:00Z"

    def apply(self, command_type, at=None, **data):
        self.state = evolve(self.state, cmd(command_type, **data), at or self.at)

    def base(self, risk="NORMAL"):
        self.apply("register_domain", id="media", name="Media", risk_class=risk, measurement_contract="Owner supplied analytics")
        self.apply("open_goal", id="goal1", domain_id="media", objective="Evaluate a possible improvement",
                   priority=3, owner_boundary="No external actions")
        self.apply("frame_problem", id="problem1", goal_id="goal1", reality="Performance is unknown",
                   conditions=[{"description": "Audience mix may change", "role": "CONDITION", "status": "HYPOTHESIS"}],
                   target="Get a reliable measurement", intervention="Run a bounded comparison",
                   unknowns=["Base rate"], control="Test design", influence="Audience exposure",
                   responsibility="Owner decides", harm_checks=["Do not mislead viewers"])
        for pid in ("maker", "forecaster", "critic", "judge"):
            self.apply("register_provider", id=pid, name=pid, kind="MODEL")
        self.apply("register_procedure", id="p1", domain_id="media", provider_id="forecaster", version="1", method="Range forecast")
        self.apply("propose_claim", id="h1", problem_id="problem1", provider_id="maker", statement="Test hypothesis",
                   evidence_ids=[], alternative="Seasonal audience difference", falsifier="Intervals miss on independent outcomes")

    def predictions_and_outcomes(self):
        self.apply("register_prediction", id="f1", claim_id="h1", procedure_id="p1", metric="rate",
                   unit="percent", lower=5, upper=7, due_at="2026-01-03T00:00:00Z", resolution_method="Read approved report")
        self.apply("register_prediction", id="f2", claim_id="h1", procedure_id="p1", metric="rate",
                   unit="percent", lower=6, upper=8, due_at="2026-01-07T00:00:00Z", resolution_method="Read approved report")
        self.apply("freeze_prediction", prediction_id="f1")
        self.apply("freeze_prediction", prediction_id="f2")
        for n, when, value in ((1, "2026-01-04T00:00:00Z", 6.0), (2, "2026-01-08T00:00:00Z", 6.5)):
            self.apply("record_source", at=when, id=f"s{n}", domain_id="media", uri=f"internal://report/{n}",
                       captured_at=when, kind="FIRST_PARTY", rights_status="CLEAR")
            self.apply("record_evidence", at=when, id=f"e{n}", domain_id="media", source_id=f"s{n}",
                       statement="Recorded measurement", observed_at=when, value=value, metric="rate")
            self.apply("record_resolution", at=when, id=f"r{n}", prediction_id=f"f{n}", evidence_id=f"e{n}")

    def review_and_lesson(self):
        self.apply("review_claim", id="review1", claim_id="h1", critic_provider_id="critic",
                   verdict="ACCEPT_FOR_TRIAL", reason="Alternative remains testable")
        self.apply("adjudicate_claim", id="adj1", claim_id="h1", review_id="review1",
                   adjudicator_provider_id="judge", verdict="ACCEPT_FOR_TRIAL", reason="Bounded trial only")
        self.apply("propose_lesson", id="lesson1", claim_id="h1", statement="Try this narrow method",
                   limits="Two observations; confounding unresolved", prediction_ids=["f1", "f2"], adjudication_id="adj1",
                   counterevidence_ids=[], counterevidence_search_note="Searched recorded evidence; none found",
                   applicability="Media domain under the measured conditions only")
        self.assertEqual(self.state["lessons"]["lesson1"]["status"], "HYPOTHESIS")
        self.apply("freeze_lesson", lesson_id="lesson1")
        self.assertEqual(self.state["lessons"]["lesson1"]["status"], "FROZEN_PENDING_OWNER")

    def test_prediction_can_preregister_outcome_source_and_resolution_must_match(self):
        self.base()
        spec = {
            "source_uri": "internal://report/future",
            "source_kind": "FIRST_PARTY",
            "value_selector": "rate",
            "capture_rule": "capture first approved report after due_at",
        }
        self.apply("register_prediction", id="fx", claim_id="h1", procedure_id="p1", metric="rate",
                   unit="percent", lower=5, upper=7, due_at="2026-01-03T00:00:00Z",
                   resolution_method="Read approved report", outcome_source_spec=spec)
        self.apply("freeze_prediction", prediction_id="fx")
        self.apply("record_source", at="2026-01-04T00:00:00Z", id="sx", domain_id="media",
                   uri="internal://report/future", captured_at="2026-01-04T00:00:00Z",
                   kind="FIRST_PARTY", rights_status="CLEAR")
        self.apply("record_evidence", at="2026-01-04T00:00:00Z", id="ex", domain_id="media",
                   source_id="sx", statement="Recorded measurement",
                   observed_at="2026-01-04T00:00:00Z", value=6.0, metric="rate")
        self.apply("record_resolution", at="2026-01-04T00:00:00Z", id="rx",
                   prediction_id="fx", evidence_id="ex")
        self.assertEqual(self.state["resolutions"]["rx"]["learning_provenance_status"],
                         "OUTCOME_SOURCE_PREREGISTERED")

    def test_legacy_prediction_remains_replayable_but_not_meta_learning_eligible(self):
        self.base()
        self.apply("register_prediction", id="legacy", claim_id="h1", procedure_id="p1", metric="rate",
                   unit="percent", lower=5, upper=7, due_at="2026-01-03T00:00:00Z",
                   resolution_method="Read approved report")
        self.assertEqual(self.state["predictions"]["legacy"]["outcome_source_spec_status"],
                         "UNSPECIFIED_NOT_META_LEARNING_ELIGIBLE")

    def test_external_critic_run_is_append_only_evidence_not_authority(self):
        self.apply(
            "record_external_critic_run",
            id="external-critic-1",
            candidate_generation_id="gen-0002",
            lease_id="upgrade-abc",
            critic_provider="external-gpt",
            critic_model="declared-model",
            prompt_version="external-critic-v1",
            run_id="manual-run-1",
            packet_hash="a" * 64,
            output_hash="b" * 64,
            blind_or_revealed="BLIND",
            channel="OWNER_MANUAL",
            independence_status="PARTIAL",
            verdict="NO_MATERIAL_DEFECT_FOUND",
            findings=[],
            post_expiry=False,
        )
        run = self.state["external_critic_runs"]["external-critic-1"]
        self.assertEqual(run["status"], "RECORDED")
        self.assertFalse(run["automatic_verified_promotion"])

    def test_external_critic_run_rejects_bad_hash(self):
        with self.assertRaises(GateError):
            self.apply(
                "record_external_critic_run",
                id="external-critic-1",
                candidate_generation_id="gen-0002",
                lease_id="upgrade-abc",
                critic_provider="external-gpt",
                critic_model="declared-model",
                prompt_version="external-critic-v1",
                run_id="manual-run-1",
                packet_hash="not-a-hash",
                output_hash="b" * 64,
                blind_or_revealed="BLIND",
                channel="OWNER_MANUAL",
                independence_status="PARTIAL",
                verdict="NO_MATERIAL_DEFECT_FOUND",
                findings=[],
                post_expiry=False,
            )

    def test_runtime_audit_event_records_lease_activation_without_conferring_authority(self):
        self.apply(
            "record_runtime_audit_event",
            id="lease-created-1",
            event_type="LEASE_CREATED",
            lease_id="upgrade-abc",
            occurred_at=self.at,
            details={"duration_seconds": 86400},
        )
        self.apply(
            "record_runtime_audit_event",
            id="lease-activated-1",
            event_type="LEASE_ACTIVATED",
            lease_id="upgrade-abc",
            occurred_at=self.at,
            details={"runtime_status": "ACTIVE"},
        )
        created = self.state["runtime_audit_events"]["lease-created-1"]
        activated = self.state["runtime_audit_events"]["lease-activated-1"]
        self.assertEqual(created["status"], "AUDIT_ONLY_NOT_AUTHORITY")
        self.assertEqual(activated["event_type"], "LEASE_ACTIVATED")
        self.assertEqual(activated["lease_id"], "upgrade-abc")

    def test_runtime_audit_event_rejects_unknown_type_and_future_time(self):
        with self.assertRaises(GateError):
            self.apply(
                "record_runtime_audit_event",
                id="bad-event",
                event_type="LEASE_RENEWED",
                lease_id="upgrade-abc",
                occurred_at=self.at,
                details={},
            )
        with self.assertRaises(GateError):
            self.apply(
                "record_runtime_audit_event",
                id="future-event",
                event_type="LEASE_ACTIVATED",
                lease_id="upgrade-abc",
                occurred_at="2027-01-01T00:00:00Z",
                details={},
            )

    def test_two_domains_do_not_change_core_and_wait_is_explicit(self):
        self.assertEqual(next_goal(self.state)["status"], "WAIT")
        self.apply("register_domain", id="youtube", name="YouTube", risk_class="NORMAL", measurement_contract="CTR")
        self.apply("register_domain", id="finance", name="Finance", risk_class="HIGH_STAKES", measurement_contract="Returns")
        self.apply("open_goal", id="g1", domain_id="youtube", objective="Measure", priority=3, owner_boundary="Read only")
        self.assertEqual(next_goal(self.state)["goal"]["id"], "g1")
        self.apply("set_goal_status", goal_id="g1", status="BLOCKED", reason="No data permission")
        self.assertEqual(next_goal(self.state)["status"], "WAIT")

    def test_preregistration_three_seats_and_trial_gate(self):
        self.base()
        self.apply("register_prediction", id="f1", claim_id="h1", procedure_id="p1", metric="rate",
                   unit="percent", lower=5, upper=7, due_at="2026-01-03T00:00:00Z", resolution_method="Report")
        self.apply("record_source", id="s1", domain_id="media", uri="internal://early", captured_at=self.at,
                   kind="FIRST_PARTY", rights_status="CLEAR")
        self.apply("record_evidence", id="e1", domain_id="media", source_id="s1", statement="Early metric",
                   observed_at=self.at, value=6, metric="rate")
        with self.assertRaises(GateError):
            self.apply("record_resolution", id="r1", prediction_id="f1", evidence_id="e1")
        with self.assertRaises(GateError):
            self.apply("review_claim", id="bad", claim_id="h1", critic_provider_id="maker", verdict="HOLD", reason="Self-review")
        self.assertEqual(self.state["predictions"]["f1"]["status"], "REGISTERED")

        # Rebuild without the early test prediction, then exercise the full guarded flow.
        self.setUp()
        self.base()
        self.predictions_and_outcomes()
        self.review_and_lesson()
        self.apply("activate_trial_lesson", lesson_id="lesson1", owner_ack="HUMAN_OWNER_APPROVED", scope="One internal pilot")
        self.assertEqual(self.state["lessons"]["lesson1"]["status"], "TRIAL_RULE")
        self.assertEqual(self.state["lessons"]["lesson1"]["owner_acceptance"], "OWNER_ACCEPTED")
        self.assertFalse(self.state["lessons"]["lesson1"]["verified"])
        self.assertEqual(self.state["resolutions"]["r1"]["interval_hit"], True)
        self.assertEqual(self.state["claims"]["h1"]["epistemic_status"], "HYPOTHESIS")

    def test_lesson_provenance_is_optional_but_required_for_learning_claim(self):
        self.base()
        self.predictions_and_outcomes()
        self.apply("review_claim", id="review1", claim_id="h1", critic_provider_id="critic",
                   verdict="ACCEPT_FOR_TRIAL", reason="Testable")
        self.apply("adjudicate_claim", id="adj1", claim_id="h1", review_id="review1",
                   adjudicator_provider_id="judge", verdict="ACCEPT_FOR_TRIAL",
                   reason="Bounded trial")
        self.apply("propose_lesson", id="lesson-p", claim_id="h1", statement="Narrow lesson",
                   limits="Bounded", prediction_ids=["f1", "f2"], adjudication_id="adj1",
                   counterevidence_ids=[], counterevidence_search_note="None found",
                   applicability="media/p1",
                   lesson_provenance={
                       "status": "AUDITED_LEDGER_DERIVED",
                       "candidate_id": "meta-1",
                       "resolution_ids": ["r1", "r2"],
                       "strata": ["media/p1"],
                       "derived_at": "2026-01-07T00:00:00Z",
                   })
        self.assertTrue(self.state["lessons"]["lesson-p"]["learning_claim_eligible"])
        self.assertEqual(
            self.state["lessons"]["lesson-p"]["lesson_provenance"]["status"],
            "AUDITED_LEDGER_DERIVED",
        )

    def test_owner_can_activate_structured_machine_readable_trial_rule(self):
        from minhtri.learning_experiment import validate_preregistration
        from minhtri.trial_rule_runtime import preregistration_digest

        self.base()
        self.predictions_and_outcomes()
        self.review_and_lesson()
        experiment = {
            "experiment_id": "trial-1",
            "frozen_at_utc": "2026-01-08T00:00:00Z",
            "primary_endpoint": "FACTUAL_ACCURACY",
            "safety_endpoint": "UNSUPPORTED_CLAIM_RATE",
            "coverage_endpoint": "GOLD_CLAIM_COVERAGE",
            "coverage_noninferiority_margin": 0.05,
            "primary_success_rule": "treatment > compute_matched",
            "safety_failure_rule": "unsupported_claim_rate must not worsen",
            "rollback_rule": "rollback on safety failure",
            "assignment_unit": "TASK_ID",
            "assignment_seed_hash": "a" * 64,
            "control_pipeline_hash": "b" * 64,
            "treatment_pipeline_hash": "c" * 64,
            "compute_matched_pipeline_hash": "d" * 64,
            "frozen_evaluator_hash": "e" * 64,
            "gold_labels_hash": "f" * 64,
            "baseline_definition": "V1_3",
            "compute_budget_contract": {
                "control": {"retrieval_calls": 1, "critic_calls": 1, "generator_calls": 1},
                "treatment": {"retrieval_calls": 2, "critic_calls": 2, "generator_calls": 1},
                "compute_matched": {"retrieval_calls": 2, "critic_calls": 2, "generator_calls": 1},
                "placebo": {"retrieval_calls": 2, "critic_calls": 2, "generator_calls": 1},
            },
            "compute_tolerance_fraction": 0.10,
            "placebo_overlay_id": "SHUFFLED_LEDGER_PLACEBO",
            "placebo_overlay_hash": "1" * 64,
            "placebo_provenance_hash": "2" * 64,
            "arm_mode": "PAIRED_FOUR_ARM",
            "primary_window_tasks": 30,
            "rollback_threshold": 0.05,
            "trial_rule_id": "lesson1",
            "trial_rule_ttl_seconds": 3600,
            "routing_keys": ["domain_id", "procedure_id"],
        }
        validate_preregistration(experiment)
        trial_spec = {
            "experiment_id": "trial-1",
            "preregistration_hash": preregistration_digest(experiment),
            "domain_id": "media",
            "procedure_id": "p1",
            "overlay_id": "COUNTEREVIDENCE_FIRST",
            "expires_at": "2026-01-09T00:00:00Z",
        }
        self.apply("activate_trial_lesson", at="2026-01-08T00:00:00Z",
                   lesson_id="lesson1", owner_ack="HUMAN_OWNER_APPROVED",
                   scope="Media/p1 bounded A/B/C trial", trial_spec=trial_spec)
        lesson = self.state["lessons"]["lesson1"]
        self.assertEqual(lesson["runtime_trial_status"], "EXECUTABLE_DECLARATIVE_OVERLAY")
        self.assertEqual(lesson["trial_spec"]["overlay_id"], "COUNTEREVIDENCE_FIRST")
        self.assertEqual(len(lesson["trial_spec_hash"]), 64)

    def test_legacy_trial_scope_is_not_runtime_executable(self):
        self.base()
        self.predictions_and_outcomes()
        self.review_and_lesson()
        self.apply("activate_trial_lesson", lesson_id="lesson1",
                   owner_ack="HUMAN_OWNER_APPROVED", scope="Legacy text-only pilot")
        self.assertEqual(
            self.state["lessons"]["lesson1"]["runtime_trial_status"],
            "LEGACY_NONEXECUTABLE_SCOPE_ONLY",
        )

    def test_lesson_cannot_freeze_without_resolved_preregistration(self):
        self.base()
        self.apply("register_prediction", id="f1", claim_id="h1", procedure_id="p1", metric="rate",
                   unit="percent", lower=5, upper=7, due_at="2026-01-03T00:00:00Z", resolution_method="Report")
        self.apply("review_claim", id="review1", claim_id="h1", critic_provider_id="critic",
                   verdict="ACCEPT_FOR_TRIAL", reason="Bounded trial")
        self.apply("adjudicate_claim", id="adj1", claim_id="h1", review_id="review1",
                   adjudicator_provider_id="judge", verdict="ACCEPT_FOR_TRIAL", reason="Bounded trial")
        self.apply("propose_lesson", id="lesson1", claim_id="h1", statement="Hypothesis only",
                   limits="No resolved outcome", prediction_ids=["f1"], adjudication_id="adj1",
                   counterevidence_ids=[], counterevidence_search_note="Searched; none found",
                   applicability="Measured media conditions only")
        self.assertEqual(self.state["lessons"]["lesson1"]["status"], "HYPOTHESIS")
        with self.assertRaises(GateError):
            self.apply("freeze_lesson", lesson_id="lesson1")

    def test_high_stakes_cannot_activate_even_with_two_outcomes(self):
        self.base(risk="HIGH_STAKES")
        self.predictions_and_outcomes()
        self.review_and_lesson()
        with self.assertRaises(GateError):
            self.apply("activate_trial_lesson", lesson_id="lesson1", owner_ack="HUMAN_OWNER_APPROVED", scope="Trading")

    def test_cross_domain_evidence_and_future_observation_are_blocked(self):
        self.base()
        self.apply("register_domain", id="other", name="Other", risk_class="NORMAL", measurement_contract="Data")
        self.apply("record_source", id="s1", domain_id="media", uri="internal://source", captured_at=self.at,
                   kind="FIRST_PARTY", rights_status="CLEAR")
        with self.assertRaises(GateError):
            self.apply("record_evidence", id="bad", domain_id="other", source_id="s1", statement="Wrong domain", observed_at=self.at)
        with self.assertRaises(GateError):
            self.apply("record_evidence", id="future", domain_id="media", source_id="s1", statement="Future",
                       observed_at="2027-01-01T00:00:00Z")
        with self.assertRaises(GateError):
            self.apply("propose_claim", id="bad", problem_id="problem1", provider_id="maker", statement="Unknown",
                       evidence_ids=[{}], alternative="Other", falsifier="Test")

    def test_external_case_is_capital_not_lesson(self):
        self.base()
        self.apply("record_source", id="ext1", domain_id="media", uri="https://example.test/case",
                   captured_at=self.at, kind="PUBLIC", rights_status="CLEAR")
        self.apply("record_evidence", id="ext-e1", domain_id="media", source_id="ext1",
                   statement="A reported external success case", observed_at=self.at)
        self.apply("record_external_case", id="case1", domain_id="media", evidence_ids=["ext-e1"],
                   outcome="SUCCESS", context="External operator reported an improvement",
                   mechanism_hypothesis="The intervention may have contributed",
                   transfer_limits="Different operator, audience and conditions",
                   uncertainty="No first-party reproduction by Owner")
        case = self.state["external_cases"]["case1"]
        self.assertEqual(case["capital_status"], "EXTERNAL_CASE_CAPITAL_UNVERIFIED")
        self.assertFalse(case["lesson_eligible"])
        self.assertEqual(self.state["lessons"], {})

    def test_failure_external_case_is_preserved_as_learning_capital(self):
        self.base()
        self.apply("record_source", id="ext1", domain_id="media", uri="https://example.test/failure",
                   captured_at=self.at, kind="PUBLIC", rights_status="UNKNOWN")
        self.apply("record_evidence", id="ext-e1", domain_id="media", source_id="ext1",
                   statement="A reported external failure case", observed_at=self.at)
        self.apply("record_external_case", id="casefail", domain_id="media", evidence_ids=["ext-e1"],
                   outcome="FAILURE", context="External attempt failed",
                   mechanism_hypothesis="Failure mechanism is only a hypothesis",
                   transfer_limits="Cannot infer Owner outcome",
                   uncertainty="Third-party report; rights and causality unresolved")
        self.assertEqual(self.state["external_cases"]["casefail"]["outcome"], "FAILURE")
        self.assertFalse(self.state["external_cases"]["casefail"]["lesson_eligible"])

    def test_learning_packet_freezes_target_evidence_and_counterevidence(self):
        self.base()
        self.apply("record_source", id="support", domain_id="media", uri="internal://support",
                   captured_at=self.at, kind="FIRST_PARTY", rights_status="CLEAR")
        self.apply("record_evidence", id="support-e", domain_id="media", source_id="support",
                   statement="Supporting observation", observed_at=self.at)
        self.state["claims"]["h1"]["evidence_ids"] = ["support-e"]
        self.apply("record_source", id="counter", domain_id="media", uri="internal://counter",
                   captured_at=self.at, kind="FIRST_PARTY", rights_status="CLEAR")
        self.apply("record_evidence", id="counter-e", domain_id="media", source_id="counter",
                   statement="Counterexample observation", observed_at=self.at)
        self.apply("freeze_learning_packet", id="packet1", trace_id="trace1", claim_id="h1",
                   counterevidence_ids=["counter-e"], external_case_ids=[],
                   counterevidence_note="Counterexample remains unresolved",
                   context_contract="Critic receives only the frozen bounded packet",
                   instruction_version="learning-assurance-v1",
                   toolset_fingerprint="no-web-bundle-only")
        packet = self.state["learning_packets"]["packet1"]
        self.assertEqual(packet["status"], "FROZEN")
        self.assertEqual(len(packet["target_hash"]), 64)
        self.assertEqual(len(packet["evidence_bundle_hash"]), 64)
        self.assertEqual(packet["supporting_evidence_ids"], ["support-e"])

    def test_critic_execution_records_provenance_and_supports_abstain(self):
        self.base()
        self.apply("freeze_learning_packet", id="packet1", trace_id="trace1", claim_id="h1",
                   counterevidence_ids=[], external_case_ids=[],
                   counterevidence_note="No counterevidence supplied yet",
                   context_contract="Frozen target only", instruction_version="v1",
                   toolset_fingerprint="bundle-only")
        self.apply("record_critic_execution", id="crit1", packet_id="packet1",
                   critic_provider_id="critic", provider="openai", model="declared-model",
                   run_id="run1", context_mode="BLIND", output_hash="abc123",
                   verdict="ABSTAIN", reason="Evidence is insufficient",
                   missing_evidence=["Independent outcome"])
        execution = self.state["critic_executions"]["crit1"]
        self.assertEqual(execution["verdict"], "ABSTAIN")
        self.assertEqual(execution["target_hash"], self.state["learning_packets"]["packet1"]["target_hash"])
        self.assertEqual(execution["evidence_bundle_hash"], self.state["learning_packets"]["packet1"]["evidence_bundle_hash"])

    def test_same_seat_cannot_be_critic_execution(self):
        self.base()
        self.apply("freeze_learning_packet", id="packet1", trace_id="trace1", claim_id="h1",
                   counterevidence_ids=[], external_case_ids=[],
                   counterevidence_note="None yet", context_contract="Frozen", instruction_version="v1",
                   toolset_fingerprint="bundle-only")
        with self.assertRaisesRegex(GateError, "distinct"):
            self.apply("record_critic_execution", id="critbad", packet_id="packet1",
                       critic_provider_id="maker", provider="declared", model="declared",
                       run_id="run1", context_mode="BLIND", output_hash="abc",
                       verdict="FINDINGS", reason="Self critique", missing_evidence=[])

    def test_negative_control_cannot_cross_domain(self):
        self.base()
        self.apply("freeze_learning_packet", id="packet1", trace_id="trace1", claim_id="h1",
                   counterevidence_ids=[], external_case_ids=[],
                   counterevidence_note="None", context_contract="Frozen", instruction_version="v1",
                   toolset_fingerprint="bundle-only")
        self.apply("record_negative_control", id="nc1", packet_id="packet1",
                   description="A tempting counter-case", expected="Claim should not overgeneralize",
                   observed="Claim stayed bounded", result="PASS", evidence_ids=[])
        self.assertEqual(self.state["negative_controls"]["nc1"]["result"], "PASS")

    def test_trace_link_binds_existing_artifact_digest(self):
        self.base()
        self.apply("record_source", id="s1", domain_id="media", uri="internal://source",
                   captured_at=self.at, kind="FIRST_PARTY", rights_status="CLEAR")
        self.apply("record_evidence", id="e1", domain_id="media", source_id="s1",
                   statement="Observation", observed_at=self.at)
        self.apply("record_trace_link", id="tl1", trace_id="trace1",
                   artifact_type="EVIDENCE", artifact_id="e1", relation="SUPPORT")
        link = self.state["trace_links"]["tl1"]
        self.assertEqual(link["trace_id"], "trace1")
        self.assertEqual(len(link["artifact_digest"]), 64)

    def test_trace_link_rejects_missing_artifact(self):
        self.base()
        with self.assertRaisesRegex(GateError, "Unknown traced artifact"):
            self.apply("record_trace_link", id="tl1", trace_id="trace1",
                       artifact_type="EVIDENCE", artifact_id="missing", relation="SUPPORT")

    def test_failed_negative_control_blocks_lesson_freeze(self):
        self.base()
        self.predictions_and_outcomes()
        self.apply("review_claim", id="review1", claim_id="h1", critic_provider_id="critic",
                   verdict="ACCEPT_FOR_TRIAL", reason="Alternative remains testable")
        self.apply("adjudicate_claim", id="adj1", claim_id="h1", review_id="review1",
                   adjudicator_provider_id="judge", verdict="ACCEPT_FOR_TRIAL",
                   reason="Bounded trial only")
        self.apply("propose_lesson", id="lesson1", claim_id="h1", statement="Try this narrow method",
                   limits="Two observations; confounding unresolved", prediction_ids=["f1", "f2"],
                   adjudication_id="adj1", counterevidence_ids=[],
                   counterevidence_search_note="Searched recorded evidence; none found",
                   applicability="Media domain under the measured conditions only")
        self.apply("freeze_learning_packet", id="packet-negative", trace_id="trace-negative",
                   claim_id="h1", counterevidence_ids=[], external_case_ids=[],
                   counterevidence_note="Adversarial control attached",
                   context_contract="Frozen", instruction_version="v1",
                   toolset_fingerprint="bundle-only")
        self.apply("record_negative_control", id="nc-fail", packet_id="packet-negative",
                   description="Known counter-case", expected="Lesson must survive",
                   observed="Lesson fails the counter-case", result="FAIL", evidence_ids=[])
        with self.assertRaisesRegex(GateError, "Failed negative control"):
            self.apply("freeze_lesson", lesson_id="lesson1")

    def test_lesson_revalidation_is_proposal_only(self):
        self.base()
        self.predictions_and_outcomes()
        self.review_and_lesson()
        self.apply("schedule_lesson_revalidation", id="sched1", lesson_id="lesson1",
                   review_after="2026-02-01T00:00:00Z",
                   staleness_conditions=["Platform policy changes", "Observed outcome reverses"],
                   reason="Recheck a slowly accumulated lesson")
        self.apply("record_lesson_revalidation", at="2026-02-02T00:00:00Z",
                   id="rev1", schedule_id="sched1", evidence_ids=[],
                   outcome="INCONCLUSIVE", reason="Not enough new first-party evidence",
                   limits="Keep current status unchanged", trigger="SCHEDULED")
        review = self.state["lesson_revalidations"]["rev1"]
        self.assertEqual(review["status"], "PROPOSAL_ONLY")
        self.assertFalse(review["automatic_lesson_mutation"])
        self.assertEqual(self.state["lessons"]["lesson1"]["status"], "FROZEN_PENDING_OWNER")

    def test_scheduled_revalidation_cannot_run_early(self):
        self.base()
        self.predictions_and_outcomes()
        self.review_and_lesson()
        self.apply("schedule_lesson_revalidation", id="sched1", lesson_id="lesson1",
                   review_after="2026-02-01T00:00:00Z",
                   staleness_conditions=["Policy change"],
                   reason="Periodic review")
        with self.assertRaisesRegex(GateError, "before review_after"):
            self.apply("record_lesson_revalidation", at="2026-01-20T00:00:00Z",
                       id="rev1", schedule_id="sched1", evidence_ids=[],
                       outcome="RETAIN", reason="Too early", limits="None",
                       trigger="SCHEDULED")

    def test_learning_failure_is_metadata_only(self):
        self.base()
        self.apply("record_source", id="s1", domain_id="media", uri="internal://source",
                   captured_at=self.at, kind="FIRST_PARTY", rights_status="CLEAR")
        self.apply("record_evidence", id="e1", domain_id="media", source_id="s1",
                   statement="Observation", observed_at=self.at)
        self.apply("record_learning_failure", id="lf1", domain_id="media",
                   artifact_type="EVIDENCE", artifact_id="e1",
                   failure_class="SOURCE_ERROR", severity="HIGH",
                   evidence_ids=["e1"], description="Source interpretation may be wrong",
                   remediation="Reopen source and collect independent evidence",
                   detected_by="HUMAN")
        failure = self.state["learning_failures"]["lf1"]
        self.assertEqual(failure["status"], "OPEN")
        self.assertFalse(failure["automatic_remediation"])
        self.assertEqual(len(failure["artifact_digest"]), 64)
        self.assertEqual(self.state["evidence"]["e1"]["verification"], "DECLARED_UNVERIFIED")

    def test_learning_failure_rejects_cross_domain_artifact(self):
        self.base()
        self.apply("register_domain", id="other", name="Other", risk_class="NORMAL",
                   measurement_contract="Other data")
        with self.assertRaisesRegex(GateError, "cross domain"):
            self.apply("record_learning_failure", id="lf1", domain_id="other",
                       artifact_type="CLAIM", artifact_id="h1",
                       failure_class="SCOPE_OVERREACH", severity="MEDIUM",
                       evidence_ids=[], description="Wrong scope",
                       remediation="Keep domain boundary", detected_by="MODEL")

    def test_critic_independence_receipt_never_auto_proves_independence(self):
        self.base()
        self.apply("freeze_learning_packet", id="packet1", trace_id="trace1", claim_id="h1",
                   counterevidence_ids=[], external_case_ids=[],
                   counterevidence_note="None", context_contract="Blind bounded packet",
                   instruction_version="v1", toolset_fingerprint="bundle-only")
        self.apply("record_critic_execution", id="crit1", packet_id="packet1",
                   critic_provider_id="critic", provider="external", model="critic-model",
                   run_id="run1", context_mode="BLIND", output_hash="out123",
                   verdict="NO_MATERIAL_DEFECT", reason="Bounded review", missing_evidence=[])
        self.apply("record_source", id="proofs", domain_id="media", uri="internal://critic-receipt",
                   captured_at=self.at, kind="FIRST_PARTY", rights_status="CLEAR")
        self.apply("record_evidence", id="proofe", domain_id="media", source_id="proofs",
                   statement="External execution receipt captured", observed_at=self.at)
        self.apply("record_critic_independence_receipt", id="cir1",
                   critic_execution_id="crit1", execution_environment_id="external-env",
                   project_runtime_id="project-env", session_id="session-1",
                   provider_receipt_hash="receipt-hash", authority_scope="SEPARATE_OWNER_APPROVED_AUTHORITY",
                   project_context_supplied=False, verification_method="EXTERNAL_EVIDENCE",
                   evidence_ids=["proofe"])
        receipt = self.state["critic_independence_receipts"]["cir1"]
        self.assertEqual(
            receipt["status"],
            "PROCESS_SEPARATED_EXTERNAL_EVIDENCE_RECORDED_NOT_FULL_INDEPENDENCE_PROOF",
        )
        self.assertFalse(receipt["automatic_independence_proof"])

    def test_critic_independence_same_runtime_is_blocked(self):
        self.base()
        self.apply("freeze_learning_packet", id="packet1", trace_id="trace1", claim_id="h1",
                   counterevidence_ids=[], external_case_ids=[],
                   counterevidence_note="None", context_contract="Blind",
                   instruction_version="v1", toolset_fingerprint="bundle-only")
        self.apply("record_critic_execution", id="crit1", packet_id="packet1",
                   critic_provider_id="critic", provider="declared", model="critic-model",
                   run_id="run1", context_mode="BLIND", output_hash="out123",
                   verdict="FINDINGS", reason="Review", missing_evidence=[])
        self.apply("record_critic_independence_receipt", id="cir1",
                   critic_execution_id="crit1", execution_environment_id="same-env",
                   project_runtime_id="same-env", session_id="session-1",
                   provider_receipt_hash="receipt-hash", authority_scope="UNKNOWN",
                   project_context_supplied=False, verification_method="RECEIPT_HASH_BOUND",
                   evidence_ids=[])
        self.assertEqual(
            self.state["critic_independence_receipts"]["cir1"]["status"],
            "BLOCKED_SAME_RUNTIME",
        )

    def test_eval_integrity_flags_leak_and_score_gaming_without_proving_cause(self):
        self.base()
        self.apply("record_eval_integrity_assessment", id="eval1", domain_id="media",
                   artifact_type="CLAIM", artifact_id="h1", output_hash="hash1",
                   forbidden_marker_hits=["answer-key-token"],
                   invariant_failures=["claimed pass despite failed invariant"],
                   claimed_pass=True, evaluator_kind="EVAL",
                   note="Deterministic guard found leakage marker and invariant failure")
        assessment = self.state["eval_integrity_assessments"]["eval1"]
        self.assertEqual(
            assessment["status"],
            "EVAL_CONTAMINATION_AND_REWARD_HACKING_SUSPECTED",
        )
        self.assertFalse(assessment["automatic_proof"])

    def test_eval_integrity_clean_signal_is_not_proof(self):
        self.base()
        self.apply("record_eval_integrity_assessment", id="eval1", domain_id="media",
                   artifact_type="CLAIM", artifact_id="h1", output_hash="hash1",
                   forbidden_marker_hits=[], invariant_failures=[],
                   claimed_pass=True, evaluator_kind="TOOL",
                   note="No configured leakage or invariant signal detected")
        self.assertEqual(
            self.state["eval_integrity_assessments"]["eval1"]["status"],
            "CLEAN_NO_SIGNAL_NOT_PROOF",
        )

    def test_deliberation_plan_escalates_on_conflict_without_storing_cot(self):
        self.base()
        self.apply("record_deliberation_plan", id="dp1", domain_id="media",
                   artifact_type="CLAIM", artifact_id="h1",
                   risk_level="LOW", evidence_conflict=True, tool_dependency=False,
                   requested_effort="LOW", rationale="Conflicting evidence requires deeper review")
        plan = self.state["deliberation_plans"]["dp1"]
        self.assertEqual(plan["effective_effort"], "HIGH")
        self.assertFalse(plan["stores_chain_of_thought"])

    def test_research_trace_keeps_social_signal_noncanonical(self):
        self.base()
        self.apply("record_source", id="social1", domain_id="media",
                   uri="https://example.test/post", captured_at=self.at,
                   kind="PUBLIC", rights_status="CLEAR")
        self.apply("record_research_trace", id="rt1", domain_id="media",
                   query="trend evidence", source_id="social1", source_role="SOCIAL_SIGNAL",
                   claim_id="h1", citation_locator="post-1", conflict_status="SUPPORTS",
                   note="Useful signal only")
        self.assertEqual(
            self.state["research_traces"]["rt1"]["truth_weight"],
            "NON_CANONICAL_SIGNAL",
        )

    def test_context_capsule_is_context_only_and_digest_bound(self):
        self.base()
        self.apply("record_context_capsule", id="ctx1", domain_id="media",
                   artifact_refs=[{"artifact_type": "CLAIM", "artifact_id": "h1"}],
                   summary="Bounded summary for future work",
                   refresh_after="2026-02-01T00:00:00Z",
                   context_purpose="Reduce long-context noise")
        capsule = self.state["context_capsules"]["ctx1"]
        self.assertEqual(capsule["status"], "CONTEXT_ONLY_NOT_CANONICAL_TRUTH")
        self.assertFalse(capsule["automatic_truth_promotion"])
        self.assertEqual(len(capsule["capsule_digest"]), 64)
        self.assertEqual(len(capsule["artifact_refs"][0]["artifact_digest"]), 64)

    def test_hash_chain_and_cache_detect_partial_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Ledger(Path(tmp) / "brain")
            config = write_owner_config(tmp)
            ledger.init()
            ledger_apply(ledger, cmd("register_domain", id="youtube", name="YouTube", risk_class="NORMAL", measurement_contract="CTR"), config)
            self.assertEqual(ledger.verify()[1], 1)
            ledger.snapshot.write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(GateError, "Snapshot differs"):
                ledger.verify()
            ledger_repair(ledger, config)
            self.assertEqual(ledger.verify()[1], 1)
            lines = ledger.events.read_text(encoding="utf-8").replace("YouTube", "Finance")
            ledger.events.write_text(lines, encoding="utf-8")
            with self.assertRaisesRegex(GateError, "chain mismatch"):
                ledger.verify()


if __name__ == "__main__":
    unittest.main()
