# t-1554 card: dry seed ops for the unreachable S5-group rows (FV3-33 + FV3-25 item 2, FV3-36)

Draft by designer, 19.11.2026. Node live-run-fvf/3, feature F19. Two builder headers (section 6, 7), serial on `exits/s5.json`,
`seeds/s5.json`, `known_red/s5.json`, both after FV3-35 part A lands. Decisions belong to the Lead: section 8 (forks).

## 1. Scope, AR-n, variety

- Rows: 33 = FV3-33 12 (`code_close.{stage,factory_file,behind}/{retry,stop,free words,empty}`) + FV3-36 21
  (`s6.walk_supply/*` 5, `s6.walk_account/*` 5, `s6.data_change/*` 5, `kind:{data_change,walk_account,walk_supply}/{free words,empty}` 6).
  Counted in `exits/s5.json` :1356-1942 (row ids read). `code_close.closed_story/*` (3, S9) is out of scope.
- FV3-25: item 1 is answered by the FV3-35 diagnosis (t-1542 family B). Item 2 shrinks to the code-close ops of this card: nobody_* is a
  stub cause (FV3-35 A), repair_limit is a product fix (FV3-35 B), resume_limit* is a trace and then a product fix (FV3-35 C). Fork F6.
- AR-1 (closed variety is a data row): the seed op scripts stay ONE data tuple, `dry_exits.OP_SCRIPTS` (:79). Change check: grep
  `scripts/tests/` for a second list of op scripts or a script name branched in `run_seed`. Expect 0.
- AR-13 (a fact is read through its reader): a seed creates a state only through a real writer (P1-b §4.3 :446-450). The walker
  judges "reached" only by `pending_ask`. It never re-reads a product fact on its own. Change check: the diff adds no read of
  `driver-state.json`, `pipeline.json` or `config.json` to `dry_world.py`/`dry_exits.py`.
- AR-28 (an unknown never becomes a pass): an op that fails, times out, or exits 0 without creating its condition leaves the row
  red. The row is never skipped and never counted as reached. Change check: the selftest row of section 6 (test line 2).
- AR-29: the checks this card adds or alters, with their owners:
  - `_seed_problems` placeholder refusal (only if F2 is taken): owner data (code), class shape.
  - The `OP_SCRIPTS` membership of any new script (only if F1 (a) is taken): owner data (code), class xref.
  - The op-branch selftest case: owner data (code), class shape.
  - No role judgment is added or moved. Census rows: `scripts/tests/fixtures/judgment-census.json` covers product scripts. Whether
    test-layer checks are census rows is an `estimate`; the Lead runs `python -m pytest ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q`.
- Commit lines: in the form of `tools/architecture_gate.py` (the only carrier; not copied here). The judgment line is
  `judgment: none -- <why>` with its reason, for example "test-layer seed grammar and fixtures; no role judgment moves".
- `variety: none -- test layer only (dry world seeds, fixtures, walker grammar); no product code path, project table or config key changes how an axis is held`.

## 2. Measured by reading (designer trail; no shell)

| id | fact | carrier |
|---|---|---|
| M1 | The `op` step already exists. `[script, args]` from the closed list `story_step.py, stage_done.py, waiver.py, controller.py`; placeholders `{task_root}`, `{task}` only; runs in the COPY (`cwd=copy.root`, `env=copy.env`, `STORY_RUN_CLASS=dry`); exit != 0 is not reached with stderr cut at 400; timeout is over the cap | `dry_world.py::run_seed` :1226-1242; `dry_exits.py` :68, :79, :1308-1312 |
| M2 | No committed recipe uses `op` (Grep `"op"` over `fixtures/`: hits only in other fixtures, none in `stories/*/seeds`; the positive control is the same grep finding `synthetic-scenario/variants.json`). The op branch has grammar selftest rows (:2645-2665) and NO run row | `dry_exits.py` :2743-2830 |
| M3 | `dry_world.py --selftest` does not exist (Grep `selftest` in dry_world.py: 0; the positive control is the same file matching `say`). The walker's table is `dry_exits.py --selftest` (:3150-3175) | as stated |
| M4 | Every `code_close.*` recipe is `drive_until {stage: "S5", ...}` (seeds/s5.json :77-108). The only S5 code-close site is `s5.nothing` ("there was nothing to automate"), which dry-1 never takes (TC-1 is `auto`, kit.json :6). The sites a dry-1 road passes are S6/S7. Measured stop in known_red: "met the conductor at S7" | `driver_core.py` :391-405; `known_red/s5.json` :88-123 |
| M5 | The key is decided at `driver_machine.py::Driver.code_close` :2093-2137. `factory_file` = step `evidence` (`code_only_request` finds no evidence file, `stage_close.py` :261-267) or `entry` (`s7.repair_verdicts`, `driver_stage_s7.py` :289). `stage` = step `receipt` (the controller refuses `code_only`) or `record` (`stage_done` refuses), when the behind branch does not apply. `behind` = refusal text "required prior logical stage incomplete" + `code_close_facts.behind` + no running holder + not completed; asked at once when `awaits`, else on the 2nd refusal at the same revision (`CODE_CLOSE_IDLE_CAP = 2`, `driver_core.py` :410) | `controller.py::code_close_conflicts` :944-966, `code_close_facts` :901-941 |
| M6 | `walk_assign_step` runs only when `s6_walkers_cap() != 1 and len(plan["blocks"]) >= 2` | `driver_stage_s6.py` :1262 |
| M7 | walkers: an absent key reads 3 (`config_contract.py` :597, :606-607). The dry world's config is the template plus the file ticket adapter (`story_run_common.py::s0_project` :416-420; it does not pin walkers, unlike `seed()` :208-211). So cap != 1 already holds: `estimate` that the template carries 3 (pinned by `test_config_migration.py` :2050). The Lead can measure with `python -B -c "import json;print(json.load(open('<world>/qa-factory/config.json'))['manual'])"` on a scratch world | as stated |
| M8 | Lanes are cut by ACCOUNT KEY, at most `MANUAL_WINDOW_CASES = 3` per lane (`controller.py` :556, `walk_lanes` :645-657). A second guest manual case joins TC-2's lane, so it gives ONE lane. Two lanes need two different keys (or 4+ same-key cases). The key is the case request's `env`/`stand_account` actors (`manual_capture.py::lane_key` :1193-1204). `dry_stub.py` writes no actors (Grep `actors\|account` in dry_stub.py: no case-actor writer) | as stated |
| M9 | **Blocker for all 21 FV3-36 rows**: under the person's live no-stand word, the S6 manual half returns `manual_no_stand` BEFORE `walk_refuse_gaps` (:1257) and :1262. It has no lanes, no assignment and no account question. dry-1 passes the stand by "go on" (t-1542 run1 tail: "S5: stand not confirmed ... passed by the person's word \"go on\"") | `driver_stage_s6.py::manual_lane_plan` :1232-1239; `waiver.py::stand_passing_word` :408-410 |
| M10 | `walk_account` (works at walkers 1 too, :37): the lane key is exactly one `stand_account:<role>`, the role is not reserved, and the stand (`environments[0]`) records no two-key pair for it. The stand record must be readable (`walk_account_raise` :100-105) | `driver_stage_s6.py` :62-128 |
| M11 | `walk_supply` = (short pool parts and `accounts.known` false) or (alone kinds and `data.known` false), not asked before. `data_change` = alone kinds and `data.may_known` false and `walk_supply` already asked or known. So a `data_change` seed passes `walk_supply` first (an intermediate answer from story.json words) | `driver_stage_s6.py` :1472-1491 |
| M12 | The walker's row cap is `ROW_CAP_EXITS = 240` s. The main-pass prefix to S4 measured 110-153 s (t-1542 run1/run3) | `dry_world.py` :1075 |

## 3. Op table (op -> condition -> rows)

The ops are recipe steps or row `stub` fields. "candidate" means the condition is read from code and the reach is not measured.
The builder measures each one first (section 6/7 step 1).

| op | kind | condition it creates | rows | status |
|---|---|---|---|---|
| OP-CC-STAGE | `op: ["controller.py", ...]` in the S5 copy before `drive_until {stage: S6\|S7, question: code_close.stage}` | the controller refuses the receipt of the FIRST S6/S7 code close with a non-behind conflict. Candidate: a running holder ("checkpoint active work", which leaves the behind branch, M5) | code_close.stage/{retry, stop, free words, empty} (4) | candidate; F2 if it needs `--input` |
| OP-CC-FILE | row `stub` (existing grammar), no op | S7 entry: the failure analyst's repair-verdicts declaration cannot be read (`s7.repair_verdicts`, step `entry`). Fallback: evidence absent at an S6 site (step `evidence`) | code_close.factory_file/{retry, stop, free words, empty} (4) | candidate; needs a road that reaches S7 repairs (M4: the main stop is the S7 conductor) |
| OP-CC-BEHIND | `op: ["controller.py", "--operation", "<reopen of S5>", ...]` or a row `stub` that leaves S5 awaiting its consumer's acceptance (X7-6) | an S6 close while S5 is neither completed nor skipped, and nothing is running | code_close.behind/{retry, stop, free words, empty} (4) | candidate; risk: `where` routes back to S5 before any S6 close (M5 silent retry) |
| OP-STAND | an op on the closed list, or a new real writer (F1) | no live no-stand word at the S6 entry, AND a stand record `environments[0]` in config (M9, M10) | precondition of all 21 FV3-36 rows | **no closed-list op is known**: `waiver.py --revoke` (:1945) removes the word, but the next stand block asks the environment question again and story.json answers "go on" again. Fork F3 |
| OP-LANES | row `start` before S4 + row `stub` for `qa-case-designer` that adds manual cases with two distinct `stand_account:<role>` actors (needs a dry_stub override, M8) | 2+ lanes at the S6 entry; cap != 1 holds by default (M7) | the parallel road of s6.walk_supply/*, s6.data_change/*, kind:walk_supply/*, kind:data_change/* (14) | candidate; F4 (main pass or row time) |
| OP-NOPAIR | the same case-actor override (one lane is enough) + a stand whose `credentials_by_role` has no two-key pair for that role | `walk_gap_role` returns the role (M10) | s6.walk_account/* (5), kind:walk_account/* (2) = 7 | candidate; depends on OP-STAND |
| OP-SHORT | OP-LANES with both lanes on ONE role whose pool holds 1 account; `accounts_way` stays "not known" (template) | `short` non-empty, `accounts.known` false | s6.walk_supply/* (5), kind:walk_supply/* (2) = 7 | candidate; depends on OP-STAND, OP-LANES |
| OP-DATA | OP-LANES with a lane whose request needs an exclusive kind with no pool; story.json words for (S6, walk_supply) | alone kinds; `data.may_known` false after walk_supply | s6.data_change/* (5), kind:data_change/* (2) = 7 | candidate; depends on OP-STAND, OP-LANES |

Per row: every row of a key uses that key's op. The rows differ only by answer. 12 + 21 = 33 rows are covered, and none is
left without an op. Rows that no op can reach: if F3 is not resolved by a real writer, the 21 FV3-36 rows have no dry road. They
become `live_only` with the measured reason M9 (the builder's scratch run prints the S6 `not checked by an agent: no stand is
confirmed` line as the measurement) and the proposed node "dry stand" (F3 b). If the FV3-33 builder's step 1 shows that no
candidate reaches a code-close key, those 4 rows get `live_only` with the measured stop and a product-node proposal (F5).

## 4. Main pass

None of the recommended ops change the main pass. Ops and row `stub`s run only in a row's copy (`run_exit_row` :1323-1331). The
main pass reads `story.json`, `kit.json` and the story's default stub (`drive_main`). INVARIANT: the main pass's verdict line and
its snapshot list are byte-equal before and after the node. Exceptions: F4 (b), adding cases to kit.json, changes the main pass
by construction (S3/S4/S6 run three or more cases) and breaks two dry_stub selftest pins (`dry_stub.py` :1392-1393, :2103-2117).
F1 (b) changes nothing in the main pass, but it widens §4.3.

## 5. Edges (each with its invariant)

- E1 op exit != 0: row red, `op <script> exit N: <stderr 400>` (existing). INV: a failed op never yields reached; the row is never skipped.
- E2 op exit 0, condition not created: `drive_until` ends "did not reach"/"met ... at <stage>"; red. INV: reach is judged ONLY by the pending ask, never by an op's exit.
- E3 op over the row's budget: `over the cap at op <script>`, red (existing :1235-1239). AT the cap it still runs (the existing cap rows :2790-2800).
- E4 op script off `OP_SCRIPTS`: refused at load, before any world (existing :1311). INV: no file of the world is written by hand except `answer.md` and the control file (N4w :189).
- E5 (only if F2) a placeholder not in the fill map: refused at load and naming it. INV: never passed to a script literally. Today an unknown `{x}` passes literally (`run_seed` :1228-1229); that is the gap this edge closes.
- E6 TEMPORAL: FV3-35 A changes `exits/s5.json` and `known_red/s5.json` first. Before A lands, this node does not start. After it lands, the builder rebases, and `pins.known_red` is counted from A's value, never from 57.
- E7 POSITIONAL: the op step stands BEFORE the `drive_until` that meets the condition, and AFTER the snapshot copy. INV: the snapshot's tree hash is unchanged after the row (`dry_world.tree_hash`/`snapshot_red` :615-628), and an op never runs in the main world.
- E8 a row that becomes reachable and then fails a check stays red with its OWN measured FAIL text and a node. It never keeps "FV3-33"/"FV3-36" as its raised_by.
- E9 `pins.known_red` drops by exactly the removed rows, each named in the commit body. A row that moves to `live_only` leaves known_red and states its measured reason.
- E10 the 240 s row cap is not raised for these rows. A seed that needs more is red `over the cap` and is reported (F4 a measures it).
- E11 `code_close.behind` by its non-`awaits` road: the first refusal is a silent retry (`driver_machine.py` :2130-2136). The seed must keep the same revision for the second refusal. INV: the driver never closes a stage over an open earlier stage.
- E12 the stage of a `code_close.*` recipe is the stage of the measured site (S6/S7), never S5 (M4). The row `start` is a snapshot the main pass makes (S4 or S5).

## 6. Builder header A: FV3-33 (+ FV3-25 item 2)

given: this card §2-§5; `C:/QAFactory/forge-repo/docs/tasks/specs/reviews/t-1542-fv3-35-diagnosis.md` (probe method §(a)); `ai-packages/qa-factory/scripts/tests/dry_world.py::run_seed`; `ai-packages/qa-factory/scripts/tests/dry_exits.py::_seed_problems`, `::_selftest_cases`; `ai-packages/qa-factory/scripts/driver_machine.py::Driver.code_close`; `ai-packages/qa-factory/scripts/controller.py::code_close_conflicts`; `ai-packages/qa-factory/scripts/stage_close.py::close_by_code`
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/dry_exits.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/dry_world.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/dry_stub.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/seeds/s5.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/exits/s5.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/known_red/s5.json
non-goals: no product script edit (any `scripts/*.py` outside `scripts/tests/`); not the S6 rows (header B); not `code_close.closed_story`; no change to story.json, kit.json or the story's default stub; no new seed step kind beyond F1/F2 as the Lead decides
handoff: the branch + a report: per key, the measured site, the op chosen and the scratch-run verdict lines; rows moved to live_only with their measured stop
edges: E1-E9, E11, E12 of this card
DoD: step 1, measure: one scratch probe run (t-1542 §(a) method) from the S5 snapshot to the first code close, printing the site and step. Step 2: recipes with the chosen ops; `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/dry_exits.py --selftest` all cases pass; then `( cd C:/QAFactory/forge-repo/ai-packages/qa-factory && python -B scripts/tests/test_scenario_dry_1.py --part exits:s5 --exits-root <scratch with the 12 rows> --ledger <absent file> )`, each reached row PASS or its own measured FAIL (E8); `dry_exits.py --check` reports 0 discrepancies
siblings: FV3-35 A/B/C (same files, serial), FV3-28 (dropped answers), FV3-36 (header B, serial after this)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261119-fv3-33-36-dry-seed-ops-card.md
test: scratch exits-root run of code_close.stage/retry, code_close.factory_file/retry, code_close.behind/retry via test_scenario_dry_1.py --part exits:s5 (canon class: narrow call, report `not run locally: test_scenario_dry_1.py, canon judges`) | expected from: pile row FV3-33; this card §3, M5
test: dry_exits.py::_selftest_cases, a new row of the "drive_main and run_seed with a fake driver" table (:2743): an op that exits 0 continues; exit != 0 is not reached and names the script and exit; an op over the budget is not reached | expected from: this card E1-E3; N4w §4.3 / S-4
test: (only if F2) dry_exits.py::_selftest_cases, a variant of the seeds grammar row (:2645): an unknown placeholder is refused naming it | expected from: this card E5

## 7. Builder header B: FV3-36

given: this card §2-§5; `ai-packages/qa-factory/scripts/driver_stage_s6.py::manual_lane_plan`, `::walk_refuse_gaps`, `::walk_gap_role`, `::walk_assign_step`, `::walk_supply_raise`; `ai-packages/qa-factory/scripts/controller.py::walk_lanes`, `::lane_keys`; `ai-packages/qa-factory/scripts/manual_capture.py::lane_key`; `ai-packages/qa-factory/scripts/tests/dry_stub.py::stub_control`; header A's landed grammar
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/dry_stub.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/dry_exits.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/seeds/s5.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/exits/s5.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/known_red/s5.json
non-goals: no product script edit; no change to kit.json or story.json unless the Lead takes F4 (b); no file written by hand into a world (§4.3) unless the Lead takes F1 (b); the code_close rows
handoff: the branch + a report: per S6 key, the op and the scratch-run verdict lines, or the live_only rows with the measured M9 line
edges: E1-E4, E6-E10 of this card; plus: a stand record the op writes is read only through `manual_capture.load_config` (AR-13), and the case-actor override of dry_stub applies only to a row's control, never to the story's default stub (INV: §4 main pass byte-equal)
DoD: step 1, measure (bounded to one scratch run): from the S5 copy with OP-STAND's candidate, does the S6 entry leave `manual_no_stand`? If not, stop: the 21 rows become `live_only` with that measured line and the report names F3 (b). Step 2: the ops; `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/dry_stub.py --selftest` and `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/dry_exits.py --selftest` pass; a scratch exits-root run (same command as header A) of the four sample rows below, each PASS or its own measured FAIL
siblings: header A (serial before), FV3-21 (the no-stand word road), TR3-10d tests `test_walk_account.py`, `test_walk_supply.py` (unit side of the same questions; unchanged)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261119-fv3-33-36-dry-seed-ops-card.md
test: scratch exits-root run of s6.walk_account/added, s6.walk_supply/the app makes them, s6.data_change/only use what exists, kind:walk_supply/free words (canon class: narrow call) | expected from: pile row FV3-36; this card §3, M6-M11
test: dry_stub.py selftest, a variant row of the N2f case-file table (:2103-2117): a row control naming case actors writes `stand_account:<role>` on exactly those cases; the default control writes none | expected from: this card §3 OP-LANES, §4 invariant

## 8. Forks (the Lead decides)

- F1 grammar for world conditions with no closed-list writer (stand record, case actors). (a) Add the real writer
  `project_decisions.py` (it writes `credentials_by_role` pointers, `driver_stage_s6.py` :93-94) to `OP_SCRIPTS`: one data row,
  §4.3 holds. (b) A new step `world: {file, from}` that copies a story-folder file into the copy: it widens §4.3, a hand-written
  input (N4w F-W6 (c), declined 14.11). (c) Row `stub` only. **Recommend (a) + (c); never (b).**
- F2 a `{story_dir}` placeholder for an op's `--input` file kept in `fixtures/stories/dry-1/ops/` (a request to a real writer, not
  a world file). Needed only if an op is a `controller.py` APPLY operation with input (`controller.py` :9412-9414). **Recommend yes, with E5.**
- F3 the no-stand blocker (M9) for all 21 FV3-36 rows. (a) An op pair: revoke the word plus a stand that S6 treats as confirmed,
  by real writers (the confirming writer is unknown: `estimate`; header B step 1 measures it). (b) `live_only` with M9 measured,
  plus a new node "dry stand": a world variant with a confirmed stand, a sibling story or a fresh-start row. (c) A Lead decision
  to drop the no-stand answer from dry-1: that changes the main pass. **Recommend: try (a) in one bounded run, else (b).** One
  road: every S6 manual-lane question then has no dry proof until "dry stand" lands; the residual is a node with owns, not a note.
- F4 the second manual case. The Lead allowed it, but M8 shows one more guest case gives no second lane: two distinct account
  keys are needed. (a) Row-level: `start: S3` + a `qa-case-designer` stub override with actors; the main pass is unchanged; the
  row time is `estimate` 120-200 s against 240 s (header B measures). (b) kit.json gets TC-3/TC-4 with actors: it changes the main
  pass and two dry_stub pins. (c) live_only. **Recommend (a); (b) only if (a) runs over the cap.**
- F5 a code-close key no candidate reaches: `live_only` with the measured stop + a product-node proposal (which close the
  controller can never refuse in a dry road is itself a finding). **Recommend.**
- F6 FV3-25: close it when FV3-33 lands (item 1 is answered by t-1542, item 2 by this card), its finding pointing at FV3-35 A/B/C
  for the other keys. **Recommend**; the pile row and the finding are Lead files (not in these owns).

## 9. Small choices closed here

- The walker's selftest is `dry_exits.py --selftest` (M3); the DoD names it as "main's equivalent" of `dry_world.py --selftest`.
- The `code_close.*` recipe stage follows the measured site (E12); the rows' `start` may move from S4 to S5 to save row time.
- One op per condition; rows of one key share one recipe (the existing recipe ids are kept).

## 10. Readers of the touched files (rule 7)

The `tools/owns_readers.py` block was NOT attached to the brief. The Lead runs
`python -B tools/owns_readers.py --paths ai-packages/qa-factory/scripts/tests/dry_exits.py ai-packages/qa-factory/scripts/tests/dry_world.py ai-packages/qa-factory/scripts/tests/dry_stub.py ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/seeds/s5.json ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/exits/s5.json ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/known_red/s5.json --names OP_SCRIPTS run_seed _seed_problems stub_control`.
Hand reading meanwhile:

| file / name | reader | effect |
|---|---|---|
| `OP_SCRIPTS` | `dry_exits.py::_seed_problems` only (Grep over scripts/tests *.py: 2 hits, both dry_exits.py) | changes in A (F1 a) |
| `seeds/s5.json` | `dry_exits.load_seeds` <- `test_scenario_dry_1.py` | changes in A then B |
| `exits/s5.json` | `dry_exits` row loader, `dry_exits.py --check` (census), `test_scenario_dry_1.py` | changes in A then B (FV3-35 A first) |
| `known_red/s5.json` | `known_red.py`, `test_scenario_dry_1.py` (`pins.known_red`) | changes in A then B |
| `dry_stub.py` control | the stub process via `DRY_STUB_CONTROL`; its own selftest pins :1392, :2103-2117 | changes in A (only if OP-CC-FILE) and B; pins unchanged under F4 (a) |
| `run_seed` | `run_exit_row` :1331; dry_exits selftest :2767-2830 | changes in A only if F2 |
| `test-layers.json` covers of test_scenario_dry_1 (:5245-5256) | layer registry | unchanged |

## 11. Reading trail

Read: pile rows FV3-25/33/35/36 (batch-3 :54, :62, :64-65); FV3-25 finding (all); t-1542 diagnosis (all); `dry_world.py`
:255-364, :1179-1418; `dry_exits.py` :60-89, :1270-1330; `seeds/s5.json` (all); `exits/s5.json` :1350-1449, :1600-1680,
:1736-1866; `kit.json`; `selftest/{seeds,exits}`; `no_move.py` :490-580; `driver_machine.py` :2070-2150; `driver_dispatch.py`
:1265-1304, :2500-2577, :4120-4133; `driver_core.py` :380-410; `stage_close.py` :200-269; `controller.py` :645-694, :901-966,
:5670-5699, :9390-9414; `driver_stage_s6.py` :25-128, :1200-1284, :1324-1509; `manual_capture.py` :1193-1204;
`config_contract.py` :597-614 (grep); `story_run_common.py` :188-229, :405-426; `known_red/s5.json` :1-30, :88-123, :233-236;
N4w spec :470-489, :580-587; P1-b spec :440-453; `design/architecture.md` :28-72; `docs/TESTING.md` §«Строка теста в DoD»,
«Что запускать», «Бюджет»; `test-layers.json` :10-21, :5243-5256. Negative claims and their controls: M2, M3, M8, the
OP_SCRIPTS readers. No shell: every number above is read, not run. M7's template value and F4's row time are `estimate`.
