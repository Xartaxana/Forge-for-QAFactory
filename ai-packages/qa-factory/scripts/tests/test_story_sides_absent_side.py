"""absent side: a part of test_story_sides.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_sides_common."""
import contextlib
import io
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_eq  # noqa: E402
sys.path.insert(0, str(harness.SCRIPTS))
import contract  # noqa: E402
from story_sides_common import ABSENT, SUBSTITUTED, copy_registry  # noqa: E402


def absent_story(task, sides=("api",)):
    """t-2559 (W2 B3): a seeded story whose `sides` are absent and this story's own; the driver runs the hold's body (`_act_await_implementation`)
    and the hold is recorded by the real controller. Returns `(root, task_root, env, driver, person)`; `person` is the question raised."""
    import story_run
    from story_run_common import driver_for, seed
    root, task_root, env = seed(task)
    sets = [part for name in sides for attr, value in (("reality", ABSENT), ("deliverable", "true"), ("source", "person"))
            for part in ("--set", f"sides.{name}.{attr}={value}")]
    harness.run_script("stage_done.py", "--task", task, *sets, cwd=root, env=env)
    driver = driver_for(root, env, task)
    person = None
    with contextlib.redirect_stdout(io.StringIO()):
        try:
            driver._act_await_implementation({"action": "await_implementation", "cause": "s5_absent_side", "held_from": "S6", "sides": {}})
        except story_run.Person as raised:
            person = raised
    return root, task_root, env, driver, person


def answer_of(driver, root, words):
    """The person's answer taken by the real `take_answer` over the open question; returns what it printed."""
    driver.state["asked"] = {"kind": "absent_side", "stage": "S6", "dispatch": ""}
    driver.state.setdefault("pending_words", {})
    path = root / "answer-words.txt"
    path.write_text(words, encoding="utf-8")
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        driver.take_answer(path)
    return out.getvalue()


def pipeline_of(task_root):
    return json.loads((task_root / "pipeline.json").read_text(encoding="utf-8"))


def absent_side_cases():
    """t-2559 (W2 B3): the S5 hold for an absent side asks whose the side is. The owner's flow end to end, then the edges."""
    import project_knowledge as PK
    import story_run
    from story_run_common import s0_pipeline, s0_project, s0_run, s0_state
    # the owner's flow: parks, is asked, answers `not ours`, the row says deliverable false with the person's words, the hold is lifted
    root, task_root, env, driver, person = absent_story("QA-5")
    try:
        check_eq("B3: the hold is recorded and a closed question is raised over the side",
                 (person is not None and person.kind, bool(pipeline_of(task_root).get("awaiting")), driver.state.get("absent_side")),
                 ("absent_side", True, "api"))
        for needle in ("`api` does not exist yet", "waits for its code", "`not ours`", "`relaunch`", "stand-in"):
            check(f"B3: the question says {needle}", needle in str(person.text), str(person.text)[:400])
        words = "not ours\nthe api is the platform team's, test on mocks"
        said = answer_of(driver, root, words)
        record = pipeline_of(task_root)
        side = record["sides"]["api"]
        check_eq("B3: the story's side is substituted, not deliverable, by the person", (side["reality"], side["deliverable"], side["source"]),
                 (SUBSTITUTED, False, "person"))
        check_eq("B3: the hold is lifted and the story no longer parks", ("awaiting" in record, contract.parks_after_s5(record)), (False, False))
        row = PK.state(root, PK.SIDES_KEY, "", "api")["row"] or {}
        check_eq("B3: the registry row says deliverable false, with the person's words, by the driver",
                 (row.get("value"), (row.get("provenance") or {}).get("words"), (row.get("provenance") or {}).get("by"),
                  (row.get("provenance") or {}).get("source")),
                 ({"deliverable": False, "settles_by": ""}, words, "driver", "person"))
        check("B3: the person is told in words that the wait is over", "`api` is another team's at your word" in said, said[-300:])
        check_eq("B3: the answer left no open question and no kept side name", (driver.state.get("asked"), "absent_side" in driver.state), ({}, False))
        # a second story of the same project is not asked (the registry row is the project's)
        root2, task_root2, env2 = s0_project("PROJ-2", config={"code_repos": [{"name": "app", "path": "app"}]})
        try:
            copy_registry(root, root2)
            out = s0_run(root2, env2, "PROJ-2", "--side", "api=absent")
            entry = (s0_pipeline(task_root2).get("sides") or {}).get("api") or {}
            check_eq("B3: a second story of the project is not asked: no stop, the side is not deliverable (W2 (3))",
                     (out.returncode, s0_state(task_root2).get("s0_block"), entry.get("deliverable"), entry.get("reality")),
                     (0, None, False, ABSENT))
        finally:
            harness.cleanup(root2)
        # a later word `it is ours` overwrites it, and the history is kept (W2)
        PK.record(root, key=PK.SIDES_KEY, environment="", element="api", state=PK.KNOWN, scope="project", value={"deliverable": True, "settles_by": ""},
                  words="no, the api is ours after all", source="person", story="QA-9", by="conductor")
        rows, _problem = PK.load(root)
        mine = [r for r in rows if r.get("key") == PK.SIDES_KEY and r.get("element") == "api"]
        check_eq("B3: the later word overwrites (the latest row reads ours) and both rows are kept",
                 (PK.state(root, PK.SIDES_KEY, "", "api")["row"]["value"]["deliverable"], len(mine)), (True, 2))
    finally:
        harness.cleanup(root)
    # `relaunch`: today's behaviour exactly - nothing changes, the hold stands
    root, task_root, env, driver, person = absent_story("QA-5")
    try:
        answer_of(driver, root, "relaunch")
        record = pipeline_of(task_root)
        check_eq("B3: `relaunch` changes nothing: the hold stands, the side is still absent and ours, no registry row",
                 (bool(record.get("awaiting")), record["sides"]["api"]["reality"], record["sides"]["api"]["deliverable"], PK.record_path(root).exists()),
                 (True, ABSENT, True, False))
        check_eq("B3: ... every side answered, in the process of the answer nothing more is asked (exit 0, the packet)",
                 _bare_relaunch(driver), story_run.EXIT_DONE)
        first_text = str(person.text)
        # B-1 (t-2562): a bare relaunch in a LATER process re-offers the door, with a lead that names the earlier answer (FR-7)
        from story_run_common import driver_for
        later = driver_for(root, env, "QA-5")
        again = _bare_relaunch(later)
        check_eq("B3 B-1: a later bare relaunch re-offers the question over the same side", (getattr(again, "kind", again), later.state.get("absent_side")),
                 ("absent_side", "api"))
        check("B3 B-1: ... with a changed lead that names the earlier answer and its date (never the same text twice)",
              str(again.text) != first_text and "you said you would start" in str(again.text) and _today() in str(again.text), str(again.text)[:300])
        check("B3 B-1: ... and the `not ours` door is in it", "`not ours`" in str(again.text))
        said = answer_of(later, root, "not ours")
        check_eq("B3 B-1: `not ours` after a `relaunch` lifts the hold", (pipeline_of(task_root)["sides"]["api"]["deliverable"],
                                                                       "awaiting" in pipeline_of(task_root)), (False, False))
    finally:
        harness.cleanup(root)
    # B-1 (b)/(d): a hold met again with NO answer for it (a crash after the `await`, a lost question file) asks again, with today's text
    root, task_root, env, driver, person = absent_story("QA-5")
    try:
        from story_run_common import driver_for
        later = driver_for(root, env, "QA-5")
        again = _bare_relaunch(later)
        check_eq("B3 B-1: no answer was recorded for this hold: the bare relaunch asks again, over the side, with the original text",
                 (getattr(again, "kind", again), str(again.text) == str(person.text)), ("absent_side", True))
        # edge (a): a hold with no `opened` still asks and records under the empty key
        blind = driver_for(root, env, "QA-5")
        blind.state.pop("absent_side_answers", None)
        real = pipeline_of(task_root)
        blind.pipeline = lambda: {**real, "awaiting": {"since": "t", "cause": "s5_absent_side", "held_from": "S6"}}
        asked = _bare_relaunch(blind)
        check_eq("B3 edge (a): a hold with no `opened` asks, never skips, and records under the empty key",
                 (getattr(asked, "kind", asked), blind.state["absent_side_answers"]["opened"]), ("absent_side", ""))
    finally:
        harness.cleanup(root)
    # other words are the conductor's: nothing is changed by code
    root, task_root, env, driver, person = absent_story("QA-5")
    try:
        unread = []
        driver.unread = lambda *a, **k: unread.append((a, k))
        got = driver._answer_absent_side("the platform team might finish it next week", "q", "S6")
        check_eq("B3: other words are read by no code: the conductor once, the hold and the side stand",
                 (got, len(unread), bool(pipeline_of(task_root).get("awaiting")), pipeline_of(task_root)["sides"]["api"]["deliverable"]),
                 (False, 1, True, True))
    finally:
        harness.cleanup(root)
    # several absent sides: the question is about ONE side and the answer never changes another (edge 2)
    root, task_root, env, driver, person = absent_story("QA-5", sides=("api", "ui"))
    try:
        check_eq("B3: two absent sides: one question, over the first by name", driver.state.get("absent_side"), "api")
        answer_of(driver, root, "not ours")
        record = pipeline_of(task_root)
        check_eq("B3: the answer for `api` leaves `ui` absent and ours (it parks the story again, asked on its own)",
                 (record["sides"]["api"]["deliverable"], record["sides"]["ui"]["reality"], record["sides"]["ui"]["deliverable"],
                  contract.parks_after_s5(record)), (False, ABSENT, True, True))
    finally:
        harness.cleanup(root)
    # B-2 (t-2562): `relaunch` on the first side still asks the second, in the same process; `not ours` on it leaves the first waiting
    root, task_root, env, driver, person = absent_story("QA-5", sides=("api", "ui"))
    try:
        answer_of(driver, root, "relaunch")
        second = _bare_relaunch(driver)
        check_eq("B3 B-2: after `relaunch` on `api` the next `where` asks about `ui` in the same process",
                 (getattr(second, "kind", second), driver.state.get("absent_side")), ("absent_side", "ui"))
        check("B3 B-2: ... with the original text over `ui`", "called `ui`" in str(second.text) and "you said" not in str(second.text), str(second.text)[:300])
        answer_of(driver, root, "not ours")
        record = pipeline_of(task_root)
        check_eq("B3 B-2: `not ours` on `ui` makes `ui` substituted and leaves `api` waiting (absent, ours, the story parks again)",
                 (record["sides"]["ui"]["reality"], record["sides"]["ui"]["deliverable"], record["sides"]["api"]["reality"],
                  record["sides"]["api"]["deliverable"], contract.parks_after_s5(record)), (SUBSTITUTED, False, ABSENT, True, True))
        # all sides answered `relaunch` in one process: nothing more is asked there (today's exit)
        root2, task_root2, env2, driver2, person2 = absent_story("QA-6", sides=("api", "ui"))
        try:
            answer_of(driver2, root2, "relaunch")
            _bare_relaunch(driver2)                       # asks about `ui`
            answer_of(driver2, root2, "relaunch")
            check_eq("B3 B-2: every side answered `relaunch`: nothing is asked, exit 0", _bare_relaunch(driver2), story_run.EXIT_DONE)
        finally:
            harness.cleanup(root2)
    finally:
        harness.cleanup(root)
    # an experiment keeps the answer in the story only; an unreadable registry is said in words and the answer stays in the story (AR-28)
    for label, prepare, line in (("--no-trace", lambda r, d: d.state.setdefault("launch", {}).update(no_trace=True),
                                  "your answer about api was kept for this story only (an experiment leaves no trace)"),
                                 ("an unreadable registry", lambda r, d: (PK.record_path(r).parent.mkdir(parents=True, exist_ok=True),
                                                                          PK.record_path(r).write_text("{not json", encoding="utf-8")),
                                  "your answer about api was kept for this story only: the project's record of sides")):
        root, task_root, env, driver, person = absent_story("QA-5")
        try:
            prepare(root, driver)
            said = answer_of(driver, root, "not ours")
            record = pipeline_of(task_root)
            check_eq(f"B3 {label}: the answer is kept in the story and the hold is lifted",
                     (record["sides"]["api"]["deliverable"], "awaiting" in record), (False, False))
            check(f"B3 {label}: and one line says it was kept for this story only", line in said, said[-400:])
            check(f"B3 {label} (F-1): ... and the line is in pipeline.warnings, where the report and gate A read it",
                  any(line in str(w) for w in record.get("warnings") or []), str(record.get("warnings"))[:300])
            if label == "--no-trace":
                check_eq("B3 --no-trace: nothing is written to the registry", PK.record_path(root).exists(), False)
        finally:
            harness.cleanup(root)


def _today() -> str:
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d")


def _bare_relaunch(driver):
    """The recorded hold met again with no flag (`awaiting_implementation`): the exit code of the `Stop` (the packet, nothing asked), or the
    `Person` raised (the question)."""
    import story_run
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            driver._act_await_implementation({"action": "awaiting_implementation", "cause": "s5_absent_side", "held_from": "S6"})
    except story_run.Stop as stop:
        return stop.code
    except story_run.Person as raised:
        return raised
    return -2


def main() -> None:
    absent_side_cases()
    harness.finish("test_story_sides_absent_side")


# split: runner piece 1
if __name__ == "__main__":
    main()
