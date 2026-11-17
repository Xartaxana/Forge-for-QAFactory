# C3-reg-precondition (t-1082) — builder report

Branch `worktree-agent-a082beb63485edff8` (worktree agent-a082beb63485edff8), one commit, not pushed. Base: origin/main with C3-0, S9, FL4.

## 1. What was done (items 1-4; item 5 is not mine)

1. `Controller.validate`, `dispatch` branch (`ai-packages/qa-factory/scripts/controller.py`): one inline block after the `required` check (`raise ValueError("dispatch contract incomplete")`) and before the closure test (`THE closure test (B-331 ...)`). Late `from gate_template import registry_problem`; the text starts `gate registry unreadable:` and is the card's wording verbatim; it goes through `blocking, _ = self._passed_by_person(p["stage"], [text])` and `raise StateConflict(blocking[0])` when still blocking. No helper (no new census unit). Reads only `p["stage"]`.
2. `design/controller-blocks.md` written by `python -B tools/controller-blocks-gen.py <file>`: 355 -> 356 blocks, `person` 17 -> 18. The generator needed nothing (no table edit); it placed the row itself, in source order, as `validate | StateConflict | raise StateConflict(blocking[0]) | person | raised from the list _passed_by_person has already filtered`. See D1 (the row is generic, not the card's wording).
3. `design/state-exits.md`: the card's row appended to "What an infrastructure failure leaves".
4. `scripts/tests/test_controller_state.py`: `REG_PRECONDITION_ROWS` (9 rows: absent, zero-bytes, not-json, not-utf8, no-rows, passed-by-word, live, malformed-first, after-reinstall) + one function `test_c3_reg_precondition_one_stop_for_an_unreadable_registry`, registered in `main()` beside the tr4_7 tests. The file is a hand-rolled harness (no pytest parametrize anywhere), so the table is a loop over rows with row id in every assert message. Seam: `gate_registry.PLUGIN_ROOT` / `gate_template._READ` / `controller.validate_record`, all restored in `finally`. No existing dispatch-refusal table was found (grep `parametrize` -> none; other tables not of this shape).
5. Changelog fragment `ai-packages/qa-factory/changelog.d/rules-debt-c3-reg-precondition.md` (one English ASCII bullet).

## 2. Deviations / divergences between the card and the code (findings)

- D1 (card item 2 vs generator). The card's controller-blocks row text ("gate registry unreadable: ... | a factory defect (FR-3): reinstall ...") cannot be the key: `test_controller_blocks.py` keys on function + the source's raise head, which for this raise is `raise StateConflict(blocking[0])`. The card says "If tools/controller-blocks-gen.py places the row, its output is used": used as is. The consequence is that the row's "way through" is the generic text of the `_passed_by_person` family; it does not name the reinstall door or the waiver command. To carry them, the generator's BY_SEGMENT/COMMAND table (`tools/controller-blocks-gen.py`, outside my owns) needs an entry for this head, as `raise StateConflict(unreadable[0])` has (controller-blocks.md row `validate | raise StateConflict(unreadable[0])`). Question for the Lead: dispatch that tools edit, or accept the generic row? I did not decide.
- D2 (card item 4, row `malformed-first`). The card expects `ValueError("dispatch contract incomplete")` for a request missing `input_hash`. In reality `validate_record("Dispatch", p)` (first line of the branch) refuses first with `ValueError('$: missing input_hash')`, and a blank hash with `'$.input_hash: too short'`: `references/record-schemas.json:174-` Dispatch `required` is the same seven keys as the branch's `required`, so `dispatch contract incomplete` is unreachable through `apply`. To still pin the card's POSITION invariant (registry stop after `required`), the row replaces `controller.validate_record` by a no-op for that row only (restored in `finally`), drops `input_hash`, and expects exactly `ValueError("dispatch contract incomplete")` with the registry broken. Finding (analog, not fixed): the `required` check of the branch is dead code behind the schema; not in scope.
- D3 (item 1's open reading). `waiver.split_overridden` is `waiver.py:202-222`: it returns `(blocking, passed)`, where `passed` is `[{"error", "decision", "at"}]`. It files nothing. Every caller in the dispatch branch (this block included, `blocking, _ = ...`) discards `passed`; the pass is visible only as the recorded `stage_overrides[]` entry in `pipeline.json` (written by `waiver.py --stage ... --block ...`). So a pass over this factory-owned block is NOT filed as a factory finding by this road. Whether another carrier (the stage-exit's `passed-by-person.jsonl`, FV1-30a) records it for a dispatch-time block was not read. No waiver code changed.
- Audit A1 (C3-0 open finding): `gate_registry.py --check` exits 0 with this import in place; the output was grepped for `gate_template` / `unreachable` and has no A1 line (only the `source_freshness` row text names `gate_template.acceptable`). The `--check` does not print an A1 finding either way before my change (not run on base), so "this import clears it" is NOT established; only "check is green".
- Negative control stops at the first failing row: with the block removed the table fails at row `absent` (`('absent', 'None')`: the dispatch was recorded), the loop does not go on to `no-rows`. Every refused row would fail by the same cause.

## 3. Witness (verbatim tails)

DoD `python -B ai-packages/qa-factory/scripts/gate_registry.py --check`: exit=0; the registry file is not edited (`git diff` names no `references/gate-registry.json`); tail shows `6 gate(s) left as debt:` (`s5_window ... [B-179]` first), `6 gate(s) exempt:`.

`scenario_walk.py --witness-for <the four owns>`: 136 lines, 95 distinct test files, 30 of them not in `slow_tests.json` (the rest are listed slow; the four scenario files `test_scenario_*` are slow). Each of the 30 run alone from the package dir, `( cd <tree>/ai-packages/qa-factory && python -B scripts/tests/<f>.py )`, all exit 0:

```
test_awaiting_state 144/144 ok | test_controller_blocks 376/376 ok | test_controller_doors 31/31 ok | test_controller_lifecycle_gate 2/2 ok
test_coverage_controller_integration 2/2 ok | test_environment_lifecycle OK | test_event_store (exit 0) | test_exploration 219/219 ok
test_exploratory_answers 111/111 ok | test_first_look_step 105/105 ok | test_fixes_13797 70/70 ok | test_gate_vocabulary 141/141 ok
test_handed_to_person 58/58 ok | test_hook_lifecycle 25/25 ok | test_local_keys 345/345 ok | test_manual_evidence 262/262 ok
test_quality_demand 84/84 ok | test_question_register 945/945 ok | test_reference_window 85/85 ok | test_resume_packet 117/117 ok
test_resume_story_isolation 310/310 ok | test_s0_close_order 29/29 ok | test_s5_plan_windows 104/104 ok | test_s5_window_leftovers 148/148 ok
test_scoped_invalidation OK | test_session_handoff OK | test_stage_closure 88/88 ok | test_state_exits 142/142 ok
test_story_run_first_look 26/26 ok | test_story_run_s6_w1_frozen 6/6 ok
```

Listed slow but judging this change, run once each (exit 0, none timed out):

```
test_controller_state.py:  PASS test_c3_reg_precondition_one_stop_for_an_unreadable_registry
                           === test_controller_state: 378/378 ok ===
test_controller_blocks.py: === test_controller_blocks: 376/376 ok ===   (also in the 30 above)
test_state_exits.py:       === test_state_exits: 142/142 ok ===         (also in the 30 above)
test_judgment_census.py:   === judgment_census: 25/25 ok ===
```

`refusal_registry.py --check`: exit=0. `selftest.py --limits --lang`: `PASS limits: SKILL.md / agents / references within size caps`, `PASS limits: every mandatory role rule ...`, `=== qa-factory selftest: 4/4 ok ===`, exit=0.

Negative control (byte copy; block cut from `controller.py` between `from gate_template import registry_problem` and `# THE closure test`):

```
sha256 before  df7b977ffde9590af7354be3364335792dbdceed409784c58f846b00c73c51bc
run (block removed): FAILED as expected: ('absent', 'None')
restored by cp:  sha256 controller.py = df7b977ffde9590af7354be3364335792dbdceed409784c58f846b00c73c51bc ; copy = df7b977f...51bc (equal)
```

## 4. FR walk (by touched sections)

- A (refusals): FR-1 the text says what is wrong, what is expected (the file reads) and the door (reinstall/update, UPGRADE.md step 3). FR-2 the door is one the person can use; the conductor cannot reinstall and reports it (card E11). FR-3 the text reports an owner-factory defect and asks nothing. FR-4 the person's recorded word passes it (rows `passed-by-word`). FR-46 a malformed request is a ValueError first (row `malformed-first`). FR-57 not a dead end: the word and the reinstall both exist.
- B — text shown to a person: the new refusal is a factory report, not a question (FR-6 `human-questions.md` not engaged beyond FR-3); no question text added.
- C (contracts): FR-14 the refusal is a StateConflict with a stable prefix; FR-39 the guard is unchanged. No field read without a producer added.
- D (identity/evidence): FR-16/17 the registry is read only through `gate_template.registry_problem` -> `gate_registry.load_registry` (AR-13); FR-40 the state has a sanctioned way out (state-exits row); FR-58 expectations in the table come from the card's text, not the code's output; FR-59 an unreadable registry never becomes a pass.
- E, F — not touched. G: FR-30 package English/ASCII (selftest `--lang` PASS); FR-31 no timing dependence; FR-32 root cause with a test; FR-54 siblings below.
- AR touched: AR-9, AR-13, AR-15, AR-25, AR-28 (commit line). Census: `selftest`/`test_judgment_census` 25/25: no new unit (the raise is inside `validate`).

## 5. Needed from integration

- SIBLING_MAP axis-5 line (item 5, the Lead's): "one stop for an unreadable registry: `controller.validate` dispatch branch via `gate_template.registry_problem()` (C3-reg-precondition); per-site why texts are belt-and-braces". Mechanism path: not touched by me.
- D1: whether `tools/controller-blocks-gen.py` gets an entry so the row names the reinstall door and the waiver command.
- The merger of S9/FL4 re-derives the `controller-blocks.md` header counts if either adds blocks (card E10).

## 6. Analogs and waiting findings (not fixed)

- The `required` check of the dispatch branch is unreachable behind `validate_record` (D2).
- `split_overridden`'s passes are discarded by every dispatch-branch caller (D3): a pass over a dispatch-time factory block leaves only the override record.
- Per-site registry texts of C3-b2/C3-d remain belt-and-braces by decision.
- `driver_dispatch.KNOWN_REFUSALS` has no row (F-T13 (a)); the driver imports `controller` in-process, so a driver running across a reinstall keeps `_READ` until restart (card E3 (i)).

## 7. Needed beyond the manifest

`tools/controller-blocks-gen.py`, `ai-packages/qa-factory/scripts/waiver.py` (split_overridden), `references/record-schemas.json` (Dispatch), `ai-packages/qa-factory/scripts/tests/test_controller_blocks.py`, `scripts/slow_tests.json`, `scenario_walk.py` output.

tests-over: the nine rows of card item 4 (80 test lines).
