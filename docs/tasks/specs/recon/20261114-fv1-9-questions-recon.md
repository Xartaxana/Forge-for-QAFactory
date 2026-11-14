# FV1-9 recon — repeats of a question and the "cannot be answered as it stands" question (scout t-657, 14.11.2026)

Condensed by the Lead from the scout's digest (tree: worktree `sc-a1a` = origin/main of 14.11; paths relative to
`ai-packages/qa-factory/`). The Lead spot-verified: `grep -ci question_register references/role-commands.json` -> 0;
`question_register.is_open` `:431-443` read; `factory-7.log:20` read ("S2 rework for Q1-Q3 refused: repair-round cap of 2 reached").

## Register: statuses and who can do what
- Statuses (`references/question-vocabulary.json:2-3`, `scripts/question_register.py:84-86`): `open`, `answered`, `not_needed`,
  `with_designer`, `named` (computed only), `deferred_to_report`. `record()` `:862` writes any recorded status; `_merge` `:252` computes
  `open`/`named`. CLI `:1843` exposes only `--answer`, `--not-needed`, `--reopen`, `--defer`. `with_designer` has no CLI flag and no
  production writer found (tests only; the grep was capped at 40 hits — not excluded beyond them).
- `is_open` `:431-443` (the "shown" predicate): False only for `with_designer` and for answered / not_needed / deferred whose record still
  holds (`_holds` `:364-369`); True otherwise, including answered-but-row-changed and anything unreadable (FR-59 direction).
- A ROLE runs no register command: `references/role-commands.json` has no `question_register.py` entry; charters say "you run no script
  for it" (`agents/qa-case-designer.md:78`, `agents/qa-case-critic.md:133`, `agents/qa-bug-reporter.md:68`). A role raises only through a
  form field — the case designer's `raise_questions` in the case file (the driver turns it into a row at the S4 exit,
  `raise_for_case` `:1373-1429`), other roles' `questions[]` in the handoff form (`raise_from_handoff` / `raise_role_question`
  `:1536-1591`).
- A role cannot answer or close a row: `--answer` needs `--where` and `--by` from closed lists (by: person, conductor, driver,
  orchestrator) plus the shown `row_hash` (`:862-921`, `:1708-1711`); there is no structured "source row" field.
- The only row pointer is the S4 `replaces` of a `raise_questions` entry (`:1411-1413`, `:1451-1464`): it repoints a PLAN ROW's question
  ref; the old register row stays open and is still printed. No withdraw / duplicate_of / supersedes found.

## What an S4 role sees of earlier questions
- Answered rows reach every role brief through `brief_pack.decisions()` `:4511` / `question_answer_lines` `:1738-1852` reading
  `QR.answers_for_brief` `:1174-1194`: one line per answered / not_needed / deferred row whose record holds — id, where, the chosen
  reading, the person's words WHOLE. The QUESTION TEXT is not in the line.
- OPEN rows are listed in no brief. The S4 designer's inputs hold neither `requirements-readiness.json` nor `question-answers.jsonl`
  (`brief_pack.py:97-98`, `references/stages.json:158-163`). The S4 critic reaches `work/requirements-readiness.json` only through the
  S2 outputs (`stages.json:75`, and the `acceptance_reads` row of the stage-critics spec).
- `raise_for_case` runs at the S4 exit: the role never sees the register at raise time. `_raise` `:1319-1332` is idempotent only on the
  same (case, Then): same before/now returns the earlier row, different text is refused naming the old id; `raise_role_question`
  `:1558-1564` is idempotent on `raised_from`. Neither compares across keys — a repeat from another case or dispatch gets a new Q<n>.

## The pack shown to a person
- Printed rows = exactly `QR.is_open(q)` over `QR.load`, register order, no cap (`scripts/question_stop.py:384-405`, `:468-522`). Gate
  A's list `gate_brief.still_open` `:4202-4252` drops row_answered, driver_owned and settled rows.
- Row data keys: `question`, `source_says[{quote, where}]`, `readings[{reading, from, if_chosen, claim?}]`, `severity`, `owner_role`,
  `before{value, where}`, `now{value, where}`, `raised_for` ({case, then} at S4; {claim, origin} at S3; {requirement|row, origin} for
  grounding); role rows add `asked_by`, `stage`, `read`, `read_missing`, `recommendation`, `why_person`, `raised_from{dispatch, row}`;
  also `norms_list`, `answer`, `ref`, `requirement`.
- No step relates two rows by data: `source_says.where` / `now.where` is a join key nowhere; `_shown` `:1270-1279` (a comparable
  before/now sentence) is used only by the (case, Then) idempotency check. In the recorded run the repeating pairs Q1/Q10, Q2/Q11, Q3/Q12
  share NO data key (they repeat by meaning only).
- The card (`scripts/gate_brief.py:2734-2820`): `the source says: "<quote[:240]>" — <where[:120]>`, before/now with where, readings with
  `(from <from or ?>)` (`:2786`, `:2794`), and `question_effects` — what each letter changes in the plan / cases (`:2776-2806`).

## Re-asking
- An unanswered shown row is printed again at the next stop with the same card text; after a partial answer the head says "still open
  after your answer of <time>" (`question_stop.py:468-505`).
- Nothing rewrites an existing open row's wording by id. Only the S2 tester's rework rewrites `requirements-readiness.json`
  (`artifact_producer.py publish`); `exit_gate.answered_question_errors` `:1276-1295` and `readiness_drift`
  (`question_register.py:498-521`) refuse a rewrite that drops or renames a row with a settled / deferred record.
- Rewording a row in place changes `row_hash` (sha256 of the whole row, `:149-156`): an earlier answer then reads
  `changed_since_answer` True and the row is open again with a note (`:264-272`). A reworded question under a NEW id has no link to the old.
- FR-7's `already_answered` / `question_body_sha` (`scripts/driver_dialog.py:29-38`, `:302-314`, `:381-392`) hash DRIVER question packets
  against `driver-answers.jsonl`; they do not read register rows; any changed word is a new question to them.

## The rehearsal's "cannot be answered as it stands"
- Text (`scripts/gate_preflight.py:1990-2022`): `{qid} cannot be answered as it stands ({defects}) — qa-requirements-tester rewrites it
  as what the source says plus the readings and where each comes from, before {role} is asked`; class FACTORY_FIXABLE; skipped for an
  answered or settled row.
- Defects (`scripts/contract.py:625-718`, `:869-878`): not an object; empty `question`; `source_says` names no quote (waived for a row
  with `asked_by`); `source_says[i]` needs quote and where; fewer than two readings; a reading not an object or with empty
  reading / from / if_chosen; `from` not a READING_ORIGINS word; a norms question from a code reading or naming a non-norm row; before/now
  incomplete (side needs value and where; reading from not claim); before/now readings lacking the claim mark.
- The cap: `controller.py` `repair_rounds()` `:380`, refusal text `:5630`. In the run: `factory-7.log:20`. After it the person saw
  ORDINARY cards with no defect line: Q1/Q2/Q3/Q6 print `a) ... (from ?)` / `b) ... (from ?)`, no "the source says" line, no before/now
  (`experiments/mybooks/factory-vs-free-agent/runs/factory-7.log:46-78`, `factory-6.log:98-117`). The sentence "cannot be answered as it
  stands" is in neither log.
- NOT TRACED: how the rehearsal finding reaches the conductor or the person after the cap; the cap logic in context; whether Q1-Q6 held
  `source_says` on disk (no `LOCAL-1/work/requirements-readiness.json` in the repo).
- Data a card could draw on, in the row or one reader away: `source_says`, before/now, `readings[].if_chosen`, `recommendation` and
  `read` (role rows), `raised_for` (case, Then), `requirement` / `ref`, the lines of `work/requirements-register.md`, `question_effects`,
  the answered rows (`answers_for_brief`).

## Rules already written
- `references/human-questions.md`: no rule about repeated questions or re-asking in other words (`:106-130` are gate B retry only).
- Phase cards carry "asked again" rules of other kinds (`skills/qa-story/phases/s2.md:100-113`, `s3.md:153-156`, `s1.md:381`), none
  about reworded repeats. `gate_brief.py:78` `DUPLICATE_KEYS` exists and was not read (bug drafts or questions — unknown).
