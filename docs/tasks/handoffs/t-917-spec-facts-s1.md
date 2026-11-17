# t-917 (F19) -- stream S1, fix round attempt 2 (critic report t-923: B1, B2, F1-F9)

DoD: `python -m pytest tools/test_owns_readers.py tools/test_dispatch_new.py tools/test_gitcmd.py -q -p no:cacheprovider`

(Handoff file of attempt 1 had this same name; rewritten. Changes are STAGED on top of 8c9e53af, no commit.)

## Output

```
........................................................................ [ 45%]
........................................................................ [ 90%]
................                                                         [100%]
160 passed in 45.53s
```

## finding -> what changed -> test row

| finding | what changed | test row |
|---|---|---|
| B1 | `Report.owned_unsearched` counts skipped owned paths (outside, `..`, control char, PATH_CAP overflow, dir over cap); `_header()`: no path subject searched -> `readers: unknown -- no owned path was searched (<k> unsearched below); <L> lines below -- base ...`; some skipped -> `; unsearched: <k> paths` after `lines below` | test_owns_readers_table: outside-repo, outside-dotdot, dir-wide, empty-list, control-char-path-only (unknown); mixed-searched-and-unsearched, control-char-path-mixed, path-cap-beyond (partial); path-cap-at, dir-at-cap (no mark) |
| B2 | `.github/workflows/*` added to the `code` row of owns_readers.json; KNOWN MISS 5 names docs/, plans/, root *.md, nested fixture JSON, tools md/yaml fixtures, gateway/ | workflow-reader |
| F1 | `_clean()`; any non-clean decision on headers+block (raise string, refusal, degraded cut) goes to the replacement line, decided once more; only its failure refuses | test_checker_failure_on_the_block_replaces_it_and_never_hides_the_dispatch[raise, degraded] |
| F2 | `_ids_refusal` also runs on the final text (one extra call) | test_ids_are_read_back_on_the_final_text_too |
| F3 | listed layered test readers print `(test, quarantine unknown)`; more part `N test (quarantine unknown)`; the mark only for `cls == "test"` | quarantine-layers-absent (changed), quarantine-layers-absent-listed, quarantine-unknown-code-reader-no-mark |
| F4 | `report()` split into _read_inputs / _owned_files / _layer_facts / _name_items / _search / _name_presence; `render()` split into _subject_lines / _header; longest owns_readers function 43 lines | all table rows (behaviour unchanged) |
| F5 | public `gitcmd.first_line(raw, limit=None)`, `_first_line = first_line` alias; owns_readers `_first_line` is a 1-line wrapper (limit 160) of it; dispatch_new uses `gitcmd.first_line` in both places | test_gitcmd.py::test_first_line_rows (10 variant rows) |
| F6 | docstring: "node C6 of the spec (§6 L9), opened by the Lead" | none (text) |
| F7 | `assert dm.designer_threshold(cut_a) == dm.designer_threshold(cut_b)` | test_block_leaves_the_manifest_reads_unchanged |
| F8 | rows AT caps: test-cap-at (25), data-cap-at (12), dir-at-cap (40), names-cap-at (20); PATH_CAP at/beyond; control char in path and name; regex-meta names; Cyrillic name; `..` path; mixed row | rows named in B1 plus test-cap-at, data-cap-at, names-cap-at, control-char-name, regex-meta-names, cyrillic-name |
| F9 | merged slots sorted by (quarantined last, test before code, tier, path) | two-owned-test-before-code |

## Header lines of the four measured cases (worktree, base origin/main 3a96d579 at run time)

1. `--paths C:/QAFactory/forge-repo/tools/gitcmd.py`:
`readers: unknown -- no owned path was searched (1 unsearched below); 1 lines below -- base origin/main 3a96d579 (literal mention; known misses: tools/owns_readers.py docstring)`
2. `--paths tools/`:
`readers: unknown -- no owned path was searched (1 unsearched below); 1 lines below -- base origin/main 3a96d579 (literal mention; known misses: tools/owns_readers.py docstring)`
3. `--paths ../outside.py tools/gitcmd.py`:
`readers: 32 outside owns, 2 lines below; unsearched: 1 paths -- base origin/main 3a96d579 (literal mention; known misses: tools/owns_readers.py docstring)`
4. `--paths tools/mechanism_gate.py --all`: header `readers: 25 outside owns, 25 lines below -- base origin/main 3a96d579 (...)`, line 12: `- outside: .github/workflows/forge-check.yml (code) names tools/mechanism_gate.py`

## Deviations

- `git fetch -q` was run once by me while measuring (the tool never fetches; origin/main moved to 3a96d579 versus 237ead44 in the report).
- Under B1 the owned-skip counter counts a PATH_CAP overflow in full (owned and given, because which were dropped is not tracked).
- `dispatch_new.main` is 63 lines (was ~58); report/render targets met.
- Replacement-line wording kept as "the manifest check refused the block (...)" (an existing test pins it) also for a raise or degraded cut.

## Questions

none

## Needed beyond the manifest

none (read tools/dispatch_manifest.py PATH_CAP only)
