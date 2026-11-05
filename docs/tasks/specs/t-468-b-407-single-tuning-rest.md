# t-468 / B-407 — the rest of the single-tuning inventory, parts A-map, A, B-run, B-report, B-deps, C, D (ACCEPTED REVISION t-492, 06.10.2026)

Lead: accepted by trail after critics t-483 and t-479; every amendment applied, the camel rule placed inside `test_locations` step 4 through `name_marker` (the designer's refinement stands: it keeps B-415's step 3 invariant). Order: B-415 → Part A; B-404 → B-run; B-416 → B-report; B-run and B-report serialize on `run_suite.py`; D independent. Status: builders next, one dispatch per part. The builder reads this file whole; its `## Manifest` header lines (given/owns/non-goals/handoff/edges/DoD) are the dispatch's manifest; the CHANGELOG line and the backlog rows named under 'Needed from integration' are the integrator's. Live proof (FR-33) gates the release.

---

# B-407 (revised for t-492): the rest of the single-tuning inventory. Test files, runners, a role's words, money

REVISED DRAFT by designer, 06.10.2026. Nothing was written to the tree. This replaces the accepted draft `docs/tasks/specs/t-468-b-407-single-tuning-rest.md` as a whole. Package paths are relative to `ai-packages/qa-factory/`; the repository root is `D:/ws1/yml-text-factory`.

## Lead amendments after the critic re-review t-536 (07.10.2026 03:10) — these override the parts below where they conflict

The critic's report with the probes: `docs/tasks/specs/reviews/t-536-critic-rereview-b-407.md`. Every item is decided by the Lead and binds the part named.

- **1 (Part A, A5 + the Consumer table "handoff production", BLOCKS).** On the reference project `run.levels` hides the markers (`test_locations._recognition` answers at step 2b before step 4): the spec's rule turns 5 test files of the 13797 impl-diff into production rows (5 → 10). Rule replaced: NOT production iff (`v.test` and `v.source` not in {`run.levels`}) or (`v.source == "run.levels"` and `markers(p)`); `roots.test` gets the same treatment as `run.levels` when it names a folder that is not wholly tests (state the edge). New key K-A4b: a fixture shaped like the reference project (the impl repo under `app_root`, a `run.levels` glob over `<impl>/tests/**`, base resolved) — `tests/x/test_a.py` excluded. Mutation "handoff accepts run.levels only through v" killed in `test_handoff.py`.
- **2 (Part A, A5 "Impl checkout", BLOCKS).** `implementation.repo` does not exist; the manifest carries `implementation.repo_id` / `local_path` and the readers accept `implementations[]` (`context_bundle.py:40-42,70,121`, `judge_diff.py:64-66`). Replaced: the entry of `implementations[]`, or `[implementation]`, read through ONE shared helper (name it; no third copy of the `implementations or [implementation]` shape); more than one entry is ambiguous; its `repo_id` is matched to config `implementation_repos[].repo_id` → `local_path`, else to `code_repos[].name` → `path` (relative to the project root); the manifest's own absolute `local_path` is a hint only (SIBLING_MAP axis 8), never the base.
- **3 (Part A, A1, BLOCKS).** `hooklib.norm` lower-cases the path, so the camel rule never fires in step 4 / `suggest` / `check`. Added: `name_marker` receives the ORIGINAL-case last segment from the caller's raw `path` (`Path(text.rstrip('/\\')).name` in `_is_test_path`; `segs[-1]` in `suggest`/`check`), lower-cases internally for the four existing lists; `_marker_hit`'s stem branch delegates to `name_marker` (one stem matcher); `markers()` must not lower-case `stem_camel_suffixes`. New key K-A1b: `FooTests.cs` outside protected code with no config → `v.test` True, `by` "markers".
- **4 (Part A, A4 segmenter, BLOCKS).** `shlex` in posix mode eats Windows backslashes (`git commit -m x tests\test_a.py` → `teststest_a.py`): a narrowing in the unsafe direction, and a fourth segmenter. Replaced: segments from `hooklib._scan(cmd, 'powershell' if the event tool_name == 'PowerShell' else 'bash')`, the `$( )` regions scanned one level down; a public alias `hooklib.command_segments(text, dialect)`; `hooklib.py` joins Part A's owns (that alias only). K-A5 gains `tests\test_a.py` and `git add tests\x.py && git commit -m x`.
- **5 (Part A, may follow).** The exec/raw command-text mismatch (`stage_guard.py:1153` vs `guard_pre_tool.py:1369`, t-467:476) is a QUEUED row, named in Part A's non-goals (`guard_pre_tool.py` is B-414/416's).
- **6 (B-run, B4, BLOCKS).** `is_pytest_command` stays the gate of the pytest path; `runner_row` is consulted only to word the note for a launch that is not pytest (an unreadable `launch-causes.json` never switches the pytest id check off — E-B-run-5). The note fires only when `selected_instance_ids` carry a selector token, never for a whole-suite run.
- **7 (Part C, C3/K-C5, BLOCKS) — decided (a):** C3 = "under tests_root and is_code_file and (markers(p) or (v.test and v.source not in {`tests_root`, `roots.test`}))" — consistent with F-3 on every spelling of `tests_root`.
- **8 (Part C, C2/E-C7 and owns, BLOCKS).** E-C7 replaced: B-373 (c) creates `scripts/assertion_detectors.py` (`assertion_probes`, `assertion_heads`); Part C, AFTER it, adds the `assert_lines` key (C2's six patterns) to `detectors.json` and ONE accessor `assert_line_patterns(doc)` in that module; `check_self_fixes` uses `assert_lines` ∪ `assertion_heads`; Part C owns `scripts/assertion_detectors.py` for that accessor only. An unreadable or malformed key gives today's `ASSERT_LINE_RE` set as a code floor plus an ORACLE_NOTES line — never "no check" (E-C4: self_fixes may only over-refuse).
- **9 (Part C, C6 and the Parts table, BLOCKS).** `qa-code-critic.md` is 9327 bytes today (`selftest --limits`: info over the old 9000 cap; A25 bounds the dispatch): "≤ 9000 bytes" replaced with "byte-neutral against the file as left by B-373 (c), checked by `test_audit_rules.py` (A25)". Order: C after B-373 (c) on `qa-code-critic.md` and after B-364 on `judge_code.py` (t-463 owns :49-51).
- **10 (Part D, D1, BLOCKS).** The consumer value must match `[A-Za-z0-9_.-]{1,128}` (today's class, `cost_capture.py:833`); anything else becomes the row's `unknown_consumer_label` (a `:` in a group would shift `key.split(":",3)`). Within one tool_use a span matched by an earlier row (package first, then project, in data order) is not matched again; a project row reusing a package id is skipped and named in `forms_problem` (E-D2, no double count).
- **11 (facts, may follow).** Line drift: `guard_pre_tool.py:1336` → :1371; `gate_preflight.py` −4 after B-408 (:1855-1990 → :1851-1986; :1875-1884 → :1871-1880; :1981-1989 → :1977-1985; :1970-1972 → :1966-1968; :1870-1872 → :1866-1868); `test_protected_test_path.py:278-283` → :299-303, :270-283 → :296-303; `hooklib.py` +1 (`load_ref_json` :278). D's manifest: B-408 left `judge.py` UNCHANGED; the non-goal "`_post`/HTTP (B-408)" becomes "a queued row (judge._post keeps its own User-Agent, t-510)". `command_shapes` / `_is_commit_shape` exist only after B-405/406: A waits for it.
- **12 (B-deps, may follow).** `_rehearsal_key` takes no cfg: read `self.config` (:788), keep the signature (`onboarding_probe.py:304` overrides it). TEMPORAL edge: at onboarding the config may not exist, so `run.dependency_files` is absent — a project listing extra files gets an onboarding proof that never matches gate A (safe: one extra rehearsal); state it. The key's dict uses names; patterns and project paths use the cwd-relative path (the reference key stays byte-identical: pyproject.toml and poetry.lock only).
- **13 (duplication, may follow).** A-map reads `test_locations.skip_dirs()` (:81); B-deps/D load data through `hooklib.load_ref_json` (:278); `_LEGACY_NOT_EXECUTED` lives where stand_health can import it without run_suite (`launch_check`); B2 sets the field before `nothing_ran` at :1470.
- **14 (Siblings, the queued runner-table row, may follow).** The row also names `launch_check._programs_run` (:239), the two loaders (`hooklib._load_run_forms` :514 vs `launch_check.load_data` :75), `_EXE_SUFFIXES`/`_name` (hooklib :441/:608 vs launch_check :56), `report_cures._is_pytest` (:49), and B-report's `command_formats` as a second substring→kind table. B-run neither converges these nor adds a third wrappers walk.
- **15 (B6, may follow).** The cure words' prose twins at `config-keys.json:492` and `templates/config.json` keep the hard-coded dotnet/karma/jest words — queued (FR-10).
- **F-11 (partly overturned, decided (a)).** A call of an agent whose form is in no row is indistinguishable from any Bash command, so `complete` stays True — the price prints `recognized_forms` beside it ("external calls counted for: testproject1, …"; analog 12 pulled into D) so an unknown agent form is visible (FR-41). `invoke` is still never a search needle.
- **Seams restated.** B-run and D can start NOW (their inputs merged; no file shared with a node in build; `judge.py` untouched by B-408). A after B-405/406 (`command_shapes`, `_is_commit_shape`, stage_guard/handoff_check). C after A, B-373 (c) and B-364. B-report after B-416 and B-run; B-deps after B-416, B-414 (`gate_preflight.py`) and A. The B-415 Q4 warning-wording conflict (a whole-root entry silences markers) is nobody's: queued.

---

## Changes from the accepted draft

All t-483 B-407 amendments and the two t-479 items are applied. One placement is a refinement, explained in row A/1. Nothing is refused.

**Missing review file.** The t-479 report does not exist on disk:
- Glob `docs/tasks/specs/reviews/*` finds only t-478, t-480 and t-483 (the same call is its own positive control).
- `logs/routing-log.jsonl` has only t-479's `delegated` line (:1261).
- B4 and the seam line are therefore applied from the Lead's quotation in this dispatch.

| # | Amendment | What changed |
|---|---|---|
| A/1 | applied | `test_files.is_test_path` is built on B-415's `test_locations.is_test_path(...)` six-key verdict (`test`, `by`, `source`, `kind`, `where`, `reason`). There is ONE markers loader, `test_locations.markers()`, extended with `stem_camel_suffixes`/`code_extensions`. `scripts/test_locations.py` enters Part A owns, serialized after B-415. The "when that function exists / False when absent" text is gone. **Placement:** the camel rule goes INTO `test_locations` step 4 (markers) through one shared function `test_locations.name_marker(segment, table)`. It does not sit as a separate OR beside the verdict. An OR outside the verdict would bypass B-415's step 3 (F2 b: inside application code with a live config, only config answers) and recreate the disagreement t-483 A/1 flagged. "Verdict OR camel" therefore holds inside the verdict, as `by: "markers"`. Consumers that must also read markers past step 3 do so explicitly, per the consumer table. |
| A/2 | applied | `needs_stage_guard` returns True on the `git commit` substring; `command_shapes(command, cfg, event)` decides. |
| A/3 | applied | `test-harness` is added to `dir_names`. Reason: today's handoff exclusion `(docs\|tests?\|test-harness)/` (`handoff_check.py:144, :319`), so the superset claim stays true. The exact-lists pin `test_protected_test_path.py:278-283` is updated (Part A owns that one pin). |
| A/4 | applied | Handoff base = the checkout of the implementation repository the diff was taken from (resolution rule in A5). |
| seam rule | replaced | "Gates accept only by==config, advice also markers" is replaced by the per-consumer error-direction table (Part A, §Consumer table). |
| B/5 | applied | `exit_means_not_executed: None` (and absent) means today's rule `{2,3,4,5}`. The consequence is said aloud in E-B-run-1, with new fork F-14: mocha and other row-less runners keep today's reading until a runner row exists. |
| B/6 | applied | `runner_row` catches `_ShapeUnavailable` and returns it as the `problem`. `_SHAPES` stays code, so the FR-13 claim for runner rows is partial, said aloud in E-B-run-4. |
| B/7 | applied | `summary.reporter_inferred_from: <row id>`. A zero-test or raising read of an inferred kind adds a `parse_gap` naming the row and `run.reporter`. `vstest … /logger:junit` and `ng e2e` are pinned in E-B-report-3. Typed runs pass `args.reporter` (`run_suite.py:2093`, read), so inference reaches untyped runs only. |
| cut | applied | Part B is cut into **B-run** (B1–B4, behind B-404), **B-report** (B5–B6, behind B-416; B-416's project cure rows feed the fallback) and **B-deps** (B7–B8, the D-0023 rehearsal key, behind B-416/B-408/B-414 on `gate_preflight.py`). B-run and B-report serialize on `run_suite.py`. A4 is split out of Part A as **A-map** (`repo_map`, advice only). Each part has its own Manifest with absolute `owns:`. |
| C/8 | applied | K-C5 uses `qa/helpers/latest.py` with `tests_root: "qa"`. |
| C/9 | applied | C5 (arch_check) is `names_a_test(rel) or (v.by == "config" and v.kind == "file")`. |
| C/10 | applied | The stage-id note fires only for stages that are `pending` or `halted`. The `running` stage and `done` stages are excluded. |
| D/11 | applied | A golden dict for `tool-123` is computed BEFORE the change and is K-D1's witness. |
| D/12 | applied | The testproject1 row is kept in code as the floor; unreadable forms data gives `complete: False`. |
| D/13 | applied, widened in the same function | The form `id` / `call_id_prefix` grammar is stated (no `:`, `~` or whitespace). `judge.settings` names ALL its silent coercions in one `problems` list: unknown provider, unknown `mode` (:119), unreadable config (:114-115), and a `judge` block that is not an object (:113). |
| t-479 B4 | applied | Shared signatures are `command_shapes(cmd, cfg=None, event=None)` and `_is_commit_shape(cmd, cfg=None, event=None)`; `command_shape` = the first of `command_shapes`. Order: B-399 → B-405/406 → B-407A. `_is_commit_shape` takes its OWN quote-aware `git commit` (and `git add`) segments, so text inside another command's quoted argument is never a commit (E-A10). |
| t-479 seam line | applied | `launch_check.runner_row` is written by B-407 **B-run** (B-404's non-goals exclude `launch_check.py`, `t-466:309`). A backlog row is queued in Siblings: "two runner tables in launch-causes.json → one reader". |
| new facts | added | <ul><li>B-416's owns include `gate_preflight.py`, `report_cures.py`, `report-cures.json` and `test_reporter_rehearsal.py` (`t-475:719-739`), so B-deps and B-report serialize behind B-416.</li><li>B-404's `test_run_forms.py` key 1 pins "`collect_forms` unchanged" (`t-466:231-232`), and `test_launch_check.py:579-580` pins the one pytest row. B-run owns both pins.</li><li>B-415 adds `skip_dirs` to the markers (`t-476:185`). A-map reads it, which replaces the accepted draft's small choice of extending a code list and partly closes analog 4.</li></ul> |

## Lead decisions carried (from t-468, with this revision's updates)

- **F-1:** (b), realized as B-415's six-key verdict. B-415's amendment makes `profiles[].roots.test`, `run.levels` and `tests_root` (not `"."`) config sources with `source` naming the carrier. Consumers choose by the table below.
- **F-2:** (a). The markers file gets additive lists plus `test-harness`.
- **F-3:** (a). The narrowing is pinned (list updated per t-483 Q4).
- **F-4:** (a).
- **F-5:** (a), `collect_forms` + `runner_row`, now written by B-run.
- **F-6:** (b). **F-7:** (a). **F-8:** (a), with the C/10 exclusion. **F-9:** (a). **F-10:** (a).
- **F-11:** (a). Owner's word (06.10.2026): a technical decision; the requirement is that it works on any project with any agents. Lead: `adapters.ticket.invoke` is NOT parsed and nothing is derived from it — the forms are data rows matched on the command text (`command_re`), the floor is today's testproject1 row, and a project with another agent adds its own row under `cost.external_agent_forms` (D1 as drafted); a call that matches no row is counted under `unknown_consumer_label` and named in `forms_problem`, never dropped silently.
- **F-12:** (a). **F-13:** a backlog row.

## Why (measured, each fact from a file I read)

**(a) Nine independent test-file recognizers.**
- `scripts/stage_guard.py:80` `TEST_FILE_RE`, searched over the whole raw command in `command_shape` (:775-785). The fast gate `needs_stage_guard` (:1179-1182) is called without an event (`guard_pre_tool.py:1336` per t-483).
- `scripts/arch_check.py:37`. The locator rule fires only on files it matches (:95). `_collect` has its own extension tuple (:116).
- `scripts/repo_map.py:146` (`rglob("*.py")`) and `:186-187`. `TEST_DEF_RE :70` is Python-only. The empty-map text at :400-402 gives no reason.
- `scripts/gate_preflight.py:474-475` `REPORTER_TEST_GLOBS`, read by `first_test_file :498-513`. Not silent: the card at :1981-1989 names `gate_rehearsal.reporter_probe_test`. But it claims "I found no existing test" after a search by file name only.
- `scripts/validate_artifacts.py:1479` `TEST_CODE_SUFFIXES`, read by `is_test_code :2146-2158`. Today any name containing "test"/"spec", or a part named tests/test/spec/e2e, counts.
- `scripts/handoff_check.py:143-146` and `:318-321`: two copies of one production filter, `(^|/)(docs|tests?|test-harness)/` (case-sensitive) plus `"test_" not in name`.
  - `backend/Tests/XTests.cs` counts as production (fixture shape `tests/test_red_sandbox_reports.py:198`).
  - `src/contest_service.py` and `src/latest_report.py` are DROPPED from S2's `diff_accounting` rows. The deriver's docstring (:311-314) exists to prevent exactly that loss.
- `scripts/judge_run.py:206`.
- `scripts/judge_code.py:67-76`, which decides which questions are asked (`questions_for :203-221`).

**Data that already exists.**
- `references/test-path-markers.json` holds four lists. `dir_names` lacks `test-harness`, and there is no CamelCase suffix. The exact lists are pinned at `tests/test_protected_test_path.py:278-283`.
- `detectors.json` `sleep` (:16-20) has no reader. Grep for `"sleep"` in `scripts/*.py` finds only arch_check's rule name; control: `retry_markers` is read at `validate_artifacts.py:2167-2177`.
- `ASSERT_LINE_RE` is at `validate_artifacts.py:1478`, used at :1979-1980. It is case-sensitive and `\b…\b`-anchored, so `Assert.Equal(`, `assertEquals(`, `.Should()` and `require.NoError(` are not assertion lines. (The inventory's ":2147 ASSERT_LINE_RE" conflates two places.)

**(b) Exit codes.**
- `run_suite.py:715` applies `{2,3,4,5}` to every runner in `nothing_ran :718-727`. But in run_suite that is not a verdict: `execution_status :910-931` reads only 124 and the totals, and `nothing_ran` is read only at :1470, to attach `error_head`.
- The reader that acts on it is `stand_health.py:61/:164`: `counts` gates the stand signals (:202, :240, :299), and the signals stop repair rounds (:19-21).
- Runner facts: `references/launch-causes.json` `collect_forms` holds one pytest row (:18-20). `launch_check.load_data :143-158` requires `append` and `ok_exits`. `_SHAPES = {"pytest": _is_pytest}` (:534) is code. `_is_pytest` raises `_ShapeUnavailable` (:525-529).
- B-404 adds a sibling key `run_forms` and does not touch `launch_check.py` (`t-466:9, :309`).

**(c) Dependency files.**
- `execution_request.py:505-506` holds six names. They feed the fingerprint (:2281-2282) and the D-0023 rehearsal key (`gate_preflight.py:1875-1884`, together with `REPORTER_CONFIG_FILES :495`, which is pytest-only).
- Reference project measured (PROJECT.md 6a): across `D:/ws1/testproject1-dev-fresh\testproject1-sdk\test-harness`, the candidate names present are only `pyproject.toml`, `poetry.lock`, `Makefile` and `testproject1_test_harness/pytest.ini`.

**(d) Stage claims.** `validate_artifacts.py:1475-1477` `STAGE_DONE_RE` is an English phrase list over a role's words, which FR-12 forbids. It refuses (`check_stage_claims :1501-1514`, the only caller is :1690), pinned by `test_validators.py:111-112`. Per t-483 C/10:
- `stage_done.py` keeps statuses in `pipeline.json`.
- S9 reads `report_facts.check`, not this check.
- The verdict head stays code-checked at :1686-1689.

**(e) External agent calls.** `cost_capture.py:831` has one testproject1 regex, and `inferred_external_calls :971-983` builds only that call. `external_reconciliation :960-968` says `complete: not unknown`, which feeds `match` (:1446-1450). Legacy keys `__external__:<hash>:<consumer>:<ts>` persist in checkpoints (:899-900). `tests/test_usage_activity.py:120-136` asserts only the consumer and `pending`; it does not pin the id.

**(f) Judge settings.** `judge.settings :107-124` coerces silently:
- an unknown provider → `"none"` (:116-118);
- an unknown mode → `"shadow"` (:119);
- an unreadable config → `{}` (:114-115);
- a non-dict `judge` block → `{}` (:113).

`readiness.py` never mentions the judge (case-insensitive `judge`: 0; control `load_config`: 2).

**(g) Node ids.** `run_suite.verify_node_ids :1165-1167` returns None for non-pytest commands, and :1173-1176 for an ImportError. The registry row `collected_ids` (`gate-registry.json:148-167`) promises "named as not verified". Debt: B-278 (`BACKLOG.md:230`) and `factory-rules-debt.md:130`.

**(h) Reporter choice.**
- `run_suite.resolve_reporter :257-273` chooses by substrings that duplicate `report-cures.json` rows.
- `:1458-1464` hard-codes three rows' words.
- Typed runs set `args.reporter = request["command"]["reporter"]` (:2093).
- B-416 adds project cure rows tried before the package rows in `report_cures.load`/`row_for` (`t-475:559-560`).

**(i) s5_precheck.** `s5_precheck.py:1854-1857` skips non-Python files. Yet `report :1920-1925` still prints "OK … Then bindings … test smells", and `agents/qa-code-critic.md:26-27` tells the critic not to re-check them. `judge_code.render :300-302` says "none skipped" after `targets :160-162` skipped files.

## Intent

The B-407 row (`plans/BACKLOG.md:433`) closes the class: closed variety goes to data; open variety is a person's word or a role's judgment; every place gets a data entry or a refusal with a door.

D-0030 verbatim: "Where a project keeps its tests is the project's own word: the person names the places inside the application repository and the factory accepts them as project configuration, protecting from change only the part that holds the application code itself (P-00); the marker list `references/test-path-markers.json` is not a gate, and a project with other names for its tests gets its entry, not a refusal."

Also D-0028 (B-373 seam) and D-0031 (B-416 seam).

## Parts and order

| part | what | owns (files) | after |
|---|---|---|---|
| A | test-file recognition + the consumer table; stage_guard, handoff, judge_run | test_files.py (new), test_locations.py, stage_guard.py, handoff_check.py, judge_run.py, test-path-markers.json + tests | B-415; B-399 → B-405/406 (stage_guard.py, handoff_check.py) |
| A-map | repo_map, advice | repo_map.py + test | A |
| B-run | runner rows, nothing_ran, stand_health, node-id notes | launch_check.py, launch-causes.json, run_suite.py (B1-B4 sites), stand_health.py + tests | B-404; before B-report (run_suite.py) |
| B-report | reporter inference, parse_gap words | run_suite.py (B5-B6 sites), report-cures.json (additive key) + test | B-416; B-run |
| B-deps | dependency files, rehearsal key, first_test_file | execution_request.py, gate_preflight.py, dependency-files.json + tests | A; B-416, B-408, B-414 (gate_preflight.py, test_reporter_rehearsal.py) |
| C | validators and judges over words and test code | validate_artifacts.py, judge_code.py, arch_check.py, s5_precheck.py, detectors.json, qa-code-critic.md + tests | A; B-373 ↔ C on detectors.json (either order) |
| D | money and the judge's settings | cost_capture.py, judge.py, external-agent-calls.json + tests | B-408 (judge.py) |

`[meaning]` requirements are in A, B-run (B3), B-report (B5), B-deps (B7), C and D1. Each goes through a critic-on-plan review before its builder (PROJECT.md item 6). t-483 has already reviewed the plan; a re-review covers this revision.

## Place table: mechanism, and the default that keeps today's Python+pytest+Jira+GitLab project unchanged

| place | part | data entry / door / safe default | today's project |
|---|---|---|---|
| stage_guard.py:80 | A | verdict union + markers; quote-aware commit/add segments | every test name and folder caught today is caught (+ `test-harness`); the narrowed names are pinned (F-3) |
| arch_check.py:37 (+:34-35, :116) | C | `names_a_test` or config-file verdict; shared sleep/locator shapes | `asyncio.sleep(n)` becomes a finding (F-9) |
| repo_map.py:146,187 | A-map | code_extensions, names, `kind`, `skip_dirs`; the empty map names its reason | `.py` maps unchanged; `.js`/`.ts` helpers under test roots may enter the ranking (advice) |
| gate_preflight.py:474-479 | B-deps | `names_a_test`; the existing card + `reporter_probe_test` stay the door | pytest picks the collect node first (:1970-1972) |
| validate_artifacts.py:1478 | C | `detectors.json` `assert_lines` (shared with B-373) | today's lines stay caught (superset pinned) |
| validate_artifacts.py:1479, :2146 | C | union + `code_extensions` | `qa/helpers/latest.py` stops being test code (F-3); `tests/**` stays |
| handoff_check.py:143-146, 318-321 | A | the verdict minus `run.levels`; base = the implementation checkout `[meaning]` | `tests/test_x.py`, `test-harness/x` still excluded; `src/contest_x.py` becomes a row |
| judge_run.py:206 | A | names on segments | `test_*`, `tests.*` still skipped |
| judge_code.py:67-76 | C | `detectors.json` `sleep`/`locator`/`negative_code`; unreadable means ask more | everything asked today is still asked |
| run_suite.py:715-722 | B-run | pytest row `not_executed_exits [2,3,4,5]`; None means today's rule | unchanged |
| stand_health.py:61 | B-run | reads `exit_means_not_executed`; None/absent means today's rule; 127 stays `[meaning]` | unchanged |
| execution_request.py:505 | B-deps | `dependency-files.json` + `run.dependency_files`; floor of six `[meaning]` | same files fingerprinted (measured) |
| validate_artifacts.py:1475-1477 | C | stage-id presence note for pending/halted stages; the role judges `[meaning]` | a true report raises nothing |
| cost_capture.py:830, 975-978 | D | `external-agent-calls.json`; testproject1 floor in code; golden pin | the same ids |
| judge.py:39, 117 (+113-119) | D | door: `problems` named in `ask`/`status`; safe default off/shadow | none/typesafe unchanged |
| node_ids.py:56, run_suite.py:1166 | B-run | runner row `node_ids`; a "not verified" note | pytest unchanged |
| run_suite.py:257-273, 1462-1464 | B-report | `command_formats` + row fallback with `reporter_inferred_from`; words from `report_cure` `[meaning]` | pytest/`dotnet test`/jest/karma resolve as today |
| s5_precheck.py:37, 1854-1858 | C | `unchecked[]`, a true OK line, the critic text | Python stories byte-identical |

Not owned: `scripts/node_ids.py`. It is pytest's checker by design; the silence is in its caller (`verify_node_ids`).

---

## Consumer table: per-consumer error direction (carried by Part A, implemented in `test_files.is_test_for`)

Let `v = test_locations.is_test_path(path, cfg, base=..., root=...)`, the six-key verdict. Its `source` is one of `test_locations`, `run.levels`, `roots.test`, `tests_root`, `markers` or `""`. Below, "markers" means `names_a_test(p) or in_test_folder(p)`, evaluated directly, past B-415's step 3.

| consumer | which error is unsafe | rule | markers unreadable |
|---|---|---|---|
| guard carve-out (B-415 R3; listed here, written there) | false "test": app code opened | `v.source == "test_locations"` only; never `run.levels`/`roots.test`/`tests_root`/markers | n/a |
| stage_guard commit shape (A) | false "not test": a test commit skips rule 5 and the manifest rule | `v.test or markers` | treated as a commit |
| validate `is_test_code` (C) | false "not test": detectors skipped | under tests_root and `is_code_file` and (`v.test or markers`) | not test code + one ORACLE_NOTES line; amended 07.10 (t-562, the Lead's override): a file under `tests_root` is test code by `CODE_EXTENSION_FLOOR`, with one ORACLE_NOTES line saying the markers could not be read |
| handoff production (A) | false "test": a production row dropped | not production iff `v.test and v.source != "run.levels"` (step 3 applies); docs/`.md`/`.lock` as today | production |
| arch_check test body (C), repo_map test file (A-map) | advice | `names_a_test(name) or (v.by == "config" and v.kind == "file")`; a repo_map helper = `v.test` and not a test file | not a test body; the reason is named |
| gate_preflight `first_test_file` (B-deps) | false "test": a helper is rehearsed | `names_a_test(name)` | `""`, so the existing card |
| judge_run `wanted_names` (A) | noise against a missed name | a segment `names_a_test` or ∈ `dir_names` | skip nothing |
| blast_radius caller/test split (G1-2) | false "test": a caller hidden among the tests | `TF.file_kind(path) == "test"` only, as the grounding table calls it (one kind per file); a site in any other file is a caller, a doubt errs to production | `file_kind` falls to its own default: production |

Invariant of the table: each consumer errs only in its own safe direction, and no consumer's rule is weaker than today's on the recognized side, except the F-3 names.

---

## Part A: "is this a test file", the consumer table, stage_guard, handoff, judge_run

### Requirements

**A1. `scripts/test_locations.py`, after B-415 lands, additive.**
- `markers()` keeps its `(table, problem)` contract. `problem` still concerns only the four grant lists. The table additionally carries:
  - `stem_camel_suffixes` (as written);
  - `code_extensions` (lower-cased, with the dot);
  - `extras_problem`.
- A malformed extra list becomes `[]` and is named in `extras_problem`. It never sets `problem`. Invariant: Part A's lists can never break a grant or B-415's guard.
- New `name_marker(segment, table) -> str` returns `"<list>:<marker>"` or `""`. It applies, in order:
  - the existing stem prefix/suffix rules (lower-cased);
  - then `stem_camel_suffixes`: the case-sensitive stem ends with S, ≥1 character before S, and when S is all upper-case the character before it is not an upper-case letter.
- Step 4 of `is_test_path` uses `name_marker` for the last segment, so camel names are `by: "markers"` and obey step 3. `suggest` uses the same function where it reads name markers.

**A2. New leaf `scripts/test_files.py`** (stdlib plus lazy `test_locations`):
- `markers()` re-exports `test_locations.markers()`.
- `names_a_test(name_or_path) -> bool|None` = `name_marker(last segment)` != "".
- `in_test_folder(path) -> bool|None`: folder segments against `dir_names`/`dir_suffixes`, lower-cased. A trailing `/` makes the last segment a folder.
- `is_code_file(path) -> bool|None`.
- `verdict(path, cfg, *, base=None, root=None) -> dict` passes through to `test_locations.is_test_path`.
- `is_test_for(consumer, path, cfg=None, *, base=None, root=None) -> bool|None` implements the consumer table for the consumers `"commit"`, `"test_code"`, `"production"`, `"test_body"`, `"test_place"`, `"name"`.

**A3. `test-path-markers.json`, additive.**
- Add `"test-harness"` to `dir_names`.
- Add `"stem_camel_suffixes": ["Test", "Tests", "Spec", "Specs", "IT"]`.
- Add `"code_extensions": [".py", ".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx", ".java", ".kt", ".kts", ".groovy", ".scala", ".cs", ".fs", ".vb", ".go", ".rb", ".php", ".swift", ".rs"]`.
- Add one `_comment` sentence for the new lists and `test-harness` (reason: handoff's historical exclusion). B-415 owns the rest of `_comment` and `skip_dirs`.
- `tests/test_protected_test_path.py:278-283`: the exact-lists pin includes `test-harness`, if B-415 left that pin in place.

**A4. `stage_guard`, `[meaning]`, inside B-405's structure.**
- `_is_commit_shape(cmd, cfg=None, event=None)`:
  - Split `cmd` into quote-aware segments: `shlex.shlex(cmd, posix=True, punctuation_chars=True)`, whitespace-split; separators are `&&`, `||`, `;`, `|`, newline.
  - A **commit segment** is one whose tokens, after leading `NAME=value` tokens, begin with `git`, `commit`. An **add segment** begins with `git`, `add`.
  - No commit segment means False.
  - Path tokens are the non-option tokens of commit and add segments; values of `COMMIT_VALUE_OPTS` are skipped.
  - The shape holds when any token matches `FACTORY_PATH_RE`, or `test_files.is_test_for("commit", token, cfg, base=<event cwd>, root=hooklib.project_root(event))` is True or None.
- `command_shapes(cmd, cfg=None, event=None)` and `command_shape` = the first of them; B-405 writes these. `check_command` passes `cfg` and `event`.
- `needs_stage_guard(cmd, cfg=None)` additionally returns True when the substring `git commit` is in `cmd`.
- Delete `TEST_FILE_RE`.

**A5. `handoff_check`, `[meaning]`.**
- One function `_production_files(files, cfg, art)`, used by `_diff_counts("production")` and `_diff_files`.
- A file is excluded when any of these holds:
  - a `docs` folder segment (case-insensitive);
  - a `.md`/`.lock` suffix;
  - `is_test_for("production", f, cfg, base=<impl checkout>, root=<project root>)`.
- **Impl checkout:** the repository named by the story's `context-manifest.json` `implementation.repo`, resolved by name through config `implementation_repos[].local_path`, else `code_repos[].path` (relative to the project root).
- **Unresolvable or ambiguous:** `base=None`, so config never matches and the markers verdict alone decides.

**A6. `judge_run.wanted_names`:** skip a quoted name when any segment (split on `.`, `/`, `::`) `is_test_for("name", seg)` is True or the segment equals a `dir_names` entry.

### Edges (each with its invariant)

- **E-A1, markers unreadable:** each consumer applies its table default, and one stderr note names the file. Invariant: an unreadable list never lets a test commit pass unchecked and never drops a production row.
- **E-A2, positional, hot path:** config and markers are read only after the `git commit` substring hits. Invariant: a Bash command without `git commit` reads no file. The test makes the loader raise on `ls -la`.
- **E-A3:** `git add tests/a.py && git commit -m x` stays a commit shape (add segment). Invariant: a bare commit of staged test files still meets `rule_pathspec`.
- **E-A4 (F-3), narrowing, enumerated per t-483 Q4:**
  - Names: `contest_x.py`, `latest_report.py`, `my_test_foo.py`, `pytest_plugin.py`, `protest_utils.py`, `foo_test.py.bak`.
  - Paths that appear only in non-commit/add segments, e.g. `pytest tests/x.py && git commit -m x`: today a commit shape, now not. This is the analog-1 class.
  - Widening: `Tests/`, `specs/`, `__tests__/`, `test-harness/`, camel names, `test_*.go/.json`.
  - Invariant: a name, folder or project place recognized as a test is recognized by every consumer of its row.
- **E-A5, temporal:** B-415 lands first, so `test_locations` exists before Part A. Part A's builder does not start until `scripts/test_locations.py` is on main. Invariant: no stub seam that is always False ships.
- **E-A6, base mismatch** (unresolvable impl checkout): only markers decide, so the safe direction is an extra row. Invariant: a production file is never dropped for a base the code could not establish.
- **E-A7, the reused verdict in a more consequential role (handoff).** It may err toward production only. Adversarial inputs that must stay production:
  - `src/contest_service.py`, `src/latest_report.py`, `src/attestation/x.py`, `src/testing/helpers.py`, `src/AUDIT.java`, `src/Contest.cs`, `src/protest_utils.py`, `src/pytest_plugin.py`;
  - and a file matched only by `run.levels`.
- **E-A8, camel boundary.** True: `FooTests.cs`, `FooTest.java`, `UITest.cs`, `FooIT.java`, `FooSpec.scala`. False: `Test.java`, `AUDIT.java`, `Latest.java`, `MyTEST.cs`.
- **E-A9:** a trailing-`/` token is a folder; empty and `.` tokens are ignored.
- **E-A10 (t-479):** `glab mr create --body "… git commit -m x tests/x.py …"`. The quoted body is one token of a non-git segment, so there is no commit segment and no commit shape. The delivery rule still applies (B-406). Invariant: only a real `git commit` invocation meets rules 5 and the manifest rule.
- **E-A11:** unbalanced quotes make `shlex` raise `ValueError`. Fallback: a commit shape when `git commit` is a substring and any whitespace token is test-ish or a factory path (today-like). Invariant: unparseable input errs toward checking.
- **E-A12:** `git -C dir commit` is not recognized, as today. Reported as an analog.
- **E-A13, extras:** a malformed `stem_camel_suffixes`/`code_extensions` gives `[]` plus `extras_problem`; grants and the guard are unaffected (A1).

### Acceptance keys

- K-A1: `name_marker` is shared by step 4 and `names_a_test`; the camel rule obeys step 3 (a `FooTests.cs` inside protected code, with a live `test_locations` that does not cover it, gives `v.test == False`).
- K-A2: superset pin. Every sample of today's recognizers stays True (including `test-harness/`), except the E-A4 list, which is pinned False with its reason.
- K-A3: the consumer table, one case per row, with a monkeypatched verdict.
- K-A4: S2 rows on the extended fixture are exactly webhook, filters, contest_service, latest_report; a `run.levels`-only match gives a row.
- K-A5: E-A2, E-A3, E-A10, E-A11.
- K-A6: the grant tests stay green.

### Tests (one mutation → the one file that kills it)

- `tests/test_test_files.py` (new): K-A3, E-A1, E-A8, E-A9, E-A13.
  Mutation: a handoff rule that accepts `run.levels` → killed here.
- `tests/test_test_locations.py` (B-415's file; additive cases only): K-A1.
  Mutation: the camel check placed outside step 4 → killed here.
- `tests/test_stage_guard.py`: K-A5, plus `git commit -m x -- src/Foo.Tests/BarTests.cs` → commit.
  Mutation: scan the raw command → E-A10 killed here.
- `tests/test_handoff.py` (extend `the_diff_opens_a_row_per_production_file :368`): K-A4.
  Mutation: keep `"test_" not in name` → killed here.
- `tests/test_judge_run.py`: `wanted_names` keeps `API_BASE_URL` and `contest_url`; skips `test_login`, `tests.api.client`, `FooTests.Bar`.
- `tests/test_protected_test_path.py`: the exact-lists pin with `test-harness`.

### Live proof (FR-33)

1. A Test Project 1 comparison story: `experiments/measurers/stage_compare.py S2` gives the same `diff_accounting` rows as the previous run.
2. A `testproject1-ui` copy (`D:/ws1/testproject1-dev-fresh\testproject1-ui`): S2 excludes `*.spec.ts`, and a commit naming a `.spec.ts` meets the commit rules.

### DoD (Part A)

Run from the repository root:
- `python -B ai-packages/qa-factory/scripts/tests/test_test_files.py`
- `python -B ai-packages/qa-factory/scripts/tests/test_test_locations.py`
- `python -B ai-packages/qa-factory/scripts/tests/test_stage_guard.py`
- `python -B ai-packages/qa-factory/scripts/stage_guard.py --selftest`
- `python -B ai-packages/qa-factory/scripts/tests/test_handoff.py`
- `python -B ai-packages/qa-factory/scripts/tests/test_judge_run.py`
- `python -B ai-packages/qa-factory/scripts/tests/test_protected_test_path.py`

Importers, once at the end:
- of `stage_guard`: test_words_doors, test_controller_rework, test_story_closed, test_stages, test_oracle_provenance, test_manifest_from_tests, test_gate_vocabulary, test_gate_preflight, test_stand_gap_remedy;
- of `handoff_check`: test_story_step, test_story_run_refusals, test_s7_null_outcome, test_blocked_by_env_window, test_story_run_gate_repair, test_repair_marker, test_field_producers, test_case_id_form_sites, test_package_generation, test_s7_pretriage, test_handoff_producers, test_null_outcomes, test_triage_identity, test_project_decisions_refs, test_artifact_writers;
- of `test_locations`: whatever `grep -l "test_locations" ai-packages/qa-factory/scripts/tests/*.py` returns after B-415 (named in the handoff);
- each as `python -B ai-packages/qa-factory/scripts/tests/<file>.py`.

Then:
- `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`
- `python -B ai-packages/qa-factory/scripts/tests/test_audit_rules.py`

The full selftest and install_smoke run in CI, not on the owner's machine.

### Manifest (Part A)

given: this spec (Consumer table, Part A, E-A, F-3/F-4); `ai-packages/qa-factory/design/factory-rules.md` (whole); `plans/builder-rules.md`; `docs/tasks/specs/t-476-b-415-test-locations.md` (R1, R6, Seams) and `t-467-b-405-b-406-adapter-forms.md` (R7-R8 on `command_shapes`); `scripts/test_locations.py` as landed by B-415; `references/test-path-markers.json`; `scripts/stage_guard.py` :72-90, :775-830, :955-958, :1152-1182, :1330-1349; `scripts/handoff_check.py` :124-150, :295-353; `scripts/judge_run.py` :60-80, :195-210; `scripts/hooklib.py` :277-346, :402-406; `tests/test_handoff.py:366-395`; `tests/test_protected_test_path.py:270-283`; `tests/test_red_sandbox_reports.py:198`.

owns:
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\test_files.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\test_locations.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\stage_guard.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\handoff_check.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\judge_run.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\references\test-path-markers.json
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_test_files.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_test_locations.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_stage_guard.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_handoff.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_judge_run.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_protected_test_path.py

non-goals:
- In `test_locations.py`, everything but A1: B-415's verdict steps 1-3, `suggest`/`check`, the CLI.
- `guard_app_under_test.py`.
- `_is_delivery_shape`, `DELIVERY_HINTS`, ticket keys, `SendMessage` (B-406/B-405/B-399).
- `rule_pathspec` and the `git commit -am` hole (analog 1).
- `repo_map.py` (A-map).
- CHANGELOG.

handoff:
- a diff summary ≤ 500 words;
- the FR walk A–G;
- verbatim test tails;
- the `needs_stage_guard` timing (1000 calls, before/after, as B-405 edge 19 asks);
- "needed beyond the manifest";
- "Needed from integration": CHANGELOG lines as text;
- analogs.

edges: E-A1…E-A13.

DoD: the Part A commands, starting with `python -B ai-packages/qa-factory/scripts/tests/test_test_files.py`.

---

## Part A-map: `repo_map` (advice only)

### Requirements

- `_walk` yields files that `is_code_file`. It skips `SKIP_DIRS` ∪ the markers' `skip_dirs` (B-415).
- `_is_test_file` = `is_test_for("test_body", rel, cfg, root=project)`.
- `_is_util_file` additionally counts a code file with `is_test_for("test_place", …)` True and not a test file (a helper in a test place).
- AST readers and `TEST_DEF_RE`/`CLASS_RE` run on `.py` only.
- A non-`.py` test file is listed with `tests: []` and `language_note: "not a Python file: its test names are not listed"`.
- `build` adds `empty_reason`: the roots read (marking those that do not exist), the files read, the files skipped by extension (top 3 with counts), and the markers problem. `render` prints it after "**The map is empty**".
- The example fence's language comes from the file extension.

### Edges

- **E-M1:** a map is a hint (FR-47). Invariant: nothing gates on it, and every empty map says why.
- **E-M2:** `skip_dirs` absent or malformed means only `SKIP_DIRS` is used. Invariant: B-415's optional list never breaks the walk.
- **E-M3:** big Java/TS repos are walked by extension. There is no new cap (today has none). The skipped-by-extension count is reported.

### Acceptance keys

- K-M1: a Java fixture gives `FooTest.java` listed with its `language_note`, and the helper ranked.
- K-M2: `empty_reason` content.
- K-M3: the Python fixture is unchanged.

### Tests

- `tests/test_repo_map.py`.
  Mutation: keep `rglob("*.py")` → killed here.

### Live proof

On a `testproject1-ui` story, the S5 map is non-empty or names its reason. On the Test Project 1 comparison run, the S5 map is unchanged.

### DoD (A-map)

- `python -B ai-packages/qa-factory/scripts/tests/test_repo_map.py`
- `python -B ai-packages/qa-factory/scripts/tests/test_brief_pack.py`
- `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`
- `python -B ai-packages/qa-factory/scripts/tests/test_audit_rules.py`

CI runs the full selftest and install_smoke.

### Manifest (A-map)

given: this spec (Consumer table, A-map); `factory-rules.md`; `plans/builder-rules.md`; `scripts/repo_map.py` (whole); `scripts/test_files.py` (Part A); `references/test-path-markers.json`.

owns:
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\repo_map.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_repo_map.py

non-goals: `UTIL_DIR_NAMES`/`STOPWORDS` (analog 10); judge re-ranking.

handoff: as in Part A.

edges: E-M1…E-M3.

DoD: `python -B ai-packages/qa-factory/scripts/tests/test_repo_map.py` and the rest above.

---

## Part B-run: runner rows, nothing_ran, stand_health, node-id notes

### Requirements

**B1. Runner rows (F-5).**
- `launch-causes.json` `collect_forms` rows gain two optional fields:
  - `not_executed_exits`: ints, default `[]`; the pytest row gets `[2, 3, 4, 5]`;
  - `node_ids`: a checker name; the pytest row gets `"pytest"`.
- `launch_check.load_data` validates them; a malformed field makes the file malformed, as today. It carries them in `out["collect_forms"]` only when present in the raw row.
- New public `launch_check.runner_row(argv) -> (row|None, problem)`, **written by B-run**. It wraps `_collect_form`, catches `_ShapeUnavailable` (and any exception) into `problem`, and returns `(None, why)` on unreadable data.
- The `about` text gets one sentence per field.
- Pins updated: `test_launch_check.py:579-580` (E2b) and B-404's `test_run_forms.py` key 1 ("`collect_forms` unchanged" becomes "unchanged except the two B-407 fields").

**B2. `run_suite`.**
- `run()` writes `summary["exit_means_not_executed"]`:
  - True: the row lists the code;
  - False: the row is known and does not list it;
  - None: no row, or a `problem`; `summary["exit_note"]` names it.
- `nothing_ran(summary)`:
  - if the field is True, True;
  - if it is None or absent, today's rule (code ∈ `{2,3,4,5}` → True);
  - then totals (`not tests`);
  - then `code not in (0, 124, None)`.
- Delete `NOTHING_RAN_EXITS`. The literal `{2,3,4,5}` stays only as `_LEGACY_NOT_EXECUTED` (the declared default for None), with a comment.

**B3. `stand_health._record` `[meaning]`.**
- `ef = summary.get("exit_means_not_executed")`.
- `ef is None` (absent or present) → `ef = exit_code in _LEGACY_NOT_EXECUTED`.
- `executed = tests > 0 and exit_code != 127 and not ef`.
- 127 stays a code constant: it is run_suite's own launch-failure code, not a runner fact.

**B4. `verify_node_ids` (B-278, first half).**
- `runner_row(argv)` with no row or no `node_ids` → `{"notes": [f"node ids were not verified: the factory lists collected tests only for runners with a node-id checker ({names}); `{argv0}` ran the ids as written"], "resolved": {}}`.
- An unknown checker name, `ImportError` of `node_ids`, or `execution.verify_node_ids: false` → a note naming it.
- The pytest path and the exit-2 refusal are unchanged. The notes reach `summary["node_id_notes"]` (`:2050-2057`).

### Edges

- **E-B-run-1 (B/5, said aloud):** with only the pytest row shipped, behaviour equals today for every runner. Mocha's exit = number of failures (scout t-457, not measured) stays "nothing ran" until a mocha row exists. A mocha row needs a recognizer in `_SHAPES` and a measured exit fact → F-14. Invariant: a runner whose exit codes the factory has no fact for is read as today, never by a guess.
- **E-B-run-2:** 124 and 127 are the runner's own codes. Invariant: a timeout is never `nothing_ran`; 127 never counts.
- **E-B-run-3:** unreadable data, or `_ShapeUnavailable`, gives None, so today's rule applies plus `exit_note`. Invariant: a broken table never changes a verdict silently.
- **E-B-run-4 (FR-13 partial):** `_SHAPES` is code, so a new runner row needs a code recognizer. The backlog row queued in Siblings is the route to one data recognizer.
- **E-B-run-5:** none of the new notes stops a launch. Invariant: only a truly missing pytest id refuses (exit 2, unchanged).

### Acceptance keys

- K-R1: with the shipped data, `nothing_ran` and `_record` equal today on the old cases (`test_run_suite_mine.py:914-918`).
- K-R2: monkeypatched data with the pytest row `not_executed_exits: [4]` → pytest exit 2 with totals counts as executed (data drives it).
- K-R3: `runner_row` returns a problem on `_ShapeUnavailable`.
- K-R4: a non-pytest launch carries the "not verified" note in the run record.

### Tests

- `tests/test_run_suite_mine.py`: K-R1, K-R2, K-R4.
  Mutation: a None field read as False → killed here (an unrecognized wrapper with exit 2 and a partial report).
- `tests/test_stand_health.py`: None/absent/True/False and 127.
- `tests/test_launch_check.py`: optional fields and K-R3.
- `tests/test_run_forms.py`: key-1 pin only.

### Live proof

1. A Test Project 1 comparison story: summaries carry `exit_means_not_executed` (pytest), and stand-health counts as before.
2. A `testproject1-ui` `run_suite` launch: `node_id_notes` carries "not verified".

### DoD (B-run)

Run from the repository root:
- `python -B ai-packages/qa-factory/scripts/tests/test_run_suite_mine.py`
- `python -B ai-packages/qa-factory/scripts/run_suite.py --selftest`
- `python -B ai-packages/qa-factory/scripts/tests/test_stand_health.py`
- `python -B ai-packages/qa-factory/scripts/stand_health.py --selftest`
- `python -B ai-packages/qa-factory/scripts/tests/test_launch_check.py`
- `python -B ai-packages/qa-factory/scripts/tests/test_run_forms.py`
- `python -B ai-packages/qa-factory/scripts/tests/test_node_ids.py`
- `python -B ai-packages/qa-factory/scripts/tests/test_gate_registry.py`

Importers of `run_suite|launch_check|stand_health`, once at the end: test_story_run_s6, test_run_suite_reports, test_reporters, test_probe_by_code, test_execution_request, test_execution_pipeline, test_s5_precheck, test_run_budget, test_live_audit_contract, test_handed_to_person, test_gate_preflight, test_onboarding_probe, test_reporter_rehearsal, test_manual_capture, test_run_block_producer, test_identity_proof_contract, test_judge_run.

Then:
- `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`
- `python -B ai-packages/qa-factory/scripts/tests/test_audit_rules.py`

CI runs the full selftest and install_smoke.

### Manifest (B-run)

given: this spec (B-run, F-5, F-14); `factory-rules.md`; `plans/builder-rules.md`; `docs/tasks/specs/t-466-b-404-run-forms.md` (R1, E10, keys 1-12); `scripts/launch_check.py` :75-160, :515-545; `references/launch-causes.json`; `scripts/run_suite.py` :700-753, :1150-1216, :1309-1490, :2040-2060, :1686-1830; `scripts/stand_health.py` :40-190; `references/gate-registry.json` :148-167.

owns:
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\launch_check.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\references\launch-causes.json
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\run_suite.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\stand_health.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_run_suite_mine.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_stand_health.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_launch_check.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_run_forms.py

non-goals:
- `run_forms` rows and `hooklib` (B-404);
- `resolve_reporter`/`parse_gap` (B-report);
- `node_ids.py`;
- `ERROR_HEAD_PREFIXES` (analog 3);
- the gate-template conversion of `collected_ids`;
- in `test_run_forms.py`, anything beyond key 1's pin.

handoff: as in Part A, plus "Needed from integration": the `factory-rules-debt.md:130` rewording (the non-pytest / import-error part is closed; the template remains).

edges: E-B-run-1…5.

DoD: `python -B ai-packages/qa-factory/scripts/tests/test_run_suite_mine.py` and the rest above.

---

## Part B-report: reporter inference and parse_gap words

### Requirements

**B5 `[meaning]` (F-6 b).** `resolve_reporter` order:
1. explicit;
2. `run.reporter`;
3. `report-cures.json` `command_formats`, a new top-level key that is today's list VERBATIM, in order: `[{"kind":"pytest","contains":["pytest"]},{"kind":"trx","contains":[".trx","logger trx"]},{"kind":"junit-xml","contains":["junit","--reporters","jest","karma","ng test","dotnet test"]}]`;
4. `report_cures.row_for(argv, <B-416's project root argument>)["reporter_kind"]` when non-null. Project cure rows (B-416) are tried first. This step sets `summary["reporter_inferred_from"] = <row id>`;
5. `"none"`.

If the table is unreadable: `"pytest"` if `is_pytest_command(argv)`, else `"none"`.

**B5b.** When `reporter_inferred_from` is set and the read yields `totals.tests == 0` or raises (`report_error`), add `parse_gap`: "the report format `<kind>` was inferred from the cure row `<id>` and reading it found no tests: set run.reporter in qa-factory/config.json to the format this command writes". The existing status logic is unchanged.

**B6. parse_gap words.**
- Opening: "this command produces no report the factory can read (reporter: {reporter})."
- Then the existing not_executed sentence.
- Then `report_cure(cmd)` when non-empty, else "Make the command write a JUnit XML or TRX report".
- End: "and set run.reporter and run.report_path in qa-factory/config.json so it is read every time."
- `RUN REPORT GAP:` stays.

### Edges

- **E-B-report-1:** a misread never turns into `passed`. A wrong parser yields 0 tests (`not_executed`) or raises (`report_error`), per t-483 B/7 reading `:910-931`, `:1433-1452`. B5b keeps the diagnosis that a misread would otherwise suppress. Invariant: an inferred format that reads nothing is said, never silent.
- **E-B-report-2:** typed runs take `args.reporter` (:2093), so inference reaches untyped runs only. Invariant: a request's declared reporter is never overridden.
- **E-B-report-3, adversarial pins:**

  | command | resolves to | why |
  |---|---|---|
  | `npx jest packages/pytest-bridge` | `pytest` | today's quirk, kept verbatim |
  | `dotnet test` | junit-xml | today |
  | `vstest.console.exe x.dll /logger:junit` | junit-xml | via "junit", step 3 |
  | `ng e2e` | junit-xml, `reporter_inferred_from: "karma"` | a zero-test read adds the B5b `parse_gap`: ng e2e is not karma |
  | `make test` | none | |
  | a pytest command whose path says `karma` | pytest | `row_for :70-73` |

- **E-B-report-4:** a project cure row (B-416) with the same id shadows the package row and feeds step 4. Invariant: the project's word wins, and `reporter_inferred_from` names the row it came from.
- **E-B-report-5:** `parse_gap`'s opening phrase is kept (pinned at `test_run_suite_mine.py:320`), and its presence still means doubt (:478-482).

### Acceptance keys

- K-P1: the E-B-report-3 table.
- K-P2: B5b on a zero-test inferred read and on a raising one.
- K-P3: parse_gap words come from the row, with the generic text when no row matches.

### Tests

- `tests/test_run_suite_reports.py`.
  Mutation: the row fallback placed before `command_formats` → `dotnet test` becomes `trx` → killed here.

### Live proof

A `testproject1-ui` untyped `run_suite` run with `run.report_path` set and no `run.reporter`: the summary carries `reporter_inferred_from`, and the report is read, or the B5b gap is named.

### DoD (B-report)

- `python -B ai-packages/qa-factory/scripts/tests/test_run_suite_reports.py`
- `python -B ai-packages/qa-factory/scripts/tests/test_run_suite_mine.py`
- `python -B ai-packages/qa-factory/scripts/run_suite.py --selftest`
- the importers of `run_suite` listed under B-run
- `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`
- `python -B ai-packages/qa-factory/scripts/tests/test_audit_rules.py`

CI runs the full selftest and install_smoke.

### Manifest (B-report)

given: this spec (B-report, F-6); `factory-rules.md`; `plans/builder-rules.md`; `docs/tasks/specs/t-475-b-414-b-416-stand-gap-card-and-report.md` N5 (:552-566, project cure rows); `scripts/run_suite.py` :257-301, :1309-1470, :2085-2096; `scripts/report_cures.py` as landed by B-416; `references/report-cures.json`.

owns:
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\run_suite.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\references\report-cures.json
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_run_suite_reports.py

non-goals: cure rows and `report_cures.py` (B-416); the conductor route (D-0031); B1-B4 sites; in `report-cures.json`, anything but the new top-level key.

handoff: as in Part A.

edges: E-B-report-1…5.

DoD: `python -B ai-packages/qa-factory/scripts/tests/test_run_suite_reports.py` and the rest above.

---

## Part B-deps: dependency files, the D-0023 rehearsal key, `first_test_file`

### Requirements

**B7 `[meaning]` (F-7).** New `references/dependency-files.json`:
- `names`: today's six, plus `setup.py`, `Pipfile`, `Pipfile.lock`, `uv.lock`, `pdm.lock`, `yarn.lock`, `pnpm-lock.yaml`, `npm-shrinkwrap.json`, `pom.xml`, `build.gradle`, `build.gradle.kts`, `settings.gradle`, `settings.gradle.kts`, `gradle.lockfile`, `go.mod`, `go.sum`, `Cargo.toml`, `Cargo.lock`, `Gemfile`, `Gemfile.lock`, `composer.json`, `composer.lock`, `global.json`, `Directory.Build.props`, `Directory.Packages.props`, `packages.lock.json`;
- `patterns` (top level of the cwd only): `*.csproj`, `*.fsproj`, `*.vbproj`;
- `report_config`: `pytest.ini`, `tox.ini`, `setup.cfg`, `conftest.py`, `jest.config.js`, `jest.config.ts`, `vitest.config.ts`, `vitest.config.js`, `karma.conf.js`, `playwright.config.ts`, `playwright.config.js`, `.runsettings`.

Code changes:
- New `execution_request.dependency_files(run_cwd, cfg) -> (paths, note)` covers the data plus `run.dependency_files` from config. It is used at :2281-2282.
- `_DEPENDENCY_FILES` stays exported as the data's names.
- `_DEPENDENCY_FLOOR` is today's six. It is used on unreadable data, with a note; data ⊇ floor is pinned.
- `gate_preflight._rehearsal_key` uses `dependency_files(cwd, cfg)` plus `report_config` instead of `_DEPENDENCY_FILES | REPORTER_CONFIG_FILES`.

**B8.** `gate_preflight.first_test_file` matches when `is_test_for("name", name)`. It keeps `REPORTER_SKIP_DIRS` and the sort order. The card at :1981-1989 is unchanged (offered to B-414).

### Edges

- **E-D-1, conflicting requirements:** the fingerprint (axis 7) against the D-0018 budget. A newly listed file present costs one extra run or rehearsal. Precedent requests keep the precedent's recorded list (:2274-2279). On the reference project, no new name is present (measured), so the key and fingerprints are byte-identical. Invariant: the allowed error is an extra run, never a missed dependency change.
- **E-D-2, temporal:** an old rehearsal row of a Java/JS project no longer matches, so it is rehearsed again and `_record_rehearsal` replaces it (:1870-1872). Invariant: a proof is never reused across a changed report config.
- **E-D-3:** patterns are top-level only. The door is `run.dependency_files`.
- **E-D-4:** unreadable data gives the floor plus a note. Invariant: never fewer files than today.

### Acceptance keys

- K-D-1: the Python fixture's dependency list and rehearsal key equal today's.
- K-D-2: `pom.xml`, `*.csproj` and `jest.config.js` change them.
- K-D-3: `first_test_file` finds `FooTest.java`, `foo_test.go`, `FooTests.cs`, and not `Contest.cs`.

### Tests

- `tests/test_execution_request.py`: K-D-1, K-D-2.
- `tests/test_reporter_rehearsal.py` (around :874): the key.
  Mutation: drop `report_config` → killed here.
- `tests/test_gate_preflight.py`: K-D-3.

### Live proof

A Test Project 1 comparison story: gate A REUSES the existing rehearsal row (the key is unchanged), and S6 reuses S5 runs as before.

### DoD (B-deps)

Run from the repository root:
- `python -B ai-packages/qa-factory/scripts/tests/test_execution_request.py`
- `python -B ai-packages/qa-factory/scripts/tests/test_reporter_rehearsal.py`
- `python -B ai-packages/qa-factory/scripts/tests/test_gate_preflight.py`

Importers of `execution_request|gate_preflight`, once at the end: test_run_suite_mine, test_red_sandbox_reports, test_red_sandbox_probe, test_probe_by_code, test_execution_pipeline, test_s5_precheck, test_run_budget, test_probe_binding, test_execution_scheduler, test_onboarding_probe, test_probe_debt, test_proof_level, test_launch_check, test_run_block_producer, test_words_doors, test_stand_gaps, test_story_run_stand_identity, test_story_run_gate_repair, test_story_run_delivery_b, test_bug_confirmation, test_handed_to_person, test_gate_question_form, test_gate_brief_and_retro, test_profile_gate, test_question_branches.

Then:
- `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`
- `python -B ai-packages/qa-factory/scripts/tests/test_audit_rules.py`

CI runs the full selftest and install_smoke.

### Manifest (B-deps)

given: this spec (B-deps, F-7); `factory-rules.md`; `plans/builder-rules.md`; DECISIONS D-0023; `scripts/execution_request.py` :500-540, :2255-2300; `scripts/gate_preflight.py` :467-534, :1855-1990 (as landed by B-416/B-408/B-414); `scripts/test_files.py` (Part A); the measured file list of the reference harness (Why (c)).

owns:
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\execution_request.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\gate_preflight.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\references\dependency-files.json
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_execution_request.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_reporter_rehearsal.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_gate_preflight.py

non-goals: `_reporter_card` and the :1983 card text (B-414); `http_get` (B-408); the reporter rehearsal flow (B-416); `_conftest_chain` (analog 2); `templates/config.json`.

handoff: as in Part A, plus "Needed from integration": `templates/config.json` `run.dependency_files: []` with a note.

edges: E-D-1…4.

DoD: `python -B ai-packages/qa-factory/scripts/tests/test_execution_request.py` and the rest above.

---

## Part C: validators and judges over a role's words and test code

### Requirements

**C1 `[meaning]` (F-8).**
- Delete `STAGE_DONE_RE`.
- New `stage_notes(path, text)`. For each whole-token stage id `S0`…`S9` in the authored text (code blocks and the appendix cut out, as at :1642-1650) whose `pipeline.json` status is `pending` or `halted`, emit one deduplicated line: "test-report.md names S8 while pipeline.json has it 'pending': if a sentence calls it finished, correct it; whether it does is yours to judge."
- `running` and `done` stages are never named.
- The lines are not errors. They go out through the valid-write hint block (:2381-2383) and `--check --verbose`.

**C2 `[meaning]`.** `check_self_fixes` reads `detectors.json` `assert_lines`:
- `(?i)assert`
- `\bexpect\s*\(`
- `(?i)\bshould\b`
- `\bverify\s*\(`
- `\brequire\.\w+\(`
- `\bt\.(Error|Errorf|Fatal|Fatalf|Fail|FailNow)\(`

Delete `ASSERT_LINE_RE`. An unreadable key means no check plus one `ORACLE_NOTES` line.

**C3 `[meaning]`.** `is_test_code` = under tests_root and `is_test_for("test_code", path, cfg, root=project_root())`. Delete `TEST_CODE_SUFFIXES`.

**C4 `[meaning]`.** `judge_code` reads its shapes from `detectors.json`:
- `sleep`: today's three plus `\bsleep\(\s*\d`, `wait_for_timeout\(`, `waitForTimeout\(`, `Task\.Delay\(`, `Thread\.Sleep\(`, `time\.Sleep\(`, `\bcy\.wait\(\s*\d`;
- `locator` (new): today's alternatives plus `\bBy\.`, `getBy[A-Z]\w*\(`, `\bcy\.get\(`, `\$\$?\(\s*['"]`;
- `negative_code` (new): today's alternatives plus `assertThrows\(`, `\.toThrow\(`, `Assert\.Throws`.

An unreadable key means ask that dimension. `render` says "M non-Python file(s) skipped (the critic reviews them in full)" instead of "none skipped".

**C5.** `arch_check`:
- `SLEEP_RE`/`LOCATOR_RE` read the same keys.
- The test-body check is `names_a_test(rel) or (v.by == "config" and v.kind == "file")`, i.e. `is_test_for("test_body", …)`.
- `_collect` uses `is_code_file`.

**C6 `[meaning]`.** `s5_precheck`:
- Returns `unchecked: [{case, file, checks: ["Then assertions", "contradictions", "smells"]}]`.
- The note says "… the code did not check its Then assertions, contradictions or smells — the code critic reads them".
- The OK line names the unchecked files and claims nothing for them.
- `agents/qa-code-critic.md:26-27`: "…already checked (…), except the files it lists under not checked by code: read those in full." The added bytes are paid for by removing redundant text; ≤ 9000 bytes.

### Edges

- **E-C1, FR-12:** the note fires on the presence of a stage id in any wording (a French sentence naming S8 included). Invariant: no phrase list over a role's words.
- **E-C2:** the refusal becomes a note. The `delivery_ready` head is still refused on contradiction (:1686-1689). Invariant: the verdict a person reads stays code-checked.
- **E-C3 (C/10):** the running stage (normally S8 while the report is written) is excluded. Invariant: the note does not fire on every report.
- **E-C4, self_fixes may only over-refuse.** Adversarial inputs that must stay refused when dropped: `Assert.Equal(200, r.Status)`, `assertEquals(a, b)`, `x.Should().Be(3)`, `expect(page).toHaveURL(u)`, `require.NoError(t, err)`, `assert r.status_code == 200`.
- **E-C5:** more judge questions mean fewer `clean` results. Invariant: nothing becomes `clean` through a missed shape.
- **E-C6 (F-9):** `asyncio.sleep(1)` becomes an arch_check finding.
- **E-C7:** `assert_lines` is shared with B-373. Lead (t-503 L10): the ONE reader is B-373's new stdlib module `scripts/assertion_detectors.py` (`assertion_detectors()`/`assertion_heads()`, reading `references/detectors.json`, no runtime import of `probe_by_code`); `validate_artifacts` imports that module and does not extend `assert_lines` on its own; if Part C lands before B-373 part (c), Part C creates the module with today's `assert_lines` only and B-373 extends it.
- **E-C8:** a Python-only story's precheck output is byte-identical.
- **E-C9 (C/9):** a helper in a project test folder (`kind: "folder"`, its name not a test) is not a test body. Invariant: page objects and helpers get no locator finding for being in a test place.

### Acceptance keys

- K-C1: `test_validators.py:111` flips from a reject to a note, and a `running` stage gives no note.
- K-C2: the E-C4 table.
- K-C3: the judge_code shape table and the "skipped" render.
- K-C4: `unchecked` plus a true OK line, and the critic phrase "not checked by code".
- K-C5: with `tests_root: "qa"`, `qa/helpers/latest.py` is not test code (today it is, by "test" in "latest": the F-3 narrowing, pinned). `qa/tests/LoginTest.java` with `@Ignore` gives the skip_markers error. `qa/tests/helpers/latest.py` is test code (folder `tests`).
- K-C6: E-C9.

### Tests

- `tests/test_validators.py`: K-C1, K-C2, K-C5.
  Mutation: put a phrase list back → the French case kills it.
- `tests/test_judge_code.py`: K-C3.
  Mutation: unreadable → do not ask → killed here.
- `tests/test_s5_precheck.py` (extend :707): K-C4.
- `tests/test_arch_check.py`: Java locator, `Thread.sleep`, `asyncio.sleep`, K-C6.

### Live proof

1. A Test Project 1 comparison story: S5 and S8 behave as before (`stage_compare`).
2. A `testproject1-ui` story through S5: `unchecked` lists the `.spec.ts` files, and the critic digest shows it read them.
3. C4 is closed by code, not proved, until the first shadow run with a judge provider.

### DoD (Part C)

Run from the repository root:
- `python -B ai-packages/qa-factory/scripts/tests/test_validators.py`
- `python -B ai-packages/qa-factory/scripts/tests/test_validate_artifacts_report.py`
- `python -B ai-packages/qa-factory/scripts/tests/test_judge_code.py`
- `python -B ai-packages/qa-factory/scripts/tests/test_s5_precheck.py`
- `python -B ai-packages/qa-factory/scripts/tests/test_arch_check.py`
- `python -B ai-packages/qa-factory/scripts/arch_check.py --selftest`

Importers, once at the end:
- of `validate_artifacts`: test_case_id_form_sites, test_bug_confirmation, test_report_facts, test_handoff_producers, test_audit_rules, test_story_closure, test_ahead_cards, test_stand_gap_remedy, test_stage_clock, test_case_gates;
- of `judge_code|arch_check|s5_precheck`: test_window_record, test_brief_pack, test_blocked_by_env_window, test_manifest_from_tests, test_report_facts, test_handed_to_person, test_handoff, test_obligation_join.

Then:
- `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`

CI runs the full selftest and install_smoke.

### Manifest (Part C)

given: this spec (Consumer table, Part C, F-8/9/10); `factory-rules.md`; `plans/builder-rules.md`; `scripts/validate_artifacts.py` :1460-1515, :1630-1690, :1957-1985, :2133-2185, :2230-2390; `scripts/judge_code.py`, `scripts/arch_check.py` (whole); `scripts/s5_precheck.py` :1-80, :685-800, :1815-1934; `agents/qa-code-critic.md`; `references/detectors.json`; `scripts/test_files.py` (Part A); `tests/test_validators.py:90-120`; `tests/test_s5_precheck.py:700-730`.

owns:
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\validate_artifacts.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\judge_code.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\arch_check.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\s5_precheck.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\references\detectors.json
D:/ws1/yml-text-factory\ai-packages\qa-factory\agents\qa-code-critic.md
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_validators.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_judge_code.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_s5_precheck.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_arch_check.py

non-goals: `probe_by_code.py` (B-373); `UNDERSTANDING_SECTIONS`; the `_is_page_object` suffixes (analog 9); AST checks for other languages.

handoff: as in Part A.

edges: E-C1…E-C9.

DoD: `python -B ai-packages/qa-factory/scripts/tests/test_validators.py` and the rest above.

---

## Part D: money (P18) and the judge's settings

### Requirements

**D1 `[meaning]` (F-11).** New `references/external-agent-calls.json` `forms[]`:
- Each row: `id`, `command_re` (on the lower-cased command), `consumer_re` (one group, on the original), `call_id_prefix`, `invocation_method`, `provider`, `service`, `unknown_consumer_label`.
- **Grammar:** `id` and `call_id_prefix` match `^[a-z0-9][a-z0-9_.-]{0,63}$` (no `:`, `~` or whitespace). The regexes compile, and `consumer_re` has ≥1 group.
- Row 1 = today's testproject1 values VERBATIM.
- **Floor:** the same row lives in code as `_TESTPROJECT1_FLOOR`; data ⊇ floor is pinned.
- **Project extension:** config `cost.external_agent_forms`, same schema, appended. Invalid project rows are skipped and named in `forms_problem`.
- **Keys:**
  - testproject1: `__external__:<hash>:<consumer>:<ts>` (unchanged);
  - other forms: `__external__:<form id>~<hash>:<consumer>:<ts>`;
  - a key with no `~` parses as testproject1 (legacy checkpoints).
- `external_reconciliation(calls, forms_problem="")` adds `recognized_forms` and sets `complete: False` when `forms_problem` is non-empty.
- **Unreadable or invalid package data:** the floor only, plus `complete: False`.

**D2.** `judge.settings` returns `problems: list[str]` naming every coercion in that one function:
- provider outside `none`/`typesafe` (exact match);
- `mode` outside `shadow`/`on` (shadow is used);
- an unreadable `qa-factory/config.json` (type named);
- a `judge` value that is not an object.

Absent config (no project) or an absent `judge` block → no problem. `ask` includes `problems`; when off because of a problem, its `reason` is that problem. `status()` includes `problems`.

### Edges

- **E-D1, temporal:** legacy keys parse as testproject1. Invariant: recapture never duplicates or loses a call (merge by id, unchanged).
- **E-D2:** two agents in one command give two calls; one form matched twice in one tool_use gives one. Invariant: one invocation is one call.
- **E-D3, unreadable data:** the testproject1 floor still records testproject1 calls, and `complete: False`, so `match` is None and the price is a range (P18). Invariant: neither a call nor an unknown is ever lost silently.
- **E-D4, grammar:** a project id with `:`/`~`, or a regex with no group, is skipped, named, and gives `complete: False`. Invariant: the project's word can only add forms and can never corrupt a key.
- **E-D5:** the judge never turns on for a provider the code cannot call; an unknown mode stays `shadow` (advisory). Invariant: every coercion is said.

### Acceptance keys

- K-D1: GOLDEN, computed by running the UNCHANGED code before any edit on the `tool-123` fixture (`test_usage_activity.py:120-128`). The literal dict `{external_call_id: "testproject1:<24 hex as measured>", consumer_agent: "jira-assistant", invocation_method: "testproject1 assistants chat", provider: "testproject1", service: "assistants", usage_status: "pending", reason: "Remote usage receipt was not present in the host transcript", observed_at, task: "T"}` is pinned, plus the identity-unavailable label `"Test Project 1 assistant (identity unavailable)"`. The handoff shows the pre-change run's output.
- K-D2: a second fixture form gives a pending call with its prefix, `complete: False`, and both ids in `recognized_forms`.
- K-D3: a legacy key parses.
- K-D4: unreadable data → the floor recognizes testproject1 and `complete: False`.
- K-D5: the four `problems` and their absence for none/absent.

### Tests

- `tests/test_usage_activity.py`: K-D1–K-D4.
  Mutation: the parser ignores `~` → killed here.
- `tests/test_judge.py`: K-D5.

### Live proof

1. A Test Project 1 comparison story: the same `external_call_id` as the golden; recapture is idempotent; `recognized_forms` is in the cost file.
2. `judge.py status` on a copy with `provider: "openai"` and `mode: "of"` prints both problems.

A second agent CLI waits for a live project.

### DoD (Part D)

Run from the repository root:
- `python -B ai-packages/qa-factory/scripts/tests/test_usage_activity.py`
- `python -B ai-packages/qa-factory/scripts/tests/test_judge.py`
- `python -B ai-packages/qa-factory/scripts/judge.py --selftest`

Importers, once at the end:
- of `cost_capture`: test_scout_reliability, test_cost_capture_tail, test_cost_capture_recapture, test_cost_capture_lock_scope, test_codex_host, test_dashboard_task_price, test_cost_capture_subagent_usage, test_cost_capture_sticky_attribution, test_dashboard_task_binding, test_factory_dashboard_task_view, test_retro_task_price, test_task_price, test_retro_orchestrator_driver, test_rate_precedence, test_friction, test_storage_visibility, test_cost_capture_ownership, test_cost_capture_nonfactory_summary;
- of `judge`: test_s5_precheck, test_oracle_provenance, test_judge_results, test_judge_form, test_judge_run, test_judge_discovery, test_judge_code.

Then:
- `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`
- `python -B ai-packages/qa-factory/scripts/tests/test_audit_rules.py`

CI runs the full selftest and install_smoke.

### Manifest (Part D)

given: this spec (Part D, F-11/12/13); `factory-rules.md`; `plans/builder-rules.md`; `scripts/cost_capture.py` :780-990, :1160-1240, :1400-1455; `scripts/judge.py` (whole, as landed by B-408); `tests/test_usage_activity.py:60-144`; `tests/test_judge.py:70-130`.

owns:
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\cost_capture.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\judge.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\references\external-agent-calls.json
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_usage_activity.py
D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_judge.py

non-goals: `_post`/HTTP (B-408); printing `recognized_forms` (analog 12); readiness (F-13); `templates/config.json`.

handoff: as in Part A, plus "Needed from integration": `templates/config.json` `cost.external_agent_forms: []` with a note.

edges: E-D1…E-D5.

DoD: `python -B ai-packages/qa-factory/scripts/tests/test_usage_activity.py` and the rest above.

---

## FR walk

- **A:** FR-1/FR-57: the repo-map reason, `unchecked`, the judge `problems` and the node-id notes each name what is wrong and the move. FR-4: stage notes are informed. FR-2: the critic is named for unchecked files.
- **B:** text shown to a person is unchanged; the parse_gap sentences are runner/role text.
- **C:** FR-12 restored; FR-13 (eight lists into data; runner recognizers still code, E-B-run-4); FR-38 (the builder confirms where the automator's text names "a weakened assert is not a fix"); FR-47.
- **D:** FR-17 (one recognizer per problem); FR-41/FR-59 (`collected_ids`, reconciliation, judge coercions); FR-18 unchanged.
- **E:** FR-37: every path in a note is the path read.
- **F:** FR-28 (K-D1 golden, K-D2/K-D4), FR-41, P18.
- **G:** FR-29 (regexes as JSON strings, no heredoc), FR-30 (ASCII; the French test sentence is ASCII), FR-52, FR-54.

## Siblings (SIBLING_MAP)

- **Axis 3:** three new reference files ship.
- **Axis 4:** `factory-rules-debt.md:130` is reworded; B-278 is part-closed.
- **Axis 5 rows:**
  - "Gate rows" (`collected_ids`): `test_gate_registry` is in B-run.
  - "Required lists ↔ null outcomes": `test_null_outcomes` is in A.
  - "Report proof ↔ gate A reporter step": B-deps E-D-2.
  - "Guard's person-granted passes": A1 keeps grants/guard untouched (E-A13); the guard row in the consumer table.
  - "Report-row readers": B-report only infers the format.
- **Axis 6:** cost readers do not depend on the provider.
- **Axis 7:** E-D-1; analog 2.

**Queued backlog rows (written at integration):**
- **NEW (t-479 seam line):** "Two runner tables in `references/launch-causes.json` (`collect_forms` keyed by `tool` with code recognizers `_SHAPES`; `run_forms` keyed by `id` with data recognizers through `hooklib.direct_test_form`) → one reader of runner identity; `not_executed_exits`/`node_ids` (B-407) and the selection form (B-373) move onto it." This also closes E-B-run-4 and is the route for F-14.
- F-13: judge problems surfaced by readiness/doctor.

**Analogs (reported, not widened):**
1. `git commit -am` and other commits with no path token never reach `rule_pathspec`; `git -C dir commit` is not recognized.
2. `_conftest_chain` is Python-only (axis 7, the unsafe direction).
3. `ERROR_HEAD_PREFIXES` / `node_ids.HEAD_PREFIXES` are pytest-shaped.
4. Walk-skip lists: `gate_preflight.REPORTER_SKIP_DIRS` and `arch_check` still do not read `skip_dirs`. A-map does.
5. `detectors.json` `dead_code` is unread.
6. Handoff `.lock` misses `package-lock.json`/`pnpm-lock.yaml`/`go.sum` (extra rows).
7. The `gate_preflight :1983` card claim → B-414.
8. `node_ids.is_pytest` duplicates `execution_request.is_pytest_command`.
9. The `_is_page_object` suffixes.
10. `repo_map` `UTIL_DIR_NAMES`/`STOPWORDS`.
11. `red_sandbox.is_generated`.
12. Nobody prints `recognized_forms`.
13. The inventory conflation and the brief's run_suite claim (Why).

## Parallel nodes (seams)

- **B-415 → A.** B-415 defines `test_locations.is_test_path(path, cfg, *, base=None, root=None)` with the six-key verdict (`test`, `by`, `source`, `kind`, `where`, `reason`; `source` from B-415's revision) and `markers()`. Part A then edits `test_locations.py` additively (A1: extras, `name_marker`, camel in step 4) and adds list entries plus `test-harness` to the markers file. The guard rule is B-415's: `source == "test_locations"`.
- **B-399 → B-405/406 → A** on `stage_guard.py`. Shared signatures are `command_shapes(cmd, cfg=None, event=None)` and `_is_commit_shape(cmd, cfg=None, event=None)`; `command_shape` = the first of `command_shapes`. A writes inside `_is_commit_shape`, plus the `git commit` clause of `needs_stage_guard`, plus `check_command` passing `event`. On `handoff_check.py`, B-405 writes `_requirements_of`; A writes `_production_files`.
- **B-404 → B-run.** B-run writes `launch_check.runner_row` and the two `collect_forms` fields, and updates key 1 of B-404's `test_run_forms.py`. B-404 does not touch `launch_check.py`.
- **B-416 → B-report** (`report-cures.json` additive `command_formats`; `row_for` with the project root feeds step 4) and **→ B-deps** (`gate_preflight.py`, `test_reporter_rehearsal.py`).
- **B-run → B-report** on `run_suite.py`.
- **B-408, B-414 → B-deps** (`gate_preflight.py`). **B-408 → D** (`judge.py`).
- **B-373 ↔ C** on `detectors.json` `assert_lines`: one reader, `scripts/assertion_detectors.py` (E-C7; whoever lands first creates it, the second extends it). The `select_one` offer to B-373 is declined (t-464 L9: resolution is by frames, not by selection). The selection form goes onto the queued unified runner table.

## Forks (returned, not decided)

F-1 to F-13 are decided (see Lead decisions carried). New:

- **F-14. Runner rows beyond pytest for exit-code facts** (consequence of B/5).
  - (a) Queue: a mocha/jest/dotnet row lands only with a measured exit fact on a real project (PROJECT.md 6a) and a recognizer, via the queued unified runner table.
  - (b) Add a mocha row now: a `_SHAPES["mocha"]` recognizer and `not_executed_exits: []`, from documentation, not measurement.
  - Recommend (a). (b) encodes an unmeasured fact into a stand signal.
- **F-15. The non-commit-segment narrowing** (E-A4, second item).
  - (a) Accept it: only commit/add segments are scanned. That is t-479's segment rule.
  - (b) Also scan every segment's tokens when a commit segment exists.
  - Recommend (a). (b) re-admits E-A10's class through compound commands, and the bare-commit hole is analog 1's own row.

## Small choices closed

- **Camel inside step 4**, through the shared `name_marker`. Reason in Changes, row A/1.
- **Markers extras:** a malformed extra never sets `markers()`'s `problem`.
- **Segmenter:** quote-aware `shlex` with `punctuation_chars`. Fallback on `ValueError` is today-like.
- **Handoff base resolution:** by `implementation.repo` name through config; ambiguous means unknown.
- **`_LEGACY_NOT_EXECUTED` naming:** today's set is kept under that name as the declared default.
- **The `test_run_forms.py` grant:** limited to key 1's pin.
- **`judge.settings`:** `problems` is a list. Absent config is not a problem.
- **Form-id grammar:** `^[a-z0-9][a-z0-9_.-]{0,63}$`.
- **A-map skip dirs:** reads B-415's `skip_dirs` instead of extending a code list.
- **Unchanged from the accepted draft:** `node_ids.py` untouched; 124/127 in code; the testproject1 id format unchanged; stage notes deduplicated; patterns top-level only; the parse_gap opening phrase kept.

## Trail

**Read for this revision:**
- `docs/tasks/specs/reviews/t-483-critic-b-415-b-407.md` (whole)
- `docs/tasks/specs/t-468-b-407-single-tuning-rest.md:1-40` (Lead decisions; the rest is my own accepted text)
- `docs/tasks/specs/t-476-b-415-test-locations.md:1-229` (Lead decisions, R1-R11, edges 1-2) plus Grep for the seam lines (:18, :20, :89-118, :152, :159, :185, :447-455)
- `docs/tasks/specs/t-467-b-405-b-406-adapter-forms.md` (Grep: :21, :25, :67, :152-159, :228, :373, :409)
- `docs/tasks/specs/t-466-b-404-run-forms.md` (Grep: :9, :56-61, :96-126, :217-232, :309, :350-352)
- `docs/tasks/specs/t-475-b-414-b-416-stand-gap-card-and-report.md:550-569, 712-741`
- `scripts/stage_guard.py:813-828, 955-972, 1179-1182`
- `scripts/run_suite.py:2085-2096` (Grep `reporter`)
- `scripts/tests/test_launch_check.py:574-585`
- `scripts/tests/test_protected_test_path.py:270-283`
- Grep `impl-diff.txt` across `scripts/` (the diff is per repository: `diff_pass.py:171`; `implementation.repo` in the context manifest: `test_judge_discovery.py:115`)

**Searches with controls:**
- Glob `docs/tasks/specs/reviews/*` → t-478, t-480, t-483 only. The t-479 report is absent; Grep `t-479` in `logs/routing-log.jsonl` → only the `delegated` line :1261.
- Glob `docs/tasks/specs/*` lists t-466/467/475/476.
- Per-module importer greps over `scripts/tests` (`run_suite` 18, `execution_request` 18, `gate_preflight` 14, `launch_check|stand_health` 4, `validate_artifacts` 13, `cost_capture` 20). Each is a non-empty result, so the call is its own control.

The original reading trail of the accepted draft stands (`t-468` Trail section).

**Relevant absolute paths:**
- D:/ws1/yml-text-factory\docs\tasks\specs\t-468-b-407-single-tuning-rest.md
- D:/ws1/yml-text-factory\docs\tasks\specs\reviews\t-483-critic-b-415-b-407.md
- D:/ws1/yml-text-factory\docs\tasks\specs\t-476-b-415-test-locations.md
- D:/ws1/yml-text-factory\docs\tasks\specs\t-467-b-405-b-406-adapter-forms.md
- D:/ws1/yml-text-factory\docs\tasks\specs\t-466-b-404-run-forms.md
- D:/ws1/yml-text-factory\docs\tasks\specs\t-475-b-414-b-416-stand-gap-card-and-report.md
