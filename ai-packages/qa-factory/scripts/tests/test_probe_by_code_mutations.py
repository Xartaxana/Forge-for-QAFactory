"""mutations: a part of test_probe_by_code.py, split by tools/test_split.py (TD-11c). The shared helpers are in probe_by_code_common."""
import hashlib
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import SCRIPTS, check, check_eq, check_in, check_not_in, cleanup, finish, run_script, temp_dir
sys.path.insert(0, str(SCRIPTS))
import acceptance  # noqa: E402
import assertion_detectors as AD  # noqa: E402
import probe_by_code as PBC  # noqa: E402
import proof_level as PL  # noqa: E402
import probe_entries  # noqa: E402
del probe_entries  # split: imported for its sys.path effect
from event_store import content_hash  # noqa: E402
from probe_by_code_common import (  # noqa: E402
    DISPATCH, FAKE_RUN_SUITE, OBLIGATION_REFS, PY, TASK, TEST_FILE, TEST_FILE_REL, cleanup_beside, env_for,
    model_entries, mutated_line, project, read_check_record, read_record, run, tree_state, write_json,
)


# --- comparing two receipts -----------------------------------------------------------------------
# Two runs of one scenario differ in the time, the job id the idempotency key hashes, the fingerprint
# over temp paths and the evidence file that names the job: `normalised` takes those out, so a receipt
# can be compared with the receipt of the same scenario read another way (`reporter_in_the_summary`).
# The golden receipts that once pinned a byte-for-byte digest of whole receipts are gone: they were
# taken from code that wrote `mutation_kind: real_behavior`, which 0.8.1 changed to `assertion`.

def normalised(root: Path, returncode: int, record: dict) -> dict:
    """The receipt with what differs between two runs of the SAME code taken out."""
    text = json.dumps({"rc": returncode, "record": record}, sort_keys=True)
    text = text.replace(str(root).replace("\\", "\\\\"), "<ROOT>").replace(str(root), "<ROOT>")
    # t-2045 N2: a Python plan now carries a per-run probe token (`qa-probe-<12 hex>` in the message, `'<12 hex>'` inside the
    # joined expression); only those two spellings are masked, so the rest of the statement still compares byte for byte.
    text = re.sub(r"qa-probe-[0-9a-f]{12}\b", "qa-probe-<TOKEN>", text)
    text = re.sub(r"(\['qa-probe', ')[0-9a-f]{12}('\])", r"\1<TOKEN>\2", text)
    # t-2064 TR2-14: a receipt file named inside the notes carries the project's hash (`<check>-live-<16 hex>.json`): masked, the rest of the note compares.
    text = re.sub(r"-live-[0-9a-f]{16}", "-live-<HASH>", text)
    value = json.loads(re.sub(r"\b[0-9a-f]{20}\b", "<JOB>", text))
    rec = value["record"]
    rec.pop("recorded_at", None)
    # The receipt's file name carries a hash of the project it was written in, and so do the manifest
    # revision and the publication line that name it: each comparison here runs in a project of its own
    # (a repeat in one project is answered `already_probed`), so those are taken out too.
    for key in ("binding", "publish", "receipt"):
        rec.pop(key, None)
    if str(rec.get("input_hash_source") or "").startswith("fingerprint:"):
        rec["input_hash"] = "<varies with the temp paths>"
        rec["window_probe"]["input_hash"] = "<varies with the temp paths>"
    for ref in rec.get("evidence_refs") or []:
        if ref["path"].endswith(".json"):
            ref["sha256"] = "<varies with the job id>"
        else:
            ref["sha256"] = "<varies with the token>"     # the report file holds the failure text, which holds the token
    return value


def author_job(root: Path) -> dict:
    """The one job the fixture's story holds: the author's run."""
    import execution_request as ER
    return ER.JobStore(root / "qa-factory" / "artifacts" / TASK / "state" / "execution-jobs").jobs()[0]


def invert_plain_assert(root: Path, stub: Path) -> dict:
    original = (root / TEST_FILE_REL).read_bytes()
    proc, record = run(root, stub, f"{TEST_FILE_REL}::test_add", "test_add")
    check("invert: exit 0", proc.returncode == 0, proc.stdout + proc.stderr)
    check_eq("invert: the verdict is intended_failure", record.get("verdict"), "intended_failure")
    check_eq("invert: expected_location is the assert's line", record.get("expected_location"),
             f"{TEST_FILE_REL}:6")
    check_eq("invert: actual_location equals it", record.get("actual_location"), record.get("expected_location"))
    # t-2064 P4b: the answer is the walk's aggregate; its reason says how many checks of the plan were proved (it was the marker's id
    # when one line was probed by the old default)
    check_eq("invert: expected_reason says the plan's checks were proved", record.get("expected_reason"),
             "1 of 1 checks of the plan proved")
    check_eq("invert: actual_reason equals it", record.get("actual_reason"), record.get("expected_reason"))
    check_eq("invert: failure_kind assertion", record.get("failure_kind"), "assertion")
    # D-0010: this tool mutates the assertion, so what it proves is that the check is live; it used
    # to claim `real_behavior`, a product mutation it never makes.
    check_eq("invert: mutation_kind assertion", record.get("mutation_kind"), "assertion")
    check_eq("invert: proof_level live", record.get("proof_level"), "live")
    # t-2064 P4b: the aggregate no longer carries the mutated statement (`mutation_detail` is `{file, line, end_line, checks}`); the
    # statement is read from the bytes the stub ran (`mutated_line`), the marker's identity from the per-check record's failing text.
    detail = record.get("mutation_detail", {})
    check_eq("invert: the detail names the file and the check the walk mutated", (detail.get("file"), detail.get("checks")),
             (TEST_FILE_REL, [f"{TEST_FILE_REL}:6"]))
    row = (record.get("checks") or [{}])[0]
    check_eq("invert: the check row is the inversion, proved by its marker", (row.get("probe_kind"), row.get("proved_by"), row.get("verdict")),
             ("invert", "marker", "intended_failure"))
    joined = re.fullmatch(r"    assert not \(add\(2, 2\) == 4\), '-'\.join\(\['qa-probe', '([0-9a-f]{12})'\]\)", mutated_line(root, record, 6))
    check("invert: the mutated statement carries the marker joined at run time (t-2045 N2)", joined is not None, mutated_line(root, record, 6))
    check_eq("invert: the run's failing text names that marker, and it is in no contiguous byte of the statement",
             (read_check_record(root, "test_add").get("observed") or {}).get("message_head"),
             "AssertionError: qa-probe-" + (joined.group(1) if joined else "?"))
    check_eq("invert: obligation_ids copied from the manifest", record.get("obligation_ids"), ["OB-ADD-1"])
    check_eq("invert: obligation_hash is content_hash(obligation_refs)", record.get("obligation_hash"),
             content_hash(OBLIGATION_REFS))
    check_eq("invert: defect_location copied", record.get("defect_location"), "calc.py:2")
    check_eq("invert: assertion_id copied", record.get("assertion_id"), "add_returns_sum")
    check_eq("invert: nothing missing from the manifest entry", record.get("manifest_fields_missing"), [])
    check_eq("invert: input_hash bound to the author's run block", record.get("input_hash"), "author-tcs-1")
    check_eq("invert: and says whose it is (the walk's request carries the author's binding)", record.get("input_hash_source"),
             "the walk's request")
    task_root = root / "qa-factory" / "artifacts" / TASK
    evidence = record.get("evidence_ref")
    check("invert: evidence_ref is a task-relative file", bool(evidence) and (task_root / evidence).is_file())
    refs = {r["path"]: r["sha256"] for r in record.get("evidence_refs") or []}
    check("invert: evidence_refs carry the evidence_ref with its sha256",
          evidence in refs and refs[evidence] == PBC.sha256((task_root / evidence).read_bytes()))
    # t-2064 P4b: a walk's requests are per RUN: work/probe-requests/probe-walk-<IID>-<run>.json; the aggregate names no one request
    request_path = task_root / "work" / "probe-requests" / "probe-walk-test_add-1.json"
    check("invert: the request is under work/probe-requests/probe-walk-<IID>-<run>.json", request_path.is_file())
    request = json.loads(request_path.read_text(encoding="utf-8")) if request_path.is_file() else {}
    check_eq("invert: purpose red_probe", request.get("purpose"), "red_probe")
    check_eq("invert: exactly this instance", request.get("selected_instance_ids"), ["test_add"])
    check_in("invert: the reason names the probe", "probe-test_add", request.get("reason", ""))
    check_eq("invert: built_by names the tool", (request.get("built_by") or {}).get("tool"), "probe_by_code.py")
    check_eq("invert: the aggregate names no single request", record.get("request"), None)
    summary = json.loads((task_root / evidence).read_text(encoding="utf-8")) if evidence else {}
    check("invert: the stub ran the MUTATED bytes", summary.get("stub_seen_marker") is True
          and summary.get("stub_seen_sha256") != PBC.sha256(original))
    check_eq("invert: the file is byte-identical after the probe", (root / TEST_FILE_REL).read_bytes(), original)
    check_eq("invert: restore verified by sha256", (record.get("restore") or {}).get("verified"), True)
    # B-373 R9: the restore reads the byte copy on disk, and the copy goes only after that is verified
    # (test_probe_by_code_copy.py pins the rest: the lock, the kill, the recovery)
    # t-2064 P4b: the walk's `restore` is `{verified, sha256, runs}` (one restore for the whole walk); where it came from is the copy
    # folder's business, pinned by the next check (nothing left under state/probe-copies) and by test_probe_by_code_copy.py
    check_eq("invert: the walk restored once, after its one run", ((record.get("restore") or {}).get("runs"),
             (record.get("restore") or {}).get("sha256")), (1, PBC.sha256(original)))
    check_eq("invert: no copy or record of one is left under state/probe-copies",
             sorted(p.name for p in (root / "qa-factory" / "state" / "probe-copies").glob("*") if p.suffix != ".lock"), [])
    check_eq("invert: the record is on disk", read_record(root, "test_add").get("verdict"), "intended_failure")
    # t-043 C: the record carries the per-test identity the author's job wrote (`instance_contracts`),
    # re-measured over the bytes the probe read BEFORE it mutated anything - never a derivation of its own
    job = author_job(root)
    contract = job["request"]["instance_contracts"]["test_add"]
    check_eq("identity: the record's instance_identity is the job's contract shas, re-measured",
             record.get("instance_identity"),
             {"instance_content_sha": contract["instance_content_sha"],
              "instance_code_sha": contract["instance_code_sha"], "job_id": job["job_id"]})
    check_eq("identity: the flat instance_content_sha says the same, under the name run blocks use",
             record.get("instance_content_sha"), contract["instance_content_sha"])
    check_eq("identity: the mutated file is recorded with the bytes it held (here the test itself)",
             record.get("mutated_file"),
             {"path": TEST_FILE_REL, "sha256": PBC.sha256(original), "code_sha": PL.code_sha(original, "test_calc.py")})
    window_probe = record.get("window_probe") or {}
    check_eq("invert: window_probe repeats the verdict and hash", (window_probe.get("verdict"), window_probe.get("input_hash")),
             ("intended_failure", "author-tcs-1"))
    check_eq("invert: window_probe carries the level and the assertion mutation",
             (window_probe.get("proof_level"), window_probe.get("mutation_kind")), ("live", "assertion"))
    return record


def class_method(root: Path, stub: Path) -> None:
    proc, record = run(root, stub, f"{TEST_FILE_REL}::TestCalc::test_method", "test_method", "invert")
    check("class method: exit 0", proc.returncode == 0, proc.stdout + proc.stderr)
    check_eq("class method: intended_failure", record.get("verdict"), "intended_failure")
    # t-2064 P4b: the aggregate holds no statement text; it is read from the bytes the stub ran
    check_in("class method: the method's assert is inverted", "assert not (result in [6, 7])", mutated_line(root, record, 27))
    check_eq("class method: location is the method's assert", record.get("expected_location"), f"{TEST_FILE_REL}:27")
    # No run block ever executed this instance: the source and build identity a receipt binds are
    # the author's record, not the probe's to type - so no receipt, and the record names each fact
    # that was missing (the exit stays 0: a verdict was recorded). Its row binds no bytes, and that
    # is no longer a missing fact: the test file's own bytes are read (Amendment 2, one reader).
    check_eq("class method: no receipt without the facts it binds", record.get("receipt"), None)
    check_eq("class method: and every missing fact is named", record.get("receipt_missing"),
             ["source_revision", "build_id"])
    check_in("class method: the note says whose record it is", "the author's record",
             " ".join(record.get("notes") or []))
    check_in("class method: nothing was published", "nothing published", str(record.get("binding")))
    check_eq("class method: no receipt file for it",
             list((root / "qa-factory" / "artifacts" / TASK / "work" / "sensitivity-receipts")
                  .glob("test_method-live-*")), [])


def hamcrest_style(root: Path, stub: Path) -> None:
    proc, record = run(root, stub, f"{TEST_FILE_REL}::test_hamcrest", "test_hamcrest", "invert")
    check("hamcrest invert: exit 0", proc.returncode == 0, proc.stdout + proc.stderr)
    check_eq("hamcrest invert: intended_failure", record.get("verdict"), "intended_failure")
    # t-2064 P4b: the statement is read from the bytes the stub ran; what the run saw is read from the per-check record (the
    # aggregate's `observed` is `{}`)
    check_in("hamcrest invert: is_not around the matcher", 'is_not(equal_to(4))', mutated_line(root, record, 31))
    observed = read_check_record(root, "test_hamcrest").get("observed") or {}
    check("hamcrest invert: the last traceback line is inside hamcrest",
          str(observed.get("location", "")).startswith("hamcrest.py:"))
    check_eq("hamcrest invert: the test file frame decides the location", record.get("actual_location"),
             f"{TEST_FILE_REL}:31")


def dead_assert(root: Path, stub: Path) -> None:
    proc, record = run(root, stub, f"{TEST_FILE_REL}::test_dead_assert", "test_dead_assert")
    check("dead assert: exit 0 (a verdict was recorded)", proc.returncode == 0, proc.stdout + proc.stderr)
    check_eq("dead assert: no_failure", record.get("verdict"), "no_failure")
    check_eq("dead assert: no actual location", record.get("actual_location"), None)


def raises_first(root: Path, stub: Path) -> None:
    proc, record = run(root, stub, f"{TEST_FILE_REL}::test_raises_first", "test_raises_first")
    check("raises first: exit 1 (an `incomplete` verdict was recorded, as for any probe that is not proved)", proc.returncode == 1,
          proc.stdout + proc.stderr)
    # N3b: a throw before the check is not proved by its place: no token in its text, so the code critic judges it (a fact: where it fell)
    check_eq("raises first: incomplete, owed a judgment", (record.get("verdict"), record.get("cause")), ("incomplete", "judgment"))
    check_eq("raises first: nothing is proved", record.get("proved_by"), None)
    # t-2064 P4b: the facts of a walk's judgment live in the per-check record's `observed` (the aggregate has no `judgment_facts`); "outside
    # the mutated statement" is the observed place against the check's own key (it was `location_hit: False`)
    seen = read_check_record(root, "test_raises_first").get("observed") or {}
    check_eq("raises first: the facts hold the place of the raise", seen.get("location"), f"{TEST_FILE_REL}:16")
    check_eq("raises first: and that it is outside the mutated statement", seen.get("location") == (record.get("checks") or [{}])[0].get("key"), False)
    check_eq("raises first: failure_kind is not assertion", seen.get("failure_kind"), "exception")


def no_assert(root: Path, stub: Path) -> None:
    original = (root / TEST_FILE_REL).read_bytes()
    stamp = (root / TEST_FILE_REL).stat().st_mtime_ns
    proc, payload = run(root, stub, f"{TEST_FILE_REL}::test_no_assert", "test_no_assert")
    check("no assert: exit 2", proc.returncode == 2, proc.stdout + proc.stderr)
    check_eq("no assert: refused", payload.get("status"), "refused")
    # t-2064 P4b item 2: a walk with an empty plan is a refusal (EP-A: an empty list is never read as proved) that names the detector table and
    # the `--at` door; it takes no lock and is a tool refusal that DOES leave the `refused: tool` record (t-2143 N4: `main` writes it through
    # `_record_tool_refusal`; it was the `no assert` text on the old first-check road, which `--at` still is)
    check_in("no assert: the message says no check of a known form was found", "no check of a form the factory reads was found", payload.get("error", ""))
    check_in("no assert: and names the door (the detector table, and --at for a check in a helper)", "--at <file>:<line>", payload.get("error", ""))
    check_eq("no assert: the file was never touched", (root / TEST_FILE_REL).stat().st_mtime_ns, stamp)
    check_eq("no assert: bytes unchanged", (root / TEST_FILE_REL).read_bytes(), original)
    refusal_record = read_record(root, "test_no_assert")
    check_eq("no assert: a refusal of the tool, with the record (refused: tool, not_executed)",
             (refusal_record.get("refused"), refusal_record.get("verdict")), ("tool", "not_executed"))
    proc, payload = run(root, stub, f"{TEST_FILE_REL}::test_nowhere", "test_nowhere")
    check_eq("unknown instance: refused before any file", (proc.returncode, payload.get("status")), (2, "refused"))


def restore_on_failure(stub: Path) -> None:
    root = project()  # its own: the shared project's test_add already holds a receipt (answered, not run)
    try:
        _restore_on_failure(root, stub)
    finally:
        cleanup(root)
        cleanup_beside(root)


def _restore_on_failure(root: Path, stub: Path) -> None:
    original = (root / TEST_FILE_REL).read_bytes()
    proc, record = run(root, stub, f"{TEST_FILE_REL}::test_add", "test_add", PROBE_STUB_CRASH="1")
    check("runner crash: exit 1", proc.returncode == 1, proc.stdout + proc.stderr)
    check_eq("runner crash: not_executed", record.get("verdict"), "not_executed")
    check_in("runner crash: the note says the runner left no report evidence (was: printed no summary)", "no report evidence",
             " ".join(record.get("notes") or []))
    check_eq("runner crash: the bytes are back", (root / TEST_FILE_REL).read_bytes(), original)
    check_eq("runner crash: restore verified", (record.get("restore") or {}).get("verified"), True)
    proc = run_script("probe_by_code.py", "--task", TASK, "--dispatch", "S5-qa-code-critic-9",
                      "--test", f"{TEST_FILE_REL}::test_add", "--instance", "test_add", "--json",
                      cwd=root, env=env_for(root, stub))
    record = json.loads(proc.stdout) if proc.stdout.strip().startswith("{") else {}
    # RH1-8 B3: the open dispatch is asked BEFORE the first byte, so a bad id is a refusal (exit 2), not a
    # `not_executed` after a mutation; the bytes were never touched.
    check("bad dispatch: exit 2", proc.returncode == 2, proc.stdout + proc.stderr)
    check_eq("bad dispatch: refused", record.get("status"), "refused")
    check_in("bad dispatch: the refusal names the id", "S5-qa-code-critic-9", record.get("error", ""))
    check_eq("bad dispatch: the bytes are untouched", (root / TEST_FILE_REL).read_bytes(), original)


def a_run_that_executed_nothing_keeps_the_standing_record(stub: Path) -> None:
    """t-177: an `intended_failure` record is replaced only by the record of a run that executed the test.
    A `not_executed` attempt (a stand that was down, a refused request) used to overwrite it, and the
    evidence that a probe had passed - what probe_debt.py settles - was gone."""
    root = project()
    try:
        path = root / "qa-factory" / "artifacts" / TASK / "work" / "probes" / "test_add.json"
        standing = {"schema_version": 1, "verdict": "intended_failure", "instance_id": "test_add",
                    "test_file_sha256": "f" * 64, "recorded_at": "2026-09-30T05:02:39+00:00",
                    "publish": {"published": False}, "receipt": None}
        write_json(path, standing)
        original = (root / TEST_FILE_REL).read_bytes()
        proc, record = run(root, stub, f"{TEST_FILE_REL}::test_add", "test_add", PROBE_STUB_CRASH="1")
        kept = read_record(root, "test_add")
        check_eq("kept: the run itself reports not_executed", (proc.returncode, record.get("verdict")), (1, "not_executed"))
        check_eq("kept: the stored verdict is still intended_failure", kept.get("verdict"), "intended_failure")
        check_eq("kept: and its measured bytes", kept.get("test_file_sha256"), "f" * 64)
        check_eq("kept: every other stored key is as it was",
                 {k: v for k, v in kept.items() if k != "last_attempt"}, standing)
        attempt = kept.get("last_attempt") or {}
        check_eq("kept: last_attempt names the verdict", attempt.get("verdict"), "not_executed")
        check("kept: last_attempt carries the time and the cause",
              bool(attempt.get("at")) and "no row of the junit-xml report" in str(attempt.get("why")), str(attempt))   # the walk's check-row note
        check_eq("kept: the test bytes are back", (root / TEST_FILE_REL).read_bytes(), original)
        # a run that executed replaces it, whatever it found
        write_json(root / "qa-factory" / "artifacts" / TASK / "work" / "probes" / "test_dead_assert.json",
                   dict(standing, instance_id="test_dead_assert"))
        proc, record = run(root, stub, f"{TEST_FILE_REL}::test_dead_assert", "test_dead_assert")
        now = read_record(root, "test_dead_assert")
        check_eq("an executed run (no_failure) replaces the intended_failure record",
                 (record.get("verdict"), now.get("verdict"), "last_attempt" in now), ("no_failure", "no_failure", False))
        proc, record = run(root, stub, f"{TEST_FILE_REL}::test_add", "test_add")
        now = read_record(root, "test_add")
        check_eq("an executed run (intended_failure) replaces it too: new bytes, no last_attempt",
                 (now.get("verdict"), now.get("test_file_sha256") == PBC.sha256(original), "last_attempt" in now),
                 ("intended_failure", True, False))
    finally:
        cleanup(root)
        cleanup_beside(root)
    path = temp_dir("qa-keep-record-") / "r.json"
    try:
        attempt = {"verdict": "not_executed", "recorded_at": "t", "notes": ["a", "the stand is down"]}
        check_eq("no stored record: nothing is kept", PBC.keep_standing_record(path, attempt), False)
        write_json(path, {"verdict": "no_failure"})
        check_eq("a stored no_failure is replaced as before", PBC.keep_standing_record(path, attempt), False)
        path.write_text("{broken", encoding="utf-8")
        check_eq("a stored record that cannot be read is replaced as before", PBC.keep_standing_record(path, attempt), False)
        write_json(path, {"verdict": "intended_failure"})
        check_eq("an executed verdict is never kept away", PBC.keep_standing_record(path, dict(attempt, verdict="no_failure")),
                 False)
        check_eq("a stored intended_failure is kept against not_executed", PBC.keep_standing_record(path, attempt), True)
        check_eq("...with the LAST note as the cause", json.loads(path.read_text(encoding="utf-8"))["last_attempt"],
                 {"at": "t", "verdict": "not_executed", "why": "the stand is down"})
        # B-373 R10 / E23: `incomplete` (the tool could not read the run) judged nothing about the test either,
        # so it never replaces an intended_failure; its last_attempt names ITS verdict
        write_json(path, {"verdict": "intended_failure"})
        incomplete = dict(attempt, verdict="incomplete", notes=["a", "the library's wording differs"])
        check_eq("an incomplete answer never replaces an intended_failure record",
                 PBC.keep_standing_record(path, incomplete), True)
        check_eq("...and last_attempt says incomplete, with the cause",
                 json.loads(path.read_text(encoding="utf-8"))["last_attempt"],
                 {"at": "t", "verdict": "incomplete", "why": "the library's wording differs"})
        write_json(path, {"verdict": "no_failure"})
        check_eq("an incomplete answer over a stored no_failure is not 'kept' (nothing to protect)",
                 PBC.keep_standing_record(path, incomplete), False)
    finally:
        cleanup(path.parent)


def multiline_keeps_line_count() -> None:
    data = TEST_FILE.encode("utf-8")
    spec = PBC.parse_node(f"{TEST_FILE_REL}::test_multiline")
    mutated, detail = PBC.plan_mutation(data, spec, "invert", "test_multiline")
    check_eq("multiline invert: the file keeps its line count", mutated.count(b"\n"), data.count(b"\n"))
    check_eq("multiline invert: the assert's first line is the location", detail["line"], 35)
    try:
        PBC.plan_mutation(data, spec, "expected", "test_multiline")
        check("expected is no mutation any more (N7)", False)
    except PBC.Refusal as exc:
        check_in("expected is refused by the plan with the one that remains", "--mutation is one of invert", str(exc))
    try:
        PBC.plan_mutation(b"def test_g():\n    assert size() > 1\n", PBC.parse_node("t.py::test_h"), "invert", "i")
        check("an unknown function is refused", False)
    except PBC.Refusal as exc:
        check_in("an unknown function is refused by name", "test_h", str(exc))


SRC_HAMCREST_MULTILINE = (b"from hamcrest import assert_that, equal_to\n\n\ndef test_h():\n    x = 1\n    assert_that(\n"
                          b"        add(2, 2),\n        equal_to(\n            4\n        ),\n    )\n    assert True\n")


SRC_LITERAL_MULTILINE = (b"def test_l():\n    assert name(\n    ) == [\n        1,\n        2,\n    ], 'msg'\n"
                         b"    assert True\n")


SRC_ORACLE_HELPER = b"def helper():\n    assert got == want, 'm'\n\n\ndef test_o():\n    helper()\n"


# (label, source, node, mutation, extra arguments, the statement after, the marker, the literal pair,
#  sha256[:16] over the mutated bytes + the sorted-key JSON of the detail). The digest is the byte golden;
#  the readable columns say which part of it a failure is about (t-667 D7, E13: characterised BEFORE the move).
PLAN_GOLDEN = [
    ("add invert", TEST_FILE.encode(), "test_add", "invert", {},
     'assert not (add(2, 2) == 4), "probe-IID invert: add(2, 2) == 4"', "probe-IID invert: add(2, 2) == 4",
     (None, None), "9c9aa8bd02ea3963"),
    ("method invert", TEST_FILE.encode(), "TestCalc::test_method", "invert", {},
     'assert not (result in [6, 7]), "probe-IID invert: result in [6, 7]"', "probe-IID invert: result in [6, 7]",
     (None, None), "cec6844c3379146e"),
    ("multiline invert", TEST_FILE.encode(), "test_multiline", "invert", {},
     'assert not (add(\n        2, 2\n    ) == 4\n\n), "probe-IID invert: add( 2, 2 ) == 4"',
     "probe-IID invert: add( 2, 2 ) == 4", (None, None), "67219c94a9f69b61"),
    ("hamcrest invert", TEST_FILE.encode(), "test_hamcrest", "invert", {},
     'assert_that(add(2, 2), __import__("hamcrest").is_not(equal_to(4)), "probe-IID invert: equal_to(4)")',
     "probe-IID invert: equal_to(4)", (None, None), "172ee75ac819028a"),
    ("hamcrest multiline invert", SRC_HAMCREST_MULTILINE, "test_h", "invert", {},
     'assert_that(add(2, 2), __import__("hamcrest").is_not(equal_to(\n            4\n        ))\n\n\n, '
     '"probe-IID invert: equal_to( 4 )")', "probe-IID invert: equal_to( 4 )", (None, None), "15b7817f941490fd"),
    ("literal over several lines, invert", SRC_LITERAL_MULTILINE, "test_l", "invert", {},
     'assert not (name(\n    ) == [\n        1,\n        2,\n    ]), "probe-IID invert: name( ) == [ 1, 2, ]"',
     "probe-IID invert: name( ) == [ 1, 2, ]", (None, None), "f30684423a999bb9"),
    ("a BOM stays: invert", b"\xef\xbb\xbf" + TEST_FILE.encode(), "test_add", "invert", {},
     'assert not (add(2, 2) == 4), "probe-IID invert: add(2, 2) == 4"', "probe-IID invert: add(2, 2) == 4",
     (None, None), "cba702e7c2fc510a"),
    ("an oracle function", SRC_ORACLE_HELPER, "test_o", "invert", {"oracle_function": "helper",
                                                                    "oracle_note": "via helper"},
     'assert not (got == want), "probe-IID invert: got == want"', "probe-IID invert: got == want", (None, None),
     "dc6a95fdb21b33f1"),
]


# (label, source, node, mutation, extra arguments, what the refusal says)
PLAN_REFUSALS = [
    ("expected is no mutation any more", TEST_FILE.encode(), "test_add", "expected", {}, "--mutation is one of invert"),
    ("a source that does not parse", b"def test_s(:\n", "test_s", "invert", {}, "tests/test_calc.py does not parse"),
    ("no assert", TEST_FILE.encode(), "test_no_assert", "invert", {}, "the function body has no assert"),
    ("an unknown mutation", TEST_FILE.encode(), "test_add", "other", {}, "--mutation is one of invert"),
]


def plan_mutation_is_pinned() -> None:
    """t-667 D7, characterisation: `plan_mutation` over assert and assert_that statements, one line and
    several, both mutations, a BOM, an oracle function, and every refusal it raises itself: the mutated
    bytes and the detail are a byte golden, and the file keeps its line count and its BOM."""
    for label, data, node, mutation, extra, after, marker, pair, digest in PLAN_GOLDEN:
        mutated, detail = PBC.plan_mutation(data, PBC.parse_node(f"{TEST_FILE_REL}::{node}"), mutation, "IID", **extra)
        check_eq(f"D7 {label}: the statement after", detail["statement_after"], after)
        check_eq(f"D7 {label}: the marker", detail["marker"], marker)
        check_eq(f"D7 {label}: no token, no factory marker (t-2045 N2)", (detail["message_marker"], detail["message_form"]), ("", ""))
        check_eq(f"D7 {label}: the literal pair", (detail.get("literal_before"), detail.get("literal_after")), pair)
        check_eq(f"D7 {label}: line count and BOM are the source's",
                 (mutated.count(b"\n"), mutated.startswith(b"\xef\xbb\xbf")),
                 (data.count(b"\n"), data.startswith(b"\xef\xbb\xbf")))
        check_eq(f"D7 {label}: the byte golden (mutated bytes + detail)",
                 hashlib.sha256(mutated + json.dumps(detail, sort_keys=True).encode()).hexdigest()[:16], digest)
        if extra:
            check_eq(f"D7 {label}: the oracle is named in the detail",
                     (detail.get("oracle_function"), detail.get("oracle_note")),
                     (extra["oracle_function"], extra["oracle_note"]))
        else:
            check_eq(f"D7 {label}: no oracle keys in the detail", "oracle_function" in detail, False)
    for label, data, node, mutation, extra, words in PLAN_REFUSALS:
        try:
            PBC.plan_mutation(data, PBC.parse_node(f"{TEST_FILE_REL}::{node}"), mutation, "IID", **extra)
            check(f"D7 refusal {label}: refused", False)
        except PBC.Refusal as exc:
            check_in(f"D7 refusal {label}: the words", words, str(exc))


def window_validates(root: Path, record: dict) -> None:
    """The record's `window_probe` dropped into a schema-2 window instance passes
    `acceptance.validate_window` with no gap at all."""
    task_root = root / "qa-factory" / "artifacts" / TASK
    probe = record["window_probe"]
    item = {"schema_version": 2, "instance_id": "test_add", "input_hash": record["input_hash"],
            "outcome": "passed", "execution_fingerprint": "fp-1",
            "review": {"verdict": "approved", "input_hash": record["input_hash"]},
            "obligation_ids": record["obligation_ids"], "obligation_refs": OBLIGATION_REFS,
            "obligation_hash": record["obligation_hash"], "assertion_id": record["assertion_id"],
            "defect_location": record["defect_location"],
            "change_disposition": "new_or_changed", "change_basis_ref": "manifest:TC-100",
            "probe": probe, "evidence_refs": record["evidence_refs"]}
    window = {"schema_version": 2, "input_hash": "window-1", "required_quality_checks": [],
              "quality_receipts": [], "instances": [item]}
    gaps = acceptance.validate_window(window, task_root)
    check_eq("validate_window: no gap on a window built from the record", gaps, [])
    broken = json.loads(json.dumps(window))
    broken["instances"][0]["probe"]["verdict"] = "no_failure"
    check_in("validate_window: a no_failure probe is a sensitivity gap", "sensitivity:test_add",
             acceptance.validate_window(broken, task_root))


def oracle_in_a_helper(root: Path, stub: Path) -> None:
    """The expectation lives in a module several tests share, and the test body asserts nothing.

    This is the shape that made `probe_by_code` refuse nine times on TP1-13797 and send one
    tooling defect back to the author in four windows. The probe now follows the oracle one hop
    out, mutates it there, says where it went, and puts the helper back.
    """
    helper = root / "tests" / "expectations.py"
    original, stamp = helper.read_bytes(), helper.stat().st_mtime_ns
    test_original = (root / TEST_FILE_REL).read_bytes()
    proc, record = run(root, stub, f"{TEST_FILE_REL}::test_via_helper", "test_via_helper")
    check("helper oracle: exit 0", proc.returncode == 0, proc.stdout + proc.stderr)
    check_eq("helper oracle: the mutated expectation fires", record.get("verdict"),
             "intended_failure")
    check_eq("helper oracle: the expected location is in the helper, not the test",
             record.get("expected_location"), "tests/expectations.py:2")
    # t-2064 P4b: the walk's record names the check it mutated by its key, `<helper file>:<line>`, not by `oracle_function` / `oracle_note`
    # (the aggregate's `mutation_detail` is `{file, line, end_line, checks}`); the old pins on those two keys are replaced by the key, and
    # the lost shared-file warning is a question in the report
    check_eq("helper oracle: the record names the check it mutated, in the helper", [c.get("key") for c in record.get("checks") or []],
             ["tests/expectations.py:2"])
    check_eq("helper oracle: the helper is restored byte for byte", helper.read_bytes(), original)
    check_eq("helper oracle: and its mtime is put back", helper.stat().st_mtime_ns, stamp)
    check_eq("helper oracle: the test file was never touched",
             (root / TEST_FILE_REL).read_bytes(), test_original)
    check_eq("helper oracle: the restore is verified",
             (record.get("restore") or {}).get("verified"), True)
    check_eq("helper oracle: the probe's identity is still the test file's sha",
             record.get("test_file_sha256"), PBC.sha256(test_original))


# --- the reader of the run's report ----------------------------------------------------------------

def junit_file(directory: Path, name: str, body: str) -> Path:
    path = directory / name
    path.write_text('<?xml version="1.0" encoding="utf-8"?>\n' + body, encoding="utf-8")
    return path


def report_rows_as_before() -> None:
    """`report_rows` gives the row the private JUnit reader gave, whichever way the shared reader
    shapes its own: the failure outranks the error, the failure's own message and stack decide,
    a skip beside a failure is still a failure, a skip alone stays a skip."""
    if not hasattr(PBC, "report_rows"):
        check("report rows: the probe reads its report through one function that wraps the shared reader", False)
        return
    directory = temp_dir("qa-probe-rows-")
    try:
        both = junit_file(directory, "both.xml",
                          '<testsuites><testsuite name="s">'
                          '<testcase classname="a.b" name="t_both"><error message="E1">tb-error</error>'
                          '<failure message=" F1 ">tb-failure</failure></testcase>'
                          '<testcase classname="a.b" name="t_error"><error message="E2">tb-error-2</error></testcase>'
                          '<testcase classname="a.b" name="t_skip_fail"><skipped message="why"/>'
                          '<failure message="F3">tb-3</failure></testcase>'
                          '<testcase classname="a.b" name="t_skip"><skipped message="not now"/></testcase>'
                          '<testcase classname="" name="t_bare"/>'
                          '<testcase classname="a.b" name="t_two_failures"><failure message="first">one</failure>'
                          '<failure message="second">two</failure></testcase>'
                          '</testsuite></testsuites>')
        rows = {r["test_id"]: r for r in PBC.report_rows(both, "junit-xml")}
        want = {
            "a.b::t_both": ("failed", "F1", "tb-failure"),
            "a.b::t_error": ("error", "E2", "tb-error-2"),
            "a.b::t_skip_fail": ("failed", "F3", "tb-3"),
            "a.b::t_skip": ("skipped", "", ""),
            "t_bare": ("passed", "", ""),
            "a.b::t_two_failures": ("failed", "first", "one"),
        }
        check_eq("report rows: the same tests, once each", sorted(rows), sorted(want))
        for test_id, expected in want.items():
            row = rows.get(test_id) or {}
            check_eq(f"report rows {test_id}: status, message, text as the private reader read them",
                     (row.get("status"), row.get("message"), row.get("text")), expected)
        same = PBC.report_rows(both, "pytest")
        check_eq("report rows: `pytest` is read the same as `junit-xml`", same, PBC.report_rows(both, "junit-xml"))
        try:
            PBC.report_rows(both, "cucumber")
            check("report rows: an unknown reporter is refused", False)
        except ValueError as exc:
            check_in("report rows: the refusal names the reporter and what is known", "cucumber", str(exc))
            check_in("report rows: and the readers there are", "junit-xml", str(exc))
        try:
            PBC.report_rows(junit_file(directory, "broken.xml", "<testsuite><testcase"), "junit-xml")
            check("report rows: broken XML propagates", False)
        except ET.ParseError:
            check("report rows: broken XML still raises the parse error the probe notes", True)
    finally:
        cleanup(directory)


def reporter_in_the_summary(stub: Path) -> None:
    """The run's summary says which reporter wrote the report, and the probe reads it with that
    reader. A summary that names none is read as JUnit, as before; one the reader does not know is
    `not_executed` with the reason, not a crash and not a guess.

    Every probe here runs in a project of its own: a second probe of test_add over the same bytes is
    ANSWERED (`already_probed`, D-0018), not run, so one shared project would test the repeat answer
    and never the reader. The receipt of a run that names no reporter is the base the others are
    compared with."""
    def probed(name: str):
        root = project()
        try:
            original = (root / TEST_FILE_REL).read_bytes()
            proc, record = run(root, stub, f"{TEST_FILE_REL}::test_add", "test_add", PROBE_STUB_REPORTER=name)
            written = normalised(root, proc.returncode, read_record(root, "test_add"))
            return proc, record, written, (root / TEST_FILE_REL).read_bytes() == original
        finally:
            cleanup(root)
            cleanup_beside(root)

    _proc, _record, base, _back = probed("")
    for name, label in (("junit-xml", "junit-xml"), ("pytest", "pytest"), ("", "no reporter")):
        proc, _record, written, _back = probed(name)
        check(f"summary names {label}: exit 0", proc.returncode == 0, proc.stdout + proc.stderr)
        check_eq(f"summary names {label}: the receipt is the one written with no reporter named", written, base)
    for name in ("cucumber", "none"):
        proc, record, _written, back = probed(name)
        notes = " ".join(record.get("notes") or [])
        check(f"reporter {name!r}: exit 1, a verdict was recorded", proc.returncode == 1, proc.stdout + proc.stderr)
        check_eq(f"reporter {name!r}: not_executed", record.get("verdict"), "not_executed")
        check_in(f"reporter {name!r}: the note carries the reason and the reporter", f"unknown reporter '{name}'", notes)
        check_in(f"reporter {name!r}: and says what the reader knows", "expected one of", notes)
        check_not_traceback(f"reporter {name!r}", proc)
        check_eq(f"reporter {name!r}: the bytes are back", back, True)
        check_eq(f"reporter {name!r}: restore verified", (record.get("restore") or {}).get("verified"), True)


def check_not_traceback(label: str, proc) -> None:
    check(f"{label}: no traceback", "Traceback" not in (proc.stderr or "") and "Traceback" not in (proc.stdout or ""),
          proc.stderr[-300:])


def refusal_text(path: str, suffix: str, directory: bool = False) -> str:
    """B-373 c (K3): the refusal of a file whose suffix has no `assertion_probes` entry, verbatim up to the
    entry shape: what is wrong (a gap of the factory's DATA), what it expected (one entry, its shape), and the
    door that exists today with its arguments inline (no pointer to a brief the role does not have open)."""
    what = (f"{path} is a directory, not a test file" if directory
            else f"no assertion probe for {suffix or 'a file with no suffix'} ({path})")
    return (f"probe_by_code: {what} - factory data gap: references/detectors.json `assertion_probes` has entries for "
            "(csharp: .cs; java: .java; typescript: .ts .tsx .js .jsx .mjs .cjs .mts .cts) and none for this suffix, "
            "so this probe reads no test of it (it never guesses a grammar). The row to add is one entry in that "
            f"file, the factory's data and not the author's test: {AD.ENTRY_SHAPE}. Return it as a tooling finding. "
            "Until the row exists the probe that breaks the product in a throwaway copy works for any language: "
            "red_sandbox.py --probe --repo <project root> --request <mutations.json> --task-root <task root>. "
            "Nothing was changed.")


def non_python_test_refused(root: Path, stub: Path) -> None:
    (root / "tests" / "Calc.kt").write_text("class CalcTests { fun adds() {} }\n", encoding="utf-8")
    (root / "tests" / "CalcTests.cs").write_text("public class CalcTests { }\n", encoding="utf-8")
    (root / "tests" / "calc.spec.ts").write_text("it('adds', () => {});\n", encoding="utf-8")
    (root / "tests" / "runner").write_text("#!/bin/sh\n", encoding="utf-8")
    # K3: a suffix with no entry is a refusal that names the data gap, the entry shape and the door
    cases = (("tests/Calc.kt::CalcTests.adds", "tests/Calc.kt", ".kt", False),
             ("tests\\Calc.kt::CalcTests.adds", "tests/Calc.kt", ".kt", False),
             ("tests/runner::test_x", "tests/runner", "", False),
             ("tests::test_x", "tests", "", True))
    for spec, shown, suffix, directory in cases:
        before = tree_state(root)
        proc, payload = run(root, stub, spec, "test_add")
        label = f"no entry {spec!r}"
        check_eq(f"{label}: exit 2", proc.returncode, 2)
        check_eq(f"{label}: refused", payload.get("status"), "refused")
        check_eq(f"{label}: the text says what is wrong, what it expected and the door",
                 payload.get("error"), refusal_text(shown, suffix, directory))
        check_in(f"{label}: the door is the product-breaking probe, with its arguments inline",
                 "red_sandbox.py --probe --repo <project root> --request <mutations.json> --task-root <task root>",
                 payload.get("error", ""))
        check_in(f"{label}: and the reason is worded as the data gap it is", "factory data gap", payload.get("error", ""))
        check_not_in(f"{label}: no pointer to a brief", "brief", payload.get("error", ""))
        check_not_in(f"{label}: no doubled space where a suffix was", "read  source", payload.get("error", ""))
        check_eq(f"{label}: no file changed, none written (no request, no receipt)", tree_state(root), before)
    # A language that HAS an entry reaches the detector path and is refused for its own reason (no such test in
    # this file) - never for "not Python"; the tree is unchanged all the same.
    def kept(tree: dict) -> dict:  # the lock a probe takes before it reads the test is never deleted (B-373 a)
        # (and the window's model file the wrapper writes: world, not the probe's work; `run` rewrites the same bytes at a new mtime)
        return {k: v for k, v in tree.items() if not k.endswith(".lock") and "/work/probe-models/" not in k}

    # t-2064 P4b: the default road lists the checks first; a test whose body holds none the factory reads (no such declaration, no
    # recognised assertion) is the EMPTY-PLAN refusal, for either reason, and the same words
    for spec, why in (("tests/CalcTests.cs::CalcTests.Adds", "no check of a form the factory reads was found"),
                      ("tests/calc.spec.ts::adds", "no check of a form the factory reads was found")):
        model_entries(root, stub, spec, "test_add")     # world, written before the snapshot: the call itself must change nothing
        before = kept(tree_state(root))
        proc, payload = run(root, stub, spec, "test_add")
        check_eq(f"entry {spec!r}: exit 2, refused", (proc.returncode, payload.get("status")), (2, "refused"))
        check_in(f"entry {spec!r}: the refusal is about the test's own shape ({why})", why, payload.get("error", ""))
        check_not_in(f"entry {spec!r}: it is not the old `not a Python test`", "not a Python test", payload.get("error", ""))
        check_eq(f"entry {spec!r}: no file changed", kept(tree_state(root)), before)
    # t-2045 N1: `--at` is read for every language. On a Python node a line that holds no check (the `def` line, 5) is refused
    # like any other language's: the text names the nearest check below (line 6) and the doors, and nothing is changed.
    before = kept(tree_state(root))
    proc = run_script("probe_by_code.py", "--task", TASK, "--dispatch", DISPATCH, "--test",
                      f"{TEST_FILE_REL}::test_add", "--instance", "test_add", "--at", "5", "--json",
                      cwd=root, env=env_for(root, stub))
    payload = json.loads(proc.stdout) if proc.stdout.strip().startswith("{") else {}
    check_eq("--at on a Python node: exit 2, refused", (proc.returncode, payload.get("status")), (2, "refused"))
    check_in("--at on a line with no check: the text says so", "holds no check of a form the factory reads", payload.get("error", ""))
    check_in("...and names the nearest check below as the door", "`--at 6`", payload.get("error", ""))
    check_not_in("...and is no longer the old `not Python`", "not Python", payload.get("error", ""))
    check_eq("--at on a Python node: nothing changed", kept(tree_state(root)), before)
    # A path that IS Python but is not shaped like a node keeps its own refusal.
    proc, payload = run(root, stub, "tests/test_calc.py", "test_add")
    check_eq("no `::` at all: still refused with the shape wanted", (proc.returncode, payload.get("status")), (2, "refused"))
    check_in("no `::` at all: and the shape is named", "<file>::<function>", payload.get("error", ""))


# --- the run directory -------------------------------------------------------------------------------

LAUNCHER = '''
"""Runs probe_by_code.main() with every call of the request builder written to a log."""
import json
import os
import sys

sys.path.insert(0, os.environ["PROBE_SCRIPTS_DIR"])
import execution_request as ER

real = ER.build_mine_request


def recording(*args, **kwargs):
    entry = {"cwd": kwargs.get("cwd") or "", "sandbox_root": kwargs.get("sandbox_root") or "",
             "purpose": kwargs.get("purpose") or ""}
    try:
        return real(*args, **kwargs)
    except Exception as exc:
        entry["refused"] = type(exc).__name__ + ": " + str(exc)
        raise
    finally:
        with open(os.environ["PROBE_CALL_LOG"], "a", encoding="utf-8") as log:
            log.write(json.dumps(entry) + "\\n")


ER.build_mine_request = recording
import probe_by_code

sys.argv = ["probe_by_code.py"] + sys.argv[1:]
probe_by_code.main()
'''


def run_recorded(root: Path, stub: Path, test: str, instance: str) -> tuple:
    """(process, the calls the probe made to the request builder, in order)."""
    model_entries(root, stub, test, instance)
    launcher = stub.parent / "launcher.py"
    launcher.write_text(LAUNCHER, encoding="utf-8")
    log = stub.parent / "calls.jsonl"
    log.unlink(missing_ok=True)
    env = env_for(root, stub, PROBE_CALL_LOG=str(log), PROBE_SCRIPTS_DIR=str(SCRIPTS),
                  PYTHONDONTWRITEBYTECODE="1")
    proc = subprocess.run([PY, "-B", str(launcher), "--task", TASK, "--dispatch", DISPATCH, "--test", test,
                           "--instance", instance, "--json"],
                          capture_output=True, text=True, encoding="utf-8", errors="replace",
                          cwd=str(root), env=env, timeout=300)
    calls = [json.loads(ln) for ln in log.read_text(encoding="utf-8").splitlines() if ln.strip()] \
        if log.is_file() else []
    return proc, calls


def run_directory_is_given(root: Path, stub: Path, label: str, wanted: Path) -> None:
    proc, calls = run_recorded(root, stub, f"{TEST_FILE_REL}::test_add", "test_add")
    record = json.loads(proc.stdout) if proc.stdout.strip().startswith("{") else {}
    check(f"{label}: exit 0", proc.returncode == 0, proc.stdout + proc.stderr)
    check_eq(f"{label}: the request builder is called once", len(calls), 1)
    check(f"{label}: no call is made without the run directory", all(c.get("cwd") for c in calls), json.dumps(calls))
    check_eq(f"{label}: the first call carries the profile's run directory",
             (calls[0].get("cwd") if calls else None), str(wanted.resolve()))
    check(f"{label}: and no call goes through a refusal",
          not any(c.get("refused") for c in calls), json.dumps(calls))
    check(f"{label}: it is --cwd, never --sandbox-root (the probe has no clone)",
          all(not c.get("sandbox_root") for c in calls))
    check_eq(f"{label}: the probe still ran, in that directory", record.get("verdict"), "intended_failure")
    request_path = root / "qa-factory" / "artifacts" / TASK / "work" / "probe-requests" / "probe-walk-test_add-1.json"
    request = json.loads(request_path.read_text(encoding="utf-8")) if request_path.is_file() else {}
    check_eq(f"{label}: the request's command runs in the same directory",
             str(Path((request.get("command") or {}).get("cwd") or "").resolve()), str(wanted.resolve()))


def run_directory(stub: Path) -> None:
    """Two projects of their own: a second probe of test_add over the same bytes is ANSWERED
    (`already_probed`), and an answer launches nothing to record."""
    root = project()
    try:
        run_directory_is_given(root, stub, "run directory '.'", root)
    finally:
        cleanup(root)
        cleanup_beside(root)
    # A profile that runs in a subdirectory: the directory the retry used to work out after the
    # refusal is the one handed over on the first call.
    root = project()
    try:
        app = root / "app"
        app.mkdir()
        for name in ("tests", "calc.py", "hamcrest.py"):
            (root / name).rename(app / name)
        config_path = root / "qa-factory" / "config.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        config["profiles"][0]["commands"]["one_test"]["cwd"] = "app"
        write_json(config_path, config)
        run_directory_is_given(root, stub, "run directory 'app'", app)
    finally:
        cleanup(root)
        cleanup_beside(root)


def mutations_flow() -> None:
    stub_dir = temp_dir("qa-probe-stub-")
    stub = stub_dir / "fake_run_suite.py"
    stub.write_text(FAKE_RUN_SUITE, encoding="utf-8")
    root = project()
    try:
        record = invert_plain_assert(root, stub)
        class_method(root, stub)
        hamcrest_style(root, stub)
        dead_assert(root, stub)
        raises_first(root, stub)
        no_assert(root, stub)
        oracle_in_a_helper(root, stub)
        restore_on_failure(stub)
        a_run_that_executed_nothing_keeps_the_standing_record(stub)
        multiline_keeps_line_count()
        plan_mutation_is_pinned()
        if record:
            window_validates(root, record)
        # After the window check: the stub records no job, so a repeated probe of the same
        # instance and mutation rewrites the evidence file the first record's sha names.
        report_rows_as_before()
        reporter_in_the_summary(stub)
        non_python_test_refused(root, stub)
        run_directory(stub)
    finally:
        cleanup(root)
        cleanup_beside(root)
        cleanup(stub_dir)


def main() -> None:
    mutations_flow()
    finish("test_probe_by_code_mutations")


# split: runner piece 1
if __name__ == "__main__":
    main()
