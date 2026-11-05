"""The ONE-SHOT `split`: lays the open rows of plans/BACKLOG.md out over the piles (spec t-580 section 4.1, F0-2b).

    python tools/piles_split.py [--repo DIR] [--dry-run] [--assign B-nnn=<slug>]...

What it does, in this order (the parsers are tools/piles.py's; nothing is parsed twice):
  1. writes the cards of the plan's 11 piles that have none yet (plans/team/team-work-plan.md 4.1, in the form of
     plans/piles/_template/README.md; the pile's first batch is row 1, status "ожидает"). An existing card is left as is;
  2. places every OPEN row of the backlog. The first rule that fires wins:
       a. named whole in two batch rows            -> UNRESOLVED (a row has one home);
       b. a finding with its id exists anywhere    -> already placed (this is why a second run changes nothing);
       c. named whole in one batch row of a card   -> "in a batch": no finding is written;
       d. named only partially (B-309 (г)-(и))     -> a finding in the pile of that card; the qualifier is noted;
       e. --assign B-nnn=<slug>                    -> that pile;
       f. the FIRST bracket tag [Fnn]              -> the pile whose card claims the feature (none or several:
          UNRESOLVED, with the candidates; a bare "F10" in the text is never a tag);
       g. no tag: by section (SECTION_PILES), else by the first file the text names that a card claims (CONTESTED
          when files of other piles are named too);
  3. writes one finding file per placed row: plans/piles/<slug>/findings/B-nnn-<translit title>.md, cells verbatim.
The backlog and the cards that exist are never touched. A row that is placed by no rule is UNRESOLVED -- nothing is
guessed; everything else is still written (exit 2), a later run continues from the same place.

Exit codes: 0 every open row has its place (or: nothing to do); 1 cannot run (no "## Закрыто", an unreadable file, a bad
option -- nothing was written); 2 UNRESOLVED rows remain (the rest is written). --dry-run writes nothing, same report.
The lists the report ends with (CLOSED BY TEXT, OWNER QUESTION, CONTESTED, ...) are for the Lead: advice, never a gate.
"""
from __future__ import annotations

import argparse
import collections
import dataclasses
import re
import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

import forge_metrics as fm  # noqa: E402
import piles  # noqa: E402
from piles import CannotRun, NO_VAL, PILES_REL  # noqa: E402

FINDINGS_DIR = "findings"
TEMPLATE_REL = PILES_REL + "/_template/README.md"
TITLE_MAX = 100
SLUG_MAX = 48
SLUG_WORDS = 6

ALREADY, BATCH, WRITE, UNRESOLVED = "already", "batch", "write", "unresolved"

TAG_RE = re.compile(r"\[(F\d\d(?:\s*,\s*F\d\d)*)\]")          # the bracket form only (E2)
OWNER_RE = re.compile(r"(?i)жд[её]т (?:слова|решени[яе]) владельца|решение за владельцем|нужно слово владельца"
                      r"|решает владелец|решение владельца(?!\s*\d)|не подтвержд\w* владельц\w*")
EQ_RE = re.compile(r"(?<![\w-])=\s*B-\d{3,}")
ASSIGN_RE = re.compile(r"^(B-\d{3,})=([a-z0-9][a-z0-9-]*)$")

# plan 4.0.2: a row with no tag goes by its section; the other sections (0, 7, 10, 12, ...) go by the files the row names
SECTION_PILES = {"1": "live-runs", "2": "roles-context", "3": "driver-controller", "4": "gates-and-words",
                 "5": "cost-dashboard", "6": "live-runs", "8": "roles-context"}

TRANSLIT = dict(zip("абвгдежзийклмнопрстуфхцчшщъыьэюя", ["a", "b", "v", "g", "d", "e", "zh", "z", "i", "y", "k", "l", "m",
                                                          "n", "o", "p", "r", "s", "t", "u", "f", "kh", "ts", "ch", "sh",
                                                          "shch", "", "y", "", "e", "yu", "ya"]))
TRANSLIT["ё"] = "e"


# ============================================================================================
# the plan's 11 piles (plans/team/team-work-plan.md 4.1) -- data that dies with this one-shot tool
# ============================================================================================

@dataclasses.dataclass(frozen=True)
class PileSpec:
    slug: str
    name: str
    priority: str
    features: str
    stand: str
    what: str
    first: str                  # the B-ids of the proposed first batch, as the plan writes them
    not_copied: str = ""        # words of the plan's cell that are not B-ids (reported, never written)


PILE_TABLE = (
    PileSpec("gates-and-words", "Текст человеку и гейты A/B", "П2", "F07", "нужен",
             "человек на гейтах отвечает словами, его слова доходят до всех читателей и не переспрашиваются; карточки "
             "гейта не врут; отозванные решения не действуют",
             "B-272, B-271, B-292 (остатки), B-338, B-339, B-376, B-392, B-365, B-387, B-388, B-358, B-362, B-423, "
             "B-424, B-425"),
    PileSpec("driver-controller", "Драйвер и контроллер", "П2", "F05, F06", "частично",
             "headless-прогон не теряет стадии при возобновлении, живость роли доказуема, свежесть тикета одна на оба "
             "пути, следующий шаг контроллера всегда верный",
             "B-421, B-422, B-437, B-438, B-311, B-312, B-316, B-317, B-330, B-331, B-335, B-366, B-382, B-383, B-384, "
             "B-385"),
    PileSpec("execution-probes", "Исполнение тестов и пробы", "П2", "F11, F03 (пробы), F09", "нужен (M1–M3 на проекте)",
             "проба «проверка живая» работает на любом языке и раннере, один предикат «это pytest», оракул — из "
             "требований, не из кода",
             "B-369, B-371, B-375, B-377, B-380, B-432, B-440, B-441, B-442, B-445, B-458, B-278, B-279"),
    PileSpec("stand-and-sources", "Стенд, источники, HTTP, Jira", "П2", "F01, F02, F03 (стенд), F18", "нужен",
             "HTTP-ошибки читаются верно, стенд-идентичность одна, тикет и его источники берутся по API и не "
             "расходятся со снимком, запись в Jira — в её разметке",
             "B-450, B-276 (остатки), B-290, B-291, B-350, B-389, B-390, B-393, B-324, B-246, B-247, B-254, B-120"),
    PileSpec("report-delivery", "Отчёт, доставка, трассировка", "П1", "F08, F12, F13", "не нужен (CI + эталоны)",
             "отчёт не показывает pass на красном, третий вердикт доставки, причины недоставки с владельцем, одна "
             "таблица триажа",
             "B-303, B-308 (а), B-304, B-306, B-310, B-353, B-363, B-347, B-357, B-374, B-266, B-270, B-286, B-430"),
    PileSpec("onboarding-hooks", "Онбординг, установка, хуки и гард", "П2", "F04, F16", "частично (L1/L2)",
             "переустановка без потерь, заметки онбординга переживают компакцию, гард узнаёт shell-обходы и жёсткие "
             "ссылки, один токенайзер оболочки",
             "B-349, B-351, B-433, B-434, B-436, B-427, B-428, B-429, B-431, B-444, B-447, B-452, B-453, B-459, B-319, "
             "B-370"),
    PileSpec("cost-dashboard", "Деньги, телеметрия, дашборд", "П3", "F14", "не нужен (эталонные прогоны)",
             "цена задачи одна и истинная (P18), дашборд по задачам и стадиям, прогноз по размеру, никаких «$0 как "
             "факт»",
             "B-439, B-397, B-398, B-219, B-141, B-138, B-121, B-083, B-084, B-085, B-079, B-187, B-198"),
    PileSpec("roles-context", "Роли, тексты и контекст", "П3", "F17, F20", "нужен (трение меряется прогоном)",
             "роли читают меньше и точнее (диета инъекции, карточки AHEAD), уставы ролей несут P16/P17, "
             "джев-суждения достроены",
             "B-346, B-188, B-133, B-161, B-169, B-076, B-072, B-023, B-024, B-126, B-131"),
    PileSpec("package-ci", "Пакет: тесты, Linux, CI", "П1", "F15", "не нужен (CI)",
             "полный прогон зелёный на Linux и на второй Windows-машине, тесты не падают под нагрузкой, время тестов в "
             "лимите",
             "B-307, B-301, B-302, B-326, B-344, B-320, B-460, B-297, B-386, B-318, B-333, B-368, B-381, B-446, B-448, "
             "B-403"),
    PileSpec("forge", "Forge: система разработки и командная работа", "П1", "F19", "не нужен",
             "разработчики работают параллельно без конфликтов; критик проверяет повторы и качество; один читатель "
             "транскриптов; меньше токенов",
             "B-419, B-309 (г)–(и), B-426, B-467, B-454, B-449, B-455, B-456, B-457, B-204, B-135, B-245",
             "фаза 0 (§3)"),
    PileSpec("live-runs", "Живые прогоны и новые проекты", "П1", "—", "нужен (кучка владельца и dev2)",
             "каждое изменение поведения роли доказано живым прогоном; фабрика идёт на незнакомом проекте и не-Python",
             "B-373 M1–M3, B-411 L1/L2, B-404, B-413, B-361, B-414, B-410, B-408 (a)(b) (замер Антона), B-417, B-418, "
             "B-015, B-092, B-104, B-097",
             "W7, «затем»"),
)


# ============================================================================================
# titles, slugs, finding text
# ============================================================================================

def finding_title(what: str, ident: str) -> str:
    """The title of a finding (spec 3.4): a leading **bold** part, else the text up to the first '. '; no '**', no
    trailing '.' or ':', one space between words. Longer than TITLE_MAX: cut at the last space and end with '…', so
    the title is never longer than TITLE_MAX (exactly TITLE_MAX stays whole). An empty cell: the id."""
    if what.startswith("**"):
        end = what.find("**", 2)
        raw = what[2:end] if end > 1 else what[2:]
    else:
        end = what.find(". ")
        raw = what[:end] if end >= 0 else what
    title = re.sub(r"\s+", " ", raw.replace("**", "")).strip().rstrip(".:").strip()
    if len(title) > TITLE_MAX:
        cut = title.rfind(" ", 0, TITLE_MAX)
        title = title[:cut if cut > 0 else TITLE_MAX - 1].rstrip() + "…"
    return title or ident


def translit_slug(title: str) -> str:
    """The file-name slug: the first SLUG_WORDS words, transliterated, [a-z0-9] and single hyphens, at most SLUG_MAX
    characters (cut at the last hyphen; a single long word is cut hard). Empty when nothing survives."""
    words = title.lower().split()[:SLUG_WORDS]
    latin = "".join(TRANSLIT.get(ch, ch) for ch in " ".join(words))
    slug = re.sub(r"-+", "-", re.sub(r"[^a-z0-9]", "-", latin)).strip("-")
    if len(slug) > SLUG_MAX:
        cut = slug.rfind("-", 0, SLUG_MAX + 1)
        slug = slug[:cut if cut > 0 else SLUG_MAX].strip("-")
    return slug


def finding_name(ident: str, title: str) -> str:
    slug = translit_slug(title)
    return "%s-%s.md" % (ident, slug) if slug else ident + ".md"


def owner_phrase(text: str):
    m = OWNER_RE.search(text)
    return m.group(0) if m else None


def _fence(text: str) -> str:
    longest = max((len(r) for r in re.findall(r"`+", text)), default=0)
    return "`" * max(3, longest + 1)


def finding_text(row: piles.Row, out) -> str:
    """The finding (spec 3.4): the cells mapped per 3.1, verbatim, then the row line itself, verbatim."""
    f = row.fields
    source = f["source"] if f["source"] not in NO_VAL else "plans/BACKLOG.md, раздел %s" % row.section
    lines = ["# " + out.title, "",
             "id: %s | кучка: `%s` | от: %s | приоритет: — | кандидат наверх: нет" % (row.id, out.slug, source), "",
             "Что не так / что сделать: " + (f["what"] or "—"), "",
             "Свидетель: " + (f["witness"] or "—"), "",
             "Принципы и правила: " + (f["principles"] or "—"), ""]
    for slug, n, qual in out.partial:
        lines += ["Член пачки `%s/%d` частично: %s -- остаток строки лежит в этой находке." % (slug, n, qual), ""]
    phrase = owner_phrase(row.text)
    lines += ["Решение владельца нужно: " + ("да — " + phrase if phrase else "нет (фраза не найдена)"), "",
              "<!-- piles split: plans/BACKLOG.md, раздел %s «%s»; ячейки строки перенесены дословно -->"
              % (row.section, row.section_title), "",
              "Строка BACKLOG.md целиком:", "", _fence(row.text), row.text, _fence(row.text), ""]
    return "\n".join(lines)


# ============================================================================================
# the cards of the plan's piles
# ============================================================================================

def _members_cell(members) -> str:
    return ", ".join(m.id + (" " + m.qualifier if m.qualifier else "") for m in members) or "—"


def render_card(template: str, spec: PileSpec, members) -> str:
    """The card in the form of plans/piles/_template/README.md: heading, properties, the 'Зачем' line and batch row 1
    are the pile's; everything else is the template's own text."""
    out, section, why_done = [], "", False
    for line in template.split("\n"):
        if line.startswith("## "):
            section = line[3:].strip()
        if line.startswith("# "):
            out.append("# %s (`%s`)" % (spec.name, spec.slug))
        elif not section and "приоритет:" in line:
            out.append("приоритет: %s | фичи: %s | стенд: %s | зона: —" % (spec.priority, spec.features, spec.stand))
        elif section == "Зачем" and line.strip() and not line.startswith("## "):
            if not why_done:
                out.append("Что изменится: " + spec.what)
                why_done = True
        elif section == "Пачки" and line.startswith("| 1 |"):
            out.append("| 1 | %s | %s | — | ожидает | — | — | — |" % (spec.what, _members_cell(members)))
        else:
            out.append(line)
    return "\n".join(out)


def check_card(text: str, rel: str, spec: PileSpec, members) -> None:
    """The template changed shape, or a cell broke the table: refuse before anything is written."""
    card = piles.parse_card(text, rel)
    ok = (not card.errors and card.title_slug == spec.slug and card.features == re.findall(r"F\d\d", spec.features)
          and len(card.rows) == 1 and [m.id for m in card.rows[0].members] == [m.id for m in members])
    if not ok:
        raise CannotRun("the card made for %s does not parse back (%s) -- %s no longer has the shape split expects "
                        "(heading, a properties line, '## Зачем', '## Пачки' with a row starting '| 1 |'); fix the "
                        "template and run again" % (spec.slug, "; ".join(card.errors) or "its fields differ", TEMPLATE_REL))


@dataclasses.dataclass
class CardPlan:
    spec: PileSpec
    rel: str
    text: str
    card: piles.Card
    dropped: list               # [(id, why)] -- named by the plan's first batch, not copied


def plan_cards(root: Path, tree: piles.Tree) -> list:
    """-> [CardPlan] for every pile of PILE_TABLE that has no card yet. First-batch ids that are closed in the backlog
    (the plan was written before they closed, m12) or not rows of it are dropped from the card row, never copied."""
    todo = [s for s in PILE_TABLE if not (s.slug in tree.piles and tree.piles[s.slug].card)]
    if not todo:
        return []
    template = piles.read_text(root / TEMPLATE_REL)
    plans = []
    for spec in todo:
        kept, dropped = [], []
        for m in piles.parse_members(spec.first)[0]:
            if m.id in tree.backlog.open_ids:
                kept.append(m)
            else:
                dropped.append((m.id, "closed in plans/BACKLOG.md" if m.id in tree.backlog.closed_ids
                                else "not a row of plans/BACKLOG.md"))
        rel = "%s/%s/README.md" % (PILES_REL, spec.slug)
        text = render_card(template, spec, kept)
        check_card(text, rel, spec, kept)
        plans.append(CardPlan(spec, rel, text, piles.parse_card(text, rel), dropped))
    return plans


# ============================================================================================
# the context: what the placement rules look at
# ============================================================================================

@dataclasses.dataclass
class Ctx:
    tree: piles.Tree
    features: list
    index: fm.FileIndex
    claims: dict                # feature id -> [slug of the cards that claim it]
    homes: dict                 # B-id -> [(slug, batch number, Member)] over all card rows
    found: dict                 # B-id -> slug of the pile folder that holds a finding for it
    assigns: dict               # B-id -> slug (--assign)
    feature_ids: frozenset = frozenset()


def build_index(root: Path) -> fm.FileIndex:
    """The files a row can name: the package plus git's tracked files (as forge_metrics.compute does); without git, the
    walk of tools/ docs/ plans/. Copies of worktrees (.claude/worktrees) never decide the fate of a row (E6)."""
    tracked = fm.tracked_files(root)
    paths = set(fm.package_files(root)) | set(tracked or [])
    if tracked is None:
        for d in ("tools", "docs", "plans"):
            paths |= set(fm.walk_files(root, d))
    return fm.FileIndex(p for p in paths if not p.startswith(".claude/worktrees/"))


def load_features(root: Path) -> list:
    try:
        return fm.load_registry(root / fm.REGISTRY_REL)
    except fm.RegistryError as exc:
        raise CannotRun("cannot read the feature registry: %s" % exc)


def with_cards(tree: piles.Tree, plans: list) -> piles.Tree:
    """The tree as it will be once the cards are written (nothing is read back from disk)."""
    merged = dict(tree.piles)
    for cp in plans:
        slug = cp.spec.slug
        old = merged.get(slug)
        merged[slug] = (dataclasses.replace(old, card=cp.card) if old
                        else piles.Pile(slug, cp.card, cp.rel, [], [], []))
    return piles.Tree(tree.root, tree.backlog, merged, [])


def build_ctx(tree: piles.Tree, features: list, index: fm.FileIndex) -> Ctx:
    claims = collections.defaultdict(list)
    for slug in sorted(tree.piles):
        card = tree.piles[slug].card
        for feat in (card.features if card else []):
            if slug not in claims[feat]:
                claims[feat].append(slug)
    homes = collections.defaultdict(list)
    for view, member in tree.member_rows():
        homes[member.id].append((view.slug, view.n, member))
    found = {}
    for slug, pile in sorted(tree.piles.items()):
        for f in pile.findings:
            for ident in (f.id, f.name_id):
                if ident:
                    found.setdefault(ident, slug)
    return Ctx(tree, features, index, dict(claims), dict(homes), found, {}, frozenset(f["id"] for f in features))


# ============================================================================================
# placing one row
# ============================================================================================

@dataclasses.dataclass
class Outcome:
    row: piles.Row
    kind: str = UNRESOLVED
    slug: str = ""
    n: int = 0                  # the batch number (kind == BATCH)
    via: str = ""               # partial | assign | tag | section | paths
    reason: str = ""            # UNRESOLVED: what could not be decided (the grouping key of the report)
    detail: str = ""
    candidates: tuple = ()
    tag: str = ""
    contested: list = dataclasses.field(default_factory=list)      # [(slug, path)] other piles' files the text names
    partial: list = dataclasses.field(default_factory=list)        # [(slug, batch number, qualifier)]
    title: str = ""
    rel: str = ""
    text: str = ""


def row_tags(text: str) -> list:
    """The bracket tags of a row in text order, each once. The bare 'F10' of 'развилка F10' is never one (E2)."""
    seen = []
    for m in TAG_RE.finditer(text):
        for t in re.findall(r"F\d\d", m.group(1)):
            if t not in seen:
                seen.append(t)
    return seen


def file_tokens(text: str) -> list:
    """Backtick tokens and bare file names in the order they stand in the text (m1: forge_metrics._file_tokens has no
    positions, so 'the first file by text' cannot be built on it)."""
    hits = [(m.start(1), m.group(1)) for m in fm.BACKTICK_RE.finditer(text)]
    hits += [(m.start(1), m.group(1)) for m in fm.BARE_PATH_RE.finditer(text)]
    return [tok for _, tok in sorted(hits)]


def _by_feature(ctx: Ctx, feat: str):
    """-> (slug, None) or (None, (reason, candidates)): a feature has to be claimed by exactly one card."""
    owners = ctx.claims.get(feat, [])
    if len(owners) == 1:
        return owners[0], None
    if not owners:
        return None, ("feature %s is claimed by no card" % feat, ())
    return None, ("feature %s is claimed by %d cards: %s" % (feat, len(owners), ", ".join(owners)), tuple(owners))


def _by_paths(ctx: Ctx, row: piles.Row):
    """-> (slug, contested, None, "") or (None, [], (reason, candidates), detail). The first file of the text that a
    card claims decides (Р7); files of other piles named after it make the row CONTESTED. A file whose feature several
    cards claim is not decided by code (E4)."""
    claimed, unclaimed = [], []
    for tok in file_tokens(row.text):
        for path in sorted(ctx.index.resolve(tok)):
            feat = fm.classify_path(ctx.features, path)
            (claimed if feat and ctx.claims.get(feat) else unclaimed).append((path, feat))
    if not claimed:
        reason = "section %s: no tag, no path" % row.section
        if unclaimed:
            feats = sorted({f or "no feature" for _, f in unclaimed})
            reason = "section %s: no tag; the files it names belong to no card (%s)" % (row.section, ", ".join(feats))
        return None, [], (reason, ()), ""
    path, feat = claimed[0]
    slug, bad = _by_feature(ctx, feat)
    if bad:
        return None, [], bad, "by the first file it names: " + path
    others = {}
    for p, f in claimed[1:]:
        for s in ctx.claims[f]:
            if s != slug:
                others.setdefault(s, p)
    return slug, sorted(others.items()), None, ""


def _place_by_rules(ctx: Ctx, row: piles.Row, out: Outcome) -> Outcome:
    """Rules e-g: --assign, the tag, the section, the files."""
    if row.id in ctx.assigns:
        out.kind, out.slug, out.via = WRITE, ctx.assigns[row.id], "assign"
        return out
    slug, bad = None, None
    if out.tag:
        slug, bad = _by_feature(ctx, out.tag)
        out.via = "tag"
    elif row.section in SECTION_PILES:
        slug, out.via = SECTION_PILES[row.section], "section"
    else:
        slug, out.contested, bad, out.detail = _by_paths(ctx, row)
        out.via = "paths"
    if bad:
        out.reason, out.candidates = bad
    else:
        out.kind, out.slug = WRITE, slug
    return out


def place_row(ctx: Ctx, row: piles.Row) -> Outcome:
    tags = row_tags(row.text)
    out = Outcome(row, tag=tags[0] if tags and tags[0] in ctx.feature_ids else "")
    homes = ctx.homes.get(row.id, [])
    whole = sorted({(s, n) for s, n, m in homes if not m.partial})
    if len(whole) > 1:
        out.via = "two-batches"
        out.reason, out.detail = "named whole in %d batch rows" % len(whole), ", ".join("%s/%d" % w for w in whole)
        return out
    if row.id in ctx.found:
        out.kind, out.slug = ALREADY, ctx.found[row.id]
        return out
    if whole:
        out.kind, out.slug, out.n = BATCH, whole[0][0], whole[0][1]
        return out
    out.partial = sorted({(s, n, m.qualifier) for s, n, m in homes if m.partial})
    if len({s for s, _, _ in out.partial}) == 1:
        out.kind, out.slug, out.via = WRITE, out.partial[0][0], "partial"
        return out
    return _place_by_rules(ctx, row, out)


def materialize(out: Outcome) -> Outcome:
    """The finding file for a WRITE outcome. Its text must parse back to this id and this pile -- otherwise nothing is
    written for the row and it is UNRESOLVED (a header cell that breaks the header line is the case)."""
    row = out.row
    out.title = finding_title(row.fields["what"], row.id)
    out.rel = "%s/%s/%s/%s" % (PILES_REL, out.slug, FINDINGS_DIR, finding_name(row.id, out.title))
    out.text = finding_text(row, out)
    fi = piles.parse_finding(out.text, out.rel)
    if fi.errors or fi.id != row.id or fi.pile != out.slug:
        out.kind, out.reason = UNRESOLVED, "the finding made for it would not parse back"
        out.detail = "; ".join(fi.errors) or 'id "%s", pile "%s"' % (fi.id, fi.pile)
    return out


def place_all(ctx: Ctx) -> list:
    """One Outcome per open row (a row listed twice above '## Закрыто' is placed once)."""
    outs, seen = [], set()
    for row in ctx.tree.backlog.rows:
        if row.closed or row.id in seen:
            continue
        seen.add(row.id)
        out = place_row(ctx, row)
        outs.append(materialize(out) if out.kind == WRITE else out)
    return outs


# ============================================================================================
# --assign
# ============================================================================================

def parse_assigns(ctx: Ctx, raw: list) -> dict:
    """Every --assign is checked before anything is written; the first refusal wins (exit 1, a usage error)."""
    open_ids = ctx.tree.backlog.open_ids
    slugs = sorted(s for s, p in ctx.tree.piles.items() if p.card)
    given = collections.defaultdict(list)
    for item in raw:
        m = ASSIGN_RE.match(item)
        if not m:
            raise CannotRun('--assign "%s": expected B-nnn=<slug>' % item)
        given[m.group(1)].append(m.group(2))
    for ident, targets in given.items():
        if len(targets) > 1:
            raise CannotRun("--assign %s is given twice (%s); give it once" % (ident, ", ".join(targets)))
    out = {}
    for ident, (slug,) in given.items():
        head = "--assign %s=%s:" % (ident, slug)
        if ident not in open_ids:
            raise CannotRun('%s %s is not an open row of plans/BACKLOG.md; expected an id listed above "## Закрыто"'
                            % (head, ident))
        if slug not in slugs:
            raise CannotRun('--assign %s=%s: no pile "%s" (no %s/%s/README.md); piles with a card: %s'
                            % (ident, slug, slug, PILES_REL, slug, ", ".join(slugs)))
        where = _locked(ctx, ident)
        if where:
            raise CannotRun("%s %s is already placed (%s); move its file by hand if it belongs elsewhere"
                            % (head, ident, where))
        out[ident] = slug
    return out


def _locked(ctx: Ctx, ident: str) -> str:
    """Where the first rules already put an id (a finding, a whole batch row, a partial member of ONE pile), else ''.
    A partial member of two piles is not locked: it falls through to --assign."""
    homes = ctx.homes.get(ident, [])
    if ident in ctx.found:
        return "finding in %s" % ctx.found[ident]
    named = ["%s %s/%d%s" % ("partial member of" if m.partial else "batch", s, n, " " + m.qualifier if m.qualifier else "")
             for s, n, m in homes]
    if any(not m.partial for _, _, m in homes) or len({s for s, _, _ in homes}) == 1:
        return "; ".join(named)
    return ""


# ============================================================================================
# the report
# ============================================================================================

def _snippet(text: str, m) -> str:
    s, e = max(0, m.start() - 25), min(len(text), m.end() + 35)
    return ("…" if s else "") + re.sub(r"\s+", " ", text[s:e]) + ("…" if e < len(text) else "")


def closed_by_text(row: piles.Row):
    hits = [m for m in (fm.CLOSED_RE.search(row.text), EQ_RE.search(row.text)) if m]
    return _snippet(row.text, min(hits, key=lambda m: m.start())) if hits else None


def _block(out: list, title: str, items: list) -> None:
    if items:
        out.append(title)
        out.extend("  " + i for i in items)


def _label(o: Outcome) -> str:
    return "%s [%s]" % (o.row.id, o.tag or "section %s" % o.row.section)


def unresolved_lines(unresolved: list) -> list:
    out = []
    by_reason = collections.Counter(o.reason for o in unresolved)
    _block(out, "UNRESOLVED (no pile by rule; nothing was guessed) -- by reason:",
           ["%s: %d" % (r, c) for r, c in sorted(by_reason.items(), key=lambda kv: (-kv[1], kv[0]))])
    out.append("UNRESOLVED rows:")
    for o in unresolved:
        extra = ("; " + o.detail) if o.detail else ""
        out.append("  %s: %s%s" % (_label(o), o.reason, extra))
    out.append("--assign lines to copy (pick one candidate; the slug is yours to choose):")
    for o in unresolved:
        if o.via == "two-batches":
            out.append("  (%s: --assign cannot help; remove it from all but one batch row of the cards by hand)" % o.row.id)
        else:
            out.append("  --assign %s=<%s>" % (o.row.id, "|".join(o.candidates) if o.candidates else "slug"))
    return out


def per_pile_lines(ctx: Ctx, outs: list) -> str:
    count = collections.defaultdict(collections.Counter)
    for o in outs:
        if o.kind == BATCH:
            count[o.slug]["batch"] += 1
        elif o.kind in (ALREADY, WRITE):
            count[o.slug]["findings"] += 1
    order = [s.slug for s in PILE_TABLE] + sorted(set(ctx.tree.piles) - {s.slug for s in PILE_TABLE})
    return "; ".join("%s %d (batch %d, findings %d)" % (s, sum(count[s].values()), count[s]["batch"], count[s]["findings"])
                     for s in order if s in ctx.tree.piles)


def nonid_items(ctx: Ctx, plans: list) -> list:
    items = ["%s/%d: %s" % (slug, r.n, piece) for slug, pile in sorted(ctx.tree.piles.items())
             if pile.card for r in pile.card.rows for piece in r.nonid]
    items += ["%s/1: %s (named by the plan's table, not B-ids; not copied)" % (cp.spec.slug, cp.spec.not_copied)
              for cp in plans if cp.spec.not_copied]
    return items


def _dropped(pairs: list) -> str:
    by_why = collections.defaultdict(list)
    for ident, why in pairs:
        by_why[why].append(ident)
    return "; ".join("%s: %s" % (why, ", ".join(ids)) for why, ids in by_why.items())


def lists_lines(ctx: Ctx, outs: list, plans: list) -> list:
    rows = [o.row for o in outs]
    out = []
    _block(out, "DROPPED FROM CARD ROWS (the plan's first batches name ids that are not open rows):",
           ["%s/1: %s" % (cp.spec.slug, _dropped(cp.dropped)) for cp in plans if cp.dropped])
    _block(out, "PARTIAL (a member named with a qualifier; the whole row is a finding of that pile):",
           ["%s %s -> %s" % (o.row.id, "; ".join("%s/%d %s" % p for p in o.partial), o.slug or "UNRESOLVED")
            for o in outs if o.partial])
    _block(out, "CONTESTED (placed by the first-named file; other piles' files also named):",
           ["%s -> %s; also %s" % (o.row.id, o.slug, ", ".join("%s (%s)" % (s, p.rsplit("/", 1)[-1]) for s, p in o.contested))
            for o in outs if o.contested])
    _block(out, "CLOSED BY TEXT (placed as usual; for the integrator to close by the owner's word):",
           ['%s "%s"' % (r.id, s) for r in rows for s in [closed_by_text(r)] if s])
    _block(out, 'OWNER QUESTION (the finding says "Решение владельца нужно: да"):',
           ['%s "%s"' % (r.id, p) for r in rows for p in [owner_phrase(r.text)] if p])
    tags = [(r, row_tags(r.text)) for r in rows]
    known = {f["id"] for f in ctx.features}
    _block(out, "MULTI-TAG (the first tag decides):",
           ["%s [%s] -> %s" % (r.id, ", ".join(t), t[0]) for r, t in tags if len(t) > 1 and t[0] in known])
    _block(out, "UNKNOWN TAG (not in plans/features.json; the row is treated as untagged):",
           ["%s [%s]" % (r.id, ", ".join(t)) for r, t in tags if t and t[0] not in known])
    _block(out, "IRREGULAR ROWS (cells differ from the table header; missing cells read '—', extra ones went to the text):",
           ["%s: %d cells, header has %d" % (r.id, len(r.cells), len(r.columns) or 5) for r in rows if r.irregular])
    _block(out, "NON-ID ITEMS IN CARD ROWS:", nonid_items(ctx, plans))
    return out


def summary_lines(ctx: Ctx, outs: list, plans: list, dry: bool) -> list:
    n = collections.Counter(o.kind for o in outs)
    verb = "would write" if dry else "written"
    parts = sum(1 for o in outs if o.kind == WRITE and o.via == "partial")
    lines = ["piles split: %d open rows in %s" % (len(outs), piles.BACKLOG_REL)]
    if plans:
        new = {c.spec.slug for c in plans}
        old = [s.slug for s in PILE_TABLE if s.slug in ctx.tree.piles and s.slug not in new]
        lines.append("  cards: %s %d (%s); already there: %s" % (verb, len(plans), ", ".join(sorted(new)),
                                                                  ", ".join(old) or "none"))
    lines.append("  findings: %s %d; already placed: %d; whole in a batch row: %d; partial: %d (inside the written)"
                 % (verb, n[WRITE], n[ALREADY], n[BATCH], parts))
    lines.append("  per pile: " + per_pile_lines(ctx, outs))
    return lines


# ============================================================================================
# run
# ============================================================================================

def write_files(root: Path, plans: list, outs: list) -> None:
    try:
        for cp in plans:
            piles.write_atomic(root / cp.rel, cp.text)
        for o in outs:
            if o.kind == WRITE:
                piles.write_atomic(root / o.rel, o.text)
    except OSError as exc:
        raise CannotRun("cannot write %s -- the files written so far stay; fix the cause and run again (a second run "
                        "continues from the same place)" % exc)


def run_split(root: Path, dry: bool, assigns: list) -> int:
    tree = piles.load_tree(root)
    features = load_features(root)
    plans = plan_cards(root, tree)
    tree = with_cards(tree, plans)
    ctx = build_ctx(tree, features, build_index(root))
    ctx.assigns = parse_assigns(ctx, assigns)
    outs = place_all(ctx)
    unresolved = [o for o in outs if o.kind == UNRESOLVED]
    n = collections.Counter(o.kind for o in outs)
    if not plans and not n[WRITE] and not unresolved:
        print("piles split: nothing to do -- every open row already has its place (%d: %d finding files, %d whole in "
              "batch rows)" % (len(outs), n[ALREADY], n[BATCH]))
        return 0
    lines = summary_lines(ctx, outs, plans, dry) + lists_lines(ctx, outs, plans)
    if unresolved:
        lines += unresolved_lines(unresolved)
        lines.append("piles split: %d row(s) UNRESOLVED -- nothing was guessed for them; place each with --assign "
                     "B-nnn=<slug> (repeatable) or by naming it in a card's batch row, then run split again" % len(unresolved))
    if not dry:
        write_files(root, plans, outs)
    lines.append("(dry run: nothing written)" if dry else "piles split: wrote %d card(s) and %d finding file(s)"
                 % (len(plans), n[WRITE]))
    print("\n".join(lines))
    return 2 if unresolved else 0


def build_parser() -> argparse.ArgumentParser:
    ap = piles._Parser(prog="piles_split.py", description=__doc__.split("\n")[0])
    ap.add_argument("--repo", help="the repository root (default: the parent of tools/)")
    ap.add_argument("--dry-run", action="store_true", help="print the report; write nothing")
    ap.add_argument("--assign", action="append", default=[], metavar="B-nnn=SLUG",
                    help="place an UNRESOLVED row in a pile (repeatable)")
    return ap


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    try:
        args = build_parser().parse_args(argv)
        return run_split(Path(args.repo) if args.repo else piles.REPO, args.dry_run, args.assign)
    except CannotRun as exc:
        print("piles split: %s" % exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
