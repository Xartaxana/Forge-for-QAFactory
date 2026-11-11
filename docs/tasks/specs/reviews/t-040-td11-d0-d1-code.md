# t-040 — critic gate, TD-11 spec D nodes D1 (t-039, scenario_world) and D0 (t-038, scenario clock)

Reviewed against: spec `docs/tasks/specs/td-11d-world-per-file.md` (§1, §2, §3, §5, §6, §7), `docs/tasks/specs/td-11-lead-brief.md`
«Правки после критика на план» item 7, the dispatch DoD, `docs/tasks/critic-diff-brief.md`. Files reviewed in the two worktrees, uncommitted.

## Verdicts

- **D1 (scenario_world): ACCEPT WITH FIXES — 2 BLOCKER, 4 MAJOR, 6 MINOR.** The blockers are small fixes in one fix round, no redesign:
  in two reproduced cases a scenario gets a world that is not its own.
- **D0 (clock): ACCEPT WITH FIXES — 0 BLOCKER, 4 MAJOR, 6 MINOR.** The clock is safe on the measured path (it changes no test
  output there). But as built, the measurement cannot decide F4: the `builds` count and `builder_s` are biased, and after D1b
  every scenario is filed under `_contained`. Fix these before the 16-file dispatch is read as data.

Accepting either node is the Lead's decision (rule 6). This file is input to it.

## Mechanical layer: control re-runs (my own, verbatim tails)

- D1 worktree: `python -B .../test_scenario_world.py` → `=== test_scenario_world: 25/25 ok ===`, exit=0.
- D0 worktree: `python -B .../test_selftest_slow_tests.py` → 9 `clock report (...)` PASS lines, `=== test_selftest_slow_tests: 110/110 ok ===`,
  exit=0, real 4.9 s.
- I did not re-run D0's live test_driver_layers run. I checked it against the code for consistency (see M-D0-1: 43 "builds" = 43 mkdtemp calls).

Probes (stdin Python, temp dirs only; the handoff gate refused a scratch file, so the source was passed inline through Bash):

```
P1 keys equal: True                                   # functools.partial(tiny,"S3") vs partial(tiny,"S5")
P1 S5 scenario got: S3 alpha-S3                       # the S5 scenario got the S3 world
P2 lambda keys equal: True                            # two lambdas in one function
P3 exit raised: Error [(...\qa-world-...\tree\sub', ...\qa-probe-...\sub', "[WinError 183] ...   # restore raised
P3 dead: False
P3 next entry same root: True sub is a file: True     # the next scenario got the unrestored world
P4 ... outside accepted; exists before cleanup: True  # a root under %USERPROFILE%, not under tempdir
P4 exists after cleanup_all: False                    # deleted by the module
P5 islink(junction): False tree_state: {'link': 'dir', 'link/out.txt': '65c7...'}   # junction followed
P5 target survives cleanup: True
```

Clock chain probe (D0 worktree, Python 3.12.10):

```
PYTHONPATH="<clock_sitecustomize>;<golden_sitecustomize>" python -B -c "..."
Error in sitecustomize; set PYTHONVERBOSE for traceback:
RecursionError: maximum recursion depth exceeded
(the same with the opposite order)
```

---

## D1 — scenario_world.py / test_scenario_world.py

### BLOCKER

**B-D1-1. Key collision: two different builds share one world.** `scenario_world.py:67-70` `world_key` takes the key from
`build.__module__` + `__qualname__` + world() args.
- Failing input (P1): `world(functools.partial(tiny, "S3"), mode="reads")` and then `world(functools.partial(tiny, "S5"), mode="reads")`.
  Both keys are `("functools", "partial", "()", "[]")`, so the S5 scenario gets the S3 world.
- The same happens for two lambdas in one function (P2), and for closures defined in a loop (same qualname, different captured values).
- This silently breaks the spec's "two builds never share a key". It is also a SPEC defect: §2.2's identity row prescribes the qualname key.
- Fix: put the build object itself into the key, `(build, repr(args), repr(sorted(kwargs.items())))`. Functions and partials are hashable
  by identity. Keep the qualname only in `_label`. If a build is unhashable, refuse it with a ValueError naming it.
- Add one table row: two partials → two builds.

**B-D1-2. A reset that raises leaves the world alive and dirty, and the next scenario gets it.** `scenario_world.py:142-151` `_restore`
marks the world dead only on a hash mismatch. Any exception from `shutil.copytree` (or from `tree_state`) escapes before `w.dead = True`.
- Failing scenario (P3): a mutates scenario replaces the directory `sub` with a file that is still open (on Windows, a child holding it).
  `harness.cleanup` swallows the delete failure. `copytree` raises `shutil.Error` (WinError 183). `dead` stays False, and the next entry
  gets the same root with `sub` still a file.
- The same holds on Linux for a directory the scenario made read-only.
- This breaks the E5 invariant "a world that could not be restored is never handed out again". The exception also replaces the
  scenario's own exception in `_open`'s `finally`.
- Fix: in `_restore`, wrap delete + copy + rehash in `try/except Exception`. On any exception set `w.dead = True` and print the same
  note line with the exception's text. Never re-raise from the reset.
- `_guard` → `_restore` is covered by the same fix.
- Add one row: monkeypatch `shutil.copytree` to raise inside the module, then expect dead and a rebuild.

### MAJOR

**M-D1-1. Cleanup deletes any root a builder returns, even outside the temp directory.** `_root_of` (`:115-122`) accepts any existing
directory. Then `_discard`/`_restore`/`cleanup_all` and `_fresh_world` delete it with `harness.cleanup`.
- P4: a build that returns `%USERPROFILE%\qa-critic-probe-outside` is accepted, and `cleanup_all` deletes it.
- A builder that returns a project path or `PLUGIN_ROOT` by mistake would delete the package. The module docstring (l.28) and the DoD
  ("tempfile only") promise otherwise.
- Fix: in `_root_of`, refuse (ValueError naming the build) a root whose `realpath` is not under `realpath(tempfile.gettempdir())`
  (`os.path.commonpath`). Also refuse a root that is itself a symlink or junction.
- Add one row: root outside tempdir → ValueError.

**M-D1-2. `run` reads `sys.argv[1:]` unconditionally, so D1b would change behaviour.** `:311-318`.
- Failing scenario after D1b: `test_story_run_s6_w1_frozen.py --fixtures <dir>` (its negative control, l.282-289). It calls
  `run_scenarios` with stdout redirected to a StringIO. `run` would refuse `'--fixtures'` with exit 2, and the refusal text is swallowed
  into the redirected buffer, so the file exits 2 and shows no reason.
- `test_story_run_s5_n1_frozen.py --capture` returns before `run_scenarios`, so it is unaffected. Other callers pass no argv.
- Fix: `run(side_by_side, in_process, *, label, names=None)`. With `names=None`, use the `sys.argv[1:]` items that do not start with `-`.
  An adopter with its own flags passes `names` explicitly.

**M-D1-3. `run` cannot be swapped into `run_scenarios` without losing names.** The driver-golden tag needs a per-scenario wrapper
(`story_run_common.py:736-743`), and `run` uses `scenario.__name__` for argv selection, the `ran to its end` line and the guard's
scenario name. A plain `tagged()` wrapper is named `run`, so every name would become "run".
- Fix (D1, so D1b is a pure swap): add `wrap=None` to `run`, applied inside the thread as `_contained(scenario, wrap)`, with the name
  taken from the unwrapped scenario.
- Otherwise the rest of `run` matches `run_scenarios` (pool of 4, the pool-then-serial order, `guard_cwd` after the pool and after each
  in-process scenario). Containment deliberately changes F9 (all pool futures run and are reported). That change is the spec's, not drift.

**M-D1-4. An unknown `QA_SCENARIO_ORDER` silently means file order.** `select` (`:281`). A typo such as `revers` makes witness 2.6(c)
compare file order with file order and pass vacuously.
- I agree with the Lead: refuse it. `run` exits 2 naming the allowed values {unset, `""`, `normal`, `reverse`}.
- `normal` must be allowed, because the workflow's choice input can carry it (today the workflow exports nothing for normal, so it is compatible either way).
- Add one row.

### MINOR

- **m-D1-1. A junction is followed by `tree_state`** (`:87-103`, P5). Windows junctions are not `islink`. `tree_state` hashes files
  outside the world, so a scenario that changes them gives a false guard FAIL, and the reset copies the target's content as real files.
  `rmtree` does not follow the junction (target survives).
  - Fix: treat `os.path.isjunction` (3.12+; fall back to `st_reparse_tag` / skip on older versions) like a link.
  - The same fix answers open point (5): the symlink row can use `_winapi.CreateJunction`, which needs no privilege, so it checks
    something on Windows instead of printing PASS over nothing (`test_scenario_world.py:335-339`).
- **m-D1-2. `tree_state` uses `os.walk` without `onerror`.** A directory it cannot list is silently treated as empty, so the guard
  misses real differences inside it (AR-28: an unknown is read as known-equal). Fix: `onerror` raises, or the directory is recorded as `unreadable`.
- **m-D1-3. The tree state ignores file mode and mtime.** A reads scenario that runs `chmod`/`utime` passes the guard. Mutates is safe
  because the reset rebuilds.
  - Spec point (F7, closed by the designer): the reset gives every file mtime=now in `copytree` order, so the build's relative mtimes
    (artifact older than receipt) are not reproduced.
  - Before freshness-style files adopt R, either copy with `copy2` and re-stamp `utime` from the pristine state, or rely explicitly on the
    2.6(c) witness. A note for the Dn nodes; no D1 code change is required.
- **m-D1-4. Pool-thread reads guard.** A guard that fires in thread A resets the root while thread B may still be reading it, and A's
  FAIL line can name A for B's write. The file still goes red. The spec's thread row allows reads to be shared but is silent on the reset.
  Fix: in a pool thread, record the FAIL line and defer the reset until the pool ends (mark the world for reset), or make reads fresh in
  the pool when a guard has fired once.
- **m-D1-5. Containment catches `Exception` only.** A scenario that calls `sys.exit(0)` (an in-process script `main`) ends the file
  green with the rest skipped. The old runner did the same. Fix: also catch `SystemExit` in `_contained` as one FAIL line.
- **m-D1-6. Leaks.** In `_make`, an exception after the build (`_root_of`, copytree) leaks the build root and the container. In
  `_fresh_world`, a `_root_of` refusal leaks the build. In `_hand_out`, a raise (deepcopy/world_enter/world_caches) happens before the
  `try`, so no restore runs. These are leaks only (temp dirs), not cross-contamination. Fix: track and clean them in `finally`.

### Answers to the dispatch questions for D1

- **(1) Can a scenario get a world another scenario wrote to?**
  - YES via B-D1-1 (key collision) and B-D1-2 (reset failure). These are the two blockers.
  - Thread races on the registry: NO. `_shared_world` is under `_LOCK`.
  - The deep copy: NO. `Path` is immutable and `made` is deep-copied on every hand-out.
  - The reads guard on exception: it runs in `finally`, so it is not skipped. It is skipped only when `_hand_out` raises (m-D1-6), and
    then the scenario never ran.
- **Tree state.** A file replaced by a directory IS caught (hash vs "dir"). Mode and mtime are missed (m-D1-3). Unreadable directories
  are missed (m-D1-2).
- **Cleanup outside the temp roots.** A symlink out of the world: not followed by rmtree. A junction: not deleted, but hashed (m-D1-1).
  The cwd goes back first (`harness.cleanup` l.406). A hostile or mistaken root IS deleted (M-D1-1).
- **(2) Does containment hide a failure?** NO, unless the adopter never calls `finish`. The FAIL line enters `harness.RESULTS` and
  `finish` exits 1; the `raising` row verifies both the pool path and the main path. Pool fidelity: see M-D1-2 and M-D1-3.
- **(3) The builder's open points.**
  1. The kwargs key: the `sorted(kwargs.items())` fix is right. The spec text sorted only the names, a spec defect. The key still needs
     B-D1-1.
  2. `run` should NOT call `finish`: callers have checks or summaries after it (s6_w1_frozen l.292-294). Keep `label` for the refusal.
  3. Dead-world rebuild as a shared world: acceptable. It is a new build at a new temp path, and E5 only forbids handing out the dead one.
  4. `QA_SCENARIO_ORDER`: refuse unknown values (M-D1-4).
  5. The symlink row: use a junction on Windows plus the m-D1-1 fix.
- **(6) TESTING.md.** One table of rows, no timing asserted, 0.4 s, no pin on script source. The test reads private `_WORLDS` and
  `_DOWNGRADES` through `state_of`; tolerable for a module's own table. The symlink row prints PASS while checking nothing on Windows (m-D1-1).

---

## D0 — scenario_clock.py / clock_sitecustomize/sitecustomize.py / workflow / test table

### MAJOR

**M-D0-1. `builds` counts every `mkdtemp`, not world builds.** `scenario_clock.py:127-128` counts every `tempdir` event regardless of
`--builders`.
- In the live run, `bad_fixtures` shows 43 builds for 43 checks: one scratch temp dir per check, not 43 worlds.
- The spec §3.1 says "number of world builds (`tempdir` events)", so this is partly a SPEC defect.
- F4's rule `build_s × (builds − 1)` would over-state the gain for any file that makes scratch dirs or calls code that makes temp dirs.
- Fix: `builds` = tempdir events whose scope intersects `--builders` (no builders given → print `-`). Print the raw count as a separate
  `tempdirs` column. Add one table row: a tempdir outside builder scope is not a build.

**M-D0-2. The interval rule biases `builder_s` in both directions, so it is not sound enough alone to decide F4 near the threshold.**
`derive` `:106-120` gives the gap before each event's end to that event.
- Over-count: the first event inside a builder absorbs everything since the previous event. For the first scenario that is interpreter
  start plus every import, which is why the fixture's `scn_a` builder_s is 2.0 including 0.5 s of "start". For later scenarios it is the
  previous scenario's trailing work and teardown.
- Under-count: the builder's own work after its last event (for `seed`, the in-process `Controller.initialize` after the `stage_done`
  child) goes to the next event, which is outside the builder.
- Under pool threads the per-scenario wall is arbitrary. The builder says so; it is acceptable for X-class files, not for S/R decisions
  on pool files.
- Fix: give the builder scope real enter and exit events.
  - `run` accepts `--builders` and passes them to the hook through an env variable.
  - The hook's `_HarnessFinder` is widened to every module loaded from `tests_dir`. After `exec_module` it wraps the functions with
    those names (`story_run_common.seed`, `s0_project`, ...), writing `builder` rows with t and seconds.
  - Builders defined in the test file itself can be wrapped through `threading.setprofile`/`sys.setprofile`, filtered by name on `call`/`return`.
  - Then `builder_s` is measured, not inferred.
- Cheaper alternative: print `builder_s` as a range [events strictly inside the scope, + the next gap] and let the Lead decide only when
  both ends fall on the same side of F4.

**M-D0-3. Cross-node: after D1b every scenario is filed under `_contained`.**
- D1's `run` calls each scenario through `scenario_world._contained`. `in_tests` keeps every frame of `scripts/tests/*.py` except
  `harness.py` and `scenario_clock.py`.
- `DEFAULT_RUNNERS` (`scenario_clock.py:30`) has `run` but not `_contained`. So the outermost non-runner name is `_contained` for every
  scenario, in the pool too.
- The 2.6(b)/(c) witnesses of every Dn node run head through this clock, so head tables would show one scenario.
- Fix (one road): exclude `scenario_world.py` frames in `in_tests`, as for `harness.py`. Or add `_contained` to `DEFAULT_RUNNERS` and add
  a table row with a scope `["<module>", "main", "run", "_contained", "scn_a"]`.

**M-D0-4. The chain to a shadowed sitecustomize recurses with golden_sitecustomize.** `sitecustomize.py:238-246`, and the same loop at
`golden_sitecustomize/sitecustomize.py:40-43`.
- Each loop skips only its own directory, so clock → golden → clock → ... until RecursionError.
- Reproduced in BOTH PYTHONPATH orders. stderr gets `Error in sitecustomize ... RecursionError` for every process, including non-test
  children, so this changes output, against the DoD.
- `_install` would also run again on each re-entry. Its `_SEEN_VAR` guard reads `os.environ`, which `os.putenv` does not update, so each
  re-entry doubles the rows and writes a second `file` row, and the sink is refused.
- Reachable when `driver_golden.py` (which prepends to an existing PYTHONPATH, `driver_golden.py:320`) runs inside a clocked
  environment or the reverse. It is not on today's measured path: `test_driver_golden.py:328-331` replaces PYTHONPATH.
- Fix once for both copies (DUPLICATION, below): a sentinel `if "sitecustomize_shadowed" in sys.modules: skip`, plus skip every
  directory that is a known hook directory (a marker file or a name list). Best is one helper file loaded by path from both. Also set an
  in-process sentinel (a module global or `sys` attribute) for the install guard, not only `putenv`.

### MINOR

- **m-D0-1. The child guard does not reach the usual children.** `os.putenv(_SEEN_VAR)` does not reach children launched with
  `env=dict(os.environ)`, which is `harness.run_script`'s form (`harness.py:187`). So a test that launches another `scripts/tests/test_*.py`
  as a child records into the sink. Two `file` rows in one stem → the whole sink is refused; a new stem → an extra table.
  - Not seen among the measured files.
  - Fix: `cmd_run` passes `QA_SCENARIO_CLOCK_PARENT=<its pid>`, and the hook acts only when `os.getppid()` equals it.
- **m-D0-2. Exit code in the `file` row.** It comes only from `harness.finish` or the excepthook. A file that calls `sys.exit(n)`
  directly records 0.
  - `cmd_run:202` prints "(the clock recorded exit N: trust this one)". "this one" is ambiguous, and the process exit code is the one to trust.
  - Fix the wording ("trust the process exit code"), and have `report` mark a row whose exit is unknown.
- **m-D0-3. A second sink reader (AR-13).** `cmd_run` reads the sink through `read_sink_one` (`:199,208`), without validation, and swallows
  errors. Fix: use `read_sink` and pick the entry.
- **m-D0-4. The run environment differs from the canon.** `cmd_run` adds `PYTHONIOENCODING=utf-8` (`:181`) for the test and all its
  children. Harmless for the measured driver files on Linux, but it can change encoding tests (`test_console_encoding.py`). Fix: drop it
  (harness already reconfigures its own streams) or name it in the report header.
- **m-D0-5. Dead helper and a wrong prefix.** `sink_rows` (`test_selftest_slow_tests.py:505`) is dead: defined, never called (grep: one
  hit, the definition). The `tempdir` prefix `name[:-8]` (`sitecustomize.py:200`) is wrong when a suffix is used; the field is unused.
- **m-D0-6. FR-28 covers only the reader; the hook is untested by any table.**
  - The "never changes output" property and the scope extraction rest on one live run.
  - Recommendation: one row that runs a tiny fixture `scripts/tests/test_*.py`-shaped file through `scenario_clock run` (one child, about
    1 s). It checks byte-equal stdout with and without the clock, one row per event kind, and the scope of a check called through a
    pool thread. That is a stage junction (TESTING.md).
  - Also: the hook is inert when the test starts through `run_py_entry.py` (argv0 is the entry, and `sys.argv` changes later) or loads
    harness by path. Then there are no check rows while the `file` row still exists, so 0 checks reads as data (AR-28). `cmd_run` never
    uses the entry, so it is fine for the workflow; say so in the docstring.

### Answers to the dispatch questions for D0

- **(4) Can the hook change a test's behaviour?**
  - Audit hook: it reacts only to `tempfile.mkdtemp`, inside try, and the compare cannot raise. There is no re-entrancy into the lock.
  - Popen: the hook patches class attributes, so tests that replace `subprocess.Popen` or `subprocess.run` are untouched, and subclasses
    go through the wrappers. `wait` re-raises `TimeoutExpired` before recording, and the row is recorded at the next successful wait.
  - Stack walk: per check, child and mkdtemp, with filename results cached. Plus one flushed write per check. This is measurement overhead
    (it inflates check-heavy files slightly), not a behaviour change.
  - Threads: `scope()` reads the calling thread's stack. Writes are locked.
  - `sys.argv[0]` on Windows: abspath + `\`→`/` work. The parts compare is case-sensitive: harmless, since `cmd_run` passes a resolved path.
  - `run_py_entry.py`: inert (m-D0-6).
  - Output changes found: the golden chain recursion (M-D0-4) and the env difference (m-D0-4). Otherwise none.
- **Is the interval rule sound enough to decide?** Not as built (M-D0-1, M-D0-2, M-D0-3). Child seconds per script ARE exact (start to
  wait). So the "children dominate → X" call is reliable. The S/R gain estimate is not.
- **(5) Workflow.**
  - Triggers: only `workflow_dispatch`. Permissions: `contents: read`. No secrets.
  - Inputs reach the shell only through `env:`; `ref` is used in `run-name` and `checkout.ref` (no shell).
  - `$FILES` is unquoted, so it is word-split and globbed. Glob characters are harmless: the names pass the `case`, slash and `-f` checks or
    are refused.
  - Suggestions: `set -f`, and `persist-credentials: false` on checkout. The test code runs with the read token in `.git/config`.
  - The builder asks whether to add a `builders` input and a report step: yes, cheap. A `builders` input passed through `env:` to a
    `scenario_clock.py report --sink ... > ci-out/scenario-clock/report.txt` step with `if: always()` and `continue-on-error`. The raw
    sink stays for the Lead's own re-read (FR-26). If M-D0-2's fix is taken, the same input also goes to `run`.
- **(6) The import by path in `test_selftest_slow_tests.py`.** It is acceptable only if NC-D's `covers` row and the plain import land in
  the same commit as D0. AR-22: a producer and its readers in one commit, which spec §1 already names for D0. Otherwise it is a smell that
  hides the dependency from the covers check; queue it as a named line rather than leaving it. The table otherwise meets TESTING.md: one
  table, fixture seconds only, no timing, no source pin.

---

## DUPLICATION AND CONSISTENCY

- **The chain-to-shadowed-sitecustomize loop is now in two files** (clock :238-246, golden :40-43), and both carry the recursion defect
  (M-D0-4). Fix it once: a shared loader helper used by both, or at least the same sentinel in both in this round.
- **`tree_state` is the 4th tree-hash helper.** Confirmed present: `test_grounding_table.py:119` `tree_hash`, `test_probe_by_code.py:416`
  `snapshot`, `test_red_window.py:95` `Story.put`. The spec leaves them un-rewired. AR-15 is kept only if a queue line exists. Proposed
  node (owner: the Lead): rewire the three onto `scenario_world.tree_state` when their files adopt (Dn) or in NC-D.
- **Two runners until D1b** (`run_scenarios` and `scenario_world.run`): accepted as transitional. D1b is a named node.
  M-D1-2 and M-D1-3 make it a pure swap.
- **Cross-node consistency:** the clock's runner list vs D1's `_contained` (M-D0-3).
- None found otherwise: grepped `_contained|DEFAULT_RUNNERS|sink_rows` over both worktrees, `def (tree_hash|snapshot|put)` over the main
  tests, and `driver_golden|golden_sitecustomize|PYTHONPATH` over `test_*.py`.

## CODE QUALITY

- D1 code is compact and readable. Problems: B-D1-1, B-D1-2, the leaks (m-D1-6), and `os.walk` swallowing errors (m-D1-2).
- D0: dead `sink_rows`, a second reader `read_sink_one`, the wrong prefix slice, an ambiguous note (m-D0-2, m-D0-3, m-D0-5).
- No non-ASCII in the new files. Grepped `[^\x00-\x7F]` over the six names; the only hit, used as a positive control, is the pre-existing
  em dash in `test_selftest_slow_tests.py:180`, present in all worktrees.

## ONE ACTION, ONE ROAD (item 12, P31)

- The clock's runner list and D1's runner disagree (M-D0-3): that is two roads to "which scenario is this". Fixed in this round.
- `run`'s argv handling would fork files with flags (M-D1-2). Fixed in this round by the `names` parameter, the same for every file.
- No exclusion of a language, project or case was found.

## Architecture (question 10)

| AR | Verdict |
|---|---|
| AR-13 | Clock sink: broken in a small way by `read_sink_one` (m-D0-3). |
| AR-14 | Kept: worlds are written only by the module, the sink only by the hook (`cmd_run` deletes a stale file, noted). |
| AR-15 | Kept on condition of the tree-hash queue line. |
| AR-18 | Kept: the guard is a `harness.check` line, silent when healthy. |
| AR-22 | Kept on condition of the NC-D row in the same commit. |
| AR-23 | Kept: zero scenarios build nothing and give a `file` row. |
| AR-28 | Mostly kept (unattributed bucket). Gaps: an unreadable directory read as equal (m-D1-2); an inert hook gives 0 checks that read as data (m-D0-6). |
| AR-29 | Kept: every check judges data (hash, key, shape); the file class stays the Lead's judgment on measured rows. |

## JUDGMENT (question 11)

Every check judges data. Neither node has a code check that decides a role's or the Lead's judgment. The census is outside `scripts/tests` (spec §1).

## FR

| FR | Verdict |
|---|---|
| FR-28 | Reader: yes. Hook: no table (m-D0-6). |
| FR-30 | Clean. |
| FR-31 | No timing asserted. Pool FAIL lines are reported from the main thread. |
| FR-43 | Sink line-buffered + flush; `_say` flush; tee flush. Kept. |

## SPEC defects found (not code)

1. §2.2 identity row: the qualname key collides for partials, lambdas and closures; `sorted(kwargs)` drops values (B-D1-1, open point 1).
2. §3.1 "world builds (`tempdir` events)" (M-D0-1).
3. §3.1 "scenario = outermost scope below main/<module>/the runner" does not name the D1 runner frame `_contained` (M-D0-3).
4. §2.2 threads row: reads are shared across threads, but the reset on a guard failure is not specified (m-D1-4).
5. F7 "mtime = now" loses the build's relative mtimes (m-D1-3).

## Not checked

- I did not re-run D0's live test_driver_layers run (checked by consistency only). The workflow has not run on GitHub; `ci_read.py`
  fetching its artifact is unverified (spec §8).
- Linux behaviour of `harness.cleanup`/`copytree` on the reset failure (reasoned, not run). The symlink path on a privileged machine.
- Pool-thread behaviour of the clock's scope under real `run_scenarios` (no pool file run under the clock).
- The scenario_walk `--witness-for` outputs in the reports (not re-run).
- Whether any of the 16 target files launches a `scripts/tests/test_*.py` child (m-D0-1 reachability not established).
- `tools/test_workflows.py` behaviour with a fifth workflow (the builder's claim, not verified).

```json
{
  "verdict": "blocker",
  "blockers": [
    "D1 B-D1-1: world_key by module+qualname collides for functools.partial / lambdas / loop closures; reproduced: partial(tiny,'S5') got the S3 world. Fix: key by the build object itself plus repr(args) and repr(sorted(kwargs.items())).",
    "D1 B-D1-2: _restore raising (shutil.Error from copytree) leaves w.dead False; reproduced: the next scenario got the unrestored root. Fix: try/except in _restore marking dead with the note line, never re-raise."
  ],
  "fixes": [
    "D1 M-D1-1: refuse a world root outside tempfile.gettempdir() or a symlink/junction root (reproduced deletion of a dir under USERPROFILE).",
    "D1 M-D1-2: run(..., names=None); default = sys.argv[1:] items not starting with '-' (s6_w1_frozen --fixtures would exit 2 after D1b).",
    "D1 M-D1-3: run(..., wrap=None) applied in-thread so D1b keeps the driver-golden tag and scenario names.",
    "D1 M-D1-4: refuse an unknown QA_SCENARIO_ORDER (allow unset, empty, normal, reverse).",
    "D1 minors: junction as link in tree_state and a junction-based symlink row on Windows; os.walk onerror; SystemExit containment; leak cleanup in _make/_fresh_world/_hand_out; deferred guard reset in pool threads.",
    "D0 M-D0-1: builds = tempdir events inside --builders scope; raw count as a separate tempdirs column.",
    "D0 M-D0-2: measured builder enter/exit rows (wrap named builders), or print builder_s as a range.",
    "D0 M-D0-3: exclude scenario_world.py frames from scope or add _contained to DEFAULT_RUNNERS, with a table row.",
    "D0 M-D0-4: recursion guard in the sitecustomize chain loop of both clock and golden (sys.modules sentinel plus skipping known hook dirs); in-process install sentinel.",
    "D0 minors: parent-pid guard for children; exit-code note wording; use read_sink in cmd_run; drop PYTHONIOENCODING; delete sink_rows; a hook junction row; workflow set -f, persist-credentials false, optional builders input and report step.",
    "Integration: NC-D covers row plus a plain import of scenario_clock in the same commit as D0; queue a node to rewire the three tree-hash helpers onto tree_state (owner: Lead)."
  ],
  "class_completeness": "Key identity: partials, lambdas and closures walked (B-D1-1). Reset failure: copytree and tree_state exceptions, and the guard path through the same _restore (B-D1-2). Delete surface: outside root, symlink, junction, cwd (M-D1-1, m-D1-1). Sitecustomize chain: both copies carry the recursion (M-D0-4). Tree-hash helpers: three precedents need a queued node. Runner names: clock vs D1 (M-D0-3).",
  "trail": {
    "read": [
      "agent-a8a063cc3d591733b: scenario_world.py, test_scenario_world.py, reports/t-039-td11-D1.md, harness.py:85-234,395-420",
      "agent-a9d22c180c0b5086d: scenario_clock.py, clock_sitecustomize/sitecustomize.py, golden_sitecustomize/sitecustomize.py (grep), driver_golden.py:320, .github/workflows/scenario-clock.yml, git diff test_selftest_slow_tests.py, reports/t-038-td11-D0.md",
      "main: story_run_common.py:705-753, test_story_run_s6_w1_frozen.py:270-294, run_py_entry.py (grep), test_driver_golden.py PYTHONPATH lines",
      "docs/tasks/specs/td-11d-world-per-file.md, td-11-lead-brief.md:195-235"
    ],
    "reruns": [
      "test_scenario_world.py: 25/25 ok, exit 0",
      "test_selftest_slow_tests.py: 110/110 ok, exit 0, 4.9 s",
      "scenario_world probes P1-P5 (partial and lambda key collision, failed reset reused, outside root deleted, junction followed)",
      "sitecustomize chain probe: RecursionError in both PYTHONPATH orders"
    ]
  }
}
```
