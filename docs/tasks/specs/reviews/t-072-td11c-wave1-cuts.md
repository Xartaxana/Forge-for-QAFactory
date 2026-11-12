# t-072 — critic gate, TD-11 spec C wave 1: the six test-file cuts (one pass on the topic)

## Verdict

| Node | Verdict | Why, in one line |
|---|---|---|
| N1 infra_failure | **accept** | the cut is faithful by my own AST reading. Optional on regeneration: `taken` moves to `_retries` |
| N4 loop_b | **accept** | faithful. No finding of its own |
| N6 controller_rework (+shim) | **accept** | faithful. The shim re-exports all 10 names the 5 importers use |
| N5 handoff_values | **accept** | faithful. Its rule-2.3 calls are right |
| N3 freshness | **accept, one fix on regeneration (non-blocking)** | faithful. `k4b` belongs in `_k1_k5` (the part name otherwise lies) |
| N2 no_move_seam (evidence only) | **regenerate after t-071** | I reproduced F1 and F2. They are not acceptable as they stand |

No blocker in the five cuts. The blocking items belong to the integrator's closing commit (NC). Four carriers turn the canon RED if they are missed (Q5, items 1-4). Overall: **fit_with_fixes**. Acceptance is the Lead's call (rule 6). This is input to it.

## Q1 — fidelity per node (my own reading: AST of `git show HEAD:<old>` against the parts + common + shim)

Method: (i) a multiset of (kind, name, sha256 of the source segment) over top-level def/class/assign, with the generated runner names (`main`, `SCENARIOS`) left out. (ii) The ordered scenario references reached from each runner (`__main__` block, `main`, top-level `for`, `run_scenarios` argument position = side_by_side/in_process), merged by old index. (iii) Whether the main path of each part reaches `finish`/`harness.finish`. (iv) An isolated import of every part: `python -B -I`, temp cwd, only that worktree's tests dir on `sys.path`, runner statements stripped so nothing runs. (v) Every module-level statement or assignment that makes a call.

| Node | (i) defs old = new | (ii) run list | (iii) closing tally | (iv) import alone | (v) side effects |
|---|---|---|---|---|---|
| N1 | 52 = 52, 0 missing / 0 extra | 29 = 29; each part's indices increasing (classify [0,1,16,17,18,20,21,22], stops [2-6], retries [7-11], tracker [12,14,15,19], texts [13,23-28]); one list + argv filter kept in every part | `finish("test_infra_failure_<part>")` at module level in all 5 | 5/5 + common OK | `START_CWD = os.getcwd()` (common:43): evaluated once per process when common is imported, read only inside common (`scenario`, `raised`). FILES/DIGEST are pure. Otherwise only `sys.path.insert` lines, kept per part |
| N4 | 41 = 41 | 24 = 24, all `__main__/main/in_process` (13+5+6) | `harness.finish` in all 3 | 3/3 + common OK | none |
| N6 | 71 = 71* | 45 = 45, `__main__/main` (8+13+24) | `finish` in all 3 | 3/3 + common + shim OK | `DROP = object()` (window_words:142), a sentinel used by that part only |
| N5 | 91 = 91 | 53 = 53, `__main__` direct calls (20+7+26) | `finish` in all 3 | 3/3 + common OK | `CLOSED_DEPTH = 20 * sys.getrecursionlimit()` (refusal:686), pure |
| N3 | 64 = 64 | 30 = 30, `__main__/main/SCENARIOS` (4+6+9+11); argv prefix filter and the "names nothing → exit" kept per part | `harness.finish` in all 4 | 4/4 + common OK | none |
| N2 (evidence) | 104 = 104 (+ shim `__all__`, `PARTS`) | 65 = 65 | **k4s and c26_g27_f2: none** | **k4s: `ModuleNotFoundError: No module named 'no_move'`** | — |

*N6: my first glob `test_controller_rework_*.py` also caught the TRACKED, pre-existing `test_controller_rework_scope.py` (107 defs instead of 71). With that file excluded, 71 = 71. The file is untouched (`git status` empty). This naming hazard is under Q6.

Why the N2 rows are the positive control: the same probe that passes the 23 files of the five nodes fails exactly on `_k4s` (F1), and the same closing walk finds no `finish` exactly in `_k4s` and `_c26_g27_f2` (F2). Both instruments discriminate.

Verified behaviour of a missing tally: `selftest.ran_nothing` (`selftest.py:458-462`) fires only for a file that defines `test_*` functions. N2's two parts define none, so in the canon they exit 0, print no tally, and a FAIL line would pass silently. F2 is a silent pass, not a loud one.

## Q2 — are F1/F2 latent in the five? Which ones must be regenerated?

- **F1 (a dropped import whose only role is its side effect: `sys.path` ← scripts/).**
  - N1, N5 and N6: every part keeps an explicit `sys.path.insert(0, str(harness.SCRIPTS | PLUGIN_ROOT/"scripts" | SCRIPTS))` statement before its first package import. The tool keeps `sys.path` lines as written, and my import-order dump shows the line in each part.
  - N3 and N4: no part imports a package module at module level before `story_run_common`. Every generated `main` calls `run_scenarios`, so `story_run_common` (which inserts scripts/ at import, `story_run_common.py:23`) is always kept.
  - The N6 parts dropped `test_story_closed` / `test_dispatch_liveness` / `person_words` / `stage_guard` against the old file. Their module-level effects are only `sys.path.insert`s and pure reads, so nothing a part relied on was lost.
  - **Provably unaffected: N1, N3, N4, N5, N6.**
- **F2 (a part with no closing finish).** Each of the five old files has ONE run block, and that block holds the `finish` (N1: module `for` + `finish`; N3, N4, N6: `main` ending in finish; N5: the `__main__` block ending in finish). The tool restricts that block, so every part carries the finish, and the closing walk confirms it. F2 needs ≥2 run blocks with the finish in only one of them. Only no_move_seam has that shape among the six. **Provably unaffected: the five.**
- **Regeneration.** Only N2 is required (by its map, after t-071). N1, N4 and N6 were cut by the first tool version. Their outputs are correct by the independent checks above, so regeneration is not needed for correctness. For P31 (one road, repeatable on a fresh `main`), I propose that the Lead dry-run the final tool on the three maps and regenerate only if the bytes differ. The old files are byte-identical between 30f16c8 (the N1/N4/N6 base) and main ba8969e (`git diff --stat` empty for all six), so no cut is stale against its source.

## Q3 — rule-2.3 decisions

- **N5:** right. Rule 2.3 is the rule, and the row's "scaffolding → common" is a hint. `OLD_JSON_KEYS` and `_apply` are part-local to `_keys`. If any other part used them, it would be an undefined name, and pyflakes is clean over the four files (I re-ran it). `_green_copy` is imported by `_main_block` (header line 13) and used by `_refusal`, so common is right. `FIXTURE` is used by `_keys` and inside common: right.
- **N3:** right for the K6-K7 helpers. They are part-local, and I ran a usage walk. `k4b_...` uses **no** part-local helper (AST: 0 references to `gate_a_story`, `staged_driver` …). Its home is free, and range-homing it in `_k6_k7` makes the part name state something false. **Fix (non-blocking, one map row on regeneration): home `k4b` in `_k1_k5`.** That restores the exact old global order (k4 → k4b → k5).
- **N1 (consistency):** `taken` (common:146) is used by `_retries` only and by nothing in common. N1 followed the row's "1-179 → common", while N3/N5 followed rule 2.3. Two readings of the same conflict is a small one-road (P31) slip. Harmless to behaviour. Fix on regeneration or leave, the Lead's call.
- **Checks in common:**
  - N1's single site is the `scenario` wrapper's `check(f"{fn.__name__} ran to its end", False, …)`. It is the runner every part needs, and it belongs in common.
  - N3's two sites are `setup:` checks inside the shared fixtures `freshness_project` (:73) and `asked_driver` (:169). They run once per call, exactly as before.
  - None of these is a module-level check (the T-B2.1 class).
  - Nothing in any common should be elsewhere, except the optional `taken`.

## Q4 — the 60 s target

"Decide at the first canon" is right. My reasons:
- Spec E2 forbids re-splitting inside the node, and §9 says per-scenario seconds are unmeasured.
- The owner ordered TD-11d (one world per file) inside this work. It changes the per-scenario cost, so a finer cut now risks churn.
- A re-cut is one map edit plus the deterministic tool.

Two cautions for the Lead:
1. The provisional seconds use check-site shares. The cost here is one world per scenario, so the scenario count is the better estimator. Infra: 320.6 s / 29 scenarios ≈ 11 s each, which gives classify (8) ≈ 88, texts (7) ≈ 77, stops ≈ 55, retries ≈ 55, tracker ≈ 44. Two parts are likely over the target, not four.
2. Rule 2.4 itself gives ceil(320.6/50) = 7 parts for infra, but the §3.1 row gave 5. The spec is inconsistent with itself; the Lead should note it.

Natural boundaries if the canon says over:
- classify at `# --- K12, K13` (`test_infra_failure_classify.py:142`);
- texts at `# --- the command, the note, the flags, the conflicts` (`test_infra_failure_texts.py:40`);
- handoff refusal at `# --- HF8-7` (`test_handoff_values_refusal.py:330`), giving A2 | HF8-7.

Local seconds, reported and not judged: tracker 29 s and main_block 31 s, six processes in parallel on Windows.

## Q5 — carriers for the closing commit

**RED in the canon if missed** (each checked by reading its reader):
1. `scripts/tests/test-layers.json` keep: the old rows of the four deleted files (infra :2016, loop_b :4452, handoff_values :1904, freshness :4433) fail `tests: keep row names no file` (`selftest.py:741`). The parts fail `unlisted:` (`:747`). AND the B2 guard (`test_selftest_slow_tests.py:477-489`) requires each part's `covers` to hold every `tests/*.py` it imports, function-level imports included:
   - every part: `tests/harness.py` and its `tests/<stem>_common.py`; N1, N3 and N4 also `tests/story_run_common.py`;
   - N6 parts: `test_controller_state`, `test_controller_rework_scope`, `test_dispatch_liveness`, `test_story_closed`, `test_story_step_manual_block`, `test_fixes_13797`;
   - N3 `_k6_k7`: `test_controller_state`, `test_controller_rework_scope`;
   - the shims: their common.

   Inheriting the old covers plus common satisfies this. Narrowing the covers below these imports turns it RED.
2. `scripts/tests/fixtures/driver-layers.json:1286-1287` (N1). L8 (`test_driver_layers.py:597-615`, keep gate_named) keys rows by (file, function). The literal `story_run.py` now sits in `test_infra_failure_stops.py:25` (k2) and `test_infra_failure_texts.py:44` (command_and_flags). Two undeclared mentions plus two "delete the row" make it RED.
3. `scripts/tests/test_window_record.py:1588-1589` (N4; keep gate_named). It does `read_text` on the deleted `test_story_run_loop_b.py`, which raises FileNotFoundError. Re-point it to `test_story_run_loop_b_loop.py`: I grepped, and "word still passes" is there.
4. `scripts/tests/test_silent_passes.py:1344` `STUB_FILES` (N2; keep detector). K24 `check_eq(got, STUB_FILES)` reads the file's text. The shim holds 0 `py` stubs against the listed 1, which makes it RED. Re-point the key to the N2 part that holds the stub. Same class as item 3: a test that reads another test file's TEXT.

**Not canon-RED, but owed in the same push:**
5. `scripts/selftest.py` TEST_TIMEOUTS :111 (infra), :129 (freshness), :145 (no_move_seam). Removing them turns `test_current_audit_contract.py:86` and `:88-89` red. That file is in **QUARANTINE** (checked in test-layers.json), so the canon is unaffected and quarantine-watch goes red. K5 forbids editing it. Per E9 the Lead marks it "перенос TD-11", or uses the `quarantine-edit:` door. The N1/N2 reports say "must change in the same commit". That is the wrong road for a quarantined file.
6. `scripts/slow_tests.json`: the old rows (:26 controller_rework → the shim is not listed, :47, :50, :58 → the shim is not listed, :114, :115) go out and the provisional part rows come in. A listed file that is absent is reported `missing` in the drift (`selftest.py:1089-1101`), which reaches the nightly `package-full-report` (max_drift). Parts that are not listed run in fast mode and weigh `fast_under_s/2` in sharding.
7. `scripts/tests/fixtures/driver-golden-rules.json:8,16,20` (N1). `driver_golden.discover` raises `Refusal("rules files.outside names test_infra_failure.py, which is not in …")` (`driver_golden.py:236-238`) on the next record. The golden is quarantined and on demand, so the canon is not affected. Re-point `outside`, the ceiling row and blind-spot `where` (→ `_texts`; `k1_data_file_is_data` is stale).
8. `design/state-exits.md` :32, :41 (N6), :57, :186 (N4), :120 (N5), :139 (N1), :187, :189 (N3). `gate_named_files` drops names that are not on disk (`selftest.py:724`), so a missed re-point loses the AR-25 proof pointer silently. :32/:41 still name the shim, which violates E4.
9. `design/architecture.md:192`, `docs/SIBLING_MAP.md:123` (N2; they name the shim, E4).
10. test-layers.json :599 (N2), :3414, :5321 (N6): covers naming the shims. They stay valid; re-point them to the parts so they mean something. :4697 is prose. :5366 is the cohort `keep_fail_at_entry` (N3), history, so leave it.
11. Prose (FR-37), with no reader that goes red:
    - `story_run_common.py:4` and `ticket_adapter.py:218` (N1);
    - `controller.py:260`, `story_run.py:126` and driver-layers.json:25 note (N3);
    - `audit_factory.py:1618` (N2) and `.github/workflows/scenario-clock.yml:4` (N4/N2);
    - `test_conductor_doors.py:641` (N4: a `PINNED_ELSEWHERE` value; the reader uses keys only, `:802`);
    - `test_words_doors.py:1320` (N6);
    - `test_story_run_loop.py:2` (N4; QUARANTINED, do not edit).

**Carriers no node listed:**
- `scripts/story_run.py:5986` ("test_no_move_seam pins that line", N2);
- `tests/test_controller_task_flag.py:310` (keep) and `tests/test_runtime_paths.py:125` (keep). Both are prose naming `test_controller_rework` with no `.py`, so the rule-2.7 `.py` grep misses them (N6);
- the B2 covers guard as a RED mechanism (item 1);
- the `driver_golden.discover` refusal mechanism (item 7). N1 listed the carrier, not that it refuses.

**One merged list for NC:** test-layers.json (keep rows + covers per item 1; the shim rows; :599/:3414/:5321) · driver-layers.json:1286-1287, :25 · test_window_record.py:1588-1589 · test_silent_passes.py:1344 · selftest.py:111, :129, :145 (+ the Lead's E9 mark on the quarantined test_current_audit_contract.py) · slow_tests.json:26, :47, :50, :58, :114, :115 · driver-golden-rules.json:8, :16, :20 · state-exits.md:32, :41, :57, :120, :139, :186, :187, :189 · architecture.md:192 · SIBLING_MAP.md:123 · prose: story_run_common.py:4, ticket_adapter.py:218, controller.py:260, story_run.py:126, story_run.py:5986, audit_factory.py:1618, scenario-clock.yml:4, test_conductor_doors.py:641, test_words_doors.py:1320, test_controller_task_flag.py:310, test_runtime_paths.py:125 · leave: CHANGELOG, test_selftest_slow_tests.py samples, test_story_run_loop.py:2 (quarantined), test-layers.json:5366 cohort.

## Q6 — standing questions

- **DUPLICATION AND CONSISTENCY.** I compared the six commons against each other, `story_run_common.py` and `harness.py` by name and by AST body hash. The commons hold no copy of each other. `raised` exists in both the N1 and N2 commons, but the bodies differ: a name collision, not a clone. One pre-existing clone is now promoted into a shared module: `story_run_freshness_common.answer_file` (:156) ≡ `story_run_common.d2_answer` (`story_run_common.py:548`), same body. A byte-identical move cannot fix it, so **queue** it (TD-11d or a follow-up). The clone ratchet is the forge-check job's; I did not run it.
- **CODE QUALITY** (generated runners). They are short and flat. No function over 60 lines in the generated code. Findings, all **queue** (tool level; no hand edit allowed):
  - (a) Copied text that now names the old file: the argv comment "`test_infra_failure.py k2_… runs only those`" in each N1 part, and the `sys.exit("test_story_run_freshness: no scenario…")` label in each N3 part.
  - (b) T-F9 holds for the N1 parts. A valid scenario name passed to the wrong part runs 0 and exits green (0/0, `harness.finish` → exit 0). The old file had the same behaviour for unknown names, but a mutation control now has to know the part.
  - (c) The tracked `test_controller_rework_scope.py` matches the parts' naming pattern. Any `test_controller_rework_*` glob treats it as a part, and my own first pass did exactly that. The shim uses an explicit `PARTS` tuple (good). Integrator and tool readers must never derive the parts by glob.
  - (d) Dead helpers moved as they were: `journal` (N6), `_scalar_paths` and `_snapshot` (N5). Queue (E11).
- **ARCHITECTURE.**
  - AR-13: no new reader of test-layers or slow_tests; the parts use harness/story_run_common. Kept.
  - AR-15: each name exists exactly once across parts + common, verified (i). Kept.
  - AR-22: the parts are producers of names that 30+ carriers read. Kept ONLY if the NC list above lands in the same push as the parts (E6). Items 1-4 starve a reader otherwise, which **blocks NC**.
- **JUDGMENT:** none. Pure code movement, no census row.
- **TESTING.md:** the parts inherit the keep row (`docs/TESTING.md:119-121`). No new test file, and the 10 s rule does not apply.
- **ONE ROAD:** one tool for every cut. The residuals are the two-version provenance (Q2) and the opposite rule-2.3 readings (Q3, `taken`). Both are minor and close by regenerating, if the Lead takes it. I grepped for a language, project or runner-name branch in the parts and found none (they are moved bodies).

## Not checked

- I did not run whole parts beyond the six controls.
- I did not run N2 (its earlier `run_*.txt` files in my scratchpad pre-date this session and are not cited).
- I did not run the clone or lint ratchets, the canon, the `--slow-tests` drift, or `test_driver_layers.py`. L8 RED is derived by reading `test_driver_layers.py:564-623` and grepping the literals.
- I could not reproduce the first tool version. N1/N4/N6 are judged on their output, not on the tool.
- I did not read the bodies of `test_controller_resume.py:574`, `test_exploration.py:554` and similar readers of state-exits.md rows. The carrier grep found no literal of the six names in them.
- The CI tallies of the old files (run 43120089137) are taken as given. The per-part sums are consistent with them, and my controls reproduced the builders' per-part numbers.

## Trail

Read:
- spec `docs/tasks/specs/td-11c-test-split.md` (all), `docs/tasks/critic-diff-brief.md`, `t-061` verdict l.9-83;
- the reports t-065/066/067/068/069/070;
- the N6 shim (whole);
- the heads and runners of N1 texts/common, N3 k1_k5, N4 threshold, N5 main_block;
- `selftest.py:440-475`, `:650-760`;
- `harness.py:199-214`, `story_run_common.py:15-30`, `:715-740`;
- `test_selftest_slow_tests.py:460-489`, `test_current_audit_contract.py:75-95`, `test_silent_passes.py:1340-1433`, `test_conductor_doors.py:630-650`, `test_window_record.py:1578-1592`;
- `driver_golden.py:205-245`, `driver-golden-rules.json:1-25`, `test_driver_layers.py:564-668`;
- the layers of 10 carrier tests from test-layers.json;
- `tools/test_split.py:1-80`.

Ran (verbatim results):
- AST multiset, run list and closing walk over six nodes: N1 52/52, N4 41/41, N6 71/71 (scope file excluded), N5 91/91, N3 64/64, N2 104/104; run lists 29/24/45/53/30/65 equal; N2 closes: k4s `[]`, c26_g27_f2 `[]`.
- Isolated import probe: 23/23 files of the five nodes `IMPORT OK`; `N2 test_no_move_seam_k4s.py exit 1 | ModuleNotFoundError: No module named 'no_move'`.
- `python -m pyflakes` over the five nodes' parts + commons: exit 0, no output.
- Importer search `git grep -n -i -E "(import|from)\s+<stem>\b|import_module|,\s*<stem>"` for each stem: only controller_rework (5 files) and no_move_seam (test_conductor_doors:970). Control `test_controller_state`, same shape: 51.
- `REWORK.<name>` across the 5 importers: 10 distinct names = the shim's `__all__`.
- Carrier grep `git grep -n -i -E "<stem>([^_a-z0-9]|$)" main -- ai-packages tools .github .gitlab-ci.yml docs/SIBLING_MAP.md plans/builder-rules.md PROCESS experiments`.
- The td-14-groups reader grep: empty. Control in the same shape: `test-layers.json` in test_quarantine.py: 10.
- Controls, each part alone:
  - `=== test_infra_failure_conductor_tracker: 40/40 ok ===` exit 0, 29 s;
  - `=== test_story_run_loop_b_answers: 106/106 ok ===` exit 0, 38 s;
  - `=== test_controller_rework_jobs_guard: 53/53 ok ===` exit 0, 12 s;
  - `=== test_handoff_values_main_block: 34/34 ok ===` exit 0, 31 s;
  - `=== test_story_run_freshness_k1_k5: 39/39 ok ===` exit 0, 26 s;
  - shim direct: `test_controller_rework.py: no checks of its own; they are in test_controller_rework_jobs_guard.py, test_controller_rework_repair_binding.py, test_controller_rework_window_words.py` exit 0.
- `git diff --stat 30f16c8 main` on the six old files: empty.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "N3 (non-blocking, on regeneration): home k4b_an_unreadable_file_with_the_question_open_never_crashes in test_story_run_freshness_k1_k5 (it uses no _k6_k7-local helper; restores the old global order k4-k4b-k5)",
    "N1 (optional, on regeneration): home taken (infra_failure_common.py:146) in test_infra_failure_retries per rule 2.3, as N3/N5 read the same conflict",
    "N2: regenerate from its map after t-071 (F1 reproduced: k4s ModuleNotFoundError no_move; F2 reproduced: k4s and c26_g27_f2 reach no finish, and ran_nothing stays silent for files without test_*)",
    "blocks NC: test-layers.json keep rows replaced in the same push; each part's covers keeps every tests/*.py it imports incl. function-level (B2 guard test_selftest_slow_tests.py:477-489)",
    "blocks NC: driver-layers.json:1286-1287 re-pointed to test_infra_failure_texts.py::command_and_flags and test_infra_failure_stops.py::k2_auth_stops_the_driver (L8, test_driver_layers.py:597-615)",
    "blocks NC: test_window_record.py:1588-1589 re-pointed to test_story_run_loop_b_loop.py (reads the deleted file's text)",
    "blocks NC: test_silent_passes.py:1344 STUB_FILES key re-pointed from the N2 shim to the N2 part holding the py stub (K24 reads file text)",
    "NC, not canon-red: TEST_TIMEOUTS :111/:129/:145 removal turns quarantined test_current_audit_contract.py:86,88-89 red in quarantine-watch; Lead marks it per E9 (no plain edit, K5)",
    "NC: slow_tests.json :26 :47 :50 :58 :114 :115 replaced (shims unlisted); driver-golden-rules.json :8 :16 :20 re-pointed (driver_golden.discover refuses a missing outside file)",
    "NC: state-exits.md :32 :41 :57 :120 :139 :186 :187 :189, architecture.md:192, SIBLING_MAP.md:123 re-pointed to parts (E4: never the shim)",
    "NC prose not listed by any node: story_run.py:5986, test_controller_task_flag.py:310, test_runtime_paths.py:125",
    "queue: answer_file (story_run_freshness_common.py:156) duplicates story_run_common.d2_answer (story_run_common.py:548); stale old-file labels copied into N1/N3 runners; T-F9 argv-in-wrong-part green for N1 parts; dead helpers journal (N6), _scalar_paths and _snapshot (N5)"
  ],
  "class_completeness": "F1/F2 class walked over all five accepted cuts: F1 provably absent (explicit sys.path line kept in every N1/N5/N6 part; story_run_common always kept in N3/N4 via the generated run_scenarios main); F2 provably absent (each old file has one run block holding finish). Carrier class 'a test reads another test file's text' found twice (test_window_record.py:1588 for N4, test_silent_passes.py:1344 for N2); carrier sweep done over ai-packages, tools, .github, SIBLING_MAP, builder-rules, PROCESS, experiments for all six stems with and without .py; three prose carriers no node listed.",
  "trail": {
    "read": [
      "docs/tasks/specs/td-11c-test-split.md",
      "docs/tasks/critic-diff-brief.md",
      "docs/tasks/specs/reviews/t-061-td11-t3-cf3-code.md:9-83",
      "worktree reports t-065, t-066, t-067, t-068, t-069, t-070",
      "agent-ac8b2ef679d592043 scripts/tests/test_controller_rework.py (shim)",
      "ai-packages/qa-factory/scripts/selftest.py:440-475, 650-760",
      "ai-packages/qa-factory/scripts/tests/harness.py:199-214",
      "ai-packages/qa-factory/scripts/tests/test_selftest_slow_tests.py:460-489",
      "ai-packages/qa-factory/scripts/tests/test_current_audit_contract.py:75-95",
      "ai-packages/qa-factory/scripts/tests/test_silent_passes.py:1340-1433",
      "ai-packages/qa-factory/scripts/tests/test_window_record.py:1578-1592",
      "ai-packages/qa-factory/scripts/tests/driver_golden.py:205-245",
      "ai-packages/qa-factory/scripts/tests/test_driver_layers.py:564-668",
      "ai-packages/qa-factory/scripts/tests/fixtures/driver-golden-rules.json:1-25",
      "td11-integration tools/test_split.py:1-80"
    ],
    "reruns": [
      {"command": "AST multiset + run list + closing walk over N1 N4 N6 N5 N3 N2 (python -B heredoc, read-only)", "result": "defs 52/52 41/41 71/71 91/91 64/64 104/104; run lists equal 29/24/45/53/30/65; N2 k4s and c26_g27_f2 close with no finish"},
      {"command": "isolated import probe python -B -I, temp cwd, runner stripped, per part/common/shim", "result": "23/23 OK for the five nodes; N2 test_no_move_seam_k4s.py exit 1 ModuleNotFoundError: No module named 'no_move'"},
      {"command": "python -m pyflakes <five nodes' parts + commons>", "result": "exit 0, no output"},
      {"command": "python -B test_infra_failure_conductor_tracker.py", "result": "=== test_infra_failure_conductor_tracker: 40/40 ok === exit 0"},
      {"command": "python -B test_story_run_loop_b_answers.py", "result": "=== test_story_run_loop_b_answers: 106/106 ok === exit 0"},
      {"command": "python -B test_controller_rework_jobs_guard.py", "result": "=== test_controller_rework_jobs_guard: 53/53 ok === exit 0"},
      {"command": "python -B test_handoff_values_main_block.py", "result": "=== test_handoff_values_main_block: 34/34 ok === exit 0"},
      {"command": "python -B test_story_run_freshness_k1_k5.py", "result": "=== test_story_run_freshness_k1_k5: 39/39 ok === exit 0"},
      {"command": "python -B test_controller_rework.py (N6 shim, no --all)", "result": "prints the three part names, no checks, exit 0"},
      {"command": "git grep importer search per stem, control test_controller_state", "result": "importers only for controller_rework (5) and no_move_seam (1); control 51"}
    ]
  }
}
```
