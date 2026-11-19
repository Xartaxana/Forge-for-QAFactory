# t-1551 FV3-35 part A report

Status: PARTIAL against the "all 14 PASS" DoD and the 57 -> 43 expectation: 8 of 14 rows PASS, 6 reach the key and fail a check. Measured wins (edge rule).

## Cause map (stub override `findings[].cause` in `overrides["s5-critic-to-automator"]`, exits/s5.json)
- s5.nobody_environment/* -> `environment`
- s5.nobody_tooling/* -> `tooling`
- s5.nobody_review/* -> `reviewer_error`

All 14 rows carry the override (the byte-identical copies are split by family).

## Removed from known_red (8, PASS)
s5.nobody_review/review, s5.nobody_review/debt, s5.nobody_review/empty, s5.nobody_environment/fixed, s5.nobody_environment/debt, s5.nobody_environment/empty, s5.nobody_tooling/debt, s5.nobody_tooling/empty.

## Kept in known_red (6, key reached, own measured FAIL text, node still FV3-35; raised_by rewritten)
- s5.nobody_review/stop, s5.nobody_environment/stop, s5.nobody_tooling/stop: "C3: the answer changed nothing: the state fingerprint is the one it was asked at (C3)".
- s5.nobody_review/free words, s5.nobody_environment/free words, s5.nobody_tooling/free words: "C2: a conductor call followed the answer and its why is not on record; C3: the answer changed nothing: the state fingerprint is the one it was asked at (C3)".
The seed now reaches S5 and the key; these are answer-word checks (stop / free words), a different defect from "met the conductor at S5". Not diagnosed here; they need their own node (Lead's call; I did not invent an id).

## Pins
`pins.known_red` 57 -> 49 (measured: 14 FV3-35 nobody rows minus 8 PASS = 6 stay). Spec expected 43; measured wins.

## Row time
No per-row time is printed. Whole run (prefix 190.6 s + 14 rows) took about 25 min wall (20:17 -> 20:42), about 93 s per row on average; no row hit ROW_CAP_EXITS (a cap hit would print as FAIL text; none did). Slowest row time: not measured per row.

## Witness
Command: `( cd ai-packages/qa-factory && python -B scripts/tests/test_scenario_dry_1.py --part exits:s5 --exits-root <temp>/t1551/root --ledger <temp>/t1551/none.json )` (root = 14 nobody rows + real seeds/s5.json). Tail:
```
PASS s5.nobody_review/review, nobody_review/debt, nobody_review/empty
FAIL s5.nobody_review/stop — C3: the answer changed nothing: ...
FAIL s5.nobody_review/free words — C2: ...; C3: ...
PASS s5.nobody_environment/fixed, debt, empty
FAIL s5.nobody_environment/stop — C3 ...
FAIL s5.nobody_environment/free words — C2 ...; C3 ...
PASS s5.nobody_tooling/debt, empty
FAIL s5.nobody_tooling/stop — C3 ...
FAIL s5.nobody_tooling/free words — C2 ...; C3 ...
(6 "known_red — new red" FAILs: the empty ledger, expected)
PASS dry-1/exits:s5/outcomes
=== scenario dry-1: 9/21 ok ===
exit 1
```
`python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check` -> `dry_exits --check: 0 discrepancies` (run after the final known_red edit).
The final known_red edit (restoring the 6 rows) came after the scratch run; it is ledger text only.

## Needed / notes
- Fix the class: the stop and free-words variants of the s5 nobody rows fail C3/C2 in the same way across all three families; likely one cause (same check on the answer step). Needs a diagnosis node.
- No CHANGELOG fragment: fixture only, no product text.
- Scratch under temp/t1551 (script copies edit35.py, mk.py, fix2.py). Nothing left running.
