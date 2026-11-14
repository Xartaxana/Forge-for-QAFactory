# Topic critic, t-839: K10 pay-down cards K1a, K2, KR (merged into main 9198b363)

Spec: `docs/tasks/specs/20261114-told-before-work-k10-paydown-spec-r2.md` (origin/main). Plan verdict before it: t-821
`reviews/20261114-tbw-k10-paydown-plan-critic.md`. Commits: 9c5db6f1 (K1a), 442ae9de (K2), 9116d50a (KR), merge 9198b363.
Lead decisions taken as given (not re-litigated): F-KR (b), owner's word 14.11 «1, 2 raise the ceiling, 3 treat as evidence»,
merge resolution (census line three-way, automator process ratchet 24117 -> 24116).

## Verdict

- **K1a: GO WITH FIXES.** The printer does what item 1-3 ask. The edges hold and every edge has a row. Fixes: S1 (the carry table is
  ambiguous on the one point K1b's rule turns on), S2 (a source pin), S4 (a second walk over records), S7 (a silent drop on the
  exception path).
- **K2: GO WITH FIXES.** The narrowing matches the code's real firing conditions (checked by running against the real data, below).
  The joins are tests over contract data (AR-1). No row was lost. Fix: S3 (a negative control inside a test; the spec asked for it).
- **KR: GO WITH FIXES.** The raise is named, set to the measured U, and states its price. Fixes: **B1** (the temporary row's removal
  trigger has no carrier and no detector) and S5 (a stale pin message).
- **Topic: GO WITH FIXES.** One blocker (B1) and seven should-fix items. Accepting the topic is the Lead's decision, not mine.

## Blocking finding

**B1. Nothing durable carries or detects removing the temporary code-critic row (K1b), or the spec's queue Q1-Q7.**
- Spec §6 (F-KR (b)) rests its error direction on this: "the batch cannot close with the row standing (a `Остатки` line with
  `узел: K1b`)". No such line or node exists on origin/main:
  - case-insensitive `git grep -i "K1b|F-KR"` over `plans/piles`: 0 hits;
  - `K1b` over `CURRENT_CONTEXT.md` and `docs/tasks` (outside snapshots and specs): 0 hits;
  - positive controls with the same grep shape: `FV2-42` in the live-run-fvf batch 2 file (2 hits); `K1b` in
    `docs/tasks/compact-snapshots/2026-11-14-0800-narrative.md` (3 hits).
- The only carriers are the KR commit message, the changelog fragment, the spec and a compact snapshot. None is a node a later
  session is held to.
- No code detector catches a forgotten K1b. `role_load.native_headroom_problems` (role_load.py 302-346) goes red only when
  `used > headroom and not used <= baseline`. A row that stays above U, or a row for a role that falls under H, is silently green.
  Q6 ("a row above the measured U is red") is not built. The pin `T3a (j)` (test_contract_slices.py 865) fixes the key list, so
  it catches a removal made without a pin edit, never a removal that was forgotten.
- The same gap holds for Q1-Q7. Each was grepped over `plans/piles` with 0 hits: `check_findings`, `run_suite:begin`,
  `exit_gate:digest`, `native_headroom`, `s5_plan_gaps|controller:*`. Positive control with the same shape: `window_first` (hits in
  live-run-fvf). The K1a builder's analog has no carrier either: the copied world builder in `test_red_sandbox_probe.py`
  vs `test_red_sandbox_diagnostic.py`.
- Fix (Lead): open a K1b node, plus nodes for Q1-Q7 and the analog, in the untaken batch of a pile, per D-0044. The proposed home
  is `plans/piles/live-run-fvf/` (its batch 2 already holds the told-before-work FV2-21…44 nodes; if batch 2 is taken, a new
  batch N+1). The K1b node names its exit condition: "native_headroom.qa-code-critic deleted, or lowered with STOP per K1b-E7".
  Optional: build Q6 as the code detector.

## Should-fix findings

**S1 (K1a report → the K1b spec). The carry table is ambiguous for the only two ids `probe_by_code` sites at P.**
- The row for `execution_request:profile` / `:active_dispatch` says "P only (8284/8367/8372 …); L too (4695/6266: a MineRefusal
  from `build_mine_request`)". I spot-checked the sites on 9c5db6f1 and they are true:
  - P printers at 8284, 8367 and 8372;
  - L sites at 4695 and 6266;
  - construction sites at 2698 and 2903 (profile) and 4780 (active_dispatch).
- K1b item 2 proves an id only if it is "carried at P sites ONLY". K1b-E4 says "an id carried at an L site: not proved there".
  Read literally, both ids are also at L, so `PROVED_ROAD["probe_by_code"]` is empty, and the code-critic's K1b green (an E(M)
  value) is at risk. That is the K1b-E7 path.
- Fix: before K1b is dispatched, the Lead decides whether "P only" excludes an id that also prints at an L site. Write the
  decision into the K1b node (B1).

**S2 (K1a). A source pin: `K10p/refuse-no-literal-line` (test_detector_verdict.py, end of `refuse_cases`) reads
`role_cli.py` text for `- [`.**
- This is in the «Пин исходника» row of `docs/TESTING.md` («не пишется»).
- Spec §2 AR-13 asked for a grep in the report, not a test.
- Fix: delete the row; the report grep is enough.

**S3 (K2; a spec defect, not the builder's). `test_k10p_k2` holds `K10p/digest-block-on-page-only/control` and `/negative`, a
doctored copy of the source that must flip the result.**
- This is the «Отрицательный контроль внутри теста» row of `docs/TESTING.md`.
- Spec K2 tests (line 304) required it.
- Fix: delete both rows; the per-role row already asserts the "iff". Or the Lead keeps them with a written reason.

**S4 (K1a; DUPLICATION). `_extra_record_lines` (role_cli.py 79-105 on 9198b363) re-implements the record walk.**
- What it re-implements: a list/tuple filter, a Record filter, and a first-seen dedup by `check`.
- Who already owns that: `detector_verdict._records_in` (flatten) together with the dedup loop of `told_fields` ("the one builder
  of the `told` key", AR-13).
- The two walks differ on nesting: `_records_in` descends into exceptions and nested lists, the new helper does not. So the JSON
  road and the text road can disagree for the same error.
- The cycle is no obstacle: `detector_verdict` can be imported inside the helper, as `stage_joints` already is.
- Severity: queue. Fold it into K1b or a small node.

**S5 (KR). Stale pin message.** test_contract_slices.py 864 still says "its one role over H stands at its named baseline". There
are three rows now. One-line wording fix (inside KR's owned pin range 864-865).

**S6 (class completeness; outside K10 owns). Two more printers drop a `RequestError`'s records.**
- `execution_scheduler.py` 709-710 prints `{"status": "invalid_schedule", "error": str(exc)}` with no `**told_fields(exc)`. Every
  `run_suite.py` JSON printer of the same exception carries it: lines 2811, 2842, 2933 and 2983.
- `onboarding_probe.py` 279-280 returns `[str(exc)]`.
- Neither is named in FV2-43/FV2-44.
- Queue line: "`RequestError` printers without `told_fields` (execution_scheduler 709, onboarding_probe 279) | узел: new, next to
  FV2-44 in live-run-fvf".

**S7 (K1a; low). A silent drop on the exception path.** If `told_line`/`row_for` raises partway through, the helper returns the
lines built so far with no tail line. That is a silent drop, against E5 "never a silent drop". Spec item 2 ("return what was built
so far") prescribes this, so it is a conflict between two parts of the spec, not a builder error. Fix: on an exception, append the
tail line for the records not printed. Queue it with S4.

## The lint findings on main (t-837)

| finding | where | origin | K10? |
|---|---|---|---|
| unused `re` | test_contract_slices.py 1053 | 442ae9de (K2) | yes, a K10 leftover |
| unused `contextlib` | test_detector_verdict.py 867 | 3051b16d (T1r-sites S-1a, t-743) | no |
| f-string without placeholders | test_stage_joints.py 946 | fee19fce (T1r round 2, t-693) | no |

All three are removed by 66d6245b (t-837). How I found them: `pyflakes` on the 9198b363 copies, then `git blame` per line.

## Standing questions

- **Fit to the spec.**
  - K1a items 1-5 and edges E1-E8 are implemented. Each edge has a `K10p/refuse-*` row.
  - The builder flagged one tension, a plain `str` problem with records. No road reaches it today, because `run_guarded` passes a
    str only for a bare ValueError. Correctly reported.
  - K2 items 1-8 are implemented. The predicates match the code's real firing conditions, checked empirically by running
    `handoff`/`handoff_check` on the merged tree:
    - contracts with `findings[].cause`: only `s5-critic-to-automator`;
    - contracts with null outcomes: only `s7-analyst-to-automator`;
    - `TRIED_CONTRACTS`: 10 contracts.
  - The firing code agrees:
    - `_declared_null_outcomes` gives `{}` for contracts without a declaration (handoff_check 1462-1531);
    - `tried_errors` gives `[]` outside `TRIED_CONTRACTS` (1775);
    - `check_findings` (1827-1868) refuses only on `cause == "tooling"`. The case-critic contract has `findings` but no `cause`
      field, so dropping it is right.
  - The S2 relabel is confirmed: controller.py 6919-6944 fires `_plan_rework_rows_problems` only for an automator dispatch.
  - KR items 1-3 are implemented. The measured U matches E(M) within 63 B.
- **The builder's own decisions.** All lean to the safe side: the extra `records-a-dict`/`records-none` rows, and the doc-scribe
  page unlisting (E6). I checked the page: there is no reader of `qa-doc-scribe/handoff-keys-2` outside the K2 report (control:
  `handoff-keys.md` is found in inject-map).
- **Seams.** K1a touches `refuse` and `run_guarded` only; with no records the output is byte-equal (rows). One note on K1a-E6:
  `driver_machine.match_known` reads the WHOLE text, not just the last line. Extra lines could therefore change routing if a row
  sentence carried `REPAIR_MARKER`/`PERSON_MARKER`. Count in stage-joints.json today: 0. No finding; noted for K1b's reviewer.
- **Tests.** The rows would catch the defect each node exists for:
  - the narrowing join is exact-equal against contract data;
  - the positional order is asserted;
  - the cap is tested AT and BEYOND the limit.
  Findings: S2, S3. The functions are long (`refuse_cases` ~75 lines, `test_k10p_k2` ~90 lines), but they are tables of one
  behaviour each: queue, not blocking.
- **DUPLICATION AND CONSISTENCY:** S4. Otherwise none found. What I checked:
  - `told_line` is reused as the one renderer;
  - the test helper `_writers` reads `handoff.index()` (the module's one reader), not `_form_candidates`, as B2 asked;
  - grepped `told_fields|_carry_told|_records_in` over `scripts/`.
  The clone ratchet is the batch's `forge-check` and was not re-run.
- **CODE QUALITY:** `_extra_record_lines` is about 28 lines with at most 3 nesting levels and has no dead branch. S7 is its one
  quality defect. No function over 60 lines in product code.
- **IN-TREE RATCHETS (axis 18), named row by row:**
  - K2 `process_ratchet_tokens`, all 12 down, e.g. automator 24486 -> 24117, code-critic 21571 -> 21174, strategist
    18188 -> 17582 (the full list is in the K2 report; I verified it against `git show` of role-load.json);
  - `COMMON_LAYER_CAP_BYTES` 10750 -> 9500 (down);
  - merge: automator 24117 -> 24116 (down);
  - census `blocking_per_role`: bug-reporter 153 -> 152, case-critic 173 -> 172 (down);
  - KR `native_headroom` raises: automator none -> 79909, code-critic none -> 72828 (TEMPORARY), strategist 46008 -> 53552. All
    three are named in the commit and the changelog, on the owner's word (a Lead-supplied decision; I did not read the session
    carrier of the word).
  - Out-of-scope observation: the merge also brought in the T1r branch's higher `ratchet_tokens` (e.g. automator 20313 -> 26053
    vs main). These come from T1r commits before K10, so naming them belongs to the T1r topic's verdict, not this one. The
    question goes back to the coordinator: is that raise named?
- **ARCHITECTURE (Q10).** Each commit names its AR-n:
  - K1a: AR-13, AR-18, AR-22, AR-23;
  - K2: AR-1, AR-10, AR-11, AR-15, AR-20, AR-23;
  - KR: AR-20.
  Each is kept:
  - AR-22: `records` now has a reader;
  - AR-18: the last line is kept;
  - AR-15: the source keeps blocks for whole-file readers;
  - AR-1: the roles are joined by a test to contract data, with no name list in code.
  AR-10 is kept only on the grounds the spec states. The F-4 (a) clause drop was accepted by the Lead. Nothing touched is left
  unnamed.
- **JUDGMENT (Q11, AR-29/P27):** none found.
  - No check classifies a role's judgment.
  - The K10 commits add no census row and no `blocks_override`, and do not edit the census scan constants.
  - K2's new headings are moved blocks, not new process text: the process tokens went down.
  - The J1 slice-block call is the designer's, accepted by the Lead (declared on the `judgment:` line).
  - The `native_headroom_problems` census row (`shape`/`data`/conductor) arrived with T1r, not K10. Its class holds: it measures
    bytes.
  - Owner's word "3 treat as evidence" (`taken` in probes.jsonl): the three commits do not touch it and build no reader. Consistent.
- **ONE ROAD (Q12, P31):** none found.
  - KR applies the one K10 rule to every role over H, at its measured U.
  - K2's narrowing is one predicate per row, from contract data.
  - K1a prints records for every `run_guarded` CLI alike.
  - What I grepped: `refuse(.*exc` callers over `scripts/*.py`; `RequestError` holders (execution_request, execution_scheduler,
    import_test_receipt, onboarding_probe, run_suite); only `run_guarded` forwards records, and S6 lists the two printers that do
    not.
- **Pair detector (rule 15).** `_writers` scopes both conditions to the SAME index row: `r["from"] in stems and
  predicate(r["contract"])`. Correct.

## Class completeness: SIBLING_MAP axes

- axis 1 policy/roles/journal: n/a (no forge rule changed).
- axis 2 exam instruments: n/a.
- axis 3 release copy: n/a until release (changelog fragments present).
- axis 4 rules/debt/backlog: n/a.
- axis 5 stage twins: covered (the rework row moved to S5/plan, as its sibling `controller:s5_plan_gaps`; other `controller:*`
  rows are Q3, uncarried, see B1).
- axis 6 measurement tools: covered (role_load untouched; U measured by its own reader).
- axes 7-16: n/a (no test identity, story path, git, shell, piles code, dispatch text, transcript, console or JSON reader touched).
- axis 17 detector verdict shape: covered (Record read through `_is_record`/`told_line`; duplication of the `_records_in` walk = S4).
- axis 18 ratchets: covered (named above).
- axes 19-27: n/a.
- axis 28 render site of the row form: n/a (not the `tests[]` row form).
- axes 29-30: n/a.
- axis 31 role carriers: covered (the digest block has one owner, the row; the source keeps the text).
- axis 32 census: queued as Q4 in the spec, but uncarried (B1).
- axis 33: n/a.
- axis 34 one road: covered (above).
- axes 35-37: n/a.
- Same-artifact sweep of K1a (the RequestError printers): S6.

## Queue lines (proposed homes; the nodes are opened by the Lead)

1. K1b node with the exit condition of the code-critic row, and S1's decision | узел: new, live-run-fvf untaken batch (B1).
2. Q1 stand/begin fixture design; Q2 duplicate rows; Q3 scout over `controller:*`; Q4 census `check_findings` roles; Q5 prose pass;
   Q6 K10 tightness detector; Q7 project files by path | узлы: new, live-run-fvf untaken batch (B1).
3. Shared red-sandbox world builder (the K1a analog) | узел: new, live-run-fvf or test-code-quality.
4. S4 + S7 (`_extra_record_lines` reuses `_records_in`; tail line on the exception path) | узел: fold into K1b.
5. S6 `RequestError` printers without `told_fields` | узел: new, next to FV2-44.
6. S2, S3, S5 | a fix round of this topic, or fold into K1b (all in K1b's owned test files or pins, except S2's
   test_detector_verdict.py).

## Trail

Read (origin/main or the named commit):
- the spec r2, whole;
- the plan verdict t-821 (structure, DUPLICATION and CODE QUALITY sections);
- the K1a, K2 and KR reports, whole;
- `docs/tasks/critic-diff-brief.md`, whole;
- `docs/SIBLING_MAP.md` (axis list; axes 17, 18, 28);
- `docs/TESTING.md` 89-105;
- `git show` of 9c5db6f1 (role_cli.py, test_detector_verdict.py, test_import_test_receipt_refusal.py, test_probe_by_code.py,
  test_red_sandbox_probe.py, changelog);
- `git show` of 442ae9de (stage-joints.json, common-rules.md, artifact-contract-plan.md, contract_slices.py, audit_factory.py,
  test_audit_rules.py, test_contract_slices.py, role-load.json, inject-map.json);
- `git show` of 9116d50a (whole);
- the 9198b363 merge message and its `--cc` for role-load.json and judgment-census.json;
- role-load.json at merge-base 01f4e197, 5a1ee009, 9116d50a, 9198b363 and origin/main;
- on the 9198b363 export:
  - handoff_check.py: 1324-1601 (grep), 1700-1725, 1728-1775, 1820-1868;
  - role_load.py 302-346;
  - controller.py 6915-6960;
  - detector_verdict.py: `_records_in`, `told_fields`;
  - stage_joints.py 468-479, 581-608;
  - driver_machine.py 40-70;
  - execution_request.py: `stand_probe_spec` (grep);
  - manual_capture.py 1585-1600;
- `git show 9c5db6f1` greps over probe_by_code.py and red_sandbox.py for the carry-table sites;
- 66d6245b stat.

Commands and results:
- `python -B -I scratchpad/probe_writers.py <9198b363 export>/scripts` -> `cause ['s5-critic-to-automator']`;
  `findings-any ['s4-case-critic-to-designer', 's5-critic-to-automator']` (the case critic without `cause`);
  `nulls ['s7-analyst-to-automator']`; `tried` = the 10 contracts.
- `python -B <export>/scripts/tests/test_contract_slices.py` -> `=== contract slices (markup, generation, freshness, shipped map):
  522/522 ok ===`.
- `python -B <export>/scripts/tests/test_detector_verdict.py` -> `=== test_detector_verdict: 464/464 ok ===`.
- `python -m pyflakes` on the 9198b363 copies of the three lint files -> `test_contract_slices.py:1053 're' imported but unused`;
  `test_detector_verdict.py:867 'contextlib' imported but unused`; `test_stage_joints.py:946 f-string is missing placeholders`.
- `git blame` on those lines -> 442ae9de / 3051b16d / fee19fce.
- The greps for B1 and S6 and the kb negative check, each with its positive control:
  - `advice, not a refusal|final message IS the digest|mended by code` over kb, factory-map and the package (excluding slices):
    only the source, the K10 test and an unrelated test_judge_form line;
  - control: `digest` in kb, 3 files.

Not run: slow files (`test_red_sandbox_probe.py`, `test_probe_by_code.py`, `test_stage_joints.py`, `test_judgment_census.py`,
`test_audit_rules.py`); the batch canon judges them. Ratchets: the `forge-check` layer.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1: the temporary native_headroom.qa-code-critic row (KR) has no carried removal trigger and no detector: no K1b node or Ostatki line in any pile (grep K1b|F-KR over plans/piles: 0, control FV2-42 found); native_headroom_problems never reds a row above U or a role under H; spec queue Q1-Q7 equally uncarried. Lead opens K1b + Q1-Q7 nodes in an untaken batch (proposed live-run-fvf)."
  ],
  "class_completeness": "Axes enumerated (1-37); covered: 5, 6, 17, 18, 31, 34; queued but uncarried: 32 (Q4) and Q3 controller rows, folded into B1; sibling outside owns found: execution_scheduler.py 709 and onboarding_probe.py 279 print a RequestError without told_fields (S6, queue next to FV2-44).",
  "fixes": [
    "B1 open K1b node (exit: code-critic row deleted or lowered with STOP) and Q1-Q7 + red-sandbox world-builder analog as pile nodes",
    "S1 Lead decides before K1b whether an id printed at both P and L sites of probe_by_code counts as P-only (profile, active_dispatch)",
    "S2 delete source pin K10p/refuse-no-literal-line in test_detector_verdict.py",
    "S3 delete negative-control rows K10p/digest-block-on-page-only/control and /negative in test_contract_slices.py (spec defect) or keep with a Lead reason",
    "S4 _extra_record_lines reuses detector_verdict._records_in plus the told_fields dedup (queue, fold into K1b)",
    "S5 test_contract_slices.py 864 message still says one role over H",
    "S6 queue RequestError printers without told_fields: execution_scheduler.py 709-710, onboarding_probe.py 279-280",
    "S7 tail line for unprinted records on the exception path of _extra_record_lines (spec item 2 vs E5)"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261114-told-before-work-k10-paydown-spec-r2.md",
      "docs/tasks/specs/reviews/20261114-tbw-k10-paydown-plan-critic.md",
      "docs/tasks/specs/reports/20261114-k10-paydown-k1a-report.md",
      "docs/tasks/specs/reports/20261114-k10-paydown-k2-report.md",
      "docs/tasks/specs/reports/20261114-k10-paydown-kr-report.md",
      "docs/tasks/critic-diff-brief.md",
      "docs/SIBLING_MAP.md axes 17, 18, 28",
      "docs/TESTING.md 89-105",
      "git show 9c5db6f1, 442ae9de, 9116d50a, 9198b363 (cc for role-load.json, judgment-census.json)",
      "scripts/handoff_check.py 1324-1868 parts, role_load.py 302-346, controller.py 6915-6960, detector_verdict.py _records_in/told_fields, stage_joints.py 468-608, driver_machine.py 40-70 (9198b363 export)"
    ],
    "reruns": [
      {"command": "python -B <9198b363 export>/scripts/tests/test_contract_slices.py", "result": "=== contract slices (markup, generation, freshness, shipped map): 522/522 ok ==="},
      {"command": "python -B <9198b363 export>/scripts/tests/test_detector_verdict.py", "result": "=== test_detector_verdict: 464/464 ok ==="},
      {"command": "python -B -I scratchpad/probe_writers.py <export>/scripts", "result": "cause [s5-critic-to-automator]; nulls [s7-analyst-to-automator]; tried 10 contracts"},
      {"command": "python -m pyflakes on 9198b363 copies of three lint files", "result": "re unused (K2 442ae9de), contextlib unused (3051b16d, not K10), f-string (fee19fce, not K10)"}
    ]
  }
}
```
