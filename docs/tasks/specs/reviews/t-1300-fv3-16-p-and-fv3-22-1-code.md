# t-1300: code review of FV3-16 card P (t-1253) and FV3-22-1 (t-1262)

Critic, diff gate. Both branches were diffed with `git -C <worktree> diff origin/main...HEAD` after `git fetch` on 18.11.2026.
The verdicts below are inputs to acceptance. The decision to accept belongs to the Lead of live-run-fvf/3 (rule 6).

---

## (A) FV3-16 card P: branch `worktree-agent-a8b00daf4eb8fbe6d`, head 50d35a53

**Verdict: NEEDS WORK, reject for this round, `failure_class: spec`.** There are no blockers and four fix-before-merge findings. On the class: the card's P4 site list was built from the call shape `raise self.held_question(self.stop_held(`. It misses two token roads that are inside P4's own invariant. The builder followed the list (F-A1, F-A2).

### Findings

**F-A1 (fix-before-merge, Q4 class): two P4 siblings on the seam token road still lose the answer row.**
- P4's invariant: "a token read inside `take_answer` and then a `Person` raised before :3614 gets `record_answer_row(token)`".
- Trace:
  1. `take_seam_answer` reads a token. `move = by_token[token]`, then `self.answer_file()` (driver_machine.py:2389-2390).
  2. Every move other than approve / person_does / stop_here goes to `seam_chosen`.
  3. `seam_chosen` raises `held_question("Your choice could not be carried out ...")` when the words are not on file (driver_machine.py:2413), or calls `no_move({"why": "chosen", ...})` (:2449).
  4. `no_move` raises `options_person` when the conductor answers `ask_person` (driver_conductor.py:696; this is also the dry stub's default verdict). It can also raise `held_question` at driver_conductor.py:765 and :770.
  5. Each of these is a Person that skips the row at the end of `take_answer` (:3629). The `except Person` funnel at :2031 only calls `ask()`.
- Example: answer `go on` (move `go_on_as_is`) to a seam question, and the conductor asks back. Result: 0 rows in `driver-answers.jsonl`. This is the same defect as the removed `gate_A/stop` row, reached through another move.
- Fix: one line `self.record_answer_row(token)` right after `self.answer_file()` at driver_machine.py:2390. It covers every move, and the stop_here line at :2398 becomes redundant.

**F-A2 (fix-before-merge, Q1/Q4): the `ticket_changed` row for a token answer says it was not a token.**
- `ticket_ask_again` now writes `record_answer_row("")` (driver_s0.py:406-408).
- `take_ticket_answer` also reaches it for the token `stop` (:452: `TICKET_CHANGED_TOKENS = ("new text", "old text", "stop")`, :27) and for `old text` / `new text` when the adapter fails (:467).
- The row's contract is "the token this answer was ('' when it was not one)" (driver_conductor.py:249). The answer `stop` therefore gets a row whose token is `""`. It is the P4 class (a token read, then a Person raised), reached through `ticket_ask_again` rather than `stop_held`.
- Fix: give `ticket_ask_again` a `token` parameter. Pass `""` from the unread caller (:450) and the read token from :452 and :467.

**F-A3 (fix-before-merge, Q5c): the halt `stop` branch has no test row.**
- P4 names it as a verified hole (driver_machine.py:3593-3598, now `record_answer_row("stop")`).
- Neither the new table nor the dry walk drives it: `exits/s0.json` has only `kind:halt/empty` and `kind:halt/free words`.
- Fix: add one case to `fv316_unread_answer_row`: a halt answered `stop` gives a held Person and one row with token `stop`. The F-A1 line is reached through table row 3 once a verdict that asks back is given for the `go on` turn; a turn of row 3 with `ask_person` instead of `continue` covers it with no new rig.

**F-A4 (fix-before-merge, Q6/Q7 copy-paste + Q5f budget):**
- (a) The pair `self.answer_file(); self.record_answer_row(token)` is pasted at 7 sites: driver_dispatch.py:1883-1884, :3457-3458, :4066-4067; driver_machine.py:2248-2249, :3596-3597; driver_s0.py:424-425; driver_stage_s7.py:507-508. ticket_ask_again (:407-408) is an eighth. The order matters: without the first call the row's `words_file` is `""`. One helper beside `settle_unread_answer` (driver_conductor.py:252), for example `record_answer(token)` = file + row, removes the copies and that hazard.
- (b) Test lines exceed product lines: 60 test insertions against 39 product insertions (numstat in the trail). Rows to cut or fold, weakest first:
  - the `if label[0] == "1"` special check (test :492-493): fold it into the case tuple as an expected `(token, kind)`;
  - the two separate rigs for rows 5 and 6 (:495-517): fold them into the table as cases with a setup hook.
- Alternatively the Lead gives a tests-over reason at merge. That reason is the Lead's to give.
- Also note test :519 `S4_CRITIC, S4_DESIGNER ="S4-..."`, a whitespace change to an untouched line.

**N-A5 (note; the builder's open question): `not built yet` on an asked-back halt question.**
- Judgment: the carve-out (driver_machine.py:3561) is in the safe direction compared with plain P3. With plain P3, `not built yet` would reach `_unread_halt_or_review` and be filed as the scout's words. The side would stay at the default `product: real`, which is the silent default PC-7 B3 (:3585-3590) exists to prevent. The carve-out keeps the old road instead (generic branch → `take_seam_answer` → `unread` → conductor). Nothing is silently defaulted, and D-0041 holds.
- The pre-existing hole stays: on that road the side is never recorded and the words are not filed for the scout. The first-answer branch (:3585) is unreachable once the question carries `offered`, so the same answer takes two roads depending on whether the question was asked back (Q12-shaped).
- Whether code may read `not built yet` on a question the conductor re-raised is a fork for the Lead (FR-12: tokens of the question shown). It is not a builder fix.
- Proposed residual for «Остатки»: `not built yet answered to the asked-back s1.no_diff halt question reaches no executor (side not recorded, words not filed) | узел: <to be opened by the Lead of live-run-fvf/3>`.

### Standing questions (A)
- **Q1 fit:**
  - P1 is as written: driver_conductor.py:887-890, writing before `no_move`. The raw writer in ticket_ask_again is removed.
  - P2 is as written: driver_machine.py:3858-3863. Filing plus `save_state` happen before `register_words_to_conductor`, and the old clause is gone.
  - P3: a new elif before the generic branch, with the `not built yet` carve-out (N-A5). POSITION INVARIANT kept: `halt_free_words` is False for every key of `seam_tokens(asked)` (:3410-3411).
  - P4: the listed sites are done; siblings are missing (F-A1, F-A2).
  - The I6 safety claim holds: driver_machine.py:1465-1474 raises the held question before `resume_role` when `asked.dispatch == dispatch` and words are filed.
- **Q2 builder decisions:** the P3 elif placement is safe. It leaves test_walk_account/test_walk_supply's located line untouched, and every token still reaches `take_seam_answer`. On the carve-out see N-A5.
- **Q3 seams:** all additive. The known_red edit removes exactly the stale `gate_A/stop` row, pin 1 → 0. That row's `raised_by` names driver_machine.py:2395-2397, the stop_here site fixed here, so it is consistent.
- **Q4 class:** F-A1 and F-A2. The axis is SIBLING_MAP "One question for every stop". Neighbours walked:
  - a Refusal (already settled, :2040-2045);
  - the gate old-answer replay (driver_gates.py:874: `_answer` without `kind`, so `record_answer_row` is a no-op by design);
  - an end row with a reassigned `dispatch` (the s1_exit_gate branch calls no `unread`, so no clash).
  The class-wide closure is for the Lead: a Person funnel at :2031 that settles the held answer, as the Refusal funnel does.
- **Q5:**
  - (a) Rows 1, 3 and 4 kill P2 and P3: with filing after the seam, pending is None at turn 1. Row 6 kills a double writer; row 5 kills stop_here.
  - (b) The expected values come from the card's table (t-1244 :82-88).
  - (c) See F-A3.
  - (d) No test was rewritten.
  - (e) No duplicate: N7/N7a assert the words file.
  - (f) See F-A4b.
  - (g) No new file.
- **Q6:** F-A4a. Otherwise P1 reuses `record_answer_row`, with no second writer. The grep `_append_jsonl(.*driver-answers` now finds only driver_conductor.py:243.
- **Q7:** F-A4a. No new function goes over 60 lines.
- **Q8:** the diff's added lines carry no non-ASCII and no CR.
- **Q9:** `known_red/gates.json` 1 → 0 (a shrink). No raises.
- **Q10:** AR-14, AR-15, AR-22 and AR-24 are named in the report. The producer–reader walk: `driver-answers.jsonl` is read by `already_answered` (driver_dialog.py:385) and by dry C2. No reader is starved. VARIETY: language-independent; nothing blocks on an unknown value.
- **Q11:** judgment none: a write order and a writer.
- **Q12:** N-A5 only. Grepped: `halt_free_words`, `not built yet` in driver_*.py.

---

## (B) FV3-22-1: branch `worktree-agent-ab84923a7b5ea3f1f`, head 1f48a2db

**Verdict: NEEDS WORK, close to accept (`failure_class: capability`).** There are no blockers and one fix-before-merge finding. The move is otherwise faithful: every moved body was compared against its old text with `self` → `road`. The canon reds are environmental (see the timing answer below).

### Findings

**F-B1 (fix-before-merge, the card's own AR-15 DoD, Q4): an unnamed duplicate of the live-S6 predicate in an owned file.**
- The card (§1.3, AR-15 row) requires every hit of the grep `"running", "blocked", "paused"` to be a caller of the survivor or a named site (FV3-24 / R2-F3).
- driver_stage_s6.py:1581 (`s6_settling_lanes`) inlines `controller.live_s6_scopes` (controller.py:690-697). That predicate's docstring names `s6_settling_lanes` as its own user, so the copy makes that docstring false.
- The report lists the site under "analogs noticed (not fixed)" and calls it outside the move. The card's DoD gives no such exit, and the file is in `owns`.
- Fix: `if live_s6_scopes(ctl): return self.S6_SETTLE_RUNNING`, inside the same try. The import is already at driver_stage_s6.py:10. Behaviour is identical, because a scope-less live row is still a list element. The alternative is a node line from the Lead.

**N-B2 (note): `consumer_person_pass`'s delegate now wraps the whole pass in `try`/`except Refusal` (driver_stage_s6.py:219-224).**
- The old code wrapped only `person_pass`. The wider scope would override a Refusal from `owe_row` and skip the P13 finding on retry. `owe_row` never raises Refusal (driver_runner.py:263-281: it marks the row owed), so there is no behaviour change today.
- Consider narrowing it when FV3-22-2 touches the delegate.

**N-B3 (note):** `s6_automation_settled` adds `not auto_scope or ...`. Both uses are guarded by `auto_scope` (driver_stage_s6.py:429, :434), so behaviour is unchanged, as the inline comment claims.

### Timing pin, test_stage_guard CX1-20 33: environmental, not a cost the branch added
- (1) The timed function `stage_guard.rule_typed_runner` and its import closure (`hooklib`, `adapter_forms`, `detector_verdict`, `runtime_paths`, `person_words`; stage_guard.py:78-84) are not in the branch's diff (11 files, none of them). The timed code is byte-identical to origin/main.
- (2) A local run of `test_stage_guard.py` on the branch, on a loaded machine: `PASS CX1-20 33: ... and 10x the input costs under 25x the time`, `=== test_stage_guard: 1683/1683 ok ===`.
- (3) The pin is a wall-clock ratio of two single samples at a superlinear threshold. The canon's 24.99 s / 0.99 s is 25.2, just over 25, which is what a loaded runner produces.
- test_probe_by_code and test_stage_joints at 300 s are node PC4-19 (package-ci/batch-4 :40). The same two files timed out on branch N2h-v, where the change did not lie on their path.
- Proposed residual for the Lead: `test_stage_guard.py CX1-20 33: a single-sample wall-clock ratio fails under CI load (canon 44193633984, 24.99 s / 0.99 s) | узел: <to be opened by the Lead, package-ci>`.

### Siblings asked by the dispatch: close paths left only in Driver methods after the extraction
1. `Driver.close_receipt` (driver_dispatch.py:2549) and `Driver.record_close` (:2559): Driver-only. The card keeps them (K5.d). They are road members the skill road must supply in FV3-22-2.
2. `Driver.manual_close` head (driver_stage_s6.py:943-~957): the held-case `refuse_case` loop stays in the Driver. Only the tail moved (K5.b).
3. The S6 code closes with their own `finalize_task` and refusal: `s6.accepted` (:414), `s6.nothing` (:421-424), `s6.results_stand` (:458-463), `s6_reprobed_close` (:706-713), `s6_reentry` (:731). Named in the card as FV3-24.
4. `s7_await_scribe` (driver_stage_s7.py:174-206): S7's own `atomic_json` twin of `mark_awaiting`. Named as FV3-26 (R2-F3).
5. `code_close_step` (driver_machine.py:2302), the deferred close record: Driver-only and out of the card.
6. `consumer_need_record` itself is now a delegate (driver_stage_s6.py:232). Its callers `s6_reprobed_close` :702, `s6_reentry` :731 and `s7_close` (driver_stage_s7.py:527) stay in the Driver.

### Standing questions (B)
- **Q1:** K5.a, K5.b, K5.c, K5.d, K5.l and K5.m are as written.
  - `live_s6_scopes` stays in controller.py by the Lead's F5 (card :862-863).
  - The refusal text is unchanged up to its door. The door is now `person_word_door` (stage_close.py:182-185).
  - `Refused` → `Refusal(str, title=)` is valid: `Refusal.__init__` takes `title` (driver_core.py:113-114).
  - The title `code_only_evidence` is kept (stage_close.py:254, driver_dispatch.py:2543-2545).
  - `request["id"]` equals the old receipt.
- **Q2:** the builder decided only the F5 consequence: no edit to story_step. That is consistent with the card.
- **Q3:** test-layers.json: `covers` additions as K5.m instructs (card :367). driver-layers.json: the BY_PERSON row is deleted and the `consumer_await` note extended.
- **Q4:** F-B1. Siblings are named above.
- **Q5:**
  - (a) The K5.m row kills the old door, which had no `--words-file`.
  - (b) The expected value comes from FR-2 and E-M2.
  - (c) The door text is the only new behaviour, and it has its row.
  - (d), (e): none.
  - (f) 7 test lines against 37 net product lines.
  - (g) No new test file.
- **Q6:** the inline sha in `code_only_request` (stage_close.py:249) duplicates `driver_core._sha` (driver_core.py:303). The card directs it (E-M5, card :252/:496), so it is not a finding. `BY_PERSON`: one definition (grep `BY_PERSON` over the package; the only other reader is driver_stage_s6.py:194).
- **Q7:** no function over 60 lines in stage_close.py. The largest is `need_record`, about 25 lines of body. No dead branches.
- **Q8:** pyflakes is clean on the five changed modules. One non-ASCII character, `§`, is in a moved docstring (not Cyrillic). No CR.
- **Q9:** driver-layers.json loses the BY_PERSON row (a shrink). No raises.
- **Q10:** AR-13, AR-14, AR-15 and AR-19 are named in the card and report. The one-way rule holds apart from F-B1. VARIETY: language-independent.
- **Q11:** no census or check change. Judgment none.
- **Q12:** none. The node IS the convergence onto one road. Grepped: `finalize_task.py"`, `close_by_code(`, `acceptance_awaits`, `"running", "blocked", "paused"` over driver_*.py.

---

## Spot-checks
- A's witness `212/212`: reproduced (trail).
- B's claim of "no other BY_PERSON reader": an own grep found only stage_close.py:21 and driver_stage_s6.py:194. Positive control: the same grep finds `PASSED_BY_PERSON` in test_probe_gap_word.py.
- B's claim "auto_done uses guarded": checked with `grep auto_done` (:408, :429, :434, :499 comment).
- A's claim "no siblings beyond P4's list": NOT reproduced (F-A1, F-A2).

## Trail
- Read:
  - finding 20261117-p1b-s0-halt...md;
  - the t-1244 diagnosis (:20-139, card P/W);
  - FV3-16 report;
  - FV3-22 card r2 (§0.1, §1.3, §2.1 rows, :862);
  - t-1262 report;
  - batch-3 rows FV3-16/22;
  - both full package diffs;
  - driver_conductor.py:205-262, :617-696;
  - driver_machine.py:2346-2450, :3380-3400, :3520-3630, :3842-3866, :1460-1480, :2008-2050;
  - driver_s0.py:395-470;
  - driver_runner.py:263-281;
  - stage_close.py whole;
  - test_stage_guard.py:274-286;
  - dry_exits.py:1392-1411;
  - controller.py:688-697;
  - driver_stage_s6.py:1570-1586.
- Reruns:
  - `( cd <A wt>/ai-packages/qa-factory/scripts/tests && python -B test_no_move_seam_n2b_n15.py )` → `=== no_move seam_n2b_n15: 212/212 ok ===`, exit 0, 0 FAIL lines.
  - `( cd <B wt>/.../tests && python -B test_stage_guard.py )` → `PASS CX1-20 33: ... and 10x the input costs under 25x the time`; `=== test_stage_guard: 1683/1683 ok ===`.
  - `python -B -m pyflakes` on B's 5 modules → clean. On A's 3 modules → only a pre-existing unused `hooklib` in driver_machine.py:3 (not in the diff).
  - numstat A: 39 product insertions against 60 test insertions. numstat B: 362 insertions / 216 deletions, test +7.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "A (FV3-16 P): axis One question for every stop. P4's site list came from the call shape raise held_question(stop_held(...)) and misses two token roads inside P4's own invariant: take_seam_answer -> seam_chosen -> no_move(why=chosen) -> options_person / held_question (driver_machine.py:2413, :2449; driver_conductor.py:696, :765, :770), and ticket_ask_again recording token '' for the token stop / old text / new text (driver_s0.py:406-408, callers :452, :467). Class-wide closure proposal for the Lead: a Person funnel at driver_machine.py:2031 like the Refusal one. B (FV3-22-1): the AR-15 grep hit driver_stage_s6.py:1581 inlines controller.live_s6_scopes in an owned file, neither a caller nor a named site; the other close paths left in the Driver are named (close_receipt, record_close, manual_close head, the S6 code closes = FV3-24, s7_await_scribe = FV3-26, code_close_step).",
  "fixes": [
    "A F-A1 fix-before-merge: driver_machine.py:2390 add self.record_answer_row(token) right after answer_file() in take_seam_answer (covers seam_chosen's Person roads; :2398 becomes redundant)",
    "A F-A2 fix-before-merge: driver_s0.py:399-408 ticket_ask_again takes the token; pass '' from :450 and the read token from :452 and :467",
    "A F-A3 fix-before-merge: test_no_move_seam_n2b_n15.py fv316_unread_answer_row: add a case for halt answered stop (one row, token stop) and an ask_person turn after a chosen token",
    "A F-A4 fix-before-merge: one helper (answer file + row) for the 8 pasted pairs (driver_dispatch.py:1883, 3457, 4066; driver_machine.py:2248, 3596; driver_s0.py:407, 424; driver_stage_s7.py:507); fold the label-1 check and the rows 5/6 rigs into the table, or the Lead gives a tests-over reason",
    "B F-B1 fix-before-merge: driver_stage_s6.py:1581 call controller.live_s6_scopes(ctl) inside the same try instead of the inline predicate, or the Lead opens a node"
  ],
  "trail": {
    "read": [
      "plans/piles/live-run-fvf/findings/20261117-p1b-s0-halt-svobodnye-slova-ne-dohodyat.md",
      "docs/tasks/specs/reviews/t-1244-fv3-16-free-words-diagnosis.md",
      ".claude/worktrees/agent-a8b00daf4eb8fbe6d/docs/tasks/specs/reports/20261117-fv3-16-p-report.md",
      "docs/tasks/specs/20261117-fv3-21c-skill-road-s6-close-card-r2.md",
      ".claude/worktrees/agent-ab84923a7b5ea3f1f/docs/tasks/specs/reports/t-1262-fv3-22-1-report.md",
      "A: driver_conductor.py, driver_machine.py, driver_s0.py, driver_dispatch.py, driver_stage_s7.py diffs and the ranges in the Trail",
      "B: stage_close.py, driver_stage_s6.py, driver_stage_s7.py, driver_dispatch.py, driver_core.py diffs, controller.py:688-697, test_stage_guard.py:274-286"
    ],
    "reruns": [
      {"command": "python -B test_no_move_seam_n2b_n15.py (A worktree, tests dir)", "result": "=== no_move seam_n2b_n15: 212/212 ok === exit 0"},
      {"command": "python -B test_stage_guard.py (B worktree, tests dir)", "result": "PASS CX1-20 33 ratio check; === test_stage_guard: 1683/1683 ok ==="}
    ]
  }
}
```
