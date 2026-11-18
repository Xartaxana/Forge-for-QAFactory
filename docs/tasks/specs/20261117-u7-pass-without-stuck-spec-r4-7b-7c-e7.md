# Spec U7 r4 - fix round t-1270: §2 site r4 (no-report half), §6 stream 7b, nodes 7c and E7 - ACCEPTED with amendments for 7b-A, 7b-B, 7c (E7 waits)

Replaces in r3 (`.claude/worktrees/arch-docs/docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md`, the copy with the block
"After the plan critic t-1267 ...") ONLY: §2 r4 "Target, 7b" + its 7b edges/invariant/tests; §6 stream 7b; §6 node E7 stub; the
7c stub (r3 header F-16). Everything else of r3 stands (streams 1, 1b, 2, 3, 4a, 5a, 5b, 6, 7a). Input: verdict
`docs/tasks/specs/reviews/t-1267-u7-plan-7b-7c.md` (REJECT 7b: B1-B7, F1-F8; K4 = node 7c) and the Architect's decisions in r3's
header (F2 one item per case; F6 `_case_chain` reads the bound verdict; B3+B6 one node; `coverage_contract.py` untouched,
`verified` False; 7c fork: `walked: False` keeps `chain_broken`; F-5 closed by the owner). Paths are from `ai-packages/qa-factory/`
unless they start with `docs/` or `tools/`. Code read on 17.11.2026 in the root checkout (7a, 5a, 5b, 1 not in that tree: 7a's
predicate is taken from r3 §2 r4 rules 1-5). Every line number below was read in this round unless marked "(critic's read)".

**Lead reading of r4 (Architect session, 17.11.2026; t-1270) - NOT yet an acceptance: nodes 7b-A, 7b-B, 7c go to one plan
re-review (the fix diff and verdict t-1267 only) before dispatch; node E7 waits for the scout read of its trigger site.**
§0 checked against the verdict: every B1-B7 and F1-F8 has a row; spot-read `contract.py:4820`, `ledger.py:1171-1182`,
`check_delivery.py:1467-1473`, `run_suite.py:1365-1367` - as cited. Forks, decided by the Architect ("решила сама", the owner
may reverse):
- F-r4-1 = (a): only an exit-0 no-report run is read by the analyst; a red-exit no-report run keeps today's halt, which the
  conductor meets (a door, not a dead end). (b) becomes a node only if a live run shows the case.
- F-r4-2 = (a): `_walk_has_no_run` also holds kind `unread`; `bug_records.py` and `test_bug_records.py` join 7b-A's owns.
- F-E7-1 = (a), subject to the scout read: the runner records the case unprepared with a typed need; at the S6 -> S7 boundary
  the driver asks once through the seam; "start it" re-walks those cases. This is the closest existing road to the owner's
  «тогда когда это понадобится» (the same run, right after the need was met).
- F-E7-2 = (a): the answer registry. F-E7-3: per stand.
**Two corrections that bind every dispatch cut from this file (the owner's questions of 17.11.2026 on streams 1, 5a, 5b, 7a:
builders ran dozens of whole test files for over an hour, and every diff carried more test lines than code):**
- WITNESS SCOPE: each node's DoD line "`scenario_walk.py --witness-for <owns>`" is REPLACED in the dispatch by an explicit list
  of at most three test files (the keep files that hold the node's own rows), run once after all edits. Everything else the
  command prints is a report line "not run locally: <files>", never a run. No file of the canon-only class (`SLOW_TESTS`,
  `test_story_run_*`, `test_controller_*`, the scenario layer) is run whole: a row added there is run by the file's own row
  selector or reported `not run -- the canon judges`. Measured: `--witness-for` prints 27 files for stream 1's owns and 40
  for 7a's (37 of them for `driver_stage_s7.py` alone).
- TEST VOLUME (`docs/TESTING.md` «Бюджет»): test lines do not exceed code lines. The rows named in §0 and §2 are an upper
  bound, not a quota: one parameterised row per BEHAVIOUR, variants as table entries of that row; an internal boundary gets no
  row (CLAUDE.md rule 11); `tests-over:` is a door for a named reason the critic can judge, and "the spec names these rows" is
  not such a reason.

**ACCEPTED with amendments (Architect session, t-1270 accepted after plan re-review t-1272,
`docs/tasks/specs/reviews/t-1272-u7-plan-r4-7b-7c.md`: accept with fixes for 7b-A, 7b-B, 7c; 0 blocking, 12 fixes).** No
third critic pass: every fix is a text edit with no new fork, and the Lead takes them here. Node E7 (section 6) is NOT accepted
by this block: it waits for its design over the scout digest `docs/tasks/specs/reports/t-1273-e7-trigger-site-digest.md`.
**Where sections 0, 2, 4 or 5 below differ from this block, this block wins; a dispatch of 7b-A, 7b-B or 7c is cut from
section 4/5 TOGETHER with this block.** The failure scenario of each item is in the verdict under the same id.

Amendments (ids of verdict t-1272):
- **N1 (7b-A).** F-r4-2 (a) is decided, so in the 7b-A dispatch: owns gain `scripts/bug_records.py` (`_walk_has_no_run` only)
  and `scripts/tests/test_bug_records.py`; the non-goal "bug_records.py (fork F-r4-2)" is dropped. Behaviour: at
  `bug_records.py::_walk_has_no_run` the admitted kinds are `("manual", "observation", "unread")`; the function's docstring and
  the comment at its call site are restated, because the function now admits a target that HAS a current row (not red by
  construction). Test: ONE added entry pair in the existing reproduction table of `test_bug_records.py` - a walk entry on an
  unread target with APP_BUG gives no `R_NOT_RED_NOW`; a `fresh_data_rerun` entry on it is still refused.
- **N2 (7b-A).** The shared key helper of `run_results` and `unread_case_reading` is the WHOLE key expression including the
  area-alias drop (`contract.py::run_results`, the `area_of` block and the alias removal around it, not only the two key lines):
  the bare alias of an area row never names another area's case. Test entry, added by 7b-B (its door is the plan row) in the `test_ledger.py` plan-row
  table: red on `api/TC-4`, read on `web/TC-4` -> the web row is `not_executed:report_unread`.
- **N3 (7b-A).** In `triage_failures` the unread loop builds its `names` from the same four keys the target reader uses
  (`instance_id`, `test_instance_id`, `test_id`, `test`; non-empty, in that order) - never the first name alone.
- **N4 (all three nodes).** The DoD lines "green in the four keep files" and every `scenario_walk.py --witness-for <owns>` line
  in sections 4 and 5 are void. Each dispatch names its witness list below; a file on the slow list
  (`scripts/slow_tests.json`) or of the canon-only class is never run whole - its rows are checked by a narrow call of the
  changed test functions and the file is a report line "not run locally: <file>, canon judges".
- **N5 (7b-A helper, read by 7b-B).** A case reads `"red"` when ANY coded reading is a failure verdict; `"unanswered"` only
  when there is no red and some reading is `""`. (A red is never hidden behind an unanswered sibling.)
- **N6 (7b-B, and 7c item 5).** POSITION in `ledger.py::plan_row_state`: the `"read"` -> `not_executed:report_unread` branch
  sits immediately before the `skipped` branch, AFTER the unconfirmed-expectation branch. INVARIANT: no failure, flaky, partial,
  error, unknown-word or unconfirmed-expectation word is hidden by `report_unread`. The same position holds for 7c's
  `not_executed:unprepared_walk`. Test entry in the plan-row table: read + an unconfirmed Then ->
  `not_verified:expectation_unconfirmed`.
- **N7 (7b-A builds, 7b-B reads).** ONE pure private classifier `contract._reading_of(verdicts) -> "" | "read" | "red" |
  "unanswered"` (rule of N5). `unread_case_reading` calls it per case, `check_delivery.unread_obligations` per obligation and
  adds only its coverage guards (oracle closed, design sufficient, gap text) on top. No second wording of the rule.
- **N8 (7b-B).** The road for `to_check` limitations: `C.bind_triage(C.triage_failures(facts["report"])[0],
  facts["triage"])["matched"]` over keys of kind `unread`, mapped to cases by the existing
  `check_delivery._failure_cases(key, failure, facts)` - no new matcher. Position note for 7b-A's `build_run_block` condition
  (F1): for a `file` contract with zero report rows it REPLACES `_file_verdict`'s `id_not_in_report`; the only readers are
  `run_history.py` (failed blocks) and the console count in `run_suite.py` - the builder confirms both by grep and reports.
- **N9 (7c).** The walk twin of `excused` carries the same guards as `unread_obligations`: `oracle_open` is False AND the gap
  text starts `not checked by hand: unprepared`. An unprepared walk with an open oracle stays `no` (`coverage red:` is kept).
  Test entry in the 7c assess table: unprepared walk, oracle open -> `no`.
- **N10 (7c).** The twin is named `unprepared_obligations(doc, report) -> frozenset`, beside `unread_obligations`; 7c's owns
  parenthetical for `check_delivery.py` gains `assess` (the union into `excused` happens at that call site).
- **F5 addendum (section 8).** `report_facts.EXECUTION_OUTCOME_STATES`: unchanged (`not_executed:report_unread` is
  `after_checks` and gives no reason text there).
- **N11 (7b-B; critic t-1293 Q1, taken 18.11.2026).** In `ledger.py::test_state`, on a row that `C.is_unread_row`, a bound
  verdict `FLAKY` with `fix_result: fixed` reads `not_verified_flaky`, not `passed_green`: its re-runs were unread too.
  INVARIANT: no branch of `test_state` reads green for a row whose result code never read. One entry in the
  `test_ledger.py` test-state table.
- **F-r4-1 residual.** Section 7 gains a live row beside L6: a `reporter: none` run with a failing test and exit != 0 - today's
  halt and the conductor; if a live run shows it, a node for option (b) is opened in U8.

Test rows - the budget each dispatch states (K6 of t-1272; added test lines must not exceed added code lines):
- 7b-A: 3 NEW parameterised rows (the `build_run_block` coding table in `test_s7_pretriage.py`; the driver row "S7 dispatches
  the analyst over unread, no code close, the brief names unread" in `test_story_run_s7.py`; the reducer row in
  `test_s7_null_outcome.py`) + about 7 entries in existing tables (7a predicate table, zero-row refusals, `multiple`, the two of N1).
- 7b-B: 3-4 NEW rows (ledger test state; ledger plan-row state - or one row with a "level" column; the trace gap word in
  `test_third_verdict.py`; the assess walk table in `test_check_delivery.py`) + about 17 entries.
- 7c: 0 NEW rows + about 12 entries in the 7b-B tables.
- NO own row (internal boundary or a duplicate of a driven door): `decide`, `brief`, "pretriage never closes",
  `unread_readings`, `unread_case_reading`, `_reading_of`, `unread_obligations`, `coverage_reasons` direct,
  `build_left_items` direct, `not_executed_findings` direct, `triage_reasons` direct, the temporal world "7b-B not merged".

Witness lists (each file once, after all edits):
- 7b-A: `test_s7_pretriage.py`, `test_triage_identity.py` whole; `test_s7_null_outcome.py` and
  `test_bug_records.py` (slow list) and `test_story_run_s7.py` (canon-only) - narrow call of the changed functions only.
- 7b-B: `test_ledger.py` whole; `test_third_verdict.py` and `test_check_delivery.py` (slow list) - narrow call only.
- 7c: `test_ledger.py`, `test_manual_evidence.py`, `test_unprepared_outcome.py` whole; `test_third_verdict.py` and
  `test_check_delivery.py` - narrow call only.

---------------------------------------------------------------------------------------------------------------------

## 0. Verdict t-1267 -> where fixed (K1)

| finding | file::function | behaviour after the fix | test row (keep file) | node |
|---|---|---|---|---|
| B1 rule 5 / S7 entry | `s7_pretriage.py::triageable_not_executed` rules 3 and 5 | rule 3 admits a deciding row with `status == "not_run"` AND `reason_code == C.REPORT_UNREAD_CODE`; rule 5 "one manual target, one observation, or one `unread` target" | `test_s7_pretriage.py` predicate table: "unread only -> True", "unread on a passed row -> False", "not_run without code beside unread -> False" | 7b-A |
| B1 empty reasons -> silent S7 close | `driver_stage_s7.py::failures_to_triage` (10-46) | appends `"results the run could not read " + names` when `targets["unread"]`; reasons never `""` over an unread target, so `stage_S7` 75 cannot close by code | `test_story_run_s7.py`: "reporter none, unread only -> analyst dispatched, no `s7.no_failures` close" | 7b-A |
| B1 zero-row triage accepted | `handoff_check.py::_no_failure_shown` (1349-1383) | after the results branch (1378-1379), before observations: `targets["unread"]` -> "work/run-report.json shows test(s) whose results the run could not read, which want your reading: <names>" | `test_s7_null_outcome.py` (keep, 5047): "zero-row triage over an unread target -> refused naming it" | 7b-A |
| B1 `told` / brief / why | `driver_stage_s7.py::stage_S7` 121 (`told` condition gains `left.get("unread")`, list gains `("unread", n)`); `s7_pretriage.py::brief` (270-283) gains `"results the run could not read " + names`; `s7_pretriage.py::decide` (233-236): a key of kind `unread` goes to `left` with why "the run's report could not be read by code; the analyst reads its log" BEFORE the `!= "manual"` branch; `pretriage` (370-372) `left` gains `"unread"` | analyst brief names unread targets with the right why | `test_s7_pretriage.py`: "decide: unread -> left, why names the log"; "brief lists unread"; "pretriage never `closes` with an unread target" | 7b-A |
| B2 ledger unreachable / NOT_EXECUTED -> factory `no` | `ledger.py::test_state` row block (1172-1182) | INSIDE the block, before 1182: `current_row` carries `C.REPORT_UNREAD_CODE` and `verdict == "NOT_EXECUTED"` -> `(REPORT_UNREAD_STATE, display)`; every other verdict keeps 1173-1182 (APP_BUG -> `failed:APP_BUG`); NO row -> unchanged `not_executed:` + `NO_RUN_RESULT` (1245) | `test_ledger.py`: "unread + analyst NOT_EXECUTED -> `not_executed:report_unread`"; "unread + APP_BUG -> `failed:APP_BUG`"; "unread, no row -> `not_executed:no result for this test in run-report.json`"; "declared reporter, report missing (no code) + NOT_EXECUTED row -> `failed:NOT_EXECUTED` unchanged" | 7b-B |
| B3 coverage_gap | `check_delivery.py::coverage_reasons` (1764-1795) + its call in `assess` (2648) + new helper `unread_obligations` | reader-side skip/re-word, `coverage_contract.py` untouched, `verified` False (§2 site D3) | `test_check_delivery.py`: "all instances unread + NOT_EXECUTED -> no coverage reason"; "one instance unanswered -> `coverage:` reason kept"; "APP_BUG on an unread instance -> `coverage red:` (product)"; "oracle open -> kept" | 7b-B (with B6) |
| B4 NOT_EXECUTED_NOT_RE_DERIVED + page/vocabulary | `check_delivery.py::not_executed_findings` (2013-2029); `agents/qa-failure-analyst.md:87`; `handoffs/vocabulary.yaml:98` | a NOT_EXECUTED row that `bind_triage` binds to a failure key of kind `unread` is skipped (no finding); every other NOT_EXECUTED row keeps `_code_row_ok`; page line 87 and the vocabulary meaning restated (§2 site A6) | `test_check_delivery.py`: "analyst NOT_EXECUTED bound to unread -> no finding"; "the same row unbound (another attempt) -> finding kept" | B4 code 7b-B; page/vocabulary 7b-A |
| B5 reducer archives | `finalize_task.py::reduce` 687 and `refresh` 727 | both conditions gain `or targets["unread"]` | `test_s7_null_outcome.py`: "unread-only report: bound analyst row kept, no `reason: no product failures`" | 7b-A |
| B6 triage_gap / multiple | `check_delivery.py::triage_reasons` 1468, 1473; `contract.py::bind_triage` 4820 | `kind in ("result", "unread")` at both lines (factory `triage:` words of `result`); `multiple` holds `key[0] in ("result", "unread")` | `test_check_delivery.py`: "unread with no row -> `triage:` reason (triage_gap)"; `test_triage_identity.py` (keep, 6561): "two rows on one unread target -> `multiple`" | 7b-B (`triage_reasons`), 7b-A (`bind_triage`) |
| B7 owns | node owns below | every file B1-B6, F1-F8 need is owned by 7b-A or 7b-B; the reducer and `coverage_reasons` are no longer non-goals | - | both |
| F1 producer edges | `run_suite.py::build_run_block` (470-606) | code set only when ALL: row `status == "not_run"`; summary has `no_junitxml`; `summary["reporter"] == "none"`; `summary["execution_status"] == "not_executed"`; no `summary["blocked"]`; the summary has no report rows. Placed after the status branches (511-540), BEFORE 541, so `PROJECT_TIMEOUT_CODE` overwrites it (timeout wins; `s5_precheck.py:3732` reads it, critic's read) | `test_s7_pretriage.py` producer rows from summary fixtures: "not_executed + none -> coded"; "inconclusive -> not coded"; "broken_run (exit != 0) -> not coded"; "timeout -> `PROJECT_TIMEOUT_CODE`"; "node-id block -> not coded"; "reporter junit-xml, file missing -> not coded"; "inferred reporter -> not coded" | 7b-A |
| F2 one item per case | `check_delivery.py::build_left_items` (2155-2272) | unchanged keying (one row per case); the 7b rows assert one item per CASE with kind `run_unread` | `test_check_delivery.py`: "two unread instances of one case -> one item" | 7b-B |
| F3 plan_row_state position | `ledger.py::plan_row_state` (679-918) | §2 site D2: red reading joins `failed` at 819; `not_executed:report_unread` after `error` (841), before the unknown word (847) | `test_ledger.py`: "plan row, all instances read NOT_EXECUTED -> `not_executed:report_unread`"; "one read APP_BUG -> `failed:APP_BUG`"; "unanswered -> `skipped:inconclusive run` unchanged"; "partial beside -> `partial`" | 7b-B |
| F4 producer rows of `_case_chain` | `test_third_verdict.py` story world (`G_walk`, 929-931 critic's read) | rows named in §2 site D4 | `test_third_verdict.py` | 7b-B |
| F5 reader list | §8 below (each reader with a verdict) | - | - | both |
| F6 trace vs red | `check_traceability.py::_case_chain` (38-113) + `walk` (191-) | reads the bound verdict through `C.unread_case_reading`: red -> `executed_failed` (terminal, no gap; the ledger's red speaks alone); read -> `result:report_unread`; unanswered -> `result:not_run` unchanged | `test_third_verdict.py` rows (D4) | 7b-B |
| F7 axis 3 cell | `design/architecture.md` line 49 cell | edited in 7b-B's commit, which merges AFTER 7b-A (both halves true at that commit) | `python -B tools/architecture_index.py --check` | 7b-B |
| F8 section kind / ratchet | `agents/qa-failure-analyst.md` section "## Tools" (`<!-- kind: process -->`, line 67) | the paragraph is process text; `references/role-load.json` rows `ratchet_tokens.qa-failure-analyst` (21557) and `process_ratchet_tokens.qa-failure-analyst` (19507, slack 0) are set to the measured value by `python -B ai-packages/qa-factory/scripts/role_load.py --all`, and the commit names the raise (AR-20) | role_load output before/after in the report | 7b-A |

Forks the draft could not close: F-r4-1 (a red `reporter: none` run exits non-zero and is `broken_run`), F-r4-2 (bug draft
reproduction on an unread target), F-E7-1..3 (§11).

---------------------------------------------------------------------------------------------------------------------

## 1. Architecture, owners, variety walk (for 7b-A, 7b-B, 7c, E7)

### 1.1 AR-n touched and the change check (copied into each node's DoD)

| AR | how | change check |
|---|---|---|
| AR-13 | one definition of a target (`contract.triage_targets`, set `unread`), one binding (`bind_triage`), one reading of an unread case (`contract.unread_readings` / `unread_case_reading`, new) read by ledger, traceability and delivery; one constant `C.REPORT_UNREAD_CODE` | no reader restates "row is unread" outside `contract.py` (critic Q6 grep `REPORT_UNREAD_CODE` -> only contract, run_suite producer, tests) |
| AR-22 | producer `run_suite.build_run_block` field `reason_code: report_unread`; every reader of `triage_targets`/`triage_failures` walked (§8) | a row per starved reader of t-1267 K2 (B1, B5, B6) green |
| AR-27 | an answered reading reaches delivery under its owner: `run_unread` (factory, F-17) or the analyst's red (product); no `not_executed_unproven`, no `NOT_EXECUTED_NOT_RE_DERIVED`, no factory `coverage_gap` for it | §3 walks; `test_check_delivery.py` rows name kind and owner |
| AR-28 / FR-59 | an unanswered target never reads `after_checks` (triage_gap + `result:not_run` + `not_executed:<NO_RUN_RESULT>` + coverage gap all stay); a code-less `not_run` never reads unread | §3 Walk 4 row |
| AR-1 | `run_unread` and its states/gaps are rows of `references/delivery-verdict-kinds.json`; no word list in code | diff adds no tuple of runner/language words to `.py` |
| AR-19 | S7 entry and delivery `run_reasons` read the same 7a predicate (unchanged twin) | named in commit |
| AR-20 | the analyst's ratchet rows rise by the measured amount, named | role_load output in report |
| AR-29 | checks altered below; code checks shape and joins, the analyst judges the log | census rows: none added; builder runs `test_judgment_census.py` and stops with a question if a unit needs a row |
| AR-3, AR-16, AR-17, AR-24, AR-25 | node E7 (§5) | E7 DoD |

### 1.2 Checks added or altered (owner, census class)

| unit | change | owner | census |
|---|---|---|---|
| `run_suite.build_run_block` | writes `reason_code: report_unread` under F1's condition | data | none added |
| `contract.triage_targets` / `triage_failures` / `bind_triage` | set `unread`, kind `unread`, `multiple` widened | data (shape) | none added |
| `contract.unread_readings` / `unread_case_reading` (new) | join of a coded row to its bound triage verdict | data (join); the verdict itself is the analyst's judgment, accepted at S7 by the consumer road | none added |
| `s7_pretriage.triageable_not_executed` (7a) rules 3, 5; `decide`; `brief` | admit / route unread | data | none added |
| `driver_stage_s7.failures_to_triage`; `handoff_check._no_failure_shown` | name unread | data | none added |
| `finalize_task.reduce` / `refresh` | count unread as a target | data | none added |
| `ledger.test_state` / `plan_row_state` | `not_executed:report_unread`; red from the bound verdict | data | none added |
| `check_traceability._case_chain` | `result:report_unread` / `executed_failed` from the bound verdict | data | none added |
| `check_delivery.triage_reasons` / `not_executed_findings` / `coverage_reasons` / `unread_obligations` (new) / `build_left_items` | B6, B4, B3, `to_check` | data | none added |
| 7c units | K4 of the verdict | data | none added |
| E7 trigger (fork F-E7-1 a) | reads a typed need + a registry state | data | none added; builder checks |

Commit lines: `architecture:` and `judgment:` in the form `tools/architecture_gate.py` checks (the one carrier; not copied);
`judgment: none` always carries ` -- <why>`.

### 1.3 Variety walk (architecture.md § A)

- axis 3: held by key|role -- `run.reporter` + the failure analyst; unknown value -> reporter `none` with exit 0 and no report: instances are the analyst's `unread` targets at S7, delivery says `run_unread` (`after_checks`) or the analyst's red; reporter `none` with exit != 0 stays `broken_run` and the S6 halt (F-r4-1); a declared reporter whose file is missing keeps the refusal and `no`
- axis 7: held by key|role -- registry key for another instance (E7, new) + the runner's judgment of the need; unknown value -> nothing started, the one question at the moment of need (F-E7-1), the case handed with what was tried on "no"
- axis 2: held by role -- the runner/agent; unknown value -> unchanged by 7b; 7c lets an unprepared walk speak as `unprepared_walk`; E7 "another instance of the stand or device" (no platform word)
- axes 1, 4, 5, 6, 8, 9, 10, 11, 12, 13: n/a -- no site of 7b/7c/E7 reads the product language, flow, requirement source, delivery target, host, people, artifact language, task size, check kinds or project age

No `narrows` line; F-r4-1 is returned as a fork because option (a) leaves the red-exit no-report run on today's halt.

---------------------------------------------------------------------------------------------------------------------

## 2. Sites (replace r3 §2 r4 "Target, 7b", its 7b edges, invariant and 7b tests)

r3 §2 r4 "Now (read)" and "Target, 7a" stand. Names: `REPORT_UNREAD_CODE = "report_unread"` in `contract.py` (the reader's home;
`run_suite.py` reads `C.REPORT_UNREAD_CODE` - builder greps that `run_suite.py` imports `contract`; if it does not, the constant
sits in `launch_check.py` beside `PROJECT_TIMEOUT_CODE` and `contract.py` imports it - one definition either way);
`REPORT_UNREAD_STATE = "not_executed:report_unread"` in `ledger.py` beside `HANDED_STATE` (37); gap `result:report_unread`; kind
`run_unread`.

### Group A - the target and S7 (node 7b-A)

**A1 `run_suite.py::build_run_block`** - F1 row of §0. Invariant: a row is coded only when the run itself reported nothing it could
read and exited 0; a row with any report row, a halted or inconclusive run, or a declared/inferred reporter is never coded.
Error direction: toward NOT coding (an uncoded `not_run` keeps today's refusal and `no`). Both worlds: blocks written before carry
no code and read as today; the next run of the instance creates the field.

**A2 `contract.py`**
- `triage_targets` (4595-4691): new set `unread` in `out`; in the result loop, a row with `result_status(row) == "not_run"`
  and `str(row.get("reason_code") or "") == REPORT_UNREAD_CODE` adds `names[0]` to `unread` and its spellings to `all`;
  NOT to `names` (the per-failure unit `triage_failures` turns into kind `result`, 4727-4736). A coded row with no name -> a note
  in `unnamed`. A coded row whose status is not `not_run` -> nothing (adversarial: `passed` + code).
- `triage_failures` (4694-4752): after the result loop, one loop over `current_results` rows that `triage_targets({"current_results":
  [row]})["unread"]` names: `add("unread", names, ids, attempt, old=...)` exactly as the result loop computes them (4729-4736).
- `bind_triage` 4820: `multiple` = keys with `key[0] in ("result", "unread")`.
- NEW `unread_readings(report, rows) -> dict`: `{instance name: verdict}` for every `unread` failure: the verdict of its ONE bound
  row (`bind_triage(...)["matched"]`), `""` when none, several, or ambiguous. Never raises (exception -> `{}`).
- NEW `unread_case_reading(report, rows, case, cfg=None) -> str`: over the current result rows whose case keys (the key expression
  of `run_results`, 4472-4473, factored into one private helper both call - AR-13) name `case` by `case_matches`: `""` when none of
  them is coded or any of them is NOT coded (a mixed case keeps its rolled-up word); `"red"` when any coded row's reading is a
  verdict other than `NOT_EXECUTED` and none is `""`; `"read"` when every reading is `NOT_EXECUTED`; `"unanswered"` otherwise.
  Error direction: toward `"unanswered"`/`""` (the caller keeps its `no`); `"read"` only when every instance has its own row.

**A3 `s7_pretriage.py`** - predicate rules 3 and 5 (§0 B1); `decide`, `brief`, `pretriage.left` (§0 B1 row). Position invariant
of `decide`: the `unread` branch sits after the bound/competing checks (226-232) and before the `!= "manual"` branch, so an
answered unread target is never re-left and no code row is ever written for one (`_code_row` is reached only by `manual`).

**A4 `driver_stage_s7.py`** - `failures_to_triage` reason; `stage_S7` `told`. Comments 87-93 (7a's restatement) add "or an
`unread` target".

**A5 `handoff_check.py::_no_failure_shown`; `finalize_task.py` 687, 727** - §0 B1, B5.

**A6 role text** - `agents/qa-failure-analyst.md`: line 87 is REPLACED by one paragraph in the same `## Tools` section (kind
process): "NOT_EXECUTED is code's word for a manual check that did not answer, and yours for a test whose results the run could
not read (an unread target, named in your brief): read that run's log (the summary its run block names, its `log_tail`) and write
one row - `NOT_EXECUTED` with `limitation` quoting what the log shows ("the log reads as passed: <quote>" or "cannot tell:
<why>"), or the failure verdict the log shows, with the fields that verdict requires. Never call it passed." No platform word.
`handoffs/vocabulary.yaml:98` meaning: "the check did not answer: code writes it at S7 for a manual check whose own record says what
stopped it; the analyst writes it for a test whose results the run could not read, quoting the log". Premise before code
(r3 item 9, kept): one run of the analyst's form check over a `NOT_EXECUTED` row on an unread target; a refusal stops the node.

### Group D - delivery (node 7b-B; B3 and B6 together)

**D1 `ledger.py::test_state`** - §0 B2. Invariant: the ledger never says `after_checks` for a reading nobody made; every failure
verdict keeps its red.

**D2 `ledger.py::plan_row_state`** - (i) at 819: `failed` also holds each case whose outcome word is `not_run` and
`C.unread_case_reading(report, C.triage_rows(triage), case, cfg_u) == "red"`; `_verdict_for_cases` (1005-1014) then reads the bound
row's verdict. (ii) after the `error` branch (839-841), before the unknown-word branch (847): cases whose word is `not_run` and
reading `"read"` -> `(REPORT_UNREAD_STATE, ", ".join(cases))`. Position invariant: no failure, flaky, partial or error word is
hidden (all above), `passed_green` stays unreachable, and an `"unanswered"` case keeps `skipped:inconclusive run` (857-859, verdict
none - test_state and the trace carry the `no`). Error direction: toward the old reading.

**D3 `check_delivery.py` coverage** - NEW `unread_obligations(doc, facts) -> (excused, red)` (frozensets of obligation ids): an
obligation of `doc["coverage"]["obligations"]` with `execution_state == "inconclusive"`, non-empty `instance_ids`, every id a key
of `C.unread_readings(facts["report"], facts["triage"])` with a non-empty verdict: all `NOT_EXECUTED` AND `oracle_open` False AND
`design_assessment == "sufficient"` AND `gap == "current sufficient evidence incomplete"` -> `excused`; any other verdict (and no
`""`) -> `red`. `coverage_reasons(doc, handed_rows_of_plan=frozenset(), excused=frozenset(), red=frozenset())`: an id in
`excused` -> skipped (the item is the ledger's `run_unread`); in `red` -> `"coverage red: " + id + " - the failure analyst read a
failure in the run log"` (family `coverage red:`, product, as RD1-21 1771-1773 routes it). `assess` 2648 passes both. Edge: any
instance unanswered, `failed`, oracle open, another gap text -> the reason stands as today. `verified` stays False
(`coverage_contract.py` untouched). Error direction: toward the gap. 7c extends `excused` (one parameter, one road).

**D4 `check_traceability.py::_case_chain`** - new keyword `triage_rows=None` on `_case_chain`, `outcome_for_case`, `gap_of_case`;
`walk` passes `C.triage_rows(C.load_json(C.artifact(artifacts, "triage.json")))`. In the branch 87-92, before line 92: when
`result == "not_run"` and `triage_rows is not None`: reading `"red"` -> `("executed_failed", f"{case}: failed (the failure analyst read
it in the run log)", "")`; `"read"` -> `("", f"{case}: the run's results could not be read by code; the failure analyst read the log",
"result:report_unread")`; else line 92 as today. `None` (every caller that passes nothing) -> today. Invariant: PASSED/FAILED
branches above untouched; only an all-coded `not_run` case moves. Tests (`test_third_verdict.py`, `G_walk` world): all rows coded +
NOT_EXECUTED rows -> `result:report_unread`; + APP_BUG on one -> no gap (executed_failed); coded, no row -> `result:not_run`;
one coded + one passed instance -> `result:partial`; table row `result:report_unread -> run_unread -> after_checks`.

**D5 kinds file** - `kinds.run_unread = {"verdict": "after_checks", "owner": "factory"}` (F-17); `ledger_states
["not_executed:report_unread"] = "run_unread"`; `trace_gaps["result:report_unread"] = "run_unread"` (exact keys win over the
`not_executed` / `result` prefixes, `delivery_verdict.py:147-156` critic's read); one note sentence.

**D6 `check_delivery.py` triage, findings, items** - B6 (1468, 1473); B4 (`not_executed_findings`: skip a row bound to a key of kind
`unread`); `build_left_items`: before the `elif meta.get("path")` branch (2263), `elif "run_unread" in item["kinds"]`: `to_check` =
"the run's results could not be read by code; what the failure analyst read in the log: <limitations of the bound rows, joined>;
to make it count, set run.reporter and run.report_path in qa-factory/config.json" (FR-37: the config path is the one the code reads;
builder confirms `report_path(cfg)` reads `run.report_path`). Not `human_text`-exempt: it obeys `references/human-questions.md`.

**D7 `design/architecture.md` line 49 axis 3 cell** - replace "reporter `none` records a green run as not executed, silently" with
"reporter `none` with no report: its tests are the failure analyst's triage targets and reach delivery as items left with the person
or as the analyst's red; a non-zero exit stays a halted run".

Edges (7b, both nodes): reporter declared, file missing -> no code -> refusal and `no` as today; inferred reporter -> no code; blocks
before 7b -> no code; no analyst row -> S7 form refuses by name (`_untriaged_failures`, kind-agnostic 1340-1346), and if passed by a
person's word: `triage_gap` + `chain_broken` + `not_executed` + coverage gap (`no`); two rows -> `multiple` refused at S7 and in
`triage_reasons`; a stale row (another attempt) -> archived by the binding as today; code on a passed row -> not a target; a
report with zero rows -> predicate False (r3); 7b-A merged without 7b-B -> answered unread reads `failed:NOT_EXECUTED` ->
`not_executed_unproven` (`no`, factory) plus coverage gap: never a pass (temporal world, closed by 7b-B).
Invariant: `execution_status` never rewritten; code never turns a log into `passed` (FR-58); an unread target with no row never
reads `after_checks`.

---------------------------------------------------------------------------------------------------------------------

## 3. Walks after 7a + 7b-A + 7b-B (K2). Story: `reporter: none`, exit 0, no report, S6 completed

1. All automated, reporter none, analyst "looks passed": rows `not_run` + code; S7 predicate True (rules 1, 2, 3 coded, 4 vacuous, 5
   unread); `failures_to_triage` non-empty; `decide` leaves unread; analyst writes NOT_EXECUTED + limitation; form accepts; reducer keeps
   rows (727). Delivery: `run_reasons` [] (7a); `triage_reasons` none; ledger `not_executed:report_unread` -> `run_unread`; plan row the
   same; trace `result:report_unread` -> `run_unread`; coverage excused; no NOT_EXECUTED finding. Verdict `after_checks`, one item per
   case, owner factory (F-17). No factory `no`.
2. Mixed (manual check present), "looks passed": as 1 plus the manual case's own kinds. `after_checks` (or what the manual case says).
3. "Looks failed" (APP_BUG on an unread instance; reachable only with exit 0, F-r4-1): ledger `failed:APP_BUG` (red, product); plan row
   `failed:APP_BUG`; trace `executed_failed` (no gap, F6); coverage `coverage red:` (product); no finding. Verdict `no`, owner product
   only.
4. No row for one target: S7 refuses by name; past it by a person's word: `triage:` (factory), ledger `not_executed:<NO_RUN_RESULT>`
   (product), trace `result:not_run` -> `chain_broken`, coverage gap. Verdict `no`; no `after_checks` for the unanswered reading.

---------------------------------------------------------------------------------------------------------------------

## 4. Nodes 7b-A and 7b-B (replace r3 §6 stream 7b). Order: 7a merged -> 7b-A (after 5a when open: `run_suite.py`) -> 7b-B -> 7c

Each node: given = r3 (§1, §2 r4 Now/7a, §4) + this file (§0-§4, §8) + `design/factory-rules.md` whole + `docs/TESTING.md`.
Witness once after all edits. FR walk A-G in the report. Over 100 lines -> critic (one pass for the topic 7b+7c).

**Node 7b-A - the target and S7** (`architecture: AR-13, AR-22, AR-28, AR-20 -- ...`)
```
given: C:/QAFactory/forge-repo/.claude/worktrees/arch-docs/docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md (sections 1, 2 r4 Now and 7a, 4), C:/QAFactory/forge-repo/docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r4-7b-7c-e7.md (sections 0-4, 8), C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md, C:/QAFactory/forge-repo/docs/TESTING.md
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/run_suite.py (build_run_block only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/contract.py (REPORT_UNREAD_CODE, triage_targets, triage_failures, bind_triage multiple, unread_readings, unread_case_reading, the run_results key helper)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/s7_pretriage.py (triageable_not_executed rules 3 and 5, decide, brief, pretriage left)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_s7.py (failures_to_triage, the told list in stage_S7, comments 87-93)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/handoff_check.py (_no_failure_shown only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/finalize_task.py (reduce line 687 and refresh line 727 only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/agents/qa-failure-analyst.md (line 87 -> the paragraph of section 2 A6)
C:/QAFactory/forge-repo/ai-packages/qa-factory/handoffs/vocabulary.yaml (NOT_EXECUTED meaning only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/role-load.json (the two qa-failure-analyst rows only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_s7_pretriage.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_story_run_s7.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_s7_null_outcome.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_triage_identity.py
non-goals: execution_status; coverage_contract.py; manual_evidence.py; ledger.py, check_traceability.py, check_delivery.py, delivery-verdict-kinds.json, architecture.md (7b-B); run_suite.refuse_missing_executor (5a); bug_records.py (fork F-r4-2); quarantined test_run_suite_reports.py and test_traceability.py; any platform word
handoff: builder report with the witness, the analyst form premise run, the reader walk of section 8 (a verdict per line) and role_load before/after verbatim
edges: section 0 F1 producer rows; code on a passed row; nameless coded row -> unnamed; no analyst row -> S7 form refuses by name; two rows -> multiple; stale row -> archived; blocks before 7b -> uncoded; 7b-B not merged -> answered unread reads no (factory), never a pass
DoD: section 0 rows of 7b-A green in the four keep files; `python -B ai-packages/qa-factory/scripts/role_load.py --all` output attached and the raise named in the commit; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`
siblings: t-1267 K3 items 8, 9 (here); readers of section 8 (verdicts in report); s7_unbound/s7_fresh (kind-agnostic, n/a)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r4-7b-7c-e7.md
```

**Node 7b-B - delivery (B2, B3+B6, B4 code, F2-F4, F6, F7)** (`architecture: AR-27, AR-28, AR-1, AR-13 -- ...`)
```
given: as 7b-A
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/ledger.py (REPORT_UNREAD_STATE, test_state row block, plan_row_state lines 819 and 841-847)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/check_traceability.py (_case_chain, outcome_for_case, gap_of_case, walk)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/check_delivery.py (triage_reasons, not_executed_findings, coverage_reasons, unread_obligations, its call in assess, build_left_items run_unread branch)
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/delivery-verdict-kinds.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/architecture.md (axis 3 cell, line 49, only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_ledger.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_third_verdict.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_check_delivery.py
non-goals: coverage_contract.py (verified stays False); run_reasons (7a); stand_word (stream 6); contract.py (7b-A); the 7c unprepared branches
handoff: builder report with the witness and the four section 3 walks run through assess on fixtures (kinds + verdict verbatim)
edges: section 2 D1-D7 edges; temporal: needs 7b-A merged (merges main first)
DoD: section 0 rows of 7b-B green; the four walks of section 3 end as written; `python -B tools/architecture_index.py --check` green; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`
siblings: t-1267 K3 items 2-7 (here); gap_of_case/outcome_for_case callers (keyword default None: builder greps `gap_of_case\(|outcome_for_case\(` and lists them)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r4-7b-7c-e7.md
```

---------------------------------------------------------------------------------------------------------------------

## 5. Node 7c - unprepared walk speaks as `unprepared_walk` (F-16 a; verdict K4 taken as content; after 7b-B)

Facts (critic's probes, K4 i-iv): gap `result:none` for an unprepared walk; coverage leg fires (`coverage_contract.py:663-705`);
`plan_row_state` reads `passed_green` for an unprepared-only row (word `""`, `run_results` 4486-4488, `rollup_status([""]) == ""`
4421-4423, read this round); a stale walk keeps `unprepared` with `current_reason`. Lead fork decided: `walked: False` keeps
`chain_broken` (FR-59).

Items: (1) `manual_evidence.py` NEW `current_unprepared(report) -> {case: [obligation ids]}`: cases whose every current manual row has
`unprepared` not None, no `result`, no `current_reason`, and `walked` not False; `unprepared_rows` stays. (2) `check_traceability.py::
_case_chain` 87-92: `result == ""`, case in `current_unprepared`, no `current_results` row names it (`C.names_case`) -> gap
`unresolved:unprepared_walk`; every other `""`, stale, not-walked, `None` keeps its gap. (3) kinds: `trace_gaps
["unresolved:unprepared_walk"] = "unprepared_walk"`, `ledger_states["not_executed:unprepared_walk"] = "unprepared_walk"`, a note
sentence. (4) `check_delivery.py`: `unread_obligations`' twin for walks extends the SAME `excused` parameter of `coverage_reasons`:
an obligation id in `current_unprepared`'s set whose `execution_state` is not `failed`; `verified` stays False. (5) `ledger.py::
plan_row_state`: after the unknown-word branch (847-850), before unconfirmed (851): a case word `""` never reaches `passed_green`;
in `current_unprepared` -> `not_executed:unprepared_walk`, else `not_executed:no result recorded for this row's cases`. (6) the
docstring of `unprepared_records` (1885-1891) restated: the requirement no longer yields its own `chain_broken` for a walked unprepared
case. Invariant: no failure/flaky/partial/error word hidden; `passed_green` unreachable for a case with no result; a not-walked or stale
walk keeps `no`. Error direction: toward `no`.
```
given: C:/QAFactory/forge-repo/docs/tasks/specs/reviews/t-1267-u7-plan-7b-7c.md (K4), C:/QAFactory/forge-repo/docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r4-7b-7c-e7.md (sections 1, 5), C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md, C:/QAFactory/forge-repo/docs/TESTING.md
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/manual_evidence.py (current_unprepared only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/check_traceability.py (_case_chain branch 87-92)
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/delivery-verdict-kinds.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/check_delivery.py (the excused set of coverage_reasons, unprepared_records docstring)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/ledger.py (plan_row_state, the branch after 847-850)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_third_verdict.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_check_delivery.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_ledger.py
non-goals: coverage_contract.py; unprepared_rows; the 7b branches; walked False (stays chain_broken)
handoff: builder report with the witness and the assess run on the all-manual fixture before/after
edges: walked -> new gap; stale -> result:none; walked False -> result:none; no record -> unchanged; an automated row of the same case -> unchanged; failed execution -> coverage gap kept; empty obligation list -> nothing skipped
DoD: test_third_verdict.py table row and the five G_walk story rows; test_check_delivery.py "one unprepared walk, S6 completed -> after_checks without chain_broken/coverage_gap" and "stale twin -> no"; test_ledger.py "probe input -> not passed_green"; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`
siblings: unprepared_records (docstring here); get("unprepared") readers (critic: 20 hits read, the predicate is their one reader for this use)
```
`architecture: AR-22, AR-27, AR-28` (verdict K4).

---------------------------------------------------------------------------------------------------------------------

## 6. Node E7 - another instance of the stand or device: asked once, when needed (F-5 closed by the owner)

Owner, 17.11.2026: «спросить один раз, но не на онбординге, а тогда когда это понадобится». Five points (K5):

1. Who meets the need: the runner at S6 (`agents/qa-runner.md`: walks manual-agent cases; "Unprepared case: walk it like any other"
   line 51; `tried.md` line 65). Today the page has NO rule on preparation actions or another instance (grep `tried\.md|authoriz|
   prepar|instance|another` -i: lines 3, 16, 32, 45, 51, 62, 65, none about starting an instance; positive control: `tried.md` at 65).
   The only stand-touching authorization in code is the conductor's `stand_remedy` (`driver_conductor.py:182-192`: `config.driver.
   stand_remedy_authorized` or `AUTHORIZED` in the stand's `bring_up`) gating `stand_prepare` (`references/conductor-actions.json:157-
   171`, precondition at 165) - a stage-entry road for the ONE configured stand, not a second instance.
2. Road to the person (existing): the conductor seam `Driver.no_move` (AR-17; `driver_conductor.py:617`, r3's read, not re-read) ->
   the conductor's `ask_person` with a class (`driver_conductor.py::pass_to_person` 194-208, raises `Person` with `why_person` and
   `checked`) -> the one question form (AR-16, `references/human-questions.md`). The person's free words reach the executor through
   a "says/run" row of `references/conductor-actions.json` (model: the stand-lesson row, line 29, `project_knowledge.py lesson ...
   --words-file`). GAP: no road found in this round's reading that turns a runner's MID-S6 need into a seam call; the proven S6 roads are
   stage-entry `stand_check` (r10) and the S7 -> delivery "left with you" road. -> fork F-E7-1.
3. Where the answer lives and who reads it next: the answer registry `records/project-knowledge.json` (AR-3; one writer
   `project_knowledge.record`, one reader `state`; keys derived from `references/config-keys.json` section `knowledge`, 
   `project_knowledge.py:82-125`; writers `BY = ("conductor", "driver")` 130; role writes closed by the guard,
   `guard_pre_tool.py:1777-1786` and `references/stage-joints.json:2039`). New stand-scoped key (proposed `environments.extra_instance`,
   element = what the role wants to start in its own words, compare `exact`, value `{"authorized": true|false}`, state `known`), with a
   CLI verb and a conductor-actions row twin of line 29. Next story: the runner's brief gets one line beside the stand lessons
   (`brief_pack.py:2882` model, "Stand lessons"), and the trigger of F-E7-1 reads `state()` first: a `known` row (yes or no) is never
   asked again with the same text (FR-7). Registry vs config: fork F-E7-2.
4. What a "no" does: the runner does not start it; the case is recorded `unprepared` (`manual_evidence.py unprepared --not-walked
   <why> --observations-file <what it tried>`, r3 a2D1) with the need and the person's word; S7 triages it; delivery lists it
   `unprepared_walk` (`after_checks`, with 7c) with `tried.md`. A recorded "no" on a later story: the runner goes straight to that
   record, no question.
5. Role text (`agents/qa-runner.md`, process section; no platform word, P2): "When a case needs another instance of the stand or
   device than the one prepared: if your brief says starting one is authorized, start it with the project's own actions and write
   what you started in `tried.md`; if it says not authorized, or says nothing, do not start it - record the case unprepared, naming
   what you would start and why (`--not-walked`), with what you tried. The factory asks the person once and remembers the answer."

§1 for E7: AR-3 (registry key), AR-14/AR-13 (one writer/reader), AR-16, AR-17, AR-24 (the person's words to the recorder), AR-25 (a
row for the new state in `design/state-exits.md`, `revoke` its exit), AR-20 (`qa-runner` ratchet rows raise, named). Variety: axis 7
and axis 2 lines of §1.3. Census: the role text adds no check; the F-E7-1 (a) trigger is `data`, class shape, none added.

Node E7 is NOT dispatchable until F-E7-1 and F-E7-2 are decided; its parts then are: (E7-1) registry key row in `config-keys.json`
`knowledge` + `project_knowledge.py` verb + conductor-actions row + `state-exits.md` row + `test_project_knowledge.py` (keep, 4113)
rows (record yes/no, revoke, unknown -> asks); (E7-2) runner page paragraph + brief line (`brief_pack.py`) + `role-load.json`
`qa-runner` rows; (E7-3) the trigger of F-E7-1 (a) with a seam row in `test_no_move_seam_sites.py` (keep, 3224): "typed need, no
record -> one conductor call, one person contact"; "record known -> no call"; and the `dry_exits.py --check` row if it names a road.
DoD of each: its rows green; `scenario_walk.py --witness-for <owns>`; E7-2 a doc-dispatch witness with keys quoted before the run
(K1 `another instance of the stand or device`, K2 `the factory asks the person once`, K3 `do not start it`; K4 absent = negative
control).

---------------------------------------------------------------------------------------------------------------------

## 7. Live proof (FR-33), rows for `live-runs`

L6 (replaces r3's): a `reporter: none` run with exit 0: the analyst reads each instance's log at S7; delivery says `after_checks`
with one `run_unread` item per CASE, or the analyst's red. L7: an all-manual story with one walked unprepared case reads
`unprepared_walk` without `chain_broken`/`coverage_gap` (7c). L8 (E7): the first case needing another instance asks once; the next
story does not ask.

---------------------------------------------------------------------------------------------------------------------

## 8. Readers of every changed field or set (K6; designer rule 7)

`owns_readers.py` block: NOT attached to this dispatch; the Lead re-runs `python -B tools/owns_readers.py --paths <owns of 7b-A,
7b-B, 7c> --names triage_targets,triage_failures,bind_triage,reason_code,REPORT_UNREAD_CODE,_case_chain,coverage_reasons` at dispatch.
Hand grep (Grep, case-insensitive) `triage_targets\(|triage_failures\(|bind_triage\(|triage_row_for\(` over `scripts/`: 152 lines (tests
included); positive control in the same call: the definitions `contract.py:4595`, `4694`, `4778`, `5063`. Production readers, verdict:
- `driver_stage_s7.py:28` failures_to_triage -> changes 7b-A; `:336-337` s7_unbound/s7_fresh -> unchanged (kind-agnostic)
- `handoff_check.py:1340-1345` _untriaged_failures -> unchanged (kind-agnostic; `multiple` widened in contract); `:1373` -> changes 7b-A
- `finalize_task.py:683, 726, 733-734` -> changes 7b-A (687/727); binding unchanged
- `s7_pretriage.py:149, 165` (manual rows only) -> unchanged; `:216-218` decide -> changes 7b-A
- `check_delivery.py:1137-1138` _code_row_ok -> unchanged (manual keys only, 1140); `:1311-1321` thin calls -> unchanged; `:1424-1425`
  _triage_binding -> unchanged (by verdict; `_failure_cases` 1396-1412 reads names and the manifest for a non-manual kind, so an unread
  key finds its cases like a result key); `:1464-1499` triage_reasons -> changes 7b-B; not_executed_findings -> changes 7b-B
- `ledger.py:986, 1000` (`triage_row_for` via `_triage_row`; a `not_run` status is own-green, so the test binds as `("ask", ...)`,
  5088-5100) -> changes 7b-B (state only)
- `contract.py:2513-2516` _bound_triage_rows -> unchanged (an unread row is bound; blocked rows read from it are the analyst's);
  `:2595-2598` _instance_failed -> unchanged (`result` only: an unread target is not red - correct); `:4906` observation_duplicates ->
  unchanged (observation only); `:5103` triage_row_for -> unchanged
- `traceability.py:466, 632`, `factory_dashboard.py:912, 939` -> unchanged (display through triage_row_for)
- `judge_results.py:80` _failed_rows -> unchanged (reads `results`/`unnamed`; an unread row is not sorted: no red evidence)
- `retro_numbers.py:1419-1420` _triage_cause -> unchanged (an APP_BUG on an unread row maps to its cause; NOT_EXECUTED is no cause)
- `bug_neighbours.py:164-176` -> unchanged in code; a unit `f:unread:<name>` appears; the 7b-A builder confirms `_failure_facts` handles
  an unknown kind (else the line becomes a question)
- `bug_records.py:1024` no_run_target -> unchanged (an unread instance is held: not "no run target"); `:1049-1053` _walk_has_no_run ->
  fork F-r4-2
- `null_outcomes.py:153` comment -> unchanged
Other changed names: `reason_code` (Grep count over scripts: 201 occurrences / 44 files, mostly other vocabularies: gate rows,
telemetry, probes); run-row readers: `s5_precheck.py:3732` (timeout, critic's read) -> unchanged by F1 precedence; `run_history.py`,
`execution_request.py`, `coverage_contract.py`, `check_delivery.py` -> the 7b-A builder lists each with a verdict (not read here).
`delivery-verdict-kinds.json` -> read by `delivery_verdict.load_kinds` (owner words checked) and `test_third_verdict.py` -> 7b-B, 7c.
`architecture.md` -> `tools/architecture_index.py` (AR lines only) -> 7b-B. `role-load.json` -> `role_load.py`, `test_role_load.py`
(K10 shape rows) -> 7b-A, E7-2. Readers in `tools/`, `.githooks/`, `.claude/`: the tool block's job (KNOWN MISSES).

---------------------------------------------------------------------------------------------------------------------

## 9. Readers of the test files: `test-layers.json` keep rows (all < 7209 = keep): test_bug_records 376, test_check_delivery 531,
test_ledger 2831, test_no_move_seam_sites 3224, test_project_knowledge 4113, test_role_load 4651, test_s7_null_outcome 5047,
test_s7_pretriage 5054, test_story_run_s7 6265, test_third_verdict 6516, test_triage_identity 6561.

## 10. Small choices closed

- 7b split into 7b-A (S7 side) and 7b-B (delivery) by file ownership; F7's cell goes to 7b-B (merges last).
- `REPORT_UNREAD_CODE` homed in `contract.py` (reader's home), with the stated fallback.
- `unread` names stay out of `names` (K5 note) and join `all`.
- `unread_readings` / `unread_case_reading` as the one join (AR-13) for ledger, trace and delivery.
- `coverage_reasons` gains two parameters (`excused`, `red`), 7c extends `excused` (one road).
- Unanswered plan row keeps `skipped:inconclusive run` (verdict none; the `no` comes from test_state/trace/triage).
- The analyst paragraph replaces line 87 (net text smaller than a new section).

## 11. Forks (returned)

- **F-r4-1** a `reporter: none` run whose tests fail usually exits non-zero -> `execution_status` `broken_run` (`run_suite.py:1365-1367`)
  -> F1 leaves it uncoded -> S6 halt as today. This is a pair of requirements in conflict (F1's honest halt vs F-15's "the analyst reads,
  a red travels as a red"). (a) keep F1: only exit-0 runs are read; a red-exit no-report run halts and the conductor meets it (no
  regression, axis 3 half-open, said in the axis 3 cell); (b) also code `broken_run` + reporter none + no report, and let 7a's predicate
  admit it (changes the meaning of "a run that halted is never triaged": a broken launcher and red tests become the analyst's to tell
  apart from the log). Recommend (a) now and (b) as a new node after a live run shows the case (U8 territory). Cost of (b): the S7
  entry invariant and `run_reasons` change meaning; a plan critic pass.
- **F-r4-2** an APP_BUG bug draft on an unread target meets the red-now fact (`bug_records.py::_current_red_problem` 988-1004: current
  row `not_run` -> `R_NOT_RED_NOW`). (a) `_walk_has_no_run` (1039-1053) also holds kind `unread`, so a `walk` reproduction entry is not
  refused for red-now (non-walk entries still are); (b) unchanged: reproduction receipts are optional, the draft ships with its triage
  row. Recommend (a) (same class as manual/observation, F5); adds `bug_records.py` and `test_bug_records.py` (keep, 376) to 7b-A.
- **F-E7-1** the moment and road of the one question (no mid-S6 runner-to-seam road found). (a) the runner records the case
  `unprepared` with a typed need (new closed field on `manual_evidence.py unprepared`, e.g. `--needs another_instance`); at the S6 ->
  S7 boundary the driver reads current manual records with that need and no registry row, and calls `no_move` once (site fallback = the
  one question, doors "start it" / "I will check these cases myself" / "stop"); the conductor records the answer through the new
  conductor-actions row; on "start it" the existing rework row (`conductor-actions.json:8`, `controller.py --operation rework --stage
  S6 --cases <ids>`) re-walks those cases. New code: the trigger site (needs a scout read of the S6 close / S7 entry first) + a
  manual_evidence field. (b) no question during the run: the need travels as an `unprepared_walk` item to delivery and the person's
  gate B answer is recorded to the registry by the conductor - asked once, at the first moment a person meets the result (later than
  "when needed"). (c) the runner's turn ends quoting the need (like s5.md:144 for 5a) - unproven road (r3 D-15 class). Recommend (a);
  cost: one driver site, one manual_evidence field, a dry_exits row, one scout.
- **F-E7-2** where the answer lives: (a) the answer registry key (AR-3 "a fact only a person's answer can give"; words kept; one writer;
  no onboarding question; revocable); (b) a config word like `stand_remedy_authorized` (driver_conductor.py:186) - a config key is
  "asked at onboarding" (AR-3), which the owner excluded. Recommend (a).
- **F-E7-3** scope of one answer: per stand (stand-scoped registry key) or per project. Recommend per stand (another stand may differ);
  the text says which stand.

## 12. Reading trail

Read this round: r3 (lines 1-1035, the header block 58-77 first); verdict t-1267 (whole); the universality brief (whole).
`driver_stage_s7.py` 1-135; `handoff_check.py` 1330-1389; `finalize_task.py` 676-755; `contract.py` 2506-2530, 2595-2619, 4411-4530,
4595-4829, 4895-4914, 5063-5105, Grep `^(TRIAGE_VERDICTS|EXECUTION_STATUS|RUN_WORDS_KNOWN|DELIVERY_REASON_OWNERS)`; `ledger.py` 679-923,
976-1025, 1160-1254, Grep constants (37-54, 1005, 1085); `delivery-verdict-kinds.json` whole; `check_delivery.py` 1120-1164, 1280-1324,
1396-1412, 1415-1514, 1661-1722, 1755-1804, 1880-1911, 2005-2034, 2155-2273, 2594-2673, 2725-2746; `coverage_contract.py` 590-714;
`s7_pretriage.py` 1-70, 195-385; `check_traceability.py` 1-127, 116-265; `run_suite.py` 466-565, 1350-1379, 2236-2385, Grep
`no_junitxml|reporter|PROJECT_TIMEOUT_CODE|_file_verdict`; `qa-failure-analyst.md` 60-95; `vocabulary.yaml` Grep NOT_EXECUTED (95-101);
`role-load.json` whole; `bug_records.py` 975-1102; `bug_neighbours.py` 155-178; `retro_numbers.py` 1405-1428; `judge_results.py` 60-89;
`qa-runner.md` Grep (lines above); `driver_conductor.py` 170-214; `conductor-actions.json` 1-29 (Grep), 150-180; `design/driver.md`
285-292; `architecture.md` 18-107, Grep answer registry; `project_knowledge.py` 1-130; Grep `project_knowledge\.py (lesson|role|account|
side)` (package, 20 hits); `test-layers.json` Grep of 14 file names. Greps behind negative claims, with controls: runner page has no
preparation rule (control `tried.md`); production triage readers (control: definitions). Not read (named where used): the 7a predicate
code (not in tree), `driver_conductor.py:617` no_move, `brief_pack.py:2882` body, the S6 close and S7 entry trigger site for F-E7-1,
`_failure_facts`, `report_path(cfg)` key, `run_history`/`execution_request` reason_code readers, `gap_of_case` callers. Budget: the
worker passed the 250K warn; reading stopped here.
