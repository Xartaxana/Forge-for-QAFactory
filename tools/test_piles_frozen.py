"""Tests for tools/piles.py: `check` item (в): a taken batch is frozen against origin/main.

Part of the split of the old tools/test_piles.py (t-596, the 120 s cap per file): the helpers are in
tools/piles_testkit.py, the fixtures `session_tree`, `tree`, `cli` in tools/conftest.py.
Run from the repo root: python -m pytest tools/test_piles_frozen.py -q
"""
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import piles  # noqa: E402
from piles_testkit import GIT_VARS, git, put, card_text, batch_text, node, ROW1, ROW2, B1, B2, CARD, ROW1_LINE, needs_git, stage, commit, edit, fetch_origin, rd, msg, batch2, dup_finding, freeze, finding_text  # noqa: E402


@pytest.fixture(autouse=True)
def _scrub_git_env(monkeypatch):
    for k in GIT_VARS:
        monkeypatch.delenv(k, raising=False)


def v_check(tree, cli, *extra):
    stage(tree, "plans/piles")
    return cli(tree, "check", *extra)


@needs_git
def test_check_v_allows_hod_status_mr_ostatki_queue_and_live_status(tree, cli):
    fetch_origin(tree)
    edit(tree, B1, "статус: в работе | взял: Ира | ветка: `main` (x) | MR: —", "статус: сдано | взял: Ира | ветка: `main` (x) | MR: `abc1234` https://x/y")
    edit(tree, B1, "Правило готовности.\n", "Правило готовности.\nочередь: forge/1 → forge/2\n")
    edit(tree, B1, "`plans/PILES.md` | — | ожидает |", "`plans/PILES.md` | — | сдано 09.10 |")
    edit(tree, B1, "## Ход\n\n- x", "## Ход\n\n- x\n- новая запись")
    edit(tree, B1, "ждёт фазы 1", "сделано")
    edit(tree, B1, "## Остатки\n\n- x", "## Остатки\n\n- y")
    edit(tree, CARD, ROW1_LINE, "| 1 | фундамент | B-230 | L | сдано | Ира | `main` (x) | `abc1234` |")
    code, out = v_check(tree, cli)
    assert code == 0 and "(в) frozen: ok" in out and "compared with origin/main " in out, out


@needs_git
def test_check_v_red_on_node_text_or_row_change(tree, cli):
    fetch_origin(tree)
    original = rd(tree, B1)
    # NEGATIVE CONTROL: the node row of a taken batch is edited -> red with the item letter and the file name
    edit(tree, B1, "| F0-1 | П1 | что | builder | `tools/a.py` |", "| F0-1 | П1 | что | builder | `tools/z.py` |")
    code, out = v_check(tree, cli)
    assert code == 2 and "(в) frozen: RED" in out and "batch-1-foundation.md" in out and "differs from origin/main" in out, out
    assert "`tools/z.py`" in out and "(it was" in out                       # the first differing line is named, with its old text
    put(tree, B1, original)                                                 # the control: the same tree restored passes
    assert v_check(tree, cli)[0] == 0
    edit(tree, B1, "Правило готовности.", "Правило готовности. Дописано.")
    assert v_check(tree, cli)[0] == 2                                       # prose outside the allowed areas
    put(tree, B1, original)
    edit(tree, B1, "ветка: `main` (x)", "ветка: `pile/forge/batch-1`")
    assert v_check(tree, cli)[0] == 2                                       # the taker and the branch are part of the freeze
    put(tree, B1, original)
    edit(tree, B1, "| F0-2 | П1 | что | builder | `plans/PILES.md` | — | ожидает |\n", "")
    assert v_check(tree, cli)[0] == 2                                       # a node row removed


@needs_git
def test_check_v_issue_pair_in_header_is_masked_the_rest_is_not(tree, cli):
    # V3 (t-593): `issue: <url>` in a taken batch's header -- old headers, no longer written; not content, never red
    fetch_origin(tree)
    original = rd(tree, B1)
    edit(tree, B1, "| стенд: не нужен", "| стенд: не нужен | issue: https://git.example/g/p/-/issues/5")   # the write-back form: appended
    code, out = v_check(tree, cli)
    assert code == 0 and "(в) frozen: ok" in out, out                       # an issue pair ADDED
    fetch_origin_with(tree, B1)                                             # origin now carries it ...
    edit(tree, B1, "issues/5", "issues/6")
    code, out = v_check(tree, cli)
    assert code == 0 and "(в) frozen: ok" in out, out                       # ... and a CHANGED value compares equal too
    edit(tree, B1, "ветка: `main` (x)", "ветка: `pile/forge/batch-1`")
    code, out = v_check(tree, cli)
    assert code == 2 and "(в) frozen: RED" in out, out                      # NEGATIVE: any other header pair is still frozen
    put(tree, B1, original)


def fetch_origin_with(root, rel):
    """origin/main := a new commit holding `rel` as it is now (a batch file that already carries a write-back)."""
    stage(root, rel)
    git(root, "commit", "-q", "-m", "origin carries it")
    fetch_origin(root)


@needs_git
def test_check_v_new_or_not_taken_batch_is_free(tree, cli):
    fetch_origin(tree)
    put(tree, B2, batch_text("forge", 2, "ожидает", [node("F0-3", "`tools/b.py`", "ожидает")], who="—", branch="—"))
    code, out = v_check(tree, cli)
    assert code == 0 and "(в) frozen: ok" in out, out                        # not on origin/main at all
    commit(tree, "batch 2 waiting")
    fetch_origin(tree)
    edit(tree, B2, "Правило готовности.", "Правило готовности. Другое.")
    assert v_check(tree, cli)[0] == 0                                        # on origin but ожидает: free


@needs_git
def test_check_v_renamed_file_is_still_frozen(tree, cli):
    fetch_origin(tree)
    git(tree, "mv", B1, "plans/piles/forge/batch-1-renamed.md")
    edit(tree, "plans/piles/forge/batch-1-renamed.md", "`tools/a.py`", "`tools/z.py`")
    code, out = v_check(tree, cli)
    assert code == 2 and "(в) frozen: RED" in out and "batch-1-renamed.md" in out, out


@needs_git
def test_check_v_deleted_taken_file_is_red(tree, cli):
    fetch_origin(tree)
    (tree / B1).unlink()
    code, out = v_check(tree, cli)
    assert code == 2 and "(в) frozen: RED" in out and "file of a taken batch was removed" in out and "batch-1-foundation.md" in out, out


@needs_git
def test_check_v_status_only_moves_forward(tree, cli):
    fetch_origin(tree)
    edit(tree, B1, "статус: в работе", "статус: ожидает")
    edit(tree, CARD, ROW1_LINE, "| 1 | фундамент | B-230 | L | ожидает | Ира | `main` (x) | — |")
    code, out = v_check(tree, cli)
    assert code == 2 and 'the status moved back from "в работе"' in out and "only goes forward" in out, out


@needs_git
def test_check_v_card_row_is_frozen_except_status_and_mr(tree, cli):
    fetch_origin(tree)
    for old, new, col in (("B-230 | L", "B-230, B-015 | L", "Строки"), ("| Ира | `main` (x)", "| Катя | `main` (x)", "Взял"),
                          ("`main` (x) | —", "`pile/forge/batch-1` | —", "Ветка"), ("фундамент | B-230", "другое | B-230", "Что"),
                          ("| L | в работе", "| XL | в работе", "Размер")):
        put(tree, CARD, card_text("forge", "Forge", [ROW1, ROW2]))
        edit(tree, CARD, old, new)
        code, out = v_check(tree, cli)
        assert code == 2 and "(в) frozen: RED" in out and "column %s changed" % col in out, (col, out)
    put(tree, CARD, card_text("forge", "Forge", [ROW1, ROW2]))
    edit(tree, CARD, ROW1_LINE, "| 1 | фундамент | B-230 | L | в работе | Ира | `main` (x) | `abc1234` |")
    assert v_check(tree, cli)[0] == 0                                        # MR may change (Статус: see the allowed-areas test)


@needs_git
def test_check_v_card_row_status_only_moves_forward(tree, cli):
    fetch_origin(tree)
    edit(tree, CARD, "| L | в работе | Ира", "| L | ожидает | Ира")             # m-1 (t-593): backwards, named by its row
    code, out = v_check(tree, cli)
    assert code == 2 and "(в) frozen: RED" in out and "row 1, column Статус moved back" in out and 'to "ожидает"' in out, out
    put(tree, CARD, card_text("forge", "Forge", [ROW1, ROW2]))                # forwards, together with the file: green
    edit(tree, B1, "статус: в работе", "статус: сдано")
    edit(tree, CARD, "| L | в работе | Ира", "| L | сдано | Ира")
    code, out = v_check(tree, cli)
    assert code == 0 and "(в) frozen: ok" in out, out


@needs_git
def test_check_v_queue_lines_only_grow(tree, cli):
    edit(tree, B1, "Правило готовности.\n", "Правило готовности.\nочередь: forge/1 → forge/2\n")
    commit(tree, "queue line")
    fetch_origin(tree)
    edit(tree, B1, "очередь: forge/1 → forge/2\n", "")
    code, out = v_check(tree, cli)
    assert code == 2 and 'queue line "очередь: forge/1 → forge/2"' in out and "was deleted" in out, out


@needs_git
def test_check_v_origin_missing_warns_not_silent(tree, cli):
    edit(tree, B1, "`tools/a.py`", "`tools/z.py`")
    code, out = v_check(tree, cli)
    assert code == 0 and "(в) NOT CHECKED frozen -- origin/main is not available here" in out, out
    assert "git fetch origin" in out and "not blocked by (в)" in out


@needs_git
def test_check_v_door_and_merge_in_progress(tree, cli):
    fetch_origin(tree)
    edit(tree, B1, "`tools/a.py`", "`tools/z.py`")
    stage(tree, "plans/piles")
    code, out = cli(tree, "check", "--msg-file", msg(tree, "s\n\npiles-skip: в -- handover of the batch\n"))
    assert code == 0 and "(в) frozen: RED, passed by the commit message: piles-skip: в -- handover" in out, out
    assert cli(tree, "check", "--msg-file", msg(tree, "s\n\npiles-skip: д -- wrong item\n"))[0] == 2
    (tree / ".git" / "MERGE_HEAD").write_text(git(tree, "rev-parse", "HEAD").strip() + "\n")      # m8
    code, out = cli(tree, "check")
    assert code == 2 and "(в)" in out and "a merge is in progress" in out and "git commit" in out


# ---- `check --all --base <rev>` (t-601): the CI form of (в) -- the pushed range's base instead of origin/main ----

def two_commits(tree):
    """HEAD~1 holds the taken batch 1 as it was; HEAD holds a node row of it edited. origin/main := HEAD (CI: nothing ahead)."""
    edit(tree, B1, "| F0-1 | П1 | что | builder | `tools/a.py` |", "| F0-1 | П1 | что | builder | `tools/z.py` |")
    commit(tree, "edit a taken batch")
    fetch_origin(tree)
    return git(tree, "rev-parse", "--short=7", "HEAD~1").strip()


@needs_git
def test_check_all_base_compares_with_the_given_rev_where_no_flag_compares_a_tree_with_itself(tree, cli):
    short = two_commits(tree)
    code, out = cli(tree, "check", "--all")                                  # no flag: origin/main is HEAD, nothing to see
    assert code == 0 and "(в) frozen: ok" in out and "compared with origin/main " in out, out
    code, out = cli(tree, "check", "--all", "--base", "HEAD~1")              # the base: the edit is a change of a taken batch
    assert code == 2 and "(в) frozen: RED" in out and "differs from the --base %s" % short in out, out
    assert "compared with --base %s" % short in out and "origin/main %s" % short not in out, out
    assert "`tools/z.py`" in out and "batch-1-foundation.md" in out


@needs_git
def test_check_all_base_at_the_pre_edit_commit_by_sha_and_by_range(tree, cli):
    short = two_commits(tree)
    sha = git(tree, "rev-parse", "HEAD~1").strip()
    assert cli(tree, "check", "--all", "--base", sha)[0] == 2                # a full sha says the same as HEAD~1
    code, out = cli(tree, "check", "--all", "--base", "HEAD")                # base == HEAD, a clean tree: says so, passes
    assert code == 0 and "(в) frozen: ok" in out and "the base is HEAD itself" in out, out
    assert "compared with --base " + git(tree, "rev-parse", "--short=7", "HEAD").strip() in out and short not in out


@needs_git
def test_check_all_base_equal_to_head_still_judges_the_working_tree(tree, cli):
    # the invariant of the HEAD == base branch: an uncommitted change to a taken batch never passes for "nothing to compare"
    two_commits(tree)
    code, out = cli(tree, "check", "--all", "--base", "HEAD")
    assert code == 0, out
    edit(tree, B1, "Правило готовности.", "Правило готовности. Дописано.")
    code, out = cli(tree, "check", "--all", "--base", "HEAD")
    assert code == 2 and "(в) frozen: RED" in out and "the base is HEAD itself" in out, out


@needs_git
@pytest.mark.parametrize("rev", ["no-such-rev", "HEAD~9", "0000000000000000000000000000000000000000"])
def test_check_all_base_unknown_rev_cannot_run_and_names_the_rev_and_the_door(tree, cli, rev):
    two_commits(tree)
    code, out = cli(tree, "check", "--all", "--base", rev)
    assert code == 1, out                                                    # CannotRun, not a pass and not a red
    assert repr(rev) in out and "--base <rev>" in out and "no flag" in out and "origin/main" in out, out
    assert "(в) frozen" not in out and "piles check: ok" not in out          # nothing was judged before the refusal


@needs_git
def test_check_all_without_base_keeps_origin_main_and_its_not_checked_door(tree, cli):
    # no origin/main here and no flag: NOT CHECKED, naming "git fetch origin" (the old behaviour is unchanged)
    code, out = cli(tree, "check", "--all")
    assert code == 0 and "(в) NOT CHECKED frozen -- origin/main is not available here" in out and "git fetch origin" in out, out
    # the same tree with --base HEAD: the flag gives (в) something to compare with, so it is judged (and prints which base)
    code, out = cli(tree, "check", "--all", "--base", "HEAD")
    assert code == 0 and "(в) frozen: ok" in out and "NOT CHECKED frozen" not in out, out


# ---- doors in the pushed range (t-604, finding F-1 of t-603): `check --base <rev>` reads `piles-skip:` from <rev>..HEAD ----

KEYS = {"а": "placement", "б": "overlap", "в": "frozen", "г": "backlog", "д": "form"}


def _make_red(tree, item):
    """Leave the tree with item `item` red (uncommitted)."""
    if item == "а":
        dup_finding(tree)
    elif item == "б":
        edit(tree, CARD, "| 2 | потом | B-015 | M | ожидает | — | — | — |", "| 2 | потом | B-015 | M | в работе | Катя | `pile/forge/batch-2` | — |")
        put(tree, B2, batch_text("forge", 2, "в работе", [node("F0-3", "`tools/a.py`")], who="Катя", branch="`pile/forge/batch-2`"))
    elif item == "в":
        edit(tree, B1, "| F0-1 | П1 | что | builder | `tools/a.py` |", "| F0-1 | П1 | что | builder | `tools/z.py` |")
    elif item == "г":
        edit(tree, "plans/BACKLOG.md", "| B-308 |", "| B-500 | **Новая.** | п | и | п |\n| B-308 |")
        put(tree, "plans/piles/forge/findings/B-500-x.md", finding_text("B-500"))      # placed: only (г) objects
    else:
        batch2(tree, writes="—")


def _red_range(tree, item, message, door_before=None):
    """HEAD~1 = the base; HEAD = the commit that makes `item` red, with `message`. `door_before`: the message of the base commit."""
    if item == "г":
        freeze(tree)
    if door_before is not None:
        git(tree, "commit", "-q", "--allow-empty", "-m", door_before)
    _make_red(tree, item)
    commit(tree, message)


def _passed(out, item):
    return "(%s) %s: RED, passed by the commit message" % (item, KEYS[item]) in out


@needs_git
@pytest.mark.parametrize("item", list(KEYS))
def test_check_all_base_reads_the_door_of_the_range_for_every_item(tree, cli, item):
    _red_range(tree, item, "s\n\npiles-skip: %s -- the push does it on purpose\n" % item)
    code, out = cli(tree, "check", "--all", "--base", "HEAD~1")
    assert code == 0 and _passed(out, item), out                              # a door in the range passes the item it names
    assert "read from the 1 commit message(s) of" in out, out
    assert not any(_passed(out, other) for other in KEYS if other != item), out


@needs_git
@pytest.mark.parametrize("item", list(KEYS))
def test_check_all_base_without_a_door_in_the_range_stays_red(tree, cli, item):
    # the door of the commit BEFORE the base is outside the range; a door for another item passes nothing
    _red_range(tree, item, "s\n\npiles-skip: %s -- wrong item\n" % next(i for i in KEYS if i != item),
               door_before="before the base\n\npiles-skip: %s -- outside the range\n" % item)
    code, out = cli(tree, "check", "--all", "--base", "HEAD~1")
    assert code == 2 and "(%s) %s: RED" % (item, KEYS[item]) in out and not _passed(out, item), out


@needs_git
def test_check_all_base_empty_range_reads_no_door_and_says_so(tree, cli):
    _red_range(tree, "а", "s\n\npiles-skip: а -- in the head commit\n")
    code, out = cli(tree, "check", "--all", "--base", "HEAD")                 # <rev> == HEAD: the head commit is not in the range
    assert code == 2 and "empty range" in out and "no piles-skip door from the range" in out and not _passed(out, "а"), out


@needs_git
def test_check_all_base_unreadable_log_warns_and_counts_no_door(tree, cli, monkeypatch):
    _red_range(tree, "а", "s\n\npiles-skip: а -- the push does it on purpose\n")
    real = piles.gitcmd.git

    def failing_log(root, *args, **kw):
        return (128, b"fatal: broken log") if args and args[0] == "log" else real(root, *args, **kw)
    monkeypatch.setattr(piles.gitcmd, "git", failing_log)
    code, out = cli(tree, "check", "--all", "--base", "HEAD~1")
    assert code == 2 and "WARN: cannot read the commit messages" in out and "fatal: broken log" in out and not _passed(out, "а"), out


@needs_git
def test_check_all_base_merges_the_message_file_with_the_range(tree, cli):
    dup_finding(tree)                                                         # (а) red, committed in the range
    _make_red(tree, "в")                                                      # (в) red, in the same commit
    commit(tree, "s\n\npiles-skip: в -- the range door\n")
    assert cli(tree, "check", "--all", "--base", "HEAD~1")[0] == 2            # the range names (в) only
    assert cli(tree, "check", "--all", "--base", "HEAD~1", "--msg-file", msg(tree, "s\n\npiles-skip: д -- wrong\n"))[0] == 2
    code, out = cli(tree, "check", "--all", "--base", "HEAD~1", "--msg-file", msg(tree, "s\n\npiles-skip: а -- the file door\n"))
    assert code == 0 and _passed(out, "а") and _passed(out, "в"), out


@needs_git
def test_check_all_base_a_fenced_door_is_no_door_and_a_broken_fence_does_not_close_the_next_one(tree, cli):
    _red_range(tree, "а", "s\n\n```\npiles-skip: а -- in a fence\n```\n")
    code, out = cli(tree, "check", "--all", "--base", "HEAD~1")
    assert code == 2 and not _passed(out, "а"), out                           # the existing regex and scanner rules are unchanged
    git(tree, "commit", "-q", "--allow-empty", "-m", "an unbalanced fence\n\n```\nnever closed\n")
    git(tree, "commit", "-q", "--allow-empty", "-m", "the door\n\npiles-skip: а -- after a broken fence\n")
    code, out = cli(tree, "check", "--all", "--base", "HEAD~3")
    assert code == 0 and _passed(out, "а") and "3 commit message(s)" in out, out
