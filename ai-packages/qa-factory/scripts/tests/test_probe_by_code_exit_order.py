"""exit order: a part of test_probe_by_code.py, split by tools/test_split.py (TD-11c). The shared helpers are in probe_by_code_common."""
import json
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import (SCRIPTS, check, check_eq, check_in, check_not_in, cleanup, finish, run_script,  # noqa: E402
                     mark_project, temp_dir, use_project)
sys.path.insert(0, str(SCRIPTS))
import contract as C  # noqa: E402
import probe_by_code as PBC  # noqa: E402
import proof_level as PL  # noqa: E402
import probe_entries  # noqa: E402
del probe_entries  # split: imported for its sys.path effect
from event_store import content_hash  # noqa: E402
from probe_by_code_common import (  # noqa: E402
    DISPATCH, FAKE_RUN_SUITE, TASK, TEST_FILE_REL, _calls, _main_in_process, _streams, binding_of,
    cleanup_beside, model_entries, project, receipt_files, row_of, run, task_of, write_json,
)


def through_real_run_suite() -> None:
    """The real `run_suite.py --request` accepts the request the script writes: a fresh
    project whose `pytest` is the red_sandbox test's stand-in (it imports the product and runs
    the function; no real pytest anywhere) — the typed request validates, the job store takes
    it, the evidence lands under the task, and the verdict comes back through the same reader."""
    from test_red_sandbox_probe import FAKE_PYTEST
    root = project()
    fake_pytest = root.parent / (root.name + "-bin") / "pytest"
    fake_pytest.write_text(FAKE_PYTEST, encoding="utf-8")
    original = (root / TEST_FILE_REL).read_bytes()
    try:
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(root))
        env.pop("PROBE_RUN_SUITE", None)
        model_entries(root, None, f"{TEST_FILE_REL}::test_add", "test_add")
        proc = run_script("probe_by_code.py", "--task", TASK, "--dispatch", DISPATCH, "--test",
                          f"{TEST_FILE_REL}::test_add", "--instance", "test_add", "--json",
                          cwd=root, env=env)
        record = json.loads(proc.stdout) if proc.stdout.strip().startswith("{") else {}
        check("real run_suite: exit 0", proc.returncode == 0, proc.stdout + proc.stderr)
        check_eq("real run_suite: intended_failure through the real runner", record.get("verdict"), "intended_failure")
        # t-2064 P4b: the aggregate has no `run` block; the run's label is the name of the evidence file it names
        check_eq("real run_suite: the label is a red_probe run (the evidence file's name)",
                 Path(str(record.get("evidence_ref") or "")).name[:10], "red_probe-")
        task_root = root / "qa-factory" / "artifacts" / TASK
        check("real run_suite: no run block was written for the red probe",
              not list((task_root / "work" / "run-blocks").glob("*")) or
              all("author1" in p.name for p in (task_root / "work" / "run-blocks").glob("*")))
        jobs = list((task_root / "state" / "execution-jobs").glob("*.json"))
        check("real run_suite: the job store holds the probe's job", len(jobs) >= 1)
        check_eq("real run_suite: the bytes are back", (root / TEST_FILE_REL).read_bytes(), original)
    finally:
        cleanup(root)
        cleanup_beside(root)


def _first(log: list, tag: str) -> int:
    return next((i for i, entry in enumerate(log) if entry[0] == tag), -1)


def _last(log: list, tag: str) -> int:
    return max((i for i, entry in enumerate(log) if entry[0] == tag), default=-1)


def main_exit_order_is_pinned() -> None:
    """t-667 D6, characterisation: the `sys.exit` order of `main` is already_probed -> publish -> print ->
    restore check -> verdict exit, and each exit code and printed byte is as before. `probe` is replaced by a
    record, so the unrestored branch, which no stub run reaches, is pinned too (the process is the real
    `main`, the argv the real CLI)."""
    root = temp_dir("qa-probe-main-")
    mark_project(root)                                               # the story below is a story of a project (CX1-18)
    (root / "qa-factory" / "artifacts" / "T-1").mkdir(parents=True)
    use_project(root)
    base = root.resolve()
    argv = ["--task", "T-1", "--dispatch", "D-1", "--test", "tests/t.py::test_x", "--instance", "iid"]
    record = {"instance_id": "iid", "verdict": "intended_failure", "expected_location": "t.py:6",
              "expected_reason": "marker", "actual_location": "t.py:7", "actual_reason": "word " * 40,
              "record": "work/probes/iid.json", "evidence_ref": "evidence/e.json", "restore": {"verified": True},
              "notes": ["n1", "n2"], "test_node": "tests/t.py::test_x", "test_file_sha256": "f" * 64}
    # the reason is folded to 120 characters: 119 and an ellipsis
    printed = ("probe iid: intended_failure — expected t.py:6 / 'marker'; actual t.py:7 / "
               + repr(("word " * 40).strip()[:119] + "…") + "\n"
               "record work/probes/iid.json; evidence evidence/e.json; restore verified\n")
    try:
        # already probed: answered before the publish and before the restore check, exit 0 either way
        answered = {"verdict": "already_probed", "instance_id": "iid", "words": "the words", "notes": ["a", "b"],
                    "restore": {"verified": False}}
        code, log = _main_in_process(argv, dict(answered), publish=("never", True))
        check_eq("D6 already_probed (text): exit 0, publish never called, calls are probe only",
                 (code, _calls(log)), (0, ["probe"]))
        check_eq("D6 already_probed (text): the bytes", _streams(log),
                 ("probe iid: already_probed — the words\nnote: a\nnote: b\n", ""))
        code, log = _main_in_process(argv + ["--json"], dict(answered), publish=("never", True))
        check_eq("D6 already_probed (json): exit 0, one JSON object, publish never called",
                 (code, _calls(log), _streams(log)),
                 (0, ["probe"], (json.dumps(answered, ensure_ascii=False, indent=1) + "\n", "")))
        args = next(entry[2] for entry in log if entry[0] == "call" and entry[1] == "probe")
        check_eq("D6 the probe is called with the CLI's values, positionally",
                 args, ("T-1", "D-1", "tests/t.py::test_x", "iid", "invert", PBC.RUN_TIMEOUT_S, "", None))
        code, log = _main_in_process(argv + ["--mutation", "invert", "--timeout", "7", "--oracle", "h::f",
                                             "--at", "12"], dict(answered))
        args = next(entry[2] for entry in log if entry[0] == "call" and entry[1] == "probe")
        check_eq("D6 the probe is called with --mutation --timeout --oracle --at as given",
                 args, ("T-1", "D-1", "tests/t.py::test_x", "iid", "invert", 7, "h::f", 12))
        # a verdict, text: probe -> publish -> print (the publish saw nothing printed) -> verdict exit
        for verdict, want in (("intended_failure", 0), ("no_failure", 0), ("wrong_location", 0),
                              ("not_executed", 1), ("incomplete", 1), ("unheard_of", 1)):
            code, log = _main_in_process(argv, dict(record, verdict=verdict, notes=list(record["notes"])),
                                         publish=("the binding line", True))
            out, err = _streams(log)
            check_eq(f"D6 {verdict}: exit {want}; probe then publish", (code, _calls(log)), (want, ["probe", "publish"]))
            check_eq(f"D6 {verdict}: published with the task and the task's artifacts folder",
                     next(e[2] for e in log if e[0] == "call" and e[1] == "publish"),
                     ("T-1", Path(PBC.artifacts_dir("T-1")).as_posix()))
            check(f"D6 {verdict}: the publish ran before the first byte was printed",
                  _first(log, "out") > max(i for i, e in enumerate(log) if e[:2] == ("call", "publish")))
            check_eq(f"D6 {verdict}: the text, binding line between the record line and the notes",
                     out, printed.replace("intended_failure —", verdict + " —")
                     + "binding: the binding line\nnote: n1\nnote: n2\n")
            check_eq(f"D6 {verdict}: nothing on stderr", err, "")
        # the publish goes back into the record's own file; with --json the whole of stdout is one object
        written = base / "qa-factory" / "artifacts" / "T-1" / "work" / "probes" / "iid.json"
        sent = dict(record, notes=list(record["notes"]))
        code, log = _main_in_process(argv + ["--json"], sent, publish=("bound it", True))
        out, _err = _streams(log)
        check_eq("D6 json: exit 0 and stdout is exactly the record, binding and publish in it",
                 (code, out), (0, json.dumps(dict(record, publish={"published": True}, binding="bound it"),
                                             ensure_ascii=False, indent=1) + "\n"))
        check_eq("D6 json: the publish was written into the record's file",
                 json.loads(written.read_text(encoding="utf-8")) if written.is_file() else None,
                 dict(record, binding="bound it", publish={"published": True}))
        written.unlink()
        code, log = _main_in_process(argv, dict(record, notes=list(record["notes"])), publish=("", False))
        check_eq("D6 nothing published: no binding line, no file written",
                 (_streams(log)[0], written.is_file()), (printed + "note: n1\nnote: n2\n", False))
        # the write of the publish fails: a note, never a crash, and the note is printed
        blocker = base / "qa-factory" / "artifacts" / "T-1" / "blocked"
        blocker.parent.mkdir(parents=True, exist_ok=True)
        blocker.write_text("a file where a folder should be", encoding="utf-8")
        code, log = _main_in_process(argv + ["--json"], dict(record, record="blocked/iid.json", notes=["n1"]),
                                     publish=("x", True))
        shown = json.loads(_streams(log)[0])
        check_eq("D6 an unwritable record: still exit 0", code, 0)
        check_eq("D6 an unwritable record: the note says so, after the earlier notes",
                 (shown["notes"][0], shown["notes"][1].startswith("the publish could not be written into the record: ")),
                 ("n1", True))
        # the restore check comes after the print and before the verdict exit
        mutated = {"path": "tests/helper.py", "sha256": "s" * 64}
        for label, over, undo in (
                ("a copy kept", {"restore": {"verified": False, "copy": "state/probe-copies/abc.orig"},
                                 "mutated_file": mutated},
                 f"copy {base / 'state/probe-copies/abc.orig'} over {base / 'tests/helper.py'}"),
                ("no copy", {"restore": {"verified": False}, "mutated_file": mutated}, "restore tests/helper.py by hand"),
                ("no restore at all, no mutated_file: the test's own file and sha", {"restore": None},
                 "restore tests/t.py by hand")):
            sha = mutated["sha256"] if "mutated_file" in over else record["test_file_sha256"]
            file_rel = mutated["path"] if "mutated_file" in over else "tests/t.py"
            code, log = _main_in_process(argv, dict(record, notes=list(record["notes"]), **over),
                                         publish=("the binding line", True))
            out, err = _streams(log)
            check_eq(f"D6 unrestored ({label}): exit 1 although the verdict is intended_failure", code, 1)
            check_eq(f"D6 unrestored ({label}): the whole record is printed first, and says NOT VERIFIED",
                     out, printed.replace("restore verified", "restore NOT VERIFIED")
                     + "binding: the binding line\nnote: n1\nnote: n2\n")
            check_eq(f"D6 unrestored ({label}): the stop line, on stderr, with the one move that undoes it",
                     err, f"PROBE: the author's bytes of {file_rel} could not be verified restored (sha256 {sha}) "
                          f"— stop and {undo}\n")
            check(f"D6 unrestored ({label}): publish, then stdout, then stderr",
                  _last(log, "out") < _first(log, "err")
                  and max(i for i, e in enumerate(log) if e[:2] == ("call", "publish")) < _first(log, "out"))
        # a refusal: one JSON line on stdout, exit 2, nothing published
        code, log = _main_in_process(argv, PBC.Refusal("no file x under the project root"))
        check_eq("D6 a refusal: exit 2, the JSON line, no publish",
                 (code, _calls(log), _streams(log)),
                 (2, ["probe"], (json.dumps({"status": "refused", "error": "no file x under the project root"},
                                             ensure_ascii=False) + "\n", "")))
        # a missing argument is the parser's: exit 2, naming every one, no probe
        code, log = _main_in_process(["--task", "T-1"])
        out, err = _streams(log)
        check_eq("D6 missing arguments: exit 2, nothing probed, nothing on stdout", (code, _calls(log), out), (2, [], ""))
        check_in("D6 missing arguments: all three are named", "the following arguments are required: --dispatch, "
                 "--test, --instance", err)
        check_not_in("A-K10 the role's text does not show the driver's door", "--s6-close",
                     err.split("required:")[-1])
        # A-K10 (HF3-6): the third form of the call. `s6_close` goes as a KEYWORD, so the positional pin above stays
        # as it was; one context per call; the dispatch id is "" in the close context.
        code, log = _main_in_process(argv, dict(answered))
        check_eq("A-K10 the ordinary call passes s6_close=False as a keyword",
                 next(e[3] for e in log if e[0] == "call" and e[1] == "probe"), {"s6_close": False})
        close_argv = ["--task", "T-1", "--s6-close", "--test", "tests/t.py::test_x", "--instance", "iid"]
        code, log = _main_in_process(close_argv, dict(answered))
        got = next(e for e in log if e[0] == "call" and e[1] == "probe")
        check_eq("A-K10 --s6-close: the probe is called with an empty dispatch and s6_close=True",
                 (code, got[2][:2], got[3]), (0, ("T-1", ""), {"s6_close": True}))
        code, log = _main_in_process(argv + ["--s6-close"], dict(answered))
        out, err = _streams(log)
        check_eq("A-K10 --dispatch with --s6-close: exit 2, nothing probed", (code, _calls(log), out), (2, [], ""))
        check_in("A-K10 --dispatch with --s6-close: 'use one' names both",
                 "use one: --dispatch <id> (an open dispatch) or --s6-close (the code close of S6)", err)
        # --release-copy: exits before anything else, refused 2, released 0, json or text
        code, log = _main_in_process(["--release-copy", "tests/x.py"], release=PBC.Refusal("a probe is running"))
        check_eq("D6 release refused: exit 2, JSON line, no probe", (code, _calls(log), _streams(log)),
                 (2, ["release"], (json.dumps({"status": "refused", "error": "a probe is running"},
                                              ensure_ascii=False) + "\n", "")))
        check_eq("D6 release is given the project root and the argument",
                 next(e[2] for e in log if e[0] == "call" and e[1] == "release"), (base.as_posix(), "tests/x.py"))
        released = {"status": "released", "file": "tests/x.py", "copy": "abc.orig", "record": {"a": 1}}
        code, log = _main_in_process(["--release-copy", "tests/x.py"] + argv, release=dict(released))
        check_eq("D6 release (text, no message): exit 0, the sentence, nothing probed",
                 (code, _calls(log), _streams(log)),
                 (0, ["release"], ('released the byte copy of tests/x.py (abc.orig); its record was {"a": 1}\n', "")))
        code, log = _main_in_process(["--release-copy", "tests/x.py"], release=dict(released, message="its message"))
        check_eq("D6 release (text, with a message): the message", (code, _streams(log)), (0, ("its message\n", "")))
        code, log = _main_in_process(["--release-copy", "tests/x.py", "--json"], release=dict(released))
        check_eq("D6 release (json): the dict, indented", (code, _streams(log)),
                 (0, (json.dumps(released, ensure_ascii=False, indent=1) + "\n", "")))
    finally:
        cleanup(root)


def missing_facts_and_a_refused_publish_do_not_change_the_exit() -> None:
    """Through the CLI: no build identity in any run block -> no receipt, `receipt_missing[]`, exit 0;
    a manifest_put that refuses -> the receipt stays, a note, exit 0."""
    stub_dir = temp_dir("qa-probe-stub-")
    stub = stub_dir / "fake_run_suite.py"
    stub.write_text(FAKE_RUN_SUITE, encoding="utf-8")
    bare = project(provenance=False)
    try:
        proc, record = run(bare, stub, f"{TEST_FILE_REL}::test_add", "test_add")
        check("no build identity: exit 0 (a verdict was recorded)", proc.returncode == 0, proc.stdout + proc.stderr)
        check_eq("no build identity: intended_failure", record.get("verdict"), "intended_failure")
        check_eq("no build identity: no receipt", record.get("receipt"), None)
        check_eq("no build identity: the missing fact is named", record.get("receipt_missing"), ["build_id"])
        check_in("no build identity: the note says where it belongs", "run block", " ".join(record.get("notes") or []))
        check_eq("no build identity: no receipt file", receipt_files(bare), [])
        check_eq("no build identity: nothing published on the row", "sensitivity_proof" in row_of(bare), False)
        check_eq("no build identity: no binding either", binding_of(bare), {})
        check_eq("no build identity: the record says why nothing was published",
                 ((record.get("publish") or {}).get("published"), "build_id" in str((record.get("publish") or {}).get("why"))),
                 (False, True))
    finally:
        cleanup(bare)
        cleanup_beside(bare)
    refused = project()
    try:
        write_json(task_of(refused) / "work" / "test-plan.json", {"rows": [{
            "id": "TS-1", "schema_version": 2, "coverage_obligations": [{"obligation_id": "OB-OTHER", "text": "x"}]}]})
        proc, record = run(refused, stub, f"{TEST_FILE_REL}::test_add", "test_add")
        check("manifest_put refuses: exit unchanged (0)", proc.returncode == 0, proc.stdout + proc.stderr)
        check("manifest_put refuses: the receipt stays on disk",
              len(receipt_files(refused)) == 1 and (task_of(refused) / record["receipt"]["path"]).is_file())
        check_eq("manifest_put refuses: the record says published False", (record.get("publish") or {}).get("published"),
                 False)
        check_in("manifest_put refuses: with the refusal", "refused", str((record.get("publish") or {}).get("manifest_put")))
        check_in("manifest_put refuses: and the printed line", "manifest_put refused", str(record.get("binding")))
        check_eq("manifest_put refuses: the row was not touched", "sensitivity_proof" in row_of(refused), False)
    finally:
        cleanup(refused)
        cleanup_beside(refused)
        cleanup(stub_dir)


def _probe_record(row: dict, measured: str, fingerprint: str, node: str, code: str = "") -> dict:
    """The record `probe()` hands `attach_receipt` after an intended failure with a verified restore:
    `test_file_sha256` is the raw file measured before the mutation, `input_hash` the run's
    fingerprint - two quantities over the same bytes."""
    fields, _missing = PBC.obligation_fields(row)
    return {"instance_id": row["instance_id"], "verdict": "intended_failure", "mutation": "invert",
            "expected_reason": "probe-x invert", "actual_reason": "probe-x invert",
            "expected_location": node.split("::")[0] + ":12", "failure_kind": "assertion",
            "record": "work/probes/x.json", "test_node": node, "mutation_detail": {"line": 12},
            "restore": {"verified": True, "sha256": measured}, "test_file_sha256": measured,
            "test_code_sha": code, "input_hash": fingerprint, "evidence_refs": [], "notes": [], **fields}


def raw_bytes_through_manifest_from_tests() -> None:
    """Amendment 2 of t-016 (critic t-035): `test_content_sha` is the RAW sha256 of the test file -
    what manifest_from_tests.py writes and validate_artifacts enforces - and a run block's
    `source_fingerprint.test_content_sha` is a fingerprint over the test AND helper files, another
    quantity. On driver3 the same bytes read 6992616693fc... and bd6d28d6aade..., and the gate that
    compared the fingerprint with the binding refused a receipt to every correctly bound row.

    Here the manifest is BUILT by manifest_from_tests.py and the run block carries a real
    fingerprint; the MEASURED BYTES gate writes the receipt for unchanged bytes and refuses it, with
    the door, once the file changed."""
    import test_manifest_from_tests as MFT
    from harness import temp_project
    root = temp_project("qa-probe-raw-")
    try:
        task = MFT.seed(root)
        use_project(root)
        wrote = MFT.run(root)
        check("raw bytes: manifest_from_tests.py writes the manifest", wrote.returncode == 0, wrote.stdout + wrote.stderr)
        manifest = json.loads((task / "work" / "automation-manifest.json").read_text(encoding="utf-8"))
        row = next(t for t in manifest["tests"] if t.get("instance_id") == "test_limit")
        test_file, helper = root / "tests" / "test_coupon.py", root / "tests" / "data_coupon.py"
        raw = PBC.sha256(test_file.read_bytes())
        check_eq("raw bytes: the manifest binds the file's raw sha256", row["trace_binding"]["test_content_sha"], raw)

        def fingerprint() -> str:  # execution_fingerprint.build's test_content_sha, over the same records
            return content_hash([{"path": str(test_file.resolve()), "sha256": PBC.sha256(test_file.read_bytes()),
                                  "kind": "test_files"},
                                 {"path": str(helper.resolve()), "sha256": PBC.sha256(helper.read_bytes()),
                                  "kind": "helper_files"}])
        run_fp = fingerprint()
        check("raw bytes: the run's fingerprint of the same bytes is another quantity", run_fp != raw, run_fp)
        components = {"source_sha": "src-9", "test_content_sha": run_fp}
        write_json(task / "work" / "run-blocks" / "20260929T090000000000Z-raw.json", {
            "schema_version": 2, "dispatch_id": "S5-qa-automator-1", "purpose": "initial",
            "input_fingerprint": "fp-raw", "source_fingerprint": components,
            "runtime_provenance": {"observed_runtime_identity": "build-9", "environment_id": "env-9"},
            "results": [{"instance_id": "test_limit", "status": "passed", "source_fingerprint": components}]})
        node = row["selector"]
        record = _probe_record(row, raw, run_fp, node, PL.code_sha(test_file.read_bytes()))
        PBC.attach_receipt(record, row, task)
        ref = record.get("receipt") or {}
        check("raw bytes, unchanged: the live receipt IS written", bool(ref.get("path")),
              json.dumps(record.get("notes")))
        check_eq("raw bytes, unchanged: nothing missing", record.get("receipt_missing"), [])
        body = json.loads((task / ref["path"]).read_text(encoding="utf-8")) if ref.get("path") else {}
        check_eq("raw bytes: the receipt binds the raw hash, never the fingerprint",
                 (body.get("test_content_hash"), body.get("source_revision"), body.get("build_id")),
                 (raw, "src-9", "build-9"))
        proven = dict(row, sensitivity_proof={"receipt_ref": ref})
        check_eq("raw bytes: the contract accepts it unchanged", C.sensitivity_proof_issues(proven, task), [])
        check_eq("raw bytes: and reached() shows the check is live", PL.reached(proven, manifest, task)["level"], "live")

        # The test file changes by a COMMENT; the manifest still binds the old bytes.
        test_file.write_bytes(test_file.read_bytes() + b"\n# edited after the review\n")
        changed = PBC.sha256(test_file.read_bytes())
        record = _probe_record(row, changed, fingerprint(), node, PL.code_sha(test_file.read_bytes()))
        PBC.attach_receipt(record, row, task)
        # MEASURED BYTES stays raw (Amendment 3): the claim must be the bytes measured.
        check_eq("raw bytes, changed: NO new receipt", record.get("receipt"), None)
        check_eq("raw bytes, changed: the stale fact is named", record.get("receipt_missing"), ["test_content_hash"])
        check_in("raw bytes, changed: the door is the author's rebind through manifest_put, no run",
                 "It is the author's to rebind, through `manifest_put.py` (no run needed): "
                 "trace_binding.test_content_sha is the sha256 of the file's bytes", " ".join(record["notes"]))
        # ...but the first receipt still counts: the change was comment-only (D-0017, Amendment 3)
        got = PL.reached(proven, manifest, task)
        check_eq("comment-only edit: the first receipt still counts, and says why",
                 (got["level"], got["words"]), ("live", "the check is live (the receipt holds over a comment-only change)"))
        # an executable line changed: other code, the receipt no longer counts
        test_file.write_bytes(test_file.read_bytes().replace(b'assert body["count"] == 1', b'assert body["count"] == 2'))
        check("raw bytes: the assert really changed", PBC.sha256(test_file.read_bytes()) != changed)
        check_eq("an assert changed: the first receipt no longer counts for the changed test",
                 PL.reached(proven, manifest, task)["level"], None)
        check_eq("raw bytes: still exactly one receipt file",
                 len(list((task / "work" / "sensitivity-receipts").glob("test_limit-live-*.json"))), 1)
    finally:
        cleanup(root)


def main() -> None:
    main_exit_order_is_pinned()
    missing_facts_and_a_refused_publish_do_not_change_the_exit()
    raw_bytes_through_manifest_from_tests()
    through_real_run_suite()
    finish("test_probe_by_code_exit_order")


# split: runner piece 1
if __name__ == "__main__":
    main()
