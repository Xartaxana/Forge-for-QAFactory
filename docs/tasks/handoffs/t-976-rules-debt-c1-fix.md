# t-976 report: C1 fix round (findings C1-1 .. C1-8)

Commit 6f21c9d4 in worktree agent-a20ee0224e84ac51c, on top of merge 68edfaf1 (ff-only was refused; per Lead's correction `git merge --no-edit origin/worktree-agent-a083d2d32ea54f961` merged clean, no conflicts).
This report is a worktree file (the tool refused the shared-checkout path); it is NOT in the fix commit.

## Per finding
- C1-1: bug_records.py `filed_bug_tiers` (new; 3 tiers: story, project home, other stories) + `filed_bug_listing` lays the tiers end to end. judge_results.py `_bug_pairs(drafts, tiers, cap)` (pure, tier by tier, draft-outer inside a tier, cuts the last tier first; returns (pairs, dropped)); `run_bugs` uses it and writes `report["pairs_dropped"]` only when dropped > 0. Zero drafts / zero bugs: no pairs, no key. Table test `bug_pairs_tier_order` in test_bug_records.py (rows: cap not reached; cut in third tier; cut in second tier with own pairs all kept; zero drafts; zero bugs).
- C1-2: `_project_bugs_dir` deleted. `_state_relative` replaced by `_project_relative` (see C1-6): project from `runtime_paths.nearest_project`, absolute posix when None. test_task_root_project_door.py: SITES row, bare-root check and the unused `judge_results` import removed.
- C1-3: filed_bug_tiers sibling filter adds `_story_exists(task.parent, p.name)`; row added to `filed_bug_listing_reads_every_home` (a non-story folder with bugs/BUG-9.md is not listed).
- C1-4: `render_bugs` adds one clause per present key (`unreadable_bug_homes`, `pairs_dropped`), unchanged when both absent (rows in `bug_pairs_tier_order`). story_step.py reporter brief names both keys.
- C1-5: test_external_writes_bug_refusals.py: one check, `resolve_bug_file(<root>/qa-factory/artifacts/T/work/proposals/bug-1.json, "bugs/BUG-1.md") == <T>/bugs/BUG-1.md` (with a state-dir BUG-1 also present).
- C1-6: duplicate entry `"file"` is project-root relative (`qa-factory/bugs/BUG-1.md`, `qa-factory/artifacts/T/bugs/BUG-1.md`); absolute posix when no project. READER LIST (case-insensitive grep over ai-packages/qa-factory for `judge-bugs|judge_bugs|duplicates|_state_relative|run_bugs|render_bugs`; positive control: it found judge_results.py's and story_step.py's own `judge-bugs.json` lines): the only writer/reader of the `file` key in code is judge_results.run_bugs; story_step.py:223/244/685 and skills/qa-story/phases/s8.md:73,367 name the file but not the `file` key; no test reads it. No reader change needed, none outside owns. common-rules.md and slices were not changed (no text states the `file` frame), so nothing regenerated.
- C1-7: only the commit's architecture line is narrowed ("the duplicate check's bug folders are read through bug_records"). Three readers named, untouched: factory_dashboard.load_bugs (own iterdir, same no-story-rule gap), exit_gate.bug_audit_errors (:1395) and audit_factory.a3_a4_artifacts (:457) (list only state_dir()/bugs; a task-root bug is never checked) -> D-2 node.
- C1-8: FR walk B corrected: "B: one notation phrase changed (test-report.md Notation line); no question text".

## FR walk (touched sections)
A - no refusal added; unreadable homes and dropped pairs are named in the report (FR-59 kept). B - see C1-8; this round adds one clause to a printed line and a brief sentence, no question text. C - producer (run_bugs) and its readers (render_bugs, brief) change in one commit; `file` has no other reader (FR-14, FR-17). D, E, F - not touched. G - English only, selftest --lang green (FR-30); one story-folder rule and one project walk reused (FR-54, axis 8).

## Witness (verbatim tails)
DoD `scenario_walk.py --witness-for ...bug_records.py judge_results.py external_writes.py` printed 27 rows. Files that are in slow_tests.json (test_bug_records, gate_brief_and_retro, gate_preflight, handoff, resolver, runtime_paths, role_commands, story_run_loop_b_*, words_doors, profile_reader, scenario_*): not run whole, "судит канон пачки"; for test_bug_records only the new/changed functions ran alone.
```
test_charters_s5_s9             60 passed in 0.36s                                   exit=0 1s
test_whole_identifier           === ... 166/166 ok ===                               exit=0 2s
test_task_root_project_door     === task_root_project_door: 10/10 ok ===             exit=0 1s
test_triage_identity            Ran 31 tests in 1.246s  OK                           exit=0 2s
test_external_writes            === test_external_writes: 52/52 ok ===               exit=0 7s
test_publication_gates          ends with NEEDS_AGENT line                           exit=0 0s
test_external_writes_bug_refusals  === external_writes_bug_refusals: 86/86 ok ===    0s
test_bug_records (filed_bug_listing_reads_every_home + bug_pairs_tier_order alone)
                                === bug_records_c1_alone: 13/13 ok ===               1s
selftest --limits --lang (subshell): PASS lang ... PASS limits ... === qa-factory selftest: 4/4 ok ===  exit=0 1s
pyflakes on the 6 touched files: exit 0, no output
```
role-load.json not touched (no K10 raise). Commit hooks: "gates: ok (7 checks)", "gates: ok (4 checks)".

## Deviations
- ff-only refused; merged instead (Lead's correction).
- `_state_relative` renamed `_project_relative` (the old name would lie after C1-6; edges line kept the old name).
- All edits made in the worktree copies of the owned paths.

## Needed beyond the manifest
cards spec E3 text; runtime_paths.nearest_project; hooklib.is_story_with_pipeline.

## Analogs noticed
factory_dashboard.load_bugs, exit_gate.bug_audit_errors, audit_factory.a3_a4_artifacts (C1-7, queued to D-2 by Lead). bug_records.owner_of / _other_stories already use `_story_exists`.
