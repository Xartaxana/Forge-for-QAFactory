# t-248 — critic diff pass, OF4-17 "one not-a-project refusal text" (wip/of4-17b: 9fccf0e + 7d472f1, base a3719cb)

Spec/DoD: finding `plans/piles/onboarding-forge/findings/20261112-odin-tekst-otkaza-not-a-project.md` (read from
`origin/wip/of-batch4`), node row OF4-17 in `batch-4-hvosty-onbordinga-i-forzha.md:44`, dispatch keys of t-248.

## Verdict

**NEEDS WORK (fit_with_fixes)**: 3 fixes before merge (F1-F3), 3 smaller ones (F4-F6) to fix in the same round, and
2 class residuals that need a node from the Lead (C1, C2). Whether to accept is the Lead's call (rule 6). The core
of the change is sound. There is one builder now, `require_project_at` and `host_probe` route through it, the
dashboard passes its door, `dashboard_refresh` reads the one marker reader, and the ratchet shrink is legitimate.
Moving the text into one shared builder, though, gave every caller the door and the advice that used to be
host_probe's alone. I proved two of those changes wrong by running them.

## Findings

**F1 (fix before merge; FR-2, AR-9). The refusal names a `--root` door that the caller does not have.**
`hooklib.py:199`: `fix = (f"Re-run with --root {above}, or run the command from inside it." if above else ...)` is
unconditional. Before the diff, `require_project_at` had no ancestor branch and said "point --root at it **where
the command has that option**". Now every ambient writer gets this text through `require_project` -> `require_project_at(..., True)`.
That is `log_append`, `stage_done`, `waiver`, `gate_brief`, `brief_pack`, `story_budget`, `window_record`,
`retro_numbers`, `tracker_write`, `test_repo_base`, `story_step`, `explore_step`, `driver_core` and `hooklib.story_root`.
`config_view` gets it too (given=False, line 292). None of these callers has a `--root` option: my grep for
`"--root"` found nothing in `log_append.py`, `config_view.py`, `stage_done.py` or `waiver.py`. The same grep found
`factory_dashboard.py:3753` and `host_probe.py:1102` (positive control).
Probe in the scratchpad: `CLAUDE_PROJECT_DIR=<proj>/sub`, cwd `<other>`, a marker at `<proj>/qa-factory/config.json`:
```
config_view: no qa-factory/config.json under ...\p248\proj\sub - refusing to create one.
The project root is ... Re-run with --root ...\p248\proj, or run the command from inside it.   (rc=3)
log_append: no qa-factory/config.json under ...\p248\proj\sub - refusing to create one.
The project root is ... Re-run with --root ...\p248\proj, or run the command from inside it.   (rc=3)
```
`config_view.py --root` would fail on argparse. The case is reachable because `project_root` falls back to the
unmarked `$CLAUDE_PROJECT_DIR` when the cwd walk finds nothing.
Expected change: `not_a_project_text` takes a flag telling whether the caller has a root option, for example
`root_option: bool`. The flag decides the ancestor branch: `Re-run with --root {above}` only when the caller has
the option; otherwise `run the command from inside {above}, or set CLAUDE_PROJECT_DIR to it`. host_probe and
factory_dashboard pass True. `require_project` and config_view pass False, and the default is False (the safe
direction: never name a door that may not exist). Add a test row: ancestor + no root option -> must not say `--root`.
The row `test_story_root_class.py:1031` ("ancestor-ambient") currently pins the defect for the generic builder.

**F2 (fix before merge; FR-10, FR-1). In host_probe's `--root` branches the refusal tells the role to give up and also names the door that works.**
`host_probe.py:1090-1094` puts "Report the host hooks as unknown, owner factory, with this fact." into `detail`,
which now appears in every branch. In base a3719cb that sentence was only in the given=False/no-ancestor branch,
where no door exists other than onboarding. Probe: `host_probe.py --root <proj>/sub` printed
"... the live guard cannot be probed here. Report the host hooks as unknown, owner factory, with this fact.\n ...
Re-run with --root ...\proj, or run the command from inside it." A role that follows the first instruction reports
"unknown" when a re-run would have probed. This is a meaning change, and it points the wrong way.
Expected change: in the branches that have a door (given=True, or an ancestor found), `detail` carries only why a
probe store there is useless. The "Report ... unknown" sentence stays for the given=False/no-ancestor branch only.
For example, host_probe passes a different `detail` depending on whether a door exists, or the builder gets a
second argument such as `dead_end_detail`.

**F3 (fix before merge; FR-41, the TP1-14336 class). config_view lost the "wrong project root" explanation and now states "not onboarded yet" as a fact.**
config_view calls with `given=False`. With nothing above, the shared text is "this project is not onboarded yet
... The next step is /qa-factory:qa-onboarding." The old config_view sentence, like the old `require_project_at`,
gave both explanations: never onboarded, OR a wrong root ("run the command from inside the project, or set
CLAUDE_PROJECT_DIR to it"). Probe with no env and a cwd outside any project:
`config_view: this project is not onboarded yet (no qa-factory/config.json in ...\p248\other or above it). Nothing
was written. The next step is /qa-factory:qa-onboarding.` An operator in the wrong folder is sent to onboard there,
which creates a stray project root. The builder took host_probe's ambient form, which was already one-sided there.
Expected change: the `not given and not above` branch of `hooklib.py:196-198` keeps the wrong-root explanation as
one clause, e.g. "... The next step is /qa-factory:qa-onboarding; if the project is elsewhere, run the command from
inside it or set CLAUDE_PROJECT_DIR to it." That restores the meaning for both config_view and host_probe.

**F4 (fix in this round; code quality, an annotation that lies). config_view's fallback can effectively never run, and its words contradict its own condition.**
`config_view.py:291-295`: `_load` raises NoConfig only when `read_config_file` finds that `config.json` does not
`exists()` (`config_contract.py:1354`). Right after that, `not_a_project_text` returns "" only if the same file
`is_file()`. So the fallback runs only if the file is deleted between the two checks. When it does run, it prints
"this project was never onboarded", while the comment above it says "the marker is there". The test at `:1128-1136`
reaches the branch only by mocking. Expected change: drop the fallback (print `shared` only), or make its sentence
true, e.g. "qa-factory/config.json under X disappeared while it was read; run the command again". The "ONE builder"
check at `:1141` then needs no config_view exemption.

**F5 (fix in this round; tests, brief item 5). Pins on script source.**
`test_story_root_class.py:1110-1111` pins the source text of `dashboard_refresh.py` (`"_carries_project(project)" in
src`, plus a check that the old literal is absent). The behaviour row at `:1108` already covers the refusal. Remove
the two source pins. The census-style "ONE builder" scan at `:1141` is a structural check and may stay.

**F6 (queue-level, Lead's carrier). Stale map row.**
`docs/SIBLING_MAP.md:216` still lists `host_probe._not_a_project` under "Outside walks" and says "cap 11". The
census in the test now has 8 entries. The doc carrier of this ratchet should drop the entry in the same move, under
rule 9 ("same commit"). The file is outside the package, so the Lead or a small-work batch makes the edit.

**Witness (rule 7, not blocking).** For t-199, 74 witness-for files are reported by return code only ("tails lost
to a shared /tmp"). The t-245 file `witness-A.txt` holds 10 tails (11 lines). My control reruns below cover the
two files the verdict depends on. The rest is for the batch canon on CI to judge.

## Answers to the dispatch keys

**(1) One builder.** Verified. `hooklib.not_a_project_text` is at :178. `require_project_at` (:219) prints it,
`host_probe._not_a_project` (:1094) returns it, `config_view.py:292` calls it, and `factory_dashboard.py:3774`
passes `extra_door`. The claim "the one builder" holds only inside the node's scope: see C1/C2.

**(2) Ratchet (AR-20, axis 18).** Legitimate. One row is removed: `OUTSIDE_WALKS` `("host_probe.py",
"_not_a_project")`, and `OUTSIDE_WALKS_MAX` goes from 9 to 8. Reason: the function no longer walks
(`resolved.parents` was removed; it calls `_nearest_project` through the builder). The census forces the
deletion, because a stale entry fails the key. Rerun: `test_runtime_paths: 83/83 ok`. This is a shrink, not a raise.
The edit is outside the dispatch's owns, and the reason holds.

**(3) Meaning change, item by item.**
- (a) Ambient bare-root text reordered (host_probe): **no meaning change.** Not onboarded, nothing written, hooks
  unknown, owner factory, next step onboarding: all kept. But see F3: the form is now shared with config_view, and
  there it is one-sided.
- (b) `require_project_at` now prints the shared two-line form, with no ancestor: **no meaning change.** The doors
  are kept (inside / `--root` where the command has it / CLAUDE_PROJECT_DIR / onboarding). It drops only the
  sentence "the factory looks in the current directory and its ancestors".
- (c) With a marker above, onboarding is no longer mentioned: **meaning change, safe in itself** (a project exists
  above). But it arrives with the unconditional `--root` door: F1, which breaks FR-2.
- (d) host_probe appends the hook and detail sentences in every branch: **meaning change, unsafe**. The hook fact is
  harmless, but "Report the host hooks as unknown" now appears next to a working door: F2 (FR-10).

**(4) Moved pins.** The rows at `:1027-1044` and the host_probe block at `:1078-1100` cover the quarantined
`hs.py:944-1012` pins named in the row ids. `test_host_probe_shapes.py` is not edited (it is not in the diff stat),
which matches finding item 4. The rows would catch the node's defect, a second builder, through the callers' real
doors. Exception: the "ancestor-ambient" row pins F1.

**(5) Class completeness (SIBLING_MAP axis 8 rows :214/:216; axis 34).** My case-insensitive grep over `scripts/*.py`
(tests excluded) used
`no qa-factory/config\.json (under|in)|not onboarded yet|never onboarded|not a (factory )?project|refusing to create`.
Positive control: `refusing to create one` in hooklib.py, count 1. Refusal texts a person sees:
- `hooklib.py:203/197`: the builder.
- `config_view.py:293`: the fallback (F4).
- **C1, missed and not queued: `check_coverage.py:63-68` `marked_root`** builds its own not-a-project refusal with
  its own ancestor hint ("is not a factory project: it has no qa-factory/config.json ... The project above it is
  {found}: pass --root {found}"). It is the same class (axis 8 row :214 names `check_coverage --root`). The diff
  did not fold it and the builder's report did not name it. Proposed: a node in an untaken onboarding-forge batch
  that routes it through `not_a_project_text(root_option=True, detail=<the coverage-map sentence>)`, exit 2 kept.
  Owner: the Lead of the pile.
- **C2, missed and not queued: `hooklib.py:366-368` `story_root`** ("which is not an onboarded project (no
  qa-factory/config.json under it ...)") is a second wording of the same refusal in the same artifact (sweep rule)
  for an explicit `project=`. Proposed: the same node (it raises StoryRootError, so it uses the builder's text plus
  its tail).
- The rest of the grep hits are comments and docstrings (check_coverage:16, contract:3215, cost_capture, guard_*,
  readiness, runtime_paths, story_step, run_suite, turn/window_budget case names), or a different class
  (`project_knowledge` "not a project-knowledge key").
- `require_project` (ambient) is named by the builder as left as-is. In fact it is NOT untouched: it now prints the
  shared text and carries F1. `recover_codex_usage`: a separate class, as stated (finding "Рядом").

**Merge-tree.** Clean against `refs/remotes/origin/main`, `origin/conv/wave-2` and `origin/conv/wave-3`. No
semantic overlap: wave-3 touches `hooklib.artifacts_dir` only; wave-2 touches `check_coverage.main` (`--ignore-receipt`),
not `marked_root`, which bears on C1 later. `OUTSIDE_WALKS_MAX = 9` on all three, so the 9 -> 8 change merges cleanly.

## Standing questions
- 1 Fit to the spec: items 1-3 and 5 of the finding are implemented. Item 3 ("ONE refusal" made true) holds only
  within the scope: C1/C2.
- 2 Builder decisions: two point the unsafe way (F1 `--root` door by default, F3 one explanation by default).
- 3 Seams: `require_project_at` gained an optional keyword (additive). `dashboard_refresh` imports a private
  `_carries_project`: tolerable, it is the named marker reader.
- 6 DUPLICATION AND CONSISTENCY: reused `_carries_project` (hooklib:35) and `_nearest_project` (hooklib:44 ->
  runtime_paths.nearest_project), with no new walk. Remaining duplicates of the refusal text: C1 check_coverage:65,
  C2 hooklib:367, and F4 config_view:293. Grepped as in (5).
- 7 CODE QUALITY: the new function `not_a_project_text` (hooklib:178-206) has 29 lines and nesting 1. One dead or
  misleading branch: F4. No copy-paste inside the diff.
- 8 Hygiene: the changelog fragment is English. selftest `--lang` is reported 4/4 by the builder (not rerun).
- 9 Ratchets: (2) above. The only row is a removal; no raise.
- 10 ARCHITECTURE: AR-9, AR-15 and AR-16 are named in both commit messages. AR-9 is broken by F1. AR-15/16 are
  incomplete for C1/C2.
- 11 JUDGMENT: none moved. The change is text routing only; no census row or scan constant is touched, so
  `judgment: none` holds.
- 12 ONE ROAD: none found. No language, project or case branch in the diff (grepped the diff for
  language/runner names: none).

## Trail
- Read: critic-diff-brief.md; the full product and test diff `a3719cb..origin/wip/of4-17b`; hooklib.py :35-51,
  :54-70, :175-232, :350-375; config_view.py :183-187, :270-300; config_contract.py :1349-1374;
  check_coverage.py :55-68; the finding file and the batch-4 row :44 (origin/wip/of-batch4); journal dev1.jsonl
  t-199/t-245/t-248 lines; SIBLING_MAP.md :208-219; tools/critic_verdict.schema.json; witness-A.txt.
- Reruns (worktree, via `( cd <worktree scripts> && ... )`):
  `python -B tests/test_story_root_class.py` -> `=== test_story_root_class: 636/636 ok ===` rc=0;
  `python -B tests/test_runtime_paths.py` -> `=== test_runtime_paths: 83/83 ok ===` (the K3 census rows PASS).
- Probes (scratchpad `p248`, nothing in the repo): the config_view and log_append ancestor case (F1), config_view
  with nothing above (F3), host_probe `--root` below a marker (F2); outputs are quoted above. `ls` afterwards: no
  `qa-factory/` created under `sub` or `other`.
- merge-tree `--write-tree` against main/wave-2/wave-3: exit 0 (clean) for all three.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Inside the node: one builder, used by require_project_at, host_probe, config_view and factory_dashboard; ratchet shrink 9 to 8 legitimate. Missed and not queued (axis 8 row 214, sweep of hooklib): check_coverage.py:63-68 marked_root builds its own not-a-project refusal with an ancestor hint (C1); hooklib.py:366-368 story_root has a second wording (C2). Proposed: one node in an untaken onboarding-forge batch, owner the pile Lead. SIBLING_MAP.md:216 still lists host_probe._not_a_project (F6).",
  "fixes": [
    "F1 hooklib.py:199 - the ancestor door 'Re-run with --root {above}' is unconditional; add a root_option flag (default False): without it say run from inside {above} or set CLAUDE_PROJECT_DIR; host_probe and factory_dashboard pass True; add a test row ancestor without root option must not say --root (test_story_root_class.py:1031 pins the defect). Proven: config_view and log_append print --root, which they lack.",
    "F2 host_probe.py:1090-1094 - 'Report the host hooks as unknown' now appears in the --root branches next to the working re-run door; keep it only in the given=False and no-ancestor branch.",
    "F3 hooklib.py:196-198 - the ambient no-ancestor branch states 'not onboarded yet' as the only explanation; restore the wrong-root clause (run from inside the project or set CLAUDE_PROJECT_DIR), which config_view and require_project_at had before.",
    "F4 config_view.py:291-295 - the fallback is reachable only by a delete race and says 'never onboarded' while its condition is marker present; drop it or make the sentence true.",
    "F5 test_story_root_class.py:1110-1111 - remove the two source-text pins on dashboard_refresh.py; the behaviour row at :1108 covers it.",
    "F6 docs/SIBLING_MAP.md:216 - drop host_probe._not_a_project from Outside walks and correct the cap (Lead carrier, outside the package)."
  ],
  "trail": {
    "read": [
      "docs/tasks/critic-diff-brief.md",
      "git diff a3719cb..origin/wip/of4-17b (all 8 files)",
      "ai-packages/qa-factory/scripts/hooklib.py:35-70,175-232,350-375",
      "ai-packages/qa-factory/scripts/config_view.py:183-187,270-300",
      "ai-packages/qa-factory/scripts/config_contract.py:1349-1374",
      "ai-packages/qa-factory/scripts/check_coverage.py:55-68",
      "plans/piles/onboarding-forge/findings/20261112-odin-tekst-otkaza-not-a-project.md",
      "origin/wip/of-batch4 batch-4-hvosty-onbordinga-i-forzha.md:44",
      "logs/journal/dev1.jsonl t-199/t-245/t-248",
      "docs/SIBLING_MAP.md:208-219",
      "scratchpad witness-A.txt"
    ],
    "reruns": [
      {"command": "python -B tests/test_story_root_class.py (worktree)", "result": "636/636 ok, rc 0"},
      {"command": "python -B tests/test_runtime_paths.py (worktree)", "result": "83/83 ok"},
      {"command": "config_view.py --keys and require_project('log_append') with CLAUDE_PROJECT_DIR=proj/sub, cwd outside", "result": "both print 'Re-run with --root <proj>'; neither has --root (F1)"},
      {"command": "host_probe.py --root proj/sub", "result": "prints 'Report the host hooks as unknown' before the re-run door (F2)"},
      {"command": "config_view.py --keys, no env, cwd with no project", "result": "'this project is not onboarded yet ... next step onboarding', no wrong-root door (F3)"},
      {"command": "git merge-tree --write-tree vs origin/main, conv/wave-2, conv/wave-3", "result": "clean x3"}
    ]
  }
}
```
