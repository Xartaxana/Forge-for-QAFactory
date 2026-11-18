#!/usr/bin/env python3
"""v2 rows: a part of test_stage_joints.py, split by tools/test_split.py (TD-11c). The shared helpers are in stage_joints_common."""
import copy
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import PLUGIN_ROOT, check, check_eq, check_in, cleanup, finish, temp_dir  # noqa: E402
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))
import null_outcomes as NO  # noqa: E402
import stage_joints as SJ  # noqa: E402
from stage_joints_common import (  # noqa: E402
    ENV, PINS, REAL, UNI, a_row, a_rows_file, audit, cli, kind_keys, member, mutated, row_of, text_of,
)


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
    real_rows = SJ.rows_for(runner, ["*"])
    check_eq("rows-for/real: since T1r the runner is told rows (112 today: +4 by T1r-cards-a, TBW-T1rc-int t-1236), each stating a requirement; +4 T9c conductor rows: with no facts the conductor is told all four, none of them the runner's",
             (len(real_rows), all(r.get("requirement") or r.get("requirement_from") for r in real_rows),
              [r["check"] for r in SJ.rows_for("conductor", ["*"])]),
             (112, True, ["no_move:options", "no_move:prose", "no_move:class", "no_move:args"]))


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
    check_eq("told-text/role-commands.json: a command row is told as a pointer to its card (T1r-pages: the card itself is `--help` and the refusal)",
             said, SJ.COMMANDS_TEXT.format(command=command, script=command.split()[0]))
    for label, row in (("an unknown carrier", {"check": "a:x", "requirement_from": "my.table"}),
                       ("a carrier key that names nothing", {"check": "a:x", "requirement_from": "validate_artifacts.PHASE_JSON_KEYS", "carrier_key": "no-such"}),
                       ("a command that names nothing", {"check": "a:x", "requirement_from": "role-commands.json", "carrier_key": "no such command"}),
                       ("a row with no requirement", {"check": "a:x"}), ("a row that is no object", None)):
        text, door = SJ.told_text(row)
        check(f"told-text/unreadable: {label} reads as a sentence saying so, never an exception or an empty text",
              "could not be read" in text and "this is a factory defect" in text and door == "", text)
    check_eq("told-line/form: `- [<check>] <expected> Door: <door>.`", SJ.told_line(own), "- [a:x] Say it. Door: edit <ID> in <home>.")
    for label, said, line in (("no final stop: the stop is added", "carried x", "- [a:x] carried x. Door: d."),
                              ("ends in a backtick: the stop follows it", "keys `a`", "- [a:x] keys `a`. Door: d."),
                              ("ends in a closing bracket: the stop follows it", "keys (a)", "- [a:x] keys (a). Door: d."),
                              ("ends in `!` or `?`: no second stop", "stop!", "- [a:x] stop! Door: d."),
                              ("ends in `.` after trailing blanks: no second stop", "stop.  ", "- [a:x] stop. Door: d.")):
        check_eq(f"told-line/stop: {label}", SJ.told_line({"check": "a:x", "requirement": said, "door": "d"}), line)
    carrier = {"check": "a:x", "requirement_from": "validate_artifacts.PHASE_JSON_KEYS", "carrier_key": artifact, "door": "d"}
    check_eq("told-line/stop: a carrier row (no final stop of its own) renders `...x. Door: d.`", SJ.told_line(carrier),
             f"- [a:x] `{artifact}` carries the keys " + ", ".join(f"`{k}`" for k in keys) + ". Door: d.")
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
    check_eq("rename/pins: the real universe is 8 exit, 5 detector, 28 window keys", [len(kind_keys(k)) for k in SJ.KINDS], [8, 5, 28])
    check_eq("rename/pins: the 8 exit keys", kind_keys("exit"), [
        "exit_gate:case_identity", "exit_gate:detector_errors", "exit_gate:digest", "exit_gate:grounding", "exit_gate:required_outputs",
        "exit_gate:scoped", "exit_gate:text_end_after_handback", "exit_gate:witness_errors"])
    check_eq("rename/pins: the 5 detector keys", kind_keys("detector"),
             ["branch_accounting:*", "check_coverage:*", "critic_rollcall:*", "planning_contract:*", "s5_precheck:*"])
    check_eq("rename/pins: every key of the universe has a row (the file also holds the 227 rows of T1r for sites outside the universe)",
             sorted(set(UNI[0]) - {r["check"] for r in REAL["joints"]}), [])
    check_eq("rename/pins: no row key is used twice", len({r["check"] for r in REAL["joints"]}), len(REAL["joints"]))
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
    check_eq("merge/branch-accounting: since T1r its case-critic leg is told by the key page, so gap F6-51/4 is gone and no gap is left",
             ([p["gap"]["ref"] for p in rows[0]["producers"] if p.get("gap")],
              [t for p in rows[0]["producers"] for t in p.get("told", [])]),
             ([], [{"path": "references/slices/<role>/handoff-keys.md", "anchor": "## Outputs"}] * 5))
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
    v2_reader()
    lookups()
    renderers()
    light_import()
    rename()
    merges()
    exit_gate_sites()
    finish("test_stage_joints_v2_rows")


# split: runner piece 1
if __name__ == "__main__":
    main()
