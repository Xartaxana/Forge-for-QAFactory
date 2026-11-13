# t-290: OF4-21 (onboarding-forge/4, П3). `brief_pack` prints story and home paths from the reader, not the literals `qa-factory/artifacts/` and `qa-factory/strategy/`

Draft by designer (t-290) for the Lead. Status: DRAFT rev 1. Forks are in §8. None is decided here.
Node row: `plans/piles/onboarding-forge/batch-4-hvosty-onbordinga-i-forzha.md:50` (origin/main 0a0db4f, read in
`.claude/worktrees/oh7-5`). Finding: `plans/piles/onboarding-forge/findings/20261112-brief-pack-pechataet-literaly-putej-a-ne-nastroennyj-koren.md`.
Base: main 0a0db4f plus OH5-2 Part A (`wip/oh5-2a`, being integrated on `conv/wave-6`). The builder starts after wave 6
merges. See §0 for how I read the OH5-2 diff without a shell.

## 0. Freshness: what I checked, and how

| Claim | Carrier read | Result |
|---|---|---|
| The literal sites in `brief_pack.py` | Grep tool, pattern `qa-factory/(artifacts\|strategy)`, `-i`, content mode, on `oh7-5/.../scripts/brief_pack.py` | **27 lines** (23 `artifacts`, 4 `strategy`). The finding says "23 lines with `qa-factory/artifacts/`", which matches. **Positive control, same shape** (same pattern, `-i`, content) on `hooklib.py` finds the known docstring `:276`. |
| The wider home literal `qa-factory` in the same file | Grep `qa-factory`, content mode | 35 lines. The 8 lines beyond the 27 are listed in §2.2 (F1). |
| OH5-2 Part A edits to `brief_pack.py` | I have **no shell** in this dispatch: my tools are Read, Grep, Glob and Write, so I could not run `git fetch` or `git diff`. Instead I read the checked-out worktree `C:\QAFactory\forge-repo\.claude\worktrees\oh5-2a` (its `.git` names `worktrees/oh5-2a`, and `HEAD` points at `refs/heads/wip/oh5-2a`). `refs/remotes/origin/wip/oh5-2a` = `2b810c0`. I could not confirm that the worktree's state equals `2b810c0` (estimate, not verified). | In that tree, `brief_pack.py:68-72` rewrites `SCRIPTS = (RP.package_root() / "scripts").as_posix()`, and `:3675` (`command_card_lines`) and `:4260` (`build`, card head) build the head through `RP.script_command('<script>', must_exist=False)`. The **same 27 literal lines sit at the same line numbers** as on main (re-grepped there). So the line numbers below hold for main + OH5-2 A. Spec t-254 §3.1/§4 Part A says the same, which corroborates it. |
| Dependency "after OH5-9 and OF3-1 c" | No `git log --grep` (no shell). Journal `logs/journal/dev1.jsonl`: `:440` `accepted` t-156 (OH5-9, `78f2a8c`). `:633` `accepted` t-214: "PR #5 merged ... OH3-9, OF3-1c ... merged b0d6c3a". Content on main: `brief_pack.py:295` carries OH5-9's `<task root>/bugs/`. `_approach_documents` reads `RP.home_dir`, and `test_brief_pack.py:2777` holds `of3_1c_home_strategy` (OF3-1 c). | **OF3-1 c: merged** (journal plus content). **OH5-9: its content is on main** (`:295`), but the batch row `onboarding-hooks/batch-5…md:40` still says `ожидает`. The status lags the code. **The Lead confirms with `git log --grep OH5-9 origin/main`** (question Q1). |
| `test_brief_pack.py` layer | `scripts/tests/test-layers.json`: `"keep"` opens at :35 and `"quarantine"` at :7004; `test_brief_pack.py` is at :277 | **keep** (layer `detector`). It was in `keep_fail_at_entry` (:6974) in the quarantine cohort record, which is historical. Also checked: `test_runtime_paths.py` :4531, `test_flow_requests.py` :1722, `test_walk_plan_fields.py` :6720, `test_brief_pack_s5_plan.py` :335 and `test_first_look_briefs.py` :6684 are **keep**. `test_brief_pack_roles.py` :7137, `test_brief_pack_manual.py` :7129, `test_exploration_perturbations.py` :8059, `test_project_approach.py` :9015 and `test_walk_brief.py` :10441 are **quarantine**. |
| The reader | `hooklib.py:691-706` `artifact_root(event, root)` (config `artifact_root`, relative or absolute, `.resolve()`d; a broken config raises `ValueError` on purpose, AR-28). `:275-282` `artifacts_dir`. `:349-390` `story_root` (what `build` uses, `brief_pack.py:4057`). `runtime_paths.py:739-799` `project_for_task` (finds the story's project from the story's own place and admits it only if its artifact root contains the story; raises `ValueError` otherwise). `:47` `home_dir`, `:38` `HOME = "qa-factory"`. | As stated. The template `references/templates/config.json` carries no `artifact_root` key, so harness projects run the default root. Grep for `artifact_root` there: none. Positive control: `tests_root` was found at :9. |
| Finding item 2: "the test at :2791 protects the wrong text, and the right fix will make it red" | `test_brief_pack.py:2777-2794` | **Contradiction**: the check is `line.endswith(f" {home}-profile.md")`. It does not pin `qa-factory/strategy/`, so the fix leaves it **green**. It does protect the wrong text in the sense that it never looks at the folder. The new row (T4) tightens it. |

## 1. Intent, rules and invariants touched

Intent (Lead brief): every path `brief_pack` prints to a role is built from the reader that says where the file is.
For a story file the reader is the story folder the code resolved through `hooklib.artifact_root` / `story_root`.
For a home file it is `runtime_paths.home_dir` / `RP.HOME`. The literals `qa-factory/artifacts/` and
`qa-factory/strategy/` never appear in text a role reads (FR-37: the path in text is the path the code writes).

### AR-n touched, with the change check each demands (copied into the DoD)

| AR | How this node touches it | Change check (DoD) |
|---|---|---|
| **AR-13**: a fact with a reader is read only through it | "where this story lives" has a reader: `hooklib.artifact_root`, reached through `story_root`, and `build` already holds its answer as `task_root`. Today 23 lines respell that fact by hand as `qa-factory/artifacts/{task}`, a second spelling that agrees only under the default root. "Where the home's strategy folder is" has the reader `RP.home_dir`; `_approach_documents` lists through it and prints a literal. The `store_provenance.source_path` of a case link has the reader `case_versions.read_source_path`; `case_paths` (:1247) reads it raw (F4). | Grep `brief_pack.py` for `qa-factory/artifacts` and `qa-factory/strategy` (`-i`, content), with the positive control on `hooklib.py:276`: **0 hits** after the node. Both outputs are pasted. Every site calls the survivor or reader named in §2. |
| **AR-4**: a printed path is relative to the project root and resolved through `runtime_paths` | the printed story path becomes "the resolved story folder relative to the story's project", computed in `runtime_paths` | the T-table rows below (default, configured, outside, no project) |
| **AR-15**: one survivor, wired everywhere (axis 8, "the story's location") | (if F2 (a)) a new survivor `runtime_paths.story_text(task_root, rel="")` spells "the story folder, or a file under it, as text a role reads". The 19 sites in `brief_pack` call it. Twins in other modules are queued in a residual node (§7). | list every site (§2). A site that cannot call the survivor is named. The axis-8 row for the survivor is queued to the full Lead (SIBLING_MAP belongs to the Lead), and the commit line reads `architecture: AR-15 -- survivor added, axis-8 row queued to Lead`, never "kept". |
| **AR-20**: shrink-only ratchets | role-load: the brief is generated text, not a charter. No `references/` text changes, so `process_ratchet_tokens` are untouched. | the witness carries `test_role_load.py` if `--witness-for` prints it. No row is raised. |
| **AR-29**: a code check judges data; a role's judgment is judged by a tier above | **no check is added or altered**. The node changes how a path is spelled; it judges nothing. `project_for_task` is reused in a new role (advice → printed path), so its error direction is stated in §3. | the census is unchanged: `test_judgment_census.py` green. The new helper is not named `*_problems`, so it is not a census unit. |

### Checks this node adds or alters: owner and census class (AR-29, P27)

| Check | Owner it serves | Census class | Census row |
|---|---|---|---|
| none added or altered. `plan_dispatch_lines` (census row `judgment-census.json:55`, class `shape`, owner `data`) only changes the first argument of its `_rel` calls; it gains no move. | data (code), unchanged | unchanged (`shape`) | unchanged |
| the T-table rows in keep `test_brief_pack.py` and the `story_text` row in keep `test_runtime_paths.py` | data | n/a (tests are not census units) | none |

FR walk the builder writes (PROJECT.md acceptance rule 1):
- A (refusals): not changed.
- B (text a person reads): "text to a person not changed"; briefs go to roles.
- C (contracts): FR-15 (a path is given, not searched), FR-14 (the shape of `request_lines` if F3 (b)).
- D (identity): FR-16, FR-58 (the test expectation comes from the requirement "the path the code writes", not from old output), FR-59 (unknown project → the true absolute path, never the default guessed).
- E (delivery): FR-37 (the core of this node).
- F (measurement): not applicable.
- G (code): FR-30 English, FR-32, FR-54 (siblings, §6).

## 2. Census of the literal (DoD key 2): every site with its reader replacement

### 2.1 The 27 `qa-factory/(artifacts|strategy)` lines (main 0a0db4f = main + OH5-2 A, same numbers)

`S(x)` below is the survivor `RP.story_text(task_root, x)` of §3 (or the brief_pack-local helper under F2 (b)).
Read/role-read column: **R** = role-read text, **P** = a PARSER prefix (it matches stored input), **D** = docstring/comment.

| # | Line | Function (D-0048) | Kind | Today | Replacement |
|---|---|---|---|---|---|
| 1 | :11 | module docstring | D | `-> qa-factory/artifacts/<T>/work/briefs/<ID>.md` | `-> <artifact root>/<T>/work/briefs/<ID>.md` (not role-read; aligned with the text) |
| 2 | :194 | `TOOLING` (scout card data) | R | `vcs_evidence.py ... --output qa-factory/artifacts/<T>/work/sources/...` (`<T>` is replaced by the key at :4275) | `--output <task root>/work/sources/<source id>/mr-<iid>.json`. `<task root>` is the placeholder the card head defines (:4260-4261) and that lines :187-192 already use. Closed choice C1. |
| 3 | :1135 | `_resolve` (task-relative branch) | R | `f"qa-factory/artifacts/{task_root.name}/" + name` | `S(name)`. **Positional invariant**: this branch never reads `_resolve`'s `project` argument, because `_bundle_view` (:1151) passes `task_root` as `project`. The story's project is found from the story's own place. |
| 4 | :1248 | `case_paths` | **P** | prefix `qa-factory/artifacts/{task_root.name}/` matched against `store_provenance.source_path` (project-relative, `case_versions.portable_source_path:57-77`) | prefix `S("") + "/"`. Value read through `case_versions.read_source_path(link)` (F4). Under a configured root the stored value is `<root rel>/<T>/...`, and today's literal never matches it. |
| 5 | :1443 | `_excluded_files` | **P** | prefix `qa-factory/artifacts/{task_root.name}/` on an excluded item's `local_ref` | prefix `S("") + "/"`. **Invariant B-231**: under a configured root, a story-prefixed `local_ref` is still recognised, so an excluded file is never handed on. Today it falls to `"work/" + ref`, a wrong path, so the excluded file IS listed by `source_material`. This is a live leak under a configured root. |
| 6 | :1494 | `source_material` | R | `- qa-factory/artifacts/{task}/{rel} (...)` | `- {S(rel)} (...)` |
| 7 | :1607 | `question_answer_lines` | R | holder `qa-factory/artifacts/{name}/` + answers rel | `S("/".join(QR.ANSWERS_REL))` |
| 8 | :1758 | `repo_map_for` | R | `qa-factory/artifacts/{task}/work/briefs/repo-map-<h>.md` | `S(f"work/briefs/repo-map-{doc['hash']}.md")` |
| 9 | :1783 | `blast_radius_line` | R | `rel = qa-factory/artifacts/{task}/work` | `rel = S("work")`. Limit: see edge E9 / F6. |
| 10 | :1852 | `_rel` (private) | R | `f"qa-factory/artifacts/{task}/{name}"` | `_rel(task_root, name) = S(name)`. Its callers pass `task_root` instead of `task` (all have it in scope): `plan_dispatch_lines` :1883 :1887 :1896 :1906 :1910, `plan_lines` :1946 :1954, `delta_lines` :2435, `fit_target_lines` :3081, `build` :4250. |
| 11 | :2856 | `APPROACH_ONE_LINE` (constant) | R | `documents qa-factory/strategy/` | the constant becomes a template with `{home}`, and `approach_forms` fills `{home}` with the home text (F1 decides whether config.json follows in the same line). Edge E10: the 200-byte pin. |
| 12 | :2859 | `APPROACH_POINTER` (constant) | R | `... qa-factory/strategy/` | the same template treatment at `approach_forms` :2943, :2947, :2950 |
| 13 | :2910 | `_approach_documents` | R | literal `qa-factory/strategy/` beside names listed from `RP.home_dir(project) / "strategy"` | **one Path for the listing and the text**: `folder = RP.home_dir(project) / "strategy"`; the names are globbed from `folder`, and the text is `folder.relative_to(Path(project)).as_posix() + "/"` (critic t-190 F3) |
| 14 | :3206 | `request_lines` | R | `qa-factory/artifacts/{task}/{UPF.REQ_LIST_FILE}` | `S(UPF.REQ_LIST_FILE)`. The signature question is F3. |
| 15 | :3332 | `exploration_lines` | R | `qa-factory/artifacts/{task}/work/briefs/{name}` | `S(f"work/briefs/{name}")` |
| 16 | :3674 | `command_card_lines` | R | `base = f"qa-factory/artifacts/{task}"` | gains a `task_root` parameter (callers :3879 `first_look_runner_lines` and :4278 `build` both hold it; no caller outside `brief_pack`: Grep `command_card_lines\(` over `scripts/` shows only these). `base = S("")`. **OH5-2 also edits this function** (:3675), so there is no D-0048 door: sequential after wave 6. |
| 17 | :3733 | `walk_brief_lines` | R | `App card: qa-factory/artifacts/{task}/work/app-card.md` | `S("work/app-card.md")` |
| 18 | :3747 | `walk_brief_lines` | R | `Case file: qa-factory/artifacts/{task}/{rel}` | `S(rel)` |
| 19 | :3851 | `first_look_runner_lines` | R | `base = f"qa-factory/artifacts/{task}"` | `base = S("")` |
| 20 | :3981 | `_fl_body` | R | `qa-factory/artifacts/{name}/{FIRST_LOOK_FILE}` | `S(FIRST_LOOK_FILE)` |
| 21 | :4068 | `build` | R | `brief_rel = qa-factory/artifacts/{task}/work/briefs/{id}.md` (also the result's `"path"`, :4503, and the resumed line, `delta_lines` :2421) | `S(f"work/briefs/{dispatch_id}.md")` |
| 22 | :4235 | `build` (case lines) | R | `- qa-factory/artifacts/{task}/{rel} (...)` | `- {S(rel)} (...)` |
| 23 | :4261 | `build` (card head) | R | `` `<task root>` = qa-factory/artifacts/{task} `` | `` `<task root>` = {S("")} ``. **OH5-2 also edits these lines** (:4260): the builder keeps OH5-2's `RP.script_command(...)` and changes only the `<task root>` value. |
| 24 | :4327 | `build._text` (omitted line) | R | `... qa-factory/config.json (...) and qa-factory/strategy/` | `{home}/strategy/` from the same home text as #11 (config.json: F1) |
| 25 | :4333 | `build._text` | R | `... read qa-factory/artifacts/{task}/work/briefs/{id}-files.md` | `S(f"work/briefs/{dispatch_id}-files.md")` |
| 26 | :4379 | `build` (`side`) | R | digests side file | `S(f"work/briefs/{dispatch_id}-digests.md")` |
| 27 | :4380 | `build` (`side`) | R | decisions side file | `S(f"work/briefs/{dispatch_id}-decisions.md")` |

### 2.2 The rest of the class in the same file (sweep-the-artifact-first, CLAUDE.md rule 9): the home literal `qa-factory/` without `artifacts|strategy`

Enumerated with a verdict each. The decision is **F1**.

| Line | Function | Text | Verdict |
|---|---|---|---|
| :87 | comment on `ROLE_FILES` | `project:` is relative to qa-factory/ | not applicable: comment, not role-read |
| :303 | `TOOLING` data | `a finding for qa-factory/factory-backlog.md` | F1 |
| :1134 | `_resolve` (`project:` branch) | `"qa-factory/" + rel, project / "qa-factory" / rel` | F1: `RP.home_dir(project) / rel`, with the text relative to `project` (the same reader as #13) |
| :2739 | `s4_stand_lines` | `more in qa-factory/config.json, environment.integrations` | F1 |
| :2751 | `S3_ROSTER_FILE` (used :2807 :2814 :2818) | `qa-factory/records/project-knowledge.json` | F1: `RP.rel_text("project-knowledge.json", project)` names where the record really is (records/ or the old state/, `runtime_paths.py:182-187`). This is a both-worlds record, so the literal is wrong today for a project that has not been re-onboarded. |
| :2855, :2859, :4327 | approach constants and the omitted line | `qa-factory/config.json` | F1 (same template as #11/#12/#24) |
| :2882 | `_approach_test_data` | `- test data: qa-factory/config.json ` | F1 |
| :2938 | `approach_forms` | `qa-factory/config.json could not be read` | F1 |

## 3. The mechanism

### 3.1 The survivor (F2 (a); under F2 (b) the same function lives in `brief_pack` as `_story_text`)

`runtime_paths.story_text(task_root, rel: str = "") -> str`:
1. `root = Path(task_root).resolve()`. On `OSError`/`ValueError`/`RuntimeError`, fall back to `Path(task_root)` as given.
2. `project = project_for_task(root)`. This is the one road for "the project the story belongs to"; it calls the one marker walk, so there is no new walk for `OUTSIDE_WALKS`. Any exception → `project = None`.
3. `head = root.relative_to(project).as_posix()` when `project` is set and `root` is under it. Otherwise (outside the project, or no project) `head = root.as_posix()` (absolute; F5).
4. `rel` is **text, never resolved**: backslashes become `/`, a leading `./` is dropped, a trailing `/` is kept, and the result is `head + "/" + rel` (or `head` when `rel` is empty). Reason: `rel` carries globs (`work/impl-diff*.txt`, `NOTES_GLOB`) and placeholders (`OWN_FINDINGS` holds `<` `>`). Those are not file names a filesystem should be asked about.
5. Never raises. Reads no environment variable, holds no cache, writes nothing (FR-45).

**Error direction of `project_for_task` in its new role** (from "find the project" to "the path printed to a role"). Allowed error: it rejects a valid project (a share it will not probe, an unreadable config). The text is then the **absolute** path of the same folder: longer, still true. Forbidden error: it names a project that does not contain the story, which would print a path relative to the wrong place. `_admits` already forbids that: a candidate is accepted only if its artifact root contains the story. Adversarial inputs that must stay on the safe side are T-rows: another copy of the project beside the real one (E2 of t-294), a story under an absolute artifact root on another drive, a broken config, a bare folder with no marker, a task path given unresolved (Windows 8.3 short name or a symlinked temp dir), and a `rel` holding `*` or `<...>`.

### 3.2 The home text
`_approach_documents`, `_resolve`'s `project:` branch and (F1) the config/records lines build the text from the Path they read through:
`RP.home_dir(project) / <x>` relative to `project`, and `RP.rel_text(name, project)` for records. The two module constants become templates filled at call time, so a test that sets `RP.HOME` sees it.

### 3.3 Call shapes
- Private and internal: `_rel(task_root, name)` and `command_card_lines(task_root, task, walk, commands, tail)` (or a keyword `task_root`; the builder picks one and lists it).
- `request_lines`: F3.

## 4. Edges, each with the invariant it protects

| Id | Edge | Behaviour | Invariant protected |
|---|---|---|---|
| E1 | **default root** (no `artifact_root` key; harness projects) | every line byte-identical to today: `qa-factory/artifacts/<T>/...`, `qa-factory/strategy/` | the default user sees no change. Keep tests outside the owns that pin today's text (`test_brief_pack_s5_plan`, `test_first_look_briefs`, `test_walk_plan_fields`, `test_story_step_start`) stay green. |
| E2 | **configured relative root** `artifact_root: "stories"` | `stories/<T>/...` everywhere, case lines and card head included; no `qa-factory/artifacts` anywhere in the brief | FR-37: joined to the project root, every printed story path is the folder `hooklib.artifact_root` resolves |
| E3 | configured root that climbs out (`"../shared"`) or is **absolute** on the same or another drive (`D:/qa-stories`) | absolute posix path of the story folder (`D:/qa-stories/<T>/...`), never a `../` form | the printed path resolves from any cwd. A relative form that climbs is never printed (F5). |
| E4 | **reader that raises**: (a) a broken `config.json` while `build` runs | `story_root` → `artifact_root` raises **before** any text exists; `build` raises as today, and `story_step` prints its note (`brief_pack` docstring :31-32). No brief is built with a default path. | AR-28 / FR-59: an unknown root never becomes the default literal |
| E4b | reader that raises at helper level (`project_for_task` raises: bare folder with no marker, config broken after `build` started, unreadable) | absolute posix path of the folder given | the text names a folder that exists, or the one the code was handed. It is never `qa-factory/artifacts/...` guessed. |
| E5 | **Windows separators**: config value `stories\qa` on Windows; any `task_root` with backslashes | `stories/qa/<T>/...` with forward slashes only (`as_posix`). On POSIX a backslash is part of a folder NAME (the writer `Path(value)` makes the same folder), so it is printed as that name. | one spelling of the separator, the same as every other path of the brief (`SCRIPTS`, `plugin:` doors). The printed path names the folder the writer created. |
| E6 | case or alias differences (Windows `C:\Proj` vs `c:\proj`; an 8.3 short temp path; a symlinked temp dir) | both sides are `resolve()`d before `relative_to`. On Windows `relative_to` folds case. The remainder keeps the folder's own spelling. | a project-relative path is never lost to an absolute one because of spelling |
| E7 | `rel` with a glob or placeholder | appended as text and never resolved; `file_lines` keeps its glob expansion (:1191-1199) | no OS error from a name that is not a file; the glob line format is unchanged |
| E8 | `_bundle_view` passes `task_root` as `project` (:1151) | the task branch ignores the argument (§2 #3) | positional: the project of the text is the story's own, never the caller's stand-in |
| E9 | **limit**: `blast_radius_line` caps at `BLAST_LINE_MAX = 300` (:1764, :1789). A long or absolute root can push head plus tail past it, and today's final `[:300]` would cut a path in the middle. | per F6 (recommended: the cap applies to the reason only; the head and the `Label the areas in <path>` tail are never cut) | FR-37: a printed path is never truncated into another path |
| E10 | **limit**: `APPROACH_SHORT_BYTES = 200` (:2852, pinned AT and BEYOND in `test_brief_pack`). `APPROACH_LINE_CHARS = 300` cut with ` ...` (:2946). | with `RP.HOME = "qa-factory"` the one-line forms are byte-identical, so the pin holds. The 300-char cut stays: the strategy folder sits at the start of its line, before the names, so the cut takes names first. | the default text keeps its pinned budget; a cut never removes the folder before the names |
| E11 | **limit**: the brief body ceiling `BRIEF_MAX_BYTES = 6 KB` with longer paths | the existing trimming order applies; every trim is a line of `Not in the brief` (E16 of the build) | no silent trim: a longer root costs room, and what it pushed out is named |
| E12 | **temporal**: the survivor does not exist before this node (F2 (a)) | it lands in the same commit as all 27 rewrites and its own `test_runtime_paths` row | no commit where `brief_pack` imports a missing function |
| E13 | `case_paths`: a `source_path` stored by a story under the default root, read after the person switched `artifact_root` | the new prefix does not match. The existing fallbacks (`link["path"]`, then the `contract.case_files` search, :1251-1259) find the file as today. | a configured root never loses a case that a fallback still finds; nothing new is guessed |
| E14 | `_excluded_files`: a `local_ref` that starts at the story under a configured root (`stories/<T>/work/sources/...`) | recognised by the new prefix and skipped | B-231: an excluded file is never handed on |
| E15 | `RP.HOME` set to another folder (the test's `elsewhere-home`) | the strategy line names `elsewhere-home/strategy/` and its file names | the folder and the names in one line come from one Path (critic t-190 F3) |
| E16 | OH5-2's lines (`command_card_lines` :3675, `build` :4260) | after wave 6: keep `RP.script_command('<script>', must_exist=False)` and change only the `<task root>` value | the card head keeps OH5-2's one quoting road (P31, t-254 N4) |

Conflicting requirement pairs named:
- (a) "default text byte-identical" vs "absolute path when there is no project". Resolved: a project with a marker under the default root gives today's text (E1). Only a markerless folder changes (E4b). That changes the **quarantined** `test_exploration_perturbations.py` T2 pin (:85-88: a bare `task` folder and a `task` string that differs from the folder name). It is listed in the handoff, not edited.
- (b) "`request_lines` keeps external callers" vs "one road". This is F3.
- (c) "one survivor" vs "SIBLING_MAP is the Lead's". The axis row is queued (F2, §1 AR-15 line).

## 5. Tests (DoD key 4): table rows only, no new test file

Every case below is a **row of one table function** in keep `scripts/tests/test_brief_pack.py`, plus one table in keep
`scripts/tests/test_runtime_paths.py` under F2 (a). The id names the case (P16). The expectations come from the
requirement "the printed path, joined to the project root, is the folder the writer resolves" (FR-58), checked by
behaviour, not by copying the code's output.

**`test_brief_pack.py`, new table `of4_21_paths_follow_the_reader` (extends the OF3-1 c function `of3_1c_home_strategy` or sits beside it; the builder picks):**

| Row id | World | Checked |
|---|---|---|
| T1 default | `harness.temp_project`, story under `qa-factory/artifacts/QA-9`, an S5 automator brief, an S6 walk brief and an S3 strategist brief built through `brief_pack.build(..., write=False)` | the key lines are byte-identical to today's text: the card head `` `<task root>` = qa-factory/artifacts/QA-9 ``, one case line, the side files, the blast line |
| T2 configured | same world plus `artifact_root: "stories"` in `qa-factory/config.json`, story under `stories/QA-9` | no `qa-factory/artifacts` in any of the three briefs. Every path of the form `stories/QA-9/...` it prints, joined to the project, resolves inside `hooklib.artifact_root(root=project) / "QA-9"`. The card head names `stories/QA-9`. |
| T3 outside | `artifact_root` = an absolute temp folder outside the project | the card head names that absolute folder (posix), no `../` and no `qa-factory/artifacts` |
| T4 home | `RP.HOME = "elsewhere-home"` (the existing loop at :2783-2791) | the strategy line contains `elsewhere-home/strategy/ elsewhere-home-profile.md`, the full fragment, and not `qa-factory/strategy/`. This rewrites the :2790-2791 check into the requirement. |
| T5 windows | `artifact_root: "stories\\qa"` | no `\` in any printed story path. On Windows (`os.sep == "\\"`) the head reads `stories/qa/QA-9`. On POSIX the printed name is the folder the writer made (assert by `Path(project, shown).resolve() == task_root.resolve()`). |
| T6 excluded (B-231) | configured root, an item `status: excluded` with `local_ref: "stories/QA-9/work/sources/S1/mr-1.json"` and that file on disk | `source_material` does not list it |
| T7 case link | configured root, a link whose `store_provenance.source_path` is `stories/QA-9/work/test-cases/a/TC-001.md` | `case_paths` returns `work/test-cases/a/TC-001.md` through the prefix branch (proved by also giving a `link["path"]` that points elsewhere) |
| T8 no project | a bare folder with no marker, `exploration_lines(task_root, ...)` | the pointer names the absolute posix folder and not `qa-factory/artifacts` |
| T9 blast limit | configured absolute root long enough that today's line exceeds 300 | per F6: the head path and the tail path are whole |

**`test_runtime_paths.py` (keep), one table for `story_text` (F2 (a)):** rows E1 default, E2 configured, E3 absolute
other drive (skipped where no second drive: the row says why), E4b no marker → absolute, broken config → absolute,
E5 backslash value, E6 unresolved temp path, E7 `rel` with `*` and with `<x>`, trailing slash kept. Each row checks the
exact returned text.

Adversarial battery (CLAUDE.md rule 11; `artifact_root` is outside input, a project config): empty or blank value is
the writer's refusal (`artifact_root must be a non-empty path`, E4), not this node's. The node adds no new limit on the
value. Magnitude is T9. Encoding: a non-ASCII root (`stories/Анна`) is a row of the `story_text` table, kept verbatim.

## 6. Siblings (DoD key 6): other scripts that print the same literals (not fixed in this node)

Command: Grep `qa-factory/(artifacts|strategy)`, count mode, glob `*.py`, over `oh7-5/ai-packages/qa-factory/scripts/`. It found
550 hits in 207 files (tests included). Non-test scripts besides `brief_pack.py` (hits): `app_card` 2,
`artifact_producer` 1, `audit_factory` 2, `check_coverage` 3, `check_delivery` 1, `config_contract` 2, `collect_gaps` 1,
`controller` 1, `check_traceability` 1, `critic_rollcall` 2, `cost_capture` 4, `driver_dispatch` 5, `driver_dialog` 1,
`driver_stage_plan` 1, `driver_gates` 3, `driver_sources` 7, `driver_stage_s7` 3, `driver_machine` 6, `driver_timing` 1,
`driver_stage_s5` 1, `driver_stage_s8s9` 2, `exit_gate` 1, `factory_dashboard` 1, `gate_brief` 1, `form_selftest` 2,
`guard_pre_tool` 5, `hooklib` 1, `interim_packet` 1, `investigation_probe` 1, `judge_cases` 1, `judge_code` 2,
`judge_diff` 1, `judge_plan` 1, `judge_requirements` 1, `judge_results` 2, `judge_sources` 1, `launch_card` 1,
`judge_run` 2, `manual_capture` 4, `ledger` 1, `plan_row` 1, `onboard_apply` 1, `planning_contract` 1,
`project_gitignore` 1, `project_decisions` 1, `postcompact_reload` 1, `readiness` 1, `red_sandbox` 2,
`refusal_registry` 1, `repo_map` 1, `runtime_probe` 1, `s5_precheck` 2, `source_exclusions` 1, `run_suite` 1,
`s5_plan` 1, `sizing` 1, `stand_identity` 1, `stage_done` 1, `stage_guard` 4, `story_progress` 1, `story_run` 1,
`story_step` 4, `test_repo_base` 1, `ticket_adapter` 3, `validate_artifacts` 4, `window_files` 1, `vcs_evidence` 4,
`walk_timing` 1, `walk_session` 1.

Read and classified as **printing to a role or person** (the rest are not classified; classification is the first
step of the residual node):
- **`story_step.py` :252 `_prompt`** (`Artifacts dir: qa-factory/artifacts/<T>/`, `Inputs:`) and **:316 `_project_rel`** (`Read <brief> first`, the form path; callers :372 :451 :1141 :1187 :1200 :1306 :3108 :3121), plus :546, :652. These print **in the same dispatch packet as the brief**. After this node, under a configured root, the prompt and the brief disagree (FR-10). See F7.
- `driver_sources.py` :74 :145 :311 :356 :427 :701 :721; `driver_dispatch.py` :2379 :3826 :3867 :3910 :3950; `driver_gates.py` :133 :156 :720; `driver_machine.py` :1054 :1708 :1714 :1727 :1730 :1955; `driver_stage_s7.py` :699 :996 :997.
- Refusal or help texts: `manual_capture.py` :284 :774 :5461 :5500; `ticket_adapter.py` :1480 :2438 :2612; `guard_pre_tool.py` :1634 :2241; `vcs_evidence.py` :646.
- Parsers on the literal (the same class as #4/#5): `cost_capture.py:939` (`anchor`), `validate_artifacts.py` :1830 :2631, `stage_guard.py:1215`, `check_coverage.py:249`.
- Hand twins of the survivor's job (relative to project, else absolute): `controller._output_rel` :9725, `config_contract._display` :2619, `stage_done._story_rel` :622, `launch_card.card_rel` :48, `stand_identity.confirmations_rel` :123.
- In `hooklib.artifact_root` itself: `project / "qa-factory" / ...` (:694, :702) spells the home instead of `RP.HOME`. This is a sibling of the home class, noted only.

SIBLING_MAP: axis 8 ("where the story is on disk") is the axis. Under F2 (a) the survivor is its new row (queued to the Lead).

## 7. The builder dispatch (draft for the Lead; header lines per R11-f)

given: this spec §0-§6; C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\design\factory-rules.md (whole); C:\QAFactory\forge-repo\.claude\worktrees\of4-21\plans\builder-rules.md; C:\QAFactory\forge-repo\.claude\worktrees\of4-21\docs\TESTING.md; C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\brief_pack.py (the 27 lines of §2.1, plus §2.2 under F1); C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\runtime_paths.py (:38-188, :715-799); C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\hooklib.py (:275-390, :691-706; read only); C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\case_versions.py (:57-98; read only); C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\user_path_failures.py (:1065-1085); C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\tests\test_brief_pack.py (:68-74 `seed`, :2777-2794); C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\tests\test_runtime_paths.py; C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\tests\test_flow_requests.py (:33, :180-230); C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\tests\test_walk_plan_fields.py (:225-240); C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\tests\harness.py (`mark_project`, `temp_project`, `use_project`)
owns:
C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\brief_pack.py
C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\tests\test_brief_pack.py
C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\runtime_paths.py
C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\tests\test_runtime_paths.py
C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\user_path_failures.py
C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\tests\test_flow_requests.py
C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\tests\test_walk_plan_fields.py
(The last five exist only under the recommended options. The node row owns only the first two. If F2 (b) is chosen, drop `runtime_paths.py` and `test_runtime_paths.py`. If F3 (a) is chosen, drop `test_flow_requests.py` and `test_walk_plan_fields.py`, and keep `user_path_failures.py` for its one argument.)
functions (D-0048): `brief_pack`: `_resolve`, `case_paths`, `_excluded_files`, `source_material`, `question_answer_lines`, `repo_map_for`, `blast_radius_line`, `_rel`, `plan_dispatch_lines`, `plan_lines`, `delta_lines`, `fit_target_lines`, `_approach_documents`, `approach_forms`, `request_lines`, `flow_request_lines`, `exploration_lines`, `command_card_lines`*, `walk_brief_lines`, `first_look_runner_lines`, `_fl_body`, `build`*, constants `TOOLING` (:194), `APPROACH_ONE_LINE`, `APPROACH_POINTER`; under F1 also `s4_stand_lines`, `s3_roster_lines`, `_approach_test_data`, `S3_ROSTER_FILE`, `TOOLING` (:303). `runtime_paths`: new `story_text`. `user_path_failures`: `main`. (*also edited by OH5-2 Part A, so there is no D-0048 door for these two: the node starts after wave 6 merges.)
non-goals: no file of §6 (story_step, driver_*, guards, other parsers; residual node F7); no edit of hooklib.py; no change to what any path resolves to (spelling only); no new test file; no edit of a quarantined test file (`test_brief_pack_roles.py`, `test_brief_pack_manual.py`, `test_exploration_perturbations.py`, `test_project_approach.py`, `test_walk_brief.py`); no cache in `story_text`; no SIBLING_MAP edit (the axis-8 row is queued to the Lead); no `references/` text
handoff: builder report (`.claude/agents/builder.md` rule 7): the diff; the FR walk A-G; the AR lines of §1; the per-site table of §2 with the call each site now makes; the verbatim witness; the Grep 0-hit proof plus its positive control; the list of quarantined pins expected to go red (expected: `test_brief_pack_roles.py:110` (#2), `test_exploration_perturbations.py:88` and `:340` (E4b/T8 world), any `test_project_approach.py` / `test_brief_pack_manual.py` / `test_walk_brief.py` pin a builder notices); the wall time of `test_brief_pack.py` before and after (no cache, §3.1); "needed beyond the manifest"
edges: E1-E16 of §4 (default byte-identical, configured, outside/absolute, reader raises at build and at helper level, Windows separators, case/8.3/symlink, glob/placeholder rel, `_bundle_view` stand-in project, 300-char blast cap, 200-byte approach pin, 6 KB ceiling, temporal survivor, stale source_path, B-231 exclusion, RP.HOME, OH5-2 lines)
DoD: (1) every site of §2.1 (and §2.2 per F1) builds its path as the replacement column says; (2) a Grep, `-i`, content mode, of `qa-factory/(artifacts|strategy)` over `scripts/brief_pack.py` gives 0 hits, with the same Grep finding `scripts/hooklib.py:276` as the positive control, both outputs pasted; (3) the T1-T9 rows of §5 in `test_brief_pack.py` and the `story_text` table in `test_runtime_paths.py` pass, with T1 asserting today's text byte for byte; (4) `test_flow_requests.py` and `test_walk_plan_fields.py` stay green on the new `request_lines` call shape (F3 (b)); verification run: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/brief_pack.py scripts/tests/test_brief_pack.py scripts/runtime_paths.py scripts/tests/test_runtime_paths.py scripts/user_path_failures.py scripts/tests/test_flow_requests.py scripts/tests/test_walk_plan_fields.py`, then every non-quarantined test file it prints, plus `python -B ai-packages/qa-factory/scripts/tests/test_judgment_census.py` named explicitly; pasted verbatim
siblings: §6 list, not fixed here. Report any further hand spelling of a story or home path noticed in `brief_pack.py`.
designer: C:\QAFactory\forge-repo\docs\tasks\specs\t-290-of4-21-brief-pack-paths.md

## 8. Forks (returned, not decided), each with a recommendation

- **F1: scope inside `brief_pack.py` (sweep-the-artifact-first).** The node row names `artifacts/` and `strategy/`. The same file carries 8 more home literals (§2.2): `config.json` ×6 lines, `records/project-knowledge.json` (a both-worlds record: the literal is **wrong today** for a project still on `state/`), `factory-backlog.md`, and the `project:` door. (a) Fix them in this node through `RP.home_dir` / `RP.rel_text`: about +12 lines, and 3-4 pins in the quarantined `test_project_approach.py` go red (listed). (b) Only the 27 lines; queue the 8. **Recommendation: (a).** Same class, same file, and rule 9 asks for the sweep. The records line is a live FR-37 defect.
- **F2: where the helper lives (AR-15, P31).** (a) A survivor `runtime_paths.story_text` (axis 8, "the story's location"), with its axis row queued to the full Lead; 5 hand twins in other modules (§6) fold into it later. (b) A `brief_pack`-local helper: smaller owns, but it is a sixth hand copy of "relative to project, else absolute". **Recommendation: (a).** One road. Cost: +2 owned files (`runtime_paths.py`, keep `test_runtime_paths.py`) and about 25 lines. `runtime_paths.py` is touched by OH5-2 Part A, so this is sequential after wave 6 anyway.
- **F3: `request_lines(found, task)` has callers outside `brief_pack`** (`user_path_failures.py:1080` CLI, which already holds `task_root` at :1072; keep tests `test_flow_requests.py` ×8 and `test_walk_plan_fields.py` ×2). (a) Add a keyword `task_root=None`, where `None` prints the default spelling built from `RP.HOME`: a second road that lies under a configured root. (b) **One road**: `request_lines(found, task_root)`. Its callers pass the story folder; the two keep tests build their story under a `harness.mark_project` project (they already do, `test_flow_requests.py:42`, `test_walk_plan_fields.py:196`) and keep their `LIST` expectation under the default root. **Recommendation: (b)** (rule 6). Cost: +3 owned files and about 15 changed test lines.
- **F4: `case_paths` reads `store_provenance.source_path` raw** (:1247), and the package has the reader `case_versions.read_source_path` (`:87-98`; also folds backslashes and the top-level `source_path`). (a) Read it through the reader in the same edit (AR-13). (b) Change only the prefix. **Recommendation: (a).** Same line, and the error direction is still a file existence check (`is_file`).
- **F5: story folder outside the project** (absolute `artifact_root`, or `../`). (a) The absolute posix path (true from any cwd; the `controller._output_rel` / `config_contract._display` precedent; briefs already carry absolute `SCRIPTS` and `plugin:` paths as runtime packets). (b) `os.path.relpath` with `..` (portable, but cwd-dependent and AR-4-ambiguous). (c) A placeholder `<artifact root>/<T>` (`hooklib._example_folder` precedent): never false, but not usable. **Recommendation: (a).** AR-4's "relative to the project root" cannot hold for a folder the person put outside the project, and FR-37 (true path) wins. The Lead may want the owner's word if AR-4's text should name this case.
- **F6: the 300-char cap of `blast_radius_line` versus a long path** (E9). (a) The cap applies to the reason only; head and tail are never cut, so the line may exceed 300 when its paths need it (stated in the docstring). (b) Drop the tail sentence before cutting the head. (c) Keep `[:300]` (a path can be cut). **Recommendation: (a).**
- **F7: the same packet's other half.** `story_step._prompt` / `_project_rel` print `qa-factory/artifacts/<T>/` beside the brief (§6). After this node, under a configured root the role's prompt and its brief disagree (FR-10, P31). (a) A residual node **OF4-21b**: story_step `_prompt`, `_project_rel`, :546, :652; the driver lines of §6; the parsers `cost_capture:939`, `validate_artifacts` :1830 :2631, `stage_guard:1215`; and fold the 5 twins into `story_text`. Owns: those files plus keep pins (`test_story_step_start.py` and the others `--witness-for` prints). Test: extend T2's world to the prompt (`story_step start` under `artifact_root: stories` → no `qa-factory/artifacts` in stdout). Carrier: a `findings/` file plus a row in the next not-taken batch of `onboarding-forge` plus a README «Содержание» row, written by the coordinator at this node's acceptance (D-0044). (b) Widen this node to story_step: about +40 lines and many keep pins in `test_story_step_*`. **Recommendation: (a).** A slice is no exclusion when the rest is a named node with owns and a test (rule 6). Until OF4-21b lands, the disagreement exists only under a non-default root, and that is already wrong today in both halves.

### Questions (not forks)
- **Q1**: the OH5-9 batch row (`onboarding-hooks/batch-5…md:40`) says `ожидает`, while the journal (`:440`, `78f2a8c`) and main's content (`brief_pack.py:295`) show it landed. I had no shell for `git log --grep`. The Lead confirms, and if needed the row status is moved.
- **Q2**: the brief asked me to read the OH5-2 diff with `git diff`. I read the `oh5-2a` worktree instead (§0). If the branch has commits the worktree lacks, re-check §2 rows #16 and #23.

## 9. Small technical choices I closed (no design weight; listed so they can be undone)
- C1: :194 uses the card's own `<task root>` placeholder instead of expanding a path into a module constant (consistent with :187-192).
- C2: `rel` in `story_text` is text, never resolved (globs and placeholders); a trailing `/` is kept.
- C3: no cache in `story_text`. The builder reports `test_brief_pack.py` wall time before and after; a cache is a later node only if the cost shows.
- C4: the two approach constants become `{home}` templates filled at call time (so `RP.HOME` set by a test is seen); their names stay.
- C5: `command_card_lines` gets `task_root` (internal-only function, two callers).
- C6: docstring :11 is aligned (`<artifact root>`); comment :87 is left as is.

## 10. Reading trail
- `.claude/worktrees/oh7-5/plans/piles/onboarding-forge/batch-4-hvosty-onbordinga-i-forzha.md:50`; `.../README.md:180`.
- The finding (whole).
- `docs/tasks/specs/t-254-oh5-2-plugin-root-given.md` :1-356 (§1-§6, Part A owns and DoD).
- `.claude/worktrees/oh7-5/ai-packages/qa-factory/scripts/brief_pack.py`: :1-120, :160-197, :1100-1260, :1430-1500, :1595-1610, :1740-1790, :1840-1860, :2730-2790, :2840-2950, :3196-3210, :3318-3337, :3660-3760, :3840-3860, :3972-3985, :4050-4140, :4225-4270, :4318-4387; plus Greps of literals, `brief_rel`, `replace("<T>"`, call sites, the function list, and `APPROACH_*` / `S3_ROSTER_FILE` users.
- `.claude/worktrees/oh5-2a/.../brief_pack.py` :64-73, and the literal Grep (27 lines, same numbers); `.git/worktrees/oh5-2a/{gitdir,HEAD}`; `.git/refs/remotes/origin/wip/oh5-2a`; `.git/packed-refs` (Grep).
- `runtime_paths.py` :1-235, :715-815, function list. `hooklib.py` :270-404, :640-730. `case_versions.py` :50-104. `user_path_failures.py` :1050-1085.
- `tests/test_brief_pack.py` :1-130, :2760-2840, literal Grep. `tests/test-layers.json` :274-285, :6960-7009, and the layer Greps. `tests/test_exploration_perturbations.py` :35-91. `tests/test_flow_requests.py` :25-39, `LIST` Grep. `tests/test_first_look_briefs.py` :340-370 and its function list. `tests/harness.py` (`mark_project`, `temp_project`, `use_project`). `references/templates/config.json` (Grep). `tests/fixtures/judgment-census.json` (Grep for `brief_pack.py`, `runtime_paths.py`).
- `design/architecture.md` :69-80, :161-188. `docs/SIBLING_MAP.md` :202-226. `plans/builder-rules.md` (7b Grep).
- Package-wide sibling Grep (count, then content for 15 named files). `story_step.py` :245-319.
- `logs/journal/dev1.jsonl` :412-440, :486-633 (Greps).
- Not read (beyond the manifest, not needed): `docs/TESTING.md` beyond what builder-rules 7b and CLAUDE.md rule 11 quote; `factory-rules.md` beyond the index loaded in every session.

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
- **Critic on plan:** skipped. No schema or money change. The forks are recommendations with no architecture change beyond F2's survivor, which the diff critic checks (rule 3). The diff critic is mandatory.
