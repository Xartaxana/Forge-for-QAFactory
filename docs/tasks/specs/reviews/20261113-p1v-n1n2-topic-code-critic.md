# t-528 — topic code critic: P1-v N1 (process rows, run class) + N2 (resume_kind)

Reviewed tree: worktree `p1v-n2` at `fa69bd1` (contains N1 `b63a226`, N1 fix round `30c2500`, N2 `fa69bd1`; base `bea0bb0` = N0 head).
Diff `git diff bea0bb0 fa69bd1 -- ai-packages/qa-factory` holds only N1+N2 commits (log checked: 3 commits, no N0 lines).
Spec: `docs/tasks/specs/20261113-p1v-run-scoreboard-spec.md` §2 W0 table (R-1..R-9), W1, W2, §7.10, §7.11, §7.12, §8 rows N1/N2, U1 row, §8.1(v), F17/F18.

**Verdict: ACCEPT WITH FIXES (fit_with_fixes) — 0 BLOCKER, 3 FIX, 5 QUEUE.** Acceptance belongs to the Lead tier; this is an input.

## Answer to the question

- N1 meets its row (a)–(e) with one deliberate, Lead-authorised divergence from §2 W1 text (end row carries more keys and `run_class`; see FIX-1 — the code is right, the spec carrier is now stale and N4 would be built against it).
- N2 meets rows (a)–(e): every caller road passes its token, R-9 is `service_cut`, out-of-table / wrong type / broken table → `unclassified` + one note, the table read through `driver_journal.run_record`, non-resumed rows carry no key, the enumeration was re-run with positive controls.
- AR rows named in the commits (AR-1, AR-13/14, AR-22, AR-23, AR-25, AR-28) are kept (q10 below).
- Class over resume roads: complete for the nine spec roads; a TENTH road exists (the transient retry) — I agree it is a new road (FIX-2).

## Findings

### FIX-1 — spec §2 W1 / §8 N4 describe a process-row shape the code no longer has (Lead-tier carrier, before the N4 dispatch)
- Code: `driver_journal.py:522-550` `process_end_row` writes `package`, `config_sha`, `answer_file`, `run_class`, `start_row_written` besides `since/process_code/question_kind`; `driver_machine.py:1792-1797` `put` skips any row while the state folder is absent.
- Spec still says (§2 W1, lines 192-194, 207): end row = `{kind,event,since,process_code,question_kind}`, and `run_class` is "Written into the `process` start row ONLY … `run_counters` reads it from there"; "two start rows with different values → `mixed`".
- Failure scenario: a fresh story run in ONE process (the common case). Folder absent at `run()` entry → no start row (`put` returns False); the folder is created during the run; the end row carries `run_class`. An N4 builder following the spec reads `run_class` from start rows only → finds none → the run is `unknown`/absent → every fresh single-process live run is "not comparable" on the scoreboard. Same for driver windows (`since` read from start rows).
- The divergence itself was a Lead decision (journal t-502: "end row carries start time and start_row_written"; the identifying keys came with it). The fix is a Lead-tier edit of §2 W1 (end-row shape; `run_class` computed once, carried by both rows; `mixed` defined over start AND end rows of distinct processes) and of the N4 row ("works from the END row; a start row without an end row = killed process"). The N1 report already flags this for N4 (`20261113-p1v-n1-report.md:139`); a report line is not a carrier N4 reads.

### FIX-2 — the tenth resume road: the in-call transient retry writes `unclassified` (Lead decision; queued question — I do not decide it)
- Code: `driver_runner.py:991-997` — a call that WORKED and then got a `transient` infra failure is retried by resuming `result["session_id"]` with `driver_resumed=True`; `how = ""` → the row says `resume_kind: unclassified` (+ note `'(none)'`).
- Is it a new road? **Yes.** It is a distinct site that turns a call into a resumed row; it is NOT in the W0 nine (R-9 is only the `prior`/interrupted-record branch, `driver_runner.py:860-864`). The W0 enumeration missed it because both Greps look for `resume=` call sites and `.resume_with(`; this branch assigns `attempt_resume` inside `run_claude` — a recon gap of the spec, not of the builder.
- Its class: same as R-9 — the driver's own resume after the model service broke the call; no refusal, no person; `checks` is already absent there (`driver_resumed` True, `:958-959`). Recommendation (for the Lead): `service_cut` (one road for "the service cut the call, the driver resumes its own session"), or a tenth token `service_retry` if the in-call retry must be told apart from the cross-process one. Either way it is excluded from G1 returns.
- What `unclassified` means for the counts today: (i) G1 is unaffected (no `checks` key on these rows); (ii) U1 (`spec:253`) counts `unclassified` resume kinds as a DATA-QUALITY defect and §8.1(v) (`spec:461`) treats a rise as a finding — normal service hiccups would raise that line, so the detector "a caller lost its token" is blinded by infrastructure noise; (iii) concrete loss of the console signal: `resume_kind_of` dedupes notes by token, and both "transient retry" and "a caller that passes no token" have token `""` (`driver_runner.py:792-798`) — after one transient retry in a process, a later caller that forgot its token prints NO note (the row still says `unclassified`).
- When the Lead names the token: one test row pinning the retry row's `resume_kind` (there is none today; the current `unclassified` behaviour is unpinned).

### FIX-3 — two readers of `run-record.json` lists validate differently (minor; quality / one road; within N1+N2 owns, builder fix round)
- `driver_journal.py:465` (`run_classes`): accepts `[]` and empty-string names. `driver_runner.py:786` (`resume_kinds`): refuses `[]` and empty strings ("not a non-empty list of names").
- Scenario: `"run_classes": [""]` is accepted as a table (no note) while `"resume_kinds": [""]` is refused with a note — the same file, the same shape, two verdicts. Not a wrong output today (an empty name can never equal a non-empty stripped env value), but two hand-written validators of one data file are the beginning of two roads (AR-13/AR-15).
- Fix: one helper in `driver_journal` (e.g. `run_record_names(key) -> (tuple, note)`), called by `run_class` and `resume_kind_of`; one strictness. Optional in the same round: the literal `RESUME_UNCLASSIFIED = "unclassified"` (`driver_runner.py:773`) can stay (the fallback must exist without the table — the builder's own note is correct).

### QUEUE-1 — N4 counting rule: a retried caller resume yields TWO rows with the same `checks` and `resume_kind` (to the N4 spec, §7.12)
- `driver_runner.py:1003-1008`: a CALLER resume that hits a transient failure without having worked is retried with `driver_resumed=False`, `how = base_how`; the row writer `:958-960` emits `checks`, `checks_n` and `resume_kind` again, with `retry: 1`.
- Scenario: R-1 handoff resume → attempt 0 transient (not worked) → attempt 1 succeeds. Two `kind: role, resumed: true` rows, both `checks: ["s5_precheck:manifest"]`, both `resume_kind: handoff_findings`. G1 as written ("resumed calls naming the check", `spec:246`, §7.12) counts two returns for one. Pre-existing for `checks` since N0 (the N0 critic did not raise it); N2 extends it to `resume_kind`. Rows carry `retry`, so the reader can count one return per caller resume (e.g. rows with `retry == 0`, or group by dispatch + launch sequence). A spec line for N4, not a fix here.

### QUEUE-2 — `plans/features.json` has no glob for `references/run-record.json` (the commit-hook WARN)
- Source: `tools/forge_metrics.py:1189-1195` offender class (b) "new package file … matches no feature". It is a forge-metrics attribution check: it does not touch package behaviour or acceptance. It matters only in that commits touching the file are counted as unattributed work in Forge metrics. Fix at integration (forge file, integrator/Lead): add `references/run-record.json` to F06 "driver headless" (its readers are the driver's journal) — and `scripts/run_counters.py` when N4 lands.

### QUEUE-3 — private cross-module call `runtime_paths._package_fingerprint` (`driver_journal.py:490`)
- The value is the per-process cached hash (`runtime_paths.py:295-335`), which is what the spec wanted. A public name in `runtime_paths` (outside N1 owns) would end reaching into a private. The builder asked this as question 2; queue to whoever owns `runtime_paths`.

### QUEUE-4 — the "a row never creates the story folder" guard lives in two copies
- `driver_machine.py:1794` (`put` in `run`) and `:1843` (`person_stop_record`): the same `if not self.state_dir.is_dir()` guard before a `journal_run`. Two lines each, so not a defect now; a shared `journal_if_story(row)` would be the one road if a third writer appears (axis "torn tail"/`journal_run` family). `person_stop_record` is outside N1 owns.

### QUEUE-5 — scope question (spec, not this diff): runs without the driver journal
- W1/W2 write into `driver-runs.jsonl`, which only the driver road has; W3 was placed explicitly so the skill road writes alike (P31, `spec:224`). The spec does not say what `run_counters` prints for resume kinds / process windows of a run with no driver journal (n/a vs 0). Out of this diff; a line for the N4 spec so the answer is `n/a`, never 0 (AR-28).

## Checked and found correct (traced)

- `run()` (`driver_machine.py:1775-1828`): start row before `progress_line`; two assignments + the closure before the outer `try`; inner `except KeyboardInterrupt: person_stop_record(); raise` runs before `finally` → Ctrl-C order is start, stopped_by_person, end(`process_code` null). An exception propagates unchanged; `finally` catches only `OSError` and `KeyboardInterrupt` around the end row, so it never replaces the exception in flight. `process_end_row` cannot raise for an unreadable question file (`OSError` caught; `errors="replace"`).
- Forbidden keys: neither row carries `exit_code`/`is_error`/`infra`/`session_id`/`dispatch*`/cost. Traced readers: `collect_stall._is_outcome` (`collect_stall.py:213`, needs `is_error|exit_code|infra`) and `driver_timing._hops` (`driver_timing.py:236`, needs `exit_code`) pass process rows by; `retro_numbers` resume readers filter `kind == "role"` (`:692`, `:1708`).
- `run_class` (`driver_journal.py:448-483`): absent/blank → `live`; exact table name → it; anything else (incl. `live`, ` dry `, `DRY`) → `unknown` + one note quoting ≤ 60 chars; broken table → `unknown` for every value (errs toward "not comparable", as the spec's direction requires). `config_sha` reads `self.project` (set at `driver_core.py:456`); `answer_file` reads `self.flags.answer` (same attribute `run`'s loop uses, `driver_machine.py:1857`). `--dry-run` goes to `describe()`, not `run()` (`story_run.py:172-174`) — no process rows on a dry run.
- N2 tokens at every site: R-1 `driver_dispatch.py:555`, R-2 `:585`, R-3 `:1075`, R-4 `resume_with` passes `kind` (`:2123`), R-5/R-6 `driver_machine.py:277/292`, R-7 `driver_dispatch.py:3674`, R-8 `driver_machine.py:553-554`, R-9 `driver_runner.py:864`. The `how` variable mirrors `why` in every branch: fresh-after-loss resets both (`:980`), `base_driver_resumed` fallback restores `service_cut` (`:1002`), caller retry restores the caller token (`:1008`). Conductor calls (`driver_conductor.py:336`, `driver_stage_s8s9.py:447` with `resume_key`) can only be resumed through R-9 → `service_cut`; fine.
- One writer of the key: the only writer of `"resumed"`/`resume_reason` rows in non-test package code is `run_claude` (Grep `"resumed"|resume_reason`, case-insensitive, over `scripts/[a-z]*.py`: package hits only in `driver_runner/driver_dispatch/driver_machine/retro_numbers`; `retro_numbers` only reads).
- No regex over refusal text added: `git diff bea0bb0 fa69bd1 -- driver_{runner,dispatch,machine,journal}.py | grep -E '^\+.*\bre\.(compile|match|search|findall|sub)'` → 0; positive control, same pattern over `driver_dispatch.py` → 10.
- The builder's "audit_rules red is not mine" (a negative claim, unverified in the report): reproduced. `test_audit_rules.py` on an archive of `bea0bb0` → the same 4 FAILs with the same numbers (`qa-failure-analyst: 18,426 vs 18361`), `371/375 ok`. Pre-existing; not N1/N2.

## Standing questions

- **Duplication and consistency (item 6):** FIX-3 (two validators of one file's lists), QUEUE-4 (folder guard twice). Grepped: `is_dir()` guards in `driver*.py`; `isinstance(names, list)` / `all(isinstance(` in `driver_{runner,journal,machine}.py`; `run_record(` callers. Nothing else found.
- **Code quality (item 7):** acceptable. `resume_kind_of` caches in `self.__dict__` so `__new__` rigs work (justified); lazy `import driver_journal` matches the existing pattern at `driver_runner.py:658`. Small smell: in `run_claude` the word `unclassified` now means two vocabularies (infra kind `infra["kind"] == "unclassified"`, `:973/:1011`, and the resume token) — readable from context, no action. Private call: QUEUE-3.
- **Architecture q10:** AR-1 kept (closed tables `run_classes`, `resume_kinds` are data); AR-13/AR-14 kept (one loader `run_record`, one class reader `run_class`, one row writer `journal_run` / `run_claude`); AR-22 readers pending N4 as declared in §7.11 (and the changelog says so); AR-23/AR-28 kept (null/`unknown`/`unclassified` with a note, never a default pass); AR-25 kept (a killed process = start without end, read as such). AR-15 at risk only by FIX-3.
- **Judgment q11:** none added. Tokens name the SITE structurally; no refusal text is classified; census `24/24` re-run green.
- **One road q12 (P31):** the resume road is one helper for all sites (`resume_kind_of`); the run class one reader. The tenth road writing a different (fallback) value than its class twin R-9 is exactly a "two roads for one thing" — FIX-2. The driver-only carrier vs the skill road: QUEUE-5 (spec scope; the shared mechanism is reached on the driver road; no exclusion is coded here).

## Class completeness (resume roads)

Enumeration re-run by me (case-insensitive Grep over `scripts/[a-z]*.py`, positive controls `driver_dispatch.py:552` and `driver_machine.py:277` found):
`resume=[a-z]` → caller sites `driver_dispatch.py:552, 583, 1072, 2119`, `driver_machine.py:551` (+ plumbing in `driver_runner.py`); `.resume_with(` → `driver_dispatch.py:3671`, `driver_machine.py:277, 292`; `run_claude(` without `resume` → `driver_dispatch.py:714`, `driver_conductor.py:336`, `driver_stage_s8s9.py:447` (resumable only via R-9). Inside `run_claude`, the places that set `attempt_resume`: `:861` (R-9), `:978` (fresh, clears), `:992` (**tenth road**, FIX-2), `:1001` (R-9 fallback), `:1005` (caller retry, QUEUE-1). Nine roads covered with their tokens; one uncovered road queued to the Lead with a recommendation. SIBLING_MAP: the "where the story is" axis (`docs/SIBLING_MAP.md:136`, readers of `driver-runs.jsonl` incl. `retro_numbers.resume_metrics`) — the new key is additive and `resume_reason` stays; the torn-tail axis (`:458`, `append_jsonl_line`) — writer unchanged (`journal_run`).

## Trail

Read: the N1+N2 diff (all package files), `driver_runner.py:770-1011`, `driver_dispatch.py:700-724`, `driver_conductor.py:330-341`, `driver_stage_s8s9.py:444-451`, `story_run.py:140-175`, `driver_timing.py:205-254`, `retro_numbers.py:1412-1433`, `runtime_paths.py` (fingerprint cache), `collect_stall.py` row filters (Grep), spec §2 W0-W2, §7.10-7.12, §8 N0-N4, U1/G1 rows, both builder reports, N0 critic verdict (Grep), `tools/forge_metrics.py:1170-1214`, `plans/features.json`, `docs/SIBLING_MAP.md` (lines 136/156/378/380/412/458), journal line t-502.

Reruns:
- `python -B scripts/tests/test_driver_stop_record.py` (worktree p1v-n2, HEAD fa69bd1) → `=== test_driver_stop_record: 239/239 ok ===`
- `python -B scripts/tests/test_judgment_census.py` (same) → `=== judgment_census: 24/24 ok ===`
- `test_audit_rules.py` on `git archive bea0bb0` in the scratchpad → `=== audit rules (...): 371/375 ok ===`, same 4 FAILs as the builder reported at fa69bd1 (pre-existing)
- regex-addition grep over the diff → `0`; positive control → `10`

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "FIX-1 (Lead-tier carrier, before N4 dispatch): amend spec 2 W1 and the N4 row - the end row carries since/package/config_sha/answer_file/run_class/start_row_written and is the row N4 works from; run_class is computed once and carried by both rows; mixed is defined over start and end rows. Today the spec says run_class is in the start row ONLY, and a fresh single-process run has no start row (driver_machine.py:1792-1797, driver_journal.py:522-550).",
    "FIX-2 (Lead decision, queued): the transient in-call retry at driver_runner.py:991-997 is a tenth resume road writing unclassified; recommend service_cut (same class as R-9: driver's own resume after the service broke the call, no checks key) or a tenth token; add one test row pinning its token. As unclassified it pollutes U1 and calibration 8.1(v) and shares the note-dedup key with a caller that forgot its token.",
    "FIX-3 (builder fix round, minor): one list validator for run-record.json keys in driver_journal used by run_class (driver_journal.py:465) and resume_kind_of (driver_runner.py:786); today one accepts [] and empty names, the other refuses them."
  ],
  "class_completeness": "Nine spec roads R-1..R-9 carry their tokens at every site (re-enumerated with positive controls). A tenth road exists inside run_claude (transient retry of a call that worked, driver_runner.py:992) - writes unclassified, queued to the Lead (FIX-2). A retried caller resume (driver_runner.py:1003-1008) repeats checks and resume_kind with retry=1 - a counting rule for N4 (QUEUE-1). Sibling map: driver-runs readers axis (SIBLING_MAP:136) additive key, resume_reason kept; torn-tail writer axis unchanged.",
  "trail": {
    "read": [
      "git diff bea0bb0 fa69bd1 -- ai-packages/qa-factory (worktree p1v-n2)",
      "ai-packages/qa-factory/scripts/driver_runner.py:770-1011",
      "ai-packages/qa-factory/scripts/driver_journal.py:426-550",
      "ai-packages/qa-factory/scripts/driver_machine.py:1775-1845",
      "ai-packages/qa-factory/scripts/driver_dispatch.py:700-724",
      "ai-packages/qa-factory/scripts/driver_conductor.py:330-341",
      "ai-packages/qa-factory/scripts/driver_stage_s8s9.py:444-451",
      "ai-packages/qa-factory/scripts/story_run.py:140-175",
      "ai-packages/qa-factory/scripts/driver_timing.py:205-254",
      "ai-packages/qa-factory/scripts/runtime_paths.py:295-335",
      "docs/tasks/specs/20261113-p1v-run-scoreboard-spec.md (2 W0-W2, 7.10-7.12, 8 rows N0-N4, G1, U1, 8.1)",
      "docs/tasks/specs/reports/20261113-p1v-n1-report.md",
      "docs/tasks/specs/reports/20261113-p1v-n2-report.md",
      "docs/tasks/specs/reviews/20261113-p1v-n0-code-critic.md (grep)",
      "tools/forge_metrics.py:1170-1214",
      "plans/features.json",
      "docs/SIBLING_MAP.md (lines 136, 156, 378, 380, 412, 458)",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B scripts/tests/test_driver_stop_record.py (worktree p1v-n2 at fa69bd1)", "result": "=== test_driver_stop_record: 239/239 ok ==="},
      {"command": "python -B scripts/tests/test_judgment_census.py (worktree p1v-n2 at fa69bd1)", "result": "=== judgment_census: 24/24 ok ==="},
      {"command": "python -B scripts/tests/test_audit_rules.py on git archive bea0bb0 (scratchpad)", "result": "=== audit rules: 371/375 ok === - same 4 FAILs (A22 ratchet, qa-failure-analyst 18,426 vs 18361) as the builder reported at fa69bd1: pre-existing"},
      {"command": "git diff bea0bb0 fa69bd1 -- driver_{runner,dispatch,machine,journal}.py | grep -E added re.compile/match/search/findall/sub", "result": "0 (positive control on driver_dispatch.py: 10)"}
    ]
  }
}
```
