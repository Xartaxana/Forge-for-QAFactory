# t-1350 - critic review of E7-3b (commit bdb88db4, branch worktree-u7-e7-3b, base origin/main c5ec1192)

**Verdict: NEEDS WORK. 0 blockers. 3 test fixes (F1-F3) should land before merge; F4-F7 are small.** Whether to accept is the Lead's / architect's decision (critic rule 6).

The product code does what the spec and the plan-review amendments ask. I checked the load-bearing fact the builder only ran over stubs (A1) against the REAL controller, and it holds in both worlds. No road closes S7 or delivers over a counting need that has no answer (A2). I found no double ask, and no world where the question is owed and never asked (A3). I found no paid-round loop (A4). The gaps are in the tests:
- No row goes through `stage_S7`.
- No row goes through the `take_answer` branch.
- No row covers the held-answer road.

So the two step positions, the answer routing and the story-only road can each be removed and every test still passes.

## Blockers

None. I walked all five blocker classes:
- (1) Close or deliver over an unanswered need: A2, every road traced.
- (2) A paid round in a loop or on an unknown: A4, the mark key, M5.
- (3) An instance the person did not allow: the re-walk runs only on `authorized is True`, from a registry row typed by `PK.instance_answer` or from a held answer that is a `bool`.
- (4) A stop with no door: `stop` holds the question and a rerun asks it again; an unread answer goes to the seam once.
- (5) Red checks: the two DoD tests and A27 are green; the other registries are the architect's runs.

## Fixes

- **F1 (fix before merge; Q5 a/c, killing power).** No test row reaches `driver_stage_s7.py::stage_S7`.
  - The rows call `s7_extra_instance_step` directly (`e7_step`), plus `s7_repairs`, `_answer_extra_instance` and `completion_for`. A grep of the new test for `stage_S7` finds nothing.
  - So deleting the main call (driver_stage_s7.py:95-96, the N2 position) or the M9 call (:75-76) survives the suite.
  - These two positions are what the node exists for ("no close over a need with no answer").
  - Needed: one row that enters `stage_S7` in world B. That world has an accepted fresh triage and a need record with no answer (Tests row 2 of the card, "-> Person, no s7_close"). It must assert that the Person is raised and no close or analyst runs. The M9 variant adds an accept record from the scribe.
- **F2 (fix before merge; Q5 c).** No row covers the `take_answer` branch `elif kind == "extra_instance"` (driver_machine.py:3464-3468).
  - The answers row calls `driver._answer_extra_instance(...)` directly.
  - If the branch is deleted, the answer falls through to the generic branches. No row catches that.
  - Needed: one answer through `take_answer` (or the `--answer` door). That can replace one of the three direct token rows, so the budget stays the same.
- **F3 (fix before merge; Q5 c).** The held-answer road has no row. It is a new behaviour at a door:
  - the written state `extra_instance_held`;
  - the answer id `held:<at>` that the step reads;
  - the story-only lead and `says` variant.

  The road starts when the registry write is refused: no stand chosen, a story that leaves no trace, or a registry that cannot be written. Every answer row uses stand `staging` in a story that leaves a trace. A swapped key (`stand|need` written, a different key read) or a lost held answer would pass every row. That breaks the card edge "the answer's write refused -> held for this story (INV: an answer is never lost, never widened)". Needed: one row with the placeholder stand: answer `start it` -> no registry row, `extra_instance_held` written, then the next step reads a yes and re-walks.
- **F4 (fix; Q6).** `s7_extra_instance_story_only` calls the private `PK._refuse_no_trace` (driver_stage_s7.py:652). A public door exists:
  - `external_writes.closed_by_run(task_root)`, which the PK docstring at project_knowledge.py:640 names "the one reader of `no_trace`";
  - and `Driver.no_trace()` (driver_core.py:685), which reads differently: the launch record plus `pipeline.json`.

  The private helper has one useful property: an unknown reads as story-only, which is the safe direction. Either make it public in PK, or call `external_writes.closed_by_run` inside the builder's own try/except with the same fail-closed direction.
- **F5 (fix; Q6, small).** The path of the note file is spelled twice:
  - `EXTRA_NOTE_REL = "work/extra-instance.json"` (driver_stage_s7.py:12);
  - `Path(task_root) / "work" / "extra-instance.json"` (check_delivery.py:1987).

  Its one writer and its one reader should share one constant. Another option is the package resolver `contract.artifact` / `artifact_write_path`.
- **F6 (fix; Q7).** `s7_extra_instance_step` is 68 lines (driver_stage_s7.py:542-609, 8 of them docstring), so it is at the ~60 line threshold. Its nesting is 4 deep: method, `for need`, `for case`, `if/elif`. Moving the per-case classification of a yes into a helper would bring both under the limit.
- **F7 (note; edge letter).** The second call in `s7_repairs` (driver_stage_s7.py:482-485) reads `controller_state()`, `pipeline()` and `awaits_acceptance` before the step, on every entry, even when there are no need rows. The card edge says "no need record -> no read beyond run-report.json". These reads are pure, so a story without a need still runs as today. Only the letter of the edge is broken. Moving the two reads after a cheap need check would fix it.

## Notes

- **N1 (a world nobody has run).** World B with S7 waiting for the scribe (the marker is set and an accept record stands) is reached only through the M9 position. In that world a yes re-walk then lets `s7_closed_by_scribe` close S7 over the old triage. `fresh=self.s7_fresh` refuses that close when the re-walk leaves a failure with no triage row. A re-walk that passes, or that leaves a need record again, closes as the spec intends. Neither A1 nor any test built this world. Risk is low.
- **N2.** `need_why` is already cut at 300 characters by E7-3a before `masked_words` sees it. A secret that crosses the cut is matched only on the part that is left. That is outside this diff.
- **N3.** The delivery words still show `need_why` unmasked (E7-3a / Q-B code, check_delivery.py:2023). The question masks the same words. This is outside this diff but on the same surface: a candidate for the Lead's «Остатки» if wanted.
- **N4.** The placeholder-stand test is spelled in three places: `s7_extra_instance_story_only`, `_answer_extra_instance` (`stand.strip() and stand != PK.PLACEHOLDER_STAND`), and `PK.instance_answer` (`no_stand`). These are small copies of one predicate.

## Per key

| Key | Answer | Evidence |
|---|---|---|
| A1 | **Holds, reproduced on the real controller, both worlds.** | Scratch run (below). It uses the `test_fixes_13797.s6_story` / `runner` rig (the rig of `test_s7_rejudge.py::q9b2`) and the real `Driver` from `driver_for`. The real `Driver.rework` runs through the controller CLI and the real `s7_extra_instance_rewalk`; only `run_role` and `walk_before` are stubbed. **World A** (`S6-manual` accepted with `stage_awaits_acceptance`): S6 is `pending`, `next` is S7, `awaiting='S6-manual'`. The rework `--cause question_answer` is ACCEPTED: `S6-qa-runner-3` is `running`, kind `manual`, cause `question_answer`. `run_role` got `complete=OpenWork(stage_awaits_acceptance)`. The lines are the recorder lines + `ALLOWED_LINE` + the role lines. `completion_for` on that id returns `OpenWork stage_awaits_acceptance`. The accept goes through with message `''`. After it: S6 `pending`, `next` = `prepare_stage S7`, and `awaits_acceptance` = `S6-qa-runner-3`, so the analyst's word binds the new dispatch. **World B** (S6 completed, S7 analyst accepted): the rework is accepted the same way and `run_role` got `complete=False`. `completion_for` returns `False` and the accept gives `''`. After it: S6 stays `completed`, `next` = S7, and the analyst stays `accepted`. `_s6_completion_problems` is never consulted because `stage_complete` is False, and the rework carries `execution_kind: manual` (`build_rework_request` `_rework_kind`). |
| A2 | **Holds.** | Roads in driver_stage_s7.py, in order: `consumer_settled` (:80) settles S6 only, no S7 close. M9 step (:75) then `s7_closed_by_scribe` (:77). Main step (:95) then `s7.no_failures` (:107), `s7.pretriaged` (:140), the investigation dispatch (:927, reached through `s7_investigation_gate` at :103 / :136 / :763) and the analyst dispatch (:162). `s7_repairs`: the re-judge loop (:478) is followed by the second step (:482-485), and that comes before `s7_open_work_ask` and `s7_close` (`s7.after_repairs`, :792). The `"close" in decided` return (:465) closes nothing, and the main step already ran in that entry. A restart: a question pending makes `where` return S7, which runs the step again. A re-walk that is running makes `where` go to `wait_existing_job`, which calls `completion_for` M1 (shown real in A1). `driver_machine.take_answer` closes nothing. **M9:** `s7_closed_by_scribe` returns False at once unless `consumer_pending("S7")` holds (:180-181). The guard tests the same predicate first, and nothing between the two calls changes it. So I found no world where the scribe closes S7 over a need while `consumer_pending` is False. |
| A3 | **No double ask found; none owed and unasked.** | The question raises a `Person` and ends the entry, so the three call sites in one entry cannot ask twice. A restart or a rerun with no answer shows the same held question; `extra_instance_asked` is rewritten and `stopped` is kept. `stop` sets `stopped` and raises `held_question`; the rerun asks with "You answered `stop` earlier." (spec). An unread answer goes to `unread` once (builder row: conductor calls +1); the conductor's `continue` re-enters S7 and the step reads whatever the conductor recorded. A revoke makes `instance_answer` return None, so the question is asked again (spec). Owed but never asked: only when `failures_to_triage` raises for a halted run (by design, INV i). An unreadable registry asks (`authorized` None). `INSTANCE_NEEDS = ("another_instance",)`, so there is one need and one question. |
| A4 | **Holds; no loop.** | The mark key is `extra_instance_rewalk["<case>\|<answer id>"]`, and it is written in `registered` before `run_role`. A new need record after the re-walk (same case, same yes) finds the mark and only gets the "walked again" note. Its `ended_at` is also newer than the answer, so it would not be owed even without the mark. Equal moments, a newer record and an unparseable moment are not owed and get a note (builder rows, M5: `moment != -inf`, any unreadable row spoils the case). `ReworkRefused` sets the mark to `refused` and is never retried. A running S7 dispatch means `continue`: nothing counted and no rework. "Neither world" means a note and False, with no mark and no paid call. A `Refusal` that comes before `controller rework` (drain or cap) registers nothing, so no round was paid. |
| A5 | **Holds; private call found (F4); held road not tested (F3).** | `PK.record(key=EXTRA_INSTANCE_KEY, environment=stand, element=need, state=KNOWN, scope="stand", value={"authorized": allowed}, words=words, source="person", by="driver", ...)` (driver_stage_s7.py:719-721). `by hand` writes authorized False and `stop` writes no row (builder rows; I read the code). A refused write (placeholder stand, the `PK.record` problem, or an exception) holds the answer under `extra_instance_held["<stand>\|<need>"]`, and the step reads it under the same key (:578). Tokens go through `s0_normalize` against a closed list, the same as `_answer_open_work` (:528 vs :706); free words go to `unread`, never to `allowed`. |
| A6 | **Holds.** | `unprepared_records`: a need row is `head + "; " + (note why or the fixed words) + "; what the runner would start and why: " + need_why [+ not walked]`. That matches §2.6. Rows without `need`, and the whole `prepared`-without-`need` sentence, are untouched by the diff. The six `why` clauses in the step match §2.6 word for word: no, refused, re-walked, newer, unparseable, neither. `extra_instance_outcomes` uses `hooklib.read_json(..., {}, kind=dict)`, which catches OSError and ValueError and checks the type. Another `schema_version` or a non-table `cases` gives `{}`. Builder rows cover the absent, unreadable, another-schema and not-a-table cases, and green for need-less rows with and without outcomes. Ran: `test_f5_unprepared_walk_is_a_left_item` passed. I did not run a before/after diff of the module: the need-less branch has no changed line. |
| A7 | **Identical, including the assigned-walker branch.** | driver_stage_s6.py:1826-1855. `manual_block_lines` returns the old walking line (or the old recorder lines) unchanged, as a fresh list. The assigned branch `extend`s that same `extra`, in the same order. The walk-supply line moved from inline code to `masked_words(words)`, which has the same body: `load_config` with ValueError giving `{}`, then `secret_pattern_hit` with ValueError counting as a hit. The two removed imports (`guard_secrets`, `MC`) are now inside `masked_words`, which is called inside the same outer `try/except Exception: pass`. So an import or config failure still drops only that line. No line can differ. |
| A8 | **Rows match the code; no other registry demands a row.** | The A27 row `('driver_stage_s7.py','Driver._answer_extra_instance','P','builder:held_question'): 1` is the `raise self.held_question(...)` on `stop` (:713). It mirrors the `_answer_open_work` row and is necessary: the stop must hold the question. MAX 55 -> 56 has its reason. Ran: `audit_factory.py --no-move` gave `counted 56 baseline 56 new 0 stale 0 ... clean`. The question-prices row matches Work (7) verbatim. driver-layers has 9 methods (all exist) and 3 state keys, which matches the code. The state-exits rows cover the 3 keys plus the note file. Judgment census: no new unit name matches `UNIT_NAME_RE` (`check_`/`rule_`/`judge`/`validate`/`refuse` prefixes, `_check`/`_errors`/`_problems` suffixes). Artifact-writers covers only files that `stages.json` declares; other files the driver writes (`work/ticket-freshness.json`) are absent from it too, so no row is owed. The architect's runs decide this. |
| A9 | **Masking holds; I found no length limit.** | `masked_words(why)` runs before `s0_quote` (QUOTE_LIMIT 300 plus the ellipsis). An exception means `(not shown: they look like a secret)` (builder row: secret masked). `closed_question` (driver_runner.py:1295) is lead + priced section with no cap. `judge_own_question` (driver_dialog.py:390-420) never withholds a question; it logs rule breaks (M18 accepts that). Measured: a lead with 10 cases x 300 characters + "and 3 more" is 3435 characters, and `human_text.problems` names no length rule for it. |
| A10 | **Budget OK; three rows missing (F1-F3).** | Numstat: tests +182 (153 + 28 + 1), product code +313 (s7 237, s6 44, check_delivery 16, plan 9, machine 5, audit 2), so tests <= product. **Through a real road:** row 8 (the real `s7_repairs`, with stubs around it), row 9 (unit level at `unprepared_records` / `extra_instance_outcomes`; the `assess` call site is not driven), row 4 (the real `PK.record` registry), row 7 (`completion_for` over a stubbed controller state). **Direct step call over stubs:** rows 1, 2, 3, 5, 6, 10. With `rework` stubbed, three things stay unproven in the suite: that the controller accepts the re-walk, that the next stage after it is S7, and that `walk_before` really runs. My A1 scratch proves the first two once. The `failures_to_triage` raise in row 6 is a stub, so only the propagation is proven. Missing: the `stage_S7` positions (F1), `take_answer` (F2) and the held road (F3). |
| A11 | **None outside.** | `--stat`: 13 files. All are in the card's owns, plus `driver_stage_plan.py` (M1) and the changelog fragment. |

## Seam and class notes

- Q3 seams: additive. The `take_answer` branch sits right after `open_work`, as the spec says. The `completion_for` branch sits after `s7_rejudge` and before the S6 rule. The `run_manual_lane` extraction keeps its output (A7).
- Q4 class: the restart twin (`completion_for`) is done. The sibling site question (`open_work`) is mirrored. The skill-phase road is driver-only by M2 (accepted). No sibling is left in the SIBLING_MAP axes I walked: restart twins, site questions, readers of need rows.
- Q6: F4, F5, N4. `masked_words` and `manual_block_lines` are extracted, not copied.
- Q7: F6. `analyst_done` is unused, as the docstring says: it is part of the call's shape.
- Q8: no Cyrillic in the diff (Perl-regex grep; the positive control found 1); EOL is LF, as in the index.
- Q9: one shrink-only raise. A27 `NO_MOVE_BASELINE_MAX` goes 55 -> 56 for row `Driver._answer_extra_instance` P held_question; it is named in the code with its reason.
- Q10: AR-13 (one copy of the lines and the masking), AR-17 (no paid call for the question), AR-24 (the registry row by the driver). The commit names them and nothing is starved.
- Q10 VARIETY: an unknown stand, a story that leaves no trace, or an unreadable registry each give a story-only question and a held answer. An unknown moment is not owed. There is no silent default.
- Q11: no judgment moves into code; the step selects by a data key and compares moments.
- Q12: none found. The searches were the stand-name branches in the diff (`PLACEHOLDER_STAND` only) and language or runner names (none).

## Spot-checks of submitter claims

- "Row 2 calls the step directly; no row exercises a walking re-walk": confirmed by reading the test diff.
- "`by hand` is not a move word" (needed for the unread doors): `NM.reserved_tokens` = approve, go on, prepare the stand, restart, retry, rework, stop. `site_check(('start it','by hand'))` passes.

## Trail

- Read: the spec r2 §2.1-§2.8 and the E7-3b card; the review t-1307 (M1-M18); the whole diff. Code read in the worktree:
  - `driver_stage_s7.py` 17-240, 458-760;
  - `driver_stage_plan.py` 1210-1270;
  - `driver_stage_s6.py` 160-190, 1682-1860;
  - `driver_dispatch.py::rework` 2843-2895;
  - `controller.py` `build_rework_request` 3737-3990 and `_s6_completion_problems` 4722-4758;
  - `acceptance.py::awaits_acceptance`;
  - `project_knowledge.py` 498-540 and 639-655;
  - `manual_evidence.py::unprepared_rows`;
  - `check_delivery.py` 1979-2030 and 2749;
  - `hooklib.read_json`; `driver_core` `_read_json` / `_write_json`;
  - `stand_gaps.stand_name`;
  - `driver_conductor` `_no_move` and `unread`; `no_move` `reserved_tokens` / `site_check`;
  - `driver_runner.closed_question`; `driver_dialog` `judge_own_question` / `s0_quote` / `s0_normalize`;
  - `test_s7_rejudge.py` q9b / q9b2; `test_fixes_13797.py` s6_story / runner.
- Runs (tails):
  - `python -m pytest .../test_no_move_seam_sites.py::test_e7_extra_instance_trigger -q` -> `1 passed in 78.94s`
  - `python -m pytest .../test_check_delivery.py::test_f5_unprepared_walk_is_a_left_item -q` -> `1 passed in 1.61s`
  - `python -B .../audit_factory.py --no-move` -> `A27 totals: ... counted 56 baseline 56 new 0 stale 0` / `A27 no move outside the seam: no violations` / `=== Result: clean ===`
  - The A1 scratch was given to `python -B -` on stdin; no file was written. The handoff gate refused a scratch file in the temp dir, so stdin was used instead. Key lines:
    - `A manual awaits: ''` / `A S6 status pending | next: {'action': 'prepare_stage', 'stage': 'S7'}` / `A awaiting = 'S6-manual'`
    - `A new S6 dispatches: {'S6-qa-runner-3': ('running', 'manual', 'question_answer')}` / `A run_role complete passed: OpenWork stage_awaits_acceptance`
    - `A completion_for(re-walk id): OpenWork stage_awaits_acceptance` / `A accept of the re-walk: ''` / `A after: S6 pending | re-walk accepted | next: {'action': 'prepare_stage', 'stage': 'S7', 'dispatch_id': None}` / `A awaiting after = 'S6-qa-runner-3'`
    - `B S6 status completed | next: {... 'S7'}` / `B new S6 dispatches: {'S6-qa-runner-3': ('running', 'manual', 'question_answer')}` / `B run_role complete passed: bool False`
    - `B completion_for(re-walk id): bool False` / `B accept of the re-walk: ''` / `B after: S6 completed | re-walk accepted | next: {... 'S7' ...}` / `B S7 dispatches: {'S7-qa-failure-analyst-1': 'accepted'}`
  - `human_text.problems` on a lead of 10 x 300 characters: `3435` / `['no_how_to_answer', 'price_lines', 'price_lines', 'price_lines']`. These rules fire because only the lead was passed, without the priced section; none is a length rule.
  - `NM.reserved_tokens`: `['approve', 'go on', 'prepare the stand', 'restart', 'retry', 'rework', 'stop']`, `by hand` False; `site_check` gives `['start it', 'by hand']`.
  - Cyrillic grep over the diff: no lines; the control `printf 'x\xd0\xb0y'` counted 1.
  - `git ls-files --eol`: `i/lf w/lf` for `driver_stage_s7.py` and `check_delivery.py`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F1 (fix before merge) no test row enters driver_stage_s7.py::stage_S7: deleting the main step call (:95-96) or the M9 call (:75-76) survives; add one world-B stage_S7 row (accepted fresh triage plus a need with no answer -> Person, no close, no analyst)",
    "F2 (fix before merge) the take_answer branch driver_machine.py:3464-3468 is not driven by any row; route one answer row through take_answer",
    "F3 (fix before merge) the held-answer road (placeholder stand or no-trace, so PK.record is refused -> extra_instance_held -> step reads held:<at> -> re-walk; story-only lead) has no row",
    "F4 s7_extra_instance_story_only calls private PK._refuse_no_trace; public door external_writes.closed_by_run (or make the PK helper public), keeping the fail-closed direction",
    "F5 the note path is spelled twice: driver_stage_s7.py:12 EXTRA_NOTE_REL vs check_delivery.py:1987; share one constant or contract.artifact",
    "F6 s7_extra_instance_step is 68 lines (542-609) with 4-level nesting; extract the per-case yes classification",
    "F7 s7_repairs second call reads controller_state/pipeline/awaits_acceptance before the step even without need rows (edge letter: no read beyond run-report.json)"
  ],
  "class_completeness": "Restart twin completion_for done (M1, real controller proven in A1); sibling site question open_work mirrored (doors, normalisation, held stop, unread once); readers of need rows unchanged except unprepared_records (need branch only); the skill-phase s7 road is driver-only by accepted M2. No sibling left on the SIBLING_MAP axes walked.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261118-u7-e7-another-instance-spec-r2.md sections 2.1-2.8 and the E7-3b card",
      "docs/tasks/specs/reviews/t-1307-u7-e7-plan-r2.md M1-M18",
      "worktree diff origin/main...bdb88db4 (13 files)",
      "driver_stage_s7.py 17-240, 458-760",
      "driver_stage_plan.py 1210-1270",
      "driver_stage_s6.py 160-190, 1682-1860",
      "driver_dispatch.py rework 2843-2895",
      "controller.py build_rework_request 3737-3990, _s6_completion_problems 4722-4758",
      "acceptance.py awaits_acceptance; project_knowledge.py 498-540, 639-655; manual_evidence.py unprepared_rows",
      "check_delivery.py 1979-2030, 2749; hooklib.read_json; stand_gaps.stand_name",
      "driver_conductor _no_move/unread; no_move reserved_tokens/site_check; driver_runner closed_question; driver_dialog judge_own_question/s0_quote/s0_normalize",
      "tests/test_s7_rejudge.py q9b/q9b2; tests/test_fixes_13797.py s6_story/runner; tests/test_no_move_seam_sites.py e7 rows"
    ],
    "reruns": [
      {"command": "python -m pytest <wt>/ai-packages/qa-factory/scripts/tests/test_no_move_seam_sites.py::test_e7_extra_instance_trigger -q", "result": "1 passed in 78.94s"},
      {"command": "python -m pytest <wt>/ai-packages/qa-factory/scripts/tests/test_check_delivery.py::test_f5_unprepared_walk_is_a_left_item -q", "result": "1 passed in 1.61s"},
      {"command": "python -B <wt>/ai-packages/qa-factory/scripts/audit_factory.py --no-move", "result": "counted 56 baseline 56 new 0 stale 0; no violations; clean"},
      {"command": "A1 scratch on stdin: real controller worlds A and B, real Driver.rework and s7_extra_instance_rewalk, completion_for then accept", "result": "A: rework question_answer accepted, complete=OpenWork awaits, after accept next=S7, awaiting=new id; B: accepted, complete=False, S6 stays completed, next=S7, analyst stays accepted"},
      {"command": "human_text.problems on a 10x300-character lead; NM.reserved_tokens/site_check; Cyrillic grep with positive control; git ls-files --eol", "result": "3435 characters, no length rule; by hand not reserved, site_check passes; no Cyrillic (control 1); LF"}
    ]
  }
}
```
