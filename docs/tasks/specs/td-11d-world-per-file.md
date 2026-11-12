# TD-11 spec D — one world per file for the KEPT slow test files (node TD-11c-W; draft, designer t-030, 11.11.2026)

Status: designer draft for Lead acceptance. Forks are in §7; none is closed here. Paths are relative to `ai-packages/qa-factory/` unless
they start with `docs/`, `plans/`, `tools/`, `.github/`. Absolute root of the node paths: `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\`
(written `<T>\` below). Brief: `docs/tasks/specs/td-11-lead-brief.md`; sister spec: `docs/tasks/specs/td-11c-test-split.md` (spec C, accepted).
Spec C's split boundaries, its registry protocol R-A1/R-A2 and its closing commit NC are referred to, never redefined.

## §1 Goal, honest frame, invariants

**Goal.** `docs/TESTING.md:119-120`: a test that needs a driver or a controller builds its world ONCE per file and takes all its checks
from it. Spec C §1 named the gap and opened TD-11c-W (§8 F7); the owner's word 11.11.2026 (spec C l.239): done in this work, not later.

**Honest frame.**
- What a world costs today, read from the builders: `seed()` = `harness.temp_project` + ONE child `stage_done.py` + an in-process
  `Controller.initialize` (`story_run_common.py:192,224-230`); `s0_project()` = temp project + a `git init` child (`story_run_common.py:388-390`);
  `test_window_record.a_story_at_s5` = in-process controller, five stage accepts and gate A (`test_window_record.py:120-138`).
  Estimate, not measured: 0.5-2 s per build on CI Linux.
- What the scenarios spend besides: child processes per check. Child-launch call sites (cmd B, §4) run from 1 to 116 per file, and one
  site can run many times (`test_probe_by_code_alternative.py` has 3 sites, `alt()` l.193-200 is called in loops). TESTING.md:120 names this
  second cost too ("a subprocess per check is a test defect"). **Sharing worlds removes only the first cost.** Estimate, not measured:
  5-25 % of a driver file's CI seconds; near 0 % for the probe family. Phase 0 (§3) measures which; no file is changed on the estimate.
- Nothing else is saved: total canon time falls by the build seconds removed, shards rebalance only after `slow_tests.json` is re-measured.

**Behaviour does not change**: the same checks with the same expected values, in the same order inside each run list. Witness: §2.6.

| AR / FR / P | How this spec touches it | How it is kept (the check goes into the node DoD) |
|---|---|---|
| AR-15 one survivor | one world module, one tree-state hash; precedents `test_grounding_table.py:119-120` (`Story.tree_hash`), `test_probe_by_code.py:416` (`snapshot`), `test_red_window.py:86-108` (`Story.put`: reset to pristine) | the module is the only place a world is cached, reset or hashed; the precedents are not rewired here (report line, §8) |
| AR-14 one writer | world directories; the clock sink; `slow_tests.json` | worlds only by the module; the sink only by the clock hook; `slow_tests.json` only by `selftest.py --slow-tests --from … --update` (integrator) |
| AR-13 one reader | the clock sink | read only by `scenario_clock.py report`; `slow_tests.json` stays read by `selftest.slow_tests()` (`selftest.py:992`) |
| AR-18 one output shape | the isolation guard | a guard failure is a `harness.check(…, False)` line naming the scenario, silent when healthy — the shape of `harness.guard_cwd` (`harness.py:122-134`) |
| AR-20 ratchets | `TEST_TIMEOUTS`, `slow_tests.json` | no ceiling row is added or raised; slow rows change only by the measuring command |
| AR-22 producer/readers | the sink + its reader; the module + its importers' `covers` | each pair lands in one commit (D0; D1 + NC-D) |
| AR-23 empty outcome | a file that runs zero scenarios | builds nothing; the sink holds one `file` row with `scenarios: 0` |
| AR-28 unknown is no pass | a scenario the clock cannot attribute | goes to an `unattributed` bucket with its seconds, never dropped, never 0 |
| AR-29 judgment | checks added (table below) | all judge data; the CLASS of a file (shareable / not) is the Lead's judgment on measured data |
| AR-4 no machine tie | temp dirs, sink path | `tempfile` only; the sink path comes from the environment |
| FR-28 a measurer gets a test | the clock reader | table rows (D0 DoD) |
| FR-31 load-only failures; no timing asserted | seconds | seconds are printed and recorded, never asserted; a green-alone/red-in-file scenario is a test defect (`defect_found`), never a ceiling |
| FR-32, FR-54 | siblings found while adopting | fixed by the same road, or a report line (§8) |
| FR-41, FR-26 | estimates; the measurement | every estimate is labelled; a class is decided only after the Lead read the raw sink rows |
| P29 | a red or raising scenario | it never poisons the next one and never hides the others (§5 E3) |
| P31 one road | every file | the same phase 0, the same classification rule, the same module and runner for every adopting file (§7 F3, F4) |

Checks added (designer rule 1, AR-29). The package census covers `scripts/*.py` outside `scripts/tests/` (`judgment-census.json:3`), so
all rows are outside it; the class is given in census vocabulary for the critic.

| Check | Where | Owner | Census class |
|---|---|---|---|
| isolation guard: tree hash of a `reads` world equal before/after the scenario; after a reset, equal to the pristine hash | `scenario_world.py` | data | shape (outside census) |
| declaration refusals: unknown `mode`, `fresh` without `why`, a build with no root | `scenario_world.py` | data | shape (outside census) |
| argv selection: a name selecting nothing exits non-zero naming the scenarios | `scenario_world.run` | data | xref (outside census) |
| clock reader: sink rows → per-scenario table; refuses a sink whose `file` row is missing | `scenario_clock.py` | data | shape (outside census) |

A reused function in a more consequential role: `harness.cleanup` (`harness.py:398-419`) becomes the reset's delete step. It may err toward
leaving files (its `force` swallows `OSError`, l.409-414) — that direction is UNSAFE for a reset, so the reset re-hashes after restore and
treats any mismatch as "world dead" (E5). Adversarial inputs that must end on the safe side: a read-only file (git objects), a file still
open by a child (Windows), the cwd inside the world (Windows refuses, Linux deletes under the process), a symlink out of the world, an
empty directory created by the scenario.

## §2 The mechanism (one road for every file)

### 2.1 Where

| Module (new, not a test file) | What | Precedent |
|---|---|---|
| `scripts/tests/scenario_world.py` | worlds (2.2), the tree hash (2.4), the one runner (2.5) | `story_step_common.py`, `story_run_common.py` |
| `scripts/tests/scenario_clock.py` + `scripts/tests/clock_sitecustomize/sitecustomize.py` | phase 0 clock (§3) | `driver_golden.py` + `golden_sitecustomize/sitecustomize.py` |

`selftest.py` collects only `test_*.py` (`selftest.py:841`), so neither needs a test-layers row; every adopting file imports
`scenario_world` DIRECTLY (not through `story_run_common`), so its keep row must list `tests/scenario_world.py` in `covers`
(`test_selftest_slow_tests.py:477-489` enforces direct imports) and `scenario_walk.py --witness-for scenario_world.py` picks every adopter
(`scenario_walk.py:913-916`). Invariant: the witness of the module is never narrower than its importers.

### 2.2 API

```python
with scenario_world.world(build, *args, mode="reads"|"mutates"|"fresh", why="", **kwargs) as made:
    ...  # `made` is a deep copy of what build(*args, **kwargs) returned; the scenario never cleans it up
```

| Rule | Text |
|---|---|
| identity | a world is keyed by `(build.__module__, build.__qualname__, repr(args), repr(sorted(kwargs)))`; two builds never share a key |
| lazy | built on the first `world()` entry of its key in this process; never at import (E4) |
| root | `build` returns a tuple whose first item is the world root (a `Path`), or an object with `.root`; anything else is refused (`ValueError` naming the build) |
| pristine | after the build the module copies the root to a sibling pristine copy (prefix `qa-world-`) and records its tree hash |
| process state | the env diff the build made (`os.environ` before/after) is re-applied on EVERY entry; a builder with other process effects declares `build.world_enter = fn(made)` (for `seed`: `harness.use_project(made[0])`, `story_run_common.py:193`), called on every entry |
| `reads` | the shared root itself; on exit the tree hash must equal the pristine hash, else a FAIL line (guard) and a reset |
| `mutates` | the shared root; on exit (normal or exception) it is RESET IN PLACE: `harness.cleanup`-style delete of the root's contents, then a copy of the pristine tree with `shutil.copy` (mtime = now, as a fresh build), then a hash check (§7 F7) |
| `fresh` | a new build every entry, deleted on exit; `why` (non-empty) names the meaning (E10); the module prints nothing, the node report lists every `fresh` with its `why` |
| threads | in a pool thread (`side_by_side`), `mutates` behaves as `fresh` (no reset while another thread may hold the root); `reads` may be shared across threads |
| cwd | before any delete or reset, a cwd inside the root goes back (`harness.cleanup` does it, `harness.py:406-407`) |
| end | every root and pristine copy is deleted at the end of `run` and by `atexit` (E5) |

A builder is shareable only if its whole product lives under its root (plus values derived from the root, like `seed`'s `env`). A builder
that writes beside its root (`alt_project`, `test_probe_by_code_alternative.py:120-125`, cleaned by `cleanup_beside`) is `fresh` unless its
node moves those paths under the root. No process object (Driver, Controller instance, monkeypatch) is ever part of a world: it is built by
the scenario after `world()` (e.g. `project_of` keeps `driver_for` inside the scenario; only `T.seed` is the world).

### 2.3 Declaring reads vs mutates

The scenario declares at its call site; no default (a missing `mode` is a `TypeError`). The rule the node applies: a scenario that starts a
driver, applies a controller operation, writes a file, records an answer or advances a stage under the root is `mutates`; a scenario that
only reads files or calls pure functions over them is `reads`. A wrong `reads` is caught by the guard (2.4) on every run, canon included.

### 2.4 Isolation proof (mechanical)

`scenario_world.tree_state(root)`: `{relative posix path: sha256 of bytes | "dir"}` over the whole tree, symlinks recorded as `link:<target>`
and never followed. It runs on every exit of a `reads` world and after every reset — in the canon, silent when equal (guard_cwd shape). Cost:
a hash of a temp project (tens of small files).

### 2.5 The one runner (§7 F3)

`scenario_world.run(side_by_side, in_process, *, label)` — the body of today's `story_run_common.run_scenarios` (`story_run_common.py:715-752`)
moved here; `run_scenarios` becomes a wrapper that keeps the driver-golden tag (l.729-743). Added:

| Added | Behaviour |
|---|---|
| containment (P29) | a scenario that raises becomes one `check("<name> ran to its end", False, <traceback tail 1500>)` line and the next scenario runs; precedent `test_infra_failure.py:156-161`. A pool thread's exception is reported from the main thread after the pool ends (keeps the FR-31 reason of l.718-720) |
| argv selection | names on argv select the scenarios equal to a name or starting with it, in file order; a name selecting nothing exits 2 naming every scenario (precedent `test_story_run_freshness.py:1338-1343`) |
| order | `QA_SCENARIO_ORDER=reverse` reverses each list (witness only, §2.6); unset = file order |
| clock | nothing: the clock is outside the package path (§3) |

Every adopting file calls `run` (directly or through `run_scenarios`); its old runner (`main` with direct calls, `for` loops, `scenario()`,
module-level loops) is replaced by the same scenarios in the same order and list.

### 2.6 Behaviour witness of an adopting node (attached in the report, not committed)

(a) static: check-call sites before = after (spec C 2.5(a) command); run list names and order before = after. (b) the node's file(s) run on
the base sha and on the head through the clock workflow (§3.2): the multiset of `PASS`/`FAIL` check names is equal, and `FAIL` names equal
the base's (`keep_fail_at_entry` reds stay red). (c) the same at head with `QA_SCENARIO_ORDER=reverse`: per-scenario PASS/FAIL sets equal
(order independence). (d) where spec C's parts exist: each part alone, `python -B <T>\<part>.py`, tally line pasted (`harness.py:179`).
Seconds are reported beside, never judged.

## §3 Phase 0: measurement node D0

### 3.1 What is recorded (sink: JSON lines, one file per test file)

`clock_sitecustomize/sitecustomize.py` is put on `PYTHONPATH` by `scenario_clock.py run`; it acts only in a process whose `sys.argv[0]` is a
`scripts/tests/test_*.py` file (children that inherit `PYTHONPATH` record nothing). It wraps, without changing any return value:

| Event | Fields |
|---|---|
| `file` | test file, start/end monotonic seconds, exit code, Python version, git sha |
| `check` | t, check name, ok, scope = the scripts/tests function names on the stack (outermost first) |
| `child` | t start, seconds, script name of argv (`stage_done.py`, `story_run.py`, `probe_by_code.py` …), scope; via `subprocess.Popen` start and wait |
| `tempdir` | t, prefix, scope (`tempfile.mkdtemp` audit event, `sys.addaudithook`) |

`scenario_clock.py report --sink <dir> [--builders seed,s0_project,…]` derives per file and per scenario (scenario = the outermost scope
name below `main`/`<module>`/the runner): wall seconds, child seconds by script, number of world builds (`tempdir` events), seconds inside
builder scopes, and the `unattributed` remainder. Builder names come from §4 column 3 (data passed on the command line).

### 3.2 Where it runs and how the result is carried

| Item | Value |
|---|---|
| CI | a `workflow_dispatch` workflow `.github/workflows/scenario-clock.yml`, inputs `files`, `ref`, `order` (normal/reverse); python:3.12 like the canon; uploads `ci-out/scenario-clock/` (sinks + each file's full stdout) |
| first run | the 16 files of §4 on `main` |
| read by | `tools/ci_read.py` (host adaptation 6), then `scenario_clock.py report` |
| carried | the report table + run id + sha + the exact command go to `plans/MEASUREMENTS.md` (pt.6b: a number with its carrier) and into §4 column "measured" at Lead acceptance |
| never | a measured number in a test, a threshold in code, a `slow_tests.json` edit by hand (TESTING.md:95) |
| decides | the Lead classifies each file by §7 F4 on the measured rows (judgment, accepted at D0 acceptance) |

## §4 Per file

Commands (Grep tool, per file, count mode, glob over the 16 names; static call sites including definitions, not runtime counts):
A = `\b(seed|s0_project|d2_seed|temp_project|alt_project|project_of|rig|Rig|manual_rig|temp_dir|staged_driver|mark_project)\(`;
B = `\b(run_driver|run_script|s0_run|s0_answer|subprocess\.run|subprocess\.Popen|run_capture)\(`; C = `^def \w+\(\)` (zero-argument
top-level functions: a scenario proxy) or the counted run list where cited. Seconds: `scripts/slow_tests.json` (measured_on 2026-11-11, line
cited). Class is PROVISIONAL (S = shareable reads, R = reset-in-place for mutating scenarios, F = fresh by meaning, X = not world-bound:
children dominate) and is decided only after D0. Gains: estimate, not measured.

| File (C node) | CI s (json line) | World builder today (verified) | A / B | Scenarios | Runner today | Provisional class | Gain (estimate) |
|---|---|---|---|---|---|---|---|
| test_infra_failure.py (N1) | 320.6 (l.50) | `project_of` 140-148 → `T.seed`; direct `T.seed` e.g. 244 | 38 / 14 | 29 (list 1124-1131) | module-level loop 1135-1137 + `scenario()` 156-161, exact-name argv | R | 15-40 s |
| test_story_run_refusals.py (N11) | 308.2 (l.116) | `seed`; `res_fixture` 1351, `CCRig` 2647, `k9_driver` 3197, `git_fixture` 943 | 21 / 8 | C 44 | `run_scenarios([], …)` 3672 | R | 15-40 s |
| test_story_run_s0.py (N12) | 286.3 (l.117) | `s0_project` (`story_run_common.py:383`, "a FRESH project"), `rest_project` 127 | 51 / 116 | 48 (23 side-by-side 3029-3051, 25 in-process 3052-3076) | `run_scenarios` 3028 | F (side-by-side, first S0 run) + S/X (units) | 0-15 s |
| test_no_move_seam.py (N2) | 283.0 (l.58) | `rig` 36-53 → `seed` + `driver_for`; `n2_the_filter` 101 builds none | 45 / 2 | C 68 | `for` loops 1391, 1669, 2212; `__main__` 2220 | R + S | 20-50 s |
| test_story_run_stand_identity.py (N14) | 274.3 (l.122) | `class Rig` 96 | 42 / 1 | C 24 | `run_scenarios([], …)` 1628 | R | 10-40 s |
| test_story_run_s6.py (N13) | 219.4 (l.120) | `seed` (36 sites), `ManualWorld` 281, `manual_rig` 312, `reprobe_rig` 2113, `pin_project` 2050 | 87 / 3 | C 35 | `run_scenarios([], …)` 2512 | R | 20-60 s |
| test_story_run_freshness.py (N3) | 159.0 (l.114) | `freshness_project` 73, `gate_a_story` 309, `staged_driver` 331 | 8 / 4 | 30 (list 1323-1334) | `run_scenarios([], chosen)` 1344, prefix argv 1337-1343 | R (clock values: E1) | 5-15 s |
| test_words_doors.py (N15) | 134.3 (l.131) | `project_env` 434, `story_with` 603, `ctrl_project` 889 | 15 / 14 | C 32 | `main` 1773, direct calls | R / X | 5-15 s |
| test_story_run_loop_b.py (N4) | 119.0 (l.115) | `seed` (29 sites) | 29 / 2 | C 25 | `run_scenarios([], …)` 2037 | R | 15-35 s |
| test_handoff_values.py (N5) | 116.4 (l.47) | `_story` 32 (mkdir only); the form is built by a CHILD `handoff_init.py` (`_form` 38-42) | 40 / 9 | C 54 | `if __name__` block 1609 | X (or R over the built form) | 0-30 s |
| test_controller_rework.py (N6) | 107.0 (l.26) | `designer_story` 365, `story_to_s8` 1143, `two_window_story` 1533 (in-process controller) | 50 / 12 | C 46 | `main` 2111, direct calls | R | 10-30 s |
| test_probe_by_code.py (N7) | 105.8 (l.65) | `project` 258 | 20 / 9 | C 22 | `main` 3102 | X | 0-10 s |
| test_grounding_table.py (N8) | 105.8 (l.43) | `Story.__init__` 66-67 (file writes only; `run` = child `grounding_table.py`, 94-96) | 1 / 1 | no scenario functions: the whole module runs at import, `finish` 929 | module level | X | 0 s |
| test_probe_by_code_languages.py (N9) | 103.7 (l.68) | `lang_project` 230, `ts_profile_project` 1854, `Rn1_8World` 2021 | 5 / 3 | C 11 | `main` 2236 | X | 0-10 s |
| test_probe_by_code_alternative.py (TD-11c-W) | 337.0 (l.66) | `alt_project` 112-162 (in-process, writes beside its root 120-125), `with_stub` 225-235 | 7 / 3 (`alt()` 193-200 called in loops: `unknown()` ×7 l.301-317, `refused()` ×8 l.349-362) | 14 (12 `with_stub` + `k23` + `k29_k30`, 605-611) | `main` 604-615 | X | 0-15 s |
| test_red_window.py (N10) | 85.8 (l.80) | `temp_project` ×8 (139…557) + `TW.a_story_at_s5` (`test_window_record.py:120-138`); `k6` already shares ONE world by `Story.put` 95-108 | 8 / 1 | 11 (`main` 593-605) | `main`, direct calls | R | 5-20 s |

Summary (estimate): 120-400 s of about 3,000 CI seconds of these 16 files. The X files are routed by §7 F1/F2, never silently left.

**MEASURED (D0, CI run 43120089137, 11.11.2026; table and carrier: `plans/MEASUREMENTS.md` §9).** The 16 files cost 1,242 s on CI, of
which 389 s are world builds and 996 s child processes outside builders. Classes decided by the Lead on F4 (a) (12.11.2026, by the
measured rows; the owner may overturn):
- ADOPT (ceiling ≥ 10 s or ≥ 15 %): no_move_seam (77 s), refusals (69 s), stand_identity (42 s), s6 (39 s), infra_failure (38 s),
  freshness (33 s), loop_b (32 s), probe_by_code_alternative (24 s), handoff_values (10.5 s), red_window (5 s, 18 %). Ceiling in all:
  370 s; the real gain is lower (only scenarios that read share).
- NOT ADOPTED, class X (builds under 6 s): s0, probe_by_code, probe_by_code_languages, words_doors, grounding_table, controller_rework.
  Their seconds are child processes; they wait for §7 F2 (the owner).
The provisional classes of the table above that the measurement overturns: controller_rework R -> X; probe_by_code_alternative X -> R
(its 13 builds are 26 s of 26 s); handoff_values X -> R (borderline).

## §5 Edges (each with the invariant it protects)

| # | Edge | Behaviour | Invariant |
|---|---|---|---|
| E1 | a scenario mutates the world (state, stage, answer, files) | `mode="mutates"`: shared root, reset in place on exit from the pristine copy, hash-checked. In a pool thread: `fresh`. A world whose bytes hold a build-time clock value (`seed` writes `checked_at` now, `story_run_common.py:218-219`; controller events carry times) is `R` only when the node's reverse-order witness (2.6 c) is equal; otherwise `fresh` with `why: "clock value in the world"` | no scenario ever sees another scenario's writes, nor a world older in meaning than a fresh build would be |
| E2 | order and argv selection | lazy build makes a scenario run alone build exactly the world it gets in the file; the order inside each list is kept; selection rules 2.5; witness 2.6 (b)(c) | a selected scenario passes or fails alone exactly as in the whole file; a selection of nothing is never a green |
| E3 | a red or raising scenario | its world is reset in `__exit__` even on an exception; the runner turns the raise into one FAIL line and runs the next (2.5); a `reads` guard failure is a FAIL line plus a reset | one failure never poisons the next scenario and never hides the others (P29) |
| E4 | import-time vs lazy | worlds are built on first `world()` entry only; module-level loops (infra 1135-1137) become a `run` call under `if __name__`; `test_grounding_table.py` (module-level script) is X and is not restructured | a file that runs zero scenarios builds nothing; importing a test file runs nothing new |
| E5 | temp cleanup, Windows and Linux, crash mid-file | delete at the end of `run` and by `atexit`, through `harness.cleanup` (read-only files, cwd go-back first). A reset whose re-hash differs (file held open by a child on Windows, etc.) marks the key DEAD: the next entry builds `fresh`, and one note line names the key. A killed process (timeout) leaves `qa-world-*` directories, as today's per-scenario `finally` does | a world that could not be restored is never handed out again; nothing is written inside the package (`harness.py:17-23`) |
| E6 | `side_by_side` vs `in_process`, child processes | a world is a directory of ONE test-file process; its children reach it by path only; no world crosses test files (selftest runs files in parallel, `--jobs 4`); pool threads never hold a root another thread may reset | sharing never changes what runs in parallel, and never couples two test files |
| E7 | temporal: before / after spec C's split of the same file | AFTER (recommended, spec C §1 and F7): the node adopts inside the parts and their `<stem>_common.py`; "one world per file" = per part; witness 2.6(d) runs locally. BEFORE (only by §7 F5): the node adopts the whole file, witness is CI only; spec C later moves the `with scenario_world.world(…)` lines byte-identically, and its witness 2.5(a) counts them unchanged | a split never adds or removes sharing; sharing never changes a split boundary |
| E8 | per-scenario seconds unknown today | `slow_tests.json` holds seconds per FILE (`selftest.py:1042-1043` parses `tests: <file> <s>s` lines); `_test_outcome` keeps only `FAIL` lines of a child (`selftest.py:491-492`); `harness.py` imports no clock (l.6-15). D0 measures (§3); the numbers go to `plans/MEASUREMENTS.md` and §4, read by the Lead | a measured number is never pinned as a test constant (TESTING.md:95) |
| E9 | seconds not in world building (alternative, probe family, grounding, handoff) | D0's child-seconds column decides; such a file is class X: no world change; its residual is a named node DP-<file> (§6) whose road is §7 F2 | a file is changed only where the measurement says the world is the cost; a residual is a node, not a line |
| E10 | a check that needs a FRESH world by meaning (first S0 run, absent files, "no controller") | `mode="fresh", why="<meaning>"`; the node report lists each with its `why` (s0 side-by-side: `s0_project` is "a FRESH project for S0 by code", `story_run_common.py:384`) | a first-run check never runs on a used world |
| E11 | AR-29 | every helper and check this spec adds judges data (shape, key, hash); none judges a scenario's meaning; the file class is the Lead's judgment | code owns data, the Lead owns the class |
| E12 | a build that changes process state (env, hooklib cache, cwd, sys.path) | env diff re-applied on every entry; other effects only through `build.world_enter`; the node lists every effect it found in its builder (grep the builder for `os.environ`, `use_project`, `chdir`, `sys.path`) | on entry, process state equals what a fresh build leaves |
| E13 | a test patches a module attribute the clock also wraps (`test_window_record.py:286` patches `WR.subprocess.run`) | the clock wraps `subprocess.Popen` methods, not `subprocess.run`; a test's patch is applied and restored over it untouched | the clock never changes a test's own stubs |

## §6 Nodes (for a weaker model)

Every node dispatch carries R11-f header lines: `given:` `owns:` `non-goals:` `handoff:` `edges:` `DoD:`. Common lines:

```
given: docs/tasks/specs/td-11d-world-per-file.md (§2, §5, its §4 row); docs/tasks/specs/td-11c-test-split.md §2, §6; plans/builder-rules.md; ai-packages/qa-factory/design/factory-rules.md; docs/TESTING.md; scripts/tests/harness.py; scripts/tests/story_run_common.py
non-goals: no change to what a scenario checks or expects; no quarantined file; no single-copy registry committed (rows go in the report, spec C R-A1); no TEST_TIMEOUTS row; no local run of a whole slow file (parts only); no split boundary moved
handoff: docs/tasks/handoffs/<task>-td11d-<node>.md -- witness verbatim + the registry row block + "Needed from integration"
edges: E1-E13 of §5
```

| Node | owns (absolute) | DoD (verification run) | Order / wave |
|---|---|---|---|
| D0 clock | `<T>\scenario_clock.py`, `<T>\clock_sitecustomize\sitecustomize.py`, `<T>\test_selftest_slow_tests.py` (one table of sink→report rows, FR-28), `C:\QAFactory\forge-repo\.github\workflows\scenario-clock.yml` | `python -B <T>\scenario_walk.py --witness-for <owns>`; `python -B <T>\test_selftest_slow_tests.py`; then one dispatch of the workflow on the 16 files, read by `tools/ci_read.py`, report table pasted | NOW, parallel with spec C wave 1 (no shared file) |
| D1 module | `<T>\scenario_world.py`, `<T>\test_scenario_world.py` (keep row via NC-D; table: reads/guard, mutates/reset, fresh/why, pool thread, raise in scenario, env replay, `world_enter`, zero scenarios, argv no-match, reverse order, dead world) | `python -B <T>\scenario_walk.py --witness-for <owns>`; `python -B <T>\test_scenario_world.py` (under 10 s) | NOW, parallel with D0 |
| D1b wiring | `<T>\story_run_common.py` (`run_scenarios` → `scenario_world.run`; `seed.world_enter`) | witness-for; then the clock workflow on `test_story_run_loop_b.py` base vs head (2.6 b, c) | after D1 and after spec C N1 and N8 merged (they re-point `story_run_common.py:4,248`, spec C §1 FR-37 row) |
| Dn adopt <file> | the file's parts + `<stem>_common.py` (spec C §7 names) — or the whole file under F5 | witness-for <owns>; 2.6 (a)-(d); the `fresh` list with `why`; the found process effects (E12) | per file: after D0 class = S/R, D1b, and that file's spec C node |
| DP-<file> residual | the file (or its parts) | per §7 F2 once answered | does not start before F2 is answered |
| NC-D integrator | `scripts/tests/test-layers.json` (`covers` += `tests/scenario_world.py` for adopters; keep row for `test_scenario_world.py`), `scripts/slow_tests.json` (`--slow-tests --from <ci-out/selftest.txt> --update` after the first canon), `plans/MEASUREMENTS.md` | the batch canon on CI (spec C R-A2) | last, in spec C's closing push or the next one |

Waves (at most 6 writing workers in all, spec C's nodes counted in the same 6; no two parallel nodes share a file):
D wave 0 = D0, D1 (beside spec C wave 1, which then runs with at most 4). D wave 1 = D1b, then Dn for spec C wave-1 files classed S/R
(infra, no_move_seam, freshness, loop_b, controller_rework; handoff_values only if R). D wave 2 = red_window (if R) after N10. D wave 3 =
refusals, s6, stand_identity, words_doors, s0 (F/S part) after spec C wave 3 (which waits for spec A phase 1, spec C F8) — or by F5.

## §7 Forks (each with a recommendation; the builder works by it until answered)

| # | Fork | Options | Recommendation; meanwhile |
|---|---|---|---|
| F1 | scope | (a) worlds only + measurement; child-per-check files get DP nodes (owns + test); (b) also remove children per check here | (a): the non-goal forbids changing what a check reaches; the DP residual is a named node (designer rule 6). Meanwhile (a) |
| F2 | DP road (TESTING.md:120 second half) | (a) one CLI child per behaviour kept, the other checks of that behaviour call the in-process door (precedent `_main_in_process`, `test_probe_by_code.py:1789`); (b) leave the children; (c) batch several checks per child | (a); it changes the road some checks take, so it needs the owner's or Lead's word. Meanwhile DP nodes wait |
| F3 | one runner | (a) every adopter runs through `scenario_world.run` (containment, argv, order everywhere); (b) the context manager only, each file keeps its runner | (a): P31 and E2/E3 for every file; cost: mechanical edits of about 8 `main`s. Meanwhile (a) |
| F4 | when a file adopts | (a) measured build seconds × (builds − 1) ≥ 10 s OR ≥ 15 % of the file's CI seconds; (b) any measurable gain; (c) always | (a): one data rule for all files; below it the diff costs more review than it saves. Meanwhile (a) |
| F5 | order vs spec C | (a) after spec C per file; (b) before, for files whose spec C node cannot start this session (wave 3 waits for spec A phase 1) | (a), with (b) only for wave-3 files blocked at the session's end (the owner's word: done in this work). Meanwhile (a) |
| F6 | test of the module | (a) new `test_scenario_world.py` with a keep row (builder-rules 7d l.59-61: a new script may have a file with a keep row, ≤ 10 s); (b) rows in an unrelated kept file | (a); TESTING.md:117 says no new test file, 7d allows it for a new script: the owner reads the tension. Meanwhile (a). **ANSWERED — the owner, 11.11.2026: (a), the new test file is allowed** |
| F7 | mutating scenarios | (a) reset in place (same path); (b) copy the template to a new path | (a): `seed` worlds hold absolute self-paths (`known_paths`, `story_run_common.py:228`; stub paths, l.235), so a copy at another path would point back at the template. Meanwhile (a) |
| F8 | where the clock lives | (a) `scripts/tests/` beside `driver_golden.py` (ships with the package); (b) `tools/` (forge only) | (a): it measures package tests and needs their paths; harness stays untouched. Meanwhile (a) |
| F9 | containment changes `run_scenarios`' contract ("Nothing is caught here", `story_run_common.py:720-721`) | (a) contain (brief edge 3, P29); (b) keep raising | (a); the FR-31 reason there (a pool thread's FAIL line swallowed) is kept by reporting from the main thread. Meanwhile (a) |

Small choices closed here: module names; `shutil.copy` (mtime now) for the reset; the `qa-world-` prefix; the sink format JSON lines; one
sink file per test file; symlinks hashed by target and never followed; the clock acts only in the test-file process.

## §8 Not verified by this draft

- Every second in §4 "Gain" and §1: estimates from static counts; D0 decides. The per-build cost of `seed` was not measured.
- Dynamic counts: commands A/B/C count call sites, not calls; C is a proxy (it counts helpers and `main` too).
- Whether path-keyed process caches (beyond `hooklib._PROJECT_ROOT_CACHE`, `harness.py:247-253`) can carry state across reset-in-place
  scenarios at the same path; the reverse-order witness (2.6 c) is the detector, not a proof.
- Driver/controller time windows that a world's build-time stamps could cross during a long file (E1): not read in `story_run.py`.
- `test_handoff_values.py` form bytes (whether `handoff_init.py` writes an absolute path): decides R vs X.
- That `tools/ci_read.py` can fetch artifacts of a `workflow_dispatch` run, and whether adding a workflow needs the mechanism gate's axis block.
- `driver_golden.py` traces as an extra witness: not used (a shared world removes a seed child from later scenarios, so traces differ by design).
- Analogs noticed, not in scope: infra's argv selects by exact name and runs nothing silently on an unknown name (`test_infra_failure.py:1135-1137`),
  fixed by the one runner only if F3 (a); three tree-hash helpers exist (§1 AR-15 row).
