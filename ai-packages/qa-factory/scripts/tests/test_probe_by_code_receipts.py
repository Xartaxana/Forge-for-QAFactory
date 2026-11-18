"""receipts: a part of test_probe_by_code.py, split by tools/test_split.py (TD-11c). The shared helpers are in probe_by_code_common."""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import SCRIPTS, check, check_eq, check_in, cleanup, finish, run_script, temp_dir, use_project
sys.path.insert(0, str(SCRIPTS))
import contract as C  # noqa: E402
import probe_by_code as PBC  # noqa: E402
import proof_level as PL  # noqa: E402
import probe_entries  # noqa: E402
del probe_entries  # split: imported for its sys.path effect
from event_store import content_hash  # noqa: E402
from probe_by_code_common import (  # noqa: E402
    DISPATCH, FAKE_RUN_SUITE, TASK, TEST_FILE_REL, binding_of, cleanup_beside, entry, env_for, give_word,
    manifest_of, model_entries, project, read_record, receipt_files, row_of, run, snapshot, task_of,
    write_json,
)


def clear_word(root: Path) -> None:
    path = task_of(root) / "pipeline.json"
    pipeline = json.loads(path.read_text(encoding="utf-8"))
    pipeline.pop("stage_overrides", None)
    write_json(path, pipeline)


def live_receipt_and_publish(root: Path, stub: Path) -> dict:
    """An `intended_failure` writes an immutable live receipt that `contract.sensitivity_proof_issues`
    accepts UNCHANGED, and publishes it in `tests[]` and in the obligation binding."""
    task = task_of(root)
    proc, record = run(root, stub, f"{TEST_FILE_REL}::test_add", "test_add")
    check("live receipt: exit 0", proc.returncode == 0, proc.stdout + proc.stderr)
    ref = record.get("receipt") or {}
    path = task / str(ref.get("path") or "missing")
    check("live receipt: the record says where the receipt is and it is on disk", path.is_file(), str(ref))
    check("live receipt: named <stem>-live-<16 hex>.json under work/sensitivity-receipts/",
          re.fullmatch(r"test_add-live-[0-9a-f]{16}\.json", path.name) is not None
          and path.parent == task / "work" / "sensitivity-receipts", path.as_posix())
    check_eq("live receipt: the ref's sha256 is the file's", ref.get("sha256"), PBC.sha256(path.read_bytes()))
    body = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    check_eq("live receipt: every PROOF_FIELDS is present and non-empty",
             [k for k in C.PROOF_FIELDS if not body.get(k)], [])
    check_eq("live receipt: the facts come from the author's record",
             (body.get("case_version"), body.get("test_content_hash"), body.get("source_revision"),
              body.get("build_id")), ("cv_1", row_of(root)["trace_binding"]["test_content_sha"], "source-1", "build-1"))
    check_eq("live receipt: its bytes are the raw file hash the probe measured, not the run's fingerprint",
             (body.get("test_content_hash"), body.get("test_content_hash") == record.get("input_hash")),
             (record.get("test_file_sha256"), False))
    check_eq("live receipt: and the code of those bytes (diff_scope.executable_sha), for comment-only edits",
             (body.get("test_code_sha"), record.get("test_code_sha")),
             (PL.code_sha((root / TEST_FILE_REL).read_bytes()),) * 2)
    check_eq("live receipt: it carries what the probe mutated, so a later record cannot change it (t-075 A)",
             (body.get("mutated_file"), bool(body.get("mutated_file"))), (record.get("mutated_file"), True))
    check_eq("live receipt: level, tool and mutation kind",
             (body.get("proof_level"), body.get("probe_tool"), body.get("mutation_kind"), body.get("mutation")),
             ("live", "probe_by_code.py", "assertion", "invert"))
    check_eq("live receipt: the failure is the probe's own",
             (body.get("expected_assertion_failure"), body.get("actual_failure"), body.get("assertion_location"),
              body.get("failure_kind")),
             (record.get("expected_reason"), record.get("actual_reason"), f"{TEST_FILE_REL}:6", "assertion"))
    check("live receipt: restoration evidence says what was restored and how it was verified",
          str(body.get("restoration_evidence")).startswith(f"probe_by_code: {TEST_FILE_REL} sha256 ")
          and str(body.get("restoration_evidence")).endswith(" verified restored"), str(body.get("restoration_evidence")))
    check_eq("live receipt: it points at the probe's record and carries the run evidence",
             (body.get("probe_record"), body.get("evidence_refs")), ("work/probes/test_add.json", record.get("evidence_refs")))
    check_eq("live receipt: obligation fields", (body.get("obligation_ids"), body.get("defect_location"),
                                                  body.get("assertion_id")),
             (["OB-ADD-1"], "calc.py:2", "add_returns_sum"))
    check_eq("live receipt: immutable, with its own hash", (body.get("immutable"), len(str(body.get("receipt_hash")))),
             (True, 64))
    check_eq("live receipt: the hash is the hash of the rest, the run evidence excluded",
             body.get("receipt_hash"), content_hash({k: v for k, v in body.items()
                                                     if k not in ("receipt_hash", "evidence_refs")}))
    check_eq("live receipt: the record on disk names the receipt too", read_record(root, "test_add").get("receipt"), ref)
    row = row_of(root)
    check_eq("published: the row's sensitivity_proof.receipt_ref is the receipt",
             (row.get("sensitivity_proof") or {}).get("receipt_ref"), ref)
    check_eq("published: the author's row keeps its file and case", (row.get("file"), row.get("case")),
             (TEST_FILE_REL, "TC-100"))
    # THE acceptance key: the contract's own validator takes the receipt as it is.
    check_eq("contract.sensitivity_proof_issues accepts the live receipt unchanged",
             C.sensitivity_proof_issues(row, task), [])
    reached = PL.reached(row, manifest_of(root), task)
    check_eq("reached(): the check is live", (reached["level"], reached["words"], reached["issues"]),
             ("live", "the check is live", []))
    binding = binding_of(root)
    check_eq("published: the obligation binding lists the instance, proven by an executed probe",
             (binding.get("instance_ids"), binding.get("sensitivity"), binding.get("proof_kind"),
              binding.get("probe_receipt_ref")), (["test_add"], "proven", "executed_red_probe", ref["path"]))
    publish = record.get("publish") or {}
    check_eq("FR-14: the record says what the publish did", (publish.get("published"), publish.get("row")),
             (True, "added"))
    check_eq("...binding by binding", [(b["obligation_id"], b["receipt"]) for b in publish.get("bindings") or []],
             [("OB-ADD-1", "set")])
    check_eq("...and the record on disk carries it", (read_record(root, "test_add").get("publish") or {}).get("row"),
             "added")
    check_eq("the fragment was scratch: nothing landed in the story's work folder",
             sorted(p.name for p in (task / "work").glob("probe-binding-*")), [])
    check_eq("the receipt files of the instance: one", len(receipt_files(root)), 1)
    return record


def a_rerun_is_idempotent_and_new_bytes_are_a_new_receipt(root: Path, stub: Path, first: dict) -> None:
    task = task_of(root)
    before = receipt_files(root)[0]
    frozen = before.read_bytes()
    # t-043 C: a second probe of the same bytes is ANSWERED, not run (D-0018) - exit 0, nothing written
    quiet = snapshot(root)
    proc, answered = run(root, stub, f"{TEST_FILE_REL}::test_add", "test_add")
    check("rerun: exit 0", proc.returncode == 0, proc.stdout + proc.stderr)
    # t-2064 P4b, what holds on the walk road: the repeat launches NOTHING (no run, no new request, job or check record, the same one receipt).
    # Only the aggregate is rebuilt (its rows say "the run was skipped"). The three pins after it are the spec's (t-2064 section on the
    # receipt, item 4: "all proved and the aggregate standing: `already_probed` as today") and the road does not meet them: PRODUCT QUESTION
    # 1 of t-2064-p4b2t2-report.md - they stay red, unbent.
    aggregate = "work/probes/test_add.json"
    moved = snapshot(root)
    check_eq("rerun: nothing LAUNCHED or written but the aggregate (requests, jobs, check records, receipts, manifest)",
             {k: v for k, v in moved.items() if k != aggregate}, {k: v for k, v in quiet.items() if k != aggregate})
    # t-2064 TR2-14 (B3): the repeat on the same bytes and the same model is answered `already_probed`: no walk ran, so the answer carries
    # no `plan_runs` and no `restore.runs` (it used to rebuild the aggregate with every row skipped, 0 and 0)
    check_eq("rerun: answered `already_probed`, the walk ran no check (no plan_runs, no restore.runs)",
             (answered.get("verdict"), answered.get("plan_runs"), (answered.get("restore") or {}).get("runs")), ("already_probed", None, None))
    check_eq("rerun on identical bytes: answered, not probed (spec; PRODUCT QUESTION 1)", answered.get("verdict"), "already_probed")
    check_eq("rerun: by the receipt it holds (spec; PRODUCT QUESTION 1)", (answered.get("by"), answered.get("level")), ("receipt", "live"))
    check_eq("rerun: nothing on disk moved (record, manifest, requests, jobs, receipts) (spec; PRODUCT QUESTION 1)", moved, quiet)
    # ...and a person's word passes ONE repeat: the probe runs, and lands on the same receipt
    give_word(root, "2999-01-01T00:00:00+00:00")
    proc, again = run(root, stub, f"{TEST_FILE_REL}::test_add", "test_add")
    clear_word(root)
    check("rerun with a word: exit 0", proc.returncode == 0, proc.stdout + proc.stderr)
    # the road never blocks a repeat, so the person's word is not read on it any more: the door that named "probe it again" is gone
    # (spec: "only a person's word repeats it", D-0018) - PRODUCT QUESTION 1, red, unbent.
    check_in("rerun with a word: the note records the word (PRODUCT QUESTION 1)", "probe it again", " ".join(again.get("notes") or []))
    check_eq("rerun on identical bytes: the same path", (again.get("receipt") or {}).get("path"),
             first["receipt"]["path"])
    check_eq("rerun on identical bytes: still one receipt file", len(receipt_files(root)), 1)
    check_eq("rerun on identical bytes: the receipt is untouched", before.read_bytes(), frozen)
    check_in("rerun: the note says the proof is already there", "already holds this proof",
             " ".join(again.get("notes") or []))
    check_eq("rerun: the row still names it", (row_of(root).get("sensitivity_proof") or {}).get("receipt_ref"),
             first["receipt"])
    # New bytes: the test's function changed. The manifest still binds the OLD bytes, and this probe
    # MEASURES the new ones (the raw sha256 of the file, before it mutates anything): the receipt
    # would claim bytes nobody compared with what ran, so there is none - and the note names the door.
    bound_before = row_of(root)["trace_binding"]["test_content_sha"]
    (root / TEST_FILE_REL).write_bytes((root / TEST_FILE_REL).read_bytes().replace(b'"sum must be 4"', b'"sum must be four"'))
    proc, stale = run(root, stub, f"{TEST_FILE_REL}::test_add", "test_add")
    check("stale binding: exit 0 (a verdict was recorded)", proc.returncode == 0, proc.stdout + proc.stderr)
    check_eq("stale binding: the probe itself is fine", stale.get("verdict"), "intended_failure")
    measured = str(stale.get("test_file_sha256"))
    check_eq("stale binding: the measured bytes are the file's raw sha256 now, not the manifest's claim",
             (measured, measured != bound_before), (PBC.sha256((root / TEST_FILE_REL).read_bytes()), True))
    check_eq("stale binding: no receipt", stale.get("receipt"), None)
    check_eq("stale binding: the stale fact is named", stale.get("receipt_missing"), ["test_content_hash"])
    notes = " ".join(stale.get("notes") or [])
    check_in("stale binding: the note names both hashes", f"(sha256 {measured}) is not the bytes the manifest "
             f"binds (trace_binding.test_content_sha {bound_before})", notes)
    check_in("stale binding: and the door (the author rebinds through manifest_put, then probe again)",
             "It is the author's to rebind, through `manifest_put.py` (no run needed): "
             "trace_binding.test_content_sha is the sha256 of the file's bytes", notes)
    check_in("stale binding: and warns off the run's fingerprint", "never a run block's source_fingerprint", notes)
    check_eq("stale binding: still one receipt file, the old one untouched",
             (len(receipt_files(root)), before.read_bytes()), (1, frozen))
    check_eq("stale binding: the row still names the old receipt (nothing was replaced)",
             (row_of(root).get("sensitivity_proof") or {}).get("receipt_ref"), first["receipt"])
    check_eq("stale binding: and nothing was published", (stale.get("publish") or {}).get("published"), False)
    scratch = temp_dir("qa-probe-frag-")
    try:  # through manifest_put, as the automator does: it is event-sourced, a hand edit would be projected away
        write_json(scratch / "f.json", {"tests": [{"instance_id": "test_add",
                                                   "trace_binding": {"test_content_sha": measured}}]})
        put = run_script("manifest_put.py", "--task", TASK, "--fragment", scratch / "f.json", cwd=root,
                         env=env_for(root, stub))
        check("new bytes: the author binds them through manifest_put", put.returncode == 0, put.stdout + put.stderr)
    finally:
        cleanup(scratch)
    got = PL.reached(row_of(root), manifest_of(root), task)
    check_eq("BYTES RULE: the old receipt is no longer valid for the row - no level is shown",
             (got["level"], got["words"]), (None, "not probed"))
    check_in("BYTES RULE: and the issue names the door", "probe the current bytes again", got["issues"])
    proc, changed = run(root, stub, f"{TEST_FILE_REL}::test_add", "test_add")
    check("new bytes: exit 0", proc.returncode == 0, proc.stdout + proc.stderr)
    new_ref = changed.get("receipt") or {}
    check("new bytes: a new receipt file", new_ref.get("path") not in (None, first["receipt"]["path"]), str(new_ref))
    check_eq("new bytes: two receipt files now, the first one untouched", (len(receipt_files(root)),
                                                                          before.read_bytes()), (2, frozen))
    check_eq("new bytes: live then live REPLACES the row's ref (equal rank)",
             (row_of(root).get("sensitivity_proof") or {}).get("receipt_ref"), new_ref)
    check_eq("new bytes: ...and the binding's", binding_of(root).get("probe_receipt_ref"), new_ref.get("path"))
    check_eq("new bytes: the instance is listed once", binding_of(root).get("instance_ids"), ["test_add"])
    check_eq("new bytes: the receipt binds the new test hash",
             json.loads((task / new_ref["path"]).read_text(encoding="utf-8")).get("test_content_hash"), measured)
    check_eq("new bytes: the row still validates", C.sensitivity_proof_issues(row_of(root), task), [])
    check_eq("new bytes: the record says it replaced", (changed.get("publish") or {}).get("row"), "replaced")
    check_eq("new bytes: reached() shows the live level again, for the current bytes only",
             PL.reached(row_of(root), manifest_of(root), task)["level"], "live")


def fabricate(task: Path, level: str, tag: str, iid: str = "test_add", sha: str = "") -> dict:
    """A valid receipt of a level, as the OTHER tool would have left it - by default for the bytes the
    test file holds now (its raw sha256: the one reader, Amendment 2)."""
    sha = sha or PBC.sha256((task.parents[2] / TEST_FILE_REL).read_bytes())
    body = {"instance_id": iid, "case_version": "cv_1", "test_content_hash": sha,
            "source_revision": "source-1", "build_id": "build-1", "expected_assertion_failure": "x",
            "actual_failure": "x", "assertion_location": f"{TEST_FILE_REL}:6", "failure_kind": "assertion",
            "restoration_evidence": "r", "immutable": True, "receipt_hash": "h-" + tag}
    if level == "live":
        body.update(mutation="invert", proof_level="live", probe_tool="probe_by_code.py", mutation_kind="assertion")
    else:
        body.update(mutation="real_behavior", proof_level="catches_broken_product", probe_tool="red_sandbox.py")
    path = task / "work" / "sensitivity-receipts" / f"{tag}.json"
    write_json(path, body)
    return {"path": path.relative_to(task).as_posix(), "sha256": PBC.sha256(path.read_bytes())}


def publish_orders() -> None:
    """Edge row 7: never downgrade, union the instance ids, replace at equal rank.

    Every scenario is a FRESH project: `manifest_put.py` is event-sourced, so a manifest written by
    hand over a story that already had a patch is projected away by the next one."""
    made: list = []
    try:
        _publish_orders(made)
    finally:
        for path in made:
            cleanup(path)


def _publish_orders(made: list) -> None:
    root = project()
    made.append(root)
    task = task_of(root)
    use_project(root)
    base = manifest_of(root)
    new = fabricate(task, "live", "new-live")
    product = fabricate(task, "product", "held-product")
    old_live = fabricate(task, "live", "held-live")
    record = {"verdict": "intended_failure", "instance_id": "test_add", "receipt": new,
              "obligation_ids": ["OB-ADD-1"], "restore": {"verified": True}}

    def scenario(name, row_ref, binding_ref, ids=("other",), record_over=None, plan=False, trap=False,
                 retracted=None):
        nonlocal root, task
        root = project()
        made.append(root)
        task = task_of(root)
        use_project(root)
        for level, tag, iid in (("live", "new-live", "test_add"), ("product", "held-product", "test_add"),
                                ("live", "held-live", "test_add"), ("product", "other-instance-product", "other")):
            fabricate(task, level, tag, iid)
        manifest = json.loads(json.dumps(base))
        manifest.pop("obligation_bindings", None)
        if retracted:
            manifest["retracted_instances"] = list(retracted)
        if trap:
            # The critic's trap: the test now holds bytes 2 (the file), and the row holds a
            # HIGHER-level receipt for bytes 1.
            row_ref = fabricate(task, "product", "held-product-bytes1", sha="bytes1")
            binding_ref = row_ref["path"]
            fresh_live = fabricate(task, "live", "new-live-bytes2")
            record_over = dict({"receipt": fresh_live}, **(record_over or {}))
        for test in manifest["tests"]:
            if test.get("instance_id") == "test_add":
                test.pop("sensitivity_proof", None)
                if row_ref:
                    test["sensitivity_proof"] = {"receipt_ref": row_ref}
        if binding_ref is not None:
            manifest["obligation_bindings"] = [{"obligation_id": "OB-ADD-1", "instance_ids": list(ids),
                                               "sensitivity": "proven", "proof_kind": "executed_red_probe",
                                               "probe_receipt_ref": binding_ref, "design_assessment": "sufficient"}]
        write_json(task / "work" / "automation-manifest.json", manifest)
        if plan:  # a plan that names other obligations: manifest_put refuses ours
            write_json(task / "work" / "test-plan.json", {"rows": [{
                "id": "TS-1", "schema_version": 2, "coverage_obligations": [
                    {"obligation_id": "OB-OTHER", "text": "x"}]}]})
        rec = dict(record, **(record_over or {}))
        said = PBC.publish_binding(TASK, task, rec)
        return rec, said

    rec, said = scenario("product then live", product, product["path"])
    check_eq("product then live: the row keeps the product receipt",
             (row_of(root).get("sensitivity_proof") or {}).get("receipt_ref"), product)
    check_eq("product then live: the binding keeps the product receipt", binding_of(root).get("probe_receipt_ref"),
             product["path"])
    check_eq("product then live: and the instance ids are the UNION", binding_of(root).get("instance_ids"),
             ["other", "test_add"])
    check_eq("product then live: an existing binding's other fields survive", binding_of(root).get("design_assessment"),
             "sufficient")
    check_in("product then live: the record says it kept the higher level", "kept", rec["publish"]["row"])
    check_in("product then live: for the binding too", "kept", rec["publish"]["bindings"][0]["receipt"])
    check_in("product then live: and what it said was not a claim of having bound it", "published", said)
    check_eq("product then live: the row still validates as the product level",
             PL.reached(row_of(root), manifest_of(root), task)["level"], "catches_broken_product")

    # F2: a receipt for OTHER bytes shields nothing (BYTES RULE), so the live probe of the bytes the row
    # binds now is published, and the window can bind - never "kept" behind a receipt for old bytes.
    rec, said = scenario("the critic's trap", None, None, trap=True)
    fresh = rec["receipt"]
    check_eq("bytes rule: the live receipt for bytes 2 IS published on the row",
             (row_of(root).get("sensitivity_proof") or {}).get("receipt_ref"), fresh)
    check_eq("bytes rule: ...and in the binding, with the union", (binding_of(root).get("probe_receipt_ref"),
                                                                    binding_of(root).get("instance_ids")),
             (fresh["path"], ["other", "test_add"]))
    check_eq("bytes rule: the record says it replaced, not kept", rec["publish"]["row"], "replaced")
    got = PL.reached(row_of(root), manifest_of(root), task)
    check_eq("bytes rule: the row reaches the live level for the current bytes",
             (got["level"], got["issues"]), ("live", []))
    import window_record as WR
    check_eq("bytes rule: and the window picks that receipt (through reached)",
             WR._window_receipt_ref(row_of(root), manifest_of(root), task)["path"], fresh["path"])
    rec, said = scenario("the trap, and only the old receipt is left", None, None, trap=True,
                         record_over={"receipt": None, "receipt_missing": ["test_content_hash"]})
    check_eq("bytes rule: with no new receipt the row reaches no level (FR-41)",
             PL.reached(row_of(root), manifest_of(root), task)["level"], None)
    check_eq("bytes rule: and the window picks nothing for other bytes",
             WR._window_receipt_ref(row_of(root), manifest_of(root), task), {})

    # retracted rows are not resurrected by the union
    rec, said = scenario("retracted", old_live, old_live["path"], ids=("gone", "other"), retracted=["gone"])
    check_eq("retracted ids leave the union", binding_of(root).get("instance_ids"), ["other", "test_add"])

    rec, said = scenario("live then live", old_live, old_live["path"])
    check_eq("live then live: the row's ref is replaced (equal rank)",
             (row_of(root).get("sensitivity_proof") or {}).get("receipt_ref"), new)
    check_eq("live then live: the binding's too", binding_of(root).get("probe_receipt_ref"), new["path"])
    check_eq("live then live: union again", binding_of(root).get("instance_ids"), ["other", "test_add"])
    check_eq("live then live: the record says replaced", rec["publish"]["row"], "replaced")

    rec, _ = scenario("row product, binding live", product, old_live["path"])
    check_eq("mixed: the product row stays", (row_of(root).get("sensitivity_proof") or {}).get("receipt_ref"), product)
    check_eq("mixed: the live binding is replaced", binding_of(root).get("probe_receipt_ref"), new["path"])
    rec, _ = scenario("row live, binding product", old_live, product["path"])
    check_eq("mixed: the live row is replaced", (row_of(root).get("sensitivity_proof") or {}).get("receipt_ref"), new)
    check_eq("mixed: the product binding stays", binding_of(root).get("probe_receipt_ref"), product["path"])

    tampered = {"path": product["path"], "sha256": "0" * 64}
    rec, _ = scenario("an invalid higher receipt holds nothing", tampered, "work/sensitivity-receipts/gone.json")
    check_eq("invalid product row ref (hash moved): replaced",
             (row_of(root).get("sensitivity_proof") or {}).get("receipt_ref"), new)
    check_eq("binding naming a file that is gone: replaced", binding_of(root).get("probe_receipt_ref"), new["path"])
    other = fabricate(task, "product", "other-instance-product", iid="other")
    rec, _ = scenario("a product receipt of another instance", None, other["path"])
    check_eq("a product receipt that is valid for ANOTHER instance holds nothing for this one",
             binding_of(root).get("probe_receipt_ref"), new["path"])
    check_eq("and the row is added", rec["publish"]["row"], "added")

    rec, _ = scenario("nothing there", None, None)
    check_eq("nothing before: the binding is created", (binding_of(root).get("instance_ids"),
                                                        binding_of(root).get("sensitivity")), (["test_add"], "proven"))
    rec, said = scenario("instance already listed under an alias", None, old_live["path"], ids=("test_add", "x"))
    check_eq("an instance already in the list is not listed twice", binding_of(root).get("instance_ids"),
             ["test_add", "x"])

    rec, said = scenario("no obligations", None, None, record_over={"obligation_ids": []})
    check_eq("empty obligation_ids: the row is published", (row_of(root).get("sensitivity_proof") or {}).get("receipt_ref"),
             new)
    check_eq("empty obligation_ids: no binding was made", manifest_of(root).get("obligation_bindings"), None)
    check_in("empty obligation_ids: the note is kept", "no obligation_ids", rec["publish"].get("bindings_note", ""))
    check_in("empty obligation_ids: and the printed line says so", "no obligation ids", said)

    # nothing to put at all: a higher receipt on the row and no obligations
    rec, said = scenario("only a higher row", product, None, record_over={"obligation_ids": []})
    check_in("a higher receipt on the row and nothing to bind: nothing is put", "nothing to put", said)

    # restore not verified / no receipt: nothing is published
    manifest = json.loads(json.dumps(base))
    write_json(task / "work" / "automation-manifest.json", manifest)
    stale = dict(record, receipt=None, receipt_missing=["build_id"])
    said = PBC.publish_binding(TASK, task, stale)
    check_in("no receipt: nothing published, and the missing fact is named", "build_id", said)
    check_eq("no receipt: the manifest is as it was", manifest_of(root), base)
    check_eq("another verdict publishes nothing and says nothing",
             PBC.publish_binding(TASK, task, dict(record, verdict="no_failure")), "")
    # manifest_put refuses: the plan names other obligations
    rec, said = scenario("refused", None, None, plan=True)
    check_eq("manifest_put refused: the record says so", rec["publish"]["published"], False)
    check_in("manifest_put refused: the printed line names the receipt that stays", new["path"], said)
    check("manifest_put refused: the receipt file stays", (task / new["path"]).is_file())
    check_eq("manifest_put refused: the row was not touched", "sensitivity_proof" in row_of(root), False)


PUBLISH_PUT_OK = re.compile(r"automation-manifest\.json: revision \d+, receipt [0-9a-f]{32}")


PUBLISH_KEPT_ROW = "kept: the row already names a valid receipt that catches a broken product"


PUBLISH_KEPT_BINDING = "kept: the binding already names a valid receipt that catches a broken product"


PUBLISH_NO_OBLIGATIONS = "no obligation_ids on this probe — the row is published, no binding"


def publish_dicts_are_pinned() -> None:
    """t-667 D5, characterisation (E13): what `publish_binding` writes into `record["publish"]` and returns,
    WHOLE, for every row case (added / replaced / kept), a binding kept by a higher-level receipt, no
    obligation ids, a refused `manifest_put`, the early exits, and a record that is not an
    `intended_failure` (returns "" and touches nothing: not the record, not the manifest, no scratch)."""
    made: list = []
    try:
        _publish_dicts(made)
        _publish_stale_projection(made)
    finally:
        for path in made:
            cleanup(path)
            cleanup_beside(path)


def _publish_stale_projection(made: list) -> None:
    """t-1253 F-3: `manifest_put.py` exit 4 = the fragment IS in the journal, only the manifest's projection is stale.
    The publish line names the replay and never says "refused"; the record says `published: False` (the manifest does
    not hold the receipt yet) with a `manifest_put` text of its own. Exit 3 keeps the refusal's words."""
    real = PBC._put_fragment
    try:
        for code, said in ((4, "manifest_put: event committed; projection stale - the fragment is in the journal"),
                           (3, "manifest_put: nothing was committed")):
            PBC._put_fragment = lambda task, fragment, _c=code, _s=said: subprocess.CompletedProcess([], _c, "", _s)
            rec, line, ref, _task = _publish_scenario(made)
            if code == 4:
                check_eq("D5 exit 4: published False, the record says committed and stale",
                         (rec["publish"]["published"], rec["publish"]["manifest_put"].startswith("committed, projection stale: ")),
                         (False, True))
                check_in("D5 exit 4: the line names the replay", f"`manifest_put.py --task {TASK} --recover`", line)
                check("D5 exit 4: and never says refused", "refused" not in line and "refused" not in rec["publish"]["manifest_put"],
                      line)
            else:
                check_eq("D5 exit 3 CONTROL: still the refusal's line",
                         line, f"manifest_put refused the publish, the receipt stays at {ref['path']}: {rec['publish']['manifest_put']}")
    finally:
        PBC._put_fragment = real


def _publish_scenario(made: list, row_tag=None, binding_tag=None, over=None, plan=False) -> tuple:
    """(the record after the publish, the line it returned, the new receipt's ref, the task folder)."""
    root = project()
    made.append(root)
    task = task_of(root)
    use_project(root)
    refs = {tag: fabricate(task, level, tag, iid) for tag, level, iid in (
        ("new-live", "live", "test_add"), ("held-product", "product", "test_add"),
        ("held-live", "live", "test_add"), ("other-product", "product", "other"))}
    manifest = manifest_of(root)
    manifest.pop("obligation_bindings", None)
    for test in manifest["tests"]:
        if test.get("instance_id") == "test_add":
            test.pop("sensitivity_proof", None)
            if row_tag:
                test["sensitivity_proof"] = {"receipt_ref": refs[row_tag]}
    if binding_tag:
        manifest["obligation_bindings"] = [{"obligation_id": "OB-ADD-1", "instance_ids": ["other"],
                                           "sensitivity": "proven", "proof_kind": "executed_red_probe",
                                           "probe_receipt_ref": refs[binding_tag]["path"],
                                           "design_assessment": "sufficient"}]
    write_json(task / "work" / "automation-manifest.json", manifest)
    if plan:  # a plan that names other obligations: manifest_put refuses ours
        write_json(task / "work" / "test-plan.json", {"rows": [{
            "id": "TS-1", "schema_version": 2, "coverage_obligations": [{"obligation_id": "OB-OTHER", "text": "x"}]}]})
    rec = dict({"verdict": "intended_failure", "instance_id": "test_add", "receipt": refs["new-live"],
                "obligation_ids": ["OB-ADD-1"], "restore": {"verified": True}}, **(over or {}))
    return rec, PBC.publish_binding(TASK, task, rec), refs["new-live"], task


def _publish_dicts(made: list) -> None:
    def pinned(label, rec, said, ref, row, bindings, line, note=None):
        put = rec["publish"].pop("manifest_put", None)
        want = {"published": True, "receipt": ref, "row": row, "bindings": bindings}
        if note:
            want["bindings_note"] = note
        check_eq(f"D5 {label}: the whole publish dict (manifest_put apart)", rec["publish"], want)
        check(f"D5 {label}: manifest_put says it put the fragment", PUBLISH_PUT_OK.fullmatch(str(put)) is not None,
              str(put))
        check_eq(f"D5 {label}: the line returned", said, line)

    def item(ids, receipt):
        return [{"obligation_id": "OB-ADD-1", "instance_ids": ids, "receipt": receipt}]

    rec, said, ref, _ = _publish_scenario(made)
    pinned("added", rec, said, ref, "added", item(["test_add"], "set"),
           f"published {ref['path']}: row added; bound OB-ADD-1")
    rec, said, ref, _ = _publish_scenario(made, "held-live", "held-live")
    pinned("replaced", rec, said, ref, "replaced", item(["other", "test_add"], "set"),
           f"published {ref['path']}: row replaced; bound OB-ADD-1")
    rec, said, ref, _ = _publish_scenario(made, "held-product", "held-product")
    pinned("kept (row and binding)", rec, said, ref, PUBLISH_KEPT_ROW, item(["other", "test_add"], PUBLISH_KEPT_BINDING),
           f"published {ref['path']}: row {PUBLISH_KEPT_ROW}; bound OB-ADD-1")
    rec, said, ref, _ = _publish_scenario(made, None, "held-product")
    pinned("a binding kept by a higher-level receipt", rec, said, ref, "added",
           item(["other", "test_add"], PUBLISH_KEPT_BINDING), f"published {ref['path']}: row added; bound OB-ADD-1")
    rec, said, ref, _ = _publish_scenario(made, None, "other-product")
    pinned("a higher receipt of ANOTHER instance holds nothing", rec, said, ref, "added",
           item(["other", "test_add"], "set"), f"published {ref['path']}: row added; bound OB-ADD-1")
    rec, said, ref, _ = _publish_scenario(made, over={"obligation_ids": []})
    pinned("no obligation ids", rec, said, ref, "added", [],
           f"published {ref['path']}: row added; no obligation ids to bind", note=PUBLISH_NO_OBLIGATIONS)
    rec, said, ref, task = _publish_scenario(made, "held-product", over={"obligation_ids": []})
    check_eq("D5 nothing to put: the whole publish dict",
             rec["publish"], {"published": True, "receipt": ref, "row": PUBLISH_KEPT_ROW, "bindings": [],
                              "bindings_note": PUBLISH_NO_OBLIGATIONS,
                              "manifest_put": "nothing to put: a receipt of a higher level is already published"})
    check_eq("D5 nothing to put: the line returned", said,
             "nothing to put: a receipt of a higher level is already published")
    rec, said, ref, task = _publish_scenario(made, plan=True)
    put = rec["publish"].pop("manifest_put")
    check_eq("D5 manifest_put refused: the publish dict (manifest_put apart)", rec["publish"],
             {"published": False, "receipt": ref, "row": "added", "bindings": item(["test_add"], "set")})
    check("D5 manifest_put refused: the refusal, cut to its last 300 characters",
          put.startswith("refused: ") and 0 < len(put) <= len("refused: ") + 300 and "waiver.py" in put, put)
    check_eq("D5 manifest_put refused: the line returned names the receipt that stays", said,
             f"manifest_put refused the publish, the receipt stays at {ref['path']}: {put}")
    # the early exits: nothing reaches the manifest
    for label, over, why in (
            ("restore not verified", {"receipt": None, "restore": {"verified": False}}, "the restore was not verified"),
            ("facts missing", {"receipt": None, "receipt_missing": ["build_id", "source_revision"]},
             "the facts a receipt binds are missing: build_id, source_revision"),
            ("no reason known", {"receipt": None}, "the receipt could not be written"),
            ("a receipt with no path", {"receipt": {"sha256": "x"}}, "the receipt could not be written")):
        rec, said, _ref, task = _publish_scenario(made, over=over)
        check_eq(f"D5 {label}: the publish dict", rec["publish"], {"published": False, "why": why})
        check_eq(f"D5 {label}: the line returned", said, f"no live receipt, nothing published ({why})")
    rec, said, _ref, task = _publish_scenario(made, over={"instance_id": "nowhere"})
    check_eq("D5 an instance the manifest does not hold: published False", rec["publish"]["published"], False)
    check_eq("D5 an instance the manifest does not hold: the refusal's own words are the reason, and the line",
             said, "nothing published: " + rec["publish"]["why"])
    check_in("D5 an instance the manifest does not hold: it names the instance", "nowhere", rec["publish"]["why"])
    # a record that is not an intended_failure: "" and nothing touched
    rec, _said, _ref, task = _publish_scenario(made)
    before_manifest = (task / "work" / "automation-manifest.json").read_bytes()
    scratch_before = sorted(p.name for p in Path(tempfile.gettempdir()).glob("qa-probe-binding-*"))
    for verdict in ("no_failure", "wrong_location", "not_executed", "incomplete", "already_probed", None):
        other = {k: v for k, v in rec.items() if k != "publish"}
        other["verdict"] = verdict
        frozen = json.loads(json.dumps(other))
        check_eq(f"D5 verdict {verdict}: returns the empty string", PBC.publish_binding(TASK, task, other), "")
        check_eq(f"D5 verdict {verdict}: the record is as it was (no publish key)", other, frozen)
    check_eq("D5 verdicts that publish nothing: the manifest bytes are as they were",
             (task / "work" / "automation-manifest.json").read_bytes(), before_manifest)
    check_eq("D5 no scratch folder is left behind, by a publish or a non-publish",
             sorted(p.name for p in Path(tempfile.gettempdir()).glob("qa-probe-binding-*")), scratch_before)


def hostile_instance_ids() -> None:
    """The receipt writer meets ids a file system does not: `::`, `[`, `/`, non-ASCII, and 120/121/300
    characters (AT and BEYOND the stem limit `contract.instance_file_stem` puts on a name)."""
    tmp = temp_dir("q-")
    try:
        ids = ["TC-1::test_x[a/b]", "test_é[ü-日本]", "a" * 119, "a" * 120, "a" * 121, "a" * 300,
               "a" * 299 + "b", "TC::x[" + "ü" * 300 + "]", "::", "///", "[[]]", "con", "x y\tz"]
        seen = {}
        for iid in ids:
            body = {"instance_id": iid, "case_version": "cv_1", "test_content_hash": "t", "proof_level": "live",
                    "probe_tool": "probe_by_code.py", "evidence_refs": [], "immutable": True}
            ref, note = PBC.write_receipt(tmp, body, iid)
            label = iid if len(iid) < 30 else f"{iid[:8]}...({len(iid)} chars)"
            check(f"battery {label}: written", ref is not None, note)
            if ref is None:
                continue
            path = tmp / ref["path"]
            check(f"battery {label}: on disk under sensitivity-receipts/ with a portable name",
                  path.is_file() and path.parent == tmp / "work" / "sensitivity-receipts"
                  and len(path.name) <= 255 and not any(ch in path.name for ch in '<>:"/\\|?*[]'), path.name)
            check_eq(f"battery {label}: the id survives the round trip",
                     json.loads(path.read_text(encoding="utf-8"))["instance_id"], iid)
            check_eq(f"battery {label}: the ref's hash is the file's", ref["sha256"], PBC.sha256(path.read_bytes()))
            again, _ = PBC.write_receipt(tmp, body, iid)
            check_eq(f"battery {label}: the same facts again are the same path", again, ref)
            check(f"battery {label}: its own file", ref["path"] not in seen.values(), ref["path"])
            seen[iid] = ref["path"]
        check_eq("ids that share their first 120 characters still get different files",
                 seen.get("a" * 300) != seen.get("a" * 299 + "b"), True)
        stem = C.instance_file_stem("a" * 120)
        check_eq("AT the stem limit the stem is the id itself", stem, "a" * 120)
        check("BEYOND it the stem is cut and told apart by a hash", len(C.instance_file_stem("a" * 121)) < 121 + 10
              and C.instance_file_stem("a" * 121) != "a" * 121)
        # An existing file under that very name with other content is never overwritten.
        body = {"instance_id": "clash", "proof_level": "live", "evidence_refs": [], "immutable": True}
        ref, _ = PBC.write_receipt(tmp, body, "clash")
        clash = tmp / ref["path"]
        clash.write_text('{"someone": "else"}', encoding="utf-8")
        got, note = PBC.write_receipt(tmp, body, "clash")
        check_eq("a same-name file with other content: no receipt", got, None)
        check_in("...and the note says nothing was overwritten", "never overwritten", note)
        check_eq("...and the file is as it was", clash.read_text(encoding="utf-8"), '{"someone": "else"}')
        # Same name, right hash field, changed content: also a collision, never a match.
        forged = dict(body, immutable=False, receipt_hash=PBC._hash_of(body))
        clash.write_text(json.dumps(forged), encoding="utf-8")
        got, note = PBC.write_receipt(tmp, body, "clash")
        check_eq("a file claiming this receipt's hash over other content: no receipt", got, None)
        # A file where the directory should be: the writer reports, it does not raise.
        blocker = temp_dir("q-")
        try:
            (blocker / "work").write_text("not a directory", encoding="utf-8")
            got, note = PBC.write_receipt(blocker, body, "clash")
            check_eq("an unwritable target: no receipt, a note, no traceback", (got, "could not be written" in note),
                     (None, True))
        finally:
            cleanup(blocker)
    finally:
        cleanup(tmp)
    # The run evidence differs on every run (a job summary, a junit file with its timings): the same
    # facts with other evidence are the same receipt, at the same path, and the first file stays.
    tmp2 = temp_dir("q-")
    try:
        body = {"instance_id": "ev", "proof_level": "live", "immutable": True,
                "evidence_refs": [{"path": "evidence/one", "sha256": "1" * 64}]}
        first, _ = PBC.write_receipt(tmp2, body, "ev")
        frozen = (tmp2 / first["path"]).read_bytes()
        second, note = PBC.write_receipt(tmp2, dict(body, evidence_refs=[{"path": "evidence/two", "sha256": "2" * 64}]), "ev")
        check_eq("other run evidence, same facts: the same path", second, first)
        check_eq("...and the first file is untouched", (tmp2 / first["path"]).read_bytes(), frozen)
        check_eq("...with no scratch file left behind",
                 sorted(p.name for p in (tmp2 / "work" / "sensitivity-receipts").iterdir()), [Path(first["path"]).name])
    finally:
        cleanup(tmp2)
    # An id with `::`, `[` and `/` through the PUBLISH too: the row and the binding find it again.
    root = project()
    try:
        task = task_of(root)
        use_project(root)
        iid = "TC-9::test_x[a/b-é]"
        manifest = manifest_of(root)
        manifest["tests"] = [entry("TC-100", "test_add", iid, obligation_ids=["OB-ADD-1"])]
        write_json(task / "work" / "automation-manifest.json", manifest)
        body = {"instance_id": iid, "case_version": "cv_1", "test_content_hash": "t", "source_revision": "s",
                "build_id": "b", "mutation": "invert", "expected_assertion_failure": "e", "actual_failure": "e",
                "assertion_location": "t.py:1", "restoration_evidence": "r", "failure_kind": "assertion",
                "proof_level": "live", "probe_tool": "probe_by_code.py", "mutation_kind": "assertion",
                "evidence_refs": [], "immutable": True}
        ref, _ = PBC.write_receipt(task, body, iid)
        rec = {"verdict": "intended_failure", "instance_id": iid, "receipt": ref, "obligation_ids": ["OB-ADD-1"],
               "restore": {"verified": True}}
        PBC.publish_binding(TASK, task, rec)
        row = next(t for t in manifest_of(root)["tests"] if t.get("instance_id") == iid)
        check_eq("hostile id: the row carries the receipt", (row.get("sensitivity_proof") or {}).get("receipt_ref"), ref)
        check_eq("hostile id: the binding lists the id", binding_of(root).get("instance_ids"), [iid])
    finally:
        cleanup(root)
        cleanup_beside(root)


def an_unverified_restore_writes_no_receipt(stub: Path) -> None:
    """The bytes of the author's file are the probe's promise; a receipt vouching for a restore nobody
    verified would be the tool's own failure dressed as a proof."""
    root = project()
    try:
        _unverified_restore(root, stub)
    finally:
        cleanup(root)
        cleanup_beside(root)


def _unverified_restore(root: Path, stub: Path) -> None:
    use_project(root)
    task = task_of(root)
    real = PBC.restore
    old_env = os.environ.get("PROBE_RUN_SUITE")
    os.environ["PROBE_RUN_SUITE"] = str(stub)
    PBC.restore = lambda *args, **kw: dict(real(*args, **kw), verified=False)
    model_entries(root, stub, f"{TEST_FILE_REL}::test_add", "test_add")
    try:
        record = PBC.probe(TASK, DISPATCH, f"{TEST_FILE_REL}::test_add", "test_add", "invert")
    finally:
        PBC.restore = real
        if old_env is None:
            os.environ.pop("PROBE_RUN_SUITE", None)
        else:
            os.environ["PROBE_RUN_SUITE"] = old_env
    # t-2064 P4b: the walk's aggregate does not call a plan with an unverified restore `intended_failure` at all (a failed restore ends the
    # walk): the verdict is `incomplete`, the restore says it was not verified, and `publish_binding` has nothing to publish (it publishes
    # `intended_failure` only) - the receipt is as absent as before, by one more gate.
    check_eq("unverified restore: the walk answers incomplete, with the restore unverified",
             (record.get("verdict"), (record.get("restore") or {}).get("verified")), ("incomplete", False))
    check_eq("unverified restore: no receipt", record.get("receipt"), None)
    check_eq("unverified restore: no receipt file", receipt_files(root), [])
    said = PBC.publish_binding(TASK, task, record)
    check_eq("unverified restore: nothing is published", (said, "published" in (record.get("publish") or {})), ("", False))
    check_eq("unverified restore: the manifest row is untouched", "sensitivity_proof" in row_of(root), False)


def the_receipt_flow() -> None:
    stub_dir = temp_dir("qa-probe-stub-")
    stub = stub_dir / "fake_run_suite.py"
    stub.write_text(FAKE_RUN_SUITE, encoding="utf-8")
    root = project()
    use_project(root)  # the in-process readers (reached) read the test's bytes under this project
    try:
        first = live_receipt_and_publish(root, stub)
        a_rerun_is_idempotent_and_new_bytes_are_a_new_receipt(root, stub, first)
    finally:
        cleanup(root)
        cleanup_beside(root)
    try:
        publish_orders()
        publish_dicts_are_pinned()
        hostile_instance_ids()
        an_unverified_restore_writes_no_receipt(stub)
    finally:
        cleanup(stub_dir)


def main() -> None:
    the_receipt_flow()
    finish("test_probe_by_code_receipts")


# split: runner piece 1
if __name__ == "__main__":
    main()
