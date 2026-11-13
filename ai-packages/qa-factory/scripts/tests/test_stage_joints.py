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
import contextlib
import copy
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import PLUGIN_ROOT, check, check_eq, check_in, check_not_in, cleanup, finish, run_script, temp_dir  # noqa: E402

sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))
import null_outcomes as NO  # noqa: E402
import stage_joints as SJ  # noqa: E402

# The walk sizes. A change of any is a change of the factory's checks and the Lead's question: the walker is not adjusted
# to agree with the tree. exit: the 8 families of all_errors + main; detector: the 5 scripts of the 9 tuples of stages.json
# (minus the adviser sizing.py; `branch_accounting.py` runs at 4 stages and is ONE member); window: 27 distinct gap kinds
# of validate_window (30 append sites, `expectation_change_gaps` from extend).
PINS = {"exit": 8, "detector": 5, "window": 27}
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


def k1_real_tree() -> None:
    report = audit(pins=PINS)
    check_eq("K1: the real tree is green (every leg, every direction)", report.problems, [])
    print(report.line())
    check_in("K1: the summary line names the walk, the rows, the gaps by leg, the joints and the stages with no detector",
            "walked exit 8, detector 5, window 27 | rows 40, gaps ", report.line())
    check_in("K1/E5: a stage with no detector is reported, not invented",
             "stages with no detector: S0, S1, S6, S7, S9", report.line())
    check_eq("K1: no walk error on the real tree", UNI[1], [])
    check_in("K3/m-3: the line says the window rows with a code producer walk the code leg only", "role leg not walked (code-to-code rows): 26",
             report.line())
    windows = kind_keys("window")
    check_eq("K3/m-3: every window row with a code producer says so in the data (acceptance:quality has no producer: a gap, not code-to-code)",
             sorted(r["check"] for r in REAL["joints"] if r["check"] in windows
                    and all(p.get("role_leg") == "not walked" for p in r["producers"])),
             sorted(k for k in windows if k != "acceptance:quality"))
    check_in("K3/m-3: a role_leg value other than `not walked` is red", "`role_leg` is only `not walked`",
             text_of(audit(data=mutated(lambda d: [p.update(role_leg="walked") for r in d["joints"] if r["check"] in windows
                                                   for p in r["producers"]][:1], False))))
    check_in("K3/m-3: F6-51/5 is on the producer leg", "producer",
             json.dumps([p["gap"]["leg"] for r in REAL["joints"] for p in r["producers"] if (p.get("gap") or {}).get("ref") == "F6-51/5"]))
    check_eq("K1: the universe is exactly 8 + 5 + 27 keys", len(UNI[0]), 40)
    check_not_in("K1: the adviser sizing is not a blocking detector", "sizing:*", " ".join(UNI[0]))
    check_not_in("K1/X2-3: the form check left the stop (a stop no longer refuses the handover form; `finish` does)",
                 "form_stop_errors", " ".join(UNI[0]))


def k2_k3_pins() -> None:
    check_eq("K2: the pins hold AT their values", audit(pins=PINS).problems, [])
    for kind, size in PINS.items():
        for pinned in (size - 1, size + 1):
            check_in(f"K3: {kind} pinned {pinned} (real {size}) is red, in both directions",
                     f"{kind} checks: {size}, pinned {pinned}", text_of(audit(pins={**PINS, kind: pinned})))
    stub = ({k: v for k, v in UNI[0].items() if k != "exit_gate:digest"}, [])
    check_in("K3: a stubbed universe one exit family short is red against the pin", "exit checks: 7, pinned 8",
             text_of(audit(uni=stub, pins=PINS)))


def k4_k5_directions() -> None:
    plus = ({**UNI[0], "exit_gate:new": member("exit", "exit_gate.py::all_errors:1")}, [])
    out = text_of(audit(uni=plus))
    check_in("K4/E2: a check in code with no row is red, naming the key", "exit_gate:new is a check in code", out)
    check_in("K4: naming where the code meets it", "(exit_gate.py::all_errors:1)", out)
    check_in("K4: and saying what to add", "has no row in references/stage-joints.json", out)
    stale = text_of(audit(data=mutated(lambda d: d["joints"].append(
        {**copy.deepcopy(d["joints"][0]), "check": "exit_gate:gone"}))))
    check_in("K5/E3: a row whose check the walk does not meet is stale", "row exit_gate:gone: stale", stale)
    two = text_of(audit(data=mutated(lambda d: d["joints"].append(copy.deepcopy(d["joints"][0])))))
    check_in("K5/E4: two rows for one check", "exit_gate:scoped has two rows", two)
    old = text_of(audit(data=mutated(lambda d: row_of(d, "exit_gate:scoped").update(check="exit:scoped_errors"))))
    check_in("rename/old-prefix-key: a row in the old prefix form is stale, never matched to its family", "row exit:scoped_errors: stale", old)
    check_in("rename/old-prefix-key: and the family has no row", "exit_gate:scoped is a check in code", old)


def k6_legs() -> None:
    quality = lambda d: row_of(d, "acceptance:quality")["producers"][0]
    handback = lambda d: row_of(d, "exit_gate:text_end_after_handback")["producers"][0]
    grounding = lambda d: row_of(d, "exit_gate:grounding")["producers"][0]
    check_in("K6/E1 producer: no writer and no gap is red",
             "the producer leg is missing and no gap is declared", text_of(audit(data=mutated(
                 lambda d: quality(d).pop("gap")))))
    check_in("K6/E1 told: no place and no gap is red", "the told leg is missing and no gap is declared",
             text_of(audit(data=mutated(lambda d: handback(d).pop("gap")))))
    check_in("K6/E1 demands: nothing demanded of a role and no gap is red",
             "the demands leg is missing for qa-requirements-tester",
             text_of(audit(data=mutated(lambda d: grounding(d).update(demands=[])))))
    gap = {"leg": "demands", "ref": "F6-51/9", "why": "a test gap on the demands leg of this role entry"}
    check_eq("K6: the same missing demands leg WITH a declared gap is green (an informed pass)",
             audit(data=mutated(lambda d: grounding(d).update(demands=[], gap=gap))).problems, [])
    check_in("K6: a gap declared on a complete leg is red, saying to remove it",
             "gap declared on a complete leg (demands) - remove it",
             text_of(audit(data=mutated(lambda d: grounding(d).update(gap=gap)))))
    check_in("K6: a gap whose ref points at nothing is red", "gap ref 'soon' is not",
             text_of(audit(data=mutated(lambda d: quality(d).update(gap={**quality(d)["gap"], "ref": "soon"})))))
    check_in("K6: a gap with a short reason is red", "gap `why` is shorter than 30",
             text_of(audit(data=mutated(lambda d: quality(d).update(gap={**quality(d)["gap"], "why": "later"})))))
    check_in("K6: a row with no producer entry is red", "`producers` is empty",
             text_of(audit(data=mutated(lambda d: row_of(d, "acceptance:review").update(producers=[])))))
    check_in("K6: an unknown entry key is red", "has an unknown key `colour`",
             text_of(audit(data=mutated(lambda d: grounding(d).update(colour="red")))))
    check_in("K6: a role with no agent file is red", "role `qa-ghost` has no agents/qa-ghost.md",
             text_of(audit(data=mutated(lambda d: grounding(d).update(roles=["qa-ghost"])))))
    check_in("K6: a detector row at another stage than its script's is red", "a detector row runs at the stages whose detectors list its script: S5",
             text_of(audit(data=mutated(lambda d: row_of(d, "s5_precheck:*").update(stages=["S4"])))))
    check_in("K6: a row that runs at no stage is red", "a check that runs at no stage",
             text_of(audit(data=mutated(lambda d: row_of(d, "acceptance:review").update(stages=[])))))
    code_sites()


def code_sites() -> None:
    """The `code:` producer: a name only in a comment or a string, a line number, a missing file are all red."""
    tmp = temp_dir("qa-joints-code-")
    try:
        scripts = tmp / "scripts"
        scripts.mkdir()
        (scripts / "mod.py").write_text('def build():\n    """build()"""\n    return 1\n# build(2)\nX = "build(3)"\n'
                                        "# def ghost():\n" 'Y = "def ghost2():"\n', encoding="utf-8")
        env = copy.copy(ENV)
        env.plugin, env.scripts = tmp, scripts
        def entry(code_ref, told="scripts/mod.py"):
            return {"code": code_ref, "field": "a test field", "told": [{"path": told}], "demands": []}
        def problems(e):
            return SJ._entry_problems("acceptance:x", 0, e, env)[0]
        check_in("K6 code: a name only in a comment is not a definition", "no function `ghost`", " | ".join(problems(entry("mod.py::ghost"))))
        check_in("K6 code: a name only in a string is not a definition", "no function `ghost2`", " | ".join(problems(entry("mod.py::ghost2"))))
        check_in("K6 code: a line number in the site is refused", "is not `<scripts file>.py::<function>`", " | ".join(problems(entry("mod.py:12"))))
        check_in("K6 code: a missing file is refused", "cannot be read", " | ".join(problems(entry("nofile.py::build"))))
        check_in("K6 code: a docstring, a comment and a string that spell `build(` are no call",
                 "no call of `build` outside its own definition", " | ".join(problems(entry("mod.py::build"))))
        (scripts / "mod.py").write_text('def build():\n    return 1\n\n\ndef run():\n    return build()\n', encoding="utf-8")
        env._texts.clear(), env._trees.clear()
        check_eq("K6 code (positive control): a real call outside the definition makes the producer called", problems(entry("mod.py::build")), [])
        check_in("K6 code: a told file outside scripts/ is refused", "called in a `scripts/*.py` file",
                 " | ".join(problems(entry("mod.py::build", told="scripts/tests/t.py"))))
        check_in("K6 code: an anchor means nothing for a code producer", "an anchor has no meaning",
                 " | ".join(problems({**entry("mod.py::build"), "told": [{"path": "scripts/mod.py", "anchor": "x"}]})))
    finally:
        cleanup(tmp)


def k7_reach() -> None:
    entry = {"roles": ["qa-automator"]}
    item = {"path": "agents/qa-runner.md", "anchor": "## Outputs"}
    check_in("K7/E15: another role's agent file is not read by this role", "is not read by qa-automator",
             " | ".join(SJ._reach_problems(entry, item, ENV)))
    check_eq("K7: a slice the injection map lists for the role is read by it",
             SJ._reach_problems(entry, {"path": "references/slices/qa-automator/artifact-contract-automation.md",
                                        "anchor": "automation"}, ENV), [])
    check_in("K7: an existing file that the map does not deliver to the role is not read by it", "is not read by qa-automator",
             " | ".join(SJ._reach_problems(entry, {"path": "references/slices/qa-runner/common-rules.md", "anchor": "x"}, ENV)))
    check_in("K7: an anchor absent from a file the role reads is red", "the anchor 'no such phrase here' is not in the file",
             " | ".join(SJ._reach_problems(entry, {"path": "agents/<role>.md", "anchor": "no such phrase here"}, ENV)))
    check_in("K7: a file that does not exist is red", "the file does not exist",
             " | ".join(SJ._reach_problems(entry, {"path": "references/slices/<role>/ghost.md", "anchor": "x"}, ENV)))
    check_in("K7: an entry with no anchor is red", "`anchor` is missing",
             " | ".join(SJ._reach_problems(entry, {"path": "agents/<role>.md"}, ENV)))
    check_eq("K7: `<role>` is expanded for each role of the entry",
             SJ._reach_problems({"roles": ["qa-scout", "qa-runner"]}, {"path": "agents/<role>.md", "anchor": "<!-- gen:digest contract_slices.py -->"}, ENV), [])


def k8_direction_c() -> None:
    base = {"roles": ["qa-requirements-tester"], "told": [{"path": "agents/<role>.md", "anchor": "## Outputs"}],
            "demands_from": None}
    check_in("K8: a demanded token absent from every told file is red", "qa-requirements-tester is not told `zz_not_a_token_zz`",
             " | ".join(SJ._demands_leg("exit_gate:x", {**base, "demands": ["zz_not_a_token_zz"]}, ENV)))
    check_eq("K8: a token present in a told file is green", SJ._demands_leg("exit_gate:x", {**base, "demands": ["derived"]}, ENV), [])
    check_in("K8: an unknown carrier is red", "`demands_from` 'my.table' is not one of",
             " | ".join(SJ._demands_leg("exit_gate:x", {**base, "demands": [], "demands_from": "my.table"}, ENV)))
    tokens, why = SJ.demand_tokens("stages.json:required_outputs", "qa-scout", "exit_gate:x", ENV)
    check_eq("K8: required_outputs are read through the stage model, by file name", (tokens, why),
             (["context-manifest.json", "context-bundle.json"], ""))
    check_eq("K8: PHASE_JSON_KEYS are read for the artifacts the role writes",
             SJ.demand_tokens("validate_artifacts.PHASE_JSON_KEYS", "qa-automator", "exit_gate:x", ENV)[0], ["tests", "run_witness"])
    check_eq("K8: the detector scripts of a role exclude its advisers",
             SJ.demand_tokens("stages.json:detectors", "qa-requirements-tester", "exit_gate:x", ENV)[0], ["branch_accounting.py"])
    check_eq("demands/check-script-stem: the `check:script` token is `<stem>.py` of the `<stem>:*` key, whatever the stage",
             [SJ.demand_tokens("check:script", "qa-test-strategist", key, ENV) for key in ("branch_accounting:*", "s5_precheck:*")],
             [(["branch_accounting.py"], ""), (["s5_precheck.py"], "")])
    check_in("K8: a carrier that yields nothing for a role is red (a stale entry, not a pass)",
             "the demands leg is missing for qa-retro-analyst",
             " | ".join(SJ._demands_leg("exit_gate:x", {**base, "roles": ["qa-retro-analyst"], "demands": [],
                                                         "demands_from": "stages.json:detectors"}, ENV)))
    check_eq("K8/E16: direction C does not run on a code producer",
             SJ._demands_leg("acceptance:x", {"code": "window_record.py::build", "told": [], "demands": ["zz"]}, ENV), [])


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
                           ("told_ratchet", {"hand_cards": 12}, "`told_ratchet` is not an object holding exactly hand_cards, legacy_legs"),
                           ("told_ratchet", {"hand_cards": 12, "legacy_legs": -1}, "told_ratchet.legacy_legs is -1, a count"),
                           ("told_ratchet", {"hand_cards": True, "legacy_legs": 9}, "told_ratchet.hand_cards is True, a count")):
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


def cli(*args) -> tuple:
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = SJ.main(list(args))
    return code, out.getvalue()


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


def a_row(check: str, roles=("qa-runner",), stages=("S5",), **extra) -> dict:
    """A synthetic v2 row (a producer entry that names `roles`, told by the page); `extra` sets requirement, when, door ..."""
    return {"check": check, "stages": list(stages), "joint": None, **extra,
            "producers": [{"roles": list(roles), "field": "a field", "told": [{"page": True}], "demands": []}]}


def a_rows_file(*rows) -> dict:
    return {"schema_version": 2, "when_kinds": list(REAL["when_kinds"]), "joints": list(rows)}


def v2_reader() -> None:
    """X5: `load_rows` is the one reader: schema 2 read, schema 1 / other / absent / broken named, never a pass (AR-28)."""
    tmp = temp_dir("qa-joints-v2-")
    try:
        def put(name: str, body) -> Path:
            path = tmp / name
            path.write_text(body if isinstance(body, str) else json.dumps(body), encoding="utf-8")
            return path
        check_eq("v2/accepted: a schema-2 file is read whole", SJ.load_rows(put("ok.json", REAL)), (REAL, ""))
        check_eq("v2/accepted: the real file is schema 2 and `path=None` is the module's DATA", (REAL["schema_version"], SJ.load_rows()[0] == REAL), (2, True))
        v1 = put("one.json", {**REAL, "schema_version": 1})
        check_eq("v2/v1-refused: a schema-1 file is `(None, why)` with the sentence", SJ.load_rows(v1), (None, "one.json has schema_version 1; this reader reads 2"))
        for label, version in (("a bool", True), ("2.0", 2.0), ("a text", "2"), ("absent", None)):
            body = {k: v for k, v in REAL.items() if k != "schema_version"} if version is None else {**REAL, "schema_version": version}
            check_eq(f"v2/v1-refused: schema_version {label} is refused", SJ.load_rows(put("x.json", body))[0], None)
        report = SJ.audit(path=v1, uni=UNI, env=ENV)
        check_eq("v2/v1-refused: audit is red with the sentence and walks nothing", (report.problems, report.counts["rows"]),
                 (["stage-joints: one.json has schema_version 1; this reader reads 2"], 0))
        code, out = cli("--data", str(v1))
        check_eq("v2/v1-refused: the CLI exits 3 (UNREADABLE), the same as for a lost file", (code, out.startswith("UNREADABLE: ")), (3, True))
        check_eq("v2/v1-refused: threshold() is None, not a number read out of a file of another schema", SJ.threshold(v1), None)
        for label, body in (("absent", None), ("broken", "{not json")):
            path = put("b.json", body) if body is not None else tmp / "gone.json"
            why = NO.load_data(path)[1]
            check_eq(f"v2/{label}: the K10 text of `null_outcomes.load_data`, unchanged", (SJ.load_rows(path), bool(why)), ((None, why), True))
        check_eq("v2/not-object: an array is `(None, why)`", SJ.load_rows(put("arr.json", "[]")), (None, "arr.json is not an object"))
        empty = put("empty.json", {**REAL, "joints": []})
        check_eq("v2/empty-rows: an empty rows list is read (the walk is red on it), and no lookup finds anything",
                 (SJ.load_rows(empty)[0]["joints"], SJ.rows_for("qa-runner", ["*"], data=SJ.load_rows(empty)[0]),
                  SJ.row_for("a:x", SJ.load_rows(empty)[0])), ([], [], (None, "no row for a:x")))
        check_in("v2/empty-rows: audit is red naming it", "has no joint rows", text_of(SJ.audit(path=empty, uni=UNI, env=ENV)))
        saved = SJ.DATA
        try:
            SJ.DATA = tmp / "gone.json"
            check_eq("E3 runtime: a rows file that is absent gives `(None, why)` to the lookups and no rows to a page",
                     (SJ.row_for("exit_gate:scoped")[0], SJ.rows_for("qa-runner", ["*"])), (None, []))
            check_in("E3 runtime: and says why", "gone.json cannot be read", SJ.row_for("exit_gate:scoped")[1])
        finally:
            SJ.DATA = saved
    finally:
        cleanup(tmp)


def lookups() -> None:
    """`row_for` and `rows_for`: found / absent / two; role, stage, capability; requirement XOR; the conductor; unknown kinds."""
    a, star = a_row("a:x"), a_row("b:*")
    data = a_rows_file(a, star, a_row("a:x", roles=("qa-scout",)), a_row("c:z"))
    check_eq("row-for/found: the row keyed by exactly the id", SJ.row_for("c:z", data), (data["joints"][3], ""))
    check_eq("row-for/found: else the row of its namespace `<stem>:*`", SJ.row_for("b:anything", data), (star, ""))
    check_eq("row-for/absent: no row is `(None, why)`", SJ.row_for("q:z", data), (None, "no row for q:z"))
    check_eq("row-for/two: two rows for one id give the first and say so", SJ.row_for("a:x", data), (a, "two rows"))
    check_eq("row-for/found: the real rows by their v2 keys", [SJ.row_for(k)[1] for k in ("exit_gate:scoped", "branch_accounting:*", "acceptance:quality")],
             ["", "", ""])

    say = {"requirement": "Say it."}
    runner, critic = "qa-runner", "qa-case-critic"        # a role with Bash, a role without
    data = a_rows_file(a_row("a:shell", when=["shell"], **say), a_row("a:no-shell", roles=(runner, critic), when=["no_shell"], **say),
                       a_row("a:always", roles=(runner, critic), **say), a_row("a:s9", stages=("S9",), **say),
                       a_row("a:any-stage", roles=(runner, critic), stages=("*",), **say), a_row("a:other-role", roles=("qa-scout",), **say))
    ids = lambda role, stages, facts=None: [r["check"] for r in SJ.rows_for(role, stages, facts, data=data)]
    check_eq("rows-for/role-stage-capability: the role, a stage of the call and a shell the role has",
             ids(runner, ["S5"]), ["a:shell", "a:always", "a:any-stage"])
    check_eq("rows-for/role-stage-capability: a role with no shell gets `no_shell` rows, not `shell` rows", ids(critic, ["S5"]),
             ["a:no-shell", "a:always", "a:any-stage"])
    check_eq("rows-for/role-stage-capability: `*` in the call is every stage; a row of stage `*` is at every stage",
             ids(runner, ["*"]), ["a:shell", "a:always", "a:s9", "a:any-stage"])
    check_eq("rows-for/role-stage-capability: a row names its roles in a producer; a role no row names gets none", ids("qa-nobody", ["*"]), [])
    both = a_row("x:both", requirement="r", requirement_from="handoff_form")
    check_eq("rows-for/requirement-only: only a row that states a requirement, one way; none, both, or blanks are not told",
             [r["check"] for r in SJ.rows_for(runner, ["S5"], data=a_rows_file(
                 a_row("x:none"), both, a_row("x:blank", requirement="  "), a_row("x:own", requirement="r"),
                 a_row("x:from", requirement_from="handoff_form")))], ["x:own", "x:from"])
    star_row = a_row("x:star", roles=("*",), **say)
    star_data = a_rows_file(star_row, a_row("x:cond", roles=("conductor",), stages=("*",), **say))
    check_eq("rows-for/role-stage-capability: `roles: [\"*\"]` is the roles of inject-map.json, never the conductor",
             [[r["check"] for r in SJ.rows_for(role, ["S5"], data=star_data)] for role in (runner, "conductor", "qa-nobody")],
             [["x:star"], ["x:cond"], []])
    cond = a_rows_file(*(a_row(f"c:{n}", roles=("conductor",), stages=("*",), when=[w], **say)
                         for n, w in (("answer", "conductor_answer"), ("m1", "move:m1"), ("m2", "move:m2"))))
    conductor = lambda facts: [r["check"] for r in SJ.rows_for("conductor", ["*"], facts, data=cond)]
    check_eq("rows-for/conductor: with the open moves only `conductor_answer` and the open `move:<id>` hold",
             (conductor({"moves": ["m1"]}), conductor({"moves": []}), conductor({})), (["c:answer", "c:m1"], ["c:answer"], ["c:answer"]))
    check_eq("rows-for/conductor: with no facts every group is returned (the page)", conductor(None), ["c:answer", "c:m1", "c:m2"])
    unknown = a_rows_file(a_row("u:zz", when=["zz_kind"], **say), a_row("u:plan", when=["plan"], **say))
    check_eq("rows-for/unknown-kind: an unknown `when` token holds (more text, never an omitted row); a stated dispatch fact decides",
             ([r["check"] for r in SJ.rows_for(runner, ["S5"], data=unknown)], [r["check"] for r in SJ.rows_for(runner, ["S5"], {}, data=unknown)],
              [r["check"] for r in SJ.rows_for(runner, ["S5"], {"plan": False}, data=unknown)],
              [r["check"] for r in SJ.rows_for(runner, ["S5"], {"plan": True}, data=unknown)]),
             (["u:zz", "u:plan"], ["u:zz", "u:plan"], ["u:zz"], ["u:zz", "u:plan"]))
    check_eq("rows-for/real: the 40 rows of today state no requirement, so no receiver is told one by this reader yet",
             [SJ.rows_for(role, ["*"]) for role in (runner, "conductor")], [[], []])


def renderers() -> None:
    """`told_text`, `told_line`, `fill`: the one composer, the one line, the placeholders."""
    import role_cli
    import validate_artifacts
    import window_record
    own = {"check": "a:x", "requirement": "  Say it.  ", "door": "edit <ID> in <home>"}
    check_eq("told-text/requirement: the sentence and the door", SJ.told_text(own), ("Say it.", "edit <ID> in <home>"))
    check_eq("told-text/handoff_form: the form sentence", SJ.told_text({"check": "a:x", "requirement_from": "handoff_form", "door": "d"}),
             (SJ.FORM_TEXT, "d"))
    artifact = next(a for a, k in validate_artifacts.PHASE_JSON_KEYS.items() if k)
    keys = validate_artifacts.PHASE_JSON_KEYS[artifact]
    check_eq("told-text/PHASE_JSON_KEYS: `<carrier_key>` carries the keys of the validator's table",
             SJ.told_text({"check": "a:x", "requirement_from": "validate_artifacts.PHASE_JSON_KEYS", "carrier_key": artifact})[0],
             f"`{artifact}` carries the keys " + ", ".join(f"`{k}`" for k in keys))
    fields = SJ.told_text({"check": "a:x", "requirement_from": "window_record.REQUIRED_ROW_FIELDS"})[0]
    check_eq("told-text/REQUIRED_ROW_FIELDS: every field of the carrier, in its order, with its own words, joined by `; `",
             fields, "; ".join(f"`{n}`: {s.what}" for n, s in window_record.REQUIRED_ROW_FIELDS.items()))
    command = next(name for name, found in role_cli.registry().items() if found.get("input") and found.get("verify"))
    said = SJ.told_text({"check": "a:x", "requirement_from": "role-commands.json", "carrier_key": command})[0]
    check_eq("told-text/role-commands.json: the command's `input` and `verify`",
             said, f"{role_cli.entry(command)['input']}; how to prove it: {role_cli.entry(command)['verify']}")
    for label, row in (("an unknown carrier", {"check": "a:x", "requirement_from": "my.table"}),
                       ("a carrier key that names nothing", {"check": "a:x", "requirement_from": "validate_artifacts.PHASE_JSON_KEYS", "carrier_key": "no-such"}),
                       ("a command that names nothing", {"check": "a:x", "requirement_from": "role-commands.json", "carrier_key": "no such command"}),
                       ("a row with no requirement", {"check": "a:x"}), ("a row that is no object", None)):
        text, door = SJ.told_text(row)
        check(f"told-text/unreadable: {label} reads as a sentence saying so, never an exception or an empty text",
              "could not be read" in text and "this is a factory defect" in text and door == "", text)
    check_eq("told-line/form: `- [<check>] <expected> Door: <door>.`", SJ.told_line(own), "- [a:x] Say it. Door: edit <ID> in <home>.")
    check_eq("told-line/form: `fill` is applied when values are given", SJ.told_line(own, {"ID": "d-1", "home": "/q"}),
             "- [a:x] Say it. Door: edit d-1 in /q.")
    check_eq("fill/missing-value-kept: a missing, empty or None value leaves its placeholder; other angle words stay",
             SJ.fill("<T> <ID> <home> <X>", {"T": "QA-1", "ID": "", "home": None}), "QA-1 <ID> <home> <X>")
    check_eq("fill/missing-value-kept: no values at all changes nothing", (SJ.fill("<T> x", None), SJ.fill("<T> x", {})), ("<T> x", "<T> x"))


def light_import() -> None:
    """import/light: the retro reads `threshold()` and must not import the walker's graph; the readers import nothing heavy."""
    import subprocess
    heavy = ("null_outcomes", "stage_guard", "inject_context", "validate_artifacts", "acceptance", "host_adapter", "window_record",
             "role_cli", "hooklib", "detector_verdict", "console_io")
    code = (f"import sys; sys.path.insert(0, {str(PLUGIN_ROOT / 'scripts')!r}); import stage_joints; "
            f"print(sorted(m for m in {heavy!r} if m in sys.modules))")
    done = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, text=True, check=False)
    check_eq("import/light: importing stage_joints loads none of the walker's or the carriers' modules", (done.returncode, done.stdout.strip()),
             (0, "[]"))


def rename() -> None:
    """The rename of §3.4 and B2: no v1 key in code or data; kind and stages come from the producer, never the key's text."""
    import re
    pattern = re.compile(r"""["'f](exit|detector|window):""")
    check_eq("rename/no-v1-key: control - the pattern finds a v1 key in a fixture string",
             [bool(pattern.search(s)) for s in ('x = "exit:scoped_errors"', "f'detector:S2:qa:x.py'", 'k = "window:review"', 'k = "exit_gate:scoped"')],
             [True, True, True, False])
    scanned = [p for p in sorted((PLUGIN_ROOT / "scripts").glob("*.py")) if p.name != "machine_facts.py"] + [PLUGIN_ROOT / "references" / "stage-joints.json"]
    hits = [f"{p.name}:{n}" for p in scanned for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1) if pattern.search(line)]
    check_eq("rename/no-v1-key: no v1 key literal in the package's scripts or the rows file (machine_facts.py: `detector:{i}` is a secret scan's label)",
             hits, [])
    check_eq("rename/pins: the real universe is 8 exit, 5 detector, 27 window keys", [len(kind_keys(k)) for k in SJ.KINDS], [8, 5, 27])
    check_eq("rename/pins: the 8 exit keys", kind_keys("exit"), [
        "exit_gate:case_identity", "exit_gate:detector_errors", "exit_gate:digest", "exit_gate:grounding", "exit_gate:required_outputs",
        "exit_gate:scoped", "exit_gate:text_end_after_handback", "exit_gate:witness_errors"])
    check_eq("rename/pins: the 5 detector keys", kind_keys("detector"),
             ["branch_accounting:*", "check_coverage:*", "critic_rollcall:*", "planning_contract:*", "s5_precheck:*"])
    check_eq("rename/pins: every row of the file is a key of the universe and the other way round",
             sorted(r["check"] for r in REAL["joints"]), sorted(UNI[0]))
    check_eq("rename/pins: AT the pins nothing is red, ±1 is (all three kinds)", [SJ._pins(UNI[0], PINS)] + [
        len(SJ._pins(UNI[0], {**PINS, k: PINS[k] + d})) for k in PINS for d in (-1, 1)], [[], 1, 1, 1, 1, 1, 1])
    only = {"foo:*": member("detector", stages=["S2"])}
    check_eq("rename/kind-not-prefix: a member keyed `foo:*` of kind detector counts in the detector pin", SJ._pins(only, {"detector": 1, "exit": 0}), [])
    odd = {"detector:S9:x:y.py": member("exit")}
    check_eq("rename/kind-not-prefix: a member keyed `detector:S9:x:y.py` of kind exit counts as exit, not as a detector",
             SJ._pins(odd, {"exit": 1, "detector": 0, "window": 0}), [])
    check_eq("rename/kind-not-prefix: a key whose producer is unknown has no kind and is counted in no pin",
             SJ._pins({"exit_gate:ghost": {"kind": "mystery", "where": "w", "stages": None}}, {"exit": 0, "detector": 0, "window": 0}), [])
    check_eq("rename/kind-not-prefix: exit and window members carry `stages: None` (never `[]`), detector members their stages",
             ({m["stages"] is None for k, m in UNI[0].items() if m["kind"] != "detector"}, UNI[0]["branch_accounting:*"]["stages"]),
             ({True}, ["S2", "S3", "S4", "S5"]))
    counted = SJ.audit(uni=({"exit_gate:ghost": {"kind": "exit", "where": "w", "stages": None}}, []), env=ENV)
    check_in("rename/kind-not-prefix: audit counts by the member's kind", "walked exit 1, detector 0, window 0", counted.line())


def merges() -> None:
    """F4 (a): a detector script is one row; its stages are the stages of the model; no-detector reads the model."""
    rows = [r for r in REAL["joints"] if r["check"] == "branch_accounting:*"]
    check_eq("merge/branch-accounting: one row, four producers (one per stage the script runs at), stages S2-S5, joint null",
             (len(rows), [p["roles"] for p in rows[0]["producers"]], rows[0]["stages"], rows[0]["joint"]),
             (1, [["qa-requirements-tester"], ["qa-test-strategist"], ["qa-case-critic"], ["qa-automator"]], ["S2", "S3", "S4", "S5"], None))
    check_eq("merge/branch-accounting: its one gap (F6-51/4, the case critic) survived the merge",
             [p["gap"]["ref"] for p in rows[0]["producers"] if p.get("gap")], ["F6-51/4"])
    check_eq("merge/stages-from-model: the real rows are green", audit(pins=PINS).problems, [])
    short = text_of(audit(data=mutated(lambda d: row_of(d, "branch_accounting:*").update(stages=["S2", "S3", "S5"]))))
    check_in("merge/stages-from-model: with S4 removed from the row it is red, naming the stages the model gives",
             "a detector row runs at the stages whose detectors list its script: S2, S3, S4, S5", short)

    def without(script: str, stage: str):
        env = copy.copy(ENV)
        env.model = copy.deepcopy(ENV.model)
        for st in env.model["stages"]:
            if st["id"] == stage:
                st["detectors"] = {r: [s for s in v if s != script] for r, v in (st.get("detectors") or {}).items()}
        return env
    check_in("merge/stages-from-model: the stages are the MODEL's: with the model's S4 listing removed the full row is red",
             "list its script: S2, S3, S5", text_of(audit(env=without("branch_accounting.py", "S4"))))
    line = audit(pins=PINS).line()
    check_in("no-detector/from-model: the line names the stages no detector runs at", "stages with no detector: S0, S1, S6, S7, S9", line)
    check_eq("no-detector/from-model: a model with S8's detector removed adds S8 (from the model, not from the injected universe)",
             audit(env=without("check_coverage.py", "S8")).no_detector, ["S0", "S1", "S6", "S7", "S8", "S9"])
    check_eq("no-detector/from-model: the injected universe does not change it", audit(uni=({}, [])).no_detector, ["S0", "S1", "S6", "S7", "S9"])


def exit_gate_sites() -> None:
    """The producer side of the rename: `own` takes the full id at every call, and the text-end record carries its check."""
    import ast
    tree = ast.parse((PLUGIN_ROOT / "scripts" / "exit_gate.py").read_text(encoding="utf-8"))
    fn = next(f for f in tree.body if isinstance(f, ast.FunctionDef) and f.name == "all_errors")
    own = next(n for n in ast.walk(fn) if isinstance(n, ast.FunctionDef) and n.name == "own")
    check_eq("exit/own-call-sites: `own(records, check)` takes the check id", [a.arg for a in own.args.args], ["records", "check"])
    calls = [n for n in ast.walk(fn) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "own"]
    given = [c.args[1].value if len(c.args) == 2 and isinstance(c.args[1], ast.Constant) else None for c in calls]
    check_eq("exit/own-call-sites: the SEVEN call sites give a full id as a literal", sorted(map(str, given)), sorted([
        "exit_gate:scoped", "exit_gate:grounding", "exit_gate:case_identity", "exit_gate:digest", "exit_gate:required_outputs",
        "exit_gate:adviser", "exit_gate:adviser"]))
    record = next(c for c in ast.walk(tree) if isinstance(c, ast.Call) and isinstance(c.func, ast.Attribute) and c.func.attr == "Record"
                  and any(k.arg == "script" and getattr(k.value, "value", None) == "exit_gate_text_end" for k in c.keywords))
    check_eq("exit/text-end-check: the text-end record carries `exit_gate:text_end_after_handback`",
             [k.value.value for k in record.keywords if k.arg == "check"], ["exit_gate:text_end_after_handback"])
    import detector_verdict as DV
    check_eq("exit/text-end-check: and the contract reads that id from it",
             DV.check_id(DV.Record("t", script="exit_gate_text_end", check="exit_gate:text_end_after_handback")), "exit_gate:text_end_after_handback")


def main() -> None:
    k1_real_tree()
    k2_k3_pins()
    k4_k5_directions()
    k6_legs()
    k7_reach()
    k8_direction_c()
    k9_unreadable_shapes()
    k10_data_file()
    k11_ratchet()
    k12_joint_census()
    k13_threshold()
    k14_cli()
    v2_reader()
    lookups()
    renderers()
    light_import()
    rename()
    merges()
    exit_gate_sites()
    finish("test_stage_joints")


if __name__ == "__main__":
    main()
