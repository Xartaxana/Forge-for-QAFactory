# T7a-C report (t-1024): validate_artifacts run-report, triage and final-report sites

Branch `worktree-agent-a5be63046dc8925f9`, commit `8d1a2e5e` (not pushed, no CI). Owned files touched: `PKG/scripts/validate_artifacts.py`,
`PKG/scripts/tests/test_validators.py`, `PKG/changelog.d/tbw-t7a-c.md`. Nothing else (the pre-commit run regenerated
`docs/OWNER_PRINCIPLES_INDEX.md` in the worktree; it is NOT staged and not part of the commit).

## What was done
All 59 `errors.append(X)` / `errors += [X for ...]` sites of the nineteen owned functions are now `refusal("validate_artifacts:<function>", X)`;
X is untouched (the wrap was made by AST positions, inserting only `refusal("<id>", ` before and `)` after the argument). No bare site is left
in an owned function. `collect_errors`, `main`, the plan/manifest functions and the T7a-A functions were not touched.

## Site table
Fragment = the message each site writes. Every function has a row in stage-joints.json (checked: `SJ.row_for` returns it). Proof: W = the
function's row of `tbw_t7a_c_sites` run against the NEW file (text equal to the OLD file's first message, `check == id`, Record `expected` equals
the row's sentence); the same table run against the byte copy of the OLD file keeps all 20 "old text" assertions green (F = the id assertions fail
there, as they must; N = the negative control below).

| function | sites | fragment | id | test row | proof |
|---|---|---|---|---|---|
| check_run_report_empty | 1 | an empty run with env_preflight=pass and without blocked/manual | validate_artifacts:check_run_report_empty | yes | W, F |
| check_run_report_head | 1 | run-report without head | ...:check_run_report_head | yes | W, F, N |
| check_run_report_v0 | 3 | no / invented execution_status; env_preflight blocked | ...:check_run_report_v0 | yes (no execution_status) | W, F |
| check_result_rows | 7 | results[i] not an object / names several cases / no name / no status / bad status / skipped without reason / totals disagree | ...:check_result_rows | yes (nameless row) | W, F |
| check_run_report_coverage | 1 | case "appears in no lane of this report" | ...:check_run_report_coverage | yes | W, F |
| check_triage_v0 | 11 | duplicate observation rows; verdict outside list; the six `errors += [...]` comprehension sites (contract readers); FLAKY reruns / mechanism / fix_result | ...:check_triage_v0 | two rows (verdict `append`; FLAKY, a second kind of site) | W, F |
| check_report_sections | 3 | section missing / out of order / verdict line not above the sections | ...:check_report_sections | yes | W, F |
| check_report_traceability | 2 | requirements / cases in no row of the appendix | ...:check_report_traceability | yes | W, F |
| check_report_left_with_you | 3 | item names no R-n and case / no "To check:" / no "Needed:"/"How:" | ...:check_report_left_with_you | yes | W, F |
| check_report_test_marks | 2 | Proven line / Left-with-you item without real-or-mock mark | ...:check_report_test_marks | yes (Proven line) | W, F |
| check_report_forbidden | 2 | factory identifier shape / bare decision marker | ...:check_report_forbidden | yes | W, F |
| check_report_human_text | 1 | Factory defects item not in plain words | ...:check_report_human_text | yes | W, F |
| check_report_gate_b | 2 | gate B words / S8,S9 decision not quoted verbatim | ...:check_report_gate_b | yes | W, F |
| check_report_blocks | 7 | marker problem / block missing / heading rules / gate B section rules | ...:check_report_blocks | yes (unterminated marker) | W, F |
| check_report_coverage | 2 | no coverage section / empty coverage section | ...:check_report_coverage | yes | W, F |
| check_ptr_readiness | 3 | no readiness section / requirements without a row / status outside list | ...:check_ptr_readiness | yes | W, F |
| check_test_report | 2 | STALE_REPORT_SUMMARY / REPORT_SUMMARY_UNREADABLE | ...:check_test_report | yes (unreadable controller.json; the row allows the callee ids, as it calls the other functions) | W, F |
| check_report_ledger_and_readiness | 4 | hand text over TEST_REPORT_MAX_BYTES / legacy ledger table / no delivery_ready line / line disagrees with ledger.json | ...:check_report_ledger_and_readiness | yes (size) | W, F |
| check_legacy_report_sections | 2 | legacy section missing / out of order | ...:check_legacy_report_sections | yes | W, F |

Count 19 functions / 59 sites / 20 test rows (19 + the second triage row).

E6 list (bare remainder of my functions): none -- no bare `errors.append` is left in any owned function. Notes lines (`notes.append`,
`ORACLE_NOTES.append`: the "manual-agent rows wait" note and the legacy-facts note) are not refusals and stay as they were.

EC-2 (multi-caller): the id is the function's own, never a helper-internal id. `check_legacy_report_sections` (callers `check_report_sections`,
`check_test_report`), `check_report_coverage` and `check_report_ledger_and_readiness` (two callers each) carry their own function id; every call
path to one of them reaches the same requirement of the same row, so one id names one requirement.
EC-4/FR-59: an unreadable row is `refusal()`'s existing sentence (unchanged code path).

## Counters (EC-3, I did not edit `told_ratchet.unsited` nor the K12 pin)
`stage_joints.py --check`: unsited 46 -> 27, rows sited: the 19 owned ids (check_run_report_empty, check_run_report_head, check_run_report_v0,
check_result_rows, check_run_report_coverage, check_triage_v0, check_report_sections, check_report_traceability, check_report_left_with_you,
check_report_test_marks, check_report_forbidden, check_report_human_text, check_report_gate_b, check_report_blocks, check_report_coverage,
check_ptr_readiness, check_test_report, check_report_ledger_and_readiness, check_legacy_report_sections). The card said "C -18"; measured -19
(the card's 18 was a count slip; 19 functions have 19 rows). "Before" was measured by swapping the byte copy of the old file in (46, equals the
Lead's number for after T7a-A). The ceiling never rises. K12 pin: `test_stage_joints.py` pins the exact measured count, so it is red in the canon
until the integrator commit (named, not a defect of this node). census: no new blocking unit.

## FR walk
- A (refusals): FR-1/FR-2 text unchanged (byte-identical; expected/door ride only through the transport); FR-59 an unreadable row stays `refusal()`'s sentence.
- B (text shown to a person): not touched (no text changed).
- C: FR-14 output shape additive (a `Record` is a `str`); FR-38 rows were already page-told (EC-7: no page touched).
- D: FR-16 the id is a literal at each site.
- E, F: not touched.
- G: FR-30 package text English (selftest `--lang` green); FR-32 a test row for each function and a negative control; FR-54 siblings below.

AR touched: AR-9, AR-13, AR-18, AR-29 (judgment: none, no check added or moved). `tests-over: nineteen functions need one provoking fixture row each`
(+122 test lines vs +105 product lines; WARN by the commit hook, reason in the commit message).

## Verbatim witness
Byte copy taken BEFORE the edit: `sha256 40fd3c0dd7661774...` (original validate_artifacts.py); new file `f28ef0df2d40a704...`.

`python -B ai-packages/qa-factory/scripts/tests/test_validators.py` (new code):
```
PASS t7a-c check_legacy_report_sections: the call refuses
PASS t7a-c check_legacy_report_sections: the first message is the old text, byte for byte
PASS t7a-c check_legacy_report_sections: the first message carries the id
PASS t7a-c check_legacy_report_sections: every message carries an id of the allowed set
PASS t7a-c check_legacy_report_sections: its row states a sentence the refusal can print
PASS t7a-c check_legacy_report_sections: the Record carries that sentence

=== test_validators: 528/528 ok ===
```
The same table against the byte copy of the OLD file (harness: loads the old module into the test): the text assertions all pass
(`20` lines "PASS ... the first message is the old text, byte for byte", `0` FAIL on them) -- the byte-identity proof (EC-1); the id assertions
fail there, as they must.

`stage_joints.py --check`:
```
after (new):    ... told counters: hand_cards 12, legacy_legs 0, unsited 27   /  stage joints: clean
before (old):   ... told counters: hand_cards 12, legacy_legs 0, unsited 46   /  stage joints: clean
```
Negative control (DoD 4, one site, `check_run_report_head`, turned bare on a byte copy of the new file):
```
stage joints: ... told counters: hand_cards 12, legacy_legs 0, unsited 28   / stage joints: clean
FAIL t7a-c check_run_report_head: the first message carries the id — expected 'validate_artifacts:check_run_report_head', got ''
FAIL t7a-c check_run_report_head: every message carries an id of the allowed set — expected [], got ['']
FAIL t7a-c check_run_report_head: the Record carries that sentence — expected 'The run report carries a non-empty `head`.', got ''
=== test_validators: 525/528 ok ===
restored: sha256 f28ef0df2d40a704 (byte copy) == f28ef0df2d40a704 (file)
```

`scenario_walk.py --witness-for ai-packages/qa-factory/scripts/validate_artifacts.py ai-packages/qa-factory/scripts/tests/test_validators.py`
printed 26 files. Run each alone (all exit 0):
```
test_ahead_cards 253/253 | test_case_key_identity_join 154/154 | test_check_witness 34/34 | test_field_producers 885/885
test_open_list_fields 15 passed | test_oracle_provenance 296/296 | test_reference_snapshot 29/29 | test_scenario_walk 95/95
test_scenario_world 33/33 | test_stage_joints_12586 12/12 | test_stand_gap_remedy 34/34 | test_triage_blocked 50/50
test_validator_class 51/51 | test_validators 528/528 | test_whole_identifier 166/166
```
Judged by the batch canon (in `slow_tests.json`): test_audit_rules, test_bug_records, test_codex_host, test_gate_preflight, test_judgment_census,
test_s5_precheck, test_s7_rejudge, test_scenario_cart_1, test_scenario_dry_1, test_scenario_local_1_0108, test_scenario_local_1_arm_b.
(`slow_tests.json` membership read by script; no printed file is quarantined.)

`python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`:
```
PASS limits: SKILL.md / agents / references within size caps
PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier
=== qa-factory selftest: 4/4 ok ===
```

## Rows that over-claim (EC-8; not edited, input for T1r-cards-R)
1. `check_report_ledger_and_readiness`: "section 1 is the table `ledger.py` generated" -- the body checks the ledger table ONLY for a legacy report
   with a `ledger.md`; for a current-form report that clause is never checked.
2. `check_legacy_report_sections`: "(legacy form) Every gate-B section stands, in order." -- the body checks the six `LEGACY_REPORT_SECTIONS`
   (Verdict, Run this yourself, Product problems, Check coverage, Readiness, Our tests and the factory), not gate-B sections as such.
Under-claim (not EC-8, for the same redraft): `check_triage_v0` names the observation duplicate, verdict and FLAKY rules but the body also refuses
what the contract readers return (no-defect, diagnostic, blocked, reorder, control, contradiction problems: six comprehension sites).
`check_test_report`'s sentence is only the delivery-summary freshness; the function otherwise only dispatches to the other checks (each its own id).

## Siblings seen (class: validator refusals in validate_artifacts.py not in my list)
Still bare in the file, outside this node: `check_escape_ledger`, `check_charter`, `check_charter_form`, `check_pipeline`, `check_estimation_ledger`,
`check_nfr_report`, `check_pipeline_v0`, `check_config` (and `check_phase_json` appends other than the two artifacts with rows). None of them has a
row in stage-joints.json (Grep of `validate_artifacts:` row ids: 41 ids, none of these names) -> E6 class (code) "no row"; wave0 T7a-8 says the
same. Axis 17 (Record shape): a `Record` is a `str` subclass; the two list-comprehension sites and the callers that filter errors by `str` ops are
unaffected (full `test_validators`, `test_triage_blocked`, `test_validator_class` green). Axis 34: `refusal()` is the only road used. Axis 39: not
touched here.

## Questions
none.

## Needed beyond the manifest
`PKG/scripts/slow_tests.json`, `PKG/scripts/tests/test-layers.json` (to sort the printed files), `PKG/scripts/tests/harness.py`,
`PKG/scripts/contract.py`, `PKG/scripts/grammar.py`, `PKG/scripts/report_facts.py` (fixtures for the rows), `tools/factory_rules_index.py`
(pre-commit stale index, regenerated, nothing staged).
