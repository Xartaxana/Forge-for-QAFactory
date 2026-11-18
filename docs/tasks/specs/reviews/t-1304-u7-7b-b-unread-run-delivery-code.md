# t-1304 - code review of node 7b-B (U7, builder t-1302): an unread run reaches delivery

Subject: commit 060648cd on branch `worktree-u7-7b-b` (merge base 6be36343; origin/main is now 9401f019, 19 commits ahead, none of them touches `ledger.py`, `check_delivery.py`, `check_traceability.py`, `contract.py` or `delivery-verdict-kinds.json`, so the merge does not conflict in these files). Spec: `docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r4-7b-7c-e7.md`, section 2 Group D, section 3, amendments N2, N6, N7, N8 and N11.

Terms used below. An "unread row" is a current result row that the run code coded `status: not_run, reason_code: report_unread` (the run exited 0 and its reporter wrote nothing code could read; `contract.is_unread_row`). A "reading" is the verdict the failure analyst wrote for such a row in `triage.json`. `contract._reading_of` turns the readings of several rows into one word: `red` (any verdict other than NOT_EXECUTED), `unanswered` (some row has no verdict), `read` (every verdict is NOT_EXECUTED). "after_checks" is the third delivery verdict: ready once the person finishes the listed checks.

## Verdict

**ACCEPT WITH FIXES (NEEDS WORK, 0 blocking findings, 3 to fix before merge, 4 notes).** The code does what the spec says. I re-ran all four section-3 walks through `check_delivery.assess`, walk 2 among them, and then ran the same walks on a story whose plan has a real coverage obligation. That second story is the case the committed test cannot reach. Every unread reading that is not `read` keeps a `no`, and nothing unread reads green. The fixes: the coverage excuse has no committed test row (F1); an obligation with no id is excused instead of failing (F2); the 7b-A changelog fragment is now false (F3). Whether to accept is the Lead's decision.

## Keys

**K1 holds.** In `ledger.py::plan_row_state` the new `read` branch (lines 868-870) sits immediately before `skipped` (871) and after the unconfirmed-expectation branch (861-863), as N6 requires. The `red` reading joins `failed` at line 826, which is the first result branch. Position invariant: every failure, placeholder, flaky, partial, error, unknown-word and unconfirmed state above it still wins, and a red reading still gives `failed:<verdict>`. Is anything refused before now reachable as not-red? No. The branch fires only when at least one case has the word `not_run`, and that case made the old `skipped` branch return at line 872. So the new branch replaces exactly one old return, `skipped:inconclusive run` (kind `decided_elsewhere`, no verdict), with `not_executed:report_unread` (`after_checks`). That is stricter. The branches below `skipped` (manual hand-off, green-open, deferred, behind-a-red, Then hand-off, sides, `passed_green`) were unreachable for such a row before and still are. The table rows "one read APP_BUG", "partial beside", "unanswered keeps skipped" and "N6: read + an unconfirmed Then" in `test_ledger.py::an_unread_run_reads_as_checks_left_never_green` pin the order. All of them pass (the DoD run is in the trail).

**K2 holds.** In `ledger.py::test_state` (1192-1196), an unread row answered NOT_EXECUTED reads `not_executed:report_unread`. An unread row answered FLAKY reads `not_verified_flaky`, with `fix_result: fixed` (the N11 row) or without it (old branch). A read row answered FLAKY and fixed still reads `passed_green` (control row). ENV_ISSUE and every other verdict keep `env_blocked:*` and `failed:*`. An unread row with no analyst row falls through to `not_executed:no result for this test in run-report.json`. No branch reads green for an unread row.

**K3 holds, with one hole (F2).** I called `unread_obligations` and `coverage_reasons` with these inputs: doc `{}` or `None`; facts `{}` or `None`; `instance_ids` empty or `None`; another gap text; oracle open or `None`; design unknown; execution failed; one instance unanswered; two rows for one instance; an id that is not an unread row; triage not a list. Every one gives `excused=[] red=[]` and the old reason, byte for byte (trail, `k3.py`). A gap with a trailing space is excused because the guard strips it, which is harmless. A report with only legacy `results[]` IS excused (`unread_readings` falls back to `results[]`), but the delivery verdict stays `no` (K8). Hole: an obligation whose `obligation_id` is `None` and whose readings are all NOT_EXECUTED is excused (F2).

**K4 holds.**
- N2: the plan-row entry "red on `api/TC-4`, read on `web/TC-4`" gives the web row `not_executed:report_unread`. It passes.
- N7: `unread_obligations` calls `C._reading_of` and adds only the three coverage guards. There is no second wording of the rule.
- N8: `_run_unread_to_check` uses `C.bind_triage(C.triage_failures(facts["report"])[0], facts["triage"])["matched"]` over keys of kind `unread`, mapped to cases by `_failure_cases`. There is no new matcher. The item text names `run.reporter` and `run.report_path`, and `run_suite.py:332` reads `run.report_path`.

**K5 holds.** I ran walk 2 myself. The `after-checks` fixture already holds a manual case: TC-002 is manual-agent, inconclusive, with a code-written NOT_EXECUTED row. It also holds TC-005, handed to the person. So the builder's walk 1 is walk 2. Output: verdict `after_checks`; items TC-001 `run_unread`, TC-002 `not_executed_code`, TC-004 `manual_human`, TC-005 `handed`; no reasons; no findings. The committed test only looks at the TC-001 item, so walk 2's manual half is checked by the verdict alone. I also re-ran walks 1, 3 and 4 on a story with one schema-2 coverage obligation bound to the unread instance (`cov_walk.py`):
- walk 1: `after_checks`, no reasons; the obligation is `inconclusive`, `sufficient`, oracle closed, with gap `current sufficient evidence incomplete`.
- walk 3: `no`, with reasons `failed:APP_BUG` (plan row and test) and `coverage red: O-TC1 - the failure analyst read a failure in the run log`.
- walk 4: `no`, with reasons `traceability`, `ledger` and `triage`, plus the coverage reason.
- the same read story plus a `remaining_gap`: `no`, and the coverage reason stays.

**K6 holds.** The new branch in `_case_chain` is guarded by `triage_rows is not None`. A case-insensitive search for `gap_of_case(|outcome_for_case(|_case_chain(` over the package finds one production caller, `walk` (check_traceability.py:258), which passes the rows. The other hits are the test callers: `test_traceability.py` 482, 531-532, 1021-1027 and `test_case_key_identity_join.py` 43, 74, 383. These pass nothing and keep today's path. I re-ran `test_traceability::typed_gap_words` and `a_case_taken_by_hand_has_an_outcome` (64 PASS) and `test_case_key_identity_join::k_b2_run_results_lookup` (8 PASS). No failures.

**K7 holds: it is the safe direction.** If one skipped-class sibling of the row is unanswered or really skipped, the plan row keeps `skipped:inconclusive run`. The read case still gets its item from two other readers: its own test row (`test_state` gives `run_unread`) and the trace (`result:report_unread`). An unanswered sibling brings its own `no`: a test-row `not_executed:no result...` plus a `triage:` reason. I found no road where the person gets neither an item nor a reason. A case with an unread row but no manifest test entry reads `not_in_manifest` in the trace, which is `no`.

**K8: no regression; the old `no` stays.** For a report that carries the coded row only in legacy `results[]`, the readers split. With the analyst's NOT_EXECUTED, `test_state` and coverage read the case as answered: there is a TC-001 `run_unread` item and no coverage reason. The trace (`unread_case_reading` reads `current_results` only) reports `run result 'not_run' is not terminal`, so the verdict is `no`. With no analyst row: `no`, with the trace, ledger and triage reasons. Before 7b-B, the same input read `failed:NOT_EXECUTED`, which is `no` too. So the verdict does not change, but in that shape the `no` now rests on the trace alone (F6). This is an estimate, not verified: the producer (`run_suite.py:550`, `build_run_block`) writes run blocks that feed `current_results`, so a coded row only in legacy `results[]` would come from a hand-made report.

**K9: the missing row is load-bearing (F1).** The `after-checks` fixture has 0 coverage obligations (`coverage.status = legacy_assessment_not_available`, checked in the trail). So the committed walk table never reaches `unread_obligations`, the `excused` skip or the `red` reason. Two defects would pass every committed test: deleting the excuse (every real reporter-`none` story reads `no`) and dropping the gap or oracle guard (a coverage gap is hidden). The cheapest committed entry follows the precedent at `test_check_delivery.py:920-925`. In the existing walk test, write a schema-2 `test-plan.json` with one `automate` obligation and add one `obligation_bindings` row (`instance_ids: [name]`, `design_assessment: sufficient`, `obligation_hash: coverage_contract.content_hash(ob)`). Then assert, per row, that no reason names the obligation (the read row) or that `coverage red: O-TC1` is present (the APP_BUG row). That is about 8 lines, and tests then stay under the code lines (about 119 against 125). `cov_walk.py` in the trail proves the fixture shape works.

**K10: the 7b-A fragment is false (F3).** No other contradiction found. `design/architecture.md` axis 3 now carries the D7 text. `agents/qa-failure-analyst.md:87` and the kinds note agree with the code. I searched the package for `delivery side`, `until 7b-B`, `7b-B not merged` and `not verified until`. The only hits are the fragment itself and an unrelated `stale_ledger_inputs` sentence. `report-risk-words.json` has no `row_states` entry for the new state, so the summary prints the prefix word "not run" (F7, a note).

## Findings

**F1 - fix before merge.** No committed row covers the coverage excuse, which is the exact code K3 judges. Reproduction: `walk2.py` prints `obligations: 0 legacy_assessment_not_available` for the builder's fixture. Smallest fix: the entry described under K9, in `test_check_delivery.py::a_run_whose_results_code_could_not_read_reaches_delivery_by_the_analysts_word`.

**F2 - fix before merge.** At `check_delivery.py:1784-1800` (`unread_obligations`), `excused.add(ob["obligation_id"])` accepts `None`, and `coverage_reasons` then skips that obligation silently. Before this change the same obligation made `coverage_reasons` raise `TypeError` at line 1843, which fails closed. Reproduction (`k3.py`): `unread_obligations(doc(ob(obligation_id=None)), good)` gives `(frozenset({None}), frozenset())`, and `coverage_reasons` gives `[]`; the old path raises TypeError. Reaching it needs a malformed plan, so realism is low. Smallest fix: `oid = ob.get("obligation_id"); if not isinstance(oid, str) or not oid: continue` at the top of the loop.

**F3 - fix before merge (outside the builder's owns, so the Lead's to place).** `changelog.d/universality-1-unread-target-reaches-the-analyst.md` ends with "delivery still reads such an answered target as not verified until the delivery side of the change lands". That text ships in the release and is false once 7b-B merges. Smallest fix: delete the clause at merge, or widen this node's owns by that one file.

**F4 - note.** `UNREAD_GAP` (check_delivery.py:1780) is a second copy of the producer's literal at `coverage_contract.py:701`, and that file is a non-goal of this node. If the producer's text drifts, the excuse silently stops working. That fails toward the gap, which is safe, and no test pins the two copies together. Proposed node for the Lead to open: `UNREAD_GAP literal twin of coverage_contract.py:701 -- export one constant from coverage_contract and read it in check_delivery | node: to be opened by the Lead (7c reuses the same guard family, N9)`.

**F5 - note, spec-level (question 1).** D3 says "any other verdict gives red", so FLAKY or ENV_ISSUE on an unread instance prints `coverage red: O-TC1 - the failure analyst read a failure in the run log` with owner product. Reproduction (`env.py`): for ENV_ISSUE, `blocked_by` is `['product', 'environment', 'factory']`, while the ledger rows say environment. The verdict `no` is correct. The product owner and the word "failure" are untrue for ENV_ISSUE. The same over-attribution already exists for a real red run (RD1-21 routes every `coverage red:` to product), so this is a sibling of an old class, not a new one.

**F6 - note.** The K8 split: `unread_readings` and `test_state` fall back to legacy `results[]`, but `unread_case_reading` does not. Reproduction: `walk2.py` "LEGACY results[] only" gives a TC-001 `run_unread` item beside the verdict `no`, with only the trace reason. The direction is safe. It is worth one line if 7b-A's helpers are ever touched again.

**F7 - note (question 2).** In the delivery summary, `not_executed:report_unread` reads "not run" (prefix `not_executed`, `report-risk-words.json` row_prefixes). Meanwhile the item says the analyst read "the log reads as passed". The spec's F5 addendum covered `report_facts` only.

## Spot-checks and standing questions

- Q1 spec fit: D1-D7 implemented as written. D2's location was replaced by N6's, as the ACCEPTED block says.
- Q2: K7 is safe.
- Q3 seams: additive only; the `triage_rows` keyword defaults to None.
- Q4 class completeness: every site of t-1267 K3 items 2-7 is reached (ledger test and plan row, trace, coverage, triage multiple, finding, item). The 7c twins are out of scope.
- Q5 tests: (a) the ledger, plan-row and trace tables kill the position and red-softening defects; coverage is not covered (F1). (b) Expected values trace to the D4 table, walks 1/3/4 and N2/N6/N11. (c) Coverage has no row (F1). (d) No test was rewritten. (e) No duplicates. (f) Budget: 111 test lines against 125 code lines.
- Q6 duplication: F4. The three `bind_triage(triage_failures(...))` calls are the road N8 and B4 prescribe.
- Q7 code quality: the new functions are under 30 lines with at most 3 nesting levels; no dead branches.
- Q8 hygiene: 0 Cyrillic and 0 CR characters in the added lines. Positive control: the same `grep -cP` finds 15 lines in CLAUDE.md.
- Q9: no ratchet file is changed.
- Q10: the commit names AR-27, AR-28, AR-1 and AR-13. VARIETY: the change keys on `reason_code`, never on a runner name, so any stack with reporter `none` gets the same road.
- Q11: no judgment moves into code; code joins a closed code to the analyst's verdict.
- Q12 one road: none found. The added lines contain no language or runner names.
- The `forge-check` pipeline was not read; it is not reachable from this session, so the coordinator holds it.

## Questions for the architect

1. F5: should `unread_obligations` put only failure verdicts in `red` (APP_BUG, APP_CHANGED, TEST_BUG) and leave ENV_ISSUE and FLAKY to their own ledger owners, with the coverage reason kept as `coverage:`? Or is the RD1-21 rule "every coverage red is the product's" meant to cover these too?
2. F7: should `report-risk-words.json` get a `row_states` row for `not_executed:report_unread`, for example "its results could not be read; left with you to check against the run log"? That would belong to 7c or a follow-up, since the file is not in 7b-B's owns.

## Trail

Read: the spec sections (lines 37-106 and 184-351); the whole diff (9 files); `contract.py` 4597-4612 and 4855-4906; `ledger.py` 682-930 and 1019-1038, 1099-1260; `coverage_contract.py` 595-705; `check_delivery.py` 920-967 (precedent); `run_suite.py` 331-332; `t-1293` lines for 7b-B.
Commands (scripts in `C:/Users/i_mas/AppData/Local/Temp/claude/b3e3188b390a00d9/1d2edd69-11a3-4cc2-8484-fbd7325289b0/scratchpad/`):
- `python -B .../tests/test_ledger.py`: `=== test_ledger: 464/464 ok ===`
- `run_fns.py test_check_delivery a_run_whose_results_code_could_not_read_reaches_delivery_by_the_analysts_word`: 18 PASS, 0 FAIL
- `run_fns.py test_third_verdict k_u7_7b_b_the_trace_reads_the_bound_verdict_of_an_unread_case`: 4 PASS
- `run_fns.py test_third_verdict k_n8_1_every_row_of_the_table`: 347 PASS, including L23 and T6 `report_unread` to `run_unread` / `after_checks`
- `run_fns.py test_traceability typed_gap_words a_case_taken_by_hand_has_an_outcome`: 64 PASS; `test_case_key_identity_join k_b2_run_results_lookup`: 8 PASS
- `walk2.py` (walk 2 and the legacy shapes), `k3.py` (21 error-direction inputs), `cov_walk.py` (walks 1/3/4 with a coverage obligation), `env.py` (ENV_ISSUE and FLAKY): outputs quoted above.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "t-1267 K3 items 2-7 all reached (ledger test_state and plan_row_state, trace _case_chain, coverage unread_obligations/coverage_reasons, triage_reasons multiple, not_executed_findings, build_left_items). Residual: UNREAD_GAP twin of coverage_contract.py:701 proposed as a node for the Lead (F4); 7c twins out of scope.",
  "fixes": [
    "F1 test_check_delivery.py walk test: add one schema-2 coverage obligation plus obligation_bindings row so the excused and coverage red paths have a committed row (fix before merge)",
    "F2 check_delivery.py unread_obligations: skip an obligation whose obligation_id is not a non-empty str (fix before merge)",
    "F3 changelog.d/universality-1-unread-target-reaches-the-analyst.md: drop the clause 'delivery still reads such an answered target as not verified until the delivery side of the change lands' (fix before merge, Lead places it: outside owns)"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r4-7b-7c-e7.md",
      "git diff origin/main...HEAD in .claude/worktrees/u7-7b-b",
      "ai-packages/qa-factory/scripts/ledger.py",
      "ai-packages/qa-factory/scripts/contract.py",
      "ai-packages/qa-factory/scripts/coverage_contract.py",
      "ai-packages/qa-factory/scripts/check_delivery.py",
      "ai-packages/qa-factory/scripts/check_traceability.py",
      "ai-packages/qa-factory/references/report-risk-words.json",
      "docs/tasks/specs/reviews/t-1293-u7-7b-a-unread-target-code.md"
    ],
    "reruns": [
      {"command": "python -B ai-packages/qa-factory/scripts/tests/test_ledger.py", "result": "464/464 ok"},
      {"command": "import-and-call test_check_delivery a_run_whose_results_code_could_not_read_reaches_delivery_by_the_analysts_word", "result": "18 PASS 0 FAIL"},
      {"command": "import-and-call test_third_verdict k_u7_7b_b_the_trace_reads_the_bound_verdict_of_an_unread_case and k_n8_1_every_row_of_the_table", "result": "4 PASS; 347 PASS"},
      {"command": "import-and-call test_traceability typed_gap_words, a_case_taken_by_hand_has_an_outcome; test_case_key_identity_join k_b2_run_results_lookup", "result": "64 PASS; 8 PASS"},
      {"command": "scratch walk2.py, k3.py, cov_walk.py, env.py", "result": "walk 2 after_checks; coverage walks 1/3/4 as spec; None obligation_id excused (F2); ENV_ISSUE coverage red owner product (F5)"}
    ]
  }
}
```
