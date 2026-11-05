"""Tests for tools/piles.py: `close <slug> <N>`: a batch closed into the Закрыто table.

Part of the split of the old tools/test_piles.py (t-596, the 120 s cap per file): the helpers are in
tools/piles_testkit.py, the fixtures `session_tree`, `tree`, `cli` in tools/conftest.py.
Run from the repo root: python -m pytest tools/test_piles_close.py -q
"""
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import piles  # noqa: E402
from piles_testkit import _no_network, PROOF_DONE, PROOF_WAITING, batch_text, batch2, GIT_VARS, put, finding_text, B1, CARD, needs_git, stage, commit, freeze, edit, fetch_origin, rd, tree_state, accept_batch1, head_hash, closed_rows  # noqa: E402


@pytest.fixture(autouse=True)
def _scrub_git_env(monkeypatch):
    for k in GIT_VARS:
        monkeypatch.delenv(k, raising=False)
    monkeypatch.delenv("GITLAB_TOKEN", raising=False)         # the default world has no token
    monkeypatch.delenv("QA_DEV_CONFIG", raising=False)


@needs_git
def test_close_moves_archive_rows_with_hash_and_rebuilds_board(tree, cli):
    accept_batch1(tree)
    h = head_hash(tree)
    code, out = cli(tree, "close", "forge", "1", "--hash", h, "--url", "https://git.example/mr/7", "--today", "2026-10-08")
    assert code == 0 and "forge/1 closed" in out and "moved to Закрыто: B-230" in out, out
    above, below = rd(tree, "plans/BACKLOG.md").split("\n## Закрыто\n")
    assert "| B-230 |" not in above and "| B-230 | **Кучки.**" in below
    row = closed_rows(tree)["B-230"]
    assert row == "| B-230 | **Кучки.** | почему 230 | владелец; закрыто 08.10.2026 пачкой `forge/1`: влито `%s` (MR https://git.example/mr/7) | P4 |" % h
    assert piles.closed_hash(row) == h
    assert list(closed_rows(tree))[-1] == "B-230" and "B-462" in closed_rows(tree)                    # appended after the last closed row
    assert "статус: закрыта | взял: Ира | ветка: `main` (x) | MR: `%s` https://git.example/mr/7" % h in rd(tree, B1)
    assert "| 1 | фундамент | B-230 | L | закрыта | Ира | `main` (x) | `%s` https://git.example/mr/7 |" % h in rd(tree, CARD)
    assert cli(tree, "board", "--check")[0] == 0 and "| B-230 | закрыто `%s` |" % h in rd(tree, "plans/PILES.md")


@needs_git
def test_close_result_passes_the_gate_after_the_freeze(tree, cli):
    freeze(tree)                                                              # lock line + findings for B-102 B-135 B-219 B-308
    accept_batch1(tree)
    commit(tree, "batch 1 accepted")
    fetch_origin(tree)                                                        # taken AND accepted on origin/main
    assert cli(tree, "close", "forge", "1", "--hash", head_hash(tree), "--today", "2026-10-08")[0] == 0
    stage(tree, "plans")
    code, out = cli(tree, "check")
    assert code == 0 and "(г) backlog: ok" in out and "(в) frozen: ok" in out and "RED" not in out, out


@needs_git
def test_close_builds_row_from_finding_for_post_freeze_id(tree, cli):
    edit(tree, CARD, "B-230 | L", "B-230, B-500 | L")
    body = ("# Новая находка.\n\nid: B-500 | кучка: `forge` | от: dev2, 08.10 | приоритет: — | кандидат наверх: нет\n\n"
            "Что не так / что сделать: первая строка\nвторая строка с | чертой\n\nабзац два\n\nСвидетель: прогон 7\n\n"
            "Принципы и правила: P1, FR-2\n\nРешение владельца нужно: нет\n\n<!-- служебное -->\n")
    put(tree, "plans/piles/forge/findings/20261008-novaya.md", body)
    accept_batch1(tree)
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree), "--today", "2026-10-08")
    assert code == 0 and "B-230, B-500" in out, out
    row = closed_rows(tree)["B-500"]
    assert row.startswith("| B-500 | **Новая находка.** первая строка вторая строка с \\| чертой абзац два | прогон 7 | dev2, 08.10; закрыто 08.10.2026 пачкой")
    assert row.endswith("| P1, FR-2 |") and "служебное" not in row
    assert not (tree / "plans/piles/forge/findings/20261008-novaya.md").exists()
    assert len(piles.split_cells(row)) == 5                                   # the escaped pipe did not add a cell


@needs_git
def test_close_three_column_row_normalised_to_five(tree, cli):
    batch2(tree, "принято")
    edit(tree, CARD, "| 2 | потом | B-015 | M | ожидает | — | — | — |", "| 2 | потом | B-015 | M | принято | Ира | `x` | — |")
    assert cli(tree, "close", "forge", "2", "--hash", head_hash(tree), "--today", "2026-10-08")[0] == 0
    row = closed_rows(tree)["B-015"]
    assert len(piles.split_cells(row)) == 5 and row.startswith("| B-015 | Прогон сравнения. | детали прогона | —; закрыто 08.10.2026 пачкой `forge/2`")
    assert row.endswith("| — |")


@needs_git
def test_close_partial_left_open_and_m5_refusal(tree, cli):
    edit(tree, CARD, "B-230 | L", "B-230, B-308 (хвост) | L")
    accept_batch1(tree)
    snap = tree_state(tree)
    h = head_hash(tree)
    code, out = cli(tree, "close", "forge", "1", "--hash", h)
    assert code == 2 and "B-308 (хвост) is a partial member of forge/1 and has no finding file" in out and tree_state(tree) == snap   # m5
    put(tree, "plans/piles/forge/findings/B-308-x.md", finding_text("B-308"))
    code, out = cli(tree, "close", "forge", "1", "--hash", h, "--today", "2026-10-08")
    assert code == 0 and "partial, left open: B-308 (хвост)" in out
    assert "B-308" not in closed_rows(tree) and "| B-308 |" in rd(tree, "plans/BACKLOG.md").split("\n## Закрыто\n")[0]
    assert (tree / "plans/piles/forge/findings/B-308-x.md").exists()


@needs_git
def test_close_requires_accepted(tree, cli):
    snap = tree_state(tree)
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree))
    assert code == 2 and 'forge/1 is "в работе"' in out and 'expected status "принято"' in out, out
    edit(tree, B1, "статус: в работе", "статус: сдано")
    snap = tree_state(tree)
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree))
    assert code == 2 and 'forge/1 is "сдано"' in out and tree_state(tree) == snap
    assert "no batch file for forge/2" in cli(tree, "close", "forge", "2", "--hash", head_hash(tree))[1]


@needs_git
def test_close_unknown_member_refused_before_any_write(tree, cli):
    edit(tree, CARD, "B-230 | L", "B-230, B-999 | L")
    accept_batch1(tree)
    snap = tree_state(tree)
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree))
    assert code == 2 and "B-999 named in forge/1 has no text anywhere" in out and "nothing was written" in out
    assert tree_state(tree) == snap


@needs_git
@pytest.mark.parametrize("args,needle", [
    ((), "--hash is required"),
    (("--hash", "abcdef"), '--hash "abcdef": expected a commit hash (7-40 hex characters)'),
    (("--hash", "a" * 41), "expected a commit hash"),
    (("--hash", "ABCDEF1"), "expected a commit hash"),
    (("--hash", "deadbee"), "deadbee is not a commit in this repository"),
])
def test_close_hash_battery_refuses_and_writes_nothing(tree, cli, args, needle):
    accept_batch1(tree)
    snap = tree_state(tree)
    code, out = cli(tree, "close", "forge", "1", *args)
    assert code == 2 and needle in out and tree_state(tree) == snap, out


@needs_git
@pytest.mark.parametrize("url", ["http://git.example/y", "https://" + "x" * 293, "https://a b", "https://", "x"])
def test_close_url_battery_refuses(tree, cli, url):
    accept_batch1(tree)
    snap = tree_state(tree)
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree), "--url", url)
    assert code == 2 and "--url" in out and "an https:// MR address (at most 300 characters, no spaces)" in out and tree_state(tree) == snap


@needs_git
@pytest.mark.parametrize("short,url_len", [(True, 300), (False, 0)])
def test_close_hash_and_url_at_the_limits_pass(tree, cli, short, url_len):
    accept_batch1(tree)
    args = ["--hash", head_hash(tree, short)]
    if url_len:
        args += ["--url", "https://" + "x" * (url_len - 8)]
    code, out = cli(tree, "close", "forge", "1", *args, "--today", "2026-10-08")
    assert code == 0, out


@needs_git
def test_close_rerun_idempotent(tree, cli):
    accept_batch1(tree)
    h = head_hash(tree)
    cli(tree, "close", "forge", "1", "--hash", h, "--today", "2026-10-08")
    snap = tree_state(tree)
    code, out = cli(tree, "close", "forge", "1", "--hash", h, "--today", "2026-10-09")
    assert code == 0 and "forge/1 is already closed (%s); nothing changed" % h in out and tree_state(tree) == snap
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree, True))
    assert code == 2 and "is already closed with" in out and tree_state(tree) == snap


# ---------------------------------------------------------------- F5-5: `close` reads «Живые доказательства» (FR-33)
# The owner's word 08.10.2026: a batch is closed by finishing, not by carrying over. A proof row is done or carried with a
# person's confirmation -- the forms of «Остатки» (leftover_problem), plus a log / notebook path for `сделано:`.

CARRY_CELL = "перенос: live-runs/1 \\| обоснование: нужен стенд \\| подтвердил: dev1, 08.10"      # `\|` is the pipe inside a table cell
HEAD = "| Что | Где | Кто | Статус |\n|---|---|---|---|\n"


def problems(**kw):
    return piles.proof_problems(batch_text("forge", 1, "принято", **kw))


def with_proof_section(body, head=None):
    """A batch file text whose «Живые доказательства» holds exactly `body` (None: no such section); `head` replaces the readiness line."""
    text = batch_text("forge", 1, "принято")
    above, rest = text.split("## Живые доказательства\n", 1)
    tail = rest.split("## Остатки", 1)[1]
    above = above.replace("Правило готовности.", head) if head else above
    return above + ("## Живые доказательства\n" + body + "\n" if body is not None else "") + "## Остатки" + tail


@pytest.mark.parametrize("cell", [
    "сделано: abc1234", "Сделано: abc1234", "  СДЕЛАНО:   t-12  ", "`сделано: abc1234`", "сделано: " + "a1" * 20, "сделано: t-596",
    "сделано: abc1234 \\| note: see the log", "сделано: t-639 \\| критик интеграции пачки 2", "note: x \\| сделано: abc1234",
    "сделано: abc1234 \\| сделано: nonsense",                              # the FIRST `сделано:` is the value, a later one is a note
    "сделано: logs/journal/dev1.jsonl", "сделано: experiments/run-13/runs/cmp3gb.md:12", "сделано: docs/n.md#s2",
    CARRY_CELL, "ПЕРЕНОС: куда-то \\| Обоснование: р \\| Подтвердил: М, 08.10", "перенос: live-runs/1 \\| обоснование: р \\| подтвердил: — dev1",
])
def test_proofs_a_finished_or_person_confirmed_row_passes(cell):
    assert problems(proof=cell) == []


@pytest.mark.parametrize("cell,needle", [
    (PROOF_WAITING, "has neither `сделано:` nor `перенос:`"),
    ("ждёт", "has neither"), ("ожидает", "has neither"), ("", "has neither"),
    ("**стоит на блокере K2/K9** (красный тест без пробы запирает S5)", "has neither"),
    ("n/a: закреплено тестами t-611", "has neither"),
    ("сделано: abcdef", "`сделано: abcdef` is neither 7-40 hex characters nor t-nnn nor a log/notebook path"),    # 6 hex: one short
    ("Сделано: ABC1234", "`сделано: ABC1234` is neither 7-40 hex"), ("СДЕЛАНО: T-12", "`сделано: T-12` is neither"),   # keys case-free, values strict
    ("сделано: nonsense \\| сделано: abc1234", "`сделано: nonsense` is neither"),                     # the first `сделано:` is the value
    ("сделано: abc1234 (see the log)", "`сделано: abc1234 (see the log)` is neither"),             # a note in the value's own segment
    ("сделано: " + "a" * 41, "is neither 7-40 hex"), ("сделано: T5", "is neither"), ("сделано: да/нет", "is neither"),
    ("сделано: logs/journal", "is neither"),                                                      # a path needs a file extension
    ("сделано:", "is neither"),
    ("сделано: t-1 \\| перенос: x \\| обоснование: р \\| подтвердил: М, 08", "carries both `сделано:` and `перенос:`"),   # neither form wins
    ("перенос: live-runs/1 \\| обоснование: р", "`подтвердил:` is missing"),
    ("перенос: live-runs/1 \\| обоснование: р \\| подтвердил:", "`подтвердил:` is empty"),
    ("перенос: live-runs/1 \\| обоснование: р \\| подтвердил: N/A", "is a placeholder, not a person's confirmation"),
    ("перенос: live-runs/1 \\| подтвердил: М, 08.10", "`обоснование:` is missing"),
    ("перенос: — \\| обоснование: р \\| подтвердил: М, 08.10", "`перенос: —` is none of a place"),
    ("перенос: live-runs/1 | обоснование: р | подтвердил: М, 08.10", "`обоснование:` is missing"),   # an unescaped pipe is another cell, not a pair
])
def test_proofs_a_row_outside_the_closed_set_is_named_with_its_what_and_its_cell(cell, needle):
    found = problems(proof=cell)
    assert len(found) == 1 and needle in found[0], found
    assert found[0].startswith("line ") and '"a"' in found[0] and '(status: "%s' % cell[:20] in found[0]      # the row's «Что» and the cell


def test_proofs_the_what_is_cut_at_80_characters_and_an_empty_what_is_said_so():
    long_what = "д" * 120
    found = piles.proof_problems(batch_text("forge", 1, "принято").replace("| a | b |", "| %s | b |" % long_what))
    assert "д" * 79 + "…" in found[0] and "д" * 80 not in found[0]
    assert "(no «Что» text)" in piles.proof_problems(batch_text("forge", 1).replace("| a | b |", "|  | b |"))[0]


def test_proofs_every_table_of_every_section_counts_and_a_header_only_table_passes():
    assert piles.proof_problems(with_proof_section(HEAD)) == []                                     # a table with only the header
    assert piles.proof_problems(with_proof_section("")) == []                                       # an empty section
    assert piles.proof_problems(with_proof_section(None)) == []                                     # no section at all
    two = HEAD + "| x | y | z | сделано: t-1 |\n\nтекст между таблицами\n\n" + HEAD + "| второй | y | z | ждёт |\n"
    found = piles.proof_problems(with_proof_section(two))
    assert len(found) == 1 and '"второй"' in found[0]                                               # the second table counts too
    found = piles.proof_problems(with_proof_section("| Что | Где |\n|---|---|\n| x | y |\n"))
    assert len(found) == 1 and "no «Статус» column" in found[0]


def test_proofs_a_comment_hides_what_it_covers_ends_the_table_and_an_unclosed_one_is_refused():
    found = piles.proof_problems(with_proof_section(HEAD + "<!-- | спрятано | y | z | ждёт | -->\n| живая | y | z | ждёт |\n"))
    assert len(found) == 1 and "no «Статус» column" in found[0] and "живая" in found[0]            # (в)'s boundary: the row after the comment is a header
    assert piles.proof_problems(with_proof_section(HEAD + "| a | y | z | сделано: t-1 | <!-- ждёт -->\n")) == []     # an inline comment ends nothing
    found = piles.proof_problems(with_proof_section(HEAD + "<!-- | x | y | z | ждёт |\n"))
    assert "never closes" in found[0] and "piles-skip: в --" in found[0]


# ---- F5-5 fix round (t-787), M1: ONE table boundary for `close` and (в) -- walk_table is the one walker --------------------

def _shape(row_lines):
    """A batch file whose proof table is HEAD + `row_lines` with the waiting cell, and the same text with the cell finished."""
    wait, done = (with_proof_section(HEAD + row_lines % c) for c in ("ждёт", PROOF_DONE))
    return wait, done


@pytest.mark.parametrize("shape,rows", [
    ("plain", "| a | b | c | %s |\n"),
    ("two rows with a rule", "| z | b | c | сделано: t-1 |\n|---|---|---|---|\n| a | b | c | %s |\n"),
])
def test_close_and_frozen_agree_on_a_row_the_gate_demands_an_edit_of(shape, rows):
    wait, done = _shape(rows)
    found = piles.proof_problems(wait)
    assert len(found) == 1 and '"a"' in found[0], found                                            # the gate names the row
    assert piles.proof_problems(done) == []
    assert piles._frozen_lines(wait) == piles._frozen_lines(done)                                  # (в) takes the edit as a «Статус» edit


@pytest.mark.parametrize("shape,rows", [
    ("a comment-only line before the row", "<!-- note -->\n| a | b | c | %s |\n"),
    ("a blank line before the row", "\n| a | b | c | %s |\n"),
    ("text before the row", "text\n| a | b | c | %s |\n"),
])
def test_a_line_that_is_not_a_table_row_ends_the_table_for_close_and_for_frozen_alike(shape, rows):
    wait, done = _shape(rows)
    found = piles.proof_problems(wait)
    assert len(found) == 1 and "no «Статус» column" in found[0] and "header: a | b | c | ждёт" in found[0], found   # the row is a NEW header: loud
    assert "piles-skip: в --" in found[0] and "no proofs are owed" in found[0]                    # both exits are named
    after = piles.proof_problems(done)
    assert len(after) == 1 and "no «Статус» column" in after[0]                                    # a «Статус» edit cures nothing...
    assert piles._frozen_lines(wait) != piles._frozen_lines(done)                                  # ...and (в) reads that header as text: not masked


def test_an_indented_pipe_line_is_no_row_for_close_and_for_frozen_alike():
    wait, done = _shape("  | a | b | c | %s |\n")
    assert piles.proof_problems(wait) == [] == piles.proof_problems(done)                          # not a row: the gate does not judge it
    assert piles._frozen_lines(wait) != piles._frozen_lines(done)                                  # and (в) does not mask it: a text line


def test_walk_table_is_the_one_boundary_of_the_three_readers():
    lines = ["## S", "|h1|h2|", "|---|---|", "| a | b |", "", "| c | d |", "  | e | f |", "<!-- x -->", "| g |"]
    kinds = [k for k, _ in piles.walk_table(lines)]
    assert kinds == [None, "header", "rule", "row", None, "header", None, None, "header"]
    assert piles.table_after(lines, "S") == (["h1", "h2"], [(["a", "b"], 4)])                      # the first table, ended by the blank line
    assert piles.table_after(lines, "Nothing") is None and piles.table_after(["## S", "text", "## T", "| h |"], "S") is None


def test_proofs_the_readiness_rule_that_names_live_proofs_needs_a_table():
    promise = "Правило готовности: пачка закрыта, когда живые доказательства (FR-33) сделаны."
    found = piles.proof_problems(with_proof_section("Только текст, таблицы нет.", promise))
    assert len(found) == 1 and "promises live proofs" in found[0] and "has no table" in found[0]
    assert "promises live proofs" in piles.proof_problems(with_proof_section(None, promise))[0]      # no section, same promise
    assert "promises live proofs" in piles.proof_problems(with_proof_section(None, "ЖИВЫЕ ДОКАЗАТЕЛЬСТВА нужны"))[0]
    assert piles.proof_problems(with_proof_section("Только текст, таблицы нет.")) == []              # no promise, no table: closes freely
    assert piles.proof_problems(with_proof_section(None, "<!-- живые доказательства -->")) == []   # a comment is no promise
    assert piles.proof_problems(with_proof_section("| Что | Статус |\n|---|---|\n", promise)) == []   # a header-only table is a table


@needs_git
def test_close_refuses_while_a_proof_row_waits_and_writes_nothing(tree, cli):
    accept_batch1(tree)
    edit(tree, B1, "| a | b | c | %s |" % PROOF_DONE, "| проба на стенде | b | c | ждёт |")
    snap = tree_state(tree)
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree), "--today", "2026-10-08")
    assert code == 2 and "plans/piles/forge/batch-1-foundation.md" in out, out                     # the batch
    assert '"проба на стенде"' in out and '(status: "ждёт")' in out                                  # the row's «Что» and the cell
    assert "«Живые доказательства» are not finished" in out and "Nothing was written" in out
    assert "`сделано: <7-40 hex | t-nnn | path/to/log-or-notebook.ext>`" in out and "`подтвердил: <кто, дата>`" in out
    assert "a PERSON" in out and tree_state(tree) == snap                                            # the door; sha256 unchanged
    edit(tree, B1, "| проба на стенде | b | c | ждёт |", "| проба на стенде | b | c | %s |" % CARRY_CELL)
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree), "--today", "2026-10-08")
    assert code == 0 and "forge/1 closed" in out and rd(tree, B1).count("статус: закрыта") == 1


@needs_git
def test_close_judges_ostatki_first_then_the_proofs_and_a_closed_batch_is_not_judged_again(tree, cli):
    accept_batch1(tree)
    edit(tree, B1, "| a | b | c | %s |" % PROOF_DONE, "| a | b | c | ждёт |")
    edit(tree, B1, "- x | сделано: t-1", "- осталось дело")
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree))
    assert code == 2 and "«Остатки» is not finished" in out and "«Живые доказательства»" not in out
    edit(tree, B1, "- осталось дело", "- x | сделано: t-1")
    assert "«Живые доказательства» are not finished" in cli(tree, "close", "forge", "1", "--hash", head_hash(tree))[1]
    edit(tree, B1, "| a | b | c | ждёт |", "| a | b | c | %s |" % PROOF_DONE)
    h = head_hash(tree)
    assert cli(tree, "close", "forge", "1", "--hash", h, "--today", "2026-10-08")[0] == 0
    edit(tree, B1, "| a | b | c | %s |" % PROOF_DONE, "| a | b | c | ждёт |")                        # re-opened after the close
    snap = tree_state(tree)
    code, out = cli(tree, "close", "forge", "1", "--hash", h)
    assert code == 0 and "already closed" in out and tree_state(tree) == snap


@needs_git
def test_close_refuses_a_batch_that_promises_live_proofs_and_has_no_table(tree, cli):
    accept_batch1(tree)
    put(tree, B1, with_proof_section("Таблицы нет.", "Правило готовности: живые доказательства (FR-33) сделаны.").replace(
        "статус: в работе", "статус: принято"))
    snap = tree_state(tree)
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree))
    assert code == 2 and "promises live proofs" in out and "has no table" in out and tree_state(tree) == snap
    assert "no proofs are owed" in out and "piles-skip: в -- <reason>" in out                       # M2(b): both exits of a shape refusal


# ---- t-787, M2: the refusal tells where a note goes and which door fits a refusal about the section's shape -----------------

REAL = pathlib.Path(__file__).resolve().parent.parent
REAL_NOTE_VALUES = {"F2-10": "t-611", "F2-7": "t-626", "B-419": "t-639"}          # the value each finished cell of forge/2 stands on


def test_the_three_real_finished_cells_of_forge_2_are_refused_with_the_note_segment_and_pass_when_split():
    text = piles.read_text(REAL / "plans/piles/forge/batch-2-critic-measurers.md")
    rows = [c for c, _ in piles.table_after(text.split("\n"), "Живые доказательства")[1] if c[3].startswith("сделано:")]
    assert [c[0].split(":")[0] for c in rows] == list(REAL_NOTE_VALUES), rows                      # lines 104-106 of the file
    for what, _, _, cell in rows:
        why = piles.proof_problems(batch_text("forge", 1, "принято", proof=cell))
        assert len(why) == 1 and "is neither 7-40 hex" in why[0], why                               # as written: refused, in the row's own words
        with pytest.raises(piles.Refused) as refusal:
            piles.check_proofs(batch_text("forge", 1, "принято", proof=cell), "b.md")
        assert "a note after it goes in its own ` \\| ` segment: `сделано: abc1234 \\| note: see the log`" in str(refusal.value)
        split = "сделано: %s \\| %s" % (REAL_NOTE_VALUES[what.split(":")[0]], cell[len("сделано: "):])
        assert piles.proof_problems(batch_text("forge", 1, "принято", proof=split)) == [], split   # the exact change: value, then ` \| note`


@pytest.mark.parametrize("pairs,ok", [
    ("сделано: abc1234", True), ("Сделано: abc1234", True), ("СДЕЛАНО: t-5", True),             # the key is case-free in BOTH gates
    ("сделано: T-5", False), ("Сделано: T-5", False), ("сделано: ABC1234", False),              # the value is strict in BOTH gates
    ("перенос: пачка 2 | обоснование: р | подтвердил: М, 08.10", True),
    ("Перенос: пачка 2 | Обоснование: р | Подтвердил: М, 08.10", True),                         # mixed-case keys inside the pairs
    ("перенос: пачка 2 | ОБОСНОВАНИЕ: | подтвердил: М, 08.10", False),                          # an empty value is still empty
    ("Перенос: пачка 2 | Обоснование: р", False),                                                # the missing key is missing in any case
])
def test_one_case_policy_for_the_shared_form_reader_in_ostatki_and_in_the_proofs(pairs, ok):
    leftover = piles.leftover_problem(piles.leftover_pairs("- x | " + pairs))
    proof = piles.proof_problems(batch_text("forge", 1, "принято", proof=pairs.replace(" | ", " \\| ")))
    assert (leftover is None) is ok and (proof == []) is ok, (leftover, proof)


# ---------------------------------------------------------------- GM1-1: close touches files only, no board

@needs_git
@pytest.mark.parametrize("token", [None, "glpat-secret-value"])
def test_close_writes_no_board_line_with_or_without_token(tree, cli, monkeypatch, token):
    _no_network(monkeypatch)
    if token:
        monkeypatch.setenv("GITLAB_TOKEN", token)
    accept_batch1(tree)
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree), "--today", "2026-10-08")
    assert code == 0 and "forge/1 closed" in out, out
    assert "доска" not in out and "issue" not in out and "glpat" not in out
    assert out.rstrip().splitlines()[-1].startswith("  Next: git add")        # the commit instruction stays last
    assert "статус: закрыта" in rd(tree, B1) and "issue:" not in rd(tree, B1)
    assert cli(tree, "board", "--check")[0] == 0


@needs_git
def test_close_runs_with_no_piles_gitlab_module(tree, cli, monkeypatch):
    monkeypatch.setitem(sys.modules, "piles_gitlab", None)                     # an import of it raises ImportError
    _no_network(monkeypatch)
    accept_batch1(tree)
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree), "--today", "2026-10-08")
    assert code == 0 and "forge/1 closed" in out and "доска" not in out, out
    assert "статус: закрыта" in rd(tree, B1) and cli(tree, "board", "--check")[0] == 0


@needs_git
def test_close_passes_a_batch_whose_header_carries_an_old_issue_line(tree, cli):
    head = next(l for l in rd(tree, B1).split("\n") if l.startswith("кучка:"))
    edit(tree, B1, head, head + " | issue: https://example.invalid/issues/7")
    accept_batch1(tree)
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree), "--today", "2026-10-08")
    assert code == 0 and "forge/1 closed" in out, out
    assert "issue: https://example.invalid/issues/7" in rd(tree, B1)            # the old line is left alone


@needs_git
def test_close_that_changes_nothing_or_is_refused_prints_no_board_word(tree, cli):
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree))        # still `в работе`: refused
    assert code == 2 and "доска" not in out
    accept_batch1(tree)
    h = head_hash(tree)
    assert cli(tree, "close", "forge", "1", "--hash", h, "--today", "2026-10-08")[0] == 0
    code, out = cli(tree, "close", "forge", "1", "--hash", h)
    assert code == 0 and "already closed" in out and "доска" not in out
    code, out = cli(tree, "close", "--id", "B-102", "--word", "владелец, 08.10", "--today", "2026-10-08")   # a row, not a batch
    assert code == 0 and "доска" not in out


# ---- t-1738 (FG7-4, F9 a): close starts the FULL worktree sweep in the background and says what became of the launch


def _launch(monkeypatch, result):
    """`worktree_sweep.launch_background` returns `result` (a (kind, text) pair) or raises it."""
    import worktree_sweep

    def fake(root, trigger, **kw):
        assert trigger == "piles-close"
        if isinstance(result, Exception):
            raise result
        return result

    monkeypatch.setattr(worktree_sweep, "launch_background", fake)


@needs_git
def test_c1_close_prints_the_started_line_before_the_commit_instruction(tree, cli, monkeypatch):
    _launch(monkeypatch, ("started", "worktree sweep started in the background (log .git/worktree-sweep/run.log)"))
    accept_batch1(tree)
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree), "--today", "2026-10-08")
    lines = out.rstrip().splitlines()
    at = lines.index("  worktrees: worktree sweep started in the background (log .git/worktree-sweep/run.log)")
    assert code == 0 and at < len(lines) - 1 and lines[-1].startswith("  Next: git add")     # the commit instruction stays last


@needs_git
def test_c2_close_names_a_sweep_that_is_already_running_and_exits_0(tree, cli, monkeypatch):
    text = "a worktree sweep is already running since 2026-11-03T10:00:00 (post-merge); a second pass is queued"
    _launch(monkeypatch, ("busy", text))
    accept_batch1(tree)
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree), "--today", "2026-10-08")
    assert code == 0 and "  worktrees: " + text in out.splitlines() and "forge/1 closed" in out


@needs_git
@pytest.mark.parametrize("result,reason", [
    (("refused", "tools/worktree_sweep.py not found in C:/x"), "tools/worktree_sweep.py not found in C:/x"),
    (("failed", "background sweep not started (OSError: no process)"), "OSError: no process"),
    (RuntimeError("it broke\nsecond line"), "RuntimeError: it broke")])
def test_c3_a_launch_that_did_not_happen_is_a_line_with_the_door_never_silence(tree, cli, monkeypatch, result, reason):
    _launch(monkeypatch, result)
    accept_batch1(tree)
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree), "--today", "2026-10-08")
    mine = [l for l in out.splitlines() if l.startswith("  worktrees:")]
    assert code == 0 and "forge/1 closed" in out and len(mine) == 1
    assert mine[0] == "  worktrees: background sweep not started (%s) -- python tools/worktree_sweep.py --apply" % reason


@needs_git
def test_c4_close_on_a_git_tree_hands_the_launcher_a_recorder_and_never_makes_a_process(tree, cli, monkeypatch):
    import subprocess
    import worktree_sweep

    (tree / "tools").mkdir(exist_ok=True)
    (tree / "tools" / "worktree_sweep.py").write_text("# stub of the main checkout's tool\n")
    real_popen, made = subprocess.Popen, []

    def spy(argv, *a, **kw):                                           # git still runs; only a launch of the sweep is caught
        if isinstance(argv, list) and "--background-run" in argv:
            made.append(argv)
            raise AssertionError("a real sweep process was made")
        return real_popen(argv, *a, **kw)

    monkeypatch.setattr(subprocess, "Popen", spy)
    with pytest.raises(AssertionError):                                # positive control: the spy DOES catch such a launch
        subprocess.Popen([sys.executable, "-c", "pass", "--background-run"])
    made.clear()
    assert worktree_sweep.spawn_detached.__name__ == "recorder"        # the `cli` fixture's recorder, not the real launcher
    accept_batch1(tree)
    code, out = cli(tree, "close", "forge", "1", "--hash", head_hash(tree), "--today", "2026-10-08")
    assert code == 0 and made == [] and len(cli.spawned) == 1 and cli.spawned[0][2] == "--background-run"
    assert "  worktrees: worktree sweep started in the background" in out
