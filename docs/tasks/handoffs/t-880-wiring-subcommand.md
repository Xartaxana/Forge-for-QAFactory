# t-880 report

Done. wiring_check.py `_HOOK_COMMAND_RE` now ends with `(?: [a-z][a-z0-9-]*)?$` (group 2 unchanged); comment block extended.
Tests: new parameterised `test_harness_hooks_subcommand_word_form` (2 legal rows, missing-file and existing-file) -- no legal-forms table existed, so one new function; 5 illegal rows added to the adversarial test (`--flag`, `a b`, `Pre`, `x;y`, `../x`). Trailing-space row NOT added: the caller does `command.strip()` first, so it is legal today as well (same for the flag-less form). `python3 tools/my_hook.py --flag` test still green (unparsed).

## DoD output
`python -B -m pytest tools/test_wiring_check.py -q -p no:cacheprovider`
112 passed in 47.55s

## Live check
`python -B tools/wiring_check.py 2>&1 | tail -5`
WIRING: OK

Questions: none. Needed beyond the manifest: none.
