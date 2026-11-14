# t-792 report: evidence path the OS cannot stat, one sentence on every OS

## What moved where
- `scripts/contract.py`: `evidence_ref_issue` body moved to `_judge_measured_ref`; the call is wrapped in one `try`
  (`ValueError`, or `OSError` with errno in ENAMETOOLONG/EINVAL/ENOENT/ENOTDIR) -> `unmeasurable_path_issue(what, raw_text, root)`.
  Other OSError (PermissionError, EIO) re-raised unchanged (FR-46). New beside the judge: `EVIDENCE_PATH_SHOWN = 80`,
  `_NO_SUCH_NAME`, `name_cannot_exist`, `_path_shown`, `unmeasurable_path_issue`; `import errno` added.
  Covers: absolute branch, relative resolve, `is_relative_to`, `under`, `is_file`, hash read; `require_hash=False` same guard.
  Every sentence of the judge echoes the path cut at 80 + "..." only when longer than 80 (shorter: byte-identical).
- `scripts/exploratory_findings.py`: `PATH_SHOWN`, `_NO_SUCH_NAME`, `_name_cannot_exist` removed; `_unmeasurable_text` is a
  one-line alias to `C.unmeasurable_path_issue("evidence", ...)`; `_judge_refs` uses `C.name_cannot_exist`; its `continue` kept
  (one sentence per ref); `import errno` dropped.
- Tests: rows added to `scripts/tests/test_exploratory_findings.py` (key_m1_1), OS-independent via patched
  `Path.is_file` / `Path.resolve` / `Path.read_bytes`.
- Changelog fragment `changelog.d/evidence-path-one-sentence-every-os.md`.

## Caller inventory of `evidence_ref_issue` (grep, positive control: it found the def at contract.py:5918)
| caller | catches around the call today |
|---|---|
| exploratory_findings.py `_judge_refs` (279) | no (own pre-guard only before the judge) |
| exploratory_findings.py `main` check (539) | no -> was a traceback, now a defect line |
| bug_records.py `_evidence_problem` (854) | yes `(OSError, ValueError)` -> junk read as missing file; now judge answers "is not a file" first (-> R_NO_FILE) |
| controller.py wrapper (2078) | no -> was a traceback |
| contract.py 2286 (`control.evidence`) | yes `(OSError, ValueError)` -> "cannot be read (exc)"; name errors now never reach it |
| contract.py 2380 (`contradiction.evidence`) | inside a `try` (not read in full) |
| contract.py 2452 (`diagnostic.evidence`) | yes, a `try` |
| investigation.py `_ref` (85) | no -> was a traceback |
| investigation.py (426) | no -> was a traceback |
Not edited (non-goal). Callers with a catch no longer see name errors from the judge; their catch still serves other OSErrors.

## Unguarded role-written path stat in other contract.py functions (listed, not edited; by grep, not read in depth)
lines 2383 (resolve/relative_to, inside the 2380 try), 3387/3392, 3445-3446, 5130-5131, 5576-5577, 3828, 2957: `resolve()` /
`is_file()` / `exists()` on a path built from a role-written string; most have no name-error guard.

## Edge 8
No test file seen by grep asserts a long (>80) path echoed whole in the judge's sentences (slow files not run; judged by the batch canon).

## Witnesses
- `python -B scripts/tests/test_exploratory_findings.py` last line: `=== test_exploratory_findings: 362/362 ok ===`
- `python -B scripts/tests/scenario_walk.py --witness-for scripts/contract.py scripts/exploratory_findings.py`: 91 lines printed;
  first 40 lines are scenario/keep rows (cart-1, local-1-0108, local-1-arm-b scenarios, then `keep test_ahead_cards.py` ...
  `keep test_probe_by_code.py`). Files in it that mention `evidence_ref_issue` and are neither slow nor quarantined:
  only test_exploratory_findings.py (run above). test_investigation, test_s7_investigation_replay, test_controller_state: slow,
  judged by the batch canon. test_evidence_ref_contract.py is not in the witness list; run anyway: `OK`.
- `python -B scripts/selftest.py --limits --lang`: `=== qa-factory selftest: 4/4 ok ===`

## FR pass
- A: refusal now names what is wrong and expected (FR-1); a real unreadable file is not turned into the role's fault (FR-46).
- C: sentence shape and one reader of it (FR-14); no new field.
- G: package English, no control bytes (FR-29/30); fix goes to the shared judge (FR-32/54).
architecture: AR-9, AR-15, AR-18 -- the shared judge holds the one guard and the one sentence; a refusal, never a traceback, on every OS
judgment: none -- a path that cannot be read is a shape fact

## Siblings noticed
Other contract.py functions above; also `_judge_refs` still pre-measures sha with its own try (needed: the judge never hashes a ref lacking sha256).
