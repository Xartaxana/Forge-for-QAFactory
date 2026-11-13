"""Tests for tools/handoff_gate.py (t-744 F5-1 N3): a READING worker (critic, designer) writes exactly ONE
file, the path on the `handoff:` line of its dispatch. Fixtures: a worker transcript (the dispatch is its
first user line) and its sidecar meta under tmp_path; `transcript_path` of the payload points at the main
session file next to the `<session>/subagents/` folder, as the harness lays it out.

Run: python -m pytest tools/test_handoff_gate.py -q
"""

import io
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

TOOLS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS_DIR))

import dispatch_manifest as dm  # noqa: E402
import handoff_gate as hg  # noqa: E402
import md_regions  # noqa: E402

SCRIPT = TOOLS_DIR / "handoff_gate.py"
REVIEWS = "docs/tasks/specs/reviews"
SPECS = "docs/tasks/specs"
HANDOFFS = "docs/tasks/handoffs"


def _dispatch(handoff_block, owns=None):
    parts = ["Review the diff.", "given: docs/x.md"]
    if owns:
        parts.append("owns:\n" + owns)
    parts += ["non-goals: none", handoff_block, "edges: none -- x", "DoD: `python -m pytest -q`"]
    return "\n".join(parts) + "\n"


class Env:
    """A session folder under tmp_path with workers in its subagents folder."""

    def __init__(self, tmp_path: Path):
        self.tmp = tmp_path
        self.main = tmp_path / "proj" / "sess.jsonl"
        self.sub = tmp_path / "proj" / "sess" / "subagents"
        self.sub.mkdir(parents=True)

    def at(self, folder, name="t-1.md") -> str:
        return str(self.tmp / folder / name)

    def worker(self, kind, dispatch, agent_id="w1", raw=None):
        """kind None = no meta. raw = the exact bytes of the transcript (instead of one user line)."""
        f = self.sub / ("agent-%s.jsonl" % agent_id)
        if raw is not None:
            f.write_bytes(raw)
        else:
            f.write_text(json.dumps({"type": "user", "message": {"role": "user", "content": dispatch}}) + "\n",
                         encoding="utf-8")
        if kind is not None:
            (self.sub / ("agent-%s.meta.json" % agent_id)).write_text(json.dumps({"agentType": kind}),
                                                                      encoding="utf-8")

    def payload(self, file_path, tool="Write", agent_id="w1", cwd=None, **extra):
        p = {"session_id": "s", "transcript_path": str(self.main), "cwd": str(cwd or self.tmp),
             "tool_name": tool, "tool_input": {"file_path": file_path}}
        if agent_id is not None:
            p["agent_id"] = agent_id
        p.update(extra)
        return p


@pytest.fixture
def env(tmp_path):
    return Env(tmp_path)


def _critic(env, handoff_block=None, kind="critic"):
    block = handoff_block if handoff_block is not None else "handoff: %s -- the verdict file" % env.at(REVIEWS)
    env.worker(kind, _dispatch(block))


# --- who is never blocked ------------------------------------------------------------------------------------

@pytest.mark.parametrize("agent_id", [None, "", 7])
def test_main_thread_passes(env, agent_id):
    _critic(env)
    payload = env.payload("tools/x.py", agent_id=None)
    if agent_id is not None:
        payload["agent_id"] = agent_id
    assert hg.decide(payload) == (0, "")


def test_builder_passes(env):
    env.worker("builder", _dispatch("handoff: %s -- the report" % env.at(HANDOFFS)))
    assert hg.decide(env.payload(env.at("tools", "x.py"))) == (0, "")
    assert hg.decide(env.payload("tools/x.py", tool="Edit")) == (0, "")


@pytest.mark.parametrize("kind", ["scout", "judge", "Explore", "Plan", "general-purpose"])
def test_other_known_kinds_pass(env, kind):
    _critic(env, kind=kind)
    assert hg.decide(env.payload("tools/x.py"))[0] == 0


@pytest.mark.parametrize("tool", ["Read", "Bash", "Grep", "NotebookEdit", None])
def test_other_tools(env, tool):
    env.worker("critic", "")  # an unreadable-looking dispatch: still no business of this hook
    payload = env.payload("tools/x.py", tool=tool)
    assert hg.decide(payload) == (0, "")


def test_gated_kinds_are_in_the_folder_table_and_builder_is_not_gated():
    assert set(hg.GATED_KINDS) == {"critic", "designer"}
    assert set(hg.GATED_KINDS) <= set(dm.HANDOFF_DIRS)
    assert dm.HANDOFF_DIRS["critic"] == REVIEWS and dm.HANDOFF_DIRS["designer"] == SPECS
    assert dm.HANDOFF_DIRS["builder"] == HANDOFFS and dm.HANDOFF_DIRS["scout"] == "docs/tasks/specs/reports"


# --- the one path --------------------------------------------------------------------------------------------

def test_critic_own_path(env):
    _critic(env)
    own = env.at(REVIEWS)
    assert hg.decide(env.payload(own)) == (0, "")
    assert hg.decide(env.payload(own, tool="Edit")) == (0, "")  # E-16: the worker may rewrite its own file
    assert hg.decide(env.payload("docs/tasks/specs/reviews/t-1.md"))[0] == 0  # relative to cwd
    assert hg.decide(env.payload(env.at(REVIEWS + "/../reviews", "t-1.md")))[0] == 0  # `..` folded by realpath


@pytest.mark.skipif(os.name != "nt", reason="a case-insensitive file system")
def test_critic_own_path_in_another_case(env):
    _critic(env)
    assert hg.decide(env.payload(env.at(REVIEWS).upper()))[0] == 0


@pytest.mark.parametrize("tool", ["Write", "Edit"])
def test_critic_other_path(env, tool):
    _critic(env)
    for other in (env.at("tools", "x.py"), env.at(REVIEWS, "t-2.md"), env.at(REVIEWS, "sub/t-1.md")):
        code, msg = hg.decide(env.payload(other, tool=tool))
        assert code == 2
        assert msg.startswith("HANDOFF GATE: this critic worker may write only the one report file")
        assert "not the handoff path" in msg and env.at(REVIEWS) in msg  # the expected path is named
        assert "Door: put your whole report into your final message" in msg and "handback_extract.py" in msg
        assert "Refused: %s" % other in msg


def test_no_handoff_path(env):
    _critic(env, "handoff: report <= 500 words, no file")
    code, msg = hg.decide(env.payload(env.at(REVIEWS)))
    assert code == 2 and "no handoff path inside docs/tasks/specs/reviews in the dispatch" in msg
    _critic(env, "handoff: docs/tasks/specs/reviews/t-1.md (relative)")  # a relative path is no path (absolute only)
    assert hg.decide(env.payload(env.at(REVIEWS)))[0] == 2


def test_two_paths(env):
    a, b = env.at(REVIEWS, "t-1.md"), env.at(REVIEWS, "t-2.md")
    _critic(env, "handoff: %s and also %s" % (a, b))
    for target in (a, b):
        code, msg = hg.decide(env.payload(target))
        assert code == 2 and "names 2 handoff paths" in msg and a in msg and b in msg and "exactly one" in msg


def test_two_paths_on_the_line_under_the_header(env):
    a, b = env.at(REVIEWS, "t-1.md"), env.at(REVIEWS, "t-2.md")
    _critic(env, "handoff:\n%s\n%s" % (a, b))
    assert hg.decide(env.payload(a))[0] == 2


def test_one_path_on_the_line_under_the_header(env):
    a = env.at(REVIEWS, "t-1.md")
    _critic(env, "handoff:\n%s (new)" % a)
    assert hg.decide(env.payload(a)) == (0, "")


def test_path_outside_dir(env):
    code_file = env.at("tools", "x.py")
    _critic(env, "handoff: %s" % code_file)
    code, msg = hg.decide(env.payload(code_file))
    assert code == 2 and "no handoff path inside docs/tasks/specs/reviews" in msg
    _critic(env, "handoff: %s" % env.at(SPECS, "t-1.md"))  # the designer's folder is not the critic's
    assert hg.decide(env.payload(env.at(SPECS, "t-1.md")))[0] == 2


def test_an_outside_path_next_to_a_good_one_is_a_mention_not_a_second_path(env):
    good = env.at(REVIEWS)
    _critic(env, "handoff: %s -- not %s" % (good, env.at("tools", "x.py")))
    assert hg.decide(env.payload(good)) == (0, "")
    assert hg.decide(env.payload(env.at("tools", "x.py")))[0] == 2


def test_only_md(env):
    txt = env.at(REVIEWS, "t-1.txt")
    _critic(env, "handoff: %s" % txt)
    assert hg.decide(env.payload(txt))[0] == 2


def test_designer_subfolder(env):
    env.worker("designer", _dispatch("handoff: %s" % env.at(REVIEWS)))  # the critic's folder, under the designer's
    code, msg = hg.decide(env.payload(env.at(REVIEWS)))
    assert code == 2 and "no handoff path inside docs/tasks/specs in the dispatch" in msg
    env.worker("designer", _dispatch("handoff: %s" % env.at(SPECS, "t-744-draft.md")))
    assert hg.decide(env.payload(env.at(SPECS, "t-744-draft.md"))) == (0, "")
    assert hg.decide(env.payload(env.at(SPECS, "other.md")))[0] == 2


def test_folder_is_compared_by_trailing_segments_not_from_cwd(env):
    own = env.at(REVIEWS)  # a path in the main tree
    _critic(env)
    worktree = env.tmp / "worktrees" / "w"
    worktree.mkdir(parents=True)
    assert hg.decide(env.payload(own, cwd=worktree)) == (0, "")
    # and the same folder tail under another root is still the folder
    other_root = str(env.tmp / "elsewhere" / REVIEWS / "t-9.md")
    _critic(env, "handoff: %s" % other_root)
    assert hg.decide(env.payload(other_root, cwd=worktree)) == (0, "")


def test_quoted_handoff(env):
    own = env.at(REVIEWS)
    _critic(env, "```\nhandoff: %s\n```" % own)
    code, msg = hg.decide(env.payload(own))
    assert code == 2 and "no handoff path" in msg
    _critic(env, "> handoff: %s" % own)
    assert hg.decide(env.payload(own))[0] == 2
    _critic(env, "handoff:\n> %s" % own)  # a quoted continuation line is not read either
    assert hg.decide(env.payload(own))[0] == 2


def test_placeholder(env):
    _critic(env, "handoff: %s" % os.path.join(str(env.tmp), "docs", "tasks", "specs", "reviews", "<t>-review.md"))
    assert hg.decide(env.payload(env.at(REVIEWS, "<t>-review.md")))[0] == 2


# --- what cannot be read is a refusal, never a pass ----------------------------------------------------------

def test_unreadable_dispatch(env):
    reason = "the dispatch text could not be read"
    env.worker("critic", None, raw=b"")  # 0 bytes
    code, msg = hg.decide(env.payload(env.at(REVIEWS)))
    assert code == 2 and reason in msg and "Door: put your whole report" in msg
    env.worker("critic", None, raw=b'{"type": "assistant", "message": {"content": "x"}}\nnot json\n')  # no user line
    assert hg.decide(env.payload(env.at(REVIEWS))) [0] == 2
    env.worker("critic", None, raw=b'{"type": "user", "message": {"content": 5}}\n')  # a content of no known type
    assert hg.decide(env.payload(env.at(REVIEWS)))[0] == 2
    assert hg.decide(env.payload(env.at(REVIEWS), agent_id="nobody"))[0] == 2  # no transcript file at all
    assert hg.decide(env.payload(env.at(REVIEWS), transcript_path=None))[0] == 2  # nothing to compose it from
    assert hg.decide(env.payload(env.at(REVIEWS), agent_id="../w1"))[0] == 2  # an unsafe id composes no path


def test_degraded_cut(env):
    own = env.at(REVIEWS)
    filler = "x" * (md_regions.MAX_TEXT_CHARS + 10)
    env.worker("critic", _dispatch("handoff: %s" % own) + filler)
    code, msg = hg.decide(env.payload(own))
    assert code == 2 and "the dispatch text could not be read" in msg


# --- an unknown kind (F-6 B) ---------------------------------------------------------------------------------

def test_unknown_kind_with_an_owns_path_is_a_writing_worker(env):
    env.worker(None, _dispatch("handoff: report", owns=env.at("tools", "x.py")))
    assert hg.decide(env.payload(env.at("tools", "x.py"))) == (0, "")


def test_unknown_kind_without_owns_is_gated_like_a_reader(env):
    own = env.at(REVIEWS)
    env.worker(None, _dispatch("handoff: %s" % own))
    assert hg.decide(env.payload(own)) == (0, "")
    code, msg = hg.decide(env.payload(env.at("tools", "x.py")))
    assert code == 2 and "not the handoff path" in msg
    env.worker(None, _dispatch("handoff: report"))
    code, msg = hg.decide(env.payload(env.at("tools", "x.py")))
    assert code == 2 and "no handoff path" in msg and "re-send the dispatch with an owns: line" in msg


@pytest.mark.parametrize("owns", ["tools/x.py\ntools/y.py", "tools/*.py"])
def test_unknown_kind_with_only_relative_owns_paths_is_a_reader_locked_to_its_handoff(env, owns):
    """t-855 (F6-8), the class's one rule: a relative path is no owns declaration (dispatch_manifest's absolute-only
    reader), so a worker of unknown kind whose owns holds relative paths only is a READER. The parallel-writer limit
    of dispatch_gate answers the same (test_dispatch_gate: the same dispatch is not counted)."""
    own = env.at(REVIEWS)
    env.worker(None, _dispatch("handoff: %s" % own, owns=owns))
    assert hg.decide(env.payload(own)) == (0, "")  # its one handoff file
    code, msg = hg.decide(env.payload(env.at("tools", "x.py")))
    assert code == 2 and "not the handoff path" in msg
    code, msg = hg.decide(env.payload("tools/x.py", tool="Edit"))
    assert code == 2 and "not the handoff path" in msg


def test_unknown_kind_with_an_absolute_owns_path_before_a_relative_one_is_a_writer(env):
    text = _dispatch("handoff: report", owns=env.at("tools", "y.py") + "\ntools/x.py")
    env.worker(None, text)
    assert dm.has_owned_paths(text) is True
    assert hg.decide(env.payload(env.at("tools", "x.py"))) == (0, "")


def test_unknown_kind_unreadable_dispatch_names_the_resend_door(env):
    env.worker(None, None, raw=b"")
    code, msg = hg.decide(env.payload(env.at("tools", "x.py")))
    assert code == 2 and "the dispatch text could not be read" in msg
    assert "re-send the dispatch with an owns: line" in msg


def test_a_bad_meta_is_an_unknown_kind(env):
    env.worker("critic", _dispatch("handoff: report"))
    (env.sub / "agent-w1.meta.json").write_text("{not json", encoding="utf-8")
    assert hg.decide(env.payload(env.at("tools", "x.py")))[0] == 2


# --- main(): the error direction -----------------------------------------------------------------------------

class _Stdin:
    def __init__(self, data: bytes):
        self.buffer = io.BytesIO(data)

    def isatty(self):
        return False


def _run_main(monkeypatch, payload_bytes):
    monkeypatch.setattr(sys, "stdin", _Stdin(payload_bytes))
    return hg.main()


def test_main_exception(env, monkeypatch, capsys):
    def boom(_payload):
        raise ValueError("boom")

    monkeypatch.setattr(hg, "decide", boom)
    worker = json.dumps(env.payload("tools/x.py")).encode()
    assert _run_main(monkeypatch, worker) == 2
    err = capsys.readouterr().err
    assert err.startswith("HANDOFF GATE:") and "the dispatch text could not be read" in err and "ValueError" in err
    assert err.count("\n") == 1  # one line
    edit = json.dumps(env.payload("tools/x.py", tool="Edit")).encode()
    assert _run_main(monkeypatch, edit) == 2
    assert "Refused: tools/x.py --" in capsys.readouterr().err
    for harmless in (env.payload("tools/x.py", agent_id=None), env.payload("tools/x.py", tool="Read"),
                     env.payload("tools/x.py", agent_id="")):
        assert _run_main(monkeypatch, json.dumps(harmless).encode()) == 0
    assert capsys.readouterr().err == ""


def test_main_broken_imports_refuse_a_worker(env, monkeypatch, capsys):
    monkeypatch.setattr(hg, "transcripts", None)
    assert _run_main(monkeypatch, json.dumps(env.payload("tools/x.py")).encode()) == 2
    assert "HANDOFF GATE" in capsys.readouterr().err
    assert _run_main(monkeypatch, json.dumps(env.payload("tools/x.py", agent_id=None)).encode()) == 0


def test_a_broken_dispatch_manifest_import_never_blocks_a_builder(env, monkeypatch, capsys):
    """A builder that owns dispatch_manifest.py and leaves it unparseable must still be able to repair it."""
    env.worker("builder", _dispatch("handoff: %s -- the report" % env.at(HANDOFFS)))
    monkeypatch.setattr(hg, "dispatch_manifest", None)
    assert hg.decide(env.payload("tools/dispatch_manifest.py", tool="Edit")) == (0, "")
    assert _run_main(monkeypatch, json.dumps(env.payload("tools/dispatch_manifest.py", tool="Edit")).encode()) == 0
    assert capsys.readouterr().err == ""
    assert _run_main(monkeypatch, json.dumps(env.payload("tools/x.py", agent_id=None)).encode()) == 0


def test_a_dispatch_manifest_that_does_not_parse_still_lets_a_builder_write(env, tmp_path):
    """The real import path, on a COPY of the hook: dispatch_manifest.py with a SyntaxError next to it."""
    copy = tmp_path / "copy"
    copy.mkdir()
    for name in ("handoff_gate.py", "transcripts.py"):
        (copy / name).write_bytes((TOOLS_DIR / name).read_bytes())
    (copy / "dispatch_manifest.py").write_text("def broken(:\n", encoding="utf-8")
    ran = {}
    for kind, tool in (("builder", "Edit"), ("critic", "Write")):
        env.worker(kind, _dispatch("handoff: %s -- the report" % env.at(REVIEWS)), agent_id=kind)
        ran[kind] = subprocess.run([sys.executable, str(copy / "handoff_gate.py")], capture_output=True,
                                   text=True, encoding="utf-8", input=json.dumps(
                                       env.payload(env.at("tools", "dispatch_manifest.py"), tool=tool, agent_id=kind)))
    assert ran["builder"].returncode == 0 and ran["builder"].stderr == ""
    assert ran["critic"].returncode == 2 and "this critic worker" in ran["critic"].stderr


@pytest.mark.parametrize("kind", ["critic", "designer"])
def test_a_broken_dispatch_manifest_import_refuses_a_gated_worker_naming_its_kind(env, monkeypatch, capsys, kind):
    _critic(env, kind=kind)
    monkeypatch.setattr(hg, "dispatch_manifest", None)
    with pytest.raises(RuntimeError):
        hg.decide(env.payload("tools/x.py"))
    assert _run_main(monkeypatch, json.dumps(env.payload("tools/x.py")).encode()) == 2
    err = capsys.readouterr().err
    assert err.startswith("HANDOFF GATE: this %s worker may write" % kind) and "Door:" in err


def test_the_exception_refusal_names_the_workers_kind_or_says_unidentified(env, monkeypatch, capsys):
    def boom(_payload):
        raise ValueError("boom")

    monkeypatch.setattr(hg, "decide", boom)
    _critic(env, kind="designer")
    assert _run_main(monkeypatch, json.dumps(env.payload("tools/x.py")).encode()) == 2
    assert capsys.readouterr().err.startswith("HANDOFF GATE: this designer worker may write")
    assert _run_main(monkeypatch, json.dumps(env.payload("tools/x.py", agent_id="nobody")).encode()) == 2
    err = capsys.readouterr().err
    assert err.startswith("HANDOFF GATE: this unidentified worker may write") and "reading" not in err


def test_one_path_in_two_spellings_counts_once(env):
    """A doubled separator is one path (a `..` inside the folder part is no candidate at all: _in_folder)."""
    own = env.at(REVIEWS)
    other_spelling = os.path.join(str(env.tmp), "docs", "tasks", "specs") + os.sep + os.sep + "reviews" + os.sep + "t-1.md"
    assert other_spelling != own
    env.worker("critic", _dispatch("handoff: %s -- the verdict, also %s" % (own, other_spelling)))
    assert hg.decide(env.payload(own)) == (0, "")
    other = env.at(REVIEWS, "t-2.md")  # a genuinely different path still counts as a second one
    env.worker("critic", _dispatch("handoff: %s -- the verdict, also %s" % (own, other)))
    code, msg = hg.decide(env.payload(own))
    assert code == 2 and "names 2 handoff paths" in msg


@pytest.mark.skipif(os.name != "nt", reason="a case-insensitive file system with both slashes")
def test_one_path_in_a_case_and_slash_spelling_counts_once(env):
    own = env.at(REVIEWS)
    env.worker("critic", _dispatch("handoff: %s -- the verdict, also %s" % (own, own.upper().replace("\\", "/"))))
    assert hg.decide(env.payload(own)) == (0, "")


@pytest.mark.parametrize("raw", [b"", b"not json", b"[1, 2]", b"\xff\xfe", b'"str"', b"null"])
def test_main_garbage_stdin_is_a_pass(monkeypatch, raw):
    assert _run_main(monkeypatch, raw) == 0


# --- the hook as a script (the form the harness runs) -------------------------------------------------------

def _script(payload, **env_extra):
    return subprocess.run([sys.executable, str(SCRIPT)], input=json.dumps(payload), capture_output=True, text=True,
                          encoding="utf-8", env={**os.environ, **env_extra})


def test_script_dry_run(env):
    _critic(env)
    ok = _script(env.payload(env.at(REVIEWS)))
    assert ok.returncode == 0 and ok.stderr == "" and ok.stdout == ""
    bad = _script(env.payload(env.at("tools", "x.py")))
    assert bad.returncode == 2 and bad.stderr.startswith("HANDOFF GATE: this critic worker")
    assert env.at(REVIEWS) in bad.stderr and "Door:" in bad.stderr
    assert _script(env.payload("tools/x.py", agent_id=None)).returncode == 0
    assert _script({"tool_name": "Write"}).returncode == 0


def test_script_refusal_with_a_non_ascii_path_still_exits_2(env):
    _critic(env)
    bad = _script(env.payload(env.at("tools", "отчёт.py")), PYTHONIOENCODING="ascii")
    assert bad.returncode == 2 and "HANDOFF GATE" in bad.stderr


def test_handoff_candidates_one_path_in_two_spellings_is_one_pair_with_its_first_folder(env):
    """h1 (F6-37): the one candidate loop of the write gate, dod_gate and the launch check."""
    a = env.at(REVIEWS)
    b = a.replace("\\", "/").replace("/docs/tasks/", "/docs/tasks/../tasks/")  # the same file, another spelling
    other = env.at(HANDOFFS, "t-2.md")
    cut = dm.section_cut("handoff: %s %s %s\n" % (a, b, other))
    base = str(env.tmp)
    assert hg.handoff_candidates(cut, [REVIEWS, HANDOFFS], base) == [(a, REVIEWS), (other, HANDOFFS)]
    assert hg.handoff_candidates(cut, [SPECS], base) == []  # a direct child only
    assert hg.handoff_candidates(cut, [], base) == []


def test_script_garbage_stdin_exits_0():
    r = subprocess.run([sys.executable, str(SCRIPT)], input="{{{", capture_output=True, text=True)
    assert r.returncode == 0 and r.stderr == ""


def test_main_stdin_that_never_ends_is_a_pass_after_the_deadline(monkeypatch):
    import threading

    release = threading.Event()

    class _Blocked:
        def read(self):
            release.wait(5)
            return b""

    class _Stdin2:
        buffer = _Blocked()

        def isatty(self):
            return False

    monkeypatch.setattr(sys, "stdin", _Stdin2())
    monkeypatch.setattr(hg, "STDIN_DEADLINE_SECONDS", 0.2)
    monkeypatch.setitem(hg._STDIN_DEADLINE_STATE, "hit", False)
    try:
        assert hg.main() == 0
        assert hg._STDIN_DEADLINE_STATE["hit"] is True
    finally:
        release.set()
