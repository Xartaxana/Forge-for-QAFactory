# t-1089 — fix round of the C3 wave after critic t-1084 (rules-debt/1/RD1-7)

Branch `worktree-agent-ac40b44fb0a175afa`, not pushed. Commits: merge `31f6c82c` (origin/main), merge `e4654ffe` (C3-reg-precondition `c50ca830`), fix commit `6b2469f8`. Both merges were clean (no conflict); the generator run after them produced no diff to `controller-blocks.md` (header counts 356: caller 105, command 220, person 18, unpassable 13).

## Per fix
1. filed `plans/piles/rules-debt/findings/20261117-c3-bound-to-priyom-ne-preobrazovan.md` + row RD1-26. Twins checked by grep over `plans/piles/`: `green_on_current_bytes_why` / `run_history` / `compare_identity` appear only in EP1-44 (`_function_identity`) and RH2-4 (raw sha, `execution-report/2`), neither names `acceptance.py:177` or `run_history.py:221,256`; hotfix-12586 HF3-3 (the queue the SIBLING_MAP text points to) is closed and the sites still exist. So the twins JOIN this finding.
2. filed `...c3-odin-stroitel-teksta-reestr-ne-chitaetsya.md` + row RD1-27 (low, П3).
3. filed (a) `...c3-slova-probe-verdict-vnutri-preobrazovannyh-sajtov.md` + RD1-28; (c) `...c3-slovo-obzora-kritika-chitaetsya-vne-reestra.md` + RD1-29; (d) `...c3-holds-over-comments-udalit-ili-podklyuchit.md` + RD1-30 (low).
4. fixed `scripts/tests/test_controller_state.py`: the `validate_record` stub is gone; rows `malformed-first` (input_hash dropped) and `malformed-first-empty` (`input_hash: ""`) run through `apply` with the registry kept at `no-rows`; assert `type(got) is ValueError` and not starting with `gate registry unreadable`, and nothing recorded. The table now reports every row (per-row try/except, one assert at the end naming all failed rows).
5. filed `...c3-dispatch-prohody-ne-zapisany-cherez-record-person-pass.md` + row RD1-31.
6. fixed: `controller.py` local renamed `registry_blocking` (3 lines, only the C3-reg block); `tools/controller-blocks-gen.py` BY_SEGMENT entry `"raise StateConflict(registry_blocking[0])"`; `controller-blocks.md` diff is exactly one row, no header count changed.

## Deviations and notes
- The generator has no "message" override: the row's message cell is the source head (`raise StateConflict(registry_blocking[0])`), exactly as the precedent `raise StateConflict(unreadable[0])` does. The route (`person`) and the way-through text are as specified; the card's message text is not printed in the row.
- The generator writes only when given a path (`python -B tools/controller-blocks-gen.py <path>`); regenerated that way.
- Merge commits carry git's default message, not the three lines of the dispatch; the merge hook raised no refusal.
- The commit hook accepted the `tools/controller-blocks-gen.py` edit (no refusal). Index-stale hook not triggered.
- Findings: priority column in batch rows uses П2 / П3 (low = П3); finding files say `П3 (низкий)` for the two low ones only in the batch/README label, the finding header carries `П3`.
- Fix 3 (b) (`selector_contract:417`) is not in the verdict's fix list; not filed here.
- Not read beyond manifest: `docs/SIBLING_MAP.md` (grep only), `plans/piles/hotfix-12586/*`, `plans/piles/execution-report/*`.

## Witness (verbatim tails)
- `( cd PKG && python -B scripts/gate_registry.py --check )` -> `A26 gate registry: no violations`
- `test_controller_state.py` -> `PASS test_c3_reg_precondition_one_stop_for_an_unreadable_registry` / `=== test_controller_state: 378/378 ok ===`
- `test_controller_blocks.py` -> `=== test_controller_blocks: 376/376 ok ===`
- `test_state_exits.py` -> `=== test_state_exits: 142/142 ok ===`
- `test_gate_registry.py` -> `=== test_gate_registry: 498/498 ok ===`
- `test_judgment_census.py` -> `=== judgment_census: 25/25 ok ===`
- `refusal_registry.py --check` -> exit 0
- `selftest.py --limits --lang` -> `PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier` / `=== qa-factory selftest: 4/4 ok ===`
- `( cd T && python -B tools/piles.py check )` -> `(д) form: ok (35 piles, 106 batches)` ... `piles check: ok`

## Negative control (byte copy)
Copy of `controller.py` taken to scratchpad, sha256 `7f56c1c333183cb50595bb4ef34a0fb350e97b7b1b87517408ee7dd2917592e2`. The C3-reg block cut (from `from gate_template import registry_problem` to `raise StateConflict(registry_blocking[0])`). Result:
`FAIL test_c3_reg_precondition_one_stop_for_an_unreadable_registry — 6 of 10 rows failed: [('absent'...), ('zero-bytes'...), ('not-json'...), ('not-utf8'...), ('no-rows'...), ('after-reinstall'...)]` / `=== test_controller_state: 377/378 ok ===`.
`no-rows` FAILs; `malformed-first`, `malformed-first-empty`, `passed-by-word`, `live` PASS (not in the failed list). Restored with `cp`; sha256 of the file and of the copy both `7f56c1c333183cb50595bb4ef34a0fb350e97b7b1b87517408ee7dd2917592e2`; `git status` shows controller.py only as the staged/committed fix.
