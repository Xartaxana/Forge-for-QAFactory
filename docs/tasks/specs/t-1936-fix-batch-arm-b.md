# t-1936 — fix batch of `experiment/thinking-roles` after arm B (LOCAL-1) — DRAFT SPEC (designer), critic round 1 applied

Status: Lead acceptance 2026-11-05 11:55 (Fable); critic-on-plan t-1938 verdict accept-with-fixes (3 blockers, 8 majors, 8 minors);
this text is the fix round (fresh designer). Forks decided by the Lead before the critic («решила сама», the owner may revert): 1 A;
2 B; 3 B and NO — a person's words travel only in the words file, never in `args`; 6 A; 9 A; 11 A. Owner's word 11:30 on F5(c): the
factory never stands — the walk runs even when preparation fails.
**Critic round 1, Lead decisions** (2026-11-05, «решила сама», the owner may overturn):
(B1) F5(c) the unprepared walk applies ONLY to preparation failures OWNED BY THE FACTORY (FR-46: a malformed plan row shape, a
recorder/tool crash or refusal after the scope checks, a missing fixture of our own) — never to story-owned reasons (an unconfirmed
expectation P20, gate A drift or no current gate A, an unpinned case, obligations not in the plan, an obligation/traceability
mismatch, an unreadable case file); those keep refusing as today with their owner named. The unprepared record has a road: it is a
manual record with `unprepared` and NO result; `validate_manual_current` classifies it with one constant; each of the four readers
carries it under its own name (F5.2(e)); the analyst judges its observations at S7; the report lists the case under "unprepared walks"
in Left with you. Forks 7 and 8 are reshaped accordingly (no pass/fail from an unprepared walk).
(B2) Fork 10: plain A — NO hand repair of `test-plan.json`; TS-14/15/16 stay as written; the rerun tests the door; the prepared road of
the X8 recorder is proven by unit tests now and by the next full run (the Lead's choice, for the owner to overturn). E5.3 rewritten.
(B3) F6 rewritten: reopen + release + stamped rework, absolute words files, `--cause reviewer_error`, measured dry run on a scratch copy
before the live run, controller state as the witness before the driver starts.
(F4) Fork 4 reversed: all three `—` moves become non-offerable (row reason in `conductor-actions.json`); no new tokens.
(F5) Fork 5 A with a binding: a `go on` waiver closes the stage only if recorded AFTER the critic dispatch it waives (field: the waiver
entry's `at` against the critic dispatch's journalled `created_at`).
(Majors 4-11, minors 12-19) pasted into the sections they name.
critic round 1: 19 resolved / 0 declined (minor 18 resolved by keeping the text, as the critic allows; under B1 the fourth reader,
`delivery_manifest.py`, carries no new key and its reason is written in F5.2(e)).
New forks of this round: 12 (S5 scope of the rerun vehicle), 13 (delivery verdict of a requirement whose only check was an unprepared walk).
Lead decisions 12:25: fork 12 A (one window TC_001/002); fork 13 A (today's trace road). Builders dispatched: N1 wt-fb1, N2 wt-fb2, N3 wt-fb3, N4 wt-fb4, N5 wt-fb5 (branches fb-n1..fb-n5 from c75ec3789).

Package under change: branch `experiment/thinking-roles`, head c75ec3789 (read-only checkout
`D:/ws1/exp-thinking-roles\pkg-b\ai-packages\qa-factory\`, below `PKG\`). Builders work in their own worktree of the
branch; every path below is package-relative (`ai-packages/qa-factory/...`).
Deferred (not in this batch): B-9 (plan row key `schema_version` not carried to the strategist), B-12 (gate A question form
does not see answered questions), B-13 (`vcs-test-repo: commit` not read by the gate). Also not in this batch: B-1 (fixed by
G10, cb032d204), B-4 (`handoff.py fill` exit 0 with no change), B-8 (`impl-diff.txt` placeholder under `current-code`).

## §1 Scope, AR-n touched, owners of every check

| item | class | AR-n touched (change check written into the node's DoD) | FR-n |
|---|---|---|---|
| F1 | stage-critic form skeleton (B-2, B-7, B-11) | AR-8 (code hands the path), AR-10 (requirement reaches the role in its field), AR-14 (one writer of the skeleton: `story_step._write_dispatch_files`), AR-15 (one placeholder token for "the author's form" in the S2-S4 critic contracts), AR-23 (empty list = declared outcome) | FR-15, FR-38, FR-1, FR-11 |
| F2 | conductor moves (B-3, B-10) | AR-1 (which move takes `args` / is offerable is a data column), AR-9 (refusal names expected shape), AR-16 (one question form), AR-17 (the seam), AR-24 (the conductor's words reach the person), AR-25 (no offered word without an executor) | FR-9, FR-10, FR-13, FR-38, FR-42 |
| F3 | person's word without a reader (B-6) | AR-13 (`waiver.split_overridden` the one reader), AR-24, AR-25 | FR-4, FR-8, FR-9, FR-12 (n/a, see F3.2 step 5) |
| F4 | code critic without typed findings (B-14, regression vs 0.10.9) | AR-10, AR-15 (the existing closed site question `s5.nobody_review` is the survivor), AR-19 (S5/S7 twins of `route`), AR-28, AR-29 (presence check only) | FR-1, FR-38, FR-47, FR-59 |
| F5 | manual S6 preparation (B-15) | AR-2, AR-10, AR-13 (one reader of unprepared rows), AR-17, AR-22 (every new field has its reader), AR-23, AR-27 (the unprepared walk reaches the report under its own name), AR-28 | FR-1, FR-4, FR-18, FR-19, FR-38, FR-41, FR-46, FR-59; P20, P21, P22, P26 |
| F6 | rerun procedure (no code) | — | P8 |

Owners and census class of every check this batch ADDS or ALTERS (AR-29, host adaptation 10). Census class words are the words
`scripts/tests/fixtures/judgment-census.json` holds: `shape`, `xref`, `safety`, `meaning`, `meaning-proxy` (critic t-1938 count:
shape 694, xref 121); "presence" is `shape`, "join" is `xref`.

| check (file :: function) | added / altered | owner it serves | census class | why it is not a judgment |
|---|---|---|---|---|
| `handoff_check.py :: check` (new `rows_owed_when` problem, F4) | added | data (code) | shape | counts rows of a section under a verdict word; never reads what a finding says |
| `stage_done.py :: record_acceptance` refusal text (F1) | altered (text only) | data | shape (row exists) | the check (`reviewed_author_dispatch`) is unchanged |
| `no_move.py :: validate_options` (F2) | altered | data | shape | reads option keys against data columns; the conductor's choice of move stays its judgment |
| `story_run.py :: person_pass` (F3) | added | intent (the person's recorded word) | xref | joins a recorded `match` (and its `at`) to a code-produced line and the critic dispatch's journal time |
| `repair_route.py :: route` (F4) | altered | data | shape | "no typed row under a send-back verdict" is the absence of a row; no cause is assumed |
| `coverage_contract.py :: validate_obligations` `evidence_policy` (F5) | altered | data | shape | type + membership in `POLICIES` |
| `manual_evidence.py :: prepare_request` `evidence_policy` + walkable split (F5) | altered | data | shape | type check; the walkable set is a closed positive list of the factory's own failures |
| `coverage_contract.py :: validate_manual_current` unprepared branch (F5) | altered | data | shape | presence of the code-written `unprepared` request and absence of `result`; it never reads what the walk found |
| `manual_evidence.py :: write_block` (refuses `result` on an unprepared record, F5) | altered | data | shape | a key's presence |
| `manual_evidence.py :: prepare_for_block` door (F5) | altered (error direction) | judgment (the manual agent walks; the analyst judges at S7) | n/a (routing, not a check) | code routes the case to the role; it judges nothing |

---

## F1 — stage-critic form skeleton (B-2, B-7, B-11)

### F1.1 Facts (read, with carrier)
- `handoff_init.fill_head` (`PKG\scripts\handoff_init.py:114`) substitutes `<TICKET>`, `work/handoffs/<dispatch>.yaml`, `<dispatch>`
  and four header values; it never touches the author placeholder.
- Author placeholders are contract text: `s2-stage-critic-to-tester.yaml:15` `<the tester's dispatch>`,
  `s3-stage-critic-to-strategist.yaml:15` `<the strategist's dispatch>`, `s4-case-critic-to-designer.yaml:18`
  `<the designer's dispatch>`, `s5-critic-to-automator.yaml:14` and `s5-critic-plan-to-automator.yaml:24,40`
  `<the automator's dispatch>`. The `inputs_read[0].path` template is `<path exactly as listed in inputs>` (s2:29, s3:32),
  `<path exactly as the designer listed it>` (s4:31), `<path exactly as the author listed it>` (s5:28).
- `stage_done.reviewed_author_dispatch` (`stage_done.py:867`) reads ONLY `inputs_read[].path`, last match wins; `version`/sha256 is
  never read there. `handoff_check._version_of` derives `version` from a real path (scout Q1).
- The refusal `stage_done.py:956-957` says "...list the author's form `work/handoffs/<its dispatch>.yaml` in `inputs_read`
  (path and sha256), then record it again". It does NOT name the concrete expected path (the author id is known at :910) and it
  DOES mention sha256.
- The contract file IS the schema: `handoff.spec(contract)` = `spec_of(template(contract))` (`handoff.py:613`);
  `handoff_check.open_row` (`handoff_check.py:2230`) opens a new row from the contract's first row, also when the form holds
  `section: []`; `_open_rows_for` (:2273) opens rows in order, so `questions[1]` into `[]` needs `questions[0]` first (critic t-1938);
  `handoff_check._is_empty_section` (:969) treats an all-placeholder list exactly as `[]`. Template rows STAY in the contract files;
  the change is in the SKELETON (the role's copy).
- B-11 reader: `question_register --from-handoff` reads the template row of `questions:` as a question (scout Q1).
  `repair_route.findings` already drops rows whose `id` is a placeholder (`repair_route.py:62`).
- B-7: `run_role(rework=...)` (`story_run.py:2795-2807`) calls only `story_step._brief` and `_prompt`; no form skeleton, no
  launch card. The ONE writer of brief+form+card is `story_step._write_dispatch_files` (`story_step.py:1081`, `keep=` semantics); it
  returns `(card, written)`, prints its own notes, and with `keep=True` KEEPS an existing brief (critic t-1938 minor 14).

### F1.2 Required behaviour
(a) **Author path filled by code (S2, S3, S4 only).** The three stage-critic contracts S2/S3/S4 use ONE placeholder token for the
author's form path: `work/handoffs/<the author's dispatch>.yaml` in `inputs[0].path`, and `inputs_read[0].path:
work/handoffs/<the author's dispatch>.yaml` as the first `inputs_read` row (the second template row keeps `<path exactly as listed in
inputs>` for the other inputs). Both S5 contracts (`s5-critic-to-automator.yaml`, `s5-critic-plan-to-automator.yaml`) keep their
`<the automator's dispatch>` token unchanged (Fork 2-B: nothing fills it; minor 13). `handoff_init.py` gets a new optional argument
`--author-dispatch <id>`; `fill_head(..., author_dispatch="")` replaces the token `<the author's dispatch>` with the id when given,
leaves it untouched when not given, and — when it filled the token — writes one YAML comment line directly above `inputs_read:` of
the skeleton: `# inputs_read[0] names the author's form the driver handed you; change it if you reviewed another` (minor 19: the
pre-filled row is the critic's attestation, its own word to change, E1.4). `story_step._handoff_form` passes `--author-dispatch` ONLY
when the contract text holds the token `<the author's dispatch>` (minor 12 — S6/S7 also have `acceptance_by`, their contracts carry
no such token), with the id `acceptance.stage_author_dispatch(controller_state, acceptance.stage_def_of(stage))` — the same function
`stage_done.record_acceptance` compares with (`stage_done.py:910`).
Two roads for one fact (critic §6, AR-15): the S6/S7 consumer roads name the author's path in brief text (`story_run.py:12273,
:13238`); the S2-S4 roads get the skeleton token. Both stay in this batch: the brief line is reading guidance, the form row is the
attestation code reads. Moving S6/S7 to the token is queued (Deferred: finding file of this batch's pile).

(b) **Empty lists in the skeleton.** After `inline_values` and after `--carry-from` / `--rows` (order in `handoff_init.main`:
`fill_head` -> `carry_from_parent` -> `prefill_rows` -> write), a new step `empty_optional_lists(text, contract)` rewrites, in the
role's copy only, every TOP-LEVEL list section that (i) is not in `handoff.REQUIRED_LISTS`, (ii) is not a `null_outcome` section of
the contract, (iii) still holds only placeholder rows (`_is_empty_section` semantics), and (iv) is one of the sections Fork 1-A
selects — `questions` (S2/S3/S4 critics) and `findings` (S2/S3/S4/S5 critics) — into `<section>: []` followed by the sample rows as
comment lines (`#   - question: "<...>"`, vocabulary hints kept as `inline_values` rendered them). The contract files are not edited
for (b).

(c) **Refusal text.** `stage_done.record_acceptance` (:956) names the concrete expected row and drops sha256:
`the stage critic's form <rel> does not say which dispatch of <author_role> it reviewed: its inputs_read needs the row
path: work/handoffs/<author>.yaml (the author's last accepted dispatch), then record it again` — with `<author>` from `:910`;
when `author` is `""`: `... no accepted dispatch of <author_role> exists at <stage> yet, so no review can be recorded`.

(d) **B-7 relaunch** (major 4). `Driver.run_role`, `rework` branch (`story_run.py:2795`): when the dispatch's handover form
(`work/handoffs/<dispatch>.yaml`) OR its launch card is absent, call `story_step._write_dispatch_files(self.task, stage, role,
dispatch, self.task_root, ",".join(rework.get("scope") or scope), notes, keep=True)`; otherwise keep today's `story_step._brief` call
(a continuation keeps writing a fresh brief, as today). The brief path for `_prompt` is
`story_step._project_rel(self.task, story_step.BRIEF_REL, dispatch)`. The notes are printed by the callee; the branch does not print
them again. A `ValueError` from a differing launch card (keep semantics, `story_step.py:1127`) is printed once as `note: ...` and the
role still runs (P1: the prompt carries everything; a card mismatch never stops a dispatch).

### F1.3 Edges (each with its invariant)
- E1.1 `stage_author_dispatch` returns `""` (no accepted author dispatch yet) -> no `--author-dispatch`, the token stays a
  placeholder, no comment line. INVARIANT: a guessed author never stands in a form — "a record given for other bytes does not count".
- E1.2 The controller state cannot be read in `_handoff_form` -> same as E1.1 (FR-59).
- E1.3 A rework of the AUTHOR after the skeleton was written (new author dispatch) -> the critic of that later round is a new
  dispatch with a new skeleton; an old critic form keeps its old author. INVARIANT: `stage_acceptance_errors` still refuses an old
  binding.
- E1.4 The role edits row 0 to another path -> the role's word stands (`reviewed_author_dispatch` takes the LAST matching row); the
  comment line tells it so.
- E1.5 `--carry-from` (repair dispatch) and (b): a carried row makes the section non-empty -> it is not emptied. INVARIANT: the carry
  is never undone by the emptying step (order fixed: emptying runs LAST).
- E1.6 (b) never empties `scope` (REQUIRED_LISTS) or a `null_outcome` section. INVARIANT: an untouched required list still reads as
  "no rows" and is refused (`handoff_check.py:1404`); check verdicts are byte-identical before/after (b) — the witness proves it on
  the S2/S3/S4/S5 critic contracts.
- E1.7 Values file writes `questions[0].question: ...` into a form whose `questions: []` -> `open_row` opens row 0 from the contract
  (existing code); `questions[1]` without `[0]` into an emptied section -> the existing refusal naming `questions[0]` as the next row
  is the declared outcome (minor 14). INVARIANT: an emptied section never accepts a row the template would not.
- E1.8 Temporal (new argument): skeletons written before this change stay on disk (`keep=True`); only new dispatches get the new
  skeleton. Both worlds read by the same `check`.
- E1.9 (d) a rework dispatch whose form and card are on disk (driver restarted) -> today's `_brief` road, no rewrite of the form.
  INVARIANT: a form the role may already have filled is never overwritten.

### F1.4 Sweep (template rows in lists, by contract — the class enumerated)
Every contract under `handoffs/` has template rows in its lists (grep `^\s*- [a-z_]+: ["']?<` over `PKG\handoffs\`: 25 files). This
is the factory's form idiom, BECAUSE the contract is the schema. The defect is only where a READER treats a placeholder row as data:
- `question_register --from-handoff` (B-11): applied — (b) + the reader drops a row whose `question` is a placeholder (E1.8).
- `repair_route.findings`: n/a — already drops placeholder ids (`repair_route.py:62`).
- `handoff_check.check`: n/a — `_is_empty_section`.
- Other readers of list sections of handoff forms: N1 reports a table (one line per `--from-handoff` / `form_view(...).data.get(<list>)`
  reader: drops placeholders / does not -> fix only for `questions`, else "queued" with pointer).

### F1.5 Tests (files are the narrowed witness)
- `scripts/tests/test_handoff_init_author.py` (new): `test_author_token_filled_s2_s3_s4`, `test_author_comment_line_written_when_filled`,
  `test_author_token_left_when_unknown`, `test_s5_contracts_get_no_author_arg`, `test_no_author_arg_without_token` (an S6 contract
  with `acceptance_by`), `test_empty_optional_lists_questions_findings`, `test_scope_never_emptied`, `test_carry_survives_emptying`,
  `test_check_verdict_unchanged_by_emptying`, `test_values_row_opens_in_emptied_section`,
  `test_second_row_without_first_refused_in_emptied_section`.
- the test file that judges `stage_done.record_acceptance` (`grep -l record_acceptance scripts/tests`):
  `test_refusal_names_author_path_no_sha256`, `test_refusal_when_no_author_yet`.
- `scripts/tests/test_rework_dispatch_files.py` (new, fast, mocks `run_claude`): `test_rework_branch_writes_form_and_card_when_absent`,
  `test_rework_branch_keeps_brief_road_when_form_present`, `test_rework_branch_card_mismatch_is_one_note`.
- `scripts/tests/test_question_register.py`: `test_placeholder_question_row_dropped`.

---

## F2 — conductor moves (B-3, B-10)

### F2.1 Facts
- `no_move.validate_options` (`no_move.py:321`): `elif "args" in option: refuse` (:371-372) for every move but `rework_stage`;
  token `—` can never be an option (:348, :359). arm B `state\conductor.jsonl`: 8 `unusable` lines (7 args/token, 1 cap; scout Q2).
- `Driver._no_move` (`story_run.py:5294-5330`): an unusable verdict that is not `ArgsRefused`/`ClassRefused` and not a `chosen` call
  -> `fallback_person(state, rule)` -> `NM.render_question(lead, fallback options)`: the conductor's `question` is dropped.
- The conductor charter is `PKG\references\conductor.md` (no `agents/qa-conductor*.md`; 12 role files). Its "Your answer" line 92
  shows ONE option schema with `"args": {...}` in every option. `story_run.py:4989` already tells the conductor "`args` goes with the
  `rework` option only", and the conductor still did it (critic t-1938) — the data column + drop (Fork 3-B) is what holds.
- `conductor-actions.json` `moves`: tokens `—` on `resume_with_words`, `story_fact`, `revoke_exclusion`; no code executor exists for
  `resume_with_words` or `revoke_exclusion` (critic grep: only `no_move.py:137/142`; control: the same grep finds both table keys). Their
  `run` texts need the person's free words (`--words`), which reach the conductor already.

### F2.2 Required behaviour
(a) **The conductor's text always reaches the person** (major 8). When the conductor answered `ask_person`/`stop` with a non-empty
`question` and `validate_options` refused the options, `_no_move` passes that question to `fallback_person(state, rule,
conductor_text=<question>)`; the fallback renders `lead`, then the fixed line `What the conductor found:`, then the conductor's text
VERBATIM cut at 1200 characters (the `lead` limit; a cut ends with `…`), then the priced fallback options. Each token the conductor's
text quotes in backticks that is NOT among the shown options gets one code line after the text: `` `<token>` is not offered here:
<rule in plain words> `` (FR-10). The `defect_found` and the `unusable` mark stay exactly as today (one per failure).
(b) **Data columns.** Each row of `moves` gains `"args": "rework" | null` (`rework` = the closed list `check_args` checks) and
`"offerable": true | false`, with `"not_offered": "<why>"` when false. `validate_options` reads the columns, not the literal
`rework_stage`: a move whose `args` column is `null` and whose option carries `args` -> the `args` key is dropped, the option kept, and
`conductor.jsonl` gets `args_dropped: [<tokens>]` on that line (Fork 3-B). An option naming a move whose `offerable` is false ->
refused as today's `—` rule, with the row's `not_offered` text in the refusal. Rows (major 7, Fork 4 reversed): `resume_with_words`,
`revoke_exclusion`, `story_fact` -> `offerable: false`, tokens stay `—`; `not_offered` for `resume_with_words` and `revoke_exclusion`:
`"run on the person's own words, never an option: a token answer carries no words"`; for `story_fact`: `"the conductor's own move: it
runs it with a value a script or the person named; never a person's choice"`. `moves_section` prints, per open move, its token and one
of `option carries "args"` / `option carries no "args"`; a non-offerable move is printed as `- <move> — run on the person's own words,
never an option` (`story_fact`: `- story_fact — yours to run, never an option`). No new tokens; E2.3 of the earlier draft is moot.
(c) **Charter.** `references/conductor.md` "Your answer": the option schema per kind — an option is `{"token", "move", "says",
"factory", "person", "story"}`; ONLY a move whose `args` column is `rework` adds `"args"`; a person's words never travel in `args`.
Name the moves section of the prompt as the place that says which move takes `args` and which moves are never options. One
sentence, no new section (P27).

### F2.3 Edges
- E2.1 Temporal: before (b) lands, the columns are absent -> a missing `args` column reads as `null` EXCEPT for the row `rework_stage`
  (compatibility); a missing `offerable` reads as `true` unless the token is `—` (today's rule). After, the columns rule. Tests pin
  both data files. INVARIANT: `rework` args are still checked by `check_args` in both worlds; no other move gains an executor for `args`.
- E2.2 A column value other than `rework`/`null` (or `offerable` not a bool) -> `DataUnreadable` naming the row (never a silent pass).
- E2.3 An `args` drop never turns a refused option into an accepted one for any other reason. INVARIANT: every other rule of
  `validate_options` runs on the option as the conductor wrote it.
- E2.4 (a) with an EMPTY conductor question -> today's behaviour. (a) with `options` absent -> same as today.
- E2.5 (a) at a gate (`GATE_KINDS`) -> `gate_fallback_question` gets the same conductor block. INVARIANT: at a gate `go on` is still
  not offered (`last_resort` rule) — the added text offers nothing.
- E2.6 The lone chosen-rework option keeps its own rule (`len(options)==1` only for `rework` when chosen) — unchanged.
- E2.7 A conductor text longer than 1200 characters -> cut, the token lines are computed on the WHOLE text. INVARIANT: a token the
  person reads is either offered or named as not offered.

### F2.4 Tests
`scripts/tests/test_no_move_seam.py`: `test_args_column_reads_data`, `test_args_on_null_column_dropped_and_journaled`,
`test_missing_column_compat_rework_only`, `test_bad_column_value_unreadable`, `test_dash_moves_not_offerable`,
`test_not_offered_refusal_quotes_row_reason`, `test_moves_section_says_args_and_never_an_option`.
`scripts/tests/test_conductor_doors.py`: `test_refused_options_keep_conductor_question`, `test_conductor_text_cut_at_1200`,
`test_unoffered_token_named_in_one_line` (the prose names `restart` while `restart` is not offered), `test_gate_fallback_keeps_conductor_text`.

---

## F3 — person's word without a reader (B-6)

### F3.1 Facts
- `waiver.record_stage_overrides` wrote `{"stage":"S2","match":"the verdict word of the stage critic is unreadable",
  "decision":"go on","by":"human"}` (arm B `pipeline.json`, scout Q3); every waiver entry carries `at` (`waiver.py:149`), and
  `split_overridden` returns it on each passed entry (`waiver.py:219`).
- `stage_review_exhausted(stage, author, critic_dispatch, record, form, unreadable=False, text="")` (`story_run.py:9530`): `author` is a
  ROLE name; it builds a seam state with NO `lines`, calls `no_move`, then computes `author_last` and reads only `accepted_for(...,
  acceptor=driver)` and a newer author dispatch. It never reads `stage_overrides`.
- The working pattern: `consumer_person_pass` (:9298) reads a live waiver through `waiver.split_overridden` and records the pass with
  the ONE writer `stage_done.py --acceptance work/handoffs/<author>.yaml --acceptor driver --verdict accept --quote "by: person - <words>"`.
- A dispatch's creation time is the `created_at` of its `dispatch` event: `Controller._dispatch_starts()` (`controller.py:6908`).

### F3.2 Required behaviour
1. `stage_review_exhausted` builds `line = f"{acceptance.STAGE_ACCEPTANCE_PHRASE}: {text}"` and puts `lines: [line]` in the seam
   state, so `standing_refusal` records it and `waiver.py --block` is verified against it.
2. New helper `Driver.person_pass(stage, author, line, answer="", since="") -> bool` holds the body of `consumer_person_pass` after its
   first two guards (split_overridden on `[line]`, then the one stage_done writer, then the print). `since` (major 5, Fork 5 binding):
   when non-empty, a passed entry is honoured only when its `at` is LATER than `since`; both are read through one normaliser
   (`controller.stamp_utc`); an `at` or a `since` that cannot be read -> not honoured. `consumer_person_pass` calls it with `since=""` —
   byte-identical behaviour (its tests stay green unchanged).
3. In `stage_review_exhausted` (minor 15): compute `author_last` (the author role's last accepted dispatch, the same expression the
   function uses today after `no_move`) and `since = Controller(task_root)._dispatch_starts().get(critic_dispatch, "")` FIRST; then
   (i) BEFORE `self.no_move(state)`: `if self.person_pass(stage, author_last, line, since=since): return None`; (ii) AFTER `no_move`
   returns, after the existing `accepted_for(..., acceptor=driver)` check and BEFORE the "newer author dispatch" check: the same call.
   `since == ""` (the critic dispatch has no journalled start) -> `person_pass` is not called at all (safe side: the conductor/person
   is asked).
4. A pass files ONE finding (P13) through `self.owe_row("project_decisions.py", "--root", str(self.project), "add-finding",
   "--essence", f"{stage} closed on the person's word over: {line}", "--scope", "local-calibration", "--witness", <the waiver entry's
   match and at>, "--idempotency-key", f"stage-review-pass:{self.task}:{stage}:{critic_dispatch}", what=..., stage=stage)` (the pattern
   at `story_run.py:11285`).
5. `controller.py:5341`: n/a for FR-12 — `_passed_by_person` -> `split_overridden` -> `contract.names_whole`; no wording is read by a
   phrase list (`names_whole("stage acceptance", "stage acceptance: ...")` passes, critic t-1938 §1).

### F3.3 Edges
- E3.1 `author_last == ""` -> `person_pass` returns False and the seam goes on as today. INVARIANT: no accept record without an author
  dispatch.
- E3.2 Revoked override / placeholder `match` -> passes nothing (`split_overridden` rule). `*` passes (existing semantics, kept).
- E3.3 A waiver recorded for ANOTHER stage -> not read (`live_stage_overrides(pipeline, (stage,))`).
- E3.4 The verdict is readable as a reject on the last round -> the same read applies; a person's `go on` RECORDED AFTER this critic
  dispatch accepts the stage with the gap (Fork 5-A, P13); the quote keeps the critic's verdict on record.
- E3.5 Position (i): INVARIANT — the pass is consulted only for the line of THIS exhausted review and only for a word recorded after
  this critic dispatch started; with no such pass the conductor is called exactly as today. Position (ii): INVARIANT — a conductor's
  own driver-accept still wins first; the "newer author dispatch -> OpenWork" branch is unreachable after a recorded pass.
- E3.6 A `stage acceptance` waiver recorded on an EARLIER round (before this critic dispatch) -> not honoured (major 5). INVARIANT: a
  person's word never accepts an author dispatch the person never saw (FR-4: no silent pass).

### F3.4 Sweep inside `story_run.py` (the builder fills the table; seeds checked by the critic)
Enumerate every `no_move(...)`/`Refusal(...)` site whose text or door names `waiver.py --block` or whose seam state can be passed by
`go on`, with a verdict line each: `reads split_overridden: yes (line)` / `fixed in this node` / `n/a — why` /
`deferred -> plans/piles/<slug>/findings/<file>`. Seeds: :1319 yes; :3330 yes; :8980 yes; :9313 consumer_person_pass yes; :9969 yes;
:11486 yes; :11762 yes; :12044 yes; :9540 stage_review_exhausted -> fixed here; `repair_limit_raise` (:10863, site question, `go on`
not a door) n/a; the S5 `stage_complete: false` refusal of arm A -> the builder classifies it.

### F3.5 Tests
`scripts/tests/test_stage_review_person_pass.py` (new, fast, Driver stub): `test_live_waiver_closes_before_conductor`,
`test_waiver_recorded_during_seam_closes_after`, `test_older_waiver_does_not_pass_later_review`, `test_unreadable_at_not_honoured`,
`test_no_dispatch_start_no_pass`, `test_revoked_waiver_passes_nothing`, `test_other_stage_waiver_ignored`, `test_no_author_no_pass`,
`test_line_carries_stage_acceptance_phrase`, `test_pass_files_one_finding_idempotent`, `test_consumer_person_pass_unchanged`.

---

## F4 — code critic without typed findings (B-14, regression)

### F4.1 Facts
- `repair_route.route` (`repair_route.py:110-115`): `form is None or (not rows and sends_back)` -> `test_defect_round("no typed
  findings", "no typed findings; cause assumed test_defect")`.
- The form passed the gate because `findings` is not in `handoff.REQUIRED_LISTS` (`handoff.py:444` = `("scope",)`); `required_when`
  only RELAXES fields (`handoff.relaxed_sections`, :521).
- The handoff gate resumes a role ONCE per finding set (`Driver.handoff`, `story_run.py:2470`).
- A closed site question for "sent back naming nothing the test writer can repair" already exists: `repair_limit_facts`
  (`story_run.py:10811-10856`) maps `code == "nobody"` with cause `reviewer_error` to key `s5.nobody_review`, offer
  `["review", "debt", "stop"]`, `call=False` (`repair_limit_raise` :10858, D-0041); `review` = "the critic reviews the window again;
  this round spends none of the repair limit". `repair_limit_gate` (:10776) refuses as an older controller when
  `route["code"] != "unknown"` and `repair_passes(budget) is None` (:10799).
- The S7 twin: `s7_reorder_outcome` (`story_run.py:12949-12985`) reads the critic's form through `route_of`; today an untyped
  send-back gives `test_defect` -> `retry`.
- Charter `PKG\agents\qa-code-critic.md`: L22/L66 name `cause`, no line says to write `findings[N].cause` through the values file;
  L65 says findings go to `work/test-code/critic-findings.md`; L70 uses `cause: data_row`, which is not a `repair_causes` word. The
  0.10.9 table "Every finding names its cause" is `D:/ws1/exp-thinking-roles\pkg-a\ai-packages\qa-factory\agents\qa-code-critic.md`
  L118-135 (read by the critic t-1938).
- S2/S3/S4 critic rounds (`story_run.py:9418`, `:9469`; S4 `s4_after_critic` :9581 `cause="test_defect"`): their contracts carry no
  `cause` field, so the round is `test_defect` by design, not an assumed cause — n/a for this item.

### F4.2 Required behaviour
(a) **Charter** (majors 11, minor 17). `agents/qa-code-critic.md` is static text, so the cause list is written in it and a test holds
it equal to `handoff.allowed("repair_causes")`. In the Tools section: one paragraph + the 0.10.9 table, re-worded as craft ("a finding
the author can act on names its cause; the route reads `findings[N].cause`"): the key paths `findings[N].id`, `.file`, `.line`,
`.problem`, `.expected`, `.cause`, `.blocking`, written as `path: value` lines in the values file the form's `# Fill:` line names;
`cause` one of `test_defect | mechanical | environment | tooling | reviewer_error`. L65 reworded: `each finding is a findings[N] row of
your form (values file); critic-findings.md holds the roll-call and notes`. L70 `cause: data_row` reworded as `the probe's data_row
case` (not a finding cause), BEFORE the equality test pins the list.
(b) **Presence at the form gate (one return to the critic).** New contract key (data, AR-1) in `s5-critic-to-automator.yaml`:
`rows_owed_when: {concerns: [findings], review: [findings]}` (the verdict words that send back = `repair_route.SEND_BACK`; a test holds
the two equal). New reader `handoff.rows_owed(contract_id, header_value) -> set` (shape of `relaxed_sections`: malformed block ->
empty set). `handoff_check.check` adds a problem for each owed section that is empty (`_is_empty_section`): `findings: no rows. The
verdict <w> sends the window back, so each thing the author must change is a row: <row sentence from row_form>; cause is one of
<list>`. The existing handoff gate resumes the critic once with that text (FR-1). The contract key and its reader are in ONE node (N2,
major 10).
(c) **No assumed cause.** `repair_route.route` rule (a) for `not rows and sends_back` (form readable) and for `form is None` with
`sends_back`: return `answer("close", "no typed findings", code="untyped")`; never `test_defect`. `findings()` keeps its unknown-cause
-> `test_defect` mapping for a ROW whose cause is outside the list (a typed row exists; B-364) — a different case, out of this item.
(d) **The site question, no conductor call** (major 6, D-0041). `repair_limit_facts`: `code == "untyped"` -> key `s5.nobody_review`,
offer `["review", "debt", "stop"]`, cause `reviewer_error`, opening `For <cases>: the critic sent the tests back but wrote no finding
the test writer can act on; the critic can review again and name them.` `repair_limit_gate` line :10799 skips the older-controller
refusal for `untyped` as it does for `unknown` (`route["code"] not in ("unknown", "untyped")`) — the builder confirms by test that
the executors of `review` and `debt` do not read `passes`; if one does, the refusal stays for `untyped` and the report says so. No
conductor call; no new question key; the existing executors of `review`/`debt`/`stop` run (the `debt` entry `s5_window_closed` reads,
:10608, is written by the existing `debt` executor).
(e) **The S7 twin** (major 9). `s7_reorder_outcome`: `route["code"] == "untyped"` -> `no_progress` with the printed reason
`S7: <test> - the critic sent the repair back without a typed finding; the round is stopped` (a branch before the generic
`route["code"]` line :12981).
(f) F1(b) gives `findings: []` in the critic's skeleton (owned by N1).

### F4.3 Edges
- E4.1 Temporal: N2 ships the contract key and its reader together; before N2 merges, `rows_owed` does not exist and nothing changes;
  after, the form gate catches an empty send-back first and (c)-(e) catch what passes it (`finish --ignore-handoff`).
- E4.2 Verdict `ok`/`approved` with zero findings -> not owed, passes (no change).
- E4.3 A send-back with only `tooling_findings` rows -> owed `findings` empty -> refused once (Fork 6-A); the refusal lists `tooling`
  as a cause, so `findings[0].cause: tooling` is a legal row (-> route `nobody`).
- E4.4 A role that the gate resumed and still returns no row -> the handoff gate's existing "after one resume" path; INVARIANT: never a
  second paid resume for the same finding set (t-217).
- E4.5 Form passed with `finish --ignore-handoff` -> (c) `untyped` -> (d) the site question. INVARIANT: no route ever dispatches the
  author on a cause nobody wrote.
- E4.6 Budget unknown + untyped -> `untyped` wins (the site question asks); the budget is not read for a close.
- E4.7 S7: an untyped send-back of a repair review -> `no_progress`, the debt stays in the triage row. INVARIANT: S7 never starts a
  round on an assumed cause either.
- Error direction of `route` in its gate role (designer rule 1): allowed error = asking the person (closed, priced, no paid call) when a
  round would have been right; forbidden = a round on an assumed cause. Adversarial inputs that must stay on the safe side: `findings`
  absent; `findings: []`; one row with placeholder `id`; one row with real `id` and placeholder `cause` (-> `findings()` mapping,
  refused earlier by the form gate as `not filled`); verdict `review`; verdict word with trailing spaces; form unreadable.

### F4.4 Tests
`scripts/tests/test_repair_route.py`: `test_untyped_send_back_closes_untyped_not_test_defect`, `test_form_none_send_back_untyped`,
`test_ok_without_findings_closes_plain`, `test_send_back_words_equal_rows_owed_words`, `test_untyped_asks_review_debt_stop`,
`test_untyped_skips_older_controller_refusal`, `test_s7_untyped_is_no_progress` (or in the S7 test file that already judges
`s7_reorder_outcome`: `grep -l s7_reorder_outcome scripts/tests`; a SLOW file -> CI only). New `scripts/tests/test_rows_owed.py`:
`test_rows_owed_reads_block`, `test_malformed_block_owes_nothing`, `test_check_refuses_empty_findings_under_concerns`,
`test_check_passes_empty_findings_under_ok`, `test_refusal_names_cause_list`. Charter: `test_code_critic_charter_names_cause_key`,
`test_code_critic_charter_cause_list_equals_vocabulary` (in the file that pins charter text — `grep -l qa-code-critic.md scripts/tests`).

---

## F5 — manual S6 preparation (B-15)

### F5.1 Facts
- `manual_evidence.prepare_request` (`:905`): order — `_validate_gate_a_content_current` (:919) -> current gate A (:921-923) ->
  `validate_plan(rows)` WHOLE-PLAN (:925-929) -> case pinned (:930-934) -> `expectation_gaps` (P20, :939-947, refused BEFORE the scope
  checks by design, docstring :907-910) -> obligations in plan (:949) -> obligation/traceability mapping (:953-958) -> three scope checks
  (:960-972) -> policy set (:973, `TypeError: unhashable type: 'dict'` on arm B TS-14/15/16) -> mixed policies/conditions (:975) ->
  `_case_thens` (:982, `Refused` when the case file cannot be read) -> request.
- `planning_contract.validate_plan` returns `coverage_contract.validate_obligations(rows)` (critic t-1938): after F5(a), an old plan with
  a dict is refused at :925 for EVERY manual case of the plan, never at :973.
- `POLICIES = {"ui","api","cli","no_write","static"}` (:34); `RESULTS = ("pass","fail","inconclusive")` (:35).
- `prepare_to_file` (:1075) writes `request.json` = the request or `{"refused": {"reason","door"}}`; `prepare_for_block` (:1095)
  returns `(ids, "")` or `([], "<reason> — <door>")`; its catch-all keeps `type + 160 chars`; its docstring states the CURRENT error
  direction "toward NOT checking by hand, P20". F5(c) reverses it for the factory's own failures only (owner's word 05.11 11:30).
- `write_block` (:1129): every record runs `_validate_current` -> `coverage_contract.validate_manual_current` (:645-705: obligation
  hash, completion condition, `approved_policy_hash`, `gate_a_decision_ref`, source revision, runtime provenance) and, when the case's
  request lists Thens, the quote rule (`_request_thens`, `_then_coverage_problems`). Records of one block share `dispatch_id`, attempt
  timestamps and `source_revision` (:1168-1173). `declared=True` (the CLI `write-block`) requires `observations` (`[]` when none).
- The four readers of `validate_manual_current` that filter records: `finalize_task.py:555` (builds `current_manual_checks`; issues ->
  `result="inconclusive", evidence_validated=False`), `coverage_contract.py:577-579` (projection of manual obligations;
  `execution = passed|failed|inconclusive if manual else not_run`), `ledger.py:1249-1251` (evidence export), `delivery_manifest.py:80-82`
  (index check).
- S7: `s7_pretriage.failing_manual_rows` / `_why_not` read `current_manual_checks` through `contract.triage_targets`; a row with
  observations is "the analyst's call (P26)" (:164-165).
- Left with you: `check_delivery.build_left_items` (:2018) keeps records whose kind's verdict is `after_checks` in
  `references/delivery-verdict-kinds.json` (`kinds` rows `{verdict, owner}`; e.g. `manual_human: after_checks / environment`).
- The X8 recorder `manual_capture.py` does not read `request.json` (case-insensitive grep `request\.json|request_path|prepare_request`:
  0; control `refused`: 60, critic t-1938) — the role can drive it for an unprepared case.
- Refused cases today: `Driver.run_manual_block` prints `not checked by hand`; `story_step` manual block refuses the whole block when any
  case is refused (`story_step.py:985-991`).

### F5.2 Required behaviour
(a) **Shape at the plan exit + the field told to the strategist.** `validate_obligations`: `decision == manual-agent` ->
`evidence_policy` must be a `str` whose `strip()` is in `POLICIES` (import the one set; no copy), error
`"<oid>: evidence_policy is one word of api|cli|no_write|static|ui; evidence kinds, phases and the completion condition go in
completion_condition and the observation fields"`; the fixed part `evidence_policy is one word of` is a module constant
`coverage_contract.POLICY_SHAPE_ERROR` (one producer; read by (c)). `manual-human` -> a non-empty `str` (no membership; C5). The
strategist slice `references/slices/qa-test-strategist/artifact-contract-plan.md` (FR-38) gets the line for `evidence_policy` with the
five words; `coverage-design.md:157-160` is re-worded so "state the evidence kinds" names `completion_condition`/observation fields as
their place.
(b) **No bare TypeError.** `prepare_request` checks each selected obligation's `evidence_policy` is a `str` before the set (:973);
else the walkable refusal of (c). `prepare_for_block`'s catch-all keeps `traceback.format_exc()` (last 20 lines, C3) under `trace` in
the request file (an artifact the conductor reads; never shown to the person).
(c) **The walkable set — a closed positive list** (blocker 1, Lead decision B1). `Refused` gains `walkable: bool`, default **False**
(every existing refusal stays as today). Walkable — and only these:
  1. `validate_plan` (:925) errors that are ALL `evidence_policy` shape errors (each error contains `POLICY_SHAPE_ERROR`): the refusal
     is NOT raised at :925; `prepare_request` remembers it and runs every later check of the case (pinned, `expectation_gaps`,
     obligations in plan, mapping, the three scope checks), each raising `walkable=False` as today; only when all of them pass, it
     raises `Refused("the plan gives <case>'s check an evidence rule that is not one word", <door as today>, <the errors>,
     walkable=True)` naming the row ids and the five words. A `validate_plan` result with ANY other error -> today's refusal at :925,
     `walkable=False`.
  2. A selected obligation's `evidence_policy` not a `str` (after the scope checks) — same refusal, `walkable=True`.
  3. Mixed policies or conditions, or an empty completion condition (:975) — today's text, `walkable=True`.
  4. Any non-`Refused`, non-`StateConflict` exception raised AFTER the three scope checks (the policy step through `_actor_preconditions`;
     `_case_thens`'s own `Refused` stays `walkable=False`): `prepare_request` wraps that tail in one `try` and raises
     `Refused("the check of <case> could not be prepared: <type>: <160 chars>", <door as today>, walkable=True)` from it.
Everything raised before or by the scope checks — gate A current/drift (:919-923), `validate_plan` with a non-policy error, not pinned,
expectation gaps (P20), obligations not in plan, the mapping mismatch, the three scope checks — and every exception raised in
`prepare_for_block` outside `prepare_request` stays `walkable=False`: refused and not walked, `manual_close`, as today.
A walkable refusal makes `prepare_to_file` write `request.json` as `{"unprepared": {"reason", "door", "trace"?, "obligation_ids",
"source_revision"?, "gate_a_decision_ref"?}, "case", "case_version"?, "thens"?, "covers"?}` (each `?` key only when code could read it)
and `prepare_for_block` returns `(ids_or_[], "", unprepared_reason)` — a 3-tuple; the signature change is owned by N5 with all callers
(`Driver.manual_prepare`, the `story_step` manual block). `run_manual_block` / `manual_plan` put an unprepared case INTO the block;
the role prompt line for it says `<case>: unprepared - <reason>; walk it yourself with the recorder (manual_capture.py) or the
browser, record what you observe, and write a finding; record no pass or fail`. `agents/qa-runner.md` (Tools) gets one paragraph:
how an unprepared case is walked and recorded (craft, P26/P27): `write-block` with `unprepared` copied from the case's `request.json`,
`observations` (every doubtful place on the way), `evidence_refs` it could record, a finding path, no `result`, no `then_quotes`.
(d) **The record and its classification** (blocker 1; Forks 7/8 reshaped). An unprepared record is a `manual-blocks` record with
`unprepared: {"reason": ...}` (equal to the case's `request.json` `unprepared.reason`), `observations`, optional `evidence_refs`,
`finding`, the shared `dispatch_id` / attempt timestamps / `source_revision`, and NO `result`.
- `coverage_contract.validate_manual_current(task, record)`: a record carrying `unprepared` takes an early branch that checks only
  (i) the case's `request.json` holds `unprepared` with the same `reason` (else `"unprepared marker without an unprepared request"`),
  (ii) `result` and `then_quotes` are absent (else `"an unprepared walk records no result: its observations go to the analyst"`),
  (iii) `obligation_ids` equal the request's `unprepared.obligation_ids`; it returns `[UNPREPARED] + <those errors>`, where
  `UNPREPARED = "unprepared walk: no result is bound"` is a constant of `coverage_contract`, and helper
  `coverage_contract.unprepared_only(issues) -> bool` is True exactly when `issues == [UNPREPARED]`. INVARIANT: an unprepared record
  NEVER yields `[]`, so every existing filter `not validate_manual_current(r)` keeps excluding it from results.
- `manual_evidence.write_block`: accepts a record whose issues are `unprepared_only` (drops the constant, keeps any other issue);
  the quote rule is skipped for it (no result). One reader `manual_evidence.unprepared_rows(report) -> list[{case, obligation_ids,
  reason, observations, finding}]` reads `current_manual_checks` rows carrying `unprepared` (AR-13).
(e) **The four readers, each under its own name** (AR-27):
  1. `finalize_task.py` (the manual reduction :535-560): `unprepared_only(issues)` -> `latest = dict(latest, evidence_validated=False,
     unprepared=<the record's unprepared>)` with NO `result` key (the stale/ambiguous branch :548 does not add `result` to an unprepared
     record; it keeps `current_reason`). Other issues -> today's `inconclusive`.
  2. `coverage_contract.py` (projection :568-610): the manual rows of an obligation are split into result rows and unprepared rows;
     `execution` is computed on result rows only (unprepared only -> `not_run`); the item gains `"unprepared": "<reason>"` and, when not
     verified and no awaiting/person_debt gap applies, `gap = "not checked by hand: unprepared - <reason>"`. `verified` stays False.
  3. `ledger.py` (:1245-1270): the export filter is unchanged (no evidence of an unprepared walk is exported as proof); `ledger.json`
     gains `"unprepared_walks": manual_evidence.unprepared_rows(report)`. Its reader: `check_delivery` — a new producer
     `unprepared_records(ledger) -> [{"kind": "unprepared_walk", "case", "ref": case, "requirements": <covers>, "to_check": <reason>,
     "source": "ledger"}]` fed into `build_left_items` where `handed_records` is gathered; data row in `delivery-verdict-kinds.json`
     `kinds`: `"unprepared_walk": {"verdict": "after_checks", "owner": "factory"}` (the builder confirms `_shape_problem` accepts the
     pair; if not, it stops and reports — the owner word `factory` is not swapped, AR-27). The report lists the case under
     "unprepared walks" in Left with you; the scribe words it (code checks the item is there, as for every left item).
  4. `delivery_manifest.py` (:80-82): code unchanged — its filter drops the record by the constant, `export_records` of the same
     filtered list equals the index, so nothing is raised and no unprepared evidence ships as proof. It carries no new key: the
     manifest lists shipped files, and an unprepared walk ships no proof; its name travels through the ledger and the report (reason
     written here so the Lead can overturn). Test pins the behaviour.
  S7: `contract.triage_targets` treats a `current_manual_checks` row carrying `unprepared` as a target with its observations; in
  `s7_pretriage._why_not` such a row returns `"an unprepared walk: whether what it observed is a bug is the analyst's call (P26)"` — code
  never decides it (FR-22: the analyst may raise a bug from a quoted observation).

### F5.3 Edges
- E5.1 `evidence_policy` absent / `""` / `None` / list / dict / int / `"UI"` / `" ui "` -> (a) refuses all but the exact lowercase word
  after `strip()` (C6: strip yes, case-fold no; `planning_contract.py:2338` already strips). INVARIANT: no non-word reaches `POLICIES`.
- E5.2 Mixed policies in one case -> walkable (item 3) after all story-owned checks passed. INVARIANT: same as E5.6.
- E5.3 (blocker 2, rewritten) An approved OLD plan (written before (a)) with a dict policy reaches S6. `validate_plan` at :925 now
  returns the policy shape errors for every such row -> item 1: the case's own story-owned checks still run (pinned, expectation gaps,
  scope, oracle), and only then is the case walked unprepared. If `validate_plan` returns any OTHER error, every manual case of the plan
  is refused as today ("the approved plan does not pass its own checks"), not walked. A plan that drifted from gate A's hash (a hand edit
  after approval) is refused at :919, not walked. At the S3 exit, a NEW plan with a dict is refused by (a). arm B is the old-plan world.
- E5.4 All cases of a block unprepared -> the block is still dispatched (no case dropped).
- E5.5 The recorder fails too (stand down, login refused) -> the runner writes the unprepared record with the observation of that
  failure. INVARIANT: never a blocker, never a `pass` or `fail` from an unprepared walk (FR-59).
- E5.6 Positional: the walkable split sits AFTER every story-owned check. INVARIANT: a case outside the approved scope, with an
  unresolved oracle, an unconfirmed expectation, an unpinned case or a gate A drift is never walked (P20) — the reversal covers only the
  factory's own preparation failures.
- E5.7 Delivery: an unprepared walk never proves a requirement (coverage `verified` False). Fork 13 decides what else the requirement
  shows; the case is always a Left with you item of kind `unprepared_walk`.
- E5.8 A runner writes `unprepared` on a PREPARED case (to escape the quote rule) -> `validate_manual_current` refuses: no unprepared
  request. INVARIANT: the marker is honoured only where code wrote it.
- E5.9 An unprepared record carrying `result` -> `write_block` refuses (`an unprepared walk records no result`). INVARIANT: no pass/fail
  without a prepared request and its quote rule.
- E5.10 `obligation_ids` could not be computed (mapping crashed: `ids = []`) -> NOT walkable (the obligations check refuses first,
  `walkable=False`). INVARIANT: an unprepared walk always has its obligation ids, so coverage can attach it.
- E5.11 Temporal: request files written before N5 hold `refused` -> read as today (`request_actors`, report); only new preparations write
  `unprepared`. Records written before N5 never carry `unprepared` -> every reader behaves as today.

### F5.4 Tests
`scripts/tests/test_manual_evidence.py`: `test_dict_policy_walkable_after_story_checks`, `test_dict_policy_with_expectation_gap_not_walkable`,
`test_expectation_gap_not_walkable`, `test_gate_a_drift_not_walkable`, `test_unpinned_case_not_walkable`,
`test_other_validate_plan_error_not_walkable`, `test_scope_refusals_not_walkable`, `test_tail_exception_walkable_keeps_trace`,
`test_preparation_failure_writes_unprepared_request`, `test_write_block_accepts_unprepared_record`,
`test_unprepared_record_with_result_refused`, `test_unprepared_marker_without_request_refused`, `test_unprepared_rows_reader`.
The file that judges `validate_obligations` (`grep -l validate_obligations scripts/tests`): `test_manual_agent_policy_must_be_word`,
`test_manual_human_policy_must_be_string`, `test_policy_shape_error_constant_in_message`. The file that judges `validate_manual_current`
(`grep -l validate_manual_current scripts/tests`): `test_unprepared_never_empty_issues`, `test_unprepared_only_helper`,
`test_coverage_unprepared_not_run_with_gap`. `scripts/tests/test_story_step_manual_block.py`: `test_unprepared_case_stays_in_block`,
`test_scope_refused_case_still_refused`. The finalize test file (`grep -l finalize_task scripts/tests`, a fast one):
`test_finalize_carries_unprepared_without_result`. `scripts/tests/test_ledger.py`: `test_ledger_lists_unprepared_walks`.
`scripts/tests/test_check_delivery.py`: `test_unprepared_walk_is_left_item_after_checks`, `test_kind_row_shape_accepted`.
The manifest test file (`grep -l delivery_manifest scripts/tests`): `test_manifest_ignores_unprepared_record`.
`scripts/tests/test_triage_control.py` (or the s7_pretriage file): `test_unprepared_row_is_the_analysts_call`.
`test_story_run_s6.py` gets `test_manual_block_dispatches_unprepared` — SLOW file, CI only.

---

## F6 — rerun of S5-S6 on arm B (procedure, no code; Lead decision B3)

**Why the earlier procedure failed (critic t-1938, measured on a scratch copy).** arm B is CLOSED (gate B decided, S8 done). A words
rework of a closed story is a REOPEN (`controller.py:3288`, `_reopen_stamp` :7223), and the stamp is skipped on a reopen
(`if words_given and not reopen and cause != "ticket_changed"`, :3469): S6-S8 stay `completed`, gate B stays `approved`, TC_014-016
never re-enter S6. The S6 manual half cannot be reworked directly ("no accepted qa-runner dispatch on S6 to rework (manual half)"):
those cases were never dispatched. The S5 window TC_001/002 is cap-refused without `--cause` ("round pass 3 ... the cap is 2");
`reviewer_error` does not spend the cap (`--cause` help: only `test_defect` spends it, :8875-8877) and matches the facts (the critic's
rejections named no typed finding). `--words-file` is read relative to the cwd (measured) — absolute paths only. A second words rework on
the reopened story DOES stamp (measured: S4 build-only on the reopened copy gave `rerun_after` stages S5-S8), but the controller refuses
it while the first rework dispatch is running ("sequential task already has an active dispatch").
**Smallest sequence that reaches S6** (S6 cannot be reworked directly, so a stamped rework of the stage before it is the vehicle; S5 is
the latest stage whose stamp lowers S6 and does NOT stale gate A — `_is_decision_after`: gate A only for S4 or earlier, :3640):
reopen with an S5 words rework, release that dispatch, then the same S5 words rework again — now on an open story, so it carries
`rerun_after = {stages: [S6, S7, S8], reviews: <the S5 critic dispatches over the cases>, decisions: [gateB-LOCAL-1]}` (`_rerun_stamp`
:3593: stages after S5 up to S8 that are completed; gate B for a stage <= S8).

Names used below (absolute; no cwd change):
`PKG = D:/ws1/exp-thinking-roles\pkg-b\ai-packages\qa-factory` (moved to the batch head H);
`PROJ = D:/ws1/mybooks-stand\tr-arm-b`; `TR = D:/ws1/mybooks-stand\tr-arm-b\qa-factory\artifacts\LOCAL-1`.
Every flag below exists at c75ec3789: `controller.py` `--task-root`, `--operation`, `--input`, `--stage`, `--role`, `--cases`,
`--words-file`, `--cause` (choices `REPAIR_CAUSES`), `--build-only`, `--brief`, `--dispatch` (:8814-8888; `release` reads
`--words-file` through `person_words.read`, :8899-8901, :8944-8945); `story_run.py` `--task`, `--project`, `--until {gate_A,gate_B,end}`,
`--dry-run`, `--answer` (:17803-17827). `stage-scope` reads its stage from `--input` JSON (`options.get("stage")`, :8934-8939), NOT
from `--stage` — the critic's run with `--stage S5` printed S5 ids for a reason not established here; use `--input`.

**Preconditions.** N1-N5 merged, CI green on the branch head H; `pkg-b` worktree at H (the notebook records H as the package boundary);
the driver of arm B is NOT running (no `story_run.py` process for `PROJ`).

**Words files** (the person's words; English; written by the Lead with the Write tool; copies under
`experiments/mybooks/thinking-roles/answers/`):
- `TR\state\words\rerun-s5-s6.txt`:
  "Rerun after the factory fix batch. S5: write the tests of TC_001 and TC_002 again; the critic's earlier rejections named no typed
  finding, so treat them as unreviewed. Then S6 again: the manual-agent cases TC_014, TC_015 and TC_016 were never walked because their
  preparation failed; walk each of them this time. Gate A stays as approved."
  (Fork 12-B: name the three debt windows TC_001, TC_002, TC_006, TC_013, TC_017, TC_018 instead.)
- `TR\state\words\release-vehicle.txt`: "Release this rework: it only reopened the story. The same rework is started again at once so
  that S6 to S8 run again."
- `TR\state\words\scope-s5.json`: `{"stage": "S5"}`; `TR\state\words\scope-s6-manual.json`: `{"stage": "S6", "execution_kind": "manual"}`.

**Step 0 — dry run on a scratch copy (mandatory, the Lead).** Copy `PROJ` whole into the session scratchpad (the critic's recipe,
t-1938 §T: the tree plus `qa-factory/config.json` under the copy root, `CLAUDE_PROJECT_DIR` pointing at the copy) and run steps 1-5 on
the copy with every path replaced; NO driver run on the copy. Proceed to the live tree only when every expected output below matched;
a mismatch -> stop, record the output in the notebook, and the Lead re-plans (the expected outputs are read from code, not measured).
1. Ids (freshness): `python -B PKG\scripts\controller.py --task-root TR --operation stage-scope --input TR\state\words\scope-s5.json`
   and the same with `scope-s6-manual.json`. Expected: `"stage": "S5"` with ids in the form `LOCAL-1_TC_0NN` (the critic measured 20);
   the S6 manual list holds `LOCAL-1_TC_014`, `_015`, `_016`. Use the ids exactly as printed below.
2. Reopen: `python -B PKG\scripts\controller.py --task-root TR --operation rework --stage S5 --role qa-automator
   --cases LOCAL-1_TC_001,LOCAL-1_TC_002 --cause reviewer_error --words-file TR\state\words\rerun-s5-s6.txt --brief`.
   Expected: `dispatched: true`, `request.reopened_at` set, NO `rerun_after`; note the dispatch id `D1` (critic: `S5-qa-automator-14`).
3. Release the vehicle: `python -B PKG\scripts\controller.py --task-root TR --operation release --dispatch D1
   --words-file TR\state\words\release-vehicle.txt`. Expected: `released: true`, `status: released` (`release_dispatch` :7278; `running`
   is releasable; the story is already open, so no second reopen stamp). A released never-accepted rework of a completed stage is not
   relaunched by `next` (`relaunch_shape` :1152-1165 — confirm on the copy with `--operation next`).
4. Stamped rework: the step-2 command again (same cases, same cause, same words file). Expected: `dispatched: true`, new id `D2`,
   `request.rerun_after == {"stages": ["S6","S7","S8"], "reviews": [<S5 qa-code-critic dispatches over TC_001/002>], "decisions":
   ["gateB-LOCAL-1"]}`; gate A is not in `decisions`. If `rerun_after` is absent (S5's status is not `completed` after steps 2-3 —
   `_rerun_stamp` :3608-3614 stamps only a completed stage or a pending one with an accepted stamped rework), STOP: the sequence does
   not reach S6 and the Lead re-plans.
5. Witness before the driver: `python -B PKG\scripts\controller.py --task-root TR --operation next`. Expected: S6, S7, S8 `pending`;
   `gateB-LOCAL-1` stale (not `approved`); `gateA-LOCAL-1` `approved`; S9 `completed` (Fork 9-A); the next action is `D2`. The output
   goes VERBATIM into the notebook as the rerun's entry witness.
6. Driver dry run (live tree only): `python -B PKG\scripts\story_run.py --task LOCAL-1 --project PROJ --until end --dry-run` — expected:
   the first action runs `D2`.
7. Run: `python -B PKG\scripts\story_run.py --task LOCAL-1 --project PROJ --until end` in the background, its log beside the earlier
   `arm-b-*.log` (`experiments/mybooks/thinking-roles/runs/`).

**What the person will be asked, and the prepared answers** (each answer a file passed with
`story_run.py --task LOCAL-1 --project PROJ --answer <absolute file>`):
- S5, if the code critic again sends TC_001/002 back with no typed finding: the closed question `s5.nobody_review` (after N2) — answer
  `review` the first time, `debt` the second.
- S5, a send-back WITH typed findings within the cap: no question (a round runs).
- S6: no question for TC_014-016 (unprepared walks are Left with you items, never a stop). If `request.json` of a case shows a
  NON-walkable refusal (a story-owned reason), that is the honest outcome — no answer; the Lead records it.
- Gate B (stale, asked again): the words of `experiments/mybooks/thinking-roles/answers/gate-b-run-b.md` with the draft numbers of the
  NEW packet: "file <every draft number> as drafts in the project's markdown only (this is a comparison run, nothing leaves the project)"
  and "delivery-1: deliver with known gaps" (P8).
- Any conductor question: answered in the person's plain words, in a file, through `--answer`.

**What goes stale / stays.** S5: the reviews over TC_001/002 stale, the window reworked by `D2`, then the code critic reviews it again
(F1/F4 on a live round). S6, S7, S8: `pending`, rerun whole — the S6 automated half runs again too, and the manual block calls
`prepare_for_block` again (the old `request.json` with `refused` is rewritten; under N5 TS-14/15/16's dict gives an unprepared walk if
their story-owned checks pass — the door under test, Fork 10-A). Gate B: stale, asked again. Gate A: approved, unchanged. S9 and the
first pass's `retro.md`: unchanged (Fork 9-A). The prepared road of the X8 recorder is NOT exercised in this rerun (Lead decision B2):
it is proven by N5's unit tests now and by the next full run.

**Expected cost and time (estimate, not verified; carriers: notebook line 115 — first-pass S5 $14.40 over 7 windows, S6 $1.03,
S7 $1.37, S8 $0.42).** S5 one window (Fork 12-A): ~$2-4, ~1 h (the Lead's figure ~3 h serial for three windows, divided by three);
Fork 12-B three windows: ~$6-10, ~3 h. S6 whole with three unprepared walks: above the first pass's $1.03 (no manual walk ran then) —
~$2-4, ~1 h. S7 + S8 + gate B: ~$2, ~0.5 h. Total 12-A ≈ $6-10 and ~2.5-3 h; 12-B ≈ $10-16 and ~4.5-5 h. "S6 only" is not available:
the manual half has no accepted dispatch to rework (measured), so S5 is the cheapest vehicle.

---

## Forks (numbered; each with a recommendation — the Lead decides)

1. **F1(b) which lists are emptied in the skeleton.** Decided A (only `questions` and `findings`).
2. **S5 author path.** Decided B (S5 not filled; both S5 contracts keep their token).
3. **`args` on a move whose column is null.** Decided B (drop + `args_dropped`) and NO (a person's words never in `args`).
4. **Tokens for the `—` moves.** Decided (critic round 1): all three non-offerable, no new tokens.
5. **`go on` over a readable last-round REJECT at the stage-critic seam.** Decided A, bound to a word recorded after the critic dispatch.
6. **What satisfies owed `findings` rows on a send-back.** Decided A.
7. **Outcome of an unprepared walk.** Decided (critic round 1): no result word at all; `unprepared` marker, observations to S7, Left with
   you item `unprepared_walk`.
8. **Evidence of an unprepared walk.** Decided (critic round 1): no pass/fail; whether an observation is a bug is the analyst's call.
9. **S9 after the rerun.** Decided A.
10. **Prepared road in the rerun.** Decided plain A (critic round 1): no hand repair.
11. **F2(a) re-ask.** Decided A.
12. **(new) S5 scope of the rerun vehicle.** (A) one window TC_001/002 — the minimum that reaches S6, and still a live S5 critic round
    over a window whose earlier rejections were untyped (tests F1/F4 once); (B) the three debt windows TC_001/002, TC_006/013,
    TC_017/018 — the owner's 11:23 word "перегнать S5–S6" read as the whole S5 debt, +~2 h and ~$6. Recommend A (the Lead's preference:
    rework only what is needed to reach S6); B if the owner wants the S5 comparison redone.
13. **(new) Delivery verdict of a requirement whose only check was an unprepared walk.** (A) keep today's trace road: the requirement
    stays without a terminal outcome (its existing kind, usually `no`), and the case is ALSO a Left with you item `unprepared_walk`
    (after_checks); (B) a new trace gap `unresolved:unprepared_walk` -> `unprepared_walk`, so the walk alone yields `after_checks`
    (+ `traceability.py` and its `unresolved[]` producer in N5's owns). Recommend A: the factory's own failure is never softened into a
    pass-like verdict (AR-28, FR-59); the analyst may still raise a bug at S7.

## Small choices closed by the designer (no design weight)
- C1 One author token `<the author's dispatch>` across the S2/S3/S4 contracts (AR-15); the S5 tokens unchanged (Fork 2-B).
- C2 `person_pass` helper extracted from `consumer_person_pass` rather than a second copy (AR-15).
- C3 The trace in `request.json` is the last 20 lines of `traceback.format_exc()`.
- C4 `rows_owed_when` as a new contract key beside `required_when` (not a reuse of `required_when`, whose list semantics would make S2-S4
  `concerns` critics owe a question).
- C5 `manual-human` policy: non-empty string, no membership.
- C6 `evidence_policy` is stripped, not case-folded.
- C7 `Refused.walkable` defaults to False (the positive list opts in; a forgotten site stays on today's safe side).
- C8 The attestation note for the pre-filled `inputs_read[0]` is a skeleton comment written by `handoff_init` (N1's file), not a brief
  line (the brief writer is not N1's).

## Nodes and owns (disjoint; `story_run.py` and `story_step.py` split by function, D-0048)

All paths under the builder's worktree `<wt>\ai-packages\qa-factory\`. Hot file `story_run.py`: each node owns only the functions
listed; the later-merging node merges `main` of the branch and resolves; ONE critic pass after the merges (R13-g).

- **N1 (F1)** — owns: `scripts/handoff_init.py`; `scripts/story_step.py (_handoff_form)`; `scripts/stage_done.py (record_acceptance)`;
  `scripts/story_run.py (run_role)`; `scripts/question_register.py (the --from-handoff row reader)`;
  `handoffs/s2-stage-critic-to-tester.yaml`, `handoffs/s3-stage-critic-to-strategist.yaml`, `handoffs/s4-case-critic-to-designer.yaml`
  (author token lines only); tests `test_handoff_init_author.py` (new), `test_rework_dispatch_files.py` (new), the record_acceptance
  test file, `test_question_register.py`, `test_handoff.py` (only if the contract edit moves its pins). Does NOT touch either S5 contract.
- **N2 (F4)** — owns: `handoffs/s5-critic-to-automator.yaml` (the new `rows_owed_when` block only; producer with its reader, major 10);
  `scripts/handoff.py (rows_owed)`; `scripts/handoff_check.py (check)`; `scripts/repair_route.py`;
  `scripts/story_run.py (repair_limit_gate, repair_limit_facts, s7_reorder_outcome)`; `agents/qa-code-critic.md`; tests
  `test_repair_route.py`, `test_rows_owed.py` (new), the charter-pin test file, the S7 file judging `s7_reorder_outcome` (CI if SLOW).
- **N3 (F2)** — owns: `scripts/no_move.py`; `references/conductor-actions.json`; `references/conductor.md`;
  `scripts/story_run.py (_no_move, fallback_person, gate_fallback_question)`; tests `test_no_move_seam.py`, `test_conductor_doors.py`.
- **N4 (F3)** — owns: `scripts/story_run.py (stage_review_exhausted, consumer_person_pass, person_pass [new])`; test
  `test_stage_review_person_pass.py` (new); the F3.4 sweep table in its report.
- **N5 (F5)** — owns: `scripts/manual_evidence.py (Refused, prepare_request, prepare_to_file, prepare_for_block, write_block,
  unprepared_rows [new])`; `scripts/coverage_contract.py (validate_obligations, POLICY_SHAPE_ERROR, validate_manual_current, UNPREPARED,
  unprepared_only, coverage_projection manual branch)`; `scripts/finalize_task.py (the manual reduction ~535-560)`;
  `scripts/ledger.py (the ledger document builder ~1245-1270)`; `scripts/check_delivery.py (unprepared_records [new], its wiring into
  build_left_items)`; `references/delivery-verdict-kinds.json (the unprepared_walk row)`; `scripts/contract.py (triage_targets)`;
  `scripts/s7_pretriage.py (_why_not)`; `scripts/story_step.py (the S6 manual block check, ~950-992, and its callers of
  prepare_for_block)`; `scripts/story_run.py (run_manual_block, manual_plan, manual_prepare)`; `agents/qa-runner.md`;
  `references/slices/qa-test-strategist/artifact-contract-plan.md`; `references/coverage-design.md`; tests: `test_manual_evidence.py`,
  `test_story_step_manual_block.py`, the validate_obligations / validate_manual_current / finalize / manifest test files (found by the
  greps in F5.4), `test_ledger.py`, `test_check_delivery.py`, the s7_pretriage test file, `test_story_run_s6.py` (CI). The largest node:
  if its worker reaches the WARN line (host adaptation 6), the remainder (readers 1-4 + S7) goes to a fresh worker whole, same node.
- Shared: `scripts/tests/fixtures/judgment-census.json` — each node adds only its own rows (different `file` keys); the later merge
  resolves. `changelog.d/` — one fragment per node (`t-1936-n<k>.md`).
- Parallel writers: 5 (cap 6). Push before worktree launch (`tools/dispatch_gate.py`).

## Witness per node (narrowed, builder-rules 7b; under a minute each; SLOW files to CI)

Command form (from the worktree root, absolute paths): `python -B -m pytest <abs test file> [<abs test file> ...] -q`.
- N1: `test_handoff_init_author.py`, `test_rework_dispatch_files.py`, the record_acceptance test file, `test_question_register.py`
  (+ `test_handoff.py` if pins moved); plus `python -B scripts/selftest.py --lang` (FR-30).
- N2: `test_repair_route.py`, `test_rows_owed.py`, the charter-pin test file, `test_judgment_census.py`; the `s7_reorder_outcome` file
  only if it is not SLOW.
- N3: `test_no_move_seam.py`, `test_conductor_doors.py`, `test_judgment_census.py`.
- N4: `test_stage_review_person_pass.py`, `test_judgment_census.py`.
- N5: `test_manual_evidence.py`, `test_story_step_manual_block.py`, the validate_obligations / validate_manual_current / finalize /
  manifest test files, `test_ledger.py`, `test_check_delivery.py`, the s7_pretriage test file, `test_judgment_census.py`, plus
  `python -B scripts/selftest.py --lang`. `test_story_run_s6.py` is never run locally (SLOW) — CI.
Each node's DoD also states its AR change check in the commit: the `architecture:` and `judgment:` lines below.
BATCH CANON: the CI pipeline on the branch after the merges (D-0059), not local.

## AR/FR walk (per node; `architecture:` line for the commit)

- N1: `architecture: AR-8, AR-10, AR-14, AR-15, AR-23 -- code fills the S2-S4 author path the driver knows and tells the critic it may
  change it; one skeleton writer for start and rework; empty optional lists are [] with the sample in comments`. FR: A FR-1; C FR-15,
  FR-38, FR-11; B — text shown to a person unchanged; D/E/F — not touched; G FR-30.
- N2: `architecture: AR-10, AR-15, AR-19, AR-28, AR-29 -- the owed findings row is a presence check told in the field and the charter;
  an untyped send-back goes to the existing closed site question at S5 and stops the round at S7, never to an assumed cause`. FR-1,
  FR-38, FR-47, FR-59; B — the person sees the existing `s5.nobody_review` form with a new opening (AR-16).
- N3: `architecture: AR-1, AR-9, AR-16, AR-17, AR-24, AR-25 -- which move takes args and which is never an option is data; the
  conductor's question reaches the person even when its options are refused`. FR-9, FR-10, FR-13, FR-38, FR-42.
- N4: `architecture: AR-13, AR-24, AR-25 -- the person's word at the stage-critic seam is read through split_overridden, honoured only
  when given after the critic dispatch, and closes the stage with a finding`. FR-4, FR-8, FR-9; FR-12 n/a (F3.2 step 5).
- N5: `architecture: AR-2, AR-10, AR-13, AR-17, AR-22, AR-23, AR-27, AR-28 -- a malformed plan row is refused by shape at S3 exit; at S6
  only the factory's own preparation failures become an unprepared walk by the role, never a dropped case, never a result, and the walk
  reaches S7 and Left with you under its own name`. FR-1, FR-4, FR-18, FR-19, FR-38, FR-41, FR-46, FR-59; P20, P21, P22, P26.

## Census rows (`scripts/tests/fixtures/judgment-census.json`, row shape `{file, function, class, roles, owner}`; words per minor 16)

- N2: `{"file": "handoff_check.py", "function": "<the new rows-owed block>", "class": "shape", "roles": ["qa-code-critic"], "owner":
  "data"}`; `{"file": "handoff.py", "function": "rows_owed", "class": "shape", "roles": ["qa-code-critic"], "owner": "data"}`;
  `repair_route.py :: route` — existing row (if any) keeps its class; if none, `{"class": "shape", "roles": ["qa-code-critic"],
  "owner": "data"}`.
- N3: `no_move.py :: validate_options` — existing row expected (class shape, roles conductor); the builder confirms.
- N4: `{"file": "story_run.py", "function": "person_pass", "class": "xref", "roles": ["conductor"], "owner": "intent"}`.
- N5: `coverage_contract.py :: validate_obligations` — existing row (shape, roles `["conductor"]`) kept as is;
  `{"file": "manual_evidence.py", "function": "prepare_request", "class": "shape", "roles": ["conductor"], "owner": "data"}` (new);
  `{"file": "coverage_contract.py", "function": "validate_manual_current", ...}` — existing row kept if present, else `shape`,
  roles `["qa-runner"]`, owner data; `{"file": "manual_evidence.py", "function": "write_block", ...}` — same rule.
- N1: no new check (text of an existing refusal; a skeleton writer is not a check).
`judgment:` commit line per node: `judgment: <rows added> -- data/shape|xref; no role content is judged`.

## Deferred
B-9, B-12, B-13 (not this batch). B-4 and B-8 — not in the brief's five classes; named so they are not lost. Queued to findings files
of the batch's pile with a row in the open batch (PROJECT.md «Командная работа» п.2): the F1.4 reader-table remainder; the F3.4 sweep
lines marked "deferred"; S6/S7 consumer contracts onto the author token (AR-15, critic §6); Fork 13-B if the owner chooses it later.

## Reading trail
Round 0 (designer): the scout digest t-1934 (whole); notebook 55-120; `PKG\references\conductor-actions.json`, `conductor.md`;
`no_move.py` 1-479; `repair_route.py`; `story_run.py` 2787-2885, 3129-3190, 5000-5450, 9290-9350, 9500-9610, 10540-10893, 12076-12165,
2470-2510; `stage_done.py` 855-979; `handoff_init.py` 30-150, 300-391; `story_step.py` 300-349, 960-999, 1078-1137; `handoff_check.py`
969-988, 1388-1477, 2219-2308; `handoff.py`/`waiver.py`/`acceptance.py` greps; `controller.py` 2080-2094, 5330-5349; `manual_evidence.py`
835-864, 955-994, 1090-1134; `coverage_contract.py` 395-419; `planning_contract.py` 2305-2369; `coverage-design.md` 150-163; the
critic contracts; census first rows.
Round 1 (this fix designer): the spec (whole); critic review t-1938 (whole); scout digest t-1934 1-30; `controller.py` 1147-1196,
3255-3480, 3498-3670, 5705-5724, 6908-6917, 7215-7240, 7278-7327, 8814-8993, greps (`reopen_story`, `_rerun_stamp`, flags,
`dispatched_seq`, active-dispatch refusal), 1488-1497; `story_run.py` 10776-10900, 12945-12989, argparse 17803-17827, greps
(`stage_review_exhausted`, `consumer_person_pass`, `owe_row`, `nobody_review`); `manual_evidence.py` 755-1186; `coverage_contract.py`
560-710; `ledger.py` 1225-1270; `delivery_manifest.py` 60-104; `finalize_task.py` 535-574; `s7_pretriage.py` 136-180;
`check_delivery.py` 1770-1810, 2018-2077, greps (`left_items`, kinds); `delivery_verdict.py` 84-123; `delivery-verdict-kinds.json`
grep; `waiver.py` grep (`at`, `split_overridden`); `traceability.py` grep; notebook 100-121; `answers/gate-b-run-b.md`.
Not verified by measurement (the designer has no shell): every "Expected" line of F6 steps 1-6 is read from code — step 0's dry run on
a scratch copy is what measures them. The `--stage` vs `--input` discrepancy of `stage-scope` with the critic's measured run is
unresolved; F6 uses `--input`. Negative claims with controls (round 0): `agents/qa-conductor*` none (control: 12 role files);
`author_dispatch` absent in story_step.py (control: `_handoff_form` found); manual_capture.py does not read `request.json` (control:
`refused` found). Round 1 negative: a dispatch record holds no creation-time field (grep `"dispatched_at"|"started_at":` 0 hits;
positive control in the same file: `dispatched_seq` and `created_at` found) — hence `_dispatch_starts`.
