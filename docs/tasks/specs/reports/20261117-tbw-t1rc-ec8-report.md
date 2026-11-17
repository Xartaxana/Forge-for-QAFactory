# TBW1-18 (TBW-T1rc-ec8, t-1247) report

Spec: `docs/tasks/specs/20261117-told-before-work-t1r-cards-spec-r3.md` section 7. The EC-8 lines were found by Grep for "EC-8" under `docs/tasks/`: `docs/tasks/specs/reviews/t-979-told-before-work-wave-a.md` (K5, lines 87-93) and the wave-A reports `reports/20261117-tbw-t6-report.md:53`, `-t4a-report.md:127`, `-t7b-report.md:45`, `-t7a-b-report.md:44`, `-t7a-c-report.md:122`. The pre-append sentences: `reports/20261117-tbw-t1r-cards-a-report.md` E-4 (30 rows, not "about 25").

## Items: DONE / PARTIAL / NOT DONE

EC-8 lines (K5):
- `null_outcome.triage` NEW row (unreadable `work/triage.json`): DONE as a row; the site (`handoff_check.py:1431`, a bare Problem) is unmoved (siting is a non-goal). It is unsited, so `told_ratchet.unsited` measures 18 against 17 stored: see Question 1.
- T6 `null_outcome.failures` / `binding`: DONE. `failures` now says what its two sites check (no row / no name / a row for several failures / several rows) and points at `binding` for the non-empty path; door names `work/triage.json` and `instance_id`. `binding` kept as is (it is right for its own path).
- T6 `claims` (blank problem `_fill_claims`): DONE. Sentence now says an unmeasurable claim stays the role's own word. The site id is unmoved.
- T6 `values_apply` / `_text_of`: DONE (the nearer fix: the row now says a source that is not UTF-8 text is refused; door names "the path or the source"). The id of the site is unmoved.
- T6 rename -> `cli`: ALREADY LANDED by -a (row `handoff_check:cli.values_rename`, door "delete the values file", shell door for 9 roles). The site still prints `handoff_check:cli` (`handoff_check.py:3284`): TBW1-17 (rename site).
- T7b `planning_contract:plan`: DONE. "every obligation of the registry has its row" (claimed by no line of `gate_plan_errors`) replaced by "its rows are well formed (unique ids, owed fields, listed depth and impact)"; the revision clauses and -a's risk-policy clause stay.
- T7a-A `check_case_form`: DONE. Refusal text `validate_artifacts.py:384` lost "inherited from the plan row"; docstring (`:378-380`) said the same and now says it is not checked here.
- T4a PT-big-read split: DONE as rows. `guard_pre_tool:PT-big-read` is now text files only (door `Grep -n`, `offset`/`limit`); NEW `.pdf` (door: `pages` ranges, `offset`/`limit` do not bound it) and `.picture` (door: record `too_large` / name it in findings, do not try `offset`/`limit`). Sub-ids count as sited (`_is_sited`), so `unsited` does not move. The branches in `guard_pre_tool.py:896-902` still print bare `block(text)`: they switch to the sub-ids at the siting node; until then `test_guard_big_read_sections.py` IM-g stays as the wave-A report left it (not run: slow/not in the printed set).
- T4a PT-owner door: DONE. Door now names the road the refused party can use (`controller.py --operation rework`, and for a non-owner role "name it in your digest, the conductor sends it back"); the sentence says the orchestrator is refused too. Still audience-wise a row told to the 12 roles: whether the producer set should be the conductor is a siting question.

Sweep of the original sentences of the 30 rows (verdict per row; body read at the cited carrier):
- tightened (4): `planning_contract:plan` (above); `validate_artifacts:check_case` (body also refuses Automated without `red_probe`: added); `check_run_report_empty` (body refuses only `env_preflight == "pass"` with no blocked/manual rows, and counts passed+failed+skipped+passed_on_retry: sentence said "carries `env_preflight: blocked`" for every zero run); `check_report_ledger_and_readiness` (ledger table is checked only for a legacy report with a `ledger.md`; the `delivery_ready` line is owed only when `ledger.json` gives a word: sentence said both unconditionally; it is T7a-C's over-claim 1).
- fixed already in -a F3 (3): `check_run_report_v0`, `check_bug_filing_header`, `check_result_rows`. Replaced in -a (2): `check_case_form`, `planning_contract:contradictions`.
- kept (21): `check_context_manifest_v0`, `check_register`, `check_behaviour_claims`, `check_understanding`, `planning_contract:branches`, `coverage_contract:obligations`, `check_then_oracles`, `s5_precheck:bindings`, `s5_precheck:oracle` (-a's `case_expectation` clause agrees with `check_case_is_oracle`, `s5_precheck.py:1924-1965`), `manifest_put:expectation_changes`, `s5_precheck:environment`, `s5_precheck:manifest`, `check_run_report_head`, `check_run_report_coverage`, `check_triage_v0`, `check_report_blocks`, `check_report_sections`, `check_report_left_with_you`, `check_report_traceability`, `check_bug`, `check_bug_form`. For `s5_precheck:environment`, `bindings`, `manifest`, `expectation_changes` the body was read through the refusal ids (grep of `refusal(` sites), not clause by clause: estimate, not verified line by line.
- No original sentence contradicts an appended clause. Under-claims (body refuses more than the row says; not EC-8, not edited): `check_context_manifest_v0` (`implementation.source` must agree with `implementations[0].source`, `validate_artifacts.py:2412`), `s5_precheck:manifest` (green vs unresolved contradictions, a case in `tests[]` and `unresolved[]`, duplicate `self_fixes`), `check_triage_v0` (T7a-C), `check_then_oracles` (implementation-only basis), `check_bug_form`. -a's clause on `check_bug` lists the required fields without `violates` (`BUG_REQUIRED`, `:83`).

## Witness (one run after all edits; verbatim tails)

```
stage_joints.py --check:
stage joints: walked exit 8, detector 5, window 28 | rows 288, ... | told counters: hand_cards 12, legacy_legs 0, unsited 18
REJECT - 1 finding(s):
- stage-joints: told_ratchet.unsited is 17 but 18 rows have no site in code (... handoff_check:null_outcome.triage, first_look:put.null_reason, ...
contract_slices.py --write: slices: 44 declared, 0 rewritten (after the final write)
contract_slices.py --check:
SLICE: K10 qa-test-strategist: the plugin share is 55,203 bytes, over ... its baseline 55,103 (`native_headroom` in references/role-load.json)
SLICE: K10 qa-automator: the plugin share is 80,034 bytes, over ... its baseline 79,970
SLICE: K10 qa-code-critic: the plugin share is 75,332 bytes, over ... its baseline 75,268
role_rules.py --check: role-rules: 457 rows, 546 carriers checked, 0 finding(s)
```
Before my edits `contract_slices --check` had no finding and `stage_joints --check` had the one finding (11 vs 17, now stored 17 after TBW1-16: clean). So the two non-green lines are mine, both named.

`scenario_walk.py --witness-for references/stage-joints.json scripts/validate_artifacts.py`, non-slow files run by `python -B <file>` (slow ones skipped: test_contract_slices, test_stage_joints, test_detector_verdict, test_selftest_slow_tests, the 4 scenarios, test_audit_rules, test_bug_records, test_codex_host, test_field_producers, test_gate_preflight, test_judgment_census, test_s5_precheck, test_s7_rejudge):
```
test_ahead_cards.py exit 0: === test_ahead_cards: 253/253 ok ===
test_case_key_identity_join.py exit 0: 154/154 ok
test_check_witness.py exit 0: 34/34 ok
test_open_list_fields.py exit 0: 15 passed in 17.67s
test_oracle_provenance.py exit 0: 296/296 ok
test_reference_snapshot.py exit 0: 29/29 ok
test_stage_joints_12586.py exit 0: 12/12 ok
test_stand_gap_remedy.py exit 0: 34/34 ok
test_triage_blocked.py exit 0: 50/50 ok
test_validator_class.py exit 0: 51/51 ok
test_whole_identifier.py exit 0: 166/166 ok
test_validators.py exit 1: === test_validators: 578/579 ok ===
FAIL t7a-a check_case_form: the first message is the old text, byte for byte - expected "... basis - inherited from the plan row)", got "... basis)"
```

## Questions / needed from integration

1. `told_ratchet.unsited` (TBW1-17's) must read 18, or `null_outcome.triage` waits for its site: `raise: told_ratchet.unsited 17 -> 18 -- null_outcome.triage waits for TBW-T1rc-site` (precedent: -a's six). Alternative: site `handoff_check.py:1431` with `refusal("handoff_check:null_outcome.triage", ...)` at TBW1-17. I added the row (the dispatch lists it); the Lead may drop it instead.
2. `scripts/tests/test_validators.py:146-147` (not owned): the expected text must lose the tail. New: `f"TC-9.md: FORM {dash} 'task' is missing (a case with updated >= 2026-09-07: task, covers: [R-n], defect_class, basis)"),` and delete line 147. Why: the refusal text changed by spec.
3. `references/role-load.json` (not owned), re-measured by `scripts/role_load.py` on this tree: `native_headroom` strategist 55103 -> 55203, automator 79970 -> 80034, code-critic 75268 -> 75332 (U-H raises, E-9). `process_ratchet_tokens`: scout 15713 -> 15731, requirements-tester 13538 -> 13555, test-strategist 17954 -> 17979, case-designer 13944 -> 13966, case-critic 19112 -> 19129, automator 24107 -> 24125, code-critic 21782 -> 21800, runner 17247 -> 17262, failure-analyst 19507 -> 19650, bug-reporter 15734 -> 15751, doc-scribe 19462 -> 19489, retro-analyst 14642 -> 14660. `ratchet_tokens` above stored (raise): scout 17182 -> 17193, requirements-tester 14907 -> 14924, case-designer 15230 -> 15252, automator 25699 -> 25715, code-critic 23607 -> 23623, failure-analyst 21557 -> 21700, doc-scribe 20501 -> 20528. Why: the page lines of `claims`, `values_apply`, `plan`, `triage` changed; page growth is minimal (already shortened once), not zero.
4. Guard sites to switch at the siting node: `guard_pre_tool.py:896-902` (picture/PDF branch to `PT-big-read.picture` / `.pdf`), `handoff_check.py` ids for `_text_of` (stays values_apply, row fits now) and the rename (`cli` -> `cli.values_rename`).

## FR walk and hygiene

A (FR-1/2/4/57): the PT-owner and PT-big-read doors now name roads the refused party can use; no ban added. B: no text to a person. C (FR-14/38): row sentences carry only what their bodies check. D (FR-58): expected texts come from the bodies read, no new output measured. E, F: not touched. G: FR-30 ASCII English; FR-54: siblings below.
Siblings (not widened): `check_plan`, `check_plan_v0`, `check_legacy_report_sections` over-claims of T7a-B/C (reports `-t7a-b-report.md:44`, `-t7a-c-report.md:122`: not in K5, not in the E-4 set); PT-logs door (Read vs shell) named in the T4a report. Beyond the manifest: `handoff_check.py`, `guard_pre_tool.py`, `s5_precheck.py`, `coverage_contract.py`, `planning_contract.py`, `stage_joints.py`, `role_load.py`, `test_validators.py`. No loop or process left running.
Commit form: `architecture: AR-10, AR-16, AR-19`; `judgment: none`; `axes: not a mechanism (package data and text)`; the changelog fragment `ai-packages/qa-factory/changelog.d/told-before-work-1-tbw1-18-ec8-sweep.md`.

## Round 2 (Lead answers, t-1247)

- Q1: the triage row is kept and SITED: `handoff_check.py:1431` now builds `refusal("handoff_check:null_outcome.triage", ...)` (text unchanged); `told_ratchet.unsited` stays 17, `stage_joints --check`: clean.
- Q2: `test_validators.py:146-147` expected text lost the tail (579/579); `role-load.json` re-measured: `process_ratchet_tokens` set to the measure (slack 0), `ratchet_tokens` raised where the measure is above (requirements-tester 14907 -> 14908, case-designer 15230 -> 15235, failure-analyst 21557 -> 21683, doc-scribe 20501 -> 20509).
- K10: tightened until every role is within its baseline: no `native_headroom` raise. Cuts: `plan` clause "its rows are well formed;", `claims` ends "one code could not measure is yours.", `values_apply` door "correct the path or the source the refusal names" (the "did you mean" hint left the row; the refusal still carries it), the ledger clause shortened. Meaning kept.
- Witness (one run): stage_joints --check exit 0 "stage joints: clean"; contract_slices --check exit 0 "slices: 44 declared, all present and fresh; 20 key pages; 12 charters carry a generated digest line"; role_rules --check exit 0 "0 finding(s)"; test_validators.py exit 0 "=== test_validators: 579/579 ok ===".
