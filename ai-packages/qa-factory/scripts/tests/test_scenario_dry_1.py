#!/usr/bin/env python3
"""Scenario `dry-1`: the dry story. The REAL driver runs a synthetic story S0..S9 in a world of its own, the roles and the conductor are
`dry_stub.py` (P1-b, node N3; spec docs/tasks/specs/20261113-p1b-dry-story-spec.md section 4, card N3).

    python -B scripts/tests/test_scenario_dry_1.py                 the census of the exits (dry_exits) and the main pass of the type `default`
    python -B scripts/tests/test_scenario_dry_1.py --part main     the main pass only
    python -B scripts/tests/test_scenario_dry_1.py --part main:<type>   the main pass of another type (a type the table does not hold is red)
    python -B scripts/tests/test_scenario_dry_1.py --part exits:<group> [--exits-root R] [--ledger L]   the walk rows of one group (node N4w)

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


GROUP_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
DEFAULT_ROOT = dry_exits.WALK_DIR.parent        # fixtures/stories/dry-1: its `exits/` and `seeds/` hold the walk files and the recipes of the groups


def groups_found(exits_root) -> list:
    """The group names of `<exits-root>/exits/*.json` and of the census files `driver-exits/*.json` (the ONE listing, for the refusal text)."""
    found = {p.stem for p in (Path(exits_root) / "exits").glob("*.json")} | {p.stem for p in dry_exits.EXITS_DIR.glob("*.json") if p.name not in dry_exits.NOT_GROUP}
    return sorted(found)


def parse_part(text: str, exits_root=None) -> tuple:
    """`(kind, label)` of `--part`: `main` / `main:<type>` -> ("main", type or `default`); `exits:<group>` -> ("exits", group), the group a non-empty
    `[a-z0-9-]` name that some `exits/<group>.json` or `driver-exits/<group>.json` holds (EW6: a typo never runs another group). Any other text, an empty
    or malformed group, or a group nobody holds: exit 2 naming the known parts and the groups found."""
    root = Path(exits_root or DEFAULT_ROOT)
    name, _, label = text.partition(":")
    if name == "main":
        return "main", label or "default"
    known = f"expected main, main:<type> or exits:<group> (groups found: {', '.join(groups_found(root)) or 'none'})"
    if name != "exits" or not GROUP_RE.match(label):
        print(f"unknown part {text!r}; {known}", file=sys.stderr)
        raise SystemExit(2)
    if label not in groups_found(root):
        print(f"unknown group {label!r}: neither {root / 'exits' / (label + '.json')} nor driver-exits/{label}.json exists; {known}", file=sys.stderr)
        raise SystemExit(2)
    return "exits", label


def emit(result) -> None:
    if result.kind == "note":
        print(f"NOTE {result.name}: {result.detail}")
    else:
        harness.check(result.name, result.kind == "pass", result.detail)


def exits_part(group: str, exits_root, ledger) -> None:
    """`--part exits:<group>` (node N4w): the rows of `<exits-root>/exits/<group>.json` and nothing else (I6). Everything is refused BEFORE a world is
    built: an absent file (EW1/EW7: red, with the census size of the group), an unreadable one, a row outside the grammar, an absent seed recipe. Then
    `dry_world.walk_exits`, `dry_exits.judge_group` against `ledger` filtered to the group's ids, and the group's `unwalked` NOTE."""
    import scenario_walk
    exits_root, tag = Path(exits_root), f"{dry_world.DEFAULT_STORY}/exits:{group}"
    path, universe = exits_root / "exits" / f"{group}.json", dry_exits.Universe.real()
    try:
        census = dry_exits.load(dry_exits.EXITS_DIR)
    except dry_exits.ExitsUnreadable as exc:
        census = None
        print(f"NOTE {tag}/census: {' '.join(str(exc).split())[:300]}")

    def unwalked(rows) -> None:
        count, texts = dry_exits.group_unwalked(group, census, rows, universe.prices, routes=universe.routes)
        for text in texts:
            print(f"NOTE {tag}/unwalked: {text}")

    if not path.is_file():
        harness.check(f"{tag}/rows", False, f"{path} is absent; expected the walk rows of group {group} (node N4:{group} writes them)")
        unwalked([])
        harness.finish("scenario dry-1")
    story_dir = dry_world.STORIES / dry_world.DEFAULT_STORY
    try:
        recipes = dry_exits.load_seeds(exits_root / "seeds" / f"{group}.json")
        classer = (lambda section, name: dry_exits.subject_class(section, name, census, universe)) if census else None
        rows = dry_exits.load_group_file(path, strict=True, universe=universe, seeds=recipes, class_of_subject=classer, story_dir=story_dir)
    except dry_exits.ExitsUnreadable as exc:
        harness.check(f"{tag}/rows", False, str(exc))
        harness.finish("scenario dry-1")
    if universe.errors:
        harness.check(f"{tag}/universe", False, "; ".join(universe.errors))
        harness.finish("scenario dry-1")
    line = lambda name, kind, detail="": emit(scenario_walk.Result(name, kind, detail))      # noqa: E731
    try:
        outcomes = dry_world.walk_exits(dry_world.DEFAULT_STORY, rows, recipes, ledger, line, exits_label=f"exits:{group}", story_dir=story_dir, universe=universe,
                                        classer=classer)
    except (scenario_walk.StoryError, dry_world.TypesError) as exc:
        harness.check(f"{tag}/load", False, str(exc))
        harness.finish("scenario dry-1")
    for name, kind, detail in dry_exits.judge_group(outcomes, ledger, [row["id"] for row in rows]):
        line(f"{tag}/{name}", kind, detail)
    unwalked(rows)
    harness.finish("scenario dry-1")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--part", help="main, main:<type> or exits:<group>; without it: the census, then the main pass of the type `default`")
    parser.add_argument("--exits-root", help="with exits:<group> only: the folder holding exits/ and seeds/ (default fixtures/stories/dry-1)")
    parser.add_argument("--ledger", help="with exits:<group> only: the label ledger (default fixtures/driver-exits/known_red.json)")
    args = parser.parse_args(argv)
    kind, label = parse_part(args.part, args.exits_root) if args.part else ("main", "default")
    for option in ("exits_root", "ledger"):
        if getattr(args, option) is not None and kind != "exits":
            print(f"--{option.replace('_', '-')} is legal only with --part exits:<group>", file=sys.stderr)
            raise SystemExit(2)
    if kind == "exits":
        exits_part(label, args.exits_root or DEFAULT_ROOT, args.ledger or dry_exits.EXITS_DIR / "known_red.json")
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
