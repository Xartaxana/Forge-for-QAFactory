# t-982 S-E report: the probe runner `mutate_once.py`

## What changed
- `ai-packages/qa-factory/scripts/tests/mutate_once.py`: rewritten to spec 5.3. Two forms (spec file as before, plus inline `--root --id --target --old --new --test [--pytest]`), `--root` accepted by both and named in the usage text. Pre-touch refusals (exit 64, `refused: ...` naming what is wrong, what is expected, the argument that fixes it): bad arguments, spec file unreadable or lacking the id, target or test outside the root, test absent, target absent, non-UTF-8 target, empty `old`, `old == new`, anchor found 0 or 2+ times. `.py` mutant `compile()`d (on the mutated BYTES, so a BOM or CRLF is the compiler's) -> SyntaxError is exit 3 `invalid` without touching. Run: `Popen` with stdout and stderr to one file in `tempfile.TemporaryDirectory(ignore_cleanup_errors=True)`, `wait(timeout=TIMEOUT_S=60)`; on timeout `kill()`; the restore in `finally` at once; a reap `wait(5)` after the restore, its timeout ignored; the output is read only after the restore and the sha compare. Outcomes: 0 killed, 1 survived, 2 restore-mismatch (wins), 3 invalid; last line `outcome: <word>`.
- `ai-packages/qa-factory/scripts/tests/test_mutate_once.py` (new): one parameterised table `test_outcome_table` (28 rows) plus a usage row.
- `ai-packages/qa-factory/scripts/tests/test-layers.json`: keep row `test_mutate_once.py`, layer `table`, covers `tests/mutate_once.py`.
- `ai-packages/qa-factory/changelog.d/forge-t982-mutate-once-probe-runner.md`: fragment.

## Witness (verbatim, tails)
```
$ python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/mutate_once.py ai-packages/qa-factory/scripts/tests/test_mutate_once.py
scripts/tests/mutate_once.py: keep test_mutate_once.py (layer table, covers it)
no scenario or keep row covers scripts/tests/test_mutate_once.py: run the whole scenario layer
scripts/tests/test_mutate_once.py: test_scenario_cart_1.py   (... _local_1_0108, _local_1_arm_b, test_scenario_walk, _world)

$ python -B -m pytest ai-packages/qa-factory/scripts/tests/test_mutate_once.py -q -p no:cacheprovider      (three runs)
29 passed in 6.24s | 29 passed in 7.07s | 29 passed in 7.25s     (the very first, cold run: 10.45s; slowest row: pytest-one-failed 1.5s)

$ python -B ai-packages/qa-factory/scripts/tests/test_mutate_once.py
.............................                                            [100%]
29 passed in 7.25s

$ python -B ai-packages/qa-factory/scripts/tests/test_console_encoding.py
K7 residue scan of scripts/*.py: 0 flagged {}
=== console encoding: 116/116 ok ===

$ python -B ai-packages/qa-factory/scripts/selftest.py --lang
PASS lang: no Cyrillic anywhere in the package
PASS lang: no control byte left by an eaten escape sequence (FR-29)
=== qa-factory selftest: 2/2 ok ===

$ python -B ai-packages/qa-factory/scripts/refusal_registry.py --check      (exit 0)
A24 refusal registry: no violations
```
`refusal_registry.py` scan reach: Grep `mutate_once` in `refusal_registry.py` -> 0; the registry lists hook refusals only, so whether it scans `scripts/tests/` is not established beyond "it ran clean".

`test_judgment_census.py` is in `slow_tests.json` (33.3 s): судит канон пачки. I did run it once anyway: `=== judgment_census: 23/25 ok ===`, FAIL `test_c1_every_unit_has_a_row_and_every_row_a_unit` and `test_c3_the_ratchet_is_dense_and_only_shrinks`. My diff touches nothing the census scans (`scripts/*.py` outside `scripts/tests/`, P24), so I expect them to be red at HEAD already; NOT verified by a baseline run (a temp worktree for the baseline would not create), estimate. The canon will judge.

## Outcome-table rows and sources (all spec 5.3, "Outcomes" table unless noted)
- script-failed-with-summary-and-FAIL-line-is-killed: row "script form non-zero with `=== ` and >=1 FAIL" -> 0 killed
- script-passed-is-survived, pytest-passed-is-survived: "exit 0 (either form)" -> 1 survived
- pytest-one-failed-is-killed: "pytest form exit 1 and >=1 failed" -> 0
- script-nonzero-without-summary / without-FAIL-line / script-crash-before-summary: "script form non-zero with no `=== ` or no FAIL" and adversarial "a script that crashes before its summary" -> 3 invalid
- pytest-import-broken-by-mutant (pytest exit 2), pytest-file-with-no-tests (exit 5): "pytest exit 2,3,4,5" and adversarial list -> 3
- py-mutant-with-syntax-error-is-invalid-untouched: "mutated .py does not compile" -> 3, mtime unchanged
- bom-and-crlf-target-restored-byte-identical: E-R2, bytes identical after
- refusal rows (old absent, old twice, empty old, new==old, non-UTF-8 target, target outside root, test outside root, test absent, unknown argument, inline form without root, one positional): "any pre-touch refusal" -> 64, no `outcome:` line, mtime unchanged
- spec-file-form-killed, spec-file-unknown-id-is-refused: E-R4 / "back-compat spec-file row"
- timeout-mutant-loops-forever: "timeout" -> 3 invalid, restored (TIMEOUT_S patched to 0.5 s)
- timeout-with-grandchild-holding-output: E-R3 and the grandchild row -> 3 invalid, restored, wall time under 6 s (< TIMEOUT_S + 5)
- unreadable-output-is-invalid-restore-verified: "output missing or unreadable" -> 3, target still restored
- restore-mismatch-wins-over-killed: "sha after != before" -> 2 (sha patched, the child would be killed)
- usage row: no arguments -> 64 and the text names `--root` (Interface)

## Lines the spec asked for (1.1)
- AR-4: stores no path; prints only the test file's name and the target's file name (sha line); `--root` explicit; the `target-outside-root` and `test-outside-root` rows; the output file is in the system temp dir, never under root.
- AR-7: what the role still decides: the places, equivalence, reading the printed FAIL lines (an import error that pytest reports as a failure is `killed` by the runner; the residual is the critic's, no exception-name list in code).
- AR-9: every refusal names the wrong thing, the expectation and the argument; `refusal_registry.py --check` exit 0.
- AR-29 class: outcome classification is shape (exit code, summary counts, compile of the mutant); the restore/sha refusal is safety. Census: outside scope (P24), no row. Unit `mutate_once.main`.

## FR pass (design/factory-rules.md, sections A-G)
- A: FR-1 refusals say what/expected/fix (the `refused:` messages); FR-2 the door named is an argument the caller owns; FR-3, FR-4, FR-5, FR-46, FR-48, FR-50, FR-57 n/a (no person-facing reason, no gate over an informed pass; a test helper).
- B: text shown to a person not changed (the runner prints to a developer's console, no question form).
- C: FR-14 output shape is a contract: the last line `outcome: <word>` and exits 0/1/2/3/64 are pinned by the table; FR-12 no phrase list over a person's or role's words (the classifier reads exit code, `=== `/`FAIL` prefixes and pytest's count line, the output of a test, not wording of a role); FR-13 the outcome vocabulary is a closed 4-word set in one dict, not project variety; others n/a.
- D: FR-17 one runner for package and forge tests (axis 34); FR-59 an unknown (unreadable output, no summary) is `invalid`, never `killed`; others n/a.
- E: delivery and reporting not touched.
- F: FR-41 an unknown is not reported as a fact (no summary -> "no summary line"); FR-28 the measurer-like helper gets a test (the new file); others n/a.
- G: FR-29 no control byte (`selftest --lang` green); FR-30 English only (green); FR-31 the timeout rows wait 0.5 s of real time and assert nothing on load; FR-32 root cause: the restore-before-read order; FR-33 n/a (no role behaviour changed); FR-54 siblings listed below; others n/a.

## Deviations and findings (not guesses)
- The spec's keep row `covers` names only `tests/mutate_once.py`, so `--witness-for ... test_mutate_once.py` prints "no scenario or keep row covers scripts/tests/test_mutate_once.py: run the whole scenario layer" plus five scenario files. The DoD wording "prints `keep test_mutate_once.py`" holds for the first path only. QUESTION: add `tests/test_mutate_once.py` to `covers` (the pattern of `test_app_card_stand_lessons.py`)? Not done, since the spec fixes `covers`.
- Volume: the table runs 6.2-7.3 s warm, 10.45 s on one cold first run (the spec's limit is 10 s); the timeout rows use TIMEOUT_S = 0.5 s to stay under it. `tests-over` not needed unless the volume gate says so.
- Decisions the spec left open, taken as the minimum reading (tell me if wrong): the inline form REQUIRES `--root` (refused without it, the spec lists it first and AR-4 says explicit); the spec-file form still reads JSON with the existing `json.loads` but a bad file/id/shape is now a 64 refusal instead of a traceback; a value beginning with `-` must be written `--old=<text>` (argparse); script-form `killed` needs a `=== ` line AND a line starting `FAIL`, pytest form needs exit 1 and `N failed` with N >= 1 in pytest's count line; when output is unreadable AND exit 0, the outcome is `invalid` (the table lists the unreadable row without an exit qualifier).
- The row "grandchild" inherits stdout explicitly (`stdout=sys.stdout`): on win32 a Popen without redirection does not inherit handles (close_fds), so only the explicit form holds the output file. The orphaned sleeper lives 8 s.
- E-R7 (hard-kill residual) is carried by the brief and the coordinator, not by code: no change here.
- I once moved the shell's working directory with `cd` in a Bash call (the hygiene hook refused it, nothing ran); later calls used absolute paths.

## Siblings noticed (report only)
- Axis 16: the spec-file form's `json.loads` stays (non-goal).
- `scripts/tests/test_console_encoding.py` K7 scans `scripts/*.py` outside tests; tests/ helpers that print (this runner) are outside that scan, so the runner's own `say()` guards against a console that cannot encode a char; a console setup is not applied to tests/ scripts in general.
- `agent_budget.py` TEST_RE counts a runner call whose command names `tests/test_x.py` or `pytest` as a test run (P20): a critic's inline probe calls will count toward its WARN; no change here (non-goal).

## Needed beyond the manifest
- `docs/tasks/specs/20261117-forge-test-rules-spec.md` section 7.1 and 10.2 (named in the dispatch text), `ai-packages/qa-factory/scripts/tests/test_console_encoding.py` (K7 scan), `ai-packages/qa-factory/scripts/tests/test_app_card_stand_lessons.py` (test style), `ai-packages/qa-factory/scripts/slow_tests.json`.
