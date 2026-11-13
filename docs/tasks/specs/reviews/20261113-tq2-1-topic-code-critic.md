# TQ2-1 option (c): code-critic pass over K1, K2 and N5 (one pass for the topic)

Critic (Opus), 13.11.2026. Spec / DoD: `docs/tasks/specs/20261113-tq2-1-revision-option-c-spec.md` (§0, §C, §D.0, K1, K2, N5, §7).
Diffs: K1 `e4ba384..a0b26ac`, K2 `a0b26ac..2e73966` (code ed55632), N5 `e4ba384..878833e`. Read-only; this file is the only write.

## Verdict

**fit_with_fixes.** No blockers. Four fixes go in before merge (F1-F4: one line to a dozen lines each, all inside the nodes' owns). One more fix
is low but cheap (F5). Three items go to the queue (Q1-Q3). Acceptance is the Lead's.

## Fixes (before merge)

- **F1 (K2), `brief_pack.py:2015-2016`, plus the B1/B7 fixture in `test_brief_pack_s5_plan.py` (`k14_...`, the `merge`/`pair` rows).**
  `k` counts concerns. In a real round the token sits on BOTH cases of a pair: S4 exit `_merge_concern_errors` demands it, and the
  spec's own key text (§K2, "TC-1, TC-2 `approve_with_concerns` with note `parametrise into one test: TC-1, TC-2`") puts it on both.
  So one pair prints `2 ask to parametrise` while the critic's line two rows above says `prints 1 merge hint(s)`. One packet then gives
  two counts for one instruction (FR-10). Fix: count distinct groups,
  `k = len({frozenset(g) for g in asked})`. Rebuild the B1 fixture with the token on TC-1 AND TC-2, and keep the assertion
  `1 ask to parametrise`. The fixture as committed is not a real round (answer 2).
- **F2 (K2), `brief_pack.py:2053-2054` with `s5_plan.concern_report`.** Take a story whose every accepted round was dropped on its
  receipt (B6). Its brief prints `- case critic's concerns: none raised in 1 accepted round(s)` right beside the head line saying
  that round "could not be read against the critic's receipt". K2-E3's invariant is "a dropped round is never reported as an empty fact
  (FR-41)", and "none raised in 1 round" is such a fact. Fix: leave the rounds of `silent` files out of the count. When no readable
  round is left, print no `none ...` files line (the silent head line and the files lines already say it). B6 adds `none raised` to
  its `unwanted` list (deviation 5, answer 4).
- **F3 (K2), `brief_pack.py:2018-2019` (`held`) and `s5_plan.py:1524-1525` (`matches`).** Both hand-roll "does this key name this case
  id" as `key == ident or ident in C.case_ids(key)`. SIBLING_MAP row «Scope key vs manifest cell» and `contract.names_case`
  (contract.py:4505, docstring: "THE ONE predicate behind every 'is this case among these keys' read ... so no second matcher exists",
  AR-13/AR-15) already own that relation. Two new copies, one in each module, are a second way of an existing thing. Today they behave
  alike, because `parametrise_group` yields bare ids (and `case_matches` adds "two different areas never match"). Fix: `held(i)` ->
  `C.names_case(scope, i, cfg)` and `matches(key, i)` -> `C.names_case([key], i, cfg)`. G7 and B7a must stay green. The spec's item 6
  wrote the copied rule: that is a spec defect the designer would have caught on the map, and the fix belongs to this round.
- **F4 (N5), `critic_rollcall.py:118` and `:120` (`verdict_at`, `fix_at`).** These sit in the same function N5 edited, follow the same
  exact-name rule, and are still hand-rolled. A header cell ``` ` Verdict ` ``` is now found for `note` but not for `verdict`: one
  function, two rules. Under the sweep-the-artifact-first rule (CLAUDE.md rule 9) the same-function neighbours come first. Fix: both
  through `C.md_column(raw[0], ...)`, plus one row of `NOTE_COLUMN_CASES` (or a sibling row) for `verdict`. Keep `case`
  (`startswith`) and `reviewed` (`in`) as the spec says (answer 6).
- **F5 (K2, low), `s5_plan.py:1228` `concerns_for_scope`.** A legacy dispatch whose record and controller both hold no scope reaches
  `build` with `scope == []`. That is "the story scope" in `build`'s own words (brief_pack.py:4285). `mine` is then empty, so every
  placed concern lands in window 0 and is dropped, with the files line "none for the cases of this window (N for other windows)". That
  is a silent UNDER-carry, against the K2 error direction ("never under-carry silently"). Rare: `pack_windows` never dispatches an empty
  window (controller.py:436-439). Fix: when `not scope`, return every concern `unplaced` with `why = "the dispatch names no scope"`.

## Queue (lines for the Lead's «Остатки»; the node ids are the Lead's)

- **Q1 (N5 siblings, outside owns).** `hand-rolled table-column lookups outside critic_rollcall: audit_factory.py:749 header.index("asked"); planning_contract.py:1341 ac_ref, :1345 source, :1446 columns.index("decision"), :2488 MD_COLUMN_OF_KEY, :2489 ts -> contract.md_column (the :1341/:1345/:1446 forms raise ValueError on a missing column, so state the error direction per site) | узел: <new node in the next untaken test-code-quality batch>`. Spot-checked: all six lines read as quoted. `:1446` is beyond the spec's list (the builder found it).
- **Q2 (F7, decided (a)).** The finding "the window cut keeps merge groups together, plus C12 on legacy windows" is owed by the Lead. It
  is not found on these refs: `git grep -i "split_windows|case_groups"` over `plans/piles/` at 2e73966 hits only
  `cost-dashboard/README.md`; the positive control `TQ2-1` hits the test-code-quality card and batch 2. Until it exists, the legacy
  residual is named only in the briefs (K2-E12).
- **Q3 (code quality, queue).** `brief_pack.case_concern_lines` runs 71 lines (`brief_pack.py:1993-2063`) with a nested `def`. It
  chooses one of four head texts by `plan`/`author`. After F1/F3 it shrinks; a table of the four texts would take it under 60. Also,
  `elsewhere` is computed for the legacy code critic and read only on the author branch (dead work, trivial). The stage `reason` in
  `concerns_for_scope:1236` is not bounded the way the exception branch is (`_show(..., 100)`). It is appended whole to a head line
  (deviation 3), so bound it there.

## Answers to the dispatch

1. **Fit per node.** K1: every key holds. The bullet is the spec text verbatim. The critic parenthesis is 59 -> 59 B. The registry row
   and anchor are present. R1 13320 -> 13355 (+39, bound 50), with R2/R3 unchanged, is in the K1 report. The edges are textual and the
   wording does not contradict K1-E1..E8. K2: items 1-16 are implemented, and edges E1-E16 are met, apart from E3's second half (F2) and
   the stated under-carry direction (F5). The three empty-outcome lines exist (`none carried` / `none for the cases of this window (N
   for other windows)` / `none raised in N`). Advice only, checked: the diff adds no `raise`, `sys.exit` or `return <n>`. `findings`,
   verdict, exit code and `ok` are computed as before, and G9 pins exit/ok/findings equal with and without a concern. `merge_hints`
   reads `apart_reason` presence only (`isinstance(str) and strip()`). N5: every key holds, `_has_note_column` is gone, and the readers
   of `note` tolerate None (I re-read `_carries` -> `parametrise_group`, `str(note or "")`).
2. **Count.** Count distinct GROUPS. What the automator and the plan critic must act on is one test per group, and `merge_hints`
   already deduplicates by group, so concerns double-count every pair. The B1 fixture is not faithful (token on TC-1 only). Fix F1.
3. **Dedup by tag.** Right. Item 6's "one row per concern" is the spec's slip, and G2/B2 say "one hint". A tag over the sorted plan keys
   of the group is the natural identity. Two concerns naming DIFFERENT groups that overlap still give two rows: over-report, the safe
   direction. The dedup is pinned (`G2: two concerns naming one group give ONE hint`).
4. **Deviations 3-5.** Deviation 3 (`_short` on the base only, E12/E13 clauses whole) is acceptable: E12/E13 ("said, never hidden")
   outrank the length bound, and the clauses are short. Bound the stage reason (Q3). Deviation 4 (merge after the cap chain) is
   acceptable. I read `plan_dispatch_lines` whole: the cap chain has no `return`, the head before it holds only the first line, the
   grouping line and the merge line, so the head order is the spec's and all three roads carry the side file. Deviation 5 is a fix (F2).
5. **Raises (AR-20, axis 18).**

   | Ratchet | Old -> new | Delta | Bound | Reason line in the commit |
   |---|---|---|---|---|
   | `ratchet_tokens.qa-case-designer` | 13320 -> 13355 | 39 | ≤ 50 | yes (a0b26ac) |
   | `process_ratchet_tokens.qa-code-critic` | 17596 -> 17686 | 90 | ≤ 100 | yes (ed55632) |
   | `ratchet_tokens.qa-code-critic` | 19420 -> 19509 | measured 19509 > 19420 | as R5 | yes (ed55632) |
   | `S5_PLAN_BRIEF_BYTES_MAX` | 9520 -> 9559 | 39 B | 1..60 | yes, plus the constant's comment |

   All four are within bound and named. R2, R3 and R7 are untouched. The census gains no row.
6. **N5 siblings.** `verdict_at`/`fix_at` are fixed in this round (F4). `audit_factory`/`planning_contract` go to the queue (Q1, node
   line above).
7. **Merge.** `git merge-tree --write-tree 2e73966 878833e` -> exit 0, tree 6b3107a, no conflict. The hunks are disjoint (K2 :911-925;
   N5 :95-140, :801-842). K2 hand-rolls no column lookup. N5's `note = None` reaches K2 only through `parametrise_group`, which takes
   None. Order: K1 -> K2 -> N5 (N5 may go anywhere; it does not depend on K2).
8. **End to end.** The chain is: critic note -> `_read_round` (receipt) -> `concern_report` -> side file for the plan author and plan
   critic on every cap road -> the author head line ("answer in the plan") -> `--check` / `plan_result` merge hint -> the plan critic's
   merge line plus the rubric bullet («On the plan», which the brief names to Grep) -> the planned slices (unchanged) / every legacy
   window's own side file. Hops where it can still be lost:
   - (a) A legacy pair split across windows, with no C12 presence check on legacy: F7, said in the brief, the finding is owed (Q2).
   - (b) A legacy dispatch with empty scope (F5).
   - (c) A legacy brief with no dispatch record: no lines (C11, by design; the production caller was not traced, estimate).
   - (d) An area story: `_placement` makes every CC unplaced, so it is carried to every window. That is over-carry, not loss (§9 analog).
   - (e) A file whose LATEST round is receipt-dropped while an earlier round listed cases. It is not `silent`, so the dropped round goes
     unnamed in the brief (existing latest-listing seam, unchanged by K2; analog, not widened).

## Standing lines (critic-diff-brief)

- **1 Fit:** as answer 1. F2 and F5 are the error-direction gaps.
- **2 Builder decisions:** deviations 1-6 judged above. 2, 3 and 4 are in the safe direction; 1 and 5 are fixes.
- **3 Seams:** K2's edits to `build`/`plan_dispatch_lines` are additive. The `window`/`plan` branches and the K7 grouping line are
  byte-unchanged (k9 and K7 rows green in the witness).
- **4 Class-wide:** the token reader is one (`parametrise_group`; `git grep -i "parametrise into one test"` over non-test scripts hits
  only the constant and a docstring, and the positive control hits the test file). The remark printer and placer are one each. The
  case-key matcher class is NOT closed (F3). The column-lookup class is closed in-artifact after F4, with the outside members queued (Q1).
- **5 Tests:** B1-B8 and G1-G9 fail before the change (the report says they were run against the a0b26ac scripts). Weak spots: B1's
  fixture (F1); B6 does not forbid `none raised` (F2). Test lines +168 vs product +252. No new test file.
- **6 DUPLICATION AND CONSISTENCY:** one finding, F3 (two copies of the `names_case` relation). The rest: none found. I grepped
  `in C\.case_ids\(` over scripts (17 hits; only the two new ones are a key-vs-id predicate) and `PARAMETRISE_TOKEN` (one parser).
  `merge_hint_rows` mirrors `hint_rows` by spec (C9), so that is not a finding.
- **7 CODE QUALITY:** `case_concern_lines` runs 71 lines, a nested def, and computes `elsewhere` for a branch that never reads it (Q3,
  queue). No function in K2's s5_plan or N5 goes over 60 lines. No dead branches otherwise.
- **8 Hygiene:** `--lang` green in all three reports. ASCII text; the rubric's «» are pre-existing in that file.
- **9 Ratchets:** the table in answer 5. No unnamed raise.
- **10 ARCHITECTURE:** AR-10/13/15/18/20/21/23/28/29 are named in ed55632; AR-10/20 in a0b26ac; AR-13 in N5. AR-13/AR-15 are
  touched and broken once (F3). Producer and readers: `case_concerns`' output is unchanged (it is `concern_report["concerns"]`), so
  gate A and `remarks_of` are unaffected.
- **11 JUDGMENT:** none moved. Code joins ids and reads presence. The blocker is the plan critic's, through a rubric bullet (process
  text, counted in R5, no craft marker added). No census row, no `blocks_override`.
- **12 ONE ROAD:** none found. Planned and legacy windows share `placed_remarks`/`remark_lines`. Both plan-size roads carry the side
  file. The legacy split residual is F7, a decided fork with a queued finding (Q2). A Lead fork is not an owner's exclusion, so it stays
  on the Lead's queue.

## Trail

Read: the spec (whole, 708 lines); `docs/tasks/critic-diff-brief.md`; the three builder reports; `git diff` of the package for all
three nodes plus the commit messages; `brief_pack.py:2066-2141` and `:4259-4350` (K2 head); `controller.py:414-450`, `:2130-2145`,
`:4147-4180`; `contract.py:3563-3569`, `:4145-4175`, `:4257-4282`, `:4480-4511`; `s5_precheck.py:1205-1230`; `critic_rollcall.py:106-125`
(N5 head); SIBLING_MAP rows matched by `(?i)scope_keys|case_ids|md_table|column` (lines 33, 152, 191, 303, 309, 335, 416);
`tools/critic_verdict.schema.json`.

Reruns:
- `( cd tq2-k2/ai-packages/qa-factory && python -B scripts/tests/test_s5_plan_grouping.py )` -> `=== test_s5_plan_grouping: 116/116 ok ===`
- `( cd tq2-n5/ai-packages/qa-factory && python -B scripts/tests/test_critic_rollcall_apply_fixes.py )` -> `=== critic_rollcall_apply_fixes: 47/47 ok ===`
- `git -C tq2-k2 merge-tree --write-tree --name-only 2e73966 878833e` -> `6b3107a3b0b9d01e1b52316ad82c4777729a0585`, exit 0
- `git diff a0b26ac..ed55632 -- scripts/*.py | grep -E '^\+.*\braise\b|sys\.exit|return [0-9]'` -> no lines (rc=1)
- `git grep -n -i "parametrise into one test" ed55632 -- scripts/*.py` (non-test) -> critic_rollcall.py:57 and an s5_plan docstring only

Not re-run: `test_brief_pack_s5_plan.py` (slow-listed; the report's 213 -> 241 is consistent with 9 rows x 3 checks + 1).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Token reader, remark printer and placer are each one. Case-key matcher class (SIBLING_MAP row Scope key vs manifest cell, contract.names_case) gains two new copies in K2: fix F3. Column-lookup class: same-function neighbours verdict_at/fix_at fixed in round (F4); audit_factory.py:749 and planning_contract.py:1341/1345/1446/2488/2489 queued (Q1). F7 finding owed by the Lead, not found on these refs (Q2).",
  "fixes": [
    "F1 K2 brief_pack.py:2015-2016 count distinct parametrise groups (frozenset) for k; B1/B7 fixture carries the token on both TC-1 and TC-2 - before merge",
    "F2 K2 brief_pack.py:2053-2054 + s5_plan.concern_report: exclude rounds of silent files from 'none raised in N'; zero readable rounds -> no none-line; B6 forbids 'none raised' - before merge",
    "F3 K2 brief_pack.py:2018-2019 held and s5_plan.py:1524-1525 matches -> contract.names_case (the one matcher, AR-13/AR-15) - before merge",
    "F4 N5 critic_rollcall.py:118,120 verdict_at/fix_at through contract.md_column, one table row - before merge",
    "F5 K2 s5_plan.py:1228 concerns_for_scope: empty scope -> every concern unplaced with why 'the dispatch names no scope' (no silent under-carry) - before merge, low",
    "Q1 N5 queue: audit_factory.py:749, planning_contract.py:1341/1345/1446/2488/2489 -> md_column, node in the next untaken test-code-quality batch",
    "Q2 queue: F7 finding (window cut keeps merge groups; C12 on legacy) owed by the Lead",
    "Q3 K2 queue: case_concern_lines 71 lines (brief_pack.py:1993-2063), elsewhere computed but unread for the legacy critic, stage reason unbounded at s5_plan.py:1236"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-tq2-1-revision-option-c-spec.md",
      "docs/tasks/critic-diff-brief.md",
      ".claude/worktrees/tq2-k1/docs/tasks/specs/reports/20261113-tq2-1-k1-report.md",
      ".claude/worktrees/tq2-k2/docs/tasks/specs/reports/20261113-tq2-1-k2-report.md",
      ".claude/worktrees/tq2-n5/docs/tasks/specs/reports/20261113-tq2-1-n5-report.md",
      "git diff e4ba384..a0b26ac, a0b26ac..2e73966, e4ba384..878833e (package) and commit messages",
      "tq2-k2 brief_pack.py:2066-2141, 4259-4350",
      "tq2-k2 controller.py:414-450, 2130-2145, 4147-4180",
      "tq2-k2 contract.py:3563-3569, 4145-4175, 4257-4282, 4480-4511",
      "tq2-k2 s5_precheck.py:1205-1230",
      "tq2-n5 critic_rollcall.py:106-125",
      "docs/SIBLING_MAP.md lines 33, 152, 191, 303, 309, 335, 416",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B scripts/tests/test_s5_plan_grouping.py (tq2-k2 package dir)", "result": "=== test_s5_plan_grouping: 116/116 ok ==="},
      {"command": "python -B scripts/tests/test_critic_rollcall_apply_fixes.py (tq2-n5 package dir)", "result": "=== critic_rollcall_apply_fixes: 47/47 ok ==="},
      {"command": "git merge-tree --write-tree --name-only 2e73966 878833e", "result": "6b3107a3b0b9d01e1b52316ad82c4777729a0585, exit 0, no conflict"},
      {"command": "git diff a0b26ac..ed55632 scripts/*.py | grep added raise/sys.exit/return n", "result": "no lines (rc=1)"}
    ]
  }
}
```
