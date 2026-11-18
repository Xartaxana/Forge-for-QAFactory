"""source list: a part of test_story_run_s0.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_run_s0_common."""
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_in, check_not_in  # noqa: E402
from story_run_common import driver_for, eq, rules_broken, s0_answer, s0_findings, s0_pipeline, s0_project, s0_question, s0_run, s0_state, set_control, stub_calls, run_scenarios
from story_run_s0_common import (  # noqa: E402
    DRAFT, EM, NO_USABLE, UNREAD_LEAD, _no_record, _record, conductor_count, price_broken,
)


DRAFT_BRANCH = "TP1-15045-visual-workflow-diff-validation"


def _config(root: Path, **blocks) -> None:
    path = root / "qa-factory" / "config.json"
    cfg = json.loads(path.read_text(encoding="utf-8"))
    cfg.update(blocks)
    path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")


UI_REPO = {"repo_id": "testproject1-ui", "local_path": "app", "remote_identity": "git.example/tp1-group/testproject1-ui"}


def s0_source_list_clean() -> None:
    """The cmp2 shape: a list naming `testproject1-ui!1924` and a `ref`, given from ANOTHER folder than the project's
    (the driver changes into the project, so a relative path must have been made absolute first)."""
    from story_run_refusals_common import git_fixture
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        app, sha = git_fixture(root)
        _config(root, implementation_repos=[UI_REPO])
        sub = root / "where-the-person-stands"
        sub.mkdir()
        listed = f"# sources the person left out\ntestproject1-ui!1924 {EM} {DRAFT}\nbranch:{DRAFT_BRANCH} - the branch of that draft MR\n\n"
        (sub / "list.txt").write_bytes(listed.encode("utf-8"))
        out = harness.run_script("story_run.py", "--project", str(root), "--task", task, "--max-boundaries", "0",
                                 "--skip-sources", "list.txt", cwd=sub, env=env)
        eq("list_clean_writes_record_and_lines: S0 goes through: exit 0", out.returncode, 0, out.stdout[-1500:] + out.stderr[-800:])
        lines = [ln for ln in out.stdout.splitlines() if ln.startswith("Before the run you asked me not to read")]
        for line in lines:
            print("S0 console: " + line)
        eq("list_clean: one console line per exclusion", len(lines), 2, out.stdout[-800:])
        eq("list_clean: the line for the merge request, in the person's words", lines[0],
           f'Before the run you asked me not to read: testproject1-ui!1924 {EM} "{DRAFT}". Nothing of it is fetched; the source review '
           "and gate A list it.")
        check_in("list_clean: and for the branch", f"branch:{DRAFT_BRANCH}", lines[1])
        record = _record(task_root)
        eq("list_clean: the record holds both words, X1 and X2", [(e["id"], e["as_written"], e["target"]["kind"]) for e in record["exclusions"]],
           [("X1", "testproject1-ui!1924", "mr"), ("X2", f"branch:{DRAFT_BRANCH}", "ref")])
        eq("list_clean: the record's reason is the person's, whole", record["exclusions"][0]["reason"], DRAFT)
        eq("list_clean: C2: the head of the request was asked of the remote and is in the record",
           record["exclusions"][0]["target"]["head_sha"], sha["C"])
        eq("list_clean: the record holds the bytes that were read (list_sha256)", record["list_sha256"],
           hashlib.sha256(listed.encode("utf-8")).hexdigest())
        eq("list_clean: and where the list was read from (absolute: the driver moved to the project)",
           Path(record["list_file"]), (sub / "list.txt").resolve())
        state = s0_state(task_root)
        eq("list_clean: C5a: the flag is kept in the launch", state["launch"].get("skip_sources"), record["list_file"])
        check_eq = eq
        check_eq("list_clean: S0 is done", s0_pipeline(task_root)["stages"]["S0"]["status"], "done")
        findings = s0_findings(root)
        check("C5e: no finding per exclusion (an exclusion is the person's word, not a defect of ours) and no pass finding for a clean list",
              "source-exclusion" not in findings and "source_list" not in findings, findings[-400:])
        check_eq("list_clean: no conductor and no role was called", stub_calls(root), [])
        check("list_clean: nothing outward: the record lives under the story's work/ only",
              (task_root / "work" / "source-exclusions.json").is_file() and not list((root / "qa-factory").glob("*exclusion*")))
        check("list_clean: the pipeline carries no pass for the list (nothing was passed)",
              not any("list of sources" in w for w in s0_pipeline(task_root).get("warnings") or []))
    finally:
        harness.cleanup(root)


def s0_source_list_stops() -> None:
    """A missing file, 11 and 10 problem lines, `retry` after the file changed, and `go on`."""
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        listed = root / "list.txt"
        out = s0_run(root, env, task, "--skip-sources", str(listed))
        eq("list_missing_file_stops: exit 3", out.returncode, 3, out.stdout[-800:])
        ask = s0_question(task_root)
        check_in("list_missing: in the story's words - it cannot be opened", "I cannot open", ask)
        check_in("list_missing: the two doors", "`retry`", ask)
        check_in("list_missing: and `go on`", "`go on`", ask)
        eq("list_missing: the question obeys human-questions.md", rules_broken(ask), [])
        eq("list_missing: the block is remembered", s0_state(task_root).get("s0_block"), "source_list")
        check("list_missing: nothing was fetched and nothing written", not (task_root / "pipeline.json").exists() and _no_record(task_root))
        eq("list_missing: the launch keeps the flag for the entry that follows the answer",
           Path(s0_state(task_root).get("launch", {}).get("skip_sources")).resolve(), listed.resolve())
        out = s0_answer(root, env, task, "retry")
        eq("list_missing: `retry` with the file still missing asks again: exit 3", out.returncode, 3, out.stdout[-500:])

        junk = lambda n: [f"junk{i} {EM} not a source" for i in range(1, n + 1)]
        good = f"testproject1-ui!1924 {EM} {DRAFT}"
        listed.write_text("\n".join(junk(11) + [good]) + "\n", encoding="utf-8")
        out = s0_answer(root, env, task, "retry")
        eq("list_malformed_stops_10_and_11_lines: 11 problems: exit 3", out.returncode, 3, out.stdout[-500:])
        ask = s0_question(task_root)
        eq("list_malformed: 11 problems: ten are listed", len([ln for ln in ask.splitlines() if ln.startswith("- line ")]), 10)
        check_in("list_malformed: and the eleventh is 'and 1 more'", "- and 1 more (all of them are in the file named below)", ask)
        check_in("list_malformed: the fix and the `go on` that applies what could be read", "start the story with the lines I could read", ask)
        check_in("list_malformed: one line of the list is usable", "1 line of the list I can use", ask)
        check_in("list_malformed: all of them are in the details file", "line 11:",
                 (task_root / "state" / "driver-question-details.md").read_text(encoding="utf-8"))
        eq("list_malformed: the question obeys human-questions.md", rules_broken(ask), [])
        listed.write_text("\n".join(junk(10) + [good]) + "\n", encoding="utf-8")
        out = s0_answer(root, env, task, "retry")
        ask = s0_question(task_root)
        eq("list_malformed: 10 problems: exit 3, all ten listed", (out.returncode, len([ln for ln in ask.splitlines() if ln.startswith("- line ")])), (3, 10))
        check_not_in("list_malformed: and no 'and N more'", "more (all of them", ask)
        check_not_in("list_malformed: the file was re-read on `retry` (the 11th line is no longer a problem)", "line 11:", ask)

        out = s0_answer(root, env, task, "go on")
        eq("list_go_on_applies_valid_only: `go on` starts the story: exit 0", out.returncode, 0, out.stdout[-1500:] + out.stderr[-600:])
        record = _record(task_root)
        eq("list_go_on: only the line that read is applied", [(e["as_written"], e["line"]) for e in record["exclusions"]],
           [("testproject1-ui!1924", 11)])
        check("list_go_on: the pass is on the record as the person's word",
              any("list of sources not to read passed by the person's word" in w for w in s0_pipeline(task_root)["warnings"]),
              str(s0_pipeline(task_root)["warnings"]))
        check("list_go_on: and filed as a finding, once (the S0 pass machinery)", s0_findings(root).count("s0-pass:QA-1:source_list") <= 1
              and "source_list passed by the person's word" in s0_findings(root), s0_findings(root)[-600:])
        eq("list_go_on: no conductor", stub_calls(root), [])
    finally:
        harness.cleanup(root)


def s0_source_list_kinds() -> None:
    """C5 (c)(d): `go on` applies the lines whose TARGET read, even with no reason or a reason that starts like a
    target; a separator makes the reason a reason; the story's own ticket and a bare `!N` are never applied."""
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        listed = root / "list.txt"
        listed.write_text("\n".join([
            "testproject1-ui!1924",                                                # 1: no reason
            "testproject1-ui!1881 TP1-13289 - x",                              # 2: a reason that starts like a target
            f"QA-1 {EM} the ticket itself",                                   # 3: the story's own ticket
            f"testproject1-ui!1700 {EM} testproject1-ui!1701 was the old one",          # 4: the separator makes it a reason
            f"!4243 {EM} no project",                                         # 5: bare !N
            f"TP1-99 {EM} fine",                                          # 6
            f"1234abcd {EM} a commit id shorter than 12 characters",          # 7: could name other commits (C2)
        ]) + "\n", encoding="utf-8")
        out = s0_run(root, env, task, "--skip-sources", str(listed))
        eq("list_ticket_itself_stops: exit 3", out.returncode, 3, out.stdout[-800:])
        ask = s0_question(task_root)
        eq("list_kinds: five problems are listed", len([ln for ln in ask.splitlines() if ln.startswith("- line ")]), 5, ask)
        check_in("list_kinds: C2: a commit id shorter than 12 characters is a problem, never a match", "line 7:", ask)
        check_in("list_ticket_itself_stops: the ticket itself is named as one", "line 3:", ask)
        check_in("list_kinds: the bare `!N` asks for its project", "line 5:", ask)
        check_not_in("list_kinds: line 4 is no problem (the separator was there)", "line 4:", ask)
        check_in("list_kinds: four of the seven lines are usable (the ones whose target read)", "4 lines of the list I can use", ask)
        eq("list_kinds: the question obeys human-questions.md", rules_broken(ask), [])
        out = s0_answer(root, env, task, "go on")
        eq("list_kinds: `go on`: exit 0", out.returncode, 0, out.stdout[-1500:] + out.stderr[-600:])
        rows = [(e["as_written"], e["reason"]) for e in _record(task_root)["exclusions"]]
        eq("list_kinds: applied are the lines whose target read, in line order, with the reasons whole", rows, [
            ("testproject1-ui!1924", ""), ("testproject1-ui!1881", "TP1-13289 - x"), ("testproject1-ui!1700", "testproject1-ui!1701 was the old one"),
            ("TP1-99", "fine")])
        check("list_kinds: the story's own ticket and the bare !N are in no exclusion",
              not any(e["as_written"] in ("QA-1", "!4243") for e in _record(task_root)["exclusions"]))
        check("list_kinds: C2: no checkout is configured, and that is PRINTED for each merge request (the word is kept without a head)",
              out.stdout.count("no local checkout of `testproject1-ui` is configured") == 3, out.stdout[-900:])
        check("list_kinds: the heads stay null", all(e["target"].get("head_sha") is None
                                                     for e in _record(task_root)["exclusions"] if e["target"]["kind"] == "mr"))
    finally:
        harness.cleanup(root)


def s0_source_list_mr_flag() -> None:
    """F10 / C5b: `--mr` naming a merge request the list leaves out is its own question, `read` or `skip`."""
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        listed = root / "list.txt"
        listed.write_text(f"testproject1-ui!1924 {EM} {DRAFT}\n", encoding="utf-8")
        out = s0_run(root, env, task, "--skip-sources", str(listed), "--mr", "!1924")
        eq("list_mr_flag_conflict_stops: a bare --mr !N equal to the word's number: exit 3", out.returncode, 3, out.stdout[-800:])
        ask = s0_question(task_root)
        check_in("list_mr_flag: the question names both words", "testproject1-ui!1924", ask)
        check_in("list_mr_flag: its own two doors", "`read`", ask)
        check_in("list_mr_flag: (b)", "`skip`", ask)
        check_not_in("list_mr_flag: never `go on` - the two words of one person do not resolve silently", "`go on`", ask)
        eq("list_mr_flag: the question obeys human-questions.md", rules_broken(ask), [])
        check("list_mr_flag: nothing was written before the answer", _no_record(task_root) and not (task_root / "pipeline.json").exists())
        set_control(root, NO_USABLE)
        out = s0_answer(root, env, task, "go on", "--mr", "!1924")
        asked = s0_question(task_root)
        check_in("list_mr_flag: `go on` is not one of its answers: asked again, changed (the one lead, then the question as it was)",
                 'Your answer "go on" ' + UNREAD_LEAD, asked)
        check("list_mr_flag: ... with its own two doors as priced option lines, and `go on` offered nowhere",
              "`read` — " in asked and "`skip` — " in asked and "`go on`" not in asked.split("## What each answer costs and does")[-1]
              and price_broken(asked) == [], asked[-700:])
        eq("list_mr_flag: ... after exactly one conductor call (D-0041)", conductor_count(root), 1)
        out = s0_answer(root, env, task, "`skip`", "--mr", "!1924")
        eq("list_mr_flag: `skip`: the story goes on: exit 0", out.returncode, 0, out.stdout[-1500:] + out.stderr[-600:])
        eq("list_mr_flag: `skip`: the word stays", [e["as_written"] for e in _record(task_root)["exclusions"]], ["testproject1-ui!1924"])
        launch = s0_state(task_root)["launch"]
        check("list_mr_flag: `skip` drops the flag (kept apart, so the scout's launch flags do not show it)",
              "mr" not in launch and launch.get("mr_dropped") == "!1924", str(launch))
    finally:
        harness.cleanup(root)
    root, task_root, env = s0_project(task)
    try:
        listed = root / "list.txt"
        listed.write_text(f"testproject1-ui!1924 {EM} {DRAFT}\n", encoding="utf-8")
        out = s0_run(root, env, task, "--skip-sources", str(listed), "--mr",
                     "https://git.example/tp1-group/testproject1-ui/-/merge_requests/1924")
        eq("list_mr_flag: the same request as a link: exit 3", out.returncode, 3, out.stdout[-500:])
        out = s0_answer(root, env, task, "read", "--mr", "https://git.example/tp1-group/testproject1-ui/-/merge_requests/1924")
        eq("list_mr_flag: `read`: exit 0", out.returncode, 0, out.stdout[-1500:] + out.stderr[-600:])
        eq("list_mr_flag: `read`: its line of the list is not applied", _record(task_root)["exclusions"], [])
        check_in("list_mr_flag: and the person is told so", "you chose to read it, so its line of the list is not applied", out.stdout)
        check_not_in("list_mr_flag: not 'the list names no source', which would be untrue", "the list names no source", out.stdout)
        check("list_mr_flag: `read` keeps the flag", s0_state(task_root)["launch"].get("mr", "").endswith("/1924"))
    finally:
        harness.cleanup(root)


def s0_source_list_inventory() -> None:
    """C1: the flag on a story whose inventory exists is a question, never a line in passing - at S0 (no
    pipeline.json yet) and after S0; a resume WITHOUT the flag is unchanged; with no inventory the flag prints."""
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        listed = root / "list.txt"
        listed.write_text(f"testproject1-ui!1924 {EM} {DRAFT}\n", encoding="utf-8")
        (task_root / "work").mkdir(parents=True)
        inventory = task_root / "work" / "source-inventory.json"
        inventory.write_text(json.dumps({"schema_version": 1, "sources": []}), encoding="utf-8")
        out = s0_run(root, env, task, "--skip-sources", str(listed))
        eq("list_flag_with_inventory_asks (at S0): exit 3", out.returncode, 3, out.stdout[-800:])
        ask = s0_question(task_root)
        check_in("list_flag_with_inventory: says the sources were already collected", "were already collected on", ask)
        check_in("list_flag_with_inventory: and what a person can do now: name them at the source review", "source review", ask)
        check_in("list_flag_with_inventory: the one door is `go on`", "`go on`", ask)
        check_not_in("list_flag_with_inventory: `retry` is no door here (the file changes nothing)", "`retry`", ask)
        eq("list_flag_with_inventory: the question obeys human-questions.md", rules_broken(ask), [])
        check("list_flag_with_inventory: nothing is written", _no_record(task_root) and not (task_root / "pipeline.json").exists())
        check_in("list_flag_with_inventory: option (b) is the `stop` door, as a priced option line",
                 "(b) `stop` — stop here and start the story again from a fresh copy", ask)
        eq("list_flag_with_inventory: every option has its three price lines", price_broken(ask), [])
        out = s0_answer(root, env, task, "stop")
        eq("list_flag_with_inventory: `stop` holds the question: exit 3", out.returncode, 3, out.stdout[-800:])
        held = s0_question(task_root)
        check_in("list_flag_with_inventory: the first line says nothing runs", "You said to stop. Nothing runs and nothing is spent.", held)
        check_in("list_flag_with_inventory: and the question is the same one", "were already collected on", held)
        check("list_flag_with_inventory: stop: the block is open, no words kept, nothing written, no conductor",
              s0_state(task_root).get("s0_block") == "source_list" and "S0" not in (s0_state(task_root).get("pending_words") or {})
              and _no_record(task_root) and not (task_root / "pipeline.json").exists() and stub_calls(root) == [])
        out = s0_answer(root, env, task, "go on")
        eq("list_flag_with_inventory: `go on`: the list is ignored and S0 goes through: exit 0", out.returncode, 0,
           out.stdout[-1200:] + out.stderr[-500:])
        check_in("list_flag_with_inventory: and says so", "the list of sources not to read is ignored for this story", out.stdout)
        check("list_flag_with_inventory: still no record", _no_record(task_root))
        check("list_flag_with_inventory: the pass is on the pipeline's warnings",
              any("list of sources not to read passed by the person's word" in w for w in s0_pipeline(task_root)["warnings"]))

        # S0 is over and the inventory is there: the same flag on a command line is the same question (C1)
        out = s0_run(root, env, task, "--skip-sources", str(listed))
        eq("list_flag_after_s0 (inventory exists): exit 3, not a line in passing", out.returncode, 3, out.stdout[-800:])
        eq("list_flag_after_s0: the block is the same one", s0_state(task_root).get("s0_block"), "source_list")
        check_in("list_flag_after_s0: the same question", "were already collected on", s0_question(task_root))
        out = s0_answer(root, env, task, "stop")
        eq("list_flag_after_s0: `stop` is read by `skip_sources_late` (S0 is over): the question is held, exit 3", out.returncode, 3, out.stdout[-800:])
        check_in("list_flag_after_s0: with the first line that says nothing runs", "You said to stop. Nothing runs and nothing is spent.", s0_question(task_root))
        eq("list_flag_after_s0: the block is still `source_list` and no conductor was called",
           (s0_state(task_root).get("s0_block"), stub_calls(root)), ("source_list", []))
        out = s0_answer(root, env, task, "go on")
        eq("list_flag_after_s0: `go on` is read (no conductor): exit 0", out.returncode, 0, out.stdout[-800:] + out.stderr[-400:])
        check_not_in("list_flag_after_s0: no conductor was called", "conductor", json.dumps(stub_calls(root)))
        eq("list_flag_after_s0: the block is closed", s0_state(task_root).get("s0_block"), None)
        check("list_flag_after_s0: still no record, and the answer is on the pipeline's warnings",
              _no_record(task_root) and any("passed by the person's word" in w for w in s0_pipeline(task_root)["warnings"]))
        out = s0_run(root, env, task, "--skip-sources", str(listed))
        eq("list_flag_after_s0: asked and answered once: the same flag again asks nothing", out.returncode, 0, out.stdout[-600:])
        out = s0_run(root, env, task)
        eq("a resume WITHOUT the flag is unchanged: exit 0, no question", out.returncode, 0, out.stdout[-600:])
        check_not_in("a resume without the flag says nothing about the list", "list of sources", out.stdout)

        # no inventory yet: one printed line, nothing written (the list is read only when a story starts)
        inventory.unlink()
        out = s0_run(root, env, task, "--skip-sources", str(listed))
        eq("list_flag_after_s0 (no inventory): exit 0", out.returncode, 0, out.stdout[-600:])
        check_in("list_flag_after_s0_prints_only: the line says it is read only when a story starts",
                 "is read only when a story starts; this story started", out.stdout)
        check_in("list_flag_after_s0_prints_only: and names the door", "at the source review, name the sources to leave out", out.stdout)
        check("list_flag_after_s0_prints_only: nothing is written and nothing is asked", _no_record(task_root)
              and s0_state(task_root).get("s0_block") is None)
    finally:
        harness.cleanup(root)


def s0_source_list_units() -> None:
    """The pieces of P4 in this process: the head lookup (C2) and what it prints when it fails, the `--mr`
    comparison, and the entries' merge."""
    import contextlib
    import io
    import os
    import subprocess
    import story_run
    from story_run_refusals_common import git_fixture
    check_eq = eq
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        app, sha = git_fixture(root)
        _config(root, implementation_repos=[UI_REPO, {"repo_id": "testproject1", "local_path": "app",
                                                      "remote_identity": "git.example/tp1-group/testproject1"}])
        driver = driver_for(root, env, task)
        check_eq("C2: one ask of the remote, ten seconds at most", story_run.Driver.LS_REMOTE_SECONDS, 10)

        def head(project="tp1-group/testproject1-ui", iid="1924"):
            entry = {"as_written": f"{project.rsplit('/', 1)[-1]}!{iid}", "target": {"kind": "mr", "host": None, "project": project,
                                                                                      "iid": iid, "head_sha": None, "branch": None}}
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                driver.s0_resolve_head(entry)
            return entry["target"]["head_sha"], out.getvalue()

        check_eq("C2: ls-remote against the local bare remote resolves the head commit", head()[0], sha["C"])
        value, printed = head(iid="999")
        check("C2: a request the remote does not list: no head, printed, the word is kept",
              value is None and "could not be looked up" in printed and "holds by the number" in printed, printed)
        value, printed = head(project="tp1-group/unknown-repo")
        check("C2: no checkout of that project: no head, printed", value is None and "no local checkout of `unknown-repo`" in printed, printed)
        check_eq("C2: the tail is compared WHOLE: `testproject1` is not `testproject1-ui` (its own entry answers for it)",
                 driver.repo_of_project("tp1-group/testproject1")[0], "testproject1")
        check_eq("C2: and the ui project finds the ui entry", driver.repo_of_project("testproject1-ui")[0], "testproject1-ui")

        # B-231 fix 3: a `branch:` word is resolved to the commit of that branch on the remote, in the same way
        subprocess.run(["git", "-C", str(app), "branch", "feature/x", sha["B"]], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(app), "push", "-q", "origin", "feature/x"], check=True, capture_output=True)

        def branch_sha(name, d=None):
            entry = {"as_written": f"branch:{name}", "target": {"kind": "ref", "sha": None, "branch": name}}
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                (d or driver).s0_resolve_branch(entry)
            return entry["target"]["sha"], out.getvalue()

        check_eq("branch word: a branch of the remote resolves to its commit", branch_sha("feat")[0], sha["C"])
        check_eq("branch word: a name with a slash is passed as refs/heads/feature/x", branch_sha("feature/x")[0], sha["B"])
        value, printed = branch_sha("nope")
        check("branch word: a branch the remote does not list: no commit, one line, the word kept",
              value is None and "could not be looked up" in printed and "holds by the branch name" in printed, printed)
        value, printed = branch_sha("x")
        check("branch word: the last segment of another branch's name (`x` of `feature/x`) is not that branch",
              value is None and "could not be looked up" in printed, printed)
        entry = {"as_written": "a" * 12, "target": {"kind": "ref", "sha": "a" * 40, "branch": None}}
        with contextlib.redirect_stdout(io.StringIO()):
            driver.s0_resolve_branch(entry)
        check_eq("branch word: a commit word is left as it is", entry["target"]["sha"], "a" * 40)
        # two repositories that keep different commits under one branch name: in doubt, no commit
        git_env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
        remote2, app2 = root / "remote2.git", root / "app2"
        for args in (["init", "-q", "--bare", str(remote2)], ["init", "-q", str(app2)]):
            subprocess.run(["git", *args], check=True, capture_output=True)
        for args in (["checkout", "-q", "-b", "feat"], ["remote", "add", "origin", str(remote2)]):
            subprocess.run(["git", "-C", str(app2), *args], check=True, capture_output=True)
        (app2 / "other.txt").write_text("other", encoding="utf-8")
        for args in (["add", "-A"], ["commit", "-q", "-m", "another repository"], ["push", "-q", "origin", "feat"]):
            subprocess.run(["git", "-C", str(app2), *args], check=True, capture_output=True, env=git_env)
        _config(root, implementation_repos=[UI_REPO, {"repo_id": "other", "local_path": "app2", "remote_identity": "x/other"}])
        driver_two = driver_for(root, env, task)
        value, printed = branch_sha("feat", driver_two)
        check("branch word: two repositories with different commits under one name: no commit, printed",
              value is None and "different commit" in printed, printed)
        check_eq("branch word: a name only one of the two repositories lists resolves to that one", branch_sha("feature/x", driver_two)[0], sha["B"])
        _config(root, implementation_repos=[UI_REPO, {"repo_id": "testproject1", "local_path": "app",
                                                      "remote_identity": "git.example/tp1-group/testproject1"}])
        # the wiring: S0 writes the record with the commit of the branch word (not only a helper that nobody calls)
        import source_exclusions as SE
        text_word = f"branch:feat {EM} the branch of that draft MR\n".encode("utf-8")
        entries_word, _p = SE.parse_bytes(text_word, task)
        with contextlib.redirect_stdout(io.StringIO()):
            driver.s0_write_list(SE, entries_word, "w.txt", text_word)
        check_eq("branch word: S0 writes the record with the commit of the branch (it is wired in, not just written)",
                 SE.read_record(task_root / "work")["exclusions"][0]["target"]["sha"], sha["C"])

        driver.LS_REMOTE_SECONDS = 0.001
        value, printed = head()
        check("C2: a remote that does not answer in time: printed, no head, the word kept",
              value is None and "did not answer within" in printed, printed)
        value, printed = branch_sha("feat")
        check("branch word: a remote that does not answer in time: printed, no commit, the word kept",
              value is None and "did not answer within" in printed and "holds by the branch name" in printed, printed)
        driver.LS_REMOTE_SECONDS = 10
        subprocess.run(["git", "-C", str(app), "remote", "set-url", "origin", str(root / "no-such-remote.git")], check=True, capture_output=True)
        value, printed = head()
        check("C2: a remote that fails: printed with its own words, no head", value is None and "could not be looked up (" in printed, printed)
        value, printed = branch_sha("feat")
        check("branch word: a remote that fails: printed with its own words, no commit", value is None and "could not be looked up (" in printed, printed)
        subprocess.run(["git", "-C", str(app), "remote", "remove", "origin"], check=True, capture_output=True)
        value, printed = branch_sha("feat")
        check("branch word: no remote at all in the implementation repository: no commit, printed, never a refusal",
              value is None and "could not be looked up (" in printed, printed)

        # s0_write_list: one record per list. The same bytes on a later S0 entry are a no-op (no second head lookup);
        # other bytes (the person edited the file between two stops) REPLACE an unrevoked record - S0 is the only
        # writer and nothing has been read yet, so the `--load` refusal for "another list" does not apply here;
        # a record that holds a revocation is kept and the person is told.
        import source_exclusions as SE
        asked = []
        driver.s0_resolve_head = lambda entry: asked.append(entry["as_written"])
        text_a, text_b = f"testproject1-ui!1924 {EM} first\n".encode("utf-8"), f"testproject1-ui!1881 {EM} second\n".encode("utf-8")
        entries_a, _p = SE.parse_bytes(text_a, task)
        entries_b, _p = SE.parse_bytes(text_b, task)
        shown = io.StringIO()
        with contextlib.redirect_stdout(shown):
            driver.s0_write_list(SE, entries_a, "a.txt", text_a)
            driver.s0_write_list(SE, entries_a, "a.txt", text_a)
        check_eq("s0_write_list: the same bytes twice: one write, one head lookup, one console line",
                 (asked, shown.getvalue().count("Before the run you asked me not to read")), (["testproject1-ui!1924"], 1))
        with contextlib.redirect_stdout(io.StringIO()):
            driver.s0_write_list(SE, entries_b, "b.txt", text_b)
        record = SE.read_record(task_root / "work")
        check_eq("s0_write_list: other bytes replace an unrevoked record (no ListRefused, no stale word)",
                 ([e["as_written"] for e in record["exclusions"]], record["list_sha256"]),
                 (["testproject1-ui!1881"], hashlib.sha256(text_b).hexdigest()))
        SE.revoke(task_root, "X1", "I want it read after all")
        shown = io.StringIO()
        with contextlib.redirect_stdout(shown):
            driver.s0_write_list(SE, entries_a, "a.txt", text_a)
        check("s0_write_list: a record that holds a revocation is kept as it is, and the person is told",
              SE.read_record(task_root / "work")["list_sha256"] == hashlib.sha256(text_b).hexdigest()
              and "holds a word you took back" in shown.getvalue(), shown.getvalue())

        # mr_conflicts: F10 / C5b
        entries = [{"as_written": "testproject1-ui!1924", "target": {"kind": "mr", "host": None, "project": "testproject1-ui", "iid": "1924"}, "reason": "x"},
                   {"as_written": "TP1-9", "target": {"kind": "ticket", "key": "TP1-9", "host": None}, "reason": "y"}]
        hit = lambda value: [e["as_written"] for e in story_run.Driver.mr_conflicts(value, entries)]
        check_eq("mr_conflicts: a bare !N equal by number", hit("!1924"), ["testproject1-ui!1924"])
        check_eq("mr_conflicts: a bare number with no bang", hit("1924"), ["testproject1-ui!1924"])
        check_eq("mr_conflicts: leading zeros are the same number", hit("!01924"), ["testproject1-ui!1924"])
        check_eq("mr_conflicts: the link of the same request", hit("https://git.example/tp1-group/testproject1-ui/-/merge_requests/1924"),
                 ["testproject1-ui!1924"])
        check_eq("mr_conflicts: the short form of the same request", hit("tp1-group/testproject1-ui!1924"), ["testproject1-ui!1924"])
        check_eq("mr_conflicts: another number is no conflict", hit("!19"), [])
        check_eq("mr_conflicts: a number inside a longer number is no conflict", hit("!19240"), [])
        check_eq("mr_conflicts: another project's short form is no conflict", hit("testproject1!1924"), [])
        check_eq("mr_conflicts: another request's link is no conflict", hit("https://git.example/tp1-group/testproject1-ui/-/merge_requests/1881"), [])
        check_eq("mr_conflicts: a ticket word is no merge request", hit("TP1-9"), [])

        # merge_list_entries: the same thing named twice keeps every reason and every line
        clean = [{"line": 3, "as_written": "testproject1-ui!1924", "target": dict(entries[0]["target"]), "reason": "first"}]
        loose = [{"line": 7, "as_written": "testproject1-ui!1924", "target": dict(entries[0]["target"]), "reason": "second"},
                 {"line": 1, "as_written": "TP1-9", "target": dict(entries[1]["target"]), "reason": ""}]
        merged = story_run.Driver.merge_list_entries(clean, loose)
        check_eq("merge_list_entries: line order, one entry per thing", [e["as_written"] for e in merged], ["TP1-9", "testproject1-ui!1924"])
        check_eq("merge_list_entries: both reasons and both lines are kept", (merged[1]["reason"], merged[1]["line"]), ("first | second", [3, 7]))
        check_eq("merge_list_entries: the clean entry passed in is not changed", clean[0]["reason"], "first")
    finally:
        harness.cleanup(root)


def s0_excluded_heads() -> None:
    """B-231 fix 3: `excluded_heads` holds only real commits. A null head (the lookup failed) is no head - it
    once became the word 'None' and `git_route` ran a rev-parse of it for every commit it listed."""
    import source_exclusions as SE
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        driver = driver_for(root, env, task)
        check_eq = eq
        check_eq("excluded_heads_null_head: no record: no heads", driver.excluded_heads(), [])
        one, two = "a" * 40, "b" * 40

        def write(text, heads):
            entries, problems = SE.parse_bytes(text.encode("utf-8"), task)
            check_eq("excluded_heads fixture: the list reads clean", problems, [])
            for entry in entries:
                if entry["target"]["kind"] == "mr":
                    entry["target"]["head_sha"] = heads.get(entry["as_written"])
            record = SE.record_path(task_root / "work")
            if record.exists():
                record.unlink()
            SE.write_record(task_root, entries, "list.txt", text.encode("utf-8"))

        write(f"testproject1-ui!1924 {EM} a\n", {"testproject1-ui!1924": None})
        check_eq("excluded_heads_null_head: a merge request whose head is null gives no head at all", driver.excluded_heads(), [])
        write(f"{two} {EM} a commit\n", {})
        check_eq("excluded_heads_null_head: a commit word gives its commit", driver.excluded_heads(), [two])
        write(f"testproject1-ui!1924 {EM} a\nbranch:feat {EM} b\ntestproject1-ui!1881 {EM} c\n",
              {"testproject1-ui!1924": None, "testproject1-ui!1881": one})
        check_eq("excluded_heads_null_head: a branch word with no commit (still null) and a null head are skipped, the real head stays",
                 driver.excluded_heads(), [one])
        write(f"testproject1-ui!1924 {EM} a\ntestproject1-ui!1881 {EM} b\n{two} {EM} c\ntestproject1-ui!1700 {EM} d\nbranch:feat {EM} e\n",
              {"testproject1-ui!1924": None, "testproject1-ui!1881": one, "testproject1-ui!1700": one})
        heads = driver.excluded_heads()
        check_eq("excluded_heads_null_head: in record order, a head shared by two requests once, never the word 'None'",
                 (heads, "None" in heads), ([one, two], False))
    finally:
        harness.cleanup(root)


def s0_source_list_texts() -> None:
    """B-231 fixes 4 and 6: what the two questions say is what `go on` does (FR-10), and the question of a story
    whose source review is over does not promise that review."""
    import source_exclusions as SE
    import story_run
    check_eq = eq
    task = "QA-1"
    root, task_root, env = s0_project(task)
    try:
        driver = driver_for(root, env, task)

        def ask(text):
            listed = root / "q-list.txt"
            listed.write_text(text, encoding="utf-8")
            try:
                driver.s0_source_list({"skip_sources": str(listed), "mr": None})
            except story_run.Person as person:
                return person.text
            return ""

        no_reason = "testproject1-ui!1924\n"
        unread = f"junk {EM} not a source\n"
        a, b, c = ask(no_reason), ask(unread), ask(no_reason + unread + f"TP1-99 {EM} fine\n")
        check_eq("list_no_reason_text: (a) a line with a target and no reason: it IS applied on `go on`, and the question says so",
                 ("1 line names a source I can read but has a problem" in a, "applied anyway and the problem is noted" in a,
                  "no source I can read" in a), (True, True, False))
        check_eq("list_no_reason_text: (b) a line whose target could not be read: it is NOT applied, and the question says so",
                 ("1 line names no source I can read: it is not applied" in b, "applied anyway" in b), (True, False))
        check_eq("list_no_reason_text: (c) both groups, each with its own count",
                 ("1 line names no source I can read: it is not applied" in c,
                  "1 line names a source I can read but has a problem" in c, "2 lines of the list I can use" in c), (True, True, True))
        # (`no_how_to_answer` is the block `ask()` appends under the text; this reads the text before it)
        body_problems = lambda text: [r for r in rules_broken(text) if r != "no_how_to_answer"]
        check_eq("list_no_reason_text: the questions obey human-questions.md", [body_problems(t) for t in (a, b, c)], [[], [], []])
        many = "".join(f"junk{i} {EM} x\n" for i in range(11)) + "testproject1-ui!1\ntestproject1-ui!2\n"
        d = ask(many)
        check_eq("list_no_reason_text: the counts are of ALL the lines, the list shown is capped at ten",
                 (len([ln for ln in d.splitlines() if ln.startswith("- line ")]), "11 lines name no source I can read" in d,
                  "2 lines name a source I can read but have a problem" in d), (10, True, True))
        check_eq("list_no_reason_text: the `go on` door is unchanged", ("`retry`" in a, "`go on`" in a), (True, True))

        # fix 6: the list after the inventory exists
        inventory = task_root / "work" / "source-inventory.json"
        inventory.parent.mkdir(parents=True, exist_ok=True)
        inventory.write_text(json.dumps({"schema_version": 1, "sources": []}), encoding="utf-8")

        def too_late():
            try:
                driver.s0_list_too_late()
            except story_run.Person as person:
                return person.text, person.details
            return "", ""

        open_text, open_details = too_late()
        check_in("list_too_late_after_s1: S1 still open: the source review is promised (today's text)", "at the source review", open_text)
        check_eq("list_too_late_after_s1: S1 still open: no details file", open_details, "")
        state = task_root / "state"
        state.mkdir(parents=True, exist_ok=True)
        (state / "controller.json").write_text(json.dumps({"stages": {"S1": {"status": "completed"}}}), encoding="utf-8")
        done_text, done_details = too_late()
        check("list_too_late_after_s1: S1 completed: the text differs", done_text != open_text)
        check_not_in("list_too_late_after_s1: S1 completed: the review is not promised", "at the source review", done_text)
        check_in("list_too_late_after_s1: and it says nothing already read is un-read", "Nothing that was already read is un-read", done_text)
        check_in("list_too_late_after_s1: and where the person's word can still go: gate A, in their own words", "at gate A", done_text)
        check_in("list_too_late_after_s1: the `go on` door is still there, as a priced option line", "(a) `go on` — the story goes on and the list is ignored", done_text)
        check_in("list_too_late_after_s1: and the 'start again from a fresh copy' option is now the `stop` door (it had none)",
                 "(b) `stop` — stop here and start the story again from a fresh copy", done_text)
        check_in("list_too_late_after_s1: with the sentence that a list is read only when a story starts", "a list is read only when a story starts", done_text)
        check_eq("list_too_late_after_s1: every option has its three price lines", price_broken(done_text), [])
        check_eq("list_too_late_after_s1: the doors the next answer reads are `go on` and `stop`", sorted(driver.state["s0_ask"]["doors"]), ["go on", "stop"])
        check_eq("list_too_late_after_s1: S1 completed: the question obeys human-questions.md (no script, no flag in its body)",
                 body_problems(done_text), [])
        check_in("list_too_late_after_s1: the exact command that records the person's word is in the details file - the remark door "
                 "(C1-4b: the conductor never records a gate decision, I6)", f"waiver.py --task {driver.task} --remark --stage S0", done_details)
        check_not_in("list_too_late_after_s1: and it no longer sends the conductor to the gate decision", "--operation gate-decision", done_details)
        original = SE.s1_completed

        def broken(_task_root):
            raise ValueError("pipeline unreadable")
        SE.s1_completed = broken
        try:
            raised_text, _d = too_late()
        finally:
            SE.s1_completed = original
        check_eq("list_too_late_after_s1: a pipeline that cannot be read is not 'completed': today's text", raised_text, open_text)
    finally:
        harness.cleanup(root)


def main() -> None:
    run_scenarios(
        [
        s0_source_list_clean,
        s0_source_list_stops,
        s0_source_list_kinds,
        s0_source_list_mr_flag,
        s0_source_list_inventory,
    ],
        [
        s0_source_list_units,
        s0_excluded_heads,
        s0_source_list_texts,
    ],
    )
    harness.finish("test_story_run_s0_source_list")


# split: runner piece 1
if __name__ == "__main__":
    main()
