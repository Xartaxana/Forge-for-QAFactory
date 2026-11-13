# Told-before-work — revision of node T1 (rows v2 + reader + gate) — DESIGNER DRAFT, fix round 1

Status: designer DRAFT for Lead acceptance (13.11.2026), fix round 1 after the critic-on-plan verdict
`docs/tasks/specs/reviews/20261113-told-before-work-t1-revision-plan-critic.md` (fit_with_fixes; B1-B4, N1-N9). Not a dispatch.
Parent: `docs/tasks/specs/20261113-told-before-work-mechanism-spec.md` ("parent"; T1 row `:390`, T0 gate `:754-773`). It replaces
the parent's T1 row by five nodes (T1-0, T1a-rows, T1a, T1b, T1c), answers the first builder's Q1-Q6
(`.claude/worktrees/tbw-t1/docs/tasks/specs/reports/20261113-tbw-t1-report.md:24-49`), and names what changes for T1r/T2/T3a/T3b/T8.
The 100 % join rule (parent `:768`) is not reopened: §2.1 says what makes it reachable and §3.2 how the count is proved.
Fork decisions of the Lead (binding, 13.11): F1 + F2 = (a), the rows file with a `ref` column and lists B and C by the `units_of`
rule; F3 (a); F4 (a) with the B2 definition (§3.4a); F5 (a); F6 (a) with B4 (§3.5a); F7 (a) with N3; F8 (c); F9 (a) dropped (B3).
Forks still open: §6 (F9', F10, F11), each with a recommendation; every node is executable on the recommendations.

Paths (every `owns:` cell in §3 spells the full absolute path):
- `W\` = `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1\ai-packages\qa-factory\` — integration tree, branch `wip/tbw-t1`, tip a2c88d8
  today (holds P1-v N0 through the merge c6418bd of `wip/p1v-n0`, T0-gate change 1 and `check_of` with its census row).
- `P\` = `C:\QAFactory\forge-repo\.claude\worktrees\p1v-t10\ai-packages\qa-factory\` — T1-0, branch `wip/p1v-t10` from 71d7ca8. Born at
  the T1-0 dispatch (the Lead creates it: `git -C C:\QAFactory\forge-repo worktree add -b wip/p1v-t10 .claude/worktrees/p1v-t10 71d7ca8`,
  push first, rule 12).
- `Wa\` = `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1a\ai-packages\qa-factory\` — T1a, branch `wip/tbw-t1a` from base B1 (§3.0).
- `Wb\` = `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1b\ai-packages\qa-factory\` — T1b, branch `wip/tbw-t1b` from base B1.
- T1c works in `W\` after T1a and T1b are merged into `wip/tbw-t1`.

The designer had no shell in either round: numbers are READ from carriers (the report, the critic's control runs R1-R5, files, git
reflogs); none was measured by the designer.

## 0. Facts read (each changes the brief or the parent)

| # | Fact, with its carrier | Consequence |
|---|---|---|
| 0.1 | The join, verbatim (report `:16-20`), command `python -B scripts/refusal_registry.py --sites --wide --census scripts/tests/fixtures/judgment-census.json --json` (run in `W\`): BEFORE (T0, c973298) `units 848, units_with_row 732, units_no_row 116, join_share 0.8632`; AFTER T0-gate change 1 (a2c88d8) `sites 3030, units 836, units_with_row 723, units_no_row 113, join_share 0.8648…, role_reachable_units 168, conductor_only_units 555, role_reachable_sites 687, stderr-print+return 241, walk_errors 0, check_arg_errors 1`. All 113 rowless units exist only through the new transports (report `:21-22`) | the gap is one cause: the census scan does not create units from the wide transports (0.2) |
| 0.2 | `test_judgment_census.units_of` builds units from `refusal_registry.sites(..., raises=raise_family(...))` WITHOUT `wide=True` (`W\scripts\tests\test_judgment_census.py:223-224`), creates u3 units from those sites (`:245-246`), flips `blocks` by them (`:278-281`), and reports every row whose unit it did not create as `stale row` (`:313-316`) | T1 needs `test_judgment_census.py` and `judgment-census.json` in its owns (the parent T1 row `:390` lists neither) |
| 0.2a | (B1) In the wide scan `blocking=None` means EVERY function counts for the list transport: `counted_list` returns True when `blocking is None` (`W\scripts\refusal_registry.py:1427-1428`), and every `.append/.extend` with an argument and every `+= [..]` becomes a `transport: "list"` record (`:1462-1467`). Critic control R1 at a2c88d8: with blocking None, 10,099 records, 8,257 of them `list`, in 2,649 units, 2,204 of them rowless; all wide units not in today's `units_of`: 2,305; NON-list units: 725, of them 113 rowless | `units_of` must drop `transport == "list"` records (and `walk_error` records) before it creates units AND before it flips `blocks`. Then the new units are exactly the 113 non-list rowless units (at a2c88d8) — §2.1, §3.2 |
| 0.3 | `_c3` adds 1 to `blocking_per_role.<r>` for every role `r` on the row of every effectively-blocking unit (`:367-372`); the ratchet is dense: a count below its ceiling is red too (`:392-394`) | every new blocking row raises each role it names by exactly 1 |
| 0.4 | (N1) The flip rule of `units_of` is "a site's `function` equals the unit's name, OR the site's line is inside one of the unit's spans" (`:280`); the join keys by the record's outermost function only. Critic R1: 11 units flip by the `units_of` rule, 10 by the join key; the one missing is `project_decisions.py::run` | list B is computed by the `units_of` rule (§3.2 probe), never from the join |
| 0.4a | (N2) `units_of` adds `(script, "<script>")` only for a `detectors` script with no function unit (`:254-264`) and puts `stages.json:<S>/<role>` tokens in every unit of that script's `refs`; C1 demands each token in the row's `ref` (`:317-325`). Critic R2: `check_coverage.py::<script>` (roles `["qa-doc-scribe"]`) is the one `<script>` row whose file gains wide non-list sites | after T1a that row is stale (list C) and the new function units of that file need `ref: stages.json:S8/qa-doc-scribe`: the rows file gets a `ref` column and a list C |
| 0.5 | Parent contradiction: §1.2 "a new unit is class `shape`/`xref`, owner `data`, roles `["conductor"]`" (`:80-81`) vs the T0 gate "the rowless units … roles do reach" (`:768`) | decided by the Lead: F1 (a) |
| 0.6 | Parent DoD line for EVERY package node: "census: no new blocking unit" (`:356-357`) | conflicts with T1a by construction; T1a carries the named exception (§2.1) |
| 0.7 | P1-v N0 wraps six families in a nested `own(records, family)` returning `DV.with_check(r, f"exit_gate:{family}")`; `own` is CALLED SEVEN times (`exit_gate.py:1883, 1884` twice, `1885, 1887, 1891, 1901`; `adviser` twice; read on `P1-v n4fix` tree `C:\QAFactory\forge-repo\.claude\worktrees\p1v-n4fix\ai-packages\qa-factory\scripts\exit_gate.py`, same lines on `W\`). `stage_joints.exit_members` keys every bare-name call leaf of `errors = …` (`stage_joints.py:100-105`, `EXIT_SKIP` `:59`), so it sees `exit:own`; `test_stage_joints.py` pins `{"exit": 8, …}` (`:31`) and is red 97/111 on `W\` (report `:35-36, 73`) | producer changed without its reader (CLAUDE.md rule 10). Defect of P1-v N0 → pre-node T1-0 |
| 0.7a | (B3) N0 is NOT on `origin/main` (critic R3/R4: 079dc63, bea0bb0 not ancestors of be2c988; `origin/main:exit_gate.py` has no `def own`). Branch tips (`.git/packed-refs`, `.git/refs/heads/wip/p1v-n4fix`) and their ancestry (reflogs `.git/logs/refs/heads/wip/p1v-*`): `wip/p1v-n0` bea0bb0 = N0 079dc63 + fix round; `wip/p1v-n1` created from bea0bb0 → 30c2500; `wip/p1v-n2` from 30c2500 → fa69bd1; `wip/p1v-n4` from fa69bd1, merges n3+n5 (ad4f7a6) → N4 020f1a9; `wip/p1v-topic` from 020f1a9, merges `wip/p1v-fix` (b4193e8) → N4 round 2 **c9b2069**; `wip/p1v-n4fix` created from c9b2069 → "P1-v N4 fix round" **71d7ca8** (accepted, journal t-540 19:39, witness on 71d7ca8); `wip/p1v-n4b` from 71d7ca8 → d8b86a6 (N4b, round 2 in work, t-568, not accepted). On the n4fix tree `own` stands at `exit_gate.py:1878` and `stage_joints.py` has `EXIT_SKIP` only (`:59, :104`), PINS `{"exit": 8, …}` (`test_stage_joints.py:31`) | both c9b2069 and 71d7ca8 contain bea0bb0 (what T1-0 needs: the `own` producer). T1-0 is based on **71d7ca8**, the newest ACCEPTED P1-v tip, which carries N0-N4 with their fix rounds; c9b2069 lacks only the N4 fix round. Analog (ii) of round 0 ("main red since N0 merged") is withdrawn |
| 0.8 | The check argument at `exit_gate.py:1881` is an f-string, the one `check_arg` walk error of the wide scan (report `:19, 37`); the walk error is emitted at `refusal_registry.py:1436-1438` with `fn = stack[0]` (`:1432`), i.e. keyed by the OUTERMOST def `all_errors`, never `own` | F7 (a) with N3 (§3.5) |
| 0.9 | Runtime ids after N0: detector findings `<producer stem>:<label check>`, `:unlabelled`, `:defect`, `:unmigrated` (`exit_gate.py:452-478`); the text-end record has `script="exit_gate_text_end"` and no `check` (`:1058-1059`) → `exit_gate_text_end:unlabelled` (`detector_verdict.py:116-127`); `acceptance.py` writes no check id | 5 exit rows map 1:1 to a runtime literal; 3 exit, 8 detector, 27 window rows do not (F3, F4, §3.4) |
| 0.10 | The 43 v1 rows: 8 `exit:`, 8 `detector:`, 27 `window:` (`W\references\stage-joints.json:9-1117`); `branch_accounting.py` is in 4 detector rows (`:398, 447, 497, 548`); all 8 detector rows carry `"demands_from": "check:script"` (`:415, 438, 468, 491, 514, 542, 565, 588`) | 4 rows merge under F4 (a); the `check:script` carrier reads the key (0.11a) |
| 0.11 | Within the package, v1 key literals stand only in `stage-joints.json` and `test_stage_joints.py` (Grep `["'f](exit\|detector\|window):` over `W\`: the other hits are `machine_facts.py:804` `detector:{i}` and test labels `"window: …"`, unrelated; the pattern finds `stage_joints.py:497`, so it works) | the rename touches two data/test files plus the readers of 0.11a |
| 0.11a | (B2) Readers of the key PREFIX or key STRUCTURE in `W\scripts\stage_joints.py`: (r1) `_pins` `:551-557` `key.split(":", 1)[0] == kind`; (r2) `audit` counts `:629`, same test; (r3) `audit` `report.no_detector` `:635-636` `k.startswith(f"detector:{stage}:")`; (r4) `_row_problems` `:497-498` "a detector row runs at the stage in its key" (`check.split(":")[1]`); (r5) `demand_tokens` `:279-280` carrier `check:script` returns `check.rsplit(":", 1)[-1]` (the script name, from the key) — r5 is not in the verdict's list; found by this round's Grep. Tests: `test_stage_joints.py:63, 65, 69-74, 78, 90, 96-110, 130, 136, 138, 155, 197-213, 221-235, 287-296, 329-334` (Grep `exit:\|detector:\|window:\|startswith` on that file). No other package file reads a key prefix (0.11) | §3.4a defines each reader's behaviour after the rename |
| 0.12 | K1 runs in `stage_joints.audit` (CI `--contracts`, parent `:64, 79`); the census is a test fixture loaded only by tests and by the dev CLI `refusal_registry.py --census <path>` (explicit path); its role filter is test-side (FR-44; parent §2.5 `:195`, N1 `:714`) | a counter that needs census roles is computed and compared in the test, never in `audit` (B4, §3.5a) |
| 0.13 | `references/role-commands.json` names `roles` per role command (`W\references\role-commands.json:5-30`); `references/stages.json` names a role per detector script (`test_judgment_census.stage_rows`, `:183-197`) | data the F1 (a) rule reads first |
| 0.14 | Wave-0 item 7 (L1-L9) is written in v1 keys (`docs/tasks/specs/20261113-told-before-work-wave0-rows.md:252-260`) | T1r translates them through §3.4 |
| 0.15 | The wide `sites()` returns `walk_error` records (`refusal_registry.py:1359-1360`; `wide_report` filters them, `:1597`); `_census_blocking` imports `units_of` and returns the RAW `blocks` set (`:1618-1626`) | T1a widens the `--wide` list set (E6) |
| 0.16 | The OH8-7 chain is closed in this base (`SUBCLASS_ROWS`, `test_judgment_census.py:755`) | F2 (a): no chain machinery |
| 0.17 | `scenario_walk.py --witness-for` accepts absolute paths (`W\scripts\tests\scenario_walk.py:860-865`) | witness commands use absolute paths |
| 0.18 | `legacy_legs` = 9, `hand_cards` = 12: estimates (report `:60`, parent 0.6) | measured and written by T1b; a different number is a report line (N6) |
| 0.19 | (N4) `selftest.gate_named_files` reads `stage-joints.json` `joints[].joint.test` through the generic carrier reader `_json_carrier` + `_field_names` (`W\scripts\selftest.py:671-687, 722`), the same road it uses for `gate-registry.json` `rows[].test` (`:721`); `test_selftest_slow_tests.py:452-473` writes a schema-less `stage-joints.json` into a patched root and expects `test_j.py` named; that file is slow (never run locally) | F10: keep the generic read (the field survives in v2) |
| 0.20 | (N9) `audit`/`threshold`/`main` read the file through `null_outcomes.load_data` (`stage_joints.py:604, 646, 668`); K10 rows pin its texts (`test_stage_joints.py:242-257`, critic) | `load_rows` wraps `null_outcomes.load_data` and adds the schema test; absent/broken texts unchanged |

Analogs noticed, NOT widened: see §9.

## 1. Invariants touched, owners, census classes

### 1.1 AR-n (change check written into each node's DoD, §3)

| AR | How the revision keeps it | Change check (node) |
|---|---|---|
| AR-29 (`architecture.md:134-157`) | the census grows by exactly the non-list wide units; each new/flipped/removed row's class/roles/owner is judged per unit (builder of T1a-rows) and accepted by the Lead (tier above), never defaulted | `test_judgment_census.py` green; class + owner named per check (T1a, T1b, T1c) |
| AR-20 (`:210-222`) | every raise/lower of `blocking_per_role.*`/`safety` listed row by row with the reconciliation of §2.1; new counters `unsited`, `hand_cards`, `legacy_legs` (data) and `rowless`, `untold`, per-unit `bare`/`tagged` (test fixture, F11) join axis 18 and critic question 9 through T10 | "ratchet rows" block in every DoD |
| AR-13 (`:161-166`), axis 32 | one scanner: T1a reads `refusal_registry.sites(raises=raise_family(wide=True))`, no second AST walk; literal ids come from the same scanner; `load_rows` is the one reader of the rows (it wraps `null_outcomes.load_data`, N9); `selftest.gate_named_files` keeps its generic carrier reader for the field `joint.test` (F10) | Grep `ast.Raise\|ast.Call` in `test_judgment_census.py` gains no hit (T1a); Grep of `stage-joints.json` readers (T1b E4) |
| AR-22 (`:233-238`) | every v2 field and every counter has a reader: data counters read by `audit`; test-side counters read by `test_stage_joints.py` (B4) | Grep of v1 keys → 0 after T1b (positive control before); §3.5a table |
| AR-23 | `universe()` members carry `stages`; for exit/window members `stages` is `null` (not judged by the stage rule), never `[]` | T1b row `rename/kind-not-prefix` |
| AR-10 (`:113-118`) | the told universe gains no silent hole: role-reachable A24 ids and literal ids without a row are counted in `rowless` (test-side, dense) until T1r | T1c rows K1-A24, K4-K6 |
| AR-28 (`:275-280`) | an absent/unreadable/v1 rows file reads `(None, why)`, never a pass; an absent counter is never read as 0 | T1b (g); T1c edges |
| AR-19 / axis 5 | `exit_gate.all_errors` (producer) and `stage_joints.exit_members` (reader) reach `main` together: T1-0 lives on the P1-v line (B3) | T1-0 rows |
| AR-1 | `EXIT_WRAPPERS`, `CHECK_PASSTHROUGH` are closed scanner vocabulary of our own code (precedents `EXIT_SKIP` `stage_joints.py:59`, `SCAN_ROOT` `test_judgment_census.py:12-14`) | — |
| FR-44 (not an AR; read for B4) | a counter lives where its loader lives: census-needing counters in the test layer (§3.5a) | §3.5a table in T1c DoD |

### 1.2 Checks added or altered — owner (P27) and census class (AR-29)

| Check | Where (node) | Owner | Class |
|---|---|---|---|
| X1 `exit_members` sees through a wrapper of `EXIT_WRAPPERS` | `stage_joints.exit_members` (T1-0) | data | shape (AST) |
| X2 census units created from the wide NON-LIST transports; the list transport never creates or flips a unit | `test_judgment_census.units_of` (T1a) | data | shape (AST) |
| X3 each new (A), flipped (B) and removed (C) row's `class`, `roles`, `owner`, `ref` | rows file (T1a-rows): drafted by the builder by the F1 (a) rule, accepted by the Lead (tier above) | judgment | per row (shape/xref/safety expected; anything else is returned, T1a-E8) |
| X4 each raised/lowered ceiling | intent of the Lead (a named raise), read by the critic (question 9) | intent | — |
| X5 v2 accepted, v1 refused, absent/broken → `(None, why)` | `stage_joints.load_rows` (T1b) | data | shape |
| X12 a key's KIND and a detector row's stages come from the model, never from the key prefix (pins, counts, `no_detector`, stage rule) | `stage_joints.universe`, `_pins`, `audit`, `_row_problems` (T1b) | data | shape / xref |
| X13 the `check:script` demand token is `<stem>.py` of the `<stem>:*` key | `stage_joints.demand_tokens` (T1b) | data | xref |
| X6 K1 direction A over the v1-derived keys (audit); direction B with the sited set and `unsited` (audit) | `stage_joints._direction_a` (T1c) | data | xref |
| X7 K1-A24/literal: every role-reachable A24 id and literal id has a row, else counted in `rowless` (dense) | `test_stage_joints.py` (T1c) | data | xref |
| X8 K3, K7, E4, E7 | `stage_joints._row_problems` (T1c) | data | shape / xref |
| X9 K4, K5, K6, K12, `conductor_only` print | `test_stage_joints.py` (T1c) | data | shape / xref |
| X10 K2 page leg, gated on `contract_slices.requirement_section` | `stage_joints._told_leg` (T1c) | data | presence/xref |
| X11 a pass-through check argument is read at the bare-name call sites of the innermost def (F7 (a), N3) | `refusal_registry` wide scan (T1c) | data | shape (AST) |

New census units a node creates in its OWN code (a function matching `UNIT_NAME_RE`, `test_judgment_census.py:69`): class
`shape`/`xref`, roles `["conductor"]`, owner `data`, row in the same commit. T1b creates none by its named functions (`load_rows`,
`row_for`, `rows_for`, `told_text`, `told_line`, `fill` do not match `UNIT_NAME_RE`): a C1 red naming a new unit in T1b is a STOP and a
question, so T1b does not own `judgment-census.json` (disjoint from T1a).

## 2. The builder's questions

### 2.1 Q1 — the 113 wide-only units (and what makes the join 100 %)
DECIDED (Lead: F1 (a) + F2 (a)):
- T1a owns `test_judgment_census.py` (`units_of` only, plus its docstring/`BLIND_SPOT` text and one table) and `judgment-census.json`.
- THE UNIT SET (B1). `units_of` computes `wide = sites(..., raises=raise_family(..., wide=True))` (blocking None) and keeps only the
  records whose `state != "walk_error"` AND `transport != "list"`; both the u3 creation loop (`:245-246`) and the flip loop
  (`:278-281`) read this kept set and nothing else. INVARIANT (POSITIONAL): the list transport never creates or flips a census unit;
  it is bounded by the blocking set the census computes from the other transports (`_census_blocking`, used by the `--wide` join).
  The new units are therefore exactly `{(file, function) of kept records} − old units` = list A; at a2c88d8 |A| = 113 (critic R1:
  "units from non-list sites: 725 without row: 113"), re-measured on base B1 by §3.2.
- Why the join reaches 1.0: every unit of the `--wide --census` join is keyed `(file, outermost function)` of a non-walk-error record
  (`wide_report`, `:1597-1598`); a non-list record's unit is a census unit after T1a (it is created from that same record); a list
  record is counted only inside `_census_blocking`'s set, which is built from census units. So after the rows land, every join unit
  has a row: `units_no_row 0`, `join_share 1.0`. A join under 1.0 after T1a is a STOP (T1a-E7), never a raised tolerance.
- THE COUNT AND ITS PROOF (§3.2 probe, run before T1a-rows and again after T1a): before — `A` = the new units, `B` = the flipped units,
  `C` = the stale `<script>` rows, `old_units`, `new_units = old_units + |A| − |C|`; after T1a on its tree — `A = [], B = [], C = []`
  and `old_units` equal to the earlier `new_units`. Expected at a2c88d8 (from critic R1/R2, not measured on B1): |A| = 113, |B| = 11
  (with `project_decisions.py::run`), |C| = 1 (`check_coverage.py::<script>`), list-only units not created ≈ 2,192 (= 2,305 − 113,
  derived). The binding numbers are the probe's on B1.
- The raise is named row by row: for every role `r`, `blocking_per_role.r`: old → new, reason `T1a: census rows for wide-transport
  units (told-before-work T0 gate item 2)`, and the reconciliation `new − old == |A rows naming r| + |B rows naming r| −
  |C rows naming r that were effectively blocking| + |relabels adding r| − |relabels removing r|`, printed from the rows file. `safety`
  likewise. The same list goes in the commit message and the report; the critic verdict repeats it (axis 18, question 9). Gate form
  `judgment: adds data check …` (`t-346-oh8-7b-chain-spec.md:147`).
- The parent DoD line "census: no new blocking unit" reads for T1a: "census: new units = exactly list A; flipped = exactly list B;
  removed = exactly list C; nothing else". Every other node keeps the parent line.

### 2.2 Q2 — the 43 renames and the red `test_stage_joints.py`
DECIDED: the red is a defect of P1-v N0 (0.7). The Lead writes `defect_found` (agent = the N0 builder tier, `ref` = N0's accepted
task_id, notes "exit_members not changed with all_errors.own; test_stage_joints 97/111") and dispatches T1-0 on the P1-v line (B3,
§3.1). T1-0 restores the v1 keys (no data edit, no rename), so the base is green and the rename stays a separate move.
DECIDED: F3 (a), F4 (a) with §3.4a, F5 (a), F7 (a) with N3.

### 2.3 Q3 — K1 with 102 A24 ids and no rows between T1 and T1r
DECIDED (F6 (a) with B4): direction A for A24 ids and literal ids lives in `test_stage_joints.py` (the census filter is test-side):
the universe of that leg is the A24 entries and literal ids whose unit's census row names a non-conductor role; an id without a row
counts in `rowless` (the told fixture, F11; ≤ dense, the ids printed); T1r lands the rows and writes `rowless: 0`. `audit`'s direction A
holds the v1-derived keys only. Direction B (row → code) is judged in `audit` against the sited set (v1-derived keys ∪
`{check_of(e) for e in REGISTRY}` ∪ every literal id of the scanner, no census), so a row keyed by any known id is never stale.

### 2.4 Q4 — `rows_for` returns only rows that carry a requirement
DECIDED (confirms the builder): `rows_for` returns only rows with `requirement` XOR `requirement_from`. A row with neither (the 40 rows
until T1r) is told by its v1 legs as today, judged by directions B/C, and is never a page line.
INVARIANT: no sentence-less line ever reaches a page or the conductor section; a row with neither field and no v1 leg is red (K3:
`told` empty), and `{"page": true}` on a row with neither field is red (K3).

### 2.5 Q5 — K4/K6 baselines wait on Q1
DECIDED: order T1a → T1c. T1c's step 0 prints the baselines from the census AFTER T1a; the told fixture is written once, by T1c.
T1b writes no baseline it cannot measure.

### 2.6 Q6 — E11 cannot tell "never sited" from "gone after sited"
DECIDED (F8 (c)): `audit` counts only (`unsited` ≤ baseline); the red-at-once half of E11 is carried, per id, by each migration node's
test row "the site writes this id" (table/variant rows, docs/TESTING.md).

## 3. Nodes

Common to every package node: `given:` `<tree>\design\factory-rules.md` whole, `C:\QAFactory\forge-repo\plans\builder-rules.md`, the
parent spec, this file, the owned files. DoD always includes: the owned tests green; `test_judgment_census.py` green; `architecture:`
line naming the §1.1 rows touched; `judgment:` line; FR walk (PROJECT.md package rule 1); "ratchet rows" block (key, old → new, reason;
"none" when none); no new test file — new cases are variant/table rows of the keep files named. Witness = the test files printed by the
node's `scenario_walk.py --witness-for` line, each run, verbatim output. Slow files are never run locally.

### 3.0 Bases and sequence (B3, N8)

| Step | Move | Base | Parallel with |
|---|---|---|---|
| s1 | Lead: `defect_found` on N0; worktree `P\` (branch `wip/p1v-t10` from 71d7ca8), pushed | — | — |
| s2 | **T1-0** (builder) | 71d7ca8 (`wip/p1v-n4fix`, accepted t-540; contains bea0bb0 = N0 + fix round, 0.7a) | nothing of T1 |
| s3 | base fix B1 (integrator move, deterministic git, no tier task): merge `wip/p1v-t10` into `wip/tbw-t1`; `W\` then runs `test_stage_joints.py` and `test_judgment_census.py` (narrow witnesses). The P1-v integrator merges `wip/p1v-t10` into the P1-v line as that batch decides (F9') | `wip/tbw-t1` a2c88d8 | — |
| s4 | **T1a-rows** (builder, writes one docs file; not a code writer) ∥ **T1b** (builder, `Wb\`) | B1 | each other |
| s5 | Lead accepts the rows file → **T1a** (builder, `Wa\`) | B1 | T1b |
| s6 | merge T1a into `wip/tbw-t1` FIRST; then T1b merges `wip/tbw-t1` into `wip/tbw-t1b`, re-runs its witness + `test_judgment_census.py`, and is merged | — | — |
| s7 | **T1c** (builder, `W\`) | `wip/tbw-t1` with T1a and T1b | — |

Base-fix edges (s3): a merge conflict in `judgment-census.json` rows (N1-N4 and a2c88d8 both added rows) is resolved by keeping both
sides' rows; a conflict anywhere else, or a red narrow witness after the merge, is a STOP returned to the Lead with the verbatim
output. INVARIANT: no T1 step runs on a base whose `test_stage_joints.py` is red. TEMPORAL: if P1-v N4b (d8b86a6, in work) is
accepted BEFORE s3, s3 merges its tip instead (the newest accepted P1-v tip at s3); if it is accepted AFTER s4 started, it is merged
into `wip/tbw-t1` only after T1a is merged (else T1a's step 0 stops and the rows file is drafted twice, N8).
Writing code builders in parallel: at most 2 (T1a and T1b; T1a-rows writes a docs file and is not counted, rule 12).

### 3.0a Node table

| Node | Owns (absolute) | Depends | Ratchet moves (exact) | Tests (keep file: row ids) | Witness scope |
|---|---|---|---|---|---|
| **T1-0** exit universe through `own` (defect of P1-v N0) | `C:\QAFactory\forge-repo\.claude\worktrees\p1v-t10\ai-packages\qa-factory\scripts\stage_joints.py` (`exit_members`, new constant `EXIT_WRAPPERS` only); `C:\QAFactory\forge-repo\.claude\worktrees\p1v-t10\ai-packages\qa-factory\scripts\tests\test_stage_joints.py` (K9 rows only) | s1 | none (`PINS` stay 8/8/27; no data) | `test_stage_joints.py`: `K9/wrap-own` (`errors = own(f(x), "a")` → member `exit:f`), `K9/wrap-mixed` (`own(f(), "a") + g()` → `exit:f`, `exit:g`), `K9/wrap-nested` (`own(own(f(), "a"), "b")` → `exit:f`), `K9/wrap-not-call` (`own(x, "a")` → neither), `K9/wrap-attr` (`own(m.f(), "a")` → walk error), `K9/wrap-noargs` (`own()` → walk error), `K9/own-is-not-a-family` (`exit:own` absent), `K9/wrap-list-skipped` (`own(list(x), "a")` → neither); the real tree red-before count → all ok | `python -B C:\QAFactory\forge-repo\.claude\worktrees\p1v-t10\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for C:\QAFactory\forge-repo\.claude\worktrees\p1v-t10\ai-packages\qa-factory\scripts\stage_joints.py C:\QAFactory\forge-repo\.claude\worktrees\p1v-t10\ai-packages\qa-factory\scripts\tests\test_stage_joints.py` |
| **T1a-rows** per-unit rows file (builder; first step = the probe run) | `C:\QAFactory\forge-repo\docs\tasks\specs\20261113-told-before-work-t1a-census-rows.md` (the one file; reads `W\` only, writes nothing in it) | s3 (B1) | — (the file names the per-role raises T1a will make) | — (doc dispatch: the key-presence run of CLAUDE.md rule 11, §3.2 step 3) | the probe output pasted verbatim + the key-presence run with its negative control |
| **T1a** census units from the wide non-list transports | `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1a\ai-packages\qa-factory\scripts\tests\test_judgment_census.py` (`units_of`, docstring "WHAT A UNIT IS" u3 and `BLIND_SPOT` text, one new table + its test function); `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1a\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (rows of lists A/B/C of the accepted rows file, `ratchet`, `about` text) | T1a-rows accepted | census rows +|A| −|C| (113/1 at a2c88d8; the accepted file's numbers bind); `blocking_per_role.<r>` by exactly the reconciliation of §2.1; `safety` + |rows judged safety|; `word-list`/`meaning-proxy`/`meaning`/`breach`/`blocks_overrides`: unchanged (any other move is a stop) | `test_judgment_census.py` table `WIDE_ROWS`: `w-stderr-return`, `w-stderr-exit`, `w-stderr-raise`, `w-stderr-exit-name` (`return EXIT_X`) → unit, blocks; `w-stderr-note` (not followed) → no unit; `w-sys-exit-str`, `w-systemexit-str`, `w-refuse`, `w-module-level` (`<module>`) → unit; `w-walk-error` (check_arg) → no unit; `w-append-no-unit` (`.append(x)` / `+= [x]` in any function → no unit); `w-append-no-flip` (an `.append` inside an existing non-blocking unit leaves `blocks` False); `w-narrow-subset` (every unit of the narrow road is still a unit); `w-flip-existing` (an existing non-blocking row gains a non-list wide site → blocks, C3 red until raised); `w-flip-nested-span` (a site in a nested def's span flips the nested unit, the `project_decisions.py::run` shape); `w-script-unit-replaced` (a `detectors` script that gains a function unit: its `<script>` row is stale, the function rows need the `stages.json:` ref); `w-raise-named` (raised exactly → green; one short / one over → C3 red both ways); plus the real-tree C1-C6 | `python -B C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1a\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1a\ai-packages\qa-factory\scripts\tests\test_judgment_census.py C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1a\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json`; + the join command of 0.1 in `Wa\` (prints `units_no_row 0`, `join_share 1.0`; it is the real check of `_census_blocking`, N7) + the §3.2 probe on `Wa\` (`A`, `B`, `C` empty) + `test_refusal_registry.py` (a fair witness of the scanner's caller set; it calls `wide_report` with an explicit `blocking`, N7) |
| **T1b** reader + v2 + rename | `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1b\ai-packages\qa-factory\scripts\stage_joints.py` (new `load_rows`, `row_for`, `rows_for`, `told_text`, `told_line`, `fill`, v2 constants; `_shape_problems`; `exit_members`, `detector_members`, `window_members`, `universe` (member shape, §3.4a); `_pins`; `demand_tokens` (the `check:script` branch only); `_row_problems` (the detector-stage line `:497-498` only, and its signature); `_direction_a` (the `where` read in its message only); `Report` and `audit` (counts, `no_detector`, `detectors` passed to `_row_problems`, read through `load_rows`); `threshold`, `main` through `load_rows`); `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1b\ai-packages\qa-factory\references\stage-joints.json` (schema 2, keys of §3.4, `when_kinds`, `when_exclusive`, `told_ratchet` with `hand_cards`, `legacy_legs` only); `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1b\ai-packages\qa-factory\scripts\exit_gate.py` (`all_errors.own` signature and its SEVEN call sites; the `check=` of the record at `:1058-1059`; nothing else); `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1b\ai-packages\qa-factory\scripts\contract_slices.py` (`_keys_outputs` only); tests `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1b\ai-packages\qa-factory\scripts\tests\test_stage_joints.py`, `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1b\ai-packages\qa-factory\scripts\tests\test_stage_joints_12586.py`, `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1b\ai-packages\qa-factory\scripts\tests\test_contract_slices.py` | s3 (B1); F10, F11 on recommendations | `told_ratchet.hand_cards` new = measured, `legacy_legs` new = measured (estimates 12/9; a difference is a report line with the list, N6); `PINS` exit 8 → 8, detector 8 → 5, window 27 → 27; census: none | `test_stage_joints.py`: `v2/accepted`, `v2/v1-refused` (why "has schema_version 1; this reader reads 2"), `v2/absent`, `v2/broken` (both: the K10 texts of `null_outcomes.load_data`, unchanged, N9), `v2/not-object`; `row-for/found`, `row-for/absent`, `row-for/two`; `rows-for/role-stage-capability`, `rows-for/requirement-only`, `rows-for/conductor`; `told-text/<carrier>` per `requirement_from` value; `told-line/form`; `fill/missing-value-kept`; `import/light`; `rename/no-v1-key` (Grep of 0.11's pattern over the package → 0; positive control on a fixture string); `rename/pins` (8/5/27, ±1 red); `rename/kind-not-prefix` (a stub universe member `{"kind": "detector"}` keyed `foo:*` counts in the detector pin; a member keyed `detector:S9:x:y.py` with kind `exit` counts as exit; exit/window members carry `stages: null`); `merge/stages-from-model` (`branch_accounting:*` with stages `["S2","S3","S4","S5"]` green; with `S4` removed red "a detector row runs at the stages whose detectors list its script: S2, S3, S4, S5"); `no-detector/from-model` (the line still says `S0, S1, S6, S7, S9`; a model with S8's detector removed adds S8); `demands/check-script-stem` (`branch_accounting:*` → token `branch_accounting.py`); `exit/literal-key` (`own(f(), "exit_gate:x")` → key `exit_gate:x`); `exit/non-literal-check` (`own(f(), name)` → walk error "the check id given to `own` at line N is not a text"); `merge/branch-accounting` (one row, 4 producers); the v1-keyed rows of 0.11a rewritten to v2 keys. `test_contract_slices.py`: `keys/through-load-rows`, `keys/findings-clean` (`keys_findings(PLUGIN) == []`, pages byte-identical). `test_stage_joints_12586.py`: unchanged rows green | `python -B C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1b\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for` + every owned path above; plus `selftest.py --slices` and `selftest.py --contracts` in `Wb\` |
| **T1c** walker gate + counters | `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1\ai-packages\qa-factory\scripts\stage_joints.py` (`_row_problems` K3/K7/E4/E7 lines, `_told_leg`, `_direction_a`, `_ratchet`, `Report`, new `check_ids`, new `sited_ids`); `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1\ai-packages\qa-factory\references\stage-joints.json` (`told_ratchet.unsited` only); `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1\ai-packages\qa-factory\scripts\refusal_registry.py` (the `check_arg` branch at `:1436-1438` and new `CHECK_PASSTHROUGH` only); `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1\ai-packages\qa-factory\scripts\tests\fixtures\told-ratchet.json` (new, F11 (b)); `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1\ai-packages\qa-factory\scripts\tests\test-layers.json` (one `fixture_owners` row: `told-ratchet.json` → `test_stage_joints.py`); `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (rows of new `stage_joints.py`/`refusal_registry.py` units only); tests `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1\ai-packages\qa-factory\scripts\tests\test_stage_joints.py`, `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1\ai-packages\qa-factory\scripts\tests\test_refusal_registry.py` | T1a and T1b merged | per §3.5a: `told_ratchet.unsited` = 0 (data); told fixture `rowless`, `untold`, `units.<file::function>.bare/tagged` = the step-0 measurement, printed per key; `check_arg_errors` 1 → 0 | `test_stage_joints.py`: `K1/missing-row` (audit, v1-derived key), `K1-lit/fallback-no-row` (`<stem>:unlabelled`, `unknown` need no row), `K1-lit/sub-id` (C14), `K1-lit/star-covers` (`<stem>:x` covered by `<stem>:*`), `K1-A24/at-baseline` green, `K1-A24/plus-one` red naming the id, `K1-A24/minus-one` red ("lower `rowless` to N"), `K1-A24/conductor-only-not-counted`, `K1-lit/adviser-counted` (`exit_gate:adviser` counted in `rowless` until T1r), `B/row-keyed-by-any-entry-not-stale`, `B/row-keyed-by-literal-not-stale`, `K3/move-token`, `K3/shell-door`, `K3/page-without-requirement` red, `K7/role-rule`, `E4/empty-roles`, `E7/two-rows`, `E7/two-star-rows`, `E11/unsited-at-baseline` green, `E11/unsited-over` red, `E11/stale-when-baseline-0` red, `K4/at-baseline`, `K4/plus-one`, `K4/new-unit-no-baseline` red, `K5/roles-subset`, `K6/untold-counted`, `K12/unsited-cap`, `told/fixture-absent` red (never 0), `told/audit-shape` (audit reads no census: an `audit` run with the census file renamed in a copy tree is unchanged), `conductor-only/printed-per-group`, `K2/gated-off`, `K2/gated-on`. `test_refusal_registry.py`: `pass/literal-at-call` (no walk error, id = the literal), `pass/non-literal-at-call` (walk error), `pass/unlisted` (walk error), `pass/nested-def` (the listed def nested in another: matched by the innermost def), `pass/attr-call-same-name-ignored` (`m.own(x)` names no id and is no call site) | `python -B C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for` + every owned path above; plus `refusal_registry.py --check` and `selftest.py --contracts` in `W\` |

### 3.1 T1-0 — exit universe through `own`
Where it lives (B3): a fix node of the P1-v topic, on `wip/p1v-t10` from 71d7ca8, so the producer (`all_errors.own`, N0) and its
reader (`exit_members`) reach `main` in one merge of the P1-v line (AR-19, CLAUDE.md rule 10). Which batch file carries the node: F9'.
What: `EXIT_WRAPPERS = ("own",)` (code constant beside `EXIT_SKIP`). In `exit_members`, a leaf that is a call of a bare name in
`EXIT_WRAPPERS` is replaced by its FIRST positional argument before the existing rule runs. The wrapper name itself is never a member.
Docstring states the rule.
Edges:
- E1 empty input — a wrapper call with no argument: walk error "a call of `own` with no argument in `errors`; extend the walk or
  simplify the call". INVARIANT: no shape the walk cannot name is skipped.
- E2 nesting — `own(own(f(), "a"), "b")`: unwrap repeatedly (bounded by the AST depth). INVARIANT: a family under any number of
  wrappers is seen.
- E3 POSITIONAL — the unwrap runs BEFORE the `EXIT_SKIP` test, so `own(list(x), "a")` gives `list`, which stays skipped. INVARIANT:
  the aggregator and `list` never become families; every family seen before N0 is seen again (pin 8 holds).
- E4 `refused = own(run_advisers(...), "adviser")` (`:1891`) and `late = own(...)` (`:1901`) are not `errors` targets: not members.
- TEMPORAL: no artifact created. Before: `exit:own` + the unwrapped keys (red). After: the 8 v1 keys (green). T1b later changes the
  key form.
DoD: the K9 rows; the real tree prints its red count before the edit (97/111 on `W\`; the count on 71d7ca8 is printed, estimate the
same, not verified) and `=== test_stage_joints: N/N ok ===` after; `architecture: AR-19, AR-22 -- the exit universe reader follows its
producer all_errors.own, on the producer's topic`; `judgment: none -- AST shape`; ratchet rows: none. Non-goals: renames,
`exit_gate.py`, data, any `wip/tbw-*` branch. siblings: `window_members` (`gaps.extend` already reads inner calls — no wrapper today,
n/a), `detector_members` (data, n/a).

### 3.2 T1a-rows — the per-unit rows file (builder node; first step is the run)
Base: `W\` after s3 (B1). The builder reads `W\` and writes only the rows file. No designer run is needed.

Step 1 (the run, FIRST). Save the script below VERBATIM as `t1a_probe.py` in the builder's own scratchpad (never in the repo) and run
`python -B <scratchpad>\t1a_probe.py C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1\ai-packages\qa-factory`. It is a pure read
(command hygiene pt. 4 does not apply: it writes only stdout).

```python
"""T1a probe: lists A (new census units), B (flipped units), C (rows that turn stale) under the T1a unit rule:
units are created and flipped by wide NON-LIST, non-walk-error records only. Pure read; prints one JSON object."""
import json
import sys
from pathlib import Path

P = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(P / "scripts"), str(P / "scripts" / "tests")]
import refusal_registry as R  # noqa: E402
import test_judgment_census as T  # noqa: E402

files = T.scan_files(P)
old = T.units_of(P, files, R.REGISTRY)["units"]
census = json.loads((P / "scripts" / "tests" / "fixtures" / "judgment-census.json").read_text(encoding="utf-8"))
rows = {(r.get("file"), r.get("function")): r for r in census.get("rows") or []}
wide = R.sites(plugin_root=P, files=files, raises=R.raise_family(plugin_root=P, files=files, wide=True))
kept = [s for s in wide if s.get("state") != "walk_error" and s.get("transport") != "list"]
narrow = R.sites(plugin_root=P, files=files, raises=R.raise_family(plugin_root=P, files=files))
new_keys = {(s["file"], s["function"]) for s in kept}
list_keys = {(s["file"], s["function"]) for s in wide if s.get("transport") == "list"}
detectors = T.stage_rows(P)["detectors"]


def refs(key):
    return sorted(f"stages.json:{sid}/{role}" for sid, role in detectors.get(key[0], []))


def holds(key):
    spans = old[key]["spans"]
    return any(s["file"] == key[0] and (s["function"] == key[1] or any(a <= s["line"] <= b for a, b in spans)) for s in kept)


A = sorted(k for k in new_keys if k not in old)
C = sorted(k for k in old if k[1] == "<script>" and any(a[0] == k[0] for a in A))
B, B0 = [], []
for key in sorted(old):
    if key in C or old[key]["blocks"] or not holds(key):
        continue
    (B0 if rows.get(key, {}).get("blocks_override") is False else B).append(key)


def row_view(key):
    r = rows.get(key, {})
    return {"file": key[0], "function": key[1], "roles": r.get("roles"), "class": r.get("class"), "ref": r.get("ref")}


print(json.dumps({
    "tree": str(P),
    "old_units": len(old),
    "new_units": len(old) + len(A) - len(C),
    "A": [{"file": k[0], "function": k[1], "refs": refs(k),
           "sites": sorted({s["line"] for s in kept if (s["file"], s["function"]) == k})} for k in A],
    "B": [row_view(k) for k in B],
    "B0_override_false": [row_view(k) for k in B0],
    "C": [row_view(k) for k in C],
    "narrow_lost": sorted(list({(s["file"], s["function"]) for s in narrow} - new_keys - set(old))),
    "list_only_units_not_created": len(list_keys - new_keys - set(old)),
}, indent=1))
```

Expected shape: one JSON object with exactly these keys; `A`/`B`/`C` lists of objects; `narrow_lost` = `[]` (a non-empty list is a
STOP: a unit of the narrow road would be lost by T1a, E5). Expected values at a2c88d8 (§2.1): |A| 113, |B| 11, |C| 1; on B1 the
numbers will differ (P1-v N1-N4 and T1-0 added code): the B1 numbers bind, a difference from 113/11/1 is a report line, not a stop.
Probe edges: an import failure or a traceback is a STOP with the verbatim output (never a hand-made list); an empty `A` on B1 is a
STOP (the 113 cannot have vanished without a census change; the Lead re-reads the base).

Step 2 (the rows). The rows file holds: §0 the probe source and its verbatim output; §1 list A — one row per unit
`file | function | class | roles | owner | ref | note | evidence (file:line)`; `ref` = the probe's `refs` joined by `, ` (empty when
none); roles by the F1 (a) rule in this order — (1) the roles of the `references/role-commands.json` commands that run the unit's
script; (2) the stage role of a `references/stages.json` `detectors` script; (3) a role whose `agents/<role>.md` or
`references/slices/<role>/` names the script; (4) else `["conductor"]` with a `note` naming the group of parent §2.8 — and the row
says which step decided; class/owner from reading the body at the probe's `sites` lines; §2 list B — `file | function | old roles |
roles after | note` (roles after = old roles unless the F1 (a) rule finds more; a change is a relabel, named); B0 is listed for the
record (no ceiling moves for it); §3 list C — `file | function | roles | ref | replaced by` (the A units of the same file, which carry
its `ref`); §4 per role: old ceiling (from `judgment-census.json` `ratchet`), the reconciliation of §2.1, new ceiling; `safety` likewise.
A reading other than `shape`/`xref`/`safety` is never drafted: the row is left out and listed under "questions" with the evidence.
Step 3 (doc witness, CLAUDE.md rule 11 DOC-DISPATCH): a key-presence run over the rows file for the verbatim keys `## 0`, `## 1 list A`,
`## 2 list B`, `## 3 list C`, `## 4 per role`, `narrow_lost`, `new_units`, with a negative control (one key removed from a copy → the
script reports failure); the script attached in full source, never committed.
Edges: E1 limit — none (|A| is whatever the probe prints). E2 a unit of A in a file with no role command, no stage row and no slice →
step (4), never guessed. E3 a unit of A whose sites refuse nothing on reading → the row is written as judged with `note: "E3: refuses
nothing -- <why>"` (T1a E9). INVARIANT: every unit the probe lists has exactly one row or one named question; no unit is added by hand.
Acceptance: the Lead (tier above the builder; X3 judgment). The builder of T1a copies the rows verbatim.

### 3.3 T1a — census units from the wide non-list transports
What: in `units_of`, compute `family = raise_family(root, files, wide=True)` and `wide = sites(root, files, raises=family)` (blocking
None); keep only records with `state != "walk_error"` and `transport != "list"` (one filtered list, computed once); create u3 units
from the kept records (`:245-246`) and flip `blocks` by the kept records (`:278-281`). `found["sites"]` counts the kept records (the
totals line says "wide non-list sites"). The docstring u3 and `BLIND_SPOT` name the wide transports, the list exclusion, and the
stderr blind spot of T0-gate change 1. Then land rows A, the B relabels/notes, remove rows C, and the raise.
Step 0 (stop on difference, precedent `t-346-oh8-7b-chain-spec.md` §3.2): run the §3.2 probe on `Wa\`; if `A`, `B` or `C` differ from
the accepted rows file, STOP before any edit and return the verbatim diff; the Lead re-cuts.
Edges:
- E1 limit: none introduced.
- E2 empty — a record with no `function` (module level) → unit `(file, "<module>")`. INVARIANT: no site is dropped for lack of a name.
- E3 an unparsable file → a `parse` walk-error record (dropped by the filter); `read_package` names the file and makes C1 red
  (`:170-180`). INVARIANT: a file the scan cannot read is never green and never creates a phantom unit.
- E4 POSITIONAL (B1) — the list/walk-error filter runs BEFORE both loops. INVARIANT: the list transport never creates or flips a census
  unit; a unit exists only where a non-list refusal site was seen.
- E5 narrow ⊆ wide — every unit of the old road stays a unit (`w-narrow-subset`, probe `narrow_lost`); if not, STOP.
- E6 the `--wide` CLI: `_census_blocking` now returns the wider raw blocking set, so list sites count in more units; the join stays 1.0
  (§2.1). The census test's wall time is printed before/after; over 60 s on the builder's machine is a question (builder-rules 7).
- E7 the join after rows: `units_no_row 0`, `join_share 1.0`; anything else STOP with the verbatim output.
- E8 a row judged `word-list`/`meaning-proxy`/`meaning`: not committed; returned. INVARIANT: a classification never smuggles a breach
  raise.
- E9 a unit of A that refuses nothing on reading: row as judged with `note: "E3: refuses nothing -- <why>"`, NO `blocks_override`.
  INVARIANT: a computed refusal is never relabelled non-blocking by the builder; the count errs toward extra blocking.
- E10 list C — the `<script>` row is removed in the same commit as the A rows of its file; its `ref` tokens move to them (C1 ref check).
  INVARIANT: a row is never dropped silently (C1 "stale row" text) and a `stages.json:` registration is never lost.
- Conflicting pair: "join 100 %" vs "census: no new blocking unit": resolved by §2.1 (named exception).
- TEMPORAL: the rows file is born before T1a (T1a-rows). Before T1a: wide-only units uncounted, join 86.5 % (a2c88d8). After: every
  non-list wide unit a census unit, join 1.0, role ceilings moved by name; K4-K6 do not exist yet (T1c).
Error direction of the reused function (advice → gate): `sites(raises=raise_family(wide=True))` moves from a dev measurement to the
census's unit road. Allowed: EXTRA units (a note counted as a refusal; E9). Never: missing a refusal of a shape it claims to scan, and
never a unit from the list transport (B1). Adversarial inputs that must stay on the safe side: `print(..., file=sys.stderr)` then
`return 2` / `return EXIT_X` / `sys.exit(2)` / `raise` → unit; the same then `return 0` or nothing → no unit, counted blind spot;
`sys.exit("msg")`, `raise SystemExit("msg")` → unit; `refuse(...)` → unit; `out.append(x)`, `errors += [x]` → no unit and no flip;
an alias `b = block; b(msg)` and a message built in another function → the named blind spots of T0 (no unit, counted).
DoD: `WIDE_ROWS` and real-tree C1-C6 green; the join command prints `units_no_row 0` and `join_share 1.0` (verbatim); the probe on `Wa\`
prints `"A": []`, `"B": []`, `"C": []` and `old_units` = the accepted file's `new_units`; `test_refusal_registry.py` green; ratchet rows
per role with the reconciliation; `architecture: AR-29, AR-20, AR-13 -- the census creates units from the one scanner's wide non-list
sites; every raise named row by row`; `judgment: adds data check <units of A>`; four-question block M1 (§5) in the commit message.

### 3.4 T1b — the rename mapping (applied once; F5 (a))

| v1 key (count) | v2 key | Basis |
|---|---|---|
| `exit:scoped_errors`, `exit:grounding_errors`, `exit:case_identity_errors`, `exit:digest_errors`, `exit:required_outputs_errors` (5) | `exit_gate:scoped`, `exit_gate:grounding`, `exit_gate:case_identity`, `exit_gate:digest`, `exit_gate:required_outputs` | the literal at the call (`exit_gate.py:1883-1887`) |
| `exit:detector_errors`, `exit:witness_errors` (2) | `exit_gate:detector_errors`, `exit_gate:witness_errors` (aggregator keys) | F3 (a) |
| `exit:text_end_after_handback` (1) | `exit_gate:text_end_after_handback`; T1b sets `check="exit_gate:text_end_after_handback"` on the record at `exit_gate.py:1058-1059` (text byte-identical) | F3 (a) |
| 8 `detector:<S>:<role>:<script>.py` | `<script stem>:*` (5 rows: `branch_accounting:*` merging 4, `planning_contract:*`, `critic_rollcall:*`, `s5_precheck:*`, `check_coverage:*`) | F4 (a); `*` is the one wildcard form, in a row key only, never at a call |
| 27 `window:<kind>` | `acceptance:<kind>` | parent §2.1 |

`exit_members` (T1b): an own-wrapped leaf's key is the wrapper's SECOND positional argument, which must be a str literal; T1b changes
the SEVEN call sites (`:1883, 1884` ×2, `1885, 1887, 1891, 1901`) to full ids (`own(scoped_errors(...), "exit_gate:scoped")`,
`own(run_advisers(...), "exit_gate:adviser")` at both adviser calls) and `own` to `DV.with_check(r, check)` — runtime ids unchanged,
text unchanged. A non-wrapped leaf keys `exit_gate:<callee>`. `detector_members` keys `<stem>:*`; `window_members` keys
`acceptance:<kind>`. Merge rule (F4 (a)): stages = the union in `stages.json` order; producers = concatenation; `joint`: equal or all
null → kept; different → STOP and return the four `joint` values.

### 3.4a T1b — every reader of the key prefix after the rename (B2)

Member shape (C9): `universe()` returns `({key: {"kind": "exit"|"detector"|"window", "where": str, "stages": [ids] | None}}, [walk
errors])`. `exit_members` and `window_members` give `stages: None`; `detector_members` gives the stages, in `stages.json` order, whose
non-advice `detectors` list the script (the merge of tuples by stem). Kind is set by the member function that produced the key and
is never derived from the key text.

| Reader (file:line on `W\`) | Today | After T1b | Test row |
|---|---|---|---|
| r1 `_pins` `stage_joints.py:551-557` | `key.split(":", 1)[0] == kind` | `m["kind"] == kind` over `uni.values()`; pins 8/5/27 | `rename/pins`, `rename/kind-not-prefix` |
| r2 `audit` counts `:629` | same prefix test | count by `m["kind"]`; the summary line reads `walked exit 8, detector 5, window 27 \| rows 40` | `k1_real_tree` line (`:63`) rewritten |
| r3 `audit` `no_detector` `:635-636` | `k.startswith(f"detector:{stage}:")` over `uni` | stage ids of `env.model` not in the union of `detector_members(env.model)` stages (from the model, not from the injectable `uni`); real tree unchanged: `S0, S1, S6, S7, S9` | `no-detector/from-model`; `:65` unchanged |
| r4 `_row_problems` `:497-498` | `check.startswith("detector:") and stages != [check.split(":")[1]]` | signature gains `detectors` (the `detector_members(env.model)` answer, computed once in `audit`); `elif check in detectors and stages != detectors[check]["stages"]` → "`stages` is {stages}, a detector row runs at the stages whose detectors list its script: {want}"; a row not in `detectors` is not judged by this line | `merge/stages-from-model`; `:136` rewritten (`s5_precheck:*` with `["S4"]` red) |
| r5 `demand_tokens` `:279-280` (`check:script`) | `check.rsplit(":", 1)[-1]` (the script name in the v1 key) | `[f"{check.split(':', 1)[0]}.py"]` — the stem is the id's namespace by definition (parent §2.1), not a kind; for the 8 rows the tokens are the same script names as today | `demands/check-script-stem` |
| r6 `_direction_a` message `:546` | `where` is a str | `m["where"]` (T1c then rewrites the function) | existing K4 row (`:96-98`) with a v2 stub |
| tests `test_stage_joints.py:63, 65, 69-74, 78, 90, 96-110, 130, 136, 138, 155, 197-213, 221-235, 287-296, 329-334` | v1 keys / `startswith("window:")` / `len == 43` | v2 keys; window rows selected by `UNI[0][key]["kind"] == "window"`; `len(UNI[0]) == 40`; K9 exit keys `exit_gate:<x>` | each row rewritten in place, same ids |

INVARIANT (B2): after T1b no reader in the package classifies a key by its text prefix; a key whose producer is unknown has no kind
and is counted in no pin (`rename/kind-not-prefix`). Positive control for "no other reader": Grep of 0.11's pattern over the package
before T1b finds `stage_joints.py:497`; after T1b the same Grep finds nothing in code.

Edges:
- E1 TEMPORAL — `schema_version` 2 is born in T1b. Before: v1 read, v1 keys. After: v2 only; a v1 file reads `(None, "… has
  schema_version 1; this reader reads 2")` and `audit`/`main` exit 3 (UNREADABLE), `threshold` returns None. `load_rows(path)` takes the
  path (default `DATA`) and wraps `null_outcomes.load_data`: absent/broken texts are those of the K10 rows, unchanged (N9). Every code
  reader of the rows moves in the same commit. `told_ratchet` holds only `hand_cards`, `legacy_legs`; `_shape_problems` requires exactly
  the keys this node writes; T1c adds `unsited` with its check. INVARIANT: no counter is ever read from an absent key as 0.
- E2 empty — a row with neither `requirement` nor `requirement_from` (all 40): allowed, not returned by `rows_for`. `fill` with a
  missing value leaves its placeholder.
- E3 runtime — rows file absent: the generated page stands; `row_for` → `(None, why)`.
- E4 the AR-13 grep (parent `:47`) over code reads of `stage-joints.json` finds `stage_joints.py` (through `load_rows`) and
  `selftest.py:722` (generic carrier reader of the field `joint.test`, F10 (a)); positive control before the change:
  `contract_slices.py:490` and `selftest.py:722` match.
- E5 `keys_findings(PLUGIN) == []` and every generated page byte-identical.
- E6 `own` with a non-literal second argument after T1b → `exit_members` walk error "the check id given to `own` at line N is not a
  text; write the id as a literal" (N5). INVARIANT: no key is invented from a name.
- E7 between T1b and T1c, `own`'s `check` parameter is still a `check_arg` walk error of the wide scan (`check_arg_errors 1`): unchanged
  from today, removed by T1c (F7 (a)).
- E8 a C1 red in `test_judgment_census.py` naming a new unit → STOP and question (T1b owns no census rows, §1.2).
- Conflicting pair: "pages byte-identical" vs "`_keys_outputs` through `load_rows`": same producers → same bytes; a page diff is a stop.
DoD: rows of §3.0a; `selftest.py --slices` and `--contracts` green in `Wb\`; Grep of 0.11's pattern → 0 code hits; after s6 merge
`test_judgment_census.py` green on the merged tree; `architecture: AR-13, AR-22, AR-23, AR-28 -- one reader of the rows; v1 keys renamed
with every reader; kind from the producer, not the prefix; absent/v1 file is unknown`; `judgment: none -- shape of a data file`.

### 3.5 T1c — the walker gate and the counters
What: `check_ids()` (reads the wide scan's records of `refusal_registry`, never its own AST walk) returns `{id: (file, function,
line)}` for every literal id of `refusal(...)`/`with_check(...)` calls and every pass-through literal (F7 (a)). `sited_ids()` = the
v1-derived universe keys ∪ `{check_of(e) for e in REGISTRY}` ∪ `check_ids()`. `audit`: direction A over the v1-derived universe only (as
today); direction B: a row whose key is not in `sited_ids()` and not a sub-id `<id>.<part>` of one → counted `unsited`, compared to
`told_ratchet.unsited` (≤, else red; at baseline 0 every such row is a stale row). `_row_problems`: K3, K7, E4, E7. `_told_leg`: K2 page
leg refused with "the page renderer is not present" while `contract_slices` has no `requirement_section`. Test side (`test_stage_joints.py`,
which loads the census and the told fixture): K1-A24/literal direction A, `rowless`, K4, K5, K6, K12, `conductor_only` per group.
`CHECK_PASSTHROUGH = {("exit_gate.py", "own"): 1}` (F7 (a), N3): when a `with_check`/`refusal` check argument is a Name that is the
parameter at that index of the INNERMOST enclosing def (the last element of the scanner's stack, not `stack[0]`, 0.8) and
`(file, innermost def)` is listed, it is no walk error; the ids are the str literals passed at that position by the bare-name calls
(`ast.Call` whose `func` is an `ast.Name` equal to the def's name) in the scope where the def is visible (its enclosing def's body for a
nested def; the module for a module-level def). An attribute call of the same name (`dispatch_identity.own(...)`, `exit_gate.py:1100`)
is never a call site. A non-literal at a call site → walk error.
Step 0: print the join (must still be 1.0), `role_reachable_units` before/after T1a, the per-unit `bare`/`tagged`, `untold`, the
`rowless` list; these become the baselines verbatim.

### 3.5a Where each counter is computed, compared and loaded (B4)

| Counter | Needs census | Computed in | Compared in | Stored in (loaded by) |
|---|---|---|---|---|
| `hand_cards` | no | `stage_joints.audit` | `audit` (dense ≤) | `references/stage-joints.json` `told_ratchet` (loaded by `load_rows`: `audit`/`threshold`/`main`, `contract_slices`, T2/T3a/T3b at run time) |
| `legacy_legs` | no | `audit` | `audit` | same |
| `unsited` | no (sited set = universe ∪ REGISTRY ids ∪ scanner literals) | `audit` | `audit` | same |
| `rowless` | yes (role reach of the id's unit) | `test_stage_joints.py` | `test_stage_joints.py` (dense) | `scripts/tests/fixtures/told-ratchet.json` (F11 (b); loaded only by `test_stage_joints.py`, owner row in `test-layers.json` `fixture_owners`) |
| `untold` | yes | `test_stage_joints.py` | `test_stage_joints.py` (≤) | same fixture |
| `bare`, `tagged` per unit `file::function` | yes | `test_stage_joints.py` | `test_stage_joints.py` (≤; a role-reachable bare site in a unit with no baseline row red, K4) | same fixture |

`audit` never opens the census or the told fixture (`told/audit-shape`). One road for literal ids (B4): ALL literal ids go to the
test-side leg with `rowless` (direction A); `audit` uses them only in the sited set (direction B), with no exemption list.
`exit_gate:adviser` (N5) is a literal id of a role-reachable unit (`exit_gate.py::all_errors`, census roles) with no row: counted in
`rowless` from T1c; T1r writes its row (its sentence on the producer side: the advisers' verdict) and lowers `rowless`.

Edges:
- E1 `<stem>:*` coverage — a literal id `<stem>:<x>` with its own row is judged by that row; otherwise by `<stem>:*`. Two `*` rows for
  one stem → E7 red. INVARIANT: an id is covered by exactly one row.
- E2 fallback ids `<stem>:unlabelled`, `unknown` need no row. INVARIANT: a fallback never stands for coverage.
- E3 `rowless` limit — at baseline green, +1 red naming the id, −1 red "lower `rowless` to N" (dense). INVARIANT: an A24/literal id
  without a row is never silent and the count only falls.
- E4 TEMPORAL — counters born here; the told fixture is born here (absent before T1c: nothing reads it; after: absent or unreadable →
  red "told-ratchet.json cannot be read", never 0). T1c → T1r: `rowless` = N, `unsited` = 0. T1r: rows land, `rowless` → 0, `unsited` →
  its count. Closing wave: `unsited` → 0; after closing any unsited row = stale = red.
- E5 POSITIONAL — in the test-side leg the fallback exemption runs BEFORE the row lookup; in `audit` the `unsited` test runs AFTER the
  sited-set lookup. INVARIANT: a fallback id never makes a row look sited; a row with a real site is never counted unsited.
- E6 the page leg gate — absent attribute: K2 rows read "not present" (red only for rows with `{"page": true}`, none before T1r);
  present (T3a): the real leg. INVARIANT: no K2 green without a renderer.
- E7 a role-reachable census unit with a bare site and no baseline row → K4 red.
- E8 the passthrough (N3) — a listed def that is never called with a literal → no id and no walk error is NOT allowed: zero call sites
  is a walk error "`own` is listed in CHECK_PASSTHROUGH and has no call with a literal check". INVARIANT: a listed function never
  hides a check argument.
- Conflicting pair: rows-first cut vs dense `bare`/`tagged`: migration nodes lower counts below baseline (allowed `≤` until the closing,
  parent `:365`); the dense rule applies to `rowless` and `unsited` only at T1r and the closing.
DoD: rows of §3.0a; the §3.5a table holds (each counter computed and compared where it says; `told/audit-shape` green);
`refusal_registry.py --check` green; `check_arg_errors 0` in the join output; baselines printed verbatim; `architecture: AR-10, AR-20,
AR-22, AR-28 -- K1/K3/K4-K6/K12 with counted baselines; census-needing counters in the test layer (FR-44); new counters named for axis 18`;
`judgment: none -- presence and joins` (plus `adds data check` for any new unit).

## 4. What a T1 change alters for other nodes (they stay as written otherwise)
- T1r: writes rows under §3.4 keys; translates wave-0 item 7 L1-L9 by §3.4 (L7/L9 → `branch_accounting:*`, L8 → `critic_rollcall:*`);
  writes the `exit_gate:adviser` row; lowers `rowless` to 0 in `scripts/tests/fixtures/told-ratchet.json` (F11 (b): T1r's owns gain that
  fixture) and writes the `unsited` baseline in `stage-joints.json`. Census rows: none. Sentences stay on producer rows; the aggregator
  rows `exit_gate:detector_errors`/`witness_errors` stay sentence-less (told by v1 legs), so one finding is never told twice (critic key 7).
- T2: `refusal()` looks rows up under v2 keys; its pass-through becomes a `CHECK_PASSTHROUGH` line. The rule of §3.5 reads call sites in
  the scope where the def is visible, i.e. the same file; `refusal` is called from other files, so T2 must state the cross-file call-site
  rule in its own spec (§9 (c)).
- T3a: `requirement_section` reads `rows_for`; its attribute turns the gated leg on; `### Not yet in rows` reads `told_ratchet.hand_cards`.
- T3b: `dispatch_groups` → `rows_for(role, stages, facts)`.
- T4, T9a, T9c: their `blocking_per_role` moves start from T1a's numbers; `judgment-census.json` order T1a → T1c → T9c/T4/T9a.
- T8: "the 8 exit families keep their legs" becomes "the 8 exit rows keep their legs under §3.4 keys".
- T5b, T6, T7a-1…8, T7b-f, T9a, T9c (F8 (c)): each DoD carries one table/variant row per migrated id "the site writes this id".
- T10: axis 18 gains `told_ratchet.unsited`/`hand_cards`/`legacy_legs` and the told fixture's counters; critic question 9 names them.
- Outside the package: P1-b C1 follows §3.4 (parent `:619`).

## 5. Four questions (CLAUDE.md rule 10)

Mechanisms: M1 census units from the wide non-list transports (T1a); M2 `EXIT_WRAPPERS` (T1-0, T1b); M3 `rowless` + the test-side
A24/literal leg of K1 (T1c); M4 `CHECK_PASSTHROUGH` (T1c); M5 the E11 split (F8 (c)); M6 kind and detector stages from the producer, not
the key prefix (T1b, B2); M7 the told fixture: census-needing counters in the test layer (T1c, B4, F11 (b)).
(a) Cost and who pays. M1: one function edit with one filter, |A| rows copied, one builder rows pass and one Lead acceptance. M2: one
constant, one branch. M3: one counter, one test leg; T1r pays one fixture line. M4: one constant, one scanner rule; T2 pays one line.
M5: one test row per migrated id. M6: a member dict and five reader edits, no new data. M7: one fixture file, one `fixture_owners` row.
(b) Axes (one block, each line closes M1-M7 by name):
axis 1: n/a M1-M7 — no policy/role file/journal carrier changes. axis 2: n/a M1-M7 — no exam instrument. axis 3: covered M1-M7 — a
`changelog.d/` fragment per package node. axis 4: n/a M1-M7 — no FR text changes. axis 5: covered M2 — `all_errors` ↔ `exit_members`
on one topic line (B3); covered M6 — `detector_members` (producer) ↔ `_pins`/`audit`/`_row_problems`/`demand_tokens` (readers) in one
commit; n/a M1, M3-M5, M7. axis 6: covered M1 — the `--wide` measurer reads the census units road (E6); n/a M2-M7. axis 7: n/a M1-M7.
axis 8: n/a M1-M7. axis 9: n/a M1-M7. axis 10: n/a M1-M7. axis 11: n/a M1-M7. axis 12: covered M1-M7 — nodes of the Lead's DAG with
statuses moved with the journal. axis 13: n/a M1-M7. axis 14: n/a M1-M7. axis 15: n/a M1-M7. axis 16: covered M6 — `load_rows` wraps
`null_outcomes.load_data`, the one JSON reader of this file (N9); n/a others. axis 17: covered M4 — check ids keep the
`detector_verdict.check_id` reader; n/a others. axis 18: covered M1, M3, M7 — raises named row by row; new counters join the axis via
T10; n/a M2, M4-M6. axes 19-27: n/a M1-M7. axis 28: n/a M1-M7 — no render site changes in T1. axes 29-31: n/a M1-M7. axis 32: covered
M1, M4 — one scanner, the census reads its wide records; covered M3, M7 — the census filter stays test-side (FR-44); n/a M2, M5, M6.
axis 33: n/a M1-M7. axis 34: covered M1-M7 — one road for every script and role: units by transport (the list exclusion is a positional
rule for every file), roles by the data-first rule, kind by the producer for every key, one passthrough rule read for every file alike.
axis 35: n/a M1-M7. axis 36: n/a M1-M7.
(c) Detectors. M1: `test_judgment_census.py` C1/C3 + calibration check 41; M2: pins; M3: K1-A24 rows; M4: pass rows + `check_arg_errors`;
M5: site rows + `unsited`; M6: `rename/kind-not-prefix`, `merge/stages-from-model`, `demands/check-script-stem`; M7: `told/fixture-absent`,
`told/audit-shape`.
(d) What stops a skip. Code on the path: a unit with no row → C1; a raise not written → C3 above; too far → C3 below; a lost family →
pin red; a rowless id over baseline → K1-A24 red; a non-literal check → walk error; a key with no producer → counted in no pin. On
discipline only: the TRUTH of a role label (X3), detected by critic question 11 and calibration check 41 (d).

## 6. Forks — Lead

Decided by the Lead (13.11, binding): F1 (a), F2 (a), F3 (a), F4 (a), F5 (a), F6 (a), F7 (a), F8 (c); F9 (a) dropped (B3). Their
option tables are in the round-0 text (git history of this file); their consequences are written into §2-§3. Open:

| # | Fork | Options, cost | Recommendation |
|---|---|---|---|
| F9' | Which carrier tracks T1-0 (B3: "a call for the Lead and the P1-v batch owner") | (a) a fix node of the P1-v line (its batch/DAG file, branch `wip/p1v-t10` from 71d7ca8), merged into the P1-v line by its integrator and into `wip/tbw-t1` at s3. Cost: the P1-v file gains a node; if that batch is frozen (PROJECT.md «Командная работа» п. 2), a finding + node in its next batch · (b) a node of this told-before-work DAG on the same branch. Cost: the producer's topic does not list the fix of its own defect; the P1-v merge to `main` could go without it | **(a)**; the node is executable either way: branch and base are the same |
| F10 | `selftest.py:722` read of `joints[].joint.test` (N4; reverses the parent's N5 decision "through `load_rows`") | (a) keep the generic carrier reader (`_json_carrier` + `_field_names`, the road of every carrier, `selftest.py:671-687, 721-722`); the field survives in v2, `test_selftest_slow_tests.py` stays green unchanged; the AR-13 grep counts this read as the collector's own fact (test names of carriers). Cost: one parent line amended · (b) through `stage_joints.load_rows(path)` bound to selftest's `PLUGIN_ROOT`, and T1b owns the slow test's fixture (schema 2). Cost: a slow file in T1b's owns (CI-only witness), selftest imports `stage_joints`, and an AR-28 sentence for the collector | **(a)** |
| F11 | Carrier of the census-needing counters (B4: FR-44 forbids `audit`/runtime data) | (a) a constant in `test_stage_joints.py` beside `PINS`. Cost: a per-unit table (~170 entries) as code; data in code (AR-1 spirit) · (b) a new fixture `scripts/tests/fixtures/told-ratchet.json`, owner `test_stage_joints.py` in `test-layers.json`. Cost: one file, one owner row · (c) per-unit counts on the census rows. Cost: a census schema change in `test_judgment_census.py` (`_c2`), more writers of the census | **(b)** |

## 7. Small choices closed by the designer
C1 `EXIT_WRAPPERS` and `CHECK_PASSTHROUGH` are code constants. C2 T1-0 keys v1 so it needs no data edit. C3 window rows map to
`acceptance:<kind>`. C4 the T1a test is one table `WIDE_ROWS` with one test function. C5 the T1a step-0 stop copies the t-346 §3.2 form.
C6 T1b changes `own`'s seven call sites to full ids. C7 `told_ratchet` is written in two moves (T1b: `hand_cards`, `legacy_legs`; T1c:
`unsited`). C8 the rows file path is `C:\QAFactory\forge-repo\docs\tasks\specs\20261113-told-before-work-t1a-census-rows.md`, written by
the T1a-rows builder. C9 the universe member is a dict `{kind, where, stages}` (B2 (i)); kind is set by the producing member function.
C10 detector stages and merged row stages are in `stages.json` order (round 0 said "sorted"; identical for S0-S9). C11 T1a and T1b run in
separate worktrees `Wa\`/`Wb\` from B1 so two writers never share a tree; merge order T1a first. C12 the probe lives in the builder's
scratchpad and in the rows file's §0, never in the repo (doc-dispatch witness form).

## 8. Reading trail
Round 0: see git history of this file (§8 of round 0).
Round 1 (fix round), read: the critic verdict (whole); this spec (whole); `W\scripts\stage_joints.py:40-219, 265-294, 380-679` and Grep
`exit:|detector:|window:|startswith\(|split\(":"`; `W\scripts\tests\test_stage_joints.py:25-104` and Grep of the same pattern;
`W\scripts\tests\test_judgment_census.py:200-334, 436-455` and Grep `UNIT_NAME_RE|units_of\(|scan_files`; `W\scripts\refusal_registry.py:
1221-1240, 1333-1357, 1426-1441, 1455-1474, 1577-1651` and Grep `transport|counted_list|check_arg|stack\[0\]`; `W\scripts\contract_slices.py:
484-508`; `W\scripts\selftest.py:671-696, 712-727`; `W\scripts\tests\test_selftest_slow_tests.py:440-475`; package Grep
`["'f](exit|detector|window):` (files, then content without `test_stage_joints.py`); Grep `check:script|demand_tokens\(|PINS` over `W\`;
parent spec `:60-84` and Grep `selftest`; `.git/packed-refs` Grep `p1v`; `.git/refs/heads/wip/p1v-n4fix`, `p1v-n4b`; reflogs
`.git/logs/refs/heads/wip/p1v-{n0,n1,n2,n3,n4,n5,fix,topic,n4fix,n4b}`, `tbw-t1`; `.git/worktrees/*/HEAD` Grep; `.git/worktrees/p1v-n4fix/gitdir`;
n4fix tree: `exit_gate.py` Grep `def own|own\(`, `stage_joints.py` Grep `EXIT_SKIP|EXIT_WRAPPERS`, `test_stage_joints.py` Grep `"exit": 8`;
journal `logs/journal/dev1.jsonl:1370, 1384-1398`.
Not read: the bodies of `test_refusal_registry.py`, `_c3`, `stage_rows` beyond the call shape at `:203-204, 258`; the CI state of any
branch; whether the P1-v batch file is frozen (F9'). The probe of §3.2 was not run (no shell); its API calls are taken from the code read
above (`scan_files(root)` `:105`, `units_of(root, files, registry)` `:210`, `stage_rows(root)["detectors"]` `:203-204`, `sites`/
`raise_family` signatures `:1147, 1221`).
Needed beyond the manifest: `.git` refs and reflogs (B3 proof), `selftest.py`, `test_selftest_slow_tests.py`, `contract_slices.py`.

## 9. Noticed, not in scope
(a) `selftest._json_carrier` reads an unreadable carrier as `{}` and names nothing (`selftest.py:682-687`): an unknown read as "no test
names", for every carrier alike (gate-registry too) — an AR-28 instance outside T1; a finding for the selftest pile, not a T1 edit.
(b) `_census_blocking` calls `units_of(root, names)` with `registry=()` while `analyse` passes `REGISTRY` (`refusal_registry.py:1625`,
`test_judgment_census.py:443`): an a24-only unit in a blocking file is blocking in the census but not in the `--wide` list bound, so list
sites there are not counted by the join (fewer join units, never a rowless one). Measurement detail, not T1's.
(c) T2's `refusal` pass-through is cross-file (§4); the same-scope rule of §3.5 does not cover it — T2's spec states its rule.
(d) The verdict's B2 list missed reader r5 (`demand_tokens`, `check:script`): included in §3.4a, so in scope now.
(e) P1-v N4b (d8b86a6) is in work on top of 71d7ca8; §3.0 s3 says when it enters `wip/tbw-t1`.

## 10. Fix round (critic-on-plan verdict, 13.11.2026)

Blocking:
- **B1** — answered by §2.1 "THE UNIT SET" (`units_of` keeps `state != "walk_error"` AND `transport != "list"` records for both loops;
  POSITIONAL invariant "the list transport never creates or flips a census unit"), T1a E4, and the count: §2.1 "THE COUNT AND ITS PROOF"
  — the §3.2 probe (`python -B <scratchpad>\t1a_probe.py C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1\ai-packages\qa-factory`,
  source in §3.2) prints `A`, `B`, `C`, `old_units`, `new_units = old_units + |A| − |C|`; expected at a2c88d8 |A| = 113, |B| = 11,
  |C| = 1 (critic R1/R2), binding numbers from the B1 run; after T1a the same probe on `Wa\` prints `A`/`B`/`C` empty and
  `old_units` = the earlier `new_units`; the join prints `units_no_row 0`, `join_share 1.0`. Test rows `w-append-no-unit`,
  `w-append-no-flip` replace the unsatisfiable `w-append-no-census`.
- **B2** — answered by §3.4a: the member shape (kind set by the producer, `stages` for detectors), and the table of readers r1 `_pins`
  `:551-557`, r2 `audit` counts `:629`, r3 `no_detector` `:635-636`, r4 `_row_problems` `:497-498`, r5 `demand_tokens` `:279-280` (found
  in this round), r6 `_direction_a` `:546`, and the test lines, each with its behaviour after and its test row; T1b owns those functions
  (§3.0a), `_row_problems` by line (T1b: `:497-498` + signature; T1c: K3/K7/E4/E7 lines), sequential, T1b first.
- **B3** — answered by fact 0.7a and §3.0/§3.1: T1-0 is based on **71d7ca8** (`wip/p1v-n4fix`, accepted t-540), which descends from
  bea0bb0 (N0 + fix round) by the reflog chain n0 → n1 (created from bea0bb0) → n2 → n4 → topic c9b2069 → n4fix 71d7ca8; c9b2069
  (`wip/p1v-topic`) also holds N0 but lacks the N4 fix round. T1-0 lives on `wip/p1v-t10` on the P1-v line (F9' for the carrier);
  `wip/tbw-t1` merges it at s3 before step A and T1b. F9 (a) dropped; analog (ii) withdrawn.
- **B4** — answered by §3.5a: per counter where it is computed, compared and stored, and who loads the file: `hand_cards`,
  `legacy_legs`, `unsited` in `audit` / `stage-joints.json` (loaded by `load_rows` callers); `rowless`, `untold`, per-unit `bare`/`tagged`
  in `test_stage_joints.py` / `scripts/tests/fixtures/told-ratchet.json` (loaded only by that test; F11 (b)); literal ids all on the
  test-side leg, `audit` uses them only in the sited set; `told/audit-shape` proves `audit` reads no census.

Non-blocking:
- **N1** applied — §3.2 probe `holds()` uses the `units_of` rule (function or span); test row `w-flip-nested-span`.
- **N2** applied — rows file `ref` column and list C (§3.2 step 2), the reconciliation minus C (§2.1), T1a E10, test row
  `w-script-unit-replaced`.
- **N3** applied — §3.5 passthrough by the innermost def and bare-name call sites in the visible scope; T1c E8; test rows `pass/nested-def`,
  `pass/attr-call-same-name-ignored`.
- **N4** applied as fork F10 (recommendation (a): `selftest.py` leaves T1b's owns, the generic read stays; 0.19, T1b E4).
- **N5** applied — seven call sites (0.7, §3.4, T1b owns); `exit_gate:adviser` counted in `rowless`, row by T1r (§3.5a, §4); non-literal
  second argument edge T1b E6, test row `exit/non-literal-check`.
- **N6** applied — T1b writes the measured `hand_cards`/`legacy_legs`; a difference from 12/9 is a report line (0.18, §3.0a).
- **N7** applied — T1a witness reason corrected; the join command named as the real check of `_census_blocking` (§3.0a).
- **N8** applied — §3.0: base fix s3 before step A; T1a ∥ T1b after it; N4b timing rule.
- **N9** applied — `load_rows(path)` wraps `null_outcomes.load_data`, K10 texts unchanged (T1b E1, rows `v2/absent`, `v2/broken`);
  axis 16 line corrected (§5).

Base of each node: T1-0 — 71d7ca8 (`wip/p1v-t10`); T1a-rows — B1 (reads `W\`); T1b — B1 (`wip/tbw-t1b`); T1a — B1 (`wip/tbw-t1a`);
T1c — `wip/tbw-t1` after T1a and T1b. B1 = `wip/tbw-t1` (a2c88d8) + merge of `wip/p1v-t10` (hash at the s3 move).
Parallelism: T1-0 alone; then T1a-rows ∥ T1b; then T1a ∥ T1b (2 code writers); T1c alone.
Remaining forks: F9' (a), F10 (a), F11 (b) — §6.
Premises the verdict broke, checked against every node: "N0 on origin/main" (gone: T1-0 on the P1-v line); "list sites only inside
census units" (gone: the filter); "flip set = join set" (gone: the probe rule); "`test_refusal_registry` imports `units_of`" (gone); "six
call sites" (gone); "kind by prefix" (gone: §3.4a); "census counters in `audit`" (gone: §3.5a).
