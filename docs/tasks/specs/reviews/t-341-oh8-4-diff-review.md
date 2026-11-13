# t-341: critic diff gate, OH8-4 Parts 1 + 2 after convergence (head 5efb17e)

Scope: `git diff 6e3133f refs/remotes/origin/wip/oh8-4` (17 files, +340/-45), tree `.claude/worktrees/oh8-4` at 5efb17e.
DoD: spec `docs/tasks/specs/t-322-oh8-4-plugin-root-literal.md` §3, §5, §7a, §7b (binding); plan review t-327.

## Verdict: fit_with_fixes (NEEDS WORK). 2 blocking findings (B1, B2), 3 fix-now minors (M1-M3), 5 follow-ups (F1-F5)

The design is right and the code does what the spec says. Every site C1-C6 and C8-C13 now goes through `RP.script_command`
with the root its row names. C7 was dropped as §7b B2 says. The token expander and the one reader do what §3.2 says.
But one keep detector is red at the head because of C13b, and the Part 1 witness says it was green. That is why this
verdict is not fit. The fix is small and mechanical: one pin re-spelled, then the witness re-run in full.
Accepting the node is the coordinator's decision (rule 6). This verdict is an input to it.

## Findings

### B1 (blocking): keep detector `test_words_doors.py` is red at 5efb17e, caused by C13b
- Where: `ai-packages/qa-factory/scripts/story_step.py:734` (`run_mode_refusal`). The door was
  `python \"{HERE.as_posix()}/waiver.py\" --task ...` and is now `{RP.script_command('waiver.py')} --task ...`.
  The scan in `test_words_doors.python_texts` renders that placeholder as bare `waiver.py`. The closing `"` after the
  script name is gone.
- The pin in `scripts/tests/test_words_doors.py:91` still expects the old rendering:
  `"scripts/story_step.py": ('waiver.py" --task {} --stage {} --block "{}" --decision "',)`.
- Witness (my run, `python -B .../scripts/tests/test_words_doors.py`):
  `FAIL no inline door outside the exemption and the pending list (B-387) — expected {}, got {'scripts/story_step.py': ['waiver.py --task {} --stage {} --block "{}" --decision "']}` /
  `=== test_words_doors: 597/598 ok ===`.
- Layer: `test-layers.json` → section `keep`, `"layer": "detector", "why": "sole AR-24 detector"`. It is not quarantined.
- Cause confirmed: base 6e3133f `story_step.py:734` has `waiver.py\"`. `test_words_doors.py` is not in the diff, and it is
  byte-identical at d6e1553, 6e3133f and the head.
- Class: Axis 5's row "Carriers of a person's words" (`docs/SIBLING_MAP.md:141`) names `test_words_doors` as the
  detector of person-words doors. Part 1's axis block says "axis 5: covered stage twins" but did not walk this row.
- Fix (fix round, Lead adds the path to owns):
  - In `test_words_doors.py:91`, change the pending entry to
    `"scripts/story_step.py": ('waiver.py --task {} --stage {} --block "{}" --decision "',),`.
  - Fix the comment at :86-89. "the second one keeps the quote that closes the script's path" no longer holds for
    story_step.py.
  - Do NOT add a mask or an exemption.
  - Witness: `python -B .../scripts/tests/test_words_doors.py` reports 598/598.

### B2 (blocking): the Part 1 witness cannot be reproduced
- The mechanical layer says: "witness-for printed 136 files and all were run: 134 green, 2 red (the frozen fixtures)".
  That cannot be true.
- `python -B .../scenario_walk.py --witness-for scripts/story_step.py` prints
  `scripts/story_step.py: keep test_words_doors.py (layer detector, covers it)`. That file is red as soon as d6e1553
  lands (B1). Nothing else touches it.
- Either the file was not run, or its red was misread. Rule 7 and rule 12: a load-bearing claim that cannot be
  reproduced is a NEEDS-WORK finding.
- Fix: after B1, re-run `scenario_walk.py --witness-for <union of both parts' owns>`. At the head this prints 157 distinct
  test files (my count). Attach the verbatim `=== ... ===` tail of every printed non-quarantined file to the acceptance.
  Do not attach a summary count.

### M1 (fix now, minor): an unknown `{script:x.py}` in stand-answers.json passes the data join silently
- Where: `scripts/tests/test_ahead_cards.py` `charter_card_join`, at the end of the stand-answers block (after the
  `"{script:" not in json.dumps(table)` check).
- `expand_script_tokens` turns a token for a script that does not exist into the gap text. That keeps FR-59: no
  non-existent path is printed. But the gap text says "the conductor runs qa-doctor to repair the installation", and
  for a typo in a shipped data row that is the wrong owner.
- The join only checks the two current rows by name, so a typo in any other row passes.
- Probe (a copy of the table with `{script:stand_helth.py}` appended to `remedy.no_recipe`, `STAND_ANSWERS_PATH`
  pointed at the copy):
  - all three current checks pass: `check1 True` / `check2 True` / `check3 no token True`;
  - the proposed check fails: `proposed check: no gap text False`.
- Fix: add one row,
  `check("no string of the loaded table names a script missing from this copy", "(missing from the plugin copy at" not in json.dumps(table), ...)`.

### M2 (fix now, minor): the frozen-fixture refresh is not recorded in the fixtures' own docstrings
- Where:
  - `scripts/tests/test_story_run_s6_w1_frozen.py:35-36`: the precedent line "Retaken on 12.11.2026 at tree 8afd343
    (the owner's word, t-107) ...";
  - `scripts/tests/test_story_run_s5_n1_frozen.py:4-5`: "taken ONCE from the tree under TR3-6".
- 5efb17e changes the fixtures, but each docstring still says the capture is as first taken.
- Fix: add one line to each docstring:
  `Refreshed 13.11.2026 at 5efb17e (OH8-4 C11, t-340): calls.json only; the card head's <plugin>/scripts/<name>.py became one double-quoted word in every prompt (s5: 9, s6: 2); events, state_keys and console byte-equal.`
- Whether this refresh needs the owner's word, as the s6 retake cited, is the coordinator's call. My input: no road
  changed (see Q1). The s6 precedent cited the owner's word because that retake also brought the file back from
  quarantine.

### M3 (fix now, minor; code quality, brief item 7): redundant imports in `role_text_roots`
- `test_ahead_cards.py:199`: `import handoff as handoff_form`, but the module header already imports `handoff` (:46).
  Use `handoff.template(...)`.
- `test_ahead_cards.py:407`: `sys.path.insert(0, str(Path(harness.__file__).resolve().parent))` repeats :36 (the tests
  folder is already on the path). Each call adds the folder to `sys.path` again. Drop the line.

### F1 (follow-up, onboarding-hooks, next untaken batch): R1, hand-made `self.scripts` spellings in the driver
- All of these are still present at the head:
  - `driver_runner.py:1080-1083`, `:1107`
  - `driver_dialog.py:275`
  - `driver_gates.py:1168`
  - `driver_machine.py:147`, `:1715`, `:3913`
  - `driver_stage_build.py:504`
- Queue them as one node, with rows added to `role_text_roots`.
- That node must carry B1's lesson. `driver_gates.py:1168` and `driver_machine.py:147/:3913` are waiver doors pinned
  in `test_words_doors.py:82-83` (DRIVER_KEY, one of them with the `waiver.py"` quote form). Put that file in the
  node's owns from the start.
- Fold in F4.

### F2 (follow-up, OH8-5): conductor literals
Still present: `story_step.py:1034`, `:1101` and `stage_done.py:209`. The Остатки line is below.

### F3 (follow-up, onboarding-hooks, with OH8-5): R4, widen `refusal_registry._host_root_lines`
- `refusal_registry.py:1125` scans only `SCANNED`.
- OH8-4 has fully cleared four files of the variable: `driver_dispatch.py`, `driver_stage_s7.py`,
  `execution_request.py` and `handoff_check.py`. My Grep -i found 0 hits in those four.
- The ratchet can take them now. `story_step.py` and `stage_done.py` can follow once OH8-5 is done.
- This is the class detector that t-327 N3 asked for.

### F4 (follow-up, inside F1): two placeholder words for one card head
- C11 (`driver_dispatch.py:698`) spells `script_command('<name>.py', ..., must_exist=False)`.
- `brief_pack.py:3707` and `:4291` spell `script_command('<script>', must_exist=False)`.
- The command form is the same, but the placeholder word differs. Pick one word (P10). Cosmetic, so not blocking.

### F5 (informational): an inaccurate line in the converge commit message
The 5efb17e message says "merge of two reviewed parts" / "already-reviewed parts". Only the plan had been reviewed
(t-327). This review is the first code review. Do not repeat the claim in the `accepted` event.

## Answers to questions 1-5

**1. Frozen fixtures.**
- I verified with `git diff --word-diff=porcelain 6e3133f origin/wip/oh8-4 -- '*calls.json' | sort | uniq -c`.
- Result: exactly `11 -<plugin>/scripts/<name>.py\`;` and `11 +\"<plugin>/scripts/<name>.py\"\`;`. There is no other
  token change. `--numstat` gives 9/9 for s5 and 2/2 for s6.
- What the fixtures protect is the serial road: the call order, events, state keys and console (see their docstrings).
  The card head is text captured as a side effect in every prompt, and mask M1 already replaces the root inside it.
- events, state_keys and console did not change, and per the attached witness the compares are green (6/6, 4/4).
- So a quoting-only refresh does not defeat the fixture. Adding a mask would ("Never mask it").
- Acceptable, with the record M2 asks for.

**2. C11.** It is a real row, not an exemption.
- It drives the REAL `Driver.run_role` on a seeded story (`common.seed` + `driver_for`), with `run_claude` stubbed to
  capture the prompt.
- It checks that the head holds `` `python "<spaced>/scripts/<name>.py"` ``, which is E2: one double-quoted word.
- The old hand spelling, unquoted and native-separator, fails that check, so the row tells the two apart.
- `must_exist=False` is edge E23 as §7b B4 wrote it. No row asserts a copy without `scripts/`, by design: qa-doctor owns
  that gap.
- The prompt and the brief card (`brief_pack.py:3707`) spell the root through the same survivor. In driver mode both
  resolve to `self.plugin`: `story_step` runs from `self.scripts`, so its `package_root()` is that copy.

**3. Part 2 tokens.** My probe used `expand_script_tokens` and `env_probe.stand_answers()` at the head:
- Unknown `{script:nope.py}`: gives the gap text `` `nope.py` (missing from the plugin copy at <root>; ...) --x ``, and no
  python path. FR-59 holds. The gap is invisible to the join (M1).
- Malformed tokens (`{script:x.txt}`, `{script:Stand_Health.PY}`, `{script: stand_health.py}`, plus the four T-bad rows):
  left exactly as written. In shipped data the join's `"{script:" not in json.dumps(table)` check catches them, so they
  cannot leak.
- In the stand answers: the token is expanded once, by the one reader at load, with root `package_root()`. That is the
  copy whose `stand_health` prints the sentence, so FR-37 holds.
  - The one-reader claim is confirmed. Grep -i `stand-answers|stand_answers\.json|STAND_ANSWERS_PATH` over the package's
    `*.py` finds only `env_probe` plus tests.
  - The non-`.py` search finds only the changelog and the file itself, so no markdown door reads it raw.
- `fill` after expansion: the expanded path holds no braces, and `fill` leaves an unknown placeholder alone (E14).
- `{{script:x.py}}` gives `{python "..."}`. No such row exists, so this is not a finding.

**4. Class completeness.**
- All R1 sites are confirmed present. Queue them as one node in the next untaken onboarding-hooks batch (batch-8 is
  taken). Its owns must include `test_words_doors.py` (F1).
- OH8-5 takes `story_step.py:1034/:1101` and `stage_done.py:209` (F2).
- R4 is in F3. R2 (`human-text.json` `plugin_path`) stays as the spec named it.
- `brief_pack`'s card head is already on the survivor (`brief_pack.py:3707`, `:4291`). There is no "Plugin root:" literal
  in `brief_pack`. Grep -i "Plugin root:" over the package finds only C11, `driver_conductor.py:316` and
  `driver_stage_s8s9.py:395` (bare roots, not commands) plus the tests. Only the placeholder word differs (F4).
- The one map miss inside this diff is the Axis 5 words-door row (B1).

**5. Duplication and consistency (brief item 6).**
- The three `cmd = lambda name: RP.script_command(name, self.plugin)` bindings (C1, C3, C4) are what spec §3.1 allows.
  The spec forbids a new Driver method.
- `env_probe._expand_tokens` is a 10-line walk over nested values. The nearest existing walker,
  `runtime_paths._read_record.read` at :993, has drop semantics, so it is not a reuse candidate.
- No second token parser: Grep for `{script:` / `SCRIPT_TOKEN_RE` finds only runtime_paths, env_probe and tests.
- `{script:}` and `PLUGIN_TOKEN` are two distinct actions (§7b B6), each with one road.
- The clone ratchet output was not attached. Its absence is noted here; I did not re-derive it.

**Code quality (brief item 7).**
- `role_text_roots` (`test_ahead_cards.py:385-566`, about 180 lines) is over 60 lines. The DoD prescribed exactly ONE
  function with site rows, so I do not raise it. If it grows in F1, split it into per-row helpers.
- M3 above.

**One road (item 12).** D1-D3 use a card marker and D4-D5 a token. That is a data-row difference: raw-read files have no
reader function, and the table has exactly one. No language, project or case is excluded. There is nothing to report.

**Standing question 10 (AR-n).** The part commits name AR-8, AR-13, AR-15, AR-5, AR-9 and AR-22. The code keeps them:
- AR-13: my Grep -i over the owned files finds only the OH8-5 sites and a comment at `story_step.py:693`.
- AR-5: neither `script_command` nor `expand_script_tokens` reads `os.environ`.
- AR-9: `refusal_registry --check` rc 0.

**Standing question 11 (judgment, AR-29).** No check unit was added. `expand_script_tokens` is a text transform, and the
new assertions are test rows. `test_judgment_census` is 22/22 on my rerun.

**Hygiene (item 8).** All seven Part 2 files: 0 control bytes, LF kept, nothing turned into CRLF. FR-29 holds despite the
heredoc WARN. `selftest --limits --lang` is 4/4.

## Остатки lines for batch-8 (ready to paste into `## Остатки`, at node acceptance; the coordinator writes them, §7b N2/N3)

```
- OH8-4 передаёт в OH8-5 литералы, которые читает дирижёр: `scripts/story_step.py:1034` и `:1101` (дверь «следующий блок», `story_step.py start`) и `scripts/stage_done.py:209` (`current_code_diff_refusal`, дверь S1 `--set implementation_source=diff`; снят с OH8-4 решением t-327 B2) — через `runtime_paths.script_command` после опыта с хостом OH8-5 | узел: OH8-5
- R4 (t-327 N3, t-341 F3): расширить `refusal_registry._host_root_lines` (`SCANNED`, `refusal_registry.py:1125`) на файлы, очищенные OH8-4 (`driver_dispatch.py`, `driver_stage_s7.py`, `execution_request.py`, `handoff_check.py`: 0 вхождений по Grep -i), и после OH8-5 — на `story_step.py`, `stage_done.py`; детектор класса «литерал корня плагина в тексте роли» | узел: OH8-5
- R1 (t-322 §6, t-341 F1/F4): ручное написание `self.scripts` в текстах драйвера — `driver_runner.py:1080-1083`, `:1107`, `driver_dialog.py:275`, `driver_gates.py:1168`, `driver_machine.py:147`, `:1715`, `:3913`, `driver_stage_build.py:504` — перевести на `script_command`, строки в `test_ahead_cards.role_text_roots`; в owns сразу `scripts/tests/test_words_doors.py` (пины DRIVER_KEY :82-83); одно слово-заполнитель с `brief_pack.py:3707/:4291` | перенос: onboarding-hooks/findings/<файл находки R1> | обоснование: пачка 8 взята, другой набор горячих файлов (5 файлов driver_*) | подтвердил: —
```
The R1 line needs a human confirmation (`подтвердил:`). Until it has one, `piles.py close` refuses it (PROJECT.md
«Командная работа» item 9). The finding file and its untaken-batch row come in the same move (D-0044).

## Trail

Read:
- the spec t-322 (whole) and review t-327 (headings and keys);
- `critic-diff-brief.md` items 6-8 and "The two layers";
- the full diff;
- at the head:
  - `runtime_paths.py:225-285` and `:980-1010`;
  - `env_probe.py` (`fill`, the table consumers);
  - `test_ahead_cards.py` (imports :29-49, the new code);
  - `test_story_run_s6_w1_frozen.py:1-60`, `test_story_run_s5_n1_frozen.py:1-40`;
  - `test_words_doors.py:60-100`, `:174-204`, `:335-356`;
  - `test_package_generation.py:466-482`, `:520-527`;
  - `refusal_registry.py:1125-1160`;
  - `driver_core.py:416-417`;
  - `brief_pack.py` Grep;
  - `test-layers.json` rows for test_words_doors and test_package_generation;
- `docs/SIBLING_MAP.md` axis list and :141;
- the batch-8 Остатки header;
- the commit messages of d6e1553, 7679f82 and 5efb17e;
- the git history of both fixture files.

Searches, all case-insensitive where content-negative:
- `claude_plugin_root|HERE.as_posix()` over the six owned code files;
- `self.scripts` in `driver_*`;
- the hand-spelling regex over `scripts/*.py`;
- `stand-answers` readers (py, then non-py);
- `Plugin root:`;
- `_host_root_lines`.

Positive controls: the `stand-answers` Grep found `env_probe.py:222`; the hand-spelling Grep found the known R1 sites.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1: keep detector test_words_doors.py red 597/598 at 5efb17e - story_step.py:734 (C13b) now renders `waiver.py --task` and the pending pin at test_words_doors.py:91 still expects `waiver.py\" --task`",
    "B2: Part 1 witness claim (134 green, only the 2 frozen red) not reproducible - witness-for scripts/story_step.py prints test_words_doors.py, which is red from d6e1553 on"
  ],
  "fixes": [
    "B1: re-spell the story_step entry at test_words_doors.py:91 to 'waiver.py --task {} --stage {} --block \"{}\" --decision \"' and fix the comment at :86-89; Lead adds the file to owns; no mask, no exemption",
    "B2: re-run scenario_walk --witness-for over the union of both parts' owns (157 files at head) and attach every non-quarantined file's tail verbatim",
    "M1: in test_ahead_cards.charter_card_join add a check that no string of the loaded stand-answers table holds '(missing from the plugin copy at'",
    "M2: one 'Refreshed 13.11.2026 at 5efb17e (OH8-4 C11, t-340)' line in the docstrings of test_story_run_s6_w1_frozen.py and test_story_run_s5_n1_frozen.py; coordinator decides whether the owner's word is needed",
    "M3: test_ahead_cards.py:199 use the module-level handoff import; drop the duplicate sys.path.insert at :407"
  ],
  "class_completeness": "Inside the diff: Axis 5 row 'Carriers of a person's words' (SIBLING_MAP.md:141, detector test_words_doors) was not walked - B1. Outside: R1 driver sites (driver_runner 1080-1083/1107, driver_dialog 275, driver_gates 1168, driver_machine 147/1715/3913, driver_stage_build 504) confirmed present, to a new node in an untaken onboarding-hooks batch with test_words_doors.py in owns; OH8-5 takes story_step 1034/1101 and stage_done 209; R4 widens refusal_registry._host_root_lines (four files already clear); brief_pack card head already on the survivor, only the placeholder word differs (F4). Ready-to-paste Остатки lines are in the review file.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-322-oh8-4-plugin-root-literal.md",
      "docs/tasks/specs/reviews/t-327-oh8-4-plan-review.md",
      "docs/tasks/critic-diff-brief.md",
      "git diff 6e3133f origin/wip/oh8-4 (all 17 files)",
      "ai-packages/qa-factory/scripts/runtime_paths.py",
      "ai-packages/qa-factory/scripts/env_probe.py",
      "ai-packages/qa-factory/scripts/tests/test_ahead_cards.py",
      "ai-packages/qa-factory/scripts/tests/test_words_doors.py",
      "ai-packages/qa-factory/scripts/tests/test_story_run_s6_w1_frozen.py",
      "ai-packages/qa-factory/scripts/tests/test_story_run_s5_n1_frozen.py",
      "ai-packages/qa-factory/scripts/tests/test_package_generation.py",
      "ai-packages/qa-factory/scripts/tests/test-layers.json",
      "ai-packages/qa-factory/scripts/refusal_registry.py",
      "ai-packages/qa-factory/scripts/brief_pack.py",
      "docs/SIBLING_MAP.md",
      "plans/piles/onboarding-hooks/batch-8-ostatki-t-282-t-254-t-287.md"
    ],
    "reruns": [
      {"command": "git diff --word-diff=porcelain 6e3133f origin/wip/oh8-4 -- '*calls.json' | sort | uniq -c", "result": "11 removals and 11 additions, all the C11 head quoting; nothing else"},
      {"command": "python -B scripts/tests/test_ahead_cards.py", "result": "296/296 ok"},
      {"command": "python -B scripts/tests/test_runtime_paths.py", "result": "130/130 ok"},
      {"command": "python -B scripts/refusal_registry.py --check", "result": "rc 0, no violations"},
      {"command": "python -B scripts/tests/test_judgment_census.py", "result": "22/22 ok"},
      {"command": "python -B scripts/selftest.py --limits --lang", "result": "4/4 ok"},
      {"command": "python -B scripts/tests/test_words_doors.py", "result": "597/598 - FAIL inline door scripts/story_step.py (B1)"},
      {"command": "python -B scripts/tests/test_conductor_doors.py, test_human_questions.py, test_gate_registry.py, test_silent_passes.py, test_whole_list_sites.py, test_person_owned_paths.py", "result": "218/218, 291/291, 438/438, 326/326, 292/292, 96/96"},
      {"command": "probe: expand_script_tokens on unknown, malformed and doubled-brace tokens; stand_answers on a table copy with a typo token", "result": "unknown gives the gap text, malformed unchanged; the typo passes all three current join checks (M1)"}
    ]
  }
}
```
