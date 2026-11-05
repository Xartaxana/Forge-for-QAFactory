"""The comparison report for one run against another: money by agent, stages by clock.

    python experiments/measurers/report_run.py --left <baseline> --right <run> [--ticket <TICKET>]

Money: every request's `usage` in the project's transcripts (the orchestrator session and every
subagent session), priced with the plugin's model-rates.json — the same method for both runs, so a
driver run and an orchestrator run are one currency. `compare.py` already does that; this script
groups it by agent and puts the two runs side by side.

Clock: `pipeline.json` records `started` and `finished` per stage, written by the factory itself at
every boundary, so the wall clock of a stage is not reconstructed from transcripts.

The driver journal (`state/driver-runs.jsonl`) adds what a transcript cannot say: which calls were
a role's first work, which were resumptions of a role, and which were conductor sessions.
"""
import argparse
import collections
import json
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import compare  # noqa: E402
import paths  # noqa: E402

BASE = paths.BASE
COPIES = dict(paths.BASELINES)
RUN_NAME = paths.RUN_NAME


copy_folder = paths.copy_folder      # the one rule lives in paths.py (B-267); the name stays for the readers


def project(name: str) -> Path:
    return BASE / copy_folder(name, COPIES) / "test-harness"


def task_root(name: str, ticket: str) -> Path:
    return project(name) / "qa-factory" / "artifacts" / ticket


def session_roles(name: str, ticket: str) -> dict:
    """{session_id: role} from the driver's journal. In a driver run every role is its own
    top-level `claude -p` session, so a transcript scan labels them all `orchestrator` — the
    journal is the only place that says which role a session was, and whether it was a
    resumption or a conductor call."""
    path = task_root(name, ticket) / "state" / "driver-runs.jsonl"
    if not path.is_file():
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            row = json.loads(line)
        except ValueError:
            continue
        sid = row.get("session_id")
        if sid:
            out[sid] = ("conductor" if row.get("kind") == "conductor"
                        else str(row.get("role") or "role"))
    return out


def money(name: str, ticket: str, cache: Path | None = None) -> dict:
    """{agent: {requests, cost_usd, dispatches}} — from the run's own transcripts, with a driver
    run's sessions attributed to the role the journal names."""
    if cache and cache.is_file():
        return json.loads(cache.read_text(encoding="utf-8"))["cost"]["by_role"]
    report = compare.cost_report(project(name), ticket)
    roles = session_roles(name, ticket)
    if not roles:
        return report["by_role"]
    by_role = collections.defaultdict(
        lambda: {"requests": 0, "cost_usd": 0.0, "unpriced_requests": 0, "dispatches": 0})
    skipped = 0
    for session in report["sessions"]:
        named = roles.get(session["session"])
        if not named:
            # A transcript in the same project folder that this run's journal does not own: an
            # abandoned attempt of the same ticket. The journal defines the run, not the folder.
            skipped += 1
            continue
        for index, row in enumerate(session["rows"]):
            agent = named if (index == 0 and named) else row["role"]
            bucket = by_role[agent]
            bucket["requests"] += row["requests"]
            bucket["cost_usd"] = round(bucket["cost_usd"] + row["cost_usd"], 2)
            bucket["unpriced_requests"] += row["unpriced_requests"]
            bucket["dispatches"] += 1
    if skipped:
        print(f"note: {skipped} transcript(s) in this project belong to an earlier attempt of the "
              f"same ticket and are not counted — {name}'s journal does not own them.\n")
    return dict(by_role)


def unpriced_total(money_by_agent: dict) -> str:
    """The unpriced-request line of one column. A cached measurement that predates the count has
    no such field: its count is unknown, and it says so rather than printing 0 (FR-41)."""
    counts = [v.get("unpriced_requests") for v in money_by_agent.values()]
    if any(c is None for c in counts):
        return "unpriced requests: unknown (this cached measurement predates the count; rerun compare.py --json to fill it)"
    return compare.unpriced_line(sum(counts))


def cache_for(run: str, named: str):
    """The cached measurement this run may be read from, or None.

    The default used to be one cache file for ANY `--left`, so every comparison silently
    printed the baseline in the left column: a comparison of two newer runs read the baseline's
    figure on the left, which was not that run's cost. A cache belongs to ONE run (FR-27): it is used only
    for the run the runs table names it for (QA_RUNS_TABLE, key caches, a path from the table's folder),
    a cache named on the command line (absolute or relative to the cwd) belongs to whoever named it, and the report
    says out loud when either was used. Its own function so a test can ask it, which is what was
    missing when the default was written."""
    if named:
        return Path(named)
    return paths.table_path("caches", run)


def clock(seconds: float) -> str:
    seconds = int(seconds or 0)
    return f"{seconds // 3600}:{seconds % 3600 // 60:02d}:{seconds % 60:02d}"


def stage_times(name: str, ticket: str) -> dict:
    pipeline = json.loads((task_root(name, ticket) / "pipeline.json").read_text(encoding="utf-8-sig"))
    out = {}
    for stage, row in (pipeline.get("stages") or {}).items():
        row = row or {}
        started, finished = row.get("started"), row.get("finished")
        span = ""
        if started and finished:
            span = clock((datetime.fromisoformat(finished) - datetime.fromisoformat(started)).total_seconds())
        out[stage] = {"status": row.get("status"), "span": span,
                      "started": (started or "")[5:16].replace("T", " "),
                      "finished": (finished or "")[5:16].replace("T", " ")}
    return out


def journal(name: str, ticket: str) -> dict:
    path = task_root(name, ticket) / "state" / "driver-runs.jsonl"
    if not path.is_file():
        return {}
    buckets = collections.defaultdict(lambda: {"calls": 0, "cost": 0.0, "turns": 0, "seconds": 0})
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            row = json.loads(line)
        except ValueError:
            continue
        key = ("conductor" if row.get("kind") == "conductor"
               else "role resumed" if row.get("resumed") else "role first work")
        bucket = buckets[key]
        bucket["calls"] += 1
        bucket["cost"] += float(row.get("total_cost_usd") or 0)
        bucket["turns"] += int(row.get("num_turns") or 0)
        bucket["seconds"] += int((row.get("duration_ms") or 0) / 1000)
    return dict(buckets)


def table(rows: list, head: list) -> None:
    print("| " + " | ".join(head) + " |")
    print("|" + "|".join("---" for _ in head) + "|")
    for row in rows:
        print("| " + " | ".join(str(cell) for cell in row) + " |")
    print()


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--left", default=paths.DEFAULT_LEFT)
    ap.add_argument("--right", default=paths.DEFAULT_RIGHT)
    ap.add_argument("--ticket", default=paths.TASK)
    ap.add_argument("--left-cache", default="",
                    help="a compare.py --json output for the left run (its transcripts may be gone); "
                         "the cache must belong to the run --left names, and only a run the runs table gives a cache has one")
    a = ap.parse_args()
    paths.require_args(ap, ("--left", a.left), ("--right", a.right), ("--ticket", a.ticket))
    left_cache = cache_for(a.left, a.left_cache)
    if left_cache and left_cache.is_file():
        gone = "" if compare.transcript_dir(project(a.left)).is_dir() else " (its transcripts are gone)"
        print(f"note: the {a.left} column is read from the cached measurement {left_cache.name}"
              f"{gone}, not from transcripts.\n")

    left = money(a.left, a.ticket, left_cache)
    right = money(a.right, a.ticket)
    print(f"## Money by agent — {a.left} vs {a.right}\n")
    agents = sorted(set(left) | set(right), key=lambda n: -(right.get(n, {}).get("cost_usd") or 0))
    rows = []
    for agent in agents:
        one, two = left.get(agent) or {}, right.get(agent) or {}
        delta = (two.get("cost_usd") or 0) - (one.get("cost_usd") or 0)
        rows.append([agent,
                     f"${one.get('cost_usd', 0):.2f}" + (f" / {one.get('requests', 0)} req" if one else ""),
                     f"${two.get('cost_usd', 0):.2f}" + (f" / {two.get('requests', 0)} req" if two else ""),
                     f"{delta:+.2f}"])
    total_left = sum((v.get("cost_usd") or 0) for v in left.values())
    total_right = sum((v.get("cost_usd") or 0) for v in right.values())
    rows.append(["**total**", f"**${total_left:.2f}**", f"**${total_right:.2f}**",
                 f"**{total_right - total_left:+.2f}**"])
    table(rows, ["agent", a.left, a.right, "delta"])
    print(f"{a.left}: {unpriced_total(left)}")
    print(f"{a.right}: {unpriced_total(right)}\n")

    print(f"## Stages by the clock — {a.left} vs {a.right}\n")
    one, two = stage_times(a.left, a.ticket), stage_times(a.right, a.ticket)
    rows = []
    for stage in sorted(set(one) | set(two)):
        row_one, row_two = one.get(stage) or {}, two.get(stage) or {}
        rows.append([stage, row_one.get("span") or "—", row_two.get("span") or "—",
                     row_two.get("status") or "—", row_two.get("finished") or "—"])
    table(rows, ["stage", f"{a.left} span", f"{a.right} span", f"{a.right} status", f"{a.right} finished"])

    for name in (a.left, a.right):
        rows_journal = journal(name, a.ticket)
        if not rows_journal:
            continue
        print(f"## Control layer — {name} (state/driver-runs.jsonl)\n")
        total = sum(v["cost"] for v in rows_journal.values()) or 1
        table([[key, v["calls"], f"${v['cost']:.2f}", f"{v['cost'] / total * 100:.0f}%",
                v["turns"], clock(v["seconds"])]
               for key, v in sorted(rows_journal.items(), key=lambda kv: -kv[1]["cost"])],
              ["kind", "calls", "cost", "share", "turns", "wall clock"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
