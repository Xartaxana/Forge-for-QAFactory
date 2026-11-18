"""paste owners: a part of test_story_run_s0.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_run_s0_common."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_in, check_not_in  # noqa: E402
from story_run_common import FIXTURE_TICKET, INCOMPLETE_TICKET, LOST_READ_TICKET, driver_for, eq, rules_broken, s0_answer, s0_findings, s0_journal, s0_pipeline, s0_project, s0_question, s0_run, s0_state, stub_calls, run_scenarios
from story_run_s0_common import RAW_15045, price_broken, snapshot_of  # noqa: E402


# --- t-281: the paste leg (F1, F2, F4, F5) and the owners of a failed read (F3) ----------------------------------------
BROWSER_COPY = ("Items can carry tags\n\nAs a warehouse operator I want tags (see QA-77).\n\nAcceptance criteria\n\n"
                "- A tag can be added to an item.\n- A tag can be removed from an item.\n")


def s0_title_question() -> None:
    """K-F2 (FV1-11): a text with NO `# ` line (what a browser copy is) is not a stop: the adapter takes the first line as the
    title and the driver keeps it without a question, as the line "title taken from the first line" of the story's
    record and a finding filed once; a rerun is silent."""
    task = "QA-1"
    root, task_root, env = s0_project(task, git=False)          # no git: readiness stops S0 once, so there is a rerun
    try:
        browser = root / "browser-copy.md"
        browser.write_bytes(BROWSER_COPY.encode("utf-8"))
        out = s0_run(root, env, task, "--ticket-file", str(browser))
        eq("K-F2: a text with no `# ` line is NOT stopped on the title: the first stop is readiness (no git here), exit 3",
           (out.returncode, s0_state(task_root).get("s0_block"), "carries no title" in out.stdout), (3, "readiness", False), out.stdout[-900:])
        snapshot = snapshot_of(task_root)
        eq("K-F2: the snapshot has the first line as its title, `title_from` first_line, and the 2 criteria of the paste (read by the same parser)",
           (snapshot["title"], snapshot["provenance"].get("title_from"), snapshot["acceptance_criteria"]),
           ("Items can carry tags", "first_line", ["A tag can be added to an item.", "A tag can be removed from an item."]))
        out = s0_answer(root, env, task, "go on")
        eq("K-F2: the rerun after the readiness answer finishes and does not ask about the title: exit 0", out.returncode, 0, out.stdout[-900:] + out.stderr[-400:])
        passes = [w for w in s0_pipeline(task_root)["warnings"] if "title taken from the first line" in w]
        check_in("K-F2: the taking is a line of the story's record, once, with the taken title quoted",
                 'S0: the ticket-title check: title taken from the first line (kept without asking): "Items can carry tags"', passes)
        eq("K-F2: the line is there once", len(passes), 1)
        eq("K-F2: and filed once as a finding (FR-4)", s0_findings(root).count("idempotency:s0-pass:QA-1:ticket_title"), 1)
        eq("K-F2: no conductor", stub_calls(root), [])
    finally:
        harness.cleanup(root)


def fv111_title_taken_without_a_question() -> None:
    """FV1-11, one parameterised case at the unit (`s0_criteria`): a title the reader took from the first line is kept
    without a stop; no title at all, the key as the title and an empty text keep the `ticket_no_title` halt; a title
    with another problem (the criteria gap) still stops for THAT problem; a `ticket_title` question stored before the
    change and answered `go on` is accepted as it was."""
    import story_run
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        driver = driver_for(root, env, task)
        first_line = {"source": "person_pasted", "title_from": "first_line"}
        head = "S0: the ticket-title check: title taken from the first line (kept without asking)"
        room = driver.S0_LINE_LIMIT - len(head) - len(': ""')     # 95: the title fits whole up to here
        cut = chr(0x2026)
        rows = (
            # id, ticket, expected (kind, block), the story-record line the taken pass reads as (None: not taken)
            ("FIRST-LINE-TITLE", {"title": "Items can carry tags", "acceptance_criteria": ["a"], "provenance": first_line}, ("line", None),
             head + ': "Items can carry tags"'),
            ("TITLE-AT-THE-LIMIT", {"title": "T" * room, "acceptance_criteria": ["a"], "provenance": first_line}, ("line", None),
             head + ': "' + "T" * room + '"'),
            ("TITLE-BEYOND-THE-LIMIT", {"title": "T" * (room + 1), "acceptance_criteria": ["a"], "provenance": first_line}, ("line", None),
             head + ': "' + "T" * (room - 1) + cut + '"'),
            ("TITLE-LONG-NON-ASCII", {"title": "T" * 200 + " é中", "acceptance_criteria": ["a"], "provenance": first_line}, ("line", None),
             head + ': "' + "T" * (room - 1) + cut + '"'),
            ("TITLE-NON-ASCII", {"title": "Café 中文 tags", "acceptance_criteria": ["a"], "provenance": first_line}, ("line", None),
             head + ': "Café 中文 tags"'),
            ("TITLE-WITH-A-DOUBLE-QUOTE", {"title": 'Say "hi" to tags', "acceptance_criteria": ["a"], "provenance": first_line}, ("line", None),
             head + ': "Say "hi" to tags"'),
            ("TITLE-WITH-WHITESPACE", {"title": "Items\tcan\x07 carry   tags", "acceptance_criteria": ["a"], "provenance": first_line}, ("line", None),
             head + ': "Items can\x07 carry tags"'),
            ("TITLE-PLUS-OTHER-PROBLEM", {"title": "Acceptance criteria", "description": "prose under the heading", "acceptance_criteria": [],
                                          "provenance": first_line}, ("stop", "ticket_incomplete"), head + ': "Acceptance criteria"'),
            ("NO-TITLE", {"title": "", "acceptance_criteria": ["a"], "provenance": {"source": "person_pasted"}}, ("stop", "ticket_no_title"), None),
            ("NO-TITLE-FROM-FIRST-LINE", {"title": "", "acceptance_criteria": ["a"], "provenance": first_line}, ("stop", "ticket_no_title"), None),
            ("KEY-AS-TITLE", {"title": task, "acceptance_criteria": ["a"], "provenance": first_line}, ("stop", "ticket_no_title"), None),
        )
        for name, ticket, expected, phrase in rows:
            driver.state.pop("s0_block", None)
            driver.state.pop("s0_passes", None)
            driver._s0_passed = []
            try:
                driver.s0_criteria(ticket, "through the tracker")
                got = ("line", None)
            except story_run.Person:
                got = ("stop", driver.state.get("s0_block"))
            eq(f"FV1-11 {name}: what the check raised", got, expected)
            kept = (driver.state.get("s0_passes") or {}).get("ticket_title") or {}
            eq(f"FV1-11 {name}: the taken line is in the story record exactly when it was taken",
               (kept.get("words") == driver.S0_TAKEN_WORDS, [driver.s0_pass_phrase(b, w) for b, w in driver._s0_passed if b == "ticket_title"]),
               (phrase is not None, [phrase] if phrase else []))
            eq(f"FV1-11 {name}: the line is one line inside the limit",
               all(len(p) <= driver.S0_LINE_LIMIT and "\n" not in p for p in [driver.s0_pass_phrase(b, w) for b, w in driver._s0_passed]), True)
        # RESUME-OLD-QUESTION: a stop stored before the change, answered `go on` after it
        driver.state.pop("s0_passes", None)
        driver._s0_passed = []
        driver.state.update(s0_block="ticket_title", pending_words={"S0": "go on"},
                            s0_ask={"kind": "halt", "text": "old question", "doors": {"retry": "retry", "go on": "go on"},
                                    "problems": ["title taken from the first line"], "paste": True})
        driver.s0_read_word()
        eq("FV1-11 RESUME-OLD-QUESTION: `go on` to the stored question is a pass with the person's words",
           ((driver.state.get("s0_passes") or {}).get("ticket_title") or {}).get("words"), "go on")
        driver.state.pop("s0_passes", None)
        driver.state.update(s0_block="ticket_title", pending_words={"S0": "retry"},
                            s0_ask={"kind": "halt", "text": "old question", "doors": {"retry": "retry", "go on": "go on"},
                                    "problems": ["title taken from the first line"], "paste": True})
        driver.s0_read_word()
        eq("FV1-11 RESUME-OLD-QUESTION: `retry` to the stored question records no pass and leaves no block",
           ("ticket_title" in (driver.state.get("s0_passes") or {}), driver.state.get("s0_block")), (False, None))
        driver.state.update(s0_passes={"ticket_title": {"words": "go on", "at": "x", "problems": ["title taken from the first line"], "witness": "w"}})
        driver._s0_passed = []
        driver.s0_criteria({"title": "Items can carry tags", "acceptance_criteria": ["a"], "provenance": first_line}, "through the tracker")
        eq("FV1-11 RESUME-OLD-QUESTION: the check takes that pass (not overwritten by the factory's) and reads it as the person's word",
           [driver.s0_pass_phrase(b, w) for b, w in driver._s0_passed],
           ["S0: the ticket-title check passed by the person's word: \"go on\""])
        # a pass the factory took BEFORE the title was stored with it (temporal): the phrase reads without the quote, never "None"
        driver.state.update(s0_passes={"ticket_title": {"words": driver.S0_TAKEN_WORDS, "at": "x", "problems": ["title taken from the first line"], "witness": "w"}})
        eq("FV1-11 STORED-TAKEN-PASS-WITHOUT-TITLE: the phrase is printed without the quote",
           driver.s0_pass_phrase("ticket_title", driver.S0_TAKEN_WORDS), "S0: the ticket-title check: title taken from the first line (kept without asking)")
        eq("FV1-11 PERSON-WORDS: the print of the person's own words is as before (unquoted, and the record line quotes them)",
           (driver.s0_pass_phrase("ticket_title", "go on", quoted_words=False), driver.s0_pass_phrase("ticket_title", "go on")),
           ("S0: the ticket-title check passed by the person's word", "S0: the ticket-title check passed by the person's word: \"go on\""))
    finally:
        harness.cleanup(root)


def s0_pasted_description_15045() -> None:
    """K-F1 through the driver: the real 15045 description pasted as the answer of the incomplete-ticket question gives its
    15 criteria (item 1 and 15 verbatim) - the same parser as the tracker's description. A heading-less paste stays 0."""
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        bad = root / "incomplete-ticket.md"
        bad.write_text(LOST_READ_TICKET, encoding="utf-8")
        s0_run(root, env, task, "--ticket-file", str(bad))
        issue = json.loads(RAW_15045.decode("utf-8"))["fields"]
        out = s0_answer(root, env, task, "# " + issue["summary"] + "\n\n" + issue["description"], "--ticket-file", str(bad))
        eq("K-F1: the 15045 description pasted as the answer: S0 finishes, exit 0 (the criteria are found, so there is no question)", out.returncode, 0, out.stdout[-900:] + out.stderr[-400:])
        snapshot = snapshot_of(task_root)
        items = snapshot["acceptance_criteria"]
        eq("K-F1: 15 criteria, item 1 and item 15 verbatim, `person_pasted`", (len(items), items[0], items[-1], snapshot["provenance"]["source"]),
           (15, "Visual revision diff opens from workflow version history.", "Existing workflow versioning/text diff behavior is not regressed.", "person_pasted"))
        check("K-F1: no glue of the next section into item 15", "QA Factory evaluation goals" not in items[-1])
    finally:
        harness.cleanup(root)
    root, task_root, env = s0_project(task)
    try:
        bad = root / "incomplete-ticket.md"
        bad.write_text(LOST_READ_TICKET, encoding="utf-8")
        s0_run(root, env, task, "--ticket-file", str(bad))
        out = s0_answer(root, env, task, "# A title\n\nA story.\n\n- one\n- two\n", "--ticket-file", str(bad))
        eq("K-F1n / D-0050: a heading-less paste has no criteria section: S0 goes on, no question (the lost-read ticket asked first; the paste answers it)",
           (out.returncode, s0_state(task_root).get("s0_block")), (0, None), out.stdout[-600:])
        check_in("K-F1n: and the story's first line says no section was found", "S0: ticket QA-1 has no section named", s0_pipeline(task_root)["warnings"][0])
    finally:
        harness.cleanup(root)


def s0_ticket_file_precedence() -> None:
    """K-F2c: a `--ticket-file` on the command line that is NEWER than the stored paste wins; the stored paste wins when the
    command line carries none (or only the flag it was answered under)."""
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        bad = root / "incomplete-ticket.md"
        bad.write_text(LOST_READ_TICKET, encoding="utf-8")
        newer = root / "newer.md"
        newer.write_text(FIXTURE_TICKET.replace("Items can carry tags", "Items carry tags (the newer file)"), encoding="utf-8")
        s0_run(root, env, task, "--ticket-file", str(bad))
        out = s0_answer(root, env, task, "# A pasted title\n\n## Acceptance criteria\n\nNo criteria in what I typed.\n", "--ticket-file", str(bad))
        eq("K-F2c setup: the paste (with the launch flag repeated beside it) is the ticket now; it has no criteria, so the same block asks again",
           (out.returncode, s0_state(task_root).get("s0_block"), (s0_state(task_root).get("s0_answers") or {}).get("ticket_file_cli")), (3, "ticket_incomplete", str(bad)))
        eq("t-287 item 6 (end to end): that entry said ONCE that the stored paste is read, with its file and the door that replaces it",
           out.stdout.count("reading the ticket text you gave earlier (qa-factory/artifacts/QA-1/state/driver-tmp/ticket-QA-1.md); give a different --ticket-file to replace it"), 1, out.stdout[-900:])
        out = s0_run(root, env, task, "--ticket-file", str(newer))
        check_not_in("t-287 item 6 (end to end): a NEW flag is the newer word and the line is not said", "reading the ticket text you gave earlier", out.stdout)
        eq("K-F2c: a NEW `--ticket-file` on the command line wins over the stored paste: S0 finishes with the newer file's ticket",
           (out.returncode, snapshot_of(task_root)["title"]), (0, "Items carry tags (the newer file)"), out.stdout[-900:] + out.stderr[-400:])
    finally:
        harness.cleanup(root)
    root, task_root, env = s0_project(task)
    try:
        bad = root / "incomplete-ticket.md"
        bad.write_text(LOST_READ_TICKET, encoding="utf-8")
        s0_run(root, env, task, "--ticket-file", str(bad))
        pasted = FIXTURE_TICKET.replace("Items can carry tags", "Items carry tags (typed)")
        out = s0_answer(root, env, task, pasted)
        eq("K-F2c: the stored paste wins when the command line carries no flag: S0 finishes with the paste's ticket",
           (out.returncode, snapshot_of(task_root)["title"]), (0, "Items carry tags (typed)"), out.stdout[-900:] + out.stderr[-400:])
    finally:
        harness.cleanup(root)


def s0_paste_only_references() -> None:
    """K-F4, the paste-only leg end to end: no tracker is set up, the person's text is scanned and `work/ticket-references.json`
    says which leg wrote it; no reference in the text is an empty list, recorded."""
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        paste = root / "with-refs.md"
        paste.write_text(FIXTURE_TICKET.replace("As a warehouse operator", "As a warehouse operator (see QA-77)", 1), encoding="utf-8")
        out = s0_run(root, env, task, "--ticket-file", str(paste))
        eq("K-F4: a paste with no tracker beside it: S0 finishes, exit 0", out.returncode, 0, out.stdout[-900:] + out.stderr[-400:])
        references = json.loads((task_root / "work" / "ticket-references.json").read_text(encoding="utf-8"))
        tickets = {r["ref"]: r for r in references["rows"] if r["kind"] == "ticket"}
        eq("K-F4: written_by [S0]; the mentioned key is a ticket row `unproven` with the reason; every ticket row says so",
           (references["written_by"], tickets["QA-77"]["status"], tickets["QA-77"]["reason"], {r["status"] for r in tickets.values()}),
           (["S0"], "unproven", "no tracker read at S0", {"unproven"}), json.dumps(references)[:600])
        eq("K-F4: the key stands once, with the origin of the person's text", (len([r for r in references["rows"] if r["ref"] == "QA-77"]), "mention:description" in tickets["QA-77"]["origins"]), (1, True))
    finally:
        harness.cleanup(root)
    root, task_root, env = s0_project(task)
    try:
        plain = root / "plain.md"
        plain.write_text("# A title\n\nA story that points at nothing.\n\n## Acceptance criteria\n\n1. It works.\n", encoding="utf-8")
        out = s0_run(root, env, task, "--ticket-file", str(plain))
        references = json.loads((task_root / "work" / "ticket-references.json").read_text(encoding="utf-8"))
        eq("K-F4 / FR-23: nothing referenced is still a recorded result: the file is there with an empty list", (out.returncode, references["rows"]), (0, []))
    finally:
        harness.cleanup(root)


def _run_adapter_in_process(root: Path, *args) -> tuple:
    """`ticket_adapter.main()` in this process, over `root`: (exit code, stdout, stderr) - the way the driver sees a child."""
    import contextlib
    import io
    import ticket_adapter
    harness.use_project(root)
    out, err = io.StringIO(), io.StringIO()
    saved = sys.argv
    sys.argv = ["ticket_adapter.py", *[str(a) for a in args]]
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = ticket_adapter.main()
    finally:
        sys.argv = saved
    return code, out.getvalue(), err.getvalue()


def s0_owners_of_a_failed_read() -> None:
    """K-F3 at the driver: exit 4 (the factory's) is a REFUSAL naming the file and never a question; exit 3 (the tracker's) is
    the `ticket_read` question with `retry_at` from the error object; exit 5 is the stop; a `--json` call whose stdout is not an
    object is the factory's too. K-F4: one place builds the raw flags for the REST read, the comparison read and the paste read."""
    import contextlib
    import io
    import story_run
    import ticket_light
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        driver = driver_for(root, env, task)
        direct = {"base_url": "https://jira.example.test", "auth_type": "basic_token", "username_ref": "QA_JIRA_EMAIL", "secret_ref": "QA_JIRA_API_TOKEN"}
        driver.config["adapters"] = {"ticket": {"kind": "jira", "method": "agent", "invoke": "jira-assistant", "direct_api": direct}}
        # the REAL adapter, over a corrupted COPY of jira-fields.json under this test's tmp dir (never the package's file)
        bad = root / "jira-fields.json"
        bad.write_text(json.dumps(dict(ticket_light.load_fields_table(), standard=[])), encoding="utf-8")
        saved = ticket_light.FIELDS_TABLE_PATH
        ticket_light.FIELDS_TABLE_PATH = bad
        try:
            code, out, err = _run_adapter_in_process(root, "get", task, "--json")
        finally:
            ticket_light.FIELDS_TABLE_PATH = saved
        eq("K-F3 setup: the adapter exits 4 over the corrupted copy and prints ONE error object", (code, json.loads(out)["owner"], json.loads(out)["file"]), (4, "factory", "jira-fields.json"))
        driver.py_stdout = lambda *a, **k: (code, out, err)
        try:
            driver.s0_rest_read()
            check("K-F3: exit 4 is a refusal", False)
        except story_run.Refusal as refusal:
            check("K-F3: exit 4 -> a Refusal that names `jira-fields.json`, says it is the factory's own and what is expected (FR-1, FR-3)",
                  "`jira-fields.json`" in refusal.text and "the cause is the factory's own" in refusal.text and "Expected:" in refusal.text, refusal.text)
        except story_run.Person:
            check("K-F3: exit 4 is never a question", False)
        check("K-F3: no question was left open and nothing was written", not driver.state.get("s0_block") and not (task_root / "work" / "ticket-snapshot.json").exists())
        # an adapter that printed no object under --json: the factory's, with its message - never a question
        for said in ("", "<html>an old adapter's prose</html>", "[1, 2]"):
            driver.py_stdout = lambda *a, said=said, **k: (3, said, "ticket_adapter: something went wrong")
            try:
                driver.s0_rest_read()
                check("K-F3: no error object -> a refusal", False)
            except story_run.Refusal as refusal:
                check_in(f"K-F3: stdout {said[:20]!r} under --json -> the exit-4 handling with the message `the adapter printed no error object`",
                         "the adapter printed no error object", refusal.text)
            except story_run.Person:
                check("K-F3: no error object is never a question", False)
        # the tracker's: the question, the time from the OBJECT (the sentence on stderr names another time on purpose)
        tracker = json.dumps({"ok": False, "owner": "tracker", "status": 429, "retry_at": "2026-10-01T12:30:00Z", "message": "the tracker could not be read"})
        driver.py_stdout = lambda *a, **k: (3, tracker, "ticket_adapter: the tracker asked to be tried again at 2026-10-01T09:00:00Z - retry")
        try:
            driver.s0_rest_read()
            check("K-F3: exit 3 is the question", False)
        except story_run.Person as person:
            check_in("K-F3: exit 3 -> the `ticket_read` question with the time read from the object", "it asked to be asked again at 2026-10-01T12:30:00Z.", person.text)
            check_not_in("K-F3: and not the time that stood in the sentence", "09:00:00Z", person.text)
            eq("K-F3: the block is `ticket_read`", driver.state.get("s0_block"), "ticket_read")
        # auth: the `ticket_auth` question (C1-3 F3 a), with or without the object - never an InfraStop
        auth = json.dumps({"ok": False, "owner": "auth", "status": 401, "retry_at": None, "message": "Jira stopped accepting the token"})
        for stdout in (auth, ""):
            driver.state.pop("s0_block", None)
            driver.py_stdout = lambda *a, stdout=stdout, **k: (5, stdout, "ticket_adapter: Jira stopped accepting the token (HTTP 401)")
            printed = io.StringIO()
            try:
                with contextlib.redirect_stdout(printed):
                    driver.s0_rest_read()
                check("K-F3: exit 5 asks the `ticket_auth` question", False)
            except story_run.InfraStop:
                check("K-F3: exit 5 is no longer an infrastructure stop", False)
            except story_run.Person as person:
                eq(f"K-F3: exit 5 (object {'present' if stdout else 'absent'}) -> the `ticket_auth` question (halt, exit 3), the door in the answer block",
                   ((person.kind, person.code), driver.state.get("s0_block"), "QA_JIRA_API_TOKEN" in person.answer_note), (("halt", 3), "ticket_auth", True))
        # the comparison leg: the factory's fault is REPORTED in the one line and the person's text goes on (C6)
        driver.state.pop("s0_block", None)
        driver.state.pop("s0_rest_failed", None)          # the `ticket_read` question above remembered a failure; the comparison would skip its read
        factory = json.dumps({"ok": False, "owner": "factory", "status": None, "retry_at": None, "message": "refused - jira-fields.json: key `standard` is empty", "file": "jira-fields.json"})
        driver.py_stdout = lambda *a, **k: (4, factory, "ticket_adapter: refused - jira-fields.json: key `standard` is empty")
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            kept = driver.s0_compare({"key": task, "title": "T", "acceptance_criteria": ["x"]}, "the snapshot's text")
        eq("K-F3 / C6: a factory fault on the comparison leg is ONE line naming the file, the story goes on with the person's text, nothing asked",
           (kept, printed.getvalue().count("\n"), "`jira-fields.json`" in printed.getvalue(), bool(driver.state.get("s0_block"))), ("the snapshot's text", 1, True, False))

        # --- K-F4: ONE place builds the raw flags; the REST read, the comparison read and the paste read pass the same ---
        calls = []
        snap = {"key": task, "title": "T", "description": "d", "acceptance_criteria": ["x"], "comments": [], "parent": None, "subtasks": [],
                "links": {"merge_request": None, "branch": None}, "provenance": {"source": "fetched"}}

        def record(script, *args, **kw):
            calls.append([str(a) for a in args])
            return 0, json.dumps(snap), ""
        driver.py_stdout = record
        driver.state.pop("s0_block", None)
        driver.s0_rest_read()
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            driver.s0_ticket("a-paste.md")
        flags = driver.s0_raw_flags()
        rest_call, paste_call, compare_call = calls[0], calls[1], calls[2]
        eq("K-F4: the REST leg's flags are the raw-dir flags of the one builder", rest_call, ["get", task, *flags, "--json"])
        eq("K-F4: the comparison leg's flags ARE the REST leg's flags (one builder function)", compare_call, rest_call)
        eq("K-F4: and the paste read names the same folder beside --ticket-file", paste_call, ["get", task, "--ticket-file", "a-paste.md", *flags, "--json"])
        check("K-F4: the folder is the story's work/ticket-raw",
              flags[0] == "--raw-dir" and Path(flags[1]).resolve() == (task_root / "work" / "ticket-raw").resolve(), str(flags))
        # K-F10: the source check that the driver calls the public name of the adapter's check was a source pin: deleted by TD-11 phase 0 (F3)
        eq("K-F10: and the check still answers through the driver", driver.direct_api_usable(), True)
    finally:
        harness.cleanup(root)


def t287_config_owner_is_the_ticket_read_question() -> None:
    """t-287 item 2 at the driver: the adapter's error object with owner `config` (a recorded `direct_api` that lacks keys) is
    the `ticket_read` question with FR-50's three answers and the adapter's sentence VERBATIM (FR-8) - never the factory's
    refusal ("Restore what the message names"), never the network advice."""
    import story_run
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        cfg_path = root / "qa-factory" / "config.json"
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        cfg["adapters"] = {"ticket": {"kind": "jira", "method": "api", "direct_api": {"custom_fields": [], "acceptance_headings": []}}}
        cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
        code, out, err = _run_adapter_in_process(root, "get", task, "--json")      # the REAL adapter over the stub
        obj = json.loads(out)
        eq("item 2 setup: the real adapter over the template stub: exit 3, owner `config`", (code, obj["owner"]), (3, "config"))
        driver = driver_for(root, env, task)
        driver.config["adapters"] = cfg["adapters"]
        driver.py_stdout = lambda *a, **k: (code, out, err)
        asked = None
        try:
            driver.s0_rest_read()
            got = ("returned", "")
        except story_run.Person as person:
            got = ("Person", person.text)
            asked = person
        except story_run.Refusal as refusal:
            got = ("Refusal", refusal.text)
        eq("item 2: owner `config` is a QUESTION (never the factory's refusal): the `ticket_read` block", (got[0], driver.state.get("s0_block")), ("Person", "ticket_read"))
        text = got[1]
        # t-363 B3 (B-256 g): the adapter's sentence - the key names and the onboarding command - is an instruction, so it
        # stands in the answer block, WHOLE (FR-8); the body says "the setting named below" and carries neither.
        keys = [f"adapters.ticket.direct_api.{k}" for k in ("base_url", "auth_type", "secret_ref", "username_ref")]
        check("B3: the body carries no key path and no plugin command, and says where the setting is named",
              not any(k in text for k in keys) and "/qa-factory:" not in text and "adapters." not in text
              and "the setting named below" in text and "named above" not in text, text)
        check("B3: the answer block carries the adapter's sentence WHOLE: every missing key and the onboarding door",
              obj["message"] in " ".join(asked.answer_note.split()) and all(k in asked.answer_note for k in keys)
              and "/qa-factory:qa-onboarding" in asked.answer_note, asked.answer_note)
        import human_text
        from story_run_common import jsonl
        driver.ask(asked)
        full = driver.question_path().read_text(encoding="utf-8")
        check("B3: in the question file the keys stand below the answer marker, not above it",
              all(k in full.split("Answer: write your words")[1] for k in keys)
              and not any(k in full.split("Answer: write your words")[0] for k in keys), full)
        eq("B3: the whole question as the person reads it passes the text rules (the block aside, the body clean)",
           human_text.problems(full), [])
        eq("B3: ...and the driver's own judgement of it recorded no broken rule",
           [r.get("problems") for r in jsonl(task_root / "state" / "driver-questions.jsonl")][-1:], [[]])
        eq("B3 control: the OLD body (the adapter's sentence pasted above the block) breaks the new rules",
           sorted({p["rule"] for p in human_text.problems("What stands in the way: " + obj["message"] + " " + "x" * 80 + "\n---\nAnswer: write your words to a file and run\n  python story_run.py --task QA-1 --answer <file>\n")}),
           ["config_key", "plugin_command"])
        driver.state["asked"] = {}
        driver.question_path().unlink()
        check("item 2: FR-50's three answers stay: `not needed`, fix and `retry`, or the ticket as text",
              all(part in text for part in ("(a) `not needed` — ", "(b) `retry` — record the setting named below for this project","(c) paste the ticket here as text")), text)
        check("item 2: and it does not send the person to the network or the VPN, nor say 'Restore'",
              "VPN" not in text and "network" not in text and "Restore" not in text, text)
        eq("item 2: the text obeys human-questions.md (the block `ask()` appends under it aside)", [r for r in rules_broken(text) if r != "no_how_to_answer"], [])
        eq("item 2: the question takes a paste (the door of answer (c))", driver.state["s0_ask"]["paste"], True)
        eq("item 2: no snapshot was written", (task_root / "work" / "ticket-snapshot.json").exists(), False)
        # control of the same call: a tracker-owned failure is the same question WITHOUT that sentence
        driver.state.pop("s0_block", None)
        tracker = json.dumps({"ok": False, "owner": "tracker", "status": 503, "retry_at": None, "message": "the tracker could not be read"})
        driver.py_stdout = lambda *a, **k: (3, tracker, "ticket_adapter: the tracker could not be read")
        try:
            driver.s0_rest_read()
            other = ""
        except story_run.Person as person:
            other = person.text
        check("item 2 (control): an exit-3 `tracker` object is the same question without the config sentence", "What stands in the way" not in other and "ticket_read" == driver.state.get("s0_block"), other)
    finally:
        harness.cleanup(root)


def t287_texts_name_the_file_read() -> None:
    """t-287 item 6 (and the wiki leg of item 1) at the driver: the title and the no-criteria questions name the file actually
    read, relative to the project; a stored paste that wins over the same flag says so once on entry; a wiki text
    has its own title question (`# ` is a list item there); an older snapshot with no `markup` is read as markdown."""
    import contextlib
    import io
    import story_run
    task = "QA-1"
    stored = "qa-factory/artifacts/QA-1/state/driver-tmp/ticket-QA-1.md"
    root, task_root, env = s0_project(task)
    try:
        driver = driver_for(root, env, task)
        driver._s0_passed = []                       # `s0()` makes it at its start; the taken title appends to it
        # --- the texts, at the unit: file named / not named; markdown / wiki / older snapshot ---
        def ask_of(ticket, file, how="from the ticket file"):
            try:
                driver.s0_criteria(ticket, how, file)
            except story_run.Person as person:
                return person.text
            return ""
        driver.state.pop("s0_block", None)
        titled = {"title": "Items can carry tags", "acceptance_criteria": ["a"], "provenance": {"source": "person_pasted", "title_from": "first_line"}}
        eq("item 6 (FV1-11): a title taken from the first line asks nothing, with or without a file named (the title question is gone)",
           (ask_of(titled, stored), ask_of(titled, None)), ("", ""))
        driver.state.pop("s0_block", None)
        wiki = {"title": "Items can carry tags", "acceptance_criteria": ["a"], "provenance": {"source": "person_pasted", "title_from": "first_line", "markup": "wiki"}}
        eq("item 1 (wiki, FV1-11): a wiki text's first-line title asks nothing either", ask_of(wiki, stored), "")
        driver.state.pop("s0_block", None)
        lost = "## Acceptance criteria\n\nThe operator can tag an item."
        text = ask_of({"title": "T", "description": lost, "acceptance_criteria": [], "provenance": {"source": "person_pasted"}}, stored)
        check("item 6: the lost-read question says it read THAT file (D-0050: no `retry`, so no 'add it to the file')",
              f"from the ticket file `{stored}`" in text and "add the criteria to" not in text and "`retry`" not in text, text)
        eq("item 6: ... and obeys human-questions.md", [r for r in rules_broken(text) if r != "no_how_to_answer"], [])
        driver.state.pop("s0_block", None)
        text = ask_of({"title": "T", "description": lost, "acceptance_criteria": [], "provenance": {"source": "fetched"}}, None, "through the tracker")
        check("item 6 (control): a ticket read through the tracker names no file", "I read ticket QA-1 through the tracker and" in text and "`qa-factory/artifacts" not in text, text)
        # --- the line on entry, at the unit ---
        def entry_line(cli, stored_cli, answered="/p/paste.md"):
            driver.state["launch"] = {"ticket_file": "/p/orig.md"}
            driver.state["s0_answers"] = {"ticket_file": answered, **({"ticket_file_cli": stored_cli} if stored_cli is not None else {})}
            driver.flags.ticket_file = cli
            printed = io.StringIO()
            with contextlib.redirect_stdout(printed):
                chosen = driver.s0_flags()["ticket_file"]
            return chosen, printed.getvalue()
        chosen, said = entry_line("/p/orig.md", "/p/orig.md")
        eq("item 6: the stored paste wins over the SAME flag repeated: ONE line names the file and the door",
           (chosen, said), ("/p/paste.md", "reading the ticket text you gave earlier (/p/paste.md); give a different --ticket-file to replace it\n"))
        chosen, said = entry_line(None, "/p/orig.md")
        eq("item 6: no flag on the command line -> the paste is read and nothing is said", (chosen, said), ("/p/paste.md", ""))
        chosen, said = entry_line("/p/new.md", "/p/orig.md")
        eq("item 6: a DIFFERENT flag is the newer word: it wins, and nothing is said about a stored paste", (chosen, said), ("/p/new.md", ""))
        chosen, said = entry_line("/p/orig.md", None)
        eq("item 6: a paste stored by an older driver (no `ticket_file_cli`) keeps its precedence and says so too", (chosen, said.count("reading the ticket text you gave earlier")), ("/p/paste.md", 1))
        chosen, said = entry_line("/p/paste.md", "/p/paste.md")
        eq("item 6: the flag IS the stored file -> nothing to explain", (chosen, said), ("/p/paste.md", ""))
        driver.state["s0_answers"] = {"ticket_file": str(root / stored), "ticket_file_cli": "/p/orig.md"}
        driver.state["launch"] = {}
        driver.flags.ticket_file = "/p/orig.md"
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            driver.s0_flags()
        eq("item 6: the file in the line is relative to the project, with forward slashes",
           printed.getvalue(), f"reading the ticket text you gave earlier ({stored}); give a different --ticket-file to replace it\n")
    finally:
        harness.cleanup(root)
    # --- end to end: a wiki paste asks its own title question, and `go on` reads its 2 criteria ---
    root, task_root, env = s0_project(task)
    try:
        wiki = root / "wiki-paste.md"
        wiki.write_text("Items can carry tags\n\nAs a warehouse operator I want tags.\n\nh2. Acceptance Criteria\n# A tag can be added.\n# A tag can be removed.\n", encoding="utf-8")
        out = s0_run(root, env, task, "--ticket-file", str(wiki))
        snapshot = snapshot_of(task_root)
        eq("item 1 (wiki, end to end, FV1-11): the title is kept without a question; the snapshot has the 2 `# ` items as criteria, markup wiki, the sentence below the title in the description",
           (out.returncode, snapshot["title"], snapshot["acceptance_criteria"], snapshot["provenance"]["markup"], snapshot["description"].startswith("As a warehouse operator")),
           (0, "Items can carry tags", ["A tag can be added.", "A tag can be removed."], "wiki", True), out.stdout[-900:] + out.stderr[-400:])
    finally:
        harness.cleanup(root)
    # a header `title:` is a title: no question at all
    root, task_root, env = s0_project(task)
    try:
        titled = root / "titled-wiki.md"
        titled.write_text("---\ntitle: Items can carry tags\n---\nh2. Acceptance Criteria\n# A tag can be added.\n# A tag can be removed.\n", encoding="utf-8")
        out = s0_run(root, env, task, "--ticket-file", str(titled))
        snapshot = snapshot_of(task_root)
        eq("item 1 (wiki with a header title): no question, exit 0, the title and 2 criteria", (out.returncode, snapshot["title"], len(snapshot["acceptance_criteria"])),
           (0, "Items can carry tags", 2), out.stdout[-900:] + out.stderr[-400:])
    finally:
        harness.cleanup(root)


def s0_flags_precedence_unit() -> None:
    """K-F2c at the unit: `s0_flags` for a stored paste against the command line."""
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        driver = driver_for(root, env, task)
        driver.state["launch"] = {"ticket_file": "/p/orig.md"}
        driver.state["s0_answers"] = {"ticket_file": "/p/paste.md", "ticket_file_cli": "/p/orig.md"}
        driver.flags.ticket_file = None
        eq("K-F2c: no flag on the command line -> the stored paste wins", driver.s0_flags()["ticket_file"], "/p/paste.md")
        driver.flags.ticket_file = "/p/orig.md"
        eq("K-F2c: the flag the paste was answered under, repeated by the continue command -> the paste stays", driver.s0_flags()["ticket_file"], "/p/paste.md")
        driver.flags.ticket_file = "/p/new.md"
        eq("K-F2c: a different `--ticket-file` -> the command line wins (the newer word)", driver.s0_flags()["ticket_file"], "/p/new.md")
        eq("K-F2c: and the older paste is dropped, so a later entry with no flag does not go back to it",
           (driver.state["s0_answers"].get("ticket_file"), driver.state["launch"]["ticket_file"]), (None, "/p/new.md"))
        driver.flags.ticket_file = None
        eq("K-F2c: that later entry with no flag reads the newer launch flag", driver.s0_flags()["ticket_file"], "/p/new.md")
        driver.state["s0_answers"] = {"ticket_file": "/p/old-paste.md"}                 # stored by an older driver: no `ticket_file_cli`
        driver.flags.ticket_file = "/p/other.md"
        eq("K-F2c / builder rule 9: a paste stored before this change keeps its old precedence (the flag does not drop it)", driver.s0_flags()["ticket_file"], "/p/old-paste.md")
        # F-5 (critic t-689): the scout's "Ticket source" line reads the KEPT launch too - an `--answer` process carries no `--ticket-file`
        driver.flags.ticket_file = None
        driver.state["launch"] = {"ticket_file": "/p/kept.md"}
        check_in("F-5: no flag on this command line, a kept `--ticket-file`: the scout is told the file", "Ticket source: --ticket-file /p/kept.md",
                 driver.role_lines("S1", "qa-scout"))
        driver.state["launch"] = {}
        check_in("F-5: neither flag nor kept file: the configured adapter", "Ticket source: the project's tracker, by the route below", driver.role_lines("S1", "qa-scout"))
        driver.flags.ticket_file = "/p/now.md"
        check_in("F-5: this command line's flag still wins", "Ticket source: --ticket-file /p/now.md", driver.role_lines("S1", "qa-scout"))
    finally:
        harness.cleanup(root)


def g10_s0_criteria_table() -> None:
    """G1-0 (D-0050, I1-I4, t-957 F-1..F-3): the S0 decision table at the unit, in-process. The expectations come from the requirement
    (a ticket with no criteria section goes on with ONE line; a criteria heading with TEXT under it that read no criteria stops, as the
    factory's own defect; an empty template goes on), not from what the code printed."""
    import ticket_adapter
    import story_run
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        driver = driver_for(root, env, task)
        driver._s0_passed = []                       # `s0()` makes it at its start; a pass applied below appends to it

        def meet(ticket):
            """(what the check raised or returned): ('line', text) or ('stop', question text)."""
            driver.state.pop("s0_block", None)
            try:
                return ("line", driver.s0_criteria(ticket, "through the tracker"))
            except story_run.Person as person:
                return ("stop", person.text)

        def snap(text, **extra):
            return {"title": "T", "description": text, "acceptance_criteria": [], "provenance": extra}

        qa2 = ticket_adapter.parse_ticket_markdown((harness.PLUGIN_ROOT / "evals" / "fixtures" / "tickets" / "QA-2.md").read_text(encoding="utf-8"), "QA-2")
        eq("QA-2 (the fixture without AC): the snapshot carries `acceptance_criteria: []`", qa2["acceptance_criteria"], [])
        kind, line = meet(qa2)
        eq("I1 / D-0050: a ticket with no criteria section goes on - no question - with ONE line naming the headings looked for",
           (kind, line), ("line", "S0: ticket QA-1 has no section named Acceptance Criteria, What needs to be tested, AC; "
                                  "the requirements are read from its description, comments, attachments and linked tickets"))
        check("F-6: and the line fits what gate A shows of a warning (180 characters)", len(line) <= 180, str(len(line)))
        driver.config["adapters"] = {"ticket": {"kind": "jira", "direct_api": {"acceptance_headings": ["A project heading " * 12]}}}
        kind, line = meet(qa2)
        check("F-6: with a long project heading the names are cut, never the sentence: still <= 180 and still ends with the sources",
              kind == "line" and len(line) <= 180 and line.endswith("linked tickets"), line)
        driver.config.pop("adapters", None)
        kind, line = meet(ticket_adapter.parse_ticket_markdown(INCOMPLETE_TICKET, "QA-1"))
        check("F-1: an EMPTY template (heading, nothing under it) goes on, and the line says the section was found empty",
              kind == "line" and "has a section `## Acceptance criteria` with nothing under it" in line, str((kind, line)))
        eq("an absent/empty description is nothing to read: goes on with the line", [meet(snap(None))[0], meet(snap(""))[0]], ["line", "line"])
        for label, text in (("markdown heading + prose", "## Acceptance criteria\n\nThe operator can tag an item."),
                            ("wiki heading + blank + prose + list (the item loop stops at the prose)", "h3. Acceptance Criteria\n\nThe operator can tag.\n\n* item"),
                            ("two sections, the first empty (F-2)", "h3. Acceptance Criteria\n\nh3. Other\n\nh3. AC\nsome prose"),
                            ("a table", "h3. Acceptance Criteria\n||Given||When||\n|a|b|")):
            kind, text_out = meet(snap(text))
            check(f"I2/I4: {label} -> STOP, the factory's reader failing and not the ticket",
                  kind == "stop" and "this is the factory's reader failing on that section, not your ticket" in text_out, str((kind, text_out[:200])))
        kind, text_out = meet(snap("## Acceptance criteria\n\nThe operator can tag an item."))
        check("F-4: the stop offers `go on`, the ticket as text and `stop` - and not `retry`",
              "`go on`" in text_out and "`stop`" in text_out and "`retry`" not in text_out, text_out)
        eq("FR-6: it obeys human-questions.md", [r for r in rules_broken(text_out) if r != "no_how_to_answer"], [])
        # F-3: the snapshot does not always say how it was read; a REST snapshot never does. Both markups are scanned.
        eq("F-3: a REST-like snapshot (no provenance at all) with a MARKDOWN heading and prose still stops", meet(snap("## Acceptance criteria\n\nprose"))[0], "stop")
        eq("F-3: an old paste (provenance without `markup`) with a WIKI heading and prose still stops", meet(snap("h3. Acceptance Criteria\nprose", source="person_pasted"))[0], "stop")
        eq("F-3: the heading the reader took as the TITLE (first line) is put back for the scan",
           meet({"title": "Acceptance criteria", "description": "prose under the heading", "acceptance_criteria": [],
                 "provenance": {"title_from": "first_line"}})[0], "stop")
        eq("n >= 1: a ticket that read criteria never meets the check", driver.s0_criteria({"title": "T", "acceptance_criteria": ["a"]}, "x"), None)
        # temporal (§4.4/§4.5): a pass stored BEFORE D-0050 for the old problem covers the new one; the person is not asked twice
        driver.state["s0_passes"] = {"ticket_incomplete": {"words": "go on", "at": "t", "problems": ["no acceptance criteria"], "recorded": True, "witness": "w"}}
        eq("I3 (§4.5): a saved `go on` with the OLD problem word passes the lost read - no question again",
           meet(snap("## Acceptance criteria\n\nprose")), ("line", None))
        driver.state["s0_passes"] = {"ticket_incomplete": {"words": "go on", "at": "t", "problems": ["unrelated"], "recorded": True, "witness": "w"}}
        eq("... and a pass for another problem covers nothing", meet(snap("## Acceptance criteria\n\nprose"))[0], "stop")
        driver.state.pop("s0_passes", None)
    finally:
        harness.cleanup(root)


def g10_s0_headings_unreadable() -> None:
    """M2 of t-984 (FR-59, FR-46, FR-2): the list of names the criteria are looked for under cannot be built - the project's
    `config.json` key is a string, or the factory's own table is gone. The stop (1) tells whose it is, in the words of the cause;
    (2) never offers the paste (it reads the same text against the same list and comes back here); (3) has its OWN problem word, so
    a `go on` given here never lets a later REAL lost read through, and the reverse; (4) obeys human-questions.md. The expected
    texts come from the requirement (an owner named correctly, no door back to the same stop), not from the code's output."""
    import story_run
    import ticket_light
    task = "QA-1"
    root, task_root, env = s0_project(task)
    real_table = ticket_light.load_fields_table
    try:
        driver = driver_for(root, env, task)
        driver._s0_passed = []
        driver.s0_file_pass = lambda *a, **k: None          # the finding is the filing script's business; this pins the question

        def snap(text):
            return {"title": "T", "description": text, "acceptance_criteria": [], "provenance": {}}

        def meet(ticket):
            driver.state.pop("s0_block", None)
            try:
                return ("line", driver.s0_criteria(ticket, "through the tracker"))
            except story_run.Person as person:
                return ("stop", person)

        lost_ticket = snap("## Acceptance criteria\n\nThe operator can tag an item.")
        plain_ticket = snap("some prose without a criteria section")

        # --- (a) the project's key is the cause: a string where a list of strings belongs
        driver.config["adapters"] = {"ticket": {"kind": "jira", "direct_api": {"acceptance_headings": "Acceptance Criteria"}}}
        kind, person = meet(plain_ticket)
        text, note, ask = person.text, person.answer_note, driver.state.get("s0_ask") or {}
        check("config cause: a stop, not a pass and not a line (FR-59)", kind == "stop", str(kind))
        check_in("config cause: the lead blames the project's setting", "This is the project's setting, not your ticket.", text)
        check_not_in("config cause: ... and does not blame the factory's file", "a file of the factory's own", text)
        check_not_in("config cause: the paste is not offered (it would come back to this stop)", "the ticket itself as text", text)
        check("config cause: the stop is stored without the paste door", ask.get("paste") is False, str(ask.get("paste")))
        check("config cause: only `go on` and `stop` are offered, and no `retry`",
              "`go on`" in text and "`stop`" in text and "`retry`" not in text, text)
        check_in("config cause: the key and its fix reach the answer block whole (the error's own sentence, FR-8)",
                 "direct_api.acceptance_headings must be a list of strings, got str; fix it in qa-factory/config.json", note)
        check_not_in("config cause: ... and not the body (human-questions.md rule 5)", "config.json", text)
        eq("config cause: the text obeys human-questions.md", [r for r in rules_broken(text) if r != "no_how_to_answer"], [])
        eq("config cause: the problem word is the unreadable-list word, not the lost-read word",
           ask.get("problems"), [driver.S0_HEADINGS_UNREADABLE])
        unreadable_problems = list(ask.get("problems") or [])

        # --- (b) the factory's own table is the cause
        driver.config.pop("adapters", None)

        def gone(*a, **k):
            raise ticket_light.TableError("jira-fields.json: missing; restore references/jira-fields.json from the plugin package")
        ticket_light.load_fields_table = gone
        kind, person = meet(plain_ticket)
        text, note, ask = person.text, person.answer_note, driver.state.get("s0_ask") or {}
        check_in("factory cause: the lead blames the factory", "This is the factory failing, not your ticket.", text)
        check_not_in("factory cause: the paste is not offered", "the ticket itself as text", text)
        check_in("factory cause: the file and how to restore it reach the answer block whole",
                 "jira-fields.json: missing; restore references/jira-fields.json from the plugin package", note)
        eq("factory cause: the text obeys human-questions.md", [r for r in rules_broken(text) if r != "no_how_to_answer"], [])
        eq("factory cause: the same unreadable-list problem word", ask.get("problems"), [driver.S0_HEADINGS_UNREADABLE])
        ticket_light.load_fields_table = real_table

        # --- (c) one problem word per fact: a `go on` given to one stop covers nothing of the other
        pass_of = lambda problems: {"ticket_incomplete": {"words": "go on", "at": "t", "problems": problems, "recorded": True, "witness": "w"}}
        driver.state["s0_passes"] = pass_of(unreadable_problems)
        eq("a `go on` given to the unreadable-list stop does NOT let a later REAL lost read through (the person never saw that section)",
           meet(lost_ticket)[0], "stop")
        driver.config["adapters"] = {"ticket": {"kind": "jira", "direct_api": {"acceptance_headings": "Acceptance Criteria"}}}
        eq("... and the same pass still covers the unreadable list it was given for", meet(plain_ticket), ("line", None))
        lost_problems = [driver.S0_LOST_READ]
        driver.state["s0_passes"] = pass_of(lost_problems)
        eq("the reverse: a `go on` given to a lost-read stop does not cover an unreadable list", meet(plain_ticket)[0], "stop")
        driver.config.pop("adapters", None)
        eq("... and still covers the lost read it was given for", meet(lost_ticket), ("line", None))
        eq("the two problem words differ", driver.S0_LOST_READ != driver.S0_HEADINGS_UNREADABLE, True)
        driver.state.pop("s0_passes", None)
    finally:
        ticket_light.load_fields_table = real_table
        harness.cleanup(root)


def s0_headings_sentence_unit() -> None:
    """K-F5 at the unit: the sentence lists the MERGED headings (the table's + the project's), verbatim, and names the setting's door."""
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        driver = driver_for(root, env, task)
        base = driver.s0_headings_looked_for()
        check_in("K-F5: the table's headings, verbatim, in the table's order", "one of: Acceptance Criteria, What needs to be tested, AC.", base)
        driver.config["adapters"] = {"ticket": {"kind": "jira", "direct_api": {"acceptance_headings": ["Things to verify", "ac"]}}}
        merged = driver.s0_headings_looked_for()
        check_in("K-F5: the project's own headings join the list (a name the table already holds, in another case, is not repeated)",
                 "one of: Acceptance Criteria, What needs to be tested, AC, Things to verify.", merged)
        check_in("K-F5: and the door is named", "`direct_api.acceptance_headings` in `qa-factory/config.json`", merged)
        # (`no_how_to_answer` is the block `ask()` appends under the text; this reads the sentence alone)
        eq("K-F5: the sentence obeys human-questions.md (the text a person reads)", [r for r in rules_broken(merged) if r != "no_how_to_answer"], [])
    finally:
        harness.cleanup(root)


def s0_prices_unreadable() -> None:
    """C1-3 (G8, FR-41): a price row an S0 site needs that the data does not have. The question is STILL asked - its option lines
    without the price lines - and ONE `defect_found` (owner: factory) names the key; the answers it takes are the same. In-process
    (a Driver changes the working directory)."""
    import no_move as NM
    import story_run
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        inventory = task_root / "work" / "source-inventory.json"
        inventory.parent.mkdir(parents=True, exist_ok=True)
        inventory.write_text(json.dumps({"schema_version": 1, "sources": []}), encoding="utf-8")
        driver = driver_for(root, env, task)
        real = NM.load_question_prices
        NM.load_question_prices = lambda: {key: rows for key, rows in real().items() if key != "s0.source_list.late"}
        try:
            try:
                driver.s0_list_too_late()
                text = ""
            except story_run.Person as person:
                text, priced = person.text, person.priced
        finally:
            NM.load_question_prices = real
        check_in("prices unreadable: the question is still asked, with its option lines", "(a) `go on` — the story goes on and the list is ignored", text)
        check_in("prices unreadable: `stop` among them", "(b) `stop` — stop here and start the story again from a fresh copy", text)
        check_not_in("prices unreadable: no price line is shown", "the factory:", text)
        eq("prices unreadable: and no token is claimed as priced", priced, ())
        defects = [e for e in s0_journal(root) if e.get("event") == "defect_found"]
        eq("prices unreadable: exactly one defect_found, owner factory, naming the key",
           (len(defects), "owner: factory" in str(defects[0].get("notes")) if defects else False,
            "s0.source_list.late" in str(defects[0].get("notes")) if defects else False), (1, True, True))
        eq("prices unreadable: the doors the next answer reads are the same", sorted(driver.state["s0_ask"]["doors"]), ["go on", "stop"])
        # the control: the real data, the same call - priced, and no defect
        before = len(defects)
        try:
            driver.s0_list_too_late()
        except story_run.Person as person:
            control, claimed = person.text, person.priced
        check_in("prices unreadable, control: with the data the price lines are there", "the factory: a record only; no agent works", control)
        eq("prices unreadable, control: the priced tokens are claimed, and no new defect",
           (claimed, len([e for e in s0_journal(root) if e.get("event") == "defect_found"])), (("go on", "stop"), before))
    finally:
        harness.cleanup(root)


def s0_stand_named_like_an_answer() -> None:
    """G7 / F4 at the process: a stand named `Stop` cannot be chosen by name (one word, two readings - code never guesses which): it is
    LEFT OUT of the stand question's doors and options and ONE finding names it (owner: environment); the other stands and `stop`
    stay; the word `Stop` is the stop door (held), never the stand."""
    task = "QA-1"
    root, task_root, env = s0_project(task, config={"environments": [{"name": "Stop"}, {"name": "Local"}]})
    try:
        out = s0_run(root, env, task, "--env", "nosuch")
        eq("G7: an unmatched `--env` with a stand named `Stop` still asks the stand question: exit 3", out.returncode, 3, out.stdout[-800:])
        ask, state = s0_question(task_root), s0_state(task_root)
        eq("G7: the doors are `local`, `go on` and `stop` -> `stop` (the stand `Stop` is not one of them)",
           state["s0_ask"]["doors"], {"stop": "stop", "local": "Local", "go on": "go on"})
        check("G7: the options offer `Local`, `go on`, `stop` as priced lines and never the stand `Stop`",
              "`Local` — " in ask and "`go on` — " in ask and "`stop` — " in ask and "`Stop` — " not in ask and price_broken(ask) == [], ask[-900:])
        check_in("F-3: the question names the left-out stand and says it needs renaming (FR-3: the person is told why a stand is missing)",
                 "This stand is named like an answer to this question, so it cannot be chosen by name: `Stop`. It needs renaming in the project's list of stands.", ask)
        check_not_in("F-3: and the configured stands it still offers are named as before", "no stand configured", ask)
        check_in("F-3: some clash: the remaining stand is still named", "The configured stands are `Local`.", ask)
        eq("F-3: the text still obeys the rules of the file for a person (no path, no field name)", rules_broken(ask), [])
        found = [e for e in s0_journal(root) if e.get("event") == "defect_found" and "`Stop`" in str(e.get("notes"))]
        eq("G7/G8: ONE finding names the stand, owner: environment",
           (len(found), str(found[0].get("notes", "")).startswith("owner: environment — the stand(s) `Stop` ") if found else None), (1, True))
        out = s0_answer(root, env, task, "Stop", "--env", "nosuch")
        check("G7: the word `Stop` is the stop door: the question is held (exit 3), no stand was chosen",
              out.returncode == 3 and "You said to stop." in s0_question(task_root) and "env" not in (s0_state(task_root).get("s0_answers") or {}),
              out.stdout[-500:])
    finally:
        harness.cleanup(root)
    # F-3 (critic t-689): EVERY configured stand clashes -> the person is not told "no stand configured" (false, FR-41); the question
    # names the left-out stands and says they need renaming, offers no stand, and still has `go on` and `stop`
    root, task_root, env = s0_project(task, config={"environments": [{"name": "Stop"}, {"name": "Retry"}]})
    try:
        out = s0_run(root, env, task, "--env", "nosuch")
        eq("F-3: all stands clash: still the stand question (exit 3)", out.returncode, 3, out.stdout[-800:])
        ask, state = s0_question(task_root), s0_state(task_root)
        check_not_in("F-3: all clash: it never says no stand is configured", "no stand configured", ask)
        check_in("F-3: all clash: it says none of the configured stands can be chosen by name", "none of the stands this project has configured can be chosen by name.", ask)
        check_in("F-3: all clash: it names the left-out stands and that they need renaming",
                 "These stands are named like an answer to this question, so they cannot be chosen by name: `Stop`, `Retry`. They need renaming in the project's list of stands.", ask)
        check("F-3: all clash: no stand option, only `go on` and `stop`, priced",
              "`Stop` — " not in ask and "`Retry` — " not in ask and "`go on` — " in ask and "`stop` — " in ask and price_broken(ask) == [], ask[-900:])
        eq("F-3: all clash: the doors are `go on` and `stop` only", state["s0_ask"]["doors"], {"stop": "stop", "go on": "go on"})
        eq("F-3: all clash: the text obeys the rules of the file for a person", rules_broken(ask), [])
    finally:
        harness.cleanup(root)


def s0_unread_road_units() -> None:
    """G1 and F4 in-process: after a conductor `continue` / `retry` at S0 the stored block is ABSENT and `s0_read_word` returns None (the
    callers run the step again); on a raise the block is stored again ONLY on that path; `s0_doors` never replaces a door held
    under `stop` (a stand named `Stop`); both callers use `s0_read_word` as a statement (None = nothing decided)."""
    import story_run
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        ask = {"kind": "halt", "text": "Which one?", "details": "d", "doors": {"mr": "mr", "branch": "branch"}, "paste": False, "problems": []}
        for verdict in ("continue", "retry"):
            driver = driver_for(root, env, task)
            driver.state.update(s0_block="flags", s0_ask=dict(ask), pending_words={"S0": "something else"})
            driver.unread = lambda *a, verdict=verdict, **k: verdict
            got = driver.s0_read_word()
            kept = s0_state(task_root)
            eq(f"G1: a conductor `{verdict}` -> None to the caller, `s0_block` / `s0_ask` absent in memory and on disk, the words consumed",
               (got, "s0_block" in driver.state, "s0_ask" in driver.state, "s0_block" in kept, "s0_ask" in kept, "S0" in (kept.get("pending_words") or {})),
               (None, False, False, False, False, False))
            check_not_in(f"G1: `{verdict}` passes nothing and decides nothing", "s0_passes", json.dumps(kept))
        driver = driver_for(root, env, task)
        driver.state.update(s0_block="flags", s0_ask=dict(ask), pending_words={"S0": "something else"})

        def asks(*a, **k):
            raise story_run.Person("halt", "again", "S0")
        driver.unread = asks
        try:
            driver.s0_read_word()
            check("G1: a question raised by the seam leaves the block stored", False)
        except story_run.Person:
            kept = s0_state(task_root)
            eq("G1: a RAISE stores the block again (memory and disk): the next answer is read against the same doors",
               (driver.state.get("s0_block"), kept.get("s0_block"), sorted((kept.get("s0_ask") or {}).get("doors") or {})), ("flags", "flags", ["branch", "mr"]))
        eq("F4: `s0_doors` never replaces a door held under `stop` (a stand named `Stop`)",
           story_run.Driver.s0_doors({"stop": "Stop", "go on": "go on"}), {"stop": "Stop", "go on": "go on"})
        eq("F4: and adds `stop` when the block holds none", story_run.Driver.s0_doors({"retry": "retry"}), {"stop": "stop", "retry": "retry"})
        # (the source check that the two callers use `s0_read_word()` as a bare statement was a source pin: deleted by TD-11 phase 0, F3)
    finally:
        harness.cleanup(root)


def main() -> None:
    run_scenarios(
        [
        s0_stand_named_like_an_answer,
        s0_title_question,
        s0_pasted_description_15045,
        s0_ticket_file_precedence,
        s0_paste_only_references,
    ],
        [
        s0_owners_of_a_failed_read,
        t287_config_owner_is_the_ticket_read_question,
        t287_texts_name_the_file_read,
        fv111_title_taken_without_a_question,
        s0_flags_precedence_unit,
        g10_s0_criteria_table,
        g10_s0_headings_unreadable,
        s0_headings_sentence_unit,
        s0_prices_unreadable,
        s0_unread_road_units,
    ],
    )
    harness.finish("test_story_run_s0_paste_owners")


# split: runner piece 1
if __name__ == "__main__":
    main()
