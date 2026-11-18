# FV3-30 (t-1513) build report

## Plan items
1. null_outcomes.py: `sibling_in` live, impl `handoff_check.py::_sibling_in_view`, params field/in as data - DONE (null_outcomes.py, handoff_check.py)
2. Grammar: `rounds` in `handoff.REQUIRED_LISTS` - DONE (handoff.py)
3. yaml block `null_outcome.rounds` (field `scope[].fix_result`, in `[fixed]`, words) - DONE (s7-automator-to-analyst.yaml). The words key is quoted, because unquoted `scope[].fix_result:` is mis-parsed by the contract parser.
4. Tests: S3 now two contracts + REQUIRED_LISTS pin (test_s7_null_outcome.py); R13 changed, R13b/c/d, a door row, R13e/f investigation rows (test_handoff.py) - DONE
5. Registered-conditions pin: the count stays 12 (the row existed). The live/impl audit row is `null_outcomes.audit`, unchanged code, green on the real tree.

## Choices (lead answers 1-3)
- Seam: `_sibling_in_view` returns ([], []) for a NON-EMPTY `rounds`, so the condition is "not consulted" in effect; `check` is not guarded. `_null_outcome_impl` is unchanged.
- `_view_for(entry, investigating)` replaces the two selection sites in `check` (not the --fix site: sibling_in opens no rows). `_investigation_view` is used only for `triage_has_no_repair`, so scope/not_for_repair verdicts and every other contract are unchanged.
- Code `handoff_check:required_rows` reused (no new refusal code, no registry file touched).
- Exact refusal text: "no rows. `rounds` is empty, and `fixed` in `scope[].fix_result` says a repair was made: N `scope` row(s) say it (<ids>), but no repair round is recorded."
  Door: "add the `rounds` row for each (changed, verify.witness), or set `fix_result` to what really happened"
- Edges: scope absent/empty -> legal; fix_result absent/null/`Fixed`/placeholder -> not fixed (exact match; R13c; report line: case variant treated as not fixed); a field not of form `<list>[].<leaf>` -> refused (fail closed).

## Witness
`python -B <scratch>/run_nodes.py test_handoff::an_untouched_list_is_empty_at_every_depth_that_crosses_no_row test_s7_null_outcome::every_other_contract_behaves_as_it_did` (these functions are not pytest-collectable; `python -m pytest ...::fn` says "not found", so a 6-line driver calls them through harness):
    PASS R13 rounds untouched beside fix_result fixed: refused (FV3-30, sibling_in)
    PASS R13b ... legal / R13c ... legal / R13d ... legal / R13e / R13f
    PASS S3: two contracts name a null outcome ...
    === nodes: 43/43 ok ===
`registry_preflight check lint read-json driver-layers census --paths <handoff, null_outcomes, handoff_check>`:
    lint ok, read-json ok, driver-layers ok
    census RED: window_record.py::judge_door is a check unit (u1) with no row in judgment-census.json
  (window_record.py is not in my diff; not caused by this change.)
not run locally: the rest of both files, canon judges.

## Needed from integration (RED consequences outside owns)
test_null_outcomes.py (not owned) fails on the real tree, measured: PINS["scope"] 32 -> 33 (rounds is now a walked carrier, home `declared`);
K0.4 sizes 32 -> 33; "homes" (1,33,52) -> (2,33,52); K0.8 summary text `walked scope 33 ... declared 2`; K0.3 "exactly one condition is live" ->
['sibling_in','triage_has_no_repair'] and the "reserved for node N1" text now needs another reserved condition (e.g. sibling_equals, N4/N6).
Card F-r2-5(a): no frozen fixture was re-judged by me; these are keep-test expectations, so I stopped there.
Not run: form_filler.py (tests helper) `_excused`/required-set now treat `rounds` as required-list; handoff_init.py:190 no longer initialises `rounds`. Noticed analogs; not measured.

## Config keys: none. Changelog fragment: Lead writes it. Tests added: ~18 lines vs ~44 code lines.

# Round 2

## 1. test_null_outcomes.py (owned now) - pins, before -> after
- PINS["scope"] 32 -> 33; K0.4 sizes tuple (32,...) -> (33,...): +1 = the `rounds` carrier
- homes `declared` 1 -> 2; summary line "walked scope 32 ... declared 1" -> "walked scope 33 ... declared 2"
- live conditions ["triage_has_no_repair"] -> ["sibling_in", "triage_has_no_repair"]
- the reserved-condition text "node N1" -> "node N4/N6", with `sibling_equals` as the reserved sample (also in E3 and the reserved-declared count rows, which used `sibling_in`)
- registry pin stays 12; never_empty 33 and pending 52 unchanged.

## 2. STOPPED: measured divergence, fix is outside owns
Script (scratch, never committed; full source below). It runs the real tree ("after") against a patched copy that emulates "before" (REQUIRED_LISTS without rounds, null_outcomes without rounds):
- `form_filler._excused(s7-automator-to-analyst, "rounds")`: True before, False after. No world-list token (`<instance>` only) occurs in any rounds row, so no filler verdict changes today. `emptiable()` is unchanged (rounds is nulled).
- `handoff_init.empty_optional_lists(template, s7-automator-to-analyst)`: NOT identical. Before: `rounds: []` + the sample row as comment lines. After: the sample row stays as live template data (`p not in nulled` at handoff_init.py:190 now skips rounds). The check reads an untouched row as empty, so the verdict is the same, but the skeleton a role gets is different (F1(b), B-11: "a reader never meets a template row as data").
Fix needs handoff_init.py:190, outside owns. Candidate (not applied): exclude from `nulled` only the sections whose entry is `triage_has_no_repair`'s / or drop `p not in nulled` for non-REQUIRED... that is a design choice, so I stop. Lead widens.

## 3. Driver source (run3.py form) - scratch run_nodes.py
```python
import sys
sys.path.insert(0, r"C:/QAFactory/forge-repo/.claude/worktrees/agent-ada34995f535ddf75/ai-packages/qa-factory/scripts/tests")
sys.path.insert(0, r"C:/QAFactory/forge-repo/.claude/worktrees/agent-ada34995f535ddf75/ai-packages/qa-factory/scripts")
import importlib
import harness
for spec in sys.argv[1:]:
    mod, fn = spec.split("::")
    getattr(importlib.import_module(mod), fn)()
    print("ran", spec)
harness.finish("nodes")
```

Measure script (scratch) measure.py:
```python
import sys
A = r"C:/QAFactory/forge-repo/.claude/worktrees/agent-ada34995f535ddf75/ai-packages/qa-factory/scripts"
sys.path.insert(0, A); sys.path.insert(0, A + "/tests")
import handoff, handoff_init, form_filler
C = "s7-automator-to-analyst"
text = handoff.template(C).text()
def world():
    return (handoff_init.empty_optional_lists(text, C), form_filler._excused(C, "rounds"), form_filler._excused(C, "unresolved"))
after = world()
real_req, real_no = handoff.REQUIRED_LISTS, handoff.null_outcomes
handoff.REQUIRED_LISTS = ("scope", "inputs_read")
handoff.null_outcomes = lambda c: {k: v for k, v in real_no(c).items() if k != "rounds"}
before = world()
print("empty_optional_lists output identical:", before[0] == after[0])
print("rounds excused before/after:", before[1], after[1], "| unresolved:", before[2], after[2])
import difflib
for l in difflib.unified_diff(before[0].split("\n"), after[0].split("\n"), "before", "after", lineterm="", n=0):
    print(l)
tokens = form_filler.rules()["world_list_tokens"]
print("world tokens:", list(tokens))
print("tokens in rounds rows:", [t for t in tokens if any(t in l for l in text.split("\n"))])
```

## Witness round 2
    python -B run_nodes.py test_handoff::an_untouched_list_is_empty_at_every_depth_that_crosses_no_row test_s7_null_outcome::every_other_contract_behaves_as_it_did
    === nodes: 43/43 ok ===
    python -B ai-packages/qa-factory/scripts/tests/test_null_outcomes.py
    === test_null_outcomes: 360/360 ok ===
    registry preflight: lint ok / read-json ok / driver-layers ok (census not judged)

# Round 3 (handoff_init skeleton restored)
handoff_init.py `empty_optional_lists`: `held` = REQUIRED_LISTS minus `rounds`, and `nulled` minus `rounds`, so the wanted set equals the old one for every contract.
Skeleton proof (script below; it loads origin/main's handoff_init.py as a module and emulates the old handoff state):
    contracts compared: 22 | differing: []
    s7-automator-to-analyst diff lines: 0
    rounds: [] present: True
Known shift (kept, as instructed): `form_filler._excused(.., "rounds")` True -> False; no world-list token occurs in rounds rows, so no verdict changes today.
Witness: driver `=== nodes: 43/43 ok ===`; `=== test_null_outcomes: 360/360 ok ===`.
Row not placed (test_handoff_init_author.py is not in owns): `test_uniform_rule_every_contract[s7-automator-to-analyst]` FAILS now (new red). It mirrors the old rule with `path in handoff.REQUIRED_LISTS or path in nulled` (line ~148) and so expects `rounds` untouched, while the skeleton (as on origin/main) writes `rounds: []`. Fix for the Lead to place: in that test (and the `optional` list of test_runner_contract_follows_the_rule, harmless) read the held set as `[p for p in handoff.REQUIRED_LISTS if p != "rounds"]` and `set(nulled) - {"rounds"}`. The row to add: assert that the s7-automator-to-analyst skeleton holds `rounds: []`.
Same file, 2 reds `test_s5_contracts_get_no_author_arg[s5-critic-to-automator|s5-critic-plan-to-automator]` fail identically on the main checkout (5c9bd80b): pre-existing, not mine.

skeleton_diff.py (scratch):
```python
import sys, importlib.util
A = r"C:/QAFactory/forge-repo/.claude/worktrees/agent-ada34995f535ddf75/ai-packages/qa-factory/scripts"
S = r"C:/Users/i_mas/AppData/Local/Temp/claude/b3e3188b390a00d9/501cb4e0-b55f-46d8-9262-11b1caefad61/scratchpad/old/handoff_init_old.py"
sys.path.insert(0, A)
import handoff, handoff_init
spec = importlib.util.spec_from_file_location("handoff_init_old", S); old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)
names = [p.stem for p in sorted(handoff.CONTRACTS.glob("*.yaml")) if p.stem not in ("index", "vocabulary")]
new_out = {c: handoff_init.empty_optional_lists(handoff.template(c).text(), c) for c in names}
real = (handoff.REQUIRED_LISTS, handoff.null_outcomes)
handoff.REQUIRED_LISTS = ("scope", "inputs_read")
handoff.null_outcomes = lambda c: {k: v for k, v in real[1](c).items() if k != "rounds"}
old_out = {c: old.empty_optional_lists(handoff.template(c).text(), c) for c in names}
diff = [c for c in names if old_out[c] != new_out[c]]
print("contracts compared:", len(names), "| differing:", diff)
print("s7-automator-to-analyst diff lines:", sum(1 for _ in __import__("difflib").unified_diff(old_out["s7-automator-to-analyst"].split("\n"), new_out["s7-automator-to-analyst"].split("\n"), lineterm="")))
print("rounds: [] present:", "\nrounds: []" in new_out["s7-automator-to-analyst"])
```
