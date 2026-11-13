# t-286: critic on the PLAN for OH6-1 (spec t-282 + Coordinator decision)

Reviewer: critic (Opus). Date: 13.11.2026. Subject: `docs/tasks/specs/t-282-oh6-1-one-component.md`.
Snapshot read: `.claude/worktrees/oh7-5` at HEAD 4274d7f. That is 0a0db4f plus the OH7-5 commit, which touches only `guard_app_under_test.py`. `origin/main` is now 79c38db, a journal-only commit. `git diff --stat 0a0db4f origin/main -- ai-packages/qa-factory/scripts/` is empty, so the spec's line numbers are still current.

**Verdict: fit_with_fixes.** Do NOT dispatch the spec as written. Its body was drafted before the coordinator's fork decisions, and the decision paragraph (l.259-261) widens the node without carrying that into owns, §2-§7 or the DoD. On top of that, the sentinel as decided (F-4 (a) with `ALLOWED = {}`) is red on main by construction. Fixes 1-4 must land before dispatch. Fixes 5-9 are small edits to the spec text. The coordinator can make all of them as a continuation of t-282: no new designer pass is needed, because no fix changes the architecture.

## What holds (checked, no finding)

- **The nine row sites: line and current error direction.** I read every one in the snapshot and each matches §2.2. `host_dispatch.py:21` returns None. `exit_gate.py:208-209` drops the name from `in_text`. `stage_guard.py:435-437` drops the candidate. `stage_guard.py:643-645` skips the route and falls to `_env_exploration` at :646. `stage_guard.py:716-718` skips the receipt. `activity_capture.py:44` raises ValueError with the same text. `cost_capture.py:1907` calls `sys.exit(0)` before `_session_scope_ok`. `cost_capture.py:3800` returns, after the `metadata` swap at :3794-3798 and before the debounce, the marker and the lock. `recover_codex_usage.py:16` uses single quotes and has no `.`/`..` guard.
- **The survivor** (`hooklib.py:269-272`) and **`is_story_folder`** (`:316-320`, condition at :317-318). The reduction in §2.1 is exactly equivalent. Old: not str, or blank, or edge-blank, or `.`/`..`, or one of `/\:\0`. New: not is_one_component(+NUL), or blank, or edge-blank. `""` is covered on both sides, and a non-str input short-circuits before `.strip()`.
- **The new calls keep every direction.** Row 1: `str(ticket or "")` makes `""` fail the survivor, so the answer is None. Row 4: `env_task` is stripped at :602, so whitespace never arrives. `explore:x` fails the survivor and still reaches `_env_exploration`. Row 5: the `isinstance` test and the truthiness test move inside the survivor. Row 9: `not session` is covered.
- **NUL edge (§4).** Measured on Python 3.12.10: `Path('C:/x')/'a\0b'/'pipeline.json'` gives `is_file()` False and `exists()` False, with no exception. So the "before" cells for sites 2 and 3 hold. After the change the answer moves to refusal at every site, and the error direction is toward refusal only.
- **`""` latent hole (§4).** Sites 2 and 3 do pass `""` today: `"" not in (".","..")` is True and the separator `any` is False, so `root/""/pipeline.json` is probed. This is confirmed by trace.
- **The COPY sentinel regex (Part B), run against the snapshot `scripts/*.py`:** 11 hits. They are the 9 row sites, `hooklib.py:272` and `hooklib.py:318`, and nothing else. Positive controls: `for c in "/\\:"` matches, and `for char in '/\\:'` matches. Negative control: `for c in "/@ \t"` does not match. Reordered `"\\/:"` does not match, which is the blind spot F-4 names. After the change, hooklib keeps exactly one hit (`"/\\:\0"` in `is_one_component`). C-3 is sound.
- **Part A shape.** One table, rows are the callers, and every check id names the caller and the case. The reachability rule plus the spy makes the table proof against mutation. The stated mutation (drop the guard in `recover`) does turn the `..` cell red: with `write=False` and the stubs, `recover` returns the dict instead of raising ValueError.
- **F-1 (a) sites are real copies, and the directions proposed for them are right.** `estimate_record.py:42` has no `:` guard. Measured: `PureWindowsPath('D:/root') / 'C:x'` gives `C:x`, so on Windows a task `C:x` escapes the artifact root today. Wiring it closes a live hole, and the ValueError text is kept. `red_sandbox._component` (:313-315) feeds `_row_problem` :335/:339. The only `pins` keys in `references/sandbox-setup.json` are `package.json` and `package-lock.json`, so no data row changes its answer. `role_digest.file_notes` (:323) has one caller, `exit_gate.py:1201`. Its direction is `""`, which is unchanged, and NUL failed there before only at the write, inside `except (OSError, ValueError)`.
- **F-2, F-3, F-5, F-6, F-7: the decisions are sound.** F-7 (a) is the only reading the brief allows ("do not widen `is_one_component`", batch l.23). F-5 (a) is the PROJECT.md p.2 rule text. F-6 is correctly queued: a degraded coordinator does not write SIBLING_MAP.
- **AR-29 / census.** Every altered check is a shape check. The existing rows are `activity_capture.py::activity_path` (census l.8), `recover_codex_usage.py::recover` (l.678) and `estimate_record.py::task_binding` (l.263, class xref). No unit is created or deleted.
- **Disjointness from in-flight work (item 6).** These branches touch none of the OH6-1 files, nor the F-1 additions, `test_resolver.py` or `test-layers.json`: `wip/oh7-1` (event_store, factory_dashboard, migrate_coverage, test_event_store), `wip/oh7-2` (refusal_registry, judgment-census.json, test_doctor_context), `wip/oh7-34` (native_context), `wip/oh7-5` (guard_app_under_test), `wip/oh5-2a` (brief_pack, guard_pre_tool, refusal_registry, runtime_paths and their tests), `wip/oh5-2b`, and `conv/wave-6`. On `conv/wave-6` the grep for the 14 file names was empty (rc=1), with a positive control: `grep -c scripts/` on the same list gives 11. `wip/oh5-2c`, `wip/oh6-3`, `wip/oh6-4` and `wip/oh6-5` carry no file diff yet. The D-0048 lists for hooklib (`is_one_component`, `is_story_folder`), stage_guard (`story_named_by_text`, `resolve_ticket`, `_recipient_receipts`; the explicit route of F-1 is inside `resolve_ticket`) and cost_capture (`_capture`, `main`, plus one new import line) are complete for the edits the spec describes.

## Fixes (numbered; every one changes the spec text)

**1. (blocking) Fold the Coordinator decision into the body. Today the dispatch header contradicts l.261.**
Trail: header `owns` l.10-18 lists 8 files. `non-goals` l.19 says "no edit of test-layers.json unless fork F-2 is accepted" and "§2.3 NOT touched unless F-1 is accepted". l.261 accepts both. §2.2, §3, §4, §5, §6 (DoD 3 "11 callers × 7 names", DoD 5 witness paths) and §7 do not carry the four F-1 sites or test-layers.json. A Sonnet builder handed this file gets two contradictory scopes.
Change:
(a) `owns:` add the absolute oh6-1 paths of `scripts/estimate_record.py`, `scripts/red_sandbox.py`, `scripts/role_digest.py` and `scripts/tests/test-layers.json`, the last restricted in `non-goals` to "`covers` of the `test_resolver.py` row only".
(b) `non-goals:` delete both "unless" clauses.
(c) §2.2: add rows 10-13. Row 10: `estimate_record.task_binding` :42, ValueError `'task must be a single task identifier'`, new form `if not hooklib.is_one_component(task): raise ValueError(<same>)`, local `import hooklib` beside :41. Row 11: `red_sandbox._component` :313-315, delete the helper and call `hooklib.is_one_component(k)` at :335 and `hooklib.is_one_component(n)` at :339 (`import hooklib` exists at :82). Row 12: `role_digest.file_notes` :323, `if not tail or not hooklib.is_one_component(name): return ""` plus a new `import hooklib` line after :37. Row 13: `stage_guard.resolve_ticket` explicit route :621 (see fix 2).
(d) §1 census table: add `estimate_record.py::task_binding` xref (l.263, unchanged) and "none" for the other three.
(e) §4: one column per new site.
(f) §5: one row each, per fix 2 and fix 6.
(g) DoD 3: the new row count.
(h) DoD 5: the new paths in `--witness-for`.
(i) §7: rows for the three files, none of them hot.
(j) F-2 entry: add the names of the three new files to the `covers` list too.
(k) Because batch 6 is taken (frozen), the zone widening goes as one "Ход" line in `batch-6-ostatki-t-203-i-t-227.md` naming the added paths. Only "Ход" may change, and `piles.py check` (б) reads the node row's "Пишет в", so it is blind to the widening otherwise.

**2. (blocking) The explicit route at `resolve_ticket` has no positional invariant and no test row.**
Trail: `stage_guard.py:612-626`. When `explicit` is non-empty, the function ALWAYS returns. It returns `explicit`, or it records `facts["explicit"]` and `facts["explicit_source"]`, runs `_collect_story_facts` "only to explain", and returns `""`. It never falls through to the resume recipient, the text, the slug, the env variable or the guess. The decision line "explicit not one component -> `""` with facts" names the result but not the position. A builder could write `if explicit and hooklib.is_one_component(explicit):` around the whole block. A refused explicit would then fall through, and the single-story guess or a text key would pick an unrelated story for a dispatch that named a bad one. The event's word would be overruled.
Change, as a §3 row: "explicit route: the survivor joins the `is_file()` condition at :621 (`if hooklib.is_one_component(explicit) and (root / explicit / "pipeline.json").is_file()`). `facts["explicit"]` and `facts["explicit_source"]` are still set (the identity refusal prints them), the explain block still runs, and the answer is `""`. A refused explicit never reaches `_resume_recipient_story`, `story_named_by_text`, the slug, `$QA_FACTORY_TASK` or the guess."
Change, as a §5 row: id `resolve_ticket_explicit`. Event `task_id=name`, exactly ONE story `T` on disk (so a fall-through would answer `T` through the guess), plus the reachability fixture for the creatable bad names. Bad name: `("", facts)` with `facts["explicit"] == name`. Good name: `("T", facts)`. This is the mirror of C-4, which uses two stories so that the guess answers nothing.

**3. (blocking) As decided, the F-4 (a) sentinel is red on main and cannot be green with `ALLOWED = {}`.**
Trail: I ran the patterns with Python `re`, line by line, over the snapshot `scripts/*.py`.
- `!= Path\(\w+\)\.name` hits 3 lines: `event_store.py:482` (deferred by the decision to a node after OH6-3), `role_digest.py:323` (wired by F-1) and `selftest.py:982`. The last is not in the spec at all; see fix 4.
- The "`in x or`" form, as a regex (`['"]/['"] in \w+ or ['"]\\\\['"] in \w+`), hits 9 lines. Only `estimate_record.py:42` is a copy. The other 8 ask "is this a PATH (does it carry a separator)", which is a different question: `assertion_detectors.py:821`, `execution_request.py:573`, `gate_preflight.py:626`, `:640`, `launch_check.py:901`, `planning_contract.py:3941`, `project_env.py:539`, `role_digest.py:179`. As a pair detector it is unscoped. The copy is "a separator test AND a `.`/`..` test on the SAME variable", and the separator half alone matches unrelated checks (critic rule 15).
- The tuple form `for \w+ in \(\s*['"]/['"],\s*['"]\\\\['"]` hits 1 line: `red_sandbox.py:315`. It is specific.
Change to Part B and to F-4 in the decision:
- Patterns: `COPY` (as is), `TUPLE` (the regex above) and `PATH_NAME = r"!= Path\(\w+\)\.name"`. Drop the `in x or` form, and name it, together with `os.path.basename(x) != x`, as a stated blind spot in the sentinel's docstring. The spy table is the detector for those two forms. `basename\(...\) *!=` hits `dependency_drift.py:92` and also `reporters.py:455`, which is not a copy, so the same unscoped-pattern objection applies.
- `ALLOWED = {"event_store.py": 1, "selftest.py": 1}`. Each entry carries the pointer to the finding of fix 4, and the allowance is shrink-only (AR-20).
- DoD 2 and §1 (AR-20 row, "empty after the node") are rewritten to say this.
- Positive controls: each pattern finds a fixture string in the test. For example `name != Path(name).name` and `for sep in ("/", "\\")`, written in the test so that the runtime string carries the backslashes.

**4. (blocking under rule 19 / P31) §2.3 misses two copies. Each is a residual that must be a named node, not silence.**
Trail: search (c) of §2.3 required a `.`/`..` tuple or set, so it could not see copies that lack that guard. Both copies below let `..` through (measured: `Path('..').name == '..'`).
- `selftest.py:982` in `_slow_tests_problem` (def at :964): `if not name or name != Path(name).name:` returns an error string. `..` passes. Note that `selftest.py` sits in the zone of `onboarding-forge/2` (in work; nodes SC2-23 and SC2-26 list it, status ожидает).
- `dependency_drift.py:92` in `load_table` (def at :78): `os.path.basename(row["file"]) != row["file"]` returns `(None, problem)`. `..` passes.
Change: §2.3 table gains both rows. The finding the decision already opens for `event_store.py:482` becomes ONE proposed node, "remaining one-component copies": `event_store.EventStore.__init__` :482 (after OH6-3), `selftest._slow_tests_problem` :982 (queue line vs onboarding-forge/2, or a D-0048 function list), and `dependency_drift.load_table` :92. Its owner is the Lead of onboarding-hooks, filed per D-0044 in the same move as the finding. Opening the node is the coordinator's decision. I only propose it.

**5. The `cost_capture.main` and `recover` rows are under-specified. A builder can produce vacuous cells.**
Trail: `cost_capture.py:3787` returns before the guard unless `_carries_project(project_root(event))` holds. At :3792-3796, when `codex_usage.metadata(tpath)` yields an `id`, that id REPLACES `session_id`, so the bad name never reaches the guard. In `recover_codex_usage.py:19` and `:42`, the code opens and reads the transcript after `scan`.
Change in §5:
- `cost_capture.main` row: "the project carries `qa-factory/config.json`; the transcript is an existing file for which `codex_usage.metadata` returns no `id` (stub `codex_usage.metadata` -> `{}`; the import is local, so patch the module attribute); stub `_choose_subagent_transcript` to a no-op."
- `recover` row: "`transcript` is an existing (empty) file."
The spy column already turns a vacuous cell red, but the spec should not leave the builder to discover that from a red run.

**6. Row ids are not fixed strings, and the mutation id does not match the table.**
Trail: §5 l.143-155 names the rows by `caller` (`recover_codex_usage.recover`, `cost_capture._capture`, `cost_capture.main`), while l.161 expects `OH6-1 recover_codex_usage-dotdot`. `cost_capture-...` would be ambiguous between the two cost rows.
Change: add an "id" column with literal strings: `is_one_component`, `is_story_folder`, `controller_record`, `named_ticket`, `story_named_by_text`, `resolve_ticket_env`, `resolve_ticket_explicit`, `recipient_receipts`, `activity_path`, `cost_capture_capture`, `cost_capture_main`, `recover_codex_usage`, `estimate_record`, `red_sandbox`, `role_digest`. The mutation id becomes `OH6-1 recover_codex_usage-dotdot`, and it then matches.

**7. The spy exemption for `is_story_folder` rests on a false premise.**
Trail: §5 l.159 says `is_story_folder` "calls it by a module-local name", so the spy does not see it. That is wrong. A bare name inside `hooklib` is a global lookup in `hooklib.__dict__`, and `hooklib.is_one_component = spy` rebinds exactly that entry. The spy DOES see the call.
Change: include `is_story_folder` in the spy column, which proves that the reduction of §2.1 was actually made. Keep only `is_one_component` exempt.

**8. Order, branch and worktree.**
Trail: header l.26 says "after OH5-10, OH5-11, OH5-13". In batch 5, OH5-10 (row l.41) and OH5-13 (row l.44) are both still ожидает, while `wip/oh5-11` and `wip/oh3-36` are merged into origin/main (checked with `merge-base --is-ancestor`). Read literally, the order line blocks the dispatch. Read per file, it does not: OH5-10 writes `native_context.py`, and OH5-13 writes `session_identity.py` and `guard_pre_tool.py`, none of which OH6-1 owns.
Change: rewrite l.26 as "per-file order satisfied: OH5-11 and wip/oh3-36 merged; OH5-10 and OH5-13 write no OH6-1 path (rows l.41, l.44)". The handoff names the branch as `wip/oh6-1`, like its siblings `wip/oh6-3`, `wip/oh6-4` and `wip/oh6-5`. It also says which move creates `.claude/worktrees/oh6-1`: the dispatch, after a push (the temporal sub-class of rule 11).

**9. Nit in the edge table (§4, non-str row, site 9).**
"Before: TypeError" holds for an int. For a list or dict id, `any(c in ['x'] ...)` is a legal membership test, so the old copy PASSED it and `recover` returned a dict carrying a list `session_id`. The "after" answer (ValueError) is unchanged. Change: "Before: TypeError for int; a list or dict passed silently."

## Item 5: FR-4 and F-8 (the silent exits)

Accepting F-8 (a) is acceptable, with one condition. The direction "quiet exit" already exists for `/ \ : . ..`, and the brief says to keep directions. The node does widen the quiet class, though: a non-str or NUL id used to leave a visible traceback (FR-4: an informed failure), and after the change it leaves nothing. So the F-8 finding must say "OH6-1 turned a traceback into a silent skip for non-str/NUL session ids". It must also be placed into a non-taken batch in the same move (D-0044), not left as a loose file. Real host ids are UUID strings, so in practice the risk is low. Not blocking.

## Standing questions

- **DUPLICATION AND CONSISTENCY:** The plan reduces duplication: 9 + 4 copies become 1. The remaining duplicates are the 3 of fix 4 (event_store:482, selftest:982, dependency_drift:92). Greps run: COPY, PATH_NAME, TUPLE, IN_OR and BASENAME over `scripts/*.py`, plus the `.`/`..` tuple/set grep, with the hit lists above.
- **CODE QUALITY:** No function grows. `red_sandbox._component` is deleted rather than kept as an alias, per fix 1(c). No quality finding on the plan.
- **ONE ROAD (item 12):** Not met until fix 4: two unlisted copies would stay on their own road with no node. F-3 (story-folder sites ask `is_one_component + is_file` while `is_story_folder` is the leaf of axis 8) is a named finding, which is acceptable as a residual with a node.
- **AR fit:** AR-15 and AR-13 hold after fixes 1, 3 and 4. AR-29: shape only. AR-20: the allowance becomes non-empty and shrink-only (fix 3).

## Class completeness

The class is "a name is one path component", on the surface of the joins that build a story, session or file path from external text. Neighbouring forms walked: the quote and loop-variable form (COPY), the tuple form, the `in x or` form, the `Path(x).name` form, the basename form, and the `.`/`..`-only guard. Stricter allow-lists (`session_identity._component`, `manual_capture.case_dir_name`) are agreed not to be copies. `vcs_evidence.py:407` is agreed not to be a copy. The 8 IN_OR hits are a different class (path vs name). On the map: axis 8 (row queued to the full Lead, F-6), axis 18 (allowance, fix 3) and axis 34 (one road, fix 4).

## Trail

Read in the snapshot: `hooklib.py` :265-275, :300-320; `host_dispatch.py` :15-24; `exit_gate.py` :200-212 and import lines; `stage_guard.py` :78-82, :428-440, :596-650, :700-722; `activity_capture.py` :1-20, :38-60; `cost_capture.py` :60-70, :1890-1925, :3780-3815; `recover_codex_usage.py` :1-70; `estimate_record.py` :34-50; `red_sandbox.py` :300-375 and its hooklib import lines; `role_digest.py` :312-330 and its imports; `event_store.py` :474-488; `selftest.py` :964-990; `dependency_drift.py` :78-96; `manual_capture.py` :288-297; `references/sandbox-setup.json` (pins); `tests/test-layers.json` :4318-4335 and the `quarantine` key at :7004; `tests/fixtures/judgment-census.json` (grep of rows); batch-5 rows OH5-10, OH5-11 and OH5-13; batch-6 (whole head, row OH6-1); batch-7 OH7 rows; onboarding-forge batch-2 rows SC2-23 and SC2-26; the finding file; spec t-282 (whole); `t-254` spec (grep of hooklib, stage_guard and test-layers); journal lines 722-734.
Not opened in full: `architecture.md`, `factory-rules.md`. The AR and FR lines were judged from the auto-loaded indexes and the spec's quotes.
Negative claims and their controls: "COPY hits nothing beyond the 11": the same run finds the 9 known row sites. "No in-flight branch touches the owned files": the same grep pipe counts 11 `scripts/` paths on `conv/wave-6`. "`is_one_component` callers": a grep over `scripts/*.py` found 19 lines, including the known `hooklib.py:269`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "1: Coordinator decision (F-1 a, F-2 a) not folded into owns, non-goals, sections 2-7 and DoD; header contradicts l.261",
    "2: resolve_ticket explicit route (stage_guard.py:621) lacks the positional invariant (refused explicit must return empty, never fall through) and a test row",
    "3: F-4 (a) sentinel red on main: PATH_NAME hits event_store.py:482 and selftest.py:982; the in-x-or form hits 8 non-copies; ALLOWED cannot be empty",
    "4: selftest.py:982 and dependency_drift.py:92 are unlisted copies letting .. through; they need a named node (rule 19, P31)"
  ],
  "fixes": [
    "1: owns gains estimate_record.py, red_sandbox.py, role_digest.py, test-layers.json; rows 10-13 in section 2.2; sections 1, 3, 4, 5, 7 and DoD 3/5 updated; a Ход line in batch-6",
    "2: section 3 row and section 5 row resolve_ticket_explicit with ONE story T; facts explicit kept",
    "3: sentinel = COPY + TUPLE + PATH_NAME; drop in-x-or; ALLOWED event_store.py 1, selftest.py 1 with pointer; DoD 2 and AR-20 row rewritten",
    "4: section 2.3 gains selftest.py:982 and dependency_drift.py:92; one proposed node with event_store.py:482, owner Lead onboarding-hooks",
    "5: cost_capture.main row needs config.json, metadata stubbed to no id, _choose_subagent_transcript no-op; recover row needs an existing transcript",
    "6: literal row-id column; mutation id matches",
    "7: is_story_folder joins the spy column (global lookup sees the spy)",
    "8: order line restated per file; branch wip/oh6-1; worktree created by the dispatch",
    "9: edge table site 9 non-str: list or dict passed before"
  ],
  "class_completeness": "Class: a name is one path component. Forms walked: quote/var, tuple, in-x-or, Path.name, basename, dot-guard. Missing from the spec: selftest.py:982, dependency_drift.py:92; event_store.py:482 deferred. Axis 8 row queued to full Lead, axis 18 allowance, axis 34 one road.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-282-oh6-1-one-component.md",
      "oh7-5 scripts: hooklib.py, host_dispatch.py, exit_gate.py, stage_guard.py, activity_capture.py, cost_capture.py, recover_codex_usage.py, estimate_record.py, red_sandbox.py, role_digest.py, event_store.py, selftest.py, dependency_drift.py, manual_capture.py (cited ranges)",
      "oh7-5 references/sandbox-setup.json; tests/test-layers.json; tests/fixtures/judgment-census.json",
      "oh7-5 plans/piles/onboarding-hooks batch-5, batch-6, batch-7, finding 20261113-kopii; onboarding-forge batch-2",
      "logs/journal/dev1.jsonl lines 722-734"
    ],
    "reruns": [
      {"command": "python re scan of scripts/*.py with the Part B COPY regex", "result": "11 hits: 9 row sites + hooklib.py:272, :318; controls dq/sq True, vcs False, reordered False"},
      {"command": "python re scan, pattern != Path(w+).name", "result": "3 hits: event_store.py:482, role_digest.py:323, selftest.py:982"},
      {"command": "python re scan, in-x-or and tuple and basename forms", "result": "in-x-or 9 hits (1 copy, 8 path checks); tuple 1 (red_sandbox.py:315); basename 2 (dependency_drift.py:92, reporters.py:455)"},
      {"command": "python 3.12.10 pathlib probe", "result": "NUL path is_file False, exists False; PureWindowsPath D:/root / C:x = C:x; Path('..').name == '..'"},
      {"command": "git diff --name-only per in-flight branch (oh7-1, oh7-2, oh7-34, oh7-5, oh5-2a, oh5-2b, conv/wave-6)", "result": "no OH6-1 or F-1 path touched"}
    ]
  }
}
```
