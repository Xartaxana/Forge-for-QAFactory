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

## Round 2 (Lead answers)
- Background runs stopped: pids 10456, 37048, 38068, 8692 killed; no python process matching test_quarantine/k5mine remained (checked by process list). The quarantine check is NOT part of this witness (CI nightly).
- Merge of origin/main: d0623a17 (N14 a154ffca inside), no conflict, no other change.
- driver-layers.json:1327 -> words_doors_common.py, :1328 -> test_words_doors_detector.py. test_silent_passes.py:1345 STUB_FILES refusals 4 -> test_story_run_refusals_cc.py (measured: stub_problems counts 4 in cc, 0 in every other refusals file and in the shim). mutations-c2-1s-fix-round.json:3 -> tests/test_story_run_refusals_t667_c21.py. state-exits.md :71,72 -> test_story_run_s6_c16b.py, :78 -> test_story_run_s6_hf2_11b.py (holds acceptance_awaits), :196 -> test_story_run_refusals_resume.py (holds refusal_resumes). Commit 18733632 (+ the audit-contract line edit below).
- test_current_audit_contract.py: the carrier selftest.py TEST_TIMEOUTS has no row for test_infra_failure.py nor test_no_move_seam.py (`grep infra_failure|no_move_seam selftest.py` finds only `:143 "test_story_run_s7_live.py": 600`), so both are pinned at the default 300: line 86 asserts 300 for test_infra_failure.py; line 88 keeps only s7_live at 600. The second stale pin (no_move_seam) showed in the witness round and was fixed the same way.

## Witness round 2 (16 files in parallel, no quarantine run)
```
test_story_run_s6_d1 81/81, manual 150/150, t292 175/175, c16b 92/92, hf2_11b 241/241: exit=0 each
test_story_run_refusals_core 263/263, sources 155/155, resume 117/117, t667_c21 169/169, cc 73/73, c24_n5 91/91: exit=0 each
test_words_doors_detector 41/41, doors 250/250, controller 212/212, flight_launcher 213/213: exit=0 each
test_current_audit_contract: first run FAILED on test_no_move_seam.py (300 != 600); after the line-88 fix, rerun once: "Ran 4 tests ... OK"
```
Not run locally: test_conductor_doors.py, test_selftest_slow_tests.py, test_quarantine.py check, canon judges.
Open: test_words_doors_flight_launcher 79.6 s, s6 manual 103.9, s6 t292 75.8, refusals core 61.5 provisional (named, not re-split).
