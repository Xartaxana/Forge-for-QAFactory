"""Tests for tools/piles.py: the parsers, `summary`, the refused `board`, the usage errors and the gate's own semantics (F0-2a).

Part of the split of the old tools/test_piles.py (t-596, the 120 s cap per file): the helpers are in
tools/piles_testkit.py, the fixtures `session_tree`, `tree`, `cli` in tools/conftest.py.
Run from the repo root: python -m pytest tools/test_piles.py -q
"""
import pathlib
import shutil
import subprocess
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
TOOLS = pathlib.Path(__file__).resolve().parent
REAL = TOOLS.parent
import piles  # noqa: E402
from piles_testkit import (GIT_VARS, clean_env, put, BACKLOG, card_text, batch_text, node, finding_text, ROW1, ROW2,  # noqa: E402
                           needs_git, stage, edit, CARD, B1, commit, freeze, git, msg, head_hash)


@pytest.fixture(autouse=True)
def _scrub_git_env(monkeypatch):
    for k in GIT_VARS:
        monkeypatch.delenv(k, raising=False)


# ================================================================== parsers

def test_split_cells_is_backtick_aware_and_honours_escaped_pipe():
    cells = piles.split_cells("| B-102 | **x** `a|b` y | c\\|d | `p|q` |")
    assert cells == ["B-102", "**x** `a|b` y", "c\\|d", "`p|q`"]
    assert piles.split_cells("| a | | b |") == ["a", "", "b"]       # an empty middle cell survives
    assert piles.split_cells("| a | `unclosed | b |") == ["a", "`unclosed", "b"]   # a lone backtick is literal


def test_header_pairs_first_colon_and_ticks():
    p = piles.header_pairs("кучка: `forge` | MR: https://git/x/y:1 | ветка: `main` (a: b) | зона: `a`, `b`")
    assert p["кучка"] == "forge" and p["mr"] == "https://git/x/y:1"
    assert p["ветка"] == "`main` (a: b)" and p["зона"] == "`a`, `b`"
    assert piles.first_tick(p["ветка"]) == "main"


@pytest.mark.parametrize("raw,word", [("сдано 08.10", "сдано"), ("В РАБОТЕ", "в работе"), (" `принято` ", "принято"),
                                      ("влито 05403ea", None), ("принятое", None), ("—", None)])
def test_status_word(raw, word):
    assert piles.status_word(raw, piles.NODE_STATUSES) == word


def test_status_word_node_only_word():
    assert piles.status_word("отклонено", piles.NODE_STATUSES) == "отклонено"
    assert piles.status_word("отклонено") is None            # a batch is never "отклонено"


@pytest.mark.parametrize("cell,expect", [
    ("B-230, B-454, B-135, B-162 (пути), B-267 (пути)",
     [("B-230", ""), ("B-454", ""), ("B-135", ""), ("B-162", "(пути)"), ("B-267", "(пути)")]),
    ("B-361/B-414", [("B-361", ""), ("B-414", "")]),
    ("B-408 (a)(b) (замер Антона)", [("B-408", "(a)(b) (замер Антона)")]),
    ("B-309 (г)–(и)", [("B-309", "(г)–(и)")]),
    ("B-299 (= B-418)", [("B-299", "(="), ("B-418", ")")]),      # m11: an id inside a qualifier is a member
])
def test_parse_members(cell, expect):
    members, _ = piles.parse_members(cell)
    assert [(m.id, m.qualifier) for m in members] == expect
    assert all(m.partial == bool(m.qualifier) for m in members)


def test_parse_members_nonid_pieces():
    members, nonid = piles.parse_members("B-100, W7, затем B-101 (a, b), —")
    assert [m.id for m in members] == ["B-100", "B-101"]
    assert nonid == ["W7", "затем B-101 (a, b)"][:1] or nonid == ["W7"]
    assert "—" not in nonid


@pytest.mark.parametrize("text,expect", [
    ("закрыто кодом: model-rates.json:83", None),
    ("| Закрыто 06.10.2026 чтением (`06b835b`) |", "06b835b"),
    ("закрыто кодом: bac83cb", "bac83cb"),
    ("влито `c16fb81` + `0877601`", "c16fb81"),
    ("пайплайны после: 7883565", None),
    ("закрыто кодом: t-574, probe_by_code.py:1906-1911", None),
    ("влито `7848917` + база `7ed70ac`", "7848917"),                 # a digits-only hash in backticks IS a hash
    ("закрыто кодом: `0275882`", "0275882"),
    ("закрыто: 7883565, затем bac83cb", "bac83cb"),                  # a bare digits-only token is skipped, not fatal
    ("надо закрыть bac83cb", None),                                   # "закрыть" is no marker
    ("закрыто 08.10.2026 пачкой `forge/1`: влито `1234567`", "1234567"),
    # m-4 (t-593): a close by the owner's word -- the hash is the word stamp's own, never a hex token of the word
    ("| B-102 | что | почему | владелец; закрыто 08.10.2026 по слову: abcdef1; влито `1234567` | P1 |", "1234567"),
    ("| B-102 | что | почему | владелец; закрыто 08.10.2026 по слову: abcdef1 | P1 |", None),
    ("| B-102 | что | почему | владелец; закрыто 08.10.2026 по слову: владелец, 08.10 | P1 |", None),
])
def test_closed_hash_forms(text, expect):
    assert piles.closed_hash(text) == expect


def test_parse_backlog_rows_sections_columns_cells():
    bl = piles.parse_backlog_rows(BACKLOG)
    assert [r.id for r in bl.rows if not r.closed] == ["B-015", "B-102", "B-135", "B-219", "B-230", "B-308"]
    assert bl.n_closed == 6 and bl.boundary > 0
    r102 = next(r for r in bl.rows if r.id == "B-102")
    assert r102.section == "7" and len(r102.cells) == 5                 # the pipes inside backticks did not split
    assert r102.fields["witness"] == "свидетель `x|y`" and r102.fields["source"] == "источник 1"
    r15 = next(r for r in bl.rows if r.id == "B-015")
    assert r15.section == "1" and r15.fields["witness"] == "детали прогона" and r15.fields["source"] == "—"


def test_parse_backlog_witness_column_and_irregular_rows():
    text = ("## 10. Ошибки\n\n| id | что сделать | свидетель | источник | принципы |\n|---|---|---|---|---|\n"
            "| B-120 | w | чем видно | src | pr |\n| B-121 | w | только три |\n| B-122 | a | b | c | d | лишнее |\n\n## Закрыто\n")
    bl = piles.parse_backlog_rows(text)
    by = {r.id: r for r in bl.rows}
    assert by["B-120"].fields["witness"] == "чем видно" and not by["B-120"].irregular
    assert by["B-121"].irregular and by["B-121"].fields["source"] == "—"
    assert by["B-122"].irregular and by["B-122"].fields["what"].endswith("лишнее")


def test_parse_backlog_without_boundary_cannot_run():
    with pytest.raises(piles.CannotRun) as e:
        piles.parse_backlog_rows("| B-001 | x |\n")
    assert "## Закрыто" in str(e.value)


def test_parse_backlog_locks():
    t = "# T\n\npiles-freeze: 2026-10-08 open=1 closed=0\npiles-freeze: nonsense\n```\npiles-freeze: 2026-10-08 open=9 closed=9\n```\n\n## Закрыто\n"
    bl = piles.parse_backlog_rows(t)
    assert [v for _, v in bl.locks] == [("2026-10-08", 1, 0), None]     # the one inside a code fence is not a lock


def test_parse_card_and_errors():
    card = piles.parse_card(card_text("forge", "Forge", [ROW1, ROW2]), "plans/piles/forge/README.md")
    assert card.errors == [] and card.title_slug == "forge" and card.name == "Forge"
    assert card.priority == "П1" and card.features == ["F19"]
    assert [(r.n, r.status, [m.id for m in r.members]) for r in card.rows] == [(1, "в работе", ["B-230"]), (2, "ожидает", ["B-015"])]
    bad = piles.parse_card("# Нет slug\n\nнет свойств\n", "x/README.md")
    assert any("heading" in e for e in bad.errors) and any("no batch table" in e for e in bad.errors)
    odd = piles.parse_card(card_text("p", "P", [["0", "x", "B-100", "S", "забыто", "—", "—", "—"]]), "x/README.md")
    assert any("1-999" in e for e in odd.errors) and any("забыто" in e for e in odd.errors)


def test_parse_batch_header_nodes_queue():
    text = batch_text("forge", 3, "сдано 08.10", [node("F0-1", "`a.py`, `b/*.py`"), node("B-100", "нет", "принято")],
                      pre="очередь: forge/1 → forge/3\nочередь: x/2 -> forge/3\n")
    b = piles.parse_batch(text, "plans/piles/forge/batch-3-x.md")
    assert b.n == 3 and b.status == "сдано" and b.errors == []
    assert b.queue == [("forge", 1, "forge", 3), ("x", 2, "forge", 3)]
    assert b.nodes[0].writers == ["a.py", "b/*.py"] and b.nodes[1].status == "принято"
    assert piles.writers_of(b) == ["a.py", "b/*.py"]                        # a принято node writes nothing any more


def test_parse_finding_header_and_name():
    f = piles.parse_finding(finding_text("B-102"), "plans/piles/forge/findings/B-102-x.md")
    assert f.id == "B-102" and f.name_id == "B-102" and f.pile == "forge" and f.errors == []
    nf = piles.parse_finding(finding_text("—"), "plans/piles/forge/findings/20261008-slug.md")
    assert nf.id == "" and nf.errors == []
    bad = piles.parse_finding("# t\n\nбез шапки\n", "plans/piles/forge/findings/B-1.md")
    assert len(bad.errors) == 2                                             # the name (B-1) and the header
    wrong = piles.parse_finding(finding_text("B-1x"), "plans/piles/forge/findings/B-102.md")
    assert any("expected B-nnn" in e for e in wrong.errors)


def test_real_forge_card_and_batch_parse_clean():
    card = piles.parse_card(piles.read_text(REAL / "plans/piles/forge/README.md"), "plans/piles/forge/README.md")
    batch = piles.parse_batch(piles.read_text(REAL / "plans/piles/forge/batch-1-foundation.md"),
                              "plans/piles/forge/batch-1-foundation.md")
    assert card.errors == [] and batch.errors == []
    assert card.rows and batch.nodes and batch.status in piles.BATCH_STATUSES


# ================================================================== the refused `board` alias, `summary`

def test_pile_folder_without_readme_is_red_in_check(tree, cli):
    (tree / "plans/piles/ghost").mkdir()
    put(tree, "plans/piles/ghost/findings/B-102-x.md", finding_text("B-102", "ghost"))
    code, out = cli(tree, "check", "--all")
    assert code == 2 and "ghost/README.md" in out and "has no README.md card" in out


@pytest.mark.parametrize("cmd", [("board",), ("board", "--check", "--if-staged"), ("board", "--help")])
def test_board_is_a_refused_alias_naming_the_pane(tree, cli, cmd):
    code, out = cli(tree, *cmd)
    assert code == 1 and "backlog_tree.py" in out and "«Бэклог»" in out and "nothing was run" in out, out
    assert not (tree / "plans/PILES.md").exists()


def test_refusals_exit_1(tree, cli):
    edit(tree, "plans/BACKLOG.md", "## Закрыто", "## Закрытое")
    for cmd in (("check", "--all"), ("summary",)):
        code, out = cli(tree, *cmd)
        assert code == 1 and '"## Закрыто"' in out, (cmd, out)
    for cmd in (("board",), ("board", "--check", "--if-staged")):
        code, out = cli(tree, *cmd)
        assert code == 1 and "backlog_tree.py" in out, (cmd, out)


def test_summary_prints_the_count_line_and_writes_nothing(tree, cli):
    before = {p: p.read_bytes() for p in (tree / "plans").rglob("*") if p.is_file()}
    code, out = cli(tree, "summary")
    assert code == 0 and out.startswith("кучек: 2; пачек: ") and "следующий свободный B-id: B-" in out, out
    assert "; остатков без исполнителя: " in out
    assert {p: p.read_bytes() for p in (tree / "plans").rglob("*") if p.is_file()} == before
    assert not (tree / "plans/PILES.md").exists()


def test_summary_counts_a_finding_without_id_and_an_empty_tree(tree, cli, tmp_path):
    put(tree, "plans/piles/forge/findings/20261008-bez-id.md", finding_text("—"))
    assert "находок без id: 1" in cli(tree, "summary")[1]
    (tmp_path / "plans").mkdir()
    (tmp_path / "plans/BACKLOG.md").write_bytes(BACKLOG.encode("utf-8"))
    code, out = cli(tmp_path, "summary")
    assert code == 0 and out.startswith("кучек: 0; пачек: нет; открытых id: ") and "закрытых: " in out, out


@needs_git
def test_usage_error_is_exit_1(tree, cli):
    assert cli(tree, "nonsense")[0] == 1
    assert cli(tree, "check", "--base", "no-such-rev", "--all")[0] == 1


# ================================================================== check: gate semantics

@needs_git
def test_check_nothing_staged_runs_nothing(tree, cli):
    code, out = cli(tree, "check")
    assert code == 0 and "nothing to check" in out
    put(tree, "docs/x.md", "x\n")
    stage(tree, "docs/x.md")
    assert "nothing to check" in cli(tree, "check")[1]


def test_check_outside_git_cannot_list_staged(tmp_path, cli):
    shutil.copytree(REAL / "plans/piles", tmp_path / "plans/piles")
    code, out = cli(tmp_path, "check")
    assert code == 1 and "cannot list the staged paths" in out and "--all" in out


def test_check_mini_tree_is_green(tree, cli):
    code, out = cli(tree, "check", "--all")
    assert code == 0, out
    assert "(а) placement: ok" in out and "(в) NOT CHECKED" in out and "(г) NOT CHECKED" in out
    assert "not frozen yet" in out


# ------------------------------------------------------------------ SL-2 (t-406): a check judges only the piles the commit touches

SCOPE_ROWS = {}
NOT_BLOCKING = "red(s) in piles this commit does not touch (not blocking)"


def scope_row(name):
    def register(fn):
        SCOPE_ROWS[name] = fn
        return fn
    return register


def _bad_finding(tree, pile, name="20261009-bad.md"):
    (tree / "plans/piles" / pile / "findings").mkdir(parents=True, exist_ok=True)
    (tree / "plans/piles" / pile / "findings" / name).write_bytes(b"# t\n\n\xff\xfe not utf-8\n")


def _touch_forge_card(tree):
    edit(tree, CARD, "Текст.", "Текст!")
    stage(tree, CARD)


def _two_developers(tree, w2="`tools/a.py`", w1=None):
    """Batch forge/1 (Ира) and a second pile's batch 1 (Катя), both «в работе», committed."""
    if w1:
        put(tree, B1, batch_text("forge", 1, "в работе", [node("F0-1", w1)]))
    put(tree, "plans/piles/report-delivery/README.md", card_text("report-delivery", "Report", [
        ["1", "x", "B-219", "M", "в работе", "Катя", "`main` (x)", "—"]], "F08"))
    put(tree, "plans/piles/report-delivery/batch-1-x.md",
        batch_text("report-delivery", 1, "в работе", [node("R1-1", w2)], who="Катя"))
    commit(tree, "two developers")


def _fn_world(tree):
    put(tree, "tools/x.py", "def a1():\n    pass\n\n\ndef b1():\n    pass\n")
    _two_developers(tree, "`tools/x.py (b1)`", "`tools/x.py (a1)`")
    assert piles.run_check(tree, True)[0] == 0                 # the control: the world is green before the code commit
    return head_hash(tree)


@scope_row("foreign-untracked-pile")
def _foreign_untracked(tree):
    put(tree, "plans/piles/stranger-pile/README.md", card_text("stranger-pile", "S"))
    put(tree, "plans/piles/stranger-pile/findings/20261014-orphan.md", finding_text("—", "stranger-pile"))
    _bad_finding(tree, "stranger-pile")
    _touch_forge_card(tree)
    return [(("check",), 0, ["piles check: ok"], ["stranger-pile", "cannot read this finding", "RED"])]


@scope_row("foreign-tracked-red")
def _foreign_tracked(tree):
    _bad_finding(tree, "report-delivery")
    commit(tree, "a red in Y")
    _touch_forge_card(tree)
    return [(("check",), 0, ["(д) form: 1 %s: report-delivery" % NOT_BLOCKING, "piles check: ok"], ["RED"])]


@scope_row("own-pile-red-elsewhere-in-pile")
def _own_pile_red(tree):
    _bad_finding(tree, "forge")
    commit(tree, "a red in X")
    edit(tree, B1, "Правило готовности.", "Правило готовности!")
    stage(tree, B1)
    return [(("check",), 2, ["(д) form: RED", "cannot read this finding"], [])]


@scope_row("a9-removal")
def _a9_removal(tree):
    freeze(tree)
    git(tree, "rm", "-q", "plans/piles/forge/findings/B-102-x.md")
    return [(("check",), 2, ["(а) placement: RED", "B-102 is open but placed nowhere"], [])]


@scope_row("a9-backlog-only")
def _a9_backlog_only(tree):
    freeze(tree)
    edit(tree, "plans/BACKLOG.md", "| B-308 |", "| B-777 | **Новое.** | почему | источник | P1 |\n| B-308 |")
    stage(tree, "plans/BACKLOG.md")
    door = msg(tree, "s\n\npiles-skip: г -- the new row is the point of this test\n")        # (г) passed: (а) alone must block
    return [(("check", "--msg-file", door), 2, ["(а) placement: RED", "B-777 is open but placed nowhere"], [])]


@scope_row("cross-pile-dupe")
def _cross_pile_dupe(tree):
    freeze(tree)
    put(tree, "plans/piles/report-delivery/findings/B-102-y.md", finding_text("B-102", "report-delivery"))
    commit(tree, "the id has two homes")
    _touch_forge_card(tree)                        # the commit touches the OTHER home
    return [(("check",), 2, ["(а) placement: RED", "B-102 is in 2 finding files"], [])]


@scope_row("xpile-unknown-id")
def _xpile_unknown_id(tree):
    """B.3: deleting a finding in pile B creates an unknown-id red in pile A's card (a partial member lives in another pile);
    a commit staging only B's delete is judged, and the green control is the same world before the delete."""
    freeze(tree)
    put(tree, "plans/piles/report-delivery/findings/B-900-x.md", finding_text("B-900", "report-delivery"))
    edit(tree, CARD, "| 2 | потом | B-015 |", "| 2 | потом | B-015, B-900 (часть) |")
    commit(tree, "forge row 2 names B-900 (partial); its finding lives in report-delivery")
    assert piles.run_check(tree, True)[0] == 0                 # the control: no unknown id while the finding exists
    git(tree, "rm", "-q", "plans/piles/report-delivery/findings/B-900-x.md")
    return [(("check",), 2, ["(а) placement: RED", "unknown id B-900 in the row of batch forge/2"], [])]


@scope_row("overlap-pair-one-side")
def _pair_one_side(tree):
    _two_developers(tree)
    edit(tree, "plans/piles/report-delivery/batch-1-x.md", "Правило готовности.", "Правило готовности!")
    stage(tree, "plans/piles/report-delivery/batch-1-x.md")
    return [(("check",), 2, ["(б) overlap: RED", "forge/1 and report-delivery/1 both write: tools/a.py"], [])]


@scope_row("overlap-pair-neither-side")
def _pair_neither_side(tree):
    put(tree, "plans/piles/third-pile/README.md", card_text("third-pile", "T"))
    _two_developers(tree)
    edit(tree, "plans/piles/third-pile/README.md", "Текст.", "Текст!")
    stage(tree, "plans/piles/third-pile/README.md")
    return [(("check",), 0, ["(б) overlap: 1 %s: forge" % NOT_BLOCKING, "piles check: ok"], ["RED"])]


@scope_row("fn-list-code-commit")
def _fn_code_commit(tree):
    _fn_world(tree)
    put(tree, "tools/x.py", "def a1():\n    pass\n")              # b1 is removed: the red names tools/x.py, no pile path is staged
    stage(tree, "tools/x.py")
    return [(("check",), 2, ["(б) overlap: RED", "report-delivery/1 lists b1 for tools/x.py"], [])]


@scope_row("fn-list-py-not-listed")
def _fn_not_listed(tree):
    _fn_world(tree)
    put(tree, "tools/y.py", "def other():\n    pass\n")
    stage(tree, "tools/y.py")
    return [(("check",), 0, ["piles check: no plans/piles or BACKLOG path staged -- nothing to check"], [])]


@scope_row("fn-list-py-waiting-batch")
def _fn_waiting(tree):
    _fn_world(tree)
    put(tree, "tools/w.py", "def only_waiting():\n    pass\n")
    put(tree, "plans/piles/report-delivery/batch-2-w.md",
        batch_text("report-delivery", 2, "ожидает", [node("R2-1", "`tools/w.py (only_waiting)`", "ожидает")], who="—", branch="—"))
    commit(tree, "a waiting batch lists tools/w.py")
    put(tree, "tools/w.py", "def renamed():\n    pass\n")                  # only an active batch's list makes a `.py` relevant
    stage(tree, "tools/w.py")
    return [(("check",), 0, ["nothing to check"], [])]


@scope_row("partly-untracked-pile")
def _partly_untracked(tree):
    _bad_finding(tree, "forge")                               # a new finding not yet added: the commit does not contain it
    edit(tree, B1, "Правило готовности.", "Правило готовности!")
    stage(tree, B1)
    return [(("check",), 0, ["piles check: ok"], ["cannot read this finding", "RED"])]


@scope_row("fn-list-range")
def _fn_range(tree):
    base = _fn_world(tree)
    put(tree, "tools/x.py", "def a1():\n    pass\n")
    commit(tree, "remove b1")
    return [(("check", "--base", base), 2, ["(б) overlap: RED", "report-delivery/1 lists b1 for tools/x.py"], []),
            (("check", "--base", head_hash(tree)), 0, ["nothing to check"], [])]


@scope_row("renamed-batch")
def _renamed(tree):
    _bad_finding(tree, "forge")
    commit(tree, "a red in X")
    git(tree, "mv", B1, "plans/piles/forge/batch-1-renamed.md")
    assert {B1, "plans/piles/forge/batch-1-renamed.md"} <= set(piles.staged_paths(tree))       # both paths are touched
    return [(("check",), 2, ["(д) form: RED"], [])]


@scope_row("deleted-pile-move-line")
def _deleted_pile(tree):
    put(tree, "plans/piles/zed/README.md", card_text("zed", "Z"))
    put(tree, "plans/piles/zed/batch-1-x.md", batch_text("zed", 1, "ожидает", [
        ["Z1-1", "П1", "`20261014-moved.md` -- узел", "builder", "`tools/z.py`", "—", "ожидает"]], who="—", branch="—"))
    put(tree, "plans/piles/forge/findings/20261014-moved.md",
        finding_text("—", "forge") + "\nперенос: zed/findings/20261014-moved.md\n")
    commit(tree, "a finding moved to zed")
    git(tree, "rm", "-r", "-q", "plans/piles/zed")
    return [(("check",), 2, ["(е) findings: RED", "20261014-moved.md"], [])]


@scope_row("range-mode")
def _range_mode(tree):
    first = head_hash(tree)
    _bad_finding(tree, "report-delivery")
    commit(tree, "A: a red in Y")
    second = head_hash(tree)
    _touch_forge_card(tree)
    commit(tree, "B: the card of X")
    return [(("check", "--base", second), 0, ["(д) form: 1 %s: report-delivery" % NOT_BLOCKING], ["RED"]),
            (("check", "--base", first), 2, ["(д) form: RED", "cannot read this finding"], [])]


@scope_row("range-empty")
def _range_empty(tree):
    return [(("check", "--base", "HEAD"), 0, ["nothing to check"], [])]


@scope_row("range-bad-rev")
def _range_bad_rev(tree):
    return [(("check", "--base", "no-such-rev"), 1, ["does not resolve to a commit"], [])]


@scope_row("all-mode-untracked-note")
def _all_mode(tree):
    put(tree, "plans/piles/stranger-pile/README.md", card_text("stranger-pile", "S"))
    _bad_finding(tree, "stranger-pile")
    return [(("check", "--all"), 2, ["(д) form: RED", "cannot read this finding", "untracked pile(s) stranger-pile"], [])]


@needs_git
@pytest.mark.parametrize("row", sorted(SCOPE_ROWS))
def test_check_scope_touched_piles(tree, cli, row):
    """B.1-B.6: a red blocks a commit only when a carrier is a touched path or lies in a touched pile (`--all` blocks on every one);
    a red elsewhere is one summary line per item; the untracked files of other piles are not read in a commit."""
    for args, code, needles, absent in SCOPE_ROWS[row](tree):
        got, out = cli(tree, *args)
        assert got == code and all(n in out for n in needles) and not any(a in out for a in absent), (args, out)


def test_cli_end_to_end_subprocess(tree):
    p =subprocess.run([sys.executable, "-B", str(TOOLS / "piles.py"), "--repo", str(tree), "check", "--all"],
                       capture_output=True, env=clean_env())
    assert p.returncode == 0 and "piles check: ok" in p.stdout.decode("utf-8")


# ================================================================== (б) overlap: the function-list door (t-877, forge F6-26, D-0048)
# Two batches «в работе» that write the same file: green with a disjoint function list of EACH (and every name defined in the file),
# red as before otherwise. Unit level (parse_batch + _pair_overlap on a tmp tree) except the two CLI tests at the end.

K1, K2 = ("forge", 1), ("forge", 2)
HOT_REL = "scripts/hot.py"                      # a package path: the file lives under ai-packages/qa-factory/
HOT_SRC = ("def top_one():\n    pass\n\n\ndef top_two():\n    pass\n\n\nclass Driver:\n    def take_answer(self):\n        pass\n\n"
           "    def last_resort(self):\n        def inner_helper():\n            pass\n\n\nasync def agen():\n    pass\n")


def hot_tree(root, rel="ai-packages/qa-factory/" + HOT_REL, src=HOT_SRC):
    put(root, rel, src)
    return root


def _batch(n, writes, hod="", pre="", status="в работе", nodes=None):
    text = batch_text("forge", n, status, nodes or [node("F6-%d" % n, writes)], pre=pre)
    return piles.parse_batch(text.replace("## Ход\n\n- x\n", "## Ход\n\n- x\n" + hod, 1) if hod else text,
                             "plans/piles/forge/batch-%d-x.md" % n)


def _overlap(root, w1, w2, hod1="", hod2="", pre1="", pre2=""):
    return piles._pair_overlap(_batch(1, w1, hod1, pre1), _batch(2, w2, hod2, pre2), K1, K2, root)


@pytest.mark.parametrize("w1,w2", [
    ("`%s (top_one)`" % HOT_REL, "`%s (top_two)`" % HOT_REL),                            # form 1, inside the backticks
    ("`%s` (`top_one`)" % HOT_REL, "`%s` (`top_two`)" % HOT_REL),                        # form 2, after the closing backtick
    ("`%s (top_one)`" % HOT_REL, "`%s` (`top_two`, `top_two`)" % HOT_REL),               # mixed; a duplicate name in a list is fine
    ("`%s (Driver.take_answer)`" % HOT_REL, "`%s (Driver.last_resort, agen)`" % HOT_REL),  # members of a class, an async def
    ("`%s (take_answer)`" % HOT_REL, "`ai-packages/qa-factory/%s (last_resort)`" % HOT_REL),  # the package prefix is stripped
])
def test_f626_overlap_two_disjoint_function_lists_are_green(tmp_path, w1, w2):
    assert _overlap(hot_tree(tmp_path), w1, w2) == []


def test_f626_overlap_a_file_outside_the_package_root_is_read_from_the_repo_root(tmp_path):
    hot_tree(tmp_path, "tools/hot.py")
    assert _overlap(tmp_path, "`tools/hot.py (top_one)`", "`tools/hot.py (top_two)`") == []


def test_f626_overlap_common_names_are_red_and_named(tmp_path):
    msgs = _overlap(hot_tree(tmp_path), "`%s (top_one, take_answer)`" % HOT_REL, "`%s (top_two, take_answer, top_one)`" % HOT_REL)
    assert len(msgs) == 1
    assert "forge/1 and forge/2 both write %s and both name take_answer, top_one" % HOT_REL in msgs[0]
    assert "disjoint" in msgs[0] and 'очередь: forge/1 → forge/2' in msgs[0] and "piles-skip: б" in msgs[0]


def test_f626_overlap_Driver_prefix_is_normalised_to_the_bare_name(tmp_path):
    """`Driver.take_answer` in one batch and `take_answer` in the other is the SAME function: red, named by the bare name."""
    msgs = _overlap(hot_tree(tmp_path), "`%s (Driver.take_answer)`" % HOT_REL, "`%s (take_answer)`" % HOT_REL)
    assert len(msgs) == 1 and "both name take_answer" in msgs[0] and "Driver." not in msgs[0]


@pytest.mark.parametrize("name", ["take_answer", "last_resort", "top_one", "agen"])
def test_f626_overlap_a_name_defined_anywhere_at_module_or_class_level_is_found(tmp_path, name):
    """The NEGATIVE-FORM control of the next test: real names (module level, class members, async) pass the existence check."""
    assert _overlap(hot_tree(tmp_path), "`%s (%s)`" % (HOT_REL, name), "`%s (top_two)`" % HOT_REL) == []


@pytest.mark.parametrize("bad", ["take_answr", "Take_answer", "inner_helper", "Driver", "no_such_function"])
def test_f626_overlap_an_undefined_name_is_red_naming_the_file_and_the_name(tmp_path, bad):
    """FR-59: a typo (or a case slip, a nested helper, a class name) must not pass as 'disjoint'."""
    msgs = _overlap(hot_tree(tmp_path), "`%s (%s)`" % (HOT_REL, bad), "`%s (top_two)`" % HOT_REL)
    assert len(msgs) == 1 and "forge/1 lists %s for %s" % (bad, HOT_REL) in msgs[0] and "is not defined in the file" in msgs[0]
    msgs = _overlap(hot_tree(tmp_path), "`%s (top_one)`" % HOT_REL, "`%s (top_two, %s)`" % (HOT_REL, bad))
    assert len(msgs) == 1 and "forge/2 lists %s for %s" % (bad, HOT_REL) in msgs[0]


def test_f626_overlap_every_bad_name_of_both_batches_is_named(tmp_path):
    msgs = _overlap(hot_tree(tmp_path), "`%s (typo_a, top_one)`" % HOT_REL, "`%s (typo_b, typo_c)`" % HOT_REL)
    assert len(msgs) == 2 and "typo_a" in msgs[0] and "typo_b, typo_c" in msgs[1] and "are not defined" in msgs[1]


@pytest.mark.parametrize("w1,w2,who", [
    ("`%s (top_one)`" % HOT_REL, "`%s`" % HOT_REL, "forge/2"),                           # a list on one side only
    ("`%s`" % HOT_REL, "`%s (top_two)`" % HOT_REL, "forge/1"),
    ("`%s`" % HOT_REL, "`%s`" % HOT_REL, "forge/1 and forge/2"),                         # neither: the file lock as before
    ("`%s (S0–S3)`" % HOT_REL, "`%s` (тексты `handoff`)" % HOT_REL, "forge/1 and forge/2"),   # prose in brackets is no list
    ("`%s ()`" % HOT_REL, "`%s (top_two)`" % HOT_REL, "forge/1"),                        # an EMPTY list is no list
])
def test_f626_overlap_a_list_on_one_side_or_none_keeps_the_file_lock(tmp_path, w1, w2, who):
    msgs = _overlap(hot_tree(tmp_path), w1, w2)
    assert len(msgs) == 1 and "forge/1 and forge/2 both write: %s" % HOT_REL in msgs[0]
    assert 'add the line "очередь: forge/1 → forge/2"' in msgs[0] and "or give %s a function list for %s" % (who, HOT_REL) in msgs[0]


def test_f626_overlap_the_queue_line_in_both_preambles_stays_green_whatever_the_lists_say(tmp_path):
    q = "\nочередь: forge/1 → forge/2\n"
    root = hot_tree(tmp_path)
    assert _overlap(root, "`%s`" % HOT_REL, "`%s`" % HOT_REL, pre1=q, pre2=q) == []                       # the old form, no lists
    assert _overlap(root, "`%s (typo)`" % HOT_REL, "`%s (typo)`" % HOT_REL, pre1=q, pre2=q) == []         # lists are not even read
    # the old red forms are unchanged: a queue on one side only is red, with the old door text
    msgs = _overlap(root, "`%s`" % HOT_REL, "`%s`" % HOT_REL, pre1=q)
    assert len(msgs) == 1 and msgs[0].startswith("forge/1 and forge/2 both write: %s -- add the line" % HOT_REL)


def test_f626_overlap_lists_do_not_hide_a_disagreement_on_the_order_of_the_unlisted_files(tmp_path):
    """Both batches also share a.py with no lists and say opposite queue directions: that red stays, the listed file is green."""
    msgs = _overlap(hot_tree(tmp_path), "`%s (top_one)`, `tools/a.py`" % HOT_REL, "`%s (top_two)`, `tools/a.py`" % HOT_REL,
                    pre1="\nочередь: forge/1 → forge/2\n", pre2="\nочередь: forge/2 → forge/1\n")
    assert len(msgs) == 1 and "both write: tools/a.py" in msgs[0] and "disagree on the order" in msgs[0] and HOT_REL not in msgs[0]


def test_f626_overlap_one_node_that_writes_the_file_bare_makes_the_batch_a_whole_file_claim(tmp_path):
    nodes = [node("F6-1", "`%s (top_one)`" % HOT_REL), node("F6-9", "`%s`" % HOT_REL)]
    msgs = piles._pair_overlap(_batch(1, "", nodes=nodes), _batch(2, "`%s (top_two)`" % HOT_REL), K1, K2, hot_tree(tmp_path))
    assert len(msgs) == 1 and "or give forge/1 a function list" in msgs[0]
    nodes = [node("F6-1", "`%s (top_one)`" % HOT_REL), node("F6-9", "`%s (take_answer)`" % HOT_REL)]      # both listed: the union
    assert piles._pair_overlap(_batch(1, "", nodes=nodes), _batch(2, "`%s (top_two)`" % HOT_REL), K1, K2, tmp_path) == []
    nodes[1] = node("F6-9", "`%s`" % HOT_REL, "принято")                                                  # a принято node writes nothing
    nodes[0] = node("F6-1", "`%s (top_one)`" % HOT_REL)
    assert piles._pair_overlap(_batch(1, "", nodes=nodes), _batch(2, "`%s (top_two)`" % HOT_REL), K1, K2, tmp_path) == []


def test_f626_overlap_a_taken_batch_declares_its_list_in_its_hod(tmp_path):
    """The node cell of a taken batch is frozen by (в); a «Ход» line is how it narrows its claim."""
    root = hot_tree(tmp_path)
    hod = "- 16.10 09:00 — функции: `%s` (`top_one`, `Driver.take_answer`)\n" % HOT_REL
    assert _overlap(root, "`%s`" % HOT_REL, "`%s (top_two)`" % HOT_REL, hod1=hod) == []
    assert _overlap(root, "`%s`" % HOT_REL, "`%s`" % HOT_REL, hod1=hod, hod2="- функции: `%s (top_two)`\n" % HOT_REL) == []
    msgs = _overlap(root, "`%s`" % HOT_REL, "`%s (top_one)`" % HOT_REL, hod1=hod)                         # the Ход list meets the cell's
    assert len(msgs) == 1 and "both name top_one" in msgs[0]
    assert len(_overlap(root, "`%s`" % HOT_REL, "`%s (top_two)`" % HOT_REL)) == 1                          # control: no Ход line, the lock
    # a keyed list in some OTHER section is no declaration
    assert piles._hod_lists(["## Остатки", "- функции: `%s (top_one)`" % HOT_REL]) == {}
    assert piles._hod_lists(["## Ход", "- функции: `%s (top_one)`" % HOT_REL, "## Остатки"]) == {HOT_REL: ["top_one"]}


@pytest.mark.parametrize("line", [
    "- 16.10 09:00 — функции: scripts/hot.py (top_one, Driver.take_answer)",       # the path without backticks (the form the Lead writes)
    "- 16.10 09:00 — функции: `scripts/hot.py` (`top_one`, `Driver.take_answer`)",
    "- 16.10: функции: `scripts/hot.py (top_one, Driver.take_answer)`",              # form 1 inside the backticks
    "функции: scripts/hot.py (top_one, Driver.take_answer)",                         # the line STARTS with the key
    "* 2026-10-16 09:00 — Функции: scripts/hot.py (top_one, Driver.take_answer)",    # another marker, an ISO date, the key in any case
    "1. 16.10.2026 — функции: scripts/hot.py (top_one), scripts/hot.py (Driver.take_answer)",   # two listed mentions union
])
def test_f626_hod_key_line_forms_all_declare(line):
    assert piles._hod_lists(["## Ход", line]) == {HOT_REL: ["top_one", "Driver.take_answer"]}


@pytest.mark.parametrize("line", [
    "- 16.10: поправила `scripts/hot.py` (`top_one`) по пину",                      # the critic's probe A: a progress note with brackets
    "- 16.10 09:00 — t-877: функции: scripts/hot.py (top_one)",                      # the key is not at the start of the line
    "- функции для scripts/hot.py (top_one)",                                       # no colon right after the word
    "- scripts/hot.py (top_one) — функции: ",                                       # the key is after the list
    "- 16.10 — функции: scripts/hot.py ()",                                         # an EMPTY bracket is no list
    "- 16.10 — функции: scripts/hot.py (S0–S3)",                                    # prose in brackets is no list
    "- 16.10 — функции: scripts/hot.py (top_one), scripts/hot.py",                  # a bare repeat in the same line is a whole-file mention
    "- 16.10 — функции: take_answer",                                               # names with no file
    "<!-- - 16.10 — функции: scripts/hot.py (top_one) -->",                         # inside a comment
])
def test_f626_hod_prose_and_malformed_key_lines_declare_nothing(line):
    assert piles._hod_lists(["## Ход", line]) == {}


def test_f626_a_narrative_hod_line_never_narrows_a_bare_node_claim(tmp_path):
    """The critic's probe A (t-880 F-1, the direction `tokens_overlap` must never err in): a bare node + a progress note with
    brackets stays the whole-file claim, so the pair with another batch's list stays RED."""
    root = hot_tree(tmp_path)
    note = "- 16.10: поправила `%s` (`top_one`) по пину\n" % HOT_REL
    msgs = _overlap(root, "`%s`" % HOT_REL, "`%s (top_two)`" % HOT_REL, hod1=note)
    assert len(msgs) == 1 and "or give forge/1 a function list for %s" % HOT_REL in msgs[0]
    keyed = note.replace("поправила", "функции:").replace(" по пину", "")                                    # the control: the keyed form declares
    assert _overlap(root, "`%s`" % HOT_REL, "`%s (top_two)`" % HOT_REL, hod1=keyed) == []


@pytest.mark.parametrize("n", [1, 2])
def test_f626_the_live_conductor_hod_declares_no_list(n):
    """The live batches whose Ход carried bracket prose (`очередь: C1-5b1 → …`, `handed_records (T12)`) read no list from it."""
    for p in (REAL / "plans/piles/conductor").glob("batch-%d-*.md" % n):
        assert piles.parse_batch(p.read_bytes().decode("utf-8"), "plans/piles/conductor/" + p.name).hod_lists == {}


def test_f626_a_hod_list_for_a_file_the_batch_does_not_write_is_ignored_with_a_warn_not_red(tree, cli):
    _two_hot_batches(tree, "`%s`" % HOT_REL, "`%s (top_two)`" % HOT_REL)
    f = tree / "plans/piles/forge/batch-1-foundation.md"
    f.write_text(f.read_text(encoding="utf-8").replace("## Ход\n\n- x\n", "## Ход\n\n- x\n- функции: tools/other.py (top_one)\n", 1), encoding="utf-8")
    b = piles.parse_batch(f.read_bytes().decode("utf-8"), "plans/piles/forge/batch-1-foundation.md")
    assert b.hod_lists == {"tools/other.py": ["top_one"]} and piles.hod_ignored(b) == ["tools/other.py"]
    code, out = cli(tree, "check", "--all")
    assert code == 2 and "WARN: forge/1" in out and "tools/other.py" in out and "ignored" in out      # red only for the lock itself
    f.write_text(f.read_text(encoding="utf-8").replace("tools/other.py (top_one)", "%s (top_one)" % HOT_REL), encoding="utf-8")
    code, out = cli(tree, "check", "--all")
    assert code == 0 and "WARN: forge/1" not in out, out


@pytest.mark.parametrize("rel", ["docs/notes.md", "tools/*.py", "scripts/"])
def test_f626_overlap_a_list_on_a_file_that_is_not_one_named_python_file_is_ignored(tmp_path, rel):
    """A markdown file, a glob, a directory: no names to check, so a list changes nothing -- the lock is red as before."""
    hot_tree(tmp_path, "docs/notes.md", "# notes\n")
    msgs = _overlap(tmp_path, "`%s (top_one)`" % rel, "`%s (top_two)`" % rel)
    assert len(msgs) == 1 and "both write: %s" % rel in msgs[0]


def test_f626_overlap_a_list_on_a_file_only_one_batch_writes_is_ignored(tmp_path):
    """No overlap, no red -- and a typo in such a list is not judged (the check is of the shared file)."""
    assert _overlap(hot_tree(tmp_path), "`%s (typo_only)`" % HOT_REL, "`tools/other.py (top_two)`") == []


@pytest.mark.parametrize("src,why", [(None, "there is no file scripts/hot.py"), ("def broken(:\n", "cannot be read as Python (SyntaxError)")])
def test_f626_overlap_a_file_that_cannot_be_read_is_red_not_a_pass(tmp_path, src, why):
    root = hot_tree(tmp_path, "ai-packages/qa-factory/" + HOT_REL, src) if src is not None else tmp_path
    msgs = _overlap(root, "`%s (top_one)`" % HOT_REL, "`%s (top_two)`" % HOT_REL)
    assert len(msgs) == 1 and why in msgs[0] and "the lists cannot be checked" in msgs[0]


@pytest.mark.parametrize("cell,paths,lists", [
    ("`a.py (f, g)`", ["a.py"], {"a.py": ["f", "g"]}),
    ("`a.py` (`f`, Driver.g)", ["a.py"], {"a.py": ["f", "Driver.g"]}),             # the Class. prefix is kept (t-880 F-3)
    ("`a.py (f, +g, +Driver.h)`", ["a.py"], {"a.py": ["f", "+g", "+Driver.h"]}),    # `+name`: a function the node ADDS (t-880 F-6)
    ("`a.py (+ g)`", ["a.py"], {}),                                                    # a plus with a space is no name
    ("`a.py (f)`, `a.py`", ["a.py", "a.py"], {}),                                      # a bare repeat in one cell is a whole-file claim (F-2)
    ("`a.py`, `a.py` (`f`)", ["a.py", "a.py"], {}),
    ("`a.py (f)`, `a.py` (`g`), `b.py`", ["a.py", "a.py", "b.py"], {"a.py": ["f", "g"]}),   # two LISTED mentions union
    ("`a.py`, `b.py (f)`", ["a.py", "b.py"], {"b.py": ["f"]}),                       # a list belongs to the path it follows
    ("`a.py (S0–S3)`", ["a.py"], {}),                                                  # prose: the path is cut clean, no list
    ("`a.py (f g)`", ["a.py"], {}),                                                    # a piece with a space is no name
    ("`a.py (f,)`", ["a.py"], {}),                                                     # an empty piece is no name
    ("`a.py` (f()))", ["a.py"], {}),                                                   # a call is no name
    ("`a.py` (new)", ["a.py"], {}),                                                    # the new-file marker of the manifests, live in the cells
    ("`a.py (New)`, `b.py` (new, f)", ["a.py", "b.py"], {"b.py": ["new", "f"]}),       # ... only ALONE; a real list may hold the name
    ("`no_move(state, options)`", ["no_move(state, options)"], {}),                     # no space before the bracket: not the form
    ("`a.py`", ["a.py"], {}),
])
def test_f626_parse_writers_reads_a_list_only_where_every_piece_is_a_name(cell, paths, lists):
    assert piles.parse_writers(cell) == (paths, lists)


def _two_hot_batches(tree, w1, w2, st2="в работе"):
    hot_tree(tree)
    put(tree, "plans/piles/forge/README.md", card_text("forge", "Forge", [
        ["1", "a", "B-230", "L", "в работе", "Ира", "`main`", "—"], ["2", "b", "B-015", "M", st2, "Катя", "`pile/forge/batch-2`", "—"]]))
    put(tree, "plans/piles/forge/batch-1-foundation.md", batch_text("forge", 1, "в работе", [node("F0-1", w1)]))
    put(tree, "plans/piles/forge/batch-2-next.md",
        batch_text("forge", 2, st2, [node("F0-2", w2)], pre="## Бриф\n" if st2 == "ожидает" else ""))   # an untaken batch has its «## Бриф» (F6-28)


def test_f626_check_cli_green_on_disjoint_lists_red_on_overlap_and_on_a_typo(tree, cli):
    _two_hot_batches(tree, "`%s (top_one)`" % HOT_REL, "`%s (top_two)`" % HOT_REL)
    code, out = cli(tree, "check", "--all")
    assert code == 0 and "(б) overlap: ok" in out, out
    _two_hot_batches(tree, "`%s (top_one, take_answer)`" % HOT_REL, "`%s (top_two, take_answer)`" % HOT_REL)
    code, out = cli(tree, "check", "--all")
    assert code == 2 and "(б) overlap: RED" in out and "both name take_answer" in out, out
    _two_hot_batches(tree, "`%s (top_one)`" % HOT_REL, "`%s (top_twoo)`" % HOT_REL)
    code, out = cli(tree, "check", "--all")
    assert code == 2 and "forge/2 lists top_twoo for %s" % HOT_REL in out, out
    _two_hot_batches(tree, "`%s (top_one)`" % HOT_REL, "`%s (top_twoo)`" % HOT_REL, st2="ожидает")   # a batch not «в работе» is not read
    code, out = cli(tree, "check", "--all")
    assert code == 0 and "(б) overlap: ok" in out, out


def test_f626_take_runs_the_same_judgement_before_it_takes(tree):
    """`take` calls (б) for the batch it takes (_overlap_refusal): the list overlap refuses it, disjoint lists let it through."""
    for w2, refused in (("`%s (top_two, take_answer)`" % HOT_REL, True), ("`%s (top_two)`" % HOT_REL, False)):
        _two_hot_batches(tree, "`%s (top_one, take_answer)`" % HOT_REL, w2, st2="ожидает")
        t = piles.load_tree(tree)
        f = piles.parse_batch((tree / "plans/piles/forge/batch-2-next.md").read_bytes().decode("utf-8"), "plans/piles/forge/batch-2-next.md")
        if refused:
            with pytest.raises(piles.Refused) as e:
                piles._overlap_refusal(t, f, ("forge", 2), tree)
            assert "both name take_answer" in str(e.value) and "then run take again" in str(e.value)
        else:
            piles._overlap_refusal(t, f, ("forge", 2), tree)


# ------------------------------------------------------------------ t-880 fix round (F-2 ... F-8)

def test_f626_a_bare_repeat_of_a_listed_file_in_one_cell_is_the_lock(tmp_path):
    root = hot_tree(tmp_path)
    for w1 in ("`%s (top_one)`, `%s`" % (HOT_REL, HOT_REL), "`%s`, `%s` (`top_one`)" % (HOT_REL, HOT_REL)):
        msgs = _overlap(root, w1, "`%s (top_two)`" % HOT_REL)
        assert len(msgs) == 1 and "or give forge/1 a function list for %s" % HOT_REL in msgs[0]
    # the control: two LISTED mentions of the file in one cell are one list (the union)
    assert _overlap(root, "`%s (top_one)`, `%s` (`take_answer`)" % (HOT_REL, HOT_REL), "`%s (top_two)`" % HOT_REL) == []


@pytest.mark.parametrize("item,red", [
    ("Driver.take_answer", False), ("Driver.last_resort", False), ("take_answer", False),
    ("Nope.take_answer", True),         # the class does not exist, though take_answer exists in Driver (the critic's probe C)
    ("Driver.top_one", True),           # a module-level function is not a member of Driver
    ("Driver.agen", True), ("Driver.no_such", True),
])
def test_f626_a_class_prefix_names_a_class_that_defines_the_method(tmp_path, item, red):
    msgs = _overlap(hot_tree(tmp_path), "`%s (%s)`" % (HOT_REL, item), "`%s (top_two)`" % HOT_REL)
    assert bool(msgs) is red
    if red:
        assert len(msgs) == 1 and "forge/1 lists %s for %s, which is not defined in the file" % (item, HOT_REL) in msgs[0]


def test_f626_the_typo_refusal_names_the_hod_key_first_then_the_cell_and_says_it_is_frozen(tmp_path):
    msg = _overlap(hot_tree(tmp_path), "`%s (typo)`" % HOT_REL, "`%s (top_two)`" % HOT_REL)[0]
    assert msg.index("`функции:` line of the batch's «Ход»") < msg.index("«Пишет в» cell (a batch not yet taken: a taken batch's cell is frozen)")
    assert "piles-skip: б" in msg and "очередь: forge/1 → forge/2" in msg


def test_f626_the_lock_door_names_every_unlisted_shared_file_and_both_forms(tmp_path):
    root = hot_tree(tmp_path)
    put(root, "ai-packages/qa-factory/scripts/hot2.py", HOT_SRC)
    msgs = _overlap(root, "`scripts/hot.py (top_one)`, `scripts/hot2.py`", "`scripts/hot.py`, `scripts/hot2.py (top_two)`")
    assert len(msgs) == 1
    assert "or give forge/2 a function list for scripts/hot.py; and forge/1 a function list for scripts/hot2.py" in msgs[0]
    assert "`функции: scripts/hot.py (f1, f2)`" in msgs[0] and "«Ход»" in msgs[0] and "«Пишет в» cell" in msgs[0]


def test_f626_plus_name_is_accepted_without_a_def_and_counted_in_the_disjointness(tmp_path):
    root = hot_tree(tmp_path)
    assert _overlap(root, "`%s (+brand_new)`" % HOT_REL, "`%s (top_two)`" % HOT_REL) == []
    assert _overlap(root, "`%s (+Driver.brand_new)`" % HOT_REL, "`%s (top_two)`" % HOT_REL) == []      # the class exists
    # counted: the other batch naming the same function (added, or by class) meets it
    msgs = _overlap(root, "`%s (+brand_new)`" % HOT_REL, "`%s (+brand_new, top_two)`" % HOT_REL)
    assert len(msgs) == 1 and "both name brand_new (brand_new: both claim to ADD it)" in msgs[0]
    msgs = _overlap(root, "`%s (+brand_new)`" % HOT_REL, "`%s (+Driver.brand_new)`" % HOT_REL)
    assert len(msgs) == 1 and "both claim to ADD it" in msgs[0]
    # a plus with a class that is not in the file is red, naming it
    msgs = _overlap(root, "`%s (+Nope.brand_new)`" % HOT_REL, "`%s (top_two)`" % HOT_REL)
    assert len(msgs) == 1 and "forge/1 lists +Nope.brand_new for %s, which is not defined" % HOT_REL in msgs[0]


@pytest.mark.parametrize("item", ["+top_one", "+take_answer", "+Driver.take_answer", "+agen"])
def test_f626_plus_name_that_the_file_already_defines_is_red_not_new(tmp_path, item):
    msgs = _overlap(hot_tree(tmp_path), "`%s (%s)`" % (HOT_REL, item), "`%s (top_two)`" % HOT_REL)
    assert len(msgs) == 1 and "forge/1 lists %s as ADDED for %s, but the file already defines it" % (item, HOT_REL) in msgs[0]


def test_f626_merge_unique_keeps_the_order_and_drops_repeats():
    assert piles.merge_unique(["a", "b"], ["b", "c", "a", "c"]) == ["a", "b", "c"]
    assert piles.merge_unique([], []) == []


def test_f626_the_batch_template_documents_the_list_forms_and_declares_nothing_itself():
    text = (REAL / "plans/piles/_template/batch.md").read_bytes().decode("utf-8").replace("\r\n", "\n")   # a Windows checkout is CRLF
    for key in ("функции:", "(f1, f2)", "Class.name", "+name", "«Пишет в»"):
        assert key in text, key
    b = piles.parse_batch(text, "plans/piles/_template/batch.md", 1)
    assert b.hod_lists == {} and all(n.lists == {} for n in b.nodes)       # the example sits in a comment: it places nothing
    keyed = piles.parse_batch(text.replace("## Ход\n", "## Ход\n\n- функции: scripts/x.py (f1)\n", 1), "plans/piles/_template/batch.md", 1)
    assert keyed.hod_lists == {"scripts/x.py": ["f1"]}                       # the negative control: a live keyed line does declare
