# FG7-7 + FG7-6 -- coordinator moves beside the node cost; the weekly scout cost-review form (DRAFT, designer t-1422)

Node: forge/7/FG7-7 (with forge/7/FG7-6), feature F19. Rows: `plans/piles/forge/batch-7-vhodyashchie-4.md:31-32`.
Findings: `plans/piles/forge/findings/20261104-khody-koordinatora-na-uzel-v-tsene.md` (FG7-7),
`plans/piles/forge/findings/20261104-nedelnyj-obzor-raskhoda-skautom-pered-kalibrovkoj.md` (FG7-6). Owner's word 04.11.2026
(direction chosen, both findings). This draft carries no money figure (P18; non-goal of the dispatch).

## 1. Target on main, measured (file:symbol)

| what | where | state |
|---|---|---|
| node cost | `tools/forge_metrics.py::node_costs` (:1231-1299), `::render_node_costs` (:1315-1375) | exists (FG7-5) |
| per-row counts | `tools/forge_metrics.py::_nc_counts` (:1182-1204): rejects, critic, redelegations (2nd+ non-critic `delegated` per task), replaced (`replaces_worker:` via `journal_validator.extract_replaces_worker`), escalations | exists |
| task_id-less lines | `tools/forge_metrics.py::_nc_tasks` (:1089-1091) `key is None -> continue`: dropped silently | gap (q7-4) |
| `returned` | `tools/forge_metrics.py` :86-89 (`UNCOUNTED_EVENTS`); validator `tools/journal_validator.py` :130-134: at most ONE `returned` per (task, worker_ref) | a resume can never leave a journal line |
| resume source | Lead main transcript `<projects>/<slug>/<session>.jsonl`: assistant `tool_use` `name: SendMessage`, `input.to` = agent id | measured, §1.1 |
| main-transcript dedupe | `tools/hop_metrics.py::_seen_before` (:405-414, uuid first copy wins, E32), `::_take_calls` (:417-427, one tool_use id once), `::session_index` (:450-473) | exists, private to hop_metrics |
| worker -> session | `tools/transcripts.py::main_transcript_of` (:489-498), `::find_agent_transcripts` (:111-128), `::agent_file_name` (:84-88, `AGENT_ID_RE` :44) | exists |
| protocol | `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` check 17 (:516-548) reads transcripts and journal; 17(b) "fix rounds run by a RESUMED worker (a `SendMessage` to a builder after a critic verdict) -- expected 0"; no scout report form; `--node-cost` never named (forge_metrics only at :986-988, attribution mode) | gap (q6-1..q6-3) |

### 1.1 Resume source -- the designer's measurement (the brief's question)

- `C:/Users/i_mas/.claude/projects/C--QAFactory-forge-repo/9408e840-5521-4070-9616-fa75174d792f.jsonl` line 448: a record
  `"type":"assistant","isSidechain":false`, block `tool_use` id `toolu_01PMJ1weQKsQoSbiiBVeLvn4`, `name: SendMessage`,
  `input.to: "a00a7a7403f471fe6"`; line 449 its tool_result ("queued for delivery ... If it finishes first, it is resumed").
- The same id maps to a task through the journal: `logs/journal/dev1.jsonl:2057` `delegated t-838 worker_ref
  agent:a00a7a7403f471fe6`; two more samples: `a6f43881d7aef64c1` -> `dev1.jsonl:2091` (t-856), `a90779f50de245f16` ->
  `dev1.jsonl:2094` (t-858). YES: SendMessage `to` == the `agent:<id>` of a delegated `worker_ref`.
- DUPLICATES: line 450 of the same file is a `"type":"api-request-blob"` record repeating the same tool_use id; every
  SendMessage id of that file sampled appears twice (448/450, 1580/1584, 1809/1820, 2660/2668, 2896/2900). Raw counts are
  therefore not moves: 951 `"name":"SendMessage"` hits over 11 main transcripts (Grep count) include these copies.
- NON-WORKER TARGETS: `input.to` may be a peer pipe `uds:\\.\pipe\LOCAL\cc-msg-...` (`0f83fb9a-...jsonl:342`,
  `1624cb4a-...jsonl:2780`, `1d2edd69-...jsonl:6241`); `agent_file_name` refuses it (`:` and `\` are outside `AGENT_ID_RE`).
- Ordering: the delegated line can be written AFTER the send (t-838: send 10:13Z, line 11:08 local; t-856 notes "retroactive"),
  and transcript `timestamp` is UTC `Z` while journal `ts` is local: the join must not use time.

## 2. Already done (not re-built)

- q7-1/q7-5: redelegations and replaced counted (`_nc_counts` :1198-1203), printed `redelegations N (replaced M)` (:1334, :1345).
- q7-6: tests `NC_CASES` row `replaced_and_escalated` (`tools/test_forge_metrics.py:1326-1329`), `NC_RENDERS` row
  `empty_journal` (:1374-1376). Open: q7-2/q7-3 (resumes), q7-4 (no-node line), q7-7 (their tests); q6-1..q6-3 (form, check).

## 3. Architecture (§1 lines)

- Package: not touched -> `variety: none -- forge tools and the calibration protocol only; no file under ai-packages/qa-factory/`.
  `tools/architecture_gate.py` is silent on these commits (no package path); no `judgment:` line is prescribed.
- AR-13 (one reader per fact): main-transcript records are read through `tools/transcripts.py` (SIBLING_MAP axis 14,
  closing rule: a new reader imports `transcripts`). Change check: grep for `"SendMessage"` / `isSidechain` / `uuids` readers
  in `tools/` with a positive control; the new survivor joins the axis 14 row.
- AR-15 (one survivor): the uuid-first-copy rule and the tool_use-id rule live today only in `hop_metrics` (§1). Card A
  lifts them into `transcripts.py`; `hop_metrics` delegates; `forge_metrics` calls them (F2). Change check: every site of the
  rule listed (hop_metrics :405-427 and the new reader), test_hop_metrics stays green unchanged.
- AR-29 / P27 census, every check this spec adds or alters:
  - `forge_metrics` moves/resumes/no-node/role rows: owner DATA (code joins and counts), class `xref` (journal x transcript join)
    and `shape`; a print, never a refusal (I-1 of FG7-5).
  - protocol 17(h) (i) presence of the report, (ii) its columns, (iii) no money: owner DATA, class `shape`; (iv) sampled token
    numbers equal the print: DATA, class `xref`; the verdict on cuts: owner JUDGMENT (the calibrator, a tier above the scout),
    class `meaning`, no code. The scout's "proposed cut" is ADVICE to that acceptor.
- Mechanism files: `tools/forge_metrics.py`, `tools/transcripts.py` (`tools/mechanism_gate.py` list :260, :280),
  `docs/SIBLING_MAP.md` (:220), `PROCESS/` (:221). Builders STAGE, the Lead COMMITS; the commit line form is
  `tools/mechanism_gate.py`'s own (not copied here).
- Import closure: `forge_metrics` is reached by a hook (`.claude/settings.json:132` compact_snapshot -> `compact_snapshot.py:428`
  `import piles` -> `piles.py:105` `from forge_metrics import`), and `tools/test_mechanism_gate.py:1691-1696` asserts
  `hop_metrics` is NOT in the hook closure (AST, nested imports count). So `forge_metrics` must never import `hop_metrics`.

## 4. Design

### 4.A FG7-7 -- coordinator moves per node

A1. Definition (finding item 1-2): `moves` of a row = `redelegations` (unchanged rule) + `resumes`. A node with one dispatch
    and no resume prints `moves 0`. `resumes` = distinct SendMessage tool_use calls of the Lead whose `input.to` equals the
    agent id of a delegated line of a task of the row. Every SendMessage is a move (a mid-run note and a resume alike: one
    Lead turn spent on a worker); the tool_result text that tells them apart is not parsed.
A2. Source (F1 recommended): the parent sessions' main transcripts via a new `transcripts.send_targets(path)`:
    one streaming pass (`iter_lines`), substring prefilter `"SendMessage"`, `parse_line`, only `type == "assistant"`, skip
    `isSidechain is True`, uuid first copy (`first_copy`), tool_use id once (`new_tool_uses`), keep blocks `name ==
    "SendMessage"` with a dict `input` whose `to` is a str -> `{"sends": [{"to", "ts", "line", "id"}], "error": None|str}`;
    an OSError sets `error`. Two primitives move from hop_metrics into transcripts (F2):
    `first_copy(seen: set, obj) -> bool` (hop_metrics `_seen_before` == `not first_copy`), `new_tool_uses(obj, seen_ids:
    set) -> list` (the tool_use blocks of `content_blocks(obj)`, a str id taken once, a block with no str id always
    returned). hop_metrics `_seen_before` and the id guard of `_take_calls` become calls of these; their behaviour is byte-
    identical.
A3. Scan scope (F4 recommended): the main transcripts `main_transcript_of(p)` of every worker transcript `p` found for the
    window's dispatches (the one `find_agent_transcripts` walk already done; `_nc_price_all` also returns `found`); each file
    once; a path that does not exist or returns `error` is an UNREADABLE session. The print names the scope.
A4. Join (no time, no text): `owner[aid]` = the task key of the FIRST delegated line (journal `seq` order, all tasks of the
    journal) whose `worker_ref` is `agent:<aid>` (`_agent_id`). A send with `agent_file_name(to) is None` is not a worker
    move and is counted nowhere. A send with a valid id: in `owner` -> `resumes[owner[aid]] += 1`; not in `owner` -> the
    no-node line, when its `ts[:10] >= ` the window day or `ts` is not a str.
A5. Unknown is never zero (FR-41): an agent of a row is UNSCANNED when its delegated `worker_ref` is not `agent:<id>`
    (`bad_ref`), its worker transcript was not found, or its session is unreadable. A row with U > 0 unscanned agents
    prints its moves as `>= N` and `resumes R (unscanned U)`.
A6. No-node line (F3 recommended): moves that reach no task -- (a) SendMessage to a valid agent id with no delegated line
    (A4), (b) `delegated` lines with no task_id whose `ts[:10]` is in the window (today dropped at `_nc_tasks` :1089-1091).
    Other task_id-less events (`dispatch_skipped`, `calibrated`, `lead_degraded`, `lead_restored`, `journal_created`) are
    not coordinator moves and are not counted.
A7. Data keys (`--json` too): row `resumes`, `resumes_unscanned`, `moves`; shared entry `resumes`, `moves`; totals
    `moves`, `no_node` = `{"sends": a, "delegated": b}`, `sessions` = `{"scanned": s, "unreadable": u}`, `roles` (A9).
A8. Print (beside the price, finding item 1): the table gains column `moves` right after `cost`, cell `N (resumes R)` or
    `>= N (resumes R, unscanned U)`; the top line gains `-- moves <cell>, rejects ...` (moves first after the `--`); a line
    after the `rows ...` line:
    `coordinator moves: redelegations + resumes (SendMessage in the parent sessions of the window's workers: scanned S,
    unreadable U); no node: N (SendMessage to an agent with no delegated line A; delegated lines with no task_id B)`.
    The shared line adds `, moves N` when N > 0. The empty-journal output stays exactly its two lines.
A9. Role rows (F5 recommended -- the producer FG7-6 needs; finding FG7-6 item 1 "по узлам и ролям"): a table after the
    top list, `| role | dispatches | tokens | cost |`, one row per `agent` value of the priced dispatches (rows + shared),
    sorted by tokens descending then name; the role tokens sum to the totals tokens; a missing/non-str `agent` is the
    role `unknown`. Printed only (P18), like the node table.

### 4.B FG7-6 -- the weekly scout cost-review form and the check that reads it

B1. A new section `## Weekly cost review (scout report form)` in the protocol, between the checklist and `## Closing out a
    run`, carrying: the dispatch (a scout before each calibration; question: "where does the window's spend go and what can
    be cut"; completeness: every row of the print read; `nothing to cut` is a valid outcome with the trail of rows read);
    `given:` = the stdout of `python -B tools/forge_metrics.py --node-cost --window <window start>`, run by the dispatcher
    and pasted into the dispatch (the scout has no shell: `.claude/agents/scout.md:5` `tools: Read, Glob, Grep`), plus
    `logs/journal/*.jsonl`; `handoff:` = `docs/tasks/specs/reports/cost-review-<YYYYMMDD>.md` (the scout folder,
    `tools/dispatch_manifest.py:215-220`; date = the window end).
B2. The report table, columns verbatim: `| row (node or role) | tokens | repeats | reason | proposed cut |`. `tokens` and
    `repeats` are copied from the print (`repeats` = its `moves` cell), never recomputed (finding item 2); `reason` cites
    journal facts by `file:line` (reject class, `replaces_worker:`, escalation) -- the scout's reading, not a verdict;
    `proposed cut` is advice. A print row with `n/d`, `>=` or unscanned resumes gets a line `not measured: <row> -- <why>`,
    never a 0. Money is never copied: the report is a repository file (P18).
B3. Check 17 gains (F8 recommended) `(h) Cost review input` (owner and class per §3): (i) the window's report exists -- absent:
    the finding line `cost review: absent for <window>` and the calibrator dispatches the scout by the form (F7); (ii) the
    five columns and, where the print had unknowns, `not measured:` lines; (iii) no money figure (a `$` followed by a digit)
    -- a hit is a finding (P18); (iv) the calibrator re-runs the same `--node-cost` window and compares the tokens of three
    rows -- a mismatch is a finding; the verdict on the cuts stays the calibrator's (the report is input, not a verdict).
    17(b) gains one pointer clause: candidates are the rows with `resumes` > 0 in the `--node-cost` print; whether a send
    was a fix round after a critic verdict stays the calibrator's reading.

## 5. Edges, each with its invariant

Card A:
- EA1 resume with no journal line (all of them: §1 `returned` once per pair) -> counted from the Lead transcript (A2-A4).
  INV: a move that left no journal line counts when its session is readable; otherwise the row prints `>=`, never a measured 0.
- EA2 send to a valid agent id with no delegated line -> no-node `sends`. INV: a send joins a row only through a delegated
  `worker_ref` equal to `agent:<to>`; never by prose, time or a guessed task.
- EA3 event with no task_id: `delegated` -> no-node `delegated`; other kinds not counted (A6). INV: no task_id-less line enters
  a row, and none vanishes silently if it is a move.
- EA4 empty journal -> output identical to the `empty_journal` row; no transcript is opened. INV: an empty journal prints
  `rows 0; dispatches 0 -- no nodes in the window` and the top line, nothing else.
- EA5 transcripts root absent (default `~/.claude/projects` missing; an explicit `--projects-root` that is not a directory stays
  exit 2, :1729-1732) -> no worker found, no session scanned, every row with an `agent:` dispatch is `>=`. INV: an absent
  root never yields `resumes 0` as measured.
- EA6 duplicate records (uuid re-write E32; `api-request-blob` copy; one tool_use id twice, §1.1) -> one send. INV: one
  tool_use id counts once; the first copy wins.
- EA7 `to` not an agent id (`uds:` peer pipe, §1.1) -> nowhere. INV: a message to a peer session is never a node move. A bare
  name that passes `AGENT_ID_RE` and maps to nothing lands in no-node `sends` (direction HIGH, named in the print scope).
- EA8 `isSidechain: true` record -> skipped. INV: a worker's own SendMessage is never the coordinator's.
- EA9 one agent id in delegated lines of two tasks -> its sends go to the task of its first line (A4). INV: every send
  counted at most once (row, shared entry or no-node line).
- EA10 a resumed worker that also got a second hand-written delegated line with the same id -> one redelegation + its
  resumes. INV: `moves` may err HIGH, never silently LOW (the cost's own direction, `_price_dispatch` docstring).
- EA11 send time vs window: a mapped send counts with its row whatever its ts (the row is kept whole, FG7-5); an unmapped
  send counts when `ts[:10] >=` window day or `ts` is absent. UTC vs local is a day-granular difference, accepted. INV: the
  join itself never reads time.
- EA12 session unreadable (missing file, OSError mid-pass) -> unreadable, its partial sends dropped, its agents unscanned.
  INV: no half number.
- EA13 shared task sends -> its shared entry, never a row. INV: I-3 of FG7-5 extended -- each move counted once.
- EA14 I-1/I-2 of FG7-5: nothing written; `transcripts` still imported inside `node_costs` (test `test_node_cost_import_stays_light`
  stays green); `forge_metrics` never imports `hop_metrics` (§3). INV: the hook closure is unchanged.
- EA15 role `agent` missing or non-str -> role `unknown`. INV: role tokens sum to the totals tokens.

Card B:
- EB1 no report that week -> 17(h)(i) finding line; the calibrator dispatches the scout (F7). INV: an absent report is never
  read as "nothing to cut".
- EB2 money in the report -> finding. INV: no repository file carries a money figure (P18).
- EB3 print unknowns -> `not measured:` lines. INV: an unknown is never a 0 in the report.
- EB4 "nothing to cut" -> valid with the trail of rows read. INV: an empty table without a trail is not a review.
- EB5 temporal: the form names the `moves` column card A creates. Before A merges the print has none -> card B lands after
  card A (or in the same wave, A first). INV: the form never names a column the print lacks on main.
- EB6 the new text restates no hand-back rule words (`tools/test_handoff_rule_anchors.py` `RESTATED` :26) and cites no
  `path:N` line anchors. INV: check 28's anchors and the pointer-only rule hold.

## 6. Builder cards (R11-f)

### Card A -- FG7-7 coordinator moves (tools)

given: this spec §1-§5 (C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-6-fg7-7-coordinator-moves-card.md); C:/QAFactory/forge-repo/tools/forge_metrics.py::node_costs, ::_nc_price_all, ::_nc_tasks, ::_nc_counts, ::_nc_row, ::render_node_costs; C:/QAFactory/forge-repo/tools/transcripts.py::main_transcript_of, ::find_agent_transcripts, ::agent_file_name, ::content_blocks, ::parse_line, ::iter_lines; C:/QAFactory/forge-repo/tools/hop_metrics.py::_seen_before, ::_take_calls; C:/QAFactory/forge-repo/tools/test_forge_metrics.py::nc_world, ::NC_CASES, ::NC_RENDERS; C:/QAFactory/forge-repo/docs/SIBLING_MAP.md axis 14
owns:
C:/QAFactory/forge-repo/tools/transcripts.py
C:/QAFactory/forge-repo/tools/hop_metrics.py
C:/QAFactory/forge-repo/tools/forge_metrics.py
C:/QAFactory/forge-repo/tools/test_forge_metrics.py
C:/QAFactory/forge-repo/docs/SIBLING_MAP.md
non-goals: no journal schema or validator change (no new event); no hook; forge_metrics never imports hop_metrics; no refused-dispatch count (F6); no money written to any file; no commit (mechanism files: stage only, the Lead commits)
handoff: C:/QAFactory/forge-repo/docs/tasks/handoffs/20261118-fg7-7-coordinator-moves.md
edges: EA1-EA15 of the spec §5, each with its invariant
DoD: `python -m pytest tools/test_forge_metrics.py tools/test_hop_metrics.py tools/test_transcripts.py -q`
siblings: transcripts.py is the one transcript reader (axis 14: the new `first_copy`, `new_tool_uses`, `send_targets` join its row "The one reader"; hop_metrics becomes their consumer); forge_metrics `node_costs` is the one node cost; calibration check 17 reads the moves (card B)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-6-fg7-7-coordinator-moves-card.md

Acceptance: A1-A9 of §4.A hold; `transcripts.py` gains `first_copy`, `new_tool_uses`, `send_targets` (stdlib only, no I/O at
import, docstrings state the error direction: may count HIGH, an unreadable file is `error`, never a raise from
`send_targets`); `hop_metrics._seen_before` and the id guard of `_take_calls` call them and test_hop_metrics passes unedited;
the axis 14 row "The one reader" names the three functions and their two consumers; `nc_world` gains an optional `mains`
argument ({session: [records]} written as `projects/proj/<session>.jsonl`). Tests, strongest first (budget: stop when test
lines reach code lines and list the rest as `tests not written: <line> -- over budget`):

    test: tools/test_forge_metrics.py::NC_CASES row resumes_from_parent_session (t-001: one dispatch a1, two distinct sends to a1, one of them also re-written under its uuid and copied as an api-request-blob, a send to a `uds:` pipe, a sidechain send, a send to a9 with no delegated line; t-002: one dispatch, no send -> t-001 resumes 2 moves 2, t-002 moves 0, no_node sends 1) | expected from: spec §4.A A1-A4, EA2 EA6-EA8; finding FG7-7 items 1-2
    test: tools/test_forge_metrics.py::NC_RENDERS row moves_column_and_no_node_line (a row with an agent whose transcript is absent prints `>= 1 (resumes 0, unscanned 1)` in the column after cost; a task_id-less delegated line in the window gives `delegated lines with no task_id 1` and joins no row) | expected from: spec §4.A A5 A6 A8, EA1 EA3
    test: tools/test_forge_metrics.py::NC_CASES row root_absent_all_unscanned (projects path missing -> sessions scanned 0, every agent row `resumes_unscanned` > 0, no row has a measured resumes 0) | expected from: spec EA5
    test: tools/test_forge_metrics.py::NC_CASES row role_rows_sum_to_total (two roles; role tokens sum to totals tokens; a dispatch with no `agent` is role `unknown`) | expected from: spec §4.A A9, EA15
    test: tools/test_forge_metrics.py::NC_RENDERS row six_accepted_top_is_five_with_reasons -- EDIT of the expected top line to carry `-- moves 1 (resumes 0), rejects ...` | expected from: spec §4.A A8
    test: none for the hop_metrics delegation -- internal boundary, behaviour unchanged; witness: tools/test_hop_metrics.py green unedited | expected from: spec §4.A A2
    test: none for the empty journal -- existing NC_RENDERS row empty_journal is the witness, unedited | expected from: spec EA4

### Card B -- FG7-6 cost-review form and check 17(h) (protocol)

given: this spec §4.B, §5 EB1-EB6 (C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-6-fg7-7-coordinator-moves-card.md); C:/QAFactory/forge-repo/PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md check 17 and `## Closing out a run`; C:/QAFactory/forge-repo/.claude/agents/scout.md (tools line); C:/QAFactory/forge-repo/tools/test_handoff_rule_anchors.py (RESTATED); card A's merged print (dependency EB5)
owns:
C:/QAFactory/forge-repo/PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md
non-goals: no code; no scout role edit; no money figure in the protocol; no other check renumbered or reworded beyond 17(b)'s one pointer clause; no commit (PROCESS/ is a mechanism path: stage only)
handoff: C:/QAFactory/forge-repo/docs/tasks/handoffs/20261118-fg7-6-cost-review-form.md
edges: EB1-EB6 of the spec §5, each with its invariant
DoD: `python -B <scratchpad>/keys_fg7_6.py PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` exit 0, the same with the extra argument `NEGATIVE-CONTROL-KEY-ABSENT` exit 1, and `python -m pytest tools/test_handoff_rule_anchors.py -q`
siblings: check 17 is the cost-gates slot (one place for cost checks); check 34 reads hop_metrics, unchanged; the scout handoff folder is `tools/dispatch_manifest.py` HANDOFF_DIRS, not restated
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-6-fg7-7-coordinator-moves-card.md

Acceptance: B1-B3 of §4.B in the protocol. The witness script (DOC-DISPATCH, attached in full in the report, never committed;
keys quoted verbatim from this DoD, written before the run):

    import pathlib, sys
    KEYS = ["## Weekly cost review (scout report form)",
            "| row (node or role) | tokens | repeats | reason | proposed cut |",
            "not measured:", "python -B tools/forge_metrics.py --node-cost --window",
            "docs/tasks/specs/reports/cost-review-", "(h) Cost review input", "nothing to cut",
            "cost review: absent for"]
    text = " ".join(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8").split())
    missing = [k for k in KEYS + sys.argv[2:] if " ".join(k.split()) not in text]
    print("missing:", missing or "none")
    sys.exit(1 if missing else 0)

    test: none -- document; DOC-DISPATCH witness by the keys above with a negative control | expected from: spec §4.B B1-B3; finding FG7-6 items 1-3

## 7. Readers of every touched file

`tools/owns_readers.py` block: NOT attached to the brief. The Lead runs `python -B tools/owns_readers.py --paths
tools/transcripts.py tools/hop_metrics.py tools/forge_metrics.py tools/test_forge_metrics.py docs/SIBLING_MAP.md
PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md --names node_costs render_node_costs _nc_price_all _seen_before _take_calls
first_copy new_tool_uses send_targets` and the plan critic answers it (Q13 (d)). Hand greps meanwhile (Grep tool, `tools/`):

| file | reader (hand grep, count) | answer |
|---|---|---|
| tools/transcripts.py | importers: tier_echo, session_context, journal_echo, dispatch_gate, forge_metrics, journal_hooks, handoff_gate, handback_extract, permission_audit, session_retro, hop_metrics, agent_budget, usage_report, test_hop_metrics (14 files, `import transcripts` forms); test_transcripts.py (52 hits) | unchanged -- additive functions only; hop_metrics, forge_metrics change in card A |
| tools/hop_metrics.py | test_hop_metrics.py; test_mechanism_gate.py:116, :1691-1696 (outside the net, not in the hook closure); calibration check 34; SIBLING_MAP :176 | unchanged output; the closure test holds because forge_metrics does not import it (EA14) |
| tools/forge_metrics.py | piles.py:105, collect_intake.py:49, piles_split.py:39, test_journal_fresh_clone.py:27, test_forge_metrics.py; `.githooks/pre-commit` (2), `pre-merge-commit` (1) run the attribution mode; mechanism_gate.py:260, :281; `node_costs`/`render_node_costs` read only in forge_metrics and its test (Grep count 12/12) | unchanged -- only `--node-cost` output and data change; changes in card A |
| tools/test_forge_metrics.py | CI only | changes in card A |
| docs/SIBLING_MAP.md | mechanism_gate.py `MAP_PATH` :207 (`parse_axes`); calibration checks 9, 12 (path liveness) | unchanged form -- one axis 14 row text, card A |
| PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md | test_handoff_rule_anchors.py (RESTATED, check 28 anchors); warn_density.py:429-439 (`WARN LAYER DENSITY` block); install_parity_anchors.json:396-403 (title, checklist heading, check 1 line); test_quarantine.py:51 (carrier path); test_claim_control_gate.py, test_mechanism_gate(_md).py (path strings); dispatch_gate.py:1438-1441 (CHK anchors: 0 in this file) | unchanged -- no anchored line edited; changes in card B |

## 8. Test cost (docs/TESTING.md)

Layer: the existing case tables `NC_CASES` / `NC_RENDERS` of `tools/test_forge_metrics.py` (layer 3 table of the module) --
no new test file (Бюджет / Файлы). Witness files: three whole files, none slow or `canon_only` (no `test_forge_metrics`,
`test_hop_metrics`, `test_transcripts` in `ai-packages/qa-factory/scripts/slow_tests.json` or `test-layers.json` `canon_only`,
both read with a positive control). Volume: four new rows, one edited row, one fixture argument -- the builder stops at the
code-line count (Объём). Runtime of `test_hop_metrics.py`: `estimate, not verified` -- the builder reports the `in N.NNs` tail.
Card B: no test file; the DOC-DISPATCH witness and one existing reader test.

## 9. Forks (returned, not decided)

- F1 resume source. (a) Lead main transcripts via `transcripts.send_targets` (recommended: measured §1.1, no schema change,
  the same local-transcript dependency the node cost already has); (b) a new journal event (`resumed`) written by a
  PostToolUse hook on SendMessage -- validator, hook and hooks wiring change, and history before it stays uncounted;
  (c) both. The finding's "резюме воркера (SendMessage) как события" reads either way.
- F2 dedupe road. (a) lift `first_copy` / `new_tool_uses` into transcripts.py, hop_metrics delegates (recommended: one
  survivor, AR-15); (b) a separate reader in transcripts.py with its own dedupe, hop_metrics untouched -- two roads for one
  rule (rule 6 defect); importing hop_metrics from forge_metrics is closed by `test_mechanism_gate.py:1691-1696`.
- F3 the no-node line. (a) moves only: unmapped sends + task_id-less `delegated` (recommended); (b) every task_id-less
  journal event by kind (`dispatch_skipped` 304 lines, 2 with task_id; most are Lead self-execution, not a move toward a
  worker).
- F4 scan scope. (a) parent sessions of the window's found workers (recommended: bounded; precedent hop_metrics
  "scanned: parent sessions only"; a session that journaled no worker is invisible to the no-node line); (b) every
  `<root>/*/*.jsonl` main transcript touched in the window -- complete no-node line, cost of reading 200-700 MB files
  (`transcripts.iter_lines` docstring) for every session.
- F5 role rows. (a) node rows only; the form's role rows are `not measured: no producer`; (b) `node_costs` adds role rows
  (A9) in card A (recommended: FG7-6 asks "по узлам и ролям" and a named producer must own it, rule 6).
- F6 dispatch-gate refusals (the FG7-7 witness: "два отказа dispatch_gate") create no delegated line, so the chosen two
  sources do not count them. (a) keep the owner's two sources and offer a separate pile row for refused Agent calls
  (recommended: the owner chose the direction 04.11.2026); (b) count refused Agent calls in the same pass (a tool_result
  `is_error` on an Agent call, mapped by the dispatch's `task:` line) in card A.
- F7 absent report at calibration. (a) a finding line and the calibrator dispatches the scout (recommended: the review
  stays off the dear tier, the finding's point); (b) a finding line only, the calibration proceeds without the input.
- F8 where the check lives. (a) 17(h) in Cost gates (recommended: the finding names cost gates; one slot); (b) a new check 50.

## 10. Small choices closed by the designer

- Report path `docs/tasks/specs/reports/cost-review-<YYYYMMDD>.md`, date = window end (the scout folder is fixed by HANDOFF_DIRS).
- Form section placed before `## Closing out a run`; 17(b) gets a pointer clause only.
- `moves` column right after `cost` (the finding: "рядом с ценой"); `resumes` folded into the `moves` cell, not a column.
- Sends counted per tool_use id; the "queued vs resumed" tool_result text is not parsed (A1).
- Agent->task join by the first delegated line (mirrors the cost's first-line rule, `same_worker`).
- Two cards with disjoint owns; card B after card A (EB5).

## 11. Noticed (not widened)

- 17(b) expects 0 resumed fix rounds while A1 counts every send: the new number is a candidate list for 17(b), not its verdict.
- Old `cli:` worker_refs make many historical rows `>=` (unscanned): honest under FR-41, noisy for windows before the hook era.

## 12. Reading trail

Reads: batch-7 rows :31-32; both findings whole; forge_metrics.py :80-99, :1005-1384, :1717-1746; test_forge_metrics.py
:100-111, :1185-1414, :1486-1495; transcripts.py :1-130, :186-215, :266-301, :486-505; hop_metrics.py :1-100, :300-479;
journal_validator.py :126-137, :286-295; journal_keys.py `task_key`/`node_of` (Grep -A14); protocol :1-30, :505-554,
:1150-1164; test_mechanism_gate.py :1680-1697 and its closure helpers (:966-1019); test_mechanism_gate_md.py :125-136;
test_handoff_rule_anchors.py :1-45; warn_density.py :425-439; install_parity_anchors.json :390-403; dispatch_gate.py :1430-1449;
architecture.md :60-73, :173-220; TESTING.md :36-150, :213-250; SIBLING_MAP.md axis 14 (:337-353).
Measurements (Grep tool): SendMessage counts in `C:/Users/i_mas/.claude/projects/C--QAFactory-forge-repo/*.jsonl` (951 over 11
files); 9408e840 lines 448-450 read whole; tool_use id duplicates (`-o`, 10 lines); `uds:` targets (8 lines, 3 files);
`agent:<id>` of three samples in `logs/journal` (3 hits, dev1.jsonl:2057/2091/2094); `"event":"dispatch_skipped"` 303/304
(two forms), with task_id 2; `"event": ?"decomposable"` 0 in `logs/` (positive control: the same form finds 304
dispatch_skipped); scout tools line; HANDOFF_DIRS; importers of forge_metrics/piles/transcripts; slow_tests.json /
test-layers.json have no hit for the three witness files (positive control: 134 `test_*.py` hits, `canon_only` found);
`.githooks` has no protocol hit (positive control: `forge_metrics` 3 hits there); no `toolkit/PROCESS` copy in this repo
(positive control: the same Glob found `design/architecture.md`).
Needed beyond the manifest: hop_metrics.py, journal_validator.py, journal_keys.py, test_mechanism_gate*.py, architecture.md,
TESTING.md, SIBLING_MAP.md, scout.md, dispatch_manifest.py, settings.json, the Lead transcripts listed above.

## 13. Lead decisions (18.11, Lead 501cb4e0, accepted)

- F1 (a) the Lead main transcripts via `transcripts.send_targets`; no new journal event. F2 (a) `first_copy` / `new_tool_uses` lift into transcripts.py, hop_metrics delegates. F3 (a) moves only. F4 (a) parent sessions of the window's found workers. F5 (b) node_costs adds role rows (A9) in card A. F6 (a) refused dispatches stay out of card A; a separate pile row for them. F7 (a) a finding line and the calibrator dispatches the scout. F8 (a) 17(h) in Cost gates.
- Order: card A first; card B after A merges (EB5).
