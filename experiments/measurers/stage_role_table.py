"""Stage-by-role table of two runs of one ticket: time, tokens and price side by side.

    python experiments/measurers/stage_role_table.py [--left <baseline>] [--right <run>] [--ticket <TICKET>] [--role-time]

Layout (the owner's template): Stage | Role | <left> time, tokens, price | <right> time, tokens,
price. TIME belongs to the STAGE, TOKENS and PRICE to the ROLE: for each stage one header row
carrying the stage's time span in each run's time column, then one row per role that either run
dispatched (the left run's order of first dispatch, then the right run's extra roles) with tokens
and price and an empty time cell; no stage subtotal rows; a grand total row (time = sum of the
stage spans, tokens and price = sums). Stages S0..S9 in order, "—" last. The orchestrator of an
orchestrator run and the conductor of a driver run are roles of their own. `--role-time` also
fills each role's own time (the union of its sessions' intervals, see Time).

Carriers (FR-24 / FR-25: every figure names its carrier, and where two records of one quantity
exist the table says which it uses and prints the gap).

  Money and tokens   The run's Claude Code transcripts, priced by `compare.py` (`compare.cost_report`
                     selects the sessions, `compare.scan` prices each transcript, `compare.price_turn`
                     prices one request) with the catalogue `report_run.py` uses. Sessions are the
                     ones `report_run.py` counts: in a driver run the sessions its journal
                     (`state/driver-runs.jsonl`) names - a transcript the journal does not own is an
                     earlier attempt and is not counted, exactly as report_run says; in an
                     orchestrator run every transcript that mentions the ticket.
                     Tokens are ALL tokens of the unique requests: input + output + cache read +
                     cache write (5m and 1h), the kinds `compare._tokens` prices.
                     A transcript's dollars are `compare.scan`'s cent-rounded figure, so the table
                     adds the same cents `report_run.money` adds and the two totals agree to the cent
                     when every session is placed.

  Stage and role     Driver run: `state/driver-runs.jsonl`. One session is placed ONCE, on the stage
                     and role of its FIRST journal row; resumed rows share the session, so the money
                     is the transcript's and the wall time is the sum of the session's rows'
                     `duration_ms`. A conductor row is the role `conductor`; a session whose first
                     row names no stage goes to "—". A journal session with no transcript is placed
                     with time only and counted in the notes line.
                     Orchestrator run: the cost files (`state/cost/<session>.json`) do not exist in
                     the run copies, and the controller's dispatch records carry no session or agent
                     id, so the join is by CLOCK. Stage windows: `pipeline.json` `stages.<S>.started`
                     (a request belongs to the stage whose window opened most recently before it).
                       - a subagent transcript goes to the stage window holding its first timestamp,
                         under the role its first user turn names (`compare.scan`'s role); it goes to
                         "—" when the controller's event log (`state/events.jsonl`, `dispatch`
                         events) says that stage never dispatched that role, or when no window holds
                         it;
                       - the orchestrator's own requests are cut by the same windows, so it has one
                         row per stage it served ("—" for requests before the first window). Its
                         dollars are the transcript's cent-rounded figure split over the stages by
                         the largest-remainder method on each request's exact price (`apportion`),
                         so the parts add back to the whole cent.

  Time               Stage span: `pipeline.json` `stages.<S>.started` -> `finished`, the span
                     report_run prints under "Stages by the clock". When `finished` is missing (or
                     the stage has no pipeline entry, as "—") the span is the UNION of the stage's
                     session intervals, printed with a `*` and one footnote line; never a zero.
                     Session intervals: driver run - each journal row as [ts - duration_ms, ts];
                     orchestrator run - first to last timestamp of a subagent transcript, or of the
                     orchestrator's requests inside the stage. A role's own time (`--role-time`) is
                     the length of the union of its intervals. The grand total time is the sum of
                     the stage spans. Printed h:mm.

The two lines after the table give, per run, the table's total against the total `report_run.py`
prints for the same run (with the cached measurement it uses for the baseline on the left). A gap is a
dropped session or a measurement taken at another moment - the line says which figure it read.
"""
import argparse
import glob
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import compare  # noqa: E402
import paths  # noqa: E402
import report_run  # noqa: E402

NO_STAGE = "—"
ORCHESTRATOR = "orchestrator"


# --- small pure helpers ---------------------------------------------------------------------------

def parse_ts(text):
    """A timezone-aware datetime, or None for an absent or unreadable stamp (never a guess)."""
    if not text:
        return None
    try:
        moment = datetime.fromisoformat(str(text).replace("Z", "+00:00"))
    except ValueError:
        return None
    return moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)


def union_seconds(intervals) -> float:
    """Length of the union of [(start, end)] intervals in seconds: overlapping time counts once."""
    total, cursor = 0.0, None
    for start, end in sorted(iv for iv in intervals if iv and iv[0] and iv[1] and iv[1] > iv[0]):
        if cursor is None or start > cursor:
            total += (end - start).total_seconds()
            cursor = end
        elif end > cursor:
            total += (end - cursor).total_seconds()
            cursor = end
    return total


def apportion(total_cents: int, weights: dict) -> dict:
    """Split a whole number of cents over the keys of `weights` in proportion to them, by the
    largest-remainder method: the parts are integers and add up to `total_cents` exactly. All
    weights zero (nothing priceable to go by): the whole amount goes to the first key - an amount
    is never dropped."""
    if not weights:
        return {}
    keys = list(weights)
    whole = sum(weights.values())
    if whole <= 0:
        return {key: (total_cents if index == 0 else 0) for index, key in enumerate(keys)}
    exact = {key: total_cents * weights[key] / whole for key in keys}
    parts = {key: int(exact[key]) for key in keys}
    left = total_cents - sum(parts.values())
    for key in sorted(keys, key=lambda k: (-(exact[k] - parts[k]), keys.index(k)))[:left]:
        parts[key] += 1
    return parts


def stage_key(stage: str) -> tuple:
    match = re.fullmatch(r"S(\d+)", stage)
    if match:
        return (0, int(match.group(1)), "")
    return (2, 0, "") if stage == NO_STAGE else (1, 0, stage)


def hmm(seconds) -> str:
    minutes = int((seconds + 30) // 60)
    return f"{minutes // 60}:{minutes % 60:02d}"


def tokens_text(count: int) -> str:
    if count >= 1_000_000:
        return f"{count / 1e6:.1f}M"
    return f"{count / 1e3:.0f}k" if count >= 1000 else str(count)


def cents_text(cents: int) -> str:
    return f"${cents / 100:.2f}"


# --- reading a run --------------------------------------------------------------------------------

def read_requests(path: Path) -> list:
    """[(timestamp, model, usage)] of the unique requests of one transcript, by the same rule as
    `compare.scan`: one per message id (the last line of it wins), a zero-token synthetic marker is
    not a request."""
    seen = {}
    for line in Path(path).open(encoding="utf-8"):
        try:
            obj = json.loads(line)
        except ValueError:
            continue
        message = obj.get("message") or {}
        if (obj.get("type") == "assistant" and message.get("usage")
                and not compare.is_empty_marker(message.get("model"), message["usage"])):
            seen[message.get("id") or obj.get("uuid")] = (
                parse_ts(obj.get("timestamp")), message.get("model"), message["usage"])
    return list(seen.values())


def request_tokens(usage) -> int:
    return sum(count for _, count in compare._tokens(usage or {}))


def session_files(root: Path, sid: str) -> list:
    """The transcript files of one session in the order `compare.cost_report` lists its rows: the
    main transcript, then its subagents by modification time."""
    return [Path(root) / f"{sid}.jsonl",
            *[Path(p) for p in sorted(glob.glob(str(Path(root) / sid / "subagents" / "*.jsonl")),
                                      key=os.path.getmtime)]]


def add(cells: dict, stage: str, role: str, cents=0, tokens=0, intervals=(), loose=0.0, first=None):
    cell = cells.setdefault((stage, role), {"cents": 0, "tokens": 0, "intervals": [], "loose": 0.0,
                                            "first": None, "sessions": 0})
    cell["cents"] += cents
    cell["tokens"] += tokens
    cell["intervals"].extend(intervals)
    cell["loose"] += loose
    cell["sessions"] += 1
    if first and (cell["first"] is None or first < cell["first"]):
        cell["first"] = first
    return cell


def journal_sessions(name: str, ticket: str) -> list:
    """One entry per session of the driver journal, in file order: the stage and role of its first
    row, and the time of all its rows. [] for a run with no journal (an orchestrator run)."""
    path = report_run.task_root(name, ticket) / "state" / "driver-runs.jsonl"
    if not path.is_file():
        return []
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            row = json.loads(line)
        except ValueError:
            continue
        sid = row.get("session_id")
        if not sid:
            continue
        entry = out.get(sid)
        if entry is None:
            role = "conductor" if row.get("kind") == "conductor" else str(row.get("role") or "role")
            entry = out[sid] = {"session": sid, "stage": str(row.get("stage") or NO_STAGE),
                                "role": role, "intervals": [], "loose": 0.0, "first": None}
        end, seconds = parse_ts(row.get("ts")), float(row.get("duration_ms") or 0) / 1000
        if end and seconds:
            entry["intervals"].append((end - timedelta(seconds=seconds), end))
        else:
            entry["loose"] += seconds
        if end:
            begin = end - timedelta(seconds=seconds)
            if entry["first"] is None or begin < entry["first"]:
                entry["first"] = begin
    return list(out.values())


def stage_windows(name: str, ticket: str) -> list:
    """[(start, stage)] sorted by start, from pipeline.json; [] when the file is absent."""
    path = report_run.task_root(name, ticket) / "pipeline.json"
    try:
        stages = json.loads(path.read_text(encoding="utf-8-sig")).get("stages") or {}
    except (OSError, ValueError):
        return []
    windows = [(parse_ts((row or {}).get("started")), stage) for stage, row in stages.items()]
    return sorted((start, stage) for start, stage in windows if start)


def stage_at(windows: list, moment):
    """The stage whose window opened most recently at or before `moment`, or None."""
    found = None
    for start, stage in windows:
        if moment is not None and start <= moment:
            found = stage
    return found


def dispatched_roles(name: str, ticket: str):
    """{stage: {roles the controller dispatched there}} from the event log, or None when the log is
    absent (then no role check is possible and none is made)."""
    path = report_run.task_root(name, ticket) / "state" / "events.jsonl"
    if not path.is_file():
        return None
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        payload = event.get("payload") or {}
        if event.get("type") == "dispatch" and payload.get("stage") and payload.get("role"):
            out.setdefault(payload["stage"], set()).add(payload["role"])
    return out


def collect(name: str, ticket: str) -> dict:
    """{cells: {(stage, role): cell}, sessions, unplaced, not_owned, no_transcript, unpriced,
    cents} - the whole run placed on stages and roles. See the module docstring for the join."""
    project = report_run.project(name)
    report = compare.cost_report(project, ticket)
    root = compare.transcript_dir(project)
    rate = compare.rates()
    by_session = {s["session"]: s for s in report["sessions"]}
    cells, notes = {}, {"sessions": 0, "unplaced": 0, "not_owned": 0, "no_transcript": 0}
    unpriced = 0

    def files_and_requests(session):
        files = session_files(root, session["session"])
        if len(files) != len(session["rows"]):
            raise RuntimeError(f"session {session['session']}: cost_report lists {len(session['rows'])} "
                               f"transcripts, {len(files)} found on disk")
        out = []
        for row, path in zip(session["rows"], files):
            requests = read_requests(path)
            if len(requests) != row["requests"]:
                raise RuntimeError(f"{path.name}: {len(requests)} requests read here, "
                                   f"{row['requests']} by compare.scan")
            out.append((row, requests))
        return out

    journal = journal_sessions(name, ticket)
    if journal:
        owned = {entry["session"] for entry in journal}
        notes["not_owned"] = sum(1 for sid in by_session if sid not in owned)
        for entry in journal:
            session = by_session.get(entry["session"])
            cents = tokens = 0
            if session is None:
                notes["no_transcript"] += 1
            else:
                unpriced += session["unpriced_requests"]
                for row, requests in files_and_requests(session):
                    cents += round(row["cost_usd"] * 100)
                    tokens += sum(request_tokens(usage) for _, _, usage in requests)
            add(cells, entry["stage"], entry["role"], cents, tokens, entry["intervals"], entry["loose"],
                entry["first"])
            notes["sessions"] += 1
            notes["unplaced"] += entry["stage"] == NO_STAGE
    else:
        windows = stage_windows(name, ticket)
        dispatched = dispatched_roles(name, ticket)
        for session in report["sessions"]:
            unpriced += session["unpriced_requests"]
            notes["sessions"] += 1
            for index, (row, requests) in enumerate(files_and_requests(session)):
                total_cents = round(row["cost_usd"] * 100)
                if index == 0:
                    groups = {}
                    for moment, model, usage in requests:
                        groups.setdefault(stage_at(windows, moment) or NO_STAGE, []).append(
                            (moment, model, usage))
                    weights = {stage: sum(compare.price_turn(rate, model, usage) or 0
                                          for _, model, usage in group)
                               for stage, group in groups.items()}
                    parts = apportion(total_cents, weights)
                    for stage, group in groups.items():
                        stamps = [moment for moment, _, _ in group if moment]
                        span = [(min(stamps), max(stamps))] if stamps else []
                        add(cells, stage, ORCHESTRATOR, parts[stage],
                            sum(request_tokens(usage) for _, _, usage in group), span, 0.0,
                            min(stamps) if stamps else None)
                        notes["unplaced"] += stage == NO_STAGE
                    if not groups:
                        add(cells, NO_STAGE, ORCHESTRATOR)
                        notes["unplaced"] += 1
                    continue
                first, last = parse_ts(row.get("first")), parse_ts(row.get("last"))
                stage, role = stage_at(windows, first), row["role"]
                if stage is None or (dispatched is not None and role not in dispatched.get(stage, ())):
                    stage = NO_STAGE
                    notes["unplaced"] += 1
                add(cells, stage, role, total_cents,
                    sum(request_tokens(usage) for _, _, usage in requests),
                    [(first, last)] if first and last else [], 0.0, first)
    return {"cells": cells, "notes": notes, "unpriced": unpriced, "spans": stage_spans(name, ticket),
            "cents": sum(cell["cents"] for cell in cells.values())}


def report_run_cents(name: str, ticket: str, cache=None) -> int:
    """The total `report_run.py` prints for this run, in cents: the sum of its money by agent."""
    money = report_run.money(name, ticket, cache if cache and cache.is_file() else None)
    return sum(round((value.get("cost_usd") or 0) * 100) for value in money.values())


# --- the table ------------------------------------------------------------------------------------

def stage_totals(cells: dict, stage: str):
    """(seconds, tokens, cents) of one stage of one run, or None when the run has nothing there."""
    mine = [cell for (s, _), cell in cells.items() if s == stage]
    if not mine:
        return None
    return (union_seconds([iv for cell in mine for iv in cell["intervals"]])
            + sum(cell["loose"] for cell in mine),
            sum(cell["tokens"] for cell in mine), sum(cell["cents"] for cell in mine))


def cell_texts(cell) -> list:
    if not cell:
        return ["—", "—", "—"]
    seconds, tokens, cents = cell
    return [hmm(seconds), tokens_text(tokens), cents_text(cents)]


def cell_totals(cell):
    return (union_seconds(cell["intervals"]) + cell["loose"], cell["tokens"], cell["cents"])


def role_order(left: dict, right: dict, stage: str) -> list:
    """The roles of one stage: the left run's in the order first dispatched, then the right run's
    roles the left did not have, in the order first dispatched."""
    def ordered(cells):
        mine = [(cell["first"] is None, cell["first"] or datetime.min.replace(tzinfo=timezone.utc), role)
                for (s, role), cell in cells.items() if s == stage]
        return [role for _, _, role in sorted(mine)]
    first = ordered(left)
    return first + [role for role in ordered(right) if role not in first]


def stage_spans(name: str, ticket: str) -> dict:
    """{stage: seconds} of `pipeline.json` `started` -> `finished`, the span report_run prints under
    "Stages by the clock". A stage with either stamp missing (or finished before started) is left
    out: its span is not known, and the table says so instead of showing a zero (FR-41)."""
    path = report_run.task_root(name, ticket) / "pipeline.json"
    try:
        stages = json.loads(path.read_text(encoding="utf-8-sig")).get("stages") or {}
    except (OSError, ValueError):
        return {}
    out = {}
    for stage, row in stages.items():
        start, end = parse_ts((row or {}).get("started")), parse_ts((row or {}).get("finished"))
        if start and end and end >= start:
            out[stage] = (end - start).total_seconds()
    return out


def stage_span(run: dict, stage: str):
    """(seconds, estimated) of one stage of one run: the pipeline span; when `finished` is missing
    the union of the stage's session intervals, flagged as estimated; (None, False) when the run has
    neither a span nor a session there."""
    if stage in run["spans"]:
        return run["spans"][stage], False
    totals = stage_totals(run["cells"], stage)
    return (totals[0], True) if totals else (None, False)


FOOTNOTE = ("\\* the stage has no `finished` in pipeline.json (or no pipeline entry): the union of "
            "its sessions' intervals is shown instead.")


def table_lines(left: dict, right: dict, names: tuple, role_time: bool = False) -> tuple:
    """(lines, any estimated span). The owner's layout: per stage one header row carrying the
    stage's time span, then a row per role with tokens and cost (and, with `role_time`, the role's
    own time); no stage subtotal rows; a grand total row - time = the sum of the stage spans."""
    a, b = names
    head = ["Стадии", "Роли"] + [f"{n} {w}" for n in (a, b) for w in ("время", "токены", "цена")]
    lines = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    stages = sorted({s for s, _ in left["cells"]} | {s for s, _ in right["cells"]}, key=stage_key)
    grand = {"l": [0.0, 0, 0], "r": [0.0, 0, 0]}
    starred = False
    for stage in stages:
        header = [stage, ""]
        for key, run in (("l", left), ("r", right)):
            seconds, estimated = stage_span(run, stage)
            starred = starred or estimated
            header += [("—" if seconds is None else hmm(seconds) + ("\\*" if estimated else "")), "", ""]
            grand[key][0] += seconds or 0
            totals = stage_totals(run["cells"], stage)
            grand[key][1] += totals[1] if totals else 0
            grand[key][2] += totals[2] if totals else 0
        lines.append("| " + " | ".join(header) + " |")
        for role in role_order(left["cells"], right["cells"], stage):
            row = ["", role]
            for run in (left, right):
                cell = run["cells"].get((stage, role))
                if not cell:
                    row += ["—" if role_time else "", "—", "—"]
                    continue
                seconds, tokens, cents = cell_totals(cell)
                row += [hmm(seconds) if role_time else "", tokens_text(tokens), cents_text(cents)]
            lines.append("| " + " | ".join(row) + " |")
    total = ["**Итого**", ""]
    for key in ("l", "r"):
        total += [f"**{hmm(grand[key][0])}**", f"**{tokens_text(grand[key][1])}**",
                  f"**{cents_text(grand[key][2])}**"]
    lines.append("| " + " | ".join(total) + " |")
    return lines, starred


def total_line(name: str, table_cents: int, report_cents: int, cache=None) -> str:
    gap = table_cents - report_cents
    source = (f" (report_run.py read the cached measurement {cache.name}, the table read the transcripts)"
              if cache and cache.is_file() else "")
    return (f"{name}: total by this table vs total by report_run.py: "
            f"{cents_text(table_cents)} vs {cents_text(report_cents)}, gap {'-' if gap < 0 else ''}"
            f"{cents_text(abs(gap))}{source}")


def notes_line(name: str, run: dict) -> str:
    n = run["notes"]
    text = (f"{name}: {n['sessions']} sessions, {n['unplaced']} under \"{NO_STAGE}\" (stage or role "
            f"could not be told); {compare.unpriced_line(run['unpriced'])}")
    if n["not_owned"]:
        text += f"; {n['not_owned']} transcript(s) of the folder not owned by the run's journal, not counted"
    if n["no_transcript"]:
        text += f"; {n['no_transcript']} journal session(s) with no transcript, placed with time only"
    return text


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--left", default=paths.DEFAULT_LEFT)
    ap.add_argument("--right", default=paths.DEFAULT_RIGHT)
    ap.add_argument("--ticket", default=paths.TASK)
    ap.add_argument("--role-time", action="store_true",
                    help="also print each role's own time (union of its sessions' intervals)")
    a = ap.parse_args()
    paths.require_args(ap, ("--left", a.left), ("--right", a.right), ("--ticket", a.ticket))
    for name in (a.left, a.right):
        try:
            report_run.copy_folder(name, report_run.COPIES)     # a baseline, else <copy_prefix><name> (B-267)
        except ValueError as err:
            print(err)
            return 2
    caches = {a.left: report_run.cache_for(a.left, ""), a.right: None}
    left, right = collect(a.left, a.ticket), collect(a.right, a.ticket)
    reported = {n: report_run_cents(n, a.ticket, caches[n]) for n in (a.left, a.right)}
    print(f"## Стадии и роли — {a.left} vs {a.right}\n")
    lines, starred = table_lines(left, right, (a.left, a.right), a.role_time)
    print("\n".join(lines) + "\n")
    print("Время стадии — h:mm, `started`→`finished` из pipeline.json (как «Stages by the clock» в "
          "report_run)" + ("; время роли — объединение интервалов её сессий" if a.role_time else "")
          + "; итого времени — сумма стадий; токены — все виды (input, output, cache); цена — по "
          "каталогу report_run.\n")
    if starred:
        print(FOOTNOTE + "\n")
    for name, run in ((a.left, left), (a.right, right)):
        print(notes_line(name, run))
    print()
    for name, run in ((a.left, left), (a.right, right)):
        print(total_line(name, run["cents"], reported[name], caches[name]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
