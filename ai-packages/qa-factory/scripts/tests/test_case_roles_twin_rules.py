"""test_case_roles_twin_rules.py - RN1-7: rule 5a of the case designer and its twin 7d in the case critic, key presence.

The designer says a case on a field whose value goes to the server or redraws the page has the Then "value kept whole,
field still in focus"; the critic must not strike that Then and must flag its absence (AR-19: author/critic twins change
together). The keys below are fixed before the run and must stand VERBATIM in BOTH agent files. A NEGATIVE control
removes each key from a copy of each text and requires the same helper to report it absent (it can fail).

Runnable on its own: `python -B scripts/tests/test_case_roles_twin_rules.py`.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness import PLUGIN_ROOT, check, finish  # noqa: E402

FILES = ("agents/qa-case-designer.md", "agents/qa-case-critic.md")
KEYS = ("goes to the server or redraws the page", "whole", "still in focus")


def missing(text: str) -> list:
    return [k for k in KEYS if k not in text]


for rel in FILES:
    text = (PLUGIN_ROOT / rel).read_text(encoding="utf-8")
    check(f"{rel}: carries every twin key", not missing(text), f"missing {missing(text)}")
    for key in KEYS:
        broken = text.replace(key, "")
        check(f"{rel}: negative control, copy without {key!r} is red", key in missing(broken))

finish("test_case_roles_twin_rules")
