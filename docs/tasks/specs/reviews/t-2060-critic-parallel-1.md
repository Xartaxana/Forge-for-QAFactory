# t-2060 critic: parallel, first part (t-2042 TR3-7, t-2043 TR3-11, t-2047 TR3-2, t-2051 TR3-8)

Base 77b448a3e. Heads: tr/tr3-7 cfdf20ca5, tr/tr3-11 986645cd7, tr/tr3-2 450165da4, tr/tr3-8 b1b30aec2.

## Verdict: NEEDS WORK (fit_with_fixes). 8 findings block the merge, 10 are fixed before it, 3 queue. The acceptance decision is the Lead's.

The DoD's three answers:

- **Can a dead walker or a stale lease record block the stand?** The stand: no. A dead holder is dropped at the next acquire even when that attempt is refused (`_try_acquire`; `test_dead_holder_dropped`). An old-shape record holds nothing. A holder with no recorded birth and a recycled pid stays `unknown` until `--release` (inherited, it has a door). But onboarding's apply can be blocked by a stale record, in two new ways: F5 and F6, both measured.
- **Can settle skip a changed item?** On its own bytes, binding, record, author or generated files: no. On inputs outside the stamp: yes. F8 (other manifest rows), F9 (a transient failure remembered), F10 (a new dispatch's scope).
- **Do the four branches conflict at merge?** No textual conflict. All six pairs were dry-run with `git merge-tree`; each gave a clean tree. No file has more than two writers (`probe_debt.py`: 7+11, `story_step.py`: 11+2, `manual_capture.py`: 7+8; `walk_session.py` and `story_run.py`: one writer), so pairwise clean means the whole set is clean, in any order. No semantic conflict found: `test_probe_debt.py` seeds no lease file (the same grep lists 15+ other test files).

## Findings

### TR3-2 (driver timing)

**F1. BLOCKS. The silence watchdog can never speak on a real run.** Surface: the reader of a role's transcript. `driver_timing.last_write` reads `dispatch_liveness.transcripts()`, which is `hooklib.story_subagent_transcripts`, which globs only `<session>/subagents/agent-*.jsonl`. A driver role is its own `claude -p` session: a MAIN transcript. Measured (`scratchpad\critic2060\stand_facts.py`, `stand2.py`), read-only on real runs:
```
tr-arm-b  transcripts: 0  LOCAL-1 role dispatches: 55  matched by transcripts: 0
tr-b20    transcripts: 0  role dispatches: 56  matched: 0
tr-walk   transcripts: 0  role dispatches: 64  matched: 0
tr-arm-a  transcripts: 0  role dispatches: 32  matched: 0
positive control, tr-arm-b: cost files 94 with transcript 94; main transcripts 94, subagent transcripts 0;
hooklib.subagent_meta on the main ones reads S5-qa-automator-13, S6-qa-runner-1, S7-qa-failure-analyst-1 ...
```
The builder's decision against `state()` is right (read at `dispatch_liveness.py` 937-943: alive with `last_at: None`), but its replacement is starved. `test_story_run_wait.py` patches `last_write`, so it cannot see this.
Fix: `dispatch_liveness.session_transcripts(project_root, since)`: the folders are the parents of `state/cost/*.json` `transcript` paths (no guess at the host's encoding), `*.jsonl` with mtime >= `since`. `last_write` matches by `hooklib.subagent_meta(path)["dispatch_id"]`, then keeps the matched path and only stats it on later polls (`watch` holds it). No cost file yet = unknown, no line. Keep `transcripts()` as it is. Test `silence_reads_the_main_transcript` in `test_driver_timing.py`: a cost file pointing at a main transcript with no `subagents/`. Witness: `last_write` on `D:/ws1/mybooks-stand\tr-arm-b`, dispatch `S5-qa-automator-13`, returns an epoch.

**F2. BLOCKS. The t-2034 M2 addition is not built.** `driver_timing.watch` says through `print(line, flush=True)`. `redirect_stdout` at `story_run.py:4406` is process-wide, so the line lands in the StringIO. `silence_line_survives_redirected_stdout` does not exist (the function list of `test_story_run_wait.py` has only the other four).
Fix: `driver_timing.console(line)`: `sys.__stdout__.write(line + "\n")`, flush, and on None or OSError nothing. `watch`'s default `say` uses it. Neighbours of the surface: the `wall_said` print in `run_claude` and both prints in `Driver.timing_write` use it too. Add the named test.

**F3. BLOCKS. The t-2034 mode gate is not built, and a byte pin goes red.** `story_step.start` prints `timing:` lines on every road. Answer to the edge: yes, there is a pin. `test_launch_card.py:271-272` takes stdout from the prompt line to its END and compares it with the card, byte for byte; the extra lines break it (read, not run: slow file, it pops `RUN_MODE_ENV`, so it runs on the skill road).
Fix: `if current_run_mode() == "driver": print("\n".join(laps.lines()))`. Add `timing_lines_not_in_card` and `timing_lines_absent_on_skill_road`. The pin stays as it is.

**F4. BLOCKS (CI red). The `--task-root` census.** Measured: `declared-not-expected: ['driver_timing']`; `test_task_root_parsers.py:157-160` is a "a new one is red" equality.
Fix: add `driver_timing` to `B_SCRIPTS` and its battery row `"driver_timing": lambda f, r: [f, r]` (the `walk_timing` row, :302). Add a `CLI_SCRIPTS` row in `audit_factory.py` beside `walk_timing` (:219), as the builder noticed.

**F4a. FIX. A byte that is not UTF-8 stops the aggregator.** `driver_timing._rows`: strict `read_text(encoding="utf-8")`, `except OSError` only. A torn multi-byte tail raises `UnicodeDecodeError`: a traceback, against "unreadable line is counted". Fix: `errors="replace"`; extend `unreadable_line_is_counted_not_dropped` with a raw bad byte.

Judged, no finding: `timed` concurrent writes (`append_jsonl_line` under `_JSONL_LOCK`, one process, only the driver writes); no `stages.json` row (the carrier belongs to no stage, same as `driver-runs.jsonl`); `_hops` on real rows (113, 114, 127, 55 hops from real `driver-runs.jsonl`). Report item to correct: the reader it names for `wall_ms` is a local variable, not the row; the row field has no reader yet (AR-22). `test_field_producers.py` in CI decides; N-LIVE is the intended reader.

### TR3-7 (lease)

**F5. BLOCKS. `_holder_state` stopped reading the scheduler's birth key: a recycled pid now holds onboarding.** `stand_lease._holder_state` is also the reader for `execution-leases.json` (`onboard_apply.LEASE_FILES`, `_holder_state`), and those rows carry `process_started_at` (`execution_scheduler.py:171,587`). Measured with a dead run's row whose pid was recycled:
```
wt-tr3-7 [('qa-factory/state/execution-leases.json', 'unknown', 'pid 42692')]
wt-tr3-2 []     (the base's code: no lock)
```
Per `test_install_retire.py:506`, a live lease refuses the apply at once. Fix: `started = str(lease.get("started") or lease.get("process_started_at") or "")`, comment: this reader serves both lease files. Control row in `test_install_retire.py`: this probe's row reads as no lock.

**F6. BLOCKS. A person's `--release` leaves a note that reads as a live lock, and `--release` cannot clear it.** The new note carries `pid`; `onboard_apply._holders` walks every object in the file holding `pid`, the `notes` list included. Measured (`scratchpad\critic2060\note_probe.py`):
```
before release: [('qa-factory/state/stand-lease.json', 'live', 'pid 34468')]
release: released
after release: [('qa-factory/state/stand-lease.json', 'unknown', 'pid 34468')]
release again: {'status': 'not_held', 'environment': 'default'}
```
The door `_live_door` names answers `not_held` while the process lives, and a recycled pid repeats it. It is exactly the case E1b.3 exists for: a hung walker. Fix: name the key `held_pid` (the pattern of the takeover note's `dead_pid`). Test in `test_install_retire.py`: the probe's sequence ends with no lease lock.

**F7. BLOCKS (CI red). A reader of the old shape is left.** `test_walk_places.py:72` `{r["job_id"] for r in status(...)["leases"]}`. Run: `KeyError: 'job_id'` from `test_case_lane_lease_unchanged`. Not in the report's walk. Fix: `{h["job"] for r in status(...)["leases"] for h in r.get("holders") or []}`.

**F7a. FIX.** `MODES` (`stand_lease.py:161`) is dead: the only hit is its definition. Delete it. `fixtures/env-facts-baseline.json` row `#15` still names `{pid, process_started_at}` and a stale line range: correct the text (no count changes).

Judged, no finding: `page_lease` exclusive (S7 holds per request, its invariant is unchanged; nesting checked: `walk_session.py:999` takes it only when `place != "case"`, so a case walk cannot block itself); old shape reads as nothing (owner's non-goal); `max_shared=1` until N5p. Note, no fix: the `mode == "exclusive"` branches in `run_suite.hold_stand` and `manual_capture._hold_stand` exist to keep a test mock's signature; that is test-shaped production code, removable when `test_run_suite_mine.py` is next touched.

### TR3-11 (settle)

**F8. FIX. The stamp leaves out what the dry run's refusal depends on.** `_rebind` refuses on `_live_ids(manifest)` and `_aliases(row)` ("would write ids the manifest does not hold"). `_stamp` holds neither. Input: `ra` kept for that reason; another window's `manifest_put` adds the id, shas and record unchanged, no new accepted author. Output: `same_bytes`, or (c) "nothing changed, not run", though the same dry run now passes. Fix: `_stamp` gains `manifest_ids`: sha256 of the JSON of `[sorted(_live_ids(manifest)), sorted(_aliases(row))]`, None when unreadable. Test `settle_retries_when_manifest_ids_change`.

**F9. FIX. Handed-up decision 4 is rejected: a transient failure must not be remembered.** "Telling it apart would be a phrase match" is not so: the branches are inside `_rebind` itself. A dry run that raised, `rc != 0` with no JSON, a refused write (the t-1937 table names a lock wait over which the writer exits non-zero) say nothing about the bytes. Today they are held until the bytes change, and the critic reads "nothing changed". Error direction wrong (FR-59). Fix: `_rebind` returns `(ok, words, stable)`; `stable=True` only for no author, a JSON `refusal`, "would not write", and unknown ids; `settle` records the `step: rebind` attempt only when stable. Grep the callers in the same change. Test `settle_retries_after_a_dry_run_that_did_not_run` (runner raises once, second settle calls it again).

**F10. FIX. (c) skips the scope check, and the report's "(b) unchanged" is false for it.** In `settle`, `_nothing_changed` returns before `scope` is computed. Input: dispatch A left `x` with `rebind`; critic B's scope excludes `x`'s case. The normal road says reason `scope` by `_scope_left`, with no subprocess; (c) says `rebind`, with a probe command spelled for B that `build_mine_request` refuses. Fix: compute `scope` first; `_nothing_changed` gets it and returns None when a non-critic item's case is outside it. The normal road still starts nothing for such an item (the scope check precedes the rebind). Test: `outcomes` empty, 0 runner calls, reason `scope`.

**F10a. FIX.** `_print_settle` prints `0 step(s)` on an unchanged settle, with no reason (the builder's own note). Add one line from `unchanged_since`.

Judged, no finding: decision 1 (memory crosses dispatches, not stories: right, the alternative makes (a) and (c) dead); decisions 2 and 3 (stricter skip, more stamp fields: the run direction); `same_bytes` reuse and `author` at N=3 (both queued in t-1937 section 2).

### TR3-8 (fill-new-account)

**F11. BLOCKS. E1c.6 does not hold on the live stand; Q1's condition is rejected.** The real recipe (tr-arm-b: `manual_capture.login` null, `login_recipe` gives `url_not ['/auth/sign-in', 'openid-connect']`) holds neither `/register` nor `/login`. So `watch` closes the window on the first step, and `_run_steps` empties `pending_new` before the password is typed. Measured through the test's own rig (`scratchpad\critic2060\signup_probe.py`):
```
A sign-in url, refused, later step fails : exit 1 last failed status ['unconfirmed'] password_of gives: False
B /register, refused, later step fails   : exit 1 last failed status [None] password_of gives: True
C /register, refused, no later step      : exit 0 last ok status [None] password_of gives: True
```
B and C are `EMAIL_TAKEN` on MyBooks: a refused account is an identity. Requiring `/register` in `url_not` is not an answer: a project fact nobody is told to write (P2), and with it the walker's `_with_pre_action` inserts a capture the open window refuses. C is the deeper defect: an unknown stays usable (FR-59). The DoD test passes only because its form sits on the sign-in URL.
Fix: record first, confirm on evidence.
1. `add(..., status=None)`; `_run_new_account` passes `UNCONFIRMED`, reason `the sign-up has not been seen to land`. `http` keeps None.
2. `pending_new` rows are `(name, path_at_add)`.
3. New `CreatedAccounts.confirm(name)`, under the lock, pops `status` and `reason` on both rows.
4. In `_run_steps` replace the `if not account.window` line: after an ok step whose word is not `goto`, when the current path is readable and differs from `path_at_add`, confirm and clear. The window keeps its own job. Do NOT add a `url_not` clause: a sign-up commonly lands on the sign-in page.
5. `resolve_actor` words: "its sign-up was refused or was not seen to land". `_settle_new_accounts` stays and overwrites the reason.
Tests: B and C above in `test_refused_signup_is_unconfirmed`; `goto` away is no proof; the existing landed control.
**Decision for the Lead:** an app that shows success on the same address stays unconfirmed. Safe direction; recommended door: a role's confirm word in N8 (P27, the role judges). The fix is executable without the answer.

**F12. FIX. Q2: `safe_to_break: "no"` makes accounts.** `_stand_may_change` passes any non-empty string; `"no"`, `"false"`, `"unknown"` pass, and `unknown` is how this onboarding records an unanswered lifecycle key (`p2-interview.md`, topic 3; for this key the form is not defined). E1c.4 direction is refuse. Real stands hold `true`. Fix: a data row `safe_to_break_no` in `manual-capture-steps.json`, `["no", "false", "none", "unknown", "n/a"]`, compared to the WHOLE stripped casefolded value (closed variety, FR-13; no phrase search, so FR-12 holds). Test: each row, plus SAFE's sentence as control. `env_probe.py:607` only prints the words: not the same question, no shared reader owed.

**F13. FIX. The `http` create route can now lose a password.** `manual_capture.py:4841` calls `store.add` AFTER a 2xx; its handlers are `StepTimeout` (a plain `Exception`) and `StepFailed`, so the new `TimeoutError` escapes with the user already on the stand. Breaks the E1c.2 invariant on the sibling caller; the report's "never lost" holds only for the new word. Fix: `add(..., wait_s=ACCOUNT_LOCK_WAIT_S)`; the route passes 300. Test: a held lock with a small wait raises by name; the row is written once released.

**F14. FIX. `secret` is not bound to the item.** `account.generated` survives across items of a walk (`SessionAccount` per actor is kept, `walk_session.py:860`). A `secret` in item 2 with no `user` types item 1's password; E1c.1 says "in the item". Fix: store `(attempt.case, name, password)`; a different case is the same refusal. Test in `test_secret_before_user_refused`.

**F15. FIX. The report says users that do not exist.** `report_facts.created_accounts_line` lists every name as "Users this story created on the stand", `unconfirmed` too. The report's "no reader needs them" is wrong, and F11 makes this common. Fix: leave `status: unconfirmed` rows out; add `; K sign-up(s) not confirmed` when K > 0. Add `report_facts.py` to this fix's owns.

## Standing questions

1. Fit to the spec: not met: F1, F2, F3 (TR3-2), F11, F14 (TR3-8), F10 (TR3-11).
2. Builder's decisions: rejected: TR3-8 Q1, Q2; TR3-11 decision 4; TR3-2's transcript reader. Accepted: the others, above.
3. Seams: additive, nothing reordered. `Driver.timed` wraps; `story_step.start` wraps.
4. Class-wide completeness: see Queue. F5/F6/F7 are the same class: producer changed, a reader left. The change check of AR-22 stopped at what the spec's list named. Map walk: axis 5 (twins): S6 sites untimed, by the spec's scope. Axis 18: below. Axis 32: below.
5. Tests: the named mutations read against their rows are killed. Gap: three DoD tests pin only the scenario where the design works (F1's patched reader, F11's form on the sign-in URL). Requested tests in the fixes close them.
6. DUPLICATION AND CONSISTENCY: `_locked` is a ninth msvcrt/fcntl copy: `execution_scheduler._file_lock` has no timeout (`LK_LOCK`, `LOCK_EX`), `event_store` :300 `lock(wait_seconds)` is a method of the store, so no direct reuse; queued, Q2. `_type_new_value` vs `_run_fill`: not reusable, `_run_fill` keeps rows holding the value; acceptable. `driver_timing._rows` vs the repo's jsonl readers: counted-problems shape is its own; acceptable. Grep over the package: `def .*lock`, `read_jsonl`, `hashlib.sha256(.*read_bytes`.
7. CODE QUALITY: `_locked` has four nesting levels (`manual_capture.py` 788-821, goes with Q2). `settle` keeps growing past 60 lines (old; +45): queue with TR3-15, which already reopens it. `MODES`: F7a. No new function over 60 lines otherwise.
8. Hygiene: the builders' `--lang` PASS read for TR3-2, TR3-8; line endings not separately checked; the integrator's `--limits --lang` is the canon.
9. IN-TREE RATCHETS: no ratchet row added or raised by any diff stat. `slow_tests.json` +1 row (an estimate, not a ratchet). The `forge-check` job (clones, lint) was not attached: read it on the branch pipeline before acceptance.
10. ARCHITECTURE: named AR-n are in the commits. Touched and broken: AR-22 and AR-13 by F5, F6, F7; AR-28 by F11, F9; AR-6-style starved reader by F1. TR3-2's report wrongly names a `wall_ms` reader.
11. JUDGMENT: no census or scan-constant edit (no such file in the diffs). `judgment: none` holds for TR3-7, TR3-2, TR3-11. TR3-8: code marks and confirms from data (a failed step, a path change), and `created:` refuses on a recorded status: a data check, spec-mandated; whether a same-address app's sign-up worked stays the role's (the N8 fork). TR3-8's census run: `908 units`, no new row. The other three did not run the census: CI.

## Queue (lines for «Остатки», as is)

- Q1. `fill-new-account joins the sign-in word sites: walk_session _with_pre_action (:1081), first_action_row (:401), preload (:1031); manual_capture run_ui (:2985, :2989), _account_steps_gate; manual-capture-steps.json final_also_actions | узел: N8`
- Q2. `one public OS-lock helper with a timeout replaces the nine msvcrt/fcntl copies (AR-15) | перенос: findings/<new file> | обоснование: touches eight modules outside these nodes | подтвердил: —`
- Q3. `settle over 60 lines, split when the debt goes per dispatch | узел: TR3-15`

For the Lead, outside any owns: `plans/features.json` lacks `driver_timing.py` (commit WARN). TR3-8's report says its worker ran another worker's mutation probe against `wt-tr1-2` for about a minute: that owner should check the tree and any run overlapping it.

## Fix worker

One worker, four branches, one fix commit each (a fix diff is re-reviewed with this verdict only). Fast witnesses: `test_driver_timing.py`, `test_stand_lease_walk.py`, `test_stand_lease.py`, `test_walk_places.py`, `test_probe_debt.py`, `test_fill_new_account.py`, `test_manual_actor.py`. CI judges `test_launch_card.py`, `test_task_root_parsers.py`, `test_install_retire.py`, `test_story_run_wait.py`, `test_story_step_start.py`.

## Spot-checks

- Witness rerun: `test_stand_lease_walk.py` `9 passed in 3.86s`, matches the report. The others by consistency: test counts match the diffs' rows.
- Negative "no other reader of the lease shape" (TR3-7): refuted, F7. Grep `stand_lease\.|stand-lease|process_started_at` over the package.
- `state()` claim (TR3-2): verified, `dispatch_liveness.py` 937-943.
- `parse_prompt` ignores the lines (TR3-2): verified; the stop prefix is at `launch_card.render`, which ends in a newline, so `parse_lines` sees them.
- Negative "no stdout pins" was the open question: refuted, F3. Same-shape grep over `test_launch_card.py`.

## Trail

Read: the brief; t-1937 sections 2 and P2-2's first text; t-1957 N1b, N1c; four reports; full code diffs of the four branches; `driver_timing.py`; `stand_lease.py` 85-135, 262-312; `onboard_apply.py` 112, 189-212, 330-352, 1009-1022; `walk_session.py` 395-408, 795-830, 900-935, 1064-1090; `probe_debt.py` 320-346, 486-560, 770-832; `manual_capture.py` SessionAccount, 738-770, 2983-2994, 4826-4885; `dispatch_liveness.py` transcripts, thresholds, 925-950; `hooklib.py` story_subagent_transcripts, subagent_meta, append_jsonl_line; `launch_card.py`; `report_facts.py` 925-945; `test_fill_new_account.py`; `test_task_root_parsers.py` 28-40, 157-163, 296-304; `test_launch_card.py` 258-272.

Runs (verbatim above):
- `python -B wt-tr3-7/.../tests/test_stand_lease_walk.py`: `9 passed in 3.86s`
- `python -B wt-tr3-7/.../tests/test_walk_places.py`: `KeyError: 'job_id'`
- Probes in `scratchpad\critic2060\`: `note_probe.py`, `lease_exec_probe.py`, `stand_facts.py`, `stand2.py`, `signup_probe.py`, `census_probe.py` (temp projects; the stand copies only read).
- `git merge-tree --write-tree --name-only` for six pairs: one tree id each, no conflict names. This leaves unreferenced objects in the shared object store; no ref moved.

Not done: the slow files (non-goal); the mutation runs; `forge-check` (not attached). Own hygiene: one `cd` and one trailing `2>&1` in my commands (warnings, no effect on any tree).

Needed beyond the manifest: `onboard_apply.py`, `dispatch_liveness.py`, `hooklib.py`, `report_facts.py`, `test_walk_places.py`, `test_task_root_parsers.py`, `test_launch_card.py`, the stand copies under `D:/ws1/mybooks-stand`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F1 TR3-2: the silence watchdog reads subagent transcripts only; 0 of 207 role dispatches matched on four real runs, it can never speak",
    "F2 TR3-2: t-2034 M2 not built, the watchdog prints through print and is lost under redirect_stdout; the named test is absent",
    "F3 TR3-2: t-2034 mode gate not built, timing lines on every road; test_launch_card.py:272 byte pin goes red; two named tests absent",
    "F4 TR3-2: test_task_root_parsers census red, declared-not-expected driver_timing",
    "F5 TR3-7: _holder_state no longer reads process_started_at; a recycled pid in execution-leases.json now reads as a live lock in onboarding",
    "F6 TR3-7: the released_by_person note carries pid; onboard_apply._holders reads it as a live lock and --release answers not_held",
    "F7 TR3-7: test_walk_places.py:72 reads the old shape, KeyError job_id",
    "F11 TR3-8: E1c.6 fails where the sign-up page is outside url_not, which is the live stand; a refused account stays an identity; also when no later step fails"
  ],
  "class_completeness": "Merge: clean on all six pairs. Class 'producer changed, a reader left' (AR-22) had three instances, F5 F6 F7, all in the fixes. The surface of F2 (driver prints under redirect) walked: wall note and timing notes join the fix. The surface of F11 walked: F13 sibling caller of add, F14 item binding, F15 report reader. Queued with executors: Q1 word sites to node N8, Q2 lock helper by finding, Q3 settle size to TR3-15. Axis 5: S6 sites untimed by the spec's scope. Axis 18: no ratchet raised. Axis 32: no census change, judgment lines hold.",
  "fixes": [
    "F1 dispatch_liveness.session_transcripts over the parents of state/cost transcript paths; last_write matches by subagent_meta dispatch_id; test silence_reads_the_main_transcript; witness on mybooks-stand tr-arm-b",
    "F2 driver_timing.console through sys.__stdout__ for watch, the wall note and timing_write; test silence_line_survives_redirected_stdout",
    "F3 print timing lines only when current_run_mode() is driver; tests timing_lines_not_in_card and timing_lines_absent_on_skill_road",
    "F4 add driver_timing to B_SCRIPTS with a battery row, and to audit_factory CLI_SCRIPTS",
    "F4a driver_timing._rows errors=replace, with a raw bad byte in the test",
    "F5 _holder_state reads started or process_started_at; control row in test_install_retire.py",
    "F6 rename the note key to held_pid; test in test_install_retire.py",
    "F7 test_walk_places.py:72 reads holders[].job",
    "F7a delete MODES; correct env-facts-baseline row #15 text",
    "F8 stamp gains manifest_ids; test settle_retries_when_manifest_ids_change",
    "F9 _rebind returns stable; only stable kept rebinds are remembered; test settle_retries_after_a_dry_run_that_did_not_run",
    "F10 compute scope before _nothing_changed; an out-of-scope non-critic item returns None; test reason scope with 0 runner calls",
    "F10a _print_settle says unchanged_since",
    "F11 add with status unconfirmed, confirm when a non-goto ok step shows a path other than the form's; resolve_actor words; tests for scenarios B and C and goto",
    "F12 data row safe_to_break_no compared to the whole value; test each row and a control",
    "F13 add takes wait_s, the http route passes 300; test",
    "F14 generated pair stores attempt.case; a different case refuses; test",
    "F15 created_accounts_line leaves out unconfirmed and counts them; report_facts.py joins the owns"
  ],
  "trail": {
    "read": [
      "docs/tasks/critic-diff-brief.md",
      "docs/tasks/specs/t-1937-s5-parallel-windows.md section 2 and P2-2 first text",
      "docs/tasks/specs/t-1957-fast-manual-walker.md N1b N1c",
      "reports t-2042 t-2043 t-2047 t-2051",
      "full code diffs of tr/tr3-7 tr/tr3-11 tr/tr3-2 tr/tr3-8 against 77b448a3e",
      "scripts: driver_timing stand_lease onboard_apply walk_session probe_debt manual_capture dispatch_liveness hooklib launch_card report_facts env_probe execution_scheduler",
      "tests: test_fill_new_account test_task_root_parsers test_launch_card test_install_retire test_walk_places"
    ],
    "reruns": [
      {"command": "python -B wt-tr3-7/ai-packages/qa-factory/scripts/tests/test_stand_lease_walk.py", "result": "9 passed in 3.86s"},
      {"command": "python -B wt-tr3-7/ai-packages/qa-factory/scripts/tests/test_walk_places.py", "result": "KeyError: 'job_id' at line 72"},
      {"command": "python -B scratchpad/critic2060/note_probe.py", "result": "after release: stand-lease.json unknown pid 34468; release again: not_held"},
      {"command": "python -B scratchpad/critic2060/lease_exec_probe.py wt-tr3-7 and wt-tr3-2", "result": "tr3-7 execution-leases.json unknown; base code no lock"},
      {"command": "python -B scratchpad/critic2060/stand_facts.py", "result": "transcripts 0, matched 0 of 55, 56, 64, 32 role dispatches"},
      {"command": "python -B scratchpad/critic2060/stand2.py", "result": "url_not /auth/sign-in, openid-connect; 94 main transcripts, 0 subagent; dispatch ids readable from main"},
      {"command": "python -B scratchpad/critic2060/signup_probe.py", "result": "A unconfirmed; B status None, password_of True; C status None, password_of True"},
      {"command": "python -B scratchpad/critic2060/census_probe.py", "result": "declared-not-expected: driver_timing"},
      {"command": "git merge-tree --write-tree --name-only, six pairs", "result": "one tree id each, no conflict"}
    ]
  }
}
```
