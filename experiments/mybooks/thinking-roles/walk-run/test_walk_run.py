"""Tests of the walk-run scripts (t-2009; recipe t-2006). Run against a TEMP copy of the plan, never tr-walk itself.

    python -m pytest -p no:cacheprovider experiments/mybooks/thinking-roles/walk-run/test_walk_run.py -q
"""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_prep as CP  # noqa: E402
import check_run as CR  # noqa: E402
import claim_check as CC  # noqa: E402
import clean_driver_state as CD  # noqa: E402
import fallback_lane as FL  # noqa: E402
import make_walk_cases as MW  # noqa: E402

REAL_PLAN = Path("C:/AI/Factory/mybooks-stand/tr-walk/qa-factory/artifacts/LOCAL-1/work/test-plan.json")
CARDS = HERE.parent.parent / "add-to-cart-disputed-places.md"
PACKAGE_SCRIPTS = Path("C:/AI/Factory/wt-fbfix/ai-packages/qa-factory/scripts")
DATA = json.loads(MW.DATA.read_text(encoding="utf-8"))
CARD_NUMBERS = [c["card"] for c in DATA["cases"]]
EXPECTED_IDS = [f"LOCAL-1_TC_1{n:02d}" for n in list(range(1, 20)) + [21, 22, 23, 24]]
SILENT = {2, 4, 5, 6, 7, 8, 19, 22}
# Strings that stand ONLY in the cards' "seen" (Vidno) fields: results the walker must never be told (rule R1). The first is the example
# of the recipe; the others are copied from the card file and checked to be there (see test_known_strings_are_in_the_seen_fields).
VIDNO_STRINGS = ["11 copies", "Valid quantity is required", "Something went wrong", "Cart item not found", "Failed to add book to cart", "Book added to cart"]


@pytest.fixture()
def story(tmp_path):
    """A temp story folder with a COPY of the real plan: <tmp>/proj/qa-factory/artifacts/LOCAL-1/work/test-plan.json."""
    if not REAL_PLAN.is_file():
        pytest.skip("the copy tr-walk is not on this machine")
    task = tmp_path / "proj" / "qa-factory" / "artifacts" / "LOCAL-1"
    (task / "work").mkdir(parents=True)
    shutil.copyfile(REAL_PLAN, task / "work" / "test-plan.json")
    return task


def generated(task):
    out = MW.build(task)
    return Path(out["target"]), out


def leaks(text: str) -> list:
    return [s for s in VIDNO_STRINGS if s in text]


# --- the generator -------------------------------------------------------------------------------------------------------------

def test_23_ids_in_the_exact_form(story):
    target, out = generated(story)
    names = sorted(p.stem for p in target.glob("*.md"))
    assert names == EXPECTED_IDS and len(names) == 23
    assert all(re.fullmatch(r"LOCAL-1_TC_1\d\d", n) for n in names)
    assert sorted(out["rows"]) == sorted(f"TS-1{n:02d}" for n in CARD_NUMBERS)


def test_idempotent_never_doubled(story):
    target, _ = generated(story)
    before = json.loads((story / "work" / "test-plan.json").read_text(encoding="utf-8"))["rows"]
    (target / "LOCAL-1_TC_101.md").write_text("stale", encoding="utf-8")
    generated(story)
    after = json.loads((story / "work" / "test-plan.json").read_text(encoding="utf-8"))["rows"]
    ids = [r["id"] for r in after]
    assert ids == [r["id"] for r in before] and len(ids) == len(set(ids)) == 20 + 23
    assert "stale" not in (target / "LOCAL-1_TC_101.md").read_text(encoding="utf-8")


def test_plan_old_rows_untouched_and_walk_rows_after_them(story):
    old = json.loads(REAL_PLAN.read_text(encoding="utf-8"))["rows"]
    generated(story)
    rows = json.loads((story / "work" / "test-plan.json").read_text(encoding="utf-8"))["rows"]
    assert rows[:20] == old
    assert [r["id"] for r in rows[20:]] == [f"TS-1{n:02d}" for n in sorted(CARD_NUMBERS)]


def test_no_vidno_words_in_any_case(story):
    target, _ = generated(story)
    for path in target.glob("*.md"):
        assert leaks(path.read_text(encoding="utf-8")) == [], path.name
    # the data file itself is clean too (the cases are made from it)
    assert leaks(MW.DATA.read_text(encoding="utf-8")) == []


def test_negative_control_the_leak_check_can_fail():
    assert leaks("Then 1. The page shows 11 copies in the cart") == ["11 copies"]
    assert leaks("clean text") == []


def test_known_strings_are_in_the_seen_fields():
    """The key test means something only if the strings are really in the cards' 'Vidno' lines (the first one is the recipe's own example)."""
    text = CARDS.read_text(encoding="utf-8")
    seen = [line for line in text.splitlines() if line.startswith("- **Видно")]
    blob = "\n".join(seen)
    for s in VIDNO_STRINGS[1:]:
        assert s in blob, s


def test_silent_cases_have_the_observation_form_never_unknown(story):
    target, _ = generated(story)
    silent_found = set()
    for n in CARD_NUMBERS:
        text = (target / f"LOCAL-1_TC_1{n:02d}.md").read_text(encoding="utf-8")
        oracles = json.loads(CP.front_line(text, "then_oracles"))
        assert all(o["source"] in CP.THEN_ORACLE_WORDS for o in oracles)
        if "NO EXPECTED VALUE" in text:
            silent_found.add(n)
            assert [o["source"] for o in oracles] != ["unknown"] and len(oracles) == 1
            assert "requirement silent" in text and "never pass or fail" in text
        else:
            assert all(o["source"] != "unknown" for o in oracles)
    assert silent_found == SILENT


def test_no_credential_value_and_login_by_name_only(story):
    target, _ = generated(story)
    blob = "\n".join(p.read_text(encoding="utf-8") for p in target.glob("*.md")) + MW.DATA.read_text(encoding="utf-8")
    assert "fill-account [data-testid=\"login-email-input\"] user user" in blob
    assert not re.search(r"password\s*[:=]\s*\S+", blob, re.I)
    assert not re.search(r"[\w.-]+@[\w-]+\.\w+", blob)


def test_sections_and_teardown(story):
    target, _ = generated(story)
    text = (target / "LOCAL-1_TC_105.md").read_text(encoding="utf-8")
    assert "## Given" in text and "## Steps" in text and "## Then" in text and "## Teardown" in text
    assert "restore_request" in text.split("## Teardown")[1]
    assert "channel: manual-agent" in text and "area: walk" in text
    one = (target / "LOCAL-1_TC_101.md").read_text(encoding="utf-8")
    assert "## Teardown" not in one and "1. If the header shows no signed-in user" not in one


def test_lanes_are_eight_of_at_most_three():
    table = FL.lanes(DATA)
    assert len(table) == 8 and sum(len(v) for v in table.values()) == 23 and max(len(v) for v in table.values()) == 3
    assert FL.lane_actors(table["G1"]) == ("guest", None)
    assert FL.lane_actors(table["AU"]) == ("user", "admin")
    assert FL.lane_actors(table["UU"]) == ("user", FL.SECOND_BROWSER)


# --- check_prep ----------------------------------------------------------------------------------------------------------------

def test_check_prep_cases_clean_with_the_package_validate_plan(story):
    if not PACKAGE_SCRIPTS.is_dir():
        pytest.skip("the package worktree is not on this machine")
    generated(story)
    n, problems = CP.check_cases(story, scripts_dir=PACKAGE_SCRIPTS)
    assert (n, problems) == (23, [])


def test_check_prep_missing_case_exit_1_naming_it(story, capsys):
    target, _ = generated(story)
    (target / "LOCAL-1_TC_110.md").unlink()
    code = CP.main(["--task-root", str(story), "--stage", "cases", "--no-validate"])
    out = capsys.readouterr().out
    assert code == 1 and "LOCAL-1_TC_110" in out and "missing" in out


def test_check_prep_bad_oracle_word_exit_1_naming_it(story, capsys):
    target, _ = generated(story)
    path = target / "LOCAL-1_TC_103.md"
    path.write_text(path.read_text(encoding="utf-8").replace('"source": "person"', '"source": "my-opinion"', 1), encoding="utf-8")
    code = CP.main(["--task-root", str(story), "--stage", "cases", "--no-validate"])
    out = capsys.readouterr().out
    assert code == 1 and "LOCAL-1_TC_103" in out and "my-opinion" in out


def test_check_prep_unvalidated_is_not_a_silent_pass(story, capsys):
    generated(story)
    code = CP.main(["--task-root", str(story), "--stage", "cases"])
    assert code == 1 and "validate_plan was not run" in capsys.readouterr().out


def test_check_prep_covers_join_broken_is_named(story):
    generated(story)
    plan_path = story / "work" / "test-plan.json"
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    row = next(r for r in plan["rows"] if r["id"] == "TS-101")
    row["coverage_obligations"][0]["requirement_refs"] = [{"ref": "R-14", "revision": "r1"}]
    plan_path.write_text(json.dumps(plan), encoding="utf-8")
    _, problems = CP.check_cases(story, validate=False)
    assert any("LOCAL-1_TC_101" in p and "meets no requirement_refs" in p for p in problems)


class _Refused(ValueError):
    def __init__(self, text, walkable=False):
        super().__init__(text)
        self.walkable = walkable


class _FakeME:
    Refused = _Refused

    @staticmethod
    def _case_obligation_mapping(task, rows, case):
        return {"OB-" + case[-3:]}

    @staticmethod
    def prepare_request(task, case, ids):
        if case.endswith("102"):
            raise _Refused("expectation unconfirmed")
        if case.endswith("103"):
            raise _Refused("evidence rule is not one word", walkable=True)
        if case.endswith("104"):
            raise KeyError("boom")
        return {}


def test_check_ready_counts_prepared_refused_unprepared(tmp_path):
    got = CP.check_ready(tmp_path, [f"LOCAL-1_TC_10{i}" for i in range(1, 6)], _FakeME, None, lambda t: [])
    assert len(got["prepared"]) == 2
    assert [c for c, _ in got["refused"]] == ["LOCAL-1_TC_102", "LOCAL-1_TC_104"]
    assert [c for c, _ in got["unprepared"]] == ["LOCAL-1_TC_103"]
    assert "KeyError" in got["refused"][1][1]


# --- claim_check ---------------------------------------------------------------------------------------------------------------

def dispatch(walk, walls, costs, per_wall, cost):
    return {"walk": walk, "items": len(walls), "wall_s": per_wall * len(walls) if isinstance(per_wall, (int, float)) else per_wall,
            "per_item_wall_s": per_wall, "cost_usd": cost,
            "rows": [{"item": f"{walk}-i{i}", "index": i - 1, "wall_s": w, "cost_usd": c} for i, (w, c) in enumerate(zip(walls, costs), 1)]}


def timing(*dispatches):
    return {"task": "LOCAL-1", "timed": True, "dispatches": list(dispatches), "places": {}, "conductor_cost_usd": 1.0, "problems": []}


def test_claim_check_holds():
    t = timing(dispatch("W1", [100, 120, 140], [0.1, 0.1, 0.1], 120.0, 0.3), dispatch("W2", [150, 150, 150], [0.2, 0.2, 0.2], 150.0, 0.6))
    verdict, lines = CC.judge(t)
    assert verdict == "HOLDS"
    assert not any("$" in line for line in lines)


def test_claim_check_refused_by_a_third_index_item_over_the_limit():
    # medians are fine (120 s, $0.10); only the THIRD item of W1 is over 420 s
    t = timing(dispatch("W1", [100, 100, 500], [0.1, 0.1, 0.1], 120.0, 0.3), dispatch("W2", [100, 100, 100], [0.1, 0.1, 0.1], 100.0, 0.3))
    verdict, lines = CC.judge(t)
    assert verdict == "REFUSED" and any("item 3" in line for line in lines)
    # the same set with the over-limit item second is NOT refused by that rule
    t2 = timing(dispatch("W1", [100, 500, 100], [0.1, 0.1, 0.1], 120.0, 0.3))
    assert CC.judge(t2)[0] == "HOLDS"


def test_claim_check_refused_by_median_wall_and_by_median_cost():
    assert CC.judge(timing(dispatch("W1", [500, 500, 500], [0.1] * 3, 500.0, 0.3)))[0] == "REFUSED"
    assert CC.judge(timing(dispatch("W1", [100, 100, 100], [0.4] * 3, 100.0, 1.8)))[0] == "REFUSED"


def test_claim_check_not_measured_is_not_proved_never_holds():
    t = timing(dispatch("W1", [100, 100, 100], [0.1] * 3, 120.0, "not measured: the driver journal names no session of this dispatch"))
    verdict, lines = CC.judge(t)
    assert verdict == "NOT PROVED" and any("not measured" in line for line in lines)
    t = timing(dispatch("W1", [100, 100, "not measured: no transcript"], [0.1, 0.1, 0.1], 120.0, 0.3))
    assert CC.judge(t)[0] == "NOT PROVED"
    t = timing(dispatch("W1", [100, 100, 100], [0.1] * 3, None, 0.3))
    assert CC.judge(t)[0] == "NOT PROVED"
    assert CC.judge({"timed": False, "dispatches": []})[0] == "NOT PROVED"


def test_claim_check_cli_three_fixtures(tmp_path, capsys):
    files = {"refused": timing(dispatch("W1", [100, 100, 500], [0.1] * 3, 120.0, 0.3)),
             "notproved": timing(dispatch("W1", [100] * 3, [0.1] * 3, 120.0, "not measured: x")),
             "holds": timing(dispatch("W1", [100] * 3, [0.1] * 3, 120.0, 0.3))}
    codes = {}
    for name, doc in files.items():
        path = tmp_path / f"{name}.json"
        path.write_text(json.dumps(doc), encoding="utf-8")
        codes[name] = CC.main([str(path)])
    printed = capsys.readouterr().out
    assert codes == {"refused": 1, "notproved": 2, "holds": 0}
    assert printed.index("REFUSED") < printed.index("NOT PROVED") < printed.index("HOLDS")
    bad = tmp_path / "bad.json"
    bad.write_text("not json", encoding="utf-8")
    assert CC.main([str(bad)]) == 2


# --- check_run -----------------------------------------------------------------------------------------------------------------

def fake_run(task, pass_on=None, drop_end_probe=None, drop_case=None, with_stop=True):
    """A consistent fake of a finished walk: every case a record, probes, detector lines; silent/limited ones all inconclusive."""
    for c in DATA["cases"]:
        cid = MW.case_id(DATA["ticket"], c["card"])
        if cid == drop_case:
            continue
        n = CR.expected_thens(c)
        undecided = c.get("silent") or c.get("limited")
        thens = [{"n": i, "result": "inconclusive" if undecided else "pass", "quote": "", "capture": ""} for i in range(1, n + 1)]
        if pass_on == cid:
            thens[0]["result"] = "pass"
        record = {"walk": "W1", "item": cid, "attempt": "a1", "thens": thens, "limitation": "x" if c.get("limited") else ""}
        walk = task / "work" / "walks" / "W1"
        walk.mkdir(parents=True, exist_ok=True)
        (walk / f"{cid}.json").write_text(json.dumps(record), encoding="utf-8")
        adir = task / "work" / "evidence" / "manual" / cid / "a1"
        adir.mkdir(parents=True, exist_ok=True)
        probes = [{"when": "start"}] + ([] if drop_end_probe == cid else [{"when": "end"}])
        (adir / "probes.jsonl").write_text("".join(json.dumps(p) + "\n" for p in probes), encoding="utf-8")
        (adir / "surprises.jsonl").write_text(json.dumps({"line": "detector", "step": 1, "listeners": "ok"}) + "\n", encoding="utf-8")
    batches = task / "state" / "walks" / "W1" / "batches"
    batches.mkdir(parents=True, exist_ok=True)
    if with_stop:
        (batches / "LOCAL-1_TC_101-b1.json").write_text(json.dumps({"status": "stopped"}), encoding="utf-8")
        (batches / "LOCAL-1_TC_101-b2.json").write_text(json.dumps({"status": "done"}), encoding="utf-8")


def test_check_run_clean_fixture(tmp_path):
    fake_run(tmp_path)
    assert CR.check_run(tmp_path) == (23, [])


def test_check_run_reports_a_pass_on_a_silent_then(tmp_path, capsys):
    """The negative control of the DoD: a fixture with a `pass` on a silent Then makes check_run report it."""
    fake_run(tmp_path, pass_on="LOCAL-1_TC_104")
    found, problems = CR.check_run(tmp_path)
    assert found == 23 and any("LOCAL-1_TC_104" in p and "`pass`" in p and "silent" in p for p in problems)
    assert CR.main(["--task-root", str(tmp_path)]) == 1
    assert "LOCAL-1_TC_104" in capsys.readouterr().out


def test_check_run_reports_a_pass_on_a_limited_case(tmp_path):
    fake_run(tmp_path, pass_on="LOCAL-1_TC_114")
    assert any("LOCAL-1_TC_114" in p and "limited" in p for p in CR.check_run(tmp_path)[1])


def test_check_run_names_missing_record_missing_end_probe_and_no_stop(tmp_path):
    fake_run(tmp_path, drop_case="LOCAL-1_TC_107", drop_end_probe="LOCAL-1_TC_108", with_stop=False)
    found, problems = CR.check_run(tmp_path)
    text = "\n".join(problems)
    assert found == 22 and "LOCAL-1_TC_107: no result record" in text
    assert "LOCAL-1_TC_108/a1: no `end` probe" in text and "state/walks/*/batches" in text


# --- clean_driver_state --------------------------------------------------------------------------------------------------------

def test_clean_driver_state(tmp_path):
    state = tmp_path / "state"
    state.mkdir()
    doc = {"sessions": {"S6-qa-runner-5": "abc"}, "deferred": [1, 2], "deferred_seq": 2, "code_close": {"S7": 1}, "question_stop": 1,
           "s6_reproved": [], "s6_manual_runner": "x", "s6_probe_after": 1, "package_pass": True, "asked": ["q"]}
    raw = json.dumps(doc).encode("utf-8")
    (state / "driver-state.json").write_bytes(raw)
    code, words = CD.clean(tmp_path)
    after = json.loads((state / "driver-state.json").read_text(encoding="utf-8"))
    assert code == 0 and sorted(after) == ["asked", "sessions"] and "dropped 8" in words
    assert (state / "driver-state.before-walk.json").read_bytes() == raw          # byte copy
    CD.clean(tmp_path)                                                              # second run keeps the FIRST copy
    assert (state / "driver-state.before-walk.json").read_bytes() == raw


def test_clean_driver_state_absent_and_broken(tmp_path):
    assert CD.clean(tmp_path)[0] == 0
    (tmp_path / "state").mkdir()
    (tmp_path / "state" / "driver-state.json").write_text("[1]", encoding="utf-8")
    assert CD.clean(tmp_path)[0] == 1
    assert (tmp_path / "state" / "driver-state.json").read_text(encoding="utf-8") == "[1]"


# --- fallback_lane -------------------------------------------------------------------------------------------------------------

class _Args:
    def __init__(self, lane):
        self.lane, self.project, self.package, self.task = lane, "C:/p", "C:/pkg", "LOCAL-1"
        self.model, self.role_timeout, self.dry_run = "claude-sonnet-5-5", 10, True


def test_fallback_passes_its_own_pid_as_parent_pid(capsys):
    lane = FL.Lane(_Args("AU"), DATA)
    assert lane.run() == 0
    opens = [c for c in lane.log if "walk_session.py open" in c.replace("\\", "/")]
    assert len(opens) == 1
    assert f"--parent-pid {os.getpid()}" in opens[0]
    assert "--actor user --actor2 admin" in opens[0] and "--items LOCAL-1_TC_111,LOCAL-1_TC_113,LOCAL-1_TC_124" in opens[0]
    order = [next(i for i, c in enumerate(lane.log) if key in c.replace("\\", "/")) for key in
             ("story_step.py start", "walk_session.py open", "brief_pack.py", "--agent qa-factory:qa-runner", "walk_session.py close", "--operation checkpoint")]
    assert order == sorted(order)
    assert "--execution-kind manual" in lane.log[0] and "--stage S6" in lane.log[0]
    assert "password" not in " ".join(lane.log).lower()


def test_fallback_list_prints_eight_lanes(capsys):
    assert FL.main(["--list"]) == 0
    assert len([l for l in capsys.readouterr().out.splitlines() if l.strip()]) == 8
