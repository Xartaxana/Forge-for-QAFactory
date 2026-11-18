#!/usr/bin/env python3
"""The stage-joints walk: the registry, its three directions, its pins and its negative controls (F6-51, FR-5, FR-38, FR-28).

`stage_joints.audit` walks the package (the error families of the exit gate, the blocking detectors of stages.json, the
gap kinds of the S5 window) against `references/stage-joints.json` and demands for each check a producer, a place the
role is told, and every demanded token in a file the role receives. A walker that walks nothing is green for the wrong
reason (t-317 F4), so the three walk sizes are pinned in BOTH directions, and every refusal below is shown on a
synthetic input or a deep copy next to the real tree passing. The real package is never mutated (FR-45).

Keys: K1 real tree green + the summary line, K2 pins AT, K3 pin -1/+1, K4 a check with no row, K5 stale row and two rows,
K6 each missing leg (and the informed gap, a gap on a complete leg, the `code:` site cases), K7 the reach rule, K8 direction
C, K9 unreadable shapes of the walk, K10 the data file, K11 the ratchet, K12 the joint census, K13 threshold(), K14 the CLI.
"""
# Shared helpers of test_stage_joints.py, split by tools/test_split.py (TD-11c).
import contextlib
import copy
import io
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import FIXTURES, PLUGIN_ROOT  # noqa: E402
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))
import null_outcomes as NO  # noqa: E402
import stage_joints as SJ  # noqa: E402


# The walk sizes. A change of any is a change of the factory's checks and the Lead's question: the walker is not adjusted
# to agree with the tree. exit: the 8 families of all_errors + main; detector: the 5 scripts of the 9 tuples of stages.json
# (minus the adviser sizing.py; `branch_accounting.py` runs at 4 stages and is ONE member); window: 28 distinct gap kinds
# of validate_window (30 append sites, `expectation_change_gaps` from extend).
PINS = {"exit": 8, "detector": 5, "window": 28}


ENV = SJ.Env.real()


REAL, _WHY = SJ.load_rows(SJ.DATA)


UNI = SJ.universe()


def kind_keys(kind: str, uni=None) -> list:
    """The keys of the universe (or of the rows) whose member is of `kind`: never a prefix test (B2)."""
    return sorted(k for k, m in (UNI if uni is None else uni)[0].items() if m["kind"] == kind)


def member(kind: str, where: str = "x.py::f:1", stages=None) -> dict:
    return {"kind": kind, "where": where, "stages": stages}


def audit(data=None, uni=None, pins=None, env=None):
    return SJ.audit(copy.deepcopy(REAL) if data is None else data, UNI if uni is None else uni, pins, env or ENV)


def mutated(change, relax_ratchet: bool = True) -> dict:
    """A deep copy of the data with `change` applied; the ratchet follows the gaps unless the case is about the ratchet."""
    data = copy.deepcopy(REAL)
    change(data)
    if relax_ratchet:
        data["ratchet"][-1]["gaps"] = sum(1 for r in data["joints"] for p in r["producers"] if p.get("gap"))
    return data


def row_of(data: dict, check_key: str) -> dict:
    return next(r for r in data["joints"] if r["check"] == check_key)


def text_of(report) -> str:
    return " | ".join(report.problems)


def cli(*args) -> tuple:
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = SJ.main(list(args))
    return code, out.getvalue()


def a_row(check: str, roles=("qa-runner",), stages=("S5",), **extra) -> dict:
    """A synthetic v2 row (a producer entry that names `roles`, told by the page); `extra` sets requirement, when, door ..."""
    return {"check": check, "stages": list(stages), "joint": None, **extra,
            "producers": [{"roles": list(roles), "field": "a field", "told": [{"page": True}], "demands": []}]}


def a_rows_file(*rows) -> dict:
    return {"schema_version": 2, "when_kinds": list(REAL["when_kinds"]), "joints": list(rows)}


# ----------------------------------------------------------------------------------------------------------------------
# T1c: the counters that need the census (FR-44: the census is a test fixture, so they are computed and compared HERE; `audit`
# never opens it, `told/audit-shape`). Two worlds (TEMPORAL): before the T1c commit nothing reads `told-ratchet.json` and no row
# is judged against it; after it, an absent or unreadable file is red ("told-ratchet.json cannot be read"), never zeros.
TOLD_FIXTURE = FIXTURES / "told-ratchet.json"


GROUP_RE = re.compile(r"parent 2\.8 group (G-[a-z]+)")


UNGROUPED = "ungrouped"


GROUP_REASONS = {      # parent spec 2.8: why a conductor-only unit is outside K2/K5/K6 (a group is read off the census row's note)
    "G-dispatch": "the caller is the driver's code or the interactive main session; a launch makes no dispatch the conductor could be told of",
    "G-free": "a command the conductor chose inside its launch; no open move's run names it",
    "G-main": "met by the interactive main session acting as conductor; it is no launch for one problem",
    "G-code": "a controller/story_step refusal answered by a code move with no resume and no conductor launch",
    UNGROUPED: "the census row names no 2.8 group (T4/T9a/T9c label them as they relabel)"}


def reachable(roles) -> bool:
    """A unit a role can meet: its census roles hold a role other than the conductor."""
    return bool(set(roles or []) - {"conductor"})


def load_told(path=None) -> tuple:
    """`(data, "")` of the told fixture, or `(None, why)`: absent, unreadable or not of its shape is red, never zero counts (E4)."""
    path = Path(path or TOLD_FIXTURE)
    data, why = NO.load_data(path)
    if data is None:
        return None, f"{path.name} cannot be read ({why})"
    units = data.get("units")
    good = (all(isinstance(data.get(k), int) and not isinstance(data.get(k), bool) and data[k] >= 0 for k in ("rowless", "untold"))
            and isinstance(units, dict) and all(isinstance(u, dict) and set(u) == {"bare", "tagged"} and all(
                isinstance(n, int) and not isinstance(n, bool) and n >= 0 for n in u.values()) for u in units.values()))
    return (data, "") if good else (None, f"{path.name} cannot be read (it holds `rowless`, `untold` and `units` of bare/tagged counts)")


def covered(check_id: str, data: dict) -> bool:
    """An id is covered by exactly one row: its own, else its namespace's `<stem>:*`, else a sub-id row `<id>.<part>` (C14)."""
    row, _why = SJ.row_for(check_id, data)
    return row is not None or any(str(r.get("check")).startswith(f"{check_id}.") for r in data["joints"])


def rowless_of(ids: dict, unit_roles: dict, data: dict) -> list:
    """K1-A24/literal: the ids a role can meet (`ids` is {id: unit}) that no row covers. E5: the fallback exemption runs BEFORE
    the row lookup, so a fallback id is never counted and never makes a row look sited."""
    out = []
    for check_id, unit in sorted(ids.items()):
        if SJ.is_fallback(check_id) or not reachable(unit_roles.get(unit)):
            continue
        if not covered(check_id, data):
            out.append(check_id)
    return out


def rowless_problems(ids: list, baseline: int) -> list:
    """`rowless` is dense: over is red naming the ids, under is red saying what to lower it to."""
    if len(ids) > baseline:
        return [f"rowless is {len(ids)}, baseline {baseline}: add a row for {', '.join(ids)}"]
    return [f"lower `rowless` to {len(ids)} (baseline {baseline})"] if len(ids) < baseline else []


def untold_problems(got: int, baseline: int) -> list:
    return [f"untold is {got}, baseline {baseline}: a blocking unit with a role has no sourced or tagged site"] if got > baseline else []


def unit_problems(measured: dict, baseline: dict) -> list:
    """K4: per `file::function` of a role-reachable unit, `bare` and `tagged` stay at or under their baseline; a unit with a bare
    site and no baseline row is red (E7)."""
    out = []
    for key, now in sorted(measured.items()):
        base = baseline.get(key)
        if base is None:
            if now["bare"]:
                out.append(f"{key}: {now['bare']} bare site(s) in a role-reachable unit with no baseline row in told-ratchet.json")
            continue
        out += [f"{key}: {state} is {now[state]}, baseline {base[state]}" for state in ("bare", "tagged") if now[state] > base[state]]
    return out


def measure_untold(units: dict, rows: dict, found: list) -> int:
    """K6: blocking census units (a row's `blocks_override: false` lifts it) with a role that hold no sourced/tagged site."""
    count = 0
    for key, unit in units.items():
        row = rows.get(key) or {}
        if not (unit["blocks"] and row.get("blocks_override") is not False and reachable(row.get("roles"))):
            continue
        told = any(s["state"] in ("sourced", "tagged") and s["file"] == key[0]
                   and (s["function"] == key[1] or any(a <= s["line"] <= b for a, b in unit["spans"])) for s in found)
        count += 0 if told else 1
    return count


def KEY_PAGE_ROLES(row: dict) -> list:
    """The roles a row's producers name literally (a `*` is expanded by the caller's mapped set, not here)."""
    return [r for e in row.get("producers") or [] if isinstance(e, dict) and isinstance(e.get("roles"), list) for r in e["roles"] if r != SJ.ANY]


def row_counts(row: dict, role: str, mapped: set) -> bool:
    """K5 (T1r-pages P-8): a row counts for a role when a producer names the role AND the row tells it: it states a requirement
    (page or call: a call-told row is a row that states one), or it is a sentence-less row whose leg for that role is the role's
    OWN key page (`references/slices/<role>/handoff-keys.md`, the `<role>` placeholder expanded for this role). Another role's page,
    an unexpanded placeholder and a leg with no path do not count (the error direction is toward NOT counting)."""
    if not SJ._row_names(row, role, lambda: mapped):
        return False
    if SJ._states_requirement(row):
        return True
    own = SJ.KEY_PAGE.format(role=role)
    return any(isinstance(e, dict) and isinstance(e.get("roles"), list) and (role in e["roles"] or SJ.ANY in e["roles"])
               and any(isinstance(t, dict) and isinstance(t.get("path"), str) and SJ._expand(t["path"], role) == own
                       for t in e.get("told") or [])
               for e in row.get("producers") or [])


def k5_problems(unit_roles: dict, unit_rows: dict, mapped: set) -> list:
    """K5: the roles of a unit (census roles minus the conductor) are each named by a told row of it (`SJ._row_names`: `*` is
    every mapped role, never the conductor)."""
    out = []
    for unit, rows in sorted(unit_rows.items()):
        missing = {r for r in set(unit_roles.get(unit) or []) - {"conductor"}
                   if not any(row_counts(row, r, mapped) for row in rows)}
        if missing:
            out.append(f"{unit[0]}::{unit[1]} is met by {', '.join(sorted(missing))}, which no row of it names")
    return out


def told_unit_rows(ids: dict, data: dict) -> dict:
    """{unit: [rows]} of the rows that state a requirement (`SJ._states_requirement`), grouped by the unit of the check id they
    cover: the row's own id, a `<stem>:*` row for every id of that stem, a sub-id row `<id>.<part>` for its parent id."""
    out = {}
    for row in data["joints"]:
        if not SJ._states_requirement(row) and not any(row_counts(row, r, {r}) for r in KEY_PAGE_ROLES(row)):
            continue
        check = str(row.get("check"))
        stem = check.split(":", 1)[0]
        hit = [u for i, u in ids.items() if i == check or i == check.rsplit(".", 1)[0]
               or (check == f"{stem}:{SJ.ANY}" and i.split(":", 1)[0] == stem)]
        for unit in set(hit):
            out.setdefault(unit, []).append(row)
    return out


def conductor_only(units: list, rows: dict) -> dict:
    """The conductor-only join units counted per group (the group is the `parent 2.8 group G-x` token of the census row's note)."""
    groups = {}
    for u in units:
        if u["roles"] is None or reachable(u["roles"]):
            continue
        found = GROUP_RE.search(str((rows.get((u["file"], u["function"])) or {}).get("note") or ""))
        group = found.group(1) if found and found.group(1) in GROUP_REASONS else UNGROUPED
        groups[group] = groups.get(group, 0) + 1
    return groups


def conductor_line(groups: dict) -> str:
    return f"conductor_only {sum(groups.values())}: " + "; ".join(f"{g} {n} ({GROUP_REASONS[g]})" for g, n in sorted(groups.items()))
