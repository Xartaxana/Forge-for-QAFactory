import hashlib
import json
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import baseline_contract as B
import gate_registry as GR
import gate_template as GT
import manual_evidence as M
from planning_contract import validate_plan


def contract():
    return {"case_id": "TC-1", "case_version": "v1", "baseline_revision": "old",
            "verification_revision": "new", "fixture_identity": "seed-1",
            "gate_a_decision_ref": "gate-A", "reason": "prove changed behaviour",
            "execution_scope": "current_task", "capture_steps": ["open old build"],
            "comparison_assertions": ["compare rendered graph"],
            "capture_artifact_refs": ["evidence/before-state.json"]}


class BaselineContractTests(unittest.TestCase):
    def test_runner_receipt_is_captured_not_product_pass_and_detects_stale_binding(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); evidence = root / "evidence"; evidence.mkdir()
            summary = evidence / "run.json"; summary.write_text("{}", encoding="utf-8")
            capture = evidence / "before-state.json"; capture.write_text('{"old": true}', encoding="utf-8")
            request = {"evidence_phase": "baseline", "idempotency_key": "baseline-1",
                       "runtime_provenance": {"expected_source_revision": "old", "observed_runtime_identity": "old-build"},
                       "baseline_contract": contract()}
            receipt_path = B.write_baseline_receipt(root, request, {"execution_status": "passed", "ended_at": "2026-01-01T00:00:00Z"}, summary)
            receipt = json.loads(receipt_path.read_text())
            self.assertEqual(receipt["status"], "captured")
            self.assertNotIn("result", receipt)
            row = {"id": "TC-1", "baseline_required": True, "execution_scope": "current_task",
                   "case_version": "v1", "baseline_revision": "old", "verification_revision": "new",
                   "fixture_identity": "seed-1", "gate_a_decision_ref": "gate-A",
                   "comparison_assertions": ["compare rendered graph"]}
            self.assertTrue(B.deployment_readiness([row], [receipt], root)["ready"])
            self.assertTrue(B.deployment_readiness([row], [receipt], root)["comparisons_ready"])
            capture.write_text('{"tampered": true}', encoding="utf-8")
            tampered = B.deployment_readiness([row], [receipt], root)
            self.assertTrue(tampered["ready"])
            self.assertFalse(tampered["comparisons_ready"])
            capture.write_text('{"old": true}', encoding="utf-8")
            row["verification_revision"] = "changed"
            result = B.deployment_readiness([row], [receipt], root)
            self.assertTrue(result["ready"])
            self.assertFalse(result["comparisons_ready"])
            self.assertFalse(result["gaps"][0]["blocks_execution"])

    def test_unknown_before_is_nonblocking_and_does_not_authorize_deployment(self):
        with tempfile.TemporaryDirectory() as td:
            row = {"case_id": "TC-1", "case_version": "v1", "baseline_required": True,
                   "execution_scope": "current_task", "comparison_assertions": ["compare graph"]}
            result = B.deployment_readiness([row], [], td)
            self.assertTrue(result["ready"])
            self.assertFalse(result["comparisons_ready"])
            self.assertFalse(result["deployment_authorized"])
            self.assertEqual(result["gaps"][0]["status"], "awaiting_baseline")
            self.assertEqual(B.validate_baseline_request({"evidence_phase": "verification"}), [])
            row["execution_scope"] = "regression_recommendation"
            self.assertEqual(B.deployment_readiness([row], [], td)["gaps"], [])

    def test_summary_without_actual_capture_is_inconclusive(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); evidence = root / "evidence"; evidence.mkdir()
            summary = evidence / "run.json"; summary.write_text("{}", encoding="utf-8")
            request = {"evidence_phase": "baseline", "idempotency_key": "baseline-empty",
                       "runtime_provenance": {"expected_source_revision": "old"}, "baseline_contract": contract()}
            receipt = B.baseline_receipt(root, request, {"execution_status": "passed"}, summary)
            self.assertEqual(receipt["status"], "inconclusive")
            row = {"id": "TC-1", "baseline_required": True, "execution_scope": "current_task", "case_version": "v1",
                   "baseline_revision": "old", "verification_revision": "new", "fixture_identity": "seed-1",
                   "comparison_assertions": ["compare rendered graph"]}
            self.assertFalse(B.deployment_readiness([row], [receipt], root)["comparisons_ready"])
            self.assertTrue(B.deployment_readiness([row], [receipt], root)["ready"])

    def test_manual_baseline_is_separate_from_manual_product_result(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); path = root / "work" / "evidence" / "before.txt"; path.parent.mkdir(parents=True)
            path.write_text("old state", encoding="utf-8")
            runtime = {"profile_id": "p", "timestamp": "2026-01-01T00:00:00Z", "environment_id": "e",
                       "expected_source_revision": "old", "observed_runtime_identity": "old-build",
                       "evidence_refs": ["build-id"], "result": "matched",
                       "provenance": {"technical_verification": True, "source_linkage": "exact",
                                      "deployed_source_revision": "old"}}
            record = {"evidence_phase": "baseline", "case": "TC-1", "case_version": "v1", "dispatch_id": "d1",
                      "source_revision": "old", "steps_actual": ["open old build"], "runtime_before": runtime,
                      "runtime_after": dict(runtime), "baseline_contract": contract(), "capture_status": "captured",
                      "attempt_id": "a1", "attempt_ended_at": "2026-01-01T00:00:00Z",
                      "evidence_refs": [{"path": "work/evidence/before.txt", "phase": "baseline",
                                         "content_hash": hashlib.sha256(path.read_bytes()).hexdigest()}]}
            self.assertEqual(M.validate_record(record, root), [])
            receipt = json.loads(M.write_baseline_receipt(root, record).read_text())
            self.assertEqual(receipt["status"], "captured")
            self.assertNotIn("result", receipt)
            record["result"] = "pass"
            self.assertIn("baseline capture cannot carry a product pass/fail result", M.validate_record(record, root))

    def test_planning_requires_comparable_baseline_contract(self):
        row = {"id": "TS-1", "impact": "moderate", "likelihood": "medium", "confidence": "high",
               "risk_rationale": "r", "risk_source_refs": ["R-1"], "risk_policy_revision": "factory-starter-v1",
               "coverage_refs": ["R-1"], "unknowns": [], "verification_depth": "normal",
               "required_scenarios": ["positive"], "test_level_rationale": "api", "design_review_required": False,
               "baseline_required": True, "execution_scope": "current_task",
               "baseline_reason": "prove changed behaviour", "baseline_build": "old-build",
               "verification_build": "new-build", **contract()}
        self.assertEqual(validate_plan([row]), [])
        row.pop("baseline_build", None)
        row.pop("baseline_revision", None)
        self.assertEqual(validate_plan([row]), [])
        with self.assertRaises(ValueError):
            B.build_baseline_fields(row, "gate-A", {})

    def test_builder_binds_approved_row_gate_and_old_runtime(self):
        row = {"case_id": "TC-1", "case_version": "v1", "baseline_reason": "before/after",
               "baseline_revision": "old", "verification_revision": "new", "fixture_identity": "seed-1",
               "execution_scope": "current_task", "capture_steps": ["open old build"],
               "comparison_assertions": ["compare graph"], "capture_artifact_refs": ["evidence/before.json"]}
        fields = B.build_baseline_fields(row, "gate-A", {"expected_source_revision": "old"})
        self.assertEqual(fields["baseline_contract"]["gate_a_decision_ref"], "gate-A")
        with self.assertRaises(ValueError):
            B.build_baseline_fields(row, "gate-A", {"expected_source_revision": "new"})

    def test_managed_state_rejects_arbitrary_gate_reference(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); state = root / "qa-factory" / "artifacts" / "TASK-1" / "state"; state.mkdir(parents=True)
            (state / "controller.json").write_text(json.dumps({"decisions": {"gate-A": {
                "id": "gate-A", "gate": "A", "status": "approved", "scope": ["TC-1"]}}}))
            request = {"task": "TASK-1", "evidence_phase": "baseline", "baseline_contract": contract()}
            self.assertEqual(B.validate_managed_gate(request, root), [])
            request["baseline_contract"] = dict(contract(), gate_a_decision_ref="forged")
            self.assertTrue(B.validate_managed_gate(request, root))

    def test_a_receipt_counts_only_by_its_accepted_status_word(self):
        missing = "baseline evidence missing, stale or incomparable"
        absent = object()
        rows = [("captured", "captured", True, None), ("inconclusive", "inconclusive", False, missing),
                ("Captured", "Captured", False, missing), ("space", " captured", False, missing),
                ("empty", "", False, missing), ("none", None, False, missing), ("int", 5, False, missing),
                ("list", ["captured"], False, missing), ("no key", absent, False, missing),
                ("other revision", "captured", False, missing)]
        broken = [("broken captured", "captured", "judged"), ("broken inconclusive", "inconclusive", "judged"),
                  ("broken no receipt", "captured", missing), ("broken other version", "captured", missing)]
        saved = list(GT._READ)
        try:
            with tempfile.TemporaryDirectory() as td:
                root = Path(td); evidence = root / "evidence"; evidence.mkdir()
                capture = evidence / "before-state.json"; capture.write_text('{"old": true}', encoding="utf-8")
                ref = {"path": "evidence/before-state.json", "sha256": hashlib.sha256(capture.read_bytes()).hexdigest()}
                row = {"id": "TC-1", "baseline_required": True, "execution_scope": "current_task",
                       "case_version": "v1", "baseline_revision": "old", "verification_revision": "new",
                       "fixture_identity": "seed-1", "gate_a_decision_ref": "gate-A",
                       "comparison_assertions": ["compare rendered graph"]}

                def receipt(word, source="old", version="v1"):
                    made = {"evidence_phase": "baseline", "case_id": "TC-1", "case_version": version,
                            "baseline_revision": "old", "verification_revision": "new", "fixture_identity": "seed-1",
                            "gate_a_decision_ref": "gate-A", "comparison_assertions": ["compare rendered graph"],
                            "source_revision": source, "evidence_refs": [ref]}
                    if word is not absent:
                        made["status"] = word
                    return made

                for label, word, ready, reason in rows:
                    with self.subTest(label):
                        got = B.deployment_readiness(
                            [row], [receipt(word, "new" if label == "other revision" else "old")], root)
                        self.assertTrue(got["ready"])
                        self.assertEqual(got["comparisons_ready"], ready)
                        self.assertEqual([g["reason"] for g in got["gaps"]], [reason] if reason else [])
                        self.assertTrue(all(g["blocks_execution"] is False for g in got["gaps"]))
                GT._READ[:] = [({"rows": "x"}, GR.structural_error({"rows": "x"}))]
                for label, word, expect in broken:
                    with self.subTest(label):
                        receipts = [] if label == "broken no receipt" else [
                            receipt(word, version="v2" if label == "broken other version" else "v1")]
                        got = B.deployment_readiness([row], receipts, root)
                        self.assertTrue(got["ready"])
                        self.assertFalse(got["comparisons_ready"])
                        reason = got["gaps"][0]["reason"]
                        if expect == "judged":
                            self.assertTrue(reason.startswith("the gate registry cannot be read ("), reason)
                            self.assertIn("baseline receipt was not judged", reason)
                            self.assertNotIn("missing", reason)
                        else:
                            self.assertEqual(reason, expect)
        finally:
            GT._READ[:] = saved

    def test_an_unknown_old_build_is_refused_never_taken(self):
        sentence = "baseline runtime must match the approved before revision"
        row = {"case_id": "TC-1", "case_version": "v1", "baseline_reason": "before/after",
               "baseline_revision": "old", "verification_revision": "new", "fixture_identity": "seed-1",
               "execution_scope": "current_task", "capture_steps": ["open old build"],
               "comparison_assertions": ["compare graph"], "capture_artifact_refs": ["evidence/before.json"]}
        for label, runtime in (("empty", {}), ("none", {"expected_source_revision": None}),
                               ("blank", {"expected_source_revision": ""}),
                               ("new", {"expected_source_revision": "new"})):
            with self.subTest(label):
                request = {"evidence_phase": "baseline", "baseline_contract": contract(), "runtime_provenance": runtime}
                lines = [e for e in B.validate_baseline_request(request) if e.startswith(sentence)]
                self.assertEqual(len(lines), 1)
                self.assertIn("'old'", lines[0])
                self.assertIn("baseline-inputs", lines[0])
                with self.assertRaises(ValueError) as caught:
                    B.build_baseline_fields(row, "gate-A", runtime)
                self.assertIn("baseline-inputs", str(caught.exception))
                self.assertIn(sentence, str(caught.exception))
        with self.subTest("old accepted"):
            runtime = {"expected_source_revision": "old"}
            request = {"evidence_phase": "baseline", "baseline_contract": contract(), "runtime_provenance": runtime}
            self.assertFalse([e for e in B.validate_baseline_request(request) if e.startswith(sentence)])
            self.assertEqual(B.build_baseline_fields(row, "gate-A", runtime)["runtime_provenance"], runtime)
        with self.subTest("no revision anywhere"):
            bare = dict(contract()); bare.pop("baseline_revision")
            errors = B.validate_baseline_request({"evidence_phase": "baseline", "baseline_contract": bare,
                                                  "runtime_provenance": {}})
            self.assertIn("baseline_contract requires baseline_revision", errors)

    def test_a_malformed_baseline_block_is_named_not_crashed(self):
        def errors_of(**fields):
            return B.validate_baseline_request({"evidence_phase": "baseline", **fields})
        sentence = "baseline runtime must match the approved before revision"
        for label, value in (("str", "x"), ("list", ["x"]), ("int", 5), ("empty str", "")):
            with self.subTest("contract " + label):
                errors = errors_of(baseline_contract=value, runtime_provenance={"expected_source_revision": "old"})
                self.assertTrue(any(e.startswith("baseline_contract must be a JSON object, got " + type(value).__name__)
                                    for e in errors), errors)
        for label, fields in (("none", {"baseline_contract": None}), ("absent", {}), ("empty", {"baseline_contract": {}})):
            with self.subTest("contract " + label):
                self.assertIn("baseline_contract requires case_id", errors_of(**fields))
        for label, value in (("str", "old"), ("list", ["old"]), ("int", 5), ("empty str", "")):
            with self.subTest("runtime " + label):
                errors = errors_of(baseline_contract=contract(), runtime_provenance=value)
                self.assertTrue(any(e.startswith("runtime_provenance must be a JSON object") for e in errors), errors)
                self.assertFalse(any(e.startswith(sentence) for e in errors), errors)
        for label, fields in (("none", {"runtime_provenance": None}), ("absent", {}), ("empty", {"runtime_provenance": {}})):
            with self.subTest("runtime " + label):
                lines = [e for e in errors_of(baseline_contract=contract(), **fields) if e.startswith(sentence)]
                self.assertEqual(len(lines), 1)
                self.assertIn("None", lines[0])
        with self.subTest("builder"):
            row = {"case_id": "TC-1", "case_version": "v1", "baseline_reason": "r", "baseline_revision": "old",
                   "verification_revision": "new", "fixture_identity": "seed-1", "execution_scope": "current_task",
                   "capture_steps": ["a"], "comparison_assertions": ["b"], "capture_artifact_refs": ["e/x.json"]}
            with self.assertRaises(ValueError) as caught:
                B.build_baseline_fields(row, "gate-A", "old")
            self.assertIn("runtime_provenance", str(caught.exception))
        with self.subTest("managed gate"):
            with tempfile.TemporaryDirectory() as td:
                root = Path(td); state = root / "qa-factory" / "artifacts" / "TASK-1" / "state"; state.mkdir(parents=True)
                (state / "controller.json").write_text(json.dumps({"decisions": {"gate-A": {
                    "id": "gate-A", "gate": "A", "status": "approved", "scope": ["TC-1"]}}}))
                got = B.validate_managed_gate({"task": "TASK-1", "evidence_phase": "baseline",
                                               "baseline_contract": "x"}, root)
                self.assertTrue(got)


if __name__ == "__main__":
    unittest.main()
