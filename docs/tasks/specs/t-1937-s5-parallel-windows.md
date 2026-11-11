# t-1937 — S5 by multiples: parallel windows (P1) and hop overhead (P2) — DRAFT SPEC, REVISION by t-2034

Status: REVISED DRAFT. **Revision by t-2034 (critic's plan review of this spec), drafted by designer under t-2052**, for Lead acceptance. A continuation of the same spec, not a new one. Forks left open are in section 4, each with a recommendation; every node is executable by the recommendation (PROJECT.md, team rule 11).
Owner's word 05.11.2026 11:30: both runs take many hours and must take about one hour; "время надо уменьшить в разы".
Owner's word 06.11.2026, verbatim: «По умолчанию запускаем в параллели и только если это не возможно, то последовательно».
Coordinator's decisions for this revision, on the critic's recommendation: `dispatch.parallel_windows` defaults to 3 and a bad value reads 3 with a note (already on branch `tr/tr3-3`, `config_contract.parallel_windows`); F3 is (b), first-write ownership with the door "a new file in the same directory"; a table "impossible, so serial" with a carrier is required (3.6); parity at N=1 is a test of an explicit project choice, and an equivalence suite pins what ships, at N=3.

Tree read for this revision: `PKG` = `D:/ws1/wt-fbfix\ai-packages\qa-factory`. `S` = `PKG\scripts`. A function name is the address; a line number is the tree's at reading and may have moved. The Lead's dispatch rewrites `PKG` for a node that has its own worktree.

## 0. Measured base and two corrections to the brief (unchanged)

Base (`experiments/mybooks/thinking-roles/time-analysis.md`, arm B): S5 window 4:13:19 of 7:23:30; S5 role duration 2:49:52; 7 windows run one after another; first passes 3:08:22, repair rounds 0:41:55; automator->critic hops 13 x 138 s (0:29:56), critic->automator hops 8 x 56 s (0:07:29).

C1. `S5-qa-code-critic-10` did NOT hang: its transcript has activity from 05:41:44 to 06:08:57; the 27 min were its own live probes; `duration_ms` of the result row covers only the last re-entry. The measurement defect is ours (P2-4).

C2. The hop's 138 s cannot be split by step from the logs. The only timed step is the settle (10 lines, 60.5-74.9 s, sum 11:10). The last settle spent 63.8 s on 11 `manifest_from_tests.py --dry-run` subprocesses, all refused, for rows of OTHER windows, zero probes. Hence P2-1 instruments and P2-2 fixes the measured sink.

Corrections since the first draft: the driver road has no `work/s5-plan.json` (t-2034 B2), so "planned test files" is no scheduler input; overlap is the automator's own choice at work time (arm B 7 windows, 4 overlapping pairs: W1/W2 `tests/api/cart/cart.spec.ts`, W3/W7 `add_to_cart`, W4/W6 `wishlist_move`, W5/W6 `cart_page`; arm A 6 windows, 0 overlaps; carrier: the critic's `overlap.py` over `controller.json` + `automation-manifest.json`, t-2034). t-1936 and walker slice 1 are merged (t-2034 q.1). N-P2-2 is done on `tr/tr3-11` (t-2043).

## 1. Scope, AR-n touched, owners and census classes (designer rule 1, host adaptations 9-10)

Touches `ai-packages/qa-factory/`. Each AR's change check goes into the DoD of the node named.

| AR | how touched | change check in the DoD | node |
|---|---|---|---|
| AR-2 open variety | whether a project's build tolerates a half-written test file is not something code can infer (P2) | name what the role still decides: where a test lives (P17); run the changed scheduler on the fixture with no overlap and the one with overlap: it reports, not halts | TR3-6, F11 |
| AR-3 config default | `dispatch.parallel_windows` | one commit: template, keys row, read with default, the interview topic. The interview topic is MISSING on `tr/tr3-3`: grep of the package there finds changelog, template, keys, `config_contract`, its test only | TR3-12 |
| AR-8 paths handed | per-dispatch findings, debt, advice, notes, judge paths | each path joins `known_paths` or the brief in the same commit, spelled as the code writes it (FR-37) | TR3-5, TR3-15 |
| AR-9 refusals | guard refusal on another window's file; `stage_complete` refused beside a running window; `--open-windows` refused on a bad name | one commit: A24 row, door, person's-word route; regenerate `controller-blocks.md`; both detectors | TR3-16, TR3-4 |
| AR-10 requirement before the work | the automator is told about file ownership before it writes | the check names where the role reads it (brief line and `agents/qa-automator.md`) in the same commit | TR3-16 |
| AR-12 friction | hop time; the new guard refusal | per-hop timing before/after (P2-1); `code_friction` of the automator before/after or "not measured" as an open item | TR3-2, TR3-16 |
| AR-13 one reader | "which dispatch am I" gets one reader across every site of table 3.1; `critic-findings`, `probe-debt`, `advice-S5`, `s5-notes`, `judge-code` paths | grep for the shape with a positive control; each site reads through the one reader or has a reason in 3.1 | TR3-13, TR3-14, TR3-5, TR3-15 |
| AR-14 one writer | table 3.3; `state/window-files/` | each new artifact: `stages.json` output + `artifact-writers.json` row in one commit; `test_artifact_writers.py` | TR3-5, TR3-15, TR3-16 |
| AR-15 one survivor | no second question queue (M3); `dispatch_identity` is a new survivor | the new survivor gets a SIBLING_MAP axis in the same commit; a site that cannot call it is named there | TR3-13, TR3-6 |
| AR-16 / FR-6 / FR-10 | a question while windows run | one question at a time through `Person`/`ask`/`take_answer`; no new question text | TR3-6 |
| AR-17 one seam | a refusal in one window | one seam per driver turn, on the main thread, after the drain; `Driver.no_move` stays the only seam | TR3-6 |
| AR-19 stage twins | the walker slice 2 reuses the scheduler seam | grep axis 5; name the twin (t-1957 N5p) in report and commit | TR3-6 |
| AR-20 ratchets | possible raise of `NO_MOVE_BASELINE`, census | every raise named row by row: key, old -> new, reason | every node |
| AR-22 producer/reader | `parallel_window`, `open_windows`, `wall_ms`, timings | each new field names its reader in the commit; `test_field_producers.py` | TR3-2, TR3-4 |
| AR-25 way out | state `window-files` claims, chain ended by a drain | each named with its exit in `state-exits.md` | TR3-16, TR3-6 |
| AR-28 unknown never a pass | the close predicate; identity unknown | each new gate read states missing/unreadable/empty and a test pins it (edges below) | TR3-6, TR3-13 |
| AR-29 judgment | checks below | each named with owner + class | all |

Checks added or altered: owner served and census class (AR-29).

| check | where | owner | class |
|---|---|---|---|
| admission: S5 window dispatches beside running ones only with the scheduler's flag, disjoint scopes, count within the cap | `controller.py` `_window_beside_running` | data (code) | xref |
| resume beside running windows, same clause | `controller._resume_problems` | data (code) | xref |
| `stage_complete: true` refused while another S5 dispatch runs | `controller.py` accept validate | data (code) | xref |
| `open_windows` names real windows of the story | `controller.py` accept validate | data (code) | xref |
| guard: a write to a test file another live window claimed is refused, with a door | `guard_pre_tool.window_file_check` | data (code) | safety |
| launch gate: a session does not start while another window's running session holds a file of this window | `story_run` scheduler | data (code) | xref |
| close predicate `s5_open_windows` | `story_run` | data (code) | xref |
| serial decision `s5_serial_reason` | `story_run` | data (code), tells, never stops | shape |
| settle leaves items of a running window | `probe_debt.settle` | data (code) | xref |
| settle: skip a rebind already refused on the same bytes (done, TR3-11) | `probe_debt.settle` | data (code) | shape |
| liveness line on a silent transcript | `story_run.launch` | data (code), tells, never stops | shape |

None of these judges a role's content. P17 stays the role's: where a test lives, extend or new. The guard refuses one write path and leaves every other. The critic's judgment of "extend versus new" stays the critic's, with the claim as a fact it is told (TR3-16).

FR walk: A (FR-1, FR-2, FR-4, FR-57: guard door is a move the automator has: a new file), B (FR-6, FR-7, FR-10: one question at a time, no new text), C (FR-14 `driver-runs.jsonl` gains `wall_ms`; FR-15 per-window paths given; FR-38/FR-39: the critic is told its path, the automator the ownership rule, before the work), D (FR-59: an unreadable window is open), E (FR-23), F (FR-24, FR-26, FR-28, FR-41), G (FR-31: barriers, no sleeps as sync; FR-43; FR-45: claims are a durable record of their own, not a write into a request; FR-55; FR-32).

Non-goals: no code in this task; no change to S1-S4, S6-S9 flow; no gateway/host settings (P25); no change of window sizes; no change of what the critic judges; no fix of "rows bind no bytes"; F1, F2, F5-F8 are not reopened; the walker's slice beyond the scheduler seam it uses.

## 2. P2 — hop overhead

### P2-1 timing carrier (TR3-2; a worktree `wt-tr3-2` holds `driver_timing.py`; status with the Lead)
- `Driver.timed(step, dispatch)` around `start`, `bind`, `handoff`, `finish` (incl. `window_record.py`), `stage_scope`, `stand_check`, `build_check`. `story_step.start` reports its sub-steps as `timing: <step> <seconds>` lines.
- Carrier `state/driver-timings.jsonl` `{ts, stage, dispatch, step, seconds}`; console `note: <step> took N s` only over 20 s.
- `driver_timing.py --task T [--json]`; `--check-hop-s 20` exits 1 listing hops (advice, never a gate).
- Tests `test_driver_timing.py`: `hop_split_sums_to_wall`, `unattributed_remainder_is_named`, `empty_file_says_no_timings`, `unreadable_line_is_counted_not_dropped`, `check_hop_s_at_and_beyond`.
- Edges: file absent: "no timings recorded", exit 0: an absent carrier never reads as "0 s overhead". A step that raises still writes its line with `error: <type>`: a failed step's time is not lost.
- **Added by t-2034.** `timing:` lines must not enter the launch card (`story_step` prints what it writes; I2 comment there), and must not reach the skill road's reader, where "the driver parses them" is false: they are printed only when `current_run_mode() == "driver"`. Test `timing_lines_not_in_card`, `timing_lines_absent_on_skill_road`.

### P2-2 settle: incremental (TR3-11, DONE on `tr/tr3-11`, t-2043)
Landed: refused-rebind memory, `stamps`, `unchanged_since`, `STABLE_LEFT`. Two consequences for this spec, both carried to TR3-15:
1. The memory lives in the debt file (`_memory_doc`), and t-2034 item 6 requires it stay one story-wide file once the debt goes per dispatch.
2. TR3-11 reused the word `same_bytes` for a kept rebind (`probe_debt.py` :842 next to the probe's :801); t-2034 item 6 asks for its own word. TR3-15 renames it.
Noticed, not decided: the stamp's `author` is the latest accepted automator of ANY window, so at N=3 each author's accept voids every item's memory. Direction is safe (retry), the cost is unmeasured. N-LIVE reads settle time from P2-1; a follow-up is a node after that, not a guess now.

### P2-3 off the critical path (after one measured run)
Every step over 5 s per hop is listed with a decision: cache, move after launch, or keep with a reason. Target median hop < 20 s, max < 45 s, by `driver_timing.py --check-hop-s 20`.

### P2-4 the silent wait (TR3-2)
`run_claude` row gains `wall_ms`; `wall_ms - duration_ms > 120000` prints one note. `launch`: a watchdog asks `dispatch_liveness` every 60 s; silence over `dispatch.abandoned_after_s` prints ONE line per episode. It never kills (F8). Invariant: a working role is never stopped by the driver. **Added by t-2034 (M2):** the watchdog writes through `sys.__stdout__`, flushed, because `defer_question` holds `redirect_stdout` and a line printed through `print` there is lost. Tests in `test_story_run_wait.py` (CI): `wall_ms_journalled`, `wall_vs_duration_note_over_120s`, `silence_line_once_per_episode`, `no_line_when_transcript_grows`, `silence_line_survives_redirected_stdout`.

## 3. P1 — parallel S5 windows

### 3.1 Every "one running dispatch" site: verdict and node

Sources: critic's B1 table, scout report (`docs/tasks/specs/reports/t-1937-scout-s5-shared-writers.md`, S-n), this designer's own grep over `S\*.py` (82 hits in 32 files by status pattern, 7 of them tests; control: it found `controller.py:4965`) and reads at the hit. Where critic and scout differ, the row says.

| site (function) | wrong output at 2+ | verdict | node |
|---|---|---|---|
| `controller` op `dispatch` :4965 (S-1) | refuses | CHANGE: `_window_beside_running` | TR3-4 |
| `controller` apply `dispatch` :1529, `accept/checkpoint` :1567, `resume` :1591 (S-2) | a non-final accept writes `S5 = pending` while others run; "stage running" readers misread | CHANGE: not lowered while another S5 dispatch is running | TR3-4 |
| `controller._resume_problems` :5752 (S-3) | a stopped window refused beside a running one | CHANGE: same clause | TR3-4 |
| `controller._closes_stage` :6786, accept validate :5330 (B3) | a bare `--not-complete` refused on the last-finishing critic while another chain is open | CHANGE: `open_windows` field | TR3-4 |
| `controller._s5_completion_problems` (scout 1c) | `stage_complete` beside a running window not refused | CHANGE: backstop refusal | TR3-4 |
| `s5_precheck.running_dispatch`, `window_dispatch`, `detector_main` (S-9) | unscoped: every case in the manifest (TP1-15045) | CHANGE: identity; two running and no identity: `UNREADABLE`, never unscoped | TR3-13 |
| `branch_accounting._s5_window`, `s5_scope`, `s5_check` (S-10) | `Unreadable`, false cause text | CHANGE: through the above; the cause text says what it knows | TR3-13 |
| `exit_gate._live_dispatch`, `dispatch_scope`, `_write_digest`, `text_end_after_handback`, `digest_errors` (S-8) | scope silently lost, digest unfiled | CHANGE: identity | TR3-13 |
| `exit_gate.write_advice` | one file, last writer wins | CHANGE: per dispatch | TR3-15 |
| `stage_guard.rule_typed_runner`, `_judge_slice` (S-7) | window 2's `--request` refused, scope judged against `active[0]` | CHANGE | TR3-14 |
| `guard_pre_tool.dispatched_role` (S-12) | wrong role, wrong doors | CHANGE: identity | TR3-14 |
| `guard_pre_tool._dispatch_open_for_owner`, callers `owner_check`, `_any_story_open_for_owner` (S-13) | guard opens for a non-owner | CHANGE: identity | TR3-14 |
| `subagent_journal` :167 `record_return` wait 0, `except: pass` (S-15); `environment_preparation` :230 | a busy lock silently loses the `returned` event | CHANGE: bounded wait | TR3-14 |
| `story_run` :3235, :16075 fallback to pipeline stage `agent_id` (scout) | resumes another window's agent | CHANGE: on the chain road per-dispatch `sessions` only | TR3-17 |
| `inject_context.dispatch` :578-586 (S-6) | refuses a second launch of a role. **Scout says MUST, critic says Agent-tool road only.** Hook matcher `Agent\|Task\|SendMessage` (`hooks.json`) and the driver launches `claude -p`, so the driver road never meets it | NO CHANGE, because the admission flag keeps two running dispatches off every road that has this hook. Pinned by `skill_road_second_start_keeps_old_refusal` | TR3-4 |
| `host_dispatch.record` :310-317 (S-14) | Codex host: receipt names no dispatch | NO CHANGE: a non-Claude host is a serial row of 3.6 | TR3-6 |
| `controller._next_action_for_state` :8029 `active[0]` (S-5: "MUST low"; critic: safe, serial resume) | names the first only | NO CHANGE: restart resumes one by one, safe; on restart the serial reason applies (3.6) | - |
| `execution_request.find_active_dispatch` (S-16) | refusal names `--dispatch` | SAFE under "no two running dispatches share a case"; pinned by `find_active_narrows_by_disjoint_case` | TR3-4 |
| `story_progress` :522 (one primary), `factory_dashboard` :1427 | display | N-P1-4 shows the windows in `progress_line`; `story_progress` keeps its primary, a display | TR3-6 |
| `stage_guard.stage_of_dispatch` :166 | role on one stage returns before counting (S5 roles are one-stage, `stages.json`) | SAFE | - |
| `controller` `checkpoint` no id :7230, `release` :7335 (S-4) | refusal names ids | SAFE: every chain caller passes the id | - |
| `revise_plan` :4872, `semantic_reopen` :4915, `invalidate` :5473, `recover` :7619, `next` :7735 | refuse beside a running dispatch | SAFE: wanted direction | - |
| `stage_guard._closed_author_door`, `_resume_doors`, `:2797` | list or stale check | SAFE | - |
| `agent_autobind`, `conductor_stop._running`, `stage_done` :1087/:1191, `probe_debt.open_critic_dispatch`, `session_handoff.can_takeover`, `window_budget` :312-318, `collect_stall` | by id, or a list | SAFE (`window_budget` read by this designer; `collect_stall` by the scout) | - |
| `manual_evidence._running_dispatch`, `validate_artifacts._s6_runner_half`, `story_run` :12252 | S6 only; S6 never runs beside S5 | SAFE here; **twin for TR3-9** | TR3-9 |
| `run_suite.active_story_stage`, `branch_accounting._running`, `guard_pre_tool:1458`, `planning_contract:341`, `exit_gate:713/1387`, `story_run:1277/5697/16605` | read a stage `running` | SAFE once S-2 is fixed. Row 2 above is the fix | TR3-4 |
| `story_run` `no_move_facts["running"]` :5493, `owed_rework` :7506, `code_close` :16599 | "something is running" is always true beside a sibling | SAFE only off a chain: no chain calls them (seam after the drain) | TR3-6 |

Not classified, left to TR3-4's reader: `controller._closed_dispatch_refusal`, `_before_windows`, `_grown_close_problems` bodies (scout 1c read their heads). The builder reads them and adds a row in its report.

### 3.2 Design

"Parallel sessions, serial bookkeeping." One driver process. Each window is a CHAIN (automator -> critic -> rounds) in its own thread. One driver lock `self._book` is held by a chain EXCEPT while its role's `claude` runs, and except around one critic `start` (below). Every other code step runs one at a time; role sessions overlap.

- **Config.** `config_contract.parallel_windows(config)` is the one reader, on both sides (AR-13); `_dispatch_setting` is not used for this key (it reads 0 as valid and has no default row). Absent key reads 3. A value that is not an int >= 1 reads 3 with one `note:` line, never a stop. **Coordinator's decision against the critic's recommendation (invalid -> serial):** a project that writes `0` to turn windows off gets 3, told by the note, whose text names the fix; the supported "off" is 1. Invariant: a bad value never stops a run and is never silent. N=1 takes the old road literally: no thread, no scheduler, no new state key, no console prefix, no `--parallel-window` flag.
- **Scheduler** (`Driver.run_chains`, the seam TR3-9 reuses; 3.7). Entered from `stage_S5` when `parallel_windows != 1`. The cap = config, or 1 when `s5_serial_reason()` names a reason (3.6): the new road with cap 1, so predicates stay one. A window is launchable when running chains < cap, no drain is on, and the launch gate holds (below). Order is today's `todo` order; a skipped window waits, others pass it. `windows` is re-read under the lock before each launch (a held list goes stale across a release).
- **Owed and pending first.** `repair_owed`, `repair_debt_pending` run through today's one-window code before any chain starts: drain, then serial first. Invariant: a round the person chose runs before any review of a sibling; t-729/t-733 position invariants hold unchanged.
- **Launch gate.** A session of window X does not start while a RUNNING session of another window holds a file of X. X's file set = its claims (`window_files`) union the `tests[].file` of the manifest rows of X's cases. Invariant: a critic's probe never mutates a file another window's session is writing, including a test that sits in a file claimed by a sibling (the guard does not see probes). Overlap blocks concurrency, never progress: when nothing else runs, the lowest ordinal launches (the waiting sibling has no running session, so the file is quiet).
- **Stage close.** `Driver.s5_open_windows(excluding=cases)`, read fresh under the lock: open = no accepted critic, OR any running or returned dispatch meeting its scope, OR an owed round for it, OR a live chain in the registry, OR any of these unreadable (FR-59). Callers: the `closes` of `s5_review`, `s5_mechanical_round` (`complete` becomes a callable), `completion_for` S5 branch. Invariants: S5 is completed only by the finish that leaves zero open windows, which may be a mechanical author's as today; exactly one finish closes it, whatever the finish order (the lock makes the last finisher see zero); `round_in_w1_blocks_close_by_w2`. A finish that is not closing and has others open passes `--open-windows <cases>`, so the controller does not refuse it as "no role to close it".
- **Chain record.** `{window, boundary, last_dispatch, exception, proc, ordinal}` in a registry. `boundary` and `last_dispatch` become thread-local properties; a chain initialises `boundary` at its start (a fresh thread has none otherwise). The main thread keeps its own values.
- **Seam after the drain (B4).** A chain catches everything. On any exception the drain starts: no new launch, running sessions finish and book; a chain reaching `run_role` or `rework` entry raises internal `Drained` (POSITION: before `start` and before `controller rework`; invariant: a drain registers no new dispatch). After all chains join, on the main thread: `InfraStop` first (F13), else the lowest ordinal's `Refusal`, else the lowest ordinal's `Person`. Main adopts that chain's record (`adopt_chain`: its `boundary`, `last_dispatch`) and re-raises to `guarded`, the road every refusal takes today. Others are NOT handled in this turn: they re-arise on re-entry, because their dispatch is still running with a saved result. Invariants: one seam per turn; `Refusal.retry` and `handle_refusal` read the failing chain's values; one-slot `standing`, `_in_no_move`, `in_code_step`, `_price_notes`, `_answer`, `gate_refusal` never see two chains (M2, M4); `drop_standing` runs only in `guarded`, which a chain never calls.
- **Questions: no new queue (M3).** The re-entry road already re-raises a running dispatch's question from its saved result (`_act_wait_existing_job`, repair gate, threshold), and a Person raised before a dispatch re-arises because the state is unchanged. So `pending_questions` is NOT added. `state["deferred"]` keeps its meaning. Invariant: a question not shown this turn is shown on a later entry, never dropped, never answered by another window's answer (`repair_key` + dispatch, as today); pinned by `queued_question_asked_next`.
- **`closes` and retry.** `closes` passes its dispatch to `route_of` and `repair_answer` explicitly, never `last_dispatch`. Spec key `refusal_retry_reads_its_own_chain`.
- **`launch` lock release (M1, M2).** A context `unbooked(dispatch)` releases only on a chain thread AND with a non-empty dispatch; the conductor and delivery calls never release. `mark_in_flight` and `clear_in_flight` run under the lock; the re-take sits in the `finally` of `unbooked`, inside the `try` that precedes `finally: clear_in_flight`, and happens exactly once on `BaseException`. `self._book` is a plain `threading.Lock`, one acquire per chain at chain start, no nesting, so an accidental nested acquire shows at once rather than serializing silently. `self.sleep(delay)` in `run_claude`'s retry backoff releases too.
- **Critic `start` outside the lock (scout's last hazard).** `story_step start` of a critic runs `probe_debt.settle` with a 90 s budget, which under the lock would stop every chain's bookkeeping. So on a chain thread, a critic's `self.step("start", ...)` runs in `unbooked` plus a second lock `self._settling`, one settle at a time. Order: release `_book`, take `_settling`, run, release `_settling`, take `_book`; `_settling` is never held while waiting for `_book`, so no deadlock. Controller writes inside are safe by `events.lock` with the 10 s CLI wait (`story_step.py:3287`). Invariant: the story-wide settle memory has one writer at a time; a running chain's bookkeeping does not wait for another window's settle. `stand_check` and `build_check` stay under the lock: unmeasured, P2-1 times them; N-LIVE decides.
- **Interrupt (M1).** Ctrl-C reaches the main thread only. Main sets the drain, kills every `proc` in the registry, joins with a capped timeout, re-raises. A chain's `proc.kill()` alone would not run. Driver killed hard: `in_flight` stays on disk and reads as "the process is gone", as today.
- **Admission.** Only the scheduler passes `--parallel-window` (on `story_step start`, on `controller rework`). Everything else keeps the old refusal text byte for byte. Invariant: no S1-S4/S6-S9 dispatch, no plan dispatch, no conductor or skill-road `start` ever runs beside another; two running dispatches never share a case; `inject_context` never meets two.
- **Per-turn steps (F12).** `owed_rows_step`, `ticket_rework_step`, `seam_rework_step`, `answer_rework_step`, `code_close_step`, `consumer_word_step` and the STUCK count run at the main loop, so inside `stage_S5` they wait for the drain, by the recommendation. Launches happen only from `stage_S5`. `until_reached` is stage-level (`UNTIL_PAST`), so it holds for the whole stage and is checked at entry as today; `max_boundaries` counts each launch and on reaching it starts the drain.
- **Console.** Each line printed in a chain carries `[W<n>]` through a thread-aware `sys.stdout` wrapper installed only on the new road (hundreds of `print`s are not edited). `progress_line`: `windows running: 3,4,5 of 7 · closed 1,2`.
- **Repair rounds** stay per window (`window_key`, `repair_key`, controller ledger).

### 3.3 Shared files: one writer each (AR-14; corrected by the scout)

| file | writer in parallel | decision |
|---|---|---|
| `state/controller.json`, `events.jsonl` | `story_step` and controller ops; one `events.lock` per story | CLI mains already wait 10 s (`LIFECYCLE_WAIT_SECONDS`). Wait-0 writers `subagent_journal:167`, `environment_preparation:230` get the bounded wait (TR3-14). Invariant: a busy lock never silently loses an event |
| driver state, `driver-runs.jsonl`, `driver-runs/<dispatch>.json` | all chains | under `_book`; `in_flight` per dispatch already |
| `work/automation-manifest.json` | `manifest_put`, `manifest_from_tests` | merged under `events.lock`; CLI already waits 10 s (t-2034 M6: the first draft's "0" is stale; 30 s is withdrawn). Invariant: no write lost; over the wait the writer is told, exit non-zero |
| `work/handoffs/<dispatch>.yaml`, `windows/`, `briefs/`, `digests/`, `run-blocks/`, `probes/`, `state/findings/<dispatch>-digest-notes.md`, `state/execution-jobs/`, `work/evidence/runs/<job>/` | per unit | no change |
| `work/test-code/critic-findings.md` | each critic | `critic-findings-<dispatch>.md` (TR3-5) |
| `work/probe-debt.json` | settle | `work/probe-debt/<dispatch>.json` + story-wide memory `work/probe-debt-memory.json` (TR3-15). Three literal definitions become one |
| `work/advice-S5.json` | exit-gate hook at every S5 stop of either role (scout: not "before each critic"), non-atomic | `work/advice-S5-<dispatch>.json`, atomic. The critic reads its author's: `advice_of` (TR3-15) |
| `work/s5-notes.md` | BOTH roles append (scout: the first draft's "read-only" is false); no writer row | F15: per-dispatch `work/s5-notes/<dispatch>.md`, read whole by the brief (TR3-15) |
| `work/judge-code.json` | `judge_code.py` at each critic's start | `work/judge-code-<dispatch>.json` (TR3-15) |
| `work/sizing.json` | `sizing.py` adviser at each stop | same arithmetic; make the write atomic so a reader never sees a torn file (TR3-15) |
| `state/driver-question.md`, `driver-questions.jsonl` | main thread only | one question per turn (3.2); no queue |
| exit gate state `_mutate_state` | hooks of parallel sessions | wait 1 s -> 10 s, printed when used. Invariant: a busy lock never reads as "gate passed" (TR3-6). Not read by the scout; the builder reads it first |
| `state/window-files/` | `window_files.py` only | new (TR3-16) |
| project test files | automators; critic probes in place | F3 (b): first-write ownership + launch gate |
| project support files (page objects, fixtures, config, `package.json`) | automators | F10: not claimed, by the recommendation. Two windows can create the same helper (scout): the critic's review judges it, after the fact |
| report | `run_suite` | per job (`unique_report`; scout 2c). No change |
| `test-results/` | the project's runner | not in the package; shared unless the project's command says otherwise. Serial stand: the lease serializes. `run.parallel: true`: 3.6 |
| stand DB / app | runs and probes | `stand_lease`; `stand_wait_s` 1800. A timed-out wait answers `stand_busy`, exit 3 (scout). Invariant: a queue timeout never reads as a window's failure: the automator sees "stand busy" and the brief says what to do; key `stand_busy_is_not_a_window_failure` (TR3-6). With three windows and critic probes (27 min seen) 1800 can run out: N-LIVE reads it |
| git index of the stand | nobody in S5 | no change |

### 3.4 Failure edges

- One chain raises: 3.2 "Seam after the drain". No other window's accepted work is lost; the failing window resumes by existing roads.
- Driver killed mid-parallel: on restart `in_flight` + controller `running` + `driver-runs/<dispatch>.json` tell each window's state; `s5_serial_reason` says "dispatches running or stopped at entry"; each goes through the existing resume road with `_resume_problems` admitting it. Invariant: a registered dispatch is run once, never twice.
- A window that can never launch for the gate: when nothing else runs it launches.
- N larger than windows: N = min(config, windows).
- A zero-closer: every window accepted and S5 still open reaches today's refusal in `stage_S5` ("run recover first"), unchanged. It stays reachable as the safety net.
- Identity unknown: `own` returns None, the callers' existing "unknown" roads apply, and the exit detector says `UNREADABLE`. Never another window's dispatch, never "every case".

### 3.5 Tests (FR-31)

Harness: `story_run_common.STUB` gets per-call start/end log lines and a BARRIER, not a sleep (M5): a call waits for its peer's start marker, with a capped timeout that fails naming the peer. Assertions are on order and overlap of logged intervals, never on wall clock. `seed()` pins `dispatch.parallel_windows: 1` so old tests keep their meaning (47 test files name a multi-window id, t-2034); new rigs leave the key out.

Equivalence suite (TR3-18), what ships at N=3: the same stub story at N=1 and at the default, compared order-free: final dispatch statuses, accepted set per window, manifest, per-window round counts, questions asked and their answers. Then each seam at the default: repair limit, debt, owed round, mechanical round, halt, question threshold, infra cut with a resume, conductor refusal, driver killed mid-run, `--until`. Fixtures: arm-B overlap shape and arm-A no-overlap shape.

Literal N=1 (a test of an explicit project choice): the expected list is FROZEN from the pre-change run into the test: stub call sequence, `events.jsonl` event sequence, driver-state keys, console text; plus `no_thread_started_at_n1`.

### 3.6 "Impossible, so serial": one function, one printed reason per run

`Driver.s5_serial_reason() -> str`; "" = parallel. One line through `state["noted"]`: `note: S5 windows run one at a time: <reason>`. Never a question, never a stop (P5, FR-59). Direction of error: it may say serial needlessly on doubt; it must never let two windows run where a row below holds.

| case | why | carrier |
|---|---|---|
| `dispatch.parallel_windows: 1` | project's word; the old road literally (not this function's cap) | `config_contract.parallel_windows` |
| any road but the driver (skill, conductor) | no scheduler there | no `--parallel-window` flag: controller's old refusal |
| host is not Claude (`self.host`) | hook env and receipts unmeasured there (S-14) | `Driver.host` |
| dispatches running or stopped at entry; an owed round, a pending debt | B3: settle them first; after they settle the reason falls away and the remainder runs parallel in the same stage | controller + `repair_limit` |
| a story begun before the upgrade (mid-S5 with an old `critic-findings.md` or `probe-debt.json`, no per-dispatch file, windows already accepted) | temporal: readers fall back to old files for its remainder | artifact presence |
| window state or scope unreadable | FR-59 | `s5_open_windows` raises |
| a project whose build or runner compiles the whole test tree | W1's half-written file reds W2's run | F11: `dispatch.parallel_windows: 1`, recorded at onboarding |
| `run.parallel: true` | runs overlap and `test-results/` is shared unless the project's command says otherwise; F2(a) stood on the lease | F16: `stand_is_serial` false; the note names the door: `run.parallel: false` queues the runs and the windows go parallel |
| model-service limit in one chain | gateway concurrency is a given (P25) | F13: `InfraStop` kind; continue at cap 1 for this run |

Not "impossible": `run.parallel: false` (template default; runs queue on the lease, sessions overlap). Under F3(b) a window that names no file is no serial case.

Temporal: the reader of the key is inert until TR3-6, so the default takes effect in the commit that lands the scheduler, and `seed` pins 1 before that (TR3-12).

### 3.7 The seam the walker uses (TR3-9, t-1957 N5p; no more than this)

`Driver.run_chains(items, launchable, chain_fn, cap) -> None`: the registry, thread start, `_book`, `unbooked`, `as_chain`/`adopt_chain`, drain, seam selection. Not S5-specific by signature. Carried to TR3-9 as twins of B1, B3, B4 (t-2034; SIBLING_MAP axis 5): the S6 identity sites of 3.1, the S6 close predicate, and thread-locals. t-1957 calls the runner `S5Scheduler` and the lock an RLock: its lines 205 and 932 change with TR3-9's own revision, not here.

## 4. Forks

Closed: F1 (a), F2 (a), F5 (a), F6 (a) as serial behaviour plus B5's exclusion, F7 (a), F8 (a), F9 void (t-1936 merged). F3 is (b) and F4 is 3, coordinator's decisions above.

Open, each with a recommendation; the nodes are written to it.

- **F10. Project support files (page objects, fixtures, config).** (a) not claimed: the guard claims only test bodies (`test_files.is_test_for("test_body", ...) is True`); two windows may touch a helper; the host's Edit refuses a stale read, and the critic judges duplicates [recommended: a "new file" door does not work for a shared helper, so claiming them means waits, against the owner's word]; (b) claimed with door "wait": a working role stops; (c) forbid helper edits during S5: breaks P17. Unmeasured; N-LIVE reads reds on helpers.
- **F11. A project whose build compiles the whole test tree.** Code cannot infer this (P2). (a) an interview topic asks once in plain words and records `dispatch.parallel_windows: 1` [recommended: carrier is the existing key, no new state]; (b) a new key `dispatch.tree_compiles_whole`: one more key for one meaning; (c) no carrier: the role sees reds and reports them: silent cost on such projects. Touches intent: the Lead may take it to the owner.
- **F12. Per-turn steps during a parallel S5.** (a) they wait for the drain, launches only from `stage_S5` [recommended: a step's trigger is mostly a person's answer, and every answer enters at a new driver turn]; (b) drain on every turn: batches, the refill gain is lost; (c) read-only predicates for each step: six new functions. Not traced: whether a role's finish alone can make one of the six owed; TR3-6's builder lists each step's inputs in its report, and a step that can be made owed by a finish is a fork back.
- **F13. Model-service limit in one chain.** (a) drain, then continue at cap 1 for this run, with a note [recommended by t-2034's table: P25 makes it a given; a stop loses the run]; (b) stop as today. The kinds of `InfraStop` were not read (`infra["kind"]`): TR3-6 names which kind is "limit" from the data table, and any other kind stops as today.
- **F14 (conditional).** If the experiment in TR3-13 finds hooks do NOT inherit `QA_FACTORY_DRIVER_RUN`, TR3-13 stops and returns: B1's hook road has no source (the PreToolUse event names no agent, S-12). No alternative is verified; a candidate is mapping `session_id` of the event to `in_flight`, which holds it only on resume.
- **F15. `work/s5-notes.md` has two appending roles and no writer row.** (a) per-dispatch `work/s5-notes/<dispatch>.md`, the brief reads all of them plus the old file [recommended: no lock, no tool, no merge step; a sibling running now is not seen until the next launch, which is what a parallel session can know anyway]; (b) a locked append tool: one more script the role must call; (c) the driver merges after each chain: a second writer.
- **F16. `run.parallel: true` projects.** (a) serial, with the note naming the door `run.parallel: false` [recommended: FR-59 safe default; a working door with no new code; MyBooks is `false`]; (b) parallel on the project's word, with a note; (c) force the lease for S5 only: a change in `run_suite`. Whether Playwright empties a shared output dir is "estimate, not verified" (scout 2c).

## 5. Small choices closed by the designer

- Reader's module and name: `dispatch_identity.py`, no imports beyond `os` (it runs at every hook; AR-12).
- `_book` a plain `Lock`, not the first draft's RLock (M1 allowed either; this is the shorter proof).
- New fast test files instead of keys in big ones where the file would be CI-only: the witness stays local.
- Dispatch field and flag `parallel_window` / `--parallel-window`; accept field and flag `open_windows` / `--open-windows`. `record-schemas.json` has no `additionalProperties` (grep: 0; control: `"Dispatch"` at :174), so no schema row is forced; the DoD adds none.
- Claim file name = sha1 of the project-relative path with forward slashes, under `state/window-files/`, created with `O_CREAT|O_EXCL`.
- Console prefix `[W<n>]`, ordinal in `stage_scope` order. Watchdog poll 60 s. `wall_ms` note 120 s. Exit-gate lock wait 10 s.
- New batch ids TR3-12..TR3-18 are proposals; the Lead checks them against the batch tip.

## 6. Nodes

Common to every writing node. **given:** `design/factory-rules.md` whole, `plans/builder-rules.md`, this spec, this node's rows of 3.1/3.3, `docs/tasks/specs/reviews/t-2034-critic-plan-t1937.md`, the scout report. **non-goals:** section 1's, plus every other node's owns. **handoff:** report `docs/tasks/specs/reports/<task>-<node>-report.md` + commit on the batch branch. **DoD adds:** the acceptance keys named; the AR change checks of section 1 for this node; FR walk lines; `architecture:` and `judgment:` lines in the commit; `changelog.d/` fragment. **Witness scope:** builder-rules 7b: the fast test FILE per owned path, each under a minute; `test_story_run_*`, `test_controller_*` and any listed slow file are not run locally and not waited for: CI; BATCH CANON = CI pipeline (D-0059). A worker reports analogs and does not widen.

Mapping of first-draft ids:

| spec node | batch node | what | builder hours (estimate) | depends |
|---|---|---|---|---|
| N-P1-0 | TR3-1 | scout, DONE (report present) | - | - |
| N-P2-1 | TR3-2 | timing + wait, with the t-2034 additions | 3 | - |
| N-P1-3 | TR3-3 | key on `tr/tr3-3` | done | - |
| N-P1-3r | **TR3-12 (new)** | interview topic, `seed` pin, batch rows | 1 | TR3-3 |
| N-P2-2 | TR3-11 | DONE on `tr/tr3-11` | done | - |
| N-P1-1a | **TR3-13 (new)** | experiment, identity reader, S5 exit readers | 3 | TR3-12 |
| N-P1-1b | **TR3-14 (new)** | hook readers | 2-3 | TR3-13 |
| N-P1-1c | TR3-4 | controller: admission, stage record, resume, close fields | 3 | TR3-3 |
| N-P1-2a | TR3-5 | findings per dispatch | 2-3 | TR3-13 |
| N-P1-2b | **TR3-15 (new)** | debt, memory, advice, notes, judge, sizing; settle exclusion | 3 | TR3-11, TR3-5, TR3-13 |
| N-P1-5 | **TR3-16 (new)** | claims + guard, now live | 3 | TR3-13 |
| N-P1-4a | **TR3-17 (new)** | chain record, thread-locals, stream, `closes` explicit: no behaviour change | 3 | TR3-2 |
| N-P1-4b | TR3-6 | scheduler, lock, close predicate, serial reason, seam; the default takes effect here | 3 | TR3-4, TR3-5, TR3-12, TR3-14, TR3-15, TR3-16, TR3-17 |
| N-P1-4c | **TR3-18 (new)** | equivalence suite and seams at the default | 2-3 | TR3-6 |
| N5p | TR3-9 | walker; its dependency stays TR3-6 | t-1957 | TR3-6 |
| N-LIVE | live proof row | MyBooks S5, FR-33 | owner's run | all |

Order on hot files: `story_run.py`: TR3-2 -> TR3-17 -> TR3-6 -> TR3-18 (tests) -> TR3-9; TR3-13 touches `exit_errors` only, TR3-5 `s5_author_round` only (function-disjoint, D-0048). `guard_pre_tool.py`: TR3-5 (`_owner_of_path`), TR3-14 (`dispatched_role`, `_dispatch_open_for_owner`, `owner_check`), TR3-16 (new function + its call in `main`): function-disjoint; a later node merges and resolves. `probe_debt.py`: TR3-11 -> TR3-15. `brief_pack.py`: TR3-5 -> TR3-15. `story_step.py`: TR3-2 (`start` timing) / TR3-13 (`_finish_gate`) / TR3-4 (`start` flag, `finish` flag) / TR3-15 (`_debt_input`, `DEBT_REL`, PRE_WORK row): function-disjoint. `controller.py`: TR3-4 only; TR3-5 changes the one text line :6860 after it. Batch rows must be rewritten to these owns (M6: `piles.py` zone checks read them); the batch's row TR3-3 "с умолчанием 1" and the finding's line are stale.

Parallel now: TR3-2, TR3-12, TR3-4. After TR3-13: TR3-14, TR3-5, TR3-16. Writers cap 6 stands.

### TR3-12 (N-P1-3r) — interview topic, `seed` pin
tier: builder.
owns: `PKG\skills\qa-onboarding\phases\p2-interview.md`, `PKG\scripts\tests\story_run_common.py` (`seed` only), `PKG\scripts\tests\test_config_migration.py`.
Do: (1) the topic of F11, in plain words (P9), writing `dispatch.parallel_windows`; recorded once; its note says "windows run in parallel; serial if ...", and a project that does not answer stays at 3. (2) `seed` writes `dispatch: {parallel_windows: 1}`.
edges: `seed` called with its own `dispatch` block: the key merges in, the caller's other keys stay; a caller that sets the key wins. Touched `story_run_common.py`: report line "тронут story_run_common.py"; `test_story_run_*` in the canon. Invariant: old tests keep their meaning; a rig that wants the default leaves the key out through a named argument `parallel_windows=None`.
tests: `interview_asks_the_compile_question`, `seed_pins_one`, `seed_none_leaves_key_out`.
witness: `python -B PKG/scripts/tests/test_config_migration.py`.

### TR3-13 (N-P1-1a) — experiment, identity reader, S5 exit readers (B1)
tier: builder; critic mandatory (a gate's reader).
owns: `S\dispatch_identity.py` (new), `S\tests\test_dispatch_identity.py` (new), `S\planning_contract.py` (`DETECTOR_DISPATCH_ENV` only), `S\s5_precheck.py` (`running_dispatch`, `window_dispatch`, `detector_main`), `S\branch_accounting.py` (`_s5_window`, the cause text of `s5_check`), `S\exit_gate.py` (`holding_dispatch` new, `_detector_env`, `_live_dispatch`), `S\story_step.py` (`_finish_gate`), `S\story_run.py` (`exit_errors` only), `PKG\design\driver.md` (the line naming the var), `docs/SIBLING_MAP.md` (new axis).
Step 0, one experiment (hygiene 6a; "hooks inherit the var" is expected, NOT measured): a scratch project with a PreToolUse hook and a Stop hook that each write `os.environ.get("QA_FACTORY_DRIVER_RUN")` to a file, one `claude -p` launched with the var set, one Bash call in it writing the same. Verbatim file contents in the report. If negative: stop and return F14.
Reader:
`dispatch_identity.named() -> str`: `QA_FACTORY_DETECTOR_DISPATCH` first (the gate names the finisher), then `QA_FACTORY_DRIVER_RUN`; stripped; blank is unset.
`dispatch_identity.own(dispatches, role="", stage="", statuses=("running",)) -> dict | None`: `dispatches` a mapping or a list. With a name: the record found and its status in `statuses` and role/stage match when asked: it. Found and not matching: None, NOT the count rule. Name not in this story's records: the count rule. No name: the count rule, exactly today's: `live[0] if len(live) == 1 else None`.
Error direction (a function that picks whose work is judged, in a gate): it may answer None; it must never answer another window's dispatch. Adversarial inputs that stay safe: two automators with a name; automator + critic where the critic's session asks for the automator (None); a name for a closed dispatch (None); a name of another story's id absent here (count: at 2+ None); blank or whitespace env; a dispatches value that is a list, None or holds non-dicts (no raise); an id that exists in this story and also in another (`S5-qa-automator-1` exists in every story): a driver child works on one story, so accepted residual: role and stage must still match, and it is named here on purpose.
Callers: `running_dispatch` through `own(role, stage)`; `window_dispatch`: named first with `statuses=(running, returned_unaccepted)`, then today's (a), (b); `detector_main`: 2+ running automators and no name: print `UNREADABLE: two or more windows are running and this check was not told whose handoff it judges`, exit `DV.EXIT_UNREADABLE`, never `run(root, None)`. Zero running with no name keeps today's road. `_live_dispatch` through `own`. `holding_dispatch(id)`: the twin of `holding_stage` (a context, restored on exit, a process global, safe because the driver's calls are under `_book` and `story_step finish` is its own process). `_detector_env` pops and sets the new var only beside a named story. `_finish_gate`: `with exit_gate.holding_stage(stage), exit_gate.holding_dispatch(dispatch["id"])`. `Driver.exit_errors`: wraps with `holding_dispatch(self.last_dispatch)`. `s5_check` cause: "2 or more automators are running and none was named" instead of the false "no running".
Temporal: before TR3-4 two running dispatches cannot exist, so every road takes the count rule's answer through a named or unnamed path with the same result: `no_env_one_running_same_as_today`.
tests (fast, in the new file, real `s5_precheck`/`exit_gate`/`branch_accounting` functions over a seeded state): `named_wins_over_count`, `detector_dispatch_beats_driver_run`, `env_other_role_is_none_not_count`, `closed_dispatch_named_is_none`, `unknown_id_falls_to_count`, `no_env_one_running_same_as_today`, `no_env_two_running_none`, `blank_env_is_unset`, `returned_named_found_only_when_asked`, `finish_with_two_automators_judges_own_scope`, `detector_two_running_no_name_unreadable_never_every_case`, `digest_scope_read_with_two_automators`. Detector shape check: `test_s5_precheck.py`, `test_branch_accounting.py`, `test_exit_gate_scope.py` in CI, except `test_exit_gate_scope.py` local.
witness: `python -B S/tests/test_dispatch_identity.py`; `python -B S/tests/test_exit_gate_scope.py`; Step 0's file contents.
Answers: B1 (identity, row s5_precheck, branch_accounting, exit_gate).

### TR3-14 (N-P1-1b) — hook readers (B1)
tier: builder; critic with TR3-13's pass (one topic, R13-g).
owns: `S\stage_guard.py` (`rule_typed_runner`, `_judge_slice`), `S\guard_pre_tool.py` (`dispatched_role`, `_dispatch_open_for_owner`, `owner_check`, `_any_story_open_for_owner`), `S\subagent_journal.py` (the `record_return` call), `S\environment_preparation.py` (:230 call), `S\tests\test_guard_window_identity.py` (new).
Do: `rule_typed_runner`: `current` for each slice = `own(dispatches)` when named; no name and one active: it; no name and 2+: the active record whose id is the request item's `dispatch_id`, else the old refusal text. A named session's request carrying a sibling's id: refused, today's text. `dispatched_role`: `own(dispatches)` first; no name: today's first-running. `_dispatch_open_for_owner(controller, owner, named=...)`: with a name, reading (1) is open only if the named record's role is the owner; no name: today's "any". Reading (2) unchanged. `subagent_journal` and `environment_preparation` pass `wait_seconds=LIFECYCLE_WAIT_SECONDS`; the swallowed exception still swallows after the wait, and leaves one line in the hook's log.
edges: invariant, a non-owner session never opens the owner guard because a sibling of the owner runs (`critic_of_w2_cannot_write_automator_artifact_while_w1_runs`). A hook's own time budget against a 10 s wait: `test_hooks_wiring.py` (hook type, so it runs) and the timeout value in `hooks.json` read by the builder; a wait longer than the hook's timeout is a return to the Lead. No name and no running dispatch: today's roads byte for byte. Unreadable controller: today's roads.
tests: `run_request_of_second_window_passes`, `run_request_of_sibling_id_refused`, `run_request_no_name_two_active_matched_by_id`, `dispatched_role_names_own_role`, `critic_of_w2_cannot_write_automator_artifact_while_w1_runs`, `owner_of_named_session_writes`, `journal_waits_for_busy_lock`.
witness: `python -B S/tests/test_guard_window_identity.py`; `python -B S/tests/test_hooks_wiring.py`; `test_stage_guard.py` (58 s) local; `test_guard_dispatch_budget_and_logs.py` CI.
Answers: B1 (stage_guard, guard_pre_tool rows), S-7, S-12, S-13, S-15.

### TR3-4 (N-P1-1c) — controller (B1, B3, S-2, S-3)
tier: builder; critic mandatory (core).
owns: `S\controller.py` (`_window_beside_running` new, op `dispatch` :4965 branch, `_resume_problems`, `build_rework_request` + `rework` op arg, apply `accept/checkpoint` and `resume` `set_stage` calls, accept validate `open_windows` + backstop), `S\story_step.py` (`start`, `finish`: flags only), `S\tests\test_s5_parallel_admission.py` (new, fast by not spawning a driver; not named `test_controller_*` on purpose), `PKG\design\controller-blocks.md` (regenerated), `PKG\references\state-exits.md`.
Do:
1. `_window_beside_running(p, state, running)` is True only when: `p["parallel_window"] is True`; `p.stage == "S5"`, role automator or code critic, `s5_part_of(p) != "plan"`; every running dispatch is an S5 window dispatch of those roles; all scopes readable and pairwise disjoint with `p`'s; `len(running) + 1 <= config_contract.parallel_windows(config)[0]`, config read by `_project_root`. Anything else: the old text, byte for byte. POSITION: the first check in the op's branch, before `required`. It reads with `.get` because `required` has not run. Invariant: all checks below it still run on the admitted dispatch; what no one flagged stays refused.
2. `_resume_problems`: the `running` refusal does not apply when `d` is an S5 window dispatch, and every running one satisfies the same clause (a stopped window resumes beside its siblings). Resume is the driver's restart road, so no flag: the stage + role + scope clause carries it. Count cap applies. Invariant: a non-S5 resume keeps the refusal; two dispatches never share a case.
3. Stage record: when the accept or checkpoint of an S5 dispatch would write `pending` (or a stop status) and another S5 dispatch is `running`, the stage keeps `running`, with `dispatch_id` of a running one. Invariant: "stage running" stays true while a window runs; a replay gives the same state (derived from state at that sequence); a journal with no two running dispatches replays byte-identical (`replay_serial_journal_identical`). `resume` :1591 same.
4. Accept: a request `open_windows: [cases]` lifts the "no role to close it" refusal at :5330 only when every case names a real window of `stage_scope` other than this dispatch's. Bad name: refused, naming the windows. Not with `unresolved`. `story_step finish --open-windows` carries it. Invariant: the silent `false` on a truly last window is still refused (`bare_not_complete_on_true_last_refused`).
5. Backstop: `stage_complete: true` on S5 refused while another S5 dispatch is `running`, naming it, door: `--not-complete --open-windows <its cases>`; person's word route as every S5 close refusal. Never reached if `s5_open_windows` is right; it is the code gate under a driver-side predicate.
6. `stage_complete` auto-set at :4601 stays: the driver always passes explicit.
edges: scope empty or missing on a running dispatch: not disjoint: refused. `parallel_window` not literally True (a string, 1): refused. Config absent or unreadable: reader's default 3. TR3-3 not merged: this node depends on it. A `returned_unaccepted` sibling: not `running`, so not counted, its scope still checked for disjointness. `_closes_stage` itself unchanged: its other callers' meaning stays; the critic's note "whether a bare `--not-complete` is refused now depends on finish order" is what item 4 settles. Today's road for a last window's own test_defect round is NOT traced by this designer (`--not-complete` with no others open): unchanged, pinned by `own_round_last_window_same_as_today` on a recorded pre-change expectation.
tests: `parallel_s5_windows_admitted_disjoint`, `overlapping_scope_refused`, `plan_dispatch_runs_alone`, `non_s5_refused_while_window_runs`, `count_over_cap_refused`, `no_flag_keeps_old_refusal_text`, `skill_road_second_start_keeps_old_refusal`, `find_active_narrows_by_disjoint_case`, `resume_beside_running_window`, `resume_non_s5_refused`, `accept_w1_leaves_s5_running_while_w2_runs`, `replay_serial_journal_identical`, `open_windows_lifts_refusal`, `open_windows_bad_name_refused`, `bare_not_complete_on_true_last_refused`, `stage_complete_refused_while_other_s5_running`, `own_round_last_window_same_as_today`.
witness: `python -B S/tests/test_s5_parallel_admission.py`; `test_controller_*` in CI.
Answers: B1 (admission, `_resume_problems`, driver-only marker), B3 (controller part), S-1..S-3, S-6, S-16, scout 1c, t-2034 q.2.

### TR3-5 (N-P1-2a) — findings per dispatch (t-2034 item 5)
tier: builder; critic as package change.
owns: `PKG\agents\qa-code-critic.md`, `PKG\handoffs\s5-critic-to-automator.yaml`, `PKG\references\code-review-rubric.md`, `PKG\references\ahead-cards.json`, `PKG\slices\qa-code-critic\handoff-keys.md`, `PKG\references\artifact-writers.json`, `PKG\references\stages.json`, `PKG\references\collect-sets.json` (findings row if any), `S\handoff_check.py` (`_findings_file`), `S\brief_pack.py` (:90-91 inputs), `S\ledger.py` (:1123), `S\controller.py` (:6860 text only), `S\guard_pre_tool.py` (`_owner_of_path`, `_is_path_key` caller), `S\story_run.py` (`s5_author_round`, its call in `s5_window`), `S\tests\test_findings_per_dispatch.py` (new).
Do: the critic writes `work/test-code/critic-findings-<dispatch>.md`; the path is in its brief and form skeleton. Registry row `work/test-code/critic-findings-*.md`, and `_owner_of_path` matches a PATH key whose base has `*` by `fnmatch`; a key without `*` keeps the exact match. `_findings_file(art, doc, row)`: the file of THIS form's dispatch; absent: `critic-findings.md` (old story); never "the newest on disk". `s5_author_round(..., critic)`: the file of that critic, fallback as above, then the digest. `brief_pack` S5 inputs for the automator: the findings of its rework's critic; for the critic: `work/test-code/` stays. `ledger`: its glob already takes both: keep, sort stable.
edges: temporal: both worlds: an old story has `critic-findings.md` and readers fall back; the new world never writes it. Invariant: a window's handoff and an author's round never read another window's findings (`findings_of_w2_not_read_by_w1`). S4's `work/test-cases/critic-findings.md` is untouched (`s4_owner_unchanged`). A dispatch id with characters unsafe in a name: ids are `S5-qa-code-critic-N`; no sanitizing. An `*` key may not claim the old exact name twice: old row stays, first match wins as today (FR-39 test on the exact path).
tests: `findings_of_w2_not_read_by_w1`, `findings_old_story_falls_back`, `author_round_reads_its_critic`, `owner_of_per_dispatch_findings_is_critic`, `s4_owner_unchanged`, `brief_of_rework_names_its_findings`.
witness: `python -B S/tests/test_findings_per_dispatch.py`; `python -B S/tests/test_artifact_writers.py`; `python -B S/tests/test_guard_write_owners.py`; `python -B S/tests/test_brief_pack.py` (14 s). `story_run` reader in CI.
Answers: t-2034 item 5, M6 (batch row), AR-13, AR-14.

### TR3-15 (N-P1-2b) — debt, memory, advice, notes, judge, sizing; settle exclusion (B5, items 1, 6; scout 2a)
tier: builder; critic as package change.
owns: `S\probe_debt.py` (`DEBT_REL` -> `debt_rel(dispatch)`, `MEMORY_REL`, `settle`, `_memory_doc`, `_previous_attempts`, `STABLE_LEFT`, `main`), `S\story_step.py` (`_debt_input`, `DEBT_REL`, PRE_WORK row :229, brief line :196, `_settle_probe_debt`), `S\brief_pack.py` (`PROOF_DEBT`, :90-92, the `advice` input), `S\exit_gate.py` (`write_advice`, `run_advisers`), `S\judge_code.py` (:316, :354), `S\sizing.py` (the write), `S\controller.py` (`S5_NOTES`, the `read_first` site; order on this file: TR3-4, TR3-5 at :6860, TR3-15), `PKG\agents\qa-automator.md`, `PKG\agents\qa-code-critic.md` (notes, advice lines), `PKG\skills\qa-story\phases\s5.md`, `PKG\references\collect-sets.json`, `PKG\references\artifact-writers.json`, `PKG\references\stages.json`, `S\tests\test_probe_debt.py`, `S\tests\test_window_artifacts.py` (new).
Do:
1. Debt per dispatch: `work/probe-debt/<dispatch>.json`, one constant, every carrier in one commit. `_debt_input` reads only its own; absent: the old file by today's rule.
2. Memory: `work/probe-debt-memory.json`: the last settle's doc whole, same shape, written by settle after the per-dispatch file; `_memory_doc` reads it, absent: the old `work/probe-debt.json`, absent: no memory, run. Invariant: memory is one story-wide file, one settle at a time (`_settling`, TR3-6); an unreadable one means run (t-2043's direction).
3. Own word: a kept rebind's reason `rebind_same_bytes`; `STABLE_LEFT` follows; `same_bytes` stays the probe's. Test renames follow.
4. **B5.** `settle` leaves any item whose case belongs to, or whose test file is in the file set of, a dispatch `running` or `returned_unaccepted` other than the settling dispatch, with reason `running_window`, no subprocess. POSITION: after the memory read and before the stale door, rebind and probe. Invariant: a settle never touches a running window's file; the item stays owed to that window's own critic. Keeps F6 (a) as serial behaviour: at N=1 no other dispatch runs and the branch never fires (`settle_serial_unchanged`). `running_window` is not in `STABLE_LEFT` (so `_nothing_changed` runs the scan). Error direction: may leave needlessly, never probes under a live author. Unreadable state: leave all out-of-scope items.
5. Advice: `write_advice` writes `work/advice-S5-<dispatch>.json` atomically, by `own()` in the hook and `holding_dispatch` at finish. No identity: the old `advice-S5.json` (skill road, serial). `advice_of(task_root, critic)`: the file of the latest accepted automator of the critic's window, then the old file; `brief_pack` names it in the critic's inputs. Non-S5 stages keep `advice-<stage>.json`.
6. Notes (F15 a): both role files name `work/s5-notes/<dispatch>.md`; `brief_pack` and the driver's "read first" line list the old file and every per-dispatch file; registry row and `stages.json` output.
7. Judge: `work/judge-code-<dispatch>.json`; PRE_WORK, brief line, `s5.md` follow.
8. `sizing.py` writes atomically.
edges: per-dispatch file written, memory write fails: settle reports it, the critic has its input; next settle runs. An empty settle: today's rule "not an input". `unchanged_since` re-address writes the per-dispatch file from memory. Old story mid-S5: readers fall back; serial reason holds (3.6). Invariant across all: a critic never reads another window's debt, advice, judge file (`critic_reads_only_its_window`).
tests: `settle_never_touches_running_window` (runner raises on any call for the item), `settle_serial_unchanged`, `memory_survives_per_dispatch_files`, `memory_absent_reads_old_file`, `memory_unreadable_runs`, `kept_rebind_has_own_word`, `debt_input_reads_only_its_own`, `debt_old_story_falls_back`, `advice_per_dispatch_atomic`, `advice_no_identity_old_path`, `critic_reads_only_its_window`, `notes_of_both_windows_in_next_brief`, `judge_per_dispatch`.
witness: `python -B S/tests/test_window_artifacts.py`; `python -B S/tests/test_probe_debt.py` (12 s); `python -B S/tests/test_judge_code.py`; `python -B S/tests/test_artifact_writers.py`; `test_story_step_start.py` (16 s) local.
Answers: B5, t-2034 items 1, 6; M6 (TR3-5 row); scout's three-definitions hazard; `s5-notes`, `advice-S5`, `sizing` rows.

### TR3-16 (N-P1-5) — first-write ownership (F3 b, now live; B2)
tier: builder; critic mandatory (a guard hook; rule 2: self-activating enforcement goes through the Lead at acceptance; here the function is in an already active file, so the critic gate carries it).
owns: `S\window_files.py` (new), `S\guard_pre_tool.py` (`window_file_check` new, its one call in `main`'s Write/Edit branch), `PKG\agents\qa-automator.md` (ownership line), `PKG\agents\qa-code-critic.md` (fact line), `PKG\references\artifact-writers.json`, `PKG\references\stages.json`, `PKG\references\state-exits.md`, `PKG\design\controller-blocks.md` or the guard's A24 row as the detector demands, `S\tests\test_guard_window_files.py` (new).
Module (one writer, AR-14): `claim(task_root, rel_path, window, dispatch) -> owner_window`: `O_CREAT|O_EXCL` on `state/window-files/<sha1>.json`, content `{path, window, dispatch, at}`; the loser reads the file. `owner(task_root, rel_path)`. `files_of(task_root, window)`. `release(task_root, window)`: the driver at a window's close (TR3-6). `window` = `Driver.window_id("S5", scope)` of the dispatch record.
Guard: `window_file_check(event)`, in order: no name (`named()` empty): return. Not an S5 window dispatch of `qa-automator`: return. Target path not a test body by `test_files.is_test_for("test_body", rel, cfg, root=project) is True`: return (F10; `None` is not a test: support files and unknowns pass). Own window: return. `claim`; lost to a live other window: refuse.
Refusal text, English, FR-1, FR-2: `this test file belongs to window <cases> until that window closes. Put your test in a new file in the same directory: <dir>. Where a test lives stays your choice (P17); a test in a new file is judged the same.` No waiting door. A person's word: recorded by the conductor as any block (builder-rule 8). Friction: a refusal is counted by the fuse (the counter at `guard_pre_tool.py:79-80`, there is no function named `_fuse`), the role in the trap writes a finding (P15).
Told before the work (FR-38, AR-10): `agents/qa-automator.md` one line; the driver's window `auto_extra` one line (TR3-6 adds it). The critic's file: a test in a new file beside a file of another window was forced by ownership, not chosen; consolidation may be named as a note, no finding on that ground.
Liveness: a claim holds until `release`. Restart: the scheduler at entry releases claims whose window is closed by `s5_open_windows`. Exit in `state-exits.md`.
Error direction: the guard may refuse needlessly, because a new file is always possible; it must never let two live windows write one test file through Write/Edit. Adversarial inputs: path with `..`, backslashes, mixed case on Windows (normalised project-relative, casefold on Windows, by an existing normaliser the builder names in its report); a path outside the project (return); a claim file empty after a crash mid-write (unknown owner: refuse with the same door, plus a note; `release` clears it); two sessions racing (O_EXCL: one wins); Write to a brand-new file nobody claimed (claims it, passes); the critic's probe (not a Write: launch gate, TR3-6); a NotebookEdit (same branch).
Known gap, named: a role writing a test file through Bash (`sed -i`, `python`) is not seen. Guard's Bash branch cannot judge it (AR-2); the launch gate and N-LIVE's check of the manifest for two windows on one file are the net. Detector: N-LIVE's overlap measure; the home of a calibration check is the Lead's decision at acceptance.
Temporal: before TR3-6, no `named()` window is ever beside another, and a single window claims everything it writes, passes. No claim is released: nothing reads them. Own-window return makes that harmless.
tests: `write_to_other_running_window_file_refused_with_door`, `own_file_allowed`, `rework_of_same_window_allowed`, `new_file_in_same_directory_allowed` (the door opens, FR-2), `no_name_no_check`, `critic_role_no_claim`, `support_file_not_claimed`, `race_one_wins`, `released_claim_free`, `empty_claim_refused_with_door`, `path_spellings_same_claim`, `arm_b_overlap_shape_second_goes_to_new_file`.
witness: `python -B S/tests/test_guard_window_files.py`; `python -B S/tests/test_guard_write_owners.py`; `python -B S/tests/test_hooks_wiring.py`.
Answers: B2. `file_overlap_waits` of the first draft is replaced by this node's and TR3-6's keys. Census class safety, as table in section 1.

### TR3-17 (N-P1-4a) — chain record, no behaviour change (B4 parts 1-2)
tier: builder; critic with TR3-6's pass.
owns: `S\story_run.py` (`boundary`, `last_dispatch` properties; `as_chain`, `adopt_chain`, `ChainStream`, `Refusal` field `chain`; `s5_review.closes`, `route_of`'s callers in it; `s5_author_round` untouched), `S\tests\test_driver_chain.py` (new).
Do: `boundary` and `last_dispatch` thread-local properties over the same names (no edits at 26 + 57 call sites; `getattr(self, "last_dispatch", "")` must keep answering ""). Main thread default stays. `as_chain(record)`/`adopt_chain(record)`. `closes` passes the dispatch to `route_of` and `repair_answer`. `Refusal` raised in a chain carries its record. `ChainStream`: writes through with `[W<n>] ` at line start for a chain thread and nothing for main; thread-safe; flushes (FR-43); not installed in this node.
edges: invariant: on the serial road every value and every byte printed is as today (`serial_values_unchanged`). `self.boundary` read on a fresh thread: the initialiser sets it at chain start; before that `AttributeError` is a bug to show, the property has no silent default except `last_dispatch`'s "". `redirect_stdout` inside a chain replaces `sys.stdout` for all: on the new road `defer_question` runs under `_book` and prints through it; the watchdog bypasses (P2-4). `pickle`/`state` never hold a record: thread objects are not saved.
tests: `thread_local_values_isolated`, `main_keeps_its_own_values`, `as_chain_restores`, `adopt_chain_stays`, `closes_reads_given_dispatch`, `refusal_retry_reads_its_own_chain`, `chain_stream_prefixes_only_chain_lines`, `serial_values_unchanged`.
witness: `python -B S/tests/test_driver_chain.py` (uses `Driver.__new__`, no subprocess); `test_story_run_*` in CI.
Answers: B4 parts 1, 2; M2 (leak of single-slot values, part).

### TR3-6 (N-P1-4b) — scheduler, lock, close, serial reason, seam (B2 source, B3, B4 part 3, B6, M1-M4)
tier: builder; critic mandatory (over 100 lines, core); ONE critic pass with TR3-17 and TR3-18.
owns: `S\story_run.py` (`run_chains` new, `stage_S5`, `s5_window`, `s5_review`, `s5_mechanical_round`, `completion_for` S5 branch, `s5_open_windows` new, `s5_serial_reason` new, `launch`, `unbooked` new, `run_claude` retry backoff, `run_role` + `rework` drain check and flag, `finish` `--open-windows`, `progress_line`, session fallback sites :3235/:16075), `S\exit_gate.py` (`_mutate_state` wait), `PKG\references\state-exits.md`, `S\tests\test_driver_chain.py`, `S\tests\test_story_run_s5_parallel.py` (new, CI), `S\tests\story_run_common.py` (STUB barrier + log).
Do: 3.2 and 3.6 as written. Inputs named: `config_contract.parallel_windows` through the Driver's config; note printed once.
edges (each with its invariant, beyond 3.2):
- N=1: `stage_S5` returns through today's body, verbatim. Invariant: no thread (`no_thread_started_at_n1`).
- Entry with owed or pending: today's body runs them, then the stage re-enters. Invariant: t-729, t-733 hold.
- A window with `qa-automator` already in `accepted_by`: its chain starts at the critic, as today.
- `Drained` is not an error: a chain ending so has `exception = None` and an open window; no seam.
- All chains drained and no exception (max_boundaries): `stage_S5` returns; the main loop reads on.
- Refusal selection: a `ReworkRefused` keeps the t-760 take-back of `owed["executed"]` inside its chain.
- A chain's `stand_check` Person: state unchanged, re-arises: `stand_person_in_chain_re_arises`.
- `save_state` under `_book` only. `story_step` readers of the driver state during a released `start`: the builder greps and reports; a reader needing a stable file gets it if `save_state` writes atomically; if not, atomic here.
- Launch gate reads `window_files.files_of` + manifest rows. An unreadable manifest: empty set plus claims; the guard still stands.
- `s5_open_windows` raising: caller treats as open: `closes` False and `--open-windows` with the raw window list; if even that cannot be read: `complete=False`, the controller refuses, the seam gets it. Never a close (FR-59).
- `completion_for`: `mine == scope` skip keeps; other windows through `s5_open_windows`.
- `release(window)` at a window's close under `_book`; a release that fails: a note; the entry sweep retries.
- Restart sweep: serial reason, then `release` of closed windows.
- Stand wait: `stand_busy` in a role's run is the role's fact: the brief line says "stand busy after N min is not your failure; say so in your digest" and no chain treats exit 3 specially (key `stand_busy_is_not_a_window_failure`). What a role does with it is the role's.
- Flag: on a chain thread every `start` and `rework` carries `--parallel-window`.
- Session: a chain's resume reads `sessions[dispatch]` only; absent: no resume, a fresh attempt by today's rule.
tests in `test_driver_chain.py` (fast; fake `step`, fake `launch`): `critic_start_does_not_hold_book`, `settling_one_at_a_time`, `unbooked_releases_once_and_retakes_on_exception`, `conductor_launch_holds_book`, `backoff_sleep_releases`, `open_windows_each_reason`, `open_windows_unreadable_is_open`, `serial_reason_each_row`, `serial_reason_printed_once`, `seam_order_infra_refusal_person`, `drain_registers_no_dispatch`, `launch_gate_waits_then_progresses`.
tests in `test_story_run_s5_parallel.py` (CI): `n3_three_automators_overlap`, `no_thread_started_at_n1`, `crash_in_one_window_others_finish`, `person_in_one_window_drains_then_asks_once`, `queued_question_asked_next`, `round_in_w1_blocks_close_by_w2`, `mechanical_last_with_other_chain_open`, `exactly_one_close_order_free`, `stage_closes_only_after_last_window`, `config_absent_reads_three`, `config_invalid_reads_three_with_note`, `refusal_retry_on_main_reads_chain`, `stand_person_in_chain_re_arises`, `driver_interrupt_kills_children`, `critic_probe_waits_for_file_holder`, `stand_busy_is_not_a_window_failure`, `ticket_rework_owed_after_drain`.
witness: `python -B S/tests/test_driver_chain.py`; report line "тронут story_run_common.py"; CI files by name.
Temporal: the commit landing this is the one where the default takes effect. A story mid-S5: 3.6.
Answers: B2 (source: claims + manifest), B3 (predicate, three callers, owed/debt), B4 part 3, B6 (serial function), M1, M2, M3, M4, M5 (barrier), S-5 note, scout's settle hazard, `_mutate_state`, t-2034 q.3.

### TR3-18 (N-P1-4c) — equivalence suite at the default (B6)
tier: builder; critic with TR3-6's pass.
owns: `S\tests\test_story_run_s5_equivalence.py` (new, CI), `S\tests\fixtures\s5_arm_b_overlap.json`, `S\tests\fixtures\s5_arm_a_no_overlap.json` (shapes, no project names beyond test paths), `S\tests\test_story_run_s5_n1_frozen.py` (new, CI), `S\slow_tests.json` (rows).
Do: 3.5. The frozen N=1 list is captured from the tree BEFORE TR3-6 lands (on the commit under it) and committed as a fixture. No builder runs these locally: it pushes and reads the pipeline once (`docs/RUNBOOK.md` §7), one wait cap per round.
edges: a seam the stub cannot drive: named in the report, never silently dropped; goes to N-LIVE's list. Order-free compare means sorted by window; question order is compared as a set per driver turn, one per turn. Invariant: every outcome that differs between N=1 and N=3 is a defect, named or justified row by row in the verdict.
tests: `equivalence_outcomes_n1_vs_default`, `seam_repair_limit`, `seam_debt`, `seam_owed_round`, `seam_mechanical_round`, `seam_halt`, `seam_question_threshold`, `seam_infra_cut_resume`, `seam_conductor_refusal`, `seam_driver_killed`, `seam_until`, `overlap_shape_all_windows_close`, `no_overlap_shape_all_windows_close`, `n1_frozen_calls`, `n1_frozen_events`, `n1_frozen_state_keys`, `n1_frozen_console`.
witness: the CI pipeline's lines for the two files, verbatim; locally only a syntax run `python -B -m py_compile`.
Answers: B6, t-2034 q.5.

### N-P2-1 (TR3-2), N-P2-3, N-LIVE
TR3-2: section 2, batch row completed with `story_step.py`, `stages.json`, `artifact-writers.json`. Witness `python -B S/tests/test_driver_timing.py`; `test_story_run_wait.py` in CI. N-LIVE: MyBooks S5 at the default: `driver_timing.py`, S5 wall against 4:13, overlap measure for pairs on one file, settle time, stand wait, reds on helper files.

## 7. Sequence (t-2034 q.1: t-1936 is merged, so the old section's conditions are void)

TR3-1 done -> TR3-3, TR3-12 -> TR3-13 -> {TR3-14, TR3-5, TR3-16} -> TR3-15 (after TR3-5, TR3-11). TR3-4 beside them (needs TR3-3). TR3-2 -> TR3-17. All -> TR3-6 -> TR3-18 -> TR3-9, N-LIVE. Critic: one pass per topic: identity (TR3-13, TR3-14); controller (TR3-4); artifacts (TR3-5, TR3-15); guard (TR3-16); driver (TR3-17, TR3-6, TR3-18). Walker slice 1 (`after`, `walk_reopen`, `s7_settle_session` in `run_role`) is in the tree; TR3-17 and TR3-6 rebase over it.

## 8. Effect estimate (arm B numbers; estimates, not verified)

P2-2: settle 11:10 -> ~0-1 min. P2-3: other ~70 s/hop x 21 hops -> target < 20 s/hop. P1 at N=3 (shipped default): "2:00-2:20" assumes bookkeeping overlap; 37:25 of hops stay serial under the lock until P2 lands, critic settles now leave the lock, and arm-B-style overlap under the guard is unmeasured. Keep it labelled estimate; N-LIVE decides. N >= 7: ~1:30-1:50. Together on B: 7:23 -> ~4:15-4:45. "About one hour" for a whole story is not reachable by P1+P2 alone (the longest window, serialized stand, S1-S4 loops): reported, scope not widened.

## 9. Where each finding landed

| finding | landed |
|---|---|
| B1 identity | `dispatch_identity` + exit readers TR3-13; hook readers TR3-14; admission marker + `_resume_problems` TR3-4; full census 3.1 |
| B2 no plan on the driver road | F3 (b): claims + guard TR3-16; launch gate from claims + manifest TR3-6; both arm shapes TR3-16, TR3-18 |
| B3 close predicate | `s5_open_windows`, three callers, owed/debt first TR3-6; `open_windows`, backstop TR3-4 |
| B4 thread values, seam, loop | record, `as_chain`, `adopt_chain`, explicit `closes`, chain init TR3-17; seam on main, per-turn steps TR3-6, F12 |
| B5 settle under parallel | `running_window` TR3-15 |
| B6 default | serial function 3.6 + TR3-6; equivalence and frozen N=1 TR3-18; `seed` pin TR3-12 |
| M1 lock release | 3.2, TR3-6, keys `unbooked_releases_once_and_retakes_on_exception`, `driver_interrupt_kills_children` |
| M2 conductor, single slots, sleep, watchdog | no release on empty dispatch, seam after drain, backoff release TR3-6; thread-locals TR3-17; watchdog TR3-2 |
| M3 queue | no `pending_questions`; re-raise is the queue 3.2, TR3-6, key `queued_question_asked_next` |
| M4 standing | one seam per turn through `guarded`, chains never call it, TR3-6 |
| M5 determinism | barrier stub TR3-6 (`story_run_common`) |
| M6 stale claims | manifest wait 3.3; t-1936 section 7; wt-fbfix `PKG`; batch rows: section 6 "Order" tells the Lead to rewrite them |
| t-2034 q.4 item 1 judge-code | TR3-15 |
| item 2 support files | F10, 3.3, TR3-16 |
| item 3 one `events.lock` | 3.3 (scout: CLI waits 10 s), TR3-14 |
| item 4 `log_append` immediate fail | NOT closed: the scout's rows do not list it, and this designer did not read it. Falls to TR3-14's builder: one read; if a role session calls it: bounded wait in that node, else a line in the report |
| item 5 findings readers | TR3-5 |
| item 6 memory, own word | TR3-15 |
| q.5 parity | TR3-18, 3.5 |
| Node lines | N-P2-1 section 2; N-P2-2 done; the rest section 6 |
| Standing Q AR, JUDGMENT, class | section 1; TR3-16 stays safety on a write; axis 5 3.7 |
| Scout S-1..S-17 | 3.1 row by row |
| Scout 2a, 2b, 2c | 3.3 |
| Scout last hazard: settle under the lock | 3.2 "Critic `start` outside the lock", TR3-6 keys |

## 10. Reading trail

This revision read: t-2034 review (all); first draft (all, in ranges: the guard refuses a whole read over 30 KB); scout report (all; absent at first look, present by the coordinator's message); batch file (all); t-2043 report (all). Carriers, wt-fbfix: `story_run.py` :1845-1884, :2356-2370, :2856-2906, :2987-3075, :10404-10432, :11164-11403, :15763-15776, :16368-16397, :16476-16535; `controller.py` :235, :1525-1572, :3875-3904, :4034-4047, :4955-5014, :5316-5337, :5742-5761, :6786-6827, :7125-7136, :7226-7237; `s5_precheck.py` :4220-4289; `branch_accounting.py` :1928-2009; `exit_gate.py` :450-507, :968-989; `stage_guard.py` :160-190, :1355-1380, :1560-1573, :2598-2625, :2650-2697, :2790-2803; `guard_pre_tool.py` :608-621, :1005-1039, :1155-1165, :1338-1395, :1436-1463; `planning_contract.py` :348-378; `story_step.py` :495-524, :880-905, :1995-2044; `handoff_check.py` :158-170; `repo_map.py` :231-257; `window_budget.py` :300-327; `validate_artifacts.py` :1908-1927; `stage_done.py` :1080-1093, :1176-1199; `conductor_stop.py` :30-47; `session_handoff.py` :26-39; `story_progress.py` :516-531; `execution_request.py` :846-885, :1950-1958; `run_suite.py` :1296-1305; `probe_debt.py` :440-451; `artifact-writers.json` :98-111; `stages.json` S5; `slow_tests.json` head + rows; `hooks.json` matchers; `architecture.md` change checks; `factory-rules.md` FR-2, FR-39, FR-45; `builder-rules.md` 7b. wt-tr3-3: `config_contract.parallel_windows`, template, keys, test. wt-tr3-11: `probe_debt.py` memory symbols by grep. `t-1957` by grep.
Greps with control: status pattern over `S\*.py`: 82 hits, 32 files, control `controller.py:4965`; `QA_FACTORY_DRIVER_RUN` case-insensitive: setter, `driver.md`, test only; `parallel_windows` over wt-fbfix: none, with the same grep finding it in wt-tr3-3; `additionalProperties` in `record-schemas.json`: none, control `"Dispatch"` :174; `_memory_doc` in wt-fbfix: none, same grep found it in wt-tr3-11.
Not read: `exit_gate._mutate_state`, `log_append.py`, `controller._closed_dispatch_refusal` bodies, `_s5_completion_problems`, the six per-turn steps' inputs, the interview topic file, `InfraStop` kinds, the last-window own-round road through `story_step finish`. Each is named on a node above as the builder's first read.
Noticed in the brief's sources, not widened: the batch's row TR3-3 and the finding's line 25 say default 1; t-1957 lines 205, 932 name `S5Scheduler` and an RLock.
Unrun: any test (no shell in this role; CI rule). Critic and scout line numbers differ in places from this tree's reading (e.g. `exit_gate._live_dispatch`): functions are the address.
