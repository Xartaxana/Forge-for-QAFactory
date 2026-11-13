# FV1-30b N6 fix round (code critic F3, F4)

Worktree `.claude/worktrees/fv130b-n6`, branch `wip/fv130b-n6`, base head 3fceeec.

## Findings -> change -> row

- F3 (three copies of the filter block): one helper `window_record.word_kept(lines, window, task_root, dispatch_id) -> (kept, let_go)`,
  placed right after `word_let_go` in `window_record.py`. It builds the live index through `s5_precheck.live_word_index` (scope = the
  window's `scope_instances` or None), calls `word_let_go`, never raises: an index of None or any exception gives `(list(lines), [])`;
  empty input gives `([], [])` without asking for the index. Input order is kept. Callers, one line each:
  - `story_step.py finish`: `gaps, let_go = window_record.word_kept(gaps, loaded, task_root, args.dispatch_id)` (still inside `if gaps:`, before `_blocked_ids` / `_handed_no_instance` / `_derived_pair`; the let-go note line is unchanged).
  - `window_record.py run`: `problems, let_go = word_kept(problems, window, task_root, dispatch_id)` (still inside `if problems:`, before every derivability test).
  - `driver_dispatch.py Driver.window_gap`: `window_gaps = window_record.word_kept(window_gaps, record, task_root, dispatch or path.stem)[0]` (the `dispatch` argument stays as the first round left it; still before the "other gap -> ()" loop).
  Rows: n1-n4 unchanged and green (the proof the refactor kept behaviour). New rows on the helper, in
  `fv1_30b_n6_the_three_judges_read_the_one_survivor`: `word_kept: the let-go line leaves, the order of the rest is kept`, `... empty input`,
  `... an index that is raising / None: every line kept, none let go`, `... a window that is no dict: every line kept`.
- F4 (the `finish` note is not pinned): `finish_options` gained `succeed=True` (stand-ins for `apply`, the tail helpers and `_run`), rows
  `f4: finish, prepare and apply succeed: the let-go line is printed as a note` (`note: passed by the person's word: obligation_binding:A`),
  `f4: ... and only the let-go line, not the kept gap`, `f4: no word: no let-go note`. First run of the row failed (the stage_done stand-in was missing, so the notes printed without the prefix after a refusal); fixed by stubbing `story_step._run`. The optional "print at once when apply refuses" was not done (the verdict calls it optional; not in the Lead's edges).
- F6 as it concerns N6: the verdict's F6 is an N3 commit finding (AR-13 naming); nothing for N6 beyond the commit lines.

## Edge checks

- Helper is called BEFORE the "every gap derivable" test at all three sites (positions unchanged by the edit).
- Index None / exception -> `(all gaps, [])`; empty input -> `([], [])`; no import cycle (window_record imports s5_precheck lazily inside the helper; story_step and driver_dispatch import window_record lazily as before).
- A difference to the first round, noted: `import window_record` at two sites is no longer inside the `try`, so an import failure of `window_record` would now propagate (finish) or reach window_gap's outer `except -> ()`. `window_record` is a module of the same package and every row imports it; judged not a new risk in practice (not separately measured).

## Census

`window_record.py::run` stays `xref` / `intent` (the block moved into a non-blocking helper; `word_kept` raises nothing and refuses nothing, so it is not a census unit under `units_of`). No value changed, nothing rose. `test_judgment_census.py` is on `scripts/slow_tests.json` and was NOT run (CI judges it); the claim "no new unit" rests on reading `units_of` (units = blocking functions), estimate, not verified by a run.

## Grep: no copy of the block is left (with a positive control)

`live_word_index\(` in `story_step.py`, `driver_dispatch.py`, `window_record.py`:
```
window_record.py:1283:        index = s5_precheck.live_word_index(task_root, scope, dispatch_id)     <- the helper (positive control: the pattern finds it)
window_record.py:1353:                word_cache.append(s5_precheck.live_word_index(task_root, scope or None, str(dispatch_id)))   <- build()'s own cached index (Q4 of the verdict), not one of the three judges
```
`word_kept\(` finds the three call sites (story_step.py:2547, window_record.py:2161, driver_dispatch.py:960); `word_let_go\(` in the three scripts is only the definition and the call inside the helper.

## Siblings

The controller's own tier judges (N1): `controller.py:7107` and `:7507` call `word_let_go(..., self._s5_word_index(d))`. Verdict: different, not a fourth copy. They hand the controller's own per-dispatch cached index (`_s5_word_index`, `controller.py:7410-7418`, `d.get("scope")`, `d.get("id")`) and carry no try/except block (`word_let_go` never raises). They already share one composition (`_s5_word_index`) between the two sites. Not edited. `window_record.build` (`live_index`, `window_record.py:1346-1357`) is the same composition once more, cached per build call; it is the verdict's Q4 (memoise per window), left alone.

## Verification run (verbatim, after the last edit; from the package dir in a subshell)

`python -B scripts/tests/scenario_walk.py --witness-for scripts/story_step.py scripts/window_record.py scripts/driver_dispatch.py` printed the same 146 `keep` lines as the first round (no new file). Every NON-slow file of it, last line of each, plus `test_window_record.py` whole (it is slow-listed, run whole here, ~2 min):

```
=== window record: 573/573 ok ===                      (test_window_record.py, whole; first run after adding F4: 572/573 = the missing stage_done stand-in, fixed)
test_conductor_stop: === conductor stop: 48/48 ok ===
test_dispatch_identity: === test_dispatch_identity: 114/114 ok ===
test_s0_close_order: === S0 close order: 29/29 ok ===
test_stage_cards: === test_stage_cards: 163/163 ok ===
test_stage_closure: === stage closure: 19/19 ok ===
test_stage_of_dispatch: === test_stage_of_dispatch: 17/17 ok ===
test_state_exits: === test_state_exits: 142/142 ok ===
test_then_remainder: === test_then_remainder: 320/320 ok ===
test_quality_demand: === quality demand: 84/84 ok ===
test_codex_tool_guidance: === test_codex_tool_guidance: 217/217 ok ===
test_driver_stop_record: === test_driver_stop_record: 42/42 ok ===
test_exploratory_answers: === test_exploratory_answers: 107/107 ok ===
test_first_look_code_look: === test_first_look_code_look: 127/127 ok ===
test_first_look_step: === test_first_look_step: 102/102 ok ===
test_gate_question_form: === gate question form: 297/297 ok ===
test_human_questions: === test_human_questions: 291/291 ok ===
test_null_outcomes: === test_null_outcomes: 337/337 ok ===
test_person_owned: === person_owned: 82/82 ok ===
test_reference_window: === test_reference_window: 85/85 ok ===
test_s5_window_leftovers: === test_s5_window_leftovers: 148/148 ok ===
test_story_run_first_look: === test_story_run_first_look: 27/27 ok ===
test_story_run_monorepo: === test_story_run_monorepo: 71/71 ok ===
test_story_run_s6_w1_frozen: === test_story_run_s6_w1_frozen: 6/6 ok ===
test_walk_account: === test_walk_account: 190/190 ok ===
test_walk_lanes_parallel: === test_walk_lanes_parallel: 196/196 ok ===
test_walk_supply: === test_walk_supply: 261/261 ok ===
test_whole_list_sites: === test_whole_list_sites: 292/292 ok ===
test_probe_not_proved: 47 passed in 5.06s
test_probe_marker_judgment: 46 passed in 8.30s
test_probe_readers: 16 passed in 1.89s
test_probe_target_fact: 13 passed in 0.92s
test_login_need: 33 passed in 2.14s
PASS lang: no control byte left by an eaten escape sequence (FR-29)
=== qa-factory selftest: 2/2 ok ===                     (python -B scripts/selftest.py --lang)
```

Not run: `test_judgment_census.py` (slow-listed, CI judges it), the other slow keep files (60+, CI).

## Deviations

- The optional "print the let-go lines at once when apply refuses" (F4) was not done.
- `finish_options` of the first round's row function gained a `succeed` parameter (the n1-n4 calls are unchanged).
- No new test file; no changelog change (the existing fragment still describes the behaviour).
