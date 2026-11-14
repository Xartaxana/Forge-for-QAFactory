#!/usr/bin/env python3
"""t-2277 FL-4: what the first look hands to the roles that read it - the head lines of the S3-S7 briefs and of the two critics.

`brief_pack.first_look_lines(task_root, stage, role)` is the one function; `brief_pack.build` calls it in the head. The record is written by
hand (the one writer `grounding_table.write_yaml`) on the project folder of `test_first_look_wiring.Project`: a register of two requirements,
a controller record, an open survey walk. One test per item of the FL-4 block of the spec; the names are the spec's.
Run: `python -B test_first_look_briefs.py` (exit code = failures) or pytest.
"""
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import harness  # noqa: E402
from harness import check, check_eq, check_in, check_not_in, finish  # noqa: E402

sys.path.insert(0, str(harness.SCRIPTS))
import brief_pack  # noqa: E402
import first_look as FL  # noqa: E402
import grounding_table as GT  # noqa: E402
from test_first_look_wiring import STAND, TICKET, WALK, Project  # noqa: E402

MARK = brief_pack.S3_ROSTER_MARK
FILE = "work/first-look.yaml"
FORBIDDEN = ("EXPECTED-VAL", "THEN-VAL", "SHOULD-VAL", "PATH-EXPECTED", "SAMPLE-EXPECTED")
PAIRS = (("S3", "qa-test-strategist"), ("S4", "qa-case-designer"), ("S4", "qa-case-critic"),
         ("S5", "qa-automator"), ("S5", "qa-code-critic"), ("S6", "qa-runner"), ("S7", "qa-failure-analyst"))


def rows_of_story():
    return [
        {"req": "R-1", "status": "confirms", "why": "the Pay button is under the total", "evidence": ["work/evidence/manual/survey-R-1/a1/001.txt"],
         "quote": "Pay", "expected": "EXPECTED-VAL", "then": "THEN-VAL", "should": "SHOULD-VAL",
         "path": {"url": "/cart", "steps": ["open the cart", "look under the total"], "expected": "PATH-EXPECTED",
                  "locators": [{"what": "Pay button", "selector": "button#pay", "seen": "yes"}],
                  "api": [{"method": "GET", "path": "/api/cart", "auth": "none", "seen": "yes",
                           "sample": {"request": "GET /api/cart", "status": "200", "response": "total 12", "expected": "SAMPLE-EXPECTED"}}],
                  "data": ["12 EUR"], "roles": ["admin"]}},
        {"req": "R-2", "status": "missing", "blocked_by": "product", "why": "the discount field is not on the page",
         "evidence": ["work/evidence/manual/survey-R-2/a1/001.txt"], "quote": "none",
         "path": {"locators": [{"what": "discount field", "selector": "input#code", "seen": "no"}]}},
        {"req": "R-3", "status": "contradicts", "why": "the total shows 12 where the text says 15", "evidence": ["work/evidence/manual/survey-R-3/a1/001.txt"],
         "quote": "12"},
        {"req": "R-4", "status": "unreachable", "blocked_by": "access", "why": "the admin screen asks for a role no account has"},
        {"req": "R-5", "status": "unreachable", "blocked_by": "product", "why": "the route answers 404", "evidence": ["work/evidence/manual/survey-R-5/a1/001.txt"]},
    ]


def write_record(p, rows=None, **frame):
    heads, reg_hash = FL.current_keys(p.task)
    record = {"walk": WALK, "stand": STAND, "stand_build": "not_established", "source_head": json.loads(heads), "register_hash": reg_hash,
              "rows": rows_of_story() if rows is None else rows, "gaps": []}
    record.update(frame)
    GT.write_yaml(p.task / "work" / "first-look.yaml", record)


def lines(p, stage, role):
    return brief_pack.first_look_lines(p.task, stage, role)


def red_row(n):
    return {"req": f"R-{n}", "status": "missing", "blocked_by": "product", "why": f"nothing for {n}"}


def test_s3_lines_count_and_red_rows():
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp, sides={"product": {"reality": "substituted"}})
        write_record(p)
        for role in ("qa-test-strategist",):          # S3 has no critic since the stage critics were removed
            got = lines(p, "S3", role)
            text = "\n".join(got)
            check_in(f"s3_lines_count_and_red_rows: the {role} head says 5 requirements", "5 requirement(s)", text)
            check_in("s3_lines_count_and_red_rows: counts by status", "1 confirms, 1 contradicts, 1 missing, 2 unreachable", text)
            for req, status in (("R-2", "missing (product)"), ("R-3", "contradicts"), ("R-4", "unreachable (access)"), ("R-5", "unreachable (product)")):
                line = next((x for x in got if x.startswith(f"- {req} ")), "")
                check(f"s3_lines_count_and_red_rows: {req} line carries its status, a why and its marker",
                      status in line and line.endswith(f"[first-look:{req}]") and len(line) > 30, line)
            check("s3_lines_count_and_red_rows: a confirmed row has no line of its own", not [x for x in got if x.startswith("- R-1 ")])
            check_in("s3_lines_count_and_red_rows: the red row's reason is the walker's words", "the discount field is not on the page", text)
            check_in("s3_lines_count_and_red_rows: the substituted side", "product (substituted)", text)
        only_green = [dict(rows_of_story()[0])]
        write_record(p, rows=only_green)
        text = "\n".join(lines(p, "S3", "qa-test-strategist"))
        check_in("s3_lines_count_and_red_rows: no red row is a line that says so (never silence), its words from the data file",
                 "no row has a red status (contradicts, missing, unreachable)", text)
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp)
        write_record(p)
        check_not_in("s3_lines_count_and_red_rows: an all-real story names no side", "Sides of the story", "\n".join(lines(p, "S3", "qa-test-strategist")))


def test_s3_line_stand_build_not_established():
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp)
        write_record(p, stand_build="not_established")
        check_in("s3_line_stand_build_not_established: the build is not established", "build is not established", "\n".join(lines(p, "S3", "qa-test-strategist")))
        write_record(p, stand_build="confirmed")
        check_not_in("s3_line_stand_build_not_established: a confirmed build says nothing of it", "build is not established",
                     "\n".join(lines(p, "S3", "qa-test-strategist")))
        write_record(p, stand_build="")
        check_in("s3_line_stand_build_not_established: a record with no word is not established either (never a pass)", "build is not established",
                 "\n".join(lines(p, "S3", "qa-test-strategist")))


def test_s4_lines_paths_ui_and_api():
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp)
        write_record(p)
        got = lines(p, "S4", "qa-case-designer")
        text = "\n".join(got)
        check_in("s4_lines_paths_ui_and_api: the screen", "screen /cart", text)
        check_in("s4_lines_paths_ui_and_api: the steps", "step open the cart", text)
        check_in("s4_lines_paths_ui_and_api: the API route with its sign-in", "api GET /api/cart (auth none, seen yes)", text)
        check_in("s4_lines_paths_ui_and_api: the sample is a seen sample", "sample seen: GET /api/cart | 200 | total 12", text)
        check_not_in("s4_lines_paths_ui_and_api: no locator or data (those are S5's)", "button#pay", text)
        check("s4_lines_paths_ui_and_api: a row with no path has no line", not [x for x in got if x.startswith("- R-3 ")])
        check("s4_lines_paths_ui_and_api: R-1 carries its marker", any(x.endswith("[first-look:R-1]") for x in got), text)
        write_record(p, rows=[rows_of_story()[2]])
        check_in("s4_lines_paths_ui_and_api: no path anywhere is said", "no row of the record names such a path", "\n".join(lines(p, "S4", "qa-case-designer")))


def test_s4_critic_lines_path_and_rule():
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp)
        write_record(p)
        text = "\n".join(lines(p, "S4", "qa-case-critic"))
        check_in("s4_critic_lines_path_and_rule: the record's path", f"qa-factory/artifacts/{TICKET}/{FILE}", text)
        check_in("s4_critic_lines_path_and_rule: the rule - a diverging step with no reason is a finding", "diverge from the path the walker took, with no reason named, are a finding", text)
        check_not_in("s4_critic_lines_path_and_rule: no path line of the rows (the critic reads the record)", "screen /cart", text)


def test_s5_lines_locators_routes_data_before_discovery():
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp)
        write_record(p)
        text = "\n".join(lines(p, "S5", "qa-automator"))
        check_in("s5_lines_locators_routes_data_before_discovery: before the automator's own discovery", "BEFORE your own discovery", text)
        check_in("s5_lines_locators_routes_data_before_discovery: the placeholder rule", "`placeholder_locator`", text)
        check_in("s5_lines_locators_routes_data_before_discovery: the provisional field", "`tests[].provisional`", text)
        check_in("s5_lines_locators_routes_data_before_discovery: a locator with what the walker saw of it", "locator Pay button: button#pay (seen yes)", text)
        check_in("s5_lines_locators_routes_data_before_discovery: a locator the walker did not see", "locator discount field: input#code (seen no)", text)
        check_in("s5_lines_locators_routes_data_before_discovery: the route", "api GET /api/cart", text)
        check_in("s5_lines_locators_routes_data_before_discovery: the data, prefixed seen", "data seen: 12 EUR", text)
        check_in("s5_lines_locators_routes_data_before_discovery: the screen and the steps are S5's too (FV1-28: the walker's path, one line per item)",
                 "- R-1 confirms: step open the cart [first-look:R-1]", text)
        check_in("s5_lines_locators_routes_data_before_discovery: the screen", "- R-1 confirms: screen /cart [first-look:R-1]", text)


def test_s5_critic_lines_path_and_rule():
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp)
        write_record(p)
        text = "\n".join(lines(p, "S5", "qa-code-critic"))
        check_in("s5_critic_lines_path_and_rule: the record's path", f"qa-factory/artifacts/{TICKET}/{FILE}", text)
        check_in("s5_critic_lines_path_and_rule: the rule on a rediscovered or guessed selector", "rediscovered or guessed where the first look saw it is a finding", text)
        check_not_in("s5_critic_lines_path_and_rule: no locator list for the critic", "button#pay", text)


def test_s6_lines_width_walked():
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp)
        write_record(p)
        got = lines(p, "S6", "qa-runner")
        check_eq("s6_lines_width_walked: one line", len(got), 1)
        check("s6_lines_width_walked: the width was walked, do not repeat the survey, go deep from the observations",
              "width was walked" in got[0] and "do not repeat the survey" in got[0] and "observations" in got[0] and FILE in got[0], got[0])
        check("s6_lines_width_walked: the cases are still walked step by step and a first-look row is no evidence that a case ran (FR-18, P26)",
              "cases are still walked step by step" in got[0] and "never evidence that a case ran" in got[0], got[0])
        check_not_in("s6_lines_width_walked: negative control - the old wording that read as 'skip what was walked' is gone", "do not repeat it", got[0])
        check_in("s6_lines_width_walked: the counts", "5 requirement(s)", got[0])


def test_s7_lines_list_observations():
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp)
        write_record(p)
        got = lines(p, "S7", "qa-failure-analyst")
        text = "\n".join(got)
        check_in("s7_lines_list_observations: the question - an executed check, then a bug candidate", "whether an executed check exists", text)
        check_in("s7_lines_list_observations: FR-22", "(FR-22)", text)
        for req in ("R-2", "R-3", "R-5"):
            line = next((x for x in got if x.startswith(f"- {req} ")), "")
            check(f"s7_lines_list_observations: {req} has a line with its reason, its evidence and its marker",
                  "evidence work/evidence/manual/survey-" in line and line.endswith(f"[first-look:{req}]"), line)
        check("s7_lines_list_observations: an unreachable row blocked by access is not a bug candidate (no line)", not [x for x in got if x.startswith("- R-4 ")])
        check("s7_lines_list_observations: a confirming row has none", not [x for x in got if x.startswith("- R-1 ")])


def test_no_record_one_line():
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp, walk=False)
        for stage, role in PAIRS:
            got = lines(p, stage, role)
            check(f"no_record_one_line: {role} at {stage} gets exactly one line, a GAP and never `no stand` as a fact",
                  len(got) == 1 and got[0].startswith("First look: a GAP (") and "(no record)" in got[0]
                  and "not a fact that there is no stand" in got[0], str(got))


def test_null_record_reason_line():
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp, walk=False)
        done = FL.put(p.task, None, "no_stand")
        check("null_record_reason_line: a null record is written", done["written"], str(done))
        for stage, role in PAIRS:
            got = lines(p, stage, role)
            check(f"null_record_reason_line: {role} at {stage} gets one line with the reason",
                  len(got) == 1 and "a GAP" in got[0] and "the stand was not walked: no stand" in got[0], str(got))


def test_unreadable_record_line():
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp, walk=False)
        (p.task / "work" / "first-look.yaml").write_text("garbage: [\n", encoding="utf-8")
        for stage, role in PAIRS:
            got = lines(p, stage, role)
            check(f"unreadable_record_line: {role} at {stage} gets one line with the reason, never a pass",
                  len(got) == 1 and "a GAP" in got[0] and "cannot be read" in got[0] and "not a fact that there is no stand" in got[0], str(got))


def test_stale_record_one_line():
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp)
        write_record(p, source_head={"product": "b" * 40})
        for stage, role in PAIRS:
            got = lines(p, stage, role)
            check(f"stale_record_one_line: {role} at {stage}: one line, STALE, no row of it", len(got) == 1 and "STALE" in got[0] and "confirms nothing" in got[0], str(got))


def test_cap_12_then_more():
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp)
        write_record(p, rows=[red_row(n) for n in range(1, 11)])        # the summary, the build line and 10 red rows: 12
        got = lines(p, "S3", "qa-test-strategist")
        check_eq("cap_12_then_more: AT the cap - 12 lines, no pointer", len(got), 12)
        check_not_in("cap_12_then_more: AT the cap - no `more`", "more:", "\n".join(got))
        write_record(p, rows=[red_row(n) for n in range(1, 12)])
        got = lines(p, "S3", "qa-test-strategist")
        check_eq("cap_12_then_more: BEYOND the cap - 12 lines and the pointer", len(got), 13)
        check_eq("cap_12_then_more: the pointer names the rest and the file", got[-1], f"+1 more: {FILE}")
        write_record(p, rows=[red_row(n) for n in range(1, 41)])
        got = lines(p, "S3", "qa-test-strategist")
        check_eq("cap_12_then_more: 40 red rows - still 12 and the pointer", (len(got), got[-1]), (13, f"+30 more: {FILE}"))
        check("cap_12_then_more: the head (summary) is the first line, never cut", got[0].startswith("First look (work/first-look.yaml"), got[0])
        check("cap_12_then_more: no line is longer than the line bound", max(len(x) for x in got[:-1]) <= brief_pack.FIRST_LOOK_LINE_CHARS + 120, str([len(x) for x in got]))
        long_why = dict(red_row(1), why="x" * 900)
        write_record(p, rows=[long_why])
        row_line = next(x for x in lines(p, "S3", "qa-test-strategist") if x.startswith("- R-1 "))
        check("cap_12_then_more: a long reason is clipped to the bound and the marker survives",
              len(row_line) <= brief_pack.FIRST_LOOK_LINE_CHARS and row_line.endswith("[first-look:R-1]") and "..." in row_line, row_line)


def test_lines_never_carry_expected_value():
    import app_card as AC
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp)
        write_record(p)
        for stage, role in PAIRS:
            text = "\n".join(lines(p, stage, role))
            for word in FORBIDDEN:
                check_not_in(f"lines_never_carry_expected_value: {role} at {stage} never carries {word}", word, text)
        items = AC.first_look_path_items(rows_of_story()[0])
        for kind, text in items:
            if kind in ("data", "sample"):
                check(f"lines_never_carry_expected_value: the {kind} item is prefixed `seen:`", "seen: " in text, text)
        both = "\n".join(lines(p, "S4", "qa-case-designer") + lines(p, "S5", "qa-automator"))
        check_eq("lines_never_carry_expected_value: the data value appears only after `seen:`", both.count("12 EUR"), both.count("seen: 12 EUR"))
        check_eq("lines_never_carry_expected_value: the sample appears only after `seen:`", both.count("total 12"), both.count("seen: GET /api/cart | 200 | total 12"))
        planted = json.dumps(rows_of_story())
        check("lines_never_carry_expected_value: the control - the record itself holds the planted words (else the test proves nothing)",
              all(word in planted for word in FORBIDDEN))
        check("lines_never_carry_expected_value: a secret in a sample is not printed",
              "hunter2hunter2hunter2hunter2xx" not in "\n".join(
                  x for _k, x in AC.first_look_path_items({"path": {"data": ["token=hunter2hunter2hunter2hunter2xx"]}})))


def test_case_critic_brief_carries_roles_and_first_look():
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp)
        p.dispatches["S4-qa-case-critic-1"] = {"id": "S4-qa-case-critic-1", "stage": "S4", "role": "qa-case-critic", "status": "running", "scope": []}
        p.save()
        write_record(p)
        text = p.brief("S4", "qa-case-critic", "S4-qa-case-critic-1")
        check_in("case_critic_brief_carries_roles_and_first_look: the roles of the product", "Product roles", text)
        check_in("case_critic_brief_carries_roles_and_first_look: the roster marker", MARK, text)
        check_in("case_critic_brief_carries_roles_and_first_look: the record's path", f"qa-factory/artifacts/{TICKET}/{FILE}", text)
        check_in("case_critic_brief_carries_roles_and_first_look: the divergence rule", "diverge from the path the walker took", text)
        check_not_in("case_critic_brief_carries_roles_and_first_look: not the strategist's instruction to name roles", "product_roles", text)
        check_in("case_critic_brief_carries_roles_and_first_look: the brief is the critic's", "Brief - S4-qa-case-critic-1 - qa-case-critic at S4", text)
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp)
        for stage, role in (("S3", "qa-test-strategist"), ("S5", "qa-automator"), ("S7", "qa-failure-analyst")):
            p.dispatches[f"{stage}-{role}-9"] = {"id": f"{stage}-{role}-9", "stage": stage, "role": role, "status": "running", "scope": []}
        p.save()
        write_record(p)
        for stage, role in (("S3", "qa-test-strategist"), ("S5", "qa-automator"), ("S7", "qa-failure-analyst")):
            check_in(f"case_critic_brief_carries_roles_and_first_look: the {role} brief at {stage} carries its first-look lines (build calls the one function)",
                     "First look", p.brief(stage, role, f"{stage}-{role}-9"))
        check_not_in("case_critic_brief_carries_roles_and_first_look: and the strategist gets no case critic's rule",
                     "diverge from the path", p.brief("S3", "qa-test-strategist", "S3-qa-test-strategist-9"))


def test_plan_critic_lines_only_when_s3_reviewer_exists():
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp)
        write_record(p)
        stages = brief_pack._stages()
        check("plan_critic_lines_only_when_s3_reviewer_exists: S3 names no reviewer in stages.json (the stage critics were removed)",
              "qa-case-critic" not in stages["S3"]["roles"], str(stages["S3"]["roles"]))
        check_eq("plan_critic_lines_only_when_s3_reviewer_exists: with no reviewer at S3 the critic gets none (nothing is invented)",
                 lines(p, "S3", "qa-case-critic"), [])
        check("plan_critic_lines_only_when_s3_reviewer_exists: the strategist still does", bool(lines(p, "S3", "qa-test-strategist")))
        check_eq("plan_critic_lines_only_when_s3_reviewer_exists: other pairs get none (a scout at S1, a tester at S2, a critic at S9)",
                 [lines(p, "S1", "qa-scout"), lines(p, "S2", "qa-requirements-tester"), lines(p, "S9", "qa-case-critic")], [[], [], []])


def test_every_knowledge_line_carries_marker():
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp)
        write_record(p)
        roster = brief_pack.case_critic_roster_lines(p.task, {"environment": STAND})
        role_lines = [x for x in roster if x.startswith("- ")]
        check("every_knowledge_line_carries_marker: the roster has role lines (the stand's admin)", bool(role_lines), str(roster))
        check("every_knowledge_line_carries_marker: every role line of the critic's roster carries the marker", all(x.endswith(MARK) for x in role_lines), str(role_lines))
        for stage, role in PAIRS:
            got = lines(p, stage, role)
            about_one = [x for x in got if x.startswith("- R-")]
            check(f"every_knowledge_line_carries_marker: every {role} line about one requirement at {stage} carries [first-look:R-n]",
                  all(x.rsplit(" ", 1)[-1].startswith("[first-look:R-") for x in about_one), str(about_one))
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp)
        cfg_path = p.root / "qa-factory" / "config.json"
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        cfg["environments"] = [{"name": STAND}]
        cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
        harness.use_project(p.root)
        roster = brief_pack.case_critic_roster_lines(p.task, {"environment": STAND})
        none = [x for x in roster if x.startswith("Product roles: none recorded")]
        check("every_knowledge_line_carries_marker: an empty roster is one marked line, with no instruction to the strategist",
              len(none) == 1 and none[0].endswith(MARK) and not [x for x in roster if "product_roles" in x], str(roster))


def _with_data(**changes):
    """A temp copy of the statuses file with `changes` applied; `FL.DATA_PATH` points at it. Returns (restore, path)."""
    tmpdir = tempfile.mkdtemp()
    path = Path(tmpdir) / "first-look-statuses.json"
    doc = dict(FL.data(), **changes)
    path.write_text(json.dumps(doc), encoding="utf-8")
    original = FL.DATA_PATH
    FL.DATA_PATH = path

    def restore():
        FL.DATA_PATH = original
    return restore


def test_red_words_come_from_the_data_file():
    """F1 (AR-1): a status added to the data file appears in the red lines with no code edit; the S7 filter and the build word are data too."""
    source = (harness.SCRIPTS / "brief_pack.py").read_text(encoding="utf-8")
    block = source[source.index("# --- the first look reaches its consumers"):source.index("# --- assembling")]
    for word in FL.data()["statuses"] + FL.data()["blocked_by"] + [FL.data()["stand_build_confirmed"]]:
        check_not_in(f"red_words_come_from_the_data_file: the word {word} is no quoted literal in the FL-4 block of brief_pack", f'"{word}"', block)
    partial = {"req": "R-6", "status": "partial", "why": "half of the field is shown"}
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp)
        rows = rows_of_story() + [partial]
        write_record(p, rows=rows)
        check("red_words_come_from_the_data_file: control - an undeclared status is no red line today",
              not [x for x in lines(p, "S3", "qa-test-strategist") if x.startswith("- R-6 ")])
        restore = _with_data(statuses=FL.data()["statuses"] + ["partial"], red_statuses=FL.data()["red_statuses"] + ["partial"])
        try:
            got = lines(p, "S3", "qa-test-strategist")
            line = next((x for x in got if x.startswith("- R-6 ")), "")
            check("red_words_come_from_the_data_file: a status added to the data file is a red line, no code edit", "partial" in line and line.endswith("[first-look:R-6]"), str(got))
            check_in("red_words_come_from_the_data_file: and it is counted by its own word", "1 partial", "\n".join(got))
            check("red_words_come_from_the_data_file: at S7 too (no narrowing is mapped for it)", any(x.startswith("- R-6 ") for x in lines(p, "S7", "qa-failure-analyst")))
        finally:
            restore()
        restore = _with_data(bug_candidate_blocked_by={"unreachable": ["access"]})
        try:
            got = lines(p, "S7", "qa-failure-analyst")
            check("red_words_come_from_the_data_file: the S7 filter is data - with `access` mapped, R-4 is listed and R-5 is not",
                  any(x.startswith("- R-4 ") for x in got) and not any(x.startswith("- R-5 ") for x in got), str(got))
        finally:
            restore()
        write_record(p, stand_build="confirmed")
        check_not_in("red_words_come_from_the_data_file: control - the data file's confirmed word silences the build line", "build is not established",
                     "\n".join(lines(p, "S3", "qa-test-strategist")))
        restore = _with_data(stand_build_confirmed="verified-build")
        try:
            check_in("red_words_come_from_the_data_file: the build word is data - another word makes `confirmed` not established", "build is not established",
                     "\n".join(lines(p, "S3", "qa-test-strategist")))
        finally:
            restore()
        restore = _with_data(red_statuses=[])
        try:
            check_in("red_words_come_from_the_data_file: no red status declared is the one line saying so, never silence", "no row has a red status ()",
                     "\n".join(lines(p, "S3", "qa-test-strategist")))
        finally:
            restore()


def test_path_items_keep_structure_and_hide_values():
    """F2: structural fields are scrubbed with tokens=False (a long data-testid survives), value fields with tokens=True."""
    import app_card as AC
    long_id = "checkout-submit-button-v2-0123456789"
    row = {"req": "R-1", "status": "confirms", "path": {
        "url": f"/shop/{long_id}", "steps": [f"click {long_id}", "type token=abcdef0123456789abcdef0123456789 into the box"],
        "locators": [{"what": "Pay", "selector": f'[data-testid="{long_id}"]', "seen": "yes"}, {"what": "Qty", "selector": "[data-testid=cart-item-quantity-input-1]", "seen": "yes"}],
        "api": [{"method": "POST", "path": f"/api/{long_id}", "auth": "token", "seen": "yes",
                 "sample": {"request": "POST", "status": "200", "response": "order a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"}}],
        "data": ["order a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"], "roles": ["admin"]}}
    items = AC.first_look_path_items(row)
    text = "\n".join(t for _k, t in items)
    check_eq("path_items_keep_structure_and_hide_values: the long selector survives whole, twice (url, locator, step, api path)", text.count(long_id), 4)
    check_in("path_items_keep_structure_and_hide_values: the second locator survives", "[data-testid=cart-item-quantity-input-1]", text)
    check_not_in("path_items_keep_structure_and_hide_values: a `token=...` pair in a step is still hidden", "abcdef0123456789abcdef0123456789", text)
    check_not_in("path_items_keep_structure_and_hide_values: a token-shaped data value is hidden", "seen: order a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6", text)
    check_not_in("path_items_keep_structure_and_hide_values: a token-shaped sample is hidden", "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6", text)
    check_in("path_items_keep_structure_and_hide_values: positive control - the data item is still there, hidden", "data seen: order [not printed]", text)
    check_not_in("path_items_keep_structure_and_hide_values: no `[not printed]` where a selector stands",
                 "[not printed]", "\n".join(t for k, t in items if k == "locator"))


def test_one_reader_of_the_record_state():
    """F6 (AR-15): the card and the brief word the SAME `first_look.state`; neither re-reads the file on its own."""
    import app_card as AC
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp)
        write_record(p)                     # the file EXISTS on disk: only the classifier can say `absent`
        original = FL.state
        try:
            FL.state = lambda task_root: {"kind": "absent", "got": FL.read(task_root), "error": ""}
            check_eq("one_reader_of_the_record_state: the brief follows the classifier (absent although a file exists)",
                     lines(p, "S3", "qa-test-strategist"), [brief_pack._fl_gap("no record", "s3")])
            check_eq("one_reader_of_the_record_state: the card follows it too", AC._first_look(p.task), ([], ["there was no first look"]))
            FL.state = lambda task_root: {"kind": "error", "got": {}, "error": "ValueError"}
            check("one_reader_of_the_record_state: an error kind is one courtesy line in the brief",
                  len(lines(p, "S3", "qa-test-strategist")) == 1 and "ValueError" in lines(p, "S3", "qa-test-strategist")[0])
        finally:
            FL.state = original
        check("one_reader_of_the_record_state: control - the real classifier on this record is `ok` and the brief has rows", FL.state(p.task)["kind"] == "ok"
              and len(lines(p, "S3", "qa-test-strategist")) > 1)
    row = rows_of_story()[1]
    check_eq("one_reader_of_the_record_state: one head of a row for the card and the brief", AC.first_look_head(row), "R-2 missing (product)")
    check_in("one_reader_of_the_record_state: the brief line starts with that head", "- R-2 missing (product): ", brief_pack._fl_line(row, "why"))


def test_roster_audience_is_a_parameter_not_a_filter():
    """F7: the critic's roster is asked for by `audience`, not cut from the strategist's lines by exact string."""
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp)
        strategist = brief_pack.s3_roster_lines(p.task, None, STAND)
        critic = brief_pack.s3_roster_lines(p.task, None, STAND, audience="critic")
        check("roster_audience: the strategist keeps its instruction and its judgment header",
              brief_pack.S3_ROSTER_NAME in strategist and any("your judgment" in x for x in strategist), str(strategist))
        check("roster_audience: the critic has the same role lines", [x for x in critic if x.startswith("- ")] == [x for x in strategist if x.startswith("- ")], str(critic))
        check("roster_audience: the critic has no instruction to name roles and no header addressed to the strategist",
              not [x for x in critic if "product_roles" in x or "your judgment" in x], str(critic))
        original = brief_pack.S3_ROSTER_NAME
        try:
            brief_pack.S3_ROSTER_NAME = original + " (composed: appended text that an equality filter would miss)"
            composed = brief_pack.case_critic_roster_lines(p.task, {"environment": STAND})
            check("roster_audience: negative control - a changed strategist line cannot leak to the critic (no string equality)",
                  not [x for x in composed if "composed" in x or "product_roles" in x], str(composed))
        finally:
            brief_pack.S3_ROSTER_NAME = original


def s5_window_lines(p, scope=("TC-001",)):
    return brief_pack.first_look_lines(p.task, "S5", "qa-automator", scope=list(scope), s5_kind="window")


def write_case(p, name, requirements):
    import contract
    root = contract.cases_root(p.task)
    root.mkdir(parents=True, exist_ok=True)
    line = "" if requirements is None else f"Requirements: {requirements}\n"       # None: a case with no requirement line at all
    (root / f"{name}.md").write_text(f"---\nid: {name}\ntask: {TICKET}\n---\nTitle: a case\n{line}", encoding="utf-8")


def window_rows(step=None):
    """R-1 is in the window; R-2 (own locator `input#code`) is not."""
    first = {"req": "R-1", "status": "confirms", "why": "w", "evidence": ["work/evidence/manual/survey-R-1/a1/001.txt"], "quote": "Pay",
             "path": {"url": "/cart", "steps": [step or "open the cart"], "locators": [{"what": "Pay button", "selector": "button#pay", "seen": "yes"}]}}
    second = {"req": "R-2", "status": "missing", "blocked_by": "product", "why": "w",
              "path": {"locators": [{"what": "discount field", "selector": "input#code", "seen": "no"}]}}
    return [first, second]


def test_s5_window_brief_holds_the_windows_substance():
    """The join from the finding's `Test` line: a non-empty record -> the S5 WINDOW brief holds the url, a step and the locator of a window
    requirement, one line per item, not those of an out-of-window requirement, and names what it left out (FR-49, AR-21)."""
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp)
        write_record(p, rows=window_rows())
        write_case(p, "TC-001", "R-1")
        got = s5_window_lines(p)
        text = "\n".join(got)
        for what, item in (("the url", "screen /cart"), ("a step", "step open the cart"), ("the locator", "locator Pay button: button#pay (seen yes)")):
            check_in(f"s5_window_brief: {what} of the window requirement is ONE line of its own", f"- R-1 confirms: {item} [first-look:R-1]", text)
        check_not_in("s5_window_brief: nothing of the out-of-window requirement", "input#code", text)
        check_eq("s5_window_brief: the outside line names the count and the record", got[-1],
                 f"+1 requirement(s) of the record outside this window: {FILE}")
        # the real build: a window dispatch of the controller holds the same lines (the call line passes `scope` and `s5_kind`)
        check_eq("s5_window_brief: control - the same record through a plan-kind call has the merged-line shape and no outside line",
                 [x for x in brief_pack.first_look_lines(p.task, "S5", "qa-automator", scope=["TC-001"], s5_kind="plan") if "outside this window" in x], [])


def test_s5_window_edges():
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp)
        write_record(p, rows=window_rows())
        # EMPTY: a window none of whose cases names a requirement -> every row, said (error direction: more)
        write_case(p, "TC-001", "none yet")
        text = "\n".join(s5_window_lines(p))
        check_in("s5_window_edges: no case names a requirement: the note", "no case of this window names a requirement: every row is shown", text)
        check("s5_window_edges: ... and every row is shown, no outside line", "input#code" in text and "button#pay" in text and "outside this window" not in text, text)
        # an R-n of the case that is not in the record is ignored; the other one stays
        write_case(p, "TC-001", "R-1, R-9")
        text = "\n".join(s5_window_lines(p))
        check("s5_window_edges: an R-n not in the record is ignored", "button#pay" in text and "input#code" not in text and "1 requirement(s) of the record outside" in text, text)
        # a case of the scope that cannot be resolved -> every row, said
        text = "\n".join(s5_window_lines(p, scope=("TC-001", "TC-404")))
        check("s5_window_edges: an unresolved case shows every row and says so",
              "could not be read: every row is shown" in text and "input#code" in text, text)
        # a case with no requirement line contributes nothing; another one still filters
        write_case(p, "TC-002", None)
        text = "\n".join(s5_window_lines(p, scope=("TC-001", "TC-002")))
        check("s5_window_edges: a case with no requirement line contributes nothing", "button#pay" in text and "input#code" not in text, text)
        # no count cap in the window: 30 requirements in the window, 30 x items lines, no `+N more`
        many = [dict(window_rows()[0], req=f"R-{n}", path={"locators": [{"what": f"w{n}", "selector": f"#s{n}", "seen": "yes"}]}) for n in range(1, 31)]
        write_record(p, rows=many)
        write_case(p, "TC-001", ", ".join(f"R-{n}" for n in range(1, 31)))
        got = s5_window_lines(p)
        check("s5_window_edges: 30 window requirements -> 30 item lines and no `+N more`",
              len([x for x in got if x.startswith("- R-")]) == 30 and not [x for x in got if " more: " in x], str(len(got)))
        # a stale record with a window: the one stale line wins
        write_record(p, rows=window_rows(), source_head={"product": "b" * 40})
        got = s5_window_lines(p)
        check("s5_window_edges: a stale record -> one STALE line, no item line", len(got) == 1 and "STALE" in got[0], str(got))


def test_s5_item_clip_and_plan_kind():
    """LIMITS: an item at 400 characters is whole, at 401 clipped with `...` and the block ends `whole:`; plan kind keeps the cap and `+N more`."""
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp)
        write_case(p, "TC-001", "R-1")
        for size, clipped in ((400, False), (401, True)):
            step = "s" * (size - len("step "))
            write_record(p, rows=window_rows(step))
            got = s5_window_lines(p)
            line = next(x for x in got if x.startswith("- R-1 confirms: step "))
            body = line[len("- R-1 confirms: "):-len(" [first-look:R-1]")]
            check_eq(f"s5_item_clip: item_{size} - the item text is {size if not clipped else 400} characters", len(body), 400)
            check_eq(f"s5_item_clip: item_{size} - clipped with `...` only beyond the bound", body.endswith("..."), clipped)
            check_eq(f"s5_item_clip: item_{size} - the block ends naming the record only when something was cut", f"whole: {FILE}" in got, clipped)
            check(f"s5_item_clip: item_{size} - the marker survives", line.endswith("[first-look:R-1]"), line)
        # plan kind: the 12-line cap and `+N more` are kept
        many = [dict(window_rows()[0], req=f"R-{n}", path={"locators": [{"what": f"w{n}", "selector": f"#s{n}", "seen": "yes"}]}) for n in range(1, 21)]
        write_record(p, rows=many)
        got = brief_pack.first_look_lines(p.task, "S5", "qa-automator", scope=["TC-001"], s5_kind="plan")
        check_eq("s5_item_clip: plan_kind - 12 lines and the pointer", (len(got), got[-1]), (13, f"+9 more: {FILE}"))
        got = brief_pack.first_look_lines(p.task, "S5", "qa-automator")
        check_eq("s5_item_clip: no keywords (every other caller) - the same cap", (len(got), got[-1]), (13, f"+9 more: {FILE}"))


def test_missing_first_look_is_a_gap_for_every_reader():
    """The live defect: a `null: no_stand` record said "no stand" as a fact. One gap sentence for S3-S7, the clause is the reader's."""
    look, name = brief_pack.FIRST_LOOK_GAP_CLAUSE["s6"], brief_pack.FIRST_LOOK_GAP_CLAUSE["s3"]
    readers = (("s3", "S3", "qa-test-strategist", name), ("s4", "S4", "qa-case-designer", name), ("s5", "S5", "qa-automator", name),
               ("s6", "S6", "qa-runner", look), ("s7", "S7", "qa-failure-analyst", look))
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp, walk=False)
        check("gap: the two clauses differ (else the per-reader data proves nothing)", look != name and look.startswith("Where needed"))
        done = FL.put(p.task, None, "no_stand")
        check("gap: a null record is written", done["written"], str(done))
        for reader, stage, role, clause in readers:
            got = lines(p, stage, role)
            check(f"gap: {reader} - a GAP, the reason, `not a fact`, then that reader's clause",
                  len(got) == 1 and got[0].startswith("First look: a GAP (the stand was not walked: no stand); "
                                                      "not a fact that there is no stand. ") and got[0].endswith(clause), str(got))
            check_not_in(f"gap: {reader} - no script is named", ".py", got[0])
            check_not_in(f"gap: {reader} - the old wording that said no stand as a fact is gone", "there was no first look", got[0])
        line = brief_pack.first_look_input_line(p.task, "work/first-look.yaml", "1 B")
        check("gap: the file line is a GAP too and names no script",
              line == "- work/first-look.yaml: no first look (the stand was not walked: no stand)",
              line)
        (p.task / "work" / "first-look.yaml").unlink()
        check_in("gap: the file line of an absent record", "no first look (the record does not exist)",
                 brief_pack.first_look_input_line(p.task, "work/first-look.yaml", ""))
        write_record(p, source_head={"product": "b" * 40})
        check("gap: a stale record keeps its meaning and gains the clause", lines(p, "S6", "qa-runner")[0].endswith(look)
              and "STALE" in lines(p, "S6", "qa-runner")[0], str(lines(p, "S6", "qa-runner")))


def test_runner_brief_says_the_probe_is_a_guess():
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp)
        check_not_in("runner_pending: control - no pending flag, no such line", "guess of code", p.first_look_brief())
        pipeline = json.loads((p.task / "pipeline.json").read_text(encoding="utf-8"))
        (p.task / "pipeline.json").write_text(json.dumps(dict(pipeline, environment_pending=True)), encoding="utf-8")
        text = p.first_look_brief()
        check_in("runner_pending: the factory's own check is a guess of code, not a fact", "that is a guess of code, not a fact. Find the way in yourself", text)
        check_in("runner_pending: the way out for the role is named", "every requirement is `unreachable` with `blocked_by: access`", text)


def access_rows(*, blocked="access"):
    return [{"req": "R-1", "status": "unreachable", "blocked_by": blocked, "why": "no account opens the admin screen"},
            {"req": "R-2", "status": "unreachable", "blocked_by": blocked, "why": "the sign-in page timed out twice"}]


def test_all_access_rows_are_one_line():
    """Item 5: every row shown unreachable for want of a way in -> ONE line with each why, whole; the closed words are the data file's."""
    lead = "First look: the walker could not reach these requirements (access): R-1: no account opens the admin screen; R-2: the sign-in page timed out twice; "
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp)
        write_record(p, rows=access_rows())
        for kind, stage, role, tail in (("s5", "S5", "qa-automator", "a gap you close with your own look"), ("s4", "S4", "qa-case-designer", "name it as a gap")):
            got = "\n".join(lines(p, stage, role))
            check_in(f"all_access: {kind} - the one line, each why whole", lead + tail, got)
            check_not_in(f"all_access: {kind} - instead of the 'no row names such a path' line", "no row of the record names such a path", got)
        write_record(p, rows=access_rows()[:1] + [dict(access_rows()[1], blocked_by="product")])
        check_in("all_access: variant one_row_product - today's text stands", "no row of the record names such a path", "\n".join(lines(p, "S5", "qa-automator")))
        write_record(p, rows=access_rows())
        for label, changes in (("key_absent", {"gap_rows": None}), ("empty_lists", {"gap_rows": {"status": [], "blocked_by": []}}),
                               ("one_list_empty", {"gap_rows": {"status": ["unreachable"], "blocked_by": []}})):
            restore = _with_data(**changes)
            try:
                check_in(f"all_access: variant {label} - the line is never printed, today's text stands", "no row of the record names such a path",
                         "\n".join(lines(p, "S5", "qa-automator")))
            finally:
                restore()


def sign_in_of(*, steps=None, url="/login", surface="ui", **extra):
    base = {"surface": surface, "actor": "default", "url": url, "steps": steps or ["opened the sign-in page", "pressed Sign in"],
            "evidence": ["work/evidence/x.txt"], "quote": "q", "req": "R-1", "why": "WHY-TEXT landed"}
    if surface == "ui":
        base.update(fields={"user": "#email", "secret": "#password", "submit": "button[type=submit]"}, landed={"url_not": ["/login-LANDED"]})
    else:
        base.update(access={"kind": "local_login", "url": "/api/login", "user_key": "AUTH_USERNAME", "secret_key": "AUTH_PASSWORD"})
    base.update(extra)
    return base


def test_own_way_in_join():
    """Join row (3): A1's `put` with a `sign_in` -> `first_look.read` -> the S5 and S6 brief line (and S3, S7)."""
    import test_first_look as TFL
    with tempfile.TemporaryDirectory() as tmp:
        s = TFL.Story(tmp)
        caps = s.ready()
        done = s.put(s.rows(caps), sign_in=TFL._good_ui(caps))
        check("own_way_in: A1's put writes the way in", done["written"], str(done))
        want = ("Way in found by this story's first look (walk S3-first-look, ui, as default): url /login; fields user #email, secret #password, "
                "submit button[type=submit]; steps: opened the sign-in page; typed the account and pressed Sign in; it worked then - if it fails "
                "now, find the way yourself and record it.")
        for stage, role in (("S5", "qa-automator"), ("S6", "qa-runner"), ("S3", "qa-test-strategist"), ("S7", "qa-failure-analyst")):
            check_eq(f"own_way_in: {role} reads the line", brief_pack.sign_in_lines(s.task, stage, role), [want])
        check_eq("own_way_in: a role outside the first look's readers gets none", brief_pack.sign_in_lines(s.task, "S9", "qa-retro-analyst"), [])
        text = "\n".join(brief_pack.sign_in_lines(s.task, "S5", "qa-automator"))
        for hidden in ("Signed in through the page", "Pay button", "work/evidence"):
            check_not_in(f"own_way_in: the line prints no `why`, quote or evidence ({hidden})", hidden, text)
        s.put(s.rows(caps), sign_in=TFL._good_http(caps))
        check_in("own_way_in: http line shape", "access local_login at /api/login, key names AUTH_USERNAME/AUTH_PASSWORD",
                 "\n".join(brief_pack.sign_in_lines(s.task, "S5", "qa-automator")))
        s.put(s.rows(caps))
        check_eq("own_way_in: a record with no sign_in -> no line (today's brief)", brief_pack.sign_in_lines(s.task, "S5", "qa-automator"), [])


def test_own_way_in_edges():
    with tempfile.TemporaryDirectory() as tmp:
        p = Project(tmp)
        for label, value in (("absent", None), ("empty", {}), ("not_a_dict", "logged in"), ("a_list", ["x"])):
            write_record(p, **({} if value is None else {"sign_in": value}))
            check_eq(f"own_way_in_edges: {label} -> no line", brief_pack.sign_in_lines(p.task, "S5", "qa-automator"), [])
        write_record(p, sign_in=sign_in_of(), source_head={"product": "b" * 40})
        check_eq("own_way_in_edges: a stale record -> no sign-in line (the stale single line wins)", brief_pack.sign_in_lines(p.task, "S5", "qa-automator"), [])
        write_record(p, rows=[], null="no_stand", sign_in=sign_in_of())
        check_eq("own_way_in_edges: a null record -> no line", brief_pack.sign_in_lines(p.task, "S5", "qa-automator"), [])
        # LIMITS: 600 whole, 601 and beyond cut AT the limit with `...`, followed by `whole:`
        write_record(p, sign_in=sign_in_of(steps=["a"]))
        base = len(brief_pack.sign_in_lines(p.task, "S5", "qa-automator")[0])
        for size, cut in ((600, False), (601, True), (2000, True)):
            write_record(p, sign_in=sign_in_of(steps=["a" * (size - base + 1)]))
            got = brief_pack.sign_in_lines(p.task, "S5", "qa-automator")
            check_eq(f"own_way_in_edges: line_{size} - {'cut at the limit with the record named' if cut else 'whole'}",
                     (len(got[0]), got[1:], got[0].endswith("...") if cut else got[0].endswith("record it.")),
                     (600, [f"whole: {FILE}"] if cut else [], True))
        # INVARIANT: a secret-looking value of a hand-edited record is scrubbed, whatever the guard at put did
        write_record(p, sign_in=sign_in_of(steps=["typed password: hunter2hunter2 in the box"]))
        check_not_in("own_way_in_edges: a password pair in a step is scrubbed", "hunter2hunter2", "\n".join(brief_pack.sign_in_lines(p.task, "S5", "qa-automator")))
        # the walker's own brief: the record is current -> the line follows
        write_record(p, sign_in=sign_in_of())
        check_in("own_way_in_edges: the walker's brief holds the way found by the last walk", "Way in found by this story's first look", p.first_look_brief())
        write_record(p)
        check_not_in("own_way_in_edges: control - no sign_in, none in the walker's brief", "Way in found by this story's first look", p.first_look_brief())


def main():
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
    finish("test_first_look_briefs")


if __name__ == "__main__":
    main()
