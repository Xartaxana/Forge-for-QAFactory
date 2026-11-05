#!/usr/bin/env python
"""How much of a role dispatch went into fighting the factory's own code.

Reads the role sessions of a run and classifies every turn: did the tool call the
role made come back as a working result, or as a crash, a guard refusal, a wrong
argument shape, or a validator rejection of our own artifact? A role that writes
its own helper script into work/ is counted too: that is the role building what
the factory failed to give it.

Money is the turn's own cost from the transcript's usage block, so a friction turn
carries the full weight of the context it had to re-read. It is priced by the turn's own
`message.model` through the package's model-rates.json (a fixed Sonnet-4 rate table used to price
every turn, so a run on claude-sonnet-5-5 or claude-opus-5-5 was measured at the wrong rate). A
turn the catalogue cannot price - no model, an unknown model, `<synthetic>` with usage, or a rate
entry without a key the turn uses - is UNPRICED: it is counted in the printed "unpriced turns"
line and left out of every money sum, never priced at a fallback (FR-41).

The classification, the turn reader and the friction count are the package's own
(`scripts/friction.py`, spellings in `references/friction-markers.json`); this file only injects the
experiment's price and prints. Nothing of that logic is copied here, so the two cannot drift apart.
"""
from __future__ import annotations
import argparse, collections, json, sys

import compare
import paths

# The package's friction module, found through paths.SCRIPTS. It goes at the END of sys.path so a
# package script can never shadow this folder's own compare/paths. Absent: fail loudly, naming the
# path - there is no local copy to fall back on.
_PACKAGE_FRICTION = paths.SCRIPTS / "friction.py"
if not _PACKAGE_FRICTION.is_file():
    raise ImportError("code_friction: the package friction module is absent: %s (expected "
                      "ai-packages/qa-factory/scripts/friction.py, found through paths.SCRIPTS)"
                      % _PACKAGE_FRICTION)
if str(paths.SCRIPTS) not in sys.path:
    sys.path.append(str(paths.SCRIPTS))
import friction as _pkg
from friction import SCRIPT, classify, is_project_test

BASE = paths.BASE
TASK = paths.TASK                   # the runs table's ticket, or None: then --ticket names it
RUNS = dict(paths.BASELINES)        # the runs table's baselines ({} without a table); other names go by copy_folder


def _price(rate):
    """The package's injected `price(model, usage)`, valued by this folder's own catalogue reader."""
    return lambda model, usage: compare.price_turn(rate, model, usage)


def turns_of(path, rate=None):
    """The package's turn reader, priced by `compare.price_turn` over `rate` (default: the rates)."""
    rate = compare.rates() if rate is None else rate
    return _pkg.turns_of(path, _price(rate))


def friction(path, rate=None):
    """The package's friction count, priced by `compare.price_turn` over `rate`."""
    rate = compare.rates() if rate is None else rate
    return _pkg.friction(path, _price(rate))


def journal_path(run):
    return (BASE / paths.copy_folder(run, RUNS) / "test-harness" / "qa-factory" / "artifacts" / TASK
            / "state" / "driver-runs.jsonl")


def sessions(run):
    j = journal_path(run)
    if not j.exists():
        return []
    out = []
    for line in j.open(encoding="utf-8"):
        try:
            r = json.loads(line)
        except Exception:
            continue
        if r.get("kind") == "role" and r.get("session_id"):
            out.append(r)
    return out


def project_dir(run):
    return paths.transcript_dir(BASE / paths.copy_folder(run, RUNS) / "test-harness")


def main():
    global TASK
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+", help="run names: a baseline of the runs table, or a copy suffix")
    ap.add_argument("--by", choices=("role", "stage"), default="role")
    ap.add_argument("--scripts", action="store_true",
                    help="instead of roles, name the scripts that refused or crashed")
    ap.add_argument("--ticket", default=None, help="the ticket whose artifacts are read (default: task of the runs table)")
    a = ap.parse_args()
    if a.ticket:
        TASK = a.ticket
    paths.require_args(ap, ("--ticket", TASK))
    rate = compare.rates()
    if a.scripts:
        per = collections.Counter()
        who = collections.defaultdict(collections.Counter)
        for run in a.runs:
            done = set()
            if not journal_path(run).is_file():
                print("no driver journal for %s: %s is absent" % (run, journal_path(run)))
            for s in sessions(run):
                p = project_dir(run) / (s["session_id"] + ".jsonl")
                if not p.exists() or s["session_id"] in done:
                    continue
                done.add(s["session_id"])
                rows, results = turns_of(p, rate)
                for r in rows:
                    for c in r["calls"]:
                        for txt in results.get(c["id"], []):
                            k = classify(txt)
                            if not k:
                                continue
                            names = SCRIPT.findall((c["arg"] or "").lower()) or \
                                SCRIPT.findall(str(txt)[:400].lower())
                            nm = names[0] if names else (c["name"] or "?")
                            # A guard message names its own subject in its first words, but the
                            # hook COMMAND LINE that precedes it lists every hook script, so the
                            # first script name in the text was telemetry_hook.py whatever the
                            # message said. That put 11 events on telemetry_hook.py which were
                            # really TURN BUDGET notices and one correct refusal about a person's
                            # word - neither is a defect of ours to fix.
                            if k == "guard":
                                for mark in ("TURN BUDGET", "STAGE GUARD", "PRE-TOOL GUARD"):
                                    if mark in str(txt):
                                        nm = mark.lower().replace(" ", "-")
                                        break
                            if is_project_test(nm):
                                k = "project-test"
                            per[(nm, k)] += 1
                            who[(nm, k)][s.get("role")] += 1
        print("%-26s %-10s %5s  roles" % ("script", "kind", "times"))
        for (nm, k), n in per.most_common(24):
            print("%-26s %-10s %5d  %s" % (nm, k, n,
                  ", ".join("%s:%d" % kv for kv in who[(nm, k)].most_common(4))))
        return 0
    for run in a.runs:
        per = collections.defaultdict(lambda: dict(
            turns=0, cost=0.0, fric_turns=0, fric_cost=0.0, dispatches=0,
            tally=collections.Counter(), money=collections.Counter()))
        done = set()
        unpriced = 0
        if not journal_path(run).is_file():
            print("\nno driver journal for %s: %s is absent" % (run, journal_path(run)))
            continue
        for s in sessions(run):
            p = project_dir(run) / (s["session_id"] + ".jsonl")
            if not p.exists() or s["session_id"] in done:
                continue
            done.add(s["session_id"])
            f = friction(p, rate)
            unpriced += f["unpriced"]
            row = per[s.get("role") if a.by == "role" else s.get("stage")]
            row["dispatches"] += 1
            for fld in ("turns", "cost", "fric_turns", "fric_cost"):
                row[fld] += f[fld]
            row["tally"].update(f["tally"])
            row["money"].update(f["money"])
        print("\n=== %s: friction of the factory's own code, by %s (%d role sessions) ==="
              % (run, a.by, len(done)))
        print("%-22s %4s %6s %7s %10s %7s %6s  %s"
              % (a.by, "disp", "turns", "$", "fric.turn", "fric.$", "share", "breakdown"))
        tot = collections.Counter()
        kinds = collections.Counter()
        for k, r in sorted(per.items(), key=lambda kv: -kv[1]["fric_cost"]):
            br = ", ".join("%s:%d" % (n, c) for n, c in r["tally"].most_common())
            sh = r["fric_cost"] / r["cost"] * 100 if r["cost"] else 0
            print("%-22s %4d %6d %7.2f %10d %7.2f %5.1f%%  %s"
                  % (str(k), r["dispatches"], r["turns"], r["cost"],
                     r["fric_turns"], r["fric_cost"], sh, br))
            for fld in ("turns", "cost", "fric_turns", "fric_cost"):
                tot[fld] += r[fld]
            kinds.update(r["tally"])
        sh = tot["fric_cost"] / tot["cost"] * 100 if tot["cost"] else 0
        print("%-22s %4s %6d %7.2f %10d %7.2f %5.1f%%  %s"
              % ("TOTAL", "", tot["turns"], tot["cost"], tot["fric_turns"], tot["fric_cost"],
                 sh, ", ".join("%s:%d" % kv for kv in kinds.most_common())))
        print("unpriced turns: %d (no rate for their model in model-rates.json; "
              "left out of every $ above)" % unpriced)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
