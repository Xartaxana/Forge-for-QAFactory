"""Coverage of the pile cards: every id of a batch row and every findings file is in the card's «Содержание» exactly once
(t-717 §L Р1/Р5), the card and the batch file carry the agreed headings, the template carries them too, «Зачем» names no B-id
and every node id of an open batch file is `<initials><N>-<n>` (never a B-id) and unique.

The row-id coverage of the NODES (every id of the card row in the «Что» of exactly one node, no id outside the row) moved from
here to the gate: `piles.py check` (д), tools/test_piles_form.py (t-769, F5-3). What stays here is what the gate does not hold.

The checks read the real tree with the parsers of tools/piles.py (no second parser). `conductor` and `forge` were converted to
the card form (t-769: «Дороги», «Содержание»), so no test is skipped for them any more; two things of their old form remain
named below and are not skipped but narrowed: their frozen batch files have no «## Бриф», and their cards have neither
«Что не так сегодня (факты)» nor «Бриф пачки 1» (a frozen batch file is never edited; a card is not padded with empty sections).
Run from the repo root: python -m pytest tools/test_pile_cards_contents.py -q
A pile tree elsewhere (the negative control of the witness): PILES_CARDS_DIR=<copy of plans/piles>.
"""
import os
import pathlib
import re
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import piles  # noqa: E402

REAL = pathlib.Path(__file__).resolve().parent.parent
PILES_DIR = pathlib.Path(os.environ.get("PILES_CARDS_DIR") or REAL / "plans" / "piles")
ID_RE = re.compile(r"(?<![\w/-])B-\d{3,}(?![\w-])")
NODE_ID_RE = re.compile(r"^[A-Z]{1,3}\d-\d+$")           # initials of the pile (C, F, DC, GW, KB) + N-n; "B-419" has no digit before the dash
CARD_HEADINGS = ["## Зачем", "## Что не так сегодня (факты)", "## Пачки", "## Бриф пачки 1", "## Дороги", "## Содержание",
                 "## Входящие", "## Вопросы владельцу"]
BATCH_HEADINGS = ["## Бриф", "## Узлы"]
LEGACY = {"conductor", "forge"}                           # cards that grew «Дороги» and «Содержание» in t-769; their frozen batch files stay as written
LEGACY_CARD_ABSENT = ("## Что не так сегодня (факты)", "## Бриф пачки 1")
LEGACY_BATCH_HEADINGS = ["## Узлы"]
SLUGS = sorted(p.name for p in PILES_DIR.iterdir() if p.is_dir() and not p.name.startswith(("_", ".")))


def section_text(text, heading):
    """The lines between the line `heading` (whole line) and the next `## ` line; None when the heading is absent."""
    out, seen, inside = [], False, False
    for line in text.split("\n"):
        if line.startswith("## "):
            if inside:
                break
            inside = seen = line.rstrip() == heading
        elif inside:
            out.append(line)
    return "\n".join(out) if seen else None


def pile_parts(slug):
    folder = PILES_DIR / slug
    pile = piles.load_pile(REAL, folder)
    return folder, pile


def row_ids_of(pile, n=None):
    return [m.id for r in pile.card.rows if n is None or r.n == n for m in r.members]


@pytest.mark.parametrize("slug", SLUGS)
def test_card_and_batch_headings(slug):
    folder, pile = pile_parts(slug)
    card = (folder / "README.md").read_text(encoding="utf-8")
    lines = [l.rstrip() for l in card.split("\n")]
    wanted = [h for h in CARD_HEADINGS if slug not in LEGACY or h not in LEGACY_CARD_ABSENT]
    assert [h for h in wanted if h not in lines] == [], "%s card lacks headings (a new pile is written from plans/piles/_template/README.md)" % slug
    assert pile.batches, "%s has no batch file" % slug
    for b in pile.batches:
        blines = [l.rstrip() for l in (folder / pathlib.Path(b.path).name).read_text(encoding="utf-8").split("\n")]
        wanted_batch = LEGACY_BATCH_HEADINGS if slug in LEGACY else BATCH_HEADINGS
        # the gate's pure reader (piles.batch_heading_problems, F6-28): one reader of «what a batch file is born with»
        lacking = [h for h in wanted_batch if any("«%s»" % h in why for why in piles.batch_heading_problems("\n".join(blines)))]
        assert lacking == [], "%s lacks headings" % b.path


def test_the_template_carries_every_card_heading():
    """A pile written from plans/piles/_template/README.md is born with the roads and the contents (t-769): the template and
    the card form cannot drift apart without this test saying which heading the template lost."""
    template = (PILES_DIR / "_template" / "README.md").read_text(encoding="utf-8")
    lines = [l.rstrip() for l in template.split("\n")]
    assert [h for h in CARD_HEADINGS if h not in lines] == [], "plans/piles/_template/README.md lacks headings"


@pytest.mark.parametrize("slug", SLUGS)
def test_zachem_names_no_id(slug):
    why = (section_text((PILES_DIR / slug / "README.md").read_text(encoding="utf-8"), "## Зачем") or "").strip()
    assert why, "%s: «Зачем» is empty" % slug
    assert ID_RE.findall(why) == [], "%s: what people read in «Зачем» names no B-id" % slug


@pytest.mark.parametrize("slug", SLUGS)
def test_every_id_and_findings_file_once_in_contents(slug):
    folder, pile = pile_parts(slug)
    contents = section_text((folder / "README.md").read_text(encoding="utf-8"), "## Содержание")
    assert contents is not None, "%s: no «## Содержание» section (a card is written from plans/piles/_template/README.md)" % slug
    names = [pathlib.Path(f.path).name for f in pile.findings]
    assert piles.contents_problems(contents, row_ids_of(pile), names) == []


def node_id_problems(ids, closed):
    """Problems of one batch file's node ids: a duplicate, and -- in a batch that is not closed -- an id that is not
    `<initials><N>-<n>`. A closed batch is history written before the form (forge/2 and forge/4 name nodes `B-419`, `B-426`)."""
    problems = ["duplicate node id %s" % i for i in sorted({i for i in ids if ids.count(i) > 1})]
    if not closed:
        problems += ["node id %s is not <initials><N>-<n>" % i for i in ids if not NODE_ID_RE.match(i)]
    return problems


@pytest.mark.parametrize("slug", SLUGS)
def test_node_ids_are_initials_form_and_unique(slug):
    """What is left of the old node test once the gate took the row-id coverage (piles.py check (д)): the node id is never a
    B-id and never repeats. Nothing here is skipped: the node table has the Узел and Что columns the gate reads."""
    folder, pile = pile_parts(slug)
    for b in pile.batches:
        lines = (folder / pathlib.Path(b.path).name).read_text(encoding="utf-8").split("\n")
        header, rows = piles.table_after(lines, "Узлы")
        cols = piles.column_map(header, {"id": "узел", "what": "что"})
        assert set(cols) == {"id", "what"}, "%s: the node table needs Узел and Что columns" % b.path
        ids = [c[cols["id"]] for c, _ in rows]
        assert ids, "%s: no nodes" % b.path
        assert node_id_problems(ids, b.status == "закрыта") == [], b.path


def test_negative_control_a_b_id_or_a_repeat_as_node_id_is_reported():
    assert node_id_problems(["DC1-1", "DC1-2", "C3-1", "F0-1"], closed=False) == []
    assert node_id_problems(["DC1-1", "B-419"], closed=False) == ["node id B-419 is not <initials><N>-<n>"]
    assert node_id_problems(["DC1-1", "B-419"], closed=True) == []                       # history is not judged for the form ...
    assert node_id_problems(["DC1-1", "DC1-1"], closed=True) == ["duplicate node id DC1-1"]   # ... but a repeat is never fine


def test_negative_control_a_removed_row_is_reported():
    """A copy of a card without one findings row (and without one id row) must be reported -- the check can fail."""
    slug = "driver-controller"
    folder, pile = pile_parts(slug)
    card = (folder / "README.md").read_text(encoding="utf-8")
    contents = section_text(card, "## Содержание")
    names = [pathlib.Path(f.path).name for f in pile.findings]
    ids = row_ids_of(pile)
    assert piles.contents_problems(contents, ids, names) == []
    lost_file = next(l for l in contents.split("\n") if names[3] in l)
    lost_id = next(l for l in contents.split("\n") if l.startswith("| %s |" % ids[0]))
    broken = "\n".join(l for l in contents.split("\n") if l not in (lost_file, lost_id))
    problems = piles.contents_problems(broken, ids, names)
    assert any(names[3] in p for p in problems) and any(ids[0] in p for p in problems), problems
