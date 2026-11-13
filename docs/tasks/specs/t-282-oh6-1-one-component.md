# t-282 — OH6-1: every copy of "a name is one path component" calls `hooklib.is_one_component` (DRAFT, designer)

Status: DRAFT for Lead acceptance. Node `onboarding-hooks/6/OH6-1`. Forks are at the end and are NOT decided here.
Line numbers were read on 13.11.2026 in the clean snapshot `C:\QAFactory\forge-repo\.claude\worktrees\oh7-5`
(origin/main 0a0db4f). Several of them have moved since the batch row was written; the moves are listed in §2.

## Dispatch header (R11-f)

given: this spec (marked, one hop: it carries the enumeration); `ai-packages/qa-factory/design/factory-rules.md` (whole, PROJECT.md "package change" p. 1); `plans/builder-rules.md` (whole); `ai-packages/qa-factory/design/architecture.md` AR-4, AR-13, AR-15, AR-20, AR-28, AR-29; `docs/TESTING.md`; `docs/SIBLING_MAP.md` axes 8, 18, 34; `plans/piles/onboarding-hooks/batch-6-ostatki-t-203-i-t-227.md` row OH6-1; `plans/piles/onboarding-hooks/findings/20261113-kopii-proverki-odnoj-komponenty-puti.md`; the eight owned files below as they are on `origin/main`; `scripts/tests/harness.py`, `scripts/tests/test-layers.json` (row `test_resolver.py`, read only)
owns:
C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\hooklib.py
C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\host_dispatch.py
C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\exit_gate.py
C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\stage_guard.py
C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\activity_capture.py
C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\cost_capture.py
C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\recover_codex_usage.py
C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\tests\test_resolver.py
non-goals: no length limit in `is_one_component` (OH6-2; brief: "do not widen `is_one_component` beyond one component"); no change to any site's answer other than the inputs listed in §4; no edit of `worker_lifecycle.py` (OH5-11 already calls `artifacts_dir` there); no new axis in `docs/SIBLING_MAP.md`; no new test file; no edit of `test-layers.json` unless fork F-2 is accepted; the extra copies of §2.3 are NOT touched unless fork F-1 is accepted
handoff: builder report per `.claude/agents/builder.md` rule 7: the diff hash on `pile/onboarding-hooks/batch-6`, the verbatim witness output, the FR walk by section, the table of §2 with the new line numbers
edges: §4 (edge table) and §3 (positional invariants per site)
DoD: §6; verification run `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <the eight owns paths>` and every file it prints (scope rule in §6)
siblings: axis 8 (where the story is on disk: the key -> folder rule), axis 34 (one road), axis 18 (the sentinel's allowance is shrink-only); extra copies of the same class outside the row: §2.3 (fork F-1)
designer: this draft (t-282), after Lead acceptance

Order (batch file, line 15): after OH5-10, OH5-11, OH5-13 (`onboarding-hooks/5`) and the merges of `wip/oh5-11`, `wip/oh3-36`.

## §1. Invariants and owners

| AR | how this node touches it | change check written into the DoD |
|---|---|---|
| AR-15 (one survivor, wired everywhere) | nine hand copies become calls of `hooklib.is_one_component`; `is_story_folder` keeps only its extras | DoD 1: grep for the problem, not the helper. The sentinel (§5 part B) is the detector. Every copy found outside the row is listed (§2.3), and each one is either wired in or named as a fork |
| AR-13 (a fact with a reader is read only through it) | "is this a single path component" has one reader | DoD 2: after the change, no owned file holds a hand copy (the sentinel is green, with an allowance of 0) |
| AR-29 (a code check judges data) | every altered check is a SHAPE check of a name; none judges a role's content | DoD 6: run `test_judgment_census.py`. Expected: no row added, none removed, no count raised. This is an estimate, not checked by a run: no check unit is created or deleted, because every refusal site stays in the same function. A raised count is named in the verdict (AR-20) |
| AR-20 (shrink-only ratchets) | the sentinel's allowance is shrink-only and is empty after the node | DoD 2: the allowance literal is `{}`; adding to it is a named raise |
| AR-28 (an unknown never becomes a pass) | NUL and non-str inputs used to pass the copies, or to crash them. After the change they are refused, in the site's own direction | DoD 3: the NUL column of the table |
| AR-4 (no tie to one machine) | `\` and `:` are refused on every OS, not only on Windows (this is unchanged and kept) | DoD 3: the `a\b` and `a:b` columns |

Owner and census class of every check the node adds or alters (AR-29, P27):

| check | owner | census class | census row (judgment-census.json) |
|---|---|---|---|
| `hooklib.is_one_component` (gains NUL) | data (code) | shape | none: not a check unit today. It is called from units |
| `hooklib.is_story_folder` (its own prefix replaced by the survivor) | data | shape | none |
| `host_dispatch.controller_record` | data | shape | none (no refusal site; returns None) |
| `exit_gate._named_ticket` | data | shape | none |
| `stage_guard.story_named_by_text`, `resolve_ticket`, `_recipient_receipts` | data | shape | none |
| `activity_capture.activity_path` | data | shape | `activity_capture.py::activity_path` shape/data (line 8), unchanged |
| `cost_capture._capture`, `cost_capture.main` | data | shape | none |
| `recover_codex_usage.recover` (gains `.`/`..`/NUL) | data | shape | `recover_codex_usage.py::recover` shape/data (line 678), unchanged |
| the sentinel in `test_resolver.py` | data (code detector) | shape. It is a test, outside the census: `scripts/tests/` is not scanned | — |

FR sections touched: C (FR-13: none of this is open variety; FR-14: no output shape changes), D (FR-17: the tool is wired everywhere the problem occurs), G (FR-32, FR-54). A: no refusal text changes, and every ValueError keeps its words. B: no text shown to a person. E, F: not touched. Principles: P31 (one road), P12.

## §2. Call sites

### 2.1 The survivor and the leaf (hooklib.py, hot file)

| function | current line (verified) | change |
|---|---|---|
| `is_one_component` | :269-272. The batch row says :233, and that has drifted. Body: `return isinstance(name, str) and bool(name) and name not in (".", "..") and not any(c in name for c in "/\\:")` | the separator literal becomes `"/\\:\0"` (Lead fork, decided: NUL is refused). The docstring names NUL. Nothing else changes: no strip, no length |
| `is_story_folder` | :305-320; prefix at :317-318. The row says :266, and that has drifted. Today: `not isinstance(name, str) or not name.strip() or name != name.strip() or name in (".", "..") or any(c in name for c in "/\\:\0") or parent is None or not str(parent).strip()` | `not is_one_component(name) or not name.strip() or name != name.strip() or parent is None or not str(parent).strip()`. The answer is unchanged for every input, because the survivor plus NUL equals the removed part |

Error direction of the survivor in its role as the one gate (designer rule 1): it may err only toward **False** (refusal). It never raises, for any input. Adversarial inputs that must stay False: `""`, `"."`, `".."`, `"/a"`, `"a/b"`, `"a\\b"`, `"C:x"`, `"a:b"`, `"a\0b"`, `"\0"`, `None`, `5`, `[]`, `b"ab"` (bytes are not str). Invariant: **at no site does the survivor accept a name that the site's old copy refused.** Every old copy is a subset of the survivor's refusals (§4 shows it column by column). So the change only moves inputs from "accepted" to "refused", never the other way.

### 2.2 The nine copies of the row

A closed choice (§8 C-1): every new call is written `hooklib.is_one_component(x)` (attribute access), so one spy on the `hooklib` module sees every site. Files that only `from hooklib import ...` get a new module-level line `import hooklib`.

| # | site | current line (verified 13.11) | current error direction | new call |
|---|---|---|---|---|
| 1 | `host_dispatch.controller_record` | :21 (row: :21, still true). `if not ticket or not dispatch or ticket in (".", "..") or any(char in ticket for char in "/\\:"): return None`. `import hooklib` is local at :19 | `None` (no record) | `if not dispatch or not hooklib.is_one_component(ticket): return None` (ticket is already `str(ticket or "")` at :20) |
| 2 | `exit_gate._named_ticket` | :208-209 (row: :209). `[name for name in facts.get("named") or [] if name not in (".", "..") and not any(c in name for c in "/\\:") and (root / name / "pipeline.json").is_file()]` | the name is dropped from `in_text`, so the result is `""` unless another key names the ticket | `[name for name in facts.get("named") or [] if hooklib.is_one_component(name) and (root / name / "pipeline.json").is_file()]` plus `import hooklib` |
| 3 | `stage_guard.story_named_by_text` | :435-437 (row: :436). `if name not in (".", "..") and not any(c in name for c in "/\\:") and (root / name / "pipeline.json").exists()` | the candidate is dropped | `if hooklib.is_one_component(name) and (root / name / "pipeline.json").exists()` (`import hooklib` exists at :81) |
| 4 | `stage_guard.resolve_ticket` (step 5, the `$QA_FACTORY_TASK` route) | :643-645 (row: :643). `if env_task and not any(c in env_task for c in "/\\:") and env_task not in (".", "..") and (root / env_task / "pipeline.json").is_file(): return env_task, facts` | the route is skipped, and control falls to `_env_exploration` (:646) | `if hooklib.is_one_component(env_task) and (root / env_task / "pipeline.json").is_file(): return env_task, facts` |
| 5 | `stage_guard._recipient_receipts` | :716-718 (row: :717). `... and isinstance(story, str) and story and not any(c in story for c in "/\\:") and story not in (".", "..") and (root / story / "pipeline.json").is_file()` | the receipt is skipped (neither evidence nor veto) | `... and hooklib.is_one_component(story) and (root / story / "pipeline.json").is_file()`. The `isinstance` test and the truthiness test are inside the survivor |
| 6 | `activity_capture.activity_path` | :44 (row: :44). `if not session or session in {".", ".."} or any(c in session for c in "/\\:"): raise ValueError("session identity must be a single safe component")` | `ValueError`, same text | `if not hooklib.is_one_component(session): raise ValueError(<same text>)` plus `import hooklib` |
| 7 | `cost_capture._capture` | :1907 (row: :1907). `if not tpath.is_file() or any(c in session_id for c in "/\\:") or session_id in (".", ".."): sys.exit(0)` | `sys.exit(0)` before anything is written | `if not tpath.is_file() or not hooklib.is_one_component(session_id): sys.exit(0)` plus `import hooklib` |
| 8 | `cost_capture.main` | :3800 (row: :3800). The same condition, then `return` | `return` before the debounce, the marker and the lock | `if not tpath.is_file() or not hooklib.is_one_component(session_id): return` |
| 9 | `recover_codex_usage.recover` | :16 (row: :16). `if not session or any(c in session for c in '/\\:'):raise ValueError('Unsupported session identity')` uses single quotes and has no `.`/`..` guard | `ValueError('Unsupported session identity')` | `if not hooklib.is_one_component(session):raise ValueError('Unsupported session identity')` plus `import hooklib`. The import resolves: the file already imports `activity_capture`, which imports `hooklib` from the same `scripts/` folder. New: `.`, `..` and NUL are refused |

Out of the row on purpose: `worker_lifecycle.py:94`. On main it now reads through `hooklib.artifacts_dir(task, event, root=root)` (OH5-11 is merged). Lines :93-94, :114-115, :154-156 and :202-210 all go through `artifacts_dir`, so the copy has gone from the file. Trail: Grep `artifacts_dir|is_one_component|"/\\\\:"` on `worker_lifecycle.py`.

Callers of the survivor that already exist and whose answer changes ONLY for a name holding NUL. Each one moves to its own refusal direction, and none needs an edit: `artifacts_dir` :280 (ValueError, earlier than the IO error it used to hit), `story_root` :371 (StoryRootError), `controller.py:2494` (`continue`), `exploration.py:134` (not a slug), `:537` and `:734` (ExplorationRefused), `host_dispatch.py:310` (skips the story branch; the receipt is still written), `role_load.py:542` (RoleLoadError), `:555` (record None, then RoleLoadError), `waiver.py:1154` and `:1169` (refuse), `subagent_journal.py:107` (`""`), `stage_guard.py:464` (no story named).

### 2.3 Copies found outside the row (grep), resolved by fork F-1

Searches, run in the snapshot `scripts/` with the Grep tool. Positive control: each pattern found the nine known sites.
(a) `in ['"]/\\\\:` found the 9 row sites, `hooklib.py:272` (the survivor) and `hooklib.py:318` (`is_story_folder`, row item), and nothing else.
(b) `for \w+ in ['"][^'"]*(\\\\|/)[^'"]*['"]\)` found the same set plus `vcs_evidence.py:407` (`"/@ \t"`, a VCS host key; the finding says it is not a copy, and this spec agrees).
(c) The `.`/`..` guard in tuple or set form, `\(\s*["']\.["']\s*,\s*["']\.\.["']\s*\)|\{...\}`, found these copies that the row does not list:

| site | line | form | difference from the survivor | verdict |
|---|---|---|---|---|
| `estimate_record.task_binding` | :42 | `not task or task in {'.','..'} or '/' in task or '\\' in task` | no `:` and no NUL; ValueError | a copy (task -> story folder) |
| `red_sandbox._component` | :313-315 | `isinstance... and name not in (".", "..") and not any(sep in name for sep in ("/", "\\"))` | no `:` and no NUL; guards `pins` keys and `must_not_preexist` names | a copy |
| `role_digest.file_notes` | :323 | `name != Path(name).name or name in (".", "..")` | depends on the OS: on POSIX `a\b` passes (estimate from pathlib semantics, not verified by a run); on Windows `a:b` gives `Path.name == "b"`, so it is refused | a copy |
| `event_store.EventStore.__init__` (`stale_marker`) | :482 | same `Path(marker).name` form; ValueError | as above | a copy, in a core file that OH6-3 owns (`event_store.py`) |
| `stage_guard.resolve_ticket`, the explicit route | :621 | `(root / explicit / "pipeline.json").is_file()` with NO component check | `explicit = "../X"` is joined unchecked | not a copy, but a MISSING guard in a function this node already owns |

Not copies (a stricter allow-list of characters, a different rule): `session_identity._component` :48-49 (`SAFE_ID = [A-Za-z0-9._-]{1,128}`), and `manual_capture.case_dir_name` :287-299 (per-part `_PART` charset, `area/TC`).

## §3. The POSITIONAL invariant at each site

| site | where the call stands | what must stay refused or unreachable |
|---|---|---|
| `is_story_folder` | the survivor is called FIRST, before `name.strip()` | a non-str `name` must never reach `.strip()` (no AttributeError: a hook gets an answer, E-8). A name that is not one component never reaches `_listing` (no listing, no stat) |
| `controller_record` | before `hooklib.artifact_root(...) / ticket` | no `read_json` is ever issued on a path built from a ticket that is not one component. The answer stays None on every doubt |
| `_named_ticket` | inside the comprehension, before the `.is_file()` join | a name that is not one component never becomes `in_text`. `""` can no longer probe `root / "" / "pipeline.json"` (that is the artifact root itself: a latent hole that closes, §4) |
| `story_named_by_text` | before the `.exists()` join | the same. The `Ticket:` line rule (`by_line`) reads only from `existing`, so a refused name cannot settle a story through the line either |
| `resolve_ticket` step 5 | after the event's own routes (explicit, resume recipient, text, slug) and BEFORE `_env_exploration` and the single-story guess. The position does not change | a refused `env_task` is never returned as the story. It still REACHES `_env_exploration`: an `explore:<slug>` value carries a `:` and must go on to that route exactly as today. The person's word still beats the guess; nothing the event named is overruled |
| `_recipient_receipts` | after `binding_names` and the dispatch test, before the `.is_file()` join | a receipt whose `task_id` is not one component is neither evidence nor a veto. A forged `task_id` cannot steer the read outside `root` |
| `activity_path` | first statement, before `project_root(event)` | no activity path, spool path or legacy move is computed for a refused session. The legacy `source.unlink()` at :57 stays unreachable for it |
| `_capture` | before `_session_scope_ok`, so before any read of config, the lock or any write | a refused session id writes nothing (no `qa-factory/` created, no cost file) |
| `main` | after `metadata(tpath)` may replace `session_id` (:3794-3798), and before `--debounced`, the "started" marker and the lock | the check runs on the FINAL `session_id` (the transcript's own id wins), and no marker or lock file is created for a refused id |
| `recover` | right after `metadata(transcript)`, before `scan`, before any read of boundaries and before any write | with a refused id, nothing is scanned, no activity file is written, and no `cost_capture.py` subprocess is started |

## §4. Edge table

The cells give the answer AFTER the change, with BEFORE where it differs.

| input | survivor | sites 2/3/4/5 (skip / next route) | site 1 (None) | site 6 (ValueError) | sites 7/8 (exit / return) | site 9 (ValueError) | invariant protected |
|---|---|---|---|---|---|---|---|
| NUL (`a\0b`) | False (new) | skipped. Before: passed the copy, and then `is_file()` was False on Python 3.8+ (estimate from pathlib semantics, not verified by a run) | None. Before: same result through `read_json(errors=Exception)` | ValueError. Before: a path holding NUL was returned and failed later at IO | quiet exit. Before: crashed later when it wrote `<id>.json` | ValueError. Before: passed; the write failed later | a name with NUL is no path component on any OS; it never reaches an OS call |
| `""` | False | skipped. Before: sites 2 and 3 PASSED `""`, so `root / "" / "pipeline.json"` = `<artifact root>/pipeline.json` was probed (a latent hole). Site 4 refused through `env_task` truthiness, site 5 through `story` truthiness | None (unchanged) | ValueError (unchanged) | unreachable: `"" or tpath.stem` gives `""` only for an empty `tpath`, and that fails `is_file()` first | ValueError (unchanged) | an empty name never names the artifact root itself as a story |
| whitespace-only `"  "` | True (unchanged; the brief forbids widening) | site 4: unreachable, `env_task` is `.strip()`-ed at :602. Sites 2/3/5: unchanged, the name is joined, and the outcome depends on the filesystem | unchanged | unchanged | unchanged | unchanged | no change in this node. `is_story_folder` still refuses blank or edge-blank names. NTFS alias names: fork F-3 |
| very long name (over 255 characters, or the path over 259) | True (unchanged; no length rule) | unchanged: the join and stat may return False or raise OSError, as today | unchanged (`read_json` swallows) | unchanged | unchanged | unchanged | not this node's: OH6-2 (fork F-7) |
| non-str (None, int, list, bytes) | False | site 5: reachable (`task_id` from JSON), refused as before. Sites 2/3: names come from `AF.keys_in` / `labelled_keys` (strings), so unreachable in practice. Site 4: unreachable (`str(...)`) | unreachable: `str(ticket or "")` | reachable if a caller passes one. Before: TypeError (`c in 5`) or an unhashable error for a list. After: ValueError, the site's own refusal | reachable (`session_id` from event JSON, `meta["id"]` from the transcript). Before: a TypeError traceback in the hook. After: quiet exit / return | reachable (`meta.get('id')`). Before: TypeError. After: ValueError | a value of the wrong type is refused in the site's direction, never a crash in a hook |
| `.` / `..` | False | skipped (unchanged) | None (unchanged) | ValueError (unchanged) | exit / return (unchanged) | ValueError (NEW; before: passed) | no name climbs or stays on the parent folder |
| `a/b`, `a\b`, `a:b` | False | unchanged | unchanged | unchanged | unchanged | unchanged | one component on every OS (AR-4) |
| `explore:<slug>` in `$QA_FACTORY_TASK` | False | site 4: skipped, then reaches `_env_exploration` (unchanged) | — | — | — | — | the exploration route stays reachable (§3) |

Conflicting requirements: none between the nine sites. "Keep each site's direction" and "refuse NUL" agree, because NUL only joins each site's existing refusal set.

## §5. Tests (test_resolver.py, a keep row of layer `table`; not quarantined)

Check: `test-layers.json` puts `test_resolver.py` under `keep` (line 4320, layer `table`). The `quarantine` section starts at line 7004, and the file name appears once in `test-layers.json`. Its `covers` list includes `hooklib.py`, but NOT the six other owned scripts (fork F-2). No new test file.

### Part A: ONE parameterised table `oh6_1_one_component_table()`

Rows are the callers. Columns are the names `..`, `.`, `a/b`, `a\b`, `a:b`, `a\0b` and the good name `T`. A check id is `OH6-1 <caller>-<label>`, where label is one of `dotdot`, `dot`, `slash`, `backslash`, `colon`, `nul`, `good`. One `check(...)` per cell, in the `harness.check` style of the file.

| caller (row id) | how the name reaches the check | refused (6 bad names) | good name `T` |
|---|---|---|---|
| `is_one_component` | direct | `False` | `True` |
| `is_story_folder` | `(<artifact root>, name)`; folder `T` exists | `False` | `True` |
| `controller_record` | `(project, name, "D")`; `T/state/controller.json` holds dispatch `D` | `None` | the record dict |
| `exit_gate._named_ticket` | stub `exit_gate.SG.resolve_ticket` to return `(name, {"named": [name]})` | `("", ...)` | `("T", ...)` |
| `story_named_by_text` | stub the name source (`stage_guard.AF.keys_in` / `labelled_keys`) to return `[name]` | `""` | `"T"` |
| `resolve_ticket` (env route) | `QA_FACTORY_TASK=name`, an event that names nothing, TWO stories `T` and `U` (so the guess answers none) | result `!= name` (here `""`) | `"T"` |
| `_recipient_receipts` | a receipt with `task_id=name`, `dispatch_id="D"` and the target among its names | `[]` | `[("T", "D")]` |
| `activity_path` | `({"cwd": project}, name)` | `ValueError` | a `Path` ending `T.json` |
| `cost_capture._capture` | event `{session_id: name, transcript_path: <existing file>}`; a recording stub on `cost_capture._session_scope_ok` | `SystemExit(0)` with the stub NOT reached | the stub reached |
| `cost_capture.main` | stub `read_event`, an existing transcript, `--debounced` in argv, a recording stub on `_debounce_window_open` (returns True), `_ends_dispatch` False | return with the stub NOT reached | the stub reached |
| `recover_codex_usage.recover` | stub `recover_codex_usage.metadata` -> `{'id': name}`, `scan` -> `([], 'x')`, `boundaries=[]`, `write=False` | `ValueError` | the result dict |

Two rules make the table proof against mutation:
(1) **Reachability.** For every bad name whose unguarded join can be CREATED on the running OS (`..` and `.` everywhere; `a/b`; on POSIX also `a\b` and `a:b` as literal folder names), the fixture creates the file the site would read. Then only the guard can produce "refused". Where it cannot be created (NUL everywhere; `a:b` on Windows), rule 2 carries the proof.
(2) **Spy.** In the same pass, a spy on `hooklib.is_one_component` (the B4 pattern of this file: replace, call, restore in `finally`) records its arguments. Every cell asserts that the spy saw the exact name. Ids: `OH6-1 <caller>-<label> asked the survivor`. Wrapper rows `is_one_component` and `is_story_folder` are exempt from the spy column: one is the survivor, and the other calls it by a module-local name.

Stated mutation (DoD 4): remove the guard from `recover_codex_usage`. The row `OH6-1 recover_codex_usage-dotdot` must turn red.

### Part B: the census sentinel `oh6_1_sentinel()`

- Pattern: `COPY = re.compile(r"""for \w+ in ['"]/\\\\:""")`. In file text it matches: a quote of either kind, a slash, two backslashes, a colon. That covers any loop variable name (`c`, `char`, ...) and both quote forms.
- Scan: every `scripts/*.py` except `hooklib.py`. Expected hits: `[]`. Allowance: `ALLOWED = {}`, shrink-only (AR-20).
- `hooklib.py` is checked apart: exactly ONE hit, inside `is_one_component`. A second hit in hooklib (for example `is_story_folder` copying again) is red.
- Positive controls: the regex finds `for c in "/\\:"`, `for char in '/\\:'` and `for sep in "/\\:\0"`, written as fixture text in the test.
- Negative control: `vcs_evidence.py`'s `for c in "/@ \t"` is not flagged.
- Differential: the text of `recover_codex_usage.py` as it stands on main today (line 16) is flagged.

## §6. DoD (inline)

1. Every site of §2.2 calls `hooklib.is_one_component` as in the "new call" column, with its direction unchanged. `is_story_folder` is reduced as in §2.1. The survivor refuses NUL. Every ValueError text is kept byte for byte.
2. The Part B sentinel is green with `ALLOWED = {}`, and its controls pass.
3. The Part A table is green: 11 callers × 7 names, plus the spy column.
4. The mutation of §5 is run once by hand (a byte copy before, the restore from it, a hash comparison as witness; command hygiene pt. 7). The red id is quoted.
5. Witness (`plans/builder-rules.md` 7b):
   `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\hooklib.py C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\host_dispatch.py C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\exit_gate.py C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\stage_guard.py C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\activity_capture.py C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\cost_capture.py C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\recover_codex_usage.py C:\QAFactory\forge-repo\.claude\worktrees\oh6-1\ai-packages\qa-factory\scripts\tests\test_resolver.py`
   Then run every file it prints, as `python -B scripts/tests/<file>.py`. The output is pasted verbatim. `test_resolver.py` is printed through its `covers: hooklib.py`. The line for `tests/test_resolver.py` itself may read "no scenario or keep row covers": that is a report line (7b). The printed set is large because `hooklib.py` sits in every scenario closure (fork F-5). This spec does not run the command; the prediction is an estimate.
6. The AR-29 change check: `python -B scripts/tests/test_judgment_census.py` is green, with no row added and no count raised. Any raise is named row by row.
7. `python -B scripts/selftest.py --lang` (FR-30) on the owned files: no Cyrillic.
8. The commit message carries `architecture: AR-15, AR-13, AR-29, AR-20, AR-28, AR-4 -- <how kept>` and a `judgment:` line (shape / data, no new refusal on a role's content). The sentinel is a new machine check, so the four questions and the axis block are written in the commit message (rule 10). The `stage_guard.py` and `cost_capture.py` function lists are those of §7.

## §7. Hot files and the D-0048 function lists

| file | hot (PROJECT.md / batch line 15) | functions touched | outside a function |
|---|---|---|---|
| `hooklib.py` | yes | `is_one_component`, `is_story_folder` | none |
| `stage_guard.py` | yes | `story_named_by_text`, `resolve_ticket`, `_recipient_receipts` | none (`import hooklib` exists at :81) |
| `cost_capture.py` | yes (batch line 15) | `_capture`, `main` | one new line `import hooklib` beside :66 (a new line, so the shared import at :66 stays untouched; §8 C-2) |
| `exit_gate.py` | no | `_named_ticket` | new line `import hooklib` beside :31/:39 |
| `activity_capture.py` | no | `activity_path` | new line `import hooklib` beside :11 |
| `recover_codex_usage.py` | no | `recover` | new line `import hooklib` beside :8-10 |
| `host_dispatch.py` | no | `controller_record` | none (local import at :19) |
| `tests/test_resolver.py` | no | new `oh6_1_one_component_table`, `oh6_1_sentinel`; two lines in `main()` | the new constants `COPY`, `ALLOWED_COPIES` |

Overlap to watch: OH6-2's scout names writers in `activity_capture.py` (:48, :50, :53) and `cost_capture.py` (:1959, :2388-2389, :3187, :3648, :3808). The batch file has no order line between OH6-1 and OH6-2. Lines :3808 (in `main`) and the area near :1907 are adjacent to this node's edits. If both run in parallel, the later node merges `main` and resolves the conflict (D-0048).

## Forks (returned, not decided)

**F-1. Copies outside the row (§2.3).** P31 and designer rule 6 say a copy left on its own road is a defect, unless it is a named node.
Options:
(a) Add `estimate_record.task_binding:42`, `red_sandbox._component:313`, `role_digest.file_notes:323` and the missing guard at `stage_guard.resolve_ticket:621` (explicit route) to OH6-1. That is three more owned files (none hot), three more table rows plus one row for the explicit route, and a direction for each: ValueError, False, `""`, and "explicit not one component -> `""` with facts" (the safe direction). Then open a separate node for `event_store.py:482`, after OH6-3 (which owns `event_store.py`, a core file, critic mandatory).
(b) Keep OH6-1 as the row has it, and file a finding that opens one node with these sites.
(c) Wire only `estimate_record` (the closest copy: story key -> folder) and queue the rest.
**Recommendation: (a).** It is one road, and the cost is about +4 table rows and three small files. `resolve_ticket:621` is inside a function already owned. The `event_store` part goes into a node with its own `owns`, per the rule "a slice is no exclusion when the rest is a named node".

**F-2. `covers` of `test_resolver.py`.** Today the keep row covers `hooklib.py` but not `host_dispatch`, `exit_gate`, `stage_guard`, `activity_capture`, `cost_capture` or `recover_codex_usage`. A later change to one of them would not run the OH6-1 table under `--witness-for`.
(a) Add the six names to `covers` (adds `test-layers.json` to `owns`, a shared file). (b) Leave it as is.
**Recommendation: (a).** Otherwise the detector is never reached by the change it guards.

**F-3. NTFS alias names (`T.`, `T `, `...`, case).** They pass the survivor today, and they pass after this node. On NTFS, `root / "T."` may open `T` (an estimate, not verified; command hygiene pt. 6a calls for one experiment). `is_story_folder` is already alias-proof through its listing.
(a) A finding: should the story-folder sites (2/3/4/5) read through `is_story_folder` instead of `is_one_component + is_file`? (b) Nothing.
**Recommendation: (a), as a separate finding.** The brief forbids widening the survivor, and alias proofing is a property of the folder lookup, not of the name.

**F-4. The sentinel's blind spots.** The prescribed regex does not see `'/' in x or '\\' in x` (`estimate_record`), the tuple `("/", "\\")` (`red_sandbox`), `x != Path(x).name` (`role_digest`, `event_store`) or a reordered literal such as `"\\/:"`.
(a) Add two more patterns with positive controls: the tuple / `in x or` form, and `!= Path\(\w+\)\.name`. They go green only if F-1 (a) is taken. (b) Keep exactly the Lead's regex.
**Recommendation: (a), if F-1 (a) is taken; otherwise (b),** because (a) without F-1 would be red on purpose.

**F-5. Witness volume.** Because `hooklib.py` is owned, `--witness-for` prints every scenario test and every keep row that covers `hooklib.py`.
(a) Run the printed set except the slow files of PROJECT.md "package change" p. 2 (`SLOW_TESTS`, `test_story_run_*`, `test_controller_*`, `test_fixes_13797`), which CI judges, and name them in the report. (b) Run everything printed.
**Recommendation: (a).** It is the rule text of p. 2. The Lead confirms that reading.

**F-6. Axis 8 row.** AR-15's change check says a survivor and its sites are named on their axis. Axis 8 (row 222) names `story_root` ("one path component") but not `is_one_component` or its callers.
(a) The Lead adds `is_one_component` and its call sites to the axis 8 row in the same batch. This is outside `owns`, and it is a row in an existing axis, not a new axis. (b) Leave it.
**Recommendation: (a).**

**F-7. (From the coordinator, OH6-2 digest.) Should the component length ceiling live inside `is_one_component`?**
What the combined option would add to OH6-1 (`owns` stays unwidened here):
- a constant `COMPONENT_LIMIT` in `hooklib.py`. `native_context.py` already imports `hooklib` (`from hooklib import person_signal, sorted_paths`, :9), so hooklib is the owner without a cycle; `native_context` may import it to sit beside `PACKET_ROOT_LIMIT`;
- one condition `len(name) <= COMPONENT_LIMIT` in the survivor;
- two more table columns ("at the limit", "limit + 1"), 22 cells;
- a changed accepted set at EVERY existing caller: `artifacts_dir` and `story_root` (a long ticket key at S0 becomes a refusal), `controller.py:2494`, `exploration` slugs, `role_load`, `waiver`, `subagent_journal`, and `host_dispatch:310`.

Direction when a name is too long: the same as a bad shape at each site (None / skip / next route / ValueError / exit(0) / return), so no site needs a new move.

Budget arithmetic (read from the code, not verified by a run). 259 − 143 (`SUPPORTED_ROOT`, `native_context.py:27`) = 116 for everything after the root. The fixed suffix depends on the WRITER, not on the name:
- activity file `\qa-factory\state\activities\` (29) + `.json` (5) + `TEMP_NAME_EXTRA` (13) = 47, so the component can be ≤ 69;
- cost file `\qa-factory\state\cost\` (23) + 5 + 13 = 41, so ≤ 75;
- story folder to `state\controller.json` + temp = `\qa-factory` (11) + `\artifacts` (10) + `\` (1) + `\state` (6) + `\controller.json` (16) + 13 = 57, so ≤ 59. Deeper files under a story are smaller still, and `artifact_root` is configurable per project (AR-3), so the suffix is not even fixed per writer.

So one name-level constant is either too loose (writers still overflow) or too tight for the shortest-suffix writer.

Coverage: `exit_gate.digest_path:1094` and `manual_capture.case_dir_name:287` (charset only) and the dispatch-id writers (`driver_dispatch`, `driver_machine`, `driver_runner`, `handoff_init`) do not call `is_one_component`, and `exit_gate.py:167` (agent name) has no guard at all. The combined option leaves OH6-2's work on all of them in place.

Options:
(a) Keep OH6-2 separate. It puts the per-writer budget where the component is formed (its row: "the check where the component is formed").
(b) A coarse sanity cap in the survivor (for example 128, the bound `session_identity.SAFE_ID` already uses) plus OH6-2's per-writer checks.
(c) Combined in OH6-1.
**Recommendation: (a).** The batch brief forbids widening `is_one_component` beyond one component. The ceiling is a property of the writer's suffix budget, not of the name. And (c) would still leave the charset-only and dispatch-id writers to OH6-2. Whether (b) is added later as a floor is OH6-2's choice after its scout, with the Lead's word, because it changes the accepted set of every caller.

**F-8. A quiet exit for a refused session id in `cost_capture` (P18, FR-4).** Sites 7 and 8 leave with no trace. A non-str id used to leave at least a traceback; now it leaves silently.
(a) Keep the direction, as the brief says, and file a finding: "a cost capture skipped for an unusable session id leaves one stderr line". (b) Add a stderr line in this node.
**Recommendation: (a).** The node keeps every direction by its brief.

Decided before the draft (not a fork): NUL is refused by the survivor (Lead, by recommendation; batch line 9).

## Coordinator decision (Opus, lead_degraded window; по рекомендации, до слова владельца, 13.11.2026)

F-1 (a): the four extra copies join OH6-1 (estimate_record, red_sandbox, role_digest, stage_guard.resolve_ticket explicit route); `event_store.py:482` goes to a new node after OH6-3, filed as a finding. F-2 (a): `test-layers.json` joins owns (the `covers` of the test_resolver keep row only). F-3 (a): separate finding (NTFS alias names). F-4 (a): two more sentinel patterns with positive controls. F-5 (a): the slow files of PROJECT.md p.2 are skipped and named. F-6 (a): queued to the full Lead (SIBLING_MAP axis 8 row; the coordinator does not write SIBLING_MAP while degraded). F-7 (a): OH6-2 stays a separate node. F-8 (a): separate finding (silent cost-capture skip). Critic on plan: required (forks, hot files).

## Small technical choices closed by the designer

- C-1: every new call is written `hooklib.is_one_component(...)`, so one spy covers every site and the census can grep one spelling.
- C-2: in files that use `from hooklib import ...`, `import hooklib` is a NEW line, not an edit of the shared import line, to keep merge conflicts small.
- C-3: the sentinel scans `hooklib.py` apart and expects exactly one hit (the survivor), instead of excluding the file. That way a re-copy inside hooklib is caught too.
- C-4: `resolve_ticket` row uses two stories, so the single-story guess cannot mask the env route's answer.
- C-5: `is_story_folder` keeps its docstring list (`/ \ : NUL`); it is still true.

## Reading trail

All paths are under `C:\QAFactory\forge-repo\.claude\worktrees\oh7-5\` unless they are absolute.
- `plans/piles/onboarding-hooks/batch-6-ostatki-t-203-i-t-227.md` (whole: row OH6-1, brief, order line 15, line 9)
- `plans/piles/onboarding-hooks/findings/20261113-kopii-proverki-odnoj-komponenty-puti.md` (whole)
- `ai-packages/qa-factory/scripts/hooklib.py` :255-379
- `host_dispatch.py` :1-40; `exit_gate.py` :185-224; `stage_guard.py` :405-474 and :600-739; `activity_capture.py` :1-70; `cost_capture.py` :1880-1919 and :3770-3814; `recover_codex_usage.py` (whole)
- `estimate_record.py` :34-49; `red_sandbox.py` :306-319 (and Grep for `_component(`); `session_identity.py` :30-54; `event_store.py` :474-487; `role_digest.py` :316-327; `manual_capture.py` :287-299; `native_context.py` :1-32; Grep of `worker_lifecycle.py`
- Greps (Grep tool, scripts/): `in ['"]/\\\\:`; `for \w+ in ['"][^'"]*(\\\\|/)[^'"]*['"]\)`; the `.`/`..` tuple and set form; `is_one_component`; the hooklib import lines of the six files. Each found the known sites (positive control)
- `scripts/tests/test_resolver.py` :1-24, :54-58, :389-395, :1055-1108, :1318-1475 (+ Grep of defs)
- `scripts/tests/test-layers.json` :1-40, :4316-4350 (+ Grep: `test_resolver.py` appears once, in keep; `quarantine` at :7004)
- `scripts/tests/scenario_walk.py` :833-932 (`witness_for` matches by import closure and keep `covers`)
- `scripts/tests/test_judgment_census.py` :150-299; `scripts/tests/fixtures/judgment-census.json` (Grep of rows)
- `ai-packages/qa-factory/design/architecture.md` :130-224 (AR-13, AR-15, AR-20, AR-29)
- `plans/builder-rules.md` (Grep 7b/witness-for); `docs/SIBLING_MAP.md` axis 8 (:202-223), axis 34 header (:582)
- Not opened: `docs/TESTING.md` and `design/factory-rules.md` in full. The FR lines come from the auto-loaded index, and the test scope from builder-rules 7b. This is noted as a gap, not as a check.
