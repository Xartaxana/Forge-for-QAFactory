"""Manual producer -> reducer -> public ledger -> delivery, including stale evidence."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_manual_evidence as fixtures
import manual_evidence as M
import finalize_task as F
import ledger as L
import delivery_manifest as D
import manifest_put
from event_store import EventStore, content_hash, atomic_json
from coverage_contract import coverage_projection
from test_coverage_contract import obligation


class ManualProjection(unittest.TestCase):
    def test_current_obligations_survive_same_case_and_public_index_is_current(self):
        with tempfile.TemporaryDirectory() as td:
            task = Path(td)
            fixtures.ROOT = task
            before, after = task / "work/evidence/before.png", task / "work/evidence/after.png"
            before.parent.mkdir(parents=True)
            before.write_bytes(b"before"); after.write_bytes(b"after")
            obs = [obligation("O-1", "manual-agent"), obligation("O-2", "manual-agent")]
            for ob in obs:
                ob["evidence_policy"] = "ui"
            atomic_json(task / "work/test-plan.json", [{"id": "TS-1", "schema_version": 2, "coverage_obligations": obs}])
            atomic_json(task / "state/story-case-links.json", {"links": [{"case_id": "TC-1", "version": "cv_1"}]})
            store = EventStore(task)
            store.commit("initialize", {"source_revision": fixtures.SNAPSHOT_SHA, "scope": ["TC-1"]}, "init")
            # t-271 (A): what the story's runs recorded - the profile checkout the proof binds to. The old fixture word
            # `source` on both sides was the only way the controller's sha256 and a probe's git HEAD could be equal.
            fixtures.seed_provenance(task)
            store.commit("dispatch", {"id": "d1", "stage": "S6", "role": "qa-runner", "scope": ["TC-1"]}, "d1")
            first = fixtures.record(before, after)
            first["completion_condition"] = "done"
            first["obligation_ids"] = ["O-1", "O-2"]
            first["obligation_hashes"] = {o["obligation_id"]: content_hash(o) for o in obs}
            first["approved_policy_hash"] = content_hash({"evidence_policy": "ui",
                "completion_condition": obs[0]["completion_condition"],
                "obligation_hashes": first["obligation_hashes"]})
            first["gate_a_decision_ref"] = "decision:gate-a"
            block = M.write_block(task, [first])
            self.assertEqual(block, M.write_block(task, [first]))
            second = copy.deepcopy(first)
            second.update(attempt_id="a2", obligation_ids=["O-1"], obligation_hashes={"O-1": content_hash(obs[0])},
                          attempt_started_at="2026-09-17T11:00:00Z", attempt_ended_at="2026-09-17T11:01:00Z")
            second["approved_policy_hash"] = content_hash({"evidence_policy": "ui",
                "completion_condition": obs[0]["completion_condition"],
                "obligation_hashes": {"O-1": content_hash(obs[0])}})
            for ref in second["evidence_refs"]:
                ref["captured_at"] = "2026-09-17T11:00:00Z"
            M.write_block(task, [second])
            F.refresh(task)
            report = json.loads((task / "work/run-report.json").read_text())
            self.assertEqual(len(report["manual_checks"]), 2)
            self.assertEqual(len(report["current_manual_checks"]), 2)
            self.assertEqual({tuple(r["current_obligation_ids"]) for r in report["current_manual_checks"]}, {("O-1",), ("O-2",)})
            self.assertEqual(report["source_revision"], fixtures.SNAPSHOT_SHA)
            projected = coverage_projection(task, report, {})
            self.assertTrue(all(o["verified"] for o in projected["obligations"]))
            ledger = L.build(task); self.assertTrue(ledger["source_inputs"]["fingerprint"]); L.write(task, ledger)
            self.assertEqual(len(ledger["manual_evidence"]["rows"]), 2)
            files = {r["path"] for r in D.build(task)["files"]}
            # OH3-33: the exported copies are checked but never listed: git ignores evidence/, the tester keeps it
            self.assertFalse(any(p.startswith(("evidence/", "work/evidence/")) for p in files))
            changed = copy.deepcopy(obs)
            changed[0]["behavior"] = "changed O-1 only"
            atomic_json(task / "work/test-plan.json",
                        [{"id": "TS-1", "schema_version": 2, "coverage_obligations": changed}])
            F.refresh(task)
            scoped = {r["current_obligation_ids"][0]: r
                      for r in json.loads((task / "work/run-report.json").read_text())["current_manual_checks"]}
            self.assertFalse(scoped["O-1"]["evidence_validated"])
            self.assertEqual(scoped["O-1"]["result"], "inconclusive")
            self.assertTrue(scoped["O-2"]["evidence_validated"])
            # Restore the plan before exercising public-copy corruption below.
            atomic_json(task / "work/test-plan.json",
                        [{"id": "TS-1", "schema_version": 2, "coverage_obligations": obs}])
            # Corrupting a captured artifact never leaves its prior public copy as authority.
            after.write_bytes(b"modified")
            F.refresh(task)
            with self.assertRaises(ValueError):
                D.build(task)  # prior index is stale
            ledger = L.build(task); L.write(task, ledger)
            self.assertFalse(any(o["verified"] for o in ledger["coverage"]["obligations"]))
            self.assertEqual(json.loads((task / "evidence/index.json").read_text())["rows"], [])
            self.assertFalse(any(r["path"].endswith(".png") for r in D.build(task)["files"]))

    def test_manifest_windows_keep_other_obligation_bindings(self):
        first = {"obligation_bindings": [{"obligation_id": "O-1", "obligation_hash": "one"}]}
        result, _ = manifest_put.merge(first, {"obligation_bindings": [{"obligation_id": "O-2", "obligation_hash": "two"}]})
        self.assertEqual({b["obligation_id"] for b in result["obligation_bindings"]}, {"O-1", "O-2"})

    def test_static_reason_is_bound_at_design_time(self):
        with tempfile.TemporaryDirectory() as td:
            task = Path(td)
            fixtures.ROOT = task
            before, after = task / "work/evidence/before.png", task / "work/evidence/after.png"
            before.parent.mkdir(parents=True)
            before.write_bytes(b"before"); after.write_bytes(b"after")
            ob = obligation("O-STATIC", "manual-agent")
            ob.update(evidence_policy="static", before_not_applicable_reason="immutable deployment config")
            atomic_json(task / "work/test-plan.json",
                        [{"id": "TS-1", "schema_version": 2, "coverage_obligations": [ob]}])
            atomic_json(task / "state/story-case-links.json",
                        {"links": [{"case_id": "TC-1", "version": "cv_1"}]})
            store = EventStore(task)
            store.commit("initialize", {"source_revision": fixtures.SNAPSHOT_SHA, "scope": ["TC-1"]}, "init")
            # t-271 (A): what the story's runs recorded - the profile checkout the proof binds to. The old fixture word
            # `source` on both sides was the only way the controller's sha256 and a probe's git HEAD could be equal.
            fixtures.seed_provenance(task)
            store.commit("dispatch", {"id": "d1", "stage": "S6", "role": "qa-runner",
                                      "scope": ["TC-1"]}, "d1")
            record = fixtures.record(before, after)
            record.update(obligation_ids=["O-STATIC"],
                          obligation_hashes={"O-STATIC": content_hash(ob)},
                          evidence_policy="static",
                          completion_condition="done",
                          before_not_applicable_reason="chosen after execution")
            record["approved_policy_hash"] = content_hash({"evidence_policy": "static",
                "completion_condition": ob["completion_condition"],
                "obligation_hashes": {"O-STATIC": content_hash(ob)}})
            record["gate_a_decision_ref"] = "decision:gate-a"
            record["evidence_refs"] = [record["evidence_refs"][1]]
            from coverage_contract import validate_manual_current
            self.assertIn("static before_not_applicable_reason differs from approved design",
                          validate_manual_current(task, record))
            record["before_not_applicable_reason"] = "immutable deployment config"
            self.assertEqual(validate_manual_current(task, record), [])
            record["completion_condition"] = "chosen after execution"
            self.assertIn("manual completion_condition differs from approved design",
                          validate_manual_current(task, record))


if __name__ == "__main__":
    unittest.main()
