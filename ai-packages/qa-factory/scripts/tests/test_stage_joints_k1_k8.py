#!/usr/bin/env python3
"""k1 k8: a part of test_stage_joints.py, split by tools/test_split.py (TD-11c). The shared helpers are in stage_joints_common."""
import copy
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import PLUGIN_ROOT, check_eq, check_in, check_not_in, cleanup, finish, temp_dir  # noqa: E402
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))
import stage_joints as SJ  # noqa: E402
from stage_joints_common import (  # noqa: E402
    ENV, PINS, REAL, UNI, audit, kind_keys, member, mutated, row_of, text_of,
)


def k1_real_tree() -> None:
    report = audit(pins=PINS)
    check_eq("K1: the real tree is green (every leg, every direction)", report.problems, [])
    print(report.line())
    check_in("K1: the summary line names the walk, the rows, the gaps by leg, the joints and the stages with no detector",
            f"walked exit 8, detector 5, window 28 | rows {len(REAL['joints'])}, gaps ", report.line())
    check_eq("K1: the rows file holds 287 rows (40 of T1 + 227 landed by T1r; +1 acceptance:novelty_question, C3-b1; +1 manifest_put:probe_owed; +4 T9c conductor rows; +12 by T1r-cards-a, TBW-T1rc-int t-1236; +1 manifest_put:node_id, RD1-19; +1 manifest_put:claim_then_pairs, RD1-34); a change is a named change of the file",
             len(REAL["joints"]), 287)
    check_in("K1/E5: a stage with no detector is reported, not invented",
             "stages with no detector: S0, S1, S6, S7, S9", report.line())
    check_eq("K1: no walk error on the real tree", UNI[1], [])
    check_in("K3/m-3: the line says the window rows with a code producer walk the code leg only", "role leg not walked (code-to-code rows): 27",
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
    check_eq("K1: the universe is exactly 8 + 5 + 28 keys", len(UNI[0]), 41)
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
    stale = text_of(audit(data=mutated(lambda d: (d["joints"].append(
        {**copy.deepcopy(row_of(d, "acceptance:review")), "check": "exit_gate:gone"}), d["told_ratchet"].update(unsited=0)))))
    check_in("K5/E3: a row whose check the walk does not meet is stale", "row exit_gate:gone: stale", stale)
    two = text_of(audit(data=mutated(lambda d: d["joints"].append(copy.deepcopy(d["joints"][0])))))
    check_in("K5/E4: two rows for one check", "exit_gate:scoped has two rows", two)
    old = text_of(audit(data=mutated(lambda d: (row_of(d, "exit_gate:scoped").update(check="exit:scoped_errors"),
                                                d["told_ratchet"].update(unsited=0)))))
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
    # TBW-T1rc-int (t-1236): a page-only entry owes no tokens (T1r), and after the Lead decision F1 no real entry is told by a path, so
    # the subject of these two lines is judged on a mutated copy of the grounding row told by a path (the carrier the demands leg still judges).
    by_path = {"told": [{"path": "references/slices/<role>/handoff-keys.md", "anchor": "## Outputs"}], "demands": []}
    check_in("K6/E1 demands: nothing demanded of a role told by a path and no gap is red",
             "the demands leg is missing for qa-requirements-tester",
             text_of(audit(data=mutated(lambda d: grounding(d).update(by_path)))))
    gap = {"leg": "demands", "ref": "F6-51/9", "why": "a test gap on the demands leg of this role entry"}
    check_eq("K6: the same missing demands leg WITH a declared gap is green (an informed pass)",
             audit(data=mutated(lambda d: grounding(d).update(by_path, gap=gap))).problems, [])
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


def main() -> None:
    k1_real_tree()
    k2_k3_pins()
    k4_k5_directions()
    k6_legs()
    k7_reach()
    k8_direction_c()
    finish("test_stage_joints_k1_k8")


# split: runner piece 1
if __name__ == "__main__":
    main()
