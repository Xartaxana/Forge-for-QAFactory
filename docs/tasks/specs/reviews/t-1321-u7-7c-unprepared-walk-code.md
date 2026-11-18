# t-1321 - code review of node 7c (U7, builder t-1316): a walked unprepared manual check reaches delivery

Subject: commit 8fe69697 on branch `worktree-u7-7c`, merge base 0598c297. origin/main is now 5bace71d, 15 commits ahead. None of those commits touches a file of this diff, so the merge does not conflict. Spec: `docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r4-7b-7c-e7.md`, section 5 plus amendments N6, N9 and N10. The dispatch added the F7 rows.

Terms used below:
- An **unprepared walk** is a `current_manual_checks` row that carries the marker `unprepared` and no `result`. The factory could not prepare the case, and the runner walked it by hand.
- **Walked** means the marker does not say `walked: False`.
- A **blank case** is a case whose run word in `contract.run_results` is `""` (no result at all).
- `after_checks` is the third delivery verdict: ready once the person finishes the listed checks.
- A **plan row** is a `TS-n` row of the ledger.
- The **base** is the origin/main package, extracted to a scratch folder and run with the same scripts.

## Verdict

**REJECT (NEEDS WORK; failure_class: code. 1 blocking finding, 5 to fix before merge, 4 notes).** The fix is local, so this is a fix round, not a redo. All four of the builder's walks reproduce. What blocks: the new blank branch in `ledger.plan_row_state` returns before the `deferred_by_decision` branch. On a plan row that holds one walked unprepared case and a sibling whose Then a decision deferred with no recorded word, the verdict turns from `no` into `after_checks`, and the deferral is never named to the person (F1). The twin `read` branch of 7b-B has the same hole, in the same function, which is inside this node's owns. Whether to accept is the Lead's decision.

## Keys

**K1 holds, with two notes.** I called `current_unprepared` directly (`k1.py`):
- Mixed rows of one case give `{}`: walked + not walked, walked + stale, walked + a `fail` row.
- A row with `result: inconclusive` is out. `result: ""` is in.
- `None`, `{}`, a list, `current_manual_checks: None`, and non-dict rows never raise and never include a case.
- `walked` absent counts as walked. `write_unprepared` (manual_evidence.py:1566-1586) always writes a bool, so an absent flag comes only from a record written before t-1955 N3, or from a hand-made one. The spec's words "walked not False" allow this reading (F9).
- `walked: 0` and `walked: "false"` also count as walked.
- One row whose obligation ids are an int makes the whole function return `{}`, which drops every walk. That is the safe direction (F10).

**K2 holds, with one hole (F3).** In `_walked_unprepared` and `_case_chain` (`k2.py`, plus the committed table, which I re-ran):
- walked gives `unresolved:unprepared_walk`; stale and not walked give `result:none`.
- An automated `passed` row of the same case wins. It wins before the new branch is reached, because `rollup_status` drops `""`.
- The "no automated row" guard decides only when the automated row has a blank status, and then the gap is `result:none`.
- `report` None returns False.
- The only production caller is `walk` (check_traceability.py:277). The test callers (`test_traceability.py`, `test_case_key_identity_join.py`) carry no unprepared row: `grep -ci unprepared` gives 0 and 0, with a positive control of 17 in `test_check_delivery.py`. Their behaviour is unchanged.
- The hole: the plan case is a bare `TC-9`, a walked row is `web/TC-9`, and a not-walked row is `api/TC-9`. The gap is `unresolved:unprepared_walk`, so the not-walked row is hidden.

**K3 (a) holds by N6's list; (b) fails (F1, F2); (c) holds.**
- (a) The branch sits after the unconfirmed-expectation branch and before `read`, which sits before `skipped`. With a walked case beside it, partial, error and an unknown word all still win (`k3.py`). The table row "failed sibling wins" passes.
- (b) Walked TC-002 plus an unread sibling with no analyst answer: plan row `not_executed:unprepared_walk`, trace `result:not_run` for the sibling, verdict `no` (trace, ledger test row and triage reasons).
- (b) Walked plus a skipped automated sibling: plan row `unprepared_walk`, trace `result:skipped`, verdict `no`. This holds even when the sibling's requirement is also covered by a passed case (walk A).
- (b) Walked plus a manual inconclusive sibling with no triage: `no`.
- So skipped and unread siblings never reach `after_checks`. But the branch also returns before every state BELOW `skipped`. One of them, `deferred_by_decision` (kind `deferred_undecided`), says `no`. Walks D1 and D2 give `after_checks` where the base gives `no` (F1). In every one of these walks the sibling is also listed as an `unprepared_walk` item (F2).
- (c) `passed_green` cannot be reached for a blank case. Every blank case returns at the new branch. Probes: a blank manual row with no marker, a `result: None` row, an automated row with status `""` beside a passed sibling. All three give `not_executed:no result...` (the base gave `passed_green`). A case with NO row at all beside a passed sibling still reads `passed_green`, in the base and on the branch. That is outside item 5, but the changelog claims otherwise (F5).

**K4 holds, with one hole (F4).** I called `unprepared_obligations` and `coverage_reasons` directly (`k4.py`):
- These give no excuse and keep the coverage reason (a few of them make `coverage_reasons` raise, which fails closed as before): an id that is `None`, `""` or an int; execution `failed` or absent; oracle open or absent; another gap text; a gap with a leading space; a second case that is not walked, stale, or has a real row; an obligation with no manual row; report `None` or a list.
- A doc that is `None`, `{}`, or has a list for `coverage` gives an empty set.
- `execution_state: None` is excused. That is the same reading `coverage_reasons` makes (F10).
- Hole: a case-less row naming the obligation is skipped, so the obligation is excused.
- `verified` stays False: the projection of the walked story prints `verified: false, execution_state: not_run, gap: "not checked by hand: unprepared - no rule"`, and the function mutates nothing.
- `UNPREPARED_GAP` copies the producer's literal at coverage_contract.py:705 (F10).

**K5 holds for the builder's four walks. Two added walks.** These are `k5.py` runs on the `after-checks` fixture plus TS-2 with obligation O-TC2:
- walked: `after_checks`, no reasons, TC-002 listed once (`['unprepared_walk']`).
- stale: `no`.
- not walked: `no`, with the traceability, ledger and coverage reasons.
- oracle open: `no`, with only `coverage red: O-TC2`.
- Added, no triage row for the walked case: verdict `no`, reason `triage:manual: the failure TC-002 has no verdict in triage.json`, and TC-002 is still an item. The person gets the item and a reason. That is right: S7 owes a verdict on an unprepared walk (contract.py:4691, s7_pretriage.py:163).
- Added, a walked row plus a later real result. Through the reducer, the same `case::oid` key keeps only the latest row (finalize_task.py:543-571), so the walk is gone. With both rows current by hand, the case is mixed and excluded: `pass` gives `no` (coverage reason) and `fail` gives `no` (`failed:untriaged`). No excuse.

**K6 holds, except for F2.** Both new kinds rows point at the existing kind `unprepared_walk` (`after_checks`, owner factory). `delivery_summary.state_words` prints the `row_states` sentence per ledger row (delivery_summary.py:44-52, 507). Both sentences hold no code word.
- "the factory could not prepare this check; left with you to check" is true for every road to `not_executed:unprepared_walk`. But that row-level state also gets copied to the row's other cases (F2).
- "its results could not be read by code; left with you to check against the run log" fits both roads to `report_unread`: the test row (ledger.py:1207) and the plan row (883).

**K7.** The readers I checked:
- `report_facts.py`: `_execution_outcome` reads only reason texts, and `after_checks` kinds give none. `_not_run_instances` (3281-3295) reads a `not_executed:*` plan row as "every manifest test of the row is not run". So a walked row marks its automated siblings "not run" in the word-passed gap lines. This is the F2 class.
- `delivery_summary.py`: changed through `row_states` only.
- `bug_records.py`: no reader.
- `handoff_check.py`: no reader.
- `finalize_task.py`: the reducer, unchanged.
- `s7_pretriage.py`: an unprepared row stays the analyst's call, unchanged.
- A manifest `unresolved[]` row with reason `unprepared_walk` would collide with the new gap, but it is refused as `factory_record` (check_delivery.py:745), so the collision gives `no`.
- `ledger.test_state` with status `""` gives `not_executed:no result for this test` (`k7.py`). It is not a defect.
- The `_case_chain` docstring describes `unresolved:<reason>` as "the manifest's unresolved[] row". For the new gap that is now untrue (F6).

**K8.** The test lines are 69 and the product lines 94 (numstat), so the volume rule holds.
- Strongest first: the assess walk table (it kills the loss of the excuse, the oracle guard, and the stale and walked filters); the plan-row entries ("no marker" kills a return of `passed_green`, "failed sibling" kills a wrong position); the `current_unprepared` table; the trace table.
- A row that cannot fail for its stated purpose: `test_third_verdict` "an automated row names the case" (F7).
- The spec asked for 0 new rows. The builder wrote two new table functions (`an_unprepared_manual_walk_...`, `k_u7_7c_...`) instead of entries in the 7b-B tables (note, the Lead's call).
- Load-bearing, ONE entry: in the existing assess table, a fifth row "TC-002 walked and a second case on O-TC2 not walked", expecting the `coverage:` reason to be kept. That is the only rule unique to this twin. The execution, id and absent-state guards each sit behind a second guard (the second case's own `no`, `coverage_reasons` raising), so none of them is the sole keeper.

**K9 fails in two places (F5, F6).** The changelog claims "one item" (false under F2) and "a plan row whose case has no result at all can no longer read passed_green" (false for a case with no row, `k3c.py`). The restated `unprepared_records` docstring is true, but "the obligation is excused" holds only while the oracle is closed. No other contradiction found:
- `agents/qa-runner.md:51` and `design/architecture.md:48` (axis 2) agree with the code.
- `agents/qa-failure-analyst.md` has no hit.
- `handoffs/vocabulary.yaml:63` (the role word `unprepared_walk`) is unaffected.

The search was `grep -rn -i "unprepared"` over `agents/`, `references/`, `design/` and `handoffs/`. Positive control: the qa-runner hit.

## Findings

**F1 - blocking.** `ledger.py::plan_row_state`, the blank branch at lines 874-879, returns before `deferred_by_decision` (lines 913-921), and that state says `no`.

Reproduction, `plan_row_state` direct (`k3d.py`): walked TC-9 plus passed TC-4 whose Then 1 is `deferred_by_decision:gate_a`. The branch gives `not_executed:unprepared_walk`; the base gives `deferred_by_decision`.

Through `assess` (`k3e.py`, walk D1): the branch gives verdict `after_checks`, no reasons, and TC-003 listed as `unprepared_walk`. The base gives `no` with "deferred without a decision: TS-2 is `deferred_by_decision`, and no word of yours is recorded for it". In the stale control D0 the verdict stays `no`, but the deferral reason disappears.

This breaks section 5's error direction ("toward `no`") and the commit's AR-28 claim. N6's invariant lists only the states ABOVE `skipped`, so the spec was silent on a `no` state below it (question 1).

Same class, same function: the 7b-B `read` branch (line 882). Read TC-9 plus a deferred passed TC-4 gives `not_executed:report_unread` (`k3f.py`, plan-row level; assess not run).

Smallest fix: hoist the `deferred` list above both branches and return `deferred_by_decision` first. Alternatively, move only the walked return (and the `read` return) below the deferred branch, keeping the not-walked `no result` return where it is. Add one entry to the plan-row table: walked plus a deferred sibling gives `deferred_by_decision`.

**F2 - fix before merge.** The plan-row kind is copied to every case of the row. `check_delivery.row_cases` (used by `ledger_records`) takes all cases of the plan row and ignores the state's detail. So siblings that passed, were skipped, are unread or are deferred become "Left with you" items of kind `unprepared_walk`, worded "the factory could not prepare this check".

Reproduction, walk B (`k3b.py`): walked TC-002 plus passed TC-003 gives `after_checks` with two items, TC-002 and TC-003, both `unprepared_walk`. This contradicts the kinds note ("ONE item") and inflates `{n}`.

Smallest fix: in `ledger_records`, scope the cases of a plan row whose state is `UNPREPARED_WALK_STATE` (and `REPORT_UNREAD_STATE`, the twin) to the cases its detail names. The precedent is `_stricter_scope`. This is outside the `check_delivery.py` parenthetical in the owns: the Lead widens the owns or opens a node. `report_facts._not_run_instances` is the same class.

**F3 - fix before merge.** Area identity. Plan case `TC-9`, current rows `web/TC-9` (walked) and `api/TC-9` (`walked: False`): `plan_row_state` gives `unprepared_walk` and `_case_chain` gives `unresolved:unprepared_walk` (`k3c.py`, `k2.py`). The not-walked row is hidden behind the bare-id match. With an obligation shared by both rows, coverage still keeps `no`; a story with no coverage obligations reads `after_checks`. The Lead's fork says not walked keeps `no` (estimate: the assess run was not done for this shape).

Smallest fix: `current_unprepared` (or a sibling return) also yields the disqualified case keys, and both readers require `names_case(walked, c) and not names_case(disqualified, c)`.

**F4 - fix before merge.** `unprepared_obligations` drops case-less rows from `cases_of` (check_delivery.py:1830, `row.get("case")`). An obligation whose other current row has no case and is `inconclusive` is excused (`k4.py`: `excused=['O1'] reasons=0`). The error direction is toward the excuse. Smallest fix: key every row, `str(row.get("case") or "")`. The key `""` is never in `walked`.

**F5 - fix before merge.** The changelog sentence "a plan row whose case has no result at all can no longer read `passed_green`" is false for a case with no row at all (`k3c.py`: `passed_green`, base and branch), and "one item" is false under F2. Fix: say "a case recorded with no result", and fix F2 or drop "one".

**F6 - fix before merge.** The `_case_chain` docstring defines `unresolved:<reason>` as the manifest's `unresolved[]` row. Add one line for `unresolved:unprepared_walk` (a walked unprepared manual case, from the run report).

**F7 - note.** In the `test_third_verdict` row "an automated row names the case", the automated row is `passed`, so the case returns `executed_passed` before the new branch. Deleting the `not any(current_results ...)` guard does not fail the row. Fix within the same line count: give the row status `""` and expect `["result:none"]`.

**F8 - note.** Tests: two new table functions against the spec's "0 new rows"; the load-bearing entry is described under K8.

**F9 - note, question 2.** An absent `walked` counts as walked, and so do `0` and `"false"`. Only legacy or hand-made records carry these, and they move from `no` to `after_checks`.

**F10 - note.**
- One malformed id list empties `current_unprepared` (safe direction).
- `execution_state: None` is excused (the same as `coverage_reasons`).
- `UNPREPARED_GAP` is a second copy of coverage_contract.py:705, the same class as F4 of t-1304 (proposed node: export one constant from `coverage_contract` | node: the Lead opens it, or folds it into the t-1304 F4 node).
- The plan row skips the "no automated row" guard that the trace applies: a walked case plus an automated status `""` reads `unprepared_walk` at the plan row and `result:none` in the trace, and the verdict is `no`.
- In `current_unprepared`, the local `ids` holds `[flag, ids]`, so the name lies.

## Seam and class notes, standing questions

- Q1: items 1-6 and N9/N10 are implemented. Item 5's "error direction toward no" is broken by F1.
- Q2: the builder's choices (absent execution counts as failed; every naming row must be walked) are in the safe direction, except F4.
- Q3: additive. The one call site in `assess` is a union.
- Q4: the F1 sibling is in 7b-B's `read` branch (same function, in owns). The F2 siblings are in `ledger_records` (outside owns) and `report_facts._not_run_instances`.
- Q5: F7, F8.
- Q6 DUPLICATION AND CONSISTENCY: `current_unprepared` is a second reader of the marker beside `unprepared_rows`; the spec ordered it. The ids expression `current_obligation_ids or obligation_ids` now appears in 3 new or old readers, and coverage_contract has a fourth. The gap literal is a twin (F10).
- Q7 CODE QUALITY: no new function is over 60 lines or nested deeper than 3 levels. Findings: the `ids` name (F10) and the docstring (F6).
- Q8: no CRLF in the diff (`grep -c $'\r'` gives 0). No Cyrillic (`grep -cP` over the Cyrillic range gives 0; positive control: CLAUDE.md gives 15).
- Q9: no ratchet touched.
- Q10: AR-22, AR-27 and AR-28 are named in the commit; F1 contradicts AR-28. VARIETY: an area project (F3) is the shape that breaks.
- Q11 JUDGMENT: none; a closed marker is joined to a closed state.
- Q12 ONE ROAD: none found. The diff holds no language, runner or project-name branch (read whole).

## Questions for the architect

1. N6 lists the states that must not be hidden only ABOVE `skipped`. Should the rule be "no `no`-verdict state anywhere below is hidden", which covers `deferred_by_decision` (F1) for both 7b-B and 7c?
2. Should a record with no `walked` field (from before t-1955 N3) count as walked (`after_checks`) or as unknown (`no`)?

## Trail

- Read: the diff in full. The spec at lines 40-99 and 355-390. The t-1304 review at lines 1-60. `ledger.py` 780-958 and 1190-1210. `check_traceability.py` 51-158. `check_delivery.py` 1760-1890, 1975-2000 and 2255-2330, plus `row_cases`. `contract.py` `run_results`, `rollup_status`, `names_case`, `case_lookup` and `is_unread_row`. `coverage_contract.py` 640-720. `manual_evidence.py` 1040-1070, 1205-1300 and 1545-1590. `finalize_task.py` 520-575. `report_facts.py` 1780-1800, 2494-2503 and 3278-3295. `delivery_summary.py` 30-75 and 480-510. `handoffs/vocabulary.yaml` 30-70. The fixture `after-checks`.
- DoD run, `python -B .../tests/test_ledger.py`: `=== test_ledger: 468/468 ok ===`.
- `test_manual_evidence.py`: `274/274 ok`. `test_unprepared_outcome.py`: `Ran 19 tests ... OK`.
- Narrow call of the two new functions (`narrow.py`): 16 PASS, no FAIL line.
- Scratch probes, all in the scratchpad folder: `k1.py`, `k2.py`, `k3.py`, `k3b.py`, `k3c.py`, `k3d.py`, `k3e.py`, `k3f.py`, `k4.py`, `k4b.py`, `k5.py`, `k7.py`. Each base comparison ran with `PKG=<scratch>/base/ai-packages/qa-factory` (from `git archive origin/main`).

```json
{
  "verdict": "blocker",
  "blockers": [
    "F1: ledger.py plan_row_state blank branch (874-879) returns before deferred_by_decision (913-921, verdict no): walked unprepared case + a sibling Then deferred with no recorded word gives after_checks instead of no (k3d/k3e, base gives no); same hole in the 7b-B read branch (882, k3f)"
  ],
  "class_completeness": "F1 sibling: 7b-B read branch in the same function (in owns) - fix in this round. F2 siblings: check_delivery.ledger_records/row_cases (outside owns, Lead widens or opens a node) and report_facts._not_run_instances. F10 literal twin joins the t-1304 F4 node.",
  "fixes": [
    "F1 (blocks): hoist the deferred list in plan_row_state above the blank and read branches, return deferred_by_decision first; one plan-row table entry",
    "F2: scope ledger_records cases of an UNPREPARED_WALK_STATE / REPORT_UNREAD_STATE plan row to the cases its detail names (precedent _stricter_scope)",
    "F3: readers require names_case(walked) and not names_case(disqualified) so a not-walked area row is not hidden behind a bare plan case",
    "F4: unprepared_obligations keys case-less rows as empty string instead of skipping them",
    "F5: changelog - 'a case recorded with no result', and drop or fix 'one item'",
    "F6: _case_chain docstring gains the unresolved:unprepared_walk line"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r4-7b-7c-e7.md",
      "docs/tasks/specs/reviews/t-1304-u7-7b-b-unread-run-delivery-code.md",
      "ai-packages/qa-factory/scripts/ledger.py",
      "ai-packages/qa-factory/scripts/check_traceability.py",
      "ai-packages/qa-factory/scripts/check_delivery.py",
      "ai-packages/qa-factory/scripts/manual_evidence.py",
      "ai-packages/qa-factory/scripts/contract.py",
      "ai-packages/qa-factory/scripts/coverage_contract.py",
      "ai-packages/qa-factory/scripts/finalize_task.py",
      "ai-packages/qa-factory/scripts/report_facts.py",
      "ai-packages/qa-factory/scripts/delivery_summary.py",
      "ai-packages/qa-factory/references/delivery-verdict-kinds.json",
      "ai-packages/qa-factory/references/report-risk-words.json",
      "ai-packages/qa-factory/handoffs/vocabulary.yaml"
    ],
    "reruns": [
      {"command": "python -B <worktree>/ai-packages/qa-factory/scripts/tests/test_ledger.py", "result": "468/468 ok"},
      {"command": "python -B <worktree>/ai-packages/qa-factory/scripts/tests/test_manual_evidence.py", "result": "274/274 ok"},
      {"command": "python -B <worktree>/ai-packages/qa-factory/scripts/tests/test_unprepared_outcome.py", "result": "Ran 19 tests OK"},
      {"command": "scratch narrow.py: the two new test functions by import-and-call", "result": "16 PASS, 0 FAIL"},
      {"command": "scratch k3e.py on branch and on origin/main extract", "result": "D1 deferred sibling: branch after_checks, base no"}
    ]
  }
}
```
