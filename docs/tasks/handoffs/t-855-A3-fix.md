# t-855 A3 fix round: report

Commit bbb9acdb on offload/a3-fix, pushed fast-forward a98f2792..bbb9acdb to origin offload/a3. Owns touched: tools/test_volume.py, tools/test_test_volume.py only.

## Done
- Fix 1: `classify(path, has_tests=staged_blob_has_tests)`. Under `ai-packages/`: segment rule only (tests/test/fixtures), no basename. Elsewhere: `test_*.py` is a test iff predicate true (default: `git show :<path>` has a line `^\s*(def test_|class Test)`); predicate False/raises/git failure/deleted file -> product. `decide()`/`sum_numstat()` take the predicate (pure by injection). Other basenames (`*_test.py`, `conftest.py`, `*_testkit.py`) stay test-by-basename outside `ai-packages/` (spec silent; unchanged behaviour, not blob-checked).
- Fix 5: WARN_TEXT -> `docs/TESTING.md «Бюджет / Объём»`; test_decide now asserts it.
- New rows: pkg_script_test_star, tool_named_test_star, tools_real_test, blob_unreadable, deleted_file_no_blob, pkg_tests_segment (predicate `_never` raises if called). Existing rows use an always-True predicate (the default would git-read, absent in unit tests).

## Witness
`( cd <wt> && python -m pytest tools/test_test_volume.py -q )`:
```
...........................                                              [100%]
27 passed in 0.39s
```
Fix 2, a98f2792's numstat (16 .githooks/commit-msg.proposed, 70 tools/test_test_volume.py, 142 tools/test_volume.py) through fixed `decide` with blob predicate reading a98f2792 blobs:
```
(False, (70, 142), '')
```
(no WARN; test 70 vs product 142, matching the A3 report).

## Own diff: DEVIATION from expectation
Staged numstat of the fix commit: `37 4 tools/test_test_volume.py`, `31 11 tools/test_volume.py`, i.e. test +37 vs product +31. Fixed tool run in the worktree on the staged index printed:
```
TEST VOLUME (WARN, the commit goes on): +37 test lines vs +31 product lines in this commit; name the reason in a line "tests-over: <reason>" of the message and in your report (docs/TESTING.md «Бюджет / Объём»).
exit=0
```
The critic expected product >= test; it is not (six required table rows plus predicates). Reason named, as the tool asks: the commit message carries `tests-over: six new table rows required by the critic verdict (fix 1) outweigh a small product delta`; rerun with that message file: silent, exit 0. Test vs product lines of this diff: +37 / +31 (net adds; 4 and 11 deleted).

## Siblings / notes
- Same basename assumption elsewhere: none seen in my reads (the classifier is the only path rule). `*_test.py`/`conftest.py` basename rule outside `ai-packages/` has the same class weakness (a non-test `x_test.py` in tools/); not fixed, spec-silent.
- Needed beyond the manifest: none.
