"""Cost and quality of one factory run, from its Claude Code transcripts and its artifacts.

    python experiments/measurers/compare.py --project <runs base>/<copy>/test-harness --ticket <TICKET>
    python compare.py --project ... --ticket ... --json > run.json

Cost: every request's `usage` in the session transcript and the subagent transcripts of that
project, priced with the plugin's model-rates.json (API list price; on a subscription this is
a comparable number, not a bill). Quality: counts from the story artifacts (register rows,
plan rows and dispositions, cases, critic rounds and unreviewed rows, manifest instances and
unresolved rows, run report, triage verdicts, bugs, ledger states) plus the judge's own bill.
"""
import argparse
import collections
import glob
import json
import os
import re
import sys
from pathlib import Path

import paths

RATES = paths.RATES
SCRIPTS = paths.SCRIPTS


def verdict_word(ledger):
    """The ledger's delivery verdict WORD (`yes`, `after_checks`, `no`; `unknown` when it disagrees with its own bool; None when
    there is no ledger), through the package's one reader - never `bool(delivery_ready)` and never the field as it stands
    (t-305 N8, FR-28: a measurer that reads the truthiness of a three-valued word counts `after_checks` as `no`)."""
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    import delivery_verdict
    return delivery_verdict.word_of(ledger)


def rates() -> dict:
    out = {}
    for e in json.loads(RATES.read_text(encoding="utf-8"))["entries"]:
        for n in [e["model_id"]] + e.get("aliases", []):
            out[n] = e["rates"]
    return out


def _tokens(u):
    """(rate key, token count) for every kind of token one usage block carries."""
    cc = u.get("cache_creation") or {}
    w5, w1 = cc.get("ephemeral_5m_input_tokens"), cc.get("ephemeral_1h_input_tokens")
    if w5 is None and w1 is None:
        w5, w1 = u.get("cache_creation_input_tokens", 0), 0
    return (("input", u.get("input_tokens", 0)), ("output", u.get("output_tokens", 0)),
            ("cache_read", u.get("cache_read_input_tokens", 0)),
            ("cache_write_5m", w5 or 0), ("cache_write_1h", w1 or 0))


def price(rate, model, u):
    """Dollars for one request, or None when the catalogue cannot price it: an unknown model, or an
    entry that lacks the rate of a token kind this request actually used (a KeyError here once
    took a whole measurement down for a catalogue row that simply had no cache-write price;
    FR-41: an unknown is None, never a zero and never a crash)."""
    r = rate.get(model)
    if not r:
        return None
    total = 0
    for key, count in _tokens(u):
        if not count:
            continue
        if key not in r:
            return None
        total += count * r[key]
    return total / 1e6


def price_turn(rate, model, u):
    """`price`, except that a turn which used no tokens costs 0 whatever its model says: a
    `<synthetic>` marker turn has no usage and nothing to price."""
    if not any(count for _, count in _tokens(u or {})):
        return 0.0
    return price(rate, model, u or {})


def price_seen(rate: dict, seen) -> tuple:
    """(dollars, unpriced requests) of the unique requests `seen` ({id: (model, usage)}). A request
    the catalogue cannot price is COUNTED and left out of the dollars: it is never a $0 stated as
    a fact (FR-41). Its own function because compare.scan and report_to_gate.scan_until both
    turned `price(...) or 0` into the run's headline number and neither said so."""
    cost, unpriced = 0.0, 0
    for model, usage in seen.values():
        one = price_turn(rate, model, usage)
        if one is None:
            unpriced += 1
        else:
            cost += one
    return cost, unpriced


def is_empty_marker(model, usage) -> bool:
    """A `<synthetic>` turn that used no tokens: a marker, not a request. One that DID use tokens is
    a request like any other and is priced (or counted unpriced) by its model."""
    return model == "<synthetic>" and not any(count for _, count in _tokens(usage or {}))


def unpriced_line(count) -> str:
    """The line every printed money figure carries, so that a $0 is never read as a price."""
    return f"unpriced requests: {count} (excluded from $)"


def transcript_dir(project: Path) -> Path:
    return paths.transcript_dir(project)


def case_files(tree: Path) -> list:
    """The case files under a run's case tree, by what a case IS and not by what it is called: a
    `*.md` whose front matter declares `id:` equal to its own file stem. The tree also holds the
    critic's findings, and the store's versions under `cases/` and `case-versions/`, which are
    copies of a case, not cases. `rglob("TC-*.md")` counted 0 for a run whose cases use the
    project's own id form (PROJ-1_TC_001.md); the id form is not ours to fix (FR-13)."""
    if not tree or not Path(tree).is_dir():
        return []
    found = []
    for path in sorted(Path(tree).rglob("*.md")):
        parts = path.relative_to(tree).parts[:-1]
        if "cases" in parts or "case-versions" in parts or path.name.startswith("critic-findings"):
            continue
        try:
            text = path.read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            continue
        lines = text.splitlines()
        if not lines or lines[0].strip() != "---":
            continue
        for line in lines[1:]:
            if line.strip() == "---":
                break
            m = re.match(r"id:\s*(.*?)\s*$", line)
            if m and m.group(1).strip("'\"") == path.stem:
                found.append(path)
                break
    return found


def scan(path: Path, rate: dict) -> dict:
    seen, role, tools = {}, None, collections.Counter()
    first = last = None
    for line in path.open(encoding="utf-8"):
        try:
            o = json.loads(line)
        except ValueError:
            continue
        ts = o.get("timestamp")
        if ts:
            first, last = first or ts, ts
        m = o.get("message") or {}
        if o.get("type") == "user" and role is None:
            c = m.get("content")
            txt = c if isinstance(c, str) else " ".join(x.get("text", "") for x in c if isinstance(x, dict))
            mm = re.search(r"qa-[a-z\-]+", txt or "")
            role = mm.group(0) if mm else "?"
        if o.get("type") == "assistant" and m.get("usage") and not is_empty_marker(m.get("model"), m["usage"]):
            seen[m.get("id") or o.get("uuid")] = (m.get("model"), m["usage"])
            for b in m.get("content", []):
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    tools[b["name"]] += 1
    cost, unpriced = price_seen(rate, seen)
    out_tokens = sum(u.get("output_tokens", 0) for _, u in seen.values())
    return {"role": role, "requests": len(seen), "cost_usd": round(cost, 2), "unpriced_requests": unpriced,
            "output_tokens": out_tokens,
            "tools": dict(tools), "first": first, "last": last}


def cost_report(project: Path, ticket: str) -> dict:
    rate = rates()
    root = transcript_dir(project)
    sessions, by_role = [], collections.defaultdict(
        lambda: {"requests": 0, "cost_usd": 0.0, "unpriced_requests": 0, "dispatches": 0})
    for main in sorted(glob.glob(str(root / "*.jsonl")), key=os.path.getmtime):
        sid = Path(main).stem
        if ticket and ticket not in Path(main).read_text(encoding="utf-8", errors="replace"):
            continue
        orch = scan(Path(main), rate)
        orch["role"] = "orchestrator"
        rows = [orch]
        for sub in sorted(glob.glob(str(root / sid / "subagents" / "*.jsonl")), key=os.path.getmtime):
            rows.append(scan(Path(sub), rate))
        for r in rows:
            by_role[r["role"]]["requests"] += r["requests"]
            by_role[r["role"]]["cost_usd"] = round(by_role[r["role"]]["cost_usd"] + r["cost_usd"], 2)
            by_role[r["role"]]["unpriced_requests"] += r["unpriced_requests"]
            by_role[r["role"]]["dispatches"] += 1
        sessions.append({"session": sid, "rows": rows, "cost_usd": round(sum(r["cost_usd"] for r in rows), 2),
                         "unpriced_requests": sum(r["unpriced_requests"] for r in rows)})
    total = round(sum(s["cost_usd"] for s in sessions), 2)
    return {"transcripts": str(root), "sessions": sessions, "by_role": dict(by_role), "total_usd": total,
            "unpriced_requests": sum(s["unpriced_requests"] for s in sessions)}


def _json(path: Path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return default


def quality_report(project: Path, ticket: str) -> dict:
    task = project / "qa-factory" / "artifacts" / ticket
    work = task / "work"
    q = {"task_root": str(task)}
    reg = work / "requirements-register.md"
    if reg.is_file():
        rows = [l for l in reg.read_text(encoding="utf-8").splitlines() if re.match(r"^\|\s*R-?\d", l)]
        q["register_rows"] = len({l.split("|")[1].strip() for l in rows})
    plan = _json(work / "test-plan.json")
    if plan:
        rows = plan.get("rows", plan) if isinstance(plan, dict) else plan
        q["plan_rows"] = len(rows)
        q["dispositions"] = dict(collections.Counter(r.get("disposition") for r in rows))
        q["levels"] = dict(collections.Counter(r.get("level") for r in rows))
    cases = case_files(work / "test-cases")
    q["cases"] = len(cases)
    q["cases_automated"] = sum(1 for c in cases if re.search(r"^status:\s*Automated", c.read_text(encoding="utf-8"), re.M))
    findings = list((work / "test-cases").rglob("critic-findings.md")) if (work / "test-cases").is_dir() else []
    if findings:
        text = findings[0].read_text(encoding="utf-8")
        m = re.search(r"round:\s*(\d+)", text)
        q["critic_rounds"] = int(m.group(1)) if m else None
        q["critic_unreviewed"] = len(re.findall(r"\|\s*TS-\d+\s*\|[^|]*\|\s*no\s*\|", text))
        v = re.search(r"[Vv]erdict[^:]*:\s*([a-z_]+)", text)
        q["critic_verdict"] = v.group(1) if v else None
    man = _json(work / "automation-manifest.json")
    if man:
        entries = man.get("entries") or man.get("instances") or man.get("tests") or []
        q["manifest_instances"] = len(entries)
        q["manifest_unresolved"] = dict(collections.Counter(str(u.get("reason")) for u in man.get("unresolved", [])))
    rr = _json(work / "run-report.json")
    if rr:
        q["run"] = {"execution_status": rr.get("execution_status"), "totals": rr.get("totals")}
    tri = _json(work / "triage.json")
    if tri:
        items = tri.get("items") or tri.get("verdicts") or tri.get("failures") or []
        q["triage"] = dict(collections.Counter(str(i.get("verdict")) for i in items if isinstance(i, dict)))
    bugs = project / "qa-factory" / "bugs"
    q["bugs"] = len(list(bugs.glob("BUG-*.md"))) if bugs.is_dir() else 0
    ledger = _json(work / "ledger.json")
    if ledger:
        rows = ledger.get("rows") or ledger.get("tests") or []
        q["ledger"] = dict(collections.Counter(str(r.get("state")) for r in rows if isinstance(r, dict)))
        q["delivery_ready"] = verdict_word(ledger)
    pipe = _json(task / "pipeline.json")
    if pipe:
        q["stages"] = {k: v.get("status") for k, v in (pipe.get("stages") or {}).items()}
        q["halts"] = len(pipe.get("halts") or [])
        q["waivers"] = len(pipe.get("stage_overrides") or []) + len(pipe.get("gate_waivers") or [])
    for name in ("judge-sources", "judge-requirements", "judge-plan", "judge-cases", "judge-code", "judge-triage", "judge-bugs"):
        if (work / f"{name}.json").is_file():
            q.setdefault("judge_files", []).append(name)
    sys.path.insert(0, str(SCRIPTS))
    try:
        import judge
        q["judge"] = judge.summary(project, ticket)
    except Exception as exc:
        q["judge"] = {"error": str(exc)}
    q["driver"] = driver_report(task)
    return q


def driver_report(task: Path) -> dict:
    """The driver's own bill: state/driver-runs.jsonl (one line per claude -p) and
    state/conductor.jsonl (one line per refusal handled by the table or the conductor)."""
    runs = task / "state" / "driver-runs.jsonl"
    if not runs.is_file():
        return {}
    by_kind = collections.defaultdict(lambda: {"calls": 0, "turns": 0, "cost_usd": 0.0})
    by_role = collections.defaultdict(lambda: {"calls": 0, "turns": 0, "cost_usd": 0.0})
    for line in runs.read_text(encoding="utf-8").splitlines():
        try:
            o = json.loads(line)
        except ValueError:
            continue
        k = by_kind[o.get("kind") or "?"]
        k["calls"] += 1; k["turns"] += int(o.get("num_turns") or 0); k["cost_usd"] = round(k["cost_usd"] + float(o.get("total_cost_usd") or 0), 2)
        r = by_role[o.get("role") or o.get("kind") or "?"]
        r["calls"] += 1; r["turns"] += int(o.get("num_turns") or 0); r["cost_usd"] = round(r["cost_usd"] + float(o.get("total_cost_usd") or 0), 2)
    out = {"by_kind": dict(by_kind), "by_role": dict(by_role),
           "total_usd": round(sum(v["cost_usd"] for v in by_kind.values()), 2)}
    cond = task / "state" / "conductor.jsonl"
    if cond.is_file():
        actions = collections.Counter()
        for line in cond.read_text(encoding="utf-8").splitlines():
            try:
                actions[json.loads(line).get("action") or "?"] += 1
            except ValueError:
                continue
        out["refusals_by_action"] = dict(actions)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--project", required=True)
    ap.add_argument("--ticket", required=True)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    project = Path(a.project).resolve()
    report = {"cost": cost_report(project, a.ticket), "quality": quality_report(project, a.ticket)}
    if a.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0
    c = report["cost"]
    print(f"transcripts: {c['transcripts']}")
    for s in c["sessions"]:
        print(f"session {s['session'][:8]}  ${s['cost_usd']}")
        for r in s["rows"]:
            print(f"   {r['role']:26} req={r['requests']:4} out={r['output_tokens']:7} ${r['cost_usd']:6.2f}  {(r['first'] or '')[11:16]}-{(r['last'] or '')[11:16]}")
    print("by role:")
    for role, v in sorted(c["by_role"].items(), key=lambda kv: -kv[1]["cost_usd"]):
        print(f"   {role:26} dispatches={v['dispatches']:2} req={v['requests']:4} ${v['cost_usd']}")
    print(f"TOTAL ${c['total_usd']}")
    print(unpriced_line(c["unpriced_requests"]))
    drv = report["quality"].get("driver") or {}
    if drv:
        print(f"driver (claude -p bill, from state/driver-runs.jsonl): ${drv['total_usd']}  by kind: {drv['by_kind']}")
        for role, v in sorted(drv["by_role"].items(), key=lambda kv: -kv[1]["cost_usd"]):
            print(f"   {role:26} calls={v['calls']:2} turns={v['turns']:4} ${v['cost_usd']}")
        print(f"   refusals by action: {drv.get('refusals_by_action')}")
    print("quality:", json.dumps(report["quality"], indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
