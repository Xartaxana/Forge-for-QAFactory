# t-772 — critic on PLAN: N-a (spec `docs/tasks/specs/20261114-fv1-24-na-claim-answer-confirms-spec.md`, designer t-763)

Critic (Opus), 14.11.2026. One pass, before code. I edited nothing except this file. Code was read in `.claude/worktrees/read-main`. I found it
at ba903eb, 26 commits behind origin/main, so I moved it (detached) to origin/main **e4df9c0** first. `git rev-parse HEAD origin/main` now
prints e4df9c0 twice. Before the move, the diff on the files in scope showed only role-rules.json (2 lines), role-load.json, role-commands.json
and SIBLING_MAP.md. All measurements ran read-only on a BYTE COPY of the real story (`cp -r` of
`...\arm-factory\test-automation-framework\qa-factory\artifacts\LOCAL-1` into my scratch). The probe scripts are in the scratchpad
(`probe1.py`..`probe5.py`), and their verbatim output is quoted below.

**Verdict: fit_with_fixes (NEEDS WORK).** Cards A and B are sound in direction and position. Card A has one certain breach that the spec
calls "may". Card B is missing two edges and a test home. **Card C must not go out as written.** On the real story, the road it relies on
already existed and lost the answer. For an answered question it also produces a re-ask whose visible text is the same, with a false
"its text changed" note. **The Lead's F-2 (a) is not right** (FR-7 in substance, P22, P9). F-1 (undated) is right only if F-2 changes.
F-4 (separate node N-a2) is right. Item 3, "not the same fact, not drafted", is right. All of this is input: the decision belongs to the Lead
tier (rule 6).

---------------------------------------------------------------------------------------------------------------------------

## Key 1 — Facts by trail; the premise re-run

The premise command of §0 was run (probe1, on the copy). Verbatim:

```
['R-10', 'R-11', 'R-12', 'R-8']
Q5 ('answered', 'a', False, False, True, "it shows before/now but its readings do not say which is the behaviour now: give each reading `claim: now|before`, once each - the case's texts cannot be tied to a reading without it", False, [])
Q8 ('answered', 'a', False, True, False, '', True, [])
Q9 ('answered', 'a', False, True, False, '', True, ['the claim of R-8 points to Q9, which is about R-11; Q5 is the question about R-8 - fix: point the claim to Q5, or name R-8 in Q9'])
Q17 ('answered', 'a', False, True, False, '', True, [])
{'R-8': 'Q5', 'R-10': 'Q5', 'R-11': 'Q5', 'R-12': 'Q5'}
```

**CONFIRMED.** Q5: `claim_confirmed` False, `before_value_needed` True, mark problem present, `settled` False, `claim_row_errors` = `[]`
(the defect). (The Q9 line is the probe's artificial row R-8->Q9, so the existing link check is expected to fire there.)

| spec fact | result |
|---|---|
| `claim_row_errors` :1466-1513, else-branch :1511 | confirmed |
| `claim_mark_problem` :869-878 | confirmed. Its text is rehearsal advice |
| `claim_reading_index` (i)/(ii)/(iii) :768-792; `_claim_letter` :795 | confirmed. Also: `_claim_letter` reads a row with NO `readings` list as the code pair (a=now). See Key 3 |
| `before_value_needed` :1788-1810 is True for any letter of an unmarked question with `before: unknown` | confirmed (:1809-1810) |
| callers of `claim_row_errors`: `validate_artifacts.check_behaviour_claims` (:717), `exit_gate.collect_errors` (:1338), `claim_projector` :180/:621/:854 | confirmed. Projector :854 judges only `origin: S3-grounding` rows (:848). Its questions are code-built and marked, so card B adds nothing there |
| `scoped_errors` hands register errors to S2 only | confirmed: in `references/stages.json` only S2 lists `work/requirements-register.md` |
| the tester's loaded slice never names `claim` | confirmed. inject-map :28-35 loads common-rules, handoff-keys, artifact-contract and vocabularies slices. Slice artifact-contract.md:60-61 says only "both `from: claim`". The "fixed pair" sentence lives ONLY in the tester's slice (grep over all slices: one hit). §9 item "other roles re-rendered?" resolved: none |
| Q5 has the handoff shape (`sources_say`, `{id, reading, cost}`, `statement`) | confirmed. Nothing in scripts projects handoff into readiness: `sources_say` appears only in `handoffs/s2-tester-to-strategist.yaml:86` and `handoff-keys.md:48` (grep, non-test). The role wrote that form itself |
| "no variants.json exists" | confirmed by `find` over `fixtures/stories` (control: 4 `story.json` found) |
| §9 "did gate A raise a rehearsal finding for Q5" | **measured: YES** (Key 4) |
| `role-load.json` margin of the tester (§9) | **measured: zero.** See Key 7. This is a certain breach, not a "may" |

**Stale/wrong:** §9's unknowns, all now measured. §3 card C's AFTER world (wrong on the real story, Key 4). Card A E-A1 "may move"
(certain, Key 7).

## Key 2 — Feasibility and positions of A, B, C

- **A:** feasible. Anchor :342 of role-rules.json is present on origin/main. `contract_slices.py --write` re-renders only the tester slice
  for this section.
- **B:** feasible. The position (else-branch, after `before_now_errors` is empty and `"before" in question`, before the link errors) keeps
  the stated POSITIONAL invariant: one line on a missing/malformed question, and the mark line never replaces the link line.
  **Where the role meets it:** the readiness file write does NOT carry it. A Write of a `.json` runs only `check_phase_json`
  (validate_artifacts.py:2670-2671; no `open_questions` judgement). The artifact_producer / `check_witness._readiness_form` (:138-142)
  checks only question/severity/owner_role. The role meets the refusal (a) at the register write when the readiness file already exists
  (validate_artifacts.py:705, PostToolUse on Write/Edit), else (b) at its own S2 stop (SubagentStop `exit_gate` :1338), still inside its
  dispatch. That is acceptable ("before it leaves S2"), but the spec must say it. It must not claim "at the write" alone.
  **A second, unstated world:** PostToolUse runs `check_register` on ANY later Write/Edit of `requirements-register.md`, at any stage. So
  the line also surfaces to whoever edits the register after S2. "S3..S9 are not newly refused" holds for stops only.
- **C:** feasible as code. `check_open_questions` (:1993-2031) skips `row_answered`, `settled`, `hidden_repeat`; Q5 reaches the loop.
  **But:** on the real story Q5 ALREADY gets an `open_questions` finding today (`question_errors`: no `source_says`, no `if_chosen`).
  See Key 4. Card C only appends the mark defect to an existing finding for Q5-shaped questions. It creates a new finding only for an
  otherwise well-formed unmarked question.

## Key 3 — Direction of error of card B; the predicate on the real story

Card B's predicate as specified, over every claim row of the copy (probe4). Verbatim:

```
R-8 Q5 reaches else: True NEW REFUSAL
R-10 Q5 reaches else: True NEW REFUSAL
R-11 Q5 reaches else: True NEW REFUSAL
R-12 Q5 reaches else: True NEW REFUSAL
today check_behaviour_claims errors: []
```

Over all 19 questions of the register: only Q5 carries a mark problem. Q7-Q19 are marked `now/before`. Q1-Q4 and Q6 have no `before`, so
the mark rule is inert for them. **No legitimate question of the real story is refused.**

| input class | card B | right? |
|---|---|---|
| code grounding rows (`GROUNDING_ROW_READINGS`, `from: claim`, no `claim`, no `before`) | never reach the else (no `before`). A claim row pointing at one already gets "does not show before/now" | yes |
| projector / S4-raise questions (`claim_readings`, marked) | accepted, by (i) | yes |
| code pair unmarked, byte-equal texts | accepted, by (ii) | yes |
| **bare row with `before`/`now` and NO `readings` list** | refused (`claim_mark_problem`: `claim_reading_index` None). Yet `_claim_letter` :798-799 reads that same row as the code pair (a=now), so `claim_confirmed` would confirm it on `a` | refusing is the right direction, but this splits one question into two readings in one module. **Must be named as an edge** (the reader stays; the gate refuses; the row is unanswerable anyway: `question_errors` "fewer than two readings") |
| one question listing several claims (Q5 -> 4 rows; arm-b Q4 -> 8 rows) | one line per row | acceptable, as spec |
| three readings / one marked / both `now` / `"Now"` / `" now"` / `1` / `null` / `["now"]` | refused (:779-785) | yes |

## Key 4 — The in-flight road (card C, F-2) on the real story

Measured on the copy (probe5: `Rehearsal(LOCAL-1,"A").check_open_questions()`), plus `state/driver-state.json`, `pipeline.json` and
`state/words/*`:

1. **Today the rehearsal already raises `open_questions-2` for Q5** ("3 defect(s): source_says ... if_chosen ..."), FACTORY_FIXABLE, with a
   waiver door. The real run recorded it too: `driver-state.json` `last_rehearsal_doors.A."open_questions-2": [{"block":"Q5",...}]`. The
   repair journal reads round 1 `repaired`, then round 2 `"outcome": "to_conductor", "stop": "no_move"`. The capped-rework conductor
   instruction (driver_gates.py:826-832) says "write a note ... **Do not rewrite the question**". So the tester road was never taken.
2. Q5 was **shown to the person again at gate A with the SAME row hash** (`driver-shownA-1794505697858.txt` and `-1794506196360.txt`:
   `"Q5": "7312c4..."`, the hash of the S3-stop answer). The card note on that showing is `gate_brief.unmarked_value_note`: "you chose a: The
   behaviour now is the intended one; the question does not say what the behaviour before the change was: say what it was". That is a
   re-ask with the same text (FR-7) and a request that is meaningless to the person (P9). The person answered "approve as is ... over every
   open item" (`pipeline.json gates.A.authorization_source`).
3. So **the loss on LOCAL-1 happened on exactly the road card C relies on.** The AFTER world of card C ("rehearsal -> tester re-mark -> one
   re-ask") is a hope, not a mechanism. It depends on a conductor rework that the repair cap and the "do not rewrite" instruction stop.
4. **Can the factory settle Q5 without the person (P22)?** Yes. On disk: the person wrote `Q5: a` (`question-answers.jsonl` line 4). Reading
   `a` is `{"id":"a","from":"claim","reading":"The behaviour now is the intended one", ...}`, and reading `b` is "The behaviour before
   (unknown) is the intended one". A ROLE reading the question can tell which reading means "now" without doubt. It needs no person.
   Code must not decide it from the wording (FR-12), but the role may (P27).
5. **F-2 (a) re-asks with the same VISIBLE text.** `row_hash` = sha256 of the whole row (question_register.py:174-181), the invisible
   `claim` keys included. A mark-only rewrite flips `changed_since_answer` to True, and the card then says "its text changed after your
   answer, so it is asked again" (gate_brief.py:4317-4318). Nothing the person reads has changed. That is FR-7 in substance, a false
   sentence to the person (P9, FR-10), and a question about what the factory already holds (P22). Only a question that ALSO needs a visible
   rewrite (Q5 does: `source_says`, `if_chosen`) is legally re-asked on changed text. Even then the meaning the person chose is
   recoverable, and P22 says the conductor settles first.
6. **F-1 (undated) has the same effect on its own:** any S2 re-dispatch of an in-flight story with an answered unmarked question is refused
   by card B until the tester marks it. The mark changes the hash, so the answer is voided and re-asked. F-1 is right only together with an
   F-2 road under which a mark-only change keeps the answer.

**My recommendation on F-2 (input; the Lead's or the owner's call):** neither (a) nor the bare (c). Recommended (d):
- The requirements tester, which owns the question, writes the two marks. The S2 critic accepts them (P27: role judges, tier above
  accepts).
- `question_register` lets an existing answer stand when its stored `row_hash` equals the hash of the CURRENT row with the readings'
  `claim` keys removed. The person saw exactly those bytes, so this is structural and hash-bound, not a reading of wording.
- The gate packet TELLS the person, without asking, which requirements their answer now confirms, with the door to change it (P13).
- Any visible change still re-asks (FR-7 legal).

Error direction of (d): a wrong mark flips meaning. The guard is: both readings marked once each, the mark-stripped hash equal to the
stored hash, the mark written only by the owner role at S2 and accepted by the S2 critic. Without the owner's word, the safe reversible
default is (c) for answered questions, with card C restricted to UNANSWERED questions (amendment C1).

## Key 5 — Readers of `unconfirmed_requirements` after a mid-story flip

The callers are coverage_contract :522/:530, manual_evidence :929, place_answers :391, traceability :1052 and validate_artifacts
:325/:1855 (grep `unconfirmed_requirements\(` non-test, plus `_confirmed_claims` / `claim_confirmed`; positive control: the definition hit at
contract.py:1443). All are pure functions recomputed at read time. A flip unconfirmed -> confirmed only REMOVES refusals: Thens with
`requirement:R-n` become legal, and a `bug` place answer on R-n is no longer refused. No recorded state is left without a way out (FR-40).
The flip can only happen at gate A (card C) or later.
- `traceability.json` is rewritten at S8 by `--write`, so it is built after the flip.
- Case Thens written at S4 as `unknown, ref Qn` stay correct: the resolver reads them through the answer.
- One stale carrier: the `answers_applied` line `not_applied: before_value_missing` for Q5 (`question-answers.jsonl` line 20). Under
  (a) a new record re-applies. Under (d) the applier must be told that a mark-only change re-opens application for the standing record.
  This edge is unnamed (AR-25).

For LOCAL-1 (past gate A) nothing flips under any card. Residual N-b, as the spec says.

## Key 6 — "Not the same fact" (item 3)

Q8 `now` = "integer 1..999 accepted, else refused" (TC-001 Then 5). Q9 = "stable error code, cart unchanged" (Then 6). Q17 = "integer 1..999
accepted" (TC-008 Then 5, page). R-8 = "whole number in an accepted range; any other value is refused **and changes nothing**". R-11 = "a
failed add (unknown book, refused input, no stock) **is shown as a failure** with a stable error and leaves the cart unchanged".
- Q8+Q9 together come close to R-8, but no single question carries a whole R.
- R-10 and R-12 have no per-Then question at all.
- `requirement` is `null` on all three, and `raised_for` has no `requirement`; the R appears only in `source_says` prose.

**The designer is right:** tying these needs a meaning judgment and has no structural link, so code must not draft it (FR-12, AR-29). Note
for N-b: the person's own words at the S3 stop say "A quantity of 0, -1, 1.5 or "abc" on the book page must be refused with a clear
message, and nothing is added" — a person's word on R-8's page side that only a role can read.

## Key 7 — P27/AR-29, census, FR-38/AR-10, role load, live branches

- Census: `claim_row_errors` stays `shape` (presence/form of two marks: data). `check_open_questions` stays `shape`. No meaning moves to
  code. Agreed.
- FR-38/AR-10: the slice sentence is sufficient IF it names the field and the two words (card A text does). The handoff form
  (`readings[].reading/cost`, `sources_say`) still contradicts it (F-4, node N-a2). Right as a separate node, but N-a2 should be opened in
  the same move with its owner, or the tester keeps copying the handoff form.
- **Role load — certain breach.** `role_load.py --role qa-requirements-tester --json` = tokens 12676 / process 11326. `role-load.json`
  has `ratchet_tokens` 12676 and `process_ratchet_tokens` 11326. `process_ratchet_problems` (role_load.py:267-290) has **no slack**: "process
  text does not grow by a token". Card A adds process text to an injected slice, so `test_role_load.py` (keep, data_join, not slow) WILL
  fail. E-A1 ("may move; builder STOPS and returns the number") guarantees a wasted round. The raise has to be named in the spec (AR-20,
  axis 18), or the sentence marked craft or offset.
- **Live branches:** origin/wip/tbw-t1r (60ddb66) and tbw-t3a (65f4232) both rewrite `references/role-load.json` (53 lines each) AND
  `scripts/contract_slices.py` (340-374 lines), the generator card A runs with `--write`. Neither touches `artifact-contract.md` or the
  tester's artifact-contract slice. So the queue line `tbw-t1r -> tbw-t3a -> fv1-24-na` is right in direction, but it must name
  `contract_slices.py` too, and it must stand in BOTH piles (PROJECT.md «Командная работа» п.3).

## Key 8 — Edges missing per card (CLAUDE.md rule 11)

- **A:** (i) the process ratchet raise is certain, not "may" (Key 7). (ii) Card A's DoD `--witness-for` list omits
  `references/role-load.json`, so `test_role_load.py`, `test_audit_rules.py` and `test_first_look_wiring.py` are not in its witness
  (measured: witness-for prints them for that path). (iii) TEMPORAL: a slice regenerated before tbw-t1r/t3a merge is stale after them;
  state which side regenerates.
- **B:** (i) where the role meets it: register write when readiness exists, else the S2 stop; never the readiness write (Key 2). (ii)
  PostToolUse on any later register write (Key 2). (iii) bare row with before/now and no `readings` (Key 3). (iv) TEMPORAL for an
  ANSWERED unmarked question on an S2 re-dispatch: the forced mark voids the answer (Key 4.6). (v) the must-stay-accepted cases (reversed
  marks; unmarked byte-equal code pair) have NO test home. The S2 door of local-1-arm-b is already refused for an unrelated reason, so a
  variant can only assert `names`, never absence. The table belongs in `test_oracle_provenance.py` (keep, gate_named, covers contract.py,
  not slow), beside its `claim_row_errors` rows :1027-1186. (vi) variant v1's value must be Q4's own readings with only `claim` removed:
  measured not byte-equal to the code pair (probe3 `code pair equal: False`), so it is refused. Say so, or a builder may write a code-pair
  value that is accepted.
- **C:** (i) answered vs unanswered (C1). (ii) the capped-rework road (driver_gates.py:826-832, "do not rewrite the question") defeats the
  re-mark. State it, or carve the mark defect out of that instruction. (iii) the `unmarked_value_note` ask on a person who chose "now" is
  reached on the real story (Key 4.2), so the claim "reached only when waived" is false: it needs a node.

## Key 9 — Tests (TESTING.md, test-layers.json, slow_tests.json)

- `test_gate_preflight_question_status.py`: keep / data_join / not slow. A right home for card C.
- `local-1-arm-b/variants.json`: scenario layer, a right home for role-written input. The S2 entry has `cut_before_seq {accepted, handed}`
  and no `variant` key, so `story_cut(entry,"variant")` = None and the variant runs on the uncut world (seq <= 58). Fine, but say it.
  `test_scenario_local_1_arm_b.py` IS slow (slow_tests.json:120, 22.8 s). The spec's "under 60 s, so the builder runs it" contradicts
  PROJECT.md "package change" p.2 ("медленный файл (`SLOW_TESTS` ...) локально не запускается и не ждётся"). The Lead decides which
  governs, or the builder runs `scenario_walk.py` for the story's variants only (if that form exists) and leaves the file to the canon.
- **K10** ("Q5 (unmarked) answered a confirms nothing", test_question_thens_claim_keys.py:308, quarantined) stays true under A/B/C as
  written and under (d): the reader is unchanged, and (d) acts on the hash, not on `claim_confirmed`.
- Missing: the accept-side table for card B (Key 8 B-v).

## Key 10 — Order, overlap, parallelism; what FV1-24 K2 may assume

Order: B depends on A (AR-10, same commit or after). C depends on the F-2 decision. One worktree, A -> B, is right. C only after the
decision, or restricted per C1. `gate_preflight.py` (hot): card C owns `check_open_questions`, and A2 of FV1-24 owns `check_bug_drafts`.
The function lists are disjoint (D-0048 form), so that is fine. role-load.json / contract_slices.py: queue after tbw-t1r and tbw-t3a
(Key 7).

**FV1-24 K2 may assume after N-a lands:** NEW stories (S2 after the commit) have marked claim questions, so the person's `a` confirms R-n
through the one reader. **It may NOT assume** that in-flight stories (LOCAL-1 and any story with an answered unmarked question) are
corrected. There K2 still refuses on a person-confirmed R unless F-2 (d) lands. K2's door must name the existing claim question (critic
t-754 A9).

## Key 11 — Four questions (rule 10); SIBLING_MAP axes

Axes counted on origin/main: `grep -cE "^#{2,3} +(Axis|Ось|axis) *[0-9]+" docs/SIBLING_MAP.md` -> **37**. This matches §6, which closes
every axis by number.
- Axis 18 must read **"covered: a named raise of `process_ratchet_tokens.qa-requirements-tester` (+ `ratchet_tokens`), certain"**, not a
  conditional.
- Axis 34 should carry the bare-row note (Key 3).
- Axis 4: the residual N-b/(d) leaves an AR-24/FR-8 instance open on in-flight stories. It needs a debt row or a queued node with a
  pointer.

Rule 10 (c) is **not met**. "The scenario variants and the test row" are regression tests of the code. "The critic's §0.2-style probe" is
not a registered detector. The leak has a deterministic signature on disk: an `answers_applied` line with `not_applied:
before_value_missing` whose question has a mark problem and whose letter is not the before-letter (LOCAL-1 line 20). Register it as a
collector row or calibration check, named in the spec. (d) "on the path" is fine for new stories.

## Key 12 — One road / class completeness (`_claim_letter(..., "before")` and siblings)

Enumeration of the readers that take "the question does not mark its readings" as None:

| site | effect on an unmarked answered question | status in the plan |
|---|---|---|
| `contract.claim_confirmed` :1353 | confirms nothing (the defect) | root cause by A+B (new stories). In-flight: N-b / F-2 |
| `contract.before_value_needed` :1809 | ANY letter needs a before value, so the question is never settled; the applier writes `before_value_missing` | not changed (agreed: safe side). Consequence below |
| `gate_brief.question_note` -> `unmarked_value_note` :4321-4326 | asks a person who chose "now" to "say what the behaviour before was" | §8 analog (2) noticed, **NOT queued** — the real story reaches it. **NEEDS WORK: queue with a pointer** |
| `contract.resolve_then_oracle` :1859 | falls to `question_then_text` -> CLAIM_NOT_MARKED (open) | safe; covered upstream by B |
| `question_register._before_from_thens` :1048 | no stamp | safe |
| `question_then_text` / `is_claim_question` | (iii) None | safe |
| `_claim_letter` bare-row branch :798 | reads a no-readings row as the code pair | contradicts card B's refusal (Key 3): name it |

The analog the spec found (the readiness form vs the handoff form, F-4) is right as N-a2. The `still_open` re-show of an answered but
unsettled question with the same hash (Key 4.2) is the same class seen from the person's side. It belongs in N-b's or (d)'s scope by name.

## Duplication and consistency (rule 18)

- Card B reuses the one judge (`claim_mark_problem` inside `claim_row_errors`): no second predicate. Good.
- Inconsistency found: `_claim_letter`'s bare-row branch vs `claim_mark_problem` give two readings of the same row (Key 3).
- Grepped: `claim_row_errors\(` callers (5 non-test sites), `unconfirmed_requirements\(` callers (7), `_claim_letter\(` (4), and
  `"texts cannot\|claim: now|before"` across the package: only the quarantined K9 and contract.py itself pin the message text. So the
  text change in card B breaks no keep test.

## Code quality (rule 18)

- Card B's new refusal text ("... qa-requirements-tester rewrites the question") names the field, the two words and the actor: FR-1/FR-2
  hold.
- The existing capped-rework instruction "Do not rewrite the question" (driver_gates.py:831) contradicts the mark defect. Card C as
  written routes the mark into a road that this sentence closes.

## One road (rule 19)

There is no exclusion of a language, project or case. Card B applies to every claim question. The S3 projector and S4 raise questions
pass by construction. No blocking residual of this class remains. The bare-row split (Key 3) is a fix of this round: name it.

---------------------------------------------------------------------------------------------------------------------------

## BINDING amendments (one sentence each)

- **A1 (card A, E-A1):** replace "may move ... STOPS" with a pre-named raise. The commit raises `process_ratchet_tokens` and
  `ratchet_tokens` of `qa-requirements-tester` by exactly the measured delta (role_load.py --role qa-requirements-tester --json, before and
  after). The commit message names it, and so does the acceptance verdict (AR-20, axis 18). The process ratchet has no slack, and the
  breach is certain at 11326/11326.
- **A2 (card A DoD):** add `references/role-load.json` to card A's `--witness-for` list, so that `test_role_load.py`,
  `test_audit_rules.py` and `test_first_look_wiring.py` are in its witness.
- **A3 (card A order):** the queue line names `references/role-load.json` AND `scripts/contract_slices.py` against origin/wip/tbw-t1r and
  tbw-t3a, written in both piles. Card A regenerates slices and re-measures role-load AFTER both merge (the late node resolves).
- **B1 (card B, where met):** state that the refusal is met at the register write when the readiness file already exists, else at the S2
  role's own stop (SubagentStop exit_gate), and never at the readiness-file write.
- **B2 (card B, TEMPORAL):** add the two missing worlds. Any post-S2 Write/Edit of the register shows the new line through PostToolUse.
  On an S2 re-dispatch of an in-flight story, an ANSWERED unmarked question must be marked, which voids its answer by hash: tie this to the
  F-2 decision.
- **B3 (card B, edge):** name the bare row (before/now, no `readings` list): refused by the gate although `_claim_letter` reads it as the
  code pair. That is the refusing direction, and the reader stays unchanged.
- **B4 (card B, test):** add the accept/refuse table (reversed marks accepted, unmarked byte-equal code pair accepted, grounding-row
  question untouched, bare row refused, the adversarial refuse list) as rows in `test_oracle_provenance.py` (keep, not slow). Pin variant
  v1's value as Q4's own readings with only `claim` removed.
- **C1 (card C):** restrict the new condition to questions with NO recorded answer. A question the person has answered is not sent back
  for a re-mark until F-2 is decided. This keeps FR-7 and P22, and it still marks every claim question before the person first sees it.
- **C2 (card C/§8):** delete the AFTER claim that the rehearsal "sends that question to the tester". Record the measured LOCAL-1 facts
  instead: rehearsal finding open_questions-2 raised; repair round 2 `to_conductor/no_move`; Q5 re-shown at gate A with the same hash and
  `unmarked_value_note`; approved over.
- **K1 (class):** queue, with a pointer and the Lead as owner, the `gate_brief.unmarked_value_note` ask on a person who chose a non-before
  reading of an unmarked question, and the same-hash re-show of an answered-but-unsettled question (Key 12). Both are reached on the real
  story.
- **K2 (rule 10 c):** register a detector for the leak. Proposed: a collector row or calibration check that flags an `answers_applied`
  line with `not_applied: before_value_missing` on a question with a `claim_mark_problem` and a letter that is not its before-letter.
- **K3 (F-4):** open node N-a2 in the same move, with its owner, so that the handoff form stops teaching `reading/cost`/`sources_say`.

## On the Lead's fork choices

- **F-1 undated — right, conditionally.** Only S2 stops and register writes see it, and its door exists. But undated + F-2 (a) re-asks
  every answered unmarked question on any S2 re-dispatch (Key 4.6). With C1 plus F-2 (d) or (c), it is right.
- **F-2 (a) — not right.** A mark-only change flips the whole-row hash, so the person sees the same visible question with a false "its text
  changed" note (FR-7 in substance, P9, FR-10). The meaning the person chose is recoverable by a role from the reading texts (P22). The
  road it relies on already failed on LOCAL-1 (repair cap, "do not rewrite"). P13: the person's word `a` is lost twice. Recommended (d)
  (Key 4). Until the owner's word: (c) for answered questions, with C1.
- **F-3 (a) — right** (Key 6).
- **F-4 (a), a separate node N-a2 — right.** Open it now (K3).
- **F-5 (a) — right:** a norm confirmation is not a behaviour-now confirmation. Q4's readings carry no `claim` and no before/now.

## Questions for the owner (plain words, with a recommendation)

- **Q1.** When you have already answered "yes, the behaviour now is intended", and the factory only later adds a hidden label to that
  question saying which answer means "now", should it (a) ask you the same question again, (b) keep your answer and tell you which
  requirements it now confirms (you can still change it), or (c) leave those requirements marked "not confirmed" for this story?
  **Recommendation: (b)**, and only when nothing you can read has changed. Any change to the wording you read means you are asked again.
  Until you decide: (c).

## Can the cards go to builders, and in what order

- **Card A + Card B:** yes, after amendments A1-A3 and B1-B4. One worktree, A then B (or one commit), queued after tbw-t1r and tbw-t3a
  for role-load.json and contract_slices.py.
- **Card C:** yes, ONLY with C1 and C2 (unanswered questions only). The answered-question road waits for the owner's word on Q1. Under
  (d) it becomes its own node: `question_register` hash tolerance plus a gate note, with its own plan critic, because it changes what
  "the text the person saw" means (PROJECT.md package change 6).
- **K1-K3:** queued nodes opened by the Lead tier (not by me).

## What stays as the designer wrote it

- The reader untouched (AR-13); item 3 not built.
- Card B's position and adversarial list; the census classes.
- The 37-axis enumeration, apart from the axis 18/34/4 lines above.
- Test homes for C (`test_gate_preflight_question_status.py`) and for role-written input (variants).
- The undated choice (with the conditions above).

## Trail

- **Read (origin/main e4df9c0, read-main):**
  - contract.py: :560-890, :1300-1615, :1786-1870
  - claim_projector.py: :590-631, :800-862
  - validate_artifacts.py: :620-720, :1711-1736, :2625-2702
  - exit_gate.py: :1276-1480
  - gate_preflight.py: :1935-2031
  - question_register.py: :40-50, :174-181, :420-515, :1030-1059
  - gate_brief.py: :4228-4327
  - driver_gates.py: :700-719, :815-834, :848-1027
  - check_witness.py: :120-254
  - role_load.py: :140-299
  - scenario_walk.py: :560-600, :781-820
  - local-1-arm-b/story.json :1-180 (of 1783), with its register claim rows and readiness Q4
  - references/inject-map.json :25-40; agents/qa-requirements-tester.md :65-95; the tester slice artifact-contract.md :57-61
  - role-rules.json :342; role-load.json keys; stages.json outputs; test-layers.json / slow_tests.json rows for 13 files
  - plans/builder-rules.md 7b; SIBLING_MAP.md headings; the t-754 review §0.2, Key 5, Key 12, proposed nodes
- **LOCAL-1 copy:** requirements-register.md :1-30, requirements-readiness.json (Q5, Q8, Q9, Q17), question-answers.jsonl, state/words/*,
  state/driver-state.json, state/conductor.jsonl gate_repair rows, pipeline.json gates.A and stage_overrides, TC-001/002/003/008 front
  matter and Thens.
- **Branches:** `git diff --stat origin/main...origin/wip/tbw-t1r|tbw-t3a` over references, role-rules, contract_slices.py.
- **Negative claims and their controls:**
  - "no code projects handoff into readiness": grep `sources_say` over the package minus tests found 2 hits, both carriers.
  - "no keep test pins the claim_mark_problem tail": grep over .py/.json/.md, where only quarantined K9 and contract.py hit.
  - "the fixed-pair sentence is only in the tester slice": grep over all slices, 1 hit (control: the source artifact-contract.md:168 hit).
  - "no variants.json": `find` (control: 4 story.json).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "Card C as written re-asks an answered unmarked claim question with identical visible text (row_hash covers invisible claim keys; gate_brief.question_note says its text changed) - FR-7 in substance, P9, P22; on LOCAL-1 the same rehearsal road already raised open_questions-2 for Q5 and lost the answer (repair round 2 to_conductor/no_move, Q5 re-shown at gate A with hash 7312c4, approved over)",
    "Card A breaches the shrink-only process ratchet with certainty: qa-requirements-tester measures 11326 process tokens against process_ratchet_tokens 11326 with no slack (role_load.py:267-290); E-A1 treats it as may and orders a stop",
    "Rule 10 (c) not met: no registered detector for the leak; the on-disk signature (answers_applied not_applied before_value_missing on a question with a claim_mark_problem and a non-before letter) is not wired"
  ],
  "class_completeness": "Siblings of 'unmarked question read as None' enumerated (claim_confirmed, before_value_needed, unmarked_value_note, resolve_then_oracle, _before_from_thens, question_then_text, _claim_letter bare-row branch): root cause covered for new stories by A+B; unmarked_value_note ask and the same-hash re-show of an answered-unsettled question are reached on the real story and not queued (K1); bare-row split to be named (B3); readiness form analog correctly queued as N-a2 (open it now, K3); 37 SIBLING_MAP axes counted on origin/main, axis 18 must be a certain named raise, axis 4 needs a debt row or node for the in-flight residual.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261114-fv1-24-na-claim-answer-confirms-spec.md",
      "docs/tasks/specs/reviews/20261114-fv1-24-plan-critic.md",
      "ai-packages/qa-factory/scripts/contract.py",
      "ai-packages/qa-factory/scripts/claim_projector.py",
      "ai-packages/qa-factory/scripts/validate_artifacts.py",
      "ai-packages/qa-factory/scripts/exit_gate.py",
      "ai-packages/qa-factory/scripts/gate_preflight.py",
      "ai-packages/qa-factory/scripts/question_register.py",
      "ai-packages/qa-factory/scripts/gate_brief.py",
      "ai-packages/qa-factory/scripts/driver_gates.py",
      "ai-packages/qa-factory/scripts/check_witness.py",
      "ai-packages/qa-factory/scripts/role_load.py",
      "ai-packages/qa-factory/scripts/tests/scenario_walk.py",
      "ai-packages/qa-factory/scripts/tests/fixtures/stories/local-1-arm-b/story.json",
      "ai-packages/qa-factory/references/inject-map.json",
      "ai-packages/qa-factory/references/role-load.json",
      "ai-packages/qa-factory/references/slices/qa-requirements-tester/artifact-contract.md",
      "ai-packages/qa-factory/design/role-rules.json",
      "ai-packages/qa-factory/scripts/tests/test-layers.json",
      "ai-packages/qa-factory/scripts/slow_tests.json",
      "plans/builder-rules.md",
      "docs/SIBLING_MAP.md",
      "LOCAL-1 byte copy: work/requirements-register.md, work/requirements-readiness.json, work/question-answers.jsonl, state/driver-state.json, state/conductor.jsonl, state/words/*, pipeline.json, work/test-cases/cart/TC-001..TC-008"
    ],
    "reruns": [
      {"command": "python -B probe1.py <copy>/LOCAL-1 (the spec's premise command)", "result": "['R-10','R-11','R-12','R-8']; Q5 claim_confirmed False, before_value_needed True, mark problem present, settled False, claim_row_errors [] - premise confirmed"},
      {"command": "python -B probe4.py <copy>/LOCAL-1 (card B predicate over every claim row)", "result": "NEW REFUSAL on R-8, R-10, R-11, R-12 (all Q5); no other question of 19 has a mark problem; today check_behaviour_claims errors []"},
      {"command": "python -B probe5.py <copy>/LOCAL-1 (Rehearsal A check_open_questions)", "result": "open_questions-2 on Q5 already raised today (source_says, if_chosen defects), FACTORY_FIXABLE, waiver door"},
      {"command": "python -B probe3.py local-1-arm-b (variant v1 value)", "result": "Q4 readings stripped of claim are not byte-equal to the code pair -> refused (code pair equal: False)"},
      {"command": "python -B role_load.py --role qa-requirements-tester --json", "result": "tokens 12676, process_tokens 11326 = ratchet_tokens 12676 / process_ratchet_tokens 11326 (no headroom)"},
      {"command": "scenario_walk.py --witness-for (card A owns incl. role-load.json; card B; card C)", "result": "role-load.json prints test_role_load.py, test_audit_rules.py, test_first_look_wiring.py; gate_preflight.py prints test_gate_preflight_question_status.py among others"},
      {"command": "grep -cE '^#{2,3} +(Axis|Ось|axis) *[0-9]+' docs/SIBLING_MAP.md (origin/main)", "result": "37"}
    ]
  },
  "fixes": [
    "A1: pre-name the raise of process_ratchet_tokens and ratchet_tokens for qa-requirements-tester by the measured delta (AR-20, axis 18) instead of stop-and-return",
    "A2: add references/role-load.json to card A witness-for so test_role_load.py runs",
    "A3: queue line names role-load.json and contract_slices.py against tbw-t1r and tbw-t3a in both piles; regenerate after both merge",
    "B1: state the refusal is met at the register write when readiness exists, else at the S2 stop, never at the readiness write",
    "B2: add TEMPORAL worlds - PostToolUse on any later register write; answered unmarked question on an S2 re-dispatch is voided by the mark (tie to F-2)",
    "B3: name the bare row (before/now, no readings list) refused while _claim_letter reads it as the code pair",
    "B4: accept/refuse table rows in test_oracle_provenance.py (keep, not slow); pin v1 as Q4 readings with only claim removed",
    "C1: restrict card C to questions with no recorded answer until F-2 is decided",
    "C2: replace card C AFTER claim with the measured LOCAL-1 facts (open_questions-2, round 2 to_conductor/no_move, same-hash re-show, approved over)",
    "K1: queue unmarked_value_note ask and same-hash re-show of answered-unsettled questions with a pointer",
    "K2: register a leak detector on answers_applied not_applied before_value_missing for unmarked claim questions",
    "K3: open node N-a2 in the same move"
  ]
}
```
