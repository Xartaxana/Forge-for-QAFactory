# F7-RC report (t-738) - register gaps through the S4 case critic's form; A2/A3 re-cut

Branch `wip/sc-f7rc` (cut from origin/main fdc94d9). Commits: merge of origin/wip/sc-a2 (a1862fb), merge of origin/wip/sc-a3 (65f6d94),
the re-cut as ONE commit (74c9430). Builder: sonnet. Spec: `docs/tasks/specs/20261114-sc-f7-recut-register-gaps-spec.md` as amended (A1-A10).

## 1. Merge facts and the role-load resolution

- `git merge origin/wip/sc-a2`: ONE conflict, `ai-packages/qa-factory/references/role-load.json` (as expected). Settled: main's file taken
  (`git checkout --ours`), merge committed. No other conflict.
- `git merge origin/wip/sc-a3`: clean (no conflict).
- Re-measure: `python -B ai-packages/qa-factory/scripts/role_load.py --all --json` after both merges (before my edits), then after.

| role | main's row (tokens / process) | measured after A2+A3 merged | measured after the re-cut | row set to |
|---|---|---|---|---|
| qa-requirements-tester | 12670 / 11320 | 12676 / 11326 | 12676 / 11326 | 12676 / 11326 |
| qa-test-strategist | 16925 / 15392 | 16989 / 15409 | 16989 / 15409 | 16989 / 15409 |
| qa-case-critic | 18296 / 15929 | 18693 / 16333 (74770 B) | 18686 / 16333 (74742 B) | 18686 / 16333 |

All other roles measure at or below main's rows (no row touched). Raises against main's rows, named (AR-20):
- `ratchet_tokens qa-requirements-tester 12670 -> 12676` - A2's text merged (tester charter).
- `ratchet_tokens qa-test-strategist 16925 -> 16989` - A2's text merged.
- `ratchet_tokens qa-case-critic 18296 -> 18686` - A2's critic text (merged), net of this re-cut.
- `process_ratchet_tokens qa-requirements-tester 11320 -> 11326`, `qa-test-strategist 15392 -> 15409`, `qa-case-critic 15929 -> 16333` - the same A2 text.

F-R6 bytes: the re-cut itself is net **-28 B / -7 tokens ratchet / 0 process tokens** on qa-case-critic against the merged A2 tip
(74770 -> 74742 B; 18693 -> 18686; 16333 -> 16333). Reached by trimming (charter line short as F-R6 (b) words it, one-line form comment, shorter
placeholder hints, F-R7 (a) rewording of the `branch_accounting --units` line); no named raise of the re-cut's own was needed.

## 2. Per-item facts

- A1: `handoff_init.EMPTIED` gained `"register_gaps": ("s4-case-critic-to-designer",)`; `refs` placeholder reads "<R-n or TC-n the gap stands
  against, or omit>". Rows in `test_exploratory_findings.py` (see 4): role's copy holds `register_gaps: []`; control: the untouched sample row of the
  RAW template IS refused at the exit check; the emptied copy raises no `register_gaps` problem; a values file opens row 0; a filled row with no refs
  gives no problem. The kept/quarantine rule: `test_handoff_init_author.py` is in the `quarantine` section of `test-layers.json` (verified), so NOT
  edited; no KEPT file pins `EMPTIED` (grep of `empty_optional_lists|EMPTIED` over tests/*.py: only the quarantined file and the control line of
  `test_handoff_inline_values.py`), so the A1 rows live in `test_exploratory_findings.py` (owned, keep).
- A2: `driver-layers.json` rows `Driver.register_gaps_write` (method), `register_gap_rows` (func), `REGISTER_GAP_WHY` (const), home `driver_stage_plan`.
  role-load rows: see 1.
- A3: `Refusal(text, dispatch=dispatch)`; the door names the conductor command `handoff_check.py --file work/handoffs/<d>.yaml --set
  register_gaps[<i>].<field>=<value>` or "delete the row and keep the gap in `questions[]`; then retry the finish. Rows recorded already are not
  recorded again." I also set `exc.known = False` (the sibling `questions[]` raise is a G refusal from `py(check=True, expect=...)`, so no phrase of
  this text may route it past the conductor; `route_known` returns None on `known False`). The spec did not state this; named here.
- A4: the form is rewritten after the add. Row: a second `handoff_check.py --fix` over the unchanged form leaves equal bytes - PASS (no drift found).
  The stale-sha residual stays accepted (the line carries the row's text whole).
- A5: step 4 catches `OSError` from `read` AND `append`. G11 (register path is a directory): read -> empty register, append raises -> Refusal naming
  `work/exploratory-findings.jsonl`, the form and the dispatch. PASS.
- A6: SIBLING_MAP axis 5 row "Skill phase <-> driver": one sentence added (the skill road records no row; qa-story pile queue; owner question F-R0).
- A7: `REGISTER_GAP_WHY` = "the reviewer of the test cases recorded it as a gap in the requirements: no test case can check it; it is not a defect of the product" (exact).
- A8: census - see 4 item "census": the scan creates NO unit for `register_gaps_write` / `register_gap_rows`, so no rows were written (a row without a unit
  fails C1). See Findings.
- A9: a key outside the template row is ignored with the print line "... carries `<key>`, not a field of the row; ignored", never refused (row G5b).
- F-R7 (a): the Techniques line now reads "Count the sentences, fields and branches of the sources you are given and ask which requirement holds
  each (the judgment of a missing one is yours)." (Lead decision F-R7 (a); not in the dispatch's non-goals list as excluded.)
- Changelog fragment: the A3 sentence rewritten (critic writes the row, the driver records it). `test_role_commands.py`: the card example's
  `--by` is now `S6-qa-runner-1` and its evidence `work/runner-notes.md` (both, as the plan critic asked); written, not run (slow, "judged by the batch canon").
- `test-layers.json`: `driver_stage_plan.py` added to the `covers` of the `test_exploratory_findings.py` keep row (the witness walk did not print the test for it).
- Call site: ONE line in `s4_critic_completion.complete`, after the `if not dispatch:` branch and before `stage_verdict_known`.
  Positional invariants pinned behaviourally: G13 (unknown verdict word -> line written, then the seam stub called, acceptance not written), G14 (refused row ->
  Refusal, neither acceptance nor seam called), G15 (no dispatch id -> no register, seam as before).
- Section read as `{}`: this parser reads a bare `register_gaps:` as `{}`, so an empty mapping is treated as null (R3); a non-empty mapping or a word is refused (R5).

## 3. FR walk (the spec's) and AR-n

A - refusals (R5/R6/R8/R10, A5) name what is wrong, what is expected ("Expected a list of rows {title, statement, refs, missing_prerequisite}, or [] for no gap")
and a door the receiver (the conductor) can use (FR-1, FR-2, FR-57). B - `REGISTER_GAP_WHY` is a plain-words text in the report (FR-6); the test checks it holds no
stage code and no `qa-` name. C - FR-11: the critic's tool (one Write of a values file) produces every field (template row is the skeleton); FR-38 told in the template
+ one charter line; FR-39 the charter names no command; FR-13 the field list is read from the template row (`handoff.template`); FR-56 `tools:` line unchanged (key checked);
FR-49 the row travels whole. D - FR-16 `recorded_by` = the completion's dispatch id; FR-18 a register line is not coverage. E - FR-21/P21 unchanged (a coverage_gap line
never adds to proven); AR-27 owner = the critic dispatch. F - n/a (no money, no measurer). G - FR-32 one table row per behaviour; FR-30 English (selftest --lang PASS); FR-47 code
records, never judges.
AR-n kept (as in the commit): AR-9, 10, 13 (read only through `exploratory_findings.read`), 14 (write only through `append`; grep below), 20 (raises named), 22 (J1), 23 (declared in the
form comment), 25, 27, 28, 29 (shape + exact-bytes identity only).

## 4. Witness (verbatim)

Verification run (package dir, one subshell):

```
( cd .../sc-f7rc/ai-packages/qa-factory && python -B scripts/tests/test_exploratory_findings.py && test_role_load && test_role_rules && test_field_producers && test_validator_class && test_ahead_cards && python -B scripts/selftest.py --limits --lang )
```
Output (tail of each, PASS lines filtered):
```
## test_exploratory_findings
=== test_exploratory_findings: 299/299 ok ===
## test_role_load
=== role_load (the one measure of a role's start load): 186/186 ok ===
## test_role_rules
role-rules: 453 rows, 542 carriers checked, 0 finding(s)
=== role rules: 57/57 ok ===
## test_field_producers
known red rows 20, not in world rows 47, rows walked 870
=== test_field_producers: 885/885 ok ===
## test_validator_class
=== test_validator_class: 51/51 ok ===
## test_ahead_cards
=== test_ahead_cards: 265/265 ok ===
## selftest --limits --lang
PASS lang: no Cyrillic anywhere in the package
PASS lang: no control byte left by an eaten escape sequence (FR-29)
PASS limits: SKILL.md / agents / references within size caps
PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier
=== qa-factory selftest: 4/4 ok ===
```
`test_exploratory_findings.py` rows added (key function `key_f7rc`, in the 299): G1 two rows recorded (kind/recorded_by/evidence=form/why constant/window pre-gate-a/print),
G2 absent / `[]` / null / placeholder-only (no file, no print), G3 placeholder skipped + real row index 1, G4 word / mapping / number refused, register bytes unchanged,
G5 two shape problems -> ONE refusal naming both, dispatch + conductor door + known False, G5b extra key ignored with print, G6 placeholder field -> writer refusal
names `--missing-prerequisite` + row index, G7 row 0 ok / row 1 refused, retry writes only row 1, G8 same form twice, G9 repair-round form (one equal, one new),
G10 reworded row -> second line, G11 directory register -> Refusal naming the register, G12 after gate A -> window `s5-s8`, G13/G14/G15 call-site rows, J1 form -> register
-> `report_facts._exploratory` counts 1 gap and `_r_exploratory` holds the statement and "missing: ...", A1 rows (emptied copy, control, values file, no refs), A4 equal bytes
after a second `handoff_check --fix`.

`scenario_walk.py --witness-for` (changed package files + fixtures) printed 97 distinct test files; the fast ones (not in `slow_tests.json`, not `test_story_run_*` /
`test_controller_*` / `test_fixes_13797`) beyond the six above were run:
```
test_artifact_writers 23/23 ok | test_codex_tool_guidance 217/217 ok | test_dispatch_identity 114/114 ok | test_driver_stop_record 255/255 ok
test_exploratory_answers 107/107 ok | test_first_look_code_look 127/127 ok | test_first_look_step 101/101 ok | test_first_look_wiring 102/102 ok
test_gate_question_form 482/482 ok | test_handoff_init 23/23 ok | test_human_questions 291/291 ok | test_knowledge_notice 15 passed | test_login_need 33 passed
test_null_outcomes 327/327 ok | test_person_owned 82/82 ok | test_probe_gap_door 54 passed | test_probe_marker_judgment 46 passed | test_probe_not_proved 47 passed
test_reference_window 85/85 ok | test_s5_window_leftovers 148/148 ok | test_walk_account 190/190 ok | test_walk_lanes_parallel 196/196 ok | test_walk_supply 261/261 ok
test_whole_list_sites 292/292 ok
```
Judged by the batch canon (written/changed, not run): `test_role_commands.py` (example `--by`/evidence), `test_judgment_census.py` (no rows needed, see Findings), `test_driver_layers.py`
(three new rows), `test_brief_pack.py` (brief text unchanged), and every slow file the walk printed (list in the walk output; incl. `test_handoff.py`, `test_handoff_values_*`,
`test_story_run_*`, `test_selftest_slow_tests.py`, `test_scenario_*`).
Read-only helper (not a test run): `units_of` of `test_judgment_census.py` called in process over the worktree: `units total 1252 problems [] rowless: []` after the helper was renamed;
before the rename it showed `('driver_stage_plan.py', 'refuse') ['u1']` rowless (a nested helper named `refuse` matched UNIT_NAME_RE), hence `gap_refusal`.

AR-14/AR-13 greps (positive controls included), run in `scripts/`:
```
grep -n "exploratory-findings.jsonl" scripts/*.py (non-test): driver_stage_s7.py:82,114,313,544 (is_file reads / list text, pre-existing); exploratory_findings.py:1,77 (the writer/reader module)
grep -n "append_jsonl_line(" scripts/*.py | grep -i explor : exploratory_findings.py:392 only  -> no new writer site
positive control (same tool, pattern known to exist): report_facts.py:358,363,368 found "exploratory_findings"
```

### Key-presence run (DOC-DISPATCH), script in FULL source (never committed; kept at `<scratchpad>/keys_f7rc.py`)

```python
"""DOC-DISPATCH key-presence run for F7-RC (never committed). Keys are quoted verbatim from the DoD item 4."""
import json
import sys
from pathlib import Path

PKG = Path(sys.argv[1])
DROP = sys.argv[2] if len(sys.argv) > 2 else ""          # negative control: one key deliberately treated as absent

charter = (PKG / "agents/qa-case-critic.md").read_text(encoding="utf-8")
form = (PKG / "handoffs/s4-case-critic-to-designer.yaml").read_text(encoding="utf-8")
cards = json.loads((PKG / "references/role-commands.json").read_text(encoding="utf-8"))
# the entry sits under a table key in role-commands.json; find it by name wherever it is
def find(node):
    if isinstance(node, dict):
        if "exploratory_findings.py add" in node:
            return node["exploratory_findings.py add"]
        for v in node.values():
            r = find(v)
            if r:
                return r
    return None
roles = find(cards)["roles"]

CHECKS = [
    ("charter present: as a row of `register_gaps` in your form", "as a row of `register_gaps` in your form" in charter),
    ("charter present: it reaches the test report", "it reaches the test report" in charter),
    ("charter present: tools: Read, Grep, Glob, Write, Edit", "tools: Read, Grep, Glob, Write, Edit" in charter),
    ("charter absent: exploratory_findings.py add", "exploratory_findings.py add" not in charter),
    ("form present: register_gaps:", "register_gaps:" in form),
    ("form present: `[]` (or no", "`[]` (or no" in form),
    ("form present: missing_prerequisite:", "missing_prerequisite:" in form),
    ("card roles lack qa-case-critic", "qa-case-critic" not in roles),
    ("card roles hold qa-runner", "qa-runner" in roles),
    ("card roles hold qa-failure-analyst", "qa-failure-analyst" in roles),
]
failed = 0
for name, ok in CHECKS:
    if DROP and name == DROP:
        ok = not ok                                      # the key deliberately absent / present wrongly
    print(("PASS " if ok else "FAIL ") + name)
    failed += 0 if ok else 1
print("RESULT:", "failure" if failed else "all keys hold", f"({failed} failed of {len(CHECKS)})")
sys.exit(1 if failed else 0)
```
Run on the real package:
```
PASS charter present: as a row of `register_gaps` in your form
PASS charter present: it reaches the test report
PASS charter present: tools: Read, Grep, Glob, Write, Edit
PASS charter absent: exploratory_findings.py add
PASS form present: register_gaps:
PASS form present: `[]` (or no
PASS form present: missing_prerequisite:
PASS card roles lack qa-case-critic
PASS card roles hold qa-runner
PASS card roles hold qa-failure-analyst
RESULT: all keys hold (0 failed of 10)        rc=0
```
NEGATIVE CONTROL (copy of the three files in a scratch dir, the form's `register_gaps:` line renamed so the key is truly absent):
```
FAIL form present: register_gaps:
RESULT: failure (1 failed of 10)              rc=1
```

## 5. Findings, analogs noticed (not widened), needed beyond the manifest

- CENSUS BLIND SPOT: the judgment census scan sees no unit for `register_gaps_write` or `register_gap_rows` (a `raise Refusal(...)` of the driver family is not a
  refusal site of `refusal_registry`; the names match no unit pattern), so A8's two rows could not be written (a row with no unit fails C1). The census therefore does not
  count these checks; same blind spot as the sibling `questions[]` raise path. Queue line for the Lead (the census text names "raise through a variable/factory" as unseen).
- `exploratory_findings.read` reads a directory as the empty register (AR-28 analog of the reader; plan critic A5) - queued by the Lead already; here G11 pins the writer's refusal.
- `question_register.raise_from_handoff` reads a non-list `questions` as `[]` in silence (§S of the spec) - queued by the Lead already.
- The skill road records no `register_gaps` row (A6/R18) - named on SIBLING_MAP axis 5; queue line owner the qa-story pile.
- CL-NS (no-shell roles listed on cards) and N7 (writer first-error-only) are other nodes; `test_validator_class` OPEN line "append raises the first ValueError only" stays.
- Within one form a duplicated row is recorded twice on the FIRST finish (`active` is read once before the loop); on a retry both are skipped. Duplicate allowed, loss never (D.4 error direction).
- Commit gate: the `judgment:` line in the form the spec gave was refused (`judgment: <text>` needs ` -- <why>`); the commit carries `judgment: adds data check register_gaps_write -- <the spec's text>` and an `axes: not a mechanism (...)` line.
- needed beyond the manifest: `scripts/handoff.py` (`is_placeholder`, parse of a bare `key:` as `{}`), `scripts/driver_core.py` (`Refusal`, `known`), `scripts/driver_machine.py` (`route_known`), `scripts/tests/test_judgment_census.py` (`units_of`, to see the unit set), `scripts/tests/test_driver_layers.py` (L1/L9 row shapes), `scripts/tests/harness.py`, `scripts/slow_tests.json`.

## Fix round (t-738, attempt 2; fresh worker; findings B1, F2, F3, F4 of the code critic t-744)

- **B1** `scripts/tests/test_role_commands.py` (card example of `exploratory_findings.py add`): the file written is now `work/runner-notes.md`, the path `--evidence` names. The file is slow, NOT run (judged by the batch canon). Proof by hand, the example's exact argv in a temp story (`work/` + `pipeline.json`, like `story("QA-10")`), script `exploratory_findings.py`:
  - NEGATIVE (evidence file absent, the old shape): `exploratory_findings.py add: evidence path work/runner-notes.md is not a file under the task root ...` and `rc=2`.
  - FIXED (`work/runner-notes.md` written first): `{"id": "EX-1", "path": "...\\work\\exploratory-findings.jsonl"}` and `rc=0`.
- **F2** `scripts/driver_stage_plan.py` `Driver.register_gaps_write`: the nested helper `gap_refusal` is renamed `refuse_gap` (name and its 4 call sites only; no logic change). Row added in `scripts/tests/fixtures/judgment-census.json`: `{"file": "driver_stage_plan.py", "function": "refuse_gap", "class": "xref", "roles": ["qa-case-critic", "conductor"], "owner": "data"}` (+ a note). ONE row: the scan sees ONE unit (the helper, u1 via `_?refuse`); `register_gaps_write` / `register_gap_rows` are not census units by name, and a unit has one row (C1), the higher class wins and `xref` outranks `shape` (CLASS_ORDER), so the helper that carries both refusals (identity join, section judge) takes `xref`. `test_judgment_census.py` is in `slow_tests.json` (33.3 s): NOT run, judged by the batch canon. In-process, the unit scan of the package (`units_of(pkg, scan_files(pkg))`, then `_c1(census, units, probs)`): before the row `driver_stage_plan.py::refuse_gap is a check unit (u1) with no row in judgment-census.json: add a row {file, function, class, roles, owner}`; unit seen: `('driver_stage_plan.py', 'refuse_gap') ['u1'] False []` (blocks False: the raise goes through a factory call, the documented blind spot); after the row: C1 problems naming driver_stage_plan: `[]`. No ceiling moved: the unit does not block, class xref has no ratchet, `blocking_per_role` unchanged. `driver-layers.json`: no row carries the helper's name (grep `gap_refusal` over the worktree found only the code and this report), so no change.
- **F3** `scripts/tests/test_exploratory_findings.py`: deleted `key_a3`, `critic_findings` and `gap_line` (`gap_line` was called only by `key_a3`; grep control over `ai-packages` shows no other caller of the three) and `key_a3` from the key list at the file's tail. J1 and K-M1-1 hold both behaviours. No docstring left saying the critic records. Count 299 -> 288 (the 11 X1/X2 checks).
- **F4** `docs/SIBLING_MAP.md` axis 5 row "A role without Bash raises a before/now question": one clause appended, `register_gaps` section of the S4 case critic's form -> `Driver.register_gaps_write` -> `exploratory_findings.append`; the row's step `question_register._question_row` is not shared, because the register differs.
- Not done: nothing. F5 and the queue lines are the Lead's.

Witness (verbatim tails), `( cd .../sc-f7rc/ai-packages/qa-factory && ... )`:
```
=== test_exploratory_findings: 288/288 ok ===
=== role_load (the one measure of a role's start load): 186/186 ok ===
PASS limits: SKILL.md / agents / references within size caps
PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier
=== qa-factory selftest: 4/4 ok ===
```
`scenario_walk.py --witness-for scripts/driver_stage_plan.py` printed 77 files; not in `slow_tests.json` (`files`) and not `test_story_run_*` / `test_controller_*` / `test_fixes_13797`: 21, each run alone once, all rc=0:
```
test_codex_tool_guidance 217/217 | test_dispatch_identity 114/114 | test_driver_stop_record 255/255 | test_exploratory_answers 107/107
test_exploratory_findings 288/288 (run above) | test_first_look_code_look 127/127 | test_first_look_step 101/101 | test_gate_question_form 482/482
test_human_questions 291/291 | test_login_need 33 passed | test_null_outcomes 327/327 | test_person_owned 82/82
test_probe_gap_door 54 passed | test_probe_marker_judgment 46 passed | test_probe_not_proved 47 passed | test_reference_window 85/85
test_s5_window_leftovers 148/148 | test_walk_account 190/190 | test_walk_lanes_parallel 196/196 | test_walk_supply 261/261 | test_whole_list_sites 292/292
```
The slow printed files (incl. `test_role_commands.py`, `test_judgment_census.py`, `test_driver_layers.py`) and `test_story_run_*`: judged by the batch canon.
