#!/usr/bin/env python3
"""`manifest_put` refuses an `assertion_id` whose line holds no check (thinking-roles TR2-1; finding 20261106-proby-cel-proby-i-ostatki).

Live runs: 7 of 41 `assertion_id` values stood one line above their check (a blank line), so a probe aimed there proved nothing.
The write now cross-references the id to the file it names through the ONE reader of "what is a check on this line"
(`probe_by_code.check_on_line`): a DATA check (AR-29), refused before the commit, the unknowns a note and never a refusal (FR-59).

Each test names the mutation that kills it. The worlds are one TypeScript and one Python test file with a blank line above a
two-line check; the project is a throwaway one (`Stand`), and `tree()` is what a refusal must leave as it found it.
"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402

sys.path.insert(0, str(harness.SCRIPTS))
import manifest_put as MP  # noqa: E402
from role_cli import EXIT_REFUSED as REFUSED  # noqa: E402
from test_manifest_projection import Stand  # noqa: E402

CASE = "TC-001"

# `blank` stands one line above the check, `first` is its first line, `cont` a continuation line of its statement, `past` a line
# after the last check (the file has more lines than that).
WORLDS = {
    "typescript": {
        "file": "tests/t.spec.ts",
        "text": "import { test, expect } from '@playwright/test';\ntest('t', async () => {\n  const a = 1;\n\n"
                "  expect(a,\n    'msg').toBe(1);\n  const b = 2;\n});\n",
        "blank": 4, "first": 5, "cont": 6, "past": 7},
    "python": {
        "file": "tests/test_t.py",
        "text": "def test_run():\n    a = 1\n\n    assert (a ==\n            1)\n    b = 2\n",
        "blank": 3, "first": 4, "cont": 5, "past": 6},
}
LANGUAGES = sorted(WORLDS)


@pytest.fixture
def stand():
    with Stand() as s:
        yield s


def world(stand, language):
    w = WORLDS[language]
    target = stand.root / w["file"]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(w["text"], encoding="utf-8")
    return w


def row(w, assertion_id=None, **more) -> dict:
    out = {"instance_id": "t_instance", "file": w["file"], "covers": [CASE], "status": "green", **more}
    if assertion_id is not None:
        out["assertion_id"] = assertion_id
    return out


def put(stand, *rows):
    return stand.put({"tests": list(rows)})


@pytest.mark.parametrize("language", LANGUAGES)
def test_blank_line_above_the_check_is_refused_naming_the_line_and_the_check_below(stand, language):
    """Kill: the id's line is not looked up (a write goes through) or the refusal drops the line / the nearest check below."""
    w = world(stand, language)
    before = stand.tree()
    code, out, err = put(stand, row(w, f"{w['file']}:{w['blank']}"))
    assert code == MP.EXIT_BAD_FRAGMENT, (code, out, err)
    assert f"line {w['blank']} of {w['file']} holds no check" in err, err
    assert f"`{w['file']}:{w['first']}`" in err, f"the door is the nearest check below: {err}"
    assert stand.tree() == before, "a refused row leaves the manifest, the journal and every file as they were"


@pytest.mark.parametrize("language", LANGUAGES)
def test_the_first_line_of_the_check_is_written(stand, language):
    """Kill: a refusal of a line the check starts on (the rule counts `starts here`)."""
    w = world(stand, language)
    code, out, err = put(stand, row(w, f"{w['file']}:{w['first']}"))
    assert code == 0, (out, err)
    assert stand.manifest()["tests"][0]["assertion_id"] == f"{w['file']}:{w['first']}"
    assert "was not checked" not in out, out


@pytest.mark.parametrize("language", LANGUAGES)
def test_a_continuation_line_of_a_multi_line_check_is_written(stand, language):
    """Kill: a reader that counts only the line a check starts on (the statement SPANS the line: Lead decision 2)."""
    w = world(stand, language)
    code, out, err = put(stand, row(w, f"{w['file']}:{w['cont']}"))
    assert code == 0, (out, err)


@pytest.mark.parametrize("language", LANGUAGES)
def test_a_line_below_the_last_check_is_refused_with_no_check_below(stand, language):
    """Kill: the refusal names a check that does not exist, or lets the id through when `nearest_below` is None."""
    w = world(stand, language)
    before = stand.tree()
    code, out, err = put(stand, row(w, f"{w['file']}:{w['past']}"))
    assert code == MP.EXIT_BAD_FRAGMENT, (code, out, err)
    assert f"this test has no check below line {w['past']}" in err, err
    assert stand.tree() == before


def _note_case(stand, w, assertion_id) -> str:
    code, out, err = put(stand, row(w, assertion_id))
    assert code == 0, (assertion_id, out, err)
    assert stand.manifest()["tests"][0]["assertion_id"] == assertion_id, "the write went through"
    notes = [line for line in out.splitlines() if line.startswith("assertion_id: the line was not checked")]
    assert len(notes) == 1, f"ONE note line says it: {out!r}"
    return notes[0]


@pytest.mark.parametrize("language", LANGUAGES)
def test_an_unreadable_file_is_a_note_and_the_write_goes_through(stand, language):
    """Kill: an absent file refused (the unknown became a refusal) or passed with no word (a silent pass)."""
    w = world(stand, language)
    assert "cannot be read" in _note_case(stand, w, "tests/gone.spec.ts:3")


@pytest.mark.parametrize("language", LANGUAGES)
def test_a_suffix_with_no_reader_is_a_note(stand, language):
    """Kill: a language the table has no entry for refused (P2: the factory does not guess a grammar), or passed in silence."""
    w = world(stand, language)
    (stand.root / "tests" / "t.zzz").write_text("one\n\nthree\n", encoding="utf-8")
    assert "cannot read" in _note_case(stand, w, "tests/t.zzz:2")


@pytest.mark.parametrize("language", LANGUAGES)
def test_an_id_not_of_the_file_line_form_is_a_note(stand, language):
    """Kill: a free-text id refused (the field has always held anything) or passed with no word."""
    w = world(stand, language)
    assert "not of the form <file>:<line>" in _note_case(stand, w, f"{w['file']} the third assert")


@pytest.mark.parametrize("language", LANGUAGES)
def test_a_file_outside_the_project_root_is_a_note_and_never_read(stand, language):
    """Kill: the id's path followed out of the project (a read of a file the project does not own)."""
    w = world(stand, language)
    outside = stand.root.parent / "outside_t.spec.ts"
    outside.write_text(WORLDS["typescript"]["text"], encoding="utf-8")
    try:
        assert "outside the project root" in _note_case(stand, w, f"../{outside.name}:4")
    finally:
        outside.unlink()


def test_a_file_that_does_not_parse_is_a_note(stand):
    """Kill: a SyntaxError of the test file escapes `run` as a traceback, or refuses the row."""
    w = WORLDS["python"]
    (stand.root / w["file"]).write_text("def test_run(:\n    assert (\n", encoding="utf-8")
    assert "cannot read" in _note_case(stand, w, f"{w['file']}:2")


def test_an_unchanged_id_on_a_row_edited_for_another_field_is_not_rechecked(stand):
    """Kill: the check reads every id of a sent row (an old manifest is broken by an unrelated edit): the id is stored while the
    file is unreadable (a note), the file then appears with a blank line there, the row is edited for `why` with the SAME id ->
    written; the same row with a CHANGED id on a blank line -> refused (the control: the check is alive)."""
    w = WORLDS["typescript"]
    stale = f"{w['file']}:{w['blank']}"
    assert put(stand, row(w, stale))[0] == 0, "stored while the file is not there yet"
    world(stand, "typescript")
    code, out, err = put(stand, row(w, stale, why="an unrelated edit"))
    assert code == 0, (out, err)
    assert "was not checked" not in out and stand.manifest()["tests"][0]["why"] == "an unrelated edit", out
    code, out, err = put(stand, row(w, f"{w['file']}:3"))
    assert code == MP.EXIT_BAD_FRAGMENT, f"control: a changed id on a line with no check is refused: {out} {err}"


def test_one_bad_row_refuses_the_whole_call_and_a_row_with_no_id_is_never_read(stand):
    """Kill: the good row of the same call written while the bad one is refused (all-or-nothing), or a row with no id read."""
    w = world(stand, "typescript")
    before = stand.tree()
    good = row(w, f"{w['file']}:{WORLDS['typescript']['first']}")
    bad = row(w, f"{w['file']}:{WORLDS['typescript']['blank']}", instance_id="other_instance")
    code, out, err = put(stand, good, bad)
    assert code == MP.EXIT_BAD_FRAGMENT and "tests[1].assertion_id" in err and "tests[0]" not in err, (out, err)
    assert stand.tree() == before
    assert put(stand, row(w, instance_id="third"))[0] == 0, "a row that carries no assertion_id is not looked at"


def test_the_reader_is_imported_only_when_an_id_row_is_sent(stand, monkeypatch):
    """Kill: `probe_by_code` imported at the top of `manifest_put` (the cost paid by every write)."""
    w = world(stand, "typescript")
    monkeypatch.delitem(sys.modules, "probe_by_code", raising=False)
    assert put(stand, row(w))[0] == 0
    assert "probe_by_code" not in sys.modules, "a write with no id row never loads the probe's reader"
    assert put(stand, row(w, f"{w['file']}:{WORLDS['typescript']['first']}", why="id"))[0] == 0
    assert "probe_by_code" in sys.modules


# --- RD1-19 (FL1): a hand-typed pytest id joins the collect of its file when it is stored (FR-16, AR-15) -----------------------------
# One world: a project whose config names a real `python -m pytest`, one test file per kind of id. Expected from the card (§3 E1-E12).
NODE_WORLD = {
    "tests/test_mod.py": (
        "import pytest\n\n\ndef test_plain():\n    assert True\n\n\n"
        "@pytest.mark.parametrize('x,y', [('a', 1), ('b', 2)])\ndef test_par(x, y):\n    assert y\n\n\n"
        "@pytest.mark.parametrize('x,y', [('a', 1), ('b', 1)])\ndef test_two(x, y):\n    assert y\n\n\n"
        "class TestA:\n    def test_y(self):\n        assert True\n\n    def test_solo(self):\n        assert True\n\n\n"
        "class TestB:\n    def test_y(self):\n        assert True\n"),
    "tests/my dir/test_sp.py": "def test_sp():\n    assert True\n",
    "tests/test_none.py": "VALUE = 1\n",
}
MOD = "tests/test_mod.py"


def with_pytest(stand, **execution):
    for name, text in NODE_WORLD.items():
        target = stand.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    cfg = stand.root / "qa-factory" / "config.json"
    data = json.loads(cfg.read_text(encoding="utf-8"))
    data["test_command_templates"] = {"quiet": f'"{Path(sys.executable).as_posix()}" -m pytest -p no:cacheprovider'}
    if execution:
        data["execution"] = {**(data.get("execution") or {}), **execution}
    cfg.write_text(json.dumps(data), encoding="utf-8")


def mark_of(stand, instance):
    return next((r for r in stand.manifest()["tests"] if r.get("instance_id") == instance), {}).get("node_id_check")


def node_row(instance, file=MOD, **more):
    return {"instance_id": instance, "file": file, "covers": [CASE], "status": "green", **more}


# (label, typed id, file, stored id, status, asked) - every row is sent alone to a fresh story
NODE_ROWS = [
    ("E4a a parametrised id pytest collects under another spelling is stored as collected", "test_par[2]", MOD, "test_par[b-2]",
     "verified", "test_par[2]"),
    ("an id collected as typed is verified", "test_plain", MOD, "test_plain", "verified", None),
    ("E5a a class method typed bare: stored as typed, the class is not added", "test_solo", MOD, "test_solo", "verified", None),
    ("E5b a class path typed: asked as typed, stored as typed", "TestA::test_y", MOD, "TestA::test_y", "verified", None),
    ("E6 a path with spaces, typed with backslashes: the stored file is the role's", "test_sp", "tests\\my dir\\test_sp.py", "test_sp",
     "verified", None),
    ("E7 a file that yielded no test: not verified, never missing", "test_ghost", "tests/test_none.py", "test_ghost", "not_verified", None),
    ("E7 a file that is not there: not verified", "test_ghost", "tests/absent.py", "test_ghost", "not_verified", None),
]


# RD1-35 (F1 (b), E8): the writer's row and a hand row that copied `generated_from` (a forged mark on it) take the same ask
SENDERS = {"hand": {}, "writer": {"generated_from": ["x"]},
           "hand, copied generated_from, forged mark": {"generated_from": ["x"], "node_id_check": {"status": "verified", "note": "x"}}}
# every row by hand; the other senders on the rename (E4a) and the no-test file (E7) only - more collects kill nothing more (R4)
SENT = [(*r, "hand") for r in NODE_ROWS] + [(*NODE_ROWS[i], s) for i in (0, 5) for s in list(SENDERS)[1:]]


@pytest.mark.parametrize("label,typed,file,stored,status,asked,sender", SENT, ids=[f"{r[0][:34]}-{r[-1][:6]}" for r in SENT])
def test_a_hand_typed_id_joins_the_collect_of_its_file(stand, label, typed, file, stored, status, asked, sender):
    """Kill: the id stored as typed with no mark (the TP1-15045 defect), a `missing` said about a file that yielded nothing, the class
    added to the manifest's spelling, a path split at a space, or `file` rewritten; a writer row exempted from the ask (RD1-35)."""
    with_pytest(stand)
    code, out, err = put(stand, node_row(typed, file, **SENDERS[sender]))
    assert code == 0, (label, out, err)
    row = stand.manifest()["tests"][0]
    assert row["instance_id"] == stored and row["file"] == file, (label, row)
    mark = row["node_id_check"]
    assert mark["status"] == status and mark.get("asked") == asked and mark["note"], (label, mark)
    if status == "not_verified":
        assert "stored not_verified" in out and "node_id_check" in out, out


def test_two_collected_candidates_and_two_classes_are_refused_naming_the_doors(stand):
    """Kill: code picks between two candidates (E4b) or two classes (E5c); the refusal drops the nearest ids or the class-path door,
    leaves a trace; E13: a rewrite that makes two rows one id is refused by the merge as stored."""
    with_pytest(stand)
    before = stand.tree()
    code, out, err = put(stand, node_row("test_two[1]"))
    assert code == REFUSED and "test_two[a-1]" in err and "test_two[b-1]" in err, (out, err)
    assert "Nothing was committed" in err and "<Class>::<function>" in err and "retracted_instances" in err, err
    assert stand.tree() == before, "a refused row leaves the manifest, the journal and every file as they were"
    code, out, err = put(stand, node_row("test_y"))
    assert code == REFUSED and "TestA::test_y" in err and "TestB::test_y" in err, (out, err)
    assert put(stand, node_row("test_par[2]"), node_row("test_par[b-2]", "tests/test_none.py"))[0] == MP.EXIT_BAD_FRAGMENT, "E13: the rewritten id collides in two files"


def test_the_persons_recorded_word_passes_a_missing_id(stand):
    """Kill: the person's word ignored (a dead end, FR-57) or matched by code of its own: the existing waiver road, the words kept."""
    with_pytest(stand)
    assert put(stand, node_row("test_nowhere"))[0] == REFUSED
    pipeline = json.loads((stand.task / "pipeline.json").read_text(encoding="utf-8"))
    pipeline["stage_overrides"] = [{"stage": "S5", "match": "not collected by pytest", "decision": "go on, the person knows",
                                    "at": "2026-11-17T10:00:00", "by": "human"}]
    (stand.task / "pipeline.json").write_text(json.dumps(pipeline), encoding="utf-8")
    code, out, err = put(stand, node_row("test_nowhere"))
    assert code == 0, (out, err)
    mark = mark_of(stand, "test_nowhere")
    assert mark["status"] == "passed_by_person" and "the person knows" in mark["note"], mark


@pytest.mark.parametrize("label", ["no command", "the switch", "not startable", "a .ts row beside it (F4)"])
def test_no_collect_is_never_a_refusal_and_never_verified(stand, label):
    """Kill: an id nobody checked stored `verified` or refused (E1): no pytest-shaped command, the switch off, a command that cannot
    start, a .ts row in the same collect (RD1-35 F4: pytest collects nothing); the reason is the mark's note and one printed line."""
    cfg = stand.root / "qa-factory" / "config.json"
    more = [node_row("t one", "tests/x.spec.ts")] if "F4" in label else []
    if more:
        with_pytest(stand)
        (stand.root / "tests" / "x.spec.ts").write_text("test('t one', async () => {});\n", encoding="utf-8")
    if label == "the switch":
        with_pytest(stand, verify_node_ids=False)
    elif label == "not startable":
        with_pytest(stand)
        data = json.loads(cfg.read_text(encoding="utf-8"))
        data["test_command_templates"] = {"quiet": "no_such_runner_xyz -m pytest"}
        cfg.write_text(json.dumps(data), encoding="utf-8")
    code, out, err = put(stand, node_row("test_plain"), *more)
    assert code == 0, (label, out, err)
    for mark in [mark_of(stand, i) for i in ["test_plain"] + [r["instance_id"] for r in more]]:
        assert mark["status"] == "not_verified" and mark["note"], (label, mark)
    assert out.count("stored not_verified") == 1, (label, out)


LINKS = [{"case_id": CASE, "version": "cv_1"}]


# (typed, collected, the re-send's own fields, the covers stored after it): a partial re-send keeps the stored fields (N1)
@pytest.mark.parametrize("typed,collected,resend,covers", [
    ("test_plain", "test_plain", {}, [CASE]), ("test_par[2]", "test_par[b-2]", {}, [CASE]),
    ("test_par[2]", "test_par[b-2]", {"covers": [CASE, "TC-002"]}, [CASE, "TC-002"])])
def test_a_role_sent_mark_is_dropped_and_rows_not_asked_keep_their_state(stand, typed, collected, resend, covers):
    """Kill: the role's mark stored (AR-14); a writer row, a patch row with no file asked or marked (E9, E10); a stored
    `not_verified` row never asked again (FR-40: it has a way out once a collect can answer); A2 (critic t-1315): that row,
    renamed by the collect, left beside its new spelling as a ghost, or losing the stored fields the re-send omits (t-1325 N1)."""
    code, out, err = put(stand, node_row(typed, node_id_check={"status": "verified", "note": "mine"}, case_version_links=LINKS))
    assert code == 0 and "the value you sent was dropped" in out, (out, err)
    assert mark_of(stand, typed)["status"] == "not_verified", "no collect existed: the role's `verified` is gone"
    assert put(stand, {"instance_id": "test_w", "file": MOD, "covers": [CASE], "status": "green", "generated_from": "x"})[0] == 0
    writer = [r for r in stand.manifest()["tests"] if r.get("instance_id") == "test_w"]
    assert len(writer) == 1 and writer[0]["node_id_check"]["status"] == "not_verified", ("a writer row is asked (RD1-35)", writer)
    assert put(stand, {"instance_id": typed, "why": "patch"})[0] == 0
    patched = next(r for r in stand.manifest()["tests"] if r.get("instance_id") == typed)
    assert patched.get("why") == "patch" and patched["node_id_check"]["status"] == "not_verified", ("a no-file patch keeps the mark", patched)
    with_pytest(stand)
    assert put(stand, {"instance_id": typed, "file": MOD, "status": "red", **resend})[0] == 0
    assert mark_of(stand, collected)["status"] == "verified", "FR-40: re-sent with its file once a collect answers"
    row = next(r for r in stand.manifest()["tests"] if r.get("instance_id") == collected)
    assert (row["status"], row.get("covers"), row.get("case_version_links")) == ("red", covers, LINKS), ("N1", row)
    rows = [MP._instance(r) for r in stand.manifest()["tests"] if MP._instance(r) in (typed, collected)]
    assert rows == [collected], ("A2: one row, no ghost", rows)


# (label, the collect's answer or what it raises, typed, stored, status, asked, a part of the note) - the answer stubbed (critic t-1315)
ANSWER_ROWS = [
    ("E1 the call raises: its reason is the note", RuntimeError("collect exploded"), "test_plain", "test_plain", "not_verified",
     None, "RuntimeError: collect exploded"),
    ("A4 a judge names another function of the file", {"resolved": {f"{MOD}::test_plian": f"{MOD}::test_plain"}}, "test_plian",
     "test_plain", "verified", "test_plian", "test_plain"),
    ("A4 a judge names a test of another file", {"resolved": {f"{MOD}::test_plian": "tests/b.py::test_plain"}}, "test_plian",
     "test_plian", "not_verified", None, "another file"),
]


@pytest.mark.parametrize("label,answer,typed,stored,status,asked,note", ANSWER_ROWS, ids=[r[0][:40] for r in ANSWER_ROWS])
def test_the_mark_says_what_the_collect_answered(stand, monkeypatch, label, answer, typed, stored, status, asked, note):
    """Kill: a raising call's reason overwritten by "pytest gave no answer" (A3, E1); a judge-resolved id stamped `verified` under
    a spelling that joins nothing (A4: the stored id is the collected one, or not verified when only `file` could join it)."""
    def collect(*_, **__):
        if isinstance(answer, Exception):
            raise answer
        return answer
    import node_ids
    with_pytest(stand)
    monkeypatch.setattr(node_ids, "check_request", collect)
    code, out, err = put(stand, node_row(typed))
    assert code == 0, (label, out, err)
    row = stand.manifest()["tests"][0]
    mark = row["node_id_check"]
    assert (row["instance_id"], mark["status"], mark.get("asked")) == (stored, status, asked) and note in mark["note"], (label, row)


def test_the_authors_spelling_re_sent_after_a_rewrite_joins_the_stored_row(stand, monkeypatch):
    """Kill: a re-sent author spelling creating a second row (E8), or asking pytest again for a spelling the store knows."""
    with_pytest(stand)
    assert put(stand, node_row("test_par[2]"))[0] == 0
    import node_ids
    monkeypatch.setattr(node_ids, "check_request", lambda *a, **k: pytest.fail("a known spelling is never collected again"))
    code, out, err = put(stand, node_row("test_par[2]", why="patched"))
    assert code == 0, (out, err)
    rows = stand.manifest()["tests"]
    assert [r["instance_id"] for r in rows] == ["test_par[b-2]"] and rows[0]["why"] == "patched", rows


# (label, the id the carriers hold, the row sent beside them, the seeded second claimant of the spelling, the id they hold after)
# Expected from card E13 and critic t-1360 R3: no carrier keeps a spelling the row lost; a spelling two rows claim stays as written.
CARRIERS = [
    ("renamed: the collected spelling in both carriers", "test_par[2]", "test_par[2]", False, "test_par[b-2]"),
    ("ambiguous: two stored rows claim it, as written", "test_par[2]", "test_plain", True, "test_par[2]"),
    ("no rename: byte for byte", "test_plain", "test_plain", False, "test_plain"),
]


@pytest.mark.parametrize("label,held,sent,seeded,after", CARRIERS, ids=[r[0][:8] for r in CARRIERS])
def test_the_carriers_of_a_renamed_row_follow_its_collected_spelling(stand, label, held, sent, seeded, after):
    """Kill: `_rewrite_instance_ids` skipping `unresolved[]` or `obligation_bindings[]` (E13: a carrier keeping the spelling its row
    lost), a name two rows claim rewritten to either or to null, a row that was not renamed touched (RD1-40, critic t-1360 R3)."""
    with_pytest(stand)
    if seeded:
        claim = {"status": "verified", "note": "n", "asked": held}
        stand.append_projected({"tests": [{"instance_id": f"test_par[{k}-2]", "file": MOD, "covers": [CASE], "status": "green",
                                           "node_id_check": claim} for k in "xz"]}, "seed")
    unresolved = {"case": CASE, "reason": "impossible", "detail": "d", "instance_ids": [held]}
    binding = {"obligation_id": "OB-1", "instance_ids": [held]}
    code, out, err = stand.put({"tests": [node_row(sent)], "unresolved": [unresolved], "obligation_bindings": [binding]})
    assert code == 0, (label, out, err)
    stored = stand.manifest()
    assert stored["unresolved"][0]["instance_ids"] == [after], (label, stored["unresolved"])
    assert stored["obligation_bindings"][0]["instance_ids"] == [after], (label, stored["obligation_bindings"])


def test_nothing_to_ask_starts_no_process_and_replay_never_collects(stand, monkeypatch):
    """Kill: a subprocess for a fragment with nothing to ask (E11), or a collect on replay (E14: a replayed event folds to its mark)."""
    import node_ids
    with_pytest(stand)
    assert put(stand, node_row("test_par[2]"))[0] == 0
    monkeypatch.setattr(node_ids, "check_request", lambda *a, **k: pytest.fail("no collect expected"))
    for fragment in ({"tests": []}, {"tests": [{"instance_id": "x"}]}, {"tests": [{"file": MOD, "function": "test_plain"}]}):
        assert MP.stamp_node_ids(fragment, stand.task, stand.root) == (fragment, [], [])
    assert stand.recover()[0] == 0 and mark_of(stand, "test_par[b-2]")["asked"] == "test_par[2]"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q", "-p", "no:cacheprovider"]))
