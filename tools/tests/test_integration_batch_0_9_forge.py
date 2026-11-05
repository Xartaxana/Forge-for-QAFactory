"""Key-presence check for the forge half of the pre-release 0.9 integration batch (t-569).

The files under test are markdown with no test set of their own, so this is the doc-dispatch witness of
CLAUDE.md rule 11: the KEYS are quoted verbatim from the dispatch's DoD (and, where the dispatch quotes no
phrase, from the batch carrier it names as "given", docs/tasks/pre-release-0.9-integration-batch.md), written
BEFORE the run; the script is committed; and a NEGATIVE control exists - set BATCH_FORGE_BREAK_KEY=<key id>
and that one key is perturbed, so the run must fail on exactly that id (an evergreen script that cannot fail
is indistinguishable from a broken one).

Run from the repository root:
    python -m pytest tools/tests/test_integration_batch_0_9_forge.py -q -p no:cacheprovider
Negative control:
    BATCH_FORGE_BREAK_KEY=axis-9-title python -m pytest tools/tests/test_integration_batch_0_9_forge.py -q
"""

import os
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]

# (key id, file, line prefix that scopes the search to one row / heading ("" = whole file), key)
KEYS = [
    # SIBLING_MAP: the three new axis titles (E-3), as the dispatch writes them
    ("axis-9-title", "docs/SIBLING_MAP.md", "## Axis 9", "is this a test file"),
    ("axis-10-title", "docs/SIBLING_MAP.md", "## Axis 10", "git-top readers"),
    ("axis-11-title", "docs/SIBLING_MAP.md", "## Axis 11", "shell-command recognizers"),
    ("axis-9-symmetry", "docs/SIBLING_MAP.md", "| The symmetry on this axis",
     "program position: commit shape ↔ delivery shape"),
    # DECISIONS: D-0033 and the C5 clause of D-0026 (E-4)
    ("d-0033-row", "DECISIONS.md", "- D-0033", "D-0033"),
    ("d-0033-basis", "DECISIONS.md", "- D-0033", "поддерживать порядок"),
    # the Lead moved the C5 clause out of D-0026's line (append-only log) into the amending line D-0034
    ("d-0026-c5", "DECISIONS.md", "- D-0034", "a precondition declared after the carry asks again"),
    ("d-0026-word", "DECISIONS.md", "- D-0034", "(the owner's word 07.10.2026 07:20: «ок»"),
    # BACKLOG: the B-420 row (E-2) and the B-410 late defects (E-2)
    ("b-420-pipelines", "plans/BACKLOG.md", "| B-420 |", "7877550"),
    ("b-420-pipelines-2", "plans/BACKLOG.md", "| B-420 |", "7877559"),
    ("b-420-fix", "plans/BACKLOG.md", "| B-420 |", "378bf8b"),
    ("b-420-green", "plans/BACKLOG.md", "| B-420 |", "7878100"),
    ("b-420-green-sha", "plans/BACKLOG.md", "| B-420 |", "4b77511"),
    ("b-410-home", "plans/BACKLOG.md", "| B-410 |", "Path.home()"),
    ("b-410-cap", "plans/BACKLOG.md", "| B-410 |", "19000"),
    ("b-410-fix", "plans/BACKLOG.md", "| B-410 |", "22a8b6f"),
    # builder-rules: the lines of E-5 (the dispatch counts five and lists six)
    ("br-polling-loop", "plans/builder-rules.md", "", "until grep -q … ; do sleep N; done"),
    ("br-polling-deadline", "plans/builder-rules.md", "",
     "a wait is bounded by a deadline and names the file it waits for"),
    ("br-size-pin", "plans/builder-rules.md", "", "size pin is a cap"),
    ("br-lint-console", "plans/builder-rules.md", "", "`lint_ratchet --check` + the console scan"),
    ("br-package", "plans/builder-rules.md", "contains:напрямую не запускать",
     "pytest в пакете напрямую не запускать"),
    ("br-confession", "plans/builder-rules.md", "",
     "a confession of a hygiene deviation carries file:line"),
    ("br-witness", "plans/builder-rules.md", "", "a witness is pasted, not typed"),
    # the t-468 Consumer table amendment (E-8), on the test_code row
    ("t468-amendment", "docs/tasks/specs/t-468-b-407-single-tuning-rest.md", "| validate `is_test_code` (C)",
     "amended 07.10 (t-562, the Lead's override)"),
]


def _text(rel):
    return (REPO / rel).read_text(encoding="utf-8")


def _scoped(text, prefix):
    if not prefix:
        return text
    if prefix.startswith("contains:"):
        part = prefix[len("contains:"):]
        return "\n".join(ln for ln in text.splitlines() if part in ln)
    return "\n".join(ln for ln in text.splitlines() if ln.startswith(prefix))


def _key(key_id, key):
    # the negative control: one key, chosen by id, is made impossible to find
    if os.environ.get("BATCH_FORGE_BREAK_KEY") == key_id:
        return key + " ~deliberately broken~"
    return key


@pytest.mark.parametrize("key_id,rel,prefix,key", KEYS, ids=[k[0] for k in KEYS])
def test_the_key_is_present(key_id, rel, prefix, key):
    scope = _scoped(_text(rel), prefix)
    assert scope, f"{rel}: no line starts with {prefix!r}"
    needle = _key(key_id, key)
    assert needle in scope, f"{rel}: key {key_id} not found: {needle!r} (scope {prefix!r})"


def test_the_map_names_exactly_the_axes_the_gate_will_read():
    # mechanism_gate reads `## Axis N` headings; 8 old axes + the three new ones
    heads = [ln for ln in _text("docs/SIBLING_MAP.md").splitlines() if ln.startswith("## Axis ")]
    assert len(heads) >= 11, heads
