# t-328: critic-on-plan for t-324 (OH8-2a, OH8-2b, OH8-6)

Critic (Opus), 2026-11-13. Spec: `docs/tasks/specs/t-324-oh8-2-oh8-6-spec.md` with the §0a decisions. I read the code at read-main HEAD 2f1cec8. `git diff --stat 303e89e HEAD -- ai-packages/qa-factory/` is empty, so the spec's line anchors hold.

**Verdict: fit_with_fixes.** The architecture is sound: one survivor in `artifacts_dir`, the guard judges the folder the write lands in, and an alias becomes `unknown-task` (a full audit). Four blocking findings need spec edits before any builder starts: B1-B4 below. N1-N6 are non-blocking edits for the same fix round.

## Blocking findings

**B1. F4(a) and A3: `landing_name`'s realpath rule opens a fail-open for a junction story. The surface is `landing_name`.**
- What A3 does: it returns a name only when `realpath(parent/name)`'s parent `samefile`s `parent`. For a story folder that is a junction or symlink, realpath leaves the parent, so A3 returns "". `is_story_folder`'s docstring says such a folder IS a story.
- Empirical probe on this machine (NTFS; junction `root/TJ` -> `elsewhere/TJ`). For each of `TJ`, `tj` and `TJ.`: `lexists` True, "realpath parent == root" False, `samefile(p, root/TJ)` True.
- The failure, traced through guard_pre_tool :1452-1487. A write to `.../artifacts/tj/test-plan.md`:
  - `_path_story` gets "" from `landing_name`, so the key stays `tj`;
  - `artifacts_dir('tj')` raises at step 4 (twin `TJ`), so `controller` is None;
  - the pipeline read raises, so the guard `return`s and **allows** the write. The OS lands it in TJ.
- Today this path reads TJ's controller, so this would be a new regression. An 8.3 name of a junction story also gets past A1 step 5.
- Neighbouring classes on the same surface:
  - case and trailing dot: caught by A1 steps 2 and 4 (in `artifacts_dir`), but NOT by the guard, which asks only `landing_name`;
  - an unlistable root: already named as a residual;
  - realpath raising: covered (returns "").
- **Fix (A3):** `landing_name` = `name` if it is listed. Otherwise, when `lexists(parent/name)`: the first listed `n` with `os.path.samefile(parent/n, parent/name)`. This is `controller._story_names`' own rule. Every error gives "". It costs one stat per entry, only off the exact path.
- Add test cells: an exact-name junction story `TJ`, with `tj` and `TJ.` written by the guard, must be judged as TJ. These cells are `nt`; on POSIX use a symlink.

**B2. Three different compositions of "this key is another spelling of an existing folder" (P31, AR-15, rule 19).**
- A1 uses steps 2, 4 and 5 (shape, `alias_twins`, `landing_name`).
- A13 (F3a) uses only `alias_twins`. An explicit `TP2-24~1`, or an alias of a junction story, therefore still "wins as written" at `exit_gate._identity`. Twenty raw joins then read T's folder: this is exactly what F3 exists to stop.
- `_path_story` (F4a) uses only `landing_name`.
- **Fix:** one hooklib predicate, e.g. `other_spelling(parent, key) -> str`. It returns the existing folder the key reaches under another name: `landing_name` when that is non-empty and differs from the key, else `alias_twins[0]`, else "".
  - A1 steps 4-5 call it.
  - A13 refuses whenever it is non-empty. A13's text in §0 F3(a) and §2 changes to match.
  - `_path_story` uses `landing_name` (the folder the OS writes to).
  - Add an exit_gate cell for the 8.3 name and one for the junction alias.

**B3. Shape rule vs leaf: `is_story_folder` and the new `artifacts_dir` disagree on a trailing dot, and step 2 breaks I2.**
- `is_story_folder` refuses only blanks (`name != name.strip()`; `strip()` does not remove dots, as hooklib:316 reads). On POSIX, an existing exact folder `v1.` is therefore a story to `story_root`. After A6, `story_root` no longer calls `artifacts_dir`, so `story_root('v1.')` returns the path. Then the CLI's `artifacts_dir('v1.')` raises at A1 step 2, which comes BEFORE the exact match (step 3).
- That makes two answers for one key, and I2 ("an exact existing key's answer is unchanged everywhere") is false.
- **Fix:** one shape predicate, e.g. `clean_key`, meaning one component with no blank at either end and no trailing dot or blank. `is_story_folder` and A1 step 2 both call it.
- I2 then names its one exception: an existing folder whose name ends in `.` or a blank is no longer a story on any OS (AR-4). §3 gets that row, and so does the table: an exact `v1.` folder on POSIX is refused by both leaves.
- Alternatively, move step 2 after step 3 and accept the AR-4 residual. Either way the spec must choose; it cannot leave both.

**B4. The cut is disjoint only inside t-324. Nodes of the SAME batch in t-321 overlap it, and no order is declared.** This is CLAUDE.md rule 4 and PROJECT.md «Командная работа» п. 3 / D-0048.
- `test_resolver.py` and the `covers` list of its `test-layers.json` row:
  - OH8-1 owns both (t-321 §A owns; it edits the OH6-1 rows and `oh6_1_sentinel`);
  - 2a and 2b own both too.
- The new `is_one_component` caller sentinel (§5):
  - OH8-1 ADDS three `hooklib.is_one_component` calls (`event_store`, `selftest`, `dependency_drift`), so the initial allow-dict depends on order;
  - if OH8-1 lands second, it must raise a shrink-only ratchet (AR-20).
- `judgment-census.json` has three writers: 2a, OH8-6 (conditional) and OH8-7. t-321 §B.7 asks the later writer to re-measure the dense ceilings; t-324 is silent on this.
- `refusal_registry.py`: t-321 §B.7 states OH8-7's function list. t-324's OH8-6 `owns` does not carry its own list; D-0048 wants it in both dispatches.
- **Fix (§4):**
  - Add `order: OH8-1 -> OH8-2a` (or the reverse, with the sentinel dict named for that world).
  - Write `refusal_registry.py (module docstring, SCOPE paragraph only)` in OH8-6 `owns`.
  - Add a census line: the later writer of 2a, OH8-6 and OH8-7 merges `main` and re-runs `test_judgment_census.py`.

## Non-blocking (same fix round)

- **N1. C6, the money line (key 4).**
  - Today a broken `host_binding` fails the whole capture loudly: `COST CAPTURE INCOMPLETE`, cost_capture:3826.
  - Under C6, `binding = {}`. The child's spend then loses its inherited parent activity, so it drops out of the story's attribution. The cost file looks complete and only stderr says otherwise. The session total is unchanged, but the story price is undercounted silently (P18, FR-41).
  - Fix:
    - write a marker into the cost file's existing `telemetry_coverage`, e.g. `"attribution": "incomplete: host_binding <path> unreadable"`, so the report prints the gap;
    - raise the note through `person_signal` (F5b), not bare stderr: one road for "a broken receipt was skipped" (P31);
    - add a test cell asserting the marker.
  - Neighbour on the same surface (shape): `binding['activity']` that is not a dict, or `segments` empty, still raises at :1949-1950. Guard it, or queue it in §8.
- **N2. C3's edge "broken project config" cannot be reached as written.**
  - `record` calls `resolve_ticket` (host_dispatch:296). That function runs `root = artifact_root(event)` unguarded, so a broken config raises BEFORE C3's block. The §5 cell "a broken config -> receipt written, dispatch_id null, signal" would go red.
  - Fix: either wrap the `resolve_ticket` call in `record` (task "" plus the C3 signal on `ValueError`/`OSError`), or drop the cell and queue the case.
- **N3. Data written before 2a (the temporal world for DATA, not folders).** §3 covers folders only. Existing alias `task_id`s in receipts, leases (execution_scheduler:156), journal tasks (B5) and pipeline `ticket` fields change readers' answers. Examples:
  - worker_lifecycle:210: a stop is denied, because `artifacts_dir` raises and `allowed` becomes None;
  - stage_guard:810: falls into its `except`.
  - Fix:
    - add a §3 row naming each reader's new answer, and its door where it denies;
    - per PROJECT.md package-change item 6(a), measure the premise on real data. One read-only command over the stand's artifact root counting folder name vs `pipeline.json` `ticket`, and receipts' `task_id` vs the listing. Put the result in the spec.
- **N4. Facts (key 1).**
  - "About 90 callers in more than 30 files" is wrong: I measured 78 call lines in 24 production files (grep below).
  - §2 misses these sites:
    - `execution_scheduler.py:156` (`/ str(lease["task"])`);
    - `exit_gate.py:1162` and `:1202` (`_ticket_of`; covered by A13 but not listed);
    - `source_exclusions.py:540` (a path hint only).
  - The spec's AR-15 problem grep `/ (task|ticket|…)\b` is blind to the `/ str(task)` form. Widen it to `/\s*(str\()?[\w\[\]"']*(task|ticket|story|key|name)`.
  - §1 says "resolve steps 1, 2, 4"; §2 A9/A10 say steps 1 and 5. Align them.
  - §8 item 8 can be closed: `host_probe.check_child` is under `except Exception` (:725).
- **N5. `_path_story` must not raise (P1).** Of the 8 sites, :933 sits after a try, while :1237, :1290 and :1304 sit outside any try. `artifact_root(event)` raises `ValueError` on a broken config.
  - State that `_path_story` returns the raw key on any exception.
  - Also note that `landing_name` lists `artifact_root(event)` while `_STORY_RE` matched a literal `/artifacts/` that may lie elsewhere (analog 7). The answer is unchanged from today; name it.
- **N6. Tests (key 6).**
  - Add these names to `OH82_NAMES`: ` T` (a leading blank), `T..`, `T. .`, the junction cells (B1), the exact-POSIX `v1.` cell (B3), the full-width `T` (must pass), and the "`T` and `t` both real" cell from §3.
  - For OH8-6, name the red probe: the same table run on the old `record` must raise in C1-C3, C5 and C6. That is the mutation witness.
- Cost (key 2): measured `os.listdir` of a 60-entry folder here at 44.7 µs. `artifacts_dir` already parses `config.json` on every call through `artifact_root`, so the listing cost is acceptable. Have steps 3-5 share ONE `_listing` call: A2 and A3 each list again, so the create world pays 3x.

## Standing questions

- **DUPLICATION AND CONSISTENCY:** B2 (three compositions of one predicate), B3 (two shape rules) and N1 (stderr vs `person_signal`). A5 removes the `_no_story` duplicate correctly. What I grepped: `_name_alias`, `is_one_component(` and `artifacts_dir(` in `scripts/*.py`.
- **CODE QUALITY:** with B1 fixed, the helpers never raise. Their error directions are stated (§3) and correct, except the guard direction fixed by B1. A6 keeps `story_root`'s near-miss text.
- **ONE ACTION, ONE ROAD (P31):**
  - F2(b) has no OS branch: good.
  - F7 (`_story_names`) answers a different question (collect every spelling, for the veto). It is not blocking. Once B1 makes `landing_name` samefile-based, `_story_names` = `{t: landing_name(root, t) == folder}` gives the same answer with one road. I propose this as a node for the coordinator to open (rule 6), not a requirement of this round.
- **Key 2 (silent pass / traceback):**
  - `guard_app_under_test:66`: `{}` gives "no grant", a refusal. Safe.
  - `inject_context:495`: in a try.
  - worker_lifecycle :94 and :156: exact-equality filters (:193, :257) keep alias receipts out.
  - stage_guard's unguarded sites take `resolve_ticket` tickets, which are exact after A9-A11.
  - I found no silent pass other than B1.
- **Key 3:** with B1 and N5 applied, judging the landing folder is sound at all 8 `_STORY_RE` sites. Door texts name the exact key (FR-2), and the fail-open at :1474-1487 is closed.
- **Key 4:** F3 gives `unknown-task`, a full audit and never a pass, once B2 extends it to 8.3 names and junctions. F5(b) is sound.
- **Key 5:** inside t-324, 2a -> {2b ∥ OH8-6} is disjoint. The refusal_registry function lists (SCOPE docstring vs `_refusal_calls`/`sites`/`raise_family`) are disjoint per t-321 §B.7; see B4 for the missing declarations.

## Trail

Read:
- the spec and the scout digest;
- `hooklib.py`: :255-445, `artifact_root`, `read_json`, `person_signal`;
- `guard_pre_tool.py`: :812-832, :926-960, :1155-1185, :1230-1315, :1440-1500;
- `exit_gate.py`: :195-300, `_ticket_of`, :1155-1165;
- `stage_guard.py`: :425-470, :590-725;
- `host_dispatch.py`: :1-40, :100-120, :225-330;
- `worker_lifecycle.py`: :86-175, :200-262;
- `controller.py`: :7795-7820;
- `cost_capture.py`: :1925-1975, :2250-2265, :3805-3830;
- `activity_capture.py`: :40-66;
- `guard_app_under_test.py`: :50-95, :205-225;
- `archive_task.py`: :188-238;
- `audit_factory.py`: :522-532;
- `env_probe.py`: :738-750;
- `traceability.py`: :1832-1860;
- `execution_scheduler.py`: :145-160;
- `source_exclusions.py`: :525-545;
- `host_probe.py`: :669-726;
- `refusal_registry.py`: :25-62 and its def list;
- `test-layers.json` rows;
- the census rows;
- t-321 §A owns and §B.7;
- the batch-8 file header.

Not read (outside this run): `architecture.md` itself (I used the AR index), `SIBLING_MAP.md` (I took the axis text from the spec), and the tests the spec names (I checked only their layer rows).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1: landing_name realpath rule returns empty for a junction/symlink story, so guard_pre_tool owner check (:1474-1487) falls open for tj and TJ. (empirical probe on NTFS); use samefile over the listing",
    "B2: the alias predicate is composed three ways (A1 steps 2/4/5, A13 alias_twins only, guard landing_name only); A13 misses 8.3 and junction aliases; one other_spelling helper",
    "B3: is_story_folder accepts an exact trailing-dot folder on POSIX while A1 step 2 refuses it before the exact match; I2 false; one clean_key shape predicate or reorder, chosen in the spec",
    "B4: cross-spec overlap with t-321 undeclared: OH8-1 owns test_resolver.py and test-layers covers and adds is_one_component calls that the new sentinel counts; judgment-census.json has three writers; OH8-6 owns lacks its D-0048 function list"
  ],
  "fixes": [
    "A3: landing_name = name if listed, else first listed n with os.path.samefile(parent/n, parent/name) when lexists; every error gives empty; add junction cells",
    "Add hooklib other_spelling(parent, key) used by A1 steps 4-5 and A13; F3(a) refuses whenever it is non-empty; add exit_gate cells for an 8.3 name and a junction alias",
    "One clean_key shape predicate shared by is_story_folder and A1 step 2; I2 names the trailing-dot exception; add an exact POSIX v1. cell",
    "Section 4: order OH8-1 and OH8-2a with the sentinel dict named for that world; OH8-6 owns says refusal_registry.py (module docstring SCOPE paragraph only); the later census writer merges main and re-runs test_judgment_census.py",
    "C6: mark telemetry_coverage attribution incomplete naming the receipt, signal via person_signal, test the marker; guard or queue the binding activity shape neighbour",
    "C3: wrap resolve_ticket in record for a broken config or drop that test cell and queue it",
    "Section 3: add the pre-2a alias DATA row (receipts, leases, journal tasks, pipeline ticket) per reader, and a read-only measurement on the stand per PROJECT.md item 6(a)",
    "Facts: 78 call lines in 24 files, not about 90 in 30+; add rows for execution_scheduler:156, exit_gate:1162 and 1202, source_exclusions:540; widen the problem grep to the str(task) form; align resolve step numbers; close analog 8 (host_probe:725 guards it)",
    "_path_story returns the raw key on any exception from artifact_root",
    "Tests: add leading blank, T.., T. ., full-width T, both-twins cells; name the old-code red probe for the OH8-6 table; share one _listing across A1 steps 3-5"
  ],
  "class_completeness": "Axis 8 (key to folder): A and B rows cover the readers, but the predicate is not yet one survivor (B2, B3) and four join sites are unlisted (N4). Axis 16 and 20 covered by C1-C6. Axis 34 holds once B2 lands. Pre-2a alias data is an uncovered temporal sibling (N3). The F7 convergence onto landing_name is proposed as a node for the coordinator.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-324-oh8-2-oh8-6-spec.md",
      "docs/tasks/specs/reviews/t-323-oh8-2-oh8-6-scout.md",
      "docs/tasks/specs/t-321-oh8-1-oh8-7-specs.md (owns, B.7)",
      "read-main scripts: hooklib.py, guard_pre_tool.py, exit_gate.py, stage_guard.py, host_dispatch.py, worker_lifecycle.py, controller.py, cost_capture.py, activity_capture.py, guard_app_under_test.py, archive_task.py, audit_factory.py, env_probe.py, traceability.py, execution_scheduler.py, source_exclusions.py, host_probe.py, refusal_registry.py",
      "read-main scripts/tests/test-layers.json rows, fixtures/judgment-census.json rows",
      "read-main plans/piles/onboarding-hooks/batch-8-ostatki-t-282-t-254-t-287.md header"
    ],
    "reruns": [
      {"command": "git diff --stat 303e89e HEAD -- ai-packages/qa-factory/ (read-main)", "result": "empty: anchors valid"},
      {"command": "grep -n 'artifacts_dir(' scripts/*.py minus the def, line and file counts", "result": "78 lines, 24 files"},
      {"command": "grep -niE 'artifact_root\\([^)]*\\) */ *(str\\()?[a-z_]+' scripts/*.py", "result": "unlisted: execution_scheduler:156, exit_gate:1162, 1202, source_exclusions:540"},
      {"command": "python timeit os.listdir on 60 dirs (scratchpad)", "result": "44.7 us per call"},
      {"command": "python junction probe root/TJ -> elsewhere/TJ (scratchpad)", "result": "TJ, tj, TJ.: realpath parent == root False; samefile True"},
      {"command": "scenario_walk.py --witness-for <2a six scripts>", "result": "112 distinct test files printed"}
    ]
  }
}
```
