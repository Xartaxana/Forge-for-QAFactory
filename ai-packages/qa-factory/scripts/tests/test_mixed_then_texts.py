"""test_mixed_then_texts.py - the role texts of HF2-3 part 3d (mixed Then outcomes in one case), key presence.

The keys are the phrases the spec t-085 section 3.6 named BEFORE the run (doc-witness property i); each must
stand VERBATIM (raw text, no whitespace folding) in the file the spec names. A key an older line already says is
extended there, never said twice, so presence in the named file is the whole check. Three things beyond presence:

  * the generated slices that carry the automation contract to the automator and the code critic hold the K5
    phrase (a hand-edited or stale slice is `contract_slices.py --check`, not this test);
  * the SAFE SIDE of FA-10: dimension 8 names the sanctioned path by the reasons of `THEN_REMAINDER_REASONS`
    only, never `contradicts_requirement` (a red by a product bug is not commented out by this text);
  * the owner's word. The sub-keys K2a, K2b and K3a exist only once the owner answers FA-10 / FA-11. One
    constant, OWNER_WORD_FA, holds the date of that word: while it is empty the three phrases must be ABSENT
    from the package (nobody may write an interpretation of the owner's word for him, rule 11a); once it holds a
    date they must be PRESENT. K2a and K2b are the two answers of ONE question: whoever sets the date keeps in
    KEYS_AFTER_OWNER_WORD only the sub-keys that answer enabled.

A NEGATIVE control proves the helper can fail (doc-witness property iii): a key that is in no file is reported
absent by the same helper, and as a key it makes the check red.

Runnable on its own: `python -B scripts/tests/test_mixed_then_texts.py`.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness import PLUGIN_ROOT, check, finish  # noqa: E402

# The date of the owner's word on FA-10 / FA-11 ("YYYY-MM-DD"). EMPTY until the owner speaks: the spec t-085
# section 11 records no word, so K2a, K2b and K3a are not written and are checked ABSENT.
OWNER_WORD_FA = ""

RUBRIC = "references/code-review-rubric.md"
AUTOMATOR = "agents/qa-automator.md"
CRITIC = "agents/qa-code-critic.md"
CONTRACT = "references/artifact-contract-automation.md"  # K5 moved here from artifact-contract.md (integration, 3d divergence 1)
DESIGNER = "agents/qa-case-designer.md"
ANALYST = "agents/qa-failure-analyst.md"

KEYS = [
    ("K1a", RUBRIC, "an independent Then placed after a failing assert"),
    ("K1b", RUBRIC, "no commented-out checks outside the dimension-8 sanctioned path"),
    ("K2", RUBRIC, "a commented-out Then with its reason, its `then_bindings` row with reason `handed_to_person` "
                   "or `blocked_by_check`, and its Left with you line"),
    ("K3a", AUTOMATOR, "move independent Thens before the red one"),
    ("K3b", AUTOMATOR, "record a Then the red stops as `blocked_by_check`, and send these rows through "
                       "`manifest_put.py --fragment` after your last `manifest_from_tests.py` run"),
    ("K3-ref", AUTOMATOR, "rubric dimension 8"),
    ("K4", CRITIC, "an independent Then behind a red"),
    ("K5a", CONTRACT, "reason: blocked_by_check, blocking_check, detail}"),
    ("K5b", CONTRACT, "blocking_check"),
    ("K5c", CONTRACT, "`thens: [n]`"),
    ("K5d", CONTRACT, "`retracted_unresolved`"),
    ("K5e", CONTRACT, "a re-sent `contradicts_requirement` row replaces its slice, and its `thens` separately"),
    ("K5-ref", CONTRACT, "rubric dimension 8"),
    ("K6", DESIGNER, "A Then that only makes sense after another case's check says which case"),    # X1 charter: sentence-initial capital
    ("K7", ANALYST, "a red that stops other Thens is triaged once; the Thens it blocks are not failures"),
]
SLICES_WITH_K5 = [
    "references/slices/qa-automator/artifact-contract-automation.md",
    "references/slices/qa-code-critic/artifact-contract-automation.md",
]
K5_PHRASE = "a re-sent `contradicts_requirement` row replaces its slice, and its `thens` separately"

# The sub-keys of the owner's word (spec 3.6: K2a at FA-10 (a), K2b at FA-10 (b), K3a at FA-11 (a)).
KEYS_AFTER_OWNER_WORD = [
    ("K2a", RUBRIC, "a Then red by a product bug is not commented out: it stays red and goes last"),
    ("K2b", RUBRIC, "a Then red by a product bug is commented out only after its red run is recorded and with its "
                    "`contradicts_requirement` row"),
    ("K3a-sub", AUTOMATOR, "pin each Then's lines (`then={n: \"a-b\"}`) in a test that checks several cases"),
]


def read(rel: str) -> str:
    return (PLUGIN_ROOT / rel).read_text(encoding="utf-8")


def key_present(rel: str, key: str) -> bool:
    """True when `key` stands verbatim in the package file `rel`; prints one line saying which."""
    found = key in read(rel)
    print(f"  key {'present' if found else 'ABSENT '} in {rel}: {key!r}")
    return found


def dimension(text: str, number: int) -> str:
    """The numbered dimension of the rubric: from `N. **` to the next numbered item (or the next heading)."""
    found = re.search(rf"^{number}\. \*\*.*?(?=^\d+\. \*\*|^## )", text, re.S | re.M)
    return found.group(0) if found else ""


def main() -> None:
    for item, rel, key in KEYS:
        check(f"{item}: {key!r} stands in {rel}", key_present(rel, key))

    for rel in SLICES_WITH_K5:
        check(f"K5: the phrase reached the generated slice {rel}", key_present(rel, K5_PHRASE))

    # The safe side of FA-10: the sanctioned path names the reasons of THEN_REMAINDER_REASONS and nothing else.
    dim8 = dimension(read(RUBRIC), 8)
    check("K2 safe side: dimension 8 was found in the rubric", "Masking" in dim8, repr(dim8[:60]))
    check("K2 safe side: dimension 8 does not name `contradicts_requirement` (FA-10 has no owner's word)",
          "contradicts_requirement" not in dim8)
    check("K2 safe side: dimension 8 names both reasons of THEN_REMAINDER_REASONS",
          "`handed_to_person`" in dim8 and "`blocked_by_check`" in dim8)

    # The owner's word: absent while the flag is empty, present once it holds a date.
    enabled = bool(OWNER_WORD_FA.strip())
    print(f"  OWNER_WORD_FA = {OWNER_WORD_FA!r}: sub-keys K2a/K2b/K3a are checked "
          f"{'PRESENT' if enabled else 'ABSENT'}")
    for item, rel, key in KEYS_AFTER_OWNER_WORD:
        found = key_present(rel, key)
        if enabled:
            check(f"{item}: the owner spoke ({OWNER_WORD_FA}), so {key!r} stands in {rel}", found)
        else:
            check(f"{item}: no owner's word on FA-10 / FA-11, so {key!r} is ABSENT from {rel}", not found)

    # NEGATIVE control (doc-witness property iii): the same helper must report a key that is in no file as absent.
    check("negative control: 'zzz-not-in-any-file' is reported ABSENT by the same helper",
          not key_present(RUBRIC, "zzz-not-in-any-file"))

    finish("mixed Then texts HF2-3d (key presence + safe side + owner-word flag + negative control)")


if __name__ == "__main__":
    main()
