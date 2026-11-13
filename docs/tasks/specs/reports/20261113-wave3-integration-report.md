# Wave 3 integration report (13.11.2026)

Branch `wip/wave3`, from origin/main 12317b6. Two jobs: A retake of the frozen S6 console capture, B merge of `origin/wip/fv19-c2` (8e70deb).

## Job A -- frozen S6 console retaken (commit 4c76175)

Cause (as measured by the Lead): 8207150 "FV1-4 N1" prints `note: brief: ...md (5,738 B)` instead of `(<a> B, <b> budget B against the ceiling)`.

Byte copy of `fixtures/s6-w1-frozen/` taken first (scratch `s6-copy`), hashes equal before the retake (4 files, each hash twice).

Mask change (M7, `test_story_run_s6_w1_frozen.py`): `BRIEF_BYTES` now also matches the one-figure form `(N B)`; the masked output of that form is `(<bytes> B)`, the two older forms are masked exactly as before. The negative control (a wording change on the two-figure line is still caught) and the two-variant row are untouched and green. Docstring: M7 line says the one-figure form; one line added: "Retaken on 13.11.2026 after FV1-4 N1 (8207150 ...) by the owner's word: console.json only". The spec `t-2147-tr3-9-walker-lanes.md` was not touched (the docstring already carries the retake history; the spec records only the first capture commit).

Capture: `python -B scripts/tests/test_story_run_s6_w1_frozen.py --capture scripts/tests/fixtures/s6-w1-frozen` (package dir, subshell) printed `captured: {'calls': 2, 'events': 4, 'state_keys': 6, 'console': 3}`. Entry counts equal the frozen file.

Fixture diff (git diff, word-diff of the changed bytes; calls/events/state_keys byte-equal, only `console.json` changed, 2 lines = 2 entries):

```
-B, <bytes> budget B against the ceiling)\n[S6]
+B)\n[S6]
-B, <bytes> budget B against the ceiling)\n[S6]
+B)\n[S6]
```
Full lines: entry 1 `...S6-qa-runner-1.md (<bytes> B, <bytes> budget B against the ceiling)` -> `...S6-qa-runner-1.md (<bytes> B)`; entry 2 the same for `S6-qa-runner-2.md`. Nothing else differs.

Verify run: `python -B scripts/tests/test_story_run_s6_w1_frozen.py` -> `=== test_story_run_s6_w1_frozen: 6/6 ok ===`.

Sibling `fixtures/s5-n1-frozen`: grep for `against the ceiling` and `budget B` found nothing in its 4 files, and `note: brief` count is 0 in each (positive control: the same grep finds both strings in `s6-w1-frozen/console.json` before the retake: 2 hits). So it carries no brief note and is not stale. Not run, not touched.

## Job B -- merge of origin/wip/fv19-c2 (merge commit 819a31f)

`git merge --no-commit --no-ff origin/wip/fv19-c2`: automatic, ZERO conflicts (auto-merged role-load.json, contract.py, manifest_put.py, s5_precheck.py, test_s5_precheck.py). 18 files, +741/-59. Ratchets: `role-load.json` raises are exactly the branch's named ones: `ratchet_tokens` qa-automator 20257->20313, qa-code-critic 19420->19478; `process_ratchet_tokens` qa-automator 18687->18746, qa-code-critic 17596->17655. No other raise; judgment-census untouched. The pre-merge `forge_metrics --check` (commit hook "WARN: ok ... new package files 1 (all classified)") passed with no features.json change needed (plans/features.json unchanged).

Conflicts: none. Doors met: none (no features row, no ratchet conflict, no tier line demanded).

Narrow witnesses (all run in the package dir):
- `scenario_walk.py --witness-for scripts/contract.py scripts/coverage_contract.py scripts/manifest_put.py scripts/migrate_artifacts.py scripts/s5_precheck.py scripts/window_record.py` printed 111 test files; non-slow subset (slow_tests.json files over 10 s, `test_story_run_*`, `test_controller_*`, `test_fixes_13797` excluded) plus the five named = 61 files run; all green (52 print `=== name: N/N ok ===`, 9 pytest-style print `N passed`/`OK`, exit 0 each).
- `=== test_s5_precheck: 1184/1184 ok ===`
- `=== test_manifest_put_merge: 378/378 ok ===`
- `=== obligation join (TP2-2553): 63/63 ok ===`
- `=== judgment_census: 24/24 ok ===`
- `=== role_load (the one measure of a role's start load): 186/186 ok ===`
- `slices: 44 declared, all present and fresh; 11 key pages; 12 charters carry a generated digest line` (contract_slices.py --check)
- `PASS limits: ...` / `=== qa-factory selftest: 4/4 ok ===` (selftest.py --limits --lang)

Push: `git push origin wip/wave3` then `git push origin wip/wave3:main` -> `12317b6..819a31f  wip/wave3 -> main` (fast-forward, no force).

## Canon (run 43515748054, `python -B tools/ci_read.py start --ref main`, token from GITHUB_TOKEN; tip 819a31f)

First attempt: failure. Job list: start success; skip-if-unchanged success; forge-check success; changes success; runner-facts skipped; test-redundancy skipped; package-fast success; install-smoke success; package-full (1) FAILURE; package-full (2) success; crap-measure skipped; quarantine-check skipped; clock success; package-full-report skipped.

The red: shard 1, `=== qa-factory selftest (shard 1/2): 214/215 ok ===`, file `test_controller_rework_repair_binding.py` 234/235, row `a recorded id under a fresh key is refused: resume, do not replace` ('resume existing dispatch' not found). Evidence it is a flake and not this wave: the same file passed on the previous main canon (run 43510284960, 20.7 s) and the wave touches none of its code path (contract/manifest_put/s5_precheck/migrate_artifacts/window_record); it passes locally 4 of 4 runs (235/235); `gh run rerun 43515748054 --failed` on the SAME commit turned package-full (1) green. No fix made (nothing to fix on evidence); the test's row is one to watch (the failure text prints only its first line in CI; the test's `refused_detail` line was not visible in the digest).

Final job list of run 43515748054 after the rerun, conclusion `success`:
```
132206578981 full / package-full (1) success
132206580063 start success
132206580690 checks / runner-facts skipped
132206581088 full / quarantine-check skipped
132206581223 full / package-full (2) success
132206581279 checks / forge-check success
132206581521 checks / package-fast success
132206631376 full / crap-measure skipped
132206634116 full / skip-if-unchanged success
132206639326 full / install-smoke success
132206649927 checks / changes success
132206656327 full / test-redundancy skipped
132215359771 full / package-full-report success
132215479923 clock success
```
The push pipeline 43515733240 (forge-check on the merge tip) was success. `test_current_audit_contract.py`: named only; it did not appear red in this canon.

The wait cap (45 min) was exceeded by the rerun (about 25 min first attempt + about 30 min rerun); reported here, run id above.

## Siblings / analogs noticed
- `fixtures/s5-n1-frozen`: not stale (see above).
- `test_controller_rework_repair_binding.py`: a CI-only intermittent on the fresh-key refusal row; worth a look (suspect the timing `never_started_after_s: 0.01` in its setup) -- queued to the Lead, not touched.

## Needed beyond the manifest
`plans/features.json` (not edited), `docs/tasks/specs/t-2147-tr3-9-walker-lanes.md` (grep only), `scripts/slow_tests.json`, `tools/ci_read.py`, the branch's fv1-19 c1 report.
