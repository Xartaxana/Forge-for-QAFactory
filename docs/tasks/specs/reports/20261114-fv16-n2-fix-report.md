# FV1-6 N2 fix round (t-788) - report

Branch wip/fv16-n2. Spec: code critic verdict t-780 (B1-B4, F1, optional closure).

## Merge from main
`git merge origin/main` -> clean (merge commit 08376ea3), no conflict in any file.

## Per finding
- B1 (`brief_pack.case_concern_lines`): restored `"Answer each in the plan: a `{token}` concern"`. Row C8b: head of a story with a concern and
  no rejected row equals, word for word, the literal text built without the clause (not a copy of the code).
- B2: the three heads that carry `({k} ask` are built without the clause, cut by `_short(.., HEAD_LINE_CHARS)`, then `({k} ask` is replaced once by
  `({rej}{k} ask`. r == 0: nothing inserted (byte-identical, C8b). If the cut text lacks `({k} ask`, the clause is appended as its own sentence
  (`. 1 of them cases it still rejected when S4 went on`); row C9b by `HEAD_LINE_CHARS = 30`. Rows C9b: a 55-char dispatch id keeps the clause
  (and the field to fill when the clause-less text fits); loop over ids of 1..79 chars: the clause once, the text without it never over 400, and
  a text of exactly 400 is reached; `in `apart_reason`` kept whenever the clause-less text holds it.
  Heads enumerated (each head where text is inserted before `_short`): plan-author - fixed; plan-judge (`elif plan`) - fixed;
  window-author - fixed; judge-in-window (`else`) - not affected, it never carried the clause and has no `({k} ask`.
- B3: both doubt heads (receipt doubt; failed read) read `... `approve_with_concerns` and every reviewed row whose verdict is not an approving one there
  before you {verb}`. Deviation of form: in the exception head the sentence has `in work/test-cases/**/critic-findings.md` where the first has
  `there`, so the added clause precedes `in work/...` (the wording itself verbatim). No verdict-word list. Row C7b (both heads, two roles, and the
  failed-read head by a raising `_sp`). Siblings in the function naming only `approve_with_concerns`: just these two; none left.
- B4 (`s5_plan._file_concerns`): case-less rejected elements (`_ref(case) is None`, which includes the dash forms `_ref` reads as no case) are decided by
  `latest_global = {plan_row: latest position}`; case-bearing elements keep `latest`. Rows C5b: two rounds, other plan row -> both carried;
  same plan row twice -> only the later one; empty plan_row twice -> the later round's only; empty plan_row earlier + other plan row later -> both
  (over-carry). Test order note: with this fixture the oldest round's remark takes `CR-global`, so C5b compares sorted ids/problems.
- F1 (`critic_rollcall.rejected_rows`): after the `reviewed is not True` skip, `_row_outcome("", {"reviewed": True, "verdict": row.get("verdict")},
  declared)[0] == "accepted"` -> continue. Signature/return as the verdict quotes; the row is rebuilt as a small dict because
  `_row_outcome` indexes `row["verdict"]` and rows passed by callers may lack the key (`.get` was used before). C12 green.
- Closure: done with B4: the pinned-set read and the removed-case prefix are in a local closure `led(case, problem)` inside `_file_concerns`;
  the nesting of the rejected loop is down by two levels; behaviour identical (C10 green).

## Witness (verbatim)
```
test_s5_plan_grouping.py:       === test_s5_plan_grouping: 307/307 ok ===
test_critic_rollcall_apply_fixes.py: === critic_rollcall_apply_fixes: 51/51 ok ===
selftest --limits --lang:       === qa-factory selftest: 4/4 ok ===
scenario_walk --witness-for scripts/brief_pack.py scripts/s5_plan.py scripts/critic_rollcall.py: printed; ran alone (each < 1 min), none slow/quarantined:
  test_detector_verdict 210/210 ok; test_one_source_per_fact 21/21 ok; test_whole_list_sites 292/292 ok;
  test_s5_plan_windows 104/104 ok; test_s5_grown_windows 65/65 ok; test_ahead_cards 265/265 ok
```
Left to the canon: test_brief_pack_s5_plan.py, test_carried_concerns.py, test_scenario_cart_1 / local_1_0108 / local_1_arm_b, other `scenario`/slow files.
New row names: C5b (x4), C7b, C8b, C9b (the C9b loop is one variant row family over dispatch-id length).

## FR pass
B - text to a person: the brief's heads changed (the clause now sits inside the parenthesis and survives the cut; the doubt heads name the non-approving rows); no person-facing question text.
C - contracts: no field added; F1 removes a second writing of "row approves" (FR-13/FR-17: one reader).
E - delivery/reporting: a still-rejected row travels with its words, never silently dropped (FR-41/FR-59).
G - code: English, no control bytes, no language/project branch (FR-30, FR-47).

architecture: AR-10, AR-21, AR-28 -- the field to fill survives the cut; a still-rejected row travels with its words; no case-less reject is dropped
judgment: none -- code carries the critic's words whole and decides nothing about the case
axes: see commit/this report - axes 1-n: the change touches no new symmetry; the heads of `case_concern_lines` swept above; rows 133/152 as in the verdict.

## Siblings noticed (not edited)
- `critic_rollcall.py` expression `row.get("ids") or [row.get("case") or ""]` appears twice (verdict: acceptable).
- Q1 (`current_rejected == []` on a `partial` round) remains with node N1.

## Needed beyond the manifest
`ai-packages/qa-factory/scripts/critic_rollcall.py` `_row_outcome` (read for F1).
