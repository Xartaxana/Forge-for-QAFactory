"""Money by agent up to a moment, for two runs side by side.

    python experiments/measurers/report_to_gate.py --left <baseline> --right <run> [--ticket <TICKET>]

Both columns are built the same way: every request in the run's own transcripts, priced with the
plugin's model-rates.json (API list price), counted only while its timestamp is at or before that
run's cut. The cut is the start of S5 — everything the run spent to reach gate A, the gate itself
included. A run that has not started S5 yet is cut at "now".

A driver run has no orchestrator session: every role is its own top-level `claude -p`, so the
session is named by the driver's journal (`state/driver-runs.jsonl`), which also says which calls
were conductor sessions and which were resumptions. Transcripts in the project folder that the
journal does not own belong to an earlier attempt and are not counted.
"""
import argparse
import collections
import glob
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import compare  # noqa: E402
import paths  # noqa: E402
import report_run  # noqa: E402


def cut_at(name: str, ticket: str) -> datetime:
    """S5's start, or now for a run that has not reached it."""
    pipeline = report_run.task_root(name, ticket) / "pipeline.json"
    try:
        stages = json.loads(pipeline.read_text(encoding="utf-8-sig")).get("stages") or {}
        started = ((stages.get("S5") or {}).get("started"))
        if started:
            return datetime.fromisoformat(started)
    except (OSError, ValueError):
        pass
    return datetime.now(timezone.utc)


def scan_until(path: Path, rate: dict, cut: datetime) -> tuple:
    """(role, requests, cost, unpriced requests) of one transcript, counting only what happened at or
    before `cut`. A request the catalogue cannot price is counted, not turned into $0 (FR-41)."""
    if cut.tzinfo is None:  # an aware stamp cannot be compared with it: refuse once, not a silent zero (FR-41)
        raise ValueError(f"scan_until: the cut {cut.isoformat()} has no timezone")

    def in_time(row) -> bool:  # before the dedupe: a copy of an id past the cut must not displace the earlier one
        stamp = row.get("timestamp")
        try:
            return bool(stamp) and datetime.fromisoformat(stamp.replace("Z", "+00:00")) <= cut
        except (ValueError, AttributeError):  # a bad stamp on one line; a naive cut is refused above, never every line
            return False

    seen = {key: (model, usage) for key, (model, usage, _stamp) in compare.requests_of(path, keep=in_time).items()}
    role = compare.role_of(path)  # the first user line, whatever its stamp
    cost, unpriced = compare.price_seen(rate, seen)
    return role, len(seen), cost, unpriced


def by_agent(name: str, ticket: str) -> dict:
    rate = compare.rates()
    root = compare.transcript_dir(report_run.project(name))
    journal = report_run.session_roles(name, ticket)
    cut = cut_at(name, ticket)
    out = collections.defaultdict(lambda: {"requests": 0, "cost_usd": 0.0, "unpriced_requests": 0})
    for main in sorted(glob.glob(str(root / "*.jsonl")), key=os.path.getmtime):
        sid = Path(main).stem
        if ticket not in Path(main).read_text(encoding="utf-8", errors="replace"):
            continue
        named = journal.get(sid)
        if journal and not named:
            continue  # an earlier attempt of the same ticket, in the same project folder
        rows = [(named or "orchestrator", *scan_until(Path(main), rate, cut)[1:])]
        for sub in sorted(glob.glob(str(root / sid / "subagents" / "*.jsonl")), key=os.path.getmtime):
            role, requests, cost, unpriced = scan_until(Path(sub), rate, cut)
            rows.append((role or "?", requests, cost, unpriced))
        for agent, requests, cost, unpriced in rows:
            if not requests:
                continue
            out[agent]["requests"] += requests
            out[agent]["cost_usd"] += cost
            out[agent]["unpriced_requests"] += unpriced
    return {agent: {"requests": v["requests"], "cost_usd": round(v["cost_usd"], 2),
                    "unpriced_requests": v["unpriced_requests"]}
            for agent, v in out.items()}


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--left", default=paths.DEFAULT_LEFT)
    ap.add_argument("--right", default=paths.DEFAULT_RIGHT)
    ap.add_argument("--ticket", default=paths.TASK)
    a = ap.parse_args()
    paths.require_args(ap, ("--left", a.left), ("--right", a.right), ("--ticket", a.ticket))
    left, right = by_agent(a.left, a.ticket), by_agent(a.right, a.ticket)
    print(f"cut: {a.left} at {cut_at(a.left, a.ticket)}, {a.right} at {cut_at(a.right, a.ticket)}\n")
    agents = sorted(set(left) | set(right),
                    key=lambda agent: -max(left.get(agent, {}).get("cost_usd", 0),
                                           right.get(agent, {}).get("cost_usd", 0)))
    print(f"| {'agent':24} | {a.left:22} | {a.right:22} | delta |")
    print("|" + "-" * 26 + "|" + "-" * 24 + "|" + "-" * 24 + "|-------|")
    for agent in agents:
        one, two = left.get(agent) or {}, right.get(agent) or {}
        cell_one = f"${one.get('cost_usd', 0):.2f} ({one.get('requests', 0)} req)" if one else "—"
        cell_two = f"${two.get('cost_usd', 0):.2f} ({two.get('requests', 0)} req)" if two else "—"
        delta = (two.get("cost_usd") or 0) - (one.get("cost_usd") or 0)
        print(f"| {agent:24} | {cell_one:22} | {cell_two:22} | {delta:+.2f} |")
    total_left = sum(v["cost_usd"] for v in left.values())
    total_right = sum(v["cost_usd"] for v in right.values())
    print(f"| {'TOTAL':24} | {f'${total_left:.2f}':22} | {f'${total_right:.2f}':22} | "
          f"{total_right - total_left:+.2f} |")
    for name, side in ((a.left, left), (a.right, right)):
        print(f"{name}: {compare.unpriced_line(sum(v['unpriced_requests'] for v in side.values()))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
