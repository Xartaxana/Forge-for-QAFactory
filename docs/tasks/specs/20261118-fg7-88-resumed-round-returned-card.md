# FG7-88 - journal: a resumed worker's round is journaled, so the FG7-22 WARN sees a verdict before the round's end; Q2 critic:<id> basis (draft card)

task: t-1467 · node: forge/7/FG7-88 · feature: F19 · designer draft, 18.11.2026 · the Lead decides (forks in section 9)

Pile row: `plans/piles/forge/batch-7-vhodyashchie-4.md:113`. Parent: `docs/tasks/specs/20261118-fg7-22-accept-before-last-worker-line-card.md`
(§3 E3, §9 F1 (c), §12: the Lead sent E3 and Q2 here).

## 0. Target on main, measured (designer, Read/Grep; positive controls named)

| # | fact | carrier |
|---|---|---|
| M1 | The stop side writes `returned` once per `delegated`: `_find_delegated` returns `done=True` after any `returned` of the last delegated with that ref and task; `_record_returned` then returns with no write (`if done:` drops the index and marker). | `tools/journal_hooks.py::_find_delegated` :116-126, `::_record_returned` :406-410; test `tools/test_journal_hooks.py:287-292` (second stop: one returned) |
| M2 | Rule 9f refuses a second `returned` per (task, worker_ref) (`returned_pairs`), and any `returned` on a task closed by `accepted`. | `tools/journal_validator.py::validate_new_lines` :1148-1162, :1218-1237 |
| M3 | The FG7-22 WARN keeps `returned_refs` as a set: once (task, ref) is in it, no line takes it out. The docstring names the miss: "KNOWN MISS (E3): a RESUMED worker has one `returned` from its first stop". | `journal_validator.py::returned_order_warnings` :795-835; docstring item 21 :245-251 |
| M4 | **Consequence of M1-M3 (the load-bearing finding):** writing a second `returned` at the second stop ALONE does not let the WARN see "a verdict before round 2 ended": at the verdict the journal holds `returned` #1 (the WARN is silent), and after an `accepted` rule 9f refuses `returned` #2. The WARN can only see it if something marks the round as OPEN AGAIN before the verdict: the resume itself. | derived from M1-M3 |
| M5 | No hook watches SendMessage: the PostToolUse matchers are `Edit\|Write\|MultiEdit\|NotebookEdit\|Bash\|PowerShell`, `Bash\|PowerShell\|Grep\|Glob\|Read`, `Task\|Agent` (twice). | `.claude/settings.json` :65-106 |
| M6 | SendMessage's input field `to` is read from real transcripts by `transcripts.send_targets` (:530-550); `forge_metrics._nc_moves` joins `to` to a task ONLY through a `delegated` with `worker_ref` `agent:<to>`; "a send to a non-agent id (a peer pipe) is a move nowhere". | `tools/transcripts.py:546`; `tools/forge_metrics.py:1240-1269` |
| M7 | `EVENTS` is a closed set; an event outside it is a FAIL (rule 3). `TASK_ID_REQUIRED_EVENTS`; rule 12 requires `worker_ref` for `delegated`/`returned`. | `journal_validator.py:295-301`, :914-920, :985-995 |
| M8 | RESULT PENDING: `session_context.open_dispatch_lines` marks an open dispatch pending iff the task key's latest `returned` is later than the open entry; `compact_snapshot` marks it on ANY `returned` of (task, ref), with no order check. | `tools/session_context.py:640-653`; `tools/compact_snapshot.py:605-611` |
| M9 | The index entry `open/<id>` is dropped after a written `returned` (:413-414); `_locate` falls back to scanning the last `SCAN_LINES` = 3000 lines of every worktree copy. | `journal_hooks.py:43`, :420-440 |
| M10 | The critic basis is compared exactly: `basis == "critic"` in the matrix (:707), in the echo R3 (`journal_echo.py:2193`), in `r3_integration_check.py:238`. Live journal: `accepted` with `"basis":"critic:t-` 67 lines, with `"basis":"critic"` 236 (all passed, so by rank); `returned` 518. | Grep counts on `logs/journal/dev1.jsonl` (both patterns found lines) |
| M11 | Mechanism files (builder stages, the Lead commits): `journal_validator.py` (:251), `session_context.py` (:228), `compact_snapshot.py` (:259), `journal_hooks.py` (:291). | `tools/mechanism_gate.py` |
| M12 | Free rule letter: `9h` 0 hits in `tools/*journal*.py` (control `9f`, same glob: 9 hits). `9g` is used in test names. | Grep |
| M13 | Test places: `test_journal_validator.py::RETURNED_ROWS` :1640 (rule 9f; row `twice-for-one-pair` :1647), `::RETURN_ROWS` :690, `::MATRIX_ROWS` :541; `test_session_context.py::test_result_pending_and_the_returned_that_never_closes` :1754 (inline table); `test_compact_snapshot.py::test_the_open_list_marks_a_dispatch_whose_worker_returned_and_a_returned_never_closes_it` :850; `test_journal_echo_r3.py` (single tests, S1/M2 :106-227); `test_r3_integration_check.py`. No test file is canon class (package `slow_tests.json`/`test-layers.json` name only the package `test_hooks_wiring.py`). | Grep |

Estimates (no shell; the Lead measures in L0, section 5): X1 - PostToolUse fires for SendMessage with `tool_input.to`,
`session_id`, `cwd`. X2 - SubagentStop (dod_gate) fires on a resumed worker's later stop with the same `agent_id` (the
brief's fact says the second stop "finds the pair closed", which implies it; not measured by me). X3 - a PostToolUse payload
of a call made inside a worker carries `agent_id`. `estimate, not verified`.

## 1. Architecture

No `ai-packages/qa-factory/` path: AR-n named by analogy (as FG7-22); `census: n/a -- forge tool`.

- AR-22 (every field read has a producer): the new `resumed` line is read by rule 9f/9h, the FG7-22 WARN, RESULT PENDING
  (session_context, compact_snapshot) and the stop side. Producer: `journal_hooks.post_send` (card A owns it), activated by
  the Lead's settings entry (L1); hand door: `python -B tools/journal_write.py event --json`. Change check (DoD): the
  docstring of item 21 and the 9h text name both.
- AR-13/15 (one rule, one survivor): what opens/closes a round is ONE helper in the validator (`_round_step`), used by
  `validate_new_lines` and `returned_order_warnings`; the hook's `_find_delegated` gets the same rule in 2 lines, and the
  card-A row "resume-then-stop" binds the two (the hook's write passes the validator through the one writer).
- AR-18: hook lines are of the `JOURNAL: <event> ...` family; the WARN text of FG7-22 is unchanged.
- AR-29 owners: 9h (FAIL) and the 9f change judge journal FORM and a JOIN - owner data (code); the WARN - data (code);
  Q2 matrix - data (code) on the basis's form; whether the critic's verdict was right stays the Lead's judgment.
- AR-2: the hook never blocks (exit 0 always); every FAIL names its door.

`variety: none -- a forge journal tool outside the package; no project, language or tracker axis is met`.
One road (rule 6): every worker kind, every acceptor and every path (hook write, commit, merge, CI `--all`) reaches the
same round rule; the three readers of the critic basis read ONE grammar (F6 (b)).

## 2. Design (written for F1 (a), F2 (a), F3 (b), F4 (a), F5 (a), F6 (b) - the recommendations)

### 2.1 Producer: `journal_hooks.post_send(payload) -> list[str]` (mode `post-send`; PostToolUse SendMessage)

Never raises, exit 0; output like `post-agent` (one `additionalContext` joined by ` | `), nothing when the list is empty.
In order, each step's "no" returns `[]` (silent: a send that is not a resume owes nothing):
1. payload is a dict, `tool_input` a dict, `to = tool_input["to"]` a str with `transcripts.agent_file_name(to)` not None.
2. the payload carries no `agent_id` (a send made inside a worker is not the coordinator's resume; X3).
3. `root = jw.repo_root(cwd)`; `ref = f"agent:{to}"`; `state = _locate(jw, jk, root, to, ref)` is not None.
4. F3 (b): the delegated's `session` and `_session(payload)` are equal, or one of them is absent.
5. the task has no `accepted` line in that copy's tail (`_tail_objs(copy)`), and the pair's round is CLOSED
   (`_find_delegated(...)[1]` is True: a `returned` since the last start). An open round = the worker is running or its
   stop is not journaled yet: the send is a course correction, not a new round.
6. write `{"event": "resumed", "task_id", "agent", "model" (when the delegated has it), "worker_ref": ref,
   "notes": cut_notes(f"{ref} resumed by SendMessage"), "session" (when known)}` into `_root_of_journal(copy) or root`
   through `jw.write_event(..., via="hook", lock_timeout=HOOK_LOCK_TIMEOUT)`. Written -> `_write_index(root, to, copy)` and
   `JOURNAL: resumed <task> written (<path>:<line>)`. Refused -> `JOURNAL: resumed NOT written for <ref> -- <messages>;
   write it: python -B tools/journal_write.py event --json '<the line>'` (the line cut by `one_line`).
An exception anywhere -> `[f"JOURNAL: resumed NOT checked for agent:{to} -- the hook failed ({type})"]`. The module
docstring gains the `post-send` line; the `main` timeout branch stays silent for `post-send` (as `pre-edit`).

### 2.2 Stop side

`_find_delegated`: a `resumed` line with the same ref and the found delegated's task sets `done = False`. Nothing else in
`_record_returned`, `_write_returned`, `post_agent` changes: a second stop with no `resumed` since is still idempotent (M1).

### 2.3 Validator (`tools/journal_validator.py`)

- `EVENTS` and `TASK_ID_REQUIRED_EVENTS` gain `resumed`; rule 12's `worker_ref` check covers `resumed`. `model` is not
  required (small choice 3).
- `_round_step(open_pairs: dict, obj) -> None`, pure: a `delegated` with a non-blank ref sets `(task, ref)` open ONLY if the
  pair was never seen; a `returned` sets it closed; a `resumed` sets it open. Refs stripped. A journal with no `resumed`
  line gives exactly today's states (one round per pair).
- Rule 9f (F2 (a)): "one `returned` per ROUND": the refusal `already has a returned for worker_ref` fires when the pair is
  seen and closed; the text adds `and no resumed since`. The closed-task and no-delegated branches are unchanged.
- Rule 9h (new, `resumed`; valid task id): refused when the task is closed by an `accepted`; when no earlier delegated of
  the task carries that ref; when the pair's round is open ("the worker has not returned since its last start, so this
  send is not a new round -- drop the line"). Door in the text: `python -B tools/journal_write.py event --json`. A refused
  line still enters the state (as 9f does today), so one bad line gives one refusal.
- `returned_order_warnings`: on a `resumed` with a str `agent`, a ref and `ts[:10] >= RETURNED_WARN_FROM`:
  `owed[tid][agent] = ref` and `returned_refs.discard((tid, ref))`. The WARN text is unchanged.
- Docstring: rule 9f says "per round"; rule 9h added; item 21's KNOWN MISS sentence becomes "a RESUMED worker is owed
  again from its `resumed` line (FG7-88; producer journal_hooks.post_send); a resume the hook could not tie (E8 race, a
  copy beyond the scan) stays silent".

### 2.4 RESULT PENDING

`session_context.open_dispatch_lines`: gather `resumed_last[key]` like `returned_last`; pending iff
`back > max(open entry's (ts, pos), resumed_last.get(key))`. `compact_snapshot`: the open-list mark shows only when the
pair's latest `returned` is later in file order than its latest `resumed`. Displays and their words are unchanged.

### 2.5 Q2 - `critic:<task id>` (card B)

`journal_validator.critic_basis(basis) -> tuple[bool, str | None]`: `(True, None)` for exactly `"critic"`; `(True, tid)`
for `"critic:" + tid` with `TASK_ID_RE.fullmatch(tid)`; `(False, None)` for anything else, a non-str included. Readers:
`_matrix_d0058_violation` branch 5 (same position), `journal_echo._check_accepted_r3` (S1: confirmed also when the cited id
is in `critic_task_ids`; else M2 phantom), `r3_integration_check` (`is_basis_critic`; lazy import, exact compare when the
validator cannot be imported). The generic FAIL text names `'critic:<critic task id>'` beside `'critic'`.

## 3. Edges, each with its invariant

| id | edge | behaviour | invariant it protects |
|---|---|---|---|
| E1 | brief edge 1: a resumed worker stops again | journal: `delegated, returned, resumed, returned`; the second `returned` is the ordinary form, read by 9f and the WARN | a round's end is journaled once per round, in the one form every reader already reads |
| E2 | brief edge 2: a resume that never stops again | no FAIL, no marker, no prune WARN, nothing at commit; a verdict written while that round is open draws the FG7-22 WARN; door: the CLI `returned` (legal: the round is open) | a resume owes the validator nothing; a verdict on an unfinished round is never silent (F4) |
| E3 | brief edge 3: a send that is not this coordinator's resume - `to` a peer pipe or any id with no `agent:<to>` delegated; a delegated of another session (F3 (b)); a send from inside a worker | no line, silent | a round exists only for a worker this session launched: an unknown never writes |
| E4 | brief edge 4, TEMPORAL: lines before the change; before the Lead's settings entry no `resumed` exists | old lines are never judged (append-only); with no `resumed` line `_round_step` yields one round per pair, so 9f, the WARN and RESULT PENDING read every existing journal exactly as today (`twice-for-one-pair` stays a FAIL). World 1, code committed, entry absent: nothing writes `resumed`, behaviour = today. World 2, entry present: lines appear. The move that creates it: L1 after the commit; an entry before the code finds `post-send` an unknown mode (writes nothing, `test_the_unknown_mode...` :308) | the change adds no FAIL or WARN to history, and neither placement order can refuse a line nobody could write |
| E5 | a send while the round is open (worker running; or stopped but its `returned` not yet written - the dod_gate window) | no line | at most one open round per pair; the miss side reproduces today, never a false FAIL |
| E6 | a send on a task closed by `accepted` | no line; the later stop finds `done` and writes nothing (as today) | an accepted closes the task for every worker (9f, session_context law); a post-verdict chat is no round |
| E7 | a send after `rejected` (a fix round by resume) | `resumed` is written (rejected never closes) | the common fix-round path (FG7-22 M7) is the one this node exists for |
| E8 | race: the worker stops before `post-send` writes `resumed` | `resumed` lands after `returned` #2's chance: the round stays open; a later verdict WARNs (over-report); door: the CLI `returned` (F5) | a race may only over-report; it never hides a verdict before an end |
| E9 | a second exit-0 stop with no `resumed` since (replay, duplicate) | nothing (M1 unchanged) | idempotence of the stop side holds per round |
| E10 | two sends before the worker stops | the first writes `resumed`, the second sees an open round: no line | one open round per pair; 9h refuses a second `resumed` anyway |
| E11 | the copy: the delegated lives in a linked worktree copy; the index entry is gone after `returned` #1 (M9) | `_locate` scans; `resumed` goes into the copy holding the delegated; the index is re-written | a round's lines live in one logical file, the one the validator, the WARN and the stop read |
| E12 | the delegated is older than `SCAN_LINES` (3000) lines in its copy | not found: no line (internal limit, no test) | a worker the hook cannot tie is never written for |
| E13 | outside input (a host answer): payload not a dict / not JSON / no `tool_input` / `to` absent, int, `""`, `../x`, `a*`, 100000 characters, non-ASCII; stdin with no EOF | `[]`, exit 0, journal bytes unchanged, no exception; deadline: silent | the hook never blocks a tool and never writes on input it cannot tie |
| E14 | 9h refusals: unknown ref, closed task, open round, before its delegated, no `worker_ref`/`task_id` | FAIL, one text per line, door named | a `resumed` never opens a task, never reopens a closed one, never opens a second round |
| E15 | a `resumed` of a worker the WARN had superseded (a later delegated of the same kind) | the resumed ref becomes the owed one of its (task, agent) slot | owed = the latest START per kind; a start is a delegated or a resumed |
| E16 | RESULT PENDING after a resume | `resumed` newer than the latest `returned` -> not pending (counted open, not "returned"); `returned` #2 later -> pending | the screen never says "returned" for a worker that is running |
| E17 | same ts on `resumed` and `returned` | file order decides (the WARN walks in order; session_context breaks ties by position) | the writer's lock order is the truth |
| E18 | a tree branched before the change commits a journal copy holding `resumed` | its old validator refuses the unknown event at that tree's commit; the Lead lands this node between waves | a line is judged by a validator that knows it (Lead duty, L1) |
| QE1 | Q2: `critic:t-123` where the matrix reaches the basis branch | same verdict as bare `critic` | a traceable critic basis is never weaker than an untraceable one |
| QE2 | Q2 adversarial (the function moves from "no meaning" to a gate's legalizer; it may err ONLY toward FAIL): `critic:`, `critic:t-12`, `critic:t-123 `, `critic: t-123`, `CRITIC:t-123`, `critic:t-１２３`, `critic:t-123A`, `critic:t-123;x`, `critic:lead`, `["critic"]`, `7`, `None` | `(False, None)`: the line falls to the generic FAIL, as today for any unknown basis | no malformed string ever legalizes an acceptance |
| QE3 | Q2: the cited id names no critic `delegated` | validator: form only (passes as bare `critic` does); echo: M2 phantom WARN at the write moment | the join stays where it already lives (echo `critic_task_ids`); the per-line matrix stays pure |
| QE4 | Q2 POSITIONAL: branch 5 stays after the judge refusal (2) and the FLOOR (4) | `critic:<id>` never rescues a below-sonnet acceptor or a judge basis | the matrix's branch order is unchanged |

## 4. Builder cards (R11-f)

Card A runs first; card B after A is committed (both own `journal_validator.py` and its test: maxConcurrent 1).

### 4.A - the resumed round

given: this file (sections 0, 2.1-2.4, 3); C:/QAFactory/forge-repo/tools/journal_hooks.py::_find_delegated, ::_locate, ::_write_returned, ::_record_returned, ::post_agent, ::_session, ::_write_index, ::cut_notes, ::main; C:/QAFactory/forge-repo/tools/transcripts.py::agent_file_name; C:/QAFactory/forge-repo/tools/journal_validator.py::EVENTS, ::TASK_ID_REQUIRED_EVENTS, ::_line_form_violations (rule 12), ::validate_new_lines (rule 9f block), ::returned_order_warnings, module docstring (9f, item 21); C:/QAFactory/forge-repo/tools/session_context.py::open_dispatch_lines; C:/QAFactory/forge-repo/tools/compact_snapshot.py (open list :605-611); C:/QAFactory/forge-repo/tools/test_journal_hooks.py::payload, ::stop, ::run_main; C:/QAFactory/forge-repo/tools/test_journal_validator.py::RETURNED_ROWS, ::RETURN_ROWS; C:/QAFactory/forge-repo/tools/test_session_context.py::test_result_pending_and_the_returned_that_never_closes; C:/QAFactory/forge-repo/tools/test_compact_snapshot.py::test_the_open_list_marks_a_dispatch_whose_worker_returned_and_a_returned_never_closes_it; C:/QAFactory/forge-repo/docs/TESTING.md
owns:
C:/QAFactory/forge-repo/tools/journal_hooks.py
C:/QAFactory/forge-repo/tools/journal_validator.py
C:/QAFactory/forge-repo/tools/session_context.py
C:/QAFactory/forge-repo/tools/compact_snapshot.py
C:/QAFactory/forge-repo/tools/test_journal_hooks.py
C:/QAFactory/forge-repo/tools/test_journal_validator.py
C:/QAFactory/forge-repo/tools/test_session_context.py
C:/QAFactory/forge-repo/tools/test_compact_snapshot.py
non-goals: no edit of .claude/settings.json (the Lead places the entry, L1), journal_write.py, dod_gate.py, journal_echo.py, forge_metrics.py, calibration_counts.py, hook_liveness_probe.py, COORDINATOR.md, DECISIONS.md; no change to the matrix (card B), to the FG7-22 WARN text, to decide()'s exit codes or to any FAIL other than 9f's text and the new 9h; no transcript read; no new test file; no commit - all four code files are mechanism files (M11): the builder STAGES, the Lead commits
handoff: the worktree branch with the change staged and not committed, and a report: the witness tail, the narrow call's number, `tests not written:` lines
edges: E1-E18 of section 3 (E8, E12, E18 are named, not rows)
DoD: `python -m pytest tools/test_journal_hooks.py tools/test_journal_validator.py tools/test_session_context.py -q; python -m pytest "tools/test_compact_snapshot.py::test_the_open_list_marks_a_dispatch_whose_worker_returned_and_a_returned_never_closes_it" -q`
siblings: journal_hooks.post_agent (the launch producer; `_find_delegated` shared, its replay branch unchanged); journal_hooks.record_returned (the stop producer, one `_find_delegated` change); journal_validator.returned_order_warnings (FG7-22, gains the resumed step); session_context.open_dispatch_lines and compact_snapshot open list (the two RESULT PENDING readers, the same rule); journal_echo (calls decide(): sees 9h through it, unchanged); forge_metrics._nc_moves (counts resumes from transcripts, unchanged - noticed, section 10)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-88-resumed-round-returned-card.md

Acceptance:
1. `post_send` and mode `post-send` as 2.1; `_find_delegated` as 2.2; `_round_step`, 9f, 9h, the WARN step, `EVENTS`,
   `TASK_ID_REQUIRED_EVENTS`, rule 12 and the docstring as 2.3; RESULT PENDING as 2.4.
2. Grep `_round_step\(` in tools/*.py (non-test) = the def + 2 calls (`validate_new_lines`, `returned_order_warnings`).
3. Narrow call over the live journal from the worktree root (the temporal invariant E4):
   `python -B -c "import sys; sys.path.insert(0,'tools'); import journal_validator as jv; L=open('logs/journal/dev1.jsonl',encoding='utf-8').read().splitlines(); print(len(jv.returned_order_warnings(L[2157:], L[:2157])))"`
   The Lead runs the same line on main before the commit; the two numbers are equal (no `resumed` line exists yet).

Test lines, strongest first (the builder writes top-down until its test lines reach its code lines):
- test: test_journal_hooks.py::RESUME_ROWS (one new parametrised table in the existing file, driving post_agent / record_returned / post_send on the `repo` fixture) row "resume-then-stop" - the journal ends `delegated, returned, resumed, returned`, one ref, the hook line says `JOURNAL: resumed` | expected from: 2.1-2.2, E1
- test: same table rows "send-while-running", "peer-pipe", "other-session", "accepted-task", "two-sends" - exactly one `resumed` in "two-sends", none in the others | expected from: E3, E5, E6, E10, F3 (b)
- test: test_journal_validator.py::RETURNED_ROWS rows "resumed-then-second-returned" (code 0), "resumed-while-round-open", "resumed-on-closed-task", "resumed-unknown-ref" (code 1, 9h needles); row `twice-for-one-pair` unchanged | expected from: 2.3, E4, E14
- test: test_journal_validator.py::RETURN_ROWS rows "resumed-verdict-before-second-stop" (one WARN) and "resumed-second-returned-then-verdict" (none) | expected from: 2.3, E1, E2
- test: test_session_context.py::test_result_pending_and_the_returned_that_never_closes rows "resumed-after-returned-is-running" (K = 0) and "second-returned-after-resumed-is-pending" | expected from: 2.4, E16
- test: test_journal_hooks.py::RESUME_ROWS payload rows (E13's list, one row each, stdin deadline excluded: the existing F3 test covers `main`) - `[]`, journal bytes equal | expected from: E13, CLAUDE.md rule 11 battery
- test: test_compact_snapshot.py::test_the_open_list_marks_a_dispatch_whose_worker_returned_and_a_returned_never_closes_it - a resumed-after-returned variant shows no mark | expected from: 2.4, E16

### 4.B - Q2, the critic basis grammar (after 4.A is committed)

given: this file (sections 2.5, 3 QE1-QE4); C:/QAFactory/forge-repo/tools/journal_validator.py::_matrix_d0058_violation, ::TASK_ID_RE; C:/QAFactory/forge-repo/tools/journal_echo.py::_check_accepted_r3, ::CRITIC_TOKEN_RE; C:/QAFactory/forge-repo/tools/r3_integration_check.py (critic trail :190-245); C:/QAFactory/forge-repo/tools/test_journal_validator.py::MATRIX_ROWS, ::_BAD_IDS; C:/QAFactory/forge-repo/tools/test_journal_echo_r3.py; C:/QAFactory/forge-repo/tools/test_r3_integration_check.py; C:/QAFactory/forge-repo/docs/TESTING.md
owns:
C:/QAFactory/forge-repo/tools/journal_validator.py
C:/QAFactory/forge-repo/tools/journal_echo.py
C:/QAFactory/forge-repo/tools/r3_integration_check.py
C:/QAFactory/forge-repo/tools/test_journal_validator.py
C:/QAFactory/forge-repo/tools/test_journal_echo_r3.py
C:/QAFactory/forge-repo/tools/test_r3_integration_check.py
non-goals: no change to the matrix's branch order, to `queued-to-lead`/`judge`, to `rejected` judging, to the echo's S2/S3/S5; no existence join in the validator (QE3); no new test file; no commit (journal_validator.py is a mechanism file; the Lead commits)
handoff: the worktree branch staged, not committed; a report: the witness tail, `tests not written:` lines
edges: QE1-QE4 of section 3
DoD: `python -m pytest tools/test_journal_validator.py tools/test_journal_echo_r3.py tools/test_r3_integration_check.py -q`
siblings: journal_echo R3 S1/M2 and r3_integration_check (the other two readers of the basis, moved to the one grammar); journal_write.py `reject --basis`/`accept --basis` (pass any string, unchanged)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-88-resumed-round-returned-card.md

Acceptance: `critic_basis` as 2.5; Grep `basis == "critic"` / `basis=="critic"` in the three code files = 0 code lines
(comments may keep the old word); Grep `critic_basis\(` (non-test) = def + 3 readers.

Test lines, strongest first:
- test: test_journal_validator.py::MATRIX_ROWS - one `critic:t-123` twin of every existing row whose basis is `critic`, the same expected verdict | expected from: 2.5, QE1, QE4
- test: same table - the QE2 strings, each as a row expecting the verdict of basis None | expected from: QE2
- test: test_journal_echo_r3.py - one parametrised test: basis `critic:t-NNN` with a critic delegated under t-NNN (another task) -> silent; with none -> the M2 literal | expected from: 2.5, QE3
- test: test_r3_integration_check.py - an accepted with basis `critic:t-NNN` in the window counts as a trail | expected from: 2.5

## 5. Lead section (not the builders')

- L0 (before card A; command hygiene pt. 6a, X1-X3): byte copy of `.claude/settings.json`; add a temporary PostToolUse
  entry, matcher `SendMessage`, command `python -B -c "import sys;open(r'<scratch>/send-probe.jsonl','ab').write(sys.stdin.buffer.read()+b'\n')"`,
  and the same command as a second SubagentStop entry; launch one scout, let it stop, SendMessage it one line, let it stop;
  read the file (fields `tool_input.to`, `session_id`, `agent_id`; two stops with one `agent_id`); restore the byte copy and
  compare hashes. If PostToolUse does not fire for SendMessage, F1 (a) has no producer: return to F1 (b).
- L1: commit card A (staged); then add the entry `{"matcher": "SendMessage", "hooks": [{"type": "command", "command":
  "python tools/journal_hooks.py post-send"}]}` under PostToolUse; land between waves (E18).
- L2: `COORDINATOR.md` § Routing log SHAPES (:407): `returned` "once per round"; new row `resumed`: `task_id`, `worker_ref`,
  `agent`, `model`; written by the PostToolUse SendMessage hook when a worker whose round ended is resumed; never opens or
  closes a task. Witness: the DOC-DISPATCH key run.
- L3: F8 (D-0046).

## 6. Readers of every touched file (rule 7)

The `tools/owns_readers.py` block was not attached (`facts:` carries one line): the hand greps below stand in; the plan
critic re-runs the tool (critic rule 24, Q13 (d)).

Touched names: `journal_hooks.post_send`, mode `post-send`, `_find_delegated` (rule); `journal_validator.EVENTS`,
`TASK_ID_REQUIRED_EVENTS`, `_round_step`, 9f/9h, `returned_order_warnings`, `critic_basis`, `_matrix_d0058_violation`;
`session_context.open_dispatch_lines`; `compact_snapshot` open list; `journal_echo._check_accepted_r3`; `r3_integration_check`.
Greps: `import journal_hooks|journal_hooks\.` non-test tools = dod_gate.py:748-749, journal_write.py:263-265, docstrings
(dispatch_gate:1090, journal_validator:249, mechanism_gate:291), hook_liveness_probe:1148/1478/1497; `\bEVENTS\b` tools = the
validator + test_journal_validator:1693 + test_journal_write:197 (its own list); `["']returned["']` = 17 files (61 hits);
`open_dispatches\(|open_dispatch_lines\(` non-test = session_context, compact_snapshot:370-371, calibration_counts:605/609
(prose mirror); `basis.{0,6}==.{0,3}["']critic` = validator, journal_echo, r3_integration_check.

| reader | reads | answer |
|---|---|---|
| `tools/dod_gate.py:748` | `record_returned` | unchanged API; on a resumed round it now gets a `written` line (not a WARN, so not logged to warn.log) |
| `tools/journal_write.py:263` | `journal_hooks._session` | unchanged |
| `tools/journal_write.py::_write_event`, `:612` | the validator; `matrix_warnings` | unchanged code; `resumed` passes rule 3 after card A; the WARN may now name a resumed ref |
| `tools/journal_write.py:805-907` (`returned` CLI, `_fill_returned`) | the last delegated of (task, ref) | unchanged; the CLI `returned` is the E2/E8 door and is legal in an open round |
| `.claude/settings.json` | hook commands | changes by the Lead (L1); `wiring_check.py:257` admits one mode argument (same shape as `post-agent`) |
| `tools/hook_liveness_probe.py` (cases 17-19, :1165 one delegated + one returned) | journal_hooks as a script | unchanged: its scenario has no resume; the composition check works on the SET of scripts (:66-72), `journal_hooks.py` already has cases - a `post-send` case is noticed, not required |
| `tools/test_hook_liveness_probe.py:440-456`, `tools/test_mechanism_gate.py:1677` | fixed command lists | unchanged (fixtures; neither reads the live entry list for SendMessage) |
| `tools/mechanism_gate.py:228/251/259/291` | the paths | unchanged; consequence: the Lead commits |
| `.githooks/pre-commit`, `pre-merge-commit` | the validator | unchanged; a committed `resumed` is judged by 9h |
| `journal_validator::decide_with_warnings`, `::decide_merge`, `::_developer_file_result`, `--all` | `matrix_warnings` -> the WARN | changes in this stream (resumed step) |
| `tools/journal_echo.py` | `decide()`; R3 basis | 9h through decide() unchanged code; R3 changes in card B |
| `tools/forge_metrics.py:86-89, :707, :868` | `TASK_EVENTS` (no `resumed`) | unchanged: a `resumed` line is outside `TASK_EVENTS`, filtered out of the window, never "unclassified" |
| `tools/calibration_counts.py:85-86, :350-380` | its own copies of the required sets | unchanged: a `resumed` without `task_id` is refused by the validator before it can reach history; noticed (section 10) |
| `tools/compact_snapshot.py:359-378` | `session_context.open_dispatches` | unchanged function; its RESULT PENDING mark changes in card A |
| `tools/test_forge_metrics.py` K6, `test_journal_validator_merge.py`, `_node.py` | exact WARN counts | unchanged: no fixture holds `resumed` |
| `tools/r3_integration_check.py` | basis | changes in card B |
| `tools/install_parity_anchors.json` | paths, presence | unchanged (estimate; the plan critic's tool run confirms) |

## 7. Test cost (docs/TESTING.md)

Card A: 7 test lines over ~110 code lines (hook ~55, validator ~35, displays ~12; estimate); one new table `RESUME_ROWS` in
the existing hook test file, every other case a row of an existing table; the payload battery is required (outside input).
Witness: three whole files + one node id. Card B: 4 lines over ~25 code lines, three whole files. No canon-class file (M13).

## 8. Small choices closed by the designer

1. Silent on a send that is not a resume (steps 1-5): only a tied send writes; no door, since nothing is owed.
2. A `delegated` reopens a round only for a never-seen pair; only `resumed` reopens a seen one: no behaviour change for a
   journal without `resumed`.
3. `model` copied, not required: the validator's required sets have copies in `calibration_counts.py`; adding `resumed` to
   `MODEL_REQUIRED_EVENTS` would split them.
4. `compact_snapshot` joins card A's owns (rule 2: a defect the change creates in the node's reach is fixed by the card).
5. `resumed` is not an `_OPEN_LIFECYCLE_EVENTS` member: a fix round after `rejected` stays out of OPEN DISPATCHES as today
   (the mirror at `calibration_counts.py:605` stays in step); noticed.
6. The WARN's date gate applies to `resumed` too (one rule for every start).
7. Cards split A/B by subject; sequential by the shared file.

## 9. Forks (the Lead decides)

- F1 - how the resumed round becomes visible (M4). (a) a `resumed` line at the send (PostToolUse SendMessage hook) and
  `returned` once per round - recommended: the WARN sees the verdict AT the verdict, on write, commit, merge and CI; needs
  X1 (L0). (b) `returned` once per stop with no resume line: needs a stop identity to stay idempotent, rule 9f must also let
  a `returned` follow an `accepted` (FG7-22 F6 (b)), and the WARN must judge NEW `returned` lines after a verdict - the
  defect is seen late (at the stop and at commit), never at the verdict. (c) stop side only: the second stop appends a
  warn.log line (check 48c); no journal change; does not meet the row ("a form the FG7-22 WARN reads").
- F2 - rule 9f (the brief keeps it a fork). (a) "one `returned` per round" (a round starts at a never-seen `delegated` or a
  `resumed`) - recommended: journals without `resumed` read as today (E4). (b) keep "one per pair" and give round ends a new
  event: every `returned` reader (17 files) learns a second name. (c) keep 9f and suffix the ref (`agent:<id>#2`): breaks the
  `agent:<id>` join (`transcripts.agent_file_name`, `_locate`, `forge_metrics._nc_moves`).
- F3 - "a resume by a peer session is not a round" has two readings: (i) a send whose `to` is a peer pipe; (ii) another Lead
  session's send to this session's worker. (a) the `agent:<to>` join only (covers i). (b) (a) + equal `session` when both
  are present (covers i and ii) - recommended. (c) (a), any session counts.
- F4 - "a resume that never stops again owes nothing". (a) owes nothing to the validator, but a verdict during that open
  round WARNs - recommended (else the node adds nothing over today). (b) owes nothing at all: the WARN ignores a round with no
  second `returned` - the miss of FG7-22 E3 stays.
- F5 - the E8 race. (a) accept it: over-report side, CLI door - recommended (the window is one hook run; a worker needs a
  model turn to stop). (b) a "stopped while closed" marker with a freshness bound, consumed by `post-send`: more state,
  a stale marker could close a later round with an old stop.
- F6 - Q2 scope. (a) the matrix only: the echo keeps exact `critic` (a `critic:<id>` accept draws R3 M1 unless notes carry
  the token). (b) one grammar `critic_basis` read by the matrix, the echo R3 and r3_integration_check - recommended (one road;
  owns widen by two files). (c) (b) + the validator FAILs when the cited id names no critic delegated: stronger, but the
  matrix is per-line and shared with merge mode. Measured effect: the 67 live `critic:t-` accepts all passed by rank (M10).
- F7 - sequencing: A then B (recommended, shared file) vs one card (one builder, four+ test files exceeds the three-file DoD).
- F8 - D-0046 (`DECISIONS.md:36`: a fix round is a fresh `delegated` with `attempt` n+1 after `rejected`) vs practice (resumes,
  FG7-22 M7). (a) leave D-0046; this node journals resumes as rounds. (b) after card A, the Lead amends D-0046 to name the
  resume as a legal fix-round form - recommended (the journal then says what is done). An owner/Lead decision.

## 10. Noticed, not widened

- `forge_metrics._nc_moves` counts resumes from transcripts; once `resumed` lines exist the journal could carry this count on
  CI too (another node).
- `calibration_counts.py:85-86` copies the validator's required sets by hand (a "two count pins" class).
- `resumed` after `rejected` is not shown under OPEN DISPATCHES (choice 5).
- `hook_liveness_probe` has no `post-send` case (optional, Lead).

## 11. Reading trail

Read: pile row :113 (and :110-112); the FG7-22 card §0-§12 (:1-268); `journal_hooks.py` :1-459, :505-564;
`journal_validator.py` :236-255, :290-303, :464-531, :640-835, :905-920, :978-999, :1140-1244; `.claude/settings.json` :20-119;
`transcripts.py` :44-88, :525-559; `forge_metrics.py` :80-93, :700-749, :860-875, :1236-1275; `session_context.py` :514-539,
:586-671; `compact_snapshot.py` :359-383, :596-615; `journal_write.py` :483-499, :548-569; `calibration_counts.py` :370-383;
`journal_echo.py` :1972-2021, :2160-2204; `r3_integration_check.py` :1-30, :190-245; `hook_liveness_probe.py` :60-75;
`test_hook_liveness_probe.py` :436-457; `test_journal_hooks.py` :59-103, :269-295 (+ def list); `test_journal_validator.py`
:1625-1664 (+ table list); `test_session_context.py` :1699-1757; `docs/TESTING.md` :75-114.
Greps (controls in M10/M12 and section 6): SendMessage over tools/COORDINATOR/agents/RUNBOOK; `9h`/`9f`; `EVENTS`; `returned`
literal counts; `open_dispatches(` callers; critic basis compares; `_OPEN_LIFECYCLE_EVENTS`; `journal_hooks` importers and
settings copies; mechanism_gate entries; package json for the four test files (control `test_story_run` = 149 hits);
`dev1.jsonl` counts (accepted+`critic:t-` 67, accepted+`critic` 236, returned 518).
Needed beyond the manifest: `.claude/settings.json`, `tools/transcripts.py`, `tools/forge_metrics.py`, `tools/session_context.py`,
`tools/compact_snapshot.py`, `tools/journal_write.py`, `tools/calibration_counts.py`, `tools/journal_echo.py`,
`tools/r3_integration_check.py`, `tools/hook_liveness_probe.py`, `tools/mechanism_gate.py`, the four test files, `docs/TESTING.md`,
`logs/journal/dev1.jsonl` (Grep only), `COORDINATOR.md` (Grep).

## 12. Lead decisions (Lead 501cb4e0, 2026-11-18)

- F1 (a), conditional on L0: the L0 probe edits .claude/settings.json for a few minutes, so it waits for the owner's word; if PostToolUse does not fire for SendMessage, F1 returns to the Lead.
- F2 (a) one `returned` per round; F3 (b); F4 (a); F5 (a); F6 (b); F7 card A then card B; F8 (b) after card A.
- Card A is not dispatched before L0.
