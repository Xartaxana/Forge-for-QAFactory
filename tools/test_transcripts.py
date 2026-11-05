"""Tests for tools/transcripts.py (B-467, t-623): the ONE reader of subagent transcripts, and its four
consumers (dispatch_gate's parallel cap, agent_budget, journal_echo, tier_echo) on the inputs that are
new with it. The existing tests of those consumers stay unedited -- they are the "behaviour unchanged"
witness; every new test lives here.

Module identity: dispatch_gate binds `transcripts` (package-style under `python -m pytest`), which is a
different object from a bare `import transcripts` in a test. Every stub for the cap therefore patches
`dispatch_gate.transcripts.<name>` and ASSERTS the stub was called; this file takes its `transcripts`
from dispatch_gate for the same reason.

Run from the repo root: python -m pytest tools/test_transcripts.py -q
"""

import ast
import json
import os
import pathlib
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import agent_budget  # noqa: E402
import dispatch_gate  # noqa: E402
import journal_echo  # noqa: E402
import tier_echo  # noqa: E402
from test_agent_budget import Session, _assistant, _write  # noqa: E402  (fixtures reused, not copied)
from test_dispatch_gate import _cap, _finish, _subagents_home  # noqa: E402
from test_journal_echo import _assistant_line, _delegated_obj, _write_agent_transcript  # noqa: E402

transcripts = dispatch_gate.transcripts
TOOLS = Path(__file__).resolve().parent
LS = chr(0x2028)  # LINE SEPARATOR: str.splitlines() ends a line here, JSONL does not
NEL = "\u0085"


def _call(name):
    return {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "t", "name": name,
                                                          "input": {}}]}}


def _line(obj):
    return json.dumps(obj, ensure_ascii=False)


def _usage_line(ctx, text="x"):
    """An assistant line whose text block holds `text` (ensure_ascii=False keeps U+2028 raw)."""
    usage = {"input_tokens": 2, "cache_creation_input_tokens": 1000, "cache_read_input_tokens": ctx - 1002}
    return _line({"type": "assistant", "message": {"usage": usage, "content": [{"type": "text", "text": text}]}})


def _write_bytes(path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def _write_lf(path, lines):
    """Lines joined by "\\n" exactly (the shared `_write` is text mode: CRLF on Windows, which the other
    tests here take as a free CRLF witness, but exact line equality needs LF)."""
    return _write_bytes(path, ("\n".join(lines) + "\n").encode("utf-8"))


def _cap_payload(session="sess-1"):
    # a WRITING dispatch (D-0040): the cap does not count or block a reading one
    return {"tool_name": "Agent", "session_id": session, "tool_input": {"subagent_type": "builder", "prompt": "go"}}


def _stat_raises(monkeypatch, name, exc):
    """Path.stat raises `exc` for the file called `name` only; returns the list of hits (a stub must be CALLED)."""
    real = pathlib.Path.stat
    hits = []

    def fake(self, *args, **kwargs):
        if self.name == name:
            hits.append(self)
            raise exc
        return real(self, *args, **kwargs)

    monkeypatch.setattr(pathlib.Path, "stat", fake)
    return hits


# ---------------------------------------------------------------------------------------------------
# shape of the module: stdlib only, nothing at import
# ---------------------------------------------------------------------------------------------------


def test_the_module_is_stdlib_only_and_does_no_io_at_import():
    tree = ast.parse((TOOLS / "transcripts.py").read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom):
            imported.add((node.module or "").split(".")[0])
    assert imported == {"json", "re", "pathlib"}
    allowed = (ast.Import, ast.ImportFrom, ast.Assign, ast.FunctionDef)
    for node in tree.body:  # the docstring is an Expr; no top-level call
        assert isinstance(node, allowed) or (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant))


def test_dispatch_gate_has_no_agent_budget_import_no_finished_delegate_no_session_regex():
    assert dispatch_gate.transcripts is not None
    for gone in ("agent_budget", "_is_finished", "_SESSION_ID_RE"):
        assert not hasattr(dispatch_gate, gone), gone


# ---------------------------------------------------------------------------------------------------
# agent_file_name / subagents_dir_of / find_agent_transcript   (I6, I7, I11)
# ---------------------------------------------------------------------------------------------------


@pytest.mark.parametrize("agent_id", [None, 5, "", "*", "a[b]", "../x", "a/b", "a b", "ab\n", chr(0x430)])
def test_agent_file_name_refuses_an_unsafe_id(agent_id):
    assert transcripts.agent_file_name(agent_id) is None


def test_agent_file_name_builds_the_name():
    assert transcripts.agent_file_name("a1-B_2") == "agent-a1-B_2.jsonl"


def test_subagents_dir_of_both_forms(tmp_path):
    main = tmp_path / "proj" / "sess.jsonl"
    assert transcripts.subagents_dir_of(str(main)) == tmp_path / "proj" / "sess" / "subagents"
    inside = tmp_path / "proj" / "sess" / "subagents" / "agent-w.jsonl"
    assert transcripts.subagents_dir_of(str(inside)) == inside.parent


def _projects(tmp_path):
    return tmp_path / ".claude" / "projects"


def test_find_agent_transcript_one_match_and_no_match(tmp_path):
    path = _write_agent_transcript(tmp_path, "abc", [_assistant_line("m")])
    assert transcripts.find_agent_transcript("abc", root=_projects(tmp_path)) == str(path)
    assert transcripts.find_agent_transcript("zzz", root=_projects(tmp_path)) is None
    assert transcripts.find_agent_transcript("abc", root=tmp_path / "nowhere") is None  # I6: no folder


@pytest.mark.parametrize("agent_id, present", [("*", "abc"), ("a[b]", "ab"), ("ab*", "abc"), ("../x", "x"), ("", "")])
def test_find_agent_transcript_unsafe_id_is_none_even_with_a_matching_file(tmp_path, agent_id, present):
    """M7: without the id check the glob metacharacters match the ONE file that exists (`*` -> agent-abc,
    `a[b]` -> agent-ab, an empty id -> agent-); exactly one file, or the ambiguity rule would mask the row."""
    path = _write_agent_transcript(tmp_path, present, [_assistant_line("m")])
    if present:  # control: the file is there and a safe id finds it
        assert transcripts.find_agent_transcript(present, root=_projects(tmp_path)) == str(path)
    assert transcripts.find_agent_transcript(agent_id, root=_projects(tmp_path)) is None


def test_find_agent_transcript_two_matches_is_ambiguous_none(tmp_path):
    """I7: one id under two sessions -- a measurement on the wrong worker is worse than none."""
    _write_agent_transcript(tmp_path, "dup", [_assistant_line("m")], sess="s1")
    assert transcripts.find_agent_transcript("dup", root=_projects(tmp_path)) is not None  # control: one match
    _write_agent_transcript(tmp_path, "dup", [_assistant_line("m")], sess="s2")
    assert transcripts.find_agent_transcript("dup", root=_projects(tmp_path)) is None


def test_find_agent_transcript_glob_error_and_missing_home_are_none(tmp_path, monkeypatch):
    class _Boom:
        def glob(self, pattern):
            raise OSError("boom")

    assert transcripts.find_agent_transcript("x", root=_Boom()) is None

    def no_home():
        raise RuntimeError("no home")

    monkeypatch.setattr(transcripts, "projects_root", no_home)
    assert transcripts.find_agent_transcript("x") is None  # root=None resolves projects_root() inside the try


def test_find_agent_transcript_root_none_uses_projects_root(tmp_path, monkeypatch):
    path = _write_agent_transcript(tmp_path, "abc", [_assistant_line("m")])
    monkeypatch.setattr(transcripts, "projects_root", lambda: _projects(tmp_path))
    assert transcripts.find_agent_transcript("abc") == str(path)


# ---------------------------------------------------------------------------------------------------
# split_lines / tail_lines   (I2, I4, I5, I9, I9b, the TAIL_BYTES boundary)
# ---------------------------------------------------------------------------------------------------


def test_split_lines_is_newline_only():
    assert transcripts.split_lines("a\nb\n") == ["a", "b"]
    assert transcripts.split_lines("a\nb") == ["a", "b"]
    assert transcripts.split_lines("") == []
    assert transcripts.split_lines("a\n\nb\n") == ["a", "", "b"]
    assert transcripts.split_lines("a\r\nb\r\n") == ["a\r", "b\r"]  # I9b: the CR is JSON whitespace
    assert transcripts.split_lines("a%sb\x0bc\x1cd%se\n" % (LS, NEL)) == ["a%sb\x0bc\x1cd%se" % (LS, NEL)]  # I9


def test_tail_lines_drops_the_cut_first_line(tmp_path):
    """M6: the first line of a tail that starts mid-file is a fragment and must go."""
    big = _line({"type": "user", "message": {"content": "y" * 70000}})
    f = _write_lf(tmp_path / "t.jsonl", [big, _assistant(123456)])
    assert transcripts.tail_lines(f) == [_assistant(123456)]
    small = _write_lf(tmp_path / "s.jsonl", ["a", "b"])
    assert transcripts.tail_lines(small) == ["a", "b"]  # start == 0: nothing is dropped


def _file_with_last_line_of(tmp_path, nbytes):
    """A short first line, then a last line of exactly `nbytes` bytes (its newline included)."""
    head = _assistant(7000)
    base = json.loads(_assistant(5000))
    last = json.dumps({**base, "pad": ""})
    last = json.dumps({**base, "pad": "p" * (nbytes - 1 - len(last.encode("utf-8")))})
    assert len(last.encode("utf-8")) + 1 == nbytes
    return _write_bytes(tmp_path / ("t%d.jsonl" % nbytes), (head + "\n" + last + "\n").encode("utf-8")), last


def test_tail_boundary_a_last_line_of_any_length_is_seen_whole(tmp_path):
    """AT and BEYOND TAIL_BYTES. The off-by-one of the moved code (a last line of exactly TAIL_BYTES, newline
    included, was dropped with the cut one) is CLOSED by t-840: the last line is returned whole."""
    n = transcripts.TAIL_BYTES
    for size in (n - 1, n, n + 1):
        f, last = _file_with_last_line_of(tmp_path, size)
        assert transcripts.tail_lines(f)[-1] == last, size  # a grown window also carries the lines before it
        assert transcripts.context_size(f) == 5000, size
    f, last = _file_with_last_line_of(tmp_path, n - 1)
    assert transcripts.tail_lines(f) == [last]  # fits the window: read once, exactly the old result


def test_tail_lines_missing_file_raises_oserror(tmp_path):
    with pytest.raises(OSError):
        transcripts.tail_lines(tmp_path / "nope.jsonl")


# t-840 (F6-7): the LAST line of the file is returned whole whatever its length. The expectations marked
# "today" were measured on 47274dc8 before the change and are pinned as they were.

SHORT_RESULT = _line({"type": "user", "message": {"content": [{"type": "tool_result", "content": "ok"}]}})


def _big_handback(nbytes=70000):
    line = _line({"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "t", "name": "SubagentHandback",
                                                                "input": {"message": "w" * nbytes}}]}})
    assert len(line.encode("utf-8")) > transcripts.TAIL_BYTES
    return line


def test_a_70kb_last_line_handback_is_seen_whole_and_is_finished(tmp_path):
    """The live case of t-744: a final SubagentHandback line of 74 KB. Today: is_finished False, tail_lines []."""
    big = _big_handback()
    for name, data in (("lf", SHORT_RESULT + "\n" + big + "\n"), ("nolf", SHORT_RESULT + "\n" + big)):
        f = _write_bytes(tmp_path / (name + ".jsonl"), data.encode("utf-8"))
        assert transcripts.tail_lines(f) == [SHORT_RESULT, big], name
        assert transcripts.is_finished(f) is True, name
        assert agent_budget.is_finished(f) is True, name


def test_a_big_handback_followed_by_short_lines_is_finished_t857(tmp_path):
    """F6-19 (the pin of F6-7 flipped from False): tail_lines still guarantees only the LAST line whole, but
    is_finished grows the window until the newest tool_use line is whole -- a 70 KB hand-back followed by one
    short line, or by the five the harness writes (result / queue lines), is finished."""
    big = _big_handback()
    f = _write_bytes(tmp_path / "big_then_short.jsonl", (big + "\n" + SHORT_RESULT + "\n").encode("utf-8"))
    assert transcripts.tail_lines(f) == [SHORT_RESULT]  # the line reader is unchanged
    assert transcripts.is_finished(f) is True
    five = _write_bytes(tmp_path / "big_then_five.jsonl", (big + "\n" + (SHORT_RESULT + "\n") * 5).encode("utf-8"))
    assert transcripts.is_finished(five) is True
    assert agent_budget.is_finished(five) is True
    short_hb = _line(_call("SubagentHandback"))
    g = _write_bytes(tmp_path / "short_then_short.jsonl", (short_hb + "\n" + SHORT_RESULT + "\n").encode("utf-8"))
    assert transcripts.is_finished(g) is True


def test_the_newest_tool_use_line_decides_behind_a_big_handback_t857(tmp_path):
    """The rule is still 'the newest tool_use decides': a later Bash call after the big hand-back -> live; two
    hand-backs, the newer one big -> finished; the older one big and the newer one a Read -> live; a user line that
    carries a tool_use block of a USER line (not an assistant call) is no tool_use line."""
    big = _big_handback()
    tail = (SHORT_RESULT + "\n") * 3
    later_bash = _write_bytes(tmp_path / "bash.jsonl", (big + "\n" + SHORT_RESULT + "\n" + _line(_call("Bash")) + "\n"
                                                        + tail).encode("utf-8"))
    assert transcripts.is_finished(later_bash) is False
    two = _write_bytes(tmp_path / "two.jsonl", (_line(_call("SubagentHandback")) + "\n" + SHORT_RESULT + "\n" + big
                                                + "\n" + tail).encode("utf-8"))
    assert transcripts.is_finished(two) is True
    old_big = _write_bytes(tmp_path / "old_big.jsonl", (big + "\n" + _line(_call("Read")) + "\n" + tail).encode("utf-8"))
    assert transcripts.is_finished(old_big) is False
    wording = _line({"type": "user", "message": {"content": [{"type": "tool_use", "id": "u", "name": "Bash", "input": {}}]}})
    mention = _write_bytes(tmp_path / "mention.jsonl", (big + "\n" + wording + "\n" + tail).encode("utf-8"))
    assert transcripts.is_finished(mention) is True


def test_the_scan_bound_is_not_finished_and_never_a_raise_t857(tmp_path):
    """TAIL_SCAN_MAX: a hand-back whose line lies wholly inside the last TAIL_SCAN_MAX bytes is found however
    many short lines follow it (2 MB, and 2000 bytes short of the bound); one that starts further back is
    'not finished', no raise; a tool_use line that is itself cut by the bound is not parsed (False); a file with
    no tool_use line at all, and an empty file, are False."""
    big = _big_handback()
    unit = (SHORT_RESULT + "\n").encode("utf-8")
    hb = big.encode("utf-8") + b"\n"

    def after(nbytes):
        return _write_bytes(tmp_path / ("after%d.jsonl" % nbytes), hb + unit * (nbytes // len(unit)))

    assert transcripts.is_finished(after(2 * 1024 * 1024)) is True
    assert transcripts.is_finished(after(transcripts.TAIL_SCAN_MAX - len(hb) - 2000)) is True
    assert transcripts.is_finished(after(transcripts.TAIL_SCAN_MAX + 1000)) is False
    cut = _write_bytes(tmp_path / "cut.jsonl", (_line(_call("Read")) + "\n").encode("utf-8")
                       + _big_handback(transcripts.TAIL_SCAN_MAX + 100_000).encode("utf-8") + b"\n")
    assert transcripts.is_finished(cut) is False  # the hand-back line is longer than the bound: never half-read
    assert transcripts.is_finished(_write_bytes(tmp_path / "none.jsonl", unit * 20_000)) is False
    assert transcripts.is_finished(_write_bytes(tmp_path / "empty2.jsonl", b"")) is False


def test_a_crlf_big_handback_followed_by_short_lines_is_finished_t857(tmp_path):
    crlf = (_big_handback() + "\r\n" + (SHORT_RESULT + "\r\n") * 4).encode("utf-8")
    assert transcripts.is_finished(_write_bytes(tmp_path / "crlf.jsonl", crlf)) is True


def test_is_finished_on_a_file_that_changes_between_stat_and_read_gives_an_answer_never_a_raise_t857(tmp_path,
                                                                                                     monkeypatch):
    f = _write_bytes(tmp_path / "grow.jsonl", (_big_handback() + "\n" + SHORT_RESULT + "\n").encode("utf-8"))
    real = pathlib.Path.stat

    class Stale:  # the size the file had before it was truncated / before it grew
        st_size = 9_000_000

    monkeypatch.setattr(pathlib.Path, "stat", lambda self, *a, **k: Stale if self == f else real(self, *a, **k))
    assert isinstance(transcripts.is_finished(f), bool)
    Stale.st_size = 10
    assert isinstance(transcripts.is_finished(f), bool)


def test_tail_lines_empty_file_no_trailing_newline_and_a_trailing_newline_is_no_line(tmp_path):
    empty = _write_bytes(tmp_path / "empty.jsonl", b"")
    assert transcripts.tail_lines(empty) == [] and transcripts.is_finished(empty) is False
    assert transcripts.tail_lines(_write_bytes(tmp_path / "nonl.jsonl", b"a\nb")) == ["a", "b"]
    assert transcripts.tail_lines(_write_bytes(tmp_path / "small.jsonl", b"a\nb\nc\n")) == ["a", "b", "c"]  # today
    big = "x" * 70000
    with_nl = _write_bytes(tmp_path / "big_nl.jsonl", (big + "\n").encode())
    without = _write_bytes(tmp_path / "big_nonl.jsonl", big.encode())
    assert transcripts.tail_lines(with_nl) == [big] and transcripts.tail_lines(without) == [big]  # today: []
    # a trailing "\n" ends the last line, it does not start an empty one; a real empty last line stays one
    assert transcripts.tail_lines(_write_bytes(tmp_path / "blank.jsonl", b"a\n\n")) == ["a", ""]  # today


def test_a_middle_line_over_the_window_is_cut_as_today_when_the_last_line_is_short(tmp_path):
    middle = "m" * 100000
    f = _write_bytes(tmp_path / "mid.jsonl", ("s1\n" + middle + "\nlast\n").encode())
    assert transcripts.tail_lines(f) == ["last"]  # today: the cut middle line is dropped, no growth


def test_a_crlf_last_line_over_the_window_keeps_its_cr_as_today(tmp_path):
    big = "y" * 70000
    f = _write_bytes(tmp_path / "crlf_big.jsonl", ("a\r\n" + big + "\r\n").encode())
    assert transcripts.tail_lines(f) == ["a\r", big + "\r"]
    assert transcripts.tail_lines(_write_bytes(tmp_path / "crlf_small.jsonl", b"a\r\nb\r\n")) == ["a\r", "b\r"]  # today


def test_a_multibyte_char_cut_by_the_window_start_does_not_touch_the_last_line(tmp_path):
    last = "é" * 40000  # 80000 bytes: the first window starts inside the line, maybe inside a character
    for lead in ("", "x"):
        f = _write_bytes(tmp_path / ("mb%s.jsonl" % lead), ("a\n" + lead + last + "\n").encode("utf-8"))
        assert transcripts.tail_lines(f) == ["a", lead + last]


def test_a_usage_line_that_is_the_last_line_and_over_the_window_is_found(tmp_path):
    f = _write_bytes(tmp_path / "usage_big.jsonl", (_assistant(1500) + "\n" + _usage_line(222222, text="p" * 70000)
                                                    + "\n").encode("utf-8"))
    assert transcripts.context_size(f) == 222222  # today: None
    assert transcripts.last_usage(transcripts.tail_lines(f)) == 222222


def test_the_window_grows_in_doubling_steps_and_every_byte_is_read_once(tmp_path, monkeypatch):
    """The performance edge: a last line of 3 MB is read once, not once per step (the sum of the reads is the
    span from the window start to EOF) and in O(log) reads."""
    last = "z" * 3_000_000
    f = _write_bytes(tmp_path / "huge.jsonl", ("a\n" + last + "\n").encode())
    reads = []
    real_open = open

    class Counting:
        def __init__(self, fh):
            self._fh = fh

        def __enter__(self):
            self._fh.__enter__()
            return self

        def __exit__(self, *exc):
            return self._fh.__exit__(*exc)

        def seek(self, *a):
            return self._fh.seek(*a)

        def read(self, *a):
            data = self._fh.read(*a)
            reads.append(len(data))
            return data

    monkeypatch.setattr(transcripts, "open", lambda *a, **k: Counting(real_open(*a, **k)), raising=False)
    assert transcripts.tail_lines(f) == ["a", last]
    assert sum(reads) == f.stat().st_size and len(reads) <= 10, reads


def test_a_file_that_shrinks_between_stat_and_read_gives_a_tail_never_an_error(tmp_path, monkeypatch):
    f = _write_bytes(tmp_path / "shrunk.jsonl", b"a\nb\n")
    real = pathlib.Path.stat

    class Stale:  # the size the file had before it was truncated
        st_size = 500_000

    monkeypatch.setattr(pathlib.Path, "stat", lambda self, *a, **k: Stale if self == f else real(self, *a, **k))
    assert isinstance(transcripts.tail_lines(f), list)


# ---------------------------------------------------------------------------------------------------
# parse_line / content_blocks / usage_total / last_usage / context_size
# ---------------------------------------------------------------------------------------------------


def test_parse_line():
    assert transcripts.parse_line('{"a": 1}') == {"a": 1}
    for bad in ("", "garbage", "[1, 2]", '"s"', "12", "null", '{"a": '):
        assert transcripts.parse_line(bad) is None


def test_parse_line_survives_a_line_of_200000_brackets():
    """I14: json.loads raises RecursionError (not a ValueError) on deep nesting."""
    with pytest.raises(RecursionError):
        json.loads("[" * 200000)  # control: the input really raises what the module must catch
    assert transcripts.parse_line("[" * 200000) is None
    assert transcripts.parse_line('{"a": ' * 100000) is None


def test_content_blocks_edges():
    assert transcripts.content_blocks(None) == []
    assert transcripts.content_blocks({}) == []
    assert transcripts.content_blocks({"message": "x"}) == []
    assert transcripts.content_blocks({"message": {"content": "text"}}) == []
    assert transcripts.content_blocks({"message": {"content": [1]}}) == [1]


def test_usage_total_sums_and_a_non_numeric_value_raises():
    assert transcripts.usage_total(_assistant(123456)) == 123456
    assert transcripts.usage_total(_line({"type": "assistant", "message": {"usage": {"input_tokens": 0}}})) is None
    assert transcripts.usage_total(_line({"type": "user", "message": {"content": "no usage"}})) is None
    assert transcripts.usage_total("garbage with \"usage\" in it") is None
    bad = _line({"type": "assistant", "message": {"usage": {"input_tokens": "abc"}}})
    with pytest.raises(ValueError):  # I10: agent_budget turns this into its fail-open
        transcripts.usage_total(bad)


def test_last_usage_is_the_newest():
    assert transcripts.last_usage([_assistant(100000), "garbage", _assistant(250000), "{}"]) == 250000
    assert transcripts.last_usage(["{}", "garbage"]) is None
    assert transcripts.last_usage([]) is None


def test_context_size_rows(tmp_path):
    assert transcripts.context_size(_write(tmp_path / "a.jsonl", [_assistant(111111)])) == 111111
    assert transcripts.context_size(_write(tmp_path / "b.jsonl", ["{}", "garbage"])) is None  # I3
    partial = _assistant(300000)[:-9]  # I2: the line being written, no closing
    f = _write_bytes(tmp_path / "c.jsonl", (_assistant(120000) + "\n" + partial).encode("utf-8"))
    assert transcripts.context_size(f) == 120000
    bin_ = (_assistant(130000) + "\n").encode("utf-8") + b"\xff\xfe\x80 garbage\n" + (_assistant(140000) + "\n").encode()
    assert transcripts.context_size(_write_bytes(tmp_path / "d.jsonl", bin_)) == 140000  # I4
    with pytest.raises(OSError):  # I1
        transcripts.context_size(tmp_path / "missing.jsonl")


def test_a_usage_line_with_u2028_or_nel_inside_a_string_is_read_whole(tmp_path):
    """I9 / M9: str.splitlines() cuts the line at U+2028 and the usage is lost."""
    for sep in (LS, NEL):  # \x0b \x0c \x1c-\x1e cannot occur raw inside valid JSON (json.dumps escapes them)
        line = _usage_line(222222, text="before%safter" % sep)
        assert len(line.splitlines()) > 1  # control: the old splitter really cuts this line
        f = _write(tmp_path / ("u%d.jsonl" % ord(sep)), [_assistant(1500), line])
        assert transcripts.context_size(f) == 222222, repr(sep)


def test_crlf_files_parse_unchanged(tmp_path):
    """I9b: the trailing CR is JSON whitespace."""
    f = _write_bytes(tmp_path / "crlf.jsonl", ("\r\n".join([_assistant(90000), _line(_call("SubagentHandback"))])
                                               + "\r\n").encode("utf-8"))
    assert transcripts.context_size(f) == 90000
    assert transcripts.is_finished(f) is True


def test_a_deep_line_before_the_usage_line_is_skipped(tmp_path):
    f = _write(tmp_path / "deep.jsonl", [_assistant(150000), '"usage" ' + "[" * 200000, _assistant(160000)])
    assert transcripts.last_usage(transcripts.split_lines(f.read_text(encoding="utf-8"))) == 160000
    g = _write(tmp_path / "deep2.jsonl", ["[" * 200000 + ' "usage"', _assistant(170000)])
    assert transcripts.last_usage(transcripts.split_lines(g.read_text(encoding="utf-8"))) == 170000


# ---------------------------------------------------------------------------------------------------
# last_tool_use_names / is_finished   (I1-I5, I9, I9b, I14)
# ---------------------------------------------------------------------------------------------------


def test_last_tool_use_names_picks_the_newest_assistant_line_with_any():
    user = _line({"type": "user", "message": {"content": [{"type": "tool_result", "content": "ok"}]}})
    lines = [_line(_call("Read")), _line(_call("SubagentHandback")), user, "garbage"]
    assert transcripts.last_tool_use_names(lines) == ["SubagentHandback"]
    assert transcripts.last_tool_use_names([_line(_call("Read")), _line(_call("Bash")), user]) == ["Bash"]
    assert transcripts.last_tool_use_names(["{}", "garbage", user]) is None
    assert transcripts.last_tool_use_names([]) is None
    text_only = _line({"type": "assistant", "message": {"content": [{"type": "text", "text": "tool_use"}]}})
    assert transcripts.last_tool_use_names([_line(_call("Read")), text_only]) == ["Read"]  # no tool_use block


def test_is_finished_rows(tmp_path):
    user = _line({"type": "user", "message": {"content": "ok"}})
    done = _write(tmp_path / "done.jsonl", [_line(_call("Read")), _line(_call("SubagentHandback")), user])
    live = _write(tmp_path / "live.jsonl", [_line(_call("SubagentHandback")), _line(_call("Bash")), user])
    empty = _write(tmp_path / "empty.jsonl", ["{}", "garbage"])  # I3: no tool_use at all -> live
    assert (transcripts.is_finished(done), transcripts.is_finished(live), transcripts.is_finished(empty)) == (
        True, False, False)
    with pytest.raises(OSError):  # I1
        transcripts.is_finished(tmp_path / "missing.jsonl")
    two = _line({"type": "assistant", "message": {"content": [
        {"type": "tool_use", "id": "a", "name": "Read", "input": {}},
        {"type": "tool_use", "id": "b", "name": "SubagentHandback", "input": {}}]}})
    assert transcripts.is_finished(_write(tmp_path / "two.jsonl", [two])) is True  # one of several blocks
    partial = _line(_call("SubagentHandback"))[:-6]  # I2: the handback line is still being written
    f = _write_bytes(tmp_path / "part.jsonl", (_line(_call("Read")) + "\n" + partial).encode("utf-8"))
    assert transcripts.is_finished(f) is False  # the earlier tool_use decides


def test_a_handback_line_holding_u2028_is_seen(tmp_path):
    """I9 / M9: a handback message with a LINE SEPARATOR in it used to be cut into two broken halves."""
    for sep in (LS, NEL):
        call = {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "t", "name": "SubagentHandback",
                                                              "input": {"message": "done%sok" % sep}}]}}
        f = _write(tmp_path / ("h%d.jsonl" % ord(sep)), [_line(_call("Read")), _line(call)])
        assert transcripts.is_finished(f) is True, repr(sep)


def test_a_deep_line_is_skipped_by_the_tool_use_reader():
    deep = '{"type": "assistant", "x": "tool_use" ' + "[" * 200000
    assert transcripts.last_tool_use_names([_line(_call("SubagentHandback")), deep]) == ["SubagentHandback"]


def test_big_transcripts_are_read_right(tmp_path):
    """I5, a 10 MB file: correct values (the timing is measured for the report, not asserted -- FR-31)."""
    filler = _line({"type": "user", "message": {"content": "z" * 9000}})
    n = 10_000_000 // (len(filler) + 1) + 1
    f = tmp_path / "big.jsonl"
    with open(f, "w", encoding="utf-8") as fh:
        for _ in range(n):
            fh.write(filler + "\n")
        fh.write(_assistant(333333) + "\n")
        fh.write(_line(_call("SubagentHandback")) + "\n")
    assert f.stat().st_size > 10_000_000
    assert transcripts.context_size(f) == 333333
    assert transcripts.is_finished(f) is True
    huge_last = _write(tmp_path / "huge_last.jsonl", [_assistant(100), _line({"type": "user", "message": {
        "content": "y" * 70000}})])
    # the last line is longer than the tail (t-840: it is returned whole, the line before it comes with it)
    assert transcripts.context_size(huge_last) == 100
    assert transcripts.is_finished(huge_last) is False


# ---------------------------------------------------------------------------------------------------
# iter_lines / iter_models
# ---------------------------------------------------------------------------------------------------


def test_iter_lines_raises_on_the_first_next_not_at_the_call(tmp_path):
    gen = transcripts.iter_lines(tmp_path / "missing.jsonl")  # a generator: nothing opened yet
    with pytest.raises(OSError):
        next(gen)


def test_iter_lines_splits_on_newline_only_and_replaces_bad_bytes(tmp_path):
    f = _write_bytes(tmp_path / "x.jsonl", ("a%sb\nc\r\n" % LS).encode("utf-8") + b"\xff\xfe\nlast")
    assert list(transcripts.iter_lines(f)) == ["a%sb" % LS, "c\r", chr(0xFFFD) * 2, "last"]


def _whole_file_lines(path):
    """The reference the streaming iter_lines must equal: the file read WHOLE, decoded, split_lines (the code
    iter_lines had before t-797 F5-2)."""
    return transcripts.split_lines(Path(path).read_bytes().decode("utf-8", errors="replace"))


CORPUS = {
    "empty": b"",
    "lone newline": b"\n",
    "two newlines": b"\n\n",
    "no final newline": b'{"a": 1}\n{"b": 2}',
    "final newline": b'{"a": 1}\n{"b": 2}\n',
    "blank line inside": b"a\n\nb\n",
    "crlf": b"a\r\nb\r\n",
    "lone cr": b"a\rb\n",
    "u2028 u0085": ("a%sb\nc%sd\n" % (LS, NEL)).encode("utf-8"),
    "broken bytes": b"\xff\xfe\nok\n\xc3\nlast\xe2\x82",
    "multibyte cut by newline": b"abc\xe2\x82\ndef\n",
    "bom": b"\xef\xbb\xbfx\ny\n",
    "nul and tabs": b"a\x00b\n\t\n",
    "only broken": b"\xff",
    "long line": b"x" * 300000 + b"\nshort\n",
}


@pytest.mark.parametrize("name", sorted(CORPUS))
def test_iter_lines_streaming_is_identical_to_the_whole_file_read_e31(tmp_path, name):
    """E31 (the four hooks read this function): every shape the old whole-file read handled gives the same lines."""
    f = _write_bytes(tmp_path / "x.jsonl", CORPUS[name])
    assert list(transcripts.iter_lines(f)) == _whole_file_lines(f)


def test_iter_lines_a_last_line_without_a_newline_is_a_line_e31(tmp_path):
    """U9: a streaming reader that drops the unterminated last line is the mutant this pins."""
    f = _write_bytes(tmp_path / "x.jsonl", b"first\nlast")
    assert list(transcripts.iter_lines(f)) == ["first", "last"]
    assert list(transcripts.iter_lines(_write_bytes(tmp_path / "one.jsonl", b"only"))) == ["only"]


def test_iter_lines_is_lazy_and_an_unreadable_file_raises_on_the_first_next_e31(tmp_path):
    folder = tmp_path / "a_folder"
    folder.mkdir()
    gen = transcripts.iter_lines(folder)       # a directory: open() fails, but only when the generator is advanced
    with pytest.raises(OSError):
        next(gen)
    f = _write_bytes(tmp_path / "x.jsonl", b"a\nb\nc\n")
    gen = transcripts.iter_lines(f)
    assert next(gen) == "a"                    # one line at a time: the rest of the file is not in a list


def test_iter_lines_a_growing_file_a_line_cut_by_a_write_is_skipped_by_the_readers_and_nothing_is_capped(tmp_path):
    """E19: the last line is half a JSON object (a write in flight); it is yielded as text, parse_line drops it,
    and request_usages counts everything before it."""
    good = _usage_request("r1", [{"input_tokens": 3, "output_tokens": 4}])
    f = _write_bytes(tmp_path / "grow.jsonl", ("\n".join(good) + '\n{"type": "assistant", "requestId": "r2", "message": {"usa').encode())
    assert list(transcripts.iter_lines(f))[-1].startswith('{"type": "assistant", "requestId": "r2"')
    assert [r["key"] for r in transcripts.request_usages(f)] == ["requestId:r1"]


def _usage_request(rid, usages, **line):
    """One assistant line per usage dict, all with requestId `rid` (the harness writes one line per content block)."""
    return [_line({"type": "assistant", "requestId": rid, "uuid": "u-%s-%d" % (rid, i),
                   "message": {"role": "assistant", "model": "m", "content": [{"type": "text", "text": "t"}], "usage": u}, **line})
            for i, u in enumerate(usages)]


def test_request_usages_takes_the_max_of_every_field_inside_a_request_u3(tmp_path):
    """U3: the measured scout t-794 case, output_tokens 17/17/17/485 on four lines of ONE request. The first line of the
    request (17) is the mutant; the sum (536) is the other wrong answer."""
    lines = _usage_request("req-1", [
        {"input_tokens": 10, "cache_creation_input_tokens": 100, "cache_read_input_tokens": 1000, "output_tokens": 17},
        {"input_tokens": 10, "cache_creation_input_tokens": 100, "cache_read_input_tokens": 1000, "output_tokens": 17},
        {"input_tokens": 10, "cache_creation_input_tokens": 100, "cache_read_input_tokens": 1000, "output_tokens": 17},
        {"input_tokens": 10, "cache_creation_input_tokens": 100, "cache_read_input_tokens": 1000, "output_tokens": 485}])
    lines += _usage_request("req-2", [{"input_tokens": 1, "output_tokens": 20}])
    got = transcripts.request_usages(_write_lf(tmp_path / "w.jsonl", lines))
    assert got == [
        {"key": "requestId:req-1", "input_tokens": 10, "cache_creation_input_tokens": 100, "cache_read_input_tokens": 1000,
         "output_tokens": 485},
        {"key": "requestId:req-2", "input_tokens": 1, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0,
         "output_tokens": 20}]
    # the max is per FIELD: a later line with a smaller input and a bigger cache-read keeps both maxima
    mixed = _usage_request("m", [{"input_tokens": 9, "cache_read_input_tokens": 1}, {"input_tokens": 2, "cache_read_input_tokens": 8}])
    got = transcripts.request_usages(_write_lf(tmp_path / "m.jsonl", mixed))
    assert (got[0]["input_tokens"], got[0]["cache_read_input_tokens"]) == (9, 8)


def test_request_usages_key_falls_back_to_uuid_then_to_the_line_number_e18(tmp_path):
    """E18: a line with neither id is its OWN request (an over-count is allowed, an under-count is not)."""
    no_rid = {"type": "assistant", "message": {"model": "m", "usage": {"output_tokens": 5}}}
    lines = [_line(dict(no_rid, uuid="same")), _line(dict(no_rid, uuid="same", message={"usage": {"output_tokens": 9}})),
             _line(no_rid), _line(no_rid)]
    got = transcripts.request_usages(_write_lf(tmp_path / "w.jsonl", lines))
    assert [(r["key"], r["output_tokens"]) for r in got] == [("uuid:same", 9), ("line:3", 5), ("line:4", 5)]
    blank = [_line({"type": "assistant", "requestId": "", "uuid": 5, "message": {"usage": {"output_tokens": 1}}})]
    assert [r["key"] for r in transcripts.request_usages(_write_lf(tmp_path / "b.jsonl", blank))] == ["line:1"]


def test_request_usages_skips_what_is_not_a_turn_and_survives_the_empty_and_the_broken_e17(tmp_path):
    real = _usage_request("r1", [{"output_tokens": 7}])[0]
    lines = ["", "garbage", "[" * 200000, _line({"type": "user", "message": {"usage": {"output_tokens": 99}}}),
             _line({"type": "assistant", "requestId": "syn", "message": {"model": "<synthetic>", "usage": {"output_tokens": 99}}}),
             _line({"type": "assistant", "requestId": "nou", "message": {"content": []}}),
             _line({"type": "assistant", "requestId": "str", "message": "x"}),
             _line({"type": "assistant", "requestId": "nd", "message": {"usage": "x"}}), real]
    assert [r["output_tokens"] for r in transcripts.request_usages(_write_lf(tmp_path / "w.jsonl", lines))] == [7]
    assert transcripts.request_usages(_write_bytes(tmp_path / "zero.jsonl", b"")) == []
    assert transcripts.request_usages(_write_lf(tmp_path / "nousage.jsonl", [_line({"type": "assistant"}), "x"])) == []
    with pytest.raises(OSError):
        transcripts.request_usages(tmp_path / "missing.jsonl")


@pytest.mark.parametrize("bad", ["abc", [1], {"x": 1}, float("inf")])
def test_request_usages_a_non_numeric_usage_value_raises_value_or_type_error_e17(tmp_path, bad):
    f = _write_lf(tmp_path / "w.jsonl", _usage_request("r1", [{"output_tokens": bad}]))
    with pytest.raises((ValueError, TypeError)):
        transcripts.request_usages(f)


def _model_request(rid, model, usages, first=0):
    """_usage_request with a model of its own and uuids that do not collide with another call's."""
    lines = _usage_request(rid, usages)
    return [_line(dict(json.loads(l), uuid="u-%s-%d" % (rid, first + i),
                       message=dict(json.loads(l)["message"], model=model))) for i, l in enumerate(lines)]


def test_request_parts_one_part_per_model_in_first_seen_order_max_inside_a_model_f6_23(tmp_path):
    """F6-23: a model fallback inside one request. The measured request (27.08): fable-5 on line 1, then four lines
    of opus-4-8, the last carrying the fallback's own usage. One part per model, each the MAX over ITS lines; the
    request as a whole (request_usages) is still the MAX over all of them."""
    first = {"input_tokens": 2, "cache_creation_input_tokens": 625, "cache_read_input_tokens": 102517, "output_tokens": 3}
    last = {"input_tokens": 2, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 98101, "output_tokens": 390}
    lines = (_model_request("req", "claude-fable-5", [first])
             + _model_request("req", "claude-opus-4-8", [first, first, first, last], first=1)
             + _model_request("other", "claude-sonnet-5", [{"output_tokens": 9}]))
    f = _write_lf(tmp_path / "w.jsonl", lines)
    got = transcripts.request_parts(f)
    assert [r["key"] for r in got] == ["requestId:req", "requestId:other"]
    assert [p["model"] for p in got[0]["parts"]] == ["claude-fable-5", "claude-opus-4-8"]
    fable, opus = got[0]["parts"]
    assert (fable["input_tokens"], fable["output_tokens"], fable["cache_creation_input_tokens"],
            fable["cache_read_input_tokens"]) == (2, 3, 625, 102517)
    assert (opus["input_tokens"], opus["output_tokens"], opus["cache_creation_input_tokens"],
            opus["cache_read_input_tokens"]) == (2, 390, 625, 102517)
    assert [p["model"] for p in got[1]["parts"]] == ["claude-sonnet-5"]
    assert transcripts.request_usages(f)[0] == {"key": "requestId:req", "input_tokens": 2, "cache_creation_input_tokens": 625,
                                                "cache_read_input_tokens": 102517, "output_tokens": 390}


def test_request_parts_the_one_hour_split_is_the_largest_known_one_and_none_when_no_line_has_it_f6_23(tmp_path):
    with_split = {"output_tokens": 1, "cache_creation": {"ephemeral_1h_input_tokens": 40}}
    other_split = {"output_tokens": 1, "cache_creation": {"ephemeral_1h_input_tokens": 70}}
    no_split = {"output_tokens": 1}
    broken = {"output_tokens": 1, "cache_creation": {"ephemeral_1h_input_tokens": -5}}
    lines = (_model_request("a", "m1", [with_split, no_split, other_split, broken])
             + _model_request("b", "m1", [no_split, broken]) + _model_request("c", "m1", [{"output_tokens": 1, "cache_creation": {"ephemeral_1h_input_tokens": 0}}]))
    got = {r["key"]: r["parts"][0]["cache_creation_1h_tokens"] for r in transcripts.request_parts(_write_lf(tmp_path / "w.jsonl", lines))}
    assert got == {"requestId:a": 70, "requestId:b": None, "requestId:c": 0}   # 0 is a KNOWN split, None is unknown


def test_request_parts_a_model_that_is_missing_or_not_a_string_is_a_part_of_its_own_f6_23(tmp_path):
    lines = _model_request("r", "m1", [{"output_tokens": 5}]) + _usage_request("r", [{"output_tokens": 8}])
    nomodel = json.loads(lines[-1])
    nomodel["message"].pop("model")
    nomodel["uuid"] = "u-nomodel"
    lines[-1] = _line(nomodel)
    lines.append(_line(dict(nomodel, uuid="u-list", message=dict(nomodel["message"], model=["m1"]))))
    got = transcripts.request_parts(_write_lf(tmp_path / "w.jsonl", lines))
    assert [(p["model"], p["output_tokens"]) for p in got[0]["parts"]] == [("m1", 5), (None, 8)]   # a list model is None, no TypeError


def test_request_parts_skipped_collects_the_lines_it_could_not_read_and_without_it_the_old_contract_holds_f6_23(tmp_path):
    def bare(rid, usage):
        return _line({"type": "assistant", "requestId": rid, "message": {"model": "m", "usage": usage}})
    lines = [bare("ok", {"output_tokens": 1}), bare("str", "x"), bare("lst", [1]), bare("num", 7), bare("null", None),
             bare("bad", {"output_tokens": "abc"}), bare("inf", {"output_tokens": float("inf")}),
             _line({"type": "assistant", "requestId": "syn", "message": {"model": "<synthetic>", "usage": "x"}})]
    f = _write_lf(tmp_path / "w.jsonl", lines)
    skipped = []
    got = transcripts.request_parts(f, skipped)
    assert [r["key"] for r in got] == ["requestId:ok"]
    assert skipped == [2, 3, 4, 6, 7]                  # null is an absent usage; the synthetic line is not looked at
    with pytest.raises((ValueError, TypeError)):       # no `skipped`: a mistyped value raises, as it always did
        transcripts.request_parts(f)
    f2 = _write_lf(tmp_path / "w2.jsonl", lines[:5])
    assert [r["key"] for r in transcripts.request_parts(f2)] == ["requestId:ok"]   # a non-object usage is skipped silently


def test_request_key_is_the_one_key_of_a_request_f6_23():
    assert transcripts.request_key({"requestId": "r", "uuid": "u"}, 4) == ("requestId", "r")
    assert transcripts.request_key({"requestId": "", "uuid": "u"}, 4) == ("uuid", "u")
    assert transcripts.request_key({"requestId": 5, "uuid": None}, 4) == ("line", 4)


def _entry(model, out, read=0, write=0, one_hour=0, **extra):
    return dict({"input_tokens": 2, "output_tokens": out, "cache_read_input_tokens": read, "cache_creation_input_tokens": write,
                 "cache_creation": {"ephemeral_5m_input_tokens": write - one_hour, "ephemeral_1h_input_tokens": one_hour},
                 "type": "message", "model": model}, **extra)


def test_request_parts_usage_iterations_of_two_or_more_entries_are_the_carrier_t886(tmp_path):
    """t-886 F-1: the provider's own per-message record beats the lines. Real shape (27.08): the lines say fable-5 once
    and opus-4-8 four times, the last line carries the iterations (fable 869 out / opus 390 out). The parts are the
    entries', whatever the lines' MAX would give (fable output 3 there)."""
    first = {"input_tokens": 2, "cache_creation_input_tokens": 625, "cache_read_input_tokens": 102517, "output_tokens": 3}
    last = {"input_tokens": 2, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 98101, "output_tokens": 390,
            "iterations": [_entry("claude-fable-5", 869, 102517, 625), _entry("claude-opus-4-8", 390, 98101, 0, type="fallback_message")]}
    lines = _model_request("req", "claude-fable-5", [first]) + _model_request("req", "claude-opus-4-8", [first, first, first, last], first=1)
    counts = {}
    got = transcripts.request_parts(_write_lf(tmp_path / "w.jsonl", lines), counts=counts)
    assert [(p["model"], p["output_tokens"], p["cache_read_input_tokens"], p["cache_creation_input_tokens"],
             p["cache_creation_1h_tokens"]) for p in got[0]["parts"]] == [
        ("claude-fable-5", 869, 102517, 625, 0), ("claude-opus-4-8", 390, 98101, 0, 0)]
    assert counts == {}                                  # both entries carry a split, no iterations malformed


def test_request_parts_the_carrier_beats_the_labels_and_puts_the_labelled_model_first_t886(tmp_path):
    """Five lines all labelled opus-4-8 (real: req_011CeTUq...), iterations fable-5 + opus-4-8: two parts, the labelled
    model FIRST (the bare dedupe key of a database filled before this fix), the other after it. A line labelled with a
    model the iterations do not name does not make a part of its own."""
    usage = {"input_tokens": 2, "output_tokens": 874, "iterations": [_entry("claude-fable-5", 279, 229161, 2972, 2972),
                                                                       _entry("claude-opus-4-8", 874, 206526)]}
    f = _write_lf(tmp_path / "w.jsonl", _model_request("r", "claude-opus-4-8", [usage] * 3))
    assert [(p["model"], p["output_tokens"]) for p in transcripts.request_parts(f)[0]["parts"]] == [
        ("claude-opus-4-8", 874), ("claude-fable-5", 279)]
    g = _write_lf(tmp_path / "g.jsonl", _model_request("r", "claude-sonnet-5", [usage]))
    assert [p["model"] for p in transcripts.request_parts(g)[0]["parts"]] == ["claude-fable-5", "claude-opus-4-8"]


def test_request_parts_iterations_of_zero_or_one_entry_are_the_max_reader_not_a_warning_t886(tmp_path):
    """The negative control: every single-model request carries a one-entry iterations (174,032 real lines)."""
    one = {"output_tokens": 7, "iterations": [_entry("m1", 99)]}
    zero = {"output_tokens": 5, "iterations": []}
    lines = _model_request("a", "m1", [one, {"output_tokens": 3}]) + _model_request("b", "m1", [zero])
    counts = {}
    got = transcripts.request_parts(_write_lf(tmp_path / "w.jsonl", lines), counts=counts)
    assert [(r["key"], [(p["model"], p["output_tokens"]) for p in r["parts"]]) for r in got] == [
        ("requestId:a", [("m1", 7)]), ("requestId:b", [("m1", 5)])]
    assert counts == {}


@pytest.mark.parametrize("iterations", ["x", {"a": 1}, 5, [_entry("m1", 1), "m2"], [_entry("m1", 1), {"model": "m2"}],
                                        [_entry("m1", 1), {"output_tokens": 3}], [_entry("m1", 1), _entry("m2", "many")],
                                        [_entry("m1", 1), _entry("", 2)], [_entry("m1", 1), _entry(["m2"], 2)]])
def test_request_parts_malformed_iterations_are_ignored_counted_and_never_raise_t886(tmp_path, iterations):
    lines = _model_request("r", "m1", [{"output_tokens": 7, "iterations": iterations}])
    counts = {}
    got = transcripts.request_parts(_write_lf(tmp_path / "w.jsonl", lines), counts=counts)   # no `skipped`: still no raise
    assert [(p["model"], p["output_tokens"]) for p in got[0]["parts"]] == [("m1", 7)]
    assert counts == {"bad_iterations": 1}


def test_request_parts_an_iterations_entry_without_a_split_is_none_and_counted_t886(tmp_path):
    no_split = _entry("m2", 5, 0, 100)
    del no_split["cache_creation"]
    lines = _model_request("r", "m1", [{"output_tokens": 7, "iterations": [_entry("m1", 1, 0, 100, 40), no_split]}])
    counts = {}
    got = transcripts.request_parts(_write_lf(tmp_path / "w.jsonl", lines), counts=counts)
    assert [(p["model"], p["cache_creation_1h_tokens"]) for p in got[0]["parts"]] == [("m1", 40), ("m2", None)]
    assert counts == {"split_missing": 1}


def test_read_requests_is_one_pass_and_lists_every_assistant_line_with_or_without_usage_t886(tmp_path):
    """The single pass (F-2): the file is opened once; with `meta` it also returns a record per non-skipped assistant
    line -- a line with no usage included, a bad-usage line and a SKIP_MODELS line excluded."""
    no_usage = _line({"type": "assistant", "requestId": "r", "uuid": "nu", "message": {"model": "m1"}})
    syn = _line({"type": "assistant", "requestId": "r", "uuid": "sy", "message": {"model": "<synthetic>", "usage": {"output_tokens": 1}}})
    bad = _line({"type": "assistant", "requestId": "r", "uuid": "bd", "message": {"model": "m1", "usage": "x"}})
    lines = _model_request("r", "m1", [{"output_tokens": 4}]) + [no_usage, syn, bad, _line({"type": "user", "uuid": "uu"})]
    f = _write_lf(tmp_path / "w.jsonl", lines)
    opened = []
    real = transcripts.iter_lines
    transcripts.iter_lines = lambda path: (opened.append(path), real(path))[1]
    try:
        skipped = []
        requests, seen = transcripts.read_requests(f, skipped, None, lambda obj: obj.get("uuid"))
    finally:
        transcripts.iter_lines = real
    assert len(opened) == 1 and skipped == [4]
    assert [(n, key, model, meta) for n, key, model, meta in seen] == [(1, ("requestId", "r"), "m1", "u-r-0"),
                                                                       (2, ("requestId", "r"), "m1", "nu")]
    assert [r["key"] for r in requests] == ["requestId:r"]
    assert transcripts.read_requests(f)[1] == []


def test_main_transcript_of_is_the_session_jsonl_next_to_the_session_folder(tmp_path):
    flat = tmp_path / "proj" / "sess-1" / "subagents" / "agent-aa.jsonl"
    assert transcripts.main_transcript_of(flat) == str(tmp_path / "proj" / "sess-1.jsonl")
    deep = tmp_path / "proj" / "sess-1" / "subagents" / "workflows" / "wf_x" / "agent-bb.jsonl"
    assert transcripts.main_transcript_of(deep) == str(tmp_path / "proj" / "sess-1.jsonl")      # the NEAREST ancestor
    nested = tmp_path / "proj" / "sess-1" / "subagents" / "x" / "subagents" / "agent-cc.jsonl"
    assert transcripts.main_transcript_of(nested) == str(tmp_path / "proj" / "sess-1" / "subagents" / "x.jsonl")
    assert transcripts.main_transcript_of(tmp_path / "proj" / "sess-1.jsonl") is None
    assert not (tmp_path / "proj").exists()                                                       # pure: no I/O


def test_find_agent_transcripts_answers_like_find_agent_transcript_for_every_id(tmp_path):
    root = tmp_path / "projects"
    _write_bytes(root / "p" / "s1" / "subagents" / "agent-one.jsonl", b"{}\n")
    _write_bytes(root / "p" / "s1" / "subagents" / "agent-two.jsonl", b"{}\n")
    _write_bytes(root / "p" / "s2" / "subagents" / "agent-two.jsonl", b"{}\n")          # ambiguous
    ids = ["one", "two", "missing", "../x", "", None, 5]
    assert transcripts.find_agent_transcripts(ids, root) == {i: transcripts.find_agent_transcript(i, root) for i in ids}
    assert transcripts.find_agent_transcripts(["one"], root)["one"].endswith("agent-one.jsonl")
    assert transcripts.find_agent_transcripts(["one"], tmp_path / "nowhere") == {"one": None}


def _model_line(model, text="t"):
    return _line({"type": "assistant", "message": {"model": model, "content": [{"type": "text", "text": text}]}})


def test_iter_models_rows(tmp_path):
    f = _write(tmp_path / "m.jsonl", [
        _model_line("opus-a"), "garbage", "", _line({"type": "user", "message": {"model": "ignored"}}),
        _model_line("<synthetic>"), _model_line(""), _line({"type": "assistant", "message": {"model": 5}}),
        _line({"type": "assistant", "message": "x"}), _line({"type": "assistant"}), _model_line("sonnet-b"),
        _model_line("opus-a")])
    assert list(transcripts.iter_models(f)) == ["opus-a", "sonnet-b", "opus-a"]  # M4: <synthetic> is skipped
    assert transcripts.SKIP_MODELS == frozenset({"<synthetic>"})
    assert list(transcripts.iter_models(_write(tmp_path / "e.jsonl", ["{}", "garbage"]))) == []  # I3
    with pytest.raises(OSError):  # I1
        list(transcripts.iter_models(tmp_path / "missing.jsonl"))


def test_iter_models_reads_a_line_with_u2028_whole_and_survives_bad_bytes_and_crlf(tmp_path):
    """I9 / I4 / I9b: one turn per assistant line, whatever the separator characters inside."""
    body = ("\n".join([_model_line("m-a", "x%sy" % LS), _model_line("m-b", "x%sy" % NEL)]) + "\n").encode("utf-8")
    f = _write_bytes(tmp_path / "ls.jsonl", body + b"\xff\xfe garbage\n" + (_model_line("m-c") + "\r\n").encode())
    assert list(transcripts.iter_models(f)) == ["m-a", "m-b", "m-c"]


def test_iter_models_skips_a_deep_line_and_keeps_reading(tmp_path):
    """I14: before this module tier_echo went silent on the WHOLE transcript at a RecursionError."""
    f = _write(tmp_path / "deep.jsonl", [_model_line("m-a"), "[" * 200000, _model_line("m-b")])
    assert list(transcripts.iter_models(f)) == ["m-a", "m-b"]
    assert list(tier_echo.iter_transcript_models(str(f))) == ["m-a", "m-b"]


# ---------------------------------------------------------------------------------------------------
# live_worker_files   (I12, the window boundary, the positional invariant, 5.8)
# ---------------------------------------------------------------------------------------------------


def _folder(tmp_path, session="sess-1"):
    folder = tmp_path / "proj" / session / "subagents"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def _agent_file(folder, name, mtime, lines=("{}",)):
    path = folder / ("agent-%s.jsonl" % name)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    os.utime(path, (mtime, mtime))
    return path


def test_live_worker_files_window_boundary_at_and_beyond(tmp_path):
    folder, now = _folder(tmp_path), 1_000_000
    _agent_file(folder, "at", now - 600)
    _agent_file(folder, "beyond", now - 601)
    _agent_file(folder, "fresh", now)
    got = transcripts.live_worker_files("sess-1", now, 600, root=tmp_path)
    assert [f.name for f in got] == ["agent-fresh.jsonl", "agent-at.jsonl"]  # newest first; now-601 is out


def test_live_worker_files_a_stale_file_is_never_opened(tmp_path, monkeypatch):
    """The positional invariant: the mtime test runs BEFORE is_finished."""
    folder, now = _folder(tmp_path), 1_000_000
    _agent_file(folder, "old", now - 5000)
    asked = []
    monkeypatch.setattr(transcripts, "is_finished", lambda p: asked.append(p) or False)
    assert transcripts.live_worker_files("sess-1", now, 600, root=tmp_path) == []
    assert asked == []


def test_live_worker_files_leaves_finished_out_and_counts_an_unreadable_one_live(tmp_path, monkeypatch):
    folder, now = _folder(tmp_path), 1_000_000
    _agent_file(folder, "done", now, [_line(_call("SubagentHandback"))])
    _agent_file(folder, "busy", now - 1, [_line(_call("Bash"))])
    _agent_file(folder, "locked", now - 2)
    real = transcripts.is_finished

    def stub(path):
        if Path(path).name == "agent-locked.jsonl":
            raise PermissionError("denied")
        return real(path)

    monkeypatch.setattr(transcripts, "is_finished", stub)
    got = transcripts.live_worker_files("sess-1", now, 600, root=tmp_path)
    assert [f.name for f in got] == ["agent-busy.jsonl", "agent-locked.jsonl"]


@pytest.mark.parametrize("sid", ["*", "../x", "a[b]", "", None, 5, "sess\n"])
def test_live_worker_files_unsafe_session_id_is_empty_with_a_matching_folder_present(tmp_path, sid):
    """5.8: one validator, here -- `*` would otherwise match the folder that exists."""
    _agent_file(_folder(tmp_path), "w", 1_000_000)
    assert transcripts.live_worker_files("sess-1", 1_000_000, 600, root=tmp_path) != []  # control
    assert transcripts.live_worker_files(sid, 1_000_000, 600, root=tmp_path) == []


def test_live_worker_files_root_none_uses_projects_root_and_a_missing_one_is_empty(tmp_path, monkeypatch):
    _agent_file(_folder(tmp_path), "w", 1_000_000)
    monkeypatch.setattr(transcripts, "projects_root", lambda: tmp_path)
    assert len(transcripts.live_worker_files("sess-1", 1_000_000, 600)) == 1
    monkeypatch.setattr(transcripts, "projects_root", lambda: tmp_path / "nowhere")
    assert transcripts.live_worker_files("sess-1", 1_000_000, 600) == []  # I6

    def no_home():
        raise RuntimeError("no home")

    monkeypatch.setattr(transcripts, "projects_root", no_home)
    with pytest.raises(RuntimeError):  # propagates: the caller (the hook main) turns it into count 0
        transcripts.live_worker_files("sess-1", 1_000_000, 600)


# ---------------------------------------------------------------------------------------------------
# D-0040: first_user_text / is_writer / live_worker_files(writer=...)
# ---------------------------------------------------------------------------------------------------


def _user(content):
    return json.dumps({"type": "user", "message": {"role": "user", "content": content}})


def _raw(tmp_path, lines, name="t.jsonl"):
    path = tmp_path / name
    path.write_text("".join(line + "\n" for line in lines), encoding="utf-8")
    return path


def test_first_user_text_string_content(tmp_path):
    assert transcripts.first_user_text(_raw(tmp_path, [_user("owns: C:\\x\\y.py"), _user("later")])) == "owns: C:\\x\\y.py"


def test_first_user_text_list_of_blocks_skips_the_non_text_ones(tmp_path):
    blocks = [{"type": "text", "text": "one"}, {"type": "image", "source": {}}, {"type": "text", "text": "two"}]
    assert transcripts.first_user_text(_raw(tmp_path, [_user(blocks)])) == "one\ntwo"


def test_first_user_text_a_list_with_no_text_block_is_empty_not_none(tmp_path):
    """E1: "" (a reader by the predicate), not None (an unknown, counted as a writer)."""
    got = transcripts.first_user_text(_raw(tmp_path, [_user([{"type": "image"}])]))
    assert got == ""
    assert transcripts.is_writer(_raw(tmp_path, [_user([{"type": "image"}])], "e1.jsonl"), lambda t: bool(t)) is False


def test_content_text_is_the_one_reader_of_a_message_content_fx5():
    """FX-5: a str as is; a list as the join of its text blocks (tool_result / image / a non-str text are not text,
    none -> ""); anything else None -- the same answers first_user_text gives (the tests around this one)."""
    blocks = [{"type": "text", "text": "one"}, {"type": "tool_result", "content": "no"}, {"type": "text", "text": 5},
              "stray", {"type": "image"}, {"type": "text", "text": "two"}]
    assert transcripts.content_text("as is") == "as is" and transcripts.content_text("") == ""
    assert transcripts.content_text(blocks) == "one\ntwo" and transcripts.content_text([{"type": "image"}]) == ""
    assert transcripts.content_text([]) == ""
    for other in (None, 5, {"type": "text", "text": "x"}):
        assert transcripts.content_text(other) is None


def test_first_user_text_empty_file_is_none(tmp_path):
    assert transcripts.first_user_text(_raw(tmp_path, [])) is None


def test_first_user_text_malformed_first_line_is_none(tmp_path):
    assert transcripts.first_user_text(_raw(tmp_path, ["{not json"])) is None
    assert transcripts.first_user_text(_raw(tmp_path, ["[1, 2]", json.dumps({"type": "assistant"})], "b.jsonl")) is None


def test_first_user_text_finds_a_user_line_behind_other_lines(tmp_path):
    """E2: a system line, a malformed one and an assistant one before the user line do not hide it."""
    lines = [json.dumps({"type": "system", "content": "x"}), "{not json", json.dumps({"type": "assistant"}), _user("the prompt")]
    assert transcripts.first_user_text(_raw(tmp_path, lines)) == "the prompt"


def test_first_user_text_the_first_user_line_decides(tmp_path):
    bad = json.dumps({"type": "user", "message": {"content": 5}})
    assert transcripts.first_user_text(_raw(tmp_path, [bad, _user("second")])) is None
    no_message = json.dumps({"type": "user"})
    assert transcripts.first_user_text(_raw(tmp_path, [no_message, _user("second")], "n.jsonl")) is None


def test_first_user_text_a_missing_file_raises_oserror(tmp_path):
    with pytest.raises(OSError):
        transcripts.first_user_text(tmp_path / "nowhere.jsonl")


def test_is_writer_follows_the_predicate_and_an_unknown_is_a_writer(tmp_path):
    has_owns = lambda text: "owns" in text  # noqa: E731
    assert transcripts.is_writer(_raw(tmp_path, [_user("owns: a")]), has_owns) is True
    assert transcripts.is_writer(_raw(tmp_path, [_user("read only")], "r.jsonl"), has_owns) is False
    assert transcripts.is_writer(_raw(tmp_path, [], "e.jsonl"), has_owns) is True  # None text: never a pass
    assert transcripts.is_writer(_raw(tmp_path, [_user("read only")], "r2.jsonl"), lambda t: None) is False  # falsy
    with pytest.raises(OSError):
        transcripts.is_writer(tmp_path / "nowhere.jsonl", has_owns)


# ---------------------------------------------------------------------------------------------------
# t-673: the worker's kind comes from the sidecar agent-<id>.meta.json (agentType) first
# ---------------------------------------------------------------------------------------------------

_REAL_META = {"agentType": "designer", "description": "opus: designer redraft t-043 dispatch C",
              "toolUseId": "toolu_01TVRwnrTkBoNN82n1ES72Cx", "spawnDepth": 1, "requestShape": "background",
              "requestNonInteractive": True}  # the shape of a real meta (keys read from a live one)


def _meta(path, content, raw=False):
    """Write the sidecar beside the transcript `path`; content is dumped as JSON unless raw (str/bytes)."""
    target = transcripts.meta_path(path)
    if isinstance(content, bytes):
        target.write_bytes(content)
    else:
        target.write_text(content if raw else json.dumps(content), encoding="utf-8")
    return target


def test_meta_path_is_the_sibling_meta_json(tmp_path):
    assert transcripts.meta_path(tmp_path / "agent-ab_1-2.jsonl") == tmp_path / "agent-ab_1-2.meta.json"
    assert transcripts.meta_path(str(tmp_path / "agent-x.jsonl")).name == "agent-x.meta.json"


def test_agent_type_reads_a_real_shaped_meta(tmp_path):
    path = _raw(tmp_path, [_user("x")], "agent-a.jsonl")
    _meta(path, _REAL_META)
    assert transcripts.agent_type(path) == "designer"
    assert transcripts.read_meta(path) == _REAL_META
    path2 = _raw(tmp_path, [], "agent-b.jsonl")
    _meta(path2, b"\xef\xbb\xbf" + json.dumps({"agentType": "builder"}).encode("utf-8"))  # a BOM is tolerated
    assert transcripts.agent_type(path2) == "builder"


def test_agent_type_a_missing_meta_is_none(tmp_path):
    path = _raw(tmp_path, [_user("x")], "agent-a.jsonl")
    assert transcripts.agent_type(path) is None and transcripts.read_meta(path) is None


def test_agent_type_a_malformed_meta_is_none_and_never_raises(tmp_path):
    for i, bad in enumerate(("{not json", "", "[1, 2]", '"builder"', "null", "[" * 200_000)):
        path = _raw(tmp_path, [], "agent-m%d.jsonl" % i)
        _meta(path, bad, raw=True)
        assert transcripts.agent_type(path) is None, bad[:20]
    path = _raw(tmp_path, [], "agent-bin.jsonl")
    _meta(path, b"\xff\xfe\x00{")  # undecodable bytes
    assert transcripts.agent_type(path) is None


def test_agent_type_a_missing_or_non_str_field_is_none(tmp_path):
    for i, content in enumerate(({}, {"agentType": None}, {"agentType": 5}, {"agentType": ["builder"]},
                                 {"agentType": {"k": "builder"}}, {"agentType": ""}, {"other": "builder"})):
        path = _raw(tmp_path, [], "agent-f%d.jsonl" % i)
        _meta(path, content)
        assert transcripts.agent_type(path) is None, content


def test_is_writer_a_builder_meta_is_a_writer_whatever_the_prompt_says(tmp_path):
    """E3: no owns in the prompt, and the predicate would say no -- the meta decides."""
    path = _raw(tmp_path, [_user("read only")], "agent-b.jsonl")
    assert transcripts.is_writer(path, lambda t: False) is False  # control: without the meta, a reader
    _meta(path, {"agentType": "builder"})
    assert transcripts.is_writer(path, lambda t: False) is True


def test_is_writer_a_reader_kind_with_an_owns_prompt_is_a_writer(tmp_path):
    """E4: the dispatch side counts a reader whose prompt carries an owns path as a writer; so does this side."""
    path = _raw(tmp_path, [_user("owns: C:\\x\\y.py")], "agent-c.jsonl")
    _meta(path, {"agentType": "critic"})
    assert transcripts.is_writer(path, lambda t: "owns" in t) is True
    quiet = _raw(tmp_path, [_user("review it")], "agent-c2.jsonl")
    _meta(quiet, {"agentType": "critic"})
    assert transcripts.is_writer(quiet, lambda t: "owns" in t) is False  # control: the prompt decides


def test_is_writer_a_reader_kind_without_a_first_line_is_a_reader(tmp_path):
    """E5: the meta is the stronger carrier; the control (no meta, no first line) is a writer."""
    path = _raw(tmp_path, [], "agent-e5.jsonl")
    _meta(path, {"agentType": "critic"})
    assert transcripts.is_writer(path, lambda t: True) is False
    bare = _raw(tmp_path, [], "agent-bare.jsonl")
    assert transcripts.is_writer(bare, lambda t: False) is True
    bad = _raw(tmp_path, [], "agent-bad.jsonl")
    _meta(bad, "{not json", raw=True)
    assert transcripts.is_writer(bad, lambda t: False) is True  # E2: a bad meta is no kind: unknown -> writer
    nostr = _raw(tmp_path, [], "agent-nostr.jsonl")
    _meta(nostr, {"agentType": 5})
    assert transcripts.is_writer(nostr, lambda t: False) is True


def test_permission_audit_reads_the_agent_type_through_transcripts(tmp_path, monkeypatch):
    """The ONE meta reader: permission_audit's snapshot labels a subagent by transcripts.agent_type."""
    import permission_audit as pa
    projects = tmp_path / "projects"
    folder = projects / "sess" / "subagents"
    folder.mkdir(parents=True)
    for name, meta in (("agent-b", {"agentType": "builder"}), ("agent-n", None), ("agent-x", {"agentType": 5})):
        (folder / (name + ".jsonl")).write_text("{}\n", encoding="utf-8")
        if meta is not None:
            (folder / (name + ".meta.json")).write_text(json.dumps(meta), encoding="utf-8")
    monkeypatch.setattr(pa, "CLAUDE_PROJECTS", projects)
    labels = {p.stem: kind for p, kind, _size in pa.snapshot_transcripts()}
    assert labels == {"agent-b": "builder", "agent-n": "subagent", "agent-x": "subagent"}
    assert ".meta.json" not in (TOOLS / "permission_audit.py").read_text(encoding="utf-8")  # no second reader
    assert ".meta.json" in (TOOLS / "transcripts.py").read_text(encoding="utf-8")  # control, same shape


def test_live_worker_files_writer_keeps_only_what_the_predicate_accepts(tmp_path):
    folder, now = _folder(tmp_path), 1_000_000
    _agent_file(folder, "w", now, [_user("owns: a")])
    _agent_file(folder, "r", now - 1, [_user("read only")])
    _agent_file(folder, "u", now - 2, [])  # unknown first line: is_writer says writer
    seen = []

    def writer(path):
        seen.append(Path(path).name)
        return transcripts.is_writer(path, lambda text: "owns" in text)

    got = transcripts.live_worker_files("sess-1", now, 600, root=tmp_path, writer=writer)
    assert [f.name for f in got] == ["agent-w.jsonl", "agent-u.jsonl"]
    assert sorted(seen) == ["agent-r.jsonl", "agent-u.jsonl", "agent-w.jsonl"]  # the stub was called
    everything = transcripts.live_worker_files("sess-1", now, 600, root=tmp_path)  # writer=None: as before
    assert [f.name for f in everything] == ["agent-w.jsonl", "agent-r.jsonl", "agent-u.jsonl"]


def test_live_worker_files_a_writer_that_raises_counts_the_file_live(tmp_path):
    """E4."""
    folder, now = _folder(tmp_path), 1_000_000
    _agent_file(folder, "boom", now, [_user("read only")])

    def writer(path):
        raise PermissionError("denied")

    assert [f.name for f in transcripts.live_worker_files("sess-1", now, 600, root=tmp_path, writer=writer)] == [
        "agent-boom.jsonl"]


def test_live_worker_files_an_unopenable_transcript_is_counted_by_the_real_writer(tmp_path, monkeypatch):
    """E3: the open raises OSError inside is_writer; live_worker_files keeps the file (today's branch)."""
    folder, now = _folder(tmp_path), 1_000_000
    _agent_file(folder, "locked", now, [_user("read only")])

    def no_open(path):
        raise PermissionError("denied")

    monkeypatch.setattr(transcripts, "iter_lines", no_open)
    got = transcripts.live_worker_files("sess-1", now, 600, root=tmp_path, writer=lambda f: transcripts.is_writer(f, lambda t: False))
    assert [f.name for f in got] == ["agent-locked.jsonl"]


def test_live_worker_files_a_finished_worker_is_not_asked_whether_it_writes(tmp_path):
    folder, now = _folder(tmp_path), 1_000_000
    _agent_file(folder, "done", now, [_user("owns: a"), _line(_call("SubagentHandback"))])
    asked = []
    got = transcripts.live_worker_files("sess-1", now, 600, root=tmp_path, writer=lambda f: asked.append(f) or True)
    assert got == [] and asked == []


# ---------------------------------------------------------------------------------------------------
# the parallel cap through dispatch_gate: the root is passed, unreadable and vanished files (5.1-5.3)
# ---------------------------------------------------------------------------------------------------


def test_recent_subagent_files_passes_the_root_and_the_window(tmp_path, monkeypatch):
    """5.1: the root ALWAYS comes from dispatch_gate._projects_root(), so a test's swap reaches the glob."""
    seen = []

    def stub(sid, now, window, root=None, writer=None):
        seen.append((sid, now, window, root, callable(writer)))  # t-673: the writer filter is always passed
        return []

    monkeypatch.setattr(dispatch_gate.transcripts, "live_worker_files", stub)
    monkeypatch.setattr(dispatch_gate, "_projects_root", lambda: tmp_path)
    assert dispatch_gate.recent_subagent_files({"session_id": "s1"}, now=42) == []
    assert seen == [("s1", 42, dispatch_gate.PARALLEL_WINDOW_SECONDS, tmp_path, True)]


def test_cap_full_cap_of_fresh_files_one_unreadable_still_blocks(tmp_path, monkeypatch):
    """M1: an is_finished that raises counts the file LIVE; it never lets the (cap+1)-th worker through."""
    _subagents_home(tmp_path, monkeypatch, n_fresh=_cap())
    real = dispatch_gate.transcripts.is_finished
    asked = []

    def stub(path):
        asked.append(Path(path).name)
        if Path(path).name == "agent-fresh0.jsonl":
            raise PermissionError("denied")
        return real(path)

    monkeypatch.setattr(dispatch_gate.transcripts, "is_finished", stub)
    code, message, note = dispatch_gate.parallel_cap_check(_cap_payload())
    assert "agent-fresh0.jsonl" in asked  # the stub was called
    assert code == 2 and "%d writing-worker transcripts" % _cap() in message and note == ""


def test_cap_full_cap_fresh_one_vanished_between_glob_and_stat_passes_one_more_still_blocks(tmp_path, monkeypatch):
    """5.3 / M10: FileNotFoundError drops that one file; it does not zero the count."""
    _subagents_home(tmp_path, monkeypatch, n_fresh=_cap())
    hits = _stat_raises(monkeypatch, "agent-fresh0.jsonl", FileNotFoundError("gone"))
    assert dispatch_gate.parallel_cap_check(_cap_payload()) == (0, "", "")  # cap-1 counted
    assert hits  # the stat stub was reached


def test_cap_plus_one_fresh_one_vanished_still_blocks(tmp_path, monkeypatch):
    _subagents_home(tmp_path, monkeypatch, n_fresh=_cap() + 1)
    hits = _stat_raises(monkeypatch, "agent-fresh0.jsonl", FileNotFoundError("gone"))
    code, message, _note = dispatch_gate.parallel_cap_check(_cap_payload())
    assert hits and code == 2 and "%d writing-worker transcripts" % _cap() in message  # cap counted: exactly the cap


def test_cap_full_cap_fresh_one_stat_permission_error_still_blocks(tmp_path, monkeypatch):
    """5.3 / M8: any other OSError on stat counts the file live (door: budget-skip)."""
    _subagents_home(tmp_path, monkeypatch, n_fresh=_cap())
    hits = _stat_raises(monkeypatch, "agent-fresh0.jsonl", PermissionError("denied"))
    code, message, _note = dispatch_gate.parallel_cap_check(_cap_payload())
    assert hits and code == 2 and "%d writing-worker transcripts" % _cap() in message


def test_cap_with_a_finished_one_of_the_cap_reuses_the_existing_witness(tmp_path, monkeypatch):
    """Control that the helper used here is the one the existing :2078 test uses (not a copy)."""
    folder = _subagents_home(tmp_path, monkeypatch, n_fresh=_cap())
    assert dispatch_gate.parallel_cap_check(_cap_payload())[0] == 2
    _finish(folder, "fresh0")
    assert dispatch_gate.parallel_cap_check(_cap_payload()) == (0, "", "")


# ---------------------------------------------------------------------------------------------------
# I13 -- transcripts does not import
# ---------------------------------------------------------------------------------------------------


def test_cap_without_the_module_counts_every_fresh_file_live_with_the_sentence(tmp_path, monkeypatch):
    """5.7 / M11: an import failure keeps the cap's direction (an unknown is never a pass) and says so."""
    folder = _subagents_home(tmp_path, monkeypatch, n_fresh=_cap())
    monkeypatch.setattr(dispatch_gate, "transcripts", None)
    code, message, note = dispatch_gate.parallel_cap_check(_cap_payload())
    assert code == 2 and "%d writing-worker transcripts" % _cap() in message and note == ""
    assert dispatch_gate.TRANSCRIPTS_MISSING in message
    assert "tools/transcripts.py did not import -- every fresh worker file counted live; door: budget-skip" in message
    assert "budget-skip: <reason>" in message
    _finish(folder, "fresh0")  # finished cannot be told without the module: still counted
    assert dispatch_gate.parallel_cap_check(_cap_payload())[0] == 2


def test_cap_without_the_module_under_the_cap_passes_with_the_sentence(tmp_path, monkeypatch):
    _subagents_home(tmp_path, monkeypatch, n_fresh=_cap() - 1, n_old=_cap() + 1)  # the window test needs no module
    monkeypatch.setattr(dispatch_gate, "transcripts", None)
    code, message, note = dispatch_gate.parallel_cap_check(_cap_payload())
    assert (code, message) == (0, "")
    assert note.startswith("PARALLEL CAP:") and dispatch_gate.TRANSCRIPTS_MISSING in note


def test_cap_without_the_module_budget_skip_carries_the_sentence(tmp_path, monkeypatch):
    _subagents_home(tmp_path, monkeypatch, n_fresh=_cap() + 1)
    monkeypatch.setattr(dispatch_gate, "transcripts", None)
    payload = _cap_payload()
    payload["tool_input"]["prompt"] = "go\nbudget-skip: the others are idle"
    code, message, note = dispatch_gate.parallel_cap_check(payload)
    assert (code, message) == (0, "")
    assert note.startswith("BUDGET-SKIP: %d writing workers" % (_cap() + 1)) and "the others are idle" in note
    assert note.endswith(dispatch_gate.TRANSCRIPTS_MISSING)


def test_cap_without_the_module_unsafe_ids_never_reach_a_glob(tmp_path, monkeypatch):
    _subagents_home(tmp_path, monkeypatch, n_fresh=_cap() + 1)
    monkeypatch.setattr(dispatch_gate, "transcripts", None)
    assert len(dispatch_gate.recent_subagent_files({"session_id": "sess-1"})) == _cap() + 1  # control: `*` would match this
    for sid in ("*", "../x", "a[b]", "", None, 7):
        assert dispatch_gate.recent_subagent_files({"session_id": sid}) == []


def test_cap_without_the_module_a_vanished_file_is_dropped(tmp_path, monkeypatch):
    _subagents_home(tmp_path, monkeypatch, n_fresh=_cap() + 1)
    monkeypatch.setattr(dispatch_gate, "transcripts", None)
    hits = _stat_raises(monkeypatch, "agent-fresh0.jsonl", FileNotFoundError("gone"))
    assert len(dispatch_gate.recent_subagent_files({"session_id": "sess-1"})) == _cap()  # cap+1 fresh, 1 vanished
    assert hits


def test_cap_without_the_module_any_other_stat_error_counts_the_file_live(tmp_path, monkeypatch):
    _subagents_home(tmp_path, monkeypatch, n_fresh=_cap())
    monkeypatch.setattr(dispatch_gate, "transcripts", None)
    hits = _stat_raises(monkeypatch, "agent-fresh0.jsonl", PermissionError("denied"))
    assert len(dispatch_gate.recent_subagent_files({"session_id": "sess-1"})) == _cap()
    assert hits


def _alone(folder, *modules):
    """`folder` holding only the named tools/ modules, outside any repo (no `tools` package to import from)."""
    folder.mkdir(parents=True)
    for name in modules:
        shutil.copy(TOOLS / name, folder / name)
    return folder


def test_dispatch_gate_alone_in_a_folder_really_fails_to_import_the_module_and_still_caps(tmp_path):
    """The real ImportError branch (the sandbox of test_critic_snapshot copies dispatch_gate alone too)."""
    home = tmp_path / "home"
    folder = home / ".claude" / "projects" / "p" / "sess-1" / "subagents"
    folder.mkdir(parents=True)
    for i in range(_cap()):
        (folder / ("agent-w%d.jsonl" % i)).write_text("{}\n", encoding="utf-8")
    env = {**os.environ, "USERPROFILE": str(home), "HOME": str(home)}

    def run(tools):
        code = ("import json, sys; sys.path.insert(0, %r); import dispatch_gate as g; "
                "print(json.dumps([g.transcripts is None, list(g.parallel_cap_check(%r))]))"
                % (str(tools), _cap_payload()))
        done = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True,
                              encoding="utf-8", env=env, cwd=str(tmp_path))
        assert done.returncode == 0, done.stderr
        return json.loads(done.stdout)

    missing, (cap_code, message, _note) = run(_alone(tmp_path / "a", "dispatch_gate.py"))
    assert missing is True and cap_code == 2 and "tools/transcripts.py did not import" in message
    present, (cap_code, message, _note) = run(_alone(tmp_path / "b", "dispatch_gate.py", "transcripts.py"))
    assert present is False and cap_code == 2 and "did not import" not in message  # control: the module is found


@pytest.fixture
def ses_tmp(tmp_path):
    return Session(tmp_path)


def test_agent_budget_without_the_module_fails_open_silently(ses_tmp, monkeypatch):
    ses = ses_tmp
    ses.worker("w1", [_assistant(450000)])
    payload = {"agent_id": "w1", "tool_name": "Edit", "tool_input": {"file_path": "x.py"}}
    assert ses.run(payload).returncode == 2  # control: the fixture really is over the STOP cap
    monkeypatch.setattr(agent_budget, "transcripts", None)
    assert agent_budget.evaluate({"transcript_path": str(ses.main), "cwd": str(ses.tmp), **payload}) == (0, "", [])


def test_agent_budget_alone_in_a_folder_exits_zero_and_silent(ses_tmp, tmp_path):
    ses = ses_tmp
    ses.worker("w1", [_assistant(450000)])
    payload = {"transcript_path": str(ses.main), "cwd": str(ses.tmp), "agent_id": "w1", "tool_name": "Edit",
               "tool_input": {"file_path": "x.py"}}

    def run(tools):  # the script directory is on sys.path, as for the real hook command
        return subprocess.run([sys.executable, str(tools / "agent_budget.py")], input=json.dumps(payload),
                              capture_output=True, text=True, encoding="utf-8", env={**os.environ, **ses.env},
                              cwd=str(tmp_path))

    with_it = run(_alone(tmp_path / "with", "agent_budget.py", "transcripts.py"))
    assert with_it.returncode == 2  # control: with the module the same payload is blocked
    alone = run(_alone(tmp_path / "without", "agent_budget.py"))
    assert (alone.returncode, alone.stdout, alone.stderr) == (0, "", "")


# ---------------------------------------------------------------------------------------------------
# agent_budget: one splitter, thin delegates (5.4)
# ---------------------------------------------------------------------------------------------------


def _calls_splitlines(source: str) -> bool:
    return "splitlines(" in source


def test_agent_budget_has_no_splitlines_left():
    assert _calls_splitlines((TOOLS / "dispatch_gate.py").read_text(encoding="utf-8"))  # positive control, same shape
    assert not _calls_splitlines((TOOLS / "agent_budget.py").read_text(encoding="utf-8"))


def test_agent_budget_reads_u2028_lines_whole_in_the_incremental_scan(tmp_path):
    block = {"type": "tool_use", "id": "toolu_a", "name": "Bash",
             "input": {"command": "python -m pytest tools/x.py # a%sb" % LS}}
    cmd = _line({"type": "assistant", "message": {"content": [block]}})  # ensure_ascii=False keeps U+2028 raw
    usage = _usage_line(260000, text="p%sq" % LS)
    assert len(cmd.splitlines()) > 1 and len(usage.splitlines()) > 1  # control: splitlines would cut both
    f = _write(tmp_path / "w.jsonl", [cmd, usage])
    state = agent_budget.update_counts(f, dict(agent_budget.FRESH_STATE))
    assert state["tests"] == 1 and state["ctx"] == 260000
    assert agent_budget.context_size(f) == 260000


def test_agent_budget_delegates_are_the_module_readers(tmp_path):
    done = _write(tmp_path / "d.jsonl", [_line(_call("SubagentHandback"))])
    assert agent_budget.is_finished(done) is True and agent_budget.context_size(done) is None
    (path, is_worker) = agent_budget.resolve_transcript(
        {"transcript_path": str(tmp_path / "proj" / "sess.jsonl"), "agent_id": "../x"})
    assert (path, is_worker) == (None, False)


# ---------------------------------------------------------------------------------------------------
# journal_echo and tier_echo through the module
# ---------------------------------------------------------------------------------------------------


def test_journal_echo_two_transcripts_for_one_id_is_silence_not_a_wrong_mismatch(tmp_path, monkeypatch):
    """F8 (c): with two files the first match could be ANOTHER worker's; nothing is printed."""
    monkeypatch.setattr(journal_echo, "_projects_root", lambda: _projects(tmp_path))
    _write_agent_transcript(tmp_path, "dupe", [_assistant_line("claude-opus-4-8")], sess="s1")
    obj = _delegated_obj(worker_ref="agent:dupe", model="sonnet")
    assert journal_echo._collect_tier_events([obj], [])[0][1] == "mismatch"  # control: one file measures
    _write_agent_transcript(tmp_path, "dupe", [_assistant_line("claude-opus-4-8")], sess="s2")
    assert journal_echo._find_agent_transcript("dupe") is None
    assert journal_echo._collect_tier_events([obj], []) == []


def test_journal_echo_unsafe_id_and_missing_home_find_nothing(tmp_path, monkeypatch):
    _write_agent_transcript(tmp_path, "abc", [_assistant_line("m")])
    monkeypatch.setattr(journal_echo, "_projects_root", lambda: _projects(tmp_path))
    assert journal_echo._find_agent_transcript("abc") is not None  # control
    for bad in ("*", "a[b]", "../x"):
        assert journal_echo._find_agent_transcript(bad) is None

    def no_home():
        raise RuntimeError("no home")

    monkeypatch.setattr(journal_echo, "_projects_root", no_home)
    assert journal_echo._find_agent_transcript("abc") is None


def test_journal_echo_and_tier_echo_share_the_module_and_its_skip_set():
    assert tier_echo.SKIP_MODELS == transcripts.SKIP_MODELS
    assert journal_echo._projects_root is transcripts.projects_root
    assert journal_echo.transcripts.find_agent_transcript is not None


def test_tier_echo_reads_a_model_line_with_u2028_as_one_turn(tmp_path):
    f = _write(tmp_path / "t.jsonl", [_model_line("m-a", "x%sy" % LS), _model_line("<synthetic>"), _model_line("m-b")])
    assert list(tier_echo.iter_transcript_models(str(f))) == ["m-a", "m-b"]
    gen = tier_echo.iter_transcript_models(str(tmp_path / "missing.jsonl"))
    with pytest.raises(OSError):
        next(gen)
