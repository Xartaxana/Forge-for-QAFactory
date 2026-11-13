# FV1-22 plan critic — S7 loops on the acceptance of S6 (critic-on-PLAN)

Spec under review: `docs/tasks/specs/20261113-fv1-22-s7-acceptance-loop-spec.md` (designer draft).
Tree of facts: `.claude/worktrees/read-main` = origin/main e4ba384 (verified: `git -C ... log -1` -> e4ba3844b2974f3e1d723fc19872fc77a3313272).
Live evidence: `C:\QAFactory\mybooks-stand\arm-factory\test-automation-framework\qa-factory\artifacts\LOCAL-1\`.
All file:line below are on read-main unless marked "arm".

**Verdict: NEEDS WORK (fit_with_fixes).** The direction holds: F1 (b) is right, and reusing `window_round_gate` is the right
survivor. But N2 as written does nothing on the very refusal of 0.2 (B1). N1 sets a new trap for every analyst dispatch that
accepts nothing (B2). N1 would also turn a keep test red, because two `known_red` rows of FV1-22 are left in place (B3). The
dotted-path relax does not work against the reader at `handoff_check.py:1577`, and it is left as an "if" for the builder (B4).
The new contract key is not contract-owned (B5). The person's way out of N2's question is not traced (B6). Six blockers, every
one a spec edit. B2 and B6 need a design decision, so they go back to the designer, or the Lead decides them. The rest the Lead
can apply directly.

---------------------------------------------------------------------------------------------------------------------------

## Q1. Facts by trail

**The cause is true on e4ba384 and agrees with the run.**
- The S7 dispatch-time contract has neither `stage_acceptance` nor `required_when` nor the author token:
  `handoffs/s7-analyst-to-automator.yaml` (0 hits).
  - The secondary contract has them: `s7-analyst-to-scribe.yaml:33-35,44-45,55-59`, and `index.yaml:63,65` (`secondary: true`).
  - `handoff.contract_of` skips secondary rows: `handoff.py:378-379`.
  - `_author_argv` is gated on `AUTHOR_TOKEN`: `story_step.py:319-336`, `handoff.py:406`.
- The reader is `acceptance.stage_acceptance_from_form`.
  - It is defined at `:1559`; the word is read at `:1566`; it is judged at `:1355,1357`.
  - It is called from `stage_done.py:1039-1042`; the refusal for the reviewed row is at `:1028-1032`.
  - The driver call is `driver_stage_plan.py:650`, reached from `driver_stage_s6.py:359` and `:387`.
- The run evidence agrees:
  - arm `state/conductor.jsonl:49-53`: the timestamps, the boundaries and the refusal text match the table in §0.2.
  - arm `S7-qa-failure-analyst-1.yaml:69-70,76`: the runner row and `verdict: concerns`.
  - arm `-4.yaml:65-70`: the runner row is gone.
  - arm `driver-question-details.md:6`.
  - Cost recomputed from `total_cost_usd` of rows 49-52: $0.6613 (the spec says ~$0.66, correct).
- **Negative claim, re-run.** Claim: "the automator contract and the analyst key page never name it". Command:
  `grep -ic "author's dispatch\|stage_acceptance"`.
  - Result: `s7-analyst-to-automator.yaml:0`, `slices/qa-failure-analyst/handoff-keys.md:0`.
  - Positive control, same call: `s7-analyst-to-scribe.yaml:4`, `slices/qa-doc-scribe/handoff-keys.md:3`. A second
    case-insensitive Grep over `handoffs/` for `stage_acceptance|required_when` hit 6 files and not the automator contract.

**Stale or wrong references (designer read f52faed; on e4ba384 these moved):**

| spec says | on e4ba384 |
|---|---|
| `handoff_check.py:1453` "the one line" (N1 owns, item 3) | `def check` is at `:1453`; the `relaxed_sections` line is `:1460`; the consumer of `relaxed` is `:1577` |
| `driver_machine.py:316-411` window_round_gate; early return `:334`; docstring `:320-322` | `:319-414`; early return `:337-338`; docstring `:323-326` |
| `window_key :302-314`, `refusal_dispatch :160-165` | `:305-317`, `:161-166` |
| `handle_refusal :413-571`; seam `:381-401`; known rows `:325-326,562-568`; empty set `:327-328`; key "" `:341-342`; answer clears nothing `:329` | `:416-576`; `:384-404`; `:328-329,567-573`; the code is at `:344-345` (empty set and key "" are ONE line, `if not key or not found: return`); `:332` |
| `driver_dispatch.py finish :842-846` / block `:838-852` | `:855-859` / `:849-865` (P1-v W0 inserted `take_checks_line` at `:836-840`) |
| `rework :2602`, cause rule `:2614-2616` | `:2644`, `:2656-2658` |
| `repair_limit_* :3010-3107` | `repair_limit_gate :3052`, `_facts :3087`, `_raise :3142` |
| test-layers quarantine rows `:9863, :8344, :9837`, quarantine starts `:7067` | `test_stage_done.py :9922`, `test_handoff_init_author.py :8403`, `test_stage_acceptance_consumer.py :9896`; quarantine starts `:7126` |
| N1-c "the `relaxed_sections` table (grep)" | there is no table. The single `relaxed_sections` call is `test_handoff.py:705`, inside the G2 loop over critic forms `:665-706` |
| N2-e "texts of `conductor.jsonl:49` and `:50` (form ids differ)" | 49 and 50 both name `S7-qa-failure-analyst-1.yaml`. The pair whose form ids differ is `:50` / `:51` |
| §0.3 (3) "`--cause tooling` spends none of the cap (`driver_dispatch.py` rework)" | the conductor ran `controller.py rework` directly (arm row 50 `did`), not `Driver.rework`. The no-cap rule is the controller's; the driver docstring only restates it |
| §4 "FV1-3 ... `question_register.py`"; N3 "`finish` is FV1-3-adjacent" | FV1-3 spec owns: `driver_dispatch.py` (`take_question_answer`, new `register_words_to_conductor`, "nothing else"), `driver_machine.py` (`_unread_halt_or_review`, one line of `take_answer`). It does NOT own `question_register.py` (its F-1) and does not touch `finish`. The `queue: FV1-3 -> N3` is unfounded |
| §1/§0.1 "S8 brief/form" twin | the S8 brief line at `driver_stage_s8s9.py:80-82` hard-codes "`header.verdict` of your form". It is a reader of the same fact and is not in N1's owns |

The refusal-string and function claims I did not list above are byte-equal on e4ba384:
`acceptance.py`, `stage_done.py`, `driver_stage_plan.py`, `driver_stage_s6.py`, `driver_stage_s7.py`, `handoff.py` and
`driver_conductor.py` are unchanged between f52faed and e4ba384 (`git diff --stat`).

## Q2. Feasibility on every road into S7 acceptance

**B1 (blocker, N2): the stop never fires on this refusal.**
- `stage_acceptance_write` calls `self.py(..., check=True, expect=...)` (`driver_stage_plan.py:650-651`). With `expect`, `py`
  raises `gate_refusal(...)` (`driver_runner.py:232-234`).
- Its text is ONE line: "the factory step stage_done.py did not complete (exit 2): expected ... the step's own words: <out>"
  (`driver_core.py:78-79`). `stage_done` prints its problems joined by "; " on one stderr line (`stage_done.py:1046`). The
  conductor's copy shows exactly that single line (arm rows 49-52).
- `findings` and `window_findings` are both empty: `Refusal.__init__` `:165-166`, and `gate_refusal` passes neither.
- So in `window_round_gate`:
  - `source = window_findings or findings or text.splitlines()[1:]` is `[]` (`driver_machine.py:341-342`);
  - `found = []`;
  - `if not key or not found: return` (`:344`).
- Result: every S7 acceptance refusal passes straight to `conductor_round`, which is the 0.2 loop unchanged. Adding
  `dispatch` (item 2) is necessary but not sufficient.
- The spec's own edge "Empty finding set ... never recorded" names this case but misses that it IS the case.
- Fix (N2 item 2): on `Refusal`, set BOTH `exc.dispatch = exc.dispatch or dispatch` AND `exc.findings = exc.findings or
  [exc.text]`. The comparison masks dispatch ids (`finding_lines`, `driver_core.py:55-64`), so the form path compares equal
  across rounds. Do NOT parse stage_done's problems out of the text (FR-12).
- N2-a must build the refusal through the real raise path: `stage_acceptance_write` with `py` stubbed to raise
  `gate_refusal(...)`. A hand-built multi-line `Refusal` would pass while the product fails, which is the
  "pin on a form nobody fills" class again.
- With the fix, D2's claim holds on the arm data: analyst-1 has scope TC-001..TC-010 (arm `controller.json`). The refusals at
  22:51 and 22:53 are both about the form of analyst-1, so they share one key, and 22:53 is `same_set` and goes to the person.

**B2 (blocker, N1): an analyst dispatch that accepts nothing gets an unfillable required field.**
- After S6 is accepted, the analyst is dispatched again: the re-triage (`s7_retriage_once`, `driver_stage_s7.py:63-70`) and
  every later S7 life. Then `awaits_acceptance("S6")` is "" and `_author_argv` returns `[]`.
- So the N1 form arrives with the `<the author's dispatch>` token row unfilled and `stage_acceptance.verdict` unfilled.
- With `required_when: {return: [...]}`, an unfilled word relaxes nothing (`handoff.py:565`). `handoff_check` refuses both
  blanks at the role's finish. The role is then resumed to fill an S6 acceptance that no code reads; it must invent a runner
  path or a word.
- E4 calls this outcome FR-59-correct. It is correct only while S6 awaits; otherwise it is a new trap (AR-23 empty outcome
  not declared; AR-25).
- The S8 twin solved the same class with `repair_carries: s8-scribe-to-gate-b: inputs_read[0].path` (`index.yaml:96-97`),
  but that covers reworks only, not a new life.
- Decision needed (designer, or Lead):
  - (i) RECOMMENDED: the two fields are owed only when the form's dispatch awaits the S6 acceptance.
    - Data/xref, census class xref, owner data: `handoff_check` asks `acceptance.awaits_acceptance` through the same reader
      `_author_argv` uses (`brief_pack.reviewed_dispatch_id`).
    - When nothing awaits, `handoff_init` drops the token row and the `stage_acceptance` section from the skeleton (the
      `--author-dispatch`-absent branch), so the role never sees them.
  - (ii) Mark both optional ("omit when your brief names no runner's handoff"). Then a missing word on an awaiting
    dispatch reaches `stage_review_exhausted(unreadable)`, one paid conductor call per occurrence instead of a finish-time
    refusal.

**Recovery road.**
- `consumer_settled` (`driver_stage_s6.py:384-388`) calls `stage_acceptance_write` with NO `stage_verdict_known` guard,
  unlike `consumer_completion` (`:357-358`) and `stage_critic_completion` (`:669-670`).
- With N1, an old or empty-word form on the recovery road is not routed to the seam. It raises through `handle_refusal`
  (bounded only once B1 is fixed).
- This is an asymmetry inside one artifact, so it gets the sweep-the-artifact-first rule: add the guard in
  `consumer_settled`. That widens N1's owns by `driver_stage_s6.consumer_settled`. If not, name it as a residual.

**Consumer review by the scribe (S8).**
- Under F2 = a, `driver_stage_s8s9.py:80-82` still tells the scribe "the verdict is `header.verdict` of your form (`ok`
  accepts it; `concerns` sends it back...)". It must be edited in the same commit (FR-37, AR-10) and added to owns.
- N2 does not wire S8. The S7-acceptance refusal at the S8 boundary keeps the unbounded conductor road until N3. Name it
  (AR-19), or add `"S8": "qa-doc-scribe"` to N2.

**B6 (blocker, N2): the person's way out of N2's question is not traced (AR-25, FR-9).**
- The `same_set` question is `no_move({"why":"threshold","kind":"refusal","call":False,"lines": refusal_lines(...)})`
  (`driver_machine.py:384-404`), at stage S7.
- S6 closes only by an accept record or a person's pass. The pass is `consumer_person_pass("S6", ...)`, which matches a live
  waiver whose `match` names the line `stage acceptance: no accept record stands for <author>` WHOLE, at stage **S6**
  (`driver_stage_s6.py:241,288`; `waiver.split_overridden` `waiver.py:202-222`).
- The spec claims "a person's `stage acceptance` waiver still passes it". It does not show that any answer to the S7
  threshold question (`go on`, `retry`, `stop`) writes that S6 waiver, records a driver accept, or reworks the analyst.
- `stage_review_exhausted` deliberately carries `lines: ["stage acceptance: <text>"]` for exactly this reason
  (`driver_stage_plan.py:705-708`, F3). The threshold question carries the stage_done text lines instead.
- If `go on` writes an S7 waiver of the refusal text, retry gives the same refusal and the same set, and the person is asked
  again: a loop of free questions with no exit. Not a paid loop, but still no way out.
- The spec must name each token's executor at this question, and test one. Recommended: for a refusal raised by
  `stage_acceptance_write`, the question's lines/block carry the STAGE_ACCEPTANCE_PHRASE line of the stage being accepted
  (S6), so `go on` is the existing person pass.

**Unknown never a pass.**
- N1 E1/E7: an empty or old word gives no record, then `stage_review_exhausted(unreadable)`. Never an accept. Holds.
- E3: an accept drops the class. Holds.

## Q3. Architecture

**Named in §1 and kept**, once the fixes below are made: AR-10, AR-13, AR-15, AR-17, AR-22, AR-23, AR-28, AR-29, AR-1.

**AR-13 is incomplete.** Readers of "the acceptance word" on e4ba384:
- `acceptance.stage_acceptance_from_form` `:1566`;
- `driver_stage_plan.stage_verdict_known` `:687`;
- `handoff_check.check` `:1460`;
- the brief texts `driver_stage_s7.py:136-137` and `driver_stage_s8s9.py:80-82`;
- the test-side writer `tests/form_filler.py:288,324-325`, which `test_field_producers._accept_form` uses with
  `verdict="concerns"` as THE reject word (`test_field_producers.py:1166-1173`).

The spec names three. The two brief lines should be built from `handoff.acceptance_verdict_path(contract)` (FR-37: the path
named in text is the path code reads), not retyped.

**Touched but unnamed:**
- AR-25 (B2, B6).
- AR-11 / AR-8 (B5: the role would see a new contract key as its own field).
- AR-20: the `known_red` rows shrink, and under F2 the role-load ratchet is raised. Both are named in the verdict of the merge.
- FR-11 is the root rule (§0.3 (1)) and should stand in §1.
- FR-37 (the brief lines).

**AR-19 / stage twins.**
- S2-S4: the stage-critic forms already carry the fields, so the producer side is fixed there. The loop-stop side is
  asymmetric: S5 and S7 are gated by N2, S2-S4 and S6 are not, until N3.
- S8: the true twin of the S7 consumer acceptance. N1 covers it under F2 = a, but its brief line is missing from owns.
  N2 does not cover it.
- If F3 = a, merge N2 into N3: wire every stage at once, keeping N2 item 2. This avoids an interim state of two roads for
  one action (P31). If F3 = b, that is an exclusion and needs the owner's word.

**Also unstated:** N2 gates every unmatched S7 refusal, not only acceptance ones. That includes refusals of the automator's
S7 repair dispatches; `window_gaps` exist only at S5 (`driver_dispatch.py:791-799`), so at S7 the cause is always `refusal`.
- With the closing role set to `qa-failure-analyst`, a series keyed on an automator dispatch is never closed by the
  automator's own completion.
- The changelog and the edges must say this blast radius.

## Q4. Error direction of reused functions; adversarial inputs

- **`relaxed_sections` / `_verdict_block`.** The spec claims "a word outside the table -> nothing relaxed". This is FALSE for
  the function. Any real word other than the keyed one relaxes every listed section (`handoff.py:564-574`: `owed_now` stays
  empty, `listed` is full). The safety comes from elsewhere: the choice validation of the filled field
  (`handoff_check.py:1585-1586`, options from the placeholder `<accept|return>`). Restate the edge with the right carrier.
  Also add a test row: word `acept` gives a choice refusal at finish.
- **B4.** Item 1d's dotted relax (`stage_acceptance.failure_class`) is matched against `path.split("[")[0].split(".")[0]`
  at `handoff_check.py:1577`, the top-level head only. A dotted entry never matches, so under `accept` the class and the
  quote stay owed. `_verdict_block` itself accepts any string, so its "if" is moot. The real edit would be at `:1577`,
  which is outside N1's owns.
  - Simpler and correct: keep `required_when: {return: [stage_acceptance]}` (whole section).
  - Under `accept` the word is by definition filled; a relax happens only when the word is a real word (`:565`).
    Placeholder or empty relaxes nothing, so the word itself stays owed.
  - No dotted path is needed. Choose this, and delete the "if" (pile rule 11).
- **`acceptance_word`.** Item 3 says an unreadable or absent contract gives `header.verdict`. Item 4 says "" when there is
  no `contract`. These contradict, and E8 ("S2-S4 unchanged") breaks under item 4 for any critic form without a `contract`
  key. Decide: no contract -> `acceptance_verdict_path("")` -> `header.verdict`, the error toward today's behaviour.
  - Nesting (a list or map at the path) gives "".
  - Case and whitespace ("Accept", " accept "): state it. `stage_acceptance_verdict` is case-sensitive; recommend strip only
    and let the choice check refuse "Accept" at finish.
  - Name the dotted getter over the plain `data` dict (`handoff.Doc.get` works on a `Doc`, not on `.data`).
- **`finding_lines` identity (advice -> gate).** The direction is right ("different" means the conductor is called). The
  missed case is the empty set (B1), which errs toward no stop at all.
- **An acceptance recorded twice.** `stage_done.py:1052-1054` writes nothing for an identical record. Holds.
- **A stale record from before the change.** `pipeline.json` `acceptance.S6` written from `header.verdict` keeps its meaning.
  Readers read the record, not the form. Holds.
- **A stale `window_rounds` series.** Edge stated; it accepts the cost of a later S7 life asking at once. Holds.

## Q5. Edges

- E1, E3, E6, E8, E9: correct.
- E2: correct, but the finish-time refusal requires B4's fix.
- E4: wrong for analyst dispatches that are not accepting S6 (B2).
- E5: deferred to F4. Fine.
- E7 TEMPORAL: correct on the live road. On the recovery road it needs the `consumer_settled` guard (Q2).
- **POSITIONAL (N2):** stated and correct (after the known rows and `code_close`, before `conductor_round`;
  `handle_refusal :567-576`).
- **Missing:**
  - the TEMPORAL world of `fixtures/form-rounds.json` (B3);
  - the CONTRACT_OWNED key (B5);
  - the S8 brief line.
- **Conflicting pairs:**
  - items 3 vs 4 (above);
  - 1d "verdict still required under accept" vs the dotted relax (B4);
  - E4 "placeholder refused (FR-59)" vs re-triage dispatches that review nothing (B2).

## Q6. Judgment (P27 / AR-29), census, money

- No new code check judges the role's meaning. accept/return stays the analyst's word; code maps it through a data table.
- The census rows in the §1 table are right. `window_round_gate` is shape over a finding set.
- B2 option (i) adds an xref unit in `handoff_check`: it needs its census row in the same commit (owner data, class xref).
- **B5.** The new top-level key `acceptance_verdict_at` must join `CONTRACT_OWNED` (`handoff.py:452-454`), as
  `required_when` and `rows_owed_when` did. Otherwise:
  - `handoff.spec` treats it as a role field;
  - `contract_slices.py --write` prints it on the analyst's key page;
  - the role may edit it in its form.
  The spec says the key is read from the template, which is right, but that does not keep it off the role's page.
  `handoff.py` owns must widen to `CONTRACT_OWNED`.
- **Money (P18).** N2's stop is `call: False`: no paid call and nothing counted twice. N1's E1/E7 road is one paid conductor
  call per occurrence, already in the conductor journal. No spend is dropped.

## Q7. Tests against `docs/TESTING.md`

- Keep-file status is correct: `test_handoff.py` keep `:2295`, `test_probe_gap_door.py` keep `:3780`.
- **B3 (blocker).** The data-join test of exactly this defect already exists in a KEEP file (TESTING.md layer 2):
  - `test_field_producers.py` (keep), registry `fixtures/form-rounds.json:27-28` (`RR-accept`, expanded over every stage with
    `acceptance_by`, using `handoff.contract_of(sits, acceptor)`, which is `s7-analyst-to-automator` for S6);
  - the two `known_red` rows of node FV1-22 at `form-rounds.json:66-67`.
  - When N1 lands, these rows turn green. The ratchet then fails the file with
    "stale: ... is green; remove its known_red row" (`test_field_producers.py:199`).
  - Under F1 (b), `_accept_form` (`:1166-1173`) fills `header.verdict: concerns` as the reject word. The S6 row must instead
    write the reject word at `acceptance_verdict_path(contract)`, else the row turns green trivially on an `accept`.
  - Required: N1 owns `test_field_producers.py` (the `_accept_form` feed only) and `fixtures/form-rounds.json` (delete rows
    66-67). These two rows are N1's witness: "the row that failed before the fix", which is TESTING.md's rule.
  - N1-a/N1-b as text-presence assertions on a template are close to the "pin" kinds the TESTING.md table forbids. Drop
    them in favour of the RR-accept rows.
- **N1-c.** Extend the G2 loop at `test_handoff.py:665-706` with `s7-analyst-to-automator` (and `s8-scribe-to-gate-b` under
  F2 = a) on the new word: `accept` -> no `stage_acceptance` problem; `return` -> class and quote owed; missing word ->
  owed; `acept` -> choice refusal. Ids name the contract and the word, as the existing ones do.
- **N1-d/e/f.** There is no acceptance block in `test_handoff.py`. The keep coverage of `stage_acceptance_from_form` is
  `test_field_producers.py:1179`; route them there. The "critic reads the pure function" fallback is not needed.
- **N2.**
  - N2-a: through the real raise path (B1).
  - N2-b: two different sets is AT the cap of 2. Add BEYOND: a third different set -> person.
  - Add the stated adversarial pair: the same text with another field named -> different.
  - N2-e: use rows `:50`/`:51`.
  - B6: one row with the person's answer -> the S6 pass recorded.
- **Limits.** The internal cap needs no battery (CLAUDE.md rule 11). The role's form is outside input (LLM-written), so the
  word gets its mini-battery in the N1-c rows: empty, nested, case, unknown word.

## Q8. Owns and crossings

**Function-level owns (N1/N2) vs other nodes:**

| other node | its functions | shared function with N1/N2? |
|---|---|---|
| FV1-3 | `driver_dispatch.take_question_answer`, new `register_words_to_conductor`; `driver_machine._unread_halt_or_review`, `take_answer` one line | NONE |
| FV1-6 | `driver_stage_plan.stage_review_exhausted`; `driver_machine.take_seam_answer`/`seam_chosen`/`seam_rework_step`; `driver_conductor.no_move_facts`/`unread`; `no_move.py` | NONE. Same file `driver_stage_plan.py` for three nodes (N1 `stage_verdict_known`, N2 `stage_acceptance_write`, FV1-6 `stage_review_exhausted`); disjoint function lists, not a hot file. Lawful under D-0048 |
| FV1-30b N1 | `controller._s5_v2_collect`, `_s5_word_index`; `window_record.py`; `branch_accounting.py` (and its N6: `driver_dispatch.window_gap`) | NONE. N2 owns only the module constant `WINDOW_ROUND_STAGES` |
| N3 | `driver_machine.window_round_gate`; `driver_dispatch.finish` `:855-859` | none with FV1-3 / FV1-6 / FV1-30b. The FV1-3 queue is not needed (see Q1) |

- **Semantic dependency to name in §4:** N1 E1/E7 send the analyst's unreadable word to `stage_review_exhausted`, which
  FV1-6 rewrites (`FINISHING_WHYS`, "running" no longer blocks the finishing dispatch). That rewrite is exactly what refused
  the conductor's rework at arm row 49. FV1-22 should name FV1-6 as the node that fixes that seam's door. There is no merge
  conflict; the later one merges main.
- **Owns are NOT sufficient.** N1 also needs:
  - `handoff.py` (`CONTRACT_OWNED`, B5);
  - `driver_stage_s8s9.py` (`stage_S8` brief line only, F2 = a);
  - `driver_stage_s6.py` (`consumer_settled`, the guard);
  - `scripts/tests/test_field_producers.py` (`_accept_form` only);
  - `scripts/tests/fixtures/form-rounds.json` (rows 66-67);
  - `handoff_check.py` `:1577` only if the dotted relax is kept (B4 recommends dropping it).
  - B2 option (i) adds `handoff_check.check` and `handoff_init` (skeleton) functions.
- **N1 and N2 may run in parallel:** disjoint functions, and each is testable alone. N3 waits for N2, or absorbs it if F3 = a.

## Q9. Executable by a weaker model?

- **N1: no, as written.**
  - Item 1d leaves an "if" to the builder (B4).
  - N1-c points at a table that does not exist.
  - N1-d/e/f are conditional.
  - The S8 brief, `CONTRACT_OWNED` and the `known_red` rows are missing.
  - After the fixes, yes.
- **N2:** executable, but it builds a no-op (B1).
- **N3:** a sketch. It has no test ids, no list of which stages' refusals change their route, and no cost statement.
- **N4:** a sketch.

## Fork table

| fork | designer rec. | critic | whose |
|---|---|---|---|
| F1 where the S6 acceptance word lives | (b) own word `stage_acceptance.verdict: accept/return` + one reader keyed by contract data | (b) is right: the 0.2 evidence shows (a) asks for a reject class the analyst never meant. Take B4's whole-section relax and B5's CONTRACT_OWNED. A data-keyed reader is not a P31 exception (one reader, data row, default) | Lead (technical; meaning change already goes through this critic, package change item 6) |
| F2 S8 scribe twin | (a) same key in S8 | (a) right, plus the S8 brief line and the S8 RR-accept row. (b) leaves two roads for one action: a P31 exception | Lead for (a); (b) = owner's word |
| F3 same-set stop beyond S5/S7 | (a) all stages (N3) | (a) right, and merge N2 into N3 so no interim asymmetric state ships. Its blast radius (S1-S4, S6, S8 refusals stop at the 2nd identical set) is a process-risk change of the factory's behaviour | **owner** (P31 exception if (b); product/process risk if (a)): ask with the cost line |
| F4 quote cites recorded evidence | (a) N4 xref at finish, all acceptor forms | (a) acceptable as data/xref, but as its own node after N1: it changes S2-S4 critics' finish too. Not a blocker of the loop | Lead; (b) leaves a P26-adjacent gap -> owner if (b) |
| new: B2 empty outcome for a non-accepting analyst | — | (i) owed only while S6 awaits (xref), skeleton drops them otherwise | designer/Lead |
| new: B6 person's door at N2's question | — | the question carries the S6 STAGE_ACCEPTANCE_PHRASE line so `go on` = `consumer_person_pass` | designer/Lead |

## Duplication and consistency

- **Finding:** the acceptance word is retyped in two brief lines (`driver_stage_s7.py:136-137`, `driver_stage_s8s9.py:80-82`)
  as `header.verdict`. They should read through `handoff.acceptance_verdict_path` (AR-13).
- `consumer_settled` vs `consumer_completion` / `stage_critic_completion`: the `stage_verdict_known` guard is missing on one
  of three (Q2).
- Searched: `grep -n "header.verdict\|get(\"header\")"` over the `scripts/` readers named above.

## Code quality

- No code yet. Spec quality: the "if" in item 1d and the items 3/4 contradiction (Q4).
- §0.2 cites a quarantined test comment (`test_stage_done.py:107`) as the carrier of the role-load slack. The carrier is
  `references/role-load.json` and its keep test.

## One road (P31, question 12)

- F1 (b): one reader with a data default. Not an exclusion.
- F2 (b) and F3 (b) are exclusions and need the owner's word.
- N2 alone, shipped before N3, is an interim two-road state (S5/S7 vs the rest). Merge it, or name it with its owner.

## Class completeness (SIBLING_MAP)

- **Axis 5, "author + critic repair loop" and "one question for every stop":** the S2-S4/S6/S8 stop is N3. The S8 consumer
  twin is half-covered (form yes, brief no, stop no).
- **Axis 5, "required lists <-> null outcomes":** the new conditional section and the reviewed row are covered by keep
  `test_null_outcomes.py`. The builder runs it if `--witness-for` prints it; B2's empty outcome is this axis.
- **Axis 18 / axis 32:** the `known_red` rows (`form-rounds.json`) and the role-load raise (F2) are named in the merge
  verdict.
- **Axis 34:** see "One road" above.
- **The "pin on a form nobody fills" class (§7):** it is real. The quarantined TR4-12 pins and the hand-built-Refusal risk
  in N2-a are both instances. The keep RR-accept registry is the right guard because it resolves the contract through
  `contract_of`. Map axis candidate: "a test resolves the form through `handoff.contract_of`, never by naming it". That is a
  proposal for the Lead; it is not added here.

## Amendments (spec section -> change); who applies

1. §3 N2 item 2 -> also `exc.findings = exc.findings or [exc.text]`. N2-a builds the refusal via `gate_refusal` through
   `stage_acceptance_write`. The edge "empty finding set" says this refusal had an empty set before. (Lead can apply.)
2. §3 N1 E4 + items 1a/1c -> declare the empty outcome for an analyst dispatch that accepts nothing (B2, option (i)
   recommended); census row for the new xref. (Designer/Lead decision.)
3. §3 N1 owns/DoD/tests -> add `test_field_producers.py` (`_accept_form`: the reject word at `acceptance_verdict_path`) and
   `fixtures/form-rounds.json` (delete `known_red` rows 66-67). The witness is `test_field_producers.py` green with those
   rows gone. Drop N1-a/N1-b text pins. (Lead can apply.)
4. §3 N1 item 1d -> `required_when: {return: [stage_acceptance]}` (whole section); delete the dotted-path "if"; restate the
   "word outside the table" edge with the choice check as its carrier. (Lead can apply.)
5. §3 N1 item 3 + owns -> `acceptance_verdict_at` joins `handoff.CONTRACT_OWNED`. (Lead can apply.)
6. §3 N2 edges/tests -> name each answer's executor at the S7 threshold question. The question carries the S6
   STAGE_ACCEPTANCE_PHRASE line; add a test row for it. (Designer/Lead decision.)
7. §3 N1 items 3/4 -> no contract -> `header.verdict` (one rule); name the dotted getter; case and whitespace stated.
   (Lead can apply.)
8. §3 N1 item 6 + owns -> `driver_stage_s8s9.py` brief `:80-82`; both brief lines read `acceptance_verdict_path`.
   (Lead can apply.)
9. §3 N1 -> guard `consumer_settled` with `stage_verdict_known` (`driver_stage_s6.py:384-388`), or name it as a residual.
   (Lead can apply.)
10. §3 N1-c -> locate the G2 loop at `test_handoff.py:665-706`; rows for accept / return / missing / `acept` per contract.
    §3 N2 -> BEYOND-cap row, field-name adversarial row, `conductor.jsonl:50/:51`. (Lead can apply.)
11. §1 -> add AR-25, AR-11, AR-20, FR-11, FR-37. §2/§3 N2 -> state that it gates every unmatched S7 refusal (automator
    repair dispatches included) and S8 is not covered. (Lead can apply.)
12. §4 -> drop `queue: FV1-3 -> N3` (FV1-3 does not own `finish`); name FV1-6 as the node that rewrites the seam that
    N1 E1/E7 use; correct the FV1-3 owns (no `question_register.py`). §0 -> refresh the stale line numbers (Q1 table).
    (Lead can apply.)
13. §5 F3 -> mark it the owner's; if (a), merge N2 into N3. (Lead decision + owner.)

## Trail

- Read on read-main:
  - the spec (whole);
  - `driver_machine.py:150-180,300-590`; `driver_core.py:40-170`; `driver_runner.py:205-240`;
    `driver_stage_plan.py:630-760`; `driver_stage_s6.py:140-420`; `driver_stage_s7.py:50-175,912-930`;
    `driver_stage_s8s9.py:78-84`; `driver_dispatch.py:770-865,2644-2668`;
  - `stage_done.py:930-1054`; `acceptance.py:1555-1581` (+ grep); `handoff.py:350-588`;
    `handoff_check.py:1435-1610,1893-1916` (+ grep of DERIVERS/BY_LEAF/ROW_JUDGMENTS); `story_step.py:315-372`;
  - `handoffs/index.yaml:58-97`, `s7-analyst-to-scribe.yaml:25-62`, `s7-analyst-to-automator.yaml` (grep + `:60-70`),
    `s8-scribe-to-gate-b.yaml:30-52`, `vocabulary.yaml:20-27,124`;
  - `waiver.py:202-222`;
  - tests `test_handoff.py:30-70,690-712`, `test_field_producers.py:1120-1200,1255-1283`, `test_probe_gap_door.py` (grep);
    `fixtures/form-rounds.json:1-40,66-67`; `test-layers.json` (grep and python probe of keep/quarantine);
    `references/null-outcomes.json` (grep);
  - `docs/TESTING.md:36-100`; `docs/SIBLING_MAP.md` axes 5, 18, 32, 34;
  - FV1-6 / FV1-3 / FV1-30b specs (grep of owns); `batch-1-live-run-fvf.md` rows.
- Diff f52faed..e4ba384 over the touched files: only `driver_core`, `driver_dispatch`, `driver_machine`, `handoff_check`,
  `story_step`, `test-layers.json` and `test_handoff.py` moved.
- Live: arm `conductor.jsonl:48-53` (and a python sum of the costs), `driver-question-details.md:6`,
  `S7-qa-failure-analyst-1.yaml:62-80`, `-4.yaml:63-72`, `controller.json` (analyst scopes).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 N2 no-op: stage_acceptance_write raises gate_refusal whose text is ONE line and carries no findings (driver_core.py:78-79, stage_done.py:1046, Refusal __init__ :165-166), so window_round_gate's source is empty and it returns at driver_machine.py:344 -> conductor every time; the 0.2 loop is unchanged",
    "B2 N1 new trap: an analyst dispatch that accepts nothing (re-triage driver_stage_s7.py:63-70, later S7 lives) gets the unfilled token row and stage_acceptance.verdict owed at finish (handoff.py:565 relaxes nothing on a placeholder), with no empty outcome declared (AR-23, AR-25)",
    "B3 N1 would turn keep test_field_producers.py red: fixtures/form-rounds.json:66-67 hold known_red rows of node FV1-22 that go stale-green; and _accept_form (:1166-1173) writes the reject word to header.verdict, wrong under F1 (b); neither file is in owns",
    "B4 N1 item 1d dotted relax cannot work: relaxed is matched against the top-level head at handoff_check.py:1577 (outside owns), and the choice is left as an if for the builder; the whole-section form is correct and simpler",
    "B5 N1 new contract key acceptance_verdict_at is not added to handoff.CONTRACT_OWNED (handoff.py:452-454): the role would see and could edit it, and the key page would list it",
    "B6 N2 the person's way out of the S7 same_set question is not traced: the S6 close needs an S6 waiver naming 'stage acceptance: no accept record stands for <author>' (driver_stage_s6.py:241,288; waiver.py:202-222); the threshold question carries the stage_done text lines at stage S7, so go on may loop (AR-25, FR-9)"
  ],
  "class_completeness": "Axis 5 twins: S8 consumer half-covered (form under F2=a yes; brief driver_stage_s8s9.py:80-82 not in owns; N2 stop does not cover S8); S2-S4/S6 stop deferred to N3 (merge N2 into N3 if F3=a, owner's fork). Inside the artifact: consumer_settled lacks the stage_verdict_known guard its two siblings have. Axis 5 null-outcomes: B2 is this axis. Axis 18/32: known_red rows and role-load raise named at merge. Axis 34: F2 (b)/F3 (b) are owner exceptions. A map-axis candidate (tests resolve forms via contract_of) is proposed to the Lead, not added.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-fv1-22-s7-acceptance-loop-spec.md",
      "read-main ai-packages/qa-factory/scripts/driver_machine.py:150-180,300-590",
      "read-main scripts/driver_core.py:40-170",
      "read-main scripts/driver_runner.py:205-240",
      "read-main scripts/driver_stage_plan.py:630-760",
      "read-main scripts/driver_stage_s6.py:140-420",
      "read-main scripts/driver_stage_s7.py:50-175,912-930",
      "read-main scripts/driver_stage_s8s9.py:78-84",
      "read-main scripts/driver_dispatch.py:770-865,2644-2668",
      "read-main scripts/stage_done.py:930-1054",
      "read-main scripts/acceptance.py:1555-1581",
      "read-main scripts/handoff.py:350-588",
      "read-main scripts/handoff_check.py:1435-1610,1893-1916",
      "read-main scripts/story_step.py:315-372",
      "read-main scripts/waiver.py:202-222",
      "read-main handoffs/index.yaml, s7-analyst-to-scribe.yaml, s7-analyst-to-automator.yaml, s8-scribe-to-gate-b.yaml, vocabulary.yaml",
      "read-main scripts/tests/test_handoff.py:30-70,690-712; test_field_producers.py:1120-1283; fixtures/form-rounds.json:1-40,66-67; test-layers.json",
      "docs/TESTING.md:36-100; docs/SIBLING_MAP.md axes 5,18,32,34",
      "docs/tasks/specs/20261113-fv1-6-*, 20261113-fv1-3-*, 20261113-fv1-30b-* (owns)",
      "arm LOCAL-1 state/conductor.jsonl:48-53, driver-question-details.md:6, work/handoffs/S7-qa-failure-analyst-1.yaml:62-80, -4.yaml:63-72, state/controller.json"
    ],
    "reruns": [
      {"command": "git -C read-main log -1 --format=%H", "result": "e4ba3844b2974f3e1d723fc19872fc77a3313272"},
      {"command": "git diff --stat f52faed e4ba384 -- <touched files>", "result": "moved: driver_core, driver_dispatch, driver_machine, handoff_check, story_step, test-layers.json, test_handoff.py; unchanged: acceptance, stage_done, driver_stage_plan/s6/s7, handoff, driver_conductor, handoffs/*"},
      {"command": "grep -ic \"author's dispatch|stage_acceptance\" s7-analyst-to-automator.yaml s7-analyst-to-scribe.yaml slices/qa-failure-analyst/handoff-keys.md slices/qa-doc-scribe/handoff-keys.md", "result": "0, 4, 0, 3 (negative confirmed with positive control in the same call)"},
      {"command": "python sum of total_cost_usd, arm conductor.jsonl rows 49-52", "result": "0.6612676"},
      {"command": "python probe test-layers.json keep/quarantine", "result": "test_handoff.py keep, test_probe_gap_door.py keep, test_field_producers.py keep, test_null_outcomes.py keep; test_stage_done/test_handoff_init_author/test_stage_acceptance_consumer quarantine (:9922/:8403/:9896)"},
      {"command": "python print S7 analyst dispatch scopes from arm controller.json", "result": "analyst-1 TC-001..TC-010; analyst-2..4 TC-005"}
    ]
  },
  "fixes": [
    "s3 N2 item 2 -> set exc.findings = exc.findings or [exc.text] as well as dispatch; N2-a builds the refusal through stage_acceptance_write with py raising gate_refusal",
    "s3 N1 E4/items 1a,1c -> declare the empty outcome for an analyst dispatch that accepts nothing (recommended: owed only while S6 awaits, xref via brief_pack.reviewed_dispatch_id; skeleton drops token row and section otherwise; census row)",
    "s3 N1 owns/DoD -> add tests/test_field_producers.py (_accept_form writes the reject word at acceptance_verdict_path) and fixtures/form-rounds.json (delete known_red rows 66-67); witness = that file green; drop N1-a/N1-b text pins",
    "s3 N1 item 1d -> required_when {return: [stage_acceptance]} whole section; delete the dotted-path branch; restate the outside-word edge with the choice check (handoff_check.py:1585-1586) as carrier",
    "s3 N1 item 3/owns -> add acceptance_verdict_at to handoff.CONTRACT_OWNED",
    "s3 N2 edges/tests -> the S7 threshold question for a stage_acceptance_write refusal carries the S6 STAGE_ACCEPTANCE_PHRASE line so go on is consumer_person_pass; name every token's executor; one test row",
    "s3 N1 items 3/4 -> one rule: no contract -> header.verdict; name the dotted getter on the data dict; state case/whitespace handling",
    "s3 N1 item 6/owns -> driver_stage_s8s9.py stage_S8 brief :80-82; both brief lines read handoff.acceptance_verdict_path",
    "s3 N1 -> guard driver_stage_s6.consumer_settled :384-388 with stage_verdict_known, or name it as a residual",
    "s3 tests -> N1-c in the G2 loop test_handoff.py:665-706 (accept/return/missing/acept per contract); N2 BEYOND-cap row, field-name adversarial row, conductor.jsonl :50/:51 pair",
    "s1/s2 -> add AR-25, AR-11, AR-20, FR-11, FR-37; state N2 gates every unmatched S7 refusal incl. automator repair dispatches and S8 is uncovered",
    "s4 -> drop queue FV1-3 -> N3; name FV1-6 (rewrites stage_review_exhausted used by N1 E1/E7); correct FV1-3 owns; s0 -> refresh stale line numbers per the Q1 table",
    "s5 F3 -> owner's fork; if (a) merge N2 into N3"
  ]
}
```
