# t-039 attempt 2 — D1 fix round (scenario_world)

Files: `ai-packages/qa-factory/scripts/tests/scenario_world.py`, `test_scenario_world.py` (worktree agent-a8a063cc3d591733b, uncommitted).

## Per finding
- B-D1-1 fixed: `world_key` = `(build, repr(args), repr(sorted(kwargs.items())))`; unhashable build -> ValueError naming it. Qualname only in `_label`. Row "two builds never share a world" (partials, two lambdas from one function, same lambda twice = one world, partial vs plain function, unhashable).
- B-D1-2 fixed: `_restore` wraps delete+copy+rehash in `try/except Exception`; any exception or mismatch -> `dead=True` + one `note:` line with the text, never re-raised (so the scenario's own exception survives). `_guard` goes through the same `_restore`. Row "a reset that raises" (copytree patched to raise; KeyError of the scenario still propagates; world dead; next entry = fresh build, old root gone).
- M-D1-1 fixed: `_root_of` refuses (ValueError naming build and root) a root whose realpath is not strictly under `realpath(gettempdir())` (the temp dir itself too), and a root that is a symlink/junction. A refused root is never deleted. Row "root outside temp" (reads/mutates/fresh; `_temp_root` is a module function the row swaps, so nothing is written outside temp; root survives; module holds nothing new) and row "link root is refused".
- M-D1-2 fixed: names = argv tokens not starting with `-`. Row "argv flags are not names". Limitation: the VALUE token of a flag (`--fixtures <dir>`) does not start with `-`, so it counts as a name and, selecting nothing, exits 2. Edge 4 as written implies this; the review's `names=` parameter was not added (not in the edges). D1b must handle `s6_w1_frozen --fixtures <dir>` (e.g. by `=` form or by an explicit names parameter - a Lead decision).
- M-D1-3 fixed: `run(..., wrap=None)`; `_contained(scenario, wrap)` applies it inside the thread; name stays the scenario's. Row "wrap is applied" (pool and main; guard FAIL line names `scenario_writer`, not the wrapper; no wrap = unchanged).
- M-D1-4 fixed: unset/`""`/`normal` = file order, `reverse`, anything else -> exit 2 naming accepted values. Row "unknown order refused, normal accepted" (`revers`, `REVERSE`, ` reverse` refused before anything runs).
- Edge 4 refusal: `_refuse` prints the text to stderr AND stdout (my decision: the review's problem was a redirected stdout; both streams carry it). The no-match row checks both.
- m-D1-1 fixed: `_is_link` (islink, `os.path.isjunction` on 3.12+, reparse-point attribute fallback) used by `tree_state`; the symlink row now makes a symlink or, failing that, a `_winapi.CreateJunction` junction (it ran for real here: no skip note printed). Not changed: `copytree(symlinks=True)` in the pristine copy follows a junction (it is not a symlink for DirEntry), so a world containing a junction will mismatch on reset and go dead (safe direction, rebuild).
- m-D1-2 fixed: `os.walk(onerror=raise)`; `_guard` treats a tree_state exception as a FAIL line with the exception text and resets.
- m-D1-3 not fixed (review: no D1 code change; note for the Dn nodes: mtime/mode are not in the tree state and the reset restamps mtime=now).
- m-D1-4 fixed: in a pool thread the guard records its FAIL line and sets `reset_pending`; `run` resets those worlds after the pool ends (`_reset_pending`). No table row (not asked; the existing pool row covers shared reads).
- m-D1-5 fixed: `_contained` catches `(Exception, SystemExit)`; row "a sys.exit in a scenario is contained".
- m-D1-6 fixed in part: `_make` cleans root and container on any failure after the root was accepted; `_hand_out` moved inside the `try` so the restore/guard runs when it raises. Not fixed on purpose: a `_root_of` refusal in `_make`/`_fresh_world` leaves the build's root alone, because a refused root may be outside temp and the module must never delete it (edge 3).

## Exit code (edge 7)
Containment adds a `harness.check(..., False)` line to `harness.RESULTS`; the same for a guard FAIL. `harness.finish` (harness.py:176-180) does `sys.exit(1 if bad else 0)`, so a file that ends with `harness.finish(label)` exits 1. `run` does not call `finish` (callers keep checks after it). A file that does NOT end with `harness.finish` and has no other exit code stays exit 0: the module cannot turn it red; the FAIL line is printed only. Such a file must end with `finish` (every file of the family does today).

## Decided by me
- stderr+stdout duplicate for refusals; the junction/symlink fallback; the temp-dir itself refused as a root; `""` accepted as order (the review's allowed set); `_temp_root()` helper as the seam for the outside-root row.

## Beyond the manifest
Read `harness.py` finish/check (lines 89-180).

## DoD output
`python -B .../test_scenario_world.py` (exit=0), all lines PASS; closing lines:
```
PASS a sys.exit in a scenario is contained
PASS reverse order reverses each list
PASS a raising scenario is contained and the next runs
PASS cleanup at the end leaves no world directory
PASS every root a builder made is gone at the end

=== test_scenario_world: 33/33 ok ===
exit=0
```
Full list (33 rows = the former 24 table rows + final leftover check, plus 8 new named rows: two builds never share a world, reset that raises, root outside temp, link root, argv flags, wrap, order, sys.exit): printed verbatim in the run; the first attempt of this run had one FAIL (my own over-strict "held paths empty" assertion in the outside-root row), fixed by comparing held paths before/after.
