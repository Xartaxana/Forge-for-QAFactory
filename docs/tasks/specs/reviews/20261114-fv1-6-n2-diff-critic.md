# FV1-6 N2 — code critic (t-780)

Subject: `wip/fv16-n2` 5b27a38 against merge base d5d602d8 (6 files, +345/-22). DoD: card N2 of
`.claude/worktrees/wave13/docs/tasks/specs/20261114-fv1-6-s4-only-spec.md` (fix round t-676; §3.2 points 1-7, E-N2-1..12, C1-C14).
The fv16-n2 worktree holds the PRE-fix-round draft of the spec; the code follows the wave13 card, so that card is the DoD used here.

**Verdict: needs_work (fit_with_fixes) — 4 merge blockers (B1-B4), 1 fix before merge (F1), 1 queue line (Q1).** The core carrier
(predicate, round cut, latest-word rule, CR ids, removed-case prefix, concerns-only CC numbering) is right and matches the card; the
blockers are a stray text edit, a head line cut that the new clause causes, two roads on which a still-rejected row reaches S5 without
its words, and one duplicated predicate body. All fixes stay inside the owned functions. Acceptance is the Lead's.

## Blockers (each executable by a fresh builder from this text alone)

**B1. Stray edit of role text; E-N2-7 broken.** `brief_pack.py` `case_concern_lines`, the plan-author head (branch `if plan and author`,
line 2030 in the worktree): `"Answer each in the plan:a `{token}` concern ..."` — the space after the colon was deleted (main has
`"Answer each in the plan: a `"`, origin/main brief_pack.py:2040). Every story with concerns, rejected rows or not, now gets a changed
brief, so "a story with no rejection sees a byte-identical brief" (E-N2-7) is false. Empirics: probe output
`Answer each in the plan:a `parametrise into one test:` concern ...`. **Fix:** restore `"Answer each in the plan: a `{token}` ..."`.

**B2. The new clause pushes the instruction past the 400-character cut.** The head is `_short(text, HEAD_LINE_CHARS)` (400). The clause
`"{r} of them cases it still rejected when S4 went on; "` (~56 chars) is inserted BEFORE the cut, so with r > 0 the tail is lost.
Empirics (dispatch id `S5-qa-automator-plan-12`, temp story path): plan-author head = 400 chars ending
`... or each test that holds them says why in `apart...` (the field name `apart_reason` lost; AR-10/FR-38: the field the role must fill);
window-author head = `... one parameterized test over...` (pre-diff text of the same inputs fits under 400). Real story paths are
longer than the temp path, so this hits the ordinary case. **Fix:** build `text` WITHOUT the clause, apply `_short(...)`, then insert
the clause into the parenthesis of the cut text (`text = text.replace(f"({k} ask", f"({rej}{k} ask", 1)` on the three heads that carry `({k} ask`; NOT the first `(`, which belongs to `concern(s)`; the parenthesis sits in the first ~120 characters and is never cut), so the clause
— bounded by itself — never pushes the instruction out (same reasoning as the residual appended after the cut at line 2043). Test row
C9b in `fv16_still_rejected_rows`: a story with r > 0 and a dispatch id of 40+ characters — the plan-author head contains
`in `apart_reason`` and the clause.

**B3. DoD (b): the doubt road and the failure road tell the automator to read ONLY the `approve_with_concerns` rows.** When a findings
file's round does not match its receipt (E-N2-4), N2 carries nothing — correct — and the brief names the file; but the head says
`read the rows marked `approve_with_concerns` there before you {verb}` (line 2056-2058), and the exception head (line 2061-2062) says the
same. A case the S4 critic still rejects in that file therefore reaches S5 with no remark AND with an instruction that points away from
its row. Empirics: SILENT probe head = `... read the rows marked `approve_with_concerns` there before you group the tests`, for a file whose
only row is `reject`. AR-21/AR-24/FR-49. **Fix:** in both heads, say `read the rows marked `approve_with_concerns` and every reviewed row
whose verdict is not an approving one there before you {verb}`. Test row C7b: the C7 story's `case_concern_lines(...)["head"]` contains
`whose verdict is not an approving one`.

**B4. A case-less still-rejected row is dropped by an unrelated case-less row of a later round.** `_read_round` puts `""` in `listed` for
every reviewed row with no case, and `_file_concerns` decides a rejected element by `latest.get(str(item["case"]))`, so all case-less
rows of a file share ONE key `""`. Round 1 rejects plan row TS-5 (no case), round 2 (fewer rows) rejects TS-6 (no case) and does not
look at TS-5: TS-5's words vanish. Empirics: `GLOBAL [('CR-TC-1', 'wrong oracle'), ('CR-global', '(plan row TS-6) no case for TS-6')]` —
TS-5 missing. Breaks E-N2-2 ("no remark is dropped for a case nobody reviewed again") and E-N2-3 (AR-28). **Fix (in `_file_concerns`
only):** for a rejected element with case `""`, the deciding position is the LATEST round whose `rejected` list holds a case-less element
with the same `plan_row` (`latest_global = {item["plan_row"]: position for position, one in enumerate(read) for item in one["rejected"]
if item["case"] == ""}`); carry it when `latest_global[item["plan_row"]] == position`. Error direction: over-carry (an approving case-less
row is not tracked, F3 allows). Case-bearing elements keep `latest`. Test row C5b: the two-round input above gives
`CR-global` (TS-6) and `CR-global.2` (TS-5) — both present.

## Fix before merge

**F1. `rejected_rows` re-implements the row-acceptance rule that `_row_outcome` already owns (DUPLICATION; SIBLING_MAP row 152:
"a new reader of the critic's word ... `scoped_verdict`").** `critic_rollcall.py:420-426` repeats `_row_outcome`'s accepted branch
(`critic_rollcall.py:248-256`: verdict None -> declared in `APPROVING_VERDICTS`; cell in `APPROVING_VERDICTS`). Two writings of "this
row approves" will drift (e.g. a future change to `_row_outcome`'s unknown-word handling). **Fix:** inside `rejected_rows`, after the
`reviewed is not True` skip, decide by `_row_outcome("", row, declared)[0] == "accepted"` (continue) — keep `word` only for the
`verdict` field (`row["verdict"]` if not None else `declared`). Behaviour identical; C12 rows stay green.

## Queue

Q1. `current_rejected` returns `[]` ("all approved") for a round whose `Verdict:` is `reject` over all-approving cells, which
`scoped_verdict` refuses as `partial` (`_round_word_rule`). Probe on the real recorded round `fixtures/run-12586-concerns`:
`recorded []`. N1's question must not say "the reviewer still rejects 0 cases" for such a round. |
перенос: узел N1 пачки FV1-6 (edge in the N1 card: `current_rejected == []` while the round is `partial` by `round_word_rule` -> the
unreadable seam, not the priced question) | обоснование: N1 is the only reader that turns `[]` into text; N2's predicate follows the
plan critic's B1 (cells decide) | подтвердил: —

## The report's open items (DoD b)

1. Lower-casing `declared` — **right**: `parse_rollcall` lower-cases the cell (`critic_rollcall.py:129`), `scoped_verdict` lower-cases
   the declared word (`:347`); without it `Verdict: APPROVE` with no verdict column would be over-listed. Probe `DECL []`.
2. `still_rejected` set after `_concern_remark` — **right**: same dict, one extra key; card's "ONE extra key" holds (C1 checks the keys).
3. Concerns first, then rejected, per round — **right** (card silent; ids made unique after collection; C6/C14 pin).
4. Judge-in-window head with no count — **right as is**: the side file prints `check` = `case critic, S4 - still rejected` per remark
   (probe side file), and the card's head form applies to the heads with `({k} ask`. No queue.
5. `case_paths` not called, inline `rsplit` — **right**: the card names the match, not the function; C10 pins both branches.
- **Can a still-rejected case reach S5 without its words?** Yes on two roads before the fixes: B3 (receipt doubt / read failure: the
  head points elsewhere) and B4 (case-less rows). By design (card): a `stale` earlier record (E-N2-9) and windows briefed before the
  merge (E-N2-10, N3 reports them). After B3+B4 none found on the roads read: `_file_concerns` -> `concern_report` -> `remarks_of` /
  `case_concern_lines` (plan, legacy window via `concerns_for_scope`, which returns every remark `unplaced` on failure).
- **Can gate A count one case twice?** No. `gate_brief.carried_concern_cases` (`gate_brief.py:2224-2237`) dedups by `case` with
  `dict.fromkeys`, and both kinds carry `case` from the same `case_ids` parse, so a case with a CC and a CR remark appears once;
  case-less (`None`) remarks are excluded there (pre-existing).

## Standing questions

- Fit (1): §3.2.1-6 implemented as written except B1-B4; `current_rejected` per card; E-N2-1..12 pinned by C1-C14 (read).
- Builder decisions (2): all five safe (above).
- Seams (3): additive; `_read_round` 3-tuple has callers only in the same file (`carried_concerns` `[1]`, `accepted_rounds`,
  `current_rejected`); grep of `_read_round(` over the package: only `critic_rollcall.py`; the quarantined `test_carried_concerns.py`
  reads `accepted_rounds` by key (line 472-477).
- Class completeness (4): map rows 133 and 152 walked — F1 is row 152's finding; row 133 lists other carriers, not touched here.
  The builder's report did not enumerate axes (map not in its manifest); the commit carries `axes: see report` — the axis block is the
  Lead's, as the commit says.
- Tests (5): C1-C14 would catch the carrier's defects; they did not catch B1 (C8 checks only the absence of "still rejected") or
  B2 (C9 checks a prefix, short dispatch id) — C9b and C7b above close the two through the brief door.
- DUPLICATION AND CONSISTENCY (6): one finding, F1. Also the expression `row.get("ids") or [row.get("case") or ""]` now appears twice
  in `critic_rollcall.py` (:427, :460) — same file, same meaning; acceptable, no finding. Grep for other readers of `CC-` ids:
  `grep -rn "CC-"` over the package — only `brief_pack.py:2025` (file line `(CC-n)`, cosmetic), `critic_rollcall.py`, `s5_plan.py`,
  CHANGELOG (positive control: the same grep finds `critic_rollcall.py:465`).
- CODE QUALITY (7): `_file_concerns` grows to ~50 lines with 4 nesting levels in the new `for item in one["rejected"]` block
  (`s5_plan.py:1184-1205`: for / if / if pinned is None / try) — fix-before-merge-optional: with B4 the block grows again; move the
  pinned-set read and the prefix into a local closure `prefix(case, problem)`; severity: queue-free, do it in the B4 round.
  `number + sum(1 for r in out if not r.get("still_rejected"))` is O(n²) per file — harmless at roll-call sizes.
- Hygiene (8): `selftest --lang --limits` green in the witness; changelog fragment present.
- Ratchets (9): none touched (no census, no baseline file in the diff).
- ARCHITECTURE (10): AR-13, AR-21, AR-22 named; AR-28 is touched (removed-case and case-less edges) and kept after B4; AR-10 touched by
  the head (B2).
- JUDGMENT (11) / P27 / AR-29 / FR-12: code carries the critic's `note`/`fix` whole and decides nothing about the case; the only test on
  the critic's output is membership of the `verdict` CELL in the closed constant `APPROVING_VERDICTS` (a structured token, the same rule
  `_row_outcome` applies) — no phrase list reads the `note`. The "(case removed since the review)" prefix is a data join against the
  pinned set. `judgment: none` holds.
- ONE ROAD (12): F1 is the one-road residual (two writings of "row approves"); none other found — grep of new branches on a language /
  project name in the diff: none (the diff branches only on `still_rejected`, `case is None`, the pinned set).

## Mergeability into origin/main 2cf488ad (DoD e)

`git diff --stat d5d602d8 origin/main -- <six files>`: only `brief_pack.py` (+92/-30 net 122 lines) and `critic_rollcall.py` (+30/-8).
`s5_plan.py`, `test_s5_plan_grouping.py`, the fragment and the report: untouched on main.
- `critic_rollcall.py`: main's hunks are in `raise_pending` (@@ -747, -765) and `main()` (@@ -1176); N2's in `REJECTED_NOTE` /
  `rejected_rows` / `current_rejected` / `_read_round` / `accepted_rounds` (@@ -403..-437). No overlap.
- `brief_pack.py`: main's hunks at @@ -105 (ROLE_FILES), -236 (TOOLING), -781/-838 (`proof_required_lines`), -3650..-3718
  (`stage_critic_names`, `reviewed_dispatch_lines`, `last_accepted_form`), -4082/-4198 (first look), -4304 (`build`); N2's single hunk is
  in `case_concern_lines` (@@ -2014/-2024), which main has not changed (it only shifted to :2005). No overlap.
- Judged by hunk distance: **clean textual merge, no conflicting function.** Semantic: nothing on main reads `_read_round`'s tuple.
- FV1-28 B1 (uncommitted in `.claude/worktrees/fv1-28-b1`, `git diff HEAD`): hunks @@ -4016..-4405 (`FIRST_LOOK_*`, `first_look_*`,
  `_fl_*`, `build`); `case_concern_lines` (:2005), `_short` (:1145), `HEAD_LINE_CHARS` (:1964) untouched — **no shared lines** with N2,
  also after the B2 fix (which keeps `HEAD_LINE_CHARS`).

## Slow / quarantined files left to the canon (DoD f)

- `test_brief_pack_s5_plan.py` (slow, keep) k14: fixtures carry only `approve_with_concerns` cells (lines 627-629) -> r = 0, heads
  unchanged except B1; B1 is not pinned there (`grep "Answer each in the plan"` over `scripts/tests/`: no hit; positive control: the same grep over `scripts/`
  finds brief_pack.py:2030). **Not red by reading.** After B2's fix: still r = 0, unchanged.
- `test_carried_concerns.py` (quarantined): K3/K7 compare id lists of `remarks_of` / `case_concerns` on the real round
  `run-12586-concerns`; probe `rejected []` on both recorded and fixed bytes -> no CR remark -> **not red**.
- `test_scenario_cart_1.py`, `test_scenario_local_1_0108.py`: the only fixture stories with `reject` cells. cart-1: `concern_report` probe
  -> `[('CC-1', None, False)]` (no CR: the reject case re-listed in round 2); local-1-0108: round 1 rejects `LOCAL-1_TC_020`, round 2
  re-lists it `approve_with_concerns` -> superseded. **Not red by reading.**
- `test_s5_precheck.py`, `test_s5_plan_controller.py`, `test_s5_grown_windows.py`, `test_story_run_*`: no reference to the changed
  functions (grep of `case_concern_lines|concern_report|case_concerns|accepted_rounds|_read_round|_file_concerns|_concern_remark` over
  tests: only `test_brief_pack_s5_plan`, `test_carried_concerns`, `test_critic_rollcall_apply_fixes` (51/51 in the witness),
  `test_s5_plan_grouping`), and no other fixture with a reject cell (grep `| reject |` over fixtures: the two stories above). Low risk.

## Trail

Read: the diff (all 6 files); `critic_rollcall.py:89-165, 236-305, 403-482`; `s5_plan.py:894-896, 1083-1237, 1270-1287`;
`brief_pack.py:1133-1135, 1952, 1993-2063`; `gate_brief.py:2224-2237`; `test_brief_pack_s5_plan.py:600-705`;
`test_carried_concerns.py:30-45, 466-479` (+grep); the N2 card and §3.2 (wave13 spec); the plan critic (N2 hits); the builder report;
`docs/tasks/critic-diff-brief.md`; SIBLING_MAP rows 133/152; fixture stories cart-1, local-1-0108 findings.
Runs (scratchpad probes, read-only on the worktree): `probe.py` (head lengths 400/303/477/235, typo, GLOBAL, SILENT, DECL),
`probe2.py` (real round: `recorded []`, `fixed []`, concerns 6 cases), `probe3.py`/`probe4.py` (cart-1 `[('CC-1', None, False)]`).
Control re-run of the narrow witness: `python -B .../tests/test_s5_plan_grouping.py` -> `=== test_s5_plan_grouping: 158/158 ok ===`
(matches the report). No slow file, no CI, no mutation run.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 brief_pack.case_concern_lines plan-author head: stray edit 'plan:a' (space deleted) changes every brief with concerns; E-N2-7 broken; restore 'plan: a'",
    "B2 brief_pack.case_concern_lines: the still-rejected clause is inserted before _short(text, 400), cutting the instruction tail (apart_reason lost on the plan-author head, 'its cases' on the window head); insert the clause after the cut; row C9b",
    "B3 brief_pack.case_concern_lines receipt-doubt head and exception head say read only approve_with_concerns rows; a still-rejected row reaches S5 with no remark and a misdirecting instruction; add every reviewed row whose verdict is not approving; row C7b",
    "B4 s5_plan._file_concerns: all case-less rows share latest key '' so a later round's unrelated case-less row drops an earlier case-less reject (probe: TS-5 lost); decide case-less rejected elements by latest round with the same plan_row; row C5b"
  ],
  "fixes": [
    "B1 restore the space: 'Answer each in the plan: a `{token}` concern'",
    "B2 build the head without rej, apply _short, then text.replace('({k} ask', '({rej}{k} ask', 1) on the cut text of the three heads with '({k} ask' (not the first parenthesis: that one is concern(s)); test C9b with a 40+ char dispatch id asserts the head holds 'in `apart_reason`' and the clause",
    "B3 both doubt heads: 'read the rows marked `approve_with_concerns` and every reviewed row whose verdict is not an approving one there before you {verb}'; test C7b",
    "B4 in _file_concerns, latest_global = {plan_row: position} over case-less rejected elements; carry a case-less element when latest_global[plan_row] == position; test C5b expects CR-global and CR-global.2",
    "F1 rejected_rows decides by _row_outcome('', row, declared)[0] == 'accepted' instead of re-implementing the approving test (SIBLING_MAP row 152)",
    "optional in the same round: move the pinned-set read and removed-case prefix of _file_concerns into a local closure to cut nesting"
  ],
  "class_completeness": "SIBLING_MAP rows 133 and 152 walked: row 152 (one reader of the critic's word per row) gives F1; row 133 neighbours not touched. Same-artifact sweep of case_concern_lines heads: all four heads checked (B2 on three, judge-in-window head right as is), both doubt heads (B3). Queue Q1 to N1 for current_rejected == [] on a round_word_rule round.",
  "trail": {
    "read": [
      "fv16-n2 diff d5d602d8..5b27a38 (6 files)",
      "ai-packages/qa-factory/scripts/critic_rollcall.py:89-165,236-305,403-482",
      "ai-packages/qa-factory/scripts/s5_plan.py:894-896,1083-1237,1270-1287",
      "ai-packages/qa-factory/scripts/brief_pack.py:1133-1135,1952,1993-2063",
      "ai-packages/qa-factory/scripts/gate_brief.py:2224-2237",
      "ai-packages/qa-factory/scripts/tests/test_brief_pack_s5_plan.py:600-705",
      "ai-packages/qa-factory/scripts/tests/test_carried_concerns.py:30-45,466-479",
      "wave13 docs/tasks/specs/20261114-fv1-6-s4-only-spec.md §3.2 and card N2",
      "wave13 docs/tasks/specs/reviews/20261114-fv1-6-s4-only-plan-critic.md (N2 hits)",
      "fv16-n2 docs/tasks/specs/reports/20261114-fv16-n2-report.md",
      "docs/tasks/critic-diff-brief.md",
      "docs/SIBLING_MAP.md rows 133,152",
      "git diff d5d602d8 origin/main for critic_rollcall.py and brief_pack.py hunks; fv1-28-b1 worktree git diff HEAD hunks"
    ],
    "reruns": [
      {"command": "python -B ai-packages/qa-factory/scripts/tests/test_s5_plan_grouping.py (fv16-n2)", "result": "=== test_s5_plan_grouping: 158/158 ok ==="},
      {"command": "python -B scratchpad/probe.py (case_concern_lines heads, global supersession, silent head)", "result": "plan-author head 400 chars ending 'apart...', 'plan:a'; GLOBAL lacks TS-5; SILENT head names only approve_with_concerns rows"},
      {"command": "python -B scratchpad/probe2.py (real round run-12586-concerns)", "result": "current_rejected recorded [] fixed []; no rejected rows"},
      {"command": "python -B scratchpad/probe4.py (cart-1 concern_report)", "result": "[('CC-1', None, False)], no CR remark"}
    ]
  }
}
```
