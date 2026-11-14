# FV1-9 — a question asked once: repeats settled or merged, re-asking in clearer words, a card that helps (designer draft, rev. 1)

Tree read: `C:\QAFactory\forge-repo\.claude\worktrees\sc-a1a\ai-packages\qa-factory` (origin/main 14.11.2026); paths below are relative
to it unless absolute. Run logs: `experiments/mybooks/factory-vs-free-agent/runs/factory-{6,7}.log` (forge root, gitignored).
Status: DRAFT for Lead acceptance; forks in §7 (OWNER's: F-4, F-6; the rest Lead's). Critic on plan is MANDATORY before any builder:
F-3 changes what a gate accepts (PROJECT.md «Как принимается изменение пакета» п. 6) and this is a new idea of the owner (step 6).
Supersedes FV1-3 spec §5 (hint lines by shared `where`, `--withdraw`) where it contradicts the owner's words; its facts are kept.

## §0. The owner's words (verbatim, from `docs/tasks/specs/20261113-fv1-3-free-answer-to-conductor-spec.md:626-653`)

13.11.2026, F-7: «роль сама может ответить на этот  вопрос, раз есть ответ на уже заданный. Если ответа нет, то показываем человеку»
14.11.2026, F-7: «вопрос на который не ответили можно задать ещё раз в другой, более понятный формулировке, но два одинаковых вопроса в
один момент конечно не надо задавать»
14.11.2026, F-8: «надо не просто сказать что не так с вопросом, а что-то что поможет человеку на вопрос ответить»

| R | requirement (the Lead's reading of the words) | mechanism (§3) | the row that proves the code part (§5) |
|---|---|---|---|
| R1 | a repeat of an ANSWERED question is settled by the role from that answer | D1 the register's questions in every brief (answered ones WITH their question text); D2 craft lines: cite `person: Qn`, raise nothing; `person` accepted only on an answer that still holds; D3 net: a declared repeat of an answered row reads "Qn's answer is its answer" | N3 `fv19_brief_lists_question_text`, `fv19_person_needs_holding_answer`; N1 `fv19_repeat_of_settled_listed_for_brief` |
| R2 | two questions asking the same thing are never shown at one moment | D1 open rows listed in every brief; D2 point at the open id; F-3 lets a Then point at an S2 reading question; D3 status `repeat`: a declared repeat is hidden while its target exists, the target's card says it was raised again; the report lists the target once | N1 `fv19_repeat_hidden_while_target_resolves`; N2 `fv19_target_card_says_also_raised`, `fv19_report_lists_target_once` |
| R3 | an unanswered question MAY be asked again later in clearer words | D4 one door `--reword` on an open row with no holding answer: id kept, `reworded[]` kept on the row, the card says it is the same question asked again | N1 `fv19_reword_keeps_id`, `fv19_reword_refused_on_answer`; N2 `fv19_card_says_asked_again` |
| R4 | a question the rehearsal flagged and nobody reworked is shown WITH what helps answer it | D5 card help by fields (H1-H7), the conductor's `note` on the cap's refusal, `(from ?)` gone, the FR-41 line when nothing helps; the gate's top never prints the defect line to the person | N1 `fv19_note_bound_to_bytes`; N2 `fv19_card_help_fields`, `fv19_card_no_help_line`, `fv19_gate_top_no_defect_line` |

Code proves the data; that a role now looks before raising is a role behaviour, proved only by a live run (FR-33): one row for
`live-runs` (the LOCAL-1 pack: no S4 question repeating Q1-Q3; a flagged S2 question shown with help).

## §1. Package header (designer rule 1; CLAUDE.md rule 10; P27, AR-29)

### 1.1 AR-n touched, how each is kept (the change check is written into the node DoDs)
- AR-1 — `repeat` is a row of `references/question-vocabulary.json` `statuses`/`recorded_statuses`; the person's words for a reading's
  origin are a data row `reading_origin_words` (read by `question_register.origin_words`, default for an unknown word). Check: grep
  `scripts/` for a literal `"repeat"` status outside `question_register.py` readers (N1 DoD).
- AR-2, AR-7, AR-29 — whether two questions ask the same thing is the ROLE's judgment (designer looks; case critic finds; designer or
  conductor declares; the person sees the merge on the card). Code never compares two questions (no `_shown`, no `where` join, no text
  match; `meaning-proxy: 8` in `judgment-census.json` unchanged). Check: census run; no new word-list/meaning-proxy/meaning unit.
- AR-10 — what the role must look at (the asked questions) reaches it in the brief BEFORE the work, and what code checks of a
  `question_repeats` entry is stated in the contract and the charter in the same commit (N3).
- AR-13 — one reader per fact: shown/not shown is `QR.is_open` only; the brief list is `QR.asked_for_brief` only; a repeat's target is
  resolved once in `QR._resolve_repeats`, called by `load` and `statuses_for`. Check: grep `status") == "repeat"` outside the register.
- AR-14 — `work/requirements-readiness.json`: the S2 tester + the register's own writer `_write_readiness` (raised rows today; `reword`
  adds one caller); `work/question-answers.jsonl`: only `_append` (records `repeat`, `note`). The conductor writes neither file directly.
- AR-16 — every new person-facing line is a card line of `gate_brief.question_card` (the one form; `human_text.problems` passes).
- AR-17 — the cap's refusal reaches the conductor through the existing `hand_to_conductor` -> `conductor_round` seam; no new seam.
- AR-20 — judgment-census rows added for new units; any raised count named in the verdict.
- AR-22 — every new field has producer and reader in one node: `same_as`/`declared_by` (record -> `_resolve_repeats`), `follows`/
  `repeated_by` (`_resolve_repeats` -> `is_open`, card, `still_open`, report, brief), `reworded[]` (`reword` -> card), `note` records
  (`record_note` -> `_merge` -> card), `question` extra on the finding (`check_open_questions` -> `unrepaired_text`).
- AR-23 — empty outcomes declared: empty register -> the brief says none asked; no help data -> the FR-41 card line.
- AR-24 — a person's answer to a hidden repeat is recorded and wins (last record); nothing drops their words.
- AR-25 — `repeat` has a way out (`--reopen`, or the person's answer; an unresolved target makes it open again); a `design/state-exits.md`
  row in N1. A reword keeps `was`; a later note supersedes an earlier one.
- AR-28 — an unresolved repeat (target gone, cycle, row changed since) is OPEN, never hidden.

### 1.2 Checks added or altered: owner served, census class
| check | where | owner | class |
|---|---|---|---|
| `record(status="repeat")`: `same_as` present, an id of the register, not itself, not closing a cycle; the row not settled | `question_register.record` | data | xref |
| hide a repeat only with a resolved, existing target and `changed_since_answer is False` | `question_register.is_open` (altered) | data (the sameness itself: judgment of the declaring role, accepted by the person who sees the merge) | xref |
| `reword`: row open with no holding settled/deferred record; readings count unchanged; result passes `contract.question_errors` | `question_register.reword` | data | shape |
| `record_note`: row exists, words 1..2000 characters, `by` from the vocabulary | `question_register.record_note` | data | shape |
| `question_repeats` entry: both ids in the register, `why` not blank (problem line, never blocking) | `question_register.repeats_for_case` | data | xref |
| `person` oracle: the ref's answer holds (`QR.settled` and status `answered`) — was raw status | `contract.then_oracle_errors` (altered) | data | xref |
| `unknown` oracle: the ref shows before/now OR has >= 2 readings (F-3) — was before/now only | `contract.then_oracle_errors` (altered) | data | xref |
| a raised question that asks what an asked one asks | `agents/qa-case-critic.md` (finding), `agents/qa-case-designer.md` (look first) | judgment, accepted by the critic's round and the person | not code |

### 1.3 SIBLING_MAP axes (one block; each line closes every mechanism M1 brief list, M2 repeat status, M3 reword, M4 help/note, M5 oracle refs)
axis 1: n/a — no policy/role-file/journal change of this deployment. axis 2: n/a — no exam instrument. axis 3: n/a — release copy follows
the package by the release procedure. axis 4: covered — no FR changes; FR-7 read for M3 (§3 D4); no debt line. axis 5: covered — stage
twins: the question stop card and the gate A card are ONE renderer (`question_card`, `open_cards` `question_stop.py:384`), so M2/M3/M4
reach both; `still_open` (gate A) and `is_open` (stop) both get the repeat rule (N1, N2). axis 6: queued — `stage_compare.py` does not
read the register; no measurer change. axis 7: n/a. axis 8: n/a — paths through the existing story root. axis 9-11: n/a. axis 12: covered
— one batch row (FV1-9); the live proof row goes to `live-runs`. axis 13: covered — M1 adds a brief section; FV1-4's "rendered whole"
holds (F-2). axis 14-16: n/a (the register reads its JSON as today). axis 17: n/a — no detector verdict shape. axis 18: covered — census
rows; `meaning-proxy` unchanged. axis 19-28: n/a — no role-file tools line, host receipts, table cells, host forms, test rows, run joins,
freshness, stand words, profiles, row-form sites. axis 29: covered — M2/M4 append through `_append` (the register's appender, as today;
not `hooklib.append_jsonl_line`: queued as an existing twin, not new). axis 30: n/a. axis 31: covered — the look-first rule lives once
per role in its charter (designer, case critic); the contract carries the form only. axis 32: covered — §1.2. axis 33: n/a. axis 34:
covered — one road per action: hiding = `is_open` for every reader; declaring = `record(status="repeat")` with two carriers (designer's
case key, conductor's CLI) exactly as raising has two carriers today (F-7); help = one card renderer for every stage. axis 35-36: n/a.

## §2. Facts (re-read on the tree named above)

- F1 Statuses: `references/question-vocabulary.json:2-3` (open, answered, not_needed, with_designer, named, deferred_to_report); `by`
  `:17`. No `repeat`/`note` (file read whole; positive control: `with_designer` found on the same lines).
- F2 `is_open` `question_register.py:431-443`: False only for `with_designer` and a settled/deferred record that holds; readers:
  `question_stop.open_cards` `:397`, `batch_text` `:489`, `answer_block` `:423`, `answers_for_brief` `:1185`, `open_blocker` `:446`,
  `driver_stage_plan.py:933`. Gate A's list is NOT `is_open`: `gate_brief.still_open` `:4202-4252` skips `QR.settled(mine)` `:4238`.
- F3 `_merge` `:252-284` and `load` `:287-340`: one record per id (the last), `row_hash` = sha256 of the row `:149-156`;
  `_answers` `:159-202` counts any `kind` other than `question`/`case` as `invalid` `:194-196` (a `note` line today would be "set aside").
- F4 `record` `:862-921`: refuses a different answer on a settled row; check-then-append is not one lock span (`load` `:879`, `_append`
  `:814-829` takes `answers_lock` itself) — a race is possible today for every record.
- F5 CLI `_VALUE_OPTIONS` `:1634-1636`: `--answer`, `--not-needed`, `--reopen`, `--defer`, ... `--from-handoff`; no reword/note/repeat
  (read whole; control: `--reopen` present).
- F6 `answers_for_brief` `:1174-1194` already carries `question` per item `:1191`; `brief_pack.question_answer_lines` `:1738-1775`
  does not print it (head `:1752-1760`). Open rows: no brief reader (recon; `decisions` `:1790-1852` reads only answers).
- F7 FV1-4: `brief_pack.build.render` `:4549-4586` "Nothing is measured against a size and nothing is dropped for room"; only a by-range
  note over 30 KB `:4594-4604`. The brief's "brief ceilings are real" describes the run of 12.11 (`factory-7.log:22` "over the 6144 budget
  B ceiling after every cut"), not this tree (§9).
- F8 ROOT CAUSE of the S2/S4 pairs: a Then can point at an existing question only as `person` (answered, `contract.py:1723`) or `unknown`
  (`:1726`), and `unknown` needs the row to carry `before` (`"before" not in questions[ref]` -> refused). S2's reading questions (Q1-Q3,
  `factory-7.log:46-60`: readings, no before/now) can therefore never be the ref of an open S4 Then: the designer MUST raise a
  before/now question (Q10-Q12). Contract text: `references/artifact-contract.md:136-140`.
- F9 `person` checks the raw status (`contract.py:1723`), so an answer whose row changed since (`changed_since_answer` True, status still
  `answered`) is accepted as an oracle. `questions` comes from `validate_artifacts._question_rows` `:272-283` (`QR.load` view).
- F10 The S4 raise step: `critic_rollcall.raise_pending` `:739-779`, skipping a case unless `C.RAISE_REF in content` `:768`; it calls
  `QR.raise_for_case` `:770`; `replaces` repoints a plan row via `planning_contract.repoint_question_ref` (`question_register.py:1461-1462`,
  `planning_contract.py:3033-3039`: by meaning, else append and a note).
- F11 Card `gate_brief.question_card` `:2734-2825`: `status_note` `:2754-2756`; source_says `:2757-2761`; before/now `:2767-2773`;
  `(from {reading.get('from', '?')})` `:2786`, `:2794`; `if chosen` `:2795-2797`; effects `:2798-2806`; the answer line LAST `:2824`.
- F12 Report: `report_facts._questions` `:2600-2621` lists every row not `QR.settled`; `_r_questions` `:3960-3985`.
- F13 Rehearsal: `gate_preflight.check_open_questions` `:1929-2022`: per row not answered/settled, `question_errors`; finding class
  FACTORY_FIXABLE `:2017-2022`, message "`{qid}` cannot be answered as it stands (...) — `qa-requirements-tester` rewrites it ...", fix "the
  question packet goes back to qa-requirements-tester at S2, ...; " + waiver words. `add` keeps `**extra` keys on the finding `:1652-1658`.
- F14 TRACED — the finding after the cap: `driver_gates.gate_repair` `:900-974` -> repair plan has no move for `open_questions` ->
  `gate_stop(reason="no_move")` `:990-993` prints "N thing(s) no code move repairs — the list goes to the conductor" (`factory-7.log:19`)
  -> `hand_to_conductor` `:1001-1014` -> `conductor_round(Refusal(conductor_text(...)))`; `conductor_text` `:791-815` prints each finding's
  message and fix, "Repair what you can ... then answer `continue`". The conductor ran `controller.py rework --stage S2 --role
  qa-requirements-tester`; the controller refused: `controller.py:5638-5662` (test_defect rounds `spent >= cap`, `design_repair_cycles`/
  `repair_cycles` `:5604`), text "... has already had N repair round(s) about the test on this S2 window; the cap is N ... carry what is
  left as a named debt to the gate ...". The conductor answered `continue` (`factory-7.log:20`). The series is recorded stopped; the next
  rehearsal shows the gate with `unrepaired_text` `:698-721` at its TOP — which prints each finding's `message` verbatim, i.e. "Q1 cannot be
  answered as it stands (...) — `qa-requirements-tester` rewrites it ..." to the PERSON. Meanwhile any question stop prints the plain cards
  with `(from ?)` (`factory-7.log:46-60`). Nobody is asked for help; no carrier exists for it.
- F15 `conductor.md` names no register command (case-insensitive grep `question.register` empty; control: `controller.py` found `:31-35`
  in the same file); its table maps situations to commands `:20-35`.
- F16 Roles run no register command (recon; `agents/qa-case-designer.md:65,78`, `agents/qa-case-critic.md:133`). The case critic's
  "Where bugs hide" `:28-36` has no repeat line; stage-critics spec A2 rewrites `:30-32` (§6).
- F17 Tests: keep files `test_question_register.py` (`test-layers.json:4203`), `test_gate_question_form.py` (`:1995`, covers
  `driver_gates.py`, `gate_preflight.py`, `gate_brief.py`), `test_oracle_provenance.py` (`:3503`), `test_brief_pack.py` (`:288`, slow 34.6 s,
  in `keep_fail_at_entry` `:7132`), `test_report_facts.py` (`:4452`, slow 55.6 s). Quarantined (not used): `test_question_stop.py` `:9279`,
  `test_story_run_gate_repair.py` `:10128`, `test_brief_pack_roles.py` `:7295`. `test_question_register.py:1602` pins
  `answers_for_brief` == `{"answers": [], "unreadable": False}` (why D1 adds a new reader instead of a key).

## §3. Design

### D1 — the asked questions reach every brief (R1, R2 prevention; data to the role)
- N1: `QR.asked_for_brief(task_root) -> {"open": [{id, question, repeated_by: [ids]}], "repeats": [{id, same_as, target_settled: bool}],
  "unreadable": bool, "present": bool}` — open = `is_open(q)` in register order; repeats = rows whose `follows` is set. One `load`.
- N3: `brief_pack.question_answer_lines` adds `; the question: "<question, whitespace squeezed, whole>"` after the head (before the
  person's words). New `brief_pack.asked_question_lines(task_root)` renders §3 D6 T1; `render` places the section right after
  "## The person's words that concern you" (POSITIONAL P5). Which briefs: every brief (F-1 (a)). Cut: none (F-2 (a), FV1-4).

### D2 — the craft rule and what code checks (R1, R2)
- Charter lines D6 T12 (designer, "When to ask") and T13 (case critic, "Where bugs hide" + "When to ask"). The role judges sameness.
- Code checks (N3, `contract.then_oracle_errors`): `person` ref -> the ref exists and `QR.settled(q) and q["status"] == "answered"`
  (F9 closed); `unknown` ref -> the ref shows before/now OR has >= 2 readings (F-3 (a)); a ref whose row is a resolved repeat is refused:
  "`{ref}` was marked as the same question as `{target}`: point the Then at `{target}`". `artifact-contract.md:136-140` says the same.

### D3 — status `repeat`: the way out for a repeat already in the register (R2 net; R1 net)
- Declared by (F-7 (a)): the case designer, in the round that repairs the critic's finding, as a case front-matter key
  `question_repeats: [{"question": "Q16", "same_as": "Q7", "why": "<one line>"}]` — executed by the S4 raise step (`raise_pending` ->
  `QR.repeats_for_case`, after `raise_for_case` of the same case), which drops the key once recorded; and the conductor, by CLI
  `question_register.py --task <T> --repeat Q16 --same-as Q7 --words-file <why> --by conductor --where conductor` (role questions it
  settles). Both reach ONE writer: `record(task_root, qid, "repeat", words, where, by, shown_hash, same_as=..., declared_by=...)`; record
  keys `same_as`, `declared_by`; `shown_hash` = the row's current `row_hash` (the executor passes it).
- Read (N1): `_merge` copies `same_as`/`declared_by`; `_resolve_repeats(questions)` (one pass after merging, in `load` and
  `statuses_for`) follows `same_as` through `repeat` rows to the first non-repeat id: found -> `follows = <that id>` on the repeat and the id
  joins `repeated_by` of the target; missing id, a cycle, or more hops than rows -> `follows = ""`, `repeat_problem` = "gone" | "cycle".
- `is_open`: status `repeat` -> `not (follows and changed_since_answer is False)`. Not settled, no `answer_key` (unchanged functions).
- Effects: the target's card prints T2; `still_open` skips a resolved repeat and copies `repeated_by` onto the target's item (P2);
  `asked_for_brief` lists the repeat under its target (T1 lines); `report_facts._questions` skips a resolved repeat and gives the target
  `also: [ids]`, `_r_questions` adds T15. The plan row resting on Q16: `repeats_for_case` calls `planning_contract.repoint_question_ref(row,
  Q16, Q7, case)` (existing; by meaning or append + note line printed by the exit step, F10).
- Way out: `--reopen Q16` (existing) or any answer to Q16 (last record wins, P13); target gone/cycle/row changed -> open again (T14).

### D4 — `--reword`: one door to ask an unanswered question again, better (R3)
- `QR.reword(task_root, qid, spec, by, where)`; CLI `--reword Qn --question-file F --by <by> --where <where>`; F is JSON
  `{"question": "<text>", "readings": ["<text a>", "<text b>"]?}`. Under `answers_lock`, through `_write_readiness`: replaces `question`
  and, when given, each `readings[i].reading` (count must match; `from`/`if_chosen`/`source_says`/before/now untouched: facts stay the
  producer's); appends `reworded: [{"at", "by", "was": <old question>}]` to the row.
- Refused (nothing written) when: no such id; the register unreadable; the row's status is `answered`/`not_needed`/`deferred_to_report`/
  `repeat` (any recorded decision, holding or not: an answered row is reopened by the person first — FR-7 speaks of answered rows, this
  door only of unanswered ones); readings count differs; the new row fails `contract.question_errors`; the text is unchanged.
  Legal on `open` with no record, on `named`, and on `open` after a reopen.
- Effects: `row_hash` changes; with no answer record `changed_since_answer` stays False; an answer typed against the old card carries the
  old shown hash (FV1-3) -> recorded with it -> `changed_since_answer` True -> asked again with the new text (toward asking). The driver's
  `already_answered`/`question_body_sha` (`driver_dialog.py`) hash driver packets: the new text is a new packet — correct, nothing was
  answered. The id is kept, so no second row stands beside it.
- Who (F-4 (a)): the conductor, by a `conductor.md` row (T11), when a row went unanswered at a stop and the person's words show they could
  not tell what is asked. The S2 tester's own rework stays the producer's road for its rows (not a reword).

### D5 — the card helps (R4) — "helps" defined by fields
Help fields, in card order: H1 `source_says[].quote/where` (today); H2 `before`/`now` (today); H3 `readings[].if_chosen` (today);
H4 `question_effects` (today); H5 NEW: the requirement text of `requirement`, `raised_for.requirement` or `ref` when it is an R id of the
register (`contract.register_rows(planning_contract.story_register_text(task_root))`; `r` match exact), printed only when the row has no
H1 quote — T5; H6 NEW: the latest `note` record of the row whose `row_hash` equals today's — T4; H7 NEW: each reading's origin in
words (`QR.origin_words`), no parenthetical when `from` is blank. A card with none of H1, H2, H5, H6 and no reading with a known `from`
prints T6 (FR-41). `(from ?)` is never printed. Code relates no two rows; answered rows the question rests on reach the card only by
the conductor's note (P27).
- The conductor fills H6: `driver_gates.conductor_text` adds T10 when `rest` holds an `open_questions` finding (P7); it writes with
  `question_register.py --task <T> --note Qn --words-file F --by conductor --where conductor` -> `record_note` -> `_append` record
  `{"kind": "note", "id", "words", "by", "where", "at", "row_hash"}` (F-5 (a)). The tester's rework is not tried again after the cap.
- The gate's top: `check_open_questions` passes `question=qid` (extra key); `unrepaired_text` prints T8 for a finding with that key
  instead of its message (P6). The conductor still receives the full message and fix.

### D6 — texts, in full (English; human-questions.md voice)
- T1 brief section `## Questions already asked of the person`, first line: "Before you raise a question, read this list. If an answered
  question below already asks what you would ask, its answer is your source: cite its id and raise nothing new. If an open question below
  already asks it, point at its id and raise nothing new: the person is asked each thing once." Lines: open `- Q7 open, not answered
  yet: <question>` + ` (also raised as Q16)` when `repeated_by`; repeat of a settled row `- Q16 asks what Q1 asks; Q1's answer is its
  answer`; repeat of an open row: listed only on its target's line. Empty: `- none: no question has been asked in this story yet`.
  Unreadable: `- the question register could not be read, so this list may be incomplete; raise what you need, and say in your digest
  that you could not check for an earlier question`.
- T2 target card: "  - the same question was also raised as Q16; it is asked once, here, and your answer is the answer to both."
- T3 reworded card (status open, `reworded` non-empty): "  - asked again in clearer words: this is the same question as before, which
  had no answer yet. Earlier it read: \"<last was, squeezed, first 240 characters>\"" (+ "..." when cut).
- T4 "  - what may help you answer, from the factory's helper, who read the sources for it: <note words, squeezed, whole>"
- T5 "  - the requirement it is about (R-8): \"<requirement text, first 240 characters>\" — work/requirements-register.md"
- T6 "  - where these readings come from is not recorded, and the factory has found nothing more about this question; answer from what
  you know of the product, or in your own words."
- T7 `reading_origin_words`: acceptance_criteria "the acceptance criteria"; description "the ticket's description"; comment "a comment on the
  ticket"; parent_ticket "the parent ticket"; code "the code"; test "an existing test"; precedent "an earlier confirmed behaviour"; person
  "your choice"; claim "the behaviour seen in the product"; attachment "an attachment". Printed `(from <words>)`; an unknown word prints
  `(from: <word>)`.
- T8 gate top: "<qid>: the factory could not rewrite this question before asking you; its card shows everything known about it."
- T10 conductor: "For each `open_questions` finding above: when `controller.py rework --stage S2 --role qa-requirements-tester` is refused
  by the repair cap, do not try again. Read the sources and write what helps the person answer that question - where each reading comes
  from, the source line, what each answer changes, an answered question it rests on - with `question_register.py --task <T> --note <id>
  --words-file <file> --by conductor --where conductor`. Do not rewrite the question; its card shows your note."
- T11 `conductor.md` row: "| A question the person left unanswered after seeing it, whose words show they could not tell what it asks |
  `question_register.py --task <T> --reword <id> --question-file <file> --by conductor --where conductor` (a JSON object: `question`, and
  optionally `readings` as the same number of texts); the id stays, and the card says it is the same question asked again |"
- T12 designer "When to ask", new first bullet: "- Before you raise, read `Questions already asked of the person` in your brief. A
  question there that already asks yours: answered -> the Then's oracle is `person` with its id, and the value is the one its answer gives;
  open -> the Then is `unknown` with its id and a `question_thens` entry; raise nothing new. When the case critic names a question you
  raised as a repeat, point its Thens at the earlier id and list it once in `question_repeats`; the driver records it and the person is
  asked once."
- T13 critic "Where bugs hide": "- **A question asked twice.** A question the designer raised that asks what an open or answered question
  in `Questions already asked of the person` already asks: a finding naming both ids; the designer repairs it in its round." "When to ask",
  appended to `:133`: "Read that list first: an answered question there is your source, an open one is named by its id; raise nothing new."
- T14 `question_note` for an unresolved repeat: "it was marked as the same question as Q7, which the factory no longer has, so it is asked
  here" (cycle: "it was marked as the same question as another one that points back to it, so it is asked here").
- T15 report note: " (raised again as Q16; this one question covers both)".

### D7 — error direction of functions put in a more responsible role (designer rule 1, PROJECT.md 6 (в))
- `is_open` (decides what a person is shown) gains a HIDING branch. Allowed error: show (a repeat shown twice = today). Forbidden: hide
  a row whose target is not an existing, resolvable row, or whose bytes changed since the declaration. Awkward inputs that must stay
  shown: `follows` missing (a dict built outside `load`), `same_as` naming itself, a missing id, a row skipped by `load` (no id, not an
  object, duplicate id: the first is kept, so a repeat of the duplicate resolves to the first), a 2- and 3-cycle, a record with no
  `row_hash` (`changed_since_answer` None), a row changed since, a non-string `same_as`, whitespace around ids (stripped as `load` strips).
- `contract.then_oracle_errors` `person` (gates a case). Allowed error: refuse (the designer writes `unknown`). Forbidden: accept an
  answer that does not hold. Awkward: changed since, `before` value missing (`before_value_needed`), deferred, `with_designer`, `named`,
  `not_needed`, a repeat, no hash (holds, as `settled` already says).
- `unknown` relaxation (F-3): allowed error: refuse. Awkward: `readings` not a list, one reading, non-dict readings, a resolved repeat
  (refused with its target), a before/now row with a broken side (still refused by `before_now_errors`).
- NOT reused: `contract.question_errors` stays the rehearsal's (no person-facing decision rests on it: H-conditions are fields); `_shown`
  stays the (case, Then) idempotency check.

## §4. Edges (each with the invariant it protects)
| edge | behaviour | invariant |
|---|---|---|
| empty / absent register | brief T1 "none" line; no repeat resolvable; `--repeat`/`--reword`/`--note` refused naming the file | nothing is hidden or written without a register |
| a row unreadable (not object, no id) | skipped by `load` as today; a repeat pointing at it is unresolved -> shown | a hidden row always has a readable target |
| a Q id cited that does not exist | oracle refused (`contract.py:1720`, unchanged); `same_as` unknown refused at write; deleted later -> T14, shown | an id never resolves by guess |
| answer whose row changed since | `person` refused; brief omits it (as today); target changed -> target asked again, repeat stays hidden behind it | a stale answer is never a source |
| repeat of a repeat / cycle | chain resolved to the end; cycle refused at write; a cycle made by a race -> every member shown | the reader alone keeps it safe (F4 race) |
| a reworded row that had an answer | refused unless the last record is a reopen | an answered question is never re-asked in new words by the factory |
| two roles declaring at once | both records append (lock per line); the last wins; a cycle from the pair -> shown | no interleaved line, no hidden cycle |
| brief over 30 KB | the by-range note (FV1-4); nothing cut (F-2) | the person's words stay first |
| card with no helping data | T6 | an unknown is said, never a bare defect line |
| `question_repeats` entry malformed / ids absent / `why` blank | a problem line from the exit step; key kept; nothing recorded (person sees both) | a failed declaration errs toward asking |
| person answers the hidden repeat | recorded; status `answered` | the person's word wins (P13) |
| note for other bytes | not shown (row_hash differs) | a note measured on other bytes never counts |
| note > 2000 characters | refused AT 2001, accepted AT 2000 | the card is a card |
- TEMPORAL (both worlds): a story recorded before the change has no `repeat` record, no `note` line, no `reworded`, no `question` key on
  findings, no `question_repeats` in cases: every reader behaves as today except (i) `(from ?)` -> T7/no parenthetical, (ii) briefs gain T1
  at the next dispatch, (iii) `person` on a stale answer is refused at the next validation of that case (a case validated before stays
  pinned; the next S4 exit re-validates). The new world is created by the first `repeat` record (S4 raise step or conductor CLI), the first
  `--reword`, the first `--note`. An old finding without `question` -> `unrepaired_text` prints its message as today.
- POSITIONAL: P1 `is_open`: the repeat branch after the not-a-dict check, before `return True`; every other status's result unchanged.
  P2 `still_open`: inside `if mine is not None`, before `QR.settled(mine)`; a row with no register match is listed. P3 `raise_pending`:
  the filter becomes `RAISE_REF in content or "question_repeats" in content`; repeats after the same case's raise; a case with neither is
  never read further. P4 `question_card`: T2/T3 right after `status_note`; H5/H6 after before/now; T6 after the readings; the answer line
  stays LAST (GW1-32). P5 `render`: the new section after the person's words, before the approach block. P6 `unrepaired_text`: only
  findings with `check == "open_questions"` and a `question` key change; the direct-checks-first sort unchanged. P7 `conductor_text`: T10
  after the findings, before the closing `continue`/`ask_person` paragraph, which stays last.

## §5. Nodes (topic: one code critic after N3; N1 first, then N2 and N3 in parallel)

### N1 — the register: `repeat`, `reword`, `note`, `asked_for_brief`, the S4 raise step  [builder -> critic]
given: this spec §0-§4; `design/factory-rules.md` whole; `plans/builder-rules.md`; `question_register.py:84-1630`; `critic_rollcall.py:739-779`;
`planning_contract.py:3033-3060`; `design/state-exits.md`; `test_question_register.py` (rows near `:1600-1630`)
owns:
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n1\ai-packages\qa-factory\scripts\question_register.py (`_answers`, `_merge`, `load`, NEW `_resolve_repeats`, `statuses_for`, `is_open`, `record` (keyword `same_as`, `declared_by`), NEW `repeats_for_case`, NEW `reword`, NEW `record_note`, NEW `asked_for_brief`, NEW `origin_words`, `vocabulary` (validate the new row), `_VALUE_OPTIONS`, `_ALL_OPTIONS`, `main`, module docstring)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n1\ai-packages\qa-factory\references\question-vocabulary.json (`repeat` in two lists; `reading_origin_words` + note)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n1\ai-packages\qa-factory\scripts\critic_rollcall.py (`raise_pending` only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n1\ai-packages\qa-factory\design\state-exits.md (one row: `repeat`, exits `--reopen`, an answer, target unresolved)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n1\ai-packages\qa-factory\scripts\tests\test_question_register.py (new rows)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n1\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (rows for new units)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n1\ai-packages\qa-factory\changelog.d\fv1-9-question-repeats.md
non-goals: no card/brief/report text (N2, N3); no text comparison of questions; no change to token reading (`parse_choices`,
`_only_tokens`, `record_answers`: FV1-13's); no renumbering; `with_designer` untouched.
edges: §4 rows 1-7, 10-13; TEMPORAL; P1, P3.
DoD rows (`test_question_register.py`): `fv19_repeat_hidden_while_target_resolves` (Q16->Q7 open: Q16 not open, Q7 `repeated_by` [Q16]);
`fv19_repeat_of_settled_listed_for_brief` (Q7 answered: `asked_for_brief.repeats` [{Q16, Q7, True}]); `fv19_repeat_unresolved_shown` (table:
same_as gone / 2-cycle / 3-cycle / row changed since / no hash / `follows` missing -> open); `fv19_repeat_write_refusals` (table: no
same_as, self, unknown id, cycle, settled row, missing hash); `fv19_person_answer_beats_repeat`; `fv19_reopen_undoes_repeat`;
`fv19_reword_keeps_id` (id, `reworded[0].was`, hash changed, `changed_since_answer` False, no new row); `fv19_reword_refused_on_answer`
(table: answered, not_needed, deferred, repeat, readings count, unchanged text, `question_errors` fails, register unreadable);
`fv19_reword_after_reopen_allowed`; `fv19_note_bound_to_bytes` (note shown on same bytes; dropped after a row change; AT 2000 / BEYOND
2001; `kind: note` not counted in `skipped`); `fv19_asked_for_brief_empty_and_unreadable`; `fv19_raise_pending_records_repeats` (a case
with only `question_repeats` is read; key dropped; plan row repointed or note line); `fv19_origin_words_unknown_default`.
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/question_register.py ai-packages/qa-factory/references/question-vocabulary.json ai-packages/qa-factory/scripts/critic_rollcall.py ai-packages/qa-factory/design/state-exits.md`
(slow files it prints are judged by CI); grep `status") == "repeat"` outside `question_register.py` -> none (AR-13); census test row.
siblings: `statuses_for` (the publish twin of `load`) gets `_resolve_repeats` too; the S3 claim projector writes rows through
`_question_row` and never declares repeats (n/a: no carrier there).
architecture: AR-1, AR-13, AR-14, AR-22, AR-23, AR-25, AR-28 -- kept as §1.1. judgment: sameness stays with the role and the person; code
checks ids and bytes only (xref/shape).

### N2 — the card, gate A, the report, the conductor's turn  [builder -> critic; after N1]
given: this spec; N1's merged diff; `design/factory-rules.md`; `plans/builder-rules.md`; `references/human-questions.md`; `gate_brief.py:2734-2830,
4160-4252`; `driver_gates.py:698-815`; `gate_preflight.py:1929-2022`; `report_facts.py:2600-2621, 3960-3985`; `references/conductor.md:1-40`
owns:
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n2\ai-packages\qa-factory\scripts\gate_brief.py (`question_card`, `question_note`, `still_open`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n2\ai-packages\qa-factory\scripts\driver_gates.py (`unrepaired_text`, `conductor_text`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n2\ai-packages\qa-factory\scripts\gate_preflight.py (`check_open_questions`: the `add` call only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n2\ai-packages\qa-factory\scripts\report_facts.py (`_questions`, `_r_questions`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n2\ai-packages\qa-factory\references\conductor.md (row T11)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n2\ai-packages\qa-factory\scripts\tests\test_gate_question_form.py (new rows)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n2\ai-packages\qa-factory\scripts\tests\test_report_facts.py (new rows; slow, judged by CI)
non-goals: no new rehearsal check; `question_errors` unchanged; no S2 rework road; no change to `question_stop.py` (FV1-3's file; cards
arrive through `open_cards` unchanged); no relating of rows by code.
edges: §4 rows 3, 4, 9, 12; TEMPORAL (old finding without `question`); P2, P4, P6, P7.
DoD rows: `test_gate_question_form.py`: `fv19_card_help_fields` (table by field: H1..H7 each present alone -> its line; H5 suppressed
when H1 quote exists); `fv19_card_no_help_line` (no H1/H2/H5/H6, `from` blank -> T6, no `?`); `fv19_origin_words_on_card` (every
READING_ORIGINS word -> T7 words; unknown -> `(from: x)`); `fv19_target_card_says_also_raised`; `fv19_card_says_asked_again` (T3, cut AT
240 / BEYOND 241 with "..."); `fv19_still_open_skips_resolved_repeat` (+ unmatched row listed); `fv19_gate_top_no_defect_line` (T8; an
old finding without `question` prints its message); `fv19_conductor_text_note_door` (T10 present only with an `open_questions` finding;
closing paragraph last); `fv19_human_text_passes` (`human_text.problems` empty on the new cards). `test_report_facts.py`:
`fv19_report_lists_target_once` (Q16 absent, Q7 note T15; unresolved repeat listed).
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/gate_brief.py ai-packages/qa-factory/scripts/driver_gates.py ai-packages/qa-factory/scripts/gate_preflight.py ai-packages/qa-factory/scripts/report_facts.py ai-packages/qa-factory/references/conductor.md`
siblings: `question_stop.open_cards`/`batch_text` take the same card (axis 5, no edit); `kept_answer_text` prints no question card (n/a).
architecture: AR-16, AR-17, AR-22, AR-23, AR-27 -- one card form, the existing seam, fields with readers, the empty outcome said, the
target carries the merged question to the report. judgment: none added (data rendering).

### N3 — briefs, oracle refs, charters  [builder -> critic; after N1; after stage-critics A2 for `qa-case-critic.md`]
given: this spec; N1's merged diff; `design/factory-rules.md`; `plans/builder-rules.md`; `brief_pack.py:1738-1852, 4510-4590`;
`contract.py:1599-1742`; `references/artifact-contract.md:126-150`; `agents/qa-case-designer.md`; `agents/qa-case-critic.md` (as A2 left it)
owns:
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n3\ai-packages\qa-factory\scripts\brief_pack.py (`question_answer_lines`, NEW `asked_question_lines`, the section lines inside `build.render`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n3\ai-packages\qa-factory\scripts\contract.py (`then_oracle_errors`: the `person | unknown` branch only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n3\ai-packages\qa-factory\references\artifact-contract.md (`then_oracles` form paragraph; `question_repeats` key paragraph)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n3\ai-packages\qa-factory\agents\qa-case-designer.md (T12)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n3\ai-packages\qa-factory\agents\qa-case-critic.md (T13)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n3\ai-packages\qa-factory\scripts\tests\test_oracle_provenance.py (new rows)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n3\ai-packages\qa-factory\scripts\tests\test_brief_pack.py (new rows; slow, judged by CI)
non-goals: no cut of any brief part; no change to `answers_for_brief`'s shape; no new role tool; `role-commands.json` unchanged (roles run
no register command).
edges: §4 rows 1, 3, 4, 8; TEMPORAL (iii); P5.
DoD rows: `test_oracle_provenance.py`: `fv19_person_needs_holding_answer` (table: settled ok; changed since / before missing / deferred /
named / not_needed / repeat refused with the door); `fv19_unknown_on_reading_question` (>=2 readings ok; 1 reading / not a list refused;
before/now broken refused); `fv19_unknown_on_repeat_points_at_target`. `test_brief_pack.py`: `fv19_brief_lists_question_text`;
`fv19_brief_lists_open_rows` (repeat on its target's line; empty; unreadable); `fv19_section_after_person_words`. Charter keys quoted
verbatim (doc-dispatch witness, CLAUDE.md rule 11: keys from T12/T13 written before the run, script attached, one negative control);
`role_load.py --all` before/after named (AR-11 change check).
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/brief_pack.py ai-packages/qa-factory/scripts/contract.py ai-packages/qa-factory/references/artifact-contract.md ai-packages/qa-factory/agents/qa-case-designer.md ai-packages/qa-factory/agents/qa-case-critic.md`
siblings: every other role brief gets the section by the same call (axis 34); `validate_artifacts.check_then_oracles` passes the view
unchanged.
architecture: AR-10, AR-13, AR-29 -- told before the work, one reader, judgment in the charters. judgment: "a question asked twice" is
the case critic's finding (judgment, accepted by the designer's round and the person); code checks refs only.

Parallelism: N2 and N3 own disjoint files. `question_register.py` only N1. Hot list (PROJECT.md «Командная работа» п. 3): only
`gate_preflight.py` (N2, the `add` call in `check_open_questions`) — name the function in the dispatch (D-0048).

## §6. Crossings and queue order
- FV1-3 (merged form): owns `driver_dispatch.py`, `driver_machine.py`, `question_stop.py`, `audit_factory.py` — none here. FV1-9 after
  FV1-3 (batch row); FV1-3's shown hashes (`question_stop.shown`) are what makes a stale answer to a reworded card fall to "asked again".
- FV1-13 (owns `question_register.py` token reading): its function list must exclude N1's (`main`, `_VALUE_OPTIONS`, `record`, `load`,
  `_merge`, `is_open`); order FV1-3 -> FV1-13 / FV1-9 N1 in either order, the later merges main.
- Stage-critics A1a (`brief_pack.TRIED_READERS`, `stage_critic_names`, `FIRST_LOOK_KIND`): disjoint from N3's functions; parallel legal.
  A2 owns `agents/qa-case-critic.md` (`:30-33`, `:133` area) after TQ2-1 K1: queue `TQ2-1 K1 -> A2 -> FV1-9 N3`. A3: no shared file.
- TQ2-1 K2 (`brief_pack.case_concern_lines`): disjoint function. FV1-28/FV1-29 (`brief_pack.py`): name functions at dispatch.
- FV1-12 (S2 card `skills/qa-story/phases/s2.md`, `stages.json`): no shared file; if FV1-12 keeps an S2 critic, its brief gets T1 too.

## §7. Forks (returned, not decided; the nodes are written on the recommendation)
- F-1 (Lead) which briefs carry the asked list: (a) every brief, like the answered lines (one road; cost ~100-200 B per open row for S5+
  roles) — recommended; (b) stages S1-S4 (`QR.ROLE_QUESTION_STAGES`) only (smaller; a second rule for one list).
- F-2 (Lead) cut: (a) none, FV1-4 (a brief is rendered whole) — recommended; (b) cap the open lines at N with the rest in the decisions
  side file (cost: the role may miss the earlier question it repeats).
- F-3 (Lead; critic on plan, a gate's meaning) `unknown` on a reading question with no before/now: (a) allowed with >= 2 readings —
  recommended: F8 shows the current rule FORCES the S4 twin of every open S2 question; (b) keep (the twins stay structural, only D3 nets
  them; every story pays a repeat per S2 question its cases rest on).
- F-4 (OWNER — what the person is shown) who may reword an unanswered question: (a) the conductor, by `--reword` — recommended; (b) also
  the raising role through its form (a second road to one action); (c) nobody but the S2 tester's rework (R3 unmet for S4 rows).
- F-5 (Lead) carrier of the help: (a) `note` record in the answers file, bound to `row_hash` — recommended (survives the tester's
  publish, one writer `_append`); (b) a row field via `_write_readiness` (lost on the tester's next publish; changes `row_hash`).
- F-6 (OWNER — a role takes a question off the person's list) the declared repeat: (a) hidden, its target's card says it was raised again
  (T2), reopenable — recommended (R2); (b) only the person merges (both shown with a "same as" line: contradicts R2).
- F-7 (Lead) who declares: (a) the designer by a case key + the conductor by CLI, one writer — recommended (the two carriers raising has);
  (b) a handoff-form key for every role (new driver step at every acceptance).
- F-8 (Lead) a question-packet rework spends the S2 `test_defect` cap: (a) unchanged; the conductor's note fills the help — recommended
  (the Lead's plan); (b) a free `repair_cause` for a question-packet rework (more S2 rounds; the cap's meaning changes).

## §8. Small choices closed by the designer
New reader `asked_for_brief` instead of a key on `answers_for_brief` (F17 pin; three readers of that shape); `follows`/`repeated_by` computed
at load, never stored; hide only on `changed_since_answer is False` (stricter than `_holds`, as `closes` is); note cap 2000 characters;
`was` cut at 240 on the card (stored whole); H5 only when no H1 quote; T7 unknown word printed plainly; the repeat record's `by` is the
executor (`driver`/`conductor`), the declaring role in `declared_by` (never printed to the person).

## §9. Brief vs carriers (reported, scope not widened)
- "the brief ceilings are real — state the cut rule": the tree has no ceiling since FV1-4 (F7); returned as F-2.
- "the existing `replaces` / ref road" for an open question: blocked for S2 reading questions by `contract.py:1726` (F8); returned as F-3.
- "related answered rows" on the card: no data relates rows; only the conductor's note can (D5, P27).
- The controller's cap refusal advertises free causes (`question_answer`, ...) a conductor could misuse for an S2 rework: noted, F-8.
- Analog noticed: `_append` is a second jsonl appender beside `hooklib.append_jsonl_line` (axis 29) — existing, not widened.

## §10. Reading trail
Read: FV1-3 spec `:440-654`; recon `20261114-fv1-9-questions-recon.md` whole; stage-critics spec `:184-273` + heading grep; `question_register.py:84-472,
788-925, 1170-1640`; `question-vocabulary.json` whole; `gate_preflight.py:1929-2034, 1564-1673`; `driver_gates.py:698-1060`; `controller.py:370-410,
5585-5668`; `gate_brief.py:2715-2830, 4176-4253`; `question_stop.py:370-526`; `brief_pack.py:1730-1860, 4255-4660`; `contract.py:621-622, 690-718,
1186-1205, 1552, 1599-1628, 1700-1742`; `validate_artifacts.py:272-332`; `critic_rollcall.py:733-779`; `planning_contract.py:3033-3047`;
`report_facts.py:2600-2621, 3960-3985`; `artifact-contract.md:120-169`; `brief-form.json` whole; `agents/qa-case-designer.md` whole;
`agents/qa-case-critic.md:20-136`; `human-questions.md:13-62`; `architecture.md:140-173` + change-check grep; `test-layers.json` entries named;
`slow_tests.json` whole; `factory-7.log:1-90`; batch file rows FV1-3/9/13.
Greps (Grep tool, tree paths): `def repair_rounds|repair-round cap`; `no code move repairs|the list goes to the conductor`; `raise_from_handoff|
raise_for_case\(|with_designer`; `from-handoff`; `then_oracle_errors\(`; `answers_for_brief|question_answer_lines`; `QR\.(settled|is_open|load)` in
report_facts; `questions\[\]` per folder (the braced glob returned nothing — a miscall; re-run per folder found `agents/`, `references/` hits).
Negatives with controls: no register command in `conductor.md` (case-insensitive `question.register` empty; control `controller.py` hit in
the same file); no `repeat`/`note` status or CLI flag (files read whole; controls `with_designer`, `--reopen`). Not read: `SIBLING_MAP.md`
beyond headings (axes enumerated by heading); `factory-6.log` (facts kept from the FV1-3 spec); `driver_dialog.py` (recon's lines).
Not run: `scenario_walk.py` (no shell in this role).

## Owner's words on the forks (14.11.2026, verbatim) — recorded by the Lead

- F-4, who may reword an unanswered question — the owner: «любая роль которой нужен ответ». This is NOT the recommended (a): the
  door is open to every role that needs the answer, not to the conductor alone. Consequence for the fix round (Lead's reading, to be
  designed, not yet in D4/N1/N3): a role runs no register command, so a role rewords through its form (the carrier it raises through),
  executed by the same single writer `QR.reword`; the conductor's CLI row stays. One writer, two carriers — the shape raising and the
  repeat declaration already have (F-7 (a)).
- F-6, the declared repeat — the owner: «да» to (a): the twin is hidden, its target's card says it was raised again, reopenable.
- On the rule of fact F8 (`contract.py:1726`) the owner: «очень странное правило. Зачем оно?» — answered by the Lead: it is a side
  effect of P20's "show before / now" duty laid on every open (`unknown`) Then, not a rule against pointing at an S2 question. F-3
  stays with the plan critic.
- FV1-30b, what the person's word "the test was not run" lets go (explained by the Lead earlier) — the owner: «ок».
