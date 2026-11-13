# T1a report - census units from the wide non-list transports (builder, 13.11.2026)

RESOLVED (Lead answer, same day): the three hooklib rows take all 12 roles + conductor; see "Final state" at the END of this file, which
supersedes every "STOPPED / provisional / 110 rows / 0.9964 / 2690" statement below. Original status text follows.

Status: STOPPED on edge (e) for `hooklib.py`; everything else is done and verified. NOTHING IS COMMITTED (the work sits uncommitted
in `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1a`, branch `wip/tbw-t1a`, base b355384): with three units rowless the census C1
is red and the join is 0.9964, so a commit would put a red base on the branch. Resume = answer the question below, add the three
rows, re-run the DoD.

## Question for the Lead (blocks the commit)

Q-hooklib. "Lead decisions" Q3 says the seven hook-guard rows take the roles of the file's existing rows, and STOP for a file whose
existing rows disagree. `stage_done.py` (8 existing rows) and `stage_guard.py` (23 existing rows) agree: every row carries all 12
roles + `conductor`; their four A rows (`stage_done.py::main`, `::record_acceptance`, `::set_facts`, `stage_guard.py::explain`) are
written so. `hooklib.py` DISAGREES. Its 10 existing rows (read from `judgment-census.json` at b355384):

- all 12 roles + conductor (7 rows): `append_jsonl_line`, `artifact_root`, `artifacts_dir`, `read_config_file`, `story_of`,
  `story_root`, `story_root_at`
- `["conductor"]` only (3 rows): `_run`, `run`, `run_forms_problems`

Left unwritten (no row, nothing guessed): `hooklib.py::block`, `hooklib.py::require_project_at`, `hooklib.py::story_cli` (A rows 38-40:
class shape, owner data, sites hooklib.py:991, :230, :579). Please name their roles. Effect of each answer on the ratchet, on top
of the table below: all 12 roles + conductor = +3 on every one of the 13 role keys; `["conductor"]` = +3 on `conductor` only
(`safety` unchanged either way, the three are shape). The rows are class shape, owner data, `note` "T1a, Lead decision Q3 ..." as
the other four.

## Step 0 (probe on `Wa\`, before any edit)

Command: `python -B C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\61b75a79-16bf-492f-9cd2-02266607001d\scratchpad\t1a_probe.py C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1a\ai-packages\qa-factory`
(the spec 3.2 source; exit 0, empty stderr, 2m23s). Output saved at `...\scratchpad\t1a_run\probe0.json` (16896 bytes). Compared
with the JSON block of section 0 of the accepted rows file by a script (`...\scratchpad\t1a_run\cmp.py`, parses that block and
compares each key):

```
old_units True
new_units True
A True
B True
B0_override_false True
C True
narrow_lost True
list_only_units_not_created True
```

So `old_units` 1145, `new_units` 1257, |A| 113, |B| 13, |C| 1, `narrow_lost` `[]`, 2202 list-only units: identical to the rows file;
no stop at step 0.

## What was changed (owned paths only)

`scripts/tests/test_judgment_census.py`: `units_of` calls `raise_family(..., wide=True)`, takes `scanned = sites(...)` and filters ONCE
(`state != "walk_error"` and `transport != "list"`) into `wide`, before `wide_by_file` and the flip loop (E4 positional invariant, a
comment states it); `found["sites"]` is `len(wide)`. Docstring "WHAT A UNIT IS" u3, `units_of` docstring and `BLIND_SPOT` name the wide
transports, the list exclusion and the stderr blind spot. New table `WIDE_ROWS` (17 rows) + one test function
`test_wide_rows_units_come_from_non_list_sites_only` (registered in `TESTS`). `scripts/tests/fixtures/judgment-census.json`: A rows
(110 of 113 so far), 13 B rows changed, the C row removed, `ratchet`, `about`.

Row ids of the §3.0a T1a row, all present: `w-stderr-return`, `w-stderr-exit`, `w-stderr-raise`, `w-stderr-exit-name`, `w-stderr-note`,
`w-sys-exit-str`, `w-systemexit-str`, `w-refuse`, `w-module-level`, `w-walk-error`, `w-append-no-unit`, `w-append-no-flip`,
`w-narrow-subset`, `w-flip-existing`, `w-flip-nested-span`, `w-script-unit-replaced`, `w-raise-named`. The narrow-road subset (E5) is also asserted for EVERY row, not only `w-narrow-subset`.

Rows were applied by a scratchpad script (`...\scratchpad\t1a_run\apply_rows.py`: parses the accepted rows file, applies Lead
decisions Q1/Q2/Q3, writes the json). It is not committed (command hygiene pt. 4a asks for a named committed script; this one is
attached by path only) - a deviation to rule on. Untouched rows keep their exact text; A rows were inserted after the last row of
their file (the file's existing order is not sorted), new files at their sorted place.

## DoD runs (verbatim)

1. Census test (after the edit, with the 110 A rows), `( cd Wa/ai-packages/qa-factory && time python -B scripts/tests/test_judgment_census.py )`:

```
FAIL test_c1_every_unit_has_a_row_and_every_row_a_unit — 
  hooklib.py::block is a check unit (u3) with no row in judgment-census.json: add a row {file, function, class, roles, owner} - ...
  hooklib.py::require_project_at is a check unit (u3) with no row in judgment-census.json: ...
  hooklib.py::story_cli is a check unit (u3) with no row in judgment-census.json: ...
PASS test_c2_every_row_is_well_formed
PASS test_c3_the_ratchet_is_dense_and_only_shrinks
PASS test_c4_the_meaning_ceiling_is_the_tests_constant
PASS test_c5_no_refusal_hides_behind_a_wrapper
PASS test_c6_totals_line
PASS test_scan_constants_are_the_specs
... (all test_neg_* PASS)
PASS test_blind_spot_states_the_subclass_clause
PASS test_wide_rows_units_come_from_non_list_sites_only
=== judgment_census: 24/25 ok ===
real	1m13.873s
census: 280 files scanned, 1257 units; shape=928 xref=208 word-list=0 meaning-proxy=8 meaning=24 safety=86; breach=1; blocks_overrides=10;
blocking_per_role: conductor=757 qa-automator=187 qa-bug-reporter=150 qa-case-critic=170 qa-case-designer=153 qa-code-critic=157
qa-doc-scribe=148 qa-failure-analyst=159 qa-requirements-tester=167 qa-retro-analyst=153 qa-runner=157 qa-scout=149 qa-test-strategist=183
```

The only red is C1 and it names exactly the three hooklib units (the question). C3 is green: the ceilings written equal the counts,
`word-list` 0, `meaning-proxy` 8, `meaning` 24, `breach` 1, `blocks_overrides` 10 did not move. Wall time (edge f): BEFORE the edit
3m39.550s (`census_before.txt`, 24/24 ok, machine busy at that moment), AFTER 1m13.874s. Both are over 60 s, and the BEFORE figure
already was: this is a QUESTION, not a cut - the census test is a CI file (`slow_tests.json` lists it), the 60 s line cannot be met
locally even without T1a. The two timings differ by 3x from machine load, so they do not measure T1a's own cost.

2. The join (spec 0.1) in `Wa\ai-packages\qa-factory`: `python -B scripts/refusal_registry.py --sites --wide --census scripts/tests/fixtures/judgment-census.json --json`:

```
sites 3078, units 836, units_with_row 833, units_no_row 3, join_share 0.9964114832535885, role_reachable_units 217,
conductor_only_units 616, walk_errors 0, check_arg_errors 1
rowless: hooklib.py::block, hooklib.py::require_project_at, hooklib.py::story_cli
```

NOT the required `units_no_row 0` / `join_share 1.0`: the three hooklib units are the whole gap (STOP (c), but with the cause known).
BEFORE T1a (spec 0.1, a2c88d8) it read 113 rowless; this is 3.

3. The probe on `Wa\` after the edit: `old_units 1257, new_units 1257, A [], B [], C [], narrow_lost [], B0_override_false []`
(`probe1.json`). The required `"A": []`, `"B": []`, `"C": []` and `old_units` 1257 hold (the probe lists UNITS, so it is satisfied
without the three rows; the join and C1 are what see them).

4. `test_scenario_walk.py` `=== test_scenario_walk: 93/93 ok ===`; `test_scenario_world.py` `=== test_scenario_world: 33/33 ok ===`;
`test_refusal_registry.py` `=== test_refusal_registry: 493/493 ok ===`; `python -B scripts/selftest.py --lang`
`=== qa-factory selftest: 2/2 ok ===`. The witness command `scenario_walk.py --witness-for <test_judgment_census.py> <judgment-census.json>`
printed: for the test file `test_scenario_cart_1.py`, `test_scenario_local_1_0108.py`, `test_scenario_local_1_arm_b.py`,
`test_scenario_walk.py`, `test_scenario_world.py` (+ "no scenario or keep row covers ..."), for the json `keep test_judgment_census.py`.
The first three are in `slow_tests.json` (never run locally, per the rules); walk and world were run (above); `test_judgment_census.py`
is run in item 1. The three slow scenario files are CI-only witnesses here.

## Section 4 recomputed (state as written: 110 A rows, hooklib's three held)

Reason for every line: `T1a: census rows for wide-transport units (told-before-work T0 gate item 2)`. A column = A rows naming the role;
B column = B rows naming the role AFTER (a B unit was non-blocking, so its roles enter whole); C = removed row, effectively blocking.

| role | old | +A | +B | -C | new | new - old |
|---|---|---|---|---|---|---|
| qa-automator | 173 | 12 | 2 | 0 | 187 | +14 |
| qa-bug-reporter | 139 | 11 | 0 | 0 | 150 | +11 |
| qa-case-critic | 164 | 6 | 0 | 0 | 170 | +6 |
| qa-case-designer | 139 | 14 | 0 | 0 | 153 | +14 |
| qa-code-critic | 139 | 15 | 3 | 0 | 157 | +18 |
| qa-doc-scribe | 139 | 10 | 0 | 1 | 148 | +9 |
| qa-failure-analyst | 140 | 18 | 1 | 0 | 159 | +19 |
| qa-requirements-tester | 157 | 10 | 0 | 0 | 167 | +10 |
| qa-retro-analyst | 139 | 13 | 1 | 0 | 153 | +14 |
| qa-runner | 140 | 16 | 1 | 0 | 157 | +17 |
| qa-scout | 139 | 10 | 0 | 0 | 149 | +10 |
| qa-test-strategist | 171 | 12 | 0 | 0 | 183 | +12 |
| conductor | 680 | 68 | 9 | 0 | 757 | +77 |
| sum | 2459 | | | | 2690 | +231 |

Reconciliation: sum +231 = 214 role-entries of the 110 A rows + 17 of the 13 B rows (automator 2, code-critic 3, failure-analyst 1,
retro-analyst 1, runner 1, conductor 9) - 1 (C row, doc-scribe) = 231. Against the rows file's table (+186, 113 A rows with the
seven hook-guard rows at conductor): the difference is the Q3 override of four rows (each takes 12 roles + conductor instead of
conductor: +4 x 12 = +48 role-entries on the 12 roles, conductor unchanged) minus the three held hooklib rows (-3 on conductor):
186 + 48 - 3 = 231. The census test's C3 independently confirms every ceiling (green). Each B/A/C term is also what the test counted:
the written ceilings equal the test's `blocking_per_role` counts exactly (item 1 totals line).

`safety`: 82 -> 86 (+4 A rows judged safety: `archive_task.py::cmd_archive`, `artifact_supersede.py::main`,
`probe_by_code.py::_read_model_file`, `probe_by_code.py::_unrestored_exit`; B and C rows add 0).

## Ratchet rows

- `blocking_per_role.qa-automator` 173 -> 187; `qa-bug-reporter` 139 -> 150; `qa-case-critic` 164 -> 170; `qa-case-designer` 139 -> 153;
  `qa-code-critic` 139 -> 157; `qa-doc-scribe` 139 -> 148; `qa-failure-analyst` 140 -> 159; `qa-requirements-tester` 157 -> 167;
  `qa-retro-analyst` 139 -> 153; `qa-runner` 140 -> 157; `qa-scout` 139 -> 149; `qa-test-strategist` 171 -> 183; `conductor` 680 -> 757
  (provisional: add 3 per role named by the hooklib answer); reason `T1a: census rows for wide-transport units (told-before-work T0 gate item 2)`.
- `safety` 82 -> 86, same reason.
- `word-list` 0, `meaning-proxy` 8, `meaning` 24, `breach` 1, `blocks_overrides` 10: unchanged.
- census rows: 1145 + 110 - 1 = 1254 now (1257 with the three hooklib rows).

## Rows decided by the Lead's overrides

Q1 confirmed (no change to the file). Q2 replace: the four relabelled B rows (`manifest_put.py::run` -> automator, code-critic;
`project_decisions.py::run` -> retro-analyst; `run_suite.py::_refuse_phantom_story` -> automator, code-critic, failure-analyst, runner;
`window_record.py::run` -> code-critic) lose `conductor`. Q3: see the question. The conductor group of step 4 is in each row's `note`.
`class`/`owner` as in the rows file table. One discrepancy inside the rows file: the table gives `archive_task.py::cmd_archive` owner
`data`, its "Undecided" paragraph says `safety/intent`; I followed the table (`data`) and the Lead's "accepted as drafted".

## FR walk (PROJECT.md package rule 1; the diff is test + fixture only)

A, B, C, D, E, F: not applicable - no refusal text, no text to a person, no contract, id or report changed. G: FR-29 no control byte and
FR-30 English only - `selftest.py --lang` 2/2 ok (item 4); FR-31 no timing test added; FR-32 root cause is the unit rule (one filter),
with a test row per behaviour; FR-54 siblings by the map: axis 32 (rows, ratchet and unit rule in one change - done), `refusal_registry.py`
reader of `units_of` (`_census_blocking`) read, not edited, the join is its check.
AR walk: AR-29 (the census grows by data judged per unit; classes shape/xref/safety only, no `word-list`/`meaning-proxy`/`meaning`/`breach`), AR-20
(every raise listed above), AR-13 (one scanner: `units_of` calls `refusal_registry.sites(raises=raise_family(wide=True))`, no `ast.Raise` or
`ast.Call` walk added to the test).

## Deviations from the spec

1. STOP on Q3/hooklib (above): 110 of 113 A rows written, no commit, no push. DoD items "join 1.0" and "`=== judgment_census: N/N ok ===`
   with C1 green" are NOT met, for that one reason.
2. Rows applied by an uncommitted scratchpad script (pt. 4a).
3. `|B|`, `|A|`, `|C|` equal the rows file; spec 3.2 expectation 113/11/1 differs only by two B units, as the rows file says.
4. Census wall time over 60 s before and after: a question for the Lead (CI-only file), see item 1.

## Analogs noticed (not widened)

- `hooklib.py`'s own existing rows are mixed (7 all-roles, 3 conductor-only): the same mixed-label class as the rows file's "Analog rows";
  `_run`, `run`, `run_forms_problems` read as hook entry points of the same road.
- `external_writes.py::check|run|list_proposals|refuse_local_key` safety/intent vs the new `main`/`record_result` shape rows (rows file, not changed).
- `check_arg_errors 1` still printed by the join (T1c's, by the spec).
- `slow_tests.json` lists `test_judgment_census.py` itself: the 60 s rule of edge (f) cannot hold for it on this machine.

## Beyond the manifest

Read: `scripts/refusal_registry.py` (`sites`, `_scan_wide`, `wide_report`, `_census_blocking`), `scripts/slow_tests.json`,
`scripts/tests/test-layers.json` rows of the witness files, `.githooks/commit-msg`.

## Final state (after the Lead's answer)

Rows added: `hooklib.py::block`, `::require_project_at`, `::story_cli` (shape, data, all 12 roles + conductor, `note` Q3). Census rows
1257 (1145 + 113 - 1). Ratchet rows (reason `T1a: census rows for wide-transport units (told-before-work T0 gate item 2)`; the 13
hooklib +3 raises: `T1a: guard refusals now counted as units`):

| key | old | new | new - old |
|---|---|---|---|
| qa-automator | 173 | 190 | +17 |
| qa-bug-reporter | 139 | 153 | +14 |
| qa-case-critic | 164 | 173 | +9 |
| qa-case-designer | 139 | 156 | +17 |
| qa-code-critic | 139 | 160 | +21 |
| qa-doc-scribe | 139 | 151 | +12 |
| qa-failure-analyst | 140 | 162 | +22 |
| qa-requirements-tester | 157 | 170 | +13 |
| qa-retro-analyst | 139 | 156 | +17 |
| qa-runner | 140 | 160 | +20 |
| qa-scout | 139 | 152 | +13 |
| qa-test-strategist | 171 | 186 | +15 |
| conductor | 680 | 760 | +80 |
| sum | 2459 | 2729 | +270 |

`safety` 82 -> 86. Unchanged: word-list 0, meaning-proxy 8, meaning 24, breach 1, blocks_overrides 10.
Reconciliation: +270 = 231 (table above: 110 A rows + 13 B - 1 C) + 39 (3 rows x 13 roles) = 270; per role e.g. automator 14 + 3 = 17,
conductor 77 + 3 = 80. Equals the rows file's +186 with Q3 applied: 186 + 48 (4 non-hooklib Q3 rows x 12 roles) + 36 (3 hooklib rows x 12
roles; their conductor +3 was already in 186) = 270. No disagreement. The census totals line printed by the test equals every written ceiling.

Witness (census C1-C6 + the two new tests called as functions, one scan; the whole file not re-run, per the Lead; last whole-file timings:
before 3m39.550s, after 1m13.874s):
```
PASS test_c1_every_unit_has_a_row_and_every_row_a_unit
PASS test_c2_every_row_is_well_formed
PASS test_c3_the_ratchet_is_dense_and_only_shrinks
PASS test_c4_the_meaning_ceiling_is_the_tests_constant
PASS test_c5_no_refusal_hides_behind_a_wrapper
PASS test_c6_totals_line
PASS test_blind_spot_states_the_subclass_clause
PASS test_wide_rows_units_come_from_non_list_sites_only
census: 280 files scanned, 1257 units; shape=931 xref=208 ... safety=86; breach=1; blocks_overrides=10; blocking_per_role: conductor=760 qa-automator=190 ...
```
Join: `units 836, units_with_row 836, units_no_row 0, join_share 1.0, check_arg_errors 1`. Probe after (earlier run, unchanged): A [], B [], C [],
old_units 1257. Other runs of the earlier section (walk 93/93, world 33/33, refusal_registry 493/493, selftest --lang 2/2) stand.
