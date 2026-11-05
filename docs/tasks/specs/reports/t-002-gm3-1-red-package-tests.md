# GM3-1: why 16 package test files are red on `main` (recon, no package edits)

Clone: `C:\AI\Factory\qa-forge-export-2026-11-05`, package `ai-packages/qa-factory/`. Tests: `scripts/tests/`. Raw outputs: `C:\AI\Factory\gm3-1-scratch\` (not committed).
Run form: `python -B <abs path>` once per file, cap 6 min, Windows. All "trial" results below are IN-MEMORY patches of a test file (scratch harness `trial.py` / `trial2.py`, nothing written into the package); they prove the proposed fix, they are not the fix.

## 0. Summary

Eight causes (C1..C8). One cause, C1 (X7-6: S6 is now accepted by its consumer, the failure analyst of S7), reddens 8 files and is the "real behaviour change that tests did not follow". Every key I could trace is class A or B (test pin or data/registry lags the code). I found NO class C (code broken) key. Two items are forks, because the fix changes what a role is told or what a gate refuses (C6 ceiling, C7 rubric pointer).

Counts of red keys by class (keys measured locally, see table for the files that crash or were over the cap): A = 38+ (C1, C3, C5, C6, C8), B = 10 (C2: one L1 key carrying 8 problems, C4: 1 key), C = 0, fork = 3 keys (C6: 2, C7: 2, counted as A/D until decided), D = the unmeasured remainder of `test_story_run_refusals.py` (C8).

## 1. Table: one row per file

| File | Status here | Red keys (as measured) | Class | Cause |
|---|---|---|---|---|
| test_story_run_refusals.py | NOT RUN to the end: over the 6-min cap (429 PASS, 0 FAIL at the kill). Supplementary 20-min run (non-spec): exit 1 after 983 s, scenario aborted by an uncaught `story_run.Person` at line 3423 | 0 FAIL lines; 1 aborting exception; rest of the file unmeasured | A (+D for the unmeasured rest) | C8 |
| test_words_doors.py | NOT RUN to the end: over the cap (369 PASS, 0 FAIL at the kill). Supplementary run: exit 1 after 572 s, **527/530** (matches CI) | 3 (`10 derived scope` x3) | A | C1 |
| test_story_run_deferred.py | red, exit 1, 28 s | 1 FAIL (`K-D1 S6 closes over the rest...`) + the scenario then aborts with FileNotFoundError; the other 7 scenarios of the file run green | A | C1 |
| test_s7_rejudge.py | red, exit 1, 38 s | 2 FAIL (Q9b) before an uncaught `StateConflict`; with the C1a helper fix 2 more appear (Q9c x2, C1b) | A | C1 |
| test_controller_state.py | red, exit 1, 35 s | 0 FAIL lines; aborts with `StateConflict` at line 1973 (the key CI names is the last PASS line before it, `P3 ...`) | A | C1 |
| test_contract_slices.py | red, exit 1, 10 s | 1 (219/220) | A | C5 |
| test_stages.py | red, exit 1, 8 s | 1 (125/126) | B | C4 |
| test_story_run_s7_live.py | red, exit 1, 32 s | 0 FAIL lines; aborts in `Live7.__init__`, `KeyError: 'request'` | A | C1 |
| test_story_run_s6.py | red, exit 1, 228 s | 15 FAIL then abort at line 341 (`Refusal`); a per-scenario re-run (`each_scenarios.py`, still going when I wrote this) shows 23+ FAIL and 2 aborting scenarios (`t261_k2...`, `t292_k19...`) | A | C1 |
| test_controller_rework.py | red, exit 1, 37 s | 0 FAIL lines; aborts at line 1859 `ValueError: no accepted qa-runner dispatch on S6 to rework: S6-qa-runner-1 is running` | A | C1 |
| test_driver_layers.py | red, exit 1, 51 s | 1 (51/52): L1 with 8 problems | B | C2 |
| test_question_branches.py | red, exit 1, 40 s | 2 (705/707) | A | C3 |
| test_brief_pack_s5_plan.py | red, exit 1, 67 s | 2 (181/183) | fork (A/C) | C7 |
| test_brief_pack_manual.py | red, exit 1, 9 s | 2 (99/101) | A, one fork | C6 |
| test_fixes_13797.py | red, exit 1, 17 s | 7 (63/70) | A | C1 |
| test_oracle_provenance.py | red, exit 1, 11 s | 1 (255/256) | A | C3 |

Not GREEN-on-Windows anywhere: all 16 are red here too.

## 2. Causes

### C1. X7-6: S6 has `acceptance_by: qa-failure-analyst`; the runner's own finish can no longer close S6. Tests and fixtures still close S6 by the runner (class A)

Touches S5-S9: YES (S6/S7 flow). The product code is already consistent; only test fixtures/pins change. Another branch rewriting S6/S7 must keep the fixtures in step.

Evidence (the shipped design, not a bug): `references/stages.json:195` `"acceptance_by": "qa-failure-analyst"` on S6 (S2, S3, S4 already had it; S5, S7, S8, S9 not). `test_controller_stage_acceptance.py:109` pins "S6 its consumer (X7-6)" and is green. Code that implements it: `scripts/acceptance.py:1286 consumer_close_refusal`, `:1314 stage_acceptance_refusal` (text "S6 cannot be closed by qa-runner's own finish: S6 has no stage acceptance for ..."), `scripts/controller.py:5310-5318` (the check runs in `validate(op="accept")` when `stage_complete`), `scripts/story_run.py:9262-9303` (`s6_consumer`, `s6_awaits`, `s6_accepted_pending`, `s6_need_record`), `:11252-11255`, `:11975-11979` (the runner's final window finishes with `OpenWork("stage_awaits_acceptance")`, `owed` and refused/held cases no longer make it `False`), `:12062-12179` (`stage_S7` and `s7_consumer_completion`: the analyst writes the accept record, then S6 closes by the record).

Verbatim key lines (first lines, full outputs in the scratch folder):
- fixes_13797: `FAIL F5: the manual half completes the stage — expected '', got 'S6 cannot be closed by qa-runner's own finish: S6 has no stage acceptance for S6-manual. Finish with `--not-complete --unresolved stage_awaits_acceptance ...`'` and `FAIL F5: S6 completed — expected 'completed', got 'running'`; also `F5: the automation half cannot complete S6 alone — 'manual-agent case TC-2' not found in: <the acceptance refusal>` (x3 more F5 lines).
- words_doors: `FAIL 10 derived scope: the automation half cannot complete S6 alone — 'manual-agent case TC-2' not found in:` , `FAIL 10 derived scope: one override of exactly that block...`, `FAIL 10 derived scope: the refusing code no longer refuses — expected '', got 'S6 derived scope: manual-agent case TC-2 has no accepted S6 dispatch ...'` (527/530).
- s7_rejudge: `FAIL Q9b the manual half closes S6 — expected '', got 'S6 cannot be closed by qa-runner's own finish ...'`, `FAIL Q9b S6 completed — expected 'completed', got 'running'`.
- s7_live: setup `controller --operation rework` prints `{"error": "sequential task already has an active dispatch: S6-qa-runner-1. Finish it first"}` (my diag `diag_s7live.out`), so `["request"]` is missing: `KeyError: 'request'`. Cause: `F.runner(... True)` of `Live7.__init__` line 91 is refused, leaving S6-qa-runner-1 running.
- controller_rework: `ValueError: no accepted qa-runner dispatch on S6 to rework: S6-qa-runner-1 is running, not accepted` (same helper).
- controller_state: `StateConflict: S6 cannot be closed by qa-worker's own finish: S6 has no stage acceptance for the last dispatch of its author` at test line 1973 (`late-s6` accept with `stage_complete: True`).
- story_run_s6 (all `got OpenWork(unresolved='stage_awaits_acceptance', ...)` where the pin says `True`/`False`): `D1(i)`, `D1(ii) stale/missing`, `D1(iii)` x8, `K3`, `K4`, `K5`, `entry 2`, `recovery: the LAST block...` x2, `K-RES ...`, `manual half absent: the automation runner gets complete=True`, `K19 by hand ...`, plus `a completion over a derived manual case nobody dispatched is refused by the controller (C4's premise)` and `setup: the last block is accepted, closing S6` (controller acceptance refusal), and two scenarios aborted by `Refusal: S6 cannot be closed at manual_close: no accept record of qa-failure-analyst stands for S6-qa-runner-2` (`s6_need_record`, story_run.py:9292).
- story_run_deferred: `FAIL K-D1 S6 closes over the rest with the code-only receipt, and S7 starts afterwards — ([], [('S6',), ('S6',), ('S6',), ('S7',)])`: `manual_close` (story_run.py:11692) now raises the same `Refusal` at its first line, so no `code_only`/`stage_done` move happens and `request.json` of the held case is never written (hence the FileNotFoundError).

Trail: `acceptance.py:1233-1346`; `controller.py:5310-5337`; `story_run.py:9262-9303, 11170-11270, 11692-11719, 11953-11999, 12062-12179`; `test_fixes_13797.py:245-256` (helper `runner`); `test_controller_state.py:32-84, 1955-1983` (`record_stage_acceptance`, `accept_stage`); `test_story_run_s6.py:266-346` (`ManualWorld`, `manual_rig`, `enter_manual`).

Proposed change (all in tests; no package code changes):

C1a. Shared helper `runner()` at `scripts/tests/test_fixes_13797.py:245`: when `complete` is true, write the consumer's accept record for that dispatch BEFORE the `accept` call: insert `if complete: BASE.record_stage_acceptance(root, "S6", dispatch_id)` (the function already exists, `test_controller_state.py:32`, it writes `pipeline.json acceptance.S6` with `reviewed_dispatch`). Expected behaviour: the controller's acceptance gate passes, the S6 derived-scope gate (`controller.py:5323`) is reached again, so the F5 / `10 derived scope` pins see their old texts, and S6 closes. This is also the honest model of the new flow (the record comes from the analyst, the runner's accept follows).
  Proving trial (in-memory): `test_fixes_13797.py` 70/70; `test_story_run_s7_live.py` 44/44; `test_controller_rework.py` 533/533 (both with the patched helper loaded); `test_s7_rejudge.py` 159/161 (leaves only C1b). `test_words_doors.py` uses `FIX.runner` identically (3 keys all via that helper, `test_words_doors.py:1470-1474`); not re-run with the patch (9 min), reading says same.
C1a'. `scripts/tests/test_controller_state.py` before line 1971 (`zero.apply("dispatch", {"id": "late-s6", ...`): call `record_stage_acceptance(zero_root, "S6")` (reviewed_dispatch "" equals the author dispatch the gate computes for a `qa-worker`/no runner dispatch). Trial: 314/314.
C1b. Driver pins that expect the runner's S6 finish to be `True`/`False` (all keys of `test_story_run_s6.py` listed above, `test_s7_rejudge.py` Q9c x2 at its `s6` completion rule): the new expected value is `OpenWork(unresolved="stage_awaits_acceptance")` (`story_run.py:9268 s6_awaits`) wherever the old value was `True` or came from `owed`/refused/held; `False` stays where `manual_scope` is non-empty (an earlier block, `:11255`). One shared way: compare `getattr(value, "unresolved", value)`. Keys: every `FAIL` line of `test_story_run_s6.out` / `each_s6.out`.
C1c. The fake-controller close sites (`ManualWorld` in `test_story_run_s6.py:266`, used by `test_story_run_deferred.py`): before a close that is meant to go through (`manual_close`, `s6_reentry`), write the analyst's accept record for the world's last accepted runner dispatch into the task root `pipeline.json` (same `record_stage_acceptance`, with `reviewed_dispatch` = that id), so `s6_accepted_pending()` (story_run.py:9279) is true. Proving keys: `K-D1 S6 closes over the rest...` and the scenario end `request.json`; `entry 3: the reduction FIRST, then the code-only receipt, then the close`. NOT trialled: the s6 file has dozens of pins to re-express; the form of the new value is a test-author choice (see fork).

Fork (C1b/C1c): either keep the shipped S6 table and re-express the pins (recommended, because the file then tests the shipped flow and the already-green `test_stage_acceptance_consumer.py` proves the consumer side), or run these driver pins with `acceptance.consumer_of` stubbed to `""` (the "world before X7-6", `story_run.py:9264`), which keeps old pins but tests a world that no longer ships. Recommendation: first.

Side findings of C1 (for the Lead, not fixed):
1. `controller.py:5311-5313` comment ("INVARIANT: a stage without `acceptance_by` (S5-S8 ...) is refused nothing new") is stale: S6 has one now. Doc-only.
2. The acceptance refusal (`:5315`) runs BEFORE the S6 derived-scope refusal (`:5323`). A runner finish with `stage_complete: true` and no record now gets the acceptance text and never the "manual half undispatched" text; both fixtures that pinned that text (F5, `10 derived scope`) must write the record first (C1a). I did not judge whether the order is wanted; it is consistent with the runner never closing S6 in the new flow.

### C2. `fixtures/driver-layers.json` has no rows for 8 new Driver methods (class B)

Touches S5-S9: yes (S6/S7 methods) but data only.
Key: `FAIL L1 holds on the real driver (8 problem(s))`: `Driver._wait_then_critic` (story_run.py:14775), `Driver.s6_accepted_pending` (:9279), `Driver.s6_awaits` (:9268), `Driver.s6_consumer` (:9263), `Driver.s6_need_record` (:9292), `Driver.s7_consumer_completion` (:12157), `Driver.s7_consumer_settled` (:12181), `Driver.ticket_rerun_critic` (:14781).
Trail: `test_driver_layers.py:306-336` (L1 census both ways), `fixtures/driver-layers.json` neighbours: `Driver.stage_acceptor`, `stage_critic_route`, `stage_review_exhausted`, `s6_reentry`, `s7_repairs`, `s7_retriage_once` are `driver_stages`; `Driver._act_wait_existing_job` is `driver_machine`.
Change: add 8 rows to `names` of `scripts/tests/fixtures/driver-layers.json` (`kind: method`): the 7 methods s6_*/s7_consumer_*/`ticket_rerun_critic` -> `home: driver_stages`; `_wait_then_critic` -> `driver_machine` (it calls `_act_wait_existing_job`, which is machine; a `driver_stages` home would make an upward edge).
Proof (in-memory trial, rows appended): `test_driver_layers.py` 52/52 (L2/L3 stay 0 problems).
Fork: homes are "a judgment (rules R1-R7 of the t-301 draft)" (the test's own text). I applied the neighbours' homes; the Lead may choose differently. Recommendation as above.

### C3. The strategist's charter no longer carries the word `P19` (class A)

Touches S5-S9: no (S3 charter).
Keys: `test_question_branches.py` `FAIL the strategist's charter carries every key — expected [], got ['P19']` and its negative control `... expected ['`impossible_key_t227b`'], got ['P19', ...]`; `test_oracle_provenance.py` `FAIL t-227b DOC-WITNESS ... got [('agents/qa-test-strategist.md', 'P19')]`.
Trail: pins `test_question_branches.py:1775` (`agent_keys`), `test_oracle_provenance.py:335` (`T227B_KEYS`); `agents/qa-test-strategist.md:25` now says "lowest rung that can observe it, on the manifesto ladder ... Witness: `test_level_rationale`, `question_refs`" and `:54` "The manifesto ladder answers only the LEVEL"; `P19` occurs in no strategist file (checked: strategist charter, its slice, `ahead-cards.json` strategist card = False, positive control: the same search finds P19 in `qa-case-critic` card). The refusal texts still say "P19 rung" (`planning_contract.py:1851`, `branch_accounting.py:1509,1520`). A precedent of moving a pin with the text is in the file: `T227B_KEYS` line 334 "moved charter -> card (t-1685 N3)".
Change: replace the key `"P19"` by `"manifesto ladder"` (the charter's own word) in `test_question_branches.py:1775` and `test_oracle_provenance.py:335`.
Proof (in-memory trial): `test_question_branches.py` 707/707; `test_oracle_provenance.py` 256/256.
Fork: alternatively add "P19" to the charter (S3 text, role-facing). Recommendation: change the pin: "P19" is a number of this repository's owner principles (PROJECT.md), a role in a customer project cannot resolve it; and the exit refusal text still names it at the moment it matters. Sibling noticed: the refusals above tell the role "P19 rung" without a pointer (FR-1/FR-6 question for the Lead, not in scope).

### C4. `references/artifact-contract.md` tree does not list `work/retro-numbers.json` (class B)

Touches S5-S9: yes, S9 inputs (doc only).
Key: `FAIL S9 inputs: 'work/retro-numbers.json' is a name artifact-contract.md documents`.
Trail: `stages.json:300-305` (S9 input `work/retro-numbers.json`, new with the S9 charter: `changelog.d/x7-4-charters-s8-s9.md:5`); `artifact-contract.md:22-28` "Where artifacts live" tree has `ledger.json ledger.md s5-plan.json` but no `retro-numbers.*`; the test builds its token set from exactly that tree (`test_stages.py:42-78`). Producer: `scripts/retro_numbers.py:2828-2829` writes `work/retro-numbers.md`, `retro-numbers.json`, `estimate-facts.json`.
Change: in `ai-packages/qa-factory/references/artifact-contract.md` line 27 add the token `retro-numbers.json` (and, as a sibling, `retro-numbers.md`, `estimate-facts.json`, which the code also writes) to the `work/` list. The doc is sliced per role: regenerate the slices with `scripts/contract_slices.py` write mode afterwards, or the freshness tests (`test_contract_slices.py`) go red.
Proof (in-memory trial adding the token): `test_stages.py` 126/126.

### C5. The map names key pages for 7 roles, the pin says 4 (class A)

Touches S5-S9: yes, S8/S9 roles (test pin only).
Key: `FAIL X1-7: the map names a key page for exactly the four roles — expected ['qa-case-designer', 'qa-requirements-tester', 'qa-scout', 'qa-test-strategist'], got [... + 'qa-bug-reporter', 'qa-doc-scribe', 'qa-retro-analyst']`.
Trail: `test_contract_slices.py:446-450`; `references/inject-map.json` and `references/slices/{qa-bug-reporter,qa-doc-scribe,qa-retro-analyst}/handoff-keys.md` exist; `contract_slices.py:449 keys_targets` reads the map. The commit `8ae68ce` (stage-joints pointers) is the sibling in the same wave.
Change: `test_contract_slices.py:450` expected set = the four plus the three; and (optional, not red now) extend the per-role anchor loop (`:453-458`) to the three new pages for `## Outputs`, `## Witness`, `## Handoff form`, generated-header (the `tried[]` rows apply to the four only).
Proof (in-memory trial of the expected set): 220/220.
Sibling not red but worth a look: `SLIM_ROLES` (`:271`) and the `common-rules.md` roles marker (`:344`) still hand the three new charter roles the `Turn economy` / `Gates and halts` sections; whether the S8/S9 charter roles should drop them like the four is a role-facing decision, not mine.

### C6. `test_brief_pack_manual.py`: the manual runner brief grew by 19 B and lists 3 trimmed input files instead of 4 (class A + a fork)

Touches S5-S9: yes (S6 brief).
Keys: `FAIL K1 the brief is within the ceiling — 6813` (pin `MANUAL_BUDGET_BYTES = 6794`, `test_brief_pack_manual.py:67`, comment: "dense (measured, 0 slack); a raise past it is named in a verdict (AR-20)"); `FAIL K2 the manual brief without its section differs ... got ['-- 3 input file(s) - read qa-factory/artifacts/TP1-12586/work/briefs/S6-qa-runner-2-files.md']` (pin `:241` says `4 input file(s)`).
Trail: I dumped both briefs (`bpm_manual.md`, `bpm_auto.md`): the manual brief has 1 inline door (`work/automation-manifest.json`) and a side file with 3; the automated brief lists 4 files inline. The S6 file list is `stages.json` S6 inputs (2) + `brief_pack.py:91 ROLE_FILES["qa-runner"]` (2) = 4 total today. The pin counts 5 total, so one input file left the list at some point; I cannot say which or why: there is no history in this clone (class D for the "why", A for the count).
Change: `test_brief_pack_manual.py:241` `4 input file(s)` -> `3 input file(s)` (measured). The ceiling (`:67`) is a SHRINK-ONLY ratchet (AR-20): fork between (a) raising it 6794 -> 6813 with a verdict naming the raise, (b) cutting 19 B from the brief text. Recommendation (a), because the brief grew with the charter wave and the cut would change role-facing text.
Not trialled (needs a decision on the fork).

### C7. The plan critic's brief no longer names the rubric («On the plan») (fork: A or C)

Touches S5-S9: yes (S5 plan-critic brief).
Keys: `FAIL the plan critic: the rubric section — 'code-review-rubric.md' not found in: <brief>` and `FAIL ... the section of the rubric — '«On the plan»' not found in: <brief>` (`test_brief_pack_s5_plan.py:98-99`).
Trail: `brief_pack.py:1668-1672` (`plan_dispatch_lines` appends the rubric line LAST in `files`); `:3423-3444` the over-ceiling fallback trims `files` from the end, keeping only "doors" (`ROLE_FILES` names starting `project:`/`plugin:`, plan-slice lines, the automation-manifest line). The rubric is not a door (`ROLE_FILES["qa-code-critic"]` has no `plugin:` entry; the comment at `:3433` even says "not the review form or the rubric"). My dump `bps_critic.md`: "Read these files" holds the plan, the review form and the manifest line, "9 input file(s)" moved to `...-files.md`; the brief is over the 6144 B budget, so the rubric pointer is the first line trimmed. The rubric IS still injected into the critic's prompt (`inject-map.json:70`), so the role still has the text, only the pointer to its section is gone. Why the brief now exceeds the ceiling (what grew: the Commands card, `The rules code will apply`, ...) I could not establish without history (D).
Fork: (a) make the rubric line a door in `brief_pack.py:3431-3437` (code; role-facing, costs bytes, the brief goes further over the ceiling), (b) drop/relax the two pins because the rubric is injected (pin change), (c) find and shrink what grew. Recommendation: (a), because FR-2 ("a door never goes") is the stated rule for a pointer a role needs and the plan critic's whole review form is that section. Not trialled.

### C8. `test_story_run_refusals.py`: the S4 critic's finish is no longer a pure function of the digest (class A for the first key; the rest is unmeasured, D)

Touches S5-S9: no (S4, the X2-7 stage-critic wave, older than the S5-S9 charter rewrite).
Evidence: the supplementary run died at `refusal_c2_4_s4_keeps_open_only_when_the_round_will_run`, test line 3423 `rule(digest)` -> `story_run.py:9494 complete` -> `:9498-9501`: with `stage_acceptor("S4")` set (stages.json S4 `acceptance_by: qa-case-critic`) and no `driver.last_dispatch`, it goes to `stage_review_exhausted` -> `no_move` -> raises `Person("the saved result of the S4 case critic carries no dispatch id, so its form cannot be found ...")`. The pins `F-3 ... the old False`, `T18`, etc. (`:3423-3444`) predate this (they test the "no acceptor" world, `:9510`).
Change (test): give the fixture a dispatch id and a handoff form with a verdict word (`work/handoffs/<id>.yaml`, `header.verdict`) so `stage_verdict_known` and `stage_acceptance_write` pass, or run the scenario with `driver.stage_acceptor = lambda s: ""` for the pins that mean the pre-X2-7 world. Proving key: that scenario's `F-3`/`T18` lines. Fork: which of the two; recommendation: build the form (tests the shipped table).
Unmeasured: after this abort the rest of the file's scenarios did not run. A per-scenario re-run (`each_scenarios.py test_story_run_refusals`, scratch `each_refusals.out`) was in progress when I wrote this report; whatever it prints after this point is class D until read. CI says only "exit 1 (conductor: continue)".

## 3. Needed beyond the manifest
`controller.py`, `acceptance.py`, `story_run.py`, `brief_pack.py`, `stages.json`, `inject-map.json`, `driver-layers.json`, other tests (`test_controller_stage_acceptance.py`, `test_stage_acceptance_consumer.py`), `changelog.d/x7-4-charters-s8-s9.md` (read freely; the manifest named only the tests, the finding and 8ae68ce).

## 4. Trail: every command run
- `git -C <clone> show 8ae68ce --stat` and `show 8ae68ce` (stage-joints pointers).
- `pwsh -NoProfile -File C:\AI\Factory\gm3-1-scratch\run_all.ps1`: runs `python -B <test>` for the 16 files in order, 360 s cap each, stdout/stderr to `<file>.out/.err`, results in `summary.txt`:
  refusals OVERCAP; words_doors OVERCAP; deferred exit=1 28s; s7_rejudge exit=1 38s; controller_state exit=1 35s; contract_slices exit=1 10s; stages exit=1 8s; s7_live exit=1 32s; s6 exit=1 228s; controller_rework exit=1 37s; driver_layers exit=1 51s; question_branches exit=1 40s; brief_pack_s5_plan exit=1 67s; brief_pack_manual exit=1 9s; fixes_13797 exit=1 17s; oracle_provenance exit=1 11s.
- Supplementary (outside the spec cap, labelled): `pwsh -File run_long.ps1` = `python -u -B` of words_doors (exit 1, 572 s, 3 FAIL) and refusals (exit 1, 983 s, aborted at line 3423); outputs `long_*.out/.err`.
- Diagnostics: `diag_s7live.py` (prints the controller answer of the seeding `rework`); `each_scenarios.py test_story_run_s6|test_story_run_deferred|test_story_run_refusals` (one scenario at a time, keeps going after an exception).
- In-memory trials (`trial.py <test> <repl.json>`, `trial2.py` for a patched helper module): fixes_13797 70/70; s7_live 44/44; controller_rework 533/533; s7_rejudge 159/161; controller_state 314/314; driver_layers 52/52; question_branches 707/707; oracle_provenance 256/256; contract_slices 220/220; stages 126/126. The briefs dumped by `trial_bpm.json` / `trial_bps.json` patches (`bpm_*.md`, `bps_critic.md`).
- Positive control of a negative search: `ahead-cards.json` P19 per card printed `True` for qa-case-critic and `False` for qa-test-strategist with the same expression.
- Hygiene: some of my Bash calls carried a `cd` prefix by mistake (non-persistent shell, no effect on files); nothing in the package or `yml-text-factory` was written.
