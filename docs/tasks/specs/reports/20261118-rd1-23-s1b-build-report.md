# RD1-23 (S1b) build report

Items: 1 DONE (R2 and R3 not moved, see Deviation), 2 DONE, 3 DONE, 4 DONE, 5 DONE.
Files: ai-packages/qa-factory/design/factory-rules-debt.md, design/factory-rules.md (Check lines of FR-5, FR-23), scripts/tests/test_null_outcomes.py (K0.15 block), changelog.d/rules-debt-1-rd1-23-debt-file-second-pass.md.

## Done
- Base check: `acceptable_provenance` is gone from `scripts/profile_contract.py` (only a comment at :913 names it as deleted); RD1-14 k4 (82d54a00) is an ancestor of HEAD. So B-255 moved.
- Moved to "Fixed since this walk" (bullets, B-ids inside; each carrier read in code): R5 FR-23, R7 FR-31, R9 FR-37, X16, W3, X9, X10, G15, X2 residue, R4 FR-22, and all 14 FR-59 gate rows (G1-G13 + environment_property_cover; the registry holds statuses converted/exempt only; the `s5_stand_limits` row was deleted by C3-j2).
- FR-59 section kept with its heading: "Nothing open." The FR-13 walk entry (W1) NARROWED to the Level-vocabulary residue (`contract.PLAN_LEVELS`; `contract.py:605` TRACE_LEVELS; the old line was :594). The W3 walk entry removed (moved).
- Header: "Thirteen rows open" = 4 (run 5: FR-11, FR-16/17, FR-21, FR-23+FR-5) + 2 walk (FR-13 W1, FR-1/2) + 5 (X1 FR-47, X3 FR-48, X4 FR-50, X7 FR-56, X11 FR-6) + 0 FR-59 + 1 FR-42 + 1 FR-7.
- FR-23+FR-5 row: the sentence "Check lines do not name ... yet" replaced by "name the declaration and the detector (18.11.2026, RD1-23)"; the four needles stay.
- K0.15 control re-pointed to the `| FR-21 |` row (>= 1); the main check unchanged.
- Check lines of FR-5 and FR-23 in factory-rules.md name `references/null-outcomes.json` and `scripts/tests/test_null_outcomes.py`.

## B-ids moved (for piles.py close --id)
B-257, B-255, B-217, B-278, B-279, B-221, B-179, B-061, B-280, B-281, B-282, B-283 (also named in bullets as closed history: B-407, B-013). The R5/R7/R9/X16/W3/X9/X10/G15/R4 rows carried no B-id; none invented.

## Deviation / question for the Lead
- R2 (FR-16/FR-17 row) and R3 (FR-21 row) NOT moved. R3: edge E2 and item 3 require the `| FR-21 |` row to stay (K0.15 control, G1-10), and its residue (a skip row whose plan declares no structured gap is never asked) is stated and not closed in code. R2: its row already carries a stated residue (no pytest-shaped command; `s5_precheck._why_no_row`), not closed in code. Both stay open with that residue; spec item 1 listed them as moves. Question: accept that, or name a different close.
- Live-runs rows (R9, R4, X10 proofs owed): not touched (plans/ is outside owns); the bullets name `live-runs/2`.

## Witness
```
python -B ai-packages/qa-factory/scripts/tests/test_null_outcomes.py  -> === test_null_outcomes: 360/360 ok ===
python -m pytest tools/test_piles_close_id.py -q                      -> 7 passed in 5.72s
python -B tools/factory_rules_index.py --check                        -> factory rules index: up to date (59 rules) / (31 rules)
python -B ai-packages/qa-factory/scripts/tests/test_s1_s2_contract.py -> === S1-S2 contract: 67/67 ok ===
python -B ai-packages/qa-factory/scripts/selftest.py --lang           -> === qa-factory selftest: 2/2 ok ===
```
Needed beyond the manifest: docs/tasks/specs/20261117-rules-debt-fix-spec.md (row id map), references/gate-registry.json, the code carriers named in the bullets.
Tests: none added; one control re-pointed (K0.15). Analogs: none noted.
