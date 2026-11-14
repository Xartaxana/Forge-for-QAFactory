# main-red2 report (2026-11-14)

Red: run 43542858497 on 9c15423, `forge-check` at `lint_ratchet.py --check`: `gate_brief.py:2868 'question_register as QR' imported but unused`.

Cause (not a lost merge): `_help_lines` (b17aeeb, FV1-9 N2) used `QR.origin_words` in its `tail` branch; the F1 (FR-10) fix on the FV1-9 side replaced that with a plain non-blank `from` test (comment in the code), leaving the import. ec7b838^2 already has the import with no `QR.` use inside the function; no side lost lines. Fix: the import line removed, nothing else.

## Witness
- `lint_ratchet.py --check`: `lint ratchet: 76 findings, 76 in the baseline, 0 new, 0 stale (pyflakes 3.2.0)`
- `selftest.py --limits --lang`: `PASS limits: SKILL.md / agents / references within size caps`, `PASS limits: every mandatory role rule ... holds`, `=== qa-factory selftest: 4/4 ok ===`
- `scenario_walk.py --witness-for scripts/gate_brief.py` names many files; fast ones run directly: `question_register: 878/878 ok`, `test_gate_vocabulary: 141/141 ok`, `test_handed_to_person: 58/58 ok`. The scenario tests (cart_1, local_1_*), others not run (slow, judged by canon of the batch).
- ci_read jobs 43542858497 (read at the time of work): changes success, runner-facts success, forge-check failure, package-fast success. No red outside owns.
- Commit pre-commit hooks passed (indexes up to date, WARN ok).

Siblings: none found; lint shows 0 new.
