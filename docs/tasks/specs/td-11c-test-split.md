# TD-11 spec C — splitting the slow and large KEPT test files (draft, designer t-027, 11.11.2026)

Status: designer draft for Lead acceptance. Forks are in §8 and none is closed here. Paths are relative to
`ai-packages/qa-factory/` unless they start with `docs/`, `plans/`, `tools/` or `.github/`. The brief is
`docs/tasks/specs/td-11-lead-brief.md`. Spec A (`td-11a-driver-split.md`) did not exist when this was drafted
(Glob `docs/tasks/specs/td-11*` found only the brief), so §4.3 says what this spec REQUIRES of spec A's
protocol and does not define a protocol of its own.

## §1 Goal, honest frame, invariants

**Goal** (the owner's words 11.11.2026, brief l.8-9): slow test files that are not in quarantine are split, like the
large source files, so builders can work in parallel and run their witness quickly.

**Honest frame.** A split does **not** lower the total test time. Every part still builds its own driver or controller
world for each scenario. What a split buys is (1) parts a builder can run on their own and (2) CI shards that are more
even (`shard_files` never splits one file, `selftest.py:822-828`, so one 320 s file sets the floor for a whole shard).
Where the seconds come from: almost every GROUP 1 file builds a world PER SCENARIO (`seed()` makes a temp project and
initialises the controller, `story_run_common.py:188-213`; `project_of()` in `test_infra_failure.py:140-148`; `rig()` in
`test_no_move_seam.py:36-53`). That breaks the budget in `docs/TESTING.md:119-120` (one world per file). Fixing it is
named as its own follow-up node, **TD-11c-W** (§8 F7), and is NOT part of any split node: inside a split, a world
reused across scenarios would be a behaviour change.

**Behaviour does not change.** A part holds byte-identical bodies of the original functions. Any diff in behaviour is a
defect of the node.

| Invariant / rule | How a split touches it | How it is kept (the check goes into each node's DoD) |
|---|---|---|
| AR-13 one reader | `test-layers.json` is read only by `selftest.test_layers()` (`selftest.py:637`); `slow_tests.json` only by `slow_tests()` (`:992`) | no node adds a reader; the parts use the readers that exist |
| AR-14 one writer | keep rows are the hand-reviewed part of `test-layers.json`; a keep row leaves only through `tools/test_quarantine.py` (`drop-keep`, `test_quarantine.py:1409-1426`) | rows change only through the subcommand of F3, or by the F3 interim rule; the report names the writer of every file it touches |
| AR-15 one survivor | helpers move to ONE `<stem>_common.py`, never into a copy per part | witness (b) in §2.5: every top-level name exists exactly once |
| AR-19 stage twins | GROUP 2 test parts mirror the modules spec B cuts | a GROUP 2 node runs after its source cut (§7) |
| AR-20 shrink-only | `TEST_TIMEOUTS` only loses rows; `slow_tests.json` replaces one row with N rows (§4); the judgment census is not touched | the report lists every row it removed, added or re-pointed (key, before → after) |
| AR-22 producer and readers | test file names are read by carriers (§4) | the parts, their keep rows and every re-pointed carrier land in ONE push (§6 E6) |
| AR-23 empty outcome | a part with no scenario, or a shim with no check | every part holds at least one scenario; a shim defines no `test_*` function, so `ran_nothing` stays silent (`selftest.py:458-462`) |
| AR-28 unknown is never a pass | the seconds of a part are unknown until the first canon | a provisional number is written, never `null` (§4.2) |
| AR-29 where judgment lives | the checks this spec adds or changes are listed in the table below | each is a data check; none judges a role |
| FR-31 a test that fails only under load is a defect | a part that is green alone and red in the canon | treated as a test defect (`defect_found` on the node), never "fixed" by raising a ceiling (§6 E2) |
| FR-32, FR-54 | a sibling found while splitting (another carrier names the file) | re-pointed in the same push, or listed in the report |
| FR-37 the path in text is the path in code | comments and docstrings that name the old file (`controller.py:260`, `story_run.py:126`, `ticket_adapter.py:218`, `person_words.py:122`, `stage_guard.py:117`, `story_run_common.py:4,248`) | re-pointed to the part; a source file owned by spec A or B goes into "Needed from integration" instead of this node's owns |
| P16 | the parametrisation is kept; tables are not cut in the middle | a table function moves whole |
| P31 one road | every split uses the same road (F1) and the same rules (§2) | §8 F1, F6 |

Checks added or changed (rule 1 of the designer role, AR-29):

| Check | Where | Owner | Census class |
|---|---|---|---|
| split witness: top-level names before = after, bodies byte-identical, check-call count before = sum after | spec A's tool (F1), or the attached script on the interim road | data | forge tooling, outside the package census |
| `split-keep` door: one keep row becomes N rows that inherit its fields, and K5 accepts the line `keep-split:` | `tools/test_quarantine.py` (F3) | data | xref |
| `scenario_walk.py --witness-for` now picks a part's witness from the narrowed `covers` | already in place | data | — |

A reused function in a more consequential role: `--witness-for` reads `covers`. It may err toward a WIDER witness
(safe). It must never pick a NARROWER one. Inputs that must stay on the safe side: a path that no part's `covers` names
(it prints "run the whole scenario layer", the safe side); a common module (every part covers it, so all of them run);
a deleted old file name (counted as changed, TD-15 A.6).

## §2 Common rules

| # | Rule |
|---|---|
| 2.1 Naming | parts: `test_<old stem>_<topic>.py`, with the topic taken from the file's own section heading (examples: `test_infra_failure_retries.py`, `test_words_doors_detector.py`); helpers: `<old stem>_common.py`, following the precedent `story_step_common.py`. A helper that is already in `story_run_common.py` stays there. |
| 2.2 Shim | the old name survives as a shim **if and only if some other test file imports it** (found by the command in 2.6). The reason: an importer in quarantine must not be edited (TESTING.md:65), and leaving kept importers alone keeps every node's owns narrow. The shim follows `test_story_step.py`: it re-exports every name any importer uses, lists them in `__all__`, defines no `test_*`, holds no check, and runs the parts with `--all`. With no importer, the old file is deleted. |
| 2.3 Common helpers | a module-level name (helper, constant, class) used by two or more parts, or by any importer, moves to `<stem>_common.py` FIRST, in the node's first commit. A name used by one part only moves with that part. |
| 2.4 Time target | every part under **60 s in the CI canon**, measured only by the pipeline (`slow_tests.json` from `--slow-tests --from`). Times on the owner's machine are not judged: they differ from CI by several times (`selftest.py:134-148` notes 238 s on Windows against 20 s in CI). Number of parts = ceil(CI seconds / 50); the boundary follows the file's section comments; an estimate is an even share and is marked as unmeasured. |
| 2.5 No lost check (mechanical witness, attached in the report) | (a) check-call sites: `git grep -c -E "(^|[^A-Za-z_])check(_eq|_in|_not_in)?\(" <base-sha> -- <old path>` equals the sum of the same command (no sha) over the parts + common + shim. (b) names: `git grep -h -E "^(def|class) [A-Za-z0-9_]+" <base-sha> -- <old>`, sorted, equals the same over parts + common (one `main` per part excepted). (c) the run list: the union of the parts' run lists (`run_scenarios` arguments / `SCENARIOS` / calls in `main` / the `if __name__` block) equals the old one, each name once; the old order is kept inside each part, and so is membership in `side_by_side` vs `in_process`. (d) byte identity of every moved top-level node (F1 tool, or the attached AST script on the interim road). (e) each part run alone, `python -B scripts/tests/<part>.py`, with its tally line `=== <label>: X/Y ok ===` pasted (`harness.py:176-179`); the old Y is not measured (§9). |
| 2.6 Importer search | `git grep -n -E "^\s*(import|from)\s+<old stem>\b" -- ai-packages/qa-factory/scripts/tests`; its positive control is the same command for `test_controller_state`, which must find 51 files. The form `import a, <stem>` / `import_module("test_…")` was searched with the Grep tool and found nothing, with a same-shape control (`, harness` / `import_module("`) that found 55 lines. |
| 2.7 Carrier search | `git grep -n "<old stem>.py" -- ai-packages docs/SIBLING_MAP.md plans/builder-rules.md .github .gitlab-ci.yml`: every hit is re-pointed, or listed with the reason it stays (history: CHANGELOG, `changelog.d`, cohort records such as `keep_fail_at_entry`). |
| 2.8 Parts never import each other | a part imports only `harness`, `story_run_common`, its `<stem>_common` and package modules (§6 E8). |

## §3 Per file

The facts were checked on `main` a9bd758. Lines: Grep count of `^`. Check lines: Grep count of `\bcheck(_eq|_in|_not_in)?\(` (lines,
not runtime checks). Seconds: `scripts/slow_tests.json` (measured_on 2026-11-11, source selftest-8069755.txt). Keep layer:
`scripts/tests/test-layers.json` (keep section l.31-5324, pin_holds l.5325-5330). **None of the 21 candidates is in quarantine or in
pin_holds**: all 21 rows were matched below l.5325, and pin_holds holds four other files. World per scenario = W.

### 3.1 GROUP 1 (CI time over 100 s)

| File (keep layer, named by) | s / lines / check lines | Parts (old line ranges) | → common | Shim? (importers) | Ceiling removed |
|---|---|---|---|---|---|
| `test_infra_failure.py` (gate_named, state-exits.md:139) | 320.6 / 1139 / 244 | `_classify` K1 182-241, K11 741-804, K12-13 819-904, F4 1096-1121; `_stops` K2/K3/K7 243-387; `_retries` K4/K5 389-448, K6 450-522, K8 524-557; `_conductor_tracker` K9/K10/K15 559-740, 805-817; `_texts` K14 906-925, 927-1094. W (`project_of` → `T.seed`) | 1-179 (PRELUDE, entry, control, install, project_of, scenario, raised) | no (none) → delete | `TEST_TIMEOUTS` "test_infra_failure.py": 600 (`selftest.py:111`) |
| `test_story_run_refusals.py` (detector, named_by itself :472/:475) | 308.2 / 3699 / 629 | `_core` 55-942 (holds the census `every_action` 446-489); `_sources` 943-1336; `_resume` 1337-1944; `_t667_c21` 1945-2640; `_cc` 2641-3191 (census cc9 3126-3191); `_c24_n5` 3192-3665. W | recording_stub 44, git_fixture 943, RES_*/res_* 1340-1395 | **yes** (test_exit_ask_tools Q, test_story_run_s0 K) | :148 (600) |
| `test_story_run_s0.py` (detector, architecture.md:86) | 286.3 / 3082 / 448 | `_snapshot` 153-1285; `_source_list` 1286-1872; `_paste_owners` 1873-2675; `_c29` 2676-3026. Two run lists (`main` 3027-3077): each scenario stays in its list. W | 58-152 (FakeJira, rest_project …); its `from test_story_run_refusals import git_fixture` (1313, 1589) → `story_run_refusals_common` | no → delete | :121 (600) |
| `test_no_move_seam.py` (detector, architecture.md:192, SIBLING:123) | 283.0 / 2235 / 378 | `_n1_n9` 63-317; `_n2b_n15` 318-795; `_sites` 796-1389; `_k4s` 1405-1672 (+el12 1408); `_c26_g27_f2` 1673-2219 (+n24 1928). Three run blocks (`main` 1390, `k4s_run` 1668, `__main__` 2220-2235): one part per block | verdict/rig/raised 29-61, 318-351, module constants (FACTS, CTRL_BODY, C26_*) | **yes** (test_conductor_doors K: raised, rig, verdict) | :145 (600) |
| `test_story_run_stand_identity.py` (gate_named: gate-registry.json:479, driver-layers) | 274.3 / 1656 / 150 | `_k35_k36` 277-738; `_t366_k37` 739-982; `_k38_edges` 983-1367; `_ep1` 1368-1626. W (`Rig`) | 83-276 (Rig, record, matched …) | no → delete | — |
| `test_story_run_s6.py` (gate_named: gate-registry.json:459, driver-layers) | 219.4 / 2548 / 267 | `_d1` 66-275; `_manual` 276-968; `_t292` 969-1697; `_c16b` 1698-2041; `_hf2_11b` 2042-2510. W | _Awaits/AWAITS 18-29, ManualWorld, manual_rig, t292_config, Staleness, pin_project, d1_blocks, REPLAY_*, ACCEPTED_S6, WHY_RUN | **yes** (test_s6_reprove_manual Q, test_story_run_deferred K) | — |
| `test_story_run_freshness.py` (gate_named, state-exits.md:187,189) | 159.0 / 1349 / 202 | `_k1_k5` 201-307; `_k6_k7` 308-675; `_k8_k14` 676-1068; `_k15_k26` 1069-1322. `SCENARIOS` 1323 + argv filter kept per part. W | 57-200 scaffolding, 309-360 (gate_a_story, staged_driver …) | no → delete | :129 (600) |
| `test_words_doors.py` (detector, sole AR-24: architecture.md:164,249, SIBLING:141) | 134.3 / 1809 / 235 | `_detector` (a) 53-428 incl. renderer; `_doors` (b) 429-879; `_controller` (b, W3-D-B) 880-1567; `_flight_launcher` (c)+(d) 1568-1772 | INLINE_DOOR, PENDING, EXEMPT, scan, driver_inline_calls (the detector API that test_detector_verdict uses through `WD.`) | **yes** (test_detector_verdict K, test_story_run_repair_limit Q) | :126 (600) |
| `test_story_run_loop_b.py` (detector, state-exits.md:57) | 119.0 / 2067 / 422 | `_loop` start-1082 (the builder subdivides only if over target); `_threshold` 1083-1516; `_answers` 1517-2035 | helpers above 1083 used after it | no → delete | — |
| `test_handoff_values.py` (detector, state-exits.md:112 in row; text at :120) | 116.4 / 1663 / 287 | `_keys` 85-590; `_refusal` 591-1342 (A2 + HF8-7); `_main_block` 1343-1608 | scaffolding 31-84 | no → delete | — |
| `test_controller_rework.py` (detector, state-exits.md:32) | 107.0 / 2161 / 364 | `_jobs_guard` 63-328; `_repair_binding` 329-1009; `_window_words` 1010-2110 | at_s5, host_receipt, designer_story + refusal fixtures (importers' names) | **yes** (denial_scope Q, launch_card Q, resume_packet K, repair_limit Q, words_doors K) | — |
| `test_probe_by_code.py` (data_join) | 105.8 / 3160 / 516 | `_receipts` 1-954; `_reader_rundir` 955-2271 (the builder subdivides at a section comment only if the first canon shows it over target); `_second_probe` 2272-3101. ONE `def main` (3102); l.1845 is the scenario `main_exit_order_is_pinned`, called from `main` at 3152 (Lead correction at acceptance, §6 E11) | DISPATCH, TASK, PROVENANCE, FAKE_RUN_SUITE, PY, TEST_FILE_REL, env_for, cleanup_beside, tree_state, _calls, _main_in_process … | **yes** (_languages, _copy, _alternative, all K) | — |
| `test_grounding_table.py` (gate_named, gate-registry.json:647) | 105.8 / 929 / 182 | `_t1_t5` 139-532; `_projection_rest` 533-end | 1-138 | no → delete (text mentions in story_run_common.py:248, fixtures/grounding-table/README.md, test_s3_s4_chain.py:570) | — |
| `test_probe_by_code_languages.py` (gate_named, gate-registry.json:591) | 103.7 / 2273 / 369 | `_plan` 152-956 (languages, plan, lexer, candidates, guards, R6, R8); `_cli` 957-1681; `_ts_playwright` 1682-2235 | runner 42-151 | no → delete | — |

### 3.2 GROUP 2 (large files mirroring the sources spec B cuts)

Measured: these are NOT all fast. Over 60 s: gate_brief_and_retro 66.1, stage_guard 68.7, report_facts 61.4. Under:
gate_preflight 49.7, controller_state 18.6.

| File (keep layer) | s / lines / check lines | Boundary | Shim? | Carriers to re-point |
|---|---|---|---|---|
| `test_gate_preflight.py` (gate_named G13) | 49.7 / 5460 / 909 | one part per module of spec B's `gate_preflight.py` map; the section comments (1147, 1459, 2119, 2322, 2410, 2817, 2851, 3508, 3598, 4236, 4306, 4803, 5134) are the seams | yes (integrations Q, extra_accounts Q, words_doors K) | gate-registry.json:313,500,523 (the part holding each gate's proof) |
| `test_report_facts.py` (gate_named, "held by import") | 61.4 / 4970 / 1119 | spec B's 12 section markers of `report_facts.py`; the test sections at 176…4803 (the `main` at 4191 is not the end: sections follow it) | yes (branch_accounting, exploratory_answers, story_closed, whole_list_sites K; screenshots, traceability Q) | architecture.md:278 |
| `test_gate_brief_and_retro.py` (gate_named, state-exits.md:131) | 66.1 / 3545 / 764 | gate A / gate B and the themes of spec B's `gate_brief.py` map; test seams 1138, 2192, 2593, 2728 | no | state-exits.md:131; driver-layers source_readers :1233, source_mentions :1276 |
| `test_stage_guard.py` (table) | 68.7 / 2236 / 423 | no section comments: group by the function under test along spec B's `stage_guard.py` seams (hook rules / command forms / CLI) | no | refusal_registry.py `test` rows (:95, 118, 173, 185, 227, 247, 261, 273, 300, 312, 558, 743, read by `registry_proof_names`, `selftest.py:688`); SIBLING:241,279; state-exits.md:73; driver-layers source_mentions :1269; stage_guard.py:117 (spec B) |
| `test_controller_state.py` (detector AR-25: architecture.md:256-257, SIBLING:125) | 18.6 / 2423 / 192 | **recommended: do not split the checks** (§8 F5). Move the fixtures 51 files import (accept_stage, seed_plan, bind_gate_a, evidence_ref, record_stage_acceptance, add_override …) into `controller_state_common.py`; the file keeps its checks and re-exports the fixtures | the file itself stays | refusal_registry.py:580; env-facts-baseline.json:112 (ratchet fixture, axis 18 — check before editing); state-exits.md:22,57,62 |

### 3.3 Not split, and the open records

| File / record | Verdict |
|---|---|
| `test_probe_by_code_alternative.py` 337.0 s / 619 lines / 76 check lines (detector, state-exits.md:106) | not a split case: some 30 lines per check-call site means the seconds sit in a few scenarios (stub runs and processes). To decide, measure in CI: (1) seconds per scenario; (2) how many child processes each one spawns; (3) the time inside `probe_by_code` against harness setup. That goes to TD-11c-W (F7). By the 60 s rule this file fails; see F6. |
| `test_red_window.py` 85.8 s / 609 lines (detector, state-exits.md:36) — SC2-34 | still over the 60 s target (it was 7 min when found): 2 parts by the window themes, IF F6 answers "one rule for all". SC2-34 then closes with the node hash. |
| B-460 / PC1-5 (freshness split by scenarios; s0 and gate_repair within the limit; the 600 s ceiling removed) | freshness and s0 are done here, so PC1-5 is re-pointed to N7/N3. `test_story_run_gate_repair.py` is in quarantine (it was not among the keep rows matched) and is NOT touched; its ceiling `selftest.py:122` stays until purge (TD-15 C.1 item 5). |
| B-344, B-381 / PC1-4 (words_doors within the limit, its ceiling) | done by N8, which removes the ceiling at :126. |
| B-214 (infra_failure, story_run_s0; "remake split_witness.py") | done by N1/N3. `split_witness.py` is not in the tree (Glob `**/split_witness*.py` is empty; the same-shape control `**/piles_split*.py` finds `tools/piles_split.py`). Its role goes to F1. The "area table" of builder-rules item 7 that B-214 names no longer exists: item 7b l.22-25 is generic, and no candidate is named in `plans/builder-rules.md` (Grep -o found 10 other names). |

## §4 Registries a split must update

### 4.1 Table

| Registry | What changes | Rule |
|---|---|---|
| `scripts/tests/test-layers.json` keep | one row per part. Inherited: `layer`, `why` (+ " (part of <old> split, TD-11c)"), `named_by` (re-pointed to the part's carrier lines), `replaced_by`. `covers` per part = recomputed from the part's own imports + literal data files (TD-15 A.6), plus `tests/<stem>_common.py` | the union of the parts' `covers` ⊇ the old `covers`: no path loses its witness. Guard: `test_selftest_slow_tests.py:477-489` (every keep row covers the helpers it imports) and `:474-476` (gate_named ⊆ keep) |
| same — the old row | no shim: the row is removed (F3 subcommand, or interim: commit line `keep-drop: <old> -- split into <parts> (TD-11c)` with the file deleted in the same commit, which K5 accepts, `test_quarantine.py:1589-1592`). Shim: the row stays, `layer: data_join`, `why: "split shim: re-exports for <importers>; checks live in <parts>"`, `covers: ["tests/<stem>_common.py"]` | K5 refuses a keep removal without the door; the importers' rows that list `tests/<old>.py` stay valid (the file exists) |
| `scripts/slow_tests.json` | old row out; each part in with a PROVISIONAL `round(old × part check lines / total check lines, 1)` | not `null`: null weighs fast_under_s/2 = 2.5 s in sharding (`selftest.py:885`), which the canon would mis-shard. Provisional rows ≥ 5 s count as unchanged in the drift diff (`selftest.py:1104`), so `package-full-report` (max_drift 5, `nightly.yml:170` with `set -e`) stays green. After the first canon: `python -B scripts/selftest.py --slow-tests --from <ci-out/selftest.txt> --update`. A shim is not listed |
| `scripts/selftest.py` TEST_TIMEOUTS | rows removed: infra_failure :111, story_run_s0 :121, words_doors :126, story_run_freshness :129, no_move_seam :145, story_run_refusals :148 (6 of 16) | parts get no row (default 300). A part that needs more is E2, not a new ceiling. `selftest.py` is integrator-only (builder-rules item 1) → integrator commit |
| `references/gate-registry.json` `test` | re-point to the part holding the gate's proof (stand_identity :479, s6 :459, languages :591, grounding_table :647, gate_preflight :313/500/523) | `test_gate_registry.py:200-202` checks only that the file exists; a shim would pass that while being a lie, so the row must name the part (E4) |
| `scripts/refusal_registry.py` `test` (stage_guard ×12, controller_state :580) | re-point to the part | read by `gate_named_files` (`selftest.py:709-724`) |
| `design/state-exits.md` backticked proofs | re-point (lines in §3) | `_PROOF_IN_BACKTICKS`, `selftest.py:659,718` |
| `design/architecture.md` (86, 164, 250, 257, 278), `docs/SIBLING_MAP.md` (123, 125, 141, 241, 279) | re-point to the part that holds the detector | prose carriers (`selftest.py:661`; `FORGE_CARRIERS`, `test_quarantine.py:50`) |
| `scripts/tests/fixtures/driver-layers.json` `source_readers` / `source_mentions` | `file` re-pointed to the part that now holds the `function` (rows for refusals, s0, s6, stand_identity, words_doors, gate_brief_and_retro, infra_failure, stage_guard, l.1231-1292) | L8 of `test_driver_layers.py:581-614` keys rows by (file, function). Spec A rewrites the same file (single copy) |
| `references/stage-joints.json`, `install_smoke.py`, `.gitlab-ci.yml`, `.github/workflows/*`, `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`, `plans/builder-rules.md` | nothing: no candidate is named there (the carrier Grep found hits only in SIBLING_MAP among these, and found other test names in builder-rules) | — |
| `tools/test_quarantine.py` | F3: `split-keep` subcommand + K5 door | spec below |

### 4.2 `split-keep` (F3 recommendation)

`python tools/test_quarantine.py split-keep OLD --into P1,P2[,...] [--shim] --reason TEXT` reads the OLD row, writes
one row per part (fields inherited as in §4.1; `covers` copied whole: the node narrows it by hand afterwards, which
TD-15 A.6 allows since a new row is no removal), and either deletes OLD's row (no `--shim`) or rewrites it as the shim
row. It writes `ci-out/keep-split-msg.txt` with `keep-split: OLD -> P1, P2 -- <reason>` plus the gate lines (AR-14).
K5 (`check_history`, `test_quarantine.py:1589-1592`) also accepts a removed keep row whose name is the OLD of a
`keep-split:` line in the same commit, when every named part exists in that commit's keep. Refusals: OLD is not a keep
row; a part is already a row; a part is not on disk; a part is a quarantine name (it never returns); an empty reason.
Today's tool needs no subcommand for the no-shim case (the `keep-drop:` door plus hand-written rows, §4.1); the
subcommand removes the hand-written inheritance, so only one writer touches the keep rows.

### 4.3 What this spec requires of spec A's protocol for single-copy registries

R-A1: a split node does NOT commit `test-layers.json`, `slow_tests.json`, `selftest.py`, `gate-registry.json`,
`refusal_registry.py`, `state-exits.md`, `architecture.md`, `SIBLING_MAP.md` or `driver-layers.json`. It hands its rows
in the report as a block that can be applied (key → new value, old → new line), and the integrator writes all of them in
ONE closing commit of the batch. R-A2: the closing commit and the node merges go to `main` in ONE push, and the batch
canon runs on that head (E6). R-A3 (only if F1 = the tool): spec A's transfer tool takes a test file and a map with
`names: {name, kind, home}`, where `home` is a part stem or `<stem>_common`. It generates each part's header (the
imports of the names it uses) and its `main` (the old run list restricted to the part, in the old order, keeping
`side_by_side`/`in_process` membership and argv filters). With `--shim` it generates the re-exporting shim. It prints
witness 2.5 (a)-(d).

## §5 Wording for docs/TESTING.md (fork F2, the owner's word)

Add after l.118 (section «Бюджет», item «Файлы»):

> Части разрезанного оставленного файла — не новый тестовый файл: каждая часть наследует строку `keep` исходного (слой,
> причину, `named_by`; `covers` сужается по своим импортам, но вместе части покрывают всё, что покрывал исходный), а
> исходная строка уходит командой `tools/test_quarantine.py split-keep`. Правило «10 с на новый файл» к частям не
> применяется: их цель — до 60 с в каноне CI (спека `docs/tasks/specs/td-11c-test-split.md`).

## §6 Edge behaviours (each with the invariant it protects)

| # | Edge | Behaviour | Invariant |
|---|---|---|---|
| E1 | sections share module-level state built once at import (no_move_seam FACTS → C26_FACTS; words_doors PENDING/EXEMPT; s6 AWAITS) | a pure constant moves to common and is imported. A constant that builds a world or touches the disk at import stays in common and is now built once PER PART: the report names it with its cost | no scenario sees a different value than before; no hidden world is added silently |
| E2 | a part still over 60 s at the first canon | not split again inside the node; the report line names it, and it goes to TD-11c-W. No `TEST_TIMEOUTS` row unless the part runs over 300 s, and then only with a `defect_found` (FR-31) | a ceiling never makes slowness acceptable |
| E3 | a helper used by exactly one other test (an importer) | it moves to common (rule 2.3: any importer counts) and the shim re-exports it; the importer is not edited | a quarantined importer is never edited; a kept importer is not widened into owns |
| E4 | a file that a design doc or registry names as a `gate_named`/detector proof | the scenarios that carry that proof stay together in ONE part, and the carrier is re-pointed to it; the shim is never the named proof | a carrier never names a file with no check (`test_gate_registry.py:202` would pass a shim: it checks existence only) |
| E5 | a file in pin_holds | none of the 21 is (pin_holds l.5325-5330). If one gets there before its node runs, the node stops and reports: pin_holds are Lead-decided pins | a pin is never moved without its registry decision |
| E6 | temporal: a part on disk without a keep row → the canon prints `unlisted:` (`selftest.py:747`) | the node branch is never canonised alone; the parts + rows + slow_tests + timeouts + carriers reach `main` in ONE push (R-A1/2). Before the push the old world holds (the old file is listed); after it, the new one. The node's local witness runs the parts directly (the listing does not affect a direct run) | a test file is never on `main` unlisted; a keep row never names a missing file (`selftest.py:741`) |
| E7 | a file with both a slow_tests row and a TEST_TIMEOUTS row (infra, s0, words_doors, freshness, no_move_seam, refusals) | both change in the same closing commit: the ceiling row is removed and the slow row is replaced by the part rows | the two registries never disagree about whether a file exists |
| E8 | parts that would import each other | forbidden. The shared name moves to common. A cycle found by witness 2.5(b) is a node defect | each part runs alone (needed for the shards and the builder's witness) |
| E9 | quarantined siblings of a kept file (test_story_run_gate_repair, test_exit_ask_tools, test_s6_reprove_manual …) | not touched. They keep importing the old name through the shim. The watch (`quarantine-watch.yml`) shows them as before. If one turns red because of the split (a name missing from the shim), the shim is fixed; the quarantined file never is (Lead marks it "перенос TD-11", brief l.29) | K5: a quarantined file is never edited (`test_quarantine.py:1576-1580`) |
| E10 | Windows vs Linux timing | the target and slow_tests are judged only on CI Linux (python:3.12, `--jobs 4`). Local seconds are reported, never judged; a part green on Windows and red on Linux is a test defect (builder-rules 7b l.39-45) | no measured constant is pinned (TESTING.md l.95) |
| E11 | a top-level function that no run list calls (general case; the draft's instance — "two `def main` in test_probe_by_code" — was false: Grep `^def main` finds `main_exit_order_is_pinned` at 1845 and the one `main` at 3102) | the parts carry the run list of the file's `main`. A function no run list reaches moves with its section, is listed in the report and is not added to a run list (behaviour unchanged); Lead decides | the split never quietly starts running checks that never ran (or stops running ones that did) |
| E12 | a red check present at the split (freshness is in `keep_fail_at_entry`, test-layers.json l.5356) | it stays red, in its part; the node does not repair it | a split never hides or repairs a red |
| E13 | a source-reading test (census over `story_run.py`/`controller.py` text: refusals 446-489 and cc9, s0 k5/k6, s6 d1_texts, stand_identity k37, words_doors driver_inline_calls) | moved byte-identical; after spec A's cut, spec A re-points the read (driver-layers L8 rows) | one reader per census (AR-13); a census never reads an empty file |
| E14 | argv selection of scenarios (infra 1133-1137, freshness `chosen` 1337-1344) | kept in every part, same semantics | a mutation control that names one scenario still runs only that one |

## §7 Nodes, manifests, parallel groups

Template for every node (header lines per R11-f; the owns differ per node, see the table):

```
given: docs/tasks/specs/td-11c-test-split.md §2, §3 (its row), §4, §6; plans/builder-rules.md; ai-packages/qa-factory/design/factory-rules.md; docs/TESTING.md; the old file; scripts/tests/story_run_common.py; scripts/tests/test_story_step.py (shim precedent)
owns: <absolute paths from the table>
non-goals: no behaviour change; no world reuse (TD-11c-W); no quarantined file; no importer edited; no single-copy registry committed (rows go in the report, R-A1); no source file
handoff: docs/tasks/handoffs/<task>-td11c-<node>.md — the witness 2.5 (a)-(e) verbatim + the registry row block + "Needed from integration"
edges: E1-E14 of §6
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>` then each part alone: `python -B ai-packages/qa-factory/scripts/tests/<part>.py` (the tally line pasted; duration reported, not judged)
```

Root of the absolute paths: `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\`. Each node owns: the old file, its parts, and
`<stem>_common.py`.

| Node | File | Parts (new files) | Wave |
|---|---|---|---|
| N1 | test_infra_failure.py | test_infra_failure_{classify,stops,retries,conductor_tracker,texts}.py, infra_failure_common.py | 1 |
| N2 | test_no_move_seam.py (+shim) | test_no_move_seam_{n1_n9,n2b_n15,sites,k4s,c26_g27_f2}.py, no_move_seam_common.py | 1 |
| N3 | test_story_run_freshness.py | test_story_run_freshness_{k1_k5,k6_k7,k8_k14,k15_k26}.py, story_run_freshness_common.py | 1 |
| N4 | test_story_run_loop_b.py | test_story_run_loop_b_{loop,threshold,answers}.py, story_run_loop_b_common.py | 1 |
| N5 | test_handoff_values.py | test_handoff_values_{keys,refusal,main_block}.py, handoff_values_common.py | 1 |
| N6 | test_controller_rework.py (+shim) | test_controller_rework_{jobs_guard,repair_binding,window_words}.py, controller_rework_common.py | 1 |
| N7 | test_probe_by_code.py (+shim) | test_probe_by_code_{receipts,reader_rundir,second_probe}.py, probe_by_code_common.py | 2 |
| N8 | test_grounding_table.py | test_grounding_table_{t1_t5,projection_rest}.py, grounding_table_common.py | 2 |
| N9 | test_probe_by_code_languages.py | test_probe_by_code_languages_{plan,cli,ts_playwright}.py, probe_by_code_languages_common.py | 2 |
| N10 | test_red_window.py (if F6) | test_red_window_{a,b}.py by window theme, red_window_common.py | 2 |
| N11 | test_story_run_refusals.py (+shim) | test_story_run_refusals_{core,sources,resume,t667_c21,cc,c24_n5}.py, story_run_refusals_common.py | 3 (after spec A phase 1, F8) |
| N12 | test_story_run_s0.py | test_story_run_s0_{snapshot,source_list,paste_owners,c29}.py, story_run_s0_common.py | 3 (after N11: it imports git_fixture) |
| N13 | test_story_run_s6.py (+shim) | test_story_run_s6_{d1,manual,t292,c16b,hf2_11b}.py, story_run_s6_common.py | 3 |
| N14 | test_story_run_stand_identity.py | test_story_run_stand_identity_{k35_k36,t366_k37,k38_edges,ep1}.py, story_run_stand_identity_common.py | 3 |
| N15 | test_words_doors.py (+shim) | test_words_doors_{detector,doors,controller,flight_launcher}.py, words_doors_common.py | 3 |
| G1-G4 | test_gate_preflight / report_facts / gate_brief_and_retro / stage_guard | one part per spec B module | after (or with) spec B's cut of the same source |
| G5 | test_controller_state.py | controller_state_common.py (fixtures only, F5) | after spec B's controller map |
| NC | integrator closing commit | the registry rows of all nodes (§4.1), TEST_TIMEOUTS, F3 subcommand if accepted (`tools/test_quarantine.py`, `tools/test_test_quarantine.py` row) | last, one push |

Waves: at most 6 writers at once (host adaptation 6). Wave 1 = six files that read no driver source. Wave 2 = the probe
family + red_window. Wave 3 = the story_run source readers, after spec A phase 1 (F8). Nodes in different files share no
owns; the only shared files are the registries, which NC writes.

## §8 Forks (each with a recommendation; a builder works by the recommendation until answered)

| # | Fork | Options | Recommendation and what is done meanwhile |
|---|---|---|---|
| F1 | the road a split moves code by | (a) spec A's committed transfer tool with a map per test file (R-A3); (b) by hand + an attached AST witness | (a): P31 (one road for every file, the Lead's own decision on sources, brief l.17-19) and repeatable over a fresh `main`. Covering (b) would cost a second witness script and a second road. Meanwhile: wave 1 starts once spec A's tool exists; until then, no split node starts |
| F2 | §5 sentence in docs/TESTING.md | add as drafted / reword / none | add as drafted (owner's word needed: TESTING.md is the owner's rule). Meanwhile the brief's reading holds (l.26-28). **ANSWERED — the owner, 11.11.2026: add as drafted; written into `docs/TESTING.md` («Бюджет», «Файлы»)** |
| F3 | keep row replacement | (a) new `split-keep` subcommand + K5 door (§4.2); (b) today's `keep-drop:` door + hand-written rows | (a): one writer of keep rows (AR-14), inheritance by code. Meanwhile (b) |
| F4 | time target | 60 s per part in CI (≈ 60 new files) / 120 s (about half as many files) | 60 s (the brief's "under a minute"). Meanwhile 60 |
| F5 | test_controller_state.py (18.6 s) | move only its fixtures to a common module / split its checks too | fixtures only: splitting the checks buys no time and gives the 51 importers no parallelism. Meanwhile fixtures only |
| F6 | one size rule for every kept file: red_window (85.8 s) and probe_by_code_alternative (337 s / 619 lines) | (a) red_window split by the 60 s rule; alternative goes to TD-11c-W as a named node with owns and a test; (b) leave both | (a): the same rule for every file (P31). A file that splitting cannot fix is a node in TD-11c-W, not an exception. Meanwhile (a) |
| F7 | world per scenario (the real cost) | a follow-up node TD-11c-W ("one world per file", TESTING.md:119-120, starting with alternative, infra_failure, s0, refusals) / nothing | open TD-11c-W as its own node after the splits (smaller files make it cheaper). Meanwhile the splits do not touch worlds. **ANSWERED — the owner's word 11.11.2026: the node is done in this work, not left for later; its spec is `docs/tasks/specs/td-11d-world-per-file.md` (designer t-030)** |
| F8 | story_run source readers: before or after spec A's cut | after spec A phase 1 / before | after: these tests read `story_run.py` text, and spec A re-points the same functions and the driver-layers L8 rows. Splitting first means two nodes on the same functions and rows, and a merge conflict. Meanwhile N11-N15 wait for spec A phase 1 |
| F9 | the shim rule | the shim survives iff any importer exists (2.2) / edit kept importers so that only quarantined ones force a shim | 2.2: owns stay narrow and kept importers are not edited by a split. Meanwhile 2.2 |

Small choices closed here (no design weight): naming 2.1; provisional slow_tests numbers by check-line share; shim row layer
`data_join`; the per-part `main` keeps the old `harness.finish` label + the part suffix.

## §9 Not verified by this draft

- Per-scenario seconds: no file has them, so part balance is estimated from check-line shares. The first canon decides (E2).
- The runtime tally Y of the old files (running them locally is barred by PROJECT.md item 2): witness 2.5 is static + per part.
- `dup_ratchet` / `lint_ratchet` reaction to moved test code (whether tests are in their scope): the integrator reads it in the batch canon.
- `audit_factory.py:1618` (names test_no_move_seam.py), `test_current_audit_contract.py:79-91` and `test_selftest_slow_tests.py:31-180`
  (they name candidate files; whether as live carriers or as sample strings was not read). Their keep/quarantine status was not checked. N2/N1/N15 read them first.
- `env-facts-baseline.json:112` (a ratchet fixture, AR-20): whether re-pointing it counts as a raise.
- Inner boundaries of `test_story_run_loop_b.py` 1-1082, of `test_stage_guard.py` (no section comments) and of the GROUP 2 parts (they wait for spec B's maps).
- That `test_gate_registry` / `test_refusal_registry` check nothing beyond the existence of a re-pointed proof (only `test_gate_registry.py:200-202` was read).
- The line numbers in `named_by` of existing rows are partly stale (handoff_values names state-exits.md:112, the text is at :120): the nodes re-point to the current lines.
