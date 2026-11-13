# t-290: OF4-21 (onboarding-forge/4, П3). `brief_pack` prints story and home paths from the reader, not the literals `qa-factory/artifacts/` and `qa-factory/strategy/`

Draft by designer (t-290) for the Lead. Status: **DRAFT rev 2**, fix round t-306 after critic on plan t-300
(`docs/tasks/specs/reviews/t-300-of4-10-of4-21-plan-review.md`, fit_with_fixes, B4-B6). What changed is in §12. The fork
decisions are in §11 and are unchanged.
Node row: `plans/piles/onboarding-forge/batch-4-hvosty-onbordinga-i-forzha.md:50`. Finding:
`plans/piles/onboarding-forge/findings/20261112-brief-pack-pechataet-literaly-putej-a-ne-nastroennyj-koren.md`.
**Base for the build: origin/main ca2f04a**, read through `C:\QAFactory\forge-repo\.claude\worktrees\read-main`. Wave 6 is merged there (PR #11, OH5-2 A+B on main), so the "after wave 6" precondition is met. The builder works in `C:\QAFactory\forge-repo\.claude\worktrees\of4-21`, which the coordinator creates from origin/main.

## 0. Freshness: what I checked, and how

| Claim | Carrier read | Result |
|---|---|---|
| The literal sites in `brief_pack.py` | Grep tool, pattern `qa-factory/(artifacts\|strategy)`, `-i`, content mode. Rev 1 used `oh7-5` (0a0db4f). **Rev 2 re-ran it on `read-main` (ca2f04a).** | **27 lines at the same numbers** (23 `artifacts`, 4 `strategy`). Positive control of the same shape: `hooklib.py:276`. Critic t-300 Key 1 reproduced it. |
| The wider home literal `qa-factory` in the same file | Grep `qa-factory`, content mode (rev 1) | 35 lines. The 8 lines beyond the 27 are in §2.2. |
| OH5-2 Part A in `brief_pack.py` | ca2f04a (read-main): `:3675` (`command_card_lines`) and `:4260` (`build`) build the card head through `RP.script_command('<script>', must_exist=False)`, and `:69-72` carry the survivor comment and `SCRIPTS` | **On main.** Rows #16 and #23 re-checked: the literals sit at :3674 and :4261, unchanged. |
| Callers of the functions whose shape changes | Grep `command_card_lines\(\|request_lines\(\|\b_rel\(` over `read-main/.../scripts/` **including `tests/`** | `command_card_lines`: `brief_pack.py:3879`, `:4278`, **and keep `tests/test_refusal_registry.py:145`**, which wave 6 added (critic t-300 B4). My rev-1 claim "no caller outside `brief_pack`" is **false** at ca2f04a. `request_lines`: `brief_pack.py:3269`, `user_path_failures.py:1080`, `test_flow_requests.py` ×7 (+1 `flow_request_lines` call at :203), `test_walk_plan_fields.py:229`, `:238`. `_rel`: only `brief_pack`'s own (the other `_rel` hits are other modules' private functions of the same name). |
| `runtime_paths` line windows at ca2f04a | Grep for function definitions | `HOME` :38, `home_dir` :47, `rel_text` :182, `package_root` :229, `script_path` :234, `script_command` :248, **`_admits` :752, `project_for_task` :774**, `_artifact_items` :839 (wave 6 shifted rev 1's :715-799 window; critic t-300 B5) |
| Other given windows at ca2f04a | Grep for function definitions | `hooklib.artifacts_dir` :275, `story_root` :349, `artifact_root` :691. `case_versions.portable_source_path` :57, `read_source_path` :87. `user_path_failures.main` :1065, `story_root` at :1072. `test_brief_pack.seed` :68, **`of3_1c_home_strategy` :2781** (the `endswith` check is at :2795), `main` :2801. `test_refusal_registry.py` :138-151 (the card-head block). |
| Dependency "after OH5-9 and OF3-1 c" | journal `:440`, `:633`; main content | both landed (§11 Q1) |
| Test layers | `test-layers.json` (rev 1, re-confirmed by critic t-300 at ca2f04a) | keep: `test_brief_pack`, `test_runtime_paths`, `test_flow_requests`, `test_walk_plan_fields`, `test_refusal_registry` (layer row :4254 per critic), `test_story_step_start`. quarantine: `test_brief_pack_roles`, `test_brief_pack_manual`, `test_exploration_perturbations`, `test_project_approach`, `test_walk_brief`. |
| Finding item 2: "the test at :2791 protects the wrong text, and the fix will make it red" | `test_brief_pack.py:2781-2798` (ca2f04a) | **Contradiction**: the check is `line.endswith(f" {home}-profile.md")`, so it stays green. Row T4 tightens it. |

## 1. Intent, rules and invariants touched

Intent (Lead brief): every path `brief_pack` prints to a role is built from the reader that says where the file is.
For a story file the reader is the story folder resolved through `hooklib.artifact_root` / `story_root`. For a home
file it is `runtime_paths.home_dir` / `RP.HOME`. The literals `qa-factory/artifacts/` and `qa-factory/strategy/`
never appear in text a role reads (FR-37).

### AR-n touched, with the change check each demands (copied into the DoD)

| AR | How this node touches it | Change check (DoD) |
|---|---|---|
| **AR-13**: a fact with a reader is read only through it | "where this story lives" has the reader `hooklib.artifact_root` (through `story_root`); `build` holds its answer as `task_root`, and 23 lines respell it by hand. "Where the home's strategy folder is" has `RP.home_dir`. The `source_path` of a case link has `case_versions.read_source_path` (F4). | Grep `brief_pack.py` for `qa-factory/(artifacts\|strategy)` (`-i`, content), positive control `hooklib.py:276`: **0 hits**, both outputs pasted. Every site calls the survivor or reader named in §2. |
| **AR-4**: a printed path is relative to the project root, resolved through `runtime_paths` | the printed story path becomes "the resolved story folder relative to the story's project", computed in `runtime_paths` | rows T1-T8 |
| **AR-15**: one survivor, wired everywhere (axis 8) | the survivor `runtime_paths.story_text(task_root, rel="")`; 19 sites in `brief_pack` call it; the twins in other modules go to OF4-21b | every site listed (§2). Commit line: `architecture: AR-15 -- survivor added, axis-8 row queued to Lead`. |
| **AR-20**: shrink-only ratchets | no `references/` text changes; `process_ratchet_tokens` untouched | no row is raised |
| **AR-24 / B-231** (the person's exclusion reaches what acts on it) | the parser site #5 decides whether an excluded file is handed on | E14, E17, rows T6, T6b |
| **AR-29**: code judges data | **no check is added or altered**; `project_for_task` is reused in a new role (§3.1 states its error direction for printing AND for parsing) | `test_judgment_census.py` green, census unchanged |

### Checks this node adds or alters: owner and census class (AR-29, P27)

| Check | Owner it serves | Census class | Census row |
|---|---|---|---|
| none added or altered. `plan_dispatch_lines` (census `judgment-census.json:55`, `shape`, `data`) only changes the first argument of its `_rel` calls. | data (code), unchanged | unchanged | unchanged |
| the T rows in keep `test_brief_pack.py` and the `story_text` table in keep `test_runtime_paths.py` | data | n/a (tests are not units) | none |

FR walk the builder writes:
- A: not changed.
- B: "text to a person not changed" (briefs go to roles).
- C: FR-15, FR-14 (the shapes of `request_lines` and `command_card_lines`).
- D: FR-16, FR-58 (expectations from the requirement), FR-59 (unknown project → the true absolute path; a parser errs toward "skip more").
- E: FR-37.
- F: n/a.
- G: FR-30, FR-32, FR-54.

## 2. Census of the literal: every site with its reader replacement (ca2f04a, same numbers as 0a0db4f)

`S(x)` = `RP.story_text(task_root, x)` (§3.1). Kind: **R** = role-read text, **P** = PARSER prefix, **D** = docstring.

### 2.1 The 27 `qa-factory/(artifacts|strategy)` lines

| # | Line | Function (D-0048) | Kind | Today | Replacement |
|---|---|---|---|---|---|
| 1 | :11 | module docstring | D | `-> qa-factory/artifacts/<T>/...` | `-> <artifact root>/<T>/work/briefs/<ID>.md` |
| 2 | :194 | `TOOLING` (scout card) | R | `--output qa-factory/artifacts/<T>/work/sources/...` | `--output <task root>/work/sources/<source id>/mr-<iid>.json` (C1) |
| 3 | :1135 | `_resolve` (task branch) | R | `f"qa-factory/artifacts/{task_root.name}/" + name` | `S(name)`. The branch never reads `_resolve`'s `project` argument (E8). |
| 4 | :1248 | `case_paths` | **P** | literal prefix on `store_provenance.source_path` | prefix `S("") + "/"`, value through `case_versions.read_source_path(link)` (F4). The fallbacks stay (E13, E17). |
| 5 | :1443 | `_excluded_files` | **P** | literal prefix on an excluded `local_ref` | **E17**: `S("") + "/"` OR any `<head>/<task_root.name>/` whose remainder starts with `work/`. Direction: skip more. |
| 6 | :1494 | `source_material` | R | `- qa-factory/artifacts/{task}/{rel} (...)` | `- {S(rel)} (...)` |
| 7 | :1607 | `question_answer_lines` | R | holder literal | `S("/".join(QR.ANSWERS_REL))` |
| 8 | :1758 | `repo_map_for` | R | repo-map path | `S(f"work/briefs/repo-map-{doc['hash']}.md")` |
| 9 | :1783 | `blast_radius_line` | R | `rel = qa-factory/artifacts/{task}/work` | `rel = S("work")` (E9 / F6) |
| 10 | :1852 | `_rel` (private) | R | `f"qa-factory/artifacts/{task}/{name}"` | `_rel(task_root, name) = S(name)`. Callers (all in `brief_pack`, all hold `task_root`): :1883 :1887 :1896 :1906 :1910 :1946 :1954 :2435 :3081 :4250. |
| 11 | :2856 | `APPROACH_ONE_LINE` | R | `documents qa-factory/strategy/` | `{home}` template filled in `approach_forms` (C4) |
| 12 | :2859 | `APPROACH_POINTER` | R | `... qa-factory/strategy/` | the same, at `approach_forms` :2943 :2947 :2950 |
| 13 | :2910 | `_approach_documents` | R | literal beside names listed from `RP.home_dir(project) / "strategy"` | one Path: `folder = RP.home_dir(project) / "strategy"`; names from `folder`; text `folder.relative_to(Path(project)).as_posix() + "/"` |
| 14 | :3206 | `request_lines` | R | REQ list path | `S(UPF.REQ_LIST_FILE)`; signature `request_lines(found, task_root)` (F3 (b)) |
| 15 | :3332 | `exploration_lines` | R | cells side file | `S(f"work/briefs/{name}")` |
| 16 | :3674 | `command_card_lines` | R | `base = f"qa-factory/artifacts/{task}"` (re-checked at ca2f04a; OH5-2's `script_command` head at :3675 is on main) | gains `task_root` (C5). Callers: `brief_pack.py` :3879 and :4278, **and keep `tests/test_refusal_registry.py:145` (B4: owned, call rewritten only)**. `base = S("")`. Keep :3675's `RP.script_command(...)` as is (E16). |
| 17 | :3733 | `walk_brief_lines` | R | app card | `S("work/app-card.md")` |
| 18 | :3747 | `walk_brief_lines` | R | case file | `S(rel)` |
| 19 | :3851 | `first_look_runner_lines` | R | `base` literal | `base = S("")` |
| 20 | :3981 | `_fl_body` | R | first-look record | `S(FIRST_LOOK_FILE)` |
| 21 | :4068 | `build` | R | `brief_rel` (also `"path"` :4503, resumed line :2421) | `S(f"work/briefs/{dispatch_id}.md")` |
| 22 | :4235 | `build` (case lines) | R | case line | `- {S(rel)} (...)` |
| 23 | :4261 | `build` (card head) | R | `` `<task root>` = qa-factory/artifacts/{task} `` (re-checked at ca2f04a; :4260's `script_command` is on main) | `` `<task root>` = {S("")} ``, with :4260 kept |
| 24 | :4327 | `build._text` | R | omitted approach line | `{home}/strategy/` (config.json per F1 (a)) |
| 25 | :4333 | `build._text` | R | files side file | `S(f"work/briefs/{dispatch_id}-files.md")` |
| 26 | :4379 | `build` (`side`) | R | digests | `S(f"work/briefs/{dispatch_id}-digests.md")` |
| 27 | :4380 | `build` (`side`) | R | decisions | `S(f"work/briefs/{dispatch_id}-decisions.md")` |

### 2.2 The rest of the class in the same file (F1 (a): fixed in this node)

| Line | Function | Text | Replacement |
|---|---|---|---|
| :87 | comment | `project:` relative to qa-factory/ | not applicable (comment) |
| :303 | `TOOLING` data | `a finding for qa-factory/factory-backlog.md` | `{home}` form filled where the card lines are emitted (:4275), from `RP.HOME` |
| :1134 | `_resolve` (`project:` branch) | `"qa-factory/" + rel` | `RP.home_dir(project) / rel`, text relative to `project` |
| :2739 | `s4_stand_lines` | `qa-factory/config.json` | home text + `/config.json` |
| :2751 | `S3_ROSTER_FILE` (:2807 :2814 :2818) | `qa-factory/records/project-knowledge.json` | `RP.rel_text("project-knowledge.json", project)` (both worlds) |
| :2855, :2859, :4327 | approach constants and omitted line | `qa-factory/config.json` | the same `{home}` template |
| :2882 | `_approach_test_data` | `- test data: qa-factory/config.json ` | home text |
| :2938 | `approach_forms` | `qa-factory/config.json could not be read` | home text |

## 3. The mechanism

### 3.1 The survivor `runtime_paths.story_text(task_root, rel: str = "") -> str`
1. `root = Path(task_root).resolve()`. On `OSError`/`ValueError`/`RuntimeError`, fall back to `Path(task_root)`.
2. `project = project_for_task(root)` (`runtime_paths.py:774`). Any exception → `None`. `_admits` (:752) already catches `Exception` around `artifact_root`, so whatever exception class OF4-10 chooses, this never raises (critic t-300 Key 2).
3. `head = root.relative_to(project).as_posix()` when `root` is under `project`, else `root.as_posix()` (F5 (a)).
4. `rel` is text, never resolved: backslashes become `/`, a leading `./` is dropped, a trailing `/` is kept, and the result is `head + "/" + rel` (C2).
5. Never raises. No env, no cache, no write.

**Error direction, PRINT sites.** Allowed error: a valid project is rejected, and the absolute path of the same folder is printed (longer, still true). Forbidden error: a path relative to a project that does not contain the story. `_admits` forbids that.

**Error direction, PARSER sites #4/#5 (B6, t-300).** The print fallback is the WRONG prefix for parsing stored text. When `project_for_task` fails, `S("")` is absolute and a stored project-relative ref stops matching. For #5 that turns a match into a leak: an excluded file is handed on. So a parser never takes the print fallback as its only prefix (E17). Its error direction is "skip more" (B-231, AR-24). #4 keeps its fallbacks (E13).

Adversarial inputs (T rows): another copy of the project beside the real one; an absolute root on another drive; a broken config; a markerless folder; an unresolved temp path (8.3, symlink); `rel` with `*` or `<...>`; a ref written under the default root after the root was switched.

### 3.2 The home text
Built from the Path read: `RP.home_dir(project) / <x>` relative to `project`, and `RP.rel_text(name, project)` for records. The constants are `{home}` templates filled at call time (C4).

### 3.3 Call shapes
- `_rel(task_root, name)` (private).
- `command_card_lines(task_root, walk, commands, tail)`. `task` was used only for the base path, so it becomes `task_root`. The builder confirms no other use of `task` in its body. If there is one, it keeps both arguments and lists the shape.
- `request_lines(found, task_root)` (F3 (b)).

Callers outside `brief_pack` (B4) are rewritten in the owned files: `user_path_failures.py:1080` (`task_root` from :1072), `test_flow_requests.py`, `test_walk_plan_fields.py`, and `test_refusal_registry.py:145`.

## 4. Edges, each with the invariant it protects

| Id | Edge | Behaviour | Invariant protected |
|---|---|---|---|
| E1 | **default root** | every line byte-identical to today | the default user sees no change. Keep tests that pin today's text stay green: `test_brief_pack_s5_plan`, `test_first_look_briefs`, `test_walk_plan_fields`, `test_flow_requests` and `test_story_step_start` **are run explicitly in the DoD** (N3, t-300), because `--witness-for` may not print them. |
| E2 | configured relative root `"stories"` | `stories/<T>/...` everywhere | FR-37 |
| E3 | root that climbs out or is absolute | absolute posix path, never `../` | the path resolves from any cwd (F5 (a)) |
| E4 | broken config while `build` runs | `story_root` → `artifact_root` raises before any text exists; `build` raises as today; `story_step` prints its note | AR-28 / FR-59: an unknown root never becomes the default literal |
| E4b | `project_for_task` raises at helper level (markerless folder, config broken after `build` started) | PRINT sites: the absolute posix path of the folder given. PARSER sites: E17. | the text names a real folder; a parser never leaks |
| E5 | Windows separators (`stories\qa`) | forward slashes only; on POSIX a backslash is part of a folder name, printed as the writer made it | one separator spelling; the printed path names the folder the writer created |
| E6 | case / 8.3 / symlink | both sides `resolve()`d; `relative_to` folds case on Windows | no false absolute path |
| E7 | `rel` with a glob or placeholder | appended as text | no OS error; the glob lines keep their format |
| E8 | `_bundle_view` passes `task_root` as `project` (:1151) | the task branch ignores that argument | positional: the story's own project |
| E9 | the 300-char blast cap | F6 (a): the cap applies to the reason only | a path is never cut |
| E10 | the 200-byte approach pin and the 300-char cut | default bytes unchanged; the folder precedes the names | pinned budget kept |
| E11 | the 6 KB brief ceiling | the existing trimming order; every trim named in `Not in the brief` | no silent trim |
| E12 | temporal: the survivor is new | it lands in one commit with every rewrite and its test row | no import of a missing function |
| E13 | `case_paths`: a `source_path` stored under the default root, read after `artifact_root` was switched | the prefix may not match; the fallbacks (`link["path"]`, the `contract.case_files` search) find the file | a case is never lost while a fallback finds it |
| E14 | `_excluded_files`: a story-prefixed `local_ref` under a configured root | recognised and skipped | B-231 |
| E15 | `RP.HOME = "elsewhere-home"` | the strategy line names `elsewhere-home/strategy/` | folder and names from one Path |
| E16 | OH5-2's lines (:3675, :4260, now on main) | keep `RP.script_command('<script>', must_exist=False)`; change only the `<task root>` value | the card's one quoting road (P31) |
| E17 | parser fallback (B6, t-300) | E17 (B6, t-300): the parser sites #4/#5 do not take the print fallback as their only prefix. `_excluded_files` recognises a story-prefixed `local_ref` when it starts with `S("") + "/"` OR with any `<head>/<task_root.name>/` whose remainder starts with `work/`; the error direction is "skip more" (an excluded file is never handed on; B-231, AR-24). `case_paths` keeps its fallbacks (E13). | B-231 / AR-24: an excluded file is never handed on, whether the project is unknown or the root was switched after the ref was written |

Conflicting requirement pairs:
- (a) "default byte-identical" vs "absolute without a project": resolved by E1/E4b. The quarantined `test_exploration_perturbations.py` T2 pin changes; it is listed, not edited.
- (b) `request_lines` external callers vs one road: F3 (b), callers owned.
- (c) one survivor vs SIBLING_MAP being the Lead's: the axis row is queued.
- (d) print fallback vs parser safety: E17.

## 5. Tests: table rows only, no new test file

Rows of one table function in keep `scripts/tests/test_brief_pack.py`, plus one table in keep `scripts/tests/test_runtime_paths.py`. Expectations come from "the printed path, joined to the project, is the folder the writer resolves" (FR-58).

**`test_brief_pack.py`, table `of4_21_paths_follow_the_reader` (beside `of3_1c_home_strategy` :2781):**

| Row id | World | Checked |
|---|---|---|
| T1 default | `harness.temp_project`, story `qa-factory/artifacts/QA-9`; S5 automator, S6 walk and S3 strategist briefs via `build(..., write=False)` | key lines byte-identical: the card head `` `<task root>` = qa-factory/artifacts/QA-9 ``, a case line, the side files, the blast line |
| T2 configured | plus `artifact_root: "stories"` | no `qa-factory/artifacts` in the three briefs; every `stories/QA-9/...` path, joined to the project, lies inside `hooklib.artifact_root(root=project) / "QA-9"`; the card head names `stories/QA-9` |
| T3 outside | absolute temp root outside the project | the card head names that absolute folder; no `../`, no literal |
| T4 home | `RP.HOME = "elsewhere-home"` (the loop at :2785-2795) | the line contains `elsewhere-home/strategy/ elsewhere-home-profile.md` and not `qa-factory/strategy/` (rewrites :2794-2795) |
| T5 windows | `artifact_root: "stories\\qa"` | no `\` in a printed story path; on Windows the head reads `stories/qa/QA-9`; on POSIX `Path(project, shown).resolve() == task_root.resolve()` |
| T6 excluded | configured root, excluded item `local_ref: "stories/QA-9/work/sources/S1/mr-1.json"`, file on disk | `source_material` does not list it |
| T6b excluded, fallback | Row T6b: a markerless story (no `qa-factory/config.json` above it) and a configured-root story whose item has `local_ref: "qa-factory/artifacts/QA-9/work/sources/S1/mr-1.json"` with that file on disk under the story | `source_material` does not list it in either world |
| T7 case link | configured root, `source_path` `stories/QA-9/work/test-cases/a/TC-001.md`, and a `link["path"]` that points elsewhere | `case_paths` returns `work/test-cases/a/TC-001.md` |
| T8 no project | bare folder, `exploration_lines(task_root, ...)` | absolute posix folder, no literal |
| T9 blast limit | a long absolute root | head and tail paths whole (F6 (a)) |

**`test_runtime_paths.py`, table for `story_text`:**
- E1 default, E2 configured, E3 absolute other drive (skipped where there is no second drive; the row says why).
- E4b no marker → absolute; broken config → absolute.
- E5 backslash value, E6 unresolved temp path, E7 `rel` with `*` and with `<x>`, trailing slash kept.
- non-ASCII root `stories/Анна`, kept verbatim.
- Each row checks the exact text.

Adversarial battery: an empty or blank value is the writer's refusal (E4). Magnitude is T9. Encoding is the non-ASCII row.

## 6. Siblings: other scripts that print the same literals (not fixed in this node)

Command (rev 1, 0a0db4f): Grep `qa-factory/(artifacts|strategy)`, count, `*.py`, over the package's `scripts/`. It found 550 hits in 207 files, tests included.

Non-test scripts besides `brief_pack.py`: `app_card` 2, `artifact_producer` 1, `audit_factory` 2, `check_coverage` 3,
`check_delivery` 1, `config_contract` 2, `collect_gaps` 1, `controller` 1, `check_traceability` 1, `critic_rollcall` 2,
`cost_capture` 4, `driver_dispatch` 5, `driver_dialog` 1, `driver_stage_plan` 1, `driver_gates` 3, `driver_sources` 7,
`driver_stage_s7` 3, `driver_machine` 6, `driver_timing` 1, `driver_stage_s5` 1, `driver_stage_s8s9` 2, `exit_gate` 1,
`factory_dashboard` 1, `gate_brief` 1, `form_selftest` 2, `guard_pre_tool` 5, `hooklib` 1, `interim_packet` 1,
`investigation_probe` 1, `judge_cases` 1, `judge_code` 2, `judge_diff` 1, `judge_plan` 1, `judge_requirements` 1,
`judge_results` 2, `judge_sources` 1, `launch_card` 1, `judge_run` 2, `manual_capture` 4, `ledger` 1, `plan_row` 1,
`onboard_apply` 1, `planning_contract` 1, `project_gitignore` 1, `project_decisions` 1, `postcompact_reload` 1,
`readiness` 1, `red_sandbox` 2, `refusal_registry` 1, `repo_map` 1, `runtime_probe` 1, `s5_precheck` 2,
`source_exclusions` 1, `run_suite` 1, `s5_plan` 1, `sizing` 1, `stand_identity` 1, `stage_done` 1, `stage_guard` 4,
`story_progress` 1, `story_run` 1, `story_step` 4, `test_repo_base` 1, `ticket_adapter` 3, `validate_artifacts` 4,
`window_files` 1, `vcs_evidence` 4, `walk_timing` 1, `walk_session` 1.

Read and classified (the residual node OF4-21b's list):
- `story_step.py` :252 `_prompt`, :316 `_project_rel` (callers :372 :451 :1141 :1187 :1200 :1306 :3108 :3121), :546, :652. These print in the same packet as the brief (FR-10, F7).
- Driver lines: `driver_sources` :74 :145 :311 :356 :427 :701 :721; `driver_dispatch` :2379 :3826 :3867 :3910 :3950; `driver_gates` :133 :156 :720; `driver_machine` :1054 :1708 :1714 :1727 :1730 :1955; `driver_stage_s7` :699 :996 :997.
- Refusal or help texts: `manual_capture` :284 :774 :5461 :5500; `ticket_adapter` :1480 :2438 :2612; `guard_pre_tool` :1634 :2241; `vcs_evidence` :646.
- Parsers: `cost_capture:939`, `validate_artifacts` :1830 :2631, `stage_guard:1215`, `check_coverage:249`.
- Hand twins of the survivor: `controller._output_rel` :9725, `config_contract._display` :2619, `stage_done._story_rel` :622, `launch_card.card_rel` :48, `stand_identity.confirmations_rel` :123.
- `hooklib.artifact_root`'s own `project / "qa-factory"` (:694, :702). OF4-10 edits that function but owns no `runtime_paths` import, so this goes to OF4-21b's list (N5, t-300).

SIBLING_MAP axis 8: `story_text` is its new row (queued to the Lead).

## 7. The builder dispatch (draft for the Lead; header lines per R11-f)

worktree: C:\QAFactory\forge-repo\.claude\worktrees\of4-21 (created by the coordinator from origin/main; every path below is under it; the line windows are current on origin/main ca2f04a)
given: this spec §0-§6; C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\design\factory-rules.md (whole); C:\QAFactory\forge-repo\.claude\worktrees\of4-21\plans\builder-rules.md; C:\QAFactory\forge-repo\.claude\worktrees\of4-21\docs\TESTING.md; C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\brief_pack.py (the 27 lines of §2.1 and the lines of §2.2); C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\runtime_paths.py (:38-260, :750-835) at origin/main ca2f04a (B5, t-300); C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\hooklib.py (:275-390, :691-706; read only); C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\case_versions.py (:57-98; read only); C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\user_path_failures.py (:1065-1085); C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\tests\test_brief_pack.py (:68-74 `seed`, :2781-2798 `of3_1c_home_strategy`); C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\tests\test_runtime_paths.py; C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\tests\test_flow_requests.py (:33, :180-230); C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\tests\test_walk_plan_fields.py (:225-240); C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\tests\test_refusal_registry.py (:138-151); C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\tests\harness.py (`mark_project`, `temp_project`, `use_project`)
owns:
C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\brief_pack.py
C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\tests\test_brief_pack.py
C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\runtime_paths.py
C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\tests\test_runtime_paths.py
C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\user_path_failures.py
C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\tests\test_flow_requests.py
C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\tests\test_walk_plan_fields.py
C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\tests\test_refusal_registry.py (only the `command_card_lines` call at :145, given a `task_root` built under a `harness.mark_project` project; nothing else in the file)
functions (D-0048):
- `brief_pack`: `_resolve`, `case_paths`, `_excluded_files`, `source_material`, `question_answer_lines`, `repo_map_for`, `blast_radius_line`, `_rel`, `plan_dispatch_lines`, `plan_lines`, `delta_lines`, `fit_target_lines`, `_approach_documents`, `_approach_test_data`, `approach_forms`, `s4_stand_lines`, `s3_roster_lines`, `request_lines`, `flow_request_lines`, `exploration_lines`, `command_card_lines`, `walk_brief_lines`, `first_look_runner_lines`, `_fl_body`, `build`, and the constants `TOOLING` (:194, :303), `APPROACH_ONE_LINE`, `APPROACH_POINTER`, `S3_ROSTER_FILE`.
- `runtime_paths`: new `story_text`.
- `user_path_failures`: `main`.
- tests: the call sites named in owns.
(OH5-2 is on main, so it imposes no order.)
non-goals: no file of §6 (residual node OF4-21b); no edit of hooklib.py; no change to what any path resolves to (spelling only); no new test file; no edit of a quarantined test file (`test_brief_pack_roles.py`, `test_brief_pack_manual.py`, `test_exploration_perturbations.py`, `test_project_approach.py`, `test_walk_brief.py`); in `test_refusal_registry.py` nothing but the :145 call; no cache in `story_text`; no SIBLING_MAP edit; no `references/` text
handoff: builder report (`.claude/agents/builder.md` rule 7). It carries:
- the diff;
- the FR walk A-G;
- the AR lines of §1;
- the per-site table of §2 with each site's new call;
- the pre-build caller grep output;
- the verbatim witness;
- the Grep 0-hit proof with its positive control;
- the quarantined pins expected to go red (`test_brief_pack_roles.py:110`, `test_exploration_perturbations.py:88` and `:340`, and any `test_project_approach.py` / `test_brief_pack_manual.py` / `test_walk_brief.py` pin noticed);
- the wall time of `test_brief_pack.py` before and after;
- "needed beyond the manifest".
edges: E1-E17 of §4 (default byte-identical; configured; outside/absolute; reader raises at build and at helper level; Windows separators; case/8.3/symlink; glob/placeholder rel; `_bundle_view` stand-in project; 300-char blast cap; 200-byte approach pin; 6 KB ceiling; temporal survivor; stale source_path; B-231 exclusion; RP.HOME; OH5-2 lines; parser fallback skip-more)
DoD:
(0) Before the build the builder greps `command_card_lines(\|request_lines(\|_rel(` over `scripts/` INCLUDING `tests/` (positive control: `brief_pack.py:3671 def command_card_lines`) and returns any further caller as a question.
(1) Every site of §2.1 and §2.2 builds its path as the replacement column says.
(2) A Grep, `-i`, content mode, of `qa-factory/(artifacts|strategy)` over `scripts/brief_pack.py` gives 0 hits; the same Grep finds `scripts/hooklib.py:276` as the positive control; both outputs pasted.
(3) Rows T1-T9 (with T6b) of §5 and the `story_text` table pass; T1 asserts today's text byte for byte.
(4) `test_flow_requests.py` and `test_walk_plan_fields.py` are green on `request_lines(found, task_root)`.
(5) `python -B C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\tests\test_refusal_registry.py` is green, named explicitly because its `covers` does not list brief_pack.py (B4, t-300).
(6) The keep files of E1 run explicitly as `python -B C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\tests\<file>.py` for `test_brief_pack_s5_plan`, `test_first_look_briefs` and `test_story_step_start` (N3, t-300), plus `test_judgment_census.py`.
DoD verification run: `python -B C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for ai-packages/qa-factory/scripts/brief_pack.py ai-packages/qa-factory/scripts/tests/test_brief_pack.py ai-packages/qa-factory/scripts/runtime_paths.py ai-packages/qa-factory/scripts/tests/test_runtime_paths.py ai-packages/qa-factory/scripts/user_path_failures.py ai-packages/qa-factory/scripts/tests/test_flow_requests.py ai-packages/qa-factory/scripts/tests/test_walk_plan_fields.py ai-packages/qa-factory/scripts/tests/test_refusal_registry.py`, then each printed non-quarantined file as `python -B <wt>\ai-packages\qa-factory\scripts\tests\<file>.py`, plus the files of (5) and (6) not already printed. Everything pasted verbatim.
siblings: §6 list, not fixed here; report any further hand spelling of a story or home path in `brief_pack.py`.
designer: C:\QAFactory\forge-repo\docs\tasks\specs\t-290-of4-21-brief-pack-paths.md

## 8. Forks (returned in rev 1; decided in §11, unchanged)

- **F1: scope inside `brief_pack.py`.** (a) Fix the 8 home literals too, or (b) only the 27. Rec (a).
- **F2: where the helper lives.** (a) The survivor `runtime_paths.story_text`, axis 8, or (b) brief_pack-local. Rec (a).
- **F3: `request_lines` external callers.** (a) A `task_root=None` legacy road, or (b) the one road `request_lines(found, task_root)` with its callers owned. Rec (b).
- **F4: `case_paths` reads `source_path` raw.** (a) Through `case_versions.read_source_path`, or (b) the prefix only. Rec (a).
- **F5: story folder outside the project.** (a) Absolute posix, (b) relpath with `..`, or (c) a placeholder. Rec (a); the AR-4 text is an owner question.
- **F6: the 300-char blast cap.** (a) The cap applies to the reason only, (b) drop the tail first, or (c) keep the cut. Rec (a).
- **F7: story_step's half of the packet.** (a) A residual node OF4-21b (story_step `_prompt`/`_project_rel`/:546/:652, the driver lines and refusal texts of §6, the parsers `cost_capture:939`, `validate_artifacts` :1830 :2631, `stage_guard:1215`, `check_coverage:249`, the 5 twins folded into `story_text`, and `hooklib.artifact_root`'s home literal). Its test: T2's world extended to `story_step start`. Its carrier: a findings file, a batch row and a README row written at this node's acceptance. Or (b) widen this node. Rec (a).
  **Follow-on order (critic t-300 Key 5):** OF4-21b's batch row carries `очередь: OF4-10 → OF4-21b`, because both edit `vcs_evidence.left_out_by_person` (OF4-21b's `vcs_evidence.py:646`).

### Questions (not forks)
- Q1: OH5-9: answered in §11.
- Q2: resolved by the fix round. Wave 6 is on main (ca2f04a), and rows #16 and #23 were re-checked there (§0).

## 9. Small technical choices I closed
- C1: :194 uses the card's `<task root>` placeholder.
- C2: `rel` in `story_text` is text, never resolved; a trailing `/` is kept.
- C3: no cache in `story_text`. The builder reports `test_brief_pack.py` wall time before and after; about 25 `project_for_task` calls per brief (N4, t-300). A cache is a later node if the cost shows.
- C4: the approach constants (and the :303 card line) become `{home}` templates filled at call time.
- C5: `command_card_lines` takes `task_root` in place of `task`. **Correction (B4): it is not internal-only.** Keep `test_refusal_registry.py:145` calls it and is owned for that one call.
- C6: docstring :11 aligned; comment :87 left.

## 10. Reading trail
- Rev 1 (0a0db4f via `oh7-5`, and `oh5-2a`): see rev 1's list, unchanged in substance:
  - `brief_pack.py` windows: :1-120, :160-197, :1100-1260, :1430-1500, :1595-1610, :1740-1790, :1840-1860, :2730-2790, :2840-2950, :3196-3210, :3318-3337, :3660-3760, :3840-3860, :3972-3985, :4050-4140, :4225-4270, :4318-4387;
  - `runtime_paths`, `hooklib`, `case_versions`, `user_path_failures`, `story_step` :245-319;
  - tests `test_brief_pack`, `test-layers.json`, `test_exploration_perturbations`, `test_flow_requests`, `test_first_look_briefs`, `harness`;
  - `architecture.md` :69-80, :161-188; `SIBLING_MAP.md` :202-226; the journal.
- Rev 2 (fix round t-306, ca2f04a via `read-main`):
  - the critic review t-300 (whole);
  - in `read-main/ai-packages/qa-factory/scripts/`: the literal Grep on `brief_pack.py` (27 lines; :3675 and :4260 carry `script_command`); the caller Grep `command_card_lines\(|request_lines\(|\b_rel\(` including `tests/`; definition Greps in `runtime_paths.py`, `hooklib.py`, `case_versions.py`, `user_path_failures.py`, `tests/test_brief_pack.py`; `tests/test_refusal_registry.py` :136-151.

## 11. Coordinator decision (Opus coordinator, degraded window, 2026-11-13; по рекомендации, до слова владельца)

- **Forks:** every fork takes the recommendation:
  - F1 (a)
  - F2 (a): the `runtime_paths.story_text` axis 8 row goes to the full Lead queue
  - F3 (b)
  - F4 (a)
  - F5 (a): whether AR-4's text should name an outside-the-project root is an owner question in the morning report
  - F6 (a)
  - F7 (a): OF4-21b is a residual node; its finding, batch row and README row are written at this node's acceptance
- **F1 (a) and the quarantined `test_project_approach.py`:** its pins that go red are not named in the DoD, since quarantined files are never in a DoD. The builder lists them in the report, and the quarantine watch sees them.
- **Q1:** OH5-9 landed (journal and `brief_pack.py:295`). The batch-5 row status is a coordinator doc line for the next doc batch.
- **Q2:** the build starts after wave 6 (OH5-2 A+B) is merged to main. The builder re-checks §2 rows #16 and #23 against main at that point.
- **Critic on plan:** corrected at 06:40. The spec carries forks and serves as the spec for more than 30 minutes of work, so rule 3 owes a critic on the plan, and the earlier "skipped" was a coordinator error. One critic pass covers this spec and t-289 (OF4-10) together as one topic. The diff critic is still mandatory.

## 12. Fix round t-306 (critic on plan t-300)

| Item | Status | How |
|---|---|---|
| B4: keep `test_refusal_registry.py:145` calls `command_card_lines` with the old shape | applied | Critic fix line verbatim: the owns line for `test_refusal_registry.py` (only the :145 call, `task_root` under `harness.mark_project`); DoD (5) names its run explicitly; DoD (0) is the pre-build grep with the positive control `brief_pack.py:3671`. §0 marks the rev-1 "no outside caller" claim false. §2 #16, §3.3 and C5 are corrected. |
| B5: relative verification command, stale windows | applied | Critic fix line verbatim as the DoD verification run (absolute worktree `scenario_walk.py`, repo-relative `--witness-for` paths, plus `test_refusal_registry.py`). Every printed file runs as `python -B <wt>\...`. A `worktree:` header line names `C:\QAFactory\forge-repo\.claude\worktrees\of4-21`. given: `runtime_paths.py (:38-260, :750-835)` at ca2f04a. The other windows were re-checked at ca2f04a: `test_brief_pack` moves to :2781-2798, and `test_refusal_registry` :138-151 is added. |
| B6: parser sites inherit the print fallback | applied | Critic fix line verbatim as E17 (§4) and row T6b (§5). §3.1 gains the PARSER error direction. §2 #4/#5 point to E17. AR-24 joins the §1 table. |
| N3: `test_story_step_start` claimed green but not run | applied | E1 now says the E1 keep files run explicitly; DoD (6) names `test_brief_pack_s5_plan`, `test_first_look_briefs`, `test_story_step_start` (with `test_flow_requests` and `test_walk_plan_fields` already in the witness list). |
| N4: about 25 `project_for_task` calls per brief | applied (note) | C3 cites it; the wall-time report stays in the handoff. No cache (C3 unchanged). |
| N5: `hooklib.artifact_root`'s own home literal goes to OF4-21b | applied | §6 last bullet and F7's OF4-21b list |
| N1, N2, N6 | not applicable to t-290 | N1 and N2 concern t-289 (OF4-10). N6 (diverged local main) is the coordinator's environment item; this spec now names only absolute worktree paths (B5). |
| Key 5 follow-on: OF4-21b after OF4-10 | applied | F7 carries `очередь: OF4-10 → OF4-21b` (both edit `vcs_evidence.left_out_by_person`) |
| Re-check rows #16 and #23 at ca2f04a | applied | §0 and §2: the literals are still at :3674 and :4261; OH5-2's `script_command` heads at :3675 and :4260 are on main |
| §11 fork decisions | unchanged | §8 is shortened to a summary of the same forks and recommendations; no decision is altered |
| Not done | — | I have no shell, so I did not re-run the rev-1 package-wide sibling count (§6) at ca2f04a. Critic t-300 says the c97dd95..ca2f04a package diff touches none of the §6 sibling files, so the list holds (estimate on the critic's trail). |
