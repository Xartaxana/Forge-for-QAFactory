# PC4-19 builder card: split the package test files near the 300 s CI cap (designer draft, t-1248, 17.11.2026)

Status: designer draft for Lead acceptance; fix round of the plan critic t-1251 applied (resubmission t-1256, section
«Fix round t-1251» at the end). Forks are in §8. None of them is closed here; each builder works by the
recommendation until the Lead answers. Node: `package-ci/4/PC4-19`, finding
`plans/piles/package-ci/findings/20261117-tests-near-the-300s-ci-cap.md`. The card executes spec C
(`docs/tasks/specs/td-11c-test-split.md`, §2 rules, §4 registries, §6 edges E1-E14) for the files below. Only the deltas
are written here. A rule spec C already states is pointed at, not copied.

Paths: `<T>` = `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\`; `<R>` = `C:\QAFactory\forge-repo\`.

## §0 Measured facts (each with its carrier)

| Fact | Carrier |
|---|---|
| The default per-file timeout is 300 s. Neither `test_stage_joints.py` nor `test_probe_by_code.py` has a `TEST_TIMEOUTS` row. `test_scenario_dry_1.py` has 900 s (the dry-story exception) | `scripts/selftest.py:105-160` (row at :118), the runner call at :494 `run_subprocess([str(path)], timeout=TEST_TIMEOUTS.get(path.name, 300))` |
| The runner starts a test file with NO arguments. So an argv row-shard (`--shard i/n`) would need a runner and CI change | `selftest.py:494` |
| CI seconds, measured_on 2026-11-17: stage_joints 259.4, dry_1 221.6, probe_by_code 206.8 | `scripts/slow_tests.json:83,125,132` |
| Brief figures, not re-read (no shell in this role): probe_by_code timed out at 300 s in 4 canons today (44136543304, 44138582097, 44145802589, the bw-int run); stage_joints 237-300 s; dry_1 262 s | dispatch `edges:` |
| Older local artifacts (run ids unknown; from before the TD-11c wave 1, since `test_infra_failure.py` is still whole there): stage_joints 48.6-83.8 s, probe_by_code 138.3-226.4 s (red twice, 755/762 and 756/762). So stage_joints grew about 4x since the told-before-work rows (K1 pin: 285 rows) | `ci-out/{art1,art2,c2,c3,c4,nightly-43178152997,canon-pc23}/*.txt` (Grep for the three names) |
| **No per-group timing exists in any CI log.** `selftest` prints one seconds figure per FILE (`check(..., seconds=)`, `selftest.py:174-178`). `harness.py` has no clock (Grep `perf_counter\|monotonic\|elapsed\|seconds` returns nothing; positive control: `def (finish\|check)\b` finds :115 and :225). So part balance below is an ESTIMATE by line-span share, marked unmeasured (spec C 2.4). The first batch canon after the split measures each part, which is the CI timing check (§3) | as cited |
| Line counts: stage_joints 1237 lines, `main` at 1208 with 23 direct calls. probe_by_code 3308 lines (spec C measured 3160 at 105.8 s), one `def main` at 3247 that holds inline set-up blocks (`temp_dir`, `project()`, try/finally, `if record:`). dry_1 155 lines, an argparse `main` | Grep `^` count; Read of each `main` |
| `tools/test_split.py` recognises only direct zero-argument calls, `run_scenarios(literal lists)`, `finish(label)` and a literal `for` in a runner. Any other statement is refused with its line (`_fill_stmt_block`, :695-708). So probe_by_code's `main` is refused as it stands (prep step B0 below). It also ACCEPTS bare module-level calls (`kind="call"`, :506-512) and a module-level `finish` (:485-489, `_is_finish` :273-277), and the parts it writes then keep them at module level; proof (g) imports each part alone (:1804), so such a part runs every check plus `finish` (`sys.exit`, `harness.py:225-229`) at import, under the 120 s per-file `IMPORT_TIMEOUT` (:82). Hence prep step D0 below (t-1251 finding 1) | `tools/test_split.py:18-56, 641-708`; t-1251 trail for :82, :273-277, :485-512, :1804 |
| `tools/test_quarantine.py split-keep OLD --into P1,... [--shim [--importers ...]] --reason` exists, and so does its K5 door (`keep-split:` line). K5 refuses a part not named `test_<old stem>_<topic>.py` | `tools/test_quarantine.py:11, 1444-1506, 1642-1668` |
| Importers: `test_probe_by_code` is imported by 5 files (shim needed). `test_stage_joints` by none (no shim; the old file is deleted). `test_scenario_dry_1` by `dry_exits.py:2666` | Grep `^\s*(import\|from)\s+(test_probe_by_code\|test_stage_joints\|test_scenario_dry_1)\b` over `scripts/`: 7 hits |
| `test_stage_joints.py` is read by name: `CONTRACT_TESTS` (`selftest.py:568`, run by `--contracts`, and fed into `gate_named_files` at :727), the `fixture_owners` row `"told-ratchet.json": "test_stage_joints.py"` (`test-layers.json:34`), and the prose detector lines AR-10 (`design/architecture.md:155`) and AR-22 (:277) | Grep (§6) |
| A kept file already shares the prefix: `test_stage_joints_12586.py` (keep row `test-layers.json:5429`; named by `references/stage-joints.json:88,594`). Stream B's prefix is shared by five kept files: `test_probe_by_code_{alternative,copy,languages_cli,languages_plan,languages_ts_playwright}.py`. Stream D's prefix by none | Grep; Glob `test_probe_by_code*.py` in `<T>` (6 files: the five + the old file); Glob `test_story_sides*.py` in `<T>` (1 file: the old file, the positive control) |
| The dry story's later stages start from snapshots made by THIS process. A snapshot made by another process is refused (E16): `dry_world.py:41` (`RUN_LABEL` per process), `:364-376` (`from_snapshot`) | Read/Grep `dry_world.py` |
| `test_story_sides.py`: 354.7 s on CI under a 600 s ceiling raised 13.11 ("the cost cut is queued", `selftest.py:155-159`). No node in any batch file splits it (Grep `test_story_sides` over `plans/piles/*/batch-*.md`: only PC1-1, PC3-1). `test_story_run_stand_identity.py`: 205.7 s with NO ceiling (default 300). It is node PC4-10 N14, status "ожидает" | `slow_tests.json:151,153`; `selftest.py:110-160` (no stand_identity row); `batch-4-...md:31` |

## §1 Invariants, checks, variety

**AR-n touched** (each change check goes into the DoD of §3 and §4):

| AR | How the card touches it | Change check (in DoD) |
|---|---|---|
| AR-13 one reader | `test-layers.json`, `slow_tests.json` are read only by `selftest.test_layers()` / `slow_tests()` | no part, common module or tool run adds a reader; the report says so |
| AR-14 one writer | keep rows | rows change only through `split-keep` (integrator, §4), with the `keep-split:` line in the commit |
| AR-15 one survivor | helpers shared by two parts or by an importer | in ONE `<stem>_common.py`; proof (b) of `test_split.py`: every top-level name exactly once |
| AR-20 shrink-only | `test-layers.json` keep (a row leaves only through the tool), `TEST_TIMEOUTS`, `slow_tests.json` | no `TEST_TIMEOUTS` row added or raised (the dry_1 900 stays as it is); the `"test_story_sides.py": 600` row and its comment leave with the deleted file (a shrink, §4); the report lists every row added, removed or re-pointed (key, old -> new) |
| AR-22 producer/readers | the old file names are read by `CONTRACT_TESTS`, `TEST_TIMEOUTS`, `fixture_owners`, architecture.md AR-10/AR-22 detector lines, `told-ratchet.json` note, `slow_tests.json`, the importers' keep-row `covers`, the `PINNED_ELSEWHERE` value at `test_conductor_doors.py:679` | every reader in §6 is re-pointed in the SAME push as the parts (E-6) |
| AR-23 empty outcome | a part with no scenario; the shim | each part holds at least one run-list entry; the shim defines no `test_*` |
| AR-28 unknown is no pass | a part's seconds before its first canon | provisional `slow_tests.json` numbers, never `null` (spec C §4.1) |
| AR-29 where judgment lives | the checks below | each is a data check; none judges a role |
| AR-10, AR-22 (detector text) | `design/architecture.md:155,277` name `test_stage_joints.py` as the walk's detector | re-pointed to the part holding the real-tree walk (`test_stage_joints_k1_k8.py`) in the closing commit |

**Checks added or altered, their owner and census class** (AR-29; CLAUDE.md rule 10, P27):

| Check | Where | Owner | Census class |
|---|---|---|---|
| split proof (a)-(g): sites, names, run list, byte identity, compile, one closing, import alone | `tools/test_split.py` (forge) | data | forge tooling, outside the package census |
| `keep-split:` K5 door | `tools/test_quarantine.py` (forge) | data | xref (forge) |
| `CONTRACT_TESTS` names the six stage-joints parts instead of one file | `scripts/selftest.py:568` | data | not a check unit (a list of files the runner runs), so no census row |
| `fixture_owners` re-pointed | `test-layers.json:34` | data | xref |
| CI timing check: each part under the target on the canon | coordinator reads the canon (§3) | data (a number read from the pipeline), accepted by the Lead | not code, no census row |

Commit lines: every package commit carries the `architecture:` and `judgment:` lines in the form that
`tools/architecture_gate.py` accepts. That file is the only carrier of the grammar; read it and do not copy it from here. The
judgment line here is `judgment: none -- <why>`, with the why written out (e.g. test bodies moved byte for byte; no check
judges a role). It is never bare.

**Variety walk** (`design/architecture.md` § A): `variety: none -- package test code moves between test files of the package's own tree; no project-facing code changes, so no axis of the variety map is met.`

**FR walk** (PROJECT.md, package change item 1). A: no refusal text changes. B: no text to a person. C: FR-14, the runner's
file list changes with its readers in one push. D: n/a, no identifiers. E: n/a. F: FR-28 and FR-31 (this node exists
because of FR-31; a ceiling is no fix). G: FR-31, FR-32 (the root cause, file size against the cap, gets a structural cut),
FR-37 (every path named in text is re-pointed, §6), FR-54 (siblings, §7).

**A reused function in a more consequential role.** `scenario_walk.witness_for` (`scenario_walk.py:888-924`) picks a
builder's witness from the parts' narrowed `covers`. It may err toward a WIDER witness (safe). It must never pick a NARROWER
one: the union of the parts' `covers` contains the old `covers` (spec C §4.1). Inputs that must stay on the safe side:
- a data file the walk reads at run time (`agents/qa-runner.md`, `references/slices/...`, `references/stage-joints.json`,
  `fixtures/told-ratchet.json`, `fixtures/judgment-census.json`). It stays in the `covers` of EVERY part that calls
  `SJ.audit`, `SJ.main` or `told_world`, even though no import names it;
- a path no part names, which prints "run the whole scenario layer" (the safe side);
- the deleted `tests/test_stage_joints.py` (counted as changed, `scenario_walk.py:904-905`);
- a common module (every part covers it, so all parts run);
- `tests/probe_by_code_common.py` for the five importer keep rows (`test-layers.json:3723, 3733, 3750, 3767, 3784`), which
  reach it through the shim: `split-keep --shim` adds it only to the parts and the shim (`tools/test_quarantine.py:1484-1497`),
  so NC-19 adds it to those five `covers` (§4). Without it, `--witness-for tests/probe_by_code_common.py` misses them.
When in doubt, an entry is KEPT.

`test_split.py` takes on no new role here. Its proof is the mechanical layer of spec C 2.5, used as before.

## §2 Common rules (deltas from spec C §2)

1. **One road** (P31, spec C F1): every move goes through `tools/test_split.py --map <map> --dry-run`, then `--apply`. The
   map lives at `<R>docs\tasks\specs\reports\<task_id>-pc4-19-<stream>-map.json` (precedent:
   `docs/tasks/specs/reports/t-068-td11c-N2-map.json`). No byte is moved by hand. A tool refusal stops the stream (E-1).
   The only hand commits are the prep lifts B0 and D0, which change no statement and which the tool's proof then checks.
2. **Time target**: per fork F1 (recommended: each part under **60 s on the CI canon**, `docs/TESTING.md` «Бюджет / Файлы»;
   spec C 2.4). Number of parts = ceil(CI s / 50), bounded by the file's indivisible run-list groups. Where the groups are
   fewer than that number, the report says so and E-2 applies.
3. **Groups, not row shards.** A part is a set of whole run-list entries in their old order. The runner starts a file with no
   arguments (§0), so an argv shard would need a runner and CI change, which the non-goals forbid.
4. **Registries**: the builder commits NONE of them. It hands the row block the tool prints plus a "Needed from integration"
   list (spec C R-A1). The integrator writes them in ONE closing commit pushed with the merges (R-A2), as in §4.
5. **Local runs**: only the parts, each alone, plus whatever `--witness-for` prints that is NOT in `slow_tests.json`. Every
   printed file that IS in `slow_tests.json` is judged by the batch canon (`docs/TESTING.md` «Уровень пачки»). The builder
   never runs the old file, `selftest.py`, CI or the canon.

## §3 Per file

### §3.A `test_stage_joints.py` -> 6 parts, no shim (stream A)

The old `main` (1208-1232) is 23 direct calls plus `finish`, which the tool recognises. Module-level world (built at import,
so built once PER PART after the split: E-3): `ENV = SJ.Env.real()` (:35), `REAL, _WHY = SJ.load_rows(SJ.DATA)` (:36),
`UNI = SJ.universe()` (:37). These go to `stage_joints_common.py` with `PINS`, `kind_keys`, `member`, `audit`, `mutated`,
`row_of`, `text_of`, `a_row`, `a_rows_file`, and every T1c helper used by two parts (`load_told`, `rowless_*`,
`*_problems`, `told_world`/`_WORLD` if `told_variants` uses them; the tool's `--dry-run` names any name a part uses that
was homed elsewhere).

| Part `<T>test_stage_joints_<topic>.py` | Run-list entries (old order) | Old lines | Estimate at 259.4 s (line share, unmeasured) |
|---|---|---|---|
| `k1_k8` | k1_real_tree, k2_k3_pins, k4_k5_directions, k6_legs (calls code_sites :162), k7_reach, k8_direction_c | 70-241 | ~39 s |
| `k9_k14` | k9_unreadable_shapes, k10_data_file, k11_ratchet, k12_joint_census, k13_threshold, k14_cli (6 in-process `SJ.main` + 1 `run_script` subprocess) | 242-414 | ~39 s |
| `v2_rows` | v2_reader, lookups, renderers, light_import (1 subprocess), rename, merges, exit_gate_sites | 415-664 | ~57 s |
| `told_variants` | told_variants | 880-1019 | ~32 s |
| `told_legs` | told_leg_and_rows, t1rp | 1020-1206 | ~43 s |
| `told_real` | told_real (the census wide scan: `RR.package_files`, `CT.units_of`, `RR.wide_report`, `told_world` :822-845) | 853-879 + helpers 683-851 | ~44 s |

Common: `<T>stage_joints_common.py`. Fixture owner of `told-ratchet.json` after the split: `test_stage_joints_told_real.py`
(it reads the fixture through `load_told` at :854). The integrator re-points it (§4).

Header lines for the stream A dispatch (the Lead prints them through `python -B tools/dispatch_new.py`; content below):

given: docs/tasks/specs/20261117-pc4-19-tests-near-300s-card.md §0-§2, §3.A, §5; docs/tasks/specs/td-11c-test-split.md §2, §4, §6; docs/TESTING.md; ai-packages/qa-factory/design/factory-rules.md; tools/test_split.py (docstring); the old file
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_stage_joints.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_stage_joints_k1_k8.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_stage_joints_k9_k14.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_stage_joints_v2_rows.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_stage_joints_told_variants.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_stage_joints_told_legs.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_stage_joints_told_real.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\stage_joints_common.py
C:\QAFactory\forge-repo\docs\tasks\specs\reports\<task_id>-pc4-19-a-map.json
non-goals: no behaviour change; no world reuse; no registry committed (`test-layers.json`, `slow_tests.json`, `selftest.py`, `architecture.md`, `told-ratchet.json`); no `TEST_TIMEOUTS` row; no edit of `scripts/stage_joints.py`; no cost cut of `told_world` (FV2-20 owns it); no CI workflow edit
handoff: C:\QAFactory\forge-repo\docs\tasks\specs\reports\<task_id>-pc4-19-a.md (proof verbatim, part tallies, `--witness-for` output, row block, "Needed from integration", the mutation list of E-4)
edges: card §5 E-1..E-17; spec C §6 E1-E14
DoD: `python -B C:\QAFactory\forge-repo\tools\test_split.py --map <map> --apply` PROOF: ok, then each part alone `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_stage_joints_<topic>.py`, then `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for <each owned path>`
siblings: axis 18 (ratchets: TEST_TIMEOUTS, slow_tests rows, by the integrator); axis 34 (one road: test_split.py for every split); class siblings in card §7
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261117-pc4-19-tests-near-300s-card.md

Acceptance keys (inline DoD):
1. `--dry-run`, then `--apply` print `PROOF: ok` with: (a) check-call sites before = after; (b) top-level names once each;
   (c) run list **23** entries before = 23 across the parts, old order inside each part; (d) byte identity of every moved
   segment; (e) compile; (f) one closing per part; (g) each part and common imported alone.
2. Each part run alone prints its tally `=== test_stage_joints_<topic>: X/Y ok ===`. The sum of the six Y is reported (the
   old Y is not measured locally). A red present at the base stays red in its part (E-12). Durations are reported, not judged.
3. `--witness-for` output pasted. Printed files that are in `slow_tests.json` are listed as "judged by the canon". The others
   are run.
4. The report lists the E-4 module-state mutations found (grep given there) with their part.
5. The AR change checks of §1: no new reader; the row block (keep rows inherit `layer: gate_named`, `why` + " (part of
   test_stage_joints.py split, TD-11c)", narrowed `covers` per §1 with the union containing the old `covers`); no
   `TEST_TIMEOUTS` line.
6. `test: none -- no behaviour: bodies move byte for byte (spec C §2.5) | expected from: td-11c-test-split.md §1 "Behaviour does not change", this card §3.A`

### §3.B `test_probe_by_code.py` -> 6 parts + shim (stream B; ownership: fork F2)

**B0 prep commit (same stream, before the split, as its own commit).** Lift each inline block of `main` into a top-level
zero-argument function. The body statements stay byte-identical, and `the_receipt_flow` (:2666) is the precedent:
- `mutations_flow()` = old 3254-3281 (stub, `root = project()`, invert_plain_assert … run_directory, the `if record:` guard, finally);
- `records_flow()` = old 3283-3292;
- `two_profiles_flow()` = old 3293-3299.

After B0, `main` is 14 direct calls plus `finish`, so the tool recognises it. Invariant: B0 changes no call, argument or
order. Witness (t-1251 finding 3; no base tally exists: the file is not run locally and timed out on 4 canons, so no green
canon tally is there to compare to): (i) the DIFF SHAPE of the B0 commit: the multiset of moved statement lines before =
after (the lifted bodies keep their 4-space indent, so the lines are byte-identical), and the only new lines are the 3 `def`
lines, the 3 call lines in `main` and blank lines; (ii) after the split, proof (a) (check-call sites before = after) and
proof (c) (**14** run-list entries). The canon then judges the parts' tallies.

| Part `<T>test_probe_by_code_<topic>.py` | Run-list entries (old order) | Main old lines of the bodies | Estimate at 206.8 / 300 s (line share, unmeasured) |
|---|---|---|---|
| `bindings` | k10p_pbc_told_is_printed, of4_6_profiles_owning_and_in_test_root_agree, b355_i_in_test_root_reads_the_one_reader, second_hop_name_in_two_files_is_refused, n2_k7_the_red_probe_reads_the_stand_as_the_run_does, the_author_binding_is_the_latest_block_by_the_clock | 2687-2780, 3080-3246 | ~18 / 27 s |
| `mutations` | mutations_flow (one shared `root` and stub: the chain record -> window_validates and the ordering note at :3272) | 452-1245 | ~56 / 81 s |
| `receipts` | the_receipt_flow (live_receipt_and_publish, a_rerun…, publish_orders, publish_dicts_are_pinned, hostile_instance_ids, an_unverified_restore…) | 1245-1789, 2001-2180, 2666-2685 | ~53 / 77 s |
| `records` | records_flow (the_record_and_the_answer_are_pinned, the_repeat_is_answered, the_s6_close_context, rh1_8_dispatch_asked_first; one `stub_dir`, :3283-3292) | 2286-2665, 2781-3079 | ~48 / 70 s |
| `two_profiles` | two_profiles_flow (two_profiles_over_one_root; its own `stub_dir`, :3293-3299; three `project(shared_second=True, …)` worlds with one `run` each) | 868-915 | ~4 / 5 s (line share understates: three project worlds and three probe runs in 48 lines) |
| `exit_order` | main_exit_order_is_pinned, missing_facts_and_a_refused_publish_do_not_change_the_exit, raw_bytes_through_manifest_from_tests, through_real_run_suite | 1789-2000, 2139-2285, 833-867 | ~28 / 40 s |

Six parts (the Lead's choice in the t-1251 fix round). After B0 there are 14 run-list entries. The units that cannot be cut
inside this node are `mutations_flow` and `the_receipt_flow` (each one world). `records_flow` and `two_profiles_flow` are
separate worlds: each makes its own `stub_dir` (`test_probe_by_code.py:3283-3285`, `:3293-3295`). The six `bindings`
entries and the four `exit_order` entries are separate entries too. The file timed out at 300 s on today's canons, so 206.8 s
is stale and 300 s is a lower bound; §2.2 then gives ceil(300/50) = 6 parts. Estimates at 300 s still put `mutations`,
`receipts` and `records` over 60 s; if the canon shows them over target, that is E-2. The real cost (a child process per
check) is PC4-14 (DP), which runs after this split. The helpers `two_profiles_over_one_root` calls (`project`, `run`,
`cleanup_beside`, `TEST_FILE_REL`, `TASK`) are used by other parts too, so they go to common.

Common `<T>probe_by_code_common.py` takes every name an importer uses: DISPATCH, OBLIGATION_REFS, PROVENANCE, TASK,
TEST_FILE_REL, PY, FAKE_RUN_SUITE, env_for, model_entries, seed_author_job, write_json, tree_state, cleanup_beside,
mutated_line, read_check_record, _calls, _main_in_process (the tool computes the full set from the 5 importers), plus helpers
used by two parts. The shim `<T>test_probe_by_code.py` re-exports them (`__all__`), defines no `test_*` and holds no check
(spec C 2.2).

Header lines for the stream B dispatch:

given: card §0-§2, §3.B, §5; td-11c-test-split.md §2, §4, §6; docs/TESTING.md; design/factory-rules.md; tools/test_split.py (docstring); the old file; scripts/tests/test_story_step.py (shim precedent)
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_probe_by_code.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_probe_by_code_bindings.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_probe_by_code_mutations.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_probe_by_code_receipts.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_probe_by_code_records.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_probe_by_code_two_profiles.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_probe_by_code_exit_order.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\probe_by_code_common.py
C:\QAFactory\forge-repo\docs\tasks\specs\reports\<task_id>-pc4-19-b-map.json
non-goals: no behaviour change beyond B0's lift; no importer edited (`probe_by_code_languages_common.py`, `test_probe_by_code_languages_{cli,ts_playwright}.py`, `test_probe_by_code_copy.py`, `test_probe_by_code_alternative.py`), nor `test_probe_by_code_languages_plan.py`; no in-process conversion (PC4-14); no world reuse (PC4-13); no registry committed; no `TEST_TIMEOUTS` row
handoff: C:\QAFactory\forge-repo\docs\tasks\specs\reports\<task_id>-pc4-19-b.md
edges: card §5 E-1..E-17; spec C §6 E1-E14
DoD: `python -B C:\QAFactory\forge-repo\tools\test_split.py --map <map> --apply` PROOF: ok, then each part alone, then each importer imported alone `python -B -c "import sys; sys.path.insert(0, r'C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests'); import <importer stem>"`, then `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for <each owned path>`
siblings: axis 18, axis 34; PC4-9 N7 map superseded (fork F2); PC4-14 re-pointed to the parts (fork F4)
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261117-pc4-19-tests-near-300s-card.md

Acceptance keys: as §3.A items 1-6, with (c) = **14** run-list entries after B0, across **6** parts; B0's witness is the
diff shape of B0 (i) above plus proofs (a) and (c) after the split (ii), with no same-tally key; (b) shim: re-exports every
name the 5 importers use, all resolvable, no `test_*`; each importer imported alone exits 0. `test:` line as §3.A item 6.

### §3.C `test_scenario_dry_1.py`: NOT split (fork F3). The reason

1. Its cost is the main pass: one sequential chain S0..S9 of the real driver. Each later stage starts from a snapshot made
   by THIS process. A part starting at S5 would either rebuild S0..S4 (no time saved) or read another process's snapshot,
   which E16 refuses (`dry_world.py:41, 364-376`; AR-28). The chain is sequential by design (P29: sequential checks stay
   together).
2. Its walk rows are ALREADY split. `--part exits:<group>` runs one group, and `.github/workflows/dry-story.yml:76` runs one
   CI job per group. The census and `forms_required` that share the default run are static reads, and splitting them off
   buys only seconds.
3. Its ceiling is 900 s by the owner's dry-story exception (`docs/TESTING.md` «Время», word 14.11.2026;
   `selftest.py:115-118`). So 221.6-262 s is not "near its timeout". The finding's premise for this file does not hold.

Honest risk: the main pass stops at S5 today (`selftest.py:115-117`). Through S9 its time may roughly double, and it stays
under 900. Above about 600 s on CI the remedy is the snapshot or world cost (the TD-11d class), not a split. Nothing in this
card writes this file. `TEST_TIMEOUTS` stays as it is.

### §3.D `test_story_sides.py` -> 4 parts, no shim (stream D, only if fork F5 (a))

The runner is 12 bare module-level calls plus `harness.finish("test_story_sides")` at 806-818. The tool ACCEPTS that shape
(§0: `test_split.py:485-512`) and writes parts that keep the calls at module level, so proof (g), which imports each part
alone, would run every check of the part and `finish` (`sys.exit`) at import, twice (dry-run, then apply), under the 120 s
cap; `driver_cases` alone may pass it. So the lift is MANDATORY:

**D0 prep commit (same stream, before the split, as its own commit; the B0 twin).** Wrap the 13 lines 806-818 (the 12 calls
and `harness.finish("test_story_sides")`) into `def main() -> None:` and add `if __name__ == "__main__":` / `    main()` at
the end of the file. Invariant: D0 changes no call, argument or order, and running the file as a script (`selftest.py:494`
starts it with no arguments, so `__name__ == "__main__"`) runs exactly what it ran before; only an import stops running the
checks, and the file has no importer (§6: the one other reader, `test_conductor_doors.py:679`, is prose). Witness: (i) the
DIFF SHAPE of the D0 commit: the 13 old lines reappear in the same order as the body of `main`, each with 4 leading spaces
added; the only other new lines are the `def` line, the `if __name__` line, `    main()` and blank lines; no other line of
the file changes; (ii) after the split, proof (a) (check-call sites before = after) and proof (c) (**12** run-list entries
across the 4 parts). Module-level `DATA` (:20, reads `references/side-realities.json`) goes to `story_sides_common.py` with
`side`, `refusal`, `pointed_at`, `stderr_of`, `REAL`/`ABSENT`/`SUBSTITUTED`, `copy_registry` and `absent_story` if shared.

| Part | Entries | Old lines |
|---|---|---|
| `test_story_sides_driver.py` | driver_cases | 291-593 |
| `test_story_sides_absent_side.py` | absent_side_cases (+ answer_of, pipeline_of, _today, _bare_relaunch) | 594-803 |
| `test_story_sides_registry.py` | registry_cases | 187-290 |
| `test_story_sides_readers.py` | word, reader, parks, awaiting, stage_done, note, edge, bom, transition cases | 25-186 |

The estimate is not given: the seconds sit in the driver worlds, not in lines. The first canon decides (E-2). The 600
ceiling row `"test_story_sides.py": 600` and its comment (`selftest.py:155-159`) are removed by NC-19 in the same push as the
deletion of the old file (t-1251 finding 5): a row keyed on a deleted file holds nothing (E-6), and removing it shrinks the
ratchet (AR-20). A part over 300 s at the first canon is E-2 / `defect_found`, never a new row. Owns, header lines and DoD:
as §3.A, with `<T>test_story_sides*.py`, `<T>story_sides_common.py`, `-d` map and report; the acceptance keys add D0's
witness (i) and (ii) above, with no same-tally key.

### CI timing check (all streams; the coordinator, after the batch canon; never the builder)

For each shard file of the batch canon run `<run>`:

`python -B C:\QAFactory\forge-repo\tools\ci_read.py artifact <run> package-full-shard-1/selftest-shard-1-of-2.txt --grep "test_(stage_joints_(k1_k8|k9_k14|v2_rows|told_variants|told_legs|told_real)|probe_by_code_(bindings|mutations|receipts|records|two_profiles|exit_order)|story_sides_(driver|absent_side|registry|readers))\.py"`

and the same for `package-full-shard-2/selftest-shard-2-of-2.txt`. Each part prints `PASS tests: … <s>s`. The verdict:
- each part is under the F1 target: accepted;
- over the target and under 300: E-2;
- `timeout` or `FAIL`: `defect_found` against the node.

The grep names the parts exactly (E-8), never `test_stage_joints_*` or `test_probe_by_code_*`. The output goes into the
batch's last `accepted` event labelled BATCH CANON. Then the integrator runs
`python -B ai-packages/qa-factory/scripts/selftest.py --slow-tests --from <ci-out/selftest.txt> --update` (spec C §4.1),
which replaces the provisional numbers.

## §4 Integrator closing commit (NC-19; one push with the stream merges, spec C R-A1/R-A2)

| Carrier | Change |
|---|---|
| `scripts/tests/test-layers.json` keep | `python tools/test_quarantine.py split-keep test_stage_joints.py --into <6 parts> --reason "PC4-19: under the 300 s cap"`, then `split-keep test_probe_by_code.py --into <6 parts> --shim --reason ...` (and `split-keep test_story_sides.py --into <4 parts> --reason ...` if F5, no shim). Then the narrowed `covers` from each builder's row block (§1 error direction). The commit carries the printed `keep-split:` lines |
| same, keep rows of the 5 importer files `test_probe_by_code_{alternative,copy,languages_cli,languages_plan,languages_ts_playwright}.py` (`:3723, :3733, :3750, :3767, :3784`) | `covers` += `tests/probe_by_code_common.py` (they reach it through the shim; `split-keep --shim` does not add it to them, `tools/test_quarantine.py:1484-1497`); `tests/test_probe_by_code.py` stays (§1 error direction) |
| same, `fixture_owners` | `"told-ratchet.json": "test_stage_joints_told_real.py"` |
| `scripts/slow_tests.json` | old rows out. Parts in at provisional `round(old × part check-call sites / total, 1)` (the tool prints the per-part site counts); never `null`. The shim is not listed |
| `scripts/selftest.py` | `CONTRACT_TESTS`: `"test_stage_joints.py"` -> the six parts in run-list order; docstring :35 names "the test_stage_joints_*.py parts". `TEST_TIMEOUTS`: the `"test_story_sides.py": 600` row and its comment (:155-159) removed in the same push as the deletion of the old file (if F5; a shrink, AR-20). No other `TEST_TIMEOUTS` change |
| `scripts/tests/test_conductor_doors.py:679` | the `PINNED_ELSEWHERE["awaiting.absent_side"]` value `"test_story_sides.py (t-2559 W2 B3: …)"` -> `"test_story_sides_absent_side.py (t-2559 W2 B3: …)"`, the rest of the string byte-identical (FR-37; the B3 checks live in `absent_side_cases`, `test_story_sides.py:629-803`; only the keys are read, :828, :842, :872, :878) (if F5) |
| `design/architecture.md:155, :277` | `test_stage_joints.py` -> `test_stage_joints_k1_k8.py` (the real-tree walk, K1/K6-K8). Rule: who writes design files is the Lead's call (TBW1-14 owns the file now; order by F4) |
| `scripts/tests/fixtures/told-ratchet.json:3` note | "read only by test_stage_joints.py" -> "read only by test_stage_joints_told_real.py" (FR-37; `told_variants` reads only a temp `gone_path`, `test_stage_joints.py:1007-1015`, so the fixture's one reader is `told_real`, the same as `fixture_owners`). The file is TBW1-15/TBW1-17's: merge order by F4 |
| Commit lines | `architecture:` / `judgment:` per `tools/architecture_gate.py`, naming AR-13, AR-14, AR-20, AR-22 |

DoD of NC-19: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <the carriers above>` plus
`python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`. The canon runs on the pushed head.

## §5 Edges (each with the invariant it protects)

| # | Edge | Behaviour | Invariant |
|---|---|---|---|
| E-1 | the tool refuses a map or a runner (probe_by_code before B0; a name homed wrong) | fix the MAP from the refusal text and re-run. A runner refusal that no map key fixes: stop, paste the refusal, return it as a question. Never hand-move code. A module-level runner is not refused (§0), which is why D0 is a mandatory prep step, not a fallback | one road (P31): every split byte is the tool's and is proved |
| E-2 | a part over target and under 300 s at the first canon | not split again in this node; the report line names it with its seconds; the Lead opens the follow-up (TD-11d / PC4-14 class). No `TEST_TIMEOUTS` row unless it is over 300 s, and then only with a `defect_found` | a ceiling never makes slowness acceptable (FR-31) |
| E-3 | a module-level world built at import (stage_joints `ENV`/`REAL`/`UNI`; story_sides `DATA`) | goes to common and is now built once per part. The report names it; its cost is read from the per-part seconds at the canon | no scenario sees another value; no world is added silently |
| E-4 | module or global state that one entry mutates and a later entry reads, across a part border | the builder greps each old file for `^\s*(SJ\|RR\|CT\|harness\|contract)\.[A-Za-z_]+ = \|setattr\(\|use_project\(\|os\.environ\|chdir\|\.clear\(\)` and lists each hit with its restore. Known, restored: stage_joints `SJ.DATA` swap (:458-463), renderer (:1087), `SJ._IDS_CACHE.clear()` (a cache, :1111); probe_by_code `PROBE_RUN_SUITE`/`PROBE_STUB_LOG` writes (:2116, :2545-2546, :2885, :2901, :3033), each popped or restored in its own `finally` (:2124-2126, :2573-2574, :2889, :2905, :3039). Known, NOT restored, verdict given here: probe_by_code `use_project(root)` (:2671 in `the_receipt_flow`; also :1472, :1486, :1671, :1853, :2078, :2112, :2209, :2278, :2601) sets `os.environ["CLAUDE_PROJECT_DIR"]` and clears the hooklib cache (`harness.py:311-318`). The leaked value points at a root `cleanup` already removed; before the split later entries ran with that dead root, after it they run with the process env. Children get the env explicitly through `env_for` (:325-329). Verdict: the leak alone triggers nothing. The builder lists each entry in a part later in old order than a `use_project` site that calls hooklib (or reads `CLAUDE_PROJECT_DIR`) IN-PROCESS without its own `use_project` first; only such an entry triggers the rule. Any other mutation with no restore and a reader in another part: the same rule. The rule: mutator and reader go into one part, or the stream stops (E-1) | no check's outcome depends on state another entry left behind; a dead root left by a removed project is no state a check may read, and an entry that does read it stays in one process with its mutator (P29) |
| E-5 | order-dependent entries sharing one world (probe_by_code `mutations_flow`, `the_receipt_flow`) | one part each, order kept | a dependent chain never crosses a process border |
| E-6 | TEMPORAL: parts on disk without keep rows (`unlisted:`); `CONTRACT_TESTS` naming a part not on disk ("contracts: … exists" FAIL, `selftest.py:576-578`); `fixture_owners` naming the deleted file (`gate_named_files` drops a missing owner, `:734-736`); `TEST_TIMEOUTS` and `PINNED_ELSEWHERE` naming the deleted `test_story_sides.py` | before the push the old world holds (old file listed, owner valid, the 600 row keyed on an existing file). The closing commit (which removes the 600 row and re-points `:679`) and the merges land in ONE push (R-A2), after which the new world holds. Builders run parts directly, which the listing does not affect | no test file on `main` unlisted; no carrier names a missing file |
| E-7 | importers of `test_probe_by_code` (5 files) | not edited. The shim re-exports; proof (g) plus each importer imported alone. Their keep rows gain `covers` `tests/probe_by_code_common.py` in NC-19 (a data row, not an edit of the file) | a kept importer is not widened into owns; a quarantined file is never edited; a common-module edit still reaches the importers' witness |
| E-8 | foreign kept files with the parts' prefix: stream A `test_stage_joints_12586.py`; stream B `test_probe_by_code_alternative.py`, `test_probe_by_code_copy.py`, `test_probe_by_code_languages_cli.py`, `test_probe_by_code_languages_plan.py`, `test_probe_by_code_languages_ts_playwright.py`; stream D none (§0 Glob) | no topic `12586`, `alternative`, `copy` or `languages_*`. Every grep or list of parts names them exactly. K5 checks only the named parts | the timing check and K5 never count a foreign file as a part, nor drop it |
| E-9 | `--witness-for` on a test-file path prints "no scenario or keep row covers …: run the whole scenario layer" plus the scenario files | the printed scenario files that are in `slow_tests.json` are listed as "judged by the canon" and not run; the rest are run; each part runs alone in any case | the builder's witness is never narrower than the parts; SLOW_TESTS never run locally |
| E-10 | `covers` narrowing | the union contains the old `covers`. An entry is dropped only when the part provably never reaches it (§1); when unsure, it is kept | `--witness-for` may err wider, never narrower |
| E-11 | a top-level function no run list reaches | moves with its section and is listed (spec C E11). stage_joints `code_sites` is reached through `k6_legs` (:162) | the split never starts or stops running a check |
| E-12 | a red at the base (probe_by_code was 755/762 on older canons) | stays red in its part; not repaired here | a split never hides or repairs a red |
| E-13 | another node lands on one of these files between draft and `--apply` (TBW1-15/17 pins, RD1-34 K4, FV2-20/23/24) | re-run `--draft`/`--dry-run` on the fresh `main`. A new top-level name gets a map row (the tool refuses a missing one) | no name lost; a name another node adds gets a home |
| E-14 | the shim with no `test_*` | `ran_nothing` stays silent (spec C §1 AR-23 row); shim keep row `layer: data_join`, `why: "split shim: …"` via `split-keep --shim` | a shim is never a named proof (spec C E4) |
| E-15 | dry_1 | untouched: `TEST_TIMEOUTS` 900, `dry-story.yml`, the `--part` CLI unchanged | the owner's dry-story exception is not reopened by a split node |
| E-16 | `selftest --contracts` now runs six files | each under the default 300; together they run the whole walk as before | `--contracts` still runs every stage-joints check |
| E-17 | conflicting pair: "bodies byte-identical" vs "every part under the target" | byte identity wins; the overflow is E-2 | behaviour is never bent to meet a time target |

## §6 Readers of every touched file (designer rule 7)

The draft's first pass had no `owns_readers.py` block and answered by hand grep (below, kept as evidence). The Lead attached
the block (base origin/main a467d124, at the end of this card); each of its lines is answered in the second table, in the
forms of `.claude/agents/critic.md` rule 24, Q13 (d), followed by the KNOWN MISSES lines.

Hand greps (Grep tool, case-sensitive file names) with their hit counts:

1. `test_stage_joints|test_scenario_dry_1|test_probe_by_code\.py` over `ai-packages/qa-factory` (the file itself
   excluded): 40 lines, used below.
2. Same over `tools/`: 0. Positive control: `test_story_step|test_null_outcomes` over `tools/` finds 1 file.
3. Same over `.github/`: 3 (dry-story.yml, dry_1 only).
4. Same over `docs/SIBLING_MAP.md`: 0. Positive control: `test_controller_state|test_no_move_seam` finds 2.
5. `…|CONTRACT_TESTS` over `.githooks/` and `.claude/agents/`: 0 each. Positive controls: `python` in `.githooks` 16;
   `witness-for` in `.claude/agents` 3.
6. Importer regex over `scripts/`: 7 hits.
7. Batch rows over `plans/piles` (Grep `TBW1-17|RD1-34|FV2-20|FV2-23|FV2-24`, `PC4-9|PC4-19`).

| Touched file | Reader | Verdict |
|---|---|---|
| `test_stage_joints.py` (deleted) | `selftest.py:568` `CONTRACT_TESTS`, :574 `cmd_contracts`, :727 `gate_named_files`; :35 docstring | changes in NC-19 |
| | `test-layers.json:5410` keep row; `:34` fixture_owners | changes in NC-19 (split-keep; owner row) |
| | `slow_tests.json:132` | changes in NC-19 |
| | `design/architecture.md:155` (AR-10 detector), `:277` (AR-22 detector), prose carriers of `gate_named_files` | changes in NC-19 (Lead's order, F4) |
| | `fixtures/told-ratchet.json:3` note | changes in NC-19 (-> told_real only) |
| | `CHANGELOG.md:668,670` | unchanged (history) |
| | `references/stage-joints.json:88,594`; the moved `:346` | unchanged (they name `test_stage_joints_12586.py`) |
| | batch rows TBW1-15, RD1-34, FV2-20, FV2-23, FV2-24; `told-before-work/batch-1-finish.md:10` ("K12 pin test_stage_joints.py:927-932") | Lead re-points to the part per the function->part map of §3.A (F4) |
| `test_probe_by_code.py` (shim) | importers `probe_by_code_languages_common.py:23-24`, `test_probe_by_code_languages_ts_playwright.py:17`, `_cli.py:23`, `test_probe_by_code_copy.py:30`, `test_probe_by_code_alternative.py:25` | unchanged (shim) |
| | `test-layers.json:3690` own row; `covers` naming `tests/test_probe_by_code.py` at :3723, :3733, :3750, :3767, :3784 | own row changes in NC-19 (`--shim`); the five `covers` change in NC-19: += `tests/probe_by_code_common.py` (§4 row), `tests/test_probe_by_code.py` kept |
| | `slow_tests.json:83` | changes in NC-19 |
| | comments `test_probe_by_code_languages_ts_playwright.py:331`, `_cli.py:631`, `test_probe_by_code_copy.py:9` | unchanged (kept importers are not edited; the name still resolves as the shim). Listed in "Needed from integration" as FR-37 text that names where a check lived |
| | batch rows PC4-9 (N7), PC4-13, PC4-14 (`_main_in_process` sample `test_probe_by_code.py:1789`); `td-11c-test-split.md` §3.1 row, §7 N7; `td-11d-world-per-file.md` (`:1789` reference) | Lead marks N7 superseded (F2) and re-points PC4-14 to the parts and common |
| `test_story_sides.py` (deleted, if F5) | `selftest.py:155-159` `TEST_TIMEOUTS` row and comment | changes in NC-19 (row removed with the deletion) |
| | `test_conductor_doors.py:679` `PINNED_ELSEWHERE` value | changes in NC-19 (-> `test_story_sides_absent_side.py`) |
| | `slow_tests.json:151`, `test-layers.json` own keep row | changes in NC-19 (split-keep, no shim) |
| new parts, `stage_joints_common.py`, `probe_by_code_common.py`, `story_sides_common.py` | `selftest` listing (keep rows), `shard_files` (slow_tests weights), `scenario_walk.witness_for` (covers), the shim | arrive in NC-19 |
| `test_scenario_dry_1.py` | `dry_exits.py:2666`, `dry-story.yml:5,76,100`, `known_red/{s0,gates}.json` `_about`, `selftest.py:118` | unchanged (not touched) |

**Answers to the `owns_readers.py` block, one per line** (block quoted at the card's end):

| Block line | Answer |
|---|---|
| `names: test_selftest_slow_tests.py (test, slow) names CONTRACT_TESTS` | unchanged: it patches `CONTRACT_TESTS` with its own tuple (`patch.object(S, "CONTRACT_TESTS", ("test_c1.py",))`, :467), so the real list's content does not reach it; slow -> judged by the batch canon |
| `names: test-layers.json (data) names CONTRACT_TESTS` | the three `why` strings (:2035 gate-registry walk, :3404 null-outcome walk, :5412 stage-joints walk): :5412 changes in NC-19 (`split-keep` copies it to the six parts with the "(part of …)" suffix and drops the old row); :2035 and :3404 unchanged (other walks) |
| `outside: test_conductor_doors.py (test, slow) names test_story_sides.py` | changes in NC-19: `:679` value re-pointed to `test_story_sides_absent_side.py` (§4 row; FR-37 prose, only the keys are read at :828, :842, :872, :878); slow -> judged by the batch canon |
| `outside: test_probe_by_code_copy.py (test, slow) names test_probe_by_code.py` | unchanged: imports through the shim (E-7); comment :9 still resolves to the shim; its keep row's `covers` change in NC-19 (§4); slow -> judged by the batch canon |
| `outside: test_probe_by_code_languages_cli.py (test, slow) names test_probe_by_code.py` | unchanged: imports through the shim (E-7); comment :631 resolves to the shim; keep-row `covers` change in NC-19 (§4); slow -> judged by the batch canon |
| `outside: test_probe_by_code_languages_ts_playwright.py (test) names test_probe_by_code.py` | unchanged: imports through the shim (E-7), imported alone in stream B's DoD; comment :331 resolves to the shim; keep-row `covers` change in NC-19 (§4) |
| `outside: test_probe_by_code_alternative.py (test, slow) names test_probe_by_code.py` | unchanged: imports through the shim (E-7); keep-row `covers` change in NC-19 (§4); slow -> judged by the batch canon |
| `outside: test_probe_debt.py (test, slow) names test_probe_by_code.py` | unchanged: `:1461` is a docstring ("A project of test_probe_by_code's shape …") naming a project shape, and the name still resolves to the shim; slow -> judged by the batch canon |
| `outside: selftest.py (code) names test_stage_joints.py, test_story_sides.py, test_scenario_dry_1.py, CONTRACT_TESTS` | changes in NC-19: `CONTRACT_TESTS` :568 and docstring :35 (stage_joints); `TEST_TIMEOUTS` story_sides row and comment :155-159 removed (F5); `test_scenario_dry_1.py` :118 unchanged (F3, E-15) |
| `outside: .github/workflows/dry-story.yml (code) names test_scenario_dry_1.py` | unchanged: dry_1 not touched (F3, E-15) |
| `outside: probe_by_code.py (code) names test_probe_by_code.py` | unchanged: `:8390` is a prose comment ("caught by test_probe_by_code the same minute"); the shim keeps the name resolvable and the comment names the test family, not a check site. Not a builder's file (non-goal: no edit of package code) |
| `outside: dry_exits.py (code) names test_scenario_dry_1.py` | unchanged: dry_1 not touched (F3) |
| `outside: probe_by_code_languages_common.py (code) names test_probe_by_code.py` | unchanged: imports through the shim (`:23-24`, E-7); the names it imports are re-exported by the shim (stream B key (b)) |
| `data: slow_tests.json names the four files` | changes in NC-19: stage_joints, probe_by_code, story_sides rows out, parts in at provisional numbers (§4); dry_1 row unchanged |
| `data: fixtures/told-ratchet.json names test_stage_joints.py` | changes in NC-19 (the integrator's closing commit, not a stream: the streams' non-goals forbid it; §4 row -> `test_stage_joints_told_real.py`; merge order against TBW1-15/17 by F4). Until that push the old name stays true because the old file still exists (E-6) |
| `data: test-layers.json names the four files` | changes in NC-19: `split-keep` for stage_joints, probe_by_code (`--shim`) and story_sides; `fixture_owners`; the five importer `covers`; dry_1 row unchanged |
| known miss of the block header: `tools/owns_readers.py` docstring | unchanged: a forge tool's docstring, not a reader of the touched files |

KNOWN MISSES (critic.md rule 24, Q13 (d)), one line each:
- miss 1 (transitive): not quoted here: `scenario_walk.py --witness-for <path>` needs a shell this role lacks. Each stream's DoD
  runs it on every owned path and pastes it (§3.A key 3), and NC-19's DoD runs it over the carriers; the transitive list is
  judged there. Question to the Lead (§8 Q-r) whether to quote it here before dispatch.
- miss 2 (built path/name): the runner's listing builds the file list from the tests directory, which is why E-6's `unlisted:`
  world exists; K5 builds `test_<old stem>_<topic>.py` (E-8 names the foreign files it must not count); `shard_files` reads
  `slow_tests.json` weights (§4). The CI timing grep names every part literally. No reader builds the three old names.
- miss 3 (pinned VALUE): values this card changes: `CONTRACT_TESTS` length 3 -> 8; Grep `len\([^)]*CONTRACT_TESTS|CONTRACT_TESTS\[`
  over `scripts/`: 0 hits; positive control in the same call shape, `len\([^)]*REAL\[|len\([^)]*CONTRACT_TESTS`: 7 hits in 3
  files. The K1 pin "285 rows" (`test_stage_joints.py:76-77`) moves byte for byte into `k1_k8`, its value unchanged (no row of
  `stage-joints.json` changes). `TEST_TIMEOUTS` loses the story_sides row: the one value pin over `TEST_TIMEOUTS`,
  `test_current_audit_contract.py:79-87`, names seven other files and pins 600 for `test_infra_failure.py` and 300 for
  `test_audit_rules.py`, so it is unaffected. `PINNED_ELSEWHERE` values are not read (keys only).
- miss 4 (short stem): covered by the file-name search (the stems `test_stage_joints`, `test_probe_by_code`,
  `test_story_sides` are long; `stage_joints` alone also matches `scripts/stage_joints.py`, which is not touched).
- miss 5 (out of scope prose): searched by hand: batch rows over `plans/piles` (hand grep 7 above; `test_story_sides` over
  `plans/piles/*/batch-*.md`: PC1-1, PC3-1 only, §0) and specs `td-11c-test-split.md`, `td-11d-world-per-file.md`; answered
  in the first table (Lead re-points open rows by F4; a closed row is history).
- miss 6 (stale base): base a467d124 is origin/main: no. t-1251 read origin/main 10756f4f (the one commit between is
  spec-only); at this resubmission local `main` shows 44585bce (a17aa89f, this card; 44585bce, a piles commit opening RD1-19b)
  -- estimate, not verified: this role has no shell to compare with origin.
- miss 7 (common-word stem): nothing owed: it over-counts, never hides.

## §7 Siblings (rule 9: sweep the artifact first, then the map)

Sweep of the carrier that names the class, `slow_tests.json`. Grep for values >= 150 s finds 9 rows, each with a verdict:
- probe_by_code 206.8: §3.B.
- dry_1 221.6: §3.C, not applicable (sequential chain, 900 exception).
- stage_joints 259.4: §3.A.
- story_run_refusals 205.6, story_run_s0 252.4, story_run_s6 279.0, words_doors 188.4: under 600 ceilings, nodes PC4-10
  N11/N12/N13/N15 (already mapped).
- story_run_stand_identity 205.7: **no ceiling, default 300**. The same failure class as the brief's files; node PC4-10 N14
  (F5).
- story_sides 354.7: over 300 under a 600 ceiling, no node. §3.D (F5).

Map: axis 18 (ratchets: `TEST_TIMEOUTS`, `slow_tests`): covered by §4 (the story_sides 600 row leaves with its file). Axis 34
(one road): `test_split.py` for every stream. Axis 31 (owner carriers): `docs/TESTING.md` holds the 60 s rule; it is
unchanged unless F1 (b), which needs the owner's word.

Tool analog (t-1251 finding 1): `test_split.py` accepts a module-level-call runner while its proof (g) note (:1812-1815)
claims a part's runner is not run. That is `tools/` code outside this card's reach; the critic proposed a node, and the Lead
opens it (non-goal of the t-1256 fix round).

## §8 Forks (each with options, recommendation, and what is done meanwhile)

| # | Fork | Options | Recommendation |
|---|---|---|---|
| F1 | part time target | (a) under 60 s on the CI canon (`docs/TESTING.md` «Бюджет / Файлы», owner 11.11.2026; spec C 2.4, F4): stage_joints 6 parts, probe_by_code 5 (bounded by its groups; corrected in the t-1251 fix round: 6, the Lead's choice); (b) the brief's "under about 150 s": 2 parts each | **(a)**. (b) contradicts the owner's written rule, and changing it needs the owner's word plus a TESTING.md edit (axis 31). (a) costs more files and a per-part import world (E-3). Meanwhile (a) |
| F2 | `test_probe_by_code.py` belongs to PC4-9 (N7) with a stale 3-part map (105.8 s / 3160 lines; now 206.8-300 s / 3308 lines) | (a) stream B of this card replaces N7: the Lead moves N7 out of PC4-9's row (PC4-9 keeps N8, N10) and marks spec C §3.1/§7 N7 superseded; (b) PC4-9 keeps N7 and takes §3.B as its amended map | **(a)**: four canons were red today on this file, PC4-9 is unstarted, and both options use the same road (the tool). (b) leaves the timeout until PC4-9 is taken |
| F3 | `test_scenario_dry_1.py` | (a) not split, for the reasons of §3.C; the Lead corrects the finding's premise (900 ceiling); (b) split census plus `forms_required` off | **(a)**: (b) saves seconds and adds a file; the chain cannot be split without breaking E16 |
| F4 | order against nodes that edit `test_stage_joints.py` / `test_probe_by_code.py` (TBW1-15 pins; TBW1-17, which the dispatch says owns lines but whose row lists no such file, only `told-ratchet.json`; RD1-34 K4; FV2-20/23/24; PC4-14) | (a) split now. A node in flight merges first and the split re-runs the tool on the fresh `main` (E-13). Nodes not started get their owns re-pointed to the part holding their function (Lead edits those rows); (b) wait until all of them land (TBW1-15 waits on "все узлы") | **(a)**: the tool makes a re-split cheap, and (b) keeps the canon red for days |
| F5 | same-class siblings outside the brief | (a) take `test_story_sides.py` as stream D (owns widen, §3.D), and the Lead starts PC4-10 N14 (stand_identity, default 300) now; (b) a finding or node in another pile for story_sides, N14 left in its queue | **(a)**: within this node's reach by its own criterion (a file over ~200 s on CI). Covering it costs one more builder |
| Q | the `owns_readers.py` block | the Lead runs `python -B tools/owns_readers.py --paths <owns of §3> --names CONTRACT_TESTS` and attaches it; §6 answers by hand grep until then | answered: the block is attached (Lead decisions) and §6 answers every line (t-1251 fix round) |
| Q-r | miss 1 of the block (transitive readers) | (a) the Lead quotes `scenario_walk.py --witness-for <each touched package path>` into §6 before the stream dispatches; (b) leave it to each stream's and NC-19's DoD run, which prints and pastes it | **(b)**: the DoD runs already carry it and the plan critic accepted the rest of §6; (a) costs one run and closes the miss in the plan itself. Meanwhile (b) |

## §9 Small choices closed here (no design weight)

- Groups, not argv shards (§0: the runner passes no arguments).
- B0 lift of `main`'s inline blocks into zero-argument functions (precedent `the_receipt_flow`), so that the one tool can
  recognise the runner.
- D0 lift of story_sides' module-level runner into `def main()` plus an `if __name__` guard (the B0 twin), so that proof (g)
  imports a part without running it (t-1251 finding 1).
- Part topics come from the file's own key labels (K1-K8, K9-K14, v2/rows, told) and its scenario names. Not `12586` (E-8).
- Fixture owner of `told-ratchet.json` = the `told_real` part.
- All six parts go into `CONTRACT_TESTS`, so `--contracts` runs the whole walk as before.
- Map and report paths follow the N2 precedent.
- Estimates by line-span share, marked unmeasured (no per-group figure exists, §0).
- The CI timing grep also names the four story_sides parts (sweep of the same artifact: stream D's parts are judged by the same
  check).

## §10 Reading trail

Read: the finding; `docs/TESTING.md:36-285`; `.claude/agents/designer.md` (dispatch); `td-11c-test-split.md:1-250`;
`plans/piles/package-ci/batch-4-dieta-testov-td-11-td-15.md:1-52`; `told-before-work/batch-1-finish.md:1-60`;
`live-run-fvf/findings/20261114-told-world-skaniruet-paket-dvazhdy.md`; `selftest.py:100-180, 560-590, 715-745`;
`test_stage_joints.py:1-100, 660-860, 1200-1237`; `test_probe_by_code.py:1-40, 2660-2690, 3240-3308`;
`test_scenario_dry_1.py` whole; `test_story_sides.py:1-24, 795-818`; `scenario_walk.py:834-928`;
`tools/test_split.py:1-106, 296-345, 641-715`; `design/architecture.md:33-74, 173-197, 200-279`;
`docs/SIBLING_MAP.md:473-502`; `reports/t-068-td11c-N2.md:1-60`.
Grepped: `selftest.py` (300/timeout, CONTRACT_TESTS, the 3 names); `test-layers.json` (keep rows of the 3 families);
`slow_tests.json` (values >= 150); `ci-out/**/*.txt` (the 3 names); function lists of the 4 test files; `harness.py`
(clock: none, control found); importers; carriers over the package, `tools/`, `.github/`, `.githooks/`, `.claude/agents/`,
`docs/SIBLING_MAP.md` (counts and controls in §6); `plans/piles` (node ids); `tools/test_quarantine.py` (split-keep/K5);
`docs/RUNBOOK.md`, `tools/ci_read.py` (artifact usage).
Not done: no CI artifact was fetched (`ci_read.py` needs a shell this role lacks); the brief's run ids are quoted, not read.
Not opened: `.gitlab-ci.yml` (absent: the path does not exist); `install_smoke.py` (covered by the package grep, 0 hits).

Fix round t-1256 (by verdict t-1251): Read `docs/tasks/specs/reviews/t-1251-pc4-19-plan.md` whole; `test_story_sides.py:795-819`;
`selftest.py:150-161`; `test_probe_by_code.py:868-915, 3245-3308`; `test-layers.json:7165-7184`;
`test_current_audit_contract.py:68-87`; `.claude/agents/critic.md:290-317`. Grepped: `test_probe_by_code.py` (`^def`,
`use_project(`, `PROBE_RUN_SUITE|PROBE_STUB_LOG`: the sites in E-4); `test_story_sides.py` (`absent_side|^def`: the B3
checks at 629-803); `test_stage_joints.py` (`load_told(|told-ratchet|gone_path`; `\b285\b`); the four reader files for the
three names (4 hits: :467, :679, :1461, :8390); `test_conductor_doors.py` `PINNED_ELSEWHERE` (keys at :828, :842, :872,
:878); `test-layers.json` (`CONTRACT_TESTS`: 3 why strings; the probe_by_code keep rows: :3690 own, :3723-:3784 covers;
`test_conductor_doors.py` row :672, keep, not quarantined); `TEST_TIMEOUTS` over `scripts/` (3 files); the `CONTRACT_TESTS`
value pins with a positive control (§6 miss 3). Glob `test_probe_by_code*.py` (6) and `test_story_sides*.py` (1) in `<T>`.
Taken from the t-1251 trail without re-reading: `tools/test_split.py:82, 273-277, 485-512, 1326-1336, 1804, 1812-1815`;
`harness.py:225-229, 311-318`; `tools/test_quarantine.py:1484-1497`.

## Lead decisions (17.11.2026, Lead session 501cb4e0, «решила сама»)

- F1 (a): under 60 s per part on the CI canon (the owner's TESTING.md rule stands); A 6 parts, B 6 parts (critic t-1251 fix 2: records split into records and two_profiles).
- F2 (a): stream B replaces PC4-9 N7; the Lead moves N7 out of PC4-9's row (PC4-9 keeps N8, N10) and marks spec C §3.1/§7 N7 superseded by this card.
- F3 (a): `test_scenario_dry_1.py` is not split; the finding's premise is corrected (its ceiling is 900 s).
- F4 (a): split now; a node in flight that edits a split file merges first and the split re-runs the tool on fresh `main` (E-13); unstarted nodes get their owns re-pointed by the Lead.
- F5 (a): stream D takes `test_story_sides.py`; PC4-10 N14 (stand_identity) starts as its own builder when a slot frees.
- Q: the `owns_readers.py` block is below (base origin/main a467d124). Two readers the card's §6 must answer by name: `scripts/probe_by_code.py` (code, names `test_probe_by_code.py`) and `fixtures/told-ratchet.json` (data, names `test_stage_joints.py`; the card's non-goals forbid editing it, so §6 says how its name stays true after the split, or the Lead widens owns).

```
readers: 14 outside owns, 20 lines below -- base origin/main a467d124 (literal mention; known misses: tools/owns_readers.py docstring)
- names: ai-packages/qa-factory/scripts/tests/test_selftest_slow_tests.py (test, slow) names CONTRACT_TESTS
- names: ai-packages/qa-factory/scripts/tests/test-layers.json (data) names CONTRACT_TESTS
- outside: ai-packages/qa-factory/scripts/tests/test_conductor_doors.py (test, slow) names ai-packages/qa-factory/scripts/tests/test_story_sides.py
- outside: ai-packages/qa-factory/scripts/tests/test_probe_by_code_copy.py (test, slow) names ai-packages/qa-factory/scripts/tests/test_probe_by_code.py
- outside: ai-packages/qa-factory/scripts/tests/test_probe_by_code_languages_cli.py (test, slow) names ai-packages/qa-factory/scripts/tests/test_probe_by_code.py
- outside: ai-packages/qa-factory/scripts/tests/test_probe_by_code_languages_ts_playwright.py (test) names ai-packages/qa-factory/scripts/tests/test_probe_by_code.py
- outside: ai-packages/qa-factory/scripts/tests/test_probe_by_code_alternative.py (test, slow) names ai-packages/qa-factory/scripts/tests/test_probe_by_code.py
- outside: ai-packages/qa-factory/scripts/tests/test_probe_debt.py (test, slow) names ai-packages/qa-factory/scripts/tests/test_probe_by_code.py
- outside: ai-packages/qa-factory/scripts/selftest.py (code) names ai-packages/qa-factory/scripts/tests/test_stage_joints.py, ai-packages/qa-factory/scripts/tests/test_story_sides.py, ai-packages/qa-factory/scripts/tests/test_scenario_dry_1.py, CONTRACT_TESTS
- outside: .github/workflows/dry-story.yml (code) names ai-packages/qa-factory/scripts/tests/test_scenario_dry_1.py
- outside: ai-packages/qa-factory/scripts/probe_by_code.py (code) names ai-packages/qa-factory/scripts/tests/test_probe_by_code.py
- outside: ai-packages/qa-factory/scripts/tests/dry_exits.py (code) names ai-packages/qa-factory/scripts/tests/test_scenario_dry_1.py
- outside: ai-packages/qa-factory/scripts/tests/probe_by_code_languages_common.py (code) names ai-packages/qa-factory/scripts/tests/test_probe_by_code.py
- data: ai-packages/qa-factory/scripts/slow_tests.json names ai-packages/qa-factory/scripts/tests/test_stage_joints.py, ai-packages/qa-factory/scripts/tests/test_probe_by_code.py, ai-packages/qa-factory/scripts/tests/test_story_sides.py, ai-packages/qa-factory/scripts/tests/test_scenario_dry_1.py
- data: ai-packages/qa-factory/scripts/tests/fixtures/told-ratchet.json names ai-packages/qa-factory/scripts/tests/test_stage_joints.py
- data: ai-packages/qa-factory/scripts/tests/test-layers.json names ai-packages/qa-factory/scripts/tests/test_stage_joints.py, ai-packages/qa-factory/scripts/tests/test_probe_by_code.py, ai-packages/qa-factory/scripts/tests/test_story_sides.py, ai-packages/qa-factory/scripts/tests/test_scenario_dry_1.py
```

## Fix round t-1251 (resubmission t-1256, designer, 17.11.2026)

Each change by the verdict `docs/tasks/specs/reviews/t-1251-pc4-19-plan.md`, with the section it landed in. No fork was decided
here; the Lead decisions above are unchanged (their F1 line still reads "B 5 parts"; the dispatch of t-1256 carries the
Lead's choice of 6, and the Lead's own line is the Lead's to edit).

| # | Finding | Change | Sections |
|---|---|---|---|
| 1 | the premise "if `--dry-run` refuses the module-level runner" is false | a mandatory D0 prep commit: `def main()` + `if __name__ == "__main__"` guard around `test_story_sides.py:806-818`, with B0's invariant and a diff-shape key; the "if refused" wording dropped; E-1 no longer lists story_sides; the tool analog left to the Lead | §0 (test_split row), §2.1, §3.D, §5 E-1, §7, §9 |
| 2 | "Five groups, against ceil(300/50) = 6" misstates the bound | Lead's choice: 6 parts; `records` split into `records` (records_flow) and `two_profiles` (two_profiles_flow, 868-915); the true bound written (14 entries, two indivisible flows, 300 s a lower bound); owns, acceptance keys and CI grep updated; F1's options text annotated | §3.B (title, table, prose, owns, keys), CI timing check, §4 split-keep row, §8 F1 |
| 3 | "the same tally as the base" has no base value | B0 witness = (i) diff shape of the B0 commit + (ii) proofs (a) and (c) after the split; the same-tally key dropped | §3.B B0 paragraph, §3.B acceptance keys |
| 4 | the importers' `covers` widening missing from the NC-19 table | a §4 row: the 5 importer keep rows (`:3723, :3733, :3750, :3767, :3784`) `covers` += `tests/probe_by_code_common.py`; mirrored in §1 (reused function, safe-side inputs), E-7 and §6 | §4, §1, §5 E-7, §6 |
| 5 | the kept `"test_story_sides.py": 600` row contradicts E-6 | NC-19 removes the row and its comment (`selftest.py:155-159`) in the same push as the deletion; a part over 300 is E-2 / `defect_found` | §3.D, §4 selftest row, §1 AR-20 and AR-22 rows, §5 E-6, §7 axis 18 |
| 6 | E-4's known probe_by_code hit has no verdict | E-4 states the verdict: the leaked `CLAUDE_PROJECT_DIR` points at a removed root; a later entry must not depend on it; the builder lists each later-part entry calling hooklib in-process without its own `use_project`, and only such an entry triggers merge-or-stop; the restored `PROBE_*` writes listed; the invariant reworded so the behaviour no longer contradicts it | §5 E-4 |
| 7 | owns_readers block lines unanswered, no KNOWN MISSES lines | one answer per block line (the Lead's two named readers included: `probe_by_code.py:8390` unchanged, `told-ratchet.json` changes in NC-19) plus miss 1-7 lines; `test_conductor_doors.py:679` re-pointed in NC-19 (new §4 row); story_sides readers added to the first table | §6, §4, §1 AR-22 row, §5 E-6 |
| minor a | told-ratchet note names `told_variants` too | the note names `told_real` only (`told_variants` reads a temp `gone_path`, :1007-1015) | §4 told-ratchet row, §6 |
| minor b | E-8 names one foreign prefix file | E-8 names the five stream-B foreign files and states stream D has none (Glob) | §5 E-8, §0 prefix row |
| sweep | same-artifact neighbours of finding 2 | the CI timing grep also names the four story_sides parts | CI timing check, §9 |

New question returned, not decided: §8 Q-r (miss 1, the transitive `--witness-for` quote this role cannot run).
Not applied (outside the findings, the Lead's): the critic's F4 suggestion to confirm `origin/wip/tbw-t1b` is dead and to
write the per-node re-point list now.

- Q-r (b) (Lead, 17.11.2026, after the fix round): miss 1 is left to each stream's DoD run (`--witness-for` of its owns) and to NC-19's; no quote in §6 before dispatch.
- B0b (Lead, 17.11.2026, builder question t-1259): a file whose kept preamble has `sys.path.insert(0, ...parents[1])` fails proof (g) (the parts are staged in a temp dir). Each stream adds a prep commit B0b replacing that line with `sys.path.insert(0, str(SCRIPTS))` after the harness import (the N2 precedent form, `test_story_step_config.py:17`); its key is the diff of that one line. Streams A and D check their preamble for the same line first. The tool gap is node PC4-20.
