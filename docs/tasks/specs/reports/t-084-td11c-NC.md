# t-084 — TD-11 spec C, node NC: wave-1 cuts regenerated on fresh main + the closing registry/carrier edits

Worktree: C:\QAFactory\forge-repo\.claude\worktrees\agent-a96c92208c5880c76 (base 5eeab44). No commit, no push.

## Status per step

| Step | State |
|---|---|
| 1 map edits | DONE: N3 map `k4b_...` home -> `test_story_run_freshness_k1_k5`; N1 map `taken` home -> `test_infra_failure_retries`. Both accepted by the tool (PROOF ok), no revert needed |
| 2 six cuts | DONE: dry-run then --apply for N1, N4, N6, N2, N3, N5, each `PROOF: ok` (below) |
| 3 registry rows | DONE: six split-keep runs (lines below); covers inherited (wider = safe side), each part additionally holds its `<stem>_common.py`; B2 import check (own script + test_selftest_slow_tests.py) finds 0 missing |
| 4 carriers | DONE with 3 open questions (below) |
| 5 changelog.d | NOT DONE, question: builder-rules item 11 asks for a fragment, but `changelog.d/` is not in my owns. Tests-only change; Lead decides |

## PROOF outputs (--apply, verbatim lines (a)(b)(c) + verdict; full outputs: the tool prints them, saved in the scratchpad)

```
N1: (a) source 244, parts 243 + common 1 + shim 0 = 244 -> ok | (b) names 52, each exactly once -> ok | (c) 29 entries, 29 across parts -> ok | PROOF: ok
N4: (a) 422 = 422 + 0 + 0 -> ok | (b) 41 -> ok | (c) 24 = 24 -> ok | PROOF: ok
N6: (a) 364 = 364 + 0 + 0 -> ok | (b) 72 -> ok; shim re-exports 10 names, all resolvable, no test_* -> ok | (c) 45 = 45 -> ok | PROOF: ok
N2: (a) 378 = 378 + 0 + 0 -> ok | (b) 104 -> ok; shim re-exports 3 names -> ok | (c) 65 = 65 -> ok | PROOF: ok
N3: (a) 203 = 201 + 2 + 0 -> ok | (b) 64 -> ok | (c) 30 = 30 -> ok | PROOF: ok
N5: (a) 286 = 286 + 0 + 0 -> ok | (b) 91 -> ok | (c) 53 = 53 -> ok | PROOF: ok
```
(the tool also printed (d) byte identity, (f) closing, (g) isolated import lines, all ok; dry-run of each map printed PROOF: ok first.)

## The six `keep-split:` lines

```
keep-split: test_infra_failure.py -> test_infra_failure_classify.py, test_infra_failure_stops.py, test_infra_failure_retries.py, test_infra_failure_conductor_tracker.py, test_infra_failure_texts.py -- TD-11c wave 1
keep-split: test_story_run_loop_b.py -> test_story_run_loop_b_loop.py, test_story_run_loop_b_threshold.py, test_story_run_loop_b_answers.py -- TD-11c wave 1
keep-split: test_controller_rework.py -> test_controller_rework_jobs_guard.py, test_controller_rework_repair_binding.py, test_controller_rework_window_words.py -- TD-11c wave 1
keep-split: test_no_move_seam.py -> test_no_move_seam_n1_n9.py, test_no_move_seam_n2b_n15.py, test_no_move_seam_sites.py, test_no_move_seam_k4s.py, test_no_move_seam_c26_g27_f2.py -- TD-11c wave 1
keep-split: test_story_run_freshness.py -> test_story_run_freshness_k1_k5.py, test_story_run_freshness_k6_k7.py, test_story_run_freshness_k8_k14.py, test_story_run_freshness_k15_k26.py -- TD-11c wave 1
keep-split: test_handoff_values.py -> test_handoff_values_keys.py, test_handoff_values_refusal.py, test_handoff_values_main_block.py -- TD-11c wave 1
```
The commit message needs all six lines (the tool's ci-out/keep-split-msg.txt held only the last run; the six lines above are the verbatim `keep-split:` lines of the six runs). N6 and N2 used `--shim`.

## Each part alone (tally; a run over 120 s locally is "judged by CI", seconds are not judged, E10)

```
=== test_infra_failure_classify: 72/72 ok ===   === test_infra_failure_stops: 52/52 ok ===   === test_infra_failure_retries: 55/55 ok ===
=== test_infra_failure_conductor_tracker: 40/40 ok ===   === test_infra_failure_texts: 87/87 ok ===      N1 sum 306 = reference 306
=== test_story_run_loop_b_loop: 264/264 ok ===   _threshold: 107/107 ok   _answers: 106/106 ok                     N4 sum 477 = reference 477
=== test_controller_rework_jobs_guard: 53/53 ok ===   _repair_binding: 235/235 ok   _window_words: 247/247 ok    N6 sum 535 = reference 535
=== test_no_move_seam_n1_n9: 119/119   n2b_n15: 109/109   sites: 506/506   k4s: 73/73   c26_g27_f2: 87/87           N2 sum 894 = reference 894
=== test_story_run_freshness_k1_k5: 61/61   k6_k7: 67/67   k8_k14: 114/114   k15_k26: 51/51                          N3 sum 293 = reference 293
=== test_handoff_values_keys: 103/103   refusal: 6401/6401   main_block: 34/34                                         N5 sum 6538 = reference 6538
```
All exit 0. window_words timed out at 120 s in the first batch run (six processes at once); rerun alone with a 400 s cap: `=== test_controller_rework_window_words: 247/247 ok ===` exit 0. Reference sums all equal: no finding.
Local seconds in the six-parallel batch (reported only): infra classify 95, stops 82, retries 97, tracker 24, texts 45; loop 108, threshold 33, answers 35; no_move sites 103, n2b_n15 89, c26 64, k4s 32, n1_n9 30; freshness 43/69/65/70; handoff 58/45/33.

Shims run directly (exit 0):
```
test_controller_rework.py: no checks of its own; they are in test_controller_rework_jobs_guard.py, test_controller_rework_repair_binding.py, test_controller_rework_window_words.py
test_no_move_seam.py: no checks of its own; they are in test_no_move_seam_n1_n9.py, test_no_move_seam_n2b_n15.py, test_no_move_seam_sites.py, test_no_move_seam_k4s.py, test_no_move_seam_c26_g27_f2.py
```

## Carrier tests and gates (python -B <path>)

```
=== test_driver_layers: 283/283 ok ===                 exit 0 (29 s)
=== test_selftest_slow_tests: 124/124 ok ===
=== test_silent_passes: 326/326 ok ===                  exit 0 (112 s, 7 files running at once)
=== window record (test_window_record): 462/462 ok ===  exit 0 (143 s under load: "judged by CI" by the 120 s rule, but it completed green)
=== test_gate_registry: 438/438 ok ===
=== audit rules (test_audit_rules): 332/332 ok ===
extra: test_conductor_doors 218/218 ok (imports the N2 shim), test_words_doors 537/537 ok (imports the N6 shim, prose edited), test_driver_golden 225/225 ok, test_selftest_shard 95/95 ok, test_selftest_ran_nothing 23/23 ok
python tools/test_quarantine.py check            -> quarantine check: 0 violation(s)   (run again at the end, after all edits)
python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang  -> PASS limits ... PASS limits ... === qa-factory selftest: 4/4 ok ===
python tools/lint_ratchet.py --check             -> lint ratchet: 36 findings, 36 in the baseline, 0 new, 0 stale (pyflakes 3.2.0)
python tools/dup_ratchet.py --check              -> scripts: 9 groups, 9 known, 0 new, 0 grown ...; tools: 16 groups, 16 known, 0 new ...
python -m pyflakes <all parts, commons, both shims>  -> exit 0, no output
```
Witness line: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <test_infra_failure_classify.py, test_no_move_seam.py, test-layers.json, slow_tests.json, selftest.py>` printed: for the parts "no scenario or keep row covers ...: run the whole scenario layer" + the five scenario files (safe side); `test_no_move_seam.py: keep test_conductor_doors.py (layer register, covers it)`; test-layers.json/slow_tests.json: `test_selftest_shard.py`, `test_selftest_slow_tests.py`; selftest.py: `test_console_encoding.py`, `test_selftest_ran_nothing.py`, `test_selftest_shard.py`, `test_selftest_slow_tests.py`. All of those ran green above (the scenario_* files were not run: they are replay worlds, full tier).

## Carrier positive control

`Grep test_controller_state([^_a-z0-9]|$)` over ai-packages/tools/.github/SIBLING_MAP, -i: 114 occurrences in 64 files (same shape as the six stem searches). Used the Grep tool (not `git grep`: the worktree guard refuses compound git commands); it reads the working tree, so it also sees the new files, which I filtered by hand.

## Carrier lines changed (file:line old -> new; lines are of the fresh tree, several moved from the verdict's numbers)

- `scripts/selftest.py` TEST_TIMEOUTS: removed `"test_infra_failure.py": 600` (:111); `"test_story_run_freshness.py": 600` (:129) with its 2-line comment; `"test_no_move_seam.py": 600` (:145) with its 2-line comment. The refusals row and its comment stay.
- `scripts/slow_tests.json`: out `test_controller_rework.py` 131.5 (:26), `test_handoff_values.py` 133.5 (:48), `test_infra_failure.py` 314.4 (:51), `test_no_move_seam.py` 180.2 (:59), `test_story_run_freshness.py` 144.1 (:119), `test_story_run_loop_b.py` 111.0 (:120). In (provisional = round(old x part check sites / total check sites, 1), check sites from the tool's row block): controller_rework jobs_guard 17.7, repair_binding 40.8, window_words 73.0 (49/113/202 of 364); handoff keys 44.8, main_block 10.3, refusal 78.4 (96/22/168 of 286); infra classify 85.4, conductor_tracker 40.1, retries 66.0, stops 62.1, texts 60.8 (66/31/51/48/47 of 243); no_move c26_g27_f2 28.3, k4s 32.6, n1_n9 27.8, n2b_n15 41.2, sites 50.3 (59/68/58/86/105 of 376); freshness k15_k26 28.0, k1_k5 28.7, k6_k7 39.4, k8_k14 48.0 (39/40/55/67 of 201); loop_b answers 27.6, loop 58.4, threshold 25.0 (105/222/95 of 422). Shims not listed. Keys sorted as the file's order. The shim rows were checked: `test_selftest_slow_tests.py` ok.
- `scripts/tests/test-layers.json`: via split-keep: 4 old rows out, 2 old rows (controller_rework, no_move_seam) re-rowed as shims (layer data_join, covers `tests/<common>.py`), 23 part rows in (inherited covers + `tests/<stem>_common.py`). Hand edit: :6081 prose `why` of `test_story_step_manual_block.py` "test_controller_rework.py, test_s6_lane_admission.py import it" -> "the test_controller_rework parts, test_s6_lane_admission.py import it" (carrier beyond the list).
- `fixtures/driver-layers.json`: :1281 file `test_infra_failure.py` -> `test_infra_failure_texts.py` (command_and_flags); :1282 `test_infra_failure.py` -> `test_infra_failure_stops.py` (k2_auth_stops_the_driver); :31 note `test_story_run_freshness.py holds the two equal` -> `test_story_run_freshness_k15_k26.py ...` (K21 holds TICKET_CHANGED_OPTIONS).
- `scripts/tests/test_window_record.py:1589-1590` `test_story_run_loop_b.py` -> `test_story_run_loop_b_loop.py` (read_text path and the check label).
- `scripts/tests/test_silent_passes.py:1344` STUB_FILES key `test_no_move_seam.py` -> `test_no_move_seam_n2b_n15.py` (the only part with a `def py(..., check=..., expect=...)` stub, line 292 there; the other `driver.py = lambda ...**k` stubs carry no `check`, K24 does not count them).
- `fixtures/driver-golden-rules.json`: `files.outside` :8 `test_infra_failure.py` -> the five parts (classify, conductor_tracker, retries, stops, texts); `ceiling_seconds` :16 `"test_infra_failure.py": 2400` -> the same 2400 on each of the five parts (the old ceiling, unchanged per file; a smaller ceiling would be my invention); blind-spot `where` :20 `test_infra_failure.py k1_data_file_is_data, the_data_file_absent_is_one_note` -> `test_infra_failure_classify.py k1_classify, test_infra_failure_texts.py the_data_file_absent_is_one_note` (`k1_data_file_is_data` no longer exists; the `load_ref_json` lambda patches are in `k1_classify` lines 55-75 and `the_data_file_absent_is_one_note`).
- `design/state-exits.md`: :32 `test_controller_rework.py` -> `test_controller_rework_repair_binding.py`, `test_controller_rework_jobs_guard.py`; :41 -> `test_controller_rework_window_words.py` (per the N6 report); :57 `test_story_run_loop_b.py` -> `test_story_run_loop_b_loop.py`; :186 same; :120 `test_handoff_values.py` -> `test_handoff_values_keys.py`, `test_handoff_values_main_block.py` (N5 report); :139 `test_infra_failure.py` -> `test_infra_failure_stops.py`, `test_infra_failure_retries.py` (N1 report); :187 `test_story_run_freshness.py (K5-K9, K21-K26)` -> four parts, each with its K range (K5 k1_k5, K6-K7 k6_k7, K8-K9 k8_k14, K21-K26 k15_k26); :189 `(K6-K7)` -> `test_story_run_freshness_k6_k7.py`.
- `design/architecture.md:192` `test_no_move_seam.py` -> the five part names. `docs/SIBLING_MAP.md:123` `test_no_move_seam n24` -> `test_no_move_seam_c26_g27_f2 n24` (n24 is there).
- Prose: `story_run_common.py:4` `test_infra_failure.py` -> "the `test_infra_failure_*.py` parts and `infra_failure_common.py`"; `ticket_adapter.py:218` -> `test_infra_failure_conductor_tracker.py K10`; `controller.py:260` -> `test_story_run_freshness_k15_k26.py K26`; `driver_s0.py:20` (old story_run.py:126) -> `test_story_run_freshness_k15_k26.py`; `driver_runner.py:1229` (old story_run.py:5986) `test_no_move_seam pins` -> `test_no_move_seam_n2b_n15 pins` (N12b is there); `audit_factory.py:1618` -> `test_no_move_seam_c26_g27_f2.py n24`; `.github/workflows/scenario-clock.yml:4` example -> "test_story_run_loop_b_loop.py test_no_move_seam_sites.py"; `test_conductor_doors.py:641` PINNED_ELSEWHERE value -> `test_story_run_loop_b_answers.py (HF2-7 ...)`; `test_words_doors.py:1329` docstring "not in test_controller_rework.py" -> "not in the test_controller_rework parts"; `test_controller_task_flag.py:310` -> `test_controller_rework_repair_binding` (the `teleport` operation scenario at :545 of that part); `test_runtime_paths.py:125` -> `test_controller_rework_jobs_guard` (`a_story_under_no_project_closes_nothing`).
- Left untouched as ordered: CHANGELOG, `changelog.d/ci-ceilings-slow-files.md`, `test_selftest_slow_tests.py` samples, `test_story_run_loop.py:2` (quarantined), `test_current_audit_contract.py` (quarantined; will go red in quarantine-watch on the 3 TEST_TIMEOUTS rows: the Lead marks it), cohort `keep_fail_at_entry` (`test-layers.json` freshness name in the cohort list, history), `tools/` (see analogs).

## FR pass (PROJECT.md "package change" item 1)

- A refusals: not touched (no refusal text changed).
- B text to a person: not touched (comments and docstrings only).
- C contracts: FR-37 applies: every path named in a carrier now names a file that exists (the carrier grep re-run, remaining hits are history/cohort/samples/quarantined listed above); FR-13: the closed variety stays in data files (`driver-golden-rules.json`, `driver-layers.json`, `slow_tests.json`).
- D identity and evidence: FR-18 n/a (no coverage claim changed); the 6 sums equal the reference sums, so no check was lost.
- E delivery: n/a.
- F measurement: FR-41 and AR-28: the seconds are provisional by check-site share and labelled as such; the first canon replaces them (`--slow-tests --from ... --update`).
- G code: FR-30 English: the new files carry no Cyrillic (`selftest.py --lang` ok); FR-29 no control byte (the tool wrote them); FR-31: no ceiling raised (one removed per file, the parts get the default 300); FR-32/FR-54: the siblings found are reported below.

AR touched: AR-13 (no new reader), AR-14 (keep rows only through split-keep), AR-15 (names once, tool (b)), AR-19, AR-20 (only shrinks: 3 TEST_TIMEOUTS rows removed), AR-22 (producers and readers land together: the parts, rows, slow_tests, timeouts and carriers are one tree), AR-25 (state-exits proofs re-pointed), AR-28.

## Questions (not decided)

1. **test-layers.json covers that name a shim** (verdict item 10: old :599 now :689 `test_conductor_doors.py` has `tests/test_no_move_seam.py`; :4331 `test_resume_packet.py` and :6840 `test_words_doors.py` have `tests/test_controller_rework.py`): NOT re-pointed. These three files import the shim (`from test_no_move_seam import raised, rig, verdict`; `import test_controller_rework as REWORK`), and the B2 guard (`test_selftest_slow_tests.py:477-489`) requires each keep row to cover every `tests/*.py` it imports; replacing the shim name with a part would turn B2 red (the importer imports the shim, which exists). Options: keep as is (my choice, B2 green); or add `tests/no_move_seam_common.py` / `tests/controller_rework_common.py` next to the shim so a change of the common reaches the importers' witness. Lead decides.
2. **state-exits.md:187 (E4)**: the named proof "K5-K9, K21-K26" is spread over four parts and cannot sit in one part (the N3 report asked the same). I named each part with its K range. If the Lead wants ONE part, the map needs a re-home (k21-k26 into one part) and a regeneration.
3. **changelog.d fragment** (step 5): see the table, not written, not in owns.
4. **driver-golden ceilings**: each of the five infra parts got the old 2400 s ceiling. Say if a different number is wanted.
5. **named_by in the new rows** is inherited and partly stale: handoff parts `design/state-exits.md:112` (the text is at :120); the controller_rework parts `state-exits.md:32` only (the :41 proof is in `_window_words`); infra and freshness parts' named_by is empty/by prose. `named_by` is informational (the gate_named set comes from carrier prose, `selftest.py:661`), so I left it.

## Needed beyond the manifest

- `docs/tasks/specs/reports/t-065..t-070 *.md` (carrier proposals per node: state-exits re-points), `tools/test_quarantine.py split-keep` usage, `test_silent_passes.py` K24 body, `driver_golden.py:205-245` (what `outside` and ceilings do), `tests/test_selftest_slow_tests.py:477-489` (B2). The files I edited under 4(d) that are not in `owns:` (`story_run_common.py`, `ticket_adapter.py`, `controller.py`, `driver_s0.py`, `driver_runner.py`, `audit_factory.py`, `scenario-clock.yml`, `test_conductor_doors.py`, `test_words_doors.py`, `test_controller_task_flag.py`, `test_runtime_paths.py`) are the one-line prose re-points of step 4(d); `driver_s0.py` and `driver_runner.py` are the driver parts that now hold the old story_run.py:126 and :5986.

## Carriers beyond the verdict list (re-pointed) and analogs (not touched)

- Re-pointed beyond the list: `test-layers.json:6081` prose (above); `driver_s0.py:20` and `driver-layers.json:31` note (the verdict named them by their old homes `story_run.py:126` and the driver-layers.json:25 note).
- NOT touched, needs a decision: `tools/source-split-carriers.json:19-20` names `scripts/tests/test_no_move_seam.py` as a `verify` arg of carrier row 4 (it still exists as a shim, runs 0 checks and exits 0, so it is a vacuous verify now; it should name a part, e.g. `test_no_move_seam_c26_g27_f2.py`). `tools/` is a non-goal here. `tools/test_test_split.py` lines 633/645/656/697/788 mention the six stems in docstrings and comments (history of the tool, no action).
- `story_run_freshness_common.answer_file` duplicates `story_run_common.d2_answer`; stale old-file labels in the generated runners (the argv comment "`test_infra_failure.py k2_... runs only those`" in each N1 part, the `sys.exit("test_story_run_freshness: no scenario...")` label in each N3 part): already in the critic's queue (t-072 Q6), tool level, not hand-edited.
- The CHANGELOG lines 3567, 3781, 4071 name the old files (history, left).

## git status --porcelain (worktree, uncommitted; ci-out/ is untracked scratch and is not listed here as it is ignored/handed back nowhere)

```
 M .github/workflows/scenario-clock.yml
 M ai-packages/qa-factory/design/architecture.md
 M ai-packages/qa-factory/design/state-exits.md
 M ai-packages/qa-factory/scripts/audit_factory.py
 M ai-packages/qa-factory/scripts/controller.py
 M ai-packages/qa-factory/scripts/driver_runner.py
 M ai-packages/qa-factory/scripts/driver_s0.py
 M ai-packages/qa-factory/scripts/selftest.py
 M ai-packages/qa-factory/scripts/slow_tests.json
 M ai-packages/qa-factory/scripts/tests/fixtures/driver-golden-rules.json
 M ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json
 M ai-packages/qa-factory/scripts/tests/story_run_common.py
 M ai-packages/qa-factory/scripts/tests/test-layers.json
 M ai-packages/qa-factory/scripts/tests/test_conductor_doors.py
 M ai-packages/qa-factory/scripts/tests/test_controller_rework.py        (now the shim)
 M ai-packages/qa-factory/scripts/tests/test_controller_task_flag.py
 D ai-packages/qa-factory/scripts/tests/test_handoff_values.py
 D ai-packages/qa-factory/scripts/tests/test_infra_failure.py
 M ai-packages/qa-factory/scripts/tests/test_no_move_seam.py             (now the shim)
 M ai-packages/qa-factory/scripts/tests/test_runtime_paths.py
 M ai-packages/qa-factory/scripts/tests/test_silent_passes.py
 D ai-packages/qa-factory/scripts/tests/test_story_run_freshness.py
 D ai-packages/qa-factory/scripts/tests/test_story_run_loop_b.py
 M ai-packages/qa-factory/scripts/tests/test_window_record.py
 M ai-packages/qa-factory/scripts/tests/test_words_doors.py
 M ai-packages/qa-factory/scripts/ticket_adapter.py
 M docs/SIBLING_MAP.md
 M docs/tasks/specs/reports/t-065-td11c-N1-map.json
 M docs/tasks/specs/reports/t-069-td11c-N3-map.json
?? ci-out/                                   (scratch, not handed back)
?? docs/tasks/specs/reports/t-084-td11c-NC.md (this report)
?? 29 files in scripts/tests/: 6 commons (controller_rework_, handoff_values_, infra_failure_, no_move_seam_, story_run_freshness_, story_run_loop_b_ `_common.py`) + 23 parts
```
The 23 parts: infra {classify,stops,retries,conductor_tracker,texts}, loop_b {loop,threshold,answers}, controller_rework {jobs_guard,repair_binding,window_words}, no_move_seam {n1_n9,n2b_n15,sites,k4s,c26_g27_f2}, story_run_freshness {k1_k5,k6_k7,k8_k14,k15_k26}, handoff_values {keys,refusal,main_block}.

Hygiene note: the two map edits (step 1) were made with `sed -i` on one token each (two one-line substitutions, `git diff` shows exactly 1 line per file); every later edit used the Edit tool. Two `cd` calls slipped in early in the session (read-only greps, no state change; the hook warned).
