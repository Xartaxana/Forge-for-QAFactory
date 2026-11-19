# t-1585 FV3-40 diagnosis: s5.nobody_{review,environment,tooling}/{stop,free words}

Verdict: NEEDS WORK. The defect is in the dry row contract, not in the driver (product) and not in the seed or stub.
The `stop` rows list C3, but their price row says the factory does nothing (fixture fix, measured green). The `free words`
rows list C2 and C3, which by the product's design these words can never satisfy, and the walk grammar has no check
that such a row can carry (judge/grammar fix; the Lead picks between two options). Diagnosis only; no file of the repo was edited.

## 1. Per-row cause table

| row | answer path (driver) | what is written | why C3 (fingerprint unchanged) | why C2 | cause | fix place |
|---|---|---|---|---|---|---|
| s5.nobody_review/stop (s5.json:409) | A | B | C | passes (measured) | F1 | s5.json:469-474 |
| s5.nobody_environment/stop (s5.json:748) | A | B | C | passes (measured) | F1 | same rows' `expect` |
| s5.nobody_tooling/stop (s5.json:1019) | A | B | C | passes (measured) | F1 | same rows' `expect` |
| s5.nobody_review/free words (s5.json:477) | D | E | G | H | F2 | dry_exits.py (see 4) |
| s5.nobody_environment/free words (s5.json:816) | D | E | G | H | F2 | same |
| s5.nobody_tooling/free words (s5.json:1087) | D | E | G | H | F2 | same |

All three families reach the SAME code path: the question is raised by `repair_limit_raise` (driver_dispatch.py:3355-3362,
`kind: "repair_limit"`, `call=False`), and the key is chosen in `repair_limit_facts` (driver_dispatch.py:3313-3317). So the
cause is one per answer and the family does not matter.

**A (stop):** `driver_dispatch.py::_answer_repair_limit` (:3432). `token == "stop"` is in `ask["offer"]`. It calls
`answer_row` (:3454), then `record_answer(token)` (:3457), then raises
`held_question(stop_held(...))` (:3458; driver_dialog.py:596-619). That builds the same Person again: kind `repair_limit`,
same stage and dispatch, the same `offered`, with a `held_lead`.

**B (stop writes):** a `driver-answers.jsonl` row with the ask's question_sha (this is why C2 passes), the answer row, and
`asked` rewritten as kind `repair_limit` at S5 with `held_lead`. Nothing is written to pipeline.json, the controller, the
handoffs or the stage outputs, and no waiver is written (`repair_pass_keys` is never reached for stop).

**C (stop, C3):** `dry_exits.py::state_fingerprint` (:974-1019) hashes the stage statuses, gates, acceptance, dispatch
statuses and rounds, handoff forms, stage outputs, and only `asked.kind`/`asked.stage` (:988-991). None of these changes.
That is the design: the price row of `stop` under all three keys says `"factory": "nothing"` (references/question-prices.json:166-180;
quoted from the loaded data: `('stop', 'nothing')`). The card that defines C3 says it is "listed only where data expects a
change" (docs/tasks/specs/20261117-p1b-gate-ask-judge-card-r2.md:123). The C3 n/a guard allows n/a exactly when the price row
says `nothing` (dry_exits.py:1543-1548). The sibling rows already do this: gates.json:23 `gate_A/stop` and s0.json:34
`halt/stop` carry `checks ["C2"(, "C6")]`, `na {"C3": "factory nothing: ..."}`. The s5 stop rows list C3 (s5.json:469-474),
which contradicts the card and the price data.

**D (free words):** `_answer_repair_limit` (:3432): the words normalise to no token of `ask["offer"]`, so the branch at
:3446-3449 calls `self.unread("repair_limit", ..., doors=offer, again=repair_limit_person)`.
`driver_conductor.py::unread` (:881-903) runs `record_answer("")` (:894), then sets state `why: "unread_answer"`, `kind:
"repair_limit"` (:896) and calls `no_move(state, moves)` with no `call=False`. So the conductor IS called. This is by design:
D-0041 (:885 "EVERY `--answer` is new words ... this always calls the conductor"), and repair_limit_raise's docstring
(:3356-3357, "a word that is none of them goes to the conductor once"). The dry conductor stub answers `ask_person` with
the open moves (dry_stub.py:111, selftest :1345-1346). `options_person` -> `_person_of` (driver_conductor.py:815-828, :439-448)
builds a Person whose kind is the STATE's kind, `repair_limit`, with `why = "unread_answer"`. `ask()` writes
`asked = {kind: repair_limit, stage: S5, ..., why: unread_answer}` (driver_dialog.py:315-323).

**E (free words writes):** an answer row (record_answer at :894), one stub conductor journal line (`conductor: "conductor"`,
dry_stub.py:1115), and the same closed question again. Nothing moves the story.

**G (free words, C3):** `asked.kind/stage` are still `repair_limit`/S5, and nothing else in the fingerprint changed (as in C).
By design nothing is recorded until the person picks a door. gates.json:24 declares this same reason for `gate_A/free words`.

**H (free words, C2):** `dry_exits.py::_check_c2` (:1428-1447) fails on ANY conductor call in the answer's own turn,
unless the call is `chosen` and excused, which needs a token (:1419-1425). So C2 cannot pass on a free-words answer to a closed
question whose product road is `unread` -> conductor. The FAIL text's second half, "its why is not on record", is a
judge-side gap, not the product's. The walker collects whys only when the pending ask's kind is `conductor`
(dry_world.py:1381-1382). Here the pending kind is `repair_limit`, and the why sits in `asked.why`, which the walker does not
read. If it did read it, C2 would still fail, with the text "with why unread_answer" (:1446). So C2 is red by construction,
whichever why is read. Established by reading; the `asked.why` value was not dumped from a world (no probe spent on it).

## 2. Product or fixture

- **stop (F1): fixture.** The `expect` block of the 3 rows lists C3 against card r2 :123 and price data `factory: nothing`.
  The product holds the question and records the answer, as its price row says. Evidence: driver_dispatch.py:3456-3458,
  question-prices.json:166-180, card r2:123, guard dry_exits.py:1543-1548, precedent gates.json:23 and s0.json:34.
  **Measured:** with `checks ["C2"]`, `na {"C3": ...}`, all 3 stop rows PASS (run below).
- **free words (F2): neither product nor seed/stub. It is the walk grammar/judge.** The product routes the words to
  the conductor by design (driver_conductor.py:885, driver_dispatch.py:3357). C2 and C3 are red by construction (H, G). The
  card's answer for free words at a seam question is "C2 and C3 n/a" (card r2:170, :346, F-4 (a)). It names C6 as the one
  remaining check, but C6 is gate-only. A non-gate key has no check left, and the loader refuses a runnable row with no listed
  check (dry_exits.py:1171-1172). The same block was already recorded at known_red s6-s9 `s6.stand_confirm/free words`
  ("the recipe cannot declare C2 and C3 n/a: a walk row needs one check and C6 is gate-only").
  **Measured:** C5 cannot stand in for it. With `checks ["C5"]`, `na {C2, C3}`, all 3 free-words rows FAIL C5: "the same
  question `repair_limit` at S5 was asked a third time with nothing new given to the author". That is the walker re-sending
  the same words to the re-raised identical ask (dry_world.py:1394-1396, G3), not a person's road.

## 3. Findings

**F1 (fixture; fix before the ledger rows leave).** s5.json `s5.nobody_{review,environment,tooling}/stop` `expect`
(:469-474, and the same block in rows :748 and :1019) list C3 for a token priced `factory: nothing`. Fix: `"checks":
["C2"], "na": {"C3": "factory nothing: stop holds the question; nothing is recorded (driver_dispatch.py _answer_repair_limit)"}`.
Then drop the 3 ledger rows from known_red/s5.json (pin 49 -> 46).
Test row: the 3 rows themselves (`--part exits:s5`): measured PASS.

**F2 (judge/grammar; the fork is the Lead's).** No check exists that a `free words` row at a non-gate closed question can
carry and pass. ONE fix place: `ai-packages/qa-factory/scripts/tests/dry_exits.py`. The Lead chooses between two options:
  - (a) Exempt in `_walk_expect_problems` (:1171): a runnable row whose C2 and C3 are both declared n/a may list no check.
    It is then judged by its always-checks (K15 on the key's window, E18, turns). Cheap, but the free-words road is then
    judged only by "the key was priced".
  - (b) Add a judged check in `JUDGE_CHECKS` (:1495), for example "Cw: free words at a closed question". It requires: an
    answer row with the ask's question_sha, at most one conductor call in the answer's turn with why `unread_answer`, the
    same key priced again in the new ask's window, and `asked.words_file` set. This also needs dry_world.py:1381 to collect
    `asked.why` for a non-conductor pending ask. Recommended, because it judges what the product promises, and it closes the
    same gap for every free-words row of this class.
  Test row: one row in the `judge_row` table of dry_exits.py's selftest (beside the C2 cases at :3196) for the chosen
  check or exemption, plus the 3 fixture rows switched to it (`--part exits:s5`), and the ledger rows dropped.

**F3 (judge text, minor; fold into F2 (b)).** The "its why is not on record" text of `_check_c2` (:1446) is misleading when
the pending ask is a site question. The why is on record in `asked.why` (driver_dialog.py:323), but the walker reads it only for
kind `conductor` (dry_world.py:1381). Fix place: dry_world.py:1381. Test row: a `judge_row` case where a site-kind pending
ask carries `why: unread_answer`.

## 4. Class notes (SIBLING_MAP axis 38, the dry census rows)

- Every `stop` price row I checked says `factory: nothing`: s5.repair_limit, exit.resume_limit, exit.resume_limit_halted,
  code_close.{stage,factory_file,behind}, s6.gate_a_dry, s7.repair_limit, s7.open_work, s8.delivery.no,
  s8.delivery.after_checks. Still, these rows list C3 on `stop` with no n/a: s5.json `s5.repair_limit/stop`,
  `exit.resume_limit/stop`, `exit.resume_limit_halted/stop`, `code_close.{stage,factory_file,closed_story,behind}/stop`, and
  s6-s9.json `s6.gate_a_dry/stop`, `s7.repair_limit/stop`, `s7.open_work/stop`, `closed.held/stop`,
  `s8.{report_match,delivery_check,delivery.yes,delivery.after_checks,delivery.no}/stop`. Most are in known_red for an
  EARLIER defect (seed not reached), so the F1 mismatch would show next, once they reach their key. The ones NOT in any
  ledger (closed.held, code_close.closed_story, s8.*) — not established whether they pass today (a stop that ends the asked
  record would change `asked.kind`) or never run; not run here. Recommended: F1 is applied to the whole class in the same
  round, or to a node the Lead opens: `stop rows list C3 against factory nothing | узел: <Lead opens>`.
- Every `free words` row at a closed question that routes through `unread` carries the F2 problem. Measured or recorded
  siblings: s6.stand_confirm/free words (FV3-16, raised_by above), and the free-words rows of s5.repair_limit,
  exit.resume_limit*, code_close.*, s6.*, s7.*, s8.* (list in the trail). F2 (b) is the class fix.

## 5. Trail

Read: the given three files; driver_dispatch.py:3140-3480; driver_conductor.py:439-563, 622-829, 881-929; driver_dialog.py:296-335,
585-624; dry_exits.py:66-80, 974-1019, 1037-1042, 1140-1179, 1380-1716; dry_world.py:1120-1415, 798-807; dry_stub.py conductor
greps; question-prices.json keys s5.nobody_*, all stop rows listed above; card r2 greps (:60-63, :115-142, :170, :346);
gates.json:20-32, s0.json:33-36; known_red/*.json raised_by of halt/free words and s6.stand_confirm/free words.

Run (one, background, on a TEMP COPY of the rows; no repo file touched):
`( cd ai-packages/qa-factory && python -B scripts/tests/test_scenario_dry_1.py --part exits:s5 --exits-root $TEMP/t1585/root --ledger $TEMP/t1585/none.json )`.
The root holds only the 6 rows, with `expect` changed as in F1 (stop: checks [C2], na C3) and as in a C5 trial (free words: checks
[C5], na C2+C3), plus the real seeds/s5.json. Tail (verbatim, cut):
```
NOTE dry-1/exits:s5/prefix: reached S4 in 170.7 s; snapshots S0, S1, S2, S3, S4
PASS dry-1/exits:s5/s5.nobody_review/stop
FAIL dry-1/exits:s5/s5.nobody_review/free words — C5: the same question `repair_limit` at S5 was asked a third time with nothing new given to the author (C5, the loop of FV1-13/FV1-22); n/a C2: ...; n/a C3: ...
PASS dry-1/exits:s5/s5.nobody_environment/stop
FAIL dry-1/exits:s5/s5.nobody_environment/free words — C5: the same question `repair_limit` at S5 was asked a third time ...
PASS dry-1/exits:s5/s5.nobody_tooling/stop
FAIL dry-1/exits:s5/s5.nobody_tooling/free words — C5: the same question `repair_limit` at S5 was asked a third time ...
FAIL dry-1/exits:s5/alive — alive only stop: s5.nobody_review: every variant but stop left the state fingerprint unchanged (free words)
PASS dry-1/exits:s5/outcomes
=== scenario dry-1: 4/13 ok ===
exit 1
```
The `alive` FAILs come from the 6-row root: review/debt/fixed are absent there. In the real file those variants PASS (t-1551),
so `alive` does not fire. The `known_red new red` FAILs come from the empty ledger. The log is kept at
`%TEMP%/t1585/run.log`. The original C2/C3 red text is t-1551's witness (report :16-17, :29-37). It is consistent with the
paths above: stop failed only on C3, and C2 passes, as re-measured.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F1: exits/s5.json s5.nobody_{review,environment,tooling}/stop expect: checks [C2], na {C3: factory nothing}; drop the 3 known_red rows (pin 49 -> 46); test row: the 3 rows under --part exits:s5 (measured PASS)",
    "F2: dry_exits.py: no check a non-gate free-words row can carry; Lead's fork (a) _walk_expect_problems :1171 exemption or (b) new judged check in JUDGE_CHECKS (recommended); test row: judge_row selftest case + the 3 free-words rows",
    "F3: dry_world.py:1381 reads why only for kind conductor; asked.why of a site question is missed, so the C2 text misstates the cause; fold into F2 (b)"
  ],
  "class_completeness": "stop rows listing C3 against factory nothing: 16 more rows in s5.json and s6-s9.json (listed in section 4); free-words rows at closed questions routed through unread share F2; the Lead applies F1 class-wide or opens a node; whether the unledgered s8.*/closed.held/code_close.closed_story stop rows pass today is not established",
  "trail": {
    "read": [
      "docs/tasks/specs/reports/t-1551-fv3-35a-report.md",
      "ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/exits/s5.json",
      "ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/known_red/s5.json",
      "ai-packages/qa-factory/scripts/driver_dispatch.py:3140-3480",
      "ai-packages/qa-factory/scripts/driver_conductor.py:439-563,622-829,881-929",
      "ai-packages/qa-factory/scripts/driver_dialog.py:296-335,585-624",
      "ai-packages/qa-factory/scripts/tests/dry_exits.py:66-80,974-1042,1140-1179,1380-1716",
      "ai-packages/qa-factory/scripts/tests/dry_world.py:798-807,1120-1415",
      "ai-packages/qa-factory/references/question-prices.json",
      "docs/tasks/specs/20261117-p1b-gate-ask-judge-card-r2.md",
      "ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/exits/gates.json",
      "ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/exits/s0.json"
    ],
    "reruns": [
      {
        "command": "( cd ai-packages/qa-factory && python -B scripts/tests/test_scenario_dry_1.py --part exits:s5 --exits-root $TEMP/t1585/root --ledger $TEMP/t1585/none.json )  [temp root: the 6 rows, stop expect checks [C2] na C3, free words checks [C5] na C2+C3]",
        "result": "PASS s5.nobody_review/stop, s5.nobody_environment/stop, s5.nobody_tooling/stop; FAIL the 3 free words rows on C5 (same question repair_limit at S5 asked a third time); scenario dry-1: 4/13 ok; exit 1"
      }
    ]
  },
  "mutants": [],
  "mutants_none": "diagnosis gate, no diff with new behaviour under review; the one run was an expectation trial on a temp copy of the rows"
}
```
