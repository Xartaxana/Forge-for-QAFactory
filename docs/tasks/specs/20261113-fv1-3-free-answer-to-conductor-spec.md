# FV1-3 (then FV1-9): a free answer to a question pack goes to the conductor — DRAFT SPEC, rev. 2 (fix round)

pile: `live-run-fvf`, batch 1 | author: designer (draft 13.11.2026; fix round 13.11.2026 after the critic-on-plan verdict
`docs/tasks/specs/reviews/20261113-fv1-3-plan-critic.md`) | status: DRAFT rev. 2, awaiting Lead acceptance
Direction: the finding's proposal, taken by the Lead of the pile on 13.11.2026 (until the owner's word).
Binding principles: P22 / FR-48 / AR-17 (code asks the person only closed questions and reads only those; any free answer is
read by the conductor, never by code, never dropped), AR-24 (the person's words reach whatever acts on them, whole), FR-12 (no
phrase lists), P18 (the conductor's spend is the conductor's, journalled by `conductor()`).

**Facts re-taken on `C:\QAFactory\forge-repo\.claude\worktrees\read-main` = origin/main `e4ba384`** (`.git/worktrees/read-main/HEAD`
reads `e4ba3844b2974f3e1d723fc19872fc77a3313272`). Every `file:line` below is on that tree unless marked "root". The builder works in
`C:\QAFactory\forge-repo\.claude\worktrees\fv1-3` (the Lead creates it from origin/main); if origin/main has moved, the builder
re-finds each function by NAME (the names are the contract, the lines are a reading aid).

## 1. Architecture, rules, owners (AR-29; CLAUDE.md rule 10)

### 1.1 AR-n touched, and the change check each demands (written into the DoD of §4)

| AR | how FV1-3 touches it | change check in the DoD |
|---|---|---|
| AR-17 (one seam to the conductor) | the threshold stop's free answer reaches the conductor through `Driver.unread` -> `Driver.no_move` (`driver_conductor.py:852-870`, `:602`); no new conductor call site | grep of the diff: no new `self.conductor(` / `run_claude("conductor"`; the new member calls `self.unread(` only |
| AR-24 (words reach the actor whole) | the words are journalled (`answer_row`) and filed (`pending_words`, saved) BEFORE the hand-over; the conductor gets them whole through the answer's words file (`answer_file()`), and a rerun re-asks an open question before it resumes the role | rows `words-at-6000`, `words-beyond-6001`, `another-language` (words FILE byte-equal); row `rerun-no-answer` |
| AR-13 / AR-14 (one reader, one writer) | the one writer of answer records stays `question_register.record` (`question_register.py:862`); the conductor writes through its CLI (`:4-16`); code reads tokens only through `record_answers` (`:976`) | grep: no new writer of `work/question-answers.jsonl` |
| AR-15 / AR-19 (one survivor; stage twins) | the halt road (`_unread_halt_or_review`, `driver_machine.py:3814-3850`) and the question stop share ONE hand-over member, `register_words_to_conductor`, including the after-seam apply and the print-back; the ORDER differs on purpose (§3.2: the question stop files the words before the seam, the halt road after) and the rerun guard (§3.3) makes the two orders equivalent for the person | row `halt-road-shares-member`; the K1 assertions of `test_story_run_loop_b_answers.py:36-82` stay green unchanged |
| AR-20 (shrink-only ratchets only shrink; a raise is named) | `audit_factory.NO_MOVE_BASELINE` (A27, `audit_factory.py:1667`): in `_act_wait_existing_job` the row `('driver_machine.py','Driver._act_wait_existing_job','P','Person:questions'): 1` (`:1687`) is REPLACED by `(...,'P','builder:held_question'): 1`. Sum and `NO_MOVE_BASELINE_MAX` unchanged; one key appears, one goes. NAMED HERE as the one ratchet movement of this node | `test_audit_rules.py` green; the commit's `architecture:` line names the swap |
| AR-22 (every field read has a producer) | `state["question_pass_lines"][dispatch]` (producer: `take_question_answer`, now ALSO after a returned seam; reader: `question_resume_prompt` `driver_dispatch.py:1720`) | row `seam-raises`: lines saved on disk before the raise; K2: lines extended after the seam |
| AR-25 (every returned state has a move) | a seam question raised at a question stop is never lost to a rerun with no `--answer` (B2): `_act_wait_existing_job` re-asks it, with its `offered` tokens, before any resume | row `rerun-no-answer` |
| AR-7 / AR-29 (code is an instrument; code judges data) | code decides only "is every non-blank line a token and nothing unread" (shape) and prints what changed in the register (data); the meaning of free words is the conductor's | `parse_choices` diff-free |
| AR-28 (an unknown never becomes a pass) | a register that cannot be read gives `all_tokens: False` -> the words go to the conductor; a register that cannot be read back after the seam prints "could not be read back", never "nothing recorded" | rows `register-unreadable`, `printback-unreadable` |

FR sections walked: A (FR-2, FR-4, FR-48), B (FR-6/FR-9 the print-back line is P9 plain text; FR-7 the rerun re-ask carries the
"answered before" block of `ask()`; FR-8; FR-10: `BLOCKING_NOTE` `question_stop.py:464-465` becomes false and is rewritten), C
(FR-12, FR-13: no phrase list; the `where`/`by` values exist in `references/question-vocabulary.json:4`, `:17`), D (FR-59), E
(FR-37: the dry-run sentence `driver_machine.py:4143-4145` "(no conductor)" becomes false and is rewritten), G (FR-29/30: fixtures
build non-ASCII with `chr()`, no Cyrillic in the package). F: not touched (no money text; the conductor journals its own cost,
`driver_conductor.py:342-347`).

### 1.2 Checks added or altered: owner and census class

| check | where | owner | census class | census row |
|---|---|---|---|---|
| hand-over predicate `read["all_tokens"] and not read["unread"]` -> no conductor; else -> conductor | `take_question_answer` (call site) and `_unread_halt_or_review` (call site, today's) | data (code: shape of lines) | shape | none: routing, refuses nothing; A27 sees no Person/Stop/`py` in the member (`audit_factory.py:1642-1700`) |
| rerun guard: an open question about this dispatch (asked + question file) is re-asked before words filed for it resume the role | `Driver._act_wait_existing_job` | data (presence of two state halves) | shape | A27 row swap (AR-20 above); no judgment-census unit (re-ask, not a refusal) |
| print-back of what the register gained during the seam | new member | data (diff of `(status, reading, at)` per id) | shape | none (prints, refuses nothing) |
| judge (`judged_reply`) only when no register was read (`recorded is None`) | new member | data condition | — | `judgment-census.json:1004` (`judged_reply`, meaning/judgment) unchanged: the unit stays, it is called on fewer roads |
| "is this free answer a choice, and which letter?" | the conductor, via `question_register.py --answer` | judgment (conductor role). At run time NO tier above accepts it; the cure is data: the print-back shows each record the conductor wrote to the person (the intent owner), who can `--reopen`. Accepted by a tier above only at critic/acceptance of the factory's own changes, never per answer | meaning (role) | none (role, not code) |
| `record` refusing a different answer on a settled id (H6) | `question_register.py:862`, unchanged | intent | safety | `judgment-census.json:797`, unchanged |

## 2. Facts

### 2.1 The lost free answer, on real run data (measured; the logs are gitignored, `runs/.gitignore:3 *.log`)

Absolute paths (root checkout only; the logs exist nowhere else):
`C:\QAFactory\forge-repo\experiments\mybooks\factory-vs-free-agent\runs\factory-6.log`, `...\runs\factory-7.log`,
`...\runs\factory-8.log`. Tracked (also in every worktree): `experiments/mybooks/factory-vs-free-agent/answers/s4-questions-batch-1.md`,
`.../answers/s3-questions-batch-2-tokens.md`, `.../runs/factory-out/work/digests/S4-qa-case-designer-2.txt`.

- The person's answer, whole: `answers/s4-questions-batch-1.md:1-18` (re-read on read-main this round: 18 lines `Qn: <own words>`,
  ASCII, none a token; `:3` `Q3: The higher quantity wins (this is what the application's AUTH.md says).`).
- The driver on it, quoted (root, verified by the first draft and again by the critic, review §1): `factory-7.log:2`
  `answer for questions (S4 S4-qa-case-designer-2): Q1: A product ...`; `:4` `S4: recorded by code — no question answered by a token`;
  `:6` `resume S4-qa-case-designer-2 ...`; `:7` `S4: 18 question(s) are open ... their answer is the pass, no second stop`. No
  `conductor:` line between `:2` and `:7`.
- The role could not use them: digest `:13` "Neither the person's answers nor the case-version pins are in the register yet. The
  validator refuses person oracles for questions it counts as unanswered."; `:15` "Q3/Q12: the higher quantity wins on merge".
- The same pack asked again: `factory-7.log:32-38` `kind: questions`, `stage: S3` ... "Nothing in your answer settled these questions."
- Closed only by the operator's hand rewrite into tokens: `answers/s3-questions-batch-2-tokens.md:1-19`; `factory-8.log:23`
  `S3: recorded by code — Q1: b, Q3: a, ...`.
- The real S4 pack is 13 299 characters (`sed -n 93,235p runs/factory-6.log | wc -c`, the critic's run, review trail).
- Not measured: the live run's `work/question-answers.jsonl` (none on disk; first-draft trail, positive control the digest).

### 2.2 Code (read-main `e4ba384`)

- The answer dispatcher `driver_machine.py` `take_answer` `:3361-3637`: empty answer `Stop` `:3366-3367`; no open question `Stop`
  `:3368-3369`; `qtext` `:3376`; the seam's `offered` branch `:3540-3545`; the `questions` branch `:3554-3557` (comment `:3555-3556`
  "no conductor, no judge"; call `:3557`); the halt branches `:3558-3571`; `asked` cleared `:3633` (only when no branch raised).
  `take_answer` is called from `_run_guarded` `:1858` (def `:1852`) BEFORE the loop; a `Person` raised inside it reaches
  `except Person: return self.ask(person)` `:2017-2018` and the process ends.
- `driver_dispatch.py` `take_question_answer` `:1746-1789`: docstring `:1747-1756` ("Nothing here calls the conductor (FR-48)" `:1749`);
  whole-answer `go on`/`stop` `:1762-1780`; tokens recorded `:1781` — the return value of `record_question_words` is DISCARDED today;
  `apply_question_answers` + `question_pass_lines` `:1782-1784`; `answered`/`resume`/`pending_words` `:1785-1788`; journal row
  `answer_row` `:1789`. No `save_state()` inside; `take_answer` saves at `:3634` (only when no branch raised) and `ask()` saves on a raise.
- `record_question_words` `:1797-1830` (prints `:1825` "recorded by code — ..."; returns `record_answers`' dict; a register that
  cannot be read gives the empty dict with `all_tokens: False` `:1806`, `:1822-1824`).
- `record_halt_words` `:1832-1848` (records, journals `answer_row` `:1846`, applies `:1847`; POSITION INVARIANT `:1837-1838`).
- `apply_question_answers` `:1852-1881`: "never raises" (`:1858`, `:1878-1880`); idempotent per record (docstring `:1855`).
- `question_threshold` `:1590-1674`: applies `:1614`; sets `question_pass_lines` `:1659-1660`; pops `pending_words` `:1661`; raises
  `Person("questions")` `:1674`. `question_resume_prompt` `:1716-1725` pops `question_pass_lines` `:1720`. `resume_role` `:1028`:
  consumes `pending_words` before any Person it raises (`:1092-1094`, `:1105`).
- Import line `driver_dispatch.py:20`: `from driver_conductor import PATH_RE` (needs `MOVES_RULE, OWN_TOKEN_RULE, PRE_FILLED`).
  `driver_machine.py:22` imports the three; `PRE_FILLED` stays used there at `:4082` (import unchanged).
- THE PRECEDENT, `driver_machine.py` `_unread_halt_or_review` `:3814-3850`: `record_halt_words` `:3824`; all-token return `:3825-3827`;
  `judged_reply` `:3828` (on EVERY non-all-token road today); the `unread` text `:3831-3849` — "recorded by code: ..." `:3836-3837`,
  "Not read, still open: " `:3839` (false for an H6 refusal on a settled id), `--register-hash that --show prints` `:3843`, `MOVES_RULE`
  / `OWN_TOKEN_RULE` `:3846`, `qtext[:6000]` `:3847`, `PRE_FILLED + read` `:3848`; `pending_words` filed AFTER `unread` returns `:3850`.
- THE ONE SEAM `driver_conductor.py`: `unread` `:852-870` (`why=unread_answer`, words verbatim, `words_file = self.answer_file()`;
  docstring `:857` "the question without a call is the site's own, raised by a rerun with no `--answer`"); `no_move` `:602-627`;
  `_no_move` `:629-677` (cap -> `fallback_person` `:646-647`); `_conductor_text` `:679-687` (the conductor's refusal text =
  `lead` + moves section + the site's text); `_ask_conductor` `:557-564` (the only `self.conductor(`); `conductor` `:263` (cap
  `CONDUCTOR_CALLS_PER_BOUNDARY = 3` `:21`, raised `:268-272`; words-file note `:310-314`; the refusal text cut `refusal.strip()[:6000]`
  `:320`; words cut `NO_MOVE_WORDS_IN_PROMPT = 6000` `:29` with a pointer to the whole file `:322-323`; cost journalled `:342-347`);
  `_person_of` `:419-431` (a seam Person keeps `kind = state["kind"]` and sets `offered`, `options`, `words_file`, `why`, `block`);
  `judged_reply` `:911` (`judge_reply.intent`, the gate-intent list `judge_reply.py:27`, reply cut to 4000 `:48`, per the critic).
- `driver_dialog.py`: `ask` `:270-329` writes `asked` (with `offered`/`options` for a seam question `:321-329`); `already_answered`
  block "You have answered this exact question before" `:302-314`; `held_question` `:600-629` — THE helper that brings the open
  question back, rebuilt from the question file and `asked`, restoring `offered`, `options`, `words_file`, `why`, `block`, rows,
  cases; `after_close` `:643-648`; `reconcile_question` `:250-268`.
- `_act_wait_existing_job` `driver_machine.py:1445-1487`: `pending_words` -> `resume_role` `:1451-1454` FIRST; then the open-`questions`
  re-ask `:1455-1463` (`raise Person("questions", <file body>, ...)` — no `offered`); the halt/s1_review re-ask `:1484-1487`.
- `question_register.py`: module docstring `:41-43` ("a question it cannot read stays with the conductor"); `_merge` `:252-276` (a
  merged question carries `status`, `reading`, `at`, `where`, `words`, `record_row_hash` — NOT `by`); `parse_choices` `:631-733`,
  error direction `:655`; `record` `:862-921` (H6 text `:855-859`, names the `--reopen` door); `_only_tokens` `:957-973`;
  `record_answers` `:976-1023` (`all_tokens` `:1020-1022`); `_shown` `:1270`; `_raise` `:1282-1335` (replay return `:1319-1332`);
  `_question_row` `:1341`; `raise_for_case` `:1373` (`replaces` `:1411-1413`).
- `question_stop.py`: `:437` "or put your answer in your own words - the factory reads it as you wrote it."; `BLOCKING_NOTE`
  `:464-465` "... words alone go to the role, and the question is asked again."; read at `:522` and `driver_dispatch.py:1646`.
- `audit_factory.py`: A27 header `:1642-1666`; `NO_MOVE_BASELINE` `:1667`; rows `:1681` (`take_question_answer`, held_question: 2),
  `:1686-1687` (`_act_wait_existing_job`: `Person:?` 1, `Person:questions` 1); cap = sum check `:2354-2356`.
- Registries: `driver-layers.json:201` (`take_question_answer`), `:206`, `:207`, `:208` (`apply_question_answers`), `:781`
  (`_act_wait_existing_job`), `:832` (`_unread_halt_or_review`), `:1186` (state key `question_pass_lines`). `test-layers.json:5834`
  `test_story_run_loop_b_threshold.py` (keep, detector), `:5879` `test_story_run_loop_b_answers.py` (keep, detector), `:4167`
  `test_question_register.py` (keep, detector), `:6009` `test_story_run_s0.py`, `:6095` `test_story_run_s6.py`, `:9243`
  `test_question_stop.py` (QUARANTINED; it pins the old `BLOCKING_NOTE` at `test_question_stop.py:594`). `scripts/slow_tests.json`:
  `:137` threshold 25.0 s, `:135` answers 27.6 s, `:35` `test_driver_layers.py` 32.5 s, `:10` `test_audit_rules.py` 9.6 s.
- Tests that pin the OLD behaviour (B1), `test_story_run_loop_b_threshold.py`: `question_stop_road` `:28-141` — answer `:69-70`
  (`Q5 I do not know yet...`, `Q6: a, but only for the admin role`), `:92` "answer: no conductor was called (FR-48)", `:108` "resume:
  no conductor on the resume" (cumulative list, so it ALSO flips — the critic named `:92`, `:139`, `:326`), `:139` "the conductor
  stayed out of all of it"; `question_stop_fallbacks` `:290-328` (words `"Q1: a\nand please keep the admin cases apart"` `:293`),
  `:326` "the conductor stayed out". Unaffected: `question_stop_loop_moves` `:331-369` (`:362`, all tokens), `question_stop_edges`
  `:187-287` and `question_stop_share_and_limits` `:144-184` (free words, but no conductor assertion).
- `story_run_loop_b_common.py` `QStub` `:24-81`: `d.conductor` stub returns `continue` and records its positional args (`:55`; `a[0]`
  is the conductor's refusal text BEFORE `conductor()`'s cut); `d.py` runs real scripts except `stage_done.py`/`story_step.py`
  (`:49-54`).
- Direct callers of `take_question_answer` with non-token answers and no conductor stub: `test_story_run_s0.py`
  `s0_fenced_decision_notice` `:1120-1148` (calls `:1137`, `:1143`); `test_story_run_s6.py` `t261_the_integration_lines_of_the_driver`
  block (b) `:904-936` (calls `:923`, `:931`).

## 3. Design (FV1-3)

### 3.1 One member for "register words that are not all tokens"

New Driver member in `driver_dispatch.py`:

`register_words_to_conductor(self, kind, stage, dispatch, qtext, words, recorded, *, shown=None) -> list`

It holds the body that today is inline in `_unread_halt_or_review` (`driver_machine.py:3828-3849`) plus the after-seam half:

1. `read = self.judged_reply(qtext, words, kind) if recorded is None else ""` (fork F-9, decided: the judge runs only where no
   register was read — S1 review, a halt with no register; on the register roads its gate-intent reading, which errs toward
   `approve`, never reaches the conductor and its call is not spent).
2. When `recorded is not None`: `before = {id: (status, reading, at)}` of `QR.load(self.task_root)["questions"]` (in `try`; failure ->
   `before = None`).
3. The text (kind -> noun, a closed driver vocabulary, not a language: `s1_review` "a source review", `halt` "a halt", `questions`
   "the open questions"):
   - "The person answered <noun> of dispatch D at S. Record what they decided with the factory's own commands (<commands>), nothing
     else; the role itself is resumed by the driver afterwards." — `<commands>` as today (`:3829-3830`), by `recorded is None`.
   - When `recorded is not None` (data condition, both register roads alike):
     "The factory read their lines against the register's questions by code - recorded by code: <recorded + deferred, or nothing>;
     do not record these again, and do not journal their words again (the driver did). "
     + ("Not recorded by code (each line says why): " + "; ".join(unread + unknown_ids) + ". " when any) — fix F8: the old label
     "Not read, still open" was false for an H6 refusal; each line already carries its reason and, for H6, the `--reopen` door.
     + "An answer they gave to a question in other words is recorded with question_register.py (--answer QID --reading <letter> |
     --not-needed QID | --defer QID, with --words-file, --where \"S stop\", --by conductor and " + HASH + ")."
     where HASH is, when `shown` is a non-empty dict (fix F5): "--register-hash = the hash the person was SHOWN: `question_stop.shown`
     in <absolute state_dir>/driver-state.json; only for an id not there, the one --show prints"; otherwise (halt road, `shown` empty)
     today's "the --register-hash that --show prints".
     + " Read the questions whole with `python <scripts>/question_register.py --task <T> --show`: the question text below may be cut."
     (fix F6; `<scripts>` = `self.scripts`, `<T>` = `self.task`).
   - `" " + MOVES_RULE + " " + OWN_TOKEN_RULE` except for `s1_review` (as today, `:3846`).
   - `"\n\n## The question\n" + qtext[:6000]` + `(PRE_FILLED + read if read else "")`.
   POSITION INVARIANT of the text: every instruction precedes `## The question`, so the two 6000-character cuts of the QUESTION
   (`qtext[:6000]` here; `refusal.strip()[:6000]` in `conductor()` `:320`, which also covers the moves section in front) cut only
   question text, never an instruction.
4. `self.unread(kind, stage, dispatch, <text>, words=words)` — `doors=None` (fork F-3 A); the call shape FV1-6 keeps compatible (it
   only adds a keyword `asked_why`). `Person` / `Stop` propagate unchanged.
5. After `unread` RETURNS and `recorded is not None`:
   - `lines = self.apply_question_answers(stage)["plan_lines"]` (the conductor's records laid over the plan in the same move; B3);
   - the print-back (fork F-11, decided): `after` as in 2; every id whose `(status, reading, at)` differs from `before` is printed in
     ONE line `"{S}: recorded by the assistant from your own words — Q3: a, Q5: not needed, Q7: until the report, Q2: open again"`
     (status -> words: `answered` -> the letter, `not_needed` -> "not needed", `deferred_to_report` -> "until the report", `open` ->
     "open again", any other status -> the status word); none changed -> `"{S}: the assistant recorded nothing from your own words;
     those questions stay open"` (AR-23 empty outcome); `before` or `after` unreadable -> `"note: the register could not be read back
     after the assistant's moves; run question_register.py --show to see what was recorded"` (AR-28: an unknown is not "nothing").
   - returns `lines` (`[]` when `recorded is None`).

Callers:
- `_unread_halt_or_review`: after `record_halt_words` and its all-token return (unchanged), `self.register_words_to_conductor(kind,
  stage, dispatch, qtext, words, recorded)` (lines discarded, as `record_halt_words` discards its own today), then `pending_words`
  as today (`:3850`, AFTER the seam: the halt road's order stays).
- `take_question_answer` (§3.2).

Byte-identical `unread` text for `s1_review` and for a `halt` with no register (`recorded is None`). For a `halt` over a register the
text changes in three named ways (label F8, the `--show` sentence F6, no judge section F-9); K1's assertions on it hold (§4 K4).

### 3.2 `take_question_answer` — the new order (POSITIONAL)

Signature gains `qtext: str = ""` (keyword with default); `take_answer` `:3557` passes the `qtext` it holds (`:3376`). A caller
without it (s0/s6 tests) gets no `## The question` body.

1. Whole-answer `go on` / `stop` — unchanged, first (`:1762-1780`).
2. `read = self.record_question_words(stage, words, shown)` — the return value is now KEPT (fix F11); `shown` = `stop["shown"]` when it
   is a dict, else `{}` (as today).
3. `self.answer_row(f"{stage} question stop: ", words, what="your answers at the question stop")` — MOVED here from `:1789`.
4. `told = self.apply_question_answers(stage)["plan_lines"]`; extend `question_pass_lines[dispatch]` — UNCHANGED place relative to the
   records (before the seam; B3: code's own records are applied and announced to the resumed role whatever the seam does).
5. `stop["answered"] = {...}`, `stop["resume"] = True`, `self.state["pending_words"][dispatch] = words`, then `self.save_state()` —
   the floor: every fact a later process needs is on disk before the seam can raise.
6. NEW: if not (`read["all_tokens"]` and not `read["unread"]`): `lines = self.register_words_to_conductor("questions", stage, dispatch,
   qtext, words, read, shown=shown)`; extend `question_pass_lines[dispatch]` with `lines` (AR-22: the role is told what the
   conductor's records changed). `Person` / `Stop` propagate (the process asks / ends).
7. Docstring rewritten: the conductor reads what code could not (FR-48 kept: code recorded its tokens first and says so).

POSITION INVARIANTS (each a row in §4):
- I1: a whole-answer `go on`/`stop` never reaches the conductor and never records a token.
- I2: every token code can read is recorded by CODE before the conductor is called, and the conductor is told it is recorded — never
  told as unread (FR-48).
- I3: a free answer NEVER counts as a chosen option by code: `parse_choices` grammar unchanged; `Q1: a because ...`, `Q1: a or b`, a
  fenced `Q1: a` record nothing by code. The only writer of a record from free words is the conductor's CLI call (`by: conductor`).
- I4: an all-token answer (H31 twin) never calls the conductor (no spend, FR-55).
- I5: the words are journalled once (`answer_row`) and filed (`pending_words`) and saved, and code's records are applied with
  `question_pass_lines` set, BEFORE the seam can raise (B3).
- I6: a role is never resumed while a question about its dispatch is open — in the `--answer` process (the Person ends it before the
  loop, `_run_guarded` `:1858` precedes it) AND in a rerun with no `--answer` (§3.3, B2).

### 3.3 The rerun guard (B2; fork F-10 decided A)

`_act_wait_existing_job`, today `:1451-1463`: the `pending_words` resume comes first, the open-`questions` re-ask second. After:

```
words = self.state["pending_words"].get(dispatch)
asked = self.state.get("asked") or {}
if (asked.get("kind") and asked.get("dispatch") == dispatch and self.question_path().is_file()
        and (words or asked.get("kind") == "questions")):
    again = self.held_question("")            # THE re-ask helper: offered / options / words_file / why / block survive
    again.text = again.text.strip()           # no lead: the body is the open question's own
    raise again
if words:
    self.resume_role(...)                     # as today
    return
```

and the old block `:1455-1463` goes (its case — an unanswered threshold stop, no words — is the `asked.get("kind") == "questions"`
arm above; its INVARIANT comment t-113 B2 edge x moves with it). The halt/s1_review re-ask `:1484-1487` is untouched.

POSITION INVARIANT: the guard sits BEFORE the `pending_words` resume, so (a) a seam question raised over filed words (kind
`questions`, `offered` set) is asked again with its own tokens and the role is not resumed; (b) for every other kind the guard fires
only in the state "words filed AND a question about this dispatch open", which today resumes the role over an open question (a
defect for any kind); (c) a state with no words and no open question, or an open question about ANOTHER dispatch, takes today's
branches unchanged; (d) an unanswered threshold stop with no words is asked again as before (same kind, stage, dispatch, body).

Census (AR-20, named): the `Person("questions", ...)` site of `_act_wait_existing_job` becomes a `held_question` call:
`NO_MOVE_BASELINE` row `:1687` `Person:questions` 1 -> removed; new row `('driver_machine.py', 'Driver._act_wait_existing_job', 'P',
'builder:held_question'): 1`; the sum, hence `NO_MOVE_BASELINE_MAX`, unchanged. If `test_audit_rules.py` refuses the swap, the
builder stops and returns it as a question (no silent raise).

### 3.4 Texts (FR-10, FR-37)

- `question_stop.py` `BLOCKING_NOTE` `:464-465` becomes: "A question marked as blocking is settled only by a recorded answer - a line
  with its id, or your own words once the assistant running this story has recorded them - or passed with `go on`; a blocking
  question nobody could record is asked again." `:437` stays (it becomes true).
- `driver_machine.py` `describe` `:4143-4145`: "would record the answers in <file> by code, per open question; words code could not
  read go to the conductor first; then the role's own session resumes with the words".
- `driver_machine.py` comment `:3555-3556`: "A threshold stop (t-113 B2, R17, FV1-3): tokens are recorded by code; words code could
  not read go to the conductor (`register_words_to_conductor`); the words go to the role's own session. Only this kind reaches it."

### 3.5 Seam outcomes (AR-25)

| seam returns | effect |
|---|---|
| `continue` / `retry` | §3.1 step 5 (apply, print-back); `take_answer` completes, `asked` cleared `:3633`; the role resumes on the next loop step with the original words and the code + conductor plan lines; the next threshold check counts the register as left (fewer open -> no stop; a larger count -> the "still open after your answer" re-stop, changed text, FR-7) |
| `Person` (conductor `ask_person` with valid options) | asked (`ask()` writes `offered`); the answer to it is read by `take_seam_answer` (`:3540`, before the `questions` branch), never by `take_question_answer`; a rerun with no answer re-asks it (§3.3) |
| cap reached (`ConductorSpent`) / unusable answer | the seam's priced fallback Person (`fallback_person` `driver_conductor.py:646-647`), one `defect_found` by the seam itself; I5 holds (all saved before) |
| conductor `stop` | `options_person` / `Stop(EXIT_GAVE_UP)` (`:677`, seam rule) |

### 3.6 Error direction of every reused function in its new role

| function, new role | may err toward | adversarial inputs that must stay on the safe side |
|---|---|---|
| `record_answers` / `_only_tokens` (token reader -> gate of the hand-over) | a missed token = one more paid conductor call; never a false "all tokens" | prose line; `Q1: a because ...`; `Q1: a or b`; two lines for one id; a fenced token; a `>` quoted token; a case word; an unknown id; Cyrillic look-alike letter; blank-only text — each gives `all_tokens: False` |
| `judged_reply` (now ONLY where no register was read) | unchanged on S1 review / halt with no register; on the register roads it is no longer called, so its "toward approve" error (critic §4) cannot reach the conductor there | an 18-question pack read as `approve` — must not appear as `PRE_FILLED` in a register-road prompt (row `no-judge-on-register`) |
| `apply_question_answers` (now also after the seam) | never raises; a failure is a note and "tried again at the next stop"; idempotent, so a second call writes nothing for records already applied | called twice with no new record -> second call `plan_lines == []` |
| `held_question` (now the rerun re-ask) | rebuilds from the question FILE and `asked`; missing file -> the guard does not fire (condition) and `reconcile_question` `:259-263` already clears a flag with no file | open question about another dispatch; file absent; `asked` with no kind |
| `register_hashes` / `stop["shown"]` (now named to the conductor) | an id with no shown hash -> the conductor uses `--show`'s hash (today's behaviour) | a row changed between showing and answering -> the record keeps the SHOWN hash, `changed_since_answer` stays visible |
| the conductor's reading of free words (role) | a misreading becomes a settled record; made VISIBLE by the print-back, undoable by `--reopen` (H6 door) | — (judgment; not code) |

## 4. Node FV1-3

given: `C:\QAFactory\forge-repo\ai-packages\qa-factory\design\factory-rules.md` (whole); `plans/builder-rules.md`; `docs/TESTING.md`;
`ai-packages/qa-factory/design/architecture.md` (AR-7, AR-13, AR-14, AR-15, AR-17, AR-19, AR-20, AR-22, AR-24, AR-25, AR-28, AR-29);
this spec, `docs/tasks/specs/20261113-fv1-3-free-answer-to-conductor-spec.md`; in the builder's worktree (functions by name, lines as
on e4ba384): `scripts/driver_dispatch.py` (import `:20`; `resume_role` `:1028-1110`; `question_threshold` `:1590-1674`;
`question_resume_prompt` `:1716-1725`; `take_question_answer` `:1746-1789`; `record_question_words` `:1797-1830`; `record_halt_words`
`:1832-1848`; `apply_question_answers` `:1852-1881`); `scripts/driver_machine.py` (`_act_wait_existing_job` `:1445-1487`;
`_run_guarded` `:1852-1870`; `take_seam_answer` `:2335-2386`, read only; `take_answer` `:3361-3637`; `_unread_halt_or_review`
`:3814-3850`; `describe` `:4134-4148`); `scripts/driver_conductor.py` (`unread` `:852-870`, `no_move` `:602-677`, `conductor` `:263-348`,
`_person_of` `:419-431`, `judged_reply` `:911`, constants `:21-48`, `ConductorSpent` `:85`); `scripts/driver_dialog.py` (`ask`
`:270-329`, `held_question` `:600-629`); `scripts/question_register.py` (CLI header `:1-16`, `record` `:862-921`, `record_answers`
`:976-1023`, `_merge` `:252-276`); `scripts/question_stop.py` `:417-523`; `scripts/audit_factory.py` `:1642-1716`, `:2330-2360`;
`references/question-vocabulary.json`; `scripts/tests/story_run_loop_b_common.py`; `scripts/tests/test_story_run_loop_b_threshold.py`;
`scripts/tests/test_story_run_loop_b_answers.py` `:36-82` (read only); the real input
`experiments/mybooks/factory-vs-free-agent/answers/s4-questions-batch-1.md` (copied VERBATIM into the test as a constant: package
tests do not read outside the package).
owns:
C:\QAFactory\forge-repo\.claude\worktrees\fv1-3\ai-packages\qa-factory\scripts\driver_dispatch.py (the import line 20 only: add `MOVES_RULE, OWN_TOKEN_RULE, PRE_FILLED`; function `Driver.take_question_answer`; NEW function `Driver.register_words_to_conductor`; nothing else)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-3\ai-packages\qa-factory\scripts\driver_machine.py (functions `Driver._act_wait_existing_job` (lines 1451-1463 region only), `Driver._unread_halt_or_review`, `Driver.describe` (the sentence 4143-4145 only); in `Driver.take_answer` ONLY the comment 3555-3556 and the call 3557)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-3\ai-packages\qa-factory\scripts\question_stop.py (constant `BLOCKING_NOTE` only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-3\ai-packages\qa-factory\scripts\audit_factory.py (dict `NO_MOVE_BASELINE`: the row of `_act_wait_existing_job` `Person:questions` removed, the row `builder:held_question` added; nothing else)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-3\ai-packages\qa-factory\scripts\tests\fixtures\driver-layers.json (one row: `{"name": "Driver.register_words_to_conductor", "kind": "method", "home": "driver_dispatch", "row": 45, "note": "FV1-3: register words code could not read -> the conductor (unread), then the after-seam apply and print-back; called by take_question_answer (dispatch) and _unread_halt_or_review (machine, downward)"}`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-3\ai-packages\qa-factory\scripts\tests\test_story_run_loop_b_threshold.py (functions `question_stop_road`, `question_stop_fallbacks` (the flips below); NEW function `fv1_3_free_answer_at_a_question_stop` (one table) and NEW scenario functions `fv1_3_the_real_s4_answer`, `fv1_3_rerun_with_no_answer`, `fv1_3_the_real_pack_size`; `main()` entries)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-3\ai-packages\qa-factory\scripts\tests\test_story_run_s0.py (function `s0_fenced_decision_notice` only: stub `driver.unread`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-3\ai-packages\qa-factory\scripts\tests\test_story_run_s6.py (function `t261_the_integration_lines_of_the_driver`, block (b) only: stub `driver.unread`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-3\ai-packages\qa-factory\changelog.d\fv1-3-free-answer-to-conductor.md (new fragment, English)
non-goals: `parse_choices` / `_TOKEN` grammar (FV1-13 owns token reading); `question_register.py` (its writer and CLI exist);
`driver_conductor.py` entirely (`unread`, `no_move_facts` are FV1-6's; `no_move`, `validate_options`, conductor-actions.json are
FV1-13 #4's); `driver_machine.take_seam_answer` / `seam_chosen` / `seam_rework_step` (FV1-6; the seam's second answer is fork F-12);
`references/conductor.md` (the prompt carries the instruction); any backfill of answers lost before the change (F-4); FV1-9;
`test_story_run_loop_b_answers.py` (read and run, not edited); the quarantined `test_question_stop.py` (not run, not edited: edge E12);
`design/driver.md` (no row of it states the old road: trail).
handoff: the builder's report (rule 7 of `.claude/agents/builder.md`) with the FR walk A-G one line each, the verbatim witness, the
axis-34 line, the A27 swap line, and every "no scenario or keep row covers" line as printed; commit on the batch branch
`pile/live-run-fvf/batch-1` in the worktree above.
edges:
- E1 empty / whitespace-only answer: `take_answer` raises `Stop(EXIT_ERROR, "<path> is empty")` `:3366-3367` before any branch,
  unchanged. Invariant: nothing recorded, no conductor call, no `answer_row`. Row `empty-whitespace`.
- E1b an answer when no question is open: `Stop(EXIT_ERROR, "no question is open ...")` `:3368-3369`, unchanged. Invariant: nothing
  recorded, no conductor. Row `no-question-open`.
- E2 all tokens (`Q1: a\nQ2: not needed`): no conductor (I4); records by code; words filed. Invariant: zero conductor spend. Row
  `all-tokens`.
- E3 free words only: conductor once; text says "recorded by code: nothing" and `--where "S2 stop"`, `--by conductor`. Invariant:
  nothing recorded by code (I3). Rows `token-word-inside-free-text`, K2.
- E4 mixed lines (`Q1: b\nQ3 go with the ticket`): Q1 recorded by code BEFORE the call (the stub reads the register and sees Q1
  answered); text "recorded by code: Q1: b". Invariant I2. Row `mixed`.
- E5 a token-looking word inside free text (`Q1: a because the ticket says so`): not a token; conductor once; Q1 stays open by code.
  Invariant I3 (the reused reader errs toward NOT seeing a choice, `question_register.py:655`). Row `token-word-inside-free-text`.
- E6 two answers for one id / `Q1: a or b`: covered by `test_question_register.py` and threshold `:79-82` (not repeated, F9);
  the hand-over consequence is the same as E5.
- E7 another language (`"Q3: " + "".join(chr(c) for c in (0x0432, 0x044B, 0x0448, 0x0435))` and a Cyrillic look-alike `"Q1: " +
  chr(0x0430)`): not tokens; conductor once; the words FILE (`task_root / d.answer_file()`) is byte-equal to the UTF-8 answer.
  Invariant: no transcoding, no loss (FR-8). Row `another-language`.
- E8 very long answer — no limit is introduced by this node. Existing limits: the words in the prompt are cut at 6000 with a pointer
  (`driver_conductor.py:29`, `:322-323`); the QUESTION is cut twice (`qtext[:6000]` in the member; `refusal.strip()[:6000]` over moves
  section + text in `conductor()` `:320`). Rows `words-at-6000` (6000 characters) and `words-beyond-6001` (6001): the words FILE is
  whole (length and bytes equal) — the QStub stubs `conductor()`, so the prompt cut is not observable there and the file is what
  carries the words past it. Row/scenario `fv1_3_the_real_pack_size`: a register of 18 questions whose texts make the question file
  at least 13 300 characters: in the stub's `a[0]` (the refusal text before the cut) the indices of "recorded by code:" and of
  "--show" are both < 6000. Invariant: no word of the person and no instruction is lost to a cut (FR-8); only question text may be
  cut, and the conductor is told where to read it whole. If the moves section alone pushes the instruction past 6000, the builder
  stops and returns a question (`conductor()` is not in owns).
- E9 an answer to a question no longer open: (a) a DIFFERENT token on a settled id -> `record`'s H6 refusal lands in `unread` ->
  conductor once; the text lists it under "Not recorded by code (each line says why)" with the `--reopen` door the line carries,
  never under "still open" (F8); the settled record is unchanged. Row `settled-other-answer`. (b) no question open: E1b. (c) the open
  question is now the seam's own (`offered`): the answer goes to `take_seam_answer` `:3540`, not here (fork F-12 for its free words).
  Invariant: a settled record is never overwritten by code.
- E10 `go on, but Q3 is the ticket's`: not the whole-answer token -> the register road -> conductor once. The whole `go on`/`stop`:
  unchanged branch (I1, existing tests). Row `go-on-not-whole`.
- E11 register unreadable at answer time (`requirements-readiness.json` replaced by `{not json` after the stop): `record_question_words`
  gives `all_tokens: False` -> conductor once, text "recorded by code: nothing". Invariant AR-28: error toward the reader, never
  toward "settled". Row `register-unreadable`. After the seam, an unreadable register prints the "could not be read back" note, never
  "recorded nothing". Row `printback-unreadable` (register made unreadable inside the conductor stub).
- E12 the quarantined pin `test_question_stop.py:594` holds the old `BLOCKING_NOTE`; the builder does not run or edit it and writes
  one report line naming it (F-6 decided A).
- E13 TEMPORAL: (a) a `driver-state.json` written before the change with an open `questions` stop: its next answer takes the new road;
  no state key is new or renamed (`question_stop.shown`, `pending_words`, `question_pass_lines`, `asked` all exist). (b) a state the
  OLD driver left after a completed free answer (asked cleared, `pending_words` filed, no conductor): no open question -> the guard
  does not fire -> the role resumes with the words as before; those words never reach the conductor (F-4 decided A, no backfill).
  (c) a process that died AFTER step 5 (words saved) and BEFORE the seam call: `asked` is still the threshold question and its file is
  on disk -> the rerun re-asks it (guard arm `kind == "questions"`), and `ask()`'s "You have answered this exact question before"
  block (`driver_dialog.py:302-314`) quotes their words; the person's next answer takes the road again (fork F-14). (d) a record the
  conductor writes (`by: conductor`, `where: "S4 stop"`) is read by every reader as any record: no register reader branches on `by`
  (critic's case-insensitive grep with positive control, review §1; `planning_contract.apply_recorded_answers` `:3459-3500` filters on
  neither `where` nor `by`).
- E14 POSITIONAL: §3.2 I1-I6 and §3.3 (a)-(d). The `questions` branch keeps its place in `take_answer` (after `offered` `:3540`, before
  the halt branches `:3558`). Invariant: a seam question's answer is never read as a threshold answer.
- E15 conflicting requirements: (i) "the words reach the role" vs "the conductor records first": the role is resumed only after the
  seam returned (I6, both worlds: §3.3), so it sees the conductor's records and both plan-line sets. (ii) "byte-identical halt prompt"
  (old K4) vs "one member with the judge decided by data" (F-9): byte identity is narrowed to `s1_review` and `halt` with no register;
  the halt-over-register text changes in the three named ways of §3.1.
- E16 seam outcomes: §3.5, rows `continue` (K2), `seam-raises` (cap: the conductor stub raises
  `driver_conductor.ConductorSpent(3, "x")` -> the fallback Person is raised out of `take_answer`; on disk before it:
  `pending_words[dispatch]`, `question_pass_lines[dispatch]` from code's own records (the apply recorder returns one line), ONE
  `human_answer` row), `rerun-no-answer`.
- E17 the conductor cap is per boundary (`take_answer` sets `S:dispatch:answer`, `:3373`): this node adds at most ONE call per answer;
  AT the cap (3 calls already on the key) the seam's fallback applies (row `seam-raises`). Invariant: no unpriced or silent outcome.
- E18 the guard (§3.3) and other kinds: invariant "a role is never resumed while a question about its dispatch is open" for every
  kind; a state with words but the open question about ANOTHER dispatch resumes as today. Row `rerun-other-dispatch`.
DoD:
- K1 the threshold stop's free answer reaches the conductor ONCE (stub count 1) with the words file whole; an all-token answer zero
  times. Rows `all-tokens`, `token-word-inside-free-text`, `mixed`.
- K2 the finding's own test, scenario `fv1_3_the_real_s4_answer` (the one row that FAILS before the change): an S4 stop
  (`QStub(root, env, stage="S4")`, a register Q1-Q18), answered with the 18 lines of `answers/s4-questions-batch-1.md` VERBATIM
  (a constant in the test); the conductor stub runs, through `d.py`, `question_register.py --task QA-9 --answer Q3 --reading a
  --words-file <task_root / d.answer_file()> --where "S4 stop" --by conductor --register-hash <d.state["question_stop"]["shown"]["Q3"]>`
  and returns `{"action": "continue"}` -> the register holds Q3 `answered`, reading `a`, `words` equal to the answer file's text,
  `record_row_hash` equal to the SHOWN hash (F5); `apply_question_answers` (a recorder wrapping the real one) ran in the order
  `apply, conductor, apply`; the printed output carries "recorded by the assistant from your own words — Q3: a"; the conductor's text
  `a[0]` carries `question_stop.shown` and "--show" and no `PRE_FILLED` heading (F-9).
- K3 ONE parameterised function `fv1_3_free_answer_at_a_question_stop` in `test_story_run_loop_b_threshold.py`, rows by id naming the
  input: `empty-whitespace`, `no-question-open`, `all-tokens`, `token-word-inside-free-text`, `mixed`, `another-language`,
  `words-at-6000`, `words-beyond-6001`, `settled-other-answer`, `go-on-not-whole`, `register-unreadable`, `printback-unreadable`,
  `seam-raises`, `no-judge-on-register` (S2 halt over a register and a question stop: `d.judged_reply` is a recorder that must stay
  uncalled), `halt-road-shares-member` (stub `d.register_words_to_conductor` with a recorder; both roads call it once, with `kind`
  `halt` / `questions`), `rerun-other-dispatch`. Each row: id, words, expected conductor calls, expected code records, expected words
  file. Parse rows already pinned elsewhere are NOT repeated (F9).
- K4 `fv1_3_rerun_with_no_answer` (B2): free answer at an S2 stop; `d.unread` raises a Person built as the seam does (kind
  `questions`, `offered = ("retry", "stop")`, `options` with moves `person_does` / `stop_here`), `d.ask` it; then `d.dispatch_action(
  {"action": "wait_existing_job", "dispatch_id": s.dispatch})` raises `Person` kind `questions` whose `offered` is `("retry", "stop")`
  and whose text holds the seam question; no `role` call in `s.claude_calls`; `pending_words[s.dispatch]` still holds the words. Then
  answer `retry` -> `take_seam_answer`; the next `dispatch_action` resumes the role in `sess-1` with the ORIGINAL words in its prompt.
- K5 B1 flips in `test_story_run_loop_b_threshold.py`: `:92` -> "answer: the conductor was called once, for the lines code could not
  read" (`len(s.conductor_calls) == 1`) plus `"recorded by code: Q1: a, Q2: b, Q3: not needed" in s.conductor_calls[0][0]`; `:108` ->
  "resume: no conductor on the resume" asserts the count is STILL 1; `:139` -> "one conductor call in all of it: the answer's"
  (`len == 1`); `question_stop_fallbacks` `:326` -> per label `len(s.conductor_calls) == 1` ("once at the answer, never at the
  rework or the resume"). Every other assertion of both functions unchanged and green.
- K6 `test_story_run_s0.py:1137` and `test_story_run_s6.py:923,931` keep their assertions with `driver.unread = lambda *a, **k:
  "continue"` set before the calls (they assert what code printed, which is unchanged).
- K7 halt road: `test_story_run_loop_b_answers.py:36-82` green UNCHANGED (its second block stubs `judged_reply` and `unread`; its
  assertions `:76-80` hold on the new text).
- K8 registries: `driver-layers.json` row added, `test_driver_layers.py` green; `NO_MOVE_BASELINE` swap, `test_audit_rules.py` green;
  if `test_judgment_census.py` or a module-size ratchet in `test_driver_layers.py` reports a new unit or a ceiling breach, the builder
  stops and returns it as a question (AR-20: never raised silently).
- K9 FR walk A-G in the report; commit message lines `architecture: AR-17, AR-24, AR-13, AR-14, AR-15, AR-19, AR-20 (A27 row swap in
  _act_wait_existing_job, sum unchanged), AR-22, AR-25, AR-28, AR-29 -- <how kept>` and the `judgment:` line.
- Verification run: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/driver_dispatch.py ai-packages/qa-factory/scripts/driver_machine.py ai-packages/qa-factory/scripts/question_stop.py ai-packages/qa-factory/scripts/audit_factory.py ai-packages/qa-factory/scripts/tests/test_story_run_loop_b_threshold.py`
  — builder-rules 7b: run EVERY file it prints whose time in `scripts/slow_tests.json` is under one minute (among them
  `test_story_run_loop_b_threshold.py` 25.0 s, `test_story_run_loop_b_answers.py` 27.6 s, `test_driver_layers.py` 32.5 s,
  `test_audit_rules.py` 9.6 s, `test_question_register.py`, `test_silent_passes.py` and the other callers of
  `_act_wait_existing_job`: `test_exit_limit_halt_answered.py`, `test_reference_window.py`, `test_story_run_s3_windows.py`, when
  printed); name the files over a minute (`test_story_run_s0.py` 289.8 s, `test_story_run_s6.py`, ...) in the report for CI on the
  batch branch; never the quarantined `test_question_stop.py`.
siblings: axis 34 (one action, one road): the halt road and the question stop share one member (covered); the seam's SECOND answer at
a question stop or a halt (free words to the seam's own question go to the generic prompt, `driver_machine.py:2370-2372`, FV1-6's
`take_seam_answer`): fork F-12, a residual node drafted below for the Lead to place; axis 5 «One question for every stop» (A27): the
new member has no Person, Stop or `py` (n/a); the guard's site is a swap (named, AR-20); neighbour class "free words with no reader":
`after_close` (`driver_dialog.py:643-648`, reached from `take_answer` `:3546-3550` and `take_seam_answer` `:2360-2362`) only journals
words that arrive at a done stage -> returned to the Lead as a finding to queue (not this node); sibling texts: `describe` (owned),
`BLOCKING_NOTE` (one constant, both readers `question_stop.py:522`, `driver_dispatch.py:1646`), the `take_answer` comment (owned), the
`take_question_answer` docstring (owned); S1 review (`record_review` records ANY words — n/a), gate A/B (`_unread_kept_gate` — n/a),
`s1_gap` free words fall through to the seam (`:3527-3528` — n/a).
designer: `C:\QAFactory\forge-repo\docs\tasks\specs\20261113-fv1-3-free-answer-to-conductor-spec.md` (rev. 2; a later resubmission is
edited by the Lead).

## 5. Node FV1-9 (sequential after FV1-3) — NOT DISPATCHABLE until the owner decides F-7 and F-8 and one scout pass is done; then it
returns to the designer

Facts (lines re-taken on read-main e4ba384 where code; run logs root): the S4 pack of 18 (`factory-6.log:93`): Q10-Q18 are
before/now questions raised from S4 cases (`_raise` `question_register.py:1282`; `_shown` `:1270`); S2's Q1-Q6 print `(from ?)`
(`factory-6.log:99-110`), printed by `gate_brief.py:2786`, `:2794` when a reading has no `from`. Same-location pairs: Q7/Q16 cite
`work/requirements-register.md:23` and `cartService.ts:53` (`factory-6.log:132-134`, `:226-228`); Q13/Q14/Q15 cite
`requirements-register.md:25` and `cartOwner.ts:7`. Q1/Q10, Q2/Q11, Q3/Q12 share NO data key (they repeat by meaning only); `_shown`
differs for Q7/Q16 ("quantities" vs "quantity"): an exact-data merge catches none of the six real pairs. The "cannot be answered as it
stands" text is the gate A rehearsal's (`gate_preflight.py:2018`; the one rule `contract.question_errors` `contract.py:625`); in the run
its S2 rework was refused by the repair-round cap (`factory-7.log:20`).

Design (recommended; F-7, F-8 decide it):
- (a) Repeats are judgment (P27, FR-12): code supplies DATA, the role judges. At the S4 exit `raise_for_case` (`question_register.py:1373`)
  returns, per NEWLY raised row, the OPEN rows sharing a `source_says[].where` OR the `now.where` (exact, whitespace collapsed; either
  location suffices) as hint lines (no refusal, no merge, no census unit). A REPLAY is told apart by data: `raise_for_case` reads the
  register ids before its loop; a row `_raise` returns whose id was already there (the idempotent return `:1319-1332`) is a replay and
  gets no hint (fix F15). Judgment: one case-critic charter line (a raised question that asks what an open question asks is a
  finding; the designer points the Then at the existing id, `replaces` `:1411-1413`). The withdrawn row's way out: F-7.
- (b) `(from ?)` is never printed: a reading with no `from` prints `(no source named)` (P9).
- (c) A question the rehearsal names "cannot be answered as it stands": F-8.

given (for its designer round): as FV1-3 plus `question_register.py:1242-1470`, `gate_brief.py:2770-2800`, `gate_preflight.py:1960-2030`,
`contract.py:600-663`, `question_stop.py:343-405`, `agents/qa-case-critic.md`; root `factory-6.log:86-235`.
owns (ESTIMATE, final at its designer round, written then against its own worktree):
`ai-packages/qa-factory/scripts/question_register.py` (`raise_for_case`; F-7 B adds CLI `--withdraw`), `scripts/gate_brief.py` (the two
`(from ...)` lines `:2786`, `:2794`), `agents/qa-case-critic.md` (one charter line), `scripts/tests/test_question_register.py` (rows).
non-goals: merging questions by text similarity or location in code (meaning-proxy ratchet `meaning-proxy: 8` shrink-only,
`judgment-census.json:4`); FV1-3's hand-over; renumbering ids.
edges: E1 a raised row with no `source_says`/`now.where` -> no hint (no key, no guess); E2 the matching row is settled -> no hint
(OPEN rows only); E3 several matches -> all ids, register order; E4 a hint never blocks the raise (invariant: a question is never
lost to a hint); E5 a blank/whitespace `from` -> `(no source named)`; E6 TEMPORAL: rows raised before the change carry no hint, nothing
retroactive; E7 POSITIONAL: the hint is computed in `raise_for_case` AFTER `_raise` returns, only for ids absent before the loop, so a
replay prints no hint.
DoD rows (`test_question_register.py`): two raised rows sharing `source_says.where` (different `now.where`) -> one hint naming the
earlier id (OR); sharing `now.where` only -> one hint; sharing neither -> no hint; a settled earlier row -> no hint; a replayed raise
-> no hint; a reading with no `from` -> `(no source named)`, never `?` (F15: the AND/OR contradiction of rev. 1 is gone).
Verification run: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/question_register.py ai-packages/qa-factory/scripts/gate_brief.py ai-packages/qa-factory/agents/qa-case-critic.md`.
siblings: the S3 claim projector writes raised rows through `_question_row` (`:1341`) too — the same hint applies there or is queued
(at its designer round).
Order: FV1-3 -> FV1-9 because FV1-9 is not ready (F-5 decided A; no shared file or function).

## 6. Crossings (against the specs in their fix rounds now)

FV1-3's function list: `driver_dispatch.py` (import line 20; `take_question_answer`; NEW `register_words_to_conductor`);
`driver_machine.py` (`_act_wait_existing_job`; `_unread_halt_or_review`; `describe` sentence; `take_answer` comment + call line only);
`question_stop.py` (`BLOCKING_NOTE`); `audit_factory.py` (`NO_MOVE_BASELINE`, two rows).

| other node | its functions (from its spec) | shared with FV1-3 | order |
|---|---|---|---|
| FV1-6 (`20261113-fv1-6-s2-door-back-to-tester-spec.md:142-149`) | `no_move.FINISHING_WHYS`; `driver_conductor.no_move_facts`, `unread` (new keyword `asked_why: str = ""`, `:171`); `driver_machine.take_seam_answer`, `seam_chosen`, `seam_rework_step`; `driver_stage_plan.stage_review_exhausted`; after its fix round probably `driver_conductor._person_of` | NONE. FV1-3 CALLS `unread(kind, stage, dispatch, text, words=...)` (compatible with the added keyword) and RELIES on `_person_of` keeping `Person.kind = state["kind"]` and setting `offered`/`options` (the guard and row K4 read them) — FV1-6 must keep both (contract line for its fix round) | parallel legal (D-0048, disjoint function lists; both write `driver_machine.py` and the later merges main). Recommended: FV1-6 first (smaller), FV1-3 merges it; the F-12 residual node goes AFTER both (it changes `take_seam_answer`'s `unread` branch, FV1-6's line) |
| FV1-22 (`20261113-fv1-22-s7-acceptance-loop-spec.md`) | N1: handoffs/acceptance/`driver_stage_plan.stage_verdict_known`/`driver_stage_s7.stage_S7`; N2: `driver_dispatch.WINDOW_ROUND_STAGES` (constant, `driver_dispatch.py:109`), `driver_stage_plan.stage_acceptance_write`; N3: `driver_machine.window_round_gate`, `driver_dispatch.finish` | NONE (FV1-3 touches neither `finish` nor the constant; its line `:315` "N3 after FV1-3 for `driver_dispatch.finish`" is moot — FV1-3 does not touch `finish`). Its "must not touch" list (`:316-321`) should add `register_words_to_conductor` and `_act_wait_existing_job` | parallel |
| CL4-1 N1 (`20261113-cl4-1-collect-stalled-looped-spec.md:151-152`) | `driver_machine.window_round_gate` only | NONE (same file `driver_machine.py`) | parallel; the later merges main |
| FV1-13 (instances 1, 2, 4) | not drafted | depends on FV1-3: its `given` must carry `register_words_to_conductor` (the ONE hand-over for register words, always passing THIS answer's words file); its token-reading change must keep I3; its #4 fix (`go on` with no code-known block, `driver_machine.py:2429-2435`) must cover the `questions` and `halt` kinds (F-3 A) | FV1-13 after FV1-3 (batch row) |

Hot files: `driver_machine.py` and `driver_dispatch.py` are not on PROJECT.md «Командная работа» p. 3's list; disjoint function lists
suffice.

## 7. Forks

Decided in this fix round (marked technical by the critic's fork table; the decision and its reason):
- F-1 owns beyond the batch row — DECIDED A: the one-road owns of §4 (they include `driver_machine.py`, `audit_factory.py`, tests, and
  NOT `question_register.py`). Reason: B keeps two roads (a P31 exception only the owner could grant); the batch is not taken.
- F-2 hand-over predicate — DECIDED A: the halt road's `all_tokens and not unread`. Reason: no halt behaviour change; a lone case word
  or a fenced token costs at most one paid call that may `continue`.
- F-3 `go on` offered by the conductor at a question stop with no code-known block — DECIDED A: `doors=None` like the halt road; the
  executor gap is FV1-13 #4's for every kind. Reason: B is a P31 exception.
- F-4 answers lost before the change — DECIDED A: no backfill; the next stop asks the still-open questions. Lead to highlight
  «решила сама»: an in-flight story's person pays one more round.
- F-5 order FV1-3 -> FV1-9 — DECIDED A. Reason (corrected): FV1-9 is not ready (owner forks + scout); no file or function is shared.
- F-6 `BLOCKING_NOTE` vs the quarantined pin — DECIDED A: change the text (FR-10); the quarantined file is not edited; the owner is told
  the same turn the `quarantine-watch` alert fires (CLAUDE.md rule 11).
- F-9 `judged_reply` on the register roads — DECIDED: called only when `recorded is None`. Reason: its gate-intent list errs toward
  `approve` on an answer to a question pack (wrong direction for a pre-filled reading) and costs a judge call per answer; a data
  condition, the same on both register roads (P31-clean).
- F-10 I6 on a rerun with no answer — DECIDED A: keep the floor (step 5 saves before the seam) and re-ask the open question in
  `_act_wait_existing_job` BEFORE the resume, through `held_question` (offered survive). Reason: B (file after the seam) loses the
  floor on a raise. Cost: the A27 row swap (AR-20, named).
- F-11 print-back of the conductor's records — DECIDED: code prints the register's changes after a returned seam (data only), with
  the empty and unreadable outcomes declared. Reason: the conductor's reading is otherwise accepted by nobody at run time.

Returned (open, with recommendation; the node runs on the recommendation):
- F-7 (FV1-9, OWNER) a raised question the designer declares a repeat: (A) hint + charter + critic only (the person may still see both
  once); (B) a register way out `question_register.py --withdraw Qn --words-file ... --by <role>` for a role-raised row no case
  references, status `withdrawn` in `question-vocabulary.json` (FR-13), excluded by `is_open`; (C) reuse `with_designer`. Recommend B
  (AR-25). Owner's: it lets a role take a question out of what the person is asked (P13/P20).
- F-8 (FV1-9, OWNER) a question the rehearsal names "cannot be answered as it stands" whose rework was refused by the cap: (A) shown
  with one plain line naming the defect; (B) not shown, listed by id for the report (FR-59); (C) unchanged. Recommend A. Owner's: what
  a person is shown.
- F-12 (NEW, Lead's placement) the seam's SECOND answer at a question stop or a halt: free words to the seam's own question go to
  `generic_prompt` (`driver_machine.py:2370-2372`) with no "recorded by code" and no register instruction — another road for the same
  action (axis 34) on both twins. Drafted residual node (designer rule 6: a node with owns and a test): owns
  `driver_machine.take_seam_answer` (the `token not in by_token` branch only): when `asked.kind` is `questions`, or `halt` over a
  register (`record_halt_words` returns a dict), record by code first (`record_question_words`) and hand over through
  `register_words_to_conductor` instead of `generic_prompt`; test: one row in `test_story_run_loop_b_threshold.py` (`Q3: a` answered
  to the seam's question -> recorded by code, conductor told so). Options: (A) a new node after FV1-6 and FV1-3 (recommended:
  `take_seam_answer` is FV1-6's function, and this needs FV1-3's member); (B) folded into FV1-6's fix round (widens a node in review).
  Brief non-goal "no new nodes" -> returned, not created.
- F-14 (NEW, Lead's) a process that died between saving the words and the seam call (E13 c): (A) re-ask the threshold question on the
  rerun (no new key; `ask()` quotes their words as "answered before"; the person answers again and the words then reach the
  conductor) — recommended (rare window, no new state); (B) a state mark `question_stop.handover_owed` set before the seam and cleared
  after it, and a rerun that replays the filed words to the conductor without asking (cost: a new key in both worlds, a replay road,
  and a words file rebuilt from `pending_words`).

## 8. Small choices closed by the designer

- The conductor gets the WHOLE answer file as `--words-file` (`driver_conductor.py:312-314`), not per-line files.
- The shown hashes are named to the conductor by FILE (`question_stop.shown` in `driver-state.json`), not listed in the prompt: a list
  of 18 x 64 characters would push the instructions toward the 6000 cut; the file is written by `save_state` (FR-37) and saved in step 5.
- The H6 label is neutral ("Not recorded by code (each line says why)") rather than splitting H6 lines by their text: code does not
  read its own refusal text back by phrase; splitting would need a field from `record_answers` (not in owns).
- The print-back detects change by `(status, reading, at)` per id, not by `by` (a merged question does not carry `by`, `_merge`
  `:262-272`); during the seam only the conductor writes.
- The after-seam apply lives in the member (both register roads); the halt road discards its lines as it discards them today.
- `references/conductor.md` unchanged: the instruction is in the prompt the member builds.
- The real answer is a constant in the test (18 ASCII lines, provenance in a comment), not a fixture file (no new fixture registry row).
- The new rows live in `test_story_run_loop_b_threshold.py` beside the flipped ones (F9), not in the halt-road file.

## 9. Brief vs carriers (reported, scope not widened)

- The brief says FV1-6 changes `take_seam_answer` / `unread` and "if FV1-3 also changes them, FV1-3 goes after": FV1-3 changes
  neither; it calls `unread` and only the F-12 residual touches `take_seam_answer`.
- The brief's B2 wording adds "an answer recorded before the upgrade / before a restart": covered as E13 (b) (old state, no backfill)
  and E13 (c) (crash window, fork F-14).
- The critic's B1 named `:92`, `:139`, `:326`; `:108` ("resume: no conductor on the resume", the same cumulative list) flips too.
- The critic's F2 cites the docstring as `driver_dispatch.py:1747-1751`; on e4ba384 the docstring spans `:1747-1756` (owned whole).
- A rev.-1 claim was wrong: step 2 "unchanged" — the return value is discarded today (`:1781`); fixed (F11).

## 10. Reading trail (this round, read-main e4ba384 unless marked)

Read: the verdict `docs/tasks/specs/reviews/20261113-fv1-3-plan-critic.md` (whole, incl. fork table); this spec rev. 1 (whole);
`.git/worktrees/read-main/HEAD`; `driver_dispatch.py:1-40, 1085-1110, 1585-1901`; `driver_machine.py:1-40, 1435-1510, 1790-1820,
1850-1875, 1995-2044, 2330-2440, 3361-3390, 3520-3580, 3600-3640, 3810-3865, 4080-4154`; `driver_conductor.py:15-54, 263-274,
300-349, 557-581, 600-738, 845-875`; `driver_dialog.py:250-329, 600-649`; `driver_core.py:222-257` (grep); `question_register.py:1-48,
252-276, 320-341, 855-1024, 1290-1420`; `story_run_loop_b_common.py` (whole); `test_story_run_loop_b_threshold.py` (whole);
`test_story_run_loop_b_answers.py:1-95`; `test_story_run_s0.py:1112-1151`; `test_story_run_s6.py:895-940`; `audit_factory.py:1630-1704`;
`answers/s4-questions-batch-1.md` (whole); FV1-6 spec `:138-157` + grep; FV1-22 spec `:138-157, 243-322` + grep; CL4-1 spec (grep owns).
Greps (Grep tool, read-main paths): `state\.pop\("asked"|\["asked"\] = |state\.get\("asked"\)` over `driver_*.py`; `class Person|def
__init__\(self, kind` (driver_core); `def _person_of|def options_person|def fallback_person`; `question is open|still open, answer|
asked\.get\("offered"\)`; `def judged_reply`; test registry names over `test-layers.json`; `slow_tests.json` names; member names over
`driver-layers.json`; `take_question_answer|_unread_halt_or_review|_act_wait_existing_job` over `*.py`; `NO_MOVE_BASELINE`;
`judged_reply|...` and `"record"` over `judgment-census.json`; `def _merge|"record_row_hash"|"by":`; `pending_words"\]\.pop|def
resume_role`; `class ConductorSpent`; `BLOCKING_NOTE|words alone go to the role` (tests: only `test_question_stop.py:594`);
`^def ` over `test_story_run_s6.py`; `\(from ` over `gate_brief.py`; `meaning-proxy`; `def question_errors|cannot be answered as it
stands`; `no conductor\)|resume the role's own session with the words` over the package.
Negative claims with positive controls: (1) no test pins `describe`'s sentence — Grep `would record the answers|would route the
answer` over `scripts/tests` empty; control: the same tool over the same path found `words alone go to the role` at
`test_question_stop.py:594`. (2) no `design/driver.md` table row for kind `questions` — Grep `^\| \`questions\`` empty; control: the
same-shape `^\| \`[a-z_]+\` \|` found rows `halt`..`ticket_changed` at `:199-204`. (3) no package text states "threshold/question
stop ... conductor" — case-insensitive Grep `(threshold|question) stop.{0,200}conductor` empty; control: the same shape
`(halt|threshold) .{0,200}conductor` over `design/` found `factory-rules.md`. (4) no reader branches on `by`: the critic's grep with
control (review §1), not re-run.
Not re-read this round: the gitignored run logs (root; verified by rev. 1 and the critic); `judge_reply.py` (critic's lines);
`planning_contract.py:3459-3500` (critic). Not run: `scenario_walk.py --witness-for` (no shell in this role; the critic's run printed
154 lines for the rev.-1 owns, incl. `keep test_story_run_loop_b_threshold.py`).

## 11. Fix round (critic-on-plan verdict, 13.11.2026)

| item | what changed | where |
|---|---|---|
| B1 stale/omitted threshold pins | `test_story_run_loop_b_threshold.py` added to owns (functions named); flips named by assertion text: `:92`, `:108` (missed by the verdict, same cumulative list), `:139`, `:326`; run locally (25.0 s) | §2.2 tests, §4 owns, K5, verification run |
| B2 rerun skips the conductor's question | §3.3 rerun guard in `_act_wait_existing_job` (before the resume, via `held_question`, offered survive); I6 restated for both worlds; temporal rows | §1.1 AR-25, §3.2 I6, §3.3, E13 (b)(c), E14, E18, K4, F-10, F-14 |
| B3 plan update skipped on a raise | code's records applied before the seam (step 4, unchanged place) AND the conductor's after a returned seam (member step 5); all saved before the seam | §3.1 step 5, §3.2 steps 4-6, I5, E16 row `seam-raises`, K2 order |
| B4 stale lines | every `file:line` re-taken on read-main e4ba384; stamp in the header; owns written against the `fv1-3` worktree | header, §2, §4 given/owns, §5, §6 |
| F1 `describe` | owned; new sentence | §3.4, §4 owns |
| F2 comment + docstring | comment `:3555-3556` owned and rewritten; docstring `:1747-1756` rewritten | §3.2 step 7, §3.4, §4 owns |
| F3 import line | `driver_dispatch.py:20` owned | §4 owns |
| F4 judge | F-9 decided; error direction and cost stated | §1.2, §3.1 step 1, §3.6, row `no-judge-on-register` |
| F5 shown hash | the conductor is told the SHOWN hash by file; row in K2 | §3.1 HASH, §3.6, K2 |
| F6 two cuts of the question | named; `--show` sentence; instructions precede `## The question`; real-size scenario | §3.1 position invariant, E8, `fv1_3_the_real_pack_size` |
| F7 nobody accepts the conductor's reading | F-11 print-back; §1.2 row corrected | §1.2, §3.1 step 5, §3.6 |
| F8 "Not read, still open" for H6 | neutral label | §3.1, E9, §8 |
| F9 K3 receipts | cut to new-behaviour rows; moved to the threshold file; K2 takes the real answer; limit rows assert the words FILE | K2, K3, §8 |
| F10 witness scope | every printed file under one minute; slow ones named for CI | verification run |
| F11 discarded return | `read = self.record_question_words(...)` | §3.2 step 2, §9 |
| F12 seam's second answer | residual node drafted, placement returned | siblings, §6, F-12 |
| F13 `after_close` | returned to the Lead as a finding to queue | siblings |
| F14 logs gitignored | absolute root paths; key lines quoted | §2.1 |
| F15 FV1-9 AND/OR, replay | OR in design and DoD; replay told by ids present before the loop; FV1-9 marked not dispatchable | §5 |
| axis 5 enumeration | A27: member n/a; guard = named swap | siblings, §1.1 AR-20 |
| forks of the verdict's table | F-1..F-6, F-9..F-11 decided with reasons; F-7, F-8 kept as OWNER's | §7 |

Forks returned in this round: F-7 (owner), F-8 (owner), F-12 (Lead: placement of the residual node), F-14 (Lead: crash window).

## Owner's words on F-7 (13.11.2026, verbatim) — input for the FV1-9 designer round

F-7, on the recommended option (B) "the role may withdraw its question with a recorded reason":
«роль сама может ответить на этот  вопрос, раз есть ответ на уже заданный. Если ответа нет, то показываем человеку»

The Lead's reading (labelled as a reading, to be confirmed by the owner): a question a role raises that repeats one already asked is
settled by the ROLE from the recorded answer to the earlier question when that answer exists (the row closes with the role's answer
and its source — the earlier question's id — never silently); when the earlier question has no answer yet, the person is shown the
question. Open inside the reading: with no answer yet, is the person shown the pair once (the repeat pointed at the earlier id) or
both rows. None of the spec's options A/B/C is this; the FV1-9 design is re-drawn from these words.

F-8: the owner asked what moment this is («это про какой момент? Когда у нас есть переделка вопросов?»); explained in chat, no
decision yet.

### Second round of the owner's words (14.11.2026, verbatim)

F-7, on "with no answer yet, the person sees the pair once":
«вопрос на который не ответили можно задать ещё раз в другой, более понятный формулировке, но два одинаковых вопроса в один момент
конечно не надо задавать»
Requirement: (1) two questions that ask the same thing are never shown to the person at the same moment; (2) a question that got
no answer MAY be asked again later in another, clearer wording (a re-ask in new words is legal, not a repeat to suppress); (3) from
the first round: when the earlier question HAS an answer, the role settles the repeat itself from that answer.

F-8, on option (A) "shown with one plain line naming the defect":
«надо не просто сказать что не так с вопросом, а что-то что поможет человеку на вопрос ответить»
Requirement: the question the rehearsal could not get reworked is shown WITH what helps the person answer it — not a line about the
question's defect. What that help is made of (what code already holds: the cited sources, before/now, the related open or answered
questions) is the FV1-9 design; a scout pass over the available data comes first (t-657).
