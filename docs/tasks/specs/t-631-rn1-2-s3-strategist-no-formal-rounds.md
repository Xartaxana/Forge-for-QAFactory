# t-631 — RN1-2: the S3 strategist cannot hand in an unfilled plan and makes no formal rework rounds (DRAFT, designer)

Status: DRAFT for the critic on plan. Node RN1-2 of `plans/piles/release-next/batch-1-release-0-10-9.md`. Owner's word 02.11.2026.
Finding: `plans/piles/release-next/findings/20261102-strateg-sdaet-nezapolnennoe-i-krugi-dorabotki.md` ("What to change", pp. 1-6; pp. 7-8 see F-7).
Fact base: recon t-1667 `docs/tasks/specs/reports/t-1667-s3-strategist-returns-recon.md` (cited as qA1..qX2), re-read and CORRECTED in §7 where the carrier
says otherwise. P = `ai-packages/qa-factory`, R = the worktree root.

Three load-bearing corrections to the brief (read on the carriers, §7):
- **C1. The S3 strategist has no shell** (`agents/qa-test-strategist.md:4` `tools: Read, Grep, Glob, Write, Edit`). A self-check COMMAND
  (finding p.6) is a door it cannot use (FR-2). The one self-check it has is the SubagentStop exit gate, which already aggregates every
  detector of the stage AND the handover form in one block (`exit_gate.py:1742-1777`). p.6 is redesigned on that (F-6).
- **C2. The S4-exit writer of new questions is not in `story_run.py`.** `critic_rollcall.py:756` calls `question_register.raise_for_case`
  -> `_name_in_plan_row` -> `planning_contract.append_question_ref`. The register's ONE row-shaper is `question_register._question_row`
  (`:1263`, already shared with the S3 claim projector) and the ONE file writer is `_write_readiness` (`:1286`) under `answers_lock`.
  Recon qB5 ("the register writes only answers") is wrong for the file, right for the role: no door the STRATEGIST can use.
- **C3. "Letters match" is not "meanings match".** Every question raised at S4 is a before/now question with the fixed pair
  (`contract.claim_question` -> `claim_readings`: reading 1 = the behaviour now is intended, reading 2 = a regression). An S2 question such as
  Q4 also has letters a/b, with unrelated meanings. Copying `if_answered[Qm]["a"]` to `if_answered[Qn]["a"]` by letter would apply, on the
  person's answer, a patch the strategist wrote for another reading - code deciding meaning (FR-47, FR-58, P20). p.5 is redesigned (F-5).

A fourth fact the brief did not carry: **the revision mark is not passive.** `planning_contract.py:180-181`: a row carrying
`coverage-observation-v1` is checked by `_validate_coverage_delta` (a `coverage_delta` becomes mandatory). Stamping the mark therefore
switches stricter checks on; item 1 is built so those checks still meet the role in its own context.

---

## §1 Goal, rules and invariants touched

**Goal.** Every refusal the S3 plan can meet before gate A for a reason that is a value code knows, or a form slot, is either filled by code
or refused at the S3 EXIT (SubagentStop, the strategist's own context) - never after `accept` as a new dispatch. The strategist gets a door
for a question the register does not hold. An S3 rework form arrives with its rows' ids. A question raised at S4 is re-pointed on the plan
row by code only where its meaning is provably the same; otherwise the rework stays the strategist's.

**Not changed:** gate A (`controller._coverage_contract_revisions`, `gate-inputs`) and the S4 rehearsal
(`gate_preflight.check_question_branches`) - it stays the backstop for every kind.

| Rule | How this node touches it | Change check (in the DoD, §4) |
|---|---|---|
| FR-1 | every new/changed refusal says what is wrong, the expected value, the field that produces it | K-1.3, K-2.3, K-3.4 assert the expected value / field name in the text |
| FR-2 | the strategist's doors are FIELDS it can write (no command); the person's word stays the conductor's (`waiver.py`) | K-6.2: no S3 REJECT line names a `.py` command except the existing waiver line |
| FR-4 / builder rule 8 | every new refusal passes on a person's word (the existing S3 waiver line of `_detector_body`) | K-2.5 |
| FR-7 | an `unresolved_ref` printed twice for one ref (R-2) becomes one line; a raise is idempotent | K-2.4, K-3.2 |
| FR-38 / AR-10 | the requirement (the `new_questions` form, the branch kinds, the delta a stamped row needs) reaches the role BEFORE the work in its agent text | K-6.1 presence test |
| FR-45 | no validator writes: the exit detector evaluates a VIRTUAL stamp; the stamp and the raise are written by a projection step (`project_plan`) | K-1.2: a detector run leaves `test-plan.json` byte-identical (sha before/after) |
| FR-47 / AR-7 | code fills the constant, copies the role's declared question into the register, re-points only on a declared replacement and by meaning; which question and which reading stay the roles' | K-5.2, K-5.3 |
| FR-59 / AR-28 | an unreadable register or plan at the exit is `UNREADABLE`, at projection a refusal to the conductor; never a pass, never `new:` refs left for S4 | K-2.6, K-3.5 |
| AR-13 | one reader per fact: revision value only via `coverage_contract.COVERAGE_CONTRACT_REVISION`; letters via `contract.reading_letters`; meanings via `contract.claim_reading_index` | K-1.1 imports the constant, no literal |
| AR-14 | one writer: plan writes by code go through `planning_contract` (`_write_plan_rows` / `atomic_json`); register rows through `question_register._question_row` + `_write_readiness` | K-3.2; mutation M-6 |
| AR-15 / AR-19 | the plan projection sits at the claim projection's seam (`story_run.Driver.s3_project`); S3 `new_questions` mirrors S4 `raise_questions` | K-1.4b; M-11 |
| AR-22 | `scope[].coverage_contract_revision` of the S3 form has no reader -> removed with its producer / null-outcome rows (F-2) | K-1.5 |
| AR-23 | `new_questions` absent or `[]` = no new question (declared outcome) | edge E-3 |
| AR-25 | each exit refusal for a branch kind names its way out (a field, or a person's word) | K-2.3 |

---

## §2 Change list (one item per finding point; decisions chosen, forks in §5)

### Item 1 — the revision mark is set by code (finding p.1)

1.1 `P/scripts/planning_contract.py`, NEW pure `stamp_revision(rows, plan_contract_mode) -> list`: a deep copy of `rows` in which every dict
row WITHOUT a value in `coverage_contract_revision` (key absent, `None` or `""`) gets `coverage_contract.COVERAGE_CONTRACT_REVISION`.
Rule by mode (mirrors `controller._coverage_contract_revisions`, whose invariant is "a mixed set is never silently turned green"):
- mode `legacy` AND no row carries a value -> rows returned unchanged (a legacy plan stays legacy, builder rule 9);
- otherwise (mode not `legacy`, or at least one row carries a value) -> every unmarked row is stamped.
A row with a value other than the constant is never changed. A non-list `rows` is returned as it is (the plan contract names it).
Invariant protected: stamping only ADDS the mark; the stricter checks the mark switches on (`_validate_coverage_delta`, `validate_obligations`)
run on the stamped rows BEFORE the role leaves (1.2), so a missing `coverage_delta` is refused in the role's context and never hidden.

1.2 `planning_contract.coverage_revision_errors(rows, allow_legacy)`: the "missing coverage_contract_revision" sentence is removed (code
supplies the value); ADD a refusal for a present value that is not the constant:
`"{rid}: coverage_contract_revision is {value!r}; this factory plans against {COVERAGE_CONTRACT_REVISION!r} and writes the mark itself - remove the field from the row (a row planned against another revision is re-planned, not relabelled)"`.
`_detector_body` computes `stamped = stamp_revision(rows, mode)` once and passes `stamped` (not `rows`) to `gate_plan_errors`, to
`s3_branch_refusals` (item 2) and to `grounding_table.role_exit_lines` / `contradiction_errors` / `register_fence` unchanged in meaning
(they do not read the mark). The detector writes nothing (FR-45).

1.3 Writer: NEW `planning_contract.project_plan(task_root) -> types.SimpleNamespace(wrote: bool, problems: list, notes: list)` (it also does
item 3.3). Reads the plan through `_plan_state`; no plan -> `wrote=False, problems=[]`; plan unreadable -> one problem; gate A approved
(`_gate_a_state`) -> nothing written, one problem line (the same ban `append_question_ref` keeps). Writes `stamp_revision(...)` (+ item 3.3)
with ONE `_write_plan_rows` call, only when a row changed. Never raises: any exception -> a problem line naming its type.

1.4 `P/scripts/story_run.py`, method `s3_project` ONLY (the seam of the claim projection, AR-15): after `CP.project(self.task_root)` returned
without problems, call `PC.project_plan(self.task_root)`; `problems` -> `Refusal("S3 plan projection (planning_contract.project_plan): " + lines,
dispatch=dispatch, retry=None)` WITHOUT `REPAIR_MARKER` (not the role's to fix: FR-59, the conductor, P22). Window 1 (labelling) writes no
plan, so `project_plan` returns `wrote=False, problems=[]` there.

1.5 Texts and contract (F-2 recommendation (a)): remove the role's duty from `agents/qa-test-strategist.md:153-155`
("`coverage_contract_revision` on every row included" is deleted; step 1's "On `coverage-observation-v1`, fill ..." becomes "Every row is
planned on `coverage-observation-v1` (code writes the mark): fill ..."), from `skills/qa-story/phases/s3.md:153-156` ("so a row without
`coverage_contract_revision` ..." -> "the revision mark is written by code when S3 closes; a row carrying another revision is refused"),
and the form line `handoffs/s3-strategist-to-designer.yaml:69`; drop the row `scope[].coverage_contract_revision` from
`references/field-producers.json:21-25` (the note's count "28 of them need a tool" -> 27), the row
`s3-strategist-to-designer:scope[].coverage_contract_revision` from `references/null-outcomes.json:158`, and set `PINS["tool_fields"]`
28 -> 27 in `scripts/tests/test_null_outcomes.py:37` (a shrink, allowed by AR-20; named in the verdict).

Tests (new file `P/scripts/tests/test_s3_strategist_rounds.py`, harness style):
K-1.1 plan without the field, mode not legacy -> after `project_plan` every row carries the constant (compared with the imported constant).
K-1.2 the detector on the unstamped plan whose rows carry a valid `coverage_delta`: `OK:` line, and the plan's sha256 is the same before and after the detector.
K-1.3 a row with `"coverage-observation-v0"` -> REJECT line contains `'coverage-observation-v1'` and `remove the field`.
K-1.4 legacy mode, no row marked -> `project_plan` returns `wrote False`, detector OK. Legacy mode, one row marked and one not, the unmarked
one without `coverage_delta` -> the detector names `coverage_delta required` for that row (the invariant of 1.1).
K-1.4b `s3_project` calls `project_plan` after `CP.project` (recorder fixture of `test_story_run_s3_windows.py`).
K-1.5 the S3 form template holds no `coverage_contract_revision`; `test_null_outcomes.py`, `test_field_producers.py` green.

### Item 2 — question branches are checked in the S3 EXIT gate (finding p.2, and the dedupe of p.8)

2.1 `planning_contract.py`: NEW module constant `S3_EXIT_KINDS = ("missing_branch", "unresolved_ref", "missing_refs", "bad_branch",
"invalid_variant", "stale_reason", "settled_question", "dependent_pair", "no_row_for_question")` - every STRATEGIST-owned kind of
`BRANCH_KINDS`. The designer-owned kinds (`case_unreadable`, `missing_reading_text`, `row_owes_case`, designer `bad_branch`) cannot arise
without cases. `no_row_for_question` moves from WARN to refusal (F-2b).

2.2 `missing_branch_findings` is REPLACED by NEW `s3_branch_refusals(task_root, rows) -> tuple(findings: list, why_unread: str)` (findings
whose `kind` is in `S3_EXIT_KINDS`, from `variant_errors` over `rows` with `cases=()`). Differences from the old reader - each one an invariant:
- a register with ZERO questions while a row carries `question_refs` / `if_answered`: `variant_errors` is still run, with `questions=[]`, so
  every ref is `unresolved_ref` (today `if not questions: return []` at `:3242-3243` lets `Q101` pass against an empty register).
  Invariant: an id the register does not hold never passes the S3 exit.
- the register file absent or unreadable (`question_register.load(...)` returns `problems`, or `register_present` false) while a row
  carries refs -> `why_unread` = that reason; `_detector_body` prints `UNREADABLE: ...` and exits 3 only when no REJECT stands (the existing
  rule for the fence, `:3382-3401`). Never `OK:`.
- an exception inside -> `why_unread` = `"question branches could not be checked (<type>: <text>)"`, never `[]` (FR-59).
- `has_branch_fields` false (a plan dated before ORACLE_CUTOFF with no branch field) -> `([], "")`: builder rule 9 unchanged.
- the questions passed to `variant_errors` include the virtual questions of item 3.2, so a declared `new:<n>` is not `unresolved_ref`.

2.3 `_detector_body`: the old `missing` block and the `no_row_for_question` WARN loop (`:3391-3392`) are replaced by ONE REJECT block:
header `REJECT — {n} question-branch problem(s) of the plan rows; at gate A an answer would not move the plan as written. Repair them now, while S3 still holds the context:`,
then one `- ` line per finding (its own message, already in FR-1 form), grouped by kind in `BRANCH_KINDS` order. The tail summary line counts
`{k} question-branch problem(s)` instead of `row(s) without a branch`. The waiver line and its `missing_branch_line` example stay as they are.
The `unresolved_ref` message (`variant_errors.unresolved`) gains the door of item 3: `... the register's ids are {ids}. For a question the
register does not hold, write "new:<n>" in question_refs and an entry in the row's new_questions (question, source_says, readings, severity,
owner_role); code raises it as the next Q-n when S3 closes`.

2.4 Dedupe at the source: the local `add` of `variant_errors` keeps a set of `(kind, where, question, message)` and appends a finding once.
Cause of R-2's doubled lines: `unresolved()` runs for the same ref from the `question_refs` loop (`:1686-1688`) and again from the
`if_answered` loop (`:1810-1815`). The S4 rehearsal reads the same function and gets the same dedupe (one fact, one line); the
`s3-remarks` header count (finding p.8) is then a count of unique findings.

2.5 `P/scripts/stage_done.py`, `s3_branch_line`: filter `item.get("kind") not in planning_contract.S3_EXIT_KINDS` (widening the existing
`missing_branch` filter `:480-483`, for its own reason: a stage that closes anyway closed on a person's recorded word, and a remark asking to
repair what that word passed contradicts the pass, FR-4). It stays the reporter for any kind outside `S3_EXIT_KINDS` and for the "not checked"
lines. `skills/qa-story/phases/s3.md:135` ("Remarks after S3 closes") is reworded: "S3 remarks appear only for a branch finding the S3
exit does not refuse; the S4 rehearsal is the backstop for the rest."

Tests:
K-2.1 plan row `question_refs: ["Q101"]`, register Q1..Q6 -> detector exit 1, REJECT block holds `Q101`; through the exit-gate fixture
pattern of `test_question_branches.py` the stop is blocked (not accepted).
K-2.2 the same with a register file of ZERO questions -> REJECT, not OK.
K-2.3 one fixture row per kind of `S3_EXIT_KINDS` -> each kind's line in the REJECT block, each naming a field.
K-2.4 the `Q101` ref present in both `question_refs` and `if_answered` -> exactly ONE line naming `Q101`.
K-2.5 a recorded S3 waiver quoting the `Q101` line -> the stop passes.
K-2.6 `requirements-readiness.json` unreadable with refs present -> `UNREADABLE:` and exit 3, no `OK:`.
K-2.7 `s3_branch_line` on a plan with only an `unresolved_ref` -> `""`.
`test_s3_remarks.py`: its assertions on the package text move to direct calls of `stage_done._s3_remark_package` (the writer is unchanged;
only its reachability shrinks); builder lists every assertion moved.

### Item 3 — the door `new:` for a question the register does not hold (finding p.3)

3.1 Plan row fields (F-3 recommendation (a)): `question_refs` may hold `"new:<n>"` (`n` an integer 1..99, unique within the ROW); the row
carries `new_questions: [{"key": "new:<n>", "question": str, "source_says": [{"quote": str, "where": str}], "readings": [{"reading": str}, ...]
(two or more), "severity": str, "owner_role": str}]`; `if_answered["new:<n>"]` is written like any branch, keyed by the letters a, b, ... of
its readings, plus `not_needed`.

3.2 NEW `planning_contract.plan_questions_view(rows) -> tuple(scoped_rows: list, virtual: list, problems: list)`. A `new:<n>` key is local to
its row, while `variant_errors` matches ids globally; so the view works on a DEEP COPY: in each row, every `new:<n>` in `question_refs` and
in the keys of `if_answered` is renamed `new:<n>@<row id>`, and each valid `new_questions` entry becomes a virtual question
`{"id": "new:<n>@<row id>", "status": "open", "readings": <the entry's readings>}`. `s3_branch_refusals` calls `variant_errors(scoped_rows,
register_questions + virtual, ...)` and, before returning, replaces `new:<n>@<row id>` by `new:<n>` in each finding's `question` and
`message`. Consequences: a `new:<n>` ref with no entry in ITS OWN row's `new_questions` is `unresolved_ref`; a branch on it is checked for
every letter of its readings and `not_needed` like any open question.
`problems` (REJECT lines in the branch block): an entry that is not an object, a `key` not of the form `new:<1..99>`, a duplicate key in a
row, an entry no `question_refs` of its row names, fewer than two readings, a missing `question`/`source_says`/`severity`/`owner_role`, and
every sentence of `contract.question_errors(entry with id "Q0")` - each as `"{rid}: new_questions[{i}] ({key}): {problem}. Expected: question, source_says, readings (two or more), severity, owner_role"`.

3.3 Raising, inside `project_plan` (1.3), under `question_register.answers_lock(task_root)`: read the register's `open_questions`; for each
row and entry in plan order call `QR._question_row(register_rows, question, raised_for={"row": rid, "origin": "S3-plan", "key": key},
taken=<highest number handed out in this move>)`; append the new rows; ONE `QR._write_readiness(path, data)` for the batch. THEN, in the plan
rows: replace the ref `new:<n>` by the issued `Q<m>` in `question_refs` (same position), rename the key `if_answered["new:<n>"]` ->
`if_answered["Q<m>"]`, remove the entry from `new_questions` (remove the key when the list is empty). Order of writes: the register FIRST,
the plan second (a crash between them leaves a question no row names - a rerun converges through `raised_for`; never a row naming a missing
question - the claim projector's own rule). Idempotent: an equal `raised_for` makes `_question_row` return `earlier`, whose id is used;
nothing is raised twice (FR-7). A plan whose entries have `problems` (3.2) is not projected (the exit gate refused it; a problem line says so).

3.4 Text: `agents/qa-test-strategist.md` step 2 gains ONE sentence (size cap 9000 B, builder rule 5): "A question the register does not hold:
`new:<n>` in `question_refs` and its entry in `new_questions` (question, source_says, readings, severity, owner_role); code raises it as the
next Q-n when S3 closes - never invent an id."

Tests:
K-3.1 row `question_refs: ["new:1"]`, a valid entry, `if_answered["new:1"]` with a, b, not_needed -> detector OK.
K-3.2 `project_plan` -> the register gains `Q7` (it held Q1..Q6) with `raised_for {"row", "origin": "S3-plan", "key"}`; the plan row carries
`Q7` in `question_refs` and `if_answered["Q7"]`, no `new_questions`; a second call writes nothing (`wrote False`, register unchanged).
K-3.3 two rows, each with its own `new:1` -> Q7 and Q8; no `unresolved_ref` at the exit before projection.
K-3.4 an entry with one reading -> REJECT naming `readings (two or more)`; `new:100` -> REJECT naming `1..99`; `new:99` -> accepted.
K-3.5 the readiness file unreadable at `project_plan` -> `problems` non-empty, the plan's sha unchanged; `s3_project` raises a Refusal whose
text has no `REPAIR_MARKER`.
K-3.6 gate A approved -> nothing written, one problem line.

### Item 4 — the S3 rework form arrives with the rows' ids (finding p.4)

4.1 `P/scripts/handoff_init.py`: NEW option `--rows ID[,ID...]` and NEW function `prefill_rows(text, contract, ids) -> tuple(text, note)`:
ids split on `,`, stripped, empties dropped, de-duplicated with order kept; for index i the pair `("scope[i].id", ids[i], 0, "")` goes
through `handoff_check.apply_values(doc, contract, pairs)` (the ONE writer of a form's words; it opens rows by index); the written paths are
recorded with `handoff_check.record_derived` (source: "the plan rows this rework dispatch was sent for (the controller's dispatch record)");
`state`, `reason` and every other key of the row stay placeholders. Applied AFTER `carry_from_parent` in `main` (carry matches rows by
identity through `_same_row`; prefilled ids must not hide the parent's rows from it - K-4.4 holds it). A pair `apply_values` refuses leaves
that row blank and the note names it (error direction: under-fill, never a guessed id).

4.2 `P/scripts/story_step.py`, function `_handoff_form` ONLY: when the dispatch record has `rework_of` AND `stage_id == "S3"` AND
`record["plan_rows"]` is a non-empty list, append `--rows <comma-joined ids>` to the argv (F-4: other stages queued).

4.3 `handoff.REQUIRED_LISTS` and `handoff_check`'s "no rows" refusal stay: a prefilled row with a placeholder `state` is still refused at the
exit, in the role's context, naming the field instead of "no rows".

Tests (new `P/scripts/tests/test_handoff_rows_prefill.py`):
K-4.1 `handoff_init --rows TS-2,TS-5` on the S3 contract -> `scope[0].id: TS-2`, `scope[1].id: TS-5`, both listed under `derived:`.
K-4.2 option absent, and `--rows ""` -> the form is byte-identical to the one written without the option.
K-4.3 `--rows TS-2,TS-2` -> one row.
K-4.4 with `--carry-from` a parent form whose rows TS-2 and TS-5 hold answers -> the listed carried keys of those rows are kept.
K-4.5 an id with `:` and one starting with `<` -> written quoted, read back equal through `handoff.parse`.
K-4.6 `_handoff_form` for an S3 record `{rework_of, plan_rows: ["TS-2"]}` passes `--rows TS-2`; for an S4 record and for an S3 primary
dispatch it passes none (monkeypatched `_run`).

### Item 5 — re-pointing a question raised at S4 (finding p.5; redesigned, C3, F-5)

5.1 The designer's declaration: the existing `raise_questions` entry of a case may carry `"replaces": "Q<m>"` - the question of the plan row
this Then rested on and that the new question replaces. `question_register.raise_for_case` reads it from the entry it already holds
(`by_then`) and passes it to `_name_in_plan_row`; nothing else is read from the designer. A `replaces` that is not a register id of the
row is ignored with a note (the fallback of 5.2).

5.2 NEW `planning_contract.repoint_question_ref(task_root, row_id, old_qid, new_qid, case) -> tuple(written: bool, line: str)`, called by
`_name_in_plan_row` INSTEAD of `append_question_ref` for a raise that declared `replaces`. It writes (one `atomic_json`; the same bans as
`append_question_ref`: no plan, unreadable plan, gate A approved or unreadable, no such row, `question_refs` not a list) ONLY when ALL hold:
(a) `old_qid` is in the row's `question_refs` and is OPEN in the register (`question_register.settled` false);
(b) both questions are before/now questions whose meaning positions are known: `contract.claim_reading_index(q, "now")` and
    `contract.claim_reading_index(q, "before")` are both not None, for the old and for the new question;
(c) the row's `reason` does not name `old_qid` as a whole token (`_id_token`);
(d) `if_answered[old_qid]` exists and is an object (there is a branch to move).
Then: in `question_refs` `old_qid` is replaced by `new_qid` at the same position; `if_answered[new_qid]` gets, for each meaning in
(now, before), the patch the old branch holds under the OLD question's letter of that meaning, written under the NEW question's letter of that
meaning; the `*` and `not_needed` keys are copied unchanged; `if_answered[old_qid]` is removed.
Any condition false: it calls `append_question_ref` (today's behaviour) and returns the line
`"{new_qid} raised for {case} replaces {old_qid} on {row_id}, but {why}; the strategist's rework sets the branch"` (why = the failed condition
in words) - the S4 rehearsal then names `missing_branch` and the existing route (`controller.ANSWER_REWORK_OWNERS` -> rework S3 `--rows`) stands.
Invariant protected: a person's answer never applies a patch written for another reading; code moves a branch only between readings of the
same MEANING, read through the one reader (`claim_reading_index`), never by letter.

5.3 `agents/qa-case-designer.md`: one sentence beside its `raise_questions` instruction: "When the Then rested on a plan-row question that
your new question replaces, add `"replaces": "Q<m>"` to its entry."

Tests (extend `P/scripts/tests/test_raise_reaches_plan_row.py`):
K-5.1 old and new are before/now questions; the old one's readings carry `claim` with `before` at position a and `now` at b, the new one is
the code's pair (now = a) -> after the raise, `if_answered[new]["a"]` equals the old branch's `"b"` patch and `if_answered[new]["b"]` the old `"a"`.
K-5.2 the old question is an S2 a/b question without meanings -> no re-point; the ref is appended as today; the returned line names `replaces`.
K-5.3 no `replaces` -> byte-identical behaviour to today (`append_question_ref`).
K-5.4 the row's `reason` names the old id -> fallback with its line.
K-5.5 gate A approved -> nothing written, the line says so.

### Item 6 — one self-check before hand-in (finding p.6; redesigned, C1, F-6)

6.1 The ONE self-check is the S3 exit gate the role meets on its first stop. After items 1-3 it carries every check gate A and the S4
rehearsal make of the plan rows (`_detector_body`: the plan contract on the stamped rows + every strategist branch kind + the register fence +
the regression section) and the handover form (`exit_gate.form_stop_errors`), in ONE block (`exit_gate.py:1742-1777`). No new command:
the role has no shell (FR-2), and a second road to the same checks would be a second reader (AR-13).

6.2 Texts made one: `agents/qa-test-strategist.md:156-158` -> "When you finish, the exit gate re-runs everything gate A and the case stage
check on your plan rows and your form, and names every finding at once; repair them all in one pass and finish again." `s3.md:137-142` is the
conductor's text, not the role's (recon qE1 read it as a contradiction; it has another reader): it keeps "do not re-run the plan contract by
hand" and gains "the strategist's exit gate is the check; nothing is run for it".

6.3 `validate_artifacts.py` (the write hook) is NOT given the full detector (§6, S-4).

Tests: K-6.1 presence: the agent file holds `names every finding at once` and no longer holds `coverage_contract_revision`.
K-6.2 one fixture reproducing R-1..R-3 (rows without the mark, `Q101`, a rework form with no rows): the S3 detector's REJECT names `Q101`
and nothing about the mark; with `--rows` the form check names `state`, not "no rows"; no REJECT line names a `.py` command except the waiver line.

---

## §3 Edges and invariants

| Edge | Behaviour | Invariant it protects |
|---|---|---|
| E-1 a plan with zero questions (no `question_refs`, `if_answered`, `new_questions` anywhere) | pre-cutoff: no branch finding; post-cutoff: only `missing_branch` for a row whose `reason` names a register id (today's rule); no register question and no ref: no finding | a story with no branch field is never refused for one (builder rule 9) |
| E-2 the register holds ZERO questions, a row names `Q3` | `unresolved_ref` REJECT (2.2) | an id the register does not hold never passes the S3 exit |
| E-3 `new_questions` absent or `[]` | no new question; a `new:<n>` ref without its entry is `unresolved_ref` | AR-23: empty is declared; a dangling `new:` ref never reaches S4 |
| E-4 a `new_questions` entry no `question_refs` of its row names | REJECT (3.2) | nothing is put to the person that no row rests on (FR-9) |
| E-5 a new question whose letters match the questions of two rows (raised for TS-24, Qm also on TS-25) | only the row of the case that declared `replaces` is touched; letters alone never trigger a re-point; the map is by meaning | an answer never applies a patch written for another reading |
| E-6 meaning positions unknown (`claim_reading_index` None) | fallback append + line; rework S3 by the existing route | an unknown never becomes a write (FR-59); code never guesses meaning |
| E-7 S3 rework, `plan_rows` empty or absent | no `--rows`; form as today; "no rows" refused in context | REQUIRED_LISTS unchanged: a handover with no rows is still refused |
| E-8 `plan_rows` names an id the plan no longer holds | the row is prefilled anyway (the controller refused unknown rows when it registered the rework, `controller.py:3280-3281`); the exit fence names a stale one | the form never invents an id; ids come only from the controller record |
| E-9 in-flight story past S3, plan from an older release | `project_plan` runs only at S3 completion and never touches it; gate A as today (door `--operation coverage_migration`, `design/controller-blocks.md:124`) | builder rule 9; nothing silently green |
| E-10 in-flight story mid-S3, rows written by the old role WITH the mark | the stamp is a no-op | a row that has a value is never changed |
| E-11 legacy mode, wholly unmarked | no stamp, no refusal | a legacy plan stays legacy (the controller's rule) |
| E-12 legacy mode, mixed | unmarked rows stamped virtually at the exit, really at completion; their `coverage_delta` is demanded at the exit | a mixed set is never turned green: the proof is demanded before the mark is written |
| E-13 a row carries another revision | REJECT with the expected value and "remove the field" | a row planned against another revision is re-planned, not relabelled |
| E-14 the self-check (exit gate) fails | the role reads `HANDOFF BLOCKED by the exit gate - N finding(s) ... Fix every one and finish again (block k/MAX)` with every line in FR-1 form (what, expected, the field); doors: its row fields; a person's word through the conductor (the waiver line) | FR-1, FR-2, FR-4 |
| E-15 the exit passes, `project_plan` fails at completion (lock wait over `LOCK_WAIT_SECONDS`, unreadable register, disk) | `s3_project` raises a Refusal to the conductor; S3 not closed, S4 not dispatched; the plan keeps its `new:` refs | an unknown is never a pass; S4 never reads a `new:` ref |
| E-16 crash between the register write and the plan write | rerun: `_question_row` finds the `raised_for` -> the same id; the plan converges | one question per (row, key) (FR-7) |
| E-17 conflicting requirements: item 2 refuses `no_row_for_question` vs GW1-41's choice of a WARN ("a negation gives a false finding") | refused, with the person's word as its door (its message already says so) - F-2b | a finding that today becomes a remarks round is said in the role's context |
| E-18 conflicting requirements: item 1 removes the role's duty to write the mark vs FR-38 (a stamped row still needs `coverage_delta`) | the agent's step 1 says every row is planned on `coverage-observation-v1` and names the delta (1.5) | FR-38: the requirement the stamp switches on is told before the work |
| E-19 two different findings with the same (kind, where, question, message) | identical text is one fact: kept once | the key includes the message: nothing distinct is lost |

Limits introduced: `new:<n>` with n in 1..99 (AT: `new:99` accepted; BEYOND: `new:100` refused, K-3.4); readings of a new question >= 2
(AT: 2 accepted; BEYOND below: 1 refused, K-3.4).

Reused functions in a more consequential role:
- `handoff_check.apply_values` (a role's words -> code's prefill). Error direction: may only under-fill (a refused pair leaves the row blank,
  the note names it). Adversarial inputs that must stay safe: an id with `:` or `#`, an id starting with `<` (a placeholder look-alike: it must be
  written quoted and read back as a value, K-4.5), an empty id (dropped), a duplicate id (one row), 200 ids (no cap; forms hold that many rows).
- `contract.claim_reading_index` (the gate card's reader -> now the decision to WRITE a branch). Error direction: may only return None
  (fallback, the strategist's rework). Adversarial inputs that must give None and no re-point: `claim` twice on one reading, three readings,
  readings without `claim` whose texts are not the code's pair, a reading with an unknown `claim` word.

---

## §4 Builder material

given: this spec; `R/plans/piles/release-next/findings/20261102-strateg-sdaet-nezapolnennoe-i-krugi-dorabotki.md`;
`R/docs/tasks/specs/reports/t-1667-s3-strategist-returns-recon.md`; `P/design/factory-rules.md` whole; `R/plans/builder-rules.md`;
`P/design/architecture.md` (AR-7, AR-10, AR-13, AR-14, AR-15, AR-22, AR-28); the files in owns and the tests named in the DoD.

owns:
C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\planning_contract.py (functions: stamp_revision NEW, coverage_revision_errors, _detector_body, s3_branch_refusals NEW replacing missing_branch_findings, plan_questions_view NEW, project_plan NEW, repoint_question_ref NEW, the local `add` and `unresolved` of variant_errors only, constant S3_EXIT_KINDS NEW)
C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\stage_done.py (s3_branch_line only)
C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\story_run.py (s3_project only)
C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\handoff_init.py (prefill_rows NEW, main)
C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\story_step.py (_handoff_form only)
C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\question_register.py (raise_for_case, _name_in_plan_row only)
C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\agents\qa-test-strategist.md
C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\agents\qa-case-designer.md (one sentence, item 5.3)
C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\skills\qa-story\phases\s3.md
C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\handoffs\s3-strategist-to-designer.yaml
C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\references\field-producers.json
C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\references\null-outcomes.json
C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\tests\test_s3_strategist_rounds.py (new)
C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\tests\test_handoff_rows_prefill.py (new)
C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\tests\test_raise_reaches_plan_row.py
C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\tests\test_question_branches.py
C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\tests\test_s3_remarks.py
C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\tests\test_case_gates.py (only its calls of missing_branch_findings)
C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\tests\test_null_outcomes.py (PINS tool_fields only)
C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\scripts\tests\test_story_run_s3_windows.py (the s3_project order key only)
C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory\changelog.d\release-next-1-rn1-2.md (new)

non-goals: TQ1-21 (`extend` target existence) and RN1-6 (request x failure rows) own every OTHER function of `planning_contract.py`,
`validate_plan` included (D-0048: disjoint functions); `story_run.py` beyond `s3_project` (`merge_answer_rework`,
`question_branch_findings` untouched); `controller.py` (gate A unchanged); `gate_preflight.py` (the S4 rehearsal unchanged); `contract.py`
(integrator-only, builder rule 1; nothing needed: `question_errors`, `claim_reading_index`, `reading_letters` are called, not changed);
`critic_rollcall.py` (its call of `raise_for_case` is unchanged); `validate_artifacts.py`; `handoff_check.py` (called, not changed);
prefill for stages other than S3 (F-4); finding p.7 (F-7); the neighbour sweep S2-S7 (F-8).

handoff: C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\docs\tasks\handoffs\t-NNN-rn1-2.md

edges: §3 E-1..E-19, the limits line and the two reused functions' adversarial inputs.

DoD — run from P (`C:\Projects\yml-text-factory\.claude\worktrees\release-10-9-706cee\ai-packages\qa-factory`), builder rules 7b and 7c;
the witness is the verbatim tail of each run:
`python -B scripts/tests/test_s3_strategist_rounds.py`
`python -B scripts/tests/test_handoff_rows_prefill.py`
`python -B scripts/tests/test_raise_reaches_plan_row.py`
`python -B scripts/tests/test_question_branches.py`
`python -B scripts/tests/test_s3_remarks.py`
`python -B scripts/tests/test_case_gates.py`
`python -B scripts/tests/test_null_outcomes.py`
`python -B scripts/tests/test_field_producers.py`
`python -B scripts/tests/test_repair_form_carry.py`
`python -B scripts/tests/test_question_register.py`
`python -B scripts/tests/test_story_run_s3_windows.py`
`python -B scripts/tests/test_story_run_words.py`
`python -B scripts/tests/test_driver_layers.py`
`python -B scripts/selftest.py --limits --lang` (two agent files change: the 9000 B cap and English)
Every key K-1.1 .. K-6.2 is a named `check` in the new or extended files.
Batch canon (integrator, not builder): `test_story_step*.py`, `test_gate_preflight*.py`, `test_audit_rules.py`, docker, ratchets.

Mutations (builder names the killing test and the one-line mutant, does not run them; builder rule 7b):
M-1 `stamp_revision` stamps a legacy wholly-unmarked plan -> K-1.4 (`test_s3_strategist_rounds.py`).
M-2 `_detector_body` validates `rows` instead of the stamped rows -> K-1.4 second half (no `coverage_delta required`).
M-3 `s3_branch_refusals` returns `[]` when the register has no question -> K-2.2.
M-4 `variant_errors.add` without the dedupe set -> K-2.4.
M-5 `stage_done.s3_branch_line` filter back to `!= "missing_branch"` -> K-2.7.
M-6 `project_plan` builds the register row itself (no `QR._question_row`, no `raised_for`) -> K-3.2 (the second call raises again).
M-7 `project_plan` writes the plan before the register -> K-3.5 (plan sha changes while the register write fails).
M-8 `prefill_rows` runs before `carry_from_parent` -> K-4.4 (`test_handoff_rows_prefill.py`).
M-9 `repoint_question_ref` maps by letter -> K-5.1 (`test_raise_reaches_plan_row.py`).
M-10 `repoint_question_ref` skips condition (b) -> K-5.2.
M-11 `s3_project` calls `project_plan` before `CP.project` -> K-1.4b (`test_story_run_s3_windows.py`).

Changelog fragment `P/changelog.d/release-next-1-rn1-2.md` (English, CHANGELOG voice): the revision mark is written by code when S3 closes;
question-branch findings are refused at the S3 exit, in the strategist's context; the `new:<n>` door for a question the register lacks;
S3 rework forms carry their rows; a question raised at S4 with `replaces` re-points its plan row by meaning; the S3 form drops
`coverage_contract_revision`.

Commit line: `architecture: AR-7, AR-10, AR-13, AR-14, AR-15, AR-22, AR-28 -- <how kept, one clause each from §1>`.

---

## §5 Forks (Lead decides; recommendation given)

- **F-1 (p.1, where the mark is written).** (a) the write hook stamps the plan the role just saved (the finding's wording): FR-45 (a validator
  writes nothing), and the role's next `Edit` of a file changed under it is refused ("modified since read") - AR-12 friction; (b) a virtual
  stamp at the exit + the real stamp at S3 completion in `s3_project`, the claim projection's seam. **Recommend (b).** Cost: a road with no
  driver gets the stamp only if it also calls `project_plan`; today `claim_projector` is driver-only as well (`audit_factory.py:166`), so the
  twins stay twins, and the gate A refusal stays the net there.
- **F-2 (p.1, the form field).** (a) delete `scope[].coverage_contract_revision` from the S3 form (no reader, AR-22) with its field-producers
  and null-outcomes rows and the pin 28 -> 27; (b) keep it and add a `handoff_check.DERIVERS` entry (touches `handoff_check.py`).
  **Recommend (a).**
- **F-2b (p.2).** `no_row_for_question`: (a) refuse at the exit (today it already makes a remarks rework round); (b) keep the WARN and drop it
  from the remarks (no round, but the answer may change nothing in the plan). **Recommend (a)**; the person's word stays its door.
- **F-3 (p.3, the spelling of the door).** (a) `question_refs: ["new:<n>"]` + `new_questions[]` (a row may rest on several questions;
  `if_answered` needs a key; mirrors S4's `raise` / `raise_questions`, AR-19); (b) the finding's literal `question: new` + a text field (one
  per row, no branch key). **Recommend (a).**
- **F-4 (p.4, which stages).** (a) S3 only now; S4+ queued (their `scope` ids are case or instance ids while a rework record may carry plan
  rows, `controller.py:3404-3407`); (b) every stage, from `plan_rows` else `scope`. **Recommend (a)**, with a queue line for `release-next`:
  "prefill of rework forms S4-S7 by the id kind of each contract's scope".
- **F-5 (p.5, re-pointing).** (a) the brief: letters match -> copy by letter - **advised against**: C3, it applies a patch to the wrong reading;
  (b) the designer declares `replaces`; code maps by MEANING, only between two before/now questions; otherwise today's route; (c) (b) plus a
  designer-declared letter map for an old question without meanings (the designer then decides the meaning of the strategist's question);
  (d) take p.5 out of RN1-2 into its own node. **Recommend (b).** The Lead should accept knowingly: the R-4 case (Q4 is an S2 four-topic
  question, not before/now) would STILL make one S3 rework under (b); only (c) removes it.
- **F-6 (p.6).** (a) the exit gate is the one self-check (no command; the role has no shell); (b) give the strategist Bash for
  `planning_contract.py` (P14 / FR-56: a shell for one check widens the role). **Recommend (a).**
- **F-7 (finding pp. 7-8, added after the brief's pp. 1-6).** p.8 (dedupe) is in item 2.4. p.7 (one question = one topic, split by code) needs a
  model of a question's topics - FR-12 risk (a detector reading wording). **Recommend:** p.7 to its own node with a designer; not RN1-2.
- **F-8 (the finding's "Neighbours").** The S2-S7 sweep "which exit refusals are code's values, which are checks after acceptance" is
  recon-sized. Neighbours seen while reading: `handoff.REQUIRED_LISTS` on every rework form (the F-4 queue line); S4 event 34 (letters on a
  before/now question) is already refused at write time by `_claim_key_errors`. **Recommend:** one scout dispatch after acceptance; its rows go
  to `release-next` batch 2.

## §6 Small choices closed by the designer

- S-1 Dedupe at the source (`variant_errors.add`), not in the package writer: every reader (exit, remarks, S4 rehearsal) gets one line.
- S-2 `new:<n>` bounded to 1..99 per row (a row resting on 99 new questions is a broken row; tested AT and BEYOND).
- S-3 `raised_for = {"row", "origin": "S3-plan", "key"}`: a key space kept apart from the claim one (`{claim, origin}`) and the grounding one
  (`{requirement | row, origin}`) by `origin`.
- S-4 `validate_artifacts.py` does not get the full S3 detector on write (a cost on every Write; the exit gate is the single self-check).
- S-5 `missing_branch_findings` is removed, not aliased (t-305 F2: an alias lets a test patch the wrong function); its callers
  (`_detector_body`, `test_case_gates.py`) move to `s3_branch_refusals`. The builder greps `missing_branch_findings` package-wide (positive
  control: its own def line before the change) and lists every caller in the report.
- S-6 The prefilled ids are recorded under `derived:` (the carry's convention), so `handoff_check` and the critic see who wrote them.
- S-7 The per-row scope of `new:<n>` is done by renaming on a deep copy (`new:<n>@<row id>`), so `variant_errors` keeps its signature and
  its other readers (the S4 rehearsal) are untouched.

## §7 Reading trail

Read: the finding (whole); recon t-1667 (whole); the batch row RN1-2 (`batch-1-release-0-10-9.md:60`); `planning_contract.py` 1-224,
1410-2017, 2290-2313, 2761-2836, 3221-3449; `stage_done.py` 435-606, 1050-1084; `question_register.py` 1150-1390 and its function index;
`artifact_packet.py` (whole: a CLI patcher; the role has no shell, so it is not the role's write path); `validate_artifacts.py` 2404-2482 (the
write hook runs `validate_plan` only); `hooks/hooks.json` (whole); `handoff_init.py` (whole); `handoff.py` 440-654; `handoff_check.py`
1370-1394, 2150-2267; `story_step.py` 295-344 and grep `_handoff_form` / `_dispatch_record`; `controller.py` 2770-2794, 3385-3414,
4168-4183 and grep `plan_rows`; `coverage_contract.py` 295-314; `contract.py` 691-803, 1288-1310, 1444-1480; `story_run.py` 3440-3607,
8700-8880; `exit_gate.py` 1730-1779 and grep; `agents/qa-test-strategist.md` (whole); `s3.md` 130-159; `s3-strategist-to-designer.yaml`
(whole); `field-producers.json` 1-40; `null-outcomes.json` 150-164; `test_null_outcomes.py` grep (PINS); `factory-rules.md` FR-1..5,
FR-7..15, FR-38, FR-39, FR-42, FR-45, FR-47; `builder-rules.md` 1-70; `stages.json` grep `detectors` (S3: `planning_contract.py`,
`branch_accounting.py`).
Corrections to the recon and the brief, verified on the carrier: qB5 (a register writer exists - C2); qE1 (`s3.md:137` addresses the
conductor; the agent's `:156-158` tells the role to run nothing - a missing sentence, not a contradiction); the brief's "`story_run.py` (S4
exit: new questions)": the S4 raise is `critic_rollcall.py:756` (Grep `raise_for_case\(` package-wide; positive control: the def at
`question_register.py:1295` appears in the same output); the revision mark switches on `_validate_coverage_delta` (`planning_contract.py:180-181`).
Needed beyond the manifest (read by the designer or left for the builder): `critic_rollcall.py:756` (read through grep), `claim_projector.py`
header and the `s3_project` / `s3_between_windows` seam; NOT read: the body of `gate_preflight.check_question_branches`,
`handoff_check.record_derived` / `open_row` signatures, `test_story_run_s3_windows.py`, `test_repair_form_carry.py`.
