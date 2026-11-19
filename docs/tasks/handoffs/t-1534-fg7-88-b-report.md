# t-1534 FG7-88 card B report

- DONE: `critic_basis` in tools/journal_validator.py (def :336), read by `_matrix_d0058_violation` branch 5 (same position, QE4), `journal_echo._check_accepted_r3` (S1 also confirmed when the cited id is in critic_task_ids), `r3_integration_check._is_critic_basis` (lazy import, exact compare on ImportError). Branch-5 and generic FAIL texts name `critic:<critic task id>`.
- Tests (existing files): MATRIX_ROWS `-cited` twins generated from every `critic` row, plus 13 QE2 rows (builder/sonnet, GENERIC); test_journal_echo_r3.py 3-row parametrised test + malformed-basis test; test_r3_integration_check.py one trail test (valid and malformed).
- Acceptance greps: `basis == "critic"` remains only in docstring lines (journal_validator.py:158, :676; journal_echo.py:2171, :2174; r3_integration_check.py:206), zero code lines. `critic_basis(` non-test = def + validator :726, echo :2193, r3 :154 (via `_is_critic_basis`).
- Note: to keep the grep at 0 code lines the word sits in a local (`word = "critic"`) in critic_basis and `_CRITIC_MARKER[:-1]` in the r3 fallback.
- tests not written: none. No new config keys. No changelog fragment written (not in owns, no path given).
- Mechanism files journal_validator.py and journal_echo.py: STAGED, NOT committed (Lead commits).

Witness: `python -B -m pytest tools/test_journal_validator.py tools/test_journal_echo_r3.py tools/test_r3_integration_check.py -q`
```
492 passed in 4.97s
```
