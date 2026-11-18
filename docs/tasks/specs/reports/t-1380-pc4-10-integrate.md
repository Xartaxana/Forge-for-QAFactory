# t-1380 PC4-10 integrate N13 / N11 / N15

Branch worktree-agent-a3855d663ef22b6c9, pushed. Merged in order: N13 6c2396e3, N11 42feafa1, N15 b10e4512 (no textual conflict; the N15 merge was refused at first by wave-merge check (d), fixed in the same merge commit 12b43c87 with a features.json glob).

Commits: 12b43c87 (merge N15 + features.json), 1bb7a050 / eed60499 / d47438f2 (split-keep N13 / N11 / N15, each message = the printed keep-split block verbatim, from ci-out/keep-split-msg.txt, plus the Co-Authored-By line), 221fc690 (carriers).

## Carriers
- slow_tests.json: DONE. 3 old rows out, 15 parts in at the reports' provisional seconds (sorted).
- selftest.py TEST_TIMEOUTS: DONE. 3 rows (+ their comment blocks) removed, no part row.
- test-layers.json keep rows: DONE by split-keep (shim row kept, --shim, importers named). Extra edit (commit 221fc690): refusals parts' `named_by` re-pointed from the old file :472/:475 to `test_story_run_refusals_core.py:472/:475` (verified: the census checks are at core lines 472 and 475). `check` refuses a detector row with no named_by, so the five other parts carry the same pointer.
- test-layers `covers` entries `tests/test_story_run_s6.py`, `tests/test_story_run_refusals.py`, `tests/test_words_doors.py` (in the rows of test_story_run_deferred.py, test_story_run_s0.py, test_detector_verdict.py): left; those rows are importers of the shim, which stays on disk.
- gate-registry.json:546 stand_login_gate: DONE -> `test_story_run_s6_t292.py`. Proof of the unknown branch: t292 K15 (screen cases, no env_file: a Person of kind stand_login is raised at S6) and K24 (`stand_login_gate` called directly). c16b only tests the price text of the question, as B1 of t-1376 would call it the wrong part.
- driver-golden-rules.json lines 26-28: DONE (parts and ~lines read from the parts).
- driver_golden.py:884 file_name: DONE -> `test_story_run_refusals_resume.py` (the probe reorders the `driver-runs` write in resume_with and reruns the file; the resume part holds the resume scenarios and their driver-runs reads). FINDING: the probe's anchor `def resume_with(` is searched in `story_run.py`, but the function is in `driver_dispatch.py:2308`: the probe refuses on main already (not mine, not touched).
- test_conductor_doors.py data strings: DONE (cc part for CC1/CC8/CC13/CC14: all CC checks are there; c16b for the three s6 rows).
- lint-baseline.json: DONE (re-keyed to c16b, count 2; `lint_ratchet.py` prints `76 findings, 76 in the baseline, 0 new, 0 stale`).
- architecture.md :203, :291 and SIBLING_MAP.md :146: DONE (four part names, shim noted). docs/SIBLING_MAP.md is a mechanism path: STAGED, not committed (Lead commits).
- test_current_audit_contract.py / test_selftest_slow_tests.py: DONE. words_doors -> `test_words_doors_flight_launcher.py` (in slow_tests); the refusals 600 pin is removed (the row no longer exists) and `test_story_run_refusals_core.py` joins `names` (expects the default 300).
- features.json: DONE. `test_words_doors_*.py`, `words_doors_common.py` added (no glob matched them). `story_run_s6_common.py` and `story_run_refusals_common.py` already match `story_run_*_common.py`.
- Changelog fragment: `ai-packages/qa-factory/changelog.d/package-ci-4-PC4-10-n11-n13-n15-splits.md`.

## Needed from integration / outside owns (not edited)
- `scripts/tests/fixtures/driver-layers.json:1327-1328` (N15): rows `test_words_doors.py` `<module>` -> `words_doors_common.py`, `part_detector` -> `test_words_doors_detector.py`.
- `scripts/tests/test_silent_passes.py:1345`: `STUB_FILES["test_story_run_refusals.py"]: 4` counts a file that is now a shim (0 stubs); the 4 stubs live in a part; canon-only judgement.
- `scripts/tests/fixtures/mutations-c2-1s-fix-round.json:3` `"test": "tests/test_story_run_refusals.py"` -> `tests/test_story_run_refusals_t667_c21.py` (N11 report).
- `design/state-exits.md:71,72,78,196` name the old files (prose).
- `test_story_run_s0.py:1312,1588` imports git_fixture through the shim (N12).

## Not an item of mine, found
- `test_current_audit_contract.py` fails on main already: `assertEqual(seen['test_infra_failure.py'],600)` (line ~85) but the 600 row of test_infra_failure.py was removed by a8a9fb40 (`git grep infra_failure 12a932a0 -- selftest.py` prints nothing; the same call finds `TEST_TIMEOUTS`). Left unfixed (a design choice of which row to pin).
- Over 60 s provisional, named, not re-split: s6 manual 103.9, s6 t292 75.8, refusals core 61.5, words_doors flight_launcher 79.6.

## Witness (one round, all edits in, 16 files in parallel; `python -B <abs path>`)
```
test_story_run_s6_d1:              === 81/81 ok ===    exit=0
test_story_run_s6_manual:          === 150/150 ok ===  exit=0
test_story_run_s6_t292:            === 175/175 ok ===  exit=0
test_story_run_s6_c16b:            === 92/92 ok ===    exit=0
test_story_run_s6_hf2_11b:         === 241/241 ok ===  exit=0
test_story_run_refusals_core:      === 263/263 ok ===  exit=0
test_story_run_refusals_sources:   === 155/155 ok ===  exit=0
test_story_run_refusals_resume:    === 117/117 ok ===  exit=0
test_story_run_refusals_t667_c21:  === 169/169 ok ===  exit=0
test_story_run_refusals_cc:        === 73/73 ok ===    exit=0
test_story_run_refusals_c24_n5:    === 91/91 ok ===    exit=0
test_words_doors_detector:         === 41/41 ok ===    exit=0
test_words_doors_doors:            === 250/250 ok ===  exit=0
test_words_doors_controller:       === 212/212 ok ===  exit=0
test_words_doors_flight_launcher:  === 213/213 ok ===  exit=0
test_current_audit_contract:       FAILED (failures=1)  AssertionError: 300 != 600 (seen['test_infra_failure.py'], pre-existing, see above)  exit=1
```
`python -B tools/test_quarantine.py check`: NOT COMPLETED. The full run (started 06:37) and a restricted K5 driver over the last 14 commits (scratchpad k5mine.py, started 07:19) were still running after 55 and 12 minutes (the per-commit import-edge scan is slow on this loaded machine; t-1376 saw the same: "timed out at 280 s"). No output, no violation seen, and no "no violation" witness either. Processes left running (named per RUNBOOK 9.8): python.exe pids 10456, 37048, 38068 (full checks) and 8692 (restricted). What was checked by hand: the three split-keep commit messages are the printed block verbatim (git log -3 shows the `keep-split:` first lines), the old row of each stays as a shim row, the parts and common modules are on disk in the same tree.

Not run locally: test_conductor_doors.py, test_selftest_slow_tests.py, canon judges.
