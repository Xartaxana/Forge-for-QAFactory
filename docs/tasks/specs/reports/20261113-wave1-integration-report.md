# Wave 1 integration report (integrator builder, 13.11.2026)

Worktree `.claude/worktrees/wave1`, branch `integ/wave-1` -> `main`. Start: origin/main 7cf8c34.

## A. Merges

| # | branch | result | commit |
|---|---|---|---|
| 1 | `origin/wip/fv111` (da90045) | clean, no conflict | 9c6c4c0 |
| 2 | `origin/wip/p1a-carriers` | 2 conflicts, both resolved keeping both sides | 5f2a473 |
| 3 | `origin/wip/findings-lead` | modify/delete on `plans/PILES.md` + 1 content conflict | e900cc5 |

Hunks:
- `ai-packages/qa-factory/design/architecture.md` (axis 18 list): main's `- Detector: ... nightly CI job quarantine-check ...` line kept (it differs from the branch's "in the same job" wording: main's wins); the branch's two added sub-bullets (`known_red.py` loader, `lint_ratchet.py` second line) added above it. The branch's own duplicate Detector line dropped (same sentence, main's wording).
- `docs/SIBLING_MAP.md` (ratchet axis, row "The members"): the SAME row changed on both sides. Main's row kept whole (including `detector: tools/test_quarantine.py check in the nightly job quarantine-check`; the branch said "in `forge-check`" - main's wins); the branch's added text from `; since P1-a (spec ... §9 R7): the known-red ledger ... (a raise is --update with an added: reason in the commit)` appended at the end of the row.
- `plans/PILES.md`: does not exist on main (board removed by the owner's word 13.11); stays deleted (`git rm`), the branch's edit to it is dropped.
- `plans/piles/package-ci/batch-3-khrapovik-doors-only.md`: the same row PC3-4 was changed by both sides (main: `статус: сделано: a48dc25 (t-431)`; branch: older status text). Main's row kept; the branch's added row PC3-5 appended after it.
- Pre-commit "(d) tracked package file matches no feature" for 4 files of P1-a: registered under F16 (the feature that holds `test_field_producers.py`, which the four files serve; the P1-a commit messages 8580665, 535ce4d, b5c7765, 62421cf name that test): `scripts/tests/known_red.py`, `form_filler.py`, `fixtures/form-rounds.json`, `fixtures/form-fill-rules.json` in `plans/features.json`.
- No `tier:` demand by the commit-msg gate; no `piles-skip:` used. ARCHITECTURE_INDEX.md and AGENTS.md stayed current ("up to date" in the hook output).

## B. CI repair

Push pipeline of 7cf8c34 (43491974536): forge-check and package-fast failed. Canon 43492038420 on 7cf8c34: forge-check, package-fast, install-smoke, package-full (1) and (2) failed. Causes and fixes (round 1 = commit 5cc4f88):

| job | test | cause (one line) | wave commit | fix |
|---|---|---|---|---|
| forge-check | lint ratchet, 7 new pyflakes findings | unused import / variable / f-string without placeholders in test files | FV1-19 / FV1-4 / P1-v test edits (test_brief_pack, test_brief_pack_s5_plan, test_flow_requests, test_s5_precheck, test_window_record) | the 7 names removed / `f` dropped (no assertion changed) |
| package-fast, package-full | test_stage_joints K1-K14 (`exit checks: 4, pinned 8`, `exit:own` has no row) | `all_errors` wrapped every family in a local `own(...)` | 079dc63 (P1-v N0) | `scripts/stage_joints.py` `EXIT_WRAPPERS = ("own",)`: the walk reads the inner family call; both pins hold (8 families) |
| install-smoke, package-full | audit A1 `run_counters.py is reachable from nothing` ; test_audit_rules GOOD A1 | new reader script with no caller | 020f1a9 (P1-v N4) | `scripts/audit_factory.py` `CLI_SCRIPTS` += `run_counters` (with the reason) |
| package-full | test_driver_layers L1 (7 names, incl. `Driver.take_checks_line`), L3, L11 | 6 new names with no row; `self.__dict__` in `resume_kind_of`; `run_counters.py` imports `driver_timing` | 079dc63 / 71d7ca8 (P1-v), FV1-11 | rows added to `fixtures/driver-layers.json` (home = the defining module, exactly as the refusal text asks); `driver_runner.resume_kind_of` uses plain `self._resume_kind_table` / `_resume_kind_said` (same semantics) plus two ad hoc `attributes` rows; one `allowed_importers` row for `run_counters.py` (precedent: `story_step.py`) |
| package-full | test_task_root_parsers census | `run_counters.py` declares `--task-root` | 020f1a9 | `run_counters` added to `B_SCRIPTS` and the `table()` (it uses exact_options + story_cli) |
| package-full | test_field_producers: 4 `unknown row` + ledger not equal | FV1-19 made `obligation_refs` code-filled, so the 4 known_red rows `obligation_refs <- manifest_from_tests@{csharp,java,python,typescript} -> window_record.row_field_gaps` are no walk rows | FV1-19 | exactly those 4 rows removed from `form-rounds.json` known_red (a shrink; the test names them) |
| package-full | test_silent_passes K1; test_story_run_s6 C16b (2 rows); test_story_run_words (3 rows) | the words of a journal note now travel by a file (`--notes-file`) | a83b5f3 (FV1-4 N0) | tests read the words from the file (`owed_words` helper in test_story_run_s6; `kept.read_text` in silent_passes); `words_files` leaves the `driver-journalnote-*` files out (they are the log_append road, not a gate/review call) |
| package-full | test_story_run_refusals, test_infra_failure_stops/retries, test_story_run_loop_b_loop | `driver-runs.jsonl` now holds `process` rows (run record) | P1-v N1 | the tests read role/conductor lines (`kind != "process"`); round 2 also the conductor-line read at refusals line 158 |
| package-full | test_handoff `_plan_row_of` | the plan row is read from the body line `Plan row:` | a60160e (FV2-1) | fixture case gets the body line instead of a front-matter `plan_row:`; assertion value (TS-3) unchanged |
| forge-check (canon 43500141242) | tools/tests/test_role_carriers_one_owner.py `cost:queue` | CLAUDE.md rule 12 no longer holds "queue is kept FULL" | 63bbd5e (Lead, coordinator pace) | owner key moved to PROJECT.md item 12 (`в работе всегда шесть пишущих билдеров`) - round 2 (d53a327) |

K10-b / K10-c, A22 / A-K1: not red on the merged tree (no failure in either shard) - verified by the canon runs, not assumed. `Driver.take_checks_line` row: added (see above).

## Witnesses (local, narrow)

- lint ratchet: `lint ratchet: 36 findings, 36 in the baseline, 0 new, 0 stale`
- test_stage_joints `111/111 ok`; test_driver_layers `283/283 ok`; test_field_producers `912/912 ok`; test_task_root_parsers `416/416 ok`; test_handoff `602/602 ok`; test_silent_passes `326/326 ok`; test_infra_failure_stops `52/52 ok`; test_infra_failure_retries `55/55 ok`; tools/tests/test_role_carriers_one_owner.py `39 passed`
- audit_factory.py: `=== Result: clean ===`
- `python -B scripts/selftest.py --lang`: `=== qa-factory selftest: 2/2 ok ===`; `test_judgment_census.py`: `=== judgment_census: 24/24 ok ===`
- `python -B tools/piles.py check --all` ... `(д) form: ok (33 piles, 101 batches)`, `(е) findings: ok`, `piles check: ok`
- Not run locally (slow tier, CI's): test_story_run_s6, _words, _refusals, _loop_b_loop; their edits were judged by CI in round 1/2.

## Still red

- `test_story_run_s6_w1_frozen.py` (`w1_frozen_console`, canon 43492038420 and 43500141242): the live console of the frozen S6 manual story differs from `fixtures/s6-w1-frozen/console.json` from entry #0. The CI log cuts the line at 300 characters, so the differing text is not visible; seeing it needs a run of the slow-tier file, which the rules forbid locally, and refreshing the capture is an owner-word act ("retaken ... the owner's word", file docstring) and is a non-goal here. QUESTION for the Lead: who retakes the capture (`python -B scripts/tests/test_story_run_s6_w1_frozen.py --capture <dir>`), after confirming that the difference is an intended console change of a wave commit (suspects: S6 console lines changed by OF/TR/P1-v nodes), not a regression.

## Final CI

Round 2 canon on d53a327: run 43502097900 (workflow_dispatch canon main) - forge-check success, install-smoke success, package-full (1) success, package-full (2) failure, package-fast failure; the ONLY red line in both is `test_story_run_s6_w1_frozen.py` (`w1_frozen_console`, 5/6 ok). Push pipeline of d53a327: 43502096306 (failed on the same package-fast line). Earlier: canon 43500141242 on 5cc4f88 (red: forge-check cost:queue, refusals line 158, w1_frozen), 43492038420 on 7cf8c34.
Queued branches of the later wave (owner-words-1113b, statuses-wave1, pc3-2, p1v-n4b) were NOT merged: main is not green (w1_frozen open) and the two rounds are used.
