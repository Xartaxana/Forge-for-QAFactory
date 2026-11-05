"""Tests for tools/journal_keys.py (B-402): the task key readers share, the declaration file
logs/journal-segments.json, `check`, the never-raising `load_segments`, and the CLI.

Run from the repo root: python -m pytest tools/test_journal_keys.py
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import journal_keys as jk

REPO_ROOT = Path(__file__).resolve().parent.parent


def _ev(ts, tid, event="delegated", agent="scout", wr="", **kw) -> dict:
    d = {"ts": ts, "event": event, "agent": agent, "category": "recon", "notes": "n"}
    if tid is not None:
        d["task_id"] = tid
    if wr:
        d["worker_ref"] = wr
    d.update(kw)
    return d


def _text(*objs) -> str:
    return "".join((o if isinstance(o, str) else json.dumps(o)) + "\n" for o in objs)


# two clones issued t-050: the branch's instance is open, main's is accepted
BR_D = _ev("2026-10-02T10:00:00", "t-050", "delegated", "scout", "agent:aaa")           # line 2
MN_D = _ev("2026-10-02T11:00:00", "t-050", "delegated", "scout", "agent:bbb")           # line 3
MN_A = _ev("2026-10-02T11:05:00", "t-050", "accepted", "scout")                         # line 4
BASE = _ev("2026-10-02T09:00:00", "t-049", "delegated", "scout", "agent:base")          # line 1
JOURNAL = _text(BASE, BR_D, MN_D, MN_A)
LINES = jk.split_lines(JOURNAL)


def _decl(*segments, version=1) -> str:
    return json.dumps({"version": version, "segments": list(segments)})


def _seg(label, idents, why="a reason") -> dict:
    return {"label": label, "why": why, "lines": [list(i) for i in idents]}


BR_ID = jk.identity(BR_D)
GOOD = _decl(_seg("branch", [BR_ID]))


def _segs(text: str) -> jk.Segments:
    segs, why = jk.parse_declaration(text)
    assert segs is not None, why
    return segs


# ---- identity and keys ----

def test_identity_has_five_fields_and_an_empty_worker_ref():
    assert jk.identity(BR_D) == ("2026-10-02T10:00:00", "t-050", "delegated", "scout", "agent:aaa")
    assert jk.identity(MN_A) == ("2026-10-02T11:05:00", "t-050", "accepted", "scout", "")
    assert len(jk.IDENTITY_FIELDS) == 5


def test_no_declaration_every_key_is_the_bare_id():
    assert jk.task_key(BR_D, jk.NO_SEGMENTS) == ("", "t-050")
    assert jk.task_key(MN_A, jk.NO_SEGMENTS) == ("", "t-050")
    assert jk.task_key(_ev("2026-10-02T10:00:00", None, "dispatch_skipped"), jk.NO_SEGMENTS) is None
    assert jk.task_key("not an object", jk.NO_SEGMENTS) is None
    # an empty list is the same as no file
    assert jk.task_key(BR_D, _segs(_decl())) == ("", "t-050")


def test_declared_lines_carry_the_label_and_the_rest_stay_bare():
    segs = _segs(GOOD)
    assert jk.task_key(BR_D, segs) == ("branch", "t-050")
    assert jk.task_key(MN_D, segs) == ("", "t-050")
    assert jk.task_key(MN_A, segs) == ("", "t-050")
    assert jk.task_key(BASE, segs) == ("", "t-049")


def test_display():
    assert jk.display(("", "t-007")) == "t-007"
    assert jk.display(("codex-fixes", "t-007")) == "t-007@codex-fixes"


# ---- ref_key (E7) ----

def test_ref_key_bare_resolves_by_the_carrier_label_when_that_segment_holds_the_id():
    segs = _segs(GOOD)
    carrier_branch = _ev("2026-10-02T10:30:00", "t-050", "escalated")           # not listed: bare side
    assert jk.ref_key("t-050", carrier_branch, segs) == ("", "t-050")
    assert jk.ref_key("t-050", BR_D, segs) == ("branch", "t-050")               # the carrier IS the declared line
    assert jk.ref_key("t-049", BR_D, segs) == ("", "t-049")                     # the carrier's segment does not hold t-049
    assert jk.ref_key("t-050", _ev("2026-10-02T10:30:00", None, "dispatch_skipped"), segs) == ("", "t-050")
    assert jk.ref_key("t-050", None, segs) == ("", "t-050")


def test_ref_key_qualified_is_explicit_and_a_non_token_is_none():
    segs = _segs(GOOD)
    assert jk.ref_key("t-050@branch", MN_A, segs) == ("branch", "t-050")
    assert jk.ref_key("t-050@nowhere", MN_A, segs) == ("nowhere", "t-050")      # a key that matches nothing
    assert jk.ref_key("t-050@", MN_A, segs) is None
    assert jk.ref_key("T-050", MN_A, segs) is None
    assert jk.ref_key("t-5", MN_A, segs) is None
    assert jk.ref_key(None, MN_A, segs) is None


# ---- check: the E3 / E5 inputs and the rest ----

def test_check_accepts_the_good_declaration():
    assert jk.check(LINES, _segs(GOOD)) == []
    assert jk.check(LINES, jk.NO_SEGMENTS) == []


def test_check_identity_matching_no_line():
    ghost = ("2026-10-02T10:00:00", "t-050", "delegated", "scout", "agent:zzz")
    problems = jk.check(LINES, _segs(_decl(_seg("branch", [BR_ID, ghost]))))
    assert len(problems) == 1 and "matches 0 journal lines" in problems[0]


def test_check_listed_count_must_equal_the_matched_count():
    twin = BR_D                                                   # two identical lines in the journal
    lines = jk.split_lines(_text(BASE, BR_D, twin, MN_D, MN_A))
    assert jk.check(lines, _segs(GOOD))[0].endswith("is listed 1 time(s) but matches 2 journal line(s)")
    twice = _segs(_decl(_seg("branch", [BR_ID, BR_ID])))
    assert jk.check(lines, twice) == []                           # listed twice, matched twice
    problems = jk.check(LINES, twice)                             # listed twice, matched once
    assert len(problems) == 1 and "listed 2 time(s) but matches 1" in problems[0]


def test_check_lines_told_apart_by_worker_ref_only():
    a = _ev("2026-10-02T10:00:00", "t-060", "delegated", "scout", "agent:one")
    b = _ev("2026-10-02T10:00:00", "t-060", "delegated", "scout", "agent:two")
    lines = jk.split_lines(_text(a, b, _ev("2026-10-02T10:01:00", "t-060", "accepted", "scout")))
    assert jk.check(lines, _segs(_decl(_seg("one", [jk.identity(a)])))) == []
    assert jk.task_key(a, _segs(_decl(_seg("one", [jk.identity(a)])))) == ("one", "t-060")
    assert jk.task_key(b, _segs(_decl(_seg("one", [jk.identity(a)])))) == ("", "t-060")


def test_check_declared_id_with_no_undeclared_line():
    both = _segs(_decl(_seg("branch", [BR_ID, jk.identity(MN_D), jk.identity(MN_A)])))
    problems = jk.check(LINES, both)
    assert len(problems) == 1 and "t-050 is declared but has no undeclared line" in problems[0]


def test_check_a_key_whose_first_line_is_not_delegated():
    orphan = _ev("2026-10-02T09:30:00", "t-050", "accepted", "scout")        # an accepted BEFORE any delegated of that key
    lines = jk.split_lines(_text(BASE, orphan, BR_D, MN_D, MN_A))
    # the undeclared ("", t-050) key now starts with an accepted
    problems = jk.check(lines, _segs(GOOD))
    assert len(problems) == 1 and "the first line of key t-050 is 'accepted', not 'delegated'" in problems[0]
    # the declared side
    declared_orphan = _segs(_decl(_seg("branch", [jk.identity(orphan)])))
    lines2 = jk.split_lines(_text(BASE, orphan, MN_D, MN_A))
    assert any("t-050@branch" in p and "'accepted'" in p for p in jk.check(lines2, declared_orphan))


def test_check_does_not_apply_the_first_delegated_rule_to_undeclared_orphans():
    # E1: an orphan accepted in a journal with no declared collision stays as it always was
    orphan = _ev("2026-10-02T09:30:00", "t-099", "accepted", "scout")
    assert jk.check(jk.split_lines(_text(BASE, orphan, BR_D, MN_D)), _segs(GOOD)) == []


def test_check_identity_listed_by_two_segments():
    two = _segs(_decl(_seg("one", [BR_ID]), _seg("two", [BR_ID])))
    problems = jk.check(LINES, two)
    assert any("listed by more than one segment (one, two)" in p for p in problems)


@pytest.mark.parametrize("label,ok", [
    ("a" * 24, True), ("a" * 25, False), ("", False), ("Codex", False), ("codex fixes", False),
    ("codex_fixes", False), ("codex-fixes-2", True), ("0", True),
])
def test_check_label_limits(label, ok):
    problems = jk.check(LINES, _segs(_decl(_seg(label, [BR_ID]))))
    assert (problems == []) is ok, problems
    if not ok:
        assert any("is not 1-24 characters of [a-z0-9-]" in p for p in problems)


def test_check_duplicate_label_empty_why_and_unknown_version():
    other = jk.identity(MN_D)
    dup = _segs(_decl(_seg("x", [BR_ID]), _seg("x", [other])))
    assert any("declared twice" in p for p in jk.check(LINES, dup))
    assert any("empty `why`" in p for p in jk.check(LINES, _segs(_decl(_seg("x", [BR_ID], why="   ")))))
    assert any("unknown version 2" in p for p in jk.check(LINES, _segs(_decl(_seg("x", [BR_ID]), version=2))))


# ---- parse_declaration shapes ----

@pytest.mark.parametrize("text", [
    "", "{not json", "[]", '"x"', "{}", '{"version": 1}', '{"version": 1, "segments": {}}',
    '{"version": 1, "segments": [5]}',
    '{"version": 1, "segments": [{"label": "x", "why": "y"}]}',
    '{"version": 1, "segments": [{"label": 7, "why": "y", "lines": []}]}',
    '{"version": 1, "segments": [{"label": "x", "why": "y", "lines": [["a", "b"]]}]}',
    '{"version": 1, "segments": [{"label": "x", "why": "y", "lines": [["a", "b", "c", "d", 5]]}]}',
    '{"version": "1", "segments": []}', '{"version": true, "segments": []}',
])
def test_parse_declaration_refuses_the_wrong_shape_with_a_reason(text):
    segs, why = jk.parse_declaration(text)
    assert segs is None and isinstance(why, str) and why


def test_dumps_declaration_roundtrips_one_identity_per_line():
    segs = _segs(_decl(_seg("x", [BR_ID, jk.identity(MN_A)], why="тест, кириллица")))
    text = jk.dumps_declaration(segs)
    again, why = jk.parse_declaration(text)
    assert why is None and again.segments == segs.segments and again.version == 1
    assert text.count("\n") == 13 and "тест" in text


# ---- load_segments never raises (E2) ----

def _journal_with(tmp_path: Path, declaration: str | bytes | None, journal: str = JOURNAL) -> Path:
    logs = tmp_path / "logs"
    logs.mkdir()
    jp = logs / "routing-log.jsonl"
    jp.write_text(journal, encoding="utf-8")
    if declaration is not None:
        data = declaration if isinstance(declaration, bytes) else declaration.encode("utf-8")
        (logs / jk.SEGMENTS_NAME).write_bytes(data)
    return jp


def test_load_segments_absent_file_is_no_segments_without_a_reason(tmp_path):
    assert jk.load_segments(_journal_with(tmp_path, None)) == (jk.NO_SEGMENTS, None)
    assert jk.load_segments(tmp_path / "nowhere" / "routing-log.jsonl") == (jk.NO_SEGMENTS, None)


def test_load_segments_good_file(tmp_path):
    segs, reason = jk.load_segments(_journal_with(tmp_path, GOOD))
    assert reason is None and segs.labels == ["branch"] and jk.task_key(BR_D, segs) == ("branch", "t-050")


@pytest.mark.parametrize("name,payload", [
    ("corrupt-bytes", b"\x00\x01\x02{{{"),
    ("non-utf8", b'{"version": 1, "segments": [], "x": "\xff\xfe"}'),
    ("list-at-top-level", b"[]"),
    ("version-2", _decl(_seg("branch", [BR_ID]), version=2)),
    ("wrong-types", b'{"version": 1, "segments": [{"label": 1, "why": 2, "lines": 3}]}'),
    ("segment-failing-check", _decl(_seg("branch", [BR_ID, ("2026-10-02T10:00:00", "t-050", "delegated", "scout", "agent:zzz")]))),
    ("empty-file", b""),
])
def test_load_segments_never_raises_and_falls_back_with_a_reason(tmp_path, name, payload):
    segs, reason = jk.load_segments(_journal_with(tmp_path, payload))
    assert segs is jk.NO_SEGMENTS and isinstance(reason, str) and reason, name
    # all or nothing: no label of a partly valid file leaks through
    assert jk.task_key(BR_D, segs) == ("", "t-050")


def test_load_segments_when_the_declaration_is_a_directory_or_the_journal_is_missing(tmp_path):
    logs = tmp_path / "logs"
    logs.mkdir()
    (logs / jk.SEGMENTS_NAME).mkdir()                                  # reading it raises IsADirectoryError / PermissionError
    segs, reason = jk.load_segments(logs / "routing-log.jsonl")
    assert segs is jk.NO_SEGMENTS and reason
    other = tmp_path / "o" / "logs"
    other.mkdir(parents=True)
    (other / jk.SEGMENTS_NAME).write_text(GOOD, encoding="utf-8")      # a declaration, no journal beside it
    segs, reason = jk.load_segments(other / "routing-log.jsonl")
    assert segs is jk.NO_SEGMENTS and reason and "FileNotFoundError" in reason


def test_load_segments_reason_is_capped(tmp_path):
    many = [("2026-10-02T10:00:00", "t-050", "delegated", "scout", f"agent:z{i}") for i in range(10)]
    segs, reason = jk.load_segments(_journal_with(tmp_path, _decl(_seg("branch", many))))
    assert segs is jk.NO_SEGMENTS and "and 7 more" in reason


# ---- the CLI ----

def _paths(tmp_path: Path, journal: str = JOURNAL):
    jp = _journal_with(tmp_path, None, journal)
    return jp, jp.parent / jk.SEGMENTS_NAME


def test_declare_writes_a_declaration_that_passes_check(tmp_path, capsys):
    jp, sp = _paths(tmp_path)
    assert jk.main(["--journal", str(jp), "declare", "--label", "branch", "--lines", "2-2", "--why", "numbering"]) == 0
    assert "label branch: 1 lines, 1 task ids" in capsys.readouterr().out
    segs, reason = jk.load_segments(jp)
    assert reason is None and jk.task_key(BR_D, segs) == ("branch", "t-050") and jk.task_key(MN_D, segs) == ("", "t-050")
    assert jk.main(["--journal", str(jp), "check"]) == 0
    assert "journal_keys check: ok -- 1 segment (branch), 1 lines, 1 task ids" in capsys.readouterr().out


def test_declare_a_second_segment_appends(tmp_path, capsys):
    other = _ev("2026-10-02T12:00:00", "t-051", "delegated", "scout", "agent:c")
    other2 = _ev("2026-10-02T12:30:00", "t-051", "delegated", "scout", "agent:d")
    jp, sp = _paths(tmp_path, _text(BASE, BR_D, MN_D, MN_A, other, other2))
    assert jk.main(["--journal", str(jp), "declare", "--label", "one", "--lines", "2-2", "--why", "w"]) == 0
    assert jk.main(["--journal", str(jp), "declare", "--label", "two", "--lines", "5-5", "--why", "w"]) == 0
    assert jk.load_segments(jp)[0].labels == ["one", "two"]
    capsys.readouterr()
    assert jk.main(["--journal", str(jp), "check"]) == 0
    assert "2 segments (one, two)" in capsys.readouterr().out


@pytest.mark.parametrize("name,args,needle", [
    ("range-past-the-end", ["--label", "branch", "--lines", "2-99", "--why", "w"], "runs past the end of the journal (4 lines)"),
    ("nothing-to-declare", ["--label", "branch", "--lines", "1-1", "--why", "w"], None),
    ("empty-why", ["--label", "branch", "--lines", "2-2", "--why", "  "], "--why is empty"),
    ("bad-label", ["--label", "Branch", "--lines", "2-2", "--why", "w"], "is not 1-24 characters"),
    ("long-label", ["--label", "a" * 25, "--lines", "2-2", "--why", "w"], "is not 1-24 characters"),
    ("bad-range", ["--label", "branch", "--lines", "5-2", "--why", "w"], "is not A-B"),
    ("range-not-numbers", ["--label", "branch", "--lines", "a-b", "--why", "w"], "is not A-B"),
    ("range-zero", ["--label", "branch", "--lines", "0-2", "--why", "w"], "is not A-B"),
])
def test_declare_refusals_write_nothing(tmp_path, capsys, name, args, needle):
    jp, sp = _paths(tmp_path, JOURNAL if name != "nothing-to-declare" else _text(
        _ev("2026-10-02T09:00:00", None, "dispatch_skipped"), BR_D, MN_D, MN_A))
    assert jk.main(["--journal", str(jp), "declare", *args]) == 1
    err = capsys.readouterr().err
    assert (needle or "nothing to declare") in err
    assert not sp.exists()


def test_declare_duplicate_label_and_a_declaration_that_fails_check(tmp_path, capsys):
    jp, sp = _paths(tmp_path)
    assert jk.main(["--journal", str(jp), "declare", "--label", "branch", "--lines", "2-2", "--why", "w"]) == 0
    before = sp.read_bytes()
    assert jk.main(["--journal", str(jp), "declare", "--label", "branch", "--lines", "3-3", "--why", "w"]) == 1
    assert "declared twice" in capsys.readouterr().err and sp.read_bytes() == before
    # declaring every instance leaves nothing undeclared: check refuses, nothing is written
    assert jk.main(["--journal", str(jp), "declare", "--label", "rest", "--lines", "3-4", "--why", "w"]) == 1
    assert "has no undeclared line" in capsys.readouterr().err and sp.read_bytes() == before


def test_declare_refuses_an_unreadable_existing_declaration(tmp_path, capsys):
    jp, sp = _paths(tmp_path)
    sp.write_text("{broken", encoding="utf-8")
    assert jk.main(["--journal", str(jp), "declare", "--label", "branch", "--lines", "2-2", "--why", "w"]) == 1
    assert "is unreadable" in capsys.readouterr().err and sp.read_text(encoding="utf-8") == "{broken"


def test_check_cli_outputs(tmp_path, capsys):
    jp, sp = _paths(tmp_path)
    assert jk.main(["--journal", str(jp), "check"]) == 0
    assert "ok -- no declaration" in capsys.readouterr().out
    sp.write_text("{broken", encoding="utf-8")
    assert jk.main(["--journal", str(jp), "check"]) == 1
    assert "journal_keys check: FAIL -- not valid JSON" in capsys.readouterr().err
    sp.write_text(_decl(_seg("branch", [BR_ID, jk.identity(MN_D), jk.identity(MN_A)])), encoding="utf-8")
    assert jk.main(["--journal", str(jp), "check"]) == 1
    assert "has no undeclared line" in capsys.readouterr().err


# ---- the real repository ----

def test_the_real_declaration_passes_check_and_has_the_measured_size():
    jp = REPO_ROOT / "logs" / "routing-log.jsonl"
    sp = REPO_ROOT / "logs" / jk.SEGMENTS_NAME
    if not jp.exists():
        pytest.skip("the forge journal history is not in this clone (github-move FK-14)")
    assert sp.exists(), "logs/journal-segments.json is part of B-402"       # the history without its declaration is a defect, not a skip
    segs, why = jk.parse_declaration(sp.read_text(encoding="utf-8"))
    assert why is None
    assert jk.check(jk.split_lines(jp.read_text(encoding="utf-8")), segs) == []
    loaded, reason = jk.load_segments(jp)
    assert reason is None and loaded.segments == segs.segments
    assert jk.summary(segs) == "1 segment (codex-fixes), 151 lines, 71 task ids"      # K3


# ---- closes_tokens: the one tokenizer of the `closes:` convention (F1 / F6 of t-525) ----

def test_closes_tokens_shapes():
    assert jk.closes_tokens("closes:t-050 and closes:t-051@codex-fixes.") == ["t-050", "t-051@codex-fixes"]
    assert jk.closes_tokens("closes:t-050,closes:t-051;") == ["t-050", "t-051"]
    assert jk.closes_tokens("discloses:t-050 encloses:t-051") == []          # the (?<!\w) boundary
    assert jk.closes_tokens("closes: t-050") == [] and jk.closes_tokens(None) == [] and jk.closes_tokens(5) == []
    assert jk.closes_tokens("closes:t-5") == ["t-5"]                          # a legacy short id stays a token (ref_key refuses it)
    assert jk.closes_tokens("closes:t-050@a closes:t-050@" + "a" * 24) == ["t-050@a", "t-050@" + "a" * 24]


@pytest.mark.parametrize("notes", [
    "closes:t-050@Codex", "closes:t-050@", "closes:t-050@codex_fixes", "closes:t-050@" + "a" * 25,
    "closes:t-050@Cod.ex",
])
def test_closes_tokens_a_malformed_label_closes_nothing_not_even_the_bare_id(notes):
    assert jk.closes_tokens(notes) == []


# ================================ the per-developer journal (t-581, F0-4) ================================
# The fixture builders are those of test_journal_per_developer.py (a tmp root with the history, the
# developer files and tools/dev.config.yaml); nothing here needs git.

import dev_config
from test_journal_per_developer import (HISTORY, DEV1, DEV2, M_CREATED, N_CREATED, created, delegated, ev,
                                        jtext, make_root, write)


def _two_files(tmp_path, dev2=None, dev1=None, **kw):
    n_lines = dev2 if dev2 is not None else [N_CREATED, delegated("t-001", "2026-10-02T09:00:00"),
                                                    delegated("t-002", "2026-10-02T09:10:00")]
    m_lines = dev1 if dev1 is not None else [M_CREATED, delegated("t-003", "2026-10-02T08:30:00")]
    return make_root(tmp_path, files={DEV1: jtext(*m_lines), DEV2: jtext(*n_lines)}, slug="dev1", **kw)


# ---- K2: a labelled closes: across files; a bare one never reaches another writer's file ----

def _row(j, rel, n):
    return next(r for r in j.rows_of(rel) if r.line_no == n)


def test_k2_a_labelled_token_names_the_task_of_that_writers_file(tmp_path):
    carrier = ev("dispatch_skipped", "2026-10-02T10:00:00", agent="scout", notes="closes:t-002@dev2")
    root = _two_files(tmp_path, dev1=[M_CREATED, delegated("t-003", "2026-10-02T08:30:00"), carrier])
    j = jk.load_all(root)
    row = _row(j, DEV1, 3)
    assert j.resolve_ref("t-002@dev2", row) == ("dev2", "t-002")
    assert j.resolve_ref("t-002@main", row) == ("", "t-002")
    assert j.resolve_ref("t-002@dev1", row) == ("", "t-002")        # the successor's slug is another name of main
    assert j.resolve_ref("t-5", row) is None                           # not a token of the grammar


def test_k2_a_bare_token_from_the_owner_file_names_main_never_the_other_writers_task(tmp_path):
    carrier = ev("dispatch_skipped", "2026-10-02T10:00:00", agent="scout", notes="closes:t-002")
    root = _two_files(tmp_path, dev1=[M_CREATED, delegated("t-003", "2026-10-02T08:30:00"), carrier])
    j = jk.load_all(root)
    row = _row(j, DEV1, 3)
    assert j.resolve_ref("t-002", row) == ("", "t-002")                # main's t-002 (the history), not dev2's
    assert ("dev2", "t-002") in {r.key for r in j.rows}              # who does hold a t-002 of her own
    # the same bare token written INSIDE dev2's file, which holds t-002, is her own task
    own = _row(j, DEV2, 3)
    assert j.resolve_ref("t-002", own) == ("dev2", "t-002")
    assert j.resolve_ref("t-001", _row(j, DEV2, 2)) == ("dev2", "t-001")
    # a bare id her file does not hold goes to main, never to a third writer
    assert j.resolve_ref("t-777", own) == ("", "t-777")


def test_k2_a_label_that_no_file_holds_closes_nothing(tmp_path):
    carrier = ev("dispatch_skipped", "2026-10-02T10:00:00", agent="scout", notes="closes:t-002@ghost")
    root = _two_files(tmp_path, dev1=[M_CREATED, delegated("t-003", "2026-10-02T08:30:00"), carrier])
    j = jk.load_all(root)
    key = j.resolve_ref("t-002@ghost", _row(j, DEV1, 3))
    assert key == ("ghost", "t-002")
    assert key not in {r.key for r in j.rows}                          # matches no task: it closes nothing
    assert "ghost" not in j.known_labels and {"", "main", "dev2", "dev1"} <= j.known_labels


def test_k2_the_validator_warns_about_a_label_no_file_holds_and_not_about_one_that_is_there():
    import journal_validator as jv
    known = {"main", "dev2", "dev1", "codex-fixes"}
    lines = [json.dumps(ev("dispatch_skipped", "2026-10-02T10:00:00", agent="scout",
                           notes="closes:t-002@dev2 closes:t-002@ghost closes:t-001@main closes:t-001@codex-fixes")),
             json.dumps(ev("defect_found", "2026-10-02T10:01:00", "t-004", ref="t-002@phantom"))]
    warns = jv._label_warnings(DEV1, lines, 5, known)
    assert len(warns) == 2
    assert "line 5" in warns[0] and "'t-002@ghost'" in warns[0] and "closes nothing" in warns[0]
    assert "line 6" in warns[1] and "'t-002@phantom'" in warns[1]


# ---- K4: the order of load_all ----

def _bytes(root, rel, data: bytes):
    p = Path(root) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)


def _order(j):
    return [(r.path.rsplit("/", 1)[-1][:-6], r.line_no) for r in j.rows]


def test_k4_files_merge_by_ts_and_equal_ts_go_history_then_successor_then_slugs(tmp_path):
    t = "2026-10-02T12:00:00"
    root = make_root(tmp_path, history=jtext(delegated("t-001", "2026-10-02T10:00:00"), delegated("t-002", t)),
                     files={DEV1: jtext(created(t, continues=HISTORY)),
                            "logs/journal/zed.jsonl": jtext(created(t)),
                            DEV2: jtext(created("2026-10-02T11:00:00"), delegated("t-001", t))})
    j = jk.load_all(root)
    assert j.problems == []
    assert _order(j) == [("routing-log", 1), ("dev2", 1), ("routing-log", 2), ("dev1", 1),
                         ("dev2", 2), ("zed", 1)]


def test_k4_a_non_monotonic_file_keeps_its_own_order(tmp_path):
    root = make_root(tmp_path, history=jtext(delegated("t-001", "2026-10-02T10:00:00"),
                                             delegated("t-002", "2026-10-02T13:30:00")),
                     files={DEV2: jtext(created("2026-10-02T09:00:00"), delegated("t-001", "2026-10-02T14:00:00"),
                                           delegated("t-002", "2026-10-02T11:00:00"),
                                           delegated("t-003", "2026-10-02T15:00:00"))})
    j = jk.load_all(root)
    assert [r.line_no for r in j.rows if r.path == DEV2] == [1, 2, 3, 4]       # the file's order, not the ts order
    assert [r.line_no for r in j.rows if r.path == HISTORY] == [1, 2]
    assert _order(j)[:2] == [("dev2", 1), ("routing-log", 1)]                    # 09:00 first, then the history's 10:00


def test_k4_a_row_with_no_usable_ts_inherits_the_ts_of_the_row_above_it(tmp_path):
    bad = dict(delegated("t-002", "2026-10-02T10:30:00"), ts="not-a-ts")
    root = make_root(tmp_path, history=jtext(delegated("t-001", "2026-10-02T10:00:00"),
                                             delegated("t-002", "2026-10-02T13:30:00")),
                     files={DEV2: jtext(created("2026-10-02T09:00:00"), bad,
                                           delegated("t-003", "2026-10-02T15:00:00")),
                            "logs/journal/dev4.jsonl": "{no json\n"})
    j = jk.load_all(root)
    order = _order(j)
    # the bad ts sits with the 09:00 line above it (before the history's 10:00); the unparsable row of dev4
    # has no ts above it and keys on "", so it comes first of all
    assert order.index(("dev2", 2)) < order.index(("routing-log", 1))
    assert order[0] == ("dev4", 1)
    dev4 = j.rows_of("logs/journal/dev4.jsonl")
    assert len(dev4) == 1 and dev4[0].obj is None and "invalid JSON" in dev4[0].error


def test_k4_one_cr_is_stripped_and_a_blank_line_is_skipped_with_its_number_counted(tmp_path):
    a, b = json.dumps(created("2026-10-02T09:00:00")), json.dumps(delegated("t-001", "2026-10-02T09:10:00"))
    root = make_root(tmp_path, history=None)
    _bytes(root, DEV2, (a + "\r\n\r\n" + b + "\r\n").encode("utf-8"))
    j = jk.load_all(root)
    assert [(r.line_no, r.raw) for r in j.rows] == [(1, a), (3, b)]     # no CR left; the blank line 2 is counted
    assert all(r.error is None for r in j.rows) and j.rows[1].key == ("dev2", "t-001")
    # only ONE trailing CR: a second one stays in the line
    _bytes(root, "logs/journal/dev4.jsonl", (a + "\r\r\n").encode("utf-8"))
    row = jk.load_all(root).rows_of("logs/journal/dev4.jsonl")[0]
    assert row.raw.endswith("\r")


def test_k4_an_empty_root_and_an_empty_developer_file(tmp_path):
    j = jk.load_all(tmp_path / "nothing")
    assert j.rows == [] and j.problems == [] and j.files == []
    root = make_root(tmp_path / "e", history=None, files={DEV2: ""})
    j = jk.load_all(root)
    assert j.rows == [] and j.problems == [] and [f.slug for f in j.files] == ["dev2"]
    assert j.next_free_id("dev2") == "t-001" and j.last_ts("dev2") is None
    assert j.successor_slug is None                     # an empty file has no line 1: it cannot continue the history


def test_k4_the_successor_continues_the_numbers_of_the_history_and_an_empty_file_does_not(tmp_path):
    root = _two_files(tmp_path)
    j = jk.load_all(root)
    assert j.successor_slug == "dev1" and j.aliases == frozenset({"main", "dev1"})
    assert j.next_free_id("") == "t-004" and j.next_free_id("main") == "t-004" and j.next_free_id("dev1") == "t-004"
    assert j.next_free_id("dev2") == "t-003"
    assert [r.line_no for r in j.logical("")] == [1, 2, 3, 1, 2]        # the history followed by the successor
    assert j.last_ts("") == "2026-10-02T08:30:00" and j.last_ts("dev2") == "2026-10-02T09:10:00"
    # a successor with only its line 1: the ids still go on from the history
    only = make_root(tmp_path / "o", files={DEV1: jtext(M_CREATED)})
    assert jk.load_all(only).next_free_id("") == "t-003"


def test_k4_two_successors_and_a_misplaced_continues_are_problems_and_none_is_a_successor(tmp_path):
    root = make_root(tmp_path, files={DEV1: jtext(M_CREATED), DEV2: jtext(created("2026-10-02T08:10:00", continues=HISTORY))})
    j = jk.load_all(root)
    assert j.successor_slug is None and any("more than one journal file continues the history" in p for p in j.problems)
    root = make_root(tmp_path / "b", files={DEV1: jtext(created("2026-10-02T08:00:00"), created("2026-10-02T08:01:00", continues=HISTORY)),
                                           DEV2: jtext(created("2026-10-02T08:10:00", continues="elsewhere.jsonl"))})
    j = jk.load_all(root)
    assert j.successor_slug is None
    assert any("`continues` is allowed on line 1 only" in p for p in j.problems)
    assert any("expected 'logs/routing-log.jsonl'" in p for p in j.problems)


# ---- K7: the slug grammar, the names, the config inputs ----

def _slug(tmp_path, text, name="r", declared=None):
    root = make_root(tmp_path / name, history=None, config=text)
    if declared:
        write(root, jk.SEGMENTS_REL, json.dumps({"version": 1, "segments": [{"label": declared, "why": "w", "lines": []}]}))
    return jk.developer_slug(root)


@pytest.mark.parametrize("value,ok", [
    ("a", False), ("ab", True), ("a" * 24, True), ("a" * 25, False), ("main", False), ("DEV1", False),
    ("dev1", True), ("m-1", True), ("1ab", False), ("-ab", False), ("ma_ria", False), ("dev1.", False),
])
def test_k7_the_slug_bounds_at_and_beyond(tmp_path, value, ok):
    slug, why = _slug(tmp_path, f"developer: {value}\n")
    if ok:
        assert (slug, why) == (value, None)
    else:
        assert slug is None and "tools/dev.config.yaml" in why and "developer: <slug>" in why     # a refusal carries its door


def test_k7_a_segment_label_is_not_a_slug(tmp_path):
    slug, why = _slug(tmp_path, "developer: codex-fixes\n", declared="codex-fixes")
    assert slug is None and "segment label" in why
    assert _slug(tmp_path, "developer: codex-fixes\n", name="plain")[0] == "codex-fixes"   # the same text, no declaration


@pytest.mark.parametrize("text", [
    "developer: dev1 # the owner\n", 'developer: "dev1"\n', "developer: 'dev1'\n", "\ufeffdeveloper: dev1\n",
    "developer: dev1\r\nstand_copy_root: C:\\x\r\n", "# who I am\nstand_copy_root: C:\\x\ndeveloper: dev1\n",
])
def test_k7_legal_spellings_of_the_key(tmp_path, text):
    assert _slug(tmp_path, text) == ("dev1", None)


@pytest.mark.parametrize("text", [
    "developer: dev1\ndeveloper: dev2\n",            # two keys: which one is meant is ambiguous
    "  developer: dev1\n",                              # not a top-level key
    "developer:\n", "developer: \n", "", "stand_copy_root: x\n", "developer: [a, b]\n",
    "developer: dev1\nunknown_key: 1\n",                # the one reader of the file refuses the whole file
    "developer dev1\n",
])
def test_k7_the_inputs_that_give_none_and_a_reason(tmp_path, text):
    slug, why = _slug(tmp_path, text)
    assert slug is None and why and "tools/dev.config.yaml" in why


def test_k7_an_absent_unreadable_or_non_utf8_config_gives_none_and_never_raises(tmp_path):
    root = make_root(tmp_path / "a", history=None)
    slug, why = jk.developer_slug(root)
    assert slug is None and "cannot be read" in why and "developer: <slug>" in why
    isdir = make_root(tmp_path / "d", history=None)
    (isdir / jk.DEV_CONFIG_REL).mkdir(parents=True)
    assert jk.developer_slug(isdir)[0] is None
    raw = make_root(tmp_path / "b", history=None)
    _bytes(raw, jk.DEV_CONFIG_REL, b"developer: mari\xff\xfe\n")
    assert jk.developer_slug(raw)[0] is None
    assert jk.developer_slug(None)[0] is None and jk.developer_slug(object())[0] is None      # never raises


def test_k7_the_slug_is_read_from_the_root_given_and_not_from_the_environment(tmp_path, monkeypatch):
    other = tmp_path / "other.yaml"
    other.write_text("developer: stranger\n", encoding="utf-8")
    monkeypatch.setenv(dev_config.ENV_DOOR, str(other))                # dev_config's own per-process door
    assert _slug(tmp_path, "developer: dev1\n") == ("dev1", None)
    assert jk.developer_slug(make_root(tmp_path / "none", history=None))[0] is None


def test_k7_one_reader_one_constant_no_second_parser_in_journal_keys():
    assert jk.SLUG_RE is dev_config.SLUG_RE
    assert not hasattr(jk, "_DEV_LINE_RE") and not hasattr(jk, "_developer_slug")
    for n in (1, 2, 24, 25):                                           # the bound of the label space holds
        assert bool(jk.SLUG_RE.match("a" * n)) == (2 <= n <= 24)
        assert bool(jk.SLUG_RE.match("a" * n)) <= bool(jk.LABEL_RE.match("a" * n))


def test_k7_journal_names_is_pure_and_names_every_problem():
    paths = ["logs/journal/dev1.jsonl", "logs/journal/Dev1.jsonl", "logs/journal/main.jsonl", "logs/journal/codex-fixes.jsonl",
             "logs/journal/x.jsonl", "logs/journal/ok-1.JSONL", "logs/journal/sub/y.jsonl", "logs/journal/notes.txt",
             "logs/routing-log.jsonl", "logs\\journal\\win.jsonl", "logs/journal/dev2.jsonl"]
    files, problems = jk.journal_names(paths, segment_labels=["codex-fixes"])
    assert [f.path for f in files] == ["logs/journal/dev1.jsonl", "logs/journal/dev2.jsonl", "logs/journal/win.jsonl"]
    text = "\n".join(problems)
    assert "Dev1.jsonl cannot be a journal file" in text and "same slug after case folding" in text
    assert "`main` is reserved" in text and "`codex-fixes` is already the label of a declared segment" in text
    assert "x.jsonl cannot be a journal file" in text and "ok-1.JSONL cannot be a journal file" in text
    assert "sub/y.jsonl" not in text and "notes.txt" not in text and "routing-log" not in text      # not journals: not mentioned
    assert all(isinstance(p, jk.NameProblem) for p in problems) and all(p.paths for p in problems)


def test_k7_the_case_folded_duplicate_is_a_name_problem_and_the_pair_is_named():
    files, problems = jk.journal_names(["logs/journal/dev1.jsonl", "logs/journal/Dev1.jsonl"])
    assert [f.slug for f in files] == ["dev1"]
    pair = [p for p in problems if "same slug" in p][0]
    assert set(pair.paths) == {"logs/journal/dev1.jsonl", "logs/journal/Dev1.jsonl"}


# ---- K17: the CLI `where` ----

def _where(root, capsys):
    rc = jk.main(["--root", str(root), "where"])
    out = capsys.readouterr()
    return rc, out.out, out.err


def test_k17_before_the_switch_it_is_the_history(tmp_path, capsys):
    rc, out, err = _where(make_root(tmp_path), capsys)
    assert rc == 0 and err == ""
    assert out.splitlines() == ["write to: logs/routing-log.jsonl", "next free id: t-003", "last ts: 2026-10-01T10:00:00"]


def test_k17_after_the_switch_with_a_slug(tmp_path, capsys):
    rc, out, err = _where(_two_files(tmp_path), capsys)
    assert rc == 0 and err == ""
    assert out.splitlines() == ["write to: logs/journal/dev1.jsonl", "next free id: t-004", "last ts: 2026-10-02T08:30:00"]
    other = _two_files(tmp_path / "n")
    write(other, jk.DEV_CONFIG_REL, "developer: dev2\n")
    rc, out, err = _where(other, capsys)
    assert rc == 0 and out.splitlines() == ["write to: logs/journal/dev2.jsonl", "next free id: t-003", "last ts: 2026-10-02T09:10:00"]


def test_k17_after_the_switch_with_a_slug_whose_file_does_not_exist_yet(tmp_path, capsys):
    root = _two_files(tmp_path)
    write(root, jk.DEV_CONFIG_REL, "developer: dev4\n")
    rc, out, err = _where(root, capsys)
    assert rc == 0
    assert out.splitlines()[0] == "write to: logs/journal/dev4.jsonl"
    assert "next free id: t-001 (the file does not exist yet" in out and "continues the history: t-004" in out
    assert "last ts: -" in out


def test_k17_after_the_switch_without_a_slug_exits_1_with_the_door(tmp_path, capsys):
    root = _two_files(tmp_path)
    (root / jk.DEV_CONFIG_REL).unlink()
    rc, out, err = _where(root, capsys)
    assert rc == 1 and out == ""
    assert "there is no file to write to" in err and "tools/dev.config.yaml" in err and "developer: <slug>" in err
    rel, why = jk.current_path(root)
    assert rel is None and "developer: <slug>" in why
    write(root, jk.DEV_CONFIG_REL, "developer: Bad Slug\n")            # E-5: a wrong slug never gives a path to write
    assert jk.current_path(root)[0] is None
    write(root, jk.DEV_CONFIG_REL, "developer: main\n")
    assert jk.current_path(root)[0] is None


def test_k17_a_tree_with_no_journal_at_all_writes_to_its_own_file_never_the_history(tmp_path, capsys):
    """GM2-4 (FK-2): a fresh repository has neither logs/journal/ nor the history file -- the history is not the answer."""
    root = tmp_path / "fresh"
    root.mkdir()
    rel, why = jk.current_path(root)                                  # no slug: nowhere to write, with the door
    assert rel is None and "developer: <slug>" in why
    rc, out, err = _where(root, capsys)
    assert rc == 1 and out == "" and "there is no file to write to" in err and "logs/routing-log.jsonl" not in err
    write(root, jk.DEV_CONFIG_REL, "developer: nova\n")
    rel, why = jk.current_path(root)
    assert rel == "logs/journal/nova.jsonl" and "journal_created" in why
    rc, out, err = _where(root, capsys)
    assert rc == 0 and out.splitlines()[0] == "write to: logs/journal/nova.jsonl"
    write(root, jk.HISTORY_REL, "")                                   # control: with the history file present the old answer stays
    assert jk.current_path(root) == (jk.HISTORY_REL, None)


def test_k17_the_command_line_entry_prints_the_same(tmp_path):
    import subprocess
    import sys
    root = _two_files(tmp_path)
    proc = subprocess.run([sys.executable, str(Path(jk.__file__)), "--root", str(root), "where"],
                          capture_output=True, text=True, encoding="utf-8")
    assert proc.returncode == 0 and proc.stdout.splitlines()[0] == "write to: logs/journal/dev1.jsonl"


# ---- the NODE of a delegated line (t-797 F5-2, M5): NODE_RE, NODE_TOKEN_RE, node_of ----

@pytest.mark.parametrize("value, ok", [
    ("forge/5/F5-2", True), ("conductor/2/C2-1", True), ("forge/4/D9", True),
    ("F5-2", False), ("forge/5", False), ("forge/0/F5-2", False), ("Forge/5/F5-2", False),
    ("forge/5/5-2", False), ("forge/5/F5-2\n", False), ("forge/5/F5-2 ", False), ("", False),
    ("forge/05/F5-2", False), ("forge//F5-2", False),
    # F6-15 (the critic's FX-6 of t-812): the id never ends in a dash; a one-letter id and a digit end stay nodes
    ("forge/5/F5-", False), ("forge/5/F-", False), ("forge/5/F5-2-", False), ("forge/5/F--", False),
    ("forge/5/F", True), ("forge/5/F5", True), ("forge/5/F5-2-3", True),
])
def test_node_re_accepts_only_slug_number_id(value, ok):
    assert (jk.NODE_RE.match(value) is not None) is ok     # `match`, not fullmatch: the trailing newline is refused too


@pytest.mark.parametrize("notes, tokens", [
    ("forge/5 F5-2 spec draft", {"forge/5/F5-2"}),                       # the old form: `<slug>/<N> <id>`
    ("node forge/5/F5-2 done", {"forge/5/F5-2"}),                        # already normalized
    ("forge/5 F5-2 and again forge/5/F5-2", {"forge/5/F5-2"}),           # the same node twice is one
    ("forge/5 F5-2 and conductor/2 C2-1", {"forge/5/F5-2", "conductor/2/C2-1"}),
    ("conductor/1 node C1-2 draft", set()),                              # prose: the id of a token holds a digit
    ("3070 passed: failed/3070/passed", set()),
    ("see plans/piles/forge/5/F5-2 file", set()),                        # inside a path
    ("forge/5 F5-2x_y", set()),                                          # more id characters follow
    ("forge/5 F5- draft", set()), ("forge/5 F5-2- draft", set()),        # F6-15: an id that ends in a dash is no token
    ("forge/5 F5-2- and forge/5 F5-2", {"forge/5/F5-2"}),
    ("", set()), (None, set()), (5, set()), (["forge/5 F5-2"], set()),
])
def test_node_tokens(notes, tokens):
    assert jk.node_tokens(notes) == tokens


@pytest.mark.parametrize("notes", ["forge/5 F5- x", "forge/5 F5-2- x", "forge/5/F5- x", "forge/5 F5-2 forge/5 F5-", "forge/4 D9"])
def test_f6_15_every_node_that_node_of_returns_is_a_node_re_form(notes):
    """The invariant between the two readers: whatever node_of names (field or notes token) is a NODE_RE string."""
    node, _reason = jk.node_of({"notes": notes})
    assert node is None or jk.NODE_RE.match(node) is not None
    assert jk.node_of({"node": "forge/5/F5-"}) == (None, "node_not_form")        # the field form: refused as a bad field


def test_node_of_the_field_first_then_the_token_normalized():
    assert jk.node_of({"node": "forge/5/F5-2", "notes": "x"}) == ("forge/5/F5-2", None)
    assert jk.node_of({"notes": "forge/5 F5-2 draft"}) == ("forge/5/F5-2", None)
    assert jk.node_of({"notes": "forge/5/F5-2 draft"}) == ("forge/5/F5-2", None)
    assert jk.node_of({"node": None, "notes": "forge/5 F5-2"}) == ("forge/5/F5-2", None)   # null is absent
    assert jk.node_of({"notes": "no node here"}) == (None, "no_node")
    assert jk.node_of({}) == (None, "no_node")


def test_node_of_e26_the_field_and_the_token_differ_two_tokens_a_bad_field():
    assert jk.node_of({"node": "forge/5/F5-2", "notes": "conductor/2 C2-1"}) == ("forge/5/F5-2", "node_token_differ")
    assert jk.node_of({"node": "forge/5/F5-2", "notes": "forge/5 F5-2"}) == ("forge/5/F5-2", None)
    assert jk.node_of({"notes": "forge/5 F5-2 conductor/2 C2-1"}) == (None, "two_tokens")        # the link is not guessed
    assert jk.node_of({"node": "F5-2", "notes": "forge/5 F5-2"}) == (None, "node_not_form")      # no fallback to the token


@pytest.mark.parametrize("value", [["forge/5/F5-2"], {"a": 1}, 5, 5.5, True, {}, []])
def test_node_of_e27_a_non_string_field_is_a_reason_never_a_type_error(value):
    assert jk.node_of({"node": value, "notes": "forge/5 F5-2"}) == (None, "node_not_string")


@pytest.mark.parametrize("obj", [None, "forge/5/F5-2", [1], 7])
def test_node_of_a_non_object_is_a_reason(obj):
    assert jk.node_of(obj) == (None, "not_an_object")


def test_node_of_a_non_string_notes_is_no_token():
    assert jk.node_of({"notes": ["forge/5 F5-2"]}) == (None, "no_node")
    assert jk.node_of({"node": "forge/5/F5-2", "notes": 5}) == ("forge/5/F5-2", None)

