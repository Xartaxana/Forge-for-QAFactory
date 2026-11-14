# Wave 9 integration report (t-720)

Base: origin/main ae41e2b (wave 8). Branch `wip/wave9`, pushed to main.

## Merges (all `--no-ff`, no conflicts, none skipped)

| order | branch | node / task | merge hash |
|---|---|---|---|
| 1 | wip/fv1-9-fix | FV1-9 N1+N2+N4+N5 + fix round (t-710) | ec7b838 |
| 2 | wip/fv130b-n5 | FV1-30b N5 (t-705/t-715) | facd5d1 |
| 3 | wip/fv130b-n4 | FV1-30b N4 (t-704/t-715) | 2a88226 |
| 4 | wip/fv123-a14 | FV1-23 A-1+A-4 (t-712) | b9dd7d0 |
| 5 | wip/p1v-fix2 | P1-v N6+N7+N6b + fix round (t-714) | 5d28c89 |

Known meeting points (test_detector_verdict.py, stage_done.py, driver_dispatch.py, role-load.json, selftest.py, conductor.md) merged automatically.
`conductor.md`: `wc -c` = 11897 bytes (<= 12000).
`changelog.d/`: fragments of all sides kept, no assembly.

## Verification (edge 2), each file one run

- `python -B scripts/selftest.py --limits --lang`: `PASS limits: ...`, `PASS lang: no Cyrillic anywhere in the package`, `=== qa-factory selftest: 4/4 ok ===`
- test_judgment_census.py: `=== judgment_census: 25/25 ok ===`
- test_question_register.py: `=== question_register: 878/878 ok ===`
- test_then_remainder.py: `=== test_then_remainder: 354/354 ok ===`
- test_detector_verdict.py: `=== test_detector_verdict: 210/210 ok ===`
- `python -m pytest experiments/measurers/test_measurers.py -q`: `282 passed in 7.31s`
- `tools/architecture_index.py --check`: `architecture index: up to date (29 invariants, 2682 bytes)`
- `tools/factory_rules_index.py --check`: `factory rules index: up to date (59 rules)`
- test_audit_rules.py, first run after merges: `=== audit rules (...): 371/375 ok ===` (A22, A-K1, A22-K4 x2 red: qa-requirements-tester 12,670 vs ratchet 12630; process 11,320 vs 11280). After the named raise below: `=== audit rules (A1/A9/A11/A13/A14/A17/A20/A21/A22/A27): 375/375 ok ===`.

## Named raise (AR-20)

Cause measured: a detached worktree at 2a88226 (after merges 1-3) gave `375/375 ok`; the red appears only with merge 4. Branch `wip/fv123-a14` (FV1-23 A-4) adds one line to `agents/qa-requirements-tester.md` ("Before you write a question, read the bundle's sources on its topic ..."), growth exactly 40 tokens on both counters.

- `references/role-load.json` `ratchet_tokens` `qa-requirements-tester`: 12630 -> 12670 (branch wip/fv123-a14)
- `references/role-load.json` `process_ratchet_tokens` `qa-requirements-tester`: 11280 -> 11320 (branch wip/fv123-a14)

No other ratchet row changed. No row was raised to hide a lost row.

## Status lines

`plans/piles/live-run-fvf/batch-1-live-run-fvf.md`: FV1-9 `принято: ec7b838 (t-720)`, FV1-30 `принято: 2a88226 (t-720)`, one «Ход» line (FV1-23 partial, status unchanged).

## Cross-branch duplicates

None seen. Note: the FV1-30b branches and the others carry the same wave-8 role-load/slice differences vs ae41e2b only because they were based earlier; the merges kept main's values.

## Pipeline

See the handoff message (read after push).
