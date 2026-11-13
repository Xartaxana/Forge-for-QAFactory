"""Tests for tools/piles.py: `take`.

Part of the split of the old tools/test_piles.py (t-596, the 120 s cap per file): the helpers are in
tools/piles_testkit.py, the fixtures `session_tree`, `tree`, `cli` in tools/conftest.py.
Run from the repo root: python -m pytest tools/test_piles_take.py -q
"""
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import piles  # noqa: E402
from piles_testkit import _no_network, GIT_VARS, git, put, batch_text, B1, B2, CARD, needs_git, edit, rd, batch2, tree_state  # noqa: E402


@pytest.fixture(autouse=True)
def _scrub_git_env(monkeypatch):
    for k in GIT_VARS:
        monkeypatch.delenv(k, raising=False)
    monkeypatch.delenv("GITLAB_TOKEN", raising=False)         # the default world has no token
    monkeypatch.delenv("QA_DEV_CONFIG", raising=False)


# ---------------------------------------------------------------- take

def take_tree(tree):
    batch2(tree)
    git(tree, "branch", "-M", "main")


@needs_git
def test_take_sets_card_and_batch_and_prints_commands(tree, cli):
    take_tree(tree)
    old = {p: rd(tree, p).split("\n") for p in (CARD, B2)}
    code, out = cli(tree, "take", "forge", "2", "--who", "dev1", "--today", "2026-10-08")
    assert code == 0, out
    assert "piles take: forge/2 taken by dev1 (08.10.2026). Next:" in out
    assert "git switch -c pile/forge/batch-2 origin/main" in out and "git add plans/piles/forge/README.md" in out and "WARNING" not in out
    for p, before in old.items():
        after = rd(tree, p).split("\n")
        assert len(after) == len(before) and len([1 for a, b in zip(before, after) if a != b]) == 1   # one line, nothing else
    row = next(l for l in rd(tree, CARD).split("\n") if l.startswith("| 2 |"))
    assert row == "| 2 | потом | B-015 | M | в работе | dev1, 08.10.2026 | `pile/forge/batch-2` | — |"
    head = next(l for l in rd(tree, B2).split("\n") if l.startswith("кучка:"))
    assert head == "кучка: `forge` | статус: в работе | взял: dev1, 08.10.2026 | ветка: `pile/forge/batch-2` | MR: — | стенд: не нужен"
    assert "PILES.md" not in out                                              # the printed `git add` names no board
    assert cli(tree, "check", "--all")[0] == 0                                # and the result passes the gate


@needs_git
def test_take_that_fails_after_the_card_write_puts_both_files_back(tree, cli, monkeypatch):
    take_tree(tree)
    snap = tree_state(tree)                                                   # sha256 of every file under plans/
    real_write, calls = piles.write_like, []

    def failing_write(path, text, form):
        calls.append(path)
        if len(calls) == 2:                                                   # the card is already written
            raise OSError("disk full")
        return real_write(path, text, form)

    monkeypatch.setattr(piles, "write_like", failing_write)
    code, out = cli(tree, "take", "forge", "2", "--who", "dev1", "--today", "2026-10-08")
    assert code == 1 and "every file touched was put back, nothing changed" in out, out
    assert tree_state(tree) == snap                                           # card and batch: the same bytes


@needs_git
def test_take_same_who_idempotent_other_who_refused(tree, cli):
    take_tree(tree)
    cli(tree, "take", "forge", "2", "--who", "dev1", "--today", "2026-10-08")
    snap = (rd(tree, CARD), rd(tree, B2))
    code, out = cli(tree, "take", "forge", "2", "--who", "dev1", "--today", "2026-10-09")
    assert code == 0 and "forge/2 is already taken by dev1; nothing changed" in out
    code, out = cli(tree, "take", "forge", "2", "--who", "dev2")
    assert code == 2 and "already taken by dev1, 08.10.2026" in out and 'status "в работе"' in out and "a batch has one taker" in out
    assert (rd(tree, CARD), rd(tree, B2)) == snap
    assert "already taken by Ира" in cli(tree, "take", "forge", "1", "--who", "dev2")[1]    # the real taker of batch 1


@needs_git
def test_take_card_batch_disagree_refused(tree, cli):
    take_tree(tree)
    edit(tree, CARD, "| 2 | потом | B-015 | M | ожидает", "| 2 | потом | B-015 | M | в работе")
    code, out = cli(tree, "take", "forge", "2", "--who", "dev1")
    assert code == 2 and 'the card and the batch file disagree on forge/2: card status "в работе", batch status "ожидает"' in out


@needs_git
def test_take_missing_batch_file_or_no_nodes_refused(tree, cli):
    code, out = cli(tree, "take", "forge", "2", "--who", "dev1")
    assert code == 2 and "no batch file for forge/2" in out and "_template/batch.md" in out
    put(tree, B2, batch_text("forge", 2, "ожидает", [], who="—", branch="—"))
    code, out = cli(tree, "take", "forge", "2", "--who", "dev1")
    assert code == 2 and "forge/2 has no nodes" in out and "## Узлы" in out
    assert "no batch row 7" in cli(tree, "take", "forge", "7", "--who", "x")[1]


@needs_git
@pytest.mark.parametrize("who,ok", [("М", True), ("м" * 40, True), ("м" * 41, False), ("", False), ("   ", False), ("a|b", False),
                                     ("a\nb", False), ("a\x00b", False), ("dev1 two", True),
                                     ("a`b", False), ("`", False)])           # m-2: a backtick unbalances the cell/pair split
def test_take_who_battery(tree, cli, who, ok):
    take_tree(tree)
    before = rd(tree, CARD)
    code, out = cli(tree, "take", "forge", "2", "--who", who)
    if ok:
        assert code == 0, out
    else:
        assert code == 2 and "--who: expected 1-40 characters" in out and rd(tree, CARD) == before


@needs_git
@pytest.mark.parametrize("n,needle", [("0", "N must be a whole number 1-999"), ("1000", "N must be a whole number 1-999"),
                                       ("x", 'got "x"'), ("999", "no batch row 999"), ("1", "already taken by Ира")])
def test_take_n_battery(tree, cli, n, needle):
    code, out = cli(tree, "take", "forge", n, "--who", "dev1")
    assert code == 2 and needle in out, out


@needs_git
@pytest.mark.parametrize("slug", ["../x", "nope", "_template", "Forge", "forge/x"])
def test_take_slug_battery(tree, cli, slug):
    code, out = cli(tree, "take", slug, "2", "--who", "dev1")
    assert code == 2 and 'no pile "%s"' % slug in out and "piles with a card: forge, report-delivery" in out, out


@needs_git
def test_take_preserves_crlf_and_bom(tree, cli):
    take_tree(tree)
    for rel, bom in ((CARD, False), (B2, True)):
        raw = (tree / rel).read_bytes().replace(b"\n", b"\r\n")
        (tree / rel).write_bytes((b"\xef\xbb\xbf" if bom else b"") + raw)
    assert cli(tree, "take", "forge", "2", "--who", "dev1", "--today", "2026-10-08")[0] == 0
    card, batch = (tree / CARD).read_bytes(), (tree / B2).read_bytes()
    assert b"\n" not in card.replace(b"\r\n", b"") and b"\n" not in batch.replace(b"\r\n", b"")
    assert batch.startswith(b"\xef\xbb\xbf") and not card.startswith(b"\xef\xbb\xbf")
    assert "dev1, 08.10.2026" in card.decode("utf-8")


@needs_git
def test_take_warns_off_main(tree, cli):
    take_tree(tree)
    git(tree, "checkout", "-q", "-b", "side")
    code, out = cli(tree, "take", "forge", "2", "--who", "dev1")
    assert code == 0 and "WARNING: the current branch is side, not main" in out


def test_take_without_git_says_branch_unknown(tree, cli):
    batch2(tree)
    code, out = cli(tree, "take", "forge", "2", "--who", "dev1")
    assert code == 0 and "WARNING: the current branch is unknown" in out


@needs_git
def test_take_runs_overlap_first_and_names_the_queue_door(tree, cli):
    batch2(tree, writes="`tools/a.py`")                                        # batch 1 (в работе) writes tools/a.py
    git(tree, "branch", "-M", "main")
    before = (rd(tree, CARD), rd(tree, B2))
    code, out = cli(tree, "take", "forge", "2", "--who", "dev1")
    assert code == 2 and "forge/1 and forge/2 both write: tools/a.py" in out and "очередь: forge/1 → forge/2" in out, out
    assert "piles-skip: б" in out and (rd(tree, CARD), rd(tree, B2)) == before
    edit(tree, B1, "Правило готовности.\n", "Правило готовности.\nочередь: forge/1 → forge/2\n")     # the door: BOTH preambles say it
    batch2(tree, writes="`tools/a.py`", pre="\nочередь: forge/1 → forge/2\n")
    assert cli(tree, "take", "forge", "2", "--who", "dev1")[0] == 0


@needs_git
@pytest.mark.parametrize("holder,config,code,needles,absent", [
    ("dev1, 12.11.2026", "developer: dev1\n", 0, ("piles take: forge/2 taken by dev1",), ("WARNING: --who",)),
    ("dev2, 12.11.2026", None, 2, ("forge/1 and forge/2 both write: tools/a.py",), ()),
    ("dev1, 12.11.2026", "developer: dev2\n", 0,
     ("WARNING: --who reads as developer dev1, but this clone's tools/dev.config.yaml names dev2",), ()),
    ("dev1, 12.11.2026", None, 0, ("piles take: forge/2 taken by dev1",), ("WARNING: --who",)),
], ids=["take-passes-own-overlaps", "take-refused-other-developer", "take-warns-who-differs-from-clone",
        "take-no-warning-without-dev-config"])
def test_take_by_developer(tree, cli, holder, config, code, needles, absent):
    """D.3: batch 1 (в работе, writes tools/a.py) belongs to `holder`; batch 2 (writes the same file) is taken with --who dev1."""
    batch2(tree, writes="`tools/a.py`")
    git(tree, "branch", "-M", "main")
    for who in ("dev1", "dev2"):
        put(tree, "logs/journal/%s.jsonl" % who, "{}\n")
    edit(tree, B1, "взял: Ира", "взял: " + holder)
    edit(tree, CARD, "| в работе | Ира |", "| в работе | %s |" % holder)
    if config:
        put(tree, "tools/dev.config.yaml", config)
    git(tree, "add", "-A")
    got, out = cli(tree, "take", "forge", "2", "--who", "dev1")
    assert got == code and all(n in out for n in needles) and not any(a in out for a in absent), out


@needs_git
@pytest.mark.parametrize("kind,tracked,code,needle", [
    ("foreign-broken", False, 0, "piles take: forge/2 taken by dev1"),
    ("foreign-active-overlap", False, 0, "piles take: forge/2 taken by dev1"),
    ("own-pile-broken", False, 1, "20261009-bad.md"),
    ("foreign-broken", True, 1, "report-delivery/batch-1-x.md"),                 # control: the same file COMMITTED is read, strictly
    ("foreign-active-overlap", True, 2, "report-delivery/1 and forge/2 both write"),   # control: a tracked active batch still holds its zone
], ids=["foreign-untracked-broken-batch", "foreign-untracked-active-overlap", "own-pile-untracked-broken",
        "foreign-tracked-broken-batch", "foreign-tracked-active-overlap"])
def test_take_reads_untracked_like_check(tree, cli, kind, tracked, code, needle):
    """B.9 (t-367 N4): the untracked files of OTHER piles are another session's -- `take` does not read them; the pile it writes is
    read whole; what is committed is read strictly, as before."""
    take_tree(tree)
    rel = "plans/piles/report-delivery/batch-1-x.md"
    if kind == "foreign-broken":
        put(tree, rel, batch_text("report-delivery", 1, "ожидает", [["R1-1", "П1", "что", "builder", "`tools/z.py`", "—", "ожидает"]],
                                  who="—", branch="—") + "\n```\nnever closed\n")
    elif kind == "foreign-active-overlap":
        put(tree, rel, batch_text("report-delivery", 1, "в работе", [["R1-1", "П1", "что", "builder", "`tools/b.py`", "—", "в работе"]]))
    else:
        (tree / "plans/piles/forge/findings").mkdir(parents=True, exist_ok=True)
        (tree / "plans/piles/forge/findings/20261009-bad.md").write_bytes(b"# t\n\n\xff\xfe not utf-8\n")
    if tracked:
        git(tree, "add", "-A", "--", "plans/piles/report-delivery")
        git(tree, "commit", "-q", "-m", "a foreign batch")
    got, out = cli(tree, "take", "forge", "2", "--who", "dev1", "--today", "2026-11-13")
    assert got == code and needle in out, out


# ---------------------------------------------------------------- GM1-1: take touches files only, no board

@needs_git
@pytest.mark.parametrize("token", [None, "glpat-secret-value"])
def test_take_writes_no_board_line_with_or_without_token(tree, cli, monkeypatch, token):
    take_tree(tree)
    _no_network(monkeypatch)
    if token:
        monkeypatch.setenv("GITLAB_TOKEN", token)
    code, out = cli(tree, "take", "forge", "2", "--who", "dev1", "--today", "2026-10-08")
    assert code == 0, out
    assert "piles take: forge/2 taken by dev1 (08.10.2026). Next:" in out
    assert "доска" not in out and "board" not in out and "PILES.md" not in out and "issue" not in out and "glpat" not in out
    assert "issue:" not in rd(tree, B2) and "| в работе | dev1, 08.10.2026 |" in rd(tree, CARD)


@needs_git
def test_take_runs_with_no_piles_gitlab_module(tree, cli, monkeypatch):
    take_tree(tree)
    monkeypatch.setitem(sys.modules, "piles_gitlab", None)                     # an import of it raises ImportError
    _no_network(monkeypatch)
    code, out = cli(tree, "take", "forge", "2", "--who", "dev1", "--today", "2026-10-08")
    assert code == 0 and "доска" not in out and "taken by dev1" in out, out
    assert cli(tree, "check", "--all")[0] == 0


@needs_git
def test_take_passes_a_batch_whose_header_carries_an_old_issue_line(tree, cli):
    take_tree(tree)
    assert cli(tree, "take", "forge", "2", "--who", "dev1", "--today", "2026-10-08")[0] == 0
    head = next(l for l in rd(tree, B2).split("\n") if l.startswith("кучка:"))
    edit(tree, B2, head, head + " | issue: https://example.invalid/issues/7")
    assert cli(tree, "check", "--all")[0] == 0                                  # an old `issue:` is neither content nor red
    code, out = cli(tree, "take", "forge", "2", "--who", "dev1")
    assert code == 0 and "nothing changed" in out and "issue: https://example.invalid/issues/7" in rd(tree, B2)


@needs_git
def test_take_that_changes_nothing_or_is_refused_prints_no_board_word(tree, cli):
    take_tree(tree)
    assert cli(tree, "take", "forge", "2", "--who", "dev1", "--today", "2026-10-08")[0] == 0
    code, out = cli(tree, "take", "forge", "2", "--who", "dev1")              # idempotent: no write
    assert code == 0 and "nothing changed" in out and "доска" not in out
    code, out = cli(tree, "take", "forge", "1", "--who", "dev2")               # refused
    assert code == 2 and "доска" not in out


@needs_git
def test_take_that_fails_and_is_rolled_back_prints_no_board_word(tree, cli, monkeypatch):
    take_tree(tree)

    def failing_write(path, text, form):
        raise OSError("disk full")
    monkeypatch.setattr(piles, "write_like", failing_write)
    code, out = cli(tree, "take", "forge", "2", "--who", "dev1")
    assert code == 1 and "доска" not in out
