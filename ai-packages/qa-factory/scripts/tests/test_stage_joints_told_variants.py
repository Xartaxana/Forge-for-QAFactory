#!/usr/bin/env python3
"""told variants: a part of test_stage_joints.py, split by tools/test_split.py (TD-11c). The shared helpers are in stage_joints_common."""
import copy
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import PLUGIN_ROOT, check, check_eq, check_in, cleanup, finish, temp_dir  # noqa: E402
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))
import refusal_registry as RR  # noqa: E402
import stage_joints as SJ  # noqa: E402
from stage_joints_common import (  # noqa: E402
    ENV, REAL, UNGROUPED, UNI, a_row, a_rows_file, audit, conductor_line, conductor_only, k5_problems,
    load_told, measure_untold, mutated, row_of, rowless_of, rowless_problems, text_of, told_unit_rows,
    unit_problems, untold_problems,
)


def told_variants() -> None:
    """The cases of the counters on synthetic input: at / over / under the baseline, the empty and absent inputs, the order."""
    u, roles = ("f.py", "g"), {("f.py", "g"): ["qa-runner"], ("f.py", "h"): ["conductor"]}
    data = a_rows_file(a_row("stage_guard:SG-1.shape"), a_row("s:*"), a_row("t:one"))
    check_eq("K1-A24/at-baseline: AT the baseline is green", rowless_problems(["a:x", "b:y"], 2), [])
    over = rowless_problems(["a:x", "b:y", "c:z"], 2)
    check("K1-A24/plus-one: one over is red and names the id", len(over) == 1 and "c:z" in over[0], str(over))
    check_eq("K1-A24/minus-one: one under is red, saying what to lower it to", rowless_problems(["a:x"], 2), ["lower `rowless` to 1 (baseline 2)"])
    check_eq("K1-A24/conductor-only-not-counted: an id whose unit only the conductor meets is not counted",
             rowless_of({"a:x": ("f.py", "h")}, roles, data), [])
    check_eq("K1-lit/fallback-no-row: `<stem>:unlabelled` and `unknown` need no row (the exemption runs before the lookup)",
             rowless_of({"s2:unlabelled": u, "unknown": u, "a:x": u}, roles, data), ["a:x"])
    check_eq("K1-lit/sub-id: a row `<id>.<part>` covers the id (C14)", rowless_of({"stage_guard:SG-1": u}, roles, data), [])
    check_eq("K1-lit/star-covers: `<stem>:x` is covered by `<stem>:*`, an exact row by itself, an id with neither is not",
             rowless_of({"s:x": u, "t:one": u, "q:z": u}, roles, data), ["q:z"])
    check_eq("K1-lit/absent-unit: an id whose unit has no census row is not role-reachable and not counted",
             rowless_of({"a:x": ("zz.py", "g")}, roles, data), [])
    missing = text_of(audit(data=mutated(lambda d: d["joints"].remove(row_of(d, "exit_gate:digest")))))
    check_in("K1/missing-row: a v1-derived check (an exit family) with no row is red, naming it and where code meets it",
             "exit_gate:digest is a check in code (exit_gate.py::all_errors:", missing)
    fallback = text_of(audit(data=mutated(lambda d: (d["joints"].append({**copy.deepcopy(row_of(d, "acceptance:review")), "check": "exit_gate:unlabelled"}),
                                                     d["told_ratchet"].update(unsited=0)))))
    check_in("K1-lit/fallback-no-row: a row keyed by a fallback id is not sited by it (E5)", "row exit_gate:unlabelled: stale", fallback)
    first = RR.check_of(RR.REGISTRY[0])
    check_eq("B/row-keyed-by-any-entry-not-stale: a row keyed by the check id of an A24 entry has a site",
             audit(data=mutated(lambda d: d["joints"].append({**copy.deepcopy(row_of(d, "acceptance:review")), "check": first}))).problems, [])
    def swap_adviser(d):
        """The real file holds one row for the literal (since T1r): the world replaces it by a copy of another row under the literal."""
        d["joints"].remove(row_of(d, "exit_gate:adviser"))
        d["joints"].append({**copy.deepcopy(row_of(d, "acceptance:review")), "check": "exit_gate:adviser"})
    check_eq("B/row-keyed-by-literal-not-stale: a row keyed by a literal id of the scanner (`exit_gate:adviser`) has a site",
             audit(data=mutated(swap_adviser)).problems, [])
    check_eq("B/row-keyed-by-literal-not-stale: and a sub-id of a sited id too",
             audit(data=mutated(lambda d: d["joints"].append({**copy.deepcopy(row_of(d, "acceptance:review")), "check": f"{first}.part"}))).problems, [])
    gone = lambda d: d["joints"].append({**copy.deepcopy(row_of(d, "acceptance:review")), "check": "exit_gate:gone"})
    # Each synthetic world states its own baseline: `base` is the measured real number (the tree's own cap), never inherited silently.
    base = REAL["told_ratchet"]["unsited"]
    check_in("E11/stale-when-baseline-0: an unsited row with the baseline at 0 is a stale row, red", "row exit_gate:gone: stale",
             text_of(audit(data=mutated(lambda d: (gone(d), d["told_ratchet"].update(unsited=0))))))
    one = lambda d: (gone(d), d["told_ratchet"].update(unsited=base + 1))
    check_eq(f"E11/unsited-at-baseline: AT the baseline (one more row than the real {base}, baseline {base + 1}) is green",
             audit(data=mutated(one)).problems, [])
    two = lambda d: (gone(d), d["joints"].append({**copy.deepcopy(row_of(d, "acceptance:review")), "check": "exit_gate:gone2"}),
                     d["told_ratchet"].update(unsited=base + 1))
    check_in("E11/unsited-over: over the baseline is red naming the counter, both numbers and the two rows",
             f"told_ratchet.unsited is {base + 1} but {base + 2} rows have no site in code", text_of(audit(data=mutated(two))))
    check_in("E11/unsited-over: and the new rows close the listed ids", "exit_gate:gone, exit_gate:gone2)", text_of(audit(data=mutated(two))))
    # K12: the cap is a NAMED number. raised_by: t-693 (T1r landed 227 rows whose sites are written later). It shrinks as the siting nodes
    # land: T9a (controller 6), T5 (s5_precheck 11, execution_request 10 rows, manifest_put 14, run_suite 7), T5b (execution_request --mine 14),
    # T6 (handoff_check 21), T7a-1..8 (validate_artifacts 42), T7b (planning_contract 12), T7c (coverage_contract 2), T3b (first_look 11).
    # lowered 150 -> 119 by T1r-sites (S-1a + S-1b sited 31 rows; the ratchet follows the measure).
    # lowered 46 -> 17 by T7a-B (10 rows) and T7a-C (19 rows), integrator t-1030.
    # lowered 17 -> 11 by T9a (sited refusals), t-1185.
    # raised 11 -> 17 by TBW-T1rc-int (t-1236): T1r-cards-a rows wait for TBW-T1rc-site (6 ids: 4 function rows + sides.provisional + sides.pending).
    UNSITED_CAP = 17
    check_eq("K12/unsited-cap: the real tree measures the named cap (a cap above the measurement is allowed (<=), one below is red)",
             (audit().counts["unsited"], REAL["told_ratchet"]["unsited"], UNSITED_CAP,
              audit(data=mutated(lambda d: d["told_ratchet"].update(unsited=UNSITED_CAP + 3))).problems,
              len(audit(data=mutated(lambda d: d["told_ratchet"].update(unsited=UNSITED_CAP - 1))).problems) > 0),
             (17, 17, 17, [], True))

    def extra_leg(d):
        """One more legacy told leg: a role entry told by a path other than its key page."""
        entry = next(p for r in d["joints"] for p in r["producers"] if not p.get("code") and isinstance(p.get("told"), list))
        entry["told"].append({"path": "agents/qa-runner.md"})
    for counter, up, down in (("hand_cards", True, True), ("legacy_legs", True, False)):
        stored = REAL["told_ratchet"][counter]
        dash = counter.replace("_", "-")
        report = audit()
        check_eq(f"told/{dash}-at-baseline: the walk counts the stored number and is green", (report.counts[counter], report.problems), (stored, []))
        if counter == "legacy_legs":
            check_eq("told/legacy-legs-floor: the stored number is 0, the floor of a count", stored, 0)
            check_in("told/legacy-legs-plus-one: one more legacy leg than the stored 0 is red naming the counter, the measured and the stored value",
                     "told_ratchet.legacy_legs is 0 but the walk counts 1", text_of(audit(data=mutated(extra_leg))))
            check_in("told/legacy-legs-negative: a stored -1 is no count, red by the shape check",
                     "a count (an integer, 0 or more) is expected", text_of(audit(data=mutated(lambda d: d["told_ratchet"].update(legacy_legs=-1)))))
        else:
            check_in(f"told/{dash}-plus-one: one more than the stored number is red naming the counter, the measured and the stored value",
                     f"told_ratchet.{counter} is {stored - 1} but the walk counts {stored}", text_of(audit(data=mutated(
                         lambda d, counter=counter: d["told_ratchet"].update({counter: stored - 1})))))
        low = text_of(audit(data=mutated(lambda d, counter=counter: d["told_ratchet"].update({counter: stored + 1}))))
        check_eq(f"told/{dash}-minus-one: {'dense: below is red, saying what to lower it to' if down else 'not dense (the table says audit only): below is green'}",
                 f"lower told_ratchet.{counter} to {stored}" in low, down)
    cards = copy.copy(ENV)
    cards.plugin = Path("no-such-plugin-root")
    check_in("told/hand-cards-unreadable: cards that cannot be counted are red, never 0", "the hand cards cannot be counted",
             text_of(SJ.audit(copy.deepcopy(REAL), UNI, None, cards, sited=set(UNI[0]))))
    # K4 / K6 / K5 on synthetic input
    base = {"a.py::f": {"bare": 2, "tagged": 1}}
    check_eq("K4/at-baseline: AT the baseline is green, and under it too", (unit_problems({"a.py::f": {"bare": 2, "tagged": 1}}, base),
             unit_problems({"a.py::f": {"bare": 1, "tagged": 0}}, base)), ([], []))
    plus = unit_problems({"a.py::f": {"bare": 3, "tagged": 1}}, base)
    check("K4/plus-one: one more bare site is red, naming the unit", len(plus) == 1 and "a.py::f: bare is 3, baseline 2" in plus[0], str(plus))
    check_in("K4/plus-one: and a tagged one too", "a.py::f: tagged is 2, baseline 1", " ".join(unit_problems({"a.py::f": {"bare": 2, "tagged": 2}}, base)))
    check_in("K4/new-unit-no-baseline: a role-reachable bare site in a unit with no baseline row is red", "a.py::new: 1 bare site(s)",
             " ".join(unit_problems({"a.py::new": {"bare": 1, "tagged": 0}}, base)))
    check_eq("K4/new-unit-no-baseline: a unit with no bare site and no row is not red", unit_problems({"a.py::new": {"bare": 0, "tagged": 1}}, base), [])
    check_eq("K6/untold-counted: at / over / under the baseline", [untold_problems(n, 5) == [] for n in (5, 6, 4)], [True, False, True])
    blocking = {"blocks": True, "spans": [(1, 9)]}
    units = {("a.py", "f"): blocking, ("a.py", "c"): blocking, ("a.py", "o"): blocking, ("a.py", "n"): {"blocks": False, "spans": []}}
    rows = {("a.py", "f"): {"roles": ["qa-runner"]}, ("a.py", "c"): {"roles": ["conductor"]}, ("a.py", "o"): {"roles": ["qa-runner"], "blocks_override": False},
            ("a.py", "n"): {"roles": ["qa-runner"]}}
    site = lambda state, line=3: {"file": "a.py", "function": "f", "line": line, "state": state}
    check_eq("K6/untold-counted: a blocking unit with a role and a bare site only is untold; a sourced or a tagged site tells it; a conductor-only, "
             "an overridden and a non-blocking unit are not counted",
             [measure_untold(units, rows, found) for found in ([site("bare")], [site("sourced")], [site("tagged")], [])], [1, 0, 0, 1])
    check_eq("K5/roles-subset: a unit's roles minus the conductor must all be named by its rows (`*` is every mapped role)",
             [k5_problems({u: r}, {u: [a_row("x:y", roles=rr, requirement="r")]}, {"qa-runner", "qa-scout"}) for r, rr in (
                 (["qa-runner", "conductor"], ("qa-runner",)), (["qa-runner", "qa-scout"], ("qa-runner",)), (["qa-runner", "qa-scout"], ("*",)))],
             [[], ["f.py::g is met by qa-scout, which no row of it names"], []])
    stub = a_rows_file(a_row("x:one", roles=("qa-runner",), requirement="a requirement"), a_row("y:*", roles=("qa-scout",), requirement="r"),
                       a_row("x:two"))
    ids = {"x:one": u, "y:a": ("f.py", "h"), "x:two": u}
    check_eq("K5/real-reads-the-rows: the rows that state a requirement are grouped by the unit of their id (a `<stem>:*` row covers the stem's ids, "
             "a row with no requirement is left out) and a role they do not name is red (the negative control of the real-tree row)",
             (sorted(map(len, told_unit_rows(ids, stub).values())), k5_problems({u: ["qa-runner", "qa-scout"], ("f.py", "h"): ["qa-scout"]},
                                                                               told_unit_rows(ids, stub), set())),
             ([1, 1], ["f.py::g is met by qa-scout, which no row of it names"]))
    groups = conductor_only([{"file": "f.py", "function": n, "roles": r} for n, r in (("a", ["conductor"]), ("b", ["conductor"]), ("c", ["conductor"]),
                                                                                     ("d", ["qa-runner"]), ("e", None))],
                            {("f.py", "a"): {"note": "x, parent 2.8 group G-free"}, ("f.py", "b"): {"note": "parent 2.8 group G-zzz"}, ("f.py", "c"): {}})
    check_eq("conductor-only/printed-per-group: the groups of the census notes, an unnamed or unknown group is `ungrouped`, a role unit and a rowless unit are not counted",
             groups, {"G-free": 1, UNGROUPED: 2})
    check_in("conductor-only/printed-per-group: the line names each group with its reason", "G-free 1 (a command the conductor chose inside its launch",
             conductor_line(groups))
    tmp = temp_dir("qa-told-")
    try:
        gone_path = tmp / "told-ratchet.json"
        data_none, why = load_told(gone_path)
        check_eq("told/fixture-absent: an absent fixture is red with the file named, never zero counts", (data_none, why.startswith("told-ratchet.json cannot be read")), (None, True))
        gone_path.write_text("{not json", encoding="utf-8")
        check_eq("told/fixture-absent: an unreadable fixture is the same", load_told(gone_path)[0], None)
        for label, body in (("a fixture with no `units`", {"rowless": 1, "untold": 1}), ("a bool count", {"rowless": True, "untold": 1, "units": {}}),
                            ("a unit with a missing key", {"rowless": 1, "untold": 1, "units": {"a.py::f": {"bare": 1}}})):
            gone_path.write_text(json.dumps(body), encoding="utf-8")
            check_eq(f"told/fixture-absent: {label} is not read as counts", load_told(gone_path)[0], None)
    finally:
        cleanup(tmp)


def main() -> None:
    told_variants()
    finish("test_stage_joints_told_variants")


# split: runner piece 1
if __name__ == "__main__":
    main()
