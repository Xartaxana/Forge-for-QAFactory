# Critic on PLAN — told-before-work T1 revision (T1-0, T1a-rows, T1a, T1b, T1c)

Plan under review: `docs/tasks/specs/20261113-told-before-work-t1-revision-spec.md` (called "plan", cited `plan:<line>`).
Tree checked: `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1`, tip a2c88d8 (`W\` = its `ai-packages\qa-factory\`).
Reviewer: critic (Opus). This verdict is an INPUT to Lead acceptance; the fork decisions stay with the Lead (rule 6).

**Verdict: fit_with_fixes.** The structure holds: one cause of the 86.5 % join, correctly identified; the rows-file node in the right
place; the fork set mostly right. But four defects block a builder dispatch, because the builder would either get a red tree
or have to invent an approach: B1 (T1a as written creates about 2,300 units, not 113), B2 (T1b's rename leaves the walker's kind
logic undefined), B3 (F9's branch premise is false: P1-v N0 is not on origin/main), B4 (which layer computes the census-filtered
counters). Each can be fixed in the plan text in one designer/Lead fix round; no fork has to be reopened. 4 blocking, 9 non-blocking.

## Blocking findings (fix in the plan before any builder dispatch)

**B1 — T1a creates units from the list transport; the plan's own test row and join argument contradict its algorithm** (plan:177-178,
plan:83-84, plan:140 row `w-append-no-census`). The plan has `units_of` call `sites(root, files, raises=family)` with blocking None and
drop only `walk_error` records. In the scanner, `blocking=None` means *every* function counts for the list transport:
`counted_list` returns True when `blocking is None` (`W\scripts\refusal_registry.py:1427-1428`), and every `.append/.extend/+= [..]`
becomes a `list` site (`:1462-1467`; the test comment says so too, `W\scripts\tests\test_refusal_registry.py:451`). Control run
(trail R1): with blocking None the wide scan gives 10,099 records, 8,257 of them `list`, in 2,649 units. 2,204 of those units have no census
row, so T1a as written would create **2,305 new units** (C1 would demand a row for each), not 113. Non-list sites: 725 units, **113 without
a row**, which matches the report. That makes the plan's §2.1 sentence "the list transport counts only inside units the census already holds" false for
`units_of` itself (that function is where the census blocking set comes from, so the definition is circular). It also makes
`w-append-no-census` unsatisfiable. Fix: T1a drops records whose `transport == "list"` (and `walk_error`) before creating units AND
before flipping `blocks`. State the invariant: "the list transport never creates or flips a census unit; it is bounded by the blocking
set the census computes from the other transports" (POSITIONAL: the filter runs before both loops, `test_judgment_census.py:245-246`
and `:278-281`). With that filter the 1.0 join follows by construction (key 6).

**B2 — the §3.4 rename leaves the walker's kind classification undefined** (plan:141, plan:223, plan:226-229). Four places in
`stage_joints.py` classify a key by its prefix `exit:`/`detector:`/`window:`:
- `_pins` at `W\scripts\stage_joints.py:551-557`;
- `audit`'s counts at `:629`;
- `report.no_detector` at `:635-636`, which uses `detector:{stage}:`;
- the detector-stage rule in `_row_problems` at `:497-498`: "a detector row runs at the stage in its key".

After the rename, detector keys are `<stem>:*` with no common prefix and no stage. The plan's pins (`detector 8 → 5`) therefore count 0, `no_detector`
names every stage, and `:497` silently stops applying (the `startswith("detector:")` test turns false, so nothing goes red). On top of that,
the merged `branch_accounting:*` row runs at S2-S5 and contradicts the rule. T1b's owns list `_shape_problems` and the three
`*_members`, not `_pins`/`Report`, and `_row_problems` belongs to T1c. Fix: (i) `universe()` returns each key's kind
(`exit|detector|window`) beside `where`, and `_pins`/counts read that kind, never the prefix. (ii) The `:497` rule becomes "a detector row's `stages` =
the sorted stages whose non-advice `detectors` list the script" (computed from `detector_members`). (iii) `no_detector` is computed
from `detector_members`' stage list. (iv) T1b owns `_pins`, `Report.no_detector`, and `_row_problems` (the `:497` line only);
`_row_problems` stays T1c's for K3/K7/E4/E7, owned function by function, T1b first. Add test rows `rename/kind-not-prefix` and
`merge/stages-from-model`.

**B3 — F9 rests on a false premise: P1-v N0 is not on origin/main** (plan:23, plan:38-39, plan:340). `git merge-base --is-ancestor` puts
079dc63 (N0) and bea0bb0 (N0 fix round) NOT in `origin/main`, tip be2c988, 17:37. That is the remote-tracking ref as fetched, so it may lag
the remote. `origin/main:scripts/exit_gate.py` has no `def own`/`with_check`; the positive control is a grep of the same file that finds
`errors = scoped_errors` at :1866. `own` stands on `origin/wip/p1v-topic`, `exit_gate.py:1878-1883`, tip c9b2069 19:20, with `PINS` still
`{"exit": 8, ...}` at `test_stage_joints.py:31`, and no `wip/p1v-*` branch changes `exit_members` (`EXIT_SKIP` only, `stage_joints.py:59`). So
F9 (a) ("own branch from origin/main") branches T1-0 from a tree with no wrapper: its real-tree claim 97/111 → 111/111 cannot be shown
there. Analog (ii), "main is red since N0 merged", is not true today. Fix: T1-0 is a fix node of the P1-v topic, on `wip/p1v-topic` or as that batch decides,
so the producer and its reader merge to `main` together (CLAUDE.md rule 10; AR-19). `wip/tbw-t1` then merges that fix before
T1b. The Lead also checks whether the P1-v batch is frozen and takes the node there (PROJECT.md «Командная работа» п. 2). That
decision belongs to the Lead and the P1-v batch owner. The `defect_found` with `ref` = N0's accepted task stays right.

**B4 — T1c puts census-filtered counters in `audit`, against 0.12/FR-44 of the plan itself** (plan:142, plan:253, plan:257).
`bare`/`tagged`/`untold` are counted "per (file, function) of role-reachable units", and `rowless` counts "role-reachable A24 ids +
literal ids". Both need the census role filter, which the plan itself puts on the test side (plan:28, 0.12; parent §2.5). Yet T1c's
`_ratchet`/`Report` in `stage_joints.audit` is to carry "the five counters", and `_direction_a` is to exempt "ids counted by `rowless`
(test-side)". The audit cannot know which ids the test counted: it sees one number in `told_ratchet.rowless`. A builder must
invent the split. Fix: one table per counter, saying where it is COMPUTED and where it is COMPARED. Proposal: `unsited`,
`hand_cards`, `legacy_legs` are computed and compared in `audit`. `bare`/`tagged`/`untold`/`rowless` are computed and compared in
`test_stage_joints.py`, and `audit` checks only their shape (present, int ≥ 0). Literal ids follow one road: either all of them go to the test-side leg with
`rowless`, and the audit universe then holds v1-derived keys only, or all stay in the audit with no exemption. Pick one; the first
fits F6 (a).

## Non-blocking findings (fix in the same plan round)

**N1 — the flip list B misses the span rule** (plan:168-170). The step-A command takes B from the join, which keys by the record's outermost
function. `units_of` also flips a NESTED unit whose span holds a site line (`test_judgment_census.py:278-281`). Control R1: 11 units
flip under the `units_of` rule, 10 by the join; the missing one is `project_decisions.py::run`. The per-role reconciliation would be
off by that unit's roles, and C3 is dense, so the builder sees red with no stated move. Fix: compute B as
`{k in units_of_old : not blocks_old(k) and some non-list wide record r in k's file has r.function == k[1] or r.line in k's spans}`.
That is a pure read over the old `units_of` and `sites(...)`.

**N2 — a `<script>` stage unit turns stale, and its refs move** (plan:171, plan:86-88). `units_of` adds `(script, "<script>")` only for
a detector script with no function units (`test_judgment_census.py:254-264`). Control R2: `check_coverage.py::<script>` (roles
`["qa-doc-scribe"]`) is the one census `<script>` row whose file gains wide non-list sites. After T1a its row is stale (C1, `:313-316`),
and the new function units must carry `ref: stages.json:S8/qa-doc-scribe` (C1 ref check, `:317-325`). Fix: the rows file gets a `ref`
column and a list C (rows removed/moved). The reconciliation becomes `+A +B_flips ± relabels − |C rows naming r|`.

**N3 — the CHECK_PASSTHROUGH scope is unspecified, and a same-name call exists** (plan:258-259). The nested `own` is defined inside
`all_errors`. The wide scan keys a record by `stack[0]` (`refusal_registry.py:1380, 1413, 1432`), which is the outermost `all_errors`, never
`own`. So the key `("exit_gate.py", "own")` is never what the walk sees unless the rule reads the innermost function. And
`exit_gate.py:1100` calls `dispatch_identity.own(...)`, a different `own` with one positional argument; `_callee` returns attributes too
(`refusal_registry.py:1273-1278`). Fix: the passthrough is matched by the INNERMOST enclosing def, and its call sites are bare-name
calls only (`ast.Name`, in the scope where that def is visible). Add test rows `pass/attr-call-same-name-ignored` and `pass/nested-def`.

**N4 — T1b owns `selftest.py:722` but not the test that judges it** (plan:141). `test_selftest_slow_tests.py:452-473` writes a
schema-less `stage-joints.json` into a patched `PLUGIN_ROOT` and expects `test_j.py` among `gate_named_files`. If `:722` reads
through a v2-only `load_rows`, or through `load_rows` bound to the module `DATA` and not to selftest's patched root, that test goes red,
and the test is not in T1b's owns (it is a keep `table` row, `test-layers.json:5073`). Fix: `load_rows(path)` takes the path. Either
the name collector keeps a tolerant read of `joints[].joint.test`, with a stated AR-28 behaviour for an unreadable file (named, never
an empty set read as "no tests"), or T1b owns that test's fixture (schema 2). The plan's own trail says `selftest.py:722` was not read
(plan:364).

**N5 — "six call sites" is wrong: `own` has seven** (plan:23 "six families", plan:141, plan:226): `exit_gate.py:1883, 1884` (twice), `1885, 1887, 1891,
1901`. The families are six, the calls seven (`adviser` is called twice). With F7 (a) the literal `exit_gate:adviser` enters the literal-id
universe and has no row (no `adviser` row in `stage-joints.json:9-1117`). Say whether it is counted in `rowless` (by B4's choice) or
gets a row in T1r. Also add the edge for an `own` call with a non-literal second argument after T1b: a walk error.

**N6 — `legacy_legs`/`hand_cards`: "a different number is a stop" contradicts 0.18** (plan:141 vs plan:34). 0.18 calls 9 an estimate that
"T1c prints"; the T1b row writes it and stops on difference. A measured baseline that differs from an estimate is not a defect. Fix: T1b prints and writes the
measured number; a difference from 12/9 is a report line with the list, not a stop.

**N7 — the witness claim about `test_refusal_registry.py`** (plan:140: "it imports `units_of` through `--wide`") is false. A grep for
`units_of|_census_blocking|--wide` in that file has no hit; the positive control, same file, finds `wide_report` at :367-372 and `raise_family(...wide=True)` at
:390. The test calls `wide_report` with an explicit `blocking`. It is still a fair witness, because T1a changes the scanner's caller set,
but the reason is wrong. Add `refusal_registry.py --sites --wide --census ...` (the join command, already listed) as the real check of
`_census_blocking`.

**N8 — base drift before step A** (plan:182-183, plan:144). If `wip/tbw-t1` merges the P1-v fix or the topic (B3) AFTER step A, the
wide units change and T1a's step 0 stops, so the rows file would be drafted twice. Fix: the sequence says "fix the base of `wip/tbw-t1`
(T1-0 merged in) → step A → rows draft". T1a and T1b can also run in parallel (disjoint files except census rows, merge order T1a
first), so the 2-writer cap allows T1a ∥ T1b once T1-0 is in.

**N9 — reader choice for `load_rows`** (plan:312 axis 16 "through `hooklib.read_json`"). Today `audit`/`threshold`/`main` read through
`null_outcomes.load_data` (`stage_joints.py:604, 646, 668`), and the K10 rows pin its texts ("stage-joints.json cannot be read",
`test_stage_joints.py:242-257`). Changing readers changes those texts. Fix: `load_rows` wraps `null_outcomes.load_data` and adds the
schema test, or the plan names the switch and its text rows.

## Answers to the keys

**1. Facts by trail.** Confirmed:
- 0.1: 113 / 836 / 86.5 % read verbatim in the report (`reports/20261113-tbw-t1-report.md:18-22`). Independently, 113 rowless non-list units (R1).
- 0.2: `units_of` without `wide`, `test_judgment_census.py:223-224`, u3 at `:245-246`, stale at `:313-316`.
- 0.3: `_c3` at `:367-372` (per role, `conductor` included, through `roles_of` `:100-102`); dense at `:392-394`.
- 0.4: flip at `:278-281`.
- 0.7: `own` at `exit_gate.py:1878-1887, 1891, 1901`, `exit_members` at `stage_joints.py:100-105`, PINS at `test_stage_joints.py:31`.
- 0.8: f-string at `exit_gate.py:1881`.
- 0.9: `exit_gate.py:452-478`, text-end at `:1059`, `check_id` at `detector_verdict.py:116-127`.
- 0.10: 8/8/27 keys, `branch_accounting` at `stage-joints.json:398, 447, 497, 548`.
- 0.15: `walk_error` at `refusal_registry.py:1358-1360, 1370`, filtered at `:1597`, `_census_blocking` at `:1618-1626`.
- 0.17: `scenario_walk.py:860-863`.
- Parent: `:80-81`, `:356-357`, `:390`, `:767-769` as quoted.

Corrected:
- 0.7 / analog (ii) / F9: N0 is not on origin/main (B3).
- "six call sites" (N5).
- The `test_refusal_registry` witness reason (N7).
- §2.1's list-transport sentence (B1).

Not re-verified: 0.13's `role-commands.json` count (31 `"roles"` lines, a count only), 0.14, 0.18 (an estimate by the plan's own label).

**2. Architecture and principles.**
- AR-29/P27: kept. Roles are a designer judgment accepted by the Lead (X3), never defaulted.
- AR-20: kept on condition of N1/N2. As written, the reconciliation can mismatch C3 with no stated move.
- AR-13: kept for `units_of` (the one scanner). Kept for `stage_joints.json` with N4/N9. `check_ids` reads the scanner's records, so there is no second walk.
- AR-14: kept by sequencing (census T1a → T1b/T1c; `stage-joints.json` T1b → T1c → T1r).
- AR-22: kept, except `told_ratchet.rowless`, whose reader is undefined until B4.
- AR-28: kept for `audit`/`main`/`threshold`. At risk in `selftest.gate_named_files` (N4).
- AR-10: kept. A24/literal ids are counted, not silent (F6 (a)), once B4 says where.
- AR-19 / axis 5: the plan names it, but B3 puts the twin fix on the wrong branch.
- AR-1: kept. `EXIT_WRAPPERS`/`CHECK_PASSTHROUGH` are scanner vocabulary of our own code, not project variety (AR-1's carriers are P2/FR-13). The precedents are `EXIT_SKIP` (`stage_joints.py:59`) and `SCAN_ROOT`, a code constant on purpose (`test_judgment_census.py:12-14`).
- FR-38: untouched in T1 (T10).
- FR-44: kept for the census, broken by T1c's audit counters (B4).
- P31: kept. One namespace (F5 (a)), one passthrough mechanism T2 reuses, units by transport for every script.
- FR-54 / sibling map: axis block present; axis 5 is affected by B3.

**3. Feasibility.**
- T1-0: executable (six K9 rows are concrete), once on the right branch (B3).
- T1a-rows: correctly placed as a designer draft after a Lead deterministic run. It needs `ref` and list C (N2) and the span-correct B (N1).
- T1a: not executable as written (B1).
- T1b: not executable as written (B2, N4).
- T1c: not executable as written (B4, N3).
- Owns: disjoint except `judgment-census.json` (T1a whole rows; T1b/T1c new-unit rows) and `stage_joints.py`/`test_stage_joints.py`, shared by T1-0/T1b/T1c in sequence. `_row_problems` is shared by T1b (B2) and T1c and must be owned function by function.
- Parallel: T1-0 ∥ step A only after the base question (N8). T1a ∥ T1b after T1-0.

**4. Provisional fork decisions.**
- **F1 (a) + F2 (a): right.** The roles are judgment (P27), drafted per unit with evidence and accepted a tier above. The data-first rule errs toward over-labelling, which is the safe direction for told work, and the dense C3 makes the cost visible. One node, because the rows arrive pre-judged; the t-346 chain machinery would be dead weight (0.16, `test_judgment_census.py:755`). Conditions: the rows file adds `ref` and list C (N2), and B is computed by the `units_of` rule (N1).
- **F4 (a): right, with B2.** Coarse `<stem>:*` keys and the `branch_accounting` merge are sound. But the kind and stage logic must be specified (B2), and `*` must be stated as the one wildcard form, rows only (plan already: "never at a call").
- **F6 (a): right in direction.** The census filter is test-side (FR-44), and direction B against the whole registry is correct. It needs B4's computed/compared table, and N5's choice for `exit_gate:adviser`.
- **F8 (c): right.** The per-id rows "the site writes this id" persist as regression rows, so a gone-after-sited id goes red at once without a `sited` flag, and the rows-first cut stays. Keep them as table/variant rows per node (docs/TESTING.md), not one test function per id.
- **Other forks on the draft's recommendation.** F3 (a) right. F5 (a) right. F7 (a) right with N3. **F9 (a) wrong** (B3); the right option is T1-0 on the P1-v topic, a call for the Lead and the P1-v batch owner.
- Nothing here needs the owner.

**5. Edges.**
- Stated and decided correctly: T1-0 E1-E4 and TEMPORAL; T1a E2, E3, E5, E7-E9 and TEMPORAL (rows born before T1a, step-0 stop); T1b E1 TEMPORAL (schema 2 born in T1b, v1 refused, `threshold` default None, matching `stage_joints.py:641-649` and `test_retro_numbers.py:211-221`), E3, E5; T1c E1-E5, including the POSITIONAL fallback-before-lookup.
- Wrong or missing:
  - T1a POSITIONAL list filter (B1).
  - The nested-span flip (N1).
  - The stage-unit stale row (N2).
  - Kind after rename (B2).
  - Passthrough scope and same-name call (N3).
  - The tolerant read in the selftest collector (N4).
  - The non-literal second argument of `own` (N5).
  - The estimate-vs-measured stop (N6).
- Conflicting pair "join 100 %" vs "no new blocking unit": resolved correctly by the named exception (plan:92-93).

**6. Stop rule.** With B1's filter, the census join reaches 1.0 by construction. Every non-list wide unit becomes a census unit, and list sites
count only in blocking units, which all carry rows (C1). The proof is the verbatim join command (plan:211, `units_no_row 0`,
`join_share 1.0`), which is a real witness. It does not hide units: they move from "rowless" into C1-demanded rows whose truth
rests on X3 (Lead acceptance with evidence per unit). The A24/literal told-row gap is a different universe (stage-joints rows,
not census), counted densely in `rowless` with the ids printed. Without B1, T1a goes red at C1 with about 2,200 rowless units.

**7. Cost.**
- T1 adds 0 tokens to a role's dispatch. Pages stay byte-identical (plan E5), and `rows_for` returns no row until T1r writes sentences (Q4).
- Indirect cost: F1 (a)'s over-labelling grows `role_reachable_units` (168 today), and so the K4-K6 told work that T3/T7 will put in front of roles. T1c step 0 should print the before/after.
- Told twice, a risk for T1r: under F3 (a), `exit_gate:detector_errors`/`witness_errors` rows coexist with the producers' `<stem>:*` rows. If T1r gives both a requirement sentence, one finding is told twice. T1r should keep sentences on the producer rows only, and the aggregator rows sentence-less (told by v1 legs).

## Standing questions (plan gate)
- DUPLICATION AND CONSISTENCY: one item, N9. `load_rows` should wrap the existing `null_outcomes.load_data`, not a second JSON reader. Otherwise none found: grep of `stage-joints` readers over `W\scripts` (contract_slices.py:490, selftest.py:722, stage_joints.py:604/646/668, retro via `threshold`). `check_ids` reuses the scanner's records (no second AST walk).
- CODE QUALITY: none at plan level. The new code is small branches and constants. Watch `_direction_a`, which gains three exemption rules (E1, E2, E5) and should stay under roughly 60 lines.
- ONE ROAD (P31): none found. The units road is the same for every script and transport. `CHECK_PASSTHROUGH` is one mechanism with T2 adding a line, not a per-file exception. Grep: plan §3-§6 for "except", "unchanged", "not for"; the only exclusions are the list transport (B1, a positional rule for all files) and fallback ids (parent N13).

## Trail
Read:
- the plan (whole);
- the report `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1\docs\tasks\specs\reports\20261113-tbw-t1-report.md` (whole);
- `W\scripts\tests\test_judgment_census.py:1-420`;
- `W\scripts\refusal_registry.py:1-110, 1221-1516, 1517-1656, 1745-1804`;
- `W\scripts\exit_gate.py:445-484, 1870-1909`, plus grep `own(|errors =`;
- `W\scripts\stage_joints.py:40-129, 480-559, 594-653`, plus grep;
- `W\scripts\detector_verdict.py:86-151`;
- `W\references\stage-joints.json` grep `"check": "`;
- `W\scripts\tests\test_stage_joints.py` grep;
- `W\scripts\selftest.py:700-727`;
- `W\scripts\tests\test_selftest_slow_tests.py:435-474`;
- `W\scripts\tests\test_retro_numbers.py:170-221`;
- `W\scripts\tests\scenario_walk.py:860-865`;
- `W\scripts\tests\test-layers.json:5070-5080`;
- `W\design\architecture.md` AR-1;
- the parent spec `:79-82, 355-358, 390, 763-770`;
- `docs/tasks/critic-diff-brief.md:44-101`.

Control runs (pure reads, scratchpad scripts, verbatim):
- R1 `python -B ...\scratchpad\t1probe.py`:
  `wide records (blocking=None): 10099 list: 8257 non-list: 1842` /
  `units from list sites: 2649 of them without census row: 2204` /
  `units from non-list sites: 725 without row: 113` /
  `new units (all wide) not in old units_of: 2305` /
  `flip set by units_of rule: 11 by join (function key only): 10 rule-only: [('project_decisions.py', 'run')]`
- R2 `python -B ...\scratchpad\t1probe2.py`:
  `<script> rows: 1` /
  `<script> rows whose file gains a wide non-list site (row turns stale, refs move): [('check_coverage.py', '<script>', ['qa-doc-scribe'])]`
- R3 `git merge-base --is-ancestor` for 079dc63, bea0bb0, c973298, ba88a80 vs origin/main: all `NOT in origin/main`; `origin/main` 2026-11-13 17:37 be2c988.
- R4 `git show origin/main:.../exit_gate.py | grep "def own|with_check"`: no hit; control grep `errors = scoped_errors` → `1866`. `origin/wip/p1v-topic`: `1878: def own`, PINS line 31 unchanged; no `EXIT_WRAPPERS` on `wip/p1v-{topic,fix,n5,n0}`.
- R5 grep `units_of|_census_blocking|--wide` in `test_refusal_registry.py`: no hit; control `check_of|wide_report|wide=True|census` → `367, 372, 390-392, 451, 565`.

No test file was run.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 T1a units_of with blocking=None creates units from the list transport (refusal_registry.py:1427-1428, 1462-1467): 2305 new units, not 113; filter transport list before unit creation and flip (plan:177-178, 83-84, row w-append-no-census)",
    "B2 the 3.4 rename leaves kind classification undefined: _pins stage_joints.py:551-557, audit counts :629, no_detector :635-636, detector stage rule :497-498 read the key prefix; universe must return the kind; T1b owns _pins/Report/_row_problems:497",
    "B3 F9 premise false: P1-v N0 (079dc63, bea0bb0) is not on origin/main; own wrapper lives on wip/p1v-topic exit_gate.py:1878; T1-0 belongs to the P1-v topic so producer and reader merge together",
    "B4 T1c puts census-filtered counters (bare/tagged/untold/rowless) in stage_joints.audit, against FR-44 and plan 0.12; state per counter where it is computed and compared; one road for literal ids"
  ],
  "fixes": [
    "B1: units_of drops transport list and walk_error records before both the u3 loop (test_judgment_census.py:245-246) and the flip loop (:278-281); invariant stated",
    "B2: universe returns kind per key; _pins and counts read it; detector stages = model stages listing the script; no_detector from detector_members; rows rename/kind-not-prefix, merge/stages-from-model",
    "B3: T1-0 on wip/p1v-topic (Lead and P1-v batch owner decide); wip/tbw-t1 merges it before step A and T1b; drop analog (ii)",
    "B4: table counter -> computed/compared layer; audit checks only shape of test-side counters; literal ids all test-side or all audit",
    "N1: list B computed by the units_of rule (function or span), catches project_decisions.py::run",
    "N2: rows file gains a ref column and list C (check_coverage.py::<script> stale, stages.json:S8/qa-doc-scribe ref moves); reconciliation minus C",
    "N3: CHECK_PASSTHROUGH matched by innermost def; call sites bare-name only (exit_gate.py:1100 dispatch_identity.own is not one); two test rows",
    "N4: load_rows(path); selftest.py:722 keeps a tolerant named read or T1b owns test_selftest_slow_tests.py fixture (lines 452-473)",
    "N5: seven own call sites, not six; exit_gate:adviser literal has no row - say rowless or T1r row; non-literal second argument edge",
    "N6: hand_cards/legacy_legs measured and written; a difference from 12/9 is a report line, not a stop",
    "N7: correct the test_refusal_registry witness reason; the join command checks _census_blocking",
    "N8: sequence base fix -> step A -> rows draft; T1a parallel to T1b after T1-0",
    "N9: load_rows wraps null_outcomes.load_data (stage_joints.py:604,646,668) or names the reader switch and K10 text rows"
  ],
  "class_completeness": "Class 1, producer changed without its reader (axis 5): exit_members is the one reader of all_errors families; window_members and detector_members have no wrapper (n/a, plan 3.1). Same class, new instance: selftest.py:722 and test_selftest_slow_tests.py as readers of stage-joints.json under v2 (N4); retro threshold checked, holds. Class 2, a key-prefix kind read after a rename: all four sites in stage_joints.py enumerated (B2); test_stage_joints.py:70-74 window prefix rows are T1b-owned tests. Class 3, a scanner switch that widens scope (blocking None): units_of and _census_blocking are the two callers (B1); test_refusal_registry passes blocking explicitly.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-told-before-work-t1-revision-spec.md (whole)",
      ".claude/worktrees/tbw-t1/docs/tasks/specs/reports/20261113-tbw-t1-report.md (whole)",
      "W/scripts/tests/test_judgment_census.py:1-420",
      "W/scripts/refusal_registry.py:1-110,1221-1656,1745-1804",
      "W/scripts/exit_gate.py:445-484,1870-1909 + grep own/errors",
      "W/scripts/stage_joints.py:40-129,480-559,594-653 + grep",
      "W/scripts/detector_verdict.py:86-151",
      "W/references/stage-joints.json grep check keys",
      "W/scripts/selftest.py:700-727",
      "W/scripts/tests/test_selftest_slow_tests.py:435-474",
      "W/scripts/tests/test_retro_numbers.py:170-221",
      "W/scripts/tests/scenario_walk.py:860-865",
      "W/scripts/tests/test-layers.json:5070-5080",
      "parent spec :79-82,355-358,390,763-770",
      "docs/tasks/critic-diff-brief.md:44-101"
    ],
    "reruns": [
      {"command": "python -B scratchpad/t1probe.py (wide sites blocking None vs census, flip sets)", "result": "list 8257 records in 2649 units, 2204 rowless; non-list 725 units, 113 rowless; 2305 new units; flips 11 by rule vs 10 by join, rule-only project_decisions.py::run"},
      {"command": "python -B scratchpad/t1probe2.py (stage script rows)", "result": "1 <script> row; check_coverage.py::<script> gains wide sites and turns stale"},
      {"command": "git merge-base --is-ancestor 079dc63|bea0bb0|c973298|ba88a80 origin/main", "result": "all NOT in origin/main (be2c988, 17:37)"},
      {"command": "git show origin/main:exit_gate.py | grep def own|with_check (control: errors = scoped_errors)", "result": "no hit; control hit line 1866; p1v-topic has def own at 1878"},
      {"command": "grep units_of|_census_blocking|--wide test_refusal_registry.py (control check_of|wide_report)", "result": "no hit; control hits 367,372,390-392,451,565"}
    ]
  }
}
```
