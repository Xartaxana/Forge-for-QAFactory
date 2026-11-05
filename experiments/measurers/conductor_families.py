"""Where a driver run's conductor money went, and what the driver's own table would have caught.

Answers three questions over one run's `state/conductor.jsonl`:
  1. how many conductor sessions there were, what they cost, and how many ran no command at all;
  2. which refusal families they were raised for, with the exact sessions/cost/turns per family;
  3. how many of them `story_run.KNOWN_REFUSALS` would have matched — i.e. how many never needed a
     model at all.

Written for a late run of the reference story, where it showed 76 sessions, $29.68, a table that
would have matched 8, and four families holding 43 sessions and $14.61 — 49% of the conductor's
money. Re-run it after every driver run: each family with a mechanical answer becomes one row of
KNOWN_REFUSALS.

    python experiments/measurers/conductor_families.py [--run <run>] [--ticket <TICKET>]

`--run` defaults to default_right of the runs table; without a table it is required.

`test_measurers.py` covers it, including that exact trap: the first version of the family table
under-counted threefold because it grouped distinct FIRST LINES instead of sessions, and a
mutation putting that back turns the test red. Still read a couple of the grouped refusals before
trusting a number from it — a test proves the arithmetic, not the reading (FR-26).
"""
import argparse
import collections
import json
import pathlib
import re
import sys

import paths

BASE = paths.BASE
RUNS = dict(paths.BASELINES)        # the runs table's baselines ({} without a table); other names go by copy_folder
PLUGIN_SCRIPTS = paths.SCRIPTS

# A family is the refusal's own opening clause, not a word anywhere in it: the same refusal text
# repeated is one family, and a family is what a table row would cover.
FAMILIES = [
    ("driver has no move", r"the driver has no move for `(\w+)`"),
    ("window not receipted", r"window is not receipt"),
    ("exit gate: REAL exit 1", r"REAL exit 1"),
    ("structured test plan invalid", r"structured test plan invalid"),
    ("stage_done before a gate", r"stands in front of gate"),
    ("S5 window acceptance record", r"window acceptance record"),
    ("resolve_return packet", r"^resolve_return:"),
    ("handover form", r"handoff|handover"),
    ("manifest", r"manifest"),
    ("witness", r"witness"),
    ("delivery step", r"^delivery"),
    ("the person's answer, routed", r"The person answered"),
]


def family(text: str) -> str:
    flat = re.sub(r"\s+", " ", (text or "").strip())
    for name, pattern in FAMILIES:
        m = re.search(pattern, flat, re.I)
        if m:
            return f"{name}: {m.group(1)}" if m.groups() else name
    return (flat[:58] or "(empty refusal)")


def known_match(text: str):
    """(name, action) from the driver's own table, or (None, None)."""
    sys.path.insert(0, str(PLUGIN_SCRIPTS))
    import story_run
    for name, pattern, action in story_run.KNOWN_REFUSALS:
        if re.search(pattern, text or "", re.I):
            return name, action
    return None, None


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass  # a redirected stdout (a test) has no encoding to set
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--run", default=paths.DEFAULT_RIGHT,
                    help="a baseline of the runs table (QA_RUNS_TABLE), or the suffix of any copy "
                         "(default: default_right of the table)")
    ap.add_argument("--ticket", default=paths.TASK)
    a = ap.parse_args()
    paths.require_args(ap, ("--run", a.run), ("--ticket", a.ticket))
    try:
        folder = paths.copy_folder(a.run, RUNS)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    root = BASE / folder / "test-harness" / "qa-factory" / "artifacts" / a.ticket
    path = root / "state" / "conductor.jsonl"
    if not path.is_file():
        print(f"no conductor journal for {a.run}: {path}")
        return 1
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    total = sum(r.get("total_cost_usd") or 0 for r in rows)
    silent = sum(1 for r in rows if "No command run" in (r.get("did") or "")
                 or not (r.get("did") or "").strip())
    empty = sum(1 for r in rows if r.get("action") == "ask_person"
                and not (r.get("question") or "").strip())
    print(f"## {a.run} — the conductor over {a.ticket}\n")
    print(f"sessions **{len(rows)}**, cost **${total:.2f}**, ran no command **{silent}**, "
          f"`ask_person` with an empty question **{empty}**\n")

    groups = collections.defaultdict(lambda: [0, 0.0, 0])
    for r in rows:
        g = groups[family(r.get("refusal") or "")]
        g[0] += 1
        g[1] += r.get("total_cost_usd") or 0
        g[2] += r.get("num_turns") or 0
    print("| refusal family | sessions | $ | turns | share of the conductor |")
    print("|---|---|---|---|---|")
    for key, (n, cost, turns) in sorted(groups.items(), key=lambda kv: -kv[1][1]):
        share = f"{100.0 * cost / total:.0f}%" if total else "—"
        print(f"| {key} | {n} | ${cost:.2f} | {turns} | {share} |")

    matched = collections.Counter()
    unmatched_cost = 0.0
    for r in rows:
        name, _ = known_match(r.get("refusal") or "")
        matched[name or "(unmatched)"] += 1
        if name is None:
            unmatched_cost += r.get("total_cost_usd") or 0
    print(f"\nthe driver's own table would have matched "
          f"**{len(rows) - matched['(unmatched)']} of {len(rows)}**; "
          f"the rest cost **${unmatched_cost:.2f}**")
    for name, n in matched.most_common():
        print(f"   {name:<20} {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
