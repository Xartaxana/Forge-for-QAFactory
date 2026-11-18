# t-1453 main-red fix

DONE 1: tools/wave.py `import os` removed (only other `os` hit is a docstring `os.replace`). Staged, not committed.
DONE 2: language_sites C1 at selftest.py `_named_by_form` (regex `scripts/tests/test_*.py`): a forge path rule on the package's own test-census names, not a project language branch. Door 3: row `...selftest.py|_named_by_form|regex|.py` kind own-code, mechanism OWN, with reason, in tools/language-sites-baseline.json. Staged, not committed. selftest.py NOT changed (no package commit).
No further red found in the two tools.

Witness:
- `python tools/lint_ratchet.py --check` -> lint ratchet: 76 findings, 76 in the baseline, 0 new, 0 stale (pyflakes 3.2.0)
- `python -B tools/language_sites.py --check` -> language_sites: ok (323 rows, 285 files scanned)
- `python -B tools/language_sites.py --check --base origin/main` -> language_sites: ok (323 rows, 285 files scanned)
- test_selftest_shard.py: not required (selftest.py unchanged). For information, it errors at collection: `ERROR ...test_selftest_shard.py::tests_dir_with` (1 error in 0.61s), independent of this change; a helper named test-like or a fixture issue - unexamined.

Needed beyond manifest: tools/language_sites.py doors text only.
