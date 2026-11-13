"""Tests for tools/piles.py: what a FINDING carries (date, text, unreadable) and the tolerant readers of finding files (F2-8,
B-471). Run from the repo root: python -m pytest tools/test_piles_findings.py -q

The helpers are in tools/piles_testkit.py, the fixtures `session_tree`, `tree`, `cli` in tools/conftest.py. A tolerant reader
(check, summary, forge_metrics, compact_snapshot) reads every finding it can and names the one it cannot; a strict one (take,
close, split, the GitLab mirror) refuses to write from a tree it could not read whole.
"""
import datetime
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import piles  # noqa: E402
from piles_testkit import (CARD, GIT_VARS, accept_batch1, batch_text, commit, edit, finding_text, head_hash, msg,  # noqa: E402
                           needs_git, node, put, stage, tree_state)

FDIR = "plans/piles/forge/findings/"
BAD = FDIR + "20261009-bad.md"
BAD_BYTES = b"# t\n\n\xff\xfe not utf-8\n"


@pytest.fixture(autouse=True)
def _scrub_git_env(monkeypatch):
    for k in GIT_VARS:
        monkeypatch.delenv(k, raising=False)


def with_header(date_text, ident="B-102"):
    return "# t\n\nid: %s | кучка: `forge` | от: %s | приоритет: — | кандидат наверх: нет\n\nчто не так\n" % (ident, date_text)


def bad_finding(tree, rel=BAD):
    (tree / rel).parent.mkdir(parents=True, exist_ok=True)
    (tree / rel).write_bytes(BAD_BYTES)


# ---------------------------------------------------------------- Finding.date: the one date reader

@pytest.mark.parametrize("name,header,expect", [
    ("20261008-x.md", "x", datetime.date(2026, 10, 8)),                  # the file name's yyyymmdd- wins
    ("20261008-x.md", "01.02.2025", datetime.date(2026, 10, 8)),         # ... over the header
    ("B-102-x.md", "08.10", datetime.date(2026, 10, 8)),                 # no date in the name: the header's DD.MM, the freeze year
    ("B-102-x.md", "08.10.2025", datetime.date(2025, 10, 8)),            # ... or DD.MM.YYYY
    ("B-102-x.md", "x", None),                                           # neither: a date is never guessed
    ("B-102-x.md", "31.02", None),                                       # the calendar refuses it
    ("20261340-x.md", "08.10", None),                                    # a bad date in the NAME is None: no fallback to the header
])
def test_finding_date_comes_from_the_name_else_the_header(name, header, expect):
    f = piles.parse_finding(with_header(header), FDIR + name)
    assert f.date == expect


def test_a_finding_without_a_header_still_carries_the_date_of_its_name_and_its_text():
    text = "# t\n\nбез шапки\n"
    named = piles.parse_finding(text, FDIR + "20261008-x.md")
    assert named.date == datetime.date(2026, 10, 8) and named.text == text and named.unreadable == ""
    assert any("no header line" in e for e in named.errors)
    assert piles.parse_finding(text, FDIR + "B-102-x.md").date is None


def test_a_zero_byte_finding_is_readable_not_unreadable(tree):
    f = piles.parse_finding("", FDIR + "20261008-x.md")
    assert f.text == "" and f.unreadable == "" and f.date == datetime.date(2026, 10, 8)
    put(tree, FDIR + "20261008-empty.md", "")
    loaded = piles.load_tree(tree, tolerant=True).piles["forge"].findings
    empty = next(x for x in loaded if x.name == "20261008-empty.md")
    assert empty.unreadable == "" and empty.text == ""                    # "empty" is not "unreadable"


def test_a_crlf_and_bom_finding_equals_its_lf_twin():
    lf = with_header("08.10")
    twin = piles.parse_finding("﻿" + lf.replace("\n", "\r\n"), FDIR + "B-102-x.md")   # parse_finding itself, not read_text
    assert twin == piles.parse_finding(lf, FDIR + "B-102-x.md")
    assert "\r" not in twin.text and not twin.text.startswith("﻿")
    assert piles.parse_finding(lf.replace("\n", "\r"), FDIR + "B-102-x.md").text == lf     # a lone CR too


def test_a_crlf_and_bom_file_loads_as_its_lf_twin(tree):
    lf = with_header("08.10")
    (tree / FDIR).mkdir(parents=True)
    (tree / FDIR / "B-102-a.md").write_bytes(b"\xef\xbb\xbf" + lf.replace("\n", "\r\n").encode("utf-8"))
    (tree / FDIR / "B-102-b.md").write_bytes(lf.encode("utf-8"))
    a, b = piles.load_tree(tree, tolerant=True).piles["forge"].findings
    assert a.text == b.text == lf and a.date == b.date == datetime.date(2026, 10, 8) and a.errors == b.errors == []


# ---------------------------------------------------------------- the tolerant load

def odd_findings(tree):
    put(tree, FDIR + "B-102-good.md", finding_text("B-102"))
    bad_finding(tree)                                                      # 0xFF bytes
    (tree / FDIR / "x.md").mkdir()                                         # a directory named like a finding
    put(tree, FDIR + "B-135-good.md", finding_text("B-135"))


def test_a_tolerant_load_names_the_unreadable_and_still_reads_every_sibling(tree):
    odd_findings(tree)
    found = {f.name: f for f in piles.load_tree(tree, tolerant=True).piles["forge"].findings}
    assert set(found) == {"B-102-good.md", "B-135-good.md", "20261009-bad.md", "x.md"}
    assert found["B-102-good.md"].id == "B-102" and found["B-135-good.md"].id == "B-135" and not found["B-102-good.md"].unreadable
    bad, directory = found["20261009-bad.md"], found["x.md"]
    assert "not valid UTF-8" in bad.unreadable and bad.id == "" and bad.text == "" and bad.date == datetime.date(2026, 10, 9)
    assert bad.errors == ["cannot read this finding (%s) -- expected a UTF-8 text file; save it as UTF-8 or delete it" % bad.unreadable]
    assert directory.unreadable and directory.id == "" and directory.text == ""
    forge = piles.load_tree(tree, tolerant=True).piles["forge"]
    assert not [e for e in forge.errors if "cannot read" in e[1]]          # the generic list does not repeat it: check (д) has one red


def test_a_strict_load_still_refuses_a_tree_it_could_not_read_whole(tree):
    odd_findings(tree)
    with pytest.raises(piles.CannotRun, match="cannot read .*20261009-bad.md.*save it as UTF-8"):
        piles.load_tree(tree)
    with pytest.raises(piles.CannotRun):
        piles.load_pile(tree, tree / "plans/piles/forge")


def test_a_directory_named_like_a_finding_is_unreadable_not_a_crash(tree):
    (tree / FDIR / "x.md").mkdir(parents=True)
    f = piles.load_tree(tree, tolerant=True).piles["forge"].findings[0]
    assert f.name == "x.md" and f.unreadable and f.errors


# ---------------------------------------------------------------- check (д): one red, a door, fail-closed

@needs_git
def test_check_all_has_exactly_one_red_for_an_unreadable_finding_and_the_door_passes_it(tree, cli):
    bad_finding(tree)
    code, out = cli(tree, "check", "--all")
    assert code == 2 and out.count("cannot read this finding") == 1, out
    assert ("%s: cannot read this finding (" % BAD) in out and "its id is unknown, so (а) placement did not see it" in out
    assert "expected a UTF-8 text file; save it as UTF-8 or delete it" in out and "(д) form: RED" in out
    code, out = cli(tree, "check", "--all", "--msg-file", msg(tree, "s\n\npiles-skip: д -- the file is mid-conversion\n"))
    assert code == 0 and "passed by the commit message" in out, out


@needs_git
@pytest.mark.parametrize("where,blocks", [
    ("forge", True),                  # the unreadable finding is committed in the pile the commit touches: its own path carries it
    ("report-delivery", False),       # ... in another pile: summarised in one line, never blocking (B.3)
    ("report-delivery-untracked", False),     # ... or untracked in another pile: not even read (B.2)
])
def test_a_staged_card_is_blocked_by_an_unreadable_finding_only_in_its_own_pile(tree, cli, where, blocks):
    pile = where.replace("-untracked", "")
    bad_finding(tree, "plans/piles/%s/findings/20261009-bad.md" % pile)
    if not where.endswith("-untracked"):
        commit(tree, "a bad finding")
    edit(tree, CARD, "Текст.", "Текст!")
    stage(tree, CARD)
    code, out = cli(tree, "check")
    if blocks:
        assert code == 2 and "cannot read this finding" in out and "(д) form: RED" in out, out
    else:
        assert code == 0 and "cannot read this finding" not in out, out
        assert ("(д) form: 1 red(s) in piles this commit does not touch (not blocking): %s" % pile in out) == (where == "report-delivery"), out


@needs_git
def test_a_staged_unreadable_finding_is_blocked_by_its_own_path(tree, cli):
    bad_finding(tree)
    stage(tree, BAD)
    code, out = cli(tree, "check")
    assert code == 2 and "cannot read this finding" in out, out


@needs_git
def test_check_names_nothing_when_no_piles_path_is_staged(tree, cli):
    bad_finding(tree)
    code, out = cli(tree, "check")
    assert code == 0 and "nothing to check" in out, out


# ---------------------------------------------------------------- the strict callers

@needs_git
def test_take_and_close_stay_strict_and_write_nothing(tree, cli):
    bad_finding(tree)
    code, out = cli(tree, "take", "forge", "2", "--who", "Dev1", "--today", "2026-10-08")
    assert code == 1 and "cannot read" in out and "20261009-bad.md" in out and "save it as UTF-8" in out, out
    accept_batch1(tree)
    snap = tree_state(tree)
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree), "--today", "2026-10-08")
    assert code == 1 and "cannot read" in out and "20261009-bad.md" in out, out
    assert tree_state(tree) == snap


# ---------------------------------------------------------------- (е) findings: every finding is in a batch (D-0044, t-769)

B1 = "plans/piles/forge/batch-1-foundation.md"
NEW = "20261014-novoe.md"
NEW_REL = FDIR + NEW


def run_e(tree, staged=None):
    return piles.check_findings(piles.Ctx(piles.load_tree(tree, tolerant=True), tree, staged, "HEAD"))


def new_finding(tree, name=NEW, pile="forge", extra="", ident="—"):
    put(tree, "plans/piles/%s/findings/%s" % (pile, name), finding_text(ident, pile) + extra)


def row(text):
    """A node row of «Узлы» whose «Что» carries `text`: from D-0044 on a finding is PLACED by a row (a node row, a row of «Остатки» /
    «Живые доказательства», a «перенос:» line of «Остатки»), never by the prose of «Ход» (t-866, F6-11)."""
    return "| F0-9 | П1 | %s | builder | `tools/a.py` | — | ожидает |" % text


def name_in(tree, text, rel=B1):
    """`text` (raw lines: use `row(...)`) at the end of the «Узлы» section, right after the last node row."""
    edit(tree, rel, "\n\n## Ход", "\n" + text + "\n\n## Ход")


def second_pile_batch(tree, text="", status="ожидает"):
    nodes = [node("R1-1")] + ([["R1-2", "П1", text, "builder", "`tools/a.py`", "—", "ожидает"]] if text else [])
    put(tree, "plans/piles/report-delivery/batch-1-x.md", batch_text("report-delivery", 1, status, nodes, who="—", branch="—"))


def test_e_negative_control_an_orphan_dated_from_d0044_is_red_and_a_row_clears_it(tree):
    new_finding(tree)
    res = run_e(tree)
    assert len(res.reds) == 1 and NEW_REL in res.reds[0].msg and "pile forge" in res.reds[0].msg and "2026-10-14" in res.reds[0].msg
    assert NEW_REL in res.reds[0].carriers and B1 in res.reds[0].carriers
    name_in(tree, row("`%s` -- узел F0-1" % NEW))
    res = run_e(tree)
    assert res.reds == [] and "0 dated from 2026-10-13 on are orphans" in res.ok


@pytest.mark.parametrize("mention", [NEW, "`%s`" % NEW, "`findings/%s`" % NEW, "plans/piles/forge/findings/%s" % NEW,
                                     "[x](findings/%s)" % NEW, "see %s." % NEW])
def test_e_a_name_with_or_without_the_findings_prefix_inside_backticks_or_not_places_it(tree, mention):
    new_finding(tree)
    name_in(tree, row(mention))
    assert run_e(tree).reds == []


@pytest.mark.parametrize("mention", ["a" + NEW, "x-" + NEW, "20261014-novoe", NEW[:-3] + "mdx"])
def test_e_a_longer_or_partial_name_does_not_place_it(tree, mention):
    new_finding(tree)
    name_in(tree, row(mention))
    assert len(run_e(tree).reds) == 1


@pytest.mark.parametrize("body", [
    "```\n%s\n```" % row(NEW),                          # a fenced block shows an example, it places nothing
    "~~~\n%s\n~~~" % row(NEW),
    "<!-- %s -->" % row(NEW),                           # the template's «Остатки» comment shows a form
    "<!--\nпервая\n%s\n-->" % row(NEW),
    "<!-- never closed\n%s" % row(NEW),                 # an unclosed comment hides the rest of the file: no false "placed"
])
def test_e_a_name_in_a_fence_or_a_comment_is_not_a_name(tree, body):
    new_finding(tree)
    name_in(tree, body)
    assert len(run_e(tree).reds) == 1


def test_e_text_before_an_unclosed_comment_and_after_a_closed_one_still_counts(tree):
    new_finding(tree)
    name_in(tree, "<!-- c -->\n%s\n<!-- never closed" % row(NEW))
    assert run_e(tree).reds == []


@pytest.mark.parametrize("name,header,red", [
    ("20261013-x.md", "x", True),                       # the day of D-0044 itself: red
    ("20261014-x.md", "x", True),
    ("20261012-x.md", "x", False),                      # the day before: the baseline
    ("B-102-x.md", "13.10", True),                      # no date in the name: the header's DD.MM, the freeze year
    ("B-102-x.md", "12.10", False),
    ("B-102-x.md", "x", False),                         # undated: it cannot be scoped, so it is the baseline, not a red
])
def test_e_the_date_scope_at_the_boundary(tree, name, header, red):
    put(tree, FDIR + name, with_header(header, "—"))
    res = run_e(tree)
    assert (len(res.reds) == 1) is red, res.reds
    assert (len(res.notes) == 0) is red and (red or "1 finding(s) dated before 2026-10-13" in res.notes[0])


def test_e_the_baseline_is_one_warn_line_with_the_count_and_the_first_five_names(tree):
    for n in range(7):
        put(tree, FDIR + "2026100%d-old.md" % (n + 1), finding_text("—"))
    res = run_e(tree)
    assert res.reds == [] and len(res.notes) == 1
    note = res.notes[0]
    assert note.startswith("WARN: 7 finding(s) dated before 2026-10-13") and note.count(".md") == 5
    assert "forge/20261001-old.md" in note and "forge/20261005-old.md" in note and "20261006-old.md" not in note


BYID = "20261014-byid.md"


def test_e_a_finding_named_only_by_its_b_id_is_placed_and_without_the_id_it_is_an_orphan(tree):
    new_finding(tree, name=BYID, ident="B-373")
    assert len(run_e(tree).reds) == 1                                           # negative: no id in any batch, no name
    name_in(tree, row("B-373 -- остаток частичного члена, узел F0-1"))            # positive: the id stands in a node row
    assert run_e(tree).reds == []
    edit(tree, B1, "B-373 -- остаток", "остаток")                               # the id removed again -> an orphan again
    assert len(run_e(tree).reds) == 1


@pytest.mark.parametrize("body", [
    "```\n%s\n```" % row("B-373"),                     # the fence rule holds for ids too
    "<!-- %s -->" % row("B-373"),
    "<!-- never closed\n%s" % row("B-373"),
    row("B-3730 и B-37 и B-373-x и findings/B-373-x.md"),   # a longer id, a shorter one, an id inside a longer token: no false placement
])
def test_e_a_b_id_in_a_fence_a_comment_or_a_longer_token_places_nothing(tree, body):
    new_finding(tree, name=BYID, ident="B-373")
    name_in(tree, body)
    assert len(run_e(tree).reds) == 1


def test_e_a_b_id_places_in_the_pile_of_the_move_line_too_and_an_id_less_finding_is_not_placed_by_one(tree):
    new_finding(tree, name=BYID, ident="B-373", extra="\nперенос: report-delivery/…\n")
    second_pile_batch(tree, "B-373")
    assert run_e(tree).reds == []
    new_finding(tree, name="20261014-noid.md", ident="—")                       # no header id: nothing to match by id
    name_in(tree, row("B-373"))
    assert [r.msg for r in run_e(tree).reds if "20261014-noid.md" in r.msg]


def test_e_a_finding_named_in_a_batch_of_another_pile_is_still_an_orphan_of_its_own(tree):
    new_finding(tree)
    second_pile_batch(tree, "`%s`" % NEW)
    res = run_e(tree)
    assert len(res.reds) == 1 and "pile forge" in res.reds[0].msg
    assert "report-delivery names it" in res.reds[0].msg and "перенос: report-delivery/…" in res.reds[0].msg


@pytest.mark.parametrize("line", ["перенос: report-delivery/…", "  перенос: report-delivery/findings/x.md", "перенос: `report-delivery/…`"])
def test_e_a_move_line_places_it_when_the_other_pile_names_it(tree, line):
    new_finding(tree, extra="\n" + line + "\n")
    assert len(run_e(tree).reds) == 1                                           # the move line alone is not enough ...
    second_pile_batch(tree, "`%s`" % NEW)                                       # ... the target pile must name the file too
    assert run_e(tree).reds == []


def test_e_a_move_to_a_pile_that_does_not_exist_or_does_not_name_it_is_red_with_the_slug(tree):
    new_finding(tree, extra="\nперенос: no-such-pile/…\n")
    res = run_e(tree)
    assert len(res.reds) == 1 and 'names the pile "no-such-pile", which does not exist' in res.reds[0].msg
    new_finding(tree, extra="\nперенос: report-delivery/…\n")
    second_pile_batch(tree, "ничего")
    res = run_e(tree)
    assert len(res.reds) == 1 and "«перенос: report-delivery/…» line is not backed" in res.reds[0].msg


def test_e_a_move_line_inside_a_fence_of_the_finding_is_not_a_move(tree):
    new_finding(tree, extra="\n```\nперенос: report-delivery/…\n```\n")
    second_pile_batch(tree, "`%s`" % NEW)
    assert len(run_e(tree).reds) == 1


def test_e_an_untaken_batch_in_status_ozhidaet_is_a_carrier(tree):
    new_finding(tree)
    put(tree, "plans/piles/forge/batch-2-next.md",
        batch_text("forge", 2, "ожидает", [node("F0-3", status="ожидает"), ["F0-4", "П1", "`%s`" % NEW, "builder", "`tools/a.py`", "—", "ожидает"]],
                   who="—", branch="—"))
    assert run_e(tree).reds == []


# ---------------------------------------------------------------- (е) is placed by a ROW, not by prose (t-866, F6-11; F4 of critic t-770)

def in_hod(tree, text, rel=B1):
    edit(tree, rel, "## Ход\n\n- x", "## Ход\n\n- x\n" + text)


def in_section(tree, heading, text, rel=B1):
    edit(tree, rel, "## %s\n" % heading, "## %s\n\n%s\n" % (heading, text))


def test_e_f4_a_name_only_in_the_prose_of_hod_is_an_orphan_and_the_same_name_in_a_node_row_places_it(tree):
    new_finding(tree)
    in_hod(tree, "- 14.10 -- `%s` лежит файлом" % NEW)
    res = run_e(tree)
    assert len(res.reds) == 1 and "no ROW of a batch file" in res.reds[0].msg and "names it in prose" in res.reds[0].msg
    name_in(tree, row("`%s`" % NEW))
    assert run_e(tree).reds == []


def test_e_f4_the_prose_of_hod_still_places_a_finding_of_the_baseline(tree):
    put(tree, FDIR + "20261012-old.md", finding_text("—"))
    in_hod(tree, "- `20261012-old.md` назван в «Ходе»")
    res = run_e(tree)
    assert res.reds == [] and res.notes == []                                  # the file level is kept for findings before 2026-10-13
    put(tree, FDIR + "20261013-edge.md", finding_text("—"))
    in_hod(tree, "- `20261013-edge.md` назван в «Ходе»")
    assert len(run_e(tree).reds) == 1                                           # the day of D-0044 itself is already row-only


@pytest.mark.parametrize("where,line", [
    ("Остатки", "- что осталось | перенос: findings/%s | обоснование: x | подтвердил: Dev1, 15.10" % NEW),    # a pointer row
    ("Остатки", "  | что осталось | перенос: findings/%s |" % NEW),                                           # an indented table row
    ("Остатки", "- `%s` сделана внутри взятой пачки | сделано: t-778" % NEW),     # work done inside a taken batch: «Остатки» is its one writable list
    ("Остатки", "- `%s` ждёт узла | узел: F0-2" % NEW),                            # F6-30 K15: a `узел:` segment is a key, like `сделано:`
    ("Остатки", "узел: F0-2 `%s`" % NEW),                                            # ... first on the line too
    ("Живые доказательства", "  | %s | стенд | кто | ждёт |" % NEW),                  # the F5-5 leftover: a row with leading spaces IS a row
    ("Живые доказательства", "| %s | стенд | кто | ждёт |" % NEW),
    ("Узлы", "   " + row("`%s`" % NEW)),
])
def test_e_f4_a_pointer_row_an_indented_row_and_rows_of_the_other_tables_place_it(tree, where, line):
    new_finding(tree)
    in_section(tree, where, line)
    assert run_e(tree).reds == []


@pytest.mark.parametrize("where,line", [
    ("Остатки", "- `%s` назван в строке без ключа `перенос:`" % NEW),             # a list item of «Остатки» is a row only with the key
    ("Ход", "| 14.10 | `%s` |" % NEW),                                          # a table inside «Ход» is prose, not a placement row
    ("Ход", "перенос: findings/%s" % NEW),                                      # the key outside «Остатки» is prose too
    ("Ход", "- `%s` | сделано: t-778" % NEW),                                   # ... and so is «сделано:» in «Ход»
    ("Остатки", "- `%s` ждёт, потому что узел: F0-2 ещё не взят" % NEW),         # F6-30 K15: `узел:` in the middle of a sentence is no key
    ("Ход", "- `%s` | узел: F0-2" % NEW),                                       # ... and not in «Ход» either
])
def test_e_f4_a_line_that_is_not_a_row_places_nothing(tree, where, line):
    new_finding(tree)
    in_section(tree, where, line)
    assert len(run_e(tree).reds) == 1


def test_e_f4_a_batch_without_the_sections_has_no_rows_and_a_renamed_finding_is_an_orphan_under_the_new_name(tree):
    new_finding(tree)
    put(tree, B1, "# forge — пачка 1\n\nкучка: `forge` | статус: в работе | взял: Ира\n\n| %s | x |\n" % NEW)     # no «Узлы» at all
    assert len(run_e(tree).reds) == 1
    put(tree, B1, batch_text("forge", 1, nodes=[node("F0-1")]))
    name_in(tree, row("`20261014-staroe.md`"))                                  # the row names the OLD file name
    assert len(run_e(tree).reds) == 1 and NEW in run_e(tree).reds[0].msg


# ---------------------------------------------------------------- (е) at commit time: a deleted batch file carries its red (F3 of critic t-770)

@needs_git
def test_e_f3_a_git_rm_of_the_only_batch_that_named_a_finding_is_a_red_of_that_commit_not_a_carried_one(tree, cli):
    new_finding(tree)
    B2 = "plans/piles/forge/batch-2-next.md"
    put(tree, B2, batch_text("forge", 2, "ожидает", [node("F0-3", status="ожидает"), ["F0-4", "П1", "`%s`" % NEW, "builder", "`tools/a.py`", "—", "ожидает"]],
                             who="—", branch="—"))
    commit(tree, "the finding and the batch row that places it")
    (tree / B2).unlink()
    stage(tree, B2)
    code, out = cli(tree, "check")
    e_lines = [ln for ln in out.splitlines() if ln.startswith("(е)")]
    assert any("(е) findings: RED" in ln and NEW_REL in ln for ln in e_lines), out
    assert not any("carried" in ln for ln in e_lines), out
    assert code == 2 and "red: " in out and "(е)" in out.splitlines()[-1], out


def test_e_an_unreadable_finding_is_not_reported_twice(tree):
    bad_finding(tree)
    res = run_e(tree)
    assert res.reds == [] and res.notes == [] and "0 findings read" in res.ok         # (д) names it, (е) does not


@needs_git
def test_e_the_cli_names_the_orphan_and_the_door_passes_it(tree, cli):
    new_finding(tree)
    code, out = cli(tree, "check", "--all")
    assert code == 2 and "(е) findings: RED" in out and NEW_REL in out and "refused -- red: (е)" in out
    for word in ("е", "e", "findings"):
        code, out = cli(tree, "check", "--all", "--msg-file", msg(tree, "s\n\npiles-skip: %s -- placed in the next commit\n" % word))
        assert code == 0 and "(е) findings: RED, passed by the commit message" in out, word
    assert cli(tree, "check", "--all", "--msg-file", msg(tree, "s\n\npiles-skip: д -- wrong item\n"))[0] == 2


@needs_git
def test_e_runs_in_a_commit_only_when_a_finding_or_a_batch_file_is_staged(tree, cli):
    new_finding(tree)
    commit(tree, "an orphan, committed through a door")
    edit(tree, "plans/piles/forge/README.md", "Текст.", "Текст. Ещё.")
    stage(tree, "plans/piles/forge/README.md")
    code, out = cli(tree, "check")
    assert code == 0 and "(е) findings: no finding or batch file staged -- not checked" in out, out
    edit(tree, B1, "- x\n", "- x\n- правка\n")                                 # a batch of the finding's own pile: its carrier
    stage(tree, B1)
    code, out = cli(tree, "check")
    assert code == 2 and "(е) findings: RED" in out and NEW_REL in out, out
    commit(tree, "x")
    second_pile_batch(tree)                                                    # a batch of another pile: the red is only carried
    stage(tree, "plans/piles/report-delivery/batch-1-x.md")
    code, out = cli(tree, "check")                                             # (д) is red here (the fixture has no card row): not (е)'s business
    assert "(е) findings: 1 red(s) in piles this commit does not touch (not blocking): forge" in out and "(е) findings: RED" not in out, out
    assert "red: (д)" in out and "(е)" not in out.splitlines()[-1], out


# ---------------------------------------------------------------- t-870 F-5: a finding or a batch file with a fence nothing closes halts every path, naming file:line

UNCLOSED_REL = FDIR + "20261014-fence.md"


def unclosed_finding(tree):
    """A finding dated from FINDINGS_FROM whose last lines open a fence nothing closes; -> the 1-based line of the opener."""
    text = finding_text("—") + "\n```\nперенос: other/x\n"
    put(tree, UNCLOSED_REL, text)
    return text.split("\n").index("```") + 1


@needs_git
def test_the_commit_msg_path_check_msg_file_refuses_a_staged_finding_with_an_unclosed_fence_naming_file_and_line(tree, cli, capsys):
    line = unclosed_finding(tree)
    stage(tree, UNCLOSED_REL)
    capsys.readouterr()
    code, out = cli(tree, "check", "--msg-file", msg(tree, "s\n\nan ordinary message\n"))
    text = out + capsys.readouterr().err
    assert code == 1 and "%s:%d:" % (UNCLOSED_REL, line) in text and "never closed" in text and "add it and run again" in text, text


@needs_git
def test_take_refuses_when_a_finding_has_an_unclosed_fence_names_file_and_line_and_writes_nothing(tree, cli, capsys):
    from piles_testkit import batch2, git
    batch2(tree)
    git(tree, "branch", "-M", "main")
    line = unclosed_finding(tree)
    snap = tree_state(tree)
    capsys.readouterr()
    code, out = cli(tree, "take", "forge", "2", "--who", "Dev1", "--today", "2026-10-08")
    text = out + capsys.readouterr().err
    assert code == 1 and "%s:%d:" % (UNCLOSED_REL, line) in text and "never closed" in text, text
    assert tree_state(tree) == snap


@needs_git
def test_close_refuses_when_a_finding_has_an_unclosed_fence_names_file_and_line_and_writes_nothing(tree, cli, capsys):
    accept_batch1(tree)
    line = unclosed_finding(tree)
    snap = tree_state(tree)
    capsys.readouterr()
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree))
    text = out + capsys.readouterr().err
    assert code == 1 and "%s:%d:" % (UNCLOSED_REL, line) in text and "never closed" in text, text
    assert tree_state(tree) == snap
