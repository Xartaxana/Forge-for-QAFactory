# t-2046 - census of language / framework exceptions in the package

Scout report. Read-only on code. Source tree: `D:/ws1/wt-fbfix\ai-packages\qa-factory\` (scripts/, references/detectors.json, agents/, references/*.md) and `D:/ws1/wt-fbfix\docs\SIBLING_MAP.md`. Line numbers are those of that worktree on 2026-11-06.

## 0. Shape of the finding

The package has ONE intended road for "other languages": `references/detectors.json` `assertion_probes` (csharp, java, typescript rows), read by `assertion_detectors.py` and `test_source.py`. Everything else about a test file was written first for Python (AST / `ast.parse` / `.py` suffix / pytest node ids) and the other road was bolted on later or left as a disclosed gap. Two kinds of exception follow:

- **A. Disclosed gap** - the code says "not a Python file, not checked" (a note / `unchecked[]` row / `incomplete`). The role (code critic) is told to read the file whole. The weaker road is visible, but it is still a weaker road: a TypeScript story gets less code checking than a Python story.
- **B. Silent asymmetry** - the other road is weaker and nothing says so, or the Python road is the weaker one (as in `--at`).

Not listed as exceptions (closed variety in data with one contract on every language, AR-1): the `sleep`/`locator`/`locator_words`/`negative_code`/`assert_lines`/`plan_antipatterns` keys of detectors.json (language-neutral regex rows); `test_files.CODE_EXTENSION_FLOOR` (test_files.py:86, data-like floor, read through `is_code_file`); `project_inventory._SWEEP_FLOOR` (project_inventory.py:152); `user_path_failures` `languages` (data table, lines 78/96/180); `hooklib` `_FALLBACK_PYTEST` (hooklib.py:898, a declared safe default under a data row, FR-59).

Out of scope (the factory's OWN python, not a project test): `audit_factory.py:1743`, `gate_registry.py:397,574`, `refusal_registry.py:833`, `stage_joints.py:82,149,244`, `null_outcomes.py:232`, `copy_detector.py:216,279` as a parser of the *project's* Python is in row 11 below, `story_run.py:1095`, `stage_guard.py:1869` (recognises a factory script run), `guard_pre_tool.py` pytest lines (guard recognises a launch by the `hooklib` data row).

## 1. Table (36 sites, grouped by mechanism, every line kept)

Rating (my reading, not a decision): **H** a story on the other language loses a gate or a proof the Python story has; **M** it loses evidence or convenience, role compensates; **L** cosmetic / over-refusal only. "Owner" = who bears the consequence: **code** = a code-owned datum or gate; **role** = the role's judgment fills the gap.

### M1. S5 exit gate (`s5_precheck.py`) reads only Python test files

| mechanism | file : function : line | what the other language does not get | consequence for a story in TS/Java/C# | owner | rate |
|---|---|---|---|---|---|
| Then-assertion binding, contradiction, smell, run-mapping, relative-oracle checks all run on `read_python` ASTs | `s5_precheck.py` : `detector` main loop : 4079-4084 (`resolved.suffix != ".py"` -> `unchecked.append`), 4098-4100 (relative oracle); constant `UNCHECKED_CHECKS` 72-74; docstring 45 | `check_bindings`, `check_run_mapping`, `check_open_oracle_asserted`, `check_smells`, `check_relative_oracle` (none runs: `files` stays empty, `targets` empty) | the S5 exit gate passes a TS test with zero Then-binding verification; disclosed as `unchecked[]` rows ("Then assertions, contradictions, smells") and a note; code critic told to read it whole | code gate skipped, role judges | H |
| `extends` target must be `.py` | `s5_precheck.py` : `_fixture_function_problem` : 2310-2311 | existence check of the named extended function | a TS `extends:` is refused "is not a Python file" (a refusal, not a note: the opposite direction, over-refuses) | code | M |
| helper methods beside a helper | `s5_precheck.py` : sibling-methods reader : 2583-2586 | method list next to a helper | not read, note | code | L |
| conftest-chain copies / copy advice | `s5_precheck.py` : 2654-2667 | copy detection in a non-`.py` conftest-like file | "copies in it were not checked - the code critic reads it whole" | role | M |
| `extends` in the plan | `s5_plan.py` : extends check : 536-537 | the `extends` fixture check | not-a-Python-file note only | code | L |
| `extends` in the brief | `brief_pack.py` : `extends` : 1922-1923 | body extraction of the extended test into the brief | note "not checked" | role | M |
| helper/test bodies parsed for the brief | `brief_pack.py` : `read` : 1849-1851 | `ast.parse`; a non-Python file is a "cannot be parsed" note, not a language note (indistinguishable from a broken Python file) | brief lacks helper lines for TS tests | role | L |

### M2. Judge and repo map

| mechanism | file : function : line | what the other language does not get | consequence | owner | rate |
|---|---|---|---|---|---|
| judge of test code | `judge_code.py` : window loop : 167, 177-181, 350 | any judgment state (asserts-match-Then, owns-its-data, dead code, hardcoded credentials) | "N non-Python file(s) skipped (the critic reviews them in full)"; the judged-state layer that lets a Python window be accepted cheaper does not exist for TS | role (critic reads whole) | H |
| repo map names/fixtures | `repo_map.py` : `_is_python` 183-184; use 282-286; `LANGUAGE_NOTE` 61, `UTIL_LANGUAGE_NOTE` 62 | test names, classes, fixtures, members | the brief's "how a test is written here" map lists the file with `tests: []`; automator navigates by hand | role | M |

### M3. Live check (`probe_by_code.py`) - Python road vs table road

| mechanism | file : function : line | Python gets / other gets | consequence | owner | rate |
|---|---|---|---|---|---|
| **Python has no `--at`**; always breaks the first assert (`first_assert`) | `probe_by_code.py` : `_refuse_flags` 2915-2919 refuses `--at` for a Python test; `first_assert` 291; `plan_mutation` 556 | non-Python: `--at <line>` picks among declarations / assertions (`locate_target` 976-1020) | the known one. A Python test whose first assert is not the Then's cannot be pointed at the right assert; the probe breaks the wrong statement (off-target note only, `target_fact` 3030, `_off_target_note` 3048) | code | H |
| mutation kinds | `probe_by_code.py` : `MUTATIONS` 166; `_refuse_flags` 2910-2914 | Python: `invert` and `expected`; table languages: `invert` only ("--mutation expected is Python's") | the `expected` mutation (value flipped) has no TS/Java/C# road | code | M |
| oracle following into helpers/fixtures | `probe_by_code.py` : `find_oracle` 362-400, `_resolve_oracle` 2934-2948, flag `--oracle` 3268-3269 | Python: one hop out into helper, fixture, conftest chain, imported modules; table languages: `_detector_oracle` only the oracle named by hand | a TS test whose assert lives in a helper cannot be probed unless the role names the oracle | code | M |
| `alternative` mutation (reading B) | `probe_by_code.py` : `_refuse_flags` 2907-2909; `load_model` 3374 (`function` hint must end `.py`); `_alt_row` 3974-3981; `_alternative_gap_record` 3755 | Python: a real model-based run; other language: only a `gap` record, never a run | reading-B proof exists for Python stories only | code | H |
| selector / node parsing | `probe_by_code.py` : `parse_node` 234-235 | `.py` goes AST path, everything else `parse_detector_node` 830 (no isolation of class chain) | two parse roads for one `--test` | code | L |
| restore of the mutated file | `probe_by_code.py` : `put_back` 2012, 2017 | `.py`: original mtime restored and `__pycache__` dropped; other: mtime = now (needed for builds) | deliberate (comment in code at 2000-2010) - recorded as classified, not a defect; listed because the asymmetry is real | code | L |
| debt replay of a probe | `probe_debt.py` : 202-204 | replays the oracle only by AST | "code replays only the oracle it can locate by AST; a helper of another language is named again with --oracle" | role | M |
| `ast.parse` on mutation checks | `probe_by_code.py` : 336, 370, 551, 586, 3444, 3543-3544, 3569, 3596, 3800 | Python-path internals (the mutation is validated by re-parsing); the table road validates by its lexer | consistent with the two-road design; no extra consequence beyond rows above | code | - |
| `assert_spans` for alternative | `probe_by_code.py` : 3432-3445 | spans of the Then's assert only for Python | alternative gap for others (above) | code | - |
| failure site of a runner report | `reporters.py` : `assertion_site` 340-350 | non-pytest `junit-xml` without a `frames` grammar gives `site_unread` (B-337); pytest and `trx`/frames-rows get a location | a language row without `frames` -> every red probe is `incomplete` | code (data row missing) | M |
| product-level probe node selection | `red_sandbox.py` : `_case_nodes` 1254-1260; docstring 51; also 49-52 | only `.py::` nodes pinned as `--node-id`; any other node launches the WHOLE case | red_sandbox probe on TS runs the full case (cost, plus noise) | code | M |

### M4. Execution: the pytest road

| mechanism | file : function : line | other runner does not get | consequence | owner | rate |
|---|---|---|---|---|---|
| node ids verified by a collect BEFORE the run | `run_suite.py` : `_verify_node_ids` 1637-1645 (`not pytest` -> `_not_verified`); `node_ids.py` : `check_request` 738-741 ("not a pytest command: node ids were not verified"); 973-975 `node_id_mismatch` gate pytest only | a wrong TS title/id is not caught before launch | the run launches, zero rows bind, failure shows later as "not executed" instead of one early refusal; the code says "not verified" in notes | code | H |
| `--mine` bare file -> test functions | `execution_request.py` : `functions_naming_case` 1327-1360 (`ast.parse`, Python only) used at 3409-3410 | bare-file `--mine` finds no function in a TS file | refusal 3422-3428 "no test mentions the case in a marker, comment or docstring" for a file that does mention it; the role must pass `--node-id` | code | M |
| node -> junit row name | `execution_request.py` : `node_report_id` 813 (`file[:-3] if endswith(".py")`) | classname spelling for non-`.py` file left as written | only pytest ids are respelled; others rely on the contract row `report_match` | code | L |
| collect memo (skip repeat collects) | `execution_request.py` : `_memo_closure` 2942-2968 (`.py` AST and import follow 2965-2967), `_config_blind` 2883, `_tree_blind_spot` | a collect for non-pytest is never remembered | cost only (~100 s per collect per story, per the code comment 3402-3440) | code | L |
| selector contract verified | `execution_request.py` : 3596-3601 | pytest: "a node id as an argument IS pytest's contract"; others ask `profile_contract.selectors_verified` | same outcome but with a different gate. **closed: FV1-18 N4, data key `selection_by_node_id`, commit 274b57f (branch wip/fv118-n4); narrowing: `py.test` still answers through `is_pytest_command` -- finding F-1 `plans/piles/live-run-fvf/findings/20261113-py-test-dva-chitatelya-odnogo-voprosa-vybor-po-id-uzla.md` (node FV2-3)** | code | L |
| quiet / log flags / `--junitxml` | `run_suite.py` : 1947-1962 (`is_pytest` adds `-q`, `--log-cli-level=WARNING`); also 2107 (`reporter != "pytest"` -> `parse_gap`) | non-pytest logs are not shortened | the 50-64 KB log that the code comment says poisons an agent's context is only guarded for pytest; `report_cures.py` 25-70 supplies a per-runner "cure" row for others (data) | code | M |
| timeout setting | `run_suite.py` : 1188 (`row.get("tool") == "pytest"`) -> `pytest_timeout_setting`; `execution_request.py` timeout reader near 780 | pytest ini timeout is read; no other runner's per-test timeout | a hard kill is classified `hard_kill` only where the ini is read | code | L |
| memo of case marker lines | `execution_request.py` : 1334 (see row above) | - | - | - | - |
| execution fingerprint | `execution_fingerprint.py` : `_parse` 339 | `executable_sha` of test files only for `.py` (see M5) | see M5 | code | M |

### M5. "Cosmetic" classifier and code sha (re-review cost)

| mechanism | file : function : line | other language does not get | consequence | owner | rate |
|---|---|---|---|---|---|
| comment-only change keeps a receipt | `diff_scope.py` : `executable_sha` 241 (`not .py` -> `""`), `classify_texts` ~284 ("cannot be classified (not Python source that tokenizes)"); tokens via Python `tokenize`; `LINE_COMMENT`/`BLOCK_MARKS` are multi-language but only used for the per-line `is_prose` | non-`.py` file: any change counts as `code` | a comment-only fix to a TS test re-runs the full rubric, detectors, arch-check and the suite - the exact cost D-0017 removed for Python; error direction is the safe one (costs a run, never ships unproven) | code | M |
| code sha on rows | `proof_level.py` : `code_sha` 565-575, `current_code_sha` 579 | `""` for non-Python (raw rule only) | receipts of TS tests go stale on any byte change | code | M |
| diff_scope `ast.parse` of a decorator span | `diff_scope.py` : 168 | case-marker decorator is cosmetic only for pytest markers (`MARKERS_FILE` is data but only `@pytest.mark.<name>` shape is read, line 40-60) | a TS case tag edit is code | code | L |
| novelty measure | `test_novelty.py` : 460-461 (`WORDS_ROW_NOT_MEASURABLE`), 542, 759; `manifest_from_tests.py` : note at 1374 | "novelty is measured for Python tests only; not measured for this file" | the extend-vs-new and duplicate checks the novelty number feeds are unmeasured for TS; code critic judges | role | M |

### M6. Manifest writing (`manifest_from_tests.py`)

| mechanism | file : function : line | other language does not get | consequence | owner | rate |
|---|---|---|---|---|---|
| Then bindings / assertion refs | `manifest_from_tests.py` : `language_rows` 1327-1375 (`assertion_refs: []` at ~1365; note 1373 "Then bindings are the author's: this language has no marker") | a `then_bindings` row per Then from markers/AST | for a non-Python file the manifest has `assertion_refs: []`; `s5_precheck` (M1) then cannot check it; the automator writes bindings by hand through `manifest_put` | role | H |
| helper counting | `manifest_from_tests.py` : 1061-1063, 1068 | helper units for the "extend vs new" count | note "its helpers were not counted - the code critic reads it whole" | role | M |
| id verification `--collect` | `manifest_from_tests.py` : `collect_refusal` 1748-1753 | collected ids | refusal; ids are "read from the source and not verified against the runner" | code | M |
| parser | `manifest_from_tests.py` : `TestFile` 305-315 (`does not parse as Python`) and dispatch 1612-1613 (`.py` -> `TestFile`, others -> `LanguageFile` via `test_source`) | the two readers produce different row shapes (`trace_binding` carries `assertion_refs`) | see above | code | - |

### M7. Other readers

| mechanism | file : function : line | other language does not get | consequence | owner | rate |
|---|---|---|---|---|---|
| radius evidence | `blast_radius.py` : `_parse` 317-326, `_symbols_from_tree` 329-, `_symbols_of` 411 (`not a.python` -> module symbol only, gap `""`), `_file_sites` 507 (`DEF_RE` only for `.py`) | changed-symbol list and same-name definition sites | a TS product change is searched by its module name only; the gap string is `""` on that road (line 411), so `unmeasured` is NOT raised for the missed symbols - the docstring at 17 says "another language gets its module-level name searched". Unclear whether silent: classify **B (silent)** pending a critic read | role (P27: the radius is the strategist's) | M |
| import-direction layers | `arch_check.py` : `IMPORT_RE` 46 (Python `import`/`from ... import`), `_module_to_rel` 93-98 (`.py`, `/__init__.py`), loop 129-139; status 107 `"imports": "checked"` whenever `layers` is configured | no TS/Java/C# import is ever matched | **silent**: status says `checked`, finds nothing - an FR-41 shape (an unknown reported as a fact) | code | H |
| sleep in comments | `arch_check.py` : 117 (`startswith("#")` only) | a `// sleep(...)` comment in TS is a finding | over-refusal on TS (the opposite direction) | code | L |
| page-object file names | `arch_check.py` : `_is_page_object` 78 (`_page.py`, `.page.ts`, `.page.js` hard-coded) | Java/C#/Kotlin page objects (`LoginPage.java`) | closed variety in code (AR-1) | code | L |
| reporter test globs floor | `gate_preflight.py` : `REPORTER_TEST_GLOBS` 589-591 | floor only; data row `test-path-markers.json` wins when readable | classified as a declared floor (FR-59), not an exception | - | - |
| manual UI walker harness | `manual_capture.py` : `harness_argv` 2296-2325 (finds the first profile whose command contains a `pytest` token and builds `<head> python` from it; else `harness_none` refusal) | a project whose tests are TS (`npx playwright test`) or Java has no profile that fits | the P26 manual-case walker cannot run through the project's own environment; the refusal names the "install Playwright for the factory's own Python" door | code | H |
| role reference | `references/test-code-patterns.md` : 23, 140, 148; `references/code-review-rubric.md` : 49; `references/artifact-contract-run.md` : 105 | rules written in `pytest.param`, `pytest.skip`, `pytest.raises` | the roles' charters carry Python spelling as the rule; a TS automator translates. This is a role's judgment, but the text is the only guide it has | role | L |
| onboarding probe | `onboarding_probe.py` 3 pytest hits, `launch_check.py` 661-670 (`_SHAPES = {"pytest": _is_pytest}`, only runner-shaped code, rest in `collect_forms` data) | - | classified: data-driven by design (launch_check.py:21) | - | - |

## 2. Controls (positive controls of the same form as each negative / counting statement)

- `grep -rniE 'endswith\(["\x27]\.(py|ts|js)'` over `scripts/` found `probe_by_code.py:234` and 11 more; same form, same flags, used for every "only `.py` is accepted" statement.
- `ast.parse` search found 70+ hits including `probe_by_code.py:336`; confirms the search form works on this tree.
- `.spec.ts`: found `gate_preflight.py:589` and `red_sandbox.py:1097` (docstring); there is NO `.spec.ts` branch in any consumer except test-file globs and `assertion_probes.typescript.suffixes`, which is data. (A negative claim; control: same grep form found those two.)
- `typescript` / `\.tsx?\b`: hits only in `sizing.py`, `diff_pass.py` (self-test strings), `user_path_failures.py` (data), `project_inventory.py` (floor list), `test_files.py` (floor). No code branch named for TypeScript exists; TS is reached only through the `assertion_probes` row. (Negative; control: same grep found `project_inventory.py:152`.)
- `playwright`: no code branch outside `manual_capture.py` and `node_ids.py` (pytest-playwright id respelling, data note) and a no-op `run_suite.teardown_playwright` (377-379).
- Site count: M1 7 + M2 2 + M3 11 + M4 8 + M5 4 + M6 4 + M7 7 = 43 table rows; 36 distinct code locations (rows that repeat one site are marked "-"). Over 40 rows, so grouped by mechanism and every line kept.
- Not searched: `skills/qa-story/phases/*.md`, `hooks/`, `tools/`, `scripts/tests/` (out of scope except as evidence). Unclassifiable sites: `blast_radius.py:411` (silent or disclosed gap - see row), `brief_pack.py:1849` (language note vs parse note).

## 3. Ranking (rating, not a decision)

1. `s5_precheck.py` unchecked road (M1) together with `manifest_from_tests.py` `assertion_refs: []` (M6): one pair, the S5 exit gate effectively does not exist for a non-Python story (disclosed, role-compensated).
2. `arch_check.py` import-direction (M7): silent "checked" with nothing matched - FR-41 shape.
3. `probe_by_code.py` Python has no `--at` (M3): the known one; the mirror asymmetries (no `expected`, no helper-following, no `alternative` run) hurt the other languages.
4. `execution_request.py` / `run_suite.py` node-id verification before launch, bare-file `--mine`, collect memo (M4).
5. `manual_capture.py` harness requires a pytest profile (M7).
6. `diff_scope.py` / `proof_level.py` cosmetic classifier (M5).
7. `judge_code.py`, `repo_map.py`, `blast_radius.py` (M2, M7).

## 4. Does `docs/SIBLING_MAP.md` have a language-parity axis?

No. Checked `D:/ws1/wt-fbfix\docs\SIBLING_MAP.md` (32 axes, headings at lines 24-554; identical file exists at `D:/ws1/yml-text-factory\docs\SIBLING_MAP.md`): grep `language|python|parity|pytest` gives 11 lines; none is an axis heading. The nearest text is the row "The assertion-probe table (B-373, D-0028, t-531)" inside Axis 5 (line 148): "a language is a data row ... A new language is a data row, never a branch in a consumer". That row covers only the probe table's consumers (`probe_by_code`, `validate_artifacts`, `reporters.assertion_site`, `red_sandbox`) and does not list `s5_precheck`, `manifest_from_tests`, `judge_code`, `repo_map`, `blast_radius`, `arch_check`, `diff_scope`, `proof_level`, `execution_request`, `run_suite`, `node_ids`, `manual_capture`, `brief_pack`, `test_novelty`, `probe_debt`. Axis 9 (line 226, "is this a test file") is the other neighbor: one leaf `test_files.is_test_for` for "is a test", with no counterpart for "how is it read". A language-parity axis (one row per mechanism above, with the "other road" named) would be a new axis per rule 9 of CLAUDE.md; none exists, so a fix today has no map to walk (class-wide completeness, rule 9, cannot be checked by the critic against the map).
