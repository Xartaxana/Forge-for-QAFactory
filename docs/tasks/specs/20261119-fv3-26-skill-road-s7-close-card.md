# FV3-26 — the skill road closes S7 by code: first step `s7.no_failures` (designer draft, t-1589)

Node `live-run-fvf/3/FV3-26`, feature F19. Model: card r2 of FV3-22 (`docs/tasks/specs/20261117-fv3-21c-skill-road-s6-close-card-r2.md`):
one body in `scripts/stage_close.py`, the Driver delegates, the skill road reaches the same body through `stage_close.SkillRoad`
from the stage's own `story_step.py start`. P = `ai-packages/qa-factory/scripts`. Line numbers were read on `main` at c1ac526f;
the builder re-reads each on the merged head (§0). Forks for the Lead: §8. The cards follow the recommendations.

## 0. Merge-time facts (builder re-checks on its start head; a shift is reported, any other difference = STOP and ask)

| # | fact (read at c1ac526f) | what the card builds on it |
|---|---|---|
| MF1 | FV3-29 (t-1588) has MERGED: `SkillRoad.record_close` binds each `log_append.py` tail result and prints a `note:` line on a failure (the form is FV3-29's; the builder quotes it). Today (P/stage_close.py:407-408) the result is dropped | E5. FV3-26-1 does not start before FV3-29 merges (both edit `stage_close.py`) |
| MF2 | `Driver.stage_S7` no-failures branch P/driver_stage_s7.py:97-110: `failures_to_triage` -> `s7_close_places(s7_gap_reason("no_failures"))` -> `s7_investigation_gate()` (`wait` returns) -> register -> `close_by_code("S7", "no failures — nothing to triage"+suffix, ["work/run-report.json"]+register, site="s7.no_failures", finalize=False, tail=[dispatch_skipped row])` | K1-K3 move it |
| MF3 | `Driver.failures_to_triage` :17-60 reads only `self.task_root` (via `driver_core._read_json` = `hooklib.read_json(path, {})`, driver_core.py:307-310); `test_s7_null_outcome.py:704,769,787` call it UNBOUND on `SimpleNamespace(task_root=...)`; `test_no_move_seam_sites.py:664,714` stub it on a driver | K1 delegate shape, E-M2 |
| MF4 | `s7_investigation_gate` :879-944 reaches `self.controller_state()`, `self.plugin` (driver_core.py:448: `--plugin-dir` or `HERE.parent`), `self.task_root`, `self.pipeline()`, and in its `dispatch` branch `self.run_role` / `self.role_lines` | K2 split |
| MF5 | `driver_dispatch.py:663-667`: the driver's `run_role` runs `story_step.py start --task T --stage S --role R [--scope] [--purpose]`; for the S7 analyst it is reached only with failures to triage or with S6 awaiting its consumer (driver_stage_s7.py:97-170) | E9, F5 |
| MF6 | today's hand close is refused: `stage_done.py --status done` on a controller-managed stage the controller has not completed exits `EXIT_BAD_ARGS` (P/stage_done.py:1256-1281); no skill-road code writes an S7 `code_only` (Grep `pretriage|investigation|place_answers` -i over story_step.py: 0 hits; positive control: the same call counts `_s6_manual_close`, 6 hits) | §1.1 defect |
| MF7 | controller `code_only` projection (controller.py:1949-1961): `stages[S7] = {status: completed, code_only: True, reason, receipt_id}`, plus `passed_over` and `superseded` rows; the S7 receipt is allowed (validate :6138) and judged by `code_close_conflicts` (:944-966: running, behind, completed); a `code_only` event of S6/S7 triggers `finalize_task.refresh` (:5025-5029) | E1, E3, §2.3 |
| MF8 | before any edit the DoD commands run once on the start head; reds there are listed as inherited | own reds told from inherited |

## 0.1 Dispatch header — FV3-26-1 (the move; driver behaviour unchanged)

task: <new id>
node: live-run-fvf/3/FV3-26
feature: F19
given:
C:/QAFactory/forge-repo/docs/tasks/specs/20261119-fv3-26-skill-road-s7-close-card.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/architecture.md
C:/QAFactory/forge-repo/docs/TESTING.md
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/stage_close.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_s7.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_s7_null_outcome.py
non-goals: SkillRoad and story_step (FV3-26-2); s7.pretriaged / s7.accepted / s7.after_repairs / s7_await_scribe / the extra-instance step bodies (§7 nodes); A27 widening (FV3-29 follow-up); S9; any quarantined test (test_place_driver.py, test_s7_investigation_driver.py, test_manual_observations.py, test_place_session.py, test_stage_acceptance_consumer.py: not run, not edited)
handoff: the diff on the branch + builder report (MF1-MF8 with lines, AR lines, narrow-call output, "not run locally: test_story_run_s7.py, canon judges", "ratchets raised: none")
edges: card §4 rows E-M1..E-M5, each with its invariant
DoD: `python -B -c "import sys;sys.path[:0]=['ai-packages/qa-factory/scripts/tests','ai-packages/qa-factory/scripts'];import test_s7_null_outcome as t;t.one_definition_no_local_set_building()"` plus the same narrow call of the `test_s7_null_outcome.py` functions holding :704/:769/:787, of the `test_no_move_seam_sites.py` function holding :654-714, of `test_driver_layers.py`'s home check, and of the `s7.no_failures` rows of `test_story_run_s7.py` (each named in the report; all five files are canon class: slow_tests.json / canon_only)
siblings: axis 5 row "Code-only stage closes" (SIBLING_MAP:130), text edited in FV3-26-2
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261119-fv3-26-skill-road-s7-close-card.md
test: test_s7_null_outcome.py::one_definition_no_local_set_building - the sentinel tuples gain `(scripts/"stage_close.py", {"s7_failures_to_triage"})` in both scans | expected from: card K1, AR-13 (the moved body stays under the triage-set sentinel)
test: none -- поведения нет: тела переносятся, драйвер ведёт себя как прежде; держат строки s7.no_failures в test_story_run_s7.py (канон) и узкие вызовы выше | expected from: card §2.1, E-M1

## 0.2 Dispatch header — FV3-26-2 (the skill road; sequential after FV3-26-1, same branch)

task: <new id>
node: live-run-fvf/3/FV3-26
feature: F19
given:
C:/QAFactory/forge-repo/docs/tasks/specs/20261119-fv3-26-skill-road-s7-close-card.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/architecture.md
C:/QAFactory/forge-repo/docs/TESTING.md
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/story_step.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/stage_close.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_story_step_manual_block.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test-layers.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/skills/qa-story/phases/s7.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/skills/qa-story/SKILL.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/changelog.d/fv3-26-skill-road-s7-close.md
C:/QAFactory/forge-repo/docs/SIBLING_MAP.md
non-goals: the driver modules (FV3-26-1 is done; a needed driver change is a question); s7.pretriaged, s7.accepted, s7.after_repairs, the extra-instance step, S9 (§7); stage_done.py's refusal text (F6); quarantined tests
handoff: the diff + builder report (AR lines, narrow-call output, the `in N.NNs` tail of the new function, the last 5 lines of `story_step.py card --stage S7`, the byte-copy hash of any probe)
edges: card §4 rows E1-E14, each with its invariant
DoD: `python -m pytest "ai-packages/qa-factory/scripts/tests/test_story_step_manual_block.py::test_fv3_26_nothing_to_triage_closes_s7_on_the_skill_road" "ai-packages/qa-factory/scripts/tests/test_story_step_manual_block.py::test_fv3_22_nothing_left_closes_s6_on_the_skill_road" -q` plus `python -B ai-packages/qa-factory/scripts/story_step.py card --stage S7` (no `over` note) plus a narrow call of `test_judgment_census.py`'s census check (canon class)
siblings: axis 5 rows "Code-only stage closes" (:130) and "Skill phase <-> driver" (:133); axis 34 via §7 nodes
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261119-fv3-26-skill-road-s7-close-card.md
test: test_story_step_manual_block.py::test_fv3_26_nothing_to_triage_closes_s7_on_the_skill_road row T1 (close: one S7 receipt, the record, the tail row, the S8 next line, no dispatch) | expected from: card §2.3, K5, E1
test: the same function, row T2 (a failure in the report -> today's dispatch of the analyst, no receipt) | expected from: card K5 step 7, E8
test: the same function, rows T3, T3b (re-entry: completed line; record missing -> E9 door, exit 2) | expected from: card K6, E3
test: the same function, row T4 (stage_done refused -> refusal + door, receipt stands, exit 2) | expected from: card E4
test: the same function, row T5 (S6 awaits its consumer -> no close, today's dispatch) | expected from: card E7
test: the same function, rows T6, T6b (investigation pass running -> no close; a pass owed -> no close, the investigation start on the next line) | expected from: card K3, E10, E11
test: the same function, row T7 (a counting need row -> no close, exit 2, door) | expected from: card E12, F2
test: the same function, row T8 (a halted run report / no run-report.json -> refusal with the driver's text, exit 2) | expected from: card E6, F4
test: the same function, row T9 (a tail row fails -> `note:` line, exit 0, record stands) | expected from: card E5, MF1
test: none -- документ: s7.md / SKILL.md / SIBLING_MAP / changelog; свидетель — вывод `card --stage S7` без `over` | expected from: card K7, K8

The builder writes the test rows top-down until test lines reach code lines and reports the rest as `tests not written: <row> -- over budget`.

**Live proof (FR-33).** One line for the batch's «Живые доказательства»: a skill-road story whose S6 run is green reaches S8 after
one `start --stage S7 --role qa-failure-analyst`, with an S7 `code_only` receipt and its record; no analyst ran.

## 1. Defect, scope, AR-n, owners, census, variety

### 1.1 Defect

On the skill road S7 closes only by prose: s7.md card line 14 and Entry check (:43-45) tell the conductor, with nothing to triage,
to "record `S7.status: done`" by `stage_done.py` by hand (Exit :26, SKILL.md:194). That record is refused: the controller holds no
completed S7 (MF6), and the only door in the refusal is a person's waiver of "no accepted controller stage". The driver closes the
same world by code at `s7.no_failures` (MF2). So a skill-road story with nothing to triage can never complete S7 by its own road
(scout q2d-q2h; P31 / axis 34 residual of card r2 fork R2-F3).

### 1.2 Scope

This node: the close at `s7.no_failures` only, by the driver's body moved to `stage_close` (K1-K4), carried on the skill road by the
stage's own `start` (K5-K6), and s7.md loses the hand line for that world (K7). The other S7 sites are named nodes (§7), so the
slice is no exclusion (designer rule 6). S9 follows only when this node lands green (Lead decision 19.11).

### 1.3 AR-n touched and the change check each demands

| AR | how kept | change check in the DoD / report |
|---|---|---|
| AR-13 | one definition each: `stage_close.s7_failures_to_triage`, `s7_close_places`, `s7_investigation_gate`, `gap_reason_text`; the Driver keeps delegates of the same names and homes | report: Grep `def failures_to_triage|def s7_close_places|def s7_investigation_gate` over P/*.py (not tests) = delegates only in driver_stage_s7.py, bodies only in stage_close.py; the triage-set sentinel scans stage_close (test line of -1) |
| AR-15 | one survivor of the S7 no-failures close, both roads; story_step copies no step | report greps the PROBLEM: `"dispatch_skipped"`, `close_unsettled`, `investigation.decision` over P/*.py; each hit is the survivor, a delegate, or a §7 site |
| AR-14 | writers unchanged: receipt by `close_receipt` -> controller `code_only`; record by `stage_done.py`; register lines by `place_answers` / `investigation` only | Grep: no `atomic_json` / `write_text` added in the story_step.py diff |
| AR-17 / FR-48 / P3 | the close runs inside the conductor's existing `start`; no new command, stop or question | Grep the diff: no new `Person`, `no_move`, `ask` site |
| AR-18 | `stage_close.py` stays outside A27 (FV3-29 follow-up). Every `road.py(` / `self.py(` in the moved bodies binds its result or uses `check=True` | grep output attached to the -1 report |
| AR-19 | S6/S7 twins: the skill road's S6 close (FV3-22) and S7 close share `close_by_code`, the re-entry reader and the E9 door builder | report names the twin call sites |
| AR-20 | no ratchet raised; existing driver-layers rows stand; a row is added only for a NEW Driver member the layer test demands (`Driver.s7_investigation_dispatch`) | report "ratchets raised: none; rows added: <names>" |
| AR-21 | `finalize=False` as the driver: the receipt hashes the report S6 left; a completed S7 is never closed again (`close_by_code` reads state first; K6) | rows T1, T3 |
| AR-22 | the S7 `code_only` receipt and S7 record gain a skill-road producer (K5); readers unchanged (§6) | report lists readers of `code_only` for S7 |
| AR-23 / FR-23 | "nothing to triage" is a recorded completed state, never an escalation | row T1 |
| AR-25 / AR-9 | every no-close outcome prints a door the receiver can run (E3b, E4, E6, E10-E12) | rows T3b, T4, T6, T7, T8 |
| AR-27 | passed-over work filed by `file_passed_over`; unsettled places gapped before the close | row T1 (place gap via the moved body) |
| AR-28 / FR-59 | unreadable state, a live S7 dispatch, a halted report, an unread need -> no close and no "closed" line | rows T6, T7, T8; E2 |
| AR-29 | §1.4 | narrow census call green; a new unit or a changed class -> builder STOPS and asks |
| AR-2 | the investigation itself, its targets and verdicts stay the analyst's; code only decides "a pass is owed" (`investigation.decision`, unchanged) | report: "what the role still decides" line |

Commit lines: an `architecture:` line naming AR-2, AR-9, AR-13, AR-14, AR-15, AR-17, AR-18, AR-19, AR-20, AR-21, AR-22, AR-23,
AR-25, AR-27, AR-28, AR-29, and a `judgment:` line, both in the form `tools/architecture_gate.py` carries (the one carrier; not
copied here). Recommended `judgment:` content: `none -- every check added or moved judges data (report targets, dispatch states,
stage status, record presence, register rows); the triage and the investigation stay the failure analyst's`. The SIBLING_MAP edit
rides FV3-26-2's commit with `axes: not a mechanism (<reason>)` (`tools/mechanism_gate.py`): it records the survivor of an existing
twin row.

### 1.4 Checks added or moved — owner and census class (AR-29, P27)

| check | where | owner | class | census unit? |
|---|---|---|---|---|
| CK1 nothing to triage (report targets, contradicts rows) | `stage_close.s7_failures_to_triage` (moved) | data | xref | no: name outside `UNIT_NAME_RE` (test_judgment_census.py:77); raises `stage_close.Refused` (not ValueError) |
| CK2 places nobody settled -> gaps | `stage_close.s7_close_places` (moved) | data; the settle answers are the analyst's (judgment) | shape | no (returns list) |
| CK3 investigation owed / running / none | `stage_close.s7_investigation_gate` (moved; decision stays `investigation.decision`) | data; the pass is the role's judgment | xref | no (returns tuple) |
| CK4 the skill close applies (stage, role, no purpose, not completed, no analyst accepted, S6 not awaiting, `code_close_conflicts` empty) | `story_step._s7_code_close` (new) | data | shape | no (name outside the regex) |
| CK5 re-entry: completed by code -> record read | `story_step._code_close_reentry` (generalized `_s6_reentry`) | data | shape | no |
| CK6 a counting need row -> no close (F2 a) | `story_step._s7_code_close` step 8 via `manual_evidence.unprepared_rows` | data; the answer is the person's (intent) | shape | no |

### 1.5 Variety walk (architecture.md § A)

- axis 7: held by registry -- the another-instance answer per stand (`project_knowledge.instance`); unknown value -> no close on the skill road, door to the card's question (F2 a; the driver asks)
- axis 8: held by table -- host forms; the close runs in `story_step` on Claude and Codex alike; unknown host -> same code path (no host read)
- axis 9: held by role -- who answers stays the conductor's question road; code adds no question
- axes 1, 2, 3, 4, 5, 6, 10, 11, 12, 13: n/a -- the change moves an S7 close between roads; it reads no product, surface, stack, source, delivery, language, size, check-kind or age value

## 2. The design

### 2.1 What moves into `stage_close.py` (FV3-26-1)

Same rules as card r2 §2.1: bodies MOVED verbatim, `self` -> `road`, `raise Refusal(` -> `raise Refused(`, every sub-step through
`road.<member>` of the same name as the old `self.<member>` (stub invariant), package imports inside functions, no `driver_*` import.

| name | moved from | notes |
|---|---|---|
| `s7_failures_to_triage(task_root, awaiting="") -> str` | `Driver.failures_to_triage` :17-60 | reads `hooklib.read_json(task_root/"work/run-report.json", {})` (the `_read_json` semantics, MF3); the entry refusal text unchanged, raised as `Refused`. Delegate: `try: return stage_close.s7_failures_to_triage(self.task_root, awaiting) except stage_close.Refused as exc: raise Refusal(str(exc), title=exc.title) from None` (works on `SimpleNamespace(task_root=)`, MF3) |
| `gap_reason_text(name) -> str` | the lookup half of `Driver.s7_gap_reason` :800-817 | `place_answers._data()["gap_reason_names"][name]`; any exception -> the same printed line, `""`. `Driver.s7_gap_reason` keeps its `s7_walk` read (driver state) and calls it for the text |
| `s7_close_places(road, why) -> list` | `Driver.s7_close_places` :819-838 | reads `road.task_root` only |
| `s7_investigation_gate(road) -> tuple` | `Driver.s7_investigation_gate` :879-926 | `investigation.load_budget(road.plugin)`; the `dispatch` branch becomes `return road.s7_investigation_dispatch(targets, budget)` |
| `s7_code_close(road, kind) -> str` | the shared tail of driver_stage_s7.py:102-110 | `kind == "no_failures"` only in this node (§7 adds `pretriaged`): `road.s7_close_places(gap_reason_text(kind))`; `verdict, suffix = road.s7_investigation_gate()`; `wait` -> return `"wait"`; `dispatch_owed` -> return `"dispatch_owed"`; register = `["work/exploratory-findings.jsonl"]` when that file exists; `road.close_by_code("S7", "no failures — nothing to triage" + suffix, ["work/run-report.json"] + register, site="s7.no_failures", finalize=False, tail=[["--event", "dispatch_skipped", "--task", road.task, "--reason", "S7: no failures to triage"]])`; return `"closed"` |

Driver side (driver_stage_s7.py): `failures_to_triage`, `s7_close_places`, `s7_investigation_gate` become delegates; new member
`s7_investigation_dispatch(targets, budget) -> (verdict, suffix)` = today's :927-944 verbatim (run_role, close_gaps, counts; returns
`"dispatched"`). `stage_S7` :99-110 becomes: `if not reasons and not awaiting:` -> `self.s7_code_close("no_failures")` -> `return`,
where `Driver.s7_code_close(kind)` is a delegate with the one `Refused` -> `Refusal` conversion. A driver `Refusal` raised by a
Driver member inside passes untouched with its `retry` / `close` (card r2 §2.1).

### 2.2 Which skill-road command carries it (F1 = a, recommended)

`story_step.py start --task T --stage S7 --role qa-failure-analyst` (no `--purpose`): the call the card already gives the conductor
for S7. When code finds nothing to triage, the same call closes S7 instead of dispatching. Why: code decides "nothing to triage" on
the stage's own transition (FR-48, P3); the conductor stops reading `run-report.json` totals to choose a road; `where` and `card`
stay read-only. No mode gate (F5 = a): on the driver road `run_role` reaches this `start` only with failures or with S6 awaiting
(MF5), where step 4/7 returns None.

### 2.3 What the person and the conductor see after

| world | `start` prints, in order; exit | `story_progress` / `where` |
|---|---|---|
| closed (T1) | captured module lines (place gaps, investigation notes, `note:` lines); `S7 is closed by code: no failures — nothing to triage<suffix>`; `next: python "${CLAUDE_PLUGIN_ROOT}/scripts/story_step.py" card --stage S8`; exit 0 | S7 done with its reason (`story_progress._code_only`, :592); S8 current, no dispatch |
| investigation running (T6) | captured lines incl. `S7: the investigation <id> is running; S7 is not closed over it`; `next: the investigation dispatch is still running: python "${CLAUDE_PLUGIN_ROOT}/scripts/story_step.py" where --task T; after it ends run this same start again: it closes S7`; exit 0 | unchanged |
| investigation owed (T6b) | captured lines; `S7: <n> observation(s) the run left open are not investigated; one bounded read-only investigation is owed`; `next: python "${CLAUDE_PLUGIN_ROOT}/scripts/story_step.py" start --task T --stage S7 --role qa-failure-analyst --purpose investigation (bind, finish --not-complete as the card's section Investigation says); then run this same start again: it closes S7`; exit 0 | unchanged |
| re-entry, record written (T3) | `S7 is completed already: nothing is closed again`; `next: python "${CLAUDE_PLUGIN_ROOT}/scripts/story_step.py" card --stage S8`; exit 0 | unchanged |
| re-entry, record missing (T3b) | `story_step: refused - S7 is completed in the controller but its stage record is not written`; `stage_close.record_door(T, "S7", ["--status","done","--digest",<reason>,"--no-journal"])`; exit 2 | unchanged |
| refused close (T4, T8) | captured lines; `story_step: refused - S7 was not closed: <text>`; the door line (E4/E6); exit 2 | unchanged |

The print order is the real order: the module calls run under `contextlib.redirect_stdout`, as `_s6_manual_close` does
(story_step.py:1240-1250).

## 3. Items

### FV3-26-1
- **K1** `stage_close.py`: `s7_failures_to_triage`, `gap_reason_text`, `s7_close_places` (§2.1); the module docstring's road-member
  list gains `plugin`, `failures_to_triage(awaiting)`, `s7_close_places(why)`, `s7_investigation_gate()`, `s7_investigation_dispatch(targets, budget)`.
- **K2** `stage_close.py`: `s7_investigation_gate(road)`; driver_stage_s7.py: delegate + new `s7_investigation_dispatch`.
- **K3** `stage_close.py`: `s7_code_close(road, kind)`; driver_stage_s7.py: `stage_S7` :99-110 -> the delegate `s7_code_close`.
- **K4** homes: driver-layers.json rows for `Driver.s7_investigation_dispatch` and `Driver.s7_code_close` (home `driver_stage_s7`,
  note "FV3-26: delegate of stage_close") only if `test_driver_layers.py` demands them; existing rows (:677, :698, :728, :729,
  :746) stand. test_s7_null_outcome.py: the sentinel rows (test line of -1).

### FV3-26-2
- **K5** `story_step.py`, new `_s7_code_close(args, controller, state) -> tuple | None`: `(lines, code)`, or None = not applicable
  (today's lines). Its docstring names FV3-26, P31, the driver site `s7.no_failures` and its ERROR DIRECTION (a gate that closes S7:
  it may err only toward None or a refusal). Steps, in order:
  1. `args.stage == "S7"`, `args.role == "qa-failure-analyst"`, no `--purpose`; else None.
  2. S7 `completed` in `controller.state()` -> K6 (`code_only` -> its lines; a role's completion -> None, today's lines).
  3. any S7 author dispatch `accepted` (`acceptance.author_dispatches(state, acceptance.stage_def_of("S7"))`, the driver's reader :70) -> None.
  4. `acceptance.awaits_acceptance(state, "S6", <pipeline>)` names an author -> None (the analyst is let in for S6; E7).
  5. `controller.code_close_conflicts(state, "S7")` non-empty -> None (a live S7 dispatch, S6 behind; the one predicate, AR-13).
  6. `road = stage_close.SkillRoad(args.task, task_root, controller)`; `reasons = road.failures_to_triage("")`; `Refused` -> E6 lines, exit 2.
  7. `reasons` non-empty -> None (today's dispatch; pre-triage = FV3-26b).
  8. a counting need row (`manual_evidence.unprepared_rows(report)` with `need`) -> E12 lines, exit 2 (F2 = a).
  9. under captured stdout: `verdict = stage_close.s7_code_close(road, "no_failures")`; `Refused`, `StateConflict`, `ValueError` ->
     the refusal lines as `_s6_manual_close` builds them (:1244-1249, `text.rpartition("\ndoor: ")`), exit 2; else the §2.3 lines.
- **K5b** `start` (story_step.py:896-933). POSITION: after the FV3-41 S6 re-entry block (:920-929), before `_manual_block_check`
  (:930). `_s7_code_close` not None -> print its lines, return its code. POSITIONAL INVARIANT: after the run-mode switch refusal
  (:911-915), so a refused switch writes nothing; before `stamp_run_mode` (:934), `_pre_work`, `judge_results --triage`,
  `controller.prepare` and `apply("dispatch")`: a close registers no dispatch, brief, card, stamp or judge file; a call whose
  steps 1-7 return None reaches today's code byte for byte.
- **K5c** `SkillRoad` members: `plugin = Path(__file__).resolve().parent.parent` (= the driver's default, MF4);
  `failures_to_triage(awaiting="")` = `s7_failures_to_triage(self.task_root, awaiting)`; `s7_close_places(why)`;
  `s7_investigation_gate()`; `s7_investigation_dispatch(targets, budget)` prints the "owed" line (§2.3) and returns
  `("dispatch_owed", "")`. No member is copied from the Driver.
- **K6** `story_step._s6_reentry` -> `_code_close_reentry(task, task_root, controller, held, next_line, stage)`; the two callers
  (S6 :925, :1213) pass `"S6"`; K5 step 2 passes `"S7"` and the `card --stage S8` next line. Text per stage: `<stage> is completed
  already: nothing is closed again`, the refused line with `<stage>`, `record_door(task, stage, ...)`. `record_door`'s docstring
  names the new reader.
- **K7** `phases/s7.md`: card line 14 from "Nothing to triage = ..." to the end of that sentence group becomes: `Start the analyst
  by the commands below: when nothing is left to triage (no failed test, no manual check that failed or was inconclusive, no
  observation, no `contradicts_requirement` row), the same \`start\` records the unsettled places as gaps, runs the investigation step and
  closes S7 by code, then prints the S8 card; it dispatches no analyst.` Line 26: drop "(nothing to triage: no role ran it, drop
  `--role`)". Entry check :43-45: "With none of those -> `start` closes S7 by code (section Investigation runs inside it) and
  journals `dispatch_skipped`; nothing is recorded by hand." Section Investigation :271-273 and places :108-109: the
  "nothing to triage" point is run by `start`; the hand steps stay for the other two points until §7 nodes. The card stays under
  `CARD_MAX_BYTES` 4000 (story_step.py:3380): witness `card --stage S7` with no `over` note.
- **K8** SKILL.md:194 "(S0, S7 with nothing to triage)" -> "(S0)". `changelog.d/fv3-26-skill-road-s7-close.md` (ASCII): the
  skill road's `start` of the S7 analyst closes S7 by code when nothing is left to triage, by the driver's code; the hand record is
  gone. SIBLING_MAP :130 names `stage_close.s7_code_close` and its two roads; :133 one clause. test-layers.json: `"stage_close.py"`
  already in the covers of test_story_step_manual_block.py (FV3-22 K5.m) - the builder confirms, adds nothing else.

## 4. Edges (each with the invariant it protects)

### 4.1 FV3-26-1 (move)
| id | edge | behaviour | invariant |
|---|---|---|---|
| E-M1 | every driver S7 world | identical calls, prints and refusals; `close_by_code` reached through `road.close_by_code` (a stub on the Driver keeps its effect) | the driver's S7 no-failures close is unchanged byte for byte |
| E-M2 | `failures_to_triage` called unbound on a namespace with only `task_root` (MF3) | works | the delegate reads nothing but `task_root` |
| E-M3 | `investigation.load_budget` fails / project raises / decision raises | the same printed lines and `("proceed","")` as today | an investigation fault never blocks a close and never reads as "investigated" |
| E-M4 | gap text unreadable | `""` + the same printed line; `close_unsettled` refuses, `s7_close_places` prints one line | the close still runs; a place is never both gap kinds |
| E-M5 | a refusal raised by a Driver member inside the moved body (`run_role` in `s7_investigation_dispatch`) | passes untouched (retry/close kept) | only `stage_close.Refused` is converted, once |

### 4.2 FV3-26-2 (skill road)
| id | edge | behaviour | invariant |
|---|---|---|---|
| E1 | nothing to triage, all guards pass | §2.3 closed row; exit 0 | a skill-road S7 with nothing to triage completes by the driver's body; no analyst is dispatched |
| E2 | `controller.state()` or the pipeline unreadable (raises) | step reads that raise -> None for steps 2-5; a `StateConflict`/`ValueError` inside step 9 -> refusal, exit 2 | an unreadable state never yields a "closed" line (AR-28) |
| E3 | S7 completed already (re-entry, by code) | record written -> completed line, exit 0; record missing -> E9 door exit 2 (`stage_close.stage_record_written`) | a completed S7 is never closed again: no second receipt, no `place_answers` / investigation write (TEMPORAL: the world the close itself creates) |
| E3c | S7 completed by a role (not `code_only`) | None: today's start | the close never claims a role's completion |
| E4 | `stage_done` refused after the receipt (`SkillRoad.record_close` raises with `record_door`) | `story_step: refused - S7 was not closed: ...`; `door: python ".../stage_done.py" --task T --stage S7 --status done --digest "no failures — nothing to triage<suffix>" --no-journal`; exit 2; the next `start` meets E3 (record missing -> the same door) | a receipt without its record is never reported closed; the door completes it; the `dispatch_skipped` tail row is not re-filed on the door road (F8 = a; the start prints `note: the journal row dispatch_skipped was not filed`) |
| E5 | a tail row (`log_append dispatch_skipped`) fails | BEFORE FV3-29 merges: result dropped, nothing printed; AFTER (MF1, the node's start condition): FV3-29's `note:` line in the captured lines; the close stands, exit 0 | a journal row is never a reason to undo or deny a written record, and its failure is never silent once FV3-29 is in |
| E6 | run report halted (`broken_run`, `timeout`, `env_blocked`), a `not_executed` with no receipt and no triageable target, or NO `run-report.json` (status None) | `story_step: refused - S7 was not closed: S7 entry: run-report.json execution_status is \`<status>\` — nothing to triage yet; the S6 halt that produced it stands`; `door: python ".../story_step.py" card --stage S6`; exit 2 (F4 = a) | a halted or missing report is never triaged and never closed over (driver parity) |
| E7 | S6 awaits its consumer (the analyst) | None: today's dispatch; the analyst is let in for S6 | S6's consumer step is never skipped by an S7 close |
| E8 | failures in the report | None: today's dispatch byte for byte | an S7 with a failure is never closed by this site |
| E9 | the driver's `run_role` runs this `start` (MF5) | reached only with failures or S6 awaiting -> step 7/4 -> None | the driver road sees no new output; if it ever met a no-failure world, the same body would close (one road) |
| E10 | an investigation pass running | `wait` -> §2.3 row, exit 0, no close, no gap of the pass's targets | a running pass is waited for (s7.md Investigation rule 0) |
| E11 | a pass owed (`decision == "dispatch"`) | `dispatch_owed` -> §2.3 row, exit 0; the conductor starts it; the next `start` sees "a pass ended" -> `close_gaps` -> close. The close reason suffix then says "<g> ... not investigated: <why>" where the driver says "investigated read-only: <k> recorded" (F3) | no close before the one pass per S7 chain has run or been gapped |
| E12 | the report holds a counting need row (`unprepared_rows` with `need`; it carries no `result`, so it is no triage target, manual_evidence.py:1346-1349) | `story_step: refused - S7 is not closed: <cases> need another instance of <stand>; the skill road closes this world after FV3-26n`; `door: ask the person once by section "Another instance of the stand" of the S7 card; a person who decides to close S7 anyway: <stage_done.py's own person's-word door, stage_done.py:1279>`; exit 2 | no S7 close over a need record with no answer (the driver's invariant, driver_stage_s7.py:92-95); errs toward no close |
| E13 | `--id` given / `--scope` given with no purpose | the steps ignore them; a close registers nothing | a close never consumes a dispatch id |
| E14 | the conductor runs `stage_done --status done` for S7 by hand | BEFORE the card lands: refused (MF6), as today. AFTER, before `start`: still refused (S7 not completed in the controller); the s7.md text no longer prescribes it. AFTER `start` closed S7: stage_done is accepted (controller completed) and rewrites the record's digest/role with the conductor's words (estimate - the builder measures it on the T1 world by one extra call and reports it) | the receipt and the controller's completion are never changed by a hand record |

## 5. Positional invariants (summary)
K5b (in `start`), K5 step order 2 -> 9: re-entry before any read that could close; analyst/S6-await/conflict guards before the
report read; the need guard before any `place_answers` / investigation write; places before the investigation gate (t-1991 U3a)
inside `s7_code_close`.

## 6. Readers of every touched file (designer rule 7)

The Lead's `tools/owns_readers.py` block was not attached (the brief has none): the Lead runs
`python -B tools/owns_readers.py --paths ai-packages/qa-factory/scripts/stage_close.py ai-packages/qa-factory/scripts/driver_stage_s7.py ai-packages/qa-factory/scripts/story_step.py ai-packages/qa-factory/skills/qa-story/phases/s7.md ai-packages/qa-factory/skills/qa-story/SKILL.md --names failures_to_triage s7_close_places s7_investigation_gate s7_gap_reason _s6_reentry record_door SkillRoad --readers`
and the plan critic answers its lines (Q13 d). Readers found by the designer (Grep, counts by file):

| touched | reader | status |
|---|---|---|
| stage_close.py | imports: controller.py (2), driver_dispatch.py, driver_stage_s6.py, driver_stage_s7.py, story_progress.py, story_step.py (2), tests test_story_run_s3_windows.py, test_story_step_manual_block.py (Grep `import stage_close|from stage_close`) | unchanged except driver_stage_s7 (-1) and story_step (-2); FV3-29 (t-1588) edits `SkillRoad.record_close` -> merge order MF1; FV3-24 (S6 steps) edits the same file -> sequenced by the Lead (COORDINATOR rule 4) |
| driver_stage_s7.py names | `failures_to_triage` etc. 96 hits / 22 files: s7_pretriage.py (3, comments/`triageable_not_executed`), contract.py, handoff_check.py, driver_machine.py, driver_dispatch.py, driver_stage_plan.py, driver_stage_s6.py (1 each, comments or calls through `self`), driver-layers.json (6 rows), test_s7_null_outcome.py (6: unbound calls, sentinel), test_no_move_seam_sites.py (5: stubs), test_story_run_s7.py (6, canon), test_silent_passes.py (1), test_story_run_s6_d1.py (1), quarantined: test_place_driver.py, test_s7_investigation_driver.py, test_manual_observations.py, test_place_session.py, test_stage_acceptance_consumer.py | unchanged (delegates keep names, homes, signatures); test_s7_null_outcome changes in -1; quarantined: not run |
| `_s6_reentry` | story_step.py only (Grep over the package; the test file reaches it through `start`) | changes in -2 (K6) |
| `record_door` | stage_close.py, story_step.py | unchanged signature; docstring names S7 (-2) |
| story_step.py `start` | the driver `run_role` (driver_dispatch.py:663), hooks binding the `Agent` call, test_story_step*.py, test_launch_card (card bytes: the close prints no card) | driver: unchanged (E9); others unchanged (a close returns before the card) |
| s7.md | story_step `card` (CARD_MAX_BYTES), driver_stage_s7.py (2), judge_results.py (2), s7_reorder.py (1), test_conductor_investigates_first.py (3: repair-cap / price paragraphs, untouched), tests that pin other sections (test_story_run_s7.py, test_controller_brief.py, test_story_run_s6_d1.py; quarantined two) (Grep `s7\.md` over scripts: 18 hits / 12 files) | unchanged paragraphs; the builder Greps each pinned phrase against the K7 diff and reports none changed |
| SKILL.md :194 | the conductor; no code reader found (builder Greps `S7 with nothing to triage` over the package) | changes in -2 |
| CODE_CLOSE_SITES `s7.no_failures` (driver_core.py:399) | driver deferred-record recovery only | unchanged (the skill road does not read it) |
| `story_progress._code_only` (:592) | both roads' progress line | unchanged; gains a skill-road S7 producer |

## 7. The other S7 sites: same node or their own (the brief's question)

| site | why not this node | named node |
|---|---|---|
| `s7.pretriaged` | needs `s7_pretriage.pretriage` run by `start` (writes triage rows) and the brief's "only the failures left" lines for the analyst dispatch; the close tail itself is `s7_code_close(road, "pretriaged")` already shaped here | FV3-26b (next; smallest after this) |
| `s7.accepted` | closes by the scribe's record (`consumer_pending("S7")` + `Driver.consumer_close_words`, a Driver member to move); the skill road's carrier is S8's call, not S7's `start` | FV3-26c |
| `s7.after_repairs` + `s7_await_scribe` | repair-life state (`s7_outcome`, `saved_done`, driver state `s7_walk`), the await marker (a twin of `mark_awaiting` with B3 finalize) | FV3-26d |
| the extra-instance step (question, re-walk, note file `work/extra-instance.json` the delivery check reads) | Person seam, driver-state held answer, re-walk marks; lifts E12's guard | FV3-26n (owns: stage_close.py, driver_stage_s7.py, story_step.py; test: a row in the same function) |
| S9 `s9.skip`, `s9.numbers` | Lead: after S7 lands green | FV3-26s9 |

## 8. Forks for the Lead (each with a recommendation)

- **F1 carrier.** (a) `start --stage S7 --role qa-failure-analyst` closes when nothing is left to triage (recommended: the stage's own
  call, as S6; no new command); (b) a new `story_step.py close --stage S7` (a new command for the conductor, FR-48 cost); (c) `card
  --stage S7` (breaks card's read-only contract).
- **F2 need rows with nothing to triage.** (a) no close while any counting need row exists, door to the card's question and
  stage_done's person's-word door; the story-only answer and re-walk stay a residual FV3-26n (recommended: smallest step, errs
  toward no close; cost: such stories still reach S8 only by the person's word until FV3-26n, as today); (b) move the whole
  extra-instance step now (+~110 moved lines, a held-answer carrier for the skill road, the note file writer; doubles this node);
  (c) ignore need rows on the skill road (one-road defect; not recommended).
- **F3 investigation on the skill road.** (a) road member `s7_investigation_dispatch`: the Driver runs the pass, the skill road returns
  "owed" and the conductor starts it; accept that the close-reason suffix differs between roads after a pass (recommended); (b) also
  make the suffix identical by recording the target list at "owed" time in a register file (new writer; later node).
- **F4 halted / missing run report on `start --stage S7`.** (a) refuse with the driver's text and the S6 card door (recommended:
  driver parity, the card's own Entry check); (b) None: today's analyst dispatch over a halted run.
- **F5 mode gate.** (a) none: one road; on the driver road the step returns None by construction (recommended, card r2 precedent);
  (b) gate on `current_run_mode() == "driver"` (a second road).
- **F6 stage_done's refusal text** still names "a `code_only` receipt" for a hand S7 close. (a) leave it (recommended: generic for every
  stage; s7.md no longer prescribes the hand line); (b) add a story_step door there (other file, other pile).
- **F7 test place.** (a) a function in `test_story_step_manual_block.py` reusing `real_story` and the `SkillRoad.py` seam (`_close`,
  :867-886) — the S7 world starts from the S6 close world (recommended; the file is already canon class, 25.5 s, run locally by
  node); (b) a new file `test_story_step_s7_close.py` with its own world (<=10 s goal; imports the world builder, a new "held by
  import" tie).
- **F8 refused record and the tail row.** (a) the door completes the record only; a `note:` line says the `dispatch_skipped` row is not
  filed (recommended: the driver calls a failed tail row "no state to ask about", driver_dispatch.py:2577); (b) `record_door` grows a
  second door line per tail row (the `rpartition("\ndoor: ")` reader then drops one).

## 9. Small choices closed by the designer
- Two sequential cards (move, then skill road), as FV3-22, so the driver witness is "unchanged".
- `s7_failures_to_triage` lives in `stage_close` (the S7 close survivor), not `s7_pretriage`: the skill road imports no driver.
- Only the text lookup of `s7_gap_reason` moves; the `s7_walk` branch reads driver state and stays (after_repairs is FV3-26d).
- "wait" / "owed" exit 0 (a next step, like S6 "awaits"); every refusal exits 2 (K5.h's rule).
- The live/behind guard is `controller.code_close_conflicts(state, "S7")` (the one predicate), read without verdicts: an unreadable
  liveness counts as running (its documented error direction).
- `_s6_reentry` generalized in place (one reader, story_step), not copied.

## 10. Reading trail
scout digest (whole); card r2 §0-§4 (lines 1-487); P/stage_close.py (whole); P/driver_stage_s7.py :1-240, :541-611, :757-1021;
P/driver_dispatch.py :650-680, :2541-2580; P/story_step.py :896-1022, :1175-1264, Grep `CARD_MAX_BYTES` (:3380); P/controller.py
:940-997, :1940-1969, :5015-5030, :6125-6160; P/stage_done.py :1236-1295; P/acceptance.py :1541-1556; P/contract.py :4626-4671;
P/manual_evidence.py :1326-1351; P/driver_core.py :307-311, :390-404, Grep `self.plugin =` (:448); P/investigation.py :477-483;
P/story_progress.py :588-607; phases/s7.md (whole); SKILL.md :186-199; architecture.md :33-72; docs/TESTING.md :75-114, :213-237;
test-layers.json :1-40 + rows; slow_tests.json :1-36 + Grep (all five witness candidates are in `files`); test_s7_null_outcome.py
:1048-1132; test_story_step_manual_block.py :1-30, :860-899; test_no_move_seam_sites.py Grep; test_judgment_census.py:77;
driver-layers.json Grep; SIBLING_MAP :130/:133 Grep; changelog.d Glob; Glob `docs/tasks/specs/*fv3-29*` = 0 (control `*fv3-2*` = 3):
no FV3-29 card on disk, its note form is MF1's to read.

## 11. Lead decisions (20.11.2026)

F1a, F2a, F3a, F4a, F5a, F6a, F7a, F8a. Nodes FV3-26b/c/d/n and FV3-26s9 are filed as rows of batch 3 when FV3-26-2 lands. FV3-26-1
goes first (FV3-29 merged at fa901743, MF1 holds); FV3-26-2 follows on main after FV3-26-1 merges.
