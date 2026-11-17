# t-1077 — code critic, topic "dry story N4:gates" (t-1037, t-1044, t-1069)

Tree `C:/QAFactory/forge-repo/.claude/worktrees/agent-a4aebd95c3ca7d59c`, branch `worktree-agent-a4aebd95c3ca7d59c`, head 395f7c48,
diff `2e9cb3a9...HEAD` (9 files). Prefixes: `T/` = `<tree>/ai-packages/qa-factory/scripts/tests/`, `S/` = `<tree>/ai-packages/qa-factory/scripts/`.
Specs read: card r2 `docs/tasks/specs/20261117-p1b-gate-ask-judge-card-r2.md` (whole, including G1-G5 and N1), the walker spec
`docs/tasks/specs/20261114-p1b-n4w-exit-walker-spec.md` (live_only rules, F-W4..F-W6, DoD of an N4 part), the two builder reports in the tree,
`docs/tasks/critic-diff-brief.md` (questions 1-12).

**Verdict: NEEDS WORK (accept with fixes).** 1 blocking finding (B1: the `gate_A/rework` row is not built the way the card says,
so its red does not show the defect the report names). 6 fixes, 7 notes. The judge, the spy stamp, the `say` seed, the n/a guards
and the turn end are built as the card says. My re-runs of the selftests and `--check` match the witness. The diagnosis of key 4 has its own
section; it finds one product class under BOTH red rows and under the existing label FV3-16.

---

## Key 4 — diagnosis of the two red rows

### 4(a) `gate_A/stop` — a PRODUCT gap. The card's expectation is right.

The trace through product code, read in the tree:
1. `_run_guarded` calls `take_answer` (`S/driver_machine.py:1871-1872`).
2. `take_answer` prints `answer for gate_A (S4): stop` (`:3389`). It sets `self._answer` with kind/stage/question_sha (`:3385`, `:3391`).
3. `take_seam_answer` runs `self.answer_file()` (`:2388`). The comment there says "the token's own words file: the audit trail row of driver-answers.jsonl names it (E6)".
   Next it runs `answer_row(...)`, the story journal's `human_answer` (`:2389`). Then `stop_here` RAISES `self.held_question(self.stop_held(...))` (`:2395-2397`).
4. `record_answer_row` runs only at the END of `take_answer` (`:3614`), after every branch, so this road never reaches it.
5. The raised `Person` is caught at the run level by `except Person as person: return self.ask(person)` (`:2031-2032`). That handler writes no answer row. The run-level settle
   `settle_unread_answer` exists only in the `except Refusal` handler (`:2033-2040`). The docstring of `record_answer_row` says the same
   (`S/driver_conductor.py:235-238`: "the run()-level funnel writes it for an answer whose reading raised a **Refusal**").

The expectation comes from the product's contract, not from what the product printed:
- `design/driver.md:206`: "The person's words go to `state/driver-answers.jsonl`".
- `record_answer_row` is "written ONCE per answer" (`S/driver_conductor.py:236`).
- Two other held roads of the SAME driver write the row BEFORE they raise the held question:
  - `combine_gate_words` (`S/driver_machine.py:2487-2493`: `self.answer_file(); self.record_answer_row("")`, then `held_question`);
  - `ticket_ask_again` (`S/driver_s0.py:401-408`: "the words are recorded FIRST (FR-8: the journal's `human_answer` and `driver-answers.jsonl`, whole), then the question comes back changed (FR-7)").

So the card is right to expect an answer row for `stop`. The FR-58 source is the design text and the two sibling roads. The judge is not the source.

- **Class.** "An answer `take_answer` has read whose branch ends in a raised `Person` leaves no `driver-answers.jsonl` row."
  Rules broken:
  - AR-24 / FR-8: the person's word is not on the driver's own record.
  - AR-22: the words file created at `:2388` for that row has no row that names it.
  - P31 / AR-15: two held roads record first, the others do not.
  - The FR-7 carrier `already_answered` (`S/driver_dialog.py:381-392`) cannot see these answers.
  The words are NOT lost to the story: `human_answer` is written at `:2389`. What is lost is the driver's answer record.
- **Members of the class, by reading.** Every `Person` raised out of `take_answer`'s branches:
  - `stop_here` (`:2395-2397`);
  - `seam_chosen`'s held roads (`:2416-2418`, `:2448-2449`);
  - `record_seam_rework`'s held roads (`S/driver_conductor.py:745-753`);
  - every `no_move` that ends in `options_person` / `fallback_person`: chosen (`:2450`) and `unread` (`S/driver_conductor.py:852-869`).
- **The existing label `kind:halt/free words -> FV3-16`** (`T/fixtures/driver-exits/known_red/s0.json`, "records no answer row ... cause not located") is, by
  reading, the `unread` member of this same class. Its cause is located here.
- **Owner.** ONE product node for the class, not one label per row: FV3-16 widened, or a new node that FV3-16 joins.
  The fix site, by reading: write the row on the `except Person` road of `_run_guarded` the way `settle_unread_answer` does for `Refusal`. A local fix of only `stop_here` would leave the siblings open.
  The fix stays outside this topic's owns (product code): the Lead opens the node.
- **Label** for `T/fixtures/driver-exits/known_red/gates.json` (key `gate_A/stop`):
  `{"node": "<node>", "raised_by": "product gap (critic t-1077): an answer take_answer has read whose branch raises a Person (here the held stop question, driver_machine.py:2395-2397) leaves no driver-answers.jsonl row: record_answer_row runs only at the end of take_answer (driver_machine.py:3614) and the run-level handler settles only a Refusal (:2033-2040), not a Person (:2031-2032); same class as FV3-16"}`
- **TEMPORAL.** `gate_B/stop` will turn red the same way once S8 exists (after FV3-20). That is the right behaviour, red in the right place. The Lead may plan its label with the same node now.

### 4(b) `gate_A/rework` — three causes on one row. The row's red line shows NOT the cause the report names. The row is not built per the card (B1).

The red line: `FAIL gate_A/rework — C2: the driver recorded no answer for this ask (...); C3: the answer changed nothing`.
`_check_c2` (`T/dry_exits.py:1382-1398`) returns at its FIRST failing clause. "No answer row" (`:1394-1395`) comes BEFORE the conductor-call clause
(`:1396-1397`). So the line shows cause (1) below, not cause (2) (edge 12):

1. **Product class of 4(a).** Under the default stub, the person's `rework` goes `seam_chosen` -> `no_move(why=chosen)` (`S/driver_machine.py:2450`).
   The default stub offers moves with no `args`, so `ArgsRefused` -> re-ask -> `fallback_person` raises a `Person` (`S/driver_conductor.py:661-664`).
   The `Person` leaves `take_answer` before `:3614`, so no answer row is written. C2's first clause comes from this cause.
2. **Edge 12, the chosen heading cut. A REAL product gap, by reading.**
   - `_conductor_text` = lead + moves + details file + gate prices + `## The person's choice` LAST (`S/driver_conductor.py:679-687`).
   - The whole text is the `refusal` (`_ask_conductor`, `:557-564`), and `refusal.strip()[:6000]` cuts it (`:320`).
   - The token the person chose is in the chosen note only (`chosen_note`, `:704-724`). The `## The person's words` section carries the ORIGINAL seed words.
   - So with a cut heading the conductor cannot know the person chose `rework`: FR-8 / FR-9 / AR-24.
   - The evidence is `chosen: false` on calls n3/n4. By the call order those are the `why=chosen` calls.
   - The report's argument "prompt_chars 25291 > 6000" is a non sequitur. `prompt_chars` measures the WHOLE prompt, which also holds `where` (2000) and up to 3 files x 8 KB
     (`CONDUCTOR_FILE_LIMIT`, `CONDUCTOR_FILES`, `:23-25`). It is not the length of the `## The refusal` section (F2).
3. **Stub artefact (R1-c).** C3 is red because the default stub cannot give `rework` its `args`, so no `seam_rework` is ever recorded.
   - Card §4 "Row data" says `gate_A/rework` carries `stub` per §9. §9 step 2 says to build the lone `rework_stage` option with `args`.
   - The row in `T/fixtures/stories/dry-1/exits/gates.json` has NO `stub` key. The report says "Rework control NOT attempted".
   - The F1 exception of §9 sorts a C2 red that comes from a counted chosen call. It does not license skipping the control. Here the C2 red does not come from that clause.

**The correct state.** Add the §9 control to `gate_A/rework` and `gate_B/rework` (B1). By reading, with that control:
- the chosen call answers with one `rework` option with `args`;
- `validate_options(chosen=True)` -> `chosen_rework` (`S/driver_conductor.py:673-676`) -> `record_seam_rework` returns `continue`;
- `take_answer` then reaches `record_answer_row` (`:3614`), so C2's answer-row clause holds;
- `seam_rework` is recorded, so C3 should see a change;
- the only red left should be C2 "a conductor call followed the answer and its why is not on record", from the chosen call that the cut heading leaves unmarked.

That is edge 12 isolated. This is expected by reading: one row run measures it.
- If the run shows that single red, the row stays `reach: story`, red, with the label below. "Stay story, red, known_red" is then the right state.
- If it shows otherwise, the builder reports it. No `live_only` (card §9).

- **Class.** "The conductor prompt's `## The refusal` section (`S/driver_conductor.py:320`) carries `_conductor_text` whole and cuts it at 6000".
  - **Surface:** conductor prompt composition. The neighbours on that surface, walked:
    - **magnitude:** besides the chosen note, `## The options at this gate` (`gate_prices`, `:684-685`) also comes after the details file and is cut the same way. The conductor then loses the priced options it is told to use (C1-4b). Same node.
    - **ordering:** the chosen note is LAST, so it is the first thing lost.
    - **encoding / empty:** n/a (an empty text gives no cut).
- **Owner.** A product node (edge 12; the card names it a product finding, §7 edge 12, §9).
- **Label** (key `gate_A/rework`, AFTER B1's run shows the isolated red):
  `{"node": "<node>", "raised_by": "product gap (critic t-1077, card r2 edge 12): the person's choice paragraph ## The person's choice is appended last to _conductor_text (driver_conductor.py:687) and the whole text is cut at 6000 characters as ## The refusal (:320), so the conductor's chosen call carries no token (stub journals chosen false) and is counted by C2; the gate's priced options (:684-685) are cut the same way"}`
- Do NOT write that label on today's row: its first failing clause is the 4(a) class, so the label would carry the wrong reason (AR-28).

---

## Findings

### B1 — BLOCKING. `gate_A/rework` / `gate_B/rework` lack the §9 rework control. The row's red is a mix of three causes.
- **Where:** `T/fixtures/stories/dry-1/exits/gates.json`, rows `gate_A/rework`, `gate_B/rework` (no `stub` key). Card §4 "Row data" first bullet, §9 step 2.
- **Failure:** the verdict line names "no answer row" + "changed nothing". The report attributes the red to edge 12. A known_red label written now would name a cause the row does not show (4(b)).
- **Correction:** add `stub.conductor` = `{"action": "ask_person", "question": ..., "why_person": ..., "checked": ..., "options": [move_option("rework_stage", "rework") + "args" from the chosen prompt's closed list]}`.
  The price lines are copied as data (§9 step 2, `T/dry_stub.py:74-99`). Run `gate_A/rework` ONCE alone. Report the line, the STUBROWS and whether `seam_rework` was recorded. Then the Lead labels per 4(b).

### F1 — FIX. Judge row (10) feeds the judge a fact shape that production never produces. The production branch of that edge has no row.
- **Where:** `T/dry_exits.py` selftest "K15 (10)" puts the `prompt: true` record INSIDE `priced_window`.
- **Why it matters:** `ask_window` drops every `prompt: true` record (`T/dry_world.py`, `ask_window` return line). So production reaches edge 3 only through `priced_seen` with `q == ordinal` (the second clause of `_k15_absent`). That clause has no row.
  The first clause, `any(r.get("prompt") is True ... for r in window)`, is dead in production. It is reachable only because the judge's own `_window` filters again.
- **Correction:** re-express row (10) as `priced_window: []`, `priced_seen: [{"key": "p.key", "q": 0, "prompt": true}]`, `ask_ordinal: 0` -> FAIL "only a conductor prompt priced". Then drop the window clause of `_k15_absent`, or keep it with a comment that it guards a hand-built fact.

### F2 — FIX. The edge-12 evidence should be the length of the section that gets cut, not of the whole prompt.
- **Where:** `T/dry_stub.py` conductor branch (journals `prompt_chars = len(prompt)`). The report §2 reads it as proof of the cut.
- **Correction:** journal, in the same line, the length of the text between `## The refusal` and the next `## ` heading of the driver's frame (`## \`story_step.py where\``). One more key, `refusal_chars`. Add a selftest row beside the `chosen` row.
  Then the cut is measured (refusal_chars == 6000 on the chosen call), not inferred (CLAUDE.md hygiene pt. 6).

### F3 — FIX. The `chosen` excuse in C2 does not depend on the token. It can hide a misrouted `record` / `nothing` token.
- **Where:** `T/dry_world.py` `row_facts` (`r.get("chosen") is not True`). The card §4 C2 states it generally.
- **Failure scenario:**
  - A product regression routes `approve` (price row `factory: record`, executor by code, `S/driver_machine.py:2390-2391`) through `seam_chosen` to the conductor.
  - The driver marks the call chosen, and the stub journals `chosen: true`. C2 does not count it.
  - The card's own per-variant table says `approve`: "no conductor call". That expectation is then never judged.
- **Correction (data-driven, one road):** excuse a `chosen` call only when the row's token has a price row whose `factory` is neither `record` nor `nothing`. This needs `judge_row`'s `prices` and the token, so move the excuse into `_check_c2`: `row_facts` carries the count of chosen calls separately.
  This amends a card sentence, so the Lead decides it. Proposed as a fix of this round, because the false-green road is in the code under review.

### F4 — FIX. `ask_reraised` fires on every gate SEAM ask. The "held" K15 text would misname a seam failure.
- **Where:** `T/dry_world.py` `run_exit_row`: `facts["ask_reraised"] = ... ask_row(questions[:ordinal], ask) is not None`.
- **Why:** the seam question has the same (kind, stage, dispatch) triple as the plain `gate_A` row before it (probe 1: ordinal 2, with an earlier gate_A row). So any K15 fail with an empty window at a seam would print "raised again without pricing (held)".
- **Correction:** decide "held" by the driver's own marker, `asked.held_lead` non-empty (`S/driver_dialog.py:629` sets it; `ask()` keeps it). The triple repeat is not that marker. Add one judge row: a seam ask with an earlier same-triple row, an empty window and no `held_lead` -> the plain "observed none" text.

### F5 — FIX. Walker defect 3 is used as a `live_only` reason, and no finding queues it.
- **Where:** `T/fixtures/driver-exits/gates.json`. Five routes (`marked_repair`, `form_vocabulary`, `handover_form`, `missing_output`, `handoff_form`) and `exit_gate:digest` are "measured" `live_only` with the why "the walker's post-answer turn is one driver boundary". The other five exit_gate joints follow that same road ("estimate").
- **Why it matters:** that is a limit of the walker (report t-1037 "Walker defects noticed" item 3), not a need for a live dispatch. My search found no finding for it: `grep -rli "post-answer|max-boundaries 1|one driver boundary"` over `plans/piles/*/findings` and the batch files -> 0 hits; positive control `dry-priced|walker` over the same findings folder -> 5 hits.
  Without a queued owner these rows have no way out when the walker gains a longer post-answer window (AR-25; P1-b live_only should mean live).
- **Correction:** a finding with an owner for walker defect 3 (and defect 2, joint ids not printed). Each such `why_unreached` names that finding. Alternatively, the Lead adds both to node R1's list.

### F6 — FIX (report). The witness of the t-1044 round is not a run of the final state, and t-1037's "needs a label" rows are superseded with no line saying so.
The t-1069 report supersedes them in fact: 4 of the 6 gate_A rows are green. The n4-gates report keeps "6 rows need a label" with no pointer to t-1069.
**Correction:** one line at its top: "superseded by `20261117-p1b-gate-ask-judge-report.md` (t-1069); rows red now: gate_A/stop, gate_A/rework". The Lead reads the node by its report (PROJECT.md p. 9: no residue).

### Notes (no change required this round)
- **N1.** G3 (c): the `not now` branch sets `ended_at` even when the fingerprint changed. G2 says the third clause sets it "only when the first two are false". Only the outcome detail is affected ("ended at none" printed on a moved state). The G1 `turns` rule still needs an unchanged fingerprint. Cosmetic.
- **N2.** G4 (ii) "other text": `put_ask` writes no text, so the case does not vary the text. `same_ask` does not compare text, so the case still proves what it must. Harmless.
- **N3.** `gate_A/free words` PASS rests on C6 alone plus K15 of the SEED (always true once the seed is reached). Nothing observes that the words reached the conductor (FR-8). This is the card's decided F-4 (a). The residual is visible in its PASS line (two n/a). The Lead may want C2's conductor-why observed there later.
- **N4.** All gate rows are judged at the CODE fallback seam question: every seed files one factory `defect_found` (R1-c). They are never judged at a conductor-built seam question. Stated in the card (§5). Queued as R1-c only once node R1 exists: node R1 (R1-a/b/c, F-8) is owed by the Lead at acceptance (card "Lead decisions F-7").
- **N5.** Identity residual, outside the card's adversarial list: a question priced and then never written as a row (the `human_text` raise of edge 8, `S/driver_dialog.py:403-409`) leaves a record with `q == n`. The next question that is written takes ordinal `n` and gets that record in its window. That is a false-green road when the next question is the same key re-raised without pricing. It is rare (the row is "never a reason not to ask"). It should be a line in R1.
- **N6.** `CHOSEN_HEADING` copies the driver's inline literal (`S/driver_conductor.py:687`). A rename turns into `chosen: false`, so C2 counts the call: a false RED, the allowed direction. Acceptable. The selftest guard of the `_conductor_text` name does not cover the heading text.
- **N7.** `_na_guards` refuses C2 n/a with a token at run time AND in the loader. That is defensive duplication, stated in its docstring. Acceptable.

---

## Acceptance keys

1. **Fit to the cards.** Done as written, file:line in the tree:
   - spy `q`/`prompt`: `T/dry_driver.py` `_raising_for_conductor`, `_question_count`, `passing_spy`;
   - one reader `ask_window` + `ask_row` + `_row_of`; `priced_at_ask` gone; `priced_window` / `ask_ordinal` / `priced_seen`: `T/dry_world.py:1153-1209`, `run_exit_row`;
   - `_holds` reads the window;
   - `say` loader (`_say_problems`) and run (`_say`), with all four failure texts;
   - K15 (i)/(ii)/(iii) and the n/a guard (`_judge_k15`); C2 offered source and C2 cut (`_check_c2`, `row_facts(first)`); C3/C2 n/a guards (`_na_guards`, `_walk_na_problems`);
   - G1 `ended_at` + armed `turns` (`_judge_always`), G2 position (the stop sits after asks/rehearse/loop/fp), G3 (a)(b)(c), G4 cases (i)(ii)+(iii) merged, (iv), judge row (11);
   - stub `chosen`/`prompt_chars`; selftest rows of §8 incl. the rename guard with its positive control; `na` NUMBER line; the 12 rows + FV1-8 row + 2 recipes.

   Done differently / not done:
   - `gate_A/rework` and `gate_B/rework` have no `stub` and §9 step 2 was not run (B1);
   - DoD (6) `stop` PASS not met: product gap, correctly reported unlabelled (DoD (8));
   - edges 3 and 10: texts present, but the production branch of edge 3 has no row (F1) and edge 10's trigger misfires at seams (F4);
   - edge 12: built; the evidence is inferred (F2).

   The other edges (1, 2, 4-9, 11, 13, 14) carry their texts and rows as the report table §6 says. Spot-checked by reading for 1, 2, 4, 6, 8, 13, 14.
2. **FR-58 / FR-12.**
   - Expected outcomes come from `references/question-prices.json` (the `factory` column, the answer rows), the person-facing packet text (`S/driver_gates.py:136-141`) and the design contract (`design/driver.md:206`, the answer row).
   - The executor citations in the per-variant table agree with the data column and do not set any value the data lacks.
   - Ask identity is the driver's own data: question row triple + spy ordinal + prompt stamp. Tokens compare by `_norm` (= `s0_normalize`). Approval words come through `gate_brief.approval_words`.
   - No phrase list. The stub's heading test is an exact line of the driver's own frame, not a person's wording (decided F-2).
   - One open point: F3 (the `chosen` excuse lets an implementation road go unjudged).
3. **Green that the product would make red.** One code road: F3. The PASS rows are honest under the card's decisions:
   - `approve` (answer row, state moved, no conductor call);
   - `retry` (C3 n/a guarded by `factory: nothing`; ended at the plain gate; the `turns` rule satisfied by the guarded n/a);
   - `free words` (thin, N3);
   - `empty`.

   No row stands in for a role's judgment (AR-7, AR-29): every check is data vs the driver's record.
4. **The two red rows.** See the section above.
   - `stop`: product, class "a Person raised out of take_answer leaves no answer row", shared with FV3-16; one product node; label text given.
   - `rework`: today a mix of three causes. B1 first. Then edge 12 isolated, product node, label text given.
5. **Class-wide completeness.**
   - SIBLING_MAP axes the cards name:
     - **axis 34 (one road):** the same judge, the C2 cut and the turn end reach every group automatically (one helper, one loop). The s5 and s6-s9 gate key rows take `say` in their own nodes (card non-goals). Not written yet, so nothing there passes for the wrong reason today.
     - **axis 38 (dry ratchets):** see key 6.
   - **Merged groups:**
     - `exits:s1-s4`: identical before/after (witness §4).
     - `exits:s0`: one detail line gained `ended at halt at S1 after turn 1`, on a row already labelled FV3-16. That fits G5 (a flip with the `ended at` detail is reported, not fixed). The row stays NOTE.
   - **Nothing in the sibling groups now passes for the wrong reason.** By reading, the new rule makes K15 on non-gate key rows stricter (the window of THIS ask, no prompt records). The `turns` always-check stays armed for rows that do not judge C3 (G1).
   - **Classes found here that live outside the diff:**
     - the answer-row class of 4(a) (product, siblings listed);
     - the 6000-char section of 4(b) (product, gate prices are its neighbour);
     - walker defects 2-3 (F5).
6. **Census and ledgers.**
   - `dry_exits.py --check` re-run: `0 discrepancies` and `NUMBER na: 10 declarations (C2 3, C3 6, K15 1)`. I recounted from the fixture: retry A/B C3 2, stop A/B C3 2, free words A/B C2+C3 4, FV1-8 K15+C2 2 = 10 (C2 3, C3 6, K15 1). It matches.
   - Ratchet raises by name:
     - `T/fixtures/driver-exits/gates.json` `unwalked` 21 -> 0 (shrink);
     - `live_only` stays base 0, with 37 gates raises each named in `raised_by` (15 routes + 6 exit_gate joints census + 15 walk route rows + 1 FV1-8 walk row), reason "N4:gates t-1037";
     - no `known_red` row added and no `pins` raised.
   - Without labels the canon is red in the right place. The part prints `FAIL known_red — new red: gate_A/rework` / `gate_A/stop`, naming `known_red/gates.json` (witness §5).
   - With the two labels (a new `known_red/gates.json` with `pins.known_red: 2`), the part would be green: the remaining rows are PASS / NOTE `after:FV3-20` / NOTE live_only, and `outcomes` PASS.
   - The `rework` label belongs only after B1 (4(b)).
7. **Duplication and code quality.**
   - **DUPLICATION AND CONSISTENCY:** no second reader. Question rows go through `driver_journal.question_rows` in the spy; prices through the judge's `prices`; approval words through `gate_brief.approval_words`; the gate stage through `driver_gates.GATE_STAGE_OF`; tokens through `_norm`.
     I compared `ask_row`'s raw triple with `dry_exits.same_ask`'s identity. They are different on purpose (ordinal lookup vs the C5 identity). No merge owed.
     Defensive duplicates: `_window` re-filters what `ask_window` filtered (F1: it creates a dead clause), and the C2 n/a check runs in the loader and at run time (N7).
   - **CODE QUALITY:** one dead branch in production (`_k15_absent` window clause, F1). `_say` formats the "pending is X at Y" text twice (minor). `callers()` in the dry_stub selftest says "list" in its docstring but returns a tuple (trivial).
     The functions added stay under ~60 lines. `run_exit_row` keeps growing; it is a scenario runner with a fixed order, readable with its G2 comment.
   - **ONE ROAD (question 12):** no exclusion of a language, project or case. The turn end and the C2 cut are general. The n/a declarations are data with run-time guards.
     F3 proposes making the `chosen` excuse data-driven by the price column, so it stays one road.
   - **TESTS (question 5):**
     - (a) killing power: the judge rows catch the identity defect that t-1037 exposed (an earlier ask's record, prompt records). The G4 cases catch an early stop by `gates == 2` and `post_turns == 1`.
     - (b) expected values trace to the card and the G-edits. Exception: row (10)'s fact shape (F1).
     - (c) new behaviour at doors has rows: the `say` grammar, the NUMBER line, the stub journal keys, PASS-line detail through `judge_group`.
     - (e) no duplicate rows found: I compared the new K15 rows with the existing "K15/E17" rows; they differ in input.
     - (f) the commit carries `tests-over:` with the reason "the card asks for ... rows". It holds: card §8 enumerates them.
     - (g) no new test file.

---

## Trail

Read:
- the card r2 whole (1-551) and the walker spec (lines 153-195, 231, 380-395, 440-480);
- both builder reports whole;
- the diff `2e9cb3a9...HEAD` whole (`dry_driver.py`, `dry_world.py`, `dry_stub.py`, `dry_exits.py`, the three fixtures);
- `T/dry_exits.py:1382-1398` (`_check_c2`) and `:1537`;
- product code in the tree:
  - `S/driver_conductor.py:23-29`, `:200-260`, `:300-350`, `:557-564`, `:640-800`, `:852-880`;
  - `S/driver_machine.py:1862-1880`, `:2025-2060`, `:2375-2455`, `:2480-2495`, `:3375-3420`, `:3590-3620`;
  - `S/driver_runner.py:280-300`; `S/driver_dialog.py:378-400`, `:590-630`; `S/driver_s0.py:395-412`; `S/driver_gates.py:46`, `:1096-1120`;
  - `references/gate-approval-words.json`, `references/question-prices.json:140-156`, `design/driver.md:200-215`;
- `T/fixtures/driver-exits/known_red/s0.json`; the census diff of `T/fixtures/driver-exits/gates.json`;
- `plans/piles/live-run-fvf/batch-3-live-run-fvf.md` (FV3-16 row);
- `docs/tasks/critic-diff-brief.md` questions 1-12; `tools/critic_verdict.schema.json`; `tools/critic_verdict_check.py` (rules).

Searches:
- `record_answer_row|settle_unread_answer|def held_question|class Person` over `S/` (writers and handlers of the answer row; positive: `record_answer_row` found at 9 sites);
- `answer_rows(|driver-answers.jsonl` over `S/`, `references/`, `design/` (readers; `design/driver.md:206` found);
- findings for walker defect 3 (0 hits, positive control 5 hits, F5).

Re-runs (cheap, from `<tree>/ai-packages/qa-factory`, via a subshell):
- `python -B scripts/tests/dry_exits.py --selftest` -> `dry_exits selftest: 193/193 cases`;
- `python -B scripts/tests/dry_exits.py --check` -> `NUMBER na: 10 declarations (C2 3, C3 6, K15 1)` ... `dry_exits --check: 0 discrepancies`;
- `python -B scripts/tests/dry_stub.py --selftest` -> `=== dry_stub --selftest: 225/225 ok ===`.

The witness of the gates part (11 min) was NOT re-run (dispatch). I checked it for consistency instead: the FAIL texts agree with the order of `_check_c2`, the n/a lines with the fixture, and the `after:FV3-20` NOTEs with the merge.

The decision to accept, the labels and opening the product nodes belong to the Lead (rule 6). This verdict is an input.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1: gate_A/rework and gate_B/rework carry no stub control per card section 4 Row data and section 9 step 2 (fixtures/stories/dry-1/exits/gates.json); the row's red is three stacked causes (answer-row product class, cut chosen heading, stub without args) and its verdict line shows the first, not edge 12; add the lone rework_stage option with args, run the row once, then label"
  ],
  "fixes": [
    "B1: add the section 9 rework control to gate_A/rework and gate_B/rework; one run of gate_A/rework alone; report line, STUBROWS and whether seam_rework was recorded",
    "F1: judge row K15 (10) must present the prompt record in priced_seen with an empty priced_window (the shape ask_window produces); drop or comment the dead window clause of _k15_absent",
    "F2: dry_stub journals refusal_chars (length of the ## The refusal section) beside prompt_chars, with a selftest row, so the edge-12 cut is measured",
    "F3: the chosen excuse of C2 applies only when the row token's price row factory is neither record nor nothing (move the excuse into _check_c2; row_facts counts chosen calls apart); Lead decides the card amendment",
    "F4: ask_reraised decided by asked.held_lead, not by a repeated (kind, stage, dispatch) triple, which fires on every gate seam ask; one judge row",
    "F5: a queued finding with an owner for walker defects 2 and 3 (one-boundary post-answer window, joint ids not printed); the live_only whys of the 5 routes and 6 exit_gate joints name it",
    "F6: the t-1037/t-1044 report gets a superseded-by line pointing to the t-1069 report and the two rows still red"
  ],
  "class_completeness": "Axis 34: judge, C2 cut and turn end are one helper and one loop for every group; s5 and s6-s9 gate key rows are their own nodes (card non-goals), nothing there passes wrongly today. Axis 38: unwalked 21->0, live_only +37 named in raised_by, no known_red raise; --check 0 discrepancies. Merged groups s0 and s1-s4 unchanged except one G5 detail on a row already labelled FV3-16. Outside the diff: product class 'a Person raised out of take_answer leaves no driver-answers.jsonl row' (stop_here, seam_chosen and record_seam_rework held roads, chosen and unread no_move ending in a Person; same cause as FV3-16) -> one product node for the Lead; product class 'conductor prompt ## The refusal cut at 6000 carries _conductor_text whole' (chosen note and gate prices) -> one product node; walker defects 2-3 unqueued (F5); node R1 (R1-a/b/c, F-8) owed by the Lead, plus N5 identity residual as an R1 line.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-p1b-gate-ask-judge-card-r2.md (whole)",
      "docs/tasks/specs/20261114-p1b-n4w-exit-walker-spec.md (153-195, 231, 380-395, 440-480)",
      "<tree>/docs/tasks/specs/reports/20261117-p1b-gate-ask-judge-report.md (whole)",
      "<tree>/docs/tasks/specs/reports/20261117-p1b-n4-gates-report.md (whole)",
      "git diff 2e9cb3a9...HEAD (all 9 files)",
      "S/driver_conductor.py 23-29, 200-260, 300-350, 557-564, 640-800, 852-880",
      "S/driver_machine.py 1862-1880, 2025-2060, 2375-2455, 2480-2495, 3375-3420, 3590-3620",
      "S/driver_dialog.py 378-400, 590-630; S/driver_s0.py 395-412; S/driver_runner.py 280-300; S/driver_gates.py 46, 1096-1120",
      "references/gate-approval-words.json; references/question-prices.json 140-156; design/driver.md 200-215",
      "T/fixtures/driver-exits/known_red/s0.json; T/fixtures/driver-exits/gates.json (diff)",
      "plans/piles/live-run-fvf/batch-3-live-run-fvf.md (FV3-16)",
      "docs/tasks/critic-diff-brief.md questions 1-12"
    ],
    "reruns": [
      {"command": "( cd <tree>/ai-packages/qa-factory && python -B scripts/tests/dry_exits.py --selftest )", "result": "dry_exits selftest: 193/193 cases"},
      {"command": "( cd <tree>/ai-packages/qa-factory && python -B scripts/tests/dry_exits.py --check )", "result": "NUMBER na: 10 declarations (C2 3, C3 6, K15 1); dry_exits --check: 0 discrepancies"},
      {"command": "( cd <tree>/ai-packages/qa-factory && python -B scripts/tests/dry_stub.py --selftest )", "result": "=== dry_stub --selftest: 225/225 ok ==="}
    ]
  }
}
```
