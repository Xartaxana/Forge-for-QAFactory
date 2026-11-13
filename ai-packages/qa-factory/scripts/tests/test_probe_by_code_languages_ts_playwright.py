"""probe_by_code.py: the TypeScript half - EP1-36 (a templated or tagged test, the aggregate of several rows, the tool's
refusal) and RN1-8 (a REAL Playwright report is read per line; E15 is the factory's data, never the tool's gap); split from
test_probe_by_code_languages.py, TD-11c N9.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import copy  # noqa: E402
import json  # noqa: E402
from harness import SCRIPTS, check, check_eq, check_in, cleanup, finish, temp_dir  # noqa: E402
import assertion_detectors as AD  # noqa: E402
import probe_by_code as PBC  # noqa: E402
import proof_level as PL  # noqa: E402
from test_probe_by_code import TASK, cleanup_beside, write_json  # noqa: E402
from probe_by_code_languages_common import (FIX, LANGS, LANG_RUN_SUITE, WRAP, lang_project, lrun, node_of, plan, refusal_of, stub_cfg, task_of)  # noqa: E402


TS_TITLES = ("describe('c', () => {\n  test('adds ${n}', async () => {\n    expect(sum(1, 2)).toBe(3);\n  });\n"
             "  test('adds 5', async () => {\n    expect(sum(1, 2)).toBe(3);\n  });\n"
             "  test('tagged @smoke', async () => {\n    expect(sum(1, 2)).toBe(3);\n  });\n});\n")


TS_ENTRY = AD.assertion_detectors()["typescript"]


TS_FILE = "src/sum.test.ts"


def refusal_class(fn):
    """(class name, name_unproved) of the refusal `fn` raises; ("", None) when it raises none."""
    try:
        fn()
    except PBC.Refusal as exc:
        return type(exc).__name__, getattr(exc, "name_unproved", None)
    return "", None


def ep1_36_titles() -> None:
    """Items 1-3: tags are taken out of both sides, a `${` title is a pattern, the candidates are what `test_source.matches` ties
    to the name, more than one is the old refusal with `--at`."""
    tail = PBC._tail_matches
    check("EP1-36 item 1: a tag the report keeps and the --test leaves out is no mismatch",
          tail("src/a.test.ts::adds @smoke", "adds", TS_ENTRY))
    check("EP1-36 item 1: ...nor the reverse", tail("src/a.test.ts::adds", "adds @smoke", TS_ENTRY))
    no_tag = dict(TS_ENTRY)
    no_tag.pop("title_tag")
    check_eq("EP1-36 item 1: an entry without `title_tag` behaves as today (the tag is part of the title)",
             tail("src/a.test.ts::adds @smoke", "adds", no_tag), False)
    check_eq("EP1-36 item 1 (BEYOND): a tag alone is not a title", tail("src/a.test.ts::adds @smoke", "@smoke", TS_ENTRY), False)
    check_eq("EP1-36 item 1: the same test with a tag is not 'another test' for the longer-title check",
             PBC._longer_title(TS_TITLES, TS_ENTRY, "tagged", "src/a.test.ts::c tagged @smoke")[0], "")
    # item 2: the title is a pattern when the entry reads templates; its literal text must be 3 characters or more
    spec = PBC.parse_node(f"{TS_FILE}::adds ${{n}}")
    check_eq("EP1-36 item 2: a `${` title sets `template`", spec.get("template"), True)
    check_eq("EP1-36 item 2: a title without it does not", PBC.parse_node(f"{TS_FILE}::adds").get("template"), None)
    check_eq("EP1-36 item 2 (AT): 3 literal characters are accepted", PBC.parse_node(f"{TS_FILE}::abc${{n}}").get("template"), True)
    check_in("EP1-36 item 2 (BEYOND): 2 literal characters are refused", "fewer than 3",
             refusal_of(lambda: PBC.parse_node(f"{TS_FILE}::ab${{n}}")))
    check_in("EP1-36 item 2: a title that is only substitutions is refused", "fewer than 3",
             refusal_of(lambda: PBC.parse_node(f"{TS_FILE}::${{a}}${{b}}")))
    # item 3: candidates
    src = PBC.Source(TS_TITLES, TS_ENTRY["lexer"], "t/x.test.ts")
    lines = lambda name: PBC._lines_of(src, PBC.declaration_candidates(src, TS_ENTRY, name, False, "t/x.test.ts"))
    check_eq("EP1-36 item 3: the raw template title is one candidate (the literal 'adds 5' is not it)", lines("adds ${n}"), [2])
    check_eq("EP1-36 item 3: a title the template renders to AND a literal one are two candidates", lines("adds 5"), [2, 5])
    check_eq("EP1-36 item 3: a tagged declaration is found by the title without its tag", lines("tagged"), [8])
    check_eq("EP1-36 item 3: ...and by the title with it (once)", lines("tagged @smoke"), [8])
    check_eq("EP1-36 item 3: a title nothing declares is no candidate", lines("zzz nothing"), [])
    message = refusal_of(lambda: plan("typescript", TS_TITLES, node=f"{TS_FILE}::adds 5"))
    check_in("EP1-36 item 3: two candidates are the old refusal with the door --at", "--at <line>", message)
    mutated, detail, _ctx = plan("typescript", TS_TITLES, node=f"{TS_FILE}::adds 5", at=3)
    mutated = mutated.decode("utf-8") if isinstance(mutated, bytes) else mutated
    check_eq("EP1-36 item 3: --at picks the template's body, and only its assertion changes",
             (detail["candidates"], detail["line"], mutated.count(".not.toBe(3)")), ([2, 5], 3, 1))
    changed = [n for n, (was, now) in enumerate(zip(TS_TITLES.splitlines(), mutated.splitlines())) if was != now]
    check_eq("EP1-36 mutation: one line changed in the one declaration, the other declarations are byte-identical",
             (changed, len(mutated.splitlines()) == len(TS_TITLES.splitlines())), ([2], True))
    tagged, detail, _ctx = plan("typescript", TS_TITLES, node=f"{TS_FILE}::tagged")
    check_eq("EP1-36 item 3: a tagged test is planned by its bare title", detail["declaration_line"], 8)
    # classes of refusal (the producer of `refused: tool`)
    check_eq("§6: no declaration is the tool's, and does not prove the name",
             refusal_class(lambda: plan("typescript", TS_TITLES, node=f"{TS_FILE}::zzz nothing")), ("ToolRefusal", True))
    check_eq("§6: no row for the suffix is the tool's", refusal_class(lambda: PBC.parse_node("t/x.zzz::a"))[0], "ToolRefusal")
    check_eq("§6: a directory is the call's", refusal_class(lambda: PBC.parse_node("tests::a", Path(SCRIPTS)))[0], "Refusal")
    check_eq("§6: the lexer that cannot read the file is the tool's",
             refusal_class(lambda: plan("typescript", "test('a', () => {\n  expect(1).toBe(1);\n"))[0], "ToolRefusal")
    check_eq("§6: no recognised assertion is the tool's", refusal_class(lambda: plan("typescript", "test('adds', () => { const x = 1; });\n", node="t/x.test.ts::adds"))[0], "ToolRefusal")
    check_eq("§6: ...but a wrong --at is the call's", refusal_class(lambda: plan("typescript", WRAP["typescript"][0].replace("{stmt}", "expect(1).toBe(1);"), at=99))[0], "Refusal")
    check_eq("§6: a --test without `::` is the call's", refusal_class(lambda: PBC.parse_node("src/sum.test.ts"))[0], "Refusal")
    check_eq("§6: two declarations are the call's", refusal_class(lambda: plan("typescript", TS_TITLES, node=f"{TS_FILE}::adds 5"))[0], "Refusal")


def judge_rows(rows: list, contract: dict, *, at=None, candidates=(3,), report_read=True, real=False):
    """`_judge_rows` over `rows` for a typescript test with `contract`: (record, the `among` values the judge saw). The
    judge and the frame reader are replaced by the row's own `v` unless `real` (the verdict table is tested elsewhere)."""
    spec = PBC.parse_node(f"{TS_FILE}::adds ${{n}}")
    # N3b: `among` reads the plan's target keys (`target_source`: `at` when --at chose; the check lies in the located body)
    detail = {"language": "typescript", "candidates": list(candidates), "at": at, "line": 3, "end_line": 5,
              "target_source": "at" if at is not None else None, "target_outside_body": False}
    record = {"task": TASK, "notes": [], "expected_location": f"{TS_FILE}:3", "expected_reason": "marker", "verdict": "not_executed"}
    request = {"instance_contracts": {"adds": contract}, "command": {"argv": ["npx", "playwright", "test"]}}
    seen = []
    old_judge, old_site = PBC.judge_probe_row, PBC.reporters.assertion_site

    def stub(row, site, entry, detail_, *, among, argv):
        seen.append(among)
        return {"verdict": row["v"], "actual_location": None, "actual_reason": None, "mismatches": [], "note": row.get("note", ""),
                "observed": {"status": row["status"]}}
    if not real:
        PBC.judge_probe_row = stub
        PBC.reporters.assertion_site = lambda *a, **k: {}
    try:
        PBC._judge_rows(Path("."), record, rows, "junit-xml", spec, detail, request, Path("x"), ["adds"], report_read)
    finally:
        PBC.judge_probe_row, PBC.reporters.assertion_site = old_judge, old_site
    return record, seen


def ep1_36_rows() -> None:
    """Items 4-6: several rows of one test, the worst speaks; no row, rows of two files and the unbound row stop BEFORE the
    aggregate; the tool's gap is written as `language` + `cause`."""
    pattern = {"file": TS_FILE, "report_test_id": "sum.test.ts::c adds ${n}", "report_match": {"pattern": "c\\ adds\\ .+"},
               "classname_match": "file_suffix"}
    row = lambda name, status, v, **extra: dict({"test_id": f"sum.test.ts::{name}", "status": status, "v": v}, **extra)
    two = [row("c adds 1", "failed", "intended_failure"), row("c adds 2", "failed", "intended_failure")]
    record, _ = judge_rows(two, pattern)
    check_eq("EP1-36 item 4: every row failed as intended -> intended_failure, both named", (record["verdict"], len(record["param_rows"])),
             ("intended_failure", 2))
    check_eq("EP1-36 item 4: ...and none of language/cause", ("cause" in record, "language" in record), (False, False))
    record, _ = judge_rows([row("c adds 1", "failed", "intended_failure"), row("c adds 2", "passed", "no_failure")], pattern)
    check_eq("EP1-36 item 4 (mutation: the first row speaks): one survivor outweighs the first row's intended_failure",
             record["verdict"], "no_failure")
    check_in("EP1-36 item 4: the survivor is named", "c adds 2", " ".join(record["notes"]))
    record, _ = judge_rows([row("c adds 1", "passed", "no_failure"), row("c adds 2", "failed", "intended_failure")], pattern)
    check_eq("EP1-36 item 4 (mutation: any instead of all): the order of rows does not matter", record["verdict"], "no_failure")
    record, _ = judge_rows([row("c adds 1", "failed", "intended_failure"), row("c adds 2", "skipped", "not_executed")], pattern)
    check_eq("EP1-36: a skipped row is not an intended failure", record["verdict"], "not_executed")
    record, _ = judge_rows([row("c adds 1", "passed", "no_failure"), row("c adds 2", "failed", "wrong_location")], pattern)
    check_eq("EP1-36: passed + wrong_location -> the mutation that never fired speaks", record["verdict"], "no_failure")
    record, _ = judge_rows([], pattern)
    check_eq("EP1-36 item 4 (M-5): no row at all is not_executed and says why, nothing raised",
             (record["verdict"], bool(record["notes"])), ("not_executed", True))
    check_eq("EP1-36 item 6 (F-1 of t-596): ...but a report that was read and held NO row is a stand that ran nothing: no cause, no language",
             ("cause" in record, "language" in record), (False, False))
    record, _ = judge_rows([row("other adds 1", "passed", "no_failure")], pattern)
    check_eq("EP1-36 item 6 (F-1 CONTROL): rows of the report and none of them this test: the tool could not bind",
             (record["verdict"], record.get("cause"), record.get("language")), ("not_executed", "tooling", "typescript"))
    record, _ = judge_rows([], {"file": TS_FILE, "report_test_id": "sum.test.ts::c adds 1"})
    check_eq("EP1-36 item 6 (F-1): the empty report through the hand-written id branch: no cause either",
             ("cause" in record, "language" in record), (False, False))
    record, _ = judge_rows([], pattern, report_read=False)
    check_eq("EP1-36 item 6: a stand that wrote no report is not a gap of the tool", ("cause" in record, "language" in record), (False, False))
    record, _ = judge_rows([{"test_id": "a/sum.test.ts::c adds 1", "status": "passed", "v": "no_failure"},
                            {"test_id": "b/sum.test.ts::c adds 1", "status": "passed", "v": "no_failure"}],
                           dict(pattern, file="a/sum.test.ts"))
    check_eq("EP1-36 item 4: rows of one file only are read (the neighbour's file is no row of this test)",
             record.get("param_rows"), None)
    record, _ = judge_rows([row("c adds 1", "passed", "no_failure")], dict(pattern, file="x/other.test.ts"), real=True)
    check_eq("EP1-36 item 4: rows that belong to another file than the contract's: not bound, not judged",
             (record["verdict"], record.get("cause")), ("not_executed", "tooling"))
    hand = {"file": TS_FILE, "report_test_id": "sum.test.ts::c adds 1"}
    record, _ = judge_rows([row("c adds 1", "passed", "no_failure"), row("c adds 1", "passed", "no_failure")], hand, real=True)
    check_eq("EP1-36 item 4: a hand-written id (no pattern, no file rule) names ONE row: two are ambiguous",
             (record["verdict"], record.get("cause")), ("not_executed", "tooling"))
    # M-4: `among` is computed, never a constant
    real_rows = [{"test_id": "sum.test.ts::c adds 1", "status": "passed", "message": "", "text": ""}]
    record, seen = judge_rows(real_rows, pattern, at=3, candidates=(2, 5), real=True)
    check_eq("EP1-36 M-4: --at among two declarations + a pass is incomplete, and a gap of the tool",
             (record["verdict"], record.get("cause"), record.get("language")), ("incomplete", "tooling", "typescript"))
    record, seen = judge_rows(real_rows, pattern, at=None, candidates=(2,), real=True)
    check_eq("EP1-36 M-4 (BEYOND): one candidate and a pass is no_failure, and no gap", (record["verdict"], "cause" in record), ("no_failure", False))
    record, seen = judge_rows([row("c adds 1", "failed", "intended_failure")], pattern, at=3, candidates=(2, 5))
    check_eq("EP1-36 M-4: the judge is told `among` from the candidates and --at", seen, [True])
    record, seen = judge_rows([row("c adds 1", "failed", "intended_failure")], pattern, at=None, candidates=(2, 5))
    check_eq("EP1-36 M-4: ...not when no --at chose", seen, [False])
    # no `file` in the contract: bind_row, as before
    # N3a's one binding: a contract with no `file` is read by `matching_rows(rows, spec["node"])`, so the row is the one the NODE names
    # (the tail after the last `::`), not the contract's `report_test_id`; a row with another name is not this test's (not_executed)
    plain = {"report_test_id": "sum.test.ts::c adds 1"}
    record, _ = judge_rows([row("adds ${n}", "failed", "intended_failure")], plain)
    check_eq("EP1-36 item 4: a contract without a file is bound by the node's own name, one row", (record["verdict"], "param_rows" in record), ("intended_failure", False))
    record, _ = judge_rows([row("c adds 1", "failed", "intended_failure")], plain)
    check_eq("EP1-36 item 4: ...and a row named only by the contract's `report_test_id` is not this node's", record["verdict"], "not_executed")
    # the shared aggregator (Python parametrised rows) keeps its behaviour
    probe: dict = {"notes": []}
    first = PBC._worst_of_rows([({"test_id": "t[1]"}, {"verdict": "intended_failure"}), ({"test_id": "t[2]"}, {"verdict": "wrong_location"})],
                               {"node": "t.py::t"}, probe)
    check_eq("EP1-36 item 5: _worst_of_rows is the one aggregator", (probe["param_rows"][1]["verdict"], probe["verdict"], first["verdict"]),
             ("wrong_location", "wrong_location", "wrong_location"))


def ts_profile_project(argv: list, rehearsed: bool = True, verified=None) -> tuple:
    """(root, cfg, manifest, spec, text) of a TypeScript project whose manifest row carries NO selector_args and NO report_test_id."""
    import onboarding_probe as OP
    root = temp_dir("qa-ep136-shape-")
    (root / "src").mkdir()
    text = "describe('c', () => {\n  test('adds', async () => {\n    expect(sum(1, 2)).toBe(3);\n  });\n});\n"
    (root / TS_FILE).write_text(text, encoding="utf-8")
    selectors = {} if verified is None else {"verified": verified}
    cfg = {"profiles": [{"profile_id": "pw", "roots": {"test": "src"}, "selectors": selectors,
                         "commands": {"one_test": {"argv": list(argv), "cwd": "."}}}]}
    if rehearsed:       # True: this command was rehearsed; a list: that command was
        proved = argv if rehearsed is True else rehearsed
        write_json(root / "qa-factory" / "state" / OP.G.REPORTER_REHEARSALS_FILE,
                   {"schema_version": 1, "rehearsals": {"k": {"profile_id": "pw", "argv_digest": OP.argv_digest(proved), "at": "2026-10-01T00:00:00"}}})
    row = {"case": "TC-1", "file": TS_FILE, "instance_id": "adds", "test": "adds", "selector": "adds"}
    return root, cfg, {"tests": [row]}, PBC.parse_node(f"{TS_FILE}::adds"), text


def shape(argv, **kw) -> tuple:
    root, cfg, manifest, spec, text = ts_profile_project(argv, **kw)
    try:
        PBC.run_shape_checks(cfg, manifest, "TC-1", manifest["tests"][0], spec, "adds", "", text, root)
        return "passed", ""
    except PBC.Refusal as exc:
        return type(exc).__name__, str(exc)
    finally:
        cleanup(root)


def ep1_36_shape() -> None:
    """Items 7-8: a row with no hand-written fields is built by `execution_request.code_selection`; a command that is the project's
    own script is refused by name and never passes; `selectors_verified` is the gate's."""
    pw = ["npx", "playwright", "test", "--reporter=junit"]
    check_eq("EP1-36 item 7+8: no hand-written fields, a rehearsed Playwright command: the row is built and the gate passes",
             shape(pw)[0], "passed")
    kind, said = shape(pw, rehearsed=False)
    check_eq("EP1-36 item 8: ...never rehearsed: the profile is not verified (the old refusal and door)", kind, "ToolRefusal")
    check_in("EP1-36 item 8: ...naming selectors.verified", "selector contract", said)
    kind, said = shape(pw, verified=False)
    check_eq("EP1-36 item 8: the literal False wins over a rehearsal on record", kind, "ToolRefusal")
    check_eq("EP1-36 item 8: ...and the literal True over none", shape(pw, rehearsed=False, verified=True)[0], "passed")
    kind, said = shape(["npx", "playwright", "test", "--reporter=line"], rehearsed=pw)
    check_eq("EP1-36 item 8: another argv than the rehearsed one is not verified (command_changed)", kind, "ToolRefusal")
    wrapper = ["node", "run-e2e.mjs"]
    kind, said = shape(wrapper, verified=True)
    check_eq("EP1-36 item 7: a wrapper script builds no selector: refused, and it is the tool's", kind, "ToolRefusal")
    check_in("EP1-36 item 7: ...BY NAME", "the project's own script", said)
    check_in("EP1-36 item 7: ...with the door", "the probe is not run on this profile; onboarding offers the direct form", said)
    # the role's own fields win and the check is as before
    root, cfg, manifest, spec, text = ts_profile_project(pw, rehearsed=False, verified=True)
    try:
        own = dict(manifest["tests"][0], selector_args=["x"], report_test_id="src/sum.test.ts::c adds")
        PBC.run_shape_checks(cfg, {"tests": [own]}, "TC-1", own, spec, "adds", "", text, root)
        check("EP1-36 item 7: hand-written fields pass as before", True)
    except PBC.Refusal as exc:
        check("EP1-36 item 7: hand-written fields pass as before", False, str(exc)[:200])
    finally:
        cleanup(root)


def tool_refusal_record(stub: Path) -> None:
    """§6: the record `refused: tool`, written only when the tool refused and the test is the instance's."""
    spec = LANGS["typescript"]
    no_assert = b"describe('calc', () => {\n  test('adds', async () => {\n    const x = 1;\n  });\n});\n"
    cases = (("E6 no recognised assertion", no_assert, node_of("typescript"), True),
             ("no declaration, the tail is the row's", no_assert.replace(b"'adds'", b"'other'"), node_of("typescript"), True),
             ("no declaration, the tail is NOT the row's", no_assert.replace(b"'adds'", b"'other'"), "src/sum.test.ts::nothing", False),
             ("a missing file", no_assert, "src/gone.test.ts::adds", False),
             ("a file that is not the row's", no_assert, "src/other.test.ts::adds", False))
    for label, data, node, wrote in cases:
        root = lang_project("typescript", data=data, files={"src/other.test.ts": data})
        try:
            before = (root / spec["file"]).read_bytes()
            proc, payload = lrun(root, stub, node, spec["iid"], stub_cfg("typescript"))
            check_eq(f"§6 {label}: exit 2, one JSON, refused", (proc.returncode, payload.get("status")), (2, "refused"))
            path = task_of(root) / "work" / "probes" / f"{spec['iid']}.json"
            # PRODUCT QUESTION 13 (t-2064-p4b2t3-report.md): the walk road's refusals ("no check of a form the factory reads was found", the
            # empty plan) write NO `refused: tool` record (t-2143 N4, EP1-36 §6; the same fork as question 2 of t-2064-p4b2t-report.md, which the
            # no_assert pin of test_probe_by_code.py took as "refusal, no record"): every pin of a `wrote` case below that reads the record is
            # RED for that one reason, and reads `{}` instead of crashing
            ask = " (PRODUCT QUESTION 13)" if wrote else ""
            check_eq(f"§6 {label}: the record exists only when the tool refused and the name is proved{ask}", path.is_file(), wrote)
            if wrote:
                def stored() -> dict:
                    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
                record = stored()
                check_eq(f"§6 {label}: not_executed, refused tool, the bytes read, the text of the refusal{ask}",
                         (record.get("verdict"), record.get("refused"), record.get("test_file_sha256"), record.get("notes"), record.get("instance_id")),
                         ("not_executed", "tool", PBC.sha256(before), [payload["error"]], spec["iid"]))
                # F-2 (t-596): the record says it is the tool's the way `_tooling_gap` does, so ONE reader (`tooling_gap_key`) answers for it
                check_eq(f"§6 {label}: the record names the tool and the language (cause, language){ask}",
                         (record.get("cause"), record.get("language")), ("tooling", "typescript"))
                check_eq(f"§6 {label}: ...and tooling_gap_key reads it for these bytes (and for no other){ask}",
                         (PL.tooling_gap_key(task_of(root), spec["iid"], PBC.sha256(before)), PL.tooling_gap_key(task_of(root), spec["iid"], "0" * 64)),
                         ("tooling:typescript", ""))
                check_eq(f"§6 {label}: ...and probe_could_not_run holds too{ask}", PL.probe_could_not_run(task_of(root), spec["iid"], PBC.sha256(before)), True)
                entry = next(t for t in json.loads((task_of(root) / "work" / "automation-manifest.json").read_text(encoding="utf-8"))["tests"]
                             if t["instance_id"] == spec["iid"])
                got = PL.already_probed(entry, {"tests": [entry]}, task_of(root), project=root)
                check_eq(f"§6 {label}: already_probed does not read it as probed", got.get("probed"), False)
                proc, payload = lrun(root, stub, node, spec["iid"], stub_cfg("typescript"))
                check_eq(f"§6 {label}: a repeat on the same bytes replaces it (idempotent){ask}",
                         stored().get("test_file_sha256"), PBC.sha256(before))
                (root / spec["file"]).write_bytes(before + b"// fixed\n")
                check(f"§6 other bytes after a fix: the record is of the old ones{ask}",
                      bool(record.get("test_file_sha256")) and record["test_file_sha256"] != PBC.sha256((root / spec["file"]).read_bytes()))
            check_eq(f"§6 {label}: the author's file is untouched", (root / spec["file"]).read_bytes() in (before, before + b"// fixed\n"), True)
        finally:
            cleanup(root)
            cleanup_beside(root)
    check_eq("§6 F-2: a .py file is no entry of the table ...",
             PBC.AD.entry_for_suffix(PBC.AD.assertion_detectors(), ".py"), (None, None))
    check_eq("§6 N4 (S4): ... so its refusal record takes the language from the AST reader's entry (the class word covers it)",
             PBC.AD.ast_entry(".py")[0], "python")
    # an intended_failure stands (E23); a write failure is a line on stderr and exit 2 (the answer never changes)
    for label, setup in (("an intended_failure stands", "stand"), ("a record that cannot be written", "block")):
        root = lang_project("typescript", data=no_assert)
        try:
            probes = task_of(root) / "work" / "probes"
            if setup == "stand":
                write_json(probes / f"{spec['iid']}.json", {"verdict": "intended_failure", "test_file_sha256": "abc"})
            else:
                probes.parent.mkdir(parents=True, exist_ok=True)
                probes.write_text("a file where the folder should be", encoding="utf-8")
            proc, payload = lrun(root, stub, node_of("typescript"), spec["iid"], stub_cfg("typescript"))
            check_eq(f"§6 {label}: exit 2 and one JSON", (proc.returncode, payload.get("status")), (2, "refused"))
            if setup == "stand":
                stored = json.loads((probes / f"{spec['iid']}.json").read_text(encoding="utf-8"))
                # the verdict and its bytes stay (green); the ATTEMPT is added only by the refusal's record: PRODUCT QUESTION 13 (no record on the
                # walk road's refusal), so `last_attempt` is absent and this pin is red for that one reason
                check_eq(f"§6 {label}: the verdict and its bytes stay, the attempt is added (PRODUCT QUESTION 13)",
                         (stored.get("verdict"), stored.get("test_file_sha256"), (stored.get("last_attempt") or {}).get("verdict")),
                         ("intended_failure", "abc", "not_executed"))
            else:
                # PRODUCT QUESTION 13 again: the walk's empty-plan refusal never tries to write a record, so there is no write failure to say
                check_in(f"§6 {label}: stderr says it (PRODUCT QUESTION 13)", "was not written", proc.stderr)
        finally:
            cleanup(root)
            cleanup_beside(root)
    root = lang_project("typescript", data=no_assert)
    try:
        proc, payload = lrun(root, stub, node_of("typescript"), "nobody", stub_cfg("typescript"))
        check_eq("§6 an instance the manifest does not name: refused (the call's), no record",
                 (proc.returncode, (task_of(root) / "work" / "probes").is_dir()), (2, False))
    finally:
        cleanup(root)
        cleanup_beside(root)


BIN_PW = ["npx", "playwright", "test"]


RN1_8_SPEC = "tests/api/cart/add-to-cart.spec.ts"


RN1_8_CASE = "LOCAL-1_TC_010"


RN1_8_PLACEHOLDER = "{project_root}"      # the fixtures' one substitution (E20): the stand's root, replaced here by the temp root


def rn1_8_real(name: str, root: Path) -> str:
    """The text of a REAL LOCAL-1 file (run 3, 02-03.11: the Playwright report and the probe record of TC_010) with the
    token `{project_root}` replaced by this test's temp root. In the JSON record the token sits in a JSON string, so a
    backslash of the root is doubled there (the record is read as JSON, never as text)."""
    text = (FIX / name).read_text(encoding="utf-8")
    return text.replace(RN1_8_PLACEHOLDER, json.dumps(str(root))[1:-1] if name.endswith(".json") else str(root))


class Rn1_8World:
    """The shared setup of the RN1-8 keys: the table entry, the pairs, the REAL Playwright report of LOCAL-1 run 3 (10 rows,
    `playwright-red-probe.junit.xml`, bytes of `evidence/runs/64d1d369a594bd0a73fd/red_probe-...junit.xml` with the stand's
    root as `{project_root}`) and the real probe record of TC_010 (`playwright-red-probe.record.json`), a project root holding
    the spec. The spec file's CONTENT is read by nothing under test (the site is read from the report's frame; the file only
    has to exist at the frame's path): it is a copy of `sum.test.ts`, the one TypeScript file of this fixture folder."""

    def __init__(self, root: Path) -> None:
        import reporters
        self.reporters = reporters
        self.root = root
        self.ts = AD.assertion_detectors()["typescript"]
        pairs = {p["id"]: p for p in self.ts["assertions"][0]["invert"]}
        self.t1, self.t2 = pairs["T1"], pairs["T2"]
        (root / "tests" / "api" / "cart").mkdir(parents=True)
        self.spec_file = root / "tests" / "api" / "cart" / "add-to-cart.spec.ts"
        self.spec_file.write_bytes((FIX / "sum.test.ts").read_bytes())
        report = root / "report.junit.xml"
        report.write_text(rn1_8_real("playwright-red-probe.junit.xml", root), encoding="utf-8")
        self.rows = reporters.read_rows(report, "junit-xml")
        self.record = json.loads(rn1_8_real("playwright-red-probe.record.json", root))
        self.red = next(r for r in self.rows if RN1_8_CASE in r["test_id"])
        d = self.record["mutation_detail"]
        # the probe's own detail for that instance, taken from the real record (line 109, candidates [106], T2)
        self.detail = {"line": d["line"], "end_line": d["end_line"], "language": d["language"], "candidates": list(d["candidates"]),
                       "at": d["at"], "pair": d["pair"], "pair_id": d["pair_id"], "fires_as": self.t2["fires_as"]}
        self.grammar = AD.grammar_of(self.ts)

    def site_of(self, row: dict) -> dict:
        frames, skip, frame_path = self.grammar
        return self.reporters.assertion_site(row, "junit-xml", self.root, self.spec_file, pytest_command=False,
                                             runtime="typescript", frames=frames, skip_frames=skip, frame_path=frame_path)

    def judge(self, row: dict, site: dict = None, argv=BIN_PW) -> dict:
        return PBC.judge_probe_row(row, site or self.site_of(row), self.ts, self.detail, among=False, argv=argv)

    def with_text(self, text: str) -> list:
        """The TC_010 row alone (a one-row list), its failure text replaced."""
        rows = [copy.deepcopy(self.red)]
        rows[0]["problems"][0]["text"] = text
        return rows

    def original_red(self) -> list:
        """The TC_010 row alone, with the ORIGINAL form's red (`.toBeLessThan`) - what a probe that did not invert would show."""
        rows = [copy.deepcopy(self.red)]
        problem = rows[0]["problems"][0]
        problem["text"] = problem["text"].replace("expect(received).not.toBeLessThan(expected)", "expect(received).toBeLessThan(expected)")
        return rows

    def record_of(self, report_rows: list) -> dict:
        """The record `_judge_rows` writes for TC_010 over `report_rows`. The contract is the one the code builds for a
        project command (file + `classname_match: file_suffix`), so the judgment does not depend on how an id is spelled."""
        spec = PBC.parse_node(RN1_8_SPEC + "::@regression " + RN1_8_CASE + " repeat add of the same book sums quantities in one line")
        record = {"task": TASK, "notes": [], "expected_location": RN1_8_SPEC + ":109", "expected_reason": "marker",
                  "verdict": "not_executed"}
        own = {"report_test_id": self.red["test_id"], "file": RN1_8_SPEC, "classname_match": "file_suffix"}
        request = {"instance_contracts": {"adds": own}, "command": {"argv": BIN_PW}}
        PBC._judge_rows(self.root, record, report_rows, "junit-xml", spec, self.detail, request, self.spec_file, ["adds"], True)
        return record


def rn1_8_k1_k2(world: Rn1_8World) -> None:
    rows, red = world.rows, world.red
    problem = red["problems"][0]
    check_eq("K-N4-3a premise: the REAL LOCAL-1 report has 10 rows, one failed (TC_010)",
             (len(rows), [r["status"] for r in rows].count("failed"), red["status"]), (10, 1, "failed"))
    check("K-N4-3a: the TC_010 message is a place and a title (the Playwright shape), not the assertion",
          problem["message"].startswith("add-to-cart.spec.ts:106:1 "))
    site = world.site_of(red)
    check_eq("K-N4-3a: the site is read at line 109 of the project's spec, an assertion",
             (site["location"], site["failure_kind"]), (RN1_8_SPEC + ":109", "assertion"))
    check_eq("K-N4-3b premise: the real record of that probe said incomplete / tooling (the defect RN1-8 fixed)",
             (world.record["verdict"], world.record["cause"]), ("incomplete", "tooling"))
    # the record is a snapshot of the real run: its `fires_as` is the T2 row as it stood THEN, so the premise pins the
    # place and the pair, never the row's text (the row grew an alternative in t-1953 and the snapshot did not)
    check_eq("K-N4-3b premise: ...its mutation detail is the probe's own: line 109, candidates [106], pair T2",
             (world.detail["line"], world.detail["candidates"], world.detail["pair_id"], bool(world.record["mutation_detail"]["fires_as"])),
             (109, [106], "T2", True))
    got = world.judge(red)
    check_eq("K-N4-3b N3b: the real report (recorded before the marker existed), failed at the mutated line with `.not.toBeLessThan`: "
             "judgment - the place and the wording prove nothing", (got["verdict"], got.get("cause"), "proved_by" in got),
             ("incomplete", "judgment", False))
    marked = copy.deepcopy(red)
    marked["problems"][0]["message"] = "qa-probe-rn18 " + marked["problems"][0]["message"]
    got = PBC.judge_probe_row(marked, world.site_of(marked), world.ts, dict(world.detail, message_marker="qa-probe-rn18"), among=False, argv=BIN_PW)
    check_eq("K-N4-3b N3b control: the same row holding the token is proved by the marker", (got["verdict"], got.get("proved_by")),
             ("intended_failure", "marker"))
    control = world.original_red()
    shown = control[0]["problems"][0]["text"].split("> 109")[0]       # the message part, before the code frame (which echoes the mutated line)
    check("K2 control premise: the text really changed", "not.toBeLessThan" not in shown and "expect(received).toBeLessThan(expected)" in shown)
    got = world.judge(control[0])
    check_eq("K2: the same report with `.toBeLessThan` (the original's own red) is NOT intended_failure", got["verdict"], "incomplete")
    check_eq("K4: ...it is E15, and the answer is the code critic's to judge (`cause: judgment`), not the tool's gap", got.get("cause"), "judgment")
    away = world.site_of(red)
    away["location"] = RN1_8_SPEC + ":30"
    check_eq("edge: the failing text fires but the failure is NOT at the mutated line: judgment, never intended_failure (N3b)",
             world.judge(red, away, argv=[])["verdict"], "incomplete")


def rn1_8_edges(world: Rn1_8World) -> None:
    fires_as = world.t2["fires_as"]
    empty = {"status": "failed", "problems": [{"kind": "failure", "message": "", "text": ""}]}
    check_eq("edge: an empty message and an empty text match nothing", PBC.fires_on(empty, world.ts, fires_as), False)
    blank = {"status": "failed", "problems": [{"kind": "failure", "message": "  \n\t\n", "text": "   \n\n  "}]}
    check_eq("edge: lines of whitespace only are skipped (no subject, no match)", PBC.fires_on(blank, world.ts, fires_as), False)
    text = world.red["problems"][0]["text"]
    check("E19 premise: the real text holds a `Retry #1` block, after the first block", "Retry #1" in text)
    first_block = world.with_text(text.split("    Retry #1")[0])
    check("E19 premise: the cut really removed the retry", "Retry #1" not in first_block[0]["problems"][0]["text"])
    check_eq("E19: the text cut at `Retry #1` gives the same verdict as the whole text (a retry does not change the verdict)",
             world.judge(first_block[0])["verdict"], world.judge(world.red)["verdict"])
    echo = {"problems": [{"kind": "failure", "message": "", "text": "boom\n  > 12 |   expect(received).not.toBe(3);\n      at a.ts:1:1"}]}
    check_eq("edge: a code frame line echoing the statement (`> 12 | expect(..)`) is not the start of a line",
             PBC.fires_on(echo, world.ts, fires_as), False)
    check_eq("edge: the first line alone still fires (the old whole-text case)",
             PBC.fires_on({"problems": [{"kind": "failure", "message": "expect(received).not.toBe(expected)", "text": ""}]},
                          world.ts, fires_as), True)


def rn1_8_k3_samples(world: Rn1_8World) -> None:
    """K3 / m-2: the Playwright-shaped samples live in `fires` / `not` of samples.json, one reading (AD.fires_in)."""
    samples = json.loads((FIX / "samples.json").read_text(encoding="utf-8"))["pairs"]
    for pair_id, pair in (("T1", world.t1), ("T2", world.t2)):
        for label, expected in (("fires", True), ("not", False)):
            shaped = [t for t in samples[pair_id][label] if "[chromium]" in t]
            check_eq(f"K3: {pair_id} has a Playwright-shaped sample in `{label}`", len(shaped), 1)
            for text in shaped:
                got = PBC.fires_on({"problems": [{"kind": "failure", "message": "cart.spec.ts:7:1 title", "text": text}]},
                                   world.ts, pair["fires_as"])
                check_eq(f"K3: {pair_id} {label}: the Playwright shape -> {expected}", got, expected)
                if expected:
                    check_eq(f"K3: {pair_id}: ...and the same sample by the WHOLE text does not fire (the old reading missed it)",
                             AD.fires_matches(pair["fires_as"], text), False)
    check_eq("K9: probe_by_code has no second reader of `fires_as` (the echo guard and fires_on go through AD.fires_in)",
             "AD.fires_matches" in Path(PBC.__file__).read_text(encoding="utf-8"), False)


def rn1_8_k8_author_message(world: Rn1_8World) -> None:
    """m-1: the author's own assertion message must never be what turns a red into `intended_failure`."""
    fires_as = world.t2["fires_as"]
    author = "add accepted\nexpected status not to be 500"      # a two-line author message; line 2 looks like a T2 message
    as_message = {"problems": [{"kind": "failure", "message": author, "text": ""}]}
    check_eq("K8: the author's two-line `message` attribute is matched WHOLE: it does not fire (never per line)",
             PBC.fires_on(as_message, world.ts, fires_as), False)
    check_eq("K8 control: the one-line `message` that IS the library's inverted text fires",
             PBC.fires_on({"problems": [{"kind": "failure", "message": "expect(received).not.toBe(expected)", "text": ""}]},
                          world.ts, fires_as), True)
    red = world.original_red()
    red[0]["problems"][0]["message"] = author
    got = world.judge(red[0])
    check_eq("K8: the original form's red with the two-line author message in `message`: incomplete (judgment), not intended_failure",
             (got["verdict"], got.get("cause")), ("incomplete", "judgment"))


def rn1_8_k4_k5_k10_records(world: Rn1_8World) -> None:
    rows, control = world.rows, world.original_red()
    record = world.record_of(rows)
    check_eq("K1 (record) N3b: the real report (no token) through _judge_rows: judgment, not intended_failure", (record["verdict"], record.get("cause")),
             ("incomplete", "judgment"))
    record = world.record_of(control)
    check_eq("K4: E15 through _judge_rows: incomplete, cause judgment, the language named",
             (record["verdict"], record.get("cause"), record.get("language")), ("incomplete", "judgment", "typescript"))
    check_eq("K4: ...with the facts the critic judges: the whole text and the place, never a verdict",
             (sorted(k for k in ("failure_text", "location") if record["judgment_facts"].get(k) is not None),
              "verdict" in record["judgment_facts"]), (["failure_text", "location"], False))
    task = world.root / "task"
    path = PL.probe_record_path(task, "adds")
    path.parent.mkdir(parents=True)
    record["test_file_sha256"] = "a" * 64
    path.write_text(json.dumps(record), encoding="utf-8")
    check_eq("K4: tooling_gap_key reads NO class from an E15 record, so `probe gap: tooling:typescript` is not asked",
             PL.tooling_gap_key(task, "adds", "a" * 64), "")
    path.write_text(json.dumps(dict(record, cause="tooling")), encoding="utf-8")
    check_eq("K4 control: the same record with `cause: tooling` DOES name the class",
             PL.tooling_gap_key(task, "adds", "a" * 64), "tooling:typescript")
    unread = world.with_text("Error: boom\n\n    no frame in this text")
    record = world.record_of(unread)
    check_eq("K5 (t-2143 N4): a failed row with TEXT and no readable frame is the critic's - the place is a fact he reads himself",
             (record["verdict"], record.get("cause"), record.get("language")), ("incomplete", "judgment", "typescript"))
    check_eq("K5: ... its text is the fact, and the place is null", ((record.get("judgment_facts") or {}).get("failure_text"),
             (record.get("judgment_facts") or {}).get("location")), ("Error: boom\n\n    no frame in this text", None))
    quiet = world.with_text("")
    quiet[0]["problems"][0]["message"] = ""
    record = world.record_of(quiet)
    check_eq("K5 control: a failed row with NO message and NO text is still the tool's gap: incomplete + cause tooling",
             (record["verdict"], record.get("cause"), record.get("language")), ("incomplete", "tooling", "typescript"))


def rn1_8_k10_several_rows(world: Rn1_8World) -> None:
    """m-3: with several report rows `judgment` is decided over ALL surviving incomplete rows, not the first."""
    e15, gap = world.original_red()[0], world.with_text("Error: boom\n\n    no frame in this text")[0]
    for label, pair in (("E15 first", [e15, gap]), ("gap first", [gap, e15])):
        record = world.record_of(pair)
        check_eq(f"K10 (N4): two rows ({label}): one E15 and one unread failure WITH text -> both are the critic's: cause judgment, both in rows",
                 (record["verdict"], record.get("cause"), len((record.get("judgment_facts") or {}).get("rows") or [])),
                 ("incomplete", "judgment", 2))
    quiet = world.with_text("")
    quiet[0]["problems"][0]["message"] = ""
    for label, pair in (("E15 first", [e15, quiet[0]]), ("gap first", [quiet[0], e15])):
        record = world.record_of(pair)
        check_eq(f"K10 control: two rows ({label}): one E15 and one failure with NO text -> cause tooling (judgment only if ALL are)",
                 (record["verdict"], record.get("cause")), ("incomplete", "tooling"))
    record = world.record_of([e15, copy.deepcopy(e15)])
    check_eq("K10 control: two E15 rows -> cause judgment", (record["verdict"], record.get("cause")), ("incomplete", "judgment"))


def rn1_8_playwright_report() -> None:
    for key in (rn1_8_k1_k2, rn1_8_edges, rn1_8_k3_samples, rn1_8_k8_author_message, rn1_8_k4_k5_k10_records, rn1_8_k10_several_rows):
        root = temp_dir("qa-probe-rn1-8-")
        try:
            key(Rn1_8World(root))
        finally:
            cleanup(root)


def main() -> None:
    ep1_36_titles()
    ep1_36_rows()
    ep1_36_shape()
    rn1_8_playwright_report()
    stub_dir = temp_dir("qa-probe-lang-stub-")
    stub = stub_dir / "fake_lang_run_suite.py"
    stub.write_text(LANG_RUN_SUITE, encoding="utf-8")
    try:
        tool_refusal_record(stub)
    finally:
        cleanup(stub_dir)
    finish("test_probe_by_code_languages_ts_playwright")


if __name__ == "__main__":
    main()
