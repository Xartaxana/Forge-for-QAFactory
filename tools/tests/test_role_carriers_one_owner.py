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
COST = "6. Cost gates (D-0035"
HYGIENE_6 = "6. An environment-negative claim requires verification: empty output"

# (aspect id, owner, key)
OWNER_KEYS = [
    ("hand-back:builder", ".claude/agents/builder.md", "DONE / PARTIAL / NOT DONE per spec item"),
    ("hand-back:critic", ".claude/agents/critic.md", "the verdict line and the number of blocking findings"),
    ("hand-back:designer", ".claude/agents/designer.md", "the forks by id with one line each"),
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
    ("cost:queue", "CLAUDE.md", "queue is kept FULL"),
]

# (carrier, pointer text it must hold, target, anchor the target must still hold)
POINTERS = [
    ("PROJECT.md", "`plans/builder-rules.md` п. 7b", RULES, RULES_7B),
    ("PROJECT.md", "`docs/tasks/critic-diff-brief.md`", BRIEF, "## The two layers"),
    (RULES, "правило 7 `.claude/agents/builder.md`", ".claude/agents/builder.md", "7. The report is a FILE; the final message is its digest."),
    (RULES, "host-адаптация 6 `CLAUDE.md`", "CLAUDE.md", COST),
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
    ("docs/CLAUDE_HOST_ADAPTATIONS_FULL.md", "the rule text is `CLAUDE.md` host adaptation 6", "CLAUDE.md", COST),
    ("SYSTEM_PROMPT.md", "CLAUDE.md rule 9", "CLAUDE.md", "9. Fix the class, not the instance (fix-the-class-not-the-instance"),
    ("docs/RUNBOOK.md", "`plans/builder-rules.md` п. 7b", RULES, RULES_7B),
    ("docs/RUNBOOK.md", "host-адаптация 6 `CLAUDE.md`", "CLAUDE.md", COST),
    ("docs/TWO_VOCABULARIES.md", "`delegation.config.yaml`", "delegation.config.yaml", "scout:"),
]


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
