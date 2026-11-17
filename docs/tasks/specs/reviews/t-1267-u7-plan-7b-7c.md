# t-1267 - critic on plan: U7 spec r3, stream 7b (F-15 a, F-17 a) and node 7c (F-16 a)

Spec: `docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md` (header; §1.2 7b row; §2 r4 lines 231-323; §3 Walk 1 533-549;
§6 stream 7b 749-779; §10 D-10..D-13, D-16; §11 F-15..F-17; §12 names). Package root below: `ai-packages/qa-factory/`.

## Verdict

**REJECT of stream 7b as written** (failure_class: spec). The design (F-15 a: the analyst reads, code records, delivery says
`run_unread` or red) is sound and keeps P27/P21; the text is not executable to that outcome. A builder following it produces,
in the three K1 variants, a factory-owned `no` where the decision promises `after_checks`, a stuck S7 for the headline story
(all-automated, `reporter: none`), and an analyst row the reducer archives. 7 blocking findings, 8 fix-before-dispatch.
Node 7c: the K4 paragraph below is executable, with two facts it adds (coverage leg fires; the ledger plan row reads
`passed_green` under the masks 7c removes). The decision to accept or re-spec is the Lead's (rule 6).

## Blocking findings

**B1 - S7 entry for an all-automated `reporter: none` story stays refused, and widening it naively closes S7 silently.**
7b item 3 extends only rule 3 of the 7a predicate. Rule 5 (spec 262: "at least one manual target, or one observation, exists")
stays, so a story whose only targets are `unread` reads False -> `failures_to_triage` raises "S7 entry ... the S6 halt stands"
(`scripts/driver_stage_s7.py:18-20`) and delivery keeps `run_not_deliverable`. Axis 3 stays stuck. Extending rule 5 alone is
worse: `failures_to_triage` builds `reasons` only from failed totals, `manual`, `observations`, nameless and `results`
(`driver_stage_s7.py:21-46`); an `unread`-only report gives `reasons == ""` -> `stage_S7` line 75 closes S7 by code
(`s7.no_failures`), the analyst is never asked. Same hole: `handoff_check._no_failure_shown` (`handoff_check.py:1370-1383`) reads
`manual`/`unnamed_manual`/`results`/`observations` only, so a zero-row analyst triage over `unread` targets is accepted.
Fix: 7b names rule 5 ("or one `unread` target"), a reason in `failures_to_triage` ("unread results <names>"), a branch in
`_no_failure_shown`, the `told` list (`driver_stage_s7.py:121-128`), and `s7_pretriage.brief` (274-283, lists only `result`/
`manual`) and `decide`'s why text (235, "a red test is the analyst's to judge" is false for `unread`).

**B2 - ledger item 5 is unreachable when the analyst answered; the "looks passed" variant reads `failed:NOT_EXECUTED`.**
`test_state` returns from the triage-row block (`ledger.py:1171-1182`) BEFORE the env_blocked branch (1239) where item 5 is
placed. Probe on today's code (row `not_run`, analyst row `NOT_EXECUTED` on the instance): `('failed:NOT_EXECUTED', ...)`,
kinds 85 -> `not_executed_unproven` = `no`, owner factory. Binding is not the problem: `triage_row_for` (contract.py
5088-5103) binds the row through the `ask` key because the own status `not_run` is not failed. Fix: inside the row block,
before line 1182, `current_row` carries `REPORT_UNREAD_CODE` and verdict `NOT_EXECUTED` -> `REPORT_UNREAD_STATE`; every other
verdict keeps 1173-1182. With NO row, keep today's `not_executed:<NO_RUN_RESULT>` (`no`, product) - the ledger must never say
`after_checks` for a reading nobody made (FR-59).

**B3 - a fourth producer of `no` is missing from D-12: `coverage_gap` (owner factory).** An automate obligation whose
instances are `not_run` gets `execution = "inconclusive"` (`coverage_contract.py:629-638`), `verified` False, `person_debt` False;
`check_delivery.coverage_reasons` (1764-1795) emits "coverage: OB-n - current sufficient evidence incomplete", owned as
`coverage_gap` (`assess` 2648). Probe: `['coverage: OB-1 — current sufficient evidence incomplete']`. So the 7b row "reporter none,
analyst NOT_EXECUTED rows -> verdict `after_checks`" cannot hold, and `coverage_contract.py` is a 7b non-goal. This is also a
pair of the spec's own requirements in conflict (FR-18 "coverage keeps verified False" vs F-15 "`after_checks`"), unstated.
Fix: reader-side in `coverage_reasons`: skip an obligation all of whose instances carry the code AND have a bound analyst
`NOT_EXECUTED` row (the item is the ledger's `run_unread`); `verified` stays False; a `failed` execution or a missing row keeps
the gap.

**B4 - the analyst's `NOT_EXECUTED` row is refused as a factory defect by an existing check, and the role page forbids it.**
`check_delivery.not_executed_findings` (2013-2029) emits `NOT_EXECUTED_NOT_RE_DERIVED` (owner factory) for every `NOT_EXECUTED`
row that fails `_code_row_ok` (1126-1162: `source == code`, bound to a MANUAL failure, inconclusive). Every analyst row on an
`unread` target fails it. `agents/qa-failure-analyst.md:87` says "NOT_EXECUTED is code's word, for a manual check that did not
answer"; `handoffs/vocabulary.yaml:98` gives the same meaning. Item 4's new paragraph would contradict line 87 on the same
page. Fix: `not_executed_findings` skips a row bound to an `unread` failure; line 87 and the vocabulary meaning are restated.

**B5 - the reducer archives the analyst's row (D-11 recurs).** `finalize_task.refresh` keeps rows only when `has_failure`
(`finalize_task.py:727`: `results | manual | unnamed | observations`). An `unread`-only report goes to 747-749: EVERY row is
archived as "current failures repaired". `reduce` line 687 likewise writes "no product failures". F-15 (a) says "the reducer
keeps the bound row", and "the reducer" is a 7b non-goal. Fix: 687 and 727 read `unread`.

**B6 - delivery does not see an unanswered or doubly-answered `unread` target.** `triage_reasons` (`check_delivery.py:1467-1483`)
reports a missing verdict only for `result`/`manual` kinds, and `observation` at 1486. An `unread` target with no row gives no
reason. The 7b edge (spec 301-302: "at delivery `triage_gap`") is false. Two rows on one target: `bind_triage` `multiple` is
`result` only (contract.py:4820). `handoff_check` lets it through, `triage_row_for` returns None, and the ledger falls to the no-row
state. Fix: `unread` joins `result` at 1468/1473 and in `multiple`.

**B7 - owns cannot carry the change (K5).** B1-B6 need `driver_stage_s7.py`, `handoff_check.py`, `finalize_task.py`,
`check_delivery.py` (`triage_reasons`, `not_executed_findings`, `coverage_reasons`, and the `to_check` text of item 7, which
nothing in owns produces), `s7_pretriage.py` beyond the predicate, `handoffs/vocabulary.yaml`, and line 87 of the analyst page.
Two of them are explicit non-goals (the reducer, coverage_contract). A builder would have to invent the requirement.

## Fix before dispatch

- F1 producer edges (item 1): the condition `no_junitxml` and `reporter == "none"` also codes rows of a run whose summary is
  `inconclusive` (runtime/input change, `run_suite.py:2347-2367`), `broken_run` (exit != 0, 1367), `timeout`, or the node-id
  block (2336). Require `summary["execution_status"] == "not_executed"`. State the precedence over `PROJECT_TIMEOUT_CODE`:
  set it before line 541 so the timeout code wins (`s5_precheck.py:3732` reads it).
- F2 expected value: "one item per instance" (spec 321-322) contradicts `build_left_items` (2155-2208: ONE item per case).
- F3 positional (CLAUDE.md rule 11 ii): `plan_row_state` today reads such a row `skipped:inconclusive run` -> `decided_elsewhere`
  (857-859; kinds 93). The spec gives no position or invariant for the new branch. Recommend: after `error` and before the
  unknown word; the analyst's red reaches the plan row only if `failed` is derived from the bound verdict. State it.
- F4 tests (Q5 c): the producer `_case_chain` change (item 6) has no keep row. `test_traceability.py` is quarantine, and
  `test_third_verdict.py:149` maps a word, not the producer. Name rows in `test_third_verdict.py`'s story world (`G_walk`, 929-931):
  all rows coded -> `result:report_unread`; a mixed case -> `result:partial` unchanged.
- F5 reader list (item 9) is incomplete. Add `judge_results._failed_rows` (63-83), `bug_records.no_run_target` /
  `_walk_has_no_run` (1007-1053; a "looks failed" APP_BUG draft on an `unread` target meets the red-now facts),
  `bug_neighbours.py:164`, `retro_numbers.py:1419`, `contract._bound_triage_rows` / `_instance_failed` (2506, 2595),
  `report_facts.EXECUTION_OUTCOME_STATES` (2488), and `finalize_task.reduce:687`.
- F6 FR-10: the trace gap reads `result:report_unread` -> `after_checks` even when the analyst found red. The packet then lists
  the case both red (ledger) and "left with you" (trace). Either read the bound verdict in `_case_chain` or state the pair.
- F7 the axis 3 cell (item 8) is untrue until B1-B6 land. Keep it in the same commit as those fixes (D-16).
- F8 Q11: item 4 adds role-read text. Name its section `kind` and the `role-load.json` `process_ratchet_tokens` row it raises,
  or mark it craft with a reason.

## Per-key answers

**K1 - premises and the three variants.** Measured and true: the producer site (`build_run_block` 470-606; rows `not_run` / "report
row missing" 536-540; `evidence[].reporter` 585; `reason_code` field 556-557). Rows reach `current_results` whole (`finalize_task`
458/510 `dict(row, ...)`). The kinds table rows and `_lookup` longest-prefix (`delivery_verdict.py:147-156`) are as cited.
`triage_targets` 4638-4639 (D-11) is true. Measured and false or partial: "the reducer keeps the bound row" (B5); the ledger
reading (B2); "three producers" (B3, B4); "delivery `triage_gap`" (B6).
Walk, story with `reporter: none`, exit 0, S6 completed, after 7a + 7b as written:
- all-automated, any variant: S7 refuses (B1); delivery `run_not_deliverable` (`no`, factory), the same as today. The analyst never reads.
- mixed (a manual target present), "looks passed": the analyst writes `NOT_EXECUTED`. Ledger `failed:NOT_EXECUTED` ->
  `not_executed_unproven` (`no`, factory). Coverage `coverage_gap` (`no`, factory). Finding `NOT_EXECUTED_NOT_RE_DERIVED`.
  Trace `run_unread`. Verdict: `no`, owner factory.
- "looks failed": APP_BUG row -> ledger `failed:APP_BUG` (`red`, product), coverage `coverage_gap`, trace `run_unread`. Verdict
  `no`; the owner is mixed (F6).
- no row: S7's form refuses by name (`_untriaged_failures` is kind-agnostic, 1340-1346), so this is not a silent pass. If S7 is
  passed by a person's word: no `triage_gap` (B6), ledger `not_executed:report_unread` (`after_checks`), but coverage still says
  `no`. So no variant gives `pass`, and FR-58 is kept (code never touches a status). An unanswered target is held off
  `after_checks` only by the coverage mask that B3's fix removes. B3 and B6 must land together.

**K2 - readers of `triage_targets` / `triage_failures`** (Grep, case-insensitive, over the package without tests; positive control:
the same call found `finalize_task.py:683/726` and the spec-named sites). Gate B / handoff `_untriaged_failures`: survives.
`_no_failure_shown`: broken (B1). `s7_pretriage.decide`: routes `unread` to `left`, but the wrong why and `brief` (B1).
`driver_stage_s7.failures_to_triage`: broken (B1). `s7_unbound` / `s7_fresh` (325-344): survive (kind-agnostic).
`check_delivery.triage_reasons`: broken (B6). `_code_row_ok` / `not_executed_findings`: broken (B4). `_triage_binding` /
`_failure_cases`: survive. `finalize_task` 687/727: broken (B5). Ledger / `triage_row_for`: binds, but the state is wrong (B2).
`traceability.triage_for` and the dashboard (`factory_dashboard.py:912-939`): survive (they display). The others: F5.
Narrowing: tight against a DECLARED reporter. `reporter_choice` returns a declared `run.reporter` before any table
(`run_suite.py:304-306`). A `junit-xml`/`trx` with its file missing keeps its reporter word, so no code and an honest `no`.
An inferred format that read zero tests has a `source`, so no `no_junitxml`. Loose against inconclusive / broken / timeout runs (F1).

**K3 - class walk** (producers of `no`, and sites deciding `not_executed`, for an automated test with no readable report):
1 `check_delivery.run_reasons`: applied (7a), but rule 5 is not (B1).
2 `ledger.test_state` 1172-1182 / 1245: misapplied (B2).
3 `ledger.plan_row_state` 857-859: `decided_elsewhere`, not a `no`; changed by item 5 with no position (F3).
4 `check_traceability._case_chain` 92: applied (item 6); no producer test (F4).
5 `coverage_contract.coverage_projection` 629-638 -> `coverage_reasons`: MISSED (B3).
6 `not_executed_findings` / `_code_row_ok`: MISSED (B4).
7 `triage_reasons`: MISSED (B6).
8 `driver_stage_s7.failures_to_triage` / `handoff_check._no_failure_shown`: MISSED (B1).
9 `finalize_task.refresh` 727 / `reduce` 687: MISSED (B5).
10 `run_suite.execution_status` 1354-1377 (summary `not_executed` / `broken_run`): n/a to change; it bounds item 1 (F1).
11 `finalize_task.reduce` 629-637 (`execution_status`): n/a, never rewritten (invariant kept).
12 `judge_results._failed_rows`: n/a (only red rows are sorted), but the item 9 walk is owed (F5).
13 `s5_precheck.py:3732` (reads `reason_code` = timeout): n/a once F1 states the precedence.

**K4 - node 7c (F-16 a), executable text for the Lead.** Facts measured (probes in the trail):
(i) gap `result:none` for an unprepared walk, `not_in_manifest` for a case nobody walked, `result:not_run` for automated;
(ii) the coverage leg DOES fire: `coverage: OB-1 — not checked by hand: unprepared - no stand` -> `coverage_gap`, from
`coverage_contract.py:663-705` (`execution` `not_run`, gap rewritten at 704-705);
(iii) `ledger.plan_row_state` reads **`passed_green`** for a plan row whose only case is an unprepared walk (word `""`,
`run_results` 4486-4488 -> `rollup_status([""]) == ""`, which is not None, so it falls to 918). Today it is masked by the trace and
coverage `no`s that 7c removes;
(iv) a stale walk keeps `unprepared` with `current_reason` set and no result (`finalize_task.py:556-562`), and
`manual_evidence.unprepared_rows` (1251-1269) does not filter it.
Node 7c, after 7b (shared files):
1. `scripts/manual_evidence.py`: one predicate `current_unprepared(report) -> {case: [obligation ids]}`, the AR-13 reader. Its
   cases are those whose every current manual row has `unprepared` not None, no `result`, no `current_reason`, and (default
   toward `no`, a Lead fork) `walked` is not False. `unprepared_rows` stays.
2. `scripts/check_traceability.py::_case_chain`, in the branch at 87-92: when `result == ""` and the case is in
   `current_unprepared` and no `current_results` row names it (`C.names_case`), return gap `unresolved:unprepared_walk`. Every other
   `""`, a stale or not-walked walk, and `None` keep their gap (error direction: toward `no`).
3. `references/delivery-verdict-kinds.json`: `trace_gaps["unresolved:unprepared_walk"] = "unprepared_walk"` (an exact key that
   wins over the `unresolved` prefix), and a note sentence.
4. `scripts/check_delivery.py::coverage_reasons` + its call in `assess` (2648): skip an obligation whose id is in the predicate's
   obligation set and whose `execution_state` is not `failed`. `verified` stays False (Fork 13 A's coverage half kept). The item
   is `unprepared_records`' one per case.
5. `scripts/ledger.py::plan_row_state`: a case word `""` never reaches `passed_green`. In `current_unprepared` it reads
   `not_executed:unprepared_walk` (kinds `ledger_states` -> `unprepared_walk`). Otherwise it reads `not_executed:no result recorded
   for this row's cases`. Position: after the unknown-word branch (847-850), before unconfirmed (851). Invariant: no failure, flaky,
   partial or error word is hidden, and `passed_green` stays unreachable for a case with no result.
6. Tests, keep files. `test_third_verdict.py`: a table row (`unresolved:unprepared_walk` -> `unprepared_walk` -> `after_checks`),
   and story rows via `G_walk`: walked -> the new gap; stale -> `result:none`; `walked: False` -> `result:none`; no record ->
   unchanged; plus an automated row of the same case -> unchanged. `test_check_delivery.py`: assess on an all-manual story, one
   unprepared walk, S6 completed -> `after_checks`, kinds without `chain_broken` / `coverage_gap`; the stale twin -> `no`.
   `test_ledger.py`: the probe input -> not `passed_green`.
7. The docstring of `unprepared_records` (1889-1890) is restated: the requirement yields its own `chain_broken` for this case only.
`architecture: AR-22, AR-27, AR-28`.

**K5 - executability of 7b.** Per item: 1 (file, function and behaviour named; edges F1; row: `test_s7_pretriage.py` built
from a summary, acceptable); 2 (named; kind split needs care: `triage_failures` 4727-4736 turns every `names` entry into kind
`result`, so `unread` must not enter `names` through that loop); 3 (rule 5 missing, B1); 4 (contradicts line 87, B4); 5 (misplaced, B2,
F3); 6 (no producer row, F4); 7 (`to_check` producer outside owns, B7); 8 (untrue as written, F7); 9 (incomplete list, F5).
Order against 7a (same predicate and test files) and 5a (`run_suite.py`, disjoint function) is stated and sufficient.

**K6.** AR-1 kept (kinds rows; `"none"` is a word of `REPORTERS`, 230). AR-22 broken: the `unread` set has starved readers
(B1, B5, B6); blocks. AR-27 broken: owner factory `no` instead of `run_unread` / red (B2, B3, B4). AR-28 / FR-59 kept by accident
(the coverage mask); at risk once B3 alone is fixed (K1). AR-29 / P27 kept: the analyst judges, code checks shape only, and
`_code_row_ok` must stop judging an analyst row's provenance as a defect (B4). P21 kept in intent. FR-18 kept (`verified` False)
but in conflict with F-15, unstated (B3). FR-35 broken: the analyst's "not executed, looks passed" is reported as "factory:
... never shown as 'the person will check'" (B4).

Q4 class: siblings outside 7b's owns are listed under B7 with their files, for the Lead to widen the round. Q6 duplication:
none found. The 7c predicate is proposed as the single reader beside `unprepared_rows` (grep `get("unprepared")` over the
scripts, 20 hits read). Q12 one road: none found. The narrowing to reporter `none` is a data condition, not a language exclusion
(grep of the spec's 7b text for language/runner names: none). VARIETY: a `reporter: none` project (any non-JUnit runner) today
stops at S7. After 7b as written it still stops (B1). After the fixes the factory passes S7 with the role's reading. No silent
default.

## Trail

Read: spec r3 lines 30-56, 225-324, 530-552, 745-779, 870-940; brief and t-1252 review (given, headers).
`run_suite.py` 290-369, 466-606, 1354-1377, 2225-2394. `ledger.py` 30-66, 679-918, 976-1024, 1085-1125, 1163-1245.
`contract.py` 4411-4513, 4595-4821, 5063-5104, 2500-2617. `check_traceability.py` 1-160. `check_delivery.py` 100-124, 1126-1162,
1282-1511, 1764-1906, 2005-2030, 2155-2214, 2594-2650, 2736-2739. `finalize_task.py` 538-573, 620-749. `handoff_check.py` 1320-1383.
`driver_stage_s7.py` 1-130, 320-359. `s7_pretriage.py` 1-60, 200-324. `coverage_contract.py` 600-709. `judge_results.py` 62-91.
`bug_records.py` 1005-1064. `traceability.py` 612-633. `factory_dashboard.py` 900-939. `delivery_verdict.py` 135-164.
`delivery-verdict-kinds.json` whole. `qa-failure-analyst.md` 70-95. `architecture.md` 49, 72. `test-layers.json` (layers of the
named test files). `test_third_verdict.py` 145-151, 920-931.
Greps (case-insensitive; positive control = a known hit in the same call): `triage_failures|triage_targets|bind_triage`
(package, no tests; hits listed in K2); `NOT_EXECUTED` (package, no tests); `reason_code` / `PROJECT_TIMEOUT_CODE` (scripts);
`get("unprepared")` (scripts). The spec-named grep for `triageable_not_executed|REPORT_UNREAD`: 0 hits in this tree (7a/7b not
merged), with its positive control `report_unreadable` found.
Probes (pure functions on in-memory dicts, nothing written):
- `L.test_state` with a `not_run` row + analyst `NOT_EXECUTED` row -> `('failed:NOT_EXECUTED', 't.sh::one')`; no row ->
  `('not_executed:no result for this test in run-report.json', ...)`.
- `L.plan_row_state` on a plan row with one unprepared walk -> `run_results {'TC-001': ''}`, `('passed_green', 'TC-001')`.
- `T.gap_of_case`: unprepared -> `'result:none'`; automated `not_run` -> `'result:not_run'`; unwalked -> `'not_in_manifest'`.
- `D.coverage_reasons`: unprepared obligation -> `['coverage: OB-1 — not checked by hand: unprepared - no stand']`; automated
  inconclusive -> `['coverage: OB-1 — current sufficient evidence incomplete']`.

```json
{
  "verdict": "blocker",
  "blockers": [
    "B1 S7 entry: predicate rule 5 unextended, so an all-automated reporter-none story stays refused; widening it alone closes S7 by code because driver_stage_s7.failures_to_triage and handoff_check._no_failure_shown ignore unread",
    "B2 ledger item 5 sits after ledger.py:1182 and is unreachable when the analyst answered: probe gives failed:NOT_EXECUTED, which maps to not_executed_unproven, no, owner factory",
    "B3 fourth producer missed: coverage_contract execution inconclusive goes through check_delivery.coverage_reasons to coverage_gap, no, owner factory (probe); coverage_contract is a 7b non-goal; FR-18 vs F-15 conflict unstated",
    "B4 check_delivery.not_executed_findings and _code_row_ok flag every analyst NOT_EXECUTED row as NOT_EXECUTED_NOT_RE_DERIVED; qa-failure-analyst.md:87 and vocabulary.yaml:98 say NOT_EXECUTED is code's word",
    "B5 finalize_task.refresh has_failure (727) and reduce (687) ignore unread, so an unread-only report archives every analyst row; the reducer is a 7b non-goal",
    "B6 check_delivery.triage_reasons and bind_triage multiple are result/manual-only, so the edge 'no analyst row gives triage_gap' is false",
    "B7 owns cannot carry B1-B6 nor the to_check producer of item 7; two of the needed files are explicit non-goals"
  ],
  "fixes": [
    "F1 build_run_block: require summary execution_status not_executed; timeout code wins (set before run_suite.py:541)",
    "F2 one item per case, not per instance (build_left_items)",
    "F3 plan_row_state position and invariant for the new branch",
    "F4 producer rows for _case_chain in test_third_verdict.py story world (G_walk)",
    "F5 complete the item 9 reader list (judge_results, bug_records, bug_neighbours, retro_numbers, contract helpers, report_facts, reduce:687)",
    "F6 trace gap vs analyst red: read the verdict or state the pair (FR-10)",
    "F7 axis 3 cell lands with B1-B6",
    "F8 name the analyst-page section kind and the process ratchet row"
  ],
  "class_completeness": "K3 enumerates 13 producers and sites: 5 missed by the spec (coverage_gap, not_executed_findings, triage_reasons, S7 entry and form, reducer keep), 2 misapplied (ledger test_state, plan_row_state position). Their files are named under B7 so the Lead can widen the round. 7c adds the masked passed_green of an unprepared-only plan row (ledger.plan_row_state) and the coverage leg, both measured.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md",
      "ai-packages/qa-factory/scripts/run_suite.py",
      "ai-packages/qa-factory/scripts/ledger.py",
      "ai-packages/qa-factory/scripts/contract.py",
      "ai-packages/qa-factory/scripts/check_traceability.py",
      "ai-packages/qa-factory/scripts/check_delivery.py",
      "ai-packages/qa-factory/scripts/finalize_task.py",
      "ai-packages/qa-factory/scripts/handoff_check.py",
      "ai-packages/qa-factory/scripts/driver_stage_s7.py",
      "ai-packages/qa-factory/scripts/s7_pretriage.py",
      "ai-packages/qa-factory/scripts/coverage_contract.py",
      "ai-packages/qa-factory/scripts/delivery_verdict.py",
      "ai-packages/qa-factory/references/delivery-verdict-kinds.json",
      "ai-packages/qa-factory/agents/qa-failure-analyst.md",
      "ai-packages/qa-factory/design/architecture.md",
      "ai-packages/qa-factory/scripts/tests/test-layers.json",
      "ai-packages/qa-factory/scripts/tests/test_third_verdict.py"
    ],
    "reruns": [
      {"command": "python -B -c probe ledger.test_state not_run row + analyst NOT_EXECUTED row", "result": "('failed:NOT_EXECUTED', 't.sh::one'); no row: ('not_executed:no result for this test in run-report.json', 't.sh::one')"},
      {"command": "python -B -c probe ledger.plan_row_state unprepared-only plan row", "result": "run_results {'TC-001': ''}; ('passed_green', 'TC-001')"},
      {"command": "python -B -c probe check_traceability.gap_of_case", "result": "unprepared 'result:none'; automated not_run 'result:not_run'; unwalked 'not_in_manifest'"},
      {"command": "python -B -c probe check_delivery.coverage_reasons", "result": "unprepared: coverage: OB-1 - not checked by hand: unprepared - no stand; automated inconclusive: coverage: OB-1 - current sufficient evidence incomplete"}
    ]
  }
}
```
