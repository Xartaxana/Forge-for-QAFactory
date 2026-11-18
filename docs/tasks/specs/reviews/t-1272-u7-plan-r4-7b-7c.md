# t-1272 - plan re-review: U7 spec r4, nodes 7b-A, 7b-B, 7c (answers t-1267)

Spec: `docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r4-7b-7c-e7.md` (header, §0-§5, §8-§11). Verdict answered:
`docs/tasks/specs/reviews/t-1267-u7-plan-7b-7c.md`. Code read in the root checkout, HEAD 3e1df1e4; `git diff --stat 3e1df1e4
53142f95` (today's origin/main) over the eleven package files read is empty, so the reads hold on origin/main. Package root below:
`ai-packages/qa-factory/`.

## Verdict

- **7b-A: ACCEPT WITH FIXES.** B1, B5, B6 (binding), F1, F8 are closed as executable text. Fixes N1-N4 below are text edits the
  Lead makes before the dispatch is cut. N1 (the decided F-r4-2 is still a non-goal in the dispatch block) and N2 (the factored key
  helper drops D2-B3's area guard) must land first: as written, a builder either cannot do the decided change or builds a
  cross-area misreading.
- **7b-B: ACCEPT WITH FIXES.** B2, B3, B4, B6 (delivery), F2-F4, F6, F7 are closed. Fixes N5-N8 are needed: the red rule, the
  plan-row position against `expectation_unconfirmed`, one classifier for readings rather than two, and the `to_check` road.
- **7c: ACCEPT WITH FIXES.** K4 of t-1267 is carried whole. Fix N9 is needed: the walk twin of `excused` lacks the `oracle_open`
  guard D3 has, which is the error direction, and the same omission was in my own K4. Fix N10 is needed too: names and owns.
- No finding blocks the design. Every fix is a text edit with no new fork. I propose that the Lead checks the edits instead of a
  third critic pass. That decision belongs to the Lead (rule 6).

## Findings (each: where, failure scenario, fix)

**N1 (7b-A, fix before dispatch: owns cannot carry a decided fork).** The Lead block decides F-r4-2 = (a): "`bug_records.py` and
`test_bug_records.py` join 7b-A's owns". The §4 7b-A block has not changed to match. `owns:` has neither file. `non-goals:` still
says "`bug_records.py (fork F-r4-2)`", and §0 has no F-r4-2 row. A builder who follows the block refuses the change. Fix:
- Add `bug_records.py (_walk_has_no_run only)` and `tests/test_bug_records.py` to the owns.
- Drop the non-goal.
- Add a §0 row. The row needs the behaviour `kind in ("manual", "observation", "unread")` at `bug_records.py:1052`. It also needs
  the docstring 1040-1042 restated, because a function named "has no run" now admits a target that HAS a current row (not red by
  construction), so the docstring would lie (Q7). The comment at 1082-1085 needs the same restatement.
- Add one entry to the existing reproduction table of `test_bug_records.py`: "walk entry on an unread target with APP_BUG -> no
  `R_NOT_RED_NOW`; a fresh_data_rerun entry on it -> still refused". The second half is the killing control of the narrowing.

**N2 (7b-A, fix before dispatch: AR-13 helper reproduces a fixed defect).** A2 says `unread_case_reading` reads case keys through
"the key expression of `run_results`, 4472-4473, factored into one private helper both call". The keys at 4472-4473 include
`case_ids(row["case"])`. For an area row `api/TC-4`, that is the bare alias `TC-4`. `run_results` drops that alias only at
4466-4471 + 4478-4479 (`area_of`; the comment at 4463-4465 says why: "the red of `api/TC-4` would read as the result of
`web/TC-4`"). Factor only 4472-4473 and match by `case_matches`, and the bare key `TC-4` names `web/TC-4`. Failure: coded row
`api/TC-4` + APP_BUG and coded row `web/TC-4` + NOT_EXECUTED give `unread_case_reading(..., "web/TC-4") == "red"`. `plan_row_state`
then reads `failed:APP_BUG` for the web row, and the trace reads `executed_failed`. Fix: the helper is 4466-4479, the keys WITH the
area-alias drop, and both callers use it. Add an entry to the `test_ledger.py` plan-row table: "red on `api/TC-4`, read on
`web/TC-4` -> web row `not_executed:report_unread`".

**N3 (7b-A, fix: a name list is left to invent).** The `triage_failures` loop in A2 is
`add("unread", names, ids, attempt, old=...)` "exactly as the result loop computes them (4729-4736)". The result loop takes `names`
from `triage_targets(...)["names"]` (4728). Lines 4729-4736 compute only attempt, ident, ids and old. A2 keeps unread names out of
`names`, so nothing hands the loop the list, and a builder may pass `[names[0]]`, which loses the other spellings `same_id` binds
by (NEAR step, `bind_triage` 4808-4809). Fix: state that the unread loop builds `names` from the same four keys as 4646-4647
(`instance_id, test_instance_id, test_id, test`, non-empty, in order).

**N4 (7b-A, fix: dispatch conflicts with the Lead block).** The Lead block caps the witness at "at most three test files". The
7b-A DoD says "green in the four keep files", and N1 adds a fifth (`test_bug_records.py`). `test_story_run_s7.py` is canon-only
(`test_story_run_*`), so its row is reported "not run - the canon judges" or run by its row selector. Fix: name the explicit list in
§4: `test_s7_pretriage.py`, `test_s7_null_outcome.py`, `test_triage_identity.py` + `test_bug_records.py` by row selector, or the
Lead raises the cap for this node by name. The same applies to the stale `scenario_walk.py --witness-for <owns>` lines in the
§4/§5 DoDs, which the block says are replaced.

**N5 (7b-B with its 7b-A helper, fix: "red" waits for every sibling, so a red is hidden).** A2: `"red"` only "when any coded row's
reading is a verdict other than NOT_EXECUTED and none is `""`". Case with two coded instances, APP_BUG on one and no row on the
other: the reading is `"unanswered"`. D2 then leaves the plan row at `skipped:inconclusive run` (`decided_elsewhere`, verdict
none). The analyst's red is missing from the plan row, but today's analogue rolls up red (`rollup_status`: any failed -> failed,
4424-4425). Not a pass: test_state, triage_gap and coverage still say `no`. But FR-10 breaks, because the plan row and the test
row disagree on a red the analyst wrote. Fix: `"red"` when ANY coded reading is a failure verdict. `"unanswered"` only with no red
and some `""`. Both are `no`, so the error direction holds. The same rule applies to D3's `red` (N7).

**N6 (7b-B, fix: positional invariant incomplete; my own F3 recommendation was incomplete).** D2 (ii) puts `"read"` ->
`not_executed:report_unread` (`after_checks`) after `error` (841) and before the unknown word (847). That is above the
unconfirmed-expectation branch (851-856). Today a `not_run` case meets the unconfirmed branch BEFORE `skipped` (857), so an open
per-Then expectation (`then_bindings` reason `expectation_unconfirmed`, or `open_oracles`) shows as `not_verified:expectation_unconfirmed`.
After D2 (ii), run_unread hides it. The run_unread item still comes from test_state and the trace, but the oracle debt is carried
by the plan row alone (the trace sees only whole-case `unresolved[]` rows, `check_traceability.py:55-76`). Fix: place (ii)
immediately before 857, after unconfirmed. Invariant: "no failure, flaky, partial, error, unknown-word or unconfirmed word is
hidden by run_unread". Add an entry to the plan-row table: "read + an unconfirmed Then -> `not_verified:expectation_unconfirmed`".
The same placement applies to 7c item (5)'s `not_executed:unprepared_walk` (after_checks). Its `no` twin `not_executed:no result
recorded` may stay above, because the direction is toward `no`.

**N7 (7b-B, Q6 fix: two classifiers of the same readings).** `unread_case_reading` (A2) and `unread_obligations` (D3) each turn
the same `unread_readings` verdicts into read/red/unanswered, with different wording of the same rule. Today D3 says "any other
verdict (and no `""`) -> red", which is N5's defect again. Fix: one pure private `contract._reading_of(verdicts) -> "" | "read" |
"red" | "unanswered"`. `unread_case_reading` calls it per case and `unread_obligations` per obligation. D3 adds its own coverage
guards (oracle closed, design sufficient, gap text) on top.

**N8 (7b-B, fix: the road for `to_check` is left to invent).** D6 asks for "limitations of the bound rows". `unread_readings` returns
verdicts only. Fix: name the road. It is `C.bind_triage(C.triage_failures(facts["report"])[0], facts["triage"])["matched"]` over
keys of kind `unread`, mapped to cases by the existing `_failure_cases(key, failure, facts)` (`check_delivery.py:1396-1412`), so no
new matcher is written. Also state F1's precedence over `_file_verdict`'s `id_not_in_report` (`run_suite.py:691`): F1 sits after
540, so for a `file` contract with zero report rows it REPLACES that code. That is harmless: the only reader is
`run_history.py:423`, for failed blocks only, plus the console count at `run_suite.py:2396`. But the replacement is a position
the spec does not name (CLAUDE.md rule 11 ii).

**N9 (7c, fix before dispatch: error direction).** Item (4) excuses "an obligation id in `current_unprepared`'s set whose
`execution_state` is not `failed`". Coverage, for an unprepared manual obligation with an open oracle that is not waiting: execution
`not_run`, so `oracle_open` True gives `coverage red:` (`check_delivery.py:1791-1792`). `awaiting` skips only a WAITING oracle
(`coverage_contract.py:688-689`). Item (4) removes that `coverage red:`. No other producer carries it: `plan_row_state`'s
`green_open` reads only green cases (863), and the trace reads only whole-case `unresolved[]` rows. The open oracle then reaches
`after_checks`, against FR-59/AR-28. The same omission was in my t-1267 K4 item 4. Fix: the walk twin carries D3's guards,
`oracle_open` False and a gap that starts `not checked by hand: unprepared` (`coverage_contract.py:705`). Add an entry to the 7c
assess table: "unprepared walk, oracle open -> `no`".

**N10 (7c, fix: names and owns).** The twin in (4) has no name ("`unread_obligations`' twin"). Name it, for example
`unprepared_obligations(doc, report) -> frozenset`, beside `unread_obligations`. Add `assess` (its call, the union into `excused`) to
the 7c `check_delivery.py` owns parenthetical: the union happens at the call site, which the block does not name.

## Per-key answers

**K1. All rows of §0 checked against the code.**
- **Citations.** Every cited line holds: `contract.py` 4472-4473, 4595-4752, 4820; `ledger.py` 1172-1182, 1245, 819, 839-859;
  `check_delivery.py` 1468/1473, 1764-1795, 2013-2029, 2263, 2648; `check_traceability.py` 87-92, 191; `s7_pretriage.py` 233-236,
  270-283, 370-372; `driver_stage_s7.py` 21-46, 121; `handoff_check.py` 1378-1382; `finalize_task.py` 687, 727;
  `run_suite.py` 511-541, 1367, 2244, 2290; `qa-failure-analyst.md` 67-68, 87; `role-load.json` 19 = 21557, 33 = 19507.
- **B1-B7 and F1-F8.** Closed as file::function + position + behaviour + row, except B7 for F-r4-2 (N1) and F5 for one name:
  t-1267 F5 listed `report_facts.EXECUTION_OUTCOME_STATES` (2488), and §8 has no line for it. Answer: unchanged.
  `_execution_outcome` reads the `not_executed` prefix of a ledger REASON (2496). `not_executed:report_unread` is `after_checks`,
  so it gives no reason text, and if it did, "not executed" is true. Add the line.
- **New design.**
  - `unread_readings`: the right join. `matched` excludes ambiguous rows, and `""` covers none/several. It never raises.
  - `unread_case_reading`: the four words and the direction are right except "red" (N5) and the key helper (N2).
  - `triage_row_for` still binds the analyst row after 7b-A. Traced: own status `not_run` makes `own_green`, so near is `[]` and the
    key is `("ask", name)`. In `bind_triage(pool)`, the row binds exactly to both `("unread", name)` and `("ask", name)`, so
    `matched[ask]` has 1 row. That is the analyst's row (contract.py 5088-5104).
  - `coverage_reasons(excused, red)`: defaults keep both callers. Readers block: `test_delivery_ownership.py` and
    `test_check_delivery.py` name it, and positional calls are unchanged. The `coverage red:` family owner is product by
    `references/delivery-reason-owners.json:99-102`. The record kind stays `coverage_gap` (`assess` 2648), the same two-owner shape
    as today.
  - `triage_rows` keyword: the only production caller of `_case_chain` is `walk` (245). `outcome_for_case`/`gap_of_case` have test
    callers only (`test_case_key_identity_join.py`, quarantined `test_traceability.py`). The keyword keeps the wrappers equal to the
    chain (C5), so it is not dead.
  - `plan_row_state` positions: (i) right; (ii) N6.

**K2. Walks traced (7a's predicate taken as r3 §2 r4 rules 1-5).**
- **Walk 1:** `failures_to_triage` is non-empty (unread reason). `decide` sends unread to `left`. `closes` stays False (`kept`
  empty, 376). The reducer keeps the row (727 + `bind_triage`). `test_state` gives REPORT_UNREAD_STATE (row branch, before 1182). The
  plan row reads "read" (ii). The trace gives `result:report_unread`. Coverage excuses it. `not_executed_findings` skips the row, and
  `triage_reasons` stays silent (1 row). Ends `after_checks`, factory. No factory `no` among the sites t-1267 K3 listed. The assess
  producers outside that list (completeness, witness, lifecycle) are not traced here, so the 7b-B handoff run through `assess`
  carries the empirical proof.
- **Walk 3:** red on the ledger (1182), the plan row (819 + `_verdict_for_cases`), the trace (`executed_failed`) and coverage
  (`coverage red:`). Holds, with N5 for a half-answered case.
- **Walk 4:** `triage:` (1473 with unread). Ledger: no row, `not_run` known, so NO_RUN_RESULT (1245). Trace: `"unanswered"`, so
  line 92 gives `result:not_run` and `chain_broken`. Coverage: a `""` verdict means neither excused nor red, so `coverage:` stays.
  No `after_checks`.
- **Temporal world (7b-A merged, 7b-B not):** answered gives `failed:NOT_EXECUTED`, so `not_executed_unproven` (`no`, factory),
  plus the NOT_EXECUTED_NOT_RE_DERIVED finding and the coverage gap. Unanswered: the S7 form refuses (kind-agnostic 1340-1346);
  past it by a person's word, `not_executed:<NO_RUN_RESULT>` and `chain_broken`. Never a pass.
- **Neighbouring class walked:** TEST_BUG/FLAKY on an unread target goes to the repair route (`stage_status.REPAIRABLE_VERDICTS`,
  171). The repair re-run is still unread, so a new attempt and a new triage follow, bounded by the repair limit. No new loop, no
  finding.

**K3. Split.** 7b-A and 7b-B own disjoint files. 7b-B reads 7b-A's contract names and merges after it (stated). 7b-B and 7c share
`ledger.py`, `check_traceability.py`, `check_delivery.py`, the kinds file and three test files. The order "7b-B -> 7c" is stated,
and 7c's edit sits in the same 87-92 branch on another word (`""` vs `not_run`). Left to invent: N3, N8, N10. Not carried: N1.

**K4. Forks.**
- **F-r4-1 (a)** is not wrong on the code: exit != 0 with no totals is `broken_run` (1367), which F1 leaves uncoded. The S7 entry
  refuses, and delivery gives `run_not_deliverable`, which equals today, so no regression. Residual (Q4/Q12 d): (b) is "a node only
  if a live run shows the case", a condition with no carrier. Give it one: an L6 variant in §7, "a `reporter: none` run with a
  failing test, exit != 0: today's halt and the conductor; if seen, open U8 node (b)". That way the live-runs pile carries it as a
  line, not as memory.
- **F-r4-2 (a)** is right on the code. `_current_red_problem` gives `R_NOT_RED_NOW` for a `not_run` row (1000-1003). The skip
  touches walk entries only (1095), and the APP_BUG fact stays. It is the same class as manual/observation. It needs the text in N1.

**K5. 7c vs t-1267 K4.** Items 1-7 are all carried, and item (3) correctly adds the `ledger_states` row that item (5) needs.
`walked: False` keeps `chain_broken`, in the edges and the non-goals. Open: N6 (position of the after_checks word), N9, N10.

**K6. Test volume.** About 40 named rows reduce to 6 new parameterised rows. The rest are entries of those rows or of tables that
already exist; the rows below either sit on an internal boundary or duplicate a door already driven.

| behaviour (door) | file | new row? | entries |
|---|---|---|---|
| producer `build_run_block` codes / does not code (run block field) | test_s7_pretriage | NEW 1 | F1's 7 summaries |
| 7a predicate admits unread | test_s7_pretriage | existing 7a table | 3 (B1) |
| S7 dispatches the analyst over unread, no `s7.no_failures` close, brief names unread (driver) | test_story_run_s7 (canon) | NEW 1 | unread-only; mixed with a kept code row (reaches `brief`/`told`) |
| S7 form zero-row refusal names unread | test_s7_null_outcome | entry of the zero-row cases | 1 |
| reducer keeps the bound row, no "no product failures" (triage.json) | test_s7_null_outcome | NEW 1 | reduce + refresh asserts in one row |
| `multiple` on unread | test_triage_identity | existing table | 1 |
| walk receipt on unread (F-r4-2) | test_bug_records | existing table | 2 (N1) |
| ledger test state of an unread test (ledger doc) | test_ledger | NEW 1 | B2's 4 |
| ledger plan-row state (ledger doc) | test_ledger | NEW 1, or joined to the row above by a "level" column | F3's 4 + N2 + N6 + 7c's 2 |
| trace gap word of a case (walk) | test_third_verdict G_walk | NEW 1 | D4's 4 + 7c's 5 |
| kinds rows | test_third_verdict | existing kinds table | `result:report_unread`, `not_executed:report_unread`, 7c's two |
| delivery verdict of the §3 walks (assess) | test_check_delivery | NEW 1 | walks 1-4 + oracle open + stale row + two instances of one case (F2) + 7c's walk / stale / oracle-open (N9) |

- **Internal boundary, no own row:** `decide`; `brief`; "pretriage never closes" (the story row asserts no close);
  `unread_readings`/`unread_case_reading`/`_reading_of`; `unread_obligations`; `coverage_reasons` direct; `build_left_items`
  direct ("one item per case" is an entry of the assess row); `not_executed_findings` direct (B4 is walk 1 plus the stale entry);
  `triage_reasons` direct (walk 4).
- **Duplicates if written as their own rows:** B3's four rows against the assess walk table (same door, Q5 e); D4's rows asserted
  again through assess.
- **The temporal edge** "7b-B not merged" gets no row: it cannot exist after the merge, and the walk-4 entry carries its invariant.
- **Budget:** 7b-A 3 new rows + about 7 entries; 7b-B 3-4 new rows + about 17 entries; 7c 0 new rows + about 12 entries.

## Standing questions (plan gate)

- **Q13 (a) EDGES:** stated for F1 (7 cases), empty report, nameless coded row, passed + code, stale row, two rows, mixed case, both
  temporal worlds. Missing: the half-answered case (N5), the open oracle under a walk (N9), unconfirmed beside read (N6).
- **Q13 (b) MEANING:** `reason_code: report_unread` = "this row is not_run because the exit-0 run wrote no readable report".
  `run_unread` = "the analyst read the log as not-a-failure; the person checks". "red" = "the analyst wrote a failure verdict
  for an unread row" (after N5). No contradiction with §3 once N5 and N6 are applied.
- **Q13 (c) PREMISES:** re-ran two. (1) `test_state` returns from the row block before 1239, with B2's position inside it: holds
  (ledger.py 1171-1182). (2) Coverage execution is `inconclusive` for `not_run` outcomes, with the gap text "current sufficient
  evidence incomplete": holds (coverage_contract.py 633-638, 698-701). The analyst-form premise (A6) stays a stop condition in the
  node. It is a declared unknown, not a claim.
- **Q13 (d) READERS:** the block was not attached, so I re-ran it (trail). The first call was a miscall: comma-joined `--names`
  read as one name, "absent". Space-separated names on origin/main 53142f95 give:
  - `names` test_case_key_identity_join (`_case_chain`, `outcome_for_case`): unchanged, keyword default None.
  - test_check_delivery (slow) (`bind_triage`, `coverage_reasons`): judged by the batch canon; new rows go in by row selector.
  - test_delivery_ownership (`coverage_reasons`): unchanged, defaults.
  - test_s7_null_outcome (slow), test_third_verdict (slow): the batch canon judges them.
  - test_s7_pretriage, test_triage_identity, test_triage_blocked (`triage_failures`): unchanged, additive kind.
  - `more` lines: interface kept, because every new parameter defaults.
  - Known misses: miss 3 (pinned VALUE): the ratchet values 21557/19507 rise, named (F8). Miss 6: base 53142f95 is origin/main:
    yes. Misses 1, 2, 4, 5 and 7 were not walked further: the §8 hand grep, 152 lines, reproduced by me (count 152 over 25 files,
    14 production files, all 14 in §8).
- **Q13 (e) FORKS:** K4.
- **Q4 CLASS:** t-1267 K3's 13 sites are all placed. A new sibling inside this artifact is N9 (7c's twin of D3), plus the
  plan-row position for both after_checks words (N6). Outside the map, no analog found.
- **Q6 DUPLICATION:** N7 (two classifiers), N2 (factored helper must be the whole key rule). Otherwise none found. Grep
  `REPORT_UNREAD|triageable_not_executed`: 0 hits on HEAD (not merged); positive control `report_unreadable` found (t-1267 trail,
  same tree).
- **Q12 ONE ROAD:** none found. The narrowing is the data word `reporter: none` plus the exit code, not a runner or language name.
  The kind tuple in `bug_records` is a closed contract vocabulary. Residual F-r4-1 (b) is given a carrier (K4).
- **VARIETY:** a project whose runner writes no JUnit (axis 3), exit 0: after 7b it passes S7 by the analyst's reading, with no
  silent default. Exit != 0: today's S6 halt to the conductor, the same as today, stated in the axis cell (D7). It is not a new
  block, but it is the half a free agent would read, hence the K4 carrier.

## Trail

- **Read:** spec r4 whole; verdict t-1267 whole; `contract.py` 2180-2201, 4249-4299, 4405-4530, 4595-4835, 5063-5107;
  `ledger.py` 679-1023, 1150-1254; `check_traceability.py` 30-270; `check_delivery.py` 1415-1514, 1755-1804, 2000-2039,
  2155-2273, 2594-2678; `coverage_contract.py` 590-714; `s7_pretriage.py` 195-385; `driver_stage_s7.py` 1-135;
  `handoff_check.py` 1330-1389; `finalize_task.py` 676-755; `run_suite.py` 466-610, 682-711, 1350-1381, 2225-2309;
  `run_history.py` 405-434; `bug_records.py` 980-1089; `gate_preflight.py` 5905-6023; `report_facts.py` 2478-2517;
  `delivery_verdict.py` 355-387; `delivery-verdict-kinds.json` whole; `qa-failure-analyst.md` 62-91; `role-load.json` (Grep);
  `test_third_verdict.py` 905-954; `tools/critic_verdict.schema.json`.
- **Greps** (positive control in the same call):
  - `triage_targets\(|triage_failures\(|bind_triage\(|triage_row_for\(` -i, scripts: 152 / 25 files (definitions in contract.py
    found).
  - `gap_of_case|outcome_for_case|_case_chain|check_traceability` -i, production: callers listed in K1.
  - `NOT_EXECUTED` over scripts.
  - `coverage red` over the package.
  - `id_not_in_report`, `R_NOT_RED_NOW|is_red_row|reproduction_problems`.
  - `unconfirmed_bindings\(|NOT_VERIFIED_UNCONFIRMED|expectation_unconfirmed` (count).
  - `def s7_repairs|REPAIR_VERDICTS|"TEST_BUG"`.
  - `summary\["reporter"\]`, `no_junitxml`.
- **Reruns:** the `owns_readers.py` calls (below); `git diff --stat 3e1df1e4 53142f95` over the eleven read files: empty.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "N1 7b-A: F-r4-2 (a) decided but the 7b-A block still lists bug_records.py as a non-goal and owns neither it nor test_bug_records.py; add owns, drop non-goal, add a section 0 row (bug_records.py:1052 kind tuple, docstring 1040-1042 and comment 1082-1085 restated) and one table entry with the fresh_data_rerun control",
    "N2 7b-A: the factored run_results key helper must be lines 4466-4479 with the area-alias drop, else api/TC-4 red reads as web/TC-4 reading (D2-B3); add a plan-row table entry",
    "N3 7b-A: the unread loop of triage_failures builds names from instance_id, test_instance_id, test_id, test as 4646-4647, not from names[0] alone",
    "N4 7b-A: the witness list exceeds the Lead block's three-file cap (four keep files plus test_bug_records); name the explicit list or raise the cap by name; replace the stale scenario_walk DoD lines",
    "N5 7b-A/7b-B: red when any coded reading is a failure verdict, unanswered only with no red; today a half-answered red case reads skipped:inconclusive run on the plan row (FR-10)",
    "N6 7b-B and 7c: the after_checks words (not_executed:report_unread, not_executed:unprepared_walk) go right before ledger.py:857, after the unconfirmed branch, so an open per-Then expectation is not hidden; state that invariant; add an entry",
    "N7 7b-B: one private contract classifier of readings used by unread_case_reading and unread_obligations instead of two rules",
    "N8 7b-B: name the to_check road (bind_triage matched over unread keys plus check_delivery._failure_cases) and F1 precedence over _file_verdict id_not_in_report",
    "N9 7c: the walk twin of excused lacks oracle_open False and the unprepared gap text guard; an open non-waiting oracle under an unprepared walk would move from coverage red to after_checks (FR-59)",
    "N10 7c: name the twin function and add the assess call (union into excused) to 7c owns",
    "F5 residue: add report_facts.EXECUTION_OUTCOME_STATES to section 8 with verdict unchanged",
    "K4 residue: give F-r4-1 (b) a carrier, an L6 variant row in section 7, instead of a conditional node"
  ],
  "class_completeness": "t-1267 K3 sites 1-13 all placed in r4 (section 0 rows). New siblings found in this artifact: the 7c walk twin of D3 lacks D3's oracle guard (N9); the plan-row position against expectation_unconfirmed applies to both after_checks words (N6); the red rule shared by trace, plan row and coverage (N5, N7). Production readers of triage_targets/triage_failures/bind_triage/triage_row_for: 14 files, all in section 8 (count reproduced: 152 lines / 25 files); report_facts.EXECUTION_OUTCOME_STATES from t-1267 F5 missing from section 8 (verdict: unchanged). Repair route on an unread TEST_BUG walked: bounded by the repair limit, no finding.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r4-7b-7c-e7.md",
      "docs/tasks/specs/reviews/t-1267-u7-plan-7b-7c.md",
      "ai-packages/qa-factory/scripts/contract.py",
      "ai-packages/qa-factory/scripts/ledger.py",
      "ai-packages/qa-factory/scripts/check_traceability.py",
      "ai-packages/qa-factory/scripts/check_delivery.py",
      "ai-packages/qa-factory/scripts/coverage_contract.py",
      "ai-packages/qa-factory/scripts/s7_pretriage.py",
      "ai-packages/qa-factory/scripts/driver_stage_s7.py",
      "ai-packages/qa-factory/scripts/handoff_check.py",
      "ai-packages/qa-factory/scripts/finalize_task.py",
      "ai-packages/qa-factory/scripts/run_suite.py",
      "ai-packages/qa-factory/scripts/run_history.py",
      "ai-packages/qa-factory/scripts/bug_records.py",
      "ai-packages/qa-factory/scripts/gate_preflight.py",
      "ai-packages/qa-factory/scripts/report_facts.py",
      "ai-packages/qa-factory/scripts/delivery_verdict.py",
      "ai-packages/qa-factory/references/delivery-verdict-kinds.json",
      "ai-packages/qa-factory/agents/qa-failure-analyst.md",
      "ai-packages/qa-factory/references/role-load.json",
      "ai-packages/qa-factory/scripts/tests/test_third_verdict.py",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B tools/owns_readers.py --paths <16 owns of 7b-A, 7b-B, 7c> --names triage_targets,triage_failures,... (comma-joined)", "result": "miscall: the comma list read as one name, reported absent; base origin/main 53142f95; 17 more-lines"},
      {"command": "python -B tools/owns_readers.py --paths contract.py check_traceability.py check_delivery.py bug_records.py --names triage_targets triage_failures bind_triage REPORT_UNREAD_CODE _case_chain coverage_reasons _walk_has_no_run outcome_for_case gap_of_case", "result": "readers: 562 outside owns; names lines: test_case_key_identity_join, test_check_delivery (slow), test_delivery_ownership, test_s7_null_outcome (slow), test_s7_pretriage, test_third_verdict (slow), test_triage_blocked, test_triage_identity"},
      {"command": "git -C forge-repo diff --stat 3e1df1e4 53142f95 -- <eleven package files read>", "result": "empty (reads hold on origin/main)"},
      {"command": "Grep -i triage_targets\\(|triage_failures\\(|bind_triage\\(|triage_row_for\\( over scripts (count)", "result": "152 total occurrences across 25 files; 14 production files, all in r4 section 8"}
    ]
  }
}
```
