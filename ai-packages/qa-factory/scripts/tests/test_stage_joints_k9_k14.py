#!/usr/bin/env python3
"""k9 k14: a part of test_stage_joints.py, split by tools/test_split.py (TD-11c). The shared helpers are in stage_joints_common."""
import copy
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import PLUGIN_ROOT, check, check_eq, check_in, check_not_in, cleanup, finish, run_script, temp_dir  # noqa: E402
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))
import stage_joints as SJ  # noqa: E402
from stage_joints_common import ENV, REAL, UNI, audit, cli, mutated, row_of, text_of  # noqa: E402


def k9_unreadable_shapes() -> None:
    members, errors = SJ.exit_members("def all_errors():\n    errors = a()\n    errors += self.x()\n"
                                      "def main():\n    errors = [e for e in errors]\n")
    check_eq("K9/E6: an attribute call in `errors` is a walk error, naming the line", len(errors), 1)
    check_in("K9: and the line", "exit_gate.py:3", errors[0])
    check_eq("K9: the family beside it is still a member", sorted(members), ["exit_gate:a"])
    check_eq("K9/member-shape: a member carries its kind, where and `stages: None` (an exit family is not judged by the stage rule)",
             members["exit_gate:a"], {"kind": "exit", "where": "exit_gate.py::all_errors:2", "stages": None})
    members, errors = SJ.exit_members("def all_errors():\n    errors = errors + list(x) + b() + (c if q else d)\n"
                                      "    if y:\n        errors += d()\n"
                                      "def main():\n    errors = [e for e in errors if e]\n    errors, passed = all_errors()\n")
    check_eq("K9: a name, a comprehension, `list`, the aggregator and a tuple target are no family, no error; a nested statement is walked",
             (sorted(members), errors), (["exit_gate:b", "exit_gate:d"], []))
    def wrapped(expr: str) -> tuple:
        members, errors = SJ.exit_members(f"def all_errors():\n    errors = {expr}\ndef main():\n    pass\n")
        return sorted(members), len(errors)
    check_eq("K9/wrap-own: own(f(x), 'exit_gate:a') is the family f under the id the call gives it", wrapped("own(f(x), 'exit_gate:a')"),
             (["exit_gate:a"], 0))
    check_eq("exit/literal-key: the key is the literal, whatever the callee is called", wrapped("own(f(), 'exit_gate:x')"), (["exit_gate:x"], 0))
    check_eq("K9/wrap-mixed: a wrapped and a bare family", wrapped("own(f(), 'exit_gate:a') + g()"), (["exit_gate:a", "exit_gate:g"], 0))
    check_eq("K9/wrap-nested: wrappers unwrap repeatedly and the INNERMOST id stands (`with_check` keeps the first)",
             wrapped("own(own(f(), 'exit_gate:a'), 'exit_gate:b')"), (["exit_gate:a"], 0))
    check_eq("K9/wrap-not-call: own(x, 'a') is neither member nor error", wrapped("own(x, 'exit_gate:a')"), ([], 0))
    check_eq("K9/wrap-attr: own(m.f(), 'a') is a walk error", wrapped("own(m.f(), 'exit_gate:a')"), ([], 1))
    members, errors = SJ.exit_members("def all_errors():\n    errors = own(f(), name)\ndef main():\n    pass\n")
    check_eq("exit/non-literal-check: own(f(), name) is a walk error and invents no key", (sorted(members), len(errors)), ([], 1))
    check_in("exit/non-literal-check: the text", "the check id given to `own` at line 2 is not a text; write the id as a literal", errors[0])
    check_eq("exit/non-literal-check: a call with no second argument is the same walk error", wrapped("own(f())"), ([], 1))
    members, errors = SJ.exit_members("def all_errors():\n    errors = own()\ndef main():\n    pass\n")
    check_eq("K9/wrap-noargs: own() is a walk error with the text", (sorted(members), len(errors)), ([], 1))
    check_in("K9/wrap-noargs: the text", "a call of `own` with no argument in `errors`; extend the walk or simplify the call", errors[0])
    check_not_in("K9/own-is-not-a-family: the wrapper is never a member", "own",
                 " ".join(SJ.exit_members("def all_errors():\n    errors = own(f(), 'exit_gate:a') + own(own(g(), 'exit_gate:b'), 'exit_gate:c')\n"
                                          "    refused = own(h(), 'exit_gate:x')\n    late = own(k(), 'exit_gate:y')\ndef main():\n    pass\n")[0]))
    check_eq("K9/wrap-list-skipped: own(list(x), 'a') gives the skipped list", wrapped("own(list(x), 'exit_gate:a')"), ([], 0))
    check_eq("K9: a file with neither function is a walk error", len(SJ.exit_members("x = 1")[1]), 2)
    check_eq("K9: a source that is not Python is a walk error", len(SJ.exit_members("def (")[1]), 1)
    src = ("def validate_window():\n    gaps.append(f(i))\n    gaps.append('a:' + x)\n    gaps.append(K if c else 'b:' + y)\n"
           "    gaps.extend(g for g in h(w))\n    gaps.extend(zz)\n")
    members, errors = SJ.window_members(src, {"K": "k:"})
    check_eq("K9/E6: gaps.append(f(i)) and gaps.extend(no call) are walk errors, each naming its line",
             sorted(e.split(" - ")[0] for e in errors), ["cannot read the check at acceptance.py:2", "cannot read the check at acceptance.py:6"])
    check_eq("K9: a constant, a module name and both branches of a conditional are members; extend adds the called name",
             sorted(members), ["acceptance:a", "acceptance:b", "acceptance:h", "acceptance:k"])
    check_eq("K9/member-shape: a window member carries kind `window`, its line, and `stages: None`", members["acceptance:a"],
             {"kind": "window", "where": "acceptance.py::validate_window:3", "stages": None})
    check_eq("K9: a name that is no module text is a walk error, not skipped",
             len(SJ.window_members("def validate_window():\n    gaps.append(NOPE + ':')\n", {})[1]), 1)
    check_eq("K9: no validate_window is a walk error", len(SJ.window_members("x = 1", {})[1]), 1)


def k10_data_file() -> None:
    check_in("K10/E8: a reason string (file unreadable) is red, never an empty registry", "stage-joints.json cannot be read",
             text_of(SJ.audit("stage-joints.json cannot be read (OSError)", UNI, None, ENV)))
    check_in("K10: an unknown top key", "has an unknown key `extra`", text_of(audit(data=mutated(lambda d: d.update(extra=1)))))
    check_in("K10: a lost top key", "lacks `friction`", text_of(audit(data=mutated(lambda d: d.pop("friction")))))
    check_in("K10: schema 1", "schema_version is 1, this reader reads 2", text_of(audit(data=mutated(lambda d: d.update(schema_version=1)))))
    for key, bad, said in (("when_kinds", [], "`when_kinds` is not a non-empty list"), ("when_exclusive", [["plan"]], "`when_exclusive` is not a list of lists"),
                           ("when_exclusive", [["plan", "zz"]], "names `zz`, which is not in `when_kinds`"),
                           ("told_ratchet", {"hand_cards": 12}, "`told_ratchet` is not an object holding exactly hand_cards, legacy_legs, unsited"),
                           ("told_ratchet", {"hand_cards": 12, "legacy_legs": -1, "unsited": 0}, "told_ratchet.legacy_legs is -1, a count"),
                           ("told_ratchet", {"hand_cards": 12, "legacy_legs": 9, "unsited": -1}, "told_ratchet.unsited is -1, a count"),
                           ("told_ratchet", {"hand_cards": True, "legacy_legs": 9, "unsited": 0}, "told_ratchet.hand_cards is True, a count")):
        check_in(f"K10/v2-shape: {key} = {bad!r} is red", said, text_of(audit(data=mutated(lambda d, key=key, bad=bad: d.update({key: bad})))))
    for key in ("when_kinds", "when_exclusive", "told_ratchet"):
        check_in(f"K10/v2-shape: a lost {key} is red", f"lacks `{key}`", text_of(audit(data=mutated(lambda d, key=key: d.pop(key)))))
    check_in("K10: an unknown row key", "unknown key `owner`", text_of(audit(data=mutated(lambda d: d["joints"][0].update(owner="x")))))
    check_in("K10: no joint rows is red", "has no joint rows", text_of(audit(data=mutated(lambda d: d.update(joints=[])))))
    check_in("K10: a short note is red", "`note` is shorter than 40", text_of(audit(data=mutated(lambda d: d.update(note="short")))))
    tmp = temp_dir("qa-joints-data-")
    try:
        for label, body in (("absent", None), ("malformed", "{not json"), ("an array", "[]")):
            path = tmp / f"{label.replace(' ', '-')}.json"
            if body is not None:
                path.write_text(body, encoding="utf-8")
            report = SJ.audit(path=path, uni=UNI, env=ENV)
            check(f"K10: a data file that is {label} is red with the file named", report.problems and "stage-joints" in report.problems[0]
                  and path.name in report.problems[0], str(report.problems))
    finally:
        cleanup(tmp)


def k11_ratchet() -> None:
    n = REAL["ratchet"][-1]["gaps"]
    check_eq("K11: the real ratchet equals the declared gaps", n, sum(1 for r in REAL["joints"] for p in r["producers"] if p.get("gap")))
    check_in("K11: a count that differs from the last entry is red", f"gaps has {n} declared gaps and the ratchet's last entry says {n + 1}",
             text_of(audit(data=mutated(lambda d: d["ratchet"].__setitem__(-1, {"node": "F6-51", "gaps": n + 1}), False))))
    check_in("K11: a history that rises is red, named as a raise", f"ratchet rises from {n} to {n + 2}",
             text_of(audit(data=mutated(lambda d: d["ratchet"].extend([{"node": "F6-51", "gaps": n + 2}]), False))))
    check_eq("K11: a history that falls to the count is green",
             audit(data=mutated(lambda d: d["ratchet"].insert(0, {"node": "F6-51", "gaps": n + 3}), False)).problems, [])
    check_in("K11: an empty ratchet is red", "ratchet is empty", text_of(audit(data=mutated(lambda d: d.update(ratchet=[]), False))))
    check_in("K11: a node that is not the node that keeps it is red", "is not F6-51",
             text_of(audit(data=mutated(lambda d: d["ratchet"][-1].update(node="N1"), False))))
    for node in ("F6-52", "F6-51a", "f6-51"):
        check_in(f"K2/m-2: a ratchet row under another node id ({node}) is refused - only F6-51 lowers it", "is not F6-51",
                 text_of(audit(data=mutated(lambda d, node=node: d["ratchet"].append({"node": node, "gaps": n - 1}), False))))
    check_in("K2/m-2: a gap ref of another node form is refused", "is not `B-<n>` or `F6-51/<n>`",
             text_of(audit(data=mutated(lambda d: [p["gap"].update(ref="F6-52/1") for r in d["joints"] for p in r["producers"] if p.get("gap")][:1], False))))
    check_in("K11: a key that is not a count is red", "`gaps` is not a count",
             text_of(audit(data=mutated(lambda d: d["ratchet"][-1].update(gaps=True), False))))


def k12_joint_census() -> None:
    test = "scripts/tests/test_stage_joints_12586.py"
    check_in("K12: a joint test that never mentions its fixture folder is red", "never mentions the fixture folder",
             text_of(audit(data=mutated(lambda d: row_of(d, "acceptance:review").update(
                 joint={"test": test, "fixture": "scripts/tests/fixtures/run-12586-digest/"})))))
    both = text_of(audit(data=mutated(lambda d: row_of(d, "acceptance:review").update(
        joint={"test": "scripts/tests/test_nowhere.py", "fixture": "scripts/tests/fixtures/nowhere/"}))))
    check_in("K12: a test that does not exist is red", "joint test scripts/tests/test_nowhere.py does not exist", both)
    check_in("K12: a fixture that does not exist is red", "joint fixture scripts/tests/fixtures/nowhere/ does not exist", both)
    check_eq("K12: a null joint is counted, never red", audit(data=mutated(lambda d: row_of(d, "exit_gate:digest").update(joint=None))).problems, [])
    held = [r["check"] for r in REAL["joints"] if r["joint"]]
    check_eq("K12: the rows that carry a recorded-run joint", sorted(held), sorted([
        "exit_gate:scoped", "exit_gate:digest", "planning_contract:*", "acceptance:quality"]))


def k13_threshold() -> None:
    check_eq("K13: threshold() reads friction.same_class_gate_blocks", SJ.threshold(), REAL["friction"]["same_class_gate_blocks"])
    tmp = temp_dir("qa-joints-thr-")
    try:
        v2 = {"schema_version": 2}
        for label, body, want in (("absent key", {**v2, "joints": []}, None), ("1 (below the floor)", {**v2, "friction": {SJ.KEY: 1}}, None),
                                  ("a bool", {**v2, "friction": {SJ.KEY: True}}, None), ("a text", {**v2, "friction": {SJ.KEY: "3"}}, None),
                                  ("2 (AT the floor)", {**v2, "friction": {SJ.KEY: 2}}, 2), ("5", {**v2, "friction": {SJ.KEY: 5}}, 5),
                                  ("a schema 1 file (the reader reads 2)", {"schema_version": 1, "friction": {SJ.KEY: 5}}, None),
                                  ("a file with no schema", {"friction": {SJ.KEY: 5}}, None)):
            path = tmp / "d.json"
            path.write_text(json.dumps(body), encoding="utf-8")
            check_eq(f"K13: {label}", SJ.threshold(path), want)
        check_eq("K13: a file that is not there gives None, not a default number", SJ.threshold(tmp / "nothing.json"), None)
    finally:
        cleanup(tmp)


def k14_cli() -> None:
    code, out = cli()
    check_eq("K14: the CLI exits 0 on the real tree and prints the line", (code, "stage joints: clean" in out), (0, True))
    done = run_script("stage_joints.py", "--check")
    check_eq("K14: the script itself exits 0 (--check)", done.returncode, 0)
    tmp = temp_dir("qa-joints-cli-")
    try:
        short = copy.deepcopy(REAL)
        short["joints"] = [r for r in short["joints"] if r["check"] != "exit_gate:digest"]
        path = tmp / "short.json"
        path.write_text(json.dumps(short), encoding="utf-8")
        code, out = cli("--data", str(path))
        check_eq("K14: a copy with one row removed exits 1 and prints the detector shape", (code, out.count("REJECT — 1 finding(s)")), (1, 1))
        check_in("K14: and names the check", "exit_gate:digest is a check in code", out)
        bad = tmp / "bad.json"
        bad.write_text("{not json", encoding="utf-8")
        code, out = cli("--data", str(bad))
        check_eq("K14/m-1: a malformed data file exits 3 (the contract's EXIT_UNREADABLE) with the UNREADABLE line",
                 (code, out.startswith("UNREADABLE: ")), (3, True))
        code, out = cli("--data", str(tmp / "absent.json"))
        check_eq("K14/m-1: an absent data file exits 3", code, 3)
        check_eq("K14: --data with no file is a usage error, exit 2", cli("--data")[0], 2)
        import detector_verdict
        check_eq("K14/m-1: the exit is the contract's constant, not a copy", detector_verdict.EXIT_UNREADABLE, 3)
        check_eq("K14/m-1: the contract reads the CLI's own output as unreadable",
                 bool(detector_verdict.parse(code, out, "")["unreadable"]), True)
    finally:
        cleanup(tmp)


def main() -> None:
    k9_unreadable_shapes()
    k10_data_file()
    k11_ratchet()
    k12_joint_census()
    k13_threshold()
    k14_cli()
    finish("test_stage_joints_k9_k14")


# split: runner piece 1
if __name__ == "__main__":
    main()
