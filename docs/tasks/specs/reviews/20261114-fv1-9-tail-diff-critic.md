# FV1-9 tail: code critic, one pass for the topic (t-747)

Object: card A = eef1219 on origin/wip/fv1-9-ta vs origin/main (8 files, +503/-7). Lighter object: cards B (ba52304), C (1d65eb3),
D (merge 659dcc4), all already in origin/main.
DoD: spec `docs/tasks/specs/20261114-fv1-9-tail-cards-spec.md`, card A plus §7b items 1-13. Mechanical layer: the builder report (attached).
No code was edited, no CI was run, no slow file was run.

## Verdict

- **Card A: fit_with_fixes.** No blocker. One fix this round (F1: text the planner reads is false). One node for the Lead (N1: the S3
  labelling window reads the planner's `next:` lines and then deletes them). Three queue lines.
- **Card B: fit.** No `defect_found`.
- **Card C: fit.** No `defect_found`.
- **Card D: fit.** No `defect_found`.

## Findings (card A)

**F1 (fix this round, not blocking): the `plan_notes` lines reach the planner with a false tail.** Files: `driver_stage_plan.py:676-677`
and `driver_gates.py:602-603`.
- Both sites tell `told_from(out, ("plan_notes",), unknown=False)` to `next:S3:<planner>` with the tail "it stays on your plan row and is
  tried again when S3 closes next; remove it if it no longer holds".
- What `plan_notes` is, read at the producer `question_register._name_in_plan_row` (`question_register.py:2049-2076`): code raised a
  question for a CASE, then failed to write that question's ref onto the plan row. The docstring says "This call rewrites `raise` to the
  new id, so it cannot run again for the same Then - there is no retry."
- So the line is not the planner's entry, nothing "stays on your plan row", and nothing is "tried again when S3 closes next".
- Failure scenario: `PC.append_question_ref` refuses for row R2. The planner's next prompt then says, under TR1, "Q9 raised for TC-3: the
  plan row could not be told about it ... (it stays on your plan row and is tried again when S3 closes next; ...)". The planner leaves
  R2 alone and expects code to retry, but no retry exists. The ref is missing for good, and gate A shows the second card that HF4-9 exists
  to prevent.
- FR-10 and the spec edge "Who is the receiver / the tails are true" are both broken.
- Fix: give the two `plan_notes` calls a tail of their own that is true, for example "code could not write this onto your plan row and
  will not try again: add it to the row yourself if it still holds". Change the expected text in the row
  `s4_after_critic: plan_notes (item 13)`. Keep the s3_project tail as it is: `planning_contract.py:3378-3380` and `:3420` really are
  retried at the next projection.

**N1 (node for the Lead, owner the FV1-9 Lead; not a blocker): a `next:S3:<planner>` line can be read and then deleted by the S3
labelling window, which writes no plan.**
- The key is stage + role (F-1 (b), as the spec says). `run_role` reads it for every S3 session of that role, including
  `stage_S3` window 1 (`driver_stage_plan.py:129`, purpose `s3_labelling`). That window "labels work/grounding.yaml and writes no plan"
  (docstring, `:107`).
- Trace in the diff world:
  1. S3 closes on window 2; `s3_project` stores its notes. Or S4 closes and the roll-call stores `plan_notes`.
  2. S3 is entered again through `stage_S3`.
  3. `s3_window()` returns "w1", because the newest strategist dispatch is the accepted exit window, not labelling (`:323-336`).
  4. The labelling window's prompt carries TR1 and the lines. Its result has words, so `forget_told` deletes them
     (`driver_dispatch.py:736-737`).
  5. Window 2, the session that can act on a plan row, gets nothing.
- How bad: the planner's own entry is not lost. It stays on the row and is retried at window 2's close (and was printed as `note:`).
  What gets lost is the told line, before the session that could act on it.
- Not traced: which re-entry roads go through `stage_S3` rather than through the direct `rework` (the direct `rework` is the correct
  session). This is an estimate.
- A neighbour I did not verify: S6's acceptor is `qa-failure-analyst`, whose session runs at S7 (`stages.json:221`). Its lines go to
  whichever analyst session comes next, and `driver_stage_s7.py:680` runs a purpose `investigation` session of the same role.
- Recommended direction: read and forget the `next:` key only for a dispatch whose own record carries no purpose. Read the purpose
  through the record (`request_binding.purpose`; axis 5, row "The S3 window word": `controller.s3_window_of` is the one reader), not
  through `run_role`'s `purpose` argument, which is "" on the rework road.
- This changes the meaning of the key, so it takes the Lead's decision and a check on the plan (PROJECT.md, package change, item 6).
  That is why I propose a node rather than a fix-round line.

**Queue lines (not blocking).**
- Q1: `told_from` is a third copy of the slice parse `json.loads(out[out.index("{"):out.rindex("}") + 1])`. The other two are
  `driver_gates.py:331` (`rehearse`, gate_preflight) and `driver_machine.py:1706`. They converge on `told_from`, or a neutral helper.
  | перенос: code-quality node P7 of spec §5 | обоснование: outside card A's owns | подтвердил: —
- Q2: the two-call block "designer `question_notes` + planner `plan_notes`" with its literal tails is written twice
  (`driver_stage_plan.py:674-677` and `driver_gates.py:598-603`). One helper `tell_rollcall(out, code)` would remove the copy.
  Severity: queue. Fold it into the F1 round if it is cheap.
- Q3: `tests/test_place_session.py` `test_one_site_for_place_lines` and `test_one_site_for_neighbour_lines` are red on origin/main too.
  Both `re.findall` look in `story_run.py` (`:382-384`, `:391-392`) for calls that live in `driver_dispatch.py:717-718`. The file sits
  in the `quarantine` section of `test-layers.json` (cohort 8073673, entered 2026-11-11), so the canon does not run it. Owner: the td-15
  quarantine node (deletion only on the owner's word); no fix in this topic.

## Keys

**1. §7b items 1-13 for card A.**
1. A-1: built as written. The stage comes from `controller_state()["dispatches"][dispatch]["stage"]` with a fallback, inside the
   `try`, before `stage_done` (`driver_stage_plan.py:575-580`). The row S7 -> scribe S8 exists. `dispatch` is the acceptor's own
   dispatch (docstring `:566`).
2. A-2: built (`driver_dispatch.py:736`). Rows: dead, empty, reused.
3. A-3: built (`told_from`, the `errors` branch). There is a row.
4. A-4: built. The only callers of `next_session_lines` and `forget_told` are `run_role:721/737` (Grep, below), and `resume_role` does
   not read the key.
5. A-5/A-7: built (`tell_next_session`'s `if fresh and role`; the early return in `forget_told`). There are rows.
6. A-6: built (state-exits row; the report shows `test_state_exits` 142/142).
7. A-8: built (`driver_gates.py:596-606`). Exit 0/1 is parsed; any other exit tells the unknown line before `RepairFailed`. No
   `check` was added.
8. A-9: built. One difference: an EMPTY value is also listed, because `parse_json_list` returns a `why` for it and the roll-call then
   makes a note. This is right: the trigger and the producer agree.
9. A-10: n/a, nothing built. Right.
10. A-11: TR1 is verbatim (`driver_dispatch.py:1807-1808`, compared to §7b item 10 character by character).
11. T-1: folded into one table. T-2: the slow row is missing. My view:
    - Each half is proved fast: the store is written by `s4_after_critic`, and `run_role` reads the key, puts it before `extra`, and
      forgets only after a saved result with words.
    - The join is visible by reading. `tell` comes before `rework` in the same function (`:674-681`), and `rework` calls
      `run_role(stage, role, ...)` with the same literals (`driver_dispatch.py:2880`).
    - So the behaviour is not unproved in a way that matters.
    - Decision: the Lead's, because T-2 is binding. Either drop the row from T-2, or have the F1 fix-round builder write it unrun. A row
      written unrun is legal: slow files are "judged by the batch canon" (builder-rules 7b).
12. `told_from` is the one helper of the three carriers: built.
13. `plan_notes` is told to the planner: built, but with the wrong tail (F1).

**2. Direction of error.**
- Never lost:
  - forget runs only after `_write_json` with words.
  - A crash, a raise in `run_claude`, or a reused result keeps the lines.
  - The tell sits before every raise: `s3_project` before the Refusal; `s4_after_critic` before `pin_cases`/`rework`; `raise_move`
    before `RepairFailed`; `stage_acceptance_write` inside the `try`.
  - The acceptor tells AFTER its own forget (completion runs in `finish`, after `:737`), so it does not delete its own fresh lines.
- Wrong role or stage: the designer literal matches `:513`/`:681`; the planner is `roles[0]` (`:114`); the acceptor is keyed by its own
  dispatch stage. Remaining exposure: N1, which is the right role and stage but the wrong window.
- Told twice:
  - A refusal resume does not read the key (A-4).
  - Dedupe is by exact string after the whitespace collapse.
  - A line forgotten and later produced again is stored again. That is right: it is a new pending state.
- Unknown: an output that does not parse, or one with an `errors` list, gives the one unknown line, never "nothing refused" (AR-28).
  `check=True` at the form raiser means a refused raise is a Refusal, and no `reword_problems` exist then.

**3. `unknown=False`: keep.** The `plan_notes` read would otherwise tell the planner "not known whether your question entries were
carried out" about a roll-call call that held none of its entries. The unknown line goes once, to the designer, whose entries the call
did execute. This is safe: the designer key still carries the unknown.

**4. `getattr(self, "state", None)`: keep (legitimate).**
- It is an existing pattern with 4 production sites (`driver_dispatch.py:556`, `driver_machine.py:329`, `driver_runner.py:436`,
  `driver_stage_s6.py:861`).
- It hides no missing state in production: `Driver.__init__` always sets `self.state` (`driver_core.py:561`).
- Asymmetry: `tell_next_session` and `forget_told` touch `self.state` directly, which is fine, because their callers always run on a
  real driver.
- Optional queue line: give the old rigs `d.state = {}`.

**5. test_place_session.** Red on origin/main too, and quarantined; see Q3. Positive control of the same shape: `git grep -n
"s7_place_lines(\|s7_neighbour_lines("` on origin/main finds `driver_dispatch.py:717,718,4026,4070` and nothing in `story_run.py`.

**6. Seams.**
- Hunks only in `run_role` (prompt lines `:719-722`, the point after save `:736-737`), the four new methods, `s3_project`,
  `stage_acceptance_write`, `s4_after_critic`, the new `cases_with_question_entries`, and `raise_move`.
- `role_lines`, `completion_for` and `s4_critic_completion` are untouched (diff read in full).
- Owns gained `design/state-exits.md` (A-6), as amended.

**7. P27 / AR-29.**
- No line judges meaning. `told_from` is a key read of JSON. `cases_with_question_entries` is a presence or shape read through
  `contract.case_files` and `front_line`/`parse_json_list`. It refuses nothing, so it is not a census unit.
- `judgment-census.json` is untouched (diff stat).
- `driver-layers.json`: 5 method rows in the form of `:201-207`. `told_from` is `"kind": "staticmethod"`; the precedent is
  `blockers_to_stop_on`. The key note is extended as §2 item 5 asks. Judged by `test_driver_layers.py` in the canon.
- A27: no baseline row names the four functions. Case-insensitive Grep: 0 hits; the same call shape finds `arrival_record`. The old
  roll-call site was doored by `# remains:`, which stays.

**8. Role text.**
- TR1 is exact.
- FR-37: the new texts name no path. The only path, `[plan file: work/test-plan.json]`, comes from the producer's own line.
- The tails: S4 is true with F-4 in place. Acceptor: true. S3 (`s3_project`): true. Planner `plan_notes`: false (F1).

**9. Tests.**
- One table `test_fv19_carriers_tell`. Its ids name the case, and each carrier row asserts through `next_session_lines(<receiving
  stage>, <role>)`, then `forget_told`.
- The two helpers print the prefixes `fv19_run_role_tells_and_forgets[...]` and `fv19_carriers_tell[cases_with_question_entries: ...]`.
  A red line still names its case.
- The negative control from the report (46 FAIL, then 587/587, sha256 equal) is consistent with the 17 carrier rows plus the store rows.
- My re-run: 587/587.

**10. DUPLICATION AND CONSISTENCY.**
- No second parser of `critic_rollcall` output, and no second store: `question_pass_lines` is the only key. Grep `question_pass_lines`
  over `scripts/*.py`: writers `driver_dispatch.py:1695,1798,1889,1902` (plus the removals in `forget_told`); readers `:1755`,
  `:1804`, `:1817`.
- The slice parse now has 3 copies (Q1).
- The roll-call tell block is written twice (Q2).

**CODE QUALITY.** No new function is over 30 lines or nested more than 3 levels. No dead branch. Copy-paste: Q2 (queue). `run_role`
was already long and grew by 4 lines.

**ONE ROAD (P31, brief item 12).**
- None found for a language, project or case: no name branch was added (diff read; the only literals are stage/role ids the functions
  already used).
- One residual of the class inside the store: H36's dispatch key is popped at prompt build, while the `next:` key is forgotten after a
  saved result. That is two removal rules in one store. It is queued in spec §7b "Queue (Lead): H36 removal after a saved result",
  owner the FV1-9 Lead.

**11. Class completeness (SIBLING_MAP, every axis).**
- Axes 1-4 n/a: not a policy, exam, release or rules-debt change.
- Axis 5: partly covered, partly queued or a node:
  - "Author + critic repair loop": S4 covered. S5 and S7 n/a, because no question-entry carrier exists there.
  - "Skill phase <-> driver": the skill road is queued (P3/F-8).
  - "The S3 window word": N1.
  - "Stage in front of a gate S4/A": `raise_move` covered.
  - "One question for every stop" (A27): no new site.
- Axes 6-12 n/a: no measurer, test identity, story path, test-file leaf, git-top reader, tokenizer or plan carrier is touched.
- Axis 13 n/a: no dispatch text cut.
- Axes 14-15 n/a.
- Axis 16 n/a: JSON of a subprocess, not a file read.
- Axis 17 n/a: not a detector verdict.
- Axis 18: no ratchet raised.
- Axes 19-31 n/a: no role tools line, receipts, markdown tables, host forms, tests[] rows, execution records, freshness, stand word,
  profiles, row form, jsonl appends, profile commands or role carriers.
- Axis 32 covered: no judgment moved (key 7).
- Axis 33 n/a: no dispatch is picked; the acceptor's stage is read from its own record.
- Axis 34 covered (One road above).
- Axes 35-36 n/a.
- State-exits row: present, with both key forms and the terminal state.

## Cards B, C, D (about a third of the pass)

**B (ba52304): fit.**
- The replay rule sits after `row` is resolved and before every other check (`question_register.py:1600-1613`).
- The history match needs the producing entry's `role` and `_squeeze(why)` (B-1).
- `reworded[0].was` (the original wording) is never matched (B-2).
- Readings are compared only when they are a list (B-3), and elements that are not objects are skipped (B-4).
- Built differently, and defensible: a match on the CURRENT text does not check role or why. B-1's parenthetical ("the last entry for the
  current text") can be read either way. The outcome falls in the spec's allowed direction (the person sees exactly the requested words;
  original edge, "Allowed error"). If the Lead meant the strict reading, it is a queue line, not a `defect_found`.

**C (1d65eb3): fit.**
- Guard: `--stage` is allowed with `--raise`, `--repeat` and `--reword`. A plain `--raise` still refuses it as stray (origin/main
  `question_register.py:2489-2498`).
- `_checked_stage` goes through `acceptance.stage_def_of` (exact case; it never raises). Valid ids come from `null_outcomes.stage_ids()`,
  sorted by number. An unreadable table refuses a non-blank value (C-3). The same check applies to `--from-handoff` (C-4).
- The sentences name the script by its full path (C-6) with `--task`/`--stage`, inside the `recorded` block.
- Seen in passing: `--stage` now accepts S5-S9 on `--from-handoff`. That is intended, because `stage_acceptance_write` raises for
  S4/S6/S7.

**D (659dcc4): fit.** `question_count` adds `and not QR.hidden_repeat(q)`, the one predicate (pure on a `load` row, error direction
"shown"). There are three rows (4, then 1, then 2 after reopen).

## Spot-checks of the submitter's claims
- "Writers 3 old + tell_next_session; readers resume prompt / next_session_lines / forget_told": reproduced (Grep above).
- "test_place_session red is pre-existing": reproduced on origin/main with a positive control (key 5). The file is quarantined (I read
  the `test-layers.json` quarantine section, not taken from the report).
- "judgment-census untouched": the diff stat has no such file.
- Witness: re-ran `test_gate_question_form.py` (587/587, matches). The other witness numbers are consistent with the diff (17 carrier
  rows + 5 run_role rows + 8 case rows).

## Trail
- Read: the spec (all of it); the builder report; the critic-diff-brief (items 1-12); SIBLING_MAP headings and axis 5; the whole card A
  diff (code and tests); `driver_dispatch.py:617-806` on the branch; `driver_stage_plan.py:78-137`, `:240-279`, `:323-363`, `:545-687`,
  `:828-853`; `critic_rollcall.py:395-414`, `:739-796`, `:1160-1209`; `question_register.py` `_name_in_plan_row` `:2049-2076` and the
  `plan_notes` greps; `planning_contract.py` notes producers; `controller.py:63-95`; `stages.json` acceptance_by; `role_cli.refuse`;
  `driver_runner.py:211-235`; `driver_gates.py:320-335`; `audit_factory.py` A27; `test_place_session.py:380-393`; the diffs of
  ba52304 and 1d65eb3 and the code part of 659dcc4; origin/main `question_register.py:2486-2500`, `acceptance.stage_def_of`,
  `null_outcomes.stage_ids`, `hidden_repeat`, `_squeeze`, `_reading_texts`.
- Re-run: `( cd .../fv1-9-ta/ai-packages/qa-factory && python -B scripts/tests/test_gate_question_form.py )` gave
  `=== gate question form: 587/587 ok ===`.
- Not re-run: `test_state_exits`, `selftest --limits --lang` (consistent with the diff), and the slow files (the canon's).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F1 (this round): driver_stage_plan.py:676-677 and driver_gates.py:602-603 tell critic_rollcall plan_notes to next:S3:<planner> with the S3 tail 'it stays on your plan row and is tried again when S3 closes next', but plan_notes are code's failed question_refs writes with no retry (question_register._name_in_plan_row :2049-2076); give these two calls a true tail of their own and update the row 's4_after_critic: plan_notes (item 13)'",
    "N1 (node, owner FV1-9 Lead): the next:S3:<planner> key is read and forgotten by the S3 labelling window (driver_stage_plan.py:129, run_role :721/:737) on a stage_S3 re-entry, before window 2 that can act on a plan row; recommended: read/forget only for a dispatch whose record has no purpose, through the record (controller.s3_window_of / request_binding.purpose); meaning change of the key -> Lead decision and plan check",
    "Q1 (queue, P7 code-quality node): told_from is the third copy of the slice JSON parse beside driver_gates.py:331 and driver_machine.py:1706",
    "Q2 (queue or fold into F1): the designer+planner tell block is copy-pasted in driver_stage_plan.py:674-677 and driver_gates.py:598-603",
    "Q3 (queue, td-15 quarantine owner): test_place_session.py rows test_one_site_for_place_lines / test_one_site_for_neighbour_lines are red on origin/main too (they grep story_run.py for calls in driver_dispatch.py:717-718); the file is quarantined",
    "T-2 (Lead decision): the slow test_story_run_* row is missing; the halves are proved fast and the join is by reading, so drop it from T-2 or let the F1 builder write it unrun for the canon"
  ],
  "class_completeness": "All 36 SIBLING_MAP axes enumerated in the file. Axis 5: S4 author+critic loop covered, S5/S7 n/a (no question-entry carrier), skill road queued (P3/F-8), S3 window word -> node N1, gate A raise_move covered, A27 no new site. Axis 18: no ratchet raised. Axis 32: no judgment moved. Axis 34: no language/project/case branch; the H36 vs next: removal rule in one store is queued by the Lead (spec 7b Queue). State-exits row present with both key forms. Cards B, C, D: fit.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261114-fv1-9-tail-cards-spec.md",
      ".claude/worktrees/fv1-9-ta/docs/tasks/specs/reports/20261114-fv1-9-ta-report.md",
      "docs/tasks/critic-diff-brief.md",
      "docs/SIBLING_MAP.md (headings, axis 5)",
      "git diff origin/main...eef1219 (all 8 files)",
      "driver_dispatch.py:617-806 (branch)",
      "driver_stage_plan.py:78-137, 240-279, 323-363, 545-687, 828-853 (branch)",
      "critic_rollcall.py:395-414, 739-796, 1160-1209",
      "question_register.py _name_in_plan_row 2049-2076",
      "planning_contract.py notes producers 3357-3453",
      "controller.py:63-95",
      "references/stages.json acceptance_by",
      "driver_runner.py:211-235, driver_gates.py:320-335, role_cli.refuse",
      "audit_factory.py A27 baseline",
      "tests/test_place_session.py:380-393, origin/main test-layers.json quarantine",
      "git show ba52304, 1d65eb3, diff 659dcc4^1..659dcc4",
      "origin/main question_register.py:2486-2500, acceptance.stage_def_of, null_outcomes.stage_ids, hidden_repeat"
    ],
    "reruns": [
      {
        "command": "( cd C:/QAFactory/forge-repo/.claude/worktrees/fv1-9-ta/ai-packages/qa-factory && python -B scripts/tests/test_gate_question_form.py )",
        "result": "=== gate question form: 587/587 ok ==="
      },
      {
        "command": "git -C <fv1-9-ta> grep -n 's7_place_lines(\\|s7_neighbour_lines(' origin/main -- story_run.py driver_dispatch.py",
        "result": "only driver_dispatch.py:717,718,4026,4070; none in story_run.py"
      }
    ]
  }
}
```
