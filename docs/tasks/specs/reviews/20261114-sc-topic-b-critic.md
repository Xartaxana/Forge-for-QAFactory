# Topic critic t-852 — stage-critics Part B (B1 `wip/sc-b1` 104b122a, B2 `wip/sc-b2` 3a183eff, B3 `wip/sc-b3` 030ba406)

Spec: `docs/tasks/specs/20261113-stage-critics-s2-s3-removed-spec.md` Part B (B.1-B.5, nodes B1/B2/B3). Owner 14.11.2026: «доделываем».

## Verdict: GO WITH FIXES (NEEDS WORK). 3 fixes block a merge (F1 for B2, F2 for B3, F3 for B2); the rest are fix-before-merge in the same round or queued as marked.

What holds: B1 implements B2-1 exactly. There is one reader, `runtime_policy.repair_cap`, at all four sites. S4/S5 stay byte-identical, a malformed row is ignored and a person's words lift the cap. B2 implements B2-2..B2-4: every seam call in `consumer_completion`/`consumer_settled` is replaced, the record is written before the warning, `GAP_PREFIX` has one home, and the close-words branch comes after `BY_PERSON`. B3 carries the B.3 texts word for word. The defects below are mostly SPEC defects that the builders carried faithfully (F1, F4, F7) plus two invariant holes (F3, F5).

## Findings and fix list (builder-executable)

**F1 [BLOCKS B2 merge; surface: the gate B packet] The S7 gap never reaches the person.** B2-5(b) and the changelog say the S7 warning "reaches gate B's packet (`gate_brief.py:2362`)". But `:2362` is inside `collect()`, the gate A data, rendered by `_tail_sections` `:3331-3356` (called from the gate A render at `:4044`). `render_gate_b` (`:5030-5160`, read through) never reads `pipeline["warnings"]`. The only readers of `pipeline["warnings"]` outside tests are `brief_pack.py:1831`, `gate_brief.py:2362` and `stage_done.py:178/190` (grep `\.get\(.warnings.\)|\[.warnings.\]` over `scripts/*.py`, positive control: it finds `gate_brief.py:3351`). So on the unreadable / form-refused / uncounted / rework-refused S7 paths, which happen after the scribe's brief, the gap ends up only in `pipeline.json` and in the driver's close words. Before B2 those paths put a question to the conductor or person. After B2 they are silent, which breaks AR-27. Row G6c (`gate_brief.collect(...)["warnings"]`) tests the wrong surface and cannot fail on this defect.
Fix (a new node "B2g", the Lead opens it; `gate_brief.py` is in no B node's owns): extract the warnings block of `_tail_sections` (`:3351-3356`) into `_warning_lines(warnings) -> list`. Have `render_gate_b` call it on the warnings `collect` reads (the same `_proved_warnings`/`_not_established` pass as `:2362-2364`, one reader). Use no text filter (FR-12). Position: before `filing_line`. Test row: G6c re-pointed to `render_gate_b("QA-9", packet)`, which contains `S7 was accepted with a gap`. It fails today. The Lead corrects the B.1 fact at line 438-439 and B2-5(b). The `changelog.d/consumer-one-round-no-barrier.md` "or gate B's packet (S7)" becomes true only with this fix.

**F2 [BLOCKS B3 merge; mechanical] B3 conflicts with main.** `git merge-tree origin/main wip/sc-b3` gives a CONFLICT in `references/role-load.json`. B3 measured on base 97ba4900 (analyst 18426→18485, scribe 17944→18014). Main now has 22442/20204 and 20420/18992. Fix: rebase on origin/main, re-run `role_load.py --all --json` on the merged tree, write the measured values (never B3's stale numbers), and restate the AR-20 raise line row by row. Witness: `test_role_load.py`, `test_role_rules.py`.

**F3 [BLOCKS B2 merge; surface: the gap writer] E-B8 holds only on the settle road.** `consumer_settled` checks `consumer_person_pass` before counting. `consumer_completion` does not: on a reject with no round, or an unreadable word, or a refused form, it calls `consumer_gap` straight away. A live stage-acceptance waiver given before the verdict is then buried under a later `gap:` record. `stage_acceptance` reads the LAST round (`acceptance.py:1313-1318`), so `consumer_close_words` reports "accepted with a gap" over a person's word. That breaks the INVARIANT "a person's word is never overwritten by a gap". G8 tests the settle road only. Fix in `driver_stage_s6.consumer_gap`, one place for all six callers: after resolving `author`, `if self.consumer_person_pass(stage, author): print(f"{stage}: a person's word passes it; no gap"); return False`. Test row G8b: the finish road, counted (1,1), `consumer_person_pass` gives True. Expect no `gap:` record, no warning, `own()` returned.

**F4 [fix before merge; Lead decides, a spec delta] The form-refused catch is wider than the form.** `stage_acceptance_write` (`driver_stage_plan.py:617-640`) raises the same `Refusal` for `question_register.py --raise` (the consumer's `questions[]`; its docstring says "so no question is lost in silence") as for `stage_done --acceptance`. With the catch in `consumer_completion`, a consumer's questions to the person become a 200-character fragment of a gap quote. For S6 they then land under "Factory defects - nothing is wanted from you". Fix: tag the question step in `stage_acceptance_write` (`exc.step = "questions"`, attribute only, S4 behaviour unchanged; add it to B2's owns). In `consumer_completion`, re-raise a tagged refusal and take the gap road only for the acceptance write. Test row G4c: a refused question raise → `Refusal` propagates, no gap record.

**F5 [fix before merge, B2; P31 one road] Q2.** The same event, the consumer's form refused by the writer, takes the gap road in `consumer_completion` and the conductor road in `consumer_settled` (`:436`, the M2 recovery where the finish died). Fix: one helper `consumer_form_write(stage, dispatch) -> str` (`""` = written, else the `why`) used by both, with F4's narrowing. It also removes the duplicated refusal flattening. Test row: G4 "settled form-refused" → gap, True.

**F6 [fix before merge, B2; duplication inside the diff] The `why` choice is copied twice.** The two-line "spent vs could not be counted" conditional appears in `consumer_completion` and in `consumer_settled`; the builder named it. Fix: `consumer_no_round_why(stage, counted, cap) -> str`. No new row.

**F7 [fix before merge, B3 text + B2 round line] Two role texts promise what nothing delivers.** (a) The round line tells the S6 analyst to "name what you could not use as a gap in your form's `unresolved` (the report shows it as a factory defect)". No reader of the analyst's form `unresolved` into the report turned up (grep `get\(.unresolved.\)` over `scripts/*.py`: the readers are controller, acceptance, contract and driver_stage_s7 manifest checks; none feeds `brief_pack`/`report_facts`). The scribe's new Tools line covers only its own gap and the `standing:` lines. Fix in `qa-doc-scribe.md`, on the Tools line B3 added: "...; an `unresolved` item of the analyst's form naming what it could not use from the run goes there too". (b) The scribe's narrowed technique says "one of the returns item 5 lists". The scribe's item 5 lists three returns, and the two merge returns live under "Where bugs hide" (`A merge the cause does not explain`), so the line forbids returns the charter allows elsewhere. Fix: "...one of the returns item 5 or «A merge the cause does not explain» names". Update the B3 DoD keys; run `test_role_rules.py`/`test_role_load.py`.

**F8 [fix before merge, B1] No changelog fragment.** B1 changes project-visible behaviour: the S6/S7 cap goes 2→1, set by `stages.json` `acceptance_rounds`, a project's `limits.repair_cycles` no longer lifts it, and a person's words do. Fix: `changelog.d/consumer-round-cap-is-data.md`.

**F9 [queue, low] The brief-time read can file a false defect row.** `consumer_round_line` reads the count at BRIEF time through `budget_or_none`. When the count cannot be read, that files a `defect_found` row "the window was closed with no repair round", which is false at brief time, and `_budget_unknown` then dedups the true verdict-time row. Fix later: a quiet read for the advice line.

## Answers 1-6

1. **`ReworkRefused` only: right.** `Driver.rework` (`driver_dispatch.py:2847-2896`) raises `ReworkRefused` only before any role runs (the controller refusal at `:2877`, no id at `:2880`). Its class docstring (`driver_core.py:189-193`) requires that a plain `Refusal` from the author's own run keep going to `guarded`. Catching any `Refusal` would write a gap after a round actually ran. Recommendation: keep it; the Lead rewords F-4 to "`ReworkRefused` (a `Refusal`)".
2. **Yes, with F4's narrowing.** See F5 (P31).
3. **No dry-run guard.** `story_run --dry-run` returns `driver.describe()` (`story_run.py:172-173`). `consumer_completion`/`consumer_settled` are reached only from `stage_S7`/`stage_S8` under `run()`. `person_pass` has its guard because `consumer_person_pass` is reached from the answer road (`driver_machine.py:2262`). The siblings on the same road (`stage_acceptance_write`, `rework`) have no guard either. A guard would be dead code. Recommendation: none.
4. **Fix, don't accept.** See F1. The owner is a new node B2g owning `gate_brief.py` (`_tail_sections` warnings block, `render_gate_b`), merged in the same wave as B2 or before it.
5. **Merge order B1 → B2 → B3 in one wave, no release between them.** Trial merges: main+B1 clean, main+B2 clean, main+B3 conflicts (F2). B1 and B2 conflict with each other in `test_story_run_s6.py` in both orders: both insert after `hf2_11b_forty_tests_changed_by_one_fixture` and edit the same `run_scenarios` line. Resolve by keeping both functions and both registrations. Why B1 first: B2 alone (cap 2) renders "Your return is the one chance ... (0 of 2 used)", which contradicts itself (FR-10). B.5's "either alone is safe" holds for state, not for this text. B1's own CI run 43525134738 ran on the BASE sha a9d69a5c (B1 report), so neither C1-C6 nor G1-G10 has been judged by CI. The batch canon after convergence must read `test_story_run_s6.py`, `test_driver_layers.py`, `test_judgment_census.py` (B2 left the census ratchet unedited, so CI decides) and A27. Process note for calibration: B1's builder launched CI itself (PROJECT.md «Командная работа» п. 13).
6. **Class completeness.** `stage_review_exhausted(` callers on B2, outside tests: only `driver_stage_plan.py` (`:805,812,819,825,843,853,1001,1005`, all S4). `consumer_exhausted` (case-insensitive over `ai-packages/`) survives only in the QUARANTINED `test_stage_acceptance_consumer.py:373` `Rig.BOUND`. Its `getattr(SR.Driver, name)` will now raise AttributeError at Rig construction, so the file errors as a whole. It is not editable (non-goal); the Lead should tell quarantine-watch readers. Siblings by design: the S5 window line (`story_progress.py`), the S7 re-judge limit, R1 (queued in the spec). The real sibling surface is gate B (F1). SIBLING_MAP has no consumer-acceptance axis; the row "One question for every stop" (A27) is not raised, because `consumer_gap`'s `self.py(..., check=True)` is exempt (`audit_factory.py:2169`).

## Standing questions

- **Fit to spec:** B1 fit. B2 fit except F1 (a spec fact), F3 (an invariant missed on one road) and F4 (a spec scope). B3 fit except F2 (stale base) and F7 (spec text).
- **DUPLICATION AND CONSISTENCY:** (i) F6, inside the diff. (ii) `consumer_gap`'s `stage_done --acceptance ... --acceptor driver --verdict accept --quote` is a second copy of `person_pass`'s call (`driver_stage_s6.py` person_pass). Queue: one `driver_accept_write(stage, author, quote, expect)`; `person_pass` was a non-goal. (iii) The refusal-flattening idiom `" ".join(str(getattr(x,"text","") or x).split())` now has 5 copies in `driver_*.py` (grep). Queue: one helper in `driver_core`. (iv) B1: none found. Grep `design_repair_cycles" if` over `scripts/*.py` minus tests on the merged main+B1 tree prints only `runtime_policy.py:84`; control on origin/main prints the four sites. (v) B3: none, text only.
- **CODE QUALITY:** no new function over 60 lines and no nesting deeper than three levels. `consumer_completion.complete` is about 25 lines. The test uses `(_ for _ in ()).throw(...)` inside a lambda to raise: it reads badly, so use a named function (queue). No dead branches. `consumer_gap` returns False/True and its callers ignore the value: consistent with spec step 1 (`own()` either way).
- **Tests and volume:** B2 has +121 test lines against about +90 product lines, with the reason given. But the G rows are one receipt per spec edge (the spec asked for them) over stubs of `consumer_counts`, `rework`, `py` and `stage_acceptance_write`. That is the stub class the quarantined Rig header warns "hid B1 and B2". G6c has no killing power (F1). The new rows F1/F3/F4/F5 come from defects and are legitimate (TESTING.md «Новый случай приходит из дефекта»). B1's C rows are a pure table on one reader, acceptable as the DoD asked.
- **Ratchets (axis 18):** B3 raises `role-load.json` `ratchet_tokens`/`process_ratchet_tokens` for analyst and scribe, to be re-measured and named after F2. B2 adds a `driver-layers.json` const row `GAP_PREFIX` (row 19, not an upward edge) and makes no census change, which CI confirms or rejects. B1 has none.
- **ARCHITECTURE:** AR-1/AR-13 kept (B1). AR-13 kept (`GAP_PREFIX`). AR-17 kept (no S6/S7 seam). AR-28 kept (unknown count → gap). AR-27 broken for S7 (F1). AR-24/FR-8 at risk (F4).
- **JUDGMENT:** none moved into code. No census row was added; `judgment: none` is true.
- **ONE ROAD:** S4 keeps the seam while S6/S7 take the gap. That difference stands on the owner's word quoted in the spec (line 405, 13.11.2026) and F1 «всё верно» (B.2), plus a data row (`acceptance_rounds`). Not a finding. F5 is the one-road residual, fixed in this round.

## Trail

Read: spec lines 405-564 and 770-864; `git diff origin/main...wip/sc-b{1,2,3}` in full; B2 report `docs/tasks/handoffs/20261114-sc-b2-report.md`; B1 report (untracked) `.claude/worktrees/sc-b1/docs/tasks/specs/reports/20261114-sc-b1-report.md`; B3 report (on branch) `docs/tasks/specs/reports/20261114-sc-b3-report.md`; `driver_stage_s6.py` (B2) person_pass, consumer_person_pass, consumer_need_record, consumer_settled; `driver_dispatch.py:2847-2945` (rework, repair_budget, budget_or_none); `driver_core.py:185-200, 600-660`; `driver_runner.py:211-232` (py); `driver_stage_plan.py:617-640`; `acceptance.py:1286-1318, 1431-1451`; `gate_brief.py:2338-2398, 3331-3360, 4020-4046, 5030-5160`; `story_run.py:165-176`; `driver_machine.py:2240-2270, 4154-4200`; `controller.py:254-255, 3930-3950`, prepare `:2148`; `audit_factory.py` A27 lines; `docs/TESTING.md:1-70`; `docs/tasks/critic-diff-brief.md`; `docs/SIBLING_MAP.md` (grep).
Control re-runs (verbatim tails): B1 DoD reader in the sc-b1 worktree → `[1, 2, 2, 2]`; real rows `S6 1 S7 1 S5 2 S4 2 SS-S6 1 SS-none 2`. B2 worktree: `=== test_dispatch_identity: 114/114 ok ===`, `=== test_driver_stop_record: 255/255 ok ===` (both match the report). B3 worktree: `=== role rules: 57/57 ok ===`, `=== role_load (the one measure of a role's start load): 186/186 ok ===` (match). Trial merges: `git merge-tree --write-tree` main+B1 clean, main+B2 clean, main+B3 CONFLICT role-load.json, (main+B1)+B2 and (main+B2)+B1 CONFLICT test_story_run_s6.py.
Negatives verified: "no other caller of the consumer seam" (case-insensitive grep, control: `consumer_exhausted` on origin/main finds 4+1+1 hits); "render_gate_b reads no warnings" (read through `:5030-5160`, plus a reader grep with a positive control on `:3351`); "B1 leaves one cap site" (grep on the merged tree, control on main = 4 sites).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F1 gate_brief.render_gate_b shows no pipeline warnings: the S7 gap never reaches the person at gate B (B2-5(b) false, row G6c asserts collect, not the gate B text); new node B2g owning gate_brief.py",
    "F2 wip/sc-b3 conflicts with main in references/role-load.json; ratchets measured on stale base 97ba4900 must be re-measured on the merged tree",
    "F3 consumer_completion writes a gap over a standing person's pass (E-B8 checked only in consumer_settled); fix in consumer_gap"
  ],
  "fixes": [
    "F1 gate_brief.py: extract _warning_lines from _tail_sections, call it in render_gate_b on collect's warnings; row G6c re-pointed to render_gate_b",
    "F2 rebase wip/sc-b3, re-measure role_load on merged tree, restate AR-20 raise",
    "F3 driver_stage_s6.consumer_gap: consumer_person_pass(stage, author) True -> no gap, return False; row G8b on the finish road",
    "F4 stage_acceptance_write tags the question_register refusal; consumer_completion re-raises it, gap only for the acceptance write; row G4c (Lead decides the spec delta)",
    "F5 consumer_settled stage_acceptance_write refusal takes the gap road via one helper consumer_form_write shared with consumer_completion; row G4 settled",
    "F6 one helper consumer_no_round_why replaces the two copies of the spent/uncounted conditional",
    "F7 qa-doc-scribe.md: Tools line carries the analyst's unresolved gap; technique names item 5 and the merge returns; update B3 keys",
    "F8 changelog fragment for B1 (cap 2 to 1 by acceptance_rounds; project limits do not lift it; a person's words do)",
    "F9 queue: consumer_round_line brief-time read must not file the window-closed defect row"
  ],
  "class_completeness": "stage_review_exhausted callers outside tests are S4 only (driver_stage_plan.py, 8 sites); consumer_exhausted remains only in quarantined test_stage_acceptance_consumer.py Rig.BOUND (now errors at init, not editable); sibling surface gate B packet uncovered (F1, new node); completion vs settled asymmetry (F5) fixed this round; S5 window line, S7 re-judge, R1 by design/queued in spec; duplication queues: driver_accept_write, refusal-flatten helper",
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-stage-critics-s2-s3-removed-spec.md:405-564,770-864",
      "git diff origin/main...wip/sc-b1, wip/sc-b2, wip/sc-b3",
      "docs/tasks/handoffs/20261114-sc-b2-report.md",
      ".claude/worktrees/sc-b1/docs/tasks/specs/reports/20261114-sc-b1-report.md",
      "wip/sc-b3:docs/tasks/specs/reports/20261114-sc-b3-report.md",
      "ai-packages/qa-factory/scripts/driver_stage_s6.py (wip/sc-b2)",
      "ai-packages/qa-factory/scripts/driver_dispatch.py:2847-2945",
      "ai-packages/qa-factory/scripts/driver_core.py:185-200,600-660",
      "ai-packages/qa-factory/scripts/driver_runner.py:211-232",
      "ai-packages/qa-factory/scripts/driver_stage_plan.py:617-640",
      "ai-packages/qa-factory/scripts/acceptance.py:1286-1318,1431-1451",
      "ai-packages/qa-factory/scripts/gate_brief.py:2338-2398,3331-3360,4020-4046,5030-5160",
      "ai-packages/qa-factory/scripts/story_run.py:165-176",
      "ai-packages/qa-factory/scripts/driver_machine.py:2240-2270,4154-4200",
      "docs/TESTING.md:1-70",
      "docs/tasks/critic-diff-brief.md"
    ],
    "reruns": [
      {"command": "python -B -c repair_cap DoD reader (sc-b1 worktree)", "result": "[1, 2, 2, 2]; S6 1 S7 1 S5 2 S4 2 SS-S6 1 SS-none 2"},
      {"command": "python -B test_dispatch_identity.py (sc-b2 worktree)", "result": "=== test_dispatch_identity: 114/114 ok ==="},
      {"command": "python -B test_driver_stop_record.py (sc-b2 worktree)", "result": "=== test_driver_stop_record: 255/255 ok ==="},
      {"command": "python -B test_role_rules.py (sc-b3 worktree)", "result": "=== role rules: 57/57 ok ==="},
      {"command": "python -B test_role_load.py (sc-b3 worktree)", "result": "=== role_load (the one measure of a role's start load): 186/186 ok ==="},
      {"command": "git merge-tree --write-tree origin/main wip/sc-b1|b2|b3 and pairwise", "result": "b1 clean, b2 clean, b3 CONFLICT role-load.json; b1+b2 either order CONFLICT test_story_run_s6.py"},
      {"command": "git grep 'design_repair_cycles\" if' on merged main+b1 tree vs origin/main", "result": "runtime_policy.py:84 only; main: 4 sites"}
    ]
  }
}
```
