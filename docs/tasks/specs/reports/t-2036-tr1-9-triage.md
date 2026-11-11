# t-2036 / TR1-9 triage: what held the S7 close ("checkpoint active work")

Scout, read-only. Copy: `D:/ws1/mybooks-stand\tr-walk`, story LOCAL-1. State dir: `qa-factory/artifacts/LOCAL-1/state/` (below `S/`).
Code root: `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts` (below `W/`).

## (a) The holder

Neither lane 13 nor the rollback record. The only dispatch in `controller.json` whose status is `running` is the S7 analyst's own dispatch, `S7-qa-failure-analyst-6`.

Evidence, `S/controller.json` (revision 353, written 06.11 08:25; the refusal was at 07:28:19; the dispatch's `agent_bound_seq` is 353 = the revision, so nothing changed after the dispatch was bound):

- statuses of the 65 dispatches (counted by script): `accepted 48, stale 14, released_by_person 2, running 1`.
- the one running row: `{"id": "S7-qa-failure-analyst-6", "stage": "S7", "role": "qa-failure-analyst", "status": "running", "dispatched_seq": 351, "agent_id": "310f83c3-...", "agent_bound_seq": 353}` (no `returned_at`, no `returned_digest`).
- lane 13: `S6-qa-runner-13` is `status: accepted` (manual_case_ids TC_118, TC_119; `unresolved: stage_awaits_acceptance`). Its walk file `S/walks/S6-qa-runner-13.json` says `"state": "closed", "reason": "closed by the driver"`. So the abandoned lane is not active work.
- the rollback record: `invalidation` has one entry (reason "t-2006: live proof of the walker..."), its `dispatch_ids` are `S6-qa-runner-2..5` (all `stale`). The two `released_by_person` rows are `S2-qa-case-critic-1` and `S5-qa-automator-14`. None of them is `running`. `state.rewound-*` folders are plain copies and are not read by the controller.
- `S/driver-state.json` `code_close.S7`: `"site": "s7.accepted", "step": "receipt", "details": "controller code_only (exit 2): ... 1) checkpoint active work before code-only completion 2) required prior logical stage incomplete"`, `at 2026-11-06T07:28:19`. Same two lines in `S/standing-refusal.json`.
- the second line, "required prior logical stage incomplete", is `stages.S6.status = "pending"` (`reason: "the runner stopped; S6 awaits the acceptance of qa-failure-analyst..."`). `stages.S7.status = "running"`.
- why the analyst row stayed `running` although its session ended: `S/driver-runs.jsonl` lines 253-258 show launch at 06:28:05, a first "role" end at 07:25:23 and two 1-turn resumes (07:26:17, 07:26:41) with exit_code 0. Then at 07:28:14 the conductor's refusal (`S/conductor.jsonl` line 55, boundary `S7:S7-qa-failure-analyst-6`): "stage_done: the stage critic's form work/handoffs/S7-qa-failure-analyst-6.yaml does not say which dispatch of qa-runner it reviewed: its inputs_read needs the row path: work/handoffs/S6-qa-runner-13.yaml". So the analyst's `finish` was never accepted, the dispatch stayed `running`, S6 stayed `pending`, and the driver then tried the S7 close by code over its own running dispatch. `controller.json.next_action` still reads `wait_existing_job S7-qa-failure-analyst-6, cancel_allowed false`.
- The analyst's `driver-runs` row says its process ended (`kind: role`, `exit_code 0`) - that is the "driver recorded this session as ended" evidence `dispatch_liveness` reads (see c). I did not run the reader on the copy (not asked to touch the factory); that this exact dispatch reads `returned` is inferred from those rows, not measured.

Limit: the copy's state was not rewritten after 07:28 (revision stayed 353), so the cause above is what the state shows now and equals the state at the refusal. The 07:28:19 refusal text itself is quoted from the driver record, not re-run.

Consequence for the fix: the finding's wording ("active dispatch of ANOTHER stage") does not match this run. The holder is a dispatch OF S7 itself (the very analyst whose acceptance is the close). The refusal text must name the dispatch id whatever its stage, and the dead-session test must apply to it.

## (b) Where the refusal and the S7 handling are

- Refusal sentence: `W/controller.py` line 798, in `code_close_conflicts(state, stage)` (def at 783): `problems.append((StateConflict, "checkpoint active work before code-only completion"))` when `facts["running"]`. Called from `Controller.validate`, op `code_only`, line 5456 (def of `validate` 4838; the op branch starts at 5442). The same sentences are literals on purpose (route generator reads them).
- The running list: `code_close_facts(state, stage)`, def at line 751; the loop at lines 768-771 counts EVERY dispatch row whose status is `running` or missing (any stage), by `row.get("id") or key`. It takes no liveness: a dispatch whose session is dead counts as running. The direction of error is deliberately the refusal (docstring, FR-59).
- Second reader of the same facts: `W/execution_request.py` lines ~929-956 (`s6_close_dispatch` uses `code_close_conflicts` and `code_close_facts` for S6).
- Driver side: `W/story_run.py`
  - `Driver.stage_S7` line 12934; `s7_closed_by_scribe` just below (line ~13030; it calls `close_by_code("S7", ..., site="s7.accepted", ...)` at ~13040). `close_by_code` def at 13796; `code_only` def at 6755 (calls `controller("code_only")` at 6768); `code_close_site` wrapper marks the refusal `close = {site, stage, step}` (~6775-6781).
  - `Driver.code_close(refusal)` def at 16625: the seam that turns the controller refusal into the question `code_close.stage` ("its own record of that close was refused ... filed as a defect of ours"). The B-20 branch at ~16654-16683 handles only "required prior logical stage incomplete" and only when `not facts["running"]`; with a running dispatch it falls through to `file_defect(...)` and `code_close_ask(...)` (line ~16680-16684) - that is the road this run took, and why the person was told "no word of yours passes what refused".
  - the question text comes from `code_close_lead` (def 16696) / `code_close_ask` (def 16685); neither names the running dispatch.

## (c) The liveness reader to reuse

`W/dispatch_liveness.py`, `state(project_root, ticket, dispatch, now=None) -> dict` (def at line 919).
- Input: `dispatch` is the controller's dispatch row (needs `id`, `role`, optional `started_at`/`dispatched_at`, `returned_at`/`returned_digest`; it may carry `in_flight`).
- Returns `{"state": "alive"|"abandoned"|"never_started"|"returned"|"unknown", "last_at": ..., "evidence": [strings]}`, plus `"process": "gone"` when the driver's pid is gone. Constants `ALIVE, ABANDONED, NEVER_STARTED, RETURNED, UNKNOWN` at lines 77-81 area.
- For a dead session: `returned` when the driver wrote its end row in `state/driver-runs.jsonl` (`driver_session_end`, def 749; evidence "the driver recorded this dispatch's session as ended (exit N)") or the row has `returned_at`; `abandoned` when the own transcript is silent past `abandoned_after_s` (600 s default) and no non-terminal host receipt exists; `never_started` when there is no transcript and no stop after `never_started_after_s` (180 s). `process: gone` is added when the driver's `in_flight` pid is dead and changes nothing else. `unknown` = no proof either way (a stale non-terminal receipt): it must keep the refusal (nothing is closed by inference).
- Dead = `returned`, `abandoned`, `never_started`. Alive/unknown = keep it as active work.
- The driver's own call site to copy: `Driver._liveness_refusal` in `story_run.py` line ~16036-16046 (`dispatch_liveness.state(self.project, self.task, dict(record, id=dispatch))`).
- The controller already wraps it for every spelling of a story name: `Controller._liveness(self, project, record, now=None, names=None)` at `controller.py` line 2206 (seniority ALIVE > UNKNOWN > RETURNED > ABANDONED > NEVER_STARTED; an unlisted state ranks as UNKNOWN), used at lines 7083, 7148, 7793. This is the one to reuse inside the controller (names via `self._story_names(project)`).
- Design note for the fixer (not decided here): `code_close_conflicts`/`code_close_facts` are pure functions of `state` with no project root, shared with `execution_request`; liveness needs `project_root` and the ticket, so the dead-dispatch filter has to be passed in (e.g. a precomputed set of dead dispatch ids) or applied at the `Controller.validate` call, keeping an unreadable verdict on the refusal side.

## (d) Tests that judge each function

- `code_close_facts`, `code_close_conflicts`: `W/tests/test_controller_state.py` (function `code_close_conflicts_is_the_one_predicate`, line 1466; sentence cases at lines 801, 830, 839, 1254, 1477-1511, 1574). Also `W/tests/test_execution_request.py` (S6 close context reuse) and `W/tests/test_code_close_behind.py` (uses the facts).
- `Driver.code_close` (B-20 branch, `code_close_ask`): `W/tests/test_code_close_behind.py` (343 lines; in-process Driver over a seeded project, controller stubbed); `W/tests/test_code_close_*` for the S6 text: `W/tests/test_story_run_s6.py` line 1956-1964 for the held-refusal wording.
- `Driver.stage_S7` / `s7_closed_by_scribe`: `W/tests/test_story_run_s7.py` (`k5_stage_s7_asks_code_before_the_analyst`, line 92) and `W/tests/test_stage_acceptance_consumer.py` (lines 304-316 call `SR.Driver.stage_S7`).
- `dispatch_liveness.state`: `W/tests/test_dispatch_liveness.py` (silent agent -> abandoned at line 143; control at 461; driver-end row and pid cases further in the file).
- `Controller._liveness`: `W/tests/test_controller_scope_expansion.py` (only test file that calls `._liveness(`); `W/tests/test_worker_lifecycle_active.py` for the host-verdict side.
- The refusal word `checkpoint active work before code-only completion` is also pinned in `W/tests/test_controller_state.py` lines 830/1254 and `W/tests/test_code_close_behind.py` line 193: a change of the sentence breaks these on purpose.

## Trail and controls

- Searched: Grep `checkpoint active work` over `W/` (hits in controller.py 798/4873/4916/5474 and tests only; story_run.py has no literal). Positive control for the state reads: the same Python reader printed the Counter of statuses and found exactly one `running` row; the driver-state key `code_close.S7.details` quoted above carries the same sentence as the code literal.
- Negative claims: "no other `running` dispatch" rests on the script `[k for k,r in dispatches if r.status in (None,'running')]` which returned only `S7-qa-failure-analyst-6`; the same script form listed `released_by_person` rows (S2-1, S5-14) as its positive control. "`dispatch_liveness` is not used by code_close_facts" - grep of `dispatch_liveness` in controller.py shows uses only at lines 2207-2222 (`_liveness`), 7031-7083 and other closure/repair paths, none in 751-800.
- Not done (outside scope): running the liveness reader on the copy; reading the analyst handoff yaml.
