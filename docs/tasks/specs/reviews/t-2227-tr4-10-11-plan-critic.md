# t-2227 — critic on plan: spec t-2222 (TR4-10, TR4-11, S5 window leftovers)

Reviewed: `docs/tasks/specs/t-2222-tr4-10-11-s5-windows-leftovers.md` (commit 072f25047), against the batch rows TR4-10/TR4-11
(`plans/piles/thinking-roles/batch-4-ostatki.md:31-32`), the Lead decisions (`docs/tasks/handoffs/20261110-lead-window-acceptance.md` §3),
the critic queue it answers (`docs/tasks/specs/reviews/t-2121-critic-tr3-6.md` Q1-Q5) and the code it names. `S` = `ai-packages/qa-factory/scripts`.
The files the spec edits are byte-equal in `wt-fbfix` HEAD and `origin/experiment/thinking-roles` (`git diff --stat HEAD origin/...` over
those paths: empty), so the spec's line numbers hold on the branch the builders cut from.

verdict: ACCEPT-WITH-FIXES (NEEDS WORK: 2 blocking spec fixes, both in part A1, to be made before A1 is dispatched; A2, B1, B2 may be
dispatched now with the non-blocking fixes folded into their text)

## 0. Facts of the spec checked by trail

| spec claim | result |
|---|---|
| `finish` :3217-3219 calls `s5_release_of_dispatch` after the accepted finish of the closing role | VERIFIED (`story_run.py:3214-3219`) |
| `s5_release_of_dispatch` :11611-11626, docstring "Q1" | VERIFIED |
| `closing_finish_releases_the_window` at `test_driver_chain.py:940` | VERIFIED (:940, called :1067) |
| "the author's mechanical round ... finished on a recovery road ... `complete=last()`" (the gap F1 (b) closes) | WRONG: every recovery road computes `complete` through `completion_for` (`story_run.py:12026, 16571, 16597, 16634, 16659, 16710, 16736, 16761, 16834`), and `completion_for("S5", <not the critic>)` returns `False` (:17000-17001). An author's finish closes S5 only on the LIVE mechanical round (`s5_mechanical_round` :11961, `complete=lambda: bool(last())`). See finding B-2 for the real gap |
| `session_gate` :291, `count_launch` :257, `stop_if_drained` :252, `run_chains` :324, `_interrupt_chains` :403 in `driver_chains.py` | VERIFIED (grep `def` of `driver_chains.py`) |
| no `except KeyboardInterrupt` in `story_run.py`; `driver_chains.py:218` hit | VERIFIED (`KeyboardInterrupt` grep: only `driver_chains.py:218, 373, 391`) |
| Ctrl-C reaches `Driver.run` on both roads | PARTLY: true for an interrupt raised inside the `try` body (:17070-17201). NOT true for one raised inside the run-level handlers (`except Refusal` -> `funnel` -> `no_move` with a words file = a paid conductor call, :17213-17220, :17844-17855). See fix F-3 |
| serial road: `_launch` kills (:1947-1949), `clear_in_flight` in `finally` (:1954) | VERIFIED |
| `launched` row at `run_claude` :2074 | NEARLY: the row is written at :2062-2066; :2077 is its `except OSError` |
| `collect_stall.py:214-239` K3 | VERIFIED (:214-240) |
| one direct appender `_append_jsonl` :581-584; callers :1569, :1572, :4526, :5598, :7443 | VERIFIED (grep `open("a"`/`O_APPEND`/`_append_jsonl(`: one appender, five callers) |
| `s5_auto_extra` :11657-11673 gives the ownership line only with `chain=True`; old body :11803 calls with `chain=False` | VERIFIED |
| guard enforces claims when `parallel_windows(cfg)[0] != 1` (`guard_pre_tool.py:1588-1589`) | VERIFIED |
| `s5_open_windows` :11522-11556 has no `returned` clause; `controller.RETURNED` at `controller.py:157` | VERIFIED |
| Q2 "N == 1: the serial `completion_for` reads the same function, so the gap closes there too" | WRONG: at N == 1 `completion_for` takes the `else` loop over `accepted_by` (:17015-17020) and never calls `s5_open_windows`; nor does the old body (`last = len(todo) == 1`, :11799). See finding B-1 |
| `state-exits.md:23` is the S5-running-beside-a-window row | VERIFIED |
| census `BLIND_SPOT` (:446-447), totals print (:496-497), docstring paragraph (:32-34), `about` on line 3 | VERIFIED |
| N2 comment at `s5_precheck.py:4265` | VERIFIED |
| N1 changelog sentence | VERIFIED as text; the arithmetic "31.2 s = three tries" NOT verified by me (taken from t-2095) |
| TR3-9 C overlap (the designer could not run git) | RUN by me, see §4 |

## 1. Blocking findings (part A1 only)

### B-1 (item 10.2, Q2) — the returned clause reaches one of three close predicates, and the window it holds open has no way out

Surface: the S5 close predicate. It has three implementations today:
(i) `s5_open_windows` — read by the chain road (`s5_last_fn` :11558) and by `completion_for` at N != 1 (:17011);
(ii) the old body's `last = len(todo) == 1` (`stage_S5` :11799) — taken at N == 1, AND at N != 1 whenever one window is left in `todo`;
(iii) the N == 1 loop of `completion_for` (:17015-17020).
The spec adds the clause to (i) only.

Failing scenario (the critic's own counter-scenario, two windows, N = 3): W1's critic accepted with route `mechanical`, W1's mechanical
round is `returned_unaccepted` (the driver died before its finish). On re-entry `todo` is computed by `accepted_by` (:11748), so W1 is NOT
in `todo`; `todo = [W2]`, `len(todo) < 2`, so `stage_S5` takes the old body, `last = True` (:11799), and W2's critic closes S5 over W1's
returned round. The two-window case — the commonest — never reaches `s5_last_fn`; the spec's test key
`returned_mechanical_round_keeps_window_open` "through `s5_last_fn` of the other window" passes while the scenario stays open.
Will the controller settle W1's return first? Not reliably: `next` hides a returned dispatch behind ANY later dispatch of the same
stage that holds a move (`controller.py:8544-8556`, `superseded_by_later_work` compares `stage` only, it does not look at windows), so a
later W2 dispatch hides W1's return and no `resolve_return` is offered.

The same hiding also leaves the fixed predicate (i) without a way out (AR-25): once W1 counts as open, W2's finish is `--not-complete`.
On the next entry `todo == []` and nothing is owed, so `stage_S5` raises "every window is accepted ... run `controller.py --operation
recover`" (:11756-11759), and nothing in the driver resolves W1's return. The spec's "error direction" names the cost as "the seam's
stuck question". In fact it is a Refusal with no designed move, which goes to the conductor and then to a person.

Required in the spec before A1:
(a) Say which predicates Q2 reaches. At N != 1 the old body's `last` has to read the same rule. The smallest edit is
`last = not self.s5_open_windows(excluding=cases)`, guarded and unreadable-is-open, only when `s5_parallel_cap() != 1`. Without it,
item 10.2 does not meet the Lead's decision on the two-window case.
(b) Correct the N == 1 sentence. At N == 1 nothing changes, because predicate (iii) is the frozen old road (Lead §3, "a promise of the
old road"). Name this as a residual of Q2 at N == 1, with the critic's words "not a regression". Whether to close it at N == 1 is a
Lead call, not the owner's. It would move the frozen set.
(c) Name the way out for "a window held open by a returned last round". Recommendation: `stage_S5` treats such a window as owing its
round, the same as `repair_owed`, and resolves the return through the existing `_act_resolve_return` / `resume_role` road. The other
option is to point to a command the conductor already has (`reconcile_dispatch` / `release`) and say so in a `state-exits.md` row.
Either is a Lead choice. A spec that only declares "open" swaps a silent close (worse) for a dead end (still a defect, AR-25).

### B-2 (item 10.1, Q1) — the "never free a window that can still write" condition misses two statuses, and its stated premise is wrong

Surface: the release-on-complete predicate. Item 10.1 frees every S5 claim when `stages.S5.status == "completed"` and no S5 dispatch is
`running`, `blocked` or `paused`. Two statuses that can still write are missing:
- `incomplete` (`controller.STOPPED = {"blocked", "paused", "incomplete"}`, `controller.py:165`). A retry inherits its checkpoint and
  writes in the same window.
- `returned_unaccepted` (`controller.RETURNED`). `resolve_return` resumes the SAME role with the person's words (`_act_resolve_return`,
  `story_run.py:16815-16836`), and that role writes again. A completed S5 beside a returned rework can happen (state-exits row 37: a
  rework does not lower the stage).
Freeing claims beside either one breaks the spec's own INVARIANT and its error direction ("releasing early is not safe").
Fix: read the sets from the controller, `{"running"} | controller.STOPPED | controller.SETTLED` (or at least `| {controller.RETURNED}`),
never a literal list (AR-13). Add one adversarial key per added status.

Premise: the F1 text and the §0 bullet justify the sweep with "an author's finish on a recovery road". That road cannot complete S5
(see §0). The real gap the sweep closes is this. A recovery process finishes window B's saved critic `--not-complete`: other windows
are open, so `complete is not True` and the :3217 release does not fire. In the SAME process it then finishes the last window A's
critic `--complete`. `s5_release_of_dispatch` frees A only. S5 is completed and never entered again, so `s5_release_closed` never runs,
and B's claims stay. A second case is the live mechanical round when something raises between its finish and `s5_window` returning.
The sweep in item 10.1 is still right (F1 (b)). The spec has to state the right scenario, and its first test key has to build it:
`stage_completed_by_author_finish_frees_every_s5_claim` describes a road that does not exist on recovery. Replace it with
`recovery_finishes_free_sibling_claims` (two saved critic results, one process). Keep the author case on the LIVE mechanical round.
Also add the batch row's literal test: S5 closed by the person's `debt` at the gate, then a rework's automator is not refused
(`batch-4-ostatki.md:31`, item (1)).

## 2. The five forks (question 1)

| fork | recommendation | my answer |
|---|---|---|
| F1 Q1 scope | (b) | RIGHT, with B-2 (correct premise, full status set). Technical, no owner question |
| F2 where the stop record lives | (a) a `driver-runs.jsonl` row through `journal_run` | RIGHT: append-only history, K3 already reads that file, one writer (AR-14); `driver-state.json` is a snapshot that `save_state` rewrites, and it is K1's carrier. Technical |
| F3 which `launched` rows a stop record clears | (a) the time window `since <= started_at`, rows before the record | ACCEPTABLE ONLY WITH F-1 below (question 2). Technical |
| F4 Q3 vs "the one that counted still runs" | (a) exempt the counting chain | RIGHT: it keeps the `count_launch` contract (`driver_chains.py:257-263`). Without the exemption, `--max-boundaries` pauses earlier than the person asked and leaves the counting chain's dispatch registered with no session. Technical |
| F5 "last dispatch" | (a) order of the controller mapping | RIGHT: it is the controller's own order rule for "later work" (`controller.py:8544-8550` walks `entries[index + 1:]`), and `dispatch_identity.records` keeps dict order (`dispatch_identity.py:36-49`). (b) has the same "never settled" risk and less precision. Technical |

Nothing in the five forks needs the owner. The Lead owns the Q2-at-N == 1 residual (B-1 (b)) and the way-out choice (B-1 (c)).

## 3. Question 2 — the F3 residual (two driver processes on one story)

Critic rule 15 applies. K3 clearing is a pair detector (a stop record AND a `launched` row), and F3 (a) scopes the pair by a time window,
not by carrier. Process B's record clears process A's row when A launched after B started and then died. Its direction is the unsafe
one: `collect_stall`'s stated error direction is "an extra transcript is the safe side, a missing one is not" (`collect_stall.py`
docstring), so a cleared K3 means a missing transcript.
I found no single-instance lock for a driver on a story. I grepped `story_run.py` for `lock`, `O_EXCL`, `pid_file` and "already
running"; the hits are not a driver lock. This is an estimate, not a proof that two drivers cannot run.
So the residual is a real cross-match, rare as it is. Two drivers on one story also share `driver-state.json`, which breaks more than K3.

Answer: do not take F3 (b) as specced (it touches `run_claude`). Take the cut list from the writer that already sees every row. That is
`journal_run` (`story_run.py:1568-1569`, the one writer of `driver-runs.jsonl`): it keeps an in-process set of open calls, adding
`(key, started_at)` on `kind == "launched"` and removing it on the outcome row of the same key. `person_stop_record` then writes
`cut: [...]`, and K3 clears exactly those rows. Cost: one function more in B1's owns (`journal_run`), no `run_claude` edit, and
`append_jsonl_line` already locks across threads. If the Lead keeps F3 (a), the residual is acceptable as a NAMED gap only if it is
written into the K3 line of the `collect_stall` docstring (FR-41: the next reader meets it), not only in the spec. This is fix F-1.

## 4. Question 4 — function-level owns, disjointness, merge order

Ran: `git -C D:/ws1/wt-tr3-9c0 diff --stat origin/experiment/thinking-roles...tr/tr3-9c-int` gives 21 files, +1687/-33. In the
package: `story_run.py` (+240), `driver-layers.json`, `judgment-census.json` (3 lines), `state-exits.md` (+1), `walk_session.py`,
`validate_artifacts.py`, `slow_tests.json`, `story_run_common.py`, the S6 fixtures and tests. NOT touched: `driver_chains.py`,
`collect_stall.py`, `window_files.py`, `s5_precheck.py`, `test_judgment_census.py`, `test_driver_chain.py`, `test_collect_stall.py`.
`story_run.py` hunk headers (`diff -U0 | grep ^@@` plus the enclosing `def` at the merge base c28123d23): `walk_before` (:3504) and the
S6 lane block (:13398-13698: `run_manual_block`, `manual_lane_plan`, `s6_walkers_cap`, `s6_serial_reason`, `s6_settling_lanes`,
`s6_lane_holds`, `s6_chain_kind`, `s6_open_lanes`, `s6_seam`, `run_s6_lanes`, `run_manual_lane`).

| pair | functions | files |
|---|---|---|
| A1 vs C | disjoint (`s5_open_windows`, `s5_auto_extra`, `finish`, new `s5_release_completed`; none in C's hunks) | `driver-layers.json` rows (C changed 15 lines): a row conflict is possible, resolved by the later merge |
| B1 vs C | disjoint (`run`, `_append_jsonl`, new `person_stop_record`) | `driver-layers.json` as above |
| A2 vs C | `driver_chains.py` not in C's diff: disjoint | `state-exits.md`: C's row is at line 50 (after the chain-registry row), A2's goes after line 23. NOT adjacent, so no conflict (the spec's "near row 26, adjacent-line conflict possible" is over-cautious) |
| B2 vs C | none | `judgment-census.json`: C changes line 4 (`ratchet`), B2 changes line 3 (`about`). The lines ARE adjacent, so git WILL conflict (the spec says "non-adjacent"). Merge B2 after C and resolve by hand: keep C's ratchet and B2's about. Fix F-4 |
| A1 vs B1 | disjoint function lists, far apart (:3219, :11626 vs :581, :17066) | both add a new Driver method and a `driver-layers.json` row. Name the insertion anchors so the two new methods do not land at the same place: A1 right after `s5_release_of_dispatch`, B1 right after `run`. Fix F-5 |
| A1 vs A2 | A2 has no `story_run.py` edits; A1 only RUNS `test_driver_chain.py`, A2 owns its keys | none |

Merge order A1 before B1: it holds, though nothing forces it. The shared files are `story_run.py` (disjoint functions) and
`driver-layers.json` (rows), so either order works if the later one merges and keeps both pins green. A2 after C1: not needed on
`state-exits.md` (not adjacent). B2 after C: needed (adjacent lines in the census file).

## 5. Question 3 — feasibility and edge completeness per part (rule 11)

**A1 (10.1, 10.2, 10.4).** Feasible: `test_driver_chain.py` already has a Driver rig with controller state, and `window_files` is
standard-library only. Edges:
- 10.1: B-2 (statuses). Positional: "inside `if complete is True`" can be read as the pre-finish block at :3150, which runs BEFORE
  `story_step finish`. The invariant to state: the sweep runs only after `story_step finish` exited 0, i.e. in or after the post-finish
  block at :3214-3219, so the stage it reads is the stage this finish wrote (fix F-6).
  Duplication: `window_files.release_stage` must reuse `release`'s loop and its empty-claim rule (one predicate parameter), not copy it
  (AR-15, see §7).
  Limits, empty input and N == 1 are named. A claim file of another stage (`S6|...`): S6 claims nothing today, and the `S5|` prefix
  covers it.
- 10.2: B-1 (predicates, way out). The adversarial list is good. Add one edge: a returned record whose `scope` meets the window AND a
  later `released_by_person` record. `DISCOUNTED` drops the second, so the returned one is last and the window is open, which is right.
  Pin it: it is the person's door.
- 10.4: the Lead's decision ("given whenever the guard enforces, on either body") is followed. But the line's first sentence, "Other
  windows of this story are written at the same time", is FALSE on the serial old body, where at most one window runs. The door
  sentence is what the role needs. Recommendation: on `chain=False` give a variant, "A test file another window of this story wrote
  first refuses your Write or Edit: put your test in a new file in the same directory; ...", and keep the chain text byte-equal
  (fix F-7, a text choice; the Lead decides). "byte for byte" then holds only for `chain=True`.

**A2 (10.3, 10.5).** Feasible: the gate loop is short, and `test_driver_chain.py` has fake `_launch` chains. Edges:
- TEMPORAL: Q3 creates a NEW state. Today `stop_if_drained` sits BEFORE registration (`story_run.py:3009-3010`, `:10679-10680`), so a
  registered dispatch that never launched cannot come out of the drain. After Q3, a chain drained at the gate leaves a `running`
  dispatch with a `launched` row and no process. The spec defers its re-entry road to a builder report line. The road should be in the
  spec before the code, because if it is a Refusal to the conductor (a paid call), Q3 costs more than it saves. My reading: `next` gives
  `wait_existing_job`, the liveness verdict is `never_started`/`abandoned`, and the `KNOWN_REFUSALS` row `dead_dispatch` (`story_run.py:217`)
  maps that to `recover`, a code move. This is an estimate, not traced to the end. The spec should cite it and give the state a
  `state-exits.md` row or a pointer to the row it shares (fix F-2).
- POSITIONAL: the gate is in `launch` (:1900-1904), so it runs on EVERY attempt of `run_claude`'s loop (transient retry, a resume of the
  same dispatch's session) and in `resume_role` (:3431), not only at a dispatch's first launch. A chain whose earlier attempt ran, and
  which then waits at a retry, would be drained mid-dispatch with a usable session behind it. State whether the drain test applies
  only before a dispatch's first process (recommended: track "this dispatch has launched once" on the record) or to every attempt, and
  pin it (fix F-2).
- F4 exemption: `_drain_by` keyed by chain number covers the counting chain's own retries, which is right. The chain's next `run_role`
  stops at `stop_if_drained` before registering, so the exemption never reaches a second dispatch. Good.
- 10.5: feasible. The row's way-out text "`stage_S5` re-enters on `pending` and reads the stopped dispatch as an entry-state reason
  (`S5_SETTLE_RUNNING`)" is doubtful as the FIRST move. `next` offers `resume_checkpoint` from the controller's stopped list before a
  stage is prepared (`controller.py`, the `stopped` branch after :8570). The row should name `next` -> `resume_checkpoint` first. I did not
  trace this to the end; the builder confirms it in one report line.

**B1 (11.1, 11.2).** Feasible. Edges:
- Ctrl-C inside the run-level handlers (fix F-3). An interrupt raised in `except Refusal` -> `funnel` -> `no_move(words_file)` (a paid
  conductor call with its own `launched` row) is not caught by a sibling `except KeyboardInterrupt` on the same `try`. Wrap the whole
  body in an outer `try/except KeyboardInterrupt` inside `run` (still B1's owns), and add a test key
  `ctrl_c_in_run_level_handler_writes_one_stop_record`.
- The record row passes by the readers: there are 11 reader modules of `driver-runs.jsonl` besides `story_run.py` (`collect_stall`,
  `dispatch_liveness`, `driver_journal`, `driver_timing`, `factory_dashboard`, `friction`, `infra_failure`, `retro_numbers`, `story_budget`,
  `story_progress`, `walk_timing`; grep `-il driver-runs`). The spec leaves the walk to the builder; list them in the spec (freshness,
  rule 11 point 5) so the AR-22 line is checkable. The `launched` row is the precedent: no `dispatch`, `session_id`, cost, `exit_code`.
  Name in the K3 docstring that `driver_journal.py` calls itself "the one reader of the driver's journal" while `collect_stall` reads
  the file itself. That is pre-existing (AR-13 debt, not this spec's), but the new K3 clause deepens it; queue it, do not widen.
- 11.2 encoding: `_append_jsonl` today writes in text mode, so on Windows a row ends `\r\n`. `append_jsonl_line` writes `O_BINARY` `\n`
  (`hooklib.py:484`). After the change a journal on Windows holds mixed line ends. The readers tolerate it: JSON whitespace takes `\r`,
  and `_read_jsonl` uses `splitlines()`. Name the edge and pin one mixed-file read in `test_driver_stop_record.py` (fix F-8).
  `ensure_ascii=False` never emits a raw `\n`, so the `ValueError` cannot fire. Confirmed.
- Ctrl-C before `run`, in `__init__` or argparse (`main` :19594-19603): no record, and no call was launched. Correct as named.

**B2 (11.3, 11.4).** Feasible: text only, and the census totals do not move. The edge is the adjacent-line merge with C (F-4).

## 6. Question 5 — AR-29 census class of every new check

| new or changed check | owner | class | judges a role's judgment? |
|---|---|---|---|
| Q2 returned clause in `s5_open_windows` | data | xref (dispatch status x window scope); not a census unit (it raises `WindowsUnreadable`, the Q7 blind spot). Consistent with C1's twin `s6_open_lanes`, which IS a row `xref / data` (C's census hunk at line 798) | no |
| Q1 `s5_release_completed` | data | xref (stage status x dispatch statuses); no refusal site | no |
| Q3 drain test in `session_gate` | data | shape (a flag); `Drained` is not a counted refusal | no |
| K3 stop-record clause in `collect_stall._k3_k4` (unit `collect_stall.judge`, row `shape / data`, census line 91) | data | xref (stop row x launched row) | no: it reads the driver's own record, never a role's words |
| the old body's `last` through `s5_open_windows` (if B-1 (a) is taken) | data | xref | no |
| Q4 brief line, Q5 row and pin, Q7 text, Q-new-2 appender, N1/N2 | — | not checks | — |
| `story_run.run` (census row 797, `shape`) gains an `except` clause | — | class unchanged | no |

No check judges a role's text, verdict or form. AR-29 holds.

## 7. Standing questions (rule 18; on a plan, answered for what the plan prescribes)

DUPLICATION AND CONSISTENCY: three findings.
(1) `window_files.release_stage` vs `release`: the spec says "plus the empty-claim rule `release` already has". That has to be one loop
with a predicate parameter, not a second copy of the walk and the age rule.
(2) Item 10.1's literal status list duplicates the controller's sets; use `controller.STOPPED`/`SETTLED` (B-2).
(3) After A1 the driver has four release entry points (`s5_release`, `s5_release_of_dispatch`, `s5_release_closed`,
`s5_release_completed`). That is acceptable if each docstring names the road it serves and all of them end in `s5_release` or
`window_files`, as the spec says.
Grepped: `def s5_release`, `s5_release(` call sites (`story_run.py:3219, 11624, 11644, 11716, 11766, 11809`), `def release` in
`window_files.py`.

CODE QUALITY: on a plan, what is checkable is the prescribed shapes. Apart from B-2's literal list and the positional ambiguity F-6, no
finding. Grepped: `except Exception|except BaseException` on the `run_claude`/`run_role`/`rework`/`resume_role` path (none swallows
`Drained`; `rework`'s `except Exception` at :10718 is in `budget_or_none`, off the path; `:1947` and `:17172` re-raise).

## 8. Class completeness (rule 5, SIBLING_MAP)

- Axis 5 (stage twins): Q3's S6 twin is inherited through `session_running` (C.7). Q2's S6 twin `s6_open_lanes` is in C1. The OLD-BODY
  twin of Q2's predicate inside S5 itself is not covered (B-1).
- Axis 5 row "Where the story is (four readers, B-268)": `driver-runs.jsonl` is one of its carriers, so a new row kind there goes
  through that row's readers (the 11-reader list in §5, B1).
- Axis 29: `_append_jsonl` joins the adopters, and the spec owns the map line. The queued siblings stay queued and are named.
- Axis 33 (dispatch identity): untouched.
- Other axes: not touched by this spec (no role file, no release copy, no gate words).

## 9. Fixes list

Blocking, before A1:
- B-1: Q2 in the old body's `last` at N != 1; correct the N == 1 sentence and name it as a residual; a way out for a window held open
  by a returned last round that `next` hides; a test of the two-window scenario through the old body.
- B-2: the 10.1 status set read from the controller (`incomplete`, `returned_unaccepted` added); correct the premise and the first
  test key; add the batch row's `debt` test.

Non-blocking:
- F-1: F3 by a cut list from `journal_run` (B1 owns `journal_run`), or the residual written into the K3 docstring line.
- F-2: Q3's new state (registered, never launched): cite the re-entry road now and give a `state-exits` row or pointer; say whether the
  drain test applies at a dispatch's first launch only, and pin it.
- F-3: an outer `except KeyboardInterrupt` around the whole `run` body, covering the run-level handlers, plus a test key.
- F-4: `judgment-census.json` lines 3 and 4 are adjacent, so B2 merges after C.
- F-5: insertion anchors for the two new Driver methods.
- F-6: 10.1 position stated as "after `story_step finish` exit 0 (:3214-3219)", not "inside `if complete is True`".
- F-7: the old-body variant of the ownership sentence (the first sentence is false there).
- F-8: name the CRLF -> LF edge of 11.2 and pin one mixed-ending read.
- List the 11 `driver-runs.jsonl` reader modules in B1's given/DoD; the 10.5 row's first way out is `next` -> `resume_checkpoint`
  (builder confirms).

Needed beyond the manifest: `controller.py` :8520-8570 (`next`'s return/stop branches), `dispatch_identity.py`, `hooklib.py`
`append_jsonl_line`, `config_contract.py` `parallel_windows`, `tools/critic_verdict.schema.json`, `t-2121-critic-tr3-6.md`, the
`judgment-census.json` and `driver-layers.json` fixtures, the TR3-9 C diff.

The decision to accept the spec, and to choose B-1 (c) and the Q2-at-N == 1 residual, is the Lead's. This verdict is an input to it.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B-1 item 10.2: the returned clause reaches only s5_open_windows; the old body's last = len(todo)==1 (story_run.py:11799) carries the two-window counter-scenario because todo excludes the critic-accepted W1; the N==1 claim is wrong (completion_for :17015-17020 never calls s5_open_windows); and a window held open by a returned last round has no way out because controller next hides the return behind any later same-stage dispatch (controller.py:8544-8556), ending at the stage_S5 Refusal (:11756-11759)",
    "B-2 item 10.1: the safety condition lists running/blocked/paused but not incomplete (controller.STOPPED) or returned_unaccepted (resolve_return resumes the same role, story_run.py:16815-16836), so it frees claims of a window that can still write; the premise (an author's recovery finish completes S5) is false, since completion_for returns False for S5 non-critics (:17000-17001); the real gap is a sibling's claims after a recovery-road not-complete critic finish followed by the last window's complete finish in the same process"
  ],
  "fixes": [
    "B-1: route the old body's last through s5_open_windows at N != 1, name the N==1 residual (Lead call), name a way out for a returned last round, test the two-window scenario through the old body",
    "B-2: read the status set from controller (running, STOPPED, SETTLED or RETURNED), correct the premise and the first test key, add the batch row's debt test",
    "F-1: F3 cut list kept by journal_run's in-process set of open calls (no run_claude edit), or the residual written into the K3 docstring line",
    "F-2: Q3 creates a registered-never-launched state: cite the re-entry road (KNOWN_REFUSALS dead_dispatch to recover, story_run.py:217) and a state-exits row; state whether the drain test applies only before a dispatch's first process",
    "F-3: an outer except KeyboardInterrupt around the whole run body so an interrupt in the run-level handlers (funnel's paid conductor call) also writes the record, plus a test key",
    "F-4: judgment-census.json line 3 (B2) and line 4 (C) are adjacent: merge B2 after C",
    "F-5: name insertion anchors for s5_release_completed and person_stop_record",
    "F-6: 10.1 position stated as after story_step finish exit 0 (:3214-3219)",
    "F-7: old-body variant of the ownership sentence; the first sentence is false on the serial body",
    "F-8: name the CRLF-to-LF edge of 11.2 and pin a mixed-ending read; list the 11 driver-runs.jsonl reader modules in B1"
  ],
  "class_completeness": "Close predicate of S5 has three implementations (s5_open_windows, the old body's last, the N==1 completion_for loop); the spec covers one (B-1). Release-on-complete status set should be the controller's constants (B-2). Axis 5: S6 twins of Q2 (s6_open_lanes in C1) and Q3 (inherited via session_running) named; axis 5 row B-268 covers the new driver-runs row kind (11 readers). Axis 29: _append_jsonl joins the adopters, queued siblings stay queued. Axis 33 untouched. Rule 15: K3 clearing is a pair detector scoped by time, not by carrier (F3 residual, F-1).",
  "trail": {
    "read": [
      "docs/tasks/specs/t-2222-tr4-10-11-s5-windows-leftovers.md",
      "plans/piles/thinking-roles/batch-4-ostatki.md:31-32",
      "docs/tasks/handoffs/20261110-lead-window-acceptance.md section 3",
      "docs/tasks/specs/reviews/t-2121-critic-tr3-6.md Q1-Q5",
      "ai-packages/qa-factory/scripts/story_run.py:575-606, 1560-1575, 1890-1960, 2040-2095, 3065-3100, 3125-3235, 10705-10725, 11446-11454, 11500-11830, 11956-12075, 16660-16700, 16815-16840, 16946-17240, 17844-17862, 19585-19610",
      "ai-packages/qa-factory/scripts/driver_chains.py:200-470",
      "ai-packages/qa-factory/scripts/window_files.py (whole)",
      "ai-packages/qa-factory/scripts/collect_stall.py:1-60, 108-242, 427-470",
      "ai-packages/qa-factory/scripts/controller.py:150-180, 8530-8570",
      "ai-packages/qa-factory/scripts/dispatch_identity.py:30-55",
      "ai-packages/qa-factory/scripts/hooklib.py:469-499",
      "ai-packages/qa-factory/scripts/guard_pre_tool.py:1575-1600",
      "ai-packages/qa-factory/scripts/config_contract.py:555-571",
      "ai-packages/qa-factory/scripts/s5_precheck.py:4258-4268",
      "ai-packages/qa-factory/scripts/driver_journal.py:1-30, story_progress.py:490-520",
      "ai-packages/qa-factory/scripts/tests/test_judgment_census.py:28-38, 440-500; fixtures/judgment-census.json lines 1-5 and grep; fixtures/driver-layers.json grep",
      "ai-packages/qa-factory/design/state-exits.md:20-40",
      "ai-packages/qa-factory/changelog.d/tr3-14-hook-readers.md",
      "docs/SIBLING_MAP.md axis 5, axis 29, axis index",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "git -C D:/ws2/wt-tr3-9c0 diff --stat origin/experiment/thinking-roles...tr/tr3-9c-int", "result": "21 files, +1687/-33; package: story_run.py, driver-layers.json, judgment-census.json, state-exits.md, walk_session.py, validate_artifacts.py, slow_tests.json, story_run_common.py, S6 fixtures/tests; no driver_chains.py, collect_stall.py, window_files.py"},
      {"command": "git diff -U0 (same range) -- story_run.py | grep ^@@ and +def", "result": "hunks in walk_before (:3504) and the S6 lane block (:13398-13698) only"},
      {"command": "git diff -U1 (same range) -- judgment-census.json state-exits.md", "result": "census line 4 (ratchet) and a row at 798; state-exits row added after line 49"},
      {"command": "git -C wt-fbfix diff --stat HEAD origin/experiment/thinking-roles -- the owned files", "result": "empty (line numbers hold)"},
      {"command": "git cat-file -e origin/experiment/thinking-roles:<each DoD test file>", "result": "all 12 named test files exist"},
      {"command": "grep KeyboardInterrupt / open(\"a\" / _append_jsonl( / completion_for( / s5_open_windows( over S", "result": "as cited in section 0"}
    ]
  }
}
```
