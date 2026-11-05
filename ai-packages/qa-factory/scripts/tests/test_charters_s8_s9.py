#!/usr/bin/env python3
"""The charters of S8 and S9 (spec t-1765 X7-4): qa-bug-reporter, qa-doc-scribe, qa-retro-analyst.

Each test names the ONE mutation that kills it (builder-rules 7a):
  test_shape_is_clean                  -> restore the old Procedure heading in one of the three files
  test_front_matter_is_verbatim        -> change `tools` of one role (FR-56)
  test_craft_keys_verbatim             -> delete a key sentence (K-S8b, K-S8s, K-S9)
  test_no_principle_numbers_or_ac      -> write `P19` or `AC` in a craft line (K-C1, K-C4)
  test_negative_controls               -> make `keys_missing` always return []
  test_craft_share                     -> move a craft section's marker to `process`
  test_brief_rows_and_key_pages        -> drop a role from brief-form.json or its handoff-keys entry from inject-map.json
  test_retro_reads_only_the_numbers    -> name the journal or `state/cost` in the retro charter again
Run: python -B -m pytest scripts/tests/test_charters_s8_s9.py -q
"""
import json
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402

sys.path.insert(0, str(harness.SCRIPTS))
import charter  # noqa: E402
import role_load  # noqa: E402

PLUGIN = Path(harness.SCRIPTS).parent
CHARTERS = ("qa-bug-reporter", "qa-doc-scribe", "qa-retro-analyst")
CRAFT_SHARE_MIN = 0.40
# The keys: sentences of the tester's craft, verbatim (spec X7-4: K-S8b, K-S8s; K-S9 is this node's own for the retro).
KEYS = {
    "qa-bug-reporter": ("red test", "who loses what", "fewest steps"),
    "qa-doc-scribe": ("within these boundaries", "found, not run", "another machine"),
    "qa-retro-analyst": ("Where did I not look", "Name a trap by its kind", "what its turns bought"),
}
# Front matter verbatim (FR-56): what the host reads as the role's tools and description.
FRONT = {
    "qa-bug-reporter": ("Read, Grep, Glob, Write, Edit, Bash", "Agent, Task"),
    "qa-doc-scribe": ("Read, Grep, Glob, Bash, Write, Edit", "Agent, Task"),
    "qa-retro-analyst": ("Read, Grep, Glob, Bash, Write, Edit", "Agent, Task"),
}
PRINCIPLE_NUMBER = re.compile(r"\b(P[0-9]{1,2}|D-0[0-9]{3})\b")
AC_WORD = re.compile(r"\bAC\b|acceptance criteria", re.IGNORECASE)


def text_of(role: str) -> str:
    return (PLUGIN / "agents" / f"{role}.md").read_text(encoding="utf-8")


def keys_missing(text: str, keys) -> list:
    """The keys the text does not hold (whitespace-normalised, so a wrapped line still holds its key)."""
    flat = " ".join(text.split())
    return [k for k in keys if k not in flat]


def craft_share(text: str) -> float:
    craft, _ignored = role_load.craft_split(text)
    return craft / len(text.encode("utf-8"))


@pytest.mark.parametrize("role", CHARTERS)
def test_shape_is_clean(role):
    text = text_of(role)
    assert charter.is_charter(text)
    assert charter.charter_errors(text) == []
    assert charter.stray_markers(text) == []


@pytest.mark.parametrize("role", CHARTERS)
def test_front_matter_is_verbatim(role):
    head = text_of(role).split("---")[1]
    fields = dict(line.split(": ", 1) for line in head.strip().split("\n"))
    tools, disallowed = FRONT[role]
    assert fields["name"] == role
    assert fields["tools"] == tools
    assert fields["disallowedTools"] == disallowed
    assert fields["description"].endswith(f"Dispatched by qa-story at {'S9' if role == 'qa-retro-analyst' else 'S8'}.")


@pytest.mark.parametrize("role", CHARTERS)
def test_craft_keys_verbatim(role):
    assert keys_missing(text_of(role), KEYS[role]) == []


@pytest.mark.parametrize("role", CHARTERS)
def test_no_principle_numbers_or_ac(role):
    text = text_of(role)
    assert PRINCIPLE_NUMBER.findall(text) == []          # K-C1
    assert AC_WORD.findall(text) == []                   # K-C4


def test_negative_controls():
    """A check that cannot fail proves nothing: each predicate must refuse a seeded fault."""
    good = text_of("qa-doc-scribe")
    assert keys_missing(good, KEYS["qa-doc-scribe"]) == []
    assert keys_missing(good.replace("another machine", "elsewhere"), KEYS["qa-doc-scribe"]) == ["another machine"]
    assert PRINCIPLE_NUMBER.findall(good + "\nSee P19 and D-0043.") == ["P19", "D-0043"]
    assert AC_WORD.findall(good + "\nEvery AC is covered.") == ["AC"]
    broken = good.replace("<!-- kind: craft -->\n## Techniques", "<!-- kind: process -->\n## Techniques")
    assert any("Techniques` is craft, its marker says process" in e for e in charter.charter_errors(broken))
    assert craft_share(broken) < craft_share(good)


@pytest.mark.parametrize("role", CHARTERS)
def test_craft_share(role):
    share = craft_share(text_of(role))
    print(f"{role}: craft share {share:.3f}")
    assert share >= CRAFT_SHARE_MIN


def test_brief_rows_and_key_pages():
    form = json.loads((PLUGIN / "references" / "brief-form.json").read_text(encoding="utf-8"))
    imap = json.loads((PLUGIN / "references" / "inject-map.json").read_text(encoding="utf-8"))
    for role in CHARTERS:
        row = form["roles"][role]
        for key in ("non_goals", "questions"):
            assert row[key].strip() and len(row[key]) <= form["line_chars"]
        assert f"plugin:references/slices/{role}/handoff-keys.md" in imap["roles"][role]
        assert (PLUGIN / "references" / "slices" / role / "handoff-keys.md").exists()


def test_retro_reads_only_the_numbers():
    """The S9 input is retro-numbers.json (X7-6); the charter names neither the journal nor the cost files."""
    text = text_of("qa-retro-analyst")
    assert "work/retro-numbers.json" in text
    assert "state/cost" not in text and "journal" not in text
    assert "on every story: the retro is always the full one" in text
