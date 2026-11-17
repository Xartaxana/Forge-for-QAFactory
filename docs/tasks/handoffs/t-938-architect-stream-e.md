# t-938 stream E: no verdict from a worker (B4 (i))

DoD: `python -m pytest tools/test_hygiene_gate.py tools/test_warn_messages.py tools/test_permission_audit.py -q -p no:cacheprovider`

Output
```
........................................................................ [ 16%]
........................................................................ [ 32%]
........................................................................ [ 48%]
........................................................................ [ 65%]
........................................................................ [ 81%]
........................................................................ [ 97%]
.........                                                                [100%]
441 passed in 12.72s
(final run, with the null row: 442 passed in 13.82s)
```

## What was done
- `tools/hygiene_gate.py`: `MSG_WORKER_ACCEPT` (spec text, ASCII, <= 350), `WORKER_VERDICT_VERBS` (data row), `_worker_verdict_call(command)`, one branch in `_decide_command` (after the journal check, before rollback): deny only when payload `agent_id` is a non-empty str AND `_worker_verdict_call`. Same deny shape/prefix. `_collect_signals`, `decide` posture, `journal_write.py` untouched.
- Recogniser: REUSES `dod_track._PYTHON_PROGRAM_RE` (import, no copy; clone ratchet untouched) and scans ALL matches (`finditer`), so any segment counts. The first positional is read by a small regex after the match (skips leading `-flags`, strips a quote). The import is lazy inside the function: a broken import raises into `decide`'s visible fail-open (never a silent refusal, never fail-closed).
- `tools/test_hygiene_gate.py`: ONE table `WORKER_VERDICT_ROWS` + `test_worker_never_writes_a_verdict`, plus one test that an existing refusal (cd) is not unrefused by the new branch.
- Changes are STAGED, not committed.

## Rows (id -> result)
accept-relative deny; reject deny; py-launcher deny; x-flag-quoted-path-with-spaces deny; second-segment-semicolon deny; second-segment-and deny; second-segment-pipe deny; subshell-absolute deny; backslashes deny; single-quoted-path deny; powershell-call-operator deny;
returned-verb allow; skip-verb allow; next-verb allow; mention-in-grep allow; other-program-accept allow; main-thread-no-agent-id (key absent) allow; null-agent-id allow; empty-agent-id allow; non-string-agent-id allow; unparsable-quote allow; unparsable-garbage allow; no-verb allow.

## Deviations
- The spec's `dod_track` has no PUBLIC name for the regex; I import the private `_PYTHON_PROGRAM_RE` (no edit to dod_track, outside owns). Public alias would be a one-line change in dod_track.
- none for null: row `null-agent-id` sends an explicit `agent_id: None`; `main-thread-no-agent-id` omits the key. Final run after adding it: `442 passed in 13.82s` (the Output block above is the run before that row; 441 passed).
- A text that merely contains `python tools/journal_write.py accept` (e.g. `echo "python tools/journal_write.py accept"`) from a worker IS refused (false refusal, accepted direction per §2.4).

## Questions
none

## Siblings noticed
none (the same recogniser forms live in `dod_track`; no second copy created).

needed beyond the manifest: `tools/permission_audit.py` (grep of hygiene_gate use), `docs/tasks/specs/20261116-architect-tier-spec.md` lines 246-265 (§2.4).

## Fix round (critic t-946)

red-before: rows `upper-case-dir` (`python TOOLS/journal_write.py accept --task t-1`) and `mixed-case-file` (`python tools/Journal_Write.py accept`) added first; run `python -m pytest tools/test_hygiene_gate.py -q -k worker_never` -> `2 failed, 24 passed` (FAILED [upper-case-dir], [mixed-case-file]; the third new row `dot-slash` already passed: `./tools/...` ends with `/tools/journal_write.py`).

| remark | change | path:line |
|---|---|---|
| N-E2 duplicated recogniser / private import | public generator `python_programs(command)` (normalised: forward slashes, lower case; empty/None yields nothing); `_is_journal_writer_call` reads it | tools/dod_track.py:243, :264 |
| N-E2 (hygiene needs the verb offset) | `python_programs` wraps `python_program_spans` (yields (program, end)); `_worker_verdict_call` reads the spans; the private `_PYTHON_PROGRAM_RE` import and the repeated body are gone. Addition beyond the literal spec, because `python_programs` yields no offsets: `is_journal_writer_program(program)` | tools/dod_track.py:235, :251; tools/hygiene_gate.py:1491 |
| N-E1 case-insensitive | `.lower()` lives in `python_program_spans`; 3 table rows | tools/dod_track.py:239; tools/test_hygiene_gate.py:342-344 |

Siblings: grep `_PYTHON_PROGRAM_RE` across tools/*.py: only dod_track.py itself remains (no other caller).

DoD output (`python -m pytest tools/test_hygiene_gate.py tools/test_dod_track.py -q`; test_dod_track.py exists and judges dod_track): `357 passed in 12.67s` (includes all existing `_is_journal_writer_call` rows).

numstat (staged, all of stream E in these files): `22 5 tools/dod_track.py`, `26 0 tools/hygiene_gate.py`, `53 0 tools/test_hygiene_gate.py`. This round: +3 test rows. The reason "spec demanded an adversarial table for input from outside" still holds.
Staged, not committed.
