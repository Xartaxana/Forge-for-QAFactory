# t-240 — critic diff review, HF8-4 topic (one pass, R13-g): P7, P8+P10, P9, P11, P1

Reviewer: critic (Opus). Spec: `docs/tasks/specs/t-205-hf8-4-parts.md` §1-§8. Plan review: `t-213-t-205-plan-review.md`.
Rules: `docs/tasks/critic-diff-brief.md`. Branch heads reviewed: P7 `77a1d50`, P8+P10 `8d3350f` (`8d12aac` P8, `8d3350f` P10),
P9 `0ce7208`, P11 `6bc60b1` (`c20697c` + `6bc60b1`), P1 `3910f15` (work commit `3149828`, merge of main `3910f15`).
Note: the repo root holds an untracked directory `origin/`, so a bare `origin/main` is ambiguous to git. I used `refs/remotes/origin/...`.

This file is my input to acceptance. The decision to accept belongs to the coordinator of the proper tier.

## Verdict per part

| part | verdict | in one line |
|---|---|---|
| P1 | **ACCEPT** | One home in `contract.py`. The split of `red_by_requirement` keeps behaviour, `refused` invariant included (traced below) |
| P7 | **ACCEPT WITH FIXES** (1 fix, does not block the merge) | Behaviour kept. `_reopened` computes the `again_in_words` predicate a second time |
| P8 | **ACCEPT** | One builder. The bytes are identical. Axis 26 now matches the code |
| P9 | **ACCEPT** | Both deviations accepted. The stated behaviour change is correct, and its direction is toward refusing |
| P10 | **ACCEPT** | `replace_file` is wired. The `_probe_cwd` unification has no effect on output, because `registered_probe` always sets `cwd` |
| P11 | **ACCEPT WITH FIXES** (1 fix, does not block the merge) | The text move and the 4 ratchets are right. The FR-33 row the spec owes is not written |

Overall: **fit_with_fixes**. Nothing blocks the merge. Two small fixes, plus Lead-side process items (section "Process").

## (1) Fit to the spec, edges, deviations

**P7** (`planning_contract.py`). The one `SETTLED_STATUSES` was deleted. The three uses read `QR.SETTLED_STATUSES`, and `QR` is lazily imported in both functions: `:2662` and `:3496`. `planning_contract` still has no load-time import of `question_register`. The DoD grep `SETTLED_STATUSES =` gives 0 hits here and 1 in `question_register.py`. Split, traced against the old body:
- `_reopened` gets the same `prior` (`intents[-1]`; the caller enters that branch only when `prior is not None`). It appends the same line to `lines`, and builds the same rework rows and the same record.
- `_publish_plan` is the old block, byte for byte. It runs once, before the records.
- `_note_applied` re-imports `QR` locally and is otherwise identical.
- `out["lines"]`/`out["rework"]` are still extended last. If `atomic_json` raises, `out` is untouched (invariant: a failed write reports nothing it did not do). The early return with no settled question is unchanged.
- Control rerun: `test_question_branches.py` gives 707/707.

- **Fix P7-1** (item 7, a copied block inside the diff; does not block the merge). `planning_contract.py:3569-3570` (branch `77a1d50`) derives `prior = intents[-1]` and `again_in_words = answer == "" and prior.get("answer") == ""` again. The caller already decided the branch with the same predicate at `:3546`. If someone later edits one copy and not the other, the line the person reads ("own words again" vs "your answer is now") would disagree with the branch that was taken. Expected change: `_reopened` takes `prior` and `again_in_words` as parameters from the caller and drops its own two derivations.
- The builder's note that `test_gate_preflight` timed out twice with no FAIL lines is accepted as the canon's to judge. It is a SLOW-class file, so CI judges it (builder-rules 7b).

**P8** (`waiver.stand_block`). The function body is the old f-string verbatim, placed after `OWN_FORM_BLOCKS`. Both callers call it, and both return before building the block when a stand is confirmed. An empty environment gives the "no stand" text. `split_overridden` sees the same string, so a recorded word still passes it. Positive control: `git grep "is not confirmed as usable"` on the branch finds only `waiver.py:380`.

Axis 26 rewrite: I checked every site it names on the branch:
- `waiver.py:373` (the constant) and `:378` (`stand_block`);
- `check_delivery.py:1574` `stand_word`;
- `driver_machine.py:3916` `_take_stand_answer`;
- `driver_stage_build.py:121` `site_seam_person(..., block=STAND_NOT_CONFIRMED_BLOCK)`;
- `story_run.py` holds none.

All are correct. The builder's note that the tail text is pinned by no test is not a finding: a missing pin is not a finding, per brief q.5.

**P10** (`execution_request.py`).
- `from event_store import replace_file` is at load. `event_store` imports only the stdlib (`event_store.py:6-16`), so there is no cycle.
- Both writes go through it. The grep `os\.replace(` gives 0 in `execution_request.py`. Positive control: 2 in `event_store.py`.
- `_observe_precedent` is the old branch moved verbatim. `now` is computed once in `_observe_stand`, and `MineRefusal`/`evidence_only` behave as before.
- `_probe_cwd`: the old second site was `Path(spec["cwd"])`; the new one reads `spec.get("cwd") or "."`. They are equivalent because `registered_probe` always returns `"cwd": str(spec.get("cwd") or ".")` (`execution_request.py` `registered_probe`, branch). So no input changes behaviour.
- Control rerun: `test_execution_request.py` gives 498/498.

**P9** (grammar / report_facts / validate_artifacts).
- All 11 `*_HEADING` constants are added, and each value equals the literal it replaces. The tuples and the 8 `REPORT_BLOCK_HEADINGS` values use them, in the same order.
- `LEGACY_SECTIONS` is built from `REPORT_BLOCK_HEADINGS`, with the same pairs and order.
- Every renderer the spec names now uses `G.REPORT_BLOCK_HEADINGS[...]`, with its suffix kept byte for byte.
- The finders at `:4350/:4485/:4604/:4720` use the constants. `SHOTS_HEADING` is added.
- `APPENDIX_HEADING` is deleted from `report_facts`. `appendix_span` and the public `appendix_body` are added, and their two callers are updated.
- No reader of the deleted names `RF.APPENDIX_HEADING`, `_appendix_body` or `REPORT_HUMAN_HEADING` remains in `ai-packages/` or `tools/` (git grep on the branch: 0 hits; positive control: the same grep finds `G.APPENDIX_HEADING`).
- `validate_artifacts` imports `report_facts` lazily, function by function.
- `is_legacy_report` stays a substring test, which is the AR-28 direction.
- `_authored_text` takes its offsets on `authored`. `check_report_traceability` keeps its early return.

I traced `_section_span` and `_headings`. A fenced or mid-line `## Appendix` is no section, so the forbidden-id check and the prose budget can only see more text. That is the refusing direction, as stated.

The DoD grep on the branch prints only the lines the spec lists as not applicable, `SHOTS_HEADING`, and the two `LEGACY_REPORT_SECTIONS` lines (deviation 1). Control rerun: `test_report_facts.py` gives 1276/1276. The builder's red-first count of 1274/1276 matches the two behaviour rows (fenced and mid-line).
- **Deviation 1 (accepted).** `validate_artifacts.py:1158/1160` keep `"## Verdict"`, `"## Run this yourself"`, `"## Product problems"` and `"## Our tests and the factory"`. Each has exactly one spelling in the package (git grep over `scripts/*.py`, `references/` and `templates/`, tests excluded: only `:1158`/`:1160`), so the tuple is their home, like `UNDERSTANDING_SECTIONS`. The two shared headings in that tuple were converted to `PTR_*` as the spec asked. The gap is the spec's: its not-applicable list omitted these lines.
- **Deviation 2 (accepted; the spec was wrong).** For the red-first row, the forbidden id must stand AFTER the fenced or mid-line mention. The old `text.find` cut the body at the first mention, so only text BELOW it was hidden. An id "above" the mention would have been visible before and after the change, and the row could not be red first. The builder's order is the one that kills the defect.

**P11.**
- The list moved verbatim, in the wording the spec gave, into `artifact-contract-automation.md` and both regenerated slices. The slice index byte counts are regenerated.
- Rubric dimension 8 now points to the contract. Dimension 6's "dimension-8 sanctioned path" is kept, as the spec required (`no-commented-out-checks` anchor).
- The automator charter pointer is changed. The three anchors of the `role-rules.json` row are moved, and each stands in its carrier on the branch.
- The critic's own slice carries the list (`slices/qa-code-critic/artifact-contract-automation.md:68`), so the stop condition did not apply.
- No "rubric dimension 8" pointer is left in the automator's files. The remaining hits are `qa-case-critic.md:52` and `judgments.json:275`, which belong to the case critic and are out of scope per the spec.
- **Fix P11-1** (spec edge, FR-33; does not block the merge, but must be done before the batch closes). The spec's edge says: "The part adds that row to its batch's 'Живые доказательства'". The table in `plans/piles/onboarding-forge/batch-2-onboarding-roles-forge-p3.md` is empty on `origin/main`, on `origin/pile/onboarding-forge/batch-2` and on every HF8-4 branch. Expected change: one row of the form "P11: the automator follows the contract's sanctioned paths (rubric dim 8 pointer) | MyBooks | — | ожидает", which moves to `live-runs` at close per PROJECT.md «Командная работа» p.9. This is a Lead/integrator edit of a taken batch (the table is writable), not a package edit.
- **Owns note** (not a blocker). Commit `6bc60b1` edits `scripts/tests/test_walk_plan_fields.py`, which is outside P11's `owns:`. The edit was needed: `role_load_raise_named` pins every role's measured ratchet, and without it the test goes red. The dispatcher did not foresee that the pin repeats `role-load.json`. That pin is a pin on a measured constant (TESTING.md «не пишется»), and it forces every future ratchet move to edit two files. Proposed: queue it as a finding against the test (owner: the Lead; I propose, the Lead opens the node).

**P1** (asked (a) and (b)).
- `contract.CONTRADICTS_REQUIREMENT` is defined before `UNRESOLVED_REASONS`. `_red_thens_of` and `PROBE_NOT_APPLICABLE_REASON` use it, and the acceptance alias stays.
- DoD grep on the branch: `contract.py` has one quoted literal (`:84`), `acceptance.py` has none.
- The 10 remaining literals equal the builder's list and the spec's P2-P6 list exactly.
- The merge `3910f15` leaves both owned files untouched (`git diff --stat 3149828 3910f15 -- contract.py acceptance.py` is empty).
- (a) **The split keeps behaviour.**
  - `_red_source` rebinds its own `runs` before the closure is called. The closure reads `runs` and `current` from `_red_source`'s scope.
  - `red_by_requirement` uses the outer `runs` only to pass it in (the uses in the function body are `:46-48` of the function), so not rebinding the outer name changes nothing.
  - The early `return {}` on unreadable runs happens at the same point: after the manifest checks, before the loop.
  - `_rows_for_instance` is the loop body moved verbatim. It returns `(matched, turned_down)` in manifest order, keeping every matching row (N1).
  - The `refused` branch is unchanged. Same condition (`not matched and turned_down and refused is not None and report is None and strict and failed(names)`), the first turned-down row only, one per instance. So a green or unrun sibling gets no refusal.
  - Each helper's docstring names the error direction "not red".
  - Control rerun: `test_red_window.py` gives 196/196.
- (b) **Stacking wave 2 on `wip/hf84-p1` is safe from the code side.** I request no change to `contract.py`/`acceptance.py`, so no fix round will move the base under P2/P3/P6. `origin/wip/hf84-p2`, `-p3` and `-p6` already have `3910f15` as an ancestor (`merge-base --is-ancestor`: all three are stacked). Conditions:
  1. P1 merges to the batch branch first, or together with them.
  2. P1 had no witness rerun after merging main (163 files came in). The wave-2 witnesses exercise `contract.py` again, and the batch canon on CI is the judge. A red result there that points at P1 is a `defect_found` against t-228.
  3. The start gate of §3 (M5) is not closed on `main`; see Process. That is a Lead record, not a code risk today: `wip/of-batch4` does not touch `contract.py` or `acceptance.py` (diff from its merge base `539361a` is empty for both files).
- Observation, queue-level: `acceptance.py:830/834/838/843/846` (`_red_refusal`) spell the word inside refusal sentences ("`{case}'s contradicts_requirement row names ...`"). P4 converts the analogous reason text at `driver_stage_s7.py:45` to `CONTRADICTS_REQUIREMENT + " rows"`. One road (P31) would put both under the same rule. This is outside P1's DoD grep, which only counts quoted literals. Proposed: append it to node OF5-2 (one home of the outcome words) rather than reopen P1.

## (2) Ratchets (AR-20, axis 18, brief q.9)

| key | old → new | reason | named in commit / changelog |
|---|---|---|---|
| `ratchet_tokens.qa-automator` | 20181 → 20257 (+76) | the list is now in the automator's slice | yes / yes |
| `process_ratchet_tokens.qa-automator` | 18614 → 18690 (+76) | same, process share | yes / yes |
| `ratchet_tokens.qa-code-critic` | 19389 → 19420 (+31) | the slice grows by the list, the rubric shrinks by a pointer | yes / yes |
| `process_ratchet_tokens.qa-code-critic` | 17566 → 17597 (+31) | same | yes / yes |

Verdict on the ratchets:
- **Justified:** the moved list is the decided F2 (d). The raise is the Lead's act named here, not the owner's.
- **Minimal:** +76 is about the ~290 bytes of the list, and the critic's +31 is net of the pointer.
- **Equal to measurement:** my rerun of `role_load.py --all` on the P11 tree gives automator 20,257 / 18,690 and critic 19,420 / 17,597, each equal to its row. Both are under the 200-token stop.

Nothing else moves silently:
- No branch touches `judgment-census.json`, `tools/dup-baseline.json`, `env-facts-baseline.json`, `driver-layers.json` or `NO_MOVE_BASELINE` (diff --stat of all five branches).
- The `role-load.json` diff is exactly the four rows.
- In `test_walk_plan_fields.py`, only the same four values move.

## (3) Duplication and quality (brief items 6-7)

DUPLICATION AND CONSISTENCY:
- **P7:** one twin predicate inside the diff (Fix P7-1).
- **P8:** no second builder (positive control above).
- **P9:** no heading spelled twice in its three files. The DoD grep shows only homes. I ran a wider grep for the 15 report heading words inside any `"...## X"` string in `report_facts.py`/`validate_artifacts.py`, and it hits only docstrings.
- **P10:** no other `os.replace` in the file.
- **P1:** no literal is left in its own files.
- **P11:** one home of the list. The two slices are generated copies.

The deterministic clone/lint ratchet result belongs to the branch `forge-check` job, which I did not see in this dispatch. The coordinator reads it at integration.

CODE QUALITY:
- New functions are all under 60 lines: `_observe_precedent` about 46, `_rows_for_instance` about 25, `_red_source` about 35, `_reopened` about 20.
- `red_by_requirement` shrinks to about 69 lines; most of it is docstring.
- No dead branch. No lying name: the `stand_block` docstring names both callers correctly.
- `waiver.py:380` is a 165-character line. The package has no line cap (`awk 'length>150'` counts 896 such lines across `scripts/*.py`), so this is not a finding.

## (4) Class completeness vs docs/SIBLING_MAP.md

**Covered:**
- Axis 26: P8 rewrite, every site verified.
- Axis 18: the P11 rows, named.
- The F1 word: P1 done; P2-P6 stacked, with exactly 10 literals left (git grep on the P1 branch matches the spec list).
- The P9 headings inside its own files.
- Axes 32 and 34: no check changes class; no language, project or case exclusion.
- A case-insensitive grep of SIBLING_MAP for `appendix|REPORT_SECTIONS|SETTLED_STATUSES|replace_file|os.replace|contradicts_requirement|sanctioned|_section_span` gives no axis besides 26 that these parts must touch. Positive control: the same grep hits line 190.

**Queued:**
- F3 → `package-ci` PC3-3 (`batch-3-khrapovik-doors-only.md:27`) plus a finding file and a card row.
- F5 → `onboarding-forge` OF5-1, F7 → OF5-2 (`batch-5-ostatki-hf8-4-i-oh3-42.md`), plus finding files and card rows.
- F6 → `report-delivery` RD2-4 (`batch-2-stroki-otcheta.md:28`) plus a finding file and a card row.

All of these are in commit `0106ff9` on `origin/main`, as the coordinator said.

**Missed (not queued; each is a line the Lead writes — I propose, the Lead's tier decides):**
- M-1: **F4.** The six grown long functions (`build_mine_request`, `manifest_from_tests.build`, `window_record.build`, `ledger.plan_row_state`, `acceptance.validate_window`, `driver_stage_s6.stage_S6`) are owed as `перенос:` lines in batch-2 «Остатки» (spec §3, §5 F4). batch-2 «Остатки» on `main` and on the batch branch holds only the 01.11 line.
- M-2: **The stand-word reader twin.** P8's non-goal is "the duplicated confirmed-and-passed-by-word loop of `s6_no_stand` and `stand_check`". It has a third member: `check_delivery.stand_word`, which reads `split_overridden([STAND_NOT_CONFIRMED_BLOCK], ...)` over `STAND_WORD_STAGES` (`check_delivery.py:1571-1581`). The drivers read `split_overridden([stand_block(env)], ...)` over `STAND_STAGES` (`driver_stage_build.py:24`). So there are two stage tuples and two match strings for one question: "is the stand word given?" (AR-13). There is no node or finding for it (git grep for `s6_no_stand` under `plans/`: 0 hits; positive control: the same grep over `docs/tasks/specs/t-205-hf8-4-parts.md` hits `:402`). Whether the two match strings can disagree on one recorded word (`names_whole(match, error)`, where a word that names the full text would not name the bare block) is not verified here. That is the node's first step. Proposed: a node in `onboarding-forge` batch-5 or a finding, owner the Lead.
- M-3: **Report headings as a new symmetry.** After P9, the report headings form a symmetry with one home in `grammar`, renderers in `report_facts`, and finders in `validate_artifacts`/`traceability`. Rule 9 calls for an axis when a new symmetry appears. This does not block: the reader half is RD2-4, and the axis can land with P5 or RD2-4. Proposed: name it in RD2-4.

## (5) AR-n and P27

- AR-13: P1, P7, P8, P9 and P10 each leave one reader or home, checked by the greps above.
- AR-15: survivors are `contract`, `QR`, `waiver.stand_block`, `grammar`/`report_facts.appendix_span`, `event_store.replace_file`, and the contract list.
- AR-14: `report_facts` writes the appendix and owns `appendix_span`; `validate_artifacts` only reads through it.
- AR-28: the `is_legacy_report` substring test is kept, and the appendix change only refuses more.
- AR-20: section (2).

Every package commit carries `architecture:` and `judgment:` lines. P27/AR-29: no new check, no census row added or reclassified, and no `blocks_override`, scan-constant or `kind: craft` edit. P11's text is testing craft (which masking is legitimate), judged by the code critic. **None found:** no check judges meaning.

## (6) Merge-ability (`git merge-tree --write-tree`)

- **Pairwise** among `main`, `p1`, `p7`, `p8p10`, `p9` and `p11` (15 pairs): every one rc=0, no conflicts.
- **Chained** onto `refs/remotes/origin/main` (p1 → p7 → p8p10 → p9 → p11): all rc=0.
- **Chained** onto `refs/remotes/origin/pile/onboarding-forge/batch-2`: all rc=0.
- **Against `wip/of-batch4`:** p1, p7, p9 and p11 conflict only in `plans/PILES.md` and/or `plans/piles/onboarding-hooks/batch-5-nerazlozhennye-nakhodki.md`, which is main drift in pile files and no package file. p8p10 is clean.

## Process (Lead tier; not part verdicts)

- PR-1: §3 "Zone records" 1 is not done. The owned-file list of P1-P11 is not in batch-2 «Ход» on `main`, on the batch branch, or on `wip/of-batch4`. Also, HF8-4's row status is still `ожидает` on `main` while P1, P7, P8, P9, P10 and P11 have been handed in (CLAUDE.md 4a).
- PR-2: §3 "Zone records" 2 / F8. The `contract.py` queue line is not on `main`. `wip/of-batch4` and `pile/onboarding-forge/batch-4` carry `очередь: onboarding-forge/2 → onboarding-forge/4` in both preambles. That is direction (b), while spec §5 still lists F8 as open with (a) recommended. Proposed: record F8 as decided (b), which matches what the lines already say, and make sure the batch-2 line reaches `main` with batch-4's merge.

## Trail

Read:
- the spec (whole) and `critic-diff-brief.md` (whole);
- t-213 (the P7-P11 lines);
- the full diffs of all five branches, and the commit messages of `77a1d50`, `8d12aac`, `8d3350f`, `0ce7208`, `c20697c`, `6bc60b1`, `3149828`;
- on the branches: `planning_contract.py:3494-3610`, `execution_request.py` `registered_probe`, `event_store.py:6-16,170-190`, `waiver.py` `split_overridden`, `driver_stage_build.py:95-125`, `report_facts.py` `_headings`/`_section_span`/`left_with_you_text`, `acceptance.py` `red_by_requirement` (whole);
- `docs/SIBLING_MAP.md` axis 26 and its grep;
- `judgment-census.json` (rows for the touched functions);
- `test-layers.json` (`test_walk_plan_fields` row);
- the batch-2 file on `main`, the batch branch and `of-batch4`; batch-5 `onboarding-forge`; PC3-3; RD2-4;
- `tools/critic_verdict.schema.json`.

Reruns (sources from `git archive` of each branch into a temporary directory; `python -B <abs path>`):
- `test_report_facts.py` (P9): `=== report_facts: 1276/1276 ok ===` rc=0
- `test_red_window.py` (P1): `=== red window: 196/196 ok ===` rc=0
- `test_question_branches.py` (P7): `=== question branches: 707/707 ok ===` rc=0
- `test_execution_request.py` (P8+P10): `=== test_execution_request: 498/498 ok ===` rc=0
- `role_load.py --all` (P11): `qa-automator 20,257 ... process 18,690 ... ratchet 20,257`; `qa-code-critic 19,420 ... 17,597 ... 19,420`
- merge-tree: as in (6).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "P7-1 planning_contract.py:3569-3570 (77a1d50): _reopened re-derives prior and the again_in_words predicate the caller already decided at :3546; pass prior and again_in_words as parameters and drop the second derivation (non-blocking)",
    "P11-1 plans/piles/onboarding-forge/batch-2-onboarding-roles-forge-p3.md: add the FR-33 row the spec edge owes to its live-evidence table (P11 role-text change, closed by code, not proven) before the batch closes (non-blocking, Lead/integrator edit)"
  ],
  "class_completeness": "Covered: axis 26 (P8 rewrite verified site by site), axis 18 (four role-load rows named), F1 word (P1 done, exactly 10 literals left for stacked P2-P6), P9 headings in own files, axes 32/34 n/a. Queued and verified on origin/main 0106ff9: F3 PC3-3, F5 OF5-1, F7 OF5-2, F6 RD2-4. Missed, proposed to the Lead: M-1 F4 transfer lines for six grown functions absent from batch-2 leftovers; M-2 stand-word reader twin (drivers stand_check/s6_no_stand vs check_delivery.stand_word: two stage tuples, two match strings) with no node; M-3 report-heading symmetry has no SIBLING_MAP axis (land with P5 or RD2-4).",
  "trail": {
    "read": [
      "docs/tasks/specs/t-205-hf8-4-parts.md",
      "docs/tasks/critic-diff-brief.md",
      "docs/tasks/specs/reviews/t-213-t-205-plan-review.md (P7-P11 lines)",
      "diffs of origin/wip/hf84-p7, hf84-p8p10, hf84-p9, hf84-p11, hf84-p1 against their merge bases",
      "planning_contract.py:3494-3610 (p7)",
      "execution_request.py registered_probe, _observe_stand, _observe_precedent (p8p10)",
      "event_store.py:6-16,170-190",
      "waiver.py split_overridden, stand_block",
      "driver_stage_build.py:95-125",
      "report_facts.py _headings, _section_span, appendix_span, appendix_body (p9)",
      "validate_artifacts.py diff hunks and DoD grep (p9)",
      "acceptance.py red_by_requirement, _red_source, _rows_for_instance (p1)",
      "docs/SIBLING_MAP.md axis 26",
      "scripts/tests/fixtures/judgment-census.json rows for touched functions",
      "scripts/tests/test-layers.json test_walk_plan_fields row",
      "plans/piles/onboarding-forge/batch-2 and batch-5, package-ci batch-3, report-delivery batch-2",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B <p9 archive>/ai-packages/qa-factory/scripts/tests/test_report_facts.py", "result": "report_facts: 1276/1276 ok, rc=0"},
      {"command": "python -B <p1 archive>/ai-packages/qa-factory/scripts/tests/test_red_window.py", "result": "red window: 196/196 ok, rc=0"},
      {"command": "python -B <p7 archive>/ai-packages/qa-factory/scripts/tests/test_question_branches.py", "result": "question branches: 707/707 ok, rc=0"},
      {"command": "python -B <p8p10 archive>/ai-packages/qa-factory/scripts/tests/test_execution_request.py", "result": "test_execution_request: 498/498 ok, rc=0"},
      {"command": "python -B <p11 archive>/ai-packages/qa-factory/scripts/role_load.py --all", "result": "qa-automator 20,257 / process 18,690; qa-code-critic 19,420 / 17,597; each equals its role-load.json row"},
      {"command": "git merge-tree --write-tree pairwise and chained over main, batch-2, p1, p7, p8p10, p9, p11", "result": "all rc=0, no conflicts; vs wip/of-batch4 only pile-file conflicts (PILES.md, onboarding-hooks batch-5)"}
    ]
  }
}
```
