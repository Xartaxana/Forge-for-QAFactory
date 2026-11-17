# t-1060 — narrow plan re-review: gate-ask judge card r2, §6 post-answer turns (fix round of t-1054)

Card: `docs/tasks/specs/20261117-p1b-gate-ask-judge-card-r2.md` (read whole). Previous verdict: `docs/tasks/specs/reviews/t-1054-p1b-gate-ask-judge-plan.md` (read whole).
Tree: `C:/QAFactory/forge-repo/.claude/worktrees/agent-a4aebd95c3ca7d59c` at `11494798` (`git log --oneline -1`). Prefixes as in the card (`T/`, `S/`, `R/`).
Scope: §6, §3 only as far as §6 leans on it, fork F-4. Everything else is t-1054's and the Lead's table "Fix round t-1057".

## Verdict

**Dispatchable after edits** (no finding blocks dispatch; five "fix before dispatch" text edits, G1-G5, plus three notes).
F-6 (a) is the right road. The designer's B1 residue trace holds by the walker's code. But §6 as written has two gaps that matter. It disarms the `turns` always-check without putting anything in its place for a row that does not list C3 (G1). And it does not say where in the loop the stop goes (G2). Its "same ask" edges are unstated (G3). The DoD control does not catch a stop placed before the turn's facts are collected (G4). And DoD (7) contradicts §6's own prediction that merged rows may flip (G5).
F-4: the designer is right. The JSON line of t-1054 that asks to queue F-4 is an error in that verdict.
Whether to accept, and whether to apply these edits, is the Lead's decision (rule 6). This review is input to it.

## Findings

### G1 — §6 removes the `turns` backstop and puts nothing in its place (fix before dispatch)
The code: the loop `T/dry_world.py:1263-1286` sets `exhausted` only through `for ... else` (`:1285-1286`), that is, when 4 turns each wrote a new question, `fp_after == fp_ask` every time, and there was no loop. `_judge_always` fails `turns` on it (`T/dry_exits.py:1397-1398`) for EVERY row, whatever its listed checks. So today `turns` is the one always-check that says "the answer moved nothing". It acts for rows that do not list C3.
§6: "The `exhausted` flag is not set when the turns end by this rule." After the change, a row whose answer leads to a different question with the state unchanged ends at turn 1, gets no `exhausted`, and is judged only by its listed checks. The §6 error-direction paragraph says "fewer turns can only show an unchanged fingerprint ... (C3 false red)". That is true for a row that lists C3. It is false for a row that does not list C3 and declares no n/a. The loader allows such a row: only an EMPTY `checks` is refused (`T/dry_exits.py:1117-1118`). The C3 n/a guard of §4 acts on a DECLARATION, not on an omission. So "a token whose data expects the state to move is always C3-judged" does not hold for a row that simply leaves C3 out.
Concrete false-green input (future s5/s6-s9 key rows, which inherit §6 "automatically", §12 non-goals): a row with `checks: ["C2"]`, a token whose price row says `stages_again`. The product answers by raising a DIFFERENT question and records nothing (a dead end dressed as a question). §6 stops at turn 1 and C2 passes, so the row is PASS. Today the walker keeps re-sending, the asks alternate, and the row ends `exhausted` -> `turns` FAIL.
No walked row today is in this shape (key 2), so this is a class gap, not a flip of an existing row.
Exact edit, §6, replace the sentence "The `exhausted` flag is not set when the turns end by this rule." with:
> "When the turns end by this rule, `run_exit_row` sets `facts["ended_at"] = {"turn": <n>, "kind": <kind>, "stage": <stage>}` instead of `exhausted`. `_judge_always` FAILs `turns` with `<row id>: the answer moved nothing and the next ask is another question (<kind> at <stage>, turn <n>); C3 is neither listed nor declared n/a` when ALL of these hold: `ended_at` is set, `fp_after == fp_ask`, and the row neither lists C3 nor declares C3 n/a. A listed C3 judges the same fingerprint itself. A C3 n/a that passed its guard (§4: no token, or `factory: nothing`) is data saying the state does not move. Invariant: **a stop at a different ask never counts as the state moved**. The outcome detail of a PASS or NOTE whose turns ended this way prints `ended at <kind> at <stage> after turn <n>`."
Also edit the error-direction sentence to: "fewer turns can only show an unchanged fingerprint where a later re-sent turn would have changed it (C3 false red, allowed); the `turns` always-check stays armed for a row that does not judge C3 (above)."
Add to §8 the judge-table row (11): "`ended_at` set, `fp_after == fp_ask`, checks `["C2"]`, no `na` -> FAIL `turns ... C3 is neither listed nor declared n/a`; the same facts with `na: {"C3": ...}` on a `factory: nothing` token -> not FAIL".
Gate rows under this edit: `retry` (C3 n/a, guard holds) and `free words` (C3 n/a, no token) stay green. `approve` and `rework` list C3. `stop` (held, same ask, so no §6 stop) is unaffected.

### G2 — POSITIONAL: §6 does not say where the stop sits in the loop (fix before dispatch)
CLAUDE.md rule 11 (ii) requires this. The loop body, in order (`T/dry_world.py:1264-1284`): run; `post_turns`; outputs; cap; fingerprint (`fp_after`); questions; `now`; whys appended (`:1274-1275`); the no-new-row break (`:1276-1277`); `asked_count`; asks appended (`:1279`); rehearse (`:1280-1281`, C6); `loop_problem` (`:1282`); the fp/loop break (`:1283-1284`). If a builder puts the §6 stop right after `:1277`, the stopped turn loses several facts:
- its asks entry is not appended;
- its gate rehearsal is not run. For `retry` the stopped ask is the re-shown plain `gate_A`, so C6 silently checks one ask fewer;
- its loop check is not run.
Exact edit, §6, add after the rule: "Position: the test sits in the same `if` as the existing loop/fingerprint break (`T/dry_world.py:1283`), after `fp_after`, the whys of the turn, the asks entry, `rehearse` and `loop_problem` are taken: `if facts["loop"] or fp_after != facts["fp_ask"] or not same_ask(asks[0]["ask"], asks[-1]["ask"]): break` (with `ended_at` set only by the third clause, and only when the first two are false). Invariant: the turn that ends the loop is collected whole. C2 reads its whys, C6 rehearses its ask when it is a gate, C3 reads its fingerprint. The comparison is with the JUDGED ask (`asks[0]`), never with the previous ask."

### G3 — "the same ask" at the §6 site: three edges unstated (fix before dispatch)
§6 uses `dry_exits.same_ask` (`T/dry_exits.py:996-1009`). That identity is (price key or kind, stage, dispatch with its number replaced, normalised SET of offered tokens). It does not compare the text, `question_sha` or the held lead.
- (a) **Equal identity, different question.** Example: a second seam question at the same gate for another reason, with the same option set; or a re-shown plain gate after the answer changed something that is not in the fingerprint. §6 calls it "the same" and re-sends the answer. So the card's absolute invariant "the walker's answer is only ever sent to the ask it was written for" overstates. It holds up to the C5 identity. This is deliberate and right: a held re-raise (`held_question`, `S/driver_dialog.py:600-629`) keeps kind, stage, dispatch and offered (`:620-621`) but changes the text (`lead`). Comparing text would end the turns on every held re-raise, and C5 would never see a product loop of "answer not read" re-raises. Edit the §6 invariant to: "the walker's answer is only re-sent to an ask with the same C5 identity as the judged ask (`same_ask`: key or kind, stage, dispatch without its number, offered set; text not compared, so a held re-raise is the same ask). Residual direction: a different question with an equal identity still gets the re-send. That is the C5 identity's own known merge (its docstring, `T/dry_exits.py:1005-1008`), not a new road."
- (b) **A free-words ask (no `offered`).** Two plain asks of the same kind, stage and dispatch are the same (an empty frozenset on both sides). State: "an ask with no offered tokens is the same as another with none at the same kind, stage and dispatch (a re-shown plain gate is the same ask)."
- (c) **No pending ask after a turn that wrote a row.** A deferred question writes a row and is not pending (`S/driver_dialog.py:429-433`). A turn can also clear `asked`. §3 item 3 now makes `:1279` take "the identified row of the then-pending ask", and there is none. The card is silent on this. State: "a turn that wrote a question row and left no pending ask ENDS the turns (it is not the judged ask). No asks entry is added. `ended_at` is set with kind `none`, and G1's `turns` rule applies."

### G4 — the §8 control does not catch every too-wide §6 (fix before dispatch)
The §8 case "a turn that raises a different ask ends the turns, `exhausted` unset; three identical asks still set `loop`" covers two failures:
- **stopping on the same ask** (too wide): the loop case fails. Good.
- **stopping before the answer is consumed**, or the G2 position: a stop placed before the asks/rehearse/fp collection still ends the turns with `exhausted` unset, so the case passes. Not caught.

Exact edit, §8 `run_exit_row` post-answer end, replace the case with: "(i) a turn whose new pending ask differs from the judged ask, with the fingerprint unchanged: `drive_fn` called exactly once with `--answer`, `post_turns == 1`, `fp_after` equals the fingerprint the fake turn left, `ended_at` set, `exhausted` unset, and with C6 listed and the new ask a gate kind, `gates` holds TWO entries (judged + stopped); (ii) the same with the new ask equal to the judged ask (same kind, stage, offered, other text): the turns go on (turn 2 runs); (iii) three identical asks set `loop`, `ended_at` unset; (iv) a row that wrote a question row and left no pending ask ends with `ended_at.kind == "none"`." Plus the judge row (11) of G1.
Feasibility pointer (no existing case drives `run_exit_row`; it starts with `from_snapshot`, `T/dry_world.py:364-376`): "build the world with the selftest's `fake_world` / `put_state` (`T/dry_exits.py:2524-2535`) and a snapshot dir `world.snaps/<row id>/<start>/` holding `.dry-snapshot.json` with `label` = `dry_world.RUN_LABEL`; the fake `drive_fn` rewrites `driver-state.json` / `driver-questions.jsonl` as `put_state` does."

### G5 — DoD (7) says AFTER == BEFORE, but §6 predicts flips (fix before dispatch)
F-6 text: "(a) ... may change outcomes of merged rows that today pass only by re-sending their answer to a different question — DoD (7) shows any change". DoD (7): "every row's outcome AFTER equals its outcome BEFORE; any change is reported with both lines, not labelled". The pair is a conflict the card does not resolve (rule 11: conflicting requirements). A builder seeing `s1.review/free words` flip from PASS to FAIL C3 cannot tell whether it has to fix its code or report the flip and stop.
Exact edit, DoD (7), append: "A flip whose AFTER line carries `ended at <kind> at <stage> after turn <n>` (G1) is §6 exposing a re-send green: it does not fail this node. The builder reports it with both lines and does not change the row, the stub or §6 for it; the Lead labels. A flip WITHOUT that detail is a defect of this change and is fixed in this node." The same rule goes in §9 for `gate_A/rework`: a C3 red with an `ended at` detail is reported with that line, and is not by itself grounds for `live_only`.

### N1 — §6 "C5 is unaffected" is slightly inaccurate (note)
Today, the sequence judged J, then B, B, B (the walker re-sending J's answer to B) sets `loop` on B,B,B (`T/dry_world.py:798-807`, `:1282`). Under §6 the turns end at the first B. So C5 changes for that sequence. It was a walker artefact (an answer re-sent to a question it was not written for), so the change is right. Edit: "C5 is unaffected for the judged ask: three identical asks of the JUDGED ask still arise and are still caught; a loop of a DIFFERENT ask that only the re-send produced is no longer manufactured."

### N2 — key 1 rests in part on product reading (note)
The walker half of the residue trace is code-certain (below). The product half has three facts: `retry` re-raises the plain gate in turn 1; in turn 2 the plain gate sends `retry` words to the conductor and to the fallback seam within one boundary; and neither the conductor call nor the `defect_found` changes the fingerprint. These are by reading:
- `log_append defect_found`, `S/driver_runner.py:1317-1327`, goes to the event log. The fingerprint parts are pipeline stages, gates and acceptance; controller dispatches; rounds; forms; outputs (`T/dry_exits.py:941-986`).
- I did not verify that the stub conductor call adds no controller dispatch.

If the fingerprint did change in turn 2, today's `retry` would break as "changed" after a re-send to the plain gate: a false green on C3, not a `turns` red. §6 removes that road as well, so the decision for F-6 (a) does not depend on which one happens.

### N3 — t-1054's JSON line on F-4 was wrong (note, key 5)
See key 5. No card edit; the Lead may note the correction against t-1054.

## Answers to the acceptance keys

1. **Yes, the B1 residue trace is correct** (walker code, every step read in the tree). The seam ask and the plain gate ask share kind `gate_A` and stage `S4`:
   - the plain gate is raised with `Person("gate_A", ..., "S4")` and no dispatch (`S/driver_gates.py:322`);
   - the fallback seam is built from `state.kind` (`S/driver_conductor.py:410-427`, `:504-527`);
   - the fingerprint holds only `asked.kind/stage` of the driver state (`T/dry_exits.py:958`). `retry` records nothing ("nothing is recorded; the gate is shown again", `S/driver_machine.py:2392-2394`).

   So `fp_after == fp_ask` on every turn. The asks alternate seam (offered set) / plain (offered `[]`). `_ask_identity` puts the offered frozenset into the identity (`T/dry_exits.py:996-1002`), so no two consecutive asks are the same and `loop_problem` (`T/dry_world.py:802-806`) never fires. Each of the 4 turns (`POST_TURNS`, `:1076`) writes a row, so the `:1276` break is never taken. The `for ... else` sets `exhausted` (`:1285-1286`), and `turns` FAILs (`T/dry_exits.py:1397-1398`). The C2 cut alone leaves this red. Caveat: N2. If the 4 turns with conductor calls run past 240 s, the red is `over the cap` instead. It is still red.
2. **Rows whose post-answer turns could meet a new different ask, and what §6 does to them.** Walked rows listed by script over `fixtures/stories/dry-1/exits/*.json` (tree and main checkout; the main checkout holds only `s0.json` and `s1-s4.json`, and no `s5`/`s6-s9` exit-row file exists in either; `--check` lists those groups from the census only):
   - `s0`: `kind:halt/free words` `[C2,C3]`, `kind:halt/empty` `[empty]`;
   - `s1-s4`: `s1.review/agree`, `s1.review/flip`, `s1.review/free words`, `kind:s1_review/free words` (all `[C2,C3]`), `s1.review/empty`;
   - `gates`: the twelve rows (the `gate_B` ones are NOTE, start S8 absent).

   What §6 does:
   - **empty rows:** the answer is refused, no new row is written, and the existing `:1276` break fires before §6 is reached. Unchanged.
   - **Every other walked non-gate row lists C3.** At a §6 stop, `fp_after` is that turn's fingerprint. A row whose fingerprint never moved was `exhausted` + C3 FAIL; it becomes C3 FAIL alone, so it stays red. A row green today stays green when its state moved before any different ask appeared. It FLIPS to red only when its green came from a re-send to a different ask (fingerprint unchanged at the first different ask). Which of the five, if any, take that road cannot be said by reading the stub's conductor verdicts: it is what DoD (7) measures (G5 says what the builder does with it).
   - **Gate rows:**
     - `approve`: the gate is recorded in turn 1, so the fingerprint changes and §6 is not reached;
     - `retry`: ends at the plain gate in turn 1, C3 n/a, and `turns` no longer fails. The intended fix;
     - `stop`: `held_question` re-raises the SAME ask (`S/driver_dialog.py:620-621`), so the turns go on and `loop` ends them at turn 2, as today;
     - `free words`: if the fallback seam carries the same offered set, the same ask means loop as today; if not, a §6 stop with C3 n/a and no token, which passes under G1;
     - `rework`: C3 listed, so a §6 stop can only add a C3 false red (G5's §9 sentence);
     - `empty`: unchanged.
   - **Selftest:** no existing case drives `run_exit_row` (grep `run_exit_row|exhausted` over `T/*.py`). The EW24 judge row (`T/dry_exits.py:2606`) is unchanged.

   **Can §6 turn a real red into a pass?**
   - A product re-ask of the SAME question (loop): no, §6 never stops on the same ask.
   - A dead end with no new question: no, the existing break applies.
   - Driver exit and cap: no, unchanged.
   - The product raising a DIFFERENT question with nothing recorded: on today's rows no (all list C3). For a row that omits C3 without a declaration, YES. This is G1, and the fix restores the invariant "a stop at a different ask never counts as the state moved".
3. **"The same ask" at the §6 site** is well defined as code (`same_ask`) but under-stated in the card. The three edges and their texts are in G3:
   - offered sets equal, text different: same, re-sent; deliberate for held re-raises; residual stated;
   - an ask with no offered tokens: same when kind, stage and dispatch agree;
   - no pending ask after a new row: unstated in the card.

   A "re-raised question" (held) is the same ask by `S/driver_dialog.py:620-621`. That is required for C5.
4. **Partly.** "Three identical asks still set `loop`" FAILS for a §6 that stops on the same ask. Nothing fails for a stop placed before the turn's facts are collected, and nothing pins "a stop is not the state moved". G4 adds controls (i)-(iv) and the judge row of G1.
5. **F-4: the designer is right, and t-1054's JSON `fixes` line ("F-5 (b) and F-4 residuals named as finding files") contradicts t-1054's own Forks table.** r1's F-4 (b) (`docs/tasks/specs/20261117-p1b-gate-ask-judge-card.md:228-231`) is "at the PLAIN ask, a new check: the answer raised a question whose offered answers are all rows of the key". r2 already judges exactly that on every gate row:
   - the `say` seed is free words at the plain ask, and it is reached only if a new question at the same stage carries a non-empty `offered` (§5 step 3);
   - K15 (iii) on the seeded ask then requires every offered token to be a `gate_A`/`gate_B` data row (§4).

   So (b) would be the same observation under a second check id. No residual is lost. The JSON line was a defect of that verdict; the Forks table's reasoning stands.
6. **Feasible after G2 and G4.** The change is one extra clause in the existing break at `T/dry_world.py:1283`, one fact (`ended_at`), one `_judge_always` branch (G1) and one fake-world case. With the position, the comparison target (`asks[0]`), the edges (G3) and the fake-world route (G4) written in, a builder invents nothing. As it stands, two choices are left to the builder: where the stop sits, and how to fake a snapshot for `run_exit_row`.

## Standing questions (narrow plan gate)
- **One action, one road (P31):** §6 is one rule for every walked row, with no exclusion of a group or variant. G1 keeps it one rule: the `turns` condition reads the row's own C3 declaration, not a list of variants. No finding.
- **Duplication and consistency:** §6 reuses `same_ask` (the C5 identity) and does not write a second identity. That is the right reuse, with its edges stated (G3). Searched `exhausted|POST_TURNS|run_exit_row|same_ask` in `T/*.py` (grep; positive control: the known sites `dry_world.py:1076`, `:1286`, `dry_exits.py:1004`, `:1397` were found). No second turn loop.
- **Code quality:** with G1-G2 the change is small and local. Without G2 the order inside the loop is a guess.
- **Tests:** G4 adds cases to an existing selftest table and no new file (TESTING.md: a table of cases for a pure branch). Volume is not measured at plan stage.

## What I did not check
- I ran no row. The post-answer ask sequences of the five merged C2/C3 rows are not known by reading (DoD (7) measures them).
- Whether the stub conductor call adds a controller dispatch (N2).
- §§1-5 and 7-16 beyond what §6 leans on (t-1054's scope, the Lead's table).

## Trail
Read in the tree:
- the r2 card, whole; the t-1054 verdict, whole; the r1 card, lines 155-163 and 226-236 (F-4);
- `T/dry_world.py` 364-376, 798-814, 1070-1080, 1125-1160, 1205-1300;
- `T/dry_exits.py` 938-1015, 1295-1440, 2524-2584, grep `exhausted|run_exit_row|POST_TURNS`;
- `S/driver_machine.py` 2380-2452, 3376-3410, 3590-3612;
- `S/driver_dialog.py` 395-435, 600-630;
- `S/driver_gates.py` 312-325;
- `S/driver_conductor.py` 405-530;
- `S/driver_runner.py` 1317-1328;
- the gates report, grep `retry|turns|exhausted|post-answer`;
- row lists of `fixtures/stories/dry-1/exits/*.json` in the tree and the main checkout, by script (`rows.py` in the scratchpad: id, reach, seed, start, token, checks).

Re-run: `( cd <tree>/ai-packages/qa-factory && python -B scripts/tests/dry_exits.py --check )` printed `dry_exits --check: 0 discrepancies` (groups `gates, hooks, s0, s1-s4, s5, s6-s9`).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "G1 section 6: a turn end at a different ask sets facts ended_at instead of exhausted; _judge_always FAILs turns when ended_at is set, fp_after equals fp_ask and the row neither lists C3 nor declares C3 n/a; invariant: a stop at a different ask never counts as the state moved; outcome detail prints ended at kind at stage after turn n; section 8 judge row 11",
    "G2 POSITIONAL: the stop is a third clause of the existing loop/fingerprint break at dry_world.py:1283, after fp_after, whys, the asks entry, rehearse and loop_problem; compared with asks[0] (the judged ask), never the previous ask",
    "G3 state the same_ask edges at the section 6 site: identity ignores text (held re-raise is the same ask, needed for C5; residual stated); no-offered asks are the same at equal kind, stage, dispatch; a turn that wrote a row and left no pending ask ends the turns with ended_at kind none",
    "G4 section 8 run_exit_row cases: drive_fn called once, post_turns 1, fp_after from that turn, gates holds the stopped gate ask when C6 listed; same-identity other-text ask continues; three identical asks set loop; no pending ask ends with kind none; fake-world route fake_world/put_state plus a snapshot dir with .dry-snapshot.json label RUN_LABEL",
    "G5 DoD 7 and section 9: a flip whose AFTER line carries the ended at detail is reported, not fixed or labelled by the builder, and does not fail the node; a flip without it is a defect of this change; a rework C3 red with that detail is not by itself grounds for live_only",
    "N1 reword C5 unaffected: holds for the judged ask; a loop of a different ask that only the re-send produced is no longer manufactured"
  ],
  "class_completeness": "Section 6 is one rule over every walked row (axis 34). Walked rows today: s0 kind:halt/free words and empty, s1-s4 s1.review/agree, flip, free words, empty, kind:s1_review/free words, the twelve gate rows; no s5 or s6-s9 exit-row files exist in the tree or main. Every non-empty walked non-gate row lists C3, so no existing red can turn green; possible green-to-red flips are measured by DoD 7. The class gap is rows that omit C3 without an n/a declaration (future s5/s6-s9 key rows): G1 closes it at the one judge. F-4 (b) duplicates the say seed plus K15 (iii) and is correctly not queued; the t-1054 JSON line asking to queue it was an error.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-p1b-gate-ask-judge-card-r2.md whole",
      "docs/tasks/specs/reviews/t-1054-p1b-gate-ask-judge-plan.md whole",
      "docs/tasks/specs/20261117-p1b-gate-ask-judge-card.md 155-163 226-236",
      "tree scripts/tests/dry_world.py 364-376 798-814 1070-1080 1125-1160 1205-1300",
      "tree scripts/tests/dry_exits.py 938-1015 1295-1440 2524-2584",
      "tree scripts/driver_machine.py 2380-2452 3376-3410 3590-3612",
      "tree scripts/driver_dialog.py 395-435 600-630",
      "tree scripts/driver_gates.py 312-325",
      "tree scripts/driver_conductor.py 405-530",
      "tree scripts/driver_runner.py 1317-1328",
      "tree docs/tasks/specs/reports/20261117-p1b-n4-gates-report.md (grep)",
      "fixtures/stories/dry-1/exits/*.json row lists, tree and main checkout (script)"
    ],
    "reruns": [
      {
        "command": "( cd <tree>/ai-packages/qa-factory && python -B scripts/tests/dry_exits.py --check )",
        "result": "dry_exits --check: 0 discrepancies; NUMBER groups: gates, hooks, s0, s1-s4, s5, s6-s9"
      }
    ]
  }
}
```
