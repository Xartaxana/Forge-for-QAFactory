# T7a-B report (t-1023): validate_artifacts sites, plan / manifest / phase-json

Branch `worktree-agent-a53f340df6d3b7c82`, code commit `bc3c28cf` (package commit; this report rides a second docs commit).
Status: done; one question (Q1) and one observation about the card's counter.

## What was done
61 refusal sites of nine functions now build `refusal("validate_artifacts:<id>", <same expr>)`: 59 by an AST-position wrap
(`errors.append(X)` -> `errors.append(refusal(id, X))`, the genexp of `errors.extend` and the listcomp of `errors +=` wrapped on
their element), plus 2 in `check_phase_json` through a nested `told(text)` that holds one literal per file (E1: no computed id).
No refusal text was touched; no other function of the file was touched.

## Site table (function | fragment | id or E6 reason (class) | test row | proof)
| function | sites | id / reason | test row (`tbw_t7a_b_sites`) | proof |
|---|---|---|---|---|
| check_plan | 17 (required fields, no TS rows, row form, R column, class, impact, priority, observation, basis, profile, parity, smoke counts, monoclass, seams, orphan R) | `validate_artifacts:check_plan` | "check_plan" | F (run on old and new: 11 + 8 messages identical) / W / N |
| check_plan_v0 | 15 | `validate_artifacts:check_plan_v0` | "check_plan_v0" | F (8 + 1 messages identical) / W / N |
| check_manifest_v0 | 8 | `validate_artifacts:check_manifest_v0` | "check_manifest_v0" | F (9 identical) / W / N |
| check_manifest_invariants | 3 | `validate_artifacts:check_manifest_invariants` | "check_manifest_invariants" | F (3 identical) / W / N |
| check_remedy_rows | 3 | `validate_artifacts:check_remedy_rows` | "check_remedy_rows" | F (5 identical) / W / N |
| check_self_fixes | 2 | `validate_artifacts:check_self_fixes` | "check_self_fixes" | F (2 identical) / W / N |
| check_marker_in_file | 1 | `validate_artifacts:check_marker_in_file` | "check_marker_in_file" | F (1 identical) / W / N (negative control below) |
| check_context_manifest_v0 | 10 | `validate_artifacts:check_context_manifest_v0` | "check_context_manifest_v0" | F (10 identical) / W / N |
| check_phase_json | 2 (broken JSON, required key missing) for `context-manifest.json` | `validate_artifacts:check_phase_json.context-manifest.json` | "check_phase_json.context-manifest.json" | F (3 + 1 identical) / W |
| check_phase_json | same 2 sites for `triage.json` | `validate_artifacts:check_phase_json.triage.json` | "check_phase_json.triage.json" | F (1 identical) / W |
| check_phase_json | same 2 sites for `automation-manifest.json`, `run-report.json` | E6 (code): code writer (`manifest_put`, `run_suite`), no row; stays a bare `str` | control row "no row for the file: stays a bare string" | F (2 + 1 identical) |
| check_phase_json | calls `check_nfr_report`, `check_run_report_*`, `check_remedy_rows` | not mine / sited by their owners | - | - |

Proof key: F = old-vs-new message lists compared (scratch script, see Witness 2), W = "the site writes this id" row (Record
`check == id`, `expected` == the row's told sentence), N = negative control (below).
Expected texts in the rows are the OLD source's literals (derived from the file before the edit; the lists `C.UNRESOLVED_REASONS`
come from `contract.py`, which is unchanged). Expected ids/rows: the ten `validate_artifacts:*` ids of stage-joints.json, all present.

Counter: `unsited 46 -> 36, rows sited: check_plan, check_plan_v0, check_manifest_v0, check_manifest_invariants, check_remedy_rows,
check_self_fixes, check_marker_in_file, check_context_manifest_v0, check_phase_json.context-manifest.json, check_phase_json.triage.json`.
The card text says "B -10" and the Lead decision says 46 at entry: matches (46 -> 36 measured, byte-copy before/after below).
I did not edit `told_ratchet.unsited` (stored value untouched) nor the K12 pin; the pin (46) is red until the integrator's commit.

## E6 list: the bare remainder of my functions
- (code) `check_phase_json` for `automation-manifest.json`, `run-report.json`: code writer, no row.
- (code) `_oracle_dated` (called by `check_plan_v0`, also by `check_case` and others): multi-caller helper outside my list, no own row; EC-2.
- (code) `check_cell_counts` is sited by T7a-A; `check_nfr_report` and `check_run_report_*` are outside my list.
- (role): none.

## Rows that over-claim (EC-8; not edited)
- `validate_artifacts:check_plan`: "the front matter counts (smoke rows **and the rest**) match the table" - the body checks only
  `smoke` against the smoke rows and `requirements_total` against the smoke count; `scenarios_total`, `by_defect_class`,
  `by_priority` are required-present but never counted against the table.
- `validate_artifacts:check_plan_v0`: "each names a **register** requirement" - the body checks only that the R column is non-empty
  (`row.get("requirements")`), not that the id is in the register.
- The other eight rows were read against their bodies; no over-claim found. (Under-claims, not reported: `check_plan` seams section,
  monoclass, orphan R roll call; `check_context_manifest_v0` v2 discovery lines.)

## FR walk
A: FR-1/2 refusal text unchanged (EC-1 proved on old vs new); the Record adds expected/door only through the transport; FR-59 an
unreadable row -> the existing factory-defect sentence in `refusal()` (untouched). B, E, F: not touched. C: FR-14 output shape
unchanged (one list of messages; Records print as their text; no JSON line here, no `told` key to place). D: FR-16 literal id at every
site (the phase-json id is two literals, not computed). G: FR-30 English only (ASCII fragment; `selftest --lang` green), FR-32 a test
row per id, FR-54 siblings: T7a-A/C use the same pattern; `_oracle_dated` listed above. AR kept: AR-9, AR-13 (ids only via `refusal`),
AR-18, AR-29 (no judgment moved). census: no new blocking unit.

## Edges
E-T7a-1: one `errors` list, one Record per append, REJECT text unchanged (old-vs-new equal on 15 provocations, 59+ messages).
EC-2: `check_remedy_rows` (2 callers: `check_phase_json`, `check_manifest_invariants`) carries its own id, because its row IS the
helper (same shape as T7a-A's `check_cell_counts`); no caller-specific requirement exists. EC-4: unknown row -> `refusal()`'s
existing sentence, untouched. Changelog fragment: `PKG/changelog.d/tbw-t7a-b.md`.

## Witness (verbatim)
1. `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/validate_artifacts.py ai-packages/qa-factory/scripts/tests/test_validators.py`
   names: test_scenario_cart_1 / dry_1 / local_1_0108 / local_1_arm_b (slow, in slow_tests.json), keep files test_audit_rules,
   test_bug_records, test_codex_host, test_gate_preflight, test_judgment_census, test_s5_precheck, test_s7_rejudge (slow, listed:
   **judged by the batch canon**); the fast ones, each run alone:
```
test_scenario_walk.py => exit 0 :: === test_scenario_walk: 95/95 ok ===
test_scenario_world.py => exit 0 :: === test_scenario_world: 33/33 ok ===
test_ahead_cards.py => exit 0 :: === test_ahead_cards: 253/253 ok ===
test_case_key_identity_join.py => exit 0 :: === case_key_identity_join: 154/154 ok ===
test_check_witness.py => exit 0 :: === check witness: 34/34 ok ===
test_field_producers.py => exit 0 :: === test_field_producers: 885/885 ok ===
test_open_list_fields.py => exit 0 :: 15 passed in 3.91s
test_oracle_provenance.py => exit 0 :: === oracle provenance: 296/296 ok ===
test_reference_snapshot.py => exit 0 :: === reference snapshot: 29/29 ok ===
test_stage_joints_12586.py => exit 0 :: === test_stage_joints_12586: 12/12 ok ===
test_stand_gap_remedy.py => exit 0 :: === test_stand_gap_remedy: 34/34 ok ===
test_triage_blocked.py => exit 0 :: === test_triage_blocked: 50/50 ok ===
test_validator_class.py => exit 0 :: === test_validator_class: 51/51 ok ===
test_validators.py => exit 0 :: === test_validators: 459/459 ok ===
test_whole_identifier.py => exit 0 :: === whole identifier and the revoked word: 166/166 ok ===
```
   (the new table adds 10 ids x 5 checks + 1 control = 51 checks to `test_validators`; 459 includes them.)
   Slow-list membership read from `scripts/slow_tests.json` (positive: the same read printed True for test_s5_precheck etc.).
2. Old-vs-new comparison (scratch script, not committed; `va_orig.py` = byte copy of the file at HEAD before the edit,
   sha256 `40FD3C0D...B32D`; both modules driven with the same 15 provocations):
```
plan msgs 11 identical | plan_empty 8 identical | plan_v0 8 identical | plan_v0_empty 1 identical | manifest_v0 9 identical
invariants 3 identical | remedy 5 identical | self_fixes 2 identical | marker 1 identical | ctx 10 identical
pj_cm 3 identical | pj_cm_broken 1 identical | pj_tr 1 identical | pj_am 2 identical | pj_rr_broken 1 identical
DIFFERENT: 0
```
3. `python -B ai-packages/qa-factory/scripts/stage_joints.py --check`, byte copy before / after:
```
BEFORE (old file): ... told counters: hand_cards 12, legacy_legs 0, unsited 46   | stage joints: clean
AFTER:             ... told counters: hand_cards 12, legacy_legs 0, unsited 36   | stage joints: clean
```
   (rows 267, gaps 4 (producer 2, told 1, demands 1), joints held 4 of 267 both times.) Restore check: new file sha256
   `2F051F9F...3B08`, equal to its copy after the old-file swap.
4. `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`:
```
PASS limits: SKILL.md / agents / references within size caps
PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier
=== qa-factory selftest: 4/4 ok ===   (exit 0)
```
5. Negative control (common DoD 4): the single site of `check_marker_in_file` turned bare on the file (`refusal("...", ` -> `(`), byte copy
   taken before:
```
FAIL t7a-b check_marker_in_file: every message carries the id — expected ['validate_artifacts:check_marker_in_file'], got ['']
stage joints: ... told counters: hand_cards 12, legacy_legs 0, unsited 37   (36 -> 37)
restored: 2F051F9FBC31D2A8F4C3386E13734F6CAC0F8A63B2CC61CFE2AC39BA170D3B08 vs copy 2F051F9FBC31D2A8F4C3386E13734F6CAC0F8A63B2CC61CFE2AC39BA170D3B08  (equal)
```
6. Commit gates on `bc3c28cf`: `gates: ok (7 checks)`, `gates: ok (4 checks)`; first attempt said "factory rules index is stale", I ran
   `python -B tools/factory_rules_index.py` and staged nothing from it (`docs/OWNER_PRINCIPLES_INDEX.md` stays modified, unstaged,
   in the worktree).

## Questions
Q1: `check_remedy_rows` has two callers (`check_phase_json` for `run-report.json` env_blocked, `check_manifest_invariants` for
unresolved[]) and now carries its id inside the helper. EC-2 literally says a multi-caller helper carries NO literal id. I read it
as inapplicable because the row id is the helper's own (same as the accepted T7a-A `check_cell_counts`); if the Lead reads EC-2
strictly, the id moves to a wrapper at the two callers. Decision belongs to the Lead.
Observation: no deviation from the spec; the card's "B -10" matches the measured 46 -> 36.

## Beyond the manifest
`scripts/contract.py` (parse_plan, manifest_unresolved, remedy_errors), `scripts/stage_joints.py` (the site scanner, `row_for`),
`scripts/slow_tests.json`, `scripts/tests/harness.py` (via test_validators), `scripts/tests/test_validators.py` T7a-A function.
