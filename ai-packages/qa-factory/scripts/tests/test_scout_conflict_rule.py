#!/usr/bin/env python3
"""The scout checks a requirement/code conflict against every source before it halts (RC1-13).

A conflict the ticket's comments, description or linked issues settle is not a halt: the digest
records the source and the quote that lifts it. Presence test over the phase file and the agent
file, with a negative control: a copy that loses a key must fail the check.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import PLUGIN_ROOT, check, finish  # noqa: E402

S1 = PLUGIN_ROOT / "skills" / "qa-story" / "phases" / "s1.md"
SCOUT = PLUGIN_ROOT / "agents" / "qa-scout.md"
KEYS = ("comments", "linked", "quote", "unresolved")


def missing(text: str) -> list:
    return [key for key in KEYS if key not in text]


def conflict_text(text: str) -> str:
    """Only the conflict passages, so a key elsewhere in the file cannot satisfy the check."""
    return "\n".join(line for line in text.splitlines() if "conflict" in line.lower()
                     or "unresolved" in line.lower() or "settle" in line.lower())


s1_text = S1.read_text(encoding="utf-8")
scout_text = SCOUT.read_text(encoding="utf-8")
check("s1.md carries the conflict-resolution keys", not missing(s1_text), str(missing(s1_text)))
check("qa-scout.md carries the conflict-resolution keys", not missing(scout_text),
      str(missing(scout_text)))
# the halt itself stays for an unresolved conflict
check("s1.md keeps the halt digest", "requirement/code conflict:" in s1_text)
# spec t-1765 X1 (B-D, register outcome "dropped" - for the critic): a conflict is no longer a halt in the scout's charter (S1 par. 3.2,
# E-X14); the halt line "requirement/code conflict:" is retired there. The carrier that replaced the rule is the charter's
# technique "Triangulate a conflict" (craft) and the When to ask bullet (the key; t-1765 X1 fix-4, F7): an unsettled conflict goes to
# `unresolved_facts` with both quotes.
check("qa-scout.md sends an unsettled conflict to `unresolved_facts` (the halt line is retired)",
      "A conflict nothing settles goes to `unresolved_facts` with both quotes." in scout_text and "requirement/code conflict:" not in scout_text)
# the rule sits next to the conflict, not elsewhere
check("s1.md conflict passages carry the rule", not missing(conflict_text(s1_text)),
      str(missing(conflict_text(s1_text))))
check("qa-scout.md conflict passages carry the rule", not missing(conflict_text(scout_text)),
      str(missing(conflict_text(scout_text))))

# negative control: every key removed from a copy turns the check red
for key in KEYS:
    for label, text in (("s1.md", s1_text), ("qa-scout.md", scout_text)):
        check(f"control: {label} without '{key}' is caught", key in missing(text.replace(key, "")))

finish("test_scout_conflict_rule")
