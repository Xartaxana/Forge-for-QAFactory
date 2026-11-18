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
