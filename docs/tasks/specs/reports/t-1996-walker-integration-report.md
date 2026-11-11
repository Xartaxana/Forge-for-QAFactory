# t-1996 walker slice 1 integration report

Branch fb-fix (worktree D:/ws1/wt-fbfix), not pushed. Commits: 231b66a30 (merge wn1a), 4367c8d42 (merge wn4), df162a3e3 (merge wn3a), 46b304714 (integration).

## Conflicts and resolutions
- merge wn1a: census fixture auto-merged, no conflict. The pre-merge-commit hook stopped the merge ("Not committing merge"): forge_metrics (b) named walk_session.py, test_walk_session.py, test_walk_batch.py as matching no feature. I added globs to feature F10 "manual evidence" in `plans/features.json` and committed the merge with that file included (so the features.json change sits inside merge 231b66a30, not in the integration commit). F10 got: scripts/walk_session.py, scripts/tests/test_walk_*.py, scripts/app_card.py, scripts/tests/test_app_card.py, references/walk-charter.md. No hook refused features.json.
- merge wn4: conflict only in `references/role-load.json` (two blocks: ratchet_tokens and process_ratchet_tokens). Resolution: qa-code-critic = HEAD side (18669 / 17199), qa-runner = wn4 side (15566 / 14407). Verified against `role_load.py --all`: actual qa-code-critic 18,669 tokens, process 17,199 (equal to ratchet); actual qa-runner 15,566 / 14,407 (equal). Both lowerings kept, no ratchet raised. (Other roles, e.g. qa-case-critic 18,271 vs 18,230, were already slack before this work.)
- merge wn3a: clean.
- Census fixture: no number changed by me; test_judgment_census 21/21 green.

## Step results
2. Pin `test_charter_words_exist_in_data` GREEN (test_walk_charter.py in the 95-passed run). 
3. `app_card` added to CLI_SCRIPTS; test_audit_rules 328/328.
4. Explore charter sentence (line 68) rewritten: "error guessing from the code facts of the brief" -> "the guess of a breakage before the route (its "Hypothesis before the route")". Reason: grep of agents/ and references/ shows no "error guessing" in qa-runner.md or walk-charter.md; the nearest live text is runner Techniques "Hypothesis before the route". Error guessing by name now lives only in qa-case-designer.md and qa-scout.md. Limits test (`--limits`) green.
5. features.json: see above.
7. Fragment `changelog.d/t-1957-slice1-integration.md`, two lines.

## Step 6 investigation
(a) `git log -S'"surprise": "<id>"' -- agents/qa-runner.md`: d7aaa2783 (X8-4, added) and 95be4810b ("fix batch t-1936 round 2: B1 cuts (code-critic, runner)", removed: its diff shows `-2. **Every doubt is an observation.** ... a recorder surprise: line by "surprise": "<id>"`). The string is absent from qa-runner.md at 9c5283d56 and after the merges. wn4 did not remove it. The test KEYS (test_charters_s5_s9.py line 57) still expects it: a stale pin versus the B1 cut. Not fixed (not a consequence of the accepted nodes; needs the Lead's choice: restore the phrase in the runner, or change the pin).
Current run after merges: `python -m pytest .../test_charters_s5_s9.py -q` -> `1 failed, 58 passed` (same test, same key).
(b) The package selftest runs each `tests/test_*.py` as its own process (`selftest.py` `_test_outcome`: `run_subprocess([path])`, pass = exit code 0). A pytest-style file has no `__main__`, so run as a script it executes nothing. Shown: `python -B .../test_charters_s5_s9.py` -> no output, `exit 0`. So the package selftest cannot see this failure. Whether CI also runs pytest on the package: `.gitlab-ci.yml` has `pytest` lines (110: `python -m pytest tools/ -q`, others pip install pytest); `docs/migration/forge-repo/.github/workflows/canon.yml` has no pytest match for this file. I did not establish that any CI job runs pytest over the package tests; the "CI green" of the branch is therefore consistent with the red file being invisible.
(c) `grep -L "__main__" scripts/tests/test_*.py | xargs grep -l "def test_"` -> 26 files: test_actor_control_rule, test_arch_check, test_audit_rules, test_blast_radius, test_brief_pack_sd_head, test_charter_form, test_charters_s5_s9, test_contract_slices, test_diff_scope, test_exit_gate_advice, test_exit_limit_halt_answered, test_fit_targets, test_handoff_init_author, test_handoff_inline_values, test_onboarding_markers, test_open_list_fields, test_open_vocabularies, test_probe_gap_door, test_probe_target_fact, test_rework_dispatch_files, test_role_load, test_rows_owed, test_stage_review_person_pass, test_test_novelty, test_tried_table, test_walk_charter. Positive control: `grep -l "__main__"` finds 581 files, including test_role_load.py. CAVEAT: this grep is imprecise. test_audit_rules.py and test_role_load.py are in the list yet run as scripts and print "N/N ok" (they have another entry form), and tests using pytest markers (import pytest / tmp_path / monkeypatch / parametrize) number only about 15 of the 26: test_brief_pack_sd_head, test_charter_form, test_charters_s5_s9, test_diff_scope, test_exit_gate_advice, test_handoff_init_author, test_open_list_fields, test_open_vocabularies, test_probe_gap_door, test_probe_target_fact, test_rework_dispatch_files, test_stage_review_person_pass, test_test_novelty, test_walk_charter (2 markers) — those are the certainly silent ones under script runs. The rest need a per-file look (not done).

## Witness
pytest (5 files): `95 passed in 32.46s`.
Scripts (each exit 0): test_audit_rules `=== audit rules (A1/A9/A11/A13/A14/A17/A20/A21/A22/A27): 328/328 ok ===`; test_judgment_census `21/21 ok`; test_role_load `165/165 ok`; test_artifact_writers `18/18 ok`; test_gate_registry `439/439 ok`; `selftest.py --lang` `2/2 ok`; `selftest.py --limits` `1/1 ok` (exit 0).

## Deviations
- features.json edit is inside merge commit 231b66a30 (the hook forced it before the merge could complete), not the integration commit.
- I used `cd` in three Bash calls inside one command line (no persistent effect intended); all later commands used absolute paths. Heredoc python script used once to resolve the role-load conflict markers (should have been Edit).
- Explore-charter rewrite chose "Hypothesis before the route" as the pointer: a wording choice of mine, small.

## Class / analogs for the Lead
- The 26-file list above: pytest-style tests invisible to the package selftest (the class behind the red craft-key pin).
- The stale pin `KEYS["qa-runner"]` `"surprise": "<id>"` versus the B1 cut; also check the other KEYS entries cannot drift the same way (they are only run under pytest).

Needed beyond the manifest: selftest.py (_test_outcome), role_load.py, qa-runner.md, test_charters_s5_s9.py, the CI files.
