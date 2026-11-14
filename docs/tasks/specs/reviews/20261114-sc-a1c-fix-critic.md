# t-733 — critic re-review of SC-A1c fix diff 1927774 (wip/sc-a1c), against verdict t-717 answer 8

Scope: ONE diff (17 files, +358/-62) against the A1c list of `docs/tasks/specs/reviews/20261114-stage-critics-topic-a-critic.md`
and the dispatch DoD items 1-4. No code edited, no CI, one cheap control re-run.

## Verdict

**fit_with_fixes** (NEEDS WORK). Item 1's invariant holds at every site, and so does the proof that nothing outside S3 window 1
changed. There are no blockers to the design. Fixes F1-F4 below are small and land in this round, before the merge with A1a/A1b. F1 is
an FR-2 defect in the new refusal text, which is the very row the DoD asked for.

## Findings

**F1 (fix before merge; FR-1/FR-2, key 7). The new `decide --close` refusal on window 1 names a door that `finish` refuses.**
`story_step.py:2836-2839` says: "or `finish --not-complete --unresolved plan_pending` ends the window". `finish` runs
`_unresolved_refusal` first (`story_step.py:1736`). It refuses `--unresolved` without `--reason`. Probe (pure function, verbatim):
`_unresolved_refusal(ns(not_complete=True), 'plan_pending', '')` -> `'story_step: finish got --unresolved without --reason "<words>".
They go together: ...'`. With `reason='w'` it returns `''`. The command also has no `--task/--dispatch-id/--digest`. The canonical
form already exists in `skills/qa-story/phases/s3.md:27,100`:
`finish --task <T> --dispatch-id <id> --digest "<digest>" --not-complete --unresolved plan_pending --reason "window 1 accepted; the plan is window 2"`.
The same omission sits in the same file: `controller.py:7605-7606` (`_s3_completion_gate` (a) "it is accepted with --not-complete --unresolved
plan_pending"). It was there before, but this diff edits that function's docstring, so the sweep covers it (rule 9). Its generated twin is
`design/controller-blocks.md:340`, and `changelog.d/sc-a1c.md:5` repeats the text. Fix: give the full s3.md form, with `--reason "<words>"`,
in all three sources, then regenerate controller-blocks. The test row `decide-s3-window-one: names a door: finish`
(`test_stage_closure.py`, substring `plan_pending`) pins the broken text and would not catch this. Running the named door through
`_unresolved_refusal` in that row would catch it.

**F2 (fix in round; DUPLICATION item 6, key 5). A copy of the closing-role test is left inside the predicate's site.**
`story_step.py:2496-2497`: `role == stage.get("roles", [role])[-1] and dispatch_can_close_stage(dispatch)`. The first conjunct is
`contract.stage_closes_with` again (`contract.py:5903-5908`: `roles[-1] == role`). Both read `references/stages.json` (`story_step._stages`
:115-116 and `contract.stage_roles`). That makes it a second copy of the test the predicate was created to own. It also raises IndexError on a
stage with `roles: []`, which the predicate alone answers False. Fix: `complete = not args.not_complete and (args.complete or
dispatch_can_close_stage(dispatch))`.

**F3 (fix in round; AR-13 sweep-the-artifact, key 5/6). A binding-only purpose copy is left in the function the diff edits.**
`driver_stage_plan.py:899` (`completion_for`, 8 lines above the re-pointed T2 site) still reads
`(record.get("request_binding") or {}).get("purpose") == "reference_walk"`. That is the rule `record_purpose` implements. It also raises
AttributeError on a truthy non-mapping binding (`"x".get`), a case `record_purpose` answers `""` for. Fix: `CT.record_purpose(record) ==
"reference_walk"`. Related: the docstring `controller.py:115` says "The one public reader (AR-13)". In the same file, `s5_part_of` (:155-159)
and `s7_part_of` (:168-173) read the same field by a DIFFERENT rule: binding when the key exists, else top `purpose` (a request that is not
yet a record). `brief_pack._purpose_word` (:874-881) copies that second rule. These are not copies of `record_purpose`, so they are not this
round's fix. Folding them needs a decision on the request-or-record reader. Queue line below. The docstring should say "the one reader of a
RECORD's purpose; `s5_part_of`/`s7_part_of` read record-or-request".

**F4 (fix in round; AR-25/FR-40 carrier, key 2).** `design/state-exits.md:43` defines the state "S3 open, window 1 accepted" with the
condition `unresolved = plan_pending`. After this diff, window 1 can also be accepted with NO `unresolved` (Q1, test row
`accept-s3-window-one-not-complete`). The code exit does not depend on `unresolved` (see key 2), so the table row only has to drop that
condition or name both shapes. A recorded state the exits table does not describe is the FR-40 carrier gap.

**N1 (code quality, fix with F1).** The comment at `story_step.py:1903` stops mid-sentence: "`--open` is". Finish it or cut it.

**N2 (stale text, fix in round if owns are widened, else queue).** `planning_contract.py:113`: "Whether what the strategist wrote is RIGHT
is the S3 critic's judgment". The S3 critic is gone, and this line names the AR-29 owner of a judgment, so it is not cosmetic. The builder
listed it. My t-717 list missed it.

## Answers to the keys

**(1) Invariant of item 1.** Kept. Proof by construction: `dispatch_can_close_stage` (`controller.py:99-109`) = `stage_closes_with` AND
`s3_window_of != "labelling"`. `s3_window_of` returns `"exit"` for every non-S3 record (`:94-95`) and for every S3 record whose binding
purpose is not `s3_labelling`. So the predicate equals the old `stage_closes_with` everywhere except S3 window 1. The exit window (no purpose,
or any other purpose), S5 plan and S7 investigation answer exactly as before. In `_closes_stage` (:7654-7666) the S5-plan and S7 exemptions
still follow the predicate. Test rows `closes-s5-plan-unchanged` and `closes-s7-investigation-unchanged` give `(True, False)`. Window 1 at
each site:
- apply default (:5131): `_closes_stage` False, so no `stage_complete` is injected and the gate takes branch (b).
- validate "no role to close it" (:5884): not raised for window 1.
- `stage_repairs` (:8627): no invented `stage_completed`.
- `_halt_doors`: `--open` only.
- `_decide_refusal`: `--close` refused.
- `finish` recorded close: notes only.
- `finish` default: False.
- `decide` print: unreachable for a window-1 close.

The only road to `stage_complete: true` on window 1 is the explicit `--complete`. It reaches `_s3_completion_gate` (a) (:7603-7606),
which is unchanged and still refuses. Test row `accept-s3-window-one-complete` confirms this. One behaviour does change: a raw controller
`accept` of window 1 with NO `stage_complete` used to get the injected True and be refused at (a). Now it is accepted as not complete. That
is the pre-A1a behaviour, and it is the intended one.

**(2) Builder Q1: S3 between windows with nothing unresolved.** Safe; no refusal is needed. The way out: `next_action` answers `prepare_stage
S3` for any S3 that is not completed (`controller.py:9208-9238`). `stage_S3` sees `between` because `s3_window()` reads only the purpose
and `status == accepted` (`driver_stage_plan.py:334`), not `unresolved`, so window 2 runs (or window 1 again by `s3_fresh_for_window2`).
`stage_repairs` does not close it (F-predicate). No code reader keys on `unresolved == plan_pending`. Grep of `plan_pending` over the
package: only the producer `driver_stage_plan.py:487` (positive control), docs, and the texts in F1. I agree with the Lead's intended
answer, provided F4 updates the exits table. The decision belongs to the Lead.

**(3) Bare `finish` default on window 1.** No caller can have relied on the old default. It sent `stage_complete: true`, which
`_s3_completion_gate` (a) always refused, so that road never succeeded. The driver never sends a bare finish for window 1:
`s3_window_completion` always returns `OpenWork("plan_pending")` (`driver_stage_plan.py:484-488`), which `driver_dispatch.py:792-833` turns
into `--not-complete --unresolved plan_pending --reason <text>`. The skill road (`phases/s3.md:27,100`) passes explicit flags.

**(4) Import cycle.** None. `story_step` already imports a dozen names from `controller` at module top. The two new names are module-level
functions defined at `controller.py:99,112`, before any class. `controller.py` has no `import story_step`: case-insensitive grep, empty;
the same-shape control `import contract` found :538/:1558/:2115. `dispatch_can_close_stage` imports `contract` lazily, and `contract.py`
does not import `controller` (grep empty; same tool found `import contract as C` in story_step.py:95).

**(5) Duplication and code quality.**
- DUPLICATION AND CONSISTENCY: F2 (closing-role copy at `story_step.py:2496`) and F3 (purpose copy at `driver_stage_plan.py:899`). Grepped:
  `stage_closes_with` over the package minus tests. Live callers are only the predicate (:104/107) and `_is_review_of` (:4108/4113).
  `_is_review_of` is not applicable: it is the stamp predicate over another role's review, and the reworked role itself is excluded. Also
  grepped `roles...[-1]`, which hit `contract.py:5908` and `story_step.py:2496`, and `request_binding.{0,40}purpose|binding.get("purpose")`
  over the scripts, which gave the list in F3. N2 is done: `parts_of` is used for the own stage and for each earlier part, and the brief
  output is unchanged (test_brief_pack 1125/1125 in the builder's layer).
- CODE QUALITY: N1 (truncated comment). In `_decide_refusal` the window-1 branch comes before the non-closing branch, and that branch is then
  guarded by `and not _labelling(dispatch)`. The guard is redundant for `close`, which already returned, but it is needed for `open`, so it
  is correct. No new function is over 60 lines. Test rows are one parameterised table per behaviour, with ids that name the case.

**(6) Class completeness by the map.**
- Axis 5, row "The S3 window word": `s3_window_of` is still the one reader of the stored word and now reads through `record_purpose`.
  `_labelling` reads through it. The `phases/s3.md` twin already gives the full finish form, so F1 aligns the code text with it.
- Axis 5, row "Stage exit <-> its finish": not touched.
- The state-exits carrier is in F4.
- Must be fixed in this round: F1 (including `controller.py:7606` and its generated twin), F2, F3 (:899), F4, N1, and N2 if owns are widened.
- Queue lines:
  - "one reader of a dispatch's purpose: fold `s5_part_of`/`s7_part_of`/`brief_pack._purpose_word` (record-or-request rule) and
    `reference_snapshot.py:69`, `report_facts.py:1887,2323` (binding-only copies) and `stage_guard._record_purpose` (top fallback) |
    узел: <Lead opens in an untaken batch of the stage-critics pile>".
  - "stale S2/S3-critic labels in kept tests `test_controller_rework_scope.py:585`, `test_coverage_controller_integration.py:43`,
    `controller_rework_common.py:152`, `story_run_common.py:297` | узел: <same>".
- Quarantined readers (`test_brief_pack_roles.py`, `test_controller_stage_acceptance.py`, `test_handoff_init_author.py`,
  `test_rows_owed.py`, all confirmed in the `quarantine` section of `test-layers.json`) are covered by the §O owner notice already proposed
  in t-717. They are not this round's fix.
- `test_conductor_doors.py:1078-1083`: not applicable. These are historical situation texts used as classifier inputs, not claims about
  current behaviour.

**(7) FR-1/FR-2 on the window-1 `decide --close` refusal.** FR-1 holds. The text says what is wrong ("S3 window 1 ... never closes S3")
and what is expected ("the plan is owed after it"). FR-2 fails for the second door (F1). The first door, `--open [<ids>]`, is usable: in
`_decide_refusal` the window-1 `open` reaches only the scope check, which is test row `decide-s3-window-one: --open is the door and is
taken`. Unverified and out of this diff: whether the person's words of a window-1 `--open` reach window 2. A1a made `--open` legal for the
strategist and A1c keeps it. The `decide` print "the rework of that work starts by itself" may not describe what happens on S3. I name this
for the Lead as a question to trace (AR-24), not as a finding.

## Spot-checks (load-bearing claims of the report)
- "80/80, negative control 74/80": re-ran `test_stage_closure.py` and got `=== stage closure: 80/80 ok ===`. The negative control's six
  FAIL lines match the six window-1 rows of the diff, which is consistent.
- "story_step's `C` is `contract`": confirmed at `story_step.py:95` (`import contract as C`).
- "`_is_review_of` correct as is": read at `controller.py:4105-4113`. I agree.
- "No ratchet or pin raised": the diff touches no ratchet file. The `test_null_outcomes` label edit changes only the label, and the values
  are unchanged.
- Negative "no live `stage_closes_with` outside the predicate except `_is_review_of`": `git grep -n -i stage_closes_with` over
  `ai-packages/qa-factory` minus tests. Positive control: the same call finds `contract.py:5903` and `controller.py:104`.

## Trail
Read:
- The verdict t-717 (:18-157) and the builder report (whole).
- `critic-diff-brief.md` (:8-105) and `SIBLING_MAP.md` axis 5 (:111-158).
- Diff 1927774 in full.
- `controller.py:93-176, 4095-4120, 5120-5140, 5870-5900, 7591-7700, 8605-8630, 9195-9240`
- `story_step.py:95-123, 1185-1200, 1890-1925, 2385-2540, 2700-2720, 2815-2870, 3095-3120, 3357-3386`
- `driver_stage_plan.py:100-140, 320-345, 476-500, 895-925, 1015-1030`
- `driver_dispatch.py:785-880, 955-975`
- `contract.py:5862-5866, 5903-5908`
- `stage_guard.py:136-137, 219-265`
- `brief_pack.py:872-884`
- `planning_contract.py:105-115`
- `driver_core.py:624-626`
- `test-layers.json` (quarantine membership)
- `test_conductor_doors.py:1078-1083`, `test_brief_pack_roles.py:409-415`

Commands:
- `python -B scripts/tests/test_stage_closure.py` (sc-a1c package dir) -> `=== stage closure: 80/80 ok ===`
- Probe of `_unresolved_refusal` / `_decide_refusal` (output quoted in F1)
- Greps listed in keys 4, 5 and 6, each with its positive control.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Item 1 invariant kept: the predicate equals stage_closes_with everywhere but S3 window 1 (s3_window_of answers exit off S3), all 8 sites re-pointed, _s3_completion_gate untouched and still the last word. Sweep gaps fixed this round: story_step.py:2496 closing-role copy (F2), driver_stage_plan.py:899 purpose copy (F3), controller.py:7606 same broken door text as the new refusal (F1), state-exits.md:43 condition (F4). Queued with node lines: record-or-request purpose readers s5_part_of/s7_part_of/brief_pack._purpose_word plus reference_snapshot.py:69, report_facts.py:1887,2323, stage_guard._record_purpose; stale critic labels in four kept tests. Quarantined readers stay under the t-717 owner notice.",
  "fixes": [
    "F1 story_step.py:2836-2839 and controller.py:7605-7606 (+ regenerated design/controller-blocks.md:340, changelog.d/sc-a1c.md:5): the finish door lacks --reason (and --task/--dispatch-id/--digest); _unresolved_refusal refuses it as written; use the phases/s3.md:27 form with --reason, and make the test row run the named door through _unresolved_refusal",
    "F2 story_step.py:2496-2497: drop the duplicate role == roles[-1] conjunct; dispatch_can_close_stage alone decides",
    "F3 driver_stage_plan.py:899: read the reference_walk purpose through CT.record_purpose; reword controller.py:115 'the one public reader' to 'the one reader of a record's purpose'",
    "F4 design/state-exits.md:43: the window-1-accepted state no longer requires unresolved = plan_pending; widen the condition",
    "N1 story_step.py:1903: finish the truncated comment",
    "N2 planning_contract.py:113: 'the S3 critic's judgment' names a removed owner (fix if owns widened, else queue)"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/reviews/20261114-stage-critics-topic-a-critic.md",
      ".claude/worktrees/sc-a1c/docs/tasks/specs/reports/20261114-sc-a1c-report.md",
      "docs/tasks/critic-diff-brief.md",
      "docs/SIBLING_MAP.md axis 5",
      "git show 1927774 (full)",
      "scripts/controller.py 93-176, 4095-4120, 5120-5140, 5870-5900, 7591-7700, 8605-8630, 9195-9240",
      "scripts/story_step.py 95-123, 1185-1200, 1890-1925, 2385-2540, 2815-2870, 3095-3120, 3357-3386",
      "scripts/driver_stage_plan.py 100-140, 320-345, 476-500, 895-925, 1015-1030",
      "scripts/driver_dispatch.py 785-880, 955-975",
      "scripts/contract.py 5862-5866, 5903-5908",
      "scripts/stage_guard.py 136-137, 219-265",
      "scripts/brief_pack.py 872-884",
      "scripts/planning_contract.py 105-115",
      "scripts/tests/test-layers.json quarantine",
      "design/state-exits.md:43, skills/qa-story/phases/s3.md:27,100, design/controller-blocks.md:340 (grep hits)"
    ],
    "reruns": [
      {"command": "python -B scripts/tests/test_stage_closure.py (sc-a1c package dir)", "result": "=== stage closure: 80/80 ok ==="},
      {"command": "probe: story_step._unresolved_refusal(ns(not_complete=True), 'plan_pending', '')", "result": "story_step: finish got --unresolved without --reason \"<words>\". They go together: ... (refused); with reason 'w' -> ''"}
    ]
  }
}
```
