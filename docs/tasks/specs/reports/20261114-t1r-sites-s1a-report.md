# T1r-sites S-1a report (t-743) - `execution_request.py` sites and `RequestError.records`

Worktree `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r`, branch `wip/tbw-t1r`, on top of 1db4ec9. Builder, Sonnet. No refusal text changed
by one byte (proof: section "Old text").

## What was done

- `execution_request.py`: `from detector_verdict import refusal`; `RequestError.records: tuple = ()` (class attribute); `validate_request`
  wraps every sited append as `errors.append(refusal("<id>", <same expression>))` and raises `exc = RequestError("; ".join(errors))` with
  `exc.records = tuple(e for e in errors if getattr(e, "check", ""))` (no sited problem: `()`); every sited `raise MineRefusal(...)` /
  `WindowFirst(...)` / `RequestError(...)` carries the Record as `args[0]`; `_sandbox_refusal` (one caller function) writes `execution_request:sandbox`.
- B3 (binding), applied literally: a site inside a helper with more than one caller has NO literal id; the id is on the caller.
  `JobStore.read` stays bare (`recover` -> `run_suite:recover`, `begin` both reads -> `run_suite:begin`, `last_run_of` bare); the same for
  `find_active_dispatch`, `_profile_for`, `_command_from_profile` (wrapped in `build_mine_request` with
  `except MineRefusal as exc: raise MineRefusal(refusal("<id>", str(exc))) from exc`) and `reference_target_problem` (text; wrapped at its
  callers `validate_request` and `_observe_stand`). `str(exc)` of the wrapped error equals the old one.
- Tests: ONE table `t1rs_sites` in `test_detector_verdict.py` (24 rows = 22 ER ids + `run_suite:begin` + `run_suite:recover`, plus controls); two rows
  (`selector_args`, `window_first`) written, NOT run, in `test_execution_request.py` (`t1rs_sites_after_the_probe`).
- Changelog `changelog.d/tbw-t1r-sites.md`.

## Site table (function | text fragment | id or E6 reason | test row | proof)

Proof key: F = proved fast (`t1rs_sites` row in `test_detector_verdict.py`, run); W = written in `test_execution_request.py`, NOT run, judged by the batch canon; N = not provoked anywhere.

| function | fragment | id | row | proof |
|---|---|---|---|---|
| validate_request | impact_regression is recommendation-only / purpose must be one of | purpose | purpose | F |
| validate_request | selected_instance_ids / current_scope_instance_ids must be a string array; outside approved current scope; must select at least one; unsupported selector for instances | selection | selection | F (at-least-one; the others by the `many` row) |
| validate_request | remaining_budget non-negative / greater than zero | budget | budget | F |
| validate_request | freshness must be explicitly fresh | freshness | freshness | F |
| validate_request | runtime_provenance is required / profile_id must match / not_applicable / person_runtime_off / must be valid matched / needs a read-only runtime_probe / runtime_probe.argv, .cwd, .timeout_s | runtime | runtime | F (the first text; the rest N, same id, same wrapper) |
| validate_request (and `_observe_stand`) | the story's record names the stand ... both as its own stand | stand.reference | stand.reference | F (validate path; the `_observe_stand` site N, same id) |
| validate_request | fingerprint_components requires ...; `verify_files` ValueError | fingerprint | fingerprint | F (first text) |
| validate_request | command must be an object ... command.selector_join | command | command | F (reporter text; 13 other appends same wrapper) |
| validate_request | execution.schema_version / reporter / data_seed_contract / selection | execution | execution | F (schema_version) |
| validate_request | behavioral command requires selector_args mapping; selector_args.<k> must be a non-empty array / placeholder / selector_join shape (x2) | selector | selector | F (mapping text) |
| validate_request | behavioral request requires instance_contracts; report_test_id; parameters; report_id_source; maps ambiguously | instance_contracts | instance_contracts | F (first text; the rest by `many`) |
| build_mine_request (caller of find_active_dispatch) | no active dispatch ...; several dispatches are open | active_dispatch | active_dispatch | F |
| _entries_of_case | is held under more than one area; names no area ...; holds N only under | case_entries | case_entries | F (first text; direct call) |
| build_mine_request (caller of _profile_for) | --profile names ... / different profiles / share the test root / no execution profile / cannot tell which | profile | profile | F (unknown profile) |
| build_mine_request (callers of _command_from_profile) + selectors.join | has no commands.one_test.argv; selectors.join ... | profile_command | profile_command | F (no argv) |
| _place_rows | the manifest names F, and no such file is under | place_rows | place_rows | F (direct call) |
| _observe_precedent, _observe_stand | runtime probe returned unknown ... (`_stand_refusal`) x3 | stand | stand | F (`_observe_stand` ProvenanceRefused) |
| _observe_stand | this is the story's first typed run on profile ... | stand.probe | stand.probe | F |
| build_mine_request | --mine needs at least one case id; --purpose is one of; --node-id names ONE case; --cwd and --sandbox-root; a red probe runs inside the sandbox | mine_call | mine_call | F (no case id; the other four N, same id) |
| build_mine_request | X is outside its scope | scope | scope | F |
| build_mine_request | the manifest names no test for X yet (x2); the manifest names F for C but no test in it | no_test | no_test | F (first loop; the other two N) |
| build_mine_request | does not run pytest, and the factory builds a selector | selector_args | `t1rs_sites_after_the_probe` | W, not run |
| `_sandbox_refusal` (callers: sandbox_run_directory x5) + build_mine_request clone-file raise | the sandbox root ... is not a directory; run directory outside / escapes / resolves / is missing; the test file F is not in the sandbox clone | sandbox | sandbox | F (not a directory; the others N, same helper) |
| build_mine_request | N test(s) of this dispatch's scope live in the same file (`WindowFirst`) | window_first | `t1rs_sites_after_the_probe` | W, not run |
| JobStore.begin | idempotency_key was already used...; claim exists but cannot be read; concurrently used; corrupt-file text of both reads | run_suite:begin | begin | F (corrupt-file text) |
| JobStore.recover | unknown execution job; corrupt-file text | run_suite:recover | recover | F (corrupt-file text) |

Not proved locally, judged by the batch canon: `selector_args`, `window_first` (rows written, not run); and the sibling texts of one id named above as "N, same
wrapper" (no row of their own: one table row per id, DoD (b)).

## Left bare (E6), classed per spec 6b item 8

- (code) `"<key> is required"` list (118), `validate_baseline_request` / `validate_managed_gate` extensions (121, 123): a caller's request-file shape no row owns today.
- (code) `probe_record` (`probe_failed_text`, `probe_not_json_text`): the probe's own failure, said by `profile_contract`.
- (code) `validate_record` failure re-raise (`RequestError(str(exc))` after `errors` is empty): the record schema, no row.
- (code) `raise ProvenanceRefused(value)` (the one reader of a probe answer) and the `raise` of it in `_observe_stand` when `evidence_only`: carries `.record`.
- (code) `s6_close_from_state` every refusal (state unreadable, a dispatch open, S6 not started / closed, the controller conflict, pipeline unreadable, closed story,
  not in the approved scope) and `build_mine_request`'s s6_close / fresh-evidence context refusals (`takes no dispatch id`, `builds only a red probe`, `names its task id`
  x2, `names no story folder` x2): the caller is `probe_by_code` / `story_run` building their own context, no role types these flags.
- (code) `JobStore.read` corrupt-file raise (B3), `JobStore.last_run_of` (E6 per B3), `find_active_dispatch`, `_profile_for`, `_command_from_profile` raises inside the helpers (B3: named at the caller).
- (code) `raise MineRefusal(f"the inputs of this run could not be fingerprinted: ...")` (fingerprint build failure).
- (role, queue to T1r-cards) none found: no E6 site states a requirement a role can meet that is not already a row.

## P-7 grep witness (`execution_request.py`)

- Every `raise RequestError|MineRefusal|WindowFirst|_sandbox_refusal` and `errors.append(` after the change: the two Grep outputs are in the transcript; sited sites hold
  `refusal("<id>"`; the unsited ones are exactly the E6 list above (lines 112, 116, 382, 426 `RequestError`; 945, 957 find_active_dispatch; 987-1044 s6_close;
  1754-1832 `_profile_for`; 1861, 1872 `_command_from_profile`; 2501 `ProvenanceRefused`; 3273-3297, 3771 `build_mine_request`; `118-123` the extend/required list).
- Literal ids: every `"execution_request:..."` / `"run_suite:..."` string literal in `scripts/*.py` after the change is one of the 31 row ids (24 ER ids and
  `run_suite:begin`, `run_suite:recover`; the other five `run_suite` ids are S-1b). No unknown id.
- `stage_joints.py --check`, summary line BEFORE (HEAD file, byte-copied back in for the run, restored, hashes equal):
  `... told counters: hand_cards 12, legacy_legs 0, unsited 150` / `stage joints: clean`.
  AFTER: `... told counters: hand_cards 12, legacy_legs 0, unsited 124` / `stage joints: clean`. 150 - 26 sited ids = 124 (S-1b sites the other 5: 119).

## Old text (byte-identity)

The same provocations ran over the pre-change file (`git show HEAD:...execution_request.py`, scratch driver in the scratchpad, not committed); the messages it printed
are the literals of `T1RS_OLD` in the test; the new file gives the same `str(exc)` on every row (test green).

## Verbatim witness

```
$ ( cd .../tbw-t1r/ai-packages/qa-factory && python -B scripts/tests/test_detector_verdict.py )
=== test_detector_verdict: 373/373 ok ===             (127 `PASS t1rs ...` lines of it)
$ python -B scripts/stage_joints.py --check
stage joints: walked exit 8, detector 5, window 27 | rows 267, gaps 4 (producer 2, told 1, demands 1), joints held 4 of 267 | role leg not walked (code-to-code rows): 26 | stages with no detector: S0, S1, S6, S7, S9 | told counters: hand_cards 12, legacy_legs 0, unsited 124
stage joints: clean
$ python -B scripts/selftest.py --limits --lang
PASS limits: SKILL.md / agents / references within size caps
PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier
=== qa-factory selftest: 4/4 ok ===
$ python -B scripts/tests/scenario_walk.py --witness-for scripts/execution_request.py       (27 files)
 fast, each alone: test_config_projection 223/223 ok; test_probe_fix_round 38 passed; test_probe_walk 32 passed;
 test_probe_word_repeat 15 passed; test_reference_window 85/85 ok
 judged by the batch canon (all in slow_tests.json, 11.5-24.9 s > slow_over_s 10): test_execution_request (also holds the two written rows),
 test_controller_state, test_gate_b_orders, test_gate_preflight, test_gate_registry, test_manual_capture, test_node_ids, test_probe_by_code,
 test_probe_by_code_alternative, test_probe_debt, test_profile_reader, test_proof_level, test_read_json, test_red_sandbox_probe,
 test_red_sandbox_reports, test_runtime_probe_onboarding, test_s5_parallel_admission, test_s5_precheck, test_scenario_cart_1,
 test_scenario_local_1_0108, test_scenario_local_1_arm_b, test_story_run_s6
```

Negative control (d): `errors.append(refusal("execution_request:freshness", ...))` turned into the bare append (byte copy of the good file taken first,
`scratchpad/er_new_backup.py`); `test_detector_verdict.py` then printed `FAIL t1rs execution_request:freshness: the Record of the row rides on the exception -
expected True, got False` (and crashed on the unreadable-row row), `stage_joints.py --check` showed `unsited 125`; restored with `cp` from the copy, hashes equal:
`07d1e50b35deae7e9b38a5b2b2ebb2f21ca1d48123fe037e869fe2589c8fca58` both, and the file is green again (373/373).

## FR walk

- A (refusals): FR-1/2/9 text and doors unchanged; the Record adds `expected` and `door`, never changes the problem; an unreadable row gives the factory-defect sentence (row `unreadable`, green). FR-4/57 n/a, no gate added.
- B (text to a person): not changed (no person text; the `missing_executor` question is `run_suite.py`, S-1b).
- C (contracts): FR-14 output shape of `str(exc)` unchanged; FR-17 one constructor `refusal()`; FR-38/49 n/a here (the page carriage is S-2).
- D (identity): FR-16 the id is a literal at the site (the scanner reads it); no id invented, none outside the 31 rows.
- E (delivery): n/a. F (measurement): n/a.
- G: FR-30 package is English/ASCII (selftest --lang green); FR-31 no timing test; FR-32 the fix goes to the one constructor.
- AR: AR-9 (sites carry the row), AR-13 (one reader `told_text` via `refusal`), AR-18, AR-22 (`records` has a reader in S-1b), AR-29 (no judgment moved).

## Questions for the Lead (design forks, left as written)

1. B3 read literally for ALL multi-caller helpers (not only `JobStore.read`): `find_active_dispatch`, `_profile_for`, `_command_from_profile` stay bare inside and are wrapped in
   `build_mine_request`. Consequence: the callers outside this node stay bare until S-1b/others wrap them: `probe_by_code.py:2686` (`_profile_for`),
   `probe_by_code.py` 4755 / 6964 / 7804 and `run_suite.py:3105` (`find_active_dispatch`), `run_suite.py:2877` (`reference_target_problem`). The critic's class walk (key B3, last paragraph) judged
   those helpers "not affected" because every caller asks the same requirement; if the Lead prefers the ids INSIDE those helpers, it is a three-line move per helper. I chose the literal reading of edge (1).
2. `s6_close_from_state`'s "not in the story's approved scope" site (the spec's second `scope` site) stays bare: the helper has two callers (`build_mine_request`, `s6_close_dispatch` -> `probe_by_code`) and the caller cannot tell that raise from the helper's other refusals. `scope` is still sited by the `build_mine_request` site. Residual E4 note: a role on the `probe_by_code --s6-close` road meets this one without the row.
3. The two written rows (`selector_args`, `window_first`) were not run and may need a fixture fix on first run of the canon (the fixture guesses which runner the factory builds no selector for).

## Analogs noticed (not widened)

- `onboarding_probe.py:278` calls `ER._command_from_profile` too (an onboarding road, bare by B3).
- `window_record.py:267` and `probe_by_code.py:2892` print `unknown_profile_refusal` as plain text, never through `refusal()`.
- Other helpers returning text (`_stand_refusal`, `_probe_refusal`, `scope_refusal`, `_no_test_refusal`) are wrapped at their raise sites here; their other callers (if any) are not sited.

## Needed beyond the manifest

`stage_joints.py` `check_ids` / `refusal_registry.py` `_scan_wide` binder (to check that `from detector_verdict import refusal` is read), `contract.py` names used by the test
(`entries_for_case`, `manifest_test_keys`, `split_case_key`), `slow_tests.json`, `harness.py`, `test_execution_request.py` fixtures (`base_request`, `ep1_37...`, `pc9b...`), `run_suite.py` / `probe_by_code.py` / `onboarding_probe.py` caller greps.
