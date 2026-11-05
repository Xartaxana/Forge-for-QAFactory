"""Tests for tools/piles.py: `close --id B-nnn --word` (one row closed by the owner's word) and the usage errors.

Part of the split of the old tools/test_piles.py (t-596, the 120 s cap per file): the helpers are in
tools/piles_testkit.py, the fixtures `session_tree`, `tree`, `cli` in tools/conftest.py.
Run from the repo root: python -m pytest tools/test_piles_close_id.py -q
"""
import pathlib
import re
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from piles_testkit import GIT_VARS, put, needs_git, stage, freeze, rd, tree_state, board_text, head_hash, closed_rows  # noqa: E402


@pytest.fixture(autouse=True)
def _scrub_git_env(monkeypatch):
    for k in GIT_VARS:
        monkeypatch.delenv(k, raising=False)


@needs_git
def test_close_id_by_word_moves_one_row_and_gate_accepts_it(tree, cli):
    freeze(tree)
    code, out = cli(tree, "close", "--id", "B-102", "--word", "владелец, 08.10", "--today", "2026-10-08")
    assert code == 0 and "B-102 closed by the owner's word (владелец, 08.10)" in out, out
    row = closed_rows(tree)["B-102"]
    assert "; закрыто 08.10.2026 по слову: владелец, 08.10 |" in row and "влито" not in row
    assert not list((tree / "plans/piles/forge/findings").glob("B-102*"))      # its finding is gone
    assert "| B-102 |" not in rd(tree, "plans/BACKLOG.md").split("\n## Закрыто\n")[0]
    stage(tree, "plans")
    code, out = cli(tree, "check")
    assert code == 0 and "closed outside close" not in out and "RED" not in out, out
    snap = tree_state(tree)
    code, out = cli(tree, "close", "--id", "B-102", "--word", "x")
    assert code == 0 and "B-102 is already closed; nothing changed" in out and tree_state(tree) == snap


@needs_git
def test_close_id_with_hash_and_refusals(tree, cli):
    snap = tree_state(tree)
    h = head_hash(tree)
    refusals = [(("--id", "B-230", "--word", "w"), "B-230 is a whole member of the live batch forge/1"),
                (("--id", "B-999", "--word", "w"), "B-999 has no text anywhere"),
                (("--id", "B-102"), "--word is required with --id"),
                (("--id", "B-102", "--word", "a|b"), "--word is required with --id"),
                (("--id", "B-102", "--word", "a\nb"), "--word is required with --id"),
                (("--id", "B-102", "--word", "a`b"), "a backtick (`)"),                       # m-2
                (("--id", "B-102", "--word", "w" * 121), "of 1-120 characters"),              # m-3: beyond the cap
                (("--id", "102", "--word", "w"), '--id "102": expected B-nnn'),
                (("--id", "B-102", "--word", "w", "--hash", "deadbee"), "is not a commit"),
                (("--id", "B-102", "--word", "w", "--url", "https://x/y"), "takes no slug, N or --url"),
                (("forge", "1", "--id", "B-102", "--word", "w"), "takes no slug, N or --url")]
    for args, needle in refusals:
        code, out = cli(tree, "close", *args)
        assert code == 2 and needle in out, (args, out)
    assert tree_state(tree) == snap
    assert cli(tree, "close", "--id", "B-102", "--word", "владелец", "--hash", h, "--today", "2026-10-08")[0] == 0
    assert "; закрыто 08.10.2026 по слову: владелец; влито `%s` |" % h in closed_rows(tree)["B-102"]


@needs_git
def test_close_word_cap_at_120_and_board_reads_hash_back(tree, cli):
    word = "decade1 " + "w" * 112                                         # 120 characters, a hex-looking first token
    assert len(word) == 120
    assert cli(tree, "close", "--id", "B-102", "--word", word, "--today", "2026-10-08")[0] == 0   # AT the cap
    assert "; закрыто 08.10.2026 по слову: %s |" % word in closed_rows(tree)["B-102"]
    h = head_hash(tree)
    assert cli(tree, "close", "--id", "B-219", "--word", "владелец decade1", "--hash", h, "--today", "2026-10-08")[0] == 0
    toc = dict(re.findall(r"^\| (B-\d+) \| (.*) \|$", board_text(tree, cli), re.M))
    assert toc["B-102"] == "закрыто (хэша нет)"                            # m-4: not 'decade1' out of the word
    assert toc["B-219"] == "закрыто `%s`" % h


@needs_git
def test_close_word_refusals_leave_the_tree_untouched(tree, cli):
    snap = tree_state(tree)
    for word in ("a`b", "w" * 121):
        code, out = cli(tree, "close", "--id", "B-102", "--word", word, "--today", "2026-10-08")
        assert code == 2 and "--word is required with --id" in out, (word, out)
    assert tree_state(tree) == snap


@needs_git
def test_close_warns_about_debt_entries_citing_closed_ids(tree, cli):
    put(tree, "ai-packages/qa-factory/design/factory-rules-debt.md", "# debt\n\n| FR-1 | here, owner B-102 | x |\n| FR-2 | B-1020 only | y |\n")
    code, out = cli(tree, "close", "--id", "B-102", "--word", "w", "--today", "2026-10-08")
    assert code == 0 and "WARNING: debt entries naming B-102: ai-packages/qa-factory/design/factory-rules-debt.md:3 -- remove them in this commit" in out, out
    assert ":4" not in out                                                     # B-1020 is another id


def test_close_preserves_crlf_backlog(tree, cli):
    p = tree / "plans/BACKLOG.md"
    p.write_bytes(p.read_bytes().replace(b"\n", b"\r\n"))
    assert cli(tree, "close", "--id", "B-102", "--word", "w", "--today", "2026-10-08")[0] == 0
    raw = p.read_bytes()
    assert b"\n" not in raw.replace(b"\r\n", b"") and "по слову: w".encode("utf-8") in raw


def test_close_and_take_usage_errors_are_exit_1(tree, cli):
    assert cli(tree, "close")[0] == 1
    assert cli(tree, "close", "--id", "B-102", "--word", "w", "--today", "08.10.2026")[0] == 1
    assert cli(tree, "take", "forge", "2")[0] == 1                             # --who is required
