#!/usr/bin/env python3
"""B-364 (= B-259, D-0027): the driver re-reads the ticket for freshness, on the skill's one command and its one trigger.

`ticket_adapter.py freshness` is the one command and the 6 hour window the one trigger (phases/s0.md section 2b); what
this file holds is the driver's side of it, in process, over a real `file` ticket adapter, a real controller and
spies on `py_stdout` (the adapter's answers where a real one cannot be made to give them), `log_append` (the real
journal is read) and the role runs (`run_role` is replaced by a stub that accepts or leaves running):

  K1  the window at and beyond (T+6h / T+6h+1s), the call's argv and timeout
  K2-K4  `none`, `context`, `requirements` (the question: human words, details, baseline bytes, `.next`, one event)
  K5  `old text`: the declined mark, the whole words kept as a remark, a words file, not asked again
  K6-K7  `new text`: S2 then S3 with cause `ticket_changed` (S3 only after S2 was accepted), gate A reopened with its
         top line (and `prepare_stage S4` before `await_gate A`), S5-S8 work of the scope invalidated; the same with no
         gate A decided (no reopen); the rework's own edges (running, superseded, a second change, no accepted work)
  K8-K9  `stop`, then a no-answer run (asked again from the files, no tracker read); an answer that is not a token
  K10-K14  the exits: throttle at/beyond 6 h and a stamp from the future, timeout, exit 5 (auth, `intermediary`),
         exit 4 / 2 / a non-object, exit 1 by owner
  K15-K20  the positions: not in the process that ran S0, not while another question is open, after the answer is
         recorded, not in the answer run; pasted argv; `launch.ticket_not_needed` written before the pop; no
         controller; a closed story; gate B's check before the rehearsal
  K21-K26  the options constant is in s0.md; no baseline; `.next` after a crash; an answer after `.next` is gone;
         the driver's word is the safe side for the reviewers (judge and route)
"""
import contextlib
import hashlib
import io
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_eq, check_in, check_not_in  # noqa: E402
from story_run_common import (  # noqa: E402
    FIXTURE_TICKET,
    OTHER_SCRIPT,
    d3_s8_done,
    driver_for,
    human_broken,
    run_scenarios,
    s0_answer,
    s0_journal,
    s0_project,
    s0_run,
    s0_state,
    seed,
    stub_calls,
)
import human_text  # noqa: E402

KEY = "QA-1"
UTC = timezone.utc
UNREAD = "is not one of the answers this question takes, so nothing has moved yet."      # the ONE lead of an unread answer


# --- the scaffolding ---------------------------------------------------------------------------------------------
def iso(when: datetime) -> str:
    return when.isoformat(timespec="seconds")


def now_whole() -> datetime:
    return datetime.now(UTC).replace(microsecond=0)


def adapter(root: Path, env: dict, task_root: Path, *args):
    """The real `ticket_adapter.py freshness` of the project, the way the driver runs it."""
    out = harness.run_script("ticket_adapter.py", "freshness", KEY, "--task-root", str(task_root), "--json", *args,
                             cwd=root, env=env)
    return out, (json.loads(out.stdout) if out.stdout.strip().startswith("{") else {})


def freshness_project(ticket: str = FIXTURE_TICKET):
    """(root, task_root, env, the ticket file): a seeded story, a `file` adapter over tickets/QA-1.md, and the baseline
    the story was built on - written by the adapter's own first look, so its stamp is now (the story has been checked)."""
    root, task_root, env = seed(KEY)
    tickets = root / "tickets"
    tickets.mkdir()
    ticket_file = tickets / f"{KEY}.md"
    ticket_file.write_text(ticket, encoding="utf-8")
    config = root / "qa-factory" / "config.json"
    cfg = json.loads(config.read_text(encoding="utf-8"))
    cfg["adapters"] = {"ticket": {"kind": "file", "path": str(tickets)}}
    config.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    (task_root / "work" / "ticket-freshness.json").unlink()          # seed stamped it; the first look must write the baseline
    out, got = adapter(root, env, task_root)
    check_eq("setup: the adapter's first look writes the baseline", (out.returncode, got.get("result")), (0, "baseline_written"))
    return root, task_root, env, ticket_file


def record(task_root: Path) -> dict:
    return json.loads((task_root / "work" / "ticket-freshness.json").read_text(encoding="utf-8"))


def set_checked(task_root: Path, when: datetime, **extra) -> None:
    path = task_root / "work" / "ticket-freshness.json"
    data = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    data.update(checked_at=iso(when), **extra)
    path.write_text(json.dumps(data), encoding="utf-8")


def make_due(task_root: Path) -> None:
    set_checked(task_root, datetime.now(UTC) - timedelta(hours=7))


def edit_requirements(ticket_file: Path) -> None:
    ticket_file.write_text(ticket_file.read_text(encoding="utf-8").replace(
        "at most 5 tags; a sixth tag", "at most 7 tags; an eighth tag"), encoding="utf-8")


def edit_comments(ticket_file: Path) -> None:
    ticket_file.write_text(ticket_file.read_text(encoding="utf-8") + "- **qa** (2026-09-12): one more comment.\n", encoding="utf-8")


def events(root: Path, name: str) -> list:
    return [row for row in s0_journal(root) if row.get("event") == name]


def snap_bytes(task_root: Path) -> bytes:
    return (task_root / "work" / "ticket-snapshot.json").read_bytes()


def spy_stdout(driver, answer=None):
    """Record every `py_stdout` call as (script, args, kwargs); `answer(args, kwargs)` -> (code, out, err) stands in for the
    adapter, or None passes the call on to the real thing."""
    calls = []
    real = driver.py_stdout

    def spy(script, *args, **kwargs):
        calls.append((script, args, kwargs))
        if answer is not None and script == "ticket_adapter.py":
            return answer(args, kwargs)
        return real(script, *args, **kwargs)
    driver.py_stdout = spy
    return calls


def adapter_calls(calls: list) -> list:
    return [c for c in calls if c[0] == "ticket_adapter.py"]


def looked(driver, *args, **kwargs):
    """(what `ticket_freshness` returned or raised, what it printed)."""
    printed = io.StringIO()
    try:
        with contextlib.redirect_stdout(printed):
            got = driver.ticket_freshness(*args, **kwargs)
    except Exception as exc:
        got = exc
    return got, printed.getvalue()


def entered(driver):
    """(what `ticket_freshness_entry` returned or raised, what it printed): a mutant that lets a look through is a FAIL
    line here, never a crash."""
    printed = io.StringIO()
    try:
        with contextlib.redirect_stdout(printed):
            got = driver.ticket_freshness_entry()
    except Exception as exc:
        got = exc
    return got, printed.getvalue()


def person_of(got):
    import story_run
    return got if isinstance(got, story_run.Person) else None


def error_object(owner: str, message: str, status=None) -> str:
    return json.dumps({"ok": False, "owner": owner, "status": status, "retry_at": None, "message": message}
                      | ({"file": "jira-fields.json"} if owner in ("factory", "person") else {}))


def question_of(driver, person) -> str:
    """The question as `ask()` writes it, the file the person reads."""
    printed = io.StringIO()
    with contextlib.redirect_stdout(printed):
        driver.ask(person)
    return driver.question_path().read_text(encoding="utf-8")


def answer_file(root: Path, words: str) -> str:
    path = root / "answer.md"
    path.write_bytes(words.encode("utf-8"))
    return str(path)


def asked_driver(root: Path, env: dict, task_root: Path, ticket_file: Path, **overrides):
    """A driver that has asked the changed-ticket question: the requirements moved, the check was due, the question is open."""
    edit_requirements(ticket_file)
    make_due(task_root)
    driver = driver_for(root, env, KEY, **overrides)
    got, _ = looked(driver)
    person = person_of(got)
    check("setup: the requirements moved, so the question is asked", person is not None and person.kind == "ticket_changed", repr(got))
    question_of(driver, person)
    return driver, person


# --- K1 the window, the call --------------------------------------------------------------------------------------
def k1_the_window_at_and_beyond() -> None:
    root, task_root, env, _ticket = freshness_project()
    try:
        t0 = now_whole() - timedelta(hours=1)
        set_checked(task_root, t0, result="none")
        driver = driver_for(root, env, KEY)
        calls = spy_stdout(driver)
        got, printed = looked(driver, now=t0 + timedelta(hours=6))
        check_eq("K1: exactly 6 h after the last check: skipped, no subprocess, no print", (got, len(calls), printed), ("skipped", 0, ""))
        got, printed = looked(driver, now=t0 + timedelta(hours=6, seconds=1))
        said = adapter_calls(calls)
        check_eq("K1: 6 h and a second: the adapter runs once", (got, len(said)), ("none", 1))
        script, args, kwargs = said[0]
        check_eq("K1: the call is `freshness <task> --task-root <root> --json`, no --ticket-file on a tracker story",
                 (args[:3], Path(args[3]).resolve(), args[4:]), (("freshness", KEY, "--task-root"), task_root.resolve(), ("--json",)))
        check_eq("K1: with the 300 s ceiling, and the adapter's stderr not echoed twice", (kwargs.get("timeout"), kwargs.get("echo")), (300, False))
        check_eq("K1: nothing is printed for `none`", printed, "")
        check("K1: the adapter stamped the check (the trigger is measured from it)",
              abs((datetime.now(UTC) - datetime.fromisoformat(record(task_root)["checked_at"])).total_seconds()) < 120)
        # a story past the window is never resumed without a look; one inside it is never re-read
        calls.clear()
        got, _ = looked(driver)
        check_eq("K1: right after the look it is not due again: no second read", (got, len(calls)), ("skipped", 0))
    finally:
        harness.cleanup(root)


# --- K2-K4 what the adapter finds -----------------------------------------------------------------------------------
def k2_k3_none_and_context() -> None:
    root, task_root, env, ticket = freshness_project()
    try:
        driver = driver_for(root, env, KEY)
        before = snap_bytes(task_root)
        make_due(task_root)
        got, printed = looked(driver)
        check_eq("K2: an unchanged ticket: `none`, silent, the baseline is not rewritten", (got, printed, snap_bytes(task_root) == before), ("none", "", True))
        edit_comments(ticket)
        make_due(task_root)
        got, printed = looked(driver)
        check_eq("K3: a new comment is `context`", got, "context")
        check_in("K3: one line, in words: what changed, and that the story goes on",
                 f"ticket {KEY} changed while the story waited (the comments); the story goes on", printed)
        check("K3: the baseline was replaced (nothing is re-planned)", snap_bytes(task_root) != before)
        check_eq("K3: and no question is open", driver.state.get("asked"), {})
    finally:
        harness.cleanup(root)


def k4_requirements_is_the_persons_question() -> None:
    root, task_root, env, ticket = freshness_project()
    try:
        before = snap_bytes(task_root)
        edit_requirements(ticket)
        make_due(task_root)
        driver = driver_for(root, env, KEY)
        got, _ = looked(driver)
        person = person_of(got)
        check("K4: requirements -> a Person", person is not None, repr(got))
        check_eq("K4: kind and stage", (person.kind, person.stage), ("ticket_changed", "S0"))
        check_eq("K4: the question breaks no rule of human-questions.md (with the answer block `ask()` adds)",
                 human_broken(person.text), [])
        check_in("K4: it says what changed, in words", "the acceptance criteria", person.text)
        check_in("K4: it says the old text is kept and the new one set aside", "kept the text the story was built on and set the new text aside", person.text)
        check_in("K4: it quotes the three answers, word for word", "re-run S2–S3 against the new text · continue on the old text with that stated as a known gap · stop here.", person.text)
        check("K4: and ends with the priced section: the tokens it reads as option lines, and what the first line means",
              all(f"`{t}` — " in person.text.split("## What each answer costs and does")[1] for t in ("new text", "old text", "stop"))
              and "anything you write after the first line is kept with your answer for gate B" in person.text, person.text[-600:])
        check_eq("K4: every option has its three price lines (item 6)", human_text.price_problems(person.text, None), [])
        check_not_in("K4: no path and no command in the body", "ticket-snapshot", person.text)
        details = json.loads(person.details)
        check("K4: the details hold the fields the adapter named", "acceptance_criteria" in details["changed"] and "detail" in details and "revisions" in details, person.details[:200])
        check_eq("K4: the baseline's bytes are unchanged", snap_bytes(task_root), before)
        check("K4: and the new text waits beside it", (task_root / "work" / "ticket-snapshot.next.json").is_file())
        check_eq("K4: exactly one `ticket_changed` event is journaled (by the adapter)", len(events(root, "ticket_changed")), 1)
        # the same text again, with nobody having answered: still the question, and still ONE event
        again, _ = looked(driver, now=datetime.now(UTC) + timedelta(hours=7))
        check_eq("K4: asked again from a due look: the same question, no second event", (person_of(again) is not None, len(events(root, "ticket_changed"))), (True, 1))
    finally:
        harness.cleanup(root)


# --- K5 old text ----------------------------------------------------------------------------------------------------
def k5_old_text() -> None:
    root, task_root, env, ticket = freshness_project()
    try:
        driver, person = asked_driver(root, env, task_root, ticket)
        words = "old text\nthe criterion on tag limits is a typo fix, the plan stands"
        with contextlib.redirect_stdout(io.StringIO()):
            driver.take_ticket_answer(words, "# q\n", "S0", "")
        pipeline = json.loads((task_root / "pipeline.json").read_text(encoding="utf-8"))
        remarks = pipeline.get("remarks") or []
        check("K5: the WHOLE answer is kept as a remark of S0", any(r.get("stage") == "S0" and "typo fix, the plan stands" in str(r) for r in remarks), json.dumps(remarks)[:300])
        check("K5: the declined mark is recorded", bool((record(task_root).get("declined") or {}).get("hash")))
        files = sorted((task_root / "state" / "words").glob("driver-ticketdecline-*.txt"))
        check_eq("K5: the words went to the adapter by file, whole", [f.read_text(encoding="utf-8") for f in files], [words])
        check("K5: the waiting text stays beside the baseline", (task_root / "work" / "ticket-snapshot.next.json").is_file())
        check_eq("K5: no rework is owed", driver.state.get("ticket_rework"), None)
        make_due(task_root)
        got, printed = looked(driver)
        check_eq("K5: the next due check says it is the declined text and goes on (not asked again)", got, "declined")
        check_in("K5: in one line with the date", "is the one declined on", printed)
        check_eq("K5: and journals no second `ticket_changed` event", len(events(root, "ticket_changed")), 1 + 1)   # the question's, then the adapter's `declined:` decision
    finally:
        harness.cleanup(root)


# --- K6-K7 new text -------------------------------------------------------------------------------------------------
def gate_a_story(decided: bool = True, late: bool = False):
    """(root, task_root, env, ticket file, controller): S0..S4 accepted and gate A approved on scope TC-1 - and S5 accepted
    when `late` - over the same file adapter as `freshness_project`."""
    root, task_root, env, ticket = freshness_project()
    import test_controller_rework_scope as SCOPED
    import test_controller_state as BASE
    from controller import Controller
    c = Controller(task_root)
    c.apply("revise_plan", {"scope": ["TC-1"], "plan_revision": "src-1", "reason": "test setup: the story's scope",
                            "idempotency_key": "scope"})
    for number in range(5 if decided else 4):
        BASE.accept_stage(c, task_root, f"S{number}")
    if decided:
        BASE.seed_plan(task_root, [SCOPED.plan_row(1, "automate")])
        c.apply("decision", BASE.bind_gate_a(task_root, {"id": "gate-a", "gate": "A", "action": "approve", "status": "approved",
                                                          "authorization_source": "human", "source_revision": "src-1", "scope": ["TC-1"],
                                                          "input_revision": "src-1", "idempotency_key": "gate-a"}))
    if late:
        BASE.accept_stage(c, task_root, "S5")
    return root, task_root, env, ticket, c


def strategist_closed_s3(controller, task_root: Path) -> None:
    """`BASE.accept_stage` closes S3 with a `qa-worker` dispatch, but the rework of S3 goes back over the work of the strategist
    (`ticket_rework_step`: "a first look accepted after the strategist is not the author"): give S3 the strategist's accepted work."""
    controller.apply("dispatch", {"id": "dS3-strategist", "stage": "S3", "role": "qa-test-strategist", "scope": ["TC-1"], "input_hash": "S3",
                                  "budget": {}, "known_paths": {}, "idempotency_key": "dispatch-S3-strategist"})
    evidence = task_root / "S3-strategist.txt"
    evidence.write_text("S3-strategist", encoding="utf-8")
    controller.apply("accept", {"id": "dS3-strategist", "status": "accepted", "stage_complete": False, "idempotency_key": "accept-S3-strategist",
                                "evidence_refs": [{"path": evidence.name, "sha256": hashlib.sha256(evidence.read_bytes()).hexdigest()}]})


def staged_driver(root: Path, env: dict, task_root: Path, accept: dict):
    """A driver whose roles are recorded, not run: `accept["on"]` says whether the stub closes the dispatch it was sent to."""
    driver = driver_for(root, env, KEY, max_boundaries=12)
    started = []

    def fake_role(stage, role, scope=None, extra=None, complete=None, rework=None, **kwargs):
        started.append((stage, role, (rework or {}).get("id"), complete))
        if accept["on"]:
            accept_dispatch(task_root, (rework or {}).get("id"), bool(complete))
        return "", None
    driver.run_role = fake_role
    driver.started = started
    return driver


def accept_dispatch(task_root: Path, dispatch_id: str, complete: bool = True) -> None:
    import hashlib
    from controller import Controller
    evidence = task_root / f"{dispatch_id}.txt"
    evidence.write_text(dispatch_id, encoding="utf-8")
    if complete:
        # X2-7: a stage with an acceptor closes over the critic's record of THIS dispatch (a refusal raises StateConflict out of `apply`: loud)
        # the record names the dispatch the controller reads as the stage's author (`""` for a fixture role that is not the stage's first)
        import acceptance
        from test_controller_state import record_stage_acceptance
        state = Controller(task_root).state()
        held = state["dispatches"][dispatch_id]
        record_stage_acceptance(task_root, held["stage"], reviewed_dispatch=acceptance.stage_author_dispatch(state, acceptance.stage_def_of(held["stage"]), held))
    Controller(task_root).apply("accept", {"id": dispatch_id, "status": "accepted", "stage_complete": complete,
                                           "evidence_refs": [{"path": evidence.name, "sha256": hashlib.sha256(evidence.read_bytes()).hexdigest()}],
                                           "idempotency_key": "accept-" + dispatch_id})


def state_of(task_root: Path) -> dict:
    from controller import Controller
    return Controller(task_root).state()


def k6_k7_new_text_reworks_s2_then_s3_then_reopens_gate_a() -> None:
    root, task_root, env, ticket, controller = gate_a_story(decided=True, late=True)
    try:
        strategist_closed_s3(controller, task_root)
        driver, _person = asked_driver(root, env, task_root, ticket)
        accept = {"on": False}
        stub = staged_driver(root, env, task_root, accept)
        stub.state = driver.state                                   # the same driver's state, a fresh process's roles
        stub.state["asked"] = {"kind": "ticket_changed", "stage": "S0", "dispatch": "", "at": "x"}
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            stub.take_ticket_answer("new text", "# q\n", "S0", "")
        check("K6: `new text` adopted the waiting text: `.next` is gone", not (task_root / "work" / "ticket-snapshot.next.json").is_file())
        check_in("K6: and it says so in words", "the new ticket text is adopted; the requirements and the plan are made again from it", printed.getvalue())
        owed = stub.state.get("ticket_rework") or {}
        check_eq("K6: S2 and S3, the stages the controller holds completed, in order", (owed.get("stages"), owed.get("words")), (["S2", "S3"], "new text"))
        check("K6: the person's words are on the journal's record (FR-8)", any("new text" in str(r.get("notes")) for r in events(root, "human_answer")))
        # S2 first; it is left running, so S3 must NOT be registered (the controller refuses a second running dispatch anyway)
        with contextlib.redirect_stdout(io.StringIO()):
            check_eq("K6: the first turn moves", stub.ticket_rework_step(), True)
            check_eq("K6: S2 is sent back with cause `ticket_changed` and complete=True", [(s, c) for s, _r, _i, c in stub.started], [("S2", True)])
            check_eq("K6: S2 left running: the next turn leaves it to the loop (False), and S3 is NOT registered", (stub.ticket_rework_step(), len(stub.started)), (False, 1))
        s2 = state_of(task_root)["dispatches"][stub.started[0][2]]
        check_eq("K6: the dispatch carries the cause and the words as its reason", (s2["repair_cause"], s2["reason"], s2["status"]), ("ticket_changed", "new text", "running"))
        accept_dispatch(task_root, stub.started[0][2], True)
        accept["on"] = False
        with contextlib.redirect_stdout(io.StringIO()):
            check_eq("K6: S2 accepted: S3 is registered now", (stub.ticket_rework_step(), [s for s, *_ in stub.started]), (True, ["S2", "S3"]))
        if not check_eq("K6: the S3 dispatch is there to be accepted", len(stub.started), 2):
            return
        s3_id = stub.started[1][2]
        accept_dispatch(task_root, s3_id, True)
        state = state_of(task_root)
        check_eq("K6: S2 and S3 stay completed (a re-run lowers nothing)", (state["stages"]["S2"]["status"], state["stages"]["S3"]["status"]), ("completed", "completed"))
        # K7: S2 and S3 are done again: gate A, decided on the old requirements, is asked again - and the automation built on them goes
        stub.save_state()
        with contextlib.redirect_stdout(printed := io.StringIO()):
            check_eq("K7: the next turn reopens gate A", stub.ticket_rework_step(), True)
        state = state_of(task_root)
        check_eq("K7: the approved gate A decision is stale", [d["status"] for d in state["decisions"].values() if d.get("gate") == "A"], ["stale"])
        check_eq("K7: S4 is pending, reopened", (state["stages"]["S4"]["status"], state["stages"]["S4"].get("gate_a_reopened")), ("pending", True))
        reopens = state.get("reopens") or []
        check_eq("K7: one reopen, the person's words as the reason, on the story's scope",
                 (len(reopens), reopens[0]["reason"].startswith("the person chose the changed ticket text: new text"), reopens[0]["affected_scope"]), (1, True, ["TC-1"]))
        check_eq("K7: S5 stood completed: its accepted work of the scope is invalidated, the stage is pending again",
                 (state["stages"]["S5"]["status"], [d["status"] for d in state["dispatches"].values() if d["stage"] == "S5"]), ("pending", ["stale", "stale"]))
        check_eq("K7: the rework is done: nothing owed, the note for gate A is set",
                 (stub.state.get("ticket_rework"), "Gate A is asked again" in (stub.state.get("gate_note") or {}).get("A", "")), (None, True))
        with contextlib.redirect_stdout(io.StringIO()):
            check_eq("K7: and a later turn has nothing to do", stub.ticket_rework_step(), False)
        # what the loop answers: the full S4 run first, THEN gate A
        first = stub.where()
        check_eq("K7: `where` answers prepare_stage S4 (a full re-run), before any await_gate A", (first.get("action"), first.get("stage")), ("prepare_stage", "S4"))
        import test_controller_state as BASE
        BASE.accept_case_review_stage(controller, task_root, "s4-redo")
        second = stub.where()
        check_eq("K7: once S4 is accepted again, gate A is asked", (second.get("action"), second.get("gate")), ("await_gate", "A"))
        # the gate's text carries the line, once
        stub.gate_text = lambda gate: "the packet"
        person = None
        try:
            stub.gate("A", top="the rest")
        except Exception as exc:
            person = exc
        check("K7: the gate A question starts with the line that says why it comes again, then the rest",
              person is not None and person.text.startswith(f"# Gate A — {KEY}\n\nGate A is asked again: you chose the new ticket text, and the requirements and the plan were made again from it.\n\nthe rest"),
              getattr(person, "text", "")[:300])
        check_eq("K7: the line is popped: the next ask of the gate does not repeat it", stub.state.get("gate_note", {}).get("A"), None)
        # t-694 F4: ONE carrier. The writer wrote `gate_note` (above); the old key is neither written nor read any more.
        check_eq("F4: the reopen wrote no `ticket_gate_note`", "ticket_gate_note" in stub.state, False)
        stub.state["ticket_gate_note"] = {"A": "a line an older driver left in its state file"}
        left_over = None
        try:
            stub.gate("A", top="")
        except Exception as exc:
            left_over = exc
        check_not_in("F4: and a leftover `ticket_gate_note` is not read at the gate (named in the report as dropped)",
                     "an older driver", getattr(left_over, "text", ""))
        check_eq("K7: no conductor was called anywhere on the way (the answer is a token, read by code, never a meaning)",
                 [c for c in stub_calls(root) if c["kind"] == "conductor"], [])
    finally:
        harness.cleanup(root)


def k7b_gate_a_not_decided_is_not_reopened() -> None:
    root, task_root, env, ticket, controller = gate_a_story(decided=False)
    try:
        strategist_closed_s3(controller, task_root)
        driver, _ = asked_driver(root, env, task_root, ticket)
        accept = {"on": True}
        stub = staged_driver(root, env, task_root, accept)
        stub.state = driver.state
        with contextlib.redirect_stdout(io.StringIO()):
            stub.take_ticket_answer("new text", "# q\n", "S0", "")
        check_eq("K7b: S2 and S3 are owed", (stub.state.get("ticket_rework") or {}).get("stages"), ["S2", "S3"])
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            turns = []
            for _ in range(5):
                turns.append(stub.ticket_rework_step())
        check_eq("K7b: S2, then S3 are re-run and accepted; the last turns reach the reopen's turn and then nothing", turns, [True, True, True, False, False])
        check_eq("K7b: no gate A was decided: no reopen is recorded", state_of(task_root).get("reopens") or [], [])
        check_in("K7b: one line says so", "no approved gate A to ask again", printed.getvalue())
        check_eq("K7b: the rework is done and no note is left", (stub.state.get("ticket_rework"), "gate_note" in stub.state), (None, False))
    finally:
        harness.cleanup(root)


def k7c_the_reworks_own_edges() -> None:
    """The step's state machine over a fake controller state: running, a stopped dispatch, a person's word, a second change,
    no accepted work - each its own move (FR-42)."""
    root, task_root, env, _ticket = freshness_project()
    try:
        driver = driver_for(root, env, KEY)
        (task_root / "state").mkdir(exist_ok=True)
        (task_root / "state" / "controller.json").write_text("{}", encoding="utf-8")       # the controller exists (B5)
        rework_calls = []
        driver.rework = lambda stage, role, cases, reason, **kw: rework_calls.append((stage, role, cases, reason, kw))
        holder = {"dispatches": {}, "stages": {}}
        driver.controller_state = lambda: holder
        driver.ticket_reopen_gate_a = lambda pending: rework_calls.append(("reopen", dict(pending)))

        def owed(stages, before=()):
            driver.state["ticket_rework"] = {"stages": list(stages), "words": "new text", "at": "t", "before": list(before)}

        def step():
            with contextlib.redirect_stdout(io.StringIO()):
                return driver.ticket_rework_step()
        accepted_s2 = {"id": "S2-qa-requirements-tester-1", "stage": "S2", "role": "qa-requirements-tester", "status": "accepted"}
        # nothing owed
        driver.state.pop("ticket_rework", None)
        check_eq("K7c: nothing owed: False, nothing called", (step(), rework_calls), (False, []))
        # a running dispatch anywhere: the loop's, not ours
        owed(["S2"])
        holder["dispatches"] = {"x": {"stage": "S5", "status": "running"}, accepted_s2["id"]: accepted_s2}
        check_eq("K7c: a dispatch is running: False, nothing registered", (step(), rework_calls), (False, []))
        # S2 has accepted work: it is registered, with the role of its last accepted dispatch, complete=True
        holder["dispatches"] = {accepted_s2["id"]: accepted_s2}
        check_eq("K7c: S2 with accepted work: registered", step(), True)
        check_eq("K7c: with the role of that dispatch, no cases, the person's words, cause `ticket_changed`, complete=True",
                 rework_calls, [("S2", "qa-requirements-tester", [], "new text", {"cause": "ticket_changed", "complete": True})])
        rework_calls.clear()
        # S2's re-run exists and is stopped (not accepted): the loop resolves it
        mine = {"id": "S2-qa-requirements-tester-2", "stage": "S2", "role": "qa-requirements-tester", "status": "incomplete", "repair_cause": "ticket_changed"}
        holder["dispatches"][mine["id"]] = mine
        check_eq("K7c: its re-run stopped: False (the loop's `where` resolves it), nothing registered twice", (step(), rework_calls), (False, []))
        # set aside before it was accepted - the controller's own words (a person's release, a retry that took its place,
        # an invalidation), never literals of ours: the rework ends with one line, the rest is not re-run, and the person's
        # choice of the new text still stands, so gate A is still asked again (the reopen move), never left on the old text
        import controller as C
        for status in (C.RELEASED, "superseded", "stale"):
            mine["status"] = status
            owed(["S2", "S3"])
            rework_calls.clear()
            printed = io.StringIO()
            with contextlib.redirect_stdout(printed):
                moved = driver.ticket_rework_step()
            check_eq(f"K7c: the re-run `{status}`: no more re-runs, the gate A move follows, the list is gone",
                     (moved, [c[0] for c in rework_calls], driver.state.get("ticket_rework")), (True, ["reopen"], None))
            check_in(f"K7c: the re-run `{status}`: one line says it was set aside and gate A is still asked again", "was set aside before it was accepted", printed.getvalue())
        mine["status"] = C.NEVER_STARTED
        owed(["S2"])
        rework_calls.clear()
        check_eq("K7c: a re-run that never started is the loop's to relaunch (`where`): False, nothing else moves", (step(), rework_calls), (False, []))
        rework_calls.clear()
        # a second change of the ticket: the earlier re-run is NOT this one's (the `before` list), so S2 is owed again
        mine["status"] = "accepted"
        owed(["S2"], before=[mine["id"]])
        check_eq("K7c: a second ticket change is owed its own re-run, not satisfied by the first", (step(), [c[0] for c in rework_calls]), (True, ["S2"]))
        rework_calls.clear()
        # this change's own re-run accepted: popped; the list is empty: the gate A move is asked for
        owed(["S2"])
        check_eq("K7c: this change's re-run accepted: the stage is done, then the gate A move", (step(), [c[0] for c in rework_calls]), (True, ["reopen"]))
        check_eq("K7c: and the list is gone", driver.state.get("ticket_rework"), None)
        rework_calls.clear()
        # a stage with no accepted work gets no rework and one line (K25)
        owed(["S6"])
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            moved = driver.ticket_rework_step()
        check_eq("K25: a stage with no accepted dispatch: no rework, skipped, then the gate A move", (moved, [c[0] for c in rework_calls]), (True, ["reopen"]))
        check_in("K25: one line says so", "S6 has no accepted work to make again; skipped", printed.getvalue())
        # no controller.json (B5): never
        (task_root / "state" / "controller.json").unlink()
        owed(["S2"])
        rework_calls.clear()
        check_eq("K18b: no controller.json: no rework, whatever is owed", (step(), rework_calls), (False, []))
    finally:
        harness.cleanup(root)


def k7d_the_reopen_sets_aside_the_late_work_and_names_what_it_cannot() -> None:
    """F3 over a fake controller: (a) a half-done S5 (pending, accepted windows) is invalidated like a completed one; (b) a
    completed stage no dispatch of the scope names (closed by code, or scopeless) is NAMED in the line and at gate A's top;
    (c) a restart after the invalidate names the same stage and records nothing twice."""
    root, task_root, env, _ticket = freshness_project()
    try:
        driver = driver_for(root, env, KEY)
        calls = []
        driver.controller = lambda op, *a, input_data=None: calls.append((op, input_data)) or {}
        holder = {"source_revision": "r", "revision": 3, "scope": ["TC-1"],
                  "decisions": {"g": {"gate": "A", "status": "approved", "source_revision": "r"}}, "stages": {}, "dispatches": {}}
        driver.controller_state = lambda: holder

        def reopen(pending):
            printed = io.StringIO()
            with contextlib.redirect_stdout(printed):
                driver.ticket_reopen_gate_a(pending)
            return printed.getvalue()
        holder["stages"] = {"S5": {"status": "pending"}}
        holder["dispatches"] = {"dS5": {"stage": "S5", "status": "accepted", "scope": ["TC-1"]}}
        reopen({"words": "new text", "at": "t"})
        check_eq("F3a: S5 only PENDING with an accepted window: the reopen and the invalidate of that window",
                 ([c[0] for c in calls], (calls[1][1] or {}).get("dispatch_ids")), (["semantic_reopen", "invalidate"], ["dS5"]))
        check_eq("F3a: nothing is left unnamed: the note for gate A is the plain line", driver.state["gate_note"]["A"].count("Note that"), 0)
        # (b) S5 completed with its window; S6 closed by code (no dispatch); S7 has a dispatch that carries no scope
        calls.clear()
        holder["stages"] = {"S5": {"status": "completed"}, "S6": {"status": "completed"}, "S7": {"status": "completed"}}
        holder["dispatches"] = {"dS5": {"stage": "S5", "status": "accepted", "scope": ["TC-1"]}, "dS7": {"stage": "S7", "status": "accepted", "scope": []}}
        said = reopen({"words": "new text", "at": "t"})
        check_eq("F3b: the window of S5 is still invalidated", [(c[0], (c[1] or {}).get("dispatch_ids")) for c in calls][1:], [("invalidate", ["dS5"])])
        note = driver.state["gate_note"]["A"]
        check("F3b: the line and the top of gate A name EVERY completed stage nothing could set aside, in words",
              all(w in said and w in note for w in ("run (S6)", "triage (S7)", "made from the old text")) and "automation" not in note, said + " || " + note)
        # (c) a restart after the invalidate: the window is `stale` now, S5 is pending, S6 and S7 still stand
        calls.clear()
        holder["stages"] = {"S5": {"status": "pending"}, "S6": {"status": "completed"}, "S7": {"status": "completed"}}
        holder["dispatches"]["dS5"]["status"] = "stale"
        holder["decisions"]["g"]["status"] = "stale"
        driver.state.pop("gate_note", None)
        reopen({"words": "new text", "at": "t", "reopened": True, "invalidated": True})
        check_eq("F3c: a restart records nothing twice", calls, [])
        check("F3c: and still names S6 and S7, and not the stage that was set aside", "run (S6)" in driver.state["gate_note"]["A"]
              and "triage (S7)" in driver.state["gate_note"]["A"] and "automation" not in driver.state["gate_note"]["A"])
    finally:
        harness.cleanup(root)


def k7e_a_ticket_rework_finished_through_the_restart_route_is_complete() -> None:
    """F4: the R12 restart route is `wait_existing_job` on a registered dispatch this driver never launched; the ticket
    re-run of S2/S3 must close COMPLETE there too (the plan baseline is re-captured), while every other rework still does not."""
    root, task_root, env, ticket, _controller = gate_a_story(decided=True)
    try:
        driver, _ = asked_driver(root, env, task_root, ticket)
        accept = {"on": False}
        stub = staged_driver(root, env, task_root, accept)
        stub.state = driver.state
        with contextlib.redirect_stdout(io.StringIO()):
            stub.take_ticket_answer("new text", "# q\n", "S0", "")
            stub.ticket_rework_step()
        dispatch_id = stub.started[0][2]
        check_eq("setup: the re-run is registered and left running (the driver 'died' here)", state_of(task_root)["dispatches"][dispatch_id]["status"], "running")
        fresh = driver_for(root, env, KEY)
        seen = []
        fresh.run_role = lambda stage, role, **kw: seen.append((stage, kw.get("complete"), (kw.get("rework") or {}).get("id"))) or ("", None)
        with contextlib.redirect_stdout(io.StringIO()):
            fresh.dispatch_action({"action": "wait_existing_job", "dispatch_id": dispatch_id})
        # X2-7: S2 has an acceptor (`acceptance_by`), so the author's re-run does not close the stage (None, never True: the controller refuses an
        # author's closing accept without the critic's record); the closing is the critic route's, which the loop enters next (checked below)
        check_eq("F4: finished through the restart route, the ticket re-run of S2 leaves the closing to the stage critic", seen, [("S2", None, dispatch_id)])
        # the stage stays `completed` from its first run, so no turn of the loop enters S2 again: the restart route itself runs the critic
        # route over the accepted re-run (`ticket_rerun_critic`, AR-25/AR-28) - and only over an accepted one, once
        seen.clear()
        with contextlib.redirect_stdout(io.StringIO()):
            fresh.ticket_rerun_critic(dispatch_id)
            check_eq("F4: a re-run still running gets no critic yet", seen, [])
            accept_dispatch(task_root, dispatch_id, False)
            fresh.ticket_rerun_critic(dispatch_id)
            fresh.ticket_rerun_critic("no-such-dispatch")
        check_eq("F4: the accepted re-run of S2 is followed by the stage critic's route (one critic call, whose finish closes)",
                 [(stage, callable(done), rework) for stage, done, rework in seen], [("S2", True, None)])
        record = state_of(task_root)["dispatches"][dispatch_id]
        check_eq("F4 control: any other rework record still answers False (the `rework_of` rule is unchanged)",
                 (fresh.completion_for("S2", record["role"], dict(record, repair_cause=None)), fresh.completion_for("S4", "qa-case-designer", {"rework_of": "x", "repair_cause": "ticket_changed"})), (False, False))
    finally:
        harness.cleanup(root)


def k4b_an_unreadable_file_with_the_question_open_never_crashes() -> None:
    """F1: `ticket_field_words([])` used to raise IndexError, so with the baseline or the waiting text unreadable the open
    question crashed every run and every answer, with no door. The question is asked again, whatever the answer."""
    import story_run
    check_eq("F1: no names, no words (the callers say their own fallback)", (story_run.Driver.ticket_field_words([]), story_run.Driver.ticket_field_words(None)), ("", ""))
    for label, spoil in (("the waiting text", lambda task_root: (task_root / "work" / "ticket-snapshot.next.json").write_text("{ not json", encoding="utf-8")),
                         ("the baseline", lambda task_root: (task_root / "work" / "ticket-snapshot.json").write_text("{ not json", encoding="utf-8"))):
        root, task_root, env, ticket = freshness_project()
        try:
            asked_driver(root, env, task_root, ticket)
            spoil(task_root)
            got, _ = entered(driver_for(root, env, KEY))
            check(f"F1: {label} unreadable, question open: a run asks it again (no crash), saying nothing is named", person_of(got) is not None
                  and "something in the requirements" in got.text, repr(got))
            for words in ("stop", "maybe", "new text", "old text"):
                fresh = driver_for(root, env, KEY)
                try:
                    with contextlib.redirect_stdout(io.StringIO()):
                        fresh.take_ticket_answer(words, "# q\n", "S0", "")
                    outcome = "went on"
                except Exception as exc:
                    outcome = "asked again" if person_of(exc) is not None else repr(exc)
                check(f"F1: {label} unreadable, answer `{words}`: no crash (a Person, or the story goes on)", outcome in ("asked again", "went on"), outcome)
                if words in ("stop", "maybe"):
                    check_eq(f"F1: {label}, `{words}`: always asked again", outcome, "asked again")
        finally:
            harness.cleanup(root)
    root, task_root, env, _ticket = freshness_project()
    try:
        make_due(task_root)
        driver = driver_for(root, env, KEY)
        spy_stdout(driver, fixed_adapter(0, json.dumps({"result": "context", "changed": []})))
        got, printed = looked(driver)
        check_eq("F1: a `context` result naming no field is a line with a fallback, not a crash", (got, "(something)" in printed), ("context", True))
        spy_stdout(driver, fixed_adapter(0, json.dumps({"result": "requirements", "changed": [], "already_answered": True})))
        got, printed = looked(driver)
        check_eq("F1: an already-answered result naming no field: the same", (got, "(the requirements)" in printed), ("declined", True))
    finally:
        harness.cleanup(root)


# --- K8-K9 stop and the words that are not a token -------------------------------------------------------------------
def k8_stop_then_a_no_answer_run_asks_again_with_no_read() -> None:
    root, task_root, env, ticket = freshness_project()
    try:
        asked_driver(root, env, task_root, ticket)
        second = driver_for(root, env, KEY, answer=answer_file(root, "stop"))
        calls = spy_stdout(second)
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            code = second.run()
        check_eq("K8: `stop`: exit 3, the same question is open", (code, second.state["asked"].get("kind")), (3, "ticket_changed"))
        again = second.question_path().read_text(encoding="utf-8")
        import story_run
        held = story_run.Driver.stop_held("Answer `new text` or `old text` when you decide.")
        check_in("K8: the question comes back and says nothing runs (the ONE `stop_held` sentence)", held, again)
        check_eq("K8/F7: the held lines are there ONCE", again.count("You said to stop."), 1)
        check_eq("K8: nothing ran: no adapter call, no rework, the new text still waits", (adapter_calls(calls), second.state.get("ticket_rework"), (task_root / "work" / "ticket-snapshot.next.json").is_file()), ([], None, True))
        check("K8: the words are on the record, whole, before the question comes back (journal and driver-answers.jsonl)",
              any("stop" in str(r.get("notes")) for r in events(root, "human_answer"))
              and any(json.loads(l).get("words") == "stop" for l in (task_root / "state" / "driver-answers.jsonl").read_text(encoding="utf-8").splitlines()))
        import story_run
        body = story_run.QUESTION_HEAD_RE.sub("", story_run.ANSWER_BLOCK_RE.sub("", again), count=1).strip()
        check_eq("K8: the question that comes back still breaks no rule of human-questions.md", human_broken(body), [])
        # a run with no answer: the open ticket_changed question is asked again from the two files, the tracker is not read
        third = driver_for(root, env, KEY)
        calls = spy_stdout(third)
        with contextlib.redirect_stdout(io.StringIO()):
            code = third.run()
        check_eq("K8: a run with no answer re-asks (exit 3) and makes no adapter call at all", (code, adapter_calls(calls)), (3, []))
        check_in("K8: the asked-again question says it was answered before (FR-7)", "You have answered this exact question before", third.question_path().read_text(encoding="utf-8"))
        check_eq("K8: nothing was journaled twice", len(events(root, "ticket_changed")), 1)
    finally:
        harness.cleanup(root)


def k9_an_answer_that_is_not_a_token() -> None:
    root, task_root, env, ticket = freshness_project()
    try:
        asked_driver(root, env, task_root, ticket)
        conducted = 0
        for label, words in (("prose", "I think the new one is fine, go ahead."), ("another script", OTHER_SCRIPT),
                             ("a token only on the second line", "please\nnew text"), ("empty first lines are skipped", "\n\n  New Text.  \nbecause")):
            driver = driver_for(root, env, KEY, answer=answer_file(root, words), max_boundaries=0)
            calls = spy_stdout(driver)
            with contextlib.redirect_stdout(io.StringIO()):
                code = driver.run()
            text = driver.question_path().read_text(encoding="utf-8") if driver.question_path().is_file() else ""
            if label.startswith("empty first lines"):
                # the FIRST non-empty line is the token: `New Text.` is `new text` after `s0_normalize` - adopted, not asked again
                check_eq("K9: the first NON-EMPTY line is the token (BOM, quotes, a full stop and case are only normalized)", (driver.state["asked"], (task_root / "work" / "ticket-snapshot.next.json").is_file()), ({}, False))
                continue
            check_eq(f"K9: {label}: asked again (exit 3), the same kind", (code, driver.state["asked"].get("kind")), (3, "ticket_changed"))
            check_in(f"K9: {label}: quotes the words and says nothing has moved yet (P03c: the one lead of an unread answer)",
                     "is not one of the answers this question takes, so nothing has moved yet.", text)
            check_not_in(f"K9: {label}: the old 'it takes only' lead is gone", "it takes only", text)
            check_eq(f"K9: {label}: the question comes back priced, every option with its three lines", human_text.price_problems(text, None), [])
            seen_calls = len([c for c in stub_calls(root) if c["kind"] == "conductor"])
            check_eq(f"K9: {label}: D-0041 - the unread answer was exactly ONE conductor call (a `continue` leaves the question standing; never `--adopt`)",
                     seen_calls, conducted + 1)
            conducted = seen_calls
            check_eq(f"K9: {label}: no adapter call, `.next` kept, no rework", (adapter_calls(calls), (task_root / "work" / "ticket-snapshot.next.json").is_file(), driver.state.get("ticket_rework")), ([], True, None))
    finally:
        harness.cleanup(root)


def k9b_a_choice_the_adapter_could_not_carry_out() -> None:
    root, task_root, env, ticket = freshness_project()
    try:
        driver, _ = asked_driver(root, env, task_root, ticket)
        for label, token, said, answer in (
                ("the new text could not be adopted", "new text", "the stored new text cannot be read",
                 fixed_adapter(3, error_object("tracker", "the stored new text cannot be read"), "ticket_adapter: the stored new text cannot be read")),
                ("the decline could not be recorded", "old text", "cannot write the story's record",
                 fixed_adapter(4, error_object("factory", "cannot write the story's record"), "ticket_adapter: cannot write the story's record")),
                ("the adapter did not finish in 300 s", "new text", "ticket_adapter.py did not finish within 300 seconds",
                 lambda args, kwargs: (124, "", "ticket_adapter.py did not finish within 300 seconds"))):
            calls = spy_stdout(driver, answer)
            person = None
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    driver.take_ticket_answer(token + "\nbecause", "# q\n", "S0", "")
            except Exception as exc:
                person = exc
            check(f"K9b: {label}: the question comes back, with the adapter's sentence (no script name in front) and the whole question after it",
                  person_of(person) is not None and f"Your choice could not be carried out: {said}\n\n" in person.text
                  and "anything you write after the first line is kept with your answer for gate B" in person.text
                  and person.text.rstrip().split("\n")[-1].startswith("the story: "), repr(person))
            check_eq(f"K9b: {label}: the words are on the record first, nothing is owed, the new text still waits, one adapter call",
                     (any("because" in str(r.get("notes")) for r in events(root, "human_answer")), driver.state.get("ticket_rework"),
                      (task_root / "work" / "ticket-snapshot.next.json").is_file(), len(adapter_calls(calls))), (True, None, True, 1))
    finally:
        harness.cleanup(root)


# --- K10-K14 the exits ----------------------------------------------------------------------------------------------
def fixed_adapter(code: int, out: str = "", err: str = ""):
    return lambda args, kwargs: (code, out, err)


def k10_exit_3_is_an_informed_pass_journaled_once_per_window() -> None:
    root, task_root, env, _ticket = freshness_project()
    try:
        make_due(task_root)
        driver = driver_for(root, env, KEY)
        spy_stdout(driver, fixed_adapter(3, error_object("tracker", "the tracker could not be read for QA-1 (HTTP 503) - retry", status=503),
                                         "ticket_adapter: the tracker could not be read for QA-1 (HTTP 503) - retry"))
        t = now_whole()
        got, printed = looked(driver, now=t)
        check_eq("K10: exit 3: `unchecked`, one line, the story goes on", got, "unchecked")
        check_in("K10: the line", "ticket not checked: the tracker could not be read for QA-1 (HTTP 503) - retry; the story goes on with the text it was built on", printed)
        check_eq("K10: `ticket_unchecked` is journaled (and never as a change)", (len(events(root, "ticket_unchecked")), len(events(root, "ticket_changed"))), (1, 0))
        for label, later, count in (("at 6 h exactly: the same window", t + timedelta(hours=6), 1), ("6 h and a second: a new window", t + timedelta(hours=6, seconds=1), 2),
                                    ("a minute later: the line is said, not journaled", t + timedelta(hours=6, seconds=61), 2)):
            got, printed = looked(driver, now=later)
            check_eq(f"K10: {label}: the line is said every time", ("ticket not checked:" in printed, got), (True, "unchecked"))
            check_eq(f"K10: {label}: journaled {count} time(s) in all", len(events(root, "ticket_unchecked")), count)
        # a throttle stamp from the future is unknown: journaled; at the slack exactly it is read by time
        driver.state["ticket_unchecked_at"] = iso(t + timedelta(seconds=60))
        looked(driver, now=t)
        check_eq("K10: a throttle stamp 60 s ahead of the clock is read by time (inside the window): not journaled", len(events(root, "ticket_unchecked")), 2)
        driver.state["ticket_unchecked_at"] = iso(t + timedelta(seconds=61))
        looked(driver, now=t)
        check_eq("K10: 61 s ahead: unknown, journaled", len(events(root, "ticket_unchecked")), 3)
        check_eq("K10: the check stays due (the adapter stamped nothing): a failed look is not a look", check_due(task_root), True)
    finally:
        harness.cleanup(root)


def check_due(task_root: Path) -> bool:
    import ticket_adapter as TA
    return TA.check_is_due(task_root)


def k11_a_check_that_does_not_finish_is_unchecked() -> None:
    import story_run
    root, task_root, env, _ticket = freshness_project()
    try:
        make_due(task_root)
        driver = driver_for(root, env, KEY)
        seen = []
        real_run = story_run.subprocess.run

        def hanging(argv, *args, **kwargs):
            if Path(str(argv[2])).name != "ticket_adapter.py":
                return real_run(argv, *args, **kwargs)              # the journal line must land
            seen.append(kwargs.get("timeout"))
            raise subprocess.TimeoutExpired(argv, kwargs.get("timeout"))
        story_run.subprocess.run = hanging
        try:
            got, printed = looked(driver)
        finally:
            story_run.subprocess.run = real_run
        check_eq("K11: a call beyond 300 s is `unchecked`, with the ceiling passed", (got, seen), ("unchecked", [300]))
        check_in("K11: one line says it did not finish", "ticket not checked: ticket_adapter.py did not finish within 300 seconds; the story goes on with the text it was built on", printed)
        check_eq("K11: journaled like exit 3", len(events(root, "ticket_unchecked")), 1)
        # a call that returns is read as usual; every other caller of py_stdout has no ceiling at all
        seen.clear()

        def returning(argv, *args, **kwargs):
            if Path(str(argv[2])).name != "ticket_adapter.py":
                return real_run(argv, *args, **kwargs)
            seen.append(kwargs.get("timeout"))
            return subprocess.CompletedProcess(argv, 0, stdout=json.dumps({"result": "none", "changed": []}), stderr="")
        story_run.subprocess.run = returning
        try:
            got, _ = looked(driver)
            driver.py_stdout("ticket_adapter.py", "--selftest")
        finally:
            story_run.subprocess.run = real_run
        check_eq("K11: a call that returns within the ceiling is read as usual; a plain `py_stdout` passes no timeout", (got, seen), ("none", [300, None]))
        check_eq("K11: the S0 read has no ceiling of its own (an exit 124 there would read as a factory fault)", story_run.Driver.PY_TIMEOUTS.get("ticket_adapter.py"), None)
    finally:
        harness.cleanup(root)


def k12_exit_5_the_lost_login_and_the_protection_service() -> None:
    import source_inventory as SI
    import story_run
    import ticket_adapter as TA
    root, task_root, env, _ticket = freshness_project()
    try:
        make_due(task_root)
        driver = driver_for(root, env, KEY)
        spy_stdout(driver, fixed_adapter(5, error_object("auth", "the tracker no longer accepts the token (HTTP 401)", status=401), "ticket_adapter: the tracker no longer accepts the token"))
        got, _ = looked(driver)
        # F3 (a) (C1-3 node B): the lost tracker login is the `ticket_auth` QUESTION (kind `ticket_auth`, exit 3), not `claude -p`'s InfraStop
        check("K12: exit 5, owner `auth`: the `ticket_auth` question (a Person, never an InfraStop), the door named in the answer block",
              isinstance(got, story_run.Person) and not isinstance(got, story_run.InfraStop) and (got.kind, got.stage, got.code) == ("ticket_auth", "S0", 3)
              and "tracker token variable" in got.answer_note, repr(got))
        check_eq("K12: and nothing is journaled as unchecked", len(events(root, "ticket_unchecked")), 0)
        spy_stdout(driver, fixed_adapter(5, "", "ticket_adapter: HTTP 401"))
        got, _ = looked(driver)
        check("K12: exit 5 with no object at all is still the lost login: the same question", isinstance(got, story_run.Person) and got.kind == "ticket_auth", repr(got))
        check("K12: its answers are priced option lines, `retry`, `go on`, `stop`, each with its three lines, and no hand command",
              all(f"`{t}` — " in got.text for t in ("retry", "go on", "stop")) and human_text.price_problems(got.text, None) == []
              and "--ticket-file" not in got.text and human_broken(got.text) == [], got.text[-700:])
        # K12b (B-408 seam): the SAME object the adapter prints for an answer the tracker is not shown to have written
        check("K12b: `intermediary` is one of the adapter's owners (B-408 is on this tree)", "intermediary" in TA.OWNERS)
        objects = []
        with contextlib.redirect_stderr(io.StringIO()):
            code = TA.refuse_auth(SI.Intercepted("HTTP 403: an HTML page, not the tracker's own answer (a firewall or a protection service)"), objects.append)
        check_eq("K12b: the adapter's own refusal of an intercepted read: exit 5, owner `intermediary`", (code, objects[0]["owner"]), (5, "intermediary"))
        sentence = objects[0]["message"]
        spy_stdout(driver, fixed_adapter(5, json.dumps(objects[0]), "ticket_adapter: " + sentence))
        got, printed = looked(driver)
        check_eq("K12b: a freshness read that meets a foreign answer is `unchecked`, never the lost-login stop", got, "unchecked")
        check_in("K12b: the line is the spec's, with B-408's own sentence in it (one path, no second text)",
                 f"ticket not checked: a protection service in front of the tracker answered, not the tracker ({sentence}); the story goes on with the text it was built on", printed)
        check_eq("K12b: journaled like exit 3, once", len(events(root, "ticket_unchecked")), 1)
        check_not_in("K12b: and the token is never told to be renewed", "renew", printed)
    finally:
        harness.cleanup(root)


def lost_login(driver):
    """A tracker that no longer accepts the token (the adapter's exit 5, owner `auth`) as the freshness check's answer."""
    return spy_stdout(driver, fixed_adapter(5, error_object("auth", "the tracker no longer accepts the token (HTTP 401)", status=401),
                                            "ticket_adapter: the tracker no longer accepts the token"))


def run_quiet(driver) -> int:
    with contextlib.redirect_stdout(io.StringIO()):
        return driver.run()


def asked_ticket_auth(root: Path, env: dict, task_root: Path):
    """A story whose check was due and whose tracker login is lost: the `ticket_auth` question is open (the first process)."""
    make_due(task_root)
    first = driver_for(root, env, KEY, max_boundaries=0)
    lost_login(first)
    got, _ = looked(first)
    person = person_of(got)
    check("setup: the lost login asks the `ticket_auth` question", person is not None and person.kind == "ticket_auth", repr(got))
    question_of(first, person)
    return first


def conductor_calls_of(root: Path) -> int:
    return len([c for c in stub_calls(root) if c["kind"] == "conductor"])


def k12c_ticket_auth_retry_go_on_stop_unread() -> None:
    """G3 (FR-9, FR-7, FR-4): each word of the `ticket_auth` question has its executor. `retry` runs the check again in this process;
    `go on` is a recorded informed pass, honoured for the freshness window and asked again only when it has run out; `stop` holds the
    question once (F7); other words are new words for the conductor (D-0041), never a silent pass."""
    root, task_root, env, _ticket = freshness_project()
    try:
        asked_ticket_auth(root, env, task_root)
        # retry: the check runs again IN THIS process; the login still lost -> the question again, never a pass
        driver = driver_for(root, env, KEY, answer=answer_file(root, "retry"), max_boundaries=0)
        calls = lost_login(driver)
        code = run_quiet(driver)
        check_eq("K12c retry: the check ran again once (the adapter was asked) and the lost login is the same question: exit 3",
                 (code, len(adapter_calls(calls)), driver.state["asked"].get("kind")), (3, 1, "ticket_auth"))
        check_eq("K12c retry: nothing was passed: no `ticket_unchecked`, no `fresh.ticket_auth` kept",
                 (len(events(root, "ticket_unchecked")), (driver.state.get("s0_answers") or {}).get("fresh.ticket_auth")), (0, None))
        # retry with the token renewed: the question is gone and the story goes on
        driver = driver_for(root, env, KEY, answer=answer_file(root, "retry"), max_boundaries=0)
        calls = spy_stdout(driver, fixed_adapter(0, json.dumps({"result": "none", "changed": []})))
        code = run_quiet(driver)
        check_eq("K12c retry: a token that works clears the question (no question open, one look)", (driver.state.get("asked"), len(adapter_calls(calls))), ({}, 1))
        check("K12c retry: ... and the exit is not a question", code != 3, str(code))
        # go on: recorded as an informed pass (FR-4), the story goes on with its text, the look is not made again in the window (FR-7)
        asked_ticket_auth(root, env, task_root)
        driver = driver_for(root, env, KEY, answer=answer_file(root, "go on"), max_boundaries=0)
        calls = lost_login(driver)
        code = run_quiet(driver)
        check_eq("K12c go on: no question (exit is not 3) and the adapter was NOT asked again after the word", (code != 3, len(adapter_calls(calls))), (True, 0))
        check_eq("K12c go on: `ticket_unchecked` is journaled once (the informed pass), the word is kept for the window",
                 (len(events(root, "ticket_unchecked")), driver.state["s0_answers"].get("fresh.ticket_auth"), bool(driver.state.get("ticket_unchecked_at"))),
                 (1, "go on", True))
        check("K12c go on: the person's word is on the journal whole", any("ticket login lost (go on): " in str(r.get("notes")) for r in events(root, "human_answer")))
        again = driver_for(root, env, KEY, max_boundaries=0)
        calls = lost_login(again)
        make_due(task_root)
        got, printed = entered(again)
        check_eq("K12c go on: a later process inside the window does not ask again (FR-7) and does not look", (got, len(adapter_calls(calls))), ("unchecked", 0))
        check_in("K12c go on: and says so in a line", "you said to go on without looking at the ticket", printed)
        # expiry: the window has run out -> the key is dropped and the check runs again; the lost login is the question again
        again.state["ticket_unchecked_at"] = iso(now_whole() - timedelta(hours=7))
        again.save_state()
        got, _ = entered(again)
        check_eq("K12c go on: past the window the check runs and the question is asked again",
                 (person_of(got) is not None and got.kind == "ticket_auth", len(adapter_calls(calls)), "fresh.ticket_auth" in (again.state.get("s0_answers") or {})),
                 (True, 1, False))
        # an unreadable stamp is not a fresh one (FR-41): the word is not honoured
        again.state.setdefault("s0_answers", {})["fresh.ticket_auth"] = "go on"
        again.state["ticket_unchecked_at"] = "not a time"
        again.state["asked"] = {}
        got, _ = entered(again)
        check_eq("K12c go on: a stamp that is not a time honours nothing", person_of(got) is not None and got.kind == "ticket_auth", True)
        # stop: held once (F7) - a second stop does not stack the held lines; the question is the same; no conductor
        driver = driver_for(root, env, KEY, answer=answer_file(root, "stop"), max_boundaries=0)
        lost_login(driver)
        before = conductor_calls_of(root)
        make_due(task_root)
        driver.state["asked"] = {"kind": "ticket_auth", "stage": "S0", "dispatch": ""}
        driver.state.setdefault("s0_answers", {}).pop("fresh.ticket_auth", None)
        question_of(driver, driver.ticket_auth_person("401"))
        for round_ in (1, 2):
            driver = driver_for(root, env, KEY, answer=answer_file(root, "stop"), max_boundaries=0)
            lost_login(driver)
            code = run_quiet(driver)
            held = driver.question_path().read_text(encoding="utf-8")
            check_eq(f"K12c stop (round {round_}): exit 3, the question held, the held line ONCE (F7), no conductor",
                     (code, driver.state["asked"].get("kind"), held.count("You said to stop."), conductor_calls_of(root) - before), (3, "ticket_auth", 1, 0))
        check("K12c stop: the held question still offers `retry` and `go on` and is priced",
              "`retry`" in held and "`go on`" in held and human_text.price_problems(held.split("## How to answer")[0], None) == [], held[-600:])
    finally:
        harness.cleanup(root)
    # other words: D-0041 - exactly ONE conductor call; a usable-less conductor shows the question again with the one lead, priced
    root, task_root, env, _ticket = freshness_project()
    try:
        from story_run_common import set_control
        set_control(root, {"conductor": {"action": "ask_person", "question": "", "did": "no options"}})
        asked_ticket_auth(root, env, task_root)
        driver = driver_for(root, env, KEY, answer=answer_file(root, "I renewed it yesterday, I think"), max_boundaries=0)
        calls = lost_login(driver)
        code = run_quiet(driver)
        held = driver.question_path().read_text(encoding="utf-8")
        check_eq("K12c unread: exit 3, kind `ticket_auth`, exactly ONE conductor call, nothing passed",
                 (code, driver.state["asked"].get("kind"), conductor_calls_of(root), (driver.state.get("s0_answers") or {}).get("fresh.ticket_auth")),
                 (3, "ticket_auth", 1, None))
        check_in("K12c unread: the question comes back with the one lead", 'Your answer "I renewed it yesterday, I think" ' + UNREAD, held)
        check_eq("K12c unread: and priced, with its three answers", (human_text.price_problems(held.split("## How to answer")[0], None),
                                                                       all(f"`{t}` — " in held for t in ("retry", "go on", "stop"))), ([], True))
        # F-2 (critic t-689): an unread answer after an unread answer does not stack its leads (the question is the held one, and
        # the lead is the NEW one); a `stop` after them is the stop line alone above the question - neither unread lead stays
        for round_, words in ((2, "I will think about the login tomorrow"), (3, "maybe the day after")):
            driver = driver_for(root, env, KEY, answer=answer_file(root, words), max_boundaries=0)
            lost_login(driver)
            run_quiet(driver)
            held_n = driver.question_path().read_text(encoding="utf-8")
            check_eq(f"K12c unread (answer {round_}): ONE lead, the newest answer's, no earlier one stacked beneath it",
                     (held_n.count(UNREAD), held_n.count(f'Your answer "{words}"'), held_n.count("I renewed it yesterday")), (1, 1, 0))
        driver = driver_for(root, env, KEY, answer=answer_file(root, "stop"), max_boundaries=0)
        lost_login(driver)
        run_quiet(driver)
        held_stop = driver.question_path().read_text(encoding="utf-8")
        check_eq("K12c unread then `stop`: the stop line ONCE and no unread lead above or under it",
                 (held_stop.count("You said to stop."), held_stop.count(UNREAD), held_stop.count("maybe the day after")), (1, 0, 0))
        check("K12c unread then `stop`: the question under it is the same one (priced, `retry` / `go on` / `stop`)",
              all(f"`{t}` — " in held_stop for t in ("retry", "go on", "stop")), held_stop[-600:])
        # a conductor `continue` returns: nothing passed, the check runs again (which decides) - the question stands, never a silent pass
        set_control(root, {"conductor": {"action": "continue"}})
        driver = driver_for(root, env, KEY, answer=answer_file(root, "never mind the login"), max_boundaries=0)
        calls = lost_login(driver)
        code = run_quiet(driver)
        check_eq("K12c unread + conductor `continue`: nothing passed; the check ran again and the question stands (exit 3)",
                 (code, driver.state["asked"].get("kind"), len(adapter_calls(calls)), (driver.state.get("s0_answers") or {}).get("fresh.ticket_auth")),
                 (3, "ticket_auth", 1, None))
    finally:
        harness.cleanup(root)


def k13_the_factorys_own_faults_are_reported() -> None:
    import story_run
    root, task_root, env, _ticket = freshness_project()
    try:
        make_due(task_root)
        driver = driver_for(root, env, KEY)
        for label, answer in (("exit 4", (4, error_object("factory", "refused - jira-fields.json is empty"), "ticket_adapter: refused")),
                              ("owner factory on exit 1", (1, error_object("factory", "an unexpected error"), "")),
                              ("exit 2 (usage)", (2, "", "usage: ticket_adapter.py freshness")),
                              ("a crash with no object", (7, "Traceback", "boom")),
                              ("exit 0 with no JSON object", (0, "this is not json", "")),
                              ("exit 0 with a result nobody knows", (0, json.dumps({"result": "weather"}), ""))):
            spy_stdout(driver, fixed_adapter(*answer))
            got, printed = looked(driver)
            check(f"K13: {label}: a Refusal that says it is the factory's own and names what is expected", isinstance(got, story_run.Refusal) and "the cause is the factory's own" in got.text, repr(got))
            check_eq(f"K13: {label}: never an informed pass, never journaled as unchecked", (printed, len(events(root, "ticket_unchecked"))), ("", 0))
        spy_stdout(driver, fixed_adapter(4, error_object("factory", "refused - jira-fields.json is empty"), ""))
        got, _ = looked(driver)
        check_in("K13: exit 4 names the file the adapter named", "jira-fields.json", got.text)
    finally:
        harness.cleanup(root)


def k14_exit_1_goes_by_the_owner() -> None:
    root, task_root, env, _ticket = freshness_project()
    try:
        make_due(task_root)
        driver = driver_for(root, env, KEY)
        spy_stdout(driver, fixed_adapter(1, error_object("person", "the ticket file you gave is missing or empty"), "ticket_adapter: the ticket file you gave is missing or empty"))
        got, printed = looked(driver)
        check_eq("K14: exit 1 owner `person`: its message in one line, `unchecked`, nothing journaled", (got, "the ticket file you gave is missing or empty" in printed, len(events(root, "ticket_unchecked"))), ("unchecked", True, 0))
        spy_stdout(driver, fixed_adapter(1, error_object("tracker", "QA-1 was not found (HTTP 404)", status=404), ""))
        got, printed = looked(driver)
        check_eq("K14: exit 1 owner `tracker` (not found): the exit-3 class, journaled", (got, len(events(root, "ticket_unchecked"))), ("unchecked", 1))
    finally:
        harness.cleanup(root)


# --- K15-K20 the positions ------------------------------------------------------------------------------------------
def k15_positions_in_the_run() -> None:
    # (a) a fresh story: S0 runs in this process and the ticket is NOT looked at (K11 of the S0 file: no read, the hash is stable)
    root, task_root, env = s0_project(KEY)
    try:
        driver = driver_for(root, env, KEY, max_boundaries=0)
        entries = []
        driver.ticket_freshness_entry = lambda: entries.append("entry") or "x"
        with contextlib.redirect_stdout(io.StringIO()):
            driver.run()
        check_eq("K15: the process that wrote S0 never looks at the ticket", entries, [])
    finally:
        harness.cleanup(root)
    # (b), (c), (d) a resumed story
    root, task_root, env, ticket = freshness_project()
    try:
        order = []
        driver = driver_for(root, env, KEY, max_boundaries=0)
        real_entry, real_accept = driver.ticket_freshness_entry, driver.accept_no_trace
        driver.ticket_freshness_entry = lambda: order.append("freshness") or real_entry()
        driver.accept_no_trace = lambda: order.append("accept_no_trace") or real_accept()
        make_due(task_root)
        calls = spy_stdout(driver)
        with contextlib.redirect_stdout(io.StringIO()):
            driver.run()
        check_eq("K15: a resumed story is looked at ONCE, before `accept_no_trace` and the loop", (order, len(adapter_calls(calls))), (["freshness", "accept_no_trace"], 1))
        # another kind of question is open: never stacked
        make_due(task_root)
        edit_requirements(ticket)
        other = driver_for(root, env, KEY, max_boundaries=0)
        other.state["asked"] = {"kind": "halt", "stage": "S3", "dispatch": "S3-x-1"}
        other.question_path().write_text("# q\nkind: halt\nstage: S3\ndispatch: S3-x-1\n\nA role halted.\n", encoding="utf-8")
        calls = spy_stdout(other)
        with contextlib.redirect_stdout(io.StringIO()):
            code = other.run()
        check_eq("K15: another question is open: no look, no new question (the halt stays)", (adapter_calls(calls), other.state["asked"].get("kind"), code), ([], "halt", 0))
        # the person's answer to ANOTHER question is recorded before the look (FR-8)
        order = []
        stage_answer = driver_for(root, env, KEY, max_boundaries=0, answer=answer_file(root, "skip"))
        stage_answer.state["asked"] = {"kind": "retro", "stage": "S9", "dispatch": ""}
        stage_answer.question_path().write_text("# q\nkind: retro\n", encoding="utf-8")
        real_take, real_entry = stage_answer.take_answer, stage_answer.ticket_freshness_entry
        stage_answer.take_answer = lambda path: order.append("take_answer") or real_take(path)
        stage_answer.ticket_freshness_entry = lambda: order.append("freshness") or real_entry()
        with contextlib.redirect_stdout(io.StringIO()):
            stage_answer.run()
        check_eq("K15: the answer is recorded first, then the look", order, ["take_answer", "freshness"])
        check_eq("K15: and the look found the moved requirements: the question is open now", stage_answer.state["asked"].get("kind"), "ticket_changed")
    finally:
        harness.cleanup(root)


def k16_a_pasted_story_passes_its_file() -> None:
    root, task_root, env, _ticket = freshness_project()
    try:
        paste = root / "pasted.md"
        paste.write_text(FIXTURE_TICKET, encoding="utf-8")
        out, got = adapter(root, env, task_root, "--ticket-file", str(paste))
        check("setup: the pasted text is read and its look stamped", out.returncode == 0, out.stderr[-300:])
        make_due(task_root)
        driver = driver_for(root, env, KEY, ticket_file=str(paste))
        calls = spy_stdout(driver)
        got, _ = looked(driver)
        script, args, _kwargs = adapter_calls(calls)[0]
        check_eq("K16: exactly when the launch names a ticket file, `--ticket-file <it>` is on the call", (args[-2:], got), (("--ticket-file", str(paste)), "none"))
        paste.write_text(FIXTURE_TICKET.replace("at most 5 tags; a sixth tag", "at most 7 tags; an eighth tag"), encoding="utf-8")
        make_due(task_root)
        got, _ = looked(driver)
        person = person_of(got)
        check("K16: a changed pasted text is the same question, saying so in the story's words", person is not None and "The ticket text you gave me" in person.text, repr(got))
        check_not_in("K16: with no path in the body", "pasted.md", person.text)
        check_in("K16: the person's own file is named in the answer block", "pasted.md", person.answer_note)
        check_eq("K16: and it breaks no rule", human_broken(person.text), [])
    finally:
        harness.cleanup(root)


def k17_the_word_that_the_ticket_is_not_needed_outlives_s0() -> None:
    root, task_root, env = s0_project(KEY)
    try:
        tickets = root / "tickets"
        text = (tickets / f"{KEY}.md").read_text(encoding="utf-8")
        (tickets / f"{KEY}.md").unlink()
        out = s0_run(root, env, KEY)
        check_eq("K17: the ticket cannot be read: the `ticket_read` question", (out.returncode, s0_state(task_root).get("s0_block")), (3, "ticket_read"))
        # a snapshot appears (the person put the text in place), and the person answers `not needed`: S0 goes on with it
        (tickets / f"{KEY}.md").write_text(text, encoding="utf-8")
        got = harness.run_script("ticket_adapter.py", "get", KEY, "--json", "--output", str(task_root / "work" / "ticket-snapshot.json"), cwd=root, env=env)
        check_eq("setup: the snapshot is on disk", got.returncode, 0)
        out = s0_answer(root, env, KEY, "not needed")
        state = s0_state(task_root)
        check_eq("K17: S0 finished", (out.returncode, (task_root / "pipeline.json").is_file()), (0, True))
        check_eq("K17: `launch.ticket_not_needed` was written before `s0_answers` was popped", ((state.get("launch") or {}).get("ticket_not_needed"), "s0_answers" in state), (True, False))
        # the next process: due, and the check is skipped on the word, with one line
        (task_root / "work" / "ticket-freshness.json").write_text(json.dumps({"checked_at": iso(datetime.now(UTC) - timedelta(hours=9)), "result": "none"}), encoding="utf-8")
        driver = driver_for(root, env, KEY)
        calls = spy_stdout(driver)
        word, printed = entered(driver)
        check_eq("K17: a due check is not run on the person's word, and one line says why", (word, adapter_calls(calls), "you said the ticket is not needed" in printed), ("not_needed", [], True))
        # control: the same story without the flag IS looked at
        driver.state["launch"].pop("ticket_not_needed")
        word, _ = entered(driver)
        check_eq("K17 control: without the word the same due story is looked at", (word, len(adapter_calls(calls))), ("none", 1))
    finally:
        harness.cleanup(root)


def k18_no_controller_means_no_look() -> None:
    root, task_root, env, ticket = freshness_project()
    try:
        make_due(task_root)
        edit_requirements(ticket)
        (task_root / "state" / "controller.json").unlink()
        driver = driver_for(root, env, KEY)
        calls = spy_stdout(driver)
        word, printed = entered(driver)
        check_eq("K18: no state/controller.json: no look, silent (`initialize` hashes the S0 snapshot first)", (word, adapter_calls(calls), printed), ("no_controller", [], ""))
        check("K18: and the snapshot is exactly the one the story was built on", not (task_root / "work" / "ticket-snapshot.next.json").is_file())
    finally:
        harness.cleanup(root)


def k19_a_closed_story_is_not_looked_at() -> None:
    root, task_root, env, ticket = freshness_project()
    try:
        make_due(task_root)
        edit_requirements(ticket)
        d3_s8_done(task_root)
        path = task_root / "pipeline.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["gates"] = {"B": {"decision": "approved", "status": "approved"}}
        path.write_text(json.dumps(data), encoding="utf-8")
        driver = driver_for(root, env, KEY)
        calls = spy_stdout(driver)
        word, printed = entered(driver)
        check_eq("K19: a closed story (gate B decided, S8 done) is not looked at, one line says so", (word, adapter_calls(calls), "this story is closed" in printed), ("closed", [], True))
    finally:
        harness.cleanup(root)


def k20_gate_b_is_checked_before_it_is_asked() -> None:
    root, task_root, env, _ticket = freshness_project()
    try:
        for gate, expected in (("B", ["freshness", "gate_repair"]), ("A", ["gate_repair"])):
            driver = driver_for(root, env, KEY)
            order = []
            driver.ticket_freshness_entry = lambda: order.append("freshness") or "none"
            driver.gate_repair = lambda g: order.append("gate_repair") or {"ran": True, "top": ""}
            driver.dispatch_action({"action": "await_gate", "gate": gate})
            check_eq(f"K20: gate {gate}: the order", order, expected)
        # M4: an open question of another kind (the gate's own, asked and unanswered) means the entry holds
        driver = driver_for(root, env, KEY)
        driver.state["asked"] = {"kind": "gate_B", "stage": "S8", "dispatch": ""}
        calls = spy_stdout(driver)
        make_due(task_root)
        word, _ = entered(driver)
        check_eq("K20 (M4): while a question is open the pre-check holds: no read, the open question is not replaced", (word, adapter_calls(calls), driver.state["asked"]["kind"]), ("held", [], "gate_B"))
    finally:
        harness.cleanup(root)


# --- K21-K26 the rest of the keys ------------------------------------------------------------------------------------
def k21_the_options_constant_is_in_s0_md() -> None:
    import story_run
    text = (harness.PLUGIN_ROOT / "skills" / "qa-story" / "phases" / "s0.md").read_text(encoding="utf-8")
    line = next(l.strip() for l in text.splitlines() if l.strip().startswith("> re-run"))
    check_eq("K21: TICKET_CHANGED_OPTIONS is the quoted line of phases/s0.md section 2b, character for character", story_run.TICKET_CHANGED_OPTIONS, line[2:])
    check_eq("K21: the tokens the code reads", story_run.TICKET_CHANGED_TOKENS, ("new text", "old text", "stop"))
    check("K21: the prose names the same three tokens and the cause", all(w in text for w in ("`new text`, `old text` or\n`stop`", "--cause ticket_changed")))


def k22_no_baseline_the_ticket_as_it_stands_becomes_one() -> None:
    root, task_root, env = seed(KEY)
    try:
        tickets = root / "tickets"
        tickets.mkdir()
        (tickets / f"{KEY}.md").write_text(FIXTURE_TICKET, encoding="utf-8")
        config = root / "qa-factory" / "config.json"
        cfg = json.loads(config.read_text(encoding="utf-8"))
        cfg["adapters"] = {"ticket": {"kind": "file", "path": str(tickets)}}
        config.write_text(json.dumps(cfg), encoding="utf-8")
        (task_root / "work" / "ticket-freshness.json").unlink()          # no stamp, no baseline: an unknown age is not a fresh one
        driver = driver_for(root, env, KEY)
        got, printed = looked(driver)
        check_eq("K22: no baseline: `baseline_written`, one line", (got, "the story had none to compare with" in printed), ("baseline_written", True))
        check("K22: and the baseline is there now", (task_root / "work" / "ticket-snapshot.json").is_file())
        got, _ = looked(driver)
        check_eq("K22: and the story is checked: not due", got, "skipped")
    finally:
        harness.cleanup(root)


def k23_a_waiting_text_after_a_crash_is_asked_again() -> None:
    root, task_root, env, ticket = freshness_project()
    try:
        edit_requirements(ticket)
        make_due(task_root)
        driver = driver_for(root, env, KEY)
        looked(driver)                                                    # the look stamped `checked_at` and wrote `.next`; the process "crashed" before asking
        check("setup: the check is stamped just now and `.next` waits", (task_root / "work" / "ticket-snapshot.next.json").is_file())
        fresh = driver_for(root, env, KEY)
        got, _ = looked(fresh)
        check_eq("K23: a waiting text nobody answered is due whatever the stamp says: the question is asked", person_of(got) is not None, True)
        check_eq("K23: and the same text is journaled once", len(events(root, "ticket_changed")), 1)
    finally:
        harness.cleanup(root)


def k24_an_answer_after_the_text_stopped_waiting() -> None:
    root, task_root, env, ticket = freshness_project()
    try:
        driver, _ = asked_driver(root, env, task_root, ticket)
        (task_root / "work" / "ticket-snapshot.next.json").unlink()      # a later look settled it
        for token in ("new text", "old text"):
            printed = io.StringIO()
            before = len(events(root, "human_answer"))
            with contextlib.redirect_stdout(printed):
                driver.take_ticket_answer(token, "# q\n", "S0", "")
            check_eq(f"K24: `{token}` with nothing waiting: the adapter's refusal is printed, the story goes on, nothing is owed", ("nothing" in printed.getvalue(), driver.state.get("ticket_rework")), (True, None))
            check_eq(f"K24: `{token}`: the words are on the journal's record all the same", len(events(root, "human_answer")), before + 1)
        # and the loop with the flag still set clears it the way `reconcile_question` clears one, then looks as usual
        later = driver_for(root, env, KEY)
        later.state["asked"] = {"kind": "ticket_changed", "stage": "S0", "dispatch": "", "at": "x"}
        later.question_path().write_text("# q\nkind: ticket_changed\nstage: S0\n\nThe ticket changed.\n", encoding="utf-8")
        ticket.write_text(FIXTURE_TICKET, encoding="utf-8")            # the text moved back: the look that follows finds nothing
        make_due(task_root)
        word, printed = entered(later)
        check_eq("K24: an open `ticket_changed` whose text is gone: the flag is cleared, the check goes on", (later.state["asked"], word), ({}, "none"))
        check_in("K24: and one line says the text no longer waits", "no longer waits", printed)
    finally:
        harness.cleanup(root)


def k26_the_drivers_word_is_never_a_reviewers() -> None:
    import judge_code
    import repair_route
    from controller import REPAIR_CAUSES, REVIEWER_CAUSES
    check_eq("K26: the controller's list is the reviewers' five and the driver's word", (REPAIR_CAUSES[-1], REVIEWER_CAUSES), ("ticket_changed", ("test_defect", "mechanical", "environment", "tooling", "reviewer_error")))
    rows = repair_route.findings({"findings": [{"id": "F1", "problem": "a sleep", "cause": "ticket_changed"}, {"id": "F2", "problem": "a stand", "cause": "environment"}]})
    check_eq("K26: a finding a reviewer typed `ticket_changed` reads as `test_defect` (it spends the cap): the safe side", [r["cause"] for r in rows], ["test_defect", "environment"])
    real = (judge_code.judge.settings, judge_code.judge.active, judge_code.judge.ask_one)
    try:
        judge_code.judge.settings = lambda root=None: {"provider": "stub", "mode": "active"}
        judge_code.judge.active = lambda cfg, name: True
        for said, expected in (("ticket_changed", "test_defect"), ("mechanical", "mechanical")):
            judge_code.judge.ask_one = lambda *a, **k: {"value": said, "decided": True, "confidence": 0.9}
            check_eq(f"K26: the judge's `{said}` reads as `{expected}`", judge_code.cause("a finding")["repair_cause"], expected)
    finally:
        judge_code.judge.settings, judge_code.judge.active, judge_code.judge.ask_one = real
    import ticket_adapter as TA
    now = datetime(2026, 10, 7, 12, 0, 0, tzinfo=UTC)
    check("K26: the adapter's future-time slack (60 s at, 61 s beyond) is the one helper both the trigger and the driver's throttle read", TA.stamp_is_ahead(iso(now + timedelta(seconds=61)), now) and not TA.stamp_is_ahead(iso(now + timedelta(seconds=60)), now))


SCENARIOS = [
    k1_the_window_at_and_beyond, k2_k3_none_and_context, k4_requirements_is_the_persons_question, k4b_an_unreadable_file_with_the_question_open_never_crashes, k5_old_text,
    k6_k7_new_text_reworks_s2_then_s3_then_reopens_gate_a, k7b_gate_a_not_decided_is_not_reopened, k7c_the_reworks_own_edges,
    k7d_the_reopen_sets_aside_the_late_work_and_names_what_it_cannot, k7e_a_ticket_rework_finished_through_the_restart_route_is_complete,
    k8_stop_then_a_no_answer_run_asks_again_with_no_read, k9_an_answer_that_is_not_a_token, k9b_a_choice_the_adapter_could_not_carry_out,
    k10_exit_3_is_an_informed_pass_journaled_once_per_window, k11_a_check_that_does_not_finish_is_unchecked,
    k12_exit_5_the_lost_login_and_the_protection_service, k12c_ticket_auth_retry_go_on_stop_unread, k13_the_factorys_own_faults_are_reported, k14_exit_1_goes_by_the_owner,
    k15_positions_in_the_run, k16_a_pasted_story_passes_its_file, k17_the_word_that_the_ticket_is_not_needed_outlives_s0,
    k18_no_controller_means_no_look, k19_a_closed_story_is_not_looked_at, k20_gate_b_is_checked_before_it_is_asked,
    k21_the_options_constant_is_in_s0_md, k22_no_baseline_the_ticket_as_it_stands_becomes_one,
    k23_a_waiting_text_after_a_crash_is_asked_again, k24_an_answer_after_the_text_stopped_waiting,
    k26_the_drivers_word_is_never_a_reviewers]


def main() -> None:
    """No argument: every scenario. Names (prefixes, `k7c k10`): only those - the one a mutation of the driver is checked
    by (builder-rules 7a), with the same checks; an argument that names nothing is an error, never a silent green."""
    wanted = sys.argv[1:]
    chosen = [s for s in SCENARIOS if not wanted or any(s.__name__.startswith(prefix) for prefix in wanted)]
    if not chosen:
        sys.exit(f"test_story_run_freshness: no scenario starts with {wanted}; they are: " + ", ".join(s.__name__ for s in SCENARIOS))
    run_scenarios([], chosen)
    harness.finish("test_story_run_freshness")


if __name__ == "__main__":
    main()
