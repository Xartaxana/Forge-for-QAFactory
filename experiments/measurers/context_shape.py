#!/usr/bin/env python
"""What each role's context is made of, so a saving can be aimed rather than guessed.

Per role, over the role sessions of the named runs:
  base      the cold-start prompt (role file + rules + brief + the host's own layer)
  args      tokens spent on the arguments of tool calls - inline python in a Bash
            heredoc lands here, and it is re-read on every later turn
  results   tokens the tool results brought in
  whole     the part of `results` that came from reading one file whole (>=2500 tok)
  peak      the largest context the role carried on a single turn
  resumes   how many dispatches were resumptions, and what a resumed turn cost
            against a turn of a first dispatch

Money is priced per turn by the turn's own `message.model` through the package's
model-rates.json. A turn the catalogue cannot price (no model, an unknown model, `<synthetic>`
with usage, a rate entry without a key the turn uses) is UNPRICED: `cost()` returns None, the
turn is counted in the printed "unpriced turns" line and left out of every $ figure (FR-41).
"""
from __future__ import annotations
import argparse, collections, json, pathlib, re

import compare
import paths

BASE = paths.BASE
TASK = paths.TASK                   # the runs table's ticket, or None: then --ticket names it
RUNS = dict(paths.BASELINES)        # the runs table's baselines ({} without a table); other names go by copy_folder
WHOLE = 2500          # tokens: a single result this big is a whole-file read
INLINE = re.compile(r"<<'?[A-Z]{2,}'?|python - |python -c|\bcat > ")


def read_session(path):
    turns, order = {}, []
    results, calls = {}, {}
    for line in path.open(encoding="utf-8", errors="replace"):
        try:
            r = json.loads(line)
        except Exception:
            continue
        m = r.get("message") or {}
        if r.get("type") == "assistant":
            u, mid = m.get("usage"), m.get("id")
            if not u or not mid:
                continue
            if mid not in turns:
                cc = u.get("cache_creation") or {}
                w5 = cc.get("ephemeral_5m_input_tokens", 0) or u.get("cache_creation_input_tokens", 0) or 0
                turns[mid] = dict(
                    read=u.get("cache_read_input_tokens", 0), w5=w5,
                    w1=cc.get("ephemeral_1h_input_tokens", 0) or 0,
                    i=u.get("input_tokens", 0), o=u.get("output_tokens", 0), args=0,
                    model=m.get("model"), usage=u)
                order.append(mid)
            for c in m.get("content", []):
                if isinstance(c, dict) and c.get("type") == "tool_use":
                    i = c.get("input") or {}
                    blob = json.dumps(i, ensure_ascii=False)
                    turns[mid]["args"] += len(blob) // 4
                    calls[c["id"]] = dict(name=c.get("name"), inline=bool(INLINE.search(blob)),
                                          arg=str(i.get("command") or i.get("file_path") or "")[:120])
        elif r.get("type") == "user":
            for c in (m.get("content") or []):
                if not isinstance(c, dict) or c.get("type") != "tool_result":
                    continue
                t = c.get("content")
                if isinstance(t, list):
                    t = " ".join(str(x.get("text", "")) for x in t if isinstance(x, dict))
                n = len(str(t or ""))
                tur = r.get("toolUseResult")
                if isinstance(tur, (dict, list)):
                    n = max(n, len(json.dumps(tur, ensure_ascii=False)))
                elif isinstance(tur, str):
                    n = max(n, len(tur))
                tid = c.get("tool_use_id")
                results[tid] = max(results.get(tid, 0), n // 4)
    return [turns[m] for m in order], results, calls


def cost(t, rate=None):
    """Dollars of one turn from its own model's catalogue rate, or None when unpriced."""
    rate = compare.rates() if rate is None else rate
    return compare.price_turn(rate, t.get("model"), t.get("usage"))


def journal_path(run):
    return (BASE / paths.copy_folder(run, RUNS) / "test-harness" / "qa-factory" / "artifacts" / TASK
            / "state" / "driver-runs.jsonl")


def sessions(run):
    j = journal_path(run)
    if not j.exists():
        return []
    out, seen = [], set()
    for line in j.open(encoding="utf-8"):
        try:
            r = json.loads(line)
        except Exception:
            continue
        if r.get("kind") != "role" or not r.get("session_id"):
            continue
        out.append(r)
        seen.add(r["session_id"])
    return out


def main():
    global TASK
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+")
    ap.add_argument("--ticket", default=None, help="the ticket whose artifacts are read (default: task of the runs table)")
    a = ap.parse_args()
    if a.ticket:
        TASK = a.ticket
    paths.require_args(ap, ("--ticket", TASK))
    rate = compare.rates()
    unpriced = 0
    per = collections.defaultdict(lambda: dict(
        turns=0, cost=0.0, base=[], args=0, results=0, whole=0, whole_files=collections.Counter(),
        peak=0, inline=0, dispatches=0, resumed=0, resumed_cost=0.0, resumed_turns=0,
        first_cost=0.0, first_turns=0))
    for run in a.runs:
        if not journal_path(run).is_file():
            print("no driver journal for %s: %s is absent" % (run, journal_path(run)))
            continue
        pd = paths.transcript_dir(BASE / paths.copy_folder(run, RUNS) / "test-harness")
        seen = set()
        for s in sessions(run):
            sid = s["session_id"]
            role = s.get("role")
            row = per[role]
            row["dispatches"] += 1
            if s.get("resumed"):
                row["resumed"] += 1
                row["resumed_cost"] += s.get("total_cost_usd") or 0
                row["resumed_turns"] += s.get("num_turns") or 0
            else:
                row["first_cost"] += s.get("total_cost_usd") or 0
                row["first_turns"] += s.get("num_turns") or 0
            if sid in seen:
                continue
            seen.add(sid)
            p = pd / (sid + ".jsonl")
            if not p.exists():
                continue
            turns, results, calls = read_session(p)
            row["turns"] += len(turns)
            costs = [cost(t, rate) for t in turns]
            unpriced += sum(1 for c in costs if c is None)
            row["cost"] += sum(c for c in costs if c is not None)
            row["args"] += sum(t["args"] for t in turns)
            row["peak"] = max(row["peak"], max((t["read"] for t in turns), default=0))
            for t in turns[:1]:
                b = t["w1"] + t["w5"] + t["i"]
                if b > 5000:
                    row["base"].append(b)
            for tid, n in results.items():
                row["results"] += n
                c = calls.get(tid) or {}
                if n >= WHOLE and c.get("name") == "Read":
                    row["whole"] += n
                    row["whole_files"][pathlib.Path(c.get("arg", "?")).name] += n
            row["inline"] += sum(1 for c in calls.values() if c.get("inline"))
    print("%-22s %4s %6s %7s %7s %7s %7s %7s %6s %6s"
          % ("role", "disp", "turns", "$", "base", "args", "results", "whole", "peak", "inline"))
    for role, r in sorted(per.items(), key=lambda kv: -kv[1]["cost"]):
        base = sum(r["base"]) // len(r["base"]) if r["base"] else 0
        print("%-22s %4d %6d %7.2f %7s %7s %7s %7s %6s %6d"
              % (role, r["dispatches"], r["turns"], r["cost"], f"{base:,}",
                 f"{r['args']:,}", f"{r['results']:,}", f"{r['whole']:,}",
                 f"{r['peak']//1000}K", r["inline"]))
    print("\nresumption: what a resumed turn costs against a first-dispatch turn")
    print("%-22s %5s %8s %8s  %s" % ("role", "resum", "$/turn", "$/turn", "verdict"))
    for role, r in sorted(per.items(), key=lambda kv: -kv[1]["resumed_cost"]):
        if not r["resumed"]:
            continue
        rt = r["resumed_cost"] / r["resumed_turns"] if r["resumed_turns"] else 0
        ft = r["first_cost"] / r["first_turns"] if r["first_turns"] else 0
        v = "resumed turn is %.1fx a fresh one" % (rt / ft) if ft else "-"
        print("%-22s %5d %8.4f %8.4f  %s" % (role, r["resumed"], rt, ft, v))
    print("\nwhole-file reads worth a slice command (top per role)")
    for role, r in sorted(per.items(), key=lambda kv: -kv[1]["whole"]):
        if not r["whole"]:
            continue
        top = ", ".join("%s %s tok" % (k, f"{v:,}") for k, v in r["whole_files"].most_common(3))
        print("  %-22s %7s tok  %s" % (role, f"{r['whole']:,}", top))
    print("\nunpriced turns: %d (no rate for their model in model-rates.json; "
          "left out of every $ above)" % unpriced)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
