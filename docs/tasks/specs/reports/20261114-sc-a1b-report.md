# Builder report: node A1b (task t-680), branch wip/sc-a1b

Commit 34fabea (pushed). CI run started before the Lead's correction: 43534571634 (canon.yml on wip/sc-a1b). Not waited for beyond one read.

## What was done
- driver_stage_plan: deleted stage_S2, s3_author_done, stage_raise_questions, stage_critic_route, stage_after_critic, stage_critic_form, stage_critic_completion, ticket_rerun_critic; stage_S3 lost its critic branches (window logic untouched); completion_for lost the acceptor sub-branch of ticket_changed and the acceptor branch (s3_ticket_completion() now plain); docstring of stage_repair_owed and the section comment corrected.
- driver_machine: S1 and S2 share one explicit stage_simple branch in _act_prepare_stage (S3 -> stage_S3, others generic getattr); _wait_then_critic deleted; wait_existing_job and the record_running retry call _act_wait_existing_job.
- driver_dispatch: s3_ticket_completion lost `closes`.
- controller._s3_completion_gate: the `author_exit_owes_plan` block replaced by `if window != "labelling" and not complete: return` (see Questions 1).
- acceptance.author_exit_owes_plan deleted. stage_done: messages at :975 and :1551 now name S4, S6, S7.
- Deleted: handoffs s2-stage-critic-to-tester.yaml, s3-stage-critic-to-strategist.yaml (git rm), index.yaml rows, NE34/NE35, handoff_init tuple entries, open-vocabularies note, test-layers covers entries (2), features.json line, driver-layers rows (525-526, 529, 531-533, 535-536, 784; stage_repair_owed note corrected), test_stage_critic_route.py (git rm; quarantine row untouched).
- Tests: W2 (S1,S2 -> simple; S3, S4; plus a no-stage_S2 check), test_first_look_step rows (`at()` returns s3_window; windows between,w1,w1,w1,between,w1,between; hasattr stage_critic_route False), test_story_run_first_look :44, test_handoff :670 tuple (and its docstring), test_question_register :1928, test_field_producers negatives -> s4-case-critic-to-designer.
- Spec line numbers moved by +1 in test-layers.json (covers at 1702/1704), plans/features.json (1195), controller (`_s3_completion_gate` block 7531-7536); others matched.

## UPDATE after the Lead's answers (second commit)
- Q1 confirmed. Q2 granted: pins moved with the deleted rows (counts shrink, not a raise): test_null_outcomes.py PINS scope 19 -> 17; never_empty homes 20 -> 18; K0.4 tuple (19,...) -> (17,...); summary line "walked scope 19"/"never_empty 20" -> 17/18; K0.4 negatives "18, pinned 19" -> "16, pinned 17" and "20, pinned 19" -> "18, pinned 17"; K0.6 id list loses NE34, NE35; K0.12 eighteen -> sixteen (18 -> 16). test_handoff.py:2011 index count 23 -> 21. Edit of test_null_outcomes.py was made by a short python replace script (hygiene WARN, not a block); every replace matched exactly once.
- Witness: `python -B test_null_outcomes.py` -> `=== test_null_outcomes: 327/327 ok ===`; `python -B test_handoff.py` -> `=== test_handoff: 596/596 ok ===`.
- Q3 quarantined readers left as they are (the Lead tells the owner): test_controller_stage_acceptance.py:279-284 names `author_exit_owes_plan` (AttributeError in watch); test_handoff_init_author.py:16,43,85,87,89,122,125,132,166,174 names `s2-stage-critic-to-tester` (and :16 `s3-stage-critic-to-strategist`); test_rows_owed.py:46 and :112 name both deleted contracts. Comments: the one in driver_stage_plan.py (owned) deleted; NOT deleted (not my files): exit_gate.py:820 (`s3_author_done`), driver_stage_s6.py:344 (`stage_critic_completion`).
- Q4: `test_quarantine.py check` NOT witnessed (my background run returned rc=127, not a valid result).
- CI run 43534571634 of the first commit is not the witness of the second; packages-full not read.

## Questions for the Lead (not decided by me)
1. controller `_s3_completion_gate`: the spec deletes lines :7533-7537 only, which leaves the outer `if window != "labelling" and not complete:` with an empty body (syntax error). I kept the outer `if` with a bare `return`: identical to today's behaviour after A1a (author_exit_owes_plan was False for S3 once acceptance_by left); closing exits (stage_complete) and window 1 are validated/refused as before. Confirm or give another direction.
2. Two pins RED on my tree, outside my owns (found by running the non-slow witnesses; both fail on CI package-fast too):
   - `test_null_outcomes.py`: deleting NE34/NE35 lowers scope contracts 19 -> 17, never_empty homes 20 -> 18, drops NE34/NE35 from the K0.6 id list, K0.12 18 -> 16 and the K0.4 negative rows (18/20 -> 16/18). Raw: `FAIL the detector over the real package finds nothing wrong -- expected [], got ['scope contracts: 17, pinned 19']`, `=== test_null_outcomes: 317/327 ok ===`. Lowered pins (shrink-only, AR-20 style) need the file added to the owns.
   - `test_handoff.py:2011`: `FAIL the index counts twenty-three handovers -- expected 23, got 21` (my owns say `:670` only). One-number fix 23 -> 21.
   I left both unedited (rule: no widening of owns).
3. The DoD grep (`stage_critic_route|ticket_rerun_critic|author_exit_owes_plan|_wait_then_critic|s3_author_done|stage-critic-to` over scripts/*.py outside fixtures/stories) does NOT print nothing. Remaining hits, all outside my owns:
   - quarantined, spec section O says unchanged: test_controller_stage_acceptance.py:279-284 (author_exit_owes_plan, will go red in quarantine-watch), test_handoff_init_author.py (16,43,85-89,122-174), test_rows_owed.py (46,112) (contract names);
   - comments only: exit_gate.py:820 (s3_author_done), driver_stage_s6.py:344 (stage_critic_completion), driver_stage_plan.py (s4_critic_completion comment "as the S2/S3 rule");
   - my own file test_story_run_s3_windows.py:183,208,1008 (A1a's rows assign driver.stage_critic_route = lambda ...; now vacuous guards; W2-only owns) and the new test lines naming the deleted names as absent.
4. test-layers R6 "3 kept files import this cohort's files" and 12 forge-check features offenders (test_forge_metrics k1) are pre-existing on main (A1a report), not mine.

## Verification (witness)
`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <the 11 changed package paths>` printed 147 test files; 58 are not in slow_tests.json. Run locally from the tests dir, all rc=0 except the two in Question 2:
```
test_first_look_step 102/102 ok; test_story_run_first_look 27/27 ok; test_field_producers 880/880 ok; test_stage_closure 27/27 ok;
test_question_register 709/709 ok; test_handoff 595/596 (the :2011 count); test_null_outcomes 317/327 (Question 2);
+ 40 more non-slow files all rc=0 (test_controller_blocks 371/371, test_driver_stop_record 255/255, test_first_look 266/266, ...)
selftest.py --limits --lang: PASS limits, PASS lang -> === qa-factory selftest: 4/4 ok ===
test_judgment_census.py: === judgment_census: 25/25 ok ===  (no ratchet value changed or needed locally)
stage_guard.py --selftest: STAGE GUARD: no violations
```
Note: `scenario_walk` also printed `no scenario or keep row covers references/open-vocabularies.json: run the whole scenario layer` (scenario files test_scenario_cart_1/local_1_0108/local_1_arm_b/walk/world; slow, judged by canon).
Deletion grep: `git grep -n <names> -- scripts/*.py` printed the hits of Question 3; control `grep stage_review_exhausted driver_stage_plan.py` prints 587, 602, 703.
Quarantine: `test_quarantine.py status` before and after: identical (431 files, cohort 8073673 not ready, R2 and R6 fail as before). `test_quarantine.py check` was started on the committed tree and did not finish in my window (it scans history; > 10 min); the commit message carries the `quarantine-edit: test_stage_critic_route.py -- ...` line and the commit hook accepted it. Result of `check` NOT witnessed.

## CI (run 43534571634, read once)
package-fast: FAIL test_null_outcomes (Question 2). forge-check: FAIL test_forge_metrics k1 (pre-existing on main). install-smoke success. package-full (1) and (2): failure, logs not read (my log greps printed nothing).
Slow files touched, judged by the batch canon: test_story_run_s3_windows (W2), test_driver_layers (driver-layers rows), test_judgment_census (census), test_selftest_slow_tests, test_story_run_*, test_controller_*, test_handoff-related slow readers.

## FR pass
A refusals: no refusal text changed (stage_done usage messages name the live stages). B: n/a. C: FR-13 (contract rows are data; producer and readers deleted in one commit, but see Question 2/3 readers), FR-17 n/a. D: n/a. E: n/a. F: n/a. G: FR-30 English (`--lang` green); FR-54 siblings below.
architecture: AR-14, AR-17, AR-19, AR-20, AR-22, AR-25 as in the commit. judgment: none -- removed an inert judgment site.

## Siblings (not edited)
- `controller._closes_stage` (7566): for S3 it answers True for an accepted window-1 strategist (stage_closes_with; no S3 labelling exception, unlike the S5 plan (`s5_part_of`) and S7 investigation (`s7_part_of`) branches). Window 1 claiming completion is refused in `_s3_completion_gate`, but whether `finish --not-complete` of window 1 trips the "no role to close it" refusal path was NOT traced. Same class as A1a's stage_repairs finding.
- acceptance.py:1273 comment still says "the stage critic's verdict on S2-S4" (not on the A1b line list); the docstrings at the listed lines (1458-1461, 1516-1517, 1524-1528) did not name S2/S3, so nothing to change there.
- test_first_look_wiring.py:99 label (A1a note) unchanged.

Needed beyond the manifest: test_null_outcomes.py, test_handoff.py:2011, driver_stage_s6.py:344, exit_gate.py:820, tools/test_quarantine.py, docs/RUNBOOK.md section 7.
