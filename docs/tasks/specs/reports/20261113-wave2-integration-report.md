# Wave 2 integration report (13.11.2026)

Integrator: builder (sonnet). Worktree `.claude/worktrees/wave2`, branch `wip/wave2`, pushed to `main` fast-forward (no force).

## Merges (order as given; every one `merge-base --is-ancestor origin/wip/<b> HEAD` = 0)

| branch | tip | merge commit |
|---|---|---|
| wip/statuses-wave1 | 0bfa3c9 | 6381002 |
| wip/owner-words-1113b | 0c9f706 | 4e086e7 |
| wip/fv2-2 | 2c1be69 | 4f37213 |
| wip/sc6-2 | 4bd145f | d07737f |
| wip/pc3-2 | 0f8dd54 | 542075f |
| wip/pc3-1 | c066402 | e44a5a2 |
| wip/p1v-n4b | 92de1c0 | 7c649bc |

No branch merged empty. `plans/PILES.md` untouched (stays deleted).

## Conflicts (fv2-2 only)

1. `ai-packages/qa-factory/scripts/tests/fixtures/form-rounds.json`. Main (wave 1) had DELETED the 4 stale `obligation_refs <- manifest_from_tests@...` known-red rows (they went green); the branch had DELETED the 3 `derive: ...requirements` rows (its fix FV2-2) and RE-ATTRIBUTED the 2 `derive: s4-designer-to-*:scope[0].plan_row` rows to FV1-14. These are independent edits, not contradictory statements of one fact. Result: both deletions applied (7 rows gone), the 2 plan_row rows in the branch's re-attributed form (the branch's addition; main had them unchanged from the base). JSON parses (checked).
2. `scripts/tests/test_handoff.py` (2 hunks): both sides state the same fact (the case's `Plan row:` body line); only line order and a label word differ. Main's text kept in both hunks.

## Repairs

- merge pc3-2 refused by the pre-commit `forge_metrics --check` (door b/d): new package file `scripts/tests/probe_by_code_languages_common.py` (cut from the old test file by PC3-1/PC3-2) matched no feature. Fix: `plans/features.json` F03 gains the glob `scripts/tests/probe_by_code_languages_common.py` (inside merge commit 542075f).
- CI repair round 1 (22c3948): `scripts/tests/test_story_sides.py` TIMED OUT at 300.1 s on canon 43506734721 shard 1 (package-full (1)). Cause commit: c066402 / 64c7d3e (PC3-1 added 88 lines of rows to a file that was already 290.5 s green on canon 43502097900, against the 300 s default). Fix: `selftest.py` `TEST_TIMEOUTS` row `test_story_sides.py: 600` with the FR-31 comment (same class as the rows of test_story_run_s6.py, test_story_run_refusals.py). Confirmed: green on canon 43510284960 (package-full (1) success).

## Ratchets raised

- `selftest.TEST_TIMEOUTS["test_story_sides.py"]`: none (300 default) -> 600. Reason above. The cost cut (split of the file, B-155 class) is not done; it is queued by the comment only, no BACKLOG row (BACKLOG frozen).
- No other ratchet touched.

## Item B (diagnostic of the frozen S6 console compare)

Implemented in `test_story_run_s6_w1_frozen.py` (commit 1f90c00): `console_diff_lines` + a print in `w1_frozen_console` AFTER the verdict, only when the live console differs; green run prints nothing more; the compare itself is unchanged. Limits as spec'd (first differing entry and at most 5 in all; json text wrapped at 200 chars with prefix `exp[i] k/n:` / `got[i] k/n:`; cut at 4000 with `...(cut, N chars)`; length line first when lengths differ; `got: <empty>`). Helper checked locally WITHOUT running the file's scenarios (3 calls: empty live, one 450 vs 5000 char entry, equal lists: line max 214 chars, cut mark present, equal lists give []).

**DIVERGENCE, item B does not reach the reader.** The spec says CI cuts a line at 300 characters. In reality the selftest runner (`scripts/selftest.py::_test_outcome`, lines 488-497) keeps only lines of the file's stdout that START WITH `FAIL`, and prints at most the FIRST 3 of them, each cut at 300. The file's own FAIL lines already take all 3 (`FAIL (the whole list of this file)`, the verdict line, and the file's summary line). So the `exp[...]`/`got[...]` lines never appear in the job log (`ci_read.py log`) nor in the shard artifact `package-full-shard-2/selftest-shard-2-of-2.txt` (both checked on canon 43510284960: grep `exp\[|got\[|console entries|got:` over the shard artifact printed nothing; positive control: the same artifact and tool printed the `FAIL` lines). The CI text actually printed for the red file, verbatim (job 132178591235 / artifact):

```
FAIL tests: scripts/tests/test_story_run_s6_w1_frozen.py  10.7s ? exit 1 ? === test_story_run_s6_w1_frozen: 5/6 ok ===
      FAIL (the whole list of this file): w1_frozen_console: the console of every entry equals the pre-C1 capture (M1, M2, M6, M7 masked)
      FAIL w1_frozen_console: the console of every entry equals the pre-C1 capture (M1, M2, M6, M7 masked) ? first difference at ?0: live ?S6: manual block of 3 case(s), 1 more block(s) after it: TC-1
```

Only the first ~120 characters of live entry 0 are visible: it begins `S6: manual block of 3 case(s), 1 more block(s) after it: TC-1, TC-2, TC-3`, then (from the earlier canon, same text) `S6: app-card: no answer` / `S6: S6-qa-runner-1: no walk session (walk_session open: the st...`. The expected side and the rest are not visible, so the merged change that produced the new console text could NOT be named from CI output (not guessed).

Fork returned to the Lead (design decision, not decided here): how the diagnostic is to be made visible under the runner's "first 3 FAIL lines, 300 chars" window. Options: (a) one extra FAIL-prefixed line with a char window around the first differing position (expected and got, ~120 chars each); (b) let `main()` of this file drop the "whole list" line when the console is the only failure and print FAIL-prefixed diagnostic lines in its place (still only 2 free lines); (c) raise `failed[:3]` in `selftest.py` for a file that asks for it (touches selftest.py, outside item B); (d) the test writes the full diagnostic to a file that the shard artifact upload carries (needs a CI-side carrier). The file stays red; the capture is not retaken.

## CI status of the LAST canon (43510284960, main 22c3948, canon wall time 19 min 32 s, limit 60)

```
start success
full / skip-if-unchanged success
checks / forge-check success
checks / changes success
full / test-redundancy skipped
checks / runner-facts skipped
checks / package-fast failure        (test_story_run_s6_w1_frozen.py only)
full / package-full (2) failure      (test_story_run_s6_w1_frozen.py only)
full / install-smoke success
full / package-full (1) success
full / crap-measure skipped
full / quarantine-check skipped
clock success
full / package-full-report skipped
```

Still red and why: only `test_story_run_s6_w1_frozen.py` (`w1_frozen_console`): the frozen capture `fixtures/s6-w1-frozen/console.json` differs from the live console (owner-word `--capture` retake pending; not mine). The first canon (43506734721, main 1f90c00) had the same red plus test_story_sides.py (fixed in round 1).

## Not mine

`scripts/tests/test_current_audit_contract.py` (unittest style, `test_one_table_decides_a_test_files_timeout`) fails when run alone: `assertEqual(seen['test_infra_failure.py'], 600)` gives 300 != 600. Red on e4ba384 already (no `test_infra_failure.py` row in `selftest.py` there either), no merged branch touches either file, and CI's canon does not report it (it never appears in the shard PASS/FAIL lines: not run by the canon, grep of both shard artifacts for `audit_contract` printed nothing; positive control: grep for `story_sides` printed a line). Left as is; it is a stale file or a missing row, for the Lead.

## Witnesses (local, narrow)

- `scenario_walk.py --witness-for` form-rounds.json test_handoff.py printed `keep test_field_producers.py` and slow scenario files only; `test_field_producers`: `=== test_field_producers: 909/909 ok ===`; `test_handoff`: `=== test_handoff: 610/610 ok ===`.
- selftest.py repair: its keep files `test_console_encoding` 116/116, `test_resolver` 1147/1147, `test_selftest_ran_nothing` 23/23, `test_selftest_shard` 95/95, `test_selftest_slow_tests` 124/124 ok.
- `selftest.py --lang`: `=== qa-factory selftest: 2/2 ok ===` (after every repair).
- `piles.py check --all`: `piles check: ok`.

## Siblings (reported, not changed)

`--capture` in the package tests (grep, files_with_matches, 3 hits incl. this file): `test_story_run_s5_n1_frozen.py` (lines 89 and 95 print `json.dumps(...)[:600]` of both sides: the same cut, same runner window, same invisibility), `test_scenario_world.py` (no `[:600]` dump found by `json.dumps(.*)[:` grep). Also: the runner's `failed[:3]` window affects every test file with rich FAIL detail.

## Needed beyond the manifest

`ai-packages/qa-factory/scripts/selftest.py`, `plans/features.json`, `ai-packages/qa-factory/scripts/slow_tests.json`, `ai-packages/qa-factory/scripts/tests/test_current_audit_contract.py`, `ai-packages/qa-factory/scripts/tests/test_story_run_s5_n1_frozen.py`, CI artifacts of runs 43506734721 / 43510284960.
