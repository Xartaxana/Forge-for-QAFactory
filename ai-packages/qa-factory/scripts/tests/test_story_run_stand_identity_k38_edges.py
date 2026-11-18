#!/usr/bin/env python3
"""k38 edges: a part of test_story_run_stand_identity.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_run_stand_identity_common."""
import contextlib
import io
import json
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_in, check_not_in  # noqa: E402
from story_run_common import run_scenarios, d2_enter, eq, human_broken, s0_question
from story_run_stand_identity_common import (  # noqa: E402
    HEAD, OLD, Rig, asked, driver_stub, flag, line_broken, matched, mismatched, run_entry, sources_mismatched,
    unknown, use_plan,
)


    # the source-order check (build_check follows stand_check at every site) and the F5 console-line check over the region of
    # `build_check` were source pins of named members: deleted by TD-11 phase 0 (F3)

# --- K38 / K39 / K40 / K44 -------------------------------------------------------------------------------------------

def k38_the_confirm_variant() -> None:
    rig = Rig(profiles=("api",), real=True)
    try:
        use_plan({"TC-1": ("api", "automate")})
        rig.put_row("person_confirms")
        date = rig.rows()[0]["recorded_at"][:10]
        code, out, started, _ = run_entry(rig, s5=("TC-1",))
        eq("K38 a person_confirms stand with no word for this story: the `confirm` question (exit 3)", (code, flag(rig).get("variant")), (3, "confirm"))
        text = s0_question(rig.task_root)
        check_in("K38 it names the decision date", f"your decision of {date}", text)
        check_in("K38 it names the registry file", "qa-factory/records/stand-identity.json", text)
        check_in("K38 it says nothing was read (the person checks it)", "you check the build yourself", text)
        check_not_in("K38 CONTROL: the `how` question does not say it", "you check the build yourself", persons_how(rig))
        code, out, started, _ = run_entry(rig, "deployed", s5=("TC-1",))
        eq("K38 `deployed` takes the word for this story and the stage goes on", (code, [r["kind"] for r in rig.confirmations()]), (0, ["deployed"]))
        # the stand's definition moved since the decision: the decision no longer counts - `voided`, asked as a how-question
        cfg = json.loads(rig.config_path.read_text(encoding="utf-8"))
        cfg["environments"][0]["base_url"] = "http://localhost:9999"
        rig.config_path.write_text(json.dumps(cfg), encoding="utf-8")
        code, out, started, _ = run_entry(rig, s5=("TC-1",))
        eq("K38 a stand whose address changed since the decision: asked again (exit 3)", code, 3)
        check_in("K38 ... with the voided text", f"You confirmed it on {date}; since then the stand's settings changed", s0_question(rig.task_root))
    finally:
        rig.done()


def persons_how(rig) -> str:
    driver = rig.driver()[0]
    return driver.build_person("S5", "", "localhost", "api", unknown("api"), None, "how").text


def k39_what_is_a_line_and_not_a_question() -> None:
    rig = Rig(profiles=("api",), timeout=2)
    try:
        use_plan({"TC-1": ("api", "automate")})
        # mismatched IS a question (the amendment); the others are one printed line each and the role starts
        rig.records(api=mismatched("api"))
        code, out, started, _ = run_entry(rig, s5=("TC-1",))
        eq("K39 `mismatched` at entry is a question (variant mismatched), no role", (code, flag(rig).get("variant"), started), (3, "mismatched", []))
        rig.records(api=sources_mismatched("api", ["a.ts"]))
        code, out, started, _ = run_entry(rig, s5=("TC-1",))
        eq("K39 a sources mismatch is a question too (variant mismatched_sources)", (code, flag(rig).get("variant")), (3, "mismatched_sources"))
        for label, record_, needle in (
                ("docker down (unknown, nobody to ask)", unknown("api", asks=None, error="which build the stand runs could not be read: docker did not answer (Cannot connect)"), "I could not read which build stand `localhost` runs"),
                ("the probe exits with an error", "__fail__", "the check stopped with an error"),
                ("the probe prints no JSON", "__nojson__", "the check printed no readable answer"),
                ("the probe does not finish in time", "__hang__", "the check did not finish in time"),
                ("a result word the factory does not know", dict(matched("api"), result="MATCHED"), "was not one I know"),
                ("a matched record that proves nothing (no technical verification)", dict(matched("api"), provenance={"technical_verification": False}), "was not one I know")):
            rig.records(api=record_)
            asked(rig)
            code, out, started, _ = run_entry(rig, s5=("TC-1",))
            lines = [ln for ln in out.splitlines() if "stand `localhost`" in ln and ln.startswith("S5:")]
            eq(f"K39 {label}: no question (exit 0), the role starts", (code, ("S5", "qa-automator") in started), (0, True))
            check_in(f"K39 {label}: ONE printed line says so", needle, "\n".join(lines))
            eq(f"K39 {label}: exactly one such line", len(lines), 1)
            eq(f"K39 {label}: the line obeys human-questions.md", line_broken(lines[0]) if lines else ["no line"], [])
            check(f"K39 {label}: and it is not a question (nothing open, no packet)", not asked(rig) and not flag(rig), str(asked(rig)))
        # a check that breaks inside the driver is a line and the run goes on (P1: code informs, it does not stop the factory)
        rig.records(api=matched("api"))
        built = rig.driver(s5=("TC-1",))

        def broken(*_args, **_kw):
            raise KeyError("slot")
        built[0].build_outcome = broken
        code, out, started, _ = run_entry(rig, built=built)
        eq("K39 a check that BREAKS is a line, not a crash: the role starts (exit 0)", (code, ("S5", "qa-automator") in started), (0, True))
        check_in("K39 ... and the line (data) says it could not be checked and that nothing is asked, with no exception name in it",
                 "the build of stand `localhost` for the api tests could not be checked; nothing is asked of you", out)
        check_not_in("K39 (t-366 F5) ... the exception's name is not on the console", "KeyError", out)
        errors = io.StringIO()
        built = rig.driver(s5=("TC-1",))
        built[0].build_outcome = broken
        with contextlib.redirect_stderr(errors):
            run_entry(rig, built=built)
        check_in("K39 (t-366 F5) ... the raw error text goes to stderr", "KeyError", errors.getvalue())
        # no registered probe (E21): a line, no question
        cfg = json.loads(rig.config_path.read_text(encoding="utf-8"))
        cfg["execution"]["runtime_probes"] = {}
        rig.config_path.write_text(json.dumps(cfg), encoding="utf-8")
        code, out, started, _ = run_entry(rig, s5=("TC-1",))
        check_in("K39 no probe registered: one line, no question, the role starts", "no way to read the build of stand `localhost` is registered for the api tests", out)
        eq("K39 ... exit 0", (code, ("S5", "qa-automator") in started), (0, True))
    finally:
        rig.done()
    # docker down on a stand the person checks themselves: a STATUS line naming the word, never a question (FR-7)
    rig = Rig(profiles=("api",))
    try:
        use_plan({"TC-1": ("api", "automate")})
        rig.put_row("person_confirms")
        date = rig.rows()[0]["recorded_at"][:10]
        rig.records(api=unknown("api", asks=None, error="which build the stand runs could not be read: docker did not answer"))
        code, out, started, _ = run_entry(rig, s5=("TC-1",))
        eq("K39 docker down on a person_confirms stand: no question, the role starts", (code, ("S5", "qa-automator") in started, asked(rig)), (0, True, {}))
        check_in("K39 ... the status line says docker is down and whose word cannot be checked", f"docker is down on `localhost`; your word of {date} (you check the build yourself on this stand) cannot be checked now", out)
        eq("K39 ... and the line obeys the rules", line_broken([ln for ln in out.splitlines() if "docker is down" in ln][0]), [])
        # CONTROL: the same record on a stand with no such row is the plain unread line
        rig2 = Rig(profiles=("api",))
        try:
            use_plan({"TC-1": ("api", "automate")})
            rig2.records(api=unknown("api", asks=None, error="which build the stand runs could not be read: docker did not answer"))
            code, out2, started2, _ = run_entry(rig2, s5=("TC-1",))
            check_not_in("K39 CONTROL: with no person_confirms row the line does not speak of a word", "your word of", out2)
        finally:
            rig2.done()
    finally:
        rig.done()


def k40_one_question_per_profile() -> None:
    rig = Rig(profiles=("api", "e2e-ui"))
    try:
        use_plan({"TC-1": ("api", "automate"), "TC-2": ("e2e-ui", "manual-agent")})
        rig.records(api=unknown("api"), **{"e2e-ui": unknown("e2e-ui")})
        code, out, started, driver = run_entry(rig, stage="S6", auto=("TC-1",), manual=("TC-2",))
        eq("K40 S6 `both` with api and e2e-ui both unknown: ONE question (exit 3), no role", (code, started), (3, []))
        first = s0_question(rig.task_root)
        eq("K40 the first question names api only", (flag(rig).get("profile"), "api tests" in first, "e2e-ui" in first), ("api", True, False))
        check_in("K40 ... and says S6 will run both halves", "running the automated tests and carrying out the manual checks", first)
        eq("K40 ... only api was probed so far", sorted({c["profile"] for c in rig.calls()}), ["api"])
        # after its answer (api is read now), the next entry asks e2e-ui
        rig.records(api=matched("api"), **{"e2e-ui": unknown("e2e-ui")})
        code, out, started, driver = run_entry(rig, "retry", stage="S6", auto=("TC-1",), manual=("TC-2",))
        eq("K40 after the answer the next entry asks e2e-ui (exit 3)", (code, flag(rig).get("profile")), (3, "e2e-ui"))
        check_in("K40 ... the api line was printed first", "the api tests on stand `localhost`: the stand runs this story's build", out)
        check_not_in("K40 ... and the second question is not about api", "api tests", s0_question(rig.task_root).split("What I need")[0])
        # CONTROL: one unknown among matched asks exactly one question, and a matched pair asks none (K44)
        rig.records(api=matched("api"), **{"e2e-ui": matched("e2e-ui")})
        code, out, started, driver = run_entry(rig, stage="S6", auto=("TC-1",), manual=("TC-2",))
        eq("K40 CONTROL: both matched - no question", (code, asked(rig)), (0, {}))
    finally:
        rig.done()


def k44_a_labelled_stand_asks_nothing() -> None:
    rig = Rig(profiles=("api", "e2e-ui"))
    try:
        use_plan({"TC-1": ("api", "automate"), "TC-2": ("e2e-ui", "manual-agent")})
        rig.records(api=matched("api", kind="", linkage="verified_content"), **{"e2e-ui": matched("e2e-ui", kind="oci_label")})
        driver, started, steps, probes = rig.driver(auto=("TC-1",), manual=("TC-2",))
        driver_stub(driver)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = d2_enter(driver, "S6")
        lines = [ln for ln in out.getvalue().splitlines() if "stand `localhost`" in ln and ln.startswith("S6:")]
        eq("K44 e2e-ui labelled == HEAD, api matched by content: S6 entry asks nothing (exit 0)", (code, asked(rig), flag(rig)), (0, {}, {}))
        eq("K44 ... and prints exactly two lines, api then e2e-ui", len(lines), 2)
        check("K44 ... the api line says it was matched by the files; the e2e-ui line names the label, or says `the way it was read` when the rules of "
              "human-text.json (they move: t-363's `config_key`) would break on the label's dotted name",
              "the files inside the container" in lines[0] and ("(read by the label org.opencontainers.image.revision of the image)" in lines[1]
                                                                   or "(read by the way it was read)" in lines[1]), "\n".join(lines))
        check("K44 ... both obey the rules", all(line_broken(ln) == [] for ln in lines))
        eq("K44 ... the roles started (the run goes on)", ("S6", "manual") in started or ("S6", "qa-runner") in started, True)
        eq("K44 ... one probe per profile, no more", sorted(c["profile"] for c in rig.calls()), ["api", "e2e-ui"])
    finally:
        rig.done()


# --- the edges of the node spec -----------------------------------------------------------------------------------------

def edges_per_window_and_per_kind() -> None:
    import story_run
    rig = Rig(profiles=("api", "e2e-ui"))
    try:
        use_plan({"TC-1": ("api", "automate"), "TC-2": ("e2e-ui", "automate")})
        rig.records(api=matched("api"), **{"e2e-ui": unknown("e2e-ui")})
        windows = [{"scope": ["TC-1"], "accepted_by": {}}, {"scope": ["TC-2"], "accepted_by": {}}]
        built = rig.driver()
        built[0].stage_scope = lambda stage, kind="": {"scope": ["TC-1", "TC-2"], "windows": windows}
        code, out, started, _ = run_entry(rig, built=built)
        eq("EDGE per window: an api window is entered while e2e-ui is unknown: no question (an e2e-ui question never blocks an api-only window)", (code, asked(rig)), (0, {}))
        eq("EDGE per window: ... and only the window's own profile was probed", sorted({c["profile"] for c in rig.calls()}), ["api"])
        windows[0]["accepted_by"] = {"qa-code-critic": 1}       # the first window is accepted: the next one is entered
        built = rig.driver()
        built[0].stage_scope = lambda stage, kind="": {"scope": ["TC-1", "TC-2"], "windows": windows}
        code, out, started, _ = run_entry(rig, built=built)
        eq("EDGE per window: the next window (e2e-ui) asks about e2e-ui", (code, flag(rig).get("profile")), (3, "e2e-ui"))
    finally:
        rig.done()
    # S6 by kind: a manual-only S6 never asks about an automate-only profile
    rig = Rig(profiles=("api", "e2e-ui"))
    try:
        use_plan({"TC-1": ("api", "automate"), "TC-2": ("e2e-ui", "manual-agent")})
        rig.records(api=unknown("api"), **{"e2e-ui": matched("e2e-ui")})
        driver, started, steps, probes = rig.driver()
        driver.build_check("S6", "manual", cases=["TC-2"])
        eq("EDGE S6 manual: only the manual-agent profile is probed; the unknown api is not asked about", [c["profile"] for c in rig.calls()], ["e2e-ui"])
        try:
            driver.build_check("S6", "automation", cases=["TC-1"])
            check("EDGE S6 automation: the automate profile is asked about", False)
        except story_run.Person as person:
            eq("EDGE S6 automation: the automate profile is asked about", person.build_question["profile"], "api")
        # a profile the dispatch's scope does not hold is not asked about, whatever the kind says
        before = len(rig.calls())
        driver.build_check("S6", "", cases=["TC-2"])
        eq("EDGE S6 no kind (a dispatch of an older story): the DISPATCH's scope decides, never all", [c["profile"] for c in rig.calls()[before:]], ["e2e-ui"])
    finally:
        rig.done()


def edges_foreign_probe_and_data() -> None:
    # AE16: a project's own probe script is never handed a flag it does not know
    rig = Rig(profiles=("api",), foreign=True)
    try:
        use_plan({"TC-1": ("api", "automate")})
        rig.records(api=matched("api"))
        code, out, started, _ = run_entry(rig, s5=("TC-1",))
        argv = rig.calls()[0]["argv"]
        eq("EDGE AE16: a foreign probe script gets neither --no-evidence nor --task-root", ("--no-evidence" in argv, "--task-root" in argv), (False, False))
        eq("EDGE AE16: and what it printed is read by its fields all the same (a matched record that validates: a line, exit 0)", code, 0)
        check_in("EDGE AE16: ... the line", "the stand runs this story's build", out)
    finally:
        rig.done()
    import stand_identity as SI
    q = SI.data()["question"]
    for key, line in q["lines"].items():
        if key.startswith("why_"):
            continue
        text = line.format(stage="S5", stand="localhost", profile="api", method="the label x of the image", date="2026-10-03", error="the build could not be read",
                           why="the check did not finish in time", said="deployed",
                           files="`src/Page.vue`, `src/Other.vue` (and 2 more)")     # FB-8 N2 (68539227): `{files}` of two lines
        eq(f"EDGE data: the status line `{key}` obeys the rules", line_broken(text), [])
    partly = "\n".join(q["partly_recorded"]["text"]).format(stand="localhost", profile="api")
    eq("EDGE data (t-366 F2): the partly-recorded text obeys the rules", human_broken(partly), [])
    check("EDGE data (t-366 F2): it names what is written and what is not, and offers deployed / retry / stop, without a path or an exception",
          all(n in partly for n in ("is written", "is not written", "`deployed`", "`retry`", "`stop`"))
          and not any(bad in partly for bad in (".jsonl", ".json", "Error", "Traceback", "exit ")), partly)
    forms = SI.data()["answers"]["forms"]
    check("EDGE data (t-366 F3): every form that takes a value has its shape in the data, and it compiles",
          all(re.compile(str(spec["value"])) for spec in forms.values() if spec.get("arg") != "none") and
          all("value" in spec for spec in forms.values() if spec.get("arg") != "none"))
    for key, text in q["reasks"].items():
        sentence = text.format(form="file", needs="the path", example="file /x", sha="a" * 7, short=HEAD[:12], stand="localhost", deployed_short=OLD[:12])
        eq(f"EDGE data: the re-ask `{key}` obeys the rules", human_broken(sentence + "\n\nWhat I need from you is one of these:\n(a) answer `retry` once you have changed the stand, and I check again."), [])
    check("EDGE data: the held text obeys the rules too", human_broken(q["held"]["stop"].format(stand="localhost") + "\n\nWhat I need from you is one of these:\n(a) `retry`.") == [])


def fb8_matched_line_names_not_shipped() -> None:
    """FB-8 (R10N1, E13): a `matched` record that did not compare a build input the container does not ship SAYS so; the cap
    is 5 names (AT 5: all named, BEYOND at 6: five and "and 1 more"); an empty or absent list is the old `matched` line."""
    rig = Rig(profiles=("api",))
    try:
        driver = rig.driver()[0]
        names = [f"build/Makefile{n}" for n in range(1, 7)]

        def line_of(shipped):
            extra = {} if shipped is None else {"not_shipped_files": shipped}
            rec = dict(matched("api", kind="sources", linkage="verified_content"), **extra)
            text, person = driver.build_outcome("S5", "", "localhost", "api", rec, "")
            return text, person
        old, person = line_of(None)
        check_in("FB8 no list: the old matched line", "the stand runs this story's build (read by", old)
        check_not_in("FB8 no list: no not-compared words", "not compared", old)
        eq("FB8 empty list: the very same old line", line_of([])[0], old)
        five, person = line_of(names[:5])
        check_in("FB8 five files: the line says they were not compared, because they are not in the container",
                 "not compared, because they are not in the container: ", five)
        check("FB8 five files: all five named, no 'more'", all(f"`{n}`" in five for n in names[:5]) and "more" not in five, five)
        six, person = line_of(names)
        check("FB8 six files: five named and 'and 1 more'", f"`{names[4]}`" in six and f"`{names[5]}`" not in six
              and "and 1 more" in six, six)
        eq("FB8 it is a line, never a question", person, None)
        for text in (five, six):
            eq("FB8 the line obeys human-questions.md", line_broken(text), [])
        odd, person = line_of(["run_suite.py"])
        eq("FB8 a file name the question rules refuse (a script name) is said in the plain words, and the line still obeys the rules",
           (line_broken(odd), "run_suite.py" in odd, "some files of this story" in odd), ([], False, True))
    finally:
        rig.done()


def main() -> None:
    run_scenarios([], [
        k38_the_confirm_variant,
        k39_what_is_a_line_and_not_a_question,
        k40_one_question_per_profile,
        k44_a_labelled_stand_asks_nothing,
        edges_per_window_and_per_kind,
        edges_foreign_probe_and_data,
        fb8_matched_line_names_not_shipped,
    ])
    harness.finish("test_story_run_stand_identity_k38_edges")


# split: runner piece 1
if __name__ == "__main__":
    main()
