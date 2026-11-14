#!/usr/bin/env python3
"""t-1502 G-1 / G-2: the grouping hint of the S5 plan, the `apart_reason` field and the rule's text in three carriers.

The join key (the forge finding of 28.10.2026): the REAL output of the producer - `fixtures/run-12586-s5-plan/s5-plan.json`, the
plan the 0.10.3 author wrote for run TP1-12586 - goes through its consumers (`s5_plan.grouping_hints`, `check_report`,
`render_slice`, `--check`; `s5_precheck.plan_result`; the plan critic's brief), not only a hand-built input.

Every key names the mutation it kills (spec t-1502 section 5.1/5.2): K3 the `apart_reason` exception removed; K9 grouping without
the level, or a private path normalizer instead of `s5_precheck._file_key`; K5 the list limit 5; K1 `extend` among the candidates;
K4 a non-text `apart_reason` kept a candidate; K3c `render_slice` without the line; K8 a second `load` in `main`; K2 (in
test_s5_precheck_plan.py) `ok = not findings and not hints`; K10 / K-G2 the text of a carrier cut out (DOC-DISPATCH witness: the
keys are the spec's lines, quoted verbatim BEFORE the run, with a negative control that cuts one key out and must go red).
"""
import contextlib
import copy
import hashlib
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import SCRIPTS, check, check_eq, check_in, check_not_in, cleanup, finish, temp_dir, temp_project  # noqa: E402

sys.path.insert(0, str(SCRIPTS))
import detector_verdict as DV  # noqa: E402
import s5_plan as SP  # noqa: E402

import test_s5_plan as BASE  # noqa: E402  (its fixtures; its checks run only under its own __main__)
from test_s5_plan_check import Fake, good_plan, has, mutate  # noqa: E402

put = BASE.put
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "run-12586-s5-plan" / "s5-plan.json"
FIXTURE_CASES = ("TC-001", "TC-002", "TC-003", "TC-004", "TC-005", "TC-006", "TC-007", "TC-008", "TC-009", "TC-011")
GROUPED = ("TC-001", "TC-002", "TC-004", "TC-005", "TC-006", "TC-007", "TC-011")      # the seven api cases of one file
API_FILE = "testproject1_test_harness/tests/integrations/project/test_integration_project_change.py"
REASON = "another fixture: needs an MS Teams integration in the target project"
# The two project files the plan's two `extend` rows name: the check looks them up under the project root.
STUBS = {"testproject1_test_harness/tests/integrations/project/test_ms_teams_integration.py":
         "def test_create_ms_teams_integration_duplicate_returns_409():\n    assert True\n",
         "testproject1_test_harness/tests/ui/integrations/test_edit_integration.py":
         "def test_edit_integration_update_alias():\n    assert True\n\n\ndef test_edit_integration_update_credentials():\n    assert True\n"}
IDS = {"TC-001": "test_put_project_change_moves_integration", "TC-002": "test_put_project_change_moves_ms_teams_integration",
       "TC-004": "test_put_project_change_requires_admin_in_target", "TC-005": "test_put_project_change_from_user_scope_and_collision"}


def fixture_plan():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


@contextlib.contextmanager
def fixture_story(ticket="QA-1"):
    """`(project, task)`: an onboarded project holding the two files the plan extends and, under a story folder, the producer's own
    `s5-plan.json`. The story's CONTROLLER is the one seam that is faked (the helpers of the story fixtures are written for the case
    ids TC-1..TC-n): `controller.Controller(task_root)` answers `Fake` with the fixture's ten cases as the S5 scope, one window
    holding all of them, and the project root - so the real plan reader, the real plan check, the real hint and the real consumers
    (`main`, `plan_result`, the brief) all read the real file. The project is cleaned up on exit."""
    import controller as CT
    project = temp_project("qa-s5grp-")
    task = project / "qa-factory" / "artifacts" / ticket
    task.mkdir(parents=True)
    put(task, "pipeline.json", json.dumps({"ticket": ticket, "size": "S", "environment": "local", "stages": {}, "gates": {}, "halts": []}))
    for rel, text in STUBS.items():
        put(project, rel, text)
    harness.use_project(project)
    put(task, SP.PLAN_REL, FIXTURE.read_bytes())
    real = CT.Controller
    CT.Controller = lambda root, *args, **kw: Fake(FIXTURE_CASES, project, windows=[{"index": 1, "surface": "other", "scope": list(FIXTURE_CASES)}])
    try:
        yield project, task
    finally:
        CT.Controller = real
        cleanup(project)


def run_main(project, *argv):
    """`(exit code, stdout, stderr)` of `s5_plan.main()` with these arguments, in this process (the controller seam as `fixture_story`)."""
    out, err, old = io.StringIO(), io.StringIO(), sys.argv
    sys.argv = ["s5_plan.py", *argv]
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = SP.main()
    finally:
        sys.argv = old
    return code, out.getvalue(), err.getvalue()


def piece_of(plan, cases):
    """The slice of the cases as `window_slice` makes it (a hand-built piece: the same keys), for `render_slice`."""
    rows = [r for r in SP._rows(plan, "cases") if r.get("case") in cases]
    return {"window": 1, "windows": [1], "asked": list(cases), "cases": rows, "missing": [],
            "tests": [t for t in SP._rows(plan, "tests") if any(c in cases for c in t.get("cases") or [])], "remainders": [],
            "requirements": [], "remarks": [], "surface": "other", "size": len(cases), "over_cap": False, "cap": None, "grown": []}


def write_plan(task, plan):
    put(task, SP.PLAN_REL, json.dumps(plan))


def with_reason(plan, case, reason):
    plan = copy.deepcopy(plan)
    for test in plan["tests"]:
        if test["cases"] == [case]:
            test["apart_reason"] = reason
    return plan


def row(identifier, cases, file="tests/test_a.py", level="api", shape="new", **extra):
    return dict({"id": identifier, "file": file, "cases": cases if isinstance(cases, str) else list(cases), "level": level, "shape": shape}, **extra)


# --- K1: the producer's real output, through the hint ---------------------------------------------------------

def k1_the_real_plan():
    plan = fixture_plan()
    hints = SP.grouping_hints(plan)
    check_eq("K1: the stand's plan gives exactly one hint (seven tests, one group)", len(hints), 1)
    expected = (f"7 tests at level api in {API_FILE} each prove their own case(s) ({IDS['TC-001']}, {IDS['TC-002']}, {IDS['TC-004']}, "
                f"{IDS['TC-005']}, +3 more): " + ", ".join(GROUPED))
    check_eq("K1: its message names the file, four test ids, '+3 more' and the seven cases", hints[0]["message"], expected)
    tail = hints[0]["message"].split("): ", 1)[1]
    check("K1: TC-003 (extend, another file) and TC-008/TC-009 (e2e-ui extends) are in no group",
          not any(case in tail for case in ("TC-003", "TC-008", "TC-009")), tail)
    check_eq("K1: the row is neutral: case, message, fix, tag", sorted(hints[0]), ["case", "fix", "message", "tag"])
    check_eq("K1: its case is the first of the group", hints[0]["case"], "TC-001")
    check("K1: its fix leads only to a parameterized test and names the door",
          "one parameterized test" in hints[0]["fix"] and "`apart_reason`" in hints[0]["fix"] and "consolidate" not in hints[0]["fix"], hints[0]["fix"])
    check("K1: the tag is stable and has the group form", hints[0]["tag"] == SP.grouping_hints(fixture_plan())[0]["tag"] and hints[0]["tag"].startswith("group-")
          and len(hints[0]["tag"]) == len("group-") + 8)
    # the same through the one reader of the file on disk
    root = temp_dir("qa-s5grp-k1-")
    try:
        put(root, SP.PLAN_REL, FIXTURE.read_bytes())
        check_eq("K1: SP.load of the producer's file gives the same hint", SP.grouping_hints(SP.load(root)), hints)
        findings, notes = SP.check_report(root, Fake(FIXTURE_CASES, windows=[{"index": 1, "surface": "other", "scope": list(FIXTURE_CASES)}]))
        check_eq("K1: the producer's real plan is clean for the plan check (the hint is no finding)", findings, [])
    finally:
        cleanup(root)


# --- K3 / K3b / K3c: the door `apart_reason`, a parameter of one test, the slice ---------------------------------

def k3_apart_reason():
    plan = with_reason(fixture_plan(), "TC-002", REASON)
    hints = SP.grouping_hints(plan)
    check_eq("K3: a reason on TC-002's test leaves a group of six", len(hints), 1)
    message = hints[0]["message"]
    check("K3: ... six tests, without TC-002 and without its test id",
          message.startswith("6 tests at level api in ") and "TC-002" not in message and IDS["TC-002"] not in message, message)
    check_in("K3: ... '+2 more'", ", +2 more)", message)
    for blank in ("   ", "", None, "\t\n"):
        again = SP.grouping_hints(with_reason(fixture_plan(), "TC-002", blank))
        check_eq(f"K3: a blank reason ({blank!r}) is no reason - seven again", again[0]["message"].split(" ", 1)[0] if again else None, "7")
    only = fixture_plan()
    for test in only["tests"]:
        if test["cases"][0] in GROUPED:
            test["apart_reason"] = REASON
    check_eq("K3: every candidate with a reason: no hint", SP.grouping_hints(only), [])


def k3b_red_as_a_parameter():
    """A case expected red is a PARAMETER of one test (B1): one test over the seven cases is not a group and is no hint."""
    plan = fixture_plan()
    tests = [t for t in plan["tests"] if t["cases"][0] not in GROUPED]
    merged = {"id": IDS["TC-001"], "file": API_FILE, "function": IDS["TC-001"], "cases": list(GROUPED),
              "thens": [t for test in plan["tests"] if test["cases"][0] in GROUPED for t in test["thens"]],
              "level": "api", "shape": "parameterize", "data": "own", "assert": "each parameter id names its case"}
    plan["tests"] = [merged] + tests
    check_eq("K3b: the seven cases as parameters of ONE parameterized test: no hint", SP.grouping_hints(plan), [])


def k3c_slice_shows_the_reason():
    text = SP.render_slice(piece_of(with_reason(fixture_plan(), "TC-002", REASON), ["TC-002"]))
    check_in("K3c: the slice of a window shows the test's reason", f"apart_reason: {REASON}", text)
    check_not_in("K3c: no field, no line", "apart_reason", SP.render_slice(piece_of(fixture_plan(), ["TC-002"])))
    check_not_in("K3c: a blank reason is no line", "apart_reason", SP.render_slice(piece_of(with_reason(fixture_plan(), "TC-002", "   "), ["TC-002"])))
    check_not_in("K3c: a reason that is not text is no line (it is a finding of the check)", "apart_reason",
                 SP.render_slice(piece_of(with_reason(fixture_plan(), "TC-002", {"why": "x"}), ["TC-002"])))
    check_in("K3c: the line sits with the other fields of the test, before its assert", f"apart_reason: {REASON}\nassert: ",
             SP.render_slice(piece_of(with_reason(fixture_plan(), "TC-002", REASON), ["TC-002"])))


# --- K4: the field's form: 300 / 301, not text ------------------------------------------------------------------

def k4_field_form():
    root = temp_dir("qa-s5grp-k4-")
    try:
        def findings_with(value, key="apart_reason"):
            plan = mutate(good_plan(), lambda p: p["tests"][0].__setitem__(key, value))
            put(root, SP.PLAN_REL, json.dumps(plan))
            return SP.check_report(root, Fake(("TC-1", "TC-2", "TC-3")))[0]
        check_eq("K4: 300 characters is accepted (AT)", [f for f in findings_with("x" * 300) if "apart_reason" in f], [])
        over = [f for f in findings_with("x" * 301) if "apart_reason" in f]
        check("K4: 301 is a finding (BEYOND), naming the field and the limit", len(over) == 1 and "301 characters" in over[0] and "limit is 300" in over[0], str(over))
        for blank in ("", None, "   "):
            check_eq(f"K4: {blank!r} is no finding (the field is optional)", [f for f in findings_with(blank) if "apart_reason" in f], [])
        absent = [f for f in SP.check_report(root, Fake(("TC-1", "TC-2", "TC-3")))[0] if "apart_reason" in f]
        check_eq("K4: the field absent (an old plan): no finding", absent, [])
        for value in ({"why": "x"}, 5, ["x"], True):
            found = [f for f in findings_with(value) if "apart_reason" in f]
            check(f"K4: {value!r} is a finding of form: not text", len(found) == 1 and "is not text" in found[0], str(found))
        pair = [row("T-1", ["TC-1"]), row("T-2", ["TC-2"], apart_reason={"why": "x"})]
        check_eq("K4: a test whose reason is not text is NOT a candidate (one candidate left: no group)", SP.grouping_hints({"tests": pair}), [])
        pair[1]["apart_reason"] = None
        check_eq("K4: ... with null it is a candidate", len(SP.grouping_hints({"tests": pair})), 1)
        pair[1]["apart_reason"] = "another surface"
        check_eq("K4: ... with a text reason it stands apart", SP.grouping_hints({"tests": pair}), [])
    finally:
        cleanup(root)


# --- K5: the list of ids: 4 / 5 ---------------------------------------------------------------------------------

def k5_id_list():
    four = SP.grouping_hints({"tests": [row(f"T-{n}", [f"TC-{n}"]) for n in range(1, 5)]})[0]["message"]
    check("K5: four ids are listed whole, with no tail (AT)", "(T-1, T-2, T-3, T-4)" in four and "more" not in four, four)
    five = SP.grouping_hints({"tests": [row(f"T-{n}", [f"TC-{n}"]) for n in range(1, 6)]})[0]["message"]
    check("K5: five ids list four and '+1 more' (BEYOND)", "(T-1, T-2, T-3, T-4, +1 more)" in five and "T-5)" not in five, five)


# --- K6: the helpers never raise; awkward inputs -----------------------------------------------------------------

def k6_helpers():
    root = temp_dir("qa-s5grp-k6-")
    try:
        check_eq("K6: no file -> (None, 'no plan')", SP.plan_for_hints(root), (None, "no plan"))
        check_eq("K6: no file -> no rows and nothing to say (the plan check says it)", SP.hint_rows(root), ([], ""))
        put(root, SP.PLAN_REL, b"{not json")
        plan, why = SP.plan_for_hints(root)
        check("K6: a plan that is not JSON -> (None, 'PlanUnreadable: ...')", plan is None and why.startswith("PlanUnreadable: "), why)
        check_eq("K6: ... no rows and nothing to say (a finding already refuses it)", SP.hint_rows(root), ([], ""))
        put(root, SP.PLAN_REL, b'{"schema": 2}')
        check("K6: another schema -> the same", SP.plan_for_hints(root)[0] is None and SP.plan_for_hints(root)[1].startswith("PlanUnreadable: "))
        put(root, SP.PLAN_REL, FIXTURE.read_bytes())
        check_eq("K6: a readable plan -> (plan, '')", (SP.plan_for_hints(root)[1], SP.plan_for_hints(root)[0]["schema"]), ("", 1))
        check_eq("K6: ... and its rows, nothing to say", (len(SP.hint_rows(root)[0]), SP.hint_rows(root)[1]), (1, ""))
        real_load = SP.load

        def boom(_root):
            raise RuntimeError("boom " + "x" * 200)
        SP.load = boom
        try:
            plan, why = SP.plan_for_hints(root)
            check("K6: a `load` that raises -> (None, '<Type>: <message up to 100>')", plan is None and why.startswith("RuntimeError: boom") and len(why) <= 100 + 20, why)
            check("K6: ... hint_rows says what failed, never raises", SP.hint_rows(root)[0] == [] and SP.hint_rows(root)[1].startswith("RuntimeError: boom"))
        finally:
            SP.load = real_load
        real_hints = SP.grouping_hints

        def broken(_plan, file_key=None):
            raise ValueError("no way")
        SP.grouping_hints = broken
        try:
            check_eq("K6: grouping_hints that raises -> hint_rows says so", SP.hint_rows(root), ([], "ValueError: no way"))
        finally:
            SP.grouping_hints = real_hints
    finally:
        cleanup(root)
    awkward = [("plan None", None), ("plan []", []), ("plan 'x'", "x"), ("tests {}", {"tests": {}}), ("tests None", {"tests": None}),
               ("row [1]", {"tests": [[1], row("T-1", ["TC-1"])]}),
               ("cases a string", {"tests": [row("T-1", "TC-1"), row("T-2", "TC-2")]}),
               ("cases with None", {"tests": [row("T-1", [1, None]), row("T-2", ["TC-2", None])]}),
               ("file 5", {"tests": [row("T-1", ["TC-1"], file=5), row("T-2", ["TC-2"], file=5)]}),
               ("level API", {"tests": [row("T-1", ["TC-1"], level="API"), row("T-2", ["TC-2"], level="API")]}),
               ("shape New", {"tests": [row("T-1", ["TC-1"], shape="New"), row("T-2", ["TC-2"], shape="New")]}),
               ("level a list", {"tests": [row("T-1", ["TC-1"], level=["api"]), row("T-2", ["TC-2"], level=["api"])]}),
               ("file blank", {"tests": [row("T-1", ["TC-1"], file="  "), row("T-2", ["TC-2"], file="  ")]}),
               ("one test", {"tests": [row("T-1", ["TC-1", "TC-2"])]}),
               ("one case in two tests", {"tests": [row("T-1", ["TC-1"]), row("T-2", ["TC-1"])]}),
               ("apart_reason a mapping", {"tests": [row("T-1", ["TC-1"], apart_reason={"why": "x"}), row("T-2", ["TC-2"], apart_reason={"why": "x"})]})]
    for label, plan in awkward:
        try:
            got = SP.grouping_hints(plan)
        except Exception as exc:        # noqa: BLE001
            got = f"raised {exc!r}"
        check_eq(f"K6: an awkward input ({label}) gives no hint and no exception", got, [])
    repeated = SP.grouping_hints({"tests": [row("T-1", ["TC-1"]), row("T-1", ["TC-2"])]})
    check_eq("K6: a repeated id does not raise (one group of two rows)", len(repeated), 1)
    check_eq("K6: a test already naming two cases and a lone neighbour of the same file: a hint",
             len(SP.grouping_hints({"tests": [row("T-1", ["TC-1", "TC-2"], shape="parameterize"), row("T-2", ["TC-3"])]})), 1)
    for shape in ("extend", "reuse", "consolidate"):
        check_eq(f"K6: shape {shape} is not a candidate", SP.grouping_hints({"tests": [row("T-1", ["TC-1"], shape=shape), row("T-2", ["TC-2"], shape=shape)]}), [])


# --- K8: --check on the real plan, through the command line ---------------------------------------------------------

def k8_check_command():
    with fixture_story() as (project, task):
        code, out, err = run_main(project, "--task", "QA-1", "--check")
        lines = out.splitlines()
        hint_at = next((i for i, line in enumerate(lines) if line.startswith("hint: [plan] 7 tests at level api in ")), None)
        ok_at = next((i for i, line in enumerate(lines) if line.startswith("OK:")), None)
        check("K8: the real plan prints the hint before the OK line", hint_at is not None and ok_at is not None and hint_at < ok_at, out[:800])
        check_eq("K8: ... the exit code is 0 (a hint is no finding)", code, 0)
        check_in("K8: ... the line under the hint is its advice", "  consider: if they share setup and action, write one parameterized test", out)
        check_in("K8: ... the OK line says the hint is advice and names the door", SP.HINT_ADVICE, out)
        verdict = DV.parse(code, out, err)
        check_eq("K8: the detector's reader finds a pass (no finding, no defect)", (verdict["findings"], verdict["defects"], verdict["unmigrated"]), ([], [], ""))
        # the same plan with every candidate answered: no hint, the same exit code
        answered = fixture_plan()
        for test in answered["tests"]:
            if test["cases"][0] in GROUPED:
                test["apart_reason"] = REASON
        write_plan(task, answered)
        code, out, err = run_main(project, "--task", "QA-1", "--check")
        check_eq("K8: every candidate answered: no hint line and the same exit code", (code, "hint:" in out), (0, False))
        check_not_in("K8: ... and the OK line carries no advice sentence", SP.HINT_ADVICE, out)
        # a finding next to a hint: the hint is printed, the verdict is a REJECT with ONE finding, exit 1
        bad = fixture_plan()
        bad["tests"][1]["apart_reason"] = "y" * 301
        write_plan(task, bad)
        code, out, err = run_main(project, "--task", "QA-1", "--check")
        check_eq("K8: a finding + a hint: exit 1, REJECT of one finding, the hint above it",
                 (code, "REJECT — 1 finding(s)" in out, 0 <= out.find("hint:") < out.find("REJECT")), (1, True, True))
        verdict = DV.parse(code, out, err)
        check_eq("K8: ... and the detector's reader counts one finding, no defect", (len(verdict["findings"]), verdict["defects"]), (1, []))
        # an unreadable plan: REJECT, exit 1, no hint, no traceback and not exit 2 (F5)
        put(task, SP.PLAN_REL, b"{half")
        code, out, err = run_main(project, "--task", "QA-1", "--check")
        check("K8: an unreadable plan is a REJECT of one finding, exit 1 (not 2), no hint, no traceback",
              code == 1 and "REJECT — 1 finding(s)" in out and "hint:" not in out and "Traceback" not in err, out + err)
        (task / SP.PLAN_REL).unlink()
        code, out, err = run_main(project, "--task", "QA-1", "--check")
        check("K8: no plan file: exit 1, REJECT, no hint", code == 1 and "REJECT" in out and "hint:" not in out, out + err)
        # the hints could not be computed (any other failure): a note that says so, the verdict unchanged
        write_plan(task, fixture_plan())
        real = SP.grouping_hints
        SP.grouping_hints = lambda plan, file_key=None: (_ for _ in ()).throw(ValueError("no way"))
        try:
            code, out, err = run_main(project, "--task", "QA-1", "--check")
        finally:
            SP.grouping_hints = real
        check("K8: grouping_hints that raises: exit 0, a 'not checked' note, no hint, no traceback",
              code == 0 and "note: not checked: the grouping hints of the plan (ValueError: no way)" in out and "hint:" not in out, out + err)


# --- K9: the key of the group, with an unlike plan ----------------------------------------------------------------------

def k9_the_key():
    check_eq("K9: one level, two files: no group",
             SP.grouping_hints({"tests": [row("T-1", ["TC-1"], file="tests/a.py"), row("T-2", ["TC-2"], file="tests/b.py")]}), [])
    spelled = SP.grouping_hints({"tests": [row("T-1", ["TC-1"], file="tests/x.py"), row("T-2", ["TC-2"], file="./tests/x.py"),
                                           row("T-3", ["TC-3"], file="tests\\x.py"), row("T-4", ["TC-4"], file=".\\tests\\x.py")]})
    check("K9: 'x.py', './x.py' and a backslash path are ONE group (the one normalizer, _file_key)",
          len(spelled) == 1 and spelled[0]["message"].startswith("4 tests at level api in tests/x.py "), str(spelled))
    check_eq("K9: the case of a path is not folded",
             SP.grouping_hints({"tests": [row("T-1", ["TC-1"], file="tests/X.py"), row("T-2", ["TC-2"], file="tests/x.py")]}), [])
    check_eq("K9: api and e2e-ui tests of one file, one of each: no group",
             SP.grouping_hints({"tests": [row("T-1", ["TC-1"], level="api"), row("T-2", ["TC-2"], level="e2e-ui")]}), [])
    two = SP.grouping_hints({"tests": [row("T-1", ["TC-1"], level="api"), row("T-2", ["TC-2"], level="api"),
                                       row("T-3", ["TC-3"], level="e2e-ui"), row("T-4", ["TC-4"], level="e2e-ui")]})
    check_eq("K9: two of each level in one file: two groups, by level, in order of appearance",
             [h["message"].split(" ")[4] for h in two], ["api", "e2e-ui"])
    check("K9: ... their tags differ", two[0]["tag"] != two[1]["tag"])
    check_eq("K9: a different suite (java, a name with no test_ prefix): the same rule, no pattern of a language",
             len(SP.grouping_hints({"tests": [row("T-1", ["TC-1"], file="src/test/CalcSpec.java", level="unit"),
                                              row("T-2", ["TC-2"], file="src/test/CalcSpec.java", level="unit")]})), 1)


# --- G-2: `fit: new` allows `parameterize`; the two meanings of `consolidates` ---------------------------------------------

TWO_LISTS = "`consolidates` means two lists: in the S5 plan, the tests a consolidated test merges; in the manifest, the cases the instance proves"      # without the full stop: it closes a parenthesis in two carriers


def merged_plan(cases, fit_of=None):
    """The fixture's plan with the tests of `cases` (all in the one api file) replaced by ONE `parameterize` test over them."""
    plan = fixture_plan()
    mine = [t for t in plan["tests"] if t["cases"][0] in cases]
    merged = {"id": mine[0]["id"], "file": API_FILE, "function": mine[0]["function"], "cases": list(cases),
              "thens": [x for t in mine for x in t["thens"]], "level": "api", "shape": "parameterize", "data": "own",
              "assert": "each parameter id names its case"}
    plan["tests"] = [merged] + [t for t in plan["tests"] if t["cases"][0] not in cases]
    for row_ in plan["cases"]:
        if fit_of and row_["case"] in fit_of:
            row_["s3"]["fit"] = fit_of[row_["case"]]
    return plan


def kg2_fit_new_parameterize():
    root = temp_dir("qa-s5grp-g2-")
    scope = Fake(FIXTURE_CASES, windows=[{"index": 1, "surface": "other", "scope": list(FIXTURE_CASES)}])
    try:
        def findings_of(plan):
            put(root, SP.PLAN_REL, json.dumps(plan))
            return SP.check_report(root, scope)[0]
        check_eq("G-2 K1: TC-004 and TC-005 (S3 fit `new`) as ONE parameterize test: no finding", findings_of(merged_plan(["TC-004", "TC-005"])), [])
        check_eq("G-2 K3 (= G-1 K3b): the seven cases of the stand as parameters of one test (fit `new` and `param`): no finding, no hint",
                 (findings_of(merged_plan(list(GROUPED))), SP.grouping_hints(merged_plan(list(GROUPED)))), ([], []))
        found = findings_of(merged_plan(["TC-004", "TC-005"], fit_of={"TC-004": "extend T3"}))
        check("G-2 K2: S3 `extend T3` + a parameterize test is still a finding (a person's S3 word needs a deviation)",
              has(found, "shape `parameterize` departs from S3", "TC-004 (S3 fit `extend T3` allows extend, reuse, consolidate)"), str(found))
        check_eq("G-2: the vocabulary row itself", SP._words()[1]["new"], ["new", "parameterize", "consolidate"])
    finally:
        cleanup(root)


def kg2_two_lists_in_three_places():
    # the two carriers' words are the row `consolidates-means-two-lists` of design/role-rules.json; the finding's text stays here
    root = temp_dir("qa-s5grp-g2b-")
    try:
        plan = mutate(good_plan(), lambda p: p["tests"][0].__setitem__("shape", "consolidate"))
        put(root, SP.PLAN_REL, json.dumps(plan))
        finding = next(f for f in SP.check_report(root, Fake(("TC-1", "TC-2", "TC-3")))[0] if "`consolidates`" in f)
        check_in("G-2 K5: the finding of an empty `consolidates` carries the phrase", TWO_LISTS, finding)
        check_in("G-2 K5: ... after its fix, in one line", "fix: list the tests it merges (", finding)
    finally:
        cleanup(root)


def kfix_one_printer_and_the_vocabulary():
    import handoff
    import s5_precheck as PC
    check("fix 4: every GROUP_SHAPES entry is a word of vocabulary `test_shapes`",
          set(SP.GROUP_SHAPES) <= set(handoff.vocabulary()["test_shapes"]), str(SP.GROUP_SHAPES))
    check("fix 4 (negative control): a shape outside the vocabulary is caught by the same comparison",
          not {"no-such-shape"} <= set(handoff.vocabulary()["test_shapes"]))
    hint = {"check": "plan", "message": "2 tests\nin one file", "fix": "write one\ntest", "level": "hint"}

    def printed(call):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            call()
        return buf.getvalue()
    direct = printed(lambda: SP.print_hints([hint]))
    via_report = printed(lambda: PC.report({"ok": True, "findings": [], "hints": [hint], "notes": [], "cases": []}))
    check_in("fix 2: report prints the lines of the shared printer", direct, via_report)
    check_eq("fix 2: a newline in a hint is one line on both paths", direct,
             "hint: [plan] 2 tests in one file\n  consider: write one test\n")


# --- TQ2-1 K2 G1-G9: the case critic's merge the plan neither follows nor answers (advice, never a gate) --------------------

def concern(case="TC-1", problem="parametrise into one test: TC-1, TC-2"):
    return {"id": "CC-1", "case": case, "problem": problem}


def mplan(keys, *tests):
    return {"cases": [{"case": key} for key in keys], "tests": list(tests)}


def k_merge_hints_table():
    two = [row("T-1", ["TC-1"]), row("T-2", ["TC-2"])]
    both = [row("T-1", ["TC-1"], apart_reason="another fixture"), row("T-2", ["TC-2"], apart_reason="another surface")]
    three = concern(problem="parametrise into one test: TC-1, TC-2, TC-3")
    table = [  # label, plan, concerns, None (no hint) or the words the ONE hint holds
        ("G1 one test holds both", mplan(["TC-1", "TC-2"], row("T-1", ["TC-1", "TC-2"], shape="extend")), [concern()], None),
        ("G2 two tests, no reason", mplan(["TC-1", "TC-2"], *two), [concern()], ["CC-1", "TC-1", "TC-2", "T-1", "T-2"]),
        ("G3a a reason on both", mplan(["TC-1", "TC-2"], *both), [concern()], None),
        ("G3b a reason on one only", mplan(["TC-1", "TC-2"], two[0], both[1]), [concern()], ["T-1", "T-2"]),
        ("G4 group of three, one test holds two", mplan(["TC-1", "TC-2", "TC-3"], row("T-1", ["TC-1", "TC-2"]), row("T-3", ["TC-3"])),
         [three], ["TC-3", "T-1", "T-3"]),
        ("G5 a case outside the plan", mplan(["TC-1"], row("T-1", ["TC-1"])), [concern(problem="parametrise into one test: TC-1, TC-9, TC-9")], None),
        ("G6 TC-2 is a remainder (no test)", mplan(["TC-1", "TC-2"], row("T-1", ["TC-1"])), [concern()], None),
        ("G7 area keys, bare ids in the concern", mplan(["speakers/TC-1", "speakers/TC-2"], row("T-1", ["speakers/TC-1"]), row("T-2", ["speakers/TC-2"])),
         [concern()], ["speakers/TC-1", "speakers/TC-2"]),
        ("G7b TC-10 is not TC-1 (the one matcher)", mplan(["TC-1", "TC-10"], row("T-1", ["TC-1"]), row("T-10", ["TC-10"])), [concern()], None),
        ("G8a no token", mplan(["TC-1", "TC-2"], *two), [concern(problem="F-2 flag precondition TC-1, TC-2")], None),
        ("G8b a global concern", mplan(["TC-1", "TC-2"], *two), [concern(case=None, problem="the case critic's findings file cannot be read")], None),
        ("G8c malformed concerns and plan rows", mplan(["TC-1", "TC-2"], *two, "x", {"cases": 5}), [None, {"problem": 5}, {"id": "CC-1"}], None),
        ("G8d a plan that is not a mapping", None, [concern()], None),
    ]
    for label, plan, concerns, wanted in table:
        got = SP.merge_hints(plan, concerns)
        if wanted is None:
            check_eq(f"{label}: no hint", got, [])
        else:
            check(f"{label}: ONE hint of the grouping hint's shape naming {wanted}",
                  len(got) == 1 and sorted(got[0]) == ["case", "fix", "message", "tag"] and all(w in got[0]["message"] for w in wanted), str(got))
    again = SP.merge_hints(mplan(["TC-1", "TC-2"], *two), [concern()])[0]
    check("G2: the tag is stable over two calls and has the merge form", again["tag"] == SP.merge_hints(mplan(["TC-1", "TC-2"], *two), [concern()])[0]["tag"]
          and again["tag"].startswith("merge-") and len(again["tag"]) == len("merge-") + 8, again["tag"])
    check_eq("G2: two concerns naming one group give ONE hint", len(SP.merge_hints(mplan(["TC-1", "TC-2"], *two), [concern(), concern("TC-2")])), 1)
    # a dispatch that names no scope (the controller refuses to send one, but a legacy record may hold none): over-carry, said aloud
    for label, scope in (("G10a empty scope list", []), ("G10b scope None", None)):
        got, why = SP.concerns_for_scope(None, None, [concern(), concern("TC-2")], scope)
        check_eq(f"{label}: every concern comes back unplaced", [c["placement"] for c in got], ["unplaced", "unplaced"])
        check_eq(f"{label}: the reason says no scope was named", why, "the dispatch names no scope")
        check_eq(f"{label}: no concerns for no concerns", SP.concerns_for_scope(None, None, [], scope), ([], "the dispatch names no scope"))


def k_merge_hint_both_paths():
    """G9: the producer's real plan and a concern splitting two of its cases: `--check` and `s5_precheck.plan_result` print the same hint
    line; the findings, `ok` and the exit code are those of the same plan with no concern (advice, never a gate)."""
    import s5_precheck as PC
    split = concern("TC-001", "parametrise into one test: TC-001, TC-002")
    real = SP.case_concerns
    try:
        results = {}
        for label, carried in (("with", [split]), ("without", [])):
            SP.case_concerns = lambda root, state, _c=carried: list(_c)
            with fixture_story() as (project, task):
                code, out, _err = run_main(project, "--task", "QA-1", "--check")
                result = PC.plan_result(task)
                printed = io.StringIO()
                with contextlib.redirect_stdout(printed):
                    PC.report(result)
            lines = lambda text: [l for l in text.splitlines() if "asked to parametrise" in l or "write one parameterized test over" in l]
            results[label] = (code, result["ok"], result["findings"], lines(out), lines(printed.getvalue()))
    finally:
        SP.case_concerns = real
    check_eq("G9: --check and plan_result print the same merge hint lines", results["with"][3], results["with"][4])
    check("G9: ... and the hint names the two cases and the door", len(results["with"][3]) == 2 and "TC-001, TC-002" in results["with"][3][0]
          and "apart_reason" in results["with"][3][1], str(results["with"][3]))
    check_eq("G9: no concern, no merge line", results["without"][3], [])
    check_eq("G9: the exit code, `ok` and the findings are those of the plan with no concern", results["with"][:3], results["without"][:3])


# --- FV1-6 N2: the rows the S4 case critic still rejects travel to the automator (rows C1-C14) -----------------------------------

R_COLS = ("plan row", "case", "reviewed", "verdict", "note", "fix")
R_DIR = "work/test-cases/api/"


def r_round(number, verdict, rows, cols=R_COLS):
    """One findings round (newest goes on top of the file); a row is `(plan row, case, reviewed, verdict, note, fix)`."""
    keep = [i for i, name in enumerate(R_COLS) if name in cols]
    table = "".join("| " + " | ".join(row[i] for i in keep) + " |\n" for row in rows)
    return (f"# Case critic findings - round {number}\n\nVerdict: {verdict}\n\n## Roll-call\n\n| " + " | ".join(cols) + " |\n|"
            + "---|" * len(cols) + "\n" + table + "\n").encode("utf-8")


def r_story(root, files, links=None):
    """`files` is `{name: [(bytes of a round, status), ...]}` oldest first; the state holds one S4 critic dispatch per round,
    in the order they were accepted, each with the receipt of the file as it stood then."""
    dispatches, number = {}, 0
    for name, rounds in files.items():
        data = b""
        for round_bytes, status in rounds:
            data = round_bytes + data
            number += 1
            ident = f"S4-qa-case-critic-{number}"
            dispatches[ident] = {"id": ident, "stage": "S4", "role": "qa-case-critic", "status": status,
                                 "evidence_refs": [{"path": R_DIR + name, "sha256": hashlib.sha256(data).hexdigest()}]}
        BASE.put(root, R_DIR + name, data)
    if links is not None:
        BASE.put(root, "state/story-case-links.json", json.dumps({"links": [{"case_id": case} for case in links]}))
    return {"dispatches": dispatches}


def r_carried(files, links=None, edit=None):
    """`(remarks, silent, stderr)` of a story built from `files`; `edit` may change a file after its receipts were taken."""
    root = temp_dir("qa-fv16-n2-")
    try:
        state = r_story(root, files, links)
        if edit:
            path = root / R_DIR / edit[0]
            path.write_bytes(edit[1](path.read_bytes()))
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            report = SP.concern_report(root, state)
        return report["concerns"], report["silent"], err.getvalue()
    finally:
        cleanup(root)


def r_brief(files, dispatch_id="W1", role="qa-automator"):
    """`(head, the side file's story path)` of the plan-form brief of `role` for a story built from `files`."""
    import brief_pack as BP
    root = temp_dir("qa-fv16-n2-")
    try:
        state = r_story(root, files)
        with contextlib.redirect_stderr(io.StringIO()):
            return (BP.case_concern_lines(root, dispatch_id, state, role, False)["head"],
                    BP._rel(root, f"work/briefs/{dispatch_id}-case-concerns.md"))
    finally:
        cleanup(root)


def r_brief_head(files, dispatch_id="W1", role="qa-automator"):
    return r_brief(files, dispatch_id, role)[0]


def fv16_still_rejected_rows():
    import critic_rollcall as CR
    ok = "accepted"
    rej = ("TS-1", "TC-1", "yes", "reject", "wrong oracle", "assert the 404")
    prt = ("TS-2", "TC-2", "yes", "partial", "half covered", "")
    appr = ("TS-1", "TC-1", "yes", "approve", "", "")
    conc = ("TS-3", "TC-3", "yes", "approve_with_concerns", "F-1 flag", "")
    ids = lambda remarks: [r["id"] for r in remarks]
    cases = lambda remarks: [r["case"] for r in remarks]

    got, silent, _ = r_carried({"critic-findings.md": [(r_round(1, "reject", [rej]), ok)]})
    check_eq("C1 reject-row-carried: one remark, id CR-TC-1, still_rejected, the critic's words whole",
             [(r["id"], r["case"], r["still_rejected"], r["check"], r["problem"], r["fix"], r["review"]) for r in got],
             [("CR-TC-1", "TC-1", True, "case critic, S4 - still rejected", "wrong oracle", "assert the 404", "S4-qa-case-critic-1")])
    check_in("C1 reject-row-carried: expected names the round and the findings file", "round S4-qa-case-critic-1 (its full finding is in "
             + R_DIR + "critic-findings.md)", got[0]["expected"])
    check_eq("C1 reject-row-carried: the keys are the chain's nine and the remark's own flag", sorted(got[0]),
             sorted(["id", "case", "test", "then", "kind", "check", "problem", "expected", "fix", "review", "still_rejected"]))
    check_eq("C1 reject-row-carried: the file is not silent", silent, [])

    got, _s, _ = r_carried({"critic-findings.md": [(r_round(1, "partial", [prt]), ok)]})
    check_eq("C2 partial-row-carried", [(r["id"], r["problem"]) for r in got], [("CR-TC-2", "half covered")])
    got, _s, _ = r_carried({"critic-findings.md": [(r_round(1, "reject", [("TS-1", "TC-1", "yes", "reject", "", "")]), ok)]})
    check_eq("C2 partial-row-carried: a reject with no note says so", got[0]["problem"], CR.REJECTED_NOTE)

    got, _s, _ = r_carried({"critic-findings.md": [(r_round(1, "reject", [rej]), ok), (r_round(2, "approve", [appr]), ok)]})
    check_eq("C3 later-approve-supersedes: nothing from the earlier reject", got, [])

    two = [rej, ("TS-2", "TC-2", "yes", "reject", "second", "")]
    got, _s, _ = r_carried({"critic-findings.md": [(r_round(1, "reject", two), ok),
                                                   (r_round(2, "approve", [("TS-2", "TC-2", "yes", "approve", "", "")]), ok)]})
    check_eq("C4 later-round-not-listing-keeps-earlier-reject: TC-1 keeps round 1's word, TC-2 is superseded",
             [(r["case"], r["review"]) for r in got], [("TC-1", "S4-qa-case-critic-1")])

    glob = ("TS-5", "", "yes", "reject", "no case named", "")
    got, _s, _ = r_carried({"critic-findings.md": [(r_round(1, "reject", [glob, ("TS-6", "", "yes", "reject", "again", "")]), ok)]})
    check_eq("C5 no-case-id-global: case None, the plan row leads the problem, ids deduplicated",
             [(r["id"], r["case"], r["problem"]) for r in got],
             [("CR-global", None, "(plan row TS-5) no case named"), ("CR-global.2", None, "(plan row TS-6) again")])

    two_rounds = lambda a, b: {"critic-findings.md": [(r_round(1, "reject", [a]), ok), (r_round(2, "reject", [b]), ok)]}
    got, _s, _ = r_carried(two_rounds(glob, ("TS-6", "", "yes", "reject", "no case for TS-6", "")))
    check_eq("C5b case-less-reject-of-another-plan-row-kept: round 2's TS-6 does not drop round 1's TS-5",
             (sorted(r["id"] for r in got), sorted(r["problem"] for r in got)),
             (["CR-global", "CR-global.2"], ["(plan row TS-5) no case named", "(plan row TS-6) no case for TS-6"]))
    got, _s, _ = r_carried(two_rounds(glob, ("TS-5", "", "yes", "reject", "still no case", "")))
    check_eq("C5b case-less-reject-of-the-same-plan-row: only the later round's remark is carried",
             [(r["id"], r["problem"]) for r in got], [("CR-global", "(plan row TS-5) still no case")])
    got, _s, _ = r_carried(two_rounds(("", "", "yes", "reject", "first", ""), ("", "", "yes", "reject", "second", "")))
    check_eq("C5b case-less-reject-with-no-plan-row: they share one key, the later round's is carried",
             [r["problem"] for r in got], ["(plan row ) second"])
    got, _s, _ = r_carried(two_rounds(("", "", "yes", "reject", "first", ""), ("TS-6", "", "yes", "reject", "other", "")))
    check_eq("C5b case-less-reject-with-no-plan-row: a later reject of ANOTHER plan row does not drop it (over-carry)",
             sorted(r["problem"] for r in got), ["(plan row ) first", "(plan row TS-6) other"])

    base = {"critic-findings.md": [(r_round(1, "approve_with_concerns", [conc]), ok)]}
    alone, _s, _ = r_carried(base)
    both, _s, _ = r_carried({"critic-findings.md": [(r_round(1, "reject", [conc, ("TS-4", "TC-4", "yes", "reject", "n", "")]), ok)]})
    first, _s, _ = r_carried({"critic-findings.md": [(r_round(1, "reject", [("TS-4", "TC-4", "yes", "reject", "n", ""), conc]), ok)]})
    check_eq("C6 concern-ids-unchanged: with no reject the concern is CC-1", ids(alone), ["CC-1"])
    check_eq("C6 concern-ids-unchanged: with a reject after it, CC-1 and CR-TC-4", ids(both), ["CC-1", "CR-TC-4"])
    check_eq("C6 concern-ids-unchanged: a reject listed BEFORE the concern does not move CC-1", sorted(ids(first)), ["CC-1", "CR-TC-4"])
    two_files = {"a/critic-findings.md": [(r_round(1, "approve_with_concerns", [conc]), ok)],
                 "b/critic-findings.md": [(r_round(2, "reject", [rej, conc]), ok)]}
    got, _s, _ = r_carried(two_files)
    check_eq("C6 concern-ids-unchanged: across files the numbering counts concerns only", ids(got), ["CC-1", "CC-2", "CR-TC-1"])

    got, silent, err = r_carried({"critic-findings.md": [(r_round(1, "reject", [rej]), ok)]}, edit=("critic-findings.md", lambda b: b + b"x"))
    check_eq("C7 receipt-doubt-carries-nothing: no remark, the file is silent", (got, silent), ([], [R_DIR + "critic-findings.md"]))
    check_in("C7 receipt-doubt-carries-nothing: stderr says why", "no end of the file matches the receipt", err)

    import brief_pack as BP
    root7 = temp_dir("qa-fv16-n2-")
    try:
        state7 = r_story(root7, {"critic-findings.md": [(r_round(1, "reject", [rej]), ok)]})
        (root7 / R_DIR / "critic-findings.md").write_bytes((root7 / R_DIR / "critic-findings.md").read_bytes() + b"x")
        for role7 in ("qa-automator", "qa-code-critic"):
            with contextlib.redirect_stderr(io.StringIO()):
                heads7 = BP.case_concern_lines(root7, "W1", state7, role7, False)["head"]
            check(f"C7b receipt-doubt-head-reads-every-non-approving-row: role {role7}",
                  len(heads7) == 1 and "whose verdict is not an approving one there before you" in heads7[0], str(heads7))
        real7, BP._sp = BP._sp, (lambda: (_ for _ in ()).throw(RuntimeError("boom")))
        try:
            fail7 = BP.case_concern_lines(root7, "W1", state7, "qa-automator", False)["head"]
        finally:
            BP._sp = real7
        check("C7b the failed-read head reads every non-approving row too", "whose verdict is not an approving one in work/test-cases" in fail7[0],
              str(fail7))
    finally:
        cleanup(root7)

    only = {"critic-findings.md": [(r_round(1, "approve_with_concerns", [conc]), ok)]}
    got, _s, _ = r_carried(only)
    check_eq("C8 no-reject-byte-identical: the concern is the nine-key CC-1 remark as before", got,
             [{"id": "CC-1", "case": "TC-3", "test": None, "then": None, "kind": "remark", "check": "case critic, S4", "problem": "F-1 flag",
               "expected": "the case critic's full finding is in " + R_DIR + "critic-findings.md, round S4-qa-case-critic-1; take it into "
               "account when the case is automated, or say in `plan_remarks` why it does not apply", "fix": "", "review": "S4-qa-case-critic-1"}])
    check_eq("C8 no-reject-byte-identical: the brief head carries no still-rejected clause", [l for l in r_brief_head(only) if "still rejected" in l], [])

    head = r_brief_head({"critic-findings.md": [(r_round(1, "reject", [conc, rej]), ok)]})
    check("C9 brief-head-counts: 2 carried, 1 of them still rejected", any(
        "carried 2 concern(s) to automation (1 of them cases it still rejected when S4 went on; 0 ask to parametrise" in l for l in head), str(head))
    check_eq("C9 brief-head-counts: r = 0, no clause", [l for l in r_brief_head(only) if "of them cases it still rejected" in l], [])

    head8, rel8 = r_brief(only)
    check_eq("C8b no-reject-head-byte-equal-to-main: the plan-author head is the text main builds, word for word", head8,
             [f"The case critic carried 1 concern(s) to automation (0 ask to parametrise cases into one test): {rel8}. Answer each in the "
              f"plan: a `{CR.PARAMETRISE_TOKEN}` concern is one parameterized test over its cases, or each test that holds them says why "
              "in `apart_reason`"])

    withrej = {"critic-findings.md": [(r_round(1, "reject", [conc, rej]), ok)]}
    clause = "1 of them cases it still rejected when S4 went on; "
    for role9, field9 in (("qa-automator", "in `apart_reason`"),):
        long9 = r_brief_head(withrej, "S5-qa-automator-plan-12-and-a-long-tail-of-id-" + "x" * 8, role9)
        check("C9b clause-does-not-cut-the-instruction: a 55-character dispatch id keeps the field to fill and the clause",
              len(long9) == 1 and clause in long9[0], str(long9))
    sizes9 = set()
    for size in range(1, 80):
        one, _rel = r_brief(withrej, "d" * size)
        pre = one[0].replace(clause, "", 1)
        check(f"C9b head-at-the-limit: id of {size} characters, the clause once and the text without it within the bound",
              one[0].count(clause) == 1 and len(pre) <= BP.HEAD_LINE_CHARS, str(one))
        sizes9.add(len(pre))
        if "apart_reason" in pre:
            check(f"C9b head-keeps-the-field: id of {size} characters", "in `apart_reason`" in one[0], one[0])
    check("C9b head-at-the-limit: the ids reach a text of exactly 400 characters before the clause, and one cut from a longer one (400)",
          BP.HEAD_LINE_CHARS in sizes9 and max(sizes9) == BP.HEAD_LINE_CHARS, str(sorted(sizes9)[-3:]))
    real_limit = BP.HEAD_LINE_CHARS
    BP.HEAD_LINE_CHARS = 30
    try:
        forced = r_brief_head(withrej)
    finally:
        BP.HEAD_LINE_CHARS = real_limit
    check("C9b clause-after-the-cut: a cut that loses the parenthesis appends the clause as its own sentence, never drops it",
          len(forced) == 1 and forced[0].endswith(". 1 of them cases it still rejected when S4 went on"), str(forced))

    gone = {"critic-findings.md": [(r_round(1, "reject", [("TS-9", "TC-9", "yes", "reject", "bad", "")]), ok)]}
    prefix = "(case removed since the review) bad"
    for label, links, wanted in (("pinned set without TC-9", ["TC-1"], prefix), ("empty pinned set (legacy)", None, "bad"),
                                 ("pinned set with TC-9", ["TC-9"], "bad")):
        got, _s, _ = r_carried(gone, links)
        check_eq(f"C10 removed-case-prefixed: {label}", [r["problem"] for r in got], [wanted])

    nine = ("TS-9", "TC-9", "yes", "reject", "bad", "")
    new = (r_round(2, "approve", [appr]), ok)
    for label, status, wanted in (("earlier critic stale", "stale", []), ("earlier critic accepted", ok, ["TC-9"])):
        got, _s, _ = r_carried({"critic-findings.md": [(r_round(1, "reject", [nine]), status), new]})
        check_eq(f"C11 stale-earlier-life-silent: {label}", cases(got), wanted)

    word = lambda w: {"critic-findings.md": [(r_round(1, "reject", [("TS-1", "TC-1", "yes", w, "n", "")]), ok)]}
    for cell, shown in (("approved", "approved"), ("fail", "fail"), ("", "unstated")):
        got, _s, _ = r_carried(word(cell))
        rows = CR.current_rejected(r_round(1, "reject", [("TS-1", "TC-1", "yes", cell, "n", "")]))
        check_eq(f"C12 unknown-word-and-no-verdict-column: cell {cell!r} is carried, as written", (cases(got), [r["verdict"] for r in rows]),
                 (["TC-1"], [shown]))
    nocol = tuple(c for c in R_COLS if c != "verdict")
    pair = [("TS-1", "TC-1", "yes", "", "a", ""), ("TS-2", "TC-2", "yes", "", "b", ""), ("TS-3", "TC-3", "no", "", "c", "")]
    for declared, wanted in (("reject", ["TC-1", "TC-2"]), ("approve_with_concerns", [])):
        got, _s, _ = r_carried({"critic-findings.md": [(r_round(1, declared, pair, cols=nocol), ok)]})
        check_eq(f"C12 unknown-word-and-no-verdict-column: no verdict column under `Verdict: {declared}` (unreviewed row skipped)",
                 cases(got), wanted)

    old = r_round(1, "reject", [rej, prt])
    new = r_round(2, "reject", [("TS-9", "TC-9", "yes", "reject", "newest only", "")])
    check_eq("C13 current-rejected-reader: a two-round file reads the newest round only",
             [(r["case"], r["problem"], r["plan_row"]) for r in CR.current_rejected(new + old)], [("TC-9", "newest only", "TS-9")])
    with contextlib.redirect_stderr(io.StringIO()):
        check_eq("C13 current-rejected-reader: a file with no roll-call is None", CR.current_rejected(b"# findings\n"), None)
        check_eq("C13 current-rejected-reader: a newest round of approving rows only is []",
                 CR.current_rejected(r_round(3, "approve", [appr, conc]) + new + old), [])
    check_eq("C13 current-rejected-reader: the problem is not cut", len(CR.current_rejected(r_round(1, "reject", [
        ("TS-1", "TC-1", "yes", "reject", "x" * 900, "")]))[0]["problem"]), 900)

    got, _s, _ = r_carried({"critic-findings.md": [(r_round(1, "reject", [rej, ("TS-7", "TC-1", "yes", "partial", "again", "")]), ok)]})
    check_eq("C14 cr-id-dedup: one case twice in a round", ids(got), ["CR-TC-1", "CR-TC-1.2"])
    got, _s, _ = r_carried({"a/critic-findings.md": [(r_round(1, "reject", [rej]), ok)],
                         "b/critic-findings.md": [(r_round(2, "reject", [rej]), ok)]})
    check_eq("C14 cr-id-dedup: one case in two files", ids(got), ["CR-TC-1", "CR-TC-1.2"])


def main():
    fv16_still_rejected_rows()
    k1_the_real_plan()
    k_merge_hints_table()
    k_merge_hint_both_paths()
    kfix_one_printer_and_the_vocabulary()
    k3_apart_reason()
    k3b_red_as_a_parameter()
    k3c_slice_shows_the_reason()
    k4_field_form()
    k5_id_list()
    k6_helpers()
    k8_check_command()
    k9_the_key()
    kg2_fit_new_parameterize()
    kg2_two_lists_in_three_places()
    finish("test_s5_plan_grouping")


if __name__ == "__main__":
    main()
