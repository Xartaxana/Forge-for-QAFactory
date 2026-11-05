# -*- coding: utf-8 -*-
"""Savings/trend report across both contours for the weekly
calibration's savings check: is delegation actually saving money, and
what's the trend.

Computes from cc_usage (the subscription contour) and requests (the
API contour) in gateway/requests.db, using full API list prices (no
batch discount; the cache multipliers are each model's own, read from
tools/model_prices.json -- a real API mechanism):

1. PRE (< --routed-start) and ROUTED (>= --routed-start [.. --until])
   windows: turns, accounted cost, $/day, a main/side breakdown by
   model.
2. Delegation counterfactual: token profiles of routed sidechains,
   re-priced at the top-tier model's rates, against the actual cost --
   gross savings in $ and %. Both sides must be whole for a figure: turns
   of a model with no price (a NULL stored cost, counted by usage_report's
   unpriced_turns) are never a $0 actual -- the line says "gross savings:
   not measurable (partial: N turn(s) without a price -- <models>)" and
   the window TOTAL lines carry the same mark (FR-41).
3. API contour: requests and accounted cost by traffic_kind.

The n/a rule is per table: with no database file, or one holding
neither table, the tool prints ONE "savings report: n/a" line and exits
0; with one table, the other table's sections read "not measured (no
`<table>` table)". An unreadable price file is one stderr line, exit 2.

The first run's recorded baseline is your first savings/trend report
-- keep it for comparison against later runs. Method caveats (a
censored baseline, and that the coordination premium isn't separable
from non-delegable top-tier work) belong in that same baseline record
and remain in force.

Prices deliberately do NOT duplicate the price table -- they're read
through tools/usage_report.py's load_prices() from tools/model_prices.json,
the single owner of pricing.
"""
import argparse
import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

_TOOLS_DIR = Path(__file__).resolve().parent
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))

# A DIRECT sibling-module import only -- NOT a "try tools.usage_report
# package-style, fall back to a sibling import" pattern. This kit's
# install tree lives inside a larger repository that ALSO carries its
# own top-level tools/ directory with a DIFFERENTLY BEHAVING
# usage_report.py; a bare `import tools.usage_report` can resolve
# "tools" as an implicit namespace package rooted at the CURRENT
# WORKING DIRECTORY (PEP 420 -- no __init__.py required) rather than
# at this file's own directory, silently picking up the WRONG module
# whenever the working directory happens to be that repo's root. The
# sys.path insertion above already guarantees a sibling `from
# usage_report import ...` resolves to THIS directory's own module
# unambiguously -- no package-style guess is needed or safe here.
from usage_report import (  # the memoized load_prices(); the one cost formula; the one unpriced-turn count
    PricesError, accounted_cost, get_prices, unpriced_turns)
from mechanism_gate import resolve_lead_binding  # the ONE reader of the Lead binding (delegation.config.yaml)

import streams

# The report prints non-ASCII text (section headers, totals): the one stream setup of tools/streams.py,
# at import time (also when the module is imported, not only on a direct run).
streams.utf8_stdio()

_UNBOUND = "fable"  # what resolve_lead_binding returns when the config names no roles.lead model
CONFIG_PATH = _TOOLS_DIR.parent / "delegation.config.yaml"
_NEEDED_TABLES = ("cc_usage", "requests")
_CONTOUR_RE = re.compile(r"^contour:\s*([A-Za-z0-9_-]+)")


def read_contour(path=None) -> str:
    """The `contour:` word of delegation.config.yaml, or "unknown" (no file, unreadable, no such line).
    No reader of this file for the contour exists in tools/ (mechanism_gate parses only roles.lead), so this
    is a minimal line scan of the one top-level key -- not a second YAML reader."""
    try:
        text = Path(path if path is not None else CONFIG_PATH).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return "unknown"
    for line in text.splitlines():
        m = _CONTOUR_RE.match(line)
        if m:
            return m.group(1)
    return "unknown"


def open_usage_db(db_path):
    """(connection, tables, reason): `tables` is the set of the report's tables the database holds. The
    connection is None (and `tables` empty) when the file is absent or unreadable, or holds NONE of the tables
    -- the n/a case; a database with only one of them is returned, the report marks the other section.
    Read-only, so a missing path is never created by the probe (sqlite3.connect would create an empty file).
    reason is "" for a missing file or no table (the n/a line needs no word), "unreadable" otherwise."""
    path = Path(db_path)
    if not path.is_file():
        return None, set(), ""
    conn = None
    try:
        conn = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
        have = {r[0] for r in conn.execute("select name from sqlite_master where type='table'")}
    except (sqlite3.Error, OSError):
        if conn is not None:
            conn.close()
        return None, set(), "unreadable"
    tables = have & set(_NEEDED_TABLES)
    if not tables:
        conn.close()
        return None, set(), ""
    return conn, tables, None


def _na_line(db_path, reason: str) -> str:
    extra = f"; reason: {reason}" if reason else ""
    return (f"savings report: n/a — no usage database for check 18"
            f" (contour {read_contour()}; source: {db_path}{extra})")


def top_tier_model(path=None) -> str:
    """The counterfactual's model: the one bound to roles.lead in delegation.config.yaml, read through
    mechanism_gate.resolve_lead_binding (no model id is written in this tool). A config that cannot be read, or
    that names no lead model, is a PricesError naming the file -- never a silent default price (FR-41). A model
    the price file does not know is not an error here: the counterfactual is then unpriced and the savings are
    "not measurable"."""
    config = Path(path if path is not None else CONFIG_PATH)
    try:
        text = config.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        raise PricesError(f"delegation config {config}: cannot be read ({getattr(e, 'strerror', None) or e});"
                          " the counterfactual prices at the model bound to roles.lead there")
    model = resolve_lead_binding(text)
    if model == _UNBOUND:
        raise PricesError(f"delegation config {config}: roles.lead names no model (subscription.model or"
                          " api.model); the counterfactual prices at the model bound to roles.lead")
    return model


def partial_mark(turns: int, models) -> str:
    """The mark of a figure that is not whole (FR-41): how many turns have no price and which models they are."""
    return f"partial: {turns} turn(s) without a price — {', '.join(models)}"


def window_summary(db: sqlite3.Connection, cond: str, params: tuple) -> dict:
    unpriced = unpriced_turns(db, cond, params)
    rows = db.execute(
        "select model, is_sidechain, count(*), sum(accounted_cost_usd),"
        " count(distinct session_id) from cc_usage where " + cond +
        " group by model, is_sidechain order by 4 desc", params).fetchall()
    days = db.execute(
        "select count(distinct substr(ts,1,10)) from cc_usage where " + cond,
        params).fetchone()[0]
    total_cost = sum(r[3] or 0 for r in rows)
    total_turns = sum(r[2] for r in rows)
    return {"rows": rows, "days": days, "total_cost": total_cost,
            "total_turns": total_turns,
            "per_day": total_cost / days if days else 0.0,
            "unpriced_turns": sum(unpriced.values()),
            "unpriced_models": sorted(str(m) for m in unpriced)}


def counterfactual_summary(db: sqlite3.Connection, cond: str, params: tuple) -> dict:
    rows = db.execute(
        "select agent_type, model, count(*), sum(input_tokens), sum(output_tokens),"
        " sum(cache_creation_tokens), sum(cache_read_tokens), sum(accounted_cost_usd)"
        " from cc_usage where is_sidechain=1 and " + cond +
        " group by agent_type, model order by 8 desc", params).fetchall()
    detail = []
    actual = cf = 0.0
    top = top_tier_model()
    cf_priced = True  # False once the top-tier model itself has no price: the counterfactual side is not whole
    for at, model, n, ti, to, tcw, tcr, cost in rows:
        # the aggregate has no 1-hour split: the counterfactual's cache writes are 5-minute (understates the savings)
        f = accounted_cost(top, ti or 0, to or 0, tcw or 0, tcr or 0)[0]
        actual += cost or 0
        if f is None:
            cf_priced = False
        else:
            cf += f
        detail.append({"agent_type": at, "model": model, "turns": n,
                       "actual": cost or 0, "as_fable": f})
    unpriced = unpriced_turns(db, "is_sidechain=1 and " + cond, params)
    actual_partial = bool(unpriced)
    # Both sides must be whole for a figure: a side with an unpriced model makes the savings "not measurable".
    # A top-tier price missing leaves every sidechain turn without a counterfactual price.
    turns = sum(d["turns"] for d in detail) if not cf_priced else sum(unpriced.values())
    models = sorted({str(m) for m in unpriced} | (set() if cf_priced else {top}))
    measurable = cf_priced and not actual_partial
    return {"detail": detail, "actual": actual, "as_fable": cf, "top_model": top,
            "actual_partial": actual_partial, "counterfactual_partial": not cf_priced,
            "unpriced_turns": turns, "unpriced_models": models,
            "gross_savings": cf - actual if measurable else None,
            "savings_pct": ((1 - actual / cf) * 100 if cf else 0.0) if measurable else None}


def api_contour_summary(db: sqlite3.Connection) -> dict:
    kinds = db.execute(
        "select traffic_kind, count(*), sum(cost_usd) from requests"
        " group by traffic_kind order by 3 desc").fetchall()
    total = db.execute("select count(*), sum(cost_usd) from requests").fetchone()
    return {"kinds": kinds, "total_n": total[0], "total_cost": total[1] or 0.0}


def print_report(db_path: str, routed_start: str, until: str = None) -> None:
    """The whole report. The n/a rule is per table: the database file absent or unreadable, or holding NEITHER
    table -> ONE n/a line and nothing else; otherwise each section is printed when ITS table exists and shows
    "not measured (no `<table>` table)" in place of its numbers when it does not (FR-41: "not measured" is said
    in words, not as a traceback). A price file that cannot be read raises PricesError BEFORE the first report
    line, so a half-printed report never precedes it."""
    db, tables, reason = open_usage_db(db_path)
    if db is None:
        print(_na_line(db_path, reason))
        return
    try:
        if "cc_usage" in tables:
            get_prices()  # only the cc_usage sections price anything
            top_tier_model()  # and the counterfactual needs the Lead binding: a refusal comes before the first line
        _print_report_body(db, tables, routed_start, until)
    finally:
        db.close()


def _not_measured(table: str) -> None:
    print(f"  not measured (no `{table}` table)")


def _print_report_body(db: sqlite3.Connection, tables: set, routed_start: str, until) -> None:
    until_cond, until_params = ("", ()) if not until else (" and ts < ?", (until,))
    has_cc = "cc_usage" in tables

    for label, cond, params in [
        ("PRE-ROUTING (< %s)" % routed_start, "ts < ?", (routed_start,)),
        ("ROUTED (>= %s%s)" % (routed_start, f" .. {until}" if until else ""),
         "ts >= ?" + until_cond, (routed_start,) + until_params),
    ]:
        print(f"\n===== {label} =====")
        if not has_cc:
            _not_measured("cc_usage")
            continue
        w = window_summary(db, cond, params)
        for model, sc, n, cost, sess in w["rows"]:
            kind = "side" if sc else "main"
            print(f"  {model:28} {kind:4} turns={n:5} sess={sess:3}"
                  f" cost=${cost or 0:9.2f}  $/turn={((cost or 0) / n):.4f}")
        mark = f" ({partial_mark(w['unpriced_turns'], w['unpriced_models'])})" if w["unpriced_turns"] else ""
        print(f"  TOTAL: {w['total_turns']} turns, ${w['total_cost']:.2f},"
              f" {w['days']} days, ${w['per_day']:.2f}/day{mark}")

    print("\n===== COUNTERFACTUAL: routed sidechains at the top-tier model's rates =====")
    if has_cc:
        c = counterfactual_summary(db, "ts >= ?" + until_cond,
                                   (routed_start,) + until_params)
        _print_counterfactual(c)
    else:
        _not_measured("cc_usage")
    _print_api_section(db, "requests" in tables)
    measured = [name for name, ok in (("subscription windows + counterfactual (cc_usage)", has_cc),
                                      ("API contour (requests)", "requests" in tables)) if ok]
    missing = [t for t in _NEEDED_TABLES if t not in tables]
    print("\nSections measured: " + "; ".join(measured)
          + (f". Not measured (table absent): {', '.join(missing)}." if missing else "."))
    print("\nFor the calibrated event's notes: $/day ROUTED, gross"
          " savings in $ and %, actual sidechain cost, API total;"
          " compare against your first run's recorded baseline.")


def _print_counterfactual(c: dict) -> None:
    print(f"  top-tier model: {c['top_model']} (roles.lead in delegation.config.yaml)")
    for d in c["detail"]:
        top = "unpriced" if d["as_fable"] is None else f"${d['as_fable']:8.2f}"
        print(f"  {str(d['agent_type']):16} {d['model']:28} turns={d['turns']:4}"
              f" actual=${d['actual']:8.2f} as-top-tier={top}")
    actual_mark = " (actual partial)" if c["actual_partial"] else ""
    cf_mark = " (counterfactual partial)" if c["counterfactual_partial"] else ""
    if c["gross_savings"] is None:
        savings = f"gross savings: not measurable ({partial_mark(c['unpriced_turns'], c['unpriced_models'])})"
    else:
        savings = f"gross savings=${c['gross_savings']:.2f} ({c['savings_pct']:.0f}%)"
    print(f"  TOTAL: actual=${c['actual']:.2f}{actual_mark}  as-top-tier=${c['as_fable']:.2f}{cf_mark}  {savings}")


def _print_api_section(db: sqlite3.Connection, has_requests: bool) -> None:
    print("\n===== API CONTOUR (requests.db, full history) =====")
    if not has_requests:
        _not_measured("requests")
        return
    a = api_contour_summary(db)
    for kind, n, cost in a["kinds"]:
        print(f"  {kind:10} n={n:4} cost=${cost or 0:.4f}")
    print(f"  TOTAL: {a['total_n']} requests, ${a['total_cost']:.4f} accounted")


def _date(value: str) -> str:
    """argparse type: a YYYY-MM-DD date, checked before anything else runs."""
    try:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):  # strptime alone takes "2026-10-7", which sorts wrong as text
            raise ValueError(value)
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value!r} is not a YYYY-MM-DD date")
    return value


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Savings/trend report (calibration check 18)")
    ap.add_argument("--db", default=str(Path(__file__).resolve().parent.parent
                                        / "gateway" / "requests.db"))
    ap.add_argument("--routed-start", required=True, type=_date,
                    help="the PRE/ROUTED boundary: the date routing was deployed"
                         " on YOUR repo (YYYY-MM-DD)")
    ap.add_argument("--until", default=None, type=_date,
                    help="upper bound of the ROUTED window (YYYY-MM-DD; for reproducible slices)")
    args = ap.parse_args(argv)
    try:
        print_report(args.db, args.routed_start, args.until)
    except PricesError as e:
        print(f"savings_report: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
