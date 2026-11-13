# Critic on plan: FV1-3 (then FV1-9), free answer to a question pack goes to the conductor

Spec under review: `docs/tasks/specs/20261113-fv1-3-free-answer-to-conductor-spec.md` (DRAFT, designer, 13.11.2026).
Tree used for facts: `.claude/worktrees/read-main` = origin/main at `e4ba384` ("wave 1 integration report"); the root
checkout was used only for the gitignored run logs of §2.1, which exist nowhere else.

**VERDICT: fit_with_fixes. 4 blocking findings (B1-B4), 15 more fixes (F1-F15).** The direction is right. FV1-3 moves
the threshold stop onto the halt road's existing hand-over, and that is the P31 / AR-19 move. But the spec as written
would leave a keep detector red, open a road where the role resumes before the conductor's question is answered,
and send the builder to line numbers that are stale by about 40 lines. Every amendment is a spec edit the Lead can
make. B2 and F7 carry a small design choice each (forks F-10 and F-11 below), and the Lead can decide them. FV1-9 is
not dispatchable as written, by its own text (forks F-7 and F-8 are open, and it needs a scout pass). It needs the
designer again after the owner's word on F-7 and F-8.

This verdict is an input to the Lead's acceptance. It is not the acceptance.

---

## 1. Facts by trail (§2 on e4ba384)

The conductor-side and register-side facts hold. Every `driver_dispatch.py`, `driver_machine.py` and test-registry
line number is stale, because the designer read the root checkout at f52faed (spec §9 says so itself).

| Spec says | On e4ba384 | Status |
|---|---|---|
| `driver_dispatch.py:1708-1751` take_question_answer; docstring `:1711`; go on/stop `:1724-1742`; record `:1743`; apply `:1744`; answered/resume/pending `:1747-1750`; answer_row `:1751` | `:1746-1789`; `:1749`; `:1762-1780`; `:1781`; `:1782`; `:1785-1788`; `:1789` | stale (+38) |
| `question_resume_prompt :1678-1687` | `:1716-1725` | stale |
| `record_question_words :1759-1792`, print `:1787` | `:1797-1830`, `:1825` | stale |
| `record_halt_words :1794-1810`, invariant `:1798-1800` | `:1832-1848`, `:1837-1838` | stale |
| `question_threshold :1552-1636`, apply `:1576` | `:1590-1674`, `:1614` | stale |
| `driver_machine.py` take_answer `3314-3590`; empty `:3319-3320`; qtext `:3329`; offered `:3493`; questions branch `:3507-3510` (call `:3510`); halt branches `:3511-3524` | `3361-3637`; `:3366-3367`; `:3376`; `:3540`; `:3554-3557` (call `:3557`); `:3558-3571` | stale (+47) |
| `_unread_halt_or_review :3767-3803`; all-token return `:3778-3780`; unread body `:3781-3802` | `:3814-3850`; `:3825-3827`; `:3828-3849` | stale |
| `_run_guarded :1811` | take_answer call at `:1858` (def `:1852`) | stale |
| seam `go on` with no block `:2356`, `:2381-2388` | take_seam_answer `:2335`; seam_chosen `:2388`; the no-block `go_on` falls to `no_move(why=chosen)` at `:2429-2435` | stale |
| s1_gap fall-through `:3480-3481` | `:3527-3528` | stale |
| `driver-layers.json:193,198,199,824` | `:201,206,207,832` | stale |
| `test-layers.json:5820 / 4109 / 5950 / 6036 / 9184` | `:5879 / 4167 / 6009 / 6095 / 9243` (9243 sits inside `quarantine`, opened at `:7126`) | stale |
| `audit_factory.py:1680` | `:1681` | stale |
| `judgment-census.json:793` (`record`) | `:797` | stale |
| K5 `test_story_run_s6.py:914,922` | `:923,931` (s0 `:1137` correct) | stale |
| `driver_conductor.py:602` no_move, `:852-870` unread, `:557` _ask_conductor, `:263` conductor, `:21` cap = 3, `:29` 6000, `:322-323` cut, `:312-314` words-file note | same | holds |
| `question_register.py:862` record, `:976-1023` record_answers, `:1020-1022` all_tokens, `:655` error direction, `:41-43` docstring, CLI header `1-15` | same | holds |
| `question-vocabulary.json:4` (`S2/S3/S4 stop`), `:17` (`conductor`) | same | holds |
| `question_stop.py:437` own words; `:464-465` BLOCKING_NOTE | same; also read at `:522` and `driver_dispatch.py:1646` | holds |
| `slow_tests.json:135` (27.6 s), `:139` (289.8 s) | same; the file is `scripts/slow_tests.json` | holds |
| §2.1 run evidence (`factory-7.log:2,4,6,7,32-38`; `factory-8.log:23`; digest `:13,:15`; answers `:3`) | verified on the root checkout. The logs are gitignored (`runs/.gitignore:3 *.log`): they exist only at `C:\QAFactory\forge-repo\experiments\...`, not in any worktree. The answers file and the digest are tracked. | holds, see F14 |
| "take_question_answer uses record_question_words' dict" (step 2 "unchanged") | `:1781` DISCARDS the return value today | see F11 |

**A negative claim re-checked.** E13(c): "no reader discriminates register records by `by`". Grep, case-insensitive:
`get\(["']by["']\)|\[["']by["']\]|by["']?\s*==` over `question_register, question_stop, planning_contract,
gate_brief, check_delivery, contract, driver_dispatch, driver_gates, report_*`. The only register hit is
`question_register.py:336`, which carries the field and does not branch on it. The other hits are unrelated dicts
(`check_delivery.py:1024`, `report_adapt.py:105`). Positive control: the same pattern over all of `scripts/*.py`
finds 40 or more known hits (`stand_gaps.py:724`, `probe_by_code.py:2629`, ...). I also checked
`planning_contract.apply_recorded_answers` (`:3459-3500`): it applies every SETTLED record and filters on neither
`where` nor `by`. So the conductor's `--where "S4 stop" --by conductor` records are applied by the same code. The
claim holds.

## 2. Feasibility, end to end

The main road works. `take_question_answer`, a dispatch member, calls `self.unread`. That is a lower layer, and
dispatch already calls it at `driver_dispatch.py:3217,3350,3450,3569,3824`. `unread` with `doors=None` goes to
`no_move`, then `_ask_conductor`, then `conductor`, which journals `total_cost_usd` (`driver_conductor.py:342-347`,
so P18 is counted). The QStub's conductor stub returns `continue` (`story_run_loop_b_common.py:55`), and the stub's
`d.py` runs `question_register.py` for real (`:47-52`), so K2 is feasible. A `Person` from the seam ends the process
through `_run_guarded`'s `except Person`, then `ask()` (`driver_machine.py:2017-2018`). The seam's own question
carries `offered` and is read by `take_seam_answer` (`:3540`). A token chosen there is never filed as role words and
never pops `pending_words` (`_file_words :4101-4112`).

Defects found on that road:

- **B2. I6 does not hold on a rerun without `--answer`.** Step 4 saves `pending_words[dispatch]`, `stop["resume"]`
  and `save_state()` BEFORE the seam can raise. A rerun with no `--answer` is a legitimate move. `unread`'s docstring
  (`driver_conductor.py:857`) says "the question without a call is the site's own, raised by a rerun with no
  `--answer`". On that rerun the loop's `wait_existing_job` reaches `_act_wait_existing_job`
  (`driver_machine.py:1451-1454`). It checks `pending_words` BEFORE the open-`asked` re-ask at `:1455-1463`, so the
  role is resumed while the conductor's question is still open. Then `resume_role` runs `question_threshold`
  (`driver_dispatch.py:1104`), which can raise a new `Person("questions")`, and `ask()` overwrites `asked`: the
  seam's question is lost (FR-7, AR-25). The halt precedent does not have this hole: it files `pending_words` AFTER
  `unread` returns (`driver_machine.py:3850`). So the spec's I6 rests on "the Person ends the process", which covers
  the `--answer` world only. Fix: see fork F-10.
- **F12. An answer site the spec does not list.** The person answers the seam's own question, raised from a question
  stop (kind `questions`, with `offered`), with register lines or free words that are not one of the offered tokens.
  Example: the conductor asks "which reading for Q3?" and the person answers `Q3: a`. That answer goes to
  `take_seam_answer`, then `unread(kind, ..., self.generic_prompt(...))` (`driver_machine.py:2365-2367`). Code
  records no token, and the conductor gets the generic prompt with no register instruction and no "recorded by
  code" line. So the second answer at the same stop takes another road than the first (axis 34). The halt twin has
  the same hole. `take_seam_answer` is owned by FV1-6. This cannot go into FV1-3's owns: it must be named in §6 and
  queued as a node with an owner (the Lead of the pile), or added to FV1-6 by the Lead.
- **F13. A neighbouring class, outside scope.** `after_close` (`driver_dialog.py:643-648`, reached from
  `driver_machine.py:3546-3550` and `:2357-2359`) only journals free words that arrive at a stage already done: no
  reader acts on them. That is the same "free words with no reader" class (P22). Queue it as a finding. It does not
  block FV1-3.
- Every state the conductor can return has a move (§3.4 holds): `continue`/`retry` returns; `ask_person` raises the
  priced Person; the cap gives `fallback_person` (`driver_conductor.py:646-647`); `stop` goes through
  `options_person` / `Stop` (`:677`). A `go on` chosen at that Person with no block is the FV1-13 #4 class, as F-3
  says.

## 3. Architecture

- AR-17 is kept: one seam, no new conductor call site. AR-24 is kept for the words (`answer_row` first, then
  `words=` plus the answer file). AR-13 and AR-14 are kept: `record` stays the one writer.
- **AR-19 / AR-15 is only partly kept.** The halt road and the question stop share the prompt member, but they file
  `pending_words` in a different order (see B2). The spec must say whether the order differs on purpose. F-10
  decides it.
- Touched but not named: **AR-22** (the producer and reader of `question_pass_lines`: B3 changes when it is produced
  relative to the resume); **AR-25** (the seam question lost on a rerun, B2); **FR-37 / FR-10** for the dry-run text
  `driver_machine.py:4143-4145`, "resume the role's own session with the words (no conductor)", which becomes false
  (F1).
- **FR-12**: no phrase list is added; the predicate is structural (`_only_tokens`, `question_register.py:957-973`).
  Holds.
- **P22**: holds for the first answer. F12 is the residual on the second answer.
- **P18**: the conductor's spend is journalled. `judged_reply` adds a judge call (`judge_reply.intent`,
  `judge_reply.py:46-49`) whose cost the spec never mentions (F4).
- **P31**: the design removes a second road. F-1 B and F-3 B would each be an exception, and only the owner can
  grant one.

## 4. Error direction of reused functions in a more responsible role

| Function, new role | Direction | Spec states it? |
|---|---|---|
| `record_answers` / `_only_tokens`: from token reader to the gate of the conductor hand-over | A missed token gives one more paid conductor call; a false "all tokens" is impossible (any prose, fenced, quoted, case-word or unknown line gives False). Toward the reader, correct. | yes (§1.1 AR-28, E11) |
| `judged_reply`: from gate/halt to the question stop | `judge_reply.intent` reads `INTENTS = approve, approve_with_edits, reject, question, waiver, other` (`judge_reply.py:27`) and truncates the reply to 4000 characters (`:48`). An answer to 18 questions read as `approve` reaches the conductor as "the option the judge reads in their words" (`PRE_FILLED`, `driver_conductor.py:34`). That error direction is toward a pass, and it is the wrong one. | **no**, §8 says only "it records nothing" (F4, F-9) |
| The conductor's own reading of free words (now writes `answered`) | A misreading becomes a settled record, and the plan follows it. Nobody at run time sees it, because nothing prints it back. | **no**. §1.2's "accepted by the tier above at critic/acceptance" is not true at run time (F7) |

Adversarial inputs:

- **Empty answer.** `take_answer` stops at `:3366-3367` before any branch. Correct (E1).
- **A token-looking word inside free text.** `Q1: a because ...` is not a token (E5, pinned already at
  `test_story_run_loop_b_threshold.py:68-84`). A whole-line `Q3: a` inside a paragraph that contradicts it is
  recorded by code. The conductor is then told "do not record these again", and the only door it gets is the
  `--reopen` text of an H6 refusal. Acceptable, by `parse_choices`'s stated direction (`:655`).
- **A very long answer.** The words go whole. But the QUESTION is cut twice: `qtext[:6000]` in the member
  (`driver_machine.py:3847`), then `refusal.strip()[:6000]` over moves section + text in `conductor()`
  (`driver_conductor.py:320`). The real S4 pack is 13 299 characters (`sed -n 93,235p runs/factory-6.log | wc -c`).
  So the end of the question text and the whole judged-reply tail are cut. The edge is not named (F6).
- **Another language.** Cyrillic look-alike letters are not tokens, so the answer goes to the conductor; FR-29
  fixtures use `chr()`. E7 covers it.
- **An answer to a question no longer open.** A settled id is refused by H6, and the refusal reaches the conductor.
  But the shared text labels it "Not read, still open:" (`driver_machine.py:3839`), which is false for a settled
  question (F8). An unknown id is named, and nothing is recorded for it. Holds.
- **Register hash.** Code stamps the hash AS SHOWN (`stop["shown"]`, `driver_dispatch.py:1781`). The conductor is
  told to use "the --register-hash that --show prints", which is TODAY's hash. A row that changed between showing
  and answering then loses its `changed_since_answer` signal (`question_register.py:866-868`) for answers recorded
  by the conductor only (F5).

## 5. Edges

- E1-E12 are decided correctly, with the exceptions noted in §4 (E8 cuts the question as well as the words; E9's
  label is false).
- **TEMPORAL (E13).** (a) An old `driver-state.json` with an open `questions` kind takes the new road: correct, and
  no state key is new. (b) No backfill (F-4). (c) Verified (§1). **Missing:** the rerun-with-no-answer world (B2)
  and the evidence's location (F14).
- **POSITIONAL (E14).** I1-I5 hold. **I6 is incomplete** (B2). **Moving step 6 after the seam breaks H36 on the
  Person path (B3).** Today the code-recorded tokens are applied to the plan BEFORE the resume, and the resumed role
  gets `question_pass_lines` (`driver_dispatch.py:1782-1784`, read at `:1720`). In the new order, a seam `Person`
  skips step 6. The next process answers the seam and resumes the role (`resume_role`, `question_resume_prompt`
  pops nothing), and only after the role returns does `question_threshold` apply the answers (`:1614`). The role has
  edited a plan code had not patched yet, and was never told. Fix: run `apply_question_answers` BEFORE the seam
  (code's records) AND after a returned seam (the conductor's records). It is idempotent ("a second call finds them
  and returns nothing", `planning_contract.py` docstring), so calling it twice is safe.
- **Conflicting pairs.** E15 is resolved only under I6, so it falls with B2. A second pair is not named: "byte-identical
  halt prompt" (K4) vs "one member with the judge on both roads" (§8). If F-9 changes the judge on register roads,
  K4's byte-identity must be narrowed.

## 6. Judgment (P27 / AR-29)

- The hand-over predicate is a shape check that routes and refuses nothing. "No census unit" is correct (A27 sees
  no Person/Stop/`py` in the new member: `audit_factory.py:1640-1700`).
- The census row for `record` is at `:797` (`safety`, `intent`). It stays unchanged.
- Census row 2's text "accepted by the tier above at critic/acceptance" is wrong: the conductor's reading of the
  person's words is judged by nobody before the plan follows it. The cheapest data-only cure, consistent with
  `record_question_words`' "printed back, so the person is never left guessing" (`driver_dispatch.py:1798-1804`):
  after a returned seam, code compares the register before and after and prints each new `by: conductor` record
  with its id and letter. That is data, not judgment, and the person can `--reopen`. Otherwise name the gap (F7).

## 7. Tests (`docs/TESTING.md`)

- **B1. A keep detector goes red and is outside owns.** `test_story_run_loop_b_threshold.py` (keep, detector,
  `test-layers.json:5834`, 25.0 s, `slow_tests.json:137`) pins the OLD behaviour. At `:68-92` it answers a stop with
  `Q5 I do not know yet...` and `Q6: a, but only for the admin role`, then asserts
  `check_eq("answer: no conductor was called (FR-48)", s.conductor_calls, [])`. `:139` repeats it cumulatively.
  `question_stop_fallbacks` (`:290-326`, words `"Q1: a\nand please keep the admin cases apart"`) asserts
  `conductor stayed out` at `:326`. Under FV1-3 each of these gets one conductor call. The file is not in owns or K
  rows, and it is in the printed witness scope while the spec's local run list leaves it out. The builder either
  ships a red keep file to CI or edits outside owns. `:362` (all tokens) stays green.
- K3 (12 rows, E2-E11 and E16, in `test_story_run_loop_b_answers.py`) is a receipt per spec edge, which TESTING.md
  §«Чего больше нет» forbids. Its parse rows (E4-E6, beyond-readings, unknown id) duplicate
  `test_story_run_loop_b_threshold.py:68-90` and `test_question_register.py` (F9). Keep only the NEW behaviour: the
  number of conductor calls and what it is told; words and words file whole AT 6000 and 6001; the apply order. Put
  these rows in `test_story_run_loop_b_threshold.py` beside the rows that flip, not in the halt-road file. K2 should
  take the REAL defect input, `experiments/mybooks/factory-vs-free-agent/answers/s4-questions-batch-1.md` (tracked,
  18 lines, 2 132 bytes): that is the one row that "fails before the change".
- The limit rows: the 6000 cut lives in `conductor()`, which QStub stubs away (`common.py:55`). A row asserting
  `len(words)` at `unread` cannot see the cut. Assert that the words FILE (`answer_file()`) is whole: that file is
  what carries the words past the cut.
- **Witness scope.** `scenario_walk.py --witness-for <the 3 owns>` prints 154 lines (run below). builder-rules 7b
  makes the printed set the scope, and files over a minute are CI's. The spec hand-picks 3 local files instead (F10).

## 8. Owns and crossings

- **Owns are not sufficient.**
  - `test_story_run_loop_b_threshold.py` is missing (`question_stop_road`, `question_stop_fallbacks`) (B1).
  - `driver_dispatch.py` "nothing else" excludes the import line `:20`, which must gain
    `MOVES_RULE, OWN_TOKEN_RULE, PRE_FILLED` (F3).
  - `driver_machine.py` needs `Driver.describe` (`:4143-4145`, F1) and the comment `:3555-3556` "no conductor, no
    judge" (F2).
  - A guard in `_act_wait_existing_job` if F-10 takes option A.
  - `driver_machine.py:22`'s import stays as it is: `PRE_FILLED` is still used at `:4082`.
- **Shared functions.** No function is written by two nodes.
  - FV1-22 owns `WINDOW_ROUND_STAGES`, `finish`, `rework`, `repair_limit_*` and `window_round_gate`: disjoint. Its
    line "N3 after FV1-3 for `driver_dispatch.finish`" is moot, because FV1-3 does not touch `finish`.
  - CL4-1 owns `window_round_gate`: disjoint.
  - FV1-6 owns `driver_conductor.unread` and `no_move_facts`, and `driver_machine.take_seam_answer`, `seam_chosen`,
    `seam_rework_step`. FV1-3 CALLS `unread`, and FV1-6 adds a keyword `asked_why: str = ""`
    (`20261113-fv1-6-...-spec.md:171`), which is additive and compatible. But §6 names FV1-22 as the party that must
    not touch `unread`; it must name FV1-6 as its owner, and the call shape FV1-3 relies on
    (`unread(kind, stage, dispatch, text, words=...)`).
  - F12 lives in FV1-6's `take_seam_answer`.
  - FV1-13 depends on FV1-3's new member and must get it in its `given`.
- **Hot files.** `driver_machine.py` and `driver_dispatch.py` are not on PROJECT.md p.3's hot list. Disjoint
  function lists are enough.

## 9. Executable by a weaker model? Is FV1-9 sequential?

- FV1-3 names a file, a function, behaviour and a test per item, and the direction is chosen. After B1-B4 and
  F1-F11 it is executable by a builder. As drafted, the stale `given:` ranges (B4) send the builder 38-47 lines
  away from the code, and nothing in the spec warns of it.
- FV1-9 is NOT executable. By its own text the owns are an "estimate", F-7 and F-8 are open, and it needs a scout
  pass. Its DoD contradicts its design: the design hints on a shared `source_says[].where` OR `now.where`, while the
  DoD says "same where, different now.where -> no hint". E7 puts the replay check "after the idempotency return
  `:1319-1332`", which is inside `_raise`, but the hint lives in `raise_for_case` (`:1373`), and the spec does not
  say how `raise_for_case` tells a replay apart (F15).
- **Sequential?** Not by files: FV1-3 writes neither `question_register.py` nor anything FV1-9 owns. It is sequential
  only because FV1-9 is not ready. F-5 A is acceptable de facto, but the reason it gives is wrong.

## Forks: is the recommendation right, and whose decision is it?

| Fork | Recommendation right? | Whose decision |
|---|---|---|
| F-1 owns beyond the batch row | **A, yes**. B is a P31 exception. | Lead (technical; the batch is not taken, status «ожидает»). B would be the owner's alone. |
| F-2 predicate | **A, yes** | Lead, technical |
| F-3 `go on` with no block | **A, yes**; FV1-13 depends on FV1-3 (already in the batch row) | Lead, technical; B is a P31 exception |
| F-4 no backfill | **A, yes** | Lead, highlighted «решила сама» (an in-flight person pays one more round) |
| F-5 order | **A, acceptable**, but the reason is readiness, not files | Lead, technical |
| F-6 BLOCKING_NOTE vs the quarantined pin | **A, yes**; B breaks FR-10. Do not edit the quarantined file. | Lead, technical; the owner is told the same turn the `quarantine-watch` alert fires (CLAUDE.md rule 11) |
| F-7 a repeated raised question: a way out | B is technically sound (AR-25) | **OWNER**: it lets a role take a question out of what the person is asked (P13/P20, product and process risk) |
| F-8 a question "cannot be answered as it stands" | **A, yes** | **OWNER**: what a person is shown, and whether to hide it |
| F-9 (new) `judged_reply` on the register roads | recommend: call the judge only when `recorded is None` (S1 review, a halt with no register). That is a data condition and P31-clean. K4's byte-identity then holds for those two roads only. | Lead, technical |
| F-10 (new) I6 on a rerun with no answer | recommend A: keep the floor (step 4), and in `_act_wait_existing_job` re-ask an open `asked` of this dispatch (question file present) BEFORE the `pending_words` resume. Positional invariant: "a role is never resumed while a question about its dispatch is open". B: file the words after the seam like the halt road, which loses the floor on a raise. | Lead, technical |
| F-11 (new) print-back of the conductor's records | recommend: code prints new `by: conductor` records after a returned seam (data only), else a named gap | Lead, technical |

## Standing lines

- **DUPLICATION AND CONSISTENCY.** One finding: K3's parse rows duplicate `test_story_run_loop_b_threshold.py:68-90`
  and `test_question_register.py` (F9). The new member is a MOVE of `_unread_halt_or_review`'s body
  (`driver_machine.py:3828-3849`), not a copy. Correct. Grepped `self.unread(` in `driver_dispatch.py` (5 existing
  sites) and `MOVES_RULE|OWN_TOKEN_RULE|PRE_FILLED` across `driver_*.py` (the home is `driver_conductor.py:34,41,47`).
- **CODE QUALITY (plan level).** The new member takes 6 positional parameters. The body moved from `:3828-3849` is
  about 22 lines, under 60. One wording defect is carried into the shared text: "Not read, still open" for an H6
  refusal (F8). There is no dead branch in the design.
- **ONE ROAD (question 12).** The design removes the second road (threshold vs halt). Residuals:
  - F12, the seam's second answer, on the generic road for both twins. Proposed node, owner: the Lead of
    `live-run-fvf`, or folded into FV1-6.
  - F-1 B and F-3 B are P31 exceptions, and only the owner can grant one. The designer rightly does not recommend
    them.
  - None found otherwise. Grepped `kind == "questions"|"questions"` over `driver_*.py` and `no_move.py`
    (`EXCLUDED_KINDS = ("s1_review",)` at `no_move.py:36`: `questions` is not excluded, so it gets the full seam).

## Amendments: section, then what to change (all are spec edits the Lead can apply; B2 and F7 apply forks F-10 and F-11)

Blockers:
- **B1** §4 owns, K, verification: add `test_story_run_loop_b_threshold.py` (functions `question_stop_road`,
  `question_stop_fallbacks`). Flip `:92` and `:326` to "conductor called once", keep `:139` honest, and run it
  locally (25 s).
- **B2** §3.2 I6 and E14: state the invariant for a rerun with no `--answer` and apply F-10 (add
  `Driver._act_wait_existing_job` to the owns of `driver_machine.py`, plus a row: open seam question + a rerun with
  no answer means the question is re-asked and `resume_role` is not called).
- **B3** §3.2 step 6, E14, K2: call `apply_question_answers` before the seam (after step 4) AND after a returned
  seam. Add a row: seam raises `Person`, so the code-recorded token is applied and `question_pass_lines` is set
  before the raise.
- **B4** §2.2, §4 given, K5 and the edges: replace every stale reference with its §1 value from this review, and
  stamp "facts re-taken on e4ba384".

Fixes:
- **F1** §4 owns: `Driver.describe` (`driver_machine.py:4143-4145`), whose dry-run sentence "(no conductor)"
  becomes false (FR-37).
- **F2** §4 owns: the comment `driver_machine.py:3555-3556`. The docstring `driver_dispatch.py:1747-1751` ("Nothing
  here calls the conductor") must be rewritten, and it already sits inside an owned function.
- **F3** §4 owns: `driver_dispatch.py:20` (the import of the three constants).
- **F4** §8 and §4 edges: replace "judged_reply is called on both roads" with fork F-9's decision, and state the
  judge's error direction and cost.
- **F5** §3.1 text for `questions`: give the conductor the hash each question was SHOWN with (`stop["shown"]`), or
  tell it to pass that hash, not `--show`'s current one. Add an edge row.
- **F6** §4 E8: name the two 6000 cuts of the QUESTION text (`driver_machine.py:3847`, `driver_conductor.py:320`).
  The conductor reads the questions through `question_register.py --show`, and the prompt says so. Add a row at the
  real pack size.
- **F7** §1.2 row 2 and §3.4: apply fork F-11 (print-back), or name the gap. Correct "accepted by the tier above".
- **F8** §3.1: in the shared text, an H6 refusal is listed as "already settled (door: --reopen)", not as "Not read,
  still open".
- **F9** §4 K3: cut to the new-behaviour rows and move them to `test_story_run_loop_b_threshold.py`. K2 takes
  `answers/s4-questions-batch-1.md` as its input. The limit rows assert the words FILE.
- **F10** §4 verification: "run every file the command prints that takes under a minute; CI judges the rest"
  (builder-rules 7b), not a hand-picked three.
- **F11** §3.2 step 2: `read = self.record_question_words(...)` (the value is discarded today at `:1781`).
- **F12** §4 siblings and §6: name the seam's second answer (`driver_machine.py:2365-2367`, owned by FV1-6) as a
  queued node with an owner.
- **F13** §4 siblings: name `after_close` (`driver_dialog.py:643-648`) as a queued finding.
- **F14** §2.1 and §4 given: the run logs are gitignored and exist only in the root checkout. Give their absolute
  root paths, or quote the lines into the spec.
- **F15** §5 FV1-9: resolve the AND/OR conflict between design and DoD, and say how `raise_for_case` tells a replay.
  After F-7 and F-8 and the scout pass, FV1-9 goes back to the designer.
- Also, in §4 siblings: enumerate axis 5, the row «One question for every stop» (A27): no change is needed, because
  the member has no Person, Stop or `py`.

## Trail

Read (on read-main e4ba384 unless marked):
- the spec, whole
- `driver_dispatch.py:1020-1119, 1580-1900`
- `driver_machine.py:1440-1470, 1852-1891, 2000-2039, 2325-2445, 3361-3420, 3520-3640, 3814-3863, 4085-4160`
- `driver_conductor.py:215-354, 468-498, 557-947`
- `question_register.py:1-50, 850-1024, 1315-1335`
- `question_stop.py` (grep)
- `no_move.py:36-40`
- `judge_reply.py:1-75`
- `planning_contract.py:3459-3500`
- `story_run_loop_b_common.py:20-80`
- `test_story_run_loop_b_answers.py:30-85, 200-225`
- `test_story_run_loop_b_threshold.py:60-140, 280-365`
- `test_question_stop.py:590-598`
- `test-layers.json` (rows), `driver-layers.json` (rows), `judgment-census.json:3-4, 788-797`, `slow_tests.json`,
  `audit_factory.py:1640-1700`
- `docs/TESTING.md:1-66`, `docs/SIBLING_MAP.md` (axes 5, 17, 18, 34), `docs/tasks/critic-diff-brief.md:37-96`,
  `plans/builder-rules.md:14-23`
- the batch row (`batch-1-live-run-fvf.md:11, 36, 39, 42, 45, 56`)
- the FV1-6, FV1-22 and CL4-1 specs (owns and crossings)
- root: `runs/factory-6.log:93-235`, `factory-7.log:1-8, 32-38`, `factory-8.log:23`,
  `digests/S4-qa-case-designer-2.txt:13, 15`, `answers/s4-questions-batch-1.md`

Commands:
- `git -C read-main log --oneline -1` printed `e4ba384 wave 1 integration report`
- `python -B <read-main>/.../scenario_walk.py --witness-for driver_dispatch.py driver_machine.py question_stop.py`
  printed 154 lines, including `keep test_story_run_loop_b_threshold.py (layer detector, covers it)`
- `sed -n 93,235p runs/factory-6.log | wc -c` printed `13299`
- `git check-ignore -v .../factory-7.log` printed `runs/.gitignore:3:*.log`
- the case-insensitive `by` grep, with its positive control (§1)

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 sec.4 owns/K/verification: test_story_run_loop_b_threshold.py (keep detector, test-layers.json:5834) asserts no conductor on free words at :92, :139, :326; FV1-3 flips them; the file is outside owns and outside the local run list",
    "B2 sec.3.2 I6/E14: pending_words + resume saved before the seam; a rerun with no --answer reaches _act_wait_existing_job (driver_machine.py:1451-1454), which resumes the role before re-asking the open seam question (:1455-1463); question_threshold can then overwrite asked (AR-25, FR-7)",
    "B3 sec.3.2 step 6: moving apply_question_answers after the seam skips it on a Person raise; the resumed role gets no question_pass_lines for code-recorded tokens (H36, driver_dispatch.py:1782-1784, :1720); apply before AND after the seam (idempotent)",
    "B4 sec.2.2/sec.4 given/K5: every driver_dispatch.py, driver_machine.py, driver-layers, test-layers, audit, census and s6 line number is stale (+38/+47); re-take on e4ba384 (table in review sec.1)"
  ],
  "fixes": [
    "F1 sec.4 owns: Driver.describe driver_machine.py:4143-4145 says (no conductor), false after FV1-3 (FR-37)",
    "F2 sec.4 owns: comment driver_machine.py:3555-3556; rewrite docstring driver_dispatch.py:1747-1751",
    "F3 sec.4 owns: import line driver_dispatch.py:20 gains MOVES_RULE, OWN_TOKEN_RULE, PRE_FILLED",
    "F4 sec.8/edges: judged_reply runs the gate-intent judge (judge_reply.py:27, :46-49) on a question pack; decide fork F-9, state its error direction and cost",
    "F5 sec.3.1: the conductor is told --show's current hash while code stamps the shown hash (stop[shown]); pass the shown hashes",
    "F6 sec.4 E8: name the two 6000 cuts of the question text (driver_machine.py:3847, driver_conductor.py:320); real pack 13299 chars; a row at that size",
    "F7 sec.1.2 row 2: the conductor's reading is accepted by nobody at run time; print back new by:conductor records (fork F-11) or name the gap",
    "F8 sec.3.1: an H6 refusal is labelled Not read, still open (driver_machine.py:3839); say already settled with the reopen door",
    "F9 sec.4 K3: cut to new-behaviour rows, move them to test_story_run_loop_b_threshold.py, K2 input = answers/s4-questions-batch-1.md, limit rows assert the words file",
    "F10 sec.4 verification: run every printed file under a minute (builder-rules 7b), not a hand-picked three",
    "F11 sec.3.2 step 2: capture read = record_question_words(...) (discarded today at driver_dispatch.py:1781)",
    "F12 sec.4 siblings/sec.6: the seam's second answer at a question stop goes generic (driver_machine.py:2365-2367, FV1-6's take_seam_answer); queue a node with an owner",
    "F13 sec.4 siblings: after_close (driver_dialog.py:643-648) journals free words with no reader; queue a finding",
    "F14 sec.2.1/given: the run logs are gitignored (runs/.gitignore:3) and exist only in the root checkout; give absolute paths or quote",
    "F15 sec.5 FV1-9: DoD AND vs design OR on where/now.where; replay detection location; back to the designer after owner decides F-7/F-8 and the scout pass"
  ],
  "class_completeness": "Axis 34 / AR-19: the threshold stop joins the halt road (covered), but the pending_words order differs (B2), and the seam's second answer stays generic on both twins (F12, FV1-6's function, to queue). Axis 5 'One question for every stop' (A27): n/a, no Person/Stop/py in the new member. Neighbour class 'free words with no reader': after_close (F13), to queue. Sibling texts: describe() (F1), BLOCKING_NOTE (both readers, :522 and driver_dispatch.py:1646) covered by the one constant.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-fv1-3-free-answer-to-conductor-spec.md",
      "read-main ai-packages/qa-factory/scripts/driver_dispatch.py:1020-1119,1580-1900",
      "read-main ai-packages/qa-factory/scripts/driver_machine.py:1440-1470,1852-1891,2000-2039,2325-2445,3361-3420,3520-3640,3814-3863,4085-4160",
      "read-main ai-packages/qa-factory/scripts/driver_conductor.py:215-354,468-498,557-947",
      "read-main ai-packages/qa-factory/scripts/question_register.py:1-50,850-1024,1315-1335",
      "read-main ai-packages/qa-factory/scripts/judge_reply.py:1-75",
      "read-main ai-packages/qa-factory/scripts/planning_contract.py:3459-3500",
      "read-main ai-packages/qa-factory/scripts/tests/story_run_loop_b_common.py:20-80",
      "read-main ai-packages/qa-factory/scripts/tests/test_story_run_loop_b_answers.py:30-85,200-225",
      "read-main ai-packages/qa-factory/scripts/tests/test_story_run_loop_b_threshold.py:60-140,280-365",
      "read-main test-layers.json, driver-layers.json, judgment-census.json, slow_tests.json, audit_factory.py:1640-1700",
      "docs/TESTING.md:1-66, docs/SIBLING_MAP.md axes 5/17/18/34, docs/tasks/critic-diff-brief.md:37-96, plans/builder-rules.md:14-23",
      "read-main plans/piles/live-run-fvf/batch-1-live-run-fvf.md rows; specs fv1-6, fv1-22, cl4-1 owns/crossings",
      "root experiments/mybooks/factory-vs-free-agent runs/factory-6.log:93-235, factory-7.log:1-8,32-38, factory-8.log:23, digests/S4-qa-case-designer-2.txt, answers/s4-questions-batch-1.md"
    ],
    "reruns": [
      {"command": "git -C .claude/worktrees/read-main log --oneline -1", "result": "e4ba384 wave 1 integration report"},
      {"command": "python -B read-main/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for driver_dispatch.py driver_machine.py question_stop.py | wc -l", "result": "154 lines; includes keep test_story_run_loop_b_threshold.py (layer detector, covers it)"},
      {"command": "sed -n 93,235p runs/factory-6.log | wc -c", "result": "13299"},
      {"command": "git check-ignore -v experiments/mybooks/factory-vs-free-agent/runs/factory-7.log", "result": "runs/.gitignore:3:*.log"},
      {"command": "Grep -i get(by)|[by]|by== over the register readers (positive control: same pattern over scripts/*.py)", "result": "only question_register.py:336 (carries, no branch); control found 40+ hits"}
    ]
  }
}
```
