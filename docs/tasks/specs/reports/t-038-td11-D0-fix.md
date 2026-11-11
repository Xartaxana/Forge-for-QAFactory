# t-038 attempt 2 - TD-11 D0 fix round (scenario clock)

Worktree: `C:\QAFactory\forge-repo\.claude\worktrees\agent-a9d22c180c0b5086d` (uncommitted, nothing committed or pushed).
Files changed: `scripts/tests/scenario_clock.py`, `scripts/tests/clock_sitecustomize/sitecustomize.py`,
`scripts/tests/test_selftest_slow_tests.py`, `.github/workflows/scenario-clock.yml` (all under `ai-packages/qa-factory/` except the workflow).

## Per finding

- M-D0-1 (builds counted every mkdtemp): FIXED. `builds` = `build` rows only (scenario_clock.py `derive`, `build` branch); `tempdir` rows go to
  their own `tempdirs` column. Live: bad_fixtures shows tempdirs 43, builds 1. Table row: "a tempdir outside any build is a tempdir, never a build".
- M-D0-2 (builder_s inferred from gaps): FIXED, direct. The hook (`clock_sitecustomize/sitecustomize.py`, `install_builders`) uses
  `sys.monitoring` (Python 3.12+): PY_START/PY_RETURN/PY_UNWIND callbacks, names from env `QA_SCENARIO_CLOCK_BUILDERS` (set by
  `run --builders`). Writes one `build` row per outermost call (t, seconds, name, scope, nested). Nested calls are flagged `nested` and
  are not counted nor summed (no double count). Child seconds whose scope holds a builder name are reported as `in_build_s`
  and are not added to the file totals again (header: "children outside builders ... children inside builders ... not added again").
  COST: one callback per distinct code object (it returns DISABLE, so that location never fires again); a function named as builder
  costs two callbacks and one scope walk per call; PY_UNWIND (cannot be disabled) costs one dict lookup per unwinding frame. Measured on
  test_driver_layers.py: plain 14.3 s, clock without builders 14.8 s, clock with builder 15.2 s. A first version keyed the cache by the
  code object and took 832 s on that file (hashing a code object walks its body on every unwind); fixed by keying on `id(code)`
  (the entry keeps the code alive). Limitation: a generator builder is not timed; Python < 3.12 writes a `clock_error` and the
  report prints it. Table rows: "a sink with build events ..." and "a nested build ...".
- M-D0-3 (`_contained`): FIXED by data: `DEFAULT_RUNNERS` gains `_contained`. Row: scope `[<module>, main, run, _contained, scn_a]` -> `scn_a`.
- M-D0-4 (chain recursion): FIXED on the clock's side alone, both orders. sitecustomize.py bottom: the chain loop runs only
  `if "sitecustomize_shadowed" not in sys.modules` (someone, e.g. the golden, already loads us from its loop and loads the next
  itself), and the install is guarded by an in-process sentinel `sys._qa_scenario_clock_installed` (not by `os.putenv`).
  Golden file NOT changed (non-goal). Rows: chain both orders (`-c print`), and a recorded run with the golden dir also on PYTHONPATH.
- m-D0-1 (child guard): FIXED. `run` sets `QA_SCENARIO_CLOCK_PARENT=<its pid>`; the hook acts only when `os.getppid()` equals it
  (works with `env=dict(os.environ)` children). Caveat: a Windows venv launcher stub would make the test's parent the stub and the
  hook inert (loud: no `file` row, the report refuses); not met here (system Python 3.12.10).
- m-D0-2 (exit wording): FIXED. Wording "trust the process exit code"; the `file` row carries `exit_seen`; the report marks a row
  with `exit_seen` false ("exit code not seen by the clock: trust the process exit code").
- m-D0-3 (second sink reader): FIXED. `cmd_run` uses `read_sink` and picks the entry by stem; `read_sink_one` deleted.
- m-D0-4 (`PYTHONIOENCODING`): FIXED, dropped from `cmd_run`.
- m-D0-5: FIXED. `sink_rows` deleted; the tempdir row now carries `name` (the directory's basename, unsliced) instead of the wrong `prefix`.
- m-D0-6: FIXED. New rows run a tiny `scripts/tests/test_*.py`-shaped fixture through `scenario_clock.run`: byte-equal stdout and exit code
  vs the plain run; one row per event kind (check x2 one from a pool thread with scope `["pool_check"]`, child, tempdir, build);
  `file` row exit 0 and seen. The docstring of the hook now says it is inert under `run_py_entry.py` or a path-loaded harness.
- Workflow remarks: FIXED. `set -euf`, `persist-credentials: false`, input `builders` (via `env: BUILDERS`, never interpolated into `run:`),
  passed to `run --builders`; final step "print the per-scenario report of the sinks" (`if: always()`, `continue-on-error: true`,
  `scenario_clock.py report ... | tee $OUT/report.txt`), raw sinks still uploaded. Still workflow_dispatch only, `contents: read`, no secrets.
  NOT run on GitHub (cannot be run here); `tools/test_workflows.py` not run (outside the DoD).
- Edge 7: FIXED. The docstring of `clock_cases` names the integrator's `covers` row (node NC-D) that lets the by-path load become a plain import
  (a docstring sentence, not a one-line `#` comment; say if a `#` line is wanted).
- Edge 3: with no `--builders`, builds, builder_s and in_build_s print `not measured` (header and cells); a builders-named file with no
  build row gets a CLOCK ERROR-style note ("builders were named but the sink holds no build row for them").
- Spec defects: none new; the review's list stands (spec 3.1 "tempdir events = builds" is superseded by edge 2).

## Decided by me

- Sorting/attribution: `build` rows join the wall-gap ordering by their END (t + seconds); only builder_s comes from them directly. Nested
  and non-named build rows are dropped before ordering.
- `tempdir` row field renamed `prefix` -> `name` (REQUIRED updated; the only reader is `scenario_clock.py`).
- A report header line now carries builder_s / children outside builders / rest, where `rest` = file wall - builder_s - children outside builders; under pool
  threads it can be wrong (concurrency), stated nowhere in code beyond the old docstring caveat.

## Finding lines (not fixed, not mine)

- `golden_sitecustomize/sitecustomize.py:40-43`: same chain loop without a `sitecustomize_shadowed` guard; it works with the clock now only because
  the clock stops. A golden + any other hook that chains back would still recurse. Fix: same `not in sys.modules` guard there.
- `tree_state`-style duplication, `run` etc. belong to D1 (not this node).

## Verification (verbatim)

`python -B <wt>\ai-packages\qa-factory\scripts\tests\test_selftest_slow_tests.py | Select-Object -Last 1` (exit 0):
```
=== test_selftest_slow_tests: 124/124 ok ===
```
(110 former + 14 new: 4 report rows with their count lines changed in place, +2 build/tempdir/nested/no-builder/_contained rows incl.
"printed table says so", +2 hook rows, +3 chain rows.)

Live proof, `scenario_clock.py run --sink <temp> --builders bad_fixtures test_driver_layers.py`, then `report --builders bad_fixtures`:
```
=== test_driver_layers: 54/54 ok ===
--- test_driver_layers.py: exit 0
== test_driver_layers.py  exit 0  wall 15.72s  python 3.12.10  sha 81e33d746e1e  scenarios: 2  checks 54  children 0  tempdirs 43
   builds 1  builder_s 0.12  children outside builders 0.00s  (children inside builders 0.00s are part of builder_s, not added again)  rest 15.59s
   scenario                                       wall_s checks fail children  child_s   in_build_s tempdirs       builds    builder_s  child seconds by script
   real_map                                        15.59     11    0        0     0.00         0.00        0            0         0.00  -
   bad_fixtures                                     0.12     43    0        0     0.00         0.00       43            1         0.12  -
```
Same sink, report WITHOUT `--builders`:
```
== test_driver_layers.py  exit 0  wall 15.72s  python 3.12.10  sha 81e33d746e1e  scenario_clock ... tempdirs 43
   builds not measured  builder_s not measured  children 0.00s
   real_map                                        15.59     11    0        0     0.00 not measured        0 not measured not measured  -
   bad_fixtures                                     0.12     43    0        0     0.00 not measured       43 not measured not measured  -
```
Two-sitecustomize proof. (a) golden dir on PYTHONPATH, `run` prepends the clock dir = clock FIRST then golden:
```
=== test_driver_layers: 54/54 ok ===
--- test_driver_layers.py: exit 0
== test_driver_layers.py  exit 0  wall 20.31s  python 3.12.10  sha 81e33d746e1e  scenarios: 2  checks 54  children 0  tempdirs 43
   builds 1  builder_s 0.16  children outside builders 0.00s ...
```
(b) golden FIRST then clock (PYTHONPATH=golden;clock set by hand with the sink, parent pid = the shell's `$PID` and builders in env, since `run` always prepends):
```
=== test_driver_layers: 54/54 ok ===
== test_driver_layers.py  exit 0  wall 31.00s  python 3.12.10  sha unknown  scenarios: 2  checks 54  children 0  tempdirs 43
   builds 1  builder_s 0.98  children outside builders 0.00s ...
```
No RecursionError on stderr in either; tally 54/54 in both. (The table also covers both orders with `-c`.) Wall times differ between runs: machine load, not asserted.

Negative control NOT run for the chain rows (no old-code copy kept); the recursion itself was reproduced by the review.

## Workflow file
Full text as in the file `.github/workflows/scenario-clock.yml` of the worktree (91 lines; the changes are the `builders` input, `BUILDERS` env, `set -euf`,
`--builders "$BUILDERS"`, the report step with `if: always()` and `continue-on-error: true`, and `persist-credentials: false`).

## Needed beyond the manifest
`sys.monitoring` docs behaviour was measured by a scratch script (scratchpad, not in the repo); the review brief only.
