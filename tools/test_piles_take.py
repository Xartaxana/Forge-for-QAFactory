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
from piles_testkit import (_no_network, GIT_VARS, git, put, batch_text, B1, B2, CARD, needs_git, edit, rd, batch2, tree_state,  # noqa: E402
                           PROOF_DONE, commit, fetch_origin, head_hash, node as mk_node)


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


# ---------------------------------------------------------------- status (SL-3, t-356): the one writer of сдано / принято

def status_world(tree, cli, kind):
    """Batch 2 of the mini tree in the state `kind`; the hash used is HEAD's short hash (nothing here moves HEAD)."""
    h = head_hash(tree, short=True)
    rows = {"taken": ["ожидает"], "submitted-node": ["сдано"], "accepted-node": ["принято: %s (t-1)" % h],
            "open-nodes": ["принято", "сдано"], "all-done": ["принято", "отклонено"], "dup": ["ожидает", "ожидает"],
            "batch-accepted-fully": ["принято", "отклонено"]}.get(kind, ["ожидает"])
    ids = ["F0-3 + F0-4"] if kind == "two-ids" else ["F0-3", "F0-3"] if kind == "dup" else ["F0-3", "F0-4"]
    nodes = [mk_node(i, "`tools/%s.py`" % "bc"[k], s) for k, (i, s) in enumerate(zip(ids, rows * 2))]
    put(tree, B2, batch_text("forge", 2, "ожидает", nodes, who="—", branch="—", proof=PROOF_DONE))
    git(tree, "branch", "-M", "main")
    if kind == "closed":
        edit(tree, CARD, "| M | ожидает", "| M | закрыта")
        edit(tree, B2, "статус: ожидает", "статус: закрыта")
    if kind != "untaken" and kind != "closed":
        assert cli(tree, "take", "forge", "2", "--who", "dev1", "--today", "2026-10-08")[0] == 0
    if kind == "card-disagrees":
        edit(tree, CARD, "| M | в работе", "| M | сдано")
    if kind in ("batch-submitted", "batch-accepted", "batch-accepted-fully"):
        assert cli(tree, "status", "forge", "2", "--set", "сдано")[0] == 0
    if kind == "batch-accepted-fully":
        assert cli(tree, "status", "forge", "2", "--set", "принято")[0] == 0
    return h


def changed_lines(tree, before):
    """{path: how many lines differ} of the card and batch 2 against `before`; -1 when the line count moved."""
    out = {}
    for rel in (CARD, B2):
        a, b = before[rel].split("\n"), rd(tree, rel).split("\n")
        out[rel] = sum(x != y for x, y in zip(a, b)) if len(a) == len(b) else -1
    return out


NODE_SET = ("F0-3", "--set")
STATUS_ROWS = [
    # id, world, args ("{h}" = the world's hash), exit code, needles of the output, writes (none / node / batch), the cell written
    ("unknown-node", "taken", ("F9-9", "--set", "сдано"), 2, ('no node "F9-9" in forge/2', "expected one of its node ids: F0-3, F0-4"), "none", ""),
    ("two-ids-row", "two-ids", (*NODE_SET, "сдано"), 2, ("names more than one id", "one row, one id", "masked by (в)"), "none", ""),
    ("duplicate-id-rows", "dup", (*NODE_SET, "сдано"), 2, ("the id F0-3 heads 2 rows of forge/2", "one row, one id"), "none", ""),
    ("backwards", "submitted-node", (*NODE_SET, "в работе"), 2, ('is "сдано" -- a status only goes forward', "edit the cell by hand"), "none", ""),
    ("accepted-then-rejected", "accepted-node", (*NODE_SET, "отклонено"), 2, ("and final", "writes nothing any more", "edit the cell by hand"), "none", ""),
    ("same-again", "submitted-node", (*NODE_SET, "сдано"), 0, ("forge/2 F0-3 is already сдано; nothing changed",), "none", ""),
    ("accepted-other-hash", "accepted-node", (*NODE_SET, "принято", "--hash", "{h}", "--task", "t-2"), 2, ('already accepted with "принято: {h} (t-1)"',), "none", ""),
    ("accepted-same-again", "accepted-node", (*NODE_SET, "принято", "--hash", "{h}", "--task", "t-1"), 0, ("is already принято; nothing changed",), "none", ""),
    ("accepted-no-evidence", "taken", (*NODE_SET, "принято"), 2, ("expected --hash <merge commit> and/or --task t-NNN",), "none", ""),
    ("accepted-hash", "taken", (*NODE_SET, "принято", "--hash", "{h}"), 0, ("set to принято: {h}. Next:",), "node", "принято: {h}"),
    ("accepted-task", "taken", (*NODE_SET, "принято", "--task", "t-415"), 0, ("set to принято (t-415)",), "node", "принято (t-415)"),
    ("accepted-both", "taken", (*NODE_SET, "принято", "--hash", "{h}", "--task", "t-415"), 0, ("set to принято: {h} (t-415)",), "node", "принято: {h} (t-415)"),
    ("node-in-work", "untaken", (*NODE_SET, "в работе"), 0, ('git commit -m "piles: status forge/2 F0-3 в работе"',), "node", "в работе"),
    ("node-rejected", "taken", (*NODE_SET, "отклонено"), 0, ("set to отклонено",), "node", "отклонено"),
    ("batch-accepted-open-node", "open-nodes", ("--set", "принято"), 2, ("cannot be accepted while its node(s) F0-4 are neither принято nor отклонено", "status forge 2 <node-id>"), "none", ""),
    ("batch-accepted-all-done", "all-done", ("--set", "принято"), 0, ("forge/2 set to принято",), "batch", "принято"),
    ("batch-submitted", "taken", ("--set", "сдано"), 0, ("git add plans/piles/forge/README.md plans/piles/forge/batch-2-next.md",
                                                         'git commit -m "piles: status forge/2 сдано"'), "batch", "сдано"),
    ("batch-submitted-again", "batch-submitted", ("--set", "сдано"), 0, ("forge/2 is already сдано; nothing changed",), "none", ""),
    ("batch-accepted-open-after-submit", "batch-accepted", ("--set", "принято"), 2, ("cannot be accepted while its node(s)",), "none", ""),
    ("batch-backwards", "batch-accepted-fully", ("--set", "сдано"), 2, ('is "принято" -- a status only goes forward', 'piles-skip: в -- <reason>'), "none", ""),
    ("batch-accepted-again", "batch-accepted-fully", ("--set", "принято"), 0, ("forge/2 is already принято; nothing changed",), "none", ""),
    ("batch-untaken", "untaken", ("--set", "сдано"), 2, ('forge/2 is "ожидает" -- take it first', "take forge 2 --who"), "none", ""),
    ("node-in-untaken-batch", "untaken", (*NODE_SET, "сдано"), 0, ("forge/2 F0-3 set to сдано",), "node", "сдано"),
    ("closed-batch", "closed", ("--set", "принято"), 2, ('forge/2 is "закрыта"',), "none", ""),
    ("closed-batch-node", "closed", (*NODE_SET, "сдано"), 2, ('forge/2 is "закрыта"',), "none", ""),
    ("card-disagrees", "card-disagrees", ("--set", "сдано"), 2, ('the card and the batch file disagree on forge/2: card status "сдано", batch status "в работе"',), "none", ""),
    ("bad-hash", "taken", (*NODE_SET, "принято", "--hash", "xyz1234"), 2, ('--hash "xyz1234": expected a commit hash (7-40 hex characters)',), "none", ""),
    ("bad-hash-empty", "taken", (*NODE_SET, "принято", "--hash", ""), 2, ("expected a commit hash",), "none", ""),
    ("bad-hash-not-a-commit", "taken", (*NODE_SET, "принято", "--hash", "deadbee"), 2, ("deadbee is not a commit in this repository",), "none", ""),
    ("bad-task-magnitude", "taken", (*NODE_SET, "принято", "--task", "t-1234567"), 2, ("expected a task id t-NNN (1-6 digits)",), "none", ""),
    ("bad-task-empty", "taken", (*NODE_SET, "принято", "--task", ""), 2, ("expected a task id t-NNN",), "none", ""),
    ("bad-task-pipe", "taken", (*NODE_SET, "принято", "--task", "t-1|x"), 2, ("expected a task id t-NNN",), "none", ""),
    ("bad-task-case", "taken", (*NODE_SET, "принято", "--task", "T-1"), 2, ("expected a task id t-NNN",), "none", ""),
    ("evidence-with-other-word", "taken", (*NODE_SET, "сдано", "--task", "t-1"), 2, ("--hash and --task go with a node set to принято",), "none", ""),
    ("evidence-at-batch-level", "taken", ("--set", "сдано", "--hash", "{h}"), 2, ("--hash and --task go with a node set to принято",), "none", ""),
    ("word-in-another-case", "taken", (*NODE_SET, "ПРИНЯТО", "--task", "t-9"), 0, ("set to принято (t-9)",), "node", "принято (t-9)"),
    ("word-with-extra-spaces", "taken", (*NODE_SET, "  В   работе "), 0, ("set to в работе",), "node", "в работе"),
    ("word-unknown", "taken", (*NODE_SET, "готово"), 2, ('--set "готово": expected one of в работе, сдано, принято, отклонено for a node',), "none", ""),
    ("word-waiting-on-a-node", "taken", (*NODE_SET, "ожидает"), 2, ("expected one of в работе, сдано, принято, отклонено for a node",), "none", ""),
    ("word-empty", "taken", (*NODE_SET, ""), 2, ('--set "": expected one of',), "none", ""),
    ("batch-word-v-rabote", "taken", ("--set", "в работе"), 2, ("expected сдано or принято for a batch", "`в работе` is written by `take`"), "none", ""),
    ("batch-word-closed", "taken", ("--set", "закрыта"), 2, ("`закрыта` is written by `close`",), "none", ""),
    ("batch-word-rejected", "taken", ("--set", "отклонено"), 2, ("expected сдано or принято for a batch", "give its id"), "none", ""),
    ("node-id-pipe", "taken", ("F0|3", "--set", "сдано"), 2, ('node id "F0|3": expected 1-40 characters without spaces',), "none", ""),
    ("node-id-newline", "taken", ("F0-3\nx", "--set", "сдано"), 2, ("node id", "without spaces"), "none", ""),
    ("node-id-empty", "taken", ("", "--set", "сдано"), 2, ('node id "": expected 1-40 characters',), "none", ""),
    ("node-id-spaced", "taken", ("F0 3", "--set", "сдано"), 2, ("node id", "without spaces"), "none", ""),
    ("node-id-too-long", "taken", ("F" * 41, "--set", "сдано"), 2, ("node id", "expected 1-40 characters"), "none", ""),
]


@needs_git
@pytest.mark.parametrize("world,args,code,needles,writes,cell", [r[1:] for r in STATUS_ROWS], ids=[r[0] for r in STATUS_ROWS])
def test_status_edges(tree, cli, world, args, code, needles, writes, cell):
    """Spec SL-3 edges 1-11 and the adversarial rows: a refusal writes nothing; a write changes ONE line per target and no other byte."""
    h = status_world(tree, cli, world)
    before = {rel: rd(tree, rel) for rel in (CARD, B2)}
    state = tree_state(tree)
    got, out = cli(tree, "status", "forge", "2", *[a.replace("{h}", h) for a in args])
    assert got == code, out
    for needle in needles:
        assert needle.replace("{h}", h) in out, (needle, out)
    changed = changed_lines(tree, before)
    assert changed == {"none": {CARD: 0, B2: 0}, "node": {CARD: 0, B2: 1}, "batch": {CARD: 1, B2: 1}}[writes], (changed, out)
    if writes == "none":
        assert tree_state(tree) == state
        return
    cell = cell.replace("{h}", h)
    row = next(l for l, o in zip(rd(tree, B2).split("\n"), before[B2].split("\n")) if l != o)
    if writes == "node":
        assert row.endswith("| %s |" % cell) and row.startswith("| F0-3 |"), row
    else:
        card_row = next(l for l, o in zip(rd(tree, CARD).split("\n"), before[CARD].split("\n")) if l != o)
        assert "статус: %s |" % cell in row and row.startswith("кучка:") and "| %s |" % cell in card_row, (row, card_row)
    assert cli(tree, "check", "--all")[0] == 0                                  # the written tree still passes the whole gate


@needs_git
@pytest.mark.parametrize("slug,n,needle", [("../x", "2", 'no pile "../x"'), ("", "2", 'no pile ""'), ("forge/x", "2", 'no pile "forge/x"'),
                                            ("Forge", "2", 'no pile "Forge"'), ("nope", "2", 'no pile "nope"'),
                                            ("forge", "0", "N must be a whole number 1-999"), ("forge", "x", 'got "x"'),
                                            ("forge", "1000", "N must be a whole number 1-999"), ("forge", "-1", "N must be"),
                                            ("forge", "99", "no batch row 99")])
def test_status_slug_and_n_battery(tree, cli, slug, n, needle):
    status_world(tree, cli, "taken")
    state = tree_state(tree)
    code, out = cli(tree, "status", slug, n, "--set", "сдано")
    assert code == 2 and needle in out and tree_state(tree) == state, out


@needs_git
@pytest.mark.parametrize("kind,code,needle", [("unclosed-fence", 1, "never closed"), ("two-files-one-n", 2, "has 2 batch files"),
                                               ("missing-card", 2, "no pile")])
def test_status_refuses_unreadable_before_any_write(tree, cli, kind, code, needle):
    """Unreadable input (a fence nothing closes, two files with one N, a missing card): nothing is written, at either level."""
    status_world(tree, cli, "taken")
    if kind == "unclosed-fence":
        (tree / B2).write_bytes((tree / B2).read_bytes() + b"\n```\nnever closed\n")
    elif kind == "two-files-one-n":
        put(tree, "plans/piles/forge/batch-2-other.md", rd(tree, B2))
    else:
        (tree / CARD).unlink()
    state = tree_state(tree)
    for args in (("--set", "сдано"), ("F0-3", "--set", "сдано")):
        got, out = cli(tree, "status", "forge", "2", *args)
        assert got == code and needle in out and tree_state(tree) == state, out


@needs_git
def test_status_keeps_crlf_bom_and_passes_frozen(tree, cli):
    """Each write into a TAKEN batch (committed and on origin/main) keeps CRLF and BOM and leaves (в) green: it writes only what (в) masks."""
    status_world(tree, cli, "taken")
    for rel, bom in ((CARD, False), (B2, True)):
        raw = (tree / rel).read_bytes().replace(b"\n", b"\r\n")
        (tree / rel).write_bytes((b"\xef\xbb\xbf" if bom else b"") + raw)
    commit(tree, "taken")
    fetch_origin(tree)
    h = head_hash(tree, short=True)
    for args in (("F0-3", "--set", "в работе"), ("F0-3", "--set", "сдано"), ("F0-3", "--set", "принято", "--hash", h, "--task", "t-415"),
                 ("F0-4", "--set", "отклонено"), ("--set", "сдано"), ("--set", "принято")):
        code, out = cli(tree, "status", "forge", "2", *args)
        assert code == 0, (args, out)
        code, out = cli(tree, "check", "--all", "--base", "HEAD")
        assert code == 0 and "(в) frozen: ok" in out, (args, out)
    git(tree, "add", "-A", "--", CARD, B2)                                      # a commit of exactly these files, as the printed Next line says
    code, out = cli(tree, "check")
    assert code == 0 and "(в) frozen: ok" in out and out.rstrip().endswith("piles check: ok"), out
    card, batch = (tree / CARD).read_bytes(), (tree / B2).read_bytes()
    assert b"\n" not in card.replace(b"\r\n", b"") and b"\n" not in batch.replace(b"\r\n", b"")
    assert batch.startswith(b"\xef\xbb\xbf") and not card.startswith(b"\xef\xbb\xbf")
    assert "статус: принято |" in batch.decode("utf-8") and "| M | принято |" in card.decode("utf-8")


@needs_git
@pytest.mark.parametrize("level", ["batch", "node"])
def test_status_rollback_on_failed_write(tree, cli, monkeypatch, level):
    status_world(tree, cli, "taken")
    state = tree_state(tree)
    real_write, calls = piles.write_like, []

    def failing_write(path, text, form):
        calls.append(path)
        if len(calls) == 2 or level == "node":                                  # batch: the card is already written
            raise OSError("disk full")
        return real_write(path, text, form)

    monkeypatch.setattr(piles, "write_like", failing_write)
    args = ("--set", "сдано") if level == "batch" else ("F0-3", "--set", "сдано")
    code, out = cli(tree, "status", "forge", "2", *args)
    assert code == 1 and "every file touched was put back, nothing changed" in out, out
    assert tree_state(tree) == state


def test_status_order_is_the_one_table():
    assert piles.STATUS_ORDER == {"ожидает": 0, "в работе": 1, "сдано": 2, "принято": 3, "закрыта": 4, "отклонено": 5}
    assert piles.BATCH_STATUSES == ("ожидает", "в работе", "сдано", "принято", "закрыта")      # a batch never holds отклонено
