# t-2002 - walker N5s, serial walk lanes (report)

Branch `wn5s` in `D:/ws1/wt-fb3`, commit `857ec889c` on b731b94ba, NOT pushed. Status: DONE for all DoD items; open points below.

## What was built
- `controller.py`: `MANUAL_WINDOW_CASES` 1 -> 3; new `walk_lanes(cases, keys, size)` (pure; key `""` = guest; a case with no usable key is a lane of its own; a `size` below 1 reads as 1, no raise - a raise would make it a census unit); new `lane_keys(task_root, cases)` (reads `manual_evidence.request_actors`: a case whose request is unreadable is left out of the map; `task_root=None` -> all `""`).
- `story_run.py`: `run_role(after=)` (the call sits in a `finally` around the result block, before bind/handoff/finish); `resume_role` (`walk_reopen` before the role, `walk_after` in a `finally`); `manual_plan` cuts with `walk_lanes` and lets an open `walk_retry` case through the done set; `run_manual_block` (walk_before after the dispatch is registered, walk extras without a `finalize_task` line unless E5s.3, today's lines on the fallback road, `after=`, `complete` as a callable that is False while `walk_pending`, re-lane after `stand_login_gate`, closed refusals named beside `plan["refused"]`); new `walk_before`, `walk_reopen`, `walk_pending`, `walk_after`, `walk_values`.
- `story_step._manual_block_door` and `story_progress._block_position` use `walk_lanes`/`lane_keys` (twins, one function, one size). `math` import removed from story_progress.
- `s6.md` (3 lines), `changelog.d/t-1957-n5s.md`, `driver-layers.json` (5 method rows, state key `walk_retry`), pins in `test_manual_window.py` (3, 5 and the cases that follow from it) and `test_story_progress.py` (C4: 3, and 7-left total 8 -> 4).
- `test_walk_lanes.py`: the 13 DoD tests, runs as a script (exit code).

## Rule walk (factory-rules, sections touched)
A - no refusal site added; the one refusal text written (`left_unchecked` request) names what happened and a door (FR-1), nothing locks the walker (FR-57: a failed `open` falls back to today's road). B - no text for a person. C - FR-14: `walk_lanes` shape documented in the docstring; FR-15 the card/report/session are made for the walker, not searched; FR-47/AR-29 code carries data (lanes, records, values), judges no Then. D - FR-41/59, AR-28: a missing verdict -> inconclusive, an unreadable request -> a lane of one, a refused build -> retried once then `left_unchecked`, never a pass. E - FR-23: every lane case ends in a record or a named refusal. F - the `after_end` timing line is written (FR-41 reader exists in `walk_timing`). G - FR-30 English (`selftest.py --lang` ok), FR-29 no control bytes, FR-54 siblings walked below.
AR: 14, 15, 19, 25, 28, 29 as in the commit.

## Witness (verbatim)
```
python -m pytest -p no:cacheprovider .../test_walk_lanes.py .../test_manual_window.py -q
.............                                                            [100%]
13 passed in 30.26s            (test_manual_window collects 0 under pytest: it is script style)
python -B .../test_manual_window.py            -> === test_manual_window: 32/32 ok ===   exit=0
python -B .../test_driver_layers.py            -> === test_driver_layers: 52/52 ok ===
python -B .../test_judgment_census.py          -> === judgment_census: 21/21 ok ===
python -B .../test_walk_lanes.py               -> 13 passed, exit=0
python -B scripts/selftest.py --lang           -> === qa-factory selftest: 2/2 ok ===
```
Negative control (byte copy first, sha256 693a7695a9c26cbec87ed855ab3f02b693f622ee083b136d062f1382e001d92c): `after` moved from the `finally` to after `finish`:
```
FAILED ...test_walk_lanes.py::test_after_runs_before_bind
E  AssertionError: ['role', ('bind', False), 'handoff', 'threshold', 'gate', 'finish', ...]
1 failed, 12 deselected
```
Restored from the copy; sha256 after restore = the same value (then the later edits were made on the restored file).
Earlier red runs fixed on the way: `test_driver_layers` L4 (state key through a class constant -> literal `"walk_retry"`), `test_judgment_census` C1 (`walk_lanes` raised -> became a census unit; now it does not raise).

## Decisions I took (spec silent) - confirm or reverse
1. `lane_keys` is a second new function in controller.py (spec: `walk_lanes` only): the unreadable-request rule needs `request_actors`'s `why`, which `manual_capture.lane_key` hides (it returns `""`), and three callers need the same map (AR-15). Alternative: three inline copies.
2. `walk_lanes` size < 1 -> 1 instead of ValueError (census unit otherwise; the judgment-census.json is not in owns).
3. Actor of a lane: key `""` -> `--actor guest`; else `manual_capture.auto_actor` of the lane's first case. A case naming 2 accounts (auto_actor refuses) or a role the stand does not list -> no session, today's road (Slice 1 does not use `--actor2` for a lane).
4. `open` fails -> the dead `state/walks/<W>.json` is deleted so `brief_pack.walk_record` sees no walk (answers N3b's open question for the fresh dispatch).
5. `walk_before` does not call `prepare_for_block`: `manual_plan` already prepared every case of the entry.
6. Idempotence marker: `work/walks/<W>/after.json` `{rows: {case: ...}}`; the retry counter: driver state key `walk_retry`. A requeue works by letting an `open` case out of `manual_done` in `manual_plan` (the accepted lane carries its id).
7. `values.yaml`: a flat JSON object of `header.verdict`, `scope[i].id/case/state/reason/evidence`, `manual_observations[i].case/then/observed/result/evidence`; `then`/`observed` are generic sentences naming the case and the record state, not the Then text. NOT proved against a live form (`handoff_check` was not run); written only when the form exists and no `.values.applied.yaml` is there.
8. Walk extras line on the walking road: "Execution kind: manual - walk the items of walk session <W> ... the factory closes the session and builds the case records when you end." + the E5s.3 last-command sentence. The request-path line and the unprepared lines are dropped on that road (E5s.7: closed by `walk_after`).
9. The edit of `test_story_progress.py` goes beyond "881-882 only": the same C4 function's `blocks_total` 8 -> 4 follows from the new window (line 891); line 894 (size 2 -> 5) is unchanged because a `None` root reads every case as a guest.

## Edges untested
- `run_manual_block` end to end (the DoD names no test; heavy): E5s.4's "brief lines always present" and the `complete` callable are covered only by reading. `resume_role` is tested with stubs; a `ready`-and-alive session skipping the reopen is not.
- `walk_after` on a REAL lane (real `record_from_walk`, real `finalize_task`, real `handoff_check` applying `values.yaml`): only stubbed. A walker that halts and is resumed: its items already handled by the first `after` (inconclusive, no verdict) are skipped by the marker on the second `after`.
- Two accounts per lane (`--actor2`), `manual_close`'s reason line double counts a case closed `left_unchecked` (it is in the accepted lane's `manual_case_ids`), the recovery road `completion_for` (`manual_plan(scope, skip=mine)`) does not see an open requeue.
- Windows `open` timing (90 s) inside `self.py` has no ceiling in `PY_TIMEOUTS`.

## CI-only files that pin what I touched (NOT run, NOT edited)
- `test_story_step_manual_block.py`: K-R2 :322-323, :344, :350, K-R3 :365, :371, K-P2 :406 (door = one case, "of at most 1 case(s)", counts), :659/:667 (`"manual_blocks(" in plan_src and gate_src` - `manual_plan` now calls `walk_lanes`), :161-167 (`manual_blocks` itself, unchanged, should stay green).
- `test_story_run_s6.py`: :321/:665/:705 (`MANUAL_BLOCK_MAX` set by hand, fine), T329-g :1657-1674 (substring `from controller import MANUAL_WINDOW_CASES` still holds); any test that drives `run_manual_block` on a fake driver now also meets `walk_before` (`self.py` calls to `finalize_task.py`, `app_card.py`, `walk_session.py`) and `self.state["walk_retry"]`.
- `test_story_progress.py`: edited C4; other S6 progress tests that count manual blocks with a window of one.
- `test_brief_pack*.py`, `test_role_commands.py`: untouched by me.

## Fix the class - analogs seen (not changed)
- `story_run.py` `completion_for` (the recovery road, ~:15639) and the S6 re-entry twin cut by `manual_plan`, so they follow it; but they do not know `walk_retry`.
- `stand_login_gate` re-chunks with plain `manual_blocks` (non-goal): `run_manual_block` re-lanes after it; the gate itself still splits by size alone.
- The skill road (`s6.md`) opens no walk session (queued by the spec; `s6.md` says it walks with `manual_capture`).

## Needed beyond the manifest
`handoffs/s6-runner-to-analyst.yaml`, `handoffs/vocabulary.yaml`, `handoff_check.py` (values file shape), `app_card.py` (CLI), `walk_session.py` (open/close/write_verdict/alive), `manual_capture.py` (`lane_key`, `auto_actor`, `load_config`), `manual_evidence.py` (`request_actors`, `build_record`, `write_unprepared`), `story_step.py` (`_brief`, `FORM_REL`, `_task_root`), `test_driver_layers.py` + `driver-layers.json` layer rules (resume_role/run_role are layer `driver_dispatch`, so the new members are homed there), `test_judgment_census.py`, `plans/features.json` (needed no change: `scripts/tests/test_walk_*.py` already covers the new test).
