"""What a driver run spent, split into the work a clean run needs and the rest.

Reads one run's `state/driver-runs.jsonl` — the cost the CLI itself reported per session, which is
the authoritative figure for a driver run (FR-24, FR-25; the token-priced `state/cost/*.json` is
`provisional` and disagrees by a few percent).

Prints: cost by stage, cost by dispatch with its controller status, the conductor's share, the
first dispatch of each (stage, role) against every later one, and the price of a resumed turn
against a fresh one.

Run 5 of the reference story, which this was written for: $128.53 total, conductor $29.63 (23%),
the first dispatch of each pair $42.35 against $47.20 for all sixteen repeats, and a resumed turn at
$0.0812 against $0.0416 fresh — 1.95x on the closed run. That last line is the money argument of the whole run: our own
gaps did not just add turns, they added the most expensive kind.

    python experiments/measurers/spend_by_dispatch.py [--run <run>] [--ticket <TICKET>]

`--run` defaults to default_right of the runs table; without a table it is required. It is a named baseline or the suffix of any copy (`<copy_prefix><name>` under the runs base, B-267).

`test_measurers.py` covers the arithmetic: the total, the conductor's share, the first
dispatch of a (stage, role) against its repeats, and the two per-turn prices (FR-28).
"""
import argparse
import collections
import json
import pathlib
import sys

import paths
import report_run

BASE = paths.BASE
RUNS = dict(paths.BASELINES)        # the runs table's baselines ({} without a table); other names go by copy_folder


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass  # a redirected stdout (a test) has no encoding to set
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--run", default=paths.DEFAULT_RIGHT,
                    help="a named baseline (" + (", ".join(sorted(RUNS)) or "none: no runs table") + ") or the suffix "
                         "of any copy `prepare_copy.py --name <name>` made: <copy_prefix><name> under the runs base (B-267)")
    ap.add_argument("--ticket", default=paths.TASK)
    a = ap.parse_args()
    paths.require_args(ap, ("--run", a.run), ("--ticket", a.ticket))
    try:
        folder = report_run.copy_folder(a.run, RUNS)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    root = BASE / folder / "test-harness" / "qa-factory" / "artifacts" / a.ticket
    if not (root / "state" / "driver-runs.jsonl").is_file():
        # a run name nobody listed may name a copy that is not there: say which file, not a traceback (FR-1)
        print(f"no driver journal for run {a.run!r}: {root / 'state' / 'driver-runs.jsonl'} is not there "
              f"(the copy is {BASE / folder}; check --run and --ticket)", file=sys.stderr)
        return 2
    rows = [json.loads(line) for line
            in (root / "state" / "driver-runs.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()]
    state = json.loads((root / "state" / "controller.json").read_text(encoding="utf-8-sig",
                                                                     errors="replace"))
    status = {k: (v or {}).get("status") for k, v in (state.get("dispatches") or {}).items()}
    total = sum(r["total_cost_usd"] for r in rows)
    print(f"## {a.run} — {a.ticket}: {len(rows)} sessions, ${total:.2f}\n")

    by_stage = collections.defaultdict(lambda: [0.0, 0, 0])
    for r in rows:
        s = by_stage[r.get("stage") or "?"]
        s[0] += r["total_cost_usd"]
        s[1] += r["num_turns"]
        s[2] += 1
    print("| stage | $ | turns | calls |")
    print("|---|---|---|---|")
    for key in sorted(by_stage):
        cost, turns, calls = by_stage[key]
        print(f"| {key} | ${cost:.2f} | {turns} | {calls} |")

    per = collections.defaultdict(lambda: [0.0, 0, 0])
    for r in rows:
        if r.get("kind") != "role":
            continue
        d = per[r["dispatch"]]
        d[0] += r["total_cost_usd"]
        d[1] += r["num_turns"]
        d[2] += 1
    print("\n| dispatch | status | $ | turns | sessions |")
    print("|---|---|---|---|---|")
    for key in sorted(per, key=lambda x: -per[x][0]):
        cost, turns, sessions = per[key]
        print(f"| {key} | {status.get(key, '?')} | ${cost:.2f} | {turns} | {sessions} |")

    conductor = sum(r["total_cost_usd"] for r in rows if r.get("kind") == "conductor")
    print(f"\nconductor **${conductor:.2f}** of ${total:.2f} "
          f"({100.0 * conductor / total:.0f}%), roles ${total - conductor:.2f}")

    first, extra = {}, []
    for key in sorted(per, key=lambda x: int(x.rsplit("-", 1)[1])):
        base = key.rsplit("-", 1)[0]
        (extra.append(key) if base in first else first.setdefault(base, key))
    print(f"\nfirst dispatch of each (stage, role): **${sum(per[k][0] for k in first.values()):.2f}**")
    print(f"every later dispatch ({len(extra)}): **${sum(per[k][0] for k in extra):.2f}**")
    for key in extra:
        print(f"   {key:<28} {status.get(key, '?'):<22} ${per[key][0]:.2f}")

    for label, want in (("resumed", True), ("fresh", False)):
        sessions = [r for r in rows if r.get("kind") == "role" and bool(r.get("resumed")) is want]
        turns = sum(r["num_turns"] for r in sessions) or 1
        cost = sum(r["total_cost_usd"] for r in sessions)
        print(f"\n{label:<8} sessions {len(sessions):>3}: ${cost:.2f}, {turns} turns "
              f"= ${cost / turns:.4f}/turn")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
