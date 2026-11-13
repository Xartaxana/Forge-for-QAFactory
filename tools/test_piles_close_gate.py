"""Tests for tools/piles.py: the carry-over gate of `close <slug> <N>`, the refused `release` alias, the all-or-nothing writes
(m-8) and the finding cell boundary of `close --id` (m-10). Run from the repo root: python -m pytest tools/test_piles_close_gate.py -q

The owner's word 08.10.2026: a batch is closed by finishing, not by carrying over. Every refusal leaves the tree byte for byte
as it was (tree_state = sha256 of every file under plans/).
"""
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import piles  # noqa: E402
from piles_testkit import (B1, B2, CARD, GIT_VARS, LEFTOVER_OK, accept_batch1, batch_text, closed_rows, commit,  # noqa: E402
                           edit, finding_text, freeze, git, head_hash, needs_git, node, put, rd, stage, tree_state)

REAL = pathlib.Path(__file__).resolve().parent.parent
CARRY = "перенос: %s | обоснование: нужен стенд | подтвердил: Dev1, 08.10"


@pytest.fixture(autouse=True)
def _scrub_git_env(monkeypatch):
    for k in GIT_VARS:
        monkeypatch.delenv(k, raising=False)


def with_leftovers(tree, *lines):
    """The accepted batch 1 whose «Остатки» holds exactly `lines`."""
    accept_batch1(tree)
    edit(tree, B1, LEFTOVER_OK, "\n".join(lines))


@needs_git
@pytest.mark.parametrize("line,needle", [
    ("- осталось дело", "has neither `сделано:` nor `перенос:`"),                       # mutation (a): a keyless line
    ("- дело | сделано: nonsense", "`сделано: nonsense` is neither 7-40 hex characters nor t-nnn"),
    ("- дело | сделано: abcdef", "neither 7-40 hex characters nor t-nnn"),              # six hex characters: one short
    ("- дело | сделано: T-5", "neither 7-40 hex characters nor t-nnn"),
    ("- дело | Сделано: T-5", "neither 7-40 hex characters nor t-nnn"),                 # the key is case-free (m3), the value is strict
    ("- дело | СДЕЛАНО: ABC1234", "`сделано: ABC1234` is neither"),                   # hex in lower case only, in both gates
    ("- дело | сделано: t-5 | перенос: пачка 2 | обоснование: р | подтвердил: М, 08.10", "carries both `сделано:` and `перенос:`"),
    ("- дело | перенос: пачка 2 | обоснование: р", "`подтвердил:` is missing"),
    ("- дело | перенос: пачка 2 | обоснование: р | подтвердил:", "`подтвердил:` is empty"),   # mutation (b): empty accepted
    ("- дело | перенос: пачка 2 | обоснование: р | подтвердил:   ", "`подтвердил:` is empty"),
    ("- дело | перенос: пачка 2 | подтвердил: М, 08.10", "`обоснование:` is missing"),
    ("- дело | перенос: пачка 2 | обоснование: | подтвердил: М, 08.10", "`обоснование:` is empty"),
    ("- дело | перенос: findings | обоснование: р | подтвердил: М, 08.10", "`перенос: findings` is none of"),
    ("- дело | перенос: пачка | обоснование: р | подтвердил: М, 08.10", "is none of findings/<file> | пачка N"),
    ("- дело | перенос: x | подтвердил: | обоснование:", "`подтвердил:` is empty"),
    # B-472 item 3: every non-empty line outside a comment is an item -- prose, a heading, a fence line (these params
    # moved here from the passing test: the old gate judged only top-level bullets)
    ("просто абзац без маркера", "has neither `сделано:` nor `перенос:`"),
    ("### подзаголовок", "has neither"),
    ("```", "has neither"),                                                              # a fence line is an item too
    ("* дело", "has neither"),
    ("• дело", "has neither"),
    ("1. дело", "has neither"),
    # t-618 F-1: a sub-bullet (an indented MARKER line) is an item of its own, and so is a tab-indented line, a 1-space line
    # and an indented line with nothing above it
    ("  - под-пункт без ключей", "has neither"),
    ("\tстрока с табуляцией", "has neither"),
    ("  отступ, а пункта выше нет", "has neither"),
    ("-->", "has neither"),                                                              # a stray `-->` is text, not a comment end
    ("<!-- a --> просто <!-- b -->", "has neither"),                                     # the text BETWEEN two comments is an item
])
def test_gate_refuses_a_line_that_is_neither_finished_nor_carried_with_a_person(tree, cli, line, needle):
    with_leftovers(tree, line)
    snap = tree_state(tree)
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree), "--today", "2026-10-08")
    assert code == 2 and needle in out, out
    assert "plans/piles/forge/batch-1-foundation.md" in out and "Nothing was written" in out
    assert "`сделано: <7-40 hex | t-nnn>`" in out and "`подтвердил: <кто, дата>`" in out        # both forms, verbatim
    assert "a PERSON" in out and tree_state(tree) == snap                                      # the door; sha256 unchanged


@needs_git
def test_gate_names_the_line_number_and_its_first_80_characters_and_lists_every_bad_line(tree, cli):
    long_line = "- " + "д" * 120
    with_leftovers(tree, "- ok | сделано: t-1", long_line, "- и ещё одна")
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree))
    shown = long_line[:80]
    assert code == 2 and (('"%s…"' % shown[:79]) in out or ('"%s"' % shown) in out), out
    assert "д" * 81 not in out and "и ещё одна" in out and out.count("has neither") == 2


@needs_git
@pytest.mark.parametrize("lines", [
    ("- дело | сделано: abcdef1",),                                                      # 7 hex: the shortest hash
    ("- дело | Сделано: abcdef1",),                                                      # t-787 m3: the KEY is case-free (the proofs gate reads it so too)
    ("- дело | ПЕРЕНОС: пачка 2 | Обоснование: р | Подтвердил: М, 08.10",),               # mixed-case keys inside the pairs
    ("- дело | сделано: " + "a1" * 20,),                                                # 40 hex: the longest
    ("- дело | сделано: t-596",),
    ("- сделано: t-596",),                                                              # the keys may come first
    ("- дело | " + CARRY % "пачка 2",),                                                  # card row 2 of the fixture is "ожидает"
    ("- `a | b` дело | сделано: t-1",),                                                 # a pipe inside backticks is no separator
    ("- дело | сделано: t-1", "  продолжение строки без ключей"),                        # t-618 F-1: 2+ spaces = one more segment
    ("- дело", "  сделано: t-1"),                                                       # the keys may stand on the continuation line
    ("- дело | перенос: пачка 2 | обоснование: нужен стенд", "  подтвердил: Dev1, 08.10"),   # a wrapped carry is one item
    ("- дело | сделано: t-1", "", "- и ещё | сделано: t-2"),                            # a blank line is no item
    ("<!-- - спрятано | в комментарии -->", "- дело | сделано: t-1"),                    # a comment holds no items
    ("<!-- a --><!-- b -->", "- дело | сделано: t-1"),                                  # nothing between two comments is no item
    (),                                                                                 # an empty section
])
def test_gate_passes_a_finished_or_person_confirmed_carry_over_and_empty_sections(tree, cli, lines):
    with_leftovers(tree, *lines)
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree), "--today", "2026-10-08")
    assert code == 0 and "forge/1 closed" in out, out
    assert rd(tree, B1).count("статус: закрыта") == 1


def run_close(tree, cli):
    return cli(tree, "close", "forge", "1", "--hash", head_hash(tree), "--today", "2026-10-08")


def carry_line(target):
    return "- дело | " + CARRY % target


X = "plans/piles/forge/findings/x.md"


def put_staged(tree, rel=X):
    """A carry-over target as the close's own commit may hold it: on disk AND in the index."""
    put(tree, rel, finding_text("—"))
    stage(tree, rel)


# ---------------------------------------------------------------- t-618 F-1: continuation boundaries (1 space / 2 spaces / tab)

@needs_git
@pytest.mark.parametrize("lines,passes", [
    (("- дело | сделано: t-1", "  продолжение"), True),                    # 2 spaces: one more ' | ' segment of the item above
    (("- дело | сделано: t-1", "   три пробела", "  два пробела"), True),    # 3 and 2 spaces: both continue
    (("- дело | сделано: t-1", " один пробел"), False),                    # 1 space: an item of its own, no keys
    (("- дело | сделано: t-1", "\tтабуляция"), False),                      # a tab: an item of its own
    (("- дело | сделано: t-1", "  - под-пункт"), False),                   # an indented marker: an item of its own
    (("- дело", "  - под-пункт | сделано: t-2"), False),                   # ... and the parent keeps its own (empty) keys
    (("- дело | сделано: t-1", "  - под-пункт", "  сделано: t-2"), True),   # the continuation joins the NEAREST item above it
    (("- дело | сделано: t-1", "", "  продолжение после пустой строки"), True),   # a blank line does not end the item
    (("  начало без пункта выше", "  сделано: t-1"), True),                # an indented line with no item above is an item; the next joins it
])
def test_gate_continuation_boundaries_one_space_two_spaces_and_a_tab(tree, cli, lines, passes):
    with_leftovers(tree, *lines)
    code, out = run_close(tree, cli)
    if passes:
        assert code == 0 and "forge/1 closed" in out, out
    else:
        assert code == 2 and "has neither" in out and "Nothing was written" in out, out


def test_leftover_items_joins_a_continuation_and_keeps_the_line_numbers_of_the_items():
    text = "# t\n\n## Остатки\n\n- a\n  b\n  - c\n d\n<!-- x\ny -->\n\ne\n"
    assert piles.leftover_items(text) == ([(5, "- a | b"), (7, "- c"), (8, "d"), (12, "e")], None)
    assert piles.leftover_items("## Остатки\n\n<!-- ok -->\n") == ([], None)


# ---------------------------------------------------------------- t-618 F-2: the section is found on the raw `## ` line

@needs_git
def test_a_fence_in_hod_cannot_hide_the_ostatki_heading(tree, cli):
    with_leftovers(tree, "- без ключей")
    edit(tree, B1, "## Ход\n\n- x", "## Ход\n\n```\n- x")                                  # an unclosed fence above the section
    snap = tree_state(tree)
    code, out = run_close(tree, cli)
    assert code == 2 and "«Остатки» is not finished" in out and "- без ключей" in out and tree_state(tree) == snap, out


@needs_git
def test_an_inline_comment_opener_in_hod_cannot_hide_the_ostatki_heading(tree, cli):
    with_leftovers(tree, "- без ключей", "<!-- конец -->")                                 # the old regex paired `<!--` below with this `-->`
    edit(tree, B1, "## Ход\n\n- x", "## Ход\n\n- x `<!--` пример")
    code, out = run_close(tree, cli)
    assert code == 2 and "«Остатки» is not finished" in out and "- без ключей" in out, out


@needs_git
def test_a_comment_around_the_heading_no_longer_hides_the_section(tree, cli):
    with_leftovers(tree, "- x | сделано: t-1", "-->")
    edit(tree, B1, "## Остатки", "<!--\n## Остатки")
    code, out = run_close(tree, cli)
    assert code == 2 and 'line' in out and '"-->": has neither' in out, out                # the stray `-->` is an item without keys


@needs_git
def test_an_unclosed_comment_in_ostatki_is_refused_with_its_line_number(tree, cli):
    with_leftovers(tree, "- дело | сделано: t-1", "<!-- забыли закрыть", "- дело | сделано: t-2")
    lineno = rd(tree, B1).split("\n").index("<!-- забыли закрыть") + 1
    snap = tree_state(tree)
    code, out = run_close(tree, cli)
    assert code == 2 and ('line %d: "<!--" opens a comment that never closes' % lineno) in out, out
    assert 'close it with "-->"' in out and "Nothing was written" in out and tree_state(tree) == snap


@needs_git
def test_the_gate_names_five_bad_lines_and_counts_the_rest(tree, cli):
    six = ["- дело-%d" % i for i in range(1, 7)]
    with_leftovers(tree, *six)
    code, out = run_close(tree, cli)
    assert code == 2 and "дело-5" in out and "дело-6" not in out and "and 1 more" in out, out
    edit(tree, B1, "\n".join(six), "\n".join(six[:5]))                                      # exactly 5: all named, no "and … more"
    code, out = run_close(tree, cli)
    assert code == 2 and "дело-5" in out and "more" not in out, out


@needs_git
def test_a_form_error_and_a_missing_target_are_listed_together(tree, cli):
    with_leftovers(tree, "- без ключей", carry_line("findings/missing.md"))
    code, out = run_close(tree, cli)
    assert code == 2 and "has neither" in out and "`перенос: findings/missing.md` names plans/piles/forge/findings/missing.md" in out, out


def test_check_leftovers_judges_only_the_form_without_a_root():
    text = "## Остатки\n\n" + carry_line("findings/nowhere.md") + "\n"
    piles.check_leftovers(text, "b.md")                                                     # two positional arguments: no existence check


# ---------------------------------------------------------------- Q6/Q7: the carry-over target must exist

@needs_git
def test_a_file_target_on_disk_but_not_staged_is_refused_with_the_git_add_door(tree, cli):
    with_leftovers(tree, carry_line("findings/x.md"))
    put(tree, X, finding_text("—"))                                                         # on disk only
    snap = tree_state(tree)
    code, out = run_close(tree, cli)
    assert code == 2 and "exists but is not staged -- `git add %s`" % X in out and "then run close again" in out, out
    assert "Nothing was written" in out and tree_state(tree) == snap


@needs_git
def test_a_file_target_that_is_staged_passes_and_so_does_one_in_backticks(tree, cli):
    with_leftovers(tree, "- дело | " + CARRY % "`findings/x.md`")
    put_staged(tree)
    code, out = run_close(tree, cli)
    assert code == 0 and "forge/1 closed" in out, out


@needs_git
def test_a_file_target_that_was_staged_and_is_gone_from_the_disk_is_refused(tree, cli):
    with_leftovers(tree, carry_line("findings/x.md"))
    put_staged(tree)
    (tree / X).unlink()                                                                     # staged, deleted in the working tree
    code, out = run_close(tree, cli)
    assert code == 2 and ("`перенос: findings/x.md` names %s, which is not in the working tree" % X) in out, out
    put_staged(tree)
    git(tree, "rm", "-q", "-f", "--", X)                                                    # `git rm`: gone from both
    code, out = run_close(tree, cli)
    assert code == 2 and "which is not in the working tree" in out, out


@needs_git
def test_a_file_target_is_matched_case_exactly(tree, cli):
    with_leftovers(tree, carry_line("findings/X.md"))
    put_staged(tree)                                                                        # x.md exists, X.md does not
    code, out = run_close(tree, cli)
    assert code == 2 and "plans/piles/forge/findings/X.md, which is not in the working tree" in out, out


@needs_git
def test_a_target_in_another_pile_needs_that_pile_and_its_file(tree, cli):
    other = "plans/piles/report-delivery/findings/x.md"
    with_leftovers(tree, carry_line("nopile/findings/x.md"))
    code, out = run_close(tree, cli)
    assert code == 2 and 'names pile "nopile", which has no plans/piles/nopile/' in out, out
    edit(tree, B1, "nopile/findings/x.md", "report-delivery/findings/x.md")
    code, out = run_close(tree, cli)
    assert code == 2 and ("names %s, which is not in the working tree" % other) in out, out
    put_staged(tree, other)
    code, out = run_close(tree, cli)
    assert code == 0 and "forge/1 closed" in out, out


@needs_git
@pytest.mark.parametrize("target,needle", [
    ("пачка 0", "has no row 0 in plans/piles/forge/README.md"),
    ("пачка 3", "has no row 3 in plans/piles/forge/README.md"),
    ("пачка 007", "has no row 7 in plans/piles/forge/README.md"),                          # the digits are a number, not a text
    ("пачка 1", "names this very batch"),
    ("пачка 1000", "`перенос: пачка 1000` is none of"),                                   # beyond the form: three digits at most
    ("findings/x.md#a", "`перенос: findings/x.md#a` is none of"),                         # an anchor: a form refusal, as before
    ("`findings/x.md` (ст. 2)", "is none of"),
])
def test_a_batch_target_must_be_a_card_row_of_this_pile_other_than_this_batch(tree, cli, target, needle):
    with_leftovers(tree, carry_line(target))
    snap = tree_state(tree)
    code, out = run_close(tree, cli)
    assert code == 2 and needle in out and "Nothing was written" in out and tree_state(tree) == snap, out


@needs_git
def test_batch_999_with_a_card_row_is_a_legal_target(tree, cli):
    with_leftovers(tree, carry_line("пачка 999"))
    edit(tree, CARD, "| M | ожидает | — | — | — |", "| M | ожидает | — | — | — |\n| 999 | далеко | B-102 | M | ожидает | — | — | — |")
    code, out = run_close(tree, cli)
    assert code == 0 and "forge/1 closed" in out, out


@needs_git
def test_a_closed_batch_is_not_a_carry_over_target(tree, cli):
    with_leftovers(tree, carry_line("пачка 2"))
    edit(tree, CARD, "| M | ожидает |", "| M | закрыта |")
    code, out = run_close(tree, cli)
    assert code == 2 and "names batch 2, which is закрыта -- carry to a batch still open" in out, out


@needs_git
def test_a_finding_this_close_deletes_is_not_a_carry_over_target(tree, cli):
    deleted = "plans/piles/forge/findings/B-230-opisanie.md"
    put(tree, deleted, finding_text("B-230"))
    stage(tree, deleted)                                                                    # staged and on disk, yet the close removes it
    with_leftovers(tree, carry_line("findings/B-230-opisanie.md"))
    code, out = run_close(tree, cli)
    assert code == 2 and "names a finding this close deletes (B-230 is a whole member of forge/1) -- carry elsewhere" in out, out


@needs_git
@pytest.mark.parametrize("n,whole", [(30, True), (31, False)])
def test_a_target_value_is_printed_whole_up_to_30_characters_and_cut_beyond(tree, cli, n, whole):
    target = "findings/" + "a" * (n - len("findings/.md")) + ".md"
    assert len(target) == n
    with_leftovers(tree, carry_line(target))
    code, out = run_close(tree, cli)
    assert code == 2, out
    assert (("`перенос: %s` names" % target) in out) == whole and (target[:29] + "…" in out) == (not whole), out
    assert "plans/piles/forge/%s" % target in out                                           # the resolved path is always whole


@needs_git
def test_the_index_is_listed_by_one_call_and_only_when_a_file_target_is_there(tree, cli, monkeypatch):
    calls = []
    real = piles.git

    def counting(root, *args, **kw):
        calls.append(args)
        return real(root, *args, **kw)
    monkeypatch.setattr(piles, "git", counting)
    other = "plans/piles/report-delivery/findings/x.md"
    with_leftovers(tree, carry_line("findings/x.md"), carry_line("report-delivery/findings/x.md"), carry_line("пачка 2"))
    put_staged(tree)
    put_staged(tree, other)
    code, out = run_close(tree, cli)
    assert code == 0, out
    listing = [a for a in calls if a[0] == "ls-files"]
    assert listing == [("ls-files", "-z", "--cached", "--", "plans/piles")], calls


@needs_git
def test_no_index_is_listed_when_the_only_target_is_a_batch(tree, cli, monkeypatch):
    calls = []
    real = piles.git
    monkeypatch.setattr(piles, "git", lambda root, *a, **kw: (calls.append(a), real(root, *a, **kw))[1])
    with_leftovers(tree, carry_line("пачка 2"))
    assert run_close(tree, cli)[0] == 0
    assert not [a for a in calls if a[0] == "ls-files"], calls


@needs_git
def test_a_failing_index_listing_is_cannot_run_and_writes_nothing(tree, cli, monkeypatch):
    real = piles.git
    monkeypatch.setattr(piles, "git", lambda root, *a, **kw: (128, b"fatal: boom") if a[0] == "ls-files" else real(root, *a, **kw))
    with_leftovers(tree, carry_line("findings/x.md"))
    put_staged(tree)
    snap = tree_state(tree)
    code, out = run_close(tree, cli)
    assert code == 1 and "cannot list the index to verify the carry-over targets (fatal: boom)" in out, out
    assert "run close inside the repository; nothing was written" in out and tree_state(tree) == snap


def test_piles_index_outside_a_repository_is_cannot_run(tree, tmp_path, monkeypatch):
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))                            # git may not climb out of the copy
    with pytest.raises(piles.CannotRun, match="cannot list the index to verify the carry-over targets"):
        piles.piles_index(tree)


@needs_git
def test_piles_index_lists_the_staged_paths_under_plans_piles(tree):
    put_staged(tree)
    index = piles.piles_index(tree)
    assert X in index and "plans/piles/forge/README.md" in index and "plans/BACKLOG.md" not in index


@needs_git
def test_gate_passes_a_batch_file_without_an_ostatki_heading(tree, cli):
    accept_batch1(tree)
    edit(tree, B1, "## Остатки", "## Другое")
    assert cli(tree, "close", "forge", "1", "--hash", head_hash(tree), "--today", "2026-10-08")[0] == 0


@needs_git
def test_gate_does_not_block_an_already_closed_batch(tree, cli):
    accept_batch1(tree)
    h = head_hash(tree)
    assert cli(tree, "close", "forge", "1", "--hash", h, "--today", "2026-10-08")[0] == 0
    edit(tree, B1, LEFTOVER_OK, "- поздняя строка без ключей")                            # a closed batch's Остатки is history
    snap = tree_state(tree)
    code, out = cli(tree, "close", "forge", "1", "--hash", h)
    assert code == 0 and "already closed" in out and tree_state(tree) == snap


@needs_git
def test_gate_comes_after_the_status_checks_and_before_the_plan(tree, cli):
    edit(tree, B1, LEFTOVER_OK, "- без ключей")
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree))              # not yet принято: the status is named first
    assert code == 2 and 'expected status "принято"' in out and "Остатки" not in out
    accept_batch1(tree)
    edit(tree, "plans/piles/forge/README.md", "B-230 | L", "B-230, B-999 | L")             # an unknown member as well as a bad line
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree))
    assert code == 2 and "«Остатки» is not finished" in out and "B-999" not in out


def test_real_batch_files_are_readable_by_the_gate():
    for path in sorted((REAL / "plans/piles").glob("*/batch-*.md")):
        piles.check_leftovers("", path.name)                                             # no section: passes
        piles.leftover_items(piles.read_text(path))                                      # and the real section parses
    template = piles.read_text(REAL / "plans/piles/_template/batch.md")
    assert piles.leftover_items(template) == ([], None)                                  # the template's comment holds the two forms only
    assert "сделано:" in template and "перенос:" in template and "подтвердил:" in template


def test_real_batch_files_are_readable_by_the_proofs_gate_and_the_template_closes_freely():
    for path in sorted((REAL / "plans/piles").glob("*/batch-*.md")):
        assert isinstance(piles.proof_problems(piles.read_text(path)), list), path               # F5-5: every real file parses
    template = piles.read_text(REAL / "plans/piles/_template/batch.md")
    assert piles.proof_problems(template) == []                    # a header-only table; the comment's example pairs are no rows
    assert "`ждёт`" in template and "`\\|`" in template and "сделано: <хэш 7-40 hex | t-nnn | путь" in template


# ---------------------------------------------------------------- the refused alias

@needs_git
def test_release_is_a_refused_alias_that_runs_nothing(tree, cli):
    accept_batch1(tree)
    snap = tree_state(tree)
    h = head_hash(tree)
    code0, out0 = cli(tree, "release")
    code1, out1 = cli(tree, "release", "forge", "1", "--hash", h, "--url", "https://x/y", "--today", "2026-10-08")
    code2, out2 = cli(tree, "release", "--id", "B-102", "--word", "w", "--bogus")
    assert (code0, code1, code2) == (1, 1, 1) and out0 == out1 == out2, (out0, out1)
    assert "`release` was renamed `close`" in out0 and "expected `close` with the same arguments" in out0
    assert "close <slug> <N> --hash <h>" in out0 and "close --id B-nnn --word" in out0
    assert tree_state(tree) == snap and "статус: принято" in rd(tree, B1) and "B-230" not in closed_rows(tree)   # mutation (c): nothing ran


# ---------------------------------------------------------------- m-8: all or nothing

class Boom(OSError):
    pass


@needs_git
def test_close_batch_that_fails_midway_puts_every_file_back(tree, cli, monkeypatch):
    put(tree, "plans/piles/forge/findings/B-230-opisanie.md", finding_text("B-230"))     # a finding the close deletes
    accept_batch1(tree)
    snap = tree_state(tree)
    h = head_hash(tree)
    real_write, calls = piles.write_like, []

    def failing_write(path, text, form):
        calls.append(path)
        if len(calls) == 3:                                                              # the BACKLOG and the card are already written
            raise Boom("disk full")
        return real_write(path, text, form)

    monkeypatch.setattr(piles, "write_like", failing_write)
    code, out = cli(tree, "close", "forge", "1", "--hash", h, "--today", "2026-10-08")
    assert code == 1 and "every file touched was put back, nothing changed" in out and "Boom" in out, out
    assert tree_state(tree) == snap and (tree / "plans/piles/forge/findings/B-230-opisanie.md").exists()


@needs_git
def test_close_id_that_fails_midway_puts_the_row_and_the_finding_back(tree, cli, monkeypatch):
    freeze(tree)
    snap = tree_state(tree)

    real_unlink = pathlib.Path.unlink

    def failing_unlink(self, missing_ok=False):                                          # `close --id` writes ONE file (the BACKLOG)
        real_unlink(self, missing_ok=missing_ok)                                         # and deletes the finding: fail after the delete
        if self.name.startswith("B-102"):
            raise Boom("unlink broke")
    monkeypatch.setattr(pathlib.Path, "unlink", failing_unlink)
    code, out = cli(tree, "close", "--id", "B-102", "--word", "w", "--today", "2026-10-08")
    assert code == 1 and "nothing changed" in out and tree_state(tree) == snap
    assert list((tree / "plans/piles/forge/findings").glob("B-102*"))


# ---------------------------------------------------------------- m-10: the cell boundary

@needs_git
def test_close_id_does_not_glue_the_partial_member_note_into_the_principles_cell(tree, cli):
    body = ("# Находка\n\nid: B-102 | кучка: `forge` | от: x | приоритет: — | кандидат наверх: нет\n\n"
            "Что не так / что сделать: суть\n\nСвидетель: прогон 7\n\nПринципы и правила: P1, FR-2\n\n"
            "Член пачки `forge/1` частично: (хвост) -- остаток строки лежит в этой находке.\n\n"
            "Решение владельца нужно: нет\n")
    put(tree, "plans/piles/forge/findings/B-102-x.md", body)
    assert cli(tree, "close", "--id", "B-102", "--word", "w", "--today", "2026-10-08")[0] == 0
    row = closed_rows(tree)["B-102"]
    assert row.endswith("| P1, FR-2 |") and "Член пачки" not in row and len(piles.split_cells(row)) == 5


# ---- the placeholder words (t-601, item 1 of finding 20261009-gate-perenosa-forki) ----

EMPTY_WORDS = ("—", "–", "-", "n/a", "none", "нет", "tbd", "?")


def carried(**over):
    pairs = {"перенос": "пачка 2", "обоснование": "нужен стенд", "подтвердил": "Dev1, 08.10"}
    pairs.update(over)
    return pairs


def test_the_placeholder_words_are_data_and_are_exactly_the_agreed_tuple():
    assert piles.LEFTOVER_EMPTY_WORDS == EMPTY_WORDS and isinstance(piles.LEFTOVER_EMPTY_WORDS, tuple)


@pytest.mark.parametrize("key", ["подтвердил", "обоснование"])
@pytest.mark.parametrize("word", EMPTY_WORDS)
def test_a_placeholder_word_is_empty_for_both_keys_and_the_refusal_names_it(key, word):
    why = piles.leftover_problem(carried(**{key: word}))
    assert why and "`%s: %s`" % (key, word) in why and "placeholder" in why, why
    padded = piles.leftover_problem(carried(**{key: "  %s  " % word}))              # padded with blanks: still empty
    assert padded and "placeholder" in padded, padded


@pytest.mark.parametrize("key", ["подтвердил", "обоснование"])
@pytest.mark.parametrize("word", ["N/A", "None", "TBD", "НЕТ", "Нет", "nOnE"])
def test_a_placeholder_word_is_matched_in_lower_case_whatever_its_case(key, word):
    why = piles.leftover_problem(carried(**{key: word}))
    assert why and "`%s: %s`" % (key, word) in why, why


@pytest.mark.parametrize("value", ["— Иванов, 09.10", "- Иванов, 09.10", "нет, потому что стенд занят", "none yet", "?? Иванов",
                                   "tbd: Dev1, 09.10", "Dev1, 08.10"])
@pytest.mark.parametrize("key", ["подтвердил", "обоснование"])
def test_a_dash_or_a_word_with_text_is_not_empty(key, value):
    assert piles.leftover_problem(carried(**{key: value})) is None


def test_both_keys_placeholders_are_both_named_and_the_missing_and_empty_forms_are_unchanged():
    why = piles.leftover_problem(carried(обоснование="—", подтвердил="n/a"))
    assert "`обоснование: —`" in why and "`подтвердил: n/a`" in why, why
    assert "`подтвердил:` is empty" in piles.leftover_problem(carried(подтвердил=""))
    assert "`подтвердил:` is missing" in piles.leftover_problem({k: v for k, v in carried().items() if k != "подтвердил"})
    assert piles.leftover_problem(carried()) is None


def test_the_done_key_keeps_its_regex_and_a_dash_is_no_done():
    assert "neither 7-40 hex characters nor t-nnn" in piles.leftover_problem({"сделано": "—"})
    assert piles.leftover_problem({"сделано": "t-601"}) is None


@needs_git
@pytest.mark.parametrize("line,needle", [
    ("- дело | перенос: пачка 2 | обоснование: нужен стенд | подтвердил: —", "`подтвердил: —` is a placeholder"),
    ("- дело | перенос: пачка 2 | обоснование: нужен стенд | подтвердил: N/A", "`подтвердил: N/A` is a placeholder"),
    ("- дело | перенос: пачка 2 | обоснование: tbd | подтвердил: Dev1, 08.10", "`обоснование: tbd` is a placeholder"),
])
def test_close_refuses_a_placeholder_confirmation_through_the_command(tree, cli, line, needle):
    with_leftovers(tree, line)
    snap = tree_state(tree)
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree), "--today", "2026-10-08")
    assert code == 2 and needle in out and "Nothing was written" in out and "a PERSON" in out, out
    assert tree_state(tree) == snap


@needs_git
def test_close_passes_a_dash_with_a_name_through_the_command(tree, cli):
    with_leftovers(tree, "- дело | перенос: пачка 2 | обоснование: нужен стенд | подтвердил: — Dev1, 09.10")
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree), "--today", "2026-10-08")
    assert code == 0 and "forge/1 closed" in out, out


# ---------------------------------------------------------------- F6-30: an «Остатки» item is written WITH its executor (check (д))

WHY = "an item is written with its executor"          # the tail of the red: the three forms
BARE = "- осталось дело"


def red_lines(out):
    return [l for l in out.splitlines() if "«Остатки» line" in l and "RED" in l]


def left(tree, cli, *lines, rel=B1, old=LEFTOVER_OK):
    """Replace the leftovers of `rel` with `lines`, stage, run `check`: -> (code, output, the «Остатки» red lines)."""
    edit(tree, rel, old, "\n".join(lines))
    stage(tree, "plans/piles")
    code, out = cli(tree, "check")
    return code, out, red_lines(out)


def other_batches(tree):
    """forge/2: a waiting batch with F0-3 (an executor) and F0-4 (none); forge/3: a CLOSED batch with F0-5; report-delivery/1: RD1-1."""
    brief = "## Бриф\n"
    put(tree, B2, batch_text("forge", 2, "ожидает", [node("F0-3", "`tools/b.py`", "ожидает"), node("F0-4", "`tools/c.py`", "ожидает", executor="—")],
                             pre=brief, who="—", branch="—"))
    put(tree, "plans/piles/forge/batch-3-old.md", batch_text("forge", 3, "закрыта", [node("F0-5", "`tools/d.py`", "принято")]))
    put(tree, "plans/piles/report-delivery/batch-1-r.md", batch_text("report-delivery", 1, "ожидает", [node("RD1-1", "`tools/e.py`", "ожидает")],
                                                                    pre=brief, who="—", branch="—"))


@needs_git
def test_k7_a_new_bare_item_is_red_with_the_three_forms_and_the_door_and_a_done_item_is_not(tree, cli):
    code, out, reds = left(tree, cli, LEFTOVER_OK, BARE)                           # the negative control: one bare line appended
    assert code == 2 and len(reds) == 1 and "осталось дело" in reds[0], out
    assert WHY in reds[0] and "сделано: <hash | t-nnn>" in reds[0] and "узел: <node id>" in reds[0] and "перенос: <target>" in reds[0]
    assert "piles-skip: <item> -- <reason>" in out                                  # the door is named (FR-2)
    code, out, reds = left(tree, cli, LEFTOVER_OK, "- осталось дело | сделано: t-12", old=LEFTOVER_OK + "\n" + BARE)
    assert reds == [], out


@needs_git
@pytest.mark.parametrize("line,red", [
    ("- дело | сделано: t-12", False), ("- дело | сделано: abc1234", False), ("- дело | сделано: —", True),
    ("- дело | сделано: abcdef", True), ("- дело | сделано: t-12 (потом)", True),
])
def test_k8_the_done_form(tree, cli, line, red):
    code, out, reds = left(tree, cli, line)
    assert bool(reds) is red, out


@needs_git
@pytest.mark.parametrize("value,needle", [
    ("F0-3", None),                                    # own pile, a node row of an untaken batch with an executor
    ("forge/2/F0-3", None),                            # cross-pile form, the same pile
    ("report-delivery/1/RD1-1", None),                 # another pile
    ("F0-1", None),                                    # a node of the item's own (taken) batch: a node row that is worked
    ("F0-99", "names no node row (looked in the batch files of pile forge"),
    ("F0-4", "has no Исполнитель"),                    # M-b: the executor check
    ("F0-5", "stands only in a «закрыта» batch"),
    ("nope/1/F0-3", 'names pile "nope", which does not exist'),
    ("forge/9/F0-3", "names batch forge/9, which has no batch file"),
    ("forge/2/RD1-1", "names no node row (looked in batch forge/2"),
    ("report-delivery/1/F0-3", "names no node row (looked in batch report-delivery/1"),
    ("F0-3 (later)", "is not a node id"),               # the value stands alone, like `сделано:`
    ("", "is not a node id"),
])
def test_k9_the_node_form(tree, cli, value, needle):
    other_batches(tree)
    code, out, reds = left(tree, cli, "- дело | узел: %s" % value)
    if needle is None:
        assert reds == [], out
    else:
        assert len(reds) == 1 and needle in reds[0], out


@needs_git
def test_k9_a_node_item_may_later_be_closed_by_done_and_a_node_alone_is_refused_by_close_with_that_sentence(tree, cli):
    other_batches(tree)
    code, out, reds = left(tree, cli, "- дело | узел: F0-3 | сделано: t-12")
    assert reds == [], out
    accept_batch1(tree)
    edit(tree, B1, "- дело | узел: F0-3 | сделано: t-12", "- дело | узел: F0-3")
    snap = tree_state(tree)
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree), "--today", "2026-10-08")
    assert code == 2 and "a «узел:» item is closed by «сделано: <hash | t-nnn>» when the node merges, or carried" in out, out
    assert tree_state(tree) == snap                                                  # the close gate's forms are unchanged


@needs_git
def test_k10_a_placeholder_confirmation_passes_check_and_is_still_refused_by_close(tree, cli):
    carry = "- дело | перенос: пачка 2 | обоснование: нужен стенд | подтвердил: —"
    code, out, reds = left(tree, cli, carry)
    assert reds == [], out                                                           # E-D1-8: (д) accepts the placeholder ...
    accept_batch1(tree)
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree), "--today", "2026-10-08")
    assert code == 2 and "`подтвердил: —` is a placeholder" in out, out              # ... `close` still demands a person
    for line in ("- дело | перенос: пачка 2 | подтвердил: —", "- дело | перенос: пачка 2 | обоснование: tbd | подтвердил: —",
                 "- дело | перенос: пачка 2 | обоснование: р", "- дело | перенос: что-то | обоснование: р | подтвердил: —"):
        edit(tree, B1, carry, line)
        stage(tree, "plans/piles")
        assert red_lines(cli(tree, "check")[1]), line
        carry = line


@needs_git
def test_k11_an_old_bare_item_stays_legal_and_counted_an_edited_one_is_red_and_the_multiset_holds(tree, cli):
    edit(tree, B1, LEFTOVER_OK, BARE + "\n" + BARE)                                  # HEAD holds the bare item twice: the grandfathered state
    commit(tree, "bare")
    assert len(piles.leftovers_unowned(piles.load_tree(tree))) == 2                  # E-D1-4: counted after the gate exists, not refused
    code, out = cli(tree, "check", "--all")
    assert not red_lines(out), out                                                   # `--all` without --base compares with HEAD: all old
    code, out, reds = left(tree, cli, BARE + " уточнение", BARE, old=BARE + "\n" + BARE)
    assert len(reds) == 1 and "уточнение" in reds[0], out                            # E-D1-5: the edited item is changed, the other stays old
    edit(tree, B1, BARE + " уточнение\n" + BARE, BARE + "\n" + BARE + "\n" + BARE)   # a THIRD copy: one old copy does not legalize it
    stage(tree, "plans/piles")
    assert len(red_lines(cli(tree, "check")[1])) == 1
    edit(tree, B1, BARE + "\n" + BARE + "\n" + BARE, "- другое | сделано: t-1\n" + BARE + "\n" + BARE)   # moved lines, unchanged: old
    stage(tree, "plans/piles")
    assert red_lines(cli(tree, "check")[1]) == []


@needs_git
def test_k12_a_closed_batch_is_never_judged(tree, cli):
    edit(tree, B1, "статус: в работе", "статус: закрыта")
    code, out, reds = left(tree, cli, BARE)
    assert reds == [], out                                                           # E-D1-10


@needs_git
def test_k13_a_file_absent_at_the_base_has_only_new_items_and_k16_an_unreadable_base_never_makes_one_old(tree, cli):
    put(tree, B2, batch_text("forge", 2, "ожидает", [node("F0-3", "`tools/b.py`", "ожидает")], pre="## Бриф\n", who="—", branch="—", leftovers=BARE))
    stage(tree, "plans/piles")
    code, out = cli(tree, "check")
    assert len(red_lines(out)) == 1 and "cannot be read here" not in out, out        # K13: the rev is readable, the path is absent: new
    commit(tree, "b2")
    code, lines = piles.run_check(tree, True, "", "HEAD")
    assert not any("«Остатки» line" in l for l in lines)                             # old against HEAD
    code, lines = piles.run_check(tree, True, "", "no-such-rev")
    text = "\n".join(lines)
    assert code == 2 and "the base no-such-rev cannot be read here" in text and "«Остатки» line" in text, text     # K16: all judged + one note
    assert text.count("cannot be read here") == 1


@needs_git
def test_k14_the_summary_count_line_names_the_unowned_leftovers_zero_included(tree, cli):
    assert "; остатков без исполнителя: 0" in cli(tree, "summary")[1]
    edit(tree, B1, LEFTOVER_OK, BARE + "\n- ok | сделано: t-1")
    found = piles.leftovers_unowned(piles.load_tree(tree))
    assert [(p, item) for p, _, item in found] == [(B1, BARE)], found
    assert "; остатков без исполнителя: 1" in cli(tree, "summary")[1]


def test_k15_the_leftover_key_regexp_knows_the_node_key_in_a_key_position_only():
    assert piles.LEFTOVER_KEY_RE.search("- x | узел: F0-1") and piles.LEFTOVER_KEY_RE.search("узел: F0-1")
    assert not piles.LEFTOVER_KEY_RE.search("- ждёт, потому что узел: F0-1 не взят")
