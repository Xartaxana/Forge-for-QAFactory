# t-1058 — critic code review of t-1053 (N2h-v: the critic stub writes its window and ends with the digest)

Reviewed: commit 5b68e59 on `worktree-agent-a40d4c19d9eced40f` (tree `C:/QAFactory/forge-repo/.claude/worktrees/agent-a40d4c19d9eced40f`; HEAD = 5b68e59; origin branch = 5b68e59).
Spec: `docs/tasks/specs/20261117-p1b-n2h-v-critic-stub-window-card.md` Part 2 (§2.1-§2.5) + "Lead decisions on the forks". Brief: `docs/tasks/critic-diff-brief.md`.

**Verdict: accept with fixes** (NEEDS WORK, small): the code meets every §2.1 item and the §2.2 order. Two selftest fixes are owed this round (F1, F2). One thing blocks the merge, and it is the coordinator's step, not the builder's (F4): the CI door named in the DoD never runs the main pass, so E10/E11/E12 have no measurement.

## Findings

**F1 — fix in round. One existing N2h row was weakened by the adaptation (key 3).** The row `N2h: probe timeout (exit -9) -> a journal line says it did not finish, no record` (dry_stub.py ~:1523) uses a lambda that answers `(-9, "probe_by_code.py did not finish within 120 s")` for EVERY script. Since N2h-v that includes `window_record.py`. `record_window` then adds the row `{"why": "window_record.py exit -9: probe_by_code.py did not finish within 120 s"}`, so `"did not finish" in json.dumps(done["live_only"])` holds even when the probe's own timeout row is missing. The row can no longer catch a lost probe timeout row. Witness (scratch probe `.../scratchpad/probe_m9.py`, calling `record_window` alone with that lambda):
```
[{'output': 'work/windows/C5.json', 'why': 'window_record.py exit -9: probe_by_code.py did not finish within 120 s'}]
N2h -9 row predicate met by the window row alone: True True
```
Fix: use `probe_part(done)` in that row's predicate, as the four other adapted rows do, or answer `window_record.py` differently in the lambda. The builder's claim "No expectation about the probe itself was weakened" is false for this row. The other adapted rows were traced and are not weakened: the first N2h row is stricter (exact call list + wrote + `live_only == []`). The rc!=0, F6 and no-selector rows filter only rows whose `why` contains `window_record.py`, so they still assert the probe's own row. The no-instance and no-command rows assert nothing that the window row could satisfy. `never` still raises on any probe call.

**F2 — fix in round. The POSITIONAL invariant "early stops never skip steps 3-4" is asserted for one early stop out of two.** §2.2 last bullet: the early `return out` paths (`:502-503` no tests, `:505-508` no command) must no longer skip the window record. The code keeps this, because `_probe_instances` returns to `critic_branch` (traced). But only the no-instance path has a row (`N2h-v: no instance -> no probe, window_record still runs`). The no-command row (`N2h: a profile without commands`) and the no-selector row run with `never`, which only *permits* `window_record`. They would stay green if `window_record` were skipped on those paths. The report says "rows: no instance, no selector, no command all still run `window_record`", and that overstates what the rows check. Fix: add `done["window_record"]["exit"] == 2` to the no-command row (and to the no-selector row).

**F3 — note (fix in round if cheap). Nothing asserts that the real `manifest_put.py` accepts the critic fragment.** In the table rows, `fake_probe` answers `manifest_put.py` with `0, "ok"`. Its comment says "the real writer is exercised by the process row below", but that process row (`N2h-v: through the process window_record.py ran…`) asserts only `window_record`, never the `manifest_put (story fragment 0)` outcome. The spec makes this a measurement ("the merge keys are measured by manifest_put's answer"). By reading, the shape is consistent with the product: `artifact-contract-automation.md:11-15` puts `critic_verdict` on `tests[]`, and `window_record.py:155/322` reads the manifest row's `critic_verdict`. The only carrier of the measurement is the main pass (F4). Suggested: the process row also asserts that the critic's `manifest_put.py (story fragment 0)` is not in `live_only`, or names its exit.

**F4 — blocks merge (a coordinator precondition, not a builder fix). The cited CI run does not contain the main pass.** Run 44033457046 (dry_only, `success`, checked out 5b68e59, per the job logs) has the jobs `list`, `tables`, `parts (s0)` and `parts (s1-s4)`. `.github/workflows/dry-story.yml` defines only `list`/`parts` (walk groups, `--part exits:<group>`)/`tables`. The main pass (`test_scenario_dry_1.py` default `("main","default")`, :132) is not in that workflow. Grepping the parts logs for `dry-1/main` finds 0 lines. So the lines the card's handoff requires (`dry-1/main/stop`, `main/known_red`, `main/time`) do not exist for this branch. E12 ("no pass that hits the ceiling reaches `main`") and E11 (the wave is code + label) cannot be met from this run. This is a dispatcher-side defect: the DoD named a door that does not run the slow file's main part. Before merge, the coordinator obtains the main lines by a road that runs `--part main` (canon `full`, or the road that produced `20261117-p1b-n2ha-main-lines-r2.txt`), then sends the E11 label step.

**F5 — note. `record_window` alone catches `(OSError, ValueError)` around the runner** (dry_stub.py:508-511). The probe and `manifest_put` calls go through the same runner unguarded. `run_script` maps only `TimeoutExpired` (:197-205), and an `OSError` from `subprocess` would hit every caller alike. The branch is inconsistent with its siblings and has no row. The `exit 0 but file absent` branch (:519-520) also has no row. It is reachable only if the tool lies, so low risk. Either drop the guard or move it into `run_script` (one runner, one error mapping).

**F6 — note. `check_story_fragments` runs twice per branch** (at the top of `critic_branch`/`automator_branch`, and again inside `merge_story_fragments`). The top call is the one that matters (a KitError before any process runs; the E7 rows pass `None` project/task_dir and depend on it). The inner call is redundant but harmless.

**F7 — note (queue candidate, outside this card's scope).** The automator's per-case fragment write + `manifest_put` + `_record` (dry_stub.py:617-625) is a near-twin of `merge_story_fragments`'s body (write under `state/dry-stub-fragments/`, run `manifest_put.py --fragment`, `_record`). The card asked to extract only the story-fragment loop, which was done. A shared `_put_fragment` helper is a possible follow-up, not a defect of this diff.

**F8 — note. The worktree is dirty:** `docs/OWNER_PRINCIPLES_INDEX.md` is modified and uncommitted (the root checkout has the same change; probably generator drift). It is not in 5b68e59. It must not be swept into the wave merge.

## Keys

1. **Items and edges have rows.** V1 has the call-order row; E7 has 3 KitError rows; E8 has the manifest_put-refused row. V2 has rows for: after the probes with `--review-receipt`, exit 1 + file, exit 2 / no file, exit 1 / no file (extra), timeout with a partial file, no instance, and the real process. V3 has the `role_digest.check == []` row. V4 is in the call-order row (the exact list holds no `run_suite.py`). Each new row can fail: the order row compares an exact list; the timeout row writes a file and expects `wrote == []`; the E7 rows depend on the early check. The builder's negative control removed the `record_window` call → 12 FAILs (in the report, consistent with the rows). No row: the exit-0-no-file branch and the OSError branch (F5). E9 has no own row, but its stub behaviour is the exit-1/2 branch, which is covered. E2, E3 and E10-E13 are not stub code (E10-E13: F4). The no-command early stop has no window row (F2).
2. **POSITIONAL holds in code** (traced): `fill_role` :946-955 writes `files` → `critic_branch` (= `_probe_instances` → `merge_story_fragments` → `record_window`) → `_fill_form` → `handoff_check --fix` → `result_text`. The window file exists before the form. A refusal, timeout or unknown becomes a `live_only` row: -9 is checked before the file (`present = code != -9 and ...`), and nothing in `wrote` (AR-28). The stub never writes `receipt_ref`; `--fix` derives it. The early stops fall through (F2: assertion missing for no-command).
3. **The adaptation weakened one row: the N2h -9 timeout row (F1).** The rest were traced and are not weakened.
4. **AR-n hold.** AR-14 (the only manifest writes are `manifest_put.py` processes), AR-13 (no `receipt_ref`/`runtime_provenance` typed by the stub; grep of the diff), AR-22, AR-28 (above), AR-29/FR-58 (window, receipt and probe come from real processes through `run_script` → `harness.run_script` → `subprocess.run`; verdict and digest are story.json data, never derived from tool output), AR-15/AR-19 (one fragment function used by both twins, one runner). `judgment: none` is true: the diff adds no product check, only selftest rows.
5. **Duplication and quality.** One fragment function, one runner; the old automator loop is removed, not cloned (diff traced). The new functions are short (`record_window` ~20 lines, `critic_branch` 7). Notes: F5, F6, F7. Searched: `dry-stub-fragments`, `"manifest_put.py"`, `except (OSError, ValueError)` in dry_stub.py.
6. **Class completeness.** Of the shipped role cards, only `agents/qa-code-critic.md` names `window_record` (grep -il over `agents/*.md`), so no other role stub owes a window record. `manifest_put --fragment` is named by the automator (already through the shared function) and the critic (now). Axis 5 (twins) is covered, and so is axis 34 (one road): no `run_suite` call by the critic, no language/project branch in the new code. None found: grepped `window_record|--fragment` in agents/. The F7 twin is outside the card.
7. **The expectation is sound by code; it is not measured.** `run_suite.build_run_block` returns None for `purpose == "red_probe"` or `evidence_phase == "baseline"` (run_suite.py:470-473). `probe_by_code.py` runs `--request` with a `red_probe` request (docstring :13-16). `red_sandbox._run_mine` passes `--purpose red_probe` for the baseline and for the mutated run alike (red_sandbox.py:1260, 1680-1686). `handoff_check.window_runtime_record` (:525-550) wants a block of THIS dispatch carrying `runtime_provenance`. The critic card has no `--mine` (qa-code-critic.md:69). So no tool on the critic's road produces it: a product gap (FR-5/FR-11/AR-22), not a stub gap. Note for the product finding: `_RECORD_PRODUCER` (handoff_check.py:522) tells the critic "written by runtime_probe.py when run_suite runs this dispatch's tests", which is a door the critic is not handed (FR-2). The measurement is owed (F4).

Standing lines: **DUPLICATION AND CONSISTENCY**: none blocking (F5 inconsistency, F7 twin queued as a candidate). **CODE QUALITY**: no function over 60 lines in the new code, no dead branch except F5. **ONE ROAD**: none found (searched the diff for language/runner/project-name branches; none). **TESTS**: the `tests-over:` line is present, and its reason holds (the card lists the rows); killing power is shown by the negative control; F1 and F2 are the gaps. **JUDGMENT**: none moved into code.

## Trail

- Read: the spec card (whole); critic-diff-brief.md (items 1-12, return form); `git show 5b68e59` (whole diff); the builder report; dry_stub.py :190-210, :450-560, :600-630, :940-990, selftest :1430-1630; harness.run_script :232-240; run_suite.py :462-478; probe_by_code.py :10-18; red_sandbox.py :1250-1262, :1672-1690; handoff_check.py :522-550; manifest_put.py :1085, :1286-1310; window_record.py critic_verdict grep; artifact-contract-automation.md :9-16; agents/*.md grep; `.github/workflows/dry-story.yml` :1-60; test_scenario_dry_1.py :56-62, :132.
- Reruns: `python -B <tree>/ai-packages/qa-factory/scripts/tests/dry_stub.py --selftest` → 13 `PASS N2h-v:` rows, `=== dry_stub --selftest: 218/218 ok ===` (matches the witness). CI `ci_read.py jobs 44033457046` → list/tables/parts(s0)/parts(s1-s4) success, no main job. The tables log shows `218/218 ok`; the parts logs contain `5b68e59…`; `--grep dry-1/main` returns 0 of 239 lines. Scratch probe `C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\501cb4e0-b55f-46d8-9262-11b1caefad61\scratchpad\probe_m9.py` → the output quoted in F1.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F4 (coordinator precondition): CI run 44033457046 (dry_only) has no main-pass job; dry-1/main/stop, main/known_red, main/time are unmeasured, so E10-E12 cannot be judged; obtain a --part main run before merge, then the E11 label step"
  ],
  "fixes": [
    "F1: dry_stub.py N2h probe-timeout row (~:1523) - use probe_part(done) in the 'did not finish' predicate (the window_record row now satisfies it alone)",
    "F2: add done['window_record']['exit'] == 2 to the N2h no-command row (and the no-selector row) so the early-stop fall-through is asserted",
    "F3 (if cheap): the N2h-v process row asserts the real manifest_put story-fragment-0 outcome of the critic call"
  ],
  "class_completeness": "Only agents/qa-code-critic.md names window_record (grep -il over agents/*.md); the manifest_put --fragment roads of the automator and critic now share merge_story_fragments; axis 5 and axis 34 covered; the automator per-case fragment write (dry_stub.py:617-625) is a near-twin left as a queue candidate outside the card",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-p1b-n2h-v-critic-stub-window-card.md",
      "docs/tasks/critic-diff-brief.md",
      "git show 5b68e59 (worktree agent-a40d4c19d9eced40f)",
      "docs/tasks/specs/reports/20261117-p1b-n2h-v-report.md (worktree)",
      "ai-packages/qa-factory/scripts/tests/dry_stub.py (worktree, branches and selftest_n2)",
      "ai-packages/qa-factory/scripts/tests/harness.py:232-240",
      "ai-packages/qa-factory/scripts/run_suite.py:462-478",
      "ai-packages/qa-factory/scripts/probe_by_code.py:10-18",
      "ai-packages/qa-factory/scripts/red_sandbox.py:1250-1262,1672-1690",
      "ai-packages/qa-factory/scripts/handoff_check.py:522-550",
      "ai-packages/qa-factory/scripts/manifest_put.py:1085,1286-1310",
      "ai-packages/qa-factory/references/artifact-contract-automation.md:9-16",
      ".github/workflows/dry-story.yml:1-60",
      "ai-packages/qa-factory/scripts/tests/test_scenario_dry_1.py:56-62,132"
    ],
    "reruns": [
      {"command": "python -B <tree>/ai-packages/qa-factory/scripts/tests/dry_stub.py --selftest", "result": "218/218 ok, 13 PASS N2h-v rows"},
      {"command": "python -B tools/ci_read.py jobs 44033457046", "result": "list, tables, parts (s0), parts (s1-s4) success; no main-pass job; tables log 218/218 ok; parts logs show 5b68e59; grep dry-1/main 0 lines"},
      {"command": "python -B scratchpad/probe_m9.py (record_window with the -9 lambda)", "result": "window row why contains 'did not finish'; the N2h timeout predicate is met without the probe row"}
    ]
  }
}
```
