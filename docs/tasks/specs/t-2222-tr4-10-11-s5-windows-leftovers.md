# t-2222 — TR4-10 and TR4-11: S5 window leftovers (critic t-2121 Q1-Q5, Q7, Q-new-1, Q-new-2, t-2095 N1/N2)

Draft by the designer (dispatch t-2222). The decisions this spec carries are the Lead's, `docs/tasks/handoffs/20261110-lead-window-acceptance.md`
section 3 (rows Q1-Q5 -> TR4-10; Q7, Q-new-1, Q-new-2, t-2095 N1/N2 -> TR4-11). Forks are in §6; nothing there is decided here.
`S` = `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts`. Line numbers are the tree of `wt-fbfix` read on 10.11.2026.

## 0. Facts read before writing (freshness; each read in its carrier)

- **Q1 is half landed already.** `story_run.py:3217-3219` (`finish`): after the accepted finish of the stage's closing role
  (`WINDOW_ROUND_STAGES[S5]`, the critic) it calls `s5_release_of_dispatch(dispatch)` (:11611-11626, docstring "Q1"), on every road
  that finishes a critic (chain, old body, `s5_close_debt`, the recovery finish). Pinned by `test_driver_chain.py`
  `closing_finish_releases_the_window` (:940-953). What is NOT covered: an S5 that completes by a finish of ANOTHER role (the
  author's mechanical round, `complete=last()`, finished on a recovery road after the driver died: the chain release after
  `s5_window` never runs, and the critic branch at :3218 does not fire). See fork F1.
- **The scheduler is no longer in `story_run.py`.** `session_gate` (:291), `count_launch` (:257), `stop_if_drained` (:252),
  `run_chains` (:324) and `_interrupt_chains` (:403) live in `S\driver_chains.py` (TR3-9a, `class DriverChains`, base of `Driver`).
  The batch row TR4-10 names `story_run.py (session_gate)` and TR4-11 names `story_run.py (_interrupt_chains)`: both stale.
- **Ctrl-C today.** `story_run.py` has no `except KeyboardInterrupt` (grep `KeyboardInterrupt` over `S\*.py`: hits only in
  `driver_chains.py` and tests; positive control: the same grep finds `driver_chains.py:218`). Serial road: `_launch` kills the child
  (:1947-1949), `clear_in_flight` runs in its `finally` (:1954), the exception leaves `Driver.run` (:17066-17230) uncaught. Parallel road:
  `run_chains` sets the drain, `_interrupt_chains` kills, joins, re-raises (driver_chains :371-396) up to `Driver.run`. Either way the
  only trace is a `launched` row (`run_claude` :2074) with no end row - exactly what `collect_stall` K3 reads as a dead driver
  (`collect_stall.py:214-239`). K2 does not fire (the `in_flight` entry is cleared).
- **Axis 29 in the driver.** The one direct appender is `_append_jsonl` (`story_run.py:581-584`, plain `open("a")`), used by
  `journal_run` (:1569), `journal_conductor` (:1572), `driver-questions.jsonl` (:4526), `driver-answers.jsonl` (:5598, :7443).
  Grep `open\([^)]*["']a\+?b?["']|mode\s*=\s*["']a` over `story_run.py, driver_*.py, collect_stall.py, window_files.py`: one hit, :583
  (it is its own positive control). `timing_write` (:1966-1978) already calls `hooklib.append_jsonl_line`.
- **Q4.** `s5_auto_extra` (:11657-11673) gives the ownership line only when `chain=True`; the old body calls it with `chain=False`
  (:11803). The guard enforces claims whenever `config_contract.parallel_windows(cfg)[0] != 1` (`guard_pre_tool.py:1588-1589`).
- **Q2.** `s5_open_windows` (:11522-11556) opens a window on: no accepted critic, a RUNNING dispatch meeting its scope, an owed round
  or debt, a live chain. No clause reads `returned_unaccepted` (`controller.RETURNED`, `controller.py:157`).
- **Q5.** `state-exits.md:23` describes the stage beside a running window and says the last running window's accept writes
  "`pending`, or `completed`"; no row says that `pending` can stand beside a `blocked`/`paused` sibling, and no test pins it.
- **Q7.** `test_judgment_census.py` prints `BLIND_SPOT` (:446-447) with the totals (:496-497); the module docstring has a BLIND SPOTS
  paragraph (:32-34); `judgment-census.json` line 3 `about` names neither the subclass gap.
- **Nits.** t-2095 N1: `S\..\changelog.d\tr3-14-hook-readers.md` line 1, "(measured worst case 31.2 seconds)". N2:
  `s5_precheck.py:4265`, comment "(b): ... a name that fits neither is None (never the count rule)".
- **TR3-9 C.** No shell tool was available to this designer, so `git diff --stat` of `wt-tr3-9c0/c1/c2` was NOT run. What stands in
  for it: the owns of `docs/tasks/specs/t-2147-tr3-9-walker-lanes.md` §C0-C2 (:287-379) and a grep of the worktrees. C0 owns
  `fixtures/s6-w1-frozen/`, `test_story_run_s6_w1_frozen.py` (exists in `wt-tr3-9c0`), `slow_tests.json`. C1 owns in `story_run.py`
  `run_manual_block`, `manual_lane_plan`, `run_manual_lane`, `stage_S6`, `walk_before`, `s6_walkers_cap`, `s6_serial_reason`,
  `s6_settling_lanes`, `s6_lane_holds`, `s6_chain_kind`, `s6_open_lanes`, `s6_seam`, `run_s6_lanes` (all found in `wt-tr3-9c1`), plus
  `fixtures/driver-layers.json`, `walk_session.py`, `design/state-exits.md` (one row), `fixtures/judgment-census.json` (one row),
  `changelog.d/tr3-9c-walker-lanes.md`. C2 owns `validate_artifacts.py` `_s6_runner_half`. In `wt-tr3-9c1`, `driver_chains.py`
  `stop_if_drained`/`count_launch`/`session_gate` are at the same lines and bodies as `wt-fbfix` (not changed by C1). The S5 members
  sit 2 lines lower in `wt-tr3-9c1` than in `wt-fbfix` (something between `finish` :3131 and `s5_open_windows` grew by 2 lines; by the
  owns it is `walk_before`) - the builder confirms with `git -C D:/ws1/wt-tr3-9c1 diff origin/experiment/thinking-roles --stat`
  before starting (estimate, not verified).

## 1. AR-n touched, the check of each, owners and census classes (designer rule 1; AR-29)

| AR | how it is touched | change check written into the DoD |
|---|---|---|
| AR-13 one reader | Q4 reads N through `config_contract.parallel_windows` (the guard's reader); Q2 reads the status word through `controller.RETURNED` and the plan part through `controller.s5_part_of` | grep `parallel_windows` in the diff: every new read calls `config_contract.parallel_windows`; no literal `"returned_unaccepted"` in `story_run.py` |
| AR-14 one writer | `driver-runs.jsonl` keeps one writer (`journal_run`); `state/window-files/` keeps one writer (`window_files`) | the stop record is written only through `journal_run`; the stage release only through a `window_files` function |
| AR-15 / axis 29 one survivor | `_append_jsonl` goes through `hooklib.append_jsonl_line` | `test_driver_stop_record.py::story_run_has_no_private_appender` (source scan with a positive control) |
| AR-17 one seam | Q3: a gated chain stopped by the drain ends `Drained`, the seam after the join stays the one place that raises | `test_driver_chain.py::gated_session_does_not_start_after_drain` |
| AR-19 twins (axis 5) | Q3 lands in the generic `session_gate`, so S6 lanes inherit it; Q2's S6 twin is `s6_open_lanes` (TR3-9 C1, edge C.6 already counts a returned lane as open); Q4/Q1 have no S6 twin (S6 claims no files) | the report and the commit name the twins in one line each |
| AR-22 producer/reader | the stop record: producer `Driver.person_stop_record` (story_run), reader `collect_stall._k3_k4`; ONE commit (part B1) | both keys of B1 in one commit; the builder greps readers of `driver-runs.jsonl` (`grep -n "driver-runs" S\*.py`, positive control: `collect_stall.py`) and names each with one line: passes the new row by, or reads it |
| AR-25 way out | Q1: a claim of a completed S5 has a way out on every road; Q5: a `state-exits.md` row for `pending` beside a stopped window | `test_state_exits.py` green; the row names the way out |
| AR-28 unknown never a pass | Q2: an unreadable returned dispatch is open; Q1: an unreadable stage releases nothing; K3: an unreadable stop record is `unreadable` | the edges below, each with a key |
| AR-10 requirement before the work | Q4: the role is told of the guard's claim rule on both bodies | `test_s5_window_leftovers.py::ownership_line_on_old_body_when_n_not_1` |
| AR-20 ratchets | no ratchet is raised by this spec; a census unit a part adds is named row by row | the `judgment:` / `architecture:` commit lines; `test_judgment_census.py` green |
| AR-29 judgment | no check here reads a role's text, verdict or form content | census classes below |

Checks added or altered (owner it serves; census class):

| check | owner | census class |
|---|---|---|
| Q2 returned clause of `s5_open_windows` | data (code) | xref (dispatch status x window scope). Not a census unit today: it raises `WindowsUnreadable(ValueError)`, which the scanner cannot see (that is Q7's blind spot); if C1 of the census lists it, its row is xref / owner data |
| Q1 `s5_release_completed` (decides to free claims) | data (code) | xref (stage status x dispatch statuses); no refusal site, not a unit |
| Q3 drain test inside `session_gate` | data (code) | shape (a flag); `Drained` is not a refusal the scanner counts, not a unit |
| K3 stop-record clause in `collect_stall` | data (code) | xref (stop row x launched row); no refusal, not a unit |
| Q4, Q5, Q7, Q-new-2, N1, N2 | — | no check added or altered (a brief line, a doc row and a pin, a printed blind spot, an appender, text) |

FR sections: A (FR-2, FR-57: Q1 removes a needless refusal; Q3), C (FR-38: Q4), D (FR-40: Q5; FR-59: Q2, Q1), F (FR-28: the K3 change
gets tests; FR-41: N1 "computed, not measured"), G (FR-30 English, FR-32). B (text to a person) - not changed. E - not changed.

## 2. TR4-10 — S5 windows (Q1-Q5)

### Item 10.1 (Q1) — claims freed when S5 completes, whichever road closed it (scope: fork F1, written to recommendation (b))

- File/function: `story_run.py` `finish` (one call, right after the existing :3218-3219 block, inside `if complete is True`), new
  `Driver.s5_release_completed()`; `window_files.py` new `release_stage(task_root, stage) -> int`.
- Behaviour: after a successful `story_step finish` with `complete is True` and `stage == "S5"` (ANY role), `s5_release_completed()`:
  (1) `config_contract.parallel_windows(self.config)[0] == 1` -> return before any read (nothing was claimed); (2) no claim file in
  `task_root / window_files.SUBDIR` -> return; (3) read `self.controller_state()`; free every S5 claim (`window_files.release_stage(task_root,
  "S5")`: every claim whose `window` starts with `S5|`, plus the empty-claim rule `release` already has) ONLY when `stages.S5.status ==
  "completed"` AND no S5 dispatch is `running`, `blocked` or `paused` (`dispatch_identity.records`); otherwise nothing; (4) a claim left
  after the release, or an exception: one `note:` line, never a stop (P1), same words as `s5_release`.
- INVARIANT: a claim of a window that can still write is never freed (a running/stopped S5 dispatch, or a stage not `completed`, keeps
  every claim); a completed S5 never leaves a claim that refuses a later S5 rework's automator.
- Error direction: releasing late is safe (a refusal with the door "new file"); releasing early is not (two windows on one file).
  Adversarial inputs that must stay on the safe side (release nothing): `stages.S5.status` absent / `"running"` / `"pending"` / not a
  string; `controller.json` absent or unreadable (`_read_json` gives `{}`); `dispatches` not a mapping or list; a stage `completed` beside
  a `running` S5 rework (state-exits.md:37: a rework does not lower the stage); a `blocked` sibling.
- Edges: absent state file -> `{}` -> nothing released, no note. N == 1 -> returns first, no read (the frozen N=1 set must stay equal).
  A window with no dispatch rows -> irrelevant (the rule reads the stage and the running set, not windows). The existing per-window
  release at :3219 stays as it is (a window closing while S5 still runs).
- Tests: `S\tests\test_s5_window_leftovers.py` (new, fast) keys `stage_completed_by_author_finish_frees_every_s5_claim`,
  `stage_completed_beside_running_rework_frees_nothing`, `unreadable_stage_frees_nothing`, `n1_reads_nothing`;
  `S\tests\test_guard_window_files.py` key `released_stage_claim_no_longer_refuses` (after `release_stage`, an automator of a later
  dispatch writing the old file gets no "until that window closes" refusal - the Lead's test wording, guard side). The existing
  `test_driver_chain.py::closing_finish_releases_the_window` stays green.

### Item 10.2 (Q2) — a window whose last dispatch is `returned_unaccepted` is open

- File/function: `story_run.py` `s5_open_windows`.
- Behaviour: one more OR clause per window: take the S5 dispatch records (`dispatch_identity.records`, `s5_part_of(r) != "plan"`) whose
  scope meets the window's cases, drop those whose status is in `controller.DISCOUNTED`, keep record order (fork F5: the order of the
  controller's mapping); if the LAST of them has status `controller.RETURNED` -> the window is open. A returned record with no scope
  -> `WindowsUnreadable` (the twin of the running clause :11539-11540; callers read it as open).
- INVARIANT: no finish closes S5 while a window's last round came back unaccepted (the critic's counter-scenario: critic accepted with
  route `mechanical`, the author's mechanical rework `returned_unaccepted`, another window's finish must not close S5); an unreadable
  state is open, never a close (FR-59).
- Error direction: may say open needlessly; that costs a stage that does not close (the seam's stuck question after `STUCK_REPEATS`),
  never a silent close. Adversarial inputs: a returned PLAN dispatch (ignored); a returned dispatch whose scope meets two windows (both
  open); a returned round followed by a later accepted dispatch of the same window (closed, if its critic is accepted); a returned
  dispatch of the `excluding` window (skipped with its window); a `superseded` record after the returned one (dropped, the returned one
  is last -> open).
- Edges: absent state file -> `WindowsUnreadable` as today. A window with no dispatch rows -> the clause is False; the other clauses
  decide as today. N == 1: the serial `completion_for` reads the same function, so the gap closes there too (the critic's "the spec
  meant to close it"); the frozen N=1 set is judged by CI and must stay equal - a red there is a fork back, never a re-pin.
- Tests: `test_s5_window_leftovers.py` keys `returned_mechanical_round_keeps_window_open` (the critic's scenario, through
  `s5_last_fn` of the other window), `later_accepted_dispatch_closes_returned_window`, `returned_plan_dispatch_ignored`,
  `returned_without_scope_is_unreadable`.

### Item 10.3 (Q3) — a chain waiting in `session_gate` does not launch after the drain began

- File/function: `driver_chains.py` `DriverChains.session_gate`, `DriverChains.count_launch` (fork F4, written to recommendation (a)).
- Behaviour: inside the `while` loop of `session_gate`, a chain that has had to WAIT (blocking was non-empty at least once in this call)
  raises `Drained` when `self._drain.is_set()` - checked before each `self._cond.wait` and again after it. A chain that reaches the gate
  with nothing blocking passes as today. Exemption: the chain whose own `count_launch` started the drain (`--max-boundaries`) still
  launches: `count_launch` records the number of the chain that set the flag (a plain attribute set under `_book`, e.g.
  `self._drain_by = record.n`, cleared in `run_chains` beside `_drain.clear()`), and the gate does not raise for that chain.
- INVARIANT: after the drain no session STARTS for a chain that was waiting (the person's question is not held behind a whole extra
  session); "the one that counted still runs" (`count_launch` docstring) keeps holding; a running session is never stopped by this.
- Edges: a drain started while a chain waits -> that chain ends `Drained`, `record.exception` None, its dispatch stays registered and
  `running` with no process and a `launched` row with no end row - the same state as a driver stopped between `start` and the process;
  re-entry handles it by today's road (the builder names that road in one report line, function and line; no code for it). The
  `launched` row is read by K3 as "may be running" until the next entry writes an outcome row for the same dispatch: accepted (an extra
  transcript is collect_stall's safe side). N == 1 / one window: no chain, `session_gate` is never entered. S6 lanes: unreachable by
  their exclusive start gate (t-2147 C.7), inherited if ever reached.
- Residual the builder checks (report lines, no edit outside owns): grep `except Exception|except BaseException` on the path
  `run_role` / `rework` / `resume_role` -> `run_claude` -> `launch` (`run_claude` :2004-2240 and `run_role` :2970-3130 hold none);
  a catch that would swallow `Drained` raised from `launch` is a fork back, not a fix.
- Tests: `S\tests\test_driver_chain.py` keys `gated_session_does_not_start_after_drain` (chain 2 waits behind chain 1's running
  session, the drain is set, chain 1's session ends: chain 2's fake `_launch` is never called, chain 2 ends with `exception is None`),
  `counting_chain_still_launches_after_its_own_drain`, `ungated_chain_unchanged_by_drain_flag`.

### Item 10.4 (Q4) — the ownership line on both bodies at N != 1

- File/function: `story_run.py` `s5_auto_extra`.
- Behaviour: the line "Other windows of this story are written at the same time. A test file one of them wrote first refuses ..." is
  appended when `config_contract.parallel_windows(self.config)[0] != 1`, whatever `chain` says; the "stand busy" line stays
  `chain`-only. Text unchanged byte for byte.
- INVARIANT: the brief says what the guard enforces, read by the guard's own reader, so the two never disagree (a bad config value
  reads the default with its note in both); at N == 1 the list is byte-equal to today (the frozen N=1 set).
- Edges: config absent / bad value -> the default (not 1) -> the line is given and the guard enforces. `chain=True` -> both lines, as
  today. No `self.config` attribute on a test rig -> the builder reads it as `{}`, never raises.
- Tests: `test_s5_window_leftovers.py` keys `ownership_line_on_old_body_when_n_not_1`, `n1_extra_unchanged`,
  `line_iff_guard_enforces` (for values 1, 2, 3, "x", absent: line present iff `parallel_windows(cfg)[0] != 1`).

### Item 10.5 (Q5) — `pending` beside a stopped window, pinned (no behaviour change)

- Files: `design/state-exits.md` one new row right after row 23 (`stages.S5.status = running` while ...); `S\tests\test_s5_parallel_admission.py`
  one key.
- Row text (state | entered | way out | proven by): "`stages.S5.status = pending` while an S5 window dispatch is `blocked` or `paused`
  (the last RUNNING window accepted beside a stopped sibling, t-2121 Q5; stage readers no longer see the stopped window, dispatch readers
  do; no reader depends on it, 10.11.2026)" | "`accept` of the last running S5 window while a sibling is `blocked`/`paused`" | "the
  stopped window leaves by `resume`, a retry (`recover`), a rework or `release`; `stage_S5` re-enters on `pending` and reads the stopped
  dispatch as an entry-state reason (`S5_SETTLE_RUNNING`)" | "`test_s5_parallel_admission.py`".
- INVARIANT: the state is named so the next reader meets it; nothing in the controller changes.
- Edges: absent state file -> n/a (a fixture state). N == 1 -> the state cannot arise (one running dispatch).
- Test: `test_s5_parallel_admission.py` key `stage_pending_beside_blocked_sibling` (W1 checkpointed `blocked` beside running W2,
  stage reads `running`(W2); W2 accepts; stage reads `pending`, W1 still `blocked`).

## 3. TR4-11 — small window and census leftovers

### Item 11.1 (Q-new-1) — a named "stopped by the person" record, read by K3 (forks F2, F3; written to recommendations (a), (a))

- Files/functions: `story_run.py` `Driver.run` (first statement `self.run_started = _now()`; one `except KeyboardInterrupt:` clause on
  the existing `try` at :17070 that calls `self.person_stop_record()` and re-raises), new `Driver.person_stop_record()`;
  `collect_stall.py` `_k3_k4` and the module docstring's K3 line.
- Not in `_interrupt_chains` (the batch row's place): it is the generic scheduler in `driver_chains.py`, knows no story and covers the
  parallel road only; `Driver.run` is where both roads' `KeyboardInterrupt` arrive.
- Record: one row through `journal_run` (so `ts` is added there): `{"kind": "stopped_by_person", "who": "person", "at": <_now()>,
  "since": <self.run_started>}`. No `dispatch`, `session_id`, `total_cost_usd`, `exit_code`, `is_error`, `infra`: the readers that bind
  sessions, prices or outcomes pass it by (as the `launched` row, :2062-2071).
- K3: a `launched` row R (not live, no later outcome) is NOT a K3 signal when a later row S in the file has `kind == "stopped_by_person"`,
  `who == "person"`, and `since` (epoch) <= R's `started_at` (else `ts`); R then goes to `ignored` with `why: "stopped by the person at
  <S.at>"`. S with `since` or `at` present and not a time -> a reason (`unreadable`), R stays judged as today. S with `since` absent, or
  `who` not `"person"` -> not honoured.
- INVARIANT: a dead driver is still a stall (a `launched` row with no stop record after it, or one launched before the stopping
  process began, or one launched AFTER the stop row, stays K3); only the calls the stopping process itself cut off are told apart.
- Error direction: clearing a K3 is the unsafe side (a missing transcript). Adversarial inputs that must stay K3: stop row BEFORE the
  launched row in the file; a launched row of a dead earlier process, started before `since`, stays K3; a launched
  row of a LATER process after the stop row; `who: "conductor"`; `since: "yesterday"` (unreadable -> stalled anyway).
  Named residual: two driver processes on one story at once (A launches after B started, A dies, B is stopped): B's record clears A's
  row. The `cut` list of fork F3 (b) closes it; not taken by recommendation.
- Edges: Ctrl-C with no story state dir (`self.state_dir` not a directory) -> nothing is written (a Ctrl-C never creates the story's
  folder; there are no `launched` rows to tell apart either). Ctrl-C before `run()` (in `Driver.__init__`, argparse) or during the
  header `progress_line` at :17067 -> no record (no call was launched). The write fails (`OSError`) -> one `note:` line, the
  `KeyboardInterrupt` still re-raises. A second Ctrl-C during the write -> the record may be absent: K3 reads a dead driver (safe side).
  `driver-runs.jsonl` absent -> created by the appender as today (only when the state dir exists). No new console line; exit as today.
  Absent `driver-state.json` -> irrelevant to K3. N == 1 vs N != 1: the same record on both roads.
- Tests: `S\tests\test_driver_stop_record.py` (new, fast) keys `ctrl_c_serial_writes_one_stop_record` (a rig whose
  `reconcile_question` raises `KeyboardInterrupt`: one row, re-raised), `ctrl_c_parallel_road_writes_one_stop_record` (the
  `KeyboardInterrupt` out of a faked `stage_S5`/`run_chains`), `no_state_dir_writes_nothing`; `S\tests\test_collect_stall.py` keys
  `k3_cleared_by_stop_record_of_same_process`, `k3_kept_without_stop_record`, `k3_kept_for_row_before_since`,
  `k3_kept_for_row_after_stop`, `k3_unreadable_stop_record_is_unreadable`, `k3_stop_record_of_other_who_ignored`.

### Item 11.2 (Q-new-2, axis 29) — the driver's appender goes through the one appender

- File/function: `story_run.py` `_append_jsonl` (body only): `hooklib.append_jsonl_line(path, json.dumps(record, ensure_ascii=False))`.
  Callers unchanged.
- INVARIANT: one torn-tail rule (AR-15); a line is never glued to a torn tail; `OSError` still reaches the caller as before
  (`journal_run`'s caller at :2077 catches it).
- Edges: a file that ends without `\n` -> the new row starts on its own line. A file absent -> folder and file created (as before).
  `json.dumps` never emits a raw `\n`, so `append_jsonl_line`'s `ValueError` cannot fire.
- Tests: `test_driver_stop_record.py` keys `append_jsonl_repairs_torn_tail`, `story_run_has_no_private_appender` (AST/regex scan of
  `story_run.py` for `open(..., "a")` finds none; positive control: the same scan finds one in a fixture string).
- Analog reported, not widened: `story_run._read_jsonl` (:587-603) splits with `splitlines()`, which also splits on U+2028 / U+0085
  inside a string (`collect_stall._jsonl_rows` splits on `\n` only).

### Item 11.3 (Q7) — the census blind spot printed

- Files: `S\tests\test_judgment_census.py` (`BLIND_SPOT` text and the docstring BLIND SPOTS paragraph), `S\tests\fixtures\judgment-census.json`
  (`about` only). The scanner (`refusal_registry.sites`) is NOT changed.
- Text (both places, same sense): "a subclass of `ValueError` or `StateConflict` raised by its own name is invisible to
  `refusal_registry.sites` (it matches the literal names); legitimate when the subclass is caught and never reaches a role, but a
  subclass chosen to keep a ratchet down is not seen - the critic's question 11 and calibration check 41 catch it".
- INVARIANT: the census counts do not change (no row, no class, no total moves).
- Test: `test_judgment_census.py` key `blind_spot_names_subclass_gap` (asserts `BLIND_SPOT` and the fixture `about` both carry
  "subclass"); the whole file green (28 s).

### Item 11.4 (t-2095 N1, N2) — text

- `changelog.d/tr3-14-hook-readers.md`: "(measured worst case 31.2 seconds)" -> "the return waits up to 31.2 seconds (three tries,
  computed, not measured) and the projection refresh up to 10 seconds".
- `s5_precheck.py:4265` comment: "a name that fits neither" -> "a held name that fits neither ... (an unheld name falls to the count
  rule in `own`)".
- Test: none new (text); `test_s5_precheck.py` green, `selftest.py --lang` is the integrator's.

## 4. Builder parts (D-0048: disjoint function lists in `story_run.py`)

Header lines per part are for the dispatch; the coordinator copies each block.

### Part A1 — TR4-10 driver side (items 10.1, 10.2, 10.4)
given: this spec; `D:/ws1/wt-fbfix\ai-packages\qa-factory\design\factory-rules.md`; `D:/ws1/wt-fbfix\plans\builder-rules.md`; `D:/ws1/wt-fbfix\docs\tasks\specs\reviews\t-2121-critic-tr3-6.md` (Q1, Q2, Q4)
owns:
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\story_run.py` (functions: `s5_open_windows`, `s5_auto_extra`, `finish` (one call line after :3219 only), new `s5_release_completed`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\window_files.py` (new `release_stage` only)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_s5_window_leftovers.py` (new)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_guard_window_files.py` (one key)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\driver-layers.json` (the row of `Driver.s5_release_completed`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\tr4-10-s5-window-leftovers.md` (new)
non-goals: the scheduler (`driver_chains.py`), the controller, the guard's code, S6, `s5_release`/`s5_release_of_dispatch` bodies.
handoff: report with the witness, the FR pass, the AR lines of §1, the twin lines (AR-19), and the TR3-9 C diff-stat line.
edges: §2 items 10.1, 10.2, 10.4 (absent state file, window with no dispatch rows, N == 1 vs N != 1).
DoD: `python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_s5_window_leftovers.py`, `python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_guard_window_files.py`, `python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_driver_chain.py`, `python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_story_run_words.py`, `python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_driver_layers.py` (each under a minute; the last two by builder-rules 7c). CI only, named: `test_story_run_s5_parallel.py`, `test_story_run_s5_n1_frozen.py` (must stay equal).
Overlap with TR3-9 C: no function; files `driver-layers.json` (C1 adds rows) - the later merge resolves rows.

### Part A2 — TR4-10 scheduler and pin (items 10.3, 10.5)
given: this spec; `factory-rules.md`; `builder-rules.md`; `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\driver_chains.py`
owns:
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\driver_chains.py` (`DriverChains.session_gate`, `DriverChains.count_launch`, `DriverChains.run_chains` (the one clear line beside `_drain.clear()`))
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_driver_chain.py` (three keys)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\design\state-exits.md` (one row after row 23)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_s5_parallel_admission.py` (one key)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\tr4-10-drain-gate.md` (new)
non-goals: `story_run.py` (nothing), the controller's code, S6 code.
handoff: report with the witness, the residual grep of 10.3, the re-entry road line of 10.3.
edges: §2 items 10.3 (a drain started while a chain waits; the counting chain; ungated chains; N == 1) and 10.5.
DoD: `python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_driver_chain.py`, `python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_s5_parallel_admission.py`, `python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_state_exits.py`, `python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_driver_layers.py`. CI only, named: `test_story_run_s5_parallel.py`.
Overlap with TR3-9 C: no `story_run.py` function. Files: `state-exits.md` (C1 adds one S6 row near row 26; A2's row goes after row 23 - adjacent-line conflict possible, the later merge resolves); `driver_chains.py` is not in C1's owns, but C1's lanes call `session_gate` through `session_running` (behaviour inherited, t-2147 C.7).

### Part B1 — TR4-11 stop record and appender (items 11.1, 11.2); producer and reader in ONE commit (AR-22)
given: this spec; `factory-rules.md`; `builder-rules.md`; `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\collect_stall.py`; `D:/ws1/wt-fbfix\docs\SIBLING_MAP.md` (axis 29)
owns:
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\story_run.py` (functions: `run`, `_append_jsonl`, new `person_stop_record`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\collect_stall.py` (`_k3_k4`, the module docstring K3 line)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_driver_stop_record.py` (new)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_collect_stall.py` (six keys)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\driver-layers.json` (the row of `Driver.person_stop_record`)
`D:/ws1/wt-fbfix\docs\SIBLING_MAP.md` (axis 29: `story_run._append_jsonl` joins the adopters)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\tr4-11-stop-record.md` (new)
non-goals: `driver_chains.py`, `run_claude`, K1/K2/K4-K7, the loop half of collect_stall, other modules' appenders (axis 29's queued siblings).
handoff: report with the witness, the `driver-runs.jsonl` reader list (AR-22), the twin line.
edges: §3 item 11.1 (Ctrl-C with no story state dir, before `run`, a failed write, a second Ctrl-C, both roads) and 11.2.
DoD: `python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_driver_stop_record.py`, `python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_collect_stall.py`, `python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_hooklib_append_jsonl.py`, `python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_story_run_words.py`, `python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_driver_layers.py`. CI only, named: every `test_story_run_*` that reads `driver-runs.jsonl` (the builder names them from the reader grep).
Overlap with TR3-9 C: no function; file `driver-layers.json` as in A1.

### Part B2 — TR4-11 census blind spot and text (items 11.3, 11.4)
given: this spec; `factory-rules.md`; `builder-rules.md`
owns:
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_judgment_census.py` (`BLIND_SPOT`, the docstring paragraph, one key)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (`about` only)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\s5_precheck.py` (the comment at :4265 only)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\tr3-14-hook-readers.md` (the one sentence)
non-goals: `refusal_registry.py`; any census row, class or count.
handoff: report with the witness and the `about` diff.
edges: none of the brief's list applies (text only); the census totals must not move.
DoD: `python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_judgment_census.py`, `python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_s5_precheck.py`.
Overlap with TR3-9 C: file `judgment-census.json` (C1 may add a row; B2 edits line 3 `about`) - non-adjacent unless the file is one line per key; the later merge resolves.

### Dependency line
A1, A2, B1, B2 own disjoint functions and files apart from the row files named above; all four may run beside TR3-9 C under D-0048.
Merge order by shared files: A1 -> B1 (`driver-layers.json`, `story_run.py` disjoint functions: the later merges `main` and keeps both
pins green); A2 after TR3-9 C1 (`state-exits.md`) or with the row conflict resolved by the later; B2 any time (after C1 if C1 adds a
census row). One critic pass for the topic "S5 windows" over A1+A2+B1 merged (R13-g; A1 touches the S5 close predicate).

## 5. Small choices closed by the designer (no design weight)

- Test homes: a new fast `test_s5_window_leftovers.py` for 10.1/10.2/10.4 (the CI file `test_story_run_s5_parallel.py` named in the
  batch row is slow and would not be a builder witness); a new fast `test_driver_stop_record.py` for 11.1/11.2.
- 10.4 reads `config_contract.parallel_windows` directly, not `s5_parallel_cap()` (no note printed from a brief builder; same reader).
- 11.1 adds no console line and keeps the exit as today (re-raise).
- 10.3's residual `launched` row with no end row is accepted (K3's safe side) rather than moving the gate before the row in `run_claude`.
- `test_story_run_words.py` (14.8 s) is a witness despite its `test_story_run_` prefix: builder-rules 7c names it as a point file.

## 6. Forks (returned; each with a recommendation)

- **F1 — Q1 scope.** The per-window release on the critic's closing finish has landed (`finish` :3219, `test_driver_chain.py`
  `closing_finish_releases_the_window`). (a) Close Q1 as done and add only the guard-side key. (b) Also add the stage-completed sweep
  of item 10.1 for an S5 completed by another role's finish (the author's mechanical round on a recovery road). **Recommended: (b)** - it
  is the Lead's "whichever road closed it"; cost one function and four keys.
- **F2 — where the stop record lives.** (a) A row of `driver-runs.jsonl` through `journal_run`: append-only history, K3 already reads
  this file, one writer. (b) A key of `driver-state.json`: a snapshot the next run overwrites; K1's home. **Recommended: (a).**
- **F3 — which `launched` rows a stop record tells apart.** (a) Those launched at or after `since` (the stopping process's start) and
  before the record. (b) An explicit `cut` list of the calls this process left without an end row (precise even with two processes on
  one story; touches `run_claude`). (c) Every earlier row (clears a dead earlier driver: unsafe). **Recommended: (a)**, residual named.
- **F4 — Q3 against "the one that counted still runs".** The Lead's "once the drain is on it does not launch" meets `count_launch`'s
  contract when the waiting chain is the one whose registration hit `--max-boundaries`. (a) Exempt that chain. (b) No exemption (the
  counting chain may end `Drained`; `--max-boundaries` then pauses one session earlier). **Recommended: (a).**
- **F5 — "last dispatch" in Q2.** (a) The last record in the controller mapping's order (insertion = `apply` order; the builder
  confirms by reading `Controller.apply` and returns a fork if not). (b) Any non-discounted returned record meeting the scope (simpler;
  errs to open, can hold S5 open for good if a returned record is never settled). **Recommended: (a).**

## 7. Contradictions and analogs noticed (not widened)

- The batch rows name `story_run.py (session_gate)` and `(_interrupt_chains)`: both moved to `driver_chains.py` (TR3-9a). The batch
  file is frozen once taken; the Lead corrects the row or lets this spec stand as the node's text.
- TR4-11's dependency "TR4-10 (shared story_run.py)" is not needed under D-0048 with the function lists above.
- `story_run._read_jsonl` splits on U+2028 (11.2 analog). Axis 29's queued siblings (`question_register`, `event_store`, `manual_capture`,
  `telemetry_capture`, `log_append`, `judge`) stay queued.

## 8. Reading trail

Read: `plans/piles/thinking-roles/batch-4-ostatki.md` (rows TR4-10, TR4-11, header); `docs/tasks/handoffs/20261110-lead-window-acceptance.md`
§2-§6; `docs/tasks/specs/reviews/t-2121-critic-tr3-6.md` (whole); `docs/tasks/specs/reviews/t-2095-rereview-identity.md` (N1, N2);
`docs/tasks/specs/t-2147-tr3-9-walker-lanes.md` §C0-C2 (:283-379) and the grep of its owns; `story_run.py` :540-610, :1095-1114,
:1555-1575, :1890-2123, :3131-3228, :11400-12100, :17066-17230, :17862-17885, :19554-19608, plus greps (`def s5_`, `KeyboardInterrupt`,
`open(..."a")`, `except Exception`, `count_launch`, `interrupted`); `driver_chains.py` (whole); `collect_stall.py` (whole);
`s5_precheck.py` :4244-4268; `window_files.py` (defs); `guard_pre_tool.py` :1557-1602; `hooklib.py` :469-498; `controller.py` :94-108,
:157-177; `dispatch_identity.py` :36-49; `design/state-exits.md` :1-60; `design/architecture.md` :140-280; `docs/SIBLING_MAP.md` axis 29;
`plans/builder-rules.md` 7, 7b, 7c; `scripts/slow_tests.json` (rows); `test_judgment_census.py` :25-39, :436-500; `judgment-census.json`
`about`; `test_driver_chain.py` :840-969; `test_guard_window_files.py` :1-80; `changelog.d/tr3-14-hook-readers.md`; worktree greps of
`wt-tr3-9c0`, `wt-tr3-9c1`, `wt-tr3-9c2`.
Needed beyond the manifest: `driver_chains.py`, `t-2121-critic-tr3-6.md`, `t-2095-rereview-identity.md`, `t-2147-tr3-9-walker-lanes.md`,
`window_files.py`, `guard_pre_tool.py`, `hooklib.py`, `controller.py`, `dispatch_identity.py`, `test_driver_chain.py`,
`test_guard_window_files.py`, `test_judgment_census.py`, `judgment-census.json`, `slow_tests.json`, `changelog.d/tr3-14-hook-readers.md`.
Not done: `git diff --stat` of the TR3-9 C worktrees (no shell tool in this role); replaced by the owns + grep above.

## 9. Lead decisions after plan critic t-2227 (10.11.2026) - part A1 is written to THESE; where §2 or §4 disagree, this section rules

The review is `docs/tasks/specs/reviews/t-2227-tr4-10-11-plan-critic.md` (B-1, B-2, F-5, F-6, F-7). Decided by the Lead, no owner question.

**D1 (B-1 a) - the old body reads the same close rule at N != 1.** `stage_S5`, the old body's `last = len(todo) == 1` (~:11799): when
`self.s5_parallel_cap() != 1` it becomes `last = (len(todo) == 1) and not self.s5_open_windows(excluding=<the cases of this window>)`,
with `WindowsUnreadable` read as open (`last = False`). At N == 1 the line is byte-equal in behaviour to today (no read).
INVARIANT: at N != 1 no body closes S5 while `s5_open_windows` names another window open; at N == 1 nothing is read and nothing moves.

**D2 (B-1 b) - N == 1 is a NAMED RESIDUAL, not closed.** The sentence of item 10.2 "N == 1: the serial `completion_for` reads the same
function" is wrong and is withdrawn: at N == 1 `completion_for` takes its own loop (~:17015-17020) and the old body never calls
`s5_open_windows`. The frozen N=1 road stays as it is (a promise of the old road; not a regression). The builder writes one line in the
`s5_open_windows` docstring: "at N == 1 the serial road does not read this function; a returned last round there is settled by the
controller's own return road".

**D3 (B-1 c) - the way out of a window held open by a returned last round.** Chosen: the driver settles the return itself, on the road
that already exists. In `stage_S5`, BEFORE the refusal "every window is accepted ... run `controller.py --operation recover`"
(~:11756-11759) is raised and only when `todo == []` at N != 1: find the windows whose last non-discounted S5 dispatch (item 10.2's
rule, one helper, not a second copy of the walk) has status `controller.RETURNED`; for the first such dispatch in record order take the
existing resolve-return move (`_act_resolve_return` -> `resume_role`, ~:16815-16836) for THAT dispatch id, then re-enter the stage loop.
No new question text, no new road. POSITIONAL INVARIANT: the refusal stays reachable when no window has a returned last round (the
state it was written for), and it is never raised while a returned last round exists that the driver can settle. Error direction: the
driver may resume a role once more than strictly needed (a paid resume); it must never close S5 over the returned round and never loop:
the same dispatch id is resolved at most once per `stage_S5` entry (a second meeting of the same id in one entry raises the old
refusal with the dispatch id named in it). If `_act_resolve_return` cannot be called from `stage_S5` without a person question that
does not exist today, the builder STOPS and returns that as a question with the lines read - it does not invent a road.
`design/state-exits.md` gets one row: state "S5 window held open by a returned last round (N != 1)", exit "the driver resolves the
return (`resolve_return`), then the window's critic", owner code.

**D4 (B-2) - item 10.1's status set and premise.** The release-on-complete sweep frees S5 claims only when `stages.S5.status ==
"completed"` AND no S5 dispatch has a status in `{"running"} | controller.STOPPED | {controller.RETURNED}` - read from the controller's
names, never a literal list (AR-13). The premise is corrected: the gap is a recovery process that finishes window B's saved critic
`--not-complete` and then the last window A's critic `--complete` in the same process (B's claims stay), plus the live mechanical
round. Test keys: `stage_completed_by_author_finish_frees_every_s5_claim` is REPLACED by `recovery_finishes_free_sibling_claims` (two
saved critic results, one process) and `live_mechanical_round_close_frees_every_s5_claim`; ADD `completed_beside_incomplete_frees_nothing`,
`completed_beside_returned_frees_nothing`, and the batch row's literal test `closed_by_debt_then_rework_automator_not_refused`.
`window_files.release_stage` reuses `release`'s loop through one predicate parameter - not a second copy of the walk and the
empty-claim rule (AR-15).

**D5 (F-6) - position of the sweep.** `s5_release_completed()` is called only after `story_step finish` exited 0, in the post-finish
block next to the existing `s5_release_of_dispatch` call (~:3214-3219) - never in the pre-finish `if complete is True` block.
INVARIANT: the stage status it reads is the one this finish wrote.

**D6 (F-7) - the ownership line on the old body.** `chain=True`: the text stays byte for byte. `chain=False` at N != 1: the variant
"A test file another window of this story wrote first refuses your Write or Edit: put your test in a new file in the same directory;"
followed by the SAME door sentence the chain text ends with (shared as one constant, not retyped). The first sentence of the chain
text ("Other windows ... at the same time") is false on the serial body and is not given there.

**D7 (F-5) - anchors.** `s5_release_completed` goes right after `s5_release_of_dispatch`.

**Test keys added to `test_s5_window_leftovers.py` by D1-D3:** `two_windows_old_body_does_not_close_over_returned_round` (the critic's
scenario: W1 critic accepted route mechanical, W1 mechanical round returned, `todo == [W2]`, W2's critic finish is NOT `last`),
`n1_old_body_reads_nothing`, `returned_last_round_is_resolved_not_refused` (todo empty: the resolve-return move is taken for W1's
dispatch id), `no_returned_round_keeps_the_old_refusal`, `same_returned_id_twice_raises_named`, `returned_then_released_by_person_is_open`
(critic §5: DISCOUNTED drops the later record, the returned one is last).

**Part A1 owns, replacing §4's list for `story_run.py`:** functions `s5_open_windows`, `s5_auto_extra`, `finish` (one call line in the
post-finish block), `stage_S5` (the `last` line and the block right before the "every window is accepted" refusal ONLY), new
`s5_release_completed`, one new private helper for "last non-discounted S5 dispatch of a window". Plus `design/state-exits.md` (one row).

**D3 AMENDED (Lead, 10.11.2026 21:50, after the builder's stop; this paragraph replaces D3 above).** `_act_resolve_return` resumes a role
only with the person's words (`pending_words`); the driver never writes them. So the way out is the EXISTING `resolve_return` question:
in `stage_S5`, at N != 1 and `todo == []`, before the "every window is accepted" refusal, a window whose last non-discounted S5 dispatch
is `controller.RETURNED` raises the existing `resolve_return` Refusal for that dispatch (one packet builder shared with
`_act_resolve_return`, text not retyped); the conductor settles it or asks, and the person's words resume the role on today's road.
INVARIANT: the old refusal stays reachable when no returned last round exists and is never raised while one does. `state-exits.md` row:
exit "the `resolve_return` question of that dispatch", owner conductor/person. Test keys: `returned_last_round_raises_resolve_return_naming_the_dispatch`
(replaces `returned_last_round_is_resolved_not_refused`); `same_returned_id_twice_raises_named` dropped (no loop once it is a Refusal).
**D1 widened:** every expression of the old body that yields `last` (the `owed` branch too) reads `s5_open_windows` at N != 1; key
`owed_branch_does_not_close_over_open_window`. A1 also owns the `CHAIN_ONLY_LINES` list of `test_story_run_s5_parallel.py` (the D6
variant line, only if an N=3 story can pass a window through the old body) and one line of `plans/features.json`.
