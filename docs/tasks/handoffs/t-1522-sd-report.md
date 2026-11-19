# t-1522 S-D report: `mutants` in the critic verdict checker

Base origin/main e3ed349b (merge: already up to date).

## Plan items
- Behaviours 1-7 DONE: `_mutant_errors(obj)` called from `validate_verdict` (tools/critic_verdict_check.py).
- Schema mirror DONE: `mutants`, `mutants_none` properties, `mutants` required (tools/critic_verdict.schema.json); joins are checker-only, said in the description.
- MUTANT_ROWS DONE: 28 rows, one parametrised test, all four test rows of the card (tools/test_critic_verdict_check.py).

## Fixtures that gained mutants (E-D1)
`_base_fit` gained `mutants: []`, `mutants_none: "no new behaviour: fixture"`; `_base_fit_with_fixes` and `_base_blocker` inherit it. No assertion was weakened or removed; only fixtures grew.

## Witness
`python -m pytest tools/test_critic_verdict_check.py -q` -> `73 passed in 2.97s`
`python -B tools/registry_preflight.py check lint --paths tools/critic_verdict_check.py` -> `registry preflight: lint ok (0.5 s)`
Budget: test +87 lines, code +174 (+25 schema).

## Decisions / notes
- Run join with duplicate reruns commands: passes if ANY joined rerun has the outcome word (no false-refuse).
- `mutants_none` present (non-null) with non-empty `mutants` is refused; non-list `mutants` gives one diagnostic.
- Green-control diagnostic is one line (first uncontrolled --test value), not per value.
- Diagnostics quote rules 17 and 21 as the card writes them; critic.md not landed (E-D5: merge waits for S-B).
- Row 'restore-mismatch in blocker' covers the blocker-link PASS case.

## Mechanism / staging
critic_verdict_check.py and schema.json left STAGED for the Lead; test file and report committed.

## Analogs seen
None outside owns. dup-baseline.json not checked (only lint run). No changelog fragment required by the dispatch.

## Round 2

- S-D-1 fixed: tools/test_critic_verdict_check.py::MUTANT_ROWS row "restore-mismatch no door" now names the target (fix "F2 restore tools/x.py by hand") but lacks `show HEAD:`; the "no target" row is kept. Red-before: with the `and "show HEAD:" in hits[0]` line deleted on a byte copy, `pytest -k door` -> `FAILED test_mutants_rows[restore-mismatch no door]`, 1 failed; restored by byte copy, sha256 0c1cab62d19ee880 equal before/after.
- S-D-2 fixed: tools/critic_verdict_check.py _mutant_errors split into _one_mutant (per item), _survivor_errors, _restore_errors; bodies moved verbatim, diagnostics unchanged; max nesting 3.
- Witness: `python -m pytest tools/test_critic_verdict_check.py -q` -> `73 passed in 2.01s`.
