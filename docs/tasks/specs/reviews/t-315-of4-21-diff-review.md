# t-315: diff gate for OF4-21 (wip/of4-21: e53c163 build t-307 + 1e7f6ad fix round t-313)

Reviewer: critic (Opus), the same context as t-310 (one pass per topic). The handoff gate bound this worker to the t-310 path, so the coordinator saved this file from the critic's hand-back. Condensed; the verdict, findings and key verdicts are verbatim in substance.

**Verdict: fit_with_fixes. 0 blocking, 1 fix.**

## F1 (fix before merge): K-BRIEF-CAP-9 takes its expected value from the code under test
`test_fit_targets.py:342` expects `"- and 1 more: TS-9 - " + runtime_paths.story_text(task, "work/briefs/S4-1-targets.md")`. `fit_target_lines` builds that line through `_rel(task_root, ...)`, which calls `RP.story_text`. An absolute path, a wrong folder or an empty head would all pass (P20 / FR-58 at the scale of one pin). The coordinator's t-313 brief prescribed this; it is a dispatcher defect. Fix: `f"qa-factory/artifacts/{task.name}/work/briefs/S4-1-targets.md"`, because `plan_rows` builds the story under the marked default project (:295-297).

The new source of the folder (task_root, not the fake id "T") is intended: spec row #10 includes :3081 `fit_target_lines`. In production `task == task_root.name`.

## Observations (no action in this node; O1 and O2 go on OF4-21b = OF5-13)
- O1: the 200 B approach invariant depends on the length of HOME. It is 191 B in the default world, 199 B for `elsewhere-home`, and 251 B for a 40-character home. `RP.HOME` is a code constant, so no project reaches this today.
- O2: "home as text" has three fallbacks in one file: `_home_text`, `_approach_documents` and `s4_stand_lines`.
- O3: the builder's quarantine list was slightly off (see Key 5).
- O4: cosmetic. Missing spaces after commas, `what =f` at :3364, and an import inside a loop in `case_paths`.
- O5: deviation 1 (`test_refusal_registry:145` uses an unmarked project) is accepted. Its assertion is on the `script_command` head.

## Keys
1. §4 edges E1-E17: all kept. E8 is kept by reading; E10 is kept in the default world (O1).
2. FR-59: kept. `story_text` gives the true absolute folder on any failure, and E17 only enlarges the skip set.
3. Shape changes reached every caller (`request_lines`, `command_card_lines`; the renamed `S3_ROSTER_FILE` has no remaining reader). No quarantined file calls them.
4. Deviations 1-3 accepted. Deviation 4 is inaccurate, because the spec does list :3081, but harmless.
5. Quarantine. The only reds new against baseline read-main ed0f63b are `test_brief_pack_roles` B-K1 (spec-named :110) and `test_exploration_perturbations` T2 (spec-named :88). :340 is NOT red. Acceptable for the canon. **Coordinator note:** write these two new reds into the quarantine-watch carrier or the batch remainder.
6. No unrun keep pin is expected to go red. `test_guard_write_owners` and `test_story_run_s0` are not coupled; `test_source_exclusions` and `test_vcs_evidence` have 0 brief_pack references.
7. Axis 8: `story_text` is the one survivor, with 0 literal hits in brief_pack (control hooklib.py:276); the out-of-file twins go to OF4-21b, and the axis-8 row is queued to Lead. Axis 34: covered. dup_ratchet rc=0. Judgment: none (census 22/22).

## Re-runs
test_brief_pack 936/936; test_runtime_paths 118/118; test_fit_targets 116/116; test_refusal_registry 263/263; test_flow_requests 94/94; test_walk_plan_fields 128/128; test_judgment_census 22/22.
Quarantined files, branch against baseline: roles 173/175 against 174/175; perturbations 136/137 against 137/137; manual 97/98 on both; materialize the same on both. dup_ratchet rc=0. Approach probe: 191 / 199 / 251 B.
