"""Quality yardstick per stage: the driver run's artifacts against the baseline runs.
Usage: python experiments/measurers/stage_compare.py s0|s1|s2|s3|s4|s5|all [--run NAME ...] [--ticket <TICKET>]
(NAME: a baseline of the runs table, or a copy `<copy_prefix>NAME`)
Every step the driver does by code must show at least what the LLM runs produced."""
import json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path

import compare
import paths
import report_run

BASE = paths.BASE
RUNS = dict(paths.BASELINES)        # the baselines of the runs table (QA_RUNS_TABLE); {} without one
TASK = paths.TASK                   # the ticket of the runs table, or None: then --ticket names it


EXTRA: list = []        # runs named on the command line with --run (B-267), shown beside the baselines


def folder_of(run):
    """The folder of a run copy: a baseline of RUNS, else `<copy_prefix><run>` (report_run.copy_folder, one rule for
    every tool of this folder)."""
    return report_run.copy_folder(run, RUNS)


def runs():
    """The columns of every ticket table: the baselines in RUNS, then the runs `--run` added."""
    return list(RUNS) + [name for name in EXTRA if name not in RUNS]


def art(run, rel):
    p = BASE / folder_of(run) / "test-harness" / "qa-factory" / "artifacts" / TASK / rel
    return p if p.exists() else None


def load(p):
    return json.load(open(p, encoding="utf-8-sig")) if p else None


def table(rows: dict[str, dict]):
    keys = []
    for r in rows.values():
        for k in r:
            if k not in keys:
                keys.append(k)
    names = list(rows)
    print(f"{'':24} | " + " | ".join(f"{n:22}" for n in names))
    for k in keys:
        print(f"{k:24} | " + " | ".join(f"{str(rows[n].get(k, '—'))[:22]:22}" for n in names))


def s0():
    rows = {}
    for run in runs():
        p = art(run, "work/ticket-snapshot.json") or art(run, "work/ticket-snapshot.md")
        d = load(p)
        if not d:
            rows[run] = {"snapshot": "none"}
            continue
        links = d.get("links") or {}
        rows[run] = {"acceptance_criteria": len(d.get("acceptance_criteria") or []),
                     "comments": len(d.get("comments") or []), "parent": d.get("parent"),
                     "subtasks": len(d.get("subtasks") or []), "description_len": len(d.get("description") or ""),
                     "merge_request": bool(links.get("merge_request")),
                     "issue_links": len(links.get("issue_links") or []), "remote_links": len(links.get("remote_links") or []),
                     "attachments": len(d.get("attachments") or []), "status": d.get("status")}
    print("## S0 — ticket snapshot"); table(rows)


def s1():
    rows = {}
    for run in runs():
        inv = load(art(run, "work/source-inventory.json"))
        r = {}
        if inv:
            src = inv.get("sources") or []
            r["sources"] = len(src)
            pre = (TASK.rsplit("-", 1)[0] + "-") if TASK and "-" in TASK else None  # the task's own key prefix
            short = lambda s: s["canonical_ref"].rsplit("/", 1)[-1].replace(pre, "") if pre else s["canonical_ref"].rsplit("/", 1)[-1]
            r["relevant"] = ",".join(sorted(short(s) for s in src if s.get("relevance") == "relevant"))
            r["excluded"] = ",".join(sorted(short(s) for s in src if s.get("relevance") == "not_relevant"))
            r["read"] = sum(1 for s in src if s.get("status") == "read")
            r["inspected"] = sum(1 for s in src if s.get("inspection_status") == "read")
            r["comments_total"] = sum(((s.get("materials") or {}).get("comments") or {}).get("count") or 0 for s in src)
            r["attachments_total"] = sum(((s.get("materials") or {}).get("attachments") or {}).get("count") or 0 for s in src)
            r["media_total"] = sum(len((((s.get("materials") or {}).get("external_media") or {}).get("items")) or []) for s in src)
            r["human_review"] = sum(1 for s in src if "human_review" in s)
            r["gap_acceptance"] = sum(1 for s in src if "gap_acceptance" in s)
        else:
            r["sources"] = "none"
        cm = load(art(run, "work/context-manifest.json"))
        if cm:
            for k in ("acceptance_criteria", "implementations", "observables", "related", "existing_tests",
                      "conflicts", "requirement_sources", "changed_areas", "known_paths", "unresolved_facts", "constraints"):
                v = cm.get(k)
                r["cm." + k] = len(v) if isinstance(v, (list, dict)) else v
        rows[run] = r
    print("## S1 — source inventory + context manifest"); table(rows)


def count_rows(p, pattern):
    if not p:
        return None
    return len(re.findall(pattern, p.read_text(encoding="utf-8", errors="replace"), re.M))


def s2():
    rows = {run: {"register_rows(R-n)": count_rows(art(run, "work/requirements-register.md"), r"^\|\s*R-\d+")} for run in runs()}
    print("## S2 — requirements register"); table(rows)


def s3():
    rows = {}
    for run in runs():
        tp = load(art(run, "work/test-plan.json"))
        r = {"plan_rows": count_rows(art(run, "work/test-plan.md"), r"^\|\s*TS-\d+")}
        if tp:
            items = tp if isinstance(tp, list) else (tp.get("rows") or tp.get("items") or tp.get("plan") or [])
            r["plan_json_rows"] = len(items) if isinstance(items, list) else "?"
        rows[run] = r
    print("## S3 — test plan"); table(rows)


def s4():
    rows = {}
    for run in runs():
        d = art(run, "work/test-cases")
        rows[run] = {"case_files": len(compare.case_files(d)),
                     "critic_findings": len(list(d.rglob("critic-findings*.md"))) if d and d.is_dir() else 0}
    print("## S4 — test cases"); table(rows)


def s5():
    rows = {}
    for run in runs():
        m = load(art(run, "work/automation-manifest.json"))
        r = {}
        if m:
            tests = m.get("tests") or []
            r["instances"] = len(tests)
            r["cases_covered"] = len({t.get("case") for t in tests if t.get("case")} | {c for t in tests for c in (t.get("covers") or [])})
            r["unresolved"] = len(m.get("unresolved") or [])
            r["files"] = len({t.get("file") or t.get("path") for t in tests})
        else:
            r["instances"] = "none"
        rows[run] = r
    print("## S5 — automation manifest"); table(rows)


def counter(values):
    """The distribution of a column as one cell: `passed_green=7,partial=2`."""
    out = {}
    for v in values:
        out[str(v)] = out.get(str(v), 0) + 1
    return ",".join(f"{k}={n}" for k, n in sorted(out.items(), key=lambda kv: (-kv[1], kv[0])))


def s6():
    """S6 — what actually ran: the run report is the only witness of execution."""
    rows = {}
    for run in runs():
        d = load(art(run, "work/run-report.json"))
        if not d:
            rows[run] = {"run_report": "none"}
            continue
        res = d.get("results") or []
        cur = d.get("current_results") or []
        tot = d.get("totals") or {}
        manual = d.get("manual_checks") or []
        rows[run] = {"execution_status": d.get("execution_status"),
                     "results": len(res), "current_results": len(cur),
                     "totals": ",".join(f"{k}={v}" for k, v in (tot or {}).items() if v),
                     "statuses": counter(r.get("status") for r in res),
                     "manual_checks": len(manual),
                     "manual_pass": sum(1 for m in manual if str(m.get("result") or m.get("status")) == "pass"),
                     "env_blocked": len(d.get("env_blocked") or []),
                     "impossible": len(d.get("impossible") or []),
                     "factory_findings": len(d.get("factory_findings") or [])}
    print("## S6 — run report"); table(rows)


def s7():
    """S7 — triage: a failure without a verdict is the defect this stage exists to prevent."""
    rows = {}
    for run in runs():
        d = load(art(run, "work/triage.json"))
        if not d:
            rows[run] = {"triage": "none"}
            continue
        t = d.get("triage") or []
        rows[run] = {"triage_rows": len(t),
                     "verdicts": counter(r.get("verdict") for r in t) or "—",
                     "with_evidence": sum(1 for r in t if r.get("evidence_refs") or r.get("evidence")),
                     "reason": str(d.get("reason") or "")[:22]}
    print("## S7 — triage"); table(rows)


def s8():
    """S8 — the ledger and the delivery verdict: the numbers the person is handed."""
    rows = {}
    for run in runs():
        led = load(art(run, "work/ledger.json"))
        dsum = load(art(run, "work/delivery-summary.json"))
        r = {}
        if led:
            lrows = led.get("rows") or []
            r["ledger_rows"] = len(lrows)
            r["states"] = counter(x.get("state") for x in lrows)
            r["delivery_ready"] = compare.verdict_word(led)
            r["blocked_by"] = len(led.get("blocked_by") or [])
            r["reasons"] = len(led.get("reasons") or [])
        else:
            r["ledger_rows"] = "none"
        if dsum:
            c = dsum.get("counts") or {}
            r["counts"] = ",".join(f"{k}={v}" for k, v in c.items() if v)
            r["gaps"] = len(dsum.get("gaps") or [])
            r["owners"] = counter((dsum.get("reasons_by_owner") or {}).keys()) or "—"
        bugs = BASE / folder_of(run) / "test-harness" / "qa-factory" / "bugs"
        r["bug_files"] = len(list(bugs.glob("BUG-*.md"))) if bugs.is_dir() else 0
        rep = art(run, "test-report.md")
        r["report_bytes"] = rep.stat().st_size if rep else "none"
        rows[run] = r
    print("## S8 — checks ledger, delivery, bugs"); table(rows)


def s9():
    """S9 — retro: prose over numbers the code computed."""
    rows = {}
    for run in runs():
        retro = art(run, "retro.md")
        nums = load(art(run, "work/retro-numbers.json"))
        r = {"retro_bytes": retro.stat().st_size if retro else "none"}
        if nums:
            story = nums.get("story") or {}
            # `usd` is the current key (None while the two records differ: the `price` cell below then
            # carries the range); `cost_usd` and `cost` are the keys of older facts files.
            r["cost_usd"] = story.get("usd") or story.get("cost_usd") or story.get("cost")
            r["requests"] = story.get("requests")
            r["halts"] = (nums.get("halts") or {}).get("count")
            r["orchestrator_share"] = nums.get("orchestrator_share_percent")
            # `control_layer` is gone from the facts (owner, 30.09: the conductor's money is the share's
            # numerator); a story's money is `price` (task_price's answer, FR-10) and `price_problem`
            # (why the journals could not be read). A facts file of an older generation has neither key,
            # and an old `control_layer` is read for nothing: the cells are just left out.
            price = nums.get("price") if isinstance(nums.get("price"), dict) else {}
            low, high = price.get("price_low_usd"), price.get("price_high_usd")
            if isinstance(low, (int, float)) and isinstance(high, (int, float)):
                r["price"] = f"{price.get('status')}: {low:.2f}" + ("" if low == high else f"-{high:.2f}")
            elif price:
                r["price"] = f"{price.get('status')}: not priced"
            if nums.get("price_problem"):
                r["price_problem"] = nums["price_problem"]
        rows[run] = r
    print("## S9 — retro numbers"); table(rows)


def stages():
    """Wall clock per stage, from pipeline.json — the same source the factory records."""
    rows = {}
    for run in runs():
        d = load(art(run, "pipeline.json"))
        if not d:
            rows[run] = {"pipeline": "none"}
            continue
        r = {}
        for name, st in (d.get("stages") or {}).items():
            st = st or {}
            r[name] = f"{st.get('status')} {str(st.get('completed_at') or st.get('at') or '')[5:16]}"
        rows[run] = r
    print("## stages — status and completion time (pipeline.json)"); table(rows)


# --- S0 of one story against the LLM run (t-267, keys K2 and K16) -------------------------------------
# `s0` above is the yardstick of the runs table's ticket: it is wired to that story and its baseline copies, and
# it stays as it is. A step moved from a role to code is compared with the LLM reference (PROJECT.md p.5); for the
# ticket read of a later story the reference is a story run itself (a key of story_runs in the runs table, or
# --ref-run): the snapshot its roles actually used.
#   LLM column     work/ticket-snapshot.json of the reference run
#   driver column  --driver-run <folder>: work/ticket-snapshot.json of that run (after t-267 the light
#                  snapshot of the REST read); with no --driver-run: the REST `_snapshot` output of the
#                  reference run (`work/sources/SRC-*/<rev>/ticket.json`), which is what the code produces
#                  from the tracker today, before t-267 - and which is why today the table stops.
import jira_light_check as jlc  # noqa: E402  (standalone stdlib measurer, same folder)

STORY_RUNS = dict(paths.STORY_RUNS)
K16_COLUMNS = ("acceptance_criteria", "comments", "parent", "description_len", "attachments", "subtasks")
ABSENT = jlc.ABSENT


def story_dir(run, story):
    """The artifacts folder of `story` in a run: a key of STORY_RUNS, a folder that is there under BASE as it always
    was (`<copy_prefix>man1`), or - B-267 - the bare suffix `prepare_copy.py --name` was given (`man1`), which is the
    folder `<copy_prefix>man1`. A folder that exists keeps its own name, so no name that worked before changes. An
    empty prefix never matches by itself: `startswith("")` is true for every name (B-267, edge 5)."""
    folder = STORY_RUNS.get(run)
    if folder is None:
        prefixed = bool(paths.COPY_PREFIX) and str(run).startswith(paths.COPY_PREFIX)
        folder = run if (BASE / str(run)).is_dir() or prefixed else report_run.copy_folder(run, {})
    return BASE / folder / "test-harness" / "qa-factory" / "artifacts" / story


def s0_columns(d: dict) -> dict:
    """The columns of the S0 table for one snapshot; ABSENT where the file does not carry the fact
    (a key that is not there is not a 0)."""
    def count(key):
        return len(d[key] or []) if isinstance(d.get(key), (list, type(None))) and key in d else ABSENT

    links = d.get("links")
    cols = {"acceptance_criteria": ABSENT, "comments": count("comments"),
            "parent": d["parent"] if "parent" in d else ABSENT,
            "subtasks": count("subtasks"),
            "description_len": len(d.get("description") or "") if "description" in d else ABSENT,
            "merge_request": bool(links.get("merge_request")) if isinstance(links, dict) else ABSENT,
            "issue_links": len(links.get("issue_links") or []) if isinstance(links, dict)
            else (len(links) if isinstance(links, list) else ABSENT),
            "remote_links": len(links.get("remote_links") or []) if isinstance(links, dict) else ABSENT,
            "attachments": ABSENT, "status": d.get("status", ABSENT)}
    ac, _ = jlc.ac_parts(d)
    if ac is not None:
        cols["acceptance_criteria"] = ac
    for key in ("attachments", "attachment_names"):
        if isinstance(d.get(key), list):
            cols["attachments"] = len(d[key])
            break
    return cols


def k16(ref: dict, drv: dict) -> list:
    """[(column, LLM value, driver value, ok, why)] - the driver must show at least what the LLM run had.
    An absent driver value is fewer only when the LLM had something there; absent on the LLM side is
    nothing to compare."""
    out = []
    for col in K16_COLUMNS:
        r, d = ref[col], drv[col]
        if r == ABSENT:
            out.append((col, r, d, True, "the LLM snapshot does not carry it: nothing to compare"))
        elif col == "parent":
            ok = r is None or d == r
            out.append((col, r, d, ok, "equal" if ok else "the parent differs from the LLM's"))
        elif d == ABSENT:
            ok = r == 0
            out.append((col, r, d, ok, "no data in the driver file, the LLM had 0" if ok
                        else "the driver file does not carry it"))
        else:
            ok = d >= r
            out.append((col, r, d, ok, "driver >= LLM" if ok else f"driver {d} < LLM {r}"))
    return out


def s0_story(story: str, driver_run=None, ref_run=None, as_json=False) -> int:
    """Print the K16 table and the K2 lines; exit code 1 on a STOP, 2 when a file is missing or no reference run is
    named (ref_run None: pass --ref-run, or give the runs table a story_runs key)."""
    if not ref_run:
        print("--ref-run is required: it has no default without a runs table (QA_RUNS_TABLE) naming a story run",
              file=sys.stderr)
        return 2
    ref_dir = story_dir(ref_run, story)
    ref_path = ref_dir / "work" / "ticket-snapshot.json"
    if driver_run:
        drv_path, drv_what = story_dir(driver_run, story) / "work" / "ticket-snapshot.json", f"snapshot of run {driver_run}"
    else:
        found = jlc.find_rest(ref_dir, story)
        drv_path, drv_what = (found[-1] if found else None), "REST `_snapshot` output (before t-267)"
    rest_found = jlc.find_rest(ref_dir, story)
    rest_path = rest_found[-1] if rest_found else None
    ref_m, drv_m, rest_m = jlc.measure(ref_path), jlc.measure(drv_path), jlc.measure(rest_path)
    problems = [f"{name}: {m['state']} ({m['path'] or 'not found under ' + str(ref_dir / 'work' / 'sources')})"
                for name, m in (("LLM snapshot", ref_m), ("driver file", drv_m)) if m["state"] != "ok"]
    if problems:
        print("## S0 - " + story + ": NOT MEASURED")
        for line in problems:
            print("  " + line)
        return 2
    ref, drv = s0_columns(load(ref_path)), s0_columns(load(drv_path))
    verdicts = k16(ref, drv)
    k2 = [("K2a own-words share %", ref_m["share_pct"], drv_m["share_pct"],
           drv_m["share_pct"] is not None and ref_m["share_pct"] is not None and drv_m["share_pct"] >= ref_m["share_pct"],
           "driver share >= LLM share"),
          ("K2b bytes", rest_m["bytes"], drv_m["bytes"],
           rest_m["bytes"] is not None and drv_m["bytes"] < rest_m["bytes"],
           "driver file below the REST ticket.json")]
    stops = [f"STOP K16 {c}: LLM {r}, driver {d} - {why} (PROJECT.md p.5: fewer than the LLM run is a stop, not 'go on')"
             for c, r, d, ok, why in verdicts if not ok]
    stops += [f"STOP {c}: {'REST ticket.json' if c.endswith('bytes') else 'LLM'} {r}, driver {d} - needs: {why} (PROJECT.md p.5)"
              for c, r, d, ok, why in k2 if not ok]
    if as_json:
        print(json.dumps({"story": story, "llm": {"path": str(ref_path), "columns": ref, "measure": ref_m},
                          "driver": {"path": str(drv_path), "what": drv_what, "columns": drv, "measure": drv_m},
                          "rest": {"path": str(rest_path), "measure": rest_m},
                          "k16": [{"column": c, "llm": r, "driver": d, "ok": ok, "why": why} for c, r, d, ok, why in verdicts],
                          "k2": [{"check": c, "reference": r, "driver": d, "ok": ok, "why": why} for c, r, d, ok, why in k2],
                          "stops": stops, "verdict": "STOP" if stops else "ok"},
                         indent=2, ensure_ascii=False, default=str))
        return 1 if stops else 0
    print(f"## S0 - {story} ticket snapshot: LLM reference ({ref_run}) vs driver")
    print(f"LLM    : {ref_path}")
    print(f"driver : {drv_path}   [{drv_what}]")
    rows = {"LLM": dict(ref), "driver": dict(drv)}
    for name, m in (("LLM", ref_m), ("driver", drv_m)):
        rows[name]["bytes"], rows[name]["own_words_share_%"] = m["bytes"], m["share_pct"]
    table(rows)
    print(f"K16 columns checked: {', '.join(K16_COLUMNS)}")
    for line in stops:
        print(line)
    print("K16/K2 verdict: " + (f"STOP ({len(stops)})" if stops else "ok - the driver shows at least what the LLM run had"))
    return 1 if stops else 0


def story_main(argv) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="stage_compare.py s0")
    ap.add_argument("stage")
    ap.add_argument("--story", required=True)
    ap.add_argument("--driver-run", default=None, help="folder (or key) of the run whose snapshot is the driver column")
    ap.add_argument("--ref-run", default=next(iter(STORY_RUNS), None),
                    help="the LLM reference run (default: the first key of story_runs in the runs table)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.stage != "s0":
        print(f"--story is for the s0 table only (got {args.stage!r}); the other stages are for the runs table's ticket only")
        return 2
    return s0_story(args.story, args.driver_run, args.ref_run, args.json)


ORDER = ["s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "stages"]


def main(argv) -> int:
    """The ticket tables: `stage_compare.py [s0..s9|stages|all] [--run NAME ...] [--ticket T]`. Each `--run` adds one
    column beside the baselines of RUNS; a name RUNS does not hold is the copy `<copy_prefix>NAME` (B-267: a run such
    as man1 was unreadable until three dicts were edited). A bad name or an unknown stage is refused by name, exit 2."""
    import argparse
    global TASK
    ap = argparse.ArgumentParser(prog="stage_compare.py")
    ap.add_argument("stage", nargs="?", default="all", help="one of " + ", ".join(ORDER) + " or all")
    ap.add_argument("--run", action="append", default=[], metavar="NAME",
                    help="a run to show beside the baselines: its name in the runs table (QA_RUNS_TABLE), or the "
                         "suffix of the copy `prepare_copy.py --name NAME` made; repeatable")
    ap.add_argument("--ticket", default=None, help="the ticket whose artifacts are read (default: task of the runs table)")
    args = ap.parse_args(argv)
    if args.stage != "all" and args.stage not in ORDER:
        print(f"unknown stage {args.stage!r}: one of {', '.join(ORDER)} or all", file=sys.stderr)
        return 2
    if args.ticket:
        TASK = args.ticket
    if not TASK:
        print("no ticket: pass --ticket or set task in the runs table (QA_RUNS_TABLE)", file=sys.stderr)
        return 2
    if not RUNS and not args.run:
        print("no runs: pass --run NAME or name baselines in the runs table (QA_RUNS_TABLE)", file=sys.stderr)
        return 2
    try:
        for name in args.run:
            folder_of(name)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    EXTRA[:] = args.run
    for name in (ORDER if args.stage == "all" else [args.stage]):
        globals()[name]()
        print()
    return 0


if __name__ == "__main__":
    if "--story" in sys.argv[1:]:
        raise SystemExit(story_main(sys.argv[1:]))
    raise SystemExit(main(sys.argv[1:]))
