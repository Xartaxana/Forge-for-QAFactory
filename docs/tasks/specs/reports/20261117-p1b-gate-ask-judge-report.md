# Report t-1069: how a gate key row is judged (builder, card r2 + binding edits G1-G5)

Tree `C:/QAFactory/forge-repo/.claude/worktrees/agent-a4aebd95c3ca7d59c`, branch `worktree-agent-a4aebd95c3ca7d59c`. Card
`docs/tasks/specs/20261117-p1b-gate-ask-judge-card-r2.md` (main checkout). Status: code and tables done; three rows of the gates part are red with
evidence (below) and come back as QUESTIONS (Q1, Q2); nothing was labelled or hidden.

## 0. Merge (card section 0)
- `git fetch origin`; `git merge origin/main` -> merge commit `016321a7` (head before: `11494798`). Conflicts: NONE (dry_stub.py merged without a conflict).
- `git merge-base --is-ancestor 5408a22fb0328284f51d0145fc0e9eeae06df1a8 HEAD` -> exit 0 (printed `ancestor=0`).
- Fact check: after the merge `known_red.json` says `main/S5 -> FV3-20` and the gate_B rows print `after:FV3-20` (world W1, edge 7).

## 1. Probe step 1 (section 9): `gate_A/approve` alone, window and `asked.offered` (verbatim)
```
FACTS gate_A/approve {"seed": {"reached": true, "detail": ""}, "ask_ordinal": 2, "post_turns": 1, "ended_at": null, "exhausted": null, "loop": "", "conductor_whys": [], "conductor_calls": 0}
  window [{"key": "gate_A", "answers": ["rework", "approve", "retry", "stop"], "q": 2, "prompt": false}] offered ['rework', 'approve', 'retry', 'stop'] seen [{"key": "s1.review", "q": 0, "prompt": false}, {"key": "gate_A", "q": 2, "prompt": true}, {"key": "gate_A", "q": 2, "prompt": false}]
  asked_after {"kind": "environment", "stage": "S5", "dispatch": "", "at": "2026-11-17T07:57:09+00:00", "offered": ["retry", "go on"], "options": [{"token": "retry", "move": "person_does"}, {"token": "go on", "move": "go_on_as_is"}], "words_file": "", "why": "", "block": "stand not confirmed"}
PASS dry-1/exits:gates/gate_A/approve
```
Reading: the seed `say` reaches the SEAM question (ordinal 2) with offered [rework, approve, retry, stop]. The records show the stamp working: of the two
`gate_A` records at q 2, ONE is `prompt: true` (the conductor prompt's `gate_prices`) and is excluded; the window holds the other. The code fallback road
(card section 5 "Which road") is confirmed: two conductor calls in the seed (`ask_person`, then the re-ask), then the code question.

## 2. Probe step 2 (rework) and the gate rows that stay red
Rework control NOT attempted with a lone `rework_stage` option: the prompt measurement settles the row first (card section 9 exception F1). Verbatim (`gate_A/rework` alone):
```
STUBROWS [{"conductor": "conductor", "n": 1, "action": "ask_person", "chosen": false, "prompt_chars": 25285}, {"conductor": "conductor", "n": 2, "action": "ask_person", "chosen": false, "prompt_chars": 25285}, {"conductor": "conductor", "n": 3, "action": "ask_person", "chosen": false, "prompt_chars": 25291}, {"conductor": "conductor", "n": 4, "action": "ask_person", "chosen": false, "prompt_chars": 25291}, {"conductor": "conductor", "n": 5, "action": "ask_person", "chosen": false, "prompt_chars": 25295}, {"conductor": "conductor", "n": 6, "action": "ask_person", "chosen": false, "prompt_chars": 25295}]
FACTS gate_A/rework {"seed": {"reached": true, "detail": ""}, "ask_ordinal": 2, "post_turns": 2, "ended_at": null, "exhausted": null, "loop": "the same question `gate_A` at S4 was asked a third time with nothing new given to the author (C5, the loop of FV1-13/FV1-22)", "conductor_whys": [], "conductor_calls": 2}
FAIL dry-1/exits:gates/gate_A/rework — C2: the driver recorded no answer for this ask (no driver-answers.jsonl row with its question_sha; 0 row(s) added); C3: the answer changed nothing: the state fingerprint is the one it was asked at (C3)
```
Every conductor call, including the two of the person's choice `rework` (n 3 and 4), journals `chosen: false` with `prompt_chars` 25291 (> 6000): the paragraph
`## The person's choice` is appended LAST by `_conductor_text` (driver_conductor.py:687) and the text goes through `refusal.strip()[:6000]` (driver_conductor.py:320),
so the heading is cut. This is a PRODUCT finding (the person's choice can be cut from the conductor's prompt, FR-8), not a stub gap: the row stays `reach: story`,
red, NOT `live_only` (edge 12 / section 9). Not labelled in known_red (Lead labels).

`gate_A/stop` (separate probe, driver output of the answer turn, verbatim head):
```
DRIVE ['--answer', 'mp\\qa-dry-row-9a7sqegf\\project\\answer.md', '--max-boundaries', '1'] rc 3 
[progress] S5 Automation · waiting for your word at gate A since 09:23 (0 min) · $0.00 so far (recorded only) · done S0–S4
answer for gate_A (S4): stop
[progress] S5 Automation · waiting for your word at gate A since 09:23 (0 min) · $0.00 so far (recorded only) · done S0–S4
# Driver question — DRY-1
kind: gate_A
stage: S4
dispatch: 
asked_at: 2026-11-17T08:23:35+00:00

You said to stop. Nothing runs and nothing is spent. If you want the factory to go on after all, answer `rework` or `approve` or `retry`.

```
`stop` IS read (the held question says "You said to stop ... answer `rework` or `approve` or `retry`") and the print `answer for gate_A (S4): stop` shows `answer_row` ran, but no
`driver-answers.jsonl` row is on disk: `record_answer_row` writes at the END of `take_answer` (driver_conductor.py:235-250) and a held question raises a `Person` out of
`take_seam_answer` (driver_machine.py:2395-2397) before it. The card table (section 4, per-variant) predicted "answer row" for `stop` and `rework`; reality: none. Same cause for rework
(its `chosen` call ends in `options_person`, a raised Person).

## 3. Row table (card section 4 "Row data"; seed reached; outcome; part time 555 s, main-pass prefix 370.6 s; per-row seconds are not printed by the part)
| row | seed | outcome |
|---|---|---|
| gate_A/rework | to-gate-A-priced reached | FAIL C2 (no answer row), C3 (unchanged) - product finding, edge 12 |
| gate_A/approve | reached | PASS |
| gate_A/retry | reached | PASS (prints its n/a C3) |
| gate_A/stop | reached | FAIL C2 (no answer row; n/a C3 printed) - Q1 |
| gate_A/free words | reached | PASS (prints n/a C2, n/a C3) |
| gate_A/empty | reached | PASS |
| gate_B/* (6 rows) | not run | NOTE `after:FV3-20` (W1; label read from known_red.json at run time) |
| gate_A/words:questions-deferred | live_only, seed null | NOTE live_only (row data per section 4: words `approve`, checks C3, C6, n/a K15 and C2) |

## 4. Before / after of `exits:s0` and `exits:s1-s4` (DoD 7), BEFORE = right after the merge, before any edit
- `exits:s1-s4`: every non-scoreboard line IDENTICAL before and after (diff empty); `6/6 ok` both.
- `exits:s0`: every row's outcome kind identical; ONE line carries new detail. BEFORE then AFTER:
```
NOTE dry-1/exits:s0/kind:halt/free words: red evidence: C2: the driver recorded no answer for this ask (no driver-answers.jsonl row with its question_sha; 0 row(s) added); C3: the answer changed nothing: the state fingerprint is the one it was asked at (C3)
NOTE dry-1/exits:s0/kind:halt/free words: red evidence: C2: the driver recorded no answer for this ask (no driver-answers.jsonl row with its question_sha; 0 row(s) added); C3: the answer changed nothing: the state fingerprint is the one it was asked at (C3); ended at halt at S1 after turn 1
```
The row is `known red -> FV3-16` (a NOTE with red evidence) before and after; the detail gained `ended at halt at S1 after turn 1` (G5: section 6 exposing a re-send; reported, row/stub/section 6 unchanged).
`2/2 ok` both.

## 5. Witness (final state, nothing edited after these runs)
`scenario_walk.py --witness-for <the seven package owns>` printed one test file, `test_scenario_dry_1.py` (all seven owns point to it). Its runs, verbatim tails:
```

=== scenario dry-1: 9/9 ok ===
rc=0
```
`--part exits:gates` (full, minus scoreboard/snapshots/unwalked/route lines):
```
NOTE dry-1/exits:gates/prefix: reached S4 in 370.6 s; snapshots S0, S1, S2, S3, S4, gate-A; stopped: the road met the conductor: a state the driver has no move for; its own words: # The factory's own words — DRY-1, conductor at S5 This is what the check printed, in its own vocabulary. It is here beca
FAIL dry-1/exits:gates/gate_A/rework — C2: the driver recorded no answer for this ask (no driver-answers.jsonl row with its question_sha; 0 row(s) added); C3: the answer changed nothing: the state fingerprint is the one it was asked at (C3)
PASS dry-1/exits:gates/gate_A/approve
PASS dry-1/exits:gates/gate_A/retry
FAIL dry-1/exits:gates/gate_A/stop — C2: the driver recorded no answer for this ask (no driver-answers.jsonl row with its question_sha; 0 row(s) added); n/a C3: factory nothing: the unchanged-state check is F-5 (b), queued at finding R1-a (live-run-fvf)
PASS dry-1/exits:gates/gate_A/free words
PASS dry-1/exits:gates/gate_A/empty
NOTE dry-1/exits:gates/gate_B/rework: after:FV3-20: its start snapshot S8 was not made
NOTE dry-1/exits:gates/gate_B/approve: after:FV3-20: its start snapshot S8 was not made
NOTE dry-1/exits:gates/gate_B/retry: after:FV3-20: its start snapshot S8 was not made
NOTE dry-1/exits:gates/gate_B/stop: after:FV3-20: its start snapshot S8 was not made
NOTE dry-1/exits:gates/gate_B/free words: after:FV3-20: its start snapshot S8 was not made
NOTE dry-1/exits:gates/gate_B/empty: after:FV3-20: its start snapshot S8 was not made
FAIL dry-1/exits:gates/known_red — new red: gate_A/rework — fix it, or add "gate_A/rework": {"node": "<FV1-n or node id>", "raised_by": "<verdict or word that names this raise>"} to C:\QAFactory\forge-repo\.claude\worktrees\agent-a4aebd95c3ca7d59c\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\known_red\gates.json kn
FAIL dry-1/exits:gates/known_red — new red: gate_A/stop — fix it, or add "gate_A/stop": {"node": "<FV1-n or node id>", "raised_by": "<verdict or word that names this raise>"} to C:\QAFactory\forge-repo\.claude\worktrees\agent-a4aebd95c3ca7d59c\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\known_red\gates.json known_
PASS dry-1/exits:gates/outcomes

=== scenario dry-1: 5/9 ok ===
```
```
dry_exits.py --selftest -> dry_exits selftest: 193/193 cases rc=0
dry_stub.py --selftest  -> === dry_stub --selftest: 225/225 ok === rc=0
dry_exits.py --check    -> NUMBER na: 10 declarations (C2 3, C3 6, K15 1)   [recount: python -B -c "import json, glob; print(sum(len((r.get('expect') or {}).get('na') or {}) for f in glob.glob('tes || dry_exits --check: 0 discrepancies
recount of `na` (scripts/): 10
```

## 6. Requirements -> where -> proving row
| card item | where | proof |
|---|---|---|
| s3 spy `q`, `prompt` | dry_driver.py `passing_spy`, `_raising_for_conductor`, `_question_count` | dry_stub selftest N2 item 5 (a)(b)(c)(d) |
| s3 `ask_window` one reader; `priced_window`, `ask_ordinal`; `priced_at_ask` gone | dry_world.py `ask_row`, `ask_window`, `_holds`, `run_exit_row` | gates part, probe 1; judge rows K15 (1)(10) |
| s3 item 4 guards (older ask, prompt, no q, rename) | `ask_window`, `_window`, selftest AST guard | selftest (d) with positive control; judge rows K15 (1)(10), older spy |
| s4 K15 (i)(ii)(iii) + n/a guard | dry_exits.py `_judge_k15`, `_k15_absent` | judge rows K15 (1)(2)(3)(4)(10), no ordinal, held, older spy |
| s4 C2 offered source + cut + chosen | `_check_c2`, `row_facts(first)` | judge rows C2 (5); row_facts case (6)(7) |
| s4 C3 n/a guard (B5), C2 n/a guard | `_na_guards`, loader `_walk_na_problems` | judge rows C3 (8)(9), unknown price row, C2 with token; loader refusals |
| s5 `say` step + loader + run | `_say_problems`, `_say` | loader rows (missing key, blank, S10, `## `, `approve`, non-ASCII, good); run_seed say rows x5 |
| s6 turn end with G1 (`ended_at`, armed `turns`), G2 position, G3 (a)(b)(c) | run_exit_row loop; `_judge_always` | judge row (11); run_exit_row cases (i)-(iv) |
| s7 edges 1-14 | edges 1,2,3,8,10 K15 texts; 4 say/K15; 5 seam-vs-plain by `offered`; 6 `q` TEMPORAL; 7 W1 NOTE; 9 `read_rows`; 11 cap; 12 `chosen`/`prompt_chars`; 13 loader; 14 guards | rows above; edge 7 gates part; edge 12 probe 2 |
| s8 `na` NUMBER | `na_counts`, `_numbers` | `check: the NUMBER list carries the na: line`; judge_group case |
| s8 stub rows | dry_stub.py conductor branch (`CHOSEN_HEADING`) | selftest `N2 edge: a prompt with a line equal ...` |
| s4 row data, recipes | exits/gates.json (12 rows + FV1-8), seeds/gates.json | `--check` 0 discrepancies; gates part |
| G4 four control cases | selftest `run_exit_row` x3 + judge (11) | selftest cases; (iii) merged with (ii): three identical asks |
| G5 | s0 line above; no s1-s4 flip | section 4 |

## 7. FR walk (test layer only)
A-B-E-F: no refusal text, no text to a person, no delivery, no money: not applicable. C-11/C-14: new spy and stub-journal fields documented in `passing_spy` / the conductor branch comment. D-59: no record, no ordinal, empty offered, prompt-only window, n/a that its guard refuses -> FAIL. G-30: fixtures ASCII (checked by the `not ASCII` loader row). AR-22 producers/readers in one commit; AR-28; AR-13 (`question_rows`, `approval_words`, `_norm`); AR-20 ratchet untouched (`--check` 0 discrepancies); AR-29 data only.

## 8. Commit lines
See the commit message on the branch (architecture / judgment / tests-over lines).

## 9. Deviations, divergences, QUESTIONS
- **Q1 (reality vs card: `stop`).** Card section 4 expects a `driver-answers.jsonl` row for `stop` (and `rework`). The product writes none for a held question (evidence section 2). `gate_A/stop` therefore FAILs C2 and DoD (6) (`stop` PASS) is not met. Options: (a) product finding (a person's `stop` leaves no audit row, FR-8/AR-24) queued, row stays red; (b) declare C2 n/a for `stop` (my guard refuses: it has a token). I did neither.
- **Q2 (`rework`).** Red by the cut heading (product finding, edge 12, section 2). C3 red on the same row (unchanged state: the choice never reached a rework). No `live_only`, no known_red row written.
- `say` reading: the card text says "pending ask must be kind `question`"; implemented as the recipe's `question` value (`gate_A`), as its failure texts show (`expected <question> at <stage>`).
- `say` reached/no-new-question texts: when no new question row appears the text is `the driver exited (<rc>) with no new question` if rc != 0, else `say: the words at <q> raised no new question` (card gives both strings, not the discriminator).
- Stage-to-gate for the approval-word loader check uses `driver_gates.GATE_STAGE_OF` (S4 -> A, S8 -> B); other stages have no approval check.
- A PASS line now prints its detail (`judge_group` passes `outcome.detail` through; was `""`) - needed for the n/a lines.
- The per-row seconds are not printed by the walker; only part totals are given.
- No negative control was run on the run_exit_row cases (position mutation): not run; the cases assert `len(gates) == 2` and `post_turns == 1`, which a too-early stop fails by reading.

## 10. Analogs noticed (not fixed)
1. `fallback_person` / default stub: every seam call through the default stub files a `defect_found` (R1-c). 2. `approve as is` unwalked (F-8). 3. `main_pass` `questions[-1]` (R1-b). 4. `dry_world.py` `main/priced` NOTE (line ~1024) will also list prompt keys (stated in the card). 5. The `say` words at a gate are the seed for the rework instruction; a `say` at s5/s6-s9 gates is their own nodes. 6. Edge 12 product finding and Q1 are finding candidates for node R1.

## 11. Needed beyond the manifest
`docs/tasks/specs/20261117-p1b-gate-ask-judge-card-r2.md` pages 407-551 (second read page), `scripts/driver_conductor.py` (235-250, 314-326, 679-687), `scripts/driver_machine.py` (2345-2450), `scripts/gate_brief.py`, `scripts/driver_gates.py` (GATE_STAGE_OF), `scripts/controller.py` (REPAIR_CAUSES), `scripts/no_move.py` (check_args), `scripts/driver_journal.py`.

## Fix round after critic t-1077 (t-1069 attempt 2; verdict `docs/tasks/specs/reviews/t-1077-p1b-n4-gates-topic-code.md`)

Tree `C:/QAFactory/forge-repo/.claude/worktrees/agent-a4aebd95c3ca7d59c`. Step 0: `git fetch origin`, `git merge origin/main` -> no conflict; merge commit `bd3a91b7` (message amended to carry the architecture / judgment / axes lines). One more commit follows with this round (sha in the handback line, not pushed).

### B1 - the section 9 rework control, run once alone (`gate_A/rework`, a one-row copy of exits/seeds in the scratchpad passed by `--exits-root`; a probe wrapper prints the stub rows)
`stub.conductor` on rows `gate_A/rework` and `gate_B/rework`: `ask_person`, ONE option = `dry_stub.move_option("rework_stage","rework")` printed as data (price lines `factory` / `person` / `delivery` as the function resolved them) + `args` taken from the closed list the prompt printed: `stage S4, role qa-case-designer, cases [TC-1], cause question_answer` (the prompt's list: `S4 -> qa-case-critic | qa-case-designer`, `cases TC-1, TC-2`, causes `test_defect | mechanical | ... | question_answer | ...`).
```
STUBROWS [{"n": 1, "action": "ask_person", "chosen": false, "prompt_chars": 25317, "refusal_chars": 6000}, {"n": 2, "action": "ask_person", "chosen": false, "prompt_chars": 25323, "refusal_chars": 6000}]
ROWFACTS {... 'answer_records': [{'kind': 'gate_A', 'stage': 'S4', 'question_sha': '1a477e5a...', 'words': 'rework', 'token': 'rework', 'words_file': 'state/words/driver-answer-1794906541370.txt'}], 'conductor_calls': 1, 'conductor_chosen': 0}
FAIL dry-1/exits:gates/gate_A/rework — C2: a conductor call followed the answer and its why is not on record
```
Exactly the single red of the verdict (no "no answer row", no "changed nothing": the answer row IS written, C3 holds). `refusal_chars` == 6000 on both conductor calls (n 2 is the answer's own call; `chosen: false`, so the heading is cut), `prompt_chars` 25323.
`seam_rework`: NOT visible as a key of `driver-state.json` at the end of any of the three answer turns (printed `False` three times; the driver drops the record once the rework step has run). Seen by its effect: turn 3 output `accepted S4-qa-case-designer-2: 9 evidence files, stage open - next role of this stage` with the note `created by a rework or relaunch packet` (the author role ran again), and C3 did not fail. So "seam_rework recorded" is inferred from the rework executing, not observed as a key.

### Findings F1-F6 and the labels
- F1: judge row K15 (10) now `priced_window: []`, `priced_seen: [{key p.key, q 0, prompt true}]`, `ask_ordinal 0` -> FAIL "only a conductor prompt priced p.key at question 0". The window clause of `_k15_absent` is kept with a comment (hand-built fact guard).
- F2: the stub journals `refusal_chars` beside `prompt_chars` (`dry_stub.refusal_chars`: text between the `## The refusal` heading and the FRAME's next heading `## `story_step.py where``; the refusal text has headings of its own). Null (never 0) when the pair is absent. Line ends are normalised CRLF -> LF before measuring: the driver's prompt reaches the stub with CR LF on Windows (measured: my text-mode dump held a doubled CR), which would add one char per line and make "== 6000" unreachable. Selftest row `N2 edge (F2)`: 6 cases (6000; the same through CRLF; a refusal with headings of its own; empty -> 0; no refusal heading -> None; no frame heading -> None), expected values from the definition.
- F3 (Lead decided, amends card section 4 C2): `row_facts` returns `conductor_calls` (all of the cut) and `conductor_chosen`; `_chosen_excused` + `_check_c2` excuse chosen calls only when the row key's price row for the token has a `factory` that is neither `record`, `nothing` nor empty; no price row / no factory -> not excused. Judge rows: rework-class token PASS; `record` FAIL; `nothing` FAIL; no factory FAIL; no price row FAIL; rework-class with 2 calls (1 chosen) FAIL. The `row_facts` selftest (6)(7) re-expressed on `(calls, chosen)` = `[(3,1),(1,1),(2,1),(2,1)]` (counts by definition from its 4 stub lines).
- F4: `ask_reraised` = non-empty `asked.held_lead`. A judge row (plain observed-none text at ordinal 2, `ask_reraised` false) and a `run_exit_row` case (seam without `held_lead` -> False, with it -> True).
- F5: finding `plans/piles/live-run-fvf/findings/20261117-p1b-walker-post-answer-window-one-boundary.md`, node row FV2-95, README row. Each `why_unreached` resting on walker defect 3 now ends `[queued: walker defects 2-3, finding 20261117-p1b-walker-post-answer-window-one-boundary.md, node FV2-95]`: 11 in `fixtures/driver-exits/gates.json` (5 routes + 6 exit_gate joints) and the 5 route walk rows of `fixtures/stories/dry-1/exits/gates.json` (same text, kept equal).
- Finding (i) `20261117-p1b-conductor-refusal-cut-loses-the-persons-choice.md`, node row FV2-94, README row (FV2-93 was the last id of the table after the merge; `FV2-94|FV2-95` had 0 hits in plans/ and docs/ before).
- F6: the superseded line at the top of `20261117-p1b-n4-gates-report.md`.
- Labels `fixtures/driver-exits/known_red/gates.json` (new, `pins.known_red: 2`): `gate_A/stop` -> FV3-16 and `gate_A/rework` -> FV2-94, raised_by texts verbatim from Key 4(a) / 4(b); `gate_A/rework` labelled because the step-1 run showed exactly the predicted single red with refusal_chars 6000. `gate_B/rework` and `gate_B/stop`: NO label - unreachable (`after:FV3-20`, start snapshot S8 does not exist); gate_B/stop will turn red like gate_A/stop once S8 exists.
- Notes of the verdict: applied: the `callers()` annotation/docstring in the dry_stub selftest (tuple). Not applied: N1 (cosmetic, not a one-line correction), N2, N6, N7 (verdict: acceptable), N3 (the Lead's call: observing C2 at free words), N4 and N5 (belong to node R1, the Lead's; N5 should be a line there).

### Witness (each once, after all edits; verbatim tails)
```
( cd pkg && python -B scripts/tests/dry_exits.py --selftest )  -> dry_exits selftest: 201/201 cases
( cd pkg && python -B scripts/tests/dry_stub.py --selftest )   -> === dry_stub --selftest: 226/226 ok ===
( cd pkg && python -B scripts/tests/dry_exits.py --check )     -> NUMBER na: 10 declarations (C2 3, C3 6, K15 1) ... dry_exits --check: 0 discrepancies
( cd pkg && python -B scripts/selftest.py --limits --lang )    -> PASS limits: SKILL.md / agents / references within size caps | PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier | === qa-factory selftest: 4/4 ok ===
python -B T/tools/piles.py --repo T check                      -> piles check: ok   (run after `git add` of the pile files; before staging it printed "nothing staged -- nothing to check")
( cd pkg && python -B scripts/tests/test_scenario_dry_1.py )   -> === scenario dry-1: 9/9 ok === rc=0
( cd pkg && python -B scripts/tests/test_scenario_dry_1.py --part exits:gates )   (the gates group once whole, rc=0)
NOTE dry-1/exits:gates/prefix: reached S4 in 371.4 s; snapshots S0, S1, S2, S3, S4, gate-A; ...
NOTE dry-1/exits:gates/gate_A/rework: red evidence: C2: a conductor call followed the answer and its why is not on record
PASS dry-1/exits:gates/gate_A/approve
PASS dry-1/exits:gates/gate_A/retry
NOTE dry-1/exits:gates/gate_A/stop: red evidence: C2: the driver recorded no answer for this ask (no driver-answers.jsonl row with its question_sha; 0 row(s) added); n/a C3: factory nothing: the unchanged-state check is F-5 (b), queued at finding R1-a (live-run-fvf)
PASS dry-1/exits:gates/gate_A/free words
PASS dry-1/exits:gates/gate_A/empty
NOTE dry-1/exits:gates/gate_B/{rework,approve,retry,stop,free words,empty}: after:FV3-20: its start snapshot S8 was not made
NOTE dry-1/exits:gates/gate_A/words:questions-deferred: live_only: measured (t-1037): ...
NOTE dry-1/exits:gates/known_red: known red: gate_A/rework -> FV2-94
NOTE dry-1/exits:gates/known_red: known red: gate_A/stop -> FV3-16
PASS dry-1/exits:gates/outcomes
=== scenario dry-1: 5/5 ok ===
```
Not run: the `exits:s0` and `exits:s1-s4` groups (not in the dispatch). F3 can change them only if a row there has a `chosen` conductor call with a token that has no rework-class price row; the BATCH CANON covers them.

### Deviations and facts
- A temporary dump line in `dry_stub.py` (the prompt to a file) was used for the first probe to read the closed args list; restored by byte copy (sha256 `01a65d7f...84ae6` before and after the restore) before the real edits.
- The owned `.py` and fixture files have CRLF; edits kept it.
- The probe wrapper and the one-row root live in the scratchpad (`t1069_probe.py`, `root/`), not committed.
- Analogs: the answer-row class (stop_here, seam_chosen, record_seam_rework, no_move ending in a Person) is the Lead's product node (FV3-16 widened); gate_B rows got the same control as gate_A (done); s5 and s6-s9 gate key rows take the judge in their own nodes.
- Needed beyond the manifest: card r2 section 9 (lines 318-334), `scripts/driver_conductor.py` (300-340), `scripts/no_move.py` (args list), `references/question-prices.json`, `scripts/tests/test_scenario_dry_1.py` (the `--exits-root` / `--ledger` doors).
