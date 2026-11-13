# t-324: DRAFT spec for OH8-2 (NTFS alias names, story key -> folder) and OH8-6 (json.loads outside SCANNED, stale SCOPE)

Designer draft (Opus) for the Lead. It is not accepted. Batch: `plans/piles/onboarding-hooks/batch-8-ostatki-t-282-t-254-t-287.md`, rows OH8-2 and OH8-6.
Every line number is from read-main `origin/main 303e89e` (`C:\QAFactory\forge-repo\.claude\worktrees\read-main`). The t-328 critic confirmed that nothing in the package changed up to read-main HEAD 2f1cec8. The builder re-anchors each line by its function name before editing.

## 0b. Fix round t-328 (critic-on-plan `docs/tasks/specs/reviews/t-328-oh8-2-oh8-6-plan-review.md`, fit_with_fixes; coordinator decisions, "решила сама")

| Finding | What changed | Where |
|---|---|---|
| B1 | `landing_name` no longer uses realpath. It returns the exact name if listed; otherwise, when `lexists(parent/name)`, the first listed `n` with `os.path.samefile(parent/n, parent/name)`; every error returns "". Added junction and symlink cells. | A3; §3 junction rows; §5 `OH82_NAMES` |
| B2 | One predicate `hooklib.other_spelling(parent, key)`. A1 steps 4-5 call it. A13 (exit_gate) maps the key to `unknown-task` whenever it is non-empty, which covers 8.3 names and junction aliases. `_path_story` uses `landing_name`. | F3; A1, A2b, A13, A15; §5 exit_gate cells |
| B3 | One shape predicate `hooklib.clean_key`, called by both `is_story_folder` and A1 step 2. I2 names its one exception: an existing folder ending in `.` or a blank is no longer a story on any OS (AR-4). | A0, A1; §3 I2 and row; §5 `v1.` cell |
| B4 | Order is OH8-1 -> OH8-2a. 2a merges `main` after wave 10, and the sentinel dict is named for that world. OH8-6 `owns` carries its function list for `refusal_registry.py`. A census line names the later writer. | §4 |
| N1 | C6: marker in `telemetry_coverage`, `person_signal` instead of stderr, and the activity/segments shape is guarded (decided here: guard, not queue). Added a test cell. | C6; §5 |
| N2 | `record` wraps `resolve_ticket` (task "" plus the C3 signal on `ValueError`/`OSError`). | C3'; §3 |
| N3 | §3 "data written before 2a" rows give each reader's new answer and door. The read-only measurement command is in the spec; the 2a builder runs it FIRST and stops on any alias. | §3.2; §6 OH8-2a |
| N4 | Counts corrected to 78 call lines in 24 files. Added rows for execution_scheduler:156, exit_gate:1162/1202 and source_exclusions:540. Widened the problem grep. Aligned the resolve step numbers (1, 1b, 2, 5). Closed §8 item 8. | F1, §1, §2.3, §8 |
| N5 | `_path_story` never raises (it returns the raw key on any exception). Named the `/artifacts/` vs `artifact_root` mismatch. | A15; §3 |
| N6 | Added `OH82_NAMES` cells: ` T`, `T..`, `T. .`, junction, `v1.`, full-width `T`, both twins real. Named the OH8-6 red probe. Steps 3-5 share one `_listing`. | §5; A1 |
| F7 follow-up | `_story_names` via `landing_name` is listed as a proposed node. | §8 item 10 |

## 0a. Lead decisions (coordinator Opus, 2026-11-13; "решила сама", by recommendation until the owner's word)

F1 (b), F2 (b), F3 (a), F4 (a), F5 (b), F6 (a: both analogs in OH8-6; the `cost_capture` line is money, so its critic is mandatory), F7 (stays). Node order: 2a, then 2b and OH8-6 in parallel. A critic-on-plan (t-328) comes before any builder: the spec carries forks and changes `hooklib.artifacts_dir`, which has 78 call lines in 24 production files (t-328 measurement). Intent 3 of the brief is corrected by F4: a guard over a write judges the folder the OS actually writes to.

## 0. Forks (returned; decided in §0a and §0b)

**F1. The route for "an alias of key T must not reach T's folder".**
`hooklib.artifacts_dir` has 78 call lines in 24 production files (t-328: `grep -n 'artifacts_dir(' scripts/*.py`, minus the def). Many of them both read and create.
- (a) Change every reading site to `is_story_folder`.
- (b) **Chosen.** One survivor (AR-15): `artifacts_dir` refuses an alias spelling. Existence probes that do not use it switch to `is_story_folder` or `is_story_with_pipeline`. Cost: one `os.listdir` per call, measured at 44.7 µs for 60 entries (t-328), shared by steps 3-5.

**F2. The create world.** **Chosen: (b).** Shape refusal (`clean_key`), exact match, and `other_spelling` (OS truth via samefile, plus casefold/strip twins on every file system). Everything else passes as create.

**F3. `exit_gate._identity` explicit task (`exit_gate.py:246`).** **Chosen: (a).** An explicit task that is one component and not an exact story folder becomes `unknown-task` whenever `hooklib.other_spelling(artifact_root(), task)` is non-empty. That covers case, trailing dot or blank, 8.3, and a junction or symlink alias. A scope fact names it: `explicit id 'T.' is another spelling of folder 'T'; keys are matched exactly`. `unknown-task` means a full audit, never a pass (FR-59, AR-28). An explicit `NOPE` (no folder, `other_spelling` empty) is unchanged (§8).

**F4. guard_pre_tool path-derived key.** **Chosen: (a).** `_path_story` returns `landing_name(artifact_root(event), key)` when that is non-empty, otherwise the raw key, so the owner rule judges the folder the write lands in. It never raises.

**F5.** **Chosen: (b)** `hooklib.person_signal`. This is now the ONE road for "a broken receipt or controller file was skipped", C6 included.

**F6.** **Chosen: (a).** C5 and C6 are in OH8-6. A critic is mandatory (money).

**F7.** `controller._story_names` STAYS in this round, because of its veto error direction. Converging it on `landing_name` is proposed as a node (§8 item 10).

## 1. Scope, AR-n, owners, census

**Goal.** No other spelling of story key `T` reaches T's folder through any site that turns a key into a story folder. Other spellings: `T.`, `T `, ` T`, `...`, `t`, an 8.3 short name, an alias of a junction story. An exact key's answer does not change anywhere, except the one named shape exception (I2). A broken JSON receipt or controller file on the host hook path is named through `person_signal` and skipped, never a traceback. The SCOPE paragraph of `refusal_registry.py` names every `SCANNED` module, and a test holds that.

**AR-n touched and the change check in the DoD:**

| AR | How it is kept | Change check in the DoD |
|---|---|---|
| AR-15 one survivor | `artifacts_dir` plus the leaves `clean_key`, `is_story_folder`, `alias_twins`, `landing_name`, `other_spelling`, `is_story_with_pipeline`. The predicate "another spelling of an existing folder" is composed ONCE (`other_spelling`). | Grep the PROBLEM: `is_one_component\(` and `/\s*(str\()?[\w\[\]"']*(task\|ticket\|story\|key\|name)` over `scripts/*.py`, case-insensitive, with a positive control (`execution_scheduler.py:156` must hit). Every hit gets a §2 row. The `is_one_component` caller sentinel (§5) is shrink-only. |
| AR-13 one reader | Receipts go through `host_dispatch.receipt_files`; files through `hooklib.read_json`. | Grep `json.loads` in `host_dispatch.py`, `activity_capture.py:57` and `cost_capture.py:1946` with a positive control. |
| AR-28 unknown never passes | exit_gate other spelling -> `unknown-task`. An unreadable receipt is never marked terminal. Incomplete cost attribution is marked, not silent. | Missing, unreadable and empty are stated for every new read (§3); a cell pins each. |
| AR-4 not tied to a machine | One outcome on NTFS and on a case-sensitive disk. `clean_key` refuses a trailing dot or blank on every OS. | Cells run on both OSs; `nt`-only and POSIX-only cells are marked. |
| AR-9 refusal names a door | The A1 refusal names the folder; `story_root`'s text is unchanged. | A test asserts the near-miss name. |
| AR-22 producer and reader | The SCOPE docstring follows `SCANNED`. | `part_scope_docstring` plus mutations. |
| AR-29 code judges data | Every added check is SHAPE or XREF. | Census rows in the same commit; `test_judgment_census.py` green (§4 census line). |

**Checks: owner and census class (AR-29, P27):**

| Check | Owner | Class | Census row |
|---|---|---|---|
| `hooklib.clean_key` (shape of a story key) | data | shape | a row if C1 names it |
| `hooklib.artifacts_dir` shape and other-spelling refusal | data | xref | the existing `hooklib.py artifacts_dir` row changes from `shape` to `xref` |
| `hooklib.is_story_folder` (now calls `clean_key`; stricter on a trailing dot) | data | xref (unchanged) | none new |
| `alias_twins`, `landing_name`, `other_spelling`, `is_story_with_pipeline` | data | xref | a row only if C1 names them |
| `stage_guard.resolve_ticket` steps 1, 1b (via `_recipient_receipts`), 2 (via `story_named_by_text`), 5, and `_names_story` | data | xref | none new |
| `exit_gate._identity` other spelling -> `unknown-task` | data | xref | the existing row if present |
| `host_dispatch.record` skip-and-signal | data | shape | if C1 names it |
| `cost_capture._capture` attribution marker | data | shape | if C1 names it |

Commit lines: 2a `judgment: adds data check hooklib.artifacts_dir`; 2b `judgment: none`; OH8-6 `judgment: none` unless C1 names a unit.

**FR walk:**
- A: FR-1, FR-2, FR-4, FR-59.
- C: FR-14 (`receipt_files` gets an additive keyword); FR-17.
- D: FR-16 (`resolve_ticket` stops producing alias ids); FR-59.
- F: FR-41 (incomplete attribution is printed, not shown as a fact; C6).
- G: FR-30, FR-32.
- B and E: only the signal lines and the refusal sentence change; each says what is wrong, then what to do.

**Non-goals.**
- No change to `is_one_component`.
- No change to its session-id and pin-key uses (activity_capture:45, cost_capture:1908, :3801, recover_codex_usage:17, red_sandbox:330, :334).
- No work on OH8-1, 3, 4, 5 or 7.
- No A24 registry rows.

## 2. Every site: a row

"Gate" means `is_story_folder` (or `story_root`, `story_of`, `story_cli`) already decides.

### 2.1 Changed: node OH8-2a

| # | Site | Function | Current | Change |
|---|---|---|---|---|
| A0 | hooklib.py (new, above `is_story_folder`) | `clean_key(name) -> bool` | — | `is_one_component(name) and name == name.strip() and name == name.rstrip(" .")`. Leading and trailing blanks, trailing dots, and `...` (which rstrips to "") are refused. Pure; never raises. |
| A0b | hooklib.py:317-319 | `is_story_folder` | its own blank check (`not name.strip() or name != name.strip()`) | Call `clean_key(name)` for the shape. The parent check, listing and `is_dir_or_no` are unchanged. **This is the one behaviour change of an exact key**: an existing folder whose name ends in `.` or a blank is no longer a story (I2 exception). |
| A1 | hooklib.py:275-282 | `artifacts_dir` | `is_one_component` only | In this order: (1) the existing one-component `ValueError`, unchanged text; (2) `not clean_key(key)` -> `StoryRootError`: "task id {key!r} starts or ends with a blank, or ends with a dot, which some file systems drop from a folder name; pass the key without them."; (3) list the root ONCE (`names = _listing(root)`); key in `names` -> the path; (4)-(5) `other = other_spelling(root, key, names)`; non-empty -> `StoryRootError`: "task id {key!r} is not the exact name of a story folder: folder {other!r} exists, and the key is matched exactly. Pass {other!r}, or a new key that is no other spelling of an existing folder."; (6) otherwise the path (create world). |
| A2 | hooklib.py (new) | `alias_twins(parent, name, names=None) -> list[str]` | — | The sorted names `n` (from `names`, or `_listing(parent)` when None) with `n != name` and `_name_alias(n) == _name_alias(name) != ""`. Never raises. |
| A2b | hooklib.py (new) | `other_spelling(parent, key, names=None) -> str` | — | THE one composition: `land = landing_name(parent, key, names)`; return `land` if `land and land != key`; else `alias_twins(parent, key, names)[0]` if any; else "". Never raises. |
| A3 | hooklib.py (new) | `landing_name(parent, name, names=None) -> str` | — | `name` if it is in `names` (or `_listing(parent)`). Else, if `os.path.lexists(Path(parent)/name)`: the first `n` of the listing in sorted order with `os.path.samefile(Path(parent)/n, Path(parent)/name)`, which is `controller._story_names`' own rule. Else "". Every `OSError`, `ValueError` or `TypeError` gives "". Cost: one stat per entry, only off the exact path. |
| A4 | hooklib.py (new) | `is_story_with_pipeline(parent, name) -> bool` | — | `is_story_folder(parent, name) and (Path(parent)/name/"pipeline.json").is_file()`; an `OSError` gives False. |
| A5 | hooklib.py:341-343 | `_no_story` | its own twin comprehension | Use `alias_twins` (text unchanged). |
| A6 | hooklib.py:376 | `story_root` | `artifacts_dir(text, event)` | `artifact_root(event) / text`. **Invariant:** `story_root`'s alias refusal keeps its own `_no_story` text (pinned by `test_controller_task_flag.py`, a keep row). Its shape gate at :371 also calls `clean_key`, so `story_root('v1.')` and `artifacts_dir('v1.')` give the same answer (B3). |
| A7 | stage_guard.py:436 | `story_named_by_text` (resolve step 2) | `is_one_component` plus `.exists()` | `hooklib.is_story_with_pipeline(root, name)` |
| A8 | stage_guard.py:463 | `_names_story` | same with `is_file` | `is_story_with_pipeline` |
| A9 | stage_guard.py:620 | `resolve_ticket` step 1 (explicit) | same | `is_story_with_pipeline`. An alias falls into the existing deny "the explicit task id names no story" with identity facts. |
| A10 | stage_guard.py:642 | `resolve_ticket` step 5 (`QA_FACTORY_TASK`) | same | `is_story_with_pipeline` |
| A11 | stage_guard.py:715 | `_recipient_receipts` (resolve step 1b, `check_resume`) | same | `is_story_with_pipeline` |
| A12 | exit_gate.py:209-210 | `_named_ticket` | same (a story-key probe, not a file name) | `is_story_with_pipeline` |
| A13 | exit_gate.py:246 | `_identity` explicit task | "wins as written" | F3(a): `unknown-task` plus a scope fact whenever `task` is one component, not `is_story_folder(artifact_root(), task)`, and `other_spelling(artifact_root(), task)` is non-empty. An `artifact_root` `ValueError`/`OSError` leaves the task as today (that config failure belongs to the gate's existing paths). The downstream `_ticket_of` joins at :1162 and :1202 are covered through this. |
| A14 | bug_records.py:1393-1400 | `_story_exists` | gate | `hooklib.is_story_with_pipeline` |
| A15 | guard_pre_tool.py:820, 933, 1164/1170, 1237, 1290, 1304, 1452/1474/1484 | the big-read door, cases-root block, `dispatched_role`, rewrite door, two plan doors, owner check | `_STORY_RE` group(1) raw | One helper `_path_story(raw, event) -> str`: the raw key (`group(1)`, or "" with no match), replaced by `landing_name(artifact_root(event), key)` when that is non-empty. **Never raises:** any exception (a broken config from `artifact_root`, among others) returns the raw key, which is today's answer. Sites :1237, :1290 and :1304 are outside any try, :933 after one (t-328 N5). `story.group(0)` is still used for splitting (:1295, :1309). |
| A16 | host_dispatch.py:21-23 | `controller_record` | `is_one_component` plus a raw join | `is_story_folder(hooklib.artifact_root(root=root), ticket)`; an `artifact_root` `ValueError`/`OSError` gives None. |
| A17 | host_dispatch.py:310-311 | `record` spawn | `is_one_component`, then `artifacts_dir` | `is_story_folder(artifact_root(event), task)`; an alias or absent folder gives dispatch_id None, and the receipt is written. C3 later wraps the block. |

### 2.2 Changed: node OH8-2b

| # | Site | Function | Current | Change |
|---|---|---|---|---|
| B1 | estimate_record.py:43-48 | `task_binding` | `is_one_component`, then a raw join | Keep the shape check (OH6-1 text). `retro.md` counts only when `is_story_folder(artifact_root(root=project_root), task)`; otherwise the existing "retro.md must exist before recording the final estimate" `ValueError`. |
| B2 | role_load.py:542 | `_task_root` | `is_one_component` plus `is_dir` | `is_story_folder(artifacts, str(task))`; text unchanged |
| B3 | archive_task.py:194 | `cmd_archive` | raw join (even `../x` traverses) | `if not is_story_folder(artifact_root(), ticket)`: the existing not-found line, `EXIT_NOT_FOUND` |
| B4 | archive_task.py:235 | `cmd_undo` | same | same |
| B5 | audit_factory.py:528 | A5 seal | `art_dir.exists()` | `if not is_story_folder(artifact_root(), task): continue` |
| B6 | env_probe.py:745 | case preconditions | `task_root.exists()` | `is_story_folder(artifacts, task)`, else `out` |

### 2.3 Stays: why

| Site | Function | Current | Why it stays |
|---|---|---|---|
| controller.py:2489-2497 | `_story_names` | `samefile` | F7; proposed node §8 item 10 |
| execution_request.py:3246, 3258; 883 | — | gate / callers resolved | upstream gate |
| execution_scheduler.py:156 | `reconcile` lease adoption | `artifact_root()/str(lease["task"])` | The lease task is written by its acquirers. Pre-2a alias leases are covered by §3.2 (measured). An alias lease's job read is only for adopting an alive exact child (`_same_process`); otherwise it stays `blocked_orphan`, the safe side. Queued as an analog in §8 to gate it with `is_story_folder` |
| exit_gate.py:166, 817, 1126, 1254, 1500 | — | gate | exact |
| exit_gate.py:125-127, 168, 182, 289, 678, 819, 904, 1064, 1110, 1125, 1162, 1202, 1258, 1281, 1367, 1406, 1432, 1501, 1513, 1525, 1564, 1667 | various (`_ticket_of` at 1162, 1202) | raw join | the task comes from `_identity` (A13) or a stage lookup over real listing names |
| inject_context.py:325; 495, 641 | — | gate / resolve_ticket ticket | exact upstream; :495 in a try |
| local_keys.py:71, waiver.py:1154-1169, vcs_evidence.py:595, hooklib.py:388, 430 | — | gate | exact |
| traceability.py:1839 | `resolve` | raw join | `story_cli` at :1856 first |
| source_exclusions.py:540 | `task_dir_hint` | `artifact_root()/str(task)` | a path HINT printed in a command, never read; the command itself goes through `story_root` |
| subagent_journal.py:107; 171 | — | — | task from `_identity`; :171 in a try |
| worker_lifecycle.py:94, 115, 156, 210 | — | `artifacts_dir(receipt task_id)` in a try | the doubt side; pre-2a alias receipts: §3.2 |
| guard_app_under_test.py:66 | — | in a try | `{}` = no grant, a refusal (safe) |
| stage_guard.py:810, 997, 1141, 1283, 1293, 1748, 1842, 1849, 1885, 2692, 2769, 2894, 2936 | — | `artifacts_dir(ticket)` | the ticket comes from `resolve_ticket` or the pipeline `ticket` field; a pre-2a alias pipeline field: §3.2 |
| role_load.py:555, role_digest.py:324 | — | dispatch id | not a story key |
| exploration.py:134, 537, 734; manual_capture.py:343-373, 3137 | — | other id kinds | §8 |
| other CLI `artifacts_dir` callers (24 production files in total) | — | CLI key | A1 covers them; an alias gets a `StoryRootError` through each script's existing `ValueError` road (§8 item 4) |
| the session-id and pin-key uses | — | — | non-goal |

### 2.4 Changed: node OH8-6 (after 2a merged)

| # | Site | Function | Current | Change |
|---|---|---|---|---|
| C1 | host_dispatch.py:243 | `record` SubagentStop mark | `json.loads`, no try | `read_json(path, None, kind=dict, errors=Exception)`. None -> `person_signal(event, "host_receipt_unreadable", "host_dispatch: the receipt {path} cannot be read as a JSON object, so it was not marked terminal and was left as it is. Rewrite it as a JSON object or delete it; until then the worker it names may still count as running.", once_key=str(path))`, then `continue`. **SKIP.** |
| C2 | host_dispatch.py:270-283 | `record` `tool_use_id` scan | `json.loads` per file | Iterate `receipt_files(project_root(event), skipped=lst)`; one `person_signal` per skipped path ("… was skipped in the launch scan; rewrite or delete it"). **SKIP.** |
| C2' | host_dispatch.py:104-115 | `receipt_files` | silent skip | An additive `skipped: list \| None = None`; it receives the paths whose read is None. `{}` stays silent. Default callers are unchanged. |
| C3' | host_dispatch.py:286 | `record` -> `resolve_ticket(event)` | unguarded (`artifact_root` raises on a broken config) | Wrap it: `ValueError`/`OSError` -> `task, facts = "", {}` plus the C3 signal naming `qa-factory/config.json`; the receipt is still written (t-328 N2). |
| C3 | host_dispatch.py:310-317 | `record` controller lookup | `json.loads`, no try | One guard over the block: `artifact_root` error; a `read_json(..., None, kind=dict, errors=Exception)` read; `dispatches` not a dict -> no match; a non-dict entry skipped; no string `id` -> None. Failure -> `person_signal` ("… {path} cannot be read as a JSON object; the receipt was written without a dispatch id; `story_step.py bind` ties it later"); the receipt IS written. |
| C4 | refusal_registry.py:33-35 | module docstring, SCOPE paragraph only | 4 of 6 names | "Scanned refusal by refusal: the hook scripts in `SCANNED` that can end a dispatch before the role does any work: `stage_guard.py`, `inject_context.py`, `guard_pre_tool.py`, `native_context.py` (SubagentStart, and the packet `inject_context` stages), `codex_roles.py`, `host_adapter.py`. A refusal there is …". The two markers stay verbatim. |
| C5 | activity_capture.py:56-58 | `activity_path` migration | `json.loads`, no try | `read_json(source, None, kind=dict, errors=Exception)`. None -> no migration, the legacy file is left, the target is returned. No raise. |
| C6 | cost_capture.py:1945-1951 | `_capture` host binding | `json.loads`, no try; `binding['activity']` not a dict or `segments` empty raises at :1949-1950 | `read_json(..., None, kind=dict, errors=Exception)`. On None, OR when `binding.get('activity')` is truthy but not a dict, OR its `segments` is not a non-empty list of dicts: no inheritance (`binding = {}` for the read failure; for a shape failure the binding stays in the key but `activities` is not replaced). Then (i) the cost file's existing `telemetry_coverage` gets `"attribution": "incomplete: host_binding <path> unreadable"` (or `"… has no usable activity"`), so the report prints the gap (FR-41, P18); (ii) `person_signal(event, "host_receipt_unreadable", …, once_key=<path>)`. The session total is unchanged. |
| C7 | cost_capture.py:1963 | own cost file | `json.loads`, no try | STAYS (§8 item 6) |

**4c check of the hook-wired modules** (grep `json\.loads?\(` with `-i`; zero-hit files were checked in the same call as hit files):

| Module | Hits | Verdict |
|---|---|---|
| cost_capture.py | 26 | 24 guarded; 1946 -> C6; 1963 -> C7 |
| validate_artifacts.py | 15 | all in a try |
| host_probe.py | 10 | 222, 239, 272, 295, 489, 684, 963 local try; 805 raises by contract, caught at :792; 657 raises by contract, callers at :603 (try) and :699 (`check_child`, under `except Exception` at :725 per t-328): guarded |
| conductor_stop.py, precompact_guard.py | 0 | — |
| gate_shown.py, session_env.py, postcompact_reload.py, agent_autobind.py | 1 each | guarded |
| telemetry_hook.py | 4 | guarded |
| activity_capture.py | 3 | 63, 145 guarded; 57 -> C5 |

## 3. Edges, each with its invariant

**Global invariants.**
- I1: another spelling never yields another story's data at a reading site.
- I2: an exact existing key's answer is unchanged everywhere, with ONE named exception: a folder whose name ends in `.` or a blank (possible only on POSIX) is no longer a story to any leaf, on any OS (AR-4; `clean_key`).
- I3: a write the OS lands in story T is judged by T's rules, never by the absent-story pass.
- I4: `artifacts_dir` never returns a path the OS opens as an existing folder under another spelling.
- I5: no hook on these paths tracebacks; an unreadable receipt is never rewritten or marked terminal; a broken file never stops the new receipt.
- I6: SCOPE names every `SCANNED` module.
- I7: a story's price is never silently undercounted; incomplete attribution is marked.

### 3.1 Folder and key world

| Edge | Behaviour | Invariant |
|---|---|---|
| Folder ABSENT (before S0), clean key, no other spelling | `artifacts_dir` returns the path (create world); gates say "no story" as today | create works |
| Folder PRESENT, exact key | step 3 path; gates yes | I2 |
| Present; key `T.`, `T `, ` T`, `T..`, `T. .`, `...` | `clean_key` refuses in both `artifacts_dir` (step 2) and `is_story_folder` | I1, I4 |
| Present; key `t`, an 8.3 name, an alias of a junction or symlink story `TJ` (`tj`, `TJ.`) | `artifacts_dir` refuses via `other_spelling` (samefile hits the junction, 8.3 and case; casefold catches case on POSIX); gates say no; guard judges as `T`/`TJ` (`landing_name` samefile); exit_gate gives `unknown-task` | I1, I3, I4 (t-328 B1/B2) |
| Exact junction or symlink folder `TJ` | exact -> a story; guard judges TJ | I2 |
| Exact POSIX folder `v1.` | refused by both leaves; `story_root('v1.')` and `artifacts_dir('v1.')` agree (the shape refusal) | I2 exception (B3) |
| `T` and `t` both real (POSIX) | `t` exact -> passes; `T.` -> shape refused | exact wins |
| Full-width `Ｔ` (U+FF34) with `T` present | not casefold-equal and not samefile -> passes as its own key | no false refusal |
| Artifact root absent | `_listing` `[]`, `lexists` False -> the path | — |
| Root unlistable (rights) | `alias_twins` `[]`; `landing_name` cannot match against an empty listing -> "", so `artifacts_dir` passes as today (residual, named); `is_story_folder` says no (safe) | never raises |
| `samefile`/`lexists` raise | "" | never raises |
| Empty key, NUL, `/`, `\`, `:`, `.`, `..` | the existing one-component `ValueError` | OH6-1 green |
| 255 characters, folder exists (AT) | accepted (the cell is skipped with a reason where the OS cannot create it) | I2 |
| 256 characters (BEYOND) | `is_story_folder` False; `artifacts_dir` returns the path; no new limit | no exception |
| Guard: broken config | `_path_story` returns the raw key; the site behaves as today | P1 (N5) |
| Guard: `_STORY_RE` matches a literal `/artifacts/` that is not `artifact_root(event)` | `landing_name` lists the configured root; no match -> raw key: today's answer | named (§8 item 7) |
| exit_gate explicit `NOPE` | unchanged | §8 item 5 |

### 3.2 Data written BEFORE 2a (temporal world for data; t-328 N3)

An alias `task_id` or `ticket` already on disk changes readers' answers as follows. **The premise is measured first:** the 2a builder runs this read-only command as its FIRST step against the stand copy named in `docs/RUNBOOK.md` §11, and reports the counts. If the stand is not reachable, the builder says so and does not invent numbers. **If any alias is found, the builder stops and reports before writing code.**

```
python -B -c "import json,os,sys,pathlib; P=pathlib.Path(sys.argv[1]); A=P/'qa-factory'/'artifacts'; L=set(os.listdir(A)) if A.is_dir() else set(); f=lambda n: isinstance(n,str) and n and n not in L and any(n.rstrip(' .').casefold()==x.rstrip(' .').casefold() for x in L); r=[]; [r.append(('pipeline.ticket',d,json.loads((A/d/'pipeline.json').read_text('utf-8-sig')).get('ticket'))) for d in sorted(L) if (A/d/'pipeline.json').is_file()]; R=P/'qa-factory'/'state'/'host-dispatches'; [r.append(('receipt.task_id',p.name,json.loads(p.read_text('utf-8-sig')).get('task_id'))) for p in sorted(R.glob('*.json'))] if R.is_dir() else None; bad=[x for x in r if (x[0]=='pipeline.ticket' and x[2] not in (None,x[1])) or (x[0]=='receipt.task_id' and f(x[2]))]; print('folders',len(L),'rows',len(r),'alias_or_mismatch',len(bad)); [print(*b) for b in bad]" <stand project root>
```

The command is a pure read (CLAUDE.md hygiene pt. 4b). Its scope is pipeline `ticket` vs folder name and receipt `task_id` vs listing. Leases and journal tasks are counted by the builder with the same predicate if the first two show any alias.

| Pre-2a data | Reader | New answer | Door |
|---|---|---|---|
| receipt `task_id` alias | `worker_lifecycle.binding_is_active` :94 | `artifacts_dir` raises -> True (keeps the veto) | release the dispatch via `controller.py --operation release` (the text at :120) |
| same | `worker_lifecycle.guard` stop :210 | stop denied (`allowed` None) | the block's own text: `request_cancel` with cause and evidence |
| same | `host_dispatch.enrich` -> `resolve_ticket` step 1 | explicit alias -> deny "explicit task id names no story" with identity facts | the identity facts name the root and the stories; re-dispatch with the exact key |
| same | `exit_gate._identity` | `unknown-task` (full audit) plus the fact line | the audit header names it |
| same | `controller._story_names` | unchanged (F7) | — |
| lease `task` alias | `execution_scheduler` :156 | adoption of an alive exact child only; else `blocked_orphan` | existing scheduler doors |
| journal `task` alias | `audit_factory` A5 (B5) | skipped | — |
| pipeline `ticket` field alias | `stage_guard` :810 | `artifacts_dir` raises inside its existing `except` path | the guard's existing refusal |

### 3.3 Receipts, controller, cost (OH8-6)

| Edge | Behaviour | Invariant |
|---|---|---|
| Receipt `""`, `{`, `[]`, `null`, non-UTF-8 bytes, nesting beyond the parser | C1/C2: skip plus `person_signal`, bytes unchanged | I5 |
| Receipt `{}` | silent skip / `continue` (today) | — |
| Receipt deleted between `is_file` and read | C1 signal ("cannot be read") | I5 |
| Receipts folder absent | `[]` | — |
| Broken project config at `resolve_ticket` (C3') | task "", signal, receipt written | I5 (N2) |
| controller.json absent | dispatch_id None, no signal | — |
| controller broken, list, `dispatches` not a dict, non-dict entry, match without `id`; broken config at C3 | dispatch_id None, signal, receipt written | I5 |
| Broken receipt sorted before the matching good one (C2) | the good one is rebound | the `receipt_files` contract |
| Broken legacy activity spool (C5) | no migration, no raise | I5 |
| `host_binding` unreadable, or `activity` not a dict, or `segments` empty (C6) | capture completes; `telemetry_coverage.attribution` marker; signal | I7 |
| Requirement pair: intent 3 vs guard | OS truth wins for writes | I3 |
| Requirement pair: intent 1 vs `_story_names` | samefile stays (F7) | veto never lifted |
| Requirement pair: A1 vs `story_root` text | A6, with the shared `clean_key` | I2 and the test pin |

**Reused functions in a more consequential role: error direction and adversarial inputs.**
- `is_story_folder` (the gate of resolve steps 1, 1b, 2, 5, and of the B rows) errs to "no", which becomes a deny with identity facts. Must stay "no": `T.`, `T `, ` T`, `T..`, `...`, `t`, the 8.3 name, `T\0`, 256 characters, a FILE `T`, an exact POSIX `v1.`.
- `other_spelling` (inside `artifacts_dir` and `exit_gate._identity`) errs to "" on listing or stat failure, which means "pass as today". Must stay refused on a listable root: `T.`, `T..`, `T. .`, `T `, `...`, `t`, the 8.3 name, `tj` and `TJ.` for junction `TJ`. Must pass: `Ｔ`, a clean new key.
- `landing_name` (the guard) errs to "", meaning the raw key, today's answer. Must land on T or TJ: `t`, `T.`, the 8.3 name, `tj`, `TJ.`.
- `receipt_files(skipped=)` errs to skip, so a second receipt for one launch is possible; the skip is signalled.

## 4. Builder nodes

**Order: OH8-1 (t-321; accepted at wip/oh8-1 fd6e0f4, landing in wave 10) -> OH8-2a -> {OH8-2b ∥ OH8-6}.**
- 2a starts from `main` AFTER wave 10 has landed, or merges `main` before its first commit. OH8-1 makes `event_store` and `dependency_drift` call `hooklib.is_one_component`, and leaves `selftest` with a pinned mirror `_is_one_component` (`OH61_ALLOWED = {"selftest.py": 1}`). The sentinel dict (§5) is named for that world.
- Hot files (`hooklib.py`, `stage_guard.py`) belong to 2a alone. Function lists are given below (D-0048).
- **Census line:** `judgment-census.json` has three writers (2a, OH8-6 if C1 names a unit, and OH8-7 of t-321, which adds `SUBCLASS_PENDING_CEILING` and raises `blocking_per_role.conductor`). Whichever of them lands later merges `main` and re-runs `python -B ai-packages/qa-factory/scripts/tests/test_judgment_census.py` before its commit.

### OH8-2a
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\hooklib.py (is_one_component untouched; clean_key, is_story_folder, alias_twins, landing_name, other_spelling, is_story_with_pipeline, artifacts_dir, _no_story, story_root)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\stage_guard.py (story_named_by_text, _names_story, resolve_ticket, _recipient_receipts)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\exit_gate.py (_named_ticket, _identity)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\bug_records.py (_story_exists)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\guard_pre_tool.py (new _path_story; its 8 call sites)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\host_dispatch.py (controller_record, record lines 310-311 only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_resolver.py (new OH8-2 section and sentinel; OH6-1 rows untouched)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test-layers.json (the `covers` of test_resolver.py only: + bug_records.py, guard_pre_tool.py)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (the artifacts_dir row plus any unit C1 names)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\oh8-2a-alias-names.md

### OH8-2b
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\estimate_record.py (task_binding)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\role_load.py (_task_root)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\archive_task.py (cmd_archive, cmd_undo)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\audit_factory.py (the A5 seal function)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\env_probe.py (the case-preconditions reader at :745)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_resolver.py (2b rows of the OH8-2 table; sentinel counts)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test-layers.json (the `covers` of test_resolver.py only: + role_load.py, archive_task.py, audit_factory.py, env_probe.py)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\oh8-2b-alias-names.md

### OH8-6
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\host_dispatch.py (record, receipt_files)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\refusal_registry.py (module docstring, SCOPE paragraph only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\activity_capture.py (activity_path)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\cost_capture.py (_capture, the host_binding block only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_refusal_registry.py (new part_scope_docstring)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_codex_host.py (new broken-receipt table)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (only if C1 names a unit; else drop)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\oh8-6-broken-receipts-scope.md

OH8-7 (t-321 §B.7) owns the `refusal_registry.py` functions `_refusal_calls`, `sites` and `raise_family`, which do not overlap this node. A critic is mandatory (money).

## 5. Tests (every case is a row in an existing keep-row file; no new test file)

**OH8-2 table: `test_resolver.py` (keep, `table`).** A new section that reuses `_oh61_project`, `_oh61_outcome` and `_oh61_patched`.
- `OH82_NAMES`, with story `T` existing (with `pipeline.json`):
  - good `T`;
  - aliases `T.`, `T `, ` T`, `T..`, `T. .`, `...`, `t`;
  - `""`, `"T\0"`;
  - AT `"k"*255` (its folder created; a skipped cell prints why); BEYOND `"k"*256`;
  - full-width `Ｔ` (must be ACCEPTED as its own key: create world for `artifacts_dir`, "no story" for the gates);
  - `nt`: the 8.3 name of T when the OS yields one;
  - the junction cells: junction `TJ` (`nt`, `mklink /J` via `_winapi.CreateJunction`) or symlink `TJ` (POSIX), queried as exact `TJ` (accepted), `tj` and `TJ.` (other spelling);
  - POSIX: an exact folder `v1.` (refused by `is_story_folder`, `story_root` and `artifacts_dir` alike);
  - POSIX: `T` and `t` both real (`t` accepted exact).
- Rows (2a):
  - `artifacts_dir_read`;
  - `artifacts_dir_create` (`NEW` -> path; `NEW.` refused; `new` while `NEW` exists -> refused on every OS);
  - `story_root_text` (the near-miss text);
  - `is_story_with_pipeline`, `story_named_by_text`, `names_story`, `resolve_ticket_explicit`, `resolve_ticket_env`, `recipient_receipts`, `named_ticket`;
  - `identity_explicit` (other spelling, including the 8.3 and junction cells -> `unknown-task` plus the fact);
  - `bug_records_story_exists`;
  - `guard_owner_check` (`tj`, `TJ.`, `t`, the 8.3 name -> judged as the story: blocked with no open owner dispatch; `NOPE` -> allowed; a broken config -> raw key, no raise);
  - `controller_record`, `record_spawn`.
- Rows (2b): `estimate_record`, `role_load_task_root`, `archive_task` (bytes of T's `pipeline.json` unchanged), `audit_a5_seal`, `env_probe_preconditions`.
- A spy cell per row records that the site asked `is_story_folder`, `artifacts_dir`, `other_spelling` or `landing_name` about the exact name. This makes the table red on the old code on Linux too.
- Negative control: `is_story_folder` patched to the old pair turns the `nt` alias cells red.
- **Sentinel (AR-15, AR-20, shrink-only):** `is_one_component(` call sites per script equal an allow-dict, measured by the builder in the post-wave-10 world: OH8-1's `event_store`, `dependency_drift` and `selftest` state, plus `activity_capture`, `cost_capture`, `recover_codex_usage`, `red_sandbox`, `exploration`, `role_digest`, `role_load` (:555), `controller` (:2494), `waiver`, `estimate_record`, `subagent_journal`, and hooklib internal (including `clean_key`). Positive control: `controller.py` is present. `selftest`'s pinned mirror stays under OH8-1's `OH61_ALLOWED`; the new sentinel counts calls of `hooklib.is_one_component`, not mirrors.
- OH6-1 rows stay green.

**OH8-6: `test_codex_host.py` (keep).**
- A table over the receipt contents `""`, `"{"`, `"[]"`, `"null"`, `b"\xff"`, `"["*100000`, a valid object, `{}`, crossed with the columns: SubagentStop mark (C1), spawn scan with the broken file sorted first (C2), `resolve_ticket` broken config (C3'), controller variants (C3), legacy activity spool (C5), and cost capture (C6, also with `activity: 5` and `segments: []`, asserting the `telemetry_coverage.attribution` marker and a completed capture).
- Assertions: bytes unchanged, one `person_signal` per broken path (spy on `hooklib.person_signal`), the receipt written, no raise.
- **Red probe (mutation witness):** the same table run against the pre-change `record`, `activity_path` and `_capture` (kept as a byte copy in the test's scratch through `importlib` of the read-main version, or by patching `hooklib.read_json` back to a raising `json.loads`) must RAISE in the C1, C2, C3, C3', C5 and C6 cells. The witness shows red on old code and green on new.

**OH8-6: `test_refusal_registry.py` (keep).** `part_scope_docstring` with `_scope_gap(doc, scanned) -> (missing, extra)` over the span `Scanned refusal by refusal` … `A refusal there is`.
- Real -> empty.
- Each mutation turns it non-empty: remove `codex_roles.py`; add `x.py` to `SCANNED`; add `` `foo.py` `` in the span; a missing marker is reported.

## 6. DoD per node

**OH8-2a.**
- FIRST: the §3.2 measurement on the RUNBOOK §11 stand copy, with counts in the report; any alias -> stop and report before code.
- Acceptance: A0-A17; §3 edges; OH8-2 2a rows plus spies, negative control and sentinel green; OH6-1 and `test_controller_task_flag.py` green; the widened problem grep with its positive control, every hit in §2.
- Verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/hooklib.py ai-packages/qa-factory/scripts/stage_guard.py ai-packages/qa-factory/scripts/exit_gate.py ai-packages/qa-factory/scripts/bug_records.py ai-packages/qa-factory/scripts/guard_pre_tool.py ai-packages/qa-factory/scripts/host_dispatch.py`, then the printed files, plus `test_judgment_census.py` and `selftest.py --lang`.
- Commit lines: `architecture: AR-15, AR-13, AR-28, AR-4, AR-9, AR-29 -- …`; `judgment: adds data check hooklib.artifacts_dir`.

**OH8-2b.**
- Acceptance: B1-B6, 2b rows and spies, sentinel counts shrink-only.
- Verification: `scenario_walk.py --witness-for` over its 5 scripts, the printed files, `selftest.py --lang`.
- Commit lines: `architecture: AR-15, AR-28 -- …`; `judgment: none`.

**OH8-6.**
- Acceptance: C1-C6 with C2' and C3'; the 4c table in the report; the codex_host table plus its red probe; `part_scope_docstring` plus mutations; critic on the diff.
- Verification: `scenario_walk.py --witness-for ai-packages/qa-factory/scripts/host_dispatch.py ai-packages/qa-factory/scripts/refusal_registry.py ai-packages/qa-factory/scripts/activity_capture.py ai-packages/qa-factory/scripts/cost_capture.py`, the printed files, `selftest.py --lang`, plus the census line of §4 if it is the later writer.
- Commit line: `architecture: AR-13, AR-22, AR-28 -- …`.

## 7. SIBLING_MAP axes

- axis 1: n/a (no policy or role change)
- axis 2: n/a
- axis 3: covered (changelog.d fragments)
- axis 4: n/a
- axis 5: n/a
- axis 6: n/a
- axis 7: n/a
- axis 8: **covered**. The "ONE key -> story-folder rule" row gains `clean_key`, `other_spelling`, `landing_name`, `alias_twins`, `is_story_with_pipeline`, `artifacts_dir` and the readers A7-A17, B1-B6. The Lead edits the map with 2a.
- axis 9: n/a
- axis 10: n/a
- axis 11: n/a
- axis 12: covered (node statuses)
- axis 13: n/a
- axis 14: n/a
- axis 15: n/a
- axis 16: **covered** (C1, C3, C5, C6 call `read_json`)
- axis 17: n/a
- axis 18: **covered** (the new sentinel is shrink-only)
- axis 19: n/a
- axis 20: **covered** (C2 converges on `receipt_files`)
- axis 21: n/a
- axis 22: n/a
- axis 23: n/a
- axis 24: n/a
- axis 25: n/a
- axis 26: n/a
- axis 27: n/a
- axis 28: n/a
- axis 29: n/a
- axis 30: n/a
- axis 31: n/a
- axis 32: **covered** (census rows, `judgment:` lines, the later-writer line)
- axis 33: n/a
- axis 34: **covered** (one predicate, one outcome on every file system; the OS is asked through samefile, with no OS branch)
- axis 35: n/a
- axis 36: n/a

## 8. Analogs (queue; not widened)

1. The session-id and pin-key `is_one_component` uses (non-goal).
2. Exploration slug folders (`exploration.is_slug`).
3. manual_capture attempt names.
4. CLIs that print a traceback for an `artifacts_dir` `ValueError` (converge on `role_cli.run_guarded`).
5. exit_gate explicit `NOPE` (no folder, no other spelling).
6. cost_capture:1963: a broken own cost file (money; must not overwrite).
7. guard_pre_tool `_STORY_RE` matches only a literal `/artifacts/` (a custom `artifact_root` is not matched; unchanged from today).
8. CLOSED: host_probe `check_child` is under `except Exception` (:725; t-328).
9. execution_scheduler:156: gate the lease task with `is_story_folder`.
10. **Proposed node (F7 follow-up, t-328):** `controller._story_names` becomes `[t for t in receipt task_ids if landing_name(root, t) == folder name]`. Same veto answer, one road. To be opened by the coordinator.

## 9. Closed small choices

- Helper names and placement in hooklib.
- `names=` parameter shared by A2, A2b and A3, so A1 lists once.
- `receipt_files(skipped=)` as a keyword.
- estimate_record keeps the absent-story message.
- `.exists()` -> `is_file` at stage_guard:436.
- Test homes as in §5.
- The SCOPE text names the modules literally, plus a test.
- C6: guard the activity/segments shape rather than queue it.

## 10. Reading trail

Round 1 (read-main 303e89e):
- the t-323 digest, batch-8 rows, both findings;
- `hooklib.py` :255-470, :691-707, :751-793, :2476, :2559;
- `controller.py` :2460-2520;
- `host_dispatch.py` whole;
- `worker_lifecycle.py` :1-230;
- `stage_guard.py` :350-735, :1785-1834;
- `exit_gate.py` :115-300, :1900-1960;
- `bug_records.py` :1388-1401;
- `estimate_record.py` :25-69;
- `role_load.py` :525-569;
- `subagent_journal.py` :90-225;
- `role_digest.py` :305-333;
- `exploration.py` :126-137, :528-540, :726-737;
- `archive_task.py` :180-245;
- `execution_request.py` :870-894;
- `audit_factory.py` :515-537;
- `env_probe.py` :730-755;
- `traceability.py` :1825-1857;
- `manual_capture.py` :335-376, :3125-3141;
- `guard_pre_tool.py` (the `_STORY_RE` sites);
- `guard_app_under_test.py` :50-69;
- `inject_context.py` :310-334, :485-499, :625-646;
- `activity_capture.py` :40-65;
- `cost_capture.py` :1900-1969 and its wrappers;
- `host_probe.py` (the 4c sites);
- `refusal_registry.py` :1-100;
- `test_refusal_registry.py`;
- `test_resolver.py` :1433-1722;
- `test-layers.json` rows; `slow_tests.json`; `hooks.json`; `judgment-census.json` rows;
- `architecture.md` AR-13, 15, 17, 18, 22, 28, 29;
- SIBLING_MAP axes 8, 16, 20, 32-34; builder-rules 7b.

Round 2 (t-328 fix):
- the t-328 review whole;
- `execution_scheduler.py` :146-159;
- `exit_gate.py` :1196-1203;
- `source_exclusions.py` :535-542.

I relied on t-328's measurements (78 lines / 24 files, the junction probe, 44.7 µs, host_probe :725) through its trail, without re-running them.

Needed beyond the manifest: none.
