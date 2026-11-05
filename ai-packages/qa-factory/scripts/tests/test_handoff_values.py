#!/usr/bin/env python3
"""A handover form is filled in one call: `handoff_check.py --values`, array paths, ONE applier (SC1-2 part A1) and ONE
refusal with one ready command (part A2).

The failure behind every key: a scout filled its form with 89 separate `--set` processes (35-50 s each), a strategist
with 73 `Edit` calls, and `--set scope[1].id` could not create the second row at all; the refusal that taught them
printed a `--set` command under every problem. Each test says the one behaviour it pins and what it protects; the keys
are the names K-A* of the spec (t-1243, section 3 parts A1 and A2).
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import (FIXTURES, PLUGIN_ROOT, SCRIPTS, check, check_eq, check_in, check_not_in, cleanup,  # noqa: E402
                     finish, run_script, temp_project)

sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))
import handoff  # noqa: E402
import handoff_check as H  # noqa: E402

CONTRACT = "s2-tester-to-strategist"
DISPATCH = "S2-qa-requirements-tester-1"
FIXTURE = FIXTURES / "s2-handoff-13877" / "work" / "handoffs" / f"{DISPATCH}.yaml"
OLD_JSON_KEYS = ("contract", "fixed", "shortened", "judged", "filled", "fields", "untouched", "no_verdict", "problems")


# ------------------------------------------------------------------------------------------------ scaffolding
def _story(root: Path) -> Path:
    art = root / "artifacts" / "QA-9"
    (art / "work").mkdir(parents=True)
    return art


def _form(art: Path, dispatch: str = DISPATCH) -> Path:
    """A fresh S2 form, started the way the factory starts it (`handoff_init.py`)."""
    run_script("handoff_init.py", "--task", "QA-9", "--stage", "S2", "--role", "qa-requirements-tester",
               "--to", "qa-test-strategist", "--dispatch", dispatch, "--task-root", str(art))
    return art / "work" / "handoffs" / f"{dispatch}.yaml"


def _form5(art: Path, dispatch: str) -> Path:
    """A fresh S5 code-critic form: untouched at birth, which the S2 form is not."""
    run_script("handoff_init.py", "--task", "QA-9", "--stage", "S5", "--role", "qa-code-critic",
               "--to", "qa-automator", "--dispatch", dispatch, "--task-root", str(art))
    return art / "work" / "handoffs" / f"{dispatch}.yaml"


def _doc(form: Path):
    return handoff.parse(form.read_text(encoding="utf-8"))


def _hc(art: Path, form: Path, *flags: str):
    done = run_script("handoff_check.py", "--file", str(form), "--task-root", str(art), "--no-judge", *flags)
    out = done.stdout
    return done.returncode, (json.loads(out) if "--json" in flags and out.lstrip().startswith("{") else out)


def _hc_stdin(art: Path, form: Path, text: str, *flags: str):
    done = subprocess.run([sys.executable, "-B", str(SCRIPTS / "handoff_check.py"), "--file", str(form),
                           "--task-root", str(art), "--no-judge", *flags],
                          input=text, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
    return done.returncode, done.stdout


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _apply(form: Path, text: str, raw: bool = False):
    """The values text through the one applier, in memory: `(document, applied, problems, notes)`."""
    pairs, bad = H.parse_values(text)
    assert not bad, [p.text for p in bad]
    doc = _doc(form)
    return H.apply_values(doc, CONTRACT, pairs, raw=raw)


def _paths(problems) -> list:
    return [p["path"] if isinstance(p, dict) else p.path for p in problems]


# ---------------------------------------------------------------------------------------------------- the keys
def one_call_fills_the_real_s2_form() -> None:
    """K-A1: the values of the real 13877 form, every path the CURRENT spec knows, go in with ONE call and leave no
    problem the form itself did not already have (the baseline is `check` on the fixture, same root)."""
    root = temp_project("qa-values-a1-")
    try:
        art = _story(root)
        form = _form(art)
        spec = handoff.spec(CONTRACT)
        fixture = handoff.parse(FIXTURE.read_text(encoding="utf-8"))
        lines = [f"{path}: {json.dumps(node.value, ensure_ascii=False)}" for path, node in fixture.nodes.items()
                 if not handoff.owned_by_contract(path) and H.INDEXED.sub("[]", path) in spec
                 and not handoff.is_placeholder(node.value)]
        values = art / "work" / "all-values.txt"
        values.write_text("\n".join(lines) + "\n", encoding="utf-8")
        check("K-A1: the values file carries many paths, rows included", len(lines) > 100 and any(
            line.startswith("scope[14].id:") for line in lines), str(len(lines)))
        base_doc, _f, base_problems, _j, _d = H.check(handoff.parse(FIXTURE.read_text(encoding="utf-8")), CONTRACT,
                                                      H.Artifacts(art, dispatch=DISPATCH), fix=True, use_judge=False)
        baseline = set(_paths(base_problems))
        code, report = _hc(art, form, "--fix", "--values", str(values), "--json")
        check_eq("K-A1: one call - the report is JSON and counts what was applied", report["values_applied"], len(lines))
        extra = sorted(set(_paths(report["problems"])) - baseline)
        check_eq("K-A1: no problem beyond the ones the fixture itself has", extra, [])
        if not baseline:
            check_eq("K-A1: the fixture has no problems, so neither has the form (exit 0)", code, 0)
        doc = _doc(form)
        check_eq("K-A1: fifteen requirement rows exist", doc.rows("scope"), list(range(15)))
        check_eq("K-A1: the last row is the fixture's", doc.get("scope[14].id"), fixture.get("scope[14].id"))
        check_eq("K-A1: a nested reading row exists", doc.get("open_questions[1].readings[1].id"), "b")
    finally:
        cleanup(root)


def stdin_is_the_same_door() -> None:
    """K-A1b: `--values -` reads the same text from stdin (the role with Bash writes no file at all)."""
    root = temp_project("qa-values-stdin-")
    try:
        art = _story(root)
        form = _form(art)
        code, out = _hc_stdin(art, form, "scope[0].id: R-1\nheader.verdict: ok\n", "--values", "-")
        doc = _doc(form)
        check_eq("K-A1b: stdin values are written", (doc.get("scope[0].id"), doc.get("header.verdict")), ("R-1", "ok"))
        check_eq("K-A1b: and no file beside the form is left behind", sorted(p.name for p in form.parent.iterdir()),
                 [form.name])
    finally:
        cleanup(root)


def an_index_equal_to_the_row_count_opens_a_row_from_the_contract() -> None:
    """K-A2: `scope[1].id` on a one-row form opens row 1. The other rows' values are never copied into it."""
    root = temp_project("qa-values-a2-")
    try:
        art = _story(root)
        form = _form(art)
        _hc(art, form, "--set", "scope[0].id=R-1", "--set", "scope[0].reason=first")
        doc, applied, problems, notes = _apply(form, "scope[1].id: R-2\n")
        check_eq("K-A2: the row opens and the id is written", (doc.rows("scope"), doc.get("scope[1].id"), applied),
                 ([0, 1], "R-2", 1))
        check_eq("K-A2: no problem", _paths(problems), [])
        check_eq("K-A2: row 1 carries the contract's placeholder, not row 0's reason",
                 doc.get("scope[1].reason"), handoff.template(CONTRACT).get("scope[0].reason"))
        check_eq("K-A2: row 0 is untouched", (doc.get("scope[0].id"), doc.get("scope[0].reason")), ("R-1", "first"))
    finally:
        cleanup(root)


def the_opened_row_is_the_contracts_template_row() -> None:
    """K-A2b: there is ONE row builder - `_row_template` of the contract; the opened lines equal its lines."""
    root = temp_project("qa-values-a2b-")
    try:
        art = _story(root)
        form = _form(art)
        _hc(art, form, "--set", "scope[0].id=R-1")                 # the form's own row 0 now differs from the contract's
        doc = _doc(form)
        tpl = H._row_template(handoff.template(CONTRACT), "scope")[2]
        last = max(n.end_line for p, n in doc.nodes.items() if p.startswith("scope[0]"))
        check("K-A2b: open_row says it opened the row", H.open_row(doc, CONTRACT, "scope", 1))
        check_eq("K-A2b: the lines after the last row are the contract's row, line for line",
                 doc.lines[last + 1:last + 1 + len(tpl)], tpl)
        check_eq("K-A2b: an index of an existing row opens nothing", H.open_row(doc, CONTRACT, "scope", 0), False)
        check_eq("K-A2b: nor does an index past the next one", H.open_row(doc, CONTRACT, "scope", 5), False)
    finally:
        cleanup(root)


def an_index_beyond_the_row_count_is_refused_and_opens_nothing() -> None:
    """K-A3: a hole is the role's mistake - no row appears and the problem names the row that is next; in-order
    indexes of one file open one row after another."""
    root = temp_project("qa-values-a3-")
    try:
        art = _story(root)
        form = _form(art)
        before = form.read_text(encoding="utf-8")
        doc, applied, problems, _n = _apply(form, "scope[2].id: R-3\n")
        check_eq("K-A3: a hole is one problem on that path", _paths(problems), ["scope[2].id"])
        check_in("K-A3: it names the next row", "the next row is `scope[1]`", problems[0].text)
        check_eq("K-A3: nothing is written and no row is opened", (applied, doc.text()), (0, before))
        doc, applied, problems, _n = _apply(form, "scope[3].id: R-4\nscope[1].id: R-2\n")
        check_eq("K-A3: scope[1] opens, scope[3] still has a hole before it", (doc.rows("scope"), _paths(problems)),
                 ([0, 1], ["scope[3].id"]))
        # AT the limit: two rows in order in one file, written backwards - the applier orders them
        _hc(art, form, "--set", "scope[1].id=R-2")
        doc, applied, problems, _n = _apply(form, "scope[3].id: R-4\nscope[2].id: R-3\n")
        check_eq("K-A3: scope[2] and scope[3] in one file open in order", (doc.rows("scope"), _paths(problems), applied),
                 ([0, 1, 2, 3], [], 2))
        check_eq("K-A3: each row has its own id", [doc.get(f"scope[{i}].id") for i in (1, 2, 3)], ["R-2", "R-3", "R-4"])
        doc, applied, problems, _n = _apply(form, "scope[3].id: R-4\nscope[2].id: R-3\nscope[5].id: R-6\n")
        check_eq("K-A3: BEYOND - scope[5] after scope[3] is refused, the rest stands",
                 (doc.rows("scope"), _paths(problems)), ([0, 1, 2, 3], ["scope[5].id"]))
    finally:
        cleanup(root)


def a_nested_row_opens_inside_its_parent() -> None:
    """K-A4: `open_questions[0].readings[1]` lands inside question 0, not at the end of the list or in question 1."""
    root = temp_project("qa-values-a4-")
    try:
        art = _story(root)
        form = _form(art)
        text = ("open_questions[1].id: Q-2\n"
                "open_questions[0].readings[1].id: b\n"
                "open_questions[0].readings[1].reading: the other way\n")
        doc, applied, problems, _n = _apply(form, text)
        check_eq("K-A4: no problem", _paths(problems), [])
        check_eq("K-A4: question 0 has two readings, the new question brings its template reading",
                 (doc.rows("open_questions"), doc.rows("open_questions[0].readings"),
                  doc.rows("open_questions[1].readings")), ([0, 1], [0, 1], [0]))
        line = lambda path: doc.nodes[path].line  # noqa: E731
        check("K-A4: the new reading sits between reading 0 and question 1",
              line("open_questions[0].readings[0].cost") < line("open_questions[0].readings[1].id")
              < line("open_questions[1].id"))
        check_eq("K-A4: its words are where they were said",
                 (doc.get("open_questions[0].readings[1].reading"), doc.get("open_questions[1].id")),
                 ("the other way", "Q-2"))
        doc, _a, problems, _n = _apply(form, "open_questions[0].readings[4].id: z\n")
        check_in("K-A4: a hole inside a nested list is refused too", "the next row is `open_questions[0].readings[1]`",
                 problems[0].text)
    finally:
        cleanup(root)


def a_placeholder_left_in_the_values_is_not_written() -> None:
    """K-A5: a skeleton line the role left as it was is not a word - it neither overwrites a value nor opens a row."""
    root = temp_project("qa-values-a5-")
    try:
        art = _story(root)
        form = _form(art)
        _hc(art, form, "--set", "header.verdict=ok")
        text = ("header.verdict: <ok|concerns|halt|impossible>\n"
                "scope[1].id: <R-n>\n"
                "scope[0].reason: \"\"\n"
                "blocked.tried: [<command or step>]\n")
        doc, applied, problems, notes = _apply(form, text)
        check_eq("K-A5: nothing is written, nothing is counted", (applied, _paths(problems)), (0, []))
        check_eq("K-A5: the value stays and no row opened", (doc.get("header.verdict"), doc.rows("scope")), ("ok", [0]))
        check_eq("K-A5: the role is told, once per line", len(notes), 4)
    finally:
        cleanup(root)


def a_malformed_line_applies_nothing() -> None:
    """K-A6: one line that does not parse and NOT ONE line of the file is applied - and the pairs that did parse are
    still returned (the guard keeps them for the role)."""
    cases = {
        "no colon": "scope[0].id: R-1\nthis is a sentence\n",
        "path twice": "header.verdict: ok\nheader.verdict: halt\n",
        "no space after the colon": "header.verdict:ok\n",
        "a list item": "scope:\n  - id: R-1\n",
        "nested json": json.dumps({"header.verdict": {"a": 1}}),
        "json array": json.dumps(["header.verdict", "ok"]),
        "broken json": "{\"header.verdict\": ",
        "json list of maps": json.dumps({"blocked.tried": [{"a": 1}]}),
    }
    for name, text in cases.items():
        pairs, bad = H.parse_values(text)
        check(f"K-A6: {name} - a problem", len(bad) >= 1, str(bad))
    pairs, bad = H.parse_values("scope[0].id: R-1\nthis is a sentence\n")
    check_eq("K-A6: the problem carries the line number", [p.path for p in bad], ["values line 2"])
    check_eq("K-A6: the good line is still returned for the guard", [(p[0], p[2]) for p in pairs], [("scope[0].id", 1)])
    root = temp_project("qa-values-a6-")
    try:
        art = _story(root)
        form = _form(art)
        values = art / "work" / "bad.txt"
        values.write_text("scope[0].id: R-1\nthis is a sentence\n", encoding="utf-8")
        before = _sha(form)
        code, report = _hc(art, form, "--values", str(values), "--json")
        check_eq("K-A6: applied by none - the form is the same bytes", (_sha(form), report["values_applied"]),
                 (before, 0))
        check("K-A6: the refusal names the file and the line", "bad.txt line 2" in _paths(report["problems"]),
              str(report["problems"])[:300])
        sibling = H.sibling_values(form)
        sibling.write_text("scope[0].id: R-1\nthis is a sentence\n", encoding="utf-8")
        code, out = _hc(art, form, "--fix")
        check_eq("K-A6: a waiting file that does not parse is not applied and not renamed",
                 (sibling.is_file(), form.with_name(f"{form.stem}.values.applied.yaml").exists(), _doc(form).get("scope[0].id")),
                 (True, False, handoff.template(CONTRACT).get("scope[0].id")))
        check_in("K-A6: and its problem refuses the form until it is rewritten", f"{sibling.name} line 2", out)
        # accepted shapes: a BOM and CRLF
        sibling.write_bytes(b"\xef\xbb\xbfheader.verdict: ok\r\nscope[0].id: R-1  # first\r\n")
        _hc(art, form, "--fix")
        doc = _doc(form)
        check_eq("K-A6: a BOM and CRLF are accepted (and a trailing comment is a comment)",
                 (doc.get("header.verdict"), doc.get("scope[0].id")), ("ok", "R-1"))
    finally:
        cleanup(root)


def an_unknown_path_is_a_problem_beside_the_applied_ones() -> None:
    """K-A7: one wrong path used to stop `--set` with exit 2 and the rest was lost; now it is one problem in the
    common list, with the closest known path, and every other pair is applied."""
    root = temp_project("qa-values-a7-")
    try:
        art = _story(root)
        form = _form(art)
        values = art / "work" / "v.txt"
        values.write_text("header.verdict: ok\nscope[0].idd: R-1\nscope[0].reason: fine\n", encoding="utf-8")
        code, report = _hc(art, form, "--values", str(values), "--json")
        doc = _doc(form)
        check_eq("K-A7: exit 1, the two good values are in", (code, report["values_applied"], doc.get("scope[0].reason")),
                 (1, 2, "fine"))
        wrong = [p for p in report["problems"] if p["path"] == "scope[0].idd"]
        check_eq("K-A7: one problem for the wrong path", len(wrong), 1)
        check_in("K-A7: it names the closest path", "did you mean `scope[0].id`", wrong[0]["problem"])
        code, report = _hc(art, form, "--set", "nothing.here=1", "--set", "scope[0].reason=still", "--json")
        check_eq("K-A7: --set with an unknown path is exit 1, not 2, and the other --set is applied",
                 (code, _doc(form).get("scope[0].reason"), "nothing.here" in _paths(report["problems"])),
                 (1, "still", True))
        doc, applied, problems, _n = _apply(form, "claims.never_heard_of_it: true\n")
        check_eq("K-A7: a path that is in neither the spec nor the form is a problem",
                 (applied, _paths(problems)), (0, ["claims.never_heard_of_it"]))
        doc, applied, problems, _n = _apply(form, "inputs[0].path: x\nschema_version: 2\n")
        check_eq("K-A7: a path the contract writes itself is refused", _paths(problems), ["inputs[0].path", "schema_version"])
    finally:
        cleanup(root)


def values_make_the_form_touched_and_code_derived_values_do_not() -> None:
    """K-A8: `untouched` (measured after the role's words, before `--fix`) is what `story_step finish` reads; a form
    the role wrote into is touched, a form code filled for it is not."""
    root = temp_project("qa-values-a8-")
    try:
        art = _story(root)
        form = _form(art)
        code, before = _hc(art, form, "--json")
        (art / "work" / "sizing.json").write_text(json.dumps({"size": "XS"}), encoding="utf-8")
        code, report = _hc(art, form, "--fix", "--json")
        check_in("K-A8: code derives the size", "size.computed = XS (from sizing.json)", report["fixed"])
        check_eq("K-A8: and the derived field is not counted as the role's (filled does not move)",
                 report["filled"], before["filled"])
        # an S5 critic form is untouched at birth (the S2 form is not: its third `inputs_read` row is a
        # placeholder that makes the first two count - the existing rule, not this node's)
        critic = _form5(art, "S5-qa-code-critic-1")
        code, report = _hc(art, critic, "--json")
        check_eq("K-A8: a fresh critic form is untouched", report["untouched"], True)
        values = art / "work" / "v.txt"
        values.write_text("scope[0].id: test_one\n", encoding="utf-8")
        code, report = _hc(art, critic, "--values", str(values), "--json")
        check_eq("K-A8: one value of the role makes it touched", report["untouched"], False)
        second = _form5(art, "S5-qa-code-critic-2")
        H.sibling_values(second).write_text("scope[0].id: test_one\n", encoding="utf-8")
        code, report = _hc(art, second, "--json")
        check_eq("K-A8: so does a waiting file, in a read-only run", report["untouched"], False)
    finally:
        cleanup(root)


def order_is_sibling_then_values_then_set() -> None:
    """K-A9: the latest and most explicit word wins - the waiting file, then `--values`, then `--set`."""
    root = temp_project("qa-values-a9-")
    try:
        art = _story(root)
        values = art / "work" / "v.txt"
        values.write_text("scope[0].reason: from values\n", encoding="utf-8")
        results = {}
        for name, with_sibling, with_values, with_set in (("all three", True, True, True), ("no --set", True, True, False),
                                                           ("sibling only", True, False, False)):
            form = _form(art, f"S2-qa-requirements-tester-{len(results) + 1}")
            if with_sibling:
                H.sibling_values(form).write_text("scope[0].reason: from sibling\nscope[0].id: R-1\n", encoding="utf-8")
            flags = (["--values", str(values)] if with_values else []) + (["--set", "scope[0].reason=from set"]
                                                                        if with_set else [])
            _hc(art, form, "--fix", *flags)
            results[name] = (_doc(form).get("scope[0].reason"), _doc(form).get("scope[0].id"))
        check_eq("K-A9: --set is last", results["all three"], ("from set", "R-1"))
        check_eq("K-A9: --values beats the waiting file", results["no --set"], ("from values", "R-1"))
        check_eq("K-A9: the waiting file alone", results["sibling only"], ("from sibling", "R-1"))
    finally:
        cleanup(root)


def a_sibling_is_applied_once() -> None:
    """K-A10: the file is renamed `.values.applied.yaml` after the form is written, so a later word of the role
    (a `--set`, an Edit) is never overwritten by the earlier file; `.values.stale.yaml` is never read."""
    root = temp_project("qa-values-a10-")
    try:
        art = _story(root)
        form = _form(art)
        sibling = H.sibling_values(form)
        stale = form.with_name(f"{form.stem}.values.stale.yaml")
        stale.write_text("scope[0].reason: from a form long gone\n", encoding="utf-8")
        sibling.write_text("scope[0].reason: first word\nscope[0].id: R-1\n", encoding="utf-8")
        code, out = _hc(art, form, "--fix")
        applied = form.with_name(f"{form.stem}.values.applied.yaml")
        check_eq("K-A10: renamed, not deleted", (sibling.exists(), applied.is_file()), (False, True))
        check_in("K-A10: the run says so", f"applied 2 value(s) from {sibling.name}; it is now {applied.name}", out)
        check_eq("K-A10: the stale file was not applied", _doc(form).get("scope[0].reason"), "first word")
        _hc(art, form, "--set", "scope[0].reason=later word")
        _hc(art, form, "--fix")
        check_eq("K-A10: a later word survives the next --fix", _doc(form).get("scope[0].reason"), "later word")
        sibling.write_text("scope[0].reason: second file\n", encoding="utf-8")
        _hc(art, form, "--fix")
        check_eq("K-A10: a new file is applied and replaces the trace",
                 (_doc(form).get("scope[0].reason"), applied.read_text(encoding="utf-8").strip(), sibling.exists()),
                 ("second file", "scope[0].reason: second file", False))
        explicit = art / "work" / "named.txt"
        explicit.write_text("scope[0].reason: named\n", encoding="utf-8")
        _hc(art, form, "--values", str(explicit))
        check_eq("K-A10: a file named by --values is applied and never renamed", (explicit.is_file(), _doc(form).get("scope[0].reason")),
                 (True, "named"))
    finally:
        cleanup(root)


def a_read_only_check_reports_the_merged_view_and_writes_nothing() -> None:
    """K-A11: FR-45 - a run that does not write (no --fix/--set/--values) shows the form as the next writing run will,
    and touches neither the form nor the waiting file."""
    root = temp_project("qa-values-a11-")
    try:
        art = _story(root)
        form = _form(art)
        sibling = H.sibling_values(form)
        sibling.write_text("scope[0].id: R-1\n", encoding="utf-8")
        hashes = (_sha(form), _sha(sibling))
        code, report = _hc(art, form, "--json")
        check_eq("K-A11: nothing on disk changed", (_sha(form), _sha(sibling)), hashes)
        check_eq("K-A11: the report says what is pending", (report["values_applied"], report["values_pending"]),
                 (1, sibling.name))
        check_not_in("K-A11: the merged field is not reported as unfilled", "scope[0].id", _paths(report["problems"]))
        check_in("K-A11: another field of the same row is", "scope[0].state", _paths(report["problems"]))
        code, out = _hc(art, form)
        check_in("K-A11: the text run says the file waits for a writing run", f"pending values from {sibling.name} - applied by --fix", out)
        check_eq("K-A11: and still writes nothing", (_sha(form), _sha(sibling)), hashes)
    finally:
        cleanup(root)


def an_empty_values_file_changes_nothing() -> None:
    """K-A14: an empty file or one of comments is neither a green form nor a touched one."""
    root = temp_project("qa-values-a14-")
    try:
        art = _story(root)
        form = _form5(art, "S5-qa-code-critic-1")
        before = form.read_text(encoding="utf-8")
        for name, text in (("empty", ""), ("comments", "# nothing yet\n\n   \n# still nothing\n"), ("only a BOM", "﻿")):
            values = art / "work" / "v.txt"
            values.write_text(text, encoding="utf-8")
            code, report = _hc(art, form, "--values", str(values), "--json")
            check_eq(f"K-A14: {name} - the form text is the same, the form is untouched, the form is not green",
                     (form.read_text(encoding="utf-8"), report["values_applied"], report["untouched"], code),
                     (before, 0, True, 1))
        H.sibling_values(form).write_text("# nothing yet\n", encoding="utf-8")
        code, report = _hc(art, form, "--json")
        check_eq("K-A14: an empty waiting file changes nothing either", (form.read_text(encoding="utf-8"),
                                                                       report["untouched"]), (before, True))
    finally:
        cleanup(root)


def a_named_values_file_that_does_not_exist_is_exit_2() -> None:
    """K-A15: a named input is never read as an empty one."""
    root = temp_project("qa-values-a15-")
    try:
        art = _story(root)
        form = _form(art)
        before = _sha(form)
        code, out = _hc(art, form, "--fix", "--values", str(art / "work" / "no-such.txt"))
        check_eq("K-A15: exit 2 and the form is untouched", (code, _sha(form)), (2, before))
        check_in("K-A15: the message names the file", "no such values file:", out)
    finally:
        cleanup(root)


def json_keeps_its_keys() -> None:
    """K-A16: FR-14 - `--json` only adds keys: the readers (story_step, the driver) parse the old ones."""
    root = temp_project("qa-values-a16-")
    try:
        art = _story(root)
        form = _form(art)
        code, report = _hc(art, form, "--json")
        check_eq("K-A16: every old key is there", [k for k in OLD_JSON_KEYS if k not in report], [])
        check_eq("K-A16: the new keys are values_* (A1) and the skeleton (A2)", sorted(k for k in report if k not in OLD_JSON_KEYS),
                 ["values_applied", "values_notes", "values_pending", "values_skeleton"])
        check_eq("K-A16: a problem keeps its three keys and gains `kind` and `also` (A2) and `code_fills` (SC2-38)", sorted(report["problems"][0]),
                 ["also", "code_fills", "fix", "kind", "path", "problem"])
    finally:
        cleanup(root)


def a_path_a_form_in_flight_still_holds_is_written_not_refused() -> None:
    """K-A18: M-7 - the spec and the form can disagree (a form begun on an older package). Written, never refused,
    when only the form has the line; not written, with a note, when only the spec has it; refused when neither."""
    root = temp_project("qa-values-a18-")
    try:
        art = _story(root)
        form = art / "work" / "handoffs" / f"{DISPATCH}.yaml"
        form.parent.mkdir(parents=True)
        form.write_text(FIXTURE.read_text(encoding="utf-8"), encoding="utf-8")        # a form begun elsewhere, in flight
        spec = handoff.spec(CONTRACT)
        old = "claims.every_production_file_reaches_a_requirement_or_is_named_not_requirement_bearing"
        kept = "claims.every_requirement_names_its_source_and_revision"
        check("K-A18: the first key is a line only the form holds", old not in spec and old in _doc(form).nodes)
        doc, applied, problems, notes = _apply(form, f"{old}: false\n{kept}: false\n")
        check_eq("K-A18: both are written, neither is a problem", (doc.get(old), doc.get(kept), applied, _paths(problems)),
                 (False, False, 2, []))
        said = [n for n in notes if old in n]
        check_eq("K-A18: the one the contract lost comes with a note", len(said), 1)
        check_in("K-A18: that says why", "is not in `s2-tester-to-strategist` any more", said[0])
        # the same key is an ordinary field now and a form-only line once part C drops it: both worlds are right
        check_eq("K-A18: the other key has a note exactly when the contract no longer holds it",
                 len([n for n in notes if kept in n]), 0 if kept in spec else 1)
        doc, applied, problems, notes = _apply(form, "claims.never_heard_of_it: true\n")
        check_eq("K-A18: neither in the spec nor in the form - a problem", _paths(problems), ["claims.never_heard_of_it"])
        # the other world: the spec has a line the form never had
        bare = _form(art, "S2-qa-requirements-tester-2")
        doc = _doc(bare)
        doc.lines = [line for line in doc.lines if line.strip() != doc.lines[doc.nodes["size.computed"].line].strip()]
        bare.write_text(doc.text(), encoding="utf-8")
        check("K-A18: the synthetic form has no size.computed line", "size.computed" not in _doc(bare).nodes)
        doc, applied, problems, notes = _apply(bare, "size.computed: XS\n")
        check_eq("K-A18: a spec path with no line in the form is not written, and is not a problem",
                 (applied, _paths(problems), "size.computed" in doc.nodes), (0, [], False))
        check_in("K-A18: the role is told", "this form has no line for it", notes[0])
    finally:
        cleanup(root)


def an_index_on_a_list_of_values_is_refused_with_the_whole_list_hint() -> None:
    """K-A22: `blocked.tried[1]: x` is not a way to append to a list of values (a `- key: value` line must never open
    inside it): the problem says to write the whole list on one line, and that line replaces the list whole."""
    root = temp_project("qa-values-a22-")
    try:
        art = _story(root)
        form = _form(art)
        doc, applied, problems, _n = _apply(form, "blocked.tried[1]: x\n")
        check_eq("K-A22: one problem, nothing written", (_paths(problems), applied), (["blocked.tried[1]"], 0))
        check_in("K-A22: it gives the whole-list line", "blocked.tried: [", problems[0].text)
        doc, applied, problems, _n = _apply(form, "scope[1]: x\n")
        check_in("K-A22: a row index with no field says to name the field", "scope[1].<field>", problems[0].text)
        doc, applied, problems, _n = _apply(form, "blocked.tried: [one, two, three]\n")
        check_eq("K-A22: the whole list is written", ([doc.get(f"blocked.tried[{i}]") for i in range(3)], _paths(problems)),
                 (["one", "two", "three"], []))
        form.write_text(doc.text(), encoding="utf-8")
        doc, applied, problems, _n = _apply(form, "blocked.tried: [only]\n")
        check_eq("K-A22: a shorter list replaces the longer one", [p for p in doc.nodes if p.startswith("blocked.tried")],
                 ["blocked.tried[0]"])
        doc, applied, problems, _n = _apply(form, "blocked.tried: just one\n")
        check_eq("K-A22: a single word for a list is refused (write it as a list)", _paths(problems), ["blocked.tried"])
        doc, applied, problems, _n = _apply(form, "header.verdict: [ok]\n")
        check_eq("K-A22: and a list for a single value is refused", _paths(problems), ["header.verdict"])
    finally:
        cleanup(root)


def set_keeps_its_raw_meaning() -> None:
    """K-A23: `--set` is the typed text byte for byte (the placeholder included) on a line the form holds; the same
    placeholder in a values file is not written (K-A5)."""
    root = temp_project("qa-values-a23-")
    try:
        art = _story(root)
        form = _form(art)
        expected = _doc(form)
        handoff.set_value(expected, "scope[0].reason", "a: b")
        handoff.set_value(expected, "header.verdict", "<one of the above>")
        _hc(art, form, "--set", "scope[0].reason=a: b", "--set", "header.verdict=<one of the above>")
        check_eq("K-A23: the form is byte for byte what handoff.set_value writes", form.read_text(encoding="utf-8"),
                 expected.text())
        check_eq("K-A23: the placeholder is the value", _doc(form).get("header.verdict"), "<one of the above>")
        doc, applied, problems, _n = _apply(form, "header.verdict: <one of the above>\nscope[0].reason: <= 80 characters>\n")
        check_eq("K-A23: the same words in a values file are not written", (applied, doc.text()), (0, form.read_text(encoding="utf-8")))
        doc, applied, problems, _n = _apply(form, "header.verdict: <one of the above>\n", raw=True)
        check_eq("K-A23: the raw flag is the only difference", (applied, doc.get("header.verdict")), (1, "<one of the above>"))
    finally:
        cleanup(root)


def a_value_from_the_file_meets_the_ordinary_limits() -> None:
    """L3: the values path does not bypass the field's length check - AT the limit there is no problem, BEYOND it the
    ordinary length problem (with its limit as data)."""
    root = temp_project("qa-values-l3-")
    try:
        art = _story(root)
        form = _form(art)
        values = art / "work" / "v.txt"
        values.write_text("scope[0].reason: " + "x" * 80 + "\n", encoding="utf-8")
        code, report = _hc(art, form, "--values", str(values), "--json")
        check_not_in("L3: 80 characters is the limit and passes", "scope[0].reason", _paths(report["problems"]))
        values.write_text("scope[0].reason: " + "x" * 81 + "\n", encoding="utf-8")
        code, report = _hc(art, form, "--values", str(values), "--json")
        long = [p for p in report["problems"] if p["path"] == "scope[0].reason"]
        check_eq("L3: 81 is refused with the limit as data", [p.get("limit") for p in long], [80])
    finally:
        cleanup(root)


# ------------------------------------------------------------------------------------- part A2: one refusal
S4 = "s4-case-critic-to-designer"


def _form4(art: Path, dispatch: str = "S4-qa-case-critic-1") -> Path:
    """A fresh S4 case-critic form - the role has NO Bash."""
    run_script("handoff_init.py", "--task", "QA-9", "--stage", "S4", "--role", "qa-case-critic",
               "--to", "qa-case-designer", "--dispatch", dispatch, "--task-root", str(art))
    return art / "work" / "handoffs" / f"{dispatch}.yaml"


def _green_copy(art: Path, edits: dict | None = None, dispatch: str = DISPATCH) -> Path:
    """The real 13877 S2 form in a story of its own, with `edits` ({path: value}, written as typed) applied."""
    form = art / "work" / "handoffs" / f"{dispatch}.yaml"
    form.parent.mkdir(parents=True, exist_ok=True)
    text = FIXTURE.read_text(encoding="utf-8")
    if "tried_note:" not in text and "\ntried:" not in text:
        # spec t-1765 X1 B-B: the S2 form carries `tried` now; the recorded 13877 fixture predates it, so the green copy states
        # why the table is empty (the contract's own door) - without it the "green" form is not green
        text += "\ntried_note: nothing was tried, the recorded fixture form predates the table\n"
    form.write_text(text, encoding="utf-8")
    doc = _doc(form)
    for path, value in (edits or {}).items():
        assert handoff.set_value(doc, path, value), path
    form.write_text(doc.text(), encoding="utf-8")
    return form


def _skeleton_of(report) -> list:
    return report["values_skeleton"].splitlines()


def one_refusal_block_one_command() -> None:
    """K-A12: three problems are ONE block with ONE command: all three paths in the skeleton, the allowed words of
    `header.verdict` inline, and not one `fix: --set` line (the 89-process failure was a command per field)."""
    root = temp_project("qa-values-a12-")
    try:
        art = _story(root)
        form = _green_copy(art, {"header.verdict": "<one of the above>", "scope[0].reason": "x" * 81,
                                 "scope[1].state": "contradiction"})
        code, report = _hc(art, form, "--json")
        paths = _paths(report["problems"])
        check_eq("K-A12: the three problems are the only ones", sorted(paths),
                 ["header.verdict", "scope[0].reason", "scope[1].state"])
        skeleton = _skeleton_of(report)
        names = [line.partition(":")[0].strip('"') for line in skeleton]
        check_eq("K-A12: the skeleton has a line for each of the three, in the order of the problems", sorted(names), sorted(paths))
        verdict = next(line for line in skeleton if line.startswith("header.verdict:"))
        check_eq("K-A12: the allowed words of header.verdict are inline",
                 [w for w in handoff.allowed("header_verdicts") if w in verdict], handoff.allowed("header_verdicts"))
        code, text = _hc(art, form)
        check_eq("K-A12: the text refusal exits 1", code, 1)
        check_eq("K-A12: ONE command in the block", text.count("--values -"), 1)
        check_eq("K-A12: and ONE heredoc", text.count("<<'EOF'"), 1)
        check_not_in("K-A12: no per-field `fix:` line", "\n      fix: ", text)
        check_not_in("K-A12: no per-field `--set` command", "--set", text)
        check_not_in("K-A12: no 'each fix below' preamble", "each fix below", text)
        check_in("K-A12: the skeleton is in the text verbatim", report["values_skeleton"], text)
        check_eq("K-A12: --json says nothing of the skeleton when the form is green",
                 _hc(art, _green_copy(art, None, "S2-green"), "--json")[1]["values_skeleton"], "")
        # nothing is cut: a long list of paths is printed whole, AT and BEYOND any count a person would pick
        for count in (1, 100, 101, 250):
            problems = [H.Problem(f"scope[{i}].id", "x") for i in range(count)]
            lines = H.values_skeleton(problems, CONTRACT, "qa-requirements-tester").splitlines()
            check_eq(f"K-A12: {count} paths give {count} lines, the last one whole", (len(lines), lines[-1].partition(":")[0]),
                     (count, f'"scope[{count - 1}].id"'))
    finally:
        cleanup(root)


def a_role_with_bash_is_shown_the_heredoc_and_the_file_door() -> None:
    """K-A12b: a heredoc is bash only, so the file door is ALWAYS beside it (any shell, or none)."""
    root = temp_project("qa-values-a12b-")
    try:
        art = _story(root)
        form = _green_copy(art, {"header.verdict": "<one of the above>"})
        code, text = _hc(art, form)
        sibling = H.sibling_values(form).as_posix()
        check_in("K-A12b: the heredoc command", "handoff_check.py\" --file", text)
        check_in("K-A12b: --fix --values - <<'EOF'", "--fix --values - <<'EOF'", text)
        check_in("K-A12b: the file door follows, in any shell or none",
                 f"or, in any shell or none: Write the same lines to {sibling} in one Write", text)
        check_in("K-A12b: the way out for what cannot be filled is the conductor's door", "handoff_help.py --file", text)
        check_not_in("K-A12b: and it is not the no-Bash role's sentence", "story_step finish applies them", text)
        check_not_in("K-A12b: no 'Rewrite' door while nothing was kept", "Rewrite", text)
    finally:
        cleanup(root)


def a_role_without_bash_is_shown_the_file_door_only() -> None:
    """K-A13: no command a role without Bash cannot run (FR-2): the file door, the skeleton, and `blocked` in the same file."""
    root = temp_project("qa-values-a13-")
    try:
        art = _story(root)
        form = _form4(art)
        code, text = _hc(art, form)
        check_eq("K-A13: a fresh S4 form is refused", code, 1)
        check_in("K-A13: the file door names the file", f"Write these lines to {H.sibling_values(form).as_posix()} in one Write; "
                 "story_step finish applies them", text)
        for banned in ("<<'EOF'", "--values -", "python \"", "handoff_help.py", "--set", "\n      fix: "):
            check_not_in(f"K-A13: no {banned!r} for a role without Bash", banned, text)
        check_in("K-A13: blocked is filled in the same values file", "fill blocked.field and blocked.problem in the same values file", text)
        report = _hc(art, form, "--json")[1]
        check_in("K-A13: the skeleton lines are in the text", report["values_skeleton"], text)
        # a role not named, or with no readable file, is shown both doors
        problems = [H.Problem("header.verdict", "x")]
        for role in ("", "qa-no-such-role"):
            both = H.refusal_text(form, S4, problems, role)
            check_in(f"K-A13: role {role!r} gets the command", "<<'EOF'", both)
            check_in(f"K-A13: role {role!r} gets the no-Bash sentence", "fill blocked.field and blocked.problem", both)
            check_in(f"K-A13: role {role!r} gets the conductor's door", "handoff_help.py", both)
    finally:
        cleanup(root)


class _NoJudge:
    asked = 0

    @staticmethod
    def active():
        return True

    @staticmethod
    def ask(*_a, **_k):
        _NoJudge.asked += 1
        raise AssertionError("the judge must never be asked by values_report")


def _tree_hashes(root: Path) -> dict:
    return {str(p.relative_to(root)): _sha(p) for p in sorted(root.rglob("*")) if p.is_file()}


def values_report_writes_nothing_and_never_asks_the_judge() -> None:
    """K-A17: the guard's question is PURE (FR-45) and costs no judge call: a word the judge would map is a problem."""
    root = temp_project("qa-values-a17-")
    try:
        art = _story(root)
        form = _green_copy(art)
        before = _tree_hashes(root)
        saved = H.judge
        H.judge = _NoJudge
        try:
            problems, role, kept = H.values_report(form, "header.verdict: contradiction\nscope[0].reason: fine\n")[:3]
        finally:
            H.judge = saved
        check_eq("K-A17: the judge was not asked", _NoJudge.asked, 0)
        check_eq("K-A17: the word outside the list is a problem, the good line is kept",
                 (_paths(problems), kept, role), (["header.verdict"], ["scope[0].reason: fine"], "qa-requirements-tester"))
        check_eq("K-A17: no file of the story changed, none was added", _tree_hashes(root), before)
        green = H.values_report(form, "scope[0].reason: fine\nheader.verdict: concerns\n")
        check_eq("K-A17: a green text has no problems, and all its lines are kept in the order they were applied (path order)",
                 (green[0], green[2]), ([], ["header.verdict: concerns", "scope[0].reason: fine"]))
    finally:
        cleanup(root)


def a_refused_values_text_keeps_its_good_lines_in_the_skeleton() -> None:
    """K-A19: M-4 - the guard refuses a text and the role REWRITES the file whole: its good lines must come back."""
    root = temp_project("qa-values-a19-")
    try:
        art = _story(root)
        form = _green_copy(art)
        good = ["scope[0].reason: first reason", "scope[1].reason: second reason", "scope[2].reason: third reason",
                "header.window: TP1-13877"]
        text = "\n".join(good[:2] + ["header.verdict: contradiction"] + good[2:]) + "\n"
        problems, role, kept = H.values_report(form, text)[:3]
        check_eq("K-A19: exactly the four good lines are kept, verbatim; the fifth is not", sorted(kept), sorted(good))
        refused = H.refusal_text(form, CONTRACT, problems, role, kept=kept)
        for line in good:
            check_in(f"K-A19: the good line `{line}` is in the refusal", "\n" + line + "\n", refused)
        verdict = handoff.allowed("header_verdicts")
        check_in("K-A19: and the fifth is a placeholder line with the allowed words", "header.verdict: <" + "|".join(verdict) + ">", refused)
        check_not_in("K-A19: the wrong word is not echoed back as a value", "header.verdict: contradiction", refused)
        check_in("K-A19: the door says to rewrite the file whole", "Rewrite", refused)
        check_in("K-A19: yours first, then the ones to fix", "yours that passed first, then the ones to fix", refused)
        skeleton = H.values_skeleton(problems, CONTRACT, role, kept=kept).splitlines()
        check_eq("K-A19: kept lines come before the lines to fix", skeleton[-1].startswith("header.verdict:"), True)
        # a text that does not PARSE: nothing is applied, every line that did parse is kept
        broken = "scope[0].reason: first\nthis line has no colon\nscope[1].reason: second\n"
        problems, role, kept = H.values_report(form, broken)[:3]
        check_eq("K-A19: a parse problem keeps the parsed lines", (kept, len(problems)),
                 (["scope[0].reason: first", "scope[1].reason: second"], 1))
        refused = H.refusal_text(form, CONTRACT, problems, role, kept=kept)
        check_in("K-A19: and gives them back", "\nscope[1].reason: second\n", refused)
        # no Bash: the file door says the lines are BELOW
        crit = H.refusal_text(art / "work" / "handoffs" / "x.yaml", S4, [H.Problem("header.verdict", "bad")],
                              "qa-case-critic", kept=["header.window: A, B"])
        check_in("K-A19: a role without Bash is told to rewrite the file whole with the lines below",
                 "Rewrite " + (art / "work" / "handoffs" / "x.values.yaml").as_posix() + " WHOLE with the lines below: "
                 "yours that passed first, then the ones to fix", crit)
        check("K-A19: its kept line stands before the line to fix",
              crit.index("header.window: A, B") < crit.index("header.verdict: <"))
        # the CLI: a values FILE with a bad line is refused with the good lines given back
        values = art / "work" / "v.txt"
        values.write_text(broken, encoding="utf-8")
        code, out = _hc(art, form, "--values", str(values))
        check_eq("K-A19: the CLI refuses it", code, 1)
        check_in("K-A19: and gives the good lines back", "\nscope[0].reason: first\nscope[1].reason: second\n", out)
        code, out = _hc_stdin(art, form, broken, "--values", "-")
        check_in("K-A19: the same through stdin", "\nscope[1].reason: second\n", out)
    finally:
        cleanup(root)


def a_blank_field_code_fills_is_not_refused_by_values_report() -> None:
    """K-A20: M-9 - the guard must not demand what only `--fix` can produce (FR-11): `review.findings_file` is derived
    from the findings file on disk, which a role without Bash cannot make a deriver find; `finish` checks it."""
    root = temp_project("qa-values-a20-")
    try:
        art = _story(root)
        form = _form4(art)
        doc = _doc(form)
        handoff.set_value(doc, "review.findings_file", "<fill>")
        form.write_text(doc.text(), encoding="utf-8")
        control = H.check(_doc(form), S4, H.Artifacts(art, dispatch=form.stem), fix=True, use_judge=False)[2]
        check_in("K-A20: the control - the same form IS refused for it by check(fix=True)",
                 "review.findings_file", _paths([p for p in control if p.kind == "blank"]))
        problems, role, kept = H.values_report(form, "header.verdict: ok\n")[:3]
        check_not_in("K-A20: values_report does not name it", "review.findings_file", _paths(problems))
        check_in("K-A20: but a blank field code does NOT fill still is a problem", "review.outcome", _paths(problems))
        check_eq("K-A20: and the good line is kept", kept, ["header.verdict: ok"])
        # the one answer
        yes = ["review.findings_file", "scope[3].case_version", "artifacts.tests[0]", "artifacts.tests[2]", "size.computed",
               "rounds[1].verify.witness", "claims." + next(iter(H.CLAIMS))]
        no = ["header.verdict", "scope[0].reason", "claims.never_heard_of_it", "artifacts.tests_other", "scope[0].id"]
        check_eq("K-A20: _code_fills says yes for what a deriver, a list deriver, a leaf or a verifier fills",
                 [H._code_fills(p) for p in yes], [True] * len(yes))
        check_eq("K-A20: and no for what only the role knows", [H._code_fills(p) for p in no], [False] * len(no))
        check("K-A20: a Problem says its kind structurally: 'not filled' is blank, a wrong word is not",
              {p.path: p.kind for p in control if p.path in ("review.findings_file", "review.outcome")}
              == {"review.findings_file": "blank", "review.outcome": "blank"}
              and H.Problem("a", "b").kind == "" and H.Problem("a", "b").also == ())
    finally:
        cleanup(root)


def a_blocked_row_puts_blocked_problem_into_the_skeleton() -> None:
    """K-A21: m-1 - the problem is on `scope[0].state`, its door is `blocked.problem`: the skeleton shows both paths."""
    root = temp_project("qa-values-a21-")
    try:
        art = _story(root)
        form = _green_copy(art, {"scope[0].state": "blocked"})
        code, report = _hc(art, form, "--json")
        row = [p for p in report["problems"] if p["path"] == "scope[0].state"]
        check_eq("K-A21: the blocked row is refused, and names its other door as data", [p["also"] for p in row], [["blocked.problem"]])
        names = [line.partition(":")[0] for line in _skeleton_of(report)]
        check_eq("K-A21: the skeleton has a line for the row AND for blocked.problem", (names.count("scope[0].state") + names.count('"scope[0].state"'),
                                                                                           names.count("blocked.problem")), (1, 1))
        problems, role, kept = H.values_report(form, "header.verdict: ok\n")[:3]
        check("K-A21: values_report keeps the same door (the guard shows it)", ("blocked.problem",) in [p.also for p in problems])
        check_in("K-A21: blocked.problem: in the refusal text", "\nblocked.problem: <", _hc(art, form)[1])
    finally:
        cleanup(root)


def a_skeleton_is_blank_for_every_field_of_every_contract() -> None:
    """A skeleton left unfilled must write NOTHING (FR-59: the line names what the role must supply, it does not
    invent a value): for every field of every contract, the placeholder line reads back as blank through the values
    parser, a list of values is one line `path: [<...>]`, and a list section expands to its first row."""
    contracts = [str(row.get("contract")) for row in handoff.index().get("handoffs", []) if row.get("contract")]
    bad, total = [], 0
    # `values_skeleton` reads the contract file again on every call; with one call per field that was ~57 s of file reads
    # (FR-31, t-1783). The schema is read-only here, so it is read once per contract for the whole loop.
    real_spec, memo = handoff.spec, {}
    handoff.spec = lambda cid: memo[cid] if cid in memo else memo.setdefault(cid, real_spec(cid))
    try:
        for contract in sorted(set(contracts)):
            spec = handoff.spec(contract)
            for generic in spec:
                if handoff.owned_by_contract(generic):
                    continue
                path = generic.replace("[]", "[0]")
                text = H.values_skeleton([H.Problem(path, "x")], contract, "")
                pairs, problems = H.parse_values(text)
                total += 1
                if problems or len(pairs) != 1 or not H._blank_value(pairs[0][1]):
                    bad.append((contract, path, text[:80]))
    finally:
        handoff.spec = real_spec
    check_eq(f"skeleton: all {total} fields of {len(set(contracts))} contracts read back blank", bad, [])
    lines = H.values_skeleton([H.Problem("blocked.tried[0]", "x")], CONTRACT, "qa-requirements-tester")
    check_eq("skeleton: a list of values is written whole on one line", lines.startswith("blocked.tried: [<"), True)
    rows = H.values_skeleton([H.Problem("scope", "no rows")], CONTRACT, "qa-requirements-tester").splitlines()
    check_eq("skeleton: a list section with no rows gets every field of its first row",
             [line.partition(":")[0].strip('"') for line in rows],
             [path.replace("[]", "[0]") for path in handoff.spec(CONTRACT) if path.startswith("scope[].")])
    notes = H.values_skeleton([H.Problem("claims.nothing_of_the_kind", "false", "repair the work")], CONTRACT, "")
    check_eq("skeleton: a problem on no field of the contract is a comment with its fix", notes,
             "# claims.nothing_of_the_kind: repair the work")
    again = H.values_skeleton([H.Problem("header.verdict", "x"), H.Problem("header.verdict", "y")], CONTRACT, "",
                              kept=["header.verdict: ok"])
    check_eq("skeleton: a path of kept is not repeated, nor a path of two problems", again, "header.verdict: ok")


def the_skeleton_cuts_nothing() -> None:
    """L2/L4: no limit is introduced - a closed list of 2000 words and a hint of 5000 characters are printed whole,
    and still read back blank."""
    words = [f"w{i:04d}" for i in range(2000)]
    spec = {"scope[].state": handoff.FieldSpec("scope[].state", [], False, 0, "text", "h" * 5000),
            "header.verdict": handoff.FieldSpec("header.verdict", [], False, 0, "text", "h" * 5000)}
    real_spec, real_options = handoff.spec, handoff.options_for_role
    handoff.spec = lambda _contract: spec
    handoff.options_for_role = lambda field, role, vocab=None: words if field.path.endswith(".state") else field.options
    try:
        text = H.values_skeleton([H.Problem("scope[0].state", "x"), H.Problem("header.verdict", "y")], CONTRACT, "r")
    finally:
        handoff.spec, handoff.options_for_role = real_spec, real_options
    state, verdict = text.splitlines()
    check_eq("cuts nothing: 2000 words in one line, all of them", all(w in state for w in words), True)
    check_eq("cuts nothing: a 5000-character hint is whole", verdict, "header.verdict: <" + "h" * 5000 + ">")
    check_eq("cuts nothing: both lines read back blank", [H._blank_value(v) for _p, v, _n, _r in H.parse_values(text)[0]], [True, True])


def a_skeleton_left_as_is_writes_nothing() -> None:
    """The refusal's own command, run as printed with no value filled, changes nothing and refuses again with the
    same problems - the placeholder never becomes a value."""
    root = temp_project("qa-values-a2-asis-")
    try:
        art = _story(root)
        form = _form4(art)
        report = _hc(art, form, "--json")[1]
        before = form.read_text(encoding="utf-8")
        code, out = _hc_stdin(art, form, report["values_skeleton"] + "\n", "--values", "-", "--json")
        again = json.loads(out)
        check_eq("as is: nothing applied", again["values_applied"], 0)
        check_eq("as is: the same problems", _paths(again["problems"]), _paths(report["problems"]))
        check_eq("as is: the form is what it was", form.read_text(encoding="utf-8"), before)
    finally:
        cleanup(root)


# ----------------------------------------------------------------------- HF8-7: the refusal names the indexed row form
S4C = "s4-case-critic-to-designer"        # the critic of round 2 of run 12586 met this contract
S4R = "s4-designer-to-runner"
GATE_A = "gate-a-to-automator"


def _problems(text: str, contract: str = S4C) -> list:
    return H.parse_values(text, contract=contract)[1]


def _skeleton(problems, contract: str = S4C, role: str = "qa-case-critic", kept=()) -> str:
    return H.values_skeleton(problems, contract, role, kept=kept)


def a_dotted_index_is_refused_with_the_indexed_row_form() -> None:
    """K1: the line the critic of round 2 wrote, `scope.0.id: TC-1`, is refused as before, and the text now names the form
    the writer takes - `"scope[0].id"` - on the contract's own list; the skeleton has the lines to fill. Protects AR-9, AR-10."""
    problems = _problems("scope.0.id: TC-1\nscope.0.state: approve\n")
    check_eq("K1: two problems, one per line", [p.path for p in problems], ["values line 1", "values line 2"])
    check_in("K1: line 1 names scope[0].id", '"scope[0].id"', problems[0].text)
    check_in("K1: line 2 names scope[0].state", '"scope[0].state"', problems[1].text)
    check_in("K1: the old part of the text stays", "is not a `path: value` line", problems[0].text)
    block = H.refusal_text("work/handoffs/S4-qa-case-critic-1.yaml", S4C, problems, "qa-case-critic")
    check_in("K1: the refusal block carries the indexed form", '"scope[0].id"', block)
    check_in("K1: and the skeleton the line of the finding", '"scope[0].state": <', _skeleton(problems))
    live = H._apply_text(handoff.template(S4C), S4C, "values", lambda: b"scope.0.id: x")[2][0].text   # the live path (M14)
    check_in("K1: the live path (--fix, --values, the waiting file) carries the contract too", '"scope[0].id"', live)


def a_list_of_objects_is_refused_with_the_first_row_lines() -> None:
    """K2: a JSON object with a list of objects, a JSON array, `scope: [{id: TC-1}]` and `findings: {id: F-1}` get the
    lines of the first row of THAT list; the field code fills (`case_version`) is not among them."""
    cases = [('{"scope": [{"id": "TC-1"}]}', "scope[0].id"), ('[{"id": "TC-1"}]', "scope[0].id"),
             ("scope: [{id: TC-1}]", "scope[0].id"), ("findings: {id: F-1}", "findings[0].id")]
    for text, want in cases:
        problems = _problems(text)
        sketch = _skeleton(problems)
        check_in(f"K2: {text!r} names {want}", f'"{want}"', problems[0].text)
        check_in(f"K2: {text!r} has the line to fill", f'"{want}": <', sketch)
        check_not_in(f"K2: {text!r}: no line for the field code fills", "case_version", sketch)
    filled = _problems("scope.0.case_version: x")[0]                # a dotted index on a field code fills (E4, FR-11)
    check_not_in("K2: a dotted code-filled field is not offered", "case_version", "".join(filled.also))
    check_not_in("K2: nor in the text as a form", '"scope[0].case_version"', filled.text)
    check_in("K2: it falls through to the rows of the list", '"scope[0].id"', filled.text)


def a_block_yaml_list_is_refused_with_the_headers_list() -> None:
    """K3: `findings:` then `- id: F-1` names `findings[0].id`; the bare `- id: x` names the first list of the contract."""
    problems = _problems("findings:\n  - id: F-1\n")
    check_eq("K3: one problem, on the item line", [p.path for p in problems], ["values line 2"])
    check_in("K3: the header's list", '"findings[0].id"', problems[0].text)
    pairs = H.parse_values("findings:\n  - id: F-1\n", contract=S4C)[0]
    check_eq("K3: the bare header stays a pair with no value (nothing is written)", [(p[0], p[1]) for p in pairs], [("findings", None)])
    check_in("K3: a bare item names the required list", '"scope[0].id"', _problems("- id: x\n")[0].text)
    two = _problems("findings:\n  - id: F-1\n    state: approve\n  - id: F-2\n    state: reject\n")
    check_eq("K3: both item lines are problems (line 5 is the repeated `state`)", [p.path for p in two][:2],
             ["values line 2", "values line 4"])
    check_in("K3: the second item still names the header's list", '"findings[0].id"', two[1].text)
    check_not_in("K3: and not the first list of the contract", "scope[0]", two[1].text)


def the_hint_never_changes_what_parse_values_decides() -> None:
    """K4: for every input of the battery the pairs and the PATHS of the problems are the same with and without the
    contract; the hint is text and `also` only, and nothing here calls `apply_values` (AR-28)."""
    saved = H.apply_values
    H.apply_values = lambda *a, **k: (_ for _ in ()).throw(AssertionError("a hint applied values"))
    try:
        for text in _battery():
            plain, with_contract = H.parse_values(text), H.parse_values(text, contract=S4C)
            check_eq(f"K4: same pairs {text[:30]!r}", with_contract[0], plain[0])
            check_eq(f"K4: same problem paths {text[:30]!r}", [p.path for p in with_contract[1]], [p.path for p in plain[1]])
    finally:
        H.apply_values = saved


def a_list_that_is_not_a_list_of_rows_gets_no_row_hint() -> None:
    """K5: `blocked.tried` is a list of values and `inputs` has nothing the role writes: no row hint, no `[0].` path."""
    for text in ("blocked.tried: [{a: 1}]", "inputs: [{path: x}]"):
        problem = _problems(text)[0]
        check_not_in(f"K5: {text!r}: the text offers no row", "a row of a list", problem.text)
        check_eq(f"K5: {text!r}: no paths", problem.also, ())
        check_not_in(f"K5: {text!r}: the skeleton offers no row", "[0].",
                     "\n".join(l for l in _skeleton([problem]).splitlines() if not l.startswith("#")))


def an_unreadable_contract_gives_the_general_text() -> None:
    """K6: a contract that does not exist gives the general form `"<list>[0].<field>"`, no exception, the same number of
    problems (E1, E2)."""
    text = "scope.0.id: TC-1\nnot a line\n"
    plain, broken = _problems(text, ""), _problems(text, "no-such-contract")
    check_eq("K6: the same number of problems", (len(plain), len(broken)), (2, 2))
    check_in("K6: the general form", '"<list>[0].<field>"', broken[0].text)
    check_eq("K6: no paths", [p.also for p in broken], [(), ()])
    nested = _problems("blocked.tried: [{a: 1}]", "")[0]                 # no readable contract: the general sentence
    check_in("K6: a nested object without a contract carries the general form", '"<list>[0].<field>"', nested.text)
    check_eq("K6: and no paths", nested.also, ())
    # t-442 (canon part D): a nested value on a path that is ALSO given by an earlier line is ONE problem - its own shape; it is
    # not read as a pair, so it is not "given twice" as well (a line is refused once, for what is wrong with it)
    for contract in ("", S4C):
        once = _problems("blocked.tried: x\nblocked.tried: [{a: 1}]\n", contract)
        check_eq(f"K4 (t-442) [{contract or 'no contract'}] a repeated path with a nested value: exactly one problem",
                 [p.path for p in once], ["values line 2"])
        check_in(f"K4 (t-442) [{contract or 'no contract'}] ... it is the nested shape", "not a nested object", once[0].text)
        check_not_in(f"K4 (t-442) [{contract or 'no contract'}] ... and not 'given twice'", "given twice", once[0].text)
    twice = _problems("blocked.tried: x\nblocked.tried: y\n", "")
    check_eq("K4 (t-442) control: the same path twice with flat values IS 'given twice', once, naming both lines",
             [(p.path, "`blocked.tried` is given twice (lines 1 and 2)" in p.text) for p in twice], [("values line 2", True)])


def the_contract_is_read_once_and_only_when_a_line_is_bad() -> None:
    """K7: a clean text and an empty one never read the contract; a thousand bad lines read it once (AR-12, E5, E6, E8)."""
    real, calls = handoff.spec, []
    handoff.spec = lambda contract: calls.append(contract) or real(contract)
    try:
        H.parse_values("header.window: TC-1\nheader.verdict: ok\n", contract=S4C)
        H.parse_values("", contract=S4C)
        H.parse_values("# only a comment\n\n", contract=S4C)
        check_eq("K7: no bad line, no read", calls, [])
        H.parse_values("scope.0.id: x\n" * 1000, contract=S4C)
        check_eq("K7: a thousand bad lines, one read", len(calls), 1)
    finally:
        handoff.spec = real


def _scalar_paths(contract: str) -> list:
    return [p for p in H.row_form(handoff.spec(contract))[1] if not p.endswith("]")]


def the_row_form_of_every_contract_is_a_path_the_writer_takes() -> None:
    """K8: the door. For every contract of `handoffs/index.yaml` (and the escalation one) that has a list of rows, the
    first path the hint names is written by `apply_values` with a real value - one applied, no problem - and is neither
    the contract's own nor code's. A spec with no list of rows gives nothing (AR-1, AR-2, FR-2)."""
    index = handoff.index()
    contracts = [str(row["contract"]) for row in index.get("handoffs", [])] + [str(index["escalation"]["contract"])]
    seen = 0
    for contract in contracts:
        spec = handoff.spec(contract)
        name, paths = H.row_form(spec)
        if not paths:
            continue
        seen += 1
        first, later = H.row_pair(paths)
        check(f"K8 {contract}: a scalar path to show", bool(first) and bool(later) and first != later, f"{paths}")
        check(f"K8 {contract}: nothing owned by the contract or filled by code",
              not any(handoff.owned_by_contract(p) or H._code_fills(p) for p in paths), f"{paths}")
        doc, applied, problems, _notes = H.apply_values(handoff.template(contract), contract, [(first, "word", 1, "")])
        check_eq(f"K8 {contract}: `{first}` is written", (applied, [p.path for p in problems]), (1, []))
    check("K8: the contracts with a list of rows were really walked", seen >= 5, f"{seen}")
    check_eq("K8: a spec with no list of rows shows nothing", H.row_form({"header.verdict": None}), ("", []))
    check_eq("K8: and the sentence is the general one", H._row_sentence([]).count('"<list>[0].<field>"'), 1)
    check_eq("K8: gate A names its own list, not `scope`", H.row_form(handoff.spec(GATE_A))[0],
             "environment.preconditions_accepted_as_blocked")


def a_section_skeleton_writes_a_list_of_values_whole() -> None:
    """K9: a problem on the section `execution` of the runner contract gets `execution[0].preconditions: [<...>]` - the
    line the writer takes - and never `execution[0].preconditions[0]`, which `_apply_one` refuses; the filled lines
    apply without a problem. A field code fills is left out (M-9)."""
    sketch = _skeleton([H.Problem("execution", "no rows", "fix")], S4R, "qa-case-designer")
    check_in("K9: the list of values is one line", '"execution[0].preconditions": [<', sketch)
    check_not_in("K9: no index on the list of values", "preconditions[0]", sketch)
    filled = "\n".join(line.split(": ", 1)[0] + ": word" for line in sketch.splitlines() if not line.startswith("#"))
    filled = filled.replace('preconditions": word', 'preconditions": [word]').replace('data_and_accounts": word',
                                                                                    'data_and_accounts": [word]')
    pairs, bad = H.parse_values(filled)
    check_eq("K9: the filled skeleton parses", bad, [])
    _doc2, applied, problems, _n = H.apply_values(handoff.template(S4R), S4R, pairs)
    check_eq("K9: and applies with no problem", [p.path for p in problems], [])
    sections = _skeleton([H.Problem("scope", "no rows", "fix")], S4R, "qa-case-designer")
    check_not_in("K9: a field code fills is not in the section skeleton", "case_version", sections)
    _d3, got, bad, _n3 = H.apply_values(handoff.template(S4R), S4R, [("execution[0].precondition", "w", 1, "")])
    check_eq("K9: a near miss on a list of values is refused", (got, len(bad)), (0, 1))
    check_not_in("K9: `_near` does not teach the indexed leaf the writer refuses", "preconditions[0]", bad[0].text + bad[0].fix)
    check_in("K9: it names the whole list", "execution[0].preconditions", bad[0].fix)


def the_guard_block_carries_the_row_form_and_the_role_line_once() -> None:
    """K10: the text the pre-tool guard prints is `refusal_text` over `values_report`: with the contract passed in, a
    file with `scope[0].state: approve` and `scope.1.id: TC-2` is refused with `"scope[1].id"`, and the role's own line
    comes first and once."""
    root = temp_project("qa-values-hf87-")
    try:
        art = _story(root)
        form = _form4(art)
        problems, role, kept = H.values_report(form, "scope[0].state: approve\nscope.1.id: TC-2\n")[:3]
        check_in("K10: the problem names scope[1].id", '"scope[1].id"', problems[0].text)
        block = H.refusal_text(form, S4C, problems, role, kept=kept)
        check_in("K10: the block names scope[1].id", '"scope[1].id": <', block)
        check_eq("K10: the role's line is kept", kept, ["scope[0].state: approve"])
        check_eq("K10: and appears once", block.count("\nscope[0].state: approve\n"), 1)
        check_eq("K10: first among the lines", _skeleton(problems, kept=kept).splitlines()[0], "scope[0].state: approve")
    finally:
        cleanup(root)


def _old_door(form: Path, text: str) -> bool:
    """A COPY of the guard's own algorithm before SC2-13 (the second parse and the second read of the form): the door
    is open when the text parses and the form with every pair applied holds a filled `blocked.problem`. It is the
    control `blocked_said` is held to; it is not production code."""
    doc = handoff.parse(form.read_text(encoding="utf-8-sig", errors="replace"))
    contract = str(doc.get("contract") or "")
    pairs, unreadable = H.parse_values(text)
    if unreadable:
        return False
    merged = H.apply_values(doc, contract, pairs)[0]
    return not handoff.is_placeholder(merged.get("blocked.problem"))


def _with_blocked_problem(form: Path, word: str = "the findings file cannot be read: permission denied") -> Path:
    doc = _doc(form)
    assert handoff.set_value(doc, "blocked.problem", word)
    form.write_text(doc.text(), encoding="utf-8")
    return form


def blocked_said_is_the_old_guards_door_on_every_input() -> None:
    """K1/K4/K8 (SC2-13, AR-13, AR-28): `values_report.blocked_said` is the answer the guard used to compute with a
    second parse and a second read of the form; on every edge it is equal to a copy of that algorithm. A text that does
    not parse opens no door, whatever the form on disk says (E1); a placeholder is no word (E2, FR-59); a list is no word
    (E4); a form that already said it keeps its door (E3). The contract and the role are the ones the form names (K8)."""
    root = temp_project("qa-values-sc213-")
    try:
        art = _story(root)
        plain = _form4(art, "S4-qa-case-critic-1")
        said = _with_blocked_problem(_form4(art, "S4-qa-case-critic-2"))
        word = "blocked.field: review.outcome\nblocked.problem: the findings file cannot be read\n"
        bad = "header.verdict: contradiction\n"
        cases = {
            "E0 a word and a door": (plain, bad + word, True),
            "E0b a door and nothing wrong": (plain, word, True),
            "E1 unparseable text, form already said": (said, bad + "this line has no colon\n", False),
            "E1b unparseable text with the door in it": (plain, bad + word + "this line has no colon\n", False),
            "E2 template placeholder": (plain, bad + "blocked.problem: <what the role tried and what refused it, verbatim>\n", False),
            "E2b empty quotes": (plain, bad + 'blocked.problem: ""\n', False),
            "E2c <fill>": (plain, bad + "blocked.problem: <fill>\n", False),
            "E3 form already said, text has a bad word and no door": (said, bad, True),
            "E4 a list is not a word": (plain, bad + "blocked.problem: [a]\n", False),
            "E7 empty file": (plain, "", False),
            "E7b comments only": (said, "# only\n# comments\n", True),
            "E7c comments only, nothing said": (plain, "# only\n", False),
            "order: row 10 before row 2": (plain, "scope[10].reason: x\nscope[2].reason: y\n" + word, True),
        }
        for shown, (form, text, expected) in cases.items():
            report = H.values_report(form, text)
            check_eq(f"K1: {shown}: blocked_said", report.blocked_said, expected)
            check_eq(f"K1: {shown}: equal to the old guard's algorithm", report.blocked_said, _old_door(form, text))
        report = H.values_report(said, bad + "this line has no colon\n")
        check_eq("K4: a text that does not parse opens no door although the form on disk has one", report.blocked_said, False)
        check("K4: and the parse problem is what comes back", len(report.problems) == 1, str(report.problems))
        doc = _doc(plain)
        report = H.values_report(plain, bad)
        check_eq("K8: the contract is the form's own", report.contract, str(doc.get("contract")))
        check_eq("K8: the role is the form's own", report.role, str(doc.get("header.role")))
        check_eq("K8: the answer is a ValuesReport of five", (type(report).__name__, len(report)), ("ValuesReport", 5))
        check_eq("K8: the unparsed branch carries them too", (H.values_report(plain, "no colon").contract,
                                                              H.values_report(plain, "no colon").role), (report.contract, report.role))
    finally:
        cleanup(root)


def a_contract_without_the_door_field_has_no_door() -> None:
    """K6 (E5): a contract that names no `blocked.problem` field has no door: `blocked_said` is False and equals the old
    algorithm; the refusal keeps its general text (the guard refuses)."""
    root = temp_project("qa-values-sc213-e5-")
    try:
        art = _story(root)
        form = _form4(art)
        real = handoff.spec

        def without_door(contract):
            return {path: node for path, node in real(contract).items() if not path.startswith("blocked.")}

        text = "header.verdict: contradiction\nblocked.problem: the findings file cannot be read\n"
        handoff.spec = without_door
        try:
            kept_form = (H.values_report(form, text).blocked_said, _old_door(form, text))
            # a form of that contract has no `blocked:` section either: strip it, as an older form would lack it
            lines, skipping, stripped = form.read_text(encoding="utf-8").splitlines(), False, []
            for line in lines:
                if line.startswith("blocked:"):
                    skipping = True
                    continue
                if skipping and line[:1] in (" ", "\t", ""):
                    continue
                skipping = False
                stripped.append(line)
            form.write_text("\n".join(stripped) + "\n", encoding="utf-8")
            check_not_in("K6: the control - the stripped form holds no blocked.problem", "blocked.problem", form.read_text(encoding="utf-8"))
            report = H.values_report(form, text)
            old = _old_door(form, text)
        finally:
            handoff.spec = real
        check_eq("K6: no field in the contract and none in the form: no door", report.blocked_said, False)
        check_eq("K6: and the old algorithm said the same", old, False)
        check_eq("K6: a form that still holds the path is written with a note, as before: new equals old", kept_form[0], kept_form[1])
    finally:
        cleanup(root)


def a_derivation_of_fix_opens_no_door() -> None:
    """K7: `blocked_said` is read BEFORE `check(fix=True)`: a `check` that fills `blocked.problem` itself is not the role
    speaking, and the door stays shut (the position's invariant: the role's word opens it, code's derivation does not)."""
    root = temp_project("qa-values-sc213-k7-")
    try:
        art = _story(root)
        form = _form4(art)
        real = H.check

        def filling(doc, contract, art_, **kw):
            done = real(doc, contract, art_, **kw)
            handoff.set_value(done[0], "blocked.problem", "filled by the fix, not by the role")
            filled = handoff.parse(done[0].text())            # `set_value` writes the text; the reader sees a parsed document
            check_eq("K7: the control - the document `check` returns carries the filled door",
                     filled.get("blocked.problem"), "filled by the fix, not by the role")
            return (filled,) + tuple(done[1:])

        H.check = filling
        try:
            report = H.values_report(form, "header.verdict: contradiction\n")
        finally:
            H.check = real
        check_eq("K7: a derivation inside check(fix=True) opens no door", report.blocked_said, False)
        check("K7: and the problems are still returned", bool(report.problems))
    finally:
        cleanup(root)


def an_empty_list_and_a_flat_list_of_rows_are_taught_the_index() -> None:
    """K11: `scope: [a, b]` parses and the writer refuses it with `_near` while the skeleton unfolds the rows (E17, a pin);
    the fresh form with no rows says `no rows` and the indexed form."""
    pairs, bad = H.parse_values("scope: [a, b]", contract=S4C)
    check_eq("K11: the flat list parses", (len(pairs), bad), (1, []))
    _doc3, applied, problems, _n = H.apply_values(handoff.template(S4C), S4C, pairs)
    check_eq("K11: the writer refuses it", (applied, [p.path for p in problems]), (0, ["scope"]))
    check_in("K11: and the skeleton unfolds the rows", '"scope[0].id": <', _skeleton(problems))
    template = handoff.template(S4C).text()
    import re
    emptied = re.sub(r"(?ms)^scope:.*?(?=^\S)", "scope: []\n", template)
    doc = handoff.parse(emptied)
    problem = [p for p in H.check(doc, S4C, H.Artifacts(Path("."), dispatch="x"), fix=False, use_judge=False)[2]
               if p.path == "scope"]
    check("K11: the fresh form without rows is refused on scope", bool(problem), "")
    if problem:
        check_in("K11: `no rows` stays", "no rows", problem[0].text)
        check_in("K11: and it carries the indexed form", '"scope[0].id"', problem[0].text)


# r0107 t-439: the depth of the CLOSED deep scalar (`scope: [[[...]]]`). `handoff._scalar` cost ~44 s at 200000 on a
# box where 20000 costs ~3.3 s (the same on the base commit 8ce4ef3f, so the time is the input's size, not a release's
# slowdown); the guard under test (`except RecursionError` in `parse_values`) is live from the interpreter's own limit
# up (2000 levels already raise it, measured), so the depth is 20 times that limit, never a fixed number below it.
# The OPEN deep inputs (`"[" * 200000`, no closers) cost ~0.02 s and keep their size.
CLOSED_DEPTH = 20 * sys.getrecursionlimit()


def _battery() -> list:
    cyr, arabic = chr(0x438) + chr(0x434), chr(0x663)        # by code point: the package carries no Cyrillic (FR-30)
    return ["scope.0.id: x", "x" * 60 + " no colon", "x" * 61 + " no colon", "scope.99999.id: x", "scope.01.id: x",
            f"scope.{arabic}.id: x", "scope.0", "scope.0: {id: x}", "blocked.tried.0: x", "Scope.0.id: x",
            "scope: {\"id\": \"x\"}", "scope[0]: {id: x}", "inputs: [{path: x}]", "contract: x.0.y",
            "".join(f"bad line {n}\n" for n in range(2000)),
            "[" * 100 + "]" * 100, "[" * 200000, "scope: " + "[" * 200000, "scope: " + "[" * 100,
            "scope: " + "[" * CLOSED_DEPTH + "]" * CLOSED_DEPTH,
            "﻿scope.0.id: x\r\nscope.0.state: y\r\n", f"scope[0].{cyr}: x", "", "# only\n# comments\n",
            '{"scope": [{"id": "x"}]}', '{"scope.0.id": "x"}', '{"a": 1, "a": 2}', "{not json}",
            "scope[0].id: ok\nscope.1.id: x\n", "scope: [a, b]", "scope: x"]


def the_battery_never_raises_and_the_hint_names_only_real_paths() -> None:
    """K12: magnitude, nesting, encoding, empty and broken input (E7-E16): no exception; a path the hint names in `also`
    is a path of the contract the writer knows; the echo cuts at 60 as before; a deep file is an ordinary refusal."""
    s4_spec = handoff.spec(S4C)     # read once: the per-path `handoff.spec(S4C)` re-parsed the contract file tens of thousands of times (FR-31, t-1783)
    for text in _battery():
        try:
            pairs, problems = H.parse_values(text, contract=S4C)
        except Exception as exc:                                  # the failure is the test's finding, not a crash
            check(f"K12: no exception {text[:30]!r}", False, repr(exc))
            continue
        for problem in problems:
            for path in problem.also:
                generic = H.INDEXED.sub("[]", path)
                check(f"K12: {path} is a field of the contract", generic in s4_spec
                      and not handoff.owned_by_contract(path), path)
    two = {n: _problems(("x" * n) + " no colon")[0].text for n in (60, 61)}
    check_in("K12: 60 characters are shown whole", "x" * 60, two[60])
    check_not_in("K12: 61 are cut at 60 as before", "x" * 61, two[61])
    check_in("K12: an index past the rows is named, the writer refuses it", '"scope[99999].id"', _problems("scope.99999.id: x")[0].text)
    _d, applied, problems, _n = H.apply_values(handoff.template(S4C), S4C, [("scope[99999].id", "x", 1, "")])
    check_eq("K12: and opens nothing", applied, 0)
    check_in("K12: `the next row`", "the next row is", problems[0].text)
    check_in("K12: 01 reads as 1", '"scope[1].id"', _problems("scope.01.id: x")[0].text)
    check_not_in("K12: a non-ASCII digit is no index", '"scope[3].id"', _problems(f"scope.{chr(0x663)}.id: x")[0].text)
    check_not_in("K12: `scope.0` is no path of a row", 'scope[0]": <', _problems("scope.0")[0].text)
    check_not_in("K12: nor is a list of values a row", "blocked.tried[0].", _problems("blocked.tried.0: x")[0].text)
    check_eq("K12: a deep array is one ordinary problem", len(_problems("[" * 100 + "]" * 100)), 1)
    check_eq("K12: a too deep array is one problem too", len(_problems("[" * 200000)), 1)
    check_in("K12: with the usual text", "not valid JSON", _problems("[" * 200000)[0].text)
    deep = H.parse_values("scope: " + "[" * 200000)
    check_eq("K12: a too deep scalar is either one problem or one pair, never a crash", len(deep[0]) + len(deep[1]), 1)
    closed = H.parse_values("scope: " + "[" * CLOSED_DEPTH + "]" * CLOSED_DEPTH, contract=S4C)
    check_eq("K12: a closed too deep scalar is one problem and no pair (the RecursionError guard is live)",
             (len(closed[0]), len(closed[1])), (0, 1))
    check_in("K12: with the ordinary text", "is not a `path: value` line", closed[1][0].text)
    check_eq("K12: BOM and CRLF read", len(_problems("﻿scope.0.id: x\r\nscope.0.state: y\r\n")), 2)
    check_eq("K12: empty and comments have nothing", [_problems(t) for t in ("", "# only\n# comments\n")], [[], []])
    many = _problems("".join(f"bad line {n}\n" for n in range(10000)))
    check_eq("K12: ten thousand bad lines, ten thousand problems (nothing cut)", len(many), 10000)


def a_skeleton_of_every_refusal_reads_back_blank() -> None:
    """K13: the whole skeleton of each refusal of K1-K3 passes `parse_values` and every value in it is blank: left as
    it is, it writes nothing, and the comments stay comments (FILE_FIX is one line)."""
    check_eq("K13: FILE_FIX is one line", "\n" in H.FILE_FIX, False)
    for text in ("scope.0.id: TC-1\nscope.0.state: approve\n", '{"scope": [{"id": "TC-1"}]}', "findings: {id: F-1}",
                 "findings:\n  - id: F-1\n", "- id: x\n"):
        sketch = _skeleton(_problems(text))
        pairs, bad = H.parse_values(sketch)
        check_eq(f"K13: {text[:24]!r}: the skeleton parses", [p.text for p in bad], [])
        check(f"K13: {text[:24]!r}: every value is blank", all(H._blank_value(p[1]) for p in pairs), f"{pairs}")


# ------------------------------------------------------------------- SC2-14: the output block of `main` (K11-K16)
CUT_REASON = "the assertion compares the response with itself, so it cannot fail for the right reason ok"     # 90 chars
SNAP_FLAGS = {"clean": (), "problems": (), "applied": ("--fix",), "pending": (), "cut": ("--fix", "--shorten")}
# t-443: the three TEXT cells that print the form path (problems, applied, pending) were re-recorded with `\` folded to `/` after `<PATH>`
# (see `_snapshot_text`); the first recording kept the Windows backslashes and so was red on Linux (CI job 28088990). Same lines, same exits.
# t-1765 X1 fix-2: the S2 form gained the `tried` table (B-B), so the clean cell counts one field more and the problems/applied/pending cells
# print one more problem and its four skeleton lines; the six cells below were re-recorded from the run's own text (K11 prints it on a miss).
# The etalon: recorded on the code BEFORE the output block left `main` (SC2-14), as `{kind: {mode: (exit, lines,
# sha256 of the stdout with the temp paths replaced)}}`. The contract of the output is FR-14: story_run.py and
# story_step.py parse this stdout and the last line of it.
SNAP_ETALON = {
    "clean": {"text": (0, 2, "df93812707156e18b859b5601dbfefb7ab844e966d13a4a022c162c3eeb7f6d0"),
              "json": (0, 20, "052f5b4cc7f8ce7b3f8dc1155cdb3050cf3c284a82727d7a3885926158b6d0da")},
    "problems": {"text": (1, 60, "d590f7744403ba4e42616894386fd9cc9ff7105e924a58c11488237aee865816"),
                 # SC2-38 F-2: each problem gained the key `code_fills` (one line each); re-recorded from the run's own text
                 "json": (1, 184, "c66bc0d4fca65e55bcc2757abb4cead8256cb6b719e2465e67f53df40934854f")},
    "applied": {"text": (1, 63, "a3599c6b7eae2dcea3422f7b0f8a5a0d8fe273d6a6a1f059bbaaa9f8b50daa0b"),
                "json": (1, 224, "4b60d733d11da4ed4f35daf758f0a34a7a4150e85d10df79aa9acc470db48d52")},
    "pending": {"text": (1, 63, "e0c585bd6ea0fcc7e3a165cb6d8423210e44ed890f6278b42a34c4447840dc94"),
                "json": (1, 224, "3de579178f38b77e1ed3832afc391ea44e5f3831a48a1d377fc8d8988cdc91c7")},
    "cut": {"text": (0, 2, "b0ca1561f6b35d9b478de9256595a6f019de1b58700069a86e8b15275b735f59"),
            "json": (0, 21, "a563708def205e0e4de7978b34d8e9e0ae926503c912361fe253500817227007")},
}


def _cut_form(art: Path) -> Path:
    """An S5 critic form filled except for one `reason` of 90 characters - over its limit of 80, the sole problem."""
    form = _form5(art, "S5-qa-code-critic-1")
    doc = _doc(form)
    start = doc.nodes["scope[0].id"].line
    end = max(n.end_line for p, n in doc.nodes.items() if p.startswith("scope[0]"))
    doc.lines = doc.lines[:start] + ["  - id: test_one", "    state: approved",
                                     f"    reason: {json.dumps(CUT_REASON)}"] + doc.lines[end + 1:]
    doc = handoff.parse(doc.text())
    for path, value in (("header.verdict", "ok"), ("review.outcome", "approved"),
                        ("review.receipt_ref", "work/windows/x.json"), ("review.rounds_used", 0),
                        ("probes.runtime_provenance", "evidence/runtime-provenance-api.json"),
                        ("probes.records[0].instance", "test_one"),
                        ("probes.records[0].verdict", "intended_failure")):
        handoff.set_value(doc, path, value)
        doc = handoff.parse(doc.text())
    form.write_text(doc.text(), encoding="utf-8")
    return form


def _snap_form(kind: str, art: Path) -> Path:
    if kind == "clean":
        # spec t-1765 X1 B-B: the S2 form now carries `tried`; the fixture predates it, so the clean cell states why the table is empty
        return _green_copy(art)
    if kind == "cut":
        return _cut_form(art)
    form = _form(art)
    if kind in ("applied", "pending"):
        H.sibling_values(form).write_text("scope[0].id: R-1\n", encoding="utf-8")
    return form


def _norm(text: str, *paths: Path) -> str:
    """The stdout with every machine-bound path replaced: the story and the form, and the package (the text answers
    print the script's own path, `python "<package>/scripts/handoff_check.py" ...`, which differs on every checkout)."""
    for path in (*paths, SCRIPTS.parent):
        for needle in (json.dumps(str(path))[1:-1], str(path), path.as_posix()):
            text = text.replace(needle, "<PATH>")
    return text


def _snapshot_text(kind: str, mode: str) -> tuple:
    """`(exit, lines, sha256, normalised stdout)` of one `handoff_check.py` run: the kind of form x the output mode."""
    root = temp_project("qa-values-k11-")
    try:
        art = _story(root)
        form = _snap_form(kind, art)
        flags = list(SNAP_FLAGS[kind]) + (["--json"] if mode == "json" else [])
        done = run_script("handoff_check.py", "--file", str(form), "--task-root", str(art), "--no-judge", *flags)
        out = _norm(done.stdout, art, form)
        if mode == "text":      # t-443: the text prints the form path raw, so after `<PATH>` a Windows run left `\work\handoffs\x.yaml`
            out = re.sub(r"<PATH>\S*", lambda m: m.group(0).replace("\\", "/"), out)      # and a Linux run `/work/...`: one form for both
        return done.returncode, len(out.splitlines()), hashlib.sha256(out.encode("utf-8")).hexdigest(), out
    finally:
        cleanup(root)


def _snapshot(kind: str, mode: str) -> tuple:
    """`(exit, lines, sha256)` of the normalised stdout (the etalon's shape)."""
    return _snapshot_text(kind, mode)[:3]


def the_output_is_the_etalon_on_every_kind_of_run() -> None:
    """K11: SC2-14, FR-14 - for {clean, problems, values applied, values waiting, `--shorten`} x {text, `--json`} the exit
    code and the whole stdout equal what the code printed before the output block left `main`. Kills mutant 8 in part
    (an output before the write) and any edit that moves a line, a space or a key."""
    for kind in SNAP_FLAGS:
        for mode in ("text", "json"):
            got = _snapshot_text(kind, mode)
            want = SNAP_ETALON.get(kind, {}).get(mode)
            if got[:3] != want:       # a hash tells nothing: show the text that differs (re-record, see SNAP_ETALON)
                print(f"K11 {kind} / {mode}: the normalised stdout was\n{got[3]}\n--- end; if the change is intended, "
                      "re-record the three values of this cell from this text (the code BEFORE the change)")
            check_eq(f"K11: {kind} / {mode}: exit, lines, sha256 of the stdout", got[:3], want)


def the_json_keys_come_in_the_order_the_readers_were_given() -> None:
    """K12: FR-14 - the order of the keys of `--json`, and of a problem's, is the one the readers were written
    against (a reader is not told it changed). Mutant 9 reorders them."""
    root = temp_project("qa-values-k12-")
    try:
        art = _story(root)
        form = _form(art)
        code, report = _hc(art, form, "--json")
        check_eq("K12: the keys of the answer, in order", list(report),
                 ["contract", "fixed", "shortened", "judged", "filled", "fields", "untouched", "no_verdict",
                  "values_applied", "values_pending", "values_notes", "values_skeleton", "problems"])
        check_eq("K12: the keys of a problem, in order", list(report["problems"][0]),
                 ["path", "problem", "fix", "kind", "also", "code_fills"])
    finally:
        cleanup(root)
    root = temp_project("qa-values-k12b-")
    try:
        art = _story(root)
        code, report = _hc(art, _snap_form("cut", art), "--fix", "--shorten", "--json")
        check_eq("K12: the keys of a cut field, in order", list(report["shortened"][0]),
                 ["field", "kept_len", "written_len"])
    finally:
        cleanup(root)


def _main_inproc(argv: list) -> tuple:
    """`(exit, stdout)` of `handoff_check.main` called in this process - for a test that must replace `os.replace`."""
    import contextlib
    import io
    saved, sys.argv = sys.argv, ["handoff_check.py", *argv]
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            code = H.main()
    finally:
        sys.argv = saved
    return code, buf.getvalue()


def a_failed_rename_is_a_problem_in_the_answer_not_a_lost_outcome() -> None:
    """K13: E12 - the file of values was applied but cannot be renamed: the answer carries the problem, `values_pending`
    names the file, `consumed` is gone (the line `applied N value(s)` is not printed), exit 1; the form holds the words.
    Kills mutant 8 (the answer built before the rename)."""
    root = temp_project("qa-values-k13-")
    real = H.os.replace
    try:
        art = _story(root)
        form = _form(art)
        sibling = H.sibling_values(form)
        sibling.write_text("scope[0].id: R-1\n", encoding="utf-8")

        def broken(*_a, **_k):
            raise OSError("locked by another process")

        H.os.replace = broken
        argv = ["--file", str(form), "--task-root", str(art), "--no-judge", "--fix"]
        code, out = _main_inproc(argv + ["--json"])
        report = json.loads(out)
        renamed = [p for p in report["problems"] if p["path"] == sibling.name]
        check_eq("K13: exit 1, the file still waits, the answer names it", (code, report["values_pending"], sibling.is_file()),
                 (1, sibling.name, True))
        check_eq("K13: one problem names the file and the lock", (len(renamed), "locked by another process" in renamed[0]["problem"]),
                 (1, True))
        check_eq("K13: the form holds the words", _doc(form).get("scope[0].id"), "R-1")
        code, out = _main_inproc(argv)
        check_in("K13: the text answer says it too", "could not be renamed", out)
        check_not_in("K13: and does not claim the file was consumed", "it is now", out)
    finally:
        H.os.replace = real
        cleanup(root)


def values_pending_is_empty_once_the_file_is_consumed() -> None:
    """K14: E13 - `values_pending` is the file's name while it waits and `""` once `--fix` consumed it (the
    expression moved unchanged). Kills mutant 10."""
    root = temp_project("qa-values-k14-")
    try:
        art = _story(root)
        form = _form(art)
        sibling = H.sibling_values(form)
        sibling.write_text("scope[0].id: R-1\n", encoding="utf-8")
        code, report = _hc(art, form, "--json")
        check_eq("K14: waiting - the name", report["values_pending"], sibling.name)
        code, report = _hc(art, form, "--fix", "--json")
        check_eq("K14: consumed - empty, and the file was renamed", (report["values_pending"], sibling.is_file(),
                                                                    report["values_applied"]), ("", False, 1))
    finally:
        cleanup(root)


def a_form_that_is_not_utf8_is_refused_whole_and_never_rewritten() -> None:
    """K15: S-2 (a), E15 - a form whose bytes are not UTF-8 is not read with `errors="replace"` (a `--fix` would write the
    replaced text over the role's file): one line, exit 2, the bytes the same, and the door it names works (FR-2).
    Kills mutant 11 (`errors="replace"` in `main`)."""
    root = temp_project("qa-values-k15-")
    try:
        art = _story(root)
        form = _form(art, "S2-qa-requirements-tester-2")      # NOT the default dispatch: the door must name it (F3)
        form.write_bytes(form.read_bytes() + b"\n# a role pasted this: \xff\xfe\xe9\n")
        before = form.read_bytes()
        for flags in ((), ("--fix",), ("--set", "scope[0].id=R-1"), ("--fix", "--shorten")):
            code, out = _hc(art, form, *flags)
            check_eq(f"K15: {flags}: exit 2, one line, the bytes are the same", (code, len(out.splitlines()), form.read_bytes() == before),
                     (2, 1, True))
        check_in("K15: the line says what it is", "not UTF-8", out)
        check_in("K15: and names the door, with the dispatch of this form",
                 f"handoff_init.py --task <T> --stage <S> --role <role> --dispatch {form.stem} --force", out)
        # The door AS PRINTED: its own flags, the placeholders filled, nothing else added but the story root.
        door = out.strip().split("Start it again: handoff_init.py ", 1)[1].split()
        fill = {"<T>": "QA-9", "<S>": "S2", "<role>": "qa-requirements-tester"}
        done = run_script("handoff_init.py", *[fill.get(word, word) for word in door], "--task-root", str(art))
        check_eq("K15: the printed door runs (exit 0)", done.returncode, 0)
        check_eq("K15: and it repaired THIS form, not a default -1 one",
                 (form.read_bytes() != before, (form.parent / f"{DISPATCH}.yaml").exists()), (True, False))
        code, report = _hc(art, form, "--json")
        check_eq("K15: the door works - a fresh form is read again (exit 1: unfilled, not 2)", (code, isinstance(report, dict)),
                 (1, True))
    finally:
        cleanup(root)


def the_not_utf8_answer_is_plain_text_even_with_json() -> None:
    """K16: E16 - with `--json` the same single plain line, exit 2 (as `no such file` and `no contract` answer): the
    caller parses stdout as JSON first and, when that fails, reads the LAST line as the reason (story_step.py,
    story_run.py). Kills mutant 12 (the branch writes JSON)."""
    root = temp_project("qa-values-k16-")
    try:
        art = _story(root)
        form = _form(art)
        form.write_bytes(form.read_bytes() + b"\n# \xff\n")
        done = run_script("handoff_check.py", "--file", str(form), "--task-root", str(art), "--no-judge", "--json")
        try:
            json.loads(done.stdout)
            parsed = True
        except ValueError:
            parsed = False
        check_eq("K16: exit 2 and stdout is not JSON", (done.returncode, parsed), (2, False))
        last = done.stdout.strip().splitlines()[-1]
        check("K16: the last line is the reason, with the form's name and the door", "not UTF-8" in last and form.name in last
              and "handoff_init.py" in last, last)
    finally:
        cleanup(root)


def the_not_utf8_door_survives_the_drivers_clip_on_a_long_path() -> None:
    """K17: F2, AR-9 - the driver keeps `splitlines()[-1][:200]` of this line (story_run.py), and the door is its tail:
    on the longest role name, a two-digit counter and a story path of 100+ characters the whole line is at most 200
    characters, so the clip cuts nothing and the door stays whole. Kills a line that prints the whole path."""
    root = temp_project("qa-values-k17-")
    try:
        deep = root.joinpath(*(["d" * 20] * 4)) / "QA-9"      # an 80-character directory chain on top of the temp root
        (deep / "work").mkdir(parents=True)
        dispatch = "S2-qa-requirements-tester-12"
        form = _form(deep, dispatch)
        form.write_bytes(form.read_bytes() + b"\n# \xff\n")
        done = run_script("handoff_check.py", "--file", str(form), "--task-root", str(deep), "--no-judge")
        last = done.stdout.strip().splitlines()[-1]
        check("K17: the form path is over 100 characters", len(str(form)) > 100, str(len(str(form))))
        check_eq("K17: the line fits the driver's clip whole", (len(last) <= 200, last[:200] == last), (True, True))
        check_in("K17: and the door, with the dispatch, is its tail", f"--dispatch {dispatch} --force", last[:200])
    finally:
        cleanup(root)


if __name__ == "__main__":
    the_output_is_the_etalon_on_every_kind_of_run()
    the_json_keys_come_in_the_order_the_readers_were_given()
    a_failed_rename_is_a_problem_in_the_answer_not_a_lost_outcome()
    values_pending_is_empty_once_the_file_is_consumed()
    a_form_that_is_not_utf8_is_refused_whole_and_never_rewritten()
    the_not_utf8_answer_is_plain_text_even_with_json()
    the_not_utf8_door_survives_the_drivers_clip_on_a_long_path()
    a_dotted_index_is_refused_with_the_indexed_row_form()
    a_list_of_objects_is_refused_with_the_first_row_lines()
    a_block_yaml_list_is_refused_with_the_headers_list()
    the_hint_never_changes_what_parse_values_decides()
    a_list_that_is_not_a_list_of_rows_gets_no_row_hint()
    an_unreadable_contract_gives_the_general_text()
    the_contract_is_read_once_and_only_when_a_line_is_bad()
    the_row_form_of_every_contract_is_a_path_the_writer_takes()
    a_section_skeleton_writes_a_list_of_values_whole()
    the_guard_block_carries_the_row_form_and_the_role_line_once()
    blocked_said_is_the_old_guards_door_on_every_input()
    a_contract_without_the_door_field_has_no_door()
    a_derivation_of_fix_opens_no_door()
    an_empty_list_and_a_flat_list_of_rows_are_taught_the_index()
    the_battery_never_raises_and_the_hint_names_only_real_paths()
    a_skeleton_of_every_refusal_reads_back_blank()
    one_call_fills_the_real_s2_form()
    stdin_is_the_same_door()
    an_index_equal_to_the_row_count_opens_a_row_from_the_contract()
    the_opened_row_is_the_contracts_template_row()
    an_index_beyond_the_row_count_is_refused_and_opens_nothing()
    a_nested_row_opens_inside_its_parent()
    a_placeholder_left_in_the_values_is_not_written()
    a_malformed_line_applies_nothing()
    an_unknown_path_is_a_problem_beside_the_applied_ones()
    values_make_the_form_touched_and_code_derived_values_do_not()
    order_is_sibling_then_values_then_set()
    a_sibling_is_applied_once()
    a_read_only_check_reports_the_merged_view_and_writes_nothing()
    an_empty_values_file_changes_nothing()
    a_named_values_file_that_does_not_exist_is_exit_2()
    json_keeps_its_keys()
    a_path_a_form_in_flight_still_holds_is_written_not_refused()
    an_index_on_a_list_of_values_is_refused_with_the_whole_list_hint()
    set_keeps_its_raw_meaning()
    a_value_from_the_file_meets_the_ordinary_limits()
    one_refusal_block_one_command()
    a_role_with_bash_is_shown_the_heredoc_and_the_file_door()
    a_role_without_bash_is_shown_the_file_door_only()
    values_report_writes_nothing_and_never_asks_the_judge()
    a_refused_values_text_keeps_its_good_lines_in_the_skeleton()
    a_blank_field_code_fills_is_not_refused_by_values_report()
    a_blocked_row_puts_blocked_problem_into_the_skeleton()
    a_skeleton_is_blank_for_every_field_of_every_contract()
    the_skeleton_cuts_nothing()
    a_skeleton_left_as_is_writes_nothing()
    finish("test_handoff_values")
