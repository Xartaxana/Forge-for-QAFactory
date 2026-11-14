#!/usr/bin/env python3
"""Scenario `dry-1`: the dry story. The REAL driver runs a synthetic story S0..S9 in a world of its own, the roles and the conductor are
`dry_stub.py` (P1-b, node N3; spec docs/tasks/specs/20261113-p1b-dry-story-spec.md section 4, card N3).

    python -B scripts/tests/test_scenario_dry_1.py                 the census of the exits (dry_exits) and the main pass of the type `default`
    python -B scripts/tests/test_scenario_dry_1.py --part main     the main pass only
    python -B scripts/tests/test_scenario_dry_1.py --part main:<type>   the main pass of another type (a type the table does not hold is red)

A stop before S9 is legal only at a row of `fixtures/driver-exits/known_red.json` named `main/S<n>` with a finding id; every other stop is red.
The stages after a ledgered stop are printed `after:<finding>`. Rows of the walk that start at a snapshot the pass did not make wait the same way.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dry_exits  # noqa: E402
import dry_world  # noqa: E402
import harness  # noqa: E402

OWNED = ("scenario_walk.py", "test_scenario_dry_1.py", "dry_world.py")
# The text this file greps for is built in two pieces: the pattern must not find itself.
UNREQUIRED = '"required": ' + "False"


def census() -> None:
    report = dry_exits.check()
    for line in report.numbers:
        print(f"NUMBER {line}")
    for line in report.notes:
        print(f"NOTE {line}")
    harness.check("dry-1/census", not report.problems, "\n".join(report.problems))


def forms_required() -> None:
    """Spec N3 item 2: no world of this layer relaxes the handover forms. The grep has a positive control of the same shape."""
    pattern = re.compile(re.escape(UNREQUIRED))
    harness.check("dry-1/world/forms-required: positive control of the grep", bool(pattern.search(f"x = {{{UNREQUIRED}}}")), "the pattern finds no sample")
    found = [name for name in OWNED if pattern.search((Path(__file__).resolve().parent / name).read_text(encoding="utf-8"))]
    harness.check("dry-1/world/forms-required: no owned file relaxes `handoffs.required`", not found, f"found in {found}")


def parse_part(text: str) -> str:
    """The type of `--part main[:<type>]` (absent type: `default`); a part that is not `main...` exits 2 naming the known parts."""
    name, _, label = text.partition(":")
    if name != "main":
        print(f"unknown part {text!r}; expected main or main:<type> (the walk rows are written by node N4)", file=sys.stderr)
        raise SystemExit(2)
    return label or "default"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--part", help="main or main:<type>; without it: the census, then the main pass of the type `default`")
    args = parser.parse_args(argv)
    label = parse_part(args.part) if args.part else "default"
    if not args.part:
        census()
        forms_required()
    if label != "default":
        harness.check(f"dry-1/main:{label}/type", False, f"unknown type {label!r}; expected default (the table of types is written by node N3t)")
        harness.finish("scenario dry-1")
    for result in dry_world.main_pass(dry_world.DEFAULT_STORY, label):
        if result.kind == "note":
            print(f"NOTE {result.name}: {result.detail}")
        else:
            harness.check(result.name, result.kind == "pass", result.detail)
    harness.finish("scenario dry-1")
    return 0


if __name__ == "__main__":
    main()
