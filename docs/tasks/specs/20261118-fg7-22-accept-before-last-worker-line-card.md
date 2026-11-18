# FG7-22 - journal: WARN "a verdict written before the worker returned" (builder part), and two Lead text edits (draft card)

task: t-1436 · node: forge/7/FG7-22 · feature: F19 · designer draft, 18.11.2026 · the Lead decides (forks in section 9)

Pile row: `plans/piles/forge/batch-7-vhodyashchie-4.md:47`. Finding: `plans/piles/forge/findings/20261112-zhurnal-priemka-pered-sdachej-canon-ne-v-witness-basis-rejected.md`
(item 1 = this card's builder part; items 2-3 = Lead text, section 5). Dependency in the row (stream B of 20261116-architect-tier,
FG7-16 on the same file) is met: row 41 reads `принято: 5a7cc34 (t-935)`.

## 0. Target on main, measured

| # | fact | carrier (read by the designer) |
|---|---|---|
| M1 | The journal already holds the worker's end as a line: `returned` (`task_id`, `worker_ref`, `model`, `via:"hook"`), written by the SubagentStop gate on an exit-0 decision. | `tools/dod_gate.py:824-825` (`if exit_code == 0: _record_returned`); `tools/journal_hooks.py::_write_returned` (:297-314), `::record_returned` (:319) |
| M2 | One `returned` per (task, worker_ref) at most: a second one is a FAIL; a `returned` on a task closed by `accepted` is a FAIL. | `tools/journal_validator.py::validate_new_lines` :1160-1179 (rule 9f) |
| M3 | A second stop of the same worker (a resumed worker) writes nothing: the recorder is idempotent. | `tools/journal_hooks.py::_record_returned` :398-402 (`if done: ... return`); test `tools/test_journal_hooks.py:257-260` |
| M4 | The hook era starts at `dev1.jsonl:2158` (first `delegated` with `via:"hook"`, ts 2026-11-16T23:09:18); first `returned` at :2162 (23:10:44). No `returned` exists before. | Grep `"event":"delegated".*"via":"hook"` head 1; Grep `"event":"returned"` head 1, on `logs/journal/dev1.jsonl` |
| M5 | Counts in the live journal (4035 lines, no seed: line 1 has no `continues`): `returned` 497, `accepted` 1324, `delegated` 1617, of them `worker_ref:"agent:` 1612 and another form 2. `returned` of critic/designer: 212. | Grep count, same file (positive controls: the same patterns found lines) |
| M6 | Sample of 7 `accepted` lines at `dev1.jsonl:4009-4026`: 2 have no `returned` of their worker anywhere - t-1407 (`agent:aa200261f837d136d`, delegated :3954, accepted :4015) and t-1410 (`agent:a858942de1345d0a7`, :3961 / :4023); the worktree copies hold none either. | Grep of both refs (2 hits each = the delegated only); Grep over `.claude/worktrees/**/logs/journal/*.jsonl`, control t-1418/t-1406 found in 12 files |
| M7 | Fix rounds run today as RESUMES with no journal line: t-1406 has one `returned` (:3957, 09:21:53, round 1) and `accepted` "round 2" at :4022 (10:51:27), no `rejected`, no second `delegated`. | Grep `"task_id":"t-14(06|10|18|09|17)"` |
| M8 | The accepted-line WARN channel is `matrix_warnings`; its callers: `journal_write.py::_write_event` :612 (accept moment, after the append), `journal_validator.py::decide_with_warnings` :1500 (commit), `::decide_merge` :1970, `::_developer_file_result` :2397. `--all` reaches it through `decide_with_warnings`/`_developer_file_result`. No test calls `matrix_warnings` directly. | Grep `matrix_warnings\(` in tools (non-test); Grep `matrix_warnings` in `tools/test_*.py` = 0, control `decide_with_warnings` = 17 hits in 4 files |
| M9 | Warnings in `_write_event` are produced AFTER the line is appended (:596-612), inside one `contextlib.suppress(Exception)` holding feature, node and matrix WARNs. | `tools/journal_write.py::_write_event` |
| M10 | The dated-WARN skeleton gates the NEW line's date: `_dated_new_objs` (`ts[:10] < since` skips). Constants `FEATURE_WARN_FROM`, `NODE_WARN_FROM`. | `tools/journal_validator.py:277-286`, `::_dated_new_objs` :1404 |
| M11 | The module's own rule numbers run to 19 in the docstring; "rule 20" is already used in code for the optional `via`/`session`/`witness_by` fields. | `journal_validator.py:135`, :981-998 |
| M12 | `rejected` with `basis`: 31 of 198 lines - `"critic"` 11, `"critic:t-NNN"` 16, `"lead"` 4. The validator puts no check on a rejected's basis (`_matrix_d0058_violation` returns None for event != accepted, :653); `journal_write.py reject` takes `--basis` (:817). | Grep `"event":"rejected".*"basis"` (-o) and count of `"event":"rejected"` |
| M13 | Witness labels: 55 `witness` fields carry `BATCH CANON`, 49 start `canon <run id>`. | Grep count on `dev1.jsonl` |
| M14 | Test fixtures of the readers that assert exact WARN counts are dated 2026-07/2026-10 (`test_journal_validator.py` NOW 2026-07-10; `test_forge_metrics.py` K6 NOW 2026-10-03); no `test_journal_validator*.py` fixture is dated 2026-11/12 except one 2098 `delegated` with a `cli:` ref. | Grep `20\d\d-1[12]-` over `tools/test_journal_validator*.py` (1 hit, :1717); Read `test_forge_metrics.py:500-575` |

The finding's own text (item 1) proposed reading the worker's last TRANSCRIPT line through `tools/transcripts.py` with a 30 s
tolerance. M1-M3 did not exist when it was written (12.11; the hook era starts 16.11): the journal now carries the end itself.
Section 2 is written for the journal-only reading (fork F1 (a)); the transcript variant is F1 (b).

## 1. Architecture

The node touches no `ai-packages/qa-factory/` path: the AR-n below are named by analogy (forge mechanisms keep the same
discipline); the judgment census is package-only: `census: n/a -- forge tool`.

- AR-22 (every field read has a producer): the new reader reads `returned` lines. Producers: `journal_hooks._write_returned`
  (SubagentStop, exit 0) and the CLI `journal_write.py returned`. The WARN line itself is terminal (read by the Lead at
  the accept moment and at commit). Change check (DoD): the builder names both producers in the docstring item.
- AR-13 / AR-15 (one reader, one survivor): the WARN reads the journal through the validator's own `_try_parse_obj` and
  `extract_replaces_worker`; ONE producer function, reached by every path through `matrix_warnings` (M8) - no call site
  is edited one by one. Change check: Grep `returned_order_warnings\(` = the def + one call (in `matrix_warnings`).
- AR-18 (one output shape): the line is built by `_warn_line` (`<tag>: WARN <text> (a warning only, the journal is not blocked)`).
- AR-29 (a code check judges data): the check judges PRESENCE (a `returned` line) and a JOIN (task_id, worker_ref).
  Owner: data (code). It never judges whether the verdict was right - that stays the Lead's judgment, read by calibration.
- AR-2 (code reports and leaves a move): a WARN, never a FAIL; the text names the door.

`variety: none -- a forge journal tool outside the package; no project, language or tracker axis is met`.
One road (rule 6): every agent kind, every acceptor and every path (write, commit, merge, CI `--all`) reaches the same function;
no agent, event path or clone is left out by name.

## 2. Design (for F1 (a), F2 (a), F3 (b), F4 (a), F5 (a) - the recommendations)

### 2.1 The function

`journal_validator.returned_order_warnings(new_lines, head_lines, *, seed_lines=()) -> list[str]` - pure, no I/O, never raises.

State, built by ONE walk over `seed_lines + head_lines + new_lines` in order (each line through `_try_parse_obj`; a line that
does not parse, or a field of the wrong type, is skipped):

- `owed[task_id][agent] = ref` - set by a `delegated` whose `worker_ref` (stripped) starts `agent:`, whose `ts` parses
  (`parse_ts`) and whose `ts[:10] >= RETURNED_WARN_FROM`; a later `delegated` of the same (task, agent) REPLACES the entry
  (a retry or a dead-worker replacement supersedes the earlier worker). A `delegated` whose notes carry
  `replaces_worker:<h>` (read by `extract_replaces_worker`) also drops `h` from every agent entry of the SAME task.
- `returned_refs` - set of (task_id, stripped worker_ref) of every `returned` line.

Judging (NEW lines only, in their order, the state including every earlier line, new ones too): for a line with `event` in
`RETURN_ORDER_EVENTS = {"accepted", "rejected"}` and a `task_id` that matches `TASK_ID_RE`, the owed refs are
`[(ref, agent) for agent, ref in owed[task_id].items() if (task_id, ref) not in returned_refs]` in insertion order. Non-empty
-> ONE WARN for the line, listing every owed ref (no cap: at most one ref per agent kind by construction). Then the line enters
the state like any other.

New constant `RETURNED_WARN_FROM = "2026-11-17"` beside `NODE_WARN_FROM`, compared on the DELEGATED line's date (M4).

### 2.2 The text (verbatim; the test reads its fixed parts)

`_warn_line(tag, f"{event} before the worker returned: {owed} has no `returned` line for {task_id} -- the verdict was written before the worker's end was journaled (after an accepted, rule 9f refuses that worker's `returned`) -- wait for the worker's stop line; a worker whose stop was lost gets `python -B tools/journal_write.py returned --task {task_id} --worker <ref>` before the verdict")`

where `owed` = `agent:<id> (<agent>)` items joined by `, `, and `tag` = `line <n in the file> event=<ev!r> task_id=<id!r>` (the tag
form of `matrix_warnings`).

### 2.3 Wiring

`matrix_warnings` ends with `return warns + returned_order_warnings(new_lines, head_lines, seed_lines=seed_lines)`; its docstring
says it now carries every accepted-line WARN (the name stays: five readers, M8). Docstring of the module: a new item `21. RETURN
ORDER (FG7-22)` after item 19 (M11: 20 is taken in code), stating the rule of 2.1, the producers (AR-22), the date gate, the known
miss (E3) and "WARN only; decide() and journal_echo never see it".

### 2.4 What does not change

`decide()`, `validate_new_lines`, every FAIL, every exit code; rule 9f; `journal_write.py`, `journal_hooks.py`, `journal_echo.py`.

## 3. Edges, each with its invariant

| id | edge | behaviour | invariant it protects |
|---|---|---|---|
| E1 | an `accepted` whose worker has no `returned` yet (worker still running, the t-057 class) | one WARN naming the ref and the agent; exit code unchanged | a verdict written while the journal holds no end of a hook-era worker of that task is never silent |
| E2 | `returned` then `accepted` | silent | a worker whose end is journaled never draws the WARN |
| E3 | a RESUMED worker (one `returned` from its first stop, M3; the verdict lands after the resume, before its next stop) | silent - KNOWN MISS, named in the docstring item | the WARN never claims more than the journal knows; the miss is the safe-for-noise side; covering it is F1 (b)/(c). Measured: fix rounds run as resumes (M7), so the miss covers the common fix-round path |
| E4 | several `returned` for one task id | each counts only for its own (task, worker_ref); a `returned` of another worker or task discharges nothing | a returned measured on another worker never counts |
| E5 | a worker that never wrote a `returned` (lost stop, crash, t-1407/t-1410 class, M6) | WARN, the same as E1 (the journal cannot tell lost from running); door: a CLI `returned` before the verdict | a missing end is reported whatever its cause; the WARN errs toward reporting |
| E6 | `accepted` for a scout / critic / designer vs a builder | one rule for every agent kind: owed = the LAST hook-era worker of EVERY agent kind on the task (F2 (a)) - a critic-entry still running on the task draws the WARN on the builder's accept | an accepted closes the task for every worker on it (rule 9f refuses every later `returned`), so every running worker of the task is owed |
| E7 | a retry (`attempt` n+1) or a `replaces_worker:` replacement whose earlier worker never returned | the superseded worker is not owed; only the latest worker per (task, agent) is | a worker the journal itself declared replaced never keeps a task in WARN forever |
| E8 | a batch accept: several verdict lines in one commit or in a row | each line judged alone, against every earlier line including the new ones; a `returned` between two verdicts counts for the later one only if it is its own task's | one task's end never discharges another's (key = task_id) |
| E9 | TEMPORAL - lines written before the check exist (old journal; before this commit the WARN does not exist anywhere) | (i) old verdict lines are never judged: every path judges only lines new against its base (append-only, commit/merge/`--all`); (ii) a NEW verdict on a task whose worker was delegated before `RETURNED_WARN_FROM` owes nothing (no `returned` could exist, M4); (iii) the move that creates the WARN is the Lead's commit of this card | the change adds no WARN to history, and no hook-era-less worker is ever owed a line nobody could write |
| E10 | a `delegated` with `cli:`/`retro:` or another non-`agent:` ref, an unparsable or absent ts, or no `task_id` | not owed | the WARN fires only on a positive fact (a hook-era `agent:` launch) - an unknown never warns (FR-59) |
| E11 | a verdict on a task with no `delegated` at all (Lead's own work, retro) | silent | absence of a launch is never a WARN |
| E12 | broken lines in seed/head (not JSON, a list, an int `task_id`, a non-string `worker_ref`) | skipped; the function returns normally | it never raises: in `_write_event` one exception would suppress the feature/node/matrix WARNs of the same block (M9) |
| E13 | `rejected` before the worker returned (F3 (b)) | the same WARN, event word `rejected`; a later `returned` stays legal (rejected never closes) | a verdict on an unfinished worker is reported whatever the verdict |
| E14 | the WARN at the accept moment comes AFTER the line is written (M9) | it informs; it cannot stop the line (F5) | the one writer's contract (validate, append, then warn) is unchanged |
| E15 | run time over the whole journal | one linear walk, dict lookups; the builder reports the time of the narrow call (section 4) over the live journal; above 0.5 s on this machine -> a report line, not a failure | the accept moment stays interactive; no second parse of the journal per call beyond this one walk |
| E16 | the accepted line itself followed in the same batch by its worker's `returned` | the WARN fires (order decides); the `returned` is a rule 9f FAIL anyway | file order is the truth; the WARN never looks ahead |
| E17 | ref whitespace | refs are compared stripped on both sides (as rule 9f strips) | a cosmetic space never makes an owed worker look returned, or the reverse |

## 4. Builder card (R11-f)

given: this file (sections 0, 2, 3); C:/QAFactory/forge-repo/tools/journal_validator.py::matrix_warnings, ::_warn_line, ::_try_parse_obj, ::extract_replaces_worker, ::parse_ts, ::TASK_ID_RE, ::NODE_WARN_FROM, ::decide_with_warnings, ::validate_new_lines (rule 9f block); C:/QAFactory/forge-repo/tools/test_journal_validator.py::WARN_ROWS, ::test_matrix_warns_on_a_passed_line, ::_line, ::_staged; C:/QAFactory/forge-repo/tools/journal_hooks.py::_write_returned (read only); C:/QAFactory/forge-repo/docs/TESTING.md
owns:
C:/QAFactory/forge-repo/tools/journal_validator.py
C:/QAFactory/forge-repo/tools/test_journal_validator.py
non-goals: no edit of journal_write.py, journal_hooks.py, journal_echo.py, dod_gate.py, COORDINATOR.md, DECISIONS.md, RUNBOOK.md; no change to decide(), any FAIL, any exit code or rule 9f; no transcript read; no new test file; no commit - journal_validator.py is a mechanism file (`tools/mechanism_gate.py:251`): the builder STAGES, the Lead commits
handoff: the worktree branch with the change staged and not committed, and a report: the witness tail, the narrow call's two numbers and first three WARN lines, `tests not written:` lines
edges: E1-E17 of section 3 (E3 is a named miss, not a row; E14/E15 are report lines)
DoD: `python -m pytest tools/test_journal_validator.py tools/test_journal_validator_merge.py tools/test_journal_validator_node.py -q; python -m pytest "tools/test_forge_metrics.py::test_k6_accepted_and_defect_found_are_covered_a_known_value_is_silent" -q`
siblings: journal_validator.matrix_warnings (INDEPENDENT CONTEXT / queued to itself - the same channel, unchanged texts); journal_write.py::_write_event (the accept-time caller, unchanged); journal_echo.py R3 MIRROR (the write-moment accepted WARN of the echo, unchanged, not this channel); session_context.py RESULT PENDING (reads `returned` by task key, unchanged)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-22-accept-before-last-worker-line-card.md

Acceptance:
1. `RETURNED_WARN_FROM`, `RETURN_ORDER_EVENTS`, `returned_order_warnings` as 2.1; text as 2.2; wiring and docstring item 21 as 2.3.
2. Grep `returned_order_warnings\(` in tools/*.py (non-test) = 2 lines (def + the call in `matrix_warnings`).
3. Narrow call over the live journal from the worktree root (replays every hook-era line as new; prints count and seconds):
   `python -B -c "import sys,time; sys.path.insert(0,'tools'); import journal_validator as jv; L=open('logs/journal/dev1.jsonl',encoding='utf-8').read().splitlines(); t=time.perf_counter(); w=jv.returned_order_warnings(L[2157:], L[:2157]); print(len(w), round(time.perf_counter()-t,3)); print(*w[:3], sep='\n')"`
   The count is a measurement for the Lead (no expected value); the WARN lines for t-1407 and t-1410 (M6) are among them.

Test lines, strongest first; all are rows of ONE new parametrised table `RETURN_ROWS` in `tools/test_journal_validator.py`
driving `jv.decide_with_warnings` with `now` = 2026-11-18T12:00:00 and lines dated 2026-11-17/18 (row (c) excepted); every row
asserts `code == 0` and the list of WARNs whose text holds `before the worker returned`:
- test: test_journal_validator.py::RETURN_ROWS row "accept-before-return" - hook-era `agent:` delegated, no returned, accepted: exactly one WARN, holds the ref, `(builder)` and the task id | expected from: section 2.1-2.2, E1
- test: same table row "returned-then-accept" - the same with the returned between: no WARN | expected from: E2
- test: same table row "pre-era-delegated" - the delegated dated 2026-11-16T22:00:00: no WARN | expected from: E9 (ii), M4
- test: same table row "other-returned" - a returned of another worker_ref of another task only: one WARN | expected from: E4, E8
- test: same table row "critic-entry-running" - builder returned, a critic delegated on the same task with no returned, builder accepted: one WARN naming the critic ref | expected from: E6
- test: same table row "superseded-retry" - attempt 1 not returned, attempt 2 returned (after a rejected), accepted: no WARN | expected from: E7
- test: same table row "batch" - two tasks, two accepted, only the second task returned: one WARN, on the first task's line | expected from: E8
- test: same table row "rejected-before-return" - one WARN whose text starts `rejected before the worker returned` | expected from: E13, 2.2
- test: same table row "cli-ref-and-broken-head" - a `cli:` delegated plus a non-JSON head line: no WARN, no exception | expected from: E10, E12

## 5. Lead section - items 2 and 3 of the row (Lead text edits; not the builder's)

Item 2 - `basis` on `rejected` (fork of D-0046). Place: `COORDINATOR.md` § "Routing log · event SHAPES", row `rejected` (line 409);
the other carrier is `DECISIONS.md:36` (D-0046: "`rejected` with `basis: critic`"). Measured (M12): practice writes three forms
(`critic` 11, `critic:t-NNN` 16, `lead` 4 of 31), the code accepts any value and `reject --basis` exists. One paragraph the Lead
may adopt: "`rejected` adds `task_id`, `model`, `by`, `attempt`, `failure_class`; + `basis`: `critic:<critic task id>` when a
critic verdict preceded the rejection (D-0046), `lead` when the Lead's own reading did". Fork L1: `critic:<id>` (recommended:
16 of 31 lines already, the verdict is traceable) vs bare `critic` (D-0046's literal). Noticed: on `accepted`, the matrix reads
only the exact `basis == "critic"` (`journal_validator.py:700`), so `critic:t-NNN` on an accepted line is not the matrix's critic
basis; it passes by rank. If the Lead adopts `critic:<id>` for `accepted` too, that is a validator change (a pile item, F-question
Q2 below), not this card.

Item 3 - BATCH CANON in `witness`. Places: `COORDINATOR.md` § Rule 4 lines 157-159 ("APPENDED to the `witness` field of the
batch's LAST `accepted` event") and `docs/RUNBOOK.md` §7 line 131 (the same). The journal is append-only, so a written line is
never appended to; practice (M13) puts the canon into the `witness` of an `accepted` written after the canon (`canon <run id>:
<verdict>`, 49 lines; 55 labelled `BATCH CANON`). One paragraph the Lead may adopt: "the canon's run id, job statuses and
`canon wall time` go into the `witness` of the batch's last `accepted`, written AFTER the canon, labelled BATCH CANON; when every
node is already accepted, the Lead writes the canon line as `BATCH CANON: <run id> <verdict>` in the `notes` of the next event
it writes about the batch". Fork L2: that door (recommended) vs a dedicated event (a validator change). Witness of both edits:
the DOC-DISPATCH key run of rule 11 (keys quoted before the run, script in full, a negative control).

## 6. Readers of every touched file (rule 7)

The `tools/owns_readers.py` block was not attached (`facts: none`): the hand grep below stands in; the plan critic re-runs the
tool (critic rule 24, Q13 (d)).

Touched: `tools/journal_validator.py` (new names `returned_order_warnings`, `RETURNED_WARN_FROM`, `RETURN_ORDER_EVENTS`; changed
behaviour of `matrix_warnings`: one more WARN kind); `tools/test_journal_validator.py` (one new table).

Hand grep `journal_validator` over `tools/` (non-test): 16 files, 98 hits; `.githooks/`: 2 hits; `.claude/settings.json`: 0 (control
`dod_gate|journal_hooks` = 3). Grep `matrix_warnings\(` (non-test): 4 call lines + def; in tests: 0 (control 17 hits).

| reader | reads | answer |
|---|---|---|
| `tools/journal_write.py:612` | `matrix_warnings` at the accept moment | unchanged code; its output gains the new WARN line (the intended accept-time channel); no `test_journal_write.py` assertion counts messages exactly (Grep `len\(res\.messages\)|messages == ` = 0; control `WARN` = 2 hits) |
| `journal_validator.py::decide_with_warnings`, `::decide_merge`, `::_developer_file_result`, `--all` | `matrix_warnings` | changes in this stream (they get the WARN through the one call) |
| `tools/journal_echo.py` | `decide`, `validate_new_lines`, `parse_ts`, `split_lines`, `check_append_only`, `extract_replaces_worker`, ... | unchanged (no WARN enters decide) |
| `tools/journal_hooks.py:255` | `extract_replaces_worker` | unchanged; it is the PRODUCER of `returned` (AR-22) |
| `tools/calibration_counts.py`, `tools/forge_metrics.py`, `tools/hop_metrics.py` | `extract_replaces_worker`, `feature_problem` | unchanged |
| `tools/test_forge_metrics.py` K6 (`decide_with_warnings`, exact WARN counts) | WARN list | unchanged: fixtures dated 2026-10 fall under the date gate (M14); one K6 node id is in the DoD |
| `tools/test_journal_validator_merge.py`, `tools/test_journal_validator_node.py` | exact WARN counts | unchanged by the date gate (M14); both run whole in the DoD |
| `tools/mechanism_gate.py:251` | the path as a mechanism file | unchanged; consequence: the Lead commits |
| `.githooks/pre-commit:35`, `.githooks/pre-merge-commit:18` | run the validator | unchanged; they print the new WARN on stderr, exit code unchanged |
| `tools/install_parity_anchors.json:519` | the path, `kind: path`, `anchors: []` | unchanged (presence only) |
| `tools/journal_keys.py`, `tools/main_gate.py:42`, `tools/md_regions.py:69`, `tools/md_table.py:8`, `tools/session_context.py:1601` | the name in prose | unchanged |

## 7. Test cost (docs/TESTING.md)

Layer 3 (a table of cases for real combinatorics: the join task x worker x order) in the module's existing test file; no new file
(«Бюджет / Файлы»: the case lies in the file whose door it is). One table, rows in force order (section 4); the builder writes
them top-down until test lines reach code lines and reports the rest as `tests not written: <row> -- over budget`. Witness: three
whole files plus one node id (none is canon-only: Grep `journal_validator` in package `*.json` = 0, control `test_story_run` = 155).

## 8. Small choices closed by the designer

1. Date gate on the DELEGATED line (not on the verdict), date granularity `"2026-11-17"`: the 16.11 23:09-24:00 launches are
   not owed (silent side). A `via:"hook"` gate was rejected: a CLI-repaired `delegated` still gets its hook `returned`.
2. Only `agent:` refs are owed: the hook writes `returned` for `agent:<id>` only (`_write_returned`).
3. Fold into `matrix_warnings` rather than five call-site edits (one road, M8); the name stays.
4. Docstring item 21, not 20 (M11).
5. No cap on the listed refs (bounded by agent kinds); no tolerance window (file order under the writer's lock is exact).

## 9. Forks (the Lead decides)

- F1 - what "the worker's last line" is. (a) the journal `returned` line (recommended: pure, the same on write, commit, merge and
  CI; producer exists; covers t-057's class and lost ends). (b) the transcript's last line via `tools/transcripts.py` (the
  finding's text): catches E3, but it reads host files that CI and other clones lack, so one line WARNs on one machine and not on
  another, and the gate stops being pure. (c) (a) now, plus a node making a resumed worker's later stop journaled (rule 9f "one per
  pair" becomes "one per stop"; owns `journal_hooks.py` (a live hook: Lead places it), `journal_validator.py` 9f, `session_context`
  RESULT PENDING). Cost of leaving E3 open: per M7, round-2 accepts are unwatched.
- F2 - who is owed. (a) the latest worker of every agent kind on the task (recommended: rule 9f closes the task for all). (b) only
  the verdict line's own agent: no WARN for a running critic-entry.
- F3 - which verdicts. (a) `accepted` only. (b) `accepted` and `rejected` (recommended: the finding names both; one row).
- F4 - placement. (a) the validator's accepted-line channel (recommended: the row's owns; reaches write, commit, merge, CI). (b)
  `journal_echo.py` beside R3 MIRROR: write moment only, outside the owns.
- F5 - strength. (a) WARN (recommended: the row says WARN; lost ends are common, M6: 2 of 7 sampled accepts would WARN). (b) a
  refusal in `journal_write.py accept` with a door flag: prevents, but widens owns to the one writer and blocks every lost-end
  accept until a CLI `returned`.
- F6 - the late `returned` after an `accepted`: (a) keep rule 9f (recommended for this node): the hook prints one `returned NOT
  written` at the stop and one `returned lost` at the 24 h prune. (b) let a `returned` follow an `accepted` (never reopening) so the
  real end is recorded: a 9f change in another node.

Questions beyond this card: Q1 - the cause of M6's missing ends (t-1407, t-1410) is not measured: `estimate, not verified`; the
Lead reads the forge lock dir `warn.log` (check 48c) for those refs. Q2 - `basis: critic:t-NNN` on `accepted` is not the matrix's
critic basis (section 5): a pile item if the Lead wants the matrix to read it.

## 10. Noticed, not widened

- D-0046 (`DECISIONS.md:36`) says a fix round is a fresh worker `delegated` with `attempt: n+1` after `rejected`; M7 shows fix rounds
  run as resumes with neither line. This is the Lead's process question; it also decides how much E3 matters.
- The pile row still names `CLAUDE.md` as the carrier of items 2-3; the SHAPES table and rule 4 now live in `COORDINATOR.md`.
- Hook-era rate of the WARN over the whole journal: `estimate` (sample 2 of 7, M6). The Lead's command: the narrow call of
  section 4 acceptance 3, after the merge.

## 11. Reading trail

Read: pile row :47, :41, :60, :1-12; the finding (whole); `journal_validator.py` :1-270 (docstring), :639-680, :738-795,
:890-980, :1056-1190, :1400-1535, :2530-2560; `journal_write.py` :1-85, :486-620, :812-829; `journal_hooks.py` :92-126,
:255-324, :374-425; `dod_gate.py` (Grep `record_returned`, `skipped_after_2_blocks`: :825, :611/:645 return 0);
`test_journal_validator.py` :37-60, :630-700, :1720-1764; `test_forge_metrics.py` :495-615; `COORDINATOR.md` :149-162,
:352-411; `docs/RUNBOOK.md` :124-133; `docs/TESTING.md` :43-150, :213-250; `ai-packages/qa-factory/design/architecture.md` (Grep
AR-1/2/13/15/18/22/29, § A :70-72); `DECISIONS.md:36`; `tools/install_parity_anchors.json:512-525`; `journal_echo.py:1965-2004`;
a recent card's form (`20261118-fg7-81-named-by-pointer-check-card.md` :154-188).
Greps (positive controls named in sections 0 and 6): journal event counts; worker refs of t-1407/t-1410 in the main journal and the
worktree copies; `basis` on rejected; witness labels; `matrix_warnings`/`decide_with_warnings` callers; `journal_validator` readers in
tools, .githooks, .claude/settings.json; date patterns in test fixtures; `toolkit/` (absent in this tree, control `tools/journal_v*.py`).
Needed beyond the manifest: `tools/journal_hooks.py`, `tools/dod_gate.py`, `tools/journal_echo.py`, `tools/test_forge_metrics.py`,
`tools/test_journal_hooks.py`, `logs/journal/dev1.jsonl` (Grep only), `COORDINATOR.md`, `DECISIONS.md`, `docs/RUNBOOK.md`,
`docs/TESTING.md`, `ai-packages/qa-factory/design/architecture.md`, `tools/mechanism_gate.py`, `tools/install_parity_anchors.json`.

## 12. Lead decisions (18.11, Lead 501cb4e0, accepted; «решила сама»)

- F1 (c): (a) in this node -- the journal `returned` line is the worker's last line (pure, the same on write, commit, merge and
  CI); the resumed-worker stop (E3, M7) becomes a separate pile row (one journaled stop per resume), not this card.
- F2 (a) the latest worker of every agent kind on the task. F3 (b) `accepted` and `rejected`. F4 (a) the validator's
  accepted-line channel. F5 (a) WARN. F6 (a) rule 9f unchanged here.
- L1: `critic:<critic task id>` (16 of 31 lines already; traceable). L2: the recommended door (BATCH CANON in the witness of the
  batch's last `accepted` written after the canon; else in the `notes` of the next batch event).
- Order: the builder card runs now (journal_validator.py and its test are mechanism files: the builder stages, the Lead commits).
  The Lead text edits of section 5 land after FG7-14 card A merges (both edit COORDINATOR.md), with the DOC-DISPATCH key witness.
- Q2 (critic:t-NNN on `accepted` read as the matrix's critic basis) goes to the pile with the E3 row.
