"""snapshot: a part of test_story_run_s0.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_run_s0_common."""
import hashlib
import json
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_in, check_not_in  # noqa: E402
from story_run_common import BOM, CUT, FIXTURE_TICKET, LOST_READ_TICKET, NOT_A_TICKET, OTHER_SCRIPT, driver_for, eq, rules_broken, s0_answer, s0_findings, s0_journal, s0_pipeline, s0_project, s0_question, s0_run, s0_state, seed, set_control, stub_calls, run_scenarios
from story_run_s0_common import (  # noqa: E402
    DRAFT, EM, FakeJira, KEY, NO_USABLE, UNREAD_LEAD, _no_record, _record, conductor_count, price_broken,
    rest_project, snapshot_of, story_15045,
)


# The S0 scenarios below are functions of their own so that the ones that only start driver
# processes (each a fresh temp project and a full S0 costs ~15 s of readiness probes) can run
# side by side; the three that build a Driver in this process (it changes the working directory)
# run one after another in the main thread. `s0_scenarios` is the runner.
def s0_snapshot() -> None:
    check_eq = eq  # this section always shows the run's output on a failed comparison

    # --- (a)(b)(c) one snapshot: JSON, byte for byte the adapter's stdout, hashed and briefed -------
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        out = s0_run(root, env, task)
        eq("D1(a) a fresh S0 by code exits 0", out.returncode, 0, out.stdout[-1500:] + out.stderr[-800:])
        snapshot = task_root / "work" / "ticket-snapshot.json"
        check("D1(a) the snapshot is work/ticket-snapshot.json", snapshot.is_file())
        check("D1(a) and there is no markdown twin", not (task_root / "work" / "ticket-snapshot.md").exists())
        env_c = dict(env)
        adapter = harness.run_script("ticket_adapter.py", "get", task, "--json", cwd=root, env=env_c)
        check_eq("D1(a) the file holds the adapter's stdout, byte for byte",
                 snapshot.read_bytes(), adapter.stdout.encode("utf-8"))
        parsed = json.loads(snapshot.read_text(encoding="utf-8"))
        check_eq("D1(a) it parses whole, as one JSON object with the ticket in it",
                 (parsed["key"], len(parsed["acceptance_criteria"])), ("QA-1", 5))
        check("D1(a) and the adapter's stderr is not in it (a stderr line would fail the parse above)",
              snapshot.read_text(encoding="utf-8").rstrip().endswith("}"))
        controller = json.loads((task_root / "state" / "controller.json").read_text(encoding="utf-8"))
        check_eq("D1(b) the controller's source_revision is the sha256 of the .json",
                 controller.get("source_revision"), hashlib.sha256(snapshot.read_bytes()).hexdigest())
        brief = harness.run_script("brief_pack.py", "--task", task, "--stage", "S1", "--role", "qa-scout",
                                   "--dispatch", "S1-qa-scout-1", "--json", "--dry-run", cwd=root, env=env)
        check_eq("D1(c) the scout's brief builds", brief.returncode, 0, brief.stderr[-500:])
        markdown = json.loads(brief.stdout)["markdown"]
        check("D1(c) and lists work/ticket-snapshot.json with its size",
              re.search(r"work/ticket-snapshot\.json \(\d+(\.\d+)? (B|KB)\)", markdown) is not None, markdown[-900:])
        check_eq("no conductor or role was called by S0", stub_calls(root), [])
        check_eq("the launch is kept for a later entry", s0_state(task_root).get("launch"), {})
        check("a story with no list is today's story: no record is written and no list line is printed",
              not (task_root / "work" / "source-exclusions.json").exists()
              and "asked me not to read" not in out.stdout and "list of sources" not in out.stdout)
    finally:
        harness.cleanup(root)


def s0_incomplete_ticket() -> None:
    check_eq = eq
    task = "QA-1"

    # --- (f)(g)(m) an incomplete ticket: the person's word is read, not ignored --------------------
    root, task_root, env = s0_project(task)
    try:
        bad = root / "incomplete-ticket.md"
        bad.write_text(LOST_READ_TICKET, encoding="utf-8")
        out = s0_run(root, env, task, "--ticket-file", str(bad))
        check_eq("D1(f) an incomplete ticket asks the person: exit 3", out.returncode, 3, out.stdout[-800:])
        first = s0_question(task_root)
        check_in("D1(f) the question is of kind halt", "kind: halt", first)
        check_in("D1(f) K13 / D-0050: it names the problem as the FACTORY's reader failing on the section, not the ticket",
                 "this is the factory's reader failing on that section, not your ticket", first)
        check_in("D-0050: and quotes the section's first line, the heading as written",
                 "The operator can tag an item and filter the list by that tag.", first)
        check_in("D-0050: the heading found, in backticks", "a section named `## Acceptance criteria`", first)
        check_not_in("D1(f) F4: it asks nothing about comments or a parent (the old phrase check is retired)", "comments", first)
        check_not_in("t-957 F-4 / FR-2: `retry` is not offered (the reader is deterministic: the same text reads the same)", "`retry`", first)
        check_in("D1(f) with `go on` among the answers", "`go on`", first)
        check_in("D1(f) and `stop`", "`stop`", first)
        details = (task_root / "state" / "driver-question-details.md").read_text(encoding="utf-8")
        check_in("K-F5: the factory's words beside the question name the headings looked for, verbatim, from the merged list (the table's)",
                 "I looked for a section named one of: Acceptance Criteria, What needs to be tested, AC.", details)
        check_not_in("D-0050: the question no longer says the requirements are 'built from the criteria'", "built from the criteria", first)
        check_eq("D1(f) the block is remembered", s0_state(task_root).get("s0_block"), "ticket_incomplete")
        check("D1(f) and no pipeline.json exists", not (task_root / "pipeline.json").exists())
        check_in("the factory's own words are beside the question", "What the check found", details)
        check_in("D-0050: a finding of the factory's own defect is filed the moment the stop is shown (once per story)",
                 "idempotency:s0-criteria-unread:QA-1", s0_findings(root))
        check_eq("the question obeys human-questions.md", rules_broken(first), [])

        # (g) is `s0_reask_battery` below: a question that takes no text is where a stray answer comes back
        # changed. THIS question takes the ticket as text (t-267 C9: any non-empty text), so what the person
        # types here that is not a door is a paste (`s0_pasted_ticket`) - the parser, not a phrase, decides.
        # (f) `go on`: the story goes on; the pass is written down everywhere it must be
        out = s0_answer(root, env, task, "go on")
        check_eq("D1(f) `go on` on a lost read: exit 0", out.returncode, 0, out.stdout[-1500:] + out.stderr[-500:])
        pipeline = s0_pipeline(task_root)
        check("D1(f) pipeline.json is written", pipeline["stages"]["S0"]["status"] == "done")
        line = "S0: the criteria-reading check passed by the person's word: \"go on\""
        check_in("D1(f) with the warning line gate A shows", line, pipeline["warnings"])
        check_in("D1(f) and the finding in the person's words (FB row)",
                 "S0 ticket_incomplete passed by the person's word: go on", s0_findings(root))
        check_in("D1(f) filed as a local calibration finding", "local-calibration", s0_findings(root))
        check_in("D1(f) once per story and block", "idempotency:s0-pass:QA-1:ticket_incomplete", s0_findings(root))
        check("D1(f) the answer is a human_answer in the journal",
              any(e.get("event") == "human_answer" and "S0 ticket_incomplete: go on" in str(e.get("notes"))
                  for e in s0_journal(root)))
        check_eq("D1(f) ZERO conductor calls on the whole path", stub_calls(root), [])
        state = s0_state(task_root)
        check("D1(f) the stop's own keys are cleared once pipeline.json is written",
              not any(k in state for k in ("s0_block", "s0_ask", "s0_passes", "s0_answers"))
              and "S0" not in state.get("pending_words", {}))
        check_eq("D1(f) the launch stays, as it was given (the file was named on the first command line only)",
                 state.get("launch"), {"ticket_file": str(bad)})
        check("the snapshot is written, from the ticket the person passed", (task_root / "work" / "ticket-snapshot.json").is_file())
    finally:
        harness.cleanup(root)


def s0_two_passes() -> None:
    check_eq = eq
    task = "QA-1"

    # --- (k)(l) a `go on` belongs to ONE block; a BOM and quotes around it still read as `go on` ------
    root, task_root, env = s0_project(task, git=False)        # no git working tree: readiness stops too
    try:
        bad = root / "incomplete-ticket.md"
        bad.write_text(LOST_READ_TICKET, encoding="utf-8")
        out = s0_run(root, env, task, "--ticket-file", str(bad))
        check_eq("(l) setup: the incomplete ticket asks first", s0_state(task_root).get("s0_block"), "ticket_incomplete")
        out = s0_answer(root, env, task, "go on")
        check_eq("D1(l) after `go on` for the ticket, readiness still asks: exit 3", out.returncode, 3, out.stdout[-800:])
        check_eq("D1(l) the block is readiness - the ticket's word did not pass it", s0_state(task_root).get("s0_block"), "readiness")
        check("D1(l) and nothing was written as a pipeline", not (task_root / "pipeline.json").exists())
        ready = s0_question(task_root)
        check_in("D1(l) it is a refusal-kind question", "kind: refusal", ready)
        check_in("D1(l) with its answers as priced option lines: `retry`", "(a) `retry` — fix what the report names, and I check again", ready)
        check_in("D1(l) and `go on`", "(b) `go on` — start the story anyway", ready)
        check_in("D1(l) and `stop`", "(c) `stop` — stop the story here; nothing runs", ready)
        check_eq("D1(l) every option has its three price lines", price_broken(ready), [])
        check_in("D1(l) the report is beside it, not in it", "vcs",
                 (task_root / "state" / "driver-question-details.md").read_text(encoding="utf-8"))
        check_not_in("D1(l) not in the body", "THIS STORY CANNOT START", ready)
        check_eq("D1(l) the readiness question obeys human-questions.md", rules_broken(ready), [])
        # (the "new problem raises the ticket block again" step is gone with the phrase check, t-267 F4: the one
        # problem the check finds is "no acceptance criteria", so there is no wider set to pass)
        # (k) the second `go on`, with a BOM, quotes and a full stop, is its own pass
        out = s0_answer(root, env, task, BOM + '"Go on."')
        check_eq("D1(k) a `go on` with a BOM, quotes and a full stop is read: exit 0", out.returncode, 0,
                 out.stdout[-1200:] + out.stderr[-500:])
        pipeline = s0_pipeline(task_root)
        passes = [w for w in pipeline["warnings"] if "passed by the person's word" in w]
        check_eq("D1(k) one warning per block passed", len(passes), 2)
        check_in("D1(k) the readiness pass is its own line", "S0: the readiness check passed by the person's word", passes)
        findings = s0_findings(root)
        check_in("D1(k) the readiness pass has its own finding", "idempotency:s0-pass:QA-1:readiness", findings)
        check_in("D1(k) beside the ticket's", "idempotency:s0-pass:QA-1:ticket_incomplete", findings)
        check_eq("D1(k) no conductor at any point", stub_calls(root), [])
        journal = [e for e in s0_journal(root) if e.get("event") == "human_answer"]
        check_eq("D1(k) every answer is a human_answer", len(journal), 2)
    finally:
        harness.cleanup(root)


def s0_pasted_ticket() -> None:
    check_eq = eq
    task = "QA-1"

    # --- (j) a pasted ticket passes the incomplete block, verbatim --------------------------------
    root, task_root, env = s0_project(task)
    try:
        bad = root / "incomplete-ticket.md"
        bad.write_text(LOST_READ_TICKET, encoding="utf-8")
        s0_run(root, env, task, "--ticket-file", str(bad))
        pasted = FIXTURE_TICKET.replace("Items can carry tags", "Items can carry tags (pasted)")
        out = s0_answer(root, env, task, pasted, "--ticket-file", str(bad))
        check_eq("D1(j) a pasted ticket passes the incomplete block: exit 0", out.returncode, 0, out.stdout[-1200:] + out.stderr[-500:])
        saved = task_root / "state" / "driver-tmp" / "ticket-QA-1.md"
        check_eq("D1(j) it was kept verbatim", saved.read_text(encoding="utf-8"), pasted.strip())
        snapshot = json.loads((task_root / "work" / "ticket-snapshot.json").read_text(encoding="utf-8"))
        check_eq("D1(j) and the snapshot is made from it, not from the file the flag named", snapshot["title"], "Items can carry tags (pasted)")
        check("D1(j) no pass was recorded - nothing was passed",
              not [w for w in s0_pipeline(task_root)["warnings"] if "passed by the person's word" in w])
        check_not_in("D1(j) and no finding", "s0-pass", s0_findings(root))
        check_eq("D1(j) no conductor", stub_calls(root), [])
        check_eq("K4: the paste is labelled `person_pasted` by the route, never by the text", snapshot["provenance"]["source"], "person_pasted")
    finally:
        harness.cleanup(root)

    # --- C9: any non-empty text is the ticket; the parser decides what it found ------------------------
    root, task_root, env = s0_project(task)
    try:
        bad = root / "incomplete-ticket.md"
        bad.write_text(LOST_READ_TICKET, encoding="utf-8")
        out = s0_run(root, env, task, "--ticket-file", str(bad))
        first = s0_question(task_root)
        typed = "# " + NOT_A_TICKET + "\n\n## Acceptance criteria\n\nNo criteria in what I typed."
        out = s0_answer(root, env, task, typed)
        check_eq("C9: words that are no door are taken as the pasted ticket: a criteria heading with prose under it reads no criteria, so exit 3",
                 out.returncode, 3, out.stdout[-800:])
        check_eq("C9: the paste was kept as typed", (task_root / "state" / "driver-tmp" / f"ticket-{task}.md").read_text(encoding="utf-8"), typed)
        again = s0_question(task_root)
        stored = "qa-factory/artifacts/QA-1/state/driver-tmp/ticket-QA-1.md"
        check_eq("C9: it is the ticket now: the same block asks again",
                 (s0_state(task_root).get("s0_block"), "ticket_incomplete" in s0_state(task_root).get("s0_block")), ("ticket_incomplete", True))
        # t-287 item 6: the question names the file actually read. The first one named the flag's file, this one names the
        # stored paste (what `retry` re-reads): the text CHANGED, so the "answered this exact question before" note is not
        # owed here (FR-7: it moves or comes back changed); it is owed on the next ask, whose text is this one's.
        check_eq("t-287 item 6: the first question names the file the flag gave, the second the stored paste - the file a retry reads",
                 (f"`{bad.name}`" in first, f"`{stored}`" in first, f"`{stored}`" in again, "incomplete-ticket" in again),
                 (True, False, True, False))
        check_not_in("C9: and nothing was read for a phrase", "mentions acceptance criteria", again)
        check_eq("K13: the re-asked question obeys human-questions.md", rules_broken(first) + rules_broken(again), [])
        out = s0_answer(root, env, task, "# " + NOT_A_TICKET + "\n\n## Acceptance criteria\n\nNo criteria in what I typed.\n\nStill nothing else.")
        third = s0_question(task_root)
        check_eq("C9 / FR-7: the third ask is the second one's text: the person's earlier answer is shown",
                 (out.returncode, s0_state(task_root).get("s0_block"), third.count("You have answered this exact question before")), (3, "ticket_incomplete", 1))
        check_eq("K13: and it obeys the rules", rules_broken(third), [])
    finally:
        harness.cleanup(root)


def s0_ticket_units() -> None:
    """The pieces of the S0 ticket route that need a Driver in this process: what is a pasted text (K6 negative), the
    one structural check (F4, F5), a snapshot already on disk (K11 temporal, F3's partial read), the tracker's door."""
    import contextlib
    import io
    import story_run
    task = "QA-1"
    root, task_root, env = s0_project(task, config={"environments": [{"name": "Local"}]})
    try:
        driver = driver_for(root, env, task)
        eq("C9: `go on`, `retry`, `not needed`, `stop`, a stand's name are no text; a title line is; white space is not",
           [driver.s0_is_text(w) for w in ("go on", " Retry. ", "`not needed`", "local", "# A title", "go on and fix it", "", "  \n",
                                           "stop", " `Stop.` ", "stop and fix it")],
           [False, False, False, False, True, True, False, False, False, False, True])
        # F4: a ticket with no title is refused, with what was expected and the way on (FR-1); one with a title and criteria passes in silence
        try:
            driver.s0_criteria({"key": task, "title": task, "acceptance_criteria": ["one"]}, "from the ticket file")
            check("F4: a ticket whose title is only its key is refused", False)
        except story_run.Person as person:
            # P05 (C1-3 F2 a): the `ticket_no_title` question with the paste door, never a Refusal that says "run the story again"
            eq("F4: the ticket with no title is the `ticket_no_title` question (halt, exit 3)", (person.kind, person.code, driver.state.get("s0_block")),
               ("halt", 3, "ticket_no_title"))
            check_in("F4: it names what is wrong and what is expected", "carries no title. The story needs a ticket with a title", person.text)
            check_not_in("F4: and puts no command to the person", "run the story again", person.text)
            check_not_in("F4: nor a flag", "--ticket-file", person.text)
            check_in("F4: the answers are priced, `stop` among them", "`stop`", person.text)
            eq("F4: its doors are `retry` and `stop`, and the paste", (sorted(driver.state["s0_ask"]["doors"]), driver.state["s0_ask"]["paste"]),
               (["retry", "stop"], True))
            driver.state.pop("s0_block", None)
            driver.state.pop("s0_ask", None)
        driver.s0_criteria({"key": task, "title": "Titled", "acceptance_criteria": ["one"]}, "from the ticket file")
        check("F4: a titled ticket with criteria passes in silence (no question, no state)", not driver.state.get("s0_block"))

        # K11 (temporal): a snapshot of the routes before D-06 is read as it is, labelled, never rewritten
        work = task_root / "work"
        work.mkdir(parents=True, exist_ok=True)
        path = work / "ticket-snapshot.json"
        for label, said in (("file", "file (route before D-06 unknown)"), ("jira_direct_api", "fetched (older label)"),
                            ("fetched", "fetched"), ("person_pasted", "person_pasted"), ("agent", "agent (route removed by D-06)"),
                            (None, "unknown (no provenance recorded)")):
            old = {"key": task, "title": "Old", "acceptance_criteria": ["one"], "comments": [],
                   "provenance": {"source": label, "fetched_at": None} if label else {}}
            path.write_text(json.dumps(old, indent=2), encoding="utf-8")
            before = hashlib.sha256(path.read_bytes()).hexdigest()
            printed = io.StringIO()
            with contextlib.redirect_stdout(printed):
                ticket, text, how, kept = driver.s0_ticket(None)
            eq(f"K11: a snapshot labelled `{label}` is kept as it is (one line, no read, the file's own text)",
               (kept, ticket["title"], text == path.read_bytes().decode("utf-8"), hashlib.sha256(path.read_bytes()).hexdigest() == before,
                printed.getvalue().strip()),
               (True, "Old", True, True, f"S0: work/ticket-snapshot.json is already there ({said}); it is read as it is and not written again"))
        # F3: "not needed" with a snapshot already there goes on with it, said in words
        driver.state["s0_answers"] = {"ticket_read": "not needed"}
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            driver.s0_ticket(None)
        check_in("F3: `not needed` with a part already read: the story goes on with it, and says so",
                 "you said the ticket is not needed, so the story goes on with it", printed.getvalue())
        # ... and without one the story ends, honestly, with the reason and the door (FR-57), and nothing is read
        path.unlink()
        calls = []
        driver.py_stdout = lambda *a, **k: calls.append(a) or (0, "{}", "")
        try:
            driver.s0_ticket(None)
            check("F3: `not needed` with nothing read ends the story", False)
        except story_run.Person as person:
            # P01 (C1-3 F2 a): the question again with its way on - `retry` drops the earlier `not needed`, the paste, `stop` - and no
            # command to run by hand; nothing was read (no adapter call)
            eq("F3: it is the `ticket_read` question (halt, exit 3) and nothing was read",
               (person.kind, person.code, driver.state.get("s0_block"), calls), ("halt", 3, "ticket_read", []))
            check_in("F3: it says what was not written", "nothing was written", person.text)
            check_not_in("F3: and names no flag and no command to run again", "--ticket-file", person.text)
            check_not_in("F3: no hand command", "run the same command again", person.text)
            eq("F3: its doors are `retry` and `stop`; the paste is a door", (sorted(driver.state["s0_ask"]["doors"]), driver.state["s0_ask"]["paste"]),
               (["retry", "stop"], True))
            driver.state.pop("s0_block", None)
            driver.state.pop("s0_ask", None)
        driver.state.pop("s0_answers")
        # F-1 (critic t-689, G19): `retry` drops the earlier `not needed` ONLY at the ticket's own question; at any other block the
        # person's word about the ticket survives (and `launch.ticket_not_needed` is still set where the ticket is read)
        for block, survives in (("readiness", True), ("ticket_incomplete", True), ("source_list", True), ("ticket_read", False)):
            driver.state["s0_answers"] = {"ticket_read": "not needed"}
            driver.state["pending_words"] = {"S0": "retry"}
            driver.state["s0_block"], driver.state["s0_ask"] = block, {"kind": "halt", "text": "q", "doors": {"retry": "retry"}}
            driver.s0_read_word()
            eq(f"F-1: `retry` at `{block}` " + ("keeps" if survives else "drops") + " the earlier `not needed`",
               (driver.state["s0_answers"].get("ticket_read") == "not needed"), survives)
        driver.state.pop("s0_answers")
        # a read that comes back forgets the failure remembered from a moment ago (it would otherwise hide a later comparison)
        driver.state["s0_rest_failed"] = "an earlier failure"
        driver.py_stdout = lambda *a, **k: (0, json.dumps({"key": task, "title": "T", "acceptance_criteria": ["one"]}), "")
        got = driver.s0_rest_read()
        eq("the tracker answered: the remembered failure is forgotten, the ticket is returned",
           ("s0_rest_failed" in driver.state, got[0]["title"]), (False, "T"))

        # C4/C5: the tracker's lost login is an infrastructure stop that names the door (the token variable the config names)
        driver.config["adapters"] = {"ticket": {"kind": "jira", "method": "agent", "invoke": "jira-assistant",
                                                "direct_api": {"base_url": "https://jira.example.test", "auth_type": "basic_token",
                                                               "username_ref": "QA_JIRA_EMAIL", "secret_ref": "QA_JIRA_API_TOKEN"}}}
        driver.py_stdout = lambda *a, **k: (5, "", "ticket_adapter: Jira stopped accepting the token (HTTP 401 while reading the ticket X-1)")
        printed = io.StringIO()
        try:
            with contextlib.redirect_stdout(printed):
                driver.s0_rest_read()
            check("C4: exit 5 stops the run", False)
        except story_run.Person as person:
            # F3 (a) (C1-3): the lost tracker login is the `ticket_auth` question (exit 3), not `claude -p`'s infrastructure (exit 5)
            eq("C4: exit 5 is the `ticket_auth` question (halt, exit 3), never the `ticket_read` one and never InfraStop",
               (person.kind, person.code, driver.state.get("s0_block")), ("halt", 3, "ticket_auth"))
            check_in("C4: it says nothing was recorded as not found", "nothing was recorded as not found", person.text)
            check_not_in("C4: the variable is not in the body", "QA_JIRA_API_TOKEN", person.text)
            check_in("C4: it is in the answer block, the one place an instruction may stand", "QA_JIRA_API_TOKEN", person.answer_note)
            eq("C4: its doors are `retry`, `not needed` and `stop`; the paste is a door",
               (sorted(driver.state["s0_ask"]["doors"]), driver.state["s0_ask"]["paste"]), (["not needed", "retry", "stop"], True))
        except story_run.InfraStop:
            check("C4: a lost tracker login is no longer an infrastructure stop", False)
        driver.state.pop("s0_block", None)
        driver.state.pop("s0_ask", None)
    finally:
        harness.cleanup(root)


def s0_reask_battery() -> None:
    """(g)(m) and the edges of the person's word, on a stop that takes NO text (the launch flags): what is not one of its
    answers comes back as the SAME question with a changed body (FR-7); the quote is cut at 300 characters, visibly; the
    journal keeps the words whole (t-208 / FR-8); an empty file is today's Stop; a token inside other words is not the token
    (FR-12); another script and 10 000 characters ask again without a crash. (Until t-267 this ran on `ticket_incomplete`,
    which now takes any non-empty text as the pasted ticket, C9.)"""
    import story_run
    check_eq = eq
    task = "QA-1"
    root, task_root, env = s0_project(task, config={"environments": [{"name": "Local"}]})
    mr = "https://githost.example.invalid/g/a/-/merge_requests/1"
    try:
        out = s0_run(root, env, task, "--mr", mr, "--branch", "feature/x")
        first = s0_question(task_root)
        check_eq("setup: two launch sources ask which to keep", s0_state(task_root).get("s0_block"), "flags")
        set_control(root, NO_USABLE)
        # D-0041: a rerun with NO `--answer` is not new words - the open question comes back and no conductor is called
        out = s0_run(root, env, task, "--mr", mr, "--branch", "feature/x")
        eq("D-0041: a rerun with no `--answer` asks again (exit 3) and calls no conductor", (out.returncode, conductor_count(root)), (3, 0))
        check_in("D-0041: and it is the same priced question", "## What each answer costs and does", s0_question(task_root))

        # (g) not one of the answers: the SAME question comes back with a changed body - and the conductor read the words first
        out = s0_answer(root, env, task, NOT_A_TICKET)
        check_eq("D1(g) an unrecognised answer asks again: exit 3", out.returncode, 3, out.stdout[-800:])
        again = s0_question(task_root)
        check_in("D1(g) the body opens with the changed sentence (the ONE lead of an unread answer)",
                 f'Your answer "{NOT_A_TICKET}" {UNREAD_LEAD}', again)
        check_not_in("D1(g) the old 'nothing moved, it takes only' lead is gone", "it takes only", again)
        check_in("D1(g) and offers the answers again, priced, `stop` among them", "(b) `branch` — keep a branch and drop the other one", again)
        check_in("D1(g) the held `stop` door is in it", "`stop` — stop the story here; nothing runs", again)
        eq("D1(g) every option of the re-ask has its three price lines", price_broken(again), [])
        check_in("D1(g) followed by the question as it was", "more than one place to take the code from", again)
        check("D1(g) FR-7: the body is not the one already answered",
              story_run.question_body_sha(first) != story_run.question_body_sha(again))
        eq("D-0041: an unread `--answer` is exactly ONE conductor call", conductor_count(root), 1)
        check_eq("D1(g) the block stays open", s0_state(task_root).get("s0_block"), "flags")
        check_eq("D1(g) the re-asked question obeys human-questions.md", rules_broken(again), [])
        check("D1(g) the answer is on the journal as a human_answer",
              any(e.get("event") == "human_answer" and "S0 flags: " + NOT_A_TICKET in str(e.get("notes"))
                  for e in s0_journal(root)), str(s0_journal(root))[-400:])
        # the quote's limit: 300 characters whole, 301 cut, and the cut is visible
        out = s0_answer(root, env, task, "x" * 300)
        check_in("D1(g) a 300-character answer is quoted whole", 'Your answer "' + "x" * 300 + '" is not one', s0_question(task_root))
        out = s0_answer(root, env, task, "x" * 301)
        long_q = s0_question(task_root)
        check_in("D1(g) a 301-character answer is cut at 300, visibly", 'Your answer "' + "x" * 300 + CUT + '" is not one', long_q)
        check_not_in("D1(g) and not quoted past it", "x" * 301, long_q)
        out = s0_answer(root, env, task, "y" * 10000)
        check_eq("D1(g) a 10 000-character answer asks again without a crash", out.returncode, 3, out.stderr[-500:])
        check_in("D1(g) quoting 300 of it", 'Your answer "' + "y" * 300 + CUT + '"', s0_question(task_root))
        # t-208 / FR-8: the quote above is the QUESTION's limit; the journal note is the person's words,
        # and every later brief reads it - it carries them whole, not cut at 1,500 (cmp2, 01.10)
        notes = [str(e.get("notes")) for e in s0_journal(root) if e.get("event") == "human_answer"]
        check("t-208 a 10 000-character S0 answer is in its human_answer note whole",
              "S0 flags: " + "y" * 10000 in notes, str([len(n) for n in notes]))
        check("t-208 and so is the 301-character one (past the quote's 300)",
              "S0 flags: " + "x" * 301 in notes, str([len(n) for n in notes]))
        # an answer file with nothing in it, or only white space, is today's Stop: nothing is asked
        # again and nothing is consumed - the question stays open for a real answer
        for empty in ("", "  \n\t "):
            out = s0_answer(root, env, task, empty)
            check_eq("edge: an empty answer file stops with the existing error", out.returncode, story_run.EXIT_ERROR, out.stdout[-300:])
            check_in("edge: and says the file is empty", "is empty", out.stdout)
        check_eq("edge: the block is still open after an empty answer", s0_state(task_root).get("s0_block"), "flags")
        # FR-12, behaviourally: an offered token INSIDE other words is not the token. The code
        # reads no phrase; "please branch now" is not `branch`, so nothing moves and it is asked again.
        out = s0_answer(root, env, task, "please branch now")
        check_eq("FR-12: an answer that merely contains an offered token is asked again: exit 3", out.returncode, 3, out.stdout[-300:])
        check_in("FR-12: with the changed sentence", 'Your answer "please branch now" is not one of the answers',
                 s0_question(task_root))
        check("FR-12: and it passed nothing", not (task_root / "pipeline.json").exists()
              and not s0_state(task_root).get("s0_passes"))
        # (m) an answer written with \u escapes (a person's own language) is asked again, not a crash
        out = s0_answer(root, env, task, OTHER_SCRIPT)
        check_eq("D1(m) an answer in another script asks again: exit 3", out.returncode, 3, out.stderr[-500:])
        check_in("D1(m) and quotes it back", OTHER_SCRIPT, s0_question(task_root))
        check("D1(m) with no traceback", "Traceback" not in out.stderr and "Traceback" not in out.stdout)
        # the same words twice: the second question is the first one's twin, and says it was answered before
        out = s0_answer(root, env, task, "retry")
        out = s0_answer(root, env, task, "retry")
        check_in("FR-7: the second identical re-ask says it was answered before", "You have answered this exact question before",
                 s0_question(task_root))
        # D-0041: the unread answers of the whole path (NOT_A_TICKET, x300, x301, y10000, "please branch now", the other script, `retry` twice;
        # the two empty files are today's Stop, `stop` is held) were exactly one conductor call each; the rerun at the top made none
        eq("D-0041: one conductor call per unread `--answer` on the whole path (8 unread answers)", conductor_count(root), 8)
        # G1: a conductor that returns `continue` leaves no stored block behind, and the caller runs the step again (the same question)
        set_control(root, {"conductor": {"action": "continue"}})
        before = conductor_count(root)
        out = s0_answer(root, env, task, "an answer the conductor lets pass")
        state = s0_state(task_root)
        eq("G1: a conductor `continue` -> the step runs again and S0 asks its question once more (exit 3), one call",
           (out.returncode, conductor_count(root) - before, state.get("s0_block")), (3, 1, "flags"))
        check("G1: and nothing was passed or decided by it", not (task_root / "pipeline.json").exists() and not state.get("s0_passes"))
    finally:
        harness.cleanup(root)


def s0_launch_flags() -> None:
    check_eq = eq
    task = "QA-1"

    # --- (i) flags: keep one launch source; `go on` and a stand name are not answers here -----------
    root, task_root, env = s0_project(task, config={"environments": [{"name": "Local"}]})
    try:
        out = s0_run(root, env, task, "--mr", "https://githost.example.invalid/g/a/-/merge_requests/1", "--branch", "feature/x")
        check_eq("D1(i) two launch sources ask which to keep: exit 3", out.returncode, 3, out.stdout[-800:])
        ask = s0_question(task_root)
        check_in("D1(i) in the story's words, with the two doors as priced option lines", "(a) `mr` — keep a merge request and drop the other one", ask)
        check_in("D1(i) the second door", "(b) `branch` — keep a branch and drop the other one", ask)
        check_in("D1(i) and `stop`", "(c) `stop` — stop the story here; nothing runs", ask)
        check_eq("D1(i) every option has its three price lines", price_broken(ask), [])
        check_not_in("D1(i) never offering the one that was not given", "`commit`", ask)
        check_eq("D1(i) the flags question obeys human-questions.md", rules_broken(ask), [])
        check_eq("D1(i) the block is remembered", s0_state(task_root).get("s0_block"), "flags")
        set_control(root, NO_USABLE)                 # a conductor with no usable options: the seam shows the SITE's question again
        out = s0_answer(root, env, task, "go on")
        check_in("D1(i) `go on` is not offered here, so it is asked again, changed",
                 UNREAD_LEAD, s0_question(task_root))
        out = s0_answer(root, env, task, "local")
        check_in("D1(i) a stand's name on a block that is not about a stand is not an answer either",
                 'Your answer "local" ' + UNREAD_LEAD, s0_question(task_root))
        eq("D-0041: each of the two unread answers was one conductor call", conductor_count(root), 2)
        # C1-3 (P04): `stop` is a door of every S0 question and has its executor here: the question is HELD (exit 3), changed
        # in its first line (FR-7), with no conductor, nothing written, nothing kept for the next step, the block still open.
        out = s0_answer(root, env, task, "stop")
        eq("S0 stop: a whole-answer `stop` holds the question: exit 3", out.returncode, 3, out.stdout[-800:])
        held = s0_question(task_root)
        check_in("S0 stop: the first line says nothing runs and nothing is spent", "You said to stop. Nothing runs and nothing is spent.", held)
        check_in("S0 stop: and how to go on after all, naming the other doors", "answer `mr` or `branch`.", held)
        check_in("S0 stop: followed by the question as it was", "more than one place to take the code from", held)
        check_not_in("S0 stop: it is not the 'not one of the answers' re-ask", "is not one of the answers", held)
        check_eq("S0 stop: the held question obeys human-questions.md", rules_broken(held), [])
        check_eq("S0 stop: every option of the held question has its three price lines", price_broken(held), [])
        stopped = s0_state(task_root)
        check("S0 stop: the block stays open and no words are kept (`pending_words` has no S0)",
              stopped.get("s0_block") == "flags" and "S0" not in (stopped.get("pending_words") or {}), str(stopped.get("pending_words")))
        check("S0 stop: nothing was written and the stop made no conductor call (the two before it are the unread answers)",
              not (task_root / "pipeline.json").exists() and conductor_count(root) == 2)
        check("S0 stop: the word is on the journal as a human_answer",
              any(e.get("event") == "human_answer" and "S0 flags: stop" in str(e.get("notes")) for e in s0_journal(root)))
        # `stop please` is other words: the re-ask of any unread answer, not the stop (FR-12: the code reads the whole token only)
        out = s0_answer(root, env, task, "stop please")
        again = s0_question(task_root)
        check_in("S0 stop: `stop please` takes the unread road (the re-ask)", 'Your answer "stop please" ' + UNREAD_LEAD, again)
        check_not_in("S0 stop: and is not the held question", "You said to stop", again)
        eq("D-0041: `stop please` is other words: exactly one more conductor call", conductor_count(root), 3)
        # a stop answered with an `s0_ask` that an older driver stored (its doors lack `stop`) is still the stop (read-time door)
        old = s0_state(task_root)
        check("S0 stop: setup: the stored ask carries `stop` among its doors", "stop" in old["s0_ask"]["doors"])
        old["s0_ask"]["doors"].pop("stop")
        (task_root / "state" / "driver-state.json").write_text(json.dumps(old), encoding="utf-8")
        out = s0_answer(root, env, task, ' "Stop." ')
        check_in("S0 stop: quoted and full-stopped it is the same stop, on the old driver's ask", "You said to stop. Nothing runs and nothing is spent.",
                 s0_question(task_root))
        out = s0_answer(root, env, task, "`branch`",
                        "--mr", "https://githost.example.invalid/g/a/-/merge_requests/1", "--branch", "feature/x")
        # the stand: one configured stand is selected and probed, and this project has no
        # environment block for the probe - which is a warning since D2, not a stop.
        state = s0_state(task_root)
        check_eq("D1(i) `branch` keeps only branch, over the command line that still says both",
                 {k: v for k, v in state["launch"].items() if k in ("mr", "branch", "commit")}, {"branch": "feature/x"})
        check("D1(i) the flags block is behind us", state.get("s0_block") != "flags")
        eq("D1(i) the doors (`branch`, `stop`) made no conductor call: only the three unread answers did", conductor_count(root), 3)
    finally:
        harness.cleanup(root)


def k5_the_agent_is_never_called() -> None:
    """K5: zero agent calls (the stub's count is 0) with `method: agent` and a usable `direct_api`, AND with an
    unusable one; the removed names are nowhere in the driver (grep, with a positive control of the same form)."""
    # a usable direct_api: the ticket comes by REST, the agent stays a write channel
    jira = FakeJira(story_15045())
    root, task_root, env = rest_project(jira)
    try:
        out = s0_run(root, env, KEY)
        eq("K5: `method: agent` + a usable direct_api: S0 reads the ticket by REST and finishes: exit 0", out.returncode, 0,
           out.stdout[-1500:] + out.stderr[-800:])
        snapshot = snapshot_of(task_root)
        eq("K5: the snapshot is the light form of the tracker's answer (15 criteria, the parent), `fetched`",
           (len(snapshot["acceptance_criteria"]), snapshot["parent"], snapshot["provenance"]["source"]), (15, "TP1-14482", "fetched"))
        eq("K5: ONE read of the tracker: the issue with every field, `/field`, the remote links (3 requests), no per-key GET",
           sorted(jira.log), sorted([f"/rest/api/2/issue/{KEY}?fields=*all", "/rest/api/2/field", f"/rest/api/2/issue/{KEY}/remotelink"]))
        eq("K5: stub count 0: no agent, no conductor, no model at all", stub_calls(root), [])
        check("K5: the raw folder and the role's files are beside the snapshot (the adapter's own files)",
              all((task_root / "work" / name).exists() for name in ("ticket-raw/issue.json", "ticket-raw/issue.pretty.json", "ticket-view.md", "ticket-references.json")))
        check("K5: and no tracker-agent line is printed", "tracker agent" not in out.stdout)
        view_text = (task_root / "work" / "ticket-view.md").read_bytes().decode("utf-8")
        check("t-281: on the REST leg the view is the story's own text: no comparison line", "read for comparison" not in view_text and view_text.startswith(KEY), view_text[:200])
        # the revision the controller keeps is the hash of that one snapshot (stable: the file is never rewritten)
        controller = json.loads((task_root / "state" / "controller.json").read_text(encoding="utf-8"))
        eq("K5: source_revision is the sha256 of the snapshot", controller.get("source_revision"),
           hashlib.sha256((task_root / "work" / "ticket-snapshot.json").read_bytes()).hexdigest())
    finally:
        jira.stop()
        harness.cleanup(root)
    # an unusable one: no direct_api at all - the question, and still no agent
    root, task_root, env = s0_project("QA-1", config={"adapters": {"ticket": {"kind": "jira", "method": "agent", "invoke": "jira-assistant"}}})
    try:
        out = s0_run(root, env, "QA-1")
        eq("K5: `method: agent` with no direct_api: the person is asked: exit 3", out.returncode, 3, out.stdout[-800:])
        eq("K5: the block is `ticket_read`, stub count 0", (s0_state(task_root).get("s0_block"), stub_calls(root)), ("ticket_read", []))
        ask = s0_question(task_root)
        check_in("K5: the question says no way to read is set up, and that the assistant only writes",
                 "the Jira assistant is not used to read tickets - it only writes to them", ask)
        check_in("K5: and 'how to get it' names recording the tracker's address and token for the project",
                 "record the tracker's address and token for this project (onboarding does it)", ask)
    finally:
        harness.cleanup(root)
    src = harness.driver_text()
    pattern = r"ticket_incomplete|ticket_by_agent|TICKET_SHAPE|\"ticket_agent\"|ticket_problems|check_ticket"
    found = sorted(set(re.findall(pattern, src)))
    eq("K5: grep of the driver set: the removed names have 0 hits, and the same pattern finds the surviving `ticket_incomplete` (positive control)",
       found, ["ticket_incomplete"])
    print(f"K5: grep -E '{pattern}' driver set -> {sorted(set(re.findall(pattern, src)))} ({len(re.findall(pattern, src))} hits, all of them the control)")


def k6_ticket_read_question() -> None:
    """K6: the tracker cannot be read: the `ticket_read` question carries FR-50's three answers and obeys the rules;
    `retry` reads again; the ticket as text becomes the snapshot; `go on` is not one of its answers; `not needed`
    with nothing read ends the story honestly."""
    jira = FakeJira([(f"/issue/{KEY}", 404), ("/myself", {"accountId": "x"})])
    root, task_root, env = rest_project(jira)
    try:
        out = s0_run(root, env, KEY)
        eq("K6: a 404 on the story's own key asks the person (never a stop for the login): exit 3", out.returncode, 3, out.stdout[-800:])
        ask = s0_question(task_root)
        eq("K6: the block is `ticket_read`", s0_state(task_root).get("s0_block"), "ticket_read")
        check("K6: three answers are present as priced option lines: `not needed`, `retry` (after fixing the way in), and the ticket as text, then `stop`",
              all(word in ask for word in ("(a) `not needed` — the story can go without this ticket", "(b) `retry` — ",
                                           ", and I read the ticket again", "(c) paste the ticket here as text",
                                           "(d) `stop` — stop the story here; nothing runs")), ask)
        eq("K6: every option has its three price lines", price_broken(ask), [])
        check_in("K6: the priced section is in the body, above the answer block", "## What each answer costs and does", ask.split("\n---\n")[0])
        check_not_in("K6: the hand command is gone from the question", "run the same command again", ask)
        eq("K6: rules_broken == []", rules_broken(ask), [])
        check_in("K6: the question names the route tried and why it failed, in the story's words",
                 f"I asked the tracker for {KEY} through its web interface, with the account recorded for this project, and it answered "
                 "that there is no such ticket, or that this account may not see it.", ask)
        check_not_in("K6: no agent is offered or named as a way to read", "assistant", ask)
        details = (task_root / "state" / "driver-question-details.md").read_text(encoding="utf-8")
        check_in("K6: the adapter's own words are beside it, not in it", "was not found (HTTP 404)", details)
        check_not_in("K6: and not in the body", "HTTP 404", ask)
        eq("K6: nothing was written for the story yet, and nobody was called", ((task_root / "pipeline.json").exists(),
                                                                             (task_root / "work" / "ticket-snapshot.json").exists(), stub_calls(root)),
           (False, False, []))
        # negative: `go on` is not one of the answers
        set_control(root, NO_USABLE)
        out = s0_answer(root, env, KEY, "go on")
        again = s0_question(task_root)
        check_in("K6 negative: `go on` gets the 'not one of the answers' re-ask (the one lead), then the question itself",
                 f'Your answer "go on" {UNREAD_LEAD}', again)
        check("K6 negative: ... with its four answers as priced option lines, `retry`, `not needed`, the ticket as text, `stop`",
              all(word in again for word in ("(a) `not needed` — ", "(b) `retry` — ", "(c) paste the ticket here as text", "(d) `stop` — ")), again)
        eq("K6 negative: every option of the re-ask has its three price lines", price_broken(again), [])
        eq("K6 negative: the block stays open, the re-ask obeys the rules, nothing moved",
           (s0_state(task_root).get("s0_block"), rules_broken(again), (task_root / "pipeline.json").exists()), ("ticket_read", [], False))
        eq("D-0041: the unread `go on` was exactly one conductor call", conductor_count(root), 1)
        asked_before = len(jira.log)
        # `retry` re-reads: the tracker came back
        jira.serve(story_15045())
        out = s0_answer(root, env, KEY, "retry")
        eq("K6: `retry` reads the ticket again, and S0 finishes: exit 0", out.returncode, 0, out.stdout[-1500:] + out.stderr[-600:])
        check("K6: the read was made again (the tracker was asked after the answer)", len(jira.log) > asked_before)
        eq("K6: and the snapshot is the tracker's (`fetched`)", snapshot_of(task_root)["provenance"]["source"], "fetched")
        eq("K6: no agent; the conductor was called for the unread `go on` only, never for `retry`",
           [c["kind"] for c in stub_calls(root)], ["conductor"])
    finally:
        jira.stop()
        harness.cleanup(root)
    # the ticket as text: the paste becomes the snapshot, `person_pasted`; the tracker, known to be down, is not asked again
    jira = FakeJira([(f"/issue/{KEY}", 404)])
    root, task_root, env = rest_project(jira)
    try:
        s0_run(root, env, KEY)
        asked_before = len(jira.log)
        pasted = FIXTURE_TICKET.replace("QA-1", KEY)
        out = s0_answer(root, env, KEY, pasted)
        eq("K6: the ticket as text ends the question: exit 0", out.returncode, 0, out.stdout[-1500:] + out.stderr[-600:])
        snapshot = snapshot_of(task_root)
        eq("K6: paste -> snapshot, provenance `person_pasted`, the paste kept as typed",
           (snapshot["provenance"]["source"], (task_root / "state" / "driver-tmp" / f"ticket-{KEY}.md").read_text(encoding="utf-8")),
           ("person_pasted", pasted.strip()))
        lines = [ln for ln in out.stdout.splitlines() if "could not be read for comparison" in ln]
        eq("C6: the tracker could not be read for comparison: ONE line, never a question, and no new request (it was down a moment ago)",
           (len(lines), len(jira.log) == asked_before, "disagreements" in snapshot), (1, True, False))
        print("C6 line: " + lines[0])
        eq("K6: no agent, no conductor", stub_calls(root), [])
    finally:
        jira.stop()
        harness.cleanup(root)
    # `not needed` with nothing read (P01, C1-3 F2 a): not an exit with a command to run by hand but the `ticket_read` question again,
    # with its way on in it - `retry` (the earlier `not needed` is dropped), the ticket as text, `stop` (FR-57: a ban has a door)
    jira = FakeJira([(f"/issue/{KEY}", 404)])
    root, task_root, env = rest_project(jira)
    try:
        s0_run(root, env, KEY)
        out = s0_answer(root, env, KEY, "Not needed.")
        held = s0_question(task_root)
        eq("P01: `not needed` with nothing read is a question: exit 3, nothing written, nobody called",
           (out.returncode, "story_run: stopped" in out.stdout, (task_root / "pipeline.json").exists(),
            (task_root / "work" / "ticket-snapshot.json").exists(), stub_calls(root)), (3, False, False, False, []), out.stdout[-900:])
        check_in("P01: it says nothing was written, in the story's words", "nothing was written", held)
        check_not_in("P01: and names no flag and no command to run by hand", "--ticket-file", held)
        check_not_in("P01: no 'run the same command again'", "run the same command again", held)
        check("P01: its three answers are priced option lines: `retry`, the ticket as text, `stop`",
              all(word in held for word in ("(a) `retry` — ", "(b) paste the ticket here as text", "(c) `stop` — ")), held)
        eq("P01: every option has its three price lines, the text obeys the rules", (price_broken(held), rules_broken(held)), ([], []))
        eq("P01: the block is `ticket_read`", s0_state(task_root).get("s0_block"), "ticket_read")
        seen = len(jira.log)
        out = s0_run(root, env, KEY)
        eq("P01/FR-7: a rerun with no `--answer` asks the same question again without reading the tracker, and calls no conductor",
           (out.returncode, len(jira.log) == seen, stub_calls(root)), (3, True, []))
        ticket = root / "ticket.md"
        ticket.write_text(FIXTURE_TICKET.replace("QA-1", KEY), encoding="utf-8")
        out = s0_run(root, env, KEY, "--ticket-file", str(ticket))
        eq("P01: a `--ticket-file` on the command line still reads: S0 finishes", out.returncode, 0, out.stdout[-900:] + out.stderr[-500:])
    finally:
        jira.stop()
        harness.cleanup(root)
    # P01 `retry`: the earlier `not needed` is dropped and the ticket is read again; the paste: G19 - an earlier `not needed` is dropped too
    for door in ("retry", "paste"):
        jira = FakeJira([(f"/issue/{KEY}", 404)])
        root, task_root, env = rest_project(jira)
        try:
            s0_run(root, env, KEY)
            s0_answer(root, env, KEY, "Not needed.")
            asked_before = len(jira.log)
            if door == "retry":
                jira.serve(story_15045())
                out = s0_answer(root, env, KEY, "retry")
            else:
                out = s0_answer(root, env, KEY, FIXTURE_TICKET.replace("QA-1", KEY))
            eq(f"P01 `{door}`: S0 finishes (exit 0)", out.returncode, 0, out.stdout[-900:] + out.stderr[-500:])
            snapshot = snapshot_of(task_root)
            eq(f"P01 `{door}`: the ticket is read, not skipped",
               (snapshot["provenance"]["source"], (s0_state(task_root).get("launch") or {}).get("ticket_not_needed")),
               ("fetched" if door == "retry" else "person_pasted", None))
            eq(f"P01 `{door}`: no conductor", stub_calls(root), [])
            if door == "retry":
                check("P01 `retry`: the tracker was asked again", len(jira.log) > asked_before)
        finally:
            jira.stop()
            harness.cleanup(root)


def k6_retry_after_and_other_failures() -> None:
    """A tracker that asks to be asked again later: the question names the time (the adapter's `retry_at`, read from
    its error OBJECT - t-281 F3: no sentence is searched for it)."""
    jira = FakeJira([])
    root, task_root, env = rest_project(jira)
    try:
        import story_run
        driver = driver_for(root, env, KEY)
        said = ("ticket_adapter: the tracker could not be read for TP1-15045 (server requested delayed retry); the tracker asked "
                "to be tried again at 2026-10-01T12:30:00Z - retry, or hand the ticket over as text (--ticket-file).")
        failure = {"owner": "tracker", "status": 429, "retry_at": "2026-10-01T12:30:00Z", "message": "x", "file": None, "from_object": True}
        try:
            driver.s0_ticket_read_question(3, said, failure)
            check("retry_at: a question was raised", False)
        except story_run.Person as person:
            check_in("retry_at: the question names the time the tracker asked for", "it asked to be asked again at 2026-10-01T12:30:00Z.", person.text)
            check_in("retry_at: and says it did not answer in a way the factory can use", "did not answer in a way I can use", person.text)
            # (`no_how_to_answer` is the block `ask()` appends under the text; this reads the text before it)
            eq("retry_at: it obeys human-questions.md", [r for r in rules_broken(person.text) if r != "no_how_to_answer"], [])
        try:
            driver.s0_ticket_read_question(3, "ticket_adapter: the tracker could not be read for X (HTTP 503) - retry, or hand it over.",
                                           {"owner": "tracker", "status": 503, "retry_at": None, "message": "x", "file": None, "from_object": True})
        except story_run.Person as person:
            check_not_in("503 with no time named: no time is invented", "asked to be asked again", person.text)
        # t-281 F3, negative control: a sentence that carries a time and an object that does not -> no time (nothing is read from the words)
        try:
            driver.s0_ticket_read_question(3, said, {"owner": "tracker", "status": 503, "retry_at": None, "message": "x", "file": None, "from_object": True})
        except story_run.Person as person:
            check_not_in("F3 negative control: the time in the SENTENCE is not read when the object names none", "2026-10-01T12:30:00Z", person.text)
        # (the source check that RETRY_AT_RE is gone and `def ticket_failure` stands was a source pin of one member: deleted by TD-11 phase 0, F3)
    finally:
        jira.stop()
        harness.cleanup(root)


def k_comparison_person_vs_tracker() -> None:
    """F27 / C6 / FR-25: `--ticket-file` given and REST set up: the person's text is the requirement, the tracker is
    read BESIDE it; both present -> ONE line and `disagreements[]` in the snapshot; the tracker failing -> ONE line, no question."""
    person = ("---\nkey: TP1-15045\ntype: Sub-task\nstatus: Ready for Review\nparent: TP1-14482\n---\n\n"
              "# Testing TP1-14482 Visual Workflow Diff for Revisions\n\nThe person's own copy of the description.\n\n"
              "## Acceptance criteria\n\n1. Visual revision diff opens from workflow version history.\n2. A single graph represents the target revision.\n\n"
              "## Comments\n\n- **po** (2026-09-18): one comment.\n")
    jira = FakeJira(story_15045())
    root, task_root, env = rest_project(jira)
    try:
        file = root / "person.md"
        file.write_text(person, encoding="utf-8")
        out = s0_run(root, env, KEY, "--ticket-file", str(file))
        eq("F27: the person's file and a tracker that says more: S0 finishes, exit 0", out.returncode, 0, out.stdout[-1500:] + out.stderr[-600:])
        snapshot = snapshot_of(task_root)
        lines = [ln for ln in out.stdout.splitlines() if ln.startswith("The person's text is the requirement for this story.")]
        eq("F27: ONE FR-25 line, naming the authority (the person) and the gap", len(lines), 1, out.stdout[-1500:])
        print("FR-25 line (person vs tracker): " + lines[0])
        fields = {d["field"]: d for d in snapshot["disagreements"]}
        eq("F27/K7: `disagreements[]` is in the snapshot: the criteria differ (2 against 15), the comments differ (1 against 1 is equal, so absent)",
           (sorted(fields), (fields["acceptance_criteria"]["person"], fields["acceptance_criteria"]["rest"])), (["acceptance_criteria"], (2, 15)))
        eq("F27: the requirement stays the person's: the snapshot holds their two criteria and `person_pasted`",
           (len(snapshot["acceptance_criteria"]), snapshot["provenance"]["source"]), (2, "person_pasted"))
        eq("F27 / t-281 F4: the comparison read passes the same `--raw-dir` as the REST read: the raw folder, the view and the references are there",
           sorted(p.name for p in (task_root / "work").iterdir() if p.name.startswith("ticket-") and p.name != "ticket-snapshot.json"),
           ["ticket-raw", "ticket-references.json", "ticket-view.md"])
        view_lines = (task_root / "work" / "ticket-view.md").read_bytes().decode("utf-8").split("\n")
        eq("t-281: on the comparison leg `ticket-view.md` opens with ONE line that says it is the tracker's text, read for comparison, "
           "and that the requirement is the person's snapshot; the view's own first line follows",
           (view_lines[0], view_lines[1].startswith(KEY), sum(1 for ln in view_lines if ln.startswith("The tracker's text, read for comparison"))),
           ("The tracker's text, read for comparison; the story's requirement is the text the person gave (ticket-snapshot.json)", True, 1))
        references = json.loads((task_root / "work" / "ticket-references.json").read_text(encoding="utf-8"))
        refs = [row["ref"] for row in references["rows"]]
        eq("F4: the tracker read SUCCEEDED, so the references are the tracker's: one row per reference (the person's text is not scanned twice), "
           "no `unproven` row, written_by [S0]",
           (len(refs) == len(set(refs)), [r for r in references["rows"] if r.get("status") == "unproven"], references["written_by"],
            "TP1-14482" in refs), (True, [], ["S0"], True), json.dumps(references["rows"])[:600])
        eq("F27: no agent, no conductor", stub_calls(root), [])
    finally:
        jira.stop()
        harness.cleanup(root)
    # the tracker says the same: the line says so, and `disagreements` is present and empty (compared: not "unknown")
    jira = FakeJira(story_15045())
    root, task_root, env = rest_project(jira)
    try:
        out = s0_run(root, env, KEY, "--ticket-file", str(_write_same_as_tracker(root, env)))
        snapshot = snapshot_of(task_root)
        eq("K7 negative: the tracker says the same: `disagreements` is [] (compared and equal), and the line says so",
           (snapshot.get("disagreements"), "The tracker now says the same about the title, the acceptance criteria, the number of comments and the parent." in out.stdout),
           ([], True), out.stdout[-900:])
    finally:
        jira.stop()
        harness.cleanup(root)
    # the tracker failing: ONE line, no question, no disagreements (unknown, not "same")
    jira = FakeJira([(f"/issue/{KEY}", 404)])
    root, task_root, env = rest_project(jira)
    try:
        file = root / "person.md"
        file.write_text(person, encoding="utf-8")
        out = s0_run(root, env, KEY, "--ticket-file", str(file))
        lines = [ln for ln in out.stdout.splitlines() if "could not be read for comparison" in ln]
        snapshot = snapshot_of(task_root)
        eq("C6: the comparison read fails: ONE line, never a question: exit 0, `disagreements` absent (unknown is not `same`)",
           (out.returncode, len(lines), "disagreements" in snapshot), (0, 1, False), out.stdout[-1200:])
        print("C6 line: " + lines[0])
        references = json.loads((task_root / "work" / "ticket-references.json").read_text(encoding="utf-8"))
        eq("F4: with no tracker read the references are the PERSON's text: written_by [S0], the ticket row `unproven` - no tracker read at S0",
           (references["written_by"], [(r["ref"], r["status"], r["reason"]) for r in references["rows"] if r["kind"] == "ticket"]),
           (["S0"], [("TP1-14482", "unproven", "no tracker read at S0")]), json.dumps(references)[:500])
        check("F4: and no raw folder was made (no tracker response to keep)", not (task_root / "work" / "ticket-raw").exists())
    finally:
        jira.stop()
        harness.cleanup(root)


def _write_same_as_tracker(root: Path, env: dict) -> Path:
    """The person's file with exactly the tracker's title, criteria (read through the adapter's own light form), comment
    count and parent: what 'the same' looks like (the description is not compared, so it is a short one)."""
    light = harness.run_script("ticket_adapter.py", "get", KEY, "--json", cwd=root, env=env)
    snap = json.loads(light.stdout)
    items = "\n".join(f"{n}. {item}" for n, item in enumerate(snap["acceptance_criteria"], 1))
    comments = "\n".join(f"- **{c['author']}** ({c['date']}): {c['text']}" for c in snap["comments"])
    path = root / "same.md"
    path.write_text(f"---\nkey: {KEY}\nparent: {snap['parent']}\n---\n\n# {snap['title']}\n\nThe person's own copy.\n\n"
                    f"## Acceptance criteria\n\n{items}\n\n## Comments\n\n{comments}\n", encoding="utf-8")
    return path


def k11_a_snapshot_on_disk_is_never_rewritten() -> None:
    """K11 (temporal): a snapshot of the routes before D-06 - the cmp2 `source: file` one, a `jira_direct_api` one - is
    read as it is at S0 and never rewritten; the tracker is not asked; its sha256 is the same after an S0 resume."""
    for label, said in (("file", "file (route before D-06 unknown)"), ("jira_direct_api", "fetched (older label)")):
        jira = FakeJira(story_15045())
        root, task_root, env = rest_project(jira, git=False)            # no git: readiness stops S0 once, so there is a resume
        try:
            old = {"key": KEY, "type": "Sub-task", "status": "Ready for Review", "title": "Testing TP1-14482 Visual Workflow Diff for Revisions",
                   "description": "Purpose: validate TP1-14482.", "acceptance_criteria": ["Visual revision diff opens from workflow version history."],
                   "comments": [{"author": "Test User 7", "date": "2026-09-18T08:20:40.161+0000", "text": "Draft MR"}],
                   "parent": "TP1-14482", "subtasks": [], "links": {"merge_request": None, "branch": None},
                   "provenance": {"source": label, "fetched_at": None}}
            path = task_root / "work" / "ticket-snapshot.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(old, indent=2) + "\n", encoding="utf-8")
            before = hashlib.sha256(path.read_bytes()).hexdigest()
            out = s0_run(root, env, KEY)
            eq(f"K11: S0 over a `{label}` snapshot stops at readiness (the setup of the resume): exit 3", out.returncode, 3, out.stdout[-900:])
            line = f"S0: work/ticket-snapshot.json is already there ({said}); it is read as it is and not written again"
            check_in(f"K11: the label is reported as `{said}`", line, out.stdout)
            out = s0_answer(root, env, KEY, "go on")
            eq("K11: the S0 resume finishes: exit 0", out.returncode, 0, out.stdout[-900:] + out.stderr[-400:])
            after = hashlib.sha256(path.read_bytes()).hexdigest()
            eq(f"K11: the sha256 of the `{label}` snapshot is unchanged after the S0 resume", after, before)
            eq("K11: the tracker was not asked at all (nothing to read: the snapshot is the ticket)", jira.log, [])
            controller = json.loads((task_root / "state" / "controller.json").read_text(encoding="utf-8"))
            eq("K11: and source_revision is that hash (stable across resumes)", controller.get("source_revision"), before)
            print(f"K11: {label}: sha256 {before} before == {after} after the S0 resume; {said}")
        finally:
            jira.stop()
            harness.cleanup(root)
    # a fresh REST snapshot is not read again at a resume either: the read is one, the hash is stable
    jira = FakeJira(story_15045())
    root, task_root, env = rest_project(jira, git=False)
    try:
        s0_run(root, env, KEY)
        path = task_root / "work" / "ticket-snapshot.json"
        before, asked = hashlib.sha256(path.read_bytes()).hexdigest(), len(jira.log)
        out = s0_answer(root, env, KEY, "go on")
        eq("K11: a fresh REST snapshot over an S0 resume: exit 0, the same bytes, no second read",
           (out.returncode, hashlib.sha256(path.read_bytes()).hexdigest() == before, len(jira.log) == asked == 3), (0, True, True), out.stdout[-900:])
        check_in("K11: and it is reported as `fetched`", "is already there (fetched)", out.stdout)
    finally:
        jira.stop()
        harness.cleanup(root)


def k13_no_criteria_section_goes_on_with_a_line() -> None:
    """K13 / D-0050 / P23 (the old K13 asked here): a ticket with NO criteria section (on the tracker route) is no question - S0 goes
    on to its next stop (readiness: no git here), and the story's record carries ONE line, the FIRST of the warnings, that names the
    headings looked for, in at most 180 characters (gate A shows five, each cut there). No finding, no conductor, no agent."""
    issue = {"id": "1", "key": "APP-1", "fields": {"summary": "Items can be tagged", "updated": "2026-09-01T10:00:00.000+0000",
                                                    "description": "A story whose description names no criteria.",
                                                    "comment": {"total": 0, "comments": []}}}
    jira = FakeJira([("/issue/APP-1/remotelink", b"[]"), ("/issue/APP-1?fields=*all", json.dumps(issue).encode("utf-8")), ("/rest/api/2/field", b"[]")])
    root, task_root, env = rest_project(jira, "APP-1", git=False)
    try:
        out = s0_run(root, env, "APP-1")
        eq("K13 / D-0050: 0 criteria and no criteria section: NO ticket question - the first stop is readiness (no git here): exit 3",
           (out.returncode, s0_state(task_root).get("s0_block")), (3, "readiness"), out.stdout[-900:])
        check_not_in("K13: and nothing was asked about criteria", "criteria", s0_question(task_root))
        out = s0_answer(root, env, "APP-1", "go on")
        eq("K13: the `go on` (readiness) finishes S0: exit 0", out.returncode, 0, out.stdout[-900:] + out.stderr[-400:])
        check_not_in("K13: no finding about the ticket (nothing was passed, nothing lost)", "ticket_incomplete", s0_findings(root))
        warnings = s0_pipeline(task_root)["warnings"]
        eq("K13 / t-957 F-6: the line is the FIRST of the story's warnings and names the headings looked for",
           warnings[0], "S0: ticket APP-1 has no section named Acceptance Criteria, What needs to be tested, AC; "
                        "the requirements are read from its description, comments, attachments and linked tickets")
        check("K13: and fits the 180 characters gate A cuts each warning at", len(warnings[0]) <= 180, str(len(warnings[0])))
        eq("K13: the snapshot is the tracker's, with no criteria", (snapshot_of(task_root)["acceptance_criteria"], snapshot_of(task_root)["provenance"]["source"]),
           ([], "fetched"))
        eq("K13: no agent, no conductor", stub_calls(root), [])
    finally:
        jira.stop()
        harness.cleanup(root)


def s0_list_applied_before_the_seed() -> None:
    """The tracker read of S0 seeds `work/source-inventory.json` (the `/field` ids and the prefix probes S1 reuses): that is no
    source collected. A list applied BEFORE the read (its record is on disk, the same bytes) must not meet the "too late"
    question at a later entry of S0 (after a readiness answer); a list the record does not hold still does."""
    jira = FakeJira(story_15045())
    root, task_root, env = rest_project(jira, git=False)             # no git: readiness stops S0 once, so there is a later entry
    try:
        listed = root / "list.txt"
        listed.write_text(f"testproject1-ui!1924 {EM} {DRAFT}\n", encoding="utf-8")
        out = s0_run(root, env, KEY, "--skip-sources", str(listed))
        eq("seed: the list is applied, the tracker is read (it seeds the inventory), readiness asks: exit 3",
           (out.returncode, s0_state(task_root).get("s0_block"), (task_root / "work" / "source-inventory.json").is_file(), _no_record(task_root)),
           (3, "readiness", True, False))
        out = s0_answer(root, env, KEY, "go on")
        eq("seed: at the next entry the list is NOT 'too late' (its record is the same bytes): S0 finishes, exit 0",
           (out.returncode, s0_state(task_root).get("s0_block")), (0, None), out.stdout[-900:])
        check_not_in("seed: and nothing says the sources were already collected", "were already collected", out.stdout)
        eq("seed: the record of the list is untouched", [e["as_written"] for e in _record(task_root)["exclusions"]], ["testproject1-ui!1924"])
    finally:
        jira.stop()
        harness.cleanup(root)
    jira = FakeJira(story_15045())
    root, task_root, env = rest_project(jira, git=False)
    try:
        listed = root / "list.txt"
        listed.write_text(f"testproject1-ui!1924 {EM} {DRAFT}\n", encoding="utf-8")
        s0_run(root, env, KEY, "--skip-sources", str(listed))
        listed.write_text(f"testproject1-ui!1881 {EM} another word\n", encoding="utf-8")       # other bytes than the record holds
        out = s0_answer(root, env, KEY, "go on")
        eq("seed negative: OTHER bytes than the record holds, with an inventory on disk, still ask 'too late': exit 3",
           (out.returncode, s0_state(task_root).get("s0_block")), (3, "source_list"), out.stdout[-900:])
        check_in("seed negative: in the same words as before", "were already collected on", s0_question(task_root))
    finally:
        jira.stop()
        harness.cleanup(root)


def k10_a_dry_run_asks_and_reads_nothing() -> None:
    """`--dry-run` skips S0 altogether, the question included, like every other S0 stop: it prints the S0 route and the
    tracker is not asked."""
    jira = FakeJira(story_15045())
    root, task_root, env = rest_project(jira)
    try:
        out = harness.run_script("story_run.py", "--project", str(root), "--task", KEY, "--dry-run", cwd=root, env=env)
        eq("dry run: exit 0", out.returncode, 0, out.stdout[-600:] + out.stderr[-400:])
        check_in("dry run: it names the REST read of S0 and that a failed read is asked, a lost login stops, no model is called",
                 "ticket_adapter get --raw-dir (the tracker by REST; a read that fails is asked of the person, a lost login stops the run, "
                 "no model is called; a dry run asks nothing and reads nothing)", out.stdout)
        eq("dry run: nothing was asked of the tracker, no question was written, nothing was called",
           (jira.log, (task_root / "state" / "driver-question.md").exists(), stub_calls(root)), ([], False, []))
        print("dry run prints: " + next(ln for ln in out.stdout.splitlines() if ln.startswith("pipeline.json is absent")))
    finally:
        jira.stop()
        harness.cleanup(root)


def s0_py_stdout_unit() -> None:
    import contextlib
    import io
    import tempfile
    import story_run
    check_eq = eq
    task = "QA-1"

    # D1(a) as a unit: stderr is printed and never part of what a caller writes to a file.
    root, task_root, env = s0_project(task)
    try:
        driver = driver_for(root, env, task)
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "noisy.py").write_text(
                "import sys\nprint('{\"key\": \"QA-1\"}')\nprint('WARN: probing the tracker', file=sys.stderr)\n",
                encoding="utf-8")
            driver.scripts = Path(tmp)
            printed = io.StringIO()
            with contextlib.redirect_stdout(printed):
                code, stdout, stderr = driver.py_stdout("noisy.py")
        check_eq("D1(a) py_stdout returns stdout alone", stdout, '{"key": "QA-1"}\n')
        check_in("D1(a) and stderr apart", "WARN: probing the tracker", stderr)
        check_in("D1(a) and prints the stderr line for the log", "WARN: probing the tracker", printed.getvalue())
        # exit 0 with something that is not one JSON object: a refusal that names the call and the
        # head of what it printed, and no snapshot - never a halt for the person.
        driver = driver_for(root, env, task)
        driver.py_stdout = lambda script, *a, **k: (0, "this is prose, not a ticket\n", "")
        try:
            driver.s0()
            check("D1(a) exit 0 with prose stdout refuses", False)
        except story_run.Refusal as refusal:
            check_in("D1(a) the refusal names the adapter call", "ticket_adapter get QA-1", refusal.text)
            check_in("D1(a) and the head of its stdout", "this is prose, not a ticket", refusal.text)
        except story_run.Person:
            check("D1(a) it is never a question for the person", False)
        check("D1(a) and no snapshot was written", not (task_root / "work" / "ticket-snapshot.json").exists())
    finally:
        harness.cleanup(root)


def s0_fenced_decision_notice() -> None:
    """t-278 (the coordinator's one-liner for t-271): a decision token inside a fenced block is ANNOUNCED at a question stop and never
    applied; the same token outside a fence is read as before, and a stop with no fence says nothing about one."""
    import contextlib
    import io
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        (task_root / "work").mkdir(parents=True, exist_ok=True)
        (task_root / "work" / "requirements-readiness.json").write_text(json.dumps({"verdict": "blocked", "open_questions": [
            {"id": "Q1", "question": "Which?", "severity": "major",
             "readings": [{"reading": "r0", "from": "description", "if_chosen": "x"}, {"reading": "r1", "from": "description", "if_chosen": "x"}]}]}),
            encoding="utf-8")
        driver = driver_for(root, env, task)
        driver.py = lambda script, *a, **k: (0, "")
        driver.unread = lambda *a, **k: "continue"       # FV1-3: words code could not read go to the conductor; this test judges what code prints
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            driver.take_question_answer("S3", "S3-qa-test-strategist-1", "```\nQ1: a\n```\n")
        out = printed.getvalue()
        check_in("fence: the decision inside the fenced block is announced, with the line", "S3: a decision inside a code block is not read: Q1: a", out)
        check_in("fence: and applied to nothing", "no question answered by a token", out)
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            driver.take_question_answer("S3", "S3-qa-test-strategist-1", "Q1: b\n")
        out = printed.getvalue()
        check_not_in("fence control: the same token outside a fence is read, and no notice is printed", "inside a code block", out)
        check_in("fence control: ... it is recorded", "recorded by code — Q1: b", out)
    finally:
        harness.cleanup(root)


def s0_legacy_snapshot() -> None:
    import contextlib
    import io
    check_eq = eq

    # --- (e) a story in flight with a legacy .md gets its .json once -----------------------------
    root, task_root, env = seed("QA-9")
    try:
        legacy = task_root / "work" / "ticket-snapshot.md"
        adapter_json = json.dumps({"key": "QA-9", "type": "Story", "status": "Open", "title": "Legacy",
                                   "description": "d", "acceptance_criteria": ["one"], "comments": [],
                                   "parent": None, "subtasks": [],
                                   "links": {"merge_request": None, "branch": None}}, indent=2)
        legacy.write_text(adapter_json + "\nWARN: the tail the old driver glued on\n", encoding="utf-8")
        out = s0_run(root, env, "QA-9")
        canon = task_root / "work" / "ticket-snapshot.json"
        check_eq("D1(e) a legacy .md holding JSON is taken: exit 0", out.returncode, 0, out.stdout[-800:] + out.stderr[-500:])
        check("D1(e) the .json exists and is the adapter's clean output", canon.is_file()
              and json.loads(canon.read_text(encoding="utf-8"))["title"] == "Legacy"
              and "WARN" not in canon.read_text(encoding="utf-8"))
        check_in("D1(e) one line says so", "ticket-snapshot.json", out.stdout)
        check("D1(e) the .md stays", legacy.is_file())
        before = (canon.read_bytes(), canon.stat().st_mtime_ns)
        out = s0_run(root, env, "QA-9")
        check_eq("D1(e) a second run leaves the .json as it was",
                 (canon.read_bytes(), canon.stat().st_mtime_ns), before)
        check_not_in("D1(e) and says nothing about it", "ticket-snapshot.json", out.stdout)
        # a markdown .md is converted the same way; a failed conversion is one line and writes nothing
        canon.unlink()
        legacy.write_text(FIXTURE_TICKET.replace("QA-1", "QA-9"), encoding="utf-8")
        driver = driver_for(root, env, "QA-9")
        driver.adopt_legacy_snapshot()
        check_eq("D1(e) a markdown .md is converted too", json.loads(canon.read_text(encoding="utf-8"))["key"], "QA-9")
        canon.unlink()
        driver.py_stdout = lambda script, *a, **k: (3, "", "no adapter")
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            driver.adopt_legacy_snapshot()
        check("D1(e) a failed conversion writes nothing", not canon.exists())
        check_eq("D1(e) and prints one line", len(printed.getvalue().strip().splitlines()), 1)
        check_in("D1(e) which says the brief will show it as not written", "not written yet", printed.getvalue())
        # no pipeline.json yet: this is S0's own business, not a legacy story
        fresh = task_root.parent / "QA-NEW"
        (fresh / "work").mkdir(parents=True)
        (fresh / "work" / "ticket-snapshot.md").write_text("x", encoding="utf-8")
        other = driver_for(root, env, "QA-NEW")
        other.adopt_legacy_snapshot()
        check("D1(e) a story with no pipeline.json is left to S0", not (fresh / "work" / "ticket-snapshot.json").exists())
    finally:
        harness.cleanup(root)


def s0_door_invariant() -> None:
    task = "QA-1"

    # --- the closed set: the S0 door is read only while S0 has no pipeline.json --------------------------
    root, task_root, env = seed(task)
    try:
        driver = driver_for(root, env, task)
        set_control(root, {"conductor": {"action": "continue", "did": "recorded", "text": "Recorded."}})
        for kind, stage in (("halt", "S0"), ("refusal", "S0")):
            driver.state["asked"] = {"kind": kind, "stage": stage, "dispatch": ""}
            driver.state["s0_block"] = "readiness"
            driver.save_state()
            (task_root / "state" / "driver-question.md").write_text("# q\nkind: halt\n", encoding="utf-8")
            answer = root / "a.md"
            answer.write_text("go on", encoding="utf-8")
            before = len(stub_calls(root))
            driver = driver_for(root, env, task)
            driver.take_answer(answer)
            # today's paths, unchanged: a halt goes to the conductor; a refusal at a stage that is
            # already done is recorded and the loop goes on
            old_way = len(stub_calls(root)) > before if kind == "halt" else len(stub_calls(root)) == before
            check(f"invariant: with pipeline.json present a `{kind}` at S0 goes the old way",
                  old_way and "S0" not in driver.state["pending_words"])
        driver.state.pop("s0_block", None)
        driver.state["asked"] = {"kind": "gate_A", "stage": "S0", "dispatch": ""}
        (task_root / "pipeline.json").unlink()
        driver.state["s0_block"] = "readiness"
        driver.save_state()
        (task_root / "state" / "driver-question.md").write_text("# q\nkind: gate_A\n", encoding="utf-8")
        driver = driver_for(root, env, task)
        driver.take_answer(answer)
        check("invariant: a gate kind never enters the S0 branch, even at S0 with no pipeline.json",
              "S0" not in driver.state["pending_words"])
    finally:
        harness.cleanup(root)


def s0_stale_block() -> None:
    """A block open at one entry must not capture the answer to a LATER stop at S0 (critic t-028).
    RUN1 stops on the incomplete ticket; the person mends the file; RUN2 (no answer) stops on a halt
    that is none of the five blocks; RUN3 answers THAT halt. The answer must take the old conductor
    route and must not be journalled against the ticket block.

    Since t-017 D2 the stand probe no longer halts S0, which is what RUN2 used to meet - so the
    unrelated halt is raised here, in this process, out of the ticket read. An in-process scenario:
    it runs after the pool (a Driver changes the working directory)."""
    import story_run
    task = "QA-1"
    root, task_root, env = s0_project(task, config={"environments": [{"name": "Local"}]})
    try:
        bad = root / "incomplete-ticket.md"
        bad.write_text(LOST_READ_TICKET, encoding="utf-8")
        out = s0_run(root, env, task, "--ticket-file", str(bad))
        eq("stale block: RUN1 asks about the incomplete ticket", (out.returncode, s0_state(task_root).get("s0_block")),
           (3, "ticket_incomplete"), out.stdout[-500:])
        bad.write_text(FIXTURE_TICKET, encoding="utf-8")
        driver = driver_for(root, env, task, max_boundaries=0)

        def unrelated(*_args, **_kwargs):
            raise story_run.Person("halt", "Something at the start of the story stopped it, and it is none "
                                   "of the questions S0 keeps a door for. What should happen next?", "S0")
        driver.ticket_get = unrelated
        eq("stale block: RUN2 (no answer) meets the unrelated halt", driver.run(), 3)
        state = s0_state(task_root)
        check("stale block: no S0 block is open any more", not state.get("s0_block") and not state.get("s0_ask"),
              str(state.get("s0_block")))
        set_control(root, {"conductor": {"action": "continue", "did": "read it", "text": "Read."}})
        answer = root / "answer.md"
        answer.write_text("the stand is fine, use Local anyway", encoding="utf-8")
        driver = driver_for(root, env, task, answer=str(answer), max_boundaries=0)
        driver.run()
        eq("stale block: RUN3 goes to the conductor (old route)", [c["kind"] for c in stub_calls(root)], ["conductor"])
        check("stale block: the journal does not say ticket_incomplete",
              not any("ticket_incomplete" in str(e.get("notes")) for e in s0_journal(root)), str(s0_journal(root))[-400:])
        check("stale block: the incomplete-ticket question is not shown again",
              not (task_root / "state" / "driver-question.md").exists()
              or "incomplete" not in s0_question(task_root))
    finally:
        harness.cleanup(root)


def main() -> None:
    run_scenarios(
        [
        s0_snapshot,
        s0_incomplete_ticket,
        s0_two_passes,
        s0_pasted_ticket,
        s0_reask_battery,
        s0_launch_flags,
        k5_the_agent_is_never_called,
        k6_ticket_read_question,
        k_comparison_person_vs_tracker,
        k11_a_snapshot_on_disk_is_never_rewritten,
        k13_no_criteria_section_goes_on_with_a_line,
        k10_a_dry_run_asks_and_reads_nothing,
        s0_list_applied_before_the_seed,
    ],
        [
        s0_py_stdout_unit,
        s0_ticket_units,
        k6_retry_after_and_other_failures,
        s0_fenced_decision_notice,
        s0_legacy_snapshot,
        s0_door_invariant,
        s0_stale_block,
    ],
    )
    harness.finish("test_story_run_s0_snapshot")


# split: runner piece 1
if __name__ == "__main__":
    main()
