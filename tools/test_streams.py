"""Tests for tools/streams.py -- the one stream setup of the tools/ scripts outside the mechanism chain (B-449).

Keys: S1 helper behaviour on streams the test builds (never the host console); S2 a subprocess whose stdout is
cp1251 gets UTF-8 bytes after the call (control: without it the bytes are cp1251), and importing has no side
effect; G the two files that run outside this tree (calibration_counts, permission_audit) still exit 0 with
tools/streams.py absent; S3 the census -- no stream reconfigure call in tools/*.py outside the mechanism chain
except in streams.py; S4 -- no chain link reaches tools/streams.py through any chain of tools/ imports.
One function serves the real check and its control in S3 (`offenders`) and in S4 (`chain_reaches`).
"""
import ast
import io
import os
import pathlib
import shutil
import subprocess
import sys

import pytest

TOOLS = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import mechanism_gate as mg  # noqa: E402
import streams  # noqa: E402
from test_mechanism_gate import _tools_module_names, _transitive_tool_module_closure  # noqa: E402

CALL = ".reconfigure" + "("      # split, so the line census (grep for the call) does not count this file
EM_DASH, CYR_I = "—", "й"
EM_DASH_UTF8 = b"\xe2\x80\x94"


# ---------------------------------------------------------------- S1 helper behaviour

class Recorder:
    """A stream-like object: records every reconfigure call; raises `fail` when given."""

    def __init__(self, fail=None):
        self.calls, self.fail = [], fail

    def reconfigure(self, **kw):
        self.calls.append(kw)
        if self.fail is not None:
            raise self.fail


class RejectsNewline(Recorder):
    """A reconfigure that does not know the `newline` option (TypeError) and applies the rest otherwise."""

    def __init__(self):
        super().__init__()
        self.applied = []

    def reconfigure(self, **kw):
        self.calls.append(kw)
        if "newline" in kw:
            raise TypeError("reconfigure() got an unexpected keyword argument 'newline'")
        self.applied.append(kw)


def narrow(codec="cp1251"):
    return io.TextIOWrapper(io.BytesIO(), encoding=codec)


def closed():
    stream = narrow()
    stream.close()
    return stream


def install(monkeypatch, out, err):
    monkeypatch.setattr(sys, "stdout", out)
    monkeypatch.setattr(sys, "stderr", err)


def is_utf8_replace(stream):
    return stream.encoding == "utf-8" and stream.errors == "replace"


def test_s1_cp1251_streams_become_utf8_replace_on_both(monkeypatch):
    out, err = narrow(), narrow("cp866")
    install(monkeypatch, out, err)
    streams.utf8_stdio()
    assert is_utf8_replace(out) and is_utf8_replace(err)
    out.write(EM_DASH)
    out.flush()
    assert out.buffer.getvalue() == EM_DASH_UTF8                 # cp1251 would have written b"\x97"


WEIRD = {
    "StringIO": io.StringIO,
    "None": lambda: None,
    "object": object,
    "closed wrapper": closed,
    "OSError": lambda: Recorder(fail=OSError(5, "boom")),
    "ValueError": lambda: Recorder(fail=ValueError("boom")),
    "TypeError": lambda: Recorder(fail=TypeError("boom")),
}


@pytest.mark.parametrize("weird", WEIRD.values(), ids=WEIRD.keys())
@pytest.mark.parametrize("position", ["stdout", "stderr"])
def test_s1_a_stream_that_cannot_be_reconfigured_is_left_alone_and_the_other_is_still_done(monkeypatch, weird, position):
    good, bad = narrow(), weird()
    install(monkeypatch, *((bad, good) if position == "stdout" else (good, bad)))
    streams.utf8_stdio()                                           # no raise
    assert is_utf8_replace(good)
    if isinstance(bad, io.StringIO):
        assert bad.getvalue() == ""
    if isinstance(bad, Recorder):
        assert len(bad.calls) == 1                                 # it was tried, once


def test_s1_a_stream_missing_from_sys_is_not_an_error(monkeypatch):
    monkeypatch.delattr(sys, "stderr")
    good = narrow()
    monkeypatch.setattr(sys, "stdout", good)
    streams.utf8_stdio()
    assert is_utf8_replace(good)


def test_s1_calling_twice_gives_the_same_state_and_the_last_call_wins(monkeypatch):
    out, err = narrow(), narrow()
    install(monkeypatch, out, err)
    streams.utf8_stdio()
    streams.utf8_stdio()
    assert is_utf8_replace(out) and is_utf8_replace(err)
    rec = Recorder()
    install(monkeypatch, rec, Recorder())
    streams.utf8_stdio(newline="\n")
    streams.utf8_stdio()
    assert rec.calls == [{"encoding": "utf-8", "errors": "replace", "newline": "\n"},
                         {"encoding": "utf-8", "errors": "replace"}]


def test_s1_a_stream_swapped_in_after_the_import_is_the_one_handled(monkeypatch):
    # `streams` was imported at the top of this module; the streams below did not exist then
    first, second = Recorder(), Recorder()
    install(monkeypatch, first, first)
    streams.utf8_stdio()
    install(monkeypatch, second, second)
    streams.utf8_stdio()
    assert len(first.calls) == 2 and len(second.calls) == 2


def test_s1_sys_stdout_stays_the_same_object(monkeypatch):
    out, err = narrow(), narrow()
    install(monkeypatch, out, err)
    streams.utf8_stdio(newline="\n")
    assert sys.stdout is out and sys.stderr is err


def test_s1_newline_is_passed_only_when_given(monkeypatch):
    rec_default, rec_lf = Recorder(), Recorder()
    install(monkeypatch, rec_default, Recorder())
    streams.utf8_stdio()
    install(monkeypatch, rec_lf, Recorder())
    streams.utf8_stdio(newline="\n")
    assert rec_default.calls == [{"encoding": "utf-8", "errors": "replace"}]       # no `newline` key, not even None
    assert rec_lf.calls == [{"encoding": "utf-8", "errors": "replace", "newline": "\n"}]


def test_s1_a_reconfigure_that_rejects_newline_leaves_the_stream_unchanged_without_a_retry(monkeypatch):
    out, err = RejectsNewline(), RejectsNewline()
    install(monkeypatch, out, err)
    streams.utf8_stdio(newline="\n")                               # no raise
    assert out.applied == [] and err.applied == []                 # unchanged: the helper does not retry without it
    assert len(out.calls) == 1 and len(err.calls) == 1


def test_s1_stdin_is_never_touched(monkeypatch):
    stdin = io.TextIOWrapper(io.BytesIO(), encoding="cp1251")
    monkeypatch.setattr(sys, "stdin", stdin)
    install(monkeypatch, narrow(), narrow())
    streams.utf8_stdio()
    assert stdin.encoding == "cp1251"


def test_s1_the_real_capture_streams_survive_the_call(capsys):
    streams.utf8_stdio(newline="\n")
    print(EM_DASH + CYR_I)
    assert capsys.readouterr().out == EM_DASH + CYR_I + "\n"       # still a str, the capture still works


# ---------------------------------------------------------------- S2 a subprocess on a cp1251 pipe

def child_env():
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONUTF8", "PYTHONPATH")}
    env["PYTHONIOENCODING"] = "cp1251"
    return env


def run_child(body):
    code = f"import sys; sys.path.insert(0, {str(TOOLS)!r}); import streams; {body}"
    return subprocess.run([sys.executable, "-c", code], capture_output=True, env=child_env(), timeout=120)


def test_s2_a_cp1251_pipe_gets_utf8_bytes_after_the_call():
    done = run_child("streams.utf8_stdio(); sys.stdout.write('\\u2014\\u0439'); sys.stderr.write('\\u2014')")
    assert done.returncode == 0, done.stderr
    assert done.stdout.rstrip(b"\r\n") == (EM_DASH + CYR_I).encode("utf-8")
    assert done.stderr.rstrip(b"\r\n") == EM_DASH_UTF8


def test_s2_control_without_the_call_the_bytes_are_cp1251():
    done = run_child("sys.stdout.write('\\u2014\\u0439')")
    assert done.returncode == 0, done.stderr
    assert done.stdout.rstrip(b"\r\n") == b"\x97\xe9"


def test_s2_importing_the_module_changes_no_stream():
    done = run_child("sys.stdout.write(sys.stdout.encoding + ' ' + sys.stderr.encoding)")
    assert done.stdout == b"cp1251 cp1251"


# ---------------------------------------------------------------- G the files that run outside this tree

def copy_alone(directory, names):
    for name in names:
        shutil.copy(TOOLS / name, directory / name)


def run_in(directory, *args):
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    return subprocess.run([sys.executable, *args], capture_output=True, env=env, cwd=str(directory), timeout=120)


GUARDED = {"calibration_counts": ["calibration_counts.py"],
           "permission_audit": ["permission_audit.py", "hygiene_gate.py"]}


@pytest.mark.parametrize("module", GUARDED)
def test_g_a_guarded_file_runs_without_streams_and_uses_it_when_present(tmp_path, module):
    probe = f"import {module} as m; print(m.streams is None)"
    here = tmp_path / "alone"
    here.mkdir()
    copy_alone(here, GUARDED[module])
    absent = run_in(here, "-c", probe)
    assert absent.returncode == 0 and absent.stdout.strip() == b"True", absent.stderr       # the no-op fallback
    helped = run_in(here, f"{module}.py", "--help")
    assert helped.returncode == 0 and b"usage" in helped.stdout.lower(), helped.stderr
    present = run_in(TOOLS, "-c", probe)                                                   # control: the real tree
    assert present.returncode == 0 and present.stdout.strip() == b"False", present.stderr


# ---------------------------------------------------------------- S3 the census

KEPT = {       # file name -> the reason a deliberate copy of the reconfigure loop stays outside the chain
    "language_sites.py": "its own copy (spec t-2065 2.7), inert until node N3 puts it into the mechanism chain "
                         "(tools/mechanism_gate.py); REMOVE this row at N3",
}


def census(directory):
    """({file name: number of `.reconfigure` attribute nodes}, {file name: why it could not be counted}) for
    directory/*.py. AST, not text: an alias counts, a string or a docstring does not."""
    counts, unreadable = {}, {}
    for path in sorted(directory.glob("*.py")):
        try:
            tree = ast.parse(path.read_bytes(), filename=path.name)
        except (SyntaxError, ValueError, RecursionError, MemoryError) as exc:
            unreadable[path.name] = f"{type(exc).__name__}: {str(exc).splitlines()[0] if str(exc) else ''}"
            continue
        counts[path.name] = sum(1 for n in ast.walk(tree) if isinstance(n, ast.Attribute) and n.attr == "reconfigure")
    return counts, unreadable


def in_chain(rel):
    return mg.mechanism_paths([rel]) == [rel]


def offenders(directory, kept=KEPT):
    """Messages: a file with a direct call outside the chain (not streams.py, not in `kept`), and a file the
    census cannot read -- an uncounted file is not a clean one."""
    counts, unreadable = census(directory)
    found = [f"tools/{name} cannot be counted ({why}) -- fix the file; the census reads every tools/*.py"
             for name, why in unreadable.items()]
    for name, n in counts.items():
        if n and name != "streams.py" and name not in kept and not in_chain(f"tools/{name}"):
            found.append(f"tools/{name} calls {CALL} {n} time(s) outside the mechanism chain -- call "
                         f"streams.utf8_stdio() instead; a chain link keeps its own copy; a deliberate copy "
                         f"goes into KEPT with its reason")
    return found


def put(directory, files):
    directory.mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        (directory / name).write_bytes(text if isinstance(text, bytes) else text.encode("utf-8"))
    return directory


COPY = "import sys\nsys.stdout" + CALL + 'encoding="utf-8")\n'


def test_s3_no_tool_outside_the_chain_carries_its_own_stream_reconfigure():
    found = offenders(TOOLS)
    assert not found, "\n".join(found)


def test_s3_positive_control_the_real_census_sees_the_helper_and_a_chain_link():
    counts, unreadable = census(TOOLS)
    assert not unreadable
    assert counts["streams.py"] == 1 and counts["journal_echo.py"] >= 1
    assert in_chain("tools/journal_echo.py") and not in_chain("tools/streams.py")


def test_s3_negative_control_a_copy_in_a_scratch_directory_is_an_offender(tmp_path):
    put(tmp_path, {"x.py": COPY})
    found = offenders(tmp_path)
    assert len(found) == 1 and found[0].startswith(f"tools/x.py calls {CALL} 1 time(s) outside the mechanism chain")


def test_s3_exact_file_match_a_neighbour_of_a_link_is_not_exempt(tmp_path):
    # usage_report.py is outside the mechanism net (test_mechanism_gate pins it), so it is the non-exempt neighbour of this test
    put(tmp_path, {"piles.py": COPY, "usage_report.py": COPY, "mechanism_gate.py": COPY,
                   "test_mechanism_gate.py": COPY, "streams.py": COPY})
    found = offenders(tmp_path)
    assert [f.split()[0] for f in found] == ["tools/test_mechanism_gate.py", "tools/usage_report.py"]


def test_s3_counts_aliases_and_attribute_nodes_not_strings_and_docstrings(tmp_path):
    put(tmp_path, {"alias.py": "import sys\nr = sys.stdout.reconfigure\nr(encoding='utf-8')\n",
                   "twice.py": COPY + COPY,
                   "text.py": '"""calls ' + CALL + ' in prose"""\nNOTE = "sys.stdout' + CALL + ')"\n'})
    counts, _ = census(tmp_path)
    assert counts == {"alias.py": 1, "twice.py": 2, "text.py": 0}
    assert [f.split()[0] for f in offenders(tmp_path)] == ["tools/alias.py", "tools/twice.py"]
    assert "2 time(s)" in offenders(tmp_path)[1]


def test_s3_a_deliberate_copy_is_exempt_only_through_kept(tmp_path):
    put(tmp_path, {"x.py": COPY})
    assert offenders(tmp_path, kept={"x.py": "a reason"}) == []
    assert len(offenders(tmp_path, kept={"y.py": "a reason"})) == 1


def test_s3_an_unparsable_or_non_utf8_file_fails_the_census_and_is_named(tmp_path):
    put(tmp_path, {"broken.py": "def broken(:\n", "latin.py": b"x = '\xff'\n", "ok.py": "x = 1\n"})
    found = offenders(tmp_path)
    assert [f.split()[0] for f in found] == ["tools/broken.py", "tools/latin.py"]
    assert all("cannot be counted" in f for f in found)


# ---------------------------------------------------------------- S4 no chain link reaches the helper

def link_stems():
    """The stems of every MECHANISM_PREFIXES entry of the form tools/<name>.py -- all links, not only live wiring."""
    names = [p[len("tools/"):] for p in mg.MECHANISM_PREFIXES if p.startswith("tools/") and p.endswith(".py")]
    return sorted(n[:-3] for n in names if "/" not in n)


def chain_reaches(start_stems, root):
    """The tools/ modules reachable by import from `start_stems`, start entries included."""
    return _transitive_tool_module_closure(set(start_stems), _tools_module_names(root), root)


def test_s4_no_chain_link_reaches_tools_streams():
    reached = chain_reaches(link_stems(), TOOLS)
    if "streams" in reached:
        culprits = [stem for stem in link_stems() if "streams" in chain_reaches({stem}, TOOLS)]
        pytest.fail(f"{culprits} reaches tools/streams.py -- a chain link keeps its own stream setup; restore the "
                    f"copy, or the Lead brings streams.py into MECHANISM_PREFIXES with a mechanism commit")


def test_s4_positive_control_two_step_chains_are_seen_and_the_links_are_listed():
    stems = link_stems()
    assert len(stems) >= 30 and "journal_echo" in stems and "piles" in stems and "streams" not in stems
    assert "tier_echo" in chain_reaches({"journal_echo"}, TOOLS)       # journal_echo -> tier_echo (a link)
    assert "gitcmd" in chain_reaches({"piles"}, TOOLS)                 # piles -> gitcmd
    assert "preflight_quota" in chain_reaches({"session_context"}, TOOLS)
    # a real two-step chain: journal_validator -> journal_keys -> dev_config (journal_validator names dev_config nowhere)
    assert "dev_config" in chain_reaches({"journal_validator"}, TOOLS)
    assert "dev_config" not in (TOOLS / "journal_validator.py").read_text(encoding="utf-8")


def test_s4_negative_control_a_helper_two_imports_away_is_found(tmp_path):
    put(tmp_path, {"chain_a.py": "import mid\n", "mid.py": "import streams\n", "streams.py": "", "other.py": ""})
    assert "streams" in chain_reaches({"chain_a"}, tmp_path)
    assert "streams" not in chain_reaches({"other"}, tmp_path)


def test_s4_any_import_form_counts_a_nested_import_too(tmp_path):
    put(tmp_path, {"a.py": "def f():\n    from streams import utf8_stdio\n", "streams.py": ""})
    assert "streams" in chain_reaches({"a"}, tmp_path)


def test_s4_a_chain_file_with_a_syntax_error_raises_loudly(tmp_path):
    put(tmp_path, {"a.py": "def broken(:\n", "streams.py": ""})
    with pytest.raises(SyntaxError):
        chain_reaches({"a"}, tmp_path)
