#!/usr/bin/env python3
"""t-1685 N1 (and N2, appended after N1 is merged): the words a role reads before the work (AR-10, FR-38).

DOC-DISPATCH WITNESS: the keys K1-n are quoted VERBATIM from spec t-1685 section 2 (N1-1..N1-6) as written BEFORE the work, F5 (b)
adapted: the norms are put to the person in ONE confirmation question. Each key is a phrase that stands in the named file in raw
bytes. The negative control reports a key that is not there; a second control proves the check can fail on a changed text.

N2 appends K2-1..K2-3 (the strategist charter: rule 1c, the branch clause).

Mutations -> killing key (this file): rule 1c dropped -> K2-1; the branch clause dropped -> K2-3; the payer text restored -> K2/absent; the scout's "That is the whole job" stop rule back -> K1-1/absent; the tester's "One question
per class." back -> K1-6/absent; `query` dropped from phase s0 -> K1-7.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_eq  # noqa: E402

KEYS = {
    "agents/qa-scout.md": [
        "where they SEE its result, where they CHANGE or UNDO it",                      # K1-1
        "never only a name inside a note",                                              # K1-2
        "then follow the data: who reads and who changes what the function writes",     # K1-3
        "A tool that did not read a source does not end it",                            # K1-4
    ],
    "agents/qa-requirements-tester.md": [
        "IS a requirement: the norm is its oracle",                                     # K1-5
        "one record per fork, never one for a class",                                   # K1-6 (X1 charter wording; the template keeps the old one below)
        # spec t-1765 X1 (B-D): K1-9 and the four norms-question keys (F5 b, t-1692 B1-B3) moved to the register template, whose keys
        # below already hold them
    ],
    "references/templates/requirements-register.md": [
        "never a reading `from: code` that drops the norm",                             # t-1692 B2
        "the norms hold (default), or one does not apply (`from: person`)",             # t-1692 B2
        "`invariant:`/`bug:candidate-defect`: a missing item cannot be added",          # t-1692 B3 (the template lists the failed-call norm too)
        "departs from it is an expected red, `contradicts`, no question of its own",    # t-1692 B1
        "IS a requirement: the norm is its oracle",                                     # K1-5
        "one `open_questions` row per fork, never one for a class",                     # K1-6
        "unknown: <why>",                                                               # K1-9
        "ONE confirmation question",                                                    # F5 (b)
        "none derived, no such question",                                               # F5 (b) edge: an empty list asks nothing
    ],
    "skills/qa-story/phases/s0.md": ["a page, filter or search: `query`"],              # K1-7
    "skills/qa-story/phases/s1.md": ["are not accept-gap: assess it relevant"],         # K1-8
    # N2 (t-1685), keys quoted from spec section 2 N2-3 and 6.2 as written BEFORE the work
    "agents/qa-test-strategist.md": [
        "gets a row that WALKS it",                                                     # K2-1
        "records every oddity on the way",                                              # K2-2
        "A one-off check of the new behaviour that will not join the regression needs no automated test",   # K2-4 (P28, X5-0)
        "`work/blast-radius.json` is evidence (importers, same-name callers, nearby tests, `unmeasured`), not the radius",   # X5-1 (P27)
        "name what the index could not see (dynamic calls, routes, UI to API, non-Python)",                                  # X5-1 (P27)
        # spec t-1765 X1 (B-D, "moved" -> the strategist's ahead card): K2-3 stands on the card as its sentence about a letter branch
        # (the closest one; the verbatim "each letter's patch passes the plan contract as if that answer" has no carrier any more).
        # The S3 side of F5 (b): the charter sentence is back (t-1765 X1 fix-5, critic t-1816 F5)
        "A norm row does not wait on the norms-list question: it is planned with the norm as the oracle",   # F5 (b), S3 side
    ],
    "references/ahead-cards.json": ["A letter branch whose answer settles the oracle sets `oracle_unknown: false`"],      # K2-3 (card)
}
ABSENT = {
    "agents/qa-scout.md": ["That is the whole job", "keyword-search the requirement text across the test"],
    "agents/qa-requirements-tester.md": ["One question per class.", "ONE question for the whole class"],
    "references/templates/requirements-register.md": ["ONE question for the whole class"],
}


def read(rel: str) -> str:
    return (harness.PLUGIN_ROOT / rel).read_bytes().decode("utf-8")


def missing(table: dict, reader=read) -> list:
    return [f"{rel}: {key}" for rel, keys in table.items() for key in keys if key not in reader(rel)]


def present(table: dict, reader=read) -> list:
    return [f"{rel}: {key}" for rel, keys in table.items() for key in keys if key in reader(rel)]


def main() -> None:
    check_eq("K1: every key stands in its file", missing(KEYS), [])
    check_eq("K1: the old stop rule and the old class-question rule are gone", present(ABSENT), [])
    check("K1 negative control: a key that is not there is reported", missing({"agents/qa-scout.md": ["a-key-that-is-nowhere"]}) != [])
    check("K1 negative control: a changed text loses its key",
          missing(KEYS, lambda rel: read(rel).replace("then follow the data", "then look around")) != [])
    check("K1 negative control: a restored old rule is reported as present",
          present(ABSENT, lambda rel: read(rel) + "\nThat is the whole job. One question per class. ONE question for the whole class\n") != [])
    harness.finish("test_detection_role_texts")


if __name__ == "__main__":
    main()
