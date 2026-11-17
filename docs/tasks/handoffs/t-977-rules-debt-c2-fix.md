# t-977 report: C2 fix round (findings C2-1..C2-6), attempt 2

Worktree `C:\QAFactory\forge-repo\.claude\worktrees\fix-c2`, branch `fix/t-977`, one commit on top of 753bffec.

## Per finding

- C2-1: `test_controller_doors.py:30` dropped `check_not_in`. `pyflakes` prints nothing.
- C2-2: `row_gate_decision` now runs the real door: `harness.run_controller_inprocess(["--task-root", task, "--operation", "gate-decision", "--gate", "A", "--words-file", <file>], root)` (file `work/gate-a-words.txt`, root = `task.parents[2]`), then checks exit 0 and the Gate A status `approved`. The BASE world CARRIES the door (no question needed). The stale-revision refusal part of the row still uses `controller.apply("decision", ...)` (it is the block, not the door). `row_checkpoint` and `row_recover`: chose the cheaper honest option, the docstring now says "the operation's body" (`controller.apply("checkpoint", ...)` / `controller.recover()`); not CLI.
- C2-3: `pinned` is now `with hooklib.selftest_root_restored(): hooklib.pin_project_root(project); yield`; `import os` removed (unused).
- C2-4: `synthetic_world` calls `harness.mark_project(root)`. BASE world behaviour unchanged: 31/31 ok.
- C2-5: `row_checkpoint` checks `needle` (the walk text), not the literal.
- C2-6: controller.py, `deployment_inputs`: the `if not any(...): raise StateConflict("approved Gate A required before deployment")` block deleted (4 lines), nothing else. Walk regenerated.

## C2-6 trace (own re-trace, current lines)

`deployment_inputs` (controller.py:2252): `state = self.state()` (:2260), then `self._validate_gate_a_content_current(state)` (:2261). That function (:4747-4754): `decision = self._current_gate_a(state)`; if falsy it calls `self._raise_all(self._noted([(StateConflict, "current Gate A decision required")], ...))`; `_raise_all` raises for any non-empty list (so it never returns on that path). `_current_gate_a` (:4741-4745) is: gate A, status approved, `source_revision == state.get("source_revision")`, over `state["decisions"]`. The deleted `any(...)` was the same predicate over the same `state` object (`state.get("decisions", {})`), with no write between the two. Past :2261 a current approved Gate A exists, so `any(...)` was always True and the raise unreachable. Invariant kept: deployment without a current approved Gate A is still refused, by `_validate_gate_a_content_current`, before `deployment_readiness` builds anything. Pin check: grep (case-insensitive, `approved Gate A required before deployment`) over the worktree, positive control = it finds controller.py:2265 and the walk row before the edit; hits outside owns: only `tools/controller-blocks-gen.py:54` (generator `COMMAND` dict key, see analogs). No package test pins the text or the 221-row count (`test_controller_blocks.py` has no 353/221 literal; it passes).

Walk diff (regenerated with `python -B tools/controller-blocks-gen.py ai-packages/qa-factory/design/controller-blocks.md`; regenerating again into a temp file is byte-identical to the committed one): header 353 -> 352, `command` 221 -> 220, and the row

`| deployment_inputs | StateConflict | approved Gate A required before deployment | command | the gate decision itself (gate-decision) |`

is gone (old row 55). The gate-decision family stays covered by the `decision references stale source revision` row (old 128); `DOOR_FAMILIES` finds all four families by block text (31/31 ok).

## FR walk

A (refusals/doors): the refusal for "no current Gate A" is unchanged in text and door (FR-1, FR-2 hold); the deleted block was unreachable so no refusal was lost (FR-4 n/a, no silent pass created). B: no text a person reads changed. C: n/a. D: FR-17/FR-54: harness helpers (`mark_project`, `run_controller_inprocess`, hooklib pair) now used instead of copies. E, F: n/a. G: FR-30 English only; selftest --lang passes.
AR-9: door named by the refusal is unchanged and now executed for gate-decision. AR-25: the recorded state "no current gate A" still has its move.

## Witness (verbatim)

DoD command, in the worktree: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/controller.py ai-packages/qa-factory/scripts/tests/test_controller_doors.py` (real 25.1s), output: the scenario rows
```
scripts/controller.py: scenario test_scenario_cart_1.py (story cart-1)
scripts/controller.py: scenario test_scenario_local_1_0108.py (story local-1-0108)
scripts/controller.py: scenario test_scenario_local_1_arm_b.py (story local-1-arm-b)
no scenario or keep row covers scripts/tests/test_controller_doors.py: run the whole scenario layer
scripts/tests/test_controller_doors.py: test_scenario_cart_1.py / _local_1_0108 / _local_1_arm_b / test_scenario_walk.py / test_scenario_world.py
```
plus 84 `keep` rows for controller.py (92 lines in all).

Each printed file run separately (cwd `scripts/tests`, `python -B <file>`); files listed in `slow_tests.json` or named `test_controller_*` / `test_story_run_*` (other than the doors file) and the three scenario files: not run, "судит канон пачки". Results:
```
rc=0  9.7s test_controller_doors.py   === 31/31 ok ===
rc=0  3.7s test_scenario_walk.py      === 93/93 ok ===
rc=0  0.7s test_scenario_world.py     === 33/33 ok ===
rc=0  5.7s test_awaiting_state.py 144/144 | 19.7s test_detector_verdict.py 464/464 | 5.7s test_exploratory_answers.py 107/107
rc=0 10.1s test_first_look_step.py 105/105 | 9.8s test_fixes_13797.py 70/70 | 5.4s test_gate_vocabulary.py 141/141
rc=0  8.0s test_handed_to_person.py 58/58 | 4.6s test_hook_lifecycle.py 25/25 | 17.3s test_local_keys.py 345/345
rc=0  5.0s test_quality_demand.py 84/84 | 8.3s test_reference_window.py 85/85 | 3.0s test_resume_packet.py 117/117
rc=0  2.2s test_resume_story_isolation.py 310/310 | 4.9s test_s0_close_order.py 29/29 | 13.4s test_s5_plan_windows.py 104/104
rc=0  5.7s test_s5_window_leftovers.py 148/148 | 11.2s test_stage_closure.py 88/88 | 1.4s test_state_exits.py 142/142
rc=0  1.7s test_environment_lifecycle.py | 5.3s test_event_store.py | 1.8s test_scoped_invalidation.py | 2.6s test_session_handoff.py (no summary line, exit 0)
```
Extra (fast, consumer of the walk): `test_controller_blocks.py` (real 5.1s) `=== test_controller_blocks: 372/372 ok ===`.
pyflakes on test_controller_doors.py: no output (clean).
Generator has no check mode (its argument is the output path); identity check: regeneration to a temp file `cmp` identical.
`( cd <worktree>/ai-packages/qa-factory && python -B scripts/selftest.py --limits --lang )` (real 2.5s): `PASS limits: SKILL.md / agents / references within size caps`, `PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier`, `=== qa-factory selftest: 4/4 ok ===`.

## Needed beyond the manifest

`ai-packages/qa-factory/scripts/tests/harness.py`, `scripts/slow_tests.json`, `tools/controller-blocks-gen.py`, `tests/test_gate_words_road.py` (CLI argv shape), `tests/test_controller_blocks.py`, `scripts/hooklib.py` (read via the review).

## Analogs noticed

- `tools/controller-blocks-gen.py:54` still holds the `COMMAND` key `"approved Gate A required before deployment"`: now an orphan entry (harmless, generator output is correct). Outside owns; queue to Lead (an orphan-key check in the generator would be the class fix).
- `tests/fixtures/judgment-census.json` mentions `deployment_inputs`; not read or touched, may carry a row about the removed block.
