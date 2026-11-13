"""Tests for tools/piles.py: `check` item (а) placement, a9 and the carried reds.

Part of the split of the old tools/test_piles.py (t-596, the 120 s cap per file): the helpers are in
tools/piles_testkit.py, the fixtures `session_tree`, `tree`, `cli` in tools/conftest.py.
Run from the repo root: python -m pytest tools/test_piles_placement.py -q
"""
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from piles_testkit import summary_text, GIT_VARS, put, card_text, batch_text, node, finding_text, B1, needs_git, stage, commit, freeze, edit, lines_with, dup_finding  # noqa: E402


@pytest.fixture(autouse=True)
def _scrub_git_env(monkeypatch):
    for k in GIT_VARS:
        monkeypatch.delenv(k, raising=False)


@needs_git
def test_check_negative_control_broken_tree_refused_with_item_name(tree, cli):
    dup_finding(tree)
    stage(tree, "plans/piles")
    code, out = cli(tree, "check")
    assert code == 2 and "(а)" in out and "B-135" in out
    assert "forge/findings/B-135-a.md" in out and "report-delivery/findings/B-135-b.md" in out
    # the same tree with the copy removed passes
    (tree / "plans/piles/report-delivery/findings/B-135-b.md").unlink()
    stage(tree, "plans/piles")
    code, out = cli(tree, "check")
    assert code == 0 and "RED" not in out, out


@needs_git
def test_check_a_unknown_id_in_card_row(tree, cli):
    edit(tree, "plans/piles/forge/README.md", "B-230", "B-230, B-999")
    stage(tree, "plans/piles")
    code, out = cli(tree, "check")
    assert code == 2 and "unknown id B-999" in out and "forge/1" in out


@needs_git
def test_check_a_whole_member_in_two_live_batches_and_two_piles(tree, cli):
    edit(tree, "plans/piles/forge/README.md", "| 2 | потом | B-015 |", "| 2 | потом | B-230, B-015 |")
    stage(tree, "plans/piles")
    code, out = cli(tree, "check")
    assert code == 2 and "B-230 is a whole member of 2 live batches" in out
    edit(tree, "plans/piles/forge/README.md", "B-230, B-015", "B-015")
    put(tree, "plans/piles/report-delivery/findings/B-230-x.md", finding_text("B-230", "report-delivery"))
    stage(tree, "plans/piles")
    code, out = cli(tree, "check")
    assert code == 2 and "B-230 has homes in 2 piles" in out and "plans/piles/forge/findings/" in out


@needs_git
def test_check_a_partial_members_in_two_piles_are_fine(tree, cli):
    edit(tree, "plans/piles/forge/README.md", "| 2 | потом | B-015 |", "| 2 | потом | B-308 (а) |")
    put(tree, "plans/piles/report-delivery/README.md",
        card_text("report-delivery", "Report", [["1", "x", "B-308 (б)", "S", "ожидает", "—", "—", "—"]], "F08"))
    stage(tree, "plans/piles")
    assert cli(tree, "check")[0] == 0


@needs_git
def test_check_a_unplaced_open_id_after_freeze_only(tree, cli):
    code, out = cli(tree, "check", "--all")
    assert code == 0 and "every open id placed" in out                        # before the freeze: said, not judged
    freeze(tree, extra_findings=False, commit_it=False)
    code, out = cli(tree, "check", "--all")
    assert code == 2 and "B-102 is open but placed nowhere" in out and "B-308" in out
    freeze_fix = tree / "plans/piles/forge/findings"
    for ident in ("B-102", "B-135", "B-219", "B-308"):
        put(tree, "plans/piles/forge/findings/%s-x.md" % ident, finding_text(ident))
    assert cli(tree, "check", "--all")[0] == 0, freeze_fix


@needs_git
def test_check_a_closed_still_placed(tree, cli):
    put(tree, "plans/piles/forge/findings/B-001-x.md", finding_text("B-001"))
    stage(tree, "plans/piles")
    code, out = cli(tree, "check")
    assert code == 2 and "B-001 is closed but still placed" in out


@needs_git
def test_check_a_both_open_and_closed(tree, cli):
    edit(tree, "plans/BACKLOG.md", "| B-230 | **Кучки.**", "| B-001 | **Двойник.**")
    stage(tree, "plans/BACKLOG.md")
    code, out = cli(tree, "check")
    assert "B-001 is both open and closed" in out and code == 2


@needs_git
def test_check_a_batch_nodes_not_in_card_row(tree, cli):
    put(tree, "plans/piles/forge/batch-1-foundation.md", batch_text("forge", 1, nodes=[node("B-102"), node("B-230")]))
    stage(tree, "plans/piles")
    code, out = cli(tree, "check")
    assert code == 2 and "the batch file names B-102, the card row does not" in out and "B-230, the card" not in out


@needs_git
def test_check_a_finding_name_and_header_must_agree(tree, cli):
    put(tree, "plans/piles/forge/findings/B-102-x.md", finding_text("B-135"))
    put(tree, "plans/piles/forge/findings/B-219-y.md", finding_text("B-219", "report-delivery"))
    stage(tree, "plans/piles")
    code, out = cli(tree, "check")
    assert code == 2 and "name says B-102" in out and 'кучка "report-delivery" but the file is in pile "forge"' in out


@needs_git
def test_check_a9_freeze_commit_staging_only_backlog_is_red(tree, cli):
    # V1 (t-593): the freeze commit stages plans/BACKLOG.md alone; the unplaced ids it creates are ITS reds
    freeze(tree, extra_findings=False, commit_it=False)
    stage(tree, "plans/BACKLOG.md")
    code, out = cli(tree, "check")
    assert code == 2 and "(а) placement: RED" in out and "B-102 is open but placed nowhere" in out, out
    assert "carried" not in lines_with(out, "(а)")[0]
    # the control: the same commit with the findings placed passes
    for ident in ("B-102", "B-135", "B-219", "B-308"):
        put(tree, "plans/piles/forge/findings/%s-x.md" % ident, finding_text(ident))
    stage(tree, "plans")
    assert cli(tree, "check")[0] == 0


@needs_git
def test_check_a9_batch_file_hand_closed_is_red(tree, cli):
    # V1: a batch file hand-set to "закрыта" frees its members -- B-230 is then open and placed nowhere
    freeze(tree)
    edit(tree, B1, "статус: в работе", "статус: закрыта")
    stage(tree, B1)                                                         # only the batch file is staged
    code, out = cli(tree, "check")
    assert code == 2 and "B-230 is open but placed nowhere" in out and "(а) placement: RED" in out, out


@needs_git
def test_check_a9_journal_only_commit_still_runs_nothing(tree, cli):
    freeze(tree, extra_findings=False)                                      # reds exist in the tree (committed)
    put(tree, "logs/journal/x.jsonl", "{}\n")
    stage(tree, "logs/journal/x.jsonl")
    code, out = cli(tree, "check")
    assert code == 0 and "nothing to check" in out, out


@needs_git
def test_check_carried_red_does_not_block_unrelated_commit(tree, cli):
    dup_finding(tree)
    commit(tree, "a violation that landed through a door")
    put(tree, "plans/piles/forge/findings/B-102-x.md", finding_text("B-102"))
    stage(tree, "plans/piles/forge/findings/B-102-x.md")
    code, out = cli(tree, "check")
    assert code == 0 and "(а) placement: carried from earlier commits (not blocking)" in out and "B-135" in out
    code, out = cli(tree, "check", "--all")
    assert code == 2 and "(а) placement: RED" in out                          # --all blocks everything
    stage(tree, "plans/piles/forge/findings/B-135-a.md")                      # touching a carrier makes it ours again
    (tree / "plans/piles/forge/findings/B-135-a.md").write_bytes(finding_text("B-135", title="Изменено").encode("utf-8"))
    stage(tree, "plans/piles/forge/findings/B-135-a.md")
    assert cli(tree, "check")[0] == 2


@needs_git
def test_check_a5_and_summary_agree_on_a_closed_id_that_is_still_placed(tree, cli):
    # m-5 (t-593): B-001 is closed. Placed by a WHOLE live member or by a finding it is an error for (а)5;
    # a PARTIAL member of a live batch is not (`close --id` may close a partial member's id; (в) freezes the Строки cell),
    # and `summary` does not count it open.
    edit(tree, "plans/piles/forge/README.md", "| 2 | потом | B-015 |", "| 2 | потом | B-001, B-015 |")
    stage(tree, "plans/piles")
    code, out = cli(tree, "check")
    assert code == 2 and "B-001 is closed but still placed" in out
    edit(tree, "plans/piles/forge/README.md", "B-001, B-015", "B-001 (хвост), B-015")
    stage(tree, "plans/piles")
    code, out = cli(tree, "check")
    assert code == 0 and "closed but still placed" not in out, out
    assert "открытых id: 6 " in summary_text(tree, cli)                       # a closed id is not counted open
    edit(tree, "plans/piles/forge/README.md", "B-001 (хвост), B-015", "B-015")
    put(tree, "plans/piles/forge/findings/B-001-x.md", finding_text("B-001"))
    stage(tree, "plans/piles")
    assert "B-001 is closed but still placed" in cli(tree, "check")[1]
