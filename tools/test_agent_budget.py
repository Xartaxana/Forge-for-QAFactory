"""Tests for tools/agent_budget.py: fixture transcripts as small JSONL under tmp_path, the hook run as
a subprocess (exit code + stdout + stderr), the sidecar folder moved to tmp_path by AGENT_BUDGET_DIR.

Run from the repo root: python -m pytest tools/test_agent_budget.py -q
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import agent_budget  # noqa: E402

SCRIPT = Path(__file__).resolve().parent / "agent_budget.py"


def _assistant(ctx: int, tool_id: str = "toolu_x", command: str = "") -> str:
    block = {"type": "tool_use", "id": tool_id, "name": "Bash" if command else "Read",
             "input": {"command": command} if command else {"file_path": "x"}}
    usage = {"input_tokens": 2, "cache_creation_input_tokens": 1000,
             "cache_read_input_tokens": ctx - 1002, "output_tokens": 5}
    return json.dumps({"type": "assistant", "message": {"usage": usage, "content": [block]}})


def _write(path: Path, lines: list) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


class Session:
    """A main transcript plus a subagents folder under tmp_path."""

    def __init__(self, tmp_path: Path):
        self.tmp = tmp_path
        self.main = tmp_path / "proj" / "sess.jsonl"
        self.sub = tmp_path / "proj" / "sess" / "subagents"
        self.env = {"AGENT_BUDGET_DIR": str(tmp_path / "side")}

    def run(self, payload: dict, **env):
        payload = {"transcript_path": str(self.main), "cwd": str(self.tmp), "tool_name": "Read",
                   "tool_input": {}, **payload}
        full = {**os.environ, **self.env, **{k: str(v) for k, v in env.items()}}
        return subprocess.run([sys.executable, str(SCRIPT)], input=json.dumps(payload), capture_output=True,
                              text=True, encoding="utf-8", env=full)

    def worker(self, agent_id: str, lines: list) -> Path:
        return _write(self.sub / ("agent-%s.jsonl" % agent_id), lines)


@pytest.fixture
def ses(tmp_path):
    return Session(tmp_path)


def _ctx_of(result) -> str:
    return json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]


def test_below_thresholds_silent(ses):
    _write(ses.main, [_assistant(100000)])
    ses.worker("w1", [_assistant(100000)])
    for payload in ({}, {"agent_id": "w1"}):
        r = ses.run(payload)
        assert (r.returncode, r.stdout, r.stderr) == (0, "", "")


def test_worker_warn_at_250k_names_the_number_once(ses):
    _write(ses.main, [_assistant(1000000)])
    ses.worker("w1", [_assistant(250000)])
    r = ses.run({"agent_id": "w1"})
    assert r.returncode == 0
    assert "worker context is 250000 tokens" in _ctx_of(r)
    assert ses.run({"agent_id": "w1"}).stdout == ""


def test_worker_stop_blocks_edit_of_a_code_file(ses):
    ses.worker("w1", [_assistant(400000)])
    r = ses.run({"agent_id": "w1", "tool_name": "Edit", "tool_input": {"file_path": "tools/x.py"}})
    assert r.returncode == 2
    for part in ("400000", "cap is 400000", "commit the work in progress", "write your report", "SubagentHandback",
                 "relaunches a fresh agent"):
        assert part in r.stderr
    assert r.stdout == ""
    assert ses.run({"agent_id": "w1", "tool_name": "Read"}).returncode == 2


@pytest.mark.parametrize("tool,tool_input", [
    ("SubagentHandback", {"message": "done"}),
    ("Bash", {"command": "git commit -m \"wip text, done\""}),
    ("Bash", {"command": "  git add tools/x.py"}),
    ("Bash", {"command": "git commit -F docs/tasks/specs/reports/msg.txt"}),
    ("PowerShell", {"command": "git status"}),
    ("Bash", {"command": "git diff --stat"}),
    ("Bash", {"command": "git stash"}),
    ("Write", {"file_path": os.path.join("{tmp}", "docs", "tasks", "specs", "reports", "t-1-report.md")}),
    ("Edit", {"file_path": "docs/tasks/handoffs/x.md"}),
    pytest.param("Write", {"file_path": "docs\\tasks\\handoffs\\x.md"},
                 marks=pytest.mark.skipif(os.name != "nt", reason="a backslash path is a Windows path; on POSIX "
                                                                  "it is one file name outside the folder (CI 7883762)")),
])
def test_worker_stop_lets_the_close_out_moves_through(ses, tool, tool_input):
    ses.worker("w1", [_assistant(450000)])
    tool_input = {k: v.replace("{tmp}", str(ses.tmp)) if isinstance(v, str) else v for k, v in tool_input.items()}
    r = ses.run({"agent_id": "w1", "tool_name": tool, "tool_input": tool_input})
    assert r.returncode == 0, r.stderr


@pytest.mark.parametrize("tool,tool_input", [
    ("Bash", {"command": "git status && rm -rf x"}),
    ("Bash", {"command": "git status; python evil.py"}),
    ("Bash", {"command": "git commit -m \"wip; a && b\""}),
    ("Bash", {"command": "git add tools/x.py && git commit -m wip"}),
    ("Bash", {"command": "git commit -m \"$(rm x)\""}),
    ("Bash", {"command": "git commit -m $MSG"}),  # a bare variable: only the `$` in the class refuses it
    ("Bash", {"command": "git commit -m `rm x`"}),
    ("Bash", {"command": "git log"}),
    ("Bash", {"command": "git statusx"}),
    ("Bash", {"command": ""}),
    ("Bash", {"command": None}),
    # the five bypasses of t-576 F2
    ("Bash", {"command": "git status \\\"; rm -rf x; echo \\\""}),
    ("Bash", {"command": "git add <(rm -rf x)"}),
    ("PowerShell", {"command": "git status (Remove-Item x)"}),
    ("PowerShell", {"command": "git status\rRemove-Item x"}),
    ("Bash", {"command": "git diff --stat > tools/agent_budget.py"}),
    # a heredoc message and a second line
    ("Bash", {"command": "git commit -F - <<'EOF'\nmsg\nEOF"}),
    ("Bash", {"command": "git status\nrm -rf x"}),
    ("Write", {"file_path": "docs/tasks/handoffs/../../../tools/x.py"}),
    ("Write", {"file_path": "docs/tasks/handoffs/../../x.md"}),
    ("Write", {"file_path": "elsewhere/docs/tasks/handoffs/x.md"}),
    ("Write", {"file_path": os.path.join("{tmp}", "..", "elsewhere", "docs", "tasks", "handoffs", "evil.py")}),
    ("Write", {"file_path": "docs/tasks/other/x.md"}),
    ("Write", {"file_path": "docs/tasks/handoffs"}),
    ("Write", {"file_path": None}),
    ("NotebookEdit", {"notebook_path": "docs/tasks/handoffs/x.ipynb"}),
])
def test_worker_stop_still_blocks_the_rest(ses, tool, tool_input):
    ses.worker("w1", [_assistant(450000)])
    tool_input = {k: v.replace("{tmp}", str(ses.tmp)) if isinstance(v, str) else v for k, v in tool_input.items()}
    r = ses.run({"agent_id": "w1", "tool_name": tool, "tool_input": tool_input})
    assert r.returncode == 2
    if tool in ("Bash", "PowerShell"):
        assert "one plain git command, no shell syntax" in r.stderr


def test_stop_cap_is_the_exact_boundary(ses):
    ses.worker("w1", [_assistant(399999)])
    assert ses.run({"agent_id": "w1", "tool_name": "Edit", "tool_input": {"file_path": "x.py"}}).returncode == 0


def test_main_warn_at_300k_and_again_only_at_350k(ses):
    _write(ses.main, [_assistant(310000)])
    first = ses.run({})
    assert "main session context is 310000 tokens" in _ctx_of(first)
    assert ses.run({}).stdout == ""
    _write(ses.main, [_assistant(349999)])
    assert ses.run({}).stdout == ""
    _write(ses.main, [_assistant(350000)])
    assert "350000 tokens" in _ctx_of(ses.run({}))


def test_main_warn_after_a_drop_arms_again(ses):
    _write(ses.main, [_assistant(310000)])
    ses.run({})
    _write(ses.main, [_assistant(100000)])
    assert ses.run({}).stdout == ""
    _write(ses.main, [_assistant(310000)])
    assert "310000" in _ctx_of(ses.run({}))


def test_ten_test_runs_warn_once_and_waits_reported(ses):
    cmds = ["python -m pytest tools/ -q"] * 9 + ["sleep 30", "python scripts/selftest.py --fast"]
    _write(ses.main, [_assistant(50000, "t%d" % i, c) for i, c in enumerate(cmds)])
    r = ses.run({})
    ctx = _ctx_of(r)
    assert "10 test runs, 1 waits" in ctx
    assert ses.run({}).stdout == ""
    side = json.loads((Path(ses.env["AGENT_BUDGET_DIR"]) / "sess.json").read_text(encoding="utf-8"))
    assert side["offset"] == ses.main.stat().st_size


def test_test_runs_count_incrementally_and_repeat_per_step(ses):
    lines = [_assistant(50000, "t%d" % i, "python -m unittest") for i in range(9)]
    _write(ses.main, lines)
    assert ses.run({}).stdout == ""
    lines += [_assistant(50000, "u%d" % i, "pytest -q") for i in range(5)]
    _write(ses.main, lines)
    assert "14 test runs" in _ctx_of(ses.run({}))
    lines.append(_assistant(50000, "z", "echo hi"))
    _write(ses.main, lines)
    assert ses.run({}).stdout == ""


def test_unparsable_or_stale_sidecar_is_rebuilt(ses):
    _write(ses.main, [_assistant(50000, "t%d" % i, "pytest") for i in range(10)])
    side = Path(ses.env["AGENT_BUDGET_DIR"]) / "sess.json"
    side.parent.mkdir(parents=True)
    side.write_text("{not json", encoding="utf-8")
    assert "10 test runs" in _ctx_of(ses.run({}))
    side.write_text(json.dumps({"offset": 10 ** 9, "tests": 0, "waits": 0, "ctx_level": 0, "tests_level": 0}))
    assert "10 test runs" in _ctx_of(ses.run({}))  # rebuilt from scratch: counted again, not 0
    assert json.loads(side.read_text(encoding="utf-8"))["tests"] == 10


@pytest.mark.parametrize("extra", [{}, {"agent_id": None}, {"agent_id": ""}, {"tool_use_id": "toolu_w1"}])
def test_no_agent_id_measures_the_main_transcript_even_with_a_fresh_worker_over_stop(ses, extra):
    """t-576 F1: a call without agent_id is the MAIN session's; a fresh worker file at 450K is not its business."""
    _write(ses.main, [_assistant(10000)])
    ses.worker("w1", [_assistant(450000, "toolu_w1")])  # just written: fresh by mtime, last tool_use id too
    r = ses.run({"tool_name": "Edit", "tool_input": {"file_path": "x.py"}, **extra})
    assert (r.returncode, r.stdout, r.stderr) == (0, "", "")
    _write(ses.main, [_assistant(310000)])
    assert "main session context is 310000 tokens" in _ctx_of(ses.run({**extra}))  # the main one is what is read


def test_main_session_is_never_stopped_even_over_the_cap(ses):
    _write(ses.main, [_assistant(900000)])
    r = ses.run({"tool_name": "Edit", "tool_input": {"file_path": "x.py"}})
    assert r.returncode == 0 and "main session context" in _ctx_of(r)


def test_stop_survives_a_newest_line_longer_than_the_tail(ses):
    """t-576 F4: the usage is kept in the sidecar, so a 70 KB last line never leaves the context unknown.
    Since F6-7 (t-840) the tail itself reaches back over a short line before the long one (the window grows
    until the newline before the last line, and the chunk read is as long as the window): the sidecar `ctx`
    is what answers only when MORE than the 64 KB window of other lines follows the usage line."""
    edit = {"agent_id": "w1", "tool_name": "Edit", "tool_input": {"file_path": "x.py"}}
    big_user = json.dumps({"type": "user", "message": {"content": "y" * 70000}})
    ses.worker("w1", [_assistant(450000), big_user])
    assert agent_budget.context_size(ses.sub / "agent-w1.jsonl") == 450000  # the tail SEES it now (F6-7)
    assert ses.run(edit).returncode == 2
    user30 = json.dumps({"type": "user", "message": {"content": "y" * 30000}})
    ses.worker("w3", [_assistant(450000), user30, user30, user30])
    assert agent_budget.context_size(ses.sub / "agent-w3.jsonl") is None  # 90 KB of other lines: the tail misses it
    assert ses.run({**edit, "agent_id": "w3"}).returncode == 2  # the sidecar's ctx does
    big_assistant = _assistant(450000, "toolu_big", "echo " + "z" * 70000)  # the usage sits INSIDE the long line
    ses.worker("w2", [_assistant(100, "toolu_a"), big_assistant])
    assert ses.run({**edit, "agent_id": "w2"}).returncode == 2


def test_the_last_usage_comes_from_the_newer_of_tail_and_sidecar(ses):
    ses.worker("w1", [_assistant(450000)])
    edit = {"agent_id": "w1", "tool_name": "Edit", "tool_input": {"file_path": "x.py"}}
    assert ses.run(edit).returncode == 2
    side = json.loads((Path(ses.env["AGENT_BUDGET_DIR"]) / "agent-w1.json").read_text(encoding="utf-8"))
    assert side["ctx"] == 450000
    with open(ses.sub / "agent-w1.jsonl", "a", encoding="utf-8") as fh:
        fh.write(_assistant(120000) + "\n")  # the worker was compacted: the newer line wins
    assert ses.run(edit).returncode == 0


@pytest.mark.parametrize("content", ["[1, 2]", '{"offset": "abc"}', '{"tests": null}', '{"offset": -5}',
                                     '{"ctx": 1.5, "offset": 0}', '"text"'])
def test_a_mistyped_sidecar_is_rebuilt_and_the_hook_stays_alive(ses, content):
    """t-576 F9: a sidecar of the wrong shape must not turn the hook off for good."""
    _write(ses.main, [_assistant(50000, "t%d" % i, "pytest") for i in range(10)])
    side = Path(ses.env["AGENT_BUDGET_DIR"]) / "sess.json"
    side.parent.mkdir(parents=True)
    side.write_text(content, encoding="utf-8")
    r = ses.run({}, AGENT_BUDGET_DEBUG="1")
    assert r.returncode == 0 and "failed open" not in r.stderr
    assert "10 test runs" in _ctx_of(r)
    assert json.loads(side.read_text(encoding="utf-8"))["tests"] == 10


def test_is_finished_reads_the_last_assistant_tool_use(tmp_path):
    def call(name):
        return json.dumps({"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "t", "name": name,
                                                                         "input": {}}]}})
    tail = json.dumps({"type": "user", "message": {"content": [{"type": "tool_result", "content": "ok"}]}})
    done = _write(tmp_path / "done.jsonl", [call("Read"), call("SubagentHandback"), tail])
    live = _write(tmp_path / "live.jsonl", [call("SubagentHandback"), call("Bash"), tail])  # a later call: live
    empty = _write(tmp_path / "empty.jsonl", ["{}", "garbage"])
    assert (agent_budget.is_finished(done), agent_budget.is_finished(live), agent_budget.is_finished(empty)) == (
        True, False, False)


def test_agent_id_without_its_file_is_silent_not_the_main_transcript(ses):
    _write(ses.main, [_assistant(900000)])
    r = ses.run({"agent_id": "nope"})
    assert (r.returncode, r.stdout) == (0, "")
    assert ses.run({"agent_id": "../x"}).returncode == 0


def test_fail_open_cases(ses):
    for stdin in ("", "{broken", "[1, 2]"):
        r = subprocess.run([sys.executable, str(SCRIPT)], input=stdin, capture_output=True, text=True,
                           env={**os.environ, **ses.env})
        assert (r.returncode, r.stdout, r.stderr) == (0, "", "")
    assert ses.run({"transcript_path": str(ses.tmp / "missing.jsonl")}).stdout == ""
    assert ses.run({"transcript_path": 5}).returncode == 0
    _write(ses.main, ['{"type": "user"}', "garbage", ""])
    r = ses.run({})
    assert (r.returncode, r.stdout, r.stderr) == (0, "", "")


def test_debug_env_prints_one_line_on_a_failure(ses):
    bad = json.dumps({"type": "assistant", "message": {"usage": {"input_tokens": "abc"}}})
    _write(ses.main, [bad])
    assert ses.run({}).stderr == ""
    r = ses.run({}, AGENT_BUDGET_DEBUG="1")
    assert r.returncode == 0 and r.stdout == ""
    assert r.stderr.count("\n") == 1 and "failed open" in r.stderr


def test_env_overrides_the_thresholds(ses):
    _write(ses.main, [_assistant(5000)])
    assert "5000 tokens" in _ctx_of(ses.run({}, AGENT_BUDGET_MAIN_WARN=4000))


def test_context_size_reads_only_the_tail(tmp_path):
    big = {"type": "user", "message": {"content": "x" * 200000}}
    f = _write(tmp_path / "t.jsonl", [json.dumps(big), _assistant(123456)])
    assert agent_budget.context_size(f) == 123456
    g = _write(tmp_path / "u.jsonl", [_assistant(123456), json.dumps(big), json.dumps(big)])
    assert agent_budget.context_size(g) is None  # beyond the window and not the last line
    h = _write(tmp_path / "v.jsonl", [_assistant(123456), json.dumps(big)])
    assert agent_budget.context_size(h) == 123456  # F6-7: the line before the long last one comes along


@pytest.mark.parametrize("folder", ["docs/tasks/specs/reviews", "docs/tasks/specs", "docs/tasks/handoffs",
                                    "docs/tasks/specs/reports"])
def test_stop_lets_a_report_into_every_role_folder_of_handoff_dirs(tmp_path, folder):
    target = os.path.join(str(tmp_path), *folder.split("/"), "t-1.md")
    assert agent_budget.stop_allows("Write", {"file_path": target}, str(tmp_path)) is True
    assert agent_budget.stop_allows("Edit", {"file_path": target}, str(tmp_path)) is True
    assert agent_budget.stop_allows("Write", {"file_path": target}, str(tmp_path / "elsewhere")) is False


def test_stop_still_refuses_beside_the_report_folders(tmp_path):
    for bad in ("docs/tasks/other/x.md", "docs/tasks/x.md", "docs/x.md", "tools/x.py", "docs/tasks/specs"):
        assert agent_budget.stop_allows("Write", {"file_path": os.path.join(str(tmp_path), *bad.split("/"))},
                                        str(tmp_path)) is False, bad


def test_allowed_dirs_is_the_two_report_folders_plus_handoff_dirs():
    import dispatch_manifest

    assert agent_budget.ALLOWED_DIRS[:2] == ("docs/tasks/handoffs", "docs/tasks/specs/reports")
    assert set(agent_budget.ALLOWED_DIRS) == {"docs/tasks/handoffs", "docs/tasks/specs/reports"} | set(
        dispatch_manifest.HANDOFF_DIRS.values())
    assert len(agent_budget.ALLOWED_DIRS) == len(set(agent_budget.ALLOWED_DIRS))


def test_stop_message_names_the_handoff_line_and_keeps_the_old_folders():
    msg = agent_budget.stop_message(450000, 400000)
    assert "handoff: line of your dispatch" in msg
    assert "docs/tasks/handoffs/" in msg and "docs/tasks/specs/reports/" in msg


def test_stop_message_tells_a_reading_worker_where_its_report_goes():
    msg = agent_budget.stop_message(450000, 400000)
    assert ("a reading worker at STOP writes its report to the `handoff:` path of its dispatch; with no "
            "`handoff:` path the final message is the report") in msg


def _tools_copy(tmp_path, manifest_source=None, transcripts_source=None):
    """A COPY of agent_budget.py + transcripts.py in tmp_path; dispatch_manifest.py there only when given;
    transcripts_source (when given) replaces the copied transcripts.py."""
    tools = Path(__file__).resolve().parent
    for name in ("agent_budget.py", "transcripts.py"):
        (tmp_path / name).write_bytes((tools / name).read_bytes())
    if manifest_source is not None:
        (tmp_path / "dispatch_manifest.py").write_text(manifest_source, encoding="utf-8")
    if transcripts_source is not None:
        (tmp_path / "transcripts.py").write_text(transcripts_source, encoding="utf-8")
    return tmp_path


def _import_probe(folder):
    probe = "import agent_budget; print(agent_budget.ALLOWED_DIRS == agent_budget._REPORT_DIRS)"
    return subprocess.run([sys.executable, "-c", probe], capture_output=True, text=True, encoding="utf-8",
                          cwd=str(folder), env={**os.environ, "PYTHONPATH": ""})


def test_an_absent_dispatch_manifest_is_silent_and_keeps_the_two_folders(tmp_path):
    """ImportError (the module is simply not beside the hook) is the plain case: no stderr at all."""
    r = _import_probe(_tools_copy(tmp_path))
    assert r.returncode == 0 and r.stdout.strip() == "True", r.stderr
    assert r.stderr == ""
    hook = subprocess.run([sys.executable, str(tmp_path / "agent_budget.py")], input=json.dumps(
        {"tool_name": "Read", "tool_input": {}, "cwd": str(tmp_path)}), capture_output=True, text=True,
        encoding="utf-8", env={**os.environ, "AGENT_BUDGET_DIR": str(tmp_path / "side")})
    assert (hook.returncode, hook.stdout, hook.stderr) == (0, "", "")


@pytest.mark.parametrize("source, exc_name", [("def broken(:\n", "SyntaxError"),
                                              ("raise RuntimeError('boom')\n", "RuntimeError")])
def test_a_broken_dispatch_manifest_keeps_the_hook_alive_with_the_two_folders(tmp_path, source, exc_name):
    """A SyntaxError / a runtime error in dispatch_manifest.py (a COPY of the tools in tmp_path) is not an
    ImportError: the hook must still import, keep the two report folders and say so in one stderr line."""
    r = _import_probe(_tools_copy(tmp_path, source))
    assert r.returncode == 0 and r.stdout.strip() == "True", r.stderr
    assert r.stderr.count("\n") == 1 and "dispatch_manifest.py did not import (%s)" % exc_name in r.stderr
    hook = subprocess.run([sys.executable, str(tmp_path / "agent_budget.py")], input=json.dumps(
        {"tool_name": "Read", "tool_input": {}, "cwd": str(tmp_path)}), capture_output=True, text=True,
        encoding="utf-8", env={**os.environ, "AGENT_BUDGET_DIR": str(tmp_path / "side")})
    assert hook.returncode == 0


# --- t-844 F6-9: transcripts that is absent or BROKEN must not switch the cost gate off in silence ----------

BROKEN_TRANSCRIPTS = [("def broken(:\n", "SyntaxError"), ("raise RuntimeError('boom')\n", "RuntimeError")]


def _hook_in(script, folder, stdin=None, **env):
    """The hook `script` run as the harness runs it; PYTHONPATH pinned so nothing outside `folder` shadows."""
    payload = {"tool_name": "Read", "tool_input": {}, "cwd": str(folder), "transcript_path": str(folder / "s.jsonl")}
    return subprocess.run([sys.executable, str(script)], input=json.dumps(payload) if stdin is None else stdin,
                          capture_output=True, text=True, encoding="utf-8",
                          env={**os.environ, "PYTHONPATH": "", "AGENT_BUDGET_DIR": str(folder / "side"), **env})


def _is_the_one_import_line(r, exc_name):
    lines = r.stderr.splitlines()
    assert len(lines) == 1 and "Traceback" not in r.stderr and len(lines[0]) <= 200, r.stderr
    assert "transcripts did not import (%s" % exc_name in lines[0]
    assert "no WARN/STOP possible" in lines[0]


@pytest.mark.parametrize("stdin", [None, "", "{broken"])
@pytest.mark.parametrize("source, exc_name", BROKEN_TRANSCRIPTS)
def test_a_broken_sibling_transcripts_keeps_the_hook_alive_with_one_loud_line(tmp_path, source, exc_name, stdin):
    """SyntaxError / an error at import in the sibling transcripts.py: exit 0, no stdout, ONE stderr line naming
    transcripts, no traceback -- whatever the stdin (no input / malformed JSON end in exit 0 as before)."""
    folder = _tools_copy(tmp_path, transcripts_source=source)
    r = _hook_in(folder / "agent_budget.py", folder, stdin)
    assert (r.returncode, r.stdout) == (0, "")
    _is_the_one_import_line(r, exc_name)


def test_a_broken_transcripts_means_no_warn_and_a_healthy_one_warns(tmp_path):
    """The off-switch is real (a 500K main session gets no WARN) and the NEGATIVE control is a healthy copy:
    the same payload warns and stderr is empty."""
    _write(tmp_path / "s.jsonl", [_assistant(500000)])
    ok_dir, bad_dir = tmp_path / "ok", tmp_path / "bad"
    ok_dir.mkdir()
    bad_dir.mkdir()
    healthy = _hook_in(_tools_copy(ok_dir) / "agent_budget.py", tmp_path)
    assert healthy.stderr == "" and "AGENT BUDGET WARN" in healthy.stdout
    broken = _hook_in(_tools_copy(bad_dir, transcripts_source="def broken(:\n") / "agent_budget.py", tmp_path)
    assert (broken.returncode, broken.stdout) == (0, "")
    _is_the_one_import_line(broken, "SyntaxError")


def test_a_long_multiline_import_error_is_still_one_short_line(tmp_path):
    folder = _tools_copy(tmp_path, transcripts_source="raise RuntimeError('x' * 500 + '\\nsecond line\\nthird')\n")
    r = _hook_in(folder / "agent_budget.py", folder)
    assert r.returncode == 0
    _is_the_one_import_line(r, "RuntimeError")


def test_a_missing_transcripts_is_silent(tmp_path):
    """transcripts ITSELF absent (the hook deployed alone in a folder) is the standalone case and stays silent:
    exit 0, empty stdout AND stderr (test_transcripts pins the same from its side)."""
    folder = _tools_copy(tmp_path)
    (folder / "transcripts.py").unlink()
    r = _hook_in(folder / "agent_budget.py", folder)
    assert (r.returncode, r.stdout, r.stderr) == (0, "", "")


def test_a_module_missing_inside_transcripts_is_loud(tmp_path):
    """A ModuleNotFoundError of ANOTHER module raised while importing transcripts (a broken dependency) is a
    broken module, not an absent one: the one loud line."""
    folder = _tools_copy(tmp_path, transcripts_source="import no_such_dependency_of_transcripts\n")
    r = _hook_in(folder / "agent_budget.py", folder)
    assert (r.returncode, r.stdout) == (0, "")
    _is_the_one_import_line(r, "ModuleNotFoundError")


@pytest.mark.parametrize("source, exc_name", BROKEN_TRANSCRIPTS)
def test_a_broken_package_style_transcripts_is_loud_too(tmp_path, source, exc_name):
    """tools.transcripts importable as a package but broken: PYTHONPATH holds <tmp>/tools/transcripts.py and
    the REAL hook runs -- the package-style branch catches it (no sibling retry of the same file)."""
    (tmp_path / "pkg" / "tools").mkdir(parents=True)
    (tmp_path / "pkg" / "tools" / "transcripts.py").write_text(source, encoding="utf-8")
    r = _hook_in(SCRIPT, tmp_path, PYTHONPATH=str(tmp_path / "pkg"))
    assert (r.returncode, r.stdout) == (0, "")
    _is_the_one_import_line(r, exc_name)


def test_a_missing_package_style_module_still_tries_the_sibling(tmp_path):
    """The inner invariant: no `tools` package beside the hook (ImportError) -> the sibling transcripts.py is
    the one used, silently (the healthy copy in the test above measures through it and warns)."""
    folder = _tools_copy(tmp_path)
    probe = "import agent_budget; print(agent_budget.transcripts.__file__)"
    r = subprocess.run([sys.executable, "-c", probe], capture_output=True, text=True, encoding="utf-8",
                       cwd=str(folder), env={**os.environ, "PYTHONPATH": ""})
    assert r.stderr == "" and Path(r.stdout.strip()).resolve() == (folder / "transcripts.py").resolve()


# --- GM1-8: the three branches of the transcript creation time (macOS birthtime, Windows ctime, Linux None) ----


class _St:
    def __init__(self, **kw):
        self.__dict__.update(kw)


def test_creation_time_branches(monkeypatch):
    assert agent_budget._creation_time(_St(st_birthtime=11.0, st_ctime=22.0)) == 11.0  # birthtime wins
    monkeypatch.setattr(agent_budget.os, "name", "nt")
    assert agent_budget._creation_time(_St(st_ctime=22.0)) == 22.0                     # Windows: ctime is creation
    monkeypatch.setattr(agent_budget.os, "name", "posix")
    assert agent_budget._creation_time(_St(st_ctime=22.0)) is None                     # Linux: unknown, not a crash


def test_sidecar_is_kept_when_creation_time_is_unknown(tmp_path, monkeypatch):
    """Linux, born = None: the stale-sidecar check is skipped, so counters are NOT reset on every turn."""
    transcript = tmp_path / "t.jsonl"
    transcript.write_text("x\n", encoding="utf-8")
    side = tmp_path / "s.json"
    side.write_text(json.dumps({"offset": 1, "tests": 7, "waits": 2, "ctx": 0, "ctx_level": 0, "tests_level": 0}),
                    encoding="utf-8")
    os.utime(side, (1, 1))  # older than the transcript: with a known birth time this would be rebuilt
    monkeypatch.setattr(agent_budget, "_creation_time", lambda st: None)
    assert agent_budget._load_sidecar(side, transcript)["tests"] == 7
    monkeypatch.setattr(agent_budget, "_creation_time", lambda st: st.st_mtime)
    assert agent_budget._load_sidecar(side, transcript)["tests"] == 0  # known and newer: rebuilt
