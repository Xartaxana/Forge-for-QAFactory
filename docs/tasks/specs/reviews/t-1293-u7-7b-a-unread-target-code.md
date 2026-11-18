# t-1293 - critic review of U7 7b-A (commit a6146c53, branch worktree-u7-7b-a)

reviewed: a6146c53 (worktree HEAD = a6146c53, clean; merge base ad336d5c; origin/main 766fad1a)
spec: r4 §3/§2 Group A + §0 rows of 7b-A, under the block "ACCEPTED with amendments" (N1, N2, N3, N5, N7, N8 position note, row budget, witness list)

**Verdict: ACCEPT WITH FIXES** (NEEDS WORK in rule 6 words; 0 blocking, 4 fixes, 2 questions). This verdict is an input to acceptance; the decision to accept stays with the Lead.

## Keys

**K1 POSITION in `s7_pretriage.decide` - PASS.** The `unread` branch (tip s7_pretriage.py 233-238) sits after `answers` (bound, 226-228) and `competing` (229-232), before `!= "manual"`. Probe on the tip: answered unread -> `by_analyst [('unread','u1')]`, `left []`, `write []`; unanswered -> `left` with why "the run's report could not be read by code; the analyst reads its log", `write []`; `_code_row` reachable only for `manual` (branch order). A bound or competing row still decides first; manual still reached. Observation, not a finding of this diff: a `source: code` row that binds an unread target lands in `by_code` and `pretriage.closes` (461) can be True. The same holds for kind `result` on main. Code writes `source: code` rows only for manual keys, so reaching this needs a name collision or a hand-forged row. At delivery `rederives` is False for such a row, so the result is NOT_EXECUTED_NOT_RE_DERIVED and `no`.

**K2 ERROR DIRECTION - PASS.** Probe (verbatim in the trail): `_reading_of([])=''`, `['']`/`[None]` -> `unanswered`, `['NOT_EXECUTED','']` -> `unanswered`, `['','APP_BUG']` -> `red`, `['not_executed']` -> `red`, `['FLAKY']` -> `red`. `unread_readings`/`unread_case_reading`: rows None / [] / "x" -> all `''`, case `unanswered`. One of two answered -> `unanswered`. Two NE rows on one target -> `''` (several). A row of another attempt -> `''`. A bare name over two targets (ambiguous) -> `''`. An empty verdict -> `''`. Coded + passed in one case -> `''`. A passed row carrying the code -> `''` and `{}`. A nameless coded row -> `unanswered`. Report None -> `''`. No input gave `read` unless every instance had its own NOT_EXECUTED row. The one exception is two current rows with the same instance_id (one NE row reads both). That shape cannot occur, because the reducer keeps one current row per instance. Minor asymmetry, in the safe direction: a legacy report (no `current_results` list) gets `unread_readings` `{'u1': 'NOT_EXECUTED'}` but `unread_case_reading` `''`.

**K3 `build_run_block` - PASS.** Condition (run_suite.py 546-550) = `status == not_run` AND `no_junitxml` AND `reporter == none` AND no `reporter_inferred_from` AND `execution_status == not_executed` AND not `blocked` AND no report rows. It sits before the timeout block (551), so `PROJECT_TIMEOUT_CODE` overwrites it. `execution_status()` (1364-1387) gives `not_executed` only for exit 0 with no totals, so a non-zero exit is `broken_run`. The node-id block sets `blocked`. The side effect (a `file` contract with zero rows: `report_unread` replaces `id_not_in_report`) is inside the spec: N8 says "REPLACES `_file_verdict`'s `id_not_in_report`". Readers, by a case-insensitive grep of `id_not_in_report` over the package:
- `run_history.py:422-423` reads the code only under `failed_block` (600: `execution_status == "failed"`). A coded row needs `not_executed`, so this reader never saw the case and loses nothing.
- `run_suite.py:2406-2415`: the console count and the "no row in the report" line stop firing for that case. The run still prints `RUN REPORT GAP` (2302-2305, reporter != pytest), plus `selection_line`'s short count (2417).
- The fixtures and quarantined tests asserting `id_not_in_report` (`test_run_suite_reports.py` 927/945, local1 `16f0-initial.summary.json` reporter `junit-xml`) have report rows or a declared reporter, so they are untouched.

No reader loses a case it needed.

**K4 amendments - PASS.**
- N1: `("manual","observation","unread")`, docstring and call-site comment restated, one entry pair in the existing table.
- N2: `_result_row_keys` holds the whole key expression with `area_of` and the alias drop. It matches the removed loop line for line (falsy skip, `str`, `area_of.get(str(key))`), and both `run_results` and `unread_case_reading` call it.
- N3: `_result_names` (four keys, non-empty, in order) is shared by `triage_targets` and the unread loop. The test asserts names `["u1","m::u1","m.u1"]`.
- N5/N7: one private `_reading_of`, called once per case. The N5 rule overrides A2's "and none is ''", as the block says.

None widened. Role text and vocabulary are byte-equal to §2 A6.

**K5 PREMISE on the tip - PASS (reproduced).** `handoff_check.check` over the S7 null-outcome form, report = an unread `u1` and a failed `f1`:
- rows f1+u1 (u1 NOT_EXECUTED + limitation) -> `[]`.
- row for f1 only -> `scope: ... 1 failure(s) of work/run-report.json have no row in it: u1`.
- two rows on u1 -> `... 2 rows answer the failure u1; ke...`.
- Zero rows: the builder's row, narrow-called -> `want your reading: u1,` (8/8 checks).

`validate_artifacts.check_triage_v0` on an analyst NOT_EXECUTED row -> `errors: []`. It is kind-agnostic, with no target check.

**K6 TEST BUDGET - PASS with two fixes.** Counted: tests +93, py code +165, text +5 (numstat), so within budget. Killing power, judged by reading:
- The predicate table entries kill rules 3 and 5.
- The `test_triage_identity` names assertion kills a names[0]-only N3 mutation.
- The bug_records pair kills the removal of `unread` in `_walk_has_no_run`.
- The null-outcome row kills both finalize `or targets["unread"]` lines and the `_no_failure_shown` branch.
- The story row kills `failures_to_triage` and `brief`.
- The build_run_block table: "timeout wins" kills a reordering; "report row exists" kills `not report_rows`. "An inferred reporter" (reporter=`pytest`) kills nothing beyond "declared reporter": both die on `reporter == "none"`. `reporter_choice` (299-322) returns `inferred_from` only with an INFERRED_KINDS reporter, never with `none`. The spec named the row, so it stays; it is noted as weak.

The unwritten variant SHOULD be written (Fix 3): it is a changed value at a door (the block row's `reason_code`) reached through the separate `by_file` branch. One entry costs about 2 lines. Restatement rows (Fix 4): `test_triage_identity.py::test_an_unread_row_is_a_target_of_its_own_kind` asserts `unread_readings` and `unread_case_reading` directly, which the spec's NO-row list forbids ("`unread_readings`, `unread_case_reading`, `_reading_of` ... the temporal world 7b-B not merged"). `multiple` is spec-named and stays.

**K7 INTERIM STATE - PASS for the builder's claim, with one question.**
- `ledger.test_state` 1172-1182: an analyst NOT_EXECUTED row gives `failed:NOT_EXECUTED`. In the kinds file that maps to `not_executed_unproven` = `no`/factory (read from `delivery-verdict-kinds.json` on the tip). With no row: `not_executed:...`, which maps to `not_executed` = `no`/product.
- `check_delivery.not_executed_findings`: `rederives` is False for an analyst row (decide never writes a row for unread), so the finding is kept.
- `check_delivery.run_reasons` 1302-1310 reads `triageable_not_executed`, so the twin moves with S7 (AR-19 held) and per-case kinds decide.
- `check_delivery.triage_reasons` 1484-1499 handles kinds result/manual/observation only. In the interim an UNANSWERED unread target past S7 by a person's word gets no `triage:` word, but stays `no` through the ledger.
- `contract._instance_failed` -> False for unread (probe), so `red_blocked_rows` ignores it, the same as any `not_run` today.
- `red_sandbox` 1439-1441: `kind` there is `execution_request.fresh_evidence` state, not a triage kind; a `not_run` row never has outcome `passed` (2162/2170).
- No crash anywhere.

The ONE green road found: `ledger.test_state` 1174-1179 returns `passed_green` for any bound row with `verdict FLAKY` and `fix_result: fixed`. The role text now invites "the failure verdict the log shows" on an unread target, and its reruns are unread too. `_reading_of` calls FLAKY `red`, so the ledger and the helper disagree. The spec's D1 (7b-B) keeps "every other verdict keeps 1173-1182", so this is a spec question for the Lead (Q1). It is not a defect of this diff's code.

**K8 census and role-load - PASS.** No new or renamed function matches `UNIT_NAME_RE` (checked by name); the only touched unit, `bug_records.reproduction_problems`, changed by a comment and has row 76 (`xref`). The diff adds no `refusal(` call. Narrow calls on the tip: `test_c3` PASS, `test_c5` PASS. `test_c1` is RED on a unit the diff does not touch: `controller.py::_s5_code_only_problems` has no census row on ad336d5c or on origin/main either (grep count 0, def count 1). It is pre-existing and outside this node. Its list names no unit of this diff, which is the positive control that c1 sees units. The census needs no row for this change. The whole file is on the slow list (96.9 s), so the canon judges it. `role_load.py --all` on the worktree prints `qa-failure-analyst 21,659 ... 19,609 (process) ... ratchet 21,659`, equal to the json rows (+102 each, named in the commit as AR-20).

## Standing questions

- Q1 FIT: all §0/§2 Group A rows and N-items present, with the error direction toward not coding and `no`.
- Q2 builder's own choices: `out["all"]` gets the spellings of all four names (consistent with the result loop); `add_result` extracts the existing loop body unchanged. Safe.
- Q3 SEAMS: edits stay inside the listed functions. `changelog.d/universality-1-...md` is outside the listed owns. It is the package's release fragment, additive and conventional; not a finding.
- Q4 CLASS: SIBLING_MAP axes walked for "kind set of triage_failures": every reader of `triage_targets` keys (driver, handoff_check, finalize x2, s7_pretriage, bug_records) handled. Delivery readers are 7b-B (non-goal), and K7 confirms they stay `no` in the interim. The FLAKY->passed_green analog is named under Q1 (owner 7b-B, `ledger.py::test_state`).
- Q5 tests: see K6. No new test file; (d) no test rewritten or deleted (one key-list assertion widened).
- Q6 DUPLICATION: FINDING (Fix 1). The predicate "`result_status(row) == "not_run"` and `reason_code == REPORT_UNREAD_CODE`" is written three times: contract.py 4655-4656 (`triage_targets`), contract.py 4892 (`unread_case_reading`) and s7_pretriage.py 387-388. Spec §1.1 AR-13 change check: "no reader restates 'row is unread' outside contract.py (grep `REPORT_UNREAD_CODE` -> only contract, run_suite producer, tests)". My grep (case-insensitive, `REPORT_UNREAD_CODE|report_unread`, positive control: it finds the definition at contract.py:4597) shows s7_pretriage.py:388. §0 B1 words rule 3 that way, so the spec contradicts itself; the stricter AR-13 check should win. Clone ratchet: forge-check output not attached, not re-derived.
- Q7 CODE QUALITY: none blocking. No new function over 60 lines; no nesting over 3. `not summary.get("reporter_inferred_from")` cannot fire with `reporter == "none"`. It is a spec-mandated defensive clause, so this is a note only. The nameless coded row's note reaches `_no_failure_shown`'s "failed result row(s)" wording. That is a generic refusal and the routing is spec'd (A2 "a note in unnamed"); note only.
- Q8 HYGIENE: 0 Cyrillic in added lines (positive control `echo тест | grep -cP` -> 1); LF kept (`ls-files --eol`).
- Q9 RATCHETS: `role-load.json` `ratchet_tokens.qa-failure-analyst` 21557 -> 21659 and `process_ratchet_tokens.qa-failure-analyst` 19507 -> 19609. Reason: the A6 paragraph (AR-20), named in the commit and equal to the measurement. No other ratchet file in the diff.
- Q10 ARCHITECTURE: FINDING (Fix 2). The commit names AR-13, AR-22, AR-28, AR-20 and has a judgment line. AR-19 is touched (rules 3/5 of the ONE predicate read by S7 entry and by `check_delivery.run_reasons` 1308), and spec §1.1 says "AR-19 ... named in commit". It is not named. VARIETY: a reporter-`none`, exit-0 project now reaches the analyst instead of the S7 entry refusal. A non-zero exit stays `broken_run` (F-r4-1). No silent default and no hand-off past the role.
- Q11 JUDGMENT: the reading of the log moves TO the role; code checks shape and binding. No census row, `blocks_override`, scan constant or craft marker was added. The judgment line is accurate.
- Q12 ONE ROAD: none found. Grep of the added `.py` lines for runner and language words: only `reporter == "none"` (absence of a reporter, the task's own condition, axis 3) and `pytest` inside a test row.

## Fixes (none blocks the merge; fix before merge)

1. `contract.py`: add one public predicate (e.g. `is_unread_row(row) -> bool`: dict, `result_status == "not_run"`, `reason_code == REPORT_UNREAD_CODE`). Call it from `triage_targets`, `unread_case_reading` and `s7_pretriage.triageable_not_executed` (rule 3). After the fix, a grep of `REPORT_UNREAD_CODE` finds only contract.py, run_suite.py (producer) and tests.
2. Commit message `architecture:` line: add AR-19 ("S7 entry and delivery `run_reasons` read the same predicate; rules 3/5 widened in that one place").
3. `test_s7_pretriage.py::build_run_block_codes_only_a_run_that_read_nothing`: add one entry with a contract carrying `file` (zero report rows, `run_none`) -> `reason_code == C.REPORT_UNREAD_CODE`. This covers the N8 replacement of `id_not_in_report` through the `by_file` branch.
4. `test_triage_identity.py::test_an_unread_row_is_a_target_of_its_own_kind`: drop the direct assertions of `C.unread_readings` (both) and `C.unread_case_reading`. They are on the spec's NO-row list, and 7b-B's ledger/plan-row door covers them. Keep the `multiple` assertion.

## Questions for the Lead (not decided here)

- Q1: an unread target answered `FLAKY` with `fix_result: fixed` reads `passed_green` in `ledger.py::test_state` (1176-1179), and spec D1 of 7b-B keeps "every other verdict". Should 7b-B's D1 read FLAKY on a coded row as not green (for example `not_verified_flaky`), in line with `_reading_of` -> `red`? The owner would be 7b-B, as an amendment of its dispatch.
- Q2: `test_judgment_census.py::test_c1` is red on origin/main because of `controller.py::_s5_code_only_problems` (no census row). That is outside this node. Is it already a node?

Note: the builder's own report and witness were not in `given`. This verdict rests on the runs below, not on the report's claims.

## Trail

- Read: spec r4 lines 1-329; `git diff origin/main...a6146c53` (whole); tip contract.py 4518-4524, 4718-4900; s7_pretriage.py 195-245, 349-461; run_suite.py 470-620, 1364-1387, 2240-2425, 290-322; run_history.py 405-440, 600; check_delivery.py 1290-1322, 1327-1338, 1475-1499, 2029-2035; ledger.py 1163-1250 (test_state, `_run_and_triage_rows`); red_sandbox.py 1385-1450; validate_artifacts.py 2501-2546; delivery-verdict-kinds.json (ledger_states, kinds); judgment-census.json (grep); slow_tests.json (grep).
- `python -B .../tests/test_s7_pretriage.py` -> `=== s7 pretriage: 479/479 ok ===`, exit 0.
- `python -B .../tests/test_triage_identity.py` -> `Ran 32 tests ... OK`.
- Narrow import-and-call: `an_unread_target_keeps_its_analysts_row` 8 checks, 0 failed; `refresh_keeps_a_row_by_the_one_matching_rule` 7/0; `test_bug_records.a_draft_of_a_place_the_runner_never_ran` 30/0; `test_story_run_s7.u7_7a_a_not_executed_a_role_can_triage_enters_s7` 10/0.
- Inline probe (K1/K2/K5/K7), outputs quoted in the keys above.
- `test_judgment_census`: c1 AssertionError `controller.py::_s5_code_only_problems is a check unit (u1) with no row`; c3 PASS; c5 PASS. `git show ad336d5c|origin/main:` census grep 0, controller def 1.
- `python -B .../scripts/role_load.py --all` -> `qa-failure-analyst 21,659 2,050 19,609 ... ratchet 21,659`.
- `git diff --numstat`: tests +93 -1; py code +165 -50; all non-test +170 -54.
- Not run locally: `test_s7_null_outcome.py`, `test_bug_records.py`, `test_story_run_s7.py`, `test_judgment_census.py` whole (slow / canon-only; the canon judges).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Readers of the new kind unread walked: driver_stage_s7, handoff_check._no_failure_shown, finalize reduce/refresh, s7_pretriage decide/brief/pretriage/predicate, bug_records._walk_has_no_run all handled; delivery readers (7b-B) stay no in the interim (ledger failed:NOT_EXECUTED / not_executed, not_executed_findings, run_reasons twin) except one analog named for the Lead: ledger.py::test_state FLAKY+fixed -> passed_green on an unread target (owner 7b-B, question Q1). Predicate restated three times (Fix 1).",
  "fixes": [
    "Fix 1: contract.py one predicate is_unread_row(row) used by triage_targets, unread_case_reading and s7_pretriage.triageable_not_executed rule 3; grep REPORT_UNREAD_CODE then finds only contract, run_suite producer, tests (AR-13 change check of spec 1.1)",
    "Fix 2: commit architecture line names AR-19 (rules 3/5 of the one predicate read by S7 entry and check_delivery.run_reasons)",
    "Fix 3: test_s7_pretriage.py::build_run_block_codes_only_a_run_that_read_nothing gains one entry with a file contract, zero report rows -> reason_code report_unread (N8 replacement of id_not_in_report)",
    "Fix 4: test_triage_identity.py::test_an_unread_row_is_a_target_of_its_own_kind drops the direct asserts of unread_readings and unread_case_reading (spec NO-row list); multiple assert stays"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r4-7b-7c-e7.md lines 1-329",
      "git diff origin/main...a6146c53 (whole)",
      "ai-packages/qa-factory/scripts/contract.py 4518-4524, 4718-4900 at a6146c53",
      "ai-packages/qa-factory/scripts/s7_pretriage.py 195-245, 349-461",
      "ai-packages/qa-factory/scripts/run_suite.py 290-322, 470-620, 1364-1387, 2240-2425",
      "ai-packages/qa-factory/scripts/run_history.py 405-440, 600",
      "ai-packages/qa-factory/scripts/check_delivery.py 1290-1338, 1475-1499, 2029-2035",
      "ai-packages/qa-factory/scripts/ledger.py 1163-1250",
      "ai-packages/qa-factory/scripts/red_sandbox.py 1385-1450",
      "ai-packages/qa-factory/scripts/validate_artifacts.py 2501-2546",
      "ai-packages/qa-factory/references/delivery-verdict-kinds.json",
      "ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json (grep)"
    ],
    "reruns": [
      {"command": "python -B <worktree>/ai-packages/qa-factory/scripts/tests/test_s7_pretriage.py", "result": "479/479 ok, exit 0"},
      {"command": "python -B <worktree>/ai-packages/qa-factory/scripts/tests/test_triage_identity.py", "result": "Ran 32 tests OK"},
      {"command": "narrow import-and-call of the four changed test functions (null_outcome x2, bug_records, story_run_s7)", "result": "8/0, 7/0, 30/0, 10/0 checks/failed"},
      {"command": "inline probe of decide, _reading_of, unread_readings, unread_case_reading, handoff_check.check, check_triage_v0, _instance_failed", "result": "no passing word on any input; binding refuses by name u1 with no row and with two rows, accepts one NOT_EXECUTED row"},
      {"command": "test_judgment_census c1, c3, c5 narrow call", "result": "c3 PASS, c5 PASS, c1 red on controller.py::_s5_code_only_problems, pre-existing on ad336d5c and origin/main"},
      {"command": "python -B <worktree>/ai-packages/qa-factory/scripts/role_load.py --all", "result": "qa-failure-analyst 21,659 total, 19,609 process = role-load.json rows"}
    ]
  }
}
```
