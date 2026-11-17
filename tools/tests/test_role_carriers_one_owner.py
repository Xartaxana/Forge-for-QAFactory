"""One owner per aspect of a role (onboarding-forge/1 F6-33, t-1206/t-1702; docs/SIBLING_MAP.md axis 31).

K-OWN: each owner's anchor sentence (OWNER_KEYS, verbatim from spec t-1206 section 4) occurs - whitespace squashed, case
folded - in exactly ONE scanned file, and that file is its owner. A second carrier is a full restatement (a finding like a
contradiction); the owner losing the key means the owner was edited without its key.
K-PTR: every pointer of POINTERS is present in its carrier and the section it names still exists in its target (a renamed
target section turns this red - the safe direction).
Scanned: tracked files (`git ls-files`; a tree with no `.git` - every file) with a text suffix, minus EXCLUDED: the
generated copy (AGENTS.md), the decision record, history and quotations (specs, handoffs, snapshots, task reports, piles,
experiments, logs), the package, test fixtures, this file. Blind spot (a false pass, named): a restatement in another
language does not match an English key - axis 31's rule and the critic's question 6 cover it.
K-NOBRIEF / K-REG (no-briefs spec section 8, owner's word 17.11.2026 "we do not create extra documents"): the register of MAIN
documents is the axis-31 table of docs/SIBLING_MAP.md read by code; no MAIN document names a DELETED file by path or by stem
(false red is the allowed side); a deleted file stays untracked; no brief file sits at the top of docs/tasks/.
Run from the repo root: python -m pytest tools/tests/test_role_carriers_one_owner.py -q
"""
import os
import pathlib
import re
import subprocess
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import md_table  # noqa: E402  (the one table reader: SIBLING_MAP axis 31 is read through it)

REAL = pathlib.Path(__file__).resolve().parents[2]
ROOT = pathlib.Path(os.environ.get("ROLE_CARRIERS_ROOT") or REAL)
SELF = "tools/tests/test_role_carriers_one_owner.py"
TEXT_SUFFIXES = (".md", ".py", ".json", ".yaml", ".yml", ".txt")
EXCLUDED = ("AGENTS.md", "DECISIONS.md", "docs/DECISIONS_ARCHIVE.md", "ai-packages/", "experiments/", "logs/", "kb/",
            "docs/tasks/specs/", "docs/tasks/handoffs/", "docs/tasks/compact-snapshots/", "docs/task_reports/",
            "plans/piles/", "tools/fixtures/", SELF)

CRITIC = ".claude/agents/critic.md"
TESTING = "docs/TESTING.md"
TESTING_RUN = "### Что запускать по своей правке"
CRIT_21 = "21. The two layers of a diff gate"
CRIT_Q6 = "Q6. **DUPLICATION AND CONSISTENCY**"
COST = "Cost gates (D-0035, D-0038, D-0040, D-0054;"
HYGIENE_6 = "6. An environment-negative claim requires verification: empty output"
TEAMWORK = "docs/TEAMWORK.md"
RUNBOOK_7 = "## 7. CI на GitHub и BATCH CANON"

# (aspect id, owner, key)
OWNER_KEYS = [
    ("hand-back:builder", ".claude/agents/builder.md", "one status line `1 done | 2 done | 3 not done --"),
    ("hand-back:critic", ".claude/agents/critic.md", "the verdict line and the number of blocking findings"),
    ("hand-back:designer", ".claude/agents/designer.md", "`1 drafted | 2 fork | 3 not drafted -- <one clause>`"),
    ("hand-back:scout", ".claude/agents/scout.md", "the Lead extracts it to a file in"),
    ("scope:builder", TESTING, "не регрессия, не соседи, не большие файлы"),
    # scope:mutation retired by the owner's word 28.10 and 10.11.2026 (docs/TESTING.md): the mutation list is no longer written
    ("scope:tests", TESTING, "Покраснел пин из таблицы выше — удаляется, не чинится"),
    ("review:critic", CRITIC, "functions over roughly 60 lines or with more than three nesting levels in the NEW code"),
    ("review:one-road", CRITIC, "a line for the coordinator to tell someone is itself a finding"),
    ("routing:rule-11", "CLAUDE.md", "a spec silent on an edge that its own requirements create is a dispatcher defect"),
    ("routing:hygiene-6", "CLAUDE.md", "from an INCORRECTLY invoked tool is a miscall, not proof the object is absent"),
    ("routing:rule-9", "CLAUDE.md", "the rule against recurrence goes on the highest level that ties the siblings together"),
    ("routing:rule-9-exit", "CLAUDE.md", "never a way to put off a rule fix while rules are being fixed"),
    ("cost:cap", "CLAUDE.md", "WARN 250K, STOP 400K"),
    ("cost:queue", "PROJECT.md", "цель держать 6 пишущих билдеров"),      # 63bbd5e: the full-queue text moved to PROJECT.md item 12; CLAUDE.md rule 12 points there; re-quoted with R1 (boot-by-topic, FG7-51)
    ("tests:oracle", "docs/TESTING.md", "тест, чьё ожидание переписано из того, что код напечатал, может только пройти"),
    ("tests:line", "docs/TESTING.md", "Пункт без поведения (перенос текста, переименование) строки не получает"),
    ("tests:files", "docs/TESTING.md", "Новый файл верен, когда случай не ложится ни в одну из них"),
]

# (carrier, pointer text it must hold, target, anchor the target must still hold)
POINTERS = [
    ("PROJECT.md", "`docs/TESTING.md` «Что запускать по своей правке»", TESTING, TESTING_RUN),
    ("PROJECT.md", "`.claude/agents/critic.md` rule 21", CRITIC, CRIT_21),
    (".claude/agents/builder.md", "`docs/TESTING.md` «Что запускать по своей правке»", TESTING, TESTING_RUN),
    (".claude/agents/builder.md", "the rule is CLAUDE.md command hygiene point 6", "CLAUDE.md", HYGIENE_6),
    (".claude/agents/critic.md", "the rule is CLAUDE.md command hygiene point 6", "CLAUDE.md", HYGIENE_6),
    (CRITIC, "the rule text is rule 22, Q6-Q7", CRITIC, CRIT_Q6),
    (CRITIC, "(its size: rule 21)", CRITIC, CRIT_21),
    (CRITIC, "the question is rule 22, Q12", CRITIC, "Q12. **ONE ROAD**"),
    (".claude/agents/designer.md", "the text is CLAUDE.md rule 11", "CLAUDE.md", "11. DoD in every dispatch (DoD-in-every-dispatch rule)"),
    (CRITIC, "docs/TESTING.md «Бюджет»", TESTING, "### Бюджет"),
    ("CLAUDE.md", "`docs/TESTING.md` «Что запускать по своей правке»", TESTING, TESTING_RUN),
    (".claude/agents/designer.md", "`docs/TESTING.md` («Что запускать по своей правке», «Строка теста в DoD»", TESTING, "### Строка теста в DoD"),
    (".claude/agents/designer.md", "`.claude/agents/critic.md` rule 24, Q13 (d)", CRITIC, "Q13. **FACTS AND EDGES**"),
    ("CLAUDE.md", "`.claude/agents/critic.md` rule 22, Q6-Q7", CRITIC, "Q7. **CODE QUALITY**"),
    ("docs/CLAUDE_HOST_ADAPTATIONS_FULL.md", "the rule text is `.claude/agents/critic.md` rule 22", CRITIC, CRIT_Q6),
    ("docs/CLAUDE_HOST_ADAPTATIONS_FULL.md", "the rule text is `CLAUDE.md` rule 12, Cost gates", "CLAUDE.md", COST),
    ("SYSTEM_PROMPT.md", "CLAUDE.md rule 9", "CLAUDE.md", "9. Fix the class, not the instance (fix-the-class-not-the-instance"),
    ("docs/RUNBOOK.md", "`docs/TESTING.md` «Что запускать по своей правке»", TESTING, TESTING_RUN),
    ("docs/RUNBOOK.md", "`CLAUDE.md` rule 12, Cost gates", "CLAUDE.md", COST),
    ("docs/TESTING.md", "правилу 21 `.claude/agents/critic.md`", CRITIC, CRIT_21),
    ("docs/TWO_VOCABULARIES.md", "`delegation.config.yaml`", "delegation.config.yaml", "scout:"),
    ("PROJECT.md", "`docs/TEAMWORK.md` § 2", TEAMWORK, "2. **Взятая пачка заморожена** (`piles.py check` (в), гейт commit-msg)"),
    ("PROJECT.md", "`docs/TEAMWORK.md` § 3", TEAMWORK, "3. **Зоны файлов пачек «в работе» не пересекаются** (`check` (б))"),
    ("PROJECT.md", "`docs/TEAMWORK.md` § 4", TEAMWORK, "4. **`plans/BACKLOG.md` заморожен** (`check` (г))"),
    ("PROJECT.md", "`docs/TEAMWORK.md` § 8", TEAMWORK, "8. **Двери**: строка `piles-skip: <пункт> -- <причина>`"),
    ("PROJECT.md", "`docs/TEAMWORK.md` § 9", TEAMWORK, "9. **Пачка закрывается доделкой, не переносом**: `close <slug> <N>` отказывает"),
    ("PROJECT.md", "`docs/OWNER_PRINCIPLES.md`", "docs/OWNER_PRINCIPLES.md", "- **P31.**"),
    ("PROJECT.md", "`docs/RUNBOOK.md` § 4.1", "docs/RUNBOOK.md", "### 4.1. Шаги релиза"),
    ("PROJECT.md", "`docs/RUNBOOK.md` §7", "docs/RUNBOOK.md", RUNBOOK_7),
    ("PROJECT.md", "правило: § Бэклог и находки", "PROJECT.md", "## Бэклог и находки"),
    ("docs/RUNBOOK.md", "`PROJECT.md` § Сессия форджа", "PROJECT.md", "## Сессия форджа"),
    ("docs/TESTING.md", "`docs/RUNBOOK.md` §7", "docs/RUNBOOK.md", RUNBOOK_7),
    ("PROJECT.md", "`.claude/skills/boot-diet/SKILL.md` § Как пишутся правила для агентов", ".claude/skills/boot-diet/SKILL.md", "## Как пишутся правила для агентов"),
    ("CLAUDE.md", "PROJECT.md § Сессия форджа", "PROJECT.md", "## Сессия форджа"),
    (TEAMWORK, "`PROJECT.md` «Командная работа» п. 3", "PROJECT.md", "3. **Зоны файлов пачек «в работе» не пересекаются** — правило: `docs/TEAMWORK.md` § 3"),
]

# The cross-file Contents table of CLAUDE.md (one row per cell, T1-T33 of the boot-by-topic spec section 2) and the own-section
# table of PROJECT.md: every cell must still name an existing heading / numbered item / file (FG7-52 later scans them by code).
_TOC_CL = "CLAUDE.md"
_RS = "docs/RUNBOOK.md"
_PRJ = "PROJECT.md"
_TW_HEAD = "## Командная работа (кучки и пачки)"
TOC_POINTERS = [
    (_TOC_CL, "| Tiers | CLAUDE.md § Tiers |", "CLAUDE.md", "## Tiers (see"),
    (_TOC_CL, "CLAUDE.md § 1 +", "CLAUDE.md", "1. Recon → scout by default"),
    (_TOC_CL, "+ CLAUDE.md § 2 +", "CLAUDE.md", "2. Implementation from a finished spec → builder"),
    (_TOC_CL, "CLAUDE.md § Rule 2 · drafting → designer", "CLAUDE.md", "### Rule 2 · drafting → designer"),
    (_TOC_CL, "| CLAUDE.md § 11 |", "CLAUDE.md", "11. DoD in every dispatch (DoD-in-every-dispatch rule)"),
    (_TOC_CL, "| Witness; acceptance by witness | CLAUDE.md § 2 |", "CLAUDE.md", "2. Implementation from a finished spec → builder"),
    (_TOC_CL, "| What a builder may run | docs/TESTING.md § Что запускать по своей правке |", TESTING, TESTING_RUN),
    (_TOC_CL, "CLAUDE.md § Rule 4 · witness scope and the BATCH CANON", "CLAUDE.md", "### Rule 4 · witness scope and the BATCH CANON"),
    (_TOC_CL, "docs/RUNBOOK.md § 7. CI на GitHub и BATCH CANON", _RS, RUNBOOK_7),
    (_TOC_CL, "| Which tests are written | docs/TESTING.md |", "docs/TESTING.md", "# Как фордж пишет тесты"),
    (_TOC_CL, "| Critic gate | CLAUDE.md § 3 |", "CLAUDE.md", "3. critic — a MANDATORY acceptance gate"),
    (_TOC_CL, "| Critic review content | .claude/agents/critic.md § 21-24 |", CRITIC, CRIT_21),
    (_TOC_CL, "| Journal | CLAUDE.md § Routing log |", "CLAUDE.md", "## Routing log — logs/journal/<dev>.jsonl"),
    (_TOC_CL, "| Six writers, queue, merge waves | PROJECT.md § Командная работа |", _PRJ, _TW_HEAD),
    (_TOC_CL, "| Cost gates | CLAUDE.md § Rule 12 · Cost gates |", "CLAUDE.md", "### Rule 12 · Cost gates"),
    (_TOC_CL, "| Session hygiene | CLAUDE.md § Command hygiene +", "CLAUDE.md", "## Command hygiene (permission hygiene)"),
    (_TOC_CL, "+ PROJECT.md § Сессия форджа |", _PRJ, "## Сессия форджа"),
    (_TOC_CL, "| Fix the class | CLAUDE.md § 9 |", "CLAUDE.md", "9. Fix the class, not the instance (fix-the-class-not-the-instance"),
    (_TOC_CL, "| Mechanisms | CLAUDE.md § 10 |", "CLAUDE.md", "10. Four questions for every mechanism"),
    (_TOC_CL, "+ docs/TEAMWORK.md |", TEAMWORK, "# Командная работа: механика, которую держит код"),
    (_TOC_CL, "| «Бэклог»; findings | PROJECT.md § Бэклог и находки |", _PRJ, "## Бэклог и находки"),
    (_TOC_CL, "| Owner's principles | docs/OWNER_PRINCIPLES.md |", "docs/OWNER_PRINCIPLES.md", "# Принципы владельца"),
    (_TOC_CL, "| Package change acceptance | PROJECT.md § Как принимается изменение пакета |", _PRJ, "## Как принимается изменение пакета"),
    (_TOC_CL, "PROJECT.md § Как разрабатывается новая идея владельца", _PRJ, "## Как разрабатывается новая идея владельца"),
    (_TOC_CL, "| Release | docs/RUNBOOK.md § 4.1. Шаги релиза |", _RS, "### 4.1. Шаги релиза"),
    (_TOC_CL, "| Language | PROJECT.md § Язык |", _PRJ, "## Язык"),
    (_TOC_CL, "PROJECT.md § Что решать самому, что спрашивать у владельца", _PRJ, "## Что решать самому, что спрашивать у владельца"),
    (_TOC_CL, "+ CLAUDE.md § 11a |", "CLAUDE.md", "11a. Question routing (question-routing rule)"),
    (_TOC_CL, "PROJECT.md § Ссылки на файлы в ответах", _PRJ, "## Ссылки на файлы в ответах"),
    (_TOC_CL, "| .claude/agents/designer.md § 7 |", ".claude/agents/designer.md", "7. READERS OF EVERY TOUCHED FILE"),
    (_TOC_CL, "| Boot diet | .claude/skills/boot-diet/SKILL.md |", ".claude/skills/boot-diet/SKILL.md", "# boot-diet — reacting to a boot-budget breach"),
    (_TOC_CL, "| How rule text for agents is written | .claude/skills/boot-diet/SKILL.md § Как пишутся правила для агентов |", ".claude/skills/boot-diet/SKILL.md", "## Как пишутся правила для агентов"),
    (_TOC_CL, "| Session start/end | PROCESS/SESSION_PROTOCOL.md |", "PROCESS/SESSION_PROTOCOL.md", "# Session Protocol"),
    (_TOC_CL, "CLAUDE.md § Role ≠ tier", "CLAUDE.md", "## Role ≠ tier"),
    (_TOC_CL, "CLAUDE.md § Lead degradation", "CLAUDE.md", "## Lead degradation"),
    (_TOC_CL, "| Dispatcher duties about workers' runs | PROJECT.md § Как принимается изменение пакета +", _PRJ, "## Как принимается изменение пакета"),
    # PROJECT.md's own table (E21: the last row routes to CLAUDE.md, which now exists)
    (_PRJ, "| Где что лежит |", _PRJ, "## Где что лежит"),
    (_PRJ, "| Принципы владельца |", _PRJ, "## Принципы владельца"),
    (_PRJ, "| Как принимается изменение пакета |", _PRJ, "## Как принимается изменение пакета"),
    (_PRJ, "| Бэклог и находки |", _PRJ, "## Бэклог и находки"),
    (_PRJ, "| Как разрабатывается новая идея владельца |", _PRJ, "## Как разрабатывается новая идея владельца"),
    (_PRJ, "| Прогоны и эксперименты |", _PRJ, "## Прогоны и эксперименты"),
    (_PRJ, "| Сессия форджа |", _PRJ, "## Сессия форджа"),
    (_PRJ, "| Командная работа (кучки и пачки) |", _PRJ, _TW_HEAD),
    (_PRJ, "| Релиз |", _PRJ, "## Релиз"),
    (_PRJ, "| Как пишутся правила для агентов |", _PRJ, "## Как пишутся правила для агентов"),
    (_PRJ, "| Язык |", _PRJ, "## Язык"),
    (_PRJ, "| Что решать самому, что спрашивать у владельца |", _PRJ, "## Что решать самому, что спрашивать у владельца"),
    (_PRJ, "| Ссылки на файлы в ответах |", _PRJ, "## Ссылки на файлы в ответах"),
    (_PRJ, "| Все темы → `CLAUDE.md` § Contents |", "CLAUDE.md", "## Contents — topic → where to read"),
]
POINTERS = POINTERS + TOC_POINTERS


def squash(text):
    return " ".join(text.split()).casefold()


def is_scanned(rel):
    rel = rel.replace("\\", "/")
    return rel.endswith(TEXT_SUFFIXES) and not any(rel == e or rel.startswith(e) for e in EXCLUDED)


def _tracked_all(root):
    if (root / ".git").exists():          # a checkout or a worktree (`.git` is a file there)
        out = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], capture_output=True, check=True).stdout
        return [p for p in out.decode("utf-8", "replace").split("\0") if p]
    return [p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()]


def tracked(root):
    return sorted(r for r in _tracked_all(root) if is_scanned(r))


def load(root, rels):
    texts = {}
    for rel in rels:
        try:
            texts[rel] = squash((root / rel).read_text(encoding="utf-8", errors="replace"))
        except OSError:                     # listed but gone from the tree: it carries nothing
            continue
    return texts


def violations(key, owner, texts):
    k = squash(key)
    found = sorted(rel for rel, t in texts.items() if k in t)
    out = [] if owner in found else ["owner %s lost its key" % owner]
    return out + ["%s restates the owner %s" % (rel, owner) for rel in found if rel != owner]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def texts():
    return load(ROOT, tracked(ROOT))


def test_scan_sees_the_owners(texts):
    """Positive control: a broken scan (no git, a wrong root) cannot pass silently."""
    assert [o for _, o, _ in OWNER_KEYS if o not in texts] == []


@pytest.mark.parametrize("aspect,owner,key", OWNER_KEYS, ids=[a for a, _, _ in OWNER_KEYS])
def test_one_owner_per_key(texts, aspect, owner, key):
    assert violations(key, owner, texts) == []


@pytest.mark.parametrize("carrier,pointer,target,anchor", POINTERS, ids=["%s->%s" % (c, t) for c, _, t, _ in POINTERS])
def test_pointer_resolves(carrier, pointer, target, anchor):
    assert squash(pointer) in squash(read(carrier)), "%s lost its pointer %r" % (carrier, pointer)
    assert squash(anchor) in squash(read(target)), "%s no longer has %r (a renamed section: update the pointer)" % (target, anchor)


def test_two_vocabularies_names_no_haiku():
    assert "haiku" not in squash(read("docs/TWO_VOCABULARIES.md"))


def test_negative_control_restatement_is_named():
    t = {"owner.md": squash("x KEY sentence y"), "other.md": squash("KEY\n   SENTENCE")}
    assert violations("key sentence", "owner.md", t) == ["other.md restates the owner owner.md"]


def test_negative_control_owner_lost_its_key():
    assert violations("key sentence", "owner.md", {"owner.md": "", "other.md": "key sentence"}) == [
        "owner owner.md lost its key", "other.md restates the owner owner.md"]


def test_negative_control_scope():
    assert not is_scanned("AGENTS.md") and not is_scanned("docs/tasks/specs/t-1.md") and not is_scanned("a.png")
    assert not is_scanned("tools/fixtures/host_pre_delivery_CLAUDE.md") and not is_scanned(SELF)
    assert is_scanned("CLAUDE.md") and is_scanned(".claude/agents/critic.md")


# ---- K-REG / K-NOBRIEF ----
SIBLING_MAP = "docs/SIBLING_MAP.md"
DOOR = "fold the text into a main document, or move the file under docs/tasks/specs/"
DELETED = [                                     # (path, stem or None); wave 2 adds docs/tasks/exchange-form.md
    ("docs/tasks/critic-diff-brief.md", "critic-diff-brief"),
    ("plans/builder-rules.md", "builder-rules"),
    ("docs/tasks/pre-release-0.9-brief-common.md", "pre-release-0.9-brief-common"),
    ("docs/tasks/pre-release-0.9-critic-brief.md", "pre-release-0.9-critic-brief"),
    ("docs/tasks/test-diet-brief.md", "test-diet-brief"),
    ("docs/tasks/test-diet-fold-brief.md", "test-diet-fold-brief"),
    ("docs/retro/README.md", None),             # no stem: "README" is a common word
]
ALLOWED = {".claude/agents/builder.md": "\"builder-rules N\" in package comments = the former numbering of the builder's rules"}
BRIEF_PATH_RE = re.compile(r"docs/tasks/[^/\s`'\"]*brief[^/\s`'\"]*\.md")


def main_documents(root):
    """MAIN = the files of axis 31 whose Owner / pointer cell starts with owner or procedure (E11: a missing table or a
    malformed row yields fewer documents, never a pass: test_register_sees_the_main_documents)."""
    lines = (root / SIBLING_MAP).read_text(encoding="utf-8").splitlines()
    table = md_table.table_after(lines, "Axis 31")
    if table is None:
        return []
    header, rows = table
    names = [h.casefold() for h in header]
    if "file" not in names or "owner / pointer" not in names:
        return []
    fi, oi = names.index("file"), names.index("owner / pointer")
    out = set()
    for cells, _ in rows:
        if len(cells) <= max(fi, oi) or not cells[oi].casefold().startswith(("owner", "procedure")):
            continue
        m = re.match(r"`([^`]+\.md)`", cells[fi])
        if not m:
            continue
        path = m.group(1)
        if "*" in path:
            out.update(q.relative_to(root).as_posix() for q in root.glob(path))
        elif (root / path).is_file():
            out.add(path)
    return sorted(out)


def forbidden_hits(text):
    t = text.casefold().replace("\\", "/")
    hits = BRIEF_PATH_RE.findall(t)
    for path, stem in DELETED:
        hits += [path.casefold()] * (path.casefold() in t)
        hits += [stem] * bool(stem and stem in t)
    return hits


def strip_allowed(rel, text):
    """Blank the ONE allowed sentence of its file (through its final period), keeping line breaks."""
    start = ALLOWED.get(rel)
    if not start:
        return text
    m = re.search(r"\s+".join(re.escape(w) for w in start.split()) + r".*?\.(?=\s|$)", text, re.S)
    if not m:
        return text
    return text[:m.start()] + re.sub(r"[^\n]", " ", m.group(0)) + text[m.end():]


def scan(rel, text):
    return [(n, h) for n, line in enumerate(strip_allowed(rel, text).splitlines(), 1) for h in forbidden_hits(line)]


MAIN = main_documents(ROOT)


def test_register_sees_the_main_documents():
    """Positive control: a broken parse of the axis-31 table fails here, never passes with an empty MAIN."""
    need = ["CLAUDE.md", "docs/TESTING.md", ".claude/agents/critic.md", "ai-packages/qa-factory/design/architecture.md"]
    assert [n for n in need if n not in MAIN] == []


@pytest.mark.parametrize("rel", MAIN)
def test_no_main_document_names_a_deleted_file(rel):
    hits = scan(rel, read(rel))
    assert hits == [], "%s names a deleted file at %s; door: %s" % (rel, hits[:5], DOOR)


@pytest.mark.parametrize("path", [d for d, _ in DELETED])
def test_deleted_files_stay_untracked(path):
    assert path not in _tracked_all(ROOT), "%s is tracked again; door: %s" % (path, DOOR)


def test_no_brief_file_at_the_top_of_docs_tasks():
    bad = [p for p in _tracked_all(ROOT) if re.fullmatch(r"docs/tasks/[^/]*brief[^/]*\.md", p, re.I)]
    assert bad == [], "%s; door: %s" % (bad, DOOR)


_BR = ".claude/agents/builder.md"
_OWN = ALLOWED[_BR] + ": 1, 9 -> rule 11; 7b, 7c -> `docs/TESTING.md` x; 8 -> FR-4."
FORBIDDEN_ROWS = [      # (rel, text, hit expected)
    ("x.md", "docs\\tasks\\Critic-Diff-Brief.md", True),
    ("x.md", "builder-rules 7b", True),                                   # B6 false-green class: a bare stem
    ("x.md", "(builder-rules п. 13)", True),
    ("x.md", "critic-diff-brief question 9", True),
    ("x.md", "docs/tasks/specs/td-11-lead-brief.md", False),
    ("x.md", "INTENT BRIEF", False),
    ("x.md", '"notes":"brief: what was delegated"', False),
    ("x.md", "```\nplans/builder-rules.md\n```", True),                    # fences are not exempt
    (_BR, _OWN, False),
    (_BR, _OWN + " Elsewhere: builder-rules 7b.", True),                  # the same stem in another sentence
    (_BR, "Other sentence builder-rules N. " + _OWN, True),
    ("x.md", _OWN, True),                                                 # the allowance is for builder.md only
    ("x.md", "docs/retro/inbox/x.md", False),
    ("x.md", "docs/retro/README.md", True),
]


@pytest.mark.parametrize("rel,text,hit", FORBIDDEN_ROWS, ids=[str(i) for i in range(len(FORBIDDEN_ROWS))])
def test_forbidden_hits(rel, text, hit):
    assert bool(scan(rel, text)) is hit, (rel, text, scan(rel, text))
