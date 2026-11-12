# Spec (DRAFT, designer t-095): the Lead's context after a compaction, short hand-backs, command hygiene cut to its refusals, the worktree guard's door, the dispatch gate

Status: draft for Lead acceptance, then critic-on-plan (forks + mechanism change; CLAUDE.md rule 3). Feature F19.
Source: `docs/tasks/specs/fg-context-and-hygiene-lead-brief.md` (owner's words 1-7 of 12.11.2026, directions A-E);
calibration `docs/tasks/specs/reports/calibration-20261112.md` + parts p1-p4; nodes FG7-18, FG7-19, FG7-20, FG7-24, FG7-25
(`plans/piles/forge/batch-7-vhodyashchie-4.md:41-48`).

## Lead acceptance of the draft (12.11.2026, dev1) — read before §0

Accepted as the plan for critic-on-plan. Corrections and decisions of the Lead; where a line here differs from the text below, this line wins.

- **F4 is wrong.** `autoCompactWindow: 350000` IS in `.claude/settings.json` (line 3, commit 97fae62; read by the Lead after the draft). A0.3 is dropped; A0.1 still measures whether the host honours the key.
- **The owner's word of 12.11 after the brief:** "тогда нужно убрать это правило … надо и из правил убрать" — the rule "every custom form is a permission request" and its point 3 (`cd … &&`, ` 2>&1` as allowlist breakers) are REMOVED from the rule text, not only silenced in the gate. C2 does exactly that; C2 is not optional and lands in the same merge as C1. Role files, the skill and check 27 lose the same motive in that merge.
- **Forks, all decided by the Lead on the recommendation** (technical; the owner may cancel any): F-A1 keep 300K; F-A2 wait for F6-36; F-B1 at most 2,000 characters and 3 + N lines; F-B2 builder, critic, designer; F-B3 file check only, the reader queued; F-B4 keep the anchor test, queue the registry; F-C1 by C0's measurement (alters `$?` only -> allow everywhere); F-C2 one short WARN; F-C3 content writes only, ignore row `ci-out/`; F-C4 own masks, convergence queued on axis 11; F-C5 the rollback class includes `git reset --hard` and `git clean -f`; F-C6 three findings in `forge`; F-D1 both; F-E1 Lead-only; F-E2 queued; F-E3 owns + numbered items outside the sections; F-E4 refusal with a door (the owner's words 4 and 6); F-E5 hook + RUNBOOK; F-E6 `test_driver_layers.py` stays out.
- **Two false refusals met by the Lead the same hour** (evidence for C1's rows): a read-only `grep … logs/journal/*.jsonl … 2>/dev/null` refused as a journal write (the F10 class, with `2>/dev/null`), and `grep … 2>&1 | head` refused for the trailing-redirect class. Both are rows of C1's table and must pass.

## 0. Facts this draft rests on (read in the carrier; see "Reading trail")

| # | Fact | Carrier |
|---|---|---|
| F1 | SessionStart with `source == "compact"` ALREADY appends `COMPACT SNAPSHOT: <newest *.md> (<age> min old)` after the boot lines (which already hold the OPEN DISPATCH lines). | `tools/session_context.py:2218-2241`, `:2309-2312`, `:544-569` |
| F2 | That line was seen after 5 of 6 compactions in the window; all 6 were `trigger: manual`; no auto-compaction was observed. The failed one ran with cwd `C:\QAFactory` (the clone's parent). | `calibration-20261112-p4.md:19`, `:53-64` |
| F3 | Every hook command is cwd-relative (`python tools/<x>.py`). The cwd fix is node F6-36, batch `onboarding-forge/1`, status `ожидает`. | `.claude/settings.json:9-113`; `plans/piles/onboarding-forge/batch-1-onboarding-roles-forge.md:3,52` |
| F4 | `autoCompactWindow` is NOT in `.claude/settings.json` (the whole file read; keys: model, hooks, enabledPlugins, extraKnownMarketplaces, permissions). The brief says the Lead set it. `git status` at dispatch shows settings.json unmodified. | `.claude/settings.json:1-174`; brief:29 |
| F5 | `compact_snapshot.REMINDER` sends the reader to "the newest `## State at` section of docs/tasks/factory-fixes.md"; that section is dated 02.10. PROJECT.md names `docs/tasks/compact-snapshots/<date>-manual.md` as the narrative carrier. | `tools/compact_snapshot.py:73-78`; `docs/tasks/factory-fixes.md:80`; PROJECT.md «Сжатие контекста» |
| F6 | `agent_budget.py` ALREADY warns the main session at 300K and every +50K (FG7-25 item 2 proposes what exists); its text does not name the snapshot duty. | `tools/agent_budget.py:46-47,111-112,266-279` |
| F7 | The 25-line digest rule ALREADY exists in builder 7, critic 16, designer 5, pinned by `tools/test_handoff_rule_anchors.py`; builder's digest carries "the closing lines of the witness". `dod_gate.BLOCK_MESSAGE` asks for "a COMPLETE final report all over again". | `.claude/agents/builder.md:64-84`; `tools/test_handoff_rule_anchors.py:23-44`; `tools/dod_gate.py:119-126` |
| F8 | Final-message length was NOT measured: p3 says sampled worker transcripts end in a `tool_result` and the main transcript holds an 8-line launch ack. `handback_extract.py` reads the last `SubagentHandback` tool_use from the worker transcript and prints `lines=`. The two claims disagree; "2-4K tokens today" (brief:36) is an estimate. | `calibration-20261112-p3.md:223`; `tools/handback_extract.py:14-32` |
| F9 | `hygiene_gate`: cd/Set-Location BLOCKs only into this repo's root at command start, else WARN; `Push-Location` is not recognised; ` 2>&1` BLOCKs (certain) in Bash and PowerShell alike; `python -c` WARNs, never blocks (`PYC_DENY_ENABLED = False`), a payload classifier M/P/O/U exists and silences P; journal write BLOCKs. No class for `git checkout --`/`git restore`, `sed -i` on a non-journal file, or a redirect into a repo file. | `tools/hygiene_gate.py:24-50,272,678,750-1090,1144-1214` |
| F10 | The journal class has a measured false positive: a read-only `ls <journal> 2>&1` counts as a write because `>` of `2>&1` passes `_has_write_form`. | `calibration-20261112-p3.md:202`; `tools/hygiene_gate.py:506-521` |
| F11 | `permission_audit.classify_hygiene` reads `_collect_signals` keys `redirect`, `cd`, `pyc`, `journal` by name; its labels are the four old classes. | `tools/permission_audit.py:170-179,454-479` |
| F12 | `permissions.allow` now exists (commit 7214fe4) with `Bash(...)` and `PowerShell(...)` rows; whether the host matches the `PowerShell(...)` form is not measured. | `.claude/settings.json:133-173` |
| F13 | `dispatch_manifest.py` is a PURE module (no I/O). Manifest items are a closed tuple `KEY_GROUPS`; `manifest-skip` items are the same six; `SECTION_STOP_RE` is imported by owns_gate/dispatch_gate. A refusal is exit 2 from `dispatch_gate.main`. A PreToolUse hook's `additionalContext` reaches the coordinator, NOT the worker's prompt. | `tools/dispatch_manifest.py:1-60,97-128,630-686`; `tools/dispatch_gate.py:1905-1917,1973-1976` |
| F14 | `scenario_walk.witness_for` covers package paths only; for any other path it prints "no scenario or keep row covers X: run the whole scenario layer" plus every scenario file. FG7-15 (pending) extends it to `tools/`. | `ai-packages/qa-factory/scripts/tests/scenario_walk.py:887-922`; batch-7:38 |
| F15 | Three hand-kept carrier lists exist already: `test_quarantine.FORGE_CARRIERS` (`:51`), `+ PACKAGE_PROSE` in `_prose_mentions` (`:1337-1346`), and a longer list at `:2194-2195`. | `tools/test_quarantine.py` |
| F16 | The "worktree guard" of t-084: its only carrier in the repo is one sentence of the report. No PreToolUse hook in `.claude/settings.json` or in `tools/claude-mods/*/hooks` refuses compound git. | `docs/tasks/specs/reports/t-084-td11c-NC.md:79`; search trail §9 |
| F17 | Role files cite "command hygiene point 6" by number (designer 3, critic, builder). | `.claude/agents/designer.md:43`, `critic.md:66,74`, `builder.md:61` |
| F18 | `CLAUDE.md`, `PROCESS/`, `.claude/agents/`, `.claude/skills/`, `.githooks/`, `.claude/settings.json` and every hook file named here are mechanism paths (axis block + `tier:` line; tier at least the lead binding). | `tools/mechanism_gate.py:211-265` |

## 1. Scope, invariants, architecture

Non-goals (dispatch): no factory package behaviour; no session relay; no change to which model plays which role; no fork decided.

ARCHITECTURE: no node owns a path under `ai-packages/qa-factory/`. E2 READS `scenario_walk.witness_for` and package carrier files; C may READ `scripts/hooklib.py` (fork F-C4). So the package commit line is not owed; a node that ends up writing a package path is a spec defect returned to the Lead. AR-n named for the forge analogues the critic should hold the nodes to: AR-13 (one reader of a fact: the carrier list, the owned paths, the hygiene signals), AR-9/FR-1/FR-2 (every refusal names what it expected and a door), AR-29/P27 (code checks form and data, the Lead/critic judge sufficiency), AR-22 (producer and reader in one commit: `_collect_signals` <-> `permission_audit`), P31 (one road: main session and workers, Bash and PowerShell get one rule unless a data row says otherwise).

Owner of every check added or altered (P27, AR-29; census class in the forge sense: "data check" = code over shape/presence, never a verdict on meaning):

| Check | Serves | Class |
|---|---|---|
| A: post-compaction line, stale-snapshot detection | data (code: file presence, age) | data |
| B: handoff file exists and was written by this worker | data | data; the report's completeness = judgment of the Lead at acceptance |
| C: refusal of cd / ad-hoc mutation / journal bypass / dirty rollback | data (the command's form, the paths' git state) | data; "was the edit worth it" stays with the reviewer |
| E: `siblings:` line present and well-formed; designer threshold counted; carriers and witnesses printed | data | data; whether the siblings list is SUFFICIENT = critic/Lead (judgment) |
| E3: pre-push fast set | data (exit codes) | data |

## 2. A — the Lead's context after a compaction (FG7-25)

§1 Goal: after any compaction the Lead's first context names the snapshot to read, the open dispatches, and one instruction "read the snapshot before your next action"; a compaction whose PreCompact snapshot is missing is visible at that moment, not a week later.
Invariant: a compaction never leaves the Lead without a pointer to the newest facts, and a missing/old snapshot is never shown as a fresh one (a snapshot measured before an earlier compaction never counts as this compaction's).

### A0 — experiments (builder, no code; one report)
owns: `C:\QAFactory\forge-repo\docs\tasks\specs\reports\fg-ctx-A0-experiments.md`
1. Auto-compaction (settles brief:27 and F2): in a throwaway session opened at a worktree root, an untracked `.claude/settings.local.json` with a small `autoCompactWindow` (if the host ignores the key, that is the finding); drive it past the window. Record: was `docs/tasks/compact-snapshots/*-auto.md` written (PreCompact fired with trigger auto), and did the post-compaction context carry the `COMPACT SNAPSHOT:` line (SessionStart `source=compact`)? Also whether a `PostCompact` event exists (a hook entry with that name in the local settings echoing to a file).
2. FG7-25 item 1 (cwd hypothesis): run the PreCompact command line verbatim with cwd = the clone's parent, on a copy of a hook input; record output and exit code.
3. Whether the Lead's `autoCompactWindow: 350000` is set anywhere (F4): `.claude/settings*.json` of the repo and the operator's user settings ARE NOT read by the builder (private); the report says only what the repo carries, and the Lead checks the user file himself.
DoD: the report quotes each command and its verbatim output. Witness: the report file (no test). Edges: the host refuses the key -> state it, try nothing else; the parent-folder run finds the script -> hypothesis refuted, named.

### A1 — the post-compaction lines
owns:
`C:\QAFactory\forge-repo\tools\session_context.py` (`compact_snapshot_line` and the `source == "compact"` branch of `main` only)
`C:\QAFactory\forge-repo\tools\compact_snapshot.py` (`REMINDER` only)
`C:\QAFactory\forge-repo\tools\test_session_context.py`
`C:\QAFactory\forge-repo\tools\test_compact_snapshot.py`
Behaviour:
1. On `source == "compact"` the appended block is three lines, after the boot lines (survives `MAX_LINES`):
   `COMPACT SNAPSHOT: <hook snapshot path> (<age> min old)`; `COMPACT NARRATIVE: <newest hand-written snapshot> (<age> min old)` only when a hand-written file is newer than the hook's; `AFTER COMPACT: read the snapshot above before your next action; accept the OPEN DISPATCH lines in a batch`.
2. Hook snapshot = newest file matching `^\d{4}-\d{2}-\d{2}-\d{4}-(manual|auto|unknown)\.md$` (the names `compact_snapshot.py` writes); hand-written = every other `*.md` except README.
3. Stale/missing: no hook snapshot, or the newest is older than `STALE_MIN` (10 min) -> the first line reads `COMPACT SNAPSHOT: MISSING for this compaction (newest hook snapshot <path>, <age> min old) -- write it now: python -B tools/compact_snapshot.py --source manual` (door per P15). Never "none" without the door.
4. `REMINDER` points to what PROJECT.md names (the newest `docs/tasks/compact-snapshots/*-manual.md` narrative + CURRENT_CONTEXT.md) instead of `factory-fixes.md` (F5).
Edges: folder absent -> MISSING line with the door; unreadable stat -> `unavailable (<reason>)` + door, never a crash (existing fail-open kept); two files with equal mtime -> name order decides (deterministic); clock skew (mtime in the future) -> age 0, not negative (existing `max(0, ...)`); `source` other than compact -> nothing added (unchanged). Temporal: before A0 the auto-compaction world is unverified — A1's lines work for whatever event reaches SessionStart with `source=compact`; if A0 shows auto-compaction does not reach it, node A3 (below) is opened, A1 is not reworked.
Tests (layer 3 table, existing files, rows not files): `test_session_context.py` one parameterised table: fresh hook snapshot / hook snapshot 11 min old (MISSING) / no folder / only hand-written files (MISSING + NARRATIVE) / hand-written newer than hook (both lines) / non-compact source (no lines). `test_compact_snapshot.py`: one row asserting REMINDER names no file absent on disk (a data join, not a phrase pin).
DoD: `python -m pytest tools/test_session_context.py tools/test_compact_snapshot.py -q` green; protocol check 32 text in the same commit (§8).

### A2 — the main-session WARN names the duty
owns: `C:\QAFactory\forge-repo\tools\agent_budget.py` (`_warns` text only), `C:\QAFactory\forge-repo\tools\test_agent_budget.py`
Behaviour: the main-session context WARN (not the worker's) adds: "write the compact snapshot (docs/tasks/compact-snapshots/) and tell the operator the one line (PROJECT.md)". Thresholds unchanged (300K, +50K). Fork F-A1 (the 350K auto window vs the 300K warn).
Edges: worker WARN text unchanged; context unknown -> no WARN (unchanged). Test: one row in the existing main-WARN table asserting the text names the snapshot folder. DoD: `python -m pytest tools/test_agent_budget.py -q`.

### A3 — conditional (opened only if A0 says auto-compaction does not reach SessionStart compact)
A new hook entry for the event A0 found (`PostCompact` or none). Not specified further until A0; owns `.claude/settings.json` (Lead places it, enforcement-file rule) — ordered after F6-36 (same file).

Four questions (A1+A2, one mechanism "post-compaction pointer"):
(a) cost: three lines per compaction; nobody pays at other times. (c) detector: check 32 (edited, §8) + `test_session_context.py`. (d) on the path: the SessionStart hook the host runs on compaction; the Lead reading the line is discipline, detector check 32 (a compaction followed by a Lead action before any Read of the named snapshot = a finding).
(b) axes: 1 covered (PROJECT.md wording quoted, no role file changes); 2 n/a (no exam instrument); 3 n/a (no package); 4 n/a (no FR); 5 n/a; 6 n/a; 7 n/a; 8 n/a; 9 n/a; 10 n/a; 11 n/a (no command words read); 12 covered (snapshot names `compact_snapshot.backlog_rows` readers untouched); 13 n/a; 14 n/a (no transcript read); 15 n/a; 16 n/a; 17 n/a; 18 n/a (no ratchet); 19-30 n/a (package axes); 31 covered (REMINDER is the one owner of "what to read after compact"; the SessionStart line points to it); 32 n/a; 33 n/a; 34 covered (one rule for manual and auto compaction, no branch by trigger); 35 n/a; 36 n/a.

## 3. B — short hand-back

§1 Goal: a worker's final message is a pointer plus a per-item status; everything heavy lives in the report file.
Invariant: work done is never lost — a worker whose dispatch names a `handoff:` path either wrote that file itself or says in its message why the Write was refused; a message with no path and no report never counts as delivered; the Lead never retypes a report.

Target and form: fork F-B1 (recommendation: at most 2,000 characters and at most 3 + N lines, N = numbered spec items; form below). Scope: fork F-B2 (recommendation builder, critic, designer; scout unchanged).
```
report: <absolute path of the handoff file>
1 done | 2 done | 3 not done -- <one clause> | 4 question
questions: none | 1) <question>
needed beyond the manifest: none | <paths>
```
No witness lines, tables, logs or file lists in the message (they are in the file). With no `handoff:` path, or a refused Write: the full report goes into the message as today (no cap) — unchanged world.

### B0 — one measurement (builder, no code)
owns: `C:\QAFactory\forge-repo\docs\tasks\specs\reports\fg-ctx-B0-handback-size.md`
Settles F8: `python -B tools/handback_extract.py --agent <id> <scratch out>` on 10 workers of 12.11 (ids from `worker_ref` of dev1.jsonl); record `lines=`/`bytes=` per worker and whether `source=handback`. If the hand-back text is absent from the worker transcripts, say so: B2's message-size detector then has no carrier and falls back to fork F-B3.

### B1 — the rule text
owns:
`C:\QAFactory\forge-repo\.claude\agents\builder.md` (rule 7 only)
`C:\QAFactory\forge-repo\.claude\agents\critic.md` (rule 16 only)
`C:\QAFactory\forge-repo\.claude\agents\designer.md` (rule 5 only)
`C:\QAFactory\forge-repo\tools\test_handoff_rule_anchors.py`
Behaviour: the three rules carry the new cap and form; "the closing lines of the witness" leaves builder 7; the fallback sentence ("never lost, never shortened"), "names no such path", "the Write is refused" and `ceil(len/200)` stay (anchors). The rule numbers do not move (check 28 (a) and the test key on them). `K2 = "at most 25 lines"` becomes the new cap key; RESTATED list updated so `docs/tasks/critic-diff-brief.md` and `plans/builder-rules.md` 11 still only point.
Edges: a dispatch whose spec has 0 numbered items -> cap 3 lines + the path; more than 20 items -> ranges allowed (`1-12 done`); resubmission after a hook block -> path and digest whole (unchanged rule).
Tests: the existing anchor table rows with the new key; no new file. Note for the critic: this file is a text pin of the kind TESTING.md lists as "не пишется"; it is the detector check 28 (a) names, kept until a forge role-rule registry exists (fork F-B4).
DoD: `python -m pytest tools/test_handoff_rule_anchors.py -q`.

### B2 — the code layer at SubagentStop
owns: `C:\QAFactory\forge-repo\tools\dod_gate.py`, `C:\QAFactory\forge-repo\tools\test_dod_gate.py`
Behaviour:
1. `BLOCK_MESSAGE` resubmission clause: "repeat the path and the digest whole (or, with no handoff path, the full report)" instead of "a COMPLETE final report all over again".
2. New data check, after the green-run check: when the worker's dispatch text (through `transcripts` and `dispatch_manifest.handoff_paths` — the readers `handoff_gate` already uses; no second parser, axis 13/14) names an absolute handoff path and the session track holds no Write/Edit by THIS `agent_id` with that `file_path`, block ONCE per agent with: "HANDOFF MISSING: your dispatch names <path> and you did not write it. Write the report there; if the Write was refused, put the full report in your final message -- this block will not repeat." Recorded in `gate_log` as `handoff_missing`.
Error direction: may err toward PASS (an unreadable dispatch, transcripts not importable, a degraded cut, two handoff paths -> pass with a stderr line), never toward a second block for this reason (the hook cannot see the final message, so it cannot know a refused Write was explained).
Edges: no handoff path -> no check; handoff path relative -> no check (`handoff_paths` returns absolute only); the file exists but written by another agent/main -> block once (the worker did not write it); the existing safety valve (2 blocks) counts this block too; doc-only exemption unaffected (it concerns runs, not the report). Temporal: tracks written before B2 lack nothing (dod_track already records `file_path`).
Tests: `test_dod_gate.py` one table: path written by this agent (pass) / not written (block once) / second stop after that block (pass) / no handoff line (pass) / transcripts import fails (pass + stderr) / file written by main (block once).
DoD: `python -m pytest tools/test_dod_gate.py -q`.

Four questions (B, one mechanism "short hand-back + report-file check"):
(a) cost: the worker writes one file it already writes; the Lead reads the file at acceptance (it already does, check 28 (d)); saves ~1-3K tokens of Lead context per hand-back (estimate, F8). (c) detector: check 28 rewritten (§8): `handoff_missing` gate_log entries, messages over the cap counted by `handback_extract` (or fork F-B3), retypes (28 (d)). (d) on the path: `dod_gate` SubagentStop for the file; the message cap itself is discipline, detector check 28 (b).
(b) axes: 1 covered (three role files + dod_gate text, one commit); 2 n/a; 3-10 n/a (no package/measurer/test-identity/story/test-file/git-top change); 11 n/a; 12 n/a; 13 covered (handoff path read through `dispatch_manifest.handoff_paths` only); 14 covered (worker file through `transcripts` only; error direction stated); 15-30 n/a; 31 covered (role files own the form; brief and builder-rules keep pointers, test RESTATED); 32 n/a (no package census); 33 n/a; 34 covered (same rule for every writing role in scope; scout difference returned as fork F-B2); 35 n/a; 36 n/a.

## 4. C — command hygiene: four refusals, the rest allowed

§1 Goal: the gate refuses the four behaviours that hurt quality or team work, each with a door; every other "non-canonical" form (compound commands, a leading variable, loops, `python -c` for reading/calculation, `grep/cat/sed` without writing, `2>&1` in Bash) passes silently and stops counting as a violation.
Invariants (what must stay refused): (1) the session shell's working directory is never moved; (2) a file in a repository working tree is never edited by an ad-hoc command (it would bypass the Edit/Write hooks); (3) the journal is written only through Edit/Write; (4) a working-tree change that is not provably the caller's own is never discarded by checkout/restore. Equally: a read or calculation is never refused.

### Error direction (designer rule 1: `_classify_pyc_payload` moves from advice to gate)
A REFUSAL requires certainty; an uncertain match passes (visible marker only where stated). Asymmetry by cost: a false refusal costs one retry through a named door; a false pass costs an unreviewed edit. Therefore: certain mutation -> refuse; certain read -> silent; unclassifiable -> fork F-C2 (recommendation: one short WARN, no refusal). The journal class keeps its existing "always refuse" asymmetry (F9 docstring, class (d)).

### The classifier "ad-hoc mutation" vs "read/calculation"
Per top-level statement (outside quotes and outside foreign heredoc bodies — the existing masks; segmenter per fork F-C4):
- M1 redirect `>`/`>>`/`Out-File`/`Set-Content`/`Add-Content`/`tee`/`Tee-Object` whose target resolves inside the payload cwd's repository working tree (root = nearest ancestor holding `.git`, a file or a directory, found by path walk, no subprocess) and not under an ignore row (fork F-C3: data row, default `ci-out/`). Not M1: `2>&1`, `>&2`, `2>/dev/null`, `> $null`, `> NUL`, `>/dev/null`, targets outside the tree (scratchpad, temp), a target held in a variable (`> $f`, `> "$out"`): uncertain -> pass.
- M2 in-place editors: `sed -i`, `perl -i`, `python -m fileinput --inplace`-style, on any path argument inside the tree.
- M3 interpreter payload (`python`/`python3`/`py` `-c` or `- <<`): payload class M from the existing `_classify_single_payload` (`open(...,'w|a|x|+')`, `write_text`, `os.remove`, `shutil.*`, `json.dump`...) -> refuse; P -> silent; O/U -> fork F-C2. `node -e`, `ruby -e`, `perl -e`, `pwsh -c`: no AST classifier -> U (pass, F-C2) — named limit, P31 note: the difference is "no classifier exists", recorded as a data row of interpreters with `payload_classifier: none`, not a branch by name.
- Not mutation (pass): `rm`, `mv`, `cp`, `mkdir`, `Remove-Item`, `New-Item`, `git mv`, `git add/commit` — fork F-C3 asks whether file-level moves join M.
Awkward inputs that must stay on the safe side (test rows): `git commit -m "fix > 3 cases"` (quoted, pass); `python -c "print(open('a').read())"` (P, silent); `python -c "import json,sys; json.dump(x, sys.stdout)"` (stdout: P after the `_STDIO_DOTTED` rule — verify, it is `json.dump` qualified -> currently M: the builder states the verdict and the critic judges; expected direction: refuse is acceptable, a door exists); `python -c "open(p,'w')"` with `p` outside the tree (M by payload, the gate cannot resolve `p` -> refuse; door: named script or Write); `echo x > C:\Users\...\scratchpad\f.txt` (pass); `echo x > docs/a.md` (refuse); `echo x >> logs/journal/dev1.jsonl` (journal class, refuse); `ls logs/journal/dev1.jsonl 2>&1` (pass — fixes F10); a 100 KB command, 65 heredoc openers (existing cap: conservative branch = pass for M, never a wider refusal); CRLF line ends; Cyrillic paths; `cd` inside `bash -c "..."` (quoted, pass).

### The four refusals and their doors (P15: what is wrong, what is expected, the door)
| Class | Refused | Door text (short, ≤ 300 chars each) |
|---|---|---|
| cd | `cd`, `Set-Location`, `Push-Location`, `Pop-Location`, `sl`, `chdir` at the start of ANY top-level statement, any target, both shells. Legal: a bare `cd <this repo root>` with nothing after it (the way back, kept); a Bash subshell `( cd x && ... )` (does not persist; Bash only — PowerShell parentheses do not scope location). | "the shell's directory must not move: hooks find tools/ from it. Use git -C <dir>, python -B <absolute path>, --repo/--root, or a ( cd <dir> && ... ) subshell in Bash." |
| mutation | M1-M3 | "a repository file is edited only through Edit/Write or a named, committed script (CLAUDE.md command hygiene 4); write scratch output outside the tree (the scratchpad)." |
| journal | unchanged class (d), minus the F10 false positive | unchanged text + "use Edit/Write at the file's tail" |
| rollback | `git checkout [<rev>] -- <paths>`, `git checkout .`, `git restore <paths>` (not `--staged` alone), when `git status --porcelain -- <paths>` (run by the hook, timeout 5 s) is non-empty | "these paths have uncommitted changes that may be another session's. Restore from the byte copy you took before, or `git stash push -- <paths>` (recoverable)." Analogs `git reset --hard`, `git clean -f`: fork F-C5. |
Rollback edges: git missing / timeout / not a repo -> pass with the visible marker "rollback not checked: <reason>"; clean paths -> pass (nothing lost); a pathspec with globs -> passed to git as is; worktrees: the status runs in the payload cwd.
WARN layer after C: the hygiene hook emits refusals only, plus F-C2's single WARN if chosen, plus the fail-open marker. `MSG_CD_NON_ROOT_WARN`, the ` 2>&1` WARN/BLOCK in Bash, the `python -c` WARN texts for P/M-uncertain are removed. ` 2>&1` in PowerShell: fork F-C1 (one data row keyed by the tool's capability, AR-1 form).

### C0 — experiments (builder, no code)
owns: `C:\QAFactory\forge-repo\docs\tasks\specs\reports\fg-ctx-C0-experiments.md`
1. PowerShell tool: `$PSVersionTable.PSVersion`; `git status 2>&1; $LASTEXITCODE; $?` and `git rev-parse --verify nosuchref 2>&1; $LASTEXITCODE; $?` — does `2>&1` change `$?`/`$LASTEXITCODE` or the output objects (settles brief:51).
2. Whether the host matches a `PowerShell(git status *)` allow row: run `git status` through the PowerShell tool in a session in default (non-auto) mode and record whether a prompt appeared (settles F12; the operator runs this, builders are in auto).
3. Import cost of `hooklib` from a forge tool: `python -X importtime -c "import sys; sys.path.insert(0,'ai-packages/qa-factory/scripts'); import hooklib"` (only if F-C4 is answered "walk").

### C1 — the gate and its audit
owns:
`C:\QAFactory\forge-repo\tools\hygiene_gate.py`
`C:\QAFactory\forge-repo\tools\test_hygiene_gate.py`
`C:\QAFactory\forge-repo\tools\permission_audit.py`
`C:\QAFactory\forge-repo\tools\test_permission_audit.py`
`C:\QAFactory\forge-repo\tools\test_warn_messages.py` (only if it pins a removed message)
Behaviour: the classifier and table above; `_collect_signals` keys renamed in one commit with `permission_audit.classify_hygiene` (AR-22): `cd`, `mutation`, `journal`, `rollback` (+ `pyc_payload` kept for measurement); `HYGIENE_CLASS_LABELS` = the four refusal classes; `AUTO_ALLOW`/`SANDBOX_HEURISTICS` stay (they model host prompts, not hygiene). `PYC_DENY_ENABLED` removed (payload class decides). The module docstring's class list rewritten to match.
Edges: non-Bash/PowerShell tool, empty/malformed stdin -> silent (unchanged); classifier exception -> visible fail-open marker (unchanged); command over 64 KB -> payload classification skipped (existing `PYC_PAYLOAD_LIMIT` -> O), redirect/cd scan still linear; several classes at once -> order journal, rollback, cd, mutation; `permissionDecisionReason` = the first.
Tests (layer 3: one parameterised table in `test_hygiene_gate.py`, a row per awkward input above + the doors present in each refusal; the adversarial battery for outside input — magnitude 100 KB/1 MB, nesting (heredoc in quotes, quotes in heredoc), encoding (CRLF, Cyrillic, UTF-8 BOM in stdin), empty/broken JSON — each a row); `test_permission_audit.py`: one row per class label.
DoD: `python -m pytest tools/test_hygiene_gate.py tools/test_permission_audit.py tools/test_warn_messages.py -q`; CLAUDE.md/skill/protocol text in the same merge (C2).

### C2 — the rule text (Lead-tier commit; a builder may hand the text as content)
owns: `C:\QAFactory\forge-repo\CLAUDE.md` (section "Command hygiene" only — ordered with E4, same file), `C:\QAFactory\forge-repo\.claude\skills\permission-audit\SKILL.md` (step 2 table)
Text: the preamble "every custom form is a permission request" is replaced by "the deployment runs in auto mode; four behaviours are refused by `tools/hygiene_gate.py`, every other form is allowed". Point NUMBERS stay 1-7 (F17): 1 tests (where they run; the "canonical form" motive dropped, the narrow-target rule kept); 2 unchanged; 3 the directory refusal and its doors; 4 the mutation refusal (pt.4 a/b table rewritten: a named committed script legal; a read/calculation payload allowed); 5 journal; 6 unchanged; 7 rollback, now gate-backed for the dirty-path case (byte-copy duty for corruption probes unchanged). A short "ready commands" list (owner's word 7): `git -C <dir> <cmd>`, `python -B <abs path>`, byte copy and restore (`Copy-Item`/`cp` to the scratchpad and back), `git stash push -- <paths>`. Skill step 2: rows 59-62 (`grep/cat/python -c` reading, `cd X &&`/`2>&1`, canonical pytest form, poll loops) leave the violations column; poll loops move to "cost (rule 7)".

Four questions (C, one mechanism "hygiene refusals"):
(a) cost: zero for allowed forms (fewer turns: the owner's word 2); one retry per refusal through its door; the rollback check costs one `git status` per checkout/restore call. (c) detector: check 27 rewritten (§8) + `test_hygiene_gate.py`. (d) on the path: PreToolUse Bash|PowerShell hook, `permissionDecision: deny`; bypass = an ad-hoc write the classifier cannot see (variable target, unknown interpreter) — discipline, detector check 27 (a) (audit replays every window command through `_collect_signals`).
(b) axes: 1 covered (CLAUDE.md text + role files keep point numbers); 2 n/a; 3 n/a; 4 n/a; 5-10 n/a; 11 covered or queued per F-C4 (the forge gate is a reader of command words; axis 11's closing rule asks for `hooklib.walk`); 12 n/a; 13 n/a; 14 n/a (audit's transcript reads unchanged, queued there already); 15 covered (stdout utf-8 setup unchanged); 16-28 n/a; 29 n/a (no jsonl appender added); 30 n/a; 31 covered (CLAUDE.md owns the rule, skill points); 32 n/a; 33 n/a; 34 covered (one rule for main/workers and both shells; the PowerShell `2>&1` difference only as a data row, F-C1); 35 n/a; 36 n/a.

Dense WARN layers (question 2): "Command hygiene" — in scope (C1 removes every WARN of allowed classes). "Search returned nothing" 56.1 % (`tools/search_control_gate.py`), WITNESS ECHO 28.7 % and NOTES LEN 21.8 % (`tools/journal_echo.py`) — queued: different mechanisms and files (`calibration-20261112-p1.md:222-226`); fork F-C6 (recommendation: three findings in `forge`, filed by the Lead, one node each).

## 5. D — the worktree guard without a door

§1 Goal: a refusal of a compound read inside one's own worktree either stops happening (after C, a compound read is allowed) or names its door.
Invariant: no refusal a worker meets lacks "what is wrong / what is expected / the door" (P15, FR-1, FR-2).
Carrier: NOT FOUND (F16). Searched: `.claude/settings.json` hook commands (13 entries, read whole); `worktree` (-i) over `tools/*.py` (22 files; none a refusal of compound git; `agent_budget.PLAIN_GIT_RE` refuses compound git only past the 400K STOP and names its door); `tools/claude-mods/**` for `git|deny|block` (0; positive control `modules` -> 2 files). Hypothesis (not verified): the host's own built-in check on `cd <dir> && git ...` compounds.

### D0 — experiment (builder in a worktree, no code)
owns: `C:\QAFactory\forge-repo\docs\tasks\specs\reports\fg-ctx-D0-guard.md`
Run in the worker's own worktree: (1) `git -C <wt> grep -n test_controller_state -- tools | head -5`; (2) `cd <wt> && git grep -n test_controller_state -- tools`; (3) the same through PowerShell. Record the verbatim refusal and its source: a hook refusal names the hook command in the transcript ("PreToolUse:Bash hook ..."); a host refusal does not.
### D1 — after D0 and after C1 (same file)
If the source is a repo hook: owns that hook file + its test (named by D0); fix the text to the P15 shape. If the source is the host: owns `C:\QAFactory\forge-repo\tools\hygiene_gate.py` + `tools/test_hygiene_gate.py`: for the exact shape the host refuses (D0's command), the gate adds before the host check an `additionalContext` line "this form is refused by the host itself; use git -C <dir> ..." — fork F-D1 (the host message cannot be changed: P25, host settings are a given).
Four questions: (a) one line per such command; (c) detector check 27 (a) counts host refusals of this shape in transcripts; (d) PreToolUse hook. (b) axes: as C (11 per F-C4, 34 covered), others n/a.

## 6. E — the dispatch gate (FG7-18, FG7-20) and the fast pre-push set (FG7-19)

§1 Goal: a writing dispatch carries its siblings and its designer status in form; the gate brings the data (witness tests, carriers naming each owned path) so the Lead does not search for it; the integrator runs a fast registry set before pushing `main`.
Invariants: a writing dispatch with no `siblings:` line never goes out silently; a dispatch over the designer threshold never goes out without a `designer:` line; the gate never judges whether a siblings list is sufficient (P27) and never refuses a well-formed line; a resubmission under the same task needs no designer (rule 2).

### What `siblings:` must contain to pass (question 3)
A header line `siblings:` (same grammar as the six keys: outside fences and quotes, case-insensitive, bullets allowed), with a non-empty body: either `none -- <reason>` (reason non-empty) or at least one entry (a path, `axis N`, or a free item). `none` without a reason, an empty body, or only whitespace -> missing. Door: the line, or `manifest-skip: siblings -- <reason>`.
On a pass the gate prints (to the Lead, `additionalContext`) for each owned path: the carriers naming it that the `siblings:` body does not mention, as a NOTE ("named by <carrier>:<line>, not in siblings:") — a report, never a refusal.

### Where the carrier list comes from (AR-13)
One data file `tools/carriers.json` (the carrier files: `docs/SIBLING_MAP.md`, `plans/builder-rules.md`, `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`, `.github/workflows/*.yml`, `ai-packages/qa-factory/scripts/tests/test-layers.json`, `.../design/state-exits.md`, `.../design/architecture.md`, `.../design/factory-rules.md`, `.../references/gate-registry.json`, `.../references/stage-joints.json`, `tools/source-split-carriers.json`, `tools/warn_layers.json`) and ONE reader `tools/carriers.py` `naming(paths, root) -> {path: [(carrier, line)]}` (match: the repo-relative path, and the package-relative path for package files; basename alone is not a match). The three lists of F15 become readers of it — fork F-E2 (now, in E2, or queued).

### How the designer threshold is counted from the dispatch text
`dispatch_manifest.designer_threshold(cut) -> (owns_count, items_count)`: `owns_count = len(owned_paths(cut))` (the one reader); `items_count` = lines matching `^\s*\d+[.)]\s` outside quoted lines and outside every manifest section (given, owns, non-goals, handoff, edges, DoD, siblings, designer). Over the threshold when either is >= 3 — fork F-E3 (count items at all, or owns only). Required then: `designer: <absolute path of the accepted draft>` (the path must exist — stat in dispatch_gate, like given paths), or `designer: skip -- <reason>` (passes; the note says "a dispatch_skipped(agent=designer) event is owed, rule 2"), or `designer: resubmission <task_id>` (passes; rule 2's continuation; calibration 1 (d) reads re-badging). Door also `manifest-skip: designer -- <reason>`.
Refusal or WARN for both lines: fork F-E4 (recommendation: refusal, exit 2, like the other six items).

### E1 — the pure part
owns: `C:\QAFactory\forge-repo\tools\dispatch_manifest.py`, `C:\QAFactory\forge-repo\tools\test_dispatch_manifest.py`, `C:\QAFactory\forge-repo\tools\test_dispatch_cut.py`
Behaviour: `KEY_GROUPS` + `siblings` (`siblings?|neighbou?rs`) and `designer`; skip items extended; `SECTION_STOP_RE` gains both (an owns continuation stops at them); `check_cut` gains the siblings form check (writing dispatches) and the designer check (over threshold); `INCOMPLETE_TEMPLATE` lists the two lines with their forms; `designer_threshold` added. Module stays pure.
Edges: a non-writing dispatch (scout, critic, designer with handoff only) -> neither check (unchanged `checked=False`); degraded cut -> UNCHECKED note, no refusal (unchanged); `siblings:` inside a fence -> not a header (named); `designer:` path relative -> treated as missing (absolute required, as owns); prose "Siblings of X:" mid-text counts as a header (the named open limit of given, same grammar).
Readers to check in the same commit (axis 13): `owns_gate` (imports `SECTION_STOP_RE`), `handoff_gate`, `dispatch_gate`; `hop_metrics._manifest_lines` repeats the stop rule (owned by FG7-29: report, do not edit).
Tests: `test_dispatch_manifest.py` one table: siblings with paths / `none -- why` / `none` (refused) / empty (refused) / absent (refused) / skip line / scout dispatch (unchecked) / `Siblings:` case / in a fence (refused as absent); designer: 2 owns (no check) / 3 owns no line (refused) / 3 owns + skip / + resubmission / + path / 3 numbered items in body (refused per F-E3) / 3 numbered items only in DoD (no check). `test_dispatch_cut.py`: a stop-at-siblings row.
DoD: `python -m pytest tools/test_dispatch_manifest.py tools/test_dispatch_cut.py tools/test_owns_gate.py -q` (the last as a reader check, not owned).

### E2 — the I/O part (after E1)
owns:
`C:\QAFactory\forge-repo\tools\dispatch_gate.py` (`decide_full` path check for `designer:`; a new WARN/NOTE function in `main`'s tail)
`C:\QAFactory\forge-repo\tools\test_dispatch_gate.py`
`C:\QAFactory\forge-repo\tools\carriers.py` (new)
`C:\QAFactory\forge-repo\tools\carriers.json` (new)
`C:\QAFactory\forge-repo\tools\warn_layers.json` (two rows: SIBLINGS NOTE, WITNESS PRINT; population: writing dispatches)
`C:\QAFactory\forge-repo\tools\mechanism_gate.py` (`MECHANISM_PREFIXES` += `tools/carriers.py`, `tools/carriers.json`: imported by a hook; closure test)
`C:\QAFactory\forge-repo\tools\test_mechanism_gate.py` (only the closure row)
Behaviour: on an allowed writing dispatch, the NOTE block lists per owned path (cap 10 paths, 5 lines each, then "+N more"): witness lines (package path: `scenario_walk.witness_for([path])`, first 5 lines, then "+N more: run scenario_walk.py --witness-for <path>"; non-package path: "witness: no scenario row -- name the test file in the DoD" until FG7-15 lands, then the same call — temporal case, the switch is FG7-15's row in `witness_for`, not a flag here) and carrier lines not mentioned in `siblings:`. Fork F-E1: also inject into the worker's prompt.
Edges: no cwd in payload -> no printout (as the path check); `scenario_walk` import fails -> "witness: unavailable (<reason>)", dispatch goes out; `carriers.json` absent/broken -> "carriers: unavailable (<reason>)"; a carrier file absent -> skipped and named once; total printout cap 60 lines; harness-sized outputs (hundreds of keep rows) -> truncated by the caps above; time budget 2 s for the whole block, past it "+ not finished (time)".
Tests: `test_dispatch_gate.py` rows: package path with a keep row / tools path before FG7-15 / carrier named & mentioned (no note) / named & not mentioned (note) / import failure / caps.
DoD: `python -m pytest tools/test_dispatch_gate.py tools/test_mechanism_gate.py -q`.

### E3 — the fast pre-push set
owns:
`C:\QAFactory\forge-repo\docs\RUNBOOK.md` (§7 only)
`C:\QAFactory\forge-repo\.githooks\pre-push.next` (content for the Lead to place on `.githooks/pre-push`: enforcement-file rule, CLAUDE.md rule 2)
Behaviour (per fork F-E5, recommendation: hook + list in RUNBOOK): on a push whose remote ref is `refs/heads/main`, run in order, stop at the first red, print each command and its time: `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`; `python -B ai-packages/qa-factory/scripts/tests/test_audit_rules.py` (~5 s, p4:106); `python -B ai-packages/qa-factory/scripts/tests/test_gate_registry.py`; `python -m pytest tools/ --collect-only -q` (t-053 class); `python -B tools/lint_ratchet.py --check`; `python -B tools/dup_ratchet.py --check`. `test_driver_layers.py` is NOT in the set (72 s locally, 300 s on CI: FG7-19 finding) — fork F-E6. Budget: 90 s total; over it the hook prints the time and does not refuse.
Edges: push of any other ref -> nothing runs; a missing script -> named line, push refused (door: `git push --no-verify` is always the operator's, the hook says so); the existing old-history check runs first, unchanged.
Test: no new test file (TESTING.md); the witness is a DOC-DISPATCH key run for RUNBOOK + one manual `pre-push.next` run on a `main` push dry run (`git push --dry-run` triggers hooks: verify in C0? — listed in §10).

### E4 — the rule text (Lead-tier; after C2 in the same file)
owns: `C:\QAFactory\forge-repo\CLAUDE.md` (rule 2's threshold sentence; R11-f row: the header lines gain `siblings:` and, over the threshold, `designer:`)
Rule 2 gains: "counted by `dispatch_manifest.designer_threshold`". R11-f lists the two lines. Designer rule 1 needs no edit (it points to R11-f).

Four questions (E1+E2, one mechanism "dispatch gate: siblings and designer"):
(a) cost: one or two header lines per writing dispatch; a refused dispatch costs one re-send; the printout ~10-60 lines of Lead context per writing dispatch (offset by fewer `rejected` of cluster A: 6 of 14, `calibration-20261112-p2.md` 15(ii)). (c) detector: check 1 (c) (now: dispatches whose threshold the code counted with a `designer: skip` line and no `dispatch_skipped` event), check 15 (cluster A count), check 11 (the two new layers' density). (d) on the path: PreToolUse Task|Agent, exit 2.
(b) axes: 1 covered (CLAUDE.md R11-f + rule 2 in E4; role files point); 2 n/a; 3 n/a (reads package files, writes none); 4 n/a; 5 n/a; 6 n/a; 7 n/a; 8 n/a; 9 n/a; 10 n/a; 11 n/a; 12 n/a; 13 covered (new keys in the one cut; readers owns_gate/handoff_gate/dispatch_gate checked; hop_metrics queued to FG7-29); 14 n/a (no transcript read); 15 n/a; 16 n/a; 17 n/a; 18 covered (warn_layers rows are a registry, not a ratchet; no raise); 19-30 n/a; 31 covered (CLAUDE.md owns the header list, the module's template points); 32 n/a; 33 n/a; 34 covered (one gate for every writing dispatch, any role, any language); 35 n/a; 36 n/a.
E3: (a) ≤ 90 s per push to main by the integrator; (c) detector check 24 (gate walk by `defect_found`: a canon-caught defect a pre-push command would have caught = a leak); (d) `.githooks/pre-push`; bypass `--no-verify`, discipline, detector check 24. Axes: 1 n/a; 9 covered (the collect-only row is "is this a test file"); 18 covered (the ratchets run, none raised); 34 covered; others n/a.

## 7. Landing order and parallelism (question 4)

| Wave | Nodes (parallel inside a wave) | Why |
|---|---|---|
| 0 | A0, B0, C0, D0 (reports only) | measurements before mechanisms (hygiene 6a) |
| 1 | A1, A2, B1, B2, C1, E1, E3 | disjoint owns |
| 2 | E2 (after E1: imports it); C2 (after C1, Lead-tier, same merge as C1); D1 (after D0 and C1: `hygiene_gate.py`) | shared files / dependency |
| 3 | E4 (after C2: `CLAUDE.md`); protocol edits (below) land with their node's merge | one writer per file |
| cond. | A3 only if A0 says so; after F6-36 (`.claude/settings.json`) | |

Shared files and their order: `CLAUDE.md`: C2 then E4. `tools/hygiene_gate.py`: C1 then D1. `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`: each node's paragraph lands in that node's merge commit, applied by the Lead (mechanism path, tier line): A1 (check 32, 17 (d)), B2 (check 28), C1+C2 (check 27, check 11's hygiene population), E2 (checks 1 (c), 11, 15, 19's snapshot unchanged), E3 (check 24); disjoint paragraphs, in wave order. `tools/dispatch_manifest.py`: E1 only. FG7-18/FG7-20 nodes in batch-7 are replaced by E1/E2 (the Lead marks them).

## 8. Protocol edits (same commit as the mechanism)

- Check 27 (meaning changes): from "count of four hygiene classes, cd/2>&1/python -c as violations" to "count of the four REFUSAL classes (cd, mutation, journal, rollback) over all window calls, from `permission_audit --summary` (labels from `HYGIENE_CLASS_LABELS`); (a) a violation is a call of a refusal class that was NOT refused (replayed through `_collect_signals` against the gate's verdict in the transcript) or an ad-hoc write the classifier cannot see found by reading the suspects; compound commands, `2>&1` in Bash, reads via `python -c`, poll loops are not counted (poll loops move to check 17 cost); (c) unsafe rollback: now also the gate's own refusals of dirty paths, counted; the baseline of 12.11 (39/68/58/1 unique) is NOT comparable and a new baseline is recorded." Remove "an ad-hoc read bypassing Read/Grep" and "bypassing the canonical pytest form" from (a).
- Check 28 (meaning changes): title "Completeness of hand-backs: the report file and the short digest". (a) anchors: the new cap key; (b) failure: `gate_log` entries `handoff_missing` of `dod_gate` per window (the code layer the old text named as a candidate now exists), hand-back messages over the cap counted by `handback_extract` on the window's workers (or F-B3), re-request notes as before; (c), (d) unchanged. First window after B records a new baseline.
- Check 32: add "every compaction is followed by the `AFTER COMPACT:` line; a `COMPACT SNAPSHOT: MISSING` line is a violation; a compaction of `trigger: auto` is checked like a manual one (A0's finding names which event carries it)".
- Check 17 (d): "a turn over 600K means a compaction was skipped" stays; add "with auto-compaction at 350K (if A0 confirms the key), a turn over 400K is a finding of the auto window".
- Check 1 (c): "counted from the dispatch's `owns` line" becomes "counted by `dispatch_manifest.designer_threshold` on the dispatch text; a `designer: skip` line without a matching `dispatch_skipped(agent=designer)` is the violation".
- Check 11: layer list gains SIBLINGS NOTE, WITNESS PRINT (`tools/dispatch_gate.py`); "Command hygiene" gets a declared population (Bash/PowerShell calls) once C1 lands.
- Check 19: if A3 adds a hook, the reference snapshot names it in the same commit.

## 9. Forks (Lead decides; builders proceed on the recommendation where marked)

| Id | Question | Options | Recommendation | Meanwhile a builder |
|---|---|---|---|---|
| F-A1 | Main WARN at 300K vs auto window 350K | keep 300K/+50K / move to 250K so the warn precedes the auto cut by 100K | keep 300K (50K before the cut is one stage boundary) | A2 on 300K |
| F-A2 | Cwd-relative hooks (F3) make A silent from the parent folder | wait for F6-36 / fold an absolute-path form of all hook commands into A3 | wait for F6-36 (its node, same file) | A1 proceeds |
| F-B1 | Target size and form | 25 lines minus witness / ≤ 2,000 chars and 3+N lines / fixed ≤ 8 lines | ≤ 2,000 chars, 3+N lines, form §3 | B1 on the recommendation |
| F-B2 | Who gets the short form | builder only / builder+critic+designer / + scout (needs Write and a handoff path, handoff_gate change) | builder+critic+designer; scout stays (FG7-29 owns its exchange) | B1 three files |
| F-B3 | If B0 shows hand-back text is not in worker transcripts | measure from the main transcript's task notifications (new reader) / no message-size detector, file check only | file check only until a reader exists; queue the reader | B2 unaffected |
| F-B4 | `test_handoff_rule_anchors.py` is a text pin TESTING.md disallows | keep as check 28 (a) detector / a forge role-rule registry (one test, anchors as data) | keep now, queue the registry | edit keys |
| F-C1 | `2>&1` in PowerShell (brief:51) | allow everywhere / one data row keyed by tool capability "stderr merge alters native status" -> WARN in that tool only | decide on C0's measurement; if it alters `$?` only (not `$LASTEXITCODE`), allow everywhere | C1 allows in Bash; PowerShell row pending |
| F-C2 | Unclassifiable interpreter payload (O/U) | silent / one WARN line / refuse | one short WARN (the only hygiene WARN left) | C1 with WARN |
| F-C3 | Scope of "mutation" | content writes only (M1-M3) / + rm/mv/cp/Remove-Item inside the tree; ignore rows (`ci-out/`) | content writes only; ignore row `ci-out/` as data | C1 on M1-M3 |
| F-C4 | Segmenter for statements | keep hygiene_gate's own masks (queue axis 11) / import package `hooklib.walk` (one tokenizer, axis 11 rule; import cost per Bash call, C0.3) | keep own masks now, queue convergence with a line on axis 11 (the map's queued list already has B-434 twins) | C1 on own masks |
| F-C5 | Rollback class width | checkout/restore only / + `git reset --hard`, `git clean -f`, `git stash drop` (same harm) | include reset --hard and clean -f | C1 on checkout/restore; add if accepted |
| F-C6 | Dense layers Search returned nothing / WITNESS ECHO / NOTES LEN | in this spec / three findings, one node each | three findings (disjoint files, separate mechanisms) | none |
| F-D1 | If the guard is the host's | WARN door from hygiene_gate ahead of the host check / CLAUDE.md ready-command line only | both (the line is in C2 anyway) | waits D0 |
| F-E1 | "печатает в диспатч" | print to the Lead (additionalContext) + carriers in the refusal / also inject into the worker prompt via the host's input rewrite (capability unverified, needs an experiment) | Lead-only now | E2 Lead-only |
| F-E2 | The three carrier lists of F15 | migrate to `carriers.json` in E2 / queue | queue (test_quarantine.py is large and outside this topic); note on axis 13 | E2 creates the reader only |
| F-E3 | Threshold count | owns + numbered items outside manifest sections / owns only (the finding's choice; deviates from rule 2's text) | owns + items outside sections; rule 2 names the counter (E4) | E1 both counts |
| F-E4 | Missing `siblings:`/`designer:` | refusal with door / WARN (FG7-18/20 findings' choice) | refusal (owner's word 4; 6 of 14 rejects are this class) | E1 refusal behind a module constant so a WARN switch is one line |
| F-E5 | Where the pre-push set lives | `.githooks/pre-push` on main pushes + RUNBOOK / RUNBOOK list only / a CI job | hook + RUNBOOK | E3 as content `.next` |
| F-E6 | `test_driver_layers.py` in the set | out (72-300 s) / in | out until it is under 30 s | E3 without it |

Closed by the designer (no design weight): STALE_MIN 10 min; printout caps (10 paths x 5 lines, 60 total, 2 s); ` (new)` style not used for `designer:`; door texts ≤ 300 chars; order of hygiene classes (journal, rollback, cd, mutation); the `designer: resubmission <task_id>` third form; report file names of A0/B0/C0/D0.

## 10. Not verified by this draft

- Whether `autoCompactWindow` is set anywhere (F4) and whether the host honours that key (A0.1).
- Whether auto-compaction fires PreCompact and SessionStart `source=compact`; whether a `PostCompact` event exists (A0.1).
- Whether the parent-folder cwd is the cause of the snapshot-less compaction of 11.11 21:09 (A0.2).
- Whether worker transcripts carry the hand-back text (F8, B0); the "2-4K tokens" size (estimate).
- What refused t-084's compound `git grep` (D0); the host-built-in hypothesis.
- `2>&1` effect in the PowerShell tool; the PowerShell version (C0.1); whether `PowerShell(...)` allow rows match (C0.2).
- The cost of importing `hooklib` per Bash call (C0.3).
- Whether `git push --dry-run` runs the pre-push hook (E3's witness).
- `json.dump(x, sys.stdout)` verdict of the payload classifier (C1 states it).
- Whether `tools/dispatch_manifest.py` is in `MECHANISM_PREFIXES` (the list was read only to line 265).

## 11. Reading trail

Read whole or in the cited ranges: the brief (1-73); `calibration-20261112.md` (1-89); p1 215-236; p3 160-249; p4 grep of check 32 (19, 49-69, 106); findings `20261112-{kontekst-lida..., spec-dispatchera..., porog-dizajnera..., suzhennyj-svidetel..., net-razdela-permissions..., nositel-perezhivaet...}.md`; batch-7 grep 15, 38-53, 61; `.claude/settings.json` 1-174; `tools/hygiene_gate.py` 1-1398; `tools/permission_audit.py` 1-130, 170-279, 437-586; `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` 18-75, 192-238, 477-503, 533-592, 777-862, 933-944; `tools/session_context.py` grep + 2215-2334; `tools/compact_snapshot.py` 1-80 + grep; `tools/dispatch_manifest.py` 1-135, 605-698 + grep of defs; `tools/dispatch_gate.py` 1-60, 700-799, 1900-2074 + grep; `scenario_walk.py` 833-932; `docs/TESTING.md` 1-148; `tools/test_handoff_rule_anchors.py` 1-172; `.claude/agents/builder.md` 64-84 (grep); `tools/dod_gate.py` 1-145 + grep; `tools/handback_extract.py` 1-50; `tools/agent_budget.py` 1-60, 262-291 + grep; `docs/SIBLING_MAP.md` 1-45, headings, 266-342; `tools/test_quarantine.py` grep + 1320-1346; `tools/warn_layers.json` 1-20 + grep; `docs/RUNBOOK.md` headings + 86-128; `.githooks/pre-push`; `tools/test_workflows.py` 1-30; `.claude/skills/permission-audit/SKILL.md` grep; `tools/mechanism_gate.py` 211-265; `docs/tasks/factory-fixes.md` grep `## State at`; onboarding-forge batch-1 1-12 + F6-36 row.
Searches for the worktree guard (D): `worktree` -i over `tools/*.py` -> 22 files, read the hits in session_context/permission_audit/dispatch_gate/handoff_gate/agent_budget (none refuses compound git); `git grep|worktree guard|защита рабочего` -i repo-wide -> only reports/brief; `guard|refus|hook` in `t-084-td11c-NC.md` -> line 79 only; `git|deny|block` -i in `tools/claude-mods` -> 0, control `modules` -> 2 files.
Noticed analogs / contradictions (reported, not widened): F4 (autoCompactWindow absent from the repo settings); F5 (stale REMINDER pointer, folded into A1); F6 (FG7-25 item 2 already built); F8 (p3 vs handback_extract); F10 (journal false positive, folded into C1); FG7-24's permissions section already landed in 7214fe4; PROCESS check 19 snapshot lists critic_snapshot/owns_gate as settings entries while `.claude/settings.json` has no such entries (they run inside dispatch_gate as trace readers — not verified).
