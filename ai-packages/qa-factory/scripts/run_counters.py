#!/usr/bin/env python3
"""run_counters.py - the counted reader of ONE run (P1-v N4; AR-12, AR-13, AR-15, AR-23, AR-28).

    python run_counters.py --task <KEY> | --task-root <the story's folder> [--json]

`counters(task_root) -> dict` reads the carriers of one story folder and returns the scoreboard counters of the run: time rows
T1-T10, first pass and rework F1, returns per check G1, gate repairs G2, questions Q1-Q3, brief sizes B1, friction R1r and the
data-quality row U1. It READS ONLY: it writes no file, prints no money, and the driver does not call it (the counters are derived
on demand). Every row is `{"state": "measured" | "unknown" | "n/a", ...}`: an input that is absent gives `unknown` (`n/a` where the
row cannot exist for the run class) with the reason, never 0 and never a crash (FR-41, AR-28).

One road per carrier (AR-13, AR-15): `driver-runs.jsonl`, the questions, the answers, `passed-by-person.jsonl` and
`brief-sizes.jsonl` only through `driver_journal.read_rows_counted` (and `question_rows` / `answer_rows`); timings only through
`driver_timing.report`; friction only through `friction.story_friction`; controller rounds through
`retro_numbers.dispatch_rounds`; the closed tables through `driver_journal.run_record`; times through `driver_journal.parse_ts`.
This file parses no JSON of its own.

Shape of the run record it works from (the CODE at the N1/N2 heads, not an older spec text): a process is `since` (its start) with an
END row that carries `since`, `package`, `config_sha`, `answer_file`, `run_class`, `start_row_written`, `process_code`,
`question_kind`; a fresh single-process run has NO start row, so the END row is the row it works from; a start row with no end
row is a process that was killed. `run_class` is computed once per process and carried by both rows.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import driver_journal as DJ  # noqa: E402
import driver_timing  # noqa: E402

PROCESS = "process"
PASSED_NAME = "passed-by-person.jsonl"
BRIEF_SIZES_NAME = "brief-sizes.jsonl"
RUNS_NAME = DJ.JOURNAL_NAME
STUB_PREFIX = "stub-"                 # the session id the dry-story stub writes (spec 7.9); read only as a safety net
SIMULATED = ("dry", "smoke")          # run classes whose roles are stubs: transcript rows cannot exist (spec 7.9)
NO_KIND = "unknown"                   # the name a row with no kind is counted under, never dropped
UNCLASSIFIED = "unclassified"
FRICTION_ROLE_KEYS = ("turns", "fric_turns", "turn_share", "kinds", "sessions", "sessions_unreachable", "dispatches", "reachable")
FRICTION_TOTAL_KEYS = ("turns", "fric_turns", "turn_share")


# --------------------------------------------------------------------------------------- small helpers

def _state(state: str, why: str = "", **fields) -> dict:
    out = {"state": state}
    if why:
        out["why"] = why
    out.update(fields)
    return out


def _unknown(why: str, **fields) -> dict:
    return _state("unknown", why, **fields)


def _number(value):
    """A plain finite non-negative number, or None (a bool, text, NaN, a negative are not seconds)."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value) if value == value and value not in (float("inf"),) and value >= 0 else None


def _naive(value) -> bool:
    """True when `value` is an ISO stamp that names no offset (`parse_ts` reads it as UTC; U1 counts it)."""
    from datetime import datetime
    if not isinstance(value, str):
        return False
    try:
        return datetime.fromisoformat(value.strip().replace("Z", "+00:00").replace("z", "+00:00")).tzinfo is None
    except ValueError:
        return False


def _merge(intervals) -> list:
    out = []
    for start, end in sorted(intervals):
        if out and start <= out[-1][1]:
            out[-1][1] = max(out[-1][1], end)
        else:
            out.append([start, end])
    return out


def _length(merged) -> float:
    return sum(end - start for start, end in merged)


def _secs(value) -> float:
    return round(value, 2)


def _pct(part, whole):
    return round(100.0 * part / whole, 1) if whole else None


def _carrier(task_root: Path, name: str, rows_of=None) -> tuple:
    """(present, rows, bad_lines) of one state carrier, read through the counted reader."""
    path = task_root / "state" / name
    rows, bad = (rows_of(task_root) if rows_of else DJ.read_rows_counted(path))
    return path.is_file(), rows, bad


# --------------------------------------------------------------------------------------- process windows

def _windows(rows: list) -> tuple:
    """([window], classes): one window per process (rows grouped by `since`), sorted by start. A window is
    {"start": dt|None, "end": dt|None, "end_row": bool, "start_row": bool, "package", "config_sha", "answer_file", "question_kind"}.
    The identifying keys come from the END row when there is one, else the start row. `classes` is every run class named by any
    process row (start or end)."""
    groups, order, classes = {}, [], []
    for row in rows:
        if row.get("kind") != PROCESS or row.get("event") not in ("start", "end"):
            continue
        since = row.get("since")
        key = since.strip() if isinstance(since, str) and since.strip() else f"{row.get('event')}@{row.get('ts')}"
        if key not in groups:
            groups[key] = {}
            order.append(key)
        groups[key][row["event"]] = row
        if isinstance(row.get("run_class"), str):
            classes.append(row["run_class"])
    windows = []
    for key in order:
        group = groups[key]
        start_row, end_row = group.get("start"), group.get("end")
        source = end_row or start_row
        start = DJ.parse_ts(key) or (DJ.parse_ts(start_row.get("ts")) if start_row else None)

        def pick(field, source=source, start_row=start_row):
            value = source.get(field)
            return value if value is not None or start_row is None else start_row.get(field)
        windows.append({"start": start, "end": DJ.parse_ts(end_row.get("ts")) if end_row else None,
                        "end_row": end_row is not None, "start_row": start_row is not None,
                        "package": pick("package"), "config_sha": pick("config_sha"), "answer_file": pick("answer_file"),
                        "question_kind": end_row.get("question_kind") if end_row else None,
                        "process_code": end_row.get("process_code") if end_row else None})
    windows.sort(key=lambda w: (w["start"] is None, w["start"] or 0))
    return windows, classes


def _run_class(classes: list, role_rows: list) -> tuple:
    """(class, why): from the process rows. None named -> unknown (never live by default); two different values -> mixed;
    one -> that value; a `live` run whose role sessions start `stub-` -> unknown (the dry-story safety net)."""
    if not classes:
        return "unknown", "no process row names a run class (the record predates the process rows)"
    if len(set(classes)) > 1:
        return "mixed", "the process rows name different run classes: " + ", ".join(sorted(set(classes)))
    only = classes[0]
    stubs = [r for r in role_rows if isinstance(r.get("session_id"), str) and r["session_id"].startswith(STUB_PREFIX)]
    if only == DJ.CLASS_LIVE and stubs:
        return "unknown", "stub sessions in a run marked live"
    return only, ""


def _open_calls(rows: list) -> list:
    """The `launched` rows with no outcome row after them, matched the way `driver_runner.journal_run` and `collect_stall` match
    (launched key = dispatch_id or call; outcome key = dispatch or kind, an outcome row carries is_error / exit_code / infra)."""
    pending = {}
    for row in rows:
        if row.get("kind") == "launched":
            key = str(row.get("dispatch_id") or row.get("call") or "")
            pending.setdefault(key, []).append(row)
        elif any(k in row for k in ("is_error", "exit_code", "infra")):
            key = str(row.get("dispatch") or row.get("kind") or "")
            if pending.get(key):
                pending[key].pop(0)
    return [r for waiting in pending.values() for r in waiting]


# --------------------------------------------------------------------------------------- the rows

def _time_rows(rows, windows, all_stamps, role_rows, conductor_rows, cut) -> dict:
    """T1-T3, T6, T7, T8 from the driver journal and the process windows."""
    out = {}
    # killed windows end at the last record of any carrier inside them (7.1)
    for index, window in enumerate(windows):
        if window["end"] is None and window["start"] is not None:
            following = windows[index + 1]["start"] if index + 1 < len(windows) else None
            inside = [t for t in all_stamps if t >= window["start"] and (following is None or t < following)]
            window["end"] = max(inside) if inside else window["start"]
    timed = [w for w in windows if w["start"] is not None]
    if timed and all_stamps is not None:
        first = min(w["start"] for w in timed)
        last = max([w["end"] for w in timed] + list(all_stamps))
        out["T1"] = _state("measured", basis="process rows", first=first.isoformat(), last=last.isoformat(),
                           wall_s=_secs((last - first).total_seconds()), processes=len(timed),
                           driver_s=_secs(sum((w["end"] - w["start"]).total_seconds() for w in timed)),
                           end_recorded=all(w["end_row"] for w in timed) and not cut,
                           end_note="" if all(w["end_row"] for w in timed) and not cut else "end not recorded")
    elif all_stamps:
        starts = [m for m in (DJ.parse_ts(r.get("started_at")) for r in rows if r.get("kind") == "launched") if m is not None]
        first, last = min(starts or all_stamps), max(all_stamps)
        out["T1"] = _state("measured", basis="fallback: first launched start to last record (no process rows)",
                           first=first.isoformat(), last=last.isoformat(), wall_s=_secs((last - first).total_seconds()),
                           processes=0, end_recorded=False, end_note="end not recorded")
    else:
        out["T1"] = _unknown("no row of any carrier has a readable time")

    def spans(rs):
        got, missing = [], 0
        for r in rs:
            end, wall = DJ.parse_ts(r.get("ts")), _number(r.get("wall_ms"))
            if end is None or wall is None:
                missing += 1
            else:
                got.append((end.timestamp() - wall / 1000.0, end.timestamp(), r))
        return got, missing

    role_spans, role_missing = spans(role_rows)
    cond_spans, cond_missing = spans(conductor_rows)
    role_union = _merge([(s, e) for s, e, _r in role_spans])
    per_session, calls_by_session = {}, {}
    for s, e, r in role_spans:
        sid = str(r.get("session_id") or "")
        per_session[sid] = per_session.get(sid, 0.0) + (e - s)
        calls_by_session[sid] = calls_by_session.get(sid, 0) + 1
    out["T2"] = _state("measured", union_s=_secs(_length(role_union)), sum_s=_secs(sum(per_session.values())),
                       calls=len(role_rows), calls_wall_unknown=role_missing,
                       per_session_s={sid: _secs(v) for sid, v in sorted(per_session.items())})
    cond_union = _merge([(s, e) for s, e, _r in cond_spans])
    both = _merge([(s, e) for s, e, _r in role_spans] + [(s, e) for s, e, _r in cond_spans])
    out["T3"] = _state("measured", not_overlapped_s=_secs(_length(both) - _length(role_union)),
                       union_s=_secs(_length(cond_union)), calls=len(conductor_rows), calls_wall_unknown=cond_missing)
    # T8: hung calls (wall exceeds the CLI's own duration by more than the one threshold)
    hung, excess, unmeasurable = 0, 0.0, 0
    for r in role_rows + conductor_rows:
        wall, dur = _number(r.get("wall_ms")), _number(r.get("duration_ms"))
        if wall is None or dur is None:
            unmeasurable += 1
        elif wall - dur > driver_timing.WALL_NOTE_OVER_MS:
            hung += 1
            excess += (wall - dur) / 1000.0
    out["T8"] = _state("measured", n=hung, excess_s=_secs(excess), unmeasurable=unmeasurable,
                       threshold_ms=driver_timing.WALL_NOTE_OVER_MS)
    # T6 / T7: the gaps between processes, each in exactly one class (never split)
    if not timed:
        why = "the record predates the process rows: no window to read a gap from"
        out["T6"], out["T7"] = _unknown(why), _unknown(why)
        return out
    gaps = []
    for before, after in zip(timed, timed[1:]):
        seconds = _secs(max(0.0, (after["start"] - before["end"]).total_seconds()))
        if before["package"] and after["package"] and before["package"] != after["package"]:
            kind, why = "operator", "the package changed between the processes"
        elif before["config_sha"] and after["config_sha"] and before["config_sha"] != after["config_sha"]:
            kind, why = "operator", "the project config changed between the processes"
        elif not before["end_row"]:
            kind, why = "not_recorded", "the earlier process left no end row"
        elif isinstance(before["question_kind"], str) and before["question_kind"]:
            if after["answer_file"] is True:
                kind, why = "person", "a question was posted and the next process started with an answer file"
            elif after["answer_file"] is False:
                kind, why = "operator", "the next process started with no answer file after a posted question"
            else:
                kind, why = "not_recorded", "whether the next process had an answer file is not recorded"
        else:
            kind, why = "operator", "the process ended with no question posted and a new one started"
        gaps.append({"class": kind, "seconds": seconds, "why": why, "question_kind": before["question_kind"]})
    person = [g for g in gaps if g["class"] == "person"]
    by_kind = {}
    for g in person:
        slot = by_kind.setdefault(str(g["question_kind"]), {"n": 0, "seconds": 0.0})
        slot["n"] += 1
        slot["seconds"] = _secs(slot["seconds"] + g["seconds"])
    last_window = timed[-1]
    open_kind = last_window["question_kind"] if last_window["end_row"] and last_window["question_kind"] else None
    out["T6"] = _state("measured", n=len(person), seconds=_secs(sum(g["seconds"] for g in person)), by_kind=by_kind,
                       open_question_kind=open_kind)
    operator = [g for g in gaps if g["class"] == "operator"]
    cause = {}
    for g in operator:
        slot = cause.setdefault(g["why"], {"n": 0, "seconds": 0.0})
        slot["n"] += 1
        slot["seconds"] = _secs(slot["seconds"] + g["seconds"])
    unclassed = [g for g in gaps if g["class"] == "not_recorded"]
    out["T7"] = _state("measured", n=len(operator), seconds=_secs(sum(g["seconds"] for g in operator)), by_cause=cause,
                       not_recorded={"n": len(unclassed), "seconds": _secs(sum(g["seconds"] for g in unclassed)),
                                     "label": "waiting, cause not recorded"},
                       inside_a_gap="unknown: decision time and patch time are not split")
    return out


def _resume_rows(role_rows: list, table: list) -> dict:
    """F1 and G1 from the role rows. A resumed row that repeats the previous attempt of the SAME call (same key, `retry` one
    higher, same `resume_kind` and `checks`) is a RETRY of that resume, counted once more in `retries`, not as a second resume."""
    last, counted, retries = {}, [], 0
    for row in role_rows:
        key = str(row.get("dispatch") or "")
        previous = last.get(key)
        retry = row.get("retry")
        if retry is not None and not isinstance(retry, bool) and isinstance(retry, int) and retry >= 1:
            retries += 1
        duplicate = bool(row.get("resumed") and previous is not None and previous.get("resumed")
                         and isinstance(retry, int) and not isinstance(retry, bool) and isinstance(previous.get("retry"), int)
                         and retry == previous["retry"] + 1 and retry >= 1
                         and row.get("resume_kind") == previous.get("resume_kind") and row.get("checks") == previous.get("checks"))
        last[key] = row
        if row.get("resumed") and not duplicate:
            counted.append(row)
    first_pass = [r for r in role_rows if not r.get("resumed")]

    def seconds(rs):
        walls = [_number(r.get("wall_ms")) for r in rs]
        return _secs(sum(w for w in walls if w is not None) / 1000.0), sum(1 for w in walls if w is None)
    by_kind, kind_not_recorded, kind_rows = {}, 0, []
    for row in counted:
        if "resume_kind" not in row:
            kind_not_recorded += 1
            continue
        token = row["resume_kind"] if isinstance(row["resume_kind"], str) and row["resume_kind"] in table else UNCLASSIFIED
        kind_rows.append((token, row))
    for token in sorted({t for t, _r in kind_rows}):
        rs = [r for t, r in kind_rows if t == token]
        by_kind[token] = {"calls": len(rs), "role_s": seconds(rs)[0], "wall_unknown": seconds(rs)[1]}
    fp_s, fp_missing = seconds(first_pass)
    rs_s, rs_missing = seconds(counted)
    f1 = _state("measured", calls=len(role_rows), first_pass={"calls": len(first_pass), "role_s": fp_s, "wall_unknown": fp_missing},
                resumed={"calls": len(counted), "role_s": rs_s, "wall_unknown": rs_missing, "by_kind": by_kind,
                         "kind_not_recorded": kind_not_recorded},
                retries=retries)
    # G1: one return per check id named by a counted resume; its role seconds in full to each id (`shared`)
    with_checks = [r for r in counted if "checks" in r]
    if counted and not with_checks and any("resume_kind" not in r for r in counted):
        return {"F1": f1, "G1": _unknown("the resumed rows predate the checks writer", resumed_calls=len(counted))}
    returns, unknown_rows = {}, 0
    for row in with_checks:
        ids = row["checks"]
        if not isinstance(ids, list) or not ids or not all(isinstance(i, str) and i for i in ids):
            ids, unknown_rows = ["unknown"], unknown_rows + 1
        counts = row.get("checks_n") if isinstance(row.get("checks_n"), dict) else {}
        wall = _number(row.get("wall_ms"))
        for ident in sorted(set(ids)):
            slot = returns.setdefault(ident, {"returns": 0, "role_s_shared": 0.0, "findings": 0, "wall_unknown": 0})
            slot["returns"] += 1
            if wall is None:
                slot["wall_unknown"] += 1
            else:
                slot["role_s_shared"] = _secs(slot["role_s_shared"] + wall / 1000.0)
            n = counts.get(ident)
            slot["findings"] += n if isinstance(n, int) and not isinstance(n, bool) else 0
    total_s, total_missing = seconds(with_checks)
    ids_total = sum(v["returns"] for v in returns.values())
    g1 = _state("measured", by_check=returns, resumed_calls_with_checks=len(with_checks), resumed_s_total=total_s,
                resumed_s_total_wall_unknown=total_missing, shared_note="role_s_shared is attributed in full to each check "
                "of a call: the per-check seconds do not sum to the total",
                resumed_without_checks=len(counted) - len(with_checks),
                unknown_check={"returns": returns.get("unknown", {}).get("returns", 0), "of": ids_total,
                               "share": _pct(returns.get("unknown", {}).get("returns", 0), ids_total), "malformed_rows": unknown_rows})
    return {"F1": f1, "G1": g1}


def _controller_rounds(task_root: Path) -> dict:
    try:
        import retro_numbers
        rounds = retro_numbers.dispatch_rounds(task_root)
    except Exception as exc:  # noqa: BLE001 - one unreadable carrier never takes the counters down
        return _unknown(f"the controller records could not be read ({type(exc).__name__})")
    if not rounds:
        return _unknown("no controller dispatch records")
    return _state("measured", records=len(rounds), rework=sum(1 for r in rounds if r.get("rework") is True),
                  rework_not_established=sum(1 for r in rounds if r.get("rework") is None))


def _friction(task_root: Path, run_class: str) -> dict:
    """R1r: turn shares and counts only, by a whitelist of keys (no money key can be copied from `story_friction`)."""
    if run_class in SIMULATED:
        return _state("n/a", "stub roles: no transcript exists for a dry or smoke run")
    try:
        import friction
        import hooklib
        base = task_root.parent.parent
        cfg = hooklib.read_json(base / "config.json", {}, errors=Exception)
        data = friction.story_friction(task_root, base, base.parent, (cfg or {}).get("cost") or {})
    except Exception as exc:  # noqa: BLE001
        return _unknown(f"{type(exc).__name__}: {exc}")
    status = data.get("status") if isinstance(data, dict) else None
    if status not in ("ok", "partial"):
        return _unknown(str((data or {}).get("reason") or "friction could not be measured"))
    roles = {}
    for name, row in sorted((data.get("roles") or {}).items()):
        kept = {k: row[k] for k in FRICTION_ROLE_KEYS if k in row}
        kept["helpers_n"] = len(row.get("helpers") or [])
        roles[name] = kept
    total = {k: (data.get("total") or {})[k] for k in FRICTION_TOTAL_KEYS if k in (data.get("total") or {})}
    return _state("measured", friction_status=status, reason=data.get("reason") or "", sessions=data.get("sessions"),
                  sessions_unreachable=data.get("sessions_unreachable"), roles=roles, total=total)


def _questions(task_root, runs_present, windows) -> dict:
    out = {}
    ran = bool(windows)
    q_present, questions, q_bad = _carrier(task_root, DJ.QUESTIONS_NAME, DJ.question_rows)
    a_present, answers, a_bad = _carrier(task_root, DJ.ANSWERS_NAME, DJ.answer_rows)
    p_present, passed, p_bad = _carrier(task_root, PASSED_NAME)
    bad = {"questions": q_bad, "answers": a_bad, "passed_by_person": p_bad}
    if q_present or ran:
        by_kind, by_stage = {}, {}
        for r in questions:
            kind, stage = str(r.get("kind") or NO_KIND), str(r.get("stage") or NO_KIND)
            by_kind[kind] = by_kind.get(kind, 0) + 1
            by_stage[stage] = by_stage.get(stage, 0) + 1
        out["Q1"] = _state("measured", n=len(questions), by_kind=dict(sorted(by_kind.items())), by_stage=dict(sorted(by_stage.items())))
    else:
        out["Q1"] = _unknown("no question record, and no process row proves the driver ran")
    if p_present or ran:
        out["Q2"] = _state("measured", n=len(passed))
    else:
        out["Q2"] = _unknown("no record of gates passed by the person's word, and no process row proves the driver ran")
    if a_present or ran:
        seen, repeats, no_sha = set(), {}, 0
        for r in answers:
            sha = r.get("question_sha")
            if not isinstance(sha, str) or not sha:
                no_sha += 1
                continue
            if sha in seen:
                kind = str(r.get("kind") or NO_KIND)
                repeats[kind] = repeats.get(kind, 0) + 1
            seen.add(sha)
        out["Q3"] = _state("measured", n=sum(repeats.values()), by_kind=dict(sorted(repeats.items())), answers=len(answers),
                           answers_without_sha=no_sha)
    else:
        out["Q3"] = _unknown("no answer record, and no process row proves the driver ran")
    return out, bad


def _briefs(task_root) -> tuple:
    present, rows, bad = _carrier(task_root, BRIEF_SIZES_NAME)
    if not present:
        return _unknown("no brief-sizes record (the record predates its writer, or no brief was dispatched)"), bad
    per_role, unreadable = {}, 0
    for r in rows:
        size, ceiling = _number(r.get("budget_bytes")), _number(r.get("ceiling"))
        if size is None or ceiling is None:
            unreadable += 1
            continue
        slot = per_role.setdefault(str(r.get("role") or NO_KIND), {"n": 0, "over": 0, "sum": 0.0, "max": 0.0})
        slot["n"] += 1
        slot["over"] += 1 if size > ceiling else 0
        slot["sum"] += size
        slot["max"] = max(slot["max"], size)
    roles = {name: {"n": s["n"], "over": s["over"], "mean_budget_bytes": round(s["sum"] / s["n"], 1), "max_budget_bytes": int(s["max"])}
             for name, s in sorted(per_role.items())}
    return _state("measured", n=sum(s["n"] for s in per_role.values()), over=sum(s["over"] for s in per_role.values()),
                  unreadable_rows=unreadable, by_role=roles), bad


# --------------------------------------------------------------------------------------- the one function

def counters(task_root) -> dict:
    """The counters of one run (module note). Writes nothing; never raises on a missing or damaged carrier."""
    task_root = Path(task_root).resolve()
    notes: list = []
    runs_present, rows, runs_bad = _carrier(task_root, RUNS_NAME)
    windows, classes = _windows(rows)
    role_rows = [r for r in rows if r.get("kind") == "role"]
    conductor_rows = [r for r in rows if r.get("kind") == "conductor"]
    table, note = DJ.run_record()
    if note:
        notes.append(note)
    names = table.get("resume_kinds")
    kinds_table = [n for n in names if isinstance(n, str)] if isinstance(names, list) else []
    run_class, class_why = _run_class(classes, role_rows)
    questions, qbad = _questions(task_root, runs_present, windows)
    briefs, bbad = _briefs(task_root)
    cut = _open_calls(rows)
    stamps = [m for m in (DJ.parse_ts(r.get("ts")) for r in rows) if m is not None]
    for name in (DJ.QUESTIONS_NAME, DJ.ANSWERS_NAME, BRIEF_SIZES_NAME):
        extra = DJ.read_rows_counted(task_root / "state" / name)[0]
        stamps += [m for m in (DJ.parse_ts(r.get("ts")) for r in extra) if m is not None]
    out = {"task": task_root.name,
           "run": _state("measured" if run_class not in ("unknown", "mixed") else "unknown", class_why,
                         run_class=run_class, processes=len(windows), processes_without_end=sum(1 for w in windows if not w["end_row"]),
                         driver_journal_present=runs_present)}
    if not runs_present:
        why = "this story has no driver journal (state/driver-runs.jsonl)"
        for key in ("T1", "T2", "T3", "T6", "T7", "T8", "F1", "G1", "G2"):
            out[key] = _unknown(why)
    else:
        out.update(_time_rows(rows, windows, stamps, role_rows, conductor_rows, cut))
        out["T1"]["cut_calls"] = [{"call": str(r.get("dispatch_id") or r.get("call") or ""), "started_at": r.get("started_at"),
                                   "wall_s": None, "wall": "unknown"} for r in cut]
        out.update(_resume_rows(role_rows, kinds_table))
        out["F1"]["controller_rounds"] = _controller_rounds(task_root)
        repairs = [r for r in rows if r.get("kind") == "gate_repair"]
        by_gate, moves = {}, 0
        for r in repairs:
            by_gate[str(r.get("gate") or NO_KIND)] = by_gate.get(str(r.get("gate") or NO_KIND), 0) + 1
            m = r.get("moves")
            moves += len(m) if isinstance(m, (list, tuple)) else (int(m) if isinstance(m, int) and not isinstance(m, bool) and m >= 0 else 0)
        out["G2"] = _state("measured", n=len(repairs), by_gate=dict(sorted(by_gate.items())), moves=moves)
    timing = driver_timing.report(task_root)
    if timing.get("timed"):
        out["T4"] = _state("measured", step_totals=timing["step_totals"], straddling_a_launch=timing["straddling_a_launch"])
        out["T5"] = _state("measured", unattributed_s=_secs(sum(h["unattributed_s"] for h in timing["hops"])), hops=len(timing["hops"]),
                           outside_hops="not computed: time inside a process window outside any hop is not split here")
    else:
        out["T4"] = _unknown(timing.get("text") or "no timings recorded")
        out["T5"] = _unknown(timing.get("text") or "no timings recorded")
    if run_class in SIMULATED:
        out["T9"] = out["T10"] = _state("n/a", "stub roles: no transcript exists for a dry or smoke run")
    else:
        why = "bookkeeping and refused-call time come from the roles' transcripts (friction.call_spans, node N4b), not read here"
        out["T9"], out["T10"] = _unknown(why), _unknown(why)
    out.update(questions)
    out["B1"] = briefs
    out["R1r"] = _friction(task_root, run_class)
    out["U1"] = _quality(rows, runs_bad, qbad, bbad, out, timing, run_class, class_why, role_rows, notes)
    return out


def _quality(rows, runs_bad, qbad, bbad, out, timing, run_class, class_why, role_rows, notes) -> dict:
    """U1: what the counters could not trust, by carrier. Lines are plain statements for the reader of the scoreboard."""
    naive = sum(1 for r in rows if _naive(r.get("ts")))
    no_kind = sum(1 for r in rows if not (isinstance(r.get("kind"), str) and r["kind"].strip()))
    f1, g1 = out.get("F1", {}), out.get("G1", {})
    unclassified = (f1.get("resumed", {}).get("by_kind", {}).get(UNCLASSIFIED, {}).get("calls", 0)) if f1.get("state") == "measured" else 0
    unknown_check = g1.get("unknown_check") if g1.get("state") == "measured" else None
    stubs = sum(1 for r in role_rows if isinstance(r.get("session_id"), str) and r["session_id"].startswith(STUB_PREFIX))
    bad = {"driver_runs": runs_bad, **qbad, "brief_sizes": bbad, "timings": len(timing.get("problems") or [])}
    lines = list(notes)
    for name, count in bad.items():
        if count:
            lines.append(f"{name}: {count} line(s) left out as unreadable")
    if naive:
        lines.append(f"{naive} row(s) carry a time with no offset (read as UTC)")
    if no_kind:
        lines.append(f"{no_kind} row(s) of the driver journal carry no kind")
    if unclassified:
        lines.append(f"{unclassified} resumed call(s) carry the `unclassified` resume kind")
    if class_why and run_class in ("unknown", "mixed"):
        lines.append(class_why)
    return _state("measured", bad_lines=bad, naive_timestamps=naive, rows_without_kind=no_kind, unclassified_resume_kinds=unclassified,
                  unknown_check_share=unknown_check, stub_sessions=stubs, timing_problems=list(timing.get("problems") or []), lines=lines)


def render(data: dict) -> str:
    lines = [f"run counters of {data['task']}: run class {data['run'].get('run_class')}"]
    for key in sorted(k for k in data if isinstance(data[k], dict) and "state" in data[k]):
        row = data[key]
        lines.append(f"{key}: {row['state']}" + (f" ({row['why']})" if row.get("why") else ""))
    lines += [f"U1: {line}" for line in data["U1"].get("lines", [])]
    return "\n".join(lines)


def cli_main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--task", help="the story's key (the name of its folder under the artifact root)")
    parser.add_argument("--task-root", help="the story's folder, qa-factory/artifacts/<KEY>")
    parser.add_argument("--json", action="store_true", help="the whole answer as JSON")
    import hooklib
    args = hooklib.exact_options(parser).parse_args(argv)
    task_root = hooklib.story_cli("run_counters.py", key=args.task, root=args.task_root)
    data = counters(task_root)
    print(json.dumps(data, indent=2, ensure_ascii=False) if args.json else render(data))
    return 0


if __name__ == "__main__":
    sys.exit(cli_main())
