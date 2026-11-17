# FV3-22 (FV3-21c) — the skill road closes S6's manual half when nothing is left to dispatch (card r2)

Designer draft r2 for task t-1199, node `live-run-fvf/3/FV3-22`. It replaces r1
(`docs/tasks/specs/20261117-fv3-21c-skill-road-s6-close-card.md`, t-1182) WHOLE. It answers every finding of the plan critic t-1195
(`docs/tasks/specs/reviews/t-1195-fv3-22-card-plan.md`: 5 blocking + 11 fixes; the table is §10) and writes the Lead decisions
F1-F5 = (a) and Q-a3 -> FV3-24 into owns, items and tests (§11). Every line number marked WT was read in the FV3-21 worktree
`C:/QAFactory/forge-repo/.claude/worktrees/agent-af279738b46568113` (the branch head plus the UNCOMMITTED fix round t-1186). The
builder re-reads each one on the merged head (§0). Forks the Lead decides are in §8. The card can be carried out by the
recommendations as written.

## 0. Where the builder starts, and the merge-time facts (t-1186 overlap; verdict F5)

**Start.** FV3-22-1 starts from `origin/main` only AFTER the FV3-21 wave has merged. That wave is the branch
`worktree-agent-af279738b46568113`: FV3-21, FV3-21b and the fix round t-1186, all accepted. The builder does not start from
a1e9a77a or from the worktree. The fix round t-1186 changes the code this card moves:
- it adds `Driver.consumer_await`;
- it adds `story_step._no_stand_refusal`;
- `story_step` now imports `live_s6_scopes` from `driver_stage_s6`.

FV3-22-2 starts from the head FV3-22-1 leaves, on the same branch.

**Merge-time facts.** The builder re-checks each fact below by reading the merged head and puts it in the report with its
`file:line`. Some facts cover the line numbers this card names; a shift there is only reported. Any other difference means STOP:
the builder returns a question and does not adapt the design.

| # | fact on the merged head (WT line where read) | what the card builds on it |
|---|---|---|
| MF1 | `driver_stage_s6.live_s6_scopes(state) -> list` is a module function. It returns the scopes of S6 dispatches with status `running`, `blocked` or `paused`, read through `dispatch_identity.records` (WT :18-25). `Driver.s6_live_scopes` returns `live_s6_scopes(self.controller_state())` (WT :1722-1724) | K5.l moves it into `stage_close` |
| MF2 | `story_step._no_stand_refusal(task, state, block) -> list` (WT :1080-1106) imports `live_s6_scopes` from `driver_stage_s6`. It returns `[]` when there is no word or an S6 dispatch is live. It skips a `manual_done_cases` case with the line `<case>: checked already by an accepted block`. It is called at X2 (WT :1060-1062) | K5.l (the import), K5.e/K5.f (X2 `spent`, E17) |
| MF3 | `Driver.consumer_await(stage, author, state, route)` (WT :349-366) holds the one `atomic_json` of `acceptance_awaits` and the awaits print. `consumer_need_record` (WT :323-347) calls it at an `await_at` site | K5.a/K5.b move both |
| MF4 | `driver-layers.json`, the `allowed_importers` list: the WT has exactly two rows, `story_step->driver_timing` and `run_counters->driver_timing` (WT :5-8). The WT has no row for the module function `live_s6_scopes` and none for `Driver.consumer_await`. On the merged head the builder reads which of these rows FV3-21 added. Before any edit it runs `test_driver_layers.py` once as the baseline | K5.l deletes any `story_step.py -> driver_stage_s6` row and fixes the homes |
| MF5 | `test_story_step_manual_block.py` rows S8-S10 call `story_step._no_stand_refusal` directly and assert that it returns a list of lines (WT :814-829) | K5.e keeps that signature |
| MF6 | `manual_close` (WT :1069-1094: head :1077-1085, tail :1086-1094). `CONSUMER_ROUTES` (WT :158-170) holds the lambdas `closes_when` / `rework_complete`. `Driver.consumer_awaits` (WT :172-180) exists and is NOT moved | K5.a/K5.b |
| MF7 | before any edit, the node's DoD witness command runs on the merged head; its reds, if any, are listed as inherited | the node's own reds are told apart from inherited ones |

## 0.1 Dispatch header — FV3-22-1 (the move; driver behaviour unchanged except the door text E-M2)

```
task: <new id>
node: live-run-fvf/3/FV3-22
feature: F19
given:
C:/QAFactory/forge-repo/docs/tasks/specs/20261117-fv3-21c-skill-road-s6-close-card-r2.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/architecture.md
C:/QAFactory/forge-repo/plans/builder-rules.md
C:/QAFactory/forge-repo/docs/TESTING.md
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/stage_close.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_s6.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_s7.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_dispatch.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_core.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/story_step.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test-layers.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_story_run_s6.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/changelog.d/fv3-22-skill-road-s6-close.md
non-goals: the skill-road close and SkillRoad (FV3-22-2); story_progress.py (FV3-22-2, K5.k); in story_step.py anything but the `live_s6_scopes` import and docstring of `_no_stand_refusal` (K5.l); any quarantined test (test_stage_acceptance_consumer.py, test_consumer_close_route.py, test_refuse_case.py, test_role_permissions.py: not run, not edited); the A27 scanner (fork R2-F2); the S6 code steps of FV3-24; driver_core._sha (stays)
handoff: the diff on the branch + the builder report (FR pass, AR lines, MF1-MF7 with lines, witness output, the R2-F2 grep output, "ratchets raised: none" and the shrinks named)
edges: card r2 §4.1 (E-M1..E-M9), each with its invariant
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/stage_close.py ai-packages/qa-factory/scripts/driver_stage_s6.py ai-packages/qa-factory/scripts/driver_stage_s7.py ai-packages/qa-factory/scripts/driver_dispatch.py ai-packages/qa-factory/scripts/driver_core.py ai-packages/qa-factory/scripts/story_step.py ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json ai-packages/qa-factory/scripts/tests/test-layers.json ai-packages/qa-factory/scripts/tests/test_story_run_s6.py` and each test file it prints; plus, when it does not print them, `scripts/tests/test_driver_layers.py`, `scripts/tests/test_judgment_census.py`, `scripts/tests/test_no_move_seam_sites.py`, `scripts/tests/test_audit_rules.py`
siblings: axis 5 row "Code-only stage closes" (SIBLING_MAP:130) - the survivor moves (the row text is edited in FV3-22-2, K5.j); axis 34 via FV3-24 and fork R2-F3; axis 26 n/a here (the reader list is edited in FV3-22-2)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-fv3-21c-skill-road-s6-close-card-r2.md
```

Test lines (TESTING.md «Строка теста в DoD»), inside the DoD of FV3-22-1:
- K5.a, K5.b, K5.c, K5.d, K5.l: `test: none -- поведения нет: тела переносятся, драйвер ведёт себя как прежде; держат существующие строки test_story_run_s6.py и тесты S7, которые печатает witness-for | expected from: r2 §2.1, E-M1`
- K5.m (the person's-word door): `test: test_story_run_s6.py::<the row that asserts "S6 cannot be closed at s6_reentry: ..." (WT :2440)> - a variant check that the same refused text ends with person_words.door(...) (" --words-file <file>") | expected from: r2 E-M2, FR-2, waiver.py:1996-1999`

## 0.2 Dispatch header — FV3-22-2 (the skill road; sequential after FV3-22-1, same branch)

```
task: <new id>
node: live-run-fvf/3/FV3-22
feature: F19
given:
C:/QAFactory/forge-repo/docs/tasks/specs/20261117-fv3-21c-skill-road-s6-close-card-r2.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/architecture.md
C:/QAFactory/forge-repo/plans/builder-rules.md
C:/QAFactory/forge-repo/docs/TESTING.md
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/story_step.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/stage_close.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/story_progress.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_story_step_manual_block.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test-layers.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/skills/qa-story/phases/s6.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/changelog.d/fv3-22-skill-road-s6-close.md
C:/QAFactory/forge-repo/docs/SIBLING_MAP.md
non-goals: the driver modules (FV3-22-1 is done; a needed driver change is a question); the other S6 code steps of the skill road (s6.nothing, s6.results_stand, s6.accepted with no manual half, s6_reentry / s6_reprobed_close, s6_reprove_before_manual) and the analyst's S6 acceptance on the skill road = FV3-24; the skill road's S7/S9 code closes (fork R2-F3); any quarantined test (test_story_progress.py included); the driver's deferred questions, stand-login gate, walk_retry, lanes
handoff: the diff on the branch + the builder report (FR pass, AR lines, witness output, the probe's byte-copy hash comparison, the `in N.NNs` tail of test_story_step_manual_block.py, the `card --stage S6` tail)
edges: card r2 §4.2 (E1-E23) and §4.3 (E-P1..E-P7), each with its invariant
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/story_step.py ai-packages/qa-factory/scripts/stage_close.py ai-packages/qa-factory/scripts/story_progress.py ai-packages/qa-factory/scripts/tests/test_story_step_manual_block.py ai-packages/qa-factory/scripts/tests/test-layers.json ai-packages/qa-factory/skills/qa-story/phases/s6.md` and each test file it prints; plus `scripts/tests/test_story_step_manual_block.py` (the new rows live there), `scripts/tests/test_judgment_census.py` and `scripts/tests/test_driver_layers.py` when it does not print them; plus `python -B ai-packages/qa-factory/scripts/story_step.py card --stage S6` with its last 5 lines (no `over` note)
siblings: axis 5 rows "Code-only stage closes" (:130) and "Skill phase <-> driver" (:133); axis 26 (the stand word's reader `waiver.stand_passing_word` and its callers, K5.j); axis 34 (FV3-24; fork R2-F3)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-fv3-21c-skill-road-s6-close-card-r2.md
```

Test lines, inside the DoD of FV3-22-2:
- K5.e, K5.f, K5.h: `test: test_story_step_manual_block.py::fv3_22_nothing_left_closes_s6_on_the_skill_road rows C1-C8, C10-C11c, C14-C16 | expected from: r2 §2.3, §4.2 E1-E13, E15-E23`
- K5.e step 1b (re-entry): `test: the same function, rows C9, C9b | expected from: r2 §2.4, E14, E14b (critic t-1195 F4)`
- K5.g: `test: the same function, row C5 | expected from: r2 K5.g (the door text)`
- K5.i: `test: test_story_step_manual_block.py::the_card_and_the_help_name_the_rule - a variant check that the S6 card names "that same call closes S6" and the person's-word door | expected from: r2 K5.i`
- K5.k: `test: test_story_step_manual_block.py::fv3_22_awaits_position rows P1-P5 | expected from: r2 K5.k, §4.3`
- K5.j: `test: none -- документ, фрагмент и реестр; covers-правки подтверждает вывод witness-for (ключи stage_close.py / story_progress.py напечатаны) | expected from: r2 K5.j`

**Live proof (FR-33).** One line goes to the batch's «Живые доказательства». At acceptance the pile rule moves it to `live-runs`.
The line: a skill-road story with every manual-agent case refused reaches S7 awaiting the analyst; after the analyst's record
(or a person's word) the same `start` closes S6 code-only.

## 1. Defect, scope, AR-n, owners, census

### 1.1 Defect (re-checked by trail on WT)

- On the skill road, S6's manual half starts with `story_step.py start --stage S6 --role qa-runner --execution-kind manual
  [--scope ...]` (`phases/s6.md:10`). When nothing is left to dispatch, `_manual_block_door` prints `no manual-agent case is left
  for a block: nothing was dispatched; covered by ...` (WT `story_step.py:1123-1126`), and `start` exits 2 (WT :913-916).
  - Under the no-stand word, the block is refused at X2 (WT :1060-1062), with no door to anything after it.
  - A block whose every case `prepare` refused gets a door of the derived rest minus THIS call's refusals only (WT :1070-1076).
- `stage_done.py --status done` refuses a controller-managed stage that the controller has not accepted (WT `stage_done.py:1234-1253`).
  With a consumer, it also refuses without the consumer's record (WT :1225-1233).
- No non-test package file writes `code_only` except the driver. The one writer is `driver_dispatch.py:2549` (Grep over the
  package for `controller\("code_only"|apply\("code_only"`; the positive control is that hit itself).
- The driver's chain: `manual_close` (WT `driver_stage_s6.py:1069-1094`) -> `finalize_task.py` -> `consumer_need_record` (WT :323-347)
  / `consumer_await` (WT :349-366) -> `close_by_code` (WT `driver_stage_s7.py:763-786`) -> `close_receipt` -> `code_only`
  (WT `driver_dispatch.py:2536-2553`) -> `record_close` (WT :2565-2581). All of these are Driver methods.

So today a skill-road story whose manual cases are all refused, or are all done, can never complete S6. "All done" includes the
case where the last block was finished `--not-complete`. This is the P31 / axis 34 residual of card r2 §4.5.

### 1.2 Scope

There is ONE survivor of the close, wired to both roads (AR-15, P31). Three steps move out of the Driver into
`scripts/stage_close.py`:
- the consumer rule;
- the manual-half close order;
- the code close.

The same module also gets the shared live predicate and the one `BY_PERSON` constant.

The Driver's methods delegate; they keep the same names and the same homes. The skill road calls the same functions from the
same call that finds nothing left. The rest of the class is named nodes, so the slice is no exclusion (designer rule 6):
- FV3-24 takes the other S6 code steps (§7);
- the S7/S9 twins are fork R2-F3.

### 1.3 AR-n touched and the change check each demands (architecture.md)

| AR | how kept | change check written into the DoD |
|---|---|---|
| AR-15 | `stage_close.py` is the one survivor of the consumer rule, the manual-half close, the code close and the live-S6 predicate; every road calls it; nothing is copied. Inside `story_step`, the remaining-cases computation is one helper `_manual_cases_left`, used by `_manual_block_door` and `_s6_manual_close` (critic §6). The per-case word step is one helper `_no_stand_cases`, used by `_no_stand_refusal` and `_s6_manual_close` (F5b) | the report lists every site found by a grep for the PROBLEM, not for the helper. Patterns: `finalize_task.py`, `"code_only"`, `acceptance_awaits`, `"running", "blocked", "paused"`, over `scripts/*.py` (not tests). Each hit is a site that calls the survivor, or a named site (FV3-24 / R2-F3). SIBLING_MAP axis 5 row :130 names `stage_close` (K5.j) |
| AR-13 | one definition and one reader each: `stage_close.BY_PERSON` (writer `person_pass`, reader `Driver.consumer_close_words`), `stage_close.live_s6_scopes`, the `CONSUMER_ROUTES` data, `acceptance.awaits_acceptance` / `accepted_for` / `consumer_of`, `controller.manual_done_cases`, `Controller.stage_scope`, `Controller._pipeline_stage_statuses`, `waiver.stand_passing_word`, `waiver.split_overridden`, `person_words.door`, `hooklib.read_json` | DoD grep: `BY_PERSON =` has exactly 1 hit in `scripts/*.py`, and that hit is in `stage_close.py`; `def live_s6_scopes` has exactly 1 hit, in `stage_close.py`; the diff of `story_step.py`, `stage_close.py` and `story_progress.py` holds no `json.loads(` of `pipeline.json` and no `["acceptance_awaits"]` read outside `mark_awaiting`. Positive control: the same grep finds `acceptance_awaits` at `acceptance.py:1497` |
| AR-14 | each record has one writer. The receipt: the controller's `code_only` operation, with its request built only by `stage_close.code_only_request`. The acceptance record: `stage_done.py --acceptance`. The awaiting marker: `stage_close.mark_awaiting` (one `atomic_json`). The refused records: `manual_evidence.write_case_refusal` | DoD grep: no `atomic_json` / `write_text` in the diff of `story_step.py` or `story_progress.py`; exactly one `atomic_json` in `stage_close.py` |
| AR-17 / FR-48 / P3 | the close is code run by the stage's own call; the conductor runs no new command; no new stop, no new question | grep over the diff: no new `Person`, `no_move` or `ask` site |
| AR-18 | the A27 detector (dropped `self.py` results, `audit_factory.py:1652, 2381`) scans the driver set only. The moved `road.py` calls leave its reach (critic m7): fork R2-F2, recommendation = a residual named here plus the DoD grep | node -1 report: every `road.py(` call in `stage_close.py` has its result bound, or `check=True` (grep output attached); `test_no_move_seam_sites.py` and `test_audit_rules.py` green, with any changed A27 total named, never raised |
| AR-19 | S6/S7 twins keep one consumer rule (`stage_close.CONSUMER_ROUTES`); the skill phase and the driver run the same code for the manual-half close | report names the twins: S7's `close_by_code` callers in `driver_stage_s7.py` unchanged (witness: the S7 tests that witness-for prints) |
| AR-20 | no ratchet raised. `stage_close` imports no `driver_*`. Any `story_step.py -> driver_stage_s6` importer row FV3-21 added is DELETED (a shrink). The `BY_PERSON` row (`driver-layers.json:82`) is deleted, because the name leaves the family. Census ceilings unchanged | report line "ratchets raised: none; shrunk: <rows>", with `test_driver_layers.py` and `test_judgment_census.py` output |
| AR-21 | the receipt is written only over a `run-report.json` the reducer has just written; a completed S6 is never reduced again (step 1b) | rows C2, C7, C9 |
| AR-22 | the producers of `code_only` and of `acceptance_awaits` now exist on the skill road; their readers are unchanged. The `awaits` position has its producer (`story_progress`) and its reader (the progress line, both roads) | report lists the readers of `acceptance_awaits` and `code_only` (grep) |
| AR-23 / FR-23 | "nothing left to dispatch" is a recorded completed state (closed, or awaiting), never an escalation. An EMPTY manual half is declared: no close here (FV3-24) | rows C1, C2, C10 |
| AR-25 | the awaiting state has two working doors: the analyst's card, and the person's word through `person_words.door` (critic m5). A refused close names its door | rows C1, C7, C9b, E9 |
| AR-27 | every refused case is named in the close reason, and its request path is in the receipt's evidence; a "checked already" case is never counted as not checked (E17); passed-over work is filed (`file_passed_over`) | rows C2, C14 |
| AR-28 / FR-59 | an underived scope, an unreadable state, a live S6 dispatch (running/blocked/paused), a word not later than the acceptance, or a completed S6 whose record is missing -> no close and no "closed" line | rows C3b, C5, C8, C9b, C11, C11b, C11c |
| AR-29 | checks and owners in §1.4 | `test_judgment_census.py` green; a new unit or a changed class -> the builder STOPS and asks |
| AR-9 | every refusal of the close ends with a `door:` line the receiver can run (the person's-word door fixed, E-M2) | rows C7, C9b, E9, K5.m |
| AR-24 | the person's words reach the pass record (`--quote "by: person - <words>"`, cut at 500 as today) | row C3 |

Commit lines: an `architecture:` line naming AR-9, AR-13, AR-14, AR-15, AR-17, AR-18, AR-19, AR-20, AR-21, AR-22, AR-23, AR-24,
AR-25, AR-27, AR-28 and AR-29, and the `judgment:` line. Both take the form `tools/architecture_gate.py` carries: it is the one
carrier of that grammar, so it is not copied here. Recommended `judgment:` content: `none -- every check added or moved judges data
(derived scope, dispatch states, record presence, word time, stage status); the verdicts stay the failure analyst's and the
person's`.

The `docs/SIBLING_MAP.md` edit rides FV3-22-2's commit with an `axes: not a mechanism (<reason>)` line (`tools/mechanism_gate.py`
reads the map). The reason: the edit records the survivor of an existing twin row (axis 5) and the readers of an existing word
(axis 26); it adds no new duty.

### 1.4 Checks added or moved — owner and census class (AR-29, P27)

| check | where | owner | census class | census unit? |
|---|---|---|---|---|
| CK1 nothing left to dispatch (derived manual scope minus done minus refused, after preparing each remaining case) | `story_step._s6_manual_close` (new) | data (code) | xref | no: its name is outside `UNIT_NAME_RE` (`test_judgment_census.py:77`); it raises nothing; it returns lines through `_manual_block_check`, whose row (`judgment-census.json:1124`, shape/data) stands |
| CK2 the automated half is settled | `stage_close.s6_automation_settled` (moved from WT `driver_stage_s6.py:532-533`) | data | xref | no (returns bool) |
| CK3 no live S6 dispatch: running, blocked or paused | `stage_close.live_s6_scopes` (moved, MF1), called in CK1 step 4 | data | shape | no (returns a list) |
| CK4 the consumer rule: the record stands, or a person's pass (word later than the acceptance); else await at `manual_close`, refuse elsewhere | `stage_close.need_record` + `mark_awaiting` (moved) | data for the record's presence and time. The verdict inside the record is the analyst's (judgment, accepted by its own form); the pass is the person's (intent) | xref | no: it raises `stage_close.Refused(Exception)`, which is not a `ValueError` / `StateConflict` subclass, so `refusal_registry` sees no site (census docstring u3) |
| CK5 the reducer must succeed before a receipt | `stage_close.manual_half_close` | data | shape | no (Exception transport) |
| CK6 the receipt needs existing evidence | `stage_close.code_only_request` | data | shape | no (Exception transport) |
| CK7 re-entry: S6 completed -> report by the stage record | `story_step._s6_manual_close` step 1b | data | shape | no |
| CK8 the progress position `awaits` | `story_progress._awaits_position` (new) | data (advice: a display line) | shape | no (returns a dict) |

New names, all outside `UNIT_NAME_RE`: `_s6_manual_close`, `_manual_cases_left`, `_no_stand_cases`, `_awaits_position`,
`need_record`, `mark_awaiting`, `manual_half_close`, `close_by_code`, `code_only_request`, `s6_automation_settled`, `live_s6_scopes`,
`person_word_door`, `consumer_pending`, `accepted_at`, `person_pass`, `consumer_person_pass`, `file_passed_over`. r1's
`_refuse_by_word` matched `^_?refuse` and is dropped (critic m3).

## 2. The design

### 2.1 Where the shared logic lives (Lead F1 = (a))

The new module is `ai-packages/qa-factory/scripts/stage_close.py`. Its docstring: "the closes by code a stage takes when no role is
left to run it, for both roads".
- It imports no `story_step` and no `driver_*`, so there is no cycle and no `allowed_importers` row (L11,
  `test_driver_layers.py:547-575`).
- Its package imports (`acceptance`, `waiver`, `controller`, `event_store`, `manual_evidence`, `person_words`, `hooklib`,
  `dispatch_identity`) are taken inside its functions; the module level holds `hashlib`, `json`, `subprocess`, `sys`, `Path` only.
- The driver modules import it, as they import `waiver`.

**The road.** A ROAD is an object with the members below. The Driver IS a road: every member exists on it today, so nothing new is
added to the Driver. The skill road is `stage_close.SkillRoad`.

**INVARIANT (stubs and spies, critic m1).** Each free function reaches every step through the road member of the same name as the
old body's `self.<member>`, never through the free twin. Its set of road members equals the old body's set of `self` members. So
every stub on a Driver attribute keeps its effect, for example `manual_request_paths` (`test_story_run_s6.py:343`,
`test_walk_lanes_parallel.py:124`, `test_story_run_s6_w1_frozen.py:134`, `test_silent_passes.py:723/737`) and `code_only`,
`person_pass`, `record_close`, `consumer_need_record`, `close_by_code`.

Road members:
- `task`, `task_root`, `project`, `dry`;
- `controller_state()`, `pipeline()`, `controller(op, *args, input_data=None)`;
- `py(script, *args, check=False, expect="") -> (code, out)`;
- `owe_row(script, *args, what, stage)`;
- `accepted_at(author)`;
- `consumer_pending(stage)`;
- `person_pass(stage, author, line, answer="", since="")`;
- `consumer_person_pass(stage, author, answer="")`;
- `consumer_need_record(stage, site)`;
- `consumer_await(stage, author, state, route)`;
- `close_by_code(stage, reason, evidence, *, finalize, site="", digest="", role="", journal=False, tail=(), fresh=None)`;
- `close_receipt(site, stage, reason, evidence)`;
- `file_passed_over(stage, receipt)`;
- `record_close(site, stage, *args, tail=(), receipt="")`;
- `manual_request_paths(cases)`.

Module contents (bodies MOVED from the named Driver methods, behaviour unchanged unless a row says otherwise):

| name | moved from (WT) | notes |
|---|---|---|
| `class Refused(Exception)` with `title: str = ""` | — | the shared refusal; NOT a ValueError |
| `BY_PERSON = "by: person"` | `driver_core.py:411` | one definition. `driver_core` no longer binds it; `driver_stage_s6` imports it from `stage_close` (its only family reader, WT :13, :213, :318); `driver-layers.json:82` row deleted (verdict F3) |
| `CONSUMER_ROUTES` (data keys only: `consumer_stage`, `author`, `who`, `what`, `await_at`, `awaits`) | `driver_stage_s6.py:158-170` | the Driver keeps `CONSUMER_ROUTES = {s: dict(row, closes_when=<its lambda>, rework_complete=<its lambda>) for s, row in stage_close.CONSUMER_ROUTES.items()}`. The lambdas are read only by `Driver.consumer_awaits` / the rework code, so one definition of the data stands (E-M9) |
| `live_s6_scopes(state) -> list` | `driver_stage_s6.py:18-25` (MF1) | `driver_stage_s6` does `from stage_close import live_s6_scopes` (so `Driver.s6_live_scopes` is unchanged); `story_step._no_stand_refusal` imports it from `stage_close` (K5.l, verdict F5c) |
| `s6_automation_settled(state, auto_scope) -> bool` | `driver_stage_s6.py:532-533` | `not auto_scope` or an accepted S6 dispatch whose `execution_kind` is `automation` or empty; `stage_S6` calls it |
| `person_word_door(task, stage) -> str` | new | `person_words.door(f'waiver.py --task {task} --stage {stage} --block "{acceptance.STAGE_ACCEPTANCE_PHRASE}"')`, the one renderer of the words part (`person_words.py:116-133`); used by `need_record`'s refusal (E-M2) and by the awaiting lines (K5.e) |
| `consumer_pending(road, stage) -> bool` | `:182-191` | |
| `accepted_at(task_root, author) -> str` | `:234-244` | |
| `person_pass(road, stage, author, line, answer="", since="") -> dict` | `:281-321` | the dry gate via `getattr(road, "dry", False)`; the record via `road.py("stage_done.py", ..., check=True, expect=...)`; `--quote f"{BY_PERSON} - "...` from this module |
| `consumer_person_pass(road, stage, author, answer="") -> bool` | `:246-279` minus the `refusal.retry` lines | the Driver delegate keeps the retry: `except Refusal as r: r.retry = lambda: self.consumer_person_pass(...); raise` (critic §4: equivalent) |
| `need_record(road, stage, site) -> bool` | `consumer_need_record` `:323-347` | raises `Refused` where the Driver raised `Refusal`; the refusal text is unchanged up to its end, then the door is `person_word_door(road.task, stage)` (E-M2); calls `road.consumer_await(stage, author, state, route)` at an `await_at` site |
| `mark_awaiting(road, stage, author, state, route) -> bool` | `consumer_await` `:349-366` (MF3) | the one `atomic_json` of the marker plus the awaits print. Named `mark_awaiting`, so it never collides with `Driver.consumer_awaits` (critic F5a). The Driver keeps `consumer_await` as a delegate; `SkillRoad.consumer_await` calls it too |
| `manual_half_close(road, done, refused) -> bool` | the tail of `manual_close`, `:1086-1094` | True = closed, False = awaits. Steps: reason words; `road.py("finalize_task.py", str(road.task_root))` (non-zero -> `Refused("S6 manual half: finalize_task.py exit <n>: <last line>")`); `road.consumer_need_record("S6", "manual_close")`; `road.close_by_code("S6", reason, ["work/run-report.json"] + road.manual_request_paths([c for c, _ in refused]), finalize=False, site="s6.manual_close")` |
| `close_by_code(road, stage, reason, evidence, *, finalize, ...) -> bool` | `driver_stage_s7.py:763-786` | the ORDER: completed check, finalize, `fresh`, `road.close_receipt`, `road.file_passed_over`, `road.record_close` |
| `code_only_request(road, stage, reason, evidence) -> dict` | the request half of `driver_dispatch.py:2539-2551` | refs hashed with `hashlib.sha256(path.read_bytes()).hexdigest()`, the controller's own form (`controller.py:2094, 2140, 2231`, judged by `_ref_issues`); `driver_core._sha` is not imported and stays (its other caller `driver_dispatch.py:2484`), see E-M5. The request holds `id`, `stage`, `reason`, `evidence_refs`, `expected_revision`, `idempotency_key`, as today. Raises `Refused(..., title="code_only_evidence")` when no evidence file exists |
| `file_passed_over(road, stage, receipt)` | `driver_stage_s6.py:1986-2006` | |

**Driver delegates.** Each delegate keeps its name and home, so every `driver-layers.json` row stands (WT :663, :664, :699, :704, :733,
:1069, :1041); the `BY_PERSON` row :82 goes. Each method above becomes one call to its free function. Where the free body can raise
`stage_close.Refused` (`consumer_need_record`, `manual_close`, `close_by_code`, `code_only`), the delegate converts it once:
`except stage_close.Refused as exc: raise Refusal(str(exc), title=exc.title) from None`. A driver `Refusal` raised inside by a Driver
member passes through untouched, with its `retry` / `close`.
- `manual_close` keeps its driver-only head (`deferred_waiting`, WT :1077-1085), then calls `manual_half_close(self, done, refused)`.
- `code_only` = `stage_close.code_only_request(self, ...)` (converted, `title` kept) + `self.controller("code_only",
  input_data=request)` + `self.progress_line()` + `return request["id"]`.
- `close_receipt`, `record_close`, `consumer_awaits` and `consumer_close_words` stay unchanged Driver methods.

**`SkillRoad(task, task_root, controller)`** (in `stage_close.py`; FV3-22-2):
- `dry = False`; `project = hooklib.project_root()`.
- `controller_state()` = `controller.state()`; `pipeline()` = `hooklib.read_json(task_root / "pipeline.json")` when it is a dict, else
  `{}`; `controller(op, input_data=...)` = `controller.apply(op, input_data)`. `apply` does the passed_over enrichment
  (`controller.py:5125`), so both roads get the same receipt.
- `py(script, *args, check, expect)`: `subprocess.run([sys.executable, "-B", str(<scripts>/script), *args], capture_output=True,
  text=True, encoding="utf-8", errors="replace")`, inheriting story_step's cwd and environment (as `story_step._run`, WT :144-153).
  - A missing script is exit 127, never `_run`'s "skipped" success.
  - With `check=True`, a non-zero exit raises `Refused(f"{script} exit {code}: <last line>" + (f" ({expect})" if expect else ""))`.
- `owe_row(...)` = `py(...)`; a failure prints `note: <what> was not filed: <last line>` and never raises.
- `accepted_at`, `consumer_pending`, `person_pass`, `consumer_person_pass`, `consumer_need_record` (= `need_record`), `consumer_await`
  (= `mark_awaiting`), `close_by_code` and `file_passed_over` are the free functions over `self`.
- `manual_request_paths(cases)` = `[manual_evidence.request_path(task_root, c).relative_to(task_root).as_posix() for c in cases]`, the
  Driver's own expression (WT :1065-1067).
- `close_receipt(site, stage, reason, evidence)` = `code_only_request(self, ...)`, then `self.controller("code_only",
  input_data=request)`; it returns the id.
- `record_close(site, stage, *args, tail=(), receipt="")` = `py("stage_done.py", "--task", task, "--stage", stage, *args,
  check=True)`, then each `tail` row through `py("log_append.py", *row)`. A refused record raises `Refused` whose text ends with the
  door `door: python "${CLAUDE_PLUGIN_ROOT}/scripts/stage_done.py" --task <T> --stage <S> <args, each quoted when it holds a space>` (E9).

### 2.2 Which skill-road command carries it (Lead F2 = (a))

`start --stage S6 --role qa-runner --execution-kind manual` carries the close itself, at the three exits that today end in
"nothing was dispatched", a door, or the word's refusal: the same call that finds nothing left closes.
- Why (FR-48 / AR-17 / P3): code runs on the stage's own transition, and the conductor never launches commands.
- `where` is read-only by contract.
- The driver never calls `start --execution-kind manual`; its only `--execution-kind` is `automation`, at `driver_dispatch.py:666`.
- No mode gate is added: it would be a second road.

### 2.3 What `start`, `where` and `story_progress` show after (Lead F3 = (a))

The print order is the real order (critic m4). `_s6_manual_close` runs the module calls under
`contextlib.redirect_stdout(<buffer>)` and splices the captured lines into the returned list in this order:
1. the case lines;
2. the captured module lines (the person's-pass line, the awaits line, "completed already", `note:` lines);
3. the trailer.

On an exception, the captured lines come before the refusal line (E20).

| world | `start` prints, in order; exit | `where` | `story_progress` line |
|---|---|---|---|
| closed by code | `<case>: not checked by hand - <why>` per refused case; captured module lines; `S6 is closed by code: the manual half of S6: <n> case(s) checked by an agent by hand, <m> not checked: <ids>`; `next: python "${CLAUDE_PLUGIN_ROOT}/scripts/story_step.py" card --stage S7`; exit 0 | `prepare_stage S7` (S6 completed) | S7 current with no dispatch: head `starting S7 <name>`, `done S0–S6` |
| awaits the consumer | case lines; the captured `S6: nothing is left to dispatch; S6 awaits the acceptance of qa-failure-analyst for <runner> (the failure analyst is let in; its record closes S6)`; `next: the failure analyst judges S6 first: python "${CLAUDE_PLUGIN_ROOT}/scripts/story_step.py" card --stage S7; or a person's word accepts it: <person_word_door(T, "S6")>; after either, run this same start again: it closes S6`; exit 0 | `prepare_stage S7` (`awaits_acceptance` moves `i`, `controller.py:9241-9271`) | S6 current: position `waiting for the failure analyst's acceptance (S7)` (K5.k); activity = the analyst's run when one runs, else `no role running` |
| after the record or the word, the same `start` | the closed row (C2/C3) | | |
| S6 completed, record done (re-entry) | `S6 is completed already: nothing is closed again`; `next: python "${CLAUDE_PLUGIN_ROOT}/scripts/story_step.py" where --task <T>`; exit 0 | unchanged | unchanged |
| S6 completed, record missing (E9 world) | `story_step: refused - S6 is completed in the controller but its stage record is not written`; `door: python "${CLAUDE_PLUGIN_ROOT}/scripts/stage_done.py" --task <T> --stage S6 --status done --digest "<reason of the S6 code_only event>" --no-journal`; exit 2 | unchanged | unchanged |

### 2.4 Re-entry after a close (verdict F4)

`story_step.start` has no guard for a completed stage before `_manual_block_check` (WT :911-916). The close therefore checks it first
(K5.e step 1b): with the controller holding S6 `completed`, it runs no reducer and no plan.
- The pipeline's S6 status is read through `Controller._pipeline_stage_statuses()` (`controller.py:8793-8800`, the one reader).
- If that status is `done`: the completed line, exit 0.
- Otherwise: the E9 door, exit 2. Its `--digest` is the `reason` of the S6 `code_only` event, read from `controller.state()["stages"]["S6"]`.
  If that cannot be read, the placeholder is `"<the close reason>"`, never a guess.

The case "re-run while S6 awaits" is E19. Re-running before the record is legal and reduces again; no receipt exists yet, so nothing
holds the report's hash. The driver also re-reduces at `manual_close` after the record (WT :1088), so this is parity.

## 3. Items

### FV3-22-1 (the move)

**K5.a** `scripts/stage_close.py` (new). It holds:
- the module docstring: both roads, the road members, the stub invariant of §2.1;
- `Refused`, `BY_PERSON`, `CONSUMER_ROUTES` (data), `live_s6_scopes`, `s6_automation_settled`, `person_word_door`;
- the free functions of §2.1's table. Their bodies are moved verbatim except for these changes:
  - `self` -> `road`;
  - `raise Refusal(` -> `raise Refused(`;
  - `self.CONSUMER_ROUTES` -> the module table;
  - every sub-step goes through `road.<member>`;
  - `_sha(path)` -> the inline hash (E-M5);
  - `need_record`'s door -> `person_word_door` (E-M2).

**K5.b** `scripts/driver_stage_s6.py`:
- `CONSUMER_ROUTES` is built from the module's data plus the two lambdas (one definition of the data).
- These become delegates (§2.1): `consumer_pending`, `accepted_at`, `person_pass`, `consumer_person_pass` (keeps the retry),
  `consumer_need_record`, `consumer_await`, `file_passed_over`.
- `manual_close` = its deferred-waiting head + `manual_half_close(self, done, refused)`, with the conversion.
- `stage_S6` computes `auto_done` by `stage_close.s6_automation_settled(state, auto_scope)`. The truth table is the same.
- The module function `live_s6_scopes` is deleted here and imported from `stage_close`.
- `BY_PERSON` is imported from `stage_close`; it is dropped from the `driver_core` import line (WT :13).

**K5.c** `scripts/driver_stage_s7.py`: `close_by_code` is a delegate to `stage_close.close_by_code(self, ...)`, with the conversion.

**K5.d** `scripts/driver_dispatch.py`: `code_only` as in §2.1. `close_receipt` and `record_close` are unchanged. `_sha` stays in the
import line (its caller :2484).

**K5.l** The homes:
- `scripts/driver_core.py`: delete `BY_PERSON` (:411).
- `scripts/tests/fixtures/driver-layers.json`:
  - delete row :82;
  - delete any `allowed_importers` row `story_step.py -> driver_stage_s6` (MF4);
  - a row FV3-21 added for the module function `live_s6_scopes` is deleted, because the name leaves the family;
  - a row for `Driver.consumer_await` is added only if `test_driver_layers.py` demands it (home `driver_stage_s6`, note "FV3-22:
    delegate of stage_close.mark_awaiting").
- `scripts/story_step.py`: `_no_stand_refusal` imports `live_s6_scopes` from `stage_close`, and its docstring names
  `stage_close.live_s6_scopes`. Nothing else in this file in node -1.

**K5.m** The person's-word door and the registry:
- `need_record`'s refusal ends with `person_word_door(...)` (E-M2).
- `test_story_run_s6.py`: the variant check of §0.1.
- `test-layers.json`: add `"stage_close.py"` to the `covers` of `test_story_run_s6.py` (WT :6178) and of
  `test_story_step_manual_block.py` (WT :6364), so that node -1's `--witness-for stage_close.py` names the tests that judge it
  (critic m6).
- `changelog.d/fv3-22-skill-road-s6-close.md` (ASCII), bullet 1: "The refusal of a close site that lacks the consumer's record now
  prints the person's-word door with its words file (waiver.py refused the old door)."

### FV3-22-2 (the skill road)

**K5.e** `scripts/story_step.py`, new function `_s6_manual_close(args, controller, state, spent: dict) -> tuple | None`. Its
docstring names FV3-22, P31 and the driver site it shares (`manual_close`).
- **Return shape (critic m2):** always the 4-tuple `(kind, lines, code, refused)`:
  - `kind` is `"done"`, `"left"` or `"automation"`;
  - `lines` is a list of str; `code` is an int; `refused` is a dict mapping case -> why;
  - `None` = not applicable (today's lines).
- **Helpers (one each, AR-15):**
  - `_manual_cases_left(state, scope, spent) -> list` = `[c for c in scope if c not in manual_done_cases(state) and c not in spent]`.
    `_manual_block_door` uses it at WT :1121-1122.
  - `_no_stand_cases(task_root, state, cases, words) -> dict` returns, for each case NOT in `manual_done_cases(state)`, its why. When
    `prepare_for_block` refuses, the why is prepare's own and its record is kept. Otherwise `write_case_refusal(..., reason,
    no_stand_door, "left_unchecked")` is written and the why is `reason`. `_no_stand_refusal` builds its lines from this dict plus the
    `checked already` lines, with its signature and return unchanged (MF5).

Steps, in this order:
1. `args.stage == "S6"`, else None.
1b. RE-ENTRY: `controller.state()["stages"]["S6"]["status"] == "completed"` -> no reducer, no plan. Return `("done", [completed
   line, next where], 0, {})` when `controller._pipeline_stage_statuses().get("S6") == "done"`, else `("done", [refused line, E9
   door], 2, {})` (§2.4).
2. `auto = controller.stage_scope("S6", state, "automation")` and `manual = controller.stage_scope("S6", state, "manual")`. If either
   is not `derived`, or its `scope` is not a list -> None.
3. `manual["scope"]` empty -> None (FV3-24's world).
4. `stage_close.live_s6_scopes(state)` non-empty -> None. This counts a running, blocked or paused S6 dispatch (verdict F2): no
   prepare and no close.
5. Not `stage_close.s6_automation_settled(state, auto["scope"])` -> `("automation", [K5.g door line], 2, {})`.
6. `done = [c for c in manual["scope"] if c in manual_done_cases(state)]`; `refused = dict(spent)`; `words =
   waiver.stand_passing_word(_read_pipeline(task_root))`. For each case of `_manual_cases_left(state, manual["scope"], refused)`, in
   derived order:
   - `why = manual_evidence.prepare_for_block(task_root, case)[1]`; a non-empty `why` -> `refused[case] = why`;
   - else with `words`, `refused.update(_no_stand_cases(task_root, state, [case], words))`;
   - else return `("left", [], 2, refused)` (something is left: no close; E18 for what prepare wrote).
7. Nothing left: build `road = stage_close.SkillRoad(args.task, task_root, controller)`. Under the captured stdout, run `closed =
   stage_close.manual_half_close(road, done, list(refused.items()))`. Return `("done", [*case lines, *captured, closed line + next
   S7 | awaits next line (§2.3)], 0, refused)`.
   - `stage_close.Refused`, `StateConflict` and `ValueError` raised inside -> `("done", [*case lines, *captured, "story_step: refused
     - S6 was not closed: " + <text>, <door line>], 2, refused)`.
   - The door line is the one the text ends with (E8, E9, E10). When the text carries no `door:`, it is `door: repair what the line
     above names, then run this start again`.

**K5.f** `scripts/story_step.py`, `_manual_block_check`, kind manual. POSITION: at the three exits that today return a refusal
because nothing can be dispatched by THIS call. Each calls `_s6_manual_close(args, controller, state, spent)`:
- (X1) `not block` (WT :1045-1047), with `spent = {}`;
- (X2) the word branch (WT :1060-1062, after `validate_manual_runner_block`), with `spent` = ONLY the cases of the block that got a
  `not checked by hand` line in this call, with their whys. They come from `_no_stand_cases`'s return value, never from the text
  lines, and never include a `checked already` case (E17, verdict F5b). `_no_stand_refusal` is changed to return its dict to X2
  through a second function `_no_stand_lines(task, block, state, cases) -> list`, so X2 computes the dict once and then the lines.
  The tests' direct call to `_no_stand_refusal` keeps its list return (MF5);
- (X3) every case of the block refused by prepare (WT :1070-1076 with `every`), with `spent = refused`.

Outcomes:
- `"done"` -> `return None, lines, code`;
- `"left"` -> today's return, except that the door is built with `spent=refused` (X1: `door([], refused)`; X3: `door([], refused)`;
  X2 keeps its own lines; at X2 under the word `"left"` is unreachable, E23);
- `"automation"` -> today's return plus K5.g's line;
- None -> today's return byte for byte.

POSITIONAL INVARIANT:
- A malformed block is refused as today and never closes: validate runs before X2/X3, and X1 has no block.
- A call whose block has a ready case never runs the plan or the close. That covers the partial-refusal exit (WT :1070-1076 without
  `every`) and the success return (WT :1077).
- Nothing the close does registers a dispatch, a stamp, a brief, an event of its own or a `run_mode` stamp: it returns before
  `stamp_run_mode` (WT :917).
- What it writes: the request files of prepare (E18), the word records, the marker, the receipt and the stage record.

**K5.g** `scripts/story_step.py`: the `"automation"` outcome appends to today's lines: `door: the automated half of S6 is not
accepted yet; the manual half closes after it: python "${CLAUDE_PLUGIN_ROOT}/scripts/story_step.py" start --task <T> --stage S6
--role qa-runner --execution-kind automation`.

**K5.h** `scripts/story_step.py`, `start` (WT :913-916) becomes `if code or (refusal and block is None):`, which prints the lines and
returns `code`. INVARIANT: every refusal return of `_manual_block_check` today has code 2 (critic §5, read WT :1018-1077). So the
widened test changes no existing outcome. The close outcome (code 0, lines, no block) returns before the stamp.

**K5.i** `skills/qa-story/phases/s6.md`, card line 6, after `code closes S6 itself: no runner, nothing re-run.`, insert:
`When the automated half is accepted and \`start --execution-kind manual\` finds no manual-agent case left to dispatch (each is done,
or refused with its reason), that same call closes S6: it reduces the run report; with the failure analyst's acceptance or a
person's word (the door it prints) it closes S6 by code, otherwise S6 awaits the failure analyst - go to the S7 card, and after its
record run the same \`start\` again.` The card section is 3168 bytes today (critic §1); with the insertion it stays under
`CARD_MAX_BYTES` 4000 (`story_step.py:3210`). Witness: `card --stage S6` prints no `over` note.

**K5.j** Changelog, map and registry:
- `changelog.d/fv3-22-skill-road-s6-close.md`, bullet 2 (ASCII): the skill road's manual `start` closes S6 when no manual-agent case
  is left to dispatch, by the same code as the driver. It reduces; the failure analyst's record or a person's word closes S6 by code;
  otherwise S6 awaits the analyst. The progress line shows that wait on both roads.
- `docs/SIBLING_MAP.md`:
  - axis 5 row "Code-only stage closes" (:130): the survivor is `scripts/stage_close.py` (`close_by_code`, `manual_half_close`,
    `need_record`, `mark_awaiting`); the Driver's methods delegate; the skill road (`story_step._s6_manual_close` via
    `stage_close.SkillRoad`) calls it;
  - row "Skill phase <-> driver" (:133): one clause naming the shared S6 manual-half close;
  - axis 26 (:455): one clause naming `waiver.stand_passing_word` as the reader for both roads, with its callers
    `Driver.s6_stand_word` (`driver_stage_s6.py:718-720`), `story_step._no_stand_refusal` / `_no_stand_cases` and
    `story_step._s6_manual_close` (critic axis 26; 0 hits for `stand_passing_word` in the map today, read this round).
- `scripts/tests/test-layers.json`: add `"story_progress.py"` to the `covers` of `test_story_step_manual_block.py`.

**K5.k** `scripts/story_progress.py` (Lead F3 = (a), verdict F1): new helper `_awaits_position(controller_state, pipeline, current)
-> dict | None`.
- It returns `{"kind": "awaits", "author": <id>, "consumer": <role>, "consumer_stage": <id or "">, "who": <words>}` when
  `acceptance.awaits_acceptance(controller_state, current, pipeline)` (the one reader) names an author.
  - `who` = `stage_close.CONSUMER_ROUTES[current]["who"]`.
  - For a stage not in that table, `who` = `_role_words(acceptance.consumer_of(current))`.
  - `consumer_stage` = the table's `consumer_stage`, or `""`.
- Any exception -> None.
- In `progress()` (WT :532-557), POSITION: a new branch `elif awaits:` after the `asked` and `waiting_gate` branches, before the
  `code_only` branch. It sets `out["position"]` and leaves `out["waiting"]` None.
- In `_parts()` (WT :607-672):
  - kind `awaits` -> `parts["position"] = f"waiting for the {who}'s acceptance" + (f" ({consumer_stage})" if consumer_stage else "")`;
  - activity: the `if run:` branch as today; with no run, `no role running` (the `elif` at WT :668 gains `"awaits"`).
- Both roads see it: the driver's `[progress]` line and the dashboard read the same dict.
- The new kind's readers are `story_progress` itself and tests only: Grep `\["position"\]|position\.kind|\.get\("position"\)` over the
  package = 3 files, `story_progress.py`, `test_story_progress.py` (quarantined) and `test_s5_plan_windows.py`. The positive control
  is the `story_progress.py` hit itself.

## 4. Edges (each with the invariant it protects)

### 4.1 FV3-22-1 (the move)

| # | edge | behaviour | invariant |
|---|---|---|---|
| E-M1 | any driver run through a moved method | the same class, text, `title`, `retry` and `close` of every Refusal; the same prints, in the same order | the driver's close machinery (`close_receipt` reads `title == "code_only_evidence"`, `record_close`'s retry, the deferred record C2-8) is unchanged |
| E-M2 | the refusal of a close site with no consumer record (`need_record`) | the text is byte-identical up to `` (`waiver.py --task <T> --stage <S> --block "stage acceptance"` ``, which becomes `person_word_door(...)` = that command + ` --words-file <file>` | a printed door is one its receiver can run: `waiver.py` refuses `--stage/--block` without `--decision` / `--words-file` (`waiver.py:1996-1999`; FR-2). `test_story_run_s6.py:2440` checks `startswith`, which still holds |
| E-M3 | `BY_PERSON` | one binding in `stage_close`; `driver_core` has none; the `driver-layers` row is deleted | the writer (`person_pass`) and the reader (`consumer_close_words`) share one constant (AR-13); `stage_close` never imports `driver_*` (L11) |
| E-M4 | `live_s6_scopes` | one definition in `stage_close`; `driver_stage_s6` and `story_step` import it from there; any `story_step -> driver_stage_s6` importer row is deleted | one predicate for both roads (AR-15); no family part is imported by a non-family script (AR-20: shrink only) |
| E-M5 | the evidence hash | inline `hashlib.sha256(path.read_bytes()).hexdigest()` in `code_only_request` | a receipt whose hash differs from the file bytes is refused by the controller's `_ref_issues`; no second judge of the hash exists |
| E-M6 | a test stub on a Driver attribute | still takes effect | every free body reaches its steps through `road.<member>` with the old member set (§2.1) |
| E-M7 | TEMPORAL: before node -1 there is no `stage_close.py`, and the Driver holds the bodies. After it (created by K5.a) the module exists, the Driver delegates, and the skill road is still unchanged until node -2 | both worlds named; a marker written before is read by the same reader | no field changes meaning; a pipeline written before the change reads the same |
| E-M8 | name collision `consumer_await` / `consumer_awaits` | the free body is `mark_awaiting`; both Driver names keep their meaning | no Driver name changes meaning; layer rows stand |
| E-M9 | `CONSUMER_ROUTES` lambdas | live only in the Driver's table | one definition of the data; `Driver.consumer_awaits` and the rework code read the lambdas unchanged |

### 4.2 FV3-22-2 (the skill road)

| # | edge | behaviour | invariant |
|---|---|---|---|
| E1 | the automated half is not accepted | no plan, no close; today's lines + the K5.g door | S6 is never closed by code over an automated half that never ran |
| E2 | the manual or automation scope is not derived / not a list | None: today's lines | an unknown scope never reads as "nothing left" (AR-28) |
| E3 | the manual scope is empty | None (FV3-24) | the driver's other sites are not replaced by the manual close |
| E4 | an S6 dispatch that is running, blocked or paused (`live_s6_scopes`) | None: no prepare, no close | no close over a walk that has not ended, and a paused walk's requests are never rewritten (verdict F2). The controller's own close check counts only `running` (`controller.py:916-918`), so it is no backstop |
| E5 | one remaining case prepares | `"left"`: today's refusal; the door = the cases not refused | a block with work left is never closed; a refused case is not offered again |
| E6 | `prepare_for_block` refuses through its catch-all (`manual_evidence.py:1338-1339`) | counted refused, named in the reason and the receipt | driver parity (`manual_plan` does the same); reported per case (AR-27) |
| E7 | the no-stand word is live | every remaining not-done case gets the word's record (prepare's own refusal kept), then the close | the driver's `manual_no_stand` + `manual_close` outcome on the skill road (P31) |
| E8 | the reducer fails | exit 2: `story_step: refused - S6 was not closed: S6 manual half: finalize_task.py exit <n>: <tail>`, then `door: repair what the line above names, then run this start again`; no marker, no receipt | nothing is closed or marked over a report nobody could build (AR-21) |
| E9 | `stage_done --status done` is refused after the receipt | exit 2; the text ends with the exact `stage_done.py --task <T> --stage S6 --status done --digest "<reason>" --no-journal` door | the receipt is never lost silently; the record can be completed by the printed command (FR-2); a later `start` lands in E14b, never in "closed" |
| E10 | the controller refuses `code_only` (the state moved, `passed_over` changed) | exit 2 with the controller's text | no receipt over a state that moved |
| E11 | a person's word dated before the runner's acceptance (or with no readable time) | not honoured: awaits | a word never accepts work the person had not seen (FR-4) |
| E12 | the consumer record stands for an EARLIER runner dispatch | not pending -> awaits | a record given for other bytes does not count (`accepted_for` reads `reviewed_dispatch == author`) |
| E13 | no consumer (`acceptance_by` absent) | `need_record` is False: the stage closes by code | the world before X7-6 behaves as the driver does (temporal) |
| E14 | S6 completed and its pipeline record done, when `start` runs again | `S6 is completed already`, next `where`; no reducer, no plan; exit 0 | a completed S6 is never reduced again: a report a receipt has hashed is never rewritten by this call (verdict F4a, AR-21) |
| E14b | S6 completed, its pipeline record NOT done (the E9 world) | exit 2 with the E9 door; no reducer; never "closed" | no false success: "closed" is printed only when the stage record exists or is written in this call (verdict F4b, AR-28) |
| E15 | TEMPORAL: before node -2 the skill road prints "nothing was dispatched"; after it, it closes. A marker written by the driver is read the same | both worlds named; K5.e-K5.h create the road | no field changes meaning |
| E16 | a case `manual_done_cases` lists as done | whatever the one reader says | no second reading of "done" (AR-13) |
| E17 | X2 with a block case already done (`checked already`) | `spent` holds only the cases that got a `not checked by hand` line; the done case counts in `done` | a checked case is never reported as not checked, and its request path never becomes receipt evidence (verdict F5b, AR-27) |
| E18 | X1's `"left"` outcome | `prepare_for_block` has written the request files of the cases it prepared, up to the first ready one; nothing else is written | FB-9 (WT :909-910) protects "no dispatch, no stamp, no event, no brief before a refusal", and that still holds. The request files are prepare's own, rewritten by the next `start` of that block; accepted (critic §7) |
| E19 | `start` re-run while S6 awaits (no record, no word) | reduces again; `mark_awaiting` does not rewrite the marker (it writes only when the reader does not name the author yet, WT :361-363); the awaits lines again; exit 0 | no receipt exists in the awaiting world, so the repeated reduction is hashed by nothing; parity with the driver, which reduces at `manual_close` before the post-record close (WT :1088-1094) |
| E20 | the module prints while `start` returns lines | captured and spliced in the order of §2.3; on a refusal, the captured lines precede it | no line is lost or reordered against what happened (critic m4) |
| E21 | the awaiting state | its `next:` names the S7 card and `person_word_door(T, "S6")` | the awaiting state has a door that works today on the skill road (critic m5, AR-25); the analyst's S6 acceptance on the skill road is FV3-24 (Q-a3) |
| E22 | the return of `_s6_manual_close` | always `(kind, lines, code, refused)` or None | one shape, unpacked in one place (critic m2) |
| E23 | X2 under the word | `"left"` is unreachable (every not-done case is refused); the code path stays per contract | under the word, no case is ever offered for walking (FV3-21b) |

### 4.3 K5.k (the progress position)

| # | edge | behaviour | invariant |
|---|---|---|---|
| E-P1 | S6 awaits the analyst | position `awaits`, `waiting for the failure analyst's acceptance (S7)` | the reader is `acceptance.awaits_acceptance`, the one the gates ask (AR-13) |
| E-P2 | S7 awaits the doc scribe | `waiting for the doc scribe's acceptance (S8)` | both stages of the table, one branch (axis 5) |
| E-P3 | the reader raises (unreadable table or state) | None: today's position | ERROR DIRECTION: this is advice; it may err only toward today's line, never toward "awaits" over a stage that is not awaiting, and `progress` never raises for it |
| E-P4 | a gate or a question waits | the gate / question position | the person's own wait is never hidden by a role's wait (POSITION) |
| E-P5 | awaiting while the analyst runs | position `awaits`; activity = the run's words as today | the run line is unchanged |
| E-P6 | the stage is completed | the reader returns `""`: the normal flow | never "awaits" over a completed stage |
| E-P7 | a consumer stage outside `CONSUMER_ROUTES` | words from `_role_words(consumer_of(stage))`, no parentheses | a future consumer is still named, never a field id (FR-6) |

**ERROR DIRECTION of the reused functions in a more consequential role** (designer rule 1).
- In K5.e, `_manual_block_door`'s "nothing left" computation (now `_manual_cases_left`), `manual_done_cases`, `prepare_for_block`
  and `live_s6_scopes` feed a GATE that closes S6. They used to be advice (a door) or a driver-only filter.
- The gate may err only toward "something is left" (no close, today's lines).
- Adversarial inputs that must stay on that side, each a row of §5:
  - an underived or non-list scope (C8);
  - a running S6 dispatch (C11), a paused one (C11b), a blocked one (C11c);
  - an automated half with no accepted runner (C5);
  - one case that prepares (C6);
  - a word older than the acceptance (C3b);
  - a reducer failure (C7);
  - a completed S6 with no record (C9b);
  - a block case already done at X2 (C14).
- The one input that errs toward closing is prepare's catch-all refusal (E6). It is the driver's own behaviour, kept for parity and
  reported per case.

## 5. Test rows

### 5.1 `test_story_step_manual_block.py::fv3_22_nothing_left_closes_s6_on_the_skill_road` (new function, registered in `main()`)

The world is built over `real_story(root, MIXED_7)` (WT :48) and the module's `start` helper (WT :80).
- Base world W: the automated half started with `start(root, c, None, kind="automation")` and accepted not-complete with
  `accept(c, root, "S6-qa-runner-1", "automation", ["TC-1"])` (WT :113); every manual case refused by a prepare stub
  (`lambda case: ([], f"refused {case}", "")`).
- The close's scripts are stubbed at ONE seam, `mock.patch.object(stage_close.SkillRoad, "py", fake)`. `fake` records `(script,
  args)`; for `finalize_task.py` it writes `work/run-report.json` (`{}`) and returns `(0, "")`; for `stage_done.py` and
  `project_decisions.py` it returns `(0, "")`.
- The controller is the real one: the receipt, the marker and the state are real.
- Values come from this card (TESTING.md: never copied from the code's output).

| row | world | expected (from) |
|---|---|---|
| C1 | W | exit 0; py calls == [`finalize_task.py`]; `acceptance.awaits_acceptance(c.state(), "S6", <pipeline>) == "S6-qa-runner-1"`; no `code_only` event; S6 not completed. The text holds, IN THIS ORDER: `TC-2: not checked by hand - refused TC-2`, then `S6 awaits the acceptance of qa-failure-analyst for S6-qa-runner-1`, then `card --stage S7`, then the person's door `--block "stage acceptance" --words-file`; `seen["scope"] == []` (§2.3, E20, E21) |
| C2 | W + an accept record for S6 (`reviewed_dispatch: "S6-qa-runner-1"`, `verdict: accept`, acceptor `qa-failure-analyst`) | exit 0; py calls == [`finalize_task.py`, `stage_done.py` with `--status done --digest <reason> --no-journal`]; `c.state()["stages"]["S6"]` has `status: completed`, `code_only: true`; the code_only event's `reason` starts `the manual half of S6: 0 case(s) checked by an agent by hand, 6 not checked: TC-2, TC-3`; `evidence_refs` include `work/run-report.json`; text holds `S6 is closed by code` (§2.3) |
| C3 | W + a live waiver `stage acceptance` on S6 with `at` `2099-01-01T00:00:00+00:00` | py calls start [`finalize_task.py`, `stage_done.py --acceptance work/handoffs/S6-qa-runner-1.yaml --acceptor driver --verdict accept --quote "by: person - <words>"`, `project_decisions.py ... add-finding`], then the close (receipt real, `stage_done.py --status done`); exit 0 (E11 negative) |
| C3b | as C3, `at` `2000-01-01T00:00:00+00:00` | C1's outcome; no `--acceptance` call (E11) |
| C4 | W with prepare READY for every case + the no-stand word (`stage_overrides` as FV3-21b `put`); `start(root, c, "TC-2")` | every TC-2..TC-7 request `== {"refused": {"reason": <word reason>, "door": <the card's door literal>, "by": "left_unchecked"}}`; C1's outcome (E7) |
| C5 | MIXED_7, no automation runner, every case refused | today's lines (exit 2) + the K5.g door line; py never called; no marker (E1, K5.g) |
| C6 | W, TC-7 prepares | exit 2; `door_scope(text) == "TC-7"`; py never called; no marker; no new dispatch, revision unchanged (E5, E18) |
| C7 | W, `finalize_task.py` returns `(1, "boom")` | exit 2; text holds `S6 was not closed: S6 manual half: finalize_task.py exit 1: boom` and a `door:` line; no marker; no code_only event (E8) |
| C8 | W, `c.stage_scope` patched to `{"derived": False, "scope": [], "reason": "x"}` | today's lines; py never called (E2) |
| C9 | C2 then `start` again | exit 0; exactly one code_only event for S6; `finalize_task.py` called ONCE over both starts; text holds `S6 is completed already` and `where --task` (E14) |
| C9b | C2 with the fake `stage_done.py` returning `(1, "refused")` on `--status done`, then `start` again (fake now `(0, "")`) | the first start: exit 2, text ends with the door `stage_done.py --task <T> --stage S6 --status done --digest`; the second: exit 2, the same door, `finalize_task.py` not called again, `S6 is closed by code` NOT in the text (E9, E14b) |
| C10 | every disposition `automate` + an accepted runner | today's lines (manual scope empty); py never called (E3) |
| C11 | W + an S6 dispatch left `running` | today's lines; py never called; no request file rewritten (E4) |
| C11b | W + an S6 manual block TC-2..TC-4 left `paused` | today's lines; py never called; the requests of TC-2..TC-4 have the same bytes as before (E4, verdict F2) |
| C11c | as C11b with status `blocked` | as C11b (E4) |
| C14 | W + the no-stand word, an accepted manual block that carried TC-2, `start(root, c, "TC-2,TC-3")` (X2) | the close reason says `1 case(s) checked by an agent by hand` and does not list TC-2 as not checked; `evidence_refs` (with an accept record as C2) do not name TC-2's request (E17) |
| C15 | the FV3-21b rows S8-S10 | unchanged: `_no_stand_refusal` still returns a list of lines (MF5) |
| C16 | W + an accept record, with `stage_close.SkillRoad.controller` patched to raise `StateConflict("moved")` on `code_only` | exit 2; text holds `S6 was not closed: moved`; S6 not completed (E10) |

### 5.2 `test_story_step_manual_block.py::fv3_22_awaits_position` (new function; worlds as written `state/controller.json` + `pipeline.json` in a temp root, no real story)

| row | world | expected (from) |
|---|---|---|
| P1 | S0-S5 done; S6 runner `S6-qa-runner-1` accepted; `acceptance_awaits.S6 = "S6-qa-runner-1"` | `progress(root)["position"]["kind"] == "awaits"`; `line` holds `waiting for the failure analyst's acceptance (S7)` and `no role running` (E-P1) |
| P2 | S0-S6 done; analyst dispatch accepted with the open-work word `stage_awaits_acceptance` | `line` holds `waiting for the doc scribe's acceptance (S8)` (E-P2) |
| P3 | P1 with `acceptance.awaits_acceptance` patched to raise | `position.kind != "awaits"`; no exception (E-P3) |
| P4 | P1 + a `driver-state.json` `asked` of a gate | `position.kind == "gate"` (E-P4) |
| P5 | P1 with S6 completed in the controller and done in the pipeline | the S6 awaits line is absent (E-P6) |

Existing rows that must stay green unchanged: K-R3..K-R5 (no automation runner -> E1), K-P2, FV3-21b S1-S10 (no automation runner ->
E1; S8-S10 = C15), `test_walk_lanes.py:298` (`_manual_block_door` signature unchanged), the driver's `test_story_run_s6.py` rows on
`manual_close` and the person's pass, and the S7 tests witness-for prints. Volume: two functions, 22 rows. The builder reports the
`in N.NNs` tail of the file (file budget 10 s).

**PROBE** (byte copy, command hygiene point 7):
- (P1) in `_manual_block_check`, delete the X1 call -> C1, C2 red;
- (P2) in `stage_close.manual_half_close`, replace `road.consumer_need_record(...)` by `False` -> C1 red;
- (P3) in `_s6_manual_close` step 4, replace `live_s6_scopes(state)` by a `running`-only filter -> C11b red;
- (P4) delete step 1b -> C9 and C9b red.

Restore from the copy; the witness is a hash comparison.

## 6. Readers of every touched file (designer rule 7)

Commands, this round, with the Grep tool:
- `stage_close|story_step\.py|story_progress|driver_core|driver_stage_s6|driver_stage_s7|driver_dispatch|driver-layers|test_story_step_manual_block|test_story_run_s6|phases/s6|BY_PERSON|live_s6_scopes|consumer_await|consumer_need_record|_no_stand_refusal|manual_close|close_by_code|CONSUMER_ROUTES|_manual_block_check|file_passed_over`
  over `tools/` = 24 hits in 5 files:
  - `controller-blocks-gen.py` (15): door strings naming `story_step.py`. Unchanged: no controller block text changes.
  - `lint-baseline.json:271` (1): `test_story_run_s6.py` HandReaderInput count 2. Unchanged: K5.m adds a check on an existing text,
    not a hand reader. The lint ratchet stays shrink-only.
  - `test_dispatch_gate.py:2302` (1): prose. Unchanged.
  - `test_quarantine.py:2173, 2235` (2): purges `driver-layers.json` rows of deleted test helpers. Unchanged: the deleted rows
    (`BY_PERSON`, an importer row) are not test helpers.
  - `test_test_quarantine.py` (5): its own fixtures. Unchanged.
- `SIBLING_MAP|test-layers\.json|changelog\.d` over `tools/` = 96 hits in 40 files. The ones that read the touched files:
  - `mechanism_gate.py` (7): SIBLING_MAP is a mechanism path, so FV3-22-2's commit carries `axes: not a mechanism (<reason>)`
    (§1.3). It changes in no stream.
  - `owns_readers.py` (6) and `lint_ratchet.py` (3): read the keep/quarantine structure of `test-layers.json`. A `covers` entry
    leaves them unchanged.
  - `test_volume.py` (1): excludes `changelog.d` from volume; the new test rows count, so the builder reports the tail.
  - `architecture_gate.py:12` (1): a `changelog.d` path is a package path, so both commits carry the `architecture:` / `judgment:` lines.
  - `source_split.py`, `test_redundancy.py`, `test_quarantine.py`, `claim_control_gate.py`, `handoff_gate.py`, `gitcmd.py` and the
    rest: read axis headings, axis 31, paths or quarantine rows. Unchanged.
- Over `.githooks/`: 0 hits. Positive control, same folder and tool: `tools/` = 21 hits in 4 files.
- Over `.claude/agents`: 2 hits, both prose (`critic.md:189, 245`). Unchanged.
- Over `.claude/skills`: 0 hits. Control: `Как пишутся правила|journal_write` = 3 hits in 3 files.
- Over `.claude/settings.json`: 0 hits for `stage_close|story_step|story_progress|driver_|test-layers|SIBLING_MAP`. Control:
  `SessionStart|tools/` = 38 hits.

Inside the package (where parallel streams meet):
- `stage_close.py` (new): read by `driver_stage_s6`, `driver_stage_s7`, `driver_dispatch` (node -1), `story_step` (nodes -1/-2) and
  `story_progress` (node -2).
- `driver_core.py`: `BY_PERSON`'s only importer was `driver_stage_s6` (Grep `BY_PERSON` over `scripts/`: `driver_core.py:411`,
  `driver_stage_s6.py:13, 213, 318`, `driver-layers.json:82`; tests have none). It changes in node -1.
- `driver-layers.json`: read by `test_driver_layers.py`, `driver_golden.py` (its `about`, :9) and `tools/test_quarantine.py`. Rows
  change in node -1; run in its DoD.
- `judgment-census.json`: no row names a moved function (Grep of the moved names over the census = 0; control: the same form finds
  `_manual_block_check`, 1 hit). Unchanged.
- Callers of the Driver methods keep the names (delegates).
- The stubs of the moved members: 50 lines in 22 test files (Grep). They keep their effect by E-M6.
- The quarantined readers (`test_stage_acceptance_consumer.py` BOUND_METHODS at WT :38, :372, `test_consumer_close_route.py` :242,
  :264, `test_refuse_case.py`) are not run and not edited.
- `_manual_block_check` callers: `start`, `test_story_step_manual_block.py`, the quarantined `test_controller_scope_expansion.py`.
  `_manual_block_door`'s caller `test_walk_lanes.py:298`: the signature is unchanged.
- `story_progress.py`: read by the driver's `[progress]` line, the dashboard, `test_runtime_paths.py` and `test_s5_plan_windows.py`
  (keep rows `test-layers.json:4713, 4888`, which cover it) and the quarantined `test_story_progress.py`. It changes in node -2;
  witness-for prints the two keep tests.
- `phases/s6.md`: read by `story_step.py card` (`CARD_MAX_BYTES`), by `test_story_step_manual_block.py::the_card_and_the_help_name_the_rule`,
  and by the quarantined `test_role_permissions.py`. It changes in node -2.
- FV3-21's branch owns the same files; this node is sequential after its merge (§0). FV3-23 (`known_red.json`, the dry stub) owns
  none of this card's files.

## 7. Siblings, analogs, and the named nodes

Sweep of the artifact (rule 9): the S6 code steps the driver takes and the skill road lacks, by enumeration.

| driver site | skill road today | verdict |
|---|---|---|
| `s6.manual_close` (`manual_close`) | none | applied: this card |
| `s6.nothing` (`stage_S6` WT :542-553) | none | moved to node FV3-24 |
| `s6.results_stand` (the freshness close; promised by `s6.md:6`) | none | moved to FV3-24 |
| `s6.accepted` (WT :535-541; consumer record, no manual half) | none | moved to FV3-24 |
| `s6_reentry` / `s6.reprobed` | none | moved to FV3-24 |
| `s6_reprove_before_manual` (HF8-18) | none: this card's close runs without the re-proof (Lead F4 = (a)) | moved to FV3-24 |
| the analyst's S6 acceptance on the skill road (Q-a3) | not known to exist: `--acceptance` occurs in `phases/s2-s4.md`, not in `s7.md` (critic m5) | FV3-24; the person's-word door works meanwhile (E21) |

**Lead action (not a fork; outside the designer's write):** the FV3-24 row text in `batch-3-live-run-fvf.md:53` names only the
re-proof and Q-a3. It should name the five sites above by name: `s6.nothing`, `s6.results_stand`, `s6.accepted`,
`s6_reentry`/`s6.reprobed`, `s6_reprove_before_manual`, plus Q-a3 (critic §5 F4). Then no site drops at close.

Axis 5 twins beyond S6 (the dispatch's `siblings:` line): the driver's code-close sites `s7.accepted`, `s7.no_failures`,
`s7.pretriaged`, `s7.after_repairs`, `s7.repair_verdicts`, `s9.skip` and `s9.numbers` (`driver_core.py:391-404`) are Driver-only too.
- `phases/s7.md:15, 42-44, 55-57` promise "S7 closes by code (`code_only`)" on the skill road.
- The package's only non-test writer of `code_only` is `driver_dispatch.py:2549`.
- `stage_done.py:1234-1253` refuses `--status done` on a controller stage the controller has not accepted.
- Whether a skill-road S7 close ever completes was NOT verified by a run this round. This is fork R2-F3.

Analogs noticed, not widened (rule 3):
- a1: the person's-word door command prefix `waiver.py --task <T> --stage <S> --block "stage acceptance"` is written in three places
  (`acceptance.py:1553`, `stage_done.py:1231`, and now `stage_close.person_word_door`). All three render the words part through
  `person_words.door`, the one renderer. The command prefix itself could be one function in `acceptance`; it is not a defect (each
  door is runnable), so this is an offer for the Lead, not this card.
- a2: the driver's word loop `manual_no_stand` (`driver_stage_s6.py`) and the skill road's `_no_stand_cases` are two loops over the
  same per-case body: the same two functions, the same order. Accepted in FV3-21b; the driver's loop is untouched here.

## 8. Forks (recommendation first)

**R2-F1 — node ids under the F5 split (critic m6).**
- (a, recommended) ONE batch node FV3-22 with two builder dispatches and two task_ids. Both dispatches carry `node:
  live-run-fvf/3/FV3-22`; their notes read "part 1 of 2: the move" / "part 2 of 2: the road". The batch file gets no new rows.
  Whether a taken batch may get rows (`docs/TEAMWORK.md` §2) was not read this round. Cost: none.
- (b) add rows FV3-22-1 / FV3-22-2 to `batch-3-live-run-fvf.md` (a Lead edit; `piles.py check`).

The card uses FV3-22-1 / FV3-22-2 as part names in either case.

**R2-F2 — the A27 detector's reach over `stage_close.py` (critic m7).**
- (a, recommended for this node) a named residual in the AR-18 row, plus node -1's grep: every `road.py(` in `stage_close.py` binds
  its result or passes `check=True`. The grep output is attached to the critic. Cost: none. Residual: a later dropped result in
  `stage_close.py` is not seen by A27.
- (b) widen A27 (`audit_factory.py:1652, 2381`): scan `stage_close.py` and recognise `road.py` as `self.py`. Owns would widen by
  `audit_factory.py` and a row in `test_audit_rules.py`. Cost: unknown here, because the scanner is built around the `Driver` class
  and the `NO_MOVE_SEAM` qualnames and was not read in full. (b) is the class fix; (a) is the cheap one.

The Lead decides.

**R2-F3 — the skill road's S7/S9 code closes (axis 5 twins of this card; axis 34).**
- (a, recommended) a new node FV3-25 in the same batch, after FV3-22, with executor scout -> designer -> builder -> critic: "the
  skill road's S7 code closes (`s7.no_failures`, `s7.pretriaged`, `s7.accepted` when the scribe's record stands) and the S9
  person-chosen closes (`s9.skip`, `s9.numbers`) by the same survivor `stage_close.close_by_code` over `SkillRoad`". It is preceded
  by one scout question: "for each site, which skill-road call is the entry, and does any skill-road path already reach a `code_only`
  receipt for S7/S9 (the controller's own projection, a phase command)?". Owns sketch: `scripts/story_step.py`,
  `scripts/stage_close.py`, `skills/qa-story/phases/s7.md` (and `s9.md`), and the keep test its witness names. Test row: a
  skill-road story with no failing test closes S7 code-only, and `stage_done` accepts the record.
- (b) fold it into FV3-24, which already carries five sites plus Q-a3.
- (c) leave it: not legal (designer rule 6; a one-road residual is a node with owns and a test).

## 9. Small choices the designer closed (the Lead can stop any)

- The door fix (E-M2) rides node -1, because the text it fixes moves there. It is the only behaviour change of node -1.
- `BY_PERSON` lives in `stage_close`. `driver_stage_s6` imports it directly, and `driver_core` does not re-export it (its only family
  reader is `driver_stage_s6`; a re-export would leave a stale layer row).
- The evidence hash is inline (E-M5) rather than a shared helper. The controller itself writes that expression in three places and
  judges the result; `driver_core._sha` stays for its own caller.
- `mark_awaiting` is the name of the free body of `consumer_await`, kept away from `consumer_awaits`.
- The `CONSUMER_ROUTES` lambdas `closes_when` and `rework_complete` stay with the Driver. r1 listed `closes_when` among the data keys;
  only `Driver.consumer_awaits` reads it.
- The print order is achieved by capturing stdout in `_s6_manual_close` (`contextlib.redirect_stdout`). No new Driver member (`say`)
  is added.
- Re-entry with the record done prints `next: ... where`, not `card --stage S7`: the story may already be past S7.
- Exit 0 for closed, awaiting and completed-already: sanctioned states with a printed move. Exit 2 for a refused close and for E14b.
- `_no_stand_refusal` keeps its signature (MF5); X2 gets the dict through `_no_stand_cases` / `_no_stand_lines`, not by parsing text.
- `SkillRoad.py` treats a missing script as exit 127 (AR-28), the opposite error direction from `story_step._run`. It is a justified
  second runner (critic §8).
- `story_progress` words come from `stage_close.CONSUMER_ROUTES["who"]` (the Lead's F3 = (a) text), with `_role_words(consumer_of)`
  as the fallback for a stage outside the table.
- The progress rows live in `test_story_step_manual_block.py`, which already imports `story_progress` (WT :31);
  `test_story_progress.py` is quarantined (`test-layers.json:10104`).
- The SIBLING_MAP edit rides FV3-22-2 with `axes: not a mechanism (...)`.

## 10. Verdict t-1195: finding -> where answered

| finding | where answered in r2 |
|---|---|
| F1 (blocking): F3 = (a) not carried | K5.k; §0.2 owns `story_progress.py`, non-goals edited; §1.4 CK8; §4.3 E-P1..E-P7; §5.2 P1-P5; §11 |
| F2 (blocking): live gate checks only `running` | K5.e step 4 via `stage_close.live_s6_scopes`; §1.4 CK3; E4; C11, C11b (paused), C11c (blocked); probe P3; error-direction paragraph |
| F3 (blocking): `BY_PERSON` / `_sha` from `driver_core` | §2.1 table rows `BY_PERSON`, `code_only_request`; K5.l; E-M3, E-M5; §1.3 AR-13, AR-20 rows; §9 |
| F4 (blocking): re-entry after the close | §2.4; K5.e step 1b; E14, E14b; C9 (no second finalize), C9b; probe P4; §1.4 CK7 |
| F5 (blocking): the t-1186 overlap | §0 (start after the FV3-21 merge, MF1-MF7); (a) `consumer_await` -> `mark_awaiting` (§2.1, E-M8); (b) X2 `spent` (K5.f, E17, C14) and the per-case body via `_no_stand_cases`; (c) `live_s6_scopes` into `stage_close`, the importer row deleted (K5.l, E-M4); (d) every line number marked WT, re-read by MF |
| m1: stub invariant / `manual_request_paths` | §2.1 road members + INVARIANT; `manual_half_close` row; E-M6 |
| m2: return shapes | K5.e "Return shape"; E22 |
| m3: census name `_refuse_by_word` | dropped; `_no_stand_cases`; §1.4 name list |
| m4: print order | §2.3 (capture and splice); E20; C1 order assertion |
| m5: Q-a3 / AR-25 door | `person_word_door` (§2.1); the awaiting `next:` (§2.3); K5.i text; E21; C1; also the defect that the old door was unrunnable (E-M2, K5.m) |
| m6: node ids; covers edit in node -1 | §0.1 / §0.2 headers; fork R2-F1; K5.m moves the `stage_close.py` covers edit into node -1 |
| m7: A27 reach | §1.3 AR-18 row; fork R2-F2; node -1 DoD lists `test_no_move_seam_sites.py`, `test_audit_rules.py` |
| axis 26 | K5.j (axis 26 clause); §0.2 `siblings:` |
| tests: DoD lines per behaviour item | §0.1 / §0.2 "Test lines"; the timing tail in §0.2 handoff and §5 |
| positional: X1 writes `request.json` (FB-9) | K5.f POSITIONAL INVARIANT; E18; C6 |
| FV3-24 row text | §7 "Lead action" |
| critic §6 AR-15 note: step 6 duplicates `_manual_block_door` | `_manual_cases_left` (K5.e helpers; §1.3 AR-15) |
| critic §5 Q-a3 only with m5 | E21; §7 table last row |

## 11. Lead decisions (17.11.2026, Opus Lead — «решила сама», until the owner's word), as carried into r2

- Node ids: this card is batch-3 node **FV3-22**; FV3-21d is node **FV3-24**. -> §0.1 / §0.2 headers; §7; fork R2-F1 for the part ids.
- F1 = (a): `scripts/stage_close.py` holds the bodies over a road; the Driver delegates; `stage_close.SkillRoad` serves the skill
  road. -> §2.1, K5.a-K5.d (node -1), SkillRoad in node -2.
- F2 = (a): `start --execution-kind manual` at the exits X1-X3 carries the close; there is no new subcommand. -> §2.2, K5.f, K5.h.
- F3 = (a): position kind `awaits` in `story_progress.progress`, both roads, S6 and S7. -> K5.k; owns of FV3-22-2; §4.3; §5.2.
- F4 = (a): the HF8-18 re-proof and the other S6 code steps go to FV3-24, after FV3-22. -> §7 (with the Lead action on the row text).
- F5 = (a): two builder nodes on one branch, FV3-22-1 (the move) then FV3-22-2 (the road), with one critic pass after the second.
  -> §0.1 / §0.2; R13-g.
- Q-a3: the analyst's acceptance of S6 on the skill road belongs to FV3-24. FV3-22 ends at the awaiting state. -> §7; the awaiting
  state still has a working door today, the person's word (E21).
- A critic on the plan before any builder: done (t-1195). Per PROJECT.md "новая идея" step 6, a second plan pass is only due if the
  r2 fixes change the architecture; the Lead decides whether it does. In the designer's reading, r2 adds no new architecture: it adds
  homes (`BY_PERSON`, `live_s6_scopes`) inside the module F1 already decided.

## 12. Reading trail

Read this round:
- The card r1 (whole) and the verdict t-1195 (whole).
- WT `driver_stage_s6.py` 1-40, 155-379, 520-559, 716-720, 1050-1100, 1986-2006, plus a grep of `consumer_await|live_s6_scopes|s6_live_scopes`.
- WT `story_step.py` 126-153, 753-758, 900-929, 990-1149, plus the `live_s6_scopes` / `stand_passing_word` greps.
- WT `driver_stage_s7.py` 755-789; WT `driver_dispatch.py` 2528-2585; WT `driver_core.py` 300-310, 386-411.
- WT `acceptance.py` 1431-1559; WT `stage_done.py` 1222-1253; WT `controller.py` 2094-2148, 2231-2238, 8793-8808, plus the
  `def apply|stage_scope|state` grep.
- WT `waiver.py` 1881-1895, 1912-1944, 1950-2004; WT `person_words.py` 116-145.
- WT `story_progress.py` 1-72, 239-243, 463-677.
- WT `test_story_step_manual_block.py` the import / def list and 749-857.
- WT `test_driver_layers.py` 140-209, 545-584; WT `test_judgment_census.py` 14-93; WT `scenario_walk.py` 863-866, 888-924.
- WT `driver-layers.json` 1-16 plus row greps; WT `judgment-census.json` name grep; WT `test-layers.json` 6175-6194, 6361-6376,
  plus row greps.
- WT `audit_factory.py` 1645-1669, 2368-2393.
- WT `skills/qa-story/phases/s6.md` 1-12 and `s7.md` 40-58, plus the `code_only` grep over the skills.
- Main: `docs/SIBLING_MAP.md` axis 5 row heads (:130, :133) and axis 26 (:453-455); `plans/piles/live-run-fvf/batch-3-live-run-fvf.md`
  50-53; `docs/TESTING.md` 55-94; `tools/lint-baseline.json` 266-275; the rule-7 greps of §6.

Negative claims and their controls:
- "the WT `driver-layers.json` has no row for `live_s6_scopes` or `Driver.consumer_await`": a grep of
  `consumer_await[^s]|live_s6_scopes|...` over the file hit `Driver.s6_live_scopes` (:1041) and the other named rows. Control: the
  same call found `_sha` :67 and `BY_PERSON` :82.
- "no non-test package file but `driver_dispatch.py` writes `code_only`": the grep `apply\("code_only"|controller\("code_only"|...`
  over the package minus tests found `driver_dispatch.py:2549` plus 2 CHANGELOG lines. The control is that hit itself, in the same
  call.
- "no census row names a moved function": the census name grep found 0. Control: the same form found `_manual_block_check`, 1 hit.
- "the position kind has no reader outside story_progress and tests": 3 files found. Control: the `story_progress.py` hit.
- "`stand_passing_word` is absent from SIBLING_MAP": the axis 26 text (:455) was read directly; it names `split_overridden` readers
  only.
- "`BY_PERSON` has no importer but `driver_stage_s6`": the grep over `scripts/` hit `driver_core.py:411`, `driver_stage_s6.py:13,
  213, 318` and `driver-layers.json:82`, and nothing in tests (the hits `PASSED_BY_PERSON` are another name).
- `.githooks/` 0 hits: control `tools/`, 21 hits. `.claude/skills` 0 hits: control, 3 hits. `.claude/settings.json` 0 hits:
  control, 38 hits.
- "`test_stage_acceptance_consumer.py`, `test_consumer_close_route.py`, `test_role_permissions.py`, `test_story_progress.py` are
  quarantined": their rows sit at `test-layers.json:9979, 7718, 9644, 10104`, after `"quarantine": {` at :7209. The keep rows
  `test_story_run_s6.py` :6175, `test_story_step_manual_block.py` :6361 and the `test_no_move_seam*` rows :3135-3304 sit before it.
- Not verified (labelled as such in the text): whether a taken batch may get rows (R2-F1); A27's full structure (R2-F2); whether a
  skill-road S7 code close completes today (R2-F3).

## 13. Brief contradictions noticed

- The verdict's prose says "7 minor fixes" (m1-m7). The brief says "5 blocking + 11": the eleven are m1-m7 plus axis 26, the DoD test
  lines, the positional FB-9 note and the FV3-24 row text. §10 answers all of them, plus the two critic notes of §5/§6.
- The verdict's F3 recommends that `driver_core` re-import `BY_PERSON`. r2 has `driver_stage_s6` import it directly instead (§9): the
  outcome is the same single definition, and no stale layer row is left behind.
- New in r2, not in the verdict: the old consumer-record refusal's person door cannot be run (`waiver.py` demands the words). It is
  fixed in this node's reach (E-M2, K5.m), per designer rule 2.

## Lead decisions on r2 forks (Lead, 17.11.2026, Opus; «решила сама»)

- R2-F1 = recommended: one node FV3-22 with two task_ids (FV3-22-1, FV3-22-2), no new batch rows.
- R2-F2 = recommended: A27 reach stays a named residual with its grep in the report; the scanner is not widened here.
- R2-F3 = recommended, but the id is **FV3-26** (FV3-25 is taken by the finding «dry world cannot put S5 into fault
  states»): the S7/S9 skill-road code closes are a new node FV3-26 of batch live-run-fvf/3.
- Order: a narrow critic re-review of the five blocking findings of t-1195 first; FV3-22-1 starts from main after the
  FV3-21 merge (t-1186).

## Lead decisions on the re-review t-1209 (Lead, 17.11.2026, Opus; «решила сама»)

Verdict: `docs/tasks/specs/reviews/t-1209-fv3-22-card-r2-rereview.md`. These override §0, §2.1, §2.4, K5.a, K5.b, K5.e step 1b, K5.l, E-M4, MF1, MF2, MF4 and rows C9/C9b where they disagree.

- F4-1, the discriminator "the S6 record is written": NOT the pipeline status (the projection writes `done` from the controller on every apply). It is: S6 `finished` in pipeline.json is present AND not earlier than the time the controller recorded S6 `completed` (the ts of the event the `code_only` reducer applied, `controller.py` ~1949). Facts measured by the Lead in the FV3-21 worktree: `stage_done.apply_stage` (`stage_done.py:815-818`) sets `finished` on done, halted and skipped and pops it on any other status; the projection never sets it. So a halt before the close, or a done before a rework, leaves a `finished` EARLIER than the completion: it reads as not written. Equal times read as written.
  - One named reader: `stage_done.stage_finished_at(pipeline, stage) -> datetime | None`, beside `stage_done.read_pipeline` (the field's writer owns its reader, AR-13); `stage_close` imports it inside the function, as it imports `controller`.
  - Either time unreadable → not written (FR-59 safe side): step 1b falls through to the close, which runs `stage_done --status done` again. Before coding, the builder measures with one command whether `stage_done.py --status done` on an S6 already done is accepted (it re-stamps) or refused; refused → STOP and report (a question to the Lead).
  - C9's fake `stage_done.py --status done` writes the record (or C9 calls the real script) so that C9 is a true positive; C9b stays as written and is red without the fix. One more row: a `finished` earlier than the completion (a halt before the close) reads as not written.
- F4-2: step 1b reads the controller with a `.get` chain (`state().get("stages", {}).get("S6", {}).get("status")`); a missing S6 entry reads as not completed. C5 and the "no automation runner -> E1" rows stay green.
- F5 (t-1186 overtook three facts; the Lead read them as accepted state once FV3-21 merges):
  - `live_s6_scopes` stays in `controller.py` (~690). Its move is DROPPED from §2.1, K5.a, K5.b, K5.l and E-M4; `stage_close`, `story_step` and step 4 call `controller.live_s6_scopes`.
  - AR-13 DoD grep: `def live_s6_scopes` exactly 1 hit, in `controller.py`.
  - K5.l keeps the existing `driver-layers.json` row `Driver.consumer_await` and adds to its note "delegate of `stage_close.mark_awaiting`"; no new row.
  - MF1, MF2, MF4 read as above; §0's re-read on the merged head still stands (a line shift is reported, any other difference STOPs).
- R2-F2: the A27 reach stays a named residual; a node row is owed in batch-3 (Lead, with the FV3-21 status move).
- FV3-26 note: `driver_stage_s7.py:772-775` is the S7 site of the same close; it is FV3-26's, not this card's.
- Order: FV3-22-1 starts from `origin/main` after the FV3-21 wave merges; no further critic pass on these edits (they apply a verdict's own fixes; the Lead checked them against the code).
