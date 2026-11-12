# Spec (DRAFT, designer t-095, revised t-103 after critic-on-plan t-098): the Lead's context after a compaction, short hand-backs, command hygiene cut to its refusals, the worktree guard's door, the dispatch gate

Status: revised draft for Lead acceptance (critic-on-plan t-098 verdict `fit_with_fixes`, `docs/tasks/specs/reviews/t-098-fg-context-hygiene-plan.md`; every finding answered in §13). Feature F19.
Source: `docs/tasks/specs/fg-context-and-hygiene-lead-brief.md` (owner's words 1-7 of 12.11.2026, directions A-E);
calibration `docs/tasks/specs/reports/calibration-20261112.md` + parts p1-p4; nodes FG7-18, FG7-19, FG7-20, FG7-24, FG7-25
(`plans/piles/forge/batch-7-vhodyashchie-4.md:41-48`).

## Lead acceptance of the draft (12.11.2026, dev1) — read before §0

Accepted as the plan for critic-on-plan. Corrections and decisions of the Lead; where a line here differs from the text below, this line wins.

- **F4 is wrong.** `autoCompactWindow: 350000` IS in `.claude/settings.json` (line 3, commit 97fae62; read by the Lead after the draft). A0.3 is dropped; A0.1 still measures whether the host honours the key.
- **The owner's word of 12.11 after the brief:** "тогда нужно убрать это правило … надо и из правил убрать" — the rule "every custom form is a permission request" and its point 3 (`cd … &&`, ` 2>&1` as allowlist breakers) are REMOVED from the rule text, not only silenced in the gate. C2 does exactly that; C2 is not optional and lands in the same merge as C1. Role files, the skill and check 27 lose the same motive in that merge.
- **Forks, all decided by the Lead on the recommendation** (technical; the owner may cancel any): F-A1 keep 300K; F-A2 wait for F6-36; F-B1 at most 2,000 characters and 3 + N lines; F-B2 builder, critic, designer; F-B3 file check only, the reader queued; F-B4 keep the anchor test, queue the registry; F-C1 by C0's measurement (alters `$?` only -> allow everywhere); F-C2 one short WARN; F-C3 content writes only, ignore row `ci-out/`; F-C4 own masks, convergence queued on axis 11; F-C5 the rollback class includes `git reset --hard` and `git clean -f`; F-C6 three findings in `forge`; F-D1 both; F-E1 Lead-only; F-E2 queued; F-E3 owns + numbered items outside the sections; F-E4 refusal with a door (the owner's words 4 and 6); F-E5 hook + RUNBOOK; F-E6 `test_driver_layers.py` stays out.
- **Two false refusals met by the Lead the same hour** (evidence for C1's rows): a read-only `grep … logs/journal/*.jsonl … 2>/dev/null` refused as a journal write (the F10 class, with `2>/dev/null`), and `grep … 2>&1 | head` refused for the trailing-redirect class. Both are rows of C1's table and must pass.

### Lead acceptance of the revision t-103 (12.11.2026, dev1)

The revision is accepted: §13 answers every finding of t-098, and the Lead read §4 (error direction, the classes, the
texts) and §9 against the verdict. No second critic pass on the plan: the revision does what the verdict prescribed
and adds no architecture of its own (PROJECT.md, new idea step 6); the code critic of each node reads the spec.
Forks decided (technical, by the Lead; the owner may cancel any):

- **F-A2 = (a)**: a named open limit with detector check 32 and the existing duty "sessions open in the clone root".
  The earlier "wait for F6-36" is withdrawn. (b) — hooks in the operator's user-level settings — is the owner's own
  file and is offered to her, never done by a builder.
- **F-A3 = (a)**, **F-C7 = (a)**, **F-C8 = (a)** (stash / stash push with a dirty scope join the rollback class as
  one data row in C1; `stash drop` / `clear` a named residual).
- **F-E7 = (b), narrowed**: `dod` leaves `ITEM_EXCLUDED_SECTIONS` (numbered acceptance criteria are spec items,
  rule 2); `edges` STAYS excluded — an edge enumeration is not a list of spec items. The earlier F-E3 decision is
  corrected by this line.
- The designer's closed choices of §9 stand, `checkout -f` and `switch --discard-changes` included.
- Told to the owner as "решила сама": the brief's §D sentence is narrowed (§5) — the "worktree guard" of t-084 is
  most likely `hygiene_gate` class (a); D0 measures it and D1 exists only on another outcome.
- At C2's acceptance the Lead reads CLAUDE.md hygiene point 1 as rewritten and strikes anything that reads as the
  removed permission rule.

## 0. Facts this draft rests on (read in the carrier; see "Reading trail")

| # | Fact | Carrier |
|---|---|---|
| F1 | SessionStart with `source == "compact"` ALREADY appends ONE line `COMPACT SNAPSHOT: <newest *.md by mtime> (<age> min old)` (or `none`) after the boot lines. It picks by mtime among ALL `*.md` except README: hook snapshots and hand-written files alike. | `tools/session_context.py:2218-2241`, `:2309-2312` |
| F2 | That line was seen after 5 of 6 compactions in the window; all 6 were `trigger: manual`; no auto-compaction was observed. The failed one is recorded under the transcript project "C--QAFactory" — the session was OPENED in the clone's parent. | `calibration-20261112-p4.md:19`, `:53-64` |
| F3 | Every hook command is cwd-relative (`python tools/<x>.py`). The cwd fix is node F6-36, batch `onboarding-forge/1`, status `ожидает`. | `.claude/settings.json:5-41` (read); `plans/piles/onboarding-forge/batch-1-onboarding-roles-forge.md:3,52` |
| F4 | CORRECTED by the Lead (acceptance section): `autoCompactWindow: 350000` is at `.claude/settings.json:3` — live now. | `.claude/settings.json:3` (re-read t-103) |
| F5 | `compact_snapshot.REMINDER` sends the reader to the `## State at` section of `docs/tasks/factory-fixes.md` (dated 02.10). PROJECT.md names `docs/tasks/compact-snapshots/<дата>-manual.md` as the hand-written narrative — the SAME name family the hook writes (`<YYYY-MM-DD-HHMM>-<source>.md`, `write_unique` adds `-2`, `-3` within one minute). The committed hand-written `2026-11-12-1210-manual.md` is indistinguishable by name from a hook snapshot. The hook writes no session id into the file today. | `tools/compact_snapshot.py:73-78,541-556,632-649,675-683`; PROJECT.md:273; `docs/tasks/compact-snapshots/` listing (t-103) |
| F6 | `agent_budget.py` ALREADY warns the main session at 300K and every +50K and keeps the last context size in a per-transcript sidecar (`ctx`); its text does not name the snapshot duty. PROJECT.md:273 says the warning repeats "каждые ~100K" while `MAIN_STEP = 50000`. | `tools/agent_budget.py:111-112,124-125,266-279`; PROJECT.md:273 |
| F7 | The 25-line digest rule ALREADY exists in builder 7, critic 16, designer 5, pinned by `tools/test_handoff_rule_anchors.py`; `dod_gate.BLOCK_MESSAGE` asks for "a COMPLETE final report all over again". | `.claude/agents/builder.md:64-84`; `tools/test_handoff_rule_anchors.py:23-44`; `tools/dod_gate.py:119-126` |
| F8 | Final-message length was NOT measured (p3 vs `handback_extract.py` disagree); "2-4K tokens today" (brief:36) is an estimate. | `calibration-20261112-p3.md:223`; `tools/handback_extract.py:14-32` |
| F9 | `hygiene_gate` today: class (a) refuses `cd`/`Set-Location` + a continuation when the target's BASENAME equals the basename of the folder holding the RUNNING copy (`_REPO_ROOT_NAME = Path(__file__).resolve().parents[1].name`), with `MSG_CD_PREFIX`; other targets WARN; `Push-Location`/`pushd` not recognised; class (b) ` 2>&1` BLOCKs; class (c) `python -c` WARNs (`PYC_DENY_ENABLED = False`), `PY_DASH_C_RE = \bpython\s+-c\b` (so `python -B -c`, `python3 -c` are not even classified); class (d) journal BLOCK = ANY write form and a journal substring in ONE statement, not tied to one object (`>` of `2>/dev/null`, a bare `echo` word count). Decisions are assembled in `_classify`, called only by `decide()`. | `tools/hygiene_gate.py:272-274,387-390,394-428,488-547,575-658,678,761-806,940-1047,1093-1214,1223-1261` |
| F10 | Measured false positives of class (d): `ls <journal> 2>&1`, `grep x <journal> 2>/dev/null`, `grep -c "echo" <journal>`, a python heredoc read holding a journal path and a `>` in strings (critic R1, live denial). | `calibration-20261112-p3.md:202`; t-098 B2 |
| F11 | `permission_audit.classify_hygiene` replays EVERY window command through `hygiene_gate._collect_signals` ("a single source of truth"); its labels are the four old classes. So anything `_collect_signals` does runs over thousands of historical commands at audit time. | `tools/permission_audit.py:454-479` |
| F12 | `permissions.allow` exists (commit 7214fe4) with `Bash(...)` and `PowerShell(...)` rows; whether the host matches the `PowerShell(...)` form is not measured. | `.claude/settings.json:133-173` |
| F13 | `dispatch_manifest.py` is a PURE module. `KEY_GROUPS` is a closed tuple; `SKIP_REFUSED_TEMPLATE` and `UNCHECKED_NOTE_TEMPLATE` hard-code the six items; `_SKIP_SEP_RE` accepts `--` and `—`. `section_cut` ends a section at the NEXT header or at the end of the text; `_section_paths` reads a section's header tail and the lines under it up to the FIRST BLANK LINE. | `tools/dispatch_manifest.py:71-128,254-307,546-581` |
| F14 | `scenario_walk.witness_for` covers package paths only; FG7-15 (pending) extends it to `tools/`. Importing `scenario_walk` imports `harness`, which inserts package paths at the head of `sys.path` and sets `os.environ` keys. | `ai-packages/qa-factory/scripts/tests/scenario_walk.py:30-33,887-922`; `harness.py:23,33` (t-098 F13) |
| F15 | Three hand-kept carrier lists exist already in `tools/test_quarantine.py` (`:51`, `:1337-1346`, `:2194-2195`). | `tools/test_quarantine.py` |
| F16 | REPLACED (t-098 F1). The "worktree guard" of t-084 has one carrier sentence: "the worktree guard refuses compound git commands". Two repo candidates refuse such a command: `hygiene_gate` class (a) — a worker's hook runs the WORKTREE's copy (cwd-relative command), whose root basename is the worktree folder (`agent-<id>`), so `cd <its worktree> && git grep` is refused with `MSG_CD_PREFIX`; and `agent_budget.PLAIN_GIT_RE` past the 400K STOP. Which one fired is not yet read in t-084's transcript. | `docs/tasks/specs/reports/t-084-td11c-NC.md:79`; `tools/hygiene_gate.py:624-634`; `.claude/settings.json:38`; `.claude/worktrees/agent-*/` (listing, t-103); `tools/agent_budget.py:118` |
| F17 | Role files cite "command hygiene point 6" by number and say "canonical form" (critic 66, 74; builder 61; designer 43); so does `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:123`. | grep t-103 |
| F18 | `CLAUDE.md`, `PROCESS/`, `.claude/agents/`, `.claude/skills/`, `.githooks/`, `.claude/settings.json`, `tools/dispatch_manifest.py` and every hook file named here are mechanism paths. The gate counts a literal `axis N:` (or `axis N (<key>):`) line for each of the 36 axes. | `tools/mechanism_gate.py:24-54,211-274,384-460` |
| F19 | `C:\QAFactory\.claude` does not exist; `C:\QAFactory\forge-repo\.claude\settings.json` does (positive control, same tool). A session rooted in the parent loads none of the clone's hooks. | Glob t-103 (both paths) |
| F20 | `tools/gitcmd.py` `git(root, *args, timeout=...)` is the one git runner (axis 10); git missing or a timeout returns rc -1, never raises. | `tools/gitcmd.py:1-55` |
| F21 | `dod_gate.evaluate` returns "no-edits" before anything else for an agent with no edits, and `main` does not save a track that did not exist when the call adds no edits. `consecutive_blocks` per agent resets on a passing stop. `handoff_gate` compares paths by `os.path.normcase(os.path.realpath(...))` and filters by `HANDOFF_DIRS` with `_in_folder`. | `tools/dod_gate.py:195-223,262-304,412-431`; `tools/handoff_gate.py:89-101,145` |
| F22 | `tools/test_warn_messages.py` pins `MSG_CD_PREFIX`, `MSG_REDIRECT_STDERR`, `MSG_PYTHON_DASH_C`, `MSG_CD_NON_ROOT_WARN` by name with a count `"HYGIENE": 4`, and loads `dispatch_gate` messages. `tools/warn_layers.json:196-209` holds the HYGIENE row (`reachable: unmeasured`). | `tools/test_warn_messages.py:95-96,173-188,304-307,498`; `tools/warn_layers.json:196-209` |

## 1. Scope, invariants, architecture

Non-goals (dispatch): no factory package behaviour; no session relay; no change to which model plays which role; no fork decided.

ARCHITECTURE: no node owns a path under `ai-packages/qa-factory/`. E2 RUNS `scenario_walk.py --witness-for` as a subprocess and reads package carrier files; nothing writes there. So the package commit line is not owed; a node that ends up writing a package path is a spec defect returned to the Lead. AR-n named for the forge analogues the critic holds the nodes to: AR-13 (one reader of a fact: the carrier list, the owned paths, the section extent, the hygiene signals, the snapshot identity), AR-9/FR-1/FR-2 (every refusal names what it expected and a door its receiver can use — reading roles included), AR-29/P27 (code checks form and data, the Lead/critic judge sufficiency), AR-22 (producer and reader in one commit: `_collect_signals` <-> `permission_audit`; the snapshot header writer <-> its reader), AR-1 (shell differences and interpreter differences are data rows read by capability), P31 (one road: main session and workers, Bash and PowerShell, redirect and interpreter payload get one rule unless a capability row says otherwise).

Owner of every check added or altered (P27, AR-29; census class in the forge sense: "data check" = code over shape/presence, never a verdict on meaning):

| Check | Serves | Class |
|---|---|---|
| A: post-compaction lines; "this compaction's snapshot" by content identity and the announced record | data (file content header, age, record) | data |
| B: handoff file exists and was written by this worker | data | data; the report's completeness = judgment of the Lead at acceptance |
| C: refusal of cd / content write with a resolved literal target / journal write / rollback of dirty paths | data (the command's form, the literal target's place, the paths' git state measured in the addressed repository) | data; "was the edit worth it" stays with the reviewer |
| C: one WARN for an interpreter payload the gate cannot resolve | data | data |
| E: `siblings:` line present and well-formed; designer threshold counted; carriers and witnesses printed | data | data; whether the siblings list is SUFFICIENT = critic/Lead (judgment) |
| E3: pre-push fast set | data (exit codes) | data |

## 2. A — the Lead's context after a compaction (FG7-25)

§1 Goal: after a compaction the Lead's first context names the snapshot written for THIS compaction (or says it is missing, with the door), the newest hand-written narrative, the open dispatches, and one instruction "read the snapshot before your next action".
Invariant: a snapshot measured before an earlier compaction never counts as this compaction's, and a missing/old snapshot is never shown as fresh.
Where the invariant is NOT kept, stated as named open limits (t-098 F6, F7), each with check 32 as its detector:
- a session OPENED in the clone's parent (`C:\QAFactory`, F2, F19) loads none of the clone's hooks: no PreCompact snapshot, no SessionStart line. No forge hook can keep the invariant on this path; F6-36 (absolute hook commands) does not register hooks for a session rooted elsewhere. Fork F-A2 (reopened).
- auto compaction is live now (`autoCompactWindow: 350000`, F4) while A0.1 has not shown that auto compaction reaches PreCompact and SessionStart `source=compact`. Until A0.1 (and A3 where it is needed) an auto compaction may leave no pointer.

### A0.1 — experiment (operator or Lead, not a builder: t-098 F10)
owns: `C:\QAFactory\forge-repo\docs\tasks\specs\reports\fg-ctx-A0-1-autocompact.md` (written by the Lead)
A builder subagent has no interactive session and cannot watch another session's hooks, so this runs in a throwaway interactive session the operator (or the Lead) opens at a worktree root, with an untracked `.claude/settings.local.json` that sets a small `autoCompactWindow` (for example 60000) and adds echo hooks for `PreCompact`, `SessionStart` and `PostCompact` that append the raw hook payload to a scratchpad file. Cost: one session driven past the small window (estimate: about 60K tokens).
Records, each with the verbatim payload lines:
1. whether the host honours the key (an auto compaction happens near the window);
2. whether PreCompact fired with `trigger: auto` (a `*-auto.md` file under `docs/tasks/compact-snapshots/`);
3. whether SessionStart fired with `source: compact` after the auto compaction;
4. whether a `PostCompact` event exists (its echo file has a line);
5. whether the `session_id` of the PreCompact payload equals the `session_id` of the following SessionStart `compact` payload (A1's identity).
Outcomes: items 2-3 yes -> A3 is not opened; item 3 no -> A3 per the outcome table below. Item 5 equal -> A1 matches by session; different -> A1's `MATCH_SESSION` constant is set False (one line), freshness rests on the announced record and age alone.

### A0.2 — reading (scout)
owns: `C:\QAFactory\forge-repo\docs\tasks\specs\reports\fg-ctx-A0-2-parent-root.md`
Read the transcript project folder of session 646c4aac (the snapshot-less compaction of 11.11 21:09): report its slug (`~/.claude/projects/<slug>/`) and the first `cwd` field of the transcript. Outcomes: the slug is the parent folder (`C--QAFactory`) -> the named limit above stands and F-A2 is decided on that fact; the slug is the clone -> the cause is elsewhere, F-A2 goes back to the Lead with the transcript lines quoted. DoD: the report quotes the path and the lines read (trail).

### A1 — the post-compaction lines, identity by content
owns:
`C:\QAFactory\forge-repo\tools\compact_snapshot.py` (`_read_trigger_from_stdin` -> returns trigger and session_id, `build_snapshot`'s first line, `write_snapshot`, `main` (`--session`), `REMINDER`, new `HOOK_HEADER_PREFIX` and `snapshot_identity`)
`C:\QAFactory\forge-repo\tools\session_context.py` (`compact_snapshot_line` -> `compact_snapshot_lines`, the `source == "compact"` branch of `main`, new announced-record read/write)
`C:\QAFactory\forge-repo\tools\test_session_context.py`
`C:\QAFactory\forge-repo\tools\test_compact_snapshot.py`
Behaviour:
1. The hook snapshot carries its identity in content (t-098 F5): its FIRST line is `<!-- compact-snapshot: hook; session: <id|unknown>; trigger: <manual|auto|unknown>; written: <ISO local> -->`. `compact_snapshot.snapshot_identity(path) -> {"session", "trigger", "written"} | None` reads at most the first 512 bytes; it is the ONE reader of that line (writer and reader in one module, AR-22); `session_context` imports it. The session id comes from the PreCompact stdin payload, or from `--session <id>` (the door below); absent -> `unknown`.
2. A hook snapshot = a `*.md` file of `docs/tasks/compact-snapshots/` whose `snapshot_identity` is not None, whatever its name (`-2` suffixes, any `--source` value). A hand-written narrative = every other `*.md` except README.
3. A hook snapshot S is "this compaction's" when ALL hold: S is not in the announced record; its age is at most `STALE_MIN` (10 min); and, when both the SessionStart payload's `session_id` and S's `session` are known and `MATCH_SESSION` is True, they are equal. Among such files the newest by mtime wins (equal mtime: name order).
4. On `source == "compact"` the appended block, after the boot lines (survives `MAX_LINES`):
   `COMPACT SNAPSHOT: <path of S> (<age> min old, trigger <t>)` — or, when no S qualifies, `COMPACT SNAPSHOT: MISSING for this compaction (newest hook snapshot <path|none>, <age> min old) -- write it now: python -B tools/compact_snapshot.py --source manual --session <id>`;
   `COMPACT NARRATIVE: <newest narrative> (<age> min old)` only when a narrative exists that is newer than S (or S is missing);
   `AFTER COMPACT: read the snapshot above before your next action; accept the OPEN DISPATCH lines in a batch`.
5. After printing, S's file name is appended to the announced record `.claude/compact_seen.json` (a list, last 200 names kept). The record is what makes a second compaction inside `STALE_MIN` with a failed PreCompact show MISSING (t-098 F5 (c); fork F-A3, builders proceed on it).
6. `REMINDER` names what PROJECT.md names after node P's edit: the newest `docs/tasks/compact-snapshots/*-narrative.md` and CURRENT_CONTEXT.md, instead of `factory-fixes.md`.
Error direction: the freshness check may err toward MISSING (a false MISSING costs one door run), never toward "fresh" for a snapshot already announced or older than `STALE_MIN`.
Edges (each with the invariant it protects):
- folder absent -> MISSING line with the door (never a pointer to nothing);
- stat or read failure of a file -> that file is skipped; all failing -> `COMPACT SNAPSHOT: unavailable (<reason>)` + the door, never a crash (fail-open of the hook kept);
- announced record absent -> empty record (first compaction after A1); record unreadable or not a JSON list -> every candidate counts as announced -> MISSING + door (the error direction above), plus `COMPACT SNAPSHOT: announced record unreadable (<reason>)`; record not writable -> the block is printed and one line `COMPACT SNAPSHOT: announced record not written (<reason>)` follows (the next compaction may then show this S once more within `STALE_MIN`: named limit, check 32);
- a file whose first line is a corrupt header (prefix present, fields missing) -> hook snapshot with `session: unknown`;
- clock skew (mtime in the future) -> age 0, not negative;
- session id absent from either payload -> the session clause is skipped (never a refusal of freshness on a missing field);
- two Lead sessions in one clone -> the session clause keeps another session's fresh snapshot from counting (when ids are known);
- `source` other than compact -> nothing added (unchanged).
Temporal (both worlds): before A1, hook snapshots carry no header; after A1 lands, those old files read as narratives and can never be "this compaction's"; the first compaction after the merge writes a headed snapshot. Before A0.1, auto compaction is unverified: A1's lines work for whatever reaches SessionStart with `source=compact`; A1 is not reworked by A0.1's outcome except the `MATCH_SESSION` line.
Tests (layer 3 table rows in the existing files, no new file): `test_session_context.py` one parameterised table: fresh headed snapshot / headed snapshot 11 min old (MISSING) / headed snapshot already announced (MISSING) / two compactions inside `STALE_MIN`, second PreCompact absent (MISSING on the second) / hand-written file named `2026-11-12-1210-manual.md` without header, newest (MISSING + NARRATIVE; the F5 file) / headed `-2` suffix file (fresh) / session mismatch with `MATCH_SESSION` True (MISSING) / session unknown (fresh) / no folder (MISSING + door) / record corrupt (MISSING + record line) / record not writable (block + not-written line) / non-compact source (no lines). `test_compact_snapshot.py`: header written with session and trigger from a payload / `--session` overrides / `snapshot_identity` round trip / REMINDER names no file absent on disk (a data join, not a phrase pin).
DoD: `python -m pytest tools/test_session_context.py tools/test_compact_snapshot.py -q` green (owned paths are outside the package: these are the test files that judge them, CLAUDE.md rule 4); node P lands check 32, 17 (d) and the PROJECT.md line in the same merge (§7, §8).

### A2 — the main-session WARN names the duty
owns: `C:\QAFactory\forge-repo\tools\agent_budget.py` (`_warns` text only), `C:\QAFactory\forge-repo\tools\test_agent_budget.py`
Behaviour: the main-session context WARN (not the worker's) adds: "write the compact snapshot (docs/tasks/compact-snapshots/) and tell the operator the one line (PROJECT.md)". Thresholds unchanged (300K, +50K; F-A1 decided). The "каждые ~100K" sentence of PROJECT.md:273 is aligned to +50K by node P in A1's merge (t-098 Q1 F6).
Edges: worker WARN text unchanged; context unknown -> no WARN (unchanged). Test: one row in the existing main-WARN table asserting the text names the snapshot folder. DoD: `python -m pytest tools/test_agent_budget.py -q`.

### A3 — conditional (opened by A0.1's outcome; not built before)
| A0.1 outcome | A3 |
|---|---|
| auto fires PreCompact and SessionStart `compact` | not opened |
| SessionStart `compact` absent, `PostCompact` exists | a `PostCompact` hook entry running `python tools/session_context.py --after-compact` (prints A1's block); owns `.claude/settings.json` (the Lead places it, enforcement-file rule) + that argument in `session_context.main`; ordered after F6-36 (same settings file) |
| neither SessionStart `compact` nor `PostCompact` | the host-independent fallback (t-098 F6): `agent_budget.evaluate`, on a main-session PreToolUse whose context is below half of the sidecar's previous `ctx`, injects A1's block once as `additionalContext`; owns `tools/agent_budget.py` (`evaluate`) + `tools/test_agent_budget.py`; after A2 (same file) |
| PreCompact does not fire on auto | the fallback above still prints the block; its first line is then MISSING with the door (a snapshot cannot be written before a compaction nobody announced) — named |
Each A3 variant gets its own spec section from the Lead before dispatch (it is not built from this table alone).

Four questions (A1+A2+A3, one mechanism "post-compaction pointer"):
(a) cost: three or four lines per compaction and one small record write; nobody pays at other times. (b) axes: §10 table, column A. (c) detector: check 32 (edited, §8) + `test_session_context.py`. (d) on the path: the SessionStart hook the host runs on compaction (and A3's carrier where opened); the Lead reading the line is discipline, detector check 32 (a compaction followed by a Lead action before any Read of the named snapshot = a finding).

## 3. B — short hand-back

§1 Goal: a worker's final message is a pointer plus a per-item status; everything heavy lives in the report file.
Invariant: work done is never lost — a worker whose dispatch names a `handoff:` path either wrote that file itself or says in its message why the Write was refused; a message with no path and no report never counts as delivered; the Lead never retypes a report.

Target and form (F-B1 decided: at most 2,000 characters and at most 3 + N lines, N = numbered spec items; F-B2 decided: builder, critic, designer; scout unchanged).
```
report: <absolute path of the handoff file>
1 done | 2 done | 3 not done -- <one clause> | 4 question
questions: none | 1) <question>
needed beyond the manifest: none | <paths>
```
No witness lines, tables, logs or file lists in the message (they are in the file). With no `handoff:` path, or a refused Write: the full report goes into the message as today (no cap) — unchanged world.

### B0 — one measurement (builder, no code)
owns: `C:\QAFactory\forge-repo\docs\tasks\specs\reports\fg-ctx-B0-handback-size.md`
Settles F8: `python -B tools/handback_extract.py --agent <id> <scratch out>` on 10 workers of 12.11 (ids from `worker_ref` of dev1.jsonl); record `lines=`/`bytes=` per worker and whether `source=handback`. Outcomes: hand-back text present -> check 28 (b) counts messages over the cap with this reader; absent -> F-B3 (decided: file check only, reader queued). DoD: the report quotes each command and its verbatim output.

### B1 — the rule text
owns:
`C:\QAFactory\forge-repo\.claude\agents\builder.md` (rule 7 only)
`C:\QAFactory\forge-repo\.claude\agents\critic.md` (rule 16 only)
`C:\QAFactory\forge-repo\.claude\agents\designer.md` (rule 5 only)
`C:\QAFactory\forge-repo\tools\test_handoff_rule_anchors.py`
Behaviour: the three rules carry the new cap and form; "the closing lines of the witness" leaves builder 7; the fallback sentence ("never lost, never shortened"), "names no such path", "the Write is refused" and `ceil(len/200)` stay (anchors). The rule numbers do not move (check 28 (a) and the test key on them). `K2 = "at most 25 lines"` becomes the new cap key; the RESTATED list is updated so `docs/tasks/critic-diff-brief.md` and `plans/builder-rules.md` 11 still only point.
Edges: both caps bind at once -> the message satisfies both (the stricter one decides; t-098 Q7); the form may put the N statuses on one line, so the line cap usually does not bind and the character cap does — stated, not a defect; a dispatch whose spec is a pointer (R11-m) -> N is counted in the persisted spec it points to; 0 numbered items -> cap 3 lines + the path; more than 20 items -> ranges allowed (`1-12 done`); resubmission after a hook block -> path and digest whole (unchanged rule).
Tests: the existing anchor table rows with the new key; no new file (F-B4 decided: the text pin stays as check 28 (a)'s detector, the registry queued).
DoD: `python -m pytest tools/test_handoff_rule_anchors.py -q`.

### B2 — the code layer at SubagentStop
owns: `C:\QAFactory\forge-repo\tools\dod_gate.py` (`BLOCK_MESSAGE`, `evaluate`/`decide` for the new check, `main`'s save condition), `C:\QAFactory\forge-repo\tools\test_dod_gate.py`
Behaviour:
1. `BLOCK_MESSAGE` resubmission clause: "repeat the path and the digest whole (or, with no handoff path, the full report)" instead of "a COMPLETE final report all over again".
2. New data check "handoff missing", run for EVERY stopping agent, BEFORE the "no-edits" return (t-098 F12: the main case is a critic or designer that never wrote): the worker's dispatch text is read through `transcripts` and `dispatch_manifest.handoff_paths` (the readers `handoff_gate` uses; no second parser, axes 13/14); candidates are filtered to paths that lie in a `HANDOFF_DIRS` folder, by importing `handoff_gate._in_folder` (one reader, no copy). When exactly one candidate remains and the session track holds no Write/Edit by THIS `agent_id` whose path MATCHES it, block ONCE per agent with: "HANDOFF MISSING: your dispatch names <path> and you did not write it. Write the report there; if the Write was refused, put the full report in your final message -- this block will not repeat." Recorded in `gate_log` as `handoff_missing`.
3. Path match (t-098 F12): equal `os.path.normcase(os.path.realpath(...))` values (case-insensitive and slash-normalized on Windows), OR equal trailing segments from the `HANDOFF_DIRS` folder down to the file name (a worktree copy `<clone>/.claude/worktrees/agent-x/docs/tasks/handoffs/r.md` matches the dispatch's `<clone>/docs/tasks/handoffs/r.md`).
4. The once-key is `gate_state["per_agent"][<agent key>]["handoff_missing_blocked"] = True`, separate from `consecutive_blocks` and never reset by a passing stop. `main` saves the track when this block fires even if the track did not exist before (the once-key must persist); the "do not grow an empty track" rule holds for every other no-edit stop.
Error direction: may err toward PASS (an unreadable dispatch, transcripts or handoff_gate not importable, a degraded cut, two or more candidates, a different clone with the same trailing segments -> pass, with a stderr line where something failed), never toward a second block for this reason (the hook cannot see the final message).
Edges: no handoff path, or none inside a `HANDOFF_DIRS` folder -> no check (a builder's handoff line naming a non-report path is not "missing"); handoff path relative -> no check (`handoff_paths` returns absolute only); the file exists but was written by another agent or by main -> block once; the existing safety valve (2 blocks) counts this block too; doc-only exemption unaffected; a track that does not exist and no block -> nothing written (unchanged). Temporal: tracks written before B2 lack nothing (dod_track already records `file_path` per `agent_id`).
Tests: `test_dod_gate.py` one table: written by this agent (pass) / not written (block once) / second stop after that block (pass) / no handoff line (pass) / handoff path outside `HANDOFF_DIRS` (pass) / two candidates (pass) / transcripts import fails (pass + stderr) / written by main (block once) / no-edit critic, no track file, not written (block once AND the track file now exists with the once-key) / written under a worktree copy of the path (pass) / path differing in case and slash direction (pass).
DoD: `python -m pytest tools/test_dod_gate.py tools/test_handoff_gate.py -q` (the second as a reader check of `_in_folder`, not owned).

B1 and B2 land in ONE merge, with check 28's edit applied by node P in that merge (t-098 F8 (c): check 28 names both the 25-line cap B1 changes and the `dod_gate` text B2 changes).

Four questions (B, one mechanism "short hand-back + report-file check"):
(a) cost: the worker writes one file it already writes; the Lead reads the file at acceptance (check 28 (d)); saves an estimated 1-3K tokens of Lead context per hand-back (F8, not measured). (b) axes: §10 table, column B. (c) detector: check 28 rewritten (§8): `handoff_missing` gate_log entries, messages over the cap counted by `handback_extract` (or F-B3), retypes (28 (d)). (d) on the path: `dod_gate` SubagentStop for the file; the message cap itself is discipline, detector check 28 (b).

## 4. C — command hygiene: four refusals, the rest allowed

§1 Goal: the gate refuses the four behaviours that hurt quality or team work, each with a door its receiver can use; every other form (compound commands without a directory change, a leading variable, loops, `python -c` for reading or calculation, `grep/cat/sed` without writing, `2>&1` in Bash, file-level `rm`/`mv`/`cp`) passes silently and stops counting as a violation.
Invariants (what must stay refused):
1. the session shell's working directory is never moved;
2. a file of a git working tree never gets its CONTENT written by a shell redirect, a write cmdlet, a .NET file write, an in-place editor or an interpreter payload whose target is a literal path (restated per t-098 F3: file-level copy/move/create/delete is outside C by F-C3, in every syntax);
3. the journal is written only through Edit/Write;
4. a working-tree change of the addressed repository is never discarded by a checkout/restore/reset/switch/clean while `git status` shows it.
Equally: a read or calculation is never refused, and no refusal is issued on a target the gate could not resolve.

### Error direction (designer rule 1: the payload classifier moves from advice to gate)
A REFUSAL requires certainty: a certain form AND a resolved literal target (or, for rollback, a measured dirty status). Everything uncertain passes; an interpreter payload the gate cannot resolve gets F-C2's one short WARN. Asymmetry by cost: a false refusal of a reading role is a dead end when its door is unusable (a critic, designer or scout cannot Write a script: `handoff_gate`), so the refusal set is kept to certain writes; a false pass costs an unreviewed edit, caught later by check 27 (a) and the reviewer.
The advisory lists of `_classify_single_payload` (`_PATH_MUTATING_METHOD_NAMES`, `_OS_MUTATING_QUALIFIED`, `_DUMP_QUALIFIED`, `_WRITE_METHOD_NAMES`, `_STDIO_DOTTED`, …) are NOT re-labelled and NOT promoted: they lean toward M on purpose (`hygiene_gate.py:954-956`) and stay the audit's measuring instrument (`pyc_payload`). The gate reads a NEW constant next to them (t-098 B1).
Adversarial inputs that must stay on the safe side (never refused): `print('a/b'.replace('/','-'))`; `json.dump({'a':1}, sys.stdout)`; `sys.stdout.buffer.write(b'x')`; `io.StringIO().write('x')`; `csv.writer(sys.stdout).writerow([1])`; `open(r'C:/Users/x/scratchpad/f.txt','w').write('x')`; `open(p,'w')` with `p` a variable; `print(open('a').read())`; `os.remove('docs/a.md')` (file-level, as `rm`); a heredoc read whose strings hold a journal path and a `>`.

### Where each signal is computed (t-098 B4)
`_collect_signals(command)` stays PURE — no subprocess, no filesystem access, no clock — because `permission_audit.classify_hygiene` replays every historical window command through it (F11). It returns FORMS only: cd hits, literal write targets, the journal flag (a pure pattern on the literal target), the rollback form, the payload classes. Everything that needs the filesystem or git — resolving a target's working tree, `git status`, statting a single checkout argument — runs only in `decide()` (which passes the results into `_classify`). The audit therefore counts SHAPES; the gate's VERDICTS are read from the transcripts (check 27).

### The statement walk (F-C4 decided: own masks)
Per top-level statement, on text with quoted segments masked and foreign heredoc bodies masked (the existing masks). Statement starts: the start of the command, after `;`, `&`, `|`, a newline, and after the words `then`, `do`, `else`, `elif`, `{`, `!`, `builtin`, `command`, `time` (t-098 F2). `(` and `$(` open a SUBSHELL region. The `MAX_HEREDOC_OPENERS` cap keeps its role: past it, heredoc-bearing statements yield no write targets (a pathological input never widens a refusal).

### Class cd
Refused: `cd`, `chdir`, `pushd`, `popd`, `Set-Location`, `sl`, `Push-Location`, `Pop-Location` at a statement start, any target or none (`cd`, `cd -`), both shells; `eval` whose argument text starts with one of these verbs (`eval "cd x"`); `[IO.Directory]::SetCurrentDirectory(...)` and `[Environment]::CurrentDirectory = ...`.
Legal: a bare `cd <this checkout's root>` with nothing after it (the way back; root = the folder holding the running copy, as today); a verb inside a SUBSHELL region when the tool's capability row says `subshell_scopes_cwd: true` (Bash `( cd x && … )`, `$(cd x && pwd)`); a verb inside a quoted child-shell argument (`bash -c "cd x && ls"`, `powershell -NoProfile -Command "Set-Location x; ls"`: the child's directory dies with it).
Capability rows (AR-1, read by capability, never by the tool's name in logic): `SHELL_CAPABILITIES = {"Bash": {"subshell_scopes_cwd": true, "cd_door": <Bash door>}, "PowerShell": {"subshell_scopes_cwd": false, "cd_door": <PowerShell door>}}`; an unknown tool name -> the PowerShell row's values (the conservative capability).
Named limits (pass, check 27 (a) reads them): a function or alias defined and called in the same command (`f(){ cd x; }; f` — the `{` start catches the body only when written inline as here; a sourced script that changes directory does not show), `source x.sh`.

### Class mutation (certain content writes)
A write target is a LITERAL path: quotes stripped, `~` expanded; a target holding a variable or a substitution (`$f`, `"$out"`, `%TEMP%`, `$env:TEMP`, `$(...)`, backticks) is not literal -> no target.
- M1 shell: redirects `>`, `>>`, `>|`, `&>`, `&>>`, `N>` with N ≥ 1 to a file (not an fd: `2>&1`, `>&2`, `1>&2` are not targets); `tee [-a]`, `Tee-Object [-FilePath]`, `Out-File [-FilePath]`, `Set-Content [-Path]`, `Add-Content [-Path]` (the first path argument); `[IO.File]::WriteAllText|WriteAllLines|WriteAllBytes|AppendAllText|AppendAllLines(<literal>, …)` (t-098 F3). Null sinks are never targets: `/dev/null`, `$null`, `NUL`, `nul`.
- M2 in-place editors, as a data row of tool -> in-place flag (AR-1): `sed -i`/`--in-place`, `perl -i`/`-pi`, `awk -i inplace` (gawk), `ruby -i`; every non-option argument after the script argument is a target. An argument the row cannot place -> no target.
- M3 interpreter payloads, as a data row (AR-1): `python`, `python3`, `py` (with or without `.exe`), any flags before `-c`/`-` (`-B`, `-I`, `-u`, `-3`, `-X <opt>`, `-W <arg>`) — the regexes `PY_DASH_C_RE`, `PY_HEREDOC_RE`, `_PY_DASH_C_ARG_RE`, `_PY_HEREDOC_EXTRACT_RE` widened to this row (t-098 F3); `node -e`, `ruby -e`, `perl -e`, `pwsh -c`, `powershell -Command` carry `payload_classifier: none` (a data row, P31: the difference is "no classifier exists", not a branch by name). For a python payload the gate reads the new constant `_GATE_WRITE_FORMS` (beside the advisory lists), which holds exactly:
  (i) `open(<literal str>, <literal mode containing w, a, x or +>)` and `io.open(...)` alike, free or in `with`;
  (ii) `Path(<literal str>).write_text(...)`, `.write_bytes(...)`, `.open(<literal mode with w/a/x/+>)`, the receiver being a call of `pathlib.Path`/`Path` (through the alias map) with one literal string argument;
  (iii) `json.dump(obj, F)` and `pickle.dump(obj, F)` where F is an inline call of form (i).
  A `.write`/`.writelines` whose receiver is a form-(i)/(ii) call belongs to that write (not counted twice). Each such call yields its literal target.
  Every other advisory-M call is classed as one of: STDIO (a `.write`/`.writelines`/`json.dump`/`pickle.dump`/`csv.writer`/`print(file=)` whose target resolves to `sys.stdout`, `sys.stderr`, or their `.buffer`) -> silent; FILE-LEVEL (`os.remove`, `os.unlink`, `os.rename`, `os.replace`, `os.rmdir`, `os.mkdir`, `os.makedirs`, `os.chmod`, `shutil.*`, and the attribute names `unlink`, `rename`, `replace`, `mkdir`, `touch`, `rmdir`) -> silent, as `rm`/`mv`/`cp`/`mkdir` are (F-C3 in every syntax: t-098 B5); everything else (an unresolved `.write`, `csv.writer` to a non-stdio object, `to_csv`/`to_excel`, `print(file=<non-stdio>)`, `open` with a non-literal path or mode, `Path(<non-literal>).write_text`, `os.truncate`) and the advisory O class -> UNCERTAIN -> F-C2's one WARN.
  A relative literal target inside a statement that follows a subshell directory change -> not resolvable -> UNCERTAIN.
Resolution, in `decide()` only: a relative target joins the payload's `cwd` field (absent -> the hook process's cwd); the working tree is found from the TARGET's own path (t-098 F3: a write from a worktree into the main clone is judged by the main clone) — the nearest ancestor of the target holding `.git` (file or directory), by path walk. A target is "in a working tree" when such an ancestor exists, the target is not under that root's `.git/`, and its root-relative path does not start with an ignore row (`HYGIENE_IGNORE_ROWS = ("ci-out/",)`, data; F-C3). Scope of "a working tree": fork F-C7 (recommendation: any git working tree; builders proceed on it).
Refused: any M1/M2/M3 literal target in a working tree. Passes: targets outside every working tree (the scratchpad, temp), null sinks, non-literal targets, ignore rows.
Accepted residuals, named (C does not keep invariant 2 against them; check 27 (a) reads the suspects): `cp`/`Copy-Item`/`mv`/`Move-Item` onto an existing tree file, `New-Item <path> -Value … -Force`, `Copy-Item` into the journal; a named script run from outside the repository (`python C:/scratch/fix.py`) that writes into the tree; interpreters with `payload_classifier: none`; non-literal targets; git plumbing writes (`git show x > f` is M1 and IS refused; `git apply`, `git checkout-index` are not); `cp x logs/journal/dev1.jsonl` (also caught at commit by `journal_validator`'s append-only check).

### Class journal (t-098 B2: one classifier with a target filter)
The journal class is "an M1, M2 or M3 write whose literal target is a journal file": the target's normalized path (backslashes -> slashes, case-insensitive) matches `logs/<…>/*.jsonl` or contains `routing-log`. Pure (no I/O), computed in `_collect_signals`. Refused wherever the target lies — inside or outside a working tree (the existing "always refuse" asymmetry, now only for a resolved journal target). `_is_journal_bypass`, `_has_write_form` and their regex set (`PRINTF_ECHO_RE`, `TEE_RE`, `SED_INPLACE_RE`, `OPEN_WRITE_MODE_RE`, `_PS_WRITE_CMDLET_RE`) are removed in the same commit; the git-statement and commit-message masks stay where M1 needs them (a quoted `>` in `git commit -m "…"` is not a redirect).

### Class rollback (t-098 B4, B6)
Form recognition (pure, in `_collect_signals` -> `rollback_form`): a statement `git` followed by any global options — `-C <dir>` (repeatable; composed left to right: `git -C a -C b` = `a/b`), `-c <k=v>`, `--no-pager`, `--literal-pathspecs` — then one of these shapes. `--git-dir`/`--work-tree` among the globals -> `rollback_form` with `unresolvable: "--git-dir/--work-tree"`.

| Shape | Scope checked | `git status` view |
|---|---|---|
| `git checkout [<rev>] -- <paths>` | paths | tracked only (`--untracked-files=no`) |
| `git checkout <rev> <path>…` (two or more non-option arguments, no `--`) | the arguments after the first | tracked only |
| `git checkout <arg>` (one argument) | `decide()` stats `<arg>` in the addressed directory: an existing file or directory -> that path; otherwise a branch switch -> pass (git itself refuses to overwrite dirty files on a switch without `-f`) | tracked only |
| `git checkout .` | `.` | tracked only |
| `git checkout -f`/`--force` [<branch>] | whole tree | tracked only |
| `git switch --discard-changes`/`-f`/`--force` <branch> | whole tree | tracked only |
| `git restore [<opts>] <paths>` | paths; `--staged` WITHOUT `--worktree`/`-W` -> pass (the working tree is untouched) | tracked only |
| `git reset --hard [<rev>]` | whole tree | tracked only |
| `git clean` with `-f`/`--force` in any flag cluster (`-f`, `-fd`, `-df`, `-xdf`, `-fX`, `-ff`) and no `-n`/`--dry-run` | the pathspec after the options, else whole tree | untracked entries (`??`); with `-x` also ignored (`!!`), with `-X` ignored only; without `-d`, an entry naming a directory (`?? dir/`) is not counted |

Measurement, in `decide()` only: the addressed directory = the payload `cwd` joined with the composed `-C` chain (t-098 B6: the status runs in the repository the command addresses, never in the cwd's when `-C` is given); `gitcmd.git(<dir>, "status", "--porcelain=v1", "-z", <view flags>, "--", *<scope>)` with `timeout=5` (the one git runner, axis 10); view flags: tracked only = `--untracked-files=no`; clean = `--untracked-files=normal` plus `--ignored` when `-x`/`-X`. Pathspec globs go to git as written. A non-empty filtered result -> refuse.
Not measurable -> pass with the visible marker `Command hygiene: rollback not checked: <reason>` (git missing, rc ≠ 0, timeout, `unresolvable`, the hook environment carrying `GIT_DIR` or `GIT_WORK_TREE`, addressed directory absent). This is a named residual of invariant 4; detector check 27 (c).
Stash family: fork F-C8 (recommendation: `git stash`/`git stash push` with a dirty scope join the class; `stash drop`/`clear` stay a named residual). Until the Lead decides, C1 builds the table above only, behind the data row so the addition is one row.

### The four refusals, the WARN, the markers (P15: what is wrong, what is expected, the door; each text ≤ 350 characters)
| Class | Text |
|---|---|
| cd (Bash) | "the shell's working directory must not move: the hooks find tools/ from it. Use git -C <dir>, python -B <absolute path>, a tool's --repo/--root, or a ( cd <dir> && ... ) subshell." |
| cd (PowerShell) | "the shell's working directory must not move: the hooks find tools/ from it. Use git -C <dir>, python -B <absolute path>, a tool's --repo/--root, or a child shell: powershell -NoProfile -Command \"Set-Location <dir>; <cmd>\" (t-098 F14; C0.1 verifies it runs)." |
| mutation | "<target> is a file of a git working tree and this command writes its content past the Edit/Write hooks. Use Edit/Write (or a named committed script). Scratch output: write it outside the tree, or put the code in a script under the scratchpad (python -B <path>). A reading role: Edit/Write your handoff file." (t-098 B1 point 4) |
| journal | "the journal <target> is written only through Edit/Write at the file's tail (journal_echo checks the line). Reading it with grep, cat or tail is fine." |
| rollback | "<n> path(s) under <dir> have uncommitted changes that may be another session's, and this command would discard them. Your own edit: undo it with Edit/Write. A byte copy you took: restore from it. Changes that are not yours: leave them and tell the Lead." (t-098 B6: no door that does the refused harm; `git stash` is no longer offered) |
| WARN (F-C2) | "Command hygiene (WARN, does not block): this python payload may write a file the gate cannot resolve; if it writes inside a repository, use Edit/Write." |
| markers | the existing fail-open marker; `rollback not checked: <reason>` |
Order when several fire: journal, rollback, cd, mutation; `permissionDecisionReason` = the first; `additionalContext` lists all, then the WARN. A command that is refused never also gets the WARN text as its reason.
Removed in C1: `MSG_CD_PREFIX`, `MSG_CD_NON_ROOT_WARN`, `MSG_REDIRECT_STDERR`, `MSG_PYTHON_DASH_C`, `MSG_PYTHON_DASH_C_OPAQUE`, `MSG_PYTHON_DASH_C_BLOCK`, `PYC_DENY_ENABLED`, the ` 2>&1` signal's BLOCK/WARN. ` 2>&1` in PowerShell: F-C1 (decided by C0.1; until then allowed everywhere).

### C0 — experiments (builder, no code; item 2 by the operator)
owns: `C:\QAFactory\forge-repo\docs\tasks\specs\reports\fg-ctx-C0-experiments.md`
1. PowerShell tool: `$PSVersionTable.PSVersion`; `git status 2>&1; $LASTEXITCODE; $?` and `git rev-parse --verify nosuchref 2>&1; $LASTEXITCODE; $?` — does `2>&1` change `$?`/`$LASTEXITCODE` or the output objects (settles F-C1). Also: `powershell -NoProfile -Command "Set-Location docs; Get-Location"` followed by `Get-Location` in the next call — the child's location must not persist (the PowerShell cd door, t-098 F14). Outcomes: persists -> the door text drops the child shell; does not -> kept.
2. (operator) Whether the host matches a `PowerShell(git status *)` allow row in default (non-auto) mode: a prompt appeared or not (settles F12).
3. Whether `git push --dry-run` to a scratch bare remote runs `.githooks/pre-push` (E3's witness): outcomes: runs -> E3's witness is that dry run; does not -> E3's witness is a run of the hook script with a hand-made stdin line naming `refs/heads/main`.
(The former item 3, `hooklib` import cost, is dropped: F-C4 decided "own masks".)

### C1 — the gate and its audit
owns:
`C:\QAFactory\forge-repo\tools\hygiene_gate.py`
`C:\QAFactory\forge-repo\tools\test_hygiene_gate.py`
`C:\QAFactory\forge-repo\tools\permission_audit.py` (`classify_hygiene`, `HYGIENE_CLASS_LABELS`)
`C:\QAFactory\forge-repo\tools\test_permission_audit.py`
`C:\QAFactory\forge-repo\tools\test_warn_messages.py` (the HYGIENE rows and the `"HYGIENE"` count: t-098 F8 (a), certainly edited)
`C:\QAFactory\forge-repo\tools\warn_layers.json` (the HYGIENE row only: t-098 F8 (b))
`C:\QAFactory\forge-repo\tools\gitcmd.py` (module docstring caller list only: + `tools/hygiene_gate.py`)
Behaviour: everything of §4 above. `_collect_signals` keys, renamed in one commit with `permission_audit.classify_hygiene` (AR-22): `cd` (list of hits with `bare_return`, `in_subshell`), `write_targets` (list of `(form, literal target)`), `journal` (bool), `rollback_form` (dict or None), `pyc_payload` (advisory M/P/O/U, kept for measurement), `payload_uncertain` (bool). `HYGIENE_CLASS_LABELS` = "cd", "content write (literal target)", "journal write", "rollback shape", "payload uncertain" — the audit labels are SHAPES, not verdicts. The HYGIENE row of `warn_layers.json` gets its population (every Bash/PowerShell call) and the new WARN literal. The module docstring's class list is rewritten to match.
Edges (each with its invariant): non-Bash/PowerShell tool, empty or malformed stdin -> silent (the gate never blocks what it cannot read); classifier exception -> the visible fail-open marker (unchanged); one payload over `PYC_PAYLOAD_LIMIT` (20,000 chars) -> O -> WARN, never a refusal; heredoc openers over `MAX_HEREDOC_OPENERS` -> no write targets from heredoc-bearing statements (never a wider refusal); CRLF -> `\r` stripped from targets; Cyrillic and space-holding paths resolved as Unicode; a UTF-8 BOM in stdin decoded (existing reader); Windows targets compared after `os.path.normcase`; a target in a directory that does not exist yet -> the walk continues upward (a new file inside a tree is still in the tree); `rollback_form` measurement raising -> the not-checked marker, never a refusal from an exception.
Tests (layer 3: one parameterised table in `test_hygiene_gate.py` over `decide()` with a `tmp_path` tree holding a `.git` directory and a second tree for cross-tree rows; rollback rows use a real `git init` repository in `tmp_path` and one row with `gitcmd.git` patched to return rc -1):
- must pass, silent: `grep x logs/journal/dev1.jsonl 2>/dev/null` (Lead row 1) / `grep -n y logs/journal/dev1.jsonl 2>&1 | head -5` (Lead row 2) / `grep -c "echo" logs/journal/dev1.jsonl` / `ls logs/journal/dev1.jsonl 2>&1` / a python heredoc whose strings hold a journal path and a `>` / `python -c "print('a/b'.replace('/','-'))"` / `json.dump({'a':1}, sys.stdout)` / `sys.stdout.buffer.write(b'x')` / `csv.writer(sys.stdout).writerow([1])` / `open(r'<scratchpad>/f.txt','w').write('x')` / `print(open('a').read())` / `python -B -c "print(1)"` / `os.remove('docs/a.md')` / `rm docs/a.md` / `cp x docs/a.md` / `git commit -m "fix > 3 cases"` / `echo x > <scratchpad>/f.txt` / `echo x > /dev/null`, `> $null`, `> NUL` / `echo x > "$out"` / `( cd sub && make )` in Bash / `bash -c "cd x && ls"` / bare `cd <root>` / `git checkout -- docs/` with only untracked files under docs/ / `git checkout main` with no file named main / `git restore --staged f.py` / `git clean -n` / `git clean -f` with nothing untracked / `git -C <other tree> restore f.py` with the other tree clean and the cwd tree dirty;
- WARN only: `io.StringIO().write('x')` / `open(p,'w')` with `p` a variable / `exec(...)`;
- refused, mutation: `echo x > docs/a.md` / `cat > docs/a.md <<EOF` / `sed -i 's/a/b/' docs/a.md` / `perl -pi -e s/a/b/ docs/a.md` / `awk -i inplace '{print}' docs/a.md` / `tee docs/a.md` / `Set-Content docs\a.md x` / `Out-File -FilePath docs\a.md` / `[IO.File]::WriteAllText('docs\a.md','x')` / `python -c "open('docs/a.md','w').write('x')"` and the same with `python -B -c`, `python3 -c`, `py -3 -c` / `Path('docs/a.md').write_text('x')` / `json.dump({}, open('docs/a.json','w'))` / from a worktree cwd `echo x > <main clone>\docs\a.md` (cross-tree);
- refused, journal: `echo x >> logs/journal/dev1.jsonl` / `tee -a logs/journal/dev1.jsonl` / `Add-Content logs\journal\dev1.jsonl x` / `python -c "open('logs/journal/dev1.jsonl','a').write('x')"` / `sed -i s/a/b/ logs/journal/dev1.jsonl`;
- refused, cd: `cd docs && ls` / `cd <worktree root> && git grep -n x` (the t-084 shape) / `Set-Location docs; ls` / `pushd docs && ls` / `popd` / `Push-Location x` / `sl x` / `chdir x` / `eval "cd x"` / `{ cd x; }` / `if true; then cd x; fi` / `for d in a; do cd $d; done` / `ls; cd x` / `builtin cd x` / `cd` / `cd -` / `[IO.Directory]::SetCurrentDirectory('x')` / `( cd sub; ls )` in PowerShell;
- refused, rollback (dirty tracked `f.py`): `git checkout -- f.py` / `git checkout HEAD f.py` / `git checkout HEAD -- f.py` / `git checkout f.py` / `git checkout .` / `git checkout -f` / `git switch --discard-changes main` / `git restore f.py` / `git restore --worktree --staged f.py` / `git reset --hard` / `git -c core.x=y --no-pager checkout -- f.py` / `git -C <other tree> restore f.py` with the other tree dirty / `git clean -fd` with an untracked file / `git clean -xdf` with only an ignored file / `git clean -fX` with an ignored file;
- markers: rollback with `gitcmd.git` rc -1 (pass + marker) / `GIT_DIR` set in the environment (pass + marker) / classifier exception (fail-open marker);
- adversarial battery for outside input: 100 KB and 1 MB commands (time bound kept), 65 heredoc openers, nesting (a heredoc inside quotes, quotes inside a heredoc), CRLF, Cyrillic paths, UTF-8 BOM in stdin, empty and broken JSON — each a row;
- each refusal row asserts its door text is present.
`test_permission_audit.py`: one row per label; one row "audit replay of `git checkout -- f.py` performs no subprocess call" (`subprocess.run` and `gitcmd.git` patched to raise; `classify_hygiene` returns normally). `test_warn_messages.py`: the HYGIENE rows name the new constants with their imperative verbs; `WARN_TEXT_BUDGET_CHARS` is not raised (a raise is named in the verdict, axis 18).
DoD: `python -m pytest tools/test_hygiene_gate.py tools/test_permission_audit.py tools/test_warn_messages.py tools/test_gitcmd.py -q` (outside-package owns: the test files that judge them); C2's text and node P's paragraphs land in the same merge.

### C2 — the rule text (Lead-tier commit; a builder may hand the text as content)
owns: `C:\QAFactory\forge-repo\CLAUDE.md` (section "Command hygiene" only — ordered before E4, same file), `C:\QAFactory\forge-repo\.claude\skills\permission-audit\SKILL.md` (step 2 table, and one scope sentence at the head of step 3)
Text:
- the preamble "Every 'custom' form of a command is a permission request to the operator" is REMOVED (the owner's word, acceptance section) and replaced by "the deployment runs in auto mode; four behaviours are refused by `tools/hygiene_gate.py`, every other form is allowed".
- Point NUMBERS stay 1-7 (F17): 1 tests — where they run and the narrow-target rule; the permission motive is dropped; the point keeps ONE defining sentence "the canonical form of a tool = its correctly invoked form, the invocation that finds a known sample", so point 6's "positive check using the canonical form (point 1)" and the role-file and protocol pointers (critic 66, builder 61, `PROCESS/…:123`) stay valid without editing them (t-098 F4; closed choice, §9); 2 unchanged; 3 the directory refusal and its doors (the "allowlist match" text is removed); 4 the content-write refusal (the pt.4 a/b table rewritten: a named committed script legal; a read or calculation payload allowed; a payload the gate cannot resolve gets one WARN); 5 journal; 6 unchanged; 7 rollback, gate-backed for the dirty-path case — 7 (b) is rewritten: `git checkout`/`restore` of a dirty path is refused by the gate whatever the status was before the corruption, so the byte copy of 7 (a) is the only rollback road for a probe.
- A short "ready commands" list (owner's word 7): `git -C <dir> <cmd>`, `python -B <abs path>`, a Bash `( cd <dir> && … )` subshell, a PowerShell child shell for a command that truly needs a working directory, byte copy and restore (`Copy-Item`/`cp` to the scratchpad and back). `git stash push` is NOT listed (t-098 B6).
- Skill step 2: rows of `grep/cat/python -c` reading, `cd X &&`/`2>&1`, the canonical pytest form, and poll loops leave the violations column; poll loops move to "cost (rule 7)". Steps 3-5 (allowlist curation) are KEPT with one scope sentence: "steps 3-5 apply to a deployment that runs with permission prompts; in auto mode they are not a hygiene duty" (t-098 F4; closed choice).

Four questions (C, one mechanism "hygiene refusals"):
(a) cost: zero for allowed forms (fewer turns: the owner's word 2); one retry per refusal through its door; one `git status` (≤ 5 s) per rollback-shaped call; a path walk per literal write target. (b) axes: §10 table, column C. (c) detector: check 27 rewritten (§8) + `test_hygiene_gate.py`. (d) on the path: PreToolUse Bash|PowerShell hook, `permissionDecision: deny`; bypass = the named residuals (file-level copies, non-literal targets, scripts outside the repo, unclassified interpreters, unmeasurable rollback) — discipline, detector check 27 (a) and (c).

Dense WARN layers (question 2): "Command hygiene" — in scope (C1 removes every WARN of allowed classes). "Search returned nothing", WITNESS ECHO, NOTES LEN — F-C6 decided: three findings in `forge`, filed by the Lead, one node each.

## 5. D — the worktree guard without a door

§1 Goal (restated per t-098 F1): a refusal a worker meets for a compound read in its own worktree names its door. A compound read WITHOUT a directory change passes after C; a compound read WITH a `cd` prefix stays refused at any target (C1's cd class), with the door `git -C <dir>` / the Bash subshell. This narrows the brief's §D sentence ("после C составная команда чтения внутри своего дерева отказом быть не должна вовсе") — the sentence is the Lead's, not the owner's word 5; the Lead tells the owner the narrowing as "решила сама" (t-098 F1 (c)).
Invariant: no refusal a worker meets lacks "what is wrong / what is expected / the door" (P15, FR-1, FR-2).
Carrier: two candidates (F16): `hygiene_gate` class (a) — the first candidate, its `MSG_CD_PREFIX` says "invoke from the root directly, with no cd", which for a worktree is no usable door; `agent_budget` past STOP.

### D0 — experiment (wave 0)
owns: `C:\QAFactory\forge-repo\docs\tasks\specs\reports\fg-ctx-D0-guard.md`
1. (scout or builder, read-only) Find t-084's builder `worker_ref` in `logs/journal/dev1.jsonl`, open its transcript, and quote the refusal verbatim: the hook name of the "PreToolUse:Bash hook" line and its text.
2. (builder in a worktree) Run in its own worktree: `git -C <wt> grep -n test_controller_state -- tools`; `cd <wt> && git grep -n test_controller_state -- tools`; the same two through PowerShell. Record each verbatim result and its source.
Outcomes: (a) the text is `MSG_CD_PREFIX` (hygiene_gate) -> D1 is DROPPED: C1's cd row covers it (the `cd <worktree root> && git grep` row and its door); (b) the text is `agent_budget`'s STOP message -> no defect if that text names its door (the report quotes it), else D1 owns `tools/agent_budget.py` (`stop_message`) + `tools/test_agent_budget.py`, after A2; (c) another repo hook -> D1 owns that hook file + its test (named by D0), P15 text; (d) the host -> F-D1 (decided "both"): C2's ready-command line + a WARN line from `hygiene_gate` for the exact shape, after C1.
### D1 — only on outcome (b), (c) or (d)
Owns as named by D0's outcome; the file's wave follows its owner rule in §7 (never in the same wave as another node owning that file). Behaviour: the refusal text gets the P15 shape; test: one row asserting the door text. DoD: the named test file, `python -m pytest <that test file> -q`.
Four questions: (a) one line per such refusal; (b) axes: §10 table, column D (outcome (a): column C applies, no separate mechanism); (c) detector check 27 (a) counts refusals of this shape in transcripts; (d) the hook that refuses.

## 6. E — the dispatch gate (FG7-18, FG7-20) and the fast pre-push set (FG7-19)

§1 Goal: a writing dispatch carries its siblings and its designer status in form; the gate brings the data (witness tests, carriers naming each owned path) so the Lead does not search for it; the integrator runs a fast registry set before pushing `main`.
Invariants: a writing dispatch with no `siblings:` line never goes out silently; a dispatch over the designer threshold never goes out without a `designer:` line; the gate never judges whether a siblings list is sufficient (P27) and never refuses a well-formed line; a resubmission under the same task needs no designer (rule 2).

### The section extent (t-098 B3: one definition)
For the siblings form, the designer line and the item count, a section is its header tail plus its continuation lines up to (excluding) the FIRST BLANK LINE, never past the next header — the rule `_section_paths` already applies. It becomes ONE function `dispatch_manifest.section_extent(cut, sec) -> last line index`, and `_section_paths` calls it (behaviour unchanged). The wide `Section.body` of `section_cut` (to the next header) is left as it is for its existing readers.

### What `siblings:` must contain to pass (question 3)
A header line `siblings:` (or `neighbours:`/`neighbors:`; same grammar as the six keys: outside fences and quotes, case-insensitive, bullets allowed). Read over its extent:
- pass, no-siblings form: the header TAIL is `none` followed by a separator and a non-empty reason, in any of: `none -- <why>`, `none — <why>` (em dash, as manifest-skip accepts), `none. <why>`, `none (<why>)` (t-098 F11);
- pass, entries: at least one entry, where an entry is any non-empty tail text other than a bare `none`, or a continuation line that is a bullet/numbered line, holds a path candidate, or holds `axis <N>`;
- missing (refused): an empty tail with no entry line in the extent; a bare `none` (also `none.`, `none --`, `none —` with nothing after) whatever follows on the next lines (the reason must sit on the header line); a plain prose line under an empty tail that is neither a bullet nor a path nor `axis N` (a blank line ends the extent, so prose after it never counts).
Door: the line, or `manifest-skip: siblings -- <reason>`.
On a pass the gate prints (to the Lead, `additionalContext`; F-E1 decided Lead-only) for each owned path the carriers naming it that the `siblings:` extent does not mention, as a NOTE ("named by <carrier>:<line>, not in siblings:") — a report, never a refusal.

### Where the carrier list comes from (AR-13)
One data file `tools/carriers.json` (entries are repo-relative paths or globs: `docs/SIBLING_MAP.md`, `plans/builder-rules.md`, `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`, `.github/workflows/*.yml`, `ai-packages/qa-factory/scripts/tests/test-layers.json`, `.../design/state-exits.md`, `.../design/architecture.md`, `.../design/factory-rules.md`, `.../references/gate-registry.json`, `.../references/stage-joints.json`, `tools/source-split-carriers.json`, `tools/warn_layers.json`) and ONE reader `tools/carriers.py` `naming(paths, root) -> {path: [(carrier, line)]}`. A glob entry is expanded with `Path(root).glob(entry)`, sorted; a glob or a path matching nothing is named once as absent (t-098 F13). Match: the repo-relative path, and the package-relative path for package files; a basename alone is not a match. The three lists of F15 stay (F-E2 decided: queued, with a note on axis 13 by node P).

### How the designer threshold is counted from the dispatch text
`dispatch_manifest.designer_threshold(cut) -> (owns_count, items_count)`: `owns_count = len(owned_paths(cut))` (the one reader); `items_count` = unquoted lines matching `^\s*\d+[.)]\s` that lie in no extent of a section listed in `ITEM_EXCLUDED_SECTIONS` (module constant). F-E3 as decided by the Lead: the set holds every manifest section (given, owns, non-goals, handoff, edges, dod, siblings, designer). Because extents end at the first blank line, the spec body written after the header block IS counted (t-098 B3). Whether numbered acceptance criteria inside `DoD:` count is fork F-E7; the builder builds the Lead's set, and the fork's other answer is a one-entry change of the constant.
Over the threshold when either count is >= 3. Required then: `designer: <absolute path of the accepted draft>` (the path must exist — stat in dispatch_gate, like given paths), or `designer: skip -- <reason>` (`--` or `—`; passes; the note says "a dispatch_skipped(agent=designer) event is owed, rule 2"), or `designer: resubmission <task_id>` (`t-<digits>`; passes; rule 2's continuation; calibration 1 (d) reads re-badging). Door also `manifest-skip: designer -- <reason>`.
Refusal for both lines (F-E4 decided), behind the module constant `DISPATCH_FORM_REFUSES = True`.
Named limits: a dispatch whose spec lives one hop away (R11-m pointer) has `items_count` = 0 by construction (check 1 (c) reads the diff; t-098 F11); a prose line beginning "Siblings …:"/"Neighbours …:"/"Designer …:" is read as a header (the existing grammar's limit) and ends the section above it.

### E1 — the pure part
owns: `C:\QAFactory\forge-repo\tools\dispatch_manifest.py`, `C:\QAFactory\forge-repo\tools\test_dispatch_manifest.py`, `C:\QAFactory\forge-repo\tools\test_dispatch_cut.py`
Behaviour:
1. `KEY_GROUPS` + `("siblings", "siblings", r"siblings?|neighbou?rs")` and `("designer", "designer", r"designer")`.
2. `INCOMPLETE_TEMPLATE`, `SKIP_REFUSED_TEMPLATE` and `UNCHECKED_NOTE_TEMPLATE` list their items DERIVED from `KEY_GROUPS` (t-098 F11, AR-1); the FIRST sentence of each template stays byte-identical (prefix pins in `test_dispatch_gate*.py` and `hook_liveness_probe` keep holding).
3. `SECTION_STOP_RE` gains `siblings?|neighbou?rs|designer`.
4. `section_extent` added; `_section_paths` calls it.
5. `check_cut` gains the siblings form check (writing dispatches) and the designer check (over threshold), each a missing item named in the INCOMPLETE text with its form.
6. `designer_threshold` and the constants `ITEM_EXCLUDED_SECTIONS`, `DISPATCH_FORM_REFUSES` added. The module stays pure.
Edges (each with its invariant): a non-writing dispatch (scout, critic, designer with handoff only) -> neither check (unchanged `checked=False`; the gate never refuses a reading dispatch for these lines); degraded cut -> UNCHECKED note, no refusal (unchanged); `siblings:` inside a fence -> not a header -> absent; `designer:` path relative -> treated as missing (absolute required, as owns); a prose "Siblings …:" line right after the owns paths -> the owned paths above it are all kept (t-098 F11: the stop cuts what follows, never what precedes).
Readers checked in the same commit (axis 13): `owns_gate` (imports `SECTION_STOP_RE`), `handoff_gate`, `dispatch_gate`; `hop_metrics._manifest_lines` repeats the stop rule (owned by FG7-29: report, do not edit). A reader test that goes red for a reason outside E1's owns is returned as a question, not edited.
Tests: `test_dispatch_manifest.py` one table — siblings: with paths / `none -- why` / `none — why` / `none. why` / `none (why)` / bare `none` (refused) / `none` then prose on the next line (refused) / empty then a blank line then prose (refused) / empty then a plain prose line (refused) / empty then a bullet (pass) / absent (refused) / skip line / scout dispatch (unchecked) / `Siblings:` case / in a fence (refused as absent) / prose "Siblings of X:" after owns paths (owned paths kept); designer: 2 owns (no check) / 3 owns no line (refused) / 3 owns + skip with `--` / with `—` / + resubmission / + path / 3 numbered items in a spec body after the header block (refused) / 3 numbered items only inside the `DoD:` extent (no check under the Lead's set; flips with F-E7) / 3 numbered items in a pointer spec (count 0, named limit); templates: the six-plus-two items appear in all three templates. `test_dispatch_cut.py`: a stop-at-siblings row; a `section_extent` row (ends at the first blank line, never past the next header).
DoD: `python -m pytest tools/test_dispatch_manifest.py tools/test_dispatch_cut.py tools/test_owns_gate.py tools/test_handoff_gate.py tools/test_dispatch_gate.py -q` (the last three as reader checks, not owned).

### E2 — the I/O part (after E1, and after C1's merge for the two shared files)
owns:
`C:\QAFactory\forge-repo\tools\dispatch_gate.py` (`decide_full` path check for `designer:`; a new NOTE function called from `main`'s tail)
`C:\QAFactory\forge-repo\tools\test_dispatch_gate.py`
`C:\QAFactory\forge-repo\tools\carriers.py` (new)
`C:\QAFactory\forge-repo\tools\carriers.json` (new)
`C:\QAFactory\forge-repo\tools\warn_layers.json` (two new rows: SIBLINGS NOTE, WITNESS PRINT; population: writing dispatches) — after C1's merge (C1 owns the HYGIENE row in wave 1)
`C:\QAFactory\forge-repo\tools\test_warn_messages.py` (rows for the two NOTE texts: t-098 F8 (a)) — after C1's merge
`C:\QAFactory\forge-repo\tools\mechanism_gate.py` (`MECHANISM_PREFIXES` += `tools/carriers.py`, `tools/carriers.json`: imported by a hook)
`C:\QAFactory\forge-repo\tools\test_mechanism_gate.py` (only the closure row)
Behaviour: on an allowed writing dispatch, the NOTE block lists per owned path (cap 10 paths, 5 lines each, then "+N more"): witness lines and carrier lines not mentioned in the `siblings:` extent. Witness lines come from a SUBPROCESS `python -B <root>/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <paths…>` (t-098 F13: never imported into the hook process — `harness` rewrites `sys.path` and `os.environ`), stdout decoded UTF-8 with replacement, timeout = what is left of the 2 s budget; it is the same command the builder's DoD names (one road). Non-package paths print "witness: no scenario row -- name the test file in the DoD" until FG7-15 lands; then the same call covers them (temporal: the switch is FG7-15's row in `witness_for`, not a flag here).
Edges: no cwd in payload -> no printout (as the path check); the subprocess fails to start, exits non-zero or times out -> "witness: unavailable (<reason>)" or "witness: not finished (time) -- run scenario_walk.py --witness-for <path>", the dispatch goes out; `carriers.json` absent/broken -> "carriers: unavailable (<reason>)"; a carrier file or glob absent -> skipped and named once; total printout cap 60 lines; time budget 2 s for the whole block INCLUDING the subprocess start; past it "+ not finished (time)". Invariant: the NOTE never refuses and never delays the dispatch past the budget.
Tests: `test_dispatch_gate.py` rows: package path with a keep row / tools path before FG7-15 / carrier named & mentioned (no note) / named & not mentioned (note) / glob entry expanded / subprocess failure / timeout (subprocess patched) / caps / `designer:` path absent (refused) / present (pass). `test_warn_messages.py`: the two NOTE texts with their verbs. `test_mechanism_gate.py`: closure row.
DoD: `python -m pytest tools/test_dispatch_gate.py tools/test_mechanism_gate.py tools/test_warn_messages.py -q`.

### E3 — the fast pre-push set
owns:
`C:\QAFactory\forge-repo\docs\RUNBOOK.md` (§7 only)
`C:\QAFactory\forge-repo\.githooks\pre-push.next` (content for the Lead to place on `.githooks/pre-push`: enforcement-file rule, CLAUDE.md rule 2)
Behaviour (F-E5 decided: hook + list in RUNBOOK): on a push whose remote ref is `refs/heads/main`, run in order, stop at the first red, print each command and its time: `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`; `python -B ai-packages/qa-factory/scripts/tests/test_audit_rules.py`; `python -B ai-packages/qa-factory/scripts/tests/test_gate_registry.py`; `python -m pytest tools/ --collect-only -q` (t-053 class); `python -B tools/lint_ratchet.py --check`; `python -B tools/dup_ratchet.py --check`. `test_driver_layers.py` stays out (F-E6 decided). Budget: 90 s total; over it the hook prints the time and does not refuse.
Edges: push of any other ref -> nothing runs; a missing script -> named line, push refused (door: `git push --no-verify` is always the operator's, the hook says so); the existing old-history check runs first, unchanged.
Test: no new test file (TESTING.md). Witness: a DOC-DISPATCH key run for RUNBOOK §7 (keys quoted from this DoD: the six command lines above and "90 s"; script attached in full; one negative control) + one run of `pre-push.next` by the road C0.3 established.
DoD: the key run's output and the hook run's output, both verbatim.

### E4 — the rule text (Lead-tier; after C2 in the same file)
owns: `C:\QAFactory\forge-repo\CLAUDE.md` (rule 2's threshold sentence; R11-f row: the header lines gain `siblings:` and, over the threshold, `designer:`)
Rule 2 gains: "counted by `dispatch_manifest.designer_threshold`". R11-f lists the two lines. Designer rule 1 needs no edit (it points to R11-f).

Four questions (E1+E2+E4, one mechanism "dispatch gate: siblings and designer"):
(a) cost: one or two header lines per writing dispatch; a refused dispatch costs one re-send; the printout ~10-60 lines of Lead context per writing dispatch (offset by fewer `rejected` of cluster A: 6 of 14, `calibration-20261112-p2.md` 15(ii)); one subprocess per writing dispatch within 2 s. (b) axes: §10 table, column E. (c) detector: check 1 (c) (dispatches whose threshold the code counted with a `designer: skip` line and no `dispatch_skipped` event), check 15 (cluster A count), check 11 (the two new layers' density). (d) on the path: PreToolUse Task|Agent, exit 2.
E3: (a) ≤ 90 s per push to main by the integrator; (b) axes: §10 table, column E3; (c) detector check 24 (a canon-caught defect a pre-push command would have caught = a leak); (d) `.githooks/pre-push`; bypass `--no-verify`, discipline, detector check 24.

## 7. Landing order and parallelism (question 4)

Node P (Lead, applied at each merge; the ONE writer of these three files in this spec): `C:\QAFactory\forge-repo\PROCESS\WEEKLY_CALIBRATION_PROTOCOL.md`, `C:\QAFactory\forge-repo\docs\SIBLING_MAP.md`, `C:\QAFactory\forge-repo\PROJECT.md`. Its paragraphs are disjoint and land in wave order: A1's merge — check 32, check 17 (d), PROJECT.md:273 (the narrative name becomes `docs/tasks/compact-snapshots/<дата>-<ЧЧММ>-narrative.md`; "каждые ~100K" becomes "каждые ~50K"); B1+B2's merge — check 28; C1+C2's merge — check 27, check 11's hygiene population, SIBLING_MAP:529 (`tools/hygiene_gate.py | command hygiene 3, 4, 5, 7`), the axis 11 queued line (hygiene_gate's own masks and its new recognizers, F-C4), the axis 10 reader line (C1's `.git` walk) and the axis 34 row (one road for a content write in every syntax); E1's merge — check 1 (c); E2's merge — check 11's two new layers, check 15, the axis 13 note (F-E2 queued lists, the new keys, `section_extent`); E3's merge — check 24.

| Wave | Nodes (parallel inside a wave) | Owned files (no file or function owned twice in a wave) |
|---|---|---|
| 0 | A0.1 (operator/Lead), A0.2 (scout), B0, C0 (item 2 operator), D0 | one report file each, all distinct |
| 1 | A1, A2, B1 + B2 (one merge), C1, E1, E3 | A1: compact_snapshot.py, session_context.py, their tests · A2: agent_budget.py `_warns`, test_agent_budget.py · B1: builder/critic/designer role rules, test_handoff_rule_anchors.py · B2: dod_gate.py, test_dod_gate.py · C1: hygiene_gate.py, test_hygiene_gate.py, permission_audit.py, test_permission_audit.py, test_warn_messages.py, warn_layers.json (HYGIENE row), gitcmd.py (docstring) · E1: dispatch_manifest.py, test_dispatch_manifest.py, test_dispatch_cut.py · E3: RUNBOOK.md §7, pre-push.next |
| 2 | C2 (after C1, same merge as C1), E2 (after E1 and after C1's merge), D1 (only on D0 outcome b/c/d; its file decides: hygiene_gate -> after C1; agent_budget -> after A2; dispatch_gate -> after E2, i.e. wave 3) | C2: CLAUDE.md "Command hygiene", SKILL.md · E2: dispatch_gate.py, test_dispatch_gate.py, carriers.py, carriers.json, warn_layers.json (two rows), test_warn_messages.py (two rows), mechanism_gate.py, test_mechanism_gate.py |
| 3 | E4 (after C2: CLAUDE.md) | CLAUDE.md rule 2 + R11-f |
| cond. | A3 by A0.1's outcome; after F6-36 (`.claude/settings.json`) or after A2 (`agent_budget.py`) | as its row in §2 |

Readers that cross nodes without owning: B2 imports `handoff_gate._in_folder` (unchanged by any node); E1's DoD runs `test_dispatch_gate.py` (owned by E2 in wave 2 — read only in wave 1).
Concurrent writers outside this spec (t-098 F8 (d)): FG7-23 (batch-7) edits the protocol's check 19 hook snapshot and SIBLING_MAP paths, and owns the stale `mechanism_gate.py:233` `critic_snapshot` carrier line (queued there); FG7-29 owns `hop_metrics`. The Lead writes `очередь:` lines for node P vs FG7-23 and E1 vs FG7-29 in both batch files before the first wave-1 merge. FG7-18/FG7-20 nodes in batch-7 are replaced by E1/E2 (the Lead marks them).

## 8. Protocol edits (node P, same merge as the mechanism)

- Check 27 (meaning changes): from "count of four hygiene classes, cd/2>&1/python -c as violations" to "count of the four REFUSAL classes (cd, content write, journal, rollback). The SHAPES come from `permission_audit --summary` (labels from `HYGIENE_CLASS_LABELS`); the VERDICTS (refused / not refused) come from the gate's own denials in the transcripts. (a) a violation is a call of a refusal class that was NOT refused, or one of C's named residuals (file-level copies onto tree files, non-literal targets, scripts outside the repo writing into it, unclassified interpreters) found by reading the suspects; compound commands, `2>&1` in Bash, reads via `python -c`, poll loops are not counted (poll loops move to check 17 cost); (c) unsafe rollback: the gate's refusals of dirty paths counted from transcripts, plus every `rollback not checked` marker read by hand; the baseline of 12.11 (39/68/58/1 unique) is NOT comparable and a new baseline is recorded." Remove "an ad-hoc read bypassing Read/Grep" and "bypassing the canonical pytest form" from (a).
- Check 28 (meaning changes): title "Completeness of hand-backs: the report file and the short digest". (a) anchors: the new cap key; (b) failure: `gate_log` entries `handoff_missing` of `dod_gate` per window, hand-back messages over the cap counted by `handback_extract` on the window's workers (or F-B3), re-request notes as before; (c), (d) unchanged; the substring "COMPLETE final report" and the 25-line cap leave the text. First window after B records a new baseline.
- Check 32: add "every compaction is followed by the `AFTER COMPACT:` line; a `COMPACT SNAPSHOT: MISSING` line is a violation of the snapshot duty; a compaction of `trigger: auto` is checked like a manual one. Named open limits, each counted when met: a session opened in the clone's parent (no hooks load: a compaction there has no line at all); auto compactions before A0.1/A3 settle which event carries the pointer (the auto window is live since 97fae62); an `announced record not written` line."
- Check 17 (d): "a turn over 600K means a compaction was skipped" stays; add "with auto-compaction at 350K (A0.1 confirms the key is honoured), a turn over 400K is a finding of the auto window".
- Check 1 (c): "counted from the dispatch's `owns` line" becomes "counted by `dispatch_manifest.designer_threshold` on the dispatch text; a `designer: skip` line without a matching `dispatch_skipped(agent=designer)` is the violation; a pointer-spec dispatch (count 0 by construction) is judged from the diff".
- Check 11: layer list gains SIBLINGS NOTE, WITNESS PRINT (`tools/dispatch_gate.py`); "Command hygiene" gets its declared population (every Bash/PowerShell call) from C1's row of `warn_layers.json`.
- Check 19: if A3 adds a hook, the reference snapshot names it in the same commit (ordered with FG7-23's check 19 edit by the `очередь:` line).

## 9. Forks

Decided by the Lead (acceptance section; restated, not re-opened): F-A1 keep 300K; F-B1; F-B2; F-B3; F-B4; F-C1 by C0; F-C2 one WARN; F-C3 content writes only, `ci-out/` (t-103 applies it to M3 too — B5, no new decision); F-C4 own masks; F-C5 reset --hard and clean -f (t-103 adds `checkout -f` and `switch --discard-changes/-f` as rows of the same harm "discard working-tree changes", B6; the Lead may strike them); F-C6; F-D1 both; F-E1 Lead-only; F-E2 queued; F-E4 refusal; F-E5; F-E6.

Open (Lead decides; builders proceed on the recommendation where marked):

| Id | Question | Options | Recommendation | Meanwhile a builder |
|---|---|---|---|---|
| F-A2 (re-opened; quotes both) | The Lead decided "F-A2 wait for F6-36". The verdict (t-098 F6): "F6-36 (absolute hook commands) does not register hooks for a session rooted in another folder, so F-A2's 'wait for F6-36' rests on a cause A0.2 does not test" — the failed compaction ran in `C:\QAFactory`, which has no `.claude` (F19). | (a) a named open limit with detector check 32, plus the existing PROJECT.md duty (sessions open in the clone root) / (b) the operator adds the PreCompact and SessionStart hooks to the user-level settings with absolute paths (private file, the operator's call; it affects every project the operator opens) / (c) keep waiting for F6-36 | (a); (b) only if the owner wants it, after A0.2 confirms the slug | A1 proceeds (it is right on every path where hooks load) |
| F-A3 (new) | Two compactions inside `STALE_MIN` with the second PreCompact failed: how is the first snapshot kept from counting? | (a) the announced record `.claude/compact_seen.json` written by `session_context` (A1 item 5) / (b) a named limit counted by check 32 | (a): the invariant is stated in the spec; cost one small write per compaction | A1 builds (a) |
| F-C7 (new) | Scope of "a working tree" for the content-write refusal | (a) any git working tree (the `.git` walk, no subprocess) / (b) only this clone and its worktrees (`git rev-parse --git-common-dir` equality, a subprocess per target) | (a): one rule, the door (Edit/Write) works in every tree, no subprocess; a stand copy written by redirect is the same harm to its own review | C1 on (a) |
| F-C8 (new) | The stash family (t-098 B6: worktrees share the main clone's stash ref; `git stash push` removes another session's changes from its tree) | (a) `git stash`/`stash push` with a dirty scope join the rollback class; `stash drop`/`clear` a named residual / (b) all stash forms a named residual / (c) (a) plus `drop`/`clear` refused unconditionally | (a) | C1 without stash; the addition is one data row |
| F-E7 (new; quotes both) | The Lead decided "F-E3 owns + numbered items outside the sections". The verdict (t-098 B3): "CLAUDE.md rule 11 puts 'named acceptance criteria' in the DoD, and rule 2 counts 'numbered items' of the spec. As written, excluding the DoD exempts exactly the items rule 2 means." | (a) the Lead's set as decided: every manifest section excluded, DoD included / (b) `dod` (and `edges`) leave `ITEM_EXCLUDED_SECTIONS`: numbered criteria in the DoD count; given/owns/handoff/non-goals lists still do not | (b): rule 2's "numbered items" are spec items, and acceptance criteria are spec items; file lists are counted by the owns half already | E1 on (a) (the acceptance section wins until the Lead decides); (b) is one constant entry |

Closed by the designer (no design weight; each visible for the Lead to strike):
- STALE_MIN 10 min; printout caps (10 paths x 5 lines, 60 total, 2 s); door and WARN texts ≤ 350 characters (was 300: the reading-role and scratch doors need the room); order of hygiene classes (journal, rollback, cd, mutation); the `designer: resubmission <task_id>` third form; report file names of A0.1/A0.2/B0/C0/D0.
- `open(p,'w')` with `p` a variable -> UNCERTAIN (one WARN), not a refusal: follows from §4's error direction and the Lead's F-C2 (t-098 B1 asked the spec to pick one).
- The gate-grade STDIO class also covers `json.dump`/`csv.writer`/`.write` on `sys.stdout`/`sys.stderr` and their `.buffer` (silent instead of WARN): the target is provably not a file; the advisory lists stay untouched.
- The snapshot header form (an HTML comment on line 1); the narrative name `<date>-<HHMM>-narrative.md`; the announced record path `.claude/compact_seen.json`, last 200 names.
- The PowerShell cd door is a child shell `powershell -NoProfile -Command`; C0.1 verifies it.
- `scenario_walk` runs as a subprocess, not an import (t-098 F13 offered both).
- B2 imports `handoff_gate._in_folder` rather than moving it (moving it into `dispatch_manifest` would put B2 and E1 on one file in one wave).
- Clean's status uses `--untracked-files=normal` and drops directory entries without `-d` (no false refusal of `git clean -f` for files git would not delete).
- CLAUDE.md hygiene point 1 keeps one sentence defining "the canonical (correctly invoked) form", so point 6, critic 66/74, builder 61 and `PROCESS/…:123` stay valid without edits (t-098 F4 offered this or a point-6 rewrite). The Lead should check it does not read as the removed permission rule; it carries the correctness motive only.
- SKILL.md steps 3-5 are kept with a one-line scope (prompt-mode deployments), not deleted (t-098 F4: "kept or queued").
- The rollback status runs through `tools/gitcmd.git` (axis 10's one runner).

For the Lead (not a fork, the Lead's own sentence): the narrowing of the brief's §D sentence (§5) is told to the owner as "решила сама".

## 10. Axis enumeration for every mechanism (rule 10 (b); t-098 F9)

Columns: A = post-compaction pointer (A1, A2, A3); B = short hand-back (B1, B2); C = hygiene refusals (C1, C2; also D on D0 outcome (a)); D = the guard's door (D1 on outcome (b)/(c)/(d)); E = dispatch gate (E1, E2, E4); E3 = pre-push set. A commit message copies ITS column as one line per axis in the form `axis N (<key>): <verdict> <why>` — 36 lines per mechanism, never a range (`tools/mechanism_gate.py` counts each axis literally).

| Axis | A | B | C | D | E | E3 |
|---|---|---|---|---|---|---|
| axis 1 (Policy <-> role files <-> journal) | covered: PROJECT.md:273 changed by node P in A1's merge; no role file changes | covered: three role files and the dod_gate text in one merge | covered: CLAUDE.md hygiene in C2; point numbers kept, point 1 keeps the canonical-form definition, so role-file pointers stay valid | covered: the door text lives in the refusing file; the ready-command line is in C2 | covered: CLAUDE.md rule 2 and R11-f in E4; designer rule 1 points to R11-f | n/a: RUNBOOK §7 only, no policy text |
| axis 2 (Per-tier exam instruments) | n/a: no exam instrument read or written | n/a: no exam instrument read or written | n/a: no exam instrument read or written | n/a: no exam instrument read or written | n/a: no exam instrument read or written | n/a: no exam instrument read or written |
| axis 3 (package <-> release copy <-> plugin) | n/a: no package path written | n/a: no package path written | n/a: no package path written | n/a: no package path written | n/a: package files read (subprocess, carriers), none written | covered: runs selftest --limits --lang against the package, writes nothing |
| axis 4 (factory rules <-> debt <-> backlog <-> principles) | n/a: no FR text changed | n/a: no FR text changed | n/a: no FR text changed | n/a: no FR text changed | n/a: no FR text changed | n/a: no FR text changed |
| axis 5 (stage twins inside the package) | n/a: no package stage touched | n/a: no package stage touched | n/a: no package stage touched | n/a: no package stage touched | n/a: no package stage touched | n/a: no package stage touched |
| axis 6 (measurement tools <-> package) | n/a: no measurer of the package changed | n/a: handback_extract read, not changed | n/a: permission_audit measures forge sessions, not the package | n/a: no measurer | n/a: no measurer | n/a: no measurer |
| axis 7 (per-test identity) | n/a: no test identity read | n/a: no test identity read | n/a: no test identity read | n/a: no test identity read | n/a: witness lines printed as scenario_walk prints them | n/a: no test identity read |
| axis 8 (where the story is on disk) | n/a: no story path | n/a: no story path | n/a: no story path | n/a: no story path | n/a: no story path | n/a: no story path |
| axis 9 ("is this a test file") | n/a: no test-file predicate | n/a: no test-file predicate | n/a: no test-file predicate | n/a: no test-file predicate | n/a: no test-file predicate | covered: the collect-only row is the "is this a test file" check, unchanged |
| axis 10 (git-top readers) | n/a: compact_snapshot keeps gitcmd, no new top reader | n/a: no git read | covered: the `.git` ancestor walk of a write target is a new top reader, named on the axis by node P (the one helper is queued, B-437); rollback status through gitcmd.git; GIT_DIR/GIT_WORK_TREE -> not-checked marker | n/a: no git reader unless D0 names one, then D1 re-checks this line | n/a: dispatch_gate's own git wrapper untouched | n/a: runs no git reader |
| axis 11 (shell-command recognizers) | n/a: reads no command words | n/a: reads no command words | queued: own masks kept (F-C4 decided); the new recognizers (statement starts, write targets, rollback forms) go on the axis 11 queued list with the B-434 twins, node P, same merge | n/a: a text change reads no new words | n/a: a dispatch is not a shell command | n/a: reads no command words |
| axis 12 (carriers of the work plan) | covered: `compact_snapshot.backlog_rows` untouched | n/a: no plan carrier | n/a: no plan carrier | n/a: no plan carrier | n/a: FG7-18/20 marked by the Lead, no parser change | n/a: no plan carrier |
| axis 13 (the dispatch text: one cut) | n/a: no dispatch read | covered: handoff path via `dispatch_manifest.handoff_paths`, folder via `handoff_gate._in_folder` | n/a: no dispatch read | n/a: no dispatch read | covered: new keys, SECTION_STOP_RE, `section_extent` used by `_section_paths`; readers owns_gate/handoff_gate/dispatch_gate in E1's DoD; hop_metrics queued to FG7-29 | n/a: no dispatch read |
| axis 14 (readers of agent transcripts) | n/a: A3's fallback reads agent_budget's sidecar, not a transcript | covered: worker file through `transcripts` only; error direction stated | n/a: permission_audit's transcript reads unchanged | n/a: D1 reads no transcript (D0 reads one by hand) | n/a: no transcript read | n/a: no transcript read |
| axis 15 (console stream setup) | n/a: emit and stdout setup unchanged | n/a: stderr setup unchanged | n/a: `_reconfigure_stdout_utf8` unchanged | n/a: unchanged | n/a: the hook's stream setup unchanged; the subprocess output is decoded UTF-8 with replacement | n/a: shell hook, no Python stream setup |
| axis 16 (package JSON reader) | n/a: no package JSON read | n/a: no package JSON read | n/a: no package JSON read | n/a: no package JSON read | n/a: test-layers.json read by scenario_walk itself in its own process | n/a: no package JSON read |
| axis 17 (detector verdict shape) | n/a: no package detector | n/a: no package detector | n/a: no package detector | n/a: no package detector | n/a: no package detector | n/a: no package detector |
| axis 18 (shrink-only ratchets) | n/a: no ratchet touched | n/a: no ratchet touched | covered: `WARN_TEXT_BUDGET_CHARS` of test_warn_messages not raised; a raise would be named in the verdict | n/a: no ratchet touched | covered: warn_layers rows are a registry, not a ratchet; no raise | covered: lint and dup ratchets run with --check, none raised |
| axis 19 (role file `tools:` line reader) | n/a: package hooklib axis, not touched | n/a: role files' `tools:` lines not changed | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis |
| axis 20 (host receipt names) | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis |
| axis 21 (package markdown tables) | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis |
| axis 22 (a host's return form) | n/a: package axis | n/a: package axis (forge hand-back form, not host-report-forms.json) | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis |
| axis 23 (fields of a tests[] row) | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis |
| axis 24 (the record of an execution) | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis |
| axis 25 (freshness of a run) | n/a: package axis (snapshot freshness is forge, own rule in A1) | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis |
| axis 26 (stand not confirmed) | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis |
| axis 27 (profile of a test row) | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis |
| axis 28 (render site of the row form) | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis |
| axis 29 (append-only jsonl writers) | n/a: the announced record is a JSON list, not a jsonl carrier | n/a: no jsonl appended (dod_track JSON unchanged in kind) | n/a: no jsonl appender added | n/a: none | n/a: none | n/a: none |
| axis 30 (commands of a profile) | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis |
| axis 31 (role carriers: one owner per aspect) | covered: REMINDER owns "what to read after compact"; PROJECT.md:273 renamed in the same merge (node P) | covered: role files own the form; critic-diff-brief and builder-rules 11 point; RESTATED list updated | covered: CLAUDE.md owns the rule; SKILL.md and SIBLING_MAP:529 point (node P) | covered: the refusal text lives in the gate only | covered: CLAUDE.md owns the header list; templates derived from KEY_GROUPS | covered: RUNBOOK §7 owns the list; the hook points to it |
| axis 32 (where judgment lives: census) | n/a: forge check; owner named in §1 (data) | n/a: forge check; owner named in §1 (data) | n/a: forge check; owners named in §1 (data) | n/a: forge check | n/a: forge check; sufficiency stays with critic/Lead (§1) | n/a: forge check |
| axis 33 (which dispatch am I) | n/a: package `dispatch_identity` not used | n/a: B2 picks the worker's dispatch through handoff_gate's forge route, not the package reader | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis |
| axis 34 (one road for one action) | covered: one rule for manual and auto compaction; identity by content, never by trigger or name | covered: one rule for builder, critic, designer (F-B2 decided) | covered: one road for a content write in every syntax; file-level operations pass in every syntax (B5); main session and workers alike; shell differences only as capability rows | covered: one door shape for every refusal | covered: one gate for every writing dispatch, any role | covered: one set for every push to main |
| axis 35 (sides of a story) | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis |
| axis 36 (row written against a substitute) | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis | n/a: package axis |

## 11. Not verified by this draft

- Whether the host honours `autoCompactWindow`, whether auto compaction fires PreCompact and SessionStart `source=compact`, whether `PostCompact` exists, whether `session_id` is stable across a compaction (A0.1).
- The slug of session 646c4aac (A0.2; p4:64 records "C--QAFactory", not re-read by t-103).
- Whether worker transcripts carry the hand-back text (B0); the "2-4K tokens" size (estimate).
- Which hook refused t-084's compound `git grep` (D0); hygiene_gate class (a) is the strong candidate, not proof.
- `2>&1` effect in the PowerShell tool and the child-shell door (C0.1); whether `PowerShell(...)` allow rows match (C0.2); whether `git push --dry-run` runs the pre-push hook (C0.3).
- The time of a `scenario_walk.py --witness-for` subprocess inside the 2 s budget (E2 bounds it by a timeout; not measured).
- Whether the PreToolUse payload always carries `cwd` (C1 falls back to the hook process's cwd; `handoff_gate` already reads the field).
- The operator's user-level settings (private).

## 12. Reading trail

t-095 (draft): the brief (1-73); `calibration-20261112.md` (1-89); p1 215-236; p3 160-249; p4 grep of check 32 (19, 49-69, 106); findings `20261112-{kontekst-lida..., spec-dispatchera..., porog-dizajnera..., suzhennyj-svidetel..., net-razdela-permissions..., nositel-perezhivaet...}.md`; batch-7 grep 15, 38-53, 61; `.claude/settings.json` 1-174; `tools/hygiene_gate.py` 1-1398; `tools/permission_audit.py` 1-130, 170-279, 437-586; `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` 18-75, 192-238, 477-503, 533-592, 777-862, 933-944; `tools/session_context.py` grep + 2215-2334; `tools/compact_snapshot.py` 1-80 + grep; `tools/dispatch_manifest.py` 1-135, 605-698 + grep of defs; `tools/dispatch_gate.py` 1-60, 700-799, 1900-2074 + grep; `scenario_walk.py` 833-932; `docs/TESTING.md` 1-148; `tools/test_handoff_rule_anchors.py` 1-172; `.claude/agents/builder.md` 64-84; `tools/dod_gate.py` 1-145 + grep; `tools/handback_extract.py` 1-50; `tools/agent_budget.py` 1-60, 262-291 + grep; `docs/SIBLING_MAP.md` 1-45, headings, 266-342; `tools/test_quarantine.py` grep + 1320-1346; `tools/warn_layers.json` 1-20 + grep; `docs/RUNBOOK.md` headings + 86-128; `.githooks/pre-push`; `tools/test_workflows.py` 1-30; SKILL.md grep; `tools/mechanism_gate.py` 211-265; `docs/tasks/factory-fixes.md` grep; onboarding-forge batch-1 1-12 + F6-36 row.
t-103 (this revision), read in the carrier: the verdict `reviews/t-098-fg-context-hygiene-plan.md` 1-525 (whole); the brief 1-73; `tools/hygiene_gate.py` 370-679, 750-1264 + grep of defs and of `CD_PREFIX_START_RE`/`PY_DASH_C_RE`/`PY_HEREDOC_RE`/`JOURNAL_JSONL_UNDER_LOGS_RE`; `tools/permission_audit.py` 440-489; `tools/dispatch_manifest.py` 60-309, 530-599; `tools/compact_snapshot.py` 530-708 + grep; `tools/session_context.py` 2205-2320 + grep (`session_id`, `compact_snapshot_line`, `STALE_MIN`: absent, a new constant); `tools/agent_budget.py` grep of defs and constants; `tools/test_warn_messages.py` grep (MSG_, dispatch_gate, hygiene); `tools/warn_layers.json` 190-219; `tools/dod_gate.py` 195-234, 395-439 + grep; `tools/dod_track.py` grep (`file_path`, `agent_id`); `tools/handoff_gate.py` 84-158 + grep; `tools/gitcmd.py` 1-55; `tools/mechanism_gate.py` grep (axis lines); `docs/SIBLING_MAP.md` axis headings (36 axes), 248-325, grep `hygiene` (row at :529, the verdict's :528 drifted by one); `.claude/skills/permission-audit/SKILL.md` 45-94; grep `canonical form|command hygiene|hygiene point` (-i) over role files, PROCESS, SKILL, builder-rules; `PROJECT.md` grep `compact-snapshots` (:273); `.claude/settings.json` 1-45; `docs/tasks/specs/reports/t-084-td11c-NC.md` 76-81; Glob `docs/tasks/compact-snapshots/2026-11-12*` (8 files, `1210-manual.md` among them); Glob `C:\QAFactory\.claude` (does not exist) with the positive control Glob `settings.json` under `C:\QAFactory\forge-repo\.claude` (found, plus 19 worktree copies under `.claude/worktrees/agent-*/`); grep of `DISPATCH INCOMPLETE|MANIFEST-SKIP REFUSED|MANIFEST-UNCHECKED` over `tools/` (8 files: the prefix-pin readers of E1 item 2).
Noticed analogs (reported, not widened): `mechanism_gate.py:233` lists `tools/critic_snapshot.py` as a hook `settings.json` does not carry (queued to FG7-23, §7); PROJECT.md:273 "~100K" vs `MAIN_STEP` 50K (folded into node P); `hygiene_gate` is outside `gitcmd`'s caller list today, as the other enforcement-chain wrappers wait for F2-11 — C1 joining it is consistent with axis 10's closing rule, not a widening.

## 13. Revision after t-098

| Finding | Where resolved, or the fork it became |
|---|---|
| B1 (payload classifier as a gate refuses reads; reading roles have no door) | §4 "Error direction" (advisory lists untouched, new `_GATE_WRITE_FORMS`), "Class mutation" M3 (certain subset (i)-(iii) with resolved literal targets; STDIO and FILE-LEVEL silent; the rest UNCERTAIN -> one WARN), the mutation door text (scratchpad script restored, "A reading role: Edit/Write your handoff file"); `open(p,'w')` choice closed in §9; C1 must-pass rows |
| B2 (journal class cross-matches; the Lead's two rows) | §4 "Class journal": a write whose literal target is a journal file, one classifier with a target filter; old pair detector removed; C1 rows: both Lead rows, `grep -c "echo"`, `ls … 2>&1`, the heredoc read |
| B3 (section extents; `siblings:` grammar; DoD items) | §6 "The section extent" (`section_extent`, first blank line, one definition), the siblings grammar (reason on the header line, entries defined, prose cases refused), the threshold count over bounded extents; DoD question -> fork F-E7 (quotes the Lead's F-E3 and the verdict); E1 test rows |
| B4 (rollback I/O in the audit's replay function) | §4 "Where each signal is computed": `_collect_signals` pure, `rollback_form` = form only, every filesystem/git step in `decide()`; check 27 reads verdicts from transcripts (§8); test row "audit replay performs no subprocess call" |
| B5 (one road: `rm` vs `os.remove`, redirect vs `open()` to scratch) | §4 M3: FILE-LEVEL calls silent as `rm`/`mv` are (F-C3 in every syntax); one target resolution for M1-M3 (literal, from the target's own path); rows `os.remove('docs/a.md')` pass and `open('<scratchpad>/f','w')` pass; axis 34 line in §10 |
| B6 (rollback: wrong repository, shapes, untracked, the door) | §4 "Class rollback": `-C` chain composed and the status run there, `-c`/`--no-pager` skipped, the shape table (rev + path without `--`, single argument by stat, `checkout -f`, `switch --discard-changes`, `reset --hard`, clean flag clusters with `-x`/`-X`), `--untracked-files=no` for checkout/restore/reset/switch, untracked/ignored views for clean; door without `git stash`; stash family -> fork F-C8 |
| F1 (the guard is likely hygiene_gate class (a)) | F16 rewritten; §5 goal restated ("names its door"; the narrowing told to the owner by the Lead); D0 reads t-084's transcript with hygiene_gate as first candidate; D1 dropped on outcome (a) |
| F2 (`pushd`, `eval`, cd after `then`/`do`/`{`) | §4 "The statement walk" and "Class cd" (verbs and starts listed; named limits for functions and `source`); C1 rows |
| F3 (mutation residuals) | §4 M1 (.NET writes, root from the target's path), M2 (`awk -i inplace`), M3 (`python -B -c`, `python3`, `py` regex widening), invariant 2 restated, residuals named; check 27 (a) names them (§8) |
| F4 (C2 residue) | C2: point 1 keeps the canonical-form definition (point 6, critic 66, builder 61, PROCESS:123 stay valid; closed choice §9); SIBLING_MAP:529 by node P in C's merge; SKILL steps 3-5 kept with a scope line (C2 owns it) |
| F5 (snapshot identity by name) | A1 items 1-5: identity by a content header with session and trigger, `snapshot_identity` the one reader; narratives renamed `-narrative.md` with PROJECT.md:273 (node P); `-N` suffix and free `--source` covered; two compactions inside `STALE_MIN` -> announced record (fork F-A3) |
| F6 (the parent-folder session loads no hooks) | §2 named open limit; A0.2 reads the slug of 646c4aac; A3's agent_budget context-drop fallback; F-A2 re-opened as a fork quoting the Lead's decision and the verdict |
| F7 (auto window live before A3 and F6-36) | §2 second named limit; check 32 text (§8) |
| F8 (hidden overlaps) | (a) test_warn_messages owned by C1 (wave 1) and by E2 for its two rows (wave 2, after C1's merge), in E2's DoD; (b) the warn_layers HYGIENE row owned by C1, E2's rows after C1's merge; (c) B1 + B2 one merge with check 28; (d) FG7-23/FG7-29 named as concurrent writers, `очередь:` lines by the Lead (§7) |
| F9 (axis ranges) | §10: one table, 36 rows x 6 mechanisms, a verdict and a reason per cell, no ranges; the commit-message form stated |
| F10 (A0.1 not a builder task) | A0.1 routed to the operator or the Lead, procedure and cost stated (§2) |
| F11 (E1 grammar edges) | §6: em dash, `none.`, `none (…)`; the prose-header row keeps owned paths; the three templates derived from `KEY_GROUPS`; the pointer-spec limit named (check 1 (c) reads the diff) |
| F12 (B2 edges) | B2 items 2-4: normcase/realpath and trailing-segment match (worktree copies), `HANDOFF_DIRS` filter via `handoff_gate._in_folder`, the once-key `handoff_missing_blocked`, the check before "no-edits" and the save on block; test rows |
| F13 (E2 import side effects) | E2: a subprocess, never an import; its start counted inside the 2 s budget; glob expansion in `carriers.json` stated |
| F14 (PowerShell door) | §4 cd door for PowerShell (child shell, `--root`, `git -C`, `python -B`); C0.1 verifies the child shell does not move the session's location |
