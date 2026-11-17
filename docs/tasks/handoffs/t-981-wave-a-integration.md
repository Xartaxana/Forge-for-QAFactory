# t-981 wave A integration (builder report)

## Step 1 merges (worktree wave-a-int, branch wave-a/integrate)
Order: T6 (a10fec4f), T7b (abd9ee64), T4a (a201e90f), T5r (a150f367), one --no-ff commit each.
test_detector_verdict.py conflicted on T6, T7b, T4a (both sides kept, marker lines removed, blank-line separation fixed,
main() calls kept in order t7c, t6, t7b, t4a); T5r merged clean. No other file conflicted.
After each resolution: T6 606/606, T7b 637/637, T4a 743/743, after T5r 743/743.

## Step 2 pins
`stage_joints.py --check` printed `unsited 46` (= the critic's 46). Set to 46: `told_ratchet.unsited` (stage-joints.json),
`UNSITED_CAP` (test_stage_joints.py:927) and the K12 expected tuple (line 932; the tuple also held 119 literals, moved too).

## Step 3 causes
- rows-for/real 114 -> 108: cause commit 442ae9de (14.11, "K10 pay-down K2: rows told exactly to the roles whose contract a check
  can judge"); measured per commit with rows_for("qa-runner",["*"]) on the file as of each commit: 7ed7f103 114, 1db4ec9f 114,
  60ddb66d 114, 8d71532b 115, 442ae9de 108, HEAD 108. Change intended by its commit message -> pin and "(114 today)" moved to 108.
- K1 units_no_row 1: the unit is `project_decisions.py::_load` (method), added by 25e0764e (17.11, rules-debt S8 X9, t-951);
  b0bfeab0 (t-975) reworked it. Census row added in the form of its neighbours:
  `{"file":"project_decisions.py","function":"_load","class":"shape","roles":["conductor"],"owner":"data"}` in
  scripts/tests/fixtures/judgment-census.json (OUTSIDE the declared owns; the step named adding the census row). Not a lost row.
  Class/owner (shape/data) is my reading of the neighbours; the Lead/critic should confirm it. No ratchet number was touched; whether
  `blocking_per_role.conductor` should rise for the new row was not checked (test_judgment_census.py not run, slow/other owner).

## Step 4
tools/test_hygiene_gate.py:348: `f'grep "journal_write.py accept" f'` -> `'grep "journal_write.py accept" f'` (f prefix only).
`lint_ratchet.py --check` still reports 1 new, NOT mine: `test_s5_precheck_sides.py:846: Plan row: TS-1 [HandReaderInput]`
(the f-string finding at test_hygiene_gate.py:348 is gone from the list).

## Witness (single run of test_stage_joints.py, taken BEFORE the K12 tuple edit at line 932; the K12 FAIL line shows got (46, 46, 46, [], True), which is the tuple now written)
- test_stage_joints last line: `=== test_stage_joints: 338/340 ok ===` (the 2 FAILs: K12 tuple, now fixed; K5/real, below)
- NEW RED, not fixed (outside the pins): `FAIL K5/real: the rows of the real file that state a requirement name every role of their unit`
  got 17 units met by roles no row names: handoff_check.py::_binding_problems, ::check_findings, validate_artifacts.py::check_behaviour_claims,
  check_bug, check_bug_filing_header, check_bug_form, check_case, check_case_form, check_cell_counts, check_delta_column,
  check_manifest_reuse, check_register, check_requirements_review, check_then_oracles, check_understanding. It comes from the wave A rows
  (T6/T7a/T7b siting); review K5 / "EC-8 lines go to TBW-T1rc" is the owner. Rows-for and K1 pins are green in this run.
- test_detector_verdict last line: `=== test_detector_verdict: 743/743 ok ===`
- stage_joints --check: `stage joints: walked exit 8, detector 5, window 27 | rows 267, gaps 4 (producer 2, told 1, demands 1), joints held 4 of 267 | role leg not walked (code-to-code rows): 26 | stages with no detector: S0, S1, S6, S7, S9 | told counters: hand_cards 12, legacy_legs 0, unsited 46` then `stage joints: clean`
- lint_ratchet --check: `lint ratchet: 77 findings, 76 in the baseline, 1 new, 0 stale (pyflakes 3.2.0)` (the 1 new is test_s5_precheck_sides.py:846)

## Noticed outside owns
- judgment-census.json edit (above); K5/real red; lint new finding in test_s5_precheck_sides.py:846.
- Not re-run after the line-932 edit (one run allowed); the number is taken from the failing run's own output.
