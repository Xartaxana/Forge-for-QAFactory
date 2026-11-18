"""t292: a part of test_story_run_s6.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_run_s6_common."""
import json
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import story_run_common  # noqa: E402
del story_run_common  # split: imported for its sys.path effect
from story_run_common import run_scenarios, check, check_eq, check_in, check_not_in, d2_answer, d2_conductor_calls, d2_pipeline, d2_seed, driver_for, eq, human_broken, s0_answer, s0_journal, s0_pipeline, s0_project, s0_question, s0_run, s0_state, set_control, stub_calls
from story_run_s6_common import (  # noqa: E402
    AWAITS, SCREENS, WITH_HTTP, enter_manual, manual_rig, t292_config, t292_enter,
)


def t292_account(root, text, name="account.env"):
    """An env file with the given text, and the config pointing at it (default keys AUTH_USERNAME / AUTH_PASSWORD)."""
    (root / name).write_text(text, encoding="utf-8")
    t292_config(root, env_file=name)


def t292_k15_to_k18_the_question_comes_before_any_block() -> None:
    """K15: a block with screen cases and no `environment.env_file` raises the question, registers nothing and launches
    nothing - the http case beside them waits for the same answer (Q10). K16/K17 are the negative controls (http only;
    the account present); K18: a named file that is missing, then present without the password."""
    task = "QA-9"
    root, task_root, env = d2_seed(task, environment="Local", pending=False)
    try:
        t292_config(root)
        cases = list(WITH_HTTP)
        driver, world, launched, moves = manual_rig(root, env, task, cases, policy=WITH_HTTP)
        text, new, person = t292_enter(driver, world, cases)
        check("K15 screen cases and no env_file: a Person is raised", person is not None)
        eq("K15: nothing is launched and no dispatch is registered (the http case waits too)", (launched, world.dispatches, new), ([], {}, ""))
        eq("K15: the Person is kind `stand_login`, at S6, for exactly the screen cases", (person.kind, person.stage, person.login_cases), ("stand_login", "S6", list(SCREENS)))
        eq("K15: the text obeys human-questions.md (with the answer block ask() puts under it)", human_broken(person.text), [])
        for word in ("`retry`", "`by hand`", "`go on`", "I have not started any of these checks"):
            check_in(f"K15: the text says {word}", word, person.text)
        for case in SCREENS:
            check_in(f"K15: the text names {case}", case, person.text)
        check_not_in("K15: and not the http case (it is not what is asked about)", "QA-9_TC_003", person.text)
        check_in("K15: the reason is the no-file one", "the project's settings name no file for it", person.text)
        check_in("K15: the details carry the config key names for the factory's reader", "environment.env_file", person.details)
        check_in("K15: ... and the door for a project that needs no sign-in", "manual_capture.login.ui", person.details)
        # the question is a real one: it is asked, and the flag names it
        driver.ask(person)
        state = s0_state(task_root)
        eq("K15: ask() sets the flag for exactly these cases", state.get("login_question"), {"stage": "S6", "cases": list(SCREENS)})
        eq("K15: and the question is kind stand_login", (state.get("asked") or {}).get("kind"), "stand_login")

        # K16: http only, no env_file: dispatched as today, no Person
        driver, world, launched, moves = manual_rig(root, env, task, ["QA-9_TC_003"], policy="api")
        text, new, person = t292_enter(driver, world, ["QA-9_TC_003"])
        eq("K16 control: http cases only and no env_file: dispatched as today, no Person", (person, [e["scope"] for e in launched]), (None, [["QA-9_TC_003"]]))
        # K17: screen cases, the account present (both keys): dispatched as today
        t292_account(root, "AUTH_USERNAME=qa-user\nAUTH_PASSWORD=SENTINEL-PW-1\n")
        driver, world, launched, moves = manual_rig(root, env, task, cases, policy=WITH_HTTP)
        text, new, person = t292_enter(driver, world, cases)
        eq("K17 control: screen cases with the account in place: dispatched as today, no Person", (person, [e["scope"] for e in launched]), (None, [cases]))
        # K18: a named file that does not exist; then one without the password
        t292_config(root, env_file="missing.env")
        driver, world, launched, moves = manual_rig(root, env, task, cases, policy=WITH_HTTP)
        text, new, person = t292_enter(driver, world, cases)
        check("K18 env_file named but missing: a Person", person is not None)
        check_in("K18: the details say the file does not exist", "does not exist", person.details)
        check_in("K18: the text says the file is not there", "the file the settings name for it is not there", person.text)
        eq("K18: nothing dispatched", (launched, world.dispatches), ([], {}))
        t292_account(root, "AUTH_USERNAME=qa-user\nSOMETHING_ELSE=SENTINEL-PW-2\n")
        driver, world, launched, moves = manual_rig(root, env, task, cases, policy=WITH_HTTP)
        text, new, person = t292_enter(driver, world, cases)
        check("K18 the file there, no password: a Person", person is not None)
        check_in("K18: the details name the missing key", "AUTH_PASSWORD is not set", person.details)
        check_in("K18: the text says the file lacks the account", "does not hold the account's name or its password", person.text)
        check_not_in("K18: no value of the file appears in the text or the details", "SENTINEL-PW", person.text + person.details + text)
        check_not_in("K18: nor the user name's value", "qa-user", person.text + person.details)
        for label, content in (("an empty password", "AUTH_USERNAME=qa-user\nAUTH_PASSWORD=\n"),
                               ("a quoted empty password", "AUTH_USERNAME=qa-user\nAUTH_PASSWORD=\"\"\n"),
                               ("a commented-out password", "AUTH_USERNAME=qa-user\n# AUTH_PASSWORD=SENTINEL-PW-3\n")):
            t292_account(root, content)
            driver, world, launched, moves = manual_rig(root, env, task, cases, policy=WITH_HTTP)
            text, new, person = t292_enter(driver, world, cases)
            check(f"K18 adversarial ({label}): still a Person (the safe side), nothing launched", person is not None and launched == [])
        t292_account(root, "export AUTH_USERNAME=qa-user\nexport AUTH_PASSWORD=pw\n")
        driver, world, launched, moves = manual_rig(root, env, task, cases, policy=WITH_HTTP)
        text, new, person = t292_enter(driver, world, cases)
        eq("K18 `export AUTH_USERNAME=x` reads as present: dispatched", (person, len(launched)), (None, 1))
        # an env_file that names a DIRECTORY, and a relative one resolved against the project root (not the cwd)
        (root / "adir").mkdir()
        t292_config(root, env_file="adir")
        driver, world, launched, moves = manual_rig(root, env, task, cases, policy=WITH_HTTP)
        check("K18 adversarial (env_file names a directory): a Person", t292_enter(driver, world, cases)[2] is not None)
    finally:
        harness.cleanup(root)


def t292_k19_the_answers_have_an_executor() -> None:
    """K19: the three answers through `ask` and `take_answer`. `retry` records nothing and the next entry asks again;
    `by hand` and `go on` record the pass with ONE command and the next entry leaves the screen cases out in the person's
    words (the http case is dispatched, not complete) and the one after closes the manual half code-only; other words go
    to the conductor with that same command."""
    import json as _json
    task = "QA-9"
    root, task_root, env = d2_seed(task, environment="Local", pending=False)
    try:
        t292_config(root)
        cases = list(WITH_HTTP)
        screens = list(SCREENS)

        def ask_it():
            driver, world, launched, moves = manual_rig(root, env, task, cases, policy=WITH_HTTP)
            _text, _new, person = t292_enter(driver, world, cases)
            driver.ask(person)
            return driver, world, launched, moves

        def overrides():
            return [o for o in (s0_pipeline(task_root).get("stage_overrides") or []) if o.get("match") == "stand login missing"]
        # retry: no waiver; the same question is asked again, with the FR-7 notice
        driver, world, launched, moves = ask_it()
        driver.take_answer(Path(d2_answer(root, "retry")))
        eq("K19 `retry`: no pass is recorded", overrides(), [])
        check("K19 `retry`: the flag is gone with the question", "login_question" not in s0_state(task_root))
        check("K19 `retry`: the journal says what was answered", any("S6 (retry): retry" in str(e.get("notes")) for e in s0_journal(root)))
        driver, world, launched, moves = manual_rig(root, env, task, cases, policy=WITH_HTTP)
        text, new, person = t292_enter(driver, world, cases)
        check("K19 `retry`: the next entry raises the Person again (the material is still missing)", person is not None and launched == [])
        driver.ask(person)
        check_in("K19 `retry`: and it is not re-asked silently (FR-7: the earlier answer is shown)", "You have answered this exact question before", s0_question(task_root))
        # other words: the conductor gets the waiver command, and nothing is recorded by code
        calls = []
        driver.conductor = lambda prompt, words=None, **kw: calls.append((prompt, words)) or {"action": "continue", "did": "read"}
        driver.take_answer(Path(d2_answer(root, "I am not sure, ask Dana")))
        eq("K19 other words: ONE conductor call, no pass recorded by code", (len(calls), overrides()), (1, []))
        check_in("K19 other words: it carries the one waiver command with this block and stage",
                 '--stage S6 --block "stand login missing" --words-file ', calls[0][0])
        check_not_in("K19 other words: and no inline `--decision` (the words go by FILE, axis 5)", "--decision", calls[0][0])
        check_in("K19 other words: and the instruction to run nothing when they do not say it", "run nothing", calls[0][0])
        eq("K19 other words: the person's words travel whole", calls[0][1], "I am not sure, ask Dana")
        # `by hand` and `go on`: ONE executor (waiver.py), the words verbatim
        for token, words in (("by hand", "By hand."), ("go on", "go on")):
            fresh_root, fresh_task_root, fresh_env = d2_seed(task, environment="Local", pending=False)
            try:
                t292_config(fresh_root)
                driver, world, launched, moves = manual_rig(fresh_root, fresh_env, task, cases, policy=WITH_HTTP)
                _text, _new, person = t292_enter(driver, world, cases)
                driver.ask(person)
                driver.take_answer(Path(d2_answer(fresh_root, words)))
                got = [o for o in (s0_pipeline(fresh_task_root).get("stage_overrides") or []) if o.get("match") == "stand login missing"]
                eq(f"K19 `{token}`: waiver.py records the block for S6 with the words verbatim", [(o["stage"], o["decision"]) for o in got], [("S6", words)])
                check(f"K19 `{token}`: and the journal has the answer", any(f"S6 ({token}): " in str(e.get("notes")) for e in s0_journal(fresh_root)))
                # the next entry: the http case only, not complete; one line per screen case with the words; request.json says so
                text, new, person = t292_enter(driver, world, cases)
                eq(f"K19 `{token}`: the next entry raises nothing and dispatches only the http case, not closing the stage",
                   (person, [(e["scope"], e["complete"]) for e in launched]), (None, [(["QA-9_TC_003"], AWAITS)]))         # X7-6c: the last window awaits the consumer
                for case in screens:
                    line = next((ln for ln in text.splitlines() if ln.startswith(f"S6: {case}: not checked by hand")), "")
                    check_in(f"K19 `{token}`: a `not checked by hand` line for {case} carries the person's words", f"the person said: \"{words}\"", line)
                    refused = _json.loads((fresh_task_root / "work" / "evidence" / "manual" / case / "request.json").read_text(encoding="utf-8"))
                    check_in(f"K19 `{token}`: {case}'s request says it was left out, in the words", f"the person said: \"{words}\"", refused["refused"]["reason"])
                    check_in(f"K19 `{token}`: ... with a door", "put the stand's test account in the project's settings", refused["refused"]["door"])
                # the one after: nothing left to dispatch: the manual half closes code-only, naming the screen cases
                moves.clear()
                text, new, person = t292_enter(driver, world, cases)
                eq(f"K19 `{token}`: the following entry closes the manual half (finalize, code_only, stage_done), no role", ([m[0] for m in moves], len(launched)), (["finalize", "code_only", "stage_done"], 1))
                check_in(f"K19 `{token}`: and names the screen cases as not checked", ", ".join(screens), moves[1][2])
            finally:
                harness.cleanup(fresh_root)
        # a pass that did not record (waiver.py refused): said, and the question comes back
        fresh_root, fresh_task_root, fresh_env = d2_seed(task, environment="Local", pending=False)
        try:
            t292_config(fresh_root)
            driver, world, launched, moves = manual_rig(fresh_root, fresh_env, task, cases, policy=WITH_HTTP)
            _text, _new, person = t292_enter(driver, world, cases)
            driver.ask(person)
            real = driver.py
            driver.py = lambda script, *a, **k: (2, "waiver: refused") if script == "waiver.py" else real(script, *a, **k)
            import contextlib
            import io
            import story_run
            said = io.StringIO()
            held = None
            with contextlib.redirect_stdout(said):
                try:
                    driver.take_answer(Path(d2_answer(fresh_root, "go on")))
                except story_run.Person as raised:
                    held = raised
            check_in("K19 a pass that did not record is said (the seam's held question, with the writer's words)",
                     "Your word could not be recorded as the pass, so nothing was passed.", getattr(held, "text", ""))
            check_in("K19 ... and it is said on the screen too", "the pass was not recorded", said.getvalue())
            _text, _new, person = t292_enter(driver, world, cases)
            check("K19 ... and the question comes back (nothing was recorded)", person is not None)
        finally:
            harness.cleanup(fresh_root)
    finally:
        harness.cleanup(root)


def t292_k20_to_k24_the_pass_is_read_only_while_the_account_is_missing() -> None:
    """K20 (temporal): the pass is recorded, then the account arrives - the screen cases are dispatched even though a pass
    exists; a revoked pass brings the question back (E17). K21: the flag isolates the answers. K22: `login.ui: null`
    asks nothing. K23: no screen case left asks nothing. K24: an unknown policy counts as a screen case."""
    import contextlib
    import io
    task = "QA-9"
    root, task_root, env = d2_seed(task, environment="Local", pending=False)
    try:
        t292_config(root)
        cases = list(WITH_HTTP)
        d2_pipeline(task_root, stage_overrides=[{"stage": "S6", "match": "stand login missing", "decision": "by hand",
                                                  "at": "2026-10-02T10:00:00+00:00", "by": "human"}])
        driver, world, launched, moves = manual_rig(root, env, task, cases, policy=WITH_HTTP)
        text, new, person = t292_enter(driver, world, cases)
        eq("K20 before the account: the pass holds - the screen cases are left out, no Person", (person, [e["scope"] for e in launched]), (None, [["QA-9_TC_003"]]))
        t292_account(root, "AUTH_USERNAME=qa-user\nAUTH_PASSWORD=pw\n")
        driver, world, launched, moves = manual_rig(root, env, task, cases, policy=WITH_HTTP)
        text, new, person = t292_enter(driver, world, cases)
        eq("K20 temporal: the account arrives after the pass: the screen cases ARE dispatched (a pass is read only while the material is missing)",
           (person, [e["scope"] for e in launched]), (None, [cases]))
        check_not_in("K20: and nothing says they were left out", "not checked by hand", text)
        # E17: the person takes the word back with waiver --revoke; the account is gone again: the question comes back
        t292_config(root)
        code, out = driver.py("waiver.py", "--revoke", "--task", task, "--stage", "S6", "--block", "stand login missing", "--decision", "I have the account now")
        eq("K20 revoke: waiver.py --revoke takes the word back", code, 0)
        driver, world, launched, moves = manual_rig(root, env, task, cases, policy=WITH_HTTP)
        text, new, person = t292_enter(driver, world, cases)
        check("K20 revoke: the question speaks again (a revoked pass is history, not a pass)", person is not None and launched == [])

        # K21: the answers do not cross
        set_control(root, {"conductor": {"action": "continue", "did": "read it", "text": "Read."}})
        d2_pipeline(task_root, stage_overrides=[])
        driver = driver_for(root, env, task)
        driver.state["asked"] = {"kind": "environment", "stage": "S6", "dispatch": ""}
        driver.state["stand_question"] = "S6"
        driver.state["login_question"] = {"stage": "S6", "cases": list(SCREENS)}      # a stale flag of the OTHER question
        driver.save_state()
        (task_root / "state" / "driver-question.md").write_text("# q\nkind: environment\n", encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            driver.take_answer(Path(d2_answer(root, "go on")))
        names = [(o.get("match"), o.get("decision")) for o in (s0_pipeline(task_root).get("stage_overrides") or [])]
        eq("K21 the stand question's answer reaches ITS branch only: the `stand not confirmed` pass, never `stand login missing`",
           [m for m, _d in names], ["stand not confirmed"])
        driver = driver_for(root, env, task)
        before = len(d2_conductor_calls(root))
        driver.state["asked"] = {"kind": "stand_login", "stage": "S6", "dispatch": ""}
        driver.state.pop("login_question", None)
        driver.save_state()
        (task_root / "state" / "driver-question.md").write_text("# q\nkind: stand_login\n", encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            driver.take_answer(Path(d2_answer(root, "go on")))
        names = [o.get("match") for o in (s0_pipeline(task_root).get("stage_overrides") or [])]
        eq("K21 a `stand_login` answer with no flag is not taken by the new branch: it goes to the conductor and records no pass",
           (names, len(d2_conductor_calls(root)) - before), (["stand not confirmed"], 1))

        # K22 (Q7): `manual_capture.login.ui: null` - no Person, the screen cases are dispatched
        t292_config(root, manual_capture={"login": {"ui": None}})
        driver, world, launched, moves = manual_rig(root, env, task, cases, policy=WITH_HTTP)
        text, new, person = t292_enter(driver, world, cases)
        eq("K22 `manual_capture.login.ui: null` and no env_file: no question, everything dispatched", (person, [e["scope"] for e in launched]), (None, [cases]))
        t292_config(root, manual_capture={"login": {"http": None}})
        driver, world, launched, moves = manual_rig(root, env, task, cases, policy=WITH_HTTP)
        check("K22 control: `login.http: null` is not a statement about the screens: the question is asked", t292_enter(driver, world, cases)[2] is not None)

        # K23: no screen case left - refused by prepare, or done - asks nothing, and manual_close is as today
        t292_config(root)
        driver, world, launched, moves = manual_rig(root, env, task, list(SCREENS), refused=list(SCREENS), policy="ui")
        text, new, person = t292_enter(driver, world, list(SCREENS))
        eq("K23 screen cases all refused by prepare, no env_file: no Person; the manual half closes as today", (person, [m[0] for m in moves]), (None, ["finalize", "code_only", "stage_done"]))
        driver, world, launched, moves = manual_rig(root, env, task, list(SCREENS), policy="ui")
        for number, case in enumerate(SCREENS, 1):
            world.dispatches[f"S6-qa-runner-{number}"] = {"stage": "S6", "status": "accepted", "execution_kind": "manual", "manual_case_ids": [case]}
        text, new, person = t292_enter(driver, world, list(SCREENS))
        eq("K23 screen cases all done, no env_file: no Person; closes as today", (person, launched, [m[0] for m in moves]), (None, [], ["finalize", "code_only", "stage_done"]))
        driver, world, launched, moves = manual_rig(root, env, task, cases, refused=list(SCREENS), policy=WITH_HTTP)
        text, new, person = t292_enter(driver, world, cases)
        eq("K23 control: screen cases refused but an http case ready: dispatched, no Person", (person, [e["scope"] for e in launched]), (None, [["QA-9_TC_003"]]))

        # K24: an unknown policy counts as a screen case, with one printed line naming the request
        driver, world, launched, moves = manual_rig(root, env, task, list(SCREENS), policy="")
        said = io.StringIO()
        with contextlib.redirect_stdout(said):
            plan = driver.manual_plan(list(SCREENS))
            try:
                driver.stand_login_gate(plan)
                raised = None
            except Exception as exc:
                raised = exc
        check("K24 an unknown policy (\"\") counts as a screen case: the Person is raised", raised is not None and getattr(raised, "kind", "") == "stand_login")
        for case in SCREENS:
            check_in(f"K24: one line says the request of {case} could not be read", f"S6: {case}: its prepared request (work/evidence/manual/{case}/request.json) could not be read", said.getvalue())
    finally:
        harness.cleanup(root)


def t292_the_real_policy_reader_and_the_question_titles() -> None:
    """`manual_policy` reads what `manual_prepare` wrote (the real one, no stub): `ui`, `api`, a refusal, a broken file and
    an absent one - the last three are "" (unknown). The question names a case by its title and id, or - with no title -
    by a link to its case file on the same line."""
    import manual_evidence as ME
    task = "QA-9"
    root, task_root, env = d2_seed(task, environment="Local", pending=False)
    try:
        driver = driver_for(root, env, task)

        def request(case, content):
            path = ME.request_path(task_root, case)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content if isinstance(content, str) else json.dumps(content), encoding="utf-8")
        request("QA-9_TC_001", {"evidence_policy": "ui", "case": "QA-9_TC_001"})
        request("QA-9_TC_002", {"evidence_policy": "api"})
        request("QA-9_TC_003", {"refused": {"reason": "r", "door": "d"}, "evidence_policy": "ui"})
        request("QA-9_TC_004", "{not json")
        request("QA-9_TC_005", {"case": "QA-9_TC_005"})
        request("QA-9_TC_006", "[1]")
        eq("manual_policy: ui / api / refused / broken / no policy / not an object / absent",
           [driver.manual_policy(f"QA-9_TC_00{n}") for n in range(1, 8)], ["ui", "api", "", "", "", "", ""])
        # the question's lines
        folder = task_root / "work" / "test-cases" / "area"
        folder.mkdir(parents=True)
        (folder / "QA-9_TC_001.md").write_text("---\nid: QA-9_TC_001\ntitle: Zoom the visual diff\nplan_row: TS-1\n---\n\n## Then\n1. x.\n", encoding="utf-8")
        (folder / "QA-9_TC_002.md").write_text("---\nid: QA-9_TC_002\ntitle: \"\"\nplan_row: TS-2\n---\n\n## Then\n1. x.\n", encoding="utf-8")
        # The index is `contract.case_index`'s own business (tested there; it memoises per process, so an earlier scenario's
        # project can hide this one's files): here it answers with the two files just written, and `case_title` is the real one.
        from unittest import mock
        found = {"QA-9_TC_001": {"path": folder / "QA-9_TC_001.md"}, "QA-9_TC_002": {"path": folder / "QA-9_TC_002.md"}}
        with mock.patch("contract.case_index", lambda _root: found):
            text = driver.stand_login_question_text(["QA-9_TC_001", "QA-9_TC_002", "QA-9_TC_009"], "no_file")
        check_in("question: a case with a title is `title (id)`", "- Zoom the visual diff (QA-9_TC_001)", text)
        check_in("question: a case with an empty title is a link to its case file on the same line", "- [QA-9_TC_002](work/test-cases/area/QA-9_TC_002.md)", text)
        check_in("question: a case the story does not hold is its bare id (never a raise)", "- QA-9_TC_009\n", text)
        eq("question: and it obeys human-questions.md", human_broken(text), [])
        for kind, reason in (("no_file", "the project's settings name no file for it"), ("missing_file", "the file the settings name for it is not there"),
                             ("missing_key", "the file the settings name does not hold the account's name or its password")):
            check_in(f"question: the reason of `{kind}`", reason, driver.stand_login_question_text(["QA-9_TC_001"], kind))
    finally:
        harness.cleanup(root)


def t308_f6_the_reason_the_person_reads_is_the_true_one() -> None:
    """t-308 F6: `stand_login_problem` names the reason the person reads. An env file that is THERE but cannot be read
    (a folder in its place, no permission) is `unreadable`, never "not there"; a settings file that cannot be loaded is a
    `missing_file` reason carrying the loader's own text, never `no_file` ("the settings name no file" - false). Controls:
    an absent file is still `missing_file`, a file without the password `missing_key`, no env_file `no_file`, a login
    declared null and a good file are no problem. Every reason's question passes human-questions.md."""
    from unittest import mock
    import manual_capture as MC
    task = "QA-9"
    root, task_root, env = d2_seed(task, environment="Local", pending=False)
    try:
        driver = driver_for(root, env, task)

        def problem(**environment):
            t292_config(root, **environment)
            return driver.stand_login_problem()
        (root / "adir").mkdir()
        kind, details = problem(env_file="adir")
        eq("F6 a folder where the env file should be: `unreadable`", kind, "unreadable")
        check_in("F6: the details say it cannot be read", "cannot be read", details)
        check_not_in("F6: and not that it does not exist", "does not exist", details)
        (root / "locked.env").write_text("AUTH_USERNAME=u\nAUTH_PASSWORD=SENTINEL-PW-9\n", encoding="utf-8")
        with mock.patch.object(MC, "_env_values", side_effect=PermissionError("denied")):
            kind, details = problem(env_file="locked.env")
        eq("F6 a file that is there but cannot be read (no permission): `unreadable`", kind, "unreadable")
        check_not_in("F6: no value of the file in the details", "SENTINEL-PW", details)
        kind, details = problem(env_file="nowhere.env")
        eq("F6 control: an absent file is still `missing_file`", kind, "missing_file")
        t292_account(root, "AUTH_USERNAME=u\nOTHER=x\n")
        eq("F6 control: a file with no password is `missing_key`", driver.stand_login_problem()[0], "missing_key")
        eq("F6 control: no env_file is `no_file`", problem()[0], "no_file")
        t292_account(root, "AUTH_USERNAME=u\nAUTH_PASSWORD=p\n")
        eq("F6 control: a good file is no problem", driver.stand_login_problem(), ("", ""))
        t292_config(root, manual_capture={"login": {"ui": None}}, env_file="nowhere.env")
        eq("F6 control: a login declared null is no problem even with a missing file", driver.stand_login_problem(), ("", ""))
        t292_config(root, env_file="locked.env")
        with mock.patch.object(MC, "load_config", side_effect=ValueError("config.json is not valid JSON (boom)")):
            kind, details = driver.stand_login_problem()
        eq("F6 the settings cannot be loaded: `missing_file`, not `no_file`", kind, "missing_file")
        check_in("F6: with the loader's own text", "config.json is not valid JSON (boom)", details)
        # every reason's question obeys human-questions.md
        for reason in ("no_file", "missing_file", "unreadable", "missing_key"):
            text = driver.stand_login_question_text(["QA-9_TC_001"], reason)
            eq(f"F6 the question for `{reason}` obeys human-questions.md", human_broken(text), [])
        check_in("F6: the `unreadable` question says the file could not be read", "the file the settings name for it could not be read",
                 driver.stand_login_question_text(["QA-9_TC_001"], "unreadable"))
    finally:
        harness.cleanup(root)


def ep1_41f_cases_all_on_a_device_skip_only_the_default_account() -> None:
    """EP1-41f (N-18): a block whose cases are ALL on a device profile asks nothing about the default web account (no env file is no
    problem), yet the account a case NAMES is still asked for on entry; a web case beside them, `None`, `[]`, a case no profile
    claims, a raise in the keying and a broken table each keep the old question (a question too many, never one too few)."""
    from unittest import mock
    import gate_preflight
    import manual_evidence as ME
    import surfaces
    task = "QA-9"
    root, task_root, env = d2_seed(task, environment="Local", pending=False)
    try:
        driver = driver_for(root, env, task)
        t292_config(root)
        path = root / "qa-factory" / "config.json"
        cfg = json.loads(path.read_text(encoding="utf-8"))
        cfg["profiles"] = [{"profile_id": "e2e-ui", "capabilities": ["web"]}, {"profile_id": "android", "capabilities": ["native"]}]
        cfg["environments"] = [{"name": "Local"}, {"name": "emu", "surface": "android"}]
        path.write_text(json.dumps(cfg), encoding="utf-8")
        keyed = {"android": {"cases": ["QA-9_TC_001", "QA-9_TC_003"]}, "e2e-ui": {"cases": ["QA-9_TC_002"]}}

        def problem(cases, keying=keyed):
            with mock.patch.object(gate_preflight, "stand_profiles", return_value=keying):
                return driver.stand_login_problem(cases)
        eq("41f control: no cases and no env file - the old question (`no_file`)", driver.stand_login_problem()[0], "no_file")
        eq("41f every case on the device: the default account is not asked", problem(["QA-9_TC_001", "QA-9_TC_003"]), ("", ""))
        eq("41f one web case beside the device case: the old question", problem(["QA-9_TC_001", "QA-9_TC_002"])[0], "no_file")
        eq("41f `None` cases: the old question", problem(None)[0], "no_file")
        eq("41f `[]` cases: the old question", problem([])[0], "no_file")
        eq("41f a case no profile claims: the old question", problem(["QA-9_TC_001", "QA-9_TC_404"])[0], "no_file")
        with mock.patch.object(gate_preflight, "stand_profiles", side_effect=OSError("x")):
            eq("41f the keying raises: the old question", driver.stand_login_problem(["QA-9_TC_001"])[0], "no_file")
        with mock.patch.object(surfaces, "TABLE_PATH", root / "no-such-table.json"):
            eq("41f a broken table: the old question, no crash", problem(["QA-9_TC_001"])[0], "no_file")
        # an account the case NAMES, with no pair on the stand, is still asked on entry - the actor loop runs on a device case
        actors = [{"id": "A1", "check": {"stand_account": "Admin"}}]
        with mock.patch.object(ME, "request_actors", return_value=(actors, "")):
            kind, details = problem(["QA-9_TC_001"])
        eq("41f a named account without a pair on a device case: asked (`missing_key`), not skipped", kind, "missing_key")
        check_in("41f ... and the details name the case and the account", "QA-9_TC_001: the account A1", details)
        # a login declared null stays first
        t292_config(root, manual_capture={"login": {"ui": None}})
        eq("41f `login.ui: null` is still no problem for a web block", problem(["QA-9_TC_002"]), ("", ""))
    finally:
        harness.cleanup(root)


IN_FLIGHT_STUB = '''import json, os, sys
from pathlib import Path
state = Path(os.environ["SEEN_STATE"])
import time
# The parent writes in_flight[<dispatch>] only after Popen returns, so the child may start first: poll (cap 5 s, 50 ms)
# until its own entry shows. No dispatch in the env (the conductor) expects no entry: read once, never wait.
want = os.environ.get("QA_FACTORY_DRIVER_RUN")
deadline = time.time() + 5
while True:
    try:
        seen = json.loads(state.read_text(encoding="utf-8")) if state.is_file() else {}
    except ValueError:
        seen = {}
    if not want or (seen.get("in_flight") or {}).get(want) or time.time() >= deadline:
        break
    time.sleep(0.05)
Path(os.environ["SEEN_OUT"]).write_text(json.dumps({"in_flight": seen.get("in_flight"), "pid": os.getpid(),
                                                    "env": os.environ.get("QA_FACTORY_DRIVER_RUN")}), encoding="utf-8")
sys.stdin.read()
print(json.dumps({"type": "result", "session_id": "", "result": "ok", "num_turns": 3, "total_cost_usd": 0.1, "is_error": False}))
'''


def t329_b268_a_role_in_flight_is_written_while_it_runs_and_removed_when_it_returns() -> None:
    """t-329 item 1 (B-268): `run_claude` writes `in_flight[<dispatch>] = {dispatch_id, pid, started_at}` into
    driver-state.json as soon as the `claude -p` process has a pid, and removes it when the call returns by any
    road. The stub reads driver-state.json FROM INSIDE the child: the entry is on disk while the process runs,
    names that very process, and the child's environment carries QA_FACTORY_DRIVER_RUN (item 2). Controls: the
    conductor's call (no dispatch) writes no entry; a call that raises leaves no entry; a resumed call names the
    session; the key is gone, not an empty dict (a state with nobody in flight reads as before)."""
    from unittest import mock
    task = "QA-9"
    root, task_root, env = d2_seed(task, environment="Local", pending=False)
    try:
        driver = driver_for(root, env, task)
        stub = root / "in_flight_stub.py"
        stub.write_text(IN_FLIGHT_STUB, encoding="utf-8")
        out = root / "seen.json"
        driver.claude = [sys.executable, str(stub)]
        driver.claude_env = dict(driver.claude_env, SEEN_STATE=str(task_root / "state" / "driver-state.json"), SEEN_OUT=str(out))
        driver.run_claude("role", "p", role="qa-automator", dispatch="S5-qa-automator-1", stage="S5")
        seen = json.loads(out.read_text(encoding="utf-8"))
        entry = (seen["in_flight"] or {}).get("S5-qa-automator-1") or {}
        eq("T329-1 while the child ran, its entry was on disk: dispatch id, and the child's own pid",
           (entry.get("dispatch_id"), entry.get("pid")), ("S5-qa-automator-1", seen["pid"]))
        check("T329-1 with a start time and no session (a first call)", bool(entry.get("started_at")) and "session_id" not in entry, str(entry))
        eq("T329-1 the child saw QA_FACTORY_DRIVER_RUN = the dispatch id", seen["env"], "S5-qa-automator-1")
        after = json.loads((task_root / "state" / "driver-state.json").read_text(encoding="utf-8"))
        check("T329-1 when the call returned the entry left, and the key with it", "in_flight" not in after, str(after.get("in_flight")))
        eq("T329-1 and the driver's own memory agrees", driver.state.get("in_flight"), None)
        driver.run_claude("role", "p", role="qa-automator", dispatch="S5-qa-automator-1", stage="S5", resume="s-prev")
        entry = (json.loads(out.read_text(encoding="utf-8"))["in_flight"] or {}).get("S5-qa-automator-1") or {}
        eq("T329-1 a resumed call names the session it resumes", entry.get("session_id"), "s-prev")
        driver.run_claude("conductor", "p", stage="S5")
        seen = json.loads(out.read_text(encoding="utf-8"))
        eq("T329-1 control: a call with no dispatch (the conductor) writes no entry and sets no marker",
           (seen["in_flight"], seen["env"]), (None, None))
        with mock.patch.object(subprocess.Popen, "communicate", side_effect=RuntimeError("the call died")):
            try:
                driver.run_claude("role", "p", role="qa-automator", dispatch="S5-qa-automator-2", stage="S5")
                raised = False
            except RuntimeError:
                raised = True
        check("T329-1 control: a call that raises still leaves no entry behind",
              raised and "in_flight" not in json.loads((task_root / "state" / "driver-state.json").read_text(encoding="utf-8")))
        # t-335 A-n6: the marking is INSIDE the try. A marking that raises (here a non-OSError, which `mark_in_flight`
        # does not swallow) used to leave the child waiting on stdin for a prompt nobody sent, and `with Popen` then
        # waited for the child for ever; now the child is killed and the error is the caller's. The stub reads stdin to
        # the end, so a child left alive would not exit by itself: it is the proof the kill happened.
        pids = []
        real_popen = subprocess.Popen

        def spy(*a, **k):
            proc = real_popen(*a, **k)
            pids.append(proc)
            return proc

        with mock.patch.object(subprocess, "Popen", spy), \
                mock.patch.object(driver, "mark_in_flight", side_effect=RuntimeError("the marking died")):
            try:
                driver.run_claude("role", "p", role="qa-automator", dispatch="S5-qa-automator-3", stage="S5")
                died = False
            except RuntimeError as exc:
                died = "the marking died" in str(exc)
        check("T335 A-n6 a marking that raises: the call raises it (the child was killed, `with` did not wait for ever)",
              died and bool(pids) and pids[0].poll() is not None, str([p.poll() for p in pids]))
        check("T335 A-n6 ...and leaves no entry behind", "in_flight" not in driver.state)
    finally:
        harness.cleanup(root)


def t329_item6_a_ticket_file_of_the_person_is_a_question_not_a_factory_fault() -> None:
    """t-329 item 6 (after t-331): the adapter says `owner: person` for a ticket or paste file that is missing or
    empty. `ticket_failure` knew four owner words, so that object read as "the adapter printed no error object" - the
    FACTORY's fault - and a missing ticket file became a factory refusal instead of the question to the person.
    The owner words are now `ticket_adapter.OWNERS`, the adapter's own list. Pinned END TO END (a real driver process,
    the file adapter, the file deleted) and on the function, with the old words as controls."""
    import ticket_adapter
    # --- end to end: `kind: file`, the ticket file is not there
    root, task_root, env = s0_project("QA-1")
    try:
        (root / "tickets" / "QA-1.md").unlink()
        out = s0_run(root, env, "QA-1")
        eq("T329-6 a file adapter with a missing file: the person is asked (exit 3), not refused", out.returncode, 3,
           out.stdout[-900:] + out.stderr[-600:])
        eq("T329-6 the block is `ticket_read` and no model was called", (s0_state(task_root).get("s0_block"), stub_calls(root)),
           ("ticket_read", []))
        ask = s0_question(task_root)
        check_in("T329-6 the question is the file-style one: the ticket file is not there", "I looked for the file QA-1.md", ask)
        check_in("T329-6 ...with a way to put it right and the paste", "put the ticket file in that folder", ask)
        check_not_in("T329-6 never 'the adapter printed no error object'", "no error object", ask + out.stdout + out.stderr)
        check_not_in("T329-6 and never the factory's own refusal", "the cause is the factory's own", out.stdout + out.stderr + ask)
    finally:
        harness.cleanup(root)
    # --- the function: every owner word the adapter can carry survives; a word it does not know is the factory's
    root, task_root, env = d2_seed("QA-9", environment="Local", pending=False)
    try:
        driver = driver_for(root, env, "QA-9")
        for owner in ticket_adapter.OWNERS:
            said = json.dumps({"ok": False, "owner": owner, "status": None, "retry_at": None, "message": "one sentence"})
            got = driver.ticket_failure(1, said, "")
            eq(f"T329-6 owner `{owner}` of the adapter's own list is kept", (got["owner"], got["from_object"], got["message"]),
               (owner, True, "one sentence"))
        check("T329-6 `person` is in the adapter's list (the fixture's own premise)", "person" in ticket_adapter.OWNERS)
        for label, said in (("an owner nobody knows", json.dumps({"ok": False, "owner": "nobody", "message": "x"})),
                            ("an object that says ok", json.dumps({"ok": True, "owner": "person"})),
                            ("no object at all", "not json")):
            got = driver.ticket_failure(1, said, "")
            eq(f"T329-6 control ({label}): the factory's, with the old words", (got["owner"], got["message"], got["from_object"]),
               ("factory", driver.NO_ERROR_OBJECT, False))
        person = driver.ticket_failure(1, json.dumps({"ok": False, "owner": "person", "message": "ticket file not found: X"}), "")
        check("T329-6 a `person` failure is not the factory's fault", not driver.ticket_is_factory_fault(1, person))
        # --- the branch of the question for a read that is not a project folder's (a pasted file that is missing)
        captured = []
        driver.s0_stop = lambda *a, **k: captured.append((a, k))
        driver.config = dict(driver.config, adapters={"ticket": {"kind": "jira"}})
        driver.s0_ticket_read_question(1, "said", person)
        text = captured[0][0][2] if captured else ""
        check_in("T329-6 the `person` branch gives the adapter's own sentence verbatim (FR-8)", "ticket file not found: X", text)
        check_in("T329-6 ...and the way on: put the ticket text in that file, or paste it", "put the ticket text in the file the message names", text)
        check_in("T329-6 ...beside the paste answer", "(c) ", text)
        check_not_in("T329-6 never the tracker's story for a person's file", "through its web interface", text)
        eq("T329-6 and it is the same `ticket_read` question", captured[0][0][0], "ticket_read")
        check_eq("T329-6 the question obeys human-questions.md", human_broken(text), [])
    finally:
        harness.cleanup(root)


def t335_b_n4_a_missing_ticket_file_flag_is_the_question_with_the_path_in_the_answer_block() -> None:
    """t-335 B-n4 (critic t-334): `--ticket-file <missing>` reached the conductor as a raw `Refusal` with the adapter's
    words, and the `person` branch of `s0_ticket_read_question` was reachable by no road. It is wired: the same
    `ticket_read` question, and the path - an instruction, human-questions.md rule 5 - stands in the answer block ONLY,
    never in the body. END TO END (a real driver process, the file adapter, the flag naming a file that is not there),
    then on the function."""
    missing_name = "no-such-ticket.md"
    root, task_root, env = s0_project("QA-1")
    try:
        missing = root / missing_name
        out = s0_run(root, env, "QA-1", "--ticket-file", str(missing))
        eq("T335 B-n4 `--ticket-file` naming a missing file: the person is asked (exit 3), not refused to the conductor",
           out.returncode, 3, out.stdout[-900:] + out.stderr[-600:])
        eq("T335 B-n4 the block is `ticket_read`, no model was called, and no 'tracker failed' mark is left for a later comparison",
           (s0_state(task_root).get("s0_block"), stub_calls(root), "s0_rest_failed" in s0_state(task_root)),
           ("ticket_read", [], False))
        ask = s0_question(task_root)
        body, _sep, answer_block = ask.partition("\n---\nAnswer:")
        check("T335 B-n4 the question has an answer block", bool(_sep), ask[-500:])
        check_not_in("T335 B-n4 the BODY never carries the missing path", missing_name, body)
        check_in("T335 B-n4 the answer block names it", f"The ticket file I looked for: {missing}", answer_block)
        check_in("T335 B-n4 the body says what is missing and points at the block", "named under \"How to answer\" below", body)
        check_not_in("T335 B-n4 the project's folder of ticket files is NOT what was looked at (kind `file` text is not used)",
                     "in the folder of ticket files", body)
        check_in("T335 B-n4 the three answers stand as priced option lines: not needed / retry / the paste, then `stop`",
                 "(a) `not needed` — ", body)
        check_in("T335 B-n4 the retry option", "(b) `retry` — put the ticket text in that file, and I read the ticket again", body)
        check_in("T335 B-n4 the paste option", "(c) paste the ticket here as text", body)
        check_in("T335 B-n4 and the stop option", "(d) `stop` — stop the story here; nothing runs", body)
        eq("T335 B-n4 the body obeys human-questions.md", human_broken(body), [])
        check_not_in("T335 B-n4 and the raw refusal is not relayed", "ticket_adapter get", ask)
        # the answer the person gives is read as for any ticket_read stop: a paste becomes the ticket
        pasted = s0_answer(root, env, "QA-1", "# Pasted title\n\nSome description.\n\n## Acceptance criteria\n- one thing\n", "--ticket-file", str(missing))
        snapshot = task_root / "work" / "ticket-snapshot.json"
        taken = json.loads(snapshot.read_text(encoding="utf-8")) if snapshot.is_file() else {}
        eq("T335 B-n4 the paste is taken: the snapshot is the pasted ticket, labelled as the person's (no second question)",
           (taken.get("title"), (taken.get("provenance") or {}).get("source")), ("Pasted title", "person_pasted"),
           pasted.stdout[-600:] + pasted.stderr[-300:])
    finally:
        harness.cleanup(root)
    # --- the function: with and without the file the adapter names; the project's kind does not change a flag's own file
    root, task_root, env = d2_seed("QA-9", environment="Local", pending=False)
    try:
        driver = driver_for(root, env, "QA-9")
        captured = []
        driver.s0_stop = lambda *a, **k: captured.append((a, k))
        failure = {"owner": "person", "status": None, "retry_at": None, "from_object": True,
                   "message": "ticket file not found: C:/x/mine.md", "file": "C:/x/mine.md"}
        said = "ticket_adapter: ticket file not found: C:/x/mine.md"
        driver.config = dict(driver.config, adapters={"ticket": {"kind": "file", "path": "C:/folder"}})
        driver.s0_ticket_read_question(1, said, failure, own_file=True)
        text, kwargs = captured[-1][0][2], captured[-1][1]
        check_not_in("T335 B-n4 (function, kind file + own_file) the body has no path", "mine.md", text)
        eq("T335 B-n4 (function) the note carries it", kwargs.get("answer_note"), "The ticket file I looked for: C:/x/mine.md")
        check_in("T335 B-n4 (function) the adapter's own sentence goes to the details, with the path",
                 "ticket file not found: C:/x/mine.md", str(kwargs.get("details")))
        driver.state.pop("s0_rest_failed", None)
        driver.s0_ticket_read_question(1, said, failure, own_file=True)
        check("T335 B-n4 (function) own_file leaves no `s0_rest_failed`", "s0_rest_failed" not in driver.state)
        driver.s0_ticket_read_question(1, said, failure)
        text = captured[-1][0][2]
        check("T335 B-n4 control: the project's kind `file` question is the one for a read that is NOT the flag's file",
              "in the folder of ticket files" in text and "mine.md" not in text)
        driver.config = dict(driver.config, adapters={"ticket": {"kind": "jira"}})
        driver.s0_ticket_read_question(1, said, dict(failure, file=None))
        text, kwargs = captured[-1][0][2], captured[-1][1]
        check_in("T335 B-n4 control: an adapter that names no file is relayed as before (the sentence, the old way on)",
                 "ticket file not found: C:/x/mine.md", text)
        eq("T335 B-n4 control: ...and no answer note", kwargs.get("answer_note"), "")
    finally:
        harness.cleanup(root)


def s6_the_manual_block_waits_for_the_writer_lock() -> None:
    """legacy-2406 W2 (M8): the manual S6 runner's in-process controller is a lifecycle command, like every CLI `main`:
    it waits for an in-flight writer instead of failing at once. The wait is `event_store.LIFECYCLE_WAIT_SECONDS`, read
    at CALL time (so a test can shorten it); the only Controller this block builds is that one."""
    import event_store
    task = "QA-9"
    root, task_root, env = d2_seed(task, environment="Local", pending=False)
    try:
        cases = [f"QA-9_TC_{i:03d}" for i in (1, 2)]
        driver, world, launched, moves = manual_rig(root, env, task, cases)
        saved = event_store.LIFECYCLE_WAIT_SECONDS
        event_store.LIFECYCLE_WAIT_SECONDS = 7
        try:
            enter_manual(driver, world, cases)
        finally:
            event_store.LIFECYCLE_WAIT_SECONDS = saved
        check_eq("the manual S6 block is dispatched by a controller that waits for the writer lock (the shortened value is read at call time)",
                 world.waits, [7])
        check_eq("and it did dispatch: one runner, for the block", [(e["role"], e["scope"]) for e in launched],
                 [("qa-runner", cases)])
        driver, world, launched, moves = manual_rig(root, env, task, cases)
        enter_manual(driver, world, cases)
        check_eq("control: unshortened, the wait is the module's own constant", world.waits, [saved])
    finally:
        harness.cleanup(root)


def main() -> None:
    run_scenarios([], [
        s6_the_manual_block_waits_for_the_writer_lock,
        t335_b_n4_a_missing_ticket_file_flag_is_the_question_with_the_path_in_the_answer_block,
        t329_item6_a_ticket_file_of_the_person_is_a_question_not_a_factory_fault,
        t329_b268_a_role_in_flight_is_written_while_it_runs_and_removed_when_it_returns,
        t292_k15_to_k18_the_question_comes_before_any_block,
        t292_k19_the_answers_have_an_executor,
        t292_k20_to_k24_the_pass_is_read_only_while_the_account_is_missing,
        t292_the_real_policy_reader_and_the_question_titles,
        t308_f6_the_reason_the_person_reads_is_the_true_one,
        ep1_41f_cases_all_on_a_device_skip_only_the_default_account,
    ])
    harness.finish("test_story_run_s6_t292")


# split: runner piece 1
if __name__ == "__main__":
    main()
