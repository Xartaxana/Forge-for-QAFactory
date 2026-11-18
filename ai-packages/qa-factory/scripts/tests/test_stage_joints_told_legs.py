#!/usr/bin/env python3
"""told legs: a part of test_stage_joints.py, split by tools/test_split.py (TD-11c). The shared helpers are in stage_joints_common."""
import copy
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import PLUGIN_ROOT, check_eq, check_in, finish  # noqa: E402
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))
import stage_joints as SJ  # noqa: E402
from stage_joints_common import (  # noqa: E402
    ENV, PINS, REAL, UNI, a_row, audit, mutated, row_counts, row_of, text_of,
)


def told_leg_and_rows() -> None:
    """K2 (gated), K3, K7, E4, E7 on synthetic rows; `told/audit-shape`."""
    import contract_slices
    import no_move
    import role_rules
    kinds = list(REAL["when_kinds"])
    stage_ids = {str(s.get("id")) for s in ENV.model.get("stages") or []}
    asks = lambda row, **extra: SJ._row_requirement("a:x", {**row, **extra}, ENV, kinds)
    full = a_row("a:x", requirement="Say it.", door="edit <ID>")
    move = no_move.move_ids()[0]
    check_eq("K3/move-token: a `move:<id>` of a real move, a `when_kinds` token and `always` are green",
             [asks(full, when=[w]) for w in (f"move:{move}", "plan", "always")], [[], [], []])
    check_in("K3/move-token: a `move:<id>` that is no move is red", "names a move that is not in conductor-actions.json", " ".join(asks(full, when=["move:zz_nope"])))
    check_in("K3/move-token: a token that is no kind is red", "`when` token `zz_kind` is not in `when_kinds`", " ".join(asks(full, when=["zz_kind"])))
    check_in("K3/move-token: an empty `when` is red", "`when` is not a non-empty list of tokens", " ".join(asks(full, when=[])))
    check_eq("K3/shell-door: `door_needs: shell` with `shell` in `when` is green, with no shell in `when` red, an unknown value red",
             [bool(asks(full, door_needs="shell", when=w)) for w in (["shell"], ["always"])] + [bool(asks(full, door_needs="zz"))], [False, True, True])
    check_in("K3/shell-door: the sentence names the door a role cannot open", "a door a role without a shell cannot open", " ".join(asks(full, door_needs="shell")))
    check_in("K3/page-without-requirement: a row told by the page that states no requirement is red", "is told by the page but states no requirement",
             " ".join(asks(a_row("a:x"))))
    check_eq("K3/page-without-requirement: a row with neither field and no page is the legacy row, not red (E2)",
             asks({**a_row("a:x"), "producers": [{"roles": ["qa-runner"], "field": "f", "told": [{"path": "agents/<role>.md", "anchor": "x"}], "demands": []}]}), [])
    check_in("K3: both fields is red", "states its requirement two ways", " ".join(asks(full, requirement_from="handoff_form")))
    check_in("K3: no door is red", "names no `door`", " ".join(SJ._row_requirement("a:x", a_row("a:x", requirement="r"), ENV, kinds)))
    check_in("K3: an unknown carrier is red", "`requirement_from` 'my.table' is not one of",
             " ".join(SJ._row_requirement("a:x", a_row("a:x", requirement_from="my.table", door="d"), ENV, kinds)))
    rule = role_rules.load(PLUGIN_ROOT)[0][0]["id"]
    check_eq("K7/role-rule: an id of design/role-rules.json is green, an id that is not there is red",
             [bool(asks(full, role_rule=r)) for r in (rule, "no-such-rule-zz")], [False, True])
    check_in("K7/role-rule: the sentence names the id", "`role_rule` no-such-rule-zz is no id of design/role-rules.json", " ".join(asks(full, role_rule="no-such-rule-zz")))
    check_in("E4/empty-roles: a requirement nobody is told is red", "a requirement nobody is told - name the roles or remove the row",
             " ".join(asks({**full, "producers": [{"roles": [], "field": "f", "told": [], "demands": []}]})))
    check_in("E4/empty-roles: one entry with no roles beside one with roles is red too", "a requirement nobody is told",
             " ".join(asks({**full, "producers": full["producers"] + [{"roles": [], "field": "f", "told": [], "demands": []}]})))
    check_in("E7/two-rows: two rows for one id are red", "exit_gate:scoped has two rows",
             text_of(audit(data=mutated(lambda d: d["joints"].append(copy.deepcopy(row_of(d, "exit_gate:scoped")))))))
    check_in("E7/two-star-rows: two `<stem>:*` rows for one stem are red", "branch_accounting:* has two rows",
             text_of(audit(data=mutated(lambda d: d["joints"].append(copy.deepcopy(row_of(d, "branch_accounting:*")))))))
    # T1r: the `*` stage line and the page branch of the demands leg (the invariants: a mixed or unknown stage and a path entry with
    # no demands stay red; a page entry's tokens are still checked)
    one_row = lambda stages: SJ._row_problems(a_row("a:x", stages=stages, requirement="Say it.", door="d"), ENV, stage_ids, {}, kinds)[0]
    check_eq("stages-star/ok: the single item `*` (every stage) is green", [p for p in one_row(["*"]) if "stages" in p], [])
    check_in("stages-star/mixed-red: `*` beside a stage id is red", "`*` stands alone", " ".join(one_row(["*", "S3"])))
    check_in("stages-empty/red: an empty stage list stays red", "`stages` is empty", " ".join(one_row([])))
    check_in("stages-star/unknown-red: an unknown stage id stays red", "which are no stage of stages.json", " ".join(one_row(["S99"])))
    page = {"roles": ["qa-runner"], "field": "a field", "told": [{"page": True}], "demands": []}
    check_eq("demands-page/empty-ok: a page entry with no demands is no finding (the page carries the sentence)",
             SJ._demands_leg("a:x", page, ENV), [])
    check_in("demands-page/token-missing-red: a page entry's token is looked up on the key page and a missing one is red",
             "qa-runner is not told `zz_not_a_token_zz`", " ".join(SJ._demands_leg("a:x", {**page, "demands": ["zz_not_a_token_zz"]}, ENV)))
    check_eq("demands-page/token-present-ok: a token the key page holds is green", SJ._demands_leg("a:x", {**page, "demands": ["## Outputs"]}, ENV), [])
    check_in("demands-path/empty-red: a path entry with no demands stays red",
             "the demands leg is missing for qa-runner", " ".join(SJ._demands_leg("a:x", {
                 **page, "told": [{"path": "references/slices/<role>/handoff-keys.md", "anchor": "## Outputs"}]}, ENV)))
    # K2: the page leg is gated on the renderer
    env = copy.copy(ENV)
    env.load_map = {"common": [], "roles": {"qa-runner": [f"plugin:{SJ.KEY_PAGE.format(role='qa-runner')}"], "qa-scout": []}}
    row = a_row("a:x", roles=("qa-runner", "qa-scout"), requirement="Say it.", door="d")
    entry = row["producers"][0]
    check_eq("K2/gated-on: T3a's renderer is present in the real package", callable(getattr(contract_slices, SJ.PAGE_RENDERER, None)), True)
    real_renderer = getattr(contract_slices, SJ.PAGE_RENDERER)
    delattr(contract_slices, SJ.PAGE_RENDERER)                  # the gate both ways: the attribute taken away, then put back
    try:
        check_in("K2/gated-off: while `contract_slices` has no `requirement_section` a page item is refused", "the page renderer is not present",
                 " ".join(SJ._told_leg(entry, env, row)))
        check_in("K2/gated-off: through the audit of a whole row", "the page renderer is not present", " ".join(SJ._row_problems(row, env, stage_ids, {}, kinds)[0]))
    finally:
        setattr(contract_slices, SJ.PAGE_RENDERER, real_renderer)
    said = " ".join(SJ._told_leg(entry, env, row))
    check_in("K2/gated-on: with the renderer present the leg is real: a role whose list lacks its key page is red", "qa-scout does not receive", said)
    check_eq("K2/gated-on: and the role whose list holds it is green", "qa-runner" in said, False)
    check_eq("K2/gated-on: a role whose capability the row's `when` does not admit owes no page",
             SJ._told_leg({**entry, "roles": ["qa-case-critic"]}, env, {**row, "when": ["shell"]}), [])
    check_in("K2/gated-on: the conductor's section needs `conductor_answer` or a `move:<id>` in `when`", "selected by `conductor_answer`",
             " ".join(SJ._told_leg({**entry, "roles": ["conductor"]}, env, {**row, "when": ["always"]})))
    check_eq("K2/gated-on: and holds with it", SJ._told_leg({**entry, "roles": ["conductor"]}, env, {**row, "when": ["conductor_answer"], "stages": ["*"]}), [])
    check_in("K2/gated-off: a code producer is not told by a page", "a code producer is told where it is CALLED",
             " ".join(SJ._told_leg({"code": "x.py::f", "told": [{"page": True}]}, env, row)))
    check_in("K2: `page: 1` is no page item", "a told entry is not an object of path and anchor", " ".join(SJ._told_leg({**entry, "told": [{"page": 1}]}, env, row)))
    # told/audit-shape: audit never opens the census or the told fixture (the proof is the list of every file it opened)
    import builtins
    opened, real_read, real_open, real_builtin = [], Path.read_text, Path.open, builtins.open
    def read_text(self, *a, **k):
        opened.append(str(self))
        return real_read(self, *a, **k)
    def path_open(self, *a, **k):
        opened.append(str(self))
        return real_open(self, *a, **k)
    def builtin_open(file, *a, **k):
        opened.append(str(file))
        return real_builtin(file, *a, **k)
    SJ._IDS_CACHE.clear()
    Path.read_text, Path.open, builtins.open = read_text, path_open, builtin_open
    try:
        shaped = SJ.audit(copy.deepcopy(REAL), UNI, PINS, ENV)
    finally:
        Path.read_text, Path.open, builtins.open = real_read, real_open, real_builtin
    check_eq("told/audit-shape: control - the patched readers saw the files audit reads (the scanner's sources, the cards)",
             (len(opened) > 3, any(p.endswith("ahead-cards.json") for p in opened), any(p.endswith("exit_gate.py") for p in opened)), (True, True, True))
    check_eq("told/audit-shape: audit opened neither the census nor the told fixture, and its answer is the real tree's",
             ([p for p in opened if "judgment-census" in p or "told-ratchet" in p], shaped.problems), ([], []))


def t1rp() -> None:
    """T1r-pages: the pointer for a command row, the call marker (K2), the one decision `call_told`, the shape of the family list, K5's legs."""
    import io
    import role_cli
    key = next(k for k, f in role_cli.registry().items() if f.get("input") and f.get("verify"))
    row_of_cmd = lambda k: {"check": "role_cli:x", "requirement_from": "role-commands.json", "carrier_key": k, "door": "d"}
    check_eq("T1rp/role-cli-pointer/real: a real key reads as the pointer, with the `--help` clause and the script = first token",
             SJ._carrier_expected(row_of_cmd(key)), (SJ.COMMANDS_TEXT.format(command=key, script=key.split()[0]), ""))
    check_in("T1rp/role-cli-pointer/subcommand: the script is the first token of the key", f"`{key.split()[0]} --help`", SJ._carrier_expected(row_of_cmd(key))[0])
    check_eq("T1rp/role-cli-pointer/absent: a key with no command is the defect text (no pointer to nothing)",
             SJ._carrier_expected(row_of_cmd("no such command")), ("", "no command `no such command`"))
    real_registry = role_cli.registry
    role_cli.registry = lambda: {"zz.py a": {"roles": ["qa-runner"]}}
    try:
        check_eq("T1rp/role-cli-pointer/empty-card: a command with neither `input` nor `verify` is the defect text",
                 SJ._carrier_expected(row_of_cmd("zz.py a")), ("", "command `zz.py a` has no card"))
    finally:
        role_cli.registry = real_registry
    out = io.StringIO()
    role_cli.refuse(key, "it is wrong", out)
    check_in("T1rp/refusal-keeps-card: the refusal still prints the card's `input`", f"what to write: {role_cli.entry(key)['input']}", out.getvalue())
    # the call marker (K2)
    env = copy.copy(ENV)
    env.load_map = {"common": [], "roles": {"qa-runner": [f"plugin:{SJ.KEY_PAGE.format(role='qa-runner')}"]}}
    row = a_row("t:one", requirement="Say it.", door="d")
    entry = row["producers"][0]
    entry["told"] = [{"page": True, "call": True}]

    def leg(families, sited, the_row=row, the_entry=entry):
        env.call_families, env.sited = families, sited
        return SJ._told_leg(the_entry, env, the_row)
    check_eq("T1rp/call-leg/listed-ok: the family listed, the row stating a requirement and sited: the marker is green", leg(["t"], {"t:one"}), [])
    check_eq("T1rp/call-leg/family-not-listed-dormant: the family not listed: the marker sleeps, K2 is green and the row is page-told",
             (leg([], {"t:one"}), SJ.call_told(row, "qa-runner", [], {"t:one"})), ([], False))
    check_in("T1rp/call-leg/no-requirement-red: a marker on a row that states no requirement is refused, naming the row",
             "t:one states no requirement", " ".join(SJ._call_leg(entry, {**row, "requirement": ""}, (setattr(env, "call_families", ["t"]), env)[1])))
    check_in("T1rp/call-leg/unsited-red: a marker on a row with no site in code is refused, the page item stands",
             "t:one has no site in code", " ".join(leg(["t"], set())))
    check_in("T1rp/call-leg/call-1-red: `call: 1` is no marker", "a told entry is not an object",
             " ".join(leg(["t"], {"t:one"}, row, {**entry, "told": [{"page": True, "call": 1}]})))
    check_eq("T1rp/call-leg/legacy-still-0: a call marker is no legacy leg, and the real file counts none", SJ._legacy_legs(REAL["joints"]), 0)
    split = {**row, "producers": [entry, {**entry, "roles": ["qa-scout"], "told": [{"page": True}]}]}
    check_eq("T1rp/call-told/decision: listed + sited + stating + every entry naming the role marked is True; an unmarked entry, an unsited row, "
             "an unnamed role, a code-less doubt are False",
             [SJ.call_told(row, "qa-runner", ["t"], {"t:one"}), SJ.call_told(split, "qa-scout", ["t"], {"t:one"}),
              SJ.call_told(split, "qa-runner", ["t"], {"t:one"}), SJ.call_told(row, "qa-runner", ["t"], set()),
              SJ.call_told(row, "qa-scout", ["t"], {"t:one"}), SJ.call_told(row, "qa-runner", "t", {"t:one"})],
             [True, False, True, False, False, False])
    # the family list: shape, reversibility
    check_eq("T1rp/call-families/real: the real file lists the six families and the real audit is clean with them",
             (SJ.call_families(REAL), audit().problems),
             (["guard_pre_tool", "stage_guard", "host_adapter", "execution_request", "run_suite", "role_cli"], []))
    check_eq("T1rp/call-families/empty-green: an EMPTY list is green (no row is told at the call; every row is page-told)",
             audit(data=mutated(lambda d: d.update(call_told_families=[], call_index_wording={}))).problems, [])
    for label, change, said in (("unknown family", lambda d: d["call_told_families"].append("zz_nope"), "names `zz_nope`, which is the family of no row"),
                                ("not a list", lambda d: d.update(call_told_families="role_cli"), "is not a list of distinct family names"),
                                ("a repeat", lambda d: d["call_told_families"].append("role_cli"), "is not a list of distinct family names"),
                                ("absent", lambda d: d.pop("call_told_families"), "lacks `call_told_families`")):
        check_in(f"T1rp/call-families/{label.replace(' ', '-')}-red", said, text_of(audit(data=mutated(change))))
    # the wording of each family's index line is data too: one per listed family
    check_eq("T1rp/call-wording/real: one wording per listed family, the real audit is clean with them",
             sorted(SJ.call_wording(REAL)), sorted(SJ.call_families(REAL)))
    check_eq("T1rp/call-wording/unusable-sleeps: a listed family with no usable wording is not told at the call (its rows stay on the page)",
             SJ.call_families({**REAL, "call_index_wording": {k: v for k, v in REAL["call_index_wording"].items() if k != "role_cli"}}),
             [f for f in SJ.call_families(REAL) if f != "role_cli"])
    for label, change, said in (("missing", lambda d: d["call_index_wording"].pop("role_cli"), "has no wording for the listed family `role_cli`"),
                                ("unlisted", lambda d: d["call_index_wording"].update(zz_nope="x"), "has a wording for `zz_nope`, which `call_told_families` does not list"),
                                ("empty", lambda d: d["call_index_wording"].update(role_cli="  "), "wording of `role_cli` is not a non-empty text"),
                                ("not-text", lambda d: d["call_index_wording"].update(role_cli=7), "wording of `role_cli` is not a non-empty text"),
                                ("not-object", lambda d: d.update(call_index_wording=["role_cli"]), "is not an object of one wording per listed family"),
                                ("absent", lambda d: d.pop("call_index_wording"), "lacks `call_index_wording`")):
        check_in(f"T1rp/call-wording/{label}-red", said, text_of(audit(data=mutated(change))))
    # K5 (P-8)
    page_row = lambda path, roles=("qa-runner",): {"check": "t:x", "producers": [{"roles": list(roles), "field": "f", "demands": [],
                                                                                  "told": [{"path": path, "anchor": "## Outputs"}]}]}
    check_eq("K5/key-page-leg-counts: a sentence-less row whose leg is the role's own key page (placeholder expanded) counts for it",
             row_counts(page_row("references/slices/<role>/handoff-keys.md"), "qa-runner", {"qa-runner"}), True)
    check_eq("K5/other-role-page-not-counted: another role's page, a leg with no path and a bare sentence-less row do not count",
             [row_counts(page_row("references/slices/qa-scout/handoff-keys.md"), "qa-runner", {"qa-runner"}),
              row_counts({**page_row("x"), "producers": [{"roles": ["qa-runner"], "told": [{"page": True}]}]}, "qa-runner", {"qa-runner"}),
              row_counts(page_row("references/slices/<role>/handoff-keys.md", ("qa-scout",)), "qa-runner", {"qa-runner"})], [False, False, False])
    check_eq("K5/call-told-counts: a row that states a requirement and carries the call marker counts for the roles it names",
             row_counts(row, "qa-runner", {"qa-runner"}), True)


def main() -> None:
    told_leg_and_rows()
    t1rp()
    finish("test_stage_joints_told_legs")


# split: runner piece 1
if __name__ == "__main__":
    main()
