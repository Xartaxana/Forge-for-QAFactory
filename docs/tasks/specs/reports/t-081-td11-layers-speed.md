# t-081 -- test_driver_layers.py made fast again

Owned: `ai-packages/qa-factory/scripts/tests/test_driver_layers.py`, this report. Nothing else touched
(`git status --porcelain`: ` M ai-packages/qa-factory/scripts/tests/test_driver_layers.py` plus this new file).

## Profile BEFORE (cProfile, 345 s under the profiler, 77 s plain)

Top by cumulative time:

```
 345.0  main -> real_maps
 336.2  analyse  (245 calls; ONE of them is the real family)
 321.3  _literal_mentions   13 862 calls   <- 93 % of the run
 195.9  ast.iter_child_nodes (295 M calls, from the recursive walk() inside _literal_mentions + ast.walk for docstrings)
  10.6  _imports_of          1 120 calls
   9.8  ast.parse            1 751 calls (compile 8.3)
   8.3  facade_importer_problems (5 calls)
   7.7  l11_problems         205 calls
   1.0  scans / Scan.__init__ / read_modules / all bad fixtures together (242 analysis_of calls = 1.05 s)
```

Counts asked for:
- `ast.parse`: 1 751 calls in all (797 from `analyse`, 560 from `_parse_script`, 394 from `read_modules`). On the real
  files: each of the 774 files of `scripts/tests/` once (L8), each of the 278 `scripts/*.py` once or twice
  (`facade_importer_problems` and `l11_problems`; the 17 family files also in `read_modules`). The bad fixtures parse tiny stubs only.
- map `json.load`: 1 (real map, `json.loads` in `real_maps`). `json.loads(json.dumps(...))` of the SMALL base map in
  `fixture()`: 488 (2 per fixture, 0.007 s total). `copy.deepcopy`: 0. Temp trees written: 246 (one `harness.temp_dir` per
  fixture, each with the facade and 0-3 stub files; `rmtree` total 0.12 s). No tree of 17 files is ever copied.
- Spec guess check: the expected wastes (real sources re-parsed per fixture, map deep-copied, 17-file temp trees, gizmo run against
  real sources) are NOT where the time goes: the fixtures (both headers) cost about 1 s of 345. Confirmed by the profile
  before touching, so I left them alone. The whole cost is ONE check, L8.

Root cause: L8 (source readers) walks every test file of the rig (774 files, 28 MB of source) ONCE PER FAMILY FILE NAME
(17 names): `_literal_mentions(tree, fname)` redid a docstring `ast.walk` plus a recursive walk of the whole tree per needle,
17 x 774 = 13 862 full walks (about 4 M AST nodes each batch of 774). Not quadratic in the family strictly, but
families x files; the generalisation to family maps multiplied the needles (1 name before, 17 now).
Second cost: `ast.parse` of 1 000+ big files with the cycle collector running (it re-scans the millions of live nodes).

## What changed (one file)

1. `_literal_mentions(tree, needle)` split into `_string_table(tree)` (ONE walk: every non-docstring string constant with
   its enclosing def, in the same walk order) and `_literal_mentions(table, needle)` (filter by needle, same result list, same order).
2. `_mention_table(text, needles)`: parses a test file, checks with one flat walk whether any string constant holds
   any needle (a regex alternation of the escaped names; a tree with none has no mention to report, docstring or not),
   builds the table only for the files that hit, caches the table per (text, needles). Trees are dropped at once (not
   cached: 45 MB of source would be about a GB of AST).
3. `_script_imports(path)` replaces `_parse_script`: imports of a script derived once per source text, cached
   by (path, text), tree dropped. `facade_importer_problems` and `l11_problems` read it (they previously parsed every script
   each and walked it for imports). The error message of an unparseable script is unchanged.
4. `_parse(text, filename)`: `ast.parse` with the cycle collector paused (restored to its previous state in `finally`).
   Used by `read_modules`, the L8 readers check, `_mention_table`, `_script_imports`.
5. `import gc` added. No map, harness, fixture, check, bad fixture, limit or timeout touched. Shared trees: none exist now (nothing
   cached holds a tree), so no fixture can mutate one; a fixture that changes a file has a different text, hence its own entry.

## Profile AFTER (25.7 s under the profiler, 11.6-12.5 s plain)

Top: `analyse` 17.0 (real family), `_mention_table` 13.7 (781 calls; the one flat `ast.walk` per test file, 6.6 M nodes
in all), `_script_imports` 8.2 (560 calls, 278 real scripts parsed once each, plus fixture stubs), `facade_importer_problems` 8.1.
What remains is the floor of single-threaded work: parsing 774 test files (about 3 s) and 278 scripts (about 3 s) and one walk over
each. Further reduction would need parallel workers or a text prefilter that is not exact for implicitly concatenated
string literals; I did neither (see questions).

## Verbatim DoD output

Wall time, three runs, final file (`date +%s.%N` around `python -B <file>`), was 77 s before:

```
run 1 12.485351800918579
run 2 11.65475845336914
run 3 11.588337182998657
=== test_driver_layers: 283/283 ok ===
```

Before/after output compared (before = `git HEAD` file, after = changed file, nothing stripped):

```
grep -c "^PASS\|^FAIL" before.txt after1.txt   -> 283 and 283
diff <(grep -E "^(PASS|FAIL)" before.txt | sort) <(... after1.txt | sort)  -> SORTED-CHECK-DIFF-EMPTY (283 lines each, 0 FAIL)
diff before.txt after1.txt   (the WHOLE output, informational lines included)  -> FULL-DIFF-EMPTY
```

Mutation probes, on a byte copy of `ai-packages/qa-factory/scripts/` in a temp dir outside the repo (script
`probes.py` in the scratchpad, mutations restored byte for byte with an assert after every run), changed test file:

```
--- probe: an equal-rank import: driver_stage_s5 imports driver_stage_s6
FAIL driver-layers.json L12 holds on the real family (1 problem(s)) --
=== test_driver_layers: 282/283 ok ===
--- probe: a ninth exceptions row (map copy)
FAIL driver-layers.json L5 holds on the real family (2 problem(s)) --
FAIL driver-layers.json: the pin equals the exceptions list, both directions (1 problem(s)) --
=== test_driver_layers: 281/283 ok ===
--- probe: a name row removed: ROLE_TOOLS
FAIL driver-layers.json L1 holds on the real family (1 problem(s)) --
=== test_driver_layers: 282/283 ok ===
--- probe: control: all restored byte for byte
=== test_driver_layers: 283/283 ok ===
```

(A first try of the ninth-row probe appended a COPY of an existing row and did not turn red: a duplicate key collapses in
the dict the check builds. That is the check's behaviour, not mine, and was not compared against the old file; the probe above uses a distinct row.)

pyflakes: `python -m pyflakes <file>` printed nothing, exit 0; control on a file with `import os` printed
`ctl.py:1:1: 'os' imported but unused`.

## Questions / for the coordinator

1. 11.6 s on this machine; the canon ran 3x slower than here (223 s vs 72 s), so expect roughly 35-40 s on CI, far under 300 s. To go
   lower, a process pool for the two bulk loops (parse + derive per test file / script) is possible and would give about 3-4 s on 8
   cores; it adds spawn cost and CPU oversubscription risk if the runner already runs files in parallel, so I did not add it. Decision yours.
2. The probe copy needed a short temp path (the repository's fixtures hit the Windows path-length limit under the scratchpad).

## Analogs noticed (not touched)

- `scripts/tests/` contains 28 MB of test source and `scripts/*.py` 17 MB: any other test that parses all of them per needle or
  per fixture has the same shape; `grep -n "glob(\"\*.py\")"` over `scripts/tests/test_*layers*`/census tests would find them. Not walked.
- `_function_reads` still does an `ast.walk` over the whole tree per source_readers row (about 30 rows, readers files only): cheap now, same shape.

Needed beyond the manifest: nothing beyond harness.py (`PLUGIN_ROOT`, `temp_dir`); the `--witness-for` listing was not used.
