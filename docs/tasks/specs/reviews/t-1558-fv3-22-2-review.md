# t-1558 — critic review: FV3-22-2, the skill road closes S6's manual half (branch wip/fv3-22-2-t1543, a096efac)

Spec: card r2 `docs/tasks/specs/20261117-fv3-21c-skill-road-s6-close-card-r2.md` (K5.e-K5.k, §2.3-§2.4, §4.2-§4.3, §5), with the Lead
decisions on t-1209 overriding it (step 1b discriminator = `finished` not earlier than the code_only completion; `.get` chain;
`live_s6_scopes` stays in `controller.py`). Builder report `t-1543-fv3-22-2-report.md`; staged `docs/SIBLING_MAP.md`.

**Verdict: NEEDS WORK (fit_with_fixes). 0 blocking findings, 7 fixes before merge (F1-F7), plus one residual (R1) for the Lead.**
Both of the builder's own decisions are in the safe direction. I recommend confirming them; that decision is the Lead's (rule 6).

## Findings

**F1 (fix before merge) — two builders of the E9 door.**
- `stage_close.py:394-402`: `SkillRoad.record_close` builds `door: python ".../stage_done.py" --task T --stage S <args>` from its args.
- `story_step.py:1190-1193`: step 1b builds the same door again as a literal (`--status done --digest "{reason}" --no-journal`).
- Failure scenario: `close_by_code` changes the record args (for example it adds `--role`, which the S7 sites pass, `stage_close.py:255`).
  The first door then changes and step 1b's copy does not, so the same E9 world prints two different commands (Q6).
- Fix: one function in `stage_close`, for example `record_door(task, stage, args)`. `record_close` and step 1b both call it.

**F2 (fix before merge) — a second reader of pipeline.json and a second ISO-with-zone parser.**
- `stage_close.stage_record_written` (`stage_close.py:314`) reads the file with its own
  `hooklib.read_json(... pipeline.json, {}, kind=dict, errors=Exception)`. That is the expression of `stage_done.read_pipeline`
  (`stage_done.py:798`), a function in the same module the new reader comes from, and of `SkillRoad.pipeline` (`stage_close.py:345`).
  Use `stage_done.read_pipeline(...)`.
- `stage_done.stage_finished_at` (`stage_done.py:801-815`) repeats the parse `fromisoformat(value.strip().replace("Z","+00:00"))` plus
  the tz check. The same parse already sits in the nested `stamp` of `stage_close.person_pass` (`stage_close.py:101-111`). Hoist one
  helper and have both use it (Q6).

**F3 (fix before merge) — builder decision (2) has no row.**
- `story_step.py:1186-1187`: an S6 the controller holds `completed` without `code_only` returns None (today's lines).
- This is new behaviour reachable through `start`'s exit, and nothing asserts it (Q5(c)).
- Probe-by-reading: drop the `code_only` check. A role-accepted S6 then reaches `stage_record_written`. That finds no code_only event,
  hits IndexError and returns False, so `start` prints the E9 door (exit 2) on a stage nobody closed by code. No row of the new
  functions goes red.
- Fix: one row (C2-like world, S6 completed by an accept event and not by `code_only`). Expected: today's X1 lines, exit 2, no E9 door.

**F4 (fix before merge) — P2 bypasses the door the card names.**
- Card §5.2 P2: "`line` holds `waiting for the doc scribe's acceptance (S8)`".
- The test calls `story_progress._awaits_position` directly and compares its dict (`test_story_step_manual_block.py`, P2). The
  `_parts` rendering of `consumer_stage` in parentheses is asserted only for S7 (P1). For S8 it is checked only as a dict field.
- Fix: P2 through `progress(root)["line"]`, as the card writes it (Q1, Q5(c)).

**F5 (fix before merge, staged map) — the axis-26 clause names the wrong callers.**
- The staged `docs/SIBLING_MAP.md` says the callers of `waiver.stand_passing_word` are `story_step._no_stand_refusal` / `_no_stand_cases`
  and `_s6_manual_close`.
- The actual callers are `_no_stand_cases_of` (`story_step.py:1125`) and `_s6_manual_close` (`:1209`). `_no_stand_cases` takes the
  words as a parameter. `_no_stand_lines` reads `waiver.stand_passing_override` (`:1138`), the underlying one reader (`waiver.py:389`).
- Fix: correct the clause before the Lead commits it (Q4/axis 26 text accuracy).

**F6 (fix before merge) — size.**
- `_s6_manual_close` is `story_step.py:1164-1237`: 74 lines, about 62 without the docstring. That is over the roughly-60 bar (Q7).
- `_manual_block_check` (`:1007-1098`) grew with the nested `settle` and `lines_of`.
- Fix: extract step 1b (the re-entry, `:1182-1193`) into a helper. The return contract is unchanged.

**F7 (fix before merge, or the Lead's reason) — run time.**
- The re-run of one function takes 43.03 s (trail). The builder's three functions take 81.22 s. The file budget is 10 s (card §5,
  docs/TESTING.md «Бюджет»).
- Every C-row builds a fresh `real_story`. C11/C11b/C11c (three worlds) and C3/C3b (two worlds) differ only after `_s6_world`, and
  could share a world copied once per variant.
- Rows to consider first: C11c (same door and filter predicate as C11b; P3 already kills via C11b) and C3b's separate world.
- Keeping the time is the Lead's reason to give at merge (rule 20).

**R1 (residual, not this diff, the Lead's call) — X2/X3 write before step 1b.**
- On a `completed` code_only S6, a `start --scope ...` still runs `prepare_for_block` (X3, `story_step.py:1080-1086`) or
  `_no_stand_cases_of` -> `write_case_refusal` (X2, `:1120-1131`). Both run before `_s6_manual_close` reaches step 1b.
- `request.json` files of refused cases are receipt evidence (`manual_request_paths`, `stage_close.py:229`), so they can be rewritten
  under a hashed receipt.
- This is pre-existing (FV3-21b and earlier did the same) and the card positions it (K5.f). E14's invariant names only the run report.
- No completed-stage guard exists in `start` before `_manual_block_check` (read `story_step.py:880-915`).
- Proposed: a node (owner: the qa-story/FV3-24 executor) or a guard in front of prepare. Opening it is the Lead's decision.

## Builder decisions (the dispatch's two edges)

- **(1) Step 1b, unreadable time or no record -> the E9 door, not "fall through": CORRECT, the safe direction.**
  - Traced: `manual_half_close` runs `finalize_task.py` FIRST (`stage_close.py:224`), then `close_by_code`. That returns True at once on
    a `completed` stage (`:243-246`), without `stage_done`.
  - So the Lead's "fall through to the close" would rewrite the run report the receipt hashed (AR-21) and then print "S6 is closed by
    code" with no record. That is exactly the false success of t-1195 F4b.
  - The door is runnable: the builder's measurement (a real code_only S6 plus a consumer record) shows `stage_done --status done` exits 0
    and sets `finished`.
  - A stale-recovery loop is excluded: `stage_done` recovers only when the store's LAST event is the identical transition
    (`stage_done.py:1350`), and the code_only event lies between.
- **(2) S6 completed by a role's accept, no `code_only` -> today's lines: SAFE.**
  - It stays inside "None = not applicable".
  - No close or reducer runs over a stage this close did not complete.
  - It needs a row (F3).

## Per item

| item | result |
|---|---|
| K5.e return shape, steps 1-7 | done. The 4-tuple is unpacked in one place (`settle`). Step 1b uses the `.get` chain (F4-2) and the t-1209 discriminator (`stage_record_written`: `finished >= stamp_utc(last code_only created_at)`, equal = written, any exception = not written). Step 4 is `controller.live_s6_scopes` (running/blocked/paused, `controller.py:690-697`), placed before every prepare and close. Step 6 under the word calls `_no_stand_cases` directly (one prepare per case; equivalent outcome, report item 4) |
| K5.f X1/X2/X3 | done. X2 `spent` = `_no_stand_cases_of`'s dict, so done cases are excluded (E17). X3 only with `every`; a partial refusal returns today's lines and never closes. Q2 note: X3's `left` lines also list the cases outside the block that the close's loop found refused (true refusals; the card asked only for the door). Not a fix |
| K5.g | done (door text matches card) |
| K5.h | done. Checked every return of `_manual_block_check`: `(None, [], 0)` or code 2 (`story_step.py:1018-1046`), so the widened test changes no existing outcome |
| K5.i | done (s6.md line; variant check with a negative control) |
| K5.j | changelog bullet 2 done; map staged (F5); test-layers `covers` gains `story_progress.py` |
| K5.k | done. POSITION after asked/gate, before code_only (`story_progress.py:548`); `except` -> None; activity `no role running` (F4 on P2) |
| AR-15 one body | verified: driver `manual_close` -> `stage_close.manual_half_close` (`driver_stage_s6.py:960`), SkillRoad -> the same; delegates at `driver_stage_s6.py:171-241` |
| refused stage_done, no second receipt | verified. C9b: the second start goes to step 1b (no reducer, no receipt). Within the close, `close_by_code`'s completed check stands |
| live filter | verified, and before any prepare on X1. The probe P3 in the report kills a running-only filter (C11b/C11c) |

## Standing questions

- Q1 fit: met except F4. Q2 decisions: see above, both safe.
- Q3 seams: `stage_done.py` gains one additive reader (authorised). No driver module is touched (diff stat: 8 files).
- Q4 CLASS: axis 5 survivor recorded. S7/S9 = FV3-26 and FV3-24 are named nodes. The analog `close_by_code`'s blind completed-check
  (`stage_close.py:243-246`) is FV3-26's by the Lead's t-1209 decision. R1 is new and the Lead's call.
- Q5 TESTS:
  - (a) killing power: read P1-P4 in the report (hash-equal restores). My own probe was not run (see mutants_none). By reading, C9b
    kills a `finished is None` pass and C9c kills a flipped `>=`. The one survivor-by-reading is F3.
  - (b) expected values trace to card §2.3 / §5 (C2 reason prefix, the C4 refusal literal from the FV3-21b card door).
  - (c) F3, F4.
  - (d) the rename `the_card_and_the_help_name_the_rule` -> `test_...`, same behaviour, `main()` updated.
  - (e) none found.
  - (f) the volume is within bounds (test +224 vs product about +340); F7 is time.
- Q6 DUPLICATION AND CONSISTENCY: F1, F2. Second script runner `SkillRoad.py` vs `story_step._run`: the card justified it (exit 127 vs
  skipped). Grepped `fromisoformat` in `stage_close.py`/`acceptance.py`/`waiver.py`; `stand_passing_(word|override)` over `scripts/*.py`;
  `def live_s6_scopes` (1 hit, `controller.py:690`).
- Q7 CODE QUALITY: F6; no dead branches found. The name `stage_record_written` matches its behaviour.
- Q8 hygiene: every touched file is all-CRLF (line count = CR count, 7 files). No Cyrillic in the diff (0; positive control 2).
- Q9 ratchets: no ratchet file in the diff (stat), no raise.
- Q10 ARCHITECTURE: AR-13/15/21/28 named in the commit and checked above. VARIETY: an unknown scope, state or time errs to today's lines or
  to a door. There is no silent default and no stop.
- Q11 JUDGMENT: none moved. The checks read data (scope derived, dispatch status, field presence, time order).
- Q12 ONE ROAD: one body for both roads. No exclusion found. The residuals FV3-24/26 are nodes.

## Trail

- Read:
  - card r2 §0.2, §2-§5 and the Lead decisions;
  - t-1209 (whole);
  - the t-1543 report;
  - `git show a096efac` for stage_close/stage_done/story_progress/story_step/tests/s6.md/changelog/test-layers;
  - `git diff --cached` (map);
  - `stage_close.py` 95-118, 214-260, 296-408;
  - `stage_done.py` 725-740, 798-838, 1000-1020, 1222-1236, 1340-1400;
  - `controller.py` 690-698, 1186-1192, 1940-1956;
  - `event_store.py` 599-615;
  - `manual_evidence.py` 1428-1463;
  - `story_step.py` 880-915, 1007-1237;
  - `waiver.py` 389-410;
  - `test-layers.json` 7359-7370.
- Re-run (DoD): `( cd <worktree> && python -m pytest ".../test_story_step_manual_block.py::test_fv3_22_nothing_left_closes_s6_on_the_skill_road" -q )`
  -> `1 passed, 16 warnings in 43.03s`.
- Tree: `git -C <worktree> status --porcelain` -> `M  docs/SIBLING_MAP.md` and `?? docs/tasks/specs/reports/t-1543-fv3-22-2-report.md`.
  The tree is dirty, so there is no probe (rule 21).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F1: one builder of the E9 stage_done door - SkillRoad.record_close (stage_close.py:394-402) and story_step step 1b (story_step.py:1190-1193) each build it; move to one stage_close function both call",
    "F2: stage_record_written (stage_close.py:314) reads pipeline.json by its own hooklib.read_json - use stage_done.read_pipeline (stage_done.py:798); stage_finished_at repeats the ISO-with-zone parse of stage_close.person_pass.stamp (stage_close.py:101-111) - one helper",
    "F3: builder decision (2) (story_step.py:1186-1187, completed S6 without code_only -> today's lines) has no row; add one: role-completed S6, X1 start -> today's lines, exit 2, no E9 door",
    "F4: P2 asserts _awaits_position's dict directly; card 5.2 asks progress(root) line holds 'waiting for the doc scribe's acceptance (S8)'",
    "F5: staged SIBLING_MAP axis-26 clause names _no_stand_refusal/_no_stand_cases as stand_passing_word callers; actual callers are _no_stand_cases_of (story_step.py:1125) and _s6_manual_close (:1209); _no_stand_lines reads stand_passing_override (:1138)",
    "F6: _s6_manual_close story_step.py:1164-1237 over the ~60-line bar; extract step 1b (:1182-1193) into a helper",
    "F7: the new function runs 43 s alone (81 s for three) against the 10 s file budget; share worlds across C11/C11b/C11c and C3/C3b, or the Lead's reason at merge",
    "R1: residual for the Lead - on a completed code_only S6, X2/X3 (story_step.py:1080-1086, 1120-1131) rewrite request.json files that are receipt evidence before step 1b runs; pre-existing, card-positioned; node or guard is the Lead's decision"
  ],
  "class_completeness": "axis 5: survivor stage_close.py recorded, driver delegates verified (driver_stage_s6.py:171-241, :960); S7/S9 skill-road closes = FV3-26, S6 other steps and analyst acceptance = FV3-24 (named nodes); analog close_by_code completed-check without record (stage_close.py:243-246) = FV3-26 per Lead t-1209; axis 26 clause needs F5; new residual R1 (writes before step 1b) for the Lead",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-fv3-21c-skill-road-s6-close-card-r2.md (0.2, 2-5, Lead decisions)",
      "docs/tasks/specs/reviews/t-1209-fv3-22-card-r2-rereview.md",
      ".claude/worktrees/fv3-22-2/docs/tasks/specs/reports/t-1543-fv3-22-2-report.md",
      "git show a096efac (all package files), git diff --cached (SIBLING_MAP)",
      "scripts/stage_close.py 95-118, 214-260, 296-408",
      "scripts/stage_done.py 725-740, 798-838, 1000-1020, 1222-1236, 1340-1400",
      "scripts/controller.py 690-698, 1186-1192, 1940-1956",
      "scripts/event_store.py 599-615",
      "scripts/manual_evidence.py 1428-1463",
      "scripts/story_step.py 880-915, 1007-1237",
      "scripts/waiver.py 389-410",
      "scripts/tests/test-layers.json 7359-7370"
    ],
    "reruns": [
      {
        "command": "( cd C:/QAFactory/forge-repo/.claude/worktrees/fv3-22-2 && python -m pytest \"ai-packages/qa-factory/scripts/tests/test_story_step_manual_block.py::test_fv3_22_nothing_left_closes_s6_on_the_skill_road\" -q )",
        "result": "1 passed, 16 warnings in 43.03s"
      },
      {
        "command": "git -C C:/QAFactory/forge-repo/.claude/worktrees/fv3-22-2 status --porcelain",
        "result": "M  docs/SIBLING_MAP.md / ?? docs/tasks/specs/reports/t-1543-fv3-22-2-report.md"
      }
    ]
  },
  "mutants": [],
  "mutants_none": "the worktree is dirty (staged docs/SIBLING_MAP.md, untracked builder report), so rule 21 forbids the probe; also the narrow test file runs over the runner's 60 s timeout (one function alone 43 s)"
}
```
