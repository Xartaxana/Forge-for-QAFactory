# SC-A1c report - one "can close its stage" predicate, one purpose reader, stale text, test hygiene

Branch `wip/sc-a1c` (from 08b2b1c, merged with origin/main: clean, no conflict). Worktree
`C:\QAFactory\forge-repo\.claude\worktrees\sc-a1c`.

## Per-item facts

1. ONE predicate. `controller.dispatch_can_close_stage(record)` (module level, pure, never raises) =
   `contract.stage_closes_with(stage, role)` AND `s3_window_of(record) != "labelling"`; an absent purpose is the exit window and
   closes (edge 1); any other stage answers as before (edge 2); a non-last role is False (edge 3). `Controller._closes_stage`
   starts with it, then keeps its S5-plan / S7-investigation / completed / derived-scope exemptions unchanged. Position
   INVARIANT (edge 4): `_s3_completion_gate` untouched and still the last word - row `accept-s3-window-one-complete` shows it
   still refuses a window-1 completeness claim; no site became able to close S3 on window 1 (control run below).
   Wired:
   - `controller.py` ~5098 / ~5851: both go through `_closes_stage` (the default `stage_complete` at accept; the "no role to
     close it" refusal) - covered by the predicate inside `_closes_stage`, no separate edit.
   - `stage_repairs`: A1a's inline `stage_closes_with(...) and s3_window_of(last) != "labelling"` replaced by
     `dispatch_can_close_stage(last)`; the local `from contract import stage_closes_with` removed.
   - `story_step._halt_doors`: closing role -> `--close`/`--open`; NEW branch for window 1 -> `--open` and the pause/recover
     road only (no `--close`).
   - `story_step.finish` (~2496): the default "last role closes" is `role == last and dispatch_can_close_stage(dispatch)`.
   - `story_step.finish` recorded `close` (~2506): `not dispatch_can_close_stage(dispatch)` -> "accepted as it is" note.
   - `story_step._decide_refusal`: window 1 + `--close` is refused (always, a form that declares the halt widens nothing) with
     the text: what is wrong (S3 window 1 never closes S3), what was expected, doors `--open [<ids>]` and
     `finish --not-complete --unresolved plan_pending` (FR-1, FR-2); window 1 + `--open` stays allowed (the door the refusal
     names); the rest of the non-closing branch is guarded by `not _labelling(dispatch)` so a role that does not close keeps its text.
   - `story_step.decide` final print (~2964): `not dispatch_can_close_stage(dispatch)`.
   story_step reads the predicate through `from controller import dispatch_can_close_stage` (story_step's `C` is `contract`, not the
   controller; no copy of the test).
   Rows (one parameterised table each, ids name the case) are in `scripts/tests/test_stage_closure.py` (fast, kept, a witness of both
   `controller.py` and `story_step.py`): `s3_window_one_never_closes` (predicate + `_closes_stage` 12 rows, purpose reader 6 rows,
   `_halt_doors` 4 rows, `_decide_refusal` 5 rows) and `s3_window_one_accept_without_unresolved` (real `Controller.apply` accept:
   window 1 `stage_complete: false` accepted; window 1 `stage_complete: true` refused by the completion gate; exit window false
   refused as before). (a) halt: no `--close`; (b) refusal with doors; (c) accepted instead of the false text (see Q1); (d) exit
   window closes; (e) S5 plan and S7 investigation unchanged (`_closes_stage` False).
   `test_story_step_decide.py` / `_finish.py` (where `decide`/`finish` end to end live) are quarantined (`test-layers.json`
   quarantine section): not run, not edited.
2. N1: ONE public reader `controller.record_purpose(record)` (binding only; `""` for an absent/non-mapping binding, a non-string
   purpose or an unreadable record; never raises). Used by `driver_stage_plan.completion_for` (T2, replaces
   `SG._record_purpose`), by `story_step` (`_purpose_of` deleted, 3 callers re-pointed) and by `controller.s3_window_of` (its
   own copy of the binding read is gone). The model dict: T2 builds `{"stages": ...}` once from one `self.stages()` call;
   `story_step._optional_row` now passes `stage_guard.stage_model()` (the file's own dict) instead of rebuilding it per call.
   `stage_guard._record_purpose` is LEFT AS IS: `stage_guard.optional_stage_of_dispatch` relies on its top-of-record fallback for its
   own guard (edge 5). N2: `brief_pack.stage_critic_names` has one local helper `parts_of(row, stage_id, parts)` used for the own
   stage `("outputs", "advice")` and for each earlier stage's part.
3. Stale text fixed: `acceptance.py:1273` ("the acceptor's verdict on S4, S6 and S7"), `stage_done.py` `--acceptance` help
   ("S4, S6, S7"), `handoffs/vocabulary.yaml:121` ("stage acceptor (S4, S6, S7)"), `handoff.py:406` ("the S4 stage critic, S7/S8
   consumers"), `handoff_init.py:468` (the spec's :435 is `--rows`; the "(S2-S4)" help is at :468) -> "the stage critic's form (S4)",
   `story_step.py:365`, `brief_pack.py:3693` docstring ("S4"), `exit_gate.py:820` (the stale part there was a reference to the
   non-existent `s3_author_done`; removed), `test_first_look_wiring.py:99` label ("the strategist stays the role"). Also one stale
   comment found beside: `brief_pack.py:4340` ("the stage critic stands on S3 too") - fixed. "S7 skeleton Reviewed dispatch" comment:
   case-insensitive grep `S2-S4|Reviewed dispatch` over the whole package: the S7 skeleton hits are
   `handoffs/s7-analyst-to-automator.yaml:67` and `s7-analyst-to-scribe.yaml:33` ("Reviewed dispatch (as in your brief): ..."); neither
   says S2-S4 or names a removed critic, so nothing to fix there (not in owns either). NOT touched as ordered: `exit_gate.py:646`,
   `driver_dialog.py:121`, `driver_dispatch.py:1833`, `question_register.ROLE_QUESTION_STAGES`.
4. Tests: N3 - the three `driver.stage_critic_route = lambda` stubs and their empty-list asserts removed (`test_story_run_s3_windows.py`
   W3 diff world, W11, SC-1) and the two `hasattr` absence pins (`test_story_run_s3_windows.py` W2, `test_first_look_step.py`
   s3_readers). N4 - `test_null_outcomes.py` label "20 never_empty" -> "18 never_empty" (the checked value).

## FR walk (touched sections)
- A refusals: FR-1/FR-2 - the new `decide --close` refusal on window 1 says what is wrong, what is expected and names two doors a
  caller can use (`--open`, `finish --not-complete --unresolved plan_pending`); the window-1 halt text offers `--open`, never the
  refused `--close` (FR-2: no door the command would refuse). FR-4: no check stops an informed pass added. FR-57: window 1 keeps a
  door at every refusal.
- B text shown to a person: not touched (a halt/refusal text for the conductor, not a question to a person).
- C contracts: FR-14/FR-15 - the new reader/predicate are code reached by name; no producer without reader (`record_purpose`
  has three readers, the predicate seven). FR-42: window 1 returns a move at every site.
- D identity: not touched. E delivery: not touched. F measurement: not touched.
- G code: FR-30 English only (selftest --lang below); FR-54 siblings walked (below); FR-47 no judgment moved into code.
AR: AR-25 (window 1 has a way out at every site), AR-13 (one purpose reader, one predicate), AR-15 (shared problem solved at one
survivor, wired at every site).

## Callers of `stage_closes_with` outside `_closes_stage` (verdicts)
- `controller.dispatch_can_close_stage` - the predicate itself.
- `controller.stage_repairs` - re-pointed (predicate).
- `controller._is_review_of` (~4111) - correct as is: it asks "is this role the stage's last reviewer of another role", the strategist
  is not a review; labelling window is not a concept there.
- `story_step._halt_doors`, `finish` (x2), `_decide_refusal`, `decide` print - re-pointed.
- `tests/test_story_run_s3_windows.py` SC-1, `test_window_stage_contract.py`: tests of `contract.stage_closes_with` itself - correct.

## Verification (verbatim)

Witness list: `( cd .../sc-a1c/ai-packages/qa-factory && python -B scripts/tests/scenario_walk.py --witness-for scripts/controller.py scripts/story_step.py scripts/driver_stage_plan.py scripts/brief_pack.py )` printed 240 rows / 142 distinct test files (the full list is long; the fast part was run). Run: every printed file that is not in `slow_tests.json`
and not `test_story_run_*` / `test_controller_*` / `test_fixes_13797` (52 files) plus `test_brief_pack.py`
(34 s), each `python -B scripts/tests/<file>` from the package dir. 53/53 rc=0:

```
test_ahead_cards.py 265/265 | test_awaiting_state.py 144/144 | test_brief_s3_roster.py 12 passed | test_codex_tool_guidance.py 217/217
test_conductor_stop.py 48/48 | test_detector_verdict.py 210/210 | test_dispatch_identity.py 114/114 | test_driver_stop_record.py 255/255
test_environment_lifecycle.py OK | test_event_store.py rc=0 | test_exploratory_answers.py 107/107 | test_field_producers.py 885/885
test_first_look_briefs.py 184/184 | test_first_look_code_look.py 127/127 | test_first_look_step.py 101/101 | test_first_look_wiring.py 102/102
test_fit_targets.py 116/116 | test_flow_requests.py 93/93 | test_gate_question_form.py 466/466 | test_gate_vocabulary.py 141/141
test_handed_to_person.py 58/58 | test_hook_lifecycle.py 25/25 | test_human_questions.py 291/291 | test_local_keys.py 199/199
test_login_need.py 33 passed | test_null_outcomes.py 327/327 | test_person_owned.py 82/82 | test_probe_gap_door.py 54 passed
test_probe_marker_judgment.py 46 passed | test_probe_not_proved.py 47 passed | test_quality_demand.py 84/84 | test_reference_window.py 85/85
test_regression_scope.py 93/93 | test_resume_packet.py 117/117 | test_resume_story_isolation.py 310/310 | test_role_load.py 186/186
test_s0_close_order.py 29/29 | test_s5_plan_windows.py 104/104 | test_s5_window_leftovers.py 148/148 | test_scoped_invalidation.py OK
test_session_handoff.py OK | test_stage_cards.py 163/163 | test_stage_closure.py 80/80 | test_stage_of_dispatch.py 17/17
test_state_exits.py 142/142 | test_then_remainder.py 354/354 | test_walk_account.py 190/190 | test_walk_lanes_parallel.py 196/196
test_walk_plan_fields.py 123/123 | test_walk_supply.py 261/261 | test_whole_identifier.py 166/166 | test_whole_list_sites.py 292/292
test_brief_pack.py 1125/1125
```

New rows alone: `python -B scripts/tests/test_stage_closure.py` -> `=== stage closure: 80/80 ok ===` (was 77 at the 1st pass of the
predicate rows, 80 with the accept rows).

CONTROL (negative): with `dispatch_can_close_stage` temporarily returning `True` for window 1 (restored right after), the same file
printed:
```
FAIL A1c predicate closes-s3-window-one: labelling - expected False, got True
FAIL A1c _closes_stage closes-s3-window-one: labelling - expected False, got True
FAIL A1c halt-doors-s3-window-one: no --close, --open stays - expected (False, True), got (True, True)
FAIL A1c halt-doors-s3-window-one: a form that declares the halt widens nothing - expected (False, True), got (True, True)
FAIL A1c accept-s3-window-one-not-complete: no 'no role to close it' refusal - accepting S3-qa-test-strategist-9 with stage_complete: false leaves S3 with no role to cl...
FAIL T1 s3-between-windows-not-closed: window 1 (purpose s3_labelling) accepted, no stage_complete, nothing open - expected [], got [('stage_completed', 'S3')]
=== stage closure: 74/80 ok ===
```

`python -B scripts/selftest.py --limits --lang` (package dir):
```
PASS lang: no Cyrillic anywhere in the package
PASS lang: no control byte left by an eaten escape sequence (FR-29)
PASS limits: SKILL.md / agents / references within size caps
PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier
=== qa-factory selftest: 4/4 ok ===
```
Syntax parse of the edited-but-slow `test_story_run_s3_windows.py`: ok (it was not run).

Slow files left to the batch canon: `test_story_run_s3_windows.py` (edited: N3 stubs removed; also judges the T2 rule of
`driver_stage_plan.completion_for` after the reader swap), all `test_story_run_*`, `test_controller_*` (incl.
`test_controller_state.py` which judges `_s3_completion_gate` and the "no role to close it" text), `test_fixes_13797.py`, and every
slow-listed file of the witness (`test_blocked_by_env_window`, `test_branch_accounting`, `test_bug_records`, ...). The `decide`
/ `finish` end-to-end files are quarantined. No ratchet or pin was raised; no pin went red in the files run.

## Edges / deviations / questions
- Q1 (behaviour to confirm): with the predicate, `finish --not-complete` with NO `--unresolved` on S3 window 1 is now ACCEPTED
  (`stage_complete: false`, window 1 stays between windows; the old text claimed "pass stage_complete: true", which the completion
  gate refuses). The live road is unaffected: `s3_window_completion` returns `OpenWork("plan_pending")`, so `finish` sends
  `--unresolved plan_pending`. The spec (c) asked for "text true for window 1"; there is no longer any refusal text at all on that
  path. If the Lead wants a refusal there ("window 1 must name plan_pending") it is a separate requirement; not guessed.
- `story_step.finish` default (`role == last`) now also does not assume completion for window 1 (a bare `finish` on window 1 sends
  `stage_complete: false` instead of `true` that the gate would refuse); the spec lists `~2494 (finish)` as a site, this is that site.
- The spec says "`story_step` reads it through `C.`": `C` in story_step is `contract`, not the controller; the predicate lives in the
  controller module (as the spec orders) and story_step imports it by name from `controller` (same module its other readers use).
- `handoff_init.py` line differs from the spec (435 -> 468 for the "(S2-S4)" help).

## Analogs noticed (not fixed, outside owns or scope)
- `planning_contract.py:113` docstring: "S3 critic's judgment" - the S3 critic is gone (stale text, outside owns).
- `stage_guard._record_purpose` keeps its top-of-record fallback for its own guard; a later node may decide whether the guard
  should read the binding only (it would then be a fourth reader to fold into `record_purpose`).
- Tests that mention the removed S2/S3 critic in labels/comments: `test_brief_pack_roles.py:411-414` (S2 critic brief),
  `test_conductor_doors.py:1079-1082`, `test_controller_stage_acceptance.py` (quarantined readers per the review), `story_run_common.py:297`,
  `controller_rework_common.py:152`, `test_controller_rework_scope.py:585`, `test_coverage_controller_integration.py:43` ("E-B11 ... S2-S4").
- `handoffs/s2-stage-critic-to-tester.yaml` / `s3-stage-critic-to-strategist.yaml` still named in `test_handoff_init_author.py:16`
  CRITIC_CONTRACTS (quarantined per the review).
- `CHANGELOG.md:56` historic text and `references/controller-api.md:124` ("revised S2-S4/A" - an unrelated phrase, left).

## Needed beyond the manifest
`scripts/contract.py` (`stage_closes_with`, `stage_roles`), `scripts/stage_guard.py`, `scripts/tests/test-layers.json`,
`scripts/slow_tests.json`, `scripts/tests/harness.py`, `scripts/tests/test_controller_state.py` (reading only),
`handoffs/s7-analyst-to-*.yaml`.
