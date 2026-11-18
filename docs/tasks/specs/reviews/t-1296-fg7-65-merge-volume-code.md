# t-1296 / forge/7/FG7-65 — critic review of fccc53ce (wave.py merge test-volume refusal)

Reviewed: `git -C C:/QAFactory/forge-repo/.claude/worktrees/fg7-65 show fccc53ce` (tools/wave.py +80/-4, tools/test_volume.py, tools/test_wave.py +38, tools/test_test_volume.py).

## Verdict

**NEEDS WORK** (accept with fixes). 1 blocking finding (F1), 4 to fix before merge (F2-F5). The decision to accept belongs to the Lead.

## Findings

**F1 (blocks) — `tools/wave.py::Wave.check_volume` (`volume_done` memo): an over-budget origin tip is merged unchecked.**
`locked()` checks the LOCAL tip first (`check_volume_local`), which sets `volume_done = True`. The later `check_volume(sha)` on the ORIGIN tip is then skipped. `publish_branch` returns silently when the local branch is an ancestor of origin's (wave.py:268), so origin's tip is what gets merged, and nobody has checked it.
Reproduction (my probe B, temp repos built with test_wave's `env` and `branch` helpers): the branch `ah` with +2 product lines is pushed, and the root gets the local `ah` = that commit. Then dev pushes one more commit to origin/ah with +9 test lines (9 > 2). `Wave(..., "ah").run()` prints only `pushed: 76b24b24…` and no TEST VOLUME line, gives rc=0, and `MERGED: True`.
With `--sha <origin tip>` the local `check_pin` refuses first, so the hole is open only without `--sha`. The tool allows that and the spec does not require `--sha`.
What must hold after the fix: the tip `merge_and_push` merges has been judged exactly once, either refused, passed, or reported as `not checked`. Example fix: memo keyed by tip (`self.volume_tip == tip`) instead of a bool. A second `not checked` line on a second distinct tip is acceptable. Or compute the volume only on the tip that will be merged.

**F2 (fix before merge) — `tools/wave.py::Wave.check_volume`: a non-ASCII path is octal-quoted by git and misclassified, which gives a FALSE refusal.**
Without `core.quotepath=false`, numstat prints `"tools/p\303\251.py"`. `classify` sees a leading `"` and returns excluded. Probe E: 3 test lines + 9 product lines in `tools/pé.py`. The raw numstat is `'9\t0\t"tools/p\\303\\251.py"\n3\t0\ttools/tests/t.py'`, and the result is `refused: TEST VOLUME: … +3 test lines vs +0 product lines`. The error goes in the blocking direction, and before this diff it was only a WARN.
Q6: the repo already has the road for this, `tools/gitcmd.py:42` (`-c core.quotepath=false` always on). Fix: pass `-c core.quotepath=false` to the numstat call, or use gitcmd. Class sibling (Q4, same classifier input): `tools/test_volume.py::run` line 135 `_git("diff", "--cached", "--numstat", "-M")` has the same defect (it only WARNs wrongly there). Fix both in this round.

**F3 (fix before merge; spec divergence, the fork is the Lead's) — `tools/wave.py::Wave.check_volume`: the door is dropped when the budget is not exceeded OR not known (K2 a/b).**
The spec says: "with the door the merge is always `--no-ff` and its message carries `tests-over: <reason>`". The code sets `over_line` only when t > p.
- Probe D (door, 0 test / 2 product): plain fast-forward, message `'wd'`, no trailer.
- Probe C (door, numstat fails): `test volume: not checked (… boom)`, then merged with message `'nf'`. The Lead's reason is lost exactly when the tool cannot count. This is an unknown turned into a silent pass of the record (FR-41 direction).
Fix: whenever `--tests-over` is given and a merge commit is made, write the trailer and force `--no-ff`. This also removes the special print branch. If the Lead prefers the builder's reading, the spec line must be amended. Either way the choice is the Lead's.

**F4 (fix before merge) — `tools/test_wave.py::test_test_volume_budget_and_door`: the "before any push" road for a LOCAL branch has no row (K1, K6).**
Every row uses `branch()`, which pushes from `dev`. The root never has `refs/heads/v1`, so `check_volume_local` never runs in any test. Deleting `check_volume_local` (or the `volume_done` dedupe) leaves all 11 rows green, judged by reading: `rev-parse --verify refs/heads/v1` fails in the root, so the function returns at its `if rc == 0`.
I checked this shape by hand. Probe A (local-only branch `lo`, 5/2): refused, `origin has lo: ''`, main unmoved. So the code is correct today but unguarded.
The local-only shape is the one behaviour (1) exists for ("origin untouched"), and it is stronger than either row the builder left unwritten. Fix: one more parameter row (`over no-door, local only`) that commits in `env.root` and asserts origin has no such branch. Its assertion `g(env.origin,"rev-parse","v1") == g(env.dev,"rev-parse","v1")` is trivially true in the present rows (dev pushed it). In the local row, assert absence on origin instead.

**F5 (fix before merge) — `tools/test_wave.py::test_tests_over_input_battery_is_checked_before_the_lock`: 4 refused rows build a full git world they never use (Q5 f/g, K7).**
The refusal happens in `wave.main` before `Wave` is built. `check-ref-format --branch` needs no repository with the branch. For those rows, `origin_main(env) != main0` is trivially false. Measured: these rows cost 1.4-3.3 s call + 2.0-3.9 s setup each, and the AT-300 row 16.1 s. Fix: the refused rows run without the `env` fixture (a bare `tmp_path` as `--repo`, assert rc 2 + text). Keep the world only for the accepted AT row. While there, add the AT-lower row (1 character, accepted) and a strip-before-length row (`" " + "x"*300`, accepted). The spec states "1–300 characters after strip", and today only the upper AT and the beyond rows exist (K5).

## Key answers

- **K1 — FINDING F1 (blocks).**
  - Local-not-on-origin: refused before the push (probe A).
  - Already on origin: refused (row `over no-door`).
  - `--sha` pin: the pin check runs before the volume check on both tips.
  - The skip road is `volume_done` when origin is ahead of local (F1).
  - `branch == MAIN` is unreachable (`locked` refuses main anyway).
  - The ancestor shortcut only fires when the tip is already in origin/main. There `origin/main...tip` would be empty (0/0, a pass), and `merge_and_push` prints "nothing to merge". This is not a skip of an over-budget branch.
- **K2.**
  - (a) and (b): FINDING F3.
  - (c): not a defect. `door_problem` validates piles' grammar (items, `DOOR_RE`). The tests-over check is a length/one-line check. The shared part is two expressions (`strip`, the `\n`/`\r` refusal). No helper to reuse: I grepped `tests-over` across tools/*.py; the only other reader is `tools/test_volume.py::door_reason`.
  - Q7 copy, minor, folded into F1's rewrite: `check_volume_local` repeats `check_pin_local` line for line (wave.py:213-222). One `local_tip()` read would serve both.
- **K3 — mostly PASS; FINDING F2.**
  - Probe F (branch merged main into itself after main gained 50 test lines): no volume line, rc 0. The 50 lines are not counted, so the merge-base is right.
  - Probe G: the raw numstat is `'-\t-\ttools/b.bin\n-\t-\ttools/c.bin\n1\t0\ttools/p.py\n1\t0\ttools/tests/{old.py => new.py}'`. The rename counts its +1 added line, binary rows are skipped, the deleted binary adds 0, and there is no crash. rc 0.
  - A deleted test file adds 0 (numstat col 1 = 0); `has_tests` on a missing blob gives False (product, 0 lines).
  - Crash surface: `sum_numstat` is inside try/except, and `git()` catches OSError/SubprocessError.
- **K4 — PASS.**
  - Message with both doors (probe): `'wave: merge x (t-868)\n\npiles-skip: \u0430 -- r\ntests-over: why'`. The order is piles-skip then tests-over, one block after a blank line.
  - Readers: `tools/piles.py:135` `DOOR_RE` is `re.M`, anchored per line, kw `piles-skip`, so a following `tests-over:` line neither matches nor breaks it. `door_lines` (piles.py:1025) uses finditer per match.
  - `tools/test_volume.py::decide` never warns on a merge.
  - `--no-ff` forcing: `merge()` is the only merge call (wave.py:301). The `--ff-only` road is gated on `over_line is None`, and the row `over door` asserts exactly one merge commit on a branch that could fast-forward. Complete. The F3 cases are by design of the builder, not a leak.
- **K5 — partial; F5 covers the missing AT-lower / strip rows.**
  - A reason starting with `-`: argparse `error: argument --tests-over: expected one argument`, SystemExit 2, before the lock (probe). `--tests-over=-x` passes, which is acceptable.
  - Non-ASCII reason: written verbatim (probe: `'…tests-over: r\xe9ason \u043f\u0440\u0438\u0447\u0438\u043d\u0430'`), and `streams.utf8_stdio` covers the console.
  - Repeated flag: the last one wins silently (probe). This is the same as `--piles-skip`/`--sha`. Not a finding.
  - Encoding neighbour walked: wave refuses only `\n`/`\r`, while `test_volume.door_reason` splits on `str.splitlines` (`\x0b`, `\x0c`, `\u2028`…). A reason with those would read back truncated. It is unreachable from a real shell argument in practice, so I record it as an observation, not a finding.
- **K6.**
  - Budget: 38 added test lines in test_wave.py + 1 changed line in test_test_volume.py, against about 80 product lines. Within the budget.
  - The rows: `equal`, `zero tests` and `zero product` are spec-named edges, so they are kept. The battery is outside input.
  - Killing power: the numstat row asserts `count == 1`, but with no local branch the dedupe is never exercised (see F4).
  - Of the two unwritten rows, "the door within the budget" becomes a needed row once F3 is decided (it pins the trailer behaviour). "The tip already in main" is weaker than every written row (the empty three-dot diff passes anyway). The local-only row (F4) is stronger than both.
  - Expected values trace to the spec (numbers from the test's own input, the trailer text from the spec).
- **K7 — measured.** `test_test_volume.py` whole: `27 passed in 5.28s`. The three new functions in test_wave.py: `11 passed, 78 deselected in 116.12s`. That is about 19% of the builder's 597 s for the whole file, which is noticeable. The heaviest rows are numstat 17.9 s, battery AT-300 16.1 s, and `over door` 7.9 s. The cheap cut is F5.

## Standing questions

- Q1 fit: F1 (refusal skipped), F3 (door "always"). The rest is as written.
- Q2 builder decisions: F3 is unsafe in the record direction. K2(c) is fine.
- Q3 seams: additive. The `merge()` message building is extended without reordering. By reading, the piles-skip line is unchanged when `over_line` is None (that row was not in my -k run; the probe with both doors shows the shape).
- Q4 class completeness: the F2 sibling `tools/test_volume.py::run` is named, same round.
- Q5 tests: F4, F5. No rewritten or deleted rows. No duplicate rows found (grepped `test_volume|tests_over|numstat` in test_wave.py; the only hits are the 3 new functions).
- Q6 DUPLICATION AND CONSISTENCY: `tools/gitcmd.py:42` should have been used or mirrored for quotepath (F2). The classifier is reused (`tv.sum_numstat`, `tv.TEST_DEF_RE`). No second definition: grepped `def test_|class Test` regex forms in wave.py, and the only hit is the `tv.TEST_DEF_RE` reference. `has_tests` mirrors `tv.staged_blob_has_tests` with a different blob source (tip vs index), which is justified.
- Q7 CODE QUALITY: `check_volume` is about 35 lines with nesting at most 2. The duplicate local-tip read is noted under K2. No dead branches beyond F3's print branch.
- Q8 hygiene: forge tools, not the package. N/a.
- Q9 ratchets: none touched (the 4 files in the diff are none of the axis-18 carriers).
- Q10 architecture: forge tool, `architecture: none` holds. VARIETY: n/a (no package stage).
- Q11 judgment: a count-based refusal authorised by the owner's word 17.11 (quoted in the commit), outside the census scan root. Nothing moved.
- Q12 ONE ROAD: none found. One classifier is shared by the hook and the merge. Grepped `numstat|sum_numstat` across tools/; the only consumers are wave.py and test_volume.py, plus r3_integration_check's own log reader, which is not a test/product classifier.

## Fixes (for a builder)

1. `tools/wave.py::Wave.check_volume`: memo by tip, not by bool. After the fix the merged tip is always judged. Add the row from fix 4 (origin ahead of local, over budget, gives a refusal).
2. `tools/wave.py::Wave.check_volume` and `tools/test_volume.py::run`: numstat with `-c core.quotepath=false`. After the fix a non-ASCII product path counts as product.
3. `tools/wave.py::Wave.check_volume`/`merge`: the door given gives the trailer and `--no-ff` on every merge commit (or the spec is amended by the Lead).
4. `tools/test_wave.py::test_test_volume_budget_and_door`: add a local-only over-budget row (origin has no branch afterwards) and an origin-ahead-of-local row.
5. `tools/test_wave.py::test_tests_over_input_battery_is_checked_before_the_lock`: refused rows without the git world; add the 1-char and the `" "+"x"*300` accepted rows.

## Trail

- Read: `git show fccc53ce` (full diff); `tools/wave.py` 76-325 and 586-695; `tools/test_volume.py` 1-140; `tools/test_wave.py` 1-104 and 719-758; `tools/piles.py` `DOOR_RE` (135) and `door_lines` (1025-1054); `.githooks/commit-msg`; `tools/journal_lock.py::_git_env`.
- Greps (case-insensitive): `piles-skip|tests-over` over *.py/*.sh/*.yml; `--numstat|quotepath|sum_numstat` over tools/. Positive control: the same searches found the new sites in wave.py:232 and test_wave.py:755.
- Probes: stdin Python scripts with no files written. They drive `test_wave.env.__wrapped__` in temp dirs and produce A-G plus the doors/argparse outputs quoted above. They were not committed, and nothing in the worktree was changed.
- `python -m pytest <wt>/tools/test_test_volume.py -q --durations=0` gave `27 passed in 5.28s`.
- `python -m pytest <wt>/tools/test_wave.py -q -k "test_volume or tests_over or numstat" --durations=0` gave `11 passed, 78 deselected in 116.12s (0:01:56)`.
- The mechanical layer (forge-check job, ratchets) is not attached. Per rule 21 it is not re-run here.

```json
{
  "verdict": "blocker",
  "blockers": [
    "F1 tools/wave.py::Wave.check_volume: volume_done set by the local-tip check skips the origin tip; origin ahead of local with +9 test vs +2 product merges unchecked (probe B, rc 0, MERGED True)"
  ],
  "fixes": [
    "F1 tools/wave.py::Wave.check_volume: memo by tip, the merged tip always judged",
    "F2 tools/wave.py::Wave.check_volume and tools/test_volume.py::run: numstat with -c core.quotepath=false (non-ASCII product path falsely refused, probe E)",
    "F3 tools/wave.py::Wave.check_volume/merge: a given --tests-over writes the trailer and forces --no-ff on every merge commit, including within budget and numstat failure (or the Lead amends the spec)",
    "F4 tools/test_wave.py::test_test_volume_budget_and_door: add local-only over-budget row and origin-ahead-of-local row",
    "F5 tools/test_wave.py::test_tests_over_input_battery_is_checked_before_the_lock: refused rows without the git world; add 1-char and strip-before-length accepted rows"
  ],
  "class_completeness": "quotepath sibling tools/test_volume.py::run (same classifier input) named for the same round; piles-skip readers (piles.py DOOR_RE re.M) unaffected by the second trailer line",
  "trail": {
    "read": [
      "git show fccc53ce",
      "tools/wave.py 76-325, 586-695",
      "tools/test_volume.py 1-140",
      "tools/test_wave.py 1-104, 719-758",
      "tools/piles.py 135, 1025-1054",
      ".githooks/commit-msg",
      "tools/gitcmd.py 19-42 (grep)"
    ],
    "reruns": [
      {"command": "python -m pytest tools/test_test_volume.py -q --durations=0", "result": "27 passed in 5.28s"},
      {"command": "python -m pytest tools/test_wave.py -q -k test_volume or tests_over or numstat --durations=0", "result": "11 passed, 78 deselected in 116.12s"},
      {"command": "stdin probes A-G on temp repos via test_wave.env", "result": "A refused origin untouched; B merged unchecked; C and D no trailer; E false refusal +3 vs +0; F and G counted correctly"}
    ]
  }
}
```
