#!/usr/bin/env python3
"""told real: a part of test_stage_joints.py, split by tools/test_split.py (TD-11c). The shared helpers are in stage_joints_common."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import FIXTURES, PLUGIN_ROOT, check_eq, finish  # noqa: E402
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))
import refusal_registry as RR  # noqa: E402
import stage_joints as SJ  # noqa: E402
from stage_joints_common import (  # noqa: E402
    GROUP_REASONS, REAL, conductor_line, conductor_only, k5_problems, load_told, measure_untold, reachable,
    rowless_of, rowless_problems, told_unit_rows, unit_problems, untold_problems,
)


CENSUS = FIXTURES / "judgment-census.json"


_WORLD = {}


def told_world() -> dict:
    """The census-side measurement of the real tree, computed once: the wide scan with the census's blocking set (the CLI's own
    road), the join, and the four counters of the told fixture."""
    if _WORLD:
        return _WORLD
    import test_judgment_census as CT
    names = RR.package_files(PLUGIN_ROOT)
    rows = {(r["file"], r["function"]): r for r in json.loads(CENSUS.read_text(encoding="utf-8"))["rows"]}
    units = CT.units_of(PLUGIN_ROOT, names)["units"]
    rep = RR.wide_report(PLUGIN_ROOT, names, RR.load_census(CENSUS), {k for k, u in units.items() if u["blocks"]})
    joined = rep["units"]
    ids = {RR.check_of(e): (Path(e["file"]).name, e["function"]) for e in RR.REGISTRY}
    ids.update({i: (f, fn) for i, (f, fn, _line) in SJ.check_ids().items()})
    # the literal `exit_gate:required_outputs` is the family `required_outputs_errors` collects (`own(..., "exit_gate:required_outputs")`
    # in `all_errors`); the walk maps every literal to `all_errors`, this join gives that one literal its own unit (t-722 Q1)
    ids["exit_gate:required_outputs"] = ("exit_gate.py", "required_outputs_errors")
    unit_roles = {k: r.get("roles") for k, r in rows.items()}
    _WORLD.update(
        rep=rep, rows=rows, units=units, ids=ids, unit_roles=unit_roles,
        by_unit={f"{u['file']}::{u['function']}": {"bare": u["states"].get("bare", 0), "tagged": u["states"].get("tagged", 0)}
                 for u in joined if reachable(u["roles"])},
        rowless=rowless_of(ids, unit_roles, REAL), untold=measure_untold(units, rows, rep["sites"]),
        groups=conductor_only(joined, rows))
    return _WORLD


def told_baselines(world: dict) -> dict:
    """What the told fixture holds: the measurement of `told_world`, printed key by key in the report of the node that wrote it."""
    return {"rowless": len(world["rowless"]), "untold": world["untold"], "units": dict(sorted(world["by_unit"].items()))}


def told_real() -> None:
    world, (told, why) = told_world(), load_told()
    check_eq("told/fixture-present: the told fixture is read", (told is not None, why), (True, ""))
    totals = world["rep"]["totals"]
    print(f"told: units_no_row {totals['units_no_row']}, join_share {totals['join_share']}, role_reachable_units "
          f"{totals['role_reachable_units']}, rowless {len(world['rowless'])} {world['rowless']}, untold {world['untold']}")
    print(conductor_line(world["groups"]))
    check_eq("K1: every join unit has a census row (100 %)", (totals["units_no_row"], totals["join_share"]), (0, 1.0))
    check_eq("K1: no check argument the scanner cannot read (`own` is a listed pass-through)", totals["check_arg_errors"], 0)
    check_eq("K1-A24/at-baseline: the A24 and literal ids a role can meet and no row covers equal the baseline",
             rowless_problems(world["rowless"], told["rowless"]), [])
    check_eq("K1-lit/adviser-rowed: `exit_gate:adviser` (a literal id of a role-reachable unit) has its row since T1r and is not counted",
             ("exit_gate:adviser" in world["rowless"], SJ.row_for("exit_gate:adviser", REAL)[0] is not None), (False, True))
    check_eq("K6/untold-counted: the blocking units with a role and no sourced/tagged site are at their baseline",
             untold_problems(world["untold"], told["untold"]), [])
    check_eq("K4/at-baseline: bare/tagged of every role-reachable unit at or under its baseline",
             unit_problems(world["by_unit"], told["units"]), [])
    check_eq("K4/baseline-covers-join: the baseline names every role-reachable unit of the join, and the join's count is the fixture's",
             (sorted(world["by_unit"]), totals["role_reachable_units"]), (sorted(told["units"]), len(told["units"])))
    check_eq("K5/real: the rows of the real file that state a requirement name every role of their unit (live now: it judges the units "
             "of those rows, none yet; T1r's rows are judged with no further edit)",
             k5_problems(world["unit_roles"], told_unit_rows(world["ids"], REAL), SJ._mapped_roles()), [])
    check_eq("conductor-only/printed-per-group: every conductor-only join unit sits in exactly one named group with its reason",
             (sum(world["groups"].values()), set(world["groups"]) <= set(GROUP_REASONS), totals["conductor_only_units"]),
             (totals["conductor_only_units"], True, totals["conductor_only_units"]))


def main() -> None:
    told_real()
    finish("test_stage_joints_told_real")


# split: runner piece 1
if __name__ == "__main__":
    main()
