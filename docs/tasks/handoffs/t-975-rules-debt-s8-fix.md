# t-975 report: S8 fix round (S8-1..S8-5), builder

## Per finding
- S8-1: `project_decisions.py` `_ScopeTable._load`: `raw = hooklib.read_json(path, None)`; `None` raises the same refusal, worded "(missing or not JSON)". The empty/malformed-rows refusal is unchanged.
- S8-2: `factory_dashboard.py` `tab_factory` (before `scope_span`): the reads of `FINDING_SCOPES` (words, `.urgent`) are in `try/except ValueError`; on failure `scope_words=()`, `urgent_words=()`, and `w1` is drawn `Unavailable: <esc(str(exc))>`; `scope_span` falls back to `esc(scope)` (the word is no word of the empty table). Every other use of `FINDING_SCOPES` in the function now reads `scope_words`/`urgent_words`. The CLI refusal (E1) is untouched. Test: one `check_eq` in `test_project_decisions_refs.py::test_the_dashboard_reads_the_writers_words` (already drove the dashboard constant): resets `_rows`, points `SCOPES_FILE` at a missing name, calls `FD.tab_factory`, expects (`"missing or not JSON"` in refusal, `<p class='nd'>Unavailable: <esc refusal></p>` in html, findings section present) == (True, True, True); state restored in `finally`.
- S8-3: `tab_factory`: `grey_slice = urgent_word is None and bool(render_findings)` gates both the grey donut slice and the legend item `unclassified (this render)` (colour `SCOPE_COLOR_OTHER`). Not covered by a test (branch unreachable in the package; the review calls it presentation only).
- S8-4: deleted the template-words loop in refs (`test_the_scope_words_are_listed_and_each_writes_a_row`) and the order pin `S8: the template's meaning lines name the data file's words, in order` in `test_conductor_doors.py`; kept the junction `dict(PD.FINDING_SCOPES) == data` and the whole-meaning check, which now looks the template line up by word (`by_word.get(word, "")`) so a missing line fails instead of being dropped by `zip`. Kept the refs:121 tuple pin.
- S8-5: corrected FR-walk line B: "B: one template line reworded with the same meaning (`factory-backlog.md:15`); no question text."

## FR walk over touched sections
A: FR-1 holds (a missing file is reported with path, shape and door; FR-4 n/a). B: see S8-5. C: n/a. D: n/a. E: n/a. F: n/a. G: FR-30 (--lang passes), FR-54 (axis 16 applied: read via hooklib.read_json).

## Witness (all inside the worktree)
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/project_decisions.py ai-packages/qa-factory/scripts/factory_dashboard.py` printed 29 test files (25 s), run each separately:
```
test_case_key_identity_join.py (2s) === 154/154 ok ===
test_cost_capture_settled.py (10s) 159/159 ok
test_dashboard_cost_gap_rows.py (1s) 9/9 ok
test_field_producers.py (17s) 885/885 ok
test_http_client.py (24s) 277/277 ok
test_ledger.py (10s) 452/452 ok
test_manifest_projection.py (8s) 182/182 ok
test_onboarding_markers.py (1s) 8/8 ok
test_pinned_lifecycle.py (7s) 51/51 ok
test_project_decisions_change_request.py (6s) 142/142 ok
test_project_decisions_doc_ref_form.py (8s) 111/111 ok
test_project_decisions_refs.py (16s) 122/122 ok   (carries the new S8-2 check)
test_project_knowledge.py (11s) 157 passed in 10.08s
test_retro_numbers.py (9s) 316/316 ok
test_sides_ledger.py (1s) 120/120 ok
test_triage_identity.py (3s) OK
```
Slow (in slow_tests.json), not run: судит канон пачки: test_bug_records, test_conductor_doors (my S8-4 edit there is therefore checked by pyflakes only), test_gate_preflight, test_guard_write_owners, test_install_retire, test_onboarding_first_reader, test_reinstall_equals_fresh, test_scenario_cart_1, test_scenario_local_1_0108, test_scenario_local_1_arm_b, test_silent_passes, test_story_run_refusals, test_test_locations, test_third_verdict.
`( cd ai-packages/qa-factory && python -B scripts/selftest.py --limits --lang )`: `PASS limits ... PASS limits ... === qa-factory selftest: 4/4 ok ===` (3.7 s).
pyflakes on the four touched .py files: only three pre-existing warnings at factory_dashboard.py:2148 (unused driver_journal imports), none from this diff.

## Needed beyond the manifest
`scripts/tests/scenario_walk.py` (the DoD path in the dispatch said `scripts/scenario_walk.py`, which does not exist: spec divergence, the real one is under tests/), `slow_tests.json`, `hooklib.py` (read_json, ref).

## Analogs noticed
- `factory_dashboard.py:2148` unused imports (pre-existing, not touched).
- `load_bugs` is C1-7, not this round.
- The grey-slice legend branch has no test row (unreachable with the shipped data file).
