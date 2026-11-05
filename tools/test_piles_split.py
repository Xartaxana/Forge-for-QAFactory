"""Tests for tools/piles_split.py (F0-2b): the one-shot `split` of plans/BACKLOG.md over the piles.

One session fixture builds a small tree (a mini BACKLOG written for `split`, a features registry, the forge and
report-delivery cards); every test works on a COPY of it under tmp_path (--repo). No git in the copies: `split` then
indexes the files by walking tools/ docs/ plans/ and the package, which is what the tests need. The GIT_* variables are
scrubbed (a hook run must not point `git ls-files` at the real index).
"""
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys

import pytest

TOOLS = pathlib.Path(__file__).resolve().parent
REAL = TOOLS.parent
sys.path.insert(0, str(TOOLS))
import piles  # noqa: E402
import piles_split as ps  # noqa: E402
from test_piles import GIT_VARS, batch_text, card_text, clean_env, node, put  # noqa: E402


@pytest.fixture(autouse=True)
def _scrub_git_env(monkeypatch):
    for k in GIT_VARS:
        monkeypatch.delenv(k, raising=False)


HEAD5 = "| id | что сделать | почему | источник | принципы |\n|---|---|---|---|---|\n"

BACKLOG = """# Бэклог фабрики

## Как вести

Текст.

## 1. Сравнительный прогон

| id | что | детали |
|---|---|---|
| B-015 | Прогон сравнения. | детали прогона |

## 2. Трение кода о роль

""" + HEAD5 + """| B-020 | **Редакторы артефактов.** Точечно. | почему 20 | источник 20 | P1 |

## 7. Релизы, приёмки, инфраструктура разработки

""" + HEAD5 + """| B-102 | **Дыра в `a|b` разборе.** ждёт слова владельца. | свидетель `x|y` | источник 1 | P1 |
| B-135 | **Сессия.** `tools/session_context.py` | почему 135 | closed by code: X; remainder: B-171 | P2 |
| B-162 | **Пути.** `tools/session_context.py` | почему 162 | источник 162 | P2 |
| B-221 | **Развилка F10.** `scripts/traceability.py` | почему 219 | источник 219 | P3 |
| B-230 | **Кучки.** | почему 230 | владелец | P4 |
| B-240 | **Общий.** общая фича [F03] | почему 240 | источник 240 | P1 |
| B-241 | **Ничей.** фича без карточки [F10] | почему 241 | источник 241 | P1 |
| B-242 | **Метка вне реестра.** [F99] | почему 242 | источник 242 | P1 |
| B-243 | **Два файла.** `tools/session_context.py` и `scripts/traceability.py` | почему 243 | источник 243 | P1 |
| B-244 | **Старое решение.** решение владельца 29.09 | почему 244 | источник 244 | P1 |
| B-272 | **Первая пачка гейтов.** | почему 272 | источник 272 | P1 |
| B-292 | **Остатки гейтов.** [F07] | почему 292 | источник 292 | P1 |

## 10. Ошибки

| id | что сделать | свидетель | источник | принципы |
|---|---|---|---|---|
| B-125 | **Свидетельская.** `tools/session_context.py` | свидетель 125 | источник 125 | P5 |

## 12. Миграция исправлений

""" + HEAD5 + """| B-308 | **Два тега** [F13, F15] (= B-303) | почему 308 | источник 308 | P5 |
| B-309 | **Хвост.** `tools/session_context.py` | почему 309 | источник 309 | P5 |

## Закрыто

""" + HEAD5 + """| B-001 | **Старое.** | почему | закрыто кодом: model-rates.json:83 | P1 |
| B-417 | **Храповик.** | почему | влито `7848917` + база `7ed70ac` | P1 |
| B-418 | **Красный main.** | пайплайны после: 7883565 | источник | P1 |
"""

FEATURES = {"schema_version": 1, "features": [
    {"id": "F03", "name": "stand", "root": "package", "globs": ["scripts/probe_by_code.py"], "stages": [], "words": []},
    {"id": "F07", "name": "words", "root": "package", "globs": ["scripts/gate_brief.py"], "stages": [], "words": []},
    {"id": "F08", "name": "coverage", "root": "package", "globs": ["scripts/traceability.py"], "stages": [], "words": []},
    {"id": "F10", "name": "manual", "root": "package", "globs": ["scripts/manual_capture.py"], "stages": [], "words": []},
    {"id": "F13", "name": "report", "root": "package", "globs": ["scripts/finalize_task.py"], "stages": [], "words": []},
    {"id": "F15", "name": "hygiene", "root": "package", "globs": ["CHANGELOG.md"], "stages": [], "words": []},
    {"id": "F19", "name": "forge", "root": "repo", "globs": ["tools/**", "plans/**", "*"], "stages": [], "words": []},
]}

FORGE_ROWS = [["1", "фундамент", "B-230, B-162 (пути)", "L", "в работе", "Ира", "`main` (x)", "—"],
              ["2", "потом", "B-309 (г)–(и)", "M", "ожидает", "—", "—", "—"]]


def build_mini(root):
    put(root, "plans/BACKLOG.md", BACKLOG)
    put(root, "plans/features.json", json.dumps(FEATURES))
    put(root, "plans/piles/forge/README.md", card_text("forge", "Forge", FORGE_ROWS))
    put(root, "plans/piles/forge/batch-1-foundation.md",
        batch_text("forge", 1, nodes=[node("F0-1", "`tools/a.py`")]))
    put(root, "plans/piles/report-delivery/README.md", card_text("report-delivery", "Report", [], "F08, F12, F13"))
    put(root, "plans/piles/_template/README.md", (REAL / "plans/piles/_template/README.md").read_text(encoding="utf-8"))
    for rel in ("ai-packages/qa-factory/scripts/traceability.py", "ai-packages/qa-factory/scripts/probe_by_code.py",
                "tools/session_context.py", ".claude/worktrees/w1/tools/worktree_only.py"):
        put(root, rel, "# stub\n")


@pytest.fixture(scope="session")
def session_tree(tmp_path_factory):
    root = tmp_path_factory.mktemp("splitmini") / "repo"
    root.mkdir()
    build_mini(root)
    return root


@pytest.fixture
def tree(session_tree, tmp_path):
    dst = tmp_path / "repo"
    shutil.copytree(session_tree, dst)
    return dst


@pytest.fixture
def run(capsys):
    def go(root, *args):
        code = ps.main(["--repo", str(root), *map(str, args)])
        return code, capsys.readouterr().out
    return go


def snapshot(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(pathlib.Path(root).rglob("*")) if p.is_file()}


def finding(root, slug, ident):
    hits = sorted((root / "plans/piles" / slug / "findings").glob(ident + "-*.md")) if (root / "plans/piles" / slug / "findings").is_dir() else []
    return hits[0] if hits else None


def where(root, ident):
    return sorted(p.parts[-3] for p in (root / "plans/piles").glob("*/findings/%s*.md" % ident))


def unresolved_ids(out):
    block = out.split("UNRESOLVED rows:\n", 1)[1].split("--assign lines", 1)[0]
    return [l.split()[0] for l in block.splitlines() if l.strip()]


ASSIGN_ALL = ["B-102=forge", "B-240=execution-probes", "B-241=forge", "B-242=forge", "B-244=forge"]


def settle(run, root):
    """Place every UNRESOLVED row of the mini tree by --assign: a clean run (exit 0)."""
    code, out = run(root, *[a for x in ASSIGN_ALL for a in ("--assign", x)])
    assert code == 0, out
    return out


# ================================================================== placement

def test_split_places_by_tag_section_and_path(tree, run):
    code, out = run(tree)
    assert code == 2                                                    # B-102, B-240, B-241, B-242, B-244 stay UNRESOLVED
    assert where(tree, "B-020") == ["roles-context"]                    # no tag, section 2
    assert where(tree, "B-135") == ["forge"]                            # no tag, section 7, tools/session_context.py -> F19
    assert where(tree, "B-221") == ["report-delivery"]                  # scripts/traceability.py -> F08
    assert where(tree, "B-308") == ["report-delivery"]                  # tag F13
    assert where(tree, "B-125") == ["forge"]                            # section 10, by its path
    assert piles.REPO and True        # the count is the OPEN rows only
    assert "piles split: 17 open rows in plans/BACKLOG.md" in out


def test_split_two_tags_takes_first_and_lists_multi_tag(tree, run):
    code, out = run(tree)
    assert "B-308 [F13, F15] -> F13" in out.split("MULTI-TAG", 1)[1]
    assert where(tree, "B-308") == ["report-delivery"]                  # F13, not F15 (package-ci)


def test_split_bare_F10_is_not_a_tag(tree, run):
    """B-221 says 'Развилка F10': a bare number is no tag. Taken for one it would be 'claimed by no card'."""
    code, out = run(tree)
    assert where(tree, "B-221") == ["report-delivery"]
    assert "B-221" not in out.split("UNRESOLVED rows:", 1)[1]


def test_split_no_tag_no_path_is_unresolved_exit_2(tree, run):
    code, out = run(tree)
    assert code == 2
    assert "B-102 [section 7]: section 7: no tag, no path" in out
    assert where(tree, "B-102") == []                                   # nothing guessed
    assert "piles split: 5 row(s) UNRESOLVED" in out
    assert where(tree, "B-135") == ["forge"]                            # the rest is still written


def test_split_unknown_tag_listed_and_treated_untagged(tree, run):
    code, out = run(tree)
    assert "B-242 [F99]" in out.split("UNKNOWN TAG", 1)[1]
    assert "B-242 [section 7]: section 7: no tag, no path" in out       # untagged, so by section/path: nothing


def test_split_feature_claimed_by_two_cards_is_unresolved(tree, run):
    code, out = run(tree)
    assert "B-240 [F03]: feature F03 is claimed by 2 cards: execution-probes, stand-and-sources" in out
    assert "--assign B-240=<execution-probes|stand-and-sources>" in out    # the line to copy, candidates named
    assert where(tree, "B-240") == []


def test_split_feature_claimed_by_no_card_is_unresolved(tree, run):
    code, out = run(tree)
    assert "B-241 [F10]: feature F10 is claimed by no card" in out
    assert where(tree, "B-241") == []


def test_split_first_file_by_text_decides_and_row_is_contested(tree, run):
    code, out = run(tree)
    assert where(tree, "B-243") == ["forge"]                            # tools/session_context.py comes first in the text
    assert "B-243 -> forge; also report-delivery (traceability.py)" in out.split("CONTESTED", 1)[1]


def test_split_assign_places_unresolved_rows(tree, run):
    out = settle(run, tree)
    assert where(tree, "B-102") == ["forge"] and where(tree, "B-240") == ["execution-probes"]
    assert "UNRESOLVED" not in out


def test_split_assign_battery(tree, run):
    before = snapshot(tree)
    cases = [(["B-015"], '--assign "B-015": expected B-nnn=<slug>'),
             (["B-999=forge"], "B-999 is not an open row"),
             (["B-001=forge"], "B-001 is not an open row"),                     # a CLOSED row is no open row
             (["B-102=nopile"], 'no pile "nopile"'),
             (["B-102=forge", "B-102=live-runs"], "--assign B-102 is given twice (forge, live-runs)"),
             (["B-230=forge"], "B-230 is already placed (batch forge/1)"),
             (["B-162=live-runs"], "B-162 is already placed (partial member of forge/1 (пути))"),
             (["B-102=../x"], "expected B-nnn=<slug>")]
    for assign, text in cases:
        code, out = run(tree, *[a for x in assign for a in ("--assign", x)])
        assert code == 1 and text in out, (assign, out)
        assert snapshot(tree) == before                                        # a refusal writes nothing, not even cards


def test_split_assign_resolves_a_row_partial_in_two_piles(tree, run):
    """A member named partially by cards of TWO piles has no home by rule: --assign decides, and is accepted."""
    put(tree, "plans/piles/report-delivery/README.md",
        card_text("report-delivery", "Report", [["1", "x", "B-020 (часть)", "S", "ожидает", "—", "—", "—"]], "F08, F12, F13"))
    put(tree, "plans/piles/forge/README.md",
        card_text("forge", "Forge", FORGE_ROWS + [["3", "y", "B-020 (другая часть)", "S", "ожидает", "—", "—", "—"]]))
    code, out = run(tree, "--dry-run")
    assert "B-020 forge/3 (другая часть); report-delivery/1 (часть) -> roles-context" in out    # rule g: its section
    code, out = run(tree, "--assign", "B-020=forge", "--dry-run")
    assert "B-020 forge/3 (другая часть); report-delivery/1 (часть) -> forge" in out
    run(tree, "--assign", "B-020=forge")
    text = finding(tree, "forge", "B-020").read_text(encoding="utf-8")
    assert "Член пачки `forge/3` частично: (другая часть)" in text and "Член пачки `report-delivery/1` частично: (часть)" in text


# ================================================================== batches, partial members, the cards

def test_split_whole_batch_member_gets_no_finding(tree, run):
    code, out = run(tree)
    assert where(tree, "B-230") == []                                   # named whole in forge/1 (an existing card)
    assert where(tree, "B-272") == []                                   # first batch of the card split itself made
    assert where(tree, "B-015") == []                                   # first batch of live-runs
    assert "whole in a batch row: 3" in out
    assert "live-runs 1 (batch 1, findings 0)" in out


def test_split_partial_member_gets_remainder_finding_in_card_pile(tree, run):
    code, out = run(tree)
    assert where(tree, "B-162") == ["forge"] and where(tree, "B-309") == ["forge"]
    assert where(tree, "B-292") == ["gates-and-words"]                  # the tag says F07 too, but the card row decides
    text = finding(tree, "forge", "B-309").read_text(encoding="utf-8")
    assert "Член пачки `forge/2` частично: (г)–(и) -- остаток строки лежит в этой находке." in text
    assert "B-309 forge/2 (г)–(и) -> forge" in out.split("PARTIAL", 1)[1]
    assert "partial: 3 (inside the written)" in out


def test_split_cards_are_made_from_the_plan_table_and_the_template(tree, run):
    forge_before = (tree / "plans/piles/forge/README.md").read_bytes()
    code, out = run(tree)
    assert (tree / "plans/piles/forge/README.md").read_bytes() == forge_before         # an existing card is left as is
    made = {p.parent.name for p in (tree / "plans/piles").glob("*/README.md")}
    assert len(ps.PILE_TABLE) == 11 and {s.slug for s in ps.PILE_TABLE} <= made and "_template" in made
    card = piles.parse_card(piles.read_text(tree / "plans/piles/live-runs/README.md"), "plans/piles/live-runs/README.md")
    assert card.errors == [] and card.title_slug == "live-runs" and card.priority == "П1" and card.features == []
    assert [(r.n, r.status, r.who) for r in card.rows] == [(1, "ожидает", "—")]
    assert [m.id for m in card.rows[0].members] == ["B-015"]               # the rest of the plan's ids are no rows of the mini backlog
    k1 = piles.parse_card(piles.read_text(tree / "plans/piles/gates-and-words/README.md"), "x/README.md")
    assert [(m.id, m.qualifier) for m in k1.rows[0].members] == [("B-272", ""), ("B-292", "(остатки)")]
    stands = (tree / "plans/piles/execution-probes/README.md").read_text(encoding="utf-8")
    assert "приоритет: П2 | фичи: F11, F03 (пробы), F09 | стенд: нужен (M1–M3 на проекте) | зона: —" in stands
    assert "Взятая пачка заморожена" in stands and "## Вопросы владельцу" in stands          # the template's own text


def test_split_closed_first_batch_ids_are_dropped_with_a_report_line(tree, run):
    code, out = run(tree)
    assert "closed in plans/BACKLOG.md: B-417, B-418" in out
    card = piles.read_text(tree / "plans/piles/live-runs/README.md")
    assert "B-417" not in card and "B-418" not in card
    assert "live-runs/1: W7, «затем»" in out.split("NON-ID ITEMS IN CARD ROWS", 1)[1]
    assert "not a row of plans/BACKLOG.md: B-" in out.split("DROPPED FROM CARD ROWS", 1)[1]        # the ids the mini backlog lacks


def test_split_two_cards_claiming_one_batch_id_is_unresolved_exit_2(tree, run):
    """NEGATIVE CONTROL: the same id named whole in two batch rows is nobody's -- nothing is written for it."""
    put(tree, "plans/piles/report-delivery/README.md",
        card_text("report-delivery", "Report", [["1", "x", "B-020", "S", "ожидает", "—", "—", "—"]], "F08, F12, F13"))
    put(tree, "plans/piles/forge/README.md",
        card_text("forge", "Forge", FORGE_ROWS + [["3", "y", "B-020", "S", "ожидает", "—", "—", "—"]]))
    code, out = run(tree, *[a for x in ASSIGN_ALL for a in ("--assign", x)])
    assert code == 2
    assert "B-020 [section 2]: named whole in 2 batch rows; forge/3, report-delivery/1" in out
    assert "B-020: --assign cannot help" in out and where(tree, "B-020") == []
    code, out = run(tree, "--assign", "B-020=forge")
    assert code == 1 and "B-020 is already placed (batch" in out
    put(tree, "plans/piles/forge/README.md", card_text("forge", "Forge", FORGE_ROWS))        # the control: one claim
    code, out = run(tree)
    assert code == 0 and where(tree, "B-020") == []                                           # whole in ONE batch: in the batch


# ================================================================== the finding

def test_split_finding_keeps_every_cell_verbatim(tree, run):
    settle(run, tree)
    path = finding(tree, "forge", "B-102")
    text = path.read_text(encoding="utf-8")
    assert text.startswith("# Дыра в `a|b` разборе\n")
    assert "id: B-102 | кучка: `forge` | от: источник 1 | приоритет: — | кандидат наверх: нет" in text
    assert "Что не так / что сделать: **Дыра в `a|b` разборе.** ждёт слова владельца." in text
    assert "Свидетель: свидетель `x|y`" in text and "Принципы и правила: P1" in text
    assert "Решение владельца нужно: да — ждёт слова владельца" in text
    assert "<!-- piles split: plans/BACKLOG.md, раздел 7 «Релизы, приёмки, инфраструктура разработки»;" in text
    row = next(l for l in BACKLOG.splitlines() if l.startswith("| B-102 |"))
    assert "```\n%s\n```" % row in text                                     # the row line itself, verbatim, fenced
    fi = piles.parse_finding(text, piles.PILES_REL + "/forge/findings/" + path.name)
    assert fi.errors == [] and fi.id == "B-102" and fi.pile == "forge"
    assert b"\r" not in path.read_bytes() and not path.read_bytes().startswith(b"\xef\xbb\xbf")     # LF, no BOM


def test_split_section_10_witness_column_and_three_column_rows(tree, run):
    run(tree)
    t10 = finding(tree, "forge", "B-125").read_text(encoding="utf-8")
    assert "Свидетель: свидетель 125" in t10 and "от: источник 125" in t10     # the свидетель column is the witness
    t1 = (tree / "plans/piles/live-runs/README.md")
    put(tree, "plans/piles/live-runs/README.md", t1.read_text(encoding="utf-8").replace("B-015", "B-9999"))
    run(tree)
    t3 = finding(tree, "live-runs", "B-015").read_text(encoding="utf-8")       # a 3-column row: детали -> witness, no source
    assert "Свидетель: детали прогона" in t3 and "от: plans/BACKLOG.md, раздел 1" in t3


def test_split_source_cell_empty_reads_the_section(tree, run):
    text = BACKLOG.replace("| B-020 | **Редакторы артефактов.** Точечно. | почему 20 | источник 20 | P1 |",
                           "| B-020 | **Редакторы артефактов.** Точечно. | почему 20 | | P1 |")
    put(tree, "plans/BACKLOG.md", text)
    run(tree)
    assert "от: plans/BACKLOG.md, раздел 2 |" in finding(tree, "roles-context", "B-020").read_text(encoding="utf-8")


def test_split_owner_question_lists_with_negative_control(tree, run):
    code, out = run(tree)
    block = out.split("OWNER QUESTION", 1)[1].split("MULTI-TAG", 1)[0]
    assert 'B-102 "ждёт слова владельца"' in block
    assert "B-244" not in block                                          # 'решение владельца 29.09' is a past decision
    text = finding(tree, "forge", "B-243").read_text(encoding="utf-8")
    assert "Решение владельца нужно: нет (фраза не найдена)" in text


def test_split_owner_phrase_controls_on_the_real_backlog():
    """P11: B-229 'решает владелец' must match, B-006 'решение владельца 29.09' must not (the real rows)."""
    bl = piles.parse_backlog_rows(piles.read_text(REAL / "plans/BACKLOG.md"))
    by = {r.id: r for r in bl.rows if not r.closed}
    assert ps.owner_phrase(by["B-229"].text) == "решает владелец"
    assert ps.owner_phrase(by["B-006"].text) is None
    assert ps.owner_phrase("не подтверждён владельцем") == "не подтверждён владельцем"


def test_split_closed_by_text_list_is_advice_and_rows_are_still_placed(tree, run):
    code, out = run(tree)
    block = out.split("CLOSED BY TEXT", 1)[1].split("OWNER QUESTION", 1)[0]
    assert "B-308" in block and "= B-303" in block                      # '= другая строка'
    assert "B-135" in block and "closed by code" in block               # 'closed by code: X; remainder: B-171'
    assert where(tree, "B-135") == ["forge"] and where(tree, "B-308") == ["report-delivery"]     # placed as usual (Р18 a)


@pytest.mark.parametrize("what,title", [
    ("**Точный заголовок.** остальное", "Точный заголовок"),
    ("Без жирного. Второе предложение", "Без жирного"),
    ("Без точки в конце ячейки", "Без точки в конце ячейки"),
    ("**Двоеточие:** хвост", "Двоеточие"),
    ("  много   пробелов  ", "много пробелов"),
    ("", "B-777"),
])
def test_split_title_forms(what, title):
    assert ps.finding_title(what, "B-777") == title


def test_split_title_limit_at_100_and_101():
    at100 = ("a" * 9 + " ") * 9 + "a" * 10                                 # exactly 100 characters, ten words
    assert len(at100) == 100 and ps.finding_title(at100, "B-1") == at100         # AT the limit: whole, no ellipsis
    over = at100 + "b"                                                       # 101 characters: the last word is cut off
    assert len(over) == 101
    assert ps.finding_title(over, "B-1") == ("a" * 9 + " ") * 8 + "a" * 9 + "…"
    assert len(ps.finding_title(over, "B-1")) <= 100                         # the cut title never exceeds the limit
    assert ps.finding_title("x" * 150, "B-1") == "x" * 99 + "…"                # no space at all: a hard cut


@pytest.mark.parametrize("title,slug", [
    ("Дыра в разборе", "dyra-v-razbore"),
    ("Щука, ёж и ъ-знак: ЭЮЯ", "shchuka-ezh-i-znak-eyuya"),
    ("один два три четыре пять шесть семь", "odin-dva-tri-chetyre-pyat-shest"),         # 6 words, the 7th is dropped
    ("`tools/x.py` ждёт", "tools-x-py-zhdet"),
    ("— — —", ""),
])
def test_split_slug_translit(title, slug):
    assert ps.translit_slug(title) == slug


def test_split_slug_limit_at_48_and_49():
    w48 = "a" * 24 + " " + "b" * 23                                       # 24 + '-' + 23 = 48 characters
    assert ps.translit_slug(w48) == "a" * 24 + "-" + "b" * 23 and len(ps.translit_slug(w48)) == 48
    w49 = "a" * 24 + " " + "b" * 24                                        # 49: cut at the last hyphen
    assert ps.translit_slug(w49) == "a" * 24
    assert ps.translit_slug("z" * 60) == "z" * 48                           # a single long word: a hard cut at 48
    assert ps.finding_name("B-5", "") == "B-5.md" and ps.finding_name("B-5", "Раз два") == "B-5-raz-dva.md"
    six = "а б в г д е ж"                                                   # 7 one-letter words
    assert ps.translit_slug(six) == "a-b-v-g-d-e"


def test_split_written_names_fit_the_finding_name_form_and_the_gate(tree, run, capsys):
    settle(run, tree)
    names = [p for p in (tree / "plans/piles").glob("*/findings/*.md")]
    assert len(names) >= 12
    for p in names:
        assert piles.FINDING_NAME_RE.match(p.name), p.name
        assert len(p.name.split("-", 2)[2][:-3]) <= 48
    capsys.readouterr()
    piles.main(["--repo", str(tree), "check", "--all"])
    out = capsys.readouterr().out
    # split writes the card from the template with an EMPTY «Содержание» (the Lead fills the rows by hand, t-717 form); since D6-D1
    # check (д) judges those rows, so the contents reds are the only ones allowed here -- every other (д) red still fails the test
    out = "\n".join(l for l in out.split("\n") if "«Содержание» names" not in l)
    assert out.count("(д) form: RED") == 0 and "(а) placement: ok" in out, out        # what split wrote passes 2a's own gate
    assert "RED" not in out


def test_split_unparseable_finding_is_unresolved_not_written(tree, run, monkeypatch):
    real = piles.parse_finding
    monkeypatch.setattr(piles, "parse_finding", lambda text, rel: real("# x\n\nno header\n", rel))
    code, out = run(tree)
    assert code == 2 and "the finding made for it would not parse back" in out
    assert not list((tree / "plans/piles").glob("*/findings/*.md"))        # nothing was written for them


# ================================================================== idempotence, dry run, files not to touch

def test_split_second_run_changes_nothing(tree, run):
    settle(run, tree)
    before = snapshot(tree)
    code, out = run(tree)
    assert code == 0 and out.startswith("piles split: nothing to do -- every open row already has its place (17: ")
    assert snapshot(tree) == before


def test_split_second_run_with_unresolved_rows_writes_nothing_new(tree, run):
    run(tree)
    before = snapshot(tree)
    code, out = run(tree)
    assert code == 2 and "wrote 0 card(s) and 0 finding file(s)" in out and "already placed: 9" in out
    assert snapshot(tree) == before


def test_split_never_overwrites_edited_or_moved_finding(tree, run):
    settle(run, tree)
    edited = finding(tree, "forge", "B-135")
    edited.write_bytes(edited.read_bytes() + "\nправка человека\n".encode("utf-8"))
    moved = finding(tree, "forge", "B-125")
    target = tree / "plans/piles/roles-context/findings" / moved.name
    target.parent.mkdir(parents=True, exist_ok=True)
    moved.replace(target)                                                 # the Lead moved it to another pile
    before = snapshot(tree)
    code, out = run(tree)
    assert code == 0 and snapshot(tree) == before                         # by id, not by file name or place
    assert where(tree, "B-125") == ["roles-context"]


def test_split_dry_run_writes_nothing(tree, run):
    before = snapshot(tree)
    code, out = run(tree, "--dry-run")
    assert code == 2 and out.rstrip().endswith("(dry run: nothing written)")
    assert "cards: would write 9" in out and "findings: would write 9;" in out
    assert snapshot(tree) == before


def test_split_does_not_touch_backlog_cards_or_template(tree, run):
    before = snapshot(tree)
    settle(run, tree)
    after = snapshot(tree)
    for rel in ("plans/BACKLOG.md", "plans/features.json", "plans/piles/forge/README.md",
                "plans/piles/report-delivery/README.md", "plans/piles/_template/README.md",
                "plans/piles/forge/batch-1-foundation.md"):
        assert after[rel] == before[rel], rel


def test_split_crlf_backlog_gives_same_findings(tree, run, tmp_path):
    crlf = tmp_path / "crlf"
    shutil.copytree(tree, crlf)
    raw = (crlf / "plans/BACKLOG.md").read_bytes()
    (crlf / "plans/BACKLOG.md").write_bytes(b"\xef\xbb\xbf" + raw.replace(b"\n", b"\r\n"))        # CRLF and a BOM
    run(tree)
    run(crlf)
    a = {k: v for k, v in snapshot(tree).items() if "/findings/" in k or k.endswith("README.md")}
    b = {k: v for k, v in snapshot(crlf).items() if "/findings/" in k or k.endswith("README.md")}
    assert a == b and len(a) > 15


def test_split_missing_closed_heading_refuses(tree, run):
    put(tree, "plans/BACKLOG.md", BACKLOG.replace("## Закрыто", "## Архив"))
    before = snapshot(tree)
    code, out = run(tree)
    assert code == 1 and 'has no "## Закрыто" heading' in out and snapshot(tree) == before


def test_split_missing_template_or_registry_cannot_run(tree, run):
    (tree / "plans/piles/_template/README.md").unlink()
    code, out = run(tree)
    assert code == 1 and "cannot read" in out and "_template" in out
    put(tree, "plans/piles/_template/README.md", "# <Название> (`<slug>`)\n")
    code, out = run(tree)
    assert code == 1 and "no longer has the shape split expects" in out
    (tree / "plans/features.json").write_text("not json", encoding="utf-8")
    code, out = run(tree)
    assert code == 1 and "feature registry" in out


def test_split_file_index_ignores_worktree_copies(tree, tmp_path):
    """E6: a copy of a file under .claude/worktrees never decides the fate of a row, with git or without it."""
    plain = ps.build_index(tree)
    assert "tools/session_context.py" in plain.pset and ".claude/worktrees/w1/tools/worktree_only.py" not in plain.pset
    repo = tmp_path / "gitrepo"
    put(repo, "tools/y.py", "# y\n")
    put(repo, ".claude/worktrees/w/tools/x.py", "# x\n")
    empty = tmp_path / "empty-template"
    empty.mkdir()
    for args in (["init", "-q", "--template=" + str(empty)], ["add", "-A", "-f"]):
        subprocess.run(["git", "-C", str(repo), *args], capture_output=True, env=clean_env(), check=True)
    tracked = subprocess.run(["git", "-C", str(repo), "ls-files"], capture_output=True, env=clean_env(), check=True).stdout
    assert b".claude/worktrees/w/tools/x.py" in tracked                    # the control: git DOES list the copy
    idx = ps.build_index(repo)
    assert "tools/y.py" in idx.pset and not any(p.startswith(".claude/worktrees/") for p in idx.paths)


def test_split_usage_errors_exit_1(tree, run):
    code, out = run(tree, "--bogus")
    assert code == 1 and out.startswith("piles split: usage:")
    code, out = run(tree, "--assign")
    assert code == 1


def test_split_help_names_the_options(capsys):
    with pytest.raises(piles.CannotRun):
        ps.build_parser().parse_args(["--nope"])
    text = ps.build_parser().format_help()
    assert "--dry-run" in text and "--assign" in text
