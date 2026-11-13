"""probe_by_code.py: the live probe of a test in ANY language - the CLI half (B-373 part c, D-0028; split from
test_probe_by_code_languages.py, TD-11c N9).

The probe launched as a role launches it (a temp project per language, the stand-in runner `PROBE_RUN_SUITE`): the verdict, the
receipt, the window, the bytes (K1a, K2, K6, E13-E15, E20, E21), every runner mode (R8), the refusals before the first write
(R6, E3-E12), the data gaps (K3, K4), the kill and the recovery. A section name as an argument runs that one:
`languages`, `modes`, `standing`, `bom`, `at`, `refusals`, `traps`, `oracle`, `gaps`, `kill`.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import copy  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
from harness import (SCRIPTS, check, check_eq, check_in, check_not_in, cleanup, finish, run_script, temp_dir)  # noqa: E402
import assertion_detectors as AD  # noqa: E402
import contract as C  # noqa: E402
import probe_by_code as PBC  # noqa: E402
import proof_level as PL  # noqa: E402
from test_probe_by_code import (DISPATCH, TASK, cleanup_beside, env_for, model_entries, mutated_line, read_check_record, write_json)  # noqa: E402
from probe_by_code_languages_common import (FIX, LANGS, LANG_RUN_SUITE, OLD_NS, check_lines, check_markers, copies_left, first_line, lang_project, lrun, node_of, refusal_record_of, refused, said, stub_cfg, task_of, tree_state, tree_state_with_entries, window_gaps, write_entries)  # noqa: E402


def one_language(stub: Path, lang: str) -> None:
    spec = LANGS[lang]
    old = OLD_NS
    root = lang_project(lang, mtime_ns=old)
    try:
        target = root / spec["file"]
        original = target.read_bytes()
        # the one call per language that runs as a child process: its exit code and its stdout are the contract (K1a, the rest of the case
        # reads what it left on disk); every other call of this file takes the in-process door
        proc, record = lrun(root, stub, node_of(lang), spec["iid"], stub_cfg(lang), real=True)
        label = f"{lang}"
        lines, markers = check_lines(lang), check_markers(lang)
        keys = [f"{spec['file']}:{n}" for n in lines]
        rows = record.get("checks") or []
        # F5: the expectation is the FIXTURE's (`marker` in LANGS), never read back from the record: a marker lost on a form that must
        # carry one is a red here, not a quiet turn onto the judgment branch. t-2064 P4b (old -> new): `mutation_detail.message_marker` of the one
        # mutation -> `proved_by == "marker"` of each CHECK row of the walk (the aggregate has one row per check, the fixture says per check)
        check_eq(f"{lang} F5: each check row carries a marker exactly where the fixture's form takes one",
                 [r.get("proved_by") == "marker" for r in rows], markers)
        if not all(markers):
            # t-2064 N3b: a form that takes no message (xunit `Assert.Equal`) carries no token, so no runner text proves the probe:
            # the code critic judges it (INV: only our own text proves without a role). The rest of the case goes on after that judgment.
            check_eq(f"{label} N3b: no token in the form, so the failure at the statement is judgment, not proved",
                     (proc.returncode, record.get("verdict"), [r.get("verdict") for r in rows], [r.get("cause") for r in rows],
                      [r.get("proved_by") for r in rows]),
                     (1, "incomplete", ["intended_failure" if m else "incomplete" for m in markers],
                      [None if m else "judgment" for m in markers], ["marker" if m else None for m in markers]))
            judged = run_script("probe_by_code.py", "--task", TASK, "--dispatch", DISPATCH, "--judge", spec["iid"], "--verdict", "fires",
                                "--quote", spec["message"].splitlines()[0], "--json", cwd=root, env=env_for(root, stub, PROBE_SCRIPTS_DIR=str(SCRIPTS)))
            try:
                answer = json.loads(judged.stdout)
            except ValueError:
                answer = {}
            check_eq(f"{label} N3b: the critic's `fires` proves it", (answer.get("verdict"), answer.get("proved_by")),
                     ("intended_failure", "critic"))
            # t-2064 fix Q7 (repin): the judgment re-folds the aggregate ON DISK (the product did that already: verdict, receipt, publish); this
            # case kept reading `record` and `proc` of the walk BEFORE the judgment, so every pin below read the owed state. From here the call
            # is the judging call (`proc`) and the record is the one the judgment left (the same file `--judge` answered from)
            proc = judged
            record = json.loads((task_of(root) / "work" / "probes" / f"{spec['iid']}.json").read_text(encoding="utf-8"))
        check(f"{label}: exit 0", proc.returncode == 0, proc.stdout + proc.stderr)
        check_eq(f"{label} K1a: intended_failure", record.get("verdict"), "intended_failure")
        line = lines[0]
        check_eq(f"{label}: expected_location is the project-relative path and the statement's line",
                 record.get("expected_location"), f"{spec['file']}:{line}")
        check_eq(f"{label}: actual_location equals it", record.get("actual_location"), record.get("expected_location"))
        # t-2064 P4b (old -> new): the reason was the marker (`fires as /`) of the one mutation; the aggregate's reason counts the plan
        check_eq(f"{label}: the reason says every check of the plan proved", record.get("expected_reason"),
                 f"{len(lines)} of {len(lines)} checks of the plan proved")
        check_eq(f"{label}: actual_reason equals it", record.get("actual_reason"), record.get("expected_reason"))
        check_eq(f"{label}: failure_kind assertion, mutation_kind assertion, level live",
                 (record.get("failure_kind"), record.get("mutation_kind"), record.get("proof_level")), ("assertion", "assertion", "live"))
        detail = record.get("mutation_detail") or {}
        # old: style, language, line, end_line of the detector's mutation -> the aggregate's `mutation_detail` is {file, line, end_line, checks}
        # (the first check's place and the keys of the plan); style and language are not carried (they were the detector's, not a fact of the run)
        check_eq(f"{label}: the detail names the file, the first check's line and the plan's keys",
                 (detail.get("file"), detail.get("line"), detail.get("end_line"), detail.get("checks")), (spec["file"], line, line, keys))
        # old: `statement_inverted` of the record == the fixture's inverted text; new: the bytes the runner saw (stub_seen_text of its first
        # run's evidence) hold that text at the first check's line (N1: a marked statement is not `after` byte for byte, so the fixture's `hit`)
        check_in(f"{label}: the statement after the inversion is what the runner saw on the first check's line",
                 spec.get("hit", spec["after"]), mutated_line(root, record, line))
        # old: at is None and the one declaration is the one candidate -> the plan is exactly the body's checks, each run once, none left
        check_eq(f"{label}: the plan is the body's checks, each run once, none left", (len(rows), record.get("plan_runs"), record.get("plan_remaining")),
                 (len(lines), len(lines), []))
        # old: the detail carried head, pair, pair_id, fires_as, marker, form, matcher_at -> each check has its own record naming its key, its kind
        # (`invert`) and the entry it ran
        own = [read_check_record(root, spec["iid"], i) for i in range(len(lines))]
        check_eq(f"{label}: every check has its own record: its key, `invert`, its entry's hash, its target",
                 [(r.get("check_key"), r.get("probe_kind"), bool(r.get("entry_sha")), (r.get("target") or {}).get("line")) for r in own],
                 [(k, "invert", True, n) for k, n in zip(keys, lines)])
        check_eq(f"{label}: the file is byte-identical afterwards", target.read_bytes(), original)
        # old: `restore.restored_from == "copy"` (the aggregate has no such key) -> the restore's sha is the author's, and one restore per run
        check_eq(f"{label}: the restore is verified, to the author's bytes, once per run, and no copy is left",
                 ((record.get("restore") or {}).get("verified"), (record.get("restore") or {}).get("sha256"), (record.get("restore") or {}).get("runs"),
                  copies_left(root)), (True, PBC.sha256(original), len(lines), []))
        # E20: a file that is not Python gets mtime "now" - the author's next build rebuilds it
        check(f"{label} E20: the restored file's mtime is NOW, not the old one", target.stat().st_mtime_ns > old + 10 ** 15)
        evidence = (task_of(root) / record["evidence_ref"]) if record.get("evidence_ref") else None
        summary = json.loads(evidence.read_text(encoding="utf-8")) if evidence and evidence.suffix == ".json" else {}
        check(f"{label}: the runner saw the MUTATED bytes", summary.get("stub_hit") is True and summary.get("stub_seen_sha256") != PBC.sha256(original))
        # old: the one request `record["request"]` (None on the walk) -> one request per run, `work/probe-requests/probe-walk-<iid>-<n>.json`
        requests = [json.loads((task_of(root) / "work" / "probe-requests" / f"probe-walk-{spec['iid']}-{n}.json").read_text(encoding="utf-8"))
                    for n in range(1, len(lines) + 1)]
        check_eq(f"{label} R7: every request is for the whole case, never a node id", [(r.get("purpose"), r.get("selected_instance_ids")) for r in requests],
                 [("red_probe", [spec["iid"]])] * len(lines))
        check_eq(f"{label} R7: with the manifest's own selector arguments", [r["command"]["selector_args"] for r in requests],
                 [{spec["iid"]: spec["selector_args"]}] * len(lines))
        check_eq(f"{label}: the requests are built by this tool", [(r.get("built_by") or {}).get("tool") for r in requests],
                 ["probe_by_code.py"] * len(lines))
        # the receipt, the publish and the window
        receipt = record.get("receipt") or {}
        check(f"{label} K1a: the live receipt is written and on disk", bool(receipt.get("path")) and (task_of(root) / receipt["path"]).is_file(), str(record.get("receipt_missing")))
        check_eq(f"{label} K1a: and published", (record.get("publish") or {}).get("published"), True)
        manifest = json.loads((task_of(root) / "work" / "automation-manifest.json").read_text(encoding="utf-8"))
        row = next(t for t in manifest["tests"] if t["instance_id"] == spec["iid"])
        check_eq(f"{label} K1a: the contract takes the receipt unchanged", C.sensitivity_proof_issues(row, task_of(root)), [])
        on_disk = task_of(root) / str(receipt.get("path") or "no-receipt")
        check_eq(f"{label} K1a: the receipt's bytes are the raw sha of the file the probe measured",
                 json.loads(on_disk.read_text(encoding="utf-8")).get("test_content_hash") if on_disk.is_file() else None, PBC.sha256(original))
        check_eq(f"{label} K1a: the window built from the record has no gap", window_gaps(root, record, spec["iid"]), [])
        broken = dict(record["window_probe"], verdict="incomplete")
        item_gaps = window_gaps(root, dict(record, window_probe=broken), spec["iid"])
        check(f"{label}: an `incomplete` probe in a window is a gap (the critic's 'could not verify')",
              any(g.startswith("sensitivity:") for g in item_gaps), str(item_gaps))
        # M1's reading (L5): the window binds by the raw file sha: same_test is `raw`, and the row has a trace binding
        identity = PL.instance_identity(row, task_of(root), root)
        # typescript is read by `test_source` since EP1-37 (B-3): its identity is MEASURED once a typed run selected the test, so
        # its `why` is "" there; C# and Java stay unmeasured
        check(f"{label} M1: the identity of a non-pytest instance is unmeasured, so the raw rule applies (why is one of the two)",
              identity.get("why") in (PL.WHY_NO_REQUEST, PL.WHY_UNMEASURED)
              or (lang == "typescript" and identity.get("why") == "" and bool(identity.get("instance_identity"))),
              f"{identity.get('why')!r} {sorted(identity.get('instance_identity') or {})}")
        check_eq(f"{label} M1: input_hash is the raw sha256 of the file", identity.get("input_hash"), PBC.sha256(original))
        check_eq(f"{label} M1: same_test says `raw` for the probe's record and the window's item",
                 PL.same_test(PL.proof_identity({"input_hash": PBC.sha256(original)}), PL.proof_identity({"input_hash": PBC.sha256(original)})), "raw")
        check_eq(f"{label} M1 (E24): the row has a trace_binding.test_content_sha", bool((row.get("trace_binding") or {}).get("test_content_sha")), True)
        check_eq(f"{label}: the record on disk is the one returned",
                 json.loads((task_of(root) / "work" / "probes" / f"{spec['iid']}.json").read_text(encoding="utf-8")).get("verdict"),
                 "intended_failure")
        # K2/E13: the same test, a pass through the launcher
        proc, got = lrun(root, stub, node_of(lang), spec["iid"], stub_cfg(lang, "pass_anyway"))
        # PRODUCT QUESTION 1 (t-2064-p4b2t2-report.md): a repeat answers the aggregate, not `already_probed`
        check_eq(f"{label}: a second probe of the same bytes is answered, not run (PRODUCT QUESTION 1)", got.get("verdict"), "already_probed")
        # t-2064 TR2-14 (B3): the second call is answered `already_probed` (the repeat on the same bytes and the same model launches nothing), and the
        # proved verdict stands on disk: the pass of the stub did not unprove it
        check_eq(f"{label}: the second call keeps the proved verdict (answered `already_probed`), a pass does not unprove it",
                 (got.get("verdict"), json.loads((task_of(root) / "work" / "probes" / f"{spec['iid']}.json").read_text(encoding="utf-8")).get("verdict")),
                 ("already_probed", "intended_failure"))
    finally:
        cleanup(root)
        cleanup_beside(root)

    # K2 / E13 / E14: the dead check, through the launcher that builds by default
    root = lang_project(lang)
    try:
        original = (root / spec["file"]).read_bytes()
        proc, record = lrun(root, stub, node_of(lang), spec["iid"], stub_cfg(lang, "pass_anyway"))
        check_eq(f"{label} K2: a passed row after a verified mutation is no_failure, exit 0", (proc.returncode, record.get("verdict")), (0, "no_failure"))
        check_eq(f"{label}: the bytes are back, no receipt, nothing published", ((root / spec["file"]).read_bytes() == original,
                                                                                record.get("receipt"), record.get("publish")), (True, None, None))
        # t-2064 P4b (old -> new): the notes of the one record -> the note of each CHECK row (the aggregate's `notes` hold the command notes only),
        # and the residual of `observed` -> `observed` of each check's own record
        check_rows = [r.get("note", "") for r in record.get("checks") or []]
        if LANGS[lang]["argv"][0] in ("dotnet", "mvn"):
            check_eq(f"{label}: every check's note names the launcher that builds by default",
                     ["the launcher builds by default" in n for n in check_rows], [True] * len(check_markers(lang)))
        else:
            check_in(f"{label}: not compiled - the residual risk is said in `observed`", "compiled output",
                     (read_check_record(root, spec["iid"]).get("observed") or {}).get("residual", ""))
    finally:
        cleanup(root)
        cleanup_beside(root)
    # F9: the same pass through a wrapper launcher: incomplete for a compiled language, still no_failure for TS
    root = lang_project(lang, argv=["bash", "run-tests.sh", "{report_path}"])
    try:
        proc, record = lrun(root, stub, node_of(lang), spec["iid"], stub_cfg(lang, "pass_anyway"))
        wanted = "no_failure" if lang == "typescript" else "incomplete"
        check_eq(f"{label} F9: a pass through a wrapper launcher gives {wanted}", (record.get("verdict"), proc.returncode),
                 (wanted, 0 if wanted == "no_failure" else 1))
        if wanted == "incomplete":
            check_in(f"{label} F9: and says the launcher may not rebuild", "may never have reached the build",
                     " ".join(r.get("note", "") for r in record.get("checks") or []))   # t-2064 P4b: the note is on the check rows
    finally:
        cleanup(root)
        cleanup_beside(root)


def one_check_data(lang: str) -> bytes:
    """The language's fixture with the body's EXTRA checks cut off (t-2064 P4b: the walk runs every check of a body, and the fixture's C# `Adds`
    has two). A section that pins the reading of ONE failing row takes this data: a plan of one check, so the call's verdict is that row's."""
    spec = LANGS[lang]
    data = (FIX / spec["fixture"]).read_bytes()
    first = first_line(lang, data)
    cut = {first + offset for offset, _text, _marker in spec.get("also", [])}
    return b"".join(ln for n, ln in enumerate(data.splitlines(keepends=True), 1) if n not in cut)


def r8_through_the_cli(stub: Path) -> None:
    """Every mode of the runner at the CLI level, for the language whose frames are the least forgiving."""
    for lang in ("csharp", "java", "typescript"):
        spec = LANGS[lang]
        for mode, verdict, exit_code, needle in (
                ("lib_frames_first", "intended_failure", 0, ""),
                ("wrong_line", "incomplete", 1, "the code critic judges it"),     # N3b: a failure elsewhere with no token is judgment
                ("error_row", "incomplete", 1, "the run's row is an error"),
                ("no_frames", "incomplete", 1, "the code critic judges it"),     # N4: a row with text and no readable place is the critic's
                ("drifted_message", "incomplete", 1, "the factory cannot read its text; the code critic judges it"),
                ("no_row", "not_executed", 1, "no row of the"),
                ("two_rows", "not_executed", 1, "ambiguous"),
                ("skipped_row", "not_executed", 1, "report status")):
            if lang != "csharp" and mode in ("no_row", "two_rows", "skipped_row"):
                continue
            # N3b: only a row holding the token is proved by the code. Java's form takes a marker (the stub prints it), so a row of any
            # shape and place is proved there; the csharp xunit and the typescript `toBe` forms take none, so the same run is judgment
            if lang == "java":
                if mode == "no_frames":
                    verdict, exit_code, needle = "intended_failure", 0, ""     # the marker outranks the place (step 1 before step 3)
            elif mode == "lib_frames_first":
                verdict, exit_code = "incomplete", 1
            if mode == "drifted_message":
                needle = "the code critic judges it"
            # t-2064 P4b: the walk runs EVERY check of a body; the section pins the reading of ONE failing row, so it takes the body with one
            # check (`one_check_data`: the fixture's second C# assertion cut) and the call's verdict is that row's
            root = lang_project(lang, data=one_check_data(lang))
            try:
                original = (root / spec["file"]).read_bytes()
                proc, record = lrun(root, stub, node_of(lang), spec["iid"], stub_cfg(lang, mode))
                # PRODUCT QUESTION 8 (t-2064-p4b2t3-report.md): a report with NO row of the test: the walk's row note says "report status None",
                # the old "no row of the ... report" is gone, and the verdict stays not_executed. PRODUCT QUESTION 9: a report with TWO rows of the
                # test is read as ONE failed row (`incomplete`, judgment) where the old road said `not_executed`, "ambiguous". Both pins stay RED
                question = {"no_row": " (PRODUCT QUESTION 8)", "two_rows": " (PRODUCT QUESTION 9)"}.get(mode, "")
                label = f"{lang} {mode}"
                red = question if lang == "csharp" else ""    # the question's pins are the verdict and the note, on the csharp rows only
                check_eq(f"{label}: {verdict}, exit {exit_code}{red if mode == 'two_rows' else ''}", (record.get("verdict"), proc.returncode),
                         (verdict, exit_code))
                check_eq(f"{label}: the bytes are back and no copy is left", ((root / spec["file"]).read_bytes() == original, copies_left(root)),
                         (True, []))
                if needle:
                    check_in(f"{label}: the note says why{red if mode in ('no_row', 'two_rows') else ''}", needle, said(record))   # old: the record's notes; new: the notes and the check row's note
                if verdict != "intended_failure":
                    check_eq(f"{label}: no receipt, nothing published", (record.get("receipt"), record.get("publish")), (None, None))
                if verdict == "incomplete":
                    check_eq(f"{label}: a verdict on the test is never claimed (no mismatches list)",
                             record.get("mismatches"), None)
                if mode == "wrong_line":
                    # t-2064 P4b (old -> new): `judgment_facts.location` / `.location_hit` of the one record -> `observed.location` of the check's own
                    # record, and "the place is not the check's" = that location differs from the check's key (no `location_hit` field is carried)
                    seen = read_check_record(root, spec["iid"]).get("observed") or {}
                    check_eq(f"{label}: the place is a fact for the critic, not a verdict", (record.get("cause"), record.get("actual_location"),
                             seen.get("location"), seen.get("location") == f"{spec['file']}:{first_line(lang)}"),
                             ("judgment", None, f"{spec['file']}:{first_line(lang) + 3}", False))
                if mode == "error_row":
                    check_eq(f"{label}: the error row is never wrong_location", record.get("actual_location"), None)
            finally:
                cleanup(root)
                cleanup_beside(root)


def a_standing_record_survives_incomplete(stub: Path) -> None:
    """E23 / K6: a stored intended_failure is kept when a later probe of other bytes is `incomplete`."""
    lang = "csharp"
    spec = LANGS[lang]
    root = lang_project(lang)
    try:
        path = task_of(root) / "work" / "probes" / f"{spec['iid']}.json"
        standing = {"schema_version": 1, "verdict": "intended_failure", "instance_id": spec["iid"], "test_file_sha256": "f" * 64,
                    "recorded_at": "2026-09-30T05:02:39+00:00", "publish": {"published": False}, "receipt": None}
        write_json(path, standing)
        proc, record = lrun(root, stub, node_of(lang), spec["iid"], stub_cfg(lang, "drifted_message"))
        kept = json.loads(path.read_text(encoding="utf-8"))
        check_eq("E23: the run is incomplete", (record.get("verdict"), proc.returncode), ("incomplete", 1))
        check_eq("E23: the stored verdict is still intended_failure", kept.get("verdict"), "intended_failure")
        check_eq("E23: every other stored key is as it was", {k: v for k, v in kept.items() if k != "last_attempt"}, standing)
        # PRODUCT QUESTION 10 (t-2064-p4b2t3-report.md): the standing record's `last_attempt.why` is the aggregate's FIRST NOTE (the command note
        # "command, fingerprint file list and runtime probe are those of this story's last typed run"), not the check row's reason: the cause
        # ("the code critic judges it") is lost from it. The pin stays RED
        check_eq("E23: last_attempt names incomplete and the cause (PRODUCT QUESTION 10)", ((kept.get("last_attempt") or {}).get("verdict"),
                                                                       "the code critic judges it" in str((kept.get("last_attempt") or {}).get("why"))),
                 ("incomplete", True))
        proc, record = lrun(root, stub, node_of(lang), spec["iid"], stub_cfg(lang, "pass_anyway"))
        check_eq("E23: an executed no_failure replaces it as before", (record.get("verdict"),
                 json.loads(path.read_text(encoding="utf-8")).get("verdict")), ("no_failure", "no_failure"))
    finally:
        cleanup(root)
        cleanup_beside(root)


def bom_and_crlf_through_the_run(stub: Path) -> None:
    """E21: a BOM and CRLF line ends - built at runtime (B-409) - reach the run's runner unchanged but for the
    statement, and come back byte for byte."""
    lang = "csharp"
    spec = LANGS[lang]
    # t-2064 P4b: the body with ONE check (`one_check_data`): the walk runs every check, and this case pins the line the one failing run reached
    base = one_check_data(lang)
    for label, data in (("a BOM and CRLF", b"\xef\xbb\xbf" + base.replace(b"\n", b"\r\n")),
                        ("CRLF alone", base.replace(b"\n", b"\r\n")),
                        ("a BOM alone", b"\xef\xbb\xbf" + base)):
        root = lang_project(lang, data=data)
        try:
            line = first_line(lang, data)
            proc, record = lrun(root, stub, node_of(lang), spec["iid"], stub_cfg(lang, line=line))
            # N3b: the csharp xunit form takes no marker, so the run is judgment, not proved; what is pinned is the line and the bytes
            # t-2064 P4b (old -> new): `expected_location` of the one failing record (the aggregate of an unproved check carries none) -> the check
            # row's key and the place its own record says the run failed at: the run reached the right line
            row_key = ((record.get("checks") or [{}])[0]).get("key")
            reached = (read_check_record(root, spec["iid"]).get("observed") or {}).get("location")
            check_eq(f"E21 ({label}): the run reached the right line (judgment: no token in this form)", (record.get("verdict"), row_key, reached),
                     ("incomplete", f"{spec['file']}:{line}", f"{spec['file']}:{line}"))
            check_eq(f"E21 ({label}): the bytes are identical afterwards", (root / spec["file"]).read_bytes(), data)
            evidence = task_of(root) / record["evidence_ref"]
            summary = json.loads(evidence.read_text(encoding="utf-8")) if evidence.suffix == ".json" else {}
            check_eq(f"E21 ({label}): the runner saw the BOM kept", summary.get("stub_seen_prefix") == "efbbbf", data.startswith(b"\xef\xbb\xbf"))
            check_eq(f"E21 ({label}): and every CRLF kept", summary.get("stub_seen_crlf"), data.count(b"\r\n"))
        finally:
            cleanup(root)
            cleanup_beside(root)
    root = lang_project(lang, data=b"namespace A { class T { void Adds() { Assert.Equal(1, \xff); } } }\n")
    try:
        before = tree_state(root)
        proc, payload = lrun(root, stub, node_of(lang), spec["iid"], stub_cfg(lang))
        refused("E21: a file that is not UTF-8", proc, payload, "is not UTF-8")
        check_eq("E21: and the tree is unchanged", tree_state(root), before)
    finally:
        cleanup(root)
        cleanup_beside(root)


TWO = (b"namespace Acme.Tests\n{\n    public class CalcTests\n    {\n        public void Adds()\n        {\n"
       b"            Assert.Equal(4, Calc.Add(2, 2));\n        }\n    }\n\n    public class MoreTests\n    {\n"
       b"        public void Adds()\n        {\n            Assert.Equal(6, Calc.Add(3, 3));\n        }\n    }\n}\n")


def at_among_two_declarations(stub: Path) -> None:
    """E3 / E5 / A5: a name declared twice is refused without --at; with --at, an `intended_failure` is
    attributable (the run failed at that very line), but a pass among two candidates is `incomplete`."""
    lang = "csharp"
    spec = LANGS[lang]
    root = lang_project(lang, data=TWO)
    try:
        before = tree_state(root)
        proc, payload = lrun(root, stub, node_of(lang), spec["iid"], stub_cfg(lang, line=7, after="Assert.NotEqual(4, Calc.Add(2, 2));"))
        # t-2064 P4b: a name declared twice has no located body, so the plan is EMPTY and the plain call is the empty-plan refusal, whose door is
        # `--at <file>:<line>`; it no longer counts the declarations nor names their lines (the old "declared 2 times ... line 5, line 13")
        refused("E3 (two declarations, no --at)", proc, payload, "no check of a form the factory reads was found", "--at <file>:<line>",
                "Nothing was changed")
        check_eq("E3: the tree is unchanged", tree_state(root), before)
        proc, record = lrun(root, stub, node_of(lang), spec["iid"], stub_cfg(lang, line=15, after="Assert.NotEqual(6, Calc.Add(3, 3));"), "--at", "15")
        # t-2064 P4b: `--at 15` is a plan of the ONE row `<file>:15` (its entry written by `lrun`); the aggregate names that row: its verdict is
        # judgment (no token in the xunit form, N3b) and the call's verdict is `incomplete`. The aggregate keeps the selected key, not `--at`
        # and the candidates [5, 13] (a replay reads the key; the old `mutation_detail.at/candidates` are not in the aggregate).
        rows = record.get("checks") or [{}]
        check_eq("--at 15 picks the second body: judgment (no token in the xunit form, N3b) at line 15",
                 (record.get("verdict"), rows[0].get("key"), rows[0].get("verdict"), rows[0].get("cause")),
                 ("incomplete", f"{spec['file']}:15", "incomplete", "judgment"))
        detail = record.get("mutation_detail") or {}
        check_eq("the record keeps the selected check (what a replay needs)", (detail.get("checks"), len(rows)), ([f"{spec['file']}:15"], 1))
    finally:
        cleanup(root)
        cleanup_beside(root)
    root = lang_project(lang, data=TWO)
    try:
        proc, record = lrun(root, stub, node_of(lang), spec["iid"], stub_cfg(lang, "pass_anyway", line=15, after="x"), "--at", "15")
        # t-2064 P4b: the first two A5 pins below are the old record's and stay RED, unbent - PRODUCT QUESTION 4 of t-2064-p4b2t2-report.md: on the
        # walk road a pass of the run when `--at` names one of TWO declarations of the name answers `no_failure` (exit 0, a survivor of the
        # selected row) with no note that the pass cannot say which body ran; the old road said `incomplete` (exit 1) and why
        check_eq("A5: a pass among two candidates is incomplete, never no_failure (PRODUCT QUESTION 4)", (record.get("verdict"), proc.returncode), ("incomplete", 1))
        check_in("A5: the note says a pass does not tell which body ran (PRODUCT QUESTION 4)", "does not say which body ran", said(record))   # TR2-14 (B2): the E5 note is on the check row
        # the one-declaration control: the same pass IS a no_failure
        proc, record = lrun(root, stub, node_of(lang), spec["iid"], stub_cfg(lang, "pass_anyway", line=7, after="x"), "--at", "7")
        check_eq("A5: --at among two candidates again (first body): still incomplete", record.get("verdict"), "incomplete")
    finally:
        cleanup(root)
        cleanup_beside(root)
    root = lang_project("csharp")
    try:
        proc, record = lrun(root, stub, node_of("csharp"), "Adds", stub_cfg("csharp", "pass_anyway"), "--at", str(first_line("csharp")))
        check_eq("A5 control: --at on a name declared ONCE does not make a pass incomplete", record.get("verdict"), "no_failure")
    finally:
        cleanup(root)
        cleanup_beside(root)


def refusals_before_the_write(stub: Path) -> None:
    """K5: every refusal of R6, E10, E12, E14, E22: exit 2, and the tree byte-identical (files and mtimes)."""
    lang = "csharp"
    spec = LANGS[lang]

    def extra(n: int, **fields) -> list:
        return [{"case": f"TC-{200 + i}", "covers": [f"TC-{200 + i}"], "file": spec["file"], "test": f"T{i}", "instance_id": f"T{i}",
                 "selector": f"CalcTests.T{i}", **fields} for i in range(n)]

    # R6 (a): the whole case runs - every row of THIS case must carry its selector and report id. Rows of the
    # same case: the case id is shared with the instance under probe.
    for count in (4, 5, 6, 8):
        rows = [dict(r, case="TC-100", covers=["TC-100"]) for r in extra(count, selector_args=["x"], report_test_id="")]
        root = lang_project(lang, extra_entries=rows)
        try:
            before = tree_state_with_entries(root, stub, node_of(lang), spec["iid"])
            proc, payload = lrun(root, stub, node_of(lang), spec["iid"], stub_cfg(lang))
            text = refused(f"R6 a ({count} offending rows)", proc, payload, "no selector of their own", "manifest_put.py --task",
                           "--fragment", "selector_args", "report_test_id")
            # t-2064 P4b, PRODUCT QUESTION 5 of t-2064-p4b2t2-report.md: the R6 (a) refusal is not what the walk road answers (exit 1, no
            # refusal text) - every R6 (a) pin stays red and unbent; the split below is guarded so the rest of the section still runs
            listed = (text.split("no selector of their own:")[1].split(". A non-pytest")[0]
                      if "no selector of their own:" in text else "")
            check_in(f"R6 a ({count} rows): the count of offenders is told", f"{count} instance(s)", text)
            check_eq(f"R6 a ({count} rows with no report_test_id): at most 5 are listed",
                     len(re.findall(r"T\d+ \(no `", listed)), min(count, 5))
            check_eq(f"R6 a ({count} rows): 'and N more' only beyond the cap of 5, with the right N",
                     re.search(r"and (\d+) more", listed).group(1) if "more" in listed else "", "" if count <= 5 else str(count - 5))
            check_eq(f"R6 a ({count} rows): the tree is unchanged", tree_state(root), before)
            check_eq(f"R6 a ({count} rows): and the refusal of the tool left its `refused: tool` record", refusal_record_of(root, spec["iid"]),
                     ("tool", "not_executed"))
        finally:
            cleanup(root)
            cleanup_beside(root)
    rows = [{"case": "TC-100", "covers": ["TC-100"], "file": "tests/Bare.cs"}]
    root = lang_project(lang, extra_entries=rows)
    try:
        before = tree_state_with_entries(root, stub, node_of(lang), spec["iid"])
        proc, payload = lrun(root, stub, node_of(lang), spec["iid"], stub_cfg(lang))
        refused("R6 a (a bare file of the case)", proc, payload, "tests/Bare.cs (names no test)")
        check_eq("R6 a (a bare file): the tree is unchanged", tree_state(root), before)
        check_eq("R6 a (a bare file): and the refusal of the tool left its `refused: tool` record", refusal_record_of(root, spec["iid"]),
                 ("tool", "not_executed"))
    finally:
        cleanup(root)
        cleanup_beside(root)
    root = lang_project(lang, verified=False)
    try:
        before = tree_state_with_entries(root, stub, node_of(lang), spec["iid"])
        proc, payload = lrun(root, stub, node_of(lang), spec["iid"], stub_cfg(lang))
        refused("R6 a (selectors.verified is false)", proc, payload, "selector contract is verified", "selectors.verified")
        check_eq("R6 a (not verified): the tree is unchanged", tree_state(root), before)
        check_eq("R6 a (not verified): and the refusal of the tool left its `refused: tool` record", refusal_record_of(root, spec["iid"]),
                 ("tool", "not_executed"))
    finally:
        cleanup(root)
        cleanup_beside(root)
    # R6 (b): --test names another file than the manifest row
    two_tests = (FIX / spec["fixture"]).read_bytes().replace(
        b"        [Fact]\n        public void Throws()", b"        [Fact]\n        public void Other()\n        {\n            Assert.Equal(1, 1);\n        }\n\n"
        b"        [Fact]\n        public void Throws()")
    root = lang_project(lang, data=two_tests, files={"tests/Other.cs": two_tests})
    try:
        before = tree_state_with_entries(root, stub, "tests/Other.cs::CalcTests.Adds", spec["iid"])
        proc, payload = lrun(root, stub, "tests/Other.cs::CalcTests.Adds", spec["iid"], stub_cfg(lang))
        refused("R6 b (another file than the manifest row's)", proc, payload, "the manifest row of 'Adds' names tests/CalcTests.cs")
        check_eq("R6 b: the tree is unchanged", tree_state(root), before)
        # R6 (c): the report id does not end with the tail (its own model file is written first: the entries are those of THIS node)
        before = tree_state_with_entries(root, stub, "tests/CalcTests.cs::CalcTests.Other", spec["iid"])
        proc, payload = lrun(root, stub, "tests/CalcTests.cs::CalcTests.Other", spec["iid"], stub_cfg(lang))
        text = refused("R6 c (the tail is another test than the report id)", proc, payload, "does not end with 'CalcTests.Other'",
                       "manifest_put.py --fragment")
        check_not_in("R6 c: no DisplayName words for a C# test", "display name", text)
        check_eq("R6 c: the tree is unchanged", tree_state(root), before)
    finally:
        cleanup(root)
        cleanup_beside(root)
    # R6 (c), Java: a @DisplayName before the declaration adds the words about the runner's id for the method
    java = (FIX / "CalcTest.java").read_bytes().replace(b"    @Test\n    void adds()", b'    @Test\n    @DisplayName("adds two numbers")\n    void adds()')
    root = lang_project("java", data=java, entry_extra={"report_test_id": "com.acme.CalcTest::adds two numbers"})
    try:
        before = tree_state_with_entries(root, stub, node_of("java"), "adds")
        proc, payload = lrun(root, stub, node_of("java"), "adds", stub_cfg("java"))
        refused("R6 c (surefire reports a @DisplayName)", proc, payload, "does not end with 'CalcTest.adds'",
                "and the report may name this test by it", "must be the runner's id for the method")
        check_eq("R6 c (DisplayName): the tree is unchanged", tree_state(root), before)
        # control: the same id with no DisplayName on the declaration does not carry the DisplayName words
        proc, payload = lrun(root, stub, "src/test/java/com/acme/CalcTest.java::CalcTest.assertjAdds", "adds", stub_cfg("java"))
        text = refused("R6 c (no DisplayName on the declaration)", proc, payload, "does not end with")
        check_not_in("R6 c control: no display name words", "display name", text)
    finally:
        cleanup(root)
        cleanup_beside(root)
    # R6 (d): a compiled entry whose one-test command forbids the rebuild
    for token in ("--no-build",):
        root = lang_project(lang, argv=["dotnet", "test", token, "--logger", "trx;LogFileName={report_path}"])
        try:
            before = tree_state_with_entries(root, stub, node_of(lang), spec["iid"])
            proc, payload = lrun(root, stub, node_of(lang), spec["iid"], stub_cfg(lang))
            refused(f"R6 d ({token} in the profile's command)", proc, payload, token, "stops the csharp build")
            check_eq(f"R6 d ({token}): the tree is unchanged", tree_state(root), before)
        finally:
            cleanup(root)
            cleanup_beside(root)
    root = lang_project("java", argv=["mvn", "surefire:test", "-Dsurefire.reportsFile={report_path}"])
    try:
        proc, payload = lrun(root, stub, node_of("java"), "adds", stub_cfg("java"))
        refused("R6 d (surefire:test)", proc, payload, "surefire:test", "stops the java build")
    finally:
        cleanup(root)
        cleanup_beside(root)
    root = lang_project("typescript", argv=["npx", "jest", "--no-build", "--outputFile={report_path}"])
    try:
        proc, payload = lrun(root, stub, node_of("typescript"), "adds", stub_cfg("typescript"))
        check_eq("R6 d: TypeScript is not compiled - a `--no-build` token is not a refusal there", proc.returncode == 2, False)
    finally:
        cleanup(root)
        cleanup_beside(root)
    # E22: --mutation expected on a test that is not Python
    root = lang_project(lang)
    try:
        before = tree_state(root)
        proc = run_script("probe_by_code.py", "--task", TASK, "--dispatch", DISPATCH, "--test", node_of(lang), "--instance",
                          spec["iid"], "--mutation", "expected", "--json", cwd=root, env=env_for(root, stub, LANG_STUB=json.dumps(stub_cfg(lang))))
        payload = json.loads(proc.stdout) if proc.stdout.strip().startswith("{") else {}
        refused("E22 (--mutation expected)", proc, payload, "--mutation expected was removed", "an `invert` entry for the check in the model file")
        check_eq("E22: the tree is unchanged", tree_state(root), before)
    finally:
        cleanup(root)
        cleanup_beside(root)
    # E6 / E7 through the CLI: no assertion, an invert-null first assertion
    root = lang_project(lang, data=b"namespace A\n{\n  class CalcTests\n  {\n    public void Adds()\n    {\n      Helpers.Expect(4);\n    }\n  }\n}\n")
    try:
        before = tree_state(root)
        proc, payload = lrun(root, stub, node_of(lang), spec["iid"], stub_cfg(lang))
        # t-2064 P4b: a body with no check is an EMPTY plan - the refusal of the plain call, whose door is `--at <file>:<line>` (it no longer
        # names `--oracle`, nor "no recognised assertion")
        refused("E6 (no recognised assertion)", proc, payload, "no check of a form the factory reads was found", "--at <file>:<line>")
        check_eq("E6: the tree is unchanged", tree_state(root), before)
    finally:
        cleanup(root)
        cleanup_beside(root)
    root = lang_project(lang)
    try:
        write_entries(root, [f"{spec['file']}:14"])     # the entry of the selected key, written before the snapshot: the refusal that follows writes nothing
        before = tree_state(root)
        proc, payload = lrun(root, stub, "tests/CalcTests.cs::CalcTests.Adds", spec["iid"], stub_cfg(lang, "pass_anyway"),
                             "--at", "14")
        refused("E5/E7 (--at on a line that starts no assertion)", proc, payload, "line 14 of tests/CalcTests.cs holds no check of a form the factory reads")
        check_eq("E7: the tree is unchanged", tree_state(root), before)
    finally:
        cleanup(root)
        cleanup_beside(root)


def traps_through_the_cli(stub: Path) -> None:
    """The critic's t-551 findings F1 and F2 as a role meets them: each input is refused before any write (exit 2,
    the author's file byte-identical, no copy made), never planned onto a string or onto an inactive branch, and
    never run - a false `no_failure` against the author is the dangerous direction."""
    ts_trap = ("describe('c', () => {\n  test('adds', () => {\n    const t = <b>don't</b>;\n"
               "    const label = 'expect(a).toBe(1)'; // don't\n    expect(sum(1, 2)).toBe(3);\n  });\n});\n").encode()
    ts_unclosed = ("describe('c', () => {\n  test('adds', () => {\n    const r = /abc\n    expect(sum(1, 2)).toBe(3);\n"
                   "  });\n});\n").encode()
    cs_if = (b"namespace Acme.Tests\n{\n  public class CalcTests\n  {\n    public void Adds()\n    {\n#if NET6\n"
             b"      Assert.Equal(4, Calc.Add(2, 2));\n#else\n      Assert.Equal(5, Calc.Add(2, 2));\n#endif\n    }\n  }\n}\n")
    ts_two = ("describe('calc', () => {\n  test('adds', () => {\n    expect(sum(1, 2)).toBe(3);\n  });\n"
              "  test('does not adds', () => {\n    expect(sum(1, 2)).toBe(3);\n  });\n});\n").encode()
    for lang, label, data, extra, needles in (
            ("typescript", "F1 (i): an apostrophe in JSX text", ts_trap, None,
             ("single-line string that crosses a line break", "opens at line 3")),
            ("typescript", "F1b (vi): an unterminated regex literal", ts_unclosed, None,
             ("regex literal that opens at line 3 and does not close on its line",)),
            # PRODUCT QUESTION 11 (t-2064-p4b2t3-report.md): `_refuse_conditional_compilation` is called by `_located` (probe_by_code.py:5066), whose
            # ToolRefusal the walk catches PER CHECK: the plan lists both branches (lines 8 and 10), both rows are `incomplete`, cause `tooling`, exit 1,
            # and the walk has written (copy, requests, record) - where plan_detector_mutation (:1962) refused before any write. PRODUCT QUESTION 12:
            # `run_shape_checks` (:2770, the longer-title refusal) is not on the walk road: the test is walked and its row is `not_executed`. Both red
            ("csharp", "F1 (ii): #if/#else/#endif (PRODUCT QUESTION 11)", cs_if, None, ("conditional-compilation directive `#if NET6` at line 7",)),
            ("typescript", "F2: the id of another test with a longer title (PRODUCT QUESTION 12)", ts_two,
             {"report_test_id": "calc does not adds::calc does not adds"},
             ("also ends with the longer title 'does not adds'", "declared at line 5"))):
        spec = LANGS[lang]
        root = lang_project(lang, data=data, entry_extra=extra)
        try:
            before = tree_state_with_entries(root, stub, node_of(lang), spec["iid"])   # TR2-14: after the window's model file `lrun` writes
            proc, payload = lrun(root, stub, node_of(lang), spec["iid"], stub_cfg(lang))
            refused(label, proc, payload, *needles)
            check_eq(f"{label}: the author's file is byte-identical and the tree unchanged",
                     ((root / spec["file"]).read_bytes() == data, tree_state(root) == before), (True, True))
            # the lexer cannot read the file: the TOOL's refusal leaves its one record (`refused: tool`), no other
            # (t-2167 F4: the conditional-compilation refusal is a ToolRefusal too, so it leaves its record)
            lexer = label.startswith(("F1 (i)", "F1b (vi)", "F1 (ii)"))   # the lexer's refusals (a record of the tool); F2 is the id's, and leaves none
            check_eq(f"{label}: no copy was made, no runner launched, and a record only for a refusal of the tool",
                     (copies_left(root), (task_of(root) / "work" / "probes").is_dir(), (task_of(root) / "evidence").is_dir()),
                     ([], lexer, False))
            if label.startswith(("F1 (i)", "F1b (vi)", "F1 (ii)")):
                # TR2-14: `tree_state` leaves the `refused: tool` record out of "unchanged"; this is the positive pin that the record exists
                # and says so (one record, the refusal's own: the instance, `refused: tool`, `not_executed`)
                found = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((task_of(root) / "work" / "probes").glob("*.json"))]
                check_eq(f"{label}: the refusal left the one `refused: tool` record",
                         [(r.get("instance_id"), r.get("refused"), r.get("verdict")) for r in found], [(spec["iid"], "tool", "not_executed")])
        finally:
            cleanup(root)
            cleanup_beside(root)
    # control: the same TS file with the right report id plans and runs (the refusal is the id's, not the file's)
    root = lang_project("typescript", data=ts_two)
    try:
        proc, record = lrun(root, stub, node_of("typescript"), "adds", stub_cfg("typescript", "pass_anyway", line=3,
                                                                                 after="expect(sum(1, 2)).not.toBe(3);"))
        check_eq("F2 control: the test's own report id is not refused", record.get("verdict"), "no_failure")
    finally:
        cleanup(root)
        cleanup_beside(root)


def oracle_in_a_helper(stub: Path) -> None:
    """The expectation lives in a helper: `--oracle <file>::<name>` names it (E6's door); the helper file must be
    in the test tree and in no protected product path (E10); it is mutated, restored and recorded as the mutated file."""
    lang = "csharp"
    spec = LANGS[lang]
    test_src = (b"namespace Acme.Tests\n{\n    public class CalcTests\n    {\n        public void Adds()\n        {\n"
                b"            Helpers.ExpectSum(2, 2, 4);\n        }\n    }\n}\n")
    helper = (b"namespace Acme.Tests\n{\n    public static class Helpers\n    {\n        public static void ExpectSum(int a, int b, int s)\n"
              b"        {\n            Assert.Equal(s, a + b);\n        }\n    }\n}\n")
    root = lang_project(lang, data=test_src, files={"tests/Helpers.cs": helper, "src/Product.cs": helper})
    try:
        before = tree_state(root)
        node = node_of(lang)
        cfg = stub_cfg(lang, file="tests/Helpers.cs", line=7, after="Assert.NotEqual(s, a + b);", stack=[
            "   at Acme.Tests.Helpers.ExpectSum(Int32 a, Int32 b, Int32 s) in {path}:line {line}"])
        proc, payload = lrun(root, stub, node, spec["iid"], cfg)
        refused("an oracle with no --oracle: the test body asserts nothing", proc, payload, "no check of a form the factory reads was found",
                "--at <file>:<line>")
        # t-2064 P4b: `--oracle <file>::<name>` selects the checks of that function (its row `tests/Helpers.cs:7`), which needs ITS entry
        # (written here: `lrun` writes none for `--oracle`); the record is the aggregate, its row names the helper's line, `mutation_detail`
        # names the file; `oracle_function` and `oracle_note` ("named by hand") are not in it any more (PRODUCT QUESTION 3 of the report)
        write_entries(root, ["tests/Helpers.cs:7"])
        proc, record = lrun(root, stub, node, spec["iid"], cfg, "--oracle", "tests/Helpers.cs::ExpectSum")
        rows = record.get("checks") or [{}]
        check_eq("--oracle: judgment (no token in the xunit form, N3b) at the helper's line", (record.get("verdict"), rows[0].get("key"), rows[0].get("cause")),
                 ("incomplete", "tests/Helpers.cs:7", "judgment"))
        detail = record.get("mutation_detail") or {}
        # RED, unbent - PRODUCT QUESTION 6: `mutation_detail.file` says tests/CalcTests.cs (the test file) while `mutated_file.path` and the row
        # name the helper the check lives in (the same mismatch is noticed in test_probe_by_code.py's oracle_in_a_helper)
        check_eq("--oracle: the record names the file it mutated (PRODUCT QUESTION 6)", (detail.get("file"), (record.get("mutated_file") or {}).get("path")),
                 ("tests/Helpers.cs", "tests/Helpers.cs"))
        check_eq("--oracle: the helper is back byte for byte and the test file was never touched",
                 ((root / "tests" / "Helpers.cs").read_bytes(), (root / spec["file"]).read_bytes()), (helper, test_src))
        check_eq("--oracle: the probe's identity is still the test file's sha", record.get("test_file_sha256"), PBC.sha256(test_src))
        check_eq("--oracle: no copy left", copies_left(root), [])
    finally:
        cleanup(root)
        cleanup_beside(root)
    root = lang_project(lang, data=test_src, files={"tests/Helpers.cs": helper, "src/Product.cs": helper, "tests/notes.txt": b"x"},
                        protected=["tests/app"])
    try:
        node = node_of(lang)
        cfg = stub_cfg(lang)
        for label, oracle, needle in (
                ("E10: a helper outside every test root (the product tree)", "src/Product.cs::ExpectSum", "is not under a test root"),
                ("E10: a helper in no file that exists", "tests/Nope.cs::ExpectSum", "no such file"),
                ("E10: a helper of another language", "tests/notes.txt::ExpectSum", "is not a csharp file")):
            before = tree_state(root)
            proc, payload = lrun(root, stub, node, spec["iid"], cfg, "--oracle", oracle)
            refused(label, proc, payload, needle)
            check_eq(f"{label}: the tree is unchanged", tree_state(root), before)
        (root / "tests" / "app").mkdir()
        (root / "tests" / "app" / "H.cs").write_bytes(helper)
        before = tree_state(root)
        proc, payload = lrun(root, stub, node, spec["iid"], cfg, "--oracle", "tests/app/H.cs::ExpectSum")
        refused("E10: a helper under protected_app_paths", proc, payload, "not under a test root", "protected_app_paths", "red_sandbox.py --probe")
        check_eq("E10 (protected): the tree is unchanged", tree_state(root), before)
        # the helper of the test's own file needs no root check
        proc, payload = lrun(root, stub, node, spec["iid"], cfg, "--oracle", "Nope")
        check_in("a helper name with no file is looked for in the test's own file",
                 "no declaration named `Nope` in tests/CalcTests.cs holds a check of a form the factory reads", payload.get("error", ""))
        check_in("...and a selection that selects nothing is a refusal, never a pass", "Nothing was changed", payload.get("error", ""))
    finally:
        cleanup(root)
        cleanup_beside(root)


def data_gaps(stub: Path) -> None:
    """K3 / K4 / E2: a language with no row, an unreadable table, an absent key and a malformed entry are four
    different refusals that all say 'factory data gap', and none changes the tree."""
    lang = "csharp"
    spec = LANGS[lang]
    root = lang_project(lang)
    scratch = temp_dir("qa-probe-gaps-")
    try:
        before = tree_state(root)
        (root / "tests" / "Calc.kt").write_text("class CalcTests { fun adds() {} }\n", encoding="utf-8")
        before = tree_state(root)
        proc, payload = lrun(root, stub, "tests/Calc.kt::CalcTests.adds", spec["iid"], stub_cfg(lang))
        text = refused("K3 (.kt: no entry)", proc, payload, "no assertion probe for .kt", "factory data gap", '"assertion_probes"',
                       "red_sandbox.py --probe --repo <project root>")
        check_in("K3: the entry shape names the fields a row needs", "fires_as", text)
        check_eq("K3: the tree is byte-identical", tree_state(root), before)
        good = json.loads(Path(AD.DETECTORS_FILE).read_text(encoding="utf-8"))
        cases = {}
        cases["unreadable"] = scratch / "missing.json"
        broken = scratch / "broken.json"
        broken.write_text("{nope", encoding="utf-8")
        cases["not json"] = broken
        absent = scratch / "absent.json"
        absent.write_text(json.dumps({k: v for k, v in good.items() if k != "assertion_probes"}), encoding="utf-8")
        cases["absent key"] = absent
        malformed = scratch / "malformed.json"
        bad = copy.deepcopy(good)
        bad["assertion_probes"]["csharp"]["assertions"][0]["invert"][0]["fires_as"] = "(unclosed"
        malformed.write_text(json.dumps(bad), encoding="utf-8")
        cases["malformed entry"] = malformed
        needles = {"unreadable": "cannot be read", "not json": "cannot be read", "absent key": "has no `assertion_probes` key",
                   "malformed entry": "assertion_probes.csharp.assertions[0].invert[0].fires_as (X1)"}
        model_entries(root, stub, node_of(lang), spec["iid"])   # t-2064 P4b: the wrapper's own file (with the shipped table), before the snapshots
        for label, path in cases.items():
            before = tree_state(root)
            proc, payload = lrun(root, stub, node_of(lang), spec["iid"], stub_cfg(lang), ASSERTION_DETECTORS_FILE=str(path))
            refused(f"K4 ({label})", proc, payload, "factory data gap", needles[label], "red_sandbox.py --probe")
            check_eq(f"K4 ({label}): the tree is unchanged", tree_state(root), before)
        texts = {l: lrun(root, stub, node_of(lang), spec["iid"], stub_cfg(lang), ASSERTION_DETECTORS_FILE=str(p))[1].get("error", "")
                 for l, p in cases.items()}
        check_eq("K4: the unreadable, the absent and the malformed refusals are three different texts",
                 len({texts["unreadable"], texts["absent key"], texts["malformed entry"]}), 3)
        # E2 (temporal): a table that is read again after the data file is repaired - nothing is remembered
        proc, record = lrun(root, stub, node_of(lang), spec["iid"], stub_cfg(lang))
        check_eq("E2: with the shipped table back, the probe runs (judgment: no token in the xunit form, N3b)", record.get("verdict"), "incomplete")
    finally:
        cleanup(root)
        cleanup_beside(root)
        cleanup(scratch)


def kill_and_recover(stub: Path) -> None:
    """E18 / E20 on the detector path: a probe killed while its file is mutated leaves the way back on disk; the
    next probe puts the author's bytes back (mtime NOW for a file that is not Python) and goes on."""
    lang = "csharp"
    spec = LANGS[lang]
    root = lang_project(lang, mtime_ns=OLD_NS)
    try:
        target = root / spec["file"]
        original = target.read_bytes()
        # a child process by necessity: the stand-in kills ITS PARENT (the role's shell call), which in process would be this test
        proc, payload = lrun(root, stub, node_of(lang), spec["iid"], stub_cfg(lang, "kill_holding_lock"), real=True)
        check("killed: the probe died (no JSON answer)", proc.returncode != 0 and not payload, proc.stdout[-200:] + proc.stderr[-200:])
        left = target.read_bytes()
        check("killed: the file was left MUTATED", left != original and spec["after"].encode() in left)
        folder = root / "qa-factory" / "state" / "probe-copies"
        check_eq("killed: a copy and its record are on disk", sorted(p.suffix for p in folder.glob("*") if p.suffix != ".lock"),
                 [".meta", ".orig"])
        proc, record = lrun(root, stub, node_of(lang), spec["iid"], stub_cfg(lang))
        check_eq("recovered: the next probe runs (judgment: no token in the xunit form, N3b)", (record.get("verdict"), proc.returncode), ("incomplete", 1))
        check_in("recovered: the note says what was recovered", "recovered tests/CalcTests.cs", said(record))   # t-2064 P4b: `said` = the notes and the check rows' notes
        check_eq("recovered: the author's bytes are back and no copy is left", (target.read_bytes() == original, copies_left(root)), (True, []))
        check("E20: the recovered file's mtime is NOW (a file that is not Python)", target.stat().st_mtime_ns > OLD_NS + 10 ** 15)
    finally:
        cleanup(root)
        cleanup_beside(root)


def main() -> None:
    # No argument runs every section; a section name (`languages`, `modes`, `standing`, `bom`, `at`, `refusals`, `traps`, `oracle`,
    # `gaps`, `kill`) runs that one.
    only = set(sys.argv[1:])
    sections = [("languages", lambda stub: [one_language(stub, lang) for lang in LANGS]),
                ("modes", r8_through_the_cli), ("standing", a_standing_record_survives_incomplete),
                ("bom", bom_and_crlf_through_the_run), ("at", at_among_two_declarations),
                ("refusals", refusals_before_the_write), ("traps", traps_through_the_cli),
                ("oracle", oracle_in_a_helper), ("gaps", data_gaps),
                ("kill", kill_and_recover)]
    wanted = [(name, fn) for name, fn in sections if not only or name in only]
    stub_dir = temp_dir("qa-probe-lang-stub-")
    stub = stub_dir / "fake_lang_run_suite.py"
    stub.write_text(LANG_RUN_SUITE, encoding="utf-8")
    try:
        for _name, fn in wanted:
            fn(stub)
    finally:
        cleanup(stub_dir)
    finish("test_probe_by_code_languages_cli")


if __name__ == "__main__":
    main()
