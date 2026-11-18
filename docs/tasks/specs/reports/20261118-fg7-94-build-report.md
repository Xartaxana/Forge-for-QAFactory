# FG7-94 build report (t-1490, builder)

Branch worktree-agent-a299857de56e6566f; origin/main merged first ("Already up to date": FG7-90/91/92 were in it). All changes STAGED, nothing committed (the Lead commits; ci_read.py, wave.py, session_context.py and their tests are mechanism files). This file sits in the worktree copy of the handoff path (the harness refused the shared-checkout path).

## Plan items
- A1 DONE `tools/ci_read.py`: `cmd_push_jobs` in `make_commands` and `main_push_jobs(root, sha)` (D2); `run_state`, `_state_word`, `cmd_run_state` untouched (diff has no line of them).
- A2 DONE one writer `ci_read.main_red_write` (lock `main-red` 10 s, temp file beside it + `os.replace`). Grep of `state.json|write_text|os.replace` in ci_read.py: lines 605-613 (inside main_red_write) and 839 (the `launch` stamp, a different file).
- A3 DONE constants MAIN_WINDOW 30, GRACE_NEW_S 120, NONE_UNKNOWN_S 900, PENDING_STALE_S 5400, HISTORY_MAX 50, NAME_MAX 60, LINE_MAX 300, FLAKY_ID_MAX 200, LAUNCH_MIN_S 300 as module constants; `main_red_tip_state`, `main_red_fold`, `main_red_refresh`.
- A4 DONE `ci_read.main_red_line` is the one formatter; `session_context.main_red_lines` and the CLI (no subcommand) both call it.
- A5 DONE `session_context.main_red_lines`: reads, then `main_red_launch` (detached); any exception = `MAIN CI: unavailable (...)`; placed right after `test_quarantine_line`.
- A6 DONE `wave.py`: `Wave.record_tip` after each successful push (merge tip, piles tip when different, journal tip); `finally` in `run()` launches after `main-merge` is released and only when something was pushed. `registry_preflight_lines` now returns the red check ids, passed as `preflight=` (F8).
- A7 DONE `.github/workflows/canon.yml.proposed` (see deviations 1-2). Probe below.
- A8 DONE docstring of ci_read.py documents `main-red`. Commit form: tools/mechanism_gate.py wants one line `axis N (<key>): covered | queued | n/a <why>` for EVERY axis of docs/SIBLING_MAP.md (38 headings, labels from `## Axis N` titles) plus the tier line; the Lead writes them. My suggestion: axis 34 (one road for one action: `main_push_jobs` shares run_state's backend/token/_open) covered; the rest n/a.
- Tests: all 7 lines written, none dropped. Test lines +274 against code lines +~570 (git diff --numstat): within budget.

## Witness
`python -m pytest tools/test_ci_read.py tools/test_session_context.py tools/test_session_context_autoboot.py tools/test_session_context_layer_a.py tools/test_session_context_wiring.py tools/test_wave.py -q` (scope of scenario_walk --witness-for, 6 files):
`773 passed, 2 skipped in 642.27s (0:10:42)`
Narrow: `-k "main_red or main_push"` in test_ci_read: `46 passed`; test_wave `-k main_red`: `5 passed`.

D1 probe (hygiene point 7, byte copy aside, restore from it):
- sha256 canon.yml before: `b3f2c450a67874f19dcddd6c267af0b5eb4a2c4f19ef8d49623b40d7a6e48f46`; the aside copy: same hash.
- proposed copied over canon.yml; `pytest test_canons_dry_only_door_calls_dry_story_and_skips_checks_full_clock, test_the_canon_is_named_by_its_ref_and_its_clock_runs_after_a_red_job` plus the FG7-91 canon tests (e1, e2, e4): `5 passed in 0.14s`.
- sha256 canon.yml after restore: `b3f2c450a67874f19dcddd6c267af0b5eb4a2c4f19ef8d49623b40d7a6e48f46` (equal); git status shows canon.yml unmodified.
- Negative control: the two named tests against the live canon.yml: `2 failed`. Whole test_workflows.py against live canon.yml: `5 failed, 35 passed` (exactly the D1 rows). These 5 pass only after the Lead places canon.yml.proposed; place it in the same commit.

## Deviations / decisions differently from the card (reality vs card)
1. canon.yml already holds FG7-91's block (group `canon-push-<ref_name>` / `canon-dispatch-<run_id>`, push on `worktree-agent-**`). I kept FG7-91's group expression (card D1's expression is not used), added `main` to `branches`, and `cancel-in-progress: ${{ github.event_name == 'push' && github.ref_name != 'main' }}` (F1 a).
2. `checks` is skipped only for a push to main: `!inputs.dry_only && !(github.event_name == 'push' && github.ref_name == 'main')`. The card's `event_name != 'push'` would also drop `checks` from FG7-91's agent-branch push canons (forge-check does not run on those pushes). `full` and `clock` take `inputs.ref || github.sha` for every push (card D1; the agent-branch push canon now checks out the pushed sha, same bytes). `checks`, `dry-story`, `run-name` keep `github.ref_name`. forge-check.yml is NOT edited (dispatch non-goal overrides card section 10 F1(c)): its `cancel-in-progress: true` on main's push stays; a finding for FG7-90's pile.
3. Card gaps I closed minimally (please confirm): head `superseded` shows `unknown ... run cancelled`; `flaky add` of an id already queued is exit 1 `already on the flaky queue`, `flaky done` of an absent id exit 1; the fixer-nothing-left line is `MAIN GREEN at <sha8>; fixer <t> on the flaky queue; nothing left, close: python -B tools/ci_read.py main-red fixer --done <t>` (card's `...` read as the prefix up to `queue`); a run that is unfinished or has no jobs adds a pseudo job `<workflow>: run` (pending/cancelled) to `main_push_jobs`; `main-red` takes `--repo DIR` before the subcommand (the launch uses it).
4. Pending outranks red in tip state (card order D4): a tip with an open run is not final even if a job already failed.

## Needed from integration
- Place `.github/workflows/canon.yml.proposed` over canon.yml (with the test_workflows.py edit).
- test_wave.py got an autouse fixture `no_main_red` (record/launch stubs) so no existing wave test spawns a detached refresh.
- Tests that run the hook on a real clone (autoboot, layer_a, wiring) now start the MAIN line and a detached `main-red refresh` there (passed; the run may have written `<common dir>/main-red/` of this clone). CI judges them on a clean clone.

## Noticed analogs (not done)
- A multi-commit push (merge + piles commit) gives CI runs only for the top sha; the merge commit stays `unknown` in the window (harmless for the fold: only final tips speak, the range names it).
- forge-check.yml `cancel-in-progress: true` on main (card F1 c) is unchanged; same starvation class.
- CHANGELOG fragment: none (AR: none, no package file touched).

## Fix round (critic t-1497, F1-F7; builder questions 1-2 accepted; forge-check.yml untouched)
- F1 DONE `main_red_refresh.mutate` keeps tips recorded by wave after the log read (pushed_at >= newest row), appended to `order`. Row `test_main_red_refresh_keeps_a_tip_recorded_during_the_read_and_names_the_reason` (fails on the previous code: the late tip is dropped).
- F2 DONE the reason is stored on the tip (`why`); the line reads it, not the refresh-wide `error`. Same row (previous code printed `no verdict after 90 min`).
- F3 DONE rows: `test_main_red_tip_state` (10), two refresh tests, `test_main_red_record_and_launch` (record, error text, 300 s throttle, no-origin).
- F4 DONE `_spawn_detached` removed; `main_red_launch` calls `worktree_sweep.spawn_detached` (row monkeypatches it; the old copy ignored that).
- F5 DONE history `<job> closed at <sha8> (<task|direct>) [(fixed by fixer)]`; row `..._closes_with_the_task_and_renames_a_corrupt_carrier`.
- F6 DONE tasks deduplicated in order before the cut to 2; row `one-wave-one-task` in `test_main_red_line` (old: `J [t-100, t-100 +1]`).
- F7 DONE `_cmd_fixer`, `_cmd_flaky` split out of `main_red_cli`. R4 also done: a LockError in refresh is exit 1 with text.
- Witness (canon.yml.proposed unchanged; canon.yml sha256 still b3f2c450...6e48f46):
  `python -m pytest tools/test_ci_read.py tools/test_session_context.py -q` -> `594 passed, 2 skipped in 102.09s`
  `python -m pytest tools/test_wave.py -k main_red -q` -> `5 passed, 133 deselected in 38.49s`
- Left staged, not committed: the commit gate for mechanism paths (axis lines) is the Lead's; the report and tests are staged with them.
