# N2h-v report (t-1053): the critic stub writes its window and ends with the digest

Branch: worktree-agent-a40d4c19d9eced40f. Files: `ai-packages/qa-factory/scripts/tests/dry_stub.py`, `.../fixtures/stories/dry-1/story.json` (row `qa-code-critic@S5` only), `ai-packages/qa-factory/changelog.d/p1b-n2h-v-critic-window.md`, this report.

## Items of section 2.1 (file:line in dry_stub.py of this branch, selftest row)

- V1, one fragment road: `check_story_fragments` :483, `merge_story_fragments` :490 (the automator's loop moved into it; `automator_branch` calls it :628, `critic_branch` :540). Story row `qa-code-critic@S5.manifest_fragments` = the one `critic_verdict: approved` fragment. Rows: `N2h-v: the critic's story fragment goes through manifest_put.py before window_record.py (call order; no run_suite call)`; E7 rows (three bad shapes -> KitError naming `qa-code-critic@S5.manifest_fragments`); E8 row `manifest_put refuses the critic fragment`. The N2e rows of the automator are unchanged and green.
- V2, window record: `record_window` :503, called :541; `fill_role` passes the story fragments and copies `row["window_record"]` (:949). Rows: `window_record runs after the probes with --review-receipt; work/windows/<dispatch>.json exists before the form`; `exit 1 -> the file it wrote stays, live_only names exit 1`; `exit 2 / no file`; `exit 1 / no file`; `timeout -> live_only, nothing in wrote (a partial file never counts)` (-9 is checked before the file); `no instance -> no probe, window_record still runs`; `through the process window_record.py ran on the world and its answer is a row`.
- V3, digest: story.json `qa-code-critic@S5.result_text` as in the spec, no code change. Row `the story's qa-code-critic@S5 digest passes the product's digest check for scope [TC-1]` (`role_digest.check == []`).
- V4, no `run_suite`: covered by the call-order row (call list has no `run_suite.py`).

## Order of section 2.2 (kept)

files (fill_role, unchanged) -> `_probe_instances` (the old probe body, early stops now fall through) -> `merge_story_fragments` -> `record_window` -> `_fill_form` -> `handoff_check --fix` -> `result_text`. `critic_branch` is now a three-step function; the early `return out` paths no longer skip steps 3-4 (rows: no instance, no selector, no command all still run `window_record`).

## Existing rows changed (needed by the new always-run window step; not new behaviour of old checks)

The N2h-a rows call `critic_branch` with fake runners: `fake_probe` now also answers `window_record.py` (writes the file) and `manifest_put.py`; `never` forbids only `probe_by_code.py` and answers `window_record.py` with exit 2/no file; a helper `probe_part` filters the window row out of `live_only` in four rows; the first N2h row's expected call list and `wrote` add the window call and `work/windows/C5.json`. No expectation about the probe itself was weakened.

## FR pass

A - refusals: a window_record or manifest_put refusal is a `live_only` row with the tool's text cut at 400, never a filled field (E4-E8); no new refusal text of the product. B - no text for a person. C - the producer of `work/windows/<dispatch>.json` is the tool, the reader `handoff_check --fix` (AR-13, AR-22); the form is never typed. D - no identifier made here. E - n/a. F - added time estimated below, not measured. G - applied: English only, no control bytes (`selftest.py --lang` green), one runner `run_script`, one fragment function, no heredoc code in the package.
AR-n: AR-14 (manifest written only by manifest_put.py), AR-28 (refusal/timeout/unknown is a journal line), AR-29 (window, receipt and probe are the tools' data; verdict and digest are story data), AR-13, AR-22, AR-15/P31 (one fragment function, one runner), AR-19 (automator/critic twins).

## Time and stop rule

Expected added time: +5..20 s in the S5 critic call (two processes), card estimate, not measured; S5 was 68.2 s and the pass 266.6 s. If `dry-1/main/time` exceeds 800 s (E12) there is no merge and the Lead decides under F-P18.

## Expectation (NOT RUN): `dry-1/main/stop`

By the card the pass stops at S5 with ONE finding, `probes.runtime_provenance` (no run block of dispatch S5-qa-code-critic-1 carries a runtime_provenance record; product gap candidate, A11, F2 (a)). Not measured by me: the slow door is the coordinator's. The label `main/S5 -> FV3-5` then needs the E11 label step.

## Witness (verbatim)

Command: `python -B ai-packages/qa-factory/scripts/tests/dry_stub.py --selftest`
```
PASS N2h-v: the critic's story fragment goes through manifest_put.py before window_record.py (call order; no run_suite call)
PASS N2h-v: window_record runs after the probes with --review-receipt; work/windows/<dispatch>.json exists before the form
PASS N2h-v: window_record exit 1 -> the file it wrote stays, live_only names exit 1
PASS N2h-v: window_record exit 2 / no file -> live_only, nothing in wrote
PASS N2h-v: window_record exit 1 / no file -> live_only, nothing in wrote
PASS N2h-v: window_record timeout -> live_only, nothing in wrote (a partial file never counts)
PASS N2h-v: no instance -> no probe, window_record still runs (its own gap is the tool's line)
PASS N2h-v: manifest_put refuses the critic fragment -> a live_only row, window_record still runs, no retry
PASS N2h-v: the critic's `manifest_fragments` as a string is a KitError naming qa-code-critic@S5.manifest_fragments
PASS N2h-v: the critic's `manifest_fragments` as an empty object in the list is a KitError naming qa-code-critic@S5.manifest_fragments
PASS N2h-v: the critic's `manifest_fragments` as an object, not a list is a KitError naming qa-code-critic@S5.manifest_fragments
PASS N2h-v: the story's qa-code-critic@S5 digest passes the product's digest check for scope [TC-1]
PASS N2h-v: through the process window_record.py ran on the world and its answer is a row (exit and text; the file is in wrote only on exit 0/1)
=== dry_stub --selftest: 218/218 ok ===
```
(Before the change the file had 205 rows; the 13 `N2h-v:` rows are the added ones.)

Negative control (byte copy of dry_stub.py taken before the edit, sha256 0b6799f9877a8997...; the call `record_window(...)` in `critic_branch` replaced by `pass` with sed; restored FROM the copy, sha256 0b6799f9877a8997... identical before and after). Result: 206/218 ok; the row asked for:
```
FAIL N2h-v: window_record runs after the probes with --review-receipt; work/windows/<dispatch>.json exists before the form — expected (['work/windows/V1.json'], True, [['--task', 'DRY-1', '--dispatch', 'V1', '--review-receipt']]), got (['work/automation-manifest.json'], False, [])
```
(the order row and the other window rows fail too, 12 FAIL lines in all).

`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/dry_stub.py` prints, besides ratchet NOTE lines:
```
scripts/tests/dry_stub.py: keep test_scenario_dry_1.py (layer scenario, covers it)
```
The only file it names is the slow one, not run by me. No non-slow file to run.

`python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check`: `dry_exits --check: 0 discrepancies`
`( cd ai-packages/qa-factory && python -B scripts/selftest.py --lang )`: `PASS lang: no control byte left by an eaten escape sequence (FR-29)` / `=== qa-factory selftest: 2/2 ok ===`

## Noted, not fixed

- tests-over: the diff adds ~130 selftest lines (13 rows) against the card's list; every row is a row of the existing N2h section of the selftest, no new file.
- The through-the-process row accepts either outcome (as the card says); I did not read which exit `window_record.py` gives in the bare world.
- Analog: `critic_branch`'s docstring and the card text still say "probe only" in the module header text (not checked); `dry_world.py` or docs naming `critic_branch` as probe-only were not searched.
- Spec fact: the card says `automator_branch`'s loop is at `:577-582`; on this tree it is the same code, now at :628 as a call.

## Needed beyond the manifest

Only the selftest region of `dry_stub.py` (existing N2h rows) and `role_digest.check`; no other file.

## Fix round (attempt 2)

Merged origin/main first (merge commit 2296cdad, no conflict). Then, in `dry_stub.py`:

- F1: row `N2h: probe timeout (exit -9) -> a journal line says it did not finish, no record` now judges `probe_part(done)`, so the window_record row cannot satisfy it.
- F2: rows `N2h: a profile without commands -> ... and the early stop still ran window_record (exit 2 from the spy)` and `N2h (c): a manifest row with no selector ...` also assert `done["window_record"]["exit"] == 2` (field `window_record.exit`, read via `.get`, so a skipped record FAILs). `never` still raises on any probe call.
- F3: the process row `N2h-v: through the process window_record.py ran on the world ...` also asserts `live_only` holds no `manifest_put.py (story fragment` row. The real `manifest_put.py` ACCEPTED the fragment (row passes); no refusal to report.
- F5: the `(OSError, ValueError)` guard moved from `record_window` into `run_script` (exit 127, text `<script> could not be launched: <Type>: <msg>`); `never` is not wrapped (E2). New rows: `N2h-v (F5): run_script maps a failed launch the same for probe, manifest_put and window_record ...` (one parameterised row over three scripts) and `N2h-v (F5): window_record exits 0 but the window file is absent ...`.
- F6: the inner `check_story_fragments` call removed from `merge_story_fragments` (the `tag` parameter is now unused, kept in the signature); the call stays at the top of both branches; the three E7 rows pass unchanged.

Verbatim runs:
- `dry_stub.py --selftest` -> `=== dry_stub --selftest: 220/220 ok ===` (was 218; +2 rows)
- `dry_exits.py --check` -> `dry_exits --check: 0 discrepancies`
- `selftest.py --lang` -> `PASS lang: no control byte left by an eaten escape sequence (FR-29)` / `=== qa-factory selftest: 2/2 ok ===`
- Negative control 1 (byte copy before, sha256 prefix a891b3bd51b0b992; mutation: the probe's -9 row popped, window row kept): `FAIL N2h: probe timeout (exit -9) -> a journal line says it did not finish, no record - expected ([], True, False), got ([], False, False)` / `219/220 ok`. Restored from the copy: hash a891b3bd51b0b992 = a891b3bd51b0b992.
- Negative control 2 (mutation: record_window skipped when `no_command` is set): `FAIL N2h: a profile without commands -> ... and the early stop still ran window_record (exit 2 from the spy) - expected (True, [], [], False, 2), got (True, [], [], False, ...` / `219/220 ok`. Restored, hashes equal (a891b3bd51b0b992).

Corrections of the two overstated sentences:
- "No expectation about the probe itself was weakened" was false: the -9 timeout row was weakened by the window row (F1); fixed here.
- "rows: no instance, no selector, no command all still run window_record" overstated: only the no-instance row asserted it; the no-command and no-selector rows only permitted it (F2); they now assert it.

Noted analogs: F7 (shared `_put_fragment` helper) not done, per non-goals. `merge_story_fragments` now has an unused `tag` parameter (left to keep call sites unchanged).
