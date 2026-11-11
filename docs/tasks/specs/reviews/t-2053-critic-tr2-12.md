# t-2053 critic on t-2040 (TR2-12): a test file that ran nothing is red

Branch `tr/tr2-12`, worktree `D:/ws1/wt-tr2-12`, diff `77b448a3e..d880f8f18`.

## Verdict

**NEEDS WORK** (`fit_with_fixes`): 1 blocking finding, 5 fix-before-merge, 2 small. The acceptance decision stays with the coordinator's tier.

The core wiring is sound: one seam (`_test_outcome`), shared by `--fast`, flagless and `--shard`; the 14 entries are present; the witness reproduces 13/13. It breaks CI on its first run, though, and the detector proves "printed nothing", not "executed nothing".

## Answers to the DoD questions

| Question | Answer |
|---|---|
| Does the detector fail open? | **Yes**, on a real path: a zero-check tally and an all-skipped entry are green; any output hides a silent file (F2). The real-directory pin closes only part of it. |
| `PYTEST_RUN_FILES`: real or dead? | **Dead door** (FR-2, F4). Empty set, read only by `ran_nothing`, populated only by the test's own patch. Nothing runs package tests by pytest "elsewhere". Listing a file makes it a silent green pass. |
| Do the two slow files need `SLOW_TESTS`? | **Yes, and a third**: `test_probe_gap_door.py` too. `test_exit_limit_halt_answered.py` also needs a `TEST_TIMEOUTS` row (F5). |
| Is the four-questions block true? | **Partly.** (a) understates the cost; (c) names a check that does not detect this; (b) and (d) hold (F6). |

## Findings

### F1. BLOCKS MERGE: the entry form leaves `.pytest_cache` in the package, and `--hygiene` goes red in every CI selftest job

- Surface: how a test file launches pytest as a script.
- Lines: the last line of all 14 files, `pytest.main([__file__, "-q"])`.
- Scenario: `.gitlab-ci.yml:199` and `:244` (and `forge-check.yml`, `nightly.yml`) run `cd ai-packages/qa-factory`, then `selftest.py --fast --jobs 4` or `--shard I/N`. With no ini file, pytest's rootdir is the common ancestor of cwd and the file, so the package root. `cmd_hygiene` runs after the tests (`selftest.py:1041-1044`, `:1070-1079`), walks the tree regardless of `.gitignore`, and reports anything untracked.
- Measured on a copy, real `test_rows_owed.py`, cwd = package root: `7 passed`, `.pytest_cache at package root: True`.
- Measured end to end on a tiny git repo, real `cmd_hygiene`:
```
== as in the diff | test exit 0 | 1 passed in 0.11s | .pytest_cache at package root: True
FAIL hygiene: the package directory carries only package content ... would install: .pytest_cache/
cmd_hygiene -> False
== control -p no:cacheprovider | test exit 0 | 1 passed in 0.04s | .pytest_cache at package root: False
PASS hygiene: the package directory carries only package content
cmd_hygiene -> True
```
- Measured through the real runner, `selftest.py --tests --hygiene` from the package root, on a copy of `scripts/*.py` plus one test file:
```
== as in the diff rc 1
PASS tests: scripts\tests\test_mini.py  5.8s
FAIL hygiene: ... a local-directory marketplace would install: .pytest_cache/
=== qa-factory selftest: 1/2 ok ===
== control -p no:cacheprovider rc 0
PASS tests: scripts\tests\test_mini.py  4.9s
PASS hygiene: the package directory carries only package content
=== qa-factory selftest: 2/2 ok ===
```
- This exact class already turned the canon red: commit `8f37605fb` (t-1999, pipeline 8042530), "runs pytest.main with -p no:cacheprovider (it left .pytest_cache)". The ancestor is on this branch.
- Origin: the finding's prescribed form omits the flag, so this is a spec defect passed on faithfully, not builder invention. The builder's witness could not see it: `--hygiene` was not run and the cwd differed.
- Fix:
  1. All 14 files take `[__file__, "-q", "-p", "no:cacheprovider"]`, as the 7 existing entries do (`test_app_card.py:296`, `test_walk_lanes.py:307` and others).
  2. The same in `ENTRY`, `test_selftest_ran_nothing.py:21`.
  3. Add a real-directory row: a `pytest.main(` without `no:cacheprovider` is a failure.
  4. The Lead corrects the spec form.
- Neighbours on this surface: all 7 other `pytest.main` entries carry the flag, so the 14 are the whole instance set.

### F2. FIX BEFORE MERGE: fails open; the decision said "count executed checks", the code tests for empty output

The spec (TR2-12) says a file with zero executed checks is red. Report line 10 calls empty output a "uniform signal", and the commit's AR-28 line says "a file that executed nothing is never a pass". Probes through the real `_test_outcome`:

| Input (a failing `test_a` in each unless noted) | Result | Should be |
|---|---|---|
| real `harness.finish()` with zero checks: `=== x: 0/0 ok ===` | GREEN | red |
| entry present, every test skipped: `1 skipped` | GREEN | red by the spec |
| no entry, `print` at import | GREEN | red |
| no entry, a stderr line at import | GREEN | red |
| no entry, a `SyntaxWarning` from `'\d'` (printed on each compile under `-B`) | GREEN | red |
| no entry, `def test_a ():` (space before the paren) | GREEN | red |
| no entry, unittest `def testFoo` | GREEN | red |
| entry without `raise SystemExit`, failing test (`1 failed`) | GREEN | red; a sibling that predates this diff |
| class method or nested `def test_` with no entry | RED | correct |
| entry, nothing collected | RED, exit 5 | correct |
| module-level skip with the entry | RED, exit 1 | safe direction |

- Partial cover: pin row 7 catches the three import-output rows for files in the real directory, because it reads source. It is itself passable: `"__main__" in text` is a substring test, and `^\s*(finish|sys\.exit|raise SystemExit)\(` matches anywhere (`test_selftest_ran_nothing.py:85`).
- Today's real directory: no file is known to be affected. 166 files match the regex, and all of them carry `finish(`, `print(`, `pytest.main` or `unittest.main`. Twenty files use a dynamic `globals()` runner; none has an uncalled `test_*` without one.
- Fix:
  1. Treat a final `: 0/0 ok ===` tally and a pytest summary with skips only as ran-nothing. Both are data, so AR-29 is kept.
  2. Add pins for both.
  3. Tighten pin row 7 to a parsed `__name__` guard or a call.
  4. Correct the AR-28 line. If the Lead accepts the empty-output proxy instead, that is a decision to record, with these rows as known gaps.

### F3. FIX BEFORE MERGE: false red; the regex reads text, not definitions (dispatch edge)

| Input | Result |
|---|---|
| Working silent script whose triple-quoted fixture holds `def test_x():` at line start | RED, "ran nothing" |
| Working silent script calling its own `def test_a()` by name | RED |
| The first case after following the refusal's advice (entry added) | RED, exit 5, so the advice does not work |

- The comment "A working script cannot turn red by this: it prints" (`selftest.py:394`) overclaims. So does axis 9's "the regex reads definitions".
- In the real directory, 18 files match the regex with no `def test_` in their AST, only in strings. They all tally, so nothing is red today; the surface is live.
- Control 8 (`test_selftest_ran_nothing.py:62`) tests only a one-line string and so does not pin this case.
- Fix: replace `_TEST_DEF` with an `ast` walk for `FunctionDef`/`AsyncFunctionDef` named `test_*`. The file just exited 0, so it parses; on a `SyntaxError` return False. This also closes the space-before-paren row of F2. Add a triple-quoted control. The called-by-name case stays a stated limit in the comment.

### F4. FIX BEFORE MERGE, LEAD'S FORK: `PYTEST_RUN_FILES` is a dead door that turns into a silent pass

- Readers: `selftest.py:404`, and the patch at `test_selftest_ran_nothing.py` section 6; the changelog mentions it.
- The comment says a listed file "is run by pytest elsewhere". The only pytest run of tests in CI is `python -m pytest tools/ -q` (`.gitlab-ci.yml:110`, `forge-check.yml:76`). Positive control: the same grep found that line and every selftest line. So listing a file makes it green and executed by nobody, with no recorded reason (FR-4).
- The refusal text does not name the constant: `pytest-run` appears in no other line of `selftest.py`, so the door is not findable from the refusal (FR-1). Report line 45 says the refusal "names the door (script entry, or PYTEST_RUN_FILES)"; only the first half is true.
- The Lead's decision does name this door, so removing it is the Lead's call.
- Recommendation: remove the set and shorten the text to `ran nothing: add a script entry`. The entry is a door anyone can use. Alternative: keep it, have selftest itself run listed files with `python -m pytest`, and name the constant in the text.
- `AR-9` is touched but not named in the commit's `architecture:` line (small).

### F5. FIX BEFORE MERGE: slow files and the ceiling (timings per the report; the coordinator holds the list)

- `slow_tests()` docstring: a file over `slow_over_s` (10 s) belongs on the list. Over it per report line 34: `test_exit_limit_halt_answered.py` 238 s, `test_brief_pack_sd_head.py` 81 s, `test_probe_gap_door.py` 36 s. None of the 15 touched files is listed.
- Effects of staying unlisted:
  - They enter `--fast`, the merge-request tier whose stated budget is ~90 s.
  - The shard balancer weighs each at 2.5 s (half of `fast_under_s`), so the two shards skew.
  - `package-full-report` shows them as `+`, counting against `max_drift` 5, and goes red past it.
- Ceiling: 238 s against the default 300 s under `--jobs 4` is the FR-31 shape. Precedents with the same numbers got 600: `test_blast_radius.py` (285.6 s), `test_story_run_freshness.py` (223 s). Add a `TEST_TIMEOUTS` row now.
- List update: `--slow-tests --from <canon output> --update` after the batch canon, not by hand (the docstring's rule), unless the Lead wants them out of `--fast` before that.
- Queue: why 13 checks cost 238 s in a file the report says is described as fast.

### F6. FIX BEFORE MERGE (TEXT): the four-questions block

- (a) **Understated.** "milliseconds" prices the regex only. Report line 54 itself says about 5 minutes of added wall time, the actual cost.
- (b) **True in form.** 32 lines against 32 axes in `docs/SIBLING_MAP.md`. Axis 9's n/a stands (the leaf answers by path, a different question), but see F3 for its wording. Axis 18: no ratchet touched.
- (c) **Not true.** Check 13 of `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` is evidence-based acceptance and typed fields. It has no line on empty runs (`ran nothing|ran_nothing` no match; control: `selftest` in the same file matches at line 370). `selftest` cannot detect its own failing open, as F2 shows. The finding's text carries the same error, so the Lead should correct both. The honest detector is pin row 7; name it, and register a calibration line if the Lead wants one.
- (d) **True.** `cmd_tests` globs every `test_*.py`, and all tiers share `_test_outcome`. A slow-listed file is judged only nightly.
- Report line 3, "no `tier:` line needed": the gate lets it through, but rule 10 asks every mechanism commit to declare a tier. For the Lead, not the builder.

### F7. SMALL: duplication

`_DEF` at `test_selftest_ran_nothing.py:79` copies `selftest._TEST_DEF`; use `ST._TEST_DEF` (it goes away with F3). The 7 older entries use three other shapes (`sys.exit(...)`, `return pytest.main`, `str(Path(__file__))`); align them or queue them under "one form on all".

### F8. SMALL: lying annotations and dead branches

`import pytest  # noqa: E402` in 6 files, at the top of the imports where E402 cannot fire: drop the comment. `except OSError: return False` in `ran_nothing` fails open, and only on a file that has just run: effectively dead, so drop it or accept it. `(stdout or "")` repeats the guard the only caller already applied.

## Standing questions

1. **Fit to the spec:** mechanism and text as written; "counts executed checks" is not met (F2).
2. **Builder's decisions:** the door's form was flagged honestly (F4); the empty-output proxy is unsafe in the direction shown (F2).
3. **Seams:** additive; the 14 files gain only the import and the last line; `test_current_audit_contract.py:75` stubs non-empty stdout, so it is unaffected.
4. **Class-wide completeness:** the 14 are the whole set for the flag (F1). `tools/` tests run under real pytest, so they are outside the class, as the report says. No sibling runner judges package test files by exit code.
5. **Tests:** both listed mutations have killers by reading (pin row 7; row 1). No row kills the cache leak, the 0/0 tally, all-skipped or the triple-quoted string.
6. **DUPLICATION AND CONSISTENCY:** F7, and F1 (the new form diverges from the existing 7). Grepped `pytest.main` in `scripts/tests/*.py` and `def.{0,6}test_` in `selftest.py`, `node_ids.py`, `test_files.py`, `manifest_from_tests.py`, `test_novelty.py`: no other definition reader there. The clone ratchet is not read: the branch is not pushed, so there is no `forge-check` yet. **Request:** that job's result is owed at the canon.
7. **CODE QUALITY:** F8. New functions are short; no long or deep function added.
8. **Hygiene:** F1 is the hygiene breach. English; `git ls-files --eol` shows LF kept on the three files checked. `--lang` per the report, not rerun.
9. **IN-TREE RATCHETS:** none in the diff.
10. **ARCHITECTURE:** AR-18 and AR-22 hold; AR-28 is overclaimed (F2); AR-9 is unnamed (F4).
11. **JUDGMENT:** none moved. `adds data check` is true. No census row or scan constant touched; `ran_nothing` does not match `UNIT_NAME_RE`.

## CI shard runner

`--shard` goes through the same `_test_outcome`. A ran-nothing file is a normal `FAIL tests:` line with the detail after the seconds, so `_DURATION_LINE` still parses it (by reading the regex and its comment, not run). Consequences for shards: F1 reddens each shard, because each runs the hygiene; F5 skews the balance.

## Spot-checks

- Witness: rerun gives 13/13, the same lines as the report.
- `KEYS["qa-runner"]`: true, the stale pin is gone (`8f37605fb`, ancestor; line 57 reads ``every `surprise:` line``). The `"surprise": "<id>"` left at line 67 is `EXPLORE_X8`, a different charter's pin.
- "14 silent": reproduced at the base (no `finish(`). **"26 / 12 with a tally": not reproduced** by my form: `^def test_` with no `__main__` substring gives 21, so 7 with a tally. Not load-bearing, since the pin is what guards the set, and the difference may be the report's looser filter.
- Windows only: the 14 files have never run on the CI image. No module-level `yaml`/`openpyxl` import or `importorskip` found (control: the same grep hit `pytest.skip`). The canon judges.

## Trail

- Read: the three given files; the diff; `selftest.py` 40-60, 88-125, 147-167, 387-440, 548-760, 906-950, 1039-1080; `harness.py` finish; `test_current_audit_contract.py` 60-95; `.gitlab-ci.yml` 186-250, 284-307; `forge-check.yml`, `nightly.yml`; `docs/SIBLING_MAP.md` axis headings and axis 9; calibration check 13; FR-2, FR-4; `8f37605fb`.
- Probes in the session scratchpad on temp files only: `probe.py`, `probe2.py`, `hyg.py`, `hyg5.py`, `notally.py`. No worktree file was changed.
- A full-package copy could not reach the hygiene step (`git add` hit "Filename too long" in temp), so `hyg5.py` used a tiny repo with the real `cmd_hygiene`, and `hyg4.py` the real selftest on `scripts/*.py`.
- Side observation, `hyg4.py`'s first run: with cwd in the 8.3 temp form (`DEV1~1`) and the file path resolved to the long name, the entry hung until the 300 s ceiling (`timed out after 300s`) and left no cache. Resolving the temp path removed it (5.8 s). The likely cause, not verified, is pytest taking the common parent of the two spellings as rootdir. Not a CI path and not a finding; both background runs have finished.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F1: the 14 entries lack -p no:cacheprovider; pytest leaves .pytest_cache at the package root and cmd_hygiene goes red in every CI selftest job (measured; same class as 8f37605fb)"
  ],
  "fixes": [
    "F1 (blocks): add -p no:cacheprovider to all 14 entries and to ENTRY in test_selftest_ran_nothing.py:21, add a real-directory pin; the Lead corrects the spec form",
    "F2: a 0/0 tally and an all-skipped pytest summary count as ran nothing, with pins; tighten pin row 7 at :85; correct the AR-28 line, or the Lead records the proxy as a decision",
    "F3: replace the _TEST_DEF regex at selftest.py:399 with an ast walk, add a triple-quoted control, correct the comment at :394",
    "F4 (Lead's fork): remove PYTEST_RUN_FILES and shorten the text, or make selftest run listed files itself and name the constant in the text; name AR-9",
    "F5: add a TEST_TIMEOUTS row for test_exit_limit_halt_answered.py; list it, test_brief_pack_sd_head.py and test_probe_gap_door.py in slow_tests.json via --update after the canon",
    "F6: correct four-questions (a) to the real added wall time and (c) to a detector that exists; the Lead corrects the finding's check 13",
    "F7, F8 (small): reuse ST._TEST_DEF, drop the noqa E402 comments and the redundant guards; align or queue the 7 older entry shapes"
  ],
  "class_completeness": "Surface: launching pytest from a test file. All 7 other pytest.main entries carry the flag, so the 14 are the whole set. Neighbouring classes walked on the detector: magnitude n/a; nesting caught (class, nested def); encoding safe (errors=replace); empty and broken input probed (F2, F3). SIBLING_MAP: 32 axes enumerated in the commit; axis 9 n/a stands. Sibling queued by F2: an entry without raise SystemExit is green on a failure (none in the real directory).",
  "trail": {
    "read": [
      "docs/tasks/critic-diff-brief.md",
      "plans/piles/thinking-roles/findings/20261106-testy-pytest-nevidimy-i-sverka-spek.md",
      "docs/tasks/specs/reports/t-2040-tr2-12-report.md",
      "ai-packages/qa-factory/scripts/selftest.py",
      "ai-packages/qa-factory/scripts/tests/test_selftest_ran_nothing.py",
      "ai-packages/qa-factory/scripts/tests/harness.py",
      "ai-packages/qa-factory/scripts/tests/test_current_audit_contract.py",
      "ai-packages/qa-factory/scripts/slow_tests.json",
      ".gitlab-ci.yml",
      "docs/migration/forge-repo/.github/workflows/forge-check.yml",
      "docs/migration/forge-repo/.github/workflows/nightly.yml",
      "docs/SIBLING_MAP.md",
      "PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md",
      "ai-packages/qa-factory/design/factory-rules.md",
      "commit 8f37605fb"
    ],
    "reruns": [
      {
        "command": "python -B D:/ws/wt-tr2-12\\ai-packages\\qa-factory\\scripts\\tests\\test_selftest_ran_nothing.py",
        "result": "=== selftest ran-nothing: 13/13 ok ==="
      },
      {
        "command": "scratchpad hyg5.py: real pytest entry, then real selftest.cmd_hygiene, tiny git repo, both entry forms",
        "result": "as in the diff: .pytest_cache present, FAIL hygiene; with -p no:cacheprovider: no cache, PASS hygiene"
      },
      {
        "command": "scratchpad hyg4.py: real selftest.py --tests --hygiene from the package root on a copy of scripts/*.py plus one test, both entry forms",
        "result": "as in the diff: rc 1, PASS tests, FAIL hygiene .pytest_cache/, 1/2 ok; with -p no:cacheprovider: rc 0, 2/2 ok"
      },
      {
        "command": "scratchpad probe.py and probe2.py: adversarial files through real selftest._test_outcome",
        "result": "0/0 tally, all-skipped and output-at-import files GREEN; a string-only def and a called test_ in working silent scripts RED"
      }
    ]
  }
}
```
