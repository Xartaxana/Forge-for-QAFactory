# TD-15 walk fix round - builder report

Branch `td/15-walk-fix`, one commit. Items 1-5, 7, 8, 10-15 DONE; 6 PARTIAL; 9 DONE. Slips: a few Bash calls began with `cd` or used a python heredoc to edit a test file (hook warned, nothing blocked); I used a long `until`/sleep loop once (moved to background), contrary to "no waiting loops".

## Items
1. DONE one vocabulary. `scenario_walk.py:41-49` (`APPROVE/REFUSED`, `GATE_ACTIONS`, `QUESTION_KINDS`, `START_ARGS`), `decision_of`, `question_kind_of` (~l.320). `story_capture.expected()` imports the walker by path (`load_walker`) and writes `decision` in the token plus `recorded_action`; `question_kind` written as the door returns it. Unknown action: refusal naming action, `seq N`, `GATE_ACTIONS`; no expected.json written. Test: `test_expected_vocabulary_and_form_inputs` + 3 walker rows.
2. DONE `expected.handed` = `walker.required_inputs(form of the accepted dispatch)`; same function the walker's `door_handed` uses. Form absent: `[]`. Reading of "the next stage's handoff form": the form of the stage's accepted dispatch (which hands to the next stage), the one the walker reads.
3. DONE `not_walked` from `expected()`: one row per (stage, facet, reason) with `count` and `samples` (<=3). Test `test_not_walked_is_one_row_per_stage_facet_reason`. The walker prints the count.
4. DONE `door_handed`: template path and folder -> `NOTE ... not comparable`, no fail; real file named and absent still fails by name (existing row); start args from the first recorded dispatch of the next stage (`start_args`: `--execution-kind`, `--purpose`, `--scope`); auto cut before that dispatch (`_cut_of`); form with no required inputs -> `[]` + NOTE; no next -> no carrier. Rows in `test_scenario_walk.py`.
5. DONE cap counts run files only (`OWN_FILES`), refusal text says so and names the 5 largest. Note: in the unchanged code the check already ran BEFORE the tool's own files were written; what counted them was the printed `size` - now run files only too. Test at cap / one byte over: `test_cap_counts_run_files_only_and_is_exact`.
6. PARTIAL speed. Measured (loaded machine, other workers running; absolute seconds noisy): copy_world was 351 of 482 s (13 calls, 27 s each); `shutil.copy2`'s copystat was two thirds of a 424-file copy (16 s copy2 vs ~5-9 s copyfile+utime). Done: `_copy_file` (copyfile + utime, the recording's ages kept), world hashed once per facet instead of twice, cut worlds built once per walk and copied per facet (`_facet_copy`; test shows one build, no leaked write). Not reachable: each `handed` facet has its own cut (no sharing) and a real `story_step start` (47-76 s each under load).
   Before (13 facets walked): build_world 24.7; S1 39.0, S2 30.9, S2/handed 93.0, S3 56.0, S4 27.3, S5 24.6, S6 20.0, S7 25.4, S8 26.7, S9 21.8, gateA 34.2, gateB 32.7, S8/delivery 50.2; facets 481.7 s, wall 586 s.
   After (19 facets, incl. 7 new `handed`): build_world 7.9; accepted facets 12.6-26.7 (S1 26.7, S2 19.8, S3 24.8, S4 21.0, S5 15.5, S6 17.3, S7 13.0, S8 12.6, S9 14.8), gateA 24.0, gateB 16.9, delivery 29.0, handed S2 75.5, S3 57.6, S4 67.0, S5 76.0, S6 57.3, S7 59.1, S8 47.0; facets 674.8 s, wall 734 s. The 13 comparable facets: ~482 s -> ~330 s. Still far over 60 s on this loaded box; a story with 7 real starts cannot meet it.
7. DONE `expected` re-run through the tool; walk and reasoned `not_walked` rows re-applied by a scratch script (the tool's `expected()` rewrites `story.json` `not_walked` whole, so a re-run loses hand rows - not fixed). Hand edit of the decision token dropped. See result below.
8. DONE `BN`, `RUN` in `exclude` of `ticket-key` AND of the `jira-key` scan rule (`tools/story-scrub-rules.json`); test `test_ticket_key_keeps_the_runs_own_ids_and_rewrites_real_keys` (BN-10, BN-11, RUN-2026 kept; TP1-13797, ABCD-123 -> REF-n).
9. DONE sha256 follow is a fixpoint (`FOLLOW_PASSES = 5`; a file changed by a remap chains its own old->new hash; after 5 changing passes the 6th changing pass refuses naming the files). Test `test_hash_follow_is_a_fixpoint` (raw -> ticket -> inventory). Refusal path not covered by a test.
10. DONE `--purpose` in `START_ARGS`; `cut_before_seq` may be a map facet -> seq (`story_cut`; omitted facet = uncut; variants of such an entry read the key `variant` - my choice, say if you want another). Rows added.
11. DONE `recorded_config` + `_carry_project_config`: `state/config-at-start.json` `bytes_b64` is written as the world's `qa-factory/config.json` in `build_world` and every `copy_world`, before any projection; `_pinned` calls `contract.case_config_reset()`. No recorded config: template + NOTE `<story>/world/config`. Result: S6 accepted and gateA decision are GREEN.
12. DONE `door_exit_gate` runs inside `exit_gate.holding_stage(stage)` and `holding_dispatch(accepted dispatch)`. The UNREADABLE line is gone; but now S2 shows real `branch_accounting.py` refusals (see below).
13. DONE `door.skip_detectors` (data, in story.json) filters `check_coverage.py:` lines (`without_detectors`); cart-1 S8 accepted carries it plus a `not_walked` row with the reason. The rest of S8 accepted is walked: PASS.
14. DONE re-walk of the eight green facets under the recorded config: S1 PASS, S5 PASS, S7 PASS, S9 PASS, S2/handed.. all `handed` PASS, gateB PASS, S8/delivery PASS; S4/accepted TURNED RED (new, below). Zero-checks question: I could not count checks (`all_errors` returns `passed` empty for every facet, probe: 0 on all nine), so "has something to check" is NOT established for S1, S5, S7, S9; only observable difference config makes: template vs recorded gives S4 red, S6 green, S8 vs template -1 refusal. Reported as unknown, not as fact.
15. DONE `capture` reads the version from the run: `pipeline.json` `run_mode.plugin_version` (else "unknown"); cart-1 `story.json` now `0.10.6`. Test `test_story_version_is_the_runs_not_the_packages`.

## cart-1 now
Summary `=== scenario cart-1: 16/19 ok ===`. FAIL lines (3, were 5): `cart-1/S2/accepted`, `cart-1/S3/accepted`, `cart-1/S4/accepted`. Now green: S6 accepted, S8 accepted (without the coverage part), gateA decision. S4 accepted is newly red. Every `handed` facet S2..S8 PASS.

### Full refusal of S2 accepted (after W1/W2; each ` | ` part)
- 9 x `requirements-register.md: R-n is implementation-only and has no behaviour claim - it is derived from the diff, the current code or another test alone (no ticket source speaks to it), so what it says is a claim about the code, not a requirement. Add a row under "## Behaviour claims" (R-n | before | before_ref | now | now_ref | differs | question): what the behaviour was before the change, what it is now, and the question that asks the person which one is expected` for R-3, R-6, R-7, R-9, R-10, R-12, R-13, R-14, R-15.
- NEW, not in the critic's list: `branch_accounting.py: the register has no ## Branches section - fix: add it (a table of the branches, or Branches: none -- <why>; see the register template)` and 8 x `branch_accounting.py: U-<id> (CART-1 description|description/criteria): "<text>" has no home - fix: add | U-<id> | R-n | to ## Source obligations (or BN-n, not_obligation: <why>, excluded: Q<n>(<letter>): <why> or excluded: "<their words>" (<file>.txt): <why>)` for U-526e0087cc3f, U-b0d4e12eb722, U-7b6bb85e78bc, U-c6975e4b5070, U-6b74c58758ef, U-d47a36f4f055, U-09e5f12b2d69, U-921223d02bf7. Probably another post-0.10.6 contract (branches / source obligations); not diagnosed - the Lead decides whether it is in the S2 amendment.
### Full refusal of S3 accepted (5 parts)
- 3 x `planning_contract.py: R-n: this requirement of the register has no row in the test plan. Expected: a row that names R-n in requirements in work/test-plan.json and in the R column of test-plan.md. If it waits for a gate A question: disposition: unverifiable, question_refs: ["Q2"] and if_answered["Q2"] with a key for every reading letter (or *) and not_needed; the reading that keeps it in scope sets a disposition that gets a case. If it should not be checked: disposition: skip with the reason, and the person sees that row at gate A. A not_planned entry does not stand in for a row.` for R-9 (Q2), R-13, R-16 (the text carries Q2 for each).
- `planning_contract.py: R-13: the register marks this requirement bug:candidate-defect, and no row plans a test for it. Expected: a row naming R-13 with disposition: automate or manual-agent; or, while a gate A question decides it, unverifiable with question_refs and an if_answered reading that sets automate or manual-agent. When the requirements do not state the expected result: oracle_unknown: true and a question; the current code is never the expected result.`
- `planning_contract.py: The section names no test and no No regression: <reason> line. Expected: Command: plus an item per test path, or No regression: <reason>; silence is not an answer.`
- No UNREADABLE line any more.
### NEW red: S4 accepted (green under the template config, red under the recorded one)
11 refusals (printed cut at 1500 chars; the full door text is reproducible with the scratch script described below): `CART-1_TC_005.md / TC_008.md / TC_010.md: FORM - Then n: R-7 / R-12 / R-10 is implementation-only (derived from the diff, from current-code: or from somebody else's test:, no ticket source and no document speaks to it): a statement read from the code is never a requirement. Use unknown with the question that shows before/now, or person once it is answered` and `FORM - basis 'requirement:R-7' names R-7, which is implementation-only ... Name what the expectation rests on instead (consistency:<where before and now differ> or external:<ref>); each Then says where its value comes from in then_oracles`. Same class as D1 (G2-12 `current-code:` derived rows); I did not write an amendment and did not diagnose beyond the text.

## DoD tails (verbatim)
```
python -m pytest D:/ws1/wt-td\15-walk-fix\tools\test_story_capture.py -q
.............                                                            [100%]
13 passed in 18.33s
python -B ...\scripts\tests\test_scenario_walk.py
PASS witness_for: a keep row that does not cover the path is not named

=== test_scenario_walk: 48/48 ok ===
python -B ...\scripts\selftest.py --limits --lang
PASS limits: SKILL.md / agents / references within size caps
PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier

=== qa-factory selftest: 4/4 ok ===
python -B ...\scripts\tests\test_scenario_cart_1.py  (once, exit 1)
FAIL cart-1/S2/accepted - outcome: expected 'accepted', got 'refused' (requirements-register.md: R-3 is implementation-only ...
FAIL cart-1/S3/accepted - outcome: expected 'accepted', got 'refused' (planning_contract.py: R-9: this requirement of the register has no row ...
FAIL cart-1/S4/accepted - outcome: expected 'accepted', got 'refused' (CART-1_TC_005.md: FORM - Then 1: R-7 is implementation-only ...
=== scenario cart-1: 16/19 ok ===
```
(The first walker test ran 42/42 and 44/44 before items 11-13 were added; the 48/48 above is after the last edit. Tool tests ran 13/13 after the last edit.)

## Seen, not fixed
- `expected()` overwrites `story.json` `not_walked` whole (hand rows lost on a re-run); `expected.json` `refusals` still carry `stage: null` rows (D8), words matched by file-name substring (gateA lists three files).
- `all_errors` `passed` is empty, so "a facet passes with zero checks" cannot be measured from outside.
- `expected()` states `handed` for a form that is absent as `[]`, which the walker then reports as "no carrier".
- Fixtures: story.json of cart-1 has CRLF (git warns on commit).
- Needed beyond the manifest: `scripts/exit_gate.py` (holding_stage), `scripts/story_step.py` (start args), `scripts/contract.py` (case_config_reset), `scripts/handoff.py`, `scripts/tests/harness.py`, the critic verdict `td-15-cart-1-reds.md`, the cart-1 events and `state/config-at-start.json`. Scratch scripts (timewalk, probe, mkstory2/3, fulltext) live only in the session scratchpad.
