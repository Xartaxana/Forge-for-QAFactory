# FG7-89 -- the coordinator-rules read check (draft card, designer, t-1465)

Status: DRAFT for the Lead. Forks F1..F7 are open (section 7); the builder card (section 9) is written on the leans and
must be re-cut where the Lead decides otherwise. Feature F19, node forge/7/FG7-89, pile row
`plans/piles/forge/batch-7-vhodyashchie-4.md` line 114.

## 1. Goal, scope, architecture lines

Goal. The coordinator learns of its rule files (`coordinator_rules.COORDINATOR_FILES`, five files) only from the
SessionStart line `COORDINATOR RULES: read ... before your first dispatch, acceptance or commit`; no gate checks the
read (pile row; Lead 501cb4e0 committed after a compaction without re-reading). After this node: when the main
session's transcript, after its newest start/compaction boundary, holds no structural Read of each present file, the
three duty points -- a dispatch (Task/Agent), a verdict (`journal_write.py accept|reject`) and a commit -- get ONE
WARN line naming the unread files. WARN only; a refusal is a later node after the false-positive measurement (F6).

In scope: one pure judging function in `tools/coordinator_rules.py` (the owner of the list), one bounded backward
segment reader in `tools/transcripts.py` (the one transcript reader, SIBLING_MAP axis 14), two thin callers
delivered as `.py.next` copies (dispatch_gate, hygiene_gate), one registry row in `tools/warn_layers.json`, tests.

Out of scope: the refusal mode; the SessionStart line text (byte-identical); `session_context.py`; `.githooks/`;
`journal_write.py`; `.claude/settings.json` (no new hook entry under F3 (a)); any worker boot load.

Architecture. The node touches no `ai-packages/qa-factory/` file, so the AR-n walk, the AR-29 owner/census lines
and the architecture_gate commit lines do not apply (designer rule 1 condition). `variety: none -- one check, one
list (COORDINATOR_FILES), one transcript form, read the same way from both callers.` Mechanism chain: the touched
`tools/coordinator_rules.py` is in `tools/mechanism_gate.py::MECHANISM_PREFIXES` and the two gates are wired by
`.claude/settings.json`, so the commit carries the axis block that `tools/mechanism_gate.py` demands (rule 10(b));
the grammar lives there, not here.

## 2. Facts

Lead's (from `facts:`): (L1) `grep -n 'COORDINATOR RULES' tools/session_context.py` -- lines 280-291, the text comes
from coordinator_rules.py, no gate reads it. (L2) `grep -n COORDINATOR_FILES tools/coordinator_rules.py` -- line 24,
the tuple; line 10 "take it from COORDINATOR_FILES, never a copy".

Designer's (measured by Read/Grep, this session; commands in section 11):
- D1 The five files: COORDINATOR.md 500, PROJECT.md 276, docs/FACTORY_RULES_INDEX.md 76, docs/ARCHITECTURE_INDEX.md
  40, docs/OWNER_PRINCIPLES_INDEX.md 35 lines (Grep `^` count). Bytes: the pile's "~93 KB" is an `estimate`; the Lead
  reads it off the `(<n> files, <bytes> bytes)` field of the SessionStart line.
- D2 Transcript boundary forms (session 501cb4e0 main transcript): a compaction writes a top-level line
  `"type":"system","subtype":"compact_boundary"` (line 869), then an attachment
  `{"type":"hook_success","hookName":"SessionStart:compact",...,"hookEvent":"SessionStart"}` (line 886); the start is
  `"hookName":"SessionStart:startup"` (line 3). Both on `"isSidechain":false` lines.
- D3 A Read leaves a structural record on the user line of its result:
  `"toolUseResult":{"type":"text","file":{"filePath":...,"numLines":N,"startLine":S,"totalLines":T}}` -- e.g. line
  45618: COORDINATOR.md `numLines 501, startLine 1, totalLines 501`; line 260: a partial read `numLines 50,
  startLine 98, totalLines 1010`. Write/Edit results carry `"type":"create"`/`"update"`, not `"text"`. Error results
  carry `"is_error":true` (91 lines in that file).
- D4 The whole session 501cb4e0 holds exactly two `Read` tool_uses of COORDINATOR.md, both at lines 45616/45629 (late
  on 18.11), against about 66 SessionStart attachments -- the incident in numbers.
- D5 Worker/main split precedent: `hygiene_gate.py::_decide_command` line 1944 -- "a subagent's payload carries
  [agent_id]; the main thread's does not (P38)"; same rule in `agent_budget.py::resolve_transcript`.
- D6 Verdict recogniser exists: `hygiene_gate.py::_worker_verdict_call` (dod_track's program recogniser +
  `WORKER_VERDICT_VERBS = {"accept","reject"}`). No shared "is this a git commit" recogniser exists in tools/ (Grep
  `def \w*commit\w*\(` over tools/*.py: 20 hits, none a command classifier; positive by its own hits).
- D7 `tools/wave.py` runs `git commit` itself (2 hits of the literal `"commit"`), so a wave merge is a commit road.
- D8 Delivery door for hook files: `tools/conftest.py::next_copy_map` -- a builder delivers `tools/<name>.py.next`, a
  run with `<NAME>_PATH=tools/<name>.py.next` tests the copy (FG7-58).
- D9 WARN layers are registered in `tools/warn_layers.json` (id, literal, carrier, hook_event, matcher, ...) and
  validated by `python -B tools/warn_density.py --check` (literal-overlap rule at warn_density.py:365); this is also
  the counter the later refusal decision reads (F6).
- D10 `transcripts.py` docstring: a main transcript is 200-700 MB; `_read_back(path, enough, limit)` is the one
  backward-growth loop. Segment size between boundaries is an `estimate` (section 11, Lead command).
- D11 coordinator_rules' own tests live in `tools/test_session_context.py` (lines 3649-3732, the SessionStart-line
  door); `tools/test_coordinator_rules.py` does not exist (Glob `tools/test_{coordinator_rules,...}*.py`, positive:
  test_hygiene_gate.py etc. found by the same call).
- Observation (not load-bearing, F7): the startup attachment of 501cb4e0 (line 3) is a persisted-output pointer and
  holds no `COORDINATOR RULES: read` text; 15 compact attachments do hold it (same-shape Grep, startup 0 / compact 15).

## 3. Behaviour

3.1 `coordinator_rules.read_state(transcript_path, root) -> (verdict, detail)` -- pure, never raises, ASCII detail.
verdict is one of `read` (every present file covered), `unread` (detail: the uncovered present files, each with its
coverage when partial: `PROJECT.md (lines 1-120 of 276)`), `cannot-judge` (detail: one reason). Per-file
`cannot-judge` (a missing file) rides inside a `read`/`unread` verdict as a note.

3.2 The window. Read backwards from the end of the main transcript (through the new transcripts.py reader, stop
predicate = a whole parsed boundary line) to the NEWEST boundary line. A boundary is a parsed line with
`isSidechain` not true AND either (a) top-level `type == "system"` and `subtype == "compact_boundary"`, or (b)
`attachment.hookName` of the form `SessionStart:<source>` with source in `BOUNDARY_SOURCES = ("startup", "compact",
"clear")`. `SessionStart:resume` is not a boundary (the restored context still holds the earlier reads; matches
`_WHEN["resume"]`). File start reached with no boundary: the whole file is the window. `READ_SCAN_MAX` bytes read
with no boundary and the file start not reached: `cannot-judge (no start within <n> MB)`.

3.3 What counts as a read (on the F2 (b) lean). A parsed line in the window, `isSidechain` not true, whose top-level
`toolUseResult` is a dict with `type == "text"` and `file` a dict holding `filePath` (str) and `startLine`,
`numLines`, `totalLines` (ints, startLine >= 1). The file is covered when the union of `[startLine, startLine+numLines-1]`
over its reads covers `[1, totalLines]` of the NEWEST read's totalLines. Path match: `filePath` (joined to root when
relative) and `root/<name>` compared after `os.path.normcase(os.path.realpath(...))` (normpath when realpath fails).

3.4 Callers (F3 (a) lean). Both callers are main-thread only (payload without a non-empty str `agent_id`), call
`coordinator_rules.read_warn(payload, trigger)` lazily imported, and append its line to their existing
additionalContext; neither verdict (exit code, `permissionDecision`) is ever changed by it.
- `dispatch_gate.py.next`: every Task/Agent call on the exit-0 path; trigger `dispatch`.
- `hygiene_gate.py.next`: a Bash/PowerShell command with a verdict call (the `_worker_verdict_call` recogniser,
  same verbs) -> trigger `verdict`; a commit road (F5 lean: a statement-start `git` whose verb after global options
  is in `COMMIT_GIT_VERBS = ("commit", "merge")`, or a python program `tools/wave.py` with first positional `merge`)
  -> trigger `commit`. Any other command never opens the transcript.

3.5 Lines (ASCII, one line each, clipped by `ascii_line.clip` to 400 chars):
- `COORDINATOR-READ WARN: no Read since the last start/compaction of <files> (before this <trigger>) -- Read each
  whole with the Read tool (the COORDINATOR RULES line); WARN, does not block`
- `COORDINATOR-READ: cannot judge (<reason>) -- not checked; read <all five> if unsure`
- a `read` verdict prints nothing; a missing file adds `COORDINATOR-READ: cannot judge <name> (<absent|empty|...>)`.

## 4. Edges, each with its invariant

- E1 A session that never dispatches, records a verdict or commits owes nothing: the check runs at the three
  triggers only. INV: no other tool call, no SessionStart, no Stop opens the transcript or prints a COORDINATOR-READ
  line.
- E2 A compacted session owes the read again: `compact_boundary` and `SessionStart:compact` are boundaries, the newest
  wins. INV: a Read recorded before the newest boundary never counts, whatever its coverage.
- E2r Resume is not a boundary. INV: `resume` never discards a read of the restored context; startup, clear and compact
  always do.
- E3 A file of COORDINATOR_FILES missing, empty, a directory, unreadable or renamed (the tuple names the old path):
  `cannot judge <name>` (probe = `_probe`, stat only), the others still judged. INV: a missing file never yields
  `unread` and never a deny; it never silences the duty for the present files.
- E4 Workers are exempt: a payload with a non-empty str `agent_id` returns before any read. INV: a worker's call never
  gets the line; a payload without `agent_id` is the main thread (P38); a worker's Read (sidechain line or subagent
  file) never satisfies the Lead's duty.
- E5 The read is measured, never claimed: only the structural `toolUseResult.file` of 3.3. INV: no text the session
  writes -- a message, a journal note, a commit message, an echo, a quote of `"toolUseResult"` inside a string, a
  Write/Edit of the file -- ever counts as a read.
- E6 `transcript_path` present but not a file / unreadable / OSError mid-read: `cannot judge (<reason>)`. INV: an
  unreadable transcript never yields `unread` and never blocks.
- E6a `transcript_path` or `cwd` absent / not a non-empty str: SILENT (no line). INV: a harness payload always carries
  both, so silence is reachable only from non-harness callers (probes, CLI tests); see small choice C4.
- E7 The scan cap `READ_SCAN_MAX` (F-free, C2): window not bounded within it -> `cannot judge`. INV: a `read` verdict
  is issued only on a window that provably starts at or before the newest boundary.
- E8 A cut last line (the harness is writing), non-JSON, a non-dict JSON, a 200,000-`[` line: skipped
  (`transcripts.parse_line`). INV: a broken line is never a boundary and never a read.
- E9 A boundary text inside content (this card read by the Lead quotes `compact_boundary`): not a boundary. INV: a
  boundary is only the top-level `type/subtype` or `attachment.hookName` of a parsed line.
- E10 Partial reads (F2 lean): coverage union; `numLines` 0 or a negative/huge value: ignored for coverage. INV: a Read
  with `limit: 1` never covers a file longer than one line; a file changed after a whole read keeps its read (C5).
- E11 A Read of another copy (a worktree `.claude/worktrees/*/COORDINATOR.md`, `read-main`, a same-named file
  elsewhere): not the file. INV: only `<cwd>/<name>` counts; a read of other bytes never counts.
- E12 Any exception inside `read_warn` or a failed lazy import of coordinator_rules in a gate: one `cannot judge
  (<ExcType>)` line. INV: the gate's verdict (exit code, deny, its other WARN layers) is identical with and without
  this layer.
- E13 A command hygiene refuses AND that is a trigger (a commit chained after a `cd`): both texts appear. INV: the
  deny is unchanged; the WARN is additive.
- E14 A quoted mention (`echo "git commit"`, a heredoc commit body naming `journal_write.py accept`): no trigger --
  recognition runs on hygiene_gate's masked statements. INV: every statement-start commit road and verdict call
  triggers; a WARN on a mis-recognised command is noise, never a block.
- E15 TEMPORAL. World A (before the Lead places the copies): `read_state`/`read_warn` exist, nothing calls them, the
  SessionStart line is the only carrier (today). World B (after the Lead copies `tools/dispatch_gate.py.next` and
  `tools/hygiene_gate.py.next` over the live files at acceptance): the WARN fires. The registry row is inert data in
  both worlds until a carrier prints its literal. The move that creates world B is the Lead's placement.
- E16 POSITIONAL. dispatch_gate: the call sits after the blocking checks, on the exit-0 path, folded into the same
  single additionalContext as the other WARN layers. INV: a refused dispatch stays refused with the same text; the
  layer never runs before a refusal is decided. hygiene_gate: after `_collect_signals`, before output assembly. INV:
  every one of the four refusals stays reachable and byte-identical.
- E17 Time: the scan rides inside hook processes with stdin deadlines. INV: the bytes read per call are bounded by
  `READ_SCAN_MAX`; a non-trigger Bash call costs only the recogniser.

## 5. Error direction (the check is advice now, a gate later)

`read_state` may err toward `unread` (a WARN the Lead did not deserve) when a read cannot be proven inside a judged
window; it errs toward `cannot-judge` when the window itself cannot be established. Under a future refusal,
`cannot-judge` must stay a pass. Adversarial inputs that must stay on the safe side:
- must stay `unread`: Read with `limit: 1`; an error Read (`is_error`, string `toolUseResult`); a Read of a worktree
  copy; a Write/Edit of the file; Grep or `cat`/`Get-Content` of it (F2 lean); a sidechain Read; a Read before the
  newest compaction; a user message whose TEXT contains `"toolUseResult":{"type":"text","file":...}`.
- must stay `cannot-judge` (never `unread`): a missing rule file; an unreadable/absent transcript file; no boundary
  within the cap.
- must stay silent: a worker payload; a non-trigger command; a payload without transcript_path/cwd.

## 6. Readers of every touched file (rule 7)

The brief carries no `tools/owns_readers.py` block; the plan critic re-runs (Q13 (d)):
`python -B tools/owns_readers.py --paths tools/coordinator_rules.py tools/transcripts.py tools/dispatch_gate.py
tools/hygiene_gate.py tools/warn_layers.json --names read_state read_warn READ_SCAN_MAX BOUNDARY_SOURCES
COMMIT_GIT_VERBS --readers`. Hand greps (Grep tool, case-sensitive; each positive by its own hits):
(g1) `import coordinator_rules|from coordinator_rules|coordinator_rules\.` in tools/ -> 7 files;
(g2) `dispatch_gate\.py|hygiene_gate\.py` over tools/*.py, .githooks/*, .claude/settings.json, workflows -> 41 files,
223 hits; (g3) `import transcripts|from tools import transcripts|warn_layers\.json` in tools/ -> 20 files.

- coordinator_rules.py readers (g1): session_context.py, agents_md.py, architecture_index.py (docstring),
  mechanism_gate.py (prefix row), test_session_context.py, test_agents_md.py, test_mechanism_gate.py -- unchanged:
  COORDINATOR_FILES and coordinator_lines are byte-identical; names are only added. The new import of
  `transcripts` is lazy (inside `read_state`), so session_context's SessionStart import cost and e16 (stdlib only at
  import) are unchanged.
- transcripts.py readers (g3): agent_budget, handoff_gate, handback_extract, forge_metrics, dispatch_gate,
  journal_hooks, journal_echo, hop_metrics, permission_audit, session_retro, warn_density, usage_report,
  session_context, tier_echo and their tests -- unchanged: one function added, existing functions byte-identical.
- dispatch_gate.py readers (g2): .claude/settings.json hook command -- unchanged; owns_gate, critic_snapshot
  (import the module) -- unchanged API; test_dispatch_gate.py / test_dispatch_gate_md.py -- unchanged rows, one new
  row in this stream; hook_liveness_probe, enforcement_probe, test_p4_stdin_deadline -- verdicts unchanged, and their
  payloads carry no transcript_path, so E6a keeps them silent (builder confirms by the narrow run in DoD);
  test_warn_messages / warn_density -- change in this stream (new registry row); mechanism_gate, search_control_gate,
  claim_control_gate, negative_lint, tier_echo, journal_echo, dod_track, main_gate, dod_gate, agent_budget, conftest
  (name mentions) -- unchanged.
- hygiene_gate.py readers (g2): settings.json -- unchanged; permission_audit + test_permission_audit (load the
  classifier) -- verdicts unchanged; test_hygiene_gate -- new table in this stream; test_warn_messages (parametrized
  across hygiene WARN texts) -- the new literal is its own layer, the HYGIENE layer's texts unchanged; the module
  docstring's "every other form pass silently" -- changes in this stream (the copy's docstring names the WARN).
- warn_layers.json readers (g3): warn_density.py, test_warn_density.py, test_warn_messages.py -- change in this
  stream (one row); the literal `COORDINATOR-READ` overlaps no registered literal (the builder's `--check` run proves
  it).

## 7. Forks (returned, not decided)

- F1 Re-read scope after a compaction (cost ~93 KB, `estimate`, per compaction; about 7 % of a 317k-token segment at
  ~4 bytes/token, `estimate`). (a) all five files at every startup/compact/clear; (b) only files whose content
  changed since their last read (hash); (c) compaction owes COORDINATOR.md + the three indexes, PROJECT.md only at
  startup/clear. LEAN (a): (b) contradicts the given edge "a compacted session owes the read again" (after a
  compaction the context no longer holds an unchanged file either), and the incident was exactly an unchanged-file
  compaction; (c) is a real saving but a scope call for the owner.
- F2 What counts as a read. (a) any Read of the path, any offset/limit; (b) Read results whose line ranges together
  cover the file (3.3) [card built on this]; (c) only a whole-file Read (startLine 1, numLines == totalLines). Second
  axis: (i) Read tool only [lean]; (ii) also Grep/`cat` (Bash output is capped, so not a whole read). LEAN (b)+(i):
  (a) is satisfied by `limit: 1`; (c) punishes a Lead who reads a long file in two windows.
- F3 Where the check runs. (a) one function in coordinator_rules, called from dispatch_gate (dispatch) and
  hygiene_gate (verdict, commit), both as `.py.next` copies [card built on this]; (b) one new PreToolUse hook entry
  `Task|Agent|Bash|PowerShell` running a new script -- no edits to two big gates, but a settings.json change by the
  Lead, coordinator_rules stops being "library only", and one more Python start on every Bash call (`estimate`
  50-100 ms); (c) journal_write.py + `.githooks/pre-commit` -- neither has a transcript_path, so "measured from the
  transcript" fails (guessing the session by mtime meets peer sessions). LEAN (a).
- F4 Repetition. (a) the WARN on every trigger until the files are read [card built on this]; (b) once per boundary
  (needs a state file per session). LEAN (a): stateless, the duty is persistent; warn_density counts the noise.
- F5 Which roads are a "commit". (a) `git commit` only; (b) every commit road the coordinator runs: `git commit`,
  `git merge`, `tools/wave.py merge` (D7) as data rows [card built on this]; (c) (b) plus `cherry-pick`, `revert`,
  `am`, `rebase`. LEAN (b) (rule 6: a road left out is a second road); (c) costs rows nobody uses today.
- F6 The road to a refusal (pile: "after the false-positive measurement"). (a) no mode constant now; a later node
  reads warn_density counts for layer COORDINATOR_READ and the owner sets the threshold [lean]; (b) ship
  `READ_CHECK_MODE = "warn"` now (precedent `journal_hooks.JOURNAL_EDIT_MODE`) so promotion is one line. LEAN (a):
  (b) ships an untested refuse branch.
- F7 (another zone) The startup SessionStart attachment of 501cb4e0 is a persisted-output pointer without the
  `COORDINATOR RULES` text (section 2 observation): at startup the duty may be invisible to the Lead, which this
  WARN then becomes the only carrier of. (a) the Lead files a row for session_context's output budget; (b) widen this
  node. LEAN (a) -- out of this node's owns; cause not measured (the line may postdate that start).

## 8. Small choices closed by the designer

- C1 Triggers include `reject`: the verdict set is `hygiene_gate.WORKER_VERDICT_VERBS`, read, not copied (one road).
- C2 `READ_SCAN_MAX = 64 MiB` (constant in coordinator_rules); the segment size is an `estimate` -- the Lead's command
  in section 11 sets the real margin before acceptance.
- C3 The window reader lives in transcripts.py (`lines_back_to(path, is_boundary, limit)`, built on `_read_back`)
  because transcripts.py is the one transcript reader; coordinator_rules passes its boundary predicate.
- C4 Absent `transcript_path`/`cwd` is silent, not `cannot judge`: probes and CLI tests send such payloads, and the
  harness always sends both.
- C5 A read stays valid if the file changes later (the Lead's own edit, a pull); tracking bytes is F1 (b)'s domain.
- C6 Path match by normcase+realpath; relative `filePath` joined to cwd.
- C7 Literal `COORDINATOR-READ WARN:`; registry id `COORDINATOR_READ`, carriers both gates, `hook_event`
  PreToolUse, matcher `Task|Agent|Bash|PowerShell`, `reachable: "unmeasured"`.

## 9. Builder card

task: <Lead fills>
node: forge/7/FG7-89
given:
C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-89-coordinator-rules-read-card.md (sections 3-5 are the spec)
C:/QAFactory/forge-repo/tools/coordinator_rules.py
C:/QAFactory/forge-repo/tools/transcripts.py
C:/QAFactory/forge-repo/tools/dispatch_gate.py
C:/QAFactory/forge-repo/tools/hygiene_gate.py
C:/QAFactory/forge-repo/tools/warn_layers.json
C:/QAFactory/forge-repo/tools/conftest.py
owns:
C:/QAFactory/forge-repo/tools/coordinator_rules.py
C:/QAFactory/forge-repo/tools/transcripts.py
C:/QAFactory/forge-repo/tools/dispatch_gate.py.next
C:/QAFactory/forge-repo/tools/hygiene_gate.py.next
C:/QAFactory/forge-repo/tools/warn_layers.json
C:/QAFactory/forge-repo/tools/test_coordinator_rules.py
C:/QAFactory/forge-repo/tools/test_hygiene_gate.py
C:/QAFactory/forge-repo/tools/test_dispatch_gate.py
non-goals: no edit of the live tools/dispatch_gate.py or tools/hygiene_gate.py (copies only; the Lead places them); no refusal mode; COORDINATOR_FILES, coordinator_lines and the SessionStart line byte-identical; no session_context.py, settings.json, .githooks/ or journal_write.py change; no worker boot load
handoff: branch with the commit (axis block per tools/mechanism_gate.py) + report: witness tails, `tests not written:` lines, the two `.py.next` paths for the Lead to place
edges: E1-E17 of section 4 of the given card, each with its invariant, and the adversarial list of section 5
DoD: `python -m pytest tools/test_coordinator_rules.py -q; HYGIENE_GATE_PATH=tools/hygiene_gate.py.next python -m pytest tools/test_hygiene_gate.py -q; DISPATCH_GATE_PATH=tools/dispatch_gate.py.next python -m pytest tools/test_dispatch_gate.py -q; python -B tools/warn_density.py --check; python -m pytest tools/test_warn_messages.py -q -k "COORDINATOR_READ or coordinator_read"`
siblings: FG7-88 (tools/journal_hooks.py, journal_validator.py, session_context.py -- disjoint owns); FG7-86 (tools/forge_metrics.py -- disjoint); any open stream owning dispatch_gate.py or hygiene_gate.py meets this node at those two files -- the Lead checks before fan-out
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-89-coordinator-rules-read-card.md

Work, in order:
1. transcripts.py: `lines_back_to(path, is_boundary, limit)` -> `(lines, bounded)`: the complete parsed-line texts from
   the newest line for which `is_boundary(obj)` is true (exclusive) to the end, and `bounded` False when `limit` was
   hit with no boundary and the file start not reached. Built on `_read_back` (stop predicate parses the whole
   lines of the added bytes; a boundary candidate cut at a chunk edge is re-judged on the joined window). Raises
   OSError like its siblings. Existing functions byte-identical.
2. coordinator_rules.py: `BOUNDARY_SOURCES`, `READ_SCAN_MAX`, `read_state(transcript_path, root)` (3.1-3.3, E2-E11),
   `read_warn(payload, trigger)` (3.4-3.5, E4, E6, E6a, E12; returns "" or the line(s)). Lazy `import transcripts`
   inside. Docstring: the new duty, the error direction of section 5, "library only" kept.
3. `tools/dispatch_gate.py.next` = the live file + the call of 3.4 at the position of E16; `tools/hygiene_gate.py.next`
   = the live file + the commit-road recogniser (`COMMIT_GIT_VERBS`, the wave row) over the masked statements + the
   call; docstring sentence on the new additive WARN. Each copy differs from its live file only by these hunks.
4. warn_layers.json: the C7 row.
5. Tests, top-down, until test lines reach code lines (docs/TESTING.md «Бюджет / Объём»):
   test: tools/test_coordinator_rules.py::one parametrized table over synthetic transcripts built once in tmp_path
   (rows: all five whole after the newest boundary -> read; one unread -> named; read before compact_boundary ->
   unread; resume boundary keeps earlier reads; partial union covers / does not cover; error Read; sidechain Read;
   worktree copy; quoted toolUseResult text; boundary text inside content; missing file -> cannot judge that name;
   transcript absent -> cannot judge; cap hit -> cannot judge; cut last line) | expected from: card sections 3.2-3.3, 4 E2-E11, 5
   test: tools/test_hygiene_gate.py::one parametrized table of `decide` on payloads with a tmp transcript (rows:
   `git commit`, `git -C x commit`, `git merge`, `python -B tools/wave.py merge`, `journal_write.py accept`, `reject`,
   `git status` -> no line, worker agent_id -> no line, quoted `echo "git commit"` -> no line, `cd x && git commit`
   -> deny unchanged + WARN) | expected from: card 3.4, E1, E4, E13, E14, F5 (b)
   test: tools/test_dispatch_gate.py::one row pair: unread transcript -> WARN folded into additionalContext with the
   exit code unchanged; same payload with agent_id -> no line | expected from: card 3.4, E12, E16
   The new file test_coordinator_rules.py is justified by «Бюджет / Файлы»: a new door (a gate WARN measured from a
   transcript), not the SessionStart-line door that test_session_context.py runs; it builds its world once.

## 10. Acceptance keys (critic and Lead)

- K1 `read_state` verdicts match section 5's three safe-side lists on the table rows (critic re-runs the table).
- K2 The two `.py.next` copies differ from their live files only by the hunks of work step 3 (`git diff --no-index`).
- K3 With the copies placed, a refused dispatch and each of hygiene's four refusals are byte-identical to before
  (rows in the existing tables stay green under the `_PATH` runs).
- K4 COORDINATOR_FILES, coordinator_lines and `transcripts.py`'s existing functions are byte-identical (diff hunks
  are additions only).
- K5 `warn_density --check` exit 0 with the new row; the literal overlaps nothing.
- K6 No COORDINATOR-READ line on a payload without transcript_path (probe payloads stay silent).
- K7 Test lines <= code lines, or `tests not written:` lines in the report.

## 11. Reading trail

Read: plans/piles/forge/batch-7-vhodyashchie-4.md 113-114; tools/coordinator_rules.py whole; tools/session_context.py
255-314; tools/dispatch_gate.py (Grep of defs/WARN layers, 1780-1858); tools/journal_hooks.py 1-40 + defs;
tools/hygiene_gate.py 1-30, 80-89, 192-197, 1915-1954, 2023-2121; tools/transcripts.py 1-56, 131-290 + defs;
tools/agent_budget.py 140-169; tools/conftest.py 18-47; tools/mechanism_gate.py 1-40, 205-234;
tools/warn_layers.json 1-32 + ids; tools/test_warn_messages.py 1-30; tools/test_warn_density.py 1-30;
docs/TESTING.md 75-114, 215-264; .claude/settings.json hook entries (Grep).
Measurements (Grep tool on C:/Users/i_mas/.claude/projects/C--QAFactory-forge-repo/501cb4e0-b55f-46d8-9262-11b1caefad61.jsonl):
`compact_boundary` count 50; `"hookName":"SessionStart:[a-z]+"` first hits 3 startup, 886/1846/2547/... compact;
`"name":"Read","input":\{"file_path":"[^"]*COORDINATOR\.md"` -> lines 45616, 45629 only;
`"numLines":\d+,"startLine":\d+,"totalLines":(499|500|501)\}` -> line 45618; `"is_error":true` count 91;
startup-attachment + `COORDINATOR RULES: read` 0, compact-attachment + same 15 (same-shape control).
Five-file line counts: Grep `^` count with a brace glob at the repo root.
`estimate` for the Lead to measure (designer has no shell): segment bytes since the newest boundary --
`python -B -c "import mmap,sys;f=open(sys.argv[1],'rb');m=mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ);i=max(m.rfind(b'\"subtype\":\"compact_boundary\"'),m.rfind(b'\"hookName\":\"SessionStart:'));print(len(m),len(m)-i)" <main transcript>`;
the five files' bytes -- the `bytes` field of the current SessionStart line.
Noticed contradiction (reported, not widened): coordinator_rules.py line 10 says "never from a copy" while
session_context.py keeps `_COORDINATOR_FALLBACK_FILES`, a literal copy pinned equal by
test_session_context.py::test_the_fallback_list_equals_coordinator_files -- this card adds no copy.
Not measured: whether the harness ever writes a non-`text` Read result for an unchanged re-read (no such type seen
in 501cb4e0); E5 counts only `type == "text"`, so such a result would read as `unread` (safe side).

## 12. Lead decisions (Lead 501cb4e0, 2026-11-18)

- F1 (a): all five files after every startup, compaction and clear.
- F2 (b)+(i): Read results whose line ranges together cover the file; the Read tool only.
- F3 (a): one function in coordinator_rules, called from dispatch_gate and hygiene_gate, both as `.py.next` copies the Lead places.
- F4 (a): the WARN on every trigger until the files are read.
- F5 (b): `git commit`, `git merge`, `tools/wave.py merge` as data rows.
- F6 (a): no mode constant now; the promotion reads warn_density for COORDINATOR_READ later.
- F7 (a): the Lead files a row for session_context's startup output budget.
- Parallel with FG7-86, which renames `transcripts.send_targets` to `lead_calls`: this node adds `lines_back_to` next to `_read_back` and touches nothing else in transcripts.py; whoever lands second merges main.
