# main-red8 report (branch wip/main-red8, base 2c8cf410)

Format per red: reproduced count -> cause (commit) -> fix (file) -> count after. W = ai-packages/qa-factory.

## R1 forge-check workflow steps
- reproduced: `python -m pytest tools/test_workflows.py -q` -> 1 failed, 26 passed (`assert 17 == 15` at test_workflows.py:169).
- cause: 5b1793c8 (P1-v N8) added two steps to forge-check.yml on purpose ("forge-check steps" is in its message): `measurers (run scoreboard tables)` and `scoreboard norms only tighten`; the test list was left at 15. WORKFLOW is the truth.
- fix: tools/test_workflows.py FORGE_CHECK_RUNS + 2 rows (`python -B experiments/measurers/test_measurers.py`; `scoreboard.py norms --check --against` / `norms --check`).
- after: 27 passed.

## R2 S3 card size and 'package defect' note
- reproduced: test_stage_cards.py 161/163 (S3 card 4127 B > 4000; no-'package defect'-note check).
- cause: bf19851d (FV1-28 C1) added a 241-byte line to the S3 card. The 'package defect' note is not a data defect: story_step._stage_card prints it exactly when the card is over CARD_MAX_BYTES (story_step.py:3278), so both reds are one cause. The line's full explanation already lives in the Actors paragraph further down s3.md (outside the card).
- fix: skills/qa-story/phases/s3.md line 17 shortened to `If accepted, once: <the record-sign-in command>` (card 3999 B, limit untouched).
- after: 163/163; S3 card 3999 bytes.

## R3 S5 plan brief ceiling
- reproduced: test_brief_pack_s5_plan.py 249/250 (K7 9702 B vs 9559 B).
- cause: 27d2e3cd (FV1-28 B1): measured by running the test at 27d2e3cd^ (9555 B, green) and 27d2e3cd (+147 B, wording of the first-look gap, head line plus file line, duplicate).
- fix: scripts/brief_pack.py: FIRST_LOOK_GAP = "First look: a GAP ({reason}); not a fact that there is no stand. {clause}"; first_look_input_line (both returns) = "- {display}: no first look ({reason})" (the head line of the same brief already carries "a GAP ... not a fact that there is no stand"); _CLAUSE_NAME "Name it as a gap where you need the stand."; _CLAUSE_LOOK "Where needed, look with your brief's tools."; reason "no record was written" -> "no record". Pins moved with the wording: tests/test_brief_pack.py (2 strings), test_first_look_briefs.py (6), test_first_look_wiring.py (3). Ceiling NOT raised.
- after: 250/250, RATCHET S5_PLAN_BRIEF_BYTES_MAX 9559 (at the ceiling, no headroom).

## R4 driver-layers census
- reproduced: test_driver_layers.py 280/283 (L4 two problems, L8 one, L11 one).
- NOTE: the task text said `repeat_recorded` "has no row"; reality: the row exists (01563f19) but is reported UNUSED, because Driver.record_repeat (driver_runner.py) reads the key through a local alias (`state = getattr(self, "state", None)`) and the L4 scanner sees only plain `self.state`.
- L4 `login_search`: cause b1f541ce (FV1-15); fix: driver-layers.json state_keys row {login_search, owner driver_stage_build (lowest module touching it: set in driver_machine, read in driver_stage_build)}.
- L4 `repeat_recorded`: cause 01563f19 (FV1-22 fix round); fix: scripts/driver_runner.py record_repeat uses plain `self.state` (behaviour identical when state is a dict; guarded by `has_state`).
- L8 test_human_questions.py `<module>`: cause a03ea511 (FV1-5) added a second module-level `python story_run.py` command text (STAND_TAIL); it is command text, not a source read; fix: source_mentions row count 1 -> 2 in driver-layers.json with the reason.
- L11 retro_numbers.py:2843 `from driver_dialog import DriverDialog` (cause ef5bdcfe, FV1-9 fix round F6): LEFT RED, see question 1. No exemption added.
- after: 282/283 (only L11).

## R5
- test_gate_brief_and_retro.py: 1087/1090 -> D8 cut packet 83 vs 84. Bisected by running the file at several commits: green at b17aeeb4^, red at d4f348a5. Cause b17aeeb4 (FV1-9 N2, `_help_lines` "tail", T6): a card with nothing that helps carries one more line (Q2 of the golden packet, line 34 of the cut packet), and the cap grows by it (`len(question_lines)` term). That is the commit's intended output (the whole-packet golden was already adjusted by ef5bdcfe). Fix: pin 83 -> 84 in the length, the last line and the sha256 (3830de60... -> 45da4c8b...). Not a ratchet. After: 1090/1090.
- test_resolver.py: 1146/1147 -> `source.count('".." in') == 1` got 2. Cause 2a4075b3 (FV1-23 A-2) added a second `".." in` predicate in runtime_paths.declared_place beside _climbs_out. The pin's intent is one predicate: fix the producer: scripts/runtime_paths.py new `_has_climb(text)` used by both sites. After: 1147/1147 (test_runtime_paths.py 169/169 too).
- test_brief_pack.py: 1168/1179 -> eleven reds, three causes. (a) stale test lambdas: `_fl_state=lambda task_root`, `_fl_body=lambda kind, task_root, got` in 3 places while the producer (27d2e3cd and its neighbours) now calls `_fl_state(task_root, kind)` and `_fl_body(kind, task_root, got, window)`: test lambdas updated (4 Q6/first_look_lines reds). (b) FV1-4 N1 role-brief ratchets (automator, case-designer, failure-analyst, runner, test-strategist): same cause as R3 (27d2e3cd, +147 B, runner/analyst +174 B) -> fixed by the same wording cut, no ratchet raised (ROLE_BRIEF_BYTES_MAX untouched). After: 1179/1179.

## Witnesses after the fix (tail lines, each run alone)
- `python -m pytest tools/test_workflows.py -q` -> `27 passed in 0.80s`
- test_stage_cards.py -> `=== test_stage_cards: 163/163 ok ===`
- test_brief_pack_s5_plan.py -> `=== test_brief_pack_s5_plan: 250/250 ok ===`
- test_driver_layers.py -> `=== test_driver_layers: 282/283 ok ===` (L11 open, question 1)
- test_gate_brief_and_retro.py -> `=== gate brief and retro numbers: 1090/1090 ok ===`
- test_brief_pack.py -> `=== test_brief_pack: 1179/1179 ok ===`
- test_resolver.py -> `=== test_resolver: 1147/1147 ok ===`
- test_role_load.py -> `=== role_load (the one measure of a role's start load): 186/186 ok ===`
- test_first_look_briefs.py 261/261, test_first_look_wiring.py 102/102, test_runtime_paths.py 169/169, test_probe_gap_door.py 54 passed (siblings of the changed code)
- `contract_slices.py --check` -> `slices: 44 declared, all present and fresh; 11 key pages; 12 charters carry a generated digest line`
- `selftest.py --limits --lang` -> `=== qa-factory selftest: 4/4 ok ===`

## Files touched
tools/test_workflows.py; W/skills/qa-story/phases/s3.md; W/scripts/brief_pack.py; W/scripts/driver_runner.py; W/scripts/runtime_paths.py; W/scripts/tests/fixtures/driver-layers.json; W/scripts/tests/test_brief_pack.py; test_first_look_briefs.py; test_first_look_wiring.py; test_gate_brief_and_retro.py; W/changelog.d/main-red-8.md; this report. (skills/ is outside the three owned package directories: s3.md is the file the R2 cause lives in.)

## Deviations / findings
- skills/qa-story/phases/s3.md is outside the owns list (scripts, references, handoffs); it is the only carrier of the S3 card. Named here.
- The task forbids running files of slow_tests.json, yet its own witnesses test_brief_pack, test_brief_pack_s5_plan, test_driver_layers, test_gate_brief_and_retro, test_resolver and (as sibling) test_runtime_paths are on that list; I ran them (alone, each under ~2 min), read as the task's explicit exception. For bisecting I also ran the first two/gate_brief file in throwaway detached worktrees at old commits (removed).
- Analogs (not widened): the 3 role ratchets and the S5 plan ceiling now sit at or within a few bytes of their limits (S5 plan 9559/9559, runner 5670 within 1-8 B), so any next first-look wording growth reds them again. The L4 scanner misses state keys reached through a local alias of `self.state` (a blind spot class; one more site would be silent in the other direction).
- Main checkout /c/QAFactory/forge-repo is behind 2c8cf410 (git log there misses newer commits); I read history through the worktree.

## Open questions
1. L11: scripts/retro_numbers.py:2843 imports `driver_dialog` directly to call `DriverDialog.role_words` (a one-line pure function). Options: (a) `from story_run import Driver` and `Driver.role_words(...)` (the facade door the check names; pulls the whole driver import into a retro reader), (b) an allowed_importers row (exemption, which I was told not to add), (c) move role_words to a lower neutral module. Not decided; L11 stays red, 282/283.
