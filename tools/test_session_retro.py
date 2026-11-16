"""Tests for tools/session_retro.py (t-878): counts of a synthetic transcript, and the CLI edges."""
import json
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import session_retro as sr  # noqa: E402


def _tu(name, **inp):
    return {"type": "assistant", "timestamp": "T2", "message": {"content": [{"type": "tool_use", "name": name, "input": inp}]}}


def _user(content, ts="T1"):
    return {"type": "user", "timestamp": ts, "message": {"content": content}}


def _err(text, ts):
    return _user([{"type": "tool_result", "is_error": True, "content": text}], ts)


@pytest.fixture
def transcript(tmp_path):
    rows = [_user("fix the thing"), _user("<system-reminder>x</system-reminder>"),
            _user("This session is being continued from a previous conversation ..."),
            _user([{"type": "text", "text": "Another Claude session sent a message: hi"}]),
            _tu("Bash", command="A=1; git -C x status"), _tu("PowerShell", command="git -C y log"),
            _tu("Read", file_path="a"), _tu("Read", file_path="a"), _tu("Read", file_path="a"), _tu("Read", file_path="b"),
            _tu("Agent", subagent_type="builder", description="d1"), _tu("Agent", subagent_type="critic", description="d1"),
            _err("PreToolUse:Agent hook error: [x] DISPATCH PATHS MISSING: owns", "T5"),
            _err("PreToolUse:Agent hook error: lower case only", "T6"),
            _err("Exit code 1\nboom", "T7")]
    p = tmp_path / "s.jsonl"
    p.write_text("\n".join(json.dumps(r) for r in rows) + "\nnot json\n[1]\n", encoding="utf-8")
    return p


def test_counts(transcript):
    r = sr.analyze(transcript)
    assert (r["operator"], r["compactions"], r["handbacks"], r["unreadable"], r["refusals"]) == (1, 1, 1, 2, 2)
    assert dict(r["shapes"]) == {"git -C": 2}
    assert dict(r["tools"])["Read"] == 4 and r["repeat_reads"] == [("a", 3)]
    assert r["redispatched"] == ["d1"] and dict(r["agents"]) == {"builder": 1, "critic": 1}
    assert [(c, t) for c, _, t in r["errors"]] == [("DISPATCH PATHS MISSING", "T5"),
                                                  ("hook: lower case only", "T6"), ("Exit code 1", "T7")]
    assert "retries after a refusal: 2" in sr.render(r, 15, 10)


@pytest.mark.parametrize("argv,code", [(["--last", "0"], 2), (["--last", "-1"], 2), (["--top", "0"], 2)])
def test_bad_numbers(argv, code):
    with pytest.raises(SystemExit) as e:
        sr.main(argv)
    assert e.value.code == code


def test_cli_edges(tmp_path, capsys):
    assert sr.main(["--dir", str(tmp_path / "none")]) == 2
    assert "no transcripts in" in capsys.readouterr().err
    (tmp_path / "e.jsonl").write_text("", encoding="utf-8")
    assert sr.main(["--dir", str(tmp_path), "--last", "1"]) == 0
    assert "e.jsonl: empty transcript" in capsys.readouterr().out
    assert sr.main(["--dir", str(tmp_path), "--session", "missing"]) == 2
    assert "missing" in capsys.readouterr().err
