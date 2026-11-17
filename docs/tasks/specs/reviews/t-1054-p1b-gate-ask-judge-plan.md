# t-1054 — critic on plan: P1-b gate ask judge card (t-1045)

Plan under review: `docs/tasks/specs/20261117-p1b-gate-ask-judge-card.md` (283 lines, read whole).
Tree: `C:/QAFactory/forge-repo/.claude/worktrees/agent-a4aebd95c3ca7d59c` at `11494798` (checked: `git log --oneline -1`).
Prefixes as in the card: `T/` = `<tree>/ai-packages/qa-factory/scripts/tests/`, `S/` = `<tree>/ai-packages/qa-factory/scripts/`, `R/` = `<tree>/ai-packages/qa-factory/references/`.

## Verdict

**NEEDS WORK. Dispatchable after the edits B1-B6.** Option (b) is right and the ask-identity rule is sound in its core.
Six edits must go into the card before a builder gets it. Without them the builder hits a red the card designs in
(B1), a row that contradicts itself (B2), a K15 that reads the conductor prompt's record as the person's question (B3),
no witness that the merged groups stay green (B4), an n/a with no guard (B5), and a DoD line that goes stale when
N2h-b2 merges (B6). Items F1-F10 are fixes for the same round.
Whether to accept the plan, and the fork decisions, belong to the Lead (rule 6). This review is input to that decision.

## Forks

| fork | answer | reason |
|---|---|---|
| F-1 | **agree (b)**, if B1, B3, B4 are edited in | The product's packet tells the person exactly this road: "To change something first, say what in your own words instead of `approve`: nothing is approved, and you get the choices with what each costs" (`S/driver_gates.py:136-141`). `rework/approve/retry/stop` exist only at the seam question. (a) is a tautology (see K15 (ii) below). (c) walks nothing. |
| F-2 | **agree (a)**, with edit F1 | The heading `## The person's choice` is text the DRIVER writes (`S/driver_conductor.py:687`). The stub only records whether it is there, so the flag observes the driver and not the double. Two defects in how the card says it: (1) §6 says "a prompt whose LAST section heading is ...", but in the real prompt the heading sits inside `## The refusal`, with `## \`story_step.py where\``, `## The person's words` and `## Files ...` after it (`S/driver_conductor.py:320-324`). So "last heading" never matches, and the rule must be "a line equal to the heading, anywhere". (2) The refusal section is cut at 6000 characters (`refusal.strip()[:6000]`, `:320`) and the choice paragraph is appended LAST (`:687`). At a gate the chosen call's `text` is the details file (`S/driver_machine.py:2448`), and that file holds the generic gate prompt with the gate packet (`qtext[:8000]`, `S/driver_conductor.py:880-882`). So the heading can be cut off. Estimate, not verified: the packet length was not measured. |
| F-3 | **agree (a)**, with edit B5 | The declaration sits next to the row it qualifies. But only K15 and C2 get an observation guard; C3 n/a gets none (B5). |
| F-4 | **agree (a)** | The plain-ask words road IS judged. Every gate row's `say` seed is "free words at the plain gate", and it is reached only if a question with `offered` follows. K15 (iii) on the seeded ask then compares that offered set with the `gate_A` rows. So (b) would judge the same thing a second time. The PASS line of `gate_A/free words` must still print its two n/a (as §3 says). |
| F-5 | **agree (a) for this card, with B5's guard** | The card does not say where (b) goes ("as a finding", §9) with no pile or owner. PROJECT.md «Командная работа» п.9 and critic rule 19: a residual is written as a finding file plus a row in an untaken batch, with an executor. Edit: name the pile (the walker pile) and the finding file in §9 F-5 and in the handoff. |

## Findings

Severity: **blocks dispatch** = edit the card before sending; **fix in round** = same card, same round; **note**.

### B1 — `gate_A/retry`: C2 turns red because the walker re-sends the answer (blocks dispatch)
Trace (every step read):
1. `retry` at the seam: `take_seam_answer` -> move `person_does` -> "nothing is recorded; the gate is shown again" (`S/driver_machine.py:2392-2394`). The next boundary raises the PLAIN gate again (`S/driver_gates.py:322`) and writes a new question row.
2. The fingerprint has `asked.kind/stage` only (`T/dry_exits.py:957`). Plain and seam are both `(gate_A, S4)`, and retry records nothing, so `fp_after == fp_ask`. One ask so far, so no loop. The walker therefore runs turn 2 (`T/dry_world.py:1281-1283`) and RE-SENDS `retry\n`, this time to the PLAIN gate.
3. At the plain gate `retry` is words: `asked.offered` is absent, `record_by_code` does not approve, and `else: _unread_kept_gate` sends it to the conductor (`S/driver_machine.py:3606-3607`). The new pending ask is kind `gate_A`, not `conductor`, so `whys` stays empty (`T/dry_world.py:1274-1275`). `conductor_calls` counts every stub conductor line after `mid` (`T/dry_world.py:1144`).
4. `_check_c2`: `calls and not whys` gives "a conductor call followed the answer and its why is not on record" (`T/dry_exits.py:1326-1327`).

Result: the DoD's "`gate_A/retry` PASS" cannot happen. Edge 10 names the re-send only for `free words`, and only against C5.
Exact edit (§3 C2 row, §5 edge 10, §6): "C2's 'no conductor call after the answer' counts the conductor calls up to the FIRST new question row after the answer (the answer's own turn). Invariant: the walker's own re-sent answer is never judged as the person's." `dry_world.run_exit_row` keeps the stub count at the first new ask (`first_ask` in `counts`). Add a table row in §6: "C2: a conductor call in a later post-answer turn is not counted". This changes C2 for every group, so B4 applies.

### B2 — the FV1-8 row contradicts the card's own guard (blocks dispatch)
`gate_A/words:questions-deferred` answers `token: "approve"` at the PLAIN ask (`T/fixtures/stories/dry-1/exits/gates.json:32`) and lists C2. At a plain ask `asked.offered` is empty and no window record of `gate_A` exists, so C2 fails ("carries no offered set", `T/dry_exits.py:1320-1321`). The card's guard forbids C2 n/a on a token row (§3). So the row can never pass once its state has a writer. At the plain ask, `approve` is the approval WORD, read by `gate_approval` from the first line (`S/driver_gates.py:1099-1117`), not an offered token.
Exact edit (§3 "Row data"): the FV1-8 row becomes `answer: {"token": null, "words": "approve", "words_file": null}`, `na: {"K15": ..., "C2": "at a plain gate the approval word is words read by gate_approval, not an offered token (driver_gates.py:1099-1117)"}`, checks `["C3","C6"]`; reach stays `live_only`.

### B3 — K15 (i) can be satisfied by the CONDUCTOR PROMPT's record, and the card does not pin which road the seed takes (blocks dispatch)
Facts:
- `no_move.validate_options` prices nothing. `priced_options` has exactly two callers on the gate path: the code fallback `S/driver_conductor.py:523`, and the conductor's PROMPT `gate_prices` -> `priced_section` -> `S/driver_runner.py:1285`. Grep of `priced_options` over `S/*.py`: `driver_conductor.py:523`, `driver_runner.py:1285`, `exploration.py:502`, the def `no_move.py:612`.
- So when the conductor's own options are accepted, the person's question has NO price record. The only `gate_A` record in its window is the prompt's. K15 (i)/(ii) then pass on a record written for the conductor, while the person saw the stub's move-row prices (`T/dry_stub.py:73-88`, `price_row(... f"moves.{move}")`). §2 item 4 calls the prompt record adversarial and argues it "cannot make a token row green". It can: K15 (iii) is then satisfied by any offered tokens drawn from rework/approve/retry/stop.
- Which road does the dry world take? The card lists this as NOT read. Read now:
  - The default stub offers every move in `## Moves open here` (`T/dry_stub.py:104-115`), and that includes `rework_stage` (its line matches `MOVE_LINE`, `S/no_move.py:221`) with no `args`. `go on` is closed at a gate (`S/no_move.py:166`).
  - `check_args(None)` refuses: "carries no \"args\" object" (`S/no_move.py:231-232`). That gives `ArgsRefused`, then one re-ask, then the stub says the same thing again, then `fallback_person` (`S/driver_conductor.py:760-773`), which files a `defect_found` (`:487-488`, `no_move_defect`) and builds `gate_fallback_question` (priced `:523`).
  - So by reading, every gate seed today reaches the CODE fallback. The window has two `gate_A` records (prompt + fallback), and the run files one factory `defect_found` per row. The test double causes that defect.
  - The `rework` row's control (a lone option) also hits the seed's conductor call: `copy.control(row["stub"])` runs before `run_seed` (`T/dry_world.py:1232-1235`). That gives "one option is legal only as the rework option when chosen", then the fallback. It works, but by accident and unstated.

Exact edit:
- (a) §2 item 1: the spy stamps `prompt: true` on a record written while the driver composes a conductor prompt (`any(f.function == "_conductor_text" for f in inspect.stack())` in `passing_spy`; test layer, it reads the driver's call chain and changes nothing).
- §2 item 3: the window excludes `prompt` records. Invariant: "a record counts for an ask only if written while raising THAT question for the person".
- §2 item 4: drop bullets 2-3, which then have no subject.
- (b) New §4 point: "the seed reaches the code fallback (`driver_conductor.py:504-527`) because the stub's default verdict carries a `rework` option with no `args` and is refused; this files one `defect_found` per row (a stub artefact, stated, not judged)". The first probe run prints the window and `asked.offered` of one row, so the road is measured and not just read.

If the Lead rejects (a), the card must at least state that K15 cannot tell prompt pricing from question pricing.

### B4 — the DoD never shows that the merged groups stay green (blocks dispatch)
The identity rule (`ask_window` replacing `priced[-1]` in K15, C2 and `_holds`), the C2 change of B1 and F-2's `chosen` exclusion apply to every group. Main holds key rows `s1.review/{agree,flip,free words,empty}` and C2 rows `kind:halt/free words`, `kind:s1_review/free words` (`fixtures/stories/dry-1/exits/s0.json`, `s1-s4.json`, main checkout, listed by script). The DoD runs only `--part exits:gates`.
Exact edit (DoD (6)): add ONE run each of `--part exits:s0` and `--part exits:s1-s4`, with every row's outcome equal to its outcome before the change (the builder records the before line from its first run, or from the last batch canon). Any change is reported, not labelled.

### B5 — C3 n/a has no guard: it can hide a real red (blocks dispatch)
§3 gives guards for K15 n/a (no `offered`) and C2 n/a (no token), but none for C3. A row whose token has `factory: stages_again` (rework) could declare C3 n/a and hide a state that did not move. That breaks AR-28 in the other direction.
Exact edit (§3, guard list and §6 table): "C3 n/a is legal only when the row's answer has no token, or the token's data row in `question-prices.json` (the row's key) has `factory: nothing`. Else FAIL 'C3 declared n/a but the price row of <token> says factory <x>'". Also change the why text: `retry`/`stop` have something observable (the data's `nothing` expects the fingerprint UNCHANGED). The why should say "factory nothing: the unchanged-state check is F-5 (b), queued at <finding>", not "nothing observable".

### B6 — TEMPORAL: `after:FV3-5` in the DoD and edge 5 (blocks dispatch)
The label comes from `T/fixtures/driver-exits/known_red.json:4-7` (`main/S5 -> FV3-5`). Node N2h-b2 changes it to `FV3-20` (`docs/tasks/specs/20261117-p1b-n2h-v-critic-stub-window-card.md:25`, `:97`). This card starts after N2h-v, so in that world the DoD line "`gate_B/*` NOTE `after:FV3-5`" is wrong.
Exact edit (DoD (6), §5 edge 5, the §7 report table): "`gate_B/*` NOTE `after:<node of main/S5 in fixtures/driver-exits/known_red.json at run time>` (FV3-5 before N2h-b2 merges, FV3-20 after); the move that changes the label is N2h-b2, the move that makes S8 is the fix of that node, not this card".

### F1 — F-2 wording and the cut prompt (fix in round)
Make F-2 (a) and the §6 stub row say "a line equal to `## The person's choice` anywhere in the prompt" (not "last section heading").
Add to §7: "if `gate_A/rework` is red on C2 with `chosen: false`, the builder checks whether the prompt the stub received carries the heading. If it does not (the 6000-character cut, `driver_conductor.py:320`, `:687`), the red is a PRODUCT finding (the person's choice can be cut from the conductor's prompt, FR-8), reported with the prompt length, never set `live_only` as a stub gap".
The stub journal line gets `prompt_chars` to make this checkable.

### F2 — K15 (ii) is a tautology; the card counts it as an observation (fix in round)
`priced_options` raises `DataUnreadable` for any answer that is not a data row (`S/no_move.py:619-626`). The spy records only after a successful call (`T/dry_driver.py:48-50`). So "answers all among the data rows" is filtered by the same file as the expectation. Only "non-empty" can fail. This is the Lead's constraint (1) / P20 / FR-58 case.
Edit §3 K15: (ii) becomes "non-empty answers (shape)", with the sentence "the subset test is not an observation: the price resolver refuses an answer outside the rows". The observations are (i) (the key was priced while raising this ask) and (iii) (`asked.offered`, driver-side after validation).

### F3 — wrong justification for `answer.words: null` (fix in round)
§3 and §10 say "a token answer ignores words, `T/dry_world.py:1110-1112`". False: when both are set, `answer_bytes` writes `f"{token}\n{words}"` (`T/dry_world.py:1108-1109`). The driver compares the WHOLE answer with the tokens (`self.s0_normalize(words) not in self.seam_tokens(asked)`, `S/driver_machine.py:3402-3403`), so `rework\nAdd a case...` is NEW gate words, not the token. Setting null is therefore NECESSARY, not cosmetic. Edit the reason to that.

### F4 — `say` reached-condition too wide (fix in round)
§4 (3) asks only for "a new question row AND `offered` non-empty". Add: "and the pending ask is still `question` at `stage`". Invariant: the seed reaches THIS gate's priced question, never another question that happens to carry `offered`. K15 would catch it later as "key not observed", but the seed detail should name the cause.
Also have the loader refuse `words` whose first line normalises to an approval word of `gate-approval-words.json`, because such words record the gate (`S/driver_gates.py:1117`).

### F5 — siblings inside the same artifact not swept (fix in round)
The card moves `_ask_of` at `T/dry_world.py:1251` off `questions[-1]`. Two neighbours read the same "newest row = the ask" in the same file:
- `T/dry_world.py:1279` (post-answer asks, same function `run_exit_row`). This one belongs in this card: apply the same identified row.
- `T/dry_world.py:928` (`main_pass`: `asked, q = len(questions), questions[-1]`). A deferred question writes a row and is not pending (`S/driver_dialog.py:430-433`). Queue it as a finding (main pass is a non-goal here), or include it.

Exact edit: §2 item 3 adds `:1279`; §8 siblings adds the `:928` line with its pointer.

### F6 — re-raised questions get no price record (fix in round, edge to add)
`held_question` builds the Person from `asked` and the question file with NO pricing (`S/driver_dialog.py:600-629`), and `ask()` writes a new row. A deferred question asked again before gate B is the same kind of re-raise. The window of such an ask is empty, so K15 FAILs. That is a false red (allowed direction), but the card does not name it. Groups s6-s9 will meet it.
Edit §5: a new edge "an ask re-raised without pricing (`held_question`, deferred re-ask): window empty -> K15 FAIL 'the ask was raised again without pricing (held)'; never read from the earlier raise's window".

### F7 — the spy's task root (fix in round, note)
`passing_spy(real, sink)` knows only the sink. The card does not say how it finds `task_root` for `question_rows`. `sink.parent.parent` is right in the driver (`T/dry_driver.py:31`). In the selftest the sink is `tmp/n2-priced/dry-priced.jsonl` (`T/dry_stub.py:1377`), so the "root" is `tmp`, which other selftest parts may fill.
Edit §2 item 1 / §6: "`task_root = sink.parent.parent`; the selftest uses `tmp/<case>/state/dry-priced.jsonl`".

### F8 — citations (note)
"The `rework` token's executor IS a conductor call (`S/driver_machine.py:2355`, `:2361`)" cites docstring lines. The call is `S/driver_machine.py:2446`. Not load-bearing.

### F9 — n/a count is invisible to the ratchets (note)
An n/a declaration lowers what is checked and has no counter. Suggest a line in `dry_exits.py --check` NUMBER: `na <n>`, for visibility (not a ratchet). The Lead decides.

### F10 — `dry_stub.py` collision with N2h-v (note, answer to key 6)
The card's change: the conductor `else:` branch of `fill_role` (journal line `T/dry_stub.py:911-913`, add `chosen` and `prompt_chars`) plus selftest rows near `:1377-1381` (spy). N2h-v changes `critic_branch` / `automator_branch` (`:577-582` on main) and a new `merge_story_fragments`, and reorders the ROLE branch of `fill_role` (N2h-v card §2.2).
So the two are disjoint by block but NOT by function (both touch `fill_role`), and both append selftest rows. Starting after N2h-v merges, as planned, is enough. The builder merges `main` and keeps both sets of rows.

## Answers to the acceptance keys

1. **Facts by trail.** Verified at file:line in the tree:
   - Plain gate raises a bare Person (`S/driver_gates.py:322`).
   - `offered` is written only `if person.offered` (`S/driver_dialog.py:321`).
   - The question row is written in `judge_own_question` (`:410-419`), after the caller priced it. Exception: if `human_text` raises, `return []` comes BEFORE the row (`:404-406`), so the row is absent. This fails red, safely.
   - Seam Person sets `offered` (`S/driver_conductor.py:422`, within the cited 419-427).
   - Fallback is priced at `:523`; the chosen heading is at `:687`.
   - Gate words go to the conductor (`S/driver_machine.py:3606-3607`); an empty answer is refused before any branch (`:3380-3381`).
   - Approval is the first line only (`S/driver_gates.py:1117`); approval words at `R/gate-approval-words.json:3-4`; `gate_A` rows at `R/question-prices.json:143-148`.
   - `priced[-1]` at `T/dry_world.py:1153-1154` and `:1243-1244`; `_ask_of(questions[-1])` at `:1251`; whys only for kind `conductor` (`:1274-1275`); seed FAIL at `T/dry_exits.py:1414-1415`; empty checks refused at `:1117-1118`.

   "Answering with words leads to a priced question behind the existing spy" holds: `priced_options` is looked up on the module at call time (`T/dry_driver.py:73`). But the record that lands depends on the road (B3). An ask is identified in the driver's records by `driver-state.json` `asked` (kind, stage, dispatch) and the `driver-questions.jsonl` row with the same triple. The row carries no id, so the ordinal is the only join. The card's rule matches this.
2. **Identity rule vs merged rows.** By reading, `s1.review/*` and the halt rows raise their question and price it in the same process before the row is written, so `q == ordinal` holds and today's greens should stay. Not run (B4 makes the builder run them).
   - Green to red is possible: a re-raised question has no record (F6), a missing row (`human_text` failure), and C2 counting after B1.
   - Red to green: I found no route once B3 (a) excludes prompt records. Without B3, a prompt record of the same key written in a turn whose conductor answered `continue` lands in the next ask's window. At a plain gate that makes K15 (i) green with nothing offered, though only for a row that does not declare K15 n/a.
   - The §2 item 4 inputs:
     - no record: FAIL;
     - earlier ask only: FAIL;
     - two asks with the same triple: the LAST row is the seam (correct), and after a `retry` the plain re-ask is newer, which is correct for that ask;
     - empty offered: the seed does not reach (FAIL).

     The error direction holds for these once B3 is applied.
3. **Per variant, expectation vs observation.** The same-file case is K15 (ii) (F2). C2's offered set is the driver's `asked.offered`, which on the fallback road comes from code `GATE_OPTIONS` and on the conductor road from the stub's options after the driver validates them. Both are driver-side, not the data file. F-2's `chosen` flag records the driver's prompt (a recorder, not an echo of the double's own decision).
   - n/a on `retry`/`stop` C3 hides an observable check: `factory: nothing` expects the state unchanged (B5, F-5).
   - n/a on `free words` C2 is real. A non-token answer at the seam is new gate words (`S/driver_machine.py:3402-3403`), and the conductor call that follows is by design, so C2 as defined cannot pass.
   - n/a on `free words` C3 is real: nothing is recorded until a choice is made.
4. **(b) vs the row's subject.** (b) tests the subject: at a gate, X in {rework, approve, retry, stop} is an answer only to the seam question (`S/driver_machine.py:2349-2361`, `:2389-2398`). A plain TOKEN typed at the plain gate (`stop`, `retry`, `rework`) is words to the conductor (`:3606-3607`), the same road as the `say` seed. That road is judged by every gate row's seed and by K15 (iii) on the seeded ask, so it is not left unjudged. The plain approval word is walked by the main pass (`T/fixtures/stories/dry-1/story.json:85`). Not walked by anything: the gate-A-only word `approve as is` (`R/gate-approval-words.json:4`, passes open items). It is not a price key, so axis 38 does not list it. Note for the Lead: either a finding, or out of scope.
5. **`say`.** The grammar is sound (three keys, non-blank, S0..S9, ASCII, no `## ` line). Add the approval-word refusal and the same-ask reach condition (F4). There is no length limit, which is acceptable because fixtures are ours. A seed that never reaches the gate gives "say: pending is <kind> at <stage>", a FAIL. TEMPORAL: B6.
6. **Weaker model.** Files and functions are named, there is a test per item, and the edges carry invariants. Missing: B1-B6, F1, F3, F4, F7. The DoD runs are exact, plus the two runs of B4. The `dry_stub.py` overlap is in F10.
7. **Census / AR-20.** No ratchet is raised, except the conditional `rework -> live_only`, which carries one named `raised_by` entry each. That holds. `driven_keys` needs EVERY answer row executable (`T/dry_exits.py:885-896`), so the N4c consequence stated in §7 is right. n/a is outside the ratchets (F9).
8. **Class-wide.** Axis 34: one `say` form and one `ask_window` for every group. Gate key rows of s5 and s6-s9 take the form in their own nodes. The card names this, and also the `:1279` / `:928` siblings (F5) and re-raised asks (F6), which s6-s9 will meet. Axis 38: unchanged. N4c: `PINNED_ELSEWHERE` stays while `rework` is `live_only`. Analog: the prompt-record problem (B3) applies to every key row whose ask is raised in a turn that also built a conductor prompt with gate prices. Solving it in the spy covers them all.

## Standing questions (plan gate)
- **One action, one road (P31, brief item 12):** one seed form, one identity helper, one n/a field, and no exclusion of a group or case. The `rework` row's private stub control is a data row, not a branch. No finding.
- **Duplication and consistency:** none found beyond F5. Searched for `priced\[-1\]|dry-priced|questions\[-1\]|priced_at_ask` with the Grep tool, case-insensitive, `*.py` under `T/`. Hits: `dry_world.py:928,1024,1131,1153-1154,1243-1244,1251,1279`, `dry_exits.py:1316,1384,2585,2600-2602`, `dry_stub.py:1377-1389`, `dry_driver.py`. Positive control: the known `priced_at_ask` sites were found.
- **Code quality:** the plan replaces one fact name and adds no second road. F2 and F3 are honesty fixes in the text.
- **Tests:** stays inside TESTING.md (table rows, one scenario part, no new file). Volume is not measured at plan stage.

## What I did not check
- I ran no driver: the default-stub road (B3) and the `retry` re-send (B1) are traced by reading, not run.
- The gate A packet length (F1, an estimate).
- `combine_gate_words` and the gate B exploratory and stand-gap readers on the seed words.
- `test_scenario_dry_1.py` / `walk_exits` (`after:` logic).
- `judgment-census.json` scope; what `scenario_walk.py --witness-for` prints.
- Whether the `rework` lone-option control passes `check_args` with the dry world's facts.

## Trail
Read:
- the card, whole;
- the gates report, whole;
- `T/dry_world.py` 905-945, 1018-1030, 1100-1300;
- `T/dry_exits.py` 880-900, 941-990, 1300-1440, consts 64-68;
- `T/dry_driver.py` 1-82;
- `T/dry_stub.py` 30-130, 896-922, 1370-1395;
- `S/driver_dialog.py` 290-349, 395-495, 600-630;
- `S/driver_gates.py` 130-142, 300-330, 1099-1118;
- `S/driver_conductor.py` 263-350, 405-560, 560-900;
- `S/driver_machine.py` 2349-2455, 3375-3420, 3575-3612, 4105-4125, grep 4080-4103;
- `S/no_move.py` 36-39, 114-128, 161-185, 208-240, 257-300, 397-520, 612-650;
- `S/driver_journal.py` 385-400;
- `R/question-prices.json` 135-160; `R/gate-approval-words.json`; `R/conductor-actions.json` moves (script);
- `T/fixtures/stories/dry-1/exits/gates.json` 1-32; `story.json` 83-87; main `exits/s0.json` and `s1-s4.json` rows (script);
- `T/fixtures/driver-exits/known_red.json`; the N2h-v card (grep);
- `docs/SIBLING_MAP.md` headings; `tools/critic_verdict.schema.json`.

Re-runs: none of the mechanical layer (plan gate; nothing attached to re-run).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 gate_A/retry: the walker re-sends retry to the plain gate in turn 2, a conductor call follows, and C2 fails (dry_world.py:1281-1283, dry_exits.py:1326-1327); C2 must count calls only up to the first new ask",
    "B2 FV1-8 row answers token approve at a plain ask with C2 listed, and the card forbids C2 n/a on a token row, so it can never pass; make it words approve with C2 n/a",
    "B3 K15 (i) can be satisfied by the conductor PROMPT record (gate_prices -> driver_runner.py:1285), since validate_options prices nothing; the spy should stamp prompt records and the window exclude them; pin the seed road (default stub rework without args refused, fallback at driver_conductor.py:523, one defect_found per row)",
    "B4 DoD lacks one run each of --part exits:s0 and exits:s1-s4; the identity rule and the C2 change apply to merged groups",
    "B5 C3 n/a has no guard; legal only for no-token rows or price rows with factory nothing",
    "B6 TEMPORAL: DoD and edge 5 hard-code after:FV3-5, which N2h-b2 changes to FV3-20 in known_red.json main/S5"
  ],
  "fixes": [
    "B1-B6 as in blockers",
    "F1 F-2 detection is a line equal to the heading anywhere, not the last heading; a C2 red with chosen false and the heading cut at 6000 chars is a product finding, not live_only; the stub journals prompt_chars",
    "F2 K15 (ii) subset test is a tautology (no_move.py:619-626 plus the spy records after success); state it as a shape check",
    "F3 the answer.words null reason is wrong: answer_bytes writes token newline words and the driver reads the whole answer as new gate words",
    "F4 say is reached only if the pending ask is still the same kind at the same stage; the loader refuses approval-word words",
    "F5 sweep dry_world.py:1279 (same function); queue or include main_pass dry_world.py:928",
    "F6 edge: a held or deferred re-raised ask has no price record; K15 FAIL with its own text",
    "F7 the spy's task_root is sink.parent.parent; the selftest sink path goes under tmp/case/state",
    "F-5 (b) and F-4 residuals named as finding files with an owner pile"
  ],
  "class_completeness": "Axis 34: one say form and one ask_window for all groups (named). Missing: dry_world.py:1279 (same artifact) and :928 (main pass) newest-row-as-ask siblings; re-raised asks with no pricing (held_question, deferred) that s6-s9 will meet; the prompt-record class applies to every key row raised in a turn that built a gate-priced conductor prompt and is fixed once in the spy. Axis 38: census unchanged; N4c PINNED_ELSEWHERE consequence stated correctly.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-p1b-gate-ask-judge-card.md",
      "tree docs/tasks/specs/reports/20261117-p1b-n4-gates-report.md",
      "tree scripts/tests/dry_world.py 905-945 1018-1030 1100-1300",
      "tree scripts/tests/dry_exits.py 64-68 880-900 941-990 1300-1440",
      "tree scripts/tests/dry_driver.py 1-82",
      "tree scripts/tests/dry_stub.py 30-130 896-922 1370-1395",
      "tree scripts/driver_dialog.py 290-495 600-630",
      "tree scripts/driver_gates.py 130-142 300-330 1099-1118",
      "tree scripts/driver_conductor.py 263-900",
      "tree scripts/driver_machine.py 2349-2455 3375-3420 3575-3612 4105-4125",
      "tree scripts/no_move.py 36-39 114-240 257-300 397-520 612-650",
      "tree scripts/driver_journal.py 385-400",
      "tree references/question-prices.json 135-160, gate-approval-words.json, conductor-actions.json moves",
      "tree fixtures exits/gates.json, story.json 83-87, driver-exits/known_red.json",
      "main fixtures exits/s0.json s1-s4.json rows",
      "docs/tasks/specs/20261117-p1b-n2h-v-critic-stub-window-card.md (grep)",
      "docs/SIBLING_MAP.md headings"
    ],
    "reruns": []
  }
}
```
