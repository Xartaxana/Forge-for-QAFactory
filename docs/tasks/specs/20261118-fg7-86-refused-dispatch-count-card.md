# FG7-86 -- refused dispatches per node beside the node cost (DRAFT, designer t-1466)

Node: forge/7/FG7-86, feature F19. Row: `plans/piles/forge/batch-7-vhodyashchie-4.md:111`. Parent decision: FG7-6/7 card
`docs/tasks/specs/20261118-fg7-6-fg7-7-coordinator-moves-card.md` §9 F6, §13 ("F6 (a) refused dispatches stay out of card A;
a separate pile row for them"). Depends on FG7-7 card A (moves). No money figure in this draft (P18).

## 0. Goal and scope

Goal: `python -B tools/forge_metrics.py --node-cost` counts, per row (node or task), the Agent/Task calls of the Lead that a
PreToolUse hook refused (`dispatch_gate` exit 2), and prints that count beside the node cost the way FG7-7 prints moves.
Scope: the read of the refusal channel (one pass over the parent sessions FG7-7 already reads), the join to a row, the
`--node-cost` data and print. Out of scope: any journal event, validator or hook change; `dispatch_gate.py`; the protocol.

## 1. Target on main, measured (file:symbol)

| what | where | state |
|---|---|---|
| refusal | `tools/dispatch_gate.py::main` :2141-2144 (completeness/paths/label), :2151-2154 (parallel cap), :2158-2160 (a trace reader): `write_verdict(payload, "refuse", ...)`, stderr, `return 2` | exists |
| the gate's own carrier | `dispatch_gate.py::write_verdict` :1758-1772: `logs/dispatch_verdict.json` rewritten WHOLE per dispatch (`_atomic_write_text(path, one record)`, :1769) | holds the LAST verdict only: cannot count a window |
| `delegated` | `tools/journal_hooks.py::_post_agent` :198-278, PostToolUse(Task\|Agent) only, after a launch result with an agent id (:205-207) | a refused call never reaches it |
| header ids | `tools/dispatch_manifest.py::header_ids` :872-901 (task/node/feature of a prompt, the reader `_post_agent` uses at :231-234) | exists |
| moves | `tools/forge_metrics.py::_nc_moves` :1240-1269, `::_nc_assemble` :1315-1349 (`moves = resumes + redelegations`), `::_moves_cell` :1409-1413, `::render_node_costs` :1423-1493 | exists in the root tree (FG7-7 card A) |
| parent-session pass | `tools/transcripts.py::send_targets` :530-550 (prefilter `"SendMessage"`, assistant, not sidechain, `first_copy`, `new_tool_uses`); its only caller `forge_metrics.py:1255` | exists |

### 1.1 The refusal channel -- the designer's measurement

- A refused Agent call is in the Lead's main transcript as a pair (sample
  `C:/Users/i_mas/.claude/projects/C--QAFactory-forge-repo/8781f497-4108-4e80-a5a1-057d52d56b3a.jsonl`):
  line 2722, assistant record, block `{"type":"tool_use","id":"toolu_01NWATyfcJuf27JDozic5Bpr","name":"Agent","input":
  {"description":...,"subagent_type":"builder","prompt":...}}`; line 2723, `"isSidechain":false`, `"type":"user"`, block
  `{"type":"tool_result","content":"PreToolUse:Agent hook error: [command hook 2]: DISPATCH PATHS MISSING ...",
  "is_error":true,"tool_use_id":"toolu_01NWATyfcJuf27JDozic5Bpr"}`, plus a top-level `"toolUseResult":"Error: ..."` string.
- Duplicates: lines 2763/2764 repeat the same tool_use id and tool_result in `api-request-blob` records (as §1.1 of FG7-6/7).
- Volume: the user-record form `"type":"user","message":{"role":"user","content":[{"type":"tool_result","content":"PreToolUse:(Agent|Task) hook error`
  -> 149 hits over 10 main transcripts; the loose form `"content":"PreToolUse:(Agent|Task) hook error: \[command hook [2]`
  -> 213 (copies included); the same loose form with `[^2]` -> 0. Every refusal seen is hook 2 (`.claude/settings.json`
  :15-32: hook 1 `agent_budget.py` has no matcher, hook 2 is `dispatch_gate.py`) -- the number is the harness's settings
  order and is NOT a key (§4).
- So the channel exists and carries the prompt (task/node lines) and the refusal: no journal schema is needed (non-goal holds).

### 1.2 Architecture (§1 lines)

- Package not touched -> `variety: none -- forge tools and their map row only; no file under ai-packages/qa-factory/`.
  `tools/architecture_gate.py` is silent on these commits; no `judgment:` line is prescribed.
- AR-13 (one reader per fact): main-transcript records are read only through `tools/transcripts.py` (SIBLING_MAP axis 14,
  `docs/SIBLING_MAP.md:341`). The refusal read joins the existing ONE pass (§2 R1); forge_metrics never parses a transcript.
  Change check: Grep `"is_error"|tool_result|PreToolUse:` over `tools/*.py` with a positive control; the only new reader is
  in transcripts.py.
- AR-15 (one survivor): the task/node of a dispatch prompt are read by `dispatch_manifest.header_ids(section_cut(prompt))`,
  the same call that gives the `delegated` line its task/node (`journal_hooks.py:231-234`). A refusal and the later
  `delegated` of the same prompt therefore name the same task. Change check: no new header regex in forge_metrics/transcripts.
- AR-29 / P27 census: the refused count is owner DATA (code joins and counts), class `xref` (transcript x journal join) and
  `shape`; a print, never a refusal (I-1 of FG7-5).
- Mechanism files: `tools/forge_metrics.py` (`tools/mechanism_gate.py:260`), `tools/transcripts.py` (:280),
  `docs/SIBLING_MAP.md` (:220). The builder STAGES, the Lead COMMITS (commit-line form: `tools/mechanism_gate.py`'s own).
- Import closure: forge_metrics is in the hook closure (FG7-6/7 §3). The new lazy import `dispatch_manifest` (inside
  `node_costs`) is already in that closure through the live hook `dispatch_gate.py`; `test_mechanism_gate.py:1691-1696`
  (no `hop_metrics` in the closure) holds as long as neither imports hop_metrics. I-2: importing forge_metrics stays light.

## 2. Design (written with the leans of §8; a different fork answer changes only the marked lines)

R1. One pass (AR-13): `transcripts.send_targets(path)` becomes `transcripts.lead_calls(path)` -> `{"sends": [...] (unchanged
    items), "refused": [{"id", "ts", "line", "prompt"}], "failed": int, "error": None|str}`; its one caller moves.
    Prefilter: a line goes on when it holds `SendMessage`, `PreToolUse:`, `"Agent"` or `"Task"`. Records: `first_copy` by
    uuid; `isSidechain is True` skipped; assistant records give SendMessage sends (as today) and Agent/Task tool_use blocks
    (`new_tool_uses`, id -> `input.prompt` when a str, else None); user records give `tool_result` blocks, each str
    `tool_use_id` once per pass. After the pass: a result with `is_error is True` whose text (`content_text(content)`)
    starts with `PreToolUse:Agent hook error` or `PreToolUse:Task hook error` is REFUSED (its prompt from the id map, None
    when the id named no tool_use in the file); a result with `is_error is True` on an Agent/Task id that is not that form
    is FAILED (F2). An OSError/ValueError mid-pass sets `error` and drops sends, refused and failed (no half number).
R2. Ids: per refused item `ids = dispatch_manifest.header_ids(dispatch_manifest.section_cut(prompt))` when the prompt is a
    str, else `{}`; an exception there is `{}` (the refusal still counts, §3 E1).
R3. Join (task first, never time or prose): (1) `ids["task"]` -> key `_jk.ref_key(task, {}, segs, journal.label_ids,
    journal.aliases)`; the key is in a row of the window -> that row; in a shared entry -> that entry; in `tasks` but in no
    window row/entry -> no-row `outside`; (2) no task id, or a key not in `tasks`: `ids["node"]` that is a row name of the
    window -> that row; a node that is not -> no-row `outside`; (3) neither -> no-row `no_task`. A no-row refusal counts
    only when `_nc_new_day(ts, win_day)` or ts is not a str (the A4 rule of FG7-7). A mapped one counts whatever its ts.
R4. Scope (F4): the same parent sessions `_nc_moves` reads (main transcripts of the window's found workers), each file once.
R5. Data (`--json` too): row and shared entry `refused` (int, or None = cannot judge, R7); `moves` = redelegations + resumes
    + refused (F1); totals `refused` = {"rows": n, "shared": s} or None when no session was read; `no_node` gains
    `"refused": {"no_task": a, "outside": b}`; totals `failed` = int (F2).
R6. Print: the moves cell becomes `N (resumes R, refused F)`, `>= N (resumes R, refused F, unscanned U)` with unscanned agents,
    `>= N (resumes R, refused cannot judge, unscanned U)` when NO agent of the row was scanned (U = the row's agent count,
    U > 0) or no session at all was read. The `coordinator moves:` line reads `redelegations + resumes + refused dispatches
    (SendMessage and PreToolUse refusals of Agent calls in the parent sessions of the window's workers: scanned S,
    unreadable U); no node: N (SendMessage to an agent with no delegated line A; delegated lines with no task_id B; refused
    with no task or node line C; refused for a task or node with no row in the window D)`; when S == 0 it ends `; refused
    dispatches: cannot judge (no parent session read)`; when failed > 0 it ends `; other failed Agent calls F`. The top line
    and the shared line carry the new cell unchanged in place (the shared line's `, moves N` keeps its rule).
R7. Unknown is never zero (FR-41): `refused` of a row is None when the row has agents and none was scanned, or when no
    session was read; a row with some unscanned agents keeps an int and its cell leads with `>=` (card A's rule, every part
    of the cell is a lower bound).
R8. The empty-journal output stays byte-identical; the "no nodes" test of `render_node_costs` (:1429) also counts the no-row
    refusals, so a window whose only facts are refusals prints its line instead of "no nodes".

## 3. Edges, each with its invariant

The brief's four edges first:
- E1 a refusal with no task line and no node (prompt without headers, non-str prompt, header_ids raising, a result whose
  tool_use id names no tool_use in the file) -> no-row `no_task`, printed `refused with no task or node line C`. INV: a
  refusal read from a readable session is counted exactly once -- in a row, a shared entry or a named no-row bucket --
  never dropped for lack of an id (the only drop is a no-row refusal dated before the window).
- E2 the same dispatch refused then passed (call y1 refused, call y2 with the same prompt passes, the hook writes its
  `delegated`) -> the row shows dispatches 1, redelegations 0, refused 1, moves 1. INV: a refusal is keyed by its tool_use
  id and a dispatch by its journal line; a refused call never becomes a dispatch, a redelegation or a priced line, and a
  passed call is never a refusal (its result has no `is_error`).
- E3 the refusal channel unreadable (session file missing, OSError/ValueError mid-pass, projects root absent) -> the
  session is unreadable, its refusals are dropped with its sends, its agents unscanned; no session read at all -> totals
  `refused` None and the line says `refused dispatches: cannot judge (no parent session read)`; a row none of whose agents
  was scanned prints `refused cannot judge`. INV: an unread channel never yields a measured `refused 0`.
- E4 the print (R6): the count sits inside the moves cell, right after `cost`, and in the top line and shared line exactly
  where moves sit. INV: wherever FG7-7 prints moves, the refused count is part of that figure (no second place to look,
  no moves figure that omits refusals).
Other edges:
- E5 duplicates: the uuid re-write, the `api-request-blob` copy of the tool_use and of the tool_result, the record's own
  `toolUseResult` string -> one refusal. INV: one tool_use id is one refusal; only `tool_result` blocks are read, never
  `toolUseResult`.
- E6 `isSidechain: true` refusal (a worker's own call) -> nowhere. INV: only the coordinator's calls are coordinator moves.
- E7 a non-refusal error on an Agent call (`is_error` true, text not the hook form: a user denial, an interrupt, a harness
  error) -> `failed`, never `refused` (F2). INV: `refused` holds only hook refusals; a change of the harness wording shows
  as `failed > 0` with `refused 0`, never as a silent drop of both.
- E8 a hook WARN on a passed call (`PreToolUse:Agent hook additional context: ...`, no `is_error`) -> nothing. INV: a call
  that went out is never refused, whatever text its result carries.
- E9 `is_error` true on a non-Agent tool (Bash, SendMessage) with any text -> nothing. INV: only Agent/Task calls (and an
  unpaired result in the hook form, E1) are dispatches.
- E10 task id and node both present and naming different rows -> the task's row. INV: the join order is task, then node;
  the node line never moves a refusal away from the task the journal knows.
- E11 a task id that resolves to no task, a node that is no window row -> `outside` when its ts is in the window. INV:
  a refusal never creates a row (rows come from the journal only, FG7-5).
- E12 a refusal on a shared task -> its shared entry's `refused` and `moves`. INV: I-3 of FG7-5 extended, each refusal once.
- E13 two refused calls with identical prompts -> 2. INV: every Agent call is one coordinator turn.
- E14 time: a mapped refusal counts with its row whatever its ts; transcript ts is UTC, journal ts local (FG7-6/7 §1.1).
  INV: the join never reads time; only the no-row window test does, day-granular.
- E15 temporal: the card builds on FG7-7 card A's `_nc_moves` / `send_targets`. World without them on the builder's base ->
  the builder stops and reports (no rebuild of card A). World with them -> R1-R8. INV: one moves definition, extended.
- E16 a session holding refusals but no found worker of the window -> not read (F4 scope); the scope is named in the
  `coordinator moves:` line. INV: the omission is printed, never implied complete.

## 4. Error directions (functions reused in a more consequential role)

- `dispatch_manifest.header_ids` (advice for the journal writer -> a join key of a count): may err towards NO id (a
  malformed or quoted header is skipped, never repaired) -> E1 bucket, never a wrong row by repair. Its prose fallback
  (`Task t-NNN` in the first chars) can name a wrong task only as it already does for the `delegated` line: the two stay
  equal (AR-15). Adversarial: header inside a fence or quote; `task: t-12x`; two `task:` lines (first wins); a 10 MB prompt.
- The refusal classifier: may err HIGH (another PreToolUse hook's refusal of an Agent call also counts: it is a refused
  dispatch too) and must never count a passed call. Safe side, each a test case or a stated non-case: `is_error` false
  with the hook prefix (E8); `is_error` true without it (E7); the prefix on a Bash result (E9); the blob copy (E5);
  `is_error` as the string "true" (not True -> not refused, it goes nowhere: the harness writes a JSON boolean).
- `transcripts.content_text`: a str as is, a list -> the `text` blocks joined; a dict/None -> None -> not the hook form ->
  `failed` when on an Agent id (E7), never refused.
- The `[command hook N]` index is never read: it is settings order (§1.1).

## 5. Builder card (R11-f)

### Card -- FG7-86 refused dispatches in the node moves (tools)

given: this spec §1-§4 (C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-86-refused-dispatch-count-card.md); C:/QAFactory/forge-repo/tools/forge_metrics.py::node_costs, ::_nc_moves, ::_nc_assemble, ::_nc_unscanned, ::_moves_cell, ::render_node_costs, ::_nc_new_day; C:/QAFactory/forge-repo/tools/transcripts.py::send_targets, ::first_copy, ::new_tool_uses, ::content_text, ::iter_lines, ::parse_line; C:/QAFactory/forge-repo/tools/dispatch_manifest.py::header_ids, ::section_cut; C:/QAFactory/forge-repo/tools/journal_keys.py::ref_key; C:/QAFactory/forge-repo/tools/test_forge_metrics.py::nc_world, ::_send, ::NC_CASES, ::NC_RENDERS, ::test_node_cost_import_stays_light; C:/QAFactory/forge-repo/docs/SIBLING_MAP.md axis 14 (:341); sample pair 8781f497-4108-4e80-a5a1-057d52d56b3a.jsonl lines 2722-2723 under C:/Users/i_mas/.claude/projects/C--QAFactory-forge-repo/
owns:
C:/QAFactory/forge-repo/tools/forge_metrics.py
C:/QAFactory/forge-repo/tools/transcripts.py
C:/QAFactory/forge-repo/tools/test_forge_metrics.py
C:/QAFactory/forge-repo/docs/SIBLING_MAP.md
non-goals: no journal event, schema or validator change; no hook or settings change; dispatch_gate.py and logs/dispatch_verdict.json untouched; no row created from a refusal; forge_metrics never imports hop_metrics and never parses a transcript itself; no money written to any file; no PROCESS edit; no commit (mechanism files: stage only, the Lead commits)
handoff: C:/QAFactory/forge-repo/docs/tasks/handoffs/20261118-fg7-86-refused-dispatch-count.md
edges: E1-E16 of the spec §3, each with its invariant; error directions §4
DoD: `python -m pytest tools/test_forge_metrics.py tools/test_transcripts.py "tools/test_mechanism_gate.py::test_b23_hop_metrics_is_outside_the_net_and_not_reached_by_the_closure" "tools/test_mechanism_gate.py::test_transitive_import_closure_of_live_wiring_is_covered_by_mechanism_prefixes" -q`
siblings: transcripts.py is the one transcript reader (axis 14 row: `send_targets` renamed `lead_calls`, sends + refused + failed in one pass); dispatch_manifest.header_ids is the one reader of a prompt's task/node (journal_hooks post-agent is the other consumer); forge_metrics node_costs is the one node cost; the weekly scout form reads the moves cell (PROCESS form `repeats`, unchanged text)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-86-refused-dispatch-count-card.md

Acceptance: R1-R8 of §2 hold. `transcripts.lead_calls` is stdlib only, no I/O at import, never raises, its docstring
states the directions (may count HIGH; an unreadable file is `error` with every list empty); `send_targets` has no other
caller left (Grep with a positive control in the report). `dispatch_manifest` is imported inside `node_costs` (I-2). The
axis 14 row names `lead_calls` and its one consumer. Witness: the DoD run's tail in the handoff. Tests, strongest first
(stop when test lines reach code lines; list the rest as `tests not written: <line> -- over budget`):

    test: tools/test_forge_metrics.py::NC_CASES row refused_then_passed_counts_once_each (main "sess": Agent tool_use y1 prompt "task: t-001", its tool_result is_error in the hook form, both also as api-request-blob copies; D("t-001","a1") passes; a refused call with a header-less prompt in the window; a refused sidechain call; an Agent call with is_error and a non-hook text; a passed call whose result carries "PreToolUse:Agent hook additional context" -> t-001 dispatches 1, redelegations 0, refused 1, moves 1; no_node refused no_task 1; failed 1) | expected from: spec §2 R1-R3 R5, E1 E2 E5-E8
    test: tools/test_forge_metrics.py::NC_CASES row root_absent_all_unscanned -- EDIT: also t-001 refused is None and totals refused is None | expected from: spec R7, E3
    test: tools/test_forge_metrics.py::NC_RENDERS row refused_cell_and_cannot_judge (NEW optional 5th tuple element `mains`, passed through `_nc_text`; a scanned row prints `1 (resumes 0, refused 1)` after cost; the no-node part prints `refused with no task or node line 1`) | expected from: spec R6, E4
    test: tools/test_forge_metrics.py::NC_CASES row refused_node_only_and_outside (a refusal with only "node: forge/7/FG7-9" joins row forge/7/FG7-9; "task: t-777" naming no task -> outside 1; a task and a node naming different rows -> the task's row) | expected from: spec R3, E10 E11
    test: tools/test_forge_metrics.py::NC_RENDERS rows six_accepted_top_is_five_with_reasons and moves_column_and_no_node_line -- EDIT of the expected cells to `moves 1 (resumes 0, refused 0)` and `>= 1 (resumes 0, refused 0, unscanned 1)` | expected from: spec R6
    test: tools/test_forge_metrics.py::test_node_cost_import_stays_light -- EDIT: the tuple also holds 'dispatch_manifest' | expected from: spec §1.2 I-2
    test: none for the empty journal -- NC_RENDERS row empty_journal is the witness, unedited | expected from: spec R8

## 6. Readers of every touched file

`tools/owns_readers.py` block: NOT attached to the brief (no shell here). The Lead runs `python -B tools/owns_readers.py
--paths tools/forge_metrics.py tools/transcripts.py tools/test_forge_metrics.py docs/SIBLING_MAP.md --names send_targets
lead_calls node_costs render_node_costs _nc_moves _nc_assemble _moves_cell` and the plan critic answers it (Q13 (d)).
Hand greps meanwhile (Grep tool, content mode, counts):

| file | reader (hand grep, count) | answer |
|---|---|---|
| tools/transcripts.py | `import transcripts` forms in tools/: 18 files, 33 hits (dispatch_gate, collect_intake, session_retro, journal_hooks, usage_report, journal_echo, session_context, tier_echo, hop_metrics, agent_budget, handoff_gate, permission_audit, handback_extract, forge_metrics + 4 tests); `send_targets` callers: forge_metrics.py:1255 only (Grep over tools/docs/.claude/.githooks/PROCESS; positive control: the same call finds `first_copy` in hop_metrics:408, session_retro:87) | unchanged for all but forge_metrics -- `first_copy`, `new_tool_uses`, `content_text` keep their contracts; forge_metrics changes in this card |
| tools/forge_metrics.py | importers: piles.py, piles_split.py, collect_intake.py, journal_validator.py (3), mechanism_gate.py (3), .githooks/pre-commit, pre-merge-commit, tests (journal_fresh_clone, journal_per_developer, journal_validator_merge, workflows, hop_metrics, forge_metrics): 14 files, 28 hits; `--node-cost` / node_costs: PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md (3: check 17(b) :523 reads `resumes`, 17(h) :545, form :1157-1164 `repeats` = the moves cell) | unchanged -- only `--node-cost` data/print change. Protocol: unchanged text; `repeats` now includes refusals (F1 lean), `>=`/cannot judge rows already go to `not measured:` (:1164) |
| tools/test_forge_metrics.py | CI only | changes in this card |
| docs/SIBLING_MAP.md | mechanism_gate.py `MAP_PATH` :207 (`parse_axes`); calibration checks 9, 12 (path liveness) | unchanged form -- one axis 14 row text |
| tools/dispatch_manifest.py (newly imported, not edited) | already imported by dispatch_gate, journal_hooks (:230) | unchanged |

## 7. Test cost (docs/TESTING.md)

Place: the existing tables `NC_CASES` / `NC_RENDERS` of `tools/test_forge_metrics.py` -- no new test file (Бюджет / Файлы).
Witness: two whole files plus two narrow node ids of `tools/test_mechanism_gate.py` (closure); none of the canon-only class
(Grep: `test_forge_metrics|test_transcripts` -> 0 in `ai-packages/qa-factory/scripts/slow_tests.json` and
`scripts/tests/test-layers.json`; positive controls in the same files: 134 `test_*.py` hits, 1 `canon_only`). Volume: three
new rows, four edited rows/asserts, one fixture element; the builder stops at the code-line count (Объём). Runtime of
`test_transcripts.py`: `estimate, not verified` -- the builder reports the `in N.NNs` tail.

## 8. Forks (returned, not decided)

- F1 where the count prints. (a) a separate `refused` column after `moves`, moves = redelegations + resumes unchanged;
  (b) refusals are part of moves: `moves = redelegations + resumes + refused`, the cell `N (resumes R, refused F)`
  (lean: the pile row's reason is "ходы координатора на узел их не видят"; the weekly form copies `repeats` from the moves
  cell (`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:1163`), so under (a) the review stays blind until a protocol edit outside
  this node's owns). Cost of (b): two expected strings of card A's tests change (§5).
- F2 what counts as refused. (a) only results in the hook form `PreToolUse:(Agent|Task) hook error`, every other `is_error`
  on an Agent call printed as `other failed Agent calls F` (lean: a wording drift of the harness shows, not silently 0);
  (b) every `is_error` Agent result is a refusal (simpler; a user denial or interrupt counts as a gate refusal); (c) the
  hook form only, the rest ignored (cheapest; a wording change drops refusals to 0 unseen).
- F3 a node whose every call was refused (no `delegated`, so no journal task). (a) no row; the refusals land in no-row
  `outside` / `no_task` (lean: rows come from the journal, FG7-5 I-3); (b) a row of kind `refused` with 0 dispatches --
  every row consumer (top list, form) meets a new kind.
- F4 scan scope. (a) the parent sessions FG7-7 reads (lean: one pass, FG7-7 F4 (a) decided; E16 names the gap); (b) every
  main transcript touched in the window -- sees sessions where nothing passed, at the cost of reading 200-700 MB files.
- F5 the refusal channel. (a) the Lead main transcript (lean: measured §1.1, history included, no schema); (b) a new
  append-only log written by `dispatch_gate.write_verdict` on refuse -- an enforcement-file change (Lead places it), a new
  carrier with readers, no history before it; (c) `logs/dispatch_verdict.json` -- rejected by measurement: one record,
  rewritten per dispatch (:1769).
- F6 a stale reader claim in another zone: `dispatch_gate.py:1716-1717` says `dispatch_verdict.json` is read by
  "session_context, calibration 17(g)"; Grep `dispatch_verdict` over tools/ finds critic_snapshot.py (4) and tests, none in
  session_context.py; PROCESS has no `dispatch_verdict` (positive control: `(g)` found at :328). (a) a finding for the
  dispatch_gate pile (lean: not this node's owns); (b) ignore.

## 9. Small choices closed by the designer

- Owns widened beyond the pile row (`forge_metrics.py`, `test_forge_metrics.py`) by `transcripts.py` and `docs/SIBLING_MAP.md`:
  AR-13 puts the transcript read in transcripts.py, and its axis 14 row names the function (rule 2: fixed by the card).
- `send_targets` renamed `lead_calls` (it no longer returns sends only; one caller). One pass, not a second function: the
  files are 200-700 MB.
- Join key of a refusal = its tool_use id; task id resolved by `journal_keys.ref_key` with an empty carrier (bare id ->
  undeclared label), like a critic token.
- An unpaired hook-form result (id not in the file) counts in `no_task`, never dropped (direction HIGH).
- Prefilter substrings are the matched fields themselves (`SendMessage`, `PreToolUse:`, `"Agent"`, `"Task"`): it may pass
  extra lines, never drop a matching one.

## 10. Noticed (not widened)

- The brief's fact cites `dispatch_gate.py` lines 22-44: that is the module docstring; the refusals are `main` :2141-2160,
  and a refusal does write one carrier (`logs/dispatch_verdict.json`, overwritten), just no `delegated` line.
- FG7-7 status: the pile row :32 still says `ожидает`, while card A's code (`_nc_moves` :1240, `send_targets` :530) is in
  the root tree and handoff t-1429 / review t-1433 exist. Whether it is on origin/main: `estimate, not verified`; the Lead
  runs `git -C C:/QAFactory/forge-repo log --oneline -1 -S _nc_moves origin/main -- tools/forge_metrics.py` (E15).
- 17(b) (:523) lists candidates by `resumes` only; refusals are not fix rounds and need no clause there.

## 11. Reading trail

Reads: batch-7 row :111 (and :31-32); FG7-6/7 card :1-110, :132-325; forge_metrics.py :1000-1499; test_forge_metrics.py
:1185-1469, :1536-1549; transcripts.py :489-573 and the def list; dispatch_gate.py :1-120, :1716-1819, :2085-2174 and its
`return 2` sites; journal_hooks.py :183-278 and the def list; dispatch_manifest.py imports, :343, :713, :872-901;
journal_keys.py `task_key`/`ref_key`/`display`; .claude/settings.json :14-35; test_mechanism_gate.py :1684-1696 and the
closure test names; PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md :1150-1167 and the `node-cost` hits; TESTING.md :75-106;
SIBLING_MAP.md :341 (the `send_targets` clause).
Measurements (Grep tool): the refused pair in 8781f497 lines 2722-2723 and copies 2763-2764 (`-o`); hook-form counts 149
(user form) / 213 (loose) / 0 (`[^2]`, same shape; control = the `[2]` form); `dispatch_verdict` in tools/ (5 files, 17
hits) and PROCESS (0, control `(g)` 7 hits); `send_targets|first_copy|new_tool_uses` readers; importers of transcripts and
forge_metrics; `node_costs|--node-cost` in PROCESS (3); slow_tests.json / test-layers.json (0 for the two witness files,
controls 134 / 1). A first Grep with a brace glob over the package scripts returned 0 for the control too: discarded as a
miscall and redone per file.
Needed beyond the manifest: transcripts.py, dispatch_manifest.py, journal_keys.py, test_forge_metrics.py,
test_mechanism_gate.py, settings.json, the protocol, TESTING.md, SIBLING_MAP.md, the Lead transcript 8781f497.

## 12. Lead decisions (Lead 501cb4e0, 2026-11-18)

- F1 (b): refusals are part of moves, the cell `N (resumes R, refused F)`.
- F2 (a): only the hook form counts as refused; every other is_error Agent result prints as `other failed Agent calls F`.
- F3 (a): no row for an all-refused node; it lands in outside / no_task.
- F4 (a): the parent sessions FG7-7 reads.
- F5 (a): the Lead main transcript is the channel.
- F6 (a): the stale reader claim at dispatch_gate.py:1716-1717 becomes a finding for the dispatch_gate pile (Lead).
- Parallel with FG7-89, which adds `transcripts.lines_back_to` next to `_read_back`: this node changes only `send_targets`/`lead_calls` and its own helpers; whoever lands second merges main.
