"""Doc witness for node A1 of spec t-1765 (D-0060): the keys K1, K5-K9 quoted verbatim from the spec's section 7,
run as a test with a NEGATIVE control (rule 11, DOC-DISPATCH WITNESS). The texts land forge-first (F-6 (a)); the
census and the craft split are named by file name only until A3/A4 land."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _count(rel: str, needle: str) -> int:
    return (ROOT / rel).read_text(encoding="utf-8").count(needle)


def _grep_c(rel: str, pattern: str) -> int:
    return len(re.findall(pattern, (ROOT / rel).read_text(encoding="utf-8"), flags=re.M))


def test_k1_p27_once():
    assert _count("PROJECT.md", "**P27.**") == 1


def test_k5_question_11_once():
    assert _count("docs/tasks/critic-diff-brief.md", "11. **JUDGMENT**") == 1


def test_k6_designer_rule_and_host_adaptation_10():
    assert _count(".claude/agents/designer.md", "the owner it serves") == 1
    lines = [ln for ln in (ROOT / "CLAUDE.md").read_text(encoding="utf-8").splitlines() if ln.startswith("10. ")]
    assert lines and "P27" in lines[0]


def test_k7_check_41_once():
    assert _count("PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md", "**Where judgment lives (P27, AR-29") == 1


def test_k8_axis_heading_once():
    assert _grep_c("docs/SIBLING_MAP.md", r"^## Axis 32 — Where judgment lives:") == 1


def test_k9_ratchet_members_named():
    for rel in ("docs/SIBLING_MAP.md", "docs/tasks/critic-diff-brief.md"):
        assert _count(rel, "judgment-census") + _count(rel, "process_ratchet_tokens") >= 2, rel


def test_negative_control_absent_key():
    # an evergreen witness that cannot fail is indistinguishable from a broken one
    assert _count("PROJECT.md", "**P99.**") == 0
    assert _grep_c("docs/SIBLING_MAP.md", r"^## Axis 99 — ") == 0
