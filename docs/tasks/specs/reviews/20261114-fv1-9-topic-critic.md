# FV1-9 topic critic (t-701): N1, N2, N4, N5. Diff gate before the merge into main

Spec/DoD: `docs/tasks/specs/20261114-fv1-9-question-repeats-spec.md`, read whole. Brief: `docs/tasks/critic-diff-brief.md`.
Diffs: N1 `eb6dd02..148c057`, N2 `148c057..d4f348a`, N4 `148c057..672786c`, N5 `148c057..859b766`.

## Verdicts

| node | verdict | merge-blocking |
|---|---|---|
| N1 | fit_with_fixes (minor: F3a, F7) | none |
| N2 | fit_with_fixes | **B1, B2**: the canon goes red on merge |
| N4 | fit_with_fixes (F4) | none (P1 must land before N3) |
| N5 | fit_with_fixes (F3) | none |
| **topic** | **fit_with_fixes** | B1, B2 block the N2 merge only. N1, N4 and N5 can merge on their own after N1 |

Accepting the work is the Lead's call (rule 6). The cap raise in B1 also needs the owner's word.

## Blocking (N2, fix in this round)

**B1: `conductor.md` at 12206 bytes turns two canon tests red.** `test_gate_words_road.py:391` checks
`len(conductor.md.read_bytes()) <= 12000`. `test_person_words.py:673` checks `content_bytes(...) <= 12000` for conductor.md and
controller-api.md. Both are keep rows in `test-layers.json` (2128, 7113), so the canon runs them. `wc -c` gives 12206, so both fail
on a fixed number. Round 2 moved only 3 of the cap's carriers. The fix is under Q1.

**B2: a canon fixture pins the old origin text.** `test_gate_brief_and_retro.py:2061,2065` (keep row, line 1853) expects
`  - a) at the root (from AC3)` and `  - b) nowhere (from spec)`. `gate_brief._origin_part` (2844) now prints `(from: AC3)` and
`(from: spec)`, because these words are not in `reading_origin_words`. The change is intended (T7), so the fix is to update both
expected lines in this round. `test_d1_answer_card.py:112` is quarantined (line 7835) and only checks `"  - b) "`, so it does not
break.

## Fixes for this round (not blocking)

- **F1 (N2, `gate_brief._help_lines` tail, 2859-2915): T6 contradicts its own card (FR-10).**
  - `known` counts only origins the data file knows. A card can show `(from: spec)` and then T6, "where these readings come from is
    not recorded".
  - `test_fv19_card_no_help_line` pins exactly this ("readings with an unknown origin word").
  - Unknown origins are exactly the rows `question_errors` flags (`contract.py:659`), which is the R4 class this card exists for.
  - A card with no readings also gets "these readings".
  - Fix: count any non-blank `from` as recorded. With no readings, print T6 without the readings clause. Update the pin.
- **F2 (N2, `gate_preflight.check_open_questions`, the `on_card=` argument): the predicate is the stop's (`is_open`), but the top
  block it filters belongs to gate A.**
  - Gate A's card list is `still_open` (gate_brief 4328). Its docstring says it lists `with_designer` and deferred rows, and it
    lists unmatched rows too.
  - Scenario: Q3 is `deferred_to_report` and fails `question_errors`. The finding gets `on_card=False`, so after the cap Q3's
    defect line prints at the top ("not questions for you") while Q3's card stands below. That is the B4 class, left half-closed.
  - The spec's "with_designer row: no card" is wrong for gate A.
  - Fix: `on_card` = the row is in gate A's list, i.e. it got past the `row_answered`/`settled`/`hidden_repeat` skips. For every
    finding that reaches `add`, that means True.
- **F3 (N5 `numbers`; N1 `repeat_records`): empty outcome (Q5).**
  - (a) Add `present` (the register exists) to `QR.repeat_records`. When the register is present, always emit
    `merged_questions: {"records": [], "unreadable": false}` and the T16 none line. Leave the key out only when there is no
    register.
  - Fix the test row "a story with a register and no merge has no key" to match.
  - (b) If the Lead confirms: texts uncut (amend spec T16 and the AT/BEYOND rows).
- **F4 (N4 `_reword_plan_entries`, planning_contract 3351-3394; N1 `rewords_for_case.one`): the reword-entry check and the spec
  build exist twice and already differ.** The plan side reports an empty or non-list key; the case side does not. Fix: one QR
  helper (`entry -> (qid, spec, problem)`) that both carriers call.
- **F5 (N2 `DriverGates.conductor_text`, T10).**
  - The text says `controller.py rework --stage S2 ...`, but the conductor's own table writes `controller.py --operation rework`
    (`conductor.md:35`).
  - It also prints `<T>` although `self.task` is known; the same function prints `--task {self.task}` two lines above.
- **F6 (N5 `merged_question_lines`, retro_numbers ~2843):** the role-in-words expression is a verbatim copy of
  `driver_dialog.role_words` (`driver_dialog.py:59`). `story_progress._role_words` (239) is a third copy. Reuse one survivor, or
  queue the convergence as a node.
- **F7 (N1):** `_one_line` and `_squeeze` are the same expression, added in the same diff. Keep one.

## Proposed nodes (owner: the FV1-9 Lead; opening a node is the Lead's call)

- **P1 (AR-22, Q4): the refusal lines of all three reword/repeat carriers reach no role and no conductor.**
  - `project_plan().notes`: the only caller (`driver_dispatch.py:2723`) reads `.problems` only, so the notes are fully silent.
  - `critic_rollcall` `question_notes`: printed on stdout only. The driver runs it with no reader (`driver_stage_plan.py:761`).
  - `raise_from_handoff` `reword_problems`: run with `check=True` and its output dropped (`driver_stage_plan.py:647`).
  - Grep (case-insensitive) `reword_problems|question_notes|planned\.notes|question_pass_lines` over `scripts/*.py`: no driver
    reader. Control: the same grep finds `question_pass_lines` in `driver_dispatch.py:1674,1734,1802,1815`, the existing road to
    the resumed role.
  - Not a merge blocker: until N3 lands no role is told the keys, and a refused reword keeps the old words (toward asking).
  - It must land BEFORE N3 (AR-10: a role told of a door must hear its refusals).
- **P2 (AR-10): nothing tells the conductor about its `--repeat` CLI door.** T11 covers rewording only, and the spec has no
  conductor text for a repeat. Put it with P1, in the hand-over text.
- **P3 (axis 5, skill road ↔ driver):** `phases/s2.md:108` and `phases/s4.md:222` tell the interactive path how to record answers.
  They have no `--note`/`--reword` door and no T10 equivalent. Add a node, or record an explicit n/a while the phases retire
  (t-301 N6).
- **P4 (sibling of "count what is shown"):** `report_facts.question_count` (2399-2412) counts hidden repeats as questions put to
  the person. Hidden repeats should be excluded, the same way `with_designer` is.
- **P5:** `_main_fv19` passes `stage=""` although `--stage` already exists in `_VALUE_OPTIONS`. The retro then prints "by
  conductor at an unrecorded stage".
- **P6:** a reword from a carrier is not idempotent across a crash. The register is written before the case or plan is rewritten.
  On replay the entry stays and is refused forever ("not shown").
- **P7 (code quality):**
  - `question_register.reword` is about 93 lines (1571-1663).
  - `gate_brief._help_lines` nests 4 levels deep in its `notes` part (2859-2915).
  - `question_card` is now about 110 lines (2734-2843).
  - Split validation from the write.

## The Lead's questions

**1. The cap: should the global raise stay? No.**
- It loosens the cost guard for every reference. `controller-api.md` (11998) and `manual-evidence.md` (11987) silently gain about
  200 bytes of growth room.
- It is also incomplete (B1).
- The row costs exactly 309 bytes: the file goes 11897 → 12206, so 206 bytes have to go.
- Preferred fix: T11's situation ("their words show they could not tell what it asks") only arises in the stop's hand-over,
  `driver_dispatch.register_words_to_conductor` (1818-1860). That text already names
  `question_register.py (--answer ... | --not-needed | --defer ...)`. Add `| --reword QID --question-file <file>` there, with the
  JSON keys. Then the conductor is told at the moment it matters (AR-10), conductor.md costs 0 bytes, and the cap and its carriers
  go back to 12 000. The function is FV1-3's, so this needs a Lead owns line.
- Option B, a cut inside conductor.md: the last sentence of line 64 ("A role is called only through the controller — ... in all
  three.") is 263 bytes. It restates table rows 31, 35 and 39. A case-insensitive grep finds no test pinning it (the positive
  control finds the same text in conductor.md).
- Option C, keep the raise: then every carrier moves.
- Carriers of the number:
  - `selftest.py:358` and its help text at `:20`
  - `test_conductor_investigates_first.py:231` and `test_conductor_doors.py:43` (moved), plus the comment at `:144`
  - `test_gate_words_road.py:391` and `test_person_words.py:673` (B1)
  - `references/README.md:7,50` and `design/README.md:12`
  - `plans/builder-rules.md:12`
  - `test_plan_contract_text.py:40` (comment "selftest.py REFERENCE_MD_MAX_BYTES")
  - per-file caps at 12000 for other files: `test_human_questions.py:108`, `test_gate_b_orders.py:566`,
    `test_grounding_schema.py:408`, `test_manual_observe.py:514`
  - `CHANGELOG.md:5766` is history, not a carrier.

**2. T6 and the nine choices.**
- Choice 9 is the literal spec condition (H1, H2, H5, H6, known `from`; H3 and H4 are not counted), so it is not a divergence.
  The defect is the other one, F1.
- 1: replaced in round 2. 2: ok. 3: fixed in round 2. 4: ok. 5: leaving out the T4 date is ok, but the T10 placeholders are F5.
  6: ok (callers check `top.strip()`, driver_gates 306-307). 7: ok (FR-41). 8: ok.
- New card lines pass `human_text.problems` (`fv19_human_text_passes`, as reported).

**3. H5: yes, one reader.**
- `gate_brief.requirement_help` is called by `still_open` and by `question_stop._with_note` (from `open_cards`, the only
  `_with_note` caller). Both read `contract.register_rows(planning_contract.story_register_text)`, cached once per pass. AR-13 and
  AR-15 are kept.
- Canon covers it: `test_fv19_stop_and_gate_cards_print_the_same_help` (`test_gate_question_form.py:1279`, keep row) goes through
  the real doors, `unanswered_questions` and `QS.open_cards`, with 5 rows including register-absent.
- The edit to `question_stop.py` breaks the spec's non-goal. It was made on the Lead's round-2 answer, and the quarantined
  `test_question_stop.py` was not touched.

**4. `notes` with no reader:** it does not block this merge, and a follow-up node is right. It is one class across three carriers
(P1) and must land before N3.

**5. Uncut texts: yes. Absent section: no.**
- Absent is wrong for a story whose register is present. It contradicts the spec's own §1.1 AR-23 ("no merge → the retro section
  says none"), §4 row 22 and the N5 DoD row ("none → the none line"). The builder met that row only through a direct call that
  `numbers` never makes.
- For the owner's B2 use (judge merges later through collect), a story with zero merges must be distinguishable from an old
  package or a missing reader.
- Uncut is right: whether two questions ask the same thing depends on how they differ, and a 200-character cut hides any
  difference past that point. The facts JSON is already whole (FR-49). Fixes: F3.

**6. Where the branches meet.**
- No two of N2, N4 and N5 touch the same file: changelog fragments and reports have distinct names. None of them edits
  `test-layers.json`, `judgment-census.json` or any ratchet fixture.
- N4 and N1 share `planning_contract.py` with disjoint functions, and N4 stands on N1.
- origin/main `eb6dd02..a3f9a49` touches none of the topic files (`git diff --stat` filtered on them: empty).
- Order: N1, then N2/N4/N5 in any order. No textual conflict is expected.
- The canon conflicts are B1 and B2.

**7. Judgment: none moved into code.**
- Whether two questions are the same is decided by the declaring role: the designer's `question_repeats` (told by T12 in N3, not
  built yet) or the conductor's CLI.
- The check on that decision is the case critic seeing `declared_by` (T13), plus the forge reading the retro and the collect
  afterwards (owner, F-9).
- Where it is written: spec §1.1 AR-2/AR-29, the `declare_repeat` docstring, and the census rows.
- What code compares:
  - ids, row hashes, chain resolution and dependants. `reason` id tokens go through `_id_token`, which is xref.
  - `reword`'s "nothing changed" is a whitespace-squeezed equality: bytes, not meaning.
  - `record_note` runs `human_text.problems(kind="report")`, the shape rows (census: shape).
- Census: 3 new rows (`declare_repeat` xref, `reword` xref, `record_note` shape), conductor 761 → 764, named in N1's DoD. N2, N4
  and N5 add no refusal units by reading. Their census run was not attached, so it is requested.

**8. Siblings: P3 and P4.** The card twins are fine:
- one `question_card` behind gate A and the stop;
- `still_open`, `is_open`, `check_open_questions` and `report_facts._questions` all call `hidden_repeat`;
- the MR section reads `still_open`.

## Standing questions

- **Fit:** as above. Every DoD row id is present (N1 has 22 `test_fv19_*` functions, as claimed; N2 has 14). The exceptions are
  F1, F2 and F3.
- **Seams:** N2 touched `question_stop.py`, `selftest.py` and two tests outside its owns (Lead round 2). The rest is additive.
- **DUPLICATION AND CONSISTENCY:** F4, F6, F7. Searched: the `role_words` grep in `scripts/*.py` (3 copies), and the entry checks
  side by side. `requirement_help` reuses `register_rows`/`story_register_text`, and `_origin_part` reuses `QR.origin_words`.
  `reading_origin_words` repeats `contract.READING_ORIGINS` as data; the junction is `fv19_origin_words_on_card`.
- **CODE QUALITY:** P7, F7.
- **AR-n:**
  - kept: AR-1, 13, 14, 16, 17, 20 (named), 23 except N5, 25, 28.
  - AR-22: P1.
  - AR-10: P2, and N3 is pending.
  - The `role == "conductor"` literal in `_may_reword` follows the spec (D4.4) and is not a list.
- **JUDGMENT:** none moved (Q7).
- **ONE ROAD:** rewording reaches exactly the roles whose forms are raised (F-11 = (a), Lead). The roles left out are those that
  have no raise carrier at all, so this is no exclusion from a shared mechanism. One residual: the skill road (P3). Searched:
  `question_register.py` in `skills/`.
- **Hygiene:** the N1 report shows no Cyrillic. The B1 caps are as above.

## Spot-checks

- Lead's "N2 selftest --limits 4/4 at d4f348a": consistent, since conductor.md is 12206 against a cap of 12206.
- N4 report "notes has no reader": confirmed (P1 grep).
- N2 report "T6 printed for H3/H4-only cards": confirmed in `_help_lines` tail, which matches the spec condition.
- N5 "zero records → no key": confirmed in `numbers`, and it diverges from the spec (Q5).

## Trail

- Read: the brief; the spec, whole; the four reports; all four diffs in full for the product files.
- Test excerpts read: `test_gate_question_form.py` 1086-1430, `test_retro_numbers.py` (the N5 row), `test_gate_brief_and_retro.py`
  2040-2075, `test_d1_answer_card.py` 105-115.
- Product code read: `conductor.md`, whole; `selftest.py` 14-22 and 380-410; `driver_dispatch.py` 1815-1870 and 2712-2740;
  `driver_stage_plan.py` 640-651 and 755-775; `contract.py` 625-663; `report_facts.py` 2399-2412;
  `branch_accounting.py` 1310-1322; `planning_contract.py` 3536-3550.
- Other files: `SIBLING_MAP.md` axis 5; the `critic_verdict.schema.json` schema.
- Greps: the `12000|12 000|12_000` carriers; `READING_ORIGINS`; `settled(` readers; `role_words`; `question_register` in
  `skills/` and in `conductor-actions.json`; and the P1 grep with its control.
- Measured: `wc -c references/*.md` gives conductor.md 12206, controller-api.md 11998, manual-evidence.md 11987. Line bytes:
  conductor.md:38 = 309, line 64 tail = 263.
- Re-run attempted: `test_judgment_census.py` on N2/N4/N5. The environment's auto-mode classifier refused it, so no control
  re-run was made. The Lead's re-runs (N4 120/120, N2 limits 4/4) are taken as attached.
- Request: attach `test_judgment_census.py` output at d4f348a, 672786c and 859b766.

```json
{"verdict": "fit_with_fixes", "blockers": ["B1 N2: conductor.md 12206 bytes fails canon checks test_gate_words_road.py:391 (raw <=12000) and test_person_words.py:673 (content_bytes <=12000); move T11 to driver_dispatch.register_words_to_conductor and revert the cap, or move every carrier with the owner's word", "B2 N2: test_gate_brief_and_retro.py:2061,2065 expect (from AC3)/(from spec); _origin_part now prints (from: AC3)/(from: spec); update the fixture in this round"], "fixes": ["F1 gate_brief._help_lines tail: T6 contradicts a card showing (from: x); count any non-blank from as recorded; no-readings wording; update test_fv19_card_no_help_line", "F2 gate_preflight.check_open_questions on_card: use gate A's list (still_open) not is_open; deferred and with_designer rows have cards at gate A", "F3 retro_numbers.numbers + QR.repeat_records present: none line when the register is present, key absent only with no register; texts uncut if the Lead confirms (amend T16)", "F4 one QR helper for reword entries shared by _reword_plan_entries and rewords_for_case", "F5 conductor_text T10: controller.py --operation rework form and self.task instead of <T>", "F6 retro_numbers role words: reuse driver_dialog.role_words or story_progress._role_words survivor, or queue", "F7 question_register: drop _one_line duplicate of _squeeze"], "class_completeness": "Card twins covered (one question_card; hidden_repeat read by still_open, is_open, check_open_questions, report_facts._questions; requirement_help one reader for stop and gate A). Missed: AR-22 refusal lines of all three carriers have no reader (P1, before N3); conductor --repeat door untold (P2); skill road phases s2.md/s4.md lack note/reword doors (P3, axis 5); report_facts.question_count counts hidden repeats (P4).", "trail": {"read": ["docs/tasks/critic-diff-brief.md", "docs/tasks/specs/20261114-fv1-9-question-repeats-spec.md", "four builder reports", "diffs eb6dd02..148c057, 148c057..d4f348a, 148c057..672786c, 148c057..859b766", "references/conductor.md", "scripts/selftest.py 14-22,380-410", "scripts/driver_dispatch.py 1815-1870,2712-2740", "scripts/driver_stage_plan.py 640-651,755-775", "scripts/contract.py 625-663", "scripts/report_facts.py 2399-2412", "tests/test_gate_question_form.py 1086-1430", "tests/test_gate_brief_and_retro.py 2040-2075", "tests/test_gate_words_road.py 380-391", "tests/test_person_words.py 660-673", "docs/SIBLING_MAP.md axis 5"], "reruns": [{"command": "wc -c references/*.md (fv1-9-n2)", "result": "conductor.md 12206, controller-api.md 11998, manual-evidence.md 11987"}, {"command": "python -B scripts/tests/test_judgment_census.py in n2/n4/n5", "result": "not run: refused by the auto-mode classifier; requested from the Lead as mechanical layer"}]}}
```
