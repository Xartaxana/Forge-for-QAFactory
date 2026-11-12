# t-190 — critic of code: OF3-1 node c (builder t-183), diff c089e17..wip/of3-1c (6fbeb28, 38de220)

Spec: `docs/tasks/specs/t-129-of3-1-knowledge-catalog.md` §5 items 6 and 7 (node c), §4, node c row, §8, §9. Lead decisions (1) and (2) from the dispatch.

## Verdict

**fit_with_fixes (NEEDS WORK).** No blocking defect in the code. The code changes match items 6(b) and 7 as written, and both Lead
decisions. The control re-runs match the builder's witness. My red probe on the scheduler shows the writer rows go red on the
pre-diff scheduler. Two things are owed before acceptance. F1: item 6(a)'s census is not in what I was given, and it is a named
DoD deliverable. F2: the `_apply_budget` configured-root store path has no row. The class-completeness gaps (Q1, Q2) belong to the
Lead's carriers, not to this builder. The decision to accept is the coordinator's (rule 6).

## Findings (by severity)

**F1 — medium, owed before acceptance (DoD gap, no code fix).** Item 6(a) says "the builder attaches a grep census of every
project-config read in `scripts/*.py` ... with a verdict per site". The spec's DoD (§5 "DoD (every node)") says: "acceptance = the
node's rows green + the census/report lines attached". It is not in the dispatch's given list or witness. It is not in a file on `main`
or the worktree either. Search: `find docs plans .claude/worktrees/of3-1c -newermt "2026-11-12 21:00" | xargs grep -li census`. The
only hits are compact snapshots and the t-180/181/182 reviews, none of them node c's census. Positive control: `grep -c -i census`
on the spec gives 22. The census matters for more than form. N-r1, N-r2, N-r4 and f's baseline read their owns off it. My own grep
found a `test_data` reader that bypasses the reader (`app_card.py:247`, Q3) and a direct config read in the scheduler
(`execution_scheduler.py:230`, Q4). Neither is named in the spec, so only the census can show whether they are already counted.
Fix: the coordinator attaches the builder's census to acceptance, or sends it back as a fix round of t-183 (report only, no code).

**F2 — low, fix before merge (test gap, brief item 5).** `execution_scheduler.py:356` (`task_root = artifacts / req["task"]` in
`_apply_budget`) is not covered under a configured root. The only `_apply_budget` row (`test_config_projection.py:349-359`) is the
broken-config raise. The configured-root row goes through `execute_schedule`, and there `load_run_budget` is not stubbed. So
`_apply_budget` returns at `policy is None` unless the machine has a run budget. Concretely: revert only :356 back to
`project_root / "qa-factory" / "artifacts" / req["task"]` and keep :351, and every row stays green. In a budgeted project, a job
already completed under the configured root would then be missed by `store.read` and charged or launched again. That is the
split-store defect F12 exists for. Fix: one row in `artifact_root_rows`. Stub `er.load_run_budget` as the broken-config row does.
Use `{"artifact_root": "stories"}` with a completed job written under `stories/S-1/state/execution-jobs`. Assert that
`es._apply_budget(plan["requests"], proj)` returns the item in `kept`.

**F3 — low, queue (FR-37 neighbour, outside owns).** `brief_pack.py:2901-2911` `_approach_documents` now lists names from
`RP.home_dir(project) / "strategy"`, but its text at :2910 still prints the literal `qa-factory/strategy/`. The new test pins this
mismatch. At `test_brief_pack.py:2791`, with `RP.HOME = "elsewhere-home"`, it expects `- strategy documents: qa-factory/strategy/
elsewhere-home-profile.md`. That line names a file under one folder and tells the role it lives in another. There is no live wrong
output today, because `runtime_paths.HOME` is the constant `"qa-factory"` (`runtime_paths.py:38`). But the test now protects the
wrong text, and the right fix will turn it red. Fix: queue :2910 (and the `APPROACH_*` texts :2853-2859, :4327) with finding (1) of
§7 (the FR-37 literal class). In this round, either assert only the names part of the line, or accept that the queued fix edits this
expectation.

**F4 — info (comment accuracy).** `env_probe.py:611-612` says data_cleanup, the brief and the audit "agree on 'recorded'". Per the
spec's mapping (row "recorded, a falsy non-list"), `cleanup_owner: false` / `0` reads `recorded` in `test_data_states` and the audit
(theme 3 answered), but `unknown` in data_cleanup. Decision (1) also has the audit count `unknown` as answered by design. The
behaviour is as specified. Only the sentence overstates. Optional fix: "what `test_data_states` does not call `recorded`, and a
falsy recorded value, is `unknown` here".

**F5 — info (quality).** `execute_schedule` resolves `artifact_root` at :568-569 and then calls `_apply_budget`, which resolves it again
at :350-351. That is two config reads in one call. The spec asks for "once per function", so this is compliant. Passing `artifacts`
in would need the `_apply_budget` signature, which is outside owns. No action needed.

**F6 — info (test form).** The Popen stub (`test_config_projection.py:330`) raises `AssertionError`. A regression therefore
crashes the file, not a named red row, and the rows after it never run. My probe shows this, and so does the builder's own note.
It is still red, so it is acceptable. A recording stub plus `check_eq(launched, [])` would name the row.

## Standing answers

- **Decision (1)** (theme 3: `unknown` = answered; hole = absent / malformed / every key not_recorded or none): sound. It matches
  FR-7 and the existing expectation "GOOD A13: test data answered 'unknown' everywhere is still answered" (test_audit_rules.py,
  pre-diff). That expectation is why the first commit returned a question. AR-28 holds: the audit's "answered" closes an interview
  topic, not a delivery. data_cleanup still says `unknown` for "unknown" (row "all unknown (an answer)" -> 0 findings, cleanup
  `unknown`). `audit_factory.py:778` implements it exactly as stated. One edge flips toward "answered": a hand-written falsy
  non-list (`false`, `0`, `{}`). Before the diff, `if v` skipped these as holes. Now the reader calls them `recorded`. This follows
  decision (1) and the reader of node a. The template block (`references/templates/config.json`: blanks plus `shared_records: []`)
  still reads as a hole. Info only.
- **Decision (2)**: kept. `owner` is stripped, so `" N/A "` gives `nobody resets this data (cleanup_owner: N/A)`
  (row "recorded none word: padded N/A"). The `or 'none'` fallback was removed and is unreachable, since `owner` is non-empty on that
  branch.
- **Deviations**: (a) the local `import hooklib` in three functions is acceptable. `env_probe` already loads hooklib at the top
  (`from hooklib import ...`, :87), and the local-import pattern exists (`config_contract.stop_after_problem`). (b) In the scheduler,
  `artifact_root` is uncaught. This is fork F12 (a) as written, and the positions match the POSITIONAL invariant: `_apply_budget`
  right after `policy is None` (:350); `execute_schedule` before `state_dir.mkdir` (:568). `prepare_schedule` and
  `LeaseRegistry.__init__`, which run earlier, create nothing (read: :86-88, :259-299; `JobStore.__init__` creates nothing,
  execution_request.py:383-388). (c) `_case_needs` catches exactly the three classes and falls back to today's folder (§4 row;
  `hooklib.artifact_root` raises `AttributeError` on a list config, `ValueError` on bad JSON or a bad value, `OSError` on read).
- **Fit to item 6(b)**: every mapping row of the table is a row in `CLEANUP_ROWS`, with ids = the left column, plus the two stand
  rows. I traced each row against `config_contract.test_data_states` (config_contract.py:893-927; `values` holds only `recorded`).
  absent, malformed, not_recorded, unknown and none leave no value, so `unknown`. A falsy recorded value hits `if value` -> `unknown`.
  A CLEANUP_NONE word -> `absent`. Anything else -> `available`. No value that read `unknown` before now reads `available`. I checked
  `"?"`, `"tbd"`, `{}` and `[]` against the old precedence (NONE first, then UNKNOWN; the two lists are disjoint). `CLEANUP_UNKNOWN`
  is removed and `CLEANUP_NONE` stays. The audit row set and the brief_pack line are as specified. **6(a)**: see F1.
- **Fit to item 7 (node c)**: the three sites read `hooklib.artifact_root(root=...)`. The reader catches and the writers raise. The
  rows asked for are present: configured root case needs / job store reused; broken config case needs from today's folder; broken
  config raises with nothing created or launched (the `made == []` check excludes only `qa-factory` and `config.json`, so
  `qa-factory/state/...` would show). The gap is F2.
- **DUPLICATION AND CONSISTENCY**: none in the diff. It removes one duplicate (`CLEANUP_UNKNOWN` vs `TEST_DATA_UNKNOWN`) and reuses
  the one reader for `test_data`, `artifact_root` and `home_dir`. Grepped: `"nobody"|"no one"|"n/a", "na"` and `"tbd"` over
  `scripts/*.py` and `references/*.json`. The only other list is `audit_factory.PLACEHOLDER_CELLS` :726, which is for table cells
  and has a different purpose. The positive control hit `CLEANUP_NONE` itself. Also grepped `["']test_data["']` over
  `scripts/*.py`: the sibling found is outside the diff (Q3). The leftover `"qa-factory" / "artifacts"` literals in the package
  (32 lines) belong to axis 8, already split between OF3-1d2, F-18d and N-r5. Mapping them beyond that is a scout's job.
- **CODE QUALITY**: no new function over 60 lines and no nesting over 3. No dead branch: the `or 'none'` fallback was removed with
  its branch. Names are honest except the comment in F4. The test file has more test lines (+162) than product lines (+45), because
  the spec asks for a table row per mapping cell, so that is justified. F5 and F6 are info.
- **JUDGMENT (q11)**: none moved. The theme-3 check is a presence check over key statuses, data_cleanup is a fact line, and the
  scheduler change is a path. No census row, `blocks_override` or scan constant is touched (diff file list: 8 files, none under
  `fixtures/` or `role-load.json`). `judgment: none` is true.
- **ARCHITECTURE (q10)**: the commits name AR-13, AR-4 and AR-28. AR-13, both directions: the producer is
  `test_data_states`. Its readers are now brief_pack :2883, audit :778 and env_probe :613. One bypass remains, `app_card.py:247`
  (Q3). AR-4: the configured root is honoured at all three node c sites. A fourth job-store site in the same file is not covered
  (Q1). AR-28: reader -> today's folder, writer -> raise, unknown never -> `available`. AR-1 (`CLEANUP_NONE`, closed variety in code)
  is touched by the edit but kept by the spec and was there before the diff, so it is not a finding. Ratchets (q9): none touched.
- **ONE ROAD (q12)**: none found. The diff text has no language, runner or project name. Every site goes through the shared reader.
  Checked by reading the full diff.
- **Tests (item 5)**: the rows would catch the node's defects, with F2 as the gap. Mutation probes stayed in the report and were not
  committed, as the spec asks.

## Class-wide completeness (spec siblings block: axes 8 and 16; sweep of the same artifact)

- **Axis 8, same file (sweep-the-artifact-first): `execution_scheduler.py:154`.** In `LeaseRegistry.recover`,
  `JobStore(self.path.parents[1] / "artifacts" / task / ...)` is a third job-store site that ignores the configured root. Under
  `artifact_root: "stories"`, a live runner's job is not found. A lease whose process looks gone is then classed `blocked_orphan`,
  not `recovered_child`. The error goes the safe way (blocked), but it is wrong. The spec did not list it. The Lead noted it only in
  `docs/tasks/compact-snapshots/2026-11-12-2201-narrative.md` ("execution_scheduler.py:154 — ещё одна копия artifact_root", under
  "Очередь onboarding-forge/4"). No pile carrier holds it. There is no `batch-4-*.md` in `plans/piles/onboarding-forge/`, on `main`
  or on `pile/onboarding-forge/batch-3`. Checked with `git grep -n -i "scheduler\|OF3-1d2"` (empty). The positive control
  `git grep -c -i "OF3-1"` found 2 in batch-3. A compact snapshot is not a carrier the target reads (CLAUDE.md rule 4) -> NEEDS-WORK
  for the Lead. Line: `execution_scheduler.LeaseRegistry.recover :154 reads the default artifacts folder (axis 8, reader, catch -> today's folder) | узел: <OF3-1d2 or a batch-4 node>`.
- **Axis 8, spec queue**: OF3-1d2 (`dispatch_liveness` :800, :951) and N-r5 (B-348) are named in §7. They are not yet in a batch
  file either (same search). §7 says the coordinator places them in a new batch-4, which does not exist yet. Same owner, same move.
- **Axis 16**: node c owns no direct-read fold. `execution_scheduler._project_parallel_defaults` :230 reads config.json with
  `utf-8`, not `-sig`. A BOM config silently gets the parallel defaults, while `artifact_root`, two functions later in the same run,
  reads the same file fine. This dates from before the diff. N-r4 is "+ census rows", so whether it is counted depends on F1 -> Q4.
- **Same-artifact neighbours of the edits**: env_probe's `data_cleanup` stand lookup -> N-r1 (named in the spec). brief_pack
  `_approach_documents` :2910 text -> F3. The audit `REQUIRED_FACTS` sibling lambdas (other themes, which use `c.get` on a possibly
  non-dict config) are not applicable: different facts with no shared reader, unchanged.

## Queue (findings outside the diff)

- Q1 `execution_scheduler.py:154` (above): node line in a pile carrier. Owner: Lead.
- Q2 §7 queue entries (OF3-1d2, N-r1..N-r8, findings (1)-(4)): batch-4 not yet opened (D-0044). Owner: Lead.
- Q3 `app_card.py:247-262` reads `cfg["test_data"]` directly, bypassing `config_contract.test_data_states` (AR-13), and prints raw
  values (an `unknown` key looks like a value). It is not in the spec or the forge finding `20261102-chitateli-test-data-mimo-odnogo.md`
  (grep "app_card": no hit). It is a reader R2 may not see: `data = cfg.get("test_data")` then `data.items()` is an alias, the
  BLIND TO class. Owner: f's baseline or an N-r row, settled through the census (F1).
- Q4 `execution_scheduler.py:226-233` `_project_parallel_defaults`: a direct `utf-8` read (BOM -> defaults, list config -> uncaught
  `AttributeError` in `effective_config`?). Axis 16 / N-r4, via the census.
- Q5 brief_pack `qa-factory/strategy/` literals :2853-2859, :2910, :4327: join finding (1) (FR-37) (F3).

## Trail

- Read: the full diff; spec §4 (:298-325), §5 items 6-7 and the node rows (:388-522), §7 (:581-620); `config_contract.py:890-927`;
  `hooklib.py:636-649`; `execution_scheduler.py:84-103, 140-161, 226-233, 259-299, 343-356, 561-578`; `execution_request.py:383-395`;
  `runtime_paths.py:38-53`; `app_card.py:240-262`; `references/templates/config.json` `test_data`; critic-diff-brief.md :25-100;
  the forge finding above; both commit messages.
- Control re-runs (worktree): `python -B .../tests/test_config_projection.py` -> `=== test_config_projection: 183/183 ok ===`;
  `test_audit_rules.py` -> `=== audit rules (...): 343/343 ok ===`; `test_brief_pack.py` -> `=== test_brief_pack: 885/885 ok ===`.
  All three match the witness.
- Scheduler red probe (scratch `probe.py`: puts a copy of the scheduler first on `sys.path`, then calls
  `test_config_projection.artifact_root_rows`). With the wip copy: `=== probe-newsched: 6/6 ok ===`. With the c089e17 copy: crash at
  `test_config_projection.py:335` -> `AssertionError: launched` (the configured-root row launches the already-completed job, so the
  defect is caught). The repo was not touched.
- Negative-claim searches, each with its positive control, are given inline above (F1, Q1, Q3, duplication).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Node c's three sites (axis 8) and the test_data reader fold (AR-13) are complete per the spec. Open: execution_scheduler.py:154 LeaseRegistry.recover is a fourth job-store site in the same file that ignores artifact_root, noted only in a compact snapshot, in no pile carrier; the spec's queue (OF3-1d2, N-r1..8, findings 1-4) is not yet in a batch file (no onboarding-forge batch-4); app_card.py:247 bypasses test_data_states; execution_scheduler.py:230 direct utf-8 config read (axis 16) depends on the census. Owner: Lead.",
  "fixes": [
    "F1: attach item 6(a)'s config-read census (a named DoD deliverable, input to N-r1/N-r2/N-r4/f), or send it back as a report-only fix round of t-183",
    "F2: test_config_projection.py artifact_root_rows: add a row with er.load_run_budget stubbed and artifact_root 'stories', a completed job under stories/S-1/state/execution-jobs, and es._apply_budget returning the item in kept (execution_scheduler.py:356 is untested under a configured root)",
    "Lead: put execution_scheduler.py:154 (LeaseRegistry.recover, axis 8) and the spec's section 7 queue into a pile carrier (onboarding-forge batch-4 per D-0044)",
    "F3 (queue, optional now): brief_pack.py:2910 prints qa-factory/strategy/ while names come from RP.home_dir; join FR-37 finding (1); the test at test_brief_pack.py:2791 pins the literal"
  ],
  "trail": {
    "read": [
      "git diff c089e17..wip/of3-1c (8 files)",
      "docs/tasks/specs/t-129-of3-1-knowledge-catalog.md sections 4, 5 items 6-7, node rows, 7",
      "ai-packages/qa-factory/scripts/config_contract.py:890-927",
      "ai-packages/qa-factory/scripts/hooklib.py:636-649",
      "ai-packages/qa-factory/scripts/execution_scheduler.py:84-103,140-161,226-233,259-299,343-356,561-578",
      "ai-packages/qa-factory/scripts/execution_request.py:383-395",
      "ai-packages/qa-factory/scripts/runtime_paths.py:38-53",
      "ai-packages/qa-factory/scripts/app_card.py:240-262",
      "docs/tasks/critic-diff-brief.md:25-100",
      "plans/piles/forge/findings/20261102-chitateli-test-data-mimo-odnogo.md",
      "docs/tasks/compact-snapshots/2026-11-12-2201-narrative.md"
    ],
    "reruns": [
      {"command": "python -B .claude/worktrees/of3-1c/ai-packages/qa-factory/scripts/tests/test_config_projection.py", "result": "=== test_config_projection: 183/183 ok ==="},
      {"command": "python -B .claude/worktrees/of3-1c/ai-packages/qa-factory/scripts/tests/test_audit_rules.py", "result": "=== audit rules (A1/A9/A11/A13/A14/A17/A20/A21/A22/A27): 343/343 ok ==="},
      {"command": "python -B .claude/worktrees/of3-1c/ai-packages/qa-factory/scripts/tests/test_brief_pack.py", "result": "=== test_brief_pack: 885/885 ok ==="},
      {"command": "scratch probe.py: artifact_root_rows against wip vs c089e17 execution_scheduler", "result": "wip: 6/6 ok; c089e17: AssertionError launched at test_config_projection.py:335 (red)"}
    ]
  }
}
```
