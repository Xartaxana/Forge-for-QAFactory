"""Tests for tools/piles.py: the commit-message door `piles-skip:` of `check`.

Part of the split of the old tools/test_piles.py (t-596, the 120 s cap per file): the helpers are in
tools/piles_testkit.py, the fixtures `session_tree`, `tree`, `cli` in tools/conftest.py.
Run from the repo root: python -m pytest tools/test_piles_door.py -q
"""
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import md_regions  # noqa: E402
from piles_testkit import GIT_VARS, git, needs_git, stage, dup_finding, msg  # noqa: E402


@pytest.fixture(autouse=True)
def _scrub_git_env(monkeypatch):
    for k in GIT_VARS:
        monkeypatch.delenv(k, raising=False)


# ---------------------------------------------------------------- the door

def red_tree(tree):
    dup_finding(tree)
    stage(tree, "plans/piles")


@needs_git
def test_check_door_passes_named_item_only(tree, cli):
    red_tree(tree)
    code, out = cli(tree, "check", "--msg-file", msg(tree, "subject\n\npiles-skip: а -- moving the finding in the next commit\n"))
    assert code == 0 and "(а) placement: RED, passed by the commit message: piles-skip: а -- moving" in out
    assert cli(tree, "check", "--msg-file", msg(tree, "subject\n\npiles-skip: д -- wrong item\n"))[0] == 2
    assert cli(tree, "check")[0] == 2                                           # no --msg-file: no door is read


@needs_git
def test_check_door_ascii_alias_and_two_items(tree, cli):
    red_tree(tree)
    for line in ("piles-skip: a -- latin a", "piles-skip: placement -- the key", "   piles-skip: б, а -- two items",
                 "piles-skip: PLACEMENT -- upper"):
        assert cli(tree, "check", "--msg-file", msg(tree, "s\n\n" + line + "\n"))[0] == 0, line


@pytest.mark.parametrize("text", [
    "s\n\n```\npiles-skip: а -- in a fence\n```\n",
    "s\n\n> piles-skip: а -- in a quote\n",
    "s\n\n# piles-skip: а -- a git comment\n",
    "s\n\nsee the piles-skip: а -- in the middle of prose\n",
    "s\n\npiles-skip: а --\n",
    "s\n\npiles-skip: а\n",
    "s\n\npiles-skip: а - reason\n",
])
@needs_git
def test_check_door_ignored_in_fence_quote_comment_or_without_reason(tree, cli, text):
    red_tree(tree)
    assert cli(tree, "check", "--msg-file", msg(tree, text))[0] == 2


@needs_git
def test_check_door_unknown_item_is_named(tree, cli):
    red_tree(tree)
    code, out = cli(tree, "check", "--msg-file", msg(tree, "s\n\npiles-skip: x -- why\n"))
    assert code == 2 and 'piles-skip: unknown item "x" -- items: а/placement, б/overlap, в/frozen, г/backlog, д/form' in out


@needs_git
def test_check_door_not_counted_when_scanner_fails_or_degrades(tree, cli, monkeypatch):
    red_tree(tree)
    m = msg(tree, "s\n\npiles-skip: а -- reason\n")
    monkeypatch.setattr(md_regions, "scan", lambda t: (_ for _ in ()).throw(RuntimeError("boom")))
    code, out = cli(tree, "check", "--msg-file", m)
    assert code == 2 and "not counted" in out and "boom" in out
    monkeypatch.setattr(md_regions, "scan", lambda t: md_regions.ScanResult([], True, "max_regions_exceeded"))
    code, out = cli(tree, "check", "--msg-file", m)
    assert code == 2 and "scanner is degraded (max_regions_exceeded)" in out


@needs_git
def test_check_door_crlf_message(tree, cli):
    red_tree(tree)
    assert cli(tree, "check", "--msg-file", msg(tree, "s\r\n\r\npiles-skip: а -- crlf\r\n"))[0] == 0


@needs_git
def test_check_refusal_text_names_item_expectation_and_door(tree, cli):
    red_tree(tree)
    code, out = cli(tree, "check")
    last = out.strip().splitlines()[-1]
    assert last.startswith("piles check: refused -- red: (а).") and 'piles-skip: <item> -- <reason>' in last
    assert "an id has one home" in out                                          # what is wrong + how to fix, per red


@needs_git
def test_check_merge_in_progress_names_the_door(tree, cli):
    red_tree(tree)
    git(tree, "update-ref", "refs/heads/other", "HEAD")
    (tree / ".git" / "MERGE_HEAD").write_text(git(tree, "rev-parse", "HEAD").strip() + "\n")
    code, out = cli(tree, "check")
    assert code == 2 and "a merge is in progress" in out and "git commit" in out
