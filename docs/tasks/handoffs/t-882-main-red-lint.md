# t-882 -- main red lint (controller.py:49 DEFAULT_LIMITS)

Status: done per coordinator answer (option a). Base 352eb40f.

## Grep (Grep tool, case-sensitive, `DEFAULT_LIMITS` over ai-packages/qa-factory and experiments; `\w+\.DEFAULT_LIMITS` over scripts/tests)
- controller.py: only line 49 (the import), no use.
- experiments/: no matches (control: same tool found hits in ai-packages).
- Readers via controller: only test_needs_author.py:355 `CTL.DEFAULT_LIMITS` (line 35 `import controller as CTL`). No other test reads CTL./controller.DEFAULT_LIMITS (the rest use runtime_policy/RP).

## Change
- controller.py:49: removed `DEFAULT_LIMITS` from the runtime_policy import.
- test_needs_author.py: added `import runtime_policy  # noqa: E402` (neighbour form); line 355 now `runtime_policy.DEFAULT_LIMITS["repair_cycles"]`.

## Witness
`python -B tools/lint_ratchet.py --check`:
lint ratchet: 76 findings, 76 in the baseline, 0 new, 0 stale (pyflakes 3.2.0)

`python -B ai-packages/qa-factory/scripts/selftest.py --lang`:
PASS lang: no Cyrillic anywhere in the package
PASS lang: no control byte left by an eaten escape sequence (FR-29)
=== qa-factory selftest: 2/2 ok ===

`python -B -m pytest .../test_needs_author.py` collects nothing (script-style test); ran directly (not in SLOW_TESTS, 3s class):
`python -B ai-packages/qa-factory/scripts/tests/test_needs_author.py` -> `=== test_needs_author: 89/89 ok ===`

## FR pass
A not applicable -- no refusal touched. B not applicable -- no person text. C not applicable -- no contract. D not applicable -- no identity/evidence. E not applicable -- no delivery/report. F not applicable -- no measurement. G: FR-32 root cause = the import became unused at the SC topic-B merge; fixed at the import and its one re-export reader. AR-13 kept (value read through its home).

## Questions: none. Needed beyond the manifest: runtime_policy.py (home of DEFAULT_LIMITS), selftest.py (SLOW_TESTS check).
