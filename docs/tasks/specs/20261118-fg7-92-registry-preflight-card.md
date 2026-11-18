# FG7-92 -- registry preflight by changed files (designer draft, t-1451)

Pile row: `plans/piles/forge/batch-7-vhodyashchie-4.md` FG7-92 (and what FG7-93 reads). Status: DRAFT; the forks in §8
are the Lead's. Every timing below is either a measurement with its carrier or labelled `estimate` with the command
the Lead runs (the designer has no shell).

## 1. Goal, scope, AR / variety

Owner's word 18.11 (row FG7-92): registry misses (a new check unit with no census row, a new family name with no
driver-layers row, a new reader-shaped JSON function, a test file with no keep row, a new pyflakes finding) reach main
because builders' narrow DoDs never run the registry checks. The fix is code, takes seconds, and NEVER stops a merge
(row FG7-94: branches merge, main may go red, one fixer repairs it).

What is built: `tools/registry_preflight.py` (new) holding THE one rule table of the factory (changed path ->
narrow registry check), a `check` door that runs one or more checks narrowly on a tree, a `run` door that reads a
diff, selects rows and runs them in child processes with a timeout, and a reader API for `dispatch_new.py` (FG7-93).
`wave.py merge` calls it and prints its lines; nothing it says changes wave's exit code.

- AR-n: none touched -- the node writes no file under `ai-packages/qa-factory/`; it only imports package test modules
  and `selftest.py` in a child process and calls their existing functions by name (docs/TESTING.md, «Что запускать»:
  "импорт модуля и вызов функции по имени").
- `variety: none -- a forge-side merge/dispatch tool; no language, project or case axis reaches it`.
- Owner and class of the check this node adds (AR-29 vocabulary, stated for the critic although no package check is
  added): owner = data (code: every row is a registry the code already enforces in the canon); census class = xref
  (registry cross-reference); role = ADVICE, never a gate (see §6 error direction).

## 2. The rule table (code: `registry_preflight.RULES`, one tuple, table order = print order)

A row = `(id, path signs, narrow call, what it catches)`. Signs are repo-relative POSIX globs over the changed paths
(fork F2 recommends path signs only); `scripts/` below means `ai-packages/qa-factory/scripts/`.

| id | path signs (any match selects the row) | narrow call (in a child process, `--root <tree>`) | catches |
|---|---|---|---|
| `census` | `scripts/*.py` (top level, not `tests/`); `scripts/tests/fixtures/judgment-census.json`; `ai-packages/qa-factory/references/stages.json`; `ai-packages/qa-factory/agents/*.md` added/deleted/renamed only | `test_judgment_census.analyse(harness.PLUGIN_ROOT, test_judgment_census.load_census())` -> red when any of `problems["C1".."C5"]` is non-empty | a check unit with no row, a stale row, a raised ceiling (C1-C5) |
| `driver-layers` | `scripts/*.py`; `scripts/tests/fixtures/*-layers.json` (fork F4: or family files only) | `test_driver_layers.real_maps()` then `harness.finish(...)`; NOT `bad_fixtures` (the checker's self-test, canon's job) | a family name with no map row, L1-L12 on the real maps |
| `read-json` | `scripts/*.py` | `test_read_json.census(<tree>/ai-packages/qa-factory/scripts)` + `census_verdict(found, KEPT)` -> red on new or stale or an unparsed file | a reader-shaped JSON function outside `KEPT`, a stale `KEPT` row |
| `test-layers` | `scripts/tests/test-layers.json`; `scripts/slow_tests.json`; `scripts/tests/test_*.py` added/deleted/renamed | `selftest.test_layers()` (raises `TestLayersError`), `selftest.slow_tests()` (raises `SlowTestsError`), `selftest._listing_ok(layers, <added test files present in the tree>, once=True)` | malformed data, a keep row naming no file, an unlisted new test file, a broken `named_by` (fork F3: not `test_selftest_slow_tests.py`) |
| `lint` | `*.py` under `lint_ratchet.ROOTS` (read from the module, never copied: today `ai-packages/qa-factory/scripts`, `tools`), any status incl. deleted | `python -B <tree>/tools/lint_ratchet.py --check --repo <tree> --path <rel>...` (NEW flag, fork F5) | a new pyflakes finding, a file that does not parse, a stale baseline row of a named (incl. deleted) file, a hand-input match in a named package test file |

Timings. Whole-file durations are MEASURED: `ai-packages/qa-factory/scripts/slow_tests.json` (`measured_on`
2026-11-17, `source` selftest.txt, CI `--jobs 4`): `test_judgment_census.py` 96.9 s, `test_driver_layers.py` 32.4 s,
`test_read_json.py` 10.2 s, `test_selftest_slow_tests.py` 12.8 s; `lint_ratchet --check` whole: "about 3 minutes" (the
Lead's siblings line, t-1451). All four test files are canon-class (they are keys of `slow_tests.json` `files`), so
docs/TESTING.md forbids running them whole locally: every row is a narrow call by construction.

Narrow-call times: `estimate, not verified` -- the Lead runs each ONCE before dispatch and writes the number into the
dispatch's `facts:` (designer guess in brackets, from the shape of the code only):

| id | command (PowerShell, repo root) | guess |
|---|---|---|
| census | `Measure-Command { python -B -c "import sys; sys.path.insert(0, r'C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests'); import test_judgment_census as T; r = T._real(); print({k: len(v) for k, v in r['problems'].items()})" }` | 5-25 s (the wide refusal scan of every script) |
| driver-layers | `Measure-Command { python -B -c "import sys; sys.path.insert(0, r'C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests'); import test_driver_layers as T; T.real_maps()" }` | 3-10 s (one map today: `fixtures/driver-layers.json`, Glob) |
| read-json | `Measure-Command { python -B -c "import sys; sys.path.insert(0, r'C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests'); import test_read_json as T; from pathlib import Path; f, u = T.census(Path(T.__file__).resolve().parents[1]); print(T.census_verdict(f, T.KEPT), u)" }` | 1-4 s (import of ~20 package modules + one AST pass) |
| test-layers | `Measure-Command { python -B -c "import sys; sys.path.insert(0, r'C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts'); import selftest as S; L = S.test_layers(); S.slow_tests(); print(S._listing_ok(L, [], True))" }` | 1-3 s |
| lint (per file) | `Measure-Command { python -B -c "import sys; sys.path.insert(0, r'C:/QAFactory/forge-repo/tools'); import lint_ratchet as LR, pyflakes.api as A; c = LR.Collector('tools/wave.py'); A.checkPath(r'C:/QAFactory/forge-repo/tools/wave.py', c); print(len(c.found))" }` | <1 s per file + interpreter start |
| temp tree | `Measure-Command { git -C C:/QAFactory/forge-repo worktree add --detach <scratch>/wt-probe origin/main }` then `git -C C:/QAFactory/forge-repo worktree remove --force <scratch>/wt-probe` | 3-15 s on Windows (fork F1 (a)/(c) pay it) |

A row whose measured narrow time exceeds `CHECK_TIMEOUT` (fork F7) is NOT run: it moves to §3's "cannot be narrowed"
list by a table edit before acceptance, never run whole.

## 3. How each check is narrowed (or why it cannot be)

- `census`: narrowed to ONE call of `analyse` (the real scan) and C1-C5; the 20 negative-fixture tests of the file
  (temp packages, the bulk of 96.9 s) are not run. It cannot be narrowed below the whole-package scan: C1 is "every unit
  has a row AND every row a unit" -- a per-file scan would read every other file's rows as stale (the test's own rule:
  "THE SCAN IS NOT DATA", `SCAN_ROOT`/`SCAN_EXCLUDE` are constants of the test). Problems are printed whole (fork F8).
- `driver-layers`: narrowed to `real_maps()` (the real maps); `bad_fixtures` x2 is skipped. Not narrowed per map
  (L11 reads every script's imports, L8 reads tests) -- fork F4.
- `read-json`: narrowed to `census` + `census_verdict` over `scripts/*.py` (G5's real half); the reader cases and the
  config cases (temp files) are skipped. Per-file narrowing is possible but saves under a second; not done.
- `test-layers`: the two ONE readers on the real files plus `_listing_ok` for the added test files; `--slow-tests`
  diffing needs a measurement (CI output) and is not run.
- `lint`: narrowed to the named files by the new `--path` flag of `lint_ratchet.py` (§5 card, fork F5): only the named
  files are linted, and only the baseline rows whose path is named are compared (a named file absent from the tree is
  linted as nothing, so its baseline rows read stale -- the same verdict the whole run gives). The hand-input line runs
  only for named files under `scripts/tests/test_*.py` and compares only their rows.
- Cannot be narrowed today, NOT in the table (listed, not run): the `--slow-tests` diff (needs a CI measurement);
  `selftest.py --limits --lang`, `test_audit_rules.py`, `test_hooks_wiring.py`, `test_null_outcomes.py`,
  `test_gate_registry.py`, `test_stage_joints_*.py` (6 files, 8.9-58.6 s each in `slow_tests.json`), `dup_ratchet.py`,
  `language_sites --check` (FG7-87: 14-20 s whole) -- not yet examined for a narrow call; fork F11 (scout) decides which
  become rows.

## 4. The `run` door and where `wave.py merge` calls it

`registry_preflight.preflight(repo, base, head, out=print, runner=None) -> Report` (the in-process API; `Report.rows` =
`[(id, state, seconds, lines)]`, `state` in `ok | red | cannot`; `Report.no_rule` = paths; `Report.empty` bool):

1. `git -C <repo> -c core.quotepath=false diff --name-status --no-renames <base>...<head>` (three dots: the branch's
   own change since the merge base; `--no-renames`: a rename is its old path deleted + its new path added, so both
   sides meet the signs). A failure -> one line `registry preflight: cannot judge (git diff: <first 200 chars>)`, no row.
2. Empty -> one line `registry preflight: no change against <base>`; nothing runs, no tree is made.
3. Each path is matched against every row; paths no row selects go to ONE line
   `registry preflight: no rule for <n> file(s): <p1>, ... <p10>` and, past 10, ` +<k> more` (`NO_RULE_SHOW = 10`).
4. No row selected -> no tree, no child. Else a temporary detached worktree of `<head>` (fork F1) under
   `<repo>/.claude/worktrees/preflight-<YYYYmmdd-HHMMSS>`; each selected row runs as a child
   `python -B <this file> check <id> --root <tree> [--paths <rel>...]` with `timeout=CHECK_TIMEOUT`, sequentially in
   table order, until `TOTAL_BUDGET` is spent; the tree is removed in `finally` (`git worktree remove --force`, then
   `rmtree`, then `worktree prune`, the order of `wave.Wave.drop`); a removal failure is one line, never a raise.
5. One line per row: `registry preflight: <id> ok (<s> s)` | `registry preflight: <id> RED (<s> s)` followed by up to
   `PROBLEM_SHOW = 5` indented problem lines and `  +<k> more` | `registry preflight: <id> cannot judge (<why>)` where
   why is `timeout after <N> s`, `budget spent`, `exit <rc>: <last stderr line>` or `<ExcType>: <msg>`.
6. Last line: `registry preflight: <r> run, <x> red, <c> cannot judge -- the merge goes on (advice; owner 18.11, FG7-94)`.

CLI: `python -B tools/registry_preflight.py run [--repo DIR] [--base origin/main] [--head HEAD]` prints the same
lines; exit 0 nothing red and nothing unjudged, 1 any red, 2 else any cannot-judge. `check <id>... [--root DIR]
[--paths <rel>...]` runs the named checks in-process, prints the same per-row lines, same exit codes; `--root`
defaults to the repo holding the script (a builder's worktree). An unknown id: exit 2, `unknown check <id>; known:
<ids>`.

`wave.py` call site (positional invariant): in `Wave.run()`, after `pin_problem()` and BEFORE
`jl.machine_lock("main-merge", ...)` (fork F1 (a)): `self.preflight(self)` where the seam `preflight=` is a constructor
parameter like `ci=`, default `wave.registry_preflight_lines`, which (i) resolves the tip as wave does (local
`refs/heads/<branch>`, else `refs/remotes/origin/<branch>`, else one line `registry preflight: cannot judge (branch
<b> not found)`), (ii) imports `registry_preflight` LAZILY inside `try`, (iii) calls
`preflight(root, "origin/main", tip, out=self.say)`, (iv) catches `Exception` (not `BaseException`) into one line
`registry preflight: cannot judge (<ExcType>: <msg>)`. Invariants the position preserves: the lock-held section is
byte-for-byte the same work as today (the preflight never lengthens `main-merge` and so never makes another wave's
60 s `LOCK_WAIT` run out); every refusal wave has today (pin, leftover, volume, conflict, unknown branch) still refuses
with its own text and code; wave's exit code is the one it would be with the preflight absent; a branch equal to or
behind origin/main yields the "no change" line (step 2) and nothing else. The preflight's lines come before `pushed:`.

## 5. The reader API for FG7-93 (`dispatch_new.py`)

- `registry_preflight.rules_for(paths, repo=None) -> list[str]`: the ids of the rows the paths select, table order,
  no duplicates. Path forms accepted (owns lines): absolute or repo-relative; `\` or `/`; a trailing ` (new)` marker
  stripped (and treated as status "added" for the A/D-only signs); a case difference folded only for the repo prefix
  on Windows (`os.path.normcase` on the prefix, the remainder kept); a path outside `repo` ignored; a directory path
  selects every row with a sign under it. No paths -> `[]`.
- `registry_preflight.command_for(paths, repo=None) -> str | None`: `None` when `rules_for` is empty; else ONE
  command, `python -B tools/registry_preflight.py check <id> [<id>...] [--paths <rel>...]` (`--paths` only when `lint`
  is selected, carrying the owns paths that are `.py` under `lint_ratchet.ROOTS`). The string contains no backtick
  and no newline (dispatch_new refuses both) and names no test file (dispatch_manifest's three-file and canon-class
  refusals stay unreached). FG7-93 appends it to `DoD:`; how many ids it keeps is FG7-93's choice, the API returns
  all, strongest first (table order).
- Both functions are pure (no git, no subprocess, no file read except `lint_ratchet.ROOTS` by import).

## 6. Edges (each with the invariant it protects)

| edge | behaviour | invariant |
|---|---|---|
| empty diff | one line, nothing runs, no tree | no check ever prints `ok` over nothing |
| a path no row knows | listed in the one `no rule for` line (10 names, then `+k more`; at 10 all ten, at 11 ten + `+1 more`) | an unknown file never triggers a check and never reads as checked |
| crash / non-zero exit not 0/1 / timeout / budget spent | `cannot judge (<why>)` for that row; the next rows still run until the budget | `cannot judge` is never printed as `ok`; the merge goes on (owner 18.11, FG7-94) |
| `git diff` fails (bad base, no origin/main) | one `cannot judge` line, no row | no verdict without a diff |
| the preflight module missing or raising on import / any `Exception` in wave's call | one `cannot judge` line | wave's exit code and refusals unchanged (non-goal: wave never refuses on the preflight) |
| branch not found locally nor on origin | one `cannot judge` line; wave then refuses with its own step-3 text | the preflight never pre-empts wave's own refusal |
| tree lacks what a check imports (an old branch tree before `--path` exists, a renamed test function) | that row `cannot judge (<ImportError/AttributeError/exit 2 text>)` | an absent checker is never green |
| renamed file | old path (D) and new path (A) both meet the signs (`--no-renames`) | a rename never hides a deleted file's stale baseline row |
| deleted `.py` with baseline rows | `lint` reads them stale -> RED, as the whole run does | the narrow verdict never passes what the whole run fails |
| non-ASCII / spaced path | `core.quotepath=false`; passed as one argv item | a quoted path never reads as an unknown file |
| pyflakes missing / baseline version drift | `lint_ratchet` exit 2 -> `cannot judge` | the ratchet's own "unknown is never a pass" holds |
| red problem output | 5 lines then `+k more` (at 5 all five, at 6 five + `+1 more`) | a huge red never floods wave's summary; the count is never lost |
| temp tree removal fails | one line naming the path; the sweep (`worktree_sweep.py`, detached merged-clean copies) cleans it later | a preflight never fails the merge on cleanup |
| TEMPORAL: before this node merges | wave prints nothing new; FG7-93 has no table to read | -- |
| TEMPORAL: after it merges, before FG7-94 | red is printed only (no queue exists yet); `Report` is returned to wave and dropped | no persistent record is written by this node (fork F9) |
| TEMPORAL: after FG7-94 | FG7-94 (owns `wave.py`) consumes `Report`; this node's lines and API unchanged | one table, one producer of the verdict |

Error direction (an existing function in a new role: the selection feeds a merge-time advice and a builder DoD).
`rules_for` may err toward SELECTING MORE (cost: seconds), never toward missing a row the change can break. Inputs that
must stay on the safe side: a new file at a new path; a rename; a deletion; a backslash or absolute owns path; a
`(new)` owns path; a directory owns path; a path differing in case on Windows. The verdict side may err toward
`cannot judge`, never toward `ok`: a child that dies, times out, or exits 2 is `cannot judge`.

## 7. Readers of every touched file (rule 7)

The `owns_readers.py` block was NOT attached to the brief. The Lead runs, before dispatch:
`python -B tools/owns_readers.py --paths tools/registry_preflight.py tools/wave.py tools/lint_ratchet.py tools/test_wave.py tools/test_lint_ratchet.py --names preflight rules_for command_for registry_preflight_lines --path`
and the critic answers its lines (Q13 (d)). Hand grep meanwhile (Grep tool, repo `tools/`, `.githooks/`,
`.claude/settings.json`; worktree copies under `.claude/worktrees/` excluded):

- `tools/lint_ratchet.py` (`lint_ratchet` in `tools/`: 21 hits in 8 files): `dup_ratchet.py` (imports `DOOR_PARSE`) --
  unchanged; `test_dup_ratchet.py`, `test_lint_ratchet.py` (import `LR`) -- unchanged / test_lint_ratchet gains rows in
  this node; `test_quarantine.py:1948` (runs `--check --repo`) -- unchanged (default path set untouched);
  `test_workflows.py:146,202` (pins the string `python tools/lint_ratchet.py --check`) -- unchanged; `lint-baseline.json`,
  `source-split-carriers.json` -- unchanged; `.github/workflows/forge-check.yml` (runs `--check`) -- unchanged;
  `.claude/settings.json:160,179` (allow-list `--check`) -- unchanged; `.githooks/`: 0 hits (positive control: `python`
  17 hits in 4 hook files).
- `tools/wave.py` (`import wave|from wave|wave\.py merge|"wave\.py"` in `tools/`: 5 hits in 4 files): `test_wave.py`
  -- changes in THIS node (the `go()` helper passes a stub `preflight=`); `test_volume.py:30` (a message text naming
  `wave.py merge`) -- unchanged; `test_test_volume.py` -- unchanged; `.claude/settings.json` 0 hits (control: the same
  file gives `lint_ratchet` 2 hits); FG7-85 (owns `wave.py`, `test_wave.py`) and FG7-94 (owns `wave.py`) -- parallel
  streams on the same file: fork F10.
- `tools/registry_preflight.py` (new): readers after this node -- `wave.py` (this node), `dispatch_new.py` (FG7-93),
  FG7-94 (consumes `Report`).
- Read, not touched: the four package modules imported in children (`test_judgment_census.py`, `test_driver_layers.py`,
  `test_read_json.py`, `selftest.py`) -- their function names `analyse`, `load_census`, `_real`, `real_maps`, `census`,
  `census_verdict`, `KEPT`, `test_layers`, `slow_tests`, `_listing_ok` become a cross-tree contract: a rename there
  makes the row `cannot judge`, not wrong (§6). `worktree_sweep.py` sees the temp tree -- unchanged.

## 8. Forks (the Lead's)

- **F1 -- where and on which tree.** (a) in `Wave.run()` before the lock, on a temp detached tree of the branch tip
  [RECOMMENDED: matches the row's "до слияния"; the lock section is untouched; output exists even when wave then
  refuses]; (b) inside `merge_and_push` on the merged tree W, first attempt only (free tree, exact post-merge state,
  but lengthens `main-merge`, risking another wave's 60 s `LOCK_WAIT`); (c) after the lock is released, on a temp tree
  of the pushed merge sha (exact main state, no lock cost, but after the merge, against the row's text). If the measured
  temp-tree cost (§2) exceeds a few seconds: a sparse tree of `ai-packages/qa-factory/` + `tools/` only.
- **F2 -- signs by path, not by added-line regex.** The row names content signs ("new `*_check` function", "new driver
  constant", "new `json.loads(read_text())`"). Recommended: path signs only -- the census unit rule is wider than any
  line regex (u2 judge calls, u3 refusal sites, `validate*`, `refuse*`, `*_errors`: `test_judgment_census.py:16-30`),
  the read-json shape includes `json.load(handle)` (`test_read_json.py:443`), and FG7-93 has owns paths, no diff, so a
  content sign would give the two callers two roads (P31). Cost: rows run on every package-script change (seconds).
- **F3 -- the test-layers row.** The row maps `test-layers.json`/`slow_tests.json` edits to `test_selftest_slow_tests.py`;
  that file tests the READER CODE on temp copies ("the data file and the tests folder they see are temp ones",
  `test_selftest_slow_tests.py:9-10`) and catches no data miss. Recommended: the readers on the real files
  (`selftest.test_layers`, `slow_tests`, `_listing_ok`); `test_selftest_slow_tests.py` stays canon's (a `selftest.py`
  code edit).
- **F4 -- driver-layers breadth.** (a) any `scripts/*.py` or map [RECOMMENDED, safe direction: L11 reads every
  script's imports]; (b) only the family files read from each map's `family` header (facade + `<prefix>*.py`) and maps
  -- cheaper, misses an outside script importing a part.
- **F5 -- lint narrowing.** (a) a new repeatable `--path REL` in `lint_ratchet.py` (owns widen: `tools/lint_ratchet.py`,
  `tools/test_lint_ratchet.py`) [RECOMMENDED: one road for the identity/count/stale logic]; (b) re-implement the
  per-file compare inside the preflight (a second road, P31: rejected); (c) list lint as "cannot be narrowed" (3 min).
- **F6 -- lint roots.** The row says "a changed file under `tools/`". Recommended: every `lint_ratchet.ROOTS` root
  (package scripts too), read from the module; the cost is the same per file.
- **F7 -- budget.** Recommended `CHECK_TIMEOUT = 30` s per row, `TOTAL_BUDGET = 60` s per run (module constants, a test
  moves them); any row measured above 30 s narrow leaves the table (§2). The owner said "seconds"; the Lead may want
  lower.
- **F8 -- whose red.** Recommended: print the problems as found, no second run on the base (doubles the time); a red
  already on main shows here too and FG7-94 attributes by merge commit. Alternative: run on base and print only new
  problems.
- **F9 -- hand-off to FG7-94.** Recommended: this node writes nothing persistent; `preflight()` returns `Report` and
  FG7-94 (it owns `wave.py`) decides how to queue it. Alternative: a queue file now -- needs a schema and an owner that
  FG7-94 is designing.
- **F10 -- `wave.py` streams.** FG7-85 (`wave.py`, `test_wave.py`) and FG7-94 (`wave.py`) are pending on the same file.
  Recommended: FG7-92 after FG7-85 lands (or before, but never parallel); this card widens owns to `tools/test_wave.py`.
- **F11 -- more registries.** §3's unexamined list (stage-joints, null-outcomes, gate-registry, hooks wiring,
  audit_rules, dup_ratchet, language_sites). Recommended: ship the five rows; a scout lists the registry checks the
  canon runs with a narrow call each; a follow-up node adds rows to the same table.

## 9. Small choices closed by the designer

- Rows run sequentially in table order (deterministic output; parallel children would contend on one CPU-bound scan).
- Checks import the TREE's modules and data (its `lint_ratchet.py`, its baseline, its tests); only the dispatcher
  file is the root's. A tree too old for a call is `cannot judge`.
- `agents/*.md` and `scripts/tests/test_*.py` select their rows only when added/deleted/renamed (content edits change
  no role name and no listing); in owns mode, only with the ` (new)` marker.
- One `no rule` line, not one line per file (a docs-heavy branch would flood the summary).
- `check` takes several ids so FG7-93 appends ONE command.

## 10. Builder card -- FG7-92

task: (Lead fills) | node: forge/7/FG7-92 | feature: F19
given: this card; `tools/wave.py`; `tools/lint_ratchet.py`; `tools/test_wave.py`; `tools/test_lint_ratchet.py`;
`ai-packages/qa-factory/scripts/tests/test_judgment_census.py`, `test_driver_layers.py`, `test_read_json.py`;
`ai-packages/qa-factory/scripts/selftest.py` (`test_layers`, `slow_tests`, `_listing_ok`)
owns:
C:/QAFactory/forge-repo/tools/registry_preflight.py (new)
C:/QAFactory/forge-repo/tools/test_registry_preflight.py (new)
C:/QAFactory/forge-repo/tools/wave.py
C:/QAFactory/forge-repo/tools/test_wave.py
C:/QAFactory/forge-repo/tools/lint_ratchet.py
C:/QAFactory/forge-repo/tools/test_lint_ratchet.py
non-goals: no `dispatch_new.py` change (FG7-93); no queue or record for FG7-94; no refusal anywhere in wave on the
preflight; no edit under `ai-packages/qa-factory/`; no row beyond the five of §2; no whole run of a canon-class file.
edges: §6 in full (every row is a requirement); §4's positional invariant; §5's path forms.
acceptance:
1. `RULES` is the one table; `rules_for`/`command_for` (§5) and `preflight` (§4) read only it.
2. `wave.py merge` prints the §4 lines before `pushed:`; its exit codes and refusal texts are unchanged with a
   preflight that is red, raises, or times out.
3. `lint_ratchet.py --path REL` (repeatable) narrows lint and comparison to the named files (§3); without `--path`
   every byte of today's behaviour holds (`test_quarantine.py:1948`, `test_workflows.py:146` unchanged).
4. The report gives the measured seconds of each `check <id>` on the real tree; a row over `CHECK_TIMEOUT` is
   reported, not shipped (fork F7).
test: (one per behaviour, strongest first; stop when test lines reach code lines and report the rest as not written)
- test: `tools/test_registry_preflight.py` -- `rules_for` table: package script -> census, driver-layers, read-json, lint;
  `judgment-census.json` -> census; `test-layers.json` / `slow_tests.json` -> test-layers; added `scripts/tests/test_x.py`
  -> test-layers + lint; `tools/x.py` -> lint; deleted `tools/x.py` -> lint; `docs/x.md` -> []; absolute, backslash,
  ` (new)`, directory, outside-repo, Windows case-differing prefix forms -> the same ids as the plain path; [] -> [].
- test: `tools/test_registry_preflight.py` -- `preflight` over a temp git repo with a fake `runner`: empty diff (one
  line, runner never called), no-rule list at 10 and at 11 files, ok row, red row at 5 and 6 problems, child crash,
  timeout, budget spent, `git diff` failure -- each the §4/§6 line and `cannot judge` never `ok`.
- test: `tools/test_wave.py` -- a wave merge with `preflight=` red / raising / slow stub: the merge is pushed, the exit
  code equals the run without a preflight, the preflight lines precede `pushed:`; `go()` passes a silent stub.
- test: `tools/test_lint_ratchet.py` -- `--path`: a new finding in the named file is exit 1; a baseline row of an
  unnamed file is not stale; a named deleted file with rows is stale; a named package test file's hand-input match
  counts and an unnamed one's does not.
- test: `tools/test_registry_preflight.py` -- `command_for` round trip: the string parses back through the `check`
  argparser to the same ids and paths; no backtick, no newline; None for [].
DoD: `python -m pytest tools/test_registry_preflight.py tools/test_wave.py tools/test_lint_ratchet.py -q`, then once
on the real tree: `python -B tools/registry_preflight.py check census driver-layers read-json test-layers lint --paths tools/wave.py`
(its per-row seconds go into the report) and `python -B tools/registry_preflight.py run --base origin/main --head HEAD`
in the builder's worktree (its lines go into the witness).
siblings: FG7-93 (reads §5), FG7-94 (consumes `Report`, owns `wave.py`), FG7-85 (owns `wave.py`/`test_wave.py`),
FG7-87 (`language_sites` fast path; a future row), FG7-90 (CI runs every check after a red one).
designer: this file (after acceptance).

## 11. Contradictions and analogs noticed (not acted on)

- The row's `test-layers.json`/`slow_tests.json` -> `test_selftest_slow_tests.py` mapping catches no data miss (F3).
- The row's "lint only for `tools/`" leaves package scripts out although `lint_ratchet.ROOTS` covers both (F6).
- The brief's fact "test_stage_joints.py does not exist" holds: the family is split into six `test_stage_joints_*.py`
  (`slow_tests.json:134-139`), all canon-class; a stage-joints row needs F11's scout.
- `wave.py` already has one information-only probe of the same class (`forge-check:` line, `wave.py:243`, never waits,
  never refuses) and one "cannot be computed: one line, the merge goes on" pattern (`check_volume`, `wave.py:272-296`):
  the preflight follows both.

## 12. Reading trail

- `plans/piles/forge/batch-7-vhodyashchie-4.md:110-119` (rows FG7-85..FG7-94).
- `tools/wave.py:1-160, 161-367, 641-769` (docstring, `git`, `Wave.__init__`, `locked`, `check_volume`, `merge_and_push`,
  `drop`, `finish`, `run`, CLI); brief fact `sed -n 25p` confirmed by Read of line 25.
- `tools/lint_ratchet.py:1-140, 231-355` (no per-file flag today: only `--check/--update/--repo/--root/--baseline`,
  `run` lines 232-238; stale computed over the whole baseline, lines 317, 338).
- `test_judgment_census.py:1-77, 484-535, 936-969`; `test_driver_layers.py:1-31, 1609-1702`; `test_read_json.py:181-208,
  439-618, 805-825`; `test_selftest_slow_tests.py:1-37, 674-694`; `selftest.py:577-676, 757-780, 1079-1108`.
- `slow_tests.json:1-12` + Grep of the five names (lines 37, 68, 96, 131, 134-139); `test-layers.json:1-45` (`canon_only`).
- `docs/TESTING.md:94-163, 280-299`; `tools/dispatch_new.py:1-117`.
- Glob `fixtures/*-layers.json`: one map (`driver-layers.json`).
- Hand greps for §7 (counts there); `worktree_sweep.py` treats detached copies (Grep `worktrees|detached|HEAD`, -i).
- Not measured (no shell): every narrow time and the temp-tree cost -- §2 commands, `estimate`.

## 13. Lead decisions (18.11)

F1 (a) before the lock on a temp tree of the branch tip; F2 path signs only; F3 the readers on the real files; F4 (a);
F5 (a) `--path REL` in lint_ratchet.py, owns widened to lint_ratchet.py and test_lint_ratchet.py; F6 every
`lint_ratchet.ROOTS` root; F7 30 s per row, 60 s per run; F8 print as found, no base run; F9 nothing persistent,
`preflight()` returns a Report; F10 the builder starts after FG7-85 merges (wave.py is one file); F11 ship five rows,
a scout lists the remaining registry checks for a follow-up node. The narrow times of section 2 are measured by the
builder in its witness (the designer had no shell).
