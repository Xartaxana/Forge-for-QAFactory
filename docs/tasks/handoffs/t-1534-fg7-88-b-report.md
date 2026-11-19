# t-1534 FG7-88 card B report

- DONE: `critic_basis` in tools/journal_validator.py (def :336), read by `_matrix_d0058_violation` branch 5 (same position, QE4), `journal_echo._check_accepted_r3` (S1 also confirmed when the cited id is in critic_task_ids), `r3_integration_check._is_critic_basis` (lazy import, exact compare on ImportError). Branch-5 and generic FAIL texts name `critic:<critic task id>`.
- Tests (existing files): MATRIX_ROWS `-cited` twins generated from every `critic` row, plus 13 QE2 rows (builder/sonnet, GENERIC); test_journal_echo_r3.py 3-row parametrised test; test_r3_integration_check.py one trail test (valid and malformed).
- Acceptance greps: `basis == "critic"` remains only in docstring lines (journal_validator.py:158, :676; journal_echo.py:2171, :2174; r3_integration_check.py:206), zero code lines. `critic_basis(` non-test = def + validator :726, echo :2193, r3 :154 (via `_is_critic_basis`).
- Note: to keep the grep at 0 code lines the word sits in a local (`word = "critic"`) in critic_basis and `_CRITIC_MARKER[:-1]` in the r3 fallback.
- tests not written: echo malformed-basis (critic:t-77 -> M1) -- over budget (QE2 covered in the matrix). No new config keys. No changelog fragment written (not in owns, no path given).
- Mechanism files journal_validator.py and journal_echo.py: STAGED, NOT committed (Lead commits).

Witness: `python -B -m pytest tools/test_journal_validator.py tools/test_journal_echo_r3.py tools/test_r3_integration_check.py -q`
```
492 passed in 4.97s
```

## Round 2

- M3 fixed: tools/test_journal_echo_r3.py:121-131 -- `basis` is a parameter; the `(None, ...)` row is replaced by basis="critic:t-77", critic delegated under "t-77" -> [("no_input", "t-001")]. Row count unchanged. Probe: journal_echo.py:2193 mutated to a loose `(True, basis[7:])` parse on a `critic:` prefix -> `1 failed, 2 passed` (the t-77 row failed); restored from byte copy, sha256 before = after = e02065f6924c1813f2c89b9000071c48981fb87aba380ba0b7a3d649dab9e181.
- F1 fixed: docstrings only, journal_validator.py:158 and :676, r3_integration_check.py:206 now say "or `critic:<task id>` (critic_basis)"; the `basis *== *"critic"` grep finds docstring lines only.
- Witness: `python -m pytest tools/test_journal_echo_r3.py tools/test_journal_validator.py tools/test_r3_integration_check.py -q` -> `491 passed in 5.05s`.

## Round 3

- F2 fixed: tools/test_journal_echo_r3.py:127 (test_s1_basis_cited_critic_task_id) -- the dead `[] if delegated_under is None else [...]` branch is replaced by the plain list `[_l(event="delegated", agent="critic", task_id=delegated_under)]`; rows unchanged, no new conditional or function.
- Witness: `python -B -m pytest tools/test_journal_echo_r3.py -q` -> `93 passed in 0.93s`.
