"""Tests for tools/handback_extract.py (t-744 N2, F19): the final hand-back of a worker transcript copied into
a report file by code. Transcripts are fixtures in tmp_path; the module reads them only through
tools/transcripts.py, so the cases here pin the picking rule, the exit codes and the no-body stdout.

Run from the repo root: python -m pytest tools/test_handback_extract.py -q
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

import handback_extract as HE  # noqa: E402

transcripts = HE.transcripts
BODY_MARKER = "BODYMARKER_7731"


def _user(text="dispatch"):
    return {"type": "user", "message": {"role": "user", "content": text}}


def _text(text):
    return {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": text}]}}


def _call(name, **inp):
    block = {"type": "tool_use", "id": "t1", "name": name, "input": inp}
    return {"type": "assistant", "message": {"role": "assistant", "content": [block]}}


def _handback(message):
    return _call("SubagentHandback", message=message)


def _write(path, objs, tail=b""):
    """A transcript of JSON objects, one per line, then raw `tail` bytes (a truncated line, a stray byte)."""
    data = "".join(json.dumps(o) + "\n" for o in objs).encode("utf-8") + tail
    Path(path).write_bytes(data)
    return Path(path)


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _run(src, out, *extra):
    return HE.main([str(src), str(out), *extra])


@pytest.fixture
def paths(tmp_path):
    return tmp_path / "agent-ab12.jsonl", tmp_path / "report.md"


def test_empty_transcript(paths):
    src, out = paths
    src.write_bytes(b"")
    assert _run(src, out) == 2
    assert not out.exists()


def test_no_assistant_text(paths):
    src, out = paths
    tool_result = {"type": "user", "message": {"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": "t1", "content": "file listing"}]}}
    user_blocks = {"type": "user", "message": {"role": "user", "content": [{"type": "text", "text": "more"}]}}
    _write(src, [_user("USER TEXT MUST NOT BE PICKED"), tool_result, user_blocks, _call("Bash", command="ls")],
           tail=b"not json at all\n")
    assert _run(src, out) == 2
    assert not out.exists()


def test_handback_preferred(paths, capsys):
    src, out = paths
    msg = {"type": "assistant", "message": {"role": "assistant", "content": [
        {"type": "text", "text": "Handing back now."},
        {"type": "tool_use", "id": "t9", "name": "SubagentHandback", "input": {"message": "REPORT"}}]}}
    _write(src, [_user(), msg])
    assert _run(src, out) == 0
    assert out.read_bytes() == b"REPORT\n"
    assert capsys.readouterr().out.strip().endswith("source=handback finished=yes digest=none")


def test_last_handback_wins(paths):
    src, out = paths
    _write(src, [_user(), _text("an earlier text that is much longer than the final hand-back " * 5),
                 _handback("FIRST " * 50), _call("Bash", command="retry"), _handback("second, short")])
    assert _run(src, out) == 0
    assert out.read_text(encoding="utf-8") == "second, short\n"


def test_empty_handback_message_falls_back_to_text(paths):
    src, out = paths
    _write(src, [_user(), _text("the text"), _handback("   ")])
    assert _run(src, out) == 0
    assert out.read_text(encoding="utf-8") == "the text\n"


def test_content_string(paths, capsys):
    src, out = paths
    _write(src, [_user(), {"type": "assistant", "message": {"role": "assistant", "content": "plain string body"}}])
    assert _run(src, out) == 4
    assert out.read_text(encoding="utf-8").endswith("\n\nplain string body\n")
    assert "source=last_text finished=no" in capsys.readouterr().out


def test_truncated_last_line(paths):
    src, out = paths
    cut = json.dumps(_handback("LATER hand-back cut in the middle"))[:40].encode("utf-8")
    _write(src, [_user(), _text("the previous candidate"), _call("Bash", command="ls")], tail=cut)
    assert _run(src, out) == 4
    lines = out.read_text(encoding="utf-8").split("\n")
    assert lines[0] == HE.UNFINISHED_MARKER
    assert lines[2] == "the previous candidate"


def test_non_utf8_byte(paths):
    src, out = paths
    data = "".join(json.dumps(o) + "\n" for o in [_user(), _handback("before XX after")]).encode("utf-8")
    src.write_bytes(data.replace(b"XX", b"\xff"))
    assert _run(src, out) == 0
    assert out.read_bytes() == "before � after\n".encode("utf-8")


def test_existing_output_kept(paths):
    src, out = paths
    _write(src, [_user(), _handback("REPORT")])
    out.write_bytes(b"the worker already wrote this\r\n")
    before = _sha(out)
    assert _run(src, out) == 3
    assert _sha(out) == before


def test_missing_out_dir(paths, tmp_path):
    src, _ = paths
    _write(src, [_user(), _handback("REPORT")])
    out = tmp_path / "nope" / "report.md"
    assert _run(src, out) == 1
    assert not out.parent.exists()


def test_missing_transcript(paths):
    src, out = paths
    assert _run(src, out) == 1
    assert not out.exists()


def test_stdout_has_no_body(paths, capsys):
    src, out = paths
    _write(src, [_user(), _handback("head line\n\n" + BODY_MARKER + "\nlast line")])
    assert _run(src, out) == 0
    shown = capsys.readouterr().out
    assert BODY_MARKER not in shown and "head line" not in shown
    assert shown == "written %s bytes=%d lines=4 source=handback finished=yes digest=none\n" % (out, out.stat().st_size)
    assert BODY_MARKER in out.read_text(encoding="utf-8")


def test_cli_prints_one_line_without_the_body(paths):
    src, out = paths
    _write(src, [_user(), _handback(BODY_MARKER)])
    done = subprocess.run([sys.executable, "-I", str(TOOLS / "handback_extract.py"), str(src), str(out)],
                          capture_output=True, text=True, encoding="utf-8")
    assert done.returncode == 0, done.stderr
    assert done.stdout.startswith("written ") and done.stdout.count("\n") == 1
    assert BODY_MARKER not in done.stdout


def test_handback_line_over_the_tail_window_is_finished(paths):
    """The live case of t-744 (agent-ab6233f5...: a final hand-back line of 74 KB): transcripts.is_finished reads
    the file's last line whole (t-840, F6-7), so finished=yes through the ONE reader."""
    src, out = paths
    big = "word " * (transcripts.TAIL_BYTES // 4)
    _write(src, [_user(), _text("working"), _handback(big)])
    assert len(json.dumps(_handback(big))) > transcripts.TAIL_BYTES  # the hand-back line alone fills the window
    assert transcripts.is_finished(src) is True
    assert _run(src, out) == 0
    assert not out.read_text(encoding="utf-8").startswith(HE.UNFINISHED_MARKER)


def test_handback_line_over_the_window_followed_by_a_line_is_finished_t857(paths, capsys):
    """F6-19 (flipped from t-840's finished=no): a 70 KB hand-back followed by a short line -- the shape the
    harness writes -- is finished through the ONE reader, which grows its window to the newest tool_use line."""
    src, out = paths
    big = "word " * (transcripts.TAIL_BYTES // 4)
    _write(src, [_user(), _handback(big), {"type": "user", "message": {"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": "t1", "content": "ok"}]}}])
    assert transcripts.is_finished(src) is True
    assert _run(src, out) == 0
    assert "source=handback finished=yes" in capsys.readouterr().out
    assert not out.read_text(encoding="utf-8").startswith(HE.UNFINISHED_MARKER)


def test_work_after_the_handback_is_unfinished(paths, capsys):
    src, out = paths
    _write(src, [_user(), _handback("REPORT"), _call("Bash", command="ls")])
    assert _run(src, out) == 4
    assert "source=handback finished=no" in capsys.readouterr().out
    assert out.read_text(encoding="utf-8").split("\n")[0] == HE.AFTER_HANDBACK_MARKER


def test_no_handback_at_all_has_the_old_marker(paths):
    src, out = paths
    _write(src, [_user(), _text("only text"), _call("Bash", command="ls")])
    assert _run(src, out) == 4
    first = out.read_text(encoding="utf-8").split("\n")[0]
    assert first == HE.UNFINISHED_MARKER and first != HE.AFTER_HANDBACK_MARKER


def test_lone_surrogate_in_the_text_is_replaced(paths):
    src, out = paths
    _write(src, [_user(), _handback("a\ud800b")])
    assert b"\\ud800" in src.read_bytes()  # the fixture carries the JSON escape, as a real transcript can
    assert _run(src, out) == 0
    assert out.read_bytes() == b"a?b\n"


@pytest.mark.parametrize("header", ["\n", "\n\n", " \n\t"])
def test_blank_header_counts_as_no_header(paths, header):
    src, out = paths
    _write(src, [_user(), _text("body")])
    assert _run(src, out, "--header", header) == 4
    with_header = out.read_bytes()
    out.unlink()
    assert _run(src, out) == 4
    assert with_header == out.read_bytes()
    assert not out.read_text(encoding="utf-8").startswith("\n")


def test_header_and_marker_order_and_newlines_kept(paths):
    src, out = paths
    _write(src, [_user(), _text("line one\r\nline two\n\n")])
    assert _run(src, out, "--header", "# Header\n\n") == 4
    assert out.read_bytes() == (HE.UNFINISHED_MARKER + "\n\n# Header\n\nline one\r\nline two\n").encode("utf-8")


def test_line_count_rule(paths, capsys):
    src, out = paths
    text = "a\n\n```\n" + "x" * 450 + "\n" + "y" * 200 + "\n```"
    assert HE.count_lines(text) == 1 + 1 + 1 + 3 + 1 + 1
    _write(src, [_user(), _handback(text)])
    assert _run(src, out) == 0
    assert "lines=8 " in capsys.readouterr().out


@pytest.fixture
def home(tmp_path, monkeypatch):
    root = tmp_path / "projects"
    monkeypatch.setattr(transcripts, "projects_root", lambda: root)
    return root


def _agent_file(root, session, agent="ab12"):
    folder = root / "slug" / session / "subagents"
    folder.mkdir(parents=True)
    return _write(folder / ("agent-%s.jsonl" % agent), [_user(), _handback("BY ID")])


def test_agent_id_found(home, tmp_path):
    _agent_file(home, "s1")
    out = tmp_path / "by-id.md"
    assert HE.main(["--agent", "ab12", str(out)]) == 0
    assert out.read_text(encoding="utf-8") == "BY ID\n"


@pytest.mark.parametrize("agent", ["zz99", "../ab12", "ab*"])
def test_agent_id_unknown_or_unsafe(home, tmp_path, agent):
    _agent_file(home, "s1")
    out = tmp_path / "x.md"
    assert HE.main(["--agent", agent, str(out)]) == 1
    assert not out.exists()


def test_agent_id_ambiguous(home, tmp_path):
    _agent_file(home, "s1")
    _agent_file(home, "s2")
    out = tmp_path / "x.md"
    assert HE.main(["--agent", "ab12", str(out)]) == 1
    assert not out.exists()


@pytest.mark.parametrize("argv", [[], ["only-one"], ["a", "b", "c"], ["--agent", "ab12"],
                                  ["--agent", "ab12", "a", "b"]])
def test_bad_arguments_are_a_call_error(argv, capsys):
    assert HE.main(argv) == 1
    assert capsys.readouterr().err


# ----- the `digest=` tail of the stdout line (t-797 F5-2 N1, I2): a report only, the file and the exit code never depend on it -----

DASH = "—"
DIGEST = "\n".join([
    "digest: v1 t-9", "## Objects", "| id | kind | gist | paths | status | owner | links | ev |", "|---|---|---|---|---|---|---|---|",
    "| a1 | claim | one claim | x.py:1 | open | %s | %s | R1 |" % (DASH, DASH), "## Trail",
    "| tid | op | target | pattern / range | flags | result | control |", "|---|---|---|---|---|---|---|",
    "| R1 | read | x.py | all | %s | read x.py:1 | %s |" % (DASH, DASH)])
NO_TRAIL = DIGEST.replace("| open | %s | %s | R1 |" % (DASH, DASH), "| open | %s | %s | R9 |" % (DASH, DASH))
READ_X = _call("Read", file_path="/repo/x.py")          # the call the one Trail row of DIGEST (read x.py) stands behind


def test_digest_tail_of_a_clean_digest(paths, capsys):
    src, out = paths
    _write(src, [_user(), READ_X, _handback(DIGEST)])
    assert _run(src, out) == 0
    shown = capsys.readouterr().out
    assert shown.endswith(" source=handback finished=yes digest=v1 objects=1 trail=1 flags=0\n")
    assert shown.count("\n") == 1 and out.read_text(encoding="utf-8") == DIGEST + "\n"


def test_digest_tail_names_the_count_and_the_first_flag(paths, capsys):
    src, out = paths
    _write(src, [_user(), READ_X, _handback(NO_TRAIL)])
    assert _run(src, out) == 0
    shown = capsys.readouterr().out
    assert shown.endswith(" digest=v1 objects=1 trail=1 flags=1 first=ev_unknown:a1:R9\n") and shown.count("\n") == 1


def test_digest_tail_first_flag_has_no_whitespace(paths, capsys):
    src, out = paths
    _write(src, [_user(), READ_X, _handback(NO_TRAIL.replace("| R9 |", "| R 9 |"))])
    assert _run(src, out) == 0
    assert capsys.readouterr().out.endswith(" flags=1 first=ev_unknown:a1:R_9\n")


def test_prose_digest_is_extracted_as_prose_and_says_none(paths, capsys):
    """The world before scout.md teaches the form: today's prose digest is copied verbatim and reported as digest=none."""
    src, out = paths
    prose = "Findings.\n\nTRAIL\nFiles read:\n - a.py\ndigest is mentioned here but is not a key"
    _write(src, [_user(), _handback(prose)])
    assert _run(src, out) == 0
    assert capsys.readouterr().out.endswith(" finished=yes digest=none\n")
    assert out.read_text(encoding="utf-8") == prose + "\n"


def test_digest_tail_of_an_unfinished_scout_message_reads_the_text_not_the_marker(paths, capsys):
    """Both unfinished markers go to the FILE only: parsing the extracted text keeps the key on the first line."""
    src, out = paths
    _write(src, [_user(), READ_X, _text(DIGEST), _call("Bash", command="ls")])
    assert _run(src, out) == 4
    assert capsys.readouterr().out.endswith(" source=last_text finished=no digest=v1 objects=1 trail=1 flags=0\n")
    assert out.read_text(encoding="utf-8").split("\n")[0] == HE.UNFINISHED_MARKER
    out.unlink()
    _write(src, [_user(), READ_X, _handback(DIGEST), _call("Bash", command="ls")])
    assert _run(src, out) == 4
    assert capsys.readouterr().out.endswith(" source=handback finished=no digest=v1 objects=1 trail=1 flags=0\n")
    assert out.read_text(encoding="utf-8").split("\n")[0] == HE.AFTER_HANDBACK_MARKER


def test_digest_reader_that_raises_is_n_d_and_the_exit_codes_stay(paths, capsys, monkeypatch):
    src, out = paths

    def boom(text):
        raise RuntimeError("the reader broke")

    for name in ("parse", "flags"):
        _write(src, [_user(), _handback(DIGEST)])
        monkeypatch.setattr(HE.digest_form, name, boom)
        assert _run(src, out) == 0
        assert capsys.readouterr().out.endswith(" finished=yes digest=n/d\n")
        assert out.read_text(encoding="utf-8") == DIGEST + "\n"
        monkeypatch.undo()
        out.unlink()
        _write(src, [_user(), _text(DIGEST), _call("Bash", command="ls")])
        monkeypatch.setattr(HE.digest_form, name, boom)
        assert _run(src, out) == 4
        assert capsys.readouterr().out.endswith(" finished=no digest=n/d\n")
        monkeypatch.undo()
        out.unlink()


def _cli_with_broken_reader(src, out):
    """handback_extract in a fresh interpreter in which `import digest_form` fails (a None entry in sys.modules)."""
    code = ("import sys; sys.modules['digest_form'] = None; sys.path.insert(0, %r); import handback_extract as H; "
            "print(H.digest_form); sys.exit(H.main([%r, %r]))" % (str(TOOLS), str(src), str(out)))
    return subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True, encoding="utf-8")


def test_a_digest_reader_that_does_not_import_leaves_the_tool_working(paths):
    src, out = paths
    _write(src, [_user(), _handback(DIGEST)])
    done = _cli_with_broken_reader(src, out)
    lines = done.stdout.strip().split("\n")
    assert done.returncode == 0, done.stderr
    assert lines[0] == "None" and lines[1].endswith(" finished=yes digest=n/d")
    assert out.read_text(encoding="utf-8") == DIGEST + "\n"
    out.unlink()
    _write(src, [_user(), _text(DIGEST), _call("Bash", command="ls")])
    assert _cli_with_broken_reader(src, out).returncode == 4


def test_the_digest_reader_import_is_guarded_with_a_stated_degradation():
    """Axis 14: a consumer that must stay alive when a reader is broken states the degraded behaviour next to the import."""
    source = (TOOLS / "handback_extract.py").read_text(encoding="utf-8")
    at = source.index("import digest_form")
    near = source[at - 40:at + 260]
    assert "except Exception" in near and "digest=n/d" in near


# ----- the trail against the transcript (t-863, F6-14): a fabricated trail is flagged, an unchecked one says so ---------------------

TH = "| tid | op | target | pattern / range | flags | result | control |"
TSEP = "|---|---|---|---|---|---|---|"


def _digest_of(*trail_rows, status="open", ev="R1"):
    """A v1 digest of ONE object standing on `ev` and the given Trail rows (each a 7-cell list)."""
    return "\n".join(["digest: v1 t-9", "## Objects", "| id | kind | gist | paths | status | owner | links | ev |", "|---|---|---|---|---|---|---|---|",
                      "| a1 | claim | one claim | x.py:1 | %s | %s | %s | %s |" % (status, DASH, DASH, ev), "## Trail", TH, TSEP]
                     + ["| " + " | ".join(r) + " |" for r in trail_rows])


def _read_row(tid, target):
    return [tid, "read", target, "all", DASH, "read %s:1" % target, DASH]


def _flags_line(src, out, capsys, code=0):
    assert _run(src, out) == code
    return capsys.readouterr().out.split(" digest=", 1)[1]


def test_a_backed_trail_has_no_trail_flag_and_a_fabricated_row_is_counted(paths, capsys):
    src, out = paths
    two = _digest_of(_read_row("R1", "x.py"), _read_row("R2", "y.py"), ev="R1,R2")
    _write(src, [_user(), READ_X, _handback(two)])
    assert _flags_line(src, out, capsys) == "v1 objects=1 trail=2 flags=1 first=trail_unbacked:1\n"
    assert out.read_text(encoding="utf-8") == two + "\n"                         # a flag, not a refusal: the digest is copied whole
    out.unlink()
    _write(src, [_user(), READ_X, _call("Read", file_path="/repo/y.py"), _handback(two)])
    assert _flags_line(src, out, capsys) == "v1 objects=1 trail=2 flags=0\n"


def test_every_row_of_a_wholly_invented_trail_is_counted(paths, capsys):
    src, out = paths
    _write(src, [_user(), _handback(_digest_of(_read_row("R1", "x.py"), _read_row("R2", "y.py"), ev="R1,R2"))])
    assert _flags_line(src, out, capsys) == "v1 objects=1 trail=2 flags=1 first=trail_unbacked:2\n"


def test_without_a_transcript_the_trail_is_unchecked_never_unbacked(paths, capsys, monkeypatch):
    """The invariant: no transcript (a gateway worker, an unreadable file) -> trail_unchecked, whatever the rows say."""
    assert HE.digest_tail(DIGEST) == " digest=v1 objects=1 trail=1 flags=1 first=trail_unchecked"
    assert HE.digest_tail(DIGEST, []) == " digest=v1 objects=1 trail=1 flags=1 first=trail_unbacked:1"      # an empty transcript is not "none"
    assert HE.digest_tail("prose only") == " digest=none"
    src, out = paths
    _write(src, [_user(), _handback(DIGEST)])

    def unreadable(path):
        raise OSError("gone")

    monkeypatch.setattr(HE, "tool_calls", unreadable)
    assert _flags_line(src, out, capsys) == "v1 objects=1 trail=1 flags=1 first=trail_unchecked\n"


def test_the_trail_flag_names_are_stated_in_the_tool_doc_from_the_one_list():
    assert all(name in HE.__doc__ for name in HE.digest_form.TRANSCRIPT_FLAG_NAMES)


def test_paths_match_by_a_normalised_substring_case_and_slashes_do_not_matter(paths, capsys):
    src, out = paths
    text = _digest_of(_read_row("R1", "Tools/X.py"))
    for recorded in ("C:\\Work\\Repo\\repo\\tools\\x.py", "c:/work/repo/repo/TOOLS/x.PY", "/r/./tools//x.py"):
        _write(src, [_user(), _call("Read", file_path=recorded), _handback(text)])
        assert _flags_line(src, out, capsys) == "v1 objects=1 trail=1 flags=0\n", recorded
        out.unlink()
    _write(src, [_user(), _call("Read", file_path="/repo/tools/xy.py"), _handback(text)])        # a different file is not a substring
    assert _flags_line(src, out, capsys) == "v1 objects=1 trail=1 flags=1 first=trail_unbacked:1\n"


def _grep_row(tid, pattern, result, control=DASH, target="tools/", flags="-i content"):
    return [tid, "grep", target, "`%s`" % pattern, flags, result, control]


ABSENT = _digest_of(_grep_row("G1", "nope", "absent", "G2"), _grep_row("G2", "yes", "found 2; a.py:1, b.py:2"), status="absent", ev="G1,G2")


def _grep(pattern, path="C:\\repo\\tools"):
    return _call("Grep", pattern=pattern, path=path, output_mode="content")


def test_a_negative_claim_is_backed_by_the_search_it_names_and_by_nothing_else(paths, capsys):
    src, out = paths
    _write(src, [_user(), _grep("nope"), _grep("yes"), _handback(ABSENT)])
    assert _flags_line(src, out, capsys) == "v1 objects=1 trail=2 flags=0\n"
    out.unlink()
    _write(src, [_user(), _grep("yes"), _handback(ABSENT)])                                         # the zero search never ran
    assert _flags_line(src, out, capsys) == "v1 objects=1 trail=2 flags=1 first=trail_unbacked:1\n"
    out.unlink()
    _write(src, [_user(), _call("Read", file_path="/repo/tools/nope"), _call("Glob", pattern="nope", path="/repo/tools"), _handback(ABSENT)])
    assert _flags_line(src, out, capsys) == "v1 objects=1 trail=2 flags=1 first=trail_unbacked:2\n"   # another tool does not stand for a Grep


def test_a_search_in_another_place_does_not_back_the_row_but_a_root_target_takes_any(paths, capsys):
    src, out = paths
    _write(src, [_user(), _grep("nope", "/repo/scripts"), _grep("yes", "/repo/scripts"), _handback(ABSENT)])
    assert _flags_line(src, out, capsys) == "v1 objects=1 trail=2 flags=1 first=trail_unbacked:2\n"
    out.unlink()
    root = ABSENT.replace("| tools/ |", "| . |")
    _write(src, [_user(), _call("Grep", pattern="nope"), _grep("yes", "/anywhere"), _handback(root)])
    assert _flags_line(src, out, capsys) == "v1 objects=1 trail=2 flags=0\n"


def test_a_glob_row_is_backed_by_a_glob_call(paths, capsys):
    src, out = paths
    text = _digest_of(["R1", "glob", "tools/", "`*.zz`", DASH, "absent", "R2"], ["R2", "glob", "tools/", "`*.py`", DASH, "found 3; a.py", DASH], ev="R1,R2")
    _write(src, [_user(), _call("Glob", pattern="*.zz", path="/repo/tools"), _call("Glob", pattern="**/*.py", path="/repo/tools"), _handback(text)])
    assert _flags_line(src, out, capsys) == "v1 objects=1 trail=2 flags=0\n"


def test_a_call_far_before_the_64k_tail_window_still_backs_the_row(paths, capsys):
    """The reader walks the whole file (iter_lines), not the tail window of is_finished."""
    src, out = paths
    filler = [_text("filler " * 500) for _ in range(120)]
    _write(src, [_user(), READ_X, *filler, _handback(DIGEST)])
    assert src.stat().st_size > 3 * transcripts.TAIL_BYTES                 # the Read line is far outside the last 64 KB
    assert [tuple(c) for c in HE.tool_calls(src)] == [("Read", "/repo/x.py", None)]
    assert _flags_line(src, out, capsys) == "v1 objects=1 trail=1 flags=0\n"


def test_a_malformed_tool_input_backs_nothing_and_breaks_nothing(paths, capsys):
    src, out = paths
    bad = [{"type": "assistant", "message": {"role": "assistant", "content": [
        {"type": "tool_use", "id": "t1", "name": "Read", "input": "x.py"}, {"type": "tool_use", "id": "t2", "name": "Read", "input": {"file_path": 7}},
        {"type": "tool_use", "id": "t3", "name": "Grep", "input": None}, "stray", {"type": "tool_use", "id": "t4", "name": "Bash", "input": {"command": "x.py"}}]}}]
    _write(src, [_user(), *bad, _handback(DIGEST)])
    assert _flags_line(src, out, capsys) == "v1 objects=1 trail=1 flags=1 first=trail_unbacked:1\n"


def test_a_digest_without_a_readable_trail_gets_no_trail_flag_of_its_own(paths, capsys):
    src, out = paths
    bad = DIGEST.replace("| tid | op |", "| op | tid |")
    _write(src, [_user(), _handback(bad)])
    assert _flags_line(src, out, capsys) == "v1 objects=1 trail=1 flags=2 first=ev_unknown:a1:R1\n"
