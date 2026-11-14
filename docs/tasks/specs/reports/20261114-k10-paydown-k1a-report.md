# K10 pay-down, card K1a: the refusal prints every refused check (builder report)

Worktree `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r`, branch `wip/tbw-t1r`, base 8d71532b. Spec: r2 §5 K1a.

## What was done
1. `role_cli.refuse(..., *, check=None, records=())`: after `how to prove it` and before `if you cannot` it prints `_extra_record_lines(records, first, own)`; `first` = `problem.check` for a Record else `""`.
2. New `role_cli._extra_record_lines(records, first, own)`: list/tuple only; `_is_record` items only; drops `first`, `own`, repeats; renders `"  " + stage_joints.told_line(row_for(check)[0] or {"check": check})`; cap `branch_accounting.limit("refusal_units_shown")` (20 today) with the tail line; no cap if the limit cannot be read; never raises. Both imports are inside the helper.
3. `run_guarded` ValueError branch passes `records=getattr(exc, "records", ())`.
4. Rows (labels in the K10p list below). 5. Carry table below. Changelog fragment written.

## Verbatim witness (from the worktree root, each alone)
```
python -B ai-packages/qa-factory/scripts/tests/test_detector_verdict.py       -> === test_detector_verdict: 464/464 ok ===   (exit 0)
python -B ai-packages/qa-factory/scripts/tests/test_import_test_receipt_refusal.py -> 7 passed in 6.12s   (exit 0)
python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang          -> PASS limits: ... PASS limits: every mandatory role rule ... === qa-factory selftest: 4/4 ok ===   (exit 0)
```
`scenario_walk.py --witness-for role_cli.py test_detector_verdict.py test_import_test_receipt_refusal.py` printed 16 files. FAST, run alone, all exit 0:
`test_exit_gate_scope.py` 106/106 ok; `test_exploratory_findings.py` 344/344 ok; `test_manifest_projection.py` 182/182 ok; `test_scenario_walk.py` 93/93 ok; `test_scenario_world.py` 33/33 ok (plus the two above).
SLOW (listed in `slow_tests.json`), NOT run, "judged by the batch canon": `test_console_encoding.py`, `test_controller_state.py`, `test_handoff.py`, `test_profile_reader.py`, `test_s5_plan_controller.py`, `test_scenario_cart_1.py`, `test_scenario_local_1_0108.py`, `test_scenario_local_1_arm_b.py`, `test_window_record.py`; and the two owned slow files `test_red_sandbox_probe.py`, `test_probe_by_code.py` (rows written, only `ast.parse` checked: "ok" for both).
No file was red on the base commit. The first draft of the `unreadable-row` row expected "no row for"; the real sentence is "the row states no requirement" (row_for returned None, `told_text` gets `{"check": id}`): the row expectation was corrected, the code is the spec's.

## U-CMD (identical, E8)
before: `qa-automator 81385 / qa-code-critic 74417 / qa-test-strategist 55976`
after:  `qa-automator 81385 / qa-code-critic 74417 / qa-test-strategist 55976`

## K10p row labels a later card (K1b) looks for in the canon
- `test_detector_verdict.py` (fast, green): `K10p/refuse-no-records/no-records`, `-records-empty/`, `-records-not-a-list/`, `-records-a-dict/`, `-records-none/` (byte-equal), `K10p/refuse-no-records` (plain str, check last), `K10p/refuse-records-printed`, `K10p/refuse-last-line-is-check`, `K10p/refuse-first-repeated`, `K10p/refuse-non-record-item`, `K10p/refuse-own-command-check`, `K10p/refuse-unreadable-row`, `K10p/refuse-at-limit`, `K10p/refuse-beyond-limit` (two labels), `K10p/refuse-limit-unreadable`, `K10p/refuse-no-literal-line`.
- `test_import_test_receipt_refusal.py` (fast, green): `K10p/import-prints-every-check/four-checks`, `.../two-checks` (pytest ids of `test_the_import_road_prints_every_refused_check`).
- `test_red_sandbox_probe.py` (slow): `K10p/rs-told-passes-through/probe/{one-entry,three-entries,repeated-check}`, `K10p/rs-told-passes-through/diagnostic/{one-entry,three-entries,repeated-check}`.
- `test_probe_by_code.py` (slow): `K10p/pbc-told/{plan,tool,refusal}/{one-record,two-records,repeated-check}`, `K10p/pbc-told/execution_request:profile/_profile_cwd`, `K10p/pbc-told/execution_request:active_dispatch/_dispatch_context`.

## Carry table (item 5; by reading code, classes P / L / A)
Sites. red_sandbox: P `red_sandbox.py:1709` (probe, after `prepare()` clone, refused-run notes at 1707-1708, answer carries `told` at 1714); P `red_sandbox.py:2195` (diagnostic, answer 2196-2198); A `red_sandbox.py:1431` (`_author_baseline`, `_fresh_instances` exception, the probe goes on); A `red_sandbox.py:2041` (`_diagnostic_red`, returns ""; the run goes on). probe_by_code: P printers `probe_by_code.py:8284` (plan), `:8367` (ToolRefusal), `:8372` (Refusal), all `told_fields(exc)`; L `probe_by_code.py:4695` (`record.update(told_fields(exc))` after the launch began), L `probe_by_code.py:6266` (`ran["request_refused_told"]`). Construction sites `refusal("execution_request:...")` in probe_by_code: `:2698` and `:2903` (profile), `:4780` (active_dispatch). `_carry_told` copies `summary["told"]` (dedup by check) for any summary with `error` and no `execution_status`; `told_fields` for an exception/Record.

Per id (carried at P only / at L too / not carried):
| id | red_sandbox | probe_by_code |
|---|---|---|
| `execution_request:profile` (ER 3387; pbc 2698, 2903) | P only (1709, 2195, via run_suite `told`) | P only (8284/8367/8372 via Refusal at 2698/2903); L too (4695/6266: a MineRefusal from `build_mine_request`) |
| `execution_request:active_dispatch` (ER 3307; run_suite 3118; pbc 4780) | P only | P only (4780); L too (4695/6266) |
| `execution_request:mine_call`, `:scope`, `:no_test`, `:profile_command`, `:case_entries`, `:sandbox`, `:window_first`, `:stand`, `:stand.probe`, `:stand.reference` (run_suite 2888/2912) | P only (printed by run_suite `--mine` JSON, parsed by `_run_mine`) | not carried at P (no Refusal construction); L only (4695/6266, if the MineRefusal comes after the launch began) |
| `execution_request:purpose`, `:selection`, `:budget`, `:freshness`, `:runtime`, `:fingerprint`, `:command`, `:execution`, `:selector`, `:instance_contracts` (ER 130-372; `validate_request`) | P only (run_suite `invalid_request` 2933/2983, parsed as `summary`) | not carried at P; L only (4695/6266) |
| `run_suite:begin` / `:recover` (ER 439-486; run_suite 2894) | not carried (the probe does not read `JobStore` begin; `_run_mine` prints a summary only when run_suite prints one; no read of 2894's output proved here) | not carried |
| `run_suite:reparse`, `:phantom_story`, `:detail_target`, `:untyped_story_run`, `:missing_executor` | not carried (other `run_suite` entry points, not `--mine`) | not carried |
Advisory sites (A: 1431, 2041) are never counted as carriers (E9). L sites carry nothing for K1b. Caveat: P-only rows for red_sandbox name an id as carried when `run_suite --mine` PRINTS its `told` at that refusal; the row labels above are the proof K1b must see green in the canon before it relies on it.

## FR walk
A: FR-1/FR-2 the refusal lists the further checks with their door; FR-4 n/a (no check added). B: FR-6 the lines are the row text through `told_line` (the one renderer); FR-7 n/a. C: FR-14 the line order is a contract and is pinned (`last-line-is-check`); FR-42 each state (no records, unreadable row, beyond cap) has a stated output. D: FR-16, FR-18 n/a; FR-59 an unreadable row prints a sentence, never a pass. E: n/a. F: FR-41 beyond the cap the tail line names the count. G: FR-30 English only (checked by `--lang`); FR-47 code is the printer, no judgment; FR-54 siblings below.

## Edge notes
E1: no records / not a list / dict / None: byte-equal (rows). E2-E7 each have a row. E8: no marker moved. One tension found, followed item 1 literally: E1 says "a plain `str` ... output byte-equal to today", item 1 says `first = ""` for a non-Record problem, so a plain str problem WITH records prints the extras. In `run_guarded` a str problem never carries records (a bare ValueError), so no road differs today; a Lead decision is needed only if a later caller passes records with a str.
Row id that `row_for` cannot read: the sentence is "(the factory's requirement row <id> could not be read: the row states no requirement; this is a factory defect). Door: ." (spec said the "could not be read" sentence: it is).
The spec's "an existing row pinning 'first check only' is updated": none exists in the owned files (the only mention is the comment at `test_contract_slices.py:980`, which is K1b's file).

## Siblings and analogs
- `role_cli.epilog`, `hooklib.block`, `stage_guard.deny`: untouched (one Record each).
- Analog noticed, not fixed: `story_run.py`/other callers of `role_cli.refuse` with a `RequestError` do not exist besides `run_guarded`; `import_test_receipt._told_request_error` still stores the first record as `args[0]` AND in `records` (E2 dedups it).
- `test_red_sandbox_diagnostic.py` holds the same world builder (`world`, `request`) that the new diagnostic rows replicated in `test_red_sandbox_probe.py` (a circular import forbids reuse): a shared helper would remove the copy (queue to Lead).

## Needed beyond the manifest
`scripts/stage_joints.py` (`row_for`, `told_text`), `scripts/execution_request.py` 128-150, `scripts/probe_by_code.py` 8062-8113 and `_plan_cli`, `scripts/tests/test_red_sandbox_diagnostic.py` 36-145, 223-295, `scripts/tests/test_probe_by_code.py` 258-322.
