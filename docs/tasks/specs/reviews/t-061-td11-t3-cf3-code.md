# t-061 — critic gate, TD-11 spec C: T-3 (`tools/test_split.py`, builder t-053, report named t-050) and C-F3 (`split-keep` + K5 door, builder t-048)

Critic (Opus), 12.11.2026. Read-only review. The experiments ran on fixtures in temp dirs outside the repo; the drafts ran read-only on the real tree; nothing was written in either worktree. A verdict is an INPUT to acceptance; accepting and changing statuses is the Lead's call.

## Verdict

- **T-3: NEEDS WORK.** 2 blockers (T-B1, T-B2) and 9 fixes.
- **C-F3: NEEDS WORK.** 2 blockers (C-B1, C-B2) and 4 fixes.
- **Can the six parallel cuts start?** Only the three wave-1 files the tool handles today: N1 `test_infra_failure`, N4 `test_story_run_loop_b`, N6 `test_controller_rework`. The tool refuses the other three wave-1 files (N2 `test_no_move_seam`, N3 `test_story_run_freshness`, N5 `test_handoff_values`) whatever the map says, so they wait for T-B1. T-B2 does not touch N1/N4/N6. Evidence: their drafts show 0 unplaced statements, `global` appears 0 times in all 15 GROUP 1 files, there are no module-level check calls, and the only late imports are inside string literals (`test_probe_by_code.py:1146-1176`). T-B2 does block merging the tool before N8 (`test_grounding_table`, wave 2). The C-F3 blockers only bite in the integrator's closing commit NC (R-A1: nodes never write `test-layers.json`), so they block no cut, but they must be fixed before NC. Lead's decision.

## T-3 findings

**T-B1 (blocks N2, N3, N5; DoD "a runner generated per part for the runner shapes found in the tree" not met).** The report checked 3 of the 6 wave-1 files and says "None refused". I ran `--draft` read-only on all 15 GROUP 1 files. These are refused:
- `test_no_move_seam` (67 refusals),
- `test_story_run_freshness` (1),
- `test_handoff_values` (215),
- `test_probe_by_code` (13),
- `test_probe_by_code_languages` (5).

I reproduced each shape on a minimal fixture (exp 21-23):
- (a) **`if __name__` block of direct scenario calls** (handoff_values:1609-…). `test_split.py:311-327` puts every function the guard calls into `guard_called` and then marks it a RUNNER (`or n.name in guard_called`). Each scenario body then goes through the runner-statement check and is refused: "runner statement not recognised … x = 1", "name `a_one` is a runner block". This is shape (4), which the docstring and report §1 claim is supported.
- (b) **`for scenario in (<literal tuple>): scenario()` inside `main`** (no_move_seam:1390). `_fill_stmt_block` accepts only call statements (`:569-572`).
- (c) **freshness `main`**: `chosen = [... SCENARIOS ...]; run_scenarios([], chosen)`. `:525` refuses any literal argument, and the empty side-by-side `[]` counts as one: "a block that reads a run list by name also calls run_scenarios with literal lists". Report §6 says this shape "needed the by-name mechanism" and was "verified in the file, not run through the tool". It is refused, and no test case covers it.
- (d) **`test_grounding_table`** (module-level checks, then `finish(...)` at module level, no runner). The draft says "0 refused construct(s)", rc 0. But every map is refused ("part … holds no scenario"; exp 19), and a module-level `finish` piece is only emitted alongside a module-level for/run/call block (`:1037`). That is a false green from `--draft`, which contradicts D7.

Fix: support (a)-(c), and either support (d) or have the draft refuse it. Each needs a table case in `test_test_split.py` built from the real shape.

**T-B2 (proof green, behaviour changed or a check lost; blocks merging the tool before N8, not N1/N4/N6).** Exp numbers are from the trail. Every case printed `PROOF: ok` (a)-(e), then the parts were run against a stub harness:
1. A **module-level check homed in common** (a `statements` row, or an assignment such as `SEEN = check(...)`; exp 3, 18). (a) counts it as "common 1". If no part imports a common name the check never runs: the original ran 3/3, the parts ran 1/1 + 1/1. If parts do import common, it runs once per part. The class is real for N8: `test_grounding_table.py` has 148 module-level check lines.
2. A **scenario call nested inside a by-name consumer** (`if …: extra()` in a `main` that reads `SCENARIOS`; exp 24). The block is copied verbatim into every part, so `extra`'s check runs in both parts: original 3/3, parts 2/2 + 2/2. `:522-528` only inspects top-level statements of the block.
3. A **statement between imports** (`os.environ[...] = ...` before `import envmod`; exp 1). It is moved after the whole header, the import now runs first, and the check goes red.
4. **Conditional rebinding across homes**: `FLAG` row in part a, `if …: FLAG = True` in common (exp 4). The part re-binds `FLAG = False` after `from common import FLAG`, and the check goes red.
5. A **late import that shadows a def** (`def helper` … `from other import helper`; exp 5). Imports are hoisted into the header, so the def now wins.
6. **`global` rebinding of a common name** by a common helper, read by a part through `from common import STATE` (exp 9). The part holds a stale copy and goes red. `:825-828` refuses only when the writer's home differs from the name's home.
7. A **mutating statement on a common name homed in one part** (`ITEMS.append(2)`; exp 15). The other part sees different data and goes red.

Fix: refuse (or keep source position for) 1, 3, 4, 5, 6 and 7. That means:
- a statement or assignment carrying a check call can never be homed in common;
- a statement that precedes the last import is refused;
- a name bound by segments in two homes is refused;
- an import after a def or assign of the same name is refused;
- a `global` write to a name read in another home is refused;
- a statement whose free names include a name homed elsewhere is refused unless homed with that name.

For 2, inspect every call inside a verbatim block (`ast.walk`), not only top-level statements.

**Proof questions (Q2).**
- (e) "compile" is near-vacuous. The (0) step already `ast.parse`d every file, so (e) fails only on compile-stage errors (`return` outside a function and similar). Its label collides with spec 2.5 (e): "each part run alone, tally pasted". A node could paste "(e) compile ok" as the run witness.
- (b) and (d) re-segment the generated text with the same `analyze`. They catch generator corruption (the tamper case shows it), but they are not independent of the classifier.
- (c) is independent of the MAP (it is derived from the written files), but not of the classifier. A call the classifier does not see as a run entry is invisible on both sides; that is what T-B2.2 shows.
- (a) counts AST call sites, not the spec's `git grep -c` lines. Two checks on one line count 2, and a check name inside a string counts 0. Both metrics count SITES, not executions, so table loops, common helpers run per caller and module-level common checks (T-B2.1) are all invisible to it. The executed count is the old Y against the sum of the new Y's (Lead brief «Правки» 9). The tool does not do that, and its report does not tell the node so.
- Proof that never passes on a real shape: a by-name consumer that holds its own check (exp 12) fails (a) whatever the map: 3 vs 4. This is safe-direction; no current file was seen with it.
- I re-ran infra_failure with homes from spec 3.1 ranges and reproduced the builder's numbers exactly (trail).

**Fixes (T-F1…T-F9), none blocking the cuts:**
- T-F1: rename the tool's (e) to "(compile)" and print a line "spec (e) and the reverse-order run (brief «Правки» 9) are the node's: not run here".
- T-F2: dead or lying code:
  - `:896-898` (`for part in plan.parts: pass` under the comment "E8 … checked on the generated text"; nothing is checked);
  - `:287` `dropped`, `:1230` `gen_names`, `:1603` `entries … or True`, `:980` `src_node` (all unused);
  - `validate_map` returns `ok`, which nobody reads.
- T-F3: functions over 60 lines: `analyze` 271-502 (232), `build_plan` 681-907 (227), `prove` 1208-1375 (168), `render_runner` 954-1043 (90), `_fill_stmt_block` 505-573, `run_map` 1476-1544, `run_draft` 1547-1611. Split at least `build_plan` and `prove` along their commented phases. Queue if the fix round is tight.
- T-F4: `find_importers` collects `alias.attr` in any ctx. A write through the alias (`REWORK.X = …`, `patch.object(REWORK, …)`) would silently stop reaching common after the split. Refuse a Store ctx or `patch.object`/`setattr` on the alias. None exists today: a grep of the 6 alias importers found 0, against a control of 3 `REWORK.` uses in `test_denial_scope.py`.
- T-F5: the rollback at `:1526-1534` deletes a target that existed byte-identical before the run (`targets_state` "same"). Skip files in `same`.
- T-F6: `done_state` (`:1451`) raises a TypeError traceback when `parts` holds a non-string (`validate_map` checks only `list`).
- T-F7: the report's id (t-050) differs from the journal task (t-053). The §6 freshness claim is false (T-B1 c).
- T-F8: `WORLD_HINTS` (`:59-61`) is a closed list of package helper names in code. It drives a WARNING only and lives in forge tooling, so this is not AR-1 proper. Queue it as a data row if it grows.
- T-F9: when a scenario named on the argv has moved to another part, the part runs zero scenarios and exits green (E14 "same semantics" holds only per part). Print which part holds the name, or exit nonzero.

**The builder's deviations (Q4):**
- D1 (an assignment needs only a `names` row): right per spec E1 and brief «Правки» 2 (R10 exempts census names). The consequence is T-B2.1: an assignment carrying a check needs the check-in-common refusal.
- D2 (the shim runs parts only with `--all`): right. Spec 2.2 says so, the precedent `test_story_step.py:49` does the same, and `selftest.ran_nothing` (`selftest.py:458-462`) is silent for a file with no `test_*`. A shim run directly by the canon must not run every part a second time. Dispatch edge 7 ("when run directly runs the parts") is the wrong reading for selftest and CI and should be corrected by the Lead.
- D3 (common name and part prefix enforced): right per spec 2.1 and the §7 table, and it is the name C-F3 gets wrong (C-B1).
- D4-D7: acceptable. D7's draft exit code is false-green on the grounding shape (T-B1 d).

**Apply (Q3).**
- Temp-then-rename, a proof over the re-read temp files, and a refusal before any write: all correct.
- A rename failure is rolled back (T-F5 aside).
- Ctrl-C leaves the placed parts with the source intact, and a re-run completes: identical targets count as "same".
- A re-run after a full apply says "nothing to do", for both the shim and the deleted source.
- A target that differs is refused.
- CRLF is kept, and mixed newlines and BOM are refused (builder case; consistent with the SIBLING_MAP line-slicing axis, since a lone CR is refused, not split).
- A stale `<common>.py` is not checked when no common is generated (minor).

## C-F3 findings

**C-B1 (wrong value pinned by a test; fix before NC).** `tools/test_quarantine.py:1479` writes the shim row as `covers: ["tests/{Path(old).stem}_common.py"]`, which gives `tests/test_controller_rework_common.py`. T-3 writes `controller_rework_common.py` (`common_stem_for`, spec 2.1, §7 table, and T-3's own row block). `tools/test_test_quarantine.py:922` asserts the wrong `tests/test_k_common.py`. I reproduced it in a temp world: `SHIM_COVERS ['tests/test_k_common.py']`. The shim keep row would cover a file that does not exist and miss the helper it imports (the guard in `test_selftest_slow_tests.py:477-489`). N2 and N6 have shims. Fix: strip a leading `test_`, as T-3 does, and fix the test.

**C-B2 (K5 door scoped wrongly; rule 15, paired condition).** The `keep-split:` door accepts the removal of OLD's row when every named part "is a keep row in that commit" (`:1658`). Nothing ties a part to THIS commit or to OLD, and nothing checks OLD's file state. In a temp repo, a commit that removes `test_k.py`'s row while `test_k.py` stays on disk, with the message `keep-split: test_k.py -> test_other.py -- not really a split` (where `test_other.py` is an older, unrelated keep row), passes `check`: `ON_DISK True RC 0 … 0 violation(s)`. The spec's wording ("every named part exists in that commit's keep") is too wide, and the builder followed it. Fix:
- every named part must be a keep row ADDED by that commit (in `new` and not in `old`) and named `<OLD stem>_*` (spec 2.1);
- without a shim, OLD must be absent from that commit's tree;
- with a shim, OLD must be present and its row rewritten.

The tree state at the sha keeps R-A1 intact: the deletion sits in the node's commit and the row change in NC. This is why the builder's open point 3 (no same-commit deletion) is right as far as it goes, and the tree check is what closes the door instead.

**Fixes:**
- C-F1: the command lets any new on-disk file be a "part". I reproduced a `test_brand_new.py` that inherits the full `detector` row. Refuse a part whose name lacks the `<OLD stem>_` prefix, and optionally one whose text lacks T-3's marker "a part of <OLD>". K5 still refuses no plain new keep row, but it never did: `check_history` polices added keep rows only for quarantine returns (`:1676`), and the "new test file" rule is the critic's standing question 5. So the diff adds no new hole there, but its door should not lend one legitimacy.
- C-F2: the shim row keeps the old `named_by`. Object: spec E4 says "the shim is never the named proof". Write `named_by: []` (a data_join row needs none: `selftest.py:617` demands it only for `detector`). Name the importers in `why`, as spec 4.1 says ("re-exports for <importers>"), through an `--importers` option or by reading T-3's row block.
- C-F3: spec 4.1 says part covers are "inherited … plus `tests/<stem>_common.py`"; 4.2 says "copied whole". Adding the common file errs on the safe side (it widens) and saves the hand edit that would make a second writer (AR-14). Add it when the file is on disk.
- C-F4: the report says "axes: not a mechanism". A new K5 door and a new commit-line convention ARE a mechanism (CLAUDE.md rule 10: "a gate, a check, a protocol convention"). The commit needs the four questions and the axis block. Update SIBLING_MAP axis 18 (row 387: "a `keep` row leaves only through `drop-keep` or a phase-2 `enter`") with the third exit, `split-keep`, in the same commit. Detector for door misuse: name one, for example the K5 accept stream already in `forge-check`.

**Open points (Q5):**
- No `--layers`: confirmed (the sibling subcommands use `--root`).
- The shim keeping `named_by`: objected (C-F2).
- No same-commit deletion: confirmed, and replaced by the tree-state check (C-B2).
- Does K5 still refuse a bare removal? Yes (case `bare-removal-still-refused`).
- Does split-keep leave the old row behind? No: it is removed, or rewritten with `--shim` (tested).
- Is it run without the door? The command writes the message file. K5 refuses a removal with no line, but a line naming foreign rows passes (C-B2).

## Standing questions

- **Fit to the spec:** T-3 misses its DoD on runner shapes (T-B1) and on proof soundness (T-B2). C-F3 fits §4.2 except for C-B1, C-B2 and C-F2/C-F3 (spec 4.1 against 4.2).
- **Seams:** C-B1 is the junction defect between the two diffs. Both are new or additive, and no seam with another node's files is touched.
- **DUPLICATION AND CONSISTENCY:** `test_split.py` re-implements things that `tools/source_split.py` (worktree a72b…, read only) already has:
  - `_targets` (`test_split:228` vs `source_split:180`);
  - the decoder (`decode_source:80` vs `read_source:464`);
  - the slicer (`slice_text:96` vs `_span_text:228`/`render:298`);
  - free names (`symbols_of:142` vs `free_names:282`);
  - reduced imports (`header_text:1046` vs `_reduced_imports:1100`);
  - docstring and `__main__` detection (`is_doc` vs `_is_doc:242`, `_is_guard` vs `_is_main_block:246`).

  Import now: no, because `source_split.py` is in a fix round. A bare queue line is not enough either (rule 19). Proposed node: "TD-11 T-4, one shared reader module for both tools (decode, slice, targets, free names, reduced imports), after source_split's fix round and before wave 2". Owner: the Lead, who opens it. Also, Lead brief «Правки» 10 still says T-3 lives "в том же файле `tools/source_split.py`". The separate-module decision exists only in the snapshot or journal note (`compact-snapshots/2026-11-12-0030-td-11-manual.md:43`). The Lead should write it into the brief with its reason.
- **CODE QUALITY:** T-F2 and T-F3 for T-3. C-F3: `cmd_split_keep` is about 65 lines, acceptable. No uncaught traceback was found in C-F3. T-3 has one (T-F6).
- **ARCHITECTURE:**
  - AR-14: T-3 writes no registry (it prints the row block). split-keep is the one writer, but the two producers disagree on the shim covers (C-B1).
  - AR-20: no ratchet row is touched by either diff (TEST_TIMEOUTS and slow_tests are untouched).
  - AR-22: covered by C-B1.
  - AR-1: no test-file name in either tool's code (T-3 refers to `TESTS_REL` and the harness protocol names `run_scenarios`/`finish`/`harness`; WORLD_HINTS is T-F8).
- **JUDGMENT:** both tools judge data only (AST, names, homes, rows). The homes are the map author's judgment. No census rows are touched.
- **ONE ROAD:** two map-driven code movers (sources vs tests) are justified only if their readers become one (node T-4 above). The exclusion "T-3 not a mode of source_split" needs its carrier (the Lead writes it). Nothing else was found: no branch on a language, project or runner name.
- **Class completeness:** SIBLING_MAP axis 18 is not updated (C-F4). The line-slicing axis is consistent. The T-B2 classes are named with their neighbours swept inside `analyze`/`build_plan` (statement, assignment, import, global, verbatim block).

## Not checked

- Running any real package test or part.
- `scenario_walk --witness-for` on generated parts.
- dup_ratchet and lint_ratchet (`forge-check`'s).
- The loop_b and controller_rework proofs (only infra_failure was re-run; the other two were checked for consistency against spec §3: 422 and 364 check lines, 24 and 45 scenarios).
- C-F3's whole-file 255 (only `-k split` was re-run, plus the full file as a side effect of my probe: 258 = 255 + 3 probes).
- `_write_layers` formatting.

## Trail

- Read:
  - spec `td-11c-test-split.md` (whole), lead brief l.160-249, `critic-diff-brief.md`;
  - `tools/test_split.py` 1-1647 (whole), `tools/test_test_split.py` (whole), report t-050 (whole);
  - the C-F3 `git diff` (whole), `check_history` 1620-1691, the report t-048 (grep of the key lines);
  - `source_split.py` def index;
  - SIBLING_MAP rows 191, 387;
  - `selftest.py` 458-462, 617, 747;
  - `test_probe_by_code.py:1135-1179`, `test_story_run_freshness.py:1345-1380`, `test_no_move_seam.py:1388-1402`, `test_handoff_values.py:80-100, 1600-1625`.
- Reruns:
  - `python -m pytest <T3 wt>/tools/test_test_split.py -q` → `18 passed in 2.16s`.
  - `python -m pytest <CF3 wt>/tools/test_test_quarantine.py -q -k split` → `20 passed, 235 deselected in 11.01s`.
  - infra_failure dry-run on a temp copy, homes from spec 3.1 → `(a) source 244, parts 243 + common 1 + shim 0 = 244 -> ok`, `(b) 52`, `(c) 29 = 29`, `(d) 52`, `(e) 6 files`, `PROOF: ok`.
  - `--draft` on the 15 GROUP 1 files (read-only): rc=2 for no_move_seam (67), freshness (1), handoff_values (215), probe_by_code (13), probe_by_code_languages (5); rc=0 for the other 10, grounding_table included ("0 refused"). Its map is refused anyway (exp 19).
  - Experiments 1-24 on temp fixtures with a stub harness (outputs quoted in the findings above).
  - K5 and split-keep probe in a temp repo → `ON_DISK True RC 0 … 0 violation(s)`; `SHIM_COVERS ['tests/test_k_common.py'] NAMED_BY ['design/state-exits.md:34']`; `NEW_ROW {'layer': 'detector', …}`.
- Negative searches with their controls:
  - `global` in the 15 files: 0 (grep `^\s+global `). There is no positive control file in the set; the absence also agrees with the drafts' "0 unplaced statement(s)".
  - Alias writes in the importers: 0, against `REWORK\.` → 3 in `test_denial_scope.py`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "T-B1 tools/test_split.py:311-327,525,569-572,1037 -- three wave-1 runner shapes refused whatever the map (handoff_values guard of direct calls, no_move_seam for-over-tuple in main, freshness run_scenarios([], chosen)) and grounding_table false-green draft; N2/N3/N5 cannot start; N1/N4/N6 can",
    "T-B2 tools/test_split.py proof green while a check is lost/duplicated or behaviour changes: module-level check homed in common (exp 3,18), nested scenario call in a by-name consumer (exp 24), statement before an import hoisted (exp 1), conditional rebinding across homes (exp 4), late import shadow (exp 5), global rebinding of a common name (exp 9), mutating statement homed apart from its name (exp 15); blocks merging the tool before N8, not N1/N4/N6",
    "C-B1 tools/test_quarantine.py:1479 and tools/test_test_quarantine.py:922 -- shim covers tests/test_<stem>_common.py, T-3 writes <stem>_common.py; fix before NC",
    "C-B2 tools/test_quarantine.py:1656-1667 -- keep-split door accepts parts that are old unrelated keep rows and never checks OLD's tree state (probe: row removed, file on disk, 0 violations); fix before NC"
  ],
  "fixes": [
    "T-F1 rename the tool's (e) compile; print that spec (e) and the reverse-order run are the node's",
    "T-F2 dead or lying code test_split.py:896-898, 287, 980, 1230, 1603; validate_map return value",
    "T-F3 functions over 60 lines: analyze 271-502, build_plan 681-907, prove 1208-1375, render_runner 954-1043, _fill_stmt_block, run_map, run_draft",
    "T-F4 refuse importer writes through the module alias (Store ctx, patch.object, setattr)",
    "T-F5 rollback must not delete targets that existed identical before the run (test_split.py:1526-1534)",
    "T-F6 done_state TypeError traceback on a non-string part (test_split.py:1451)",
    "T-F7 report id t-050 vs task t-053; the freshness claim in report section 6 is false",
    "T-F8 WORLD_HINTS closed list in code: queue as a data row if it grows",
    "T-F9 an argv naming a scenario of another part runs nothing and exits green: name the part or exit nonzero",
    "C-F1 refuse a part not named <OLD stem>_* (optionally without the T-3 part marker)",
    "C-F2 shim row: named_by [] (E4), importers named in why",
    "C-F3 add tests/<common>.py to each part's covers when it exists (spec 4.1 vs 4.2, safe direction)",
    "C-F4 the K5 door is a mechanism: four questions and axis block in the commit; SIBLING_MAP axis 18 row gains split-keep as a keep exit; name the detector"
  ],
  "class_completeness": "SIBLING_MAP axis 18 (keep row exits) not updated by C-F3 (C-F4); line-slicing axis consistent (lone CR refused). T-B2 classes swept across analyze/build_plan neighbours (statement, assignment, import, global, verbatim block). Duplication with source_split.py needs a node (T-4 shared reader, owner Lead), not a bare queue line. The separate-module decision must be written into the Lead brief (Правки item 10 still says same file).",
  "trail": {
    "read": [
      "docs/tasks/specs/td-11c-test-split.md",
      "docs/tasks/specs/td-11-lead-brief.md:160-249",
      "docs/tasks/critic-diff-brief.md",
      ".claude/worktrees/agent-af3a560c41c1247c7/tools/test_split.py",
      ".claude/worktrees/agent-af3a560c41c1247c7/tools/test_test_split.py",
      ".claude/worktrees/agent-af3a560c41c1247c7/docs/tasks/specs/reports/t-050-td11-T-3.md",
      ".claude/worktrees/agent-abc822039ea7c01c8 git diff (tools/test_quarantine.py, tools/test_test_quarantine.py)",
      ".claude/worktrees/agent-abc822039ea7c01c8/tools/test_quarantine.py:1620-1691",
      ".claude/worktrees/agent-abc822039ea7c01c8/docs/tasks/specs/reports/t-048-td11-C-F3.md",
      ".claude/worktrees/agent-a72b9f65526f4b5b4/tools/source_split.py (def index)",
      "docs/SIBLING_MAP.md rows 191, 387",
      "ai-packages/qa-factory/scripts/selftest.py:458-462,617,747",
      "ai-packages/qa-factory/scripts/tests/test_story_run_freshness.py:1345-1380",
      "ai-packages/qa-factory/scripts/tests/test_no_move_seam.py:1388-1402",
      "ai-packages/qa-factory/scripts/tests/test_handoff_values.py:80-100,1600-1625",
      "ai-packages/qa-factory/scripts/tests/test_probe_by_code.py:1135-1179"
    ],
    "reruns": [
      {"command": "python -m pytest <T3 worktree>/tools/test_test_split.py -q", "result": "18 passed in 2.16s"},
      {"command": "python -m pytest <CF3 worktree>/tools/test_test_quarantine.py -q -k split", "result": "20 passed, 235 deselected in 11.01s"},
      {"command": "test_split --map (homes from spec 3.1) --dry-run on a temp copy of test_infra_failure.py", "result": "(a) 244 = 243 + 1 + 0 ok; (b) 52; (c) 29 = 29; (d) 52; (e) 6; PROOF: ok"},
      {"command": "test_split --draft on the 15 GROUP 1 files (read-only)", "result": "rc=2: no_move_seam 67, freshness 1, handoff_values 215, probe_by_code 13, probe_by_code_languages 5; rc=0 for the rest, grounding_table included although every map for it is refused"},
      {"command": "experiments 1-24 on temp fixtures with a stub harness", "result": "PROOF ok with red or duplicated runtime results in exp 1, 3, 4, 5, 9, 15, 18, 24; refused shapes in exp 7, 8, 11, 12, 21, 22, 23"},
      {"command": "K5/split-keep probe in a temp repo (helpers of test_test_quarantine)", "result": "ON_DISK True RC 0 (0 violations); SHIM_COVERS tests/test_k_common.py; unrelated new file accepted as a part with the detector row"}
    ]
  }
}
```
