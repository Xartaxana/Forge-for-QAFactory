"""Tests for tools/md_table.py's fence reader -- the ONE fence reader of the markdown tools (F6-16, critic t-815 F-4 / L-7).

The invariants under test: (1) `fence_walk` reads a block by the rule "a mark of the opening kind closes it"; a mark of the OTHER
kind inside a block is inside, so a fence opened with `~~~` and met by ``` is NOT closed (and the reverse); (2) `md_lines_outside_fences`
and `unclosed_fence` are views of it; (3) a fence inside an HTML comment is no fence once the comment is blanked (the comment wins);
(4) the piles reader of the BACKLOG head that would hide a `piles-freeze:` line behind a block nothing closes fails LOUDLY, naming
the line of the opener (the `fence_unclosed:<line>` model of digest_form); (5) `leftover_items` stays fence-blind by design.

Run from the repo root: python -m pytest tools/test_md_table.py -q
"""
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

import md_table  # noqa: E402
import piles  # noqa: E402
from piles_testkit import finding_text, put  # noqa: E402


def roles(text):
    return [r for _, _, r in md_table.fence_walk(text.split("\n"))]


# ----- fence_walk: the roles, and the kind rule ----------------------------------------------------------------------------

def test_the_roles_of_a_closed_block():
    assert roles("a\n```py\nb\n```\nc") == ["text", "open", "inside", "close", "text"]


def test_a_tilde_block_is_closed_by_a_tilde_mark_and_a_backtick_block_by_a_backtick_mark():
    assert roles("~~~\nx\n~~~") == ["open", "inside", "close"] and roles("```\nx\n```") == ["open", "inside", "close"]


def test_a_fence_opened_with_tildes_and_met_by_backticks_is_not_closed():
    text = "~~~\nx\n```\n@import-looking line\n"
    assert roles(text) == ["open", "inside", "inside", "inside", "inside"]
    assert md_table.unclosed_fence(text.split("\n")) == 0
    assert [i for i, _ in md_table.md_lines_outside_fences(text.split("\n"))] == []


def test_a_fence_opened_with_backticks_and_met_by_tildes_is_not_closed():
    text = "```\nx\n~~~\ny"
    assert roles(text) == ["open", "inside", "inside", "inside"] and md_table.unclosed_fence(text.split("\n")) == 0


def test_the_mark_of_the_other_kind_inside_a_block_does_not_hide_the_real_close():
    text = "~~~\n```\n~~~\nafter"
    assert roles(text) == ["open", "inside", "close", "text"] and md_table.unclosed_fence(text.split("\n")) is None


@pytest.mark.parametrize("line,is_mark", [("```", True), ("   ~~~", True), ("    ```", False), ("``", False), ("x ```", False),
                                          ("~~~~ info", True), ("\t```", False)])
def test_what_is_a_mark_up_to_three_spaces_and_a_run_of_three(line, is_mark):
    assert (roles(line) == ["open"]) is is_mark


def test_a_longer_opener_is_not_closed_by_a_shorter_run_the_old_agents_md_case():
    assert roles("````\n```\n@X\n````") == ["open", "inside", "inside", "close"]
    assert roles("````\n```\n@X") == ["open", "inside", "inside"] and md_table.unclosed_fence("````\n```\n@X".split("\n")) == 0


def test_a_closer_carrying_an_info_string_does_not_close_the_other_old_agents_md_case():
    assert roles("```\n```sh\n@X\n```") == ["open", "inside", "inside", "close"]
    assert roles("```\n```sh\n@X") == ["open", "inside", "inside"]


@pytest.mark.parametrize("closer", ["```", "````", "`````  ", "   ```\t", "  ````"])
def test_a_closer_is_the_same_character_a_run_at_least_as_long_and_nothing_else(closer):
    assert roles("```\nx\n%s" % closer) == ["open", "inside", "close"]


@pytest.mark.parametrize("not_closer", ["``", "```x", "~~~", "    ```", "``` ```", "````lang"])
def test_what_does_not_close_a_triple_backtick_block(not_closer):
    assert roles("```\nx\n%s" % not_closer) == ["open", "inside", "inside"]


def test_a_longer_opener_needs_its_own_length_the_same_for_tildes():
    assert roles("~~~~~\nx\n~~~~\n~~~~~~") == ["open", "inside", "inside", "close"]


def test_digest_form_reads_a_sh_line_inside_an_open_block_as_inside_not_close():
    import digest_form
    body, flag = digest_form._body(["key", "```", "```sh", "x"], 0)
    assert body == ["", "", ""] and flag == 2                                    # the block never closed: flagged by its line


def test_piles_reads_a_sh_line_inside_an_open_block_as_inside_not_close():
    with pytest.raises(piles.CannotRun) as e:
        piles.backlog_marks(backlog("```\n```sh\n%s\n" % LOCK).split("\n"))
    assert "plans/BACKLOG.md:1:" in str(e.value)
    assert [v for _, v in piles.backlog_marks(backlog("```\n```sh\n%s\n```\n%s\n" % (LOCK, LOCK)).split("\n"))[2]] == [("2026-10-08", 1, 0)]


def test_the_views_agree_with_the_walk():
    lines = "t0\n```\ninside\n```\nt4\n~~~\nnever".split("\n")
    assert list(md_table.md_lines_outside_fences(lines)) == [(0, "t0"), (4, "t4")]
    assert md_table.unclosed_fence(lines) == 5
    assert md_table.unclosed_fence("a\n```\nb\n```".split("\n")) is None and md_table.unclosed_fence([]) is None


def test_two_unclosed_looking_openers_name_the_one_nothing_closes():
    assert md_table.unclosed_fence("```\nx\n```\n~~~\ny".split("\n")) == 3


# ----- the comment wins ----------------------------------------------------------------------------------------------------

def test_a_fence_inside_an_html_comment_is_no_fence_once_the_comment_is_blanked():
    lines = ["a", "<!--", "```", "-->", "b"]
    assert md_table.unclosed_fence(lines) == 2                                  # the raw lines: a block opens inside the comment
    blanked, unclosed = md_table._blank_comments(lines)
    assert unclosed is None and md_table.unclosed_fence(blanked) is None        # the comment hides the mark: nothing opens
    assert [l for _, l in md_table.md_lines_outside_fences(blanked)] == ["a", "", "", "", "b"]


# ----- piles: the BACKLOG head reader is loud on a block nothing closes ----------------------------------------------------

LOCK = "piles-freeze: 2026-10-08 open=1 closed=0"


def backlog(head):
    return head + "\n## Открыто\n\n| id | what |\n|---|---|\n| B-001 | x |\n\n## Закрыто\n\n| id | what |\n|---|---|\n"


def test_an_unclosed_fence_in_the_backlog_head_is_loud_and_names_the_line_of_the_opener():
    text = backlog("# Backlog\n\nprose\n```\nan example\n%s\n" % LOCK)
    with pytest.raises(piles.CannotRun) as e:
        piles.parse_backlog_rows(text)
    msg = str(e.value)
    assert msg.startswith("plans/BACKLOG.md:4:") and "never closed" in msg and "piles-freeze:" in msg and "before the first «## » heading" in msg
    assert "add it and run again" in msg                                         # the door is named (FR-1)


def test_a_tilde_opener_met_by_backticks_is_loud_too():
    with pytest.raises(piles.CannotRun) as e:
        piles.backlog_marks(backlog("~~~\n```\n%s\n" % LOCK).split("\n"))
    assert "plans/BACKLOG.md:1:" in str(e.value)


def test_a_closed_fence_hides_its_lock_and_a_lock_after_it_is_read():
    marks, boundary, locks = piles.backlog_marks(backlog("```\n%s\n```\n%s\n" % (LOCK, LOCK)).split("\n"))
    assert [v for _, v in locks] == [("2026-10-08", 1, 0)] and locks[0][0] == 4


def test_a_fence_below_the_first_h2_is_not_the_head_and_is_not_loud():
    text = backlog("# Backlog\n%s\n" % LOCK) + "\n```\nnever closed in the table area\n"
    assert [v for _, v in piles.parse_backlog_rows(text).locks] == [("2026-10-08", 1, 0)]


def test_the_live_backlog_head_reads_without_a_fence_error():
    piles.parse_backlog_rows(piles.read_text(TOOLS.parent / "plans" / "BACKLOG.md"))


# ----- the readers that stay fence-blind by design -------------------------------------------------------------------------

def test_leftover_items_stays_fence_blind_only_a_comment_hides_a_line():
    items, unclosed = piles.leftover_items("## Остатки\n\n```\n- fenced item\n\n- after an unclosed fence\n")
    assert [t for _, t in items] == ["```", "- fenced item", "- after an unclosed fence"] and unclosed is None


# ----- piles: the readers of the placement (batch prose, a finding's own moves) are loud on a block nothing closes -----------

B1 = "plans/piles/forge/batch-1-foundation.md"
F_REL = "plans/piles/forge/findings/20261014-novoe.md"


def _line_of(tree, rel, needle):
    return [l for l in (tree / rel).read_bytes().decode("utf-8").split("\n")].index(needle) + 1


def _appended(tree, rel, tail):
    put(tree, rel, (tree / rel).read_bytes().decode("utf-8") + tail)


@pytest.mark.parametrize("command", [("check", "--all"), ("board",)])
def test_a_batch_file_with_an_unclosed_fence_is_loud_names_file_and_line_and_exits_1(tree, cli, capsys, command):
    _appended(tree, B1, "\n```\n| F9-9 | hidden row |\n")
    line = _line_of(tree, B1, "```")
    capsys.readouterr()
    code, out = cli(tree, *command)
    err = capsys.readouterr().err
    text = out + err
    assert code == 1 and "%s:%d:" % (B1, line) in text and "never closed" in text and "«not placed»" in text, text
    assert "add it and run again" in text                                             # the door (FR-1)


@pytest.mark.parametrize("command", [("check", "--all"), ("board",)])
def test_a_finding_with_an_unclosed_fence_is_loud_names_file_and_line_and_exits_1(tree, cli, capsys, command):
    put(tree, F_REL, finding_text("—") + "\n~~~\nперенос: other/x\n")
    line = _line_of(tree, F_REL, "~~~")
    code, out = cli(tree, *command)
    text = out + capsys.readouterr().err
    assert code == 1 and "%s:%d:" % (F_REL, line) in text and "never closed" in text, text


def test_closed_fences_in_a_batch_file_and_a_finding_stay_quiet_and_rows_after_them_are_read(tree):
    _appended(tree, B1, "\n```\nan example\n```\n")
    put(tree, F_REL, finding_text("—") + "\n```\nперенос: gone/x\n```\n")
    tr = piles.load_tree(tree, tolerant=True)
    assert piles.pile_prose(tr)                                                       # no CannotRun
    f = next(x for x in tr.piles["forge"].findings if x.name == "20261014-novoe.md")
    assert piles._finding_moves(f) == []                                              # the fenced line is no move, and nothing is raised


def test_batch_prose_without_a_path_still_names_the_line_and_the_two_readers_are_loud_directly(tree):
    with pytest.raises(piles.CannotRun) as e:
        piles._batch_prose("a\n```\nb\n")
    assert str(e.value).startswith("this batch file:2:")
    put(tree, F_REL, finding_text("—") + "\n```\n")
    f = next(x for x in piles.load_tree(tree, tolerant=True).piles["forge"].findings if x.name == "20261014-novoe.md")
    with pytest.raises(piles.CannotRun) as e:
        piles._finding_moves(f)
    assert str(e.value).startswith(F_REL + ":")


def test_proof_problems_stays_fence_blind_too():
    """A table inside a block nothing closes is still read (only a comment hides a line): no CannotRun, the problem is found at its line."""
    problems = piles.proof_problems("## Живые доказательства\n\n```\n| a | b |\n")
    assert len(problems) == 1 and problems[0].startswith("line 4: the table has no «Статус» column")


# ----- t-870 F-1: a finding is read through the SAME blanking as a batch file -----------------------------------------------

def _finding(tree, body):
    put(tree, F_REL, finding_text("—") + body)
    return next(x for x in piles.load_tree(tree, tolerant=True).piles["forge"].findings if x.name == "20261014-novoe.md")


def test_a_fence_inside_a_comment_of_a_finding_is_no_fence_and_the_move_outside_the_comment_is_read(tree):
    f = _finding(tree, "\n<!-- template:\n```\n-->\nперенос: forge/6\n")
    assert piles._finding_moves(f) == ["forge"]                                      # no CannotRun: the mark sits in a comment


def test_a_move_inside_a_comment_of_a_finding_is_no_move(tree):
    assert piles._finding_moves(_finding(tree, "\n<!--\nперенос: forge/6\n-->\n")) == []


# ----- t-870 F-2: ONE builder of the refusal, ONE text -----------------------------------------------------------------------

def _fence_refusal(caller, tree):
    """-> (the message of the refusal `caller` raises on a fence nothing closes, the `<where>:<line>` prefix it must start with)."""
    if caller == "backlog_marks":
        run, prefix = (lambda: piles.backlog_marks(backlog("```\nx\n").split("\n"))), "plans/BACKLOG.md:1"
    elif caller == "_batch_prose":
        run, prefix = (lambda: piles._batch_prose("```\nx\n", "plans/piles/forge/batch-1-x.md")), "plans/piles/forge/batch-1-x.md:1"
    else:
        f = _finding(tree, "\n```\nx\n")
        run, prefix = (lambda: piles._finding_moves(f)), "%s:%d" % (F_REL, f.text.split("\n").index("```") + 1)
    with pytest.raises(piles.CannotRun) as e:
        run()
    return str(e.value), prefix


@pytest.mark.parametrize("caller", ["backlog_marks", "_batch_prose", "_finding_moves"])
def test_the_three_callers_refuse_in_one_form(tree, caller):
    msg, prefix = _fence_refusal(caller, tree)
    assert msg.startswith(prefix + ": the fenced block opened here is never closed -- it hides every line after it, so "), msg
    assert "; expected a closing line of the same kind (``` or ~~~) " in msg and msg.endswith("; add it and run again"), msg


# ----- t-870 F-4: comment vs fence, the FIRST OPENER WINS ---------------------------------------------------------------------

def test_a_comment_opener_inside_an_open_fence_is_code_no_comment_starts():
    lines = ["```", "<!-- an opener example", "```", "| F6-16 | x |"]
    blanked, unclosed = md_table._blank_comments(lines)
    assert blanked == lines and unclosed is None and md_table.unclosed_fence(blanked) is None        # the critic's case: nothing raised
    assert [l for _, l in md_table.md_lines_outside_fences(blanked)] == ["| F6-16 | x |"]


def test_a_closed_comment_inside_a_fence_is_kept_as_code():
    lines = ["~~~", "<!-- c -->", "~~~", "t"]
    assert md_table._blank_comments(lines) == (lines, None)


def test_a_fence_that_never_closes_stays_the_fences_own_refusal_even_with_a_comment_opener_inside():
    lines = ["```", "<!-- x", "y"]
    assert md_table._blank_comments(lines) == (lines, None) and md_table.unclosed_fence(lines) == 0
    with pytest.raises(piles.CannotRun) as e:
        piles._batch_prose("\n".join(lines), "plans/piles/forge/batch-1-x.md")
    assert str(e.value).startswith("plans/piles/forge/batch-1-x.md:1:")                                # the fence opened first


def test_a_closed_fence_with_a_comment_opener_inside_is_read_normally_by_the_batch_reader():
    prose = piles._batch_prose("a\n```\n<!-- an opener example\n```\n| F6-16 | x |", "plans/piles/forge/batch-1-x.md")
    assert prose == "a\n| F6-16 | x |"


def test_a_fence_opened_inside_a_comment_that_never_closes_is_hidden_with_the_rest_no_refusal():
    """The silent case that STAYS (not this round's to fix): the comment hides everything after it, as an HTML reader would show."""
    blanked, unclosed = md_table._blank_comments(["a", "<!-- c", "```", "b"])
    assert unclosed == 1 and blanked == ["a", "<!-- c", "```", "b"]
    assert piles._batch_prose("a\n<!-- c\n```\nb", "x.md") == "a\n"


@pytest.mark.parametrize("line,expected", [("``` <!-- x -->", ["open", "inside", "close"]), ("<!-- x --> ```", ["open", "inside", "close"]),
                                           ("text <!-- ``` -->", ["text", "text", "open"]), ("<!-- ``` -->", ["text", "text", "open"])])
def test_on_one_line_the_first_opener_wins(line, expected):
    """A mark at the line start opens before any comment (the `<!--` after it is only an info string); a comment that closes
    first leaves a mark after it to open; a mark INSIDE a comment is commented out (the line is text, and the third line, a bare
    mark, is then the one that opens)."""
    blanked, _ = md_table._blank_comments([line, "inside", "```"])
    assert [r for _, _, r in md_table.fence_walk(blanked)] == expected


def test_without_a_fence_the_walk_blanks_exactly_what_the_old_regex_did():
    import random
    import re
    def old(lines):
        out = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), "\n".join(lines), flags=re.S).split("\n")
        return out, next((i for i, l in enumerate(out) if "<!--" in l), None)
    rng = random.Random(7)
    parts = ["<!--", "-->", "a", " ", "<!-->", "|", "x y", "<!-- c -->", "-- >"]
    for _ in range(400):
        lines = ["".join(rng.choice(parts) for _ in range(rng.randint(0, 5))) for _ in range(rng.randint(1, 6))]
        assert md_table._blank_comments(lines) == old(lines), lines


# ----- t-870 F-6: a tab-indented mark is text for the one fence reader (CommonMark), where the old agents_md regex took it --------

def test_a_tab_indented_mark_is_text_not_a_fence_so_an_import_after_it_expands():
    assert roles("\t```\n@import-looking line") == ["text", "text"] and md_table.unclosed_fence(["\t```", "x"]) is None
