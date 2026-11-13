"""Tests for tools/piles.py: `check` items (б) overlap and (д) form.

Part of the split of the old tools/test_piles.py (t-596, the 120 s cap per file): the helpers are in
tools/piles_testkit.py, the fixtures `session_tree`, `tree`, `cli` in tools/conftest.py.
Run from the repo root: python -m pytest tools/test_piles_form.py -q
"""
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import piles  # noqa: E402
from piles_testkit import GIT_VARS, put, card_text, batch_text, node, finding_text, ROW1, ROW2, needs_git, stage, commit, edit, msg  # noqa: E402


@pytest.fixture(autouse=True)
def _scrub_git_env(monkeypatch):
    for k in GIT_VARS:
        monkeypatch.delenv(k, raising=False)


# ---------------------------------------------------------------- (б) overlap

BRIEF = "## Бриф\n"       # the heading an UNTAKEN batch file carries (F6-28, `_heading_reds`)


def two_batches(tree, w1, w2, pre1="", pre2="", st1="в работе", st2="в работе"):
    put(tree, "plans/piles/forge/README.md", card_text("forge", "Forge", [
        ["1", "a", "B-230", "L", st1, "Ира", "`main`", "—"], ["2", "b", "B-015", "M", st2, "Катя", "`pile/forge/batch-2`", "—"]]))
    put(tree, "plans/piles/forge/batch-1-foundation.md", batch_text("forge", 1, st1, [node("F0-1", w1)], pre=pre1))
    put(tree, "plans/piles/forge/batch-2-next.md", batch_text("forge", 2, st2, [node("F0-2", w2)], pre=pre2))
    stage(tree, "plans/piles")


@needs_git
def test_check_b_overlap_red_queue_both_passes(tree, cli):
    two_batches(tree, "`tools/piles.py`", "`tools/piles.py`")
    code, out = cli(tree, "check")
    assert code == 2 and "(б) overlap: RED" in out and "forge/1 and forge/2 both write: tools/piles.py" in out
    assert "очередь: forge/1 → forge/2" in out
    q = "\nочередь: forge/1 → forge/2\n"
    two_batches(tree, "`tools/piles.py`", "`tools/piles.py`", q, q)
    code, out = cli(tree, "check")
    assert code == 0, out


@needs_git
def test_check_b_queue_on_one_side_or_opposite_directions_is_red(tree, cli):
    q = "\nочередь: forge/1 → forge/2\n"
    two_batches(tree, "`tools/piles.py`", "`tools/piles.py`", q, "")
    assert cli(tree, "check")[0] == 2
    two_batches(tree, "`tools/piles.py`", "`tools/piles.py`", q, "\nочередь: forge/2 → forge/1\n")
    code, out = cli(tree, "check")
    assert code == 2 and "disagree on the order" in out


PKG_TOPS = ("scripts", "references", "changelog.d")


@pytest.mark.parametrize("a,b,tops,red", [
    ("tools/x.py", "scripts/x.py", PKG_TOPS, False),          # two full paths with the same basename: not the same file
    ("x.py", "scripts/x.py", PKG_TOPS, True),                  # a bare basename against a path
    ("ai-packages/qa-factory/scripts/x.py", "scripts/x.py", PKG_TOPS, True),   # the package prefix is stripped
    ("tools/", "tools/piles.py", PKG_TOPS, True),             # a directory against a file inside it
    ("tools/*.py", "tools/piles.py", PKG_TOPS, True),         # a glob against a literal
    ("plans/piles/**", "plans/piles/forge/batch-1.md", PKG_TOPS, True),
    ("plans/piles/*", "plans/piles/forge/batch-1.md", PKG_TOPS, False),   # '*' stops at a slash, as in features.json
    ("tools/a*", "tools/ab*", PKG_TOPS, True),                # two globs whose literal prefixes nest
    ("tools/a*", "docs/b*", PKG_TOPS, False),
    ("tools\\piles.py", "tools/piles.py", PKG_TOPS, True),    # a backslash is a slash
    ("docs/x.md", "docs/y.md", PKG_TOPS, False),
    ("ai-packages/qa-factory/", "changelog.d/", PKG_TOPS, True),      # the whole package against a package folder
    ("ai-packages/qa-factory", "changelog.d/", PKG_TOPS, True),       # the root without its slash is the same token
    ("ai-packages/qa-factory/", "tools/x.py", PKG_TOPS, False),       # `tools` is not a package top
    ("ai-packages/qa-factory/", "tools/x.py", None, True),            # no tops: the safe side
    ("ai-packages/qa-factory/", "scripts/x.py", PKG_TOPS, True),      # a literal file: the false green of an empty token is closed
    ("ai-packages/qa-factory/", "story_run.py", PKG_TOPS, True),      # a bare basename has no resolvable place: the safe side
    ("ai-packages/qa-factory/", "**/x.py", PKG_TOPS, True),           # a glob first segment: the safe side
    ("ai-packages/qa-factory/", "tools/*.py", PKG_TOPS, False),       # a known top outside the package: still no overlap
    ("   ", "tools/", PKG_TOPS, False),                             # a span of spaces is no token and overlaps nothing
])
def test_check_b_token_overlap_rules(a, b, tops, red):
    assert piles.tokens_overlap(piles._norm_token(a), piles._norm_token(b), tops=tops) is red
    assert piles.tokens_overlap(piles._norm_token(b), piles._norm_token(a), tops=tops) is red


# ---------------------------------------------------------------- (б) one developer's batches (SL-4)

def vocab_for(kind, tree, monkeypatch):
    """The developer vocabulary a `test_dev_of` row reads: a literal set, or the real reader on a tree / with git failing."""
    if kind == "git-fails":
        monkeypatch.setattr(piles, "git", lambda root, *a: (-1, b"git cannot run"))
        return piles.developer_vocabulary(tree)
    if kind == "untracked":
        put(tree, "logs/journal/dev1.jsonl", "{}\n")
        stage(tree, "logs/journal/dev1.jsonl")
        put(tree, "logs/journal/dev2.jsonl", "{}\n")                       # on disk, not in the index
        return piles.developer_vocabulary(tree)
    return frozenset(kind.split("+")) if kind else frozenset()


@needs_git
@pytest.mark.parametrize("who,kind,want", [
    ("dev10", "dev1", None),                                   # the token is dev10, not dev1
    ("dev1-old", "dev1", None),
    ("dev1 → dev2 (передача)", "dev1+dev2", None),              # two slugs
    ("Ира", "dev1", None),
    ("владелец (Lead)", "dev1", None),
    ("—", "dev1", None),
    ("", "dev1", None),
    ("DEV1, 13.11.2026", "dev1", "dev1"),                      # case is folded, the date goes
    ("Lead dev1 (Opus), 13.11.2026", "dev1", "dev1"),          # lead and opus are not slugs
    ("Lead dev1", "lead+dev1", None),                          # a journal named lead.jsonl: two slugs
    ("dev1, 05.11.2026", "dev1", "dev1"),                      # the real values of github-move/3 and onboarding-forge/1
    ("dev1 (Opus coord), 12.11.2026", "dev1", "dev1"),
    ("dev1ира", "dev1", None),                                 # a slug is a whole token: a letter of another alphabet breaks it
    ("dev12", "dev1", None),
    ("xdev1", "dev1", None),
    ("dev1,", "dev1", "dev1"),
    ("(dev1)", "dev1", "dev1"),
    ("dev1, 12.11.2026", "", None),                            # empty-vocab
    ("dev2, 13.11.2026", "untracked", None),                   # untracked-journal-not-slug
    ("dev1, 13.11.2026", "untracked", "dev1"),
    ("dev1, 13.11.2026", "git-fails", None),                   # git-fails-empty-vocab
], ids=["dev10", "dev1-old", "two-slugs-handover", "cyrillic-name", "owner-and-lead", "dash", "empty", "case-folded-with-date",
        "lead-and-opus-are-not-slugs", "journal-named-lead", "real-github-move-3", "real-onboarding-forge-1", "dev1-cyrillic-glued", "dev12-digit-glued", "xdev1-letter-glued",
        "dev1-comma", "dev1-parens", "empty-vocab",
        "untracked-journal-not-slug", "tracked-journal-is-slug", "git-fails-empty-vocab"])
def test_dev_of(tree, monkeypatch, who, kind, want):
    assert piles.dev_of(who, vocab_for(kind, tree, monkeypatch)) == want


def dev_batches(tree, who1, who2, w1, w2, journals=("dev1",), st2="в работе", node2="в работе"):
    for j in journals:
        put(tree, "logs/journal/%s.jsonl" % j, "{}\n")
    put(tree, "plans/piles/forge/README.md", card_text("forge", "Forge", [
        ["1", "a", "B-230", "L", "в работе", who1, "`main`", "—"], ["2", "b", "B-015", "M", st2, who2, "`pile/forge/batch-2`", "—"]]))
    put(tree, "plans/piles/forge/batch-1-foundation.md", batch_text("forge", 1, "в работе", [node("F0-1", w1[0], w1[1])], who=who1))
    put(tree, "plans/piles/forge/batch-2-next.md", batch_text("forge", 2, st2, [node("F0-2", w2, node2)], who=who2))
    stage(tree, "plans/piles", "logs/journal")


@needs_git
@pytest.mark.parametrize("who1,who2,w1,w2,journals,code,needle", [
    ("dev1, 12.11.2026", "dev1 (Opus), 13.11.2026", ("`scripts/tests/a.py`", "в работе"), "`scripts/tests/`", ("dev1",), 0,
     "1 pair(s) of one developer not compared (dev1: forge/1 + forge/2; inside one developer the only guard is `owns_gate`'s WARN"),
    ("dev1, 12.11.2026", "Ира", ("`ai-packages/qa-factory/`", "в работе"), "`scripts/x.py`", ("dev1",), 2,
     "forge/1 and forge/2 both write: ai-packages/qa-factory/ (the whole package) ~ scripts/x.py"),
    ("dev1, 12.11.2026", "dev2, 13.11.2026", ("`scripts/x.py`", "ожидает"), "`scripts/x.py`", ("dev1", "dev2"), 2,
     "forge/1 and forge/2 both write: scripts/x.py"),                      # a waiting node of a taken batch keeps its zone (F-D1 (3))
    ("dev1, 12.11.2026", "dev1, 13.11.2026", ("`scripts/x.py`", "в работе"), "`scripts/x.py`", ("dev1",), 0,
     "not compared"),                                                      # two clones, one slug: read as one developer (the accepted risk)
], ids=["same-developer", "different-developer", "waiting-node-other-developer", "two-clones-one-slug"])
def test_check_b_pair_by_developer(tree, cli, who1, who2, w1, w2, journals, code, needle):
    dev_batches(tree, who1, who2, w1, w2, journals)
    got, out = cli(tree, "check")
    assert got == code and needle in out, out


@needs_git
def test_check_b_only_active_batches_and_unfinished_nodes_count(tree, cli):
    two_batches(tree, "`tools/piles.py`", "`tools/piles.py`", pre2=BRIEF, st2="ожидает")
    assert cli(tree, "check")[0] == 0                                         # a waiting batch writes nothing yet
    put(tree, "plans/piles/forge/batch-2-next.md", batch_text("forge", 2, "в работе", [node("F0-2", "`tools/piles.py`", "принято")]))
    stage(tree, "plans/piles")
    two_batches(tree, "`tools/piles.py`", "`tools/piles.py`")
    put(tree, "plans/piles/forge/batch-2-next.md", batch_text("forge", 2, "в работе", [node("F0-2", "`tools/piles.py`", "принято")]))
    stage(tree, "plans/piles")
    assert cli(tree, "check")[0] == 0                                         # an accepted node no longer writes


# ---------------------------------------------------------------- (д) form

def form_case(tree, cli, text, needle, rel="plans/piles/forge/batch-1-foundation.md"):
    put(tree, rel, text)
    stage(tree, "plans/piles")
    code, out = cli(tree, "check")
    assert code == 2 and "(д) form: RED" in out and needle in out, out
    return out


@needs_git
def test_check_d_missing_writes_or_executor_red(tree, cli):
    form_case(tree, cli, batch_text("forge", 1, nodes=[node("F0-1", "—")]), 'no path in "Пишет в"')
    form_case(tree, cli, batch_text("forge", 1, nodes=[node("F0-1", "без бэктиков.py")]), 'no path in "Пишет в"')
    form_case(tree, cli, batch_text("forge", 1, nodes=[node("F0-1", "`a.py`", executor="—")]), "has no Исполнитель")
    put(tree, "plans/piles/forge/batch-1-foundation.md", batch_text("forge", 1, nodes=[node("F0-1", "нет")]))
    stage(tree, "plans/piles")
    assert cli(tree, "check")[0] == 0                                          # the word "нет": a node that writes no file


@needs_git
def test_check_d_unknown_status_red(tree, cli):
    form_case(tree, cli, batch_text("forge", 1, "готово", nodes=[node("F0-1")]), 'status "готово"')
    form_case(tree, cli, batch_text("forge", 1, nodes=[node("F0-1", status="влито 05403ea")]), 'status "влито 05403ea"')
    put(tree, "plans/piles/forge/batch-1-foundation.md", batch_text("forge", 1, nodes=[node("F0-1", status="сдано 08.10")]))
    stage(tree, "plans/piles")
    assert cli(tree, "check")[0] == 0                                          # a date after the word is fine


@needs_git
def test_check_d_optional_priority_pair_in_the_batch_header_is_accepted_and_masks_nothing(tree, cli):
    base = batch_text("forge", 1, nodes=[node("F0-1")])
    pair_at = {"last": base.replace("стенд: не нужен", "стенд: не нужен | приоритет: П3"),
               "first": base.replace("кучка: `forge` |", "кучка: `forge` | приоритет: П2 |"),
               "ticks": base.replace("стенд: не нужен", "стенд: не нужен | приоритет: `П3` | issue: https://x/-/issues/1")}
    for name, text in pair_at.items():                                         # at: the three places, the three words
        assert text != base, name
        put(tree, "plans/piles/forge/batch-1-foundation.md", text)
        stage(tree, "plans/piles")
        assert cli(tree, "check")[0] == 0, name
    # beyond: the pair does not hide a real defect of the same line -- a misspelt status key is red as without the pair
    bad = base.replace("статус:", "status:").replace("стенд: не нужен", "стенд: не нужен | приоритет: П3")
    form_case(tree, cli, bad, 'status "" starts with no known status word')


@needs_git
def test_check_d_missing_columns_and_header_red(tree, cli):
    form_case(tree, cli, "# F — пачка 1\n\nкучка: `forge` | статус: в работе\n\n## Узлы\n\n| Узел | Что |\n|---|---|\n| a | b |\n",
              "no Исполнитель, Пишет в, Статус column")
    form_case(tree, cli, "# F — пачка 1\n\nбез шапки\n", "no header line")


@needs_git
def test_check_d_duplicate_batch_number_red(tree, cli):
    put(tree, "plans/piles/forge/batch-1-copy.md", batch_text("forge", 1, nodes=[node("F0-9", "`z.py`")]))
    stage(tree, "plans/piles")
    code, out = cli(tree, "check")
    assert code == 2 and "batch forge/1 has 2 files" in out


@needs_git
def test_check_d_card_ahead_of_file_red_file_ahead_ok(tree, cli):
    edit(tree, "plans/piles/forge/README.md", "| 1 | фундамент | B-230 | L | в работе", "| 1 | фундамент | B-230 | L | сдано")
    stage(tree, "plans/piles")
    code, out = cli(tree, "check")
    assert code == 2 and "the card is ahead of the file" in out
    edit(tree, "plans/piles/forge/README.md", "| 1 | фундамент | B-230 | L | сдано", "| 1 | фундамент | B-230 | L | ожидает")
    stage(tree, "plans/piles")
    assert cli(tree, "check")[0] == 0                                          # the file is ahead of the card: normal while work runs


@needs_git
def test_check_d_file_without_card_row_red(tree, cli):
    put(tree, "plans/piles/forge/batch-5-x.md", batch_text("forge", 5, nodes=[node("F0-1", "`q.py`")]))
    stage(tree, "plans/piles")
    code, out = cli(tree, "check")
    assert code == 2 and "has no row 5 in the card" in out


@needs_git
def test_check_d_frozen_batch_with_empty_nodes_red(tree, cli):
    form_case(tree, cli, batch_text("forge", 1, "в работе", nodes=[]), "empty node table")
    put(tree, "plans/piles/forge/batch-1-foundation.md", batch_text("forge", 1, "ожидает", nodes=[], pre=BRIEF))
    edit(tree, "plans/piles/forge/README.md", "| 1 | фундамент | B-230 | L | в работе", "| 1 | фундамент | B-230 | L | ожидает")
    stage(tree, "plans/piles")
    assert cli(tree, "check")[0] == 0                                          # a waiting batch may still be empty


# ---------------------------------------------------------------- (д) F6-28: «Содержание» and «## Бриф» at commit time

FOUND = "plans/piles/forge/findings/20261014-x.md"


def contents_card(*rows):
    """The forge card with a «## Содержание» section holding `rows` (one line each)."""
    return card_text("forge", "Forge", [ROW1, ROW2]) + "\n## Содержание\n\n| id / файл | что |\n|---|---|\n" + "\n".join(rows) + "\n"


def d_reds(out):
    return [l for l in out.splitlines() if l.startswith("(д) form: RED --") and "«Содержание»" in l]


@pytest.mark.parametrize("contents,names,ids,wants", [
    ("| B-230 | B-015 | `findings/x.md` |", ["x.md"], ["B-230", "B-015"], []),                       # AT: exactly once
    ("| B-230 | B-015 |", ["x.md"], ["B-230", "B-015"], ["findings/x.md 0 times"]),                  # K1: BEYOND, below
    ("| B-230 | B-015 | x.md | x.md |", ["x.md"], ["B-230", "B-015"], ["findings/x.md 2 times"]),    # K2: BEYOND, above
    ("| B-230 | B-015 | ax.md |", ["x.md"], ["B-230", "B-015"], ["findings/x.md 0 times"]),         # K6: a longer name is not this one
    ("| B-230 | B-015 | ax.md x.md |", ["x.md"], ["B-230", "B-015"], []),                            # ... and does not spoil the real one
    ("| B-230 | B-015 | `x.md` |", ["x.md", "ax.md"], ["B-230", "B-015"], ["findings/ax.md 0 times"]),
    ("| B-230 | B-015 |\n```\nx.md\n```", ["x.md"], ["B-230", "B-015"], ["findings/x.md 0 times"]),   # only inside a fence: not a row
    ("| B-230 | B-015 |\n<!-- x.md -->", ["x.md"], ["B-230", "B-015"], ["findings/x.md 0 times"]),   # only inside a comment
    ("| B-230 | B-015 | x.md\n```\nnever closed", ["x.md"], ["B-230", "B-015"], ["is never closed"]),   # a fence without end: one refusal, never a pass
    ("| B-230 | x.md |", ["x.md"], ["B-230", "B-015"], ["B-015 0 times"]),                            # K5: a row id is absent
    ("| B-230 | B-015 | B-015 | x.md |", ["x.md"], ["B-230", "B-015"], ["B-015 2 times"]),
    ("| B-230 | B-0150 | x.md |", ["x.md"], ["B-230", "B-015"], ["B-015 0 times"]),                  # B-015 is not B-0150 (whole token)
    ("| B-230 | B-015 |", [], [], []),                                                               # nothing owed: no red (empty pile)
])
def test_f628_contents_problems_pure(contents, names, ids, wants):
    got = piles.contents_problems(contents, ids, names)
    assert len(got) == len(wants) and all(w in g for w, g in zip(wants, got)), got


@needs_git
def test_k1_k2_k5_a_staged_finding_or_row_id_missing_or_repeated_in_the_contents_is_red_naming_it_and_the_card(tree, cli):
    put(tree, FOUND, finding_text("—"))
    put(tree, "plans/piles/forge/README.md", contents_card("| B-230 | B-015 |"))
    stage(tree, "plans/piles")
    code, out = cli(tree, "check")
    reds = d_reds(out)
    assert code == 2 and len(reds) == 1 and "findings/20261014-x.md 0 times" in reds[0] and "plans/piles/forge/README.md" in reds[0], out
    assert "add its row" in reds[0]                                                    # what to do, in the red
    put(tree, "plans/piles/forge/README.md", contents_card("| B-230 | B-015 | x |", "| `20261014-x.md` | y |", "| 20261014-x.md |"))
    stage(tree, "plans/piles")
    reds = d_reds(cli(tree, "check")[1])
    assert len(reds) == 1 and "20261014-x.md 2 times" in reds[0]
    put(tree, "plans/piles/forge/README.md", contents_card("| B-230 | `20261014-x.md` |"))
    stage(tree, "plans/piles")
    reds = d_reds(cli(tree, "check")[1])
    assert len(reds) == 1 and "B-015 0 times" in reds[0]
    put(tree, "plans/piles/forge/README.md", contents_card("| B-230 | B-015 | `20261014-x.md` |"))
    stage(tree, "plans/piles")
    assert d_reds(cli(tree, "check")[1]) == []                                          # the positive control


@needs_git
def test_k3_a_card_without_a_contents_section_is_not_judged_by_item_1(tree, cli):
    put(tree, FOUND, finding_text("—"))                                                 # E-D1-1: the older form
    stage(tree, "plans/piles")
    assert d_reds(cli(tree, "check")[1]) == []


@needs_git
def test_the_name_in_another_piles_card_does_not_count(tree, cli):
    put(tree, FOUND, finding_text("—"))
    put(tree, "plans/piles/forge/README.md", contents_card("| B-230 | B-015 |"))
    put(tree, "plans/piles/report-delivery/README.md", card_text("report-delivery", "Report", [], "F08") + "\n## Содержание\n\n| 20261014-x.md |\n")
    stage(tree, "plans/piles")
    reds = d_reds(cli(tree, "check")[1])
    assert len(reds) == 1 and "findings/20261014-x.md 0 times" in reds[0] and "forge/README.md" in reds[0]


@needs_git
def test_k4_an_untaken_batch_needs_the_brief_heading_and_a_taken_one_is_not_judged(tree, cli):
    put(tree, "plans/piles/forge/batch-1-foundation.md", batch_text("forge", 1, "ожидает", nodes=[node("F0-1")], brief=False))
    edit(tree, "plans/piles/forge/README.md", "| 1 | фундамент | B-230 | L | в работе", "| 1 | фундамент | B-230 | L | ожидает")
    stage(tree, "plans/piles")
    code, out = cli(tree, "check")
    assert code == 2 and "an untaken batch has no «## Бриф» heading -- write it from plans/piles/_template/batch.md" in out, out
    put(tree, "plans/piles/forge/batch-1-foundation.md", batch_text("forge", 1, "ожидает", nodes=[node("F0-1")], pre=BRIEF))
    stage(tree, "plans/piles")
    assert cli(tree, "check")[0] == 0                                                   # E-D1-3: with the heading: green
    put(tree, "plans/piles/forge/batch-1-foundation.md", batch_text("forge", 1, "в работе", nodes=[node("F0-1")]))
    edit(tree, "plans/piles/forge/README.md", "| 1 | фундамент | B-230 | L | ожидает", "| 1 | фундамент | B-230 | L | в работе")
    stage(tree, "plans/piles")
    code, out = cli(tree, "check")
    assert code == 0 and "«## Бриф»" not in out, out                                    # a taken batch: frozen text, never asked to change


@needs_git
def test_a_missing_nodes_heading_of_an_untaken_batch_is_named_too(tree, cli):
    text = batch_text("forge", 1, "ожидает", nodes=[node("F0-1")], pre=BRIEF).replace("## Узлы", "## Узел")
    form_case(tree, cli, text, "an untaken batch has no «## Узлы» heading")


@needs_git
def test_check_d_card_slug_and_finding_header_red(tree, cli):
    edit(tree, "plans/piles/forge/README.md", "# Forge (`forge`)", "# Forge (`other`)")
    stage(tree, "plans/piles")
    code, out = cli(tree, "check")
    assert code == 2 and "folder name wins" in out
    put(tree, "plans/piles/forge/README.md", card_text("forge", "Forge", [ROW1, ROW2]))
    put(tree, "plans/piles/forge/findings/B-102-x.md", "# t\n\nбез шапки\n")
    stage(tree, "plans/piles")
    code, out = cli(tree, "check")
    assert code == 2 and "no header line" in out


@needs_git
def test_check_d_judges_only_staged_files(tree, cli):
    put(tree, "plans/piles/forge/batch-1-foundation.md", batch_text("forge", 1, nodes=[node("F0-1", "—")]))
    commit(tree, "a form defect that landed")
    put(tree, "plans/piles/forge/findings/B-102-x.md", finding_text("B-102"))
    stage(tree, "plans/piles/forge/findings/B-102-x.md")
    assert cli(tree, "check")[0] == 0
    assert cli(tree, "check", "--all")[0] == 2


@needs_git
def test_check_staged_deletion_is_not_judged_as_a_file(tree, cli):
    put(tree, "plans/piles/forge/findings/B-102-x.md", finding_text("B-102"))
    commit(tree, "add a finding")
    (tree / "plans/piles/forge/findings/B-102-x.md").unlink()
    stage(tree, "plans/piles")
    code, out = cli(tree, "check")
    assert code == 0 and "RED" not in out                                      # a path in the staged list that is gone is a deletion


@needs_git
def test_check_d_template_is_not_judged(tree, cli):
    put(tree, "plans/piles/_template/batch.md", "# <Кучка> — пачка N\n\nничего\n")
    stage(tree, "plans/piles/_template")
    code, out = cli(tree, "check")
    assert code == 0 and "RED" not in out


# ---------------------------------------------------------------- (д) row-id coverage of the nodes (t-769, F5-3)

def what_node(i, what):
    n = node(i)
    n[2] = what
    return n


def cover(tree, members, whats, status="в работе", contents=True, extra_rows=()):
    """A forge card whose row 1 holds `members` (the Строки cell) and a batch file whose nodes have the given «Что» cells."""
    card = card_text("forge", "Forge", [["1", "фундамент", members, "L", status, "Ира", "`main`", "—"], *extra_rows])
    put(tree, "plans/piles/forge/README.md", card.replace("## Входящие", "## Содержание\n\nx\n\n## Входящие") if contents else card)
    put(tree, "plans/piles/forge/batch-1-foundation.md",
        batch_text("forge", 1, status, [what_node("F1-%d" % (k + 1), w) for k, w in enumerate(whats)]))


def cover_reds(tree):
    t = piles.load_tree(tree, tolerant=True)
    return [r.msg for v in t.all_views() for r in piles._coverage_reds(t, v, t.piles[v.slug].card_rel)]


def test_d_coverage_exactly_one_node_per_row_id_passes(tree):
    cover(tree, "B-230, B-015", ["B-230: делает раз", "B-015, затем так"])
    assert cover_reds(tree) == []


def test_d_coverage_negative_control_zero_and_two_nodes_are_red_naming_batch_id_and_count(tree):
    cover(tree, "B-230, B-015", ["B-230: делает", "ничего"])
    reds = cover_reds(tree)
    assert len(reds) == 1 and "batch forge/1" in reds[0] and "B-015" in reds[0] and "0 nodes" in reds[0], reds
    cover(tree, "B-230", ["B-230: раз", "и снова B-230"])
    reds = cover_reds(tree)
    assert len(reds) == 1 and "B-230" in reds[0] and "2 nodes (F1-1, F1-2)" in reds[0], reds


def test_d_coverage_one_node_may_carry_several_members_and_repeat_an_id(tree):
    cover(tree, "B-230, B-015", ["B-230 и B-015: один узел, B-230 дважды"])
    assert cover_reds(tree) == []


def test_d_coverage_a_partial_member_may_stand_in_several_nodes_but_not_in_none(tree):
    cover(tree, "B-230 (а), B-015", ["B-230: часть один", "B-230: часть два, B-015"])
    assert cover_reds(tree) == []
    cover(tree, "B-230 (а), B-015", ["B-015"])
    reds = cover_reds(tree)
    assert len(reds) == 1 and "B-230" in reds[0] and "0 nodes" in reds[0], reds


@pytest.mark.parametrize("start", ["Сверка", "сверка", "**Проверить**", "`проверить`", "> проверить"])
def test_d_coverage_a_cross_check_node_counts_neither_toward_one_nor_as_outside(tree, start):
    cover(tree, "B-230", ["B-230: делает", "%s B-230 и B-999 по карте" % start])
    assert cover_reds(tree) == []


def test_d_coverage_a_node_that_only_mentions_a_cross_check_word_is_an_ordinary_node(tree):
    cover(tree, "B-230", ["B-230: делает", "Не сверка B-230"])
    assert len(cover_reds(tree)) == 1


def test_d_coverage_an_id_outside_the_row_is_red_unless_it_belongs_to_another_row_of_the_card(tree):
    cover(tree, "B-230", ["B-230: делает, как B-999"])
    reds = cover_reds(tree)
    assert len(reds) == 1 and "node F1-1 names B-999" in reds[0] and "forge/1" in reds[0], reds
    cover(tree, "B-230", ["B-230: делает после B-015"], extra_rows=[["2", "потом", "B-015", "M", "ожидает", "—", "—", "—"]])
    assert cover_reds(tree) == []                                             # a sibling batch's id is a reference, not a claim


def test_d_coverage_an_id_inside_a_file_name_is_not_an_id(tree):
    cover(tree, "B-230", ["B-230: см. `findings/B-102-x.md` и plans/B-103/y"])
    assert cover_reds(tree) == []


def test_d_coverage_a_row_without_members_a_closed_batch_and_a_card_without_contents_are_not_judged(tree):
    cover(tree, "—", ["B-999 где угодно", "и B-998"])
    assert cover_reds(tree) == []
    cover(tree, "B-230", ["ничего"], status="закрыта")
    assert cover_reds(tree) == []                                             # history: frozen for good
    cover(tree, "B-230", ["ничего"], contents=False)
    assert cover_reds(tree) == []                                             # not in the t-717 form: the gate does not ask
    cover(tree, "B-230", ["ничего"])
    assert len(cover_reds(tree)) == 1                                         # the same tree with «Содержание» is judged


def test_d_coverage_runs_in_the_gate_and_its_door_is_the_existing_one(tree, cli):
    cover(tree, "B-230", ["ничего"])
    code, out = cli(tree, "check", "--all")
    assert code == 2 and "(д) form: RED -- batch forge/1: the row id B-230 stands in the «Что» of 0 nodes" in out, out
    code, out = cli(tree, "check", "--all", "--msg-file", msg(tree, "s\n\npiles-skip: д -- the nodes are written next\n"))
    assert code == 0 and "(д) form: RED, passed by the commit message" in out, out
