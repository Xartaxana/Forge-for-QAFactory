# t-1280 -- critic: FG7-63 code (DoD-run gate copy + witness canon split)

Tree `.claude/worktrees/agent-a21c6e8e467134b7d`, head b31dd4f1 (27b22803 + b31dd4f1 over origin/main 9d4ed53f).

**Verdict: NEEDS WORK** -- 1 blocking finding (F1), 5 fix-before-merge (F2-F6), 2 decisions that belong to the Lead (F7, F8).
Whether to accept, and whether to amend the spec on F7/F8, is the Lead's decision. This verdict is an input to it.

## Findings

**F1 (BLOCKS placement) -- once placed, the copy turns an existing tools test red, and every builder dispatch that names a test file now makes git calls inside the hook.**
`_canon_class` (dispatch_manifest.py.next, `_canon_class`) runs `owns_readers._resolve` / `_ls_tree` / `_slow_status`, which means `git rev-parse`, `git ls-tree` and `git show`, all through `subprocess.run`. Nearly every builder dispatch names a `test_*.py`, so these calls happen on almost every builder dispatch. With the copy loaded as `dispatch_manifest`, `tools/test_dispatch_gate.py::test_push_before_launch_warns_when_main_is_ahead_of_origin` fails at line 2617 (`assert all(cwd == "Z:/repo" for _a, cwd in calls)`). The fixture's DoD is `python -m pytest tools/test_dispatch_gate.py -q` (`_DOD_LINE`, line 56), so the gate's own git calls land in the test's patched `subprocess.run`, carrying `cwd=None` and `-C <tree>`. The same test passes against the live gate (Trail, runs 2-4). The cost is also not what commit b31dd4f1 (a) says ("one read of two data files"): it is three git subprocesses plus loading the package selftest module, measured at 0.54 s cold and 0.23 s warm inside one process. Each hook run is a new process, so a builder dispatch pays the cold cost.
Fix (also closes F4 and deviation 6): drop the git route. Read the slow list from the working tree through `selftest.slow_tests(<root>/ai-packages/qa-factory/scripts/slow_tests.json)`, the package's one reader, loaded the way the copy already loads `selftest` (`tq._pkg_module`). That removes the subprocesses, the latency and the snapshot mix: today the slow list is read at HEAD while test-layers.json is read from the working tree, so one class is built from two snapshots. If the Lead keeps git, the fix is to edit test 2617 so it filters to dispatch_gate's own calls, and that edit has to land in the same commit as the placement.

**F2 (fix before merge) -- R2 gives a false refusal on a real tools/ test, because the match is on basenames only.**
The probe DoD `` `python -m pytest tools/test_controller_blocks_gen.py -q` `` is refused with "runs the canon-only file(s) test_controller_blocks_gen.py whole". The glob `test_controller_*.py` belongs to the package, and the file is a forge tools test. Today this is the one collision: tools/ test names checked against the 152 slow keys and 4 globs. Any future tools/ test that shares a name with one of the 152 package slow keys will be refused the same way. Fix: count a token toward R2 only when its path is not under a `tools` directory (the class is package-only by its own data homes). A cleaner variant: a bare name, or a path whose parent is `scripts/tests`. R3 can keep counting all test files.

**F3 (fix before merge) -- the whitespace split misses tokens with punctuation glued on (false passes).**
`` `python -m pytest scripts/tests/test_story_step.py; echo ok` `` and `` `(python -m pytest scripts/tests/test_story_step.py)` `` both pass with code 0. `_TOKEN_STRIP` strips quotes and backticks only, so `test_story_step.py;` and `test_story_step.py)` fail `endswith(".py")`. Fix: strip `;,()&|<>` from both ends of each token as well. On the shared tokenizer (axis 11): the one walker is the package's `hooklib.walk`. The forge has no public tokenizer (hygiene_gate's `_tokenize` is private, and agent_budget's convergence is queued as B-434). For a hint scan of `.py` tokens in a DoD, the stripped split is proportionate. Converging on `hooklib.walk` is axis 11's queued node B-434, not this round's.

**F4 (fix before merge) -- the class predicate is implemented twice (Q6).**
`scenario_walk._canon_class` + `is_canon` (scenario_walk.py `witness_for`) and the copy's `_canon_class` + the inline `f in cls["slow"] or any(fnmatch.fnmatchcase(...))` both compose the same class from the same two files, by different roads: the working tree vs HEAD, and selftest.slow_tests vs owns_readers. No file gets a second reader, so the spec's letter holds. But the definition "canon-only = slow keys OR canon_only globs" lives in two places, and they already disagree on snapshot. Fix: one function in selftest next to `test_layers` / `slow_tests` (e.g. `canon_class(package) -> {slow, globs, why}` plus `is_canon(name, cls)`), called by both.

**F5 (fix before merge, Q5(c)) -- the gate's real class reader has no row.**
Every gate row monkeypatches `_canon_class`. Its real behaviour has no test, and that behaviour reaches a door: the note "canon class could not be read (...)" on an actual read failure, the `no_list` note when the key is absent, and `layers.get("absent")`. F1's fix makes the reader take a path, so a temp-dir row becomes cheap. One row is enough: a missing slow_tests.json gives the unread note and code 0. The new `layers_problems` refusal `"canon_only" must be a list of test file name globs` (a selftest door) has no row either.

**F6 (fix before merge, Q7) -- small code issues.**
`_canon_class(root=None)`: the `root` parameter is never passed by any caller (dead). The docstring says "the ONE I/O of this module", but the slow-list read also goes through owns_readers' module-level `_config()` read of tools/owns_readers.json. That is a third file the docstring does not mention, and it disappears if F1 is fixed as proposed.

**F7 (Lead decides; spec divergence, deviation 3) -- R3 skips files named by node id.**
`` `pytest tools/test_a.py::x tools/test_b.py::x tools/test_c.py::x tools/test_d.py::x tools/test_e.py::x` `` passes. The spec reads "the DoD commands name more than 3 distinct test files". The deviation points the safe way for time (node-id runs are narrow) and the unsafe way for the hub-DoD class (one DoD fanning out over many files). Either amend the spec text, or count the file part of `file.py::name` tokens in R3 (one line: `tok.split("::")[0]`).

**F8 (Lead decides; spec silent) -- a directory run passes.**
`` `python -m pytest ai-packages/qa-factory/scripts/tests -q` `` passes. It runs every canon file whole, so it is the widest violation of R2. The spec names no rule for directory arguments. Proposed as a follow-up row for the gate: `<a DoD pytest run of the package tests directory passes R2> | узел: <node id the Lead opens>`.

## Deviations judged
(1) Repo root from the module location: acceptable. At placement it is the forge checkout, which holds both data homes; the dispatch cwd may be a worktree or a temp dir.
(2) Class read only when a `test_*.py` token appears: correct. All 152 slow keys and all 4 globs have the `test_*.py` shape (Trail, run 5).
(3) See F7.
(4) Fallback scenario lines under the canon header: consistent with the spec's "the scenario layer judges it". The prefix "no scenario or keep row covers <rel>" is kept byte for byte (test_scenario_walk.py row and scenario_walk.py diff).
(5) `EXTRA_SKIP_ITEMS`: right for the byte-for-byte invariant. A typo `dod_run` gets "unknown item 'dod_run'", and the refusal text names the exact door, so the miss can be recovered.
(6) The slow list at HEAD through owns_readers: see F1. This deviation is what causes the blocker.
(7) `selftest.py` joined the owns: needed (`test_layers()` must return the key, and the shape check guards it). Its row is missing (F5).

## Seam and class notes
- K2 POSITION: verified by reading `check_cut` (the check runs after `still` and the form/designer notes, and appends to the end of `skip_notes`) and by a run. All 313 rows of test_dispatch_manifest.py pass against the copy. A dispatch refused today keeps its message, because every refusal returns before line 1111. One form changes on purpose: `manifest-skip: dod-run -- x` was SKIP-REFUSED as an unknown item and now passes. A passing dispatch gets a new note only if the class is unreadable or `canon_only` is absent. The dispatch's K2 command (`DISPATCH_MANIFEST_PATH=...`) does nothing: that variable is read nowhere (case-insensitive grep over tools/ and .claude/ found 0; the control grep for `dispatch_manifest.py` found 2 files). So I loaded the copy as `dispatch_manifest` with a preload runner (Trail). Any builder witness produced with that variable tested the live gate. The builder's report was not in my manifest, so I did not reproduce its witness. My own runs replace it.
- K3 (probe through `dm.check`, the copy, real class data): spaces in a quoted path -> refused (right). Windows backslashes -> refused (right). `--only name` -> refused (matches the spec; `--only` is not a narrowing flag of the story tests). `-k name` on a canon file -> refused (matches the spec; the way-on names `::`). Env prefix -> refused (right). A file named in prose, or in a one-token span -> passes (right, `_tokens_ok`). A tools/ basename collision -> false refusal (F2). Two commands joined with `&&` -> the canon file is caught (right). Glued `;` or `)` -> false pass (F3). Directory -> false pass (F8). Five node ids -> pass (F7). `selftest.py --limits` -> pass (right).
- K4: test_dispatch_cut, test_dispatch_new, test_dispatch_gate and test_dispatch_gate_md against the copy: 524 passed, 1 failed (F1). Error direction with git absent or failing: owns_readers `_git` maps any exception to rc -1, so `slow` is None and the result is a note and a pass. The whole read sits in `except Exception`. A hook outside a repo does not block.
- K5: `test_quarantine._write_layers` loads the whole object, mutates it and dumps it back, so `canon_only` is kept. `_blob_sections` reads only its four sections and ignores the rest. source_split's JSON rewrite dumps the loaded object, so the key is kept. `selftest.layers_problems` has no unknown-key refusal (it checks named keys only). No reader drops or refuses the key, so no blocking finding.
- Q4 class-wide: axis 9 (what a test file is) -- the gate classifies by basename, which is the source of F2. Axis 11 -- see F3. Axis 13 -- the copy reuses `_command_lines` / `_INLINE_SPAN_RE`, so the dispatch text has no second parser. No sibling is left open outside the fixes above.
- Q6 DUPLICATION AND CONSISTENCY: F4. The slow-list reader is reused (owns_readers -> `selftest._slow_tests_problem`). test-layers.json goes through `selftest.test_layers` in both places. I did not re-derive the clone ratchet; its result is forge-check's.
- Q7 CODE QUALITY: `_dod_run_check` is about 45 lines with 3 nesting levels, and `_canon_class` about 30. witness_for grew about 20 lines and stays readable. F6.
- Q8: no Cyrillic in the added package lines (0). `git diff --check` is clean. LF is kept.
- Q9: no ratchet row raised. `canon_only` is a new key, not a shrink-only section of AR-20.
- Q10: AR-20 lists test-layers.json among its carriers, and the commit does not name AR-20. The key added is not a ratchet section, so no reader is starved. Minor: name it in the placement commit. VARIETY: forge-only gate plus a package test helper. A project of any shape is untouched, and an unreadable class is a note, never a block.
- Q11 JUDGMENT: the refusals are token shape against a data list, with a waiver door. No role judgment moved. The forge tool is outside the census scan root.
- Q12 ONE ROAD: none found. The gate applies to builders only per the spec. Searched: the basename and `tools/` branches in the copy. The only path-scoped issue is F2, which goes the other way: the package class is applied to tools/.
- Q5 TESTS: (a) killing power -- the 14-row table would catch R1, R2 (slow and glob), R3 at 3/4, and the waiver and its non-waiver. It cannot catch F2 or F3. (b) Values trace to the spec (3 pass, 4 refused; `dod` does not waive) and to the spec's note text. (c) F5. (d) The rewritten witness_for fallback row is still checked at test_scenario_walk.py (new text row). (e) No duplicates found. (f) `msg.startswith("DOD-RUN REFUSED")` is a prefix pin on the door's identity, which is acceptable. Volume: about 55 test lines against about 165 code lines, within budget. (g) No new test file.

## Spot-checks
- "canon_only is read by both consumers": scenario_walk via `layers.get("canon_only")`, the gate via `test_layers(...)["canon_only"]`. Verified by the live `--witness-for scripts/selftest.py` run (Trail, run 6), which printed the header and `run locally: 1 file(s); canon judges: 4 file(s)`.
- "slow list has only test_*.py keys": 152 keys, 0 of another shape (run 5).

## Trail
Read: dispatch_manifest.py.next diff vs live; `.next` 255-310, 680-705, 1043-1128; owns_readers.py 85-305; test_quarantine.py 88-105, 196-218; selftest.py 595-615, 1008-1030; scenario_walk.py and test_scenario_walk.py diffs; test_dispatch_manifest.py diff and imports; test_dispatch_gate.py 2142-2154, 2585-2620, line 56; gitcmd.py `git`; SIBLING_MAP axis 11; architecture.md AR-20; commit b31dd4f1 message.
1. `python -B <scratch>/run_next.py <tree> tools/test_dispatch_manifest.py` (preloads `.next` as `dispatch_manifest`) -> `313 passed in 2.99s`, `has _dod_run_check: True`.
2. Same runner on test_dispatch_cut, test_dispatch_new, test_dispatch_gate, test_dispatch_gate_md -> `1 failed, 524 passed in 44.28s`; FAILED `test_dispatch_gate.py::test_push_before_launch_warns_when_main_is_ahead_of_origin`.
3. The same test alone against the live gate (`python -m pytest ... -q` in the tree) -> `1 passed in 0.53s`.
4. The same test alone against the copy -> `1 failed`, `AssertionError` at test_dispatch_gate.py:2617.
5. Data probe: slow keys 152, `nontest keys []`, tools collisions `['test_controller_blocks_gen.py']`.
6. `python -B <tree>/ai-packages/qa-factory/scripts/tests/test_scenario_walk.py` -> `=== test_scenario_walk: 99/99 ok ===`; `scenario_walk.py --witness-for scripts/selftest.py` -> 1 local file, header, 4 canon files, count line.
7. `<scratch>/probe.py`: `canon_class 0.54s ... why []`, `second 0.23s`; K3 case results as listed in the seam notes.
8. Hygiene: Cyrillic in the package diff `+` lines: 0; `git diff --check`: empty; `ls-files --eol`: lf.

```json
{
  "verdict": "blocker",
  "blockers": [
    "F1: once placed, the copy turns tools/test_dispatch_gate.py::test_push_before_launch_warns_when_main_is_ahead_of_origin red (line 2617): _canon_class makes three git subprocess calls (owns_readers _resolve/_ls_tree/_slow_status) on every builder dispatch that names a test file; fix: read slow_tests.json from the working tree through selftest.slow_tests, or edit that test in the placement commit"
  ],
  "fixes": [
    "F1 tools/dispatch_manifest.py.next::_canon_class: drop the git route, read slow_tests.json through selftest.slow_tests (blocks)",
    "F2 tools/dispatch_manifest.py.next::_dod_run_check: R2 ignores tokens under a tools directory; tools/test_controller_blocks_gen.py is falsely refused today (before merge)",
    "F3 tools/dispatch_manifest.py.next::_dod_run_check: also strip ;,()&|<> from token ends; test_x.py; and test_x.py) pass today (before merge)",
    "F4 one class predicate in selftest (canon_class + is_canon) called by scenario_walk.witness_for and the gate (before merge)",
    "F5 one row driving the real class reader to the unread note; one row for the canon_only shape refusal of selftest.layers_problems (before merge)",
    "F6 dead root parameter and the inaccurate one-I/O docstring of _canon_class (before merge)",
    "F7 Lead: amend the R3 spec text or count file.py::name tokens",
    "F8 Lead: open a node for directory pytest runs passing R2"
  ],
  "class_completeness": "Axis 9: basename classification causes F2. Axis 11: whitespace split, F3; convergence to hooklib.walk is the queued B-434. Axis 13: reuses _command_lines, no second dispatch parser. K5: canon_only kept by test_quarantine._write_layers and source_split; no strict reader refuses it.",
  "trail": {
    "read": [
      "tools/dispatch_manifest.py.next",
      "tools/owns_readers.py",
      "tools/test_quarantine.py",
      "tools/gitcmd.py",
      "tools/test_dispatch_manifest.py",
      "tools/test_dispatch_gate.py",
      "ai-packages/qa-factory/scripts/selftest.py",
      "ai-packages/qa-factory/scripts/tests/scenario_walk.py",
      "ai-packages/qa-factory/scripts/tests/test_scenario_walk.py",
      "ai-packages/qa-factory/scripts/tests/test-layers.json",
      "docs/SIBLING_MAP.md",
      "ai-packages/qa-factory/design/architecture.md"
    ],
    "reruns": [
      {"command": "run_next.py preload of .next; pytest tools/test_dispatch_manifest.py", "result": "313 passed"},
      {"command": "run_next.py preload of .next; pytest test_dispatch_cut, test_dispatch_new, test_dispatch_gate, test_dispatch_gate_md", "result": "1 failed, 524 passed; test_push_before_launch_warns_when_main_is_ahead_of_origin"},
      {"command": "pytest that test against the live gate", "result": "1 passed"},
      {"command": "python -B test_scenario_walk.py", "result": "99/99 ok"},
      {"command": "probe.py K3 cases and _canon_class timing", "result": "0.54s cold; false refusal on test_controller_blocks_gen.py; false passes on glued ; and ), on directory runs and on 5 node ids"}
    ]
  }
}
```
