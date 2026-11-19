# t-1543 FV3-22-2 builder report (the skill road closes S6's manual half)

Branch `wip/fv3-22-2-t1543`, commit `a096efac` (package files). `docs/SIBLING_MAP.md` is a mechanism path: STAGED, not committed (the Lead commits it).
Not committed: this report.

## Plan items (card r2 K5.e-K5.k, with the t-1209 overrides)
- K5.e `story_step._s6_manual_close`, `_manual_cases_left`, `_no_stand_cases` (+ `_no_stand_cases_of`, `_no_stand_lines`): DONE. `story_step.py`.
- K5.e step 1b (re-entry) with the t-1209 discriminator: DONE. `stage_done.stage_finished_at` (new, beside `read_pipeline`), `stage_close.stage_record_written`.
- `stage_close.SkillRoad` (all road members): DONE. `stage_close.py`.
- K5.f X1/X2/X3 call at the three exits (`settle` in `_manual_block_check`): DONE.
- K5.g automation door line: DONE. K5.h `start` widened to `if code or (refusal and block is None)`: DONE.
- K5.i `phases/s6.md` card line 6: DONE; `card --stage S6` prints no `over` note.
- K5.j changelog bullet 2, `SIBLING_MAP.md` axis 5 (two rows) and axis 26, `test-layers.json` covers `story_progress.py`: DONE (map staged only).
- K5.k `story_progress._awaits_position` + `progress()` branch + `_parts()`: DONE.
- Tests: rows C1-C11c, C14-C16, C9c (extra, t-1209), P1-P5, K5.i variant: DONE. Nothing left unwritten.

## Measurement ordered by the Lead (before coding), temp root, not the repo
Script `/tmp/fv/measure.py` (temp dir, a real story built with the test fixtures, S6 closed by a real `code_only` receipt, then a person's accept record, then the command below twice):
```
cmd: python -B <worktree>/ai-packages/qa-factory/scripts/stage_done.py --task QA-9 --stage S6 --status done --digest measure --no-journal
acceptance exit 0  pipeline.json: acceptance S6 -> accept by driver for S6-qa-runner-1
run 1 exit 0  pipeline.json: S6 -> done at 2026-11-19T19:02:36+00:00   (finished set: '2026-11-19T19:02:36+00:00')
run 2 exit 0  pipeline.json: S6 -> done (recovered existing event)       (finished unchanged)
```
ACCEPTED on an already-completed S6, not refused. Without a consumer record the same command exits 2 (`S6 is closed by the stage acceptance of qa-failure-analyst ...`): that is the consumer rule, a different refusal.

## Witness
DoD command (one run after all edits):
```
python -m pytest ".../test_story_step_manual_block.py::test_fv3_22_nothing_left_closes_s6_on_the_skill_road" "...::test_fv3_22_awaits_position" "...::test_the_card_and_the_help_name_the_rule" -q
3 passed, 18 warnings in 81.22s (0:01:21)
```
The `in N.NNs` tail is 81.22s for the three functions (card file budget was 10 s: each row builds a real controller story; not reduced).
Whole file as a script (development run): `=== test_story_step_manual_block: 281/281 ok ===`.
`python -B .../story_step.py card --stage S6` tail (no `over` note; `grep -c "over 4000"` = 0):
```
- Boundary and judge: Read ...\phases\s6.md offset=43 limit=85
- Runtime first; baseline never blocks execution: Read ...\phases\s6.md offset=128 limit=27
Another config key: `config_view.py --keys [PREFIX]` lists them, `config_view.py --get PATH` prints one (never read config.json whole).
```
`scenario_walk.py --witness-for <the owns + stage_done.py>`: `run locally: 16 file(s); canon judges: 80 file(s)`. The 16, each run as a script, exit 0:
test_conductor_stop 48/48, test_dispatch_identity 114/114, test_probe_not_proved 47 passed, test_s0_close_order 29/29, test_stage_cards 163/163, test_stage_closure 88/88, test_stage_of_dispatch 20/20, test_state_exits 142/142, test_then_remainder 354/354, test_s5_plan_windows 104/104, test_resume_packet 117/117, test_sizing 240/240, test_source_stage_integration 21/21, test_story_sides_readers 45/45, test_story_sides_registry 33/33, test_selftest_shard 103/103.
`selftest.py --limits`: `PASS limits ...` x2; `selftest.py --lang`: `PASS lang: no control byte left ...`.

not run locally: test_story_step_manual_block.py (whole), test_judgment_census.py, test_driver_layers.py, canon judges
(Honesty: I did run the manual_block file whole as a development run, line above; I did not run census, driver_layers or the canon judges. No layer file or `driver-layers.json` is touched, so "ratchets raised: none".)

## Probe (byte copy before, restore from it, sha256 after)
Target `test_fv3_22_nothing_left_closes_s6_on_the_skill_road`, each probe red, file restored:
- P1 X1 call replaced by today's lines (`story_step.py`): red at C1/C2 (`IndexError`: no receipt). sha256 before = after = `ece29e26e3f01496...`.
- P2 `road.consumer_need_record(...)` -> `if False:` (`stage_close.py`): red (`IndexError` at C1/C2: it closed over no record). sha256 before = after = `2e21c5573976d9b0...`.
- P3 live filter `running`-only: `AssertionError: ["C11b ...", "C11c ..."]` (C11 green, as the card says). sha256 `ece29e26e3f01496f304f37062806cd0ad26813e7fbb33fa789275a90bb9728d` before = after, equal True.
- P4 step 1b -> `if False:`: `AssertionError: ["C9 ...", "C9c ...", "C9b ..."]`. same sha256, equal True.
`git status` after the probes: only `M docs/SIBLING_MAP.md` (staged).

## AR lines (change checks; greps run on the final tree)
- AR-13: `BY_PERSON =` 1 hit, `stage_close.py:24`. `def live_s6_scopes` 1 hit, `controller.py:690` (t-1209 F5: it stays there). Diff of `story_step.py` / `stage_close.py` / `story_progress.py`: no `json.loads(` of pipeline.json, no `["acceptance_awaits"]` read. Positive control: `acceptance.py:1523-1524` found by the same grep.
- AR-14: `atomic_json(` in `stage_close.py` = 1; no `atomic_json` / `write_text` / `Person(` / `no_move` / `ask(` in the added lines of `story_step.py`, `story_progress.py`, `stage_close.py` (grep output empty; control: `atomic_json(` count 1 in stage_close).
- AR-15: one `_manual_cases_left` (used by `_manual_block_door` and `_s6_manual_close`), one `_no_stand_cases` (used by `_no_stand_cases_of` and `_s6_manual_close`). Sites of the problem (`finalize_task.py`, `"code_only"`, `acceptance_awaits`, `"running", "blocked", "paused"`): survivor callers = `stage_close.py`, `story_step.py`, Driver delegates; named sites left = other S6 steps (FV3-24), S7/S9 (FV3-26).
- AR-18: every `road.py(` in `stage_close.py` binds its result (`:224`, `:248`) or passes `check=True` (`:126`). A27 not widened (residual named).
- AR-19/20/22: S7 `close_by_code` callers unchanged; no `driver-layers.json`, no census edit; `stage_close` imports no `driver_*`/`story_step`.
- AR-21: C2, C7, C9: the reducer runs before the marker; a completed S6 is never reduced again. AR-23/25/27/28: C1, C9b, C14, C3b, C5, C8, C11*.
- FR pass: FR-1/2/5/40 every refusal of the close ends with a `door:` the receiver can run (`person_word_door`, the E9 `stage_done.py ... --digest "<reason>"`); FR-4 the person's word is recorded (`by: person`), word time later than the acceptance (C3, C3b); FR-48 no new stop, ask or conductor command; FR-59 any unreadable time/scope/state reads toward "left", "not written" or no close; FR-29 no control byte (selftest --lang); FR-54 axis 5 twins named in the map, S7/S9 = FV3-26.

## Deviations and decisions the card did not fix (please confirm)
1. Step 1b, Lead text "unreadable time -> not written: falls through to the close, which runs `stage_done --status done` again": the close cannot do that (`close_by_code` returns early on a completed stage, no `stage_done`). I returned the E9 door (exit 2, `stage_done --status done --digest "<reason>"`, no reducer) for every not-written case, unreadable times included. `stage_close.py` `stage_record_written`, `story_step.py` step 1b.
2. A stage the controller completed WITHOUT a `code_only` receipt (a role's accept) -> step 1b returns None (today's lines). Not covered by the card; it keeps today's behaviour. `story_step.py` step 1b.
3. `stage_finished_at`: a `finished` with no time zone -> None (not written); `Z` is read as UTC. Completion time = `stamp_utc` of the S6 `code_only` event's `created_at` (seconds, as `finished` is).
4. Step 6 under the no-stand word: `_no_stand_cases` is called directly (it runs `prepare_for_block` itself), not prepare first and then `_no_stand_cases` (one prepare per case, same outcome).
5. pytest: the harness `check` never raises, so a red check would pass a pytest node. The three DoD functions end with `_assert_green_since(count)` (raises when a check since the start failed). The existing `the_card_and_the_help_name_the_rule` was renamed `test_the_card_and_the_help_name_the_rule` (the DoD name) and `main()` calls it.
6. `start` prints a closed S6 "closed by code: <reason of the receipt read back from the controller>", so the reason text is the controller's, not rebuilt.
7. Windows line endings: working files are CRLF; my first patch scripts hit FR-29 (a heredoc ate `\n` into a real newline, `SyntaxError`), found by `ast.parse` and fixed with the Edit tool before commit.

## Noticed, not widened
- The driver's word loop `manual_no_stand` and the skill road's `_no_stand_cases` are still two loops (card a2).
- Second script runner: `SkillRoad.py` (exit 127 on a missing script) vs `story_step._run` (skipped success) - justified by the card.
- `test_story_step_manual_block.py` is 81 s for 3 functions; the other 18 functions of the file are not pytest-collected (no `test_` prefix).
- `driver_stage_s6.py` and `driver_stage_s7.py` still hold the other code-close sites (FV3-24 / FV3-26).

## Needed from integration
- Lead: commit the staged `docs/SIBLING_MAP.md` (mechanism path; message `axes: not a mechanism (the edit records the survivor of an existing twin row, axis 5, and the readers of an existing word, axis 26; it adds no new duty)` + `tier:` line).
- Live proof line (FR-33) for the batch: a skill-road story with every manual-agent case refused reaches S7 awaiting the analyst; after the analyst's record (or a person's word) the same `start` closes S6 code-only.

## Config keys
None added.

## CHANGELOG fragment
`ai-packages/qa-factory/changelog.d/fv3-22-skill-road-s6-close.md` bullet 2 (the fragment existed from part 1; I appended).

## Beyond the manifest (read)
`scripts/controller.py` (live_s6_scopes, code_only event, stamp_utc), `scripts/acceptance.py`, `scripts/stage_done.py` (written: `stage_finished_at` only, authorised), `scripts/hooklib.py`, `scripts/driver_runner.py` (Driver.py), `tests/story_run_common.py`, `tests/test_controller_state.py`, `tests/test_fixes_13797.py`, `docs/TESTING.md` witness scope.

## Round 2 (fix round over a096efac, commit 5866e362; review t-1558)

- F1 DONE: `stage_close.record_door(task, stage, args)` (stage_close.py, new, before `stage_record_written`) is the one door builder; `SkillRoad.record_close` and `story_step._s6_reentry` call it, so both print the same command for the same args. Note: a one-word digest is now unquoted on step 1b too (the shared rule quotes only whitespace); real reasons contain spaces, C9b/C9c green.
- F2 DONE: `stage_close.stage_record_written` reads through `stage_done.read_pipeline`; new `stage_done.iso_with_zone(value)` (stage_done.py, before `stage_finished_at`) is the one ISO-with-zone parse, used by `stage_finished_at` and `person_pass`'s `stamp` (stage_close.py:101-). Naive/unparseable -> None / "" as before; the `OverflowError`/`OSError` catch of `timestamp()` stays in `stamp`.
- F3 DONE: row C2b in `test_fv3_22_nothing_left_closes_s6_on_the_skill_road` (S6 completed by two role accepts, no `code_only`: exit 2, no step, no receipt, no `stage_done.py` door, no "S6 was not closed"). Probe: dropping the `code_only` check in `_s6_reentry` made C2b red (`... True, False` for "stage_done.py" in text); restored by byte copy (`cmp` equal).
- F4 DONE: P2 now builds a real root (state/controller.json + pipeline.json, S0-S6 done) and asserts `progress(root)` position kind `awaits` and `waiting for the doc scribe's acceptance (S8)` in `["line"]`.
- F5 DONE (staged): SIBLING_MAP axis-26 clause names `_no_stand_cases_of`, `_s6_manual_close`; `_no_stand_cases` takes words as a parameter; `_no_stand_lines` reads `waiver.stand_passing_override`. Re-staged, not committed.
- F6 DONE: step 1b extracted to `story_step._s6_reentry(task, task_root, controller, held, where)`; `_s6_manual_close` return contract unchanged (now calls it when S6 is `completed`).
- F7 DONE (Lead's decision): row C11c deleted; C11/C11b stay. Run time 39.8 s for three functions (was 81 s).
- Choices confirmed by the Lead (E9 door for unreadable time; role-accepted S6 -> today's lines): unchanged, (2) now has row C2b.

Witness (from the worktree root, after all edits):
```
python -m pytest ...::test_fv3_22_nothing_left_closes_s6_on_the_skill_road ...::test_fv3_22_awaits_position ...::test_the_card_and_the_help_name_the_rule -q
3 passed in 39.76s
python -B ai-packages/qa-factory/scripts/selftest.py --lang
=== qa-factory selftest: 2/2 ok ===
```
not run locally: the whole test_story_step_manual_block.py and the canon judges (CI); Driver.close_by_code behaviour untouched (record_door output is byte-equal to the former inline text for whitespace-bearing args).
Analogs noticed, not touched: none new beyond R1 (Lead's node).
