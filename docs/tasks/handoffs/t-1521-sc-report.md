# t-1521 S-C report: the `test:` line gate

Items (spec 5.1, 1-7): all DONE. Files: tools/dispatch_manifest.py, tools/dispatch_new.py (both STAGED, not committed), tools/test_dispatch_manifest.py, tools/test_dispatch_new.py (committed).
1 `test_lines` / `_test_line_parse` / `_test_line_state` (dispatch_manifest.py:1003 and neighbours). 2 check_cut gate: builder + threshold, label `no line` | `ill-formed: <80 chars>`. 3 one token `test`. 4 sites below. 5 door `manifest-skip: test -- <reason>`. 6 `TEST_LINE_REFUSES = True` (:120); False -> note TEST LINE NOT ENFORCED. 7 `--test` repeatable in dispatch_new.py, printed after DoD:, backtick/newline and empty-item refusals apply.

## Iteration sites of item 4 (line after edit, tools/dispatch_manifest.py)
- `SKIP_ONLY_ITEMS` :108, `ALL_ITEMS = ITEMS + SKIP_ONLY_ITEMS` :109, `_DISPLAY.update` :111
- `_parse_skip_line` :316 (`name not in ALL_ITEMS`)
- `SKIP_REFUSED_TEMPLATE` :168 (lists ALL_ITEMS -> "..., facts, test")
- `newly` :1206; `still` :1214; `_items_text` :1033 reads `_DISPLAY` (has `test`)
- `_FORM_HINTS["test"]` :137. `_expected_forms()` is built over `_FORM_GROUPS`, not ITEMS, so unchanged; the hint is inserted into the INCOMPLETE message only when `test` is still missing (before " To send it anyway on purpose", :1222) -- my choice, so no other refusal text grows.
- dispatch_new.py: `--test` parser line; `_empty_item` tuple gains "test"; `build_text` emits `test:` lines after DoD:.

## Tests (spec 7.5 test-line rows)
- tools/test_dispatch_manifest.py::TEST_ROWS (27 ids: the pass and refuse inputs of the adversarial list) + test_test_line_labels_scope_and_switch (labels, non-builder, skip note, switch off). `PARTS` gains a default `test` line (E-C3): every over-threshold fixture carries one. Changed cases: K1 (expects `test` in missing), K5/K7 (a test line prepended), K6 (text gains `test`); no check weakened.
- tools/test_dispatch_new.py: rows `test-line-printed`, `test-line-absent-over-threshold`; `TEST` added to 4 designer rows, SKIP_D and test_block_leaves_the_manifest_reads_unchanged (E-C3).
- Budget: tests +82 lines vs code +97.

## Witness
`python -B -m pytest tools/test_dispatch_new.py tools/test_dispatch_manifest.py tools/test_dispatch_gate.py -q` ->
`FAILED tools/test_dispatch_gate.py::test_main_folds_the_coordinator_read_warn_into_additional_context[main-thread]` / `1 failed, 812 passed in 28.28s`
The one red is the KNOWN one (FG7-89), untouched.
Siblings: `python -B -m pytest tools/test_owns_gate.py tools/test_hook_liveness_probe.py tools/test_journal_hooks.py -q` -> `288 passed in 132.46s`: none asserts a launch decision on an over-threshold builder prompt that turned red (test_owns_gate.py:63 and test_journal_hooks.py:259 build `designer: skip` prompts; green).
`python -B tools/registry_preflight.py check lint --paths tools/dispatch_manifest.py tools/dispatch_new.py` -> `registry preflight: lint ok (0.4 s)`
not run locally: tools/test_dispatch_gate_md.py (markdown variant), canon judges. test_dispatch_gate.py needed no edit.

## Notes
- READERS NOTE in check_cut untouched.
- The hint carries the Cyrillic section name from the spec (`docs/TESTING.md «Строка теста в DoD»`); tools/ is outside the package language check.
- No CHANGELOG fragment: tools/ is not package.
- Analog: the `EXTRA_SKIP_ITEMS` comment ("kept out of ITEMS so texts stay byte for byte") is now partly stale for SKIP_REFUSED text. No other.
- Staged mechanism files: tools/dispatch_manifest.py, tools/dispatch_new.py.

## Round 2
- S-C-1 fixed: tools/dispatch_manifest.py `_TEST_KEY_RE` (optional closing backtick) + `_test_line_parse` (leading backtick stripped alone); row `pass-backticked-key` in TEST_ROWS.
- S-C-2 fixed: `_dod_commands` skips lines where `_test_line_parse` is not None; row in test_dod_run_check (test line naming a canon file inside the DoD extent -> 0).
- S-C-3 fixed: dead `test_lines` removed (`_test_line_state` is the one loop); `designer_threshold` computed once in check and passed to `_form_missing`; row `test-line-blank-item` in test_dispatch_new.py CASES.
- S-C-4 fixed: docs/TESTING.md names the gate in tools/dispatch_manifest.py; CLAUDE.md R11-f lists `test:`. BOOT BUDGET before/after: CLAUDE.md 14495 -> 14565 / 16700; total 118404 -> 118474 / 120000.
- Witness: `python -B -m pytest tools/test_dispatch_manifest.py tools/test_dispatch_new.py tools/test_dispatch_gate_md.py -q` -> `498 passed in 2.43s`; `python -B tools/pointer_lint.py --check` -> `pointer_lint: ok (34 files, 1959 pointers)` rc=0.

## Round 3 (attempt 3, Opus; verdict t-1530 R1-R4)
- Merge: origin/main (S-B 64186e28, S-D 9ee5c5e2) merged into the branch as d705436c (parents 2b389a03, 9ee5c5e2). CLAUDE.md conflict: R11-f taken from this branch with the R4 fix, R11-h taken verbatim from main (the critic's-probe clause kept); AGENTS.md: main's side taken (`git -C <wt> checkout --theirs AGENTS.md`, my own worktree) then regenerated with `python -B tools/agents_md.py` (114879 bytes).
- R1 fixed: tools/dispatch_manifest.py `_TEST_KEY_RE` takes an optional backtick before the colon too (`test`: form); row `pass-backticked-word` in TEST_ROWS. Spec 5.1's other PASS forms (bare, bulleted, bold, whole-line backticked, `test:`) already had one row each.
- R2 fixed: tools/dispatch_manifest.py `_dod_commands` skips a line only when `_test_line_parse` returns a well-formed parse (`got is not None and not got[2]`); row in test_dod_run_check: `- Test: <canon run>` inside the DoD extent -> 2 `test_canon_x.py whole`.
- R3 fixed: the S-C-2 row in test_dod_run_check now puts the well-formed test line inside the `dod=` value (second line of the DoD section) -> 0.
- R4 fixed: CLAUDE.md R11-f reads "and, for a builder, `test:` (...)" (resolved in the merge hunk, commit d705436c). CLAUDE.md 14222 bytes (main 14136); BOOT BUDGET 109276 / 120000, CLAUDE.md 14222/16700.
- docs/TESTING.md, tools/dispatch_new.py, tools/test_dispatch_new.py: no change needed this round.

### Red-before (byte copy of tools/dispatch_manifest.py, each mutation reverted from it)
```
9cf42a8914437a69                      <- sha256 prefix before
== R1 revert
FAILED tools/test_dispatch_manifest.py::test_test_line_table[pass-backticked-word]
1 failed, 50 passed, 320 deselected in 0.37s
== R2 revert
FAILED tools/test_dispatch_manifest.py::test_dod_run_check[python -m pytest test_a.py -q`\n- Test: `python -m pytest test_canon_x.py -q--builder-cls4-
1 failed, 50 passed, 320 deselected in 0.27s
== skip removed (R3)
FAILED tools/test_dispatch_manifest.py::test_dod_run_check[python -m pytest test_a.py -q`\n`test: test_canon_x.py | expected from: owner--builder-cls3
1 failed, 50 passed, 320 deselected in 0.27s
9cf42a8914437a69                      <- file after restore
9cf42a8914437a69                      <- byte copy
```

### Witness (one run after all code edits, from the worktree root)
```
$ python -m pytest tools/test_dispatch_manifest.py tools/test_dispatch_new.py tools/test_dispatch_gate_md.py -q
500 passed in 4.30s
$ python -B tools/agents_md.py --check
AGENTS.md: up to date (114879 bytes)
$ python -B tools/pointer_lint.py --check
pointer_lint: ok (34 files, 1985 pointers)
pointer_lint exit 0
$ python -B tools/session_context.py | grep 'BOOT BUDGET'
BOOT BUDGET: 109276 bytes / 120000 (9 files) | CLAUDE.md: 14222/16700
```
- Tests: +3 rows / -1 row in tools/test_dispatch_manifest.py (+1 comment line); code +2 / -1 lines.
- Notes: FG7-95's READERS NOTE untouched. Spec 5.1 item 1 still names `test_lines(cut)`, which the code no longer has (critic seam note, for the Lead). Merge-commit hook printed a WARN on a journal event without `feature` (logs/journal/dev1.jsonl line 4255, t-1523) -- not this task's.
