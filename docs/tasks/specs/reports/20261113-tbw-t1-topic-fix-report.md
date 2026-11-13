# T1 topic fix round (F1-F3) report

Branch `wip/tbw-t1`. Merge of origin/main first, then the fixes. Verdict: `docs/tasks/specs/reviews/20261113-tbw-t1-topic-code-critic.md`.

## F1 - merge of origin/main
- Merged: **12317b6** (the tip when I fetched and merged). TEMPORAL: origin/main moved to **819a31f** (FV1-19e C1/C2, AR-9/13 door pins,
  s6 console retake) while I worked; not chased, per the dispatch. The integrator merges 819a31f after this branch.
- Conflicts: `stage_joints.py` (topic side of `exit_members` / `EXIT_WRAPPERS` kept; main's duplicate `own(<family call>...)` unwrap block, which the
  topic's `while` loop already covers, dropped; `EXIT_FUNCTIONS =(` spacing fixed), `judgment-census.json` (rows: union - main's 3 rows
  `contract.py::_ref_shape_problems`, `contract.py::obligation_ref_problems`, `handoff_init.py::clean_purpose` kept next to the topic's; `about`
  and `ratchet` taken from the topic, then re-measured). `test-layers.json` merged on its own.
- Numbers that moved (command: `scripts/tests/test_judgment_census.py` totals line; `step0.py` over the test's own `told_world`, scratchpad):
  - `judgment-census.json ratchet.blocking_per_role.conductor 760 -> 761`: main's new unit `handoff_init.py::clean_purpose` (main itself moved 680 -> 681
    for it). Every other key unchanged: automator 190, bug-reporter 153, case-critic 173, case-designer 156, code-critic 160, doc-scribe 151,
    failure-analyst 162, requirements-tester 170, retro-analyst 156, runner 160, scout 152, test-strategist 186; safety 86, meaning 24, meaning-proxy 8.
  - `told-ratchet.json units branch_accounting.py::s5_problems bare 1 -> 3`: main's FV1-30a / FV1-19a refusals (a4fc87b, 2e8cd4d) added bare sites to an existing unit.
  - `told-ratchet.json units manifest_put.py::run bare 15 -> 16`: main's stderr refusal + `EXIT_BAD_FRAGMENT` (FV1-19 N1, 5f47f7b..7cf8c34).
  - Unchanged: `rowless 55`, `untold 253`, 220 role-reachable units (bare_total 859 -> 862, tagged 0), `conductor_only_units 616 -> 617`
    (the same new unit), `hand_cards 12`, `legacy_legs 9`, `unsited 0`, PINS 8/5/27 (the audit line prints walked exit 8, detector 5, window 27).
  - No raise from anything but main's new units / code; no STOP condition.
- INVARIANT on the merged tree: `units_no_row 0`, `join_share 1.0`, `check_arg_errors 0`, C1 green (no unit of main lacks a row; the 3 main rows
  cover the new units), so no row was added by hand.
- Features gate: the pre-commit WARN named `scripts/tests/fixtures/told-ratchet.json` (T1c's file) as matching no feature (a pre-existing offender,
  WARN not refusal); added to the feature that already owns `judgment-census.json` in `plans/features.json` (one line, no other change).
- Commit: the merge commit `6d9ecb4`.

## F2 - K5 real-tree row
- `test_stage_joints.py`: `told_unit_rows(ids, data)` builds `{unit: [rows]}` from the rows of the real file that state a requirement
  (`SJ._states_requirement`), grouped by `world["ids"]` (own id; a `<stem>:*` row for every id of that stem; a sub-id row for its parent id).
  `told_real` now calls `k5_problems(world["unit_roles"], told_unit_rows(world["ids"], REAL), SJ._mapped_roles())`.
  `role_set` removed; `k5_problems` calls `SJ._row_names(row, role, mapped)` (Q-d first item). Still empty today (0 rows state a requirement), live at T1r with no edit.
- New variant row `K5/real-reads-the-rows` (synthetic input: grouping, `<stem>:*`, a row with no requirement left out, red naming the missing role).
- Negative control on the REAL tree's own function (`k5ctl.py`, scratchpad; a stubbed input - a deepcopy of `REAL` with one row given a requirement and
  producer role `qa-nobody`; no tracked file touched, so no byte copy to restore):
```
real: []
real rows stating a requirement: 0
stub row exit_gate:scoped unit ('exit_gate.py', 'all_errors') unit roles ['qa-automator', ... 'qa-test-strategist']
stubbed: ['exit_gate.py::all_errors is met by qa-automator, qa-bug-reporter, ... qa-test-strategist, which no row of it names']
```
- Sibling sweep of `test_stage_joints.py` for a check on a call with literal empty arguments (`..., [])` with `{}` / `[]` / `set()` args): hits at `:138`
  (`audit(data=mutated(...))`, real data), `:233` (`SJ._demands_leg("acceptance:x", {...})`, real input), `:348` (`audit(data=mutated(...))`, real), `:500`
  (`conductor({})` against non-empty expected values, a deliberate empty edge): all real, none vacuous. The only vacuous one was the K5 row (fixed).
  Positive control for the search: the same pattern found the new `:829` line. Nothing left to fix, nothing queued.

## F3 - changelog fragments
- New `ai-packages/qa-factory/changelog.d/tbw-t1b-rows-schema-2.md` (T1b) and `tbw-t1c-told-counters.md` (T1c): English, ASCII, one bullet each.
  `tbw-t1-rows-v2.md` left as is (optional rename not done).

## Runtime (verdict answer 6)
- `test_stage_joints.py` measured 2m26s (146 s) once on this machine, `slow_tests.json` lists 67.6 s. Answer 6 / Q-a: the number is refreshed by the canon's
  `selftest.py --slow-tests` diff (`max_drift` 5), not by hand, and the cost cut (single shared wide scan) is a queued node. NOT hand-edited, NOT split.
  Risk named by the critic: `selftest --contracts` default 300 s ceiling (this run: 121.6 s inside it, see the witness).

## FR walk
- A (refusals): not changed in meaning; only a test row, fixtures and a merge. B - no text to a person changed. C - K5 now reads `SJ._row_names` (one reader). 
  D - n/a. E - n/a. F (FR-41, FR-59): K5/real no longer passes on an unknown (empty input). G - FR-30 English/ASCII (fragments, test text); FR-31 not load dependent; FR-44 the
  census-side counters stay in the test layer.

## Deviations
- `stage_joints.py` conflict: besides taking the topic side, I removed the `EXIT_FUNCTIONS =(` spacing typo (cosmetic).
- `plans/features.json` one line (the warning above).
- origin/main moved to 819a31f after the merge (see F1).

## Witness (verbatim)
Fast files from `scenario_walk.py --witness-for scripts/stage_joints.py scripts/contract_slices.py scripts/refusal_registry.py scripts/exit_gate.py`
(slow-listed files in the print - audit_rules, branch_accounting, console_encoding, read_json, resolver, resume_stopped, s5_plan_controller,
scenario_cart_1, scenario_local_1_*, story_run_s3_windows, words_doors - not run; judgment_census and stage_joints run as asked):
```
test_contract_slices      === contract slices (markup, generation, freshness, shipped map): 252/252 ok ===
test_detector_verdict     === test_detector_verdict: 209/209 ok ===
test_dispatch_identity    === test_dispatch_identity: 114/114 ok ===
test_dispatch_liveness    === test_dispatch_liveness: 441/441 ok ===
test_exit_gate_digest_source === exit gate digest source: 94/94 ok ===
test_exit_gate_lock_wait  === test_exit_gate_lock_wait: 8/8 ok ===
test_exit_gate_scope      === test_exit_gate_scope: 104/104 ok ===
test_exit_text_end        === exit text end: 50/50 ok ===
test_exploration_identity === test_exploration_identity: 66/66 ok ===
test_first_look_step      === test_first_look_step: 102/102 ok ===
test_guard_command_text   === test_guard_command_text: 197/197 ok ===
test_hook_lifecycle       === test_hook_lifecycle: 25/25 ok ===
test_host_adapter         === test_host_adapter: 95/95 ok ===
test_reference_window     === test_reference_window: 85/85 ok ===
test_refusal_registry     === test_refusal_registry: 504/504 ok ===
test_retro_numbers        === test_retro_numbers: 289/289 ok ===
test_role_digest          === test_role_digest: 93/93 ok ===
test_role_load            === role_load (the one measure of a role's start load): 186/186 ok ===
test_s0_close_order       === S0 close order: 29/29 ok ===
test_source_stage_integration === test_source_stage_integration: 21/21 ok ===
test_stage_of_dispatch    === test_stage_of_dispatch: 17/17 ok ===
test_stages               === test_stages: 135/135 ok ===
test_story_run_first_look === test_story_run_first_look: 27/27 ok ===
test_then_remainder       === test_then_remainder: 294/294 ok ===
test_validators           === test_validators: 343/343 ok ===
test_whole_identifier     === whole identifier and the revoked word: 166/166 ok ===
test_whole_list_sites     === test_whole_list_sites: 292/292 ok ===
test_stage_joints         === test_stage_joints: 292/292 ok ===   (2m26s; told: units_no_row 0, join_share 1.0, role_reachable_units 220, rowless 55, untold 253)
test_judgment_census      === judgment_census: 25/25 ok ===        (conductor=761 ... safety=86, breach=1)
contract_slices.py --check  slices: 44 declared, all present and fresh; 11 key pages; 12 charters carry a generated digest line
```
Before the ratchet re-cut the census test printed `FAIL test_c3_the_ratchet_is_dense_and_only_shrinks - blocking_per_role.conductor is 761, above its ceiling 760`
(the measurement that produced the named raise above); after it 25/25.
`selftest.py --contracts --lang` (package-dir subshell):
```
PASS lang: no control byte left by an eaten escape sequence (FR-29)
PASS tests: scripts\tests\test_null_outcomes.py  7.2s
PASS tests: scripts\tests\test_gate_registry.py  20.6s
PASS tests: scripts\tests\test_stage_joints.py  121.6s
=== qa-factory selftest: 5/5 ok ===
```
Inside `selftest --contracts` `test_stage_joints` took 121.6 s against the 300 s ceiling.
