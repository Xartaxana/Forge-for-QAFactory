# FV1-9 plan critic — spec `docs/tasks/specs/20261114-fv1-9-question-repeats-spec.md` (rev. 1 + the owner's words on the forks)

Critic (Opus), plan gate, 14.11.2026. Tree checked: `.claude/worktrees/read-main` at `d5059a5` (origin/main). Paths below are
relative to `ai-packages/qa-factory/` there. One pass. The owner's decisions on F-4 and F-6 (the last section of the spec,
delivered mid-review) are folded in: F-6 = (a), F-4 = «любая роль которой нужен ответ».

**Verdict: NEEDS WORK (fit_with_fixes).** The direction is right: data reaches the role first, the role judges sameness, and
one writer handles each action. F-3 (a) is sound with a tighter predicate. Four findings block builder dispatch, and all four
can be fixed in the spec text without redesign:
- B1: a hidden repeat strands everything that rests on it.
- B2: the person cannot see, judge or undo the merge that hides a question from them.
- B3: `--reword` does not protect meaning under a shared id. The owner's F-4 widens this door to every role.
- B4: the gate-top line T8 contradicts the block it sits in, and it names hidden rows.

## Findings

### B1 (blocks) — what rests on a hidden repeat never settles, but T2 tells the person "your answer is the answer to both"
- Evidence. `resolve_then_oracle` (`scripts/contract.py:1810-1870`) reads the Then's OWN ref. When status != `answered`, the
  result is "the question is {status}" and stays `open`. A Then `unknown:Q16` whose Q16 is `repeat` therefore never settles.
  §4 TEMPORAL (iii) says "a case validated before stays pinned", so pinned cases keep Q16.
- Plan rows. D3 repoints the plan row through `planning_contract.repoint_question_ref`. `_repoint_obstacle`
  (`scripts/planning_contract.py:3012-3018`) needs BOTH questions to carry claim marks
  (`does not say which of its readings is the behaviour now`). An S2 reading question (Q1-Q3, the very case of the run) never
  carries them. So the move always falls back to `append_question_ref`: the row's `if_answered[Q16]` branch stays, and the
  note says "the strategist's rework sets the branch". No step dispatches that rework.
- The conductor's CLI `--repeat` repoints nothing at all.
- Result. The person answers Q7 once. The cases and plan rows keyed by Q16 do not move. T2 promised the opposite, which
  breaks P22 ("promised and not done"). AR-22 also breaks: the readers of Q16 lose their producer, the person's answer.
- Change to the spec. `record(status="repeat")` refuses, naming the dependants, while any artifact still keys the hidden id
  other than through the declaring case's own Thens: a plan row's `question_refs`/`if_answered`, or another case's
  `then_oracles`/`question_thens`. This is an xref check, census class `xref`. The door is "repoint them first (the
  strategist's rework for a plan row, the case designer for a case), then declare". The declaring designer repoints its own
  Thens in the same round, as T12 says.
- Code never maps letters between the two questions (AR-29), so there is no "follow the target" in the resolver.
- Add a §4 row: "a declared repeat with dependants -> refused; nothing hidden". Add `fv19_repeat_refused_with_dependants` to
  N1 (the plan reader is `planning_contract`, given to N1 read-only).
- With F-3 (a) in place, the preventive road (D1/D2) makes the net (D3) rare, so this refusal costs little.

### B2 (blocks) — the hidden merge is a role's judgment with no tier above that can see or undo it (F-6 (a) kept)
- §1.2 says the sameness is "accepted by the person who sees the merge". But T2 prints only "also raised as Q16". The person
  never sees Q16's text, so they cannot tell whether it really is the same question.
- The way out offered is `--reopen` (a CLI command, not a door the person can use; FR-2, FR-57) or "an answer to Q16" (the
  person has no card for Q16).
- The designer may declare without the critic having found anything. The key is dropped once recorded (D3), so the case
  critic sees no trace in the case.
- The conductor's CLI declaration is judged by nobody.
- Change to T2: "the same question was also raised as Q16: \"<Q16 question, squeezed, first 240 characters>\". It is asked
  once, here, and your answer is the answer to both. If Q16 asks something else, write `Q16: ask separately`".
- That last phrase needs a token. If a new token is too much, use the existing door a person can type, read by the conductor
  (FV1-3's free-answer road). Name which one.
- Also: `asked_for_brief.repeats` carries `declared_by`, and T1 prints it for the case critic, so a self-declared repeat gets
  reviewed in the critic's next round. Census row: the hiding stays `xref` and the sameness judgment is the critic's and the
  person's. State this in §1.2.

### B3 (blocks) — `--reword` and the owner's F-4: meaning under a shared id

**Problem.** D4 replaces `readings[i].reading` and keeps the letters. Several artifacts key the id by letter:
- S3 plan rows `if_answered[Qn][a|b]`;
- case `question_thens` texts by letter, the non-claim road (`scripts/contract.py:846-849`,
  `scripts/planning_contract.py:2091-2104`);
- `question_effects` on the card (`scripts/gate_brief.py:2798-2806`).

A reworded reading "a" therefore inherits Thens and plan effects written for the old "a", and nothing checks that. `reworded[]`
stores only the old `question`, so even the person cannot compare the readings. The owner opened the door to "any role that
needs the answer", which multiplies the writers whose meaning drift nobody checks.

**Change to the spec (D4, N1, N3).**
- (a) Carrier: a role rewords through the form it raises through. The case designer uses a case front-matter key
  `reword_questions: [{"question": "Qn", "text": "...", "readings": [...]?, "why": "..."}]`, executed by `raise_pending`. Other
  roles use an item of the handoff `questions[]` with `rewords: Qn`, executed by `raise_from_handoff`. Both end at
  `QR.reword`, one writer. The conductor's CLI row stays (T11).
- (b) Who may: "a role that needs the answer" read as DATA. The role's own artifact names the id: its case's
  `then_oracles`/`question_thens`, its plan row's `question_refs`, the row's `asked_by` = that role, or `raised_for.case` of a
  case it owns. That is an xref check with a refusal naming the rule. A role with no such link is refused with "raise or cite
  it instead".
- (c) Protecting the meaning:
  - by default a reword changes `question` only;
  - readings' texts may change ONLY while no artifact other than the rewording role's own keys the id by letter (the B1
    dependants reader, reused);
  - `from`/`claim`/`if_chosen`/before/now and the count stay untouched, as already written;
  - `reworded[]` stores the old readings too, and T3 prints the old wording;
  - at most one reword per row between two showings to the person, so roles cannot re-reword each other unseen.
- (d) Who judges the meaning was kept: the rewording role's stage critic, in its acceptance round, because the key is
  executed at the exit step after the critic. The person also sees T3 with the earlier wording beside the new one. Code checks
  only ids, shape and dependants (census `xref`/`shape`).
- (e) Data the role needs to know a row went unanswered: add to `asked_for_brief.open[]` how many stops showed it (`shown`
  count, producer: the stop's shown-hash record in the driver state, `scripts/driver_dispatch.py:1811-1827`). Without it,
  "needs the answer" is fine but "unanswered after seeing it" (the reason to reword at all) is not visible to a role.
- (f) Reword between the stop and the answer: verified safe. The stop passes the shown hashes
  (`scripts/driver_dispatch.py:1827`, `record_answers` `scripts/question_register.py:1003`), and `record` stores them as given
  (`:862-921`), so an old-card answer falls to `changed_since_answer` True and is asked again. Correct the spec's attribution:
  it names FV1-3's `question_stop.shown`, which does not exist on main. FV1-3 is still «ожидает» in
  `plans/piles/live-run-fvf/batch-1-live-run-fvf.md:36`. The road today is `driver_dispatch.record_question_words`.
- (g) TEMPORAL: a later S2 tester publish rewrites the row from its own copy. The reword and `reworded[]` are lost, and an
  answer recorded on the reworded bytes reads as changed and is asked again. This is the same loss for which F-5 rejected
  (b) for notes. State it as accepted (toward asking) or route the reword through the tester's input.

### B4 (blocks) — T8 sits under a header that says the opposite, and a hidden repeat still reaches it
- `unrepaired_text` (`scripts/driver_gates.py:698-713`) heads its block with: "These are the factory's own to repair, not
  questions for you ... Your answer does not depend on them". T8 under it says "Q1: ... its card shows everything known about
  it", which is a question the person IS answering in the same packet. That is an FR-10 contradiction.
- `check_open_questions` (`scripts/gate_preflight.py:1997-2001`) skips only `row_answered` and `settled`. A hidden `repeat`
  row with defects still yields a finding. That finding goes to the conductor (T10 asks for a note on a hidden row), and T8
  says "its card shows ..." for a row with no card.
- Change to the spec:
  - the `open_questions` findings carrying `question` are left OUT of `unrepaired_text`. The card itself carries T6/H-lines,
    so no top line is needed and T8 is dropped. If the Lead keeps a top line, it goes in its own block with its own header,
    and the header claim stays true for the rest;
  - `check_open_questions` skips a row that is not `QR.is_open` with status `repeat`, using the single predicate of m1 below;
  - N2 owns that branch, so widen N2's `gate_preflight.py` scope from "the `add` call only" to `check_open_questions` (two
    lines) and name it in the D-0048 function list.

### Minor (fix in the same round)
- m1 (AR-13, P31, one road). "Skip a resolved repeat" is re-derived in `still_open` (P2), `report_facts._questions`,
  `asked_for_brief` and now `check_open_questions`. Add ONE predicate `QR.hidden_repeat(q)` (status `repeat`, `follows` set,
  `changed_since_answer is False`). `is_open` and every one of these readers call it. Change N1's grep DoD to a positive form:
  "`hidden_repeat` is the only reader of `follows`".
- m2. §2 F2's reader list is incomplete. Unlisted readers of `is_open` include:
  - `question_register.py:1005` (`record_answers` idempotency);
  - `:1118` (`question_lines_unread`: a stray `Q16:` line of the person is no longer flagged once Q16 is hidden; state it);
  - `question_stop.py:251` (the count limit);
  - `question_stop.py:493`;
  - `planning_contract.py:2750`;
  - `driver_machine.py:2807`;
  - `check_witness.readiness_rules` via `open_blocker`.

  None breaks, as traced: a hidden blocker repeat of an open target leaves the target blocking. List them, so a builder does not
  rediscover them.
- m3. Target reworded or rewritten after the declaration: Q16 stays hidden behind a question that may now ask something else.
  Store `target_hash` in the repeat record and hide only while the target's `row_hash` equals it. Otherwise the row is shown
  with T14-like text. Add a test row.
- m4. T1 says "If an answered question **below**". The answered rows are in "## The person's words that concern you", ABOVE
  the new section (`scripts/brief_pack.py:4530-4534`). Say "above, under the person's words".
- m5. T7. `person` -> "your choice" reads oddly in "(from your choice)"; use "what you said earlier". `claim` -> "the behaviour
  seen in the product" is wrong for the `before` reading, which is the base revision's behaviour. Use "the change under test
  (before / now)".
- m6. T6 says "the factory has found nothing more", but H3/H4 lines may already be printed above it. Say "nothing more than
  what is shown here".
- m7. Ratchets (critic question 9). New refusal sites in `question_register.py` (`reword`, `record_note`, `--repeat`) raise the
  census `blocking_per_role.conductor` (761, `scripts/tests/fixtures/judgment-census.json:4`). N1 must name the expected raise.
  AR-20 "named in the verdict" is not a DoD a Sonnet builder can meet blind.
- m8. §4 row 4 "target changed -> repeat stays hidden behind it" has no test row. Add it to `fv19_repeat_hidden_while_target_resolves`.
- m9. `question_repeats` naming the id being raised this round (`raise`) or a not-yet-written id: not stated. Refuse it as
  "malformed" (row 10).

## K1 — facts (spot-checked on read-main)
- `is_open`, `scripts/question_register.py:431-443`: False only for `with_designer`, and for settled/deferred whose `_holds`
  is true (`:364-369`). TRUE.
- `contract.py:1723` (`person` checks the raw status) and `:1726` (`unknown` needs `"before" in questions[ref]` and no
  `before_now_errors`). TRUE.
- F8 "forces an S4 twin of every open S2 question": TRUE, narrowed to "of every open S2 reading question a Then rests on".
  Nothing else in `then_oracle_errors` blocks pointing at an S2 row.
- No brief ceiling after FV1-4: `render` docstring `scripts/brief_pack.py:4524-4527` ("Nothing is measured against a size and
  nothing is dropped for room"); the only size branch is the 30 KB by-range note at `:4569-4579`. TRUE.
- `_write_readiness` at `:1364-1371` ("The caller holds `answers_lock`"), `answers_lock` at `:788`, `_append` taking the lock
  itself at `:821`, `record` at `:862` checking before `_append` (race, F4). TRUE.
- Cap refusal: `scripts/controller.py:5653-5664` ("has already had N repair round(s) about the test on this S2 window; the cap
  is N"). The spec cites `:5638-5662`, a near match. TRUE.
- Hand-over `scripts/driver_gates.py:976-1014`; `open_questions` is not in `GATE_DIRECT_CHECKS` (`:50`, only
  `question_branches`), so it does reach the conductor. TRUE.
- F11 `(from {reading.get('from', '?')})` at `scripts/gate_brief.py:2786` and `:2794`. TRUE.
- F14: a question stop does not run the rehearsal. No `gate_preflight`/`question_errors` use in `question_stop.py`;
  control: `driver_machine.py:1350` calls `gate_repair`.
- Negative checks with controls:
  - no `def shown` in `question_stop.py` (case-insensitive; control `def open_cards` found at `:384`);
  - the question card prints no `recommendation` (only a comment at `gate_brief.py:4066`; control `readings_unnameable`
    found at `:2819`).

## K2 — fit to R1-R4
- R1: met on the preventive road (D1 answered lines with question text + T12). The net (D3 on a settled target) is met only
  after B1: today the repeat's dependants never take the target's answer.
- R2: met for the person's view (hiding at every reader, after m1). Partly met in substance until B1/B2.
- R3: met in shape. Meaning safety and the owner's "any role" door need B3.
- R4: partly met.
  - The card help by fields (H5/H7/T6) reaches every stop.
  - The conductor's note (H6) exists only after a gate-A rehearsal plus the cap path (T10 sits in `conductor_text`). So the
    FIRST stop that shows a flawed S2 question carries no note. State this as accepted, or let T10's row in `conductor.md` also
    apply at a question stop.
  - The gate-top line needs B4.

## K3 — architecture and FR
- Kept: AR-1, AR-14 (two carriers, one writer), AR-16, AR-17, AR-28 (unresolved -> shown).
- Weak: AR-13 (m1), AR-22 (B1), AR-25 (B2: the person's way out), FR-10 (B4), FR-57 (B2).
- Missing from §1.1: AR-24 for the note (a free text shown to the person is not their words, but it lands on their card), and
  AR-27 (the report under the target: N2 names it, §1.1 does not).
- FR-7: kept (reword only on unanswered rows; an answer on old bytes is asked again).
- FR-12: no phrase list, kept.
- FR-40: `repeat` has exits once B2 gives the person one.
- FR-41: T6 kept (m6).
- FR-45: no validator writes, kept.
- FR-59: the hiding branch hides only on resolved data. Kept with m3.

## K4 — hiding branch cases
- Target answered then reopened: the target goes back to open, the repeat stays hidden behind it. Fine.
- Target deferred: the target is not open (`is_open` False when held), so both are deferred together; the report lists the
  target (`also`). Fine.
- Target `not_needed` or `with_designer`: hidden together. Fine.
- Target reworded or rewritten after the declaration: hidden behind possibly different meaning (m3).
- Chains and cycles: handled by `_resolve_repeats`, as the spec says.
- Declared by the designer without or against the critic: B2.
- Declaration with dependants: B1.
- Who accepts the declaration today: nobody above the declaring role. After B2: the case critic, through T1's `declared_by`,
  plus the person, through T2 with Q16's text and a door.

## K5 — `--reword` / the owner's F-4
Covered in B3. In short:
- the role door is the form key, executed by `QR.reword`;
- roles are limited to those whose own artifact names the id (data);
- readings stay frozen while others key them by letter;
- one reword per showing;
- the role's stage critic plus the person (old wording on T3) judge the meaning.

FV1-3's hashes are not needed. Today's `record_question_words` shown hashes already make a stale answer fall to "asked again".

## K6 — the note
- T4 marks it as the factory's helper's. Bound to row bytes via `row_hash` (D5). Good.
- Missing: (a) T10 and T4 must say the note does not choose a reading: "do not say which reading is right; the person
  decides". Without that the conductor becomes an oracle on the person's card (P20, FR-58).
- (b) `record_note` runs `human_text.problems` on the words and refuses on a hit (shape, an existing reader; no phrase list
  added), so plugin paths and ids do not reach the person.
- (c) A note naming "an answered question it rests on" goes stale if that row is reopened later. Accept this, or print the
  note's date.

## K7 — texts against `human-questions.md`
- No plugin path or field name. T5's `work/requirements-register.md` is a markdown document, which the file allows.
- Qn ids only.
- FR-10 breaks: T8 (B4), and T2's promise (B1).
- Wording fixes: m4, m5, m6.

## K8 — nodes
- Owns are disjoint except the B4 widening of N2 inside `gate_preflight.py` (name `check_open_questions`).
- Order FV1-3 -> N1 -> (N2 || N3), with A2 before N3 for `qa-case-critic.md`, is right.
- FV1-13's list must exclude `record_answers` too, if m2's reader at `:1005` is touched.
- What a builder would otherwise invent:
  - the dependants reader (B1/B3: name it — a `planning_contract` plan read plus `contract.case_files` front lines);
  - the census raise counts (m7);
  - the token/door for "ask separately" (B2);
  - the role-form keys of B3 (a), which belong in N1 (the `raise_pending`/`raise_from_handoff` execution) and N3 (charters
    plus `artifact-contract.md`).
- §4 edges land in test rows except row 4's target half (m8) and the new B1/B3/m3 rows.

## K9 — size
One topic of three nodes is right. D1-D5 are each needed: D1 and D2 prevent, D3 is the net, D4 is R3, D5 is R4. With F-3 (a)
the net is rare, so B1's refusal is cheap. No part should be deferred. Cut T8 (B4) rather than build it.

## K10 — judgment census
- New units: `record`(repeat) xref, `is_open` branch xref, `reword` shape + xref (B3 b, c), `record_note` shape,
  `repeats_for_case` xref, `then_oracle_errors` alterations xref. Owner `data` for all of them.
- The sameness and meaning judgments stay with roles (case critic, the rewording role's stage critic) and the person.
- No meaning check in code. `meaning-proxy` stays at 8. `blocking_per_role.conductor` rises (m7).

## F-3 (a) — judged
- F8 is true (K1).
- P20/FR-58: the relaxation lets nothing literal through. An `unknown` Then still needs a `question_thens` entry
  (`scripts/contract.py:1730-1733`). Letter-keyed entries on a non-claim question are already the supported road: they are
  read by `question_then_text` `:846-849` and checked complete by `planning_contract.py:2091-2104`. `resolve_then_oracle`
  keeps the Then `open` until a letter answer holds, and leaves own-words, changed or `not_needed` answers unresolved
  (`:1840-1870`).
- The `before` duty was about a behaviour claim. A reading question asks the requirement itself, with its readings and
  sources (`question_errors` `:625-662`), which is what the person needs.
- Error direction D7 (refuse on doubt) is right. Tighten the predicate:
  - `readings` is a list of 2 to len(QUESTION_LETTERS) dicts, each with a non-blank `reading`. More readings than letters
    leaves the card unlettered (`scripts/gate_brief.py:2775-2788`), so the Then could never settle by letter;
  - `readings_unnameable` is refused;
  - a row carrying any of `before`/`now` still goes through `before_now_errors`.
- Recommendation: accept F-3 (a) with that predicate.

## F-4 / F-6 — what each option costs the person (both now decided by the owner)
- F-6 (a), decided: the person sees one card instead of two. The cost is that a wrong merge is invisible unless T2 shows the
  twin's text and a door (B2).
- F-4, any role, decided: the person may see a question asked again in other words by whichever role needed it, more than
  once over a story. Each time costs them a re-read. Safety rests on B3: readings frozen under dependants, one reword per
  showing, the old wording shown.

## Questions only the owner can answer
1. B2: may the person split a hidden twin back out with a typed word (a new closed token such as `Q16: ask separately`), or
   only through free words read by the conductor?
2. B3 (b): does «роль которой нужен ответ» mean a role whose own work cites the question (the data reading proposed here), or
   also a role that merely reads it in its brief?

## Duplication and consistency (question 6)
Found:
- m1, the hiding rule re-derived in four readers;
- B1 and B3 should reuse ONE dependants reader rather than two;
- `_append` vs `hooklib.append_jsonl_line`, already queued by the spec (§9, axis 29), not a finding.

Grepped: `is_open(` across `scripts/*.py`; `repoint_question_ref`, `question_then_keys`, `is_claim_question(` uses.

## Code quality (question 7)
None found at the plan level (no code yet). Watch `question_card`, already about 90 lines (`scripts/gate_brief.py:2734-2825`):
adding H5, H6, T2, T3 and T6 inline pushes it further. N2 should put the help lines in one helper.

## One road (question 12)
- Hiding: one predicate once m1 is fixed.
- Declaring: one writer, two carriers.
- Rewording: one writer, carriers per F-4.
- Help: one card.

No language, project or case exclusion: grepped the spec for "only", "not for", "except", and found none that leaves a case
outside a shared mechanism. F-1 (a) keeps the brief list universal.

## Trail
Read:
- the spec (whole, incl. the owner's section);
- the recon (whole);
- `scripts/question_register.py` 140-160, 250-345, 355-470, 495-525, 780-925, 976-1012, 1108-1125, 1174-1196, 1364-1372,
  1440-1470;
- `scripts/contract.py` 621-722, 752-770, 800-900, 1599-1745, 1810-1880;
- `scripts/planning_contract.py` 2060-2110, 2735-2760, 2992-3063;
- `scripts/driver_gates.py` 50-56, 698-1020;
- `scripts/gate_preflight.py` 1620-1660, 1929-2030;
- `scripts/gate_brief.py` 2734-2830, 4162-4255;
- `scripts/brief_pack.py` 1735-1772, 4515-4600;
- `scripts/controller.py` 5600-5665;
- `scripts/validate_artifacts.py` 268-290;
- `scripts/question_stop.py` 245-256;
- `scripts/driver_dispatch.py` 1805-1830;
- `scripts/check_witness.py` 122-212;
- `references/artifact-contract.md` 126-150;
- `references/human-questions.md` 1-105;
- `references/question-vocabulary.json` 1-3;
- `scripts/tests/fixtures/judgment-census.json` 1-15;
- `plans/piles/live-run-fvf/batch-1-live-run-fvf.md` FV1 rows;
- `docs/tasks/critic-diff-brief.md` 47-105.

Greps:
- `is_open(` over `scripts/`;
- `requirements-readiness` over `scripts/`;
- `record_answers(`;
- `def shown` (control `def open_cards`);
- `recommendation` in `gate_brief.py` (control `readings_unnameable`);
- `GATE_DIRECT_CHECKS`.

No mechanical layer exists at a plan gate, so nothing was re-run.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1: a hidden repeat strands its dependants (pinned Thens unknown:Q16 never settle via resolve_then_oracle contract.py:1840; plan-row repoint always falls to append for an S2 reading target, planning_contract.py:3012-3018) while T2 promises the answer covers both - refuse a repeat while other artifacts key the id",
    "B2: the hidden merge is judged by nobody above the declaring role - T2 must show the twin's text and a door the person can use; T1 shows declared_by to the case critic",
    "B3: --reword (now open to any role per the owner's F-4) can change reading meaning under letters keyed by plan rows and question_thens - define the form carrier, the data test for which role may, frozen readings under dependants, one reword per showing, old wording on T3, the stage critic as judge",
    "B4: T8 sits under unrepaired_text's header that says these are not questions for the person (driver_gates.py:708-711, FR-10), and check_open_questions still flags hidden repeats (gate_preflight.py:1997-2001)"
  ],
  "class_completeness": "Hiding rule: walked every is_open reader on read-main (m2 lists the unlisted ones); one predicate QR.hidden_repeat required (m1). Stage twins (axis 5) covered by the one card renderer; gate A still_open and the rehearsal both need the predicate. Dependants of an id (plan rows, case question_thens, then_oracles) are one class shared by B1 and B3: one reader.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261114-fv1-9-question-repeats-spec.md",
      "docs/tasks/specs/recon/20261114-fv1-9-questions-recon.md",
      "read-main scripts/question_register.py",
      "read-main scripts/contract.py",
      "read-main scripts/planning_contract.py",
      "read-main scripts/driver_gates.py",
      "read-main scripts/gate_preflight.py",
      "read-main scripts/gate_brief.py",
      "read-main scripts/brief_pack.py",
      "read-main scripts/controller.py",
      "read-main scripts/validate_artifacts.py",
      "read-main scripts/question_stop.py",
      "read-main scripts/driver_dispatch.py",
      "read-main scripts/check_witness.py",
      "read-main references/artifact-contract.md",
      "read-main references/human-questions.md",
      "read-main references/question-vocabulary.json",
      "read-main scripts/tests/fixtures/judgment-census.json",
      "read-main plans/piles/live-run-fvf/batch-1-live-run-fvf.md",
      "docs/tasks/critic-diff-brief.md"
    ],
    "reruns": []
  },
  "fixes": [
    "B1: record(status=repeat) refuses while plan rows or other cases key the id; new edge row and test fv19_repeat_refused_with_dependants",
    "B2: T2 prints the twin's question text and a person's door to split it; asked_for_brief exposes declared_by to the case critic",
    "B3: role-side reword through the form key executed by QR.reword; data test for which role; readings frozen under other dependants; reworded[] keeps old readings; one reword per showing; stage critic judges; state the S2 republish loss",
    "B4: drop T8 (or give it its own block); check_open_questions skips hidden repeats; widen N2 scope to that function",
    "F-3 (a): tighten the predicate to 2..len(QUESTION_LETTERS) dict readings with non-blank reading, readings_unnameable refused",
    "m1-m9 as listed: one hidden_repeat predicate, full is_open reader list, target_hash, T1/T6/T7 wording, census raise named, missing test rows, malformed question_repeats",
    "K6: T4/T10 say the note never picks a reading; record_note runs human_text.problems"
  ]
}
```
