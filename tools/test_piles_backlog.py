"""Tests for tools/piles.py: `check` item (г) backlog (the freeze line and the archive).

Part of the split of the old tools/test_piles.py (t-596, the 120 s cap per file): the helpers are in
tools/piles_testkit.py, the fixtures `session_tree`, `tree`, `cli` in tools/conftest.py.
Run from the repo root: python -m pytest tools/test_piles_backlog.py -q
"""
import pathlib
import shutil
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
TOOLS = pathlib.Path(__file__).resolve().parent
REAL = TOOLS.parent
from piles_testkit import GIT_VARS, git, put, BACKLOG, finding_text, needs_git, stage, freeze, edit, lines_with  # noqa: E402


@pytest.fixture(autouse=True)
def _scrub_git_env(monkeypatch):
    for k in GIT_VARS:
        monkeypatch.delenv(k, raising=False)


# ---------------------------------------------------------------- (г) backlog

def g_lines(out):
    return lines_with(out, "(г)")


@needs_git
def test_check_g_inactive_before_freeze(tree, cli):
    edit(tree, "plans/BACKLOG.md", "| B-230 | **Кучки.**", "| B-230 | **Кучки правка.**")
    stage(tree, "plans/BACKLOG.md")
    code, out = cli(tree, "check")
    assert code == 0 and "(г) NOT CHECKED backlog -- not frozen yet" in out


@needs_git
def test_check_g_not_staged_is_not_checked(tree, cli):
    stage(tree, "plans/piles")
    put(tree, "plans/piles/forge/findings/B-102-x.md", finding_text("B-102"))
    stage(tree, "plans/piles")
    assert "plans/BACKLOG.md is not staged" in cli(tree, "check")[1]


@needs_git
def test_check_g_freeze_commit_counts(tree, cli):
    edit(tree, "plans/BACKLOG.md", "## Как вести", "piles-freeze: 2026-10-08 open=6 closed=6\n\n## Как вести")
    for ident in ("B-102", "B-135", "B-219", "B-308"):
        put(tree, "plans/piles/forge/findings/%s-x.md" % ident, finding_text(ident))
    stage(tree, "plans")
    code, out = cli(tree, "check")
    assert code == 0 and "(г) backlog: ok (freeze commit" in out, out
    edit(tree, "plans/BACKLOG.md", "open=6 closed=6", "open=7 closed=5")
    stage(tree, "plans")
    code, out = cli(tree, "check")
    assert code == 2 and "says open=7 closed=5 but the file has open=6 closed=6" in out


@needs_git
def test_check_g_new_open_row_red(tree, cli):
    freeze(tree)
    edit(tree, "plans/BACKLOG.md", "| B-308 |", "| B-500 | **Новая.** | п | и | п |\n| B-308 |")
    stage(tree, "plans/BACKLOG.md")
    code, out = cli(tree, "check")
    assert code == 2 and "new open row B-500" in out and "findings/" in out


@needs_git
def test_check_g_close_move_green(tree, cli):
    freeze(tree)
    p = tree / "plans/BACKLOG.md"
    t = p.read_bytes().decode("utf-8")
    row = next(l for l in t.split("\n") if l.startswith("| B-230 |"))
    t = t.replace(row + "\n", "")
    t += "| B-230 | **Кучки.** | почему 230 | владелец; закрыто 08.10.2026 пачкой `forge/1`: влито `abcdef1` | P4 |\n"
    p.write_bytes(t.encode("utf-8"))
    edit(tree, "plans/piles/forge/README.md", "| 1 | фундамент | B-230 | L | в работе", "| 1 | фундамент | B-230 | L | закрыта")
    edit(tree, "plans/piles/forge/batch-1-foundation.md", "статус: в работе", "статус: закрыта")
    stage(tree, "plans")
    code, out = cli(tree, "check")
    assert code == 0 and "(г) backlog: ok" in out, out


@needs_git
def test_check_g_closed_outside_close_red(tree, cli):
    freeze(tree)
    p = tree / "plans/BACKLOG.md"
    t = p.read_bytes().decode("utf-8")
    row = next(l for l in t.split("\n") if l.startswith("| B-102 |"))
    p.write_bytes((t.replace(row + "\n", "") + row + "\n").encode("utf-8"))
    stage(tree, "plans")
    code, out = cli(tree, "check")
    assert code == 2 and "closed outside close: B-102" in out
    # the owner's-word suffix is the sanctioned way to close one row (P3)
    t = p.read_bytes().decode("utf-8").replace(row, row[:-2] + "; закрыто 08.10.2026 по слову: владелец, 08.10 |")
    p.write_bytes(t.encode("utf-8"))
    stage(tree, "plans")
    assert "closed outside close" not in cli(tree, "check")[1]


@needs_git
def test_check_g_marker_removed_and_two_locks_red(tree, cli):
    freeze(tree)
    edit(tree, "plans/BACKLOG.md", "piles-freeze: 2026-10-08 open=6 closed=6\n\n", "")
    stage(tree, "plans/BACKLOG.md")
    code, out = cli(tree, "check")
    assert code == 2 and "the freeze line was removed" in out
    git(tree, "checkout", "-q", "HEAD", "--", "plans/BACKLOG.md")
    edit(tree, "plans/BACKLOG.md", "piles-freeze: 2026-10-08", "piles-freeze: 2026-10-08 open=6 closed=6\npiles-freeze: 2026-10-08")
    stage(tree, "plans/BACKLOG.md")
    code, out = cli(tree, "check")
    assert code == 2 and "two piles-freeze lines" in out


@needs_git
def test_check_g_archive_row_edited_and_removed_rows_red(tree, cli):
    freeze(tree)
    edit(tree, "plans/BACKLOG.md", "почему 219", "почему 219, дописано")
    edit(tree, "plans/BACKLOG.md", "| B-001 | **Старое.** | почему | закрыто кодом: model-rates.json:83 | P1 |\n", "")
    stage(tree, "plans/BACKLOG.md")
    code, out = cli(tree, "check")
    assert code == 2 and "the archive row B-219 was edited" in out and "closed row removed: B-001" in out


@needs_git
def test_check_g_vanished_open_row_red(tree, cli):
    freeze(tree)
    p = tree / "plans/BACKLOG.md"
    t = p.read_bytes().decode("utf-8")
    row = next(l for l in t.split("\n") if l.startswith("| B-135 |"))
    p.write_bytes(t.replace(row + "\n", "").encode("utf-8"))
    stage(tree, "plans/BACKLOG.md")
    code, out = cli(tree, "check")
    assert code == 2 and "row vanished: B-135" in out


def test_check_g_head_unavailable_is_not_checked(tmp_path, cli):
    shutil.copytree(REAL / "plans", tmp_path / "plans")
    git(tmp_path, "init", "-q")
    put(tmp_path, "plans/BACKLOG.md", BACKLOG)
    stage(tmp_path, "plans/BACKLOG.md")
    code, out = cli(tmp_path, "check", "--all")
    assert "(г) NOT CHECKED backlog" in out and "HEAD" in out


@needs_git
def test_check_g_base_option(tree, cli):
    freeze(tree)
    base = git(tree, "rev-parse", "HEAD~1").strip()
    code, out = cli(tree, "check", "--all", "--base", base)
    assert code == 0 and "compared with " + base in out                        # the freeze commit against its parent
