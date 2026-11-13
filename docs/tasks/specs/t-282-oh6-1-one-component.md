# t-282 — OH6-1: every copy of "a name is one path component" calls `hooklib.is_one_component` (designer draft, fix round t-291 applied)

Status: the draft, with the coordinator's fork decisions and the fixes of critic-on-plan t-286 (fix round t-291) applied.
Node `onboarding-hooks/6/OH6-1`. Line numbers were read on 13.11.2026 in the clean snapshot
`C:\QAFactory\forge-repo\.claude\worktrees\oh7-5` (origin/main 0a0db4f). Critic t-286 found that
`git diff --stat 0a0db4f origin/main -- ai-packages/qa-factory/scripts/` is empty at 79c38db, so the lines still hold.
Several of them have drifted from the batch row since it was written; §2 lists those.

## Dispatch header (R11-f)

given: this spec (marked, one hop: it carries the enumeration); `ai-packages/qa-factory/design/factory-rules.md` (whole, PROJECT.md "package change" p. 1); `plans/builder-rules.md` (whole); `ai-packages/qa-factory/design/architecture.md` AR-4, AR-13, AR-15, AR-20, AR-28, AR-29; `docs/TESTING.md`; `docs/SIBLING_MAP.md` axes 8, 18, 34; `plans/piles/onboarding-hooks/batch-6-ostatki-t-203-i-t-227.md` row OH6-1; `plans/piles/onboarding-hooks/findings/20261113-kopii-proverki-odnoj-komponenty-puti.md`; the eleven owned scripts below as they are on `origin/main`; `scripts/tests/harness.py`; `scripts/tests/test_role_digest_notes.py` (how a notes tail is built for `file_notes`); `references/sandbox-setup.json` (a valid row for `_row_problem`); `scripts/tests/test-layers.json` (row `test_resolver.py`)
owns:
C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\hooklib.py
C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\host_dispatch.py
C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\exit_gate.py
C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\stage_guard.py
C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\activity_capture.py
C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\cost_capture.py
C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\recover_codex_usage.py
C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\estimate_record.py
C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\red_sandbox.py
C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\role_digest.py
C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\tests\test_resolver.py
C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\tests\test-layers.json
non-goals:
- no length limit in `is_one_component` (OH6-2; the brief says "do not widen `is_one_component` beyond one component");
- no change to any site's answer other than for the inputs listed in §4;
- no edit of `worker_lifecycle.py` (OH5-11 already calls `artifacts_dir` there);
- no edit of `event_store.py`, `selftest.py` or `dependency_drift.py` (see §2.4, "Copies left to a named node");
- in `test-layers.json`, ONLY the `covers` list of the `test_resolver.py` keep row changes;
- no new axis in `docs/SIBLING_MAP.md`;
- no new test file.

handoff: a builder report per `.claude/agents/builder.md` rule 7. It contains:
- the commit hash on branch `wip/oh6-1` (like its siblings `wip/oh6-3`, `wip/oh6-4` and `wip/oh6-5`);
- the verbatim witness output;
- the FR walk by section;
- the table of §2 with the new line numbers.

The worktree `C:\QAFactory\forge-repo\.claude\worktrees\oh6-1` does not exist at spec time. The dispatch creates it, after a push (`tools/dispatch_gate.py`). Every owns path above refers to that tree.

edges: §4 (the edge table) and §3 (the positional invariants per site).

DoD: §6. The verification run is `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <the twelve owns paths>`, plus every file it prints (scope rule in §6, item 5).

siblings: axis 8 (where the story is on disk: the key -> folder rule); axis 34 (one road); axis 18 (the sentinel's allowance is shrink-only). Copies of the same class outside this node: §2.4.

designer: this draft (t-282), after Lead acceptance; fix round t-291.

Order: the per-file order is satisfied. OH5-11 and `wip/oh3-36` are merged into origin/main. OH5-10 and OH5-13 write no OH6-1 path: OH5-10 writes `native_context.py`, and OH5-13 writes `session_identity.py` and `guard_pre_tool.py` (batch-5 rows l.41 and l.44, as read by critic t-286).

Coordinator moves before the dispatch. They are outside this file and are not the builder's:
- (i) Batch 6 is taken, so it is frozen. Add one "Ход" line to `plans/piles/onboarding-hooks/batch-6-ostatki-t-203-i-t-227.md` naming the added paths of OH6-1: `scripts/estimate_record.py`, `scripts/red_sandbox.py`, `scripts/role_digest.py` and `scripts/tests/test-layers.json` (`covers` only). This is t-286 fix 1(k).
- (ii) File the finding "is_one_component copies outside OH6-1" (§2.4).
- (iii) File the findings F-3 and F-8. The F-8 finding names the widened quiet class (see F-8), and each finding is placed into a non-taken batch in the same move (D-0044).

## §1. Invariants and owners

| AR | how this node touches it | change check written into the DoD |
|---|---|---|
| AR-15 (one survivor, wired everywhere) | 9 hand copies of the row, plus 3 more copies (`estimate_record`, `red_sandbox`, `role_digest`) and 1 missing guard (`resolve_ticket` explicit route), become calls of `hooklib.is_one_component`. `is_story_folder` keeps only its extras | DoD 1: grep for the problem, not the helper. The sentinel (§5 Part B) is the detector. Every copy found by grep is either wired in (§2.2) or named for one node (§2.4) |
| AR-13 (a fact with a reader is read only through it) | "is this a single path component" has one reader | DoD 2: no hand copy remains in any owned file. The sentinel is green, and its only allowance is the two named sites of §2.4 |
| AR-29 (a code check judges data) | every altered check is a SHAPE check of a name; none judges a role's content | DoD 6: run `test_judgment_census.py`. Expected: no row added, none removed, no count raised. No check unit is created or deleted: every refusal site stays in its function, and `red_sandbox._component` has no census row (grep of `judgment-census.json`). A raised count is named in the verdict (AR-20) |
| AR-20 (shrink-only ratchets) | the sentinel's allowance is `{"event_store.py": 1, "selftest.py": 1}`, shrink-only, and each entry points to the §2.4 node | DoD 2: the allowance is exactly that literal. Any addition is a named raise. The node of §2.4 shrinks it to `{}` |
| AR-28 (an unknown never becomes a pass) | NUL and non-str inputs used to pass the copies or crash them. Now they are refused, in each site's own direction | DoD 3: the NUL column of the table |
| AR-4 (no tie to one machine) | `\` and `:` are refused on every OS. This is new for `estimate_record` (`:`), `red_sandbox` (`:`) and `role_digest` (`\` and `:` on POSIX) | DoD 3: the `a\b` and `a:b` columns |

The owner and census class of every check that the node adds or alters (AR-29, P27):

| check | owner | census class | census row (judgment-census.json) |
|---|---|---|---|
| `hooklib.is_one_component` (gains NUL) | data (code) | shape | none. It is not a check unit; units call it |
| `hooklib.is_story_folder` (its own prefix replaced by the survivor) | data | shape | none |
| `host_dispatch.controller_record` | data | shape | none (no refusal site; it returns None) |
| `exit_gate._named_ticket` | data | shape | none |
| `stage_guard.story_named_by_text`, `resolve_ticket` (env route and explicit route), `_recipient_receipts` | data | shape | none |
| `activity_capture.activity_path` | data | shape | `activity_capture.py::activity_path` shape/data (l.8), unchanged |
| `cost_capture._capture`, `cost_capture.main` | data | shape | none |
| `recover_codex_usage.recover` (gains `.`, `..` and NUL) | data | shape | `recover_codex_usage.py::recover` shape/data (l.678), unchanged |
| `estimate_record.task_binding` (gains `:` and NUL) | data | shape | `estimate_record.py::task_binding` xref/data (l.263), unchanged: the unit's class is decided by its other checks |
| `red_sandbox._row_problem` (pins keys and `must_not_preexist`; `_component` deleted) | data | shape | none |
| `role_digest.file_notes` | data | shape | none |
| the sentinel in `test_resolver.py` | data (code detector) | shape. It is a test, outside the census, because `scripts/tests/` is not scanned | — |

FR sections touched:
- A: no refusal text changes, and every ValueError and problem string keeps its words.
- B: no text shown to a person.
- C: FR-13 (none of this is open variety) and FR-14 (no output shape changes).
- D: FR-17 (the tool is wired wherever the problem occurs).
- E and F: not touched.
- G: FR-32 and FR-54.

Principles: P31 (one road) and P12.

## §2. Call sites

### 2.1 The survivor and the leaf (`hooklib.py`, a hot file)

| function | current line (verified) | change |
|---|---|---|
| `is_one_component` | :269-272. The batch row says :233, which has drifted. Body: `return isinstance(name, str) and bool(name) and name not in (".", "..") and not any(c in name for c in "/\\:")` | The separator literal becomes `"/\\:\0"` (the Lead's fork, decided: NUL is refused). The docstring names NUL. Nothing else changes: no strip, no length |
| `is_story_folder` | :305-320, with the prefix at :317-318. The row says :266, which has drifted. Today: `not isinstance(name, str) or not name.strip() or name != name.strip() or name in (".", "..") or any(c in name for c in "/\\:\0") or parent is None or not str(parent).strip()` | `not is_one_component(name) or not name.strip() or name != name.strip() or parent is None or not str(parent).strip()`. The answer is unchanged for every input (critic t-286 confirmed the equivalence) |

The error direction of the survivor in its role as the one gate (designer rule 1):
- It may err only toward **False** (refusal), and it never raises, for any input.
- Adversarial inputs that must stay False: `""`, `"."`, `".."`, `"/a"`, `"a/b"`, `"a\\b"`, `"C:x"`, `"a:b"`, `"a\0b"`, `"\0"`, `None`, `5`, `[]`, `b"ab"`.
- The invariant: **at no site does the survivor accept a name that the site's old copy refused.** Every old copy's refusals are a subset of the survivor's (§4). So the change only moves inputs from "accepted" to "refused", never the other way.

### 2.2 The sites (rows 1-9 are the batch row; rows 10-13 were folded in by the coordinator's decision on F-1 (a))

A closed choice (C-1): every new call is written `hooklib.is_one_component(x)` (attribute access), so that one spy on the `hooklib` module sees every site.

| # | site | current line (verified 13.11) | current error direction | new call |
|---|---|---|---|---|
| 1 | `host_dispatch.controller_record` | :21 (the row says :21). `if not ticket or not dispatch or ticket in (".", "..") or any(char in ticket for char in "/\\:"): return None`. `import hooklib` is local at :19 | `None` | `if not dispatch or not hooklib.is_one_component(ticket): return None` (ticket is already `str(ticket or "")` at :20) |
| 2 | `exit_gate._named_ticket` | :208-209 (the row says :209). `[name for name in facts.get("named") or [] if name not in (".", "..") and not any(c in name for c in "/\\:") and (root / name / "pipeline.json").is_file()]` | the name is dropped from `in_text` | `... if hooklib.is_one_component(name) and (root / name / "pipeline.json").is_file()]`, plus a new line `import hooklib` |
| 3 | `stage_guard.story_named_by_text` | :435-437 (the row says :436). `if name not in (".", "..") and not any(c in name for c in "/\\:") and (root / name / "pipeline.json").exists()` | the candidate is dropped | `if hooklib.is_one_component(name) and (root / name / "pipeline.json").exists()` (`import hooklib` exists at :81) |
| 4 | `stage_guard.resolve_ticket`, step 5 (the env route) | :643-645 (the row says :643). `if env_task and not any(c in env_task for c in "/\\:") and env_task not in (".", "..") and (root / env_task / "pipeline.json").is_file(): return env_task, facts` | the route is skipped and control falls to `_env_exploration` (:646) | `if hooklib.is_one_component(env_task) and (root / env_task / "pipeline.json").is_file(): return env_task, facts` |
| 5 | `stage_guard._recipient_receipts` | :716-718 (the row says :717). `... and isinstance(story, str) and story and not any(c in story for c in "/\\:") and story not in (".", "..") and (root / story / "pipeline.json").is_file()` | the receipt is skipped | `... and hooklib.is_one_component(story) and (root / story / "pipeline.json").is_file()` |
| 6 | `activity_capture.activity_path` | :44 (the row says :44). `if not session or session in {".", ".."} or any(c in session for c in "/\\:"): raise ValueError("session identity must be a single safe component")` | `ValueError` | `if not hooklib.is_one_component(session): raise ValueError(<same text>)`, plus a new line `import hooklib` |
| 7 | `cost_capture._capture` | :1907 (the row says :1907). `if not tpath.is_file() or any(c in session_id for c in "/\\:") or session_id in (".", ".."): sys.exit(0)` | `sys.exit(0)` | `if not tpath.is_file() or not hooklib.is_one_component(session_id): sys.exit(0)`, plus a new line `import hooklib` |
| 8 | `cost_capture.main` | :3800 (the row says :3800). The same condition, followed by `return` | `return` | `if not tpath.is_file() or not hooklib.is_one_component(session_id): return` |
| 9 | `recover_codex_usage.recover` | :16 (the row says :16). `if not session or any(c in session for c in '/\\:'):raise ValueError('Unsupported session identity')`. Single quotes; no `.`/`..` guard | `ValueError` | `if not hooklib.is_one_component(session):raise ValueError('Unsupported session identity')`, plus a new line `import hooklib`. The import resolves: the file already imports `activity_capture`, which imports `hooklib` from `scripts/`. New: `.`, `..` and NUL are refused |
| 10 | `estimate_record.task_binding` | :42. `if not task or task in {'.','..'} or '/' in task or '\\' in task: raise ValueError('task must be a single task identifier')`. No `:` guard: on Windows, `PureWindowsPath('D:/root') / 'C:x'` gives `C:x`, so the task escapes the artifact root (measured by critic t-286) | `ValueError('task must be a single task identifier')` | `if not hooklib.is_one_component(task): raise ValueError('task must be a single task identifier')`, with a local `import hooklib` beside the local import at :41 |
| 11 | `red_sandbox._component` (:313-315), used at `_row_problem` :335 (pins keys) and :339 (`must_not_preexist`) | `isinstance(name, str) and bool(name) and name not in (".", "..") and not any(sep in name for sep in ("/", "\\"))`. No `:` and no NUL | the problem strings `"pins (a non-empty {file name: request field})"` / `"must_not_preexist (a non-empty list of names)"` | DELETE `_component` (it has no caller outside the file: Grep `\b_component\b` over `scripts/`). Call `hooklib.is_one_component(k)` at :335 and `hooklib.is_one_component(n)` at :339. `import hooklib` exists at :82. The data rows of `references/sandbox-setup.json` (pins `package.json` and `package-lock.json`) do not change their answer |
| 12 | `role_digest.file_notes` | :323. `if not tail or not name or name != Path(name).name or name in (".", ".."): return ""`. This form depends on the OS | `""` (never raises) | `if not tail or not hooklib.is_one_component(name): return ""`, plus a new line `import hooklib` after :37 |
| 13 | `stage_guard.resolve_ticket`, step 1 (the explicit route) | :621. `if (root / explicit / "pipeline.json").is_file(): return explicit, facts`, with NO component check. When `explicit` is non-empty (:615), the function always returns from inside the block (:612-626) | the explicit id is joined unchecked; a missing story gives `("", facts)` after the explain block | `if hooklib.is_one_component(explicit) and (root / explicit / "pipeline.json").is_file(): return explicit, facts`. The rest of the block is unchanged (see §3: never fall through) |

Out of the row on purpose: `worker_lifecycle.py:94`. On main it now reads through `hooklib.artifacts_dir(task, event, root=root)` (OH5-11 is merged), and so do :114-115, :154-156 and :202-210. The copy is gone.

Callers of the survivor that already exist, and whose answer changes ONLY for a name holding NUL. Each moves to its own refusal direction, and none needs an edit:
- `artifacts_dir` :280
- `story_root` :371
- `controller.py:2494`
- `exploration.py:134`, `:537` and `:734`
- `host_dispatch.py:310`
- `role_load.py:542` and `:555`
- `waiver.py:1154` and `:1169`
- `subagent_journal.py:107`
- `stage_guard.py:464`

### 2.3 Searches (trail)

All searches were run with the Grep tool over the snapshot's `scripts/*.py`. The positive control is that each pattern found the known sites.
- (a) `in ['"]/\\\\:` found the 9 row sites, `hooklib.py:272` and `hooklib.py:318`.
- (b) `for \w+ in ['"][^'"]*(\\\\|/)[^'"]*['"]\)` found the same set plus `vcs_evidence.py:407` (`"/@ \t"`, a VCS host key; not a copy).
- (c) The `.`/`..` guard in tuple or set form found `estimate_record.py:42`, `red_sandbox.py:314`, `role_digest.py:323`, `event_store.py:482`, `manual_capture.py:295` and `session_identity.py:49`.
- (d) Added in fix round t-291 after critic t-286: `!= Path\(\w+\)\.name|basename\(row\["file"\]\) != ` found `event_store.py:482`, `role_digest.py:323`, `selftest.py:982` and `dependency_drift.py:92`.
- `stage_guard.py:621` (row 13) was found by reading `resolve_ticket`.

Not copies, because each applies a stricter allow-list of characters, which is a different rule: `session_identity._component` :48-49 (`SAFE_ID = [A-Za-z0-9._-]{1,128}`) and `manual_capture.case_dir_name` :287-299.

### 2.4 Copies left to a named node

These go to the finding to be filed: onboarding-hooks, "is_one_component copies outside OH6-1". It is ONE new node, filed by the coordinator, and its owner is the Lead of onboarding-hooks. Its sites are not touched here.

| site | line | form | why not in OH6-1 |
|---|---|---|---|
| `event_store.EventStore.__init__` (`stale_marker`) | :482 | `marker != Path(marker).name or marker in (".", "..")`; ValueError | a core file that OH6-3 owns; the node comes after OH6-3 |
| `selftest._slow_tests_problem` | :982 (def at :964) | `if not name or name != Path(name).name:` returns an error string. `..` passes (`Path('..').name == '..'`) | `selftest.py` is in the zone of `onboarding-forge/2` (nodes SC2-23 and SC2-26): a queue line, or a D-0048 function list |
| `dependency_drift.load_table` | :92 (def at :78) | `os.path.basename(row["file"]) != row["file"]` returns `(None, problem)`. `..` passes | it belongs with the other two, so all three become one node |

The sentinel's allowance (§5 Part B) names `event_store.py` and `selftest.py` with this pointer. `dependency_drift.py` is outside the sentinel's patterns, because the basename form is a named blind spot.

## §3. The POSITIONAL invariant at each site

| site | where the call stands | what must stay refused or unreachable |
|---|---|---|
| `is_story_folder` | the survivor is called FIRST, before `name.strip()` | A non-str `name` never reaches `.strip()`. A name that is not one component never reaches `_listing` |
| `controller_record` | before `hooklib.artifact_root(...) / ticket` | No `read_json` is issued on a path built from a ticket that is not one component. The answer is None on every doubt |
| `_named_ticket` | inside the comprehension, before the `.is_file()` join | A name that is not one component never becomes `in_text`. `""` can no longer probe `<artifact root>/pipeline.json` |
| `story_named_by_text` | before the `.exists()` join | The same. `by_line` reads only from `existing`, so a refused name cannot settle a story through the `Ticket:` line either |
| `resolve_ticket` env route (step 5) | after the event's own routes and BEFORE `_env_exploration` and the guess; the position does not change | A refused `env_task` is never returned. It still REACHES `_env_exploration`: an `explore:<slug>` value carries a `:` and must go on to that route |
| `resolve_ticket` explicit route (step 1) | the survivor joins the `is_file()` condition at :621, INSIDE the `if explicit:` block | `facts["explicit"]` and `facts["explicit_source"]` are still set (the identity refusal prints them), the explain block (`load_config`, `key_form`, `_collect_story_facts`) still runs, and the answer is `("", facts)`. A refused explicit NEVER reaches `_resume_recipient_story`, `story_named_by_text`, the slug, `$QA_FACTORY_TASK` or the single-story guess. The event's word is never overruled by a guess. Wrapping the whole block in the check is the defect this row forbids |
| `_recipient_receipts` | after `binding_names` and the dispatch test, before the `.is_file()` join | A receipt whose `task_id` is not one component is neither evidence nor a veto |
| `activity_path` | the first statement, before `project_root(event)` | No path is computed and no legacy move happens (`source.unlink()` at :57) for a refused session |
| `_capture` | before `_session_scope_ok` | A refused id writes nothing |
| `main` | after `metadata(tpath)` may replace `session_id` (:3794-3798), and before `--debounced`, the marker and the lock | The check runs on the FINAL `session_id`, and no marker or lock is created for a refused id |
| `recover` | right after `metadata(transcript)`, before `scan` | Nothing is scanned or written, and no subprocess is started |
| `estimate_record.task_binding` | the first statement after the local imports, before `artifact_root(...) / task` | No `retro.md` or `controller.json` is read from outside the artifact root. The refusal text stays `'task must be a single task identifier'`, not the later "retro.md must exist" |
| `red_sandbox._row_problem` | inside the same `all(...)` at :335 and :339; the pins value test `isinstance(v, str) and v` stays | A pins key or a `must_not_preexist` name that is not one component makes the row a problem, with the same problem string |
| `role_digest.file_notes` | before `Path(task_root).joinpath(...)` and `mkdir` | No notes file is written outside `<task root>/state/findings/` for a refused id, and the function never raises |

## §4. Edge table

The cells give the answer AFTER the change, and BEFORE where it differs. Sites are numbered as in §2.2.

| input | survivor | 2/3/4/5 (skip / next route) | 13 (explicit -> `""`) | 1 (None) | 6 (ValueError) | 7/8 (exit / return) | 9 (ValueError) | 10 (ValueError) | 11 (problem) | 12 (`""`) | invariant protected |
|---|---|---|---|---|---|---|---|---|---|---|---|
| NUL `a\0b` | False (new) | skipped. Before: passed; `is_file()` is False on Python 3.12 (measured by t-286) | `""`. Before: same result through `is_file()` False | None. Before: same result | ValueError. Before: a NUL path was returned | quiet exit. Before: crashed at the write | ValueError. Before: passed | ValueError (same text). Before: passed, then "retro.md must exist" | problem. Before: accepted | `""`. Before: same result (the write failed inside `except (OSError, ValueError)`) | a name with NUL never reaches an OS call |
| `""` | False | skipped. Before: sites 2 and 3 PASSED it, so `<artifact root>/pipeline.json` was probed | unreachable (`if explicit:`) | None | ValueError | unreachable (`is_file()` fails first) | ValueError | ValueError | problem | `""` | an empty name never names the artifact root |
| whitespace-only | True (unchanged) | site 4 unreachable (stripped at :602); 2/3/5 unchanged | unchanged | unchanged | unchanged | unchanged | unchanged | unchanged | unchanged | unchanged | no change; NTFS aliases are F-3 |
| very long | True (unchanged) | unchanged | unchanged | unchanged | unchanged | unchanged | unchanged | unchanged | unchanged | unchanged | OH6-2 (F-7) |
| non-str | False | 5: reachable, refused as before; 2/3/4 unreachable | unreachable (`str(...)`) | unreachable (`str(ticket or "")`) | ValueError. Before: TypeError, or unhashable for a list | quiet exit / return. Before: a TypeError traceback (F-8) | ValueError. Before: TypeError for an int; a list or dict passed silently, and `recover` returned a dict carrying it | ValueError. Before: TypeError (`'/' in 5`) | problem (unchanged: `isinstance`) | unreachable (`str(dispatch_id or "")`) | refused in the site's direction, never a crash in a hook |
| `.` / `..` | False | skipped (unchanged) | `("", facts)`. Before: `root/../pipeline.json` was joined, and `..` was returned as the story if that file existed (a hole) | None | ValueError | exit / return | ValueError (NEW) | ValueError (unchanged) | problem (unchanged) | `""` (unchanged) | no name climbs or stays on the parent folder |
| `a/b`, `a\b`, `a:b` | False | unchanged | `("", facts)`. Before: joined unchecked | unchanged | unchanged | unchanged | unchanged | `a:b` NEW (before: passed; on Windows `C:x` escapes the root) | `a:b` NEW (before: accepted) | `a\b` and `a:b` NEW on POSIX (before: passed); unchanged on Windows | one component on every OS (AR-4) |
| `explore:<slug>` in `$QA_FACTORY_TASK` | False | site 4: skipped, then reaches `_env_exploration` (unchanged) | — | — | — | — | — | — | — | — | the exploration route stays reachable |

Conflicting requirements: none. "Keep each site's direction" and "refuse NUL / `:`" agree, because the new refusals only join each site's existing refusal set.

## §5. Tests (`test_resolver.py`: a keep row of layer `table`, not quarantined)

`test-layers.json` puts `test_resolver.py` under `keep` (l.4320, layer `table`). The `quarantine` section starts at l.7004, and the file name appears once. The change to `test-layers.json` (coordinator decision F-2 (a)): add `activity_capture.py`, `cost_capture.py`, `estimate_record.py`, `exit_gate.py`, `host_dispatch.py`, `recover_codex_usage.py`, `red_sandbox.py`, `role_digest.py` and `stage_guard.py` to the `covers` list of the `test_resolver.py` row. Nothing else in the file changes. No new test file.

### Part A: ONE parameterised table, `oh6_1_one_component_table()`

The columns are the names `..`, `.`, `a/b`, `a\b`, `a:b`, `a\0b` and the good name `T`. A check id is `OH6-1 <id>-<label>`, where `<id>` is the literal in the first column below and `<label>` is one of `dotdot`, `dot`, `slash`, `backslash`, `colon`, `nul` or `good`. There is one `check(...)` per cell, in the `harness.check` style.

| id | caller | how the name reaches the check | refused (6 bad names) | good name `T` |
|---|---|---|---|---|
| `is_one_component` | `hooklib.is_one_component` | direct | `False` | `True` |
| `is_story_folder` | `hooklib.is_story_folder` | `(<artifact root>, name)`; folder `T` exists | `False` | `True` |
| `controller_record` | `host_dispatch.controller_record` | `(project, name, "D")`; `T/state/controller.json` holds dispatch `D` | `None` | the record dict |
| `named_ticket` | `exit_gate._named_ticket` | stub `exit_gate.SG.resolve_ticket` -> `(name, {"named": [name]})` | `("", ...)` | `("T", ...)` |
| `story_named_by_text` | `stage_guard.story_named_by_text` | stub `stage_guard.AF.keys_in` / `labelled_keys` -> `[name]` | `""` | `"T"` |
| `resolve_ticket_env` | `stage_guard.resolve_ticket`, step 5 | `QA_FACTORY_TASK=name`; the event names nothing; TWO stories `T` and `U`, so the guess answers none | result `""` (`!= name`) | `"T"` |
| `resolve_ticket_explicit` | `stage_guard.resolve_ticket`, step 1 | event `{"task_id": name}`; exactly ONE story `T` on disk, so a fall-through would answer `T` through the guess | `("", facts)` with `facts["explicit"] == name` | `("T", facts)` |
| `recipient_receipts` | `stage_guard._recipient_receipts` | a receipt with `task_id=name`, `dispatch_id="D"` and the target among its names | `[]` | `[("T", "D")]` |
| `activity_path` | `activity_capture.activity_path` | `({"cwd": project}, name)` | `ValueError` | a `Path` ending in `T.json` |
| `cost_capture_capture` | `cost_capture._capture` | event `{session_id: name, transcript_path: <existing file>}`; a recording stub on `cost_capture._session_scope_ok` | `SystemExit(0)`, with the stub NOT reached | the stub reached |
| `cost_capture_main` | `cost_capture.main` | the project carries `qa-factory/config.json`; the transcript is an existing file for which `codex_usage.metadata` returns no `id` (stub `codex_usage.metadata` -> `{}`; the import is local, so patch the module attribute); stub `_choose_subagent_transcript` to a no-op; stub `read_event`; `--debounced` in argv; a recording stub on `_debounce_window_open` (returns True); `_ends_dispatch` -> False | return, with the stub NOT reached | the stub reached |
| `recover_codex_usage` | `recover_codex_usage.recover` | `transcript` is an existing (empty) file; stub `recover_codex_usage.metadata` -> `{'id': name}` and `scan` -> `([], 'x')`; `boundaries=[]`; `write=False` | `ValueError` | the result dict |
| `estimate_record` | `estimate_record.task_binding` | `(project, name)`; story `T` has `retro.md` and `state/controller.json` with a `source_revision` | `ValueError` whose text is `'task must be a single task identifier'` | the binding dict |
| `red_sandbox` | `red_sandbox._row_problem` | a valid row (copied from `references/sandbox-setup.json`), checked twice: once with `pins={name: "field"}` and once with `must_not_preexist=[name]` | the problem strings starting `"pins ("` and `"must_not_preexist ("`, respectively | neither problem string (`""`, or a problem about another key) |
| `role_digest` | `role_digest.file_notes` | `(tmp task root, name, a message with a notes tail, built as in test_role_digest_notes.py)` | `""`, and no file written | a task-relative path, and the file exists |

Two rules make the table proof against mutation:
1. **Reachability.** For every bad name whose unguarded join can be CREATED on the running OS, the fixture creates the file that the site would read. That means `..` and `.` everywhere, `a/b` everywhere, and on POSIX also `a\b` and `a:b` as literal names. Then only the guard can produce "refused". Where the file cannot be created (NUL everywhere; `a:b` on Windows), rule 2 carries the proof.
2. **Spy.** In the same pass, a spy on `hooklib.is_one_component` records its arguments, using the B4 pattern of this file: replace, call, restore in `finally`. Every cell asserts that the spy saw the exact name; the id is `OH6-1 <id>-<label> asked the survivor`. Only the `is_one_component` row is exempt. The `is_story_folder` row is NOT exempt: a bare name inside `hooklib` is a global lookup in `hooklib.__dict__`, which the spy rebinds, so this column proves that the reduction of §2.1 was made.

The stated mutation (DoD 4): remove the guard from `recover_codex_usage`. Then `OH6-1 recover_codex_usage-dotdot` must turn red.

### Part B: the census sentinel, `oh6_1_sentinel()`

Three patterns, taken from critic t-286 fix 3:
- `COPY = r"""for \w+ in ['"]/\\\\:"""`: any loop variable name, either quote form, with the literal slash, two backslashes and a colon.
- `TUPLE = r"""for \w+ in \(\s*['"]/['"],\s*['"]\\\\['"]"""`: the tuple form (`red_sandbox.py:315` today).
- `PATH_NAME = r"!= Path\(\w+\)\.name"`: the `Path(x).name` form.

Scan: every `scripts/*.py` except `hooklib.py`, line by line, with all three patterns.
- The expected hits equal the allowance: `ALLOWED = {"event_store.py": 1, "selftest.py": 1}`. Each entry carries a comment pointing to the finding "is_one_component copies outside OH6-1" (§2.4). The allowance is shrink-only (AR-20).
- A file with more hits than its allowance is red. So is any file not in the allowance that has a hit.
- An allowance entry with fewer hits than allowed is also red, with the message "shrink the allowance": a stale entry is never kept silently.

`hooklib.py` is checked separately. It must have exactly ONE `COPY` hit, inside `is_one_component`, and no `TUPLE` or `PATH_NAME` hit.

Stated blind spots, written in the sentinel's docstring:
- the `'/' in x or '\\' in x` form (as a regex it hits 8 path-vs-name checks that are not copies);
- `os.path.basename(x) != x` (it also hits `reporters.py:455`, which is not a copy);
- a reordered literal such as `"\\/:"`.

For these forms, the Part A spy table and the §2.4 node are the detectors.

Controls:
- Positive: each pattern finds a fixture string written in the test so that the runtime string carries the backslashes. The fixtures are `for c in "/\\:"`, `for char in '/\\:'`, `for sep in "/\\:\0"`, `for sep in ("/", "\\")` and `name != Path(name).name`.
- Negative: `for c in "/@ \t"` (`vcs_evidence.py`) is not flagged.
- Differential: `recover_codex_usage.py` line 16, as it stands on main today, is flagged by `COPY`. `red_sandbox.py` line 315, as it stands today, is flagged by `TUPLE`.

## §6. DoD (inline)

1. Every site of §2.2 (rows 1-13) calls `hooklib.is_one_component` as the "new call" column says, with its direction unchanged. `red_sandbox._component` is deleted, and `is_story_folder` is reduced as in §2.1. The survivor refuses NUL. Every ValueError text and problem string is kept byte for byte.
2. The Part B sentinel is green with `ALLOWED = {"event_store.py": 1, "selftest.py": 1}`, each entry pointing to §2.4, and all its controls pass.
3. The Part A table is green: 15 rows × 7 names = 105 cells, plus the spy column (14 rows × 7 = 98 cells).
4. The mutation of §5 is run once by hand: take a byte copy before, restore from it, and use a hash comparison as the witness (command hygiene pt. 7). The red id `OH6-1 recover_codex_usage-dotdot` is quoted.
5. Witness (`plans/builder-rules.md` 7b):
   `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\hooklib.py C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\host_dispatch.py C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\exit_gate.py C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\stage_guard.py C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\activity_capture.py C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\cost_capture.py C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\recover_codex_usage.py C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\estimate_record.py C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\red_sandbox.py C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\role_digest.py C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\tests\test_resolver.py C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\tests\test-layers.json`
   - Run every file it prints with `python -B scripts/tests/<file>.py`, and paste the output verbatim.
   - The slow files of PROJECT.md "package change" p. 2 (`SLOW_TESTS`, `test_story_run_*`, `test_controller_*`, `test_fixes_13797`) are not run locally. They are named in the report, and CI judges them (decision F-5 (a)).
   - `test_resolver.py` is printed through its `covers` (`hooklib.py`, and after this node also the nine added names).
   - A line "no scenario or keep row covers" is a report line (7b).
   - The predicted set is an estimate; this spec did not run the command.
6. The AR-29 change check: `python -B scripts/tests/test_judgment_census.py` is green, with no row added and no count raised. Any raise is named row by row.
7. `python -B scripts/selftest.py --lang` (FR-30): no Cyrillic in the owned files.
8. The commit message carries:
   - `architecture: AR-15, AR-13, AR-29, AR-20, AR-28, AR-4 -- <how kept>`;
   - a `judgment:` line (shape / data, and no new refusal on a role's content);
   - the four questions and the axis block, because the sentinel is a new machine check (rule 10);
   - the function lists of §7.

## §7. Hot files and the D-0048 function lists

| file | hot (PROJECT.md / batch line 15) | functions touched | outside a function |
|---|---|---|---|
| `hooklib.py` | yes | `is_one_component`, `is_story_folder` | none |
| `stage_guard.py` | yes | `story_named_by_text`, `resolve_ticket` (env route :643 and explicit route :621), `_recipient_receipts` | none (`import hooklib` exists at :81) |
| `cost_capture.py` | yes (batch line 15) | `_capture`, `main` | one new line `import hooklib` beside :66 (C-2) |
| `exit_gate.py` | no | `_named_ticket` | a new line `import hooklib` beside :31/:39 |
| `activity_capture.py` | no | `activity_path` | a new line `import hooklib` beside :11 |
| `recover_codex_usage.py` | no | `recover` | a new line `import hooklib` beside :8-10 |
| `host_dispatch.py` | no | `controller_record` | none (local import at :19) |
| `estimate_record.py` | no | `task_binding` | none (local import beside :41) |
| `red_sandbox.py` | no | `_row_problem`; `_component` deleted | none (`import hooklib` exists at :82) |
| `role_digest.py` | no | `file_notes` | a new line `import hooklib` after :37 |
| `tests/test_resolver.py` | no | new `oh6_1_one_component_table` and `oh6_1_sentinel`; two lines in `main()` | the new constants `COPY`, `TUPLE`, `PATH_NAME`, `ALLOWED` |
| `tests/test-layers.json` | no | — | the `covers` list of the `test_resolver.py` row only |

In-flight overlap: per critic t-286, no in-flight branch touches these files. OH6-2's scout names writers in `activity_capture.py` (:48, :50, :53) and `cost_capture.py` (:1959, :2388-2389, :3187, :3648, :3808), and there is no order line between OH6-1 and OH6-2. Whichever node lands later merges `main` and resolves the conflict (D-0048).

## Forks (returned by the draft; decided below)

**F-1. Copies outside the row.** Options: (a) fold in `estimate_record:42`, `red_sandbox:313`, `role_digest:323` and the explicit route `stage_guard.resolve_ticket:621`, and send `event_store.py:482` to its own node after OH6-3; (b) keep the row as it is, plus a finding; (c) wire `estimate_record` only. Recommendation: (a).

**F-2. `covers` of `test_resolver.py`.** Options: (a) add the owned scripts to `covers` (this puts `test-layers.json` into owns); (b) leave it. Recommendation: (a).

**F-3. NTFS alias names (`T.`, `T `, `...`, case).** They pass the survivor before and after this node. Options: (a) a separate finding: should story-folder sites read through `is_story_folder`? (b) nothing. Recommendation: (a).

**F-4. The sentinel's blind spots.** Options: (a) more patterns with positive controls; (b) the Lead's regex only. Recommendation: (a). As amended by t-286 fix 3: `COPY` + `TUPLE` + `PATH_NAME`, the `in x or` and basename forms named as blind spots, and an allowance of 2 named sites.

**F-5. Witness volume.** Options: (a) skip the slow files of PROJECT.md p. 2 and name them; (b) run everything. Recommendation: (a).

**F-6. Axis 8 row.** Options: (a) the Lead names `is_one_component` and its sites on the axis 8 row; (b) leave it. Recommendation: (a).

**F-7. (From the coordinator, OH6-2 digest.) Should the length ceiling live in `is_one_component`?** Recommendation: (a) keep OH6-2 separate.

What the combined option would add:
- a `COMPONENT_LIMIT` in `hooklib.py`. `native_context.py:9` already imports `hooklib`, so this creates no cycle;
- one condition in the survivor;
- 2 more columns in the table;
- a changed accepted set at EVERY existing caller (`artifacts_dir`, `story_root`, `controller.py:2494`, `exploration`, `role_load`, `waiver`, `subagent_journal`, `host_dispatch:310`).

The direction when a name is too long would be the same as for a bad shape at every site.

Budget (read from the code, not verified by a run): 259 − 143 = 116 characters after the root.
- activity file: 29 + 5 + 13 = 47, so the component must be ≤ 69;
- cost file: 23 + 5 + 13 = 41, so ≤ 75;
- story folder to `state\controller.json`: 57, so ≤ 59. Deeper files leave less, and `artifact_root` is configurable per project (AR-3).

So one name-level constant is either too loose or too tight. It would also not cover `exit_gate.digest_path:1094`, `manual_capture.case_dir_name:287`, the dispatch-id writers, or `exit_gate.py:167`. And the brief forbids widening the survivor.

**F-8. A quiet exit for a refused session id in `cost_capture` (P18, FR-4).** Options: (a) keep the direction and file a finding; (b) add a stderr line now. Recommendation: (a). Per critic t-286, the finding must say: "OH6-1 turned a traceback into a silent skip for non-str/NUL session ids". It is placed into a non-taken batch in the same move (D-0044).

Decided before the draft (not a fork): NUL is refused by the survivor (Lead, by recommendation; batch line 9).

## Coordinator decision (Opus, lead_degraded window; по рекомендации, до слова владельца, 13.11.2026)

F-1 (a): the four extra copies join OH6-1 (estimate_record, red_sandbox, role_digest, stage_guard.resolve_ticket explicit route); `event_store.py:482` goes to a new node after OH6-3, filed as a finding. F-2 (a): `test-layers.json` joins owns (the `covers` of the test_resolver keep row only). F-3 (a): separate finding (NTFS alias names). F-4 (a): two more sentinel patterns with positive controls. F-5 (a): the slow files of PROJECT.md p.2 are skipped and named. F-6 (a): queued to the full Lead (SIBLING_MAP axis 8 row; the coordinator does not write SIBLING_MAP while degraded). F-7 (a): OH6-2 stays a separate node. F-8 (a): separate finding (silent cost-capture skip). Critic on plan: required (forks, hot files).
Fix round t-291 applied t-286 items 1-9

## Small technical choices closed by the designer

- C-1: every new call is written `hooklib.is_one_component(...)`, so that one spy covers every site.
- C-2: in files that use `from hooklib import ...`, `import hooklib` is a NEW line. The shared import line is not edited.
- C-3: the sentinel scans `hooklib.py` separately and expects exactly one `COPY` hit (the survivor).
- C-4: the `resolve_ticket_env` row uses two stories, so the guess cannot mask the env route's answer. The `resolve_ticket_explicit` row is its mirror: it uses ONE story, so a fall-through would show.
- C-5: `is_story_folder` keeps its docstring list (`/ \ : NUL`), which is still true.
- C-6 (t-291): `red_sandbox._component` is deleted rather than kept as an alias. It has no caller outside the file: a Grep of `\b_component\b` over `scripts/` finds red_sandbox's lines only in that file, and the same pattern finds `session_identity._component` (positive control).

## §10. Fix round t-291 (critic t-286 items 1-9: where each was applied)

1. The coordinator decision is folded in. The header `owns` gains `estimate_record.py`, `red_sandbox.py`, `role_digest.py` and `test-layers.json`. `non-goals` loses both "unless" clauses and restricts `test-layers.json` to `covers`. §2.2 gains rows 10-13. §1 gains census rows. §4 gains columns 10-13. §5 gains rows and the `covers` change. DoD 3 and DoD 5 are updated. §7 gains rows. The F-2 entry carries the names. The batch-6 "Ход" line is coordinator move (i) in the header.
2. The explicit route: §2.2 row 13; §3 row "resolve_ticket explicit route" (returns `("", facts)`, never falls through); §5 row `resolve_ticket_explicit` with ONE story `T`; §4 column 13; C-4.
3. The sentinel: §5 Part B is now `COPY` + `TUPLE` + `PATH_NAME`. The `in x or` and basename forms are stated blind spots. `ALLOWED = {"event_store.py": 1, "selftest.py": 1}` points to §2.4. The §1 AR-13 and AR-20 rows and DoD 2 are rewritten. Positive, negative and differential controls are given per pattern.
4. The missed copies: §2.3 search (d), and the new §2.4 "Copies left to a named node" (`event_store.py:482`, `selftest.py:982`, `dependency_drift.py:92`), with the pointer "finding to be filed: onboarding-hooks, 'is_one_component copies outside OH6-1'". Also header non-goals and coordinator move (ii).
5. Under-specified rows: §5 rows `cost_capture_main` (config.json, `codex_usage.metadata` -> `{}` patched on the module, `_choose_subagent_transcript` no-op) and `recover_codex_usage` (an existing empty transcript).
6. Row ids: §5 Part A gains a literal "id" column with the 15 strings. The mutation id `OH6-1 recover_codex_usage-dotdot` now matches (§5, DoD 4).
7. The spy and `is_story_folder`: §5 rule 2 includes `is_story_folder` in the spy column, and only `is_one_component` is exempt. DoD 3 counts 14 spy rows.
8. Order, branch and worktree: the header "Order" line is restated per file; the handoff names branch `wip/oh6-1`; the header says that the dispatch creates the worktree, after a push.
9. The edge nit: the §4 non-str row, site 9, now reads "Before: TypeError for an int; a list or dict passed silently".

Also applied (t-286 "Item 5", not numbered): the F-8 finding wording and its placement in a non-taken batch (F-8; coordinator move (iii)).

## Reading trail

All paths are under `C:\QAFactory\forge-repo\.claude\worktrees\oh7-5\` unless absolute.
- `plans/piles/onboarding-hooks/batch-6-ostatki-t-203-i-t-227.md` (whole); `plans/piles/onboarding-hooks/findings/20261113-kopii-proverki-odnoj-komponenty-puti.md` (whole)
- `ai-packages/qa-factory/scripts/hooklib.py` :255-379; `host_dispatch.py` :1-40; `exit_gate.py` :185-224; `stage_guard.py` :405-474, :600-739; `activity_capture.py` :1-70; `cost_capture.py` :1880-1919, :3770-3814; `recover_codex_usage.py` (whole)
- `estimate_record.py` :34-69 and the import lines; `red_sandbox.py` :306-343 and the import lines (`import hooklib` at :82); `role_digest.py` :316-327 and the import lines (:30-37); `event_store.py` :474-487; `session_identity.py` :30-54; `manual_capture.py` :287-299; `native_context.py` :1-32; a Grep of `worker_lifecycle.py`
- Greps (Grep tool, `scripts/`): searches (a)-(d) of §2.3; `is_one_component`; `\b_component\b` (files); `file_notes\(` (callers: `exit_gate.py:1201`, `tests/test_role_digest_notes.py`)
- `scripts/tests/test_resolver.py` :1-24, :54-58, :389-395, :1055-1108, :1318-1475; `scripts/tests/test-layers.json` :1-40, :4316-4350; `scripts/tests/scenario_walk.py` :833-932; `scripts/tests/test_judgment_census.py` :150-299; `scripts/tests/fixtures/judgment-census.json` (Grep of rows, including `estimate_record.py::task_binding` at l.263)
- `ai-packages/qa-factory/design/architecture.md` :130-224; `plans/builder-rules.md` (Grep 7b); `docs/SIBLING_MAP.md` axis 8 (:202-223), axis 34 (:582)
- `docs/tasks/specs/reviews/t-286-oh6-1-plan-review.md` (whole)
- Not opened in full: `docs/TESTING.md` and `design/factory-rules.md`. The FR lines come from the auto-loaded index; this is noted as a gap.
