#!/usr/bin/env python3
"""sources: a part of test_story_run_refusals.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_run_refusals_common."""
import contextlib
import io
import json
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_eq, check_in, check_not_in  # noqa: E402
from story_run_common import driver_for, jsonl, run_scenarios, seed
from story_run_refusals_common import git_fixture  # noqa: E402


def refusal_left_out_sources() -> None:
    """B-231 P4/P8: what the person left out before the run is never collected by code, never routed through the
    local checkout, and is named to the scout; the review question says how to take a word back."""
    import subprocess
    import source_exclusions as SE
    task = "TP1-15045"
    root, task_root, env = seed(task)
    try:
        app, sha = git_fixture(root)
        cfg_path = root / "qa-factory" / "config.json"
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        cfg["implementation_repos"] = [{"repo_id": "testproject1-ui", "local_path": "app",
                                        "remote_identity": "git.example/tp1-group/testproject1-ui"}]
        cfg_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
        driver = driver_for(root, env, task)

        # --- close_vcs_gaps_skips_excluded: the `vcs_evidence` stub must not be called for the excluded item ---
        url_1924 = "https://git.example/tp1-group/testproject1-ui/-/merge_requests/1924"
        url_1881 = "https://git.example/tp1-group/testproject1-ui/-/merge_requests/1881"
        inventory = task_root / "work" / "source-inventory.json"
        inventory.write_text(json.dumps({"schema_version": 1, "sources": [
            {"source_id": "SRC-1", "canonical_ref": "https://jira.example.invalid/browse/TP1-15045", "status": "read",
             "materials": {"external_media": {"status": "pending", "items": [
                 {"url": url_1924, "status": "excluded", "excluded_by": {"exclusion": "X1"}},
                 {"url": url_1881, "status": "pending"}]}}}]}), encoding="utf-8")
        calls: list = []

        def fake_py(script, *args, **kwargs):
            calls.append((script, list(args)))
            if script == "vcs_evidence.py":
                target = driver.project / args[args.index("--output") + 1]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(json.dumps({"status": "read", "revision": "abc123456789", "complete": True,
                                              "discussions": [], "notes": [], "diffs": [], "metadata": {}}), encoding="utf-8")
            return 0, ""

        saved_py = driver.py
        driver.py = fake_py
        try:
            check_eq("close_vcs_gaps_skips_excluded: the ladder collects what is pending", driver.close_vcs_gaps(
                ["source-inventory.json: materials not inspected"]), True)      # no id: "every source is fair game"
            fetched = [a[a.index("--url") + 1] for s, a in calls if s == "vcs_evidence.py"]
            check_eq("close_vcs_gaps_skips_excluded: vcs_evidence is asked for 1881 and never for 1924", fetched, [url_1881])
            recorded = [a[a.index("--media-url") + 1] for s, a in calls if s == "ticket_adapter.py"]
            check_eq("and only 1881 is recorded as inspected", recorded, [url_1881])
            calls.clear()
            check_eq("with a source id named the same skip holds", driver.close_vcs_gaps(
                ["source material unavailable and not accepted by a person: SRC-1"]), True)
            check_eq("(same again: 1881 only)", [a[a.index("--url") + 1] for s, a in calls if s == "vcs_evidence.py"], [url_1881])
            # an excluded item alone: nothing to collect, nothing asked of anyone
            inventory.write_text(json.dumps({"schema_version": 1, "sources": [
                {"source_id": "SRC-1", "status": "read", "materials": {"external_media": {"status": "read", "items": [
                    {"url": url_1924, "status": "excluded"}]}}}]}), encoding="utf-8")
            calls.clear()
            check_eq("only excluded items: no collection, the caller is not told something was collected",
                     (driver.close_vcs_gaps(["source-inventory.json: materials not inspected"]), calls), (False, []))
        finally:
            driver.py = saved_py

        # --- git_route: a commit only an excluded head carries is skipped (C2) --------------------------------
        def route(label):
            note = driver.git_route(url_1881, "sources/SRC-1/mr-1881-git.md")
            body = (task_root / "work" / "sources" / "SRC-1" / "mr-1881-git.md")
            return note, (body.read_text(encoding="utf-8") if body.is_file() else "")

        note, body = route("no list")
        check("git_route, no list: both commits of the ticket prefix are listed (today's behaviour)",
              sha["A"][:9] in note and sha["C"][:9] in note, note)
        text = "testproject1-ui!1924 - Draft MR of an earlier factory run, not a product change\n"
        entries, problems = SE.parse_bytes(text.encode("utf-8"), task)
        check_eq("the list parses", problems, [])
        entries[0]["target"]["head_sha"] = sha["C"]
        inventory.unlink()                     # a list is written before the inventory exists, never after
        SE.write_record(task_root, entries, "list.txt", text.encode("utf-8"))
        (task_root / "work" / "sources" / "SRC-1" / "mr-1881-git.md").unlink()
        note, body = route("excluded head")
        check("git_route skips the commit only the excluded head carries", sha["C"][:9] not in note and sha["C"] not in body,
              note + body[:400])
        check("git_route keeps the older commit of the prefix that main carries too (an ancestor of the head, not its own change)",
              sha["A"][:9] in note and sha["A"] in body, note + body[:400])
        # an unreachable head skips nothing
        record = json.loads((task_root / "work" / "source-exclusions.json").read_text(encoding="utf-8"))
        record["exclusions"][0]["target"]["head_sha"] = "f" * 40
        (task_root / "work" / "source-exclusions.json").write_text(json.dumps(record), encoding="utf-8")
        (task_root / "work" / "sources" / "SRC-1" / "mr-1881-git.md").unlink()
        note, body = route("unreachable head")
        check("git_route: a head this checkout does not hold skips nothing", sha["A"][:9] in note and sha["C"][:9] in note, note)
        # the head once main carries it too: no longer only the excluded request's own change
        git_env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
        for args in (["checkout", "-q", "-B", "main", "feat"], ["commit", "-q", "--allow-empty", "-m", "later work on main"]):
            subprocess.run(["git", "-C", str(app), *args], check=True, capture_output=True, env=git_env)
        record["exclusions"][0]["target"]["head_sha"] = sha["C"]
        (task_root / "work" / "source-exclusions.json").write_text(json.dumps(record), encoding="utf-8")
        (task_root / "work" / "sources" / "SRC-1" / "mr-1881-git.md").unlink()
        note, body = route("merged head")
        check("git_route: a commit another branch carries is not skipped (in doubt it is read)",
              sha["C"][:9] in note, note)
        # an abbreviated head of a `ref` word resolves to the full id
        check("only_from_excluded_head: a head that resolves to nothing is False, a commit that is no hex is False",
              not driver.only_from_excluded_head(app, sha["A"], ["deadbeef" * 5]) and
              not driver.only_from_excluded_head(app, "not-a-sha", [sha["C"]]))

        # --- role_lines: the scout is told, with the head commit (C2) and the door ---------------------------------
        lines = driver.role_lines("S1", "qa-scout")
        told = [ln for ln in lines if ln.startswith("Left out by the person's word before the run")]
        check_eq("role_lines: one line for the scout", len(told), 1)
        check_in("role_lines: the word as written and the reason", 'testproject1-ui!1924 ("Draft MR of an earlier factory run', told[0])
        check_in("role_lines: the head commit, so a citation by commit is the same source", f"head commit {sha['C'][:12]}", told[0])
        check_in("role_lines: what not to do with it", "do not read, collect, cite as a source, precedent or existing coverage", told[0])
        check_in("role_lines: and the door", "say so in your handoff", told[0])
        check_eq("role_lines: other roles get no such line", [ln for ln in driver.role_lines("S2", "qa-requirements-tester")
                                                               if "Left out" in ln], [])
        SE.record_path(task_root / "work").write_text("{not json", encoding="utf-8")
        try:
            driver.role_lines("S1", "qa-scout")
            check("role_lines: an unreadable record refuses", False)
        except story_run_refusal() as refusal:
            check_in("role_lines: an unreadable record is a refusal that names the file", "source-exclusions.json", refusal.text)
        SE.record_path(task_root / "work").unlink()
        check_eq("role_lines: no record, no line (today's launch lines)",
                 [ln for ln in driver.role_lines("S1", "qa-scout") if "Left out" in ln], [])
        launch = (driver.state.setdefault("launch", {}))
        launch["mr_dropped"] = "!1924"
        driver.flags.mr = "!1924"
        check_in("role_lines: an --mr the person gave up at S0 is not in the scout's launch flags",
                 "Launch flags: none", "\n".join(driver.role_lines("S1", "qa-scout")))
        driver.flags.mr = None

        # --- the review question says how to take a word back -------------------------------------------------------
        driver.py = lambda script, *a, **k: (0, "THE TABLE")
        check_not_in("review text, no list: no sentence about left-out sources", "left out by you", driver.s1_review_text("digest"))
        (task_root / "work" / "source-exclusions.json").write_text(json.dumps(record), encoding="utf-8")
        shown = driver.s1_review_text("digest")
        check_in("review text, a list: the sentence", "The ones marked 'left out by you (before the run)' are not read; to read "
                 "one after all, name it in your answer.", shown)
        check_eq("review text: the sentence is there once", shown.count("left out by you"), 1)
    finally:
        harness.cleanup(root)


def refusal_adapter_forms_links_and_prefix() -> None:
    """B-405/B-406 (R9): `close_vcs_gaps` reads a link by `ticket_light.classify_url` - the PATH only, the number is group 2
    and must end the path or be followed by `/` (B7), a pull request is never sent to the GitLab collector - and `git_route`
    takes the ticket's prefix from the project's key form (none under a prefix-less form: the commit search is skipped)."""
    import subprocess
    task = "TP1-15045"
    root, task_root, env = seed(task)
    try:
        driver = driver_for(root, env, task)
        base = "https://githost.example.test/g/p"
        links = {
            "plain": f"{base}/-/merge_requests/5",
            "diffs": f"{base}/-/merge_requests/6/diffs",
            "query": "https://githost.example.test/login?next=/g/p/-/merge_requests/7",
            "glued": f"{base}/-/merge_requests/8a",
            "pull": "https://github.com/o/r/pull/9",
            "enterprise": "https://ghe.example.test/o/r/pull/10",
            "escaped": f"{base}/-/merge" + chr(92) + "_requests/11",
            "issue": f"{base}/-/issues/12",
            "bitbucket": "https://bitbucket.example.test/o/r/pull-requests/13",
            "fragment": "https://githost.example.test/login#/g/p/-/merge_requests/14",
        }
        inventory = task_root / "work" / "source-inventory.json"
        inventory.parent.mkdir(parents=True, exist_ok=True)
        inventory.write_text(json.dumps({"schema_version": 1, "sources": [
            {"source_id": "SRC-1", "canonical_ref": "https://jira.example.invalid/browse/TP1-15045", "status": "read",
             "materials": {"external_media": {"status": "pending", "items": [
                 {"url": url, "status": "pending"} for url in links.values()]}}}]}), encoding="utf-8")
        calls: list = []

        def fake_py(script, *args, **kwargs):
            calls.append((script, list(args)))
            if script == "vcs_evidence.py":
                target = driver.project / args[args.index("--output") + 1]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(json.dumps({"status": "read", "revision": "abc123456789", "complete": True,
                                              "discussions": [], "notes": [], "diffs": [], "metadata": {}}), encoding="utf-8")
            return 0, ""

        saved_py = driver.py
        driver.py = fake_py
        shown = io.StringIO()
        try:
            with contextlib.redirect_stdout(shown):
                got = driver.close_vcs_gaps(["source-inventory.json: materials not inspected"])
        finally:
            driver.py = saved_py
        fetched = [a[a.index("--url") + 1] for s, a in calls if s == "vcs_evidence.py"]
        outputs = [a[a.index("--output") + 1].rsplit("/", 1)[-1] for s, a in calls if s == "vcs_evidence.py"]
        recorded = [a[a.index("--media-url") + 1] for s, a in calls if s == "ticket_adapter.py"]
        check_eq("forms/links: the ladder collected something", got, True)
        check_eq("forms/links: only the merge requests are sent to the GitLab collector (plain, /diffs, the markdown-escaped one)",
                 fetched, [links["plain"], links["diffs"], links["escaped"].replace(chr(92), "")])
        check_eq("forms/links B7: the number is group 2 of the kind's rule (5, 6 from /diffs, 11 through the escape)",
                 outputs, ["mr-5.json", "mr-6.json", "mr-11.json"])
        check_eq("forms/links: and only those are recorded as inspected", recorded, [links["plain"], links["diffs"], links["escaped"]])
        for name in ("query", "glued", "enterprise", "issue", "bitbucket", "fragment"):
            check(f"forms/links: `{name}` is no request (never collected without a receipt)", links[name] not in fetched, str(fetched))
        check("forms/links: a pull request is never sent to vcs_evidence", links["pull"] not in fetched)
        check_in("forms/links: ... one line says why, naming the link", links["pull"] + " is a pull request", shown.getvalue())
        check_in("forms/links: ... and that it stays pending", "left pending", shown.getvalue())
        items = {i["url"]: i["status"] for s in json.loads(inventory.read_text(encoding="utf-8"))["sources"]
                 for i in s["materials"]["external_media"]["items"]}
        check_eq("forms/links: the pull request item stays pending in the inventory", items[links["pull"]], "pending")
        check_eq("forms/links: so does a glued number", items[links["glued"]], "pending")
    finally:
        harness.cleanup(root)

    # --- git_route: the prefix is the key form's ---
    def route_for(task_name: str, ticket_cfg: dict | None, commits: tuple = (), url_iid: str = "1881"):
        proj, proj_root, proj_env = seed(task_name)
        try:
            app, _sha = git_fixture(proj)
            git_env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
            for message in commits:
                subprocess.run(["git", "-C", str(app), "commit", "-q", "--allow-empty", "-m", message], check=True,
                               capture_output=True, env=git_env)
            cfg_path = proj / "qa-factory" / "config.json"
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            cfg["implementation_repos"] = [{"repo_id": "testproject1-ui", "local_path": "app",
                                            "remote_identity": "git.example/tp1-group/testproject1-ui"}]
            if ticket_cfg is not None:
                cfg["adapters"]["ticket"].update(ticket_cfg)
            cfg_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
            drv = driver_for(proj, proj_env, task_name)
            said = io.StringIO()
            with contextlib.redirect_stdout(said):
                note = drv.git_route(f"https://git.example/tp1-group/testproject1-ui/-/merge_requests/{url_iid}", "sources/SRC-1/mr-x-git.md")
            written = proj_root / "work" / "sources" / "SRC-1" / "mr-x-git.md"
            return note, said.getvalue(), (written.read_text(encoding="utf-8") if written.is_file() else "")
        finally:
            harness.cleanup(proj)

    note, said, body = route_for("TP1-15045", None)
    check("forms/git_route (Jira, today's behaviour): the ticket prefix finds the commits of the ticket", "the local checkout app" in note, note)
    check_not_in("forms/git_route (Jira): nothing is skipped, so nothing is said", "no project prefix", said)
    note, said, body = route_for("123", {"name": "github"})
    check_eq("forms/git_route (numeric story, no ref for this number): the prefix search is skipped, so nothing is found", (note, body), ("", ""))
    check_in("forms/git_route (numeric story): the line says the prefix search was skipped and why", "has no project prefix", said)
    note, said, body = route_for("123", {"name": "github"}, url_iid="1924")
    check("forms/git_route (numeric story): the merge-request ref is still asked and answers", "the local checkout app" in note, note)
    # MY_PROJ-12: the prefix is MY_PROJ (the old regex read PROJ, and `--grep=PROJ-` also lists the commits of PROJ-99, another project)
    note, said, body = route_for("MY_PROJ-12", None, commits=("MY_PROJ-12 the story's change", "PROJ-99 another project's change"))
    check_in("forms/git_route (MY_PROJ-12): the story's own commit is listed", "MY_PROJ-12 the story's change", body)
    check_not_in("forms/git_route (MY_PROJ-12): the other project's commit is not (the prefix is MY_PROJ, whole)", "PROJ-99 another", body)
    check_not_in("forms/git_route (MY_PROJ-12): a prefix exists, so no line about skipping", "no project prefix", said)


def refusal_launch_warns_on_a_task_that_is_no_key() -> None:
    """B-405 R14: `--task` that is not a ticket key of the project's form prints ONE WARN naming the form, and the run
    goes on (a warning, never a refusal: P1); a proper key prints nothing."""
    def launch(task: str, ticket_cfg: dict | None = None) -> tuple:
        root, task_root, env = seed(task)
        try:
            if ticket_cfg is not None:
                cfg_path = root / "qa-factory" / "config.json"
                cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
                cfg["adapters"]["ticket"].update(ticket_cfg)
                cfg_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
            shown = io.StringIO()
            with contextlib.redirect_stdout(shown):
                driver = driver_for(root, env, task)
            return [ln for ln in shown.getvalue().splitlines() if ln.startswith("WARN: --task")], driver.task
        finally:
            harness.cleanup(root)

    lines, task = launch("QA-9")
    check_eq("launch/jira: a proper key prints no WARN", (lines, task), ([], "QA-9"))
    lines, task = launch("my_task")
    check_eq("launch/jira: a task that is no key prints exactly one WARN and the driver is built (the run goes on)",
             (len(lines), task), (1, "my_task"))
    check_in("launch/jira: ... naming the task and the form", "'my_task' is not a ticket key of this project: a ticket key like PROJ-123", lines[0])
    check_in("launch/jira: ... and that it goes on", "going on", lines[0])
    lines, task = launch("123", {"name": "github"})
    check_eq("launch/github: a number is a key", (lines, task), ([], "123"))
    lines, task = launch("QA-9", {"name": "github"})
    check_eq("launch/github: a Jira-shaped task is not, and the WARN names the numeric form", (len(lines), "like #123" in lines[0]), (1, True))


def refusal_person_words_kept_whole() -> None:
    """t-208 / FR-8: the driver writes a person's answer into the `human_answer` journal note, and every later
    brief reads that note as the person's standing instructions. Cut at 1,500 characters (cmp2, 01.10: the S1
    source-review answer, about 1,900 characters), the sentence at the END of an answer - the standing
    instruction - never reached a role. INVARIANT: a note carries the words whole, any size (it goes to the journal by a file,
    `log_append.py --notes-file`); the stage prefix and an empty answer stay as they were; an owed row keeps the file."""
    import brief_pack
    import person_words
    import story_run
    standing = "Standing for every role after this: never write to the tracker, Draft only."
    # 2,500 characters with a line break in the middle and the standing sentence last: the part a cut at
    # 1,500 loses is the part that matters
    body = "\n".join(f"line {n}: the review of this source is as written." for n in range(1, 41))
    words = (body + "\n" + "w" * (2500 - len(body) - len(standing) - 2) + " " + standing)
    check_eq("fixture: the answer is 2,500 characters and ends with the standing sentence",
             (len(words), words.endswith(standing)), (2500, True))

    root, task_root, env = seed("QA-9")
    try:
        driver = driver_for(root, env, "QA-9")
        inventory = driver.task_root / "work" / "source-inventory.json"
        inventory.parent.mkdir(parents=True, exist_ok=True)
        inventory.write_text(json.dumps({"schema_version": 1, "sources": []}), encoding="utf-8")
        real_py = driver.py

        def py(script, *args, **kwargs):
            # the review recording is the adapter's own business (proved elsewhere); the journal is real
            return (0, "") if script == "ticket_adapter.py" else real_py(script, *args, **kwargs)
        driver.py = py

        def answer(kind: str, stage: str, dispatch: str, text: str) -> None:
            driver.state["asked"] = {"kind": kind, "stage": stage, "dispatch": dispatch}
            driver.conductor_calls = {}        # each answer is its own session: the per-boundary cap (3) is not what this scenario judges
            driver.state_dir.mkdir(parents=True, exist_ok=True)
            (driver.state_dir / "driver-question.md").write_text("---\nkind: " + kind + "\n---\nQuestion?\n", encoding="utf-8")
            sent = root / "answer.md"
            sent.write_bytes(text.encode("utf-8"))
            driver.take_answer(sent)

        def notes() -> list:
            return [str(e.get("notes")) for e in jsonl(root / "qa-factory" / "records" / "journal.jsonl")
                    if e.get("event") == "human_answer"]

        # (1) the S1 source review
        answer("s1_review", "S1", "S1-qa-scout-1", words)
        check_in("the S1 review answer is in its human_answer note whole, after the stage prefix",
                 "S1 source review: " + words, notes())
        check_eq("and the driver's own answers file holds it whole too",
                 jsonl(driver.state_dir / "driver-answers.jsonl")[-1]["words"], words)
        _shown, whole = brief_pack.decisions({}, "S2", "qa-case-designer", "QA-9", root)
        check_in("the standing sentence at its end is in the next brief's decisions side file",
                 standing, "\n".join(whole))
        check_in("with the whole answer beside it", "S1 source review: " + words, "\n".join(whole))

        # (2) a question stop: the answer keeps its lead words and goes whole
        stop_words = words.replace("line 1:", "stop line 1:", 1)
        answer("questions", "S2", "S2-qa-case-designer-1", stop_words)
        check_in("a question-stop answer is in its note whole, after `S2 question stop: `",
                 "S2 question stop: " + stop_words, notes())
        check_in("and its standing sentence reaches the side file too", "S2 question stop: " + stop_words,
                 "\n".join(brief_pack.decisions({}, "S3", "qa-case-designer", "QA-9", root)[1]))

        # (3) at and beyond the old limit (FV1-4 N0, J-1): no size cuts the note - it travels by a file, not a command line
        for size in (20000, 21000, 40000):
            sized = chr(ord("a") + size % 7) * size
            answer("questions", "S2", "S2-qa-case-designer-1", sized)
            got = [n for n in notes() if n == "S2 question stop: " + sized]
            check_eq(f"J-1: an answer of {size} characters is in its note whole, once", len(got), 1)
            check_not_in(f"J-1: and the note of {size} characters has no cut marker", "[cut:", got[0] if got else "")
            check_eq(f"J-1: while the answers file keeps all of {size}",
                     jsonl(driver.state_dir / "driver-answers.jsonl")[-1]["words"], sized)

        # (4) edges of the helper itself: a prefix with nothing after it is today's note, CRLF becomes LF
        check_eq("J-2: an empty answer is the prefix alone, as before", story_run._answer_note("S1: ", ""), "S1: ")
        check_eq("J-3: CRLF in an answer becomes LF in the note", story_run._answer_note("S1: ", "a\r\nb"), "S1: a\nb")
        check_eq("J-3: person_words.lf is the one place of that rule", (person_words.lf("a\r\nb\rc\n"), person_words.lf(None)),
                 ("a\nb\nc\n", ""))
        # J-2 end to end: an empty answer reaches answer_row as the prefix alone, written to its file
        before = len(notes())
        driver.answer_row("S1: ", "", what="the empty answer")
        check_eq("J-2: the prefix alone is a note, written by its file", notes()[before:], ["S1: "])
        check_eq("J-2: the file that carried it holds the prefix", [p.read_text(encoding="utf-8") for p in
                 sorted((driver.state_dir.parent / "state" / "words").glob("driver-journalnote-*.txt"))][-1], "S1: ")

        # J-4 the door itself: refused with the reader's own words, nothing written
        story_dir = driver.state_dir.parent
        bad = root / "bad-notes"
        bad.mkdir(exist_ok=True)

        def door(*extra):
            return real_py("log_append.py", "--event", "human_answer", "--task", "QA-9", *extra)
        count = len(notes())
        empty, utf16 = bad / "empty.txt", bad / "utf16.txt"
        empty.write_bytes(b"")
        utf16.write_bytes("words".encode("utf-16"))
        for label, extra in (("missing", ["--notes-file", str(bad / "none.txt")]), ("empty", ["--notes-file", str(empty)]),
                             ("not UTF-8", ["--notes-file", str(utf16)]), ("a directory", ["--notes-file", str(bad)])):
            code, out = door(*extra)
            check_eq(f"J-4: a {label} --notes-file is refused, exit 1, naming the option", (code, "--notes-file" in out), (1, True))
        code, out = door("--notes", "inline words", "--notes-file", str(empty))
        check_eq("J-4: --notes with --notes-file is refused naming both", (code, "--notes" in out and "--notes-file" in out), (1, True))
        good = bad / "good.txt"
        good.write_bytes("first\r\nsecond".encode("utf-8"))
        check_eq("J-4: --notes at its default with --notes-file is accepted", door("--notes", "", "--notes-file", str(good))[0], 0)
        check_eq("J-4: nothing was written by the refusals; the file's text is whole, as given",
                 notes()[count:], ["first\r\nsecond"])

        # (5) J-5 / TEMPORAL / E-31 / E-32 / blank: the owed row keeps the file, the replay writes whole
        calls = []
        failing = [True]

        def py_fail(script, *args, **kwargs):
            if script == "log_append.py" and "human_answer" in args:
                calls.append(list(args))
                if failing[0]:
                    return (1, "journal refused once")
            return real_py(script, *args, **kwargs)
        driver.py = py_fail
        long_words = "five " + "x" * 39990 + "\nsecond line"
        before = len(notes())
        with contextlib.redirect_stdout(io.StringIO()):
            driver.answer_row("S3: ", long_words, what="the long answer")
        owed = driver.owed_list()
        args = owed[-1]["args"]
        kept = Path(args[args.index("--notes-file") + 1])
        check_eq("J-5: the failed first write left no row and the owed row names the file by an absolute path",
                 (len(notes()) - before, "--notes" in args, kept.is_absolute()), (0, False, True))
        check_eq("J-5: the file holds prefix + words whole", kept.read_text(encoding="utf-8"), "S3: " + long_words)
        failing[0] = False
        with contextlib.redirect_stdout(io.StringIO()):
            driver.owed_rows_step()
        check_eq("J-5: the replay writes prefix + words whole", notes()[before:], ["S3: " + long_words])
        check_eq("J-5: the file is still there and the row left the list", (kept.is_file(), driver.owed_list()), (True, []))

        # TEMPORAL: a row owed BEFORE this change carries --notes <text> and replays to the same note
        driver.state["owed_rows"] = [{"id": "row-old", "script": "log_append.py", "tries": 1, "exit": 1, "what": "an old row",
                                      "stage": "S1", "at": "2026-11-01T00:00:00+00:00", "tail": "",
                                      "args": ["--event", "human_answer", "--task", "QA-9", "--notes", "S1: an old note"]}]
        before = len(notes())
        with contextlib.redirect_stdout(io.StringIO()):
            driver.owed_rows_step()
        check_eq("TEMPORAL: a pre-change owed row replays to the same note", notes()[before:], ["S1: an old note"])

        # a blank note (no prefix, blank words) writes no file and passes --notes as before
        calls.clear()
        files_before = sorted((story_dir / "state" / "words").glob("driver-journalnote-*.txt"))
        driver.answer_row("", "  ", what="a blank note")
        check_eq("blank: the row passes --notes with the blank note, and no file is made",
                 (calls[-1][calls[-1].index("--notes"):], sorted((story_dir / "state" / "words").glob("driver-journalnote-*.txt"))
                  == files_before), (["--notes", "  "], True))

        # E-32: the story folder moved before the replay -> refused naming the file, the row stays owed
        failing[0] = True
        with contextlib.redirect_stdout(io.StringIO()):
            driver.answer_row("S3: ", "moved words", what="the moved answer")
        moved = Path(driver.owed_list()[-1]["args"][-1])
        hidden = moved.with_name(moved.name + ".moved")
        moved.rename(hidden)
        failing[0] = False
        before = len(notes())
        import driver_core
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                driver.owed_rows_step()
            asked = False
        except driver_core.Person:
            asked = True        # the second failure is the seam's question (OWED_ROW_TRIES, unchanged)
        rows = driver.owed_list()
        check_eq("E-32: the replay is refused, the row stays owed with the file it names, nothing is written, the seam asks",
                 (len(notes()) - before, len(rows), moved.name in rows[0]["tail"], asked), (0, 1, True, True))
        hidden.rename(moved)
        driver.state["owed_rows"] = []

        # E-31 (F12 a): the note file cannot be written -> OSError propagates, the command line is never the road
        calls.clear()
        real_write = person_words.write_words

        def broken_write(*a, **k):
            raise OSError("disk full")
        person_words.write_words = broken_write
        try:
            driver.answer_row("S3: ", "unsaved", what="the unsaved answer")
            raised = False
        except OSError:
            raised = True
        finally:
            person_words.write_words = real_write
        check_eq("E-31: a failed write raises OSError and no log_append call is made", (raised, calls), (True, []))
    finally:
        harness.cleanup(root)


def story_run_refusal():
    import story_run
    return story_run.Refusal


def main() -> None:
    run_scenarios([], [
        refusal_left_out_sources,
        refusal_adapter_forms_links_and_prefix,
        refusal_launch_warns_on_a_task_that_is_no_key,
        refusal_person_words_kept_whole,
    ])
    harness.finish("test_story_run_refusals_sources")


# split: runner piece 1
if __name__ == "__main__":
    main()
