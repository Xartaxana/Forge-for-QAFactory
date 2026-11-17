# FV3-21c — the skill road closes S6's manual half when nothing is left to dispatch (draft card)

Designer draft for task t-1182, node `live-run-fvf/3/FV3-21c` (the brief names it FV3-21; card r2 §4.5 calls it FV3-21c; the
dispatch's own `node:` line says `FV3-21` — see §11 "Brief contradictions"). Source: card r2
`docs/tasks/specs/20261117-s6-manual-half-no-stand-card-r2.md` §4.5 (:606-620), fork R2-F1 = (a). Every line number below was read
in the worktree `C:/QAFactory/forge-repo/.claude/worktrees/agent-af279738b46568113` (the branch holding FV3-21 + FV3-21b).
The Lead decides every fork in §8; the card can be carried out by its recommendations as written.

## 0. Dispatch header (for the builder dispatch; `python -B tools/dispatch_new.py` prints the checked form)

```
task: <new id>
node: live-run-fvf/3/FV3-21c
feature: F19
given:
C:/QAFactory/forge-repo/docs/tasks/specs/20261117-fv3-21c-skill-road-s6-close-card.md
C:/QAFactory/forge-repo/docs/tasks/specs/20261117-s6-manual-half-no-stand-card-r2.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/architecture.md
C:/QAFactory/forge-repo/plans/builder-rules.md
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/stage_close.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_s6.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_s7.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_dispatch.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/story_step.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_story_step_manual_block.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test-layers.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/skills/qa-story/phases/s6.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/changelog.d/fv3-21c-skill-road-s6-close.md
C:/QAFactory/forge-repo/docs/SIBLING_MAP.md
non-goals: the other S6 code steps of the skill road (s6.nothing, s6.results_stand, s6.accepted with no manual half, s6_reentry, s6_reprove_before_manual) = node FV3-21d (§7); story_progress.py (fork F3); any quarantined test; the driver's deferred questions, stand-login gate, walk_retry, lanes
handoff: the diff on the branch + the builder report (FR pass, AR lines, witness output, the probe's byte-copy comparison)
edges: §4 of the card (E1-E16), each with its invariant
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <every owned package path>` and each test file it prints; plus `scripts/tests/test_judgment_census.py` and `scripts/tests/test_driver_layers.py` when the witness does not print them (the detectors of AR-29 / AR-20, architecture.md step 8)
siblings: axis 5 rows "Code-only stage closes" (SIBLING_MAP:130) and "Skill phase <-> driver" (:133); axis 34 (one road); FV3-21d named in §7
designer: <this file, once accepted>
```

If fork F5 = (a) (two builder nodes), node FV3-21c-1 owns the four driver/shared files + `test-layers.json` and carries items
K5.a-K5.d; node FV3-21c-2 owns the rest and K5.e-K5.j, sequential after FV3-21c-1 (same branch).

## 1. Defect, scope, AR-n, owners, census

### 1.1 Defect (re-checked by trail)

- On the skill road S6's manual half is started with `story_step.py start --stage S6 --role qa-runner --execution-kind manual
  [--scope ...]` (`phases/s6.md:10`). When nothing is left to dispatch, `_manual_block_door` prints `no manual-agent case is left
  for a block: nothing was dispatched; covered by ...` (`story_step.py:1108-1111`) and `start` exits 2; under the FV3-21b word the
  block is refused with no door to anything after it (`:1059-1076`); a block whose every case `prepare` refused gets a door of the
  derived rest minus THIS call's refusals only (`:1084-1090`, `spent`), so earlier refusals are offered again.
- `stage_done.py --status done` refuses S6 while the controller has not accepted it and names a `code_only` receipt as the road
  (`stage_done.py:1225-1250`); with a consumer it also refuses without the consumer's record (`:1215-1224`,
  `acceptance.consumer_close_refusal`, `acceptance.py:1512-1527`). The author's own finish cannot complete S6 either
  (`acceptance.stage_acceptance_refusal`, `acceptance.py:1554-1559`).
- No skill-road file writes `code_only`: a count grep of `code_only|code-only` over `scripts/*.py` lists 21 non-test scripts and
  `story_step.py` is not among them (positive control in the same call: `stage_done.py:1`, `story_progress.py:7`).
- The only writer is the driver: `manual_close` (`driver_stage_s6.py:1050-1075`) -> `finalize_task.py` -> `consumer_need_record`
  (`:313-347`) -> `close_by_code` (`driver_stage_s7.py:763-786`) -> `close_receipt` -> `code_only` (`driver_dispatch.py:2536-2563`)
  -> `controller("code_only")` (`driver_runner.py:391-405`, the CLI) -> `record_close` (`driver_dispatch.py:2565-2581`). All are
  Driver methods needing `self`.
- The driver reaches `manual_close` only when (i) the manual scope is non-empty and (ii) the automated half is empty or an S6 runner
  of the automated half is accepted (`stage_S6`, `driver_stage_s6.py:513-515, 541, 605-610`; `run_manual_block` `:1642-1645`).

So today a skill-road story whose manual cases are all refused, or all done with the last block finished `--not-complete`,
can never complete S6: P31 / axis 34 residual of card r2 §4.5.

### 1.2 Scope

ONE survivor of the close, wired to both roads (AR-15, P31): the consumer rule, the manual-half close order and the code close
move out of the Driver into a module both roads import; the Driver's methods delegate (same names, same homes); the skill road
calls the same functions from the same call that finds nothing left. Out of scope, named as node FV3-21d (§7): the other S6 code
steps the skill road lacks (a slice is no exclusion: the rest is a named node of this spec, designer rule 6).

### 1.3 AR-n touched and the change check each demands (architecture.md)

| AR | how kept | change check written into the DoD |
|---|---|---|
| AR-15 | `stage_close.py` is the one survivor of three steps (consumer rule, manual-half close, code close); every road calls it; nothing is copied | report lists every site by a grep for the PROBLEM, not the helper: `finalize_task.py`, `"code_only"`, `acceptance_awaits` over `scripts/*.py` (not tests), each hit = a site that calls the survivor or is named; SIBLING_MAP axis 5 row "Code-only stage closes" (:130) names `stage_close` as the survivor in the same commit (K5.j) |
| AR-13 | `acceptance.awaits_acceptance` / `accepted_for` / `consumer_of`, `controller.manual_done_cases`, `Controller.stage_scope`, `waiver.stand_passing_word`, `waiver.split_overridden`, `hooklib.read_json` / `project_root` are the readers; no second parse | DoD grep over the diff of `story_step.py` and `stage_close.py`: no `"acceptance_awaits"` read outside the moved marker writer, no `json.loads(` of `pipeline.json`; positive control: the same grep finds `acceptance_awaits` in `acceptance.py:1496` |
| AR-14 | code_only receipt: the controller's `code_only` operation only, request built by one builder `stage_close.code_only_request`; acceptance record: `stage_done.py --acceptance` only; awaiting marker: the one moved site in `stage_close.need_record`; refused records: `manual_evidence.write_case_refusal` only | DoD grep: no `atomic_json` / `write_text` in the diff of `story_step.py`; in `stage_close.py` exactly one `atomic_json` (the marker) |
| AR-17 / FR-48 / P3 | the close is code run by the stage's own call; the conductor runs no new command; no new stop, no new question | no new `Person`, `no_move`, `ask` site in the diff (grep) |
| AR-19 | S6/S7 twins keep sharing one consumer rule (`CONSUMER_ROUTES` one definition); the skill phase and the driver now run the same code for the manual-half close | report names the twins: S7's close sites (`s7_close` via `consumer_need_record`, `close_by_code` callers in `driver_stage_s7.py`) behave unchanged (witness: the S7 tests witness-for prints) |
| AR-20 | no ratchet raised: `driver-layers.json` `allowed_importers` unchanged (stage_close imports no `driver_*`), census ceilings unchanged | report line "ratchets raised: none" with `test_driver_layers.py` and `test_judgment_census.py` output |
| AR-21 | the receipt is written only over a `run-report.json` the reducer has just written (reduce first) | rows C2, C7 |
| AR-22 | the `code_only` producer and the `acceptance_awaits` producer now exist on the skill road; their readers (`stage_done` close check, `awaits_acceptance`, the controller's `next`) are unchanged; the s6.md promise gets its producer | grep `acceptance_awaits|code_only` readers listed in the report |
| AR-23 / FR-23 | "nothing left to dispatch" is a recorded completed state (closed, or awaiting) — never an escalation; an EMPTY manual half is declared: no close here (FV3-21d) | rows C1, C2, C10 |
| AR-25 | the awaiting state has its move (the S7 card, then the same `start`); a refused close names its door | rows C1, C7, E9 |
| AR-27 | every refused case is named in the close reason and its request path stands in the receipt's evidence; passed-over work is filed (moved `file_passed_over`) | row C2 |
| AR-28 / FR-59 | an underived scope, an unreadable state, a live S6 dispatch, a word not later than the acceptance -> no close / no pass | rows C3b, C5, C8, C11 |
| AR-29 | checks and owners in §1.4 | `test_judgment_census.py` green; a new unit or changed class -> builder STOPS and asks |
| AR-9 | every refusal of the close ends with a `door:` line | rows C7, E9 |
| AR-24 | the person's words reach the pass record (`--quote "by: person - <words>"`, cut at 500 as today — unchanged, not widened) | row C3 |

Commit lines: the `architecture:` line naming AR-9, AR-13, AR-14, AR-15, AR-17, AR-19, AR-20, AR-21, AR-22, AR-23, AR-25, AR-27,
AR-28, AR-29 and the `judgment:` line, both in the form `tools/architecture_gate.py` carries (the one carrier of the grammar; not
copied here). Recommended `judgment:` content: `none -- every check added or moved judges data (derived scope, dispatch states,
record presence, word time); the verdicts stay the failure analyst's and the person's`. The `docs/SIBLING_MAP.md` edit carries the
`axes: not a mechanism (<reason>)` line (`tools/mechanism_gate.py`), reason: a twin row of axis 5 records the survivor of an existing
twin; no new duty.

### 1.4 Checks added or moved — owner and census class (AR-29, P27)

| check | where | owner | census class | census unit? |
|---|---|---|---|---|
| CK1 nothing left to dispatch (derived manual scope minus done minus refused, after preparing each remaining case) | `story_step._s6_manual_close` (new) | data (code) | xref (joins scope, accepted dispatches, prepare outcomes) | no: returns lines (list transport) from `_manual_block_check`, whose row (`judgment-census.json:1124`, shape/data) stands |
| CK2 the automated half is settled (empty, or an accepted S6 automation runner) | `stage_close.s6_automation_settled` (moved from `driver_stage_s6.py:513-514`) | data | xref | no: returns bool |
| CK3 no live S6 dispatch | in CK1 (reads `state.dispatches` status `running`) | data | shape | no |
| CK4 the consumer rule: record stands, person's pass (word later than acceptance), else await at `manual_close` / refuse elsewhere | `stage_close.need_record` (moved) | data for record presence and time; the verdict inside the record is the analyst's (judgment, accepted by its own form) and the pass is the person's (intent) | xref | no: raises `stage_close.Refused(Exception)`, the same transport class as the driver's `Refusal(Exception)` today (no census row for `consumer_need_record` today: r2 trail) |
| CK5 the reducer must succeed before a receipt | `stage_close.manual_half_close` (moved) | data | shape | no (Exception transport) |
| CK6 the receipt needs existing evidence | `stage_close.code_only_request` (moved from `driver_dispatch.py:2539-2545`) | data | shape | no (Exception transport) |

## 2. The design (answers to the brief's questions 1-3; each choice is also a fork in §8)

### 2.1 Where the shared logic lives (Q1; fork F1)

New module `ai-packages/qa-factory/scripts/stage_close.py`: "the closes by code a stage takes when no role is left to run it, for
both roads". It imports no `story_step` and no `driver_*` (no cycle; no `allowed_importers` row, `driver-layers.json:5-8`); its
package imports (`acceptance`, `waiver`, `controller`, `event_store`, `manual_evidence`, `hooklib`) are taken inside functions, as
the Driver does today. The driver modules import it (a family module importing a non-family module is legal, as `waiver` /
`manual_evidence`).

What replaces `self`: a ROAD — an object with the members below. The Driver IS a road (every member exists on it today; nothing
new on the Driver). The skill road is `stage_close.SkillRoad`. INVARIANT (stubs and spies): every step a shared function takes goes
through the road's member of that name, never straight to the free twin — so `driver.accepted_at`, `driver.consumer_person_pass`,
`driver.close_by_code`, `driver.py` stubs in `test_story_run_s6.py:2583-2587, 2847-2927` keep their effect.

Road members: `task`, `task_root`, `project`, `dry`; `controller_state()`, `pipeline()`, `controller(op, *args, input_data=None)`;
`py(script, *args, check=False, expect="") -> (code, out)`; `owe_row(script, *args, what, stage)`; `accepted_at(author)`;
`consumer_pending(stage)`; `person_pass(stage, author, line, answer="", since="")`; `consumer_person_pass(stage, author, answer="")`;
`consumer_need_record(stage, site)`; `close_by_code(stage, reason, evidence, *, finalize, site="", digest="", role="",
journal=False, tail=(), fresh=None)`; `close_receipt(site, stage, reason, evidence)`; `file_passed_over(stage, receipt)`;
`record_close(site, stage, *args, tail=(), receipt="")`.

Free functions (bodies MOVED from the named Driver methods, behaviour unchanged):

| function | moved from | notes |
|---|---|---|
| `class Refused(Exception)` with `title: str = ""` | — | the shared refusal; NOT a ValueError (census: same transport class as `driver_core.Refusal`) |
| `CONSUMER_ROUTES` (data keys only: `consumer_stage`, `author`, `who`, `what`, `await_at`, `closes_when`, `awaits`) | `driver_stage_s6.py:148-160` | the Driver keeps `CONSUMER_ROUTES = {s: dict(row, rework_complete=<its lambda>) for s, row in stage_close.CONSUMER_ROUTES.items()}` — one definition of the data |
| `s6_automation_settled(state, auto_scope) -> bool` | `driver_stage_s6.py:513-514` | `stage_S6` calls it |
| `consumer_pending(road, stage) -> bool` | `:172-181` | |
| `accepted_at(task_root, author) -> str` | `:224-234` | |
| `heard_word(pipeline, stage, line, since) -> dict` | the waiver half of `person_pass` incl. `stamp`, `:282-301` | pure |
| `person_pass(road, stage, author, line, answer="", since="") -> dict` | `:271-311` | dry gate via `road.dry`; the record via `road.py("stage_done.py", ..., check=True, expect=...)` |
| `consumer_person_pass(road, stage, author, answer="") -> bool` | `:236-269` minus the `refusal.retry` lines | the Driver delegate keeps the retry (`except Refusal as r: r.retry = ...; raise`) |
| `need_record(road, stage, site) -> bool` | `consumer_need_record`, `:313-347` | raises `Refused` where the Driver raised `Refusal`; the one marker writer (`atomic_json`) lives here |
| `manual_half_close(road, done, refused) -> bool` | the tail of `manual_close`, `:1067-1075` | True = closed, False = awaits; reason words, `road.py("finalize_task.py", ...)`, `road.consumer_need_record("S6", "manual_close")`, `road.close_by_code(..., finalize=False, site="s6.manual_close")`; evidence `["work/run-report.json"] + <request paths of refused cases via manual_evidence.request_path>` |
| `close_by_code(road, stage, reason, evidence, *, finalize, ...) -> bool` | `driver_stage_s7.py:763-786` | the ORDER: completed check, finalize, `fresh`, `road.close_receipt`, `road.file_passed_over`, `road.record_close` |
| `code_only_request(road, stage, reason, evidence) -> dict` | the request half of `driver_dispatch.py:2539-2551` | raises `Refused(..., title="code_only_evidence")` when no evidence file exists |
| `file_passed_over(road, stage, receipt)` | `driver_stage_s6.py:1972-1992` | |

Driver delegates (each keeps its name and home, so every `driver-layers.json` row — `:664, 698-704, 733, 1069` — stands): the
methods above become one call to the free function; where the free body can raise `stage_close.Refused`
(`consumer_need_record`, `manual_close`, `close_by_code`, `code_only`) the delegate converts it once:
`except stage_close.Refused as exc: raise Refusal(str(exc), title=exc.title) from None`. `manual_close` keeps its driver-only
head (the `deferred_waiting` refusals, `:1058-1066`) and then calls `manual_half_close(self, done, refused)`. `code_only` keeps
`self.controller("code_only", input_data=request)` and `self.progress_line()`. `close_receipt` and `record_close` stay Driver
methods unchanged (their refusal annotations and retry are driver machinery).

`SkillRoad(task, task_root, controller)` (in `stage_close.py`): `dry = False`; `project` = `hooklib.project_root()`;
`controller_state()` = `controller.state()`; `pipeline()` = `hooklib.read_json(task_root / "pipeline.json")` as a dict (else `{}`);
`controller(op, input_data=...)` = `controller.apply(op, input_data)`; `py` = a subprocess of `<scripts>/<script>` with
`sys.executable -B`, a missing script is exit 127 (never the "skipped" success of `story_step._run`, `:144-150`), `check=True` and
a non-zero exit raise `Refused(f"{script} exit {code}: <last line>" + expect)`; `owe_row` = `py(...)`, a failure prints
`note: <what> was not filed: <last line>` and never raises; `accepted_at`, `consumer_pending`, `person_pass`,
`consumer_person_pass`, `consumer_need_record`, `close_by_code`, `file_passed_over` = the free functions with `self`;
`close_receipt` = `code_only_request` then `self.controller("code_only", input_data=request)`, returns the id;
`record_close(site, stage, *args, tail, receipt)` = `py("stage_done.py", "--task", task, "--stage", stage, *args, check=True)`,
then each `tail` row through `py("log_append.py", *row)`; a refused record raises `Refused` whose text ends with the door
`stage_done.py --task <T> --stage <S> <args>` (E9).

### 2.2 Which skill-road command carries it (Q2; fork F2)

`start --stage S6 --role qa-runner --execution-kind manual` itself, at its refusal exits that today end in "nothing was
dispatched" or a door: the same call that finds nothing left closes. Why: FR-48 / AR-17 / P3 — code runs on the stage's own
transition and the conductor is never a command launcher; a new subcommand would be one more command the orchestrator must
remember (the very gap: the card already promises "code closes S6 itself", `s6.md:6`); `where` is read-only by contract
(`story_step.py:3316-3318`). The driver never calls `start --execution-kind manual` (it registers manual blocks in-process,
`driver_stage_s6.py:1629-1630`; its only `--execution-kind` is `automation`, `driver_dispatch.py:666`), so no driver run passes
the new branch twice; if it ever did, both roads would still run the one function (no mode gate is added: a mode gate would be a
second road).

### 2.3 What `start`, `where` and `story_progress` show after (Q3; fork F3 for the progress line)

| world | `start` prints (last lines), exit | `where` | `story_progress` line (read, not run) |
|---|---|---|---|
| closed by code | the case lines, `S6 is closed by code: the manual half of S6: <n> case(s) checked by an agent by hand, <m> not checked: <ids>`, then `next: python "${CLAUDE_PLUGIN_ROOT}/scripts/story_step.py" card --stage S7`; exit 0 | `next: {"action": "prepare_stage", "stage": "S7", ...}` and `stage card: story_step.py card --stage S7` (S6 completed; loop `controller.py:9241-9271`) | current S7 with no dispatch: head `starting S7 <name>`, `done S0–S6` (`story_progress.py:501, 663-667`) |
| awaits the consumer | the case lines, the moved print `S6: nothing is left to dispatch; S6 awaits the acceptance of qa-failure-analyst for <runner> (the failure analyst is let in; its record closes S6)` (`driver_stage_s6.py:341-342`), then `next: the failure analyst judges S6 first: python "${CLAUDE_PLUGIN_ROOT}/scripts/story_step.py" card --stage S7; after its record, run this same start again: it closes S6`; exit 0 | `next: {"action": "prepare_stage", "stage": "S7", ...}` (`awaits_acceptance` moves `i`, `controller.py:9259-9261`) | current S6, nothing running: position `dispatch` (or `manual block i of n` when the latest S6 dispatch was a manual block) with `no role running` (`:550-557, 663-669`) — it does NOT say "awaiting"; fork F3 |
| after the analyst's record | `where` says `prepare_stage S6` (the wait is over, S6 still open); the S6 card sends the orchestrator to the same `start`, which closes S6 code-only (row C2) | | |

## 3. Items

K5.a-K5.d: the move (driver behaviour unchanged). K5.e-K5.j: the skill road.

**K5.a** `scripts/stage_close.py` (new): the module docstring (both roads, the road members of §2.1, the stub invariant), `Refused`,
`CONSUMER_ROUTES` (data), and the free functions of §2.1's table, bodies moved verbatim except: `self` -> `road`; `raise Refusal(`
-> `raise Refused(`; `self.CONSUMER_ROUTES` -> the module table; sub-steps through `road.<member>`.

**K5.b** `scripts/driver_stage_s6.py`: `CONSUMER_ROUTES` built from the module's data (one definition); `consumer_pending`,
`accepted_at`, `person_pass`, `consumer_person_pass`, `consumer_need_record`, `file_passed_over` become delegates (§2.1);
`manual_close` = its deferred-waiting head + `manual_half_close(self, done, refused)` with the conversion; `stage_S6` computes
`auto_done` by `stage_close.s6_automation_settled(state, auto_scope)` (same truth table: an automation runner, or a runner with no
`execution_kind`, accepted).

**K5.c** `scripts/driver_stage_s7.py`: `close_by_code` = delegate to `stage_close.close_by_code(self, ...)` with the conversion.

**K5.d** `scripts/driver_dispatch.py`: `code_only` = `stage_close.code_only_request(self, ...)` (with the conversion, keeping
`title`) + `self.controller("code_only", input_data=request)` + `self.progress_line()` + return the id. `close_receipt` and
`record_close` unchanged.

**K5.e** `scripts/story_step.py`, new function `_s6_manual_close(args, controller, state, spent: dict) -> tuple | None`, docstring
naming FV3-21c, P31, and the driver site it shares (`manual_close`). Steps, in this order:
1. `args.stage == "S6"`, else None.
2. `auto = controller.stage_scope("S6", state, "automation")`, `manual = controller.stage_scope("S6", state, "manual")`; either
   not `derived` or its `scope` not a list -> None (AR-28: today's lines).
3. `manual["scope"]` empty -> None (an empty manual half is FV3-21d's world: the driver closes it by other sites).
4. any dispatch of `state["dispatches"]` with `stage == "S6"` and `status == "running"` -> None (a live walk: no close).
5. not `stage_close.s6_automation_settled(state, auto["scope"])` -> return the marker `"automation"` (K5.g adds the door line).
6. `done = [c for c in manual["scope"] if c in manual_done_cases(state)]`; `refused = dict(spent)`; `words =
   waiver.stand_passing_word(_read_pipeline(task_root))`; for each case of `manual["scope"]` not in `done` and not in `refused`:
   `why = manual_evidence.prepare_for_block(task_root, case)[1]`; `why` -> `refused[case] = why`; else with `words` ->
   `manual_evidence.write_case_refusal(task_root, case, reason, door, "left_unchecked")` with `(reason, door) =
   manual_evidence.no_stand_refusal(words)` and `refused[case] = reason`; else (a case is ready, or walkable unprepared) ->
   return `("left", refused)` (something is left: no close).
7. Nothing left: `road = stage_close.SkillRoad(args.task, task_root, controller)`; `closed = stage_close.manual_half_close(road,
   done, list(refused.items()))`; return `("done", [*case lines "<case>: not checked by hand - <why>" for refused],
   <the closed or the awaits line of §2.3>, 0)`; `stage_close.Refused`, `StateConflict` and `ValueError` raised inside ->
   `("done", ["story_step: refused - S6 was not closed: " + <text>, <door line, E9>], 2)`.
The per-case word step is the same four lines as FV3-21b's branch (`:1066-1072`): factor them into one helper
`_refuse_by_word(task_root, case, reason, door) -> str` (returns the why) used by both places (rule 9 sweep inside the artifact).

**K5.f** `scripts/story_step.py`, `_manual_block_check`, kind manual. POSITION: at the three exits that today return a refusal
because nothing can be dispatched by THIS call — (X1) `not block` (`:1045-1047`), (X2) the FV3-21b word branch (`:1061-1076`,
after `validate_manual_runner_block`), (X3) every case of the block refused by prepare (`:1084-1090` with `every`) — call
`_s6_manual_close(args, controller, state, spent)` with `spent` = {} for X1, the block's cases with their reasons for X2/X3.
Outcomes: `("done", lines, code)` -> return `(None, lines, code)`; `("left", refused)` -> today's return, except the door is built
with `spent=refused` (X1: `door([], refused)`; X3: `door([], refused)`; X2 keeps its own door lines and appends nothing);
`"automation"` -> today's return plus K5.g's line; None -> today's return byte for byte.
POSITIONAL INVARIANT: a malformed block is refused as today and never closes (validate runs before X2/X3; X1 has no block); a call
whose block has a ready case (the partial-refusal exit `:1084-1090` without `every`, and the success return `:1091`) never runs the
plan or the close; nothing the close does registers a dispatch, a stamp, a brief or a `run_mode` stamp (it returns before
`stamp_run_mode`, `:917`).

**K5.g** `scripts/story_step.py`: the `"automation"` outcome appends to today's lines: `door: the automated half of S6 is not
accepted yet; the manual half closes after it: python "${CLAUDE_PLUGIN_ROOT}/scripts/story_step.py" start --task <T> --stage S6
--role qa-runner --execution-kind automation` (AR-25: the null outcome of K-R5's world gets its move; K-R5 keeps passing — it
checks substrings and `door_scope` reads only `--execution-kind manual --scope`).

**K5.h** `scripts/story_step.py`, `start` (`:913-916`): `if code or (refusal and block is None):` print the lines and return
`code`. INVARIANT: today `refusal` is non-empty only with `code == 2`, so the widened test changes nothing for existing outcomes;
the close outcome (`code == 0`, lines, no block) returns before the stamp and registers nothing.

**K5.i** `skills/qa-story/phases/s6.md`, card line 6, after `code closes S6 itself: no runner, nothing re-run.` insert: `When the
automated half is accepted and \`start --execution-kind manual\` finds no manual-agent case left to dispatch (each is done, or
refused with its reason), that same call closes S6: it reduces the run report; with the failure analyst's acceptance or a
person's word it closes S6 by code, otherwise S6 awaits the failure analyst - go to the S7 card, and after its record run the same
\`start\` again.` The card stays under `CARD_MAX_BYTES` (`story_step.py card --stage S6` prints no `over` note — the builder runs it
and quotes the tail). The freshness sentence before it is FV3-21d's (§7), not edited here.

**K5.j** `changelog.d/fv3-21c-skill-road-s6-close.md` (ASCII, one bullet): the skill road's manual `start` closes S6 when no
manual-agent case is left to dispatch, by the same code as the driver (reduce; the failure analyst's record or a person's word
closes it by code; otherwise S6 awaits the analyst). `docs/SIBLING_MAP.md` axis 5 row "Code-only stage closes" (:130): the survivor
is `scripts/stage_close.py` (`close_by_code`, `manual_half_close`, `need_record`), the Driver's methods delegate, and the skill
road (`story_step._s6_manual_close` via `stage_close.SkillRoad`) calls it; row "Skill phase <-> driver" (:133) gains one clause
naming the shared S6 manual-half close. `scripts/tests/test-layers.json`: add `stage_close.py` to the `covers` of
`test_story_step_manual_block.py` (`:6363`) and of `test_story_run_s6.py` (`:6177`), so `--witness-for stage_close.py` names the two
tests that judge it.

**Live proof (FR-33).** The batch's «Живые доказательства» gets one line, moved to `live-runs` at acceptance by the pile rule: a
skill-road story with every manual-agent case refused reaches S7 (awaiting), and after the analyst's record its S6 closes code-only.

## 4. Edges (each with the invariant it protects)

| # | edge | behaviour | invariant |
|---|---|---|---|
| E1 | the automated half not accepted (auto scope non-empty, no accepted automation runner) | no plan, no close; today's lines + K5.g door | S6 is never closed by code over an automated half that never ran (the driver's precondition, one predicate) |
| E2 | manual scope or automation scope not derived / not a list | None: today's lines | an unknown scope never reads as "nothing left" (AR-28) |
| E3 | manual scope empty | None: today's lines (FV3-21d) | the driver's other sites (`s6_reentry`, `s6.accepted`, `s6.nothing`) are not replaced by the manual close |
| E4 | a live (running) S6 dispatch | None | no close over work still running (the controller would refuse the receipt anyway, `code_close_conflicts` :947-950) |
| E5 | one remaining case prepares (ready, or walkable unprepared) | `("left")`: today's refusal, door = the ready cases only | a block with work left is never closed; a refused case is not offered again |
| E6 | `prepare_for_block` refuses on a factory failure (`except Exception` -> refusal, `manual_evidence.py:1338-1339`) | counted refused, named in the reason and the receipt | parity with the driver (`manual_plan` does the same); the case is reported "not checked by hand" with its reason, never silent (AR-27) |
| E7 | no-stand word live | every remaining case gets the word's record (prepare's own refusal kept), then the close | the driver's `manual_no_stand` + `manual_close` outcome on the skill road (P31); a case prepare refused keeps its record (AR-27) |
| E8 | reducer fails | exit 2, `story_step: refused - S6 was not closed: S6 manual half: finalize_task.py exit <n>: <tail>`, door `repair what finalize_task.py names, then run this start again`; no marker, no receipt | nothing is closed or marked over a report nobody could build (AR-21) |
| E9 | `stage_done --status done` refused after the receipt | exit 2; text ends with the door: the exact `stage_done.py --task <T> --stage S6 --status done --digest "<reason>" --no-journal` | the receipt is never lost silently; the record can be completed by the printed command (FR-2); a later `start` re-runs the reducer and `close_by_code` sees `completed` and writes no second receipt |
| E10 | the controller refuses `code_only` (state moved, passed_over changed) | exit 2 with the controller's text | no receipt over a state that moved (the controller's own check) |
| E11 | a person's word dated before (or with no readable time vs) the runner's acceptance | not honoured: awaits | a word never accepts work the person had not seen (F1, FR-4) |
| E12 | consumer record stands for an EARLIER runner dispatch, not the last | not pending -> await (or refuse at no await site) | "a record given for other bytes does not count" (`accepted_for` reads `reviewed_dispatch == author`) |
| E13 | no consumer (`acceptance_by` absent: older stages.json) | `need_record` False: closes by code | the world before X7-6 behaves as the driver does (temporal) |
| E14 | S6 already completed when `start` runs again | reducer runs again, `close_by_code` prints `the controller holds it completed already` and writes no second receipt; exit 0 | at most one receipt per close (`driver_stage_s7.py:772-775`) |
| E15 | TEMPORAL — before the change: no `stage_close.py`, the Driver methods hold the bodies, the skill road prints "nothing was dispatched"; after: the module exists (created by K5.a), the Driver delegates, the skill road closes. A story mid-flight with a marker written by the driver is read the same (one reader) | both worlds named; K5.a creates the module, K5.e-K5.h the road | a pipeline written before the change is read by the same readers; no field changes meaning |
| E16 | a manual case listed done by `manual_done_cases` whose block was superseded or invalidated | whatever `manual_done_cases` says (the one reader; the driver uses it too) | no second reading of "done" (AR-13) |

ERROR DIRECTION of the reused function in a more consequential role (designer rule 1): the "nothing left" computation of
`_manual_block_door` (`:1099-1111`) was ADVICE (a door) and `manual_done_cases` / `prepare_for_block` fed it; in K5.e they feed a
GATE that closes S6. The gate may err only toward "something is left" (no close, today's lines). Adversarial inputs that must stay
on that side, each a row of §5: an underived or non-list scope (C8); a state without `dispatches` or with a running S6 dispatch
(C11); an automated half with no accepted runner (C5); one case that prepares (C6); a word older than the acceptance (C3b); a
reducer failure (C7). The one input that errs toward closing — prepare's catch-all refusal (E6) — is the driver's own behaviour,
kept for parity and reported per case.

## 5. Test rows (one function added to `scripts/tests/test_story_step_manual_block.py`, registered in `main()` `:815`)

`fv3_21c_nothing_left_closes_s6_on_the_skill_road`, over `real_story(root, MIXED_7)` (`:48-69`) and the module's `start` helper
(`:80-105`). Base world W: the automated half started with `start(root, c, None, kind="automation")` and accepted not-complete
with `accept(c, root, "S6-qa-runner-1", "automation", ["TC-1"])` (`:113`); every manual case refused by a prepare stub
(`lambda case: ([], f"refused {case}", "")`). The close's scripts are stubbed at ONE seam, `mock.patch.object(stage_close.SkillRoad,
"py", fake)`: `fake` records `(script, args)`, writes `work/run-report.json` (`{}`) for `finalize_task.py` and returns `(0, "")`;
`stage_done.py` and `project_decisions.py` return `(0, "")`. The controller is the real one (receipt, marker and state are real).

| row | world | expected |
|---|---|---|
| C1 (§4.5) | W | exit 0; py calls == [`finalize_task.py`]; `acceptance.awaits_acceptance(c.state(), "S6", <pipeline>) == "S6-qa-runner-1"`; pipeline `acceptance_awaits.S6 == "S6-qa-runner-1"`; no `code_only` event; S6 not completed; text holds `S6 awaits the acceptance of qa-failure-analyst for S6-qa-runner-1` and `card --stage S7`; `seen["scope"] == []` |
| C2 (§4.5) | W + an accept record for S6 in pipeline.json (`reviewed_dispatch: "S6-qa-runner-1"`, `verdict: accept`, acceptor `qa-failure-analyst`) | exit 0; py calls == [`finalize_task.py`, `stage_done.py` with `--status done --digest <reason> --no-journal`]; `c.state()["stages"]["S6"]` has `status: completed`, `code_only: true`; the code_only event's `reason` starts `the manual half of S6: 0 case(s) checked by an agent by hand, 6 not checked: TC-2, TC-3`; its `evidence_refs` include `work/run-report.json`; text holds `S6 is closed by code` |
| C3 | W + a live waiver `stage acceptance` on S6 with `at` `2099-01-01T00:00:00+00:00` | py calls start [`finalize_task.py`, `stage_done.py --acceptance work/handoffs/S6-qa-runner-1.yaml --acceptor driver --verdict accept --quote "by: person - <words>"`, `project_decisions.py ... add-finding`] then the close (receipt real, `stage_done.py --status done`); exit 0 |
| C3b | as C3, `at` `2000-01-01T00:00:00+00:00` | not honoured: C1's outcome (awaits), no `--acceptance` call |
| C4 | W with prepare READY for every case + the no-stand word (`stage_overrides` as FV3-21b `put`), `start(root, c, "TC-2")` | every TC-2..TC-7 request `== {"refused": {"reason": <word reason>, "door": NO_STAND_DOOR, "by": "left_unchecked"}}`; C1's outcome |
| C5 (control) | MIXED_7, no automation runner, every case refused | today's lines (exit 2) + the K5.g door line; py never called; no marker |
| C6 | W, TC-7 prepares | exit 2; `door_scope(text) == "TC-7"`; py never called; no marker |
| C7 | W, `finalize_task.py` returns `(1, "boom")` | exit 2; text holds `S6 was not closed: S6 manual half: finalize_task.py exit 1: boom` and a `door:` line; no marker; no code_only event |
| C8 | W, `c.stage_scope` patched to `{"derived": False, "scope": [], "reason": "x"}` | today's lines; py never called |
| C9 | C2 then `start` again | exit 0; exactly one code_only event for S6; text holds `completed already` |
| C10 | all dispositions `automate` + an accepted runner | today's lines (manual scope empty); py never called |
| C11 | W + an S6 dispatch left `running` | today's lines; py never called |

Existing rows that must stay green unchanged: K-R3..K-R5 (`:355-392`; no automation runner -> E1), K-P2 (`:395-421`), FV3-21b
S1-S7 (`:749-812`; no automation runner -> E1), `test_walk_lanes.py:298` (`_manual_block_door` signature unchanged), and the driver's
`test_story_run_s6.py` rows on `manual_close` (`:2583-2712`) and the S7 tests witness-for prints.

PROBE (byte copy, command hygiene point 7): (P1) in `_manual_block_check`, delete the X1 call of `_s6_manual_close` -> C1, C2 red;
(P2) in `stage_close.manual_half_close`, replace `road.consumer_need_record(...)` by `False` -> C1 red; restore from the copy,
witness = a hash comparison.

## 6. Readers of every touched file (designer rule 7)

Command (Grep tool, this round): pattern
`stage_close|story_step\.py|driver_stage_s6|driver_stage_s7|driver_dispatch|test_story_step_manual_block|phases/s6|consumer_need_record|manual_close|close_by_code|CONSUMER_ROUTES|_manual_block_check|file_passed_over`
over `tools/` = 16 hits in 2 files: `tools/controller-blocks-gen.py` (15; doc strings naming `story_step.py` doors: unchanged — no
door text of its table changes) and `tools/test_dispatch_gate.py:2302` (a prose sample naming `story_step.py`: unchanged). The wider
pattern adding `SIBLING_MAP|test-layers\.json` over `tools/` = 89 hits in 35 files: the readers of `test-layers.json`
(`test_quarantine.py`, `test_redundancy.py`, `source_split.py`, `lint_ratchet.py` and their tests) read the keep/quarantine
structure — a new `covers` entry: unchanged; the readers of `SIBLING_MAP.md` (`mechanism_gate.py`, `owns_readers.py`,
`tests/test_role_carriers_one_owner.py` axis 31, `claim_control_gate.py`, `handoff_gate.py` and others) read axis headings / axis 31 /
paths — an edited row inside axis 5: unchanged. Over `.githooks/` = 0 (positive control: `tools/` in the same folder = 21 hits in
4 files). Over `.claude/agents` = 8 hits, all prose (`designer.md:22, 96`, `critic.md:29, 189, 198, 227, 241, 261`): unchanged. Over
`.claude/skills` = 3 hits (`boot-diet/SKILL.md`, `critic-exam-gen/SKILL.md`), prose: unchanged.

Inside the package (the readers parallel streams meet at): the callers of the Driver methods keep the names (delegates); the census
(`judgment-census.json`) and the layer map (`driver-layers.json`) are read by `test_judgment_census.py` / `test_driver_layers.py`:
unchanged rows expected, run in the DoD; `_manual_block_check` callers: `start`, `test_story_step_manual_block.py`, the quarantined
`test_controller_scope_expansion.py:545-549` (not run, not edited); `_manual_block_door` caller `test_walk_lanes.py:298`: unchanged
signature. FV3-21 and FV3-21b own the same files on the same branch: this node is sequential after them (card r2 §4.5).

## 7. Siblings, analogs, and the named node FV3-21d

Sweep of the artifact (rule 9) — the S6 code steps the driver takes and the skill road lacks, by enumeration:

| driver site | skill road today | verdict |
|---|---|---|
| `s6.manual_close` (`manual_close`) | none | applied: this card |
| `s6.nothing` (`stage_S6` :523-534, no automate and no manual case) | none (`s6.md:5` "asks nothing", no close) | moved to node FV3-21d |
| `s6.results_stand` (freshness close, :541-574; promised by `s6.md:6, 76-79`) | none (the brief's analog a1) | moved to FV3-21d |
| `s6.accepted` (consumer record, no manual half, :516-522) | none: an automation-only story with a consumer cannot complete S6 on the skill road | moved to FV3-21d |
| `s6_reentry` / `s6_reprobed_close` (stale live checks proved by code, then close) | none | moved to FV3-21d |
| `s6_reprove_before_manual` (HF8-18, :607-608; promised by `s6.md:85`) | none: this card's close runs without the re-proof (fork F4) | moved to FV3-21d |

**Node FV3-21d** (same pile, sequential after FV3-21c; fork F4 decides its timing): "the skill road runs S6's other code steps by
the same code as the driver: nothing to execute, the results stand, the consumer's record closes an automation-only S6, the stale
live checks proved before the manual half and before the close". owns: `scripts/story_step.py`, `scripts/stage_close.py`,
`scripts/driver_stage_s6.py`, `scripts/tests/test_story_step_manual_block.py` (or the keep file its witness names),
`skills/qa-story/phases/s6.md`. Test row: a real story whose automated runs all stand fresh closes S6 code-only on the skill road
with no runner (`site s6.results_stand` reason), and an automation-only story whose runner awaits closes S6 after the analyst's
record. Its spec needs one scout question: "which `story_step` call is the skill road's entry to S6 for each of these sites, and
which of `s6_freshness` / `s6_changed` / `probe_by_code` are Driver-bound?".

Analogs noticed, not widened (rule 3):
- a1 (brief): `s6.md:6, 76-79` promise a freshness close only the driver writes — FV3-21d.
- a2: `s6.md:85` promises the re-proof before the manual half — driver only — FV3-21d.
- a3: neither `s6.md` nor `s7.md` tells the skill road that S6 awaits the analyst or how the analyst's record is taken (the
  analyst's brief carries the awaiting author, `story_step.py:334-335`; whether its `finish` records the acceptance of S6 on the
  skill road was NOT verified this round). K5.i adds the S6 half; the S7 half is a question to the Lead (§8 Q-a3).
- a4: the per-case word loop exists in the driver (`manual_no_stand`, `driver_stage_s6.py:1388-1396`) and in `story_step`
  (FV3-21b) — accepted in r2; K5.e factors the skill-road copies into one helper, the driver's loop is untouched.
- a5: `story_progress` has no "awaiting the consumer" position for either road (grep `await|consumer`, case-insensitive, over
  `story_progress.py`: 1 hit, the gate's `await_gate`, `:529`) — fork F3.

## 8. Forks (recommendation first)

**F1 — where the one survivor lives.** (a, recommended) move the bodies into `scripts/stage_close.py` over a road (§2.1); Driver
delegates; `stage_close.SkillRoad` for the skill road. Cost: ~300 lines moved/added, a critic pass (diff over 100 lines).
(b) call the Driver's mixin methods unbound over a duck object from `story_step` — no move, but `story_step` imports
`driver_stage_s6`/`driver_stage_s7`/`driver_dispatch`: three new `allowed_importers` rows, a raise of a shrink-only ratchet
(`driver-layers.json:5-8`, AR-20). (c) a one-step driver mode the skill road shells out to — no such mode exists, and it is one more
command for the conductor (FR-48).

**F2 — which call carries the close.** (a, recommended) `start --execution-kind manual` at the exits X1-X3 (§2.2). (b) a new
`story_step.py close-manual --task <T>` subcommand plus a card line — a command the orchestrator must remember (the gap's own shape).
(c) `where` — read-only by contract.

**F3 — the progress line in the awaiting world.** (a, recommended) add a position kind `awaits` to `story_progress.progress` for the
current stage when `acceptance.awaits_acceptance` names an author (the one reader), words `waiting for the <who>'s acceptance
(<consumer stage>)` from `stage_close.CONSUMER_ROUTES`; both roads, S6 and S7 (axis 5); owns + `scripts/story_progress.py`, a row in
`test_story_step_manual_block.py` (it already imports `story_progress`, `:31`; `test_story_progress.py` is quarantined,
`test-layers.json:10103`). Cost: ~15 lines + one row. (b) keep `no role running`, as the driver's awaiting state shows today; one
finding in the pile of the progress line.

**F4 — the re-proof and the other S6 code steps (FV3-21d).** (a, recommended) FV3-21d is a named node (§7) after FV3-21c; until it
lands, the skill road's manual close runs without the HF8-18 re-proof — the skill road never re-proved; today it cannot close at all.
(b) fold FV3-21d into this card — needs its scout question first and roughly doubles the node.

**F5 — one builder node or two.** (a, recommended) FV3-21c-1 (the move: K5.a-K5.d; witness = the driver's own tests unchanged) then
FV3-21c-2 (the road: K5.e-K5.j), sequential on one branch, ONE critic pass for the topic after the second. (b) one node.

Questions to the Lead:
- Q-a3: is the analyst's acceptance of S6 taken on the skill road today (who runs `stage_done --acceptance` for S6 from the analyst's
  form)? If not, FV3-21d (or a node of its own) carries it; FV3-21c's awaiting world depends on it for its second half.

## 9. Small choices the designer closed (the Lead can stop any)

- The module name `stage_close.py` (a glob of `scripts/*close*` finds none in `scripts/`, only five tests; control: the same glob
  form `scripts/*stage*` finds `stage_done.py` and six driver/stage modules).
- `Refused(Exception)` with `title`, converted once in the four Driver delegates; no Driver attribute is added (driver-layers rows).
- `CONSUMER_ROUTES` split: data in `stage_close`, the driver-only `rework_complete` lambda added by the Driver.
- `SkillRoad` lives in `stage_close.py`, not in `story_step.py` (the module both roads import; `story_step` imports it inside the
  function, as its other lazy imports).
- `SkillRoad.py` treats a missing script as exit 127 (never `_run`'s "skipped" success): a close must not pass over a reducer that
  did not run (AR-28).
- The person's pass on the skill road is recorded with `--acceptor driver` (`acceptance.DRIVER_ACCEPTOR`): one record form, read
  by `consumer_close_words` and `accepted_for` as today; the name says "code acceptor", not "the driver process".
- Exit 0 for both the closed and the awaiting outcome (sanctioned states with a printed move); exit 2 for a refused close.
- The plan runs only when the automated half is settled (E1), so every existing skill-road row keeps its world.
- `stage_close.py` gets `covers` entries in two keep rows instead of a test file of its own (a new case is a table row).
- The SIBLING_MAP edit rides the builder's commit with `axes: not a mechanism (...)`.

## 10. Reading trail

Read this round (worktree): card r2 §4 (:520-620), §11-§12 and the Lead's decisions (:770-854); `story_step.py` 112-165, 326-347,
700-758, 889-928, 995-1126, 3290-3439 + import grep; `driver_stage_s6.py` 130-354, 501-615, 918-977, 1015-1089, 1290-1414,
1625-1664, 1970-1993; `driver_stage_s7.py` 755-814; `driver_dispatch.py` 2525-2584; `driver_runner.py` 380-405;
`controller.py` 933-972, 3970-3999, 5110-5145, 6020-6089, 9236-9275; `acceptance.py` 1390-1569; `stage_done.py` 975-1060, 1215-1270;
`story_progress.py` 365-401, 463-519, 520-587, 600-672; `manual_evidence.py` 1280-1339; `skills/qa-story/phases/s6.md` (whole);
`s7.md` 5-34; `scripts/tests/test_story_step_manual_block.py` 1-118, 355-421, 745-841; `scenario_walk.py` 834-924;
`test-layers.json` 6174-6193, 6360-6373; `driver-layers.json` 1-12 + row grep; `judgment-census.json` 1-14 + row grep;
`design/architecture.md` 160-294; `docs/SIBLING_MAP.md` axis 5 rows (:116-145, cut at 220 chars) and axis heads.
Greps (Grep tool): `code_only|code-only` count over `scripts/*.py`; the Driver method names over `scripts/tests/fixtures` and
`test_story_run_s6.py`; `execution-kind|_manual_block_check|_manual_block_door` over `scripts/*.py`; `awaits_acceptance|
acceptance_awaits|AWAITS_WORD` over controller/acceptance/stage_done/story_step; `DRIVER_ACCEPTOR`; `^(import|from)` over the
modules `stage_close` will import (none imports `story_step` or `driver_*`; control: the same call with `waiver|hooklib` added finds
`acceptance.py:11`, `driver_core.py:13-18`, ...); the rule-7 reader greps of §6.

Negative claims and their controls:
- "story_step writes no `code_only`" — count grep lists 21 scripts without it; control in the same call: `stage_done.py:1`,
  `story_progress.py:7`.
- "the driver never runs `start --execution-kind manual`" — the only driver hit is `driver_dispatch.py:666` (`automation`); control:
  the same grep finds `story_step.py:1023`.
- "no module stage_close.py exists" — `scripts/*close*` glob: tests only; control: `scripts/*stage*` finds `stage_done.py`.
- "the modules stage_close imports import no story_step/driver_*" — empty for `story_step|driver_` on that file set; control with
  `waiver|hooklib` added: 11 hits.
- "story_progress has no awaiting position" — case-insensitive `await|consumer` over `story_progress.py`: only `:529` (the gate).
- "test_story_progress.py, test_refuse_case.py, test_controller_scope_expansion.py are quarantined" — rows at `:10103`, `:9414`,
  `:7750`, after `"quarantine": {` (`:7208`); `test_story_step_manual_block.py` (`:6360`), `test_story_run_s6.py` (`:6174`),
  `test_walk_lanes.py` (`:6642`) before it (keep).
- `.githooks/` reader count 0 — control `tools/` in the same folder: 21 hits.

## 11. Brief contradictions noticed

- The dispatch's `node:` line says `live-run-fvf/3/FV3-21`; the brief's own text and card r2 §4.5 name this node FV3-21c. The
  card uses FV3-21c; the Lead fixes the node id in the pile file.
- The brief's handoff path names `fv3-21c` while the scout recon said `start --stage S6 --execution-kind manual` "prints only" at
  `:1094-1111`: re-checked — it prints AND exits 2 via `start` (`:913-916`).
- The brief's test row ("the automation runner accepted not-complete and every manual case refused -> reduces and awaits the
  analyst") is C1; it holds only with the automated half settled — the precondition the driver has (`:513-515`), stated here as E1.

## Lead decisions (17.11.2026, Opus Lead — «решила сама», until the owner's word)

- Node ids: this card is batch-3 node **FV3-22**; FV3-21d below is node **FV3-24** (row added with this decision).
- F1 = (a): `scripts/stage_close.py` holds the bodies over a road; Driver delegates; `stage_close.SkillRoad` for the skill road.
- F2 = (a): `start --execution-kind manual` at the exits X1-X3 carries the close; no new subcommand.
- F3 = (a): position kind `awaits` in `story_progress.progress`, both roads, S6 and S7.
- F4 = (a): the HF8-18 re-proof and the other S6 code steps go to FV3-24 (FV3-21d), after FV3-22.
- F5 = (a): two builder nodes on one branch, FV3-22-1 (the move, K5.a-K5.d) then FV3-22-2 (the road, K5.e-K5.j); one critic pass after the second.
- Q-a3: the analyst's acceptance of S6 on the skill road belongs to FV3-24 in either case. FV3-22 ends at the awaiting state; if FV3-24's
  scout finds the acceptance already taken on the skill road, that item closes there as n/a with its trail.
- Before any builder: a critic on this plan (new module, moved bodies over 100 lines).
