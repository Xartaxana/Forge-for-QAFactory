# t-723 attempt 2 - SC-A1c fix round (critic t-733), report

## Per finding
- F1 closed. The door is now the full s3.md form `finish --task <T> --dispatch-id <id> --digest "<digest>" --not-complete --unresolved plan_pending --reason "<words>"` in: `story_step.py` `_decide_refusal` (real task/did filled in), `controller.py` `_s3_completion_gate` (a) text, `changelog.d/sc-a1c.md`, and the generated `design/controller-blocks.md` (via its generator). The test row now extracts the named finish door from the refusal, checks all six flags are present, and runs it through `_unresolved_refusal` expecting "".
- F2 closed. `complete = not args.not_complete and (args.complete or dispatch_can_close_stage(dispatch))`. Row: `closes-no-roles` (a stage with no roles -> False). The finish site itself is not driven by a fast file; the predicate row is the pin.
- F3 closed. `driver_stage_plan.completion_for` reads `CT.record_purpose(record)` (local `import controller as CT`, same as its sibling methods). `record_purpose` docstring now "the one reader of a RECORD's purpose ... `s5_part_of`/`s7_part_of` read record-or-request". Rows (in test_stage_closure.py, no new file): reference_walk -> True; binding `"x"` -> no AttributeError, False; no binding -> False.
- F4 closed. `design/state-exits.md` row names both shapes (with `unresolved = plan_pending`, and none), same exit.
- N1 closed: comment finished ("`--open` is the one door").
- N2 closed: `planning_contract.py` "the stage's acceptor's judgment". I could NOT establish the S3 acceptor from `references/stages.json` (the S3 row lists only `qa-test-strategist` in `roles`, no acceptor field), so the generic wording was used as the spec allowed.

## Deviations / beyond owns
- `tools/controller-blocks-gen.py` EDITED (not in owns): the door text of controller-blocks.md lives in that generator's COMMAND map, so the md cannot change otherwise. One line.
- Regenerating controller-blocks.md also pulled two pre-existing drifts unrelated to this round (two `_s5_v2_collect` rows lost a parenthetical; count 219 -> 221). The generator is the authority; the file is now current.
- A stray file `--check` was created in the worktree root by calling the generator with `--check` (it takes an output path, no such flag); removed, `git status` shows none.

## Witness (verbatim)
`( cd .../sc-a1c/ai-packages/qa-factory && python -B scripts/tests/test_stage_closure.py && ...test_state_exits.py && ...test_null_outcomes.py && python -B scripts/selftest.py --limits --lang )`
```
=== stage closure: 88/88 ok ===
=== test_state_exits: 142/142 ok ===
=== test_null_outcomes: 327/327 ok ===
PASS limits: SKILL.md / agents / references within size caps
PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier
=== qa-factory selftest: 4/4 ok ===
```
Generator: `python -B tools/controller-blocks-gen.py ai-packages/qa-factory/design/controller-blocks.md` run twice; `git status --short` after the second run (no further change):
```
 M changelog.d/sc-a1c.md, design/controller-blocks.md, design/state-exits.md, scripts/{controller,driver_stage_plan,planning_contract,story_step}.py, scripts/tests/test_stage_closure.py, tools/controller-blocks-gen.py
```
Negative control F1 (`--reason` dropped from the door text in story_step.py; byte copy taken first):
```
sha256 before: 53496cc18623f5e22be4a856f4f58f0681621f0810c574892d57ce4c42db42c2
FAIL A1c decide-s3-window-one: --close refused: the finish door is the full form ...
FAIL A1c decide-s3-window-one: --close refused: the finish door passes `_unresolved_refusal` - expected '', got 'story_step: finish got --unresolved without --reason "<words>". ...'
(+ the same two for the halted-form row)   === stage closure: 84/88 ok ===
sha256 after restore: 53496cc18623f5e22be4a856f4f58f0681621f0810c574892d57ce4c42db42c2  (equal)
```
Slow files (`test_story_run_*`, `test_controller_*`, `test_fixes_13797`, slow_tests.json members): judged by the batch canon, not run.

## Siblings / analogs
Door text: all four sources aligned. Left per non-goals (queued by the critic): `s5_part_of`/`s7_part_of`/`brief_pack._purpose_word` record-or-request readers. Note `controller.py:7596` docstring still says "`finish --not-complete`" (shorthand in a docstring, not a door text).

## Needed beyond the manifest
`tools/controller-blocks-gen.py`, `references/stages.json` (read), `controller.py` / `contract.py` (read).

## Four questions / architecture
architecture: AR-25 (recorded state has an exit: F4), AR-13 (one purpose reader: F3), AR-9 (door usable: F1). judgment: none, no check added; text and a predicate reuse only.
