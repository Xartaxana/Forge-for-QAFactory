# t-758 attempt 2 - SC-N7 fix round report

Worktree `.claude/worktrees/sc-n7`, branch `wip/sc-n7`, on top of 3ae834f.

## Per finding
- F1: `exploratory_findings.append` (oracle block): `confirmed` appends only its sentence; `_closed(..., "oracle_status", ...)` is now the `else`. Any other unlisted value still gets the closed-list sentence.
- F2: `_nested_keys`: skips keys in `EXCLUDED` (the excluded walk reports them once at any depth). A nested unknown, non-excluded key keeps its "not a field of" sentence.
- F3: `_judge_refs`: `resolve()` / `is_relative_to` / `is_file()` wrapped in `try/except ValueError`; `str(exc)` is appended as that ref's sentence and the loop continues; collected problems survive. OSError untouched.
- F4: the K-M1-1 "all problems" table in `test_exploratory_findings.py` gained exact-match (`check_eq`) rows: confirmed oracle alone; unlisted oracle alone (control); excluded key once in evidence ref / probe / origin / corrects; same key in probe and origin once; nested unknown non-excluded key; over-long path alone and with two other problems (title, statement); NUL path alone. Expected single-problem texts are the old messages (excluded sentence verbatim; the OS-path text is what the stdlib raises, probed directly, not the new code; those rows exist only where the platform raises ValueError - they ran on this Windows machine).
- Correction of earlier claims: the first report's and commit's "every sentence is byte-identical" was false for F1/F2 (as the verdict says); it holds after this round.

## Witness
`python -B scripts/tests/test_exploratory_findings.py` (package dir): `=== test_exploratory_findings: 325/325 ok ===` (was 314; no FAIL lines).
`python -B scripts/selftest.py --limits --lang`: `=== qa-factory selftest: 4/4 ok ===`

## FR pass
- A: refusal still names what is wrong and the expected form; one refusal, each problem once (FR-1, FR-2 unchanged).
- G: no heredoc escapes / control bytes (the NUL is built by a `\x00` Python escape in the test, not a literal byte); English only; no new test file; row added to the existing table (FR-29, FR-30).

## Siblings noticed
none beyond the verdict's queue lines (red_sandbox --diagnostic etc.). Platform note: on non-Windows the over-long path may raise no ValueError; the rows are then omitted by design.
