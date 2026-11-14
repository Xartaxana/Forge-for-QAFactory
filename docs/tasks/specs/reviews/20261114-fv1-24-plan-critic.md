# t-754 — critic on PLAN: FV1-24 (spec `docs/tasks/specs/20261114-fv1-24-bug-drafts-verdict-spec.md`)

Critic (Opus), 14.11.2026. One pass, before code. Nothing edited except this file. All runs are read-only, on a BYTE COPY of the ARM
story (`<scratch>/arm/LOCAL-1`, copied with `cp -r` from
`C:\QAFactory\mybooks-stand\arm-factory\test-automation-framework\qa-factory\artifacts\LOCAL-1`), importing the package from
`.claude/worktrees/read-main` (HEAD ba903eb). I checked that the tree is fresh enough for this review:
`git diff --stat ba903eb origin/main(7379e0d)` over bug_records.py, place_answers.py, driver_dispatch.py, contract.py,
place-answers.json, gate_preflight.py, finalize_task.py, driver_stage_s7.py and agents/ shows only three agent files that are not
analyst/runner (qa-case-critic, qa-requirements-tester, qa-test-strategist). The code I ran is the code on origin/main.

**Verdict: fit_with_fixes (NEEDS WORK).** K1 can be dispatched once amendments A1-A4 are in. K2 must NOT be dispatched as written:
it needs A5-A12, plus question Q1 settled (or its default taken). K5 can be dispatched with A13-A15, after B3. F-2 (a) is
rejected (it breaks P13 / P27). F-3 (a) is rejected (it creates a second reader). My recommendations differ from the Lead's choices
on F-2 and F-3. These are inputs: the decision belongs to the Lead tier (rule 6).

---------------------------------------------------------------------------------------------------------------------------

## Key 1 — Facts by trail (§0 and §9 measured)

### §0.1 (the t-1991 mechanism): CONFIRMED by reading the carrier

These line ranges hold the named functions on origin/main: place_answers `places` :294, `_requirement_list` :381-395, `_bug_list`
:453-471, `_answer_lines` :474-525, `settled_answer` :639-694, `close_unsettled` :728-820, `_line_for` :825-847; bug_records
`_walk_receipt_problem` :912-938, `_app_bug_problem` :941-945, `_current_red_problem` :948-964, `_walk_has_no_run` :967-980,
`reproduction_problems` :983-1079, `confirmation_of` :1119-1162, `_oracle_problems` :702-755, `draft_requirements` :1766-1784;
`Driver.s7_place_lines` driver_dispatch.py:4026-4068; `s7_close_places` driver_stage_s7.py:569 (called at :78, :110, :515);
`s7_places_scribe_line` :590, read by driver_stage_s8s9.py:85; finalize_task `refresh` archive: `bind_triage` plus the
`stale-triage-` writer, reason "not bound to current failure" (at :729-742 of the 726-746 window).

### §0.2 LR2-1: confirmed, with one correction (L5) and one premise that FAILS (L8)

Probe on the copy (one python stdin payload, read-only). Output, verbatim (trimmed to the load-bearing lines):

```
unconfirmed_requirements: ['R-10', 'R-11', 'R-12', 'R-8']
code_sourced_requirements: ['R-8', 'R-10', 'R-11', 'R-12']
cutoff: 2026-10-31 after: True
row keys: ['ac_ref', 'code_says', 'delta', 'derived_from', 'observable', 'parity', 'r', 'requirement', 'source']
sources: {'R-1': 'ac', 'R-2': 'ac', 'R-3': 'ac', 'R-4': 'story', 'R-5': 'story', 'R-6': 'story', 'R-13': 'story', 'R-7': 'derived', 'R-8': 'derived', 'R-9': 'story', 'R-10': 'derived', 'R-11': 'derived', 'R-12': 'derived'}
DRAFT qty-input-cart-page.json requirements: ['R-11', 'R-3'] instance: TC-009#obs1 in current: False in failure names: True walk_has_no_run: True
  confirmation_of: ('reproduced_by_factory', ['walk'], [])
  place_of_draft: draft-qty-input-cart-page
DRAFT qty-input-product-page.json requirements: ['R-3', 'R-8'] instance: TC-008#obs1 in current: False in failure names: False walk_has_no_run: False
  confirmation_of: ('unconfirmed', [], ['no APP_BUG triage row'])
  place_of_draft: case-TC-008
RECORD place-answer-case-TC-008.json bug requirement R-3 answer_problems: []
  settled_answer: (..., 'carrier missing', 'no draft carries this walk receipt (no APP_BUG triage row)')
RECORD place-answer-draft-qty-input-cart-page.json bug requirement R-3 answer_problems: []   settled_answer: 'settled'
RECORD place-answer-case-TC-010.json / req-R-2 / req-R-5: not_a_bug, settled
```

- L1-L4: confirmed. `stale-triage-7b2b5f8638725cec.json` holds `TC-008#obs1` APP_BUG, with the reason "not bound to current
  failure". `grep -c TC-008 work/triage.json` = 0 (control `TC-009#` = 27). `grep -c TC-008 work/run-report.json` = 0 (control
  `TC-009` = 144).
- L5: confirmed but needs a correction. The measured problem list is ONLY `no APP_BUG triage row`. The red-now fact never runs,
  because `walk_wide` short-circuits on the first `or` (bug_records.py:1019-1020). The spec's "`_current_red_problem` -> not
  known" is a guess, not what the code does.
- L6, L7, L10: confirmed. The findings register `work/exploratory-findings.jsonl` holds 3 lines, all `observation`, all
  recorded_by `S7-qa-failure-analyst-1`. `coverage_gap` = 0 and `unresolved_question` = 0. The `kind` grep is its own
  positive control.
- **L8 premise FAILS.** "The expectation the factory derived rode into a bug draft ... no question" is false on the question
  register. The person answered the claim questions for both derived Rs the drafts name. Question register on the copy
  (`place_answers._questions`):

```
Q4 answered 'a' | "Do you confirm these norms we derived: stock is never exceeded, a repeated add keeps one line, a failed add changes nothing, no add touches another owner's cart?"
Q5 answered 'a' | "The code behaves as listed for R-8, R-10, R-11, R-12 and no source states it: is the behaviour now the intended one?"
Q8 answered 'a' claim_confirmed: True | "Which quantities and book ids must the add refuse? Is the accepted range 1..999?"  raised_for {'case': 'TC-001', 'then': 5}
Q9 answered 'a' claim_confirmed: True | "Is a failed add meant to leave the cart unchanged and return a stable error?"   raised_for {'case': 'TC-001', 'then': 6}
Q17 answered 'a' claim_confirmed: True | "Which quantities must the product page refuse?"                               raised_for {'case': 'TC-008', 'then': 5}
claim_questions: {'R-8': 'Q5', 'R-10': 'Q5', 'R-11': 'Q5', 'R-12': 'Q5'}
Q5 claim_confirmed: False letter: None   readings: [{"id": "a", "from": "claim", "reading": "The behaviour now is the intended one", ...}, {"id": "b", "from": "claim", ...}]
```

  `unconfirmed_requirements` still lists R-8 and R-11. The reason is a reader false negative, not an absent answer.
  `_confirmed_claims` reads only `claim_questions` (R -> Q5). Q5's readings carry `from: claim` but no `claim: now` key, so
  `_claim_letter` returns None and `claim_confirmed(Q5)` = False (contract.py:1340-1369). The per-Then questions Q8, Q9 and Q17,
  which ARE `claim_confirmed`, are not tied to an R by that reader at all. The blind evaluation itself says card 1's expectation
  is "ответ владельца" (`blind-eval.md:20`).

  What card 4 really is: R-11 is about a failed ADD. The cart draft applies it to an UPDATE (`PUT /api/cart/<id>`), and reads
  "shown as a failure" as "a message on the page". That is the analyst reading the requirement wider than its words: class C
  (meaning), not class B. On correct data, K2 would not catch card 4. On ARM it catches it only because of the reader false
  negative above.

### §9 "NOT established" items: measured now

| item | result |
|---|---|
| is R-11 in `C.unconfirmed_requirements` of ARM | **yes** (and R-8, R-10, R-12) — but see L8: a false negative of the reader |
| key name of a row's source cell | **`source`** (`register_rows` docstring contract.py:1187 and the measured row keys) |
| `confirmation_of` on the ARM drafts | product page `('unconfirmed', [], ['no APP_BUG triage row'])`; cart `('reproduced_by_factory', ['walk'], [])` |
| do ARM place records stand NOW | all 5 have `answer_problems == []` (capture hashes hold) |
| K1 on ARM (simulated in memory: `_app_bug_problem` / `_walk_has_no_run` patched for instance `TC-008#obs1` only) | `simulated _no_run_target: True`; `confirmation_of: ('reproduced_by_factory', ['walk'], [])`; `settled_answer(case-TC-008): ('settled', '')` |
| K2 hits on ARM | product page names `['R-3','R-8']`, hit F-3(b) `['R-8']`, hit F-3(a) `['R-8']`, `oracle: None`; cart names `['R-11','R-3']`, hit `['R-11']` under both |
| F-3 sets | (a) `['R-10','R-11','R-12','R-7','R-8']`; (b) `['R-10','R-11','R-12','R-8']` |
| gate B on the product-page draft | `draft_verdicts: []` -> gate_preflight.py:5929 adds "TC-008 bug draft without a triage verdict" (FACTORY_FIXABLE) |
| how the requirement_silent question reaches the person | measured, see Key 5 |
| stage-joints / state-exits | no card adds a recorded state; K2 adds a refusal line of the existing `write`, and the line carries its door (FR-57). No exit row owed — I agree with the designer |

## Key 2 — Feasibility and positions

- **K1 is feasible.** `draft_triage_key`, `current_instance_results`, `triage_failures` (`names`) and `id_spellings` all exist
  with the assumed shapes. The POSITIONAL invariant is correct: the early return `if wide and not has_walk` (:1014-1015) and the
  per-entry `wide and not walking` skip (:1027-1031) both stay, so a non-walk entry keeps both facts.
- **K1 does not close instance (б) card 1 end to end.** The §1 sibling line says gate B "reads the same reader". That is FALSE:
  `gate_preflight.check_bug_drafts` reads `BR.draft_verdicts(draft, verdicts)` DIRECTLY (:5924) and blocks a draft with no
  triage verdict (:5929-5936). Its door, "S7 re-triages it", loops: finalize_task archives the row again. Only code-reading drafts
  have a positional exemption there (:5915-5923).
- **K1 and K2 together undo K1 on ARM.** The product-page draft names R-8. Under K2 (either F-3 option) R-8 is in the set and the
  draft has no `oracle`, so `_inferred_draft_list` refuses. Then `_walk_receipt_problem` -> `answer_problems` is non-empty
  (bug_records.py:935-937), the walk receipt is void, and the step falls back to `unconfirmed`. K1's TEMPORAL claim
  ("reproduced_by_factory after the commit") and the §7b live row are therefore false as soon as K2 lands. Neither card names
  the other's effect.
- **K2 is feasible as code, but its position leaves a road open.** `_inferred_draft_list` runs "only when `_bug_list` returned
  nothing". In `settled_answer` (:654-660), a record whose draft was ABSORBED by a merge drops the `_bug_list` lines and goes to
  `_settled_through`. Line :627-629 settles the place when the manifestation's `evidence` equals the answer's `seen.capture`,
  WITHOUT reading the merged draft's requirements. So an inferred R in `manifestations[].requirement` (which `draft_requirements`
  does read) rides in through a merge. That breaks K2-b's own invariant "never rides into a bug".

## Key 3 — Direction of error of K2, and the awkward inputs

The allowed direction stated in the spec is correct: DOWN. A real bug may become a question; an inferred expectation must never
be filed. But the spec's set makes DOWN fire on cases where the person already spoke. Measured on ARM: K2 would demote card 1, the
one real bug, whose expectation the owner confirmed (Q17, Q8, Q5). The awkward inputs:

| input | spec says | finding |
|---|---|---|
| several Rs, mixed sources, one `oracle.question` | refused unless the draft's `oracle` stands | **rule 15 pair, not scoped.** `_oracle_problems` in question form (:713-734) checks only that the question is answered and the quote is in the answer. It never ties the question to the inferred R. Draft {R-3 ac, R-8 derived (Q17), R-11 derived, unconfirmed} + `oracle {question: Q17}` -> passes, and R-11 rides in |
| a derived R the person confirmed | F-3(a): stays inferred unless the draft's oracle cites it | wrong under (a): union by source has no `_confirmed_claims` subtraction. Under (b) it is subtracted — but only through `claim_questions`, which misses Q5-shaped and per-Then questions (L8) |
| the answer's OWN expectation is `question`/`person` grounding that R | not stated | K2 ignores the answer's expectation and still demands the draft's `oracle`: the same word must be given twice |
| empty register (no file) | `(set(), "")`, nothing refused | an R named with no register is unknown: by the stated direction it must refuse |
| an R absent from the register | not stated | not in the set, so it passes: the error goes UP |
| no requirement at all | nothing (K2-e) | accepted |
| `requirements: "R-11"` (a string) | a test row with no expected outcome | `draft_requirements` ignores a non-list and falls back to `violates` (R-3), so R-11 escapes: UP |

## Key 4 — P27 / AR-29

No card moves "is this a bug" into code. K1 checks a join (instance membership). K2 checks a join (source cell, question
answered). Card 4's real defect (reading a requirement wider than its words) is meaning, and correctly stays with K5 and the
scribe. Census: units are functions (`judgment-census.json` `rows`, 1265 of them). `bug_records.reproduction_problems` is class
**xref** (owner data); `place_answers.answer_problems` is **xref**. §1.2 calls both "shape (join)": a wrong class. Neither
`_no_run_target` nor `_inferred_draft_list` is a refusal site of its own (the `_bug_list` siblings have no row), so I expect no
new row. But `test_judgment_census.py` is in `slow_tests.json`: its printed value must come from the branch's CI run, not from a
local witness. **F-2 (a) moves intent into code** — see Key 6.

## Key 5 — P20 / P26 literal; F-6 measured

- The three answers exist and are enforced (`_answer_lines`). **The expectation SOURCE reaches only the S8 scribe**
  (`s7_places_scribe_line`, called from driver_stage_s8s9.py:85). Case-insensitive grep `expectation` over gate_brief.py,
  report_facts.py and brief_pack.py: no hits. Positive controls with the same command shape: place_answers.py = 26 hits;
  gate_brief.py holds `confirmation_of` = 1. So the gate B packet, which code owns, shows a bug row with its step word but no
  source of the expectation. P26's "рядом с каждым вердиктом назван ИСТОЧНИК" holds only when the scribe writes it into the
  report. This is a residual no card covers: proposed node N-c.
- **F-6, measured from the code: one road inside the findings register, but two roads for "is R-n intended".**
  - A `requirement_silent` line (`_line_for`: `unresolved_question`, `oracle_status: owner_question`) reaches the person at
    gate B through `report_facts.exploratory_gate_parts` -> `questions` (:3940-3977), with the closed answer block that
    gate_brief builds.
  - After gate B is decided, the same line becomes a "Left with you" line (`_open_finding_lines` :3383-3396, which returns []
    before gate B). These two are one road in time, not a duplicate.
  - BUT the line joins a question-register row only when its `refs` carry a Q id (:3967). `_line_for` puts R ids and the case in
    `refs`, never the R's claim question (`claim_questions[R]`). So K2's door (a NEW requirement_silent place) asks the person
    about R-8 or R-11 a second time, through the findings road, while Q5, Q8, Q9 and Q17 already answered it through the question
    register. That is FR-7 (asked again with new text), P22 (asking what the factory already holds) and P31 (two roads for one
    question).
  - Whether the findings-road question goes through `human-questions.md` (AR-16): not established (not read). It is part of
    node N-b.

## Key 6 — F-2

Read today:
- `bug_records` (:335-370) writes a bug text for every draft, with the step word and its problems.
- `delivery_summary` (:327-338) lists every draft not filed as `draft` / `selected`, with `confirmation`.
- `gate_brief` (:4655-4664) shows every draft as a numbered bug row, with its step read through `confirmation_of`.
- `gate_preflight` (:6001-6009) says the gate "shows the bug as unconfirmed".
- S8 files only what gate B selected (`delivery_summary` :299-304, `selected_by_decision`).

So today the PERSON decides at gate B whether an unconfirmed draft is filed. **Recommendation (a) is wrong.** "The bug reporter
files only a draft whose place is settled" overrides the person's gate B selection in code. That breaks P13 (the person's word
passes any gate), FR-9 (what a person decides has an executor) and P27 (the person decides at gates). My recommendation, (b'):
- keep today's selection;
- show the draft's unsettled-place reason BESIDE its gate B row and its report row ("a suspected bug the factory could not
  settle: <why>");
- file only on the person's selection;
- the report counts it with its word.

This changes what a person reads, so it is an owner question (Q2). Before a card is drafted, read:
- `gate_brief` bug rows (:4630-4720);
- the S8 filing rule (`agents/qa-bug-reporter.md`, plus where S8 reads `gate_b` selections);
- `check_delivery` / `report_facts` on whether an unconfirmed or selected draft moves `delivery_ready`;
- `report_facts` bug section.

The card's files: `gate_brief.py` (bug row), `report_facts.py` (bug section). gate_preflight is NOT needed.

## Key 7 — F-3 cost

On ARM data, (a) adds only R-7 to the set. R-7 has a corroborating area case (matrix `ok:MB-cartRules-fits`) and no draft names
it, so (a) costs 0 extra questions over (b). Under EITHER set, K2 refuses both ARM drafts and its door mints 2 requirement_silent
questions. **Both are re-asks**: R-8 is answered by Q17/Q8/Q5, R-11 by Q9/Q4/Q5. The person is NOT asked something only they can
know; they are asked something they already answered (P22 "сначала разбирается сам" fails). The §7 cost line ("5 of 13 Rs
derived") is not the cost. The measured cost is 2 of 2 drafts refused and 2 of 2 questions duplicated.

**Recommend F-3 (b), against the Lead's (a).** (a) creates a second reader of "is R-n's expectation confirmed" (S5 reads
`unconfirmed_requirements`, S7 would read source ∪ that). R-7 would then be confirmed at S5 and inferred at S7: AR-13 and P31
broken (rule 19). Under (b), `inferred_requirements` is just `C.unconfirmed_requirements(text, questions)`, so no new reader and
no data row `inferred_sources` (AR-1 and AR-22 lines drop).

## Key 8 — Edges per card

- K1 has a limit, empty input, unreadable report, spelling and POSITIONAL edges. Missing: (i) the gate B twin (Key 2); (ii) the
  TEMPORAL claim must state the K2 interaction (a place-born draft naming an inferred R stays unconfirmed until the analyst splits
  it); (iii) the K1-a invariant text "absent from its attempt" contradicts the card: an instance absent from the WHOLE report IS
  lifted. Reword to "a draft whose instance the current report holds (any attempt, any spelling) keeps both facts".
- K2 has a TEMPORAL edge. It does not name the new gate B finding on old stories: a voided walk receipt (code `R_WALK_ANSWER`) is
  not `R_NO_TRIAGE`, so gate_preflight.py:6002-6009 now adds "bug draft reproduction not checkable". Missing edges: rule 15
  scoping, absorbed-draft path, answer-own-expectation, absent R, no register, `requirements` not a list (Key 3).
  `inferred_sources` absent/present: moot under F-3 (b).
- K5: see A14.

## Key 9 — Tests against docs/TESTING.md

**Blocking.** Both expected test homes are QUARANTINED: `test-layers.json` `quarantine` holds `test_walk_receipt.py`,
`test_place_answers.py` and `test_bug_reproduction.py` (cohort 8073673, entered 2026-11-11). The cards' own non-goals forbid any
edit of a quarantined file, so K1 and K2 as written have no legal test home. `scenario_walk.py --witness-for` (run from read-main)
does not print them. It prints stories `cart-1`, `local-1-0108`, `local-1-arm-b`; keep files `test_bug_records.py` (detector),
`test_place_of_draft_observation.py` (table, covers place_answers.py), `test_investigation.py`, and others.

On top of that, 18 rows, one per edge, is the "квитанция на ключ" TESTING.md removes (:55, :96). Rows on internal boundaries
(report unreadable, data row broken, sources row empty) are tests of an internal boundary, which CLAUDE.md rule 11 rules out.
The defect-born case is the ARM shape. TESTING.md wants it as ONE scenario: a variant row of a story. `local-1-arm-b` already has
the ARM register but no drafts or place records; the material is added as story fixture data, not as a new test file. The
role-written inputs (draft, answer file) get the adversarial mini-battery as variant rows of that scenario.

## Key 10 — Order and overlap

- K1 and K2 file sets are disjoint. Branch diffs (`merge-base origin/main` -> branch, `--name-only`, filtered to the K1/K2/K5
  files):
  - wip/fv1-9-ta: empty diff, already merged; the control is the non-empty output for fv1-5 and tbw-t1r.
  - wip/fv1-5: `design/role-rules.json`.
  - wip/tbw-t1r: `references/role-load.json` plus the analyst and runner slices.
  - wip/tbw-t3a: `references/role-load.json` plus the analyst and runner slices.
  - wip/fv1-22r-n1, fv1-9-n1/n2/n4/n5, tbw-t2: none.
- No collision for K1 or K2. **K5 collides with wip/tbw-t1r and wip/tbw-t3a (role-load.json) and wip/fv1-5 (role-rules.json)**,
  none of them named in §6.
- B3 is NOT on main: `git log origin/main` shows stage-critics A1a (feb7090) and A1b (34fabea, b161e3f) only, and no remote branch
  carries B3. K5 waits, as the spec says.

## Key 11 — Axes and four questions

origin/main SIBLING_MAP has 37 axes (verified; the root checkout is stale at 36). Wrong lines:
- axis 32: the census class is xref, not shape.
- axis 34 "covered": false under F-3 (a) (a second reader); true under (b).
- axis 18: the census raise is read from CI (slow file).
- axis 1, 3, 5, 13, 16, 21, 24 and the rest as written: acceptable.

Four questions:
- K2 (a): the cost line is unmeasured and wrong (Key 7).
- K1 (d): "`confirmation_of` is called by every reader of the step (report, gate B, settled_answer)" is false for gate B's verdict
  check (Key 2).
- K5 (c): acceptable.

## Key 12 — One road, class completeness

- Gate B's `draft_verdicts` block is K1's twin on the same action ("a place-born draft's evidence"). It is left uncovered and not
  queued: NEEDS WORK (A2).
- K2 closes the walk/place road only. A draft naming an unconfirmed R that is lifted by `fresh_data_rerun` / `own_script` (no
  place answer) is not reached; nor are triage APP_BUG rows citing an inferred R (`ARM/work/triage.json` cites R-11). The spec
  names these as "analogs" but queues no node: A12.
- The second question road (Key 5): proposed node N-b.
- The reader false negative (L8): proposed node N-a. Its producer is not located: a request to the coordinator for a scout
  ("who writes claim questions whose readings carry `from: claim` but no `claim` key, as Q5; how a question `raised_for
  {case, then}` maps to its R").

## Duplication and consistency (rule 18)

- K1 adds `_no_run_target` as a third reading of "does this run hold the instance", beside `_walk_has_no_run` (triage_failures
  names) and `_current_red_problem` (current_instance_results). Spec item 2 folds it into `_walk_has_no_run`, but item 3 calls it
  again for the APP_BUG fact. A3: compute it ONCE per draft in `reproduction_problems`.
- F-3 (a) duplicates the confirmed-source reader (Key 7).
- Grepped: `unconfirmed_requirements(` callers in place_answers (one, :391); `confirmation_of(` callers (gate_brief :4664,
  delivery_summary :103/:105, factory_dashboard :1285, place_answers :218/:632/:673, bug_records :362/:1607/:1643).

## Code quality (rule 18)

- The K2 door text sends the analyst to edit `expected` prose, which no check reads.
- The door "new place `new-<slug>` answered `requirement_silent`" duplicates an existing question (Key 5). It should name the
  claim question when one exists (A9).

## One road (rule 19)

F-3 (a) is a second road for "confirmed source" with no owner's word: it blocks, A5. The F-6 second question road is a residual:
proposed node N-b with owner the Lead (opens it).

---------------------------------------------------------------------------------------------------------------------------

## BINDING amendments (each one sentence)

- A1 (K1): in `bug_records._no_run_target` / §3 K1 TEMPORAL and §7b, state that a place-born draft naming an R in
  `unconfirmed_requirements` stays `unconfirmed` after K2 until the analyst splits that part off, and use the ARM product-page
  draft (R-3 + R-8) as the stated example.
- A2 (K1 sibling): open a card on `gate_preflight.check_bug_drafts` (hot file, its own node and queue line) that exempts a draft
  with no run target from the "without a triage verdict" / "without an APP_BUG verdict" findings, reading the SAME predicate as K1
  (exported from bug_records, one reader); until it lands, K1's changelog says gate B still blocks such a draft.
- A3 (K1): compute the no-run-target predicate once per draft inside `bug_records.reproduction_problems` and pass it to both the
  APP_BUG and the red-now decisions, instead of two separate calls.
- A4 (K1 and K2 tests): replace the "expected `test_walk_receipt.py` / `test_place_answers.py`" owns, which are quarantined, with
  ONE scenario variant family on story `local-1-arm-b`. The ARM drafts and place records are added as story fixture data. The
  adversarial rows cover only the role-written draft and answer. The internal-boundary rows are dropped.
- A5 (K2, F-3): take F-3 (b): `place_answers.inferred_requirements` is exactly `C.unconfirmed_requirements(text, _questions(task))`,
  with no `inferred_sources` row (AR-1/AR-22 lines and test rows K2-d, "sources row broken/empty" drop).
- A6 (K2): in `place_answers._inferred_draft_list`, scope the grounding per R. An inferred R counts as grounded only by a question
  tied to THAT R — `C.claim_questions(text)[R]`, or the record's own `expectation` of source `question`/`person` when its id
  grounds that R — never by "some answered question in `oracle`" (rule 15).
- A7 (K2): run the draft-requirements check on the absorbed-draft path too: in `place_answers.settled_answer`, before
  `_settled_through`, the claimant's `draft_requirements` go through the same check.
- A8 (K2 edges): in `place_answers._inferred_draft_list`, an R named by the draft but absent from the register, a draft naming an R
  when the story has no register, and a `requirements` field that is not a list each produce a refusal with a door (direction
  DOWN).
- A9 (K2 door): the refusal text in `place-answers.json` `line_texts.inferred_in_draft` names the R's existing claim question
  (`claim_questions[R]`) when there is one, and offers a new `requirement_silent` place only when there is none; drop the
  instruction to edit `expected` prose.
- A10 (K2 TEMPORAL): K2's changelog and edge list name the new gate B finding "bug draft reproduction not checkable"
  (gate_preflight.py:6002-6009) that a voided walk receipt raises on stories already in flight.
- A11 (§2 instance map): move "(в) card 4" from K2 to K5 plus the scribe (class C: the analyst read a confirmed add requirement as
  covering an update and a page message), and keep K2 as the class closure for "a draft's other Rs" with the measured ARM facts
  of L8 recorded in §0.2.
- A12 (class): the batch file gets a queued node, with owner the Lead, for drafts lifted by `fresh_data_rerun` / `own_script` and
  for triage APP_BUG rows that name an unconfirmed R (the same action on the non-walk roads).
- A13 (K5 order): add `очередь:` lines for K5 against wip/tbw-t1r and wip/tbw-t3a (`references/role-load.json`) and wip/fv1-5
  (`design/role-rules.json`), besides B3.
- A14 (K5 text): replace "One draft carries one expectation source" (it would split the legitimate R-3 + R-8 draft) with "a part
  that rests on what the factory inferred and no person confirmed goes to the person as a question, never into the bug".
- A15 (K5 text): add one analyst craft line on reading a requirement wider than its words (an add rule is not an update rule;
  "shown as a failure" is not "a message on the page"; read wider, it is your inference: ask).
- A16 (§1.2 / axis 32 / axis 18): correct the census classes to xref and state that the `test_judgment_census.py` value is read
  from the branch CI run (slow file).

## Proposed nodes (opened by the Lead tier, not by me)

- N-a (contract.py `_confirmed_claims` / the claim-question producer, after a scout): a person's answer to a claim question
  whose readings lack the `claim` key (Q5 shape), and a `claim_confirmed` question raised for a Then whose R is R-n (Q8/Q9/Q17),
  confirm R-n through the ONE reader. This is a meaning change for every `unconfirmed_requirements` reader, so it gets a plan
  critic (PROJECT.md package change item 6). K2 depends on it: without it, K2 refuses expectations the person confirmed.
- N-b (`place_answers._line_for` + `report_facts.exploratory_gate_parts`): a requirement_silent line carries its R's claim
  question id in `refs`, so it joins the question-register row (one road, FR-7). Also establish whether the findings-road question
  passes through `human-questions.md` (AR-16).
- N-c (gate B packet): the expectation source of a settled `bug` answer shown beside its bug row (P26 literal), not only in the
  scribe's brief.

## Questions for the owner (plain words, with my recommendation)

- Q1. The factory sometimes asked you "is the behaviour now the intended one?" and you said yes, but the check that decides
  "did a person confirm this" cannot see that answer. Until that is fixed, should a bug resting on such a point be held back as a
  question (safe, but you are asked again), or should we fix that check first and then turn the new rule on? **Recommendation:
  fix the check first (N-a), then K2; K1 and K5 go ahead now.**
- Q2. When the factory could not confirm a suspected bug, should it still appear in the bug list at gate B for you to choose
  (with the reason it could not be confirmed), or disappear from the bugs and show only as an open gap? **Recommendation: keep it
  in the list with the reason; you choose (P13).**

## What stays as the designer wrote it

F-1 (a): no objection. The finding's test line "S7 не закрывается без вердикта" should be marked superseded in the pile by the
owner's 13.11 word. F-4 (a) and F-5 (a): no objection, given A2. §5 (FV1-25 carrier): consistent with the code.

## Trail

- Read: the spec (whole).
- Read, place_answers.py: :100-229, :380-540, :614-853.
- Read, bug_records.py: :335-374, :640-800, :900-1169, :1755-1784.
- Read, contract.py: :1186-1225, :1300-1459; the `current_instance_results` head; the `triage_failures` doc.
- Read, other package code: driver_dispatch.py:4026-4069; gate_preflight.py:5870-6040; gate_brief.py:4640-4685;
  delivery_summary.py:290-359; report_facts.py:3378-3416 and :3935-3994; finalize_task.py:726-746 (grep);
  driver_stage_s7.py (grep).
- Read, data and docs: place-answers.json keys; judgment-census.json (`about`, `ratchet`, rows for place_answers and
  reproduction_problems); test-layers.json (quarantine/keep); docs/TESTING.md:1-125; SIBLING_MAP axes 24, 32, 34 (origin/main),
  axis count.
- Read, ARM: drafts (both), place-answer-case-TC-008.json, register head and matrix and claims, stale-triage file, findings
  register; blind-eval.md:18-26, 50-56, 76-80; batch-1 FV1-24/25 rows.
- Runs: the probe (Key 1); the questions probe; the K1 simulation; the git branch diffs; witness-for; the grep controls above.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "Tests: K1/K2 rows target test_walk_receipt.py and test_place_answers.py, both QUARANTINED in test-layers.json (cohort 8073673); the cards' non-goals forbid editing them; 18 per-edge rows contradict docs/TESTING.md",
    "K2 under F-3 (a) creates a second reader of 'is R-n confirmed' beside contract.unconfirmed_requirements (AR-13, P31, rule 19)",
    "K2 oracle grounding is a rule-15 pair not scoped per R: any answered question in oracle lifts every inferred R the draft names",
    "K2 is bypassed on the absorbed-draft path: settled_answer -> _settled_through :627-629 settles without reading the merged draft's requirements",
    "K2 premise on ARM rests on a reader false negative: Q5 answered a (claim readings lack the claim key) and Q8/Q9/Q17 claim_confirmed are not tied to R-8/R-11; K2 would demote card 1 whose expectation the owner confirmed and re-ask answered questions (P22, FR-7)",
    "K1 does not reach gate B: gate_preflight.check_bug_drafts reads draft_verdicts directly (:5924-5936) and blocks the place-born draft; the spec's sibling line claiming gate B reads the same reader is false",
    "F-2 (a) overrides the person's gate B selection in code (P13, FR-9, P27)"
  ],
  "fixes": [
    "A1 K1 temporal/7b: state the K2 interaction with the ARM product-page draft (R-3 + R-8)",
    "A2 open a gate_preflight.check_bug_drafts card exempting a no-run-target draft via the same exported predicate",
    "A3 compute the no-run-target predicate once per draft in reproduction_problems",
    "A4 test home: one scenario variant family on story local-1-arm-b with ARM drafts/place records as fixture data; drop internal-boundary rows",
    "A5 take F-3 (b): inferred_requirements == C.unconfirmed_requirements; no inferred_sources row",
    "A6 scope grounding per R via C.claim_questions[R] or the record's own question/person expectation",
    "A7 run the draft-requirements check on the absorbed-draft path before _settled_through",
    "A8 refuse with a door: R absent from the register, R named with no register, requirements not a list",
    "A9 door names the existing claim question; drop the edit-expected-prose instruction",
    "A10 name the new gate B 'reproduction not checkable' finding in K2's temporal edge and changelog",
    "A11 move card 4 to K5 plus scribe (class C); record L8 measured facts",
    "A12 queue a node for non-walk lifted drafts and triage APP_BUG rows naming an unconfirmed R",
    "A13 queue lines for K5 against wip/tbw-t1r, wip/tbw-t3a (role-load.json) and wip/fv1-5 (role-rules.json)",
    "A14 replace 'One draft carries one expectation source' with the inferred-and-unconfirmed wording",
    "A15 add an analyst craft line on reading a requirement wider than its words",
    "A16 census classes xref; census value read from CI (slow file)"
  ],
  "class_completeness": "NEEDS WORK. Gate B draft_verdicts is K1's uncovered twin (A2). K2 covers the walk/place road only; the fresh_data_rerun/own_script road and triage APP_BUG rows naming an unconfirmed R are not queued (A12). The absorbed-draft path is a hole inside K2 (A7). Second question road for 'is R-n intended' (findings register vs question register) proposed as node N-b; reader false negative for Q5-shaped and per-Then confirmations proposed as node N-a (scout requested for its producer); expectation source missing from the gate B packet proposed as node N-c. Axes checked against origin/main SIBLING_MAP (37 axes); axis 32 class and axis 34 claim corrected.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261114-fv1-24-bug-drafts-verdict-spec.md (whole)",
      "read-main scripts/place_answers.py:100-229,380-540,614-853",
      "read-main scripts/bug_records.py:335-374,640-800,900-1169,1755-1784",
      "read-main scripts/contract.py:1186-1225,1300-1459",
      "read-main scripts/driver_dispatch.py:4026-4069",
      "read-main scripts/gate_preflight.py:5870-6040",
      "read-main scripts/gate_brief.py:4640-4685",
      "read-main scripts/delivery_summary.py:290-359",
      "read-main scripts/report_facts.py:3378-3416,3935-3994",
      "origin/main scripts/tests/test-layers.json, fixtures/judgment-census.json, docs/SIBLING_MAP.md axes 24/32/34 and count",
      "docs/TESTING.md:1-125",
      "ARM work/bug-drafts/*.json, evidence/place-answer-case-TC-008.json, work/requirements-register.md, state/migration/stale-triage-7b2b5f8638725cec.json, work/exploratory-findings.jsonl",
      "experiments/mybooks/factory-vs-free-agent/runs/blind-eval.md:18-26,50-56,76-80"
    ],
    "reruns": [
      {"command": "python -B - <probe> (read-main scripts, ARM byte copy): unconfirmed_requirements, register_rows, confirmation_of, answer_problems, settled_answer", "result": "unconfirmed R-8,R-10,R-11,R-12; source key 'source'; product page unconfirmed ['no APP_BUG triage row']; cart reproduced_by_factory [walk]; all 5 records answer_problems []"},
      {"command": "python -B - <questions probe>: claim_questions, claim_confirmed per Q", "result": "claim_questions all -> Q5; Q5 answered a but claim_confirmed False (readings lack claim key); Q8/Q9/Q17 claim_confirmed True"},
      {"command": "python -B - <K1 simulation, in-memory patch for TC-008#obs1>", "result": "no_run_target True; confirmation_of reproduced_by_factory [walk]; settled_answer settled; K2 hits R-8 (product page) and R-11 (cart) under both F-3 options"},
      {"command": "git diff --name-only merge-base..origin/<wip branches> filtered to K1/K2/K5 files", "result": "fv1-9-ta empty; fv1-5 role-rules.json; tbw-t1r and tbw-t3a role-load.json + analyst/runner slices; others none"},
      {"command": "scenario_walk.py --witness-for bug_records.py place_answers.py place-answers.json driver_dispatch.py (read-main)", "result": "stories cart-1, local-1-0108, local-1-arm-b; keep test_bug_records.py, test_place_of_draft_observation.py, test_investigation.py ...; quarantined test_walk_receipt/test_place_answers not printed"},
      {"command": "grep -c -i expectation gate_brief.py report_facts.py brief_pack.py (control place_answers.py)", "result": "0 hits in the three; control 26"}
    ]
  }
}
```
