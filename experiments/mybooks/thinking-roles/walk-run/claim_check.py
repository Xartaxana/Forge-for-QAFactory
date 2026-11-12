#!/usr/bin/env python3
"""claim_check.py - the verdict on the speed and money claim of Slice 1 (t-2006 sec 4.2; t-1957 sec 7 step 4). Read-only.

    python walk_timing.py --task-root <T> --json > timing.json
    python claim_check.py timing.json

The claim: at most 7 minutes (420 s) and at most $0.50 per item. The input is `walk_timing.py --json`.
  REFUSED     the MEDIAN per-item wall (each row carries its dispatch's `per_item_wall_s`) is over 420 s, OR the median per-item cost (each row
              carries its dispatch's `cost_usd` / items) is over 0.50, OR any item from the third on in its dispatch has `wall_s` over 420 or
              `cost_usd` over 0.50. A figure over its limit refuses the claim whatever else is unknown.
  NOT PROVED  nothing is over, but a figure the verdict needs is "not measured" (a string, None, missing): named (AR-28: an unknown never passes).
  HOLDS       every figure is measured and none is over.
Prints ratios to the limits and yes/no, never a dollar value (F5). Exit 0 HOLDS, 1 REFUSED, 2 NOT PROVED.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

WALL_LIMIT_S = 420.0
COST_LIMIT_USD = 0.50
THIRD = 3          # items from the 3rd on in a dispatch are the late ones


def _number(value):
    return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def _unknown(value) -> str:
    return str(value) if isinstance(value, str) else "missing"


def judge(timing) -> tuple:
    """(verdict, [lines]) from the parsed `walk_timing --json` answer."""
    lines, refused, unknown = [], [], []
    if not isinstance(timing, dict) or not timing.get("timed") or not timing.get("dispatches"):
        return "NOT PROVED", ["no walk was timed: nothing to judge"]
    walls, costs = [], []
    for rep in timing["dispatches"]:
        rows = rep.get("rows") or []
        walk = rep.get("walk")
        per_wall = _number(rep.get("per_item_wall_s"))
        cost = _number(rep.get("cost_usd"))
        per_cost = cost / len(rows) if cost is not None and rows else None
        for i, row in enumerate(rows, 1):
            name = f"{walk}/{row.get('item')}"
            if per_wall is None:
                unknown.append(f"per-item wall of {walk}: {_unknown(rep.get('wall_s'))}")
            else:
                walls.append(per_wall)
            if per_cost is None:
                unknown.append(f"per-item cost of {walk}: {_unknown(rep.get('cost_usd'))}")
            else:
                costs.append(per_cost)
            if i >= THIRD:
                w, c = _number(row.get("wall_s")), _number(row.get("cost_usd"))
                if w is None:
                    unknown.append(f"wall of item {i} {name}: {_unknown(row.get('wall_s'))}")
                elif w > WALL_LIMIT_S:
                    refused.append(f"item {i} of a dispatch ({name}) wall is {w / WALL_LIMIT_S:.2f} x the limit")
                if c is None:
                    unknown.append(f"cost of item {i} {name}: {_unknown(row.get('cost_usd'))}")
                elif c > COST_LIMIT_USD:
                    refused.append(f"item {i} of a dispatch ({name}) cost is {c / COST_LIMIT_USD:.2f} x the limit")
    if walls:
        ratio = statistics.median(walls) / WALL_LIMIT_S
        lines.append(f"median per-item wall: {ratio:.2f} x the limit ({'over' if ratio > 1 else 'within'})")
        if ratio > 1:
            refused.append(f"median per-item wall is {ratio:.2f} x the limit")
    if costs:
        ratio = statistics.median(costs) / COST_LIMIT_USD
        lines.append(f"median per-item cost: {ratio:.2f} x the limit ({'over' if ratio > 1 else 'within'})")
        if ratio > 1:
            refused.append(f"median per-item cost is {ratio:.2f} x the limit")
    unknown = list(dict.fromkeys(unknown))
    if refused:
        return "REFUSED", lines + ["over: " + s for s in refused] + (["also not measured: " + s for s in unknown])
    if unknown:
        return "NOT PROVED", lines + ["not measured: " + s for s in unknown]
    return "HOLDS", lines


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("timing", help="the file written by walk_timing.py --json")
    args = parser.parse_args(argv)
    try:
        timing = json.loads(Path(args.timing).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        print(f"NOT PROVED\n  {args.timing} cannot be read as JSON ({type(exc).__name__})")
        return 2
    verdict, lines = judge(timing)
    print(verdict)
    for line in lines:
        print("  " + line)
    return {"HOLDS": 0, "REFUSED": 1}.get(verdict, 2)


if __name__ == "__main__":
    sys.exit(main())
