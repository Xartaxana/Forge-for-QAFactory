# t-985 wave A fix round (builder report)

Worktree `.claude/worktrees/wave-a-int`, branch `wave-a/integrate`, base e47e086c. One commit, not pushed.

## Done (A, code findings)
- F1 `refusal_registry._key_text(node, bind)`: one recogniser. The key now unwraps through `_record_kind` (the wide scan's reader): bare name, `from ... import refusal as R`, `DV.refusal`, `with_check(X, id)`, any id expression. The file's binding is read by one new helper `_detector_bind`, used by `_scan_wide` and by the narrow scan (same code both sides, AR-13). Row in `test_refusal_registry.py::part_scanner`: bare / alias / attribute / non-literal id / with_check.
- F2 `s5_precheck._Window.add` builds `_sited("plan", case, DV.refusal("s5_precheck:plan", message), fix, tag)`; `plan_result` untouched (bare). Row in `test_s5_precheck_sides.py::tbw_t5r_sites`: a C1 deviation of a window carries `told[0].check == s5_precheck:plan`, `told` last.
- F3 `planning_contract.gate_plan_errors` keeps a line that already has a check. Row `plan obligation` in `tbw_t7b_sites` (v2 row, empty `coverage_obligations`) expects `coverage_contract:obligations`, the old text, sentence and door.
- F6 `guard_pre_tool.big_read_check`: `text` built once; `block(text)` on the picture/PDF branch, `block(refusal(id, text))` otherwise. Consequence (not named in the review): the A24 key of both sites is now `text`, so the registry entry `PT-big-read` has `"call": "text"` (refusal_registry.py, in owns). Without it `refusal_registry.py --check` is red (3 violations, seen in the witness run).
- F8 `coverage_contract.validate_obligations`: local `def bad(text)` with the literal once; 36 appends use it. `coverage_contract:obligations.observation` (line ~455) is a different id and stays. `stage_joints.py --check` unsited unchanged (46).
- F9 `t4a_provoke` split: the wrapper saves `CLAUDE_PROJECT_DIR` and `hooklib._PROJECT_ROOT_CACHE`, makes the root, calls `t4a_provoke_in(G, HA, root)` in try, and in finally restores both and `cleanup(root)`. `t1rs_sites` restores only the env var, not the cache (analog, below).

## Report lines owed by wave A
- F4 (T7b, EC-2): the invariant reading is "a helper keeps the literal when every caller states ONE requirement". `gate_plan_errors` has three callers (gate_preflight:1918, variant_errors, _detector_body:4495) and all state the requirement of `planning_contract:plan`, so the literal sits there; `validate_plan` has seven callers with other requirements, so it has none. The earlier "7 callers, so no literal" was only half the reason.
- F5 (T6, EC-8, T1r-cards-R): the failure to rename the values file (OSError, `handoff_check` ~:3203-3208) is sited under `handoff_check:cli` (the id follows `wave0-rows.md:65`). The `cli` sentence ("names an existing UTF-8 form ... `--shorten` only with `--fix`") and door ("run `handoff_init` again") do not fit this problem; its own door is "delete <values>". Not "N". Goes to TBW-T1rc with the other EC-8 lines.
- F10 (T5r, E6): bare `raise ValueError(...)` / `_MergeRefused` sites of `manifest_put.py` that no row of T5r owns, with class:
  - `_retract_obligations:891`, `_retract_instances:943,953`, `_retract_unresolved:988,994` - class: shape/clash of a retraction request (the `retract` key's own payload; not the `retract` row), role-reachable through the CLI payload, bare.
  - `_merge:1938,1940` - class: shape of incoming obligation bindings (stable ids, duplicates), bare.
  - `_fold_step:1996,2000` - class: shape of the `manifest_seed` / `manifest_patch` payload (missing object), bare.
  - `read_fragment:2284,2292` - class: fragment unreadable / not an object, bare.
  - `_refuse_unmergeable:2227` - class: any exception of a malformed fragment re-raised as `_MergeRefused`, bare.
  Remainder for a row owner; no siting done here (out of scope).
- F7: the commit message carries `tests-over:` (reason: each review fix names its own test row).

## Part C
- Lint: the finding at `test_s5_precheck_sides.py:846` is NOT a pyflakes unused name. It is the second line of the ratchet, class `HandReaderInput`, family `RR-plan-row`: the literal `"Plan row: TS-1\n"` matches the `hand_inputs` pattern `Plan row:\s*TS-\d+` of `form-rounds.json`. Fix: `plan_row = "TS-1"` is used for the plan JSON and the line is `f"Plan row: {plan_row}\n"`. `lint_ratchet.py --check` now prints `0 new`.
- `told_ratchet.unsited`: `stage_joints.py --check` still prints 46 after C; `stage-joints.json` not touched.
- K5/real: NOT fixed, QUESTION for the Lead. Details below. I added no role to any row.

### K5/real (the 17 offender units; census roles from `judgment-census.json`, rows from `stage-joints.json`)
Measured with `told_unit_rows` / `row_counts` over the real file (script in the scratchpad, not committed). Every offender is a unit whose census roles are ALL 12 roles (or the 2 of `check_behaviour_claims`) because it is reached from a shared dispatcher, while its row names only the artifact's owner:

| unit | row names | census roles that no row names |
|---|---|---|
| handoff_check::_binding_problems | qa-failure-analyst | the other 11 roles |
| handoff_check::check_findings | qa-code-critic | the other 11 roles (incl. qa-failure-analyst) |
| validate_artifacts::check_behaviour_claims | qa-requirements-tester | qa-case-critic |
| ::check_bug, ::check_bug_filing_header, ::check_bug_form | qa-bug-reporter | the other 11 roles |
| ::check_case, ::check_case_form, ::check_then_oracles | qa-case-designer | the other 11 roles |
| ::check_cell_counts | qa-case-designer, qa-requirements-tester | the other 10 roles |
| ::check_delta_column, ::check_manifest_reuse, ::check_register, ::check_requirements_review, ::check_understanding | qa-requirements-tester | the other 11 roles |

Why I did not add (reading the callers):
- `validate_artifacts` units are reached from `collect_errors` (:2626), the write-time validator that runs on whatever file a role writes; the branch is chosen by the PATH (`/test-cases/`, `/bugs/`, `requirements-register.md`, ...). A role meets the check only by writing that artifact, which `guard_pre_tool.owner_check` allows to the owner only (PT-owner). So the rows name the roles that really meet them; the census lists every role because the dispatcher is shared. This is the "listed only because a helper is shared" case: a QUESTION, not an addition.
- `handoff_check::check_findings` is run for any form with a `findings` list (:1858, `return [], []` otherwise); which contracts carry `findings` I did not map (it would be 11 roles x contracts and the test_handoff cases show at least `s5-critic-to-automator` and `s7-analyst-to-automator`). `_binding_problems` is reached through `check_null_outcome` for a form whose section is not empty (:1343-1344), again per contract.
- Adding about 150 role-unit pairs to told rows would also surely move the K8/K10 told-page caps and `contract_slices`; I did not test it, because an addition that the callers do not support is the wrong direction anyway.

QUESTION to the Lead: (a) shrink the census `roles` of these 17 units to the roles that can meet them (a `judgment-census.json` edit, which is not in my owns and is a ratchet-adjacent file), or (b) relax K5 for units reached through a path-chosen dispatcher, or (c) tell me the roles to add and the cap policy. Until one is chosen `FAIL K5/real` stays (it was red before this round, same 17 units).

## Analogs noticed (not done)
- `t1rs_sites` restores `CLAUDE_PROJECT_DIR` but not `hooklib._PROJECT_ROOT_CACHE` (the F9 precedent is half a precedent); `tbw_t7b_sites` saves `CLAUDE_PROJECT_DIR` into `saved` (line ~1918) - not checked whether it restores. `tbw_t5r_sites` also never restores the env var (the `use_project` call has no restore).
- F1 sibling: `_record_kind` / `_key_text` are still two functions with one binding; the A24 scan of other files than SCANNED is unaffected (K6).
- F3 sibling: `variant_errors` and `gate_preflight` read `gate_plan_errors` lines; no code change needed, they get the inner ids now.

## FR pass (sections A-G of factory-rules.md)
- A (refusals): no refusal text, door or class changed; the F3 fix keeps the inner row id and its sentence (FR-1, FR-2 unchanged).
- B (text to a person): not changed; every sentence is the old one (the old texts are pinned by the digests and `old` tables).
- C (contracts): FR-14 output shape of a finding dict unchanged (`told` stays last, the F2 test pins it); FR-13 no vocabulary moved into code.
- D (identity): FR-16/17 - the key of a wrapped refusal is read by the one reader (`_record_kind`); the `PT-big-read` entry's `call` follows the source.
- E (delivery): not changed.
- F (measurement): not changed; `unsited` stays 46 (measured, `stage_joints.py --check`).
- G (code): FR-30 English only (checked: new lines ASCII except an existing em dash in guard_pre_tool text, unchanged); FR-31 no load-dependent test added; FR-54 siblings listed above.

Architecture: AR-13 kept by F1 (one recogniser `_record_kind` for the key and the wide scan, one binding helper); AR-18 kept: the refusal shape is `refusal(id, text)` at every touched site, no hand-built Record, F3 keeps the Record's own check.

## Witness
All commands from the worktree root `C:\QAFactory\forge-repo\.claude\worktrees\wave-a-int`.

1. DoD command `python -B ai-packages/qa-factory/scripts/scenario_walk.py ...--witness-for <5 files>` prints 120 lines: 3 scenarios (test_scenario_cart_1.py, test_scenario_local_1_0108.py, test_scenario_local_1_arm_b.py) and `keep` tests; 83 unique files. Last lines:
```
scripts/guard_pre_tool.py: keep test_stage_guard.py (layer table, covers it)
scripts/guard_pre_tool.py: keep test_test_locations.py (layer detector, covers it)
scripts/guard_pre_tool.py: keep test_words_carry.py (layer detector, covers it)
```
2. Every printed file, run once each (6 in parallel, 240 s cap, cwd = package dir). The files that `slow_tests.json` lists (test_story_run_*, test_controller_*, test_fixes_13797, test_scenario_*, test_s5_precheck.py, test_stage_guard.py, test_handoff.py, test_hooks_wiring.py, test_judgment_census.py, test_doctor_context.py and others, 40 of the 83) were NOT run: "judged by the canon of the batch". The run (before the `PT-big-read` entry fix) printed:
```
test_ahead_cards 253/253  test_artifact_supersede 71/71  test_codex_tool_guidance 217/217  test_detector_verdict 745/745
test_dispatch_identity 114/114  test_env_evidence 42/42  test_field_producers 885/885  test_fit_targets 116/116  test_flow_requests 93/93
test_gate_question_form 591/591  test_gate_role_accounts 44 passed  test_guard_big_read_sections 248/248  test_guard_command_text 197/197
test_guard_project_knowledge 10/10  test_guard_window_files 103/103  test_handed_to_person 58/58  test_manual_evidence 262/262
test_obligation_join 87/87  test_oracle_provenance 296/296  test_owner_role_one_list 15/15  test_probe_every_check 319 passed
test_quality_demand 84/84  test_regression_scope 93/93  test_s5_precheck_sides 201/201  test_s5_window_leftovers 148/148
test_sides_ledger 120/120  test_source_stage_integration 21/21  test_stage_joints_12586 12/12  test_stand_gap_remedy 34/34
test_then_remainder 354/354  test_validator_class 51/51  test_walk_plan_fields 123/123  test_whole_identifier 166/166
test_whole_list_sites 292/292  test_baseline_contract rc=0 (no summary line)  test_doctor_access rc=0 (no summary line)
test_refusal_registry => rc=1 530/533: FAIL the shipped package has no unregistered refusal ... guard_pre_tool.py:900 (big_read_check): the refusal `text` is not in refusal_registry.REGISTRY
test_s0_close_order => rc=1 28/29: FAIL the registry itself is clean ... guard_pre_tool.py:900 (big_read_check) ...
```
The two reds were caused by F6 (key `text`); fixed in `refusal_registry.py` (`PT-big-read` `call: "text"`) and re-run:
```
=== test_refusal_registry: 533/533 ok ===
=== S0 close order: 29/29 ok ===
=== test_guard_big_read_sections: 248/248 ok ===
=== test_detector_verdict: 745/745 ok ===
```
(the other files of the first run do not read the registry or the guard text; not re-run after the one-line registry change - they are listed above as run BEFORE it).
3. `python -B ai-packages/qa-factory/scripts/refusal_registry.py --check` -> `A24 refusal registry: no violations`
4. `python -B ai-packages/qa-factory/scripts/stage_joints.py --check` -> `... told counters: hand_cards 12, legacy_legs 0, unsited 46` / `stage joints: clean`
5. `( cd <worktree> && python tools/lint_ratchet.py --check )` -> `lint ratchet: 76 findings, 76 in the baseline, 0 new, 0 stale (pyflakes 3.2.0)`
6. ONE run of `scripts/tests/test_stage_joints.py` at the end: `=== test_stage_joints: 339/340 ok ===`; the only FAIL line: `FAIL K5/real: the rows of the real file that state a requirement name every role of their unit ... got [17 units: handoff_check.py::_binding_problems, ::check_findings, validate_artifacts.py::check_behaviour_claims, check_bug, check_bug_filing_header, check_bug_form, check_case, check_case_form, check_cell_counts, check_delta_column, check_manifest_reuse, check_register, check_requirements_review, check_then_oracles, check_understanding]` (same 17 as the integrator's list; K12 pin and rows-for are green).

## Needed beyond the manifest
- `tools/lint_ratchet.py`, `ai-packages/qa-factory/scripts/tests/fixtures/form-rounds.json` (to read the real lint finding), `judgment-census.json`, `validate_artifacts.py`, `handoff_check.py`, `manifest_put.py` (reads for part C / F10), `slow_tests.json`, `docs/tasks/handoffs/t-981-wave-a-integration.md`.
