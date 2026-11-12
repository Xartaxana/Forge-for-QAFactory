"""Anchors of the hand-back carrier rule texts (t-744 / t-754, F5-1 N1, feature F19): the rule "the report is a FILE at the
dispatch's `handoff:` path, the final message is its pointer plus a per-item status of at most 2,000 characters and 3 + N lines" sits in the numbered rule that check 28 (a)
of PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md anchors (critic 16, builder 7, designer 5), scout.md carries only its one extraction
sentence (F-1 B: no Write, no 25-line rule), judge.md is untouched (E-25), check 28 (d) carries its
key, and the brief and builder-rules carry a POINTER to the role file (F6-33, t-1206: one owner per aspect) and no copy of the
rule.

The keys K1, K2 are quoted VERBATIM from spec t-744 section 3.3 ("the file at `handoff:`", "at most 25 lines"; replaced by the 2,000-character cap, spec fg-context-and-hygiene B1); K3 is the
pointer of builder-rules rule 11 (t-1206 section 2 E1d), K4 from t-744 section 6 ("(d) Hand-back carrier"); the line definition (F-7 B, `ceil(len/200)`) from section L; the
fallback ("never lost, never shortened") from section 3.3. The scout keys are the F-1 B sentence of section L.
Run from the repo root: python -m pytest tools/test_handoff_rule_anchors.py -q
A tree elsewhere (the negative control of the witness): HANDOFF_ANCHORS_ROOT=<copy of the files, same relative paths>.
"""
import os
import pathlib
import re

import pytest

REAL = pathlib.Path(__file__).resolve().parent.parent
ROOT = pathlib.Path(os.environ.get("HANDOFF_ANCHORS_ROOT") or REAL)

K1 = "the file at `handoff:`"
K2 = "at most 2,000 characters"
K3 = "правило 7 `.claude/agents/builder.md`"
K4 = "(d) Hand-back carrier"
K_LINE = "ceil(len/200)"
K_BRIEF = "`.claude/agents/critic.md` rules 16-17"
RESTATED = [K2, K_LINE, "не длиннее 25 строк", "2 000 символов", "2000 символов"]
K_FALLBACK = "never lost, never shortened"
K_SCOUT = ("`tools/handback_extract.py`", "`docs/tasks/specs/reports/`")

CRITIC = ".claude/agents/critic.md"
BUILDER = ".claude/agents/builder.md"
SCOUT = ".claude/agents/scout.md"
DESIGNER = ".claude/agents/designer.md"
JUDGE = ".claude/agents/judge.md"
BRIEF = "docs/tasks/critic-diff-brief.md"
RULES = "plans/builder-rules.md"
PROTOCOL = "PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md"

# role file -> number of the rule that carries the report (check 28 (a) anchors keep their numbers)
ANCHOR_RULE = {CRITIC: 16, BUILDER: 7, DESIGNER: 5}
FILE_RULE_KEYS = [K1, K2, K_LINE, K_FALLBACK]


def squash(text):
    """Whitespace collapsed to single spaces: a key broken over two lines of a wrapped rule is still the key."""
    return " ".join(text.split())


def missing_keys(text, keys):
    """The keys that do not occur in `text` (whitespace-insensitive); [] when all are present."""
    flat = squash(text)
    return [k for k in keys if squash(k) not in flat]


def restated(text):
    """The RESTATED keys (the hand-back rule's own words) found in a pointer copy; [] when it only points."""
    return [k for k in RESTATED if squash(k) in squash(text)]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def rule_block(text, number):
    """The text of numbered rule `number` of a role file (from its `N. ` line to the next `M. ` rule line); None when absent."""
    starts = [(int(m.group(1)), m.start()) for m in re.finditer(r"^(\d+)\. ", text, re.M)]
    for i, (n, pos) in enumerate(starts):
        if n == number:
            end = starts[i + 1][1] if i + 1 < len(starts) else len(text)
            return text[pos:end]
    return None


@pytest.mark.parametrize("rel", sorted(ANCHOR_RULE))
def test_role_rule_carries_file_rule(rel):
    block = rule_block(read(rel), ANCHOR_RULE[rel])
    assert block is not None, "%s has no rule %d" % (rel, ANCHOR_RULE[rel])
    assert missing_keys(block, FILE_RULE_KEYS) == [], "%s rule %d lacks %s" % (
        rel, ANCHOR_RULE[rel], missing_keys(block, FILE_RULE_KEYS))


@pytest.mark.parametrize("rel", sorted(ANCHOR_RULE))
def test_role_rule_has_the_world_before_the_hook(rel):
    """E-1/E-2: no `handoff:` path or a refused Write -> the full report in chat."""
    block = squash(rule_block(read(rel), ANCHOR_RULE[rel]))
    assert "names no such path" in block and "the Write is refused" in block


def test_critic_rule_17_puts_the_block_in_the_file():
    block = squash(rule_block(read(CRITIC), 17))
    assert "critic_verdict_check.py" in block and "`handoff:`" in block


def test_critic_rule_17_not_renumbered():
    """Rule 18 (duplication / code quality) keeps its number; rules 16 and 17 are in place."""
    text = read(CRITIC)
    for n in (16, 17, 18):
        assert rule_block(text, n) is not None


def test_brief_what_comes_back():
    """F6-33: the brief POINTS to critic.md rules 16-17 and carries no copy of the hand-back rule."""
    text = read(BRIEF)
    assert missing_keys(text, ["`handoff:`", K_BRIEF, "critic_verdict_check.py"]) == []
    assert restated(text) == []


def test_builder_rules_p11():
    """F6-33: rule 11 points to builder.md rule 7 for the form and keeps only the report's content."""
    block = rule_block(read(RULES), 11)
    assert block is not None
    assert missing_keys(block, [K3, "`handoff:`"]) == []
    assert restated(block) == []


def test_calibration_check_28_has_d():
    text = read(PROTOCOL)
    assert missing_keys(text, [K4]) == []
    assert text.index("28. **Completeness of hand-backs: the report file and the short digest.**") < text.index(K4) < text.index("29. **Upgrade delivery")


def test_scout_has_the_extraction_sentence_and_no_file_rule():
    """F-1 B: scout has no Write and no 25-line rule; it says its final message is the report and the Lead extracts it."""
    text = read(SCOUT)
    assert missing_keys(text, list(K_SCOUT)) == []
    assert "25 lines" not in text and "Write" not in text.split("---", 2)[1]
    assert K2 not in squash(text)


def test_judge_untouched_by_the_rule():
    """E-25: judge.md keeps its pinned reply shape - none of the file-rule keys."""
    text = read(JUDGE)
    assert [k for k in (K1, K2, K_LINE) if squash(k) in squash(text)] == []


def test_negative_control_missing_keys_reports():
    assert missing_keys("no keys here", [K1]) == [K1]


def test_negative_control_one_key_absent_from_a_copy():
    """One key removed from a temp copy of a real rule -> the check reports exactly that key (a check that cannot fail is not a check)."""
    block = rule_block(read(CRITIC), ANCHOR_RULE[CRITIC])
    assert missing_keys(block, FILE_RULE_KEYS) == []
    copy = squash(block).replace(K2, "a few lines")
    assert missing_keys(copy, FILE_RULE_KEYS) == [K2]


K_SCOUT_FORM = ("digest: v1", "docs/tasks/exchange-form.md")


def test_scout_rule_10_teaches_the_digest_form_v1():
    """F5-2 N1 (t-797 section 6): scout.md rule 10 carries the key line of the form and the note that holds its grammar; the
    old pins (the extraction sentence, no Write, no 25-line rule) are the test above and stay."""
    block = rule_block(read(SCOUT), 10)
    assert block is not None, "scout.md has no rule 10"
    assert missing_keys(block, list(K_SCOUT_FORM)) == []
    assert "25 lines" not in squash(block) and K2 not in squash(block)


def test_negative_control_scout_form_key_absent_from_a_copy():
    block = rule_block(read(SCOUT), 10)
    copy = squash(block).replace(K_SCOUT_FORM[0], "digest form")
    assert missing_keys(copy, list(K_SCOUT_FORM)) == [K_SCOUT_FORM[0]]


def test_negative_control_restatement_in_a_pointer_copy():
    """The old brief paragraph pasted back into a copy of the brief -> restated() names the keys (a check that cannot fail is not a check)."""
    copy = read(BRIEF) + "\nanswer in chat with at most 2,000 characters; a line over 200 characters counts as ceil(len/200)\n"
    assert restated(copy) == [K2, K_LINE]
