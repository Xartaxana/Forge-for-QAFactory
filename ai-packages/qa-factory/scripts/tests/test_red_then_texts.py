"""test_red_then_texts.py - the texts of nodes R1 and R3 of t-1508 (a red Then does not block the others, release 0.10.5).

Why. On TP1-12586 the person asked to check Thens 3 and 4 of TC-003, which a red Then 2 had stopped. The analyst's rule 2c
sent "an independent one" back to the author (`rework` = S5), and the conductor had no text for the question at all. The
owner's words (28.10.2026): independent Thens are moved above the red and dependent ones are recorded as `blocked_by_check`;
the analyst's old 2c "is not right" (who moves the independent Thens when a first Then suddenly turns red?); never comment a
red-by-bug Then out when moving it is possible (FA-10).

This is the doc-dispatch witness (CLAUDE.md rule 11): the keys are quoted VERBATIM from docs/tasks/specs/t-1508-red-then-chain.md
sections 5.1 (K-R1-1 .. K-R1-7) and 5.3 (K-R3-1 .. K-R3-8) as written BEFORE the texts; the script is committed and carries its
own NEGATIVE controls (a copy without a key, a copy with the old 2c put back, a copy with "comment out" next to "Then", a
PRESENT key that is in no file - all through `problems_of`). K-R3-6 (the analyst's brief names `red_sandbox.py --diagnostic`)
lives in test_brief_pack_roles.py, next to the card pins.

Whitespace is folded (the texts wrap near column 125); the words, the punctuation and the backticks are verbatim.

Runnable on its own: `python -B scripts/tests/test_red_then_texts.py`.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import PLUGIN_ROOT, check, finish  # noqa: E402

ANALYST = "agents/qa-failure-analyst.md"
S7 = "skills/qa-story/phases/s7.md"
CONDUCTOR = "references/conductor.md"
FILES = (ANALYST, S7, CONDUCTOR)

# (id, file, key) - PRESENT, verbatim from the spec.
PRESENT = (
    ("K-R1-1a", S7, "read first: the case's triage row"),
    ("K-R1-1b", S7, "Self-probe notes"),
    ("K-R1-2", S7, "never `rework --stage S5`"),
    ("K-R1-3", S7, "always takes `--words-file`, never `--reason`"),
    ("K-R1-4", CONDUCTOR, "never `rework --stage S5`"),
    ("K-R1-6", S7, "the report writer run again, and gate B is asked again"),
    ("K-R1-7", CONDUCTOR, "say so first"),
    ("K-R3-1", ANALYST, "list it under the row's `blocked_thens`"),
    ("K-R3-2", ANALYST, "the blocker's draft lists this case in its `cases`"),
    ("K-R3-3", ANALYST, "the test in the repository is never changed"),
    ("K-R3-4", ANALYST, "and the `reorder` of rule 2c"),
    ("K-R3-7", ANALYST, "write `diagnostic.thens` from the run's `failure_line`"),
    ("K-R3-8", ANALYST, "a code critic reviews that one test"),
    # Rule 7 (draft) and the 2d reconciliation of the spec's "Edges".
    ("R3-rule7", ANALYST, "A draft lists in `cases` every case whose row names it through `blocking_check`."),
    ("R3-2d", ANALYST, "not a control experiment, it never changes the red's verdict"),
)

# (id, file, key) - ABSENT: the old 2c sentence.
ABSENT = (
    ("K-R3-5", ANALYST, "its repair goes to the author (`rework`)"),
)

# K-R1-5: "comment out" next to "Then" (either order, within a short window) in none of the texts (FA-10).
COMMENT_OUT = re.compile(r"comment(?:ed|ing)?\s+out.{0,60}\bThen|\bThen.{0,60}comment(?:ed|ing)?\s+out", re.I)


def fold(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def read_texts() -> dict:
    return {name: (PLUGIN_ROOT / name).read_text(encoding="utf-8") for name in FILES}


def problems_of(texts: dict, extra_present: tuple = ()) -> list:
    """Every key that is wrong in `texts` ({file: text}); [] when the texts are right."""
    problems = []
    folded = {name: fold(text) for name, text in texts.items()}
    for item, name, key in PRESENT + tuple(extra_present):
        if fold(key) not in folded[name]:
            problems.append(f"{item}: {name} lacks {key!r}")
    for item, name, key in ABSENT:
        if fold(key) in folded[name]:
            problems.append(f"{item}: {name} still carries {key!r}")
    for name, text in folded.items():
        found = COMMENT_OUT.search(text)
        if found:
            problems.append(f"K-R1-5: {name} advises to comment a Then out: {found.group(0)!r}")
    return problems


def the_keys_hold_in_the_shipped_texts() -> None:
    found = problems_of(read_texts())
    for line in found:
        print("  PROBLEM:", line)
    check(f"every key holds in the shipped texts ({len(PRESENT)} PRESENT, {len(ABSENT)} ABSENT, K-R1-5 absent)", found == [])


def the_checker_reports_what_it_should() -> None:
    """The negative controls: a checker that cannot fail is indistinguishable from a broken one."""
    texts = read_texts()

    old_2c = dict(texts, **{ANALYST: texts[ANALYST] + "\nName an independent one in the triage note; its repair goes to the author (`rework`).\n"})
    check("analyst with the old 2c sentence put back: K-R3-5 reported",
          any(p.startswith("K-R3-5") for p in problems_of(old_2c)))
    print("negative control: analyst with the old 2c re-inserted -> K-R3-5 reported")

    for item, name, key in (("K-R1-2", S7, "never `rework --stage S5`"), ("K-R1-4", CONDUCTOR, "never `rework --stage S5`"),
                            ("K-R1-6", S7, "the report writer run again, and gate B is asked again")):
        # the mutant: the key taken out of its file (the spec's three mutants of 5.1)
        mutant = dict(texts, **{name: fold(texts[name]).replace(fold(key), "")})
        check(f"{name} without {item}: reported", any(p.startswith(item) for p in problems_of(mutant)))
        print(f"negative control: {name} with {item} removed -> reported")

    for item, name, key in (("K-R3-1", ANALYST, "list it under the row's `blocked_thens`"),
                            ("K-R3-2", ANALYST, "the blocker's draft lists this case in its `cases`"),
                            ("K-R3-8", ANALYST, "a code critic reviews that one test")):
        mutant = dict(texts, **{name: fold(texts[name]).replace(fold(key), "")})
        check(f"{name} without {item}: reported", any(p.startswith(item) for p in problems_of(mutant)))
        print(f"negative control: {name} with {item} removed -> reported")

    for name in (S7, CONDUCTOR):
        bad = dict(texts, **{name: texts[name] + "\nIf a Then is red, comment out the Then and go on.\n"})
        check(f"{name} with 'comment out' next to 'Then': K-R1-5 reported", any(p.startswith("K-R1-5") for p in problems_of(bad)))
    check("the plain word 'comment' (a Jira comment) next to 'Then' is not reported",
          not any(p.startswith("K-R1-5") for p in problems_of(dict(texts, **{S7: texts[S7] + "\nRead the Jira comment, then go on.\n"}))))
    print("negative control: 'comment out' next to 'Then' -> reported; a plain 'comment' -> not")

    zzz = ("zzz", ANALYST, "zzz-not-in-any-file")
    check("a PRESENT key that is in no file: reported by problems_of",
          any(p.startswith("zzz:") for p in problems_of(texts, extra_present=(zzz,))))
    print("negative control: 'zzz-not-in-any-file' as a PRESENT key -> reported")


if __name__ == "__main__":
    the_keys_hold_in_the_shipped_texts()
    the_checker_reports_what_it_should()
    finish("Red-Then chain texts (t-1508 R1/R3)")
