"""SS1-13: a LOCAL story started with no change to ground on is the person's question at S0, before the scout (t-526 section 5, t-508 N3).

The owner's words (31.10.2026): a real ticket with no merge request link - the scout looks itself, no question. So the question is
asked ONLY for a local story (`local_keys.is_local`) with no `--mr`/`--branch`/`--commit`/`--ungrounded`, no answer already kept in
`launch`, and a `work/ticket-references.json` that is readable and names no merge or pull request (`ticket_light.change_kinds`, the
table's `is_change`). Proven here: the condition in both directions, its error directions (a file absent or unreadable, a table that
cannot be read: no question), the four answers and where each lands (`launch`, the scout's line, `pipeline.json`, its warning), a
restart without an answer asking again (the call stands OUTSIDE `if not kept`), a second entry after the answer asking nothing, and the
skill path's door (`story_step._halt_doors`, M8).

Mutations (each killed by THIS file): the call moved after `s0_rest` (the stub-scout/pipeline check: the question must stand before
`pipeline.json`); condition 1 removed (the `--mr`/`launch` rows); condition 2 removed (the merge-request row); "no file" read as "no
references" (the absent-file row); `change` kinds a literal list in the driver (the temp-table row); condition 3 removed or widened to
every ticket (the real-ticket rows); `code_repos` ignored (the no-repository row); the `role_lines` line removed (the scout-line row);
the `launch` check removed (the second-entry row); the call put inside `if not kept` (the restart row); `_halt_doors` always printing
the door, or never (the four manifest rows); the `is_change` bool check removed (the table row).
"""
import io
import json
import sys
import types
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_in, check_not_in  # noqa: E402
from story_run_common import (  # noqa: E402
    FIXTURE_TICKET,
    driver_for,
    eq as check_eq,
    rules_broken,
    run_scenarios,
    s0_answer,
    s0_pipeline,
    s0_project,
    s0_question,
    s0_run,
    s0_state,
    stub_calls,
)

sys.path.insert(0, str(harness.SCRIPTS))
import ticket_light as TL  # noqa: E402

KEY = "LOCAL-1"
REPOS = {"code_repos": [{"name": "app", "path": "app"}]}
MR_LINK = "https://git.example.com/group/proj/-/merge_requests/12"


def local_project(**config):
    """A project for a local story: its text file `qa-factory/local-tickets/LOCAL-1.md` (the fact `is_local` reads)."""
    root, task_root, env = s0_project(KEY, config=config or None)
    folder = root / "qa-factory" / "local-tickets"
    folder.mkdir(parents=True)
    (folder / f"{KEY}.md").write_text(FIXTURE_TICKET, encoding="utf-8")
    return root, task_root, env


def references(task_root: Path, rows) -> None:
    work = task_root / "work"
    work.mkdir(parents=True, exist_ok=True)
    (work / "ticket-references.json").write_text(json.dumps({"schema_version": 1, "ticket": KEY, "rows": rows}), encoding="utf-8")


def flags_of(driver, **more) -> dict:
    return dict(driver.s0_flags(), **more)


def asks(driver, flags=None) -> bool:
    """Does `s0_no_change_entry` raise the question? (the question is a `Person` and the block is stored)"""
    import story_run
    try:
        with redirect_stdout(io.StringIO()):
            driver.s0_no_change_entry(flags if flags is not None else driver.s0_flags())
    except story_run.Person:
        return driver.state.get("s0_block") == "no_change"
    return False


def the_condition() -> None:
    """Condition 1, 2 and 3 in both directions, and the directions of error (t-526 section 5)."""
    root, task_root, env = local_project(**REPOS)
    try:
        harness.use_project(root)
        driver = driver_for(root, env, KEY)
        references(task_root, [{"ref": "https://tracker.example.com/browse/PROJ-9", "kind": "ticket", "origins": ["mention:description"]}])
        check_eq("a local story, no flags, no change in its references: asked", asks(driver), True)
        driver.state.pop("s0_block", None)
        driver.state.pop("s0_ask", None)
        for name in ("mr", "branch", "commit"):
            check_eq(f"condition 1: --{name} given: no question", asks(driver, flags_of(driver, **{name: "x"})), False)
        check_eq("condition 1: --ungrounded given: no question", asks(driver, flags_of(driver, ungrounded=True)), False)
        check_eq("condition 1: an answer already kept in launch: no question",
                 asks(driver, flags_of(driver, implementation_source="current-code")), False)
        # condition 2: the references
        for kind in ("merge_request", "pull_request"):
            references(task_root, [{"ref": MR_LINK, "kind": kind, "origins": ["mention:description"]}])
            check_eq(f"condition 2: a {kind} row: no question (the diff is read)", asks(driver), False)
        for kind in ("gitlab_issue", "url", "confluence"):
            references(task_root, [{"ref": "https://x.example.com/p", "kind": kind, "origins": ["mention:description"]}])
            check_eq(f"condition 2: a {kind} row is no change: asked", asks(driver), True)
            driver.state.pop("s0_block", None)
            driver.state.pop("s0_ask", None)
        references(task_root, [])
        check_eq("condition 2: an empty list of rows: asked", asks(driver), True)
        driver.state.pop("s0_block", None)
        driver.state.pop("s0_ask", None)
        # the error direction of condition 2: not readable means no question
        (task_root / "work" / "ticket-references.json").unlink()
        check_eq("ERROR DIRECTION: no references file: no question (mutation: absent read as no references)", asks(driver), False)
        (task_root / "work" / "ticket-references.json").write_text("{ not json", encoding="utf-8")
        check_eq("ERROR DIRECTION: a file that is not JSON: no question", asks(driver), False)
        (task_root / "work" / "ticket-references.json").write_text(json.dumps({"rows": "none"}), encoding="utf-8")
        check_eq("ERROR DIRECTION: rows that are not a list: no question", asks(driver), False)
        references(task_root, [])
        real = TL.change_kinds

        def damaged(*_a, **_k):
            raise TL.TableError("reference-kinds.json: damaged")
        TL.change_kinds = damaged
        try:
            check_eq("ERROR DIRECTION: the kinds table cannot be read: no question", asks(driver), False)
        finally:
            TL.change_kinds = real
        check_eq("and the table read again: asked", asks(driver), True)
    finally:
        harness.cleanup(root)


def the_table_is_the_reader() -> None:
    """`is_change` is read from the table, never a list in the driver (AR-1): a kind the table marks is a change, one it does not mark is not."""
    root, task_root, env = local_project(**REPOS)
    try:
        harness.use_project(root)
        driver = driver_for(root, env, KEY)
        shipped = TL.change_kinds()
        check_eq("the shipped table: merge_request and pull_request, nothing else", shipped, {"merge_request", "pull_request"})
        table = json.loads(TL.KINDS_TABLE_PATH.read_text(encoding="utf-8"))
        for entry in table["kinds"]:
            entry.pop("is_change", None)
            if entry["kind"] == "url" or entry["kind"] == "confluence":
                entry["is_change"] = True
        marked = root / "marked-kinds.json"
        marked.write_text(json.dumps(table), encoding="utf-8")
        check_eq("a table without the field on merge_request: it is no change", TL.change_kinds(marked), {"confluence"})
        saved = TL.KINDS_TABLE_PATH
        TL.KINDS_TABLE_PATH = marked
        try:
            references(task_root, [{"ref": MR_LINK, "kind": "merge_request", "origins": ["x"]}])
            check_eq("the driver reads the table: a merge_request row of a table that does not mark it is asked (mutation: a literal list)",
                     asks(driver), True)
            driver.state.pop("s0_block", None)
            driver.state.pop("s0_ask", None)
            references(task_root, [{"ref": "https://x.example.com/p", "kind": "confluence", "origins": ["x"]}])
            check_eq("and a kind the table marks stops the question", asks(driver), False)
        finally:
            TL.KINDS_TABLE_PATH = saved
        bad = json.loads(TL.KINDS_TABLE_PATH.read_text(encoding="utf-8"))
        bad["kinds"][1]["is_change"] = "yes"
        raised = ""
        try:
            TL.check_reference_kinds(bad)
        except TL.TableError as exc:
            raised = str(exc)
        check_in("`is_change: \"yes\"` is refused by name (mutation: the bool check removed)", "merge_request", raised)
        check_in("... and says what it must be", "true or false", raised)
        absent_ok = json.loads(TL.KINDS_TABLE_PATH.read_text(encoding="utf-8"))
        absent_ok["kinds"][0].pop("is_change", None)
        check_eq("a kind without the field is accepted", bool(TL.check_reference_kinds(absent_ok)), True)
    finally:
        harness.cleanup(root)


def only_a_local_story() -> None:
    """Condition 3: ONLY a local story. A real ticket with no flags goes the old road (owner, 31.10.2026)."""
    for task, why in (("PROJ-1", "a real ticket"), ("LOCAL-5", "a LOCAL-shaped key with no text file and no mark")):
        root, task_root, env = s0_project(task)
        try:
            harness.use_project(root)
            driver = driver_for(root, env, task)
            references(task_root, [])
            check_eq(f"{why} with no flags and no change in its text: no question (mutation: condition 3 removed)", asks(driver), False)
        finally:
            harness.cleanup(root)


def the_question_and_its_options() -> None:
    """The text and the doors, with and without a code repository."""
    root, task_root, env = local_project(**REPOS)
    try:
        harness.use_project(root)
        driver = driver_for(root, env, KEY)
        references(task_root, [])
        check_eq("asked", asks(driver), True)
        ask = driver.state["s0_ask"]
        text = ask["text"]
        check_in("the question names the story", KEY, text)
        for token in ("current code", "change", "ungrounded", "stop"):
            check_in(f"the answer `{token}` is offered", f"`{token}`", text)
        check_in("`current code` carries the label", "Recommended", text)
        check_in("... and says what it shows", "never as the expected value", text)
        check_eq("the doors", sorted(ask["doors"]), ["change", "current code", "stop", "ungrounded"])
        check_in("the prices of the question are read (what current code leaves unverified)", "new behaviour, which the code in place cannot show", text)
    finally:
        harness.cleanup(root)
    root, task_root, env = local_project()
    try:
        harness.use_project(root)
        driver = driver_for(root, env, KEY)
        references(task_root, [])
        check_eq("no code repository: still asked", asks(driver), True)
        ask = driver.state["s0_ask"]
        check_not_in("no code repository: no `current code` answer (mutation: always offered)", "`current code`", ask["text"])
        check_not_in("... and it is no door", "current code", " ".join(ask["doors"]))
        check_in("... the text says why", "no code repository", ask["text"])
        check_eq("... the other three answers stand", sorted(ask["doors"]), ["change", "stop", "ungrounded"])
    finally:
        harness.cleanup(root)
    root, task_root, env = local_project()
    try:
        out = s0_run(root, env, KEY)
        check_eq("no code repository, a driver process: the stop (exit 3)", out.returncode, 3, out.stdout[-600:])
        shown = s0_question(task_root)
        check_in("... the file says there is no repository", "no code repository", shown)
        check_not_in("... and offers no `current code`", "`current code`", shown)
        check_eq("... and the file obeys human-questions.md", rules_broken(shown), [])
    finally:
        harness.cleanup(root)


def the_answers_end_to_end() -> None:
    """Driver processes: the stop before the scout, then each answer where it lands."""
    root, task_root, env = local_project(**REPOS)
    try:
        out = s0_run(root, env, KEY)
        check_eq("a local story with no change: the stop is exit 3", out.returncode, 3, out.stdout[-900:] + out.stderr[-500:])
        check_eq("the block is remembered", s0_state(task_root).get("s0_block"), "no_change")
        question = s0_question(task_root)
        check_in("the question is the no-change one", "No merge request, branch or commit was given", question)
        check_eq("the question file obeys human-questions.md (the label, the prices, the answer block)", rules_broken(question), [])
        check_eq("the stop stands before the story is written as started: no pipeline.json (mutation: the call after s0_rest)",
                 (task_root / "pipeline.json").exists(), False)
        check_eq("no scout or conductor was called", stub_calls(root), [])
        # a restart with no answer asks again: the snapshot is kept now, and the call is outside `if not kept`
        again = s0_run(root, env, KEY)
        check_eq("a restart with no answer: the same stop (mutation: the call inside `if not kept`)", (again.returncode, s0_state(task_root).get("s0_block")),
                 (3, "no_change"))
        # `change`: the command is printed and the question held
        held = s0_answer(root, env, KEY, "change")
        check_eq("`change`: the question is held (exit 3)", held.returncode, 3, held.stdout[-900:])
        shown = s0_question(task_root)
        check_in("... with the start-again command naming the three flags (mutation: the branch removed)", "--mr <link>, --branch <name> or --commit <sha>", shown)
        check_not_in("... and it is not the unread-answer lead", "is not one of the answers this question takes", shown)
        check_in("... and the question itself is still there", "No merge request, branch or commit was given", shown)
        check_eq("... still no pipeline.json", (task_root / "pipeline.json").exists(), False)
        check_eq("... nobody was called", stub_calls(root), [])
        # `current code`
        done = s0_answer(root, env, KEY, "current code")
        check_eq("`current code`: S0 goes on and ends (exit 0)", done.returncode, 0, done.stdout[-1200:] + done.stderr[-600:])
        pipeline = s0_pipeline(task_root)
        check_eq("pipeline.json carries implementation_source (mutation: s0_rest ignores launch)", pipeline.get("implementation_source"), "current-code")
        warnings = pipeline.get("warnings") or []
        check("... and the warning of the record", any(w.startswith("no change to ground on: tests are grounded on the current code") for w in warnings), str(warnings))
        check_eq("launch keeps the answer", (s0_state(task_root).get("launch") or {}).get("implementation_source"), "current-code")
        harness.use_project(root)
        driver = driver_for(root, env, KEY)
        lines = driver.role_lines("S1", "qa-scout")
        check("the scout is told BEFORE its work (mutation: the role_lines line removed)", "implementation_source: current-code" in lines, str(lines))
        check_eq("... and the launch flags line says none", lines[0], "Launch flags: none")
        # the second entry asks nothing
        check_eq("the entry after the answer asks nothing (mutation: the launch check removed)", asks(driver), False)
        check_eq("S0 is not asked again from the story's own record: no block left", s0_state(task_root).get("s0_block"), None)
    finally:
        harness.cleanup(root)
    root, task_root, env = local_project(**REPOS)
    try:
        s0_run(root, env, KEY)
        done = s0_answer(root, env, KEY, "ungrounded")
        check_eq("`ungrounded`: S0 goes on (exit 0)", done.returncode, 0, done.stdout[-1200:] + done.stderr[-600:])
        check_eq("launch.ungrounded is kept", (s0_state(task_root).get("launch") or {}).get("ungrounded"), True)
        check_eq("pipeline.json: no implementation_source of its own (the scout and gate B carry ungrounded)",
                 s0_pipeline(task_root).get("implementation_source"), None)
        harness.use_project(root)
        driver = driver_for(root, env, KEY)
        lines = driver.role_lines("S1", "qa-scout")
        check_eq("the scout's launch flags line carries --ungrounded", lines[0], "Launch flags: --ungrounded")
        check_not_in("... and no current-code line", "implementation_source:", " ".join(lines))
    finally:
        harness.cleanup(root)
    root, task_root, env = local_project(**REPOS)
    try:
        s0_run(root, env, KEY)
        held = s0_answer(root, env, KEY, "stop")
        check_eq("`stop`: held, exit 3", held.returncode, 3)
        check_in("... with the stop text", "You said to stop", s0_question(task_root))
        check_eq("... nothing was called", stub_calls(root), [])
    finally:
        harness.cleanup(root)


def the_change_door_keeps_the_restart_flag() -> None:
    """t-586 F-1, real processes: the `--mr` / `--commit` of the restart the `change` door prints is kept in `launch` by an
    entry that is NOT the first, so a later process with no flags still sees it (no `Launch flags: none`, no second question);
    a restart with no flags keeps asking."""
    for flag, value in (("--mr", "https://git.example/g/p/-/merge_requests/7"), ("--commit", "abc1234")):
        root, task_root, env = local_project(**REPOS)
        try:
            s0_run(root, env, KEY)
            s0_answer(root, env, KEY, "change")
            check_eq(f"{flag}: before the restart launch holds no such word", (s0_state(task_root).get("launch") or {}).get(flag[2:]), None)
            s0_run(root, env, KEY, flag, value)
            kept = (s0_state(task_root).get("launch") or {}).get(flag[2:])
            check_eq(f"{flag}: the restart's word is kept in launch (mutation: s0_keep_late_launch removed)", kept, value)
            check("... and the question is not the no-change one", s0_state(task_root).get("s0_block") != "no_change", str(s0_state(task_root).get("s0_block")))
            harness.use_project(root)
            driver = driver_for(root, env, KEY)
            check_eq(f"{flag}: a later driver with no flags reads it", driver.launch_flags().get(flag[2:]), value)
            check_in(f"{flag}: the scout's line names it", flag, driver.role_lines("S1", "qa-scout")[0])
        finally:
            harness.cleanup(root)
    root, task_root, env = local_project(**REPOS)
    try:
        s0_run(root, env, KEY)
        s0_answer(root, env, KEY, "change")
        again = s0_run(root, env, KEY)
        check_eq("a restart with no flags keeps asking", (again.returncode, s0_state(task_root).get("s0_block")), (3, "no_change"))
    finally:
        harness.cleanup(root)


def a_real_ticket_goes_the_old_road() -> None:
    """The owner's rule end to end: a tracker key with no flags is not asked; S0 ends and the scout's cascade is left to look."""
    root, task_root, env = s0_project("PROJ-1", config=REPOS)
    try:
        out = s0_run(root, env, "PROJ-1")
        check_eq("a real ticket, no flags: S0 ends (exit 0)", out.returncode, 0, out.stdout[-900:] + out.stderr[-500:])
        check("... and the block is not the no-change one", s0_state(task_root).get("s0_block") != "no_change")
        check_eq("... and implementation_source stays for the scout to find", s0_pipeline(task_root).get("implementation_source"), None)
    finally:
        harness.cleanup(root)


def the_skill_path_door() -> None:
    """M8: the door of `story_step._halt_doors` at an S1 halt on `implementation.source: none`; none when the manifest says otherwise."""
    import story_step
    root = Path(harness.temp_project("qa-no-mr-door-"))
    try:
        task_root = root / "qa-factory" / "artifacts" / "LOCAL-1"
        (task_root / "work").mkdir(parents=True)
        args = types.SimpleNamespace(task="LOCAL-1", dispatch_id="S1-qa-scout-1")
        dispatch = {"id": "S1-qa-scout-1", "stage": "S1", "role": "qa-scout", "status": "running", "agent_id": "AG-1"}
        manifest = task_root / "work" / "context-manifest.json"

        def doors(stage="S1", written=None):
            if written is not None:
                manifest.write_text(written, encoding="utf-8")
            return story_step._halt_doors(args, task_root, dict(dispatch, stage=stage), False)
        door = "stage_done.py --task LOCAL-1 --set implementation_source=<current-code|ungrounded>"
        resume = "story_step.py resume --task LOCAL-1 --dispatch-id S1-qa-scout-1"
        absent = doors()
        check_not_in("no manifest: no door (mutation: always printed)", "implementation_source", absent)
        for label, body in (("implementation.source", {"implementation": {"source": "none"}}),
                            ("implementations[0].source", {"implementations": [{"source": "none"}]}),
                            ("implementation_source", {"implementation_source": "none"})):
            text = doors(written=json.dumps(body))
            check_in(f"{label}: none -> the door", door, text)
            check_in(f"{label}: none -> the resume", resume, text)
            check_in(f"{label}: none -> the value is said in the message", "SendMessage", text)
            check_in(f"{label}: none -> the old road still stands (nothing is closed)", "--operation recover", text)
        check_not_in("a diff was found: no door (mutation: the condition removed)", "implementation_source",
                     doors(written=json.dumps({"implementation": {"source": "diff"}})))
        check_not_in("a manifest that is not JSON: no door", "implementation_source", doors(written="{ nope"))
        check_not_in("a manifest that is a list: no door", "implementation_source", doors(written="[]"))
        check_not_in("another stage with `none`: no door", "implementation_source",
                     doors(stage="S2", written=json.dumps({"implementation": {"source": "none"}})))
    finally:
        harness.cleanup(root)


def the_twins_say_the_same() -> None:
    """AR-19: the skill's twin of the driver (`phases/s1.md`) and the role's text (`agents/qa-scout.md`) carry the same rule."""
    s1 = (harness.PLUGIN_ROOT / "skills" / "qa-story" / "phases" / "s1.md").read_text(encoding="utf-8")
    check_in("s1.md: the question before the dispatch for a local story", "A real ticket is never asked first", s1)
    check_in("s1.md: the scout's prompt line", "implementation_source: current-code", s1)
    scout = (harness.PLUGIN_ROOT / "agents" / "qa-scout.md").read_text(encoding="utf-8")
    check_in("qa-scout.md step 4: not halting when current-code is in the dispatch", "no `implementation_source: current-code` in the dispatch", scout)
    # spec t-1765 X1 (B-D, register outcome "dropped" - for the critic): "step 6" and "Refusals" of the old procedure are gone; the
    # rule is held by the pin above and by s1.md (the twin). The charter's halt sentence is the carrier that replaced them.
    check_in("qa-scout.md When to ask: the halt is for absent data only", "Stop (`halt`) only when the data is absent", scout)
    prices = json.loads((harness.PLUGIN_ROOT / "references" / "question-prices.json").read_text(encoding="utf-8"))
    rows = prices["questions"].get("s0.no_change") or []
    check_eq("the prices: three answers and stop", [r["answer"] for r in rows], ["current code", "change", "ungrounded", "stop"])


def main():
    the_twins_say_the_same()
    run_scenarios([the_answers_end_to_end, a_real_ticket_goes_the_old_road],
                  [the_change_door_keeps_the_restart_flag, the_condition, the_table_is_the_reader, only_a_local_story, the_question_and_its_options, the_skill_path_door])
    harness.finish("no-MR entry (SS1-13)")


if __name__ == "__main__":
    main()
