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
Run from the repo root: python -m pytest tools/tests/test_role_carriers_one_owner.py -q
"""
import os
import pathlib
import subprocess

import pytest

REAL = pathlib.Path(__file__).resolve().parents[2]
ROOT = pathlib.Path(os.environ.get("ROLE_CARRIERS_ROOT") or REAL)
SELF = "tools/tests/test_role_carriers_one_owner.py"
TEXT_SUFFIXES = (".md", ".py", ".json", ".yaml", ".yml", ".txt")
EXCLUDED = ("AGENTS.md", "DECISIONS.md", "docs/DECISIONS_ARCHIVE.md", "ai-packages/", "experiments/", "logs/", "kb/",
            "docs/tasks/specs/", "docs/tasks/handoffs/", "docs/tasks/compact-snapshots/", "docs/task_reports/",
            "plans/piles/", "tools/fixtures/", SELF)

BRIEF = "docs/tasks/critic-diff-brief.md"
RULES = "plans/builder-rules.md"
RULES_7B = "7b. **Уровень билдера и уровень пачки**"
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
    ("scope:builder", RULES, "не регрессия, не соседи, не большие файлы"),
    # scope:mutation retired by the owner's word 28.10 and 10.11.2026 (docs/TESTING.md): the mutation list is no longer written
    ("scope:tests", RULES, "Покрасневший пин удаляется, а не чинится"),
    ("review:critic", BRIEF, "functions over roughly 60 lines or with more than three nesting levels in the NEW code"),
    ("review:one-road", BRIEF, "a line for the coordinator to tell someone is itself a finding"),
    ("routing:rule-11", "CLAUDE.md", "a spec silent on an edge that its own requirements create is a dispatcher defect"),
    ("routing:hygiene-6", "CLAUDE.md", "from an INCORRECTLY invoked tool is a miscall, not proof the object is absent"),
    ("routing:rule-9", "CLAUDE.md", "the rule against recurrence goes on the highest level that ties the siblings together"),
    ("cost:cap", "CLAUDE.md", "WARN 250K, STOP 400K"),
    ("cost:queue", "PROJECT.md", "цель держать 6 пишущих билдеров"),      # 63bbd5e: the full-queue text moved to PROJECT.md item 12; CLAUDE.md rule 12 points there; re-quoted with R1 (boot-by-topic, FG7-51)
    ("tests:oracle", "docs/TESTING.md", "тест, чьё ожидание переписано из того, что код напечатал, может только пройти"),
    ("tests:line", "docs/TESTING.md", "Пункт без поведения (перенос текста, переименование) строки не получает"),
    ("tests:files", "docs/TESTING.md", "Новый файл верен, когда случай не ложится ни в одну из них"),
]

# (carrier, pointer text it must hold, target, anchor the target must still hold)
POINTERS = [
    ("PROJECT.md", "`plans/builder-rules.md` п. 7b", RULES, RULES_7B),
    ("PROJECT.md", "`docs/tasks/critic-diff-brief.md`", BRIEF, "## The two layers"),
    (RULES, "правило 7 `.claude/agents/builder.md`", ".claude/agents/builder.md", "7. The report is a FILE; the final message is its digest."),
    (RULES, "`CLAUDE.md` rule 12, Cost gates", "CLAUDE.md", COST),
    (".claude/agents/builder.md", "`plans/builder-rules.md` 7b", RULES, RULES_7B),
    (".claude/agents/builder.md", "the rule is CLAUDE.md command hygiene point 6", "CLAUDE.md", HYGIENE_6),
    (".claude/agents/critic.md", "the rule is CLAUDE.md command hygiene point 6", "CLAUDE.md", HYGIENE_6),
    (".claude/agents/critic.md", "docs/tasks/critic-diff-brief.md items 6-7", BRIEF, "6. **DUPLICATION AND CONSISTENCY**"),
    (".claude/agents/critic.md", "docs/tasks/critic-diff-brief.md «The two layers»", BRIEF, "## The two layers"),
    (".claude/agents/critic.md", "docs/tasks/critic-diff-brief.md item 12", BRIEF, "12. **ONE ROAD**"),
    (".claude/agents/designer.md", "the text is CLAUDE.md rule 11", "CLAUDE.md", "11. DoD in every dispatch (DoD-in-every-dispatch rule)"),
    (".claude/agents/designer.md", "`plans/builder-rules.md` 7b", RULES, RULES_7B),
    (BRIEF, "`.claude/agents/critic.md` rules 16-17", ".claude/agents/critic.md", "16. The report is a FILE; the final message is its digest."),
    ("CLAUDE.md", "`docs/tasks/critic-diff-brief.md` items 6-7", BRIEF, "7. **CODE QUALITY**"),
    ("docs/CLAUDE_HOST_ADAPTATIONS_FULL.md", "the rule text is `docs/tasks/critic-diff-brief.md`", BRIEF, "6. **DUPLICATION AND CONSISTENCY**"),
    ("docs/CLAUDE_HOST_ADAPTATIONS_FULL.md", "the rule text is `CLAUDE.md` rule 12, Cost gates", "CLAUDE.md", COST),
    ("SYSTEM_PROMPT.md", "CLAUDE.md rule 9", "CLAUDE.md", "9. Fix the class, not the instance (fix-the-class-not-the-instance"),
    ("docs/RUNBOOK.md", "`plans/builder-rules.md` п. 7b", RULES, RULES_7B),
    ("docs/RUNBOOK.md", "`CLAUDE.md` rule 12, Cost gates", "CLAUDE.md", COST),
    ("docs/TESTING.md", "`docs/tasks/critic-diff-brief.md` «The two layers»", BRIEF, "## The two layers"),
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
    (RULES, "`docs/RUNBOOK.md` §7", "docs/RUNBOOK.md", RUNBOOK_7),
    ("docs/TESTING.md", "`plans/builder-rules.md` п. 7b", RULES, RULES_7B),
    (BRIEF, "`plans/builder-rules.md` 7b", RULES, RULES_7B),
    ("PROJECT.md", "`.claude/skills/boot-diet/SKILL.md` § Как пишутся правила для агентов", ".claude/skills/boot-diet/SKILL.md", "## Как пишутся правила для агентов"),
    ("CLAUDE.md", "PROJECT.md § Сессия форджа", "PROJECT.md", "## Сессия форджа"),
    (TEAMWORK, "`PROJECT.md` «Командная работа» п. 3", "PROJECT.md", "3. **Зоны файлов пачек «в работе» не пересекаются** — правило: `docs/TEAMWORK.md` § 3"),
    (RULES, "«Откуда берётся ожидаемое значение»", "docs/TESTING.md", "### Откуда берётся ожидаемое значение"),
    (RULES, "`docs/TESTING.md` «Тест может упасть»", "docs/TESTING.md", "### Тест может упасть"),
    (RULES, "по цели `docs/TESTING.md` «Бюджет / Файлы»", "docs/TESTING.md", "- **Файлы**"),
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
    (_TOC_CL, "| What a builder may run | plans/builder-rules.md § 7b |", RULES, RULES_7B),
    (_TOC_CL, "CLAUDE.md § Rule 4 · witness scope and the BATCH CANON", "CLAUDE.md", "### Rule 4 · witness scope and the BATCH CANON"),
    (_TOC_CL, "docs/RUNBOOK.md § 7. CI на GitHub и BATCH CANON", _RS, RUNBOOK_7),
    (_TOC_CL, "| Which tests are written | docs/TESTING.md |", "docs/TESTING.md", "# Как фордж пишет тесты"),
    (_TOC_CL, "| Critic gate | CLAUDE.md § 3 |", "CLAUDE.md", "3. critic — a MANDATORY acceptance gate"),
    (_TOC_CL, "| Critic review content | docs/tasks/critic-diff-brief.md |", BRIEF, "# Standing brief for the critic gate on a builder diff"),
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


def tracked(root):
    if (root / ".git").exists():          # a checkout or a worktree (`.git` is a file there)
        out = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], capture_output=True, check=True).stdout
        rels = [p for p in out.decode("utf-8", "replace").split("\0") if p]
    else:
        rels = [p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()]
    return sorted(r for r in rels if is_scanned(r))


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


def test_negative_control_real_key_in_a_copy(tmp_path):
    """A real key pasted into a COPY of a pointer file -> named (a check that cannot fail is not a check)."""
    _, owner, key = OWNER_KEYS[6]                      # review:critic
    for rel in (owner, ".claude/agents/critic.md"):
        dst = tmp_path / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(read(rel), encoding="utf-8")
    with (tmp_path / ".claude/agents/critic.md").open("a", encoding="utf-8") as f:
        f.write("\n" + key + "\n")
    assert violations(key, owner, load(tmp_path, tracked(tmp_path))) == [
        ".claude/agents/critic.md restates the owner %s" % owner]
