# t-1307 - plan critic of U7 / E7 r2 (another instance of the stand or device, asked once when needed), node universality/1/U1-11

Spec under review: `docs/tasks/specs/20261118-u7-e7-another-instance-spec-r2.md` ("r2"). First edition reviewed in t-1295 (amendments N1-N11).
Base: `git -C C:/QAFactory/forge-repo rev-parse HEAD origin/main` -> `9401f019...` twice, so the root checkout equals origin/main; `git status --short -- ai-packages/qa-factory` printed nothing (package clean). r2 was written on 6be36343; the delta 6be36343..9401f019 is FV3-22 (`stage_close.py` new; `driver_stage_s6.py` -215/+, `driver_stage_s7.py`, `driver_dispatch.py`). Every symbol r2 cites still exists (`run_manual_lane`, `consumer_awaits`, `consumer_settled`, `close_by_code` now delegating to `stage_close`). Nodes 7b-B (branch `worktree-u7-7b-b`) and 7c are not merged. E7-1 is built on `worktree-u7-e7-1` (cf5a9bf6); its `instance_answer` signature matches what E7-3b and E7-2 expect.

Terms used below. "Need record": an unprepared manual record whose marker carries `need: another_instance`. "Re-walk": the S6 runner rework that S7 starts after a "yes". "World A": S6 awaits its consumer (the failure analyst) when S7 is entered. "World B": S6 is completed (the rework happens inside an open S7). "Skill road": the conductor working a story from `skills/qa-story/phases/*.md` without the driver. "Restart road": a dispatch finished after a driver restart (`wait_existing_job`, `resume_role`), which takes its `complete` from `driver_stage_plan.py::completion_for`, not from the live caller.

## Verdict

**NEEDS WORK: r2 is ready for builders after the listed amendments.** M1-M5 block the dispatch of E7-3a / E7-3b (failure_class: spec). M6-M17 are fix-before-dispatch text edits. E7-1 is not reopened: no finding blocks it. The decision to accept stays with the Lead / architect (critic rule 6).

## A. Blocking amendments of t-1295 (N1-N5)

- **N1 - closed in part.** r2 §2.3 states both worlds with their `complete=`, the lines by source symbol, and the walk road through `walk_before` inside `on_request`. Checked: `driver_dispatch.py::run_role` (the `after is None` block) finds `state/walks/<id>.json` and wires `walk_after`, so the walk road works as r2 says. `controller rework --stage S6` while S6 awaits is accepted by code (C1 below). **Left:** the restart road. `driver_stage_plan.py::completion_for` knows the S7 re-judge dispatches (`state["s7_rejudge"]` -> `False`) but not the E7 re-walk. For an E7 re-walk finished after a restart it applies the plain S6 rule: in world A, if the walk build was refused (`walk_pending(mine)` is True) it returns `False`. Then no awaits word is sent, `awaits_acceptance` reads `""`, and `controller.next` re-plans S6. That breaks N1's invariant. In world B with no consumer it can return `True`, which breaks "`C` is never True". -> **M1.**
- **N2 - closed in part.** The position is right (`driver_stage_s7.py::stage_S7`: after the freshness block, before `if not analyst_done:`), and invariants i-iv hold as traced in E. **Left:** the second call (F-r2-1) has no stated arguments or return handling (M6). The `s7.accepted` close of `s7_closed_by_scribe` is not in the invariant's list of closes and is not argued (M9).
- **N3 - closed** (r2 §2.6 plus the run file of F-r2-2). The need branch replaces the false "could not prepare" words. Exception: need rows that the validator refused still reach these words (M3), and the 3a-only window still shows the old words (F, M10).
- **N4 - closed.** `--need-why` is stored as `unprepared.need_why` on both roads, and the walk road copies `limitation` into it. Checked against `manual_evidence.py::write_unprepared`: its "was walked ... leave --not-walked out" refusal guards `not_walked`, not the new field, so a walked case keeps its reason.
- **N5 - closed.** `told-ratchet.json` joins E7-3a's owns, with `write_unprepared` bare 4 -> 5. The scanner counts one site per `raise` (C6). Condition to write into the card: `need_record_problems` must never raise (M13).

## B. N6-N11

- **N6 - closed in part.** The validator guard is written (E7-3a Work 2). But `finalize_task.py` keeps the `unprepared` marker on a record it refuses (it only adds `result: inconclusive` and `evidence_errors`), and `manual_evidence.py::unprepared_rows` selects rows by "marker not None". A refused or stale need record therefore still reaches the S7 step (the person is asked about it) and the §2.6 words. -> **M3.**
- **N7 - closed.** The key is `extra_instance_rewalk["<case>|<answer id>"]`, and equal moments are not owed. The detection of an unreadable moment is a separate defect (M5).
- **N8 - closed.** Cap of 10 plus "and K more", masking, batteries, and `walk_rule_errors` refusing while the session lives. The lead's 300-character cut cannot be reached: the record is already cut at `NOT_WALKED_MAX` = 300, and `driver_s0.py::QUOTE_LIMIT` = 300 (H).
- **N9 - closed in part.** The commands are exact, but two are broken. (1) The E7-3b line `pytest test_audit_rules.py::test_a27_baseline`: the file runs its whole battery at module level (`try: test_a1() ... test_a27_battery()`) and then calls `finish(...)`, which is `sys.exit`. Collecting that one id therefore runs the whole slow file and ends in SystemExit, and `test_a27_baseline` asserts nothing (it uses `check`). (2) The E7-2 line names `test_ss1_11_stand_lessons`, which does not exist (only `ss1_11_stand_lessons`), and no E7-2 Work item creates it. -> **M4, M11.**
- **N10 - closed.** The doors' `says`, every printed line and the lead are written out. A new gap of the same kind: the runner-facing `ALLOWED_LINE` has no text (M7).
- **N11 - closed in part.** The base moved again to 9401f019 (FV3-22 touched E7-3b's `driver_stage_s6.py` and `driver_stage_s7.py`). §5 still rests on the block of base 76768bac. t-1294 was accepted (`logs/journal/dev1.jsonl`, 2026-11-18T00:42:43). `controller.py` has not changed since 76768bac (`git log 76768bac..origin/main -- controller.py`: empty), so `manual_blocks` and `MANUAL_BLOCK_CASES = 5` stand. -> **M17.**

## C. Section 7 items

1. **`rework --stage S6 --cause question_answer` while S6 awaits: accepted (by code reading, no run).** `controller.py::build_rework_request` has no check on S6's status, and `question_answer` is in `REPAIR_CAUSES`. The `dispatch` apply checks only the stages below the target (`controller.py` op `dispatch`: `any(... f"S{i}" ... for i in range(n))`, so S0-S5 for an S6 dispatch). Live precedent: `driver_stage_s6.py::consumer_settled` already reworks S6 while it awaits, with `complete=route["rework_complete"]` = `consumer_awaits("S6", True)`. **The awaits word does not reach `_s6_completion_problems`:** an `OpenWork` finish is "not complete" (`driver_dispatch.py`, branch `isinstance(complete, OpenWork)`), and the check runs only `if d["stage"] == "S6" and p.get("stage_complete")`. The first seam row of E7-3b stays the run proof.
2. **Readers of `walk_retry`: not only S6.** Grep `walk_retry` and `walk_pending(` over `scripts/`: the readers are `driver_dispatch.py::walk_pending`, `driver_stage_s6.py::manual_todo`, `driver_stage_s6.py::manual_plan`, `driver_stage_s6.py::run_manual_lane`, **and `driver_stage_plan.py::completion_for`** (the restart road). Positive control: the same grep finds the writers at `walk_case_records` and `walk_after`. Live road: an inert leftover (S6 is not entered again in world A or B). Restart road: it is the mechanism of M1.
3. **Writer census: no row demanded.** `test_artifact_writers.py::every_declared_artifact_has_an_owner` demands a row only for `stages.json` `outputs`. An extra row must be "real" (its basename appears in `scripts/*.py`). `work/extra-instance.json` is not a stage output, so it needs no row; the `state-exits.md` row is enough.
4. **No length limit applies to the lead.** `driver_runner.py::closed_question` joins the lead and the priced section with no cap. `driver_dialog.py::judge_own_question` never refuses ("asked anyway"). `human_text.problems` has only a `too_short` length rule. `no_move.py::CONDUCTOR_TEXT_LIMIT` = 1200 cuts only the conductor's own text (`conductor_found`), not a site lead. Search: Grep `(LEAD|QUESTION|TEXT|WORDS|BODY)_?(MAX|LIMIT|CAP)` (case-insensitive) over `scripts/*.py`; positive control: the same call found `PROBE_GAP_LEAD_LIMIT` and `QUESTION_LIMIT`.
5. **Measured: pytest collects a `test_` wrapper without running `main()`, except in `test_audit_rules.py`.** Scratch file `C:/Users/i_mas/AppData/Local/Temp/claude/b3e3188b390a00d9/1d2edd69-11a3-4cc2-8484-fbd7325289b0/scratchpad/c5/test_wrap_probe.py` imports `test_state_exits` and checks that `harness.RESULTS` is empty after the import. It then runs one scenario and asserts. A planted failing check is the negative control. Output tail: `FAIL planted failure` ... `1 failed, 1 passed in 2.28s`. Exception: `test_audit_rules.py` runs its battery and `finish()` at import (N9). Caveat: `harness.RESULTS` is shared by the whole process, so a wrapper must judge only the slice it added (M16).
6. **One site per `raise`: true.** `refusal_registry.py::_scan_wide` emits one record per `raise <Call>` node of the exception family. `list` appends count only inside units that block. Measured with `test_judgment_census.units_of` on the tree (101 s): `write_unprepared` blocks=True (u3); `walk_rule_errors`, `_validate_unprepared`, `verdict_problems` and `record_problems` all blocks=False. So 3a's new list texts add nothing, and the new `raise` adds exactly 1, provided `need_record_problems` itself never raises (M13).

Remaining §7 items: the base is clean and the delta is read (header); t-1294 is accepted (N11); `manual_blocks` is unchanged (N11). The file is 58,331 bytes by `wc -c`; r2 says 57,914, so it was edited after it was measured.

## D. The two decided forks

- **F-r2-1 (a) leaves two roads uncovered.** (1) What the second call receives and does. `s7_repairs` has no `analyst_done` or `awaiting`. It is reached in world B, and also in world A when `consumer_settled` returns False with an older accepted analyst (`record.reviewed_dispatch != awaiting and done and not mine`). On `True` it must `return` before `s7_open_work_ask` and `s7_close`; r2 never says so (M6). (2) Its restart twin. Re-judge dispatches are registered in `state["s7_rejudge"]` for `completion_for`, while E7 re-walk ids are not (M1).
- **F-r2-2 (a) leaves three roads uncovered.** (1) Several notes for one case (refused, then re-walked): which one wins is not stated. (2) A file with `schema_version` other than 1 has no stated reading. (3) The skill road writes no note and asks no question. That is the wider M2, which this fork does not cause but makes visible: delivery there truthfully says "no answer ... was recorded" because nobody asked.

## E. Roads into and out of `stage_S7` with the step at the stated position

Walked in `driver_stage_s7.py::stage_S7` and `s7_repairs`:
1. `s7_closed_by_scribe`: closes `s7.accepted` before the step, with `fresh=self.s7_fresh`. A need record that has no `attempt_id` binds to any triage row (t-1295 P2). So a person-chosen S6 rework done after S7 went to await the scribe would close S7 unasked. This is not traced to the end: it depends on whether `controller.py::_rerun_stamp` stales the S7 analyst. It is a road r2 neither names nor argues (M9).
2. `consumer_settled` (world A) with accept / reject / gap: each returns True and leads to a later entry that reaches the step. Holds.
3. Freshness block: `s7_retriage_once` may ask the seam question before the step. That asks, it does not close. The next entry reaches the step before the analyst. Holds.
4. The step, then `failures_to_triage`, then the no-failures close, the pre-triage close and the analyst: all after the step. Holds.
5. `s7_repairs`: test repairs, then re-judge rounds, then the second call (F-r2-1), then `open_work`, then `s7_close`. Holds with M6.
6. Restart road of the step's own re-walk (`completion_for`): breaks N1's invariant (M1).
7. Skill road (`skills/qa-story/phases/s7.md`, the driver's twin under AR-19; it already carries the re-judge rework at line 250): the step does not exist there, so the analyst is dispatched and S7 closes over an unanswered need. This breaks the owner's "ask once when needed" (M2).
8. Refused or stale need rows (M3): the step asks over a record the validator refused.

## F. The window "3a merged, 3b not"

**Not true by code as stated.** In that window `check_delivery.py::unprepared_records` still says "the factory could not prepare this check and the agent walked it without a result: needs another instance of the stand or device; not started without the person's word". That is false for a prepared case (t-1295's N3), and it suggests a word was asked for when nobody asked. The case stays listed and is never silent, but what reaches the person is wrong, not merely softened (`after_checks`). The window needs a runner to improvise a hidden flag, so this does not block (M10).

## G. Node cards

**Silent edges:**
- **E7-3a:**
  - (a) `need_record_problems` must never raise (C6).
  - (b) A verdict with `needs` plus a pass or fail Then that reaches the build after its session ended (session check skipped): `record_from_walk` "never `build_record`" silently drops the Then words. State it: refuse into the `walk_retry` road, or keep them as observations (M14).
  - (c) `unprepared_rows` gains `need` on refused or stale rows (M3).
- **E7-3b:**
  - (a) `environment_record._moment` returns `float("-inf")` for an unreadable stamp (`contract.py::_answer_moment`). It never says "does not parse", so "both parse ... strictly earlier" read literally makes an unreadable `ended_at` owed: a paid round on an unknown (M5).
  - (b) `current_manual_checks` holds one row per (case, obligation) (`finalize_task.py`, `manual_groups` key `case::oid`). The count `<n> check(s)`, the 10-case cap and "owed" must be counted by case (M8).
  - (c) Second-call arguments and return (M6).
  - (d) `ALLOWED_LINE` text (M7).
  - (e) Restart road (M1).
  - (f) Note file: which note wins, and the schema (M15).
  - (g) Runner words holding a path or a flag break `human-questions.md` rules. They are logged as the factory's own rule breaks (`judge_own_question`). State that this is accepted, or strip them (M18).
  - (h) The `s7.accepted` road (M9).
- **E7-2:** (a) the wrapper work item (M11). (b) `instance_lines` when the row's `at` or story is unreadable: say "(date not known)", never a guessed one.

**Owns:**
- E7-3b lacks `scripts/driver_stage_plan.py` (M1).
- The skill twin `skills/qa-story/phases/s7.md` is in no card (M2).
- The rest is complete against the Work items.
- Overlaps follow merge order: `state-exits.md` E7-1 -> 3a -> 3b; `manual_evidence.py` 7c -> 3a -> E7-2; `check_delivery.py` and `test_check_delivery.py` 7b-B (branch diff touches both) -> 7c -> 3b.

## H. Test plans

- **E7-3a:** the rows fit the budget; strongest first holds; the CLI battery has 300 / 301. **Missing:** a refused markerless need gives no `need` in `unprepared_rows` (M3).
- **E7-3b:**
  - **Missing, strongest first:**
    - (1) An unreadable moment is not owed (it guards the paid round, M5).
    - (2) A restart of a re-walk in world A with a refused build: the next step is S7 (M1).
    - (3) A refused need record gives no question (M3).
    - (4) The F-r2-1 re-judge row is dropped "by budget". That is stronger than the written "11 cases -> 10 + more" row: it guards an unasked S7 close, while the other guards text. Swap them, and fold the cap into the world A row's lead assertion.
    - (5) Answer tokens in other case or with quotes (`Start It`, quoted `by hand`), as outside input.
  - **Surplus:**
    - "walk road: `walk_before` called in `on_request`" pins an internal call order; assert the session line in row 3 instead.
    - The lead cut at 300 cannot be reached (N8); keep only masking.
- **E7-2:** fine, once the wrapper exists.
- **E7-1:** not judged (it is at the builder; not reopened).

## Amendments

- **M1 (blocking; E7-3b).** Add `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_plan.py` to the owns. Work: "`completion_for`: an S6 qa-runner dispatch whose id is a value of `state["extra_instance_rewalk"]` returns the step's world rule, BEFORE the S6 rule: S6 not completed -> `consumer_awaits("S6", True)`; S6 completed -> `False`. INVARIANT: on every road that finishes the re-walk, `controller.next` is S7 afterwards and `complete` is never True." Seam row (2) of H.
- **M2 (blocking; E7-2, or a node the architect names; Q-A).** The skill twin: `skills/qa-story/phases/s7.md` gets the same step before the analyst. When `run-report.json` holds a need record and `project_knowledge.py show` has no answer for the stand, the conductor asks the person once, with the lead and doors of §2.4. It records the answer with `project_knowledge.py instance`. On a yes it reworks S6 qa-runner over the cases with `--cause question_answer`. Name AR-19 in §1.
- **M3 (blocking; E7-3a).** "`unprepared_rows` adds `need`, `need_why`, `ended_at`, `prepared` only to a row with no `result`, no `evidence_errors` and no `current_reason`. A refused or stale need record reads as today's unprepared row. INVARIANT N6 at every reader: the S7 step and §2.6 never act on a need the validator refused." Row in E7-3a and E7-3b.
- **M4 (blocking; E7-3b DoD).** Replace `pytest ... test_audit_rules.py::test_a27_baseline` with `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/audit_factory.py --no-move` (A27 on the real tree plus its census; `--help` confirms the flag). `test_audit_rules.py` stays "not run locally: canon".
- **M5 (blocking; E7-3b §2.3 step 4).** "A moment parses when `environment_record._moment(x) != float('-inf')`. An unreadable `ended_at` or answer moment -> not owed, printed line, note `unparseable`." Row (1) of H.
- **M6 (E7-3b Work 2).** "The second call is `s7_extra_instance_step(state, True, awaiting)` with `awaiting` read again (`acceptance.awaits_acceptance`). On True, `s7_repairs` returns before `open_work` and `s7_close`."
- **M7 (E7-3b §2.3).** Write `ALLOWED_LINE` out. Suggested: "The person allowed the factory to start another instance of the stand or device for these checks: start it with the project's own actions, write what you started in `tried.md`, and walk the checks again."
- **M8 (E7-3b).** "Need rows are grouped by case: `<n>` counts cases, the cap is 10 cases, and owed is decided per case from its latest `ended_at`."
- **M9 (§2.1 INVARIANT).** Name `s7.accepted`: either argued as unreachable after a need (the analyst is staled by the person's S6 rework), or the step runs before `s7_closed_by_scribe`. The builder checks `_rerun_stamp` and says which.
- **M10 (§3 window).** Correct the claim. Either move the need branch of `unprepared_records` (HEAD words, WORLD = "no answer about starting one was recorded") into E7-3a, or state that the window shows the old false words (Q-B).
- **M11 (E7-2 Work).** "(8) wrapper `test_ss1_11_stand_lessons` (§6 C1)."
- **M12 (E7-3b tests).** The swaps and the missing rows listed under H.
- **M13 (E7-3a).** "`need_record_problems` returns a list and never raises (one raise in `write_unprepared`: bare 4 -> 5 exactly)."
- **M14 (E7-3a edges).** `needs` plus a pass or fail Then at build time is refused into the `walk_retry` road, never dropped silently.
- **M15 (E7-3b Work 5).** "One entry per case, the latest note wins. A file with another `schema_version` reads as `{}`."
- **M16 (§6 C1).** The wrapper records `n = len(harness.RESULTS)` before its scenario and asserts on `RESULTS[n:]`.
- **M17 (header, §5).** Base 9401f019. The Lead re-runs `owns_readers.py` over the E7-3b paths (FV3-22 moved `driver_stage_s6.py` and `driver_stage_s7.py`).
- **M18 (E7-3b edges).** Runner words in the lead are shown as written, after masking; a rule hit is logged as the factory's own break, accepted.

## Questions for the architect

- **Q-A, where the skill twin lands.** (a) E7-2: role text, after 3b, and the flag stays hidden until then. (b) Its own node after E7-2. **Recommend (a):** one node for all role-facing text.
- **Q-B, the 3a window words.** (a) Move the need branch of `unprepared_records` into 3a (it adds the slow `test_check_delivery.py` to 3a's narrow run). (b) Keep the window and state that the words are wrong. **Recommend (a):** no false sentence ever reaches the person.

## Plan-gate lines (rule 24)

- **Q13(a) EDGES:** M5, M8, M14, M15 and the restart road M1.
- **Q13(b) MEANING:** "unprepared walk" now means "could not prepare, OR prepared and needs an instance" (§2.6). Refused or stale need rows contradict this (M3).
- **Q13(c) PREMISES:** re-ran "nothing but S6 reads `walk_retry`": does not reproduce (C2), so it blocks via M1. "One site per raise" reproduces (C6).
- **Q13(e) FORKS:** see D.
- **Q4 CLASS:** readers of need rows are the step, `check_delivery.unprepared_records` and `ledger.unprepared_walks` (M3 covers them through the one reader). The restart twins of a driver-started S6 rework are `s7_rejudge` (done) and E7 (M1).
- **Q6 DUPLICATION:** `masked_words` and `manual_block_lines` are extracted, not copied (good). Moment parsers: `manual_evidence.py::_moment` and `environment_record._moment` differ; r2 picks the latter, which is acceptable with M5.
- **Q12 ONE ROAD:** the skill road is left outside the mechanism without a data row or the owner's word (M2, blocks).
- **VARIETY:** an unknown stand, registry or answer asks once (story-only variant). No silent default except the -inf moment (M5).

## Trail

- **Read:** r2 whole; t-1295 whole; r4 §5 (7c). On origin/main 9401f019:
  - `driver_stage_s7.py` 1-180, 340-540.
  - `driver_stage_s6.py` 140-410, 825-850, 1245-1265.
  - `driver_dispatch.py` 620-730, 1150-1490, 2843-2945.
  - `controller.py` 3737-4020, 4715-4760, 5594-5713, 6020-6090, 8386-8416, 10205-10240.
  - `acceptance.py` 1480-1540.
  - `stage_guard.py` 805-844.
  - `driver_stage_plan.py` 1205-1300.
  - `check_delivery.py` 1901-1922.
  - `manual_evidence.py` 1278-1296, 1527-1570.
  - `finalize_task.py` 530-576.
  - `no_move.py` 330-434.
  - `driver_runner.py` 1295-1315.
  - `driver_dialog.py` 266-421, 765-780.
  - `contract.py` 504-518.
  - `refusal_registry.py` 1360-1385, 1440-1600.
  - `test_judgment_census.py` 77-87, 200-297.
  - `test_stage_joints.py` 683-700, 820-845.
  - `test_artifact_writers.py` 1-130.
  - `test_state_exits.py` 38-130.
  - `test_audit_rules.py` 1333-1405.
  - `harness.py` 75-100, 225-232.
  - `told-ratchet.json` head and row 347.
  - `conductor-actions.json` price classes and rows 19-33.
  - `question-prices.json` rows `s7.open_work` and `s6.walk_account`.
  - `architecture.md` AR-19.
- **Commands:** `rev-parse HEAD origin/main` -> 9401f019 x2; `log --oneline 6be36343..origin/main` (FV3-22, FG7-65); `diff --stat` of the delta and of the branches 7b-B / E7-1; the scratch pytest probe (`1 failed, 1 passed`); the `units_of` measurement (101.5 s); `wc -c` -> 58331; DoD `python -B tools/dispatch_manifest.py --help` -> exit=0.

```json
{
  "verdict": "blocker",
  "failure_class": "spec",
  "blockers": [
    "M1 E7-3b: driver_stage_plan.py::completion_for (restart road) does not know E7 re-walk ids; world A with a refused walk build returns False, so controller.next re-plans S6; add the world rule branch and the file to owns",
    "M2 E7-2 or new node: skills/qa-story/phases/s7.md (AR-19 skill twin) has no step; the skill road closes S7 over an unanswered need (Q12)",
    "M3 E7-3a: unprepared_rows keeps need keys on refused or stale records (finalize_task keeps the marker), so the S7 step and the delivery words act on a need the validator refused (N6 at the readers)",
    "M4 E7-3b DoD: test_audit_rules.py::test_a27_baseline runs the whole slow battery at import and exits via finish(); use audit_factory.py --no-move",
    "M5 E7-3b step 4: environment_record._moment returns -inf for an unreadable stamp; state parse as != -inf, else an unreadable ended_at is owed (a paid round on an unknown)"
  ],
  "fixes": [
    "M6 second call in s7_repairs: arguments and return before open_work and s7_close",
    "M7 ALLOWED_LINE text written out",
    "M8 need rows grouped by case for count, cap and owed",
    "M9 s7.accepted road named and argued in the 2.1 invariant",
    "M10 3a window claim corrected or need branch words moved to 3a",
    "M11 E7-2 work item for wrapper test_ss1_11_stand_lessons",
    "M12 E7-3b test rows: add unparseable, restart, refused-need rows; swap F-r2-1 row for the 11-case row; drop walk_before order pin",
    "M13 need_record_problems never raises",
    "M14 needs plus pass or fail Then at build time refused into walk_retry",
    "M15 note file latest wins; other schema reads as empty",
    "M16 wrapper judges only its own slice of harness.RESULTS",
    "M17 base 9401f019 and owns_readers rerun for E7-3b paths",
    "M18 runner words with rule hits shown masked, logged as factory rule breaks"
  ],
  "class_completeness": "Restart twins of a driver-started S6 rework: s7_rejudge registered in completion_for, E7 re-walk not (M1). Stage twins: driver stage_S7 vs skill phase s7.md, E7 only on the driver (M2). Readers of need rows: S7 step, check_delivery.unprepared_records, ledger.unprepared_walks all fed by unprepared_rows, fixed once there (M3).",
  "trail": {
    "read": [
      "docs/tasks/specs/20261118-u7-e7-another-instance-spec-r2.md",
      "docs/tasks/specs/reviews/t-1295-u7-e7-plan.md",
      "docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r4-7b-7c-e7.md:355-384",
      "ai-packages/qa-factory/scripts/driver_stage_s7.py:1-180,340-540",
      "ai-packages/qa-factory/scripts/driver_stage_s6.py:140-410",
      "ai-packages/qa-factory/scripts/driver_dispatch.py:620-730,1150-1490,2843-2945",
      "ai-packages/qa-factory/scripts/controller.py:3737-4020,4715-4760,5594-5713,6020-6090",
      "ai-packages/qa-factory/scripts/driver_stage_plan.py:1205-1300",
      "ai-packages/qa-factory/scripts/finalize_task.py:530-576",
      "ai-packages/qa-factory/scripts/manual_evidence.py:1278-1296,1527-1570",
      "ai-packages/qa-factory/scripts/refusal_registry.py:1440-1600",
      "ai-packages/qa-factory/scripts/tests/test_audit_rules.py:1333-1405",
      "ai-packages/qa-factory/scripts/tests/test_artifact_writers.py:1-130",
      "ai-packages/qa-factory/scripts/contract.py:504-518"
    ],
    "reruns": [
      {"command": "git -C C:/QAFactory/forge-repo rev-parse HEAD origin/main", "result": "9401f019 twice; package status clean"},
      {"command": "python -m pytest scratchpad/c5/test_wrap_probe.py -q", "result": "1 failed, 1 passed (planted negative control fails, wrapper passes, main not run at import)"},
      {"command": "units_of over the tree via test_judgment_census", "result": "write_unprepared blocks True; walk_rule_errors, _validate_unprepared, verdict_problems, record_problems blocks False; 101.5 s"},
      {"command": "python -B tools/dispatch_manifest.py --help", "result": "exit=0"}
    ]
  }
}
```
