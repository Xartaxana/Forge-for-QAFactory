# t-1244 / FV3-16: why free words fail C2/C3 at `kind:halt` and `s6.stand_confirm` (diagnosis)

Critic diagnosis of an unclear bug (CLAUDE.md rule 3). Node `live-run-fvf/3/FV3-16`. The diagnosis is the input to the Lead's decision; it does not decide it (critic rule 6).

**Verdict: NEEDS WORK, on BOTH sides, at both sites.** The product has a real defect, and the walk row's expectation is also wrong. Fixing only one side leaves both rows red:
- **Product (one root, two sites).** When a free answer is handed to the seam and the conductor asks back (`ask_person`), the `Person` leaves `take_answer` before its last line. So `driver-answers.jsonl` gets no row. At the halt, the words are also never filed for the role.
- **Check.** C2 ("no conductor call followed the answer") and C3 ("the state fingerprint moved") cannot hold for a free answer that goes to the conductor and is asked back. They fail even after the product fix. They are n/a there, the way the gate rows already declare them. Declaring both n/a leaves the row with no check, so the walker needs one new check kind (C11 below).

## Reproduction (in-process, the seam test rig, ~10 s)

I drove `take_answer` with `no_move_seam_common.logged_rig`, which stubs the conductor (command and verbatim output in the Trail):

| case | Person raised | conductor calls | driver-answers rows | `pending_words[dispatch]` | seam question's `words_file` holds the answer bytes |
|---|---|---|---|---|---|
| halt S1, free words, conductor asks back | yes (kind `halt`, offered retry/go on/stop) | 1 | **0** | **None** | yes |
| same, turn 2 (the same words re-sent to the seam question, as the walker does) | yes | — | **0** | **None** | — |
| halt S1, free words, conductor `continue` (control) | no | 1 | 1 | `'go on without it'` | — |
| stand S5, free words, conductor asks back | yes (kind `environment`) | 1 | **0** | n/a (no dispatch) | yes |
| stand S5, free words, conductor `continue` (control) | no | 1 | 1 | n/a | — |
| halt: asked back, then the token `go on` | no | 2 | 1 (token only) | **None** | — |
| halt: asked back, then the token `stop` | yes (held) | 1 | **0** | None | — |

The controls show the row and the filing exist only on the road where the conductor returns. The rows of the dry walk use the stub's default verdict (`dry_stub.py::conductor_verdict` :130, `ask_person` "stub: offered every open move"). That is the asked-back road, which explains the finding's facts exactly: "answer for halt" is printed, there is no C2 row, the role does not resume, and the fingerprint is unchanged.

## Site 1: `kind:halt/free words` (S1/S2)

**Cause (product).** The road is: `driver_machine.py::Driver.take_answer` :3584 → `::_unread_halt_or_review` :3838-3845 → `driver_dispatch.py::register_words_to_conductor` :1971 → `driver_conductor.py::Driver.unread` :887-890 → `no_move` → the stub's `ask_person` → `options_person` raises `Person` (driver_conductor.py:696).
- `pending_words[dispatch] = words` sits AFTER the seam (:3845). The comment at :3842-3843 says "the words are filed AFTER the seam (this road's order)", so it is never reached.
- The audit row is written only at take_answer's end (:3614). That line is skipped as well.
- `_run_guarded`'s `except Person` (:2031) only calls `ask()`. The Refusal funnel at :2040 has `settle_unread_answer`, but nothing settles the answer on a Person.

The twin road already has this fixed. `take_question_answer`, invariant I5 of FV1-3 (driver_dispatch.py:1905-1910), reads: "everything a later process needs is on disk BEFORE the seam, which may raise a Person or end the process - the answer's audit row too ... so a rerun's re-ask carries FR-7's block". Two more holes are on the same road:
- (a) A free answer to the halt's SEAM question (kind `halt` + `offered`) is caught by the generic offered branch (:3554) → `take_seam_answer` → `unread`. `_file_words` files nothing for kind `halt` (:4122-4133), so the second answer never reaches the role either.
- (b) The `go on` token on the seam question closes the question and leaves `pending_words` empty. The role never gets the original words, although the halt promises "the same role continues in its own session with your words" (driver_dialog.py:114).

Breaks: AR-24 / FR-8 (the words do not reach the role), FR-7 (no row, so `already_answered`, driver_dialog.py:381-389, cannot tell a re-ask), AR-22.

**Check.** C2 (dry_exits.py:1392-1411) also fails when any conductor call follows the answer (`"unread_answer" in whys or (calls and not whys)`, :1409). D-0041 (the owner's word, 10.10.2026) requires that conductor call: "New words from the person that the code cannot read ALWAYS go to the conductor" (docs/DECISIONS_ARCHIVE.md:70; `Driver.unread` docstring :880). So C2 cannot pass for these words even after the product fix.

C3 (:1414-1421) cannot pass on the asked-back road either. `state_fingerprint` (:955-993) reads stages, gates, acceptance, `asked.kind/stage`, dispatches, rounds, forms and outputs. The seam question keeps the kind (`halt`, `_person_of` :437) and the stage. The words live in `pending_words` and `driver-answers.jsonl`, both outside the fingerprint. The stub's `halt` verdict is perpetual (finding, `dry_stub.py:409-415`), so a resumed role would also halt again with the same form bytes.

**Diagnosis: product AND check wrong.**

## Site 2: `s6.stand_confirm/free words` (asked at S5)

**Cause (product).** The road is: `driver_machine.py::_take_stand_answer` :3983-3991 → `Driver.unread(... block=STAND_NOT_CONFIRMED_BLOCK)` → `no_move` → `ask_person` → `Person`. The answer gets no row (the same skipped :3614). The design in the docstring is right:
- the code reads only a stand name or a token (FR-12);
- other words go to the conductor with the exact `waiver.py --words-file` door (FR-4: an informed pass needs the person's word; FR-48: the conductor settles it before asking);
- D-0041 requires that conductor call.

No words for a role are owed here (the stand question names no dispatch; `_file_words` :4138). So the only product defect is the missing row, the same root as at site 1.

**Check.** The same reasoning as site 1: the conductor call is by design (C2 n/a), and an asked-back answer moves nothing in the fingerprint (C3 n/a).

**Diagnosis: product wrong (the row only) AND check wrong.**

## Recommended builder cards

### Card P (product)

**owns:**
- `ai-packages/qa-factory/scripts/driver_conductor.py` (`Driver.unread`)
- `ai-packages/qa-factory/scripts/driver_machine.py` (`Driver._unread_halt_or_review`, `Driver.take_answer` offered-branch position, `Driver.take_seam_answer` stop branch, the halt `stop` branch)
- `ai-packages/qa-factory/scripts/driver_s0.py` (`ticket_ask_again`)
- `ai-packages/qa-factory/scripts/tests/test_no_move_seam_n2b_n15.py` (the table; the designer may name another seam file within budget)
- a `changelog.d/` fragment

**Behaviour:**
- P1. `Driver.unread`, before `no_move`: `self.answer_file(); self.record_answer_row("")`. It is a no-op when no answer is being taken or its row is already written (`record_answer_row` :239-242, once per answer).
  - Invariant: every unread answer is on record before a conductor call that may raise. This is the I5 rule lifted to the one entry used by all 26 `unread` call sites (AR-15).
  - `driver_s0.py::ticket_ask_again` :407-409 appends its own raw row before `unread`. It must switch to the same writer (`answer_file(); record_answer_row("")`), or P1 writes two rows (AR-14, one writer).
  - `driver_dispatch.py:1909` (I5) stays: it uses the same idempotent writer.
- P2. `_unread_halt_or_review`: `self.state["pending_words"][dispatch] = words; self.save_state()` BEFORE `register_words_to_conductor` (the I5 order of driver_dispatch.py:1905-1910). The "this road's order" clause is deleted. This is safe: the I6 guard (driver_machine.py:1465-1474) never resumes a role while a question about its dispatch is open. A `stop` on the seam question therefore holds, and a `go on` / `retry` closes the question and the role resumes with the ORIGINAL words. That fixes hole (b).
- P3. `take_answer`: an answer to a seam question of kind `halt` that is NOT one of its offered tokens takes the halt branch (:3584 → `_unread_halt_or_review`), not the generic offered branch. This is the `seam_gate_words` pattern (:3403-3404, :3554).
  - POSITION INVARIANT: every token of `asked.offered`, `stop` included, still reaches `take_seam_answer`.
  - This fixes hole (a).
- P4. A token read inside `take_answer` and then a `Person` raised before :3614 gets `self.record_answer_row(token)` before the raise. This is the `_delivery_token` pattern (:3866-3869).
  - Verified holes: `take_seam_answer` `stop_here` (:2395-2397; the probe row "then `stop`": 0 rows) and the halt `stop` branch (:3578-3583).
  - The builder checks the other `raise self.held_question(self.stop_held(` sites the same way: driver_dispatch.py:1881, :3453, :4060; driver_machine.py:2249; driver_s0.py:425; driver_stage_s7.py:503. Sites :3869 and :3936 are already right.

**Table** (one parameterised table, a row per case; the expected values come from the `record_answer_row` docstring "written ONCE per answer", the halt promise at driver_dialog.py:114, and I5/I6):
1. halt, free words, asked back: exactly 1 row (token `""`, `question_sha` of the halt question); `pending_words[dispatch] == words`.
2. stand, free words, asked back: exactly 1 row; no `pending_words` entry.
3. halt, asked back, then `go on`: after it, `pending_words[dispatch]` is still the original words; 2 rows (`""`, `go on`).
4. halt, asked back, then free words again: the second answer is filed for the role and has its own row.
5. a seam question answered `stop`: 1 row with token `stop`.
6. `ticket_changed` unread: exactly 1 row (no duplicate).
7. conductor `continue` (control): exactly 1 row (no second row at :3614).

N7/N7a (n2b :81-139) assert the words file, not the row, so these rows duplicate nothing (Q5e).

**AR / FR:** AR-14, AR-15, AR-17, AR-22, AR-24; FR-7, FR-8. Judgment: none (a write order and a writer; no reading of meaning).

### Card W (walker; land it after P, or on P's branch)

**owns:**
- `ai-packages/qa-factory/scripts/tests/dry_exits.py` (`CHECKS_JUDGED`, `JUDGE_CHECKS`, new `_check_c11`, the loader guard, the self-test cases, `alive`)
- `ai-packages/qa-factory/scripts/tests/dry_world.py` (facts)
- `scripts/tests/fixtures/stories/dry-1/exits/s0.json`, `.../exits/s6-s9.json`
- `scripts/tests/fixtures/driver-exits/known_red/s0.json`, `.../known_red/s6-s9.json`

**Behaviour:**
- W1. New check **C11, "unread words are on record and travel"**. PASS only if all of:
  - (a) a `driver-answers.jsonl` row with `question_sha == ask_sha`, token `""` and words equal to the row's answer words (stripped LF text, as `take_answer` keeps them);
  - (b) at least 1 conductor call in the answer's own turn not marked `chosen` (`conductor_calls - conductor_chosen`). This is the D-0041 obligation: the words reach the reader that can act (AR-24);
  - (c) when the first ask after the answer's own turn carries `offered`, its `words_file` holds the answer's bytes whole. With no `offered`, (c) is n/a.

  `dry_world.run_row` / `row_facts` gather the answer bytes and that file's bytes. The judge opens no file (AR-13). C11 is a data check: presence, count and bytes (AR-29). The loader refuses C11 on a row whose answer has a token (a token is C2-judged), the twin of the C2-n/a guard at :1123.
- W2. Every reachable `/free words` row whose answer goes to `Driver.unread` gets `"checks": ["C11"], "na": {"C2": "unread words go to the conductor by design: D-0041 (docs/DECISIONS_ARCHIVE.md:70), driver_conductor.py::Driver.unread", "C3": "the stub's conductor asks back: the seam question keeps kind and stage, and the words are in driver-answers / pending_words, outside state_fingerprint"}`. The rows:
  - s0: `kind:halt`;
  - s6-s9: `s6.stand_login`, `s6.stand_confirm`, `s6.stand_confirm.login`, `s6.gate_a_dry`, `s7.repair_limit`, `s7.open_work`, `closed.held`, `s8.report_match`, `s8.delivery_check`, `s8.delivery.{yes,after_checks,no}`.

  The three `s8.delivery.*` rows take the `reenter` road (driver_machine.py:3852-3863): no `unread`, and the delivery step is the conductor session. Their (b) holds only if that session runs in the answer's turn. If it does not, the row is red, never green (the safe direction), and the first run with an S7 snapshot settles it.

  `s1.review` and `kind:s1_review` free words keep C2/C3: `record_review` reads them by code, with no conductor.
- W3. The stub default stays `ask_person`. It is the harder road, and C11 judges it.
- W4. **Fork for the Lead (it touches the non-goal `alive` row).** After W2, `kind:halt` has only `free words` (fingerprint unchanged by design) and `empty`. `alive` (dry_exits.py:1631-1633) would then stay "alive only stop" red forever. Recommendation: a variant whose row declares C3 n/a is not counted as "moving". A declaration that the answer is not expected to move the state is no evidence that the subject is dead.
- W5. Remove the ledger entries only once P is in: `kind:halt/free words` (s0 pin 1 → 0) and `s6.stand_confirm/free words` (s6-s9 pin 14 → 13).
- Self-test cases (dry_exits self-test table):
  - row + call + file → ok;
  - no row → FAIL naming "no driver-answers row";
  - no unchosen call → FAIL;
  - file bytes differ → FAIL;
  - no `offered` → (c) n/a;
  - C11 with a token → loader refusal.

## Seam and class notes

- **Surface:** take_answer's answer record and words filing on the seam roads ("One question for every stop", docs/SIBLING_MAP.md:128).
- **Neighbouring classes walked:**
  - the token road (P4);
  - the second answer to a seam question (P3);
  - the raw second writer (`ticket_ask_again`, P1);
  - a Refusal (already settled, :2040);
  - empty input (refused at :3380, the `empty` rows pass).
- **A third free-words site:** yes. All 26 `Driver.unread` call sites share the missing row (P1 fixes them at the one entry). The 10 other s6-s9 free-words rows will go red the same way once FV3-21 lets the main pass make S6+ snapshots. Today they are not run (dry_world.py:1012).
- **Q4:** fixed in P and W; nothing leaves the round.
- **Q6:** P1 reuses `record_answer_row` (driver_conductor.py:235) and removes the raw second writer (driver_s0.py:407). C11 reuses the facts `answer_records`, `conductor_calls` and `asks`, and adds no second reader.
- **Q12:** none found. It is one check for every conductor-routed free answer, with no exclusion per kind, language or project. I grepped `free words` rows across all exits files.
- **VARIETY:** project-agnostic. No project value is read; on an unknown, nothing defaults.

## Spot-checks

- The report's "`_take_stand_answer` :3959, `unread` + `return False` :3983-3991" is confirmed by Read.
- The finding's "no answer row, no resume, conductor ask_person" is reproduced (table above).
- My negative "no test asserts a missing row" was checked with a grep for `driver-answers.jsonl").is_file()|exists()` over tests: 0 hits. The positive control, the same tree with `driver-answers.jsonl`, gave 10 files.
- The canon claims (seed reaches the ask) were not re-run: they need a canon run, which is not mine (rule 21).

## Trail

**Read:**
- the finding file;
- the s6-s9 report §Round 3;
- driver_machine.py :1455-1560, :1855-1894, :1975-2054, :2349-2498, :3375-3620, :3828-3875, :3940-4020, :4106-4152;
- driver_conductor.py :220-262, :434-455, :617-826, :876-973;
- driver_dispatch.py :1890-2049, :3436-3450, :4040-4060;
- driver_s0.py :398-436, :845-856;
- driver_dialog.py :270-360;
- driver_runner.py :282-292;
- dry_exits.py :50-74, :913-993, :1370-1640;
- dry_world.py :1125-1150, :1290-1374;
- dry_stub.py :90-134;
- known_red/s0.json, the worker-tree known_red/s6-s9.json;
- the exits rows of s0/gates/s1-s4/s6-s9;
- DECISIONS_ARCHIVE.md:69-70;
- SIBLING_MAP.md:126-129;
- no_move_seam_common.py; test_no_move_seam_n2b_n15.py :60-139.

**Rerun:** `python -B - <<EOF` (the probe drove `take_answer` through `no_move_seam_common.logged_rig`, with stdout redirected and only the result lines printed). Verbatim:

```
[halt S1, ask back] raised=True kind=halt offered=['retry', 'go on', 'stop'] words_file='state/words/driver-answer-1794941967470.txt'; calls=1; rows=0; pending_words=None
[halt S1, ask back] seam words_file bytes == answer: True
[halt S1, ask back] turn2 raised=True; rows=0; pending_words=None
[halt S1, continue (control)] raised=False; calls=1; rows=1; pending_words='go on without it'
[stand S5, ask back] raised=True kind=environment offered=['retry', 'go on', 'stop'] words_file='state/words/driver-answer-1794941977468.txt'; calls=1; rows=0; pending_words=None
[stand S5, ask back] seam words_file bytes == answer: True
[stand S5, ask back] turn2 raised=True; rows=0; pending_words=None
[stand S5, continue (control)] raised=False; calls=1; rows=1; pending_words=None
[halt seam then go on] raised=False; calls=2; rows=[('go on', 'go on')]; pending_words=None; asked=None
[halt seam then stop] raised=True; calls=1; rows=[]; pending_words=None; asked='halt'
```

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "One root: a Person raised by the seam inside take_answer skips the answer row (driver_machine.py:3614) and, at the halt, the words filing (:3845). P1 fixes all 26 Driver.unread call sites at the one entry (driver_conductor.py:876). The raw second writer driver_s0.py:407 is converted. Hole (a), a free answer to the halt's seam question (P3), and hole (b), go on without the original words (P2), are the same artifact. The token road (P4) was verified at :2397 and :3583; 6 more stop_held sites are listed for the builder. Walk side: the 12 conductor-routed free-words rows (s0 kind:halt, s6-s9 x12) take the new C11 with C2/C3 n/a; alive needs the Lead's fork W4. Axis: SIBLING_MAP.md:128 One question for every stop.",
  "fixes": [
    "P1 driver_conductor.py::Driver.unread: answer_file() + record_answer_row('') before no_move; driver_s0.py::ticket_ask_again:407 switched to record_answer_row (no double row)",
    "P2 driver_machine.py::_unread_halt_or_review:3838-3845: pending_words[dispatch]=words + save_state BEFORE register_words_to_conductor (the I5 order, driver_dispatch.py:1905-1910); the I6 guard :1465 keeps it safe",
    "P3 driver_machine.py::take_answer :3554: a non-token answer to a seam question of kind halt takes the halt branch (:3584), the seam_gate_words pattern; tokens unchanged",
    "P4 driver_machine.py:2395-2397 and :3578-3583: record_answer_row(token) before raise held_question; check driver_dispatch.py:1881,:3453,:4060, driver_machine.py:2249, driver_s0.py:425, driver_stage_s7.py:503",
    "P table rows in test_no_move_seam_n2b_n15.py: halt and stand asked back -> 1 row; halt pending_words==words; go on keeps the original words; second free answer filed; stop -> row token stop; ticket_changed 1 row; continue control 1 row",
    "W1 dry_exits.py: new check C11 (row with ask_sha and token '' and the words; >=1 unchosen conductor call in the answer turn; the seam ask's words_file holds the answer bytes when offered); facts from dry_world.py; loader refuses C11 with a token",
    "W2 exits rows s0 kind:halt/free words and the 12 s6-s9 free-words rows: checks [C11], na C2 (D-0041) and C3 (asked back, outside state_fingerprint)",
    "W4 Lead fork: alive (dry_exits.py:1631) should not count a variant whose row declares C3 n/a as moving",
    "W5 ledgers: drop kind:halt/free words (s0 pin 1->0) and s6.stand_confirm/free words (s6-s9 pin 14->13) once P is in"
  ],
  "trail": {
    "read": [
      "plans/piles/live-run-fvf/findings/20261117-p1b-s0-halt-svobodnye-slova-ne-dohodyat.md",
      ".claude/worktrees/agent-a2002f57c73d7bdae/docs/tasks/specs/reports/20261117-p1b-n4-s6-s9-report.md",
      "ai-packages/qa-factory/scripts/driver_machine.py",
      "ai-packages/qa-factory/scripts/driver_conductor.py",
      "ai-packages/qa-factory/scripts/driver_dispatch.py",
      "ai-packages/qa-factory/scripts/driver_s0.py",
      "ai-packages/qa-factory/scripts/driver_dialog.py",
      "ai-packages/qa-factory/scripts/driver_runner.py",
      "ai-packages/qa-factory/scripts/tests/dry_exits.py",
      "ai-packages/qa-factory/scripts/tests/dry_world.py",
      "ai-packages/qa-factory/scripts/tests/dry_stub.py",
      "ai-packages/qa-factory/scripts/tests/no_move_seam_common.py",
      "ai-packages/qa-factory/scripts/tests/test_no_move_seam_n2b_n15.py",
      "ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/known_red/s0.json",
      "ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/exits/*.json",
      "docs/DECISIONS_ARCHIVE.md:69-70",
      "docs/SIBLING_MAP.md:126-129"
    ],
    "reruns": [
      {
        "command": "python -B - (in-process probe: take_answer through no_move_seam_common.logged_rig, conductor stub ask_person vs continue)",
        "result": "halt ask back: raised, calls=1, rows=0, pending_words=None; control continue: rows=1, pending_words set; stand ask back: rows=0; control: rows=1; halt seam then go on: pending_words=None; then stop: rows=[]"
      }
    ]
  }
}
```
