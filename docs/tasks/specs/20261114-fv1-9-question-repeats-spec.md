# FV1-9 — a question asked once: repeats settled or merged, re-asking in clearer words, a card that helps (designer draft, rev. 2 — fix round of plan critic t-664)

Tree read: `C:\QAFactory\forge-repo\.claude\worktrees\read-main\ai-packages\qa-factory` (origin/main `50d9012`, 14.11.2026, FV1-3's code
merged); paths below are relative to it unless absolute. Run logs: `experiments/mybooks/factory-vs-free-agent/runs/factory-{6,7}.log`
(forge root, gitignored). Rev. 1 was read on `sc-a1a` (origin/main before FV1-3); every line number below is re-read on `50d9012`.
Status: DRAFT rev. 2 for Lead acceptance. Forks in §7: F-3/F-4/F-6/F-9/F-10 are decided (Lead or owner, quoted); F-11..F-14 are new
and returned. Critic on plan: rev. 1 had its pass (t-664, `docs/tasks/specs/reviews/20261114-fv1-9-plan-critic.md`, fit_with_fixes);
PROJECT.md «новая идея» step 6: a repeat pass only if the fixes change architecture. They add one node (N4, strategist carrier) and one
reader into the retro (N5, owner's word on B2) — the Lead judges whether that is an architecture change (§7 F-14).
Supersedes FV1-3 spec §5 (hint lines by shared `where`, `--withdraw`) where it contradicts the owner's words; its facts are kept.

## §0. The owner's words (verbatim, from `docs/tasks/specs/20261113-fv1-3-free-answer-to-conductor-spec.md:626-653` and the last section)

13.11.2026, F-7: «роль сама может ответить на этот  вопрос, раз есть ответ на уже заданный. Если ответа нет, то показываем человеку»
14.11.2026, F-7: «вопрос на который не ответили можно задать ещё раз в другой, более понятный формулировке, но два одинаковых вопроса в
один момент конечно не надо задавать»
14.11.2026, F-8: «надо не просто сказать что не так с вопросом, а что-то что поможет человеку на вопрос ответить»
14.11.2026, F-4: «любая роль которой нужен ответ»; F-6: «да» to (a); B3 (b): «да» (xref reading); B2: «никак. фабрика отмечает слитые
вопросы в ретро и мы смотрим потом на сколько решение было верным при анализе фабрики через коллект» (full record: last section).

| R | requirement (the Lead's reading of the words) | mechanism (§3) | the row that proves the code part (§5) |
|---|---|---|---|
| R1 | a repeat of an ANSWERED question is settled by the role from that answer | D1 the register's questions in every brief (answered ones WITH their question text); D2 craft lines: cite `person: Qn`, raise nothing; `person` accepted only on an answer that holds; D3 net: a declared repeat of an answered row reads "Qn's answer is its answer" | N3 `fv19_brief_lists_question_text`, `fv19_person_needs_holding_answer`; N1 `fv19_repeat_of_settled_listed_for_brief` |
| R2 | two questions asking the same thing are never shown at one moment | D1 open rows listed in every brief; D2 point at the open id; F-3 lets a Then point at an S2 reading question; D3 status `repeat`: hidden only while nothing else rests on it and its target stands, the target's card says it was raised twice; the report lists the target once; every merge recorded for the retro | N1 `fv19_repeat_hidden_while_target_resolves`, `fv19_repeat_refused_with_dependants`; N2 `fv19_target_card_says_also_raised`, `fv19_report_lists_target_once`; N5 `fv19_retro_lists_merged_questions` |
| R3 | an unanswered question MAY be asked again later in clearer words, by any role that needs the answer | D4 one writer `QR.reword`, reached through the form each role raises through and the conductor's CLI; id kept; who-may by data; readings frozen under others' letters; one reword per showing; old wording stored and shown | N1 `fv19_reword_keeps_id`, `fv19_reword_refusals`, `fv19_reword_who_may`, `fv19_reword_readings_frozen`; N4 `fv19_plan_reword_entry`; N2 `fv19_card_says_asked_again` |
| R4 | a question the rehearsal flagged and nobody reworked is shown WITH what helps answer it | D5 card help by fields (H1-H7), the conductor's `note`, `(from ?)` gone, the FR-41 line when nothing helps; the flagged question's defect line no longer printed at the gate's top | N1 `fv19_note_bound_to_bytes`; N2 `fv19_card_help_fields`, `fv19_card_no_help_line`, `fv19_gate_top_skips_carded_question` |

Code proves the data; that a role now looks before raising is a role behaviour, proved only by a live run (FR-33): one row for
`live-runs` (the LOCAL-1 pack: no S4 question repeating Q1-Q3; a flagged S2 question shown with help; a merge in the retro).

## §1. Package header (designer rule 1; CLAUDE.md rule 10; P27, AR-29)

### 1.1 AR-n touched, how each is kept (the change check is written into the node DoDs)
- AR-1 — `repeat` is a row of `references/question-vocabulary.json` `statuses`/`recorded_statuses`; the person's words for a reading's
  origin are a data row `reading_origin_words` (read by `question_register.origin_words`, default for an unknown word); which artifact
  kind is a role's OWN for the reword rules is a data row `reword_own_artifacts` (`{"qa-case-designer": "cases", "qa-test-strategist":
  "plan_rows"}`, default: none — the role's own link is then only `asked_by`). Change check (N1 DoD): grep `scripts/` for the literal
  `"repeat"` status and for the two role names outside `question_register.py` readers and the data file (positive control: the grep finds
  `with_designer` in `question_register.py`).
- AR-2, AR-7, AR-29 — whether two questions ask the same thing, and whether a reword kept the meaning, is the ROLE's judgment (designer
  looks; case critic finds and sees `declared_by`; the rewording role's stage critic judges the reword; the forge judges merges afterwards
  from the retro and the collect, owner 14.11). Code never compares two questions (no `_shown`, no `where` join, no text match;
  `meaning-proxy: 8` unchanged) and never maps a letter of one question to a letter of another (B1). Change check: census run; no new
  word-list/meaning-proxy/meaning unit.
- AR-10 — what the role must look at reaches it in the brief BEFORE the work (asked list, `shown_at_last_stop`, `declared_by`), and every
  role-side key (`question_repeats`, `reword_questions`, the `rewords` item of `questions[]`) and what code checks of it is stated in the
  contract and the charters in the same commit as the code that reads it (N1 code + N3 text land in one topic; N3 merges with N1's ids).
- AR-13 — one reader per fact: hidden/not hidden is `QR.hidden_repeat` only (called by `is_open`, `still_open`, `report_facts._questions`,
  `asked_for_brief`, `check_open_questions`); `follows` is read by `hidden_repeat` only; who keys an id is `QR.dependants` only (B1 and B3
  share it); the brief list is `QR.asked_for_brief` only; the last stop's shown hashes outside the driver are `QR.last_stop_shown` only;
  merge history is `QR.repeat_records` only. Change check: grep `follows` / `repeat_history` outside their one reader -> none.
- AR-14 — `work/requirements-readiness.json`: the S2 tester (producer) + `_write_readiness` (the one code writer: raised rows today,
  `reword` adds one caller); `work/question-answers.jsonl`: only `_append` (records `repeat`, `note`). The conductor writes neither file
  directly; `work/test-plan.json`: the `planning_contract` writers (`repoint_bare_ref` is one more through `_plan_row_for_write`).
- AR-16 — every new person-facing line is a card line of `gate_brief.question_card` (the one form; `human_text.problems` passes) or a
  report line of `_r_questions`.
- AR-17 — the cap's refusal reaches the conductor through the existing `hand_to_conductor` -> `conductor_round` seam; no new seam.
- AR-20 — judgment-census raise named in N1's DoD: `blocking_per_role.conductor` 761 -> 764 (m7).
- AR-22 — every new field has producer and reader: `same_as`/`declared_by`/`target_hash`/`texts`/`stage` (`declare_repeat` ->
  `_resolve_repeats`, `repeat_records`), `follows`/`repeated_by`/`repeat_problem` (`_resolve_repeats` -> `hidden_repeat`, card, report,
  brief), `reworded[]` (`reword` -> card T3, brief), `note` records (`record_note` -> `_merge` -> card), `question`/`on_card` extras on the
  finding (`check_open_questions` -> `unrepaired_text`), `merged_questions` (`retro_numbers.numbers` -> `render`; the collector carries both
  the raw records (E2) and `retro-numbers.json` (C4)). B1 keeps the readers of a hidden id from losing their producer.
- AR-23 — empty outcomes declared: empty register -> the brief says none asked; no help data -> the FR-41 card line; no merge -> the retro
  section says none.
- AR-24 — a person's answer to a hidden repeat is recorded and wins (last record); a stray `Q16:` line still reaches `gate_words_view`
  (`named_not_recorded`, `question_register.py:1169`, `not settled`); the note is NOT the person's words and is marked as the helper's (T4).
- AR-25 — `repeat` has ways out: `--reopen` (conductor, existing), the person's answer to its id, the target gone / changed / a cycle
  (shown again, T14); a `design/state-exits.md` row in N1. A reword keeps `was`; a later note supersedes an earlier one.
- AR-27 — the report lists the target once with T15; an unresolved repeat is listed under its own id.
- AR-28 — an unresolved repeat (target gone, changed since, cycle, row changed since) is OPEN, never hidden; a dependants read that fails
  counts as "dependants exist" (refuse, show both).

### 1.2 Checks added or altered: owner served, census class
| check | where | owner | class / census unit |
|---|---|---|---|
| declare a repeat: `same_as` an id of the register, not itself, no cycle, row not settled/deferred, NO dependants left after the bare-ref repoint (B1) | NEW `question_register.declare_repeat` (raises `Refused`) | data | xref; NEW unit, blocking (conductor +1) |
| hide a repeat: status `repeat`, chain resolved, `changed_since_answer is False`, target's `row_hash` == stored `target_hash` | NEW `question_register.hidden_repeat` (read by `is_open`, altered) | data (sameness: the declaring role's judgment, seen by the case critic through `declared_by`, judged afterwards by the forge from the retro/collect) | xref; no refusal site, no unit |
| `reword`: row open/named and unanswered; shown at the last stop on its current bytes; who-may by data; readings frozen under others' letters; count unchanged; passes `contract.question_errors`; text changed; `why` not blank | NEW `question_register.reword` (raises `Refused`) | data (meaning kept: judgment of the rewording role's stage critic; the person sees the old wording) | xref; NEW unit, blocking (conductor +1) |
| `record_note`: row exists, words 1..2000 characters, `human_text.problems` empty, `by` from the vocabulary | NEW `question_register.record_note` (raises `Refused`) | data | shape; NEW unit, blocking (conductor +1) |
| case keys `question_repeats` / `reword_questions` and the `rewords` item of `questions[]`: shape + ids (problem lines, never blocking) | NEW `repeats_for_case`, `rewords_for_case`; `raise_from_handoff` (altered) | data | xref; list transport, no new unit |
| plan key `reword_questions` (problem lines, never blocking) | NEW `planning_contract._reword_plan_entries` (from `project_plan`) | data | xref; list transport, no new unit |
| bare-ref repoint: unapproved plan, row names old in `question_refs`, no `if_answered[old]`, reason does not name old | NEW `planning_contract.repoint_bare_ref` | data | xref; returns a tuple, no unit |
| `person` oracle: the ref's answer holds (`QR.settled` and status `answered`) — was raw status | `contract.then_oracle_errors` (altered) | data | xref; existing unit, list transport |
| `unknown` oracle: before/now shown OR 2..26 dict readings each with a non-blank `reading`, no `readings_unnameable` (F-3) | `contract.then_oracle_errors` (altered) | data | xref; existing unit |
| a raised `open_questions` finding is skipped for a hidden repeat; tagged `question`/`on_card` | `gate_preflight.check_open_questions` (altered) | data | shape; existing unit, list transport |
| a question raised that asks what an asked one asks; a self-declared repeat (`declared_by`) | `agents/qa-case-critic.md` (finding), `agents/qa-case-designer.md` (look first) | judgment, accepted by the critic's round | not code |
| a reword kept the meaning | the rewording role's stage critic (its acceptance round reads the brief's `reworded` line) | judgment, accepted by the critic tier; the person sees T3 | not code |
| a merge was right | the forge, from the retro section (N5) and the collect (E2) | judgment after the run (owner 14.11) | not code |

### 1.3 SIBLING_MAP axes (one block; each line closes every mechanism M1 brief list, M2 repeat status + retro record, M3 reword, M4 help/note, M5 oracle refs)
axis 1: n/a — no policy/role-file/journal change of this deployment. axis 2: n/a — no exam instrument. axis 3: n/a — release copy follows
the package by the release procedure. axis 4: covered — no FR changes; FR-7 read for M3 (§3 D4); no debt line. axis 5: covered — stage
twins: the question stop card and the gate A card are ONE renderer (`question_card`, `open_cards` `question_stop.py:384`), so M2/M3/M4
reach both; `still_open` (gate A), `is_open` (stop), `check_open_questions` (rehearsal) all call `hidden_repeat` (N1, N2). axis 6: covered
— the collector already tails `work/question-answers.jsonl` (`references/collect-sets.json:53`, E2) and copies `work/retro-numbers.json`
(`:46`, C4): M2's retro record reaches the forge with no collector change; `stage_compare.py` does not read the register (no measurer
change). axis 7: n/a. axis 8: n/a — paths through the existing story root. axis 9-11: n/a. axis 12: covered — one batch row (FV1-9); the
live proof row goes to `live-runs`. axis 13: covered — M1 adds a brief section; FV1-4's "rendered whole" holds (F-2). axis 14-16: n/a.
axis 17: n/a — no detector verdict shape. axis 18: covered — census rows, raise named (761 -> 764); `meaning-proxy` unchanged. axis 19-28:
n/a — no role-file tools line, host receipts, table cells, host forms, test rows, run joins, freshness, stand words, profiles, row-form
sites. axis 29: covered — M2/M4 append through `_append` (the register's appender; `hooklib.append_jsonl_line` `:600` is an existing twin,
queued, not new). axis 30: n/a. axis 31: covered — the look-first rule lives once per role in its charter; the contract carries the forms
only. axis 32: covered — §1.2. axis 33: n/a. axis 34: covered — one road per action: hiding = `hidden_repeat` for every reader; declaring
= `declare_repeat` with two carriers (designer's case key, conductor's CLI); rewording = `reword` with the carrier each role RAISES
through (case key, plan key, `questions[]` item, CLI) — the reach of rewording equals the reach of raising (§7 F-11); help = one card
renderer for every stage; merge history = one record read by retro and collect. axis 35-36: n/a.

## §2. Facts (re-read on read-main `50d9012`)

- F1 Statuses: `references/question-vocabulary.json:2-3` (open, answered, not_needed, with_designer, named, deferred_to_report); `where`
  `:4` (`gate A` ... `conductor`, `stage ran`); `by` `:17`. No `repeat`/`note` (file read whole; control: `with_designer` on the same lines).
- F2 `is_open` `question_register.py:431-443`: False only for `with_designer` and a settled/deferred record that holds. ALL readers (m2):
  `question_register.py:451` (`open_blocker`), `:1005` (`record_answers` idempotency: a hidden repeat is not `same` for a new answer, so the
  answer is written), `:1118` (`question_lines_unread`: a stray `Q16:` line of a hidden repeat is no longer flagged here; it still reaches
  `gate_words_view.named_not_recorded` `:1169`), `:1185` (`answers_for_brief`: a repeat has no settled status, no entry);
  `question_stop.py:251` (the count: a hidden repeat is not counted — the threshold counts what is shown), `:307`/`:333` (`open_blocker`:
  a hidden blocker repeat leaves its open target blocking), `:397` (`open_cards`), `:423` (`answer_block`), `:490`/`:494` (`batch_text`: a
  hidden repeat counts as neither open nor settled — it is inside its target's card); `planning_contract.py:2750`, `driver_machine.py:2809`,
  `report_facts.py:3965` (each asks DEFERRED and not open: unchanged for `repeat`); `driver_stage_plan.py:933` (`settle_role_questions`:
  a hidden repeat is not handed to the conductor); `check_witness.readiness_rules` `:169` via `open_blocker` `:181`, `:184`;
  `branch_accounting._exclusion` via `open_blocker` `:2290`. None breaks (traced by the critic; re-listed here). Gate A's list is NOT
  `is_open`: `gate_brief.still_open` `:4202` skips `QR.settled(mine)`.
- F3 `_merge` `:252-284`, `load` `:287-340`: one record per id (the last), `row_hash` = sha256 of the row (`_hash` `:149-156`); `_answers`
  `:159-202` counts any `kind` other than `question`/`case` as `invalid` `:194-196` (a `note` line today would be "set aside"); a
  `question` record with an unknown status is `invalid` too (so a `repeat` record written before N1's vocabulary row is set aside).
- F4 `record` `:862-921`: refuses a different answer on a settled row; `status="open"` (a reopen) needs no hash `:895`, so `--reopen` works
  on a `repeat` row once `repeat` is a recorded status; check-then-append is not one lock span (`load` `:879`, `_append` `:814-829` takes
  `answers_lock` `:788` itself) — a race is possible today for every record.
- F5 CLI `_VALUE_OPTIONS` `:1634-1636`; operations `:1727-1733`; no reword/note/repeat (read whole; control: `--reopen` present `:1697`).
- F6 `answers_for_brief` `:1174-1194` carries `question` per item `:1191`; `brief_pack.question_answer_lines` `:1735` does not print it.
  `test_question_register.py:1602` pins `answers_for_brief` == `{"answers": [], "unreadable": False}` (why D1 adds a new reader).
- F7 FV1-4: `brief_pack.build.render` `:4523-4560` "Nothing is measured against a size and nothing is dropped for room" `:4526`; the
  answered rows print under "## The person's words that concern you" `:4529-4533`, ABOVE where D1's section goes; only a by-range note over
  30 KB `:4568-4578`.
- F8 ROOT CAUSE of the S2/S4 pairs: a Then can point at an existing question only as `person` (answered, `contract.py:1723`) or `unknown`
  (`:1726`, needs `"before" in questions[ref]`). S2's reading questions can never be the ref of an open S4 Then, so the designer must raise
  a before/now twin. Narrowed by the critic (true): "of every open S2 reading question a Then rests on".
- F9 `person` checks the raw status (`contract.py:1723`), so an answer whose row changed since is accepted as an oracle.
- F10 S4 raise step: `critic_rollcall.raise_pending` `:739-779` (substring filter `C.RAISE_REF in content` `:768`; writes the authoring file
  and re-pins `:775-777`); its printer is the O4 block of `critic_rollcall.main` `:1170-1182` (`plan_notes` printed, never dropped).
  `replaces` -> `planning_contract.repoint_question_ref` `:3033-3073`, whose `_repoint_obstacle` `:2992-3030` needs BOTH questions to say
  which reading is before/now `:3012-3017` — never true for an S2 reading question, so the move falls back to `append_question_ref`
  `:2934-2958` (B1). Every S4-raised question is appended to its case's plan row `question_refs` (`_name_in_plan_row` `:1443-1470`).
- F11 Card `gate_brief.question_card` `:2734-2825`: `status_note` `:2754-2756`; source_says `:2757-2761`; before/now `:2767-2773`;
  `(from {reading.get('from', '?')})` `:2786`, `:2794`; unlettered readings over 26 `:2777-2788` (`QUESTION_LETTERS` `:2415`); `if chosen`
  `:2795-2797`; effects `:2798-2806`; `readings_unnameable` `:2819`; the answer line LAST `:2824`.
- F12 Report: `report_facts._questions` `:2635-2656` lists every row not `QR.settled` (text, not ids); `_r_questions` `:4143-4168`.
- F13 Rehearsal: `gate_preflight.check_open_questions` `:1929-2022`: skips `row_answered` `:1991` and register-settled `:1993`; finding
  FACTORY_FIXABLE `:2017-2022`; `add` keeps `**extra` keys. The packet's own rehearsal list shows only `person_decides` items
  (`gate_brief.open_rehearsal_items` `:514-515`), so a FACTORY_FIXABLE finding reaches the person only through `unrepaired_text`.
- F14 TRACED — after the cap: `driver_gates.gate_stop` `:976-999` -> `hand_to_conductor` `:1001-1014` -> `conductor_round(Refusal(
  conductor_text(...)))` `:791-815`; controller cap refusal `controller.py:5653-5664`. A stopped series shows `unrepaired_text`
  `:698-721` at the gate's top `:918`, under the header "These are the factory's own to repair, not questions for you ... Your answer does
  not depend on them" `:708-711`, printing each finding's message verbatim — for `open_questions` that is "Q1 cannot be answered as it
  stands ..." about a question the same packet asks (FR-10, B4).
- F15 `conductor.md` (the conductor's system prompt, `driver_conductor.py:337`) names no register command; its table `:17-44`. FV1-3's
  hand-over text names `question_register.py --answer|--not-needed|--defer` (`driver_dispatch.register_words_to_conductor` `:1854-1856`).
- F16 Roles run no register command. Raise carriers today: the case designer's case key `raise_questions` (`raise_pending`); the
  strategist's plan-row `new_questions` (`planning_contract.project_plan` `:3315-3377` -> `_raise_new_questions` `:3247-3286`); the stage
  acceptors' form `questions[]` (`driver_stage_plan.stage_acceptance_write` `:641-651` runs `question_register.py --raise --from-handoff`
  -> `raise_from_handoff` `:1591-1627`; the case critic's charter `agents/qa-case-critic.md:133`); the S2 tester writes the register itself.
  No other role's form is raised (grep `"--raise"` in `scripts/*.py`: only `driver_stage_plan.py:647`; control: the test hits in
  `test_question_register.py`).
- F17 FV1-3 on read-main (corrects rev. 1 and the critic's B3 (f)): the stop saves `state["question_stop"] = {..., "shown": hashes, ...}`
  in `<task>/state/driver-state.json` (`driver_dispatch.py:1668-1670`; `state_dir` `driver_core.py:461`), OVERWRITTEN at every stop; the
  person's words go `take_question_answer` `:1760` -> `record_question_words(stage, words, shown)` `:1890` -> `QR.record_answers(..., shown,
  ...)` `:1906`; words that are not all tokens go `register_words_to_conductor` `:1818` (FV1-3's one hand-over, AR-17). `question_stop.shown`
  is a driver-state KEY, not a function (`question_stop.py` has no `def shown`); the batch file on read-main still says FV1-3 «ожидает»
  (`plans/piles/live-run-fvf/batch-1-live-run-fvf.md:36`) — a status lag, the code is merged.
- F18 Collector: `references/collect-sets.json` is the data of `qa-collect` (`collect_pack.py:12`, `SETS_FILE` `:56`); E2 `work/question-
  answers.jsonl` mode `tail` (`:53`: each collect takes the new lines since the last one, `collect_pack.py:872-895`), E1 the readiness file
  `sum open_questions` (`:52`, items as they stand at collect time), C4 `work/retro-numbers.json` `copy` (`:46`). Retro facts:
  `retro_numbers.numbers` `:2115` (returns the facts dict `:2229`), rendered by `render` `:2648`, written by `write_retro` `:3001`.
- F19 Census: `judgment-census.json:4` ratchet `blocking_per_role.conductor: 761`; `question_register.py::record` is a `safety`/`intent` row
  (`:867`), `raise_from_handoff` `shape` (`:864`), `_raise` `xref` (`:861`).
- F20 Tests: keep rows (section `keep` `test-layers.json:36-7131`): `test_question_register.py` `:4203`, `test_gate_question_form.py`
  `:1995`, `test_oracle_provenance.py` `:3503`, `test_brief_pack.py` `:288` (slow, `keep_fail_at_entry` `:7134`), `test_report_facts.py`
  `:4452` (slow), `test_retro_numbers.py` `:4569`, `test_s3_strategist_rounds.py` `:4770` (holds the `project_plan` cases). Quarantined
  (section from `:7164`, not used): `test_question_stop.py`, `test_story_run_gate_repair.py`, `test_brief_pack_roles.py`,
  `test_stage_critic_route.py` `:9951`, `test_planning_contract_not_planned.py` `:9069`.

## §3. Design

### D1 — the asked questions reach every brief (R1, R2 prevention; data to the role)
- N1: `QR.asked_for_brief(task_root) -> {"open": [{id, question, repeated_by: [ids], shown_at_last_stop: bool, reworded: int}],
  "repeats": [{id, same_as, target_settled: bool, declared_by}], "unreadable": bool, "present": bool}` — open = `is_open(q)` in register
  order; repeats = rows for which `hidden_repeat(q)`; `shown_at_last_stop` = `QR.last_stop_shown(task_root)["shown"].get(id) == row_hash`
  (B3 (e): the only record of a showing with its bytes today is the last stop's, F17 — a COUNT of showings has no producer, so the brief
  carries the fact the reword rule needs; a gate A showing is not recorded and does not count — the error goes toward fewer rewords).
  One `load`, one driver-state read.
- `QR.last_stop_shown(task_root) -> {"stage", "at", "shown": {id: hash}}`, `{"shown": {}}` when the file or the key is absent or
  unreadable (never raises). The ONE reader of the driver's `question_stop` outside the driver (read-only).
- N3: `brief_pack.question_answer_lines` adds `; the question: "<question, whitespace squeezed, whole>"` after the head (before the
  person's words). New `brief_pack.asked_question_lines(task_root)` renders T1; `render` places the section right after the person's
  words and before the approach block (POSITIONAL P5). Which briefs: every brief (F-1 (a)). Cut: none (F-2 (a), FV1-4).

### D2 — the craft rule and what code checks (R1, R2)
- Charter lines T12 (designer, "When to ask") and T13 (case critic, "Where bugs hide" + "When to ask"). The role judges sameness.
- Code checks (N3, `contract.then_oracle_errors`): `person` ref -> the ref exists and `QR.settled(q) and q["status"] == "answered"` (F9
  closed); `unknown` ref -> before/now shown (as today) OR, when the row carries neither `before` nor `now`: `readings` is a list of 2..26
  items (26 = `len(question_register.LETTERS)`, the alphabet `gate_brief.QUESTION_LETTERS` `:2415` letters the card by), every item a dict
  with a non-blank `reading`, and `readings_unnameable` is not true (F-3 (a), the critic's tighter predicate). A row carrying `before` or
  `now` still goes through `before_now_errors`. A ref whose row is a hidden repeat is refused: "`{ref}` was marked as the same question as
  `{target}`: point the Then at `{target}`". `artifact-contract.md:136-140` says the same. The `question_thens` duty `:1729-1733` unchanged.

### D3 — status `repeat`: the net for a repeat already in the register (R2 net; R1 net)
- Declared by (F-7 (a)): the case designer, as a case front-matter key `question_repeats: [{"question": "Q16", "same_as": "Q7", "why":
  "<one line>"}]`, executed by the S4 raise step (`raise_pending` -> `QR.repeats_for_case`, after `raise_for_case` of the same case); and the
  conductor, by CLI `question_register.py --task <T> --repeat Q16 --same-as Q7 --words-file <why> --by conductor --where "stage ran"`.
  Both reach ONE function `QR.declare_repeat(task_root, qid, same_as, why, *, by, declared_by, stage)`:
  1. under `answers_lock`? No: `declare_repeat` reads (`load`), repoints, re-reads, then calls `record` (which appends under the lock) —
     the race of F4 is the same as every record's; the reader keeps it safe (§4 row "race").
  2. checks: `same_as` a string id of the register, not `qid`, following `same_as` from it through `repeat` rows never reaches `qid`
     (cycle), `qid` not settled/deferred/`with_designer`, `qid` not already a hidden repeat of the SAME target (then: no-op, return the
     existing record — idempotent replay), `why` not blank.
  3. B1 bare refs: for each plan row that names `qid` in `question_refs` with no `if_answered[qid]` and whose `reason` does not name it,
     `planning_contract.repoint_bare_ref(task_root, row_id, qid, same_as, case)` replaces the ref (no letter is involved: AR-29 kept).
  4. B1 dependants: `QR.dependants(task_root, qid)` after step 3; ANY plan row still naming `qid` (`question_refs` or `if_answered`), ANY
     case naming it (`then_oracles` ref with source `person`/`unknown`, or a `question_thens` entry), or `unknown` non-empty -> `Refused`
     naming each: "`Q16` cannot be merged into `Q7` while these still rest on Q16: plan row TS-3 (its answers branch), case TC-9 (Then 2).
     Expected: repoint them first — the test planner's rework for a plan row, the case designer for a case — then declare the repeat again".
  5. `record(task_root, qid, "repeat", why, "stage ran", by, row_hash_of_qid, same_as=..., declared_by=..., target_hash=row_hash_of_target,
     stage=..., texts={"question": <qid's question>, "same_as_question": <target's question>})` — `record` gains these keyword fields,
     stored only on a `repeat` record. The record is the RETRO RECORD (owner, B2): who declared, both ids, both texts as they stood, the
     why, the stage, the time — durable in the answers file, which the collector tails (E2, F18).
- Read (N1): `_merge` copies `same_as`/`declared_by`/`target_hash` of a `repeat` record; `_resolve_repeats(questions)` (one pass after
  merging, in `load` and `statuses_for`) follows `same_as` through `repeat` rows to the first non-repeat id: found, and every hop's stored
  `target_hash` equals its immediate target's `row_hash` -> `follows = <that id>`, the id joins `repeated_by` of the target; missing id ->
  `repeat_problem = "gone"`, a cycle or more hops than rows -> `"cycle"`, a hop whose target changed -> `"target_changed"`; `follows = ""`.
- `QR.hidden_repeat(q)`: `status == "repeat" and q.get("follows") and not q.get("repeat_problem") and q.get("changed_since_answer") is
  False`. `is_open`: `if status == "repeat": return not hidden_repeat(q)`. Not settled, no `answer_key` (unchanged functions).
- History: `_answers` also collects every `repeat` record in file order (a 5th return value; its two callers `load` and `statuses_for` are
  N1's); `load` returns it as `repeat_history`. `QR.repeat_records(task_root) -> {"records": [{id, same_as, declared_by, by, why, stage,
  at, texts, standing}], "unreadable": bool}` — `standing` = "merged" (the id is a hidden repeat now, behind this record's target),
  "shown again: gone|cycle|target_changed|its words changed", "answered by the person", "reopened", "replaced by a later merge".
- Effects: the target's card prints T2; `still_open` skips a hidden repeat and copies `repeated_by` onto the target's item (P2);
  `asked_for_brief` lists the repeat under its target (T1 lines, `declared_by` for the case critic — B2's tier above); `report_facts.
  _questions` skips a hidden repeat and gives the target `also: [ids]`, `_r_questions` adds T15; `check_open_questions` skips a hidden
  repeat (B4); `retro_numbers` lists every record (D7, N5).
- Ways out: `--reopen Q16` (conductor, existing; no person door — owner 14.11), any answer to Q16 typed by the person (`record_answers`
  reads every register id, last record wins, P13), target gone / changed / a cycle -> shown again with T14.
- A reword of a TARGET (F-13): `reword` re-declares each of the row's hidden repeats with the new `target_hash` (one `repeat` record each,
  `by` = the reword's executor, `declared_by` = the original declarer, `why` = "carried over: <target> was asked again in clearer words";
  a reword keeps the meaning — the stage critic judges that), so a reword never shows two questions at once. A tester's republish of the
  target is NOT carried: the repeat shows again (`target_changed`) — toward asking.

### D4 — `reword`: one writer, the carriers each role raises through (R3; owner's F-4, B3)
- One writer: `QR.reword(task_root, qid, spec, *, role, by, stage) -> row`; `spec` = `{"question": "<text>", "readings": ["<a>", ...]?,
  "why": "<one line>"}`. Under `answers_lock`, through `_write_readiness`: replaces `question` and, when `readings` is given, each
  `readings[i].reading` (`from`/`claim`/`if_chosen`/`source_says`/before/now untouched: facts stay the producer's); appends `reworded:
  [{"at", "by", "role", "stage", "why", "was": <old question>, "was_readings": [<old texts>] (only when readings changed)}]`.
- Carriers (B3 (a); the reach of rewording = the reach of raising, F16):
  - case designer: case front-matter key `reword_questions: [{"question": "Qn", "text": "...", "readings": [...]?, "why": "..."}]`,
    executed by `raise_pending` -> `QR.rewords_for_case(task_root, case_text, case_id)` (after `repeats_for_case`), role
    `qa-case-designer`, `by` = `driver`, stage `S4`; done entries dropped from the key; refused entries kept, a line each.
  - stage acceptors (the case critic today, `qa-case-critic.md:133`): an item of the form's `questions[]` carrying `rewords: "Qn"` with
    `question`, `readings?`, `why`; `raise_from_handoff` routes such items to `QR.reword` (role = `asked_by`, `by` = `driver`, stage =
    `stage`) and the others to `raise_role_question` as today. A refused reword is a line in the result (`"reword_problems"`), NEVER part
    of the all-or-nothing refusal (`stage_acceptance_write` runs it with `check=True` `:648`: a reword's timing must not refuse the
    critic's finish). Shape errors of a `rewords` item are reword problems too.
  - test planner (strategist): plan-row key `reword_questions` (same entry shape), executed at S3 close by `planning_contract.project_plan`
    -> NEW `_reword_plan_entries(root, rows)` (after `_raise_new_questions`), role `qa-test-strategist`, `by` = `driver`, stage `S3`; done
    entries leave the row (as `new_questions` do, `_rename_new_refs` `:3307-3311`); refused ones stay, a problem line each (`out.problems`
    is NOT used for them — those stop the plan write; a new `out.notes`). N4.
  - conductor: CLI `question_register.py --task <T> --reword <id> --question-file <file> --by conductor --where "stage ran"` (T11), role
    `conductor`.
- Refused (nothing written) when (B3 (b), (c), FR-7):
  1. no such id; the register unreadable;
  2. the row's status is not `open` and not `named` (answered / not_needed / deferred_to_report / repeat / with_designer — an answered row
     is reopened by the person first; FR-7 speaks of answered rows, this door only of unanswered ones);
  3. ONE REWORD PER SHOWING: the last question stop did not show this id on its CURRENT bytes (`last_stop_shown(...)["shown"].get(qid) !=
     row_hash`) — "not shown to the person in these words since it was last worded; it can be asked again in other words after the person
     has seen it". (A first reword also needs the showing: "asked again" presumes it was asked.)
  4. WHO MAY (F-10, owner 14.11): role `conductor` always; a role in `reword_own_artifacts` when its own artifact kind names the id
     (`dependants` has a case naming it for `cases`, a plan row naming it for `plan_rows`) or the row was raised by its carrier
     (`raised_for.case` for `cases`, `raised_for.origin == "S3-plan"` for `plan_rows`); any other role when the row's `asked_by` == role.
     Else: "`<role>` does not cite Qn in its own work: raise a question of your own, or cite Qn by its id instead".
  5. READINGS FROZEN (B3 (c)): `readings` given and `dependants` shows a letter-keyed dependant that is NOT the role's own kind (a plan row
     with `if_answered[qid]` for any role but the planner; a case `question_thens` entry for `qid` for any role but the case designer; any
     for the conductor and the acceptors), or `dependants.unknown` -> "the readings of Qn are what TS-3 / TC-9 answer by letter: reword the
     question only, or ask their owner to repoint first". The count differs -> refused; a blank reading -> refused.
  6. the new row fails `contract.question_errors`; the question text and every given reading are unchanged; `why` blank.
- Effects: `row_hash` changes; no answer record -> `changed_since_answer` stays False; an answer typed against the old card carries the old
  shown hash (`driver-state.json` `question_stop.shown`, F17) -> recorded with it -> `changed_since_answer` True -> asked again with the new
  text (toward asking; verified by the critic, B3 (f)). The driver's packet hashes (`driver_dialog.py`) see a new packet — nothing was
  answered. The id is kept, so no second row stands beside it.
- Who judges the meaning (B3 (d)): the rewording role's stage critic in its acceptance round (the case designer's at S4, the planner's at
  S3; the brief shows `reworded` with the old wording, T1); the acceptor's and the conductor's rewords are judged by the person only (T3
  shows the old wording beside the new). Code checks ids, shape, showing, dependants.
- TEMPORAL loss (B3 (g)), chosen: ACCEPTED toward asking. A later S2 tester publish rewrites the row from its own copy: the reword and
  `reworded[]` are lost, the row is the tester's text, an answer recorded on the reworded bytes reads `changed_since_answer` True and is
  asked again; a repeat whose target was reworded and then republished shows again (`target_changed`). Routing rewords through the
  tester's input would make every reword an S2 rework (the cap of F-8). Not chosen.

### D5 — the card helps (R4) — "helps" defined by fields
Help fields, in card order: H1 `source_says[].quote/where` (today); H2 `before`/`now` (today); H3 `readings[].if_chosen` (today); H4
`question_effects` (today); H5 NEW: the requirement text of `requirement`, `raised_for.requirement` or `ref` when it is an R id of the
register (`contract.register_rows(planning_contract.story_register_text(task_root))`; `r` match exact), printed only when the row has no H1
quote — T5; H6 NEW: the latest `note` record of the row whose `row_hash` equals today's — T4; H7 NEW: each reading's origin in words
(`QR.origin_words`), no parenthetical when `from` is blank. A card with none of H1, H2, H5, H6 and no reading with a known `from` prints T6
(FR-41). `(from ?)` is never printed. Code relates no two rows; answered rows the question rests on reach the card only by the
conductor's note (P27). The help lines are built by ONE helper `gate_brief._help_lines(question, ...)` (critic: `question_card` is ~90 lines).
- The conductor fills H6: `driver_gates.conductor_text` adds T10 when `rest` holds an `open_questions` finding (P7); it writes with
  `question_register.py --task <T> --note Qn --words-file F --by conductor --where "stage ran"` -> `record_note` -> `_append` record
  `{"kind": "note", "id", "words", "by", "where", "at", "row_hash"}` (F-5 (a)). `record_note` refuses words on which `human_text.problems`
  finds anything (K6 (b): plugin paths, field names never reach the person). The tester's rework is not tried again after the cap.
- The note exists only after a gate-A rehearsal reached the cap path (the rehearsal is the only detector of a flawed question); the FIRST
  question stop showing a flawed S2 question carries H1-H5/H7 but no note — ACCEPTED (K2 R4); a stop-time detector is a new detector,
  noted in §9, not built here.
- The gate's top (B4): `check_open_questions` skips a row whose register match is a hidden repeat (`QR.hidden_repeat`) and passes
  `question=qid, on_card=<the match is is_open>` (extra keys). `unrepaired_text` leaves out every finding with `check == "open_questions"`
  and `on_card is True`: the person answers that question on its card, which carries the H-lines/T6, so no top line (T8 dropped). The
  header claim stays true for the rest. A finding without the keys (old) or with `on_card` False (e.g. a `with_designer` row: no card)
  prints its message as today. The conductor still receives the full message and fix.

### D6 — texts, in full (English; human-questions.md voice)
- T1 brief section `## Questions already asked of the person`, first line: "Before you raise a question, read this list and the answers
  above, under the person's words. If an answered question there already asks what you would ask, its answer is your source: cite its id
  and raise nothing new. If an open question below already asks it, point at its id and raise nothing new: the person is asked each thing
  once." Lines: open `- Q7 open, not answered yet: <question>` + ` (shown to the person at the last question stop)` when
  `shown_at_last_stop` + ` (asked again in other words N time(s); earlier: "<last was, squeezed, 240>")` when `reworded` + ` (also raised
  as Q16, merged here by <declared_by>)` when `repeated_by`; repeat of a settled row `- Q16 asks what Q1 asks (merged by <declared_by>);
  Q1's answer is its answer`; repeat of an open row: only on its target's line. Empty: `- none: no question has been asked in this story
  yet`. Unreadable: `- the question register could not be read, so this list may be incomplete; raise what you need, and say in your digest
  that you could not check for an earlier question`. (Briefs are role-facing: role names are allowed here.)
- T2 target card: "  - this question was raised twice in this story; it is asked once, here, and your answer is the answer to both." (No
  twin text and no split door — owner 14.11, B2; FR-10 holds because B1 refuses a merge anything else rests on.)
- T3 reworded card (status open, `reworded` non-empty): "  - asked again in clearer words: this is the same question as before, which had
  no answer yet. Earlier it read: \"<last was, squeezed, first 240 characters>\"" (+ "..." when cut); and, when `was_readings` exists, one
  line per changed reading: "    earlier, reading <letter> read: \"<old text, squeezed, first 200 characters>\"".
- T4 "  - what may help you answer, from the factory's helper, who read the sources for it (written <YYYY-MM-DD>; it does not say which
  answer is right - you decide): <note words, squeezed, whole>"
- T5 "  - the requirement it is about (R-8): \"<requirement text, first 240 characters>\" — work/requirements-register.md"
- T6 "  - where these readings come from is not recorded, and the factory has found nothing more than what is shown here; answer from what
  you know of the product, or in your own words."
- T7 `reading_origin_words`: acceptance_criteria "the acceptance criteria"; description "the ticket's description"; comment "a comment on
  the ticket"; parent_ticket "the parent ticket"; code "the code"; test "an existing test"; precedent "an earlier confirmed behaviour";
  person "what you said earlier"; claim "the change under test (before / now)"; attachment "an attachment". Printed `(from <words>)`; an
  unknown word prints `(from: <word>)`.
- T8 — dropped (B4).
- T10 conductor: "For each `open_questions` finding above: when `controller.py rework --stage S2 --role qa-requirements-tester` is refused
  by the repair cap, do not try again. Read the sources and write what helps the person answer that question - where each reading comes
  from, the source line, what each answer changes, an answered question it rests on - with `question_register.py --task <T> --note <id>
  --words-file <file> --by conductor --where \"stage ran\"`. Do not say which reading is right: the person decides. Do not rewrite the
  question; its card shows your note."
- T11 `conductor.md` row: "| A question the person was shown at the last question stop and left unanswered, whose words show they could
  not tell what it asks | `question_register.py --task <T> --reword <id> --question-file <file> --by conductor --where \"stage ran\"` (a
  JSON object: `question`, `why`, and optionally `readings` as the same number of texts; refused while plan rows or cases answer it by
  letter - then the question text only); the id stays, the card shows the earlier wording |"
- T12 designer "When to ask", new first bullet: "- Before you raise, read `Questions already asked of the person` in your brief and the
  answers above it. A question there that already asks yours: answered -> the Then's oracle is `person` with its id, and the value is the
  one its answer gives; open -> the Then is `unknown` with its id and a `question_thens` entry; raise nothing new. When the case critic
  names a question you raised as a repeat, point every Then at the earlier id and list it once in `question_repeats` with a one-line
  `why`; the driver records it and the person is asked once (it is refused while a plan row or another case still rests on it). A question
  the brief marks `shown to the person at the last question stop` that your cases rest on and that went unanswered may be asked again in
  clearer words through `reword_questions` (the same meaning; change the readings only when no plan row answers them by letter)."
- T13 critic "Where bugs hide": "- **A question asked twice.** A question the designer raised, or a `raise_questions` entry, that asks
  what an open or answered question in `Questions already asked of the person` already asks: a finding naming both; the designer repairs
  it in its round. A merge the list shows `merged by qa-case-designer` that you judge wrong is a finding too." "When to ask", appended to
  `:133`: "Read that list first: an answered question there is your source, an open one is named by its id; raise nothing new. A question
  you asked that the brief marks shown and unanswered may be asked again in clearer words: an item of `questions[]` with `rewords: <id>`,
  `question`, `why` (and `readings` only when nothing answers them by letter)."
- T14 `question_note` for a repeat shown again: gone "it was marked as the same question as Q7, which the factory no longer has, so it is
  asked here"; cycle "it was marked as the same question as another one that points back to it, so it is asked here"; target_changed "it
  was marked as the same question as Q7, whose words have changed since, so it is asked here"; its own words changed "it was marked as
  the same question as Q7, but its own words have changed since, so it is asked here".
- T15 report note: " (raised twice in this story; this one question covers both)".
- T16 retro section `## Questions merged as one` (N5): one line per record: "- Q16 merged into Q7 by <declared_by in words> at <stage>
  (<at>): \"<Q16 text, 200>\" / \"<Q7 text, 200>\"; why: <why, 200>; now: <standing>"; none: "- none: no question was merged in this
  story"; unreadable: "- the question records could not be read, so merges are not known".

### D7 — the retro record and its readers (owner 14.11, B2; AR-22)
- Producer: `declare_repeat` (D3 step 5) — the `repeat` record in `work/question-answers.jsonl` with `texts`, `declared_by`, `by`,
  `stage`, `at`, `words` (the why), `same_as`, `row_hash`, `target_hash`. The answers file is append-only: an undone merge (reopen, answer)
  keeps its record.
- Reader 1 (in run): `_resolve_repeats` (last record per id).
- Reader 2 (retro): `QR.repeat_records` -> `retro_numbers.numbers` key `merged_questions: {"records": [...], "unreadable": bool}` (only
  when the register is present; absent for an older story, as `knowledge` is `:2220-2227`) -> `render` T16 via NEW
  `merged_question_lines`. The retro analyst reads `retro-numbers.md` (`brief_pack.py:105`).
- Reader 3 (forge, after the run): the collector — E2 tails the answers file (`collect-sets.json:53`) and C4 copies
  `retro-numbers.json` (`:46`): an existing data row each, so NO collector change and no new mechanism (F18). The texts travel inside the
  record because E1 carries the readiness rows as they stand at collect time, not as they stood at the merge.
- Not recorded for the retro: rewords (they stay on the row, `reworded[]`, which E1 carries) — small choice §8.

### D8 — error direction of functions put in a more responsible role (designer rule 1, PROJECT.md 6 (в))
- `is_open` (decides what a person is shown) gains a HIDING branch through `hidden_repeat`. Allowed error: show. Forbidden: hide a row
  whose target is not an existing, resolvable, unchanged row, or whose bytes changed since the declaration, or on which anything else
  rests (B1 at write). Awkward inputs that must stay shown: `follows` missing (a dict built outside `load`), `same_as` naming itself, a
  missing id, a row skipped by `load` (no id, not an object, duplicate id — the first is kept, so a repeat of the duplicate resolves to the
  first), a 2- and 3-cycle, a record with no `row_hash` (`changed_since_answer` None), no `target_hash`, a row changed since, a target
  changed since, a non-string `same_as`, whitespace around ids (stripped as `load` strips).
- `dependants` (gates a merge and the readings of a reword). Allowed error: report a dependant that is not one (refuse). Forbidden:
  miss one. Awkward: plan absent (no rows: none), plan unreadable (`unknown`), cases unreadable (`story_cases` problems -> `unknown`), a
  case whose `then_oracles` line does not parse (`unknown`), an `if_answered` key with whitespace, an id inside `reason` only (counted,
  as `row_open_questions` `:611-619` counts it).
- `contract.then_oracle_errors` `person` (gates a case). Allowed error: refuse. Forbidden: accept an answer that does not hold. Awkward:
  changed since, `before` value missing (`before_value_needed`), deferred, `with_designer`, `named`, `not_needed`, a repeat, no hash (holds).
- `unknown` relaxation (F-3): allowed error: refuse. Awkward: `readings` not a list, one reading, 27 readings, a non-dict reading, a blank
  `reading`, `readings_unnameable` true, a resolved repeat (refused with its target), a before/now row with a broken side (still refused).
- `last_stop_shown` (gates a reword). Allowed error: "not shown" (refuse the reword). Awkward: no driver state, a `shown` that is not a
  dict, a hash that is not a string, a stop of another stage (any stage counts: the bytes are what matter).
- NOT reused: `contract.question_errors` stays the rehearsal's and the reword's shape check; `_shown` stays the (case, Then) check.

## §4. Edges (each with the invariant it protects)
| edge | behaviour | invariant |
|---|---|---|
| empty / absent register | brief T1 "none" line; no repeat resolvable; `--repeat`/`--reword`/`--note` refused naming the file | nothing is hidden or written without a register |
| a row unreadable (not object, no id) | skipped by `load` as today; a repeat pointing at it is `gone` -> shown | a hidden row always has a readable target |
| a Q id cited that does not exist | oracle refused (`contract.py:1720`); `same_as` unknown refused at write; deleted later -> T14, shown | an id never resolves by guess |
| answer whose row changed since | `person` refused; brief omits it (as today); the repeat stays hidden behind a target whose ANSWER went stale (the target is asked again), but a target whose ROW changed shows the repeat again (m3) | a stale answer is never a source; a hidden row never sits behind other words |
| a declared repeat with dependants (B1) | refused, naming each plan row / case; nothing hidden; bare plan refs are repointed first; a dependants read that fails -> refused | the person's one answer reaches everything that rests on the hidden id |
| plan approved at gate A | `repoint_bare_ref` writes nothing (the approval ban); the ref stays a dependant -> refused | code never changes the plan the person approved |
| repeat of a repeat / cycle | chain resolved to the end; cycle refused at write; a cycle made by a race -> every member shown | the reader alone keeps it safe (F4 race) |
| race: two writers declare / reword at once | records append under the lock per line; last wins; a cycle from the pair -> shown; a reword and a merge racing: the merge's `target_hash` no longer matches -> shown | no interleaved line, no hidden row behind changed words |
| `question_repeats` malformed / ids absent / `same_as` = `raise` or a not-yet-written id / `why` blank (m9) | a line from the exit step (`question_notes`); key kept; nothing recorded | a failed declaration errs toward asking |
| replay of the same declaration | no-op (the row is already a hidden repeat of the same target); key dropped | idempotent |
| person answers the hidden repeat | recorded; status `answered`; the retro record reads "answered by the person" | the person's word wins (P13) |
| a reworded row that had an answer | refused unless the last record is a reopen (status `open`) | an answered question is never re-asked in new words by the factory |
| a second reword before a showing | refused (one reword per showing) | roles never re-reword each other unseen |
| a reword of a row others answer by letter | readings refused, question text allowed | a reading's meaning never changes under another role's letters |
| a reword by a role whose work does not cite the id | refused, "raise or cite it instead" | only a role that needs the answer rewords (owner 14.11) |
| a reword of a target of hidden repeats | the repeats are re-declared with the new hash (F-13) | two questions are never shown at one moment because of a reword |
| S2 tester republish after a reword | reword lost; answers on the reworded bytes asked again; repeats behind it shown | toward asking (accepted, D4) |
| brief over 30 KB | the by-range note (FV1-4); nothing cut (F-2) | the person's words stay first |
| card with no helping data | T6 | an unknown is said, never a bare defect line |
| note for other bytes | not shown (row_hash differs) | a note measured on other bytes never counts |
| note size | refused AT 2001 characters, accepted AT 2000; 0 / blank refused | the card is a card |
| note with a plugin path / field name | refused by `human_text.problems` | the person never reads our internals |
| rehearsal finding about a hidden repeat | not raised | no defect line about a question nobody is shown |
| retro with no merge / unreadable answers file | T16 none / unreadable line | an unknown is never "none" |
| reword text / readings size | the `contract.question_errors` limits (unchanged); `why` blank refused | — |
- TEMPORAL (both worlds): a story recorded before the change has no `repeat` record, no `note` line, no `reworded`, no `question`/`on_card`
  key on findings, no `question_repeats`/`reword_questions` in cases or plan rows, no `rewords` items: every reader behaves as today except
  (i) `(from ?)` -> T7/no parenthetical, (ii) briefs gain T1 at the next dispatch, (iii) `person` on a stale answer is refused at the next
  validation of that case (a case validated before stays pinned; the next S4 exit re-validates). The new world is created by the first
  `declare_repeat` (S4 raise step or conductor CLI), the first `reword` (any carrier), the first `--note`. An old finding without the keys
  -> `unrepaired_text` prints its message as today. A `repeat` record read by a package BEFORE N1's vocabulary row (a downgrade) is
  `invalid`, set aside, and the row is shown (F3) — toward asking. A driver state from before FV1-3 has no `question_stop.shown`: no reword
  is possible until a stop records one.
- POSITIONAL: P1 `is_open`: the repeat branch after the not-a-dict check and before `return True`; every other status's result unchanged.
  P2 `still_open`: inside `if mine is not None`, before `QR.settled(mine)`; a row with no register match is listed. P3 `raise_pending`: the
  filter becomes "any of `raise`, `question_repeats`, `reword_questions` in content"; per case: `raise_for_case`, then `repeats_for_case`,
  then `rewords_for_case`; write and re-pin once if the text changed; a case with none of the three is never read further or written.
  P4 `question_card`: T2/T3 right after `status_note`; H5/H6 after before/now; T6 after the readings; the answer line stays LAST (GW1-32).
  P5 `render`: the new section after the person's words, before the approach block. P6 `unrepaired_text`: the filter runs before the dedupe
  and the direct-checks-first sort, which are unchanged; the header and the gate-decision line unchanged. P7 `conductor_text`: T10 after the
  findings, before the closing `continue`/`ask_person` paragraph, which stays last. P8 `check_open_questions`: the hidden-repeat skip right
  after the register-settled skip `:1993`, before `question_errors`. P9 `raise_from_handoff`: `rewords` items are taken out BEFORE the
  `role_question_errors` loop, so they never enter the all-or-nothing refusal; executed AFTER the raises (a `rewords` naming an id raised in
  the same form is then found). P10 `project_plan`: `_reword_plan_entries` after `_raise_new_questions` and before `_write_plan_rows`; under
  the same approval ban (approved -> not executed, a note).

## §5. Nodes (topic: one code critic after the last node; N1 first, then N2, N3, N4, N5 in parallel)

### N1 — the register: `repeat`, `reword`, `note`, `dependants`, `asked_for_brief`, the S4 raise step, the handoff item, the bare-ref repoint  [builder -> critic]
given: this spec §0-§4; `design/factory-rules.md` whole; `plans/builder-rules.md`; `question_register.py:84-1800`; `critic_rollcall.py:739-779,
1160-1182`; `planning_contract.py:598-660, 2934-3073` (read for `repoint_bare_ref`; `_plan_state`, `_plan_row_for_write`, `_write_row_state`
reused); `gate_brief.py:2471-2540` (`story_cases`, read-only); `contract.py:1041` (`front_line`), `then_oracles_from_text` (read-only);
`driver_dispatch.py:1660-1672` (the `question_stop` shape, read-only); `design/state-exits.md`; `scripts/tests/fixtures/judgment-census.json`;
`test_question_register.py` (rows near `:1560-1630`, `:1840-2010`)
owns:
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n1\ai-packages\qa-factory\scripts\question_register.py (`_answers`, `_merge`, `load`, NEW `_resolve_repeats`, NEW `hidden_repeat`, `statuses_for`, `is_open`, `record` (keywords `same_as`, `declared_by`, `target_hash`, `stage`, `texts`), NEW `declare_repeat`, NEW `dependants`, NEW `repeats_for_case`, NEW `rewords_for_case`, NEW `reword`, NEW `record_note`, NEW `last_stop_shown`, NEW `asked_for_brief`, NEW `repeat_records`, NEW `origin_words`, `raise_from_handoff`, `vocabulary` (validate the new rows), `_VALUE_OPTIONS`, `_ALL_OPTIONS`, `main`, module docstring)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n1\ai-packages\qa-factory\references\question-vocabulary.json (`repeat` in two lists; `reading_origin_words` + note; `reword_own_artifacts` + note)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n1\ai-packages\qa-factory\scripts\critic_rollcall.py (`raise_pending`; the O4 block of `main` `:1170-1182`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n1\ai-packages\qa-factory\scripts\planning_contract.py (NEW `repoint_bare_ref` only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n1\ai-packages\qa-factory\design\state-exits.md (one row: `repeat`, exits `--reopen`, the person's answer, target gone/changed/cycle)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n1\ai-packages\qa-factory\scripts\tests\test_question_register.py (new rows)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n1\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (rows for the three new units; `blocking_per_role.conductor` 761 -> 764)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n1\ai-packages\qa-factory\changelog.d\fv1-9-question-repeats.md
non-goals: no card/brief/report/retro text (N2, N3, N5); no text comparison of questions; no letter mapping; no change to token reading
(`parse_choices`, `_only_tokens`, `record_answers`: FV1-13's); no renumbering; `with_designer` untouched; no driver_dispatch change (the
stop already saves `shown`); no collector change.
edges: §4 rows 1-16, 20-21, 25; TEMPORAL; P1, P3, P9.
DoD rows (`test_question_register.py`, each a table where it says so):
`fv19_repeat_hidden_while_target_resolves` (Q16->Q7 open: Q16 not open, Q7 `repeated_by` [Q16]; target answered then its answer goes stale
-> Q16 still hidden (m8); target row changed -> Q16 shown, `repeat_problem` `target_changed` (m3));
`fv19_repeat_of_settled_listed_for_brief` (Q7 answered: `asked_for_brief.repeats` [{Q16, Q7, True, declared_by}]);
`fv19_repeat_unresolved_shown` (table: same_as gone / 2-cycle / 3-cycle / own row changed / no hash / no target_hash / `follows` missing /
non-string same_as -> open);
`fv19_repeat_write_refusals` (table: no same_as, self, unknown id, cycle, settled row, deferred row, blank why, register unreadable);
`fv19_repeat_refused_with_dependants` (table: plan row with `if_answered[Q16]` -> refused naming TS-n; another case with `then_oracles`
`unknown:Q16` -> refused naming it; `question_thens` entry -> refused; plan row with a bare `question_refs` Q16 -> repointed to Q7 and
declared; approved plan with a bare ref -> refused; cases unreadable -> refused);
`fv19_repeat_replay_noop`; `fv19_person_answer_beats_repeat`; `fv19_reopen_undoes_repeat`;
`fv19_repeat_records_history` (two records, one undone by an answer: both returned, `standing` "merged" / "answered by the person", texts as
they stood after the target was reworded);
`fv19_reword_keeps_id` (id, `reworded[0].was`, `was_readings` only when readings changed, hash changed, `changed_since_answer` False, no new row);
`fv19_reword_refusals` (table: answered, not_needed, deferred, repeat, with_designer, not shown at the last stop, shown on other bytes,
second reword before a new showing, readings count, blank reading, unchanged text, `question_errors` fails, blank why, register unreadable);
`fv19_reword_who_may` (table: conductor ok; case designer with a case citing Qn ok / without refused; planner with a plan row citing Qn ok;
acceptor with `asked_by` = itself ok / another refused);
`fv19_reword_readings_frozen` (designer: plan row `if_answered[Qn]` -> readings refused, question-only accepted; planner: case
`question_thens` -> refused; conductor: any -> refused; dependants unknown -> refused);
`fv19_reword_carries_repeats` (target of a hidden repeat reworded -> repeat still hidden, a new record with the new `target_hash`);
`fv19_reword_after_reopen_allowed`;
`fv19_note_bound_to_bytes` (note shown on same bytes; dropped after a row change; AT 2000 / BEYOND 2001; blank; a plugin path refused;
`kind: note` not counted in `skipped`);
`fv19_asked_for_brief_empty_and_unreadable` (+ `shown_at_last_stop` from a driver state fixture; no driver state -> False);
`fv19_raise_pending_records_repeats` (a case with only `question_repeats` is read; recorded, key dropped; refused -> key kept, a
`question_notes` line; a case with none of the three keys is not written (mtime unchanged));
`fv19_raise_pending_rewords` (`reword_questions` executed, entry dropped; refused entry kept with a line);
`fv19_handoff_rewords_item` (a `rewords` item rewords; a refused one is a `reword_problems` line and the other entries are raised; a
malformed one never refuses the form);
`fv19_origin_words_unknown_default`; `fv19_cli_repeat_reword_note` (each flag: exit 0 / refusal exit 2 with the expected text; exactly-one-
operation rule names the three new operations).
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/question_register.py ai-packages/qa-factory/references/question-vocabulary.json ai-packages/qa-factory/scripts/critic_rollcall.py ai-packages/qa-factory/scripts/planning_contract.py ai-packages/qa-factory/design/state-exits.md`
(slow files it prints are judged by CI); grep `follows` and `repeat_history` in `scripts/*.py`: only their one reader (AR-13); grep the
literal `"repeat"` status and the two role names of `reword_own_artifacts` outside the register and the data file -> none (AR-1);
`test_judgment_census.py` green with the conductor ceiling at 764 — if the scan reports another count, STOP and return the number as a
question (m7), never raise it further.
siblings: `statuses_for` (the publish twin of `load`) gets `_resolve_repeats` too; the S3 claim projector writes rows through
`_question_row` and never declares repeats (n/a: no carrier there); `_raise_new_questions` is N4's twin carrier.
architecture: AR-1, AR-13, AR-14, AR-20, AR-22, AR-23, AR-25, AR-28 -- kept as §1.1. judgment: sameness and meaning stay with the roles,
their critics and the forge (retro); code checks ids, bytes, showings and dependants only (xref/shape).

### N2 — the card, gate A, the rehearsal, the report, the conductor's turn  [builder -> critic; after N1]
given: this spec; N1's merged diff; `design/factory-rules.md`; `plans/builder-rules.md`; `references/human-questions.md`; `gate_brief.py:2734-2830,
4160-4252`; `driver_gates.py:698-815`; `gate_preflight.py:1929-2022`; `report_facts.py:2635-2656, 4143-4168`; `references/conductor.md:1-44`
owns:
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n2\ai-packages\qa-factory\scripts\gate_brief.py (`question_card`, NEW `_help_lines`, `question_note`, `still_open`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n2\ai-packages\qa-factory\scripts\driver_gates.py (`unrepaired_text`, `conductor_text`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n2\ai-packages\qa-factory\scripts\gate_preflight.py (`check_open_questions` only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n2\ai-packages\qa-factory\scripts\report_facts.py (`_questions`, `_r_questions`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n2\ai-packages\qa-factory\references\conductor.md (row T11)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n2\ai-packages\qa-factory\scripts\tests\test_gate_question_form.py (new rows)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n2\ai-packages\qa-factory\scripts\tests\test_report_facts.py (new rows; slow, judged by CI)
non-goals: no new rehearsal check; `question_errors` unchanged; no S2 rework road; no change to `question_stop.py` (cards arrive through
`open_cards` unchanged); no relating of rows by code; no person door to split a merge and no conductor row for it (owner 14.11).
edges: §4 rows 3, 4, 17-19, 21; TEMPORAL (old finding without the keys); P2, P4, P6, P7, P8.
DoD rows: `test_gate_question_form.py`: `fv19_card_help_fields` (table by field: H1..H7 each present alone -> its line; H5 suppressed
when H1 quote exists); `fv19_card_no_help_line` (no H1/H2/H5/H6, `from` blank -> T6, no `?`); `fv19_origin_words_on_card` (every
READING_ORIGINS word -> T7 words; unknown -> `(from: x)`); `fv19_target_card_says_also_raised` (T2; no twin text, no split door);
`fv19_card_says_asked_again` (T3, cut AT 240 / BEYOND 241 with "..."; changed readings lines); `fv19_note_on_card` (T4 with date and the
"you decide" clause); `fv19_repeat_shown_again_note` (T14 per `repeat_problem`); `fv19_still_open_skips_hidden_repeat` (+ unmatched row
listed); `fv19_gate_top_skips_carded_question` (table: `on_card` True -> left out; `on_card` False -> printed; old finding without keys ->
printed; header unchanged); `fv19_rehearsal_skips_hidden_repeat` (`check_open_questions` raises no finding for it; tags `question`/
`on_card` on the others); `fv19_conductor_text_note_door` (T10 present only with an `open_questions` finding; closing paragraph last);
`fv19_human_text_passes` (`human_text.problems` empty on the new cards). `test_report_facts.py`: `fv19_report_lists_target_once` (Q16 absent,
Q7 note T15; unresolved repeat listed).
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/gate_brief.py ai-packages/qa-factory/scripts/driver_gates.py ai-packages/qa-factory/scripts/gate_preflight.py ai-packages/qa-factory/scripts/report_facts.py ai-packages/qa-factory/references/conductor.md`
siblings: `question_stop.open_cards`/`batch_text` take the same card (axis 5, no edit); `kept_answer_text` prints no question card (n/a).
architecture: AR-13, AR-16, AR-17, AR-22, AR-23, AR-27 -- one predicate, one card form, the existing seam, fields with readers, the empty
outcome said, the target carries the merged question to the report. judgment: none added (data rendering).
Hot list (PROJECT.md «Командная работа» п. 3): `gate_preflight.py` — function list `check_open_questions` (D-0048).

### N3 — briefs, oracle refs, contract text, charters  [builder -> critic; after N1; after stage-critics A2 for `qa-case-critic.md`]
given: this spec; N1's merged diff; `design/factory-rules.md`; `plans/builder-rules.md`; `brief_pack.py:1735-1852, 4515-4580`;
`contract.py:1599-1742`; `references/artifact-contract.md:126-150`; `agents/qa-case-designer.md`; `agents/qa-case-critic.md` (as A2 left it);
`stages.json` (S2/S3 `acceptance_by`, read-only)
owns:
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n3\ai-packages\qa-factory\scripts\brief_pack.py (`question_answer_lines`, NEW `asked_question_lines`, the section lines inside `build.render`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n3\ai-packages\qa-factory\scripts\contract.py (`then_oracle_errors`: the `person | unknown` branch only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n3\ai-packages\qa-factory\references\artifact-contract.md (`then_oracles` form paragraph; paragraphs for the case keys `question_repeats`, `reword_questions`, the plan-row key `reword_questions`, the `rewords` item of a form's `questions[]`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n3\ai-packages\qa-factory\agents\qa-case-designer.md (T12)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n3\ai-packages\qa-factory\agents\qa-case-critic.md (T13)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n3\ai-packages\qa-factory\agents\qa-test-strategist.md (one bullet: the plan-row `reword_questions`, the same meaning, readings only when no case answers them by letter)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n3\ai-packages\qa-factory\scripts\tests\test_oracle_provenance.py (new rows)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n3\ai-packages\qa-factory\scripts\tests\test_brief_pack.py (new rows; slow, judged by CI)
non-goals: no cut of any brief part; no change to `answers_for_brief`'s shape; no new role tool; `role-commands.json` unchanged (roles run
no register command). The S2/S3 acceptor charter: if `stages.json` names an S3 acceptor other than `qa-case-critic`, the T13 `rewords`
sentence goes into its charter's `questions[]` line too — that charter path is then named back to the Lead as "needed beyond the
manifest" before it is edited (owns is normative).
edges: §4 rows 1, 3, 4, 18; TEMPORAL (iii); P5.
DoD rows: `test_oracle_provenance.py`: `fv19_person_needs_holding_answer` (table: settled ok; changed since / before missing / deferred /
named / not_needed / repeat refused with the door); `fv19_unknown_on_reading_question` (table: 2 readings ok; 26 ok; 27 refused; 1
refused; not a list refused; a non-dict reading refused; a blank reading refused; `readings_unnameable` refused; before/now broken
refused); `fv19_unknown_on_repeat_points_at_target`. `test_brief_pack.py`: `fv19_brief_lists_question_text`; `fv19_brief_lists_open_rows`
(repeat on its target's line with `declared_by`; shown/reworded marks; empty; unreadable); `fv19_section_after_person_words`. Charter and
contract keys quoted verbatim (doc-dispatch witness, CLAUDE.md rule 11: keys from T12/T13 and the four contract paragraphs written before
the run, script attached, one negative control); `role_load.py --all` before/after named (AR-11 change check).
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/brief_pack.py ai-packages/qa-factory/scripts/contract.py ai-packages/qa-factory/references/artifact-contract.md ai-packages/qa-factory/agents/qa-case-designer.md ai-packages/qa-factory/agents/qa-case-critic.md ai-packages/qa-factory/agents/qa-test-strategist.md`
siblings: every other role brief gets the section by the same call (axis 34); `validate_artifacts.check_then_oracles` passes the view
unchanged.
architecture: AR-10, AR-13, AR-29 -- told before the work, one reader, judgment in the charters. judgment: "a question asked twice" and
"a reword kept the meaning" are critics' findings (judgment, accepted by the critic tier); code checks refs only.

### N4 — the planner's reword carrier  [builder -> critic; after N1]
given: this spec §3 D4, §4; N1's merged diff (`QR.reword`); `design/factory-rules.md`; `plans/builder-rules.md`; `planning_contract.py:3247-3377`;
`test_s3_strategist_rounds.py` (the `project_plan` cases)
owns:
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n4\ai-packages\qa-factory\scripts\planning_contract.py (`project_plan`, NEW `_reword_plan_entries`; NOT `repoint_bare_ref` (N1's, merged before))
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n4\ai-packages\qa-factory\scripts\tests\test_s3_strategist_rounds.py (new rows)
non-goals: no new plan check at the S3 exit (the key's shape is checked when executed, problem lines only); no change to `new_questions`.
edges: §4 rows 12-16, 2 (approved plan); P10; TEMPORAL (a plan with no key passes through unchanged — `declared`/`stamped` logic `:3339-3341`
gains "or a row carries `reword_questions`").
DoD rows (`test_s3_strategist_rounds.py`): `fv19_plan_reword_entry` (table: an entry rewords Qn and leaves the row; a refused entry stays with
a note line and the plan IS written for the rest; an approved plan executes nothing and notes it; a plan with no key is not written).
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/planning_contract.py`
siblings: `_raise_new_questions` (the raise carrier of the same role, axis 34); `raise_pending`/`raise_from_handoff` (N1's carriers).
architecture: AR-14, AR-22 -- the plan's code writer, the key has a reader in the same topic. judgment: none added.

### N5 — the retro marks merged questions (owner 14.11, B2)  [builder -> critic; after N1]
given: this spec §3 D7, T16; N1's merged diff (`QR.repeat_records`); `design/factory-rules.md`; `plans/builder-rules.md`; `retro_numbers.py:2115-2300,
2648-2800`; `test_retro_numbers.py`
owns:
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n5\ai-packages\qa-factory\scripts\retro_numbers.py (`numbers`, `render`, NEW `merged_question_lines`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-n5\ai-packages\qa-factory\scripts\tests\test_retro_numbers.py (new rows)
non-goals: no collector change (E2/C4 already carry it, F18); no judgment of whether a merge was right (the forge's, after the run).
edges: §4 row 22; TEMPORAL (an older story: no key, the section absent — as `knowledge`); a `repeat_records` exception -> `{"problem": ...}`
and the unreadable line, never a raise of the retro.
DoD rows (`test_retro_numbers.py`): `fv19_retro_lists_merged_questions` (two records -> two T16 lines with texts as they stood and standing;
none -> the none line; unreadable -> its line; texts cut AT 200 / BEYOND 201).
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/retro_numbers.py`
siblings: `knowledge` block (the same "only when present" shape).
architecture: AR-22, AR-23, AR-27 -- the record has its reader, the empty outcome said. judgment: none added.

Order and parallelism (brief item 6): N1 first — it now also owns `planning_contract.repoint_bare_ref` (B1) and reads `planning_contract`
plan state and `gate_brief.story_cases` read-only for `dependants`; then N2, N3, N4, N5 in parallel: N2/N3/N5 own disjoint files; N4 shares
`planning_contract.py` with N1 only by disjoint function lists and runs after N1's merge. `question_register.py` only N1. Hot list: only
`gate_preflight.py` (N2, `check_open_questions`). One code critic for the topic after the last node merges (R13-g). Each node stays
Sonnet-executable: file, function, behaviour, a test row per item, edges named.

## §6. Crossings and queue order
- FV1-3 (MERGED on `50d9012`, F17): owns `driver_dispatch.py`, `driver_machine.py`, `question_stop.py`, `audit_factory.py` — none here. Its
  shown hashes (`driver-state.json` `question_stop.shown`, saved `driver_dispatch.py:1668-1670`, passed `:1797-1798` to `record_answers`
  `:1906`) are what makes a stale answer to a reworded card fall to "asked again", and what `last_stop_shown` reads.
- FV1-13 (owns `question_register.py` token reading): its function list must exclude N1's (`main`, `_VALUE_OPTIONS`, `_ALL_OPTIONS`,
  `record`, `load`, `_merge`, `_answers`, `is_open`, `statuses_for`, `raise_from_handoff`); `record_answers` is FV1-13's and N1 does not
  touch it (m2's `:1005` reader is unchanged). Order FV1-13 / FV1-9 N1 in either order, the later merges main.
- Stage-critics A1a (`brief_pack.TRIED_READERS`, `stage_critic_names`, `FIRST_LOOK_KIND`): disjoint from N3's functions; parallel legal.
  A2 owns `agents/qa-case-critic.md` (`:30-33`, `:133` area) after TQ2-1 K1: queue `TQ2-1 K1 -> A2 -> FV1-9 N3`. A3: no shared file.
- TQ2-1 K2 (`brief_pack.case_concern_lines`): disjoint function. FV1-28/FV1-29 (`brief_pack.py`): name functions at dispatch.
- FV1-12 (S2 card `skills/qa-story/phases/s2.md`, `stages.json`): no shared file; if FV1-12 keeps an S2 critic, its brief gets T1 too and
  its form's `questions[]` takes the `rewords` item by the same `raise_from_handoff`.
- `retro_numbers.py` / `planning_contract.py`: any batch in work on them names functions at dispatch (D-0048); not hot files.

## §7. Forks
Decided (written into the nodes):
- F-1 (Lead, (a)) every brief carries the asked list.
- F-2 (Lead, (a)) no cut (FV1-4).
- F-3 (critic accepted (a), Lead) `unknown` on a reading question with no before/now: allowed with 2..26 dict readings, each with a
  non-blank `reading`, no `readings_unnameable`; a row with `before`/`now` still goes through `before_now_errors` (D2).
- F-4 (OWNER 14.11) who may reword: «любая роль которой нужен ответ» — designed as D4 (B3 (a)-(g)).
- F-5 (Lead, (a)) the note is a `note` record bound to `row_hash`.
- F-6 (OWNER 14.11, (a)) the declared repeat is hidden, its target's card says it was raised twice; ways out `--reopen` (conductor), an
  answer, an unresolved target.
- F-7 (Lead, (a)) the designer by a case key + the conductor by CLI, one function `declare_repeat`.
- F-8 (Lead, (a)) the cap unchanged; the conductor's note fills the help.
- F-9 (OWNER 14.11, closes the critic's question 1, B2) how the person splits a wrongly merged twin: «никак. фабрика отмечает слитые
  вопросы в ретро и мы смотрим потом на сколько решение было верным при анализе фабрики через коллект». No person door, no token, no
  conductor row; every merge is a durable record read by the retro (N5) and carried by the collector (E2/C4, unchanged); the case critic
  sees `declared_by` in its brief. (The Lead's earlier recommendation — free words read by the conductor and `--reopen` — is not built.)
- F-10 (OWNER 14.11, «да», closes the critic's question 2, B3 (b)) «роль которой нужен ответ» = a role whose OWN work cites the question
  id (D4 refusal 4); a role that only reads it in its brief raises or cites, it does not reword.
Returned (new in rev. 2; nodes written on the recommendation):
- F-11 (Lead; P31 one road) the reach of rewording = the reach of raising: case designer, planner, the stage acceptors whose form the
  driver raises (today the case critic), the conductor. Roles whose form is never raised (S1 scout, S2 tester's form, S5+ roles) reword
  nothing — they cannot raise either; the S2 tester rewrites its own rows by its publish. (a) as written — recommended: one road, the
  same carriers as raising; (b) widen raising AND rewording to every role's form at its acceptance (F-7 (b)'s cost: a driver step at every
  acceptance, a new node per stage). Covering the S5+ side costs a raise carrier for roles that today have none.
- F-12 (Lead) B1's bare-ref repoint: (a) `declare_repeat` repoints a plan row's bare `question_refs` entry (no branch, no reason mention,
  plan not approved) before the dependants check — recommended: every S4-raised question sits in its row's `question_refs`
  (`_name_in_plan_row`, F10), so without it EVERY S4 declaration is refused and the net is dead; no letter is mapped (AR-29); (b) pure B1:
  any naming refuses; the door is always the planner's rework (cost: one S3 rework per merge, or no merge).
- F-13 (Lead) a reword of a target of hidden repeats: (a) carry the repeats over (re-declare with the new hash) — recommended: R2 holds
  and the reword's meaning is judged by the stage critic; (b) refuse a reword of a target (cost: the questions asked twice are exactly the
  ones nobody may clarify); (c) let the repeats show again (R2 broken at the next stop).
- F-14 (Lead) critic re-pass: N4 (the planner's carrier, from F-4) and N5 (the retro reader, from F-9) are new nodes; the Lead judges
  whether they change the architecture (PROJECT.md «новая идея» step 6: a repeat pass only then). Recommendation: no full re-pass; the one
  code critic of the topic reads §7 F-11..F-13 with the diff.

## §8. Small choices closed by the designer
New reader `asked_for_brief` instead of a key on `answers_for_brief` (F6 pin); `follows`/`repeated_by`/`repeat_problem` computed at load,
never stored; hide only on `changed_since_answer is False` (stricter than `_holds`, as `closes` is); note cap 2000 characters; `was` cut at
240 on the card (stored whole); H5 only when no H1 quote; T7 unknown word printed plainly; every `repeat`/`note`/reword record uses `where`
= `stage ran` (an existing value; never shown to the person for these kinds) and `by` = the executor (`driver`/`conductor`), the declaring
role in `declared_by`/`role` and the stage in `stage`; `shown_at_last_stop` instead of a showing count (no producer of a count, F17); a
reword's refusals from a role carrier are lines, never a refusal of the carrier's step; rewords are not retro records (they stay on the row,
which E1 carries); T2 carries no twin text (a text with no move invites a split the factory will not make); the note prints its date (K6
(c): a note may go stale when a row it names is reopened); census `roles` of the new units = `["conductor"]`, as `_raise` (F19).

## §9. Brief vs carriers (reported, scope not widened)
- "the brief ceilings are real — state the cut rule": no ceiling since FV1-4 (F7); F-2.
- "the existing `replaces` / ref road" for an open question: blocked for S2 reading questions by `contract.py:1726` (F8); F-3.
- "related answered rows" on the card: no data relates rows; only the conductor's note can (D5, P27).
- The controller's cap refusal advertises free causes (`question_answer`, ...) a conductor could misuse for an S2 rework: noted, F-8.
- Analog: `_append` is a second jsonl appender beside `hooklib.append_jsonl_line` (`hooklib.py:600`, axis 29) — existing, not widened.
- A gate A showing is not recorded with its bytes (only the last question stop's are, overwritten at every stop): rewords count only stop
  showings. A durable showing record would let the brief carry a count — a new writer in the driver; not built.
- A question flawed by the rehearsal's measure is detected only at gate A, so no note reaches an earlier stop (D5): a stop-time check is a
  new detector; not built.
- The batch file on read-main shows FV1-3 «ожидает» although its code is merged (F17): a status lag for the integrator.
- Who the S3 acceptor is (`stages.json`) was not read; N3 handles it by a named rule (non-goals).

## Fix round (plan critic t-664, 14.11.2026)
- B1 -> D3 steps 3-4 (`declare_repeat` refuses while dependants remain, names each and the door), `QR.dependants` (one reader, also B3),
  `planning_contract.repoint_bare_ref` (F-12), §4 rows "declared repeat with dependants", "plan approved"; N1 `fv19_repeat_refused_with_dependants`;
  §1.2 row 1. T2 keeps its promise because of it.
- B2 -> decided by the owner (F-9): no person door; the critic's "tier above" kept where it needs no person: `declared_by` in T1 for the
  case critic, T13's "a merge you judge wrong is a finding"; every merge recorded for the retro (D7, N5, T16); §1.2 rows "hide" and "a merge
  was right". The critic's T2 text with the twin and `ask separately` is NOT applied (owner's word).
- B3 -> D4 whole: (a) carriers per role (case key, plan key N4, `questions[]` item, CLI); (b) who-may by data, `reword_own_artifacts`
  (F-10); (c) question-only by default, readings frozen under others' letters, `was_readings`, T3 prints them, one reword per showing; (d)
  the stage critic + the person; (e) `shown_at_last_stop` in the brief — DISAGREE with "a count": the only producer is the stop's
  `question_stop.shown`, overwritten at every stop (`driver_dispatch.py:1668-1670`), so a count has no producer without a new driver writer
  (§9); the boolean is what the reword rule needs; (f) attribution corrected: on `50d9012` FV1-3 is merged and `question_stop.shown` exists
  as a driver-state KEY (`driver_dispatch.py:1669`, read `:1797`), not as a function — the critic read the tree before the merge; (g) loss
  accepted toward asking (D4). N1 rows `fv19_reword_*`, N4 `fv19_plan_reword_entry`, N3 charters.
- B4 -> T8 dropped; `unrepaired_text` leaves out `open_questions` findings with `on_card` True (D5, P6); `check_open_questions` skips a
  hidden repeat via `QR.hidden_repeat` (P8); N2 owns `check_open_questions` whole (hot-list function named); N2
  `fv19_gate_top_skips_carded_question`, `fv19_rehearsal_skips_hidden_repeat`.
- m1 -> `QR.hidden_repeat`, the one predicate (D3, §1.1 AR-13); N1 DoD grep: `follows` read only by it.
- m2 -> F2 lists every `is_open`/`open_blocker` reader on read-main with its effect (+ `branch_accounting.py:2290`, `question_stop.py:307,
  333`, `driver_stage_plan.py:933`).
- m3 -> `target_hash` in the repeat record; `repeat_problem` `target_changed` -> shown with T14; N1 row in `fv19_repeat_hidden_while_target_resolves`.
- m4 -> T1 says "the answers above, under the person's words" (F7, `brief_pack.py:4529-4533`).
- m5 -> T7: person "what you said earlier", claim "the change under test (before / now)".
- m6 -> T6 "nothing more than what is shown here".
- m7 -> N1 DoD: `blocking_per_role.conductor` 761 -> 764 (three new blocking units: `declare_repeat`, `reword`, `record_note`); another
  count -> stop and ask.
- m8 -> the target-answer-goes-stale half added to `fv19_repeat_hidden_while_target_resolves`.
- m9 -> §4 row: `same_as` = `raise` or a not-yet-written id -> malformed line, nothing recorded.
- K2 R4 (first stop has no note) -> accepted and stated (D5), §9.
- K3 missing AR-24, AR-27 -> added to §1.1.
- K6 (a) T4/T10 say the note never picks a reading; (b) `record_note` runs `human_text.problems`; (c) the note's date printed (§8).
- K8 FV1-13 exclusion list extended (§6); the dependants reader named; census counts named; the role-form keys placed in N1/N3/N4.
- Code quality: the help lines in one helper `gate_brief._help_lines` (D5).
- F-3 -> written as the critic accepted it, with its predicate (D2, D8, N3 `fv19_unknown_on_reading_question`).
- Line numbers re-read on `50d9012`: `report_facts._questions` is `:2635` (rev. 1 `:2600`), `_r_questions` `:4143` (rev. 1 `:3960`),
  `brief_pack.question_answer_lines` `:1735`, `render` `:4523`; controller cap `:5653-5664`.

## §10. Reading trail
Rev. 1: FV1-3 spec `:440-654`; recon `20261114-fv1-9-questions-recon.md`; stage-critics spec `:184-273`; and the files listed there on `sc-a1a`.
Rev. 2 (read-main `50d9012`, HEAD read from `.git/worktrees/read-main/HEAD`): the critic verdict whole; this spec whole;
`question_register.py:84-483, 780-1029, 1105-1194, 1300-1479, 1580-1779`; `driver_dispatch.py:1640-1679, 1770-2039`; `driver_stage_plan.py:615-674,
918-957`; `driver_gates.py:690-819, 895-1019`; `gate_preflight.py:1929-2023`; `gate_brief.py:2471-2530, 2730-2829, 3745-3784`;
`contract.py:1696-1755`; `planning_contract.py:590-669, 2934-3093, 3247-3377`; `critic_rollcall.py:735-784, 1160-1189`; `brief_pack.py:4515-4584`;
`report_facts.py:2635-2664, 4143-4172`; `question_stop.py:245-259, 486-499`; `retro_numbers.py:2205-2239`; `collect_pack.py:340-399, 655-714`;
`references/question-vocabulary.json` whole; `references/conductor.md:1-44`; `judgment-census.json:1-30`; `human-questions.md:1-70`
(forge root copy); `architecture.md` change-check lines (grep).
Greps (Grep tool, read-main): `^def` lists of `question_register.py`, `question_stop.py`, `check_witness.py`, `branch_accounting.py`,
`retro_numbers.py`, `planning_contract.py` (question functions); `QR\.is_open\(|QR\.open_blocker\(|is_open\(q|row|question` over `scripts/*.py`
(the full reader list); `raise_from_handoff|from-handoff|raise_pending\(`; `raise_role_question|"--raise"` (only `driver_stage_plan.py:647`
runs the handoff raise; control: test hits); `record_question_words|free answer|kept_answer` (FV1-3 functions found); `shown=|"shown":` in
`driver_*.py`; `def take_question_answer|_unread_halt_or_review|unread|judged_reply`; `self.state_dir =`; `conductor\.md` in `scripts/*.py`;
`question_register|--reopen|^\|` in `conductor.md` (no register row; control: the table rows found); `QUESTION_LETTERS|LETTERS|readings_unnameable`;
`unrepaired`; `top=`; `rehearsal` in `gate_brief.py`; `project_plan\(` in tests (only `test_s3_strategist_rounds.py`); test-layers rows for the
seven test files and the section keys (`keep` `:36`, `keep_fail_at_entry` `:7132`, `quarantine` `:7164`); census rows of `question_register`,
`critic_rollcall`, `planning_contract`; `collect-sets.json` for `question|work/` and `"tail"` (E2 `:53`, E1 `:52`, C4 `:46`); `retro-numbers\.json`
producers; `questions\[\]` in package md/yaml/json (charter `qa-case-critic.md:133`, `brief-form.json`, `ahead-cards.json`).
Negatives with controls: no `def shown` in `question_stop.py` (its `^def` list read whole; `open_cards` found); no register row in
`conductor.md` (table read; `controller.py` rows found); no `repeat`/`note` status or CLI flag (files read; `with_designer`, `--reopen` found);
no other `--raise` caller (pattern found test hits).
Not read: `SIBLING_MAP.md` beyond headings (axes by heading); `stages.json` (S3 acceptor — handled by N3's rule); `driver_dialog.py`;
`test_s3_strategist_rounds.py` body (named by its `project_plan(` hits); `human_text.problems` body (called as the existing reader).
Not run: `scenario_walk.py` (no shell in this role).

## Owner's words on the forks (14.11.2026, verbatim) — recorded by the Lead

- F-4, who may reword an unanswered question — the owner: «любая роль которой нужен ответ». This is NOT the recommended (a): the
  door is open to every role that needs the answer, not to the conductor alone. Consequence for the fix round (Lead's reading): a role runs
  no register command, so a role rewords through its form (the carrier it raises through), executed by the same single writer `QR.reword`;
  the conductor's CLI row stays. One writer, two carriers — the shape raising and the repeat declaration already have (F-7 (a)).
- F-6, the declared repeat — the owner: «да» to (a): the twin is hidden, its target's card says it was raised again, reopenable.
- On the rule of fact F8 (`contract.py:1726`) the owner: «очень странное правило. Зачем оно?» — answered by the Lead: it is a side
  effect of P20's "show before / now" duty laid on every open (`unknown`) Then, not a rule against pointing at an S2 question. F-3
  stays with the plan critic.
- FV1-30b, what the person's word "the test was not run" lets go (explained by the Lead earlier) — the owner: «ок».
- B3 (b) (F-10), «роль, чья собственная работа ссылается на этот вопрос» — the owner: «да».
- B2 (F-9), how the person splits a wrongly merged twin — the owner: «никак. фабрика отмечает слитые вопросы в ретро и мы смотрим потом
  на сколько решение было верным при анализе фабрики через коллект».

## Lead decisions on rev. 2 (14.11.2026, acceptance of fix round t-668)

- F-11 = (a): the reach of rewording equals the reach of raising (P31, one road).
- F-12 = (a): `declare_repeat` repoints a plan row's bare `question_refs` entry before the B1 check; an approved plan with a bare ref is refused.
- F-13 = (a): a reword of a target carries its hidden repeats over (re-declared with the new hash).
- F-14: no second full pass of the plan critic. N4 (the planner's carrier) and N5 (the retro reader) follow the owner's words on B3 and
  B2 and add no new architecture; the topic's one code critic reads §7 F-11..F-13 and N4/N5 with the diff (PROJECT.md, new idea, step 6).
- The spec is ACCEPTED for dispatch: N1 first, then N2, N3, N4, N5 in parallel.
