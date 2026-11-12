# t-147 — critic diff gate, batch onboarding-forge/2 (streams hot, tests, small, handoff)

One pass per topic (R13-g). Diffs read: `git -C <worktree> diff origin/main...HEAD` for of-hot (26ee0aa, 336d909),
of-tests (465db10, ae1c141, 80fa246, 0724236), of-small (d896052, 93901cc) and of-handoff (d0c5311, a4e5949, d2621c5).
SC2-32, TQ1-28 and RC1-15 are out of scope. Node rows: `plans/piles/onboarding-forge/batch-2-onboarding-roles-forge-p3.md`
rows 40-61.

## Verdict lines

- **hot (DC1-28, DC1-27): NEEDS WORK, 1 blocking finding (H1).** Fixes H2-H5 do not block.
- **tests (OH3-25): ACCEPT WITH FIXES.** T1 does not block.
- **small (CX2-12, EP1-19): ACCEPT WITH FIXES.** S1-S3 do not block the merge. S2 is a carrier the coordinator has to write.
- **handoff (SC2-42, HF8-28 F8/F9/kept echo, HF8-29): ACCEPT WITH FIXES.** HO1 should be fixed in this round (it is the node's own
  invariant on the node's own surface). HO2 does not block.
- Batch as a whole: **NEEDS WORK** until H1 is fixed. Accepting the batch is the coordinator's call, not mine (rule 6).

## Findings

### hot

**H1 (BLOCKING). The DC1-27 pins sit in a quarantined file, so the canon never runs them. The quarantine edit also has no `quarantine-edit:` line.**
- Where: `scripts/tests/test_answer_rework_pairs.py`. `one_carrier_each()` holds checks D1 (`Driver.EARLIER_ANSWER is
  question_register.EARLIER_ANSWER_MARK` and the literal appears in one script only) and D2 (an owner added to
  `controller.ANSWER_REWORK_OWNERS` is taken by `_owed_rework_parts` and by `Driver.merge_answer_rework`). The same commit
  also changes the file's last check from `Driver.__dict__[...]` to `inspect.getattr_static`.
- Evidence: the `quarantine` section of `scripts/tests/test-layers.json` holds the key `test_answer_rework_pairs.py`, so this
  is a quarantined file (cohort 8073673, entered 2026-11-11). A grep for `EARLIER_ANSWER_MARK|ANSWER_REWORK_OWNERS` over
  `scripts/tests/*.py` finds exactly one file, this one. The positive control: the same grep finds this file. The full message
  of 336d909 has no `quarantine-edit:` line. `tools/test_quarantine.py:1632` refuses such a commit with
  "expected a line 'quarantine-edit: test_answer_rework_pairs.py -- <reason>'". docs/TESTING.md:67 says a test does not come back
  from quarantine.
- Why it blocks: the node's only proof of AR-13/AR-19 (the commit's own `architecture:` lines) is a pin that runs only in the
  twice-weekly `quarantine-watch`. A future copy of the mark, or a second owner table, passes the canon. The node row asks for
  exactly this pin (FR-54, FR-28).
- Expected fix: move `one_carrier_each` (D1, D2) into a keep file. Candidates are `test_gate_words_road.py` (keep, it already
  drives the gate rework) or a keep test of `question_register`. Then either revert the edits to the quarantined file, or keep
  them and carry `quarantine-edit: test_answer_rework_pairs.py -- <reason>` in the commit message. The getattr_static repair of a
  quarantined test is itself a quarantine edit.

**H2. The refusal registry row is stale for the new branch.**
- Where: `refusal_registry.py:121` (`SG-resume-stopped`). Its `refuses` field still says "only open dispatch is stopped
  (blocked/paused) ... names `story_step.py resume`". The same call (`stopped_text`, `_stopped_refusal`) now also refuses
  an `incomplete` dispatch's agent, and that refusal names the `recover` door (AR-18, FR-1: the registry describes what is refused
  and by which door).
- Expected fix: extend that row's `refuses` (and `unpassable_because`, if needed) with the incomplete branch and its
  `controller.py --operation recover` door, or add a row of its own.

**H3. On the controller's side, `incomplete_words` names `recover` even when `recover` prints no packet.**
- Where: `controller.py` `_resume_status_problems`, `if status == "incomplete": return [(StateConflict, self.incomplete_words(did))]`.
- Trace: take an incomplete dispatch whose `reason == BUDGET_EXHAUSTED`. `_resume_status_problems` returns `incomplete_words`.
  `_resume_problems` marks the stop checks "did not run", so the budget sentence of `_resume_stop_problems` is never reached.
  Meanwhile `_retry_packet` returns None for `BUDGET_EXHAUSTED` (`controller.py:8783`), so `recover` prints no packet for it. The
  same holds for a later record of the same stage and role (`retry_packets` skips it). Either way the refusal names a dead door
  (FR-2).
- Contrast: the guard (`_incomplete_target`) checks `retry_packets` and ALLOWs exactly these cases, and test K1-10 E4 pins that.
  The commit's AR-25 line ("one move (recover) on both the controller and the guard side") therefore holds on the guard's side
  only. This is pre-existing, but the node row says "одна дверь `recover` в тех же словах с обеих сторон; взаимодействие с
  `retry_packets` оценивает узел".
- Expected fix: the incomplete branch of `_resume_status_problems` names `recover` only when `retry_packets` lists the
  dispatch. Otherwise it names the door that applies: the budget sentence for `BUDGET_EXHAUSTED`, and `next` for a later record.
  Fix this round, or queue it as a node with an owner.

**H4. Duplication: `_incomplete_target` clones the head of `_stopped_target`.**
- Where: `stage_guard.py` `_incomplete_target` and `_stopped_target`. Both run the same 7 statements: records, receipts `extra`,
  `rows`, the non-dict guard, the "exactly one open, the rest `_SETTLED_BESIDE_STOP`" test and `ident`. Only the status set and
  the door check differ.
- Expected fix: one helper, `_one_open_record(event, ticket, target, controller, statuses) -> (key, rec) | None`, read by both.
- A third spelling of the same door sentence also stands at `controller.py` `_resume_stop_problems`:
  `retry = f"the retry packet \`controller.py --task-root {root} --operation recover\` prints"`. It sits beside
  `incomplete_words`, the sentence the commit calls "the ONE" (AR-15). Make one carry the other.

**H5. The hot stream's witness is narrower than its witness scope.**
- The summary I was given carries only `test_resume_stopped` 105/108 -> 109/109.
- `scenario_walk.py --witness-for scripts/stage_guard.py ...` prints the three scenario tests, `test_judgment_census`,
  `test_refusal_registry`, `test_stage_guard`, `test_resume_story_isolation` and more. The two test files DC1-27 refactored
  (`test_gate_words_road`, `test_gate_decision_manual_pass`) carry no witness in the summary.
- I re-ran five of them myself, all green (see the trail). The builder's report still has to attach its own `--witness-for` run
  (rule 7, plans/builder-rules.md 7b).

### tests

**T1 (does not block). Two inline register writers are left, with no carrier.**
- Where: `fixtures/manual-evidence/scaffold.py:369` (copies an oracle register into `work/requirements-register.md`) and
  `test_brief_pack.py:3201`. The second writes a `# register` stub only to test `file_lines` presence; I judge it
  not applicable (it is not a story register).
- Status of the rest: the commits say 7 of the 13 files are quarantined (verified: traceability_report,
  validate_artifacts_report, s3_s4_chain, s1_s2_contract, exit_gate_grounding, judge_results and judge are QUAR). That is correctly
  not applicable. `scaffold.py` is not quarantined and is not queued anywhere in the batch's «Остатки».
- Expected fix: route `scaffold.py` through `harness.write_register(task, register, head="")`, or put a leftover row on it.
- Other notes: `test_grounding_table` and `test_report_facts` were migrated with py_compile as the only local witness. They are slow
  files and CI judges them, which is legitimate, but the batch's BATCH CANON must show them green. The LF change (0724236) is a
  no-op on CI's Linux. On Windows it makes the file bytes equal `reg.encode()`, which is what `register_sha256` in
  `test_grounding_table` hashes: consistent. The 60-line split is verified: the longest function in `test_sizing.py` is now 59
  lines (`oh3_34_...`), measured with ast.

### small

**S1. The "local" reading of a zone-less time contradicts the data and the sibling reader of the same field (CX2-12's own class).**
- Where: `dispatch_liveness._stop_records` (`epoch_of(record["ts"], naive="local")`, "the hook's own clock") and
  `dispatch_liveness.driver_session_end` (`naive="local"`, "the driver's own clock"), plus the `NAIVE_READINGS` comment in
  `codex_usage.py`.
- What the writers do (rule 13, read from the writers): the hook journal is written at `hooklib.py:2494`,
  `datetime.now(timezone.utc).isoformat(...)`, which is UTC-aware. `driver-runs.jsonl` is written by `driver_runner.journal_run`
  with `_now()` (`driver_core.py:260`, `datetime.now(timezone.utc)`), also UTC-aware. The other reader of `driver-runs.jsonl`,
  `driver_journal.parse_ts` ("The one reader of the driver's journal"), reads a naive stamp AS UTC.
- So after this node, two readers of one field still disagree on a naive time. That is exactly what the row asked to end
  ("названным смыслом на каждого читателя (данные, не догадка)"). The commit says it chose "each reader's existing meaning kept".
  Real rows carry `+00:00`, so live behaviour does not change; the named meaning is the defect.
- Expected fix: `naive="utc"` at both sites, with the comment corrected. Better for `driver_session_end`: read `ts` through
  `driver_journal.parse_ts` (AR-13; `collect_stall.py:27` already records "driver_journal calls itself its one reader" as a
  known gap).

**S2. The AR-13 claim overreaches, and the rest of the class has no carrier.**
- The commit says "a stored time is read only through codex_usage.epoch_of / iso_of". A census over package scripts finds
  `fromisoformat|strptime` in 39 files outside the reader (counted with grep -c over `scripts/*.py`, roughly 60 sites). Among
  them are two exact clones of `codex_usage.stamp`: `driver_journal.parse_ts` and `cost_capture.parse_ts`.
- I find no "time readers" axis in docs/SIBLING_MAP.md, no finding file and no batch row. My searches: a case-insensitive grep of
  `plans/piles/*/findings` and the batch for "time reader|epoch_of|читатели времени", with the positive control that the CX2-12
  finding itself is found. The dispatch says the axis "is queued to Lead", but no carrier exists yet.
- Expected: narrow the `architecture:` claim to the readers the row named, and write the queue carrier: one finding with the
  census list plus a row in a batch that is not yet taken, and the axis proposal to Lead. The class is not complete and not
  properly queued until that file exists. Writing the carrier and deciding on the axis belong to the coordinator and the Lead,
  not to me.

**S3. EP1-19 puts one project's fact into a universal charter (P2, AR-3).**
- Where: `agents/qa-runner.md`, the new bullet: "(`full_reindex` is a query parameter, not a JSON body field)". That is a fact
  about the MyBooks SDK (run 14857), stated to every project as if it were a rule.
- Expected fix: a generic example, e.g. "a flag the SDK sends as a query parameter goes in the query string, not in the JSON
  body". The craft rule stays. Role-load: +80 tokens against a slack of 73 left on that row (commit: 15971 -> 16051, row 16124),
  and the process ratchet is unchanged. A shorter wording also returns slack.
- Note: `codex_usage.py` is an odd home for "the ONE reader of a stored time". `story_progress` now imports a Codex-usage module
  for a generic time parser. I record it as a placement question for S2's node, not as a fix.

### handoff

**HO1 (fix this round). `_near` still offers a row-0 path the writer does not write. This is the F9 class at a sibling site in the same artifact.**
- Probe on `s8-scribe-to-gate-b`, `apply_values` on a fresh template:
  - `inputs_read.rows: x` -> "did you mean `inputs_read[0].rows`?" with fix `inputs_read[0].rows: <value>`.
  - Applying `inputs_read[0].rows` gives `applied 0` and the note "this form has no line for it ... not written".
  - Applying `inputs_read[1].rows` gives `applied 1`. This is my positive control, and it shows the probe tells the cases apart.
- Cause: `handoff_check._near` fills each leftover `[]` with `[0]` (`guess.replace("[]", "[0]")`) and never asks `_concrete`.
- The finding's item 5 ("подсказка никогда не называет путь, который писатель отказывает", for ALL items) and the row both name
  `_near`. The builder closed `_near` only for the list-of-values case (K9).
- Expected fix: `_near` runs its unindexed `[]`s through `_concrete(..., nodes, held=<the indexes the person wrote>)`. When the
  person's own index names a row that does not hold the field (`inputs_read[0].row`), it offers the row that does, or no path.
  Add one K row per case.

**HO2 (does not block). `_writable_lines` still echoes a line the writer drops without a refusal.**
- Probe: `_writable_lines(template(s8), s8, [inputs_read[0].rows: x, inputs_read[1].rows: y, no_such.field: z])` returns
  `['inputs_read[0].rows: x', 'inputs_read[1].rows: y']`. The refused `no_such.field` is dropped correctly (control). The first
  line comes back although the next apply writes nothing (note only).
- Expected fix: also leave out a pair whose trial apply has `count == 0` with a "not written" note.

**F9 / `_concrete` (question 4): checked, it holds.**
- Probe over every contract under `handoff.CONTRACTS`: for each list of rows, the paths `row_form` offers, and the `first`/`later`
  samples of `row_pair`, were applied to a fresh template. 244 combinations, 0 refused or unwritten.
- Positive control: the old F9 path `inputs_read[0].rows` (and `inputs_read[2].rows`) is detected as unwritten by the same probe.
- Unreadable template: `handoff.spec(c)` is `spec_of(template(c))`, so a template that cannot be read also leaves the spec
  empty. Then `_ValuesHints` gives the general text, and `values_skeleton` raises before it would use `nodes`.
- The `[0]` fallback of `_concrete(nodes=None)` is reachable only by a caller that passes its own spec without nodes. Every
  package caller passes nodes: `handoff_init._fill_line` passes `doc.nodes`, `check()` and `values_skeleton` pass
  `_template_nodes`. The invariant holds in the safe direction.
- Note: handoff_init reads `doc.nodes` (the form) while handoff_check reads the template's nodes. They agree on a fresh form;
  I record this without asking for a fix.

**SC2-42: checked, it holds.**
- `VOCAB_LIST` excludes `;`. A sweep of `handoffs/ references/ agents/ skills/` for a hand list ending in any other closer
  (`)`, quote, backtick, `.`, `]`) found none. The positive control: the same pipeline catches a synthetic `- a|b)`.

**HF8-29: done, as the coordinator recorded.**
- `spec_once`/`hint`/`aim` now live in `_ValuesHints`.
- `parse_values` is still 86 lines with three closures of its own (`bad`, `said`, `keep_all`). That is over the ~60 norm, but
  `--limits` passes. I record it under code quality and do not ask for a fix.

## Standing questions

1. **Each node vs its row:**
   - DC1-28: yes on the guard's side. The controller's side has a dead door (H3).
   - DC1-27: the code doubles were already gone on main (verified: `driver_machine.py:2417` `EARLIER_ANSWER = EARLIER_ANSWER_MARK`;
     `driver_dispatch.py:1902` reads `C.ANSWER_REWORK_OWNERS`). The one in-process runner is done. The pins are in quarantine (H1).
   - OH3-25: done for the keep files; `scaffold.py` is left (T1).
   - CX2-12: one reader and one renderer exist. The per-reader meaning is not grounded in data (S1), and the class is not queued
     (S2).
   - EP1-19: done, but with a project fact in it (S3).
   - SC2-42: done.
   - HF8-28: F8, F9 and the kept echo are done; `_near` F9-class is left (HO1, HO2).
   - HF8-29: done.
2. **stage_guard/controller (FR-1, FR-2, AR-17):** the guard's refusal says what is wrong (no agent holds the context), what it
   expects and the door (`recover` prints the packet, `--operation dispatch --input` sends it). The door is checked to open:
   `retry_packets`, the same reader `recover` prints (K1-10 asserts that `controller.recover()` contains the dispatch id). Every
   doubt is ALLOW, so no unknown refuses. The previous silent ALLOW of a message to a context-less agent is closed wherever a door
   exists. AR-17 holds: the guard leaves a move, with no new seam. Gaps: the registry row (H2) and the controller's dead door (H3).
3. **CX2-12 time direction:**
   - Right: `_epoch` (UTC, driver entry), `story_progress._epoch` (UTC; the progress readers' sources `_now()`/`created_at` are
     UTC) and `_row_time` (none).
   - Wrong in name: `_stop_records` and `driver_session_end` (S1).
   - Siblings outside the reader: `driver_journal.parse_ts`, `cost_capture.parse_ts`, `codex_usage.stamp` (kept for the money
     path) and about 39 files with `fromisoformat`/`strptime`.
   - Class: not complete and not properly queued (S2).
4. **HF8-28 F9 `_concrete`:** the invariant holds for the hint, the samples and the skeleton, including the unreadable-template
   direction. It does not hold at `_near` (HO1).
5. **DUPLICATION AND CONSISTENCY:**
   - H4 (guard head clone; a third spelling of the recover sentence).
   - S2 (`stamp`/`parse_ts` x2 clones remain).
   - Positive: the three in-process controller runners became one (`harness.run_controller_inprocess`). A grep of
     `CTL.main()`/`controller.main()` in tests found no fourth copy in the files I read; control: the harness itself is found.
   - `write_register` is one writer.
   - **CODE QUALITY:** `_concrete` builds its regex per index but is small (19 lines). `check()` is 186 lines (pre-existing,
     grown by two calls). `parse_values` is 86 lines. `_incomplete_target`'s docstring is accurate.
6. **AR-n / FR walks:**
   - Spot-checked. AR-13 in d896052 is false as worded (S2). AR-25 in 26ee0aa is true on the guard side only (H3). AR-9 in d2621c5
     is true for the hint and the skeleton but not for `_near` (HO1). AR-13/AR-19 in 336d909 are pinned only in quarantine (H1).
     AR-10/AR-11/AR-20 in 93901cc are true (process ratchet unchanged; role-load slack still positive).
   - JUDGMENT: DC1-28 "adds data check" is a join over records and retry packets, not over a role's words; the census is 22/22.
   - FR walks: no builder report with a per-section FR walk was attached (only the coordinator's summary), so the negatives in it
     could not be spot-checked. The `architecture:`/`judgment:` lines are what I checked.
   - **ONE ROAD (item 12):** no branch on a language, runner or project name in the four code diffs (read in full). The one
     project-specific item is S3's example text, which is not a branch.

## Class completeness (rule 5)

- DC1-28 class: "a message to an agent whose dispatch the controller will not resume". Covered by status: blocked/paused
  (SC2-17), incomplete (this node), superseded/released (retired by `_resumable_agents`), accepted (closed author).
  `returned_unaccepted`/`stale` with an `agent_id` was not walked by this node. The controller refuses `resume` for them with a
  `next` door; on the guard side I did not trace whether a message passes. This is a candidate for a scout question, not a verdict
  input.
- CX2-12: S2.
- HF8-28: HO1 is the same artifact (sweep-the-artifact-first).
- OH3-25: T1.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "H1 hot: DC1-27 pins (one_carrier_each D1/D2) live only in quarantined test_answer_rework_pairs.py, never run by the canon; commit 336d909 edits a quarantined file with no quarantine-edit line -- move the pins to a keep file and revert or justify the quarantined edit"
  ],
  "fixes": [
    "H1 hot test_answer_rework_pairs.py:one_carrier_each -> move to a keep file (e.g. test_gate_words_road.py); quarantine-edit line or revert (BLOCKS)",
    "H2 hot refusal_registry.py SG-resume-stopped row: name the incomplete branch and its recover door",
    "H3 hot controller.py _resume_status_problems incomplete branch: name recover only when retry_packets lists the dispatch; else the budget sentence or next (or queue as a node)",
    "H4 hot stage_guard.py _incomplete_target/_stopped_target: one shared head helper; one spelling of the recover retry sentence (incomplete_words vs _resume_stop_problems retry)",
    "H5 hot: attach the scenario_walk --witness-for run for stage_guard.py/controller.py/harness.py incl. test_gate_words_road and test_gate_decision_manual_pass",
    "T1 tests fixtures/manual-evidence/scaffold.py:369 -> harness.write_register, or a leftover row",
    "S1 small dispatch_liveness._stop_records and driver_session_end: naive=utc (writers are UTC-aware; driver_journal.parse_ts reads naive as UTC), fix NAIVE_READINGS comment; prefer driver_journal.parse_ts for driver-runs ts",
    "S2 small: narrow the AR-13 claim; coordinator writes the time-readers finding (driver_journal.parse_ts, cost_capture.parse_ts, codex_usage.stamp, about 39 files) and a batch row, axis proposal to Lead",
    "S3 small agents/qa-runner.md: replace the MyBooks full_reindex example with a generic query-vs-body example (P2, AR-3)",
    "HO1 handoff handoff_check.py:_near: concretize leftover [] and a person's index through _concrete; inputs_read.rows on s8 must not offer inputs_read[0].rows",
    "HO2 handoff handoff_check.py:_writable_lines: also drop pairs whose trial apply writes nothing (count 0, not-written note)"
  ],
  "class_completeness": "DC1-28: guard covers blocked/paused/incomplete/retired/closed; controller side of incomplete has a dead door (H3); returned_unaccepted/stale message path not traced (scout candidate). CX2-12: not complete, not queued -- no SIBLING_MAP axis, no finding carrier; about 39 files parse times outside epoch_of (S2). HF8-28: _near is an F9 sibling in the same artifact (HO1). OH3-25: scaffold.py left without a carrier (T1); 7 quarantined files correctly n/a.",
  "trail": {
    "read": [
      "of-hot diff origin/main...HEAD (controller.py, stage_guard.py, harness.py, test_answer_rework_pairs.py, test_gate_decision_manual_pass.py, test_gate_words_road.py, test_resume_stopped.py)",
      "of-hot stage_guard.py 1258-1330, 1630-1760; controller.py 6215-6260, 6362-6387, 8497-8566, 8767-8792; refusal_registry.py 121-129; driver_machine.py 2417; driver_dispatch.py 1889-1919",
      "of-tests diff origin/main...HEAD (harness.py, test_sizing.py, test_gate_question_form.py, test_grounding_table.py, test_oracle_provenance.py, test_report_facts.py); test-layers.json quarantine keys",
      "of-small diff origin/main...HEAD (codex_usage.py, dispatch_liveness.py, story_progress.py, qa-runner.md, test_dispatch_liveness.py); hooklib.py:2494; driver_core.py:259; driver_runner.py:401-404; driver_journal.py:1-30,321-333; collect_stall.py:24-29",
      "of-handoff diff origin/main...HEAD (handoff_check.py, handoff_init.py, test_handoff_values_refusal.py, test_handoff_inline_values.py); handoff_check.py _near 2458-2469, _open_row 2375-2400, aim 2255-2268; handoff.py template/spec",
      "batch-2-onboarding-roles-forge-p3.md rows 40-61; findings 20261101-hvosty-hf8-7, 20261101-parse-values-120; docs/SIBLING_MAP.md axis list; docs/tasks/critic-diff-brief.md; tools/test_quarantine.py:1515,1632; docs/TESTING.md:67-85",
      "commit messages 26ee0aa, 336d909, 465db10, ae1c141, 80fa246, 0724236, d896052, 93901cc, d0c5311, a4e5949, d2621c5"
    ],
    "reruns": [
      {"command": "of-hot: python -B tests/test_resume_stopped.py", "result": "109/109 ok"},
      {"command": "of-hot: python -B tests/test_gate_decision_manual_pass.py", "result": "105/105 ok"},
      {"command": "of-hot: python -B tests/test_gate_words_road.py", "result": "219/219 ok"},
      {"command": "of-hot: python -B tests/test_judgment_census.py", "result": "22/22 ok"},
      {"command": "of-hot: python -B tests/test_refusal_registry.py", "result": "223/223 ok"},
      {"command": "of-tests: python -B tests/test_sizing.py; test_gate_question_form.py; test_oracle_provenance.py", "result": "240/240, 297/297, 296/296 ok"},
      {"command": "of-small: python -B tests/test_dispatch_liveness.py", "result": "409/409 ok"},
      {"command": "of-handoff: python -B tests/test_handoff_values_refusal.py; test_handoff_inline_values.py", "result": "6458/6458, 83/83 ok"},
      {"command": "probe: every contract, row_form offered paths and row_pair first+later applied to a fresh template", "result": "244 checked, 0 dead; control inputs_read[0].rows on s8 -> applied 0 not written"},
      {"command": "probe: _near on s8 inputs_read.rows / inputs_read[0].row", "result": "offers inputs_read[0].rows, which applies 0 (HO1)"},
      {"command": "probe: _writable_lines s8 [inputs_read[0].rows, inputs_read[1].rows, no_such.field]", "result": "keeps the first two; the first is not written (HO2)"},
      {"command": "python -B tests/scenario_walk.py --witness-for scripts/stage_guard.py ...", "result": "3 scenarios + 27 keep files listed (H5)"}
    ]
  }
}
```
