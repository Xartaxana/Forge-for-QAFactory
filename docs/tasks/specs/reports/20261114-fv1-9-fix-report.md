# t-710 FV1-9 fix round: report

Branch wip/fv1-9-fix at a3f9a49 + merges of origin/wip/fv1-9-n1, n2, n4, n5 (all four merged with no textual conflict, in that order) + one fix commit (hash in the digest). Spec: verdict `docs/tasks/specs/reviews/20261114-fv1-9-topic-critic.md`.

## Verdict item -> change -> where -> test row

| item | what changed | file | test row |
|---|---|---|---|
| B1 | the `--reword QID --question-file <file>` door with its JSON keys is now told in the question stop's hand-over text; the T11 row left conductor.md (12206 -> 11897 bytes); `REFERENCE_MD_MAX_BYTES` and the two test carriers N2 moved are back to 12000 (README.md files, builder-rules.md, test_plan_contract_text.py were not changed by N2: untouched) | `scripts/driver_dispatch.py` `register_words_to_conductor` (the `recorded is not None` text), `references/conductor.md`, `scripts/selftest.py:358`, `tests/test_conductor_investigates_first.py:231`, `tests/test_conductor_doors.py:31` | `selftest --limits` (below); K5 byte checks in test_conductor_investigates_first; test_conductor_doors SIZE_CAP. No test row pins the new hand-over sentence (see gaps) |
| B2 | both expected lines now `(from: AC3)` / `(from: spec)` | `tests/test_gate_brief_and_retro.py:2061,2065` | the same rows |
| F1 | T6 counts any non-blank `from` as a recorded origin; with no readings T6 prints as `NO_HELP_LINE_NO_READINGS` (no readings clause) | `scripts/gate_brief.py` (`_help_lines` tail, new constant next to `NO_HELP_LINE`) | `test_fv19_card_no_help_line`: bare card -> no-readings text and no "these readings"; blank / absent origin -> T6; unknown origin `spec` -> `(from: spec)` and no "not recorded" |
| F2 | `on_card` = the row is in gate A's list: after the answered/settled/hidden-repeat skips, True unless the row is `driver_owned` (that row is skipped by `still_open` too) | `scripts/gate_preflight.py` `check_open_questions`, the `self.add(...)` call | `test_fv19_rehearsal_skips_hidden_repeat`: `with_designer` row now `on_card` True (was pinned False) |
| F3 | `repeat_records` returns `present`; `numbers` emits `merged_questions: {"records": [], "unreadable": false}` when the register is present, none only without a register; unreadable stays `unreadable: true` with no none line (unchanged branch); texts and why printed whole | `scripts/question_register.py` `repeat_records`, `scripts/retro_numbers.py` `numbers`, `merged_question_lines` | `test_fv19_retro_lists_merged_questions` (register + no merge -> key + none line; no register -> no key; 250 and 201 characters whole); `test_fv19_repeat_records_history` (`present` False for a missing root, True with a readiness file) |
| F4 | one helper `reword_entry(item) -> (qid, spec, problem)` and one `REWORD_ENTRY_FORM` in question_register; both carriers call it. The case side now also says "is not an object" for a non-object entry; the key-level check (non-list / empty key) stays in the plan carrier, where the plan row is the unit (the case side reads its key through `parse_json_list`) | `scripts/question_register.py` (`reword_entry`, `rewords_for_case.one`), `scripts/planning_contract.py` `_reword_plan_entries` | existing N1/N4 reword rows (test_question_register, test_gate_question_form) pass unchanged |
| F5 | T10 names `controller.py --operation rework --stage S2 --role qa-requirements-tester` and prints `--task {self.task}`; `<T>` only when `self.task` is empty | `scripts/driver_gates.py` `conductor_text` | `test_fv19_conductor_text_note_door`: word-for-word T10 with task `T-1`; new row: empty task keeps `<T>` |
| F6 | `merged_question_lines` reads `DriverDialog.role_words` (lazy import) instead of the copy; an absent `declared_by` still prints "an unrecorded role" | `scripts/retro_numbers.py` | existing row "the role is in words" (`by test strategist at S3`) |
| F7 | `_one_line` removed, `_squeeze` is the survivor. Difference: `_squeeze(None)` is `""`, `_one_line(None)` was `"None"`; every caller passes an exception, so no behavior changed | `scripts/question_register.py` | none (internal) |

## Verification (verbatim)

Slow files named by `scripts/slow_tests.json` and therefore dropped from the local run, judged by the batch canon: test_gate_words_road.py (68.0 s), test_person_words.py (35.2 s), test_gate_brief_and_retro.py (106.3 s), test_conductor_doors.py (53.0 s), test_report_facts.py (55.6 s). B2's fixture lines are only judged by the canon.

```
( cd .../qa-factory && python -B scripts/selftest.py --limits --lang )
PASS lang: no Cyrillic anywhere in the package
PASS lang: no control byte left by an eaten escape sequence (FR-29)
PASS limits: SKILL.md / agents / references within size caps
PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier
=== qa-factory selftest: 4/4 ok ===
```
(run before the last two small test edits; no package source changed after it. conductor.md: `wc -c` 11897.)

```
python -B scripts/tests/test_conductor_investigates_first.py     -> === test_conductor_investigates_first: 33/33 ok ===
python -B scripts/tests/test_question_register.py                -> === question_register: 878/878 ok ===   (first run 876/877: the pin of repeat_records' old shape, fixed above)
python -m pytest scripts/tests/test_retro_numbers.py scripts/tests/test_gate_question_form.py scripts/tests/test_judgment_census.py -q
                                                                  -> 63 passed in 127.60s
python -m pytest scripts/tests/test_judgment_census.py -q         -> 25 passed in 102.98s   (the critic's request; census file untouched, no refusal unit added or removed)
```
test_question_register.py and test_conductor_investigates_first.py are script-style files (own harness); `pytest` on them errors at collection (`fixture 'tmp' not found`, `SystemExit`), so they were run with `python -B` as above.

`scenario_walk.py --witness-for scripts/<each owned script>` prints "keep <file> (layer ..., covers it)" lines, a naming of covering files, many of them slow (driver_dispatch and driver_gates name test_walk_*, test_words_doors, test_driver_layers, test_check_delivery, test_story_run_* ...). Not run by me: all of those are "judged by the batch canon". The full lists were printed for driver_dispatch (first lines: test_audit_rules, test_bug_records, test_case_versions_scope, test_check_delivery, test_codex_tool_guidance, test_conductor_doors, test_console_encoding, test_controller_gate_decision ...) and gate_brief (incl. test_scenario_cart_1, test_scenario_local_1_0108, test_story_run_s6, test_whole_identifier).

## FR walk (touched sections) and package lines

- A (refusals): reword_entry's problem texts keep "Expected: <form>" (FR-1); the hand-over text names the door (FR-2: the conductor can use it).
- B (text to a person): the card's T6 line changed; F1 removes a self-contradicting card (FR-10); T6 wording passes `human_text.problems` rows (`fv19_human_text_passes` runs in test_gate_question_form: passed).
- C (contracts): `present` has producer `repeat_records` and reader `numbers` in one commit (FR-14, AR-22); F4 one shared entry check.
- D, E: not touched except FR-41/AR-23: with a register, "no merge" is stated, an unreadable register says so.
- F, G: no measurement touched; text is English, `--lang` passes (FR-30); no heredoc code (FR-29).
- architecture: AR-10 (door told at the hand-over, where the conductor needs it), AR-13 (one reader role_words; one reword_entry), AR-15 (shared problem at one survivor), AR-20 (a cap raise is REVERSED: 12206 -> 12000, shrink only), AR-22/AR-23 (present, none line), AR-28 (unknown register stays unreadable, not none).
- judgment: none -- data rendering and a shared shape check; no judgment moved; census run attached, unchanged.

## Gaps, questions, analogs

- Gap (needs a Lead decision, not done): no test row pins the new `--reword ... --question-file` sentence in `register_words_to_conductor`: the hand-over text is built inside `Driver` and the existing tests that call it (`test_story_run_loop_b_threshold.py`, in `driver-layers.json`) are outside my owns and slow. Add a row there if wanted.
- F2 divergence from the verdict's wording ("True for every finding that reaches add"): I excluded `driver_owned` rows, because `still_open` skips them too (gate_brief ~4360), so "in gate A's list" is False for them. Cheap to flip.
- F1: the no-readings T6 wording is mine, derived by dropping the readings clause: "the factory has found nothing more than what is shown here; answer from what you know of the product, or in your own words." Spec T6 says nothing of the no-readings text.
- F3(b): texts are uncut as the Lead confirmed; the spec's T16 / AT-BEYOND rows still say 200 characters: amend the spec (not mine). 
- Analogs noticed: the verdict's P1 to P7 (not touched). `story_progress._role_words` (239) is still a third copy of `driver_dialog.role_words`; I replaced only the retro copy (owns). Other `_one_line` helpers exist in blast_radius, brief_pack, bug_records, gate_brief, person_owned, traceability (different bodies/limits: not clones of the removed one).
- Needed beyond the manifest: `scripts/question_stop.py`, `scripts/tests/test_judgment_census.py`, `scripts/slow_tests.json`, `scripts/driver_dialog.py` (read), `git diff eb6dd02 origin/wip/fv1-9-n2` for the carriers.
