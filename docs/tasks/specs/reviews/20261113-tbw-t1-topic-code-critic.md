# Code critic — topic "told before work" T1 revision (T1a, T1b, T1c on T1-0), 13.11.2026

Reviewed: worktree `.claude/worktrees/tbw-t1`, branch `wip/tbw-t1`, head 47d95a1, base 71d7ca8. Spec/DoD:
`docs/tasks/specs/20261113-told-before-work-t1-revision-spec.md` (read whole) + the three Lead decisions in the dispatch.
One pass for the topic (R13-g). Read-only on code.

**Verdict: fit_with_fixes.** The three nodes fit their spec rows, with one hole (K5 cannot go red on the real tree). The ratchet
raises are named and reconcile exactly. The topic may NOT merge to main as it stands: it conflicts with origin/main, and merging main
brings new code into T1a's wider unit road, so the census and the told fixture have to be measured again after the merge (F1). Three
fixes before merge, the rest queued with owners.

## Findings — before merge

**F1 (topic / integrator + T1a-rows re-cut; blocks the merge).** `git merge-tree --write-tree HEAD origin/main` (origin/main = 12317b6,
22c3948 is an ancestor) gives `CONFLICT (content)` in `scripts/stage_joints.py` and `scripts/tests/fixtures/judgment-census.json`;
`test-layers.json` merges on its own.
- `stage_joints.py`: main's 3a49510 carries the same `EXIT_WRAPPERS` fix as T1-0 (423a6a5, which is NOT an ancestor of main), and T1b
  rewrote those lines. Take the topic side of `exit_members` (`stage_joints.py:105-163`).
- `judgment-census.json`: main adds 3 rows (`contract.py::_ref_shape_problems`, `::obligation_ref_problems`,
  `handoff_init.py::clean_purpose`) and sets `conductor` 680 → 681.
- Beyond the textual conflict: main changes 39 package scripts in 129 commits (`git diff --stat 71d7ca8 origin/main`), with 17 added
  lines of refusal shape (my grep for stderr / `sys.exit` / `SystemExit` / `raise` / `refuse|block|deny(`). `role-commands.json` gains
  14 lines, and `guard_pre_tool.py` (where 26 of the 55 `rowless` ids come from) changes by 54 lines. Under T1a's wide `units_of`
  these probably create new A/B units, which would turn C1, the join (1.0) and C3 red. They could also move `rowless` (dense),
  `untold`, and K4's exact unit set (`test_stage_joints.py` "K4/baseline-covers-join"). This is an estimate, not verified; I did not
  run the census on a merged tree.
- Required before the merge:
  - merge origin/main into `wip/tbw-t1` and resolve as above (union of the rows);
  - run the §3.2 probe again on the merged tree;
  - write the rows for any new A/B/C and have the Lead accept them (X3 judgment);
  - take the ratchet from the census test's own totals line, never from 760 + 1 added by hand;
  - regenerate `told-ratchet.json` with step 0;
  - get the join to `units_no_row 0` / `join_share 1.0`;
  - then run BATCH CANON on CI.

**F2 (T1c, `scripts/tests/test_stage_joints.py:814`; before merge).** `check_eq("K5/real: ...", k5_problems(world["unit_roles"], {}, set()), [])`
always gets an empty `unit_rows`, so the real-tree K5 can never be red. This includes the time after T1r lands rows that state a
requirement, and T1r's §4 line does not wire K5. A "live at T1r" check written so that it can never go live is an unknown passing as
green (FR-59). Fix: build `unit_rows` from `REAL["joints"]` rows that satisfy `SJ._states_requirement`, grouped by
`world["ids"][row["check"]]` (or by `<stem>:*` coverage). Today that is still empty (the builder's deviation 4), and it becomes live at
T1r with no further edit. Then `role_set` (`:736`) should call `SJ._row_names` (see Q-d).

**F3 (T1b + T1c, `ai-packages/qa-factory/changelog.d/`; before merge).** Spec §5 axis 3 says "covered M1-M7: a `changelog.d/` fragment
per package node". `git log 71d7ca8..HEAD -- changelog.d/` shows none from T1b or T1c.
- T1b changes shipped data and behaviour: `references/stage-joints.json` goes to schema 2 with renamed keys; `exit_gate.all_errors.own`
  takes full ids; the text-end record carries `exit_gate:text_end_after_handback`.
- T1c adds the K2/K3/K7/E4/E7 and counter checks to `stage_joints.audit` and adds `refusal_registry.CHECK_PASSTHROUGH`.
- One fragment each. A side note: the existing `tbw-t1-rows-v2.md` (from a2c88d8) describes the stderr narrowing, not rows v2. Its
  name is misleading; renaming it is optional.

## Findings — queue (each with its owner; the Lead writes them into «Остатки» / opens the node)

- **Q-a (Q6) runtime.** `told_world` (`test_stage_joints.py:767-787`) runs `CT.units_of` (one full wide scan, `:775`) and then
  `RR.wide_report` (a second full wide scan with `raise_family`, `:776`), plus the `check_ids` subset scan. `told/audit-shape` clears
  `_IDS_CACHE` (`:995`), which forces one more scan. The growth itself is EXPECTED: §3.5a puts the census-side counters in this file.
  It is not FR-31 (the time does not depend on load) and not FR-55 (no role pays for it). The double scan is avoidable cost. The file
  is already in `slow_tests.json` (67.6 s > `slow_over_s` 10), so it is already CI-only and needs no layer or quarantine change. The
  number is stale: it is refreshed by the canon's `selftest.py --slow-tests` diff (`max_drift` 5), not by hand. Risk: it runs in
  `selftest --contracts` (`CONTRACT_TESTS`, `selftest.py:558`) under the default 300 s ceiling; ~150 s local, a loaded runner is
  1.3-1.6x (estimate, not verified). Line: `test_stage_joints told_world scans the package twice: one wide scan (blocking None),
  list records then kept by the census blocking set, feeds units_of and the join | узел: <T10 or a B-155-class node>`.
- **Q-b** `stage_joints.rows_for` returns `[]` when the rows cannot be read (`stage_joints.py:526-528`). That is an unknown read as "no
  requirement" (AR-28). The builder reported it, and T1c only verifies (L2), which fits the Lead's decision. Owner: T3a, the first
  consumer. It returns or refuses with the reason (`(rows, why)`), and its spec names this. Node T3a.
- **Q-c** `refusal_registry.py:1404`: pass-through id records carry `state: "walk_error"` although they are no error. The name lies,
  even though every reader today filters on that state consistently (`refusal_registry.py:1600, 1648`,
  `test_judgment_census.py:237`). Owner: T2, which adds the `refusal` pass-through and should introduce a non-site state for scan
  facts.
- **Q-d duplication** (question 6):
  - `role_set` (`test_stage_joints.py:736`) re-implements T1b's `stage_joints._row_names` (`stage_joints.py:486-491`, the `*` → mapped
    roles, not the conductor rule). Fix together with F2.
  - `measure_untold` (`:723-733`) is a third copy of the `units_of` flip rule (function OR line in spans).
  - `_hand_cards` (`stage_joints.py:1017-1025`) is a second reader of `ahead-cards.json` beside `hooklib.load_ref_json`
    (`brief_pack.py:416`). It needs `(None, why)`, which that reader does not give.
  - `exit_members` (`stage_joints.py:145-158`) and `_passthrough` (`refusal_registry.py:1367-1408`) both read `own`'s literal. Both are
    spec-mandated (§3.4, §3.5), so this is a Lead line for the closing wave, not the builders' fault.
- **Q-e code quality** (question 7): `_row_requirement` `stage_joints.py:836-896` is about 61 lines with 4 nesting levels
  (else→for→if→if). The nested lambda on `:890` hides a read of `role_rules.load`. Split into one helper per row field; queue.
- **Q-f** `covered()` (`test_stage_joints.py:680-683`) lets ANY `<id>.<part>` row cover the id. Parent C14 is narrower: the id is
  exempt only when every site carries a sub-id. The error goes toward green (fewer `rowless`). Today no sub-id rows exist. Owner: T1r.
- **Q-g** `legacy_legs` and `unsited` are ceilings only (`DENSE_COUNTERS = ("hand_cards",)`, `stage_joints.py:986`). The §3.5a table is
  ambiguous, and the builder flagged it (deviation 3). A ceiling that falls without being lowered lets a later rise through silently
  (AR-20 drift). Lead's choice.
- **Q-h** The T1c commit message's axis block says `other axes: n/a, scanner and joints only` (not an enumeration) and has no
  four-question block. Spec §5 carries the full enumeration for M3/M4/M7, so the text exists; noted for calibration, not blocking.
- **Q-i** The conductor-only group is read from the census `note` by regex (`GROUP_RE`). It is a structured fact kept in free text.
  Today it is print-only. Owners: T4/T9a/T9c, who relabel; they should give the census row a field.
- **Q-j** The T1a report says `archive_task.py::cmd_archive` owner is `data`; the file says `intent`, which matches the rows file table
  (`t1a-census-rows.md:1226`). The report text is wrong; the data is right.
- Census witness at 47d95a1: T1c added the row `stage_joints.py::check_ids` and checked it only "by scratch". The census test is slow,
  so it belongs to CI, and the BATCH CANON must show it green.

## Answers 1-8

1. **Fit per node.**
   - **T1a: fit.**
     - The filter runs once before both loops (`test_judgment_census.py:237`, E4).
     - All 17 `WIDE_ROWS` ids are present.
     - Scan constants are untouched: my grep of the 94cfa27 diff for `SCAN_*|UNIT_NAME_RE|JUDGE_CALLS|MEANING_CEILING|blocks_override`
       finds no `-`/`+` line.
     - Rows: 113 A, 1 C, 13 B (4 relabels).
     - The join was 1.0 per the witness.
   - **T1b: fit.**
     - `load_rows` wraps `null_outcomes.load_data` and refuses v1 (`stage_joints.py:419-433`).
     - The kind comes from the producer (r1-r6).
     - Pins are 8/5/27.
     - The seven `own` call sites take full ids and the runtime ids are unchanged (`test_detector_verdict.py:209-217` expects
       `exit_gate:scoped`/`adviser`).
     - The Lead's control was 212/212.
   - **T1c: fit except K5 (F2).** Each gate:
     - K1: audit direction A over the v1 universe (`_direction_a`, `stage_joints.py:955-975`), and the test-side A24/literal leg with
       `rowless` dense.
     - B: the sited set (`sited_ids`, `:313-318`).
     - K3/K7/E4: `_row_requirement`.
     - E7: two rows, `*` included.
     - K2: gated on `contract_slices.requirement_section`.
     - K4/K6: per-unit and `untold` ceilings.
     - K12: `unsited` ≤ 0.
     - L1: counters inside `audit`.

   Does a NEW untold requirement turn red?
   - a new v1-derived key → audit "has no row";
   - a new role-reachable A24 or literal id → `rowless` +1, red naming it;
   - a new bare site in a known unit → `bare` over its baseline;
   - a new role-reachable unit with a bare site → "no baseline row";
   - a new blocking role unit with no told site → `untold` +1;
   - a new row with no site → "stale";
   - all yes, by the variant rows I read. The exception is K5 (F2).

2. **Ratchets.**
   - I recomputed T1a from the JSON diff b355384 → 94cfa27 (`recon.py` in the scratchpad). Every `blocking_per_role` delta = role
     entries of the 113 A rows + roles-after of the 13 B rows − the C row:
     - automator 15+2 = 17;
     - code-critic 18+3 = 21;
     - failure-analyst 21+1 = 22;
     - retro 16+1 = 17;
     - runner 19+1 = 20;
     - doc-scribe 13−1 = 12;
     - conductor 71+9 = 80;
     - the other six equal their A counts.
   - `safety` 82 → 86 = the 4 A rows judged safety. All other keys are unchanged.
   - The +3 hooklib raise is applied to all 13 keys: committed 190 / 153 / 173 / 156 / 160 / 151 / 162 / 170 / 156 / 160 / 152 / 186 /
     760. The dispatch's "173->187, 680->757" are the provisional pre-hooklib numbers; the committed ones are +3 on each. It is named in
     the commit message with its reason. No `blocks_override` was added.
   - T1b: `PINS` detector 8 → 5 (named); new `told_ratchet.hand_cards` 12, `legacy_legs` 9 (named, measured).
   - T1c: census ratchet unchanged (`check_ids` non-blocking); new `unsited` 0; new told fixture `rowless` 55, `untold` 253, 220 units
     (named in the report and the commit's axis-18 line).
   - No silent raise. Joining the new counters to axis 18 and question 9 is queued to T10 by spec §4.
3. **Rename and AR-22.**
   - Producers: `exit_gate.own` and the rows file. Readers: `exit_members`, the pins, `audit`, `_row_problems`, `demand_tokens`,
     `contract_slices._keys_outputs`, `threshold` (retro_numbers through it). All changed in 9bc4711.
   - Case-insensitive `git grep` over `ai-packages` and `tools` for the v1 key forms gives 0 hits outside `test_stage_joints.py`
     (positive control, same pattern: 5 hits in `test_stage_joints.py`, the intended v1 fixtures).
   - The Grep tool with `["'f](exit|detector|window):` -i over the package finds only unrelated hits (`machine_facts.py:804`, "Window:"
     texts, test labels).
   - Readers of the runtime id `exit_gate_text_end`: only the producer and the test.
   - `when_exclusive` still has only a shape reader. Its reader is the T3a/T3b page renderer, per the parent :137 (temporal, named).
4. **L1/L2.**
   - `hand_cards` (`_hand_cards`) and `legacy_legs` (`_legacy_legs`) are computed in `audit` (`stage_joints.py:1112-1118`) and compared
     in `_told_counters`.
   - Unreadable cards → red "cannot be counted", never 0 (row `told/hand-cards-unreadable`).
   - A stored value that is absent or not a count: `_shape_problems` is red (`:620-626`, K10 rows), and `_told_counters` skips it,
     never treats it as 0.
   - An unreadable told fixture → `load_told` gives `(None, why)` and is red.
   - No unknown passes as a number. L2 was verified with no page line, as the Lead decided; the residual is Q-b.
5. **Judgment.** Every new check judges data:
   - K3/K7/E4 (`_row_requirement`): shape/xref — presence, closed carriers, a move id exists, a role-rule id exists;
   - K2 (`_page_leg`): presence/xref;
   - K4/K6/K12, `rowless`, the counters: xref/shape;
   - `CHECK_PASSTHROUGH`: AST shape;
   - census row `check_ids`: xref / conductor / data, non-blocking.

   None classifies a role's text. The census rows T1a adds are shape 101, xref 8, safety 4; no word-list/meaning class, no lowered
   class. The truth of each role label stays X3 (judged by the Lead), with calibration check 41.
6. **Runtime.** See Q-a: the growth is expected, the file is already slow-listed, no layer change is needed. The `slow_tests.json`
   number is refreshed by the canon; a cost-cut node is queued. Not a defect of the test under FR-31.
7. **Duplication T1c vs T1b.** T1c reuses `row_for` (`covered`), `rows_for` / `_row_holds` (`_page_leg`) and `_states_requirement` /
   `_carrier_expected` (`_row_requirement`). The one re-implementation is `role_set` vs `_row_names` (Q-d). The others in Q-d are
   outside T1b.
8. **Merge.** No, not as it stands: see F1. The conflicts are expected and confirmed against 12317b6.

## Standing lines

- **DUPLICATION AND CONSISTENCY:** Q-d. Grepped: `ahead-cards` -i over `scripts/*.py`; `walk_error` -i over `scripts`;
  `_census_blocking` read (`refusal_registry.py:1669-1684`; `told_world` inlines its set because it also needs `units`, a defensible
  choice).
- **CODE QUALITY:** Q-c, Q-e; no dead branch found in the new code.
- **ONE ROAD:** none found. `CHECK_PASSTHROUGH` is one closed row of our own code, read alike for every file. The `check_ids` text
  pre-filter (`detector_verdict` + `with_check(`/`refusal(`) mirrors the scanner's own binding; no language, project or case exclusion.
  Grepped: the T1c diff for language/runner names (none).
- **ARCHITECTURE:**
  - T1a names AR-29/20/13; T1b names AR-13/22/23/28; T1c names AR-10/20/22/28 (each kept, per the answers above).
  - AR-19 (exit producer and reader): main and the topic carry the same unwrap.
- **JUDGMENT:** no judgment moved into code (answer 5).
- **IN-TREE RATCHETS:** answer 2.
- **Hygiene:**
  - `--lang` 2/2 per the T1c witness.
  - No control bytes seen in the diffs read.
- **Class completeness (map):**
  - axis 5: producer/reader in one commit (`own` / `exit_members`, `detector_members` / readers);
  - axis 18: new counters queued to T10 by the spec;
  - axis 32: one scanner (both T1a and T1c read `refusal_registry.sites`);
  - axis 34: one road;
  - analogs outside the owns: Q-b, Q-c, spec §9 (a) `selftest._json_carrier`.

## Trail

- Read:
  - the spec, whole (599 lines);
  - `docs/tasks/critic-diff-brief.md`;
  - `docs/SIBLING_MAP.md` axis 18;
  - the reports T1a (whole), T1c (whole); the T1b and T1-0 reports by their commit messages;
  - `git show` of 94cfa27 (census test diff, fixture), 9bc4711 (`contract_slices`, `exit_gate` diff, message), 47d95a1 (`stage_joints`,
    `refusal_registry`, `test_stage_joints`, `test_refusal_registry` excerpt, data, `test-layers`);
  - `stage_joints.py:98-272, 389-633, 1072-1111`;
  - `refusal_registry.py:1590-1693`;
  - `test_judgment_census.py:75-88` (constants);
  - `selftest.py:100-151, 820-859`;
  - `slow_tests.json` (head, entries);
  - parent spec `:62-81`;
  - rows file grep `cmd_archive`.
- Ran:
  - `git log/diff --stat 71d7ca8..HEAD`;
  - census ratchet and row counts at 71d7ca8 / b355384 / 94cfa27 / b577ad3 / 47d95a1: 1144 / 1145 / 1257 / 1257 / 1258 rows; ratchet
    as in answer 2;
  - `recon.py` (scratchpad) over the b355384 → 94cfa27 and 94cfa27 → 47d95a1 census diffs:
    `A 113 C 1 changed 13`, `A classes {'shape': 101, 'safety': 4, 'xref': 8}`, `A blocks_override []`, per-role deltas as in answer 2;
    `A 1 C 0 changed 0` for T1c;
  - `git merge-tree --write-tree --name-only HEAD origin/main`:
    `CONFLICT (content): Merge conflict in ai-packages/qa-factory/scripts/stage_joints.py`,
    `... judgment-census.json`;
  - `git merge-base --is-ancestor 22c3948 origin/main` → yes; `423a6a5` → NOT in main;
  - the v1-key grep with its positive control (5 hits in `test_stage_joints.py`);
  - control re-run `( cd .../tbw-t1/ai-packages/qa-factory && python -B scripts/tests/test_refusal_registry.py )` →
    `=== test_refusal_registry: 504/504 ok ===` (22.6 s), equal to the T1c witness.
- Not run: `test_stage_joints.py` and `test_judgment_census.py`, both slow-listed and CI-only.
- Questions: none.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "axis 5 covered (own/exit_members, detector_members/readers in one commit); axis 18: every raise named and reconciled, new counters queued to T10 by spec section 4; axis 32 one scanner; axis 34 none found; analogs outside owns queued: rows_for silent empty (T3a), check_id state name (T2), selftest _json_carrier (spec 9a)",
  "fixes": [
    "F1 topic (before merge): merge origin/main 12317b6 into wip/tbw-t1; conflicts stage_joints.py (take topic exit_members, stage_joints.py:105-163) and judgment-census.json (union rows); re-run the 3.2 probe, rows for new A/B/C accepted by Lead, ratchet from the census totals, regenerate told-ratchet.json by step 0, join 1.0, then BATCH CANON",
    "F2 T1c test_stage_joints.py:814 (before merge): K5/real passes an empty unit_rows and can never be red; build unit_rows from REAL rows that state a requirement via world ids, and make role_set (:736) call SJ._row_names",
    "F3 T1b+T1c changelog.d (before merge): add one fragment per node (schema 2 + key rename + own full ids; audit K2/K3/K7/E4/E7/counters + CHECK_PASSTHROUGH) per spec section 5 axis 3",
    "Q-a queue: told_world scans the package twice (test_stage_joints.py:775-776); one shared wide scan; slow_tests.json number refreshed by the canon --slow-tests diff, no layer change",
    "Q-b queue T3a: rows_for returns [] on unreadable rows (stage_joints.py:526-528), AR-28",
    "Q-c queue T2: refusal_registry.py:1404 check_id records typed state walk_error",
    "Q-e queue: _row_requirement stage_joints.py:836-896 over 60 lines, nested lambda :890",
    "Q-f queue T1r: covered() sub-id rule broader than parent C14 (test_stage_joints.py:680-683)",
    "Q-g Lead choice: legacy_legs and unsited ceiling-only (stage_joints.py:986)"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-told-before-work-t1-revision-spec.md",
      "docs/tasks/critic-diff-brief.md",
      "docs/SIBLING_MAP.md axis 18",
      ".claude/worktrees/tbw-t1/docs/tasks/specs/reports/20261113-tbw-t1a-report.md",
      ".claude/worktrees/tbw-t1/docs/tasks/specs/reports/20261113-t1c-report.md",
      "git show 94cfa27 9bc4711 47d95a1 (package diffs and messages)",
      "ai-packages/qa-factory/scripts/stage_joints.py:98-272,389-633,1072-1111",
      "ai-packages/qa-factory/scripts/refusal_registry.py:1590-1693",
      "ai-packages/qa-factory/scripts/tests/test_judgment_census.py:75-88",
      "ai-packages/qa-factory/scripts/selftest.py:100-151,820-859",
      "ai-packages/qa-factory/scripts/slow_tests.json",
      "docs/tasks/specs/20261113-told-before-work-mechanism-spec.md:62-81"
    ],
    "reruns": [
      {"command": "python -B scripts/tests/test_refusal_registry.py (in tbw-t1/ai-packages/qa-factory)", "result": "=== test_refusal_registry: 504/504 ok === (22.6 s)"},
      {"command": "git merge-tree --write-tree --name-only HEAD origin/main", "result": "CONFLICT (content) in scripts/stage_joints.py and scripts/tests/fixtures/judgment-census.json"},
      {"command": "recon.py census diff b355384 -> 94cfa27", "result": "A 113 C 1 changed 13; classes shape 101 safety 4 xref 8; every blocking_per_role delta = A + B-after - C; safety +4"}
    ]
  }
}
```
