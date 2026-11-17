# Scout digest t-1200: variety axes 1-6 (what holds each axis today)

Verbatim hand-back of the scout, extracted from its transcript by the coordinator (scouts cannot write files). Frozen: not edited after extraction.

digest: v1 t-1200

Scope: axes 1-6, parts A-E, read-only, no opinions on the axis list. The verdict rows (a1V..a6V) are facts about where each axis is held, not recommendations. Row ids are `a<axis><part><n>`; D rows carry the outcome in the gist as (i) refuses/halts, (ii) silent default, (iii) reports and leaves the move. Outside this table: `docs/tasks/specs/20261117-universality-variety-map-brief.md` was read in full (R1); `architecture.md` section A (R2) says each Trail-named table has one reader.

## Objects

| id | kind | gist | paths | status | owner | links | ev |
|---|---|---|---|---|---|---|---|
| a1A1 | data | dependency-files.json lists manifests of Python, JS, Java, Go, Rust, Ruby, PHP, .NET; reader execution_request::dependency_table | ai-packages/qa-factory/references/dependency-files.json:3-10 | held | — | a1D3 | R9,R36 |
| a1A2 | data | project-dependencies.json: locks poetry/uv/pdm, install commands poetry/uv/pdm only; reader dependency_drift::load_table, install_command | ai-packages/qa-factory/references/project-dependencies.json:3-12 | held | — | a1D2 | R8,G19 |
| a1A3 | data | test-path-markers.json code_extensions covers 20 language extensions; skip_dirs covers node_modules, target, obj, vendor | ai-packages/qa-factory/references/test-path-markers.json:8-11 | held | — | a3A3 | R10 |
| a1A4 | data | build-identity-methods.json ladder sources, oci_label, build_sha_file; command and person_confirms are person-owned; reader runtime_probe | ai-packages/qa-factory/references/build-identity-methods.json:5-14 | held | — | — | R12,G20 |
| a1B1 | config | keys app_root, protected_app_paths, code_repos, implementation_repos, profiles (runtime, package_manager), profiles.commands.install, run.dependency_files | ai-packages/qa-factory/references/config-keys.json:9-61 | held | — | — | R3,G4 |
| a1B2 | interview | topic 1 (repos, paths, default branch), 2b (runtime, package manager), 5 (command that brings environment to lock) | ai-packages/qa-factory/skills/qa-onboarding/phases/p2-interview.md:83-106 | held | — | a1B1 | R18,R19 |
| a1C1 | role | phase 1 "Application stack" row: entry points, local run, manifests; nothing language-specific; automator "written the project's way" | ai-packages/qa-factory/skills/qa-onboarding/phases/p1-discovery.md:42 | held | — | — | R20,R21 |
| a1D1 | hardcoded | project_env::resolve: Python venv/poetry/.venv sources; any other stack gets source `inherited`, reported in the returned dict (iii) | ai-packages/qa-factory/scripts/project_env.py:38-40 | hardcoded | — | — | R34,R35 |
| a1D2 | hardcoded | dependency_drift reads Poetry locks only; quote "the answer for them is unknown, never in_sync or differs" (iii) | ai-packages/qa-factory/references/project-dependencies.json:2 | hardcoded | — | a1A2 | R8,G19 |
| a1D3 | hardcoded | execution_request::_DEPENDENCY_FLOOR names six Python/JS files; used only when the table is unreadable, named once in `problem` (iii) | ai-packages/qa-factory/scripts/execution_request.py:580-583 | hardcoded | — | a1A1 | R36 |
| a1D4 | hardcoded | execution_request::_pytest_ini_name assumes pytest.ini/tox.ini/setup.cfg/pyproject; "None when there is none" (iii) | ai-packages/qa-factory/scripts/execution_request.py:659-695 | hardcoded | — | a3D4 | R37 |
| a1E1 | fixture | probe-languages (CalcTest.java, CalcTests.cs, sum.test.ts), test_story_run_monorepo.py (subfolder project), evals/fixtures/sample-pytest-repo | ai-packages/qa-factory/scripts/tests/fixtures/probe-languages | proven | — | — | G16,G17,G18 |
| a1E2 | pilot | stack not stated in MEASUREMENTS.md; node_ids.py:8 names pytest-playwright for TP1-15045; runs named TP1-13797, TP1-13958, TP1-15045, TP1-12586, TP2-2553 | plans/MEASUREMENTS.md:38-45 | partial | — | — | R42,R43,G21,G13 |
| a1V | verdict | MIXED: manifests, extensions, locks, build identity are tables; roots and install command are config; Python env selection and Poetry-only lock are hard-coded | — | verdict | — | a1A1,a1B1,a1D1 | R9,R3,R34 |
| a2A1 | data | surfaces.json rows web, api, cli, desktop, android, ios (capability, hands, selectors, devices); reader surfaces.py::rows, declared_surfaces | ai-packages/qa-factory/references/surfaces.json:23-58 | held | — | — | R5,R13 |
| a2A2 | data | surfaces.json not_surfaces unit/event/manual; words.unknown_word sends an unknown surface word to a person | ai-packages/qa-factory/references/surfaces.json:5-9 | held | — | a2D2 | R5 |
| a2A3 | data | no table row for database, queue, GraphQL, gRPC; zero hits in references/*.json | ai-packages/qa-factory/references | absent | — | — | Z2,C2 |
| a2A4 | prose | Kafka/gRPC/ORM appear only as pattern advice in test-code-patterns.md, not as a surface | ai-packages/qa-factory/references/test-code-patterns.md:83-91 | partial | — | a2A3 | G25 |
| a2B1 | config | profiles[].capabilities, supported_capabilities, adapter_capabilities; environments[].surface, driver, device, app (note history line 391) | ai-packages/qa-factory/references/config-keys.json:46-53 | held | — | — | R3,R4 |
| a2B2 | interview | phase 1 row "Mobile surface" (names are examples, not a list); topic 2 mobile batch; topic 2b | ai-packages/qa-factory/skills/qa-onboarding/phases/p2-interview.md:218-235 | held | — | a2B1 | R18,R20 |
| a2C1 | role | automator technique "The lowest rung that observes the behaviour. API or component first"; no surface named | ai-packages/qa-factory/agents/qa-automator.md:48 | held | — | — | R21 |
| a2C2 | role | surfaces.json words for cli/desktop: "those cases go to a person" (person as executor) | ai-packages/qa-factory/references/surfaces.json:26-33 | held | — | a2D1 | R5 |
| a2D1 | hardcoded | surfaces.py:24 AGENT_HANDS=("browser","http","driver"); comment "any other row's cases go to a person" (iii) | ai-packages/qa-factory/scripts/surfaces.py:24 | hardcoded | — | a2C2 | G5,R13 |
| a2D2 | default | declared_surfaces: unknown capability word gets hands "person" and unknown_word text, never silence (iii) | ai-packages/qa-factory/scripts/surfaces.py:126-129 | default | — | a2A2 | R13 |
| a2D3 | hardcoded | gate_preflight::_probe_sign_in defaults to PlaywrightBackend (browser); missing Playwright gives a door text (iii) | ai-packages/qa-factory/scripts/gate_preflight.py:2805 | hardcoded | — | — | R40,G5 |
| a2D4 | hardcoded | env_probe: `if not surfaces.profiles_driven_by(cfg, "browser"): return None` skips deriving a UI address silently (ii) | ai-packages/qa-factory/scripts/env_probe.py:553 | hardcoded | — | — | R41 |
| a2E1 | fixture | test_mobile_road.py, test_device_stand.py (names only); surfaces.json:3 says no row has run on a device, iOS is general knowledge | ai-packages/qa-factory/scripts/tests/test_mobile_road.py | partial | — | — | G15b,R5 |
| a2E2 | pilot | web and API pilots only (TP1-15045 pytest-playwright); android row follows tooling read in t-524-ep1-41a-report.md; no mobile, DB, queue, CLI run named | plans/MEASUREMENTS.md:40 | partial | — | — | R5,G21,Z3 |
| a2V | verdict | MIXED: web, api, android, ios are table rows plus stand config; cli, desktop route to a person; database, queue, GraphQL, gRPC not addressed | — | verdict | — | a2A1,a2A3 | R5,Z2 |
| a3A1 | data | launch-causes.json collect_forms: about 24 runner rows (pytest, dotnet test, jest, vitest, mocha, playwright, go, cargo, mvn, gradle, rspec, phpunit); reader launch_check::runner_row | ai-packages/qa-factory/references/launch-causes.json:18-52 | held | — | a3D3 | G2,R14 |
| a3A2 | data | detectors.json assertion_probes rows for csharp, java, typescript, python; read via assertion_detectors.py, test_source.read_file | ai-packages/qa-factory/references/detectors.json:85-326 | held | — | a3D1 | G3,R17 |
| a3A3 | data | test-path-markers.json dir/stem/camel-suffix markers; suggestion and fallback only, never a permission; reader test_files.py | ai-packages/qa-factory/references/test-path-markers.json:2-9 | held | — | — | R10 |
| a3A4 | data | case_forms.py DEFAULT_FORM "TC-{nnn}" always recognised after configured templates; reader case_forms::forms | ai-packages/qa-factory/scripts/case_forms.py:34 | held | — | — | G11 |
| a3A5 | data | BDD: no gherkin/cucumber/specflow/reqnroll anywhere in package outside tests, changelog.d, evals | ai-packages/qa-factory | absent | — | a3C3 | Z1,C1,G18 |
| a3B1 | config | tests_root, test_locations, cases_root, case_id_form, test_command_templates, profiles (commands, selectors, reporter) | ai-packages/qa-factory/references/config-keys.json:19-56 | held | — | — | R3,R4 |
| a3B2 | interview | topics 1b (case store), 1c (test places), 2b (selectors, reporter, commands), 5 (parallel_windows question about whole-folder builds) | ai-packages/qa-factory/skills/qa-onboarding/phases/p2-interview.md:107-139 | held | — | a3B1 | R18,R19,G15 |
| a3C1 | role | phase 1 "Rule: read files, not names": framework confirmed by reading a real test file, not a manifest name | ai-packages/qa-factory/skills/qa-onboarding/phases/p1-discovery.md:23-28 | held | — | — | R20 |
| a3C2 | role | automator Outcome "written the project's way"; fixtures "the project's way"; code critic reviews against "the project framework" | ai-packages/qa-factory/agents/qa-automator.md:15 | held | — | — | R21,G13 |
| a3C3 | role | case designer writes Given-When-Then cases as the case form; no framework binding | ai-packages/qa-factory/agents/qa-case-designer.md:3 | held | — | a3A5 | G17 |
| a3D1 | default | manifest_from_tests: non-Python file with no table row is a note with a door; NO_READER_DOOR "write this file's rows yourself" (iii) | ai-packages/qa-factory/scripts/manifest_from_tests.py:344 | hardcoded | — | a3A2 | R17 |
| a3D2 | hardcoded | probe_by_code.py:251 `if not file.endswith(".py"): return parse_detector_node(...)`; line 2805 non-pytest refusal "Nothing was changed" with door (i) | ai-packages/qa-factory/scripts/probe_by_code.py:251 | hardcoded | — | — | R15,R16 |
| a3D3 | hardcoded | node_ids::missing_sentence says "is not collected by pytest"; runner_form with no row returns (None, note), collect all-or-nothing (iii) | ai-packages/qa-factory/scripts/node_ids.py:755-793 | hardcoded | — | a3A1 | R14 |
| a3D4 | hardcoded | execution_request::pytest_rootdir walk over pytest ini files; non-pytest project gets None (iii) | ai-packages/qa-factory/scripts/execution_request.py:683-695 | hardcoded | — | a1D4 | R37 |
| a3D5 | default | case_forms: unreadable configured form is ignored, problems() reports, TC-{nnn} still applies (iii) | ai-packages/qa-factory/scripts/case_forms.py:20 | default | — | a3A4 | G11 |
| a3E1 | fixture | sample-pytest-repo, probe-languages, local1-playwright, local1-manifest (add-to-cart.spec.ts), n5-hop (page-object .ts), case-id-form-13877, pytest-timeout (jest-junit.xml) | ai-packages/qa-factory/scripts/tests/fixtures | proven | — | — | G16,G17,G18 |
| a3E2 | pilot | TP1-13877 (id form `TP1-13877_TC_001`, architecture.md:59); TP1-15045 (pytest-playwright); no JUnit/NUnit/Appium project run named in MEASUREMENTS.md | ai-packages/qa-factory/design/architecture.md:59 | partial | — | — | R2,Z3 |
| a3V | verdict | MIXED: runners, languages, markers are tables; roots, id form, commands are config; pytest paths hard-coded; BDD not addressed | — | verdict | — | a3A1,a3B1,a3D1,a3A5 | G2,R3,R17,Z1 |
| a4A1 | data | side-realities.json realities real/absent/substituted, default product real; reference-kinds.json is_change true for merge_request and pull_request | ai-packages/qa-factory/references/side-realities.json:2-5 | held | — | — | R46,R11 |
| a4B1 | config | code_repos, implementation_repos, app_root (code present?), knowledge rows product.sides, environments.sides, environments.reference_for | ai-packages/qa-factory/references/config-keys.json:706-710 | held | — | — | G4,R3 |
| a4B2 | interview | topic 1 "no local checkout is a legitimate answer"; 1b no case library is "a real answer"; 1c "We have no tests records nothing" | ai-packages/qa-factory/skills/qa-onboarding/phases/p2-interview.md:101-129 | held | — | — | R18 |
| a4C1 | role | S0 conductor question s0.no_change, four doors change, current code, ungrounded, not built yet | ai-packages/qa-factory/scripts/driver_s0.py:934-971 | held | — | a4D1 | R24 |
| a4C2 | role | scout: "Stop only when the data is absent"; side "not built yet is no halt: ground it on the requirements" | ai-packages/qa-factory/agents/qa-scout.md:86-87 | held | — | — | R22 |
| a4C3 | role | requirements tester: every requirement checkable or an open_questions record; claims from diff stay claims; `before_ref: reference:<item>` | ai-packages/qa-factory/agents/qa-requirements-tester.md:24-26 | held | — | — | R23 |
| a4D1 | hardcoded | s0_no_change_entry asks only for a LOCAL story; quote "a real ticket with no flags goes the old road" (iii) | ai-packages/qa-factory/scripts/driver_s0.py:939 | hardcoded | — | a4C1 | R24 |
| a4D2 | hardcoded | s0_no_change_entry: option "current code" offered only `if repos` (code_repos non-empty) (iii) | ai-packages/qa-factory/scripts/driver_s0.py:947-954 | hardcoded | — | — | R24 |
| a4D3 | hardcoded | readiness::check_app_repo: app_root "." alone proves nothing; no code gives NOT_CONFIGURED or MISSING owned by user (iii) | ai-packages/qa-factory/scripts/readiness.py:534-564 | hardcoded | — | — | R25 |
| a4E1 | fixture | after-checks, artifacts-good (impl-diff.txt), stories/local-1-0108, local1-manifest, local1-playwright; no fixture found named for "reference system" | ai-packages/qa-factory/scripts/tests/fixtures | partial | — | — | G16,G17 |
| a4E2 | pilot | MR-grounded runs TP2-2553 (MR !64), MR !668, pilot 13958 (MR !664); local-story runs not named in MEASUREMENTS.md | plans/MEASUREMENTS.md:38-43 | partial | — | — | R43 |
| a4V | verdict | MIXED: code present or absent is config plus a conductor question; requirements quality is role judgment; reference system is registry rows; local-only entry hard-coded | — | verdict | — | a4B1,a4C1,a4D1 | R3,R24 |
| a5A1 | data | adapter-forms.json ticket.kinds jira, file, github, gitlab, ado (key regex, mentions), local, fallback_kind jira; reader adapter_forms.py | ai-packages/qa-factory/references/adapter-forms.json:4-18 | held | — | a5D3 | R7,R29 |
| a5A2 | data | requirement-source-kinds.json kinds tracker(adapter), wiki(role), repository(grep), file(grep), other(role); unknown kind routes to role | ai-packages/qa-factory/references/requirement-source-kinds.json:4-10 | held | — | — | R6 |
| a5A3 | data | reference-kinds.json link classes ticket, merge_request, gitlab_issue, pull_request, confluence, figma; unmatched is `url`; reader ticket_light.py | ai-packages/qa-factory/references/reference-kinds.json:4-37 | held | — | — | R11,G24 |
| a5A4 | data | jira-fields.json (Jira field table), read by ticket_light.py; Jira-only table | ai-packages/qa-factory/scripts/ticket_light.py:33 | held | — | a5D4 | G24 |
| a5B1 | config | adapters.ticket (name, method, command, mcp_tool, invoke, direct_api, project_keys, key_pattern), requirements_sources, strategy_documents | ai-packages/qa-factory/references/config-keys.json:96-111 | held | — | — | R3,R4,G4 |
| a5B2 | interview | topic 7 tickets (read route direct API only, verified before believed), topic 10 source of truth for requirements, phase 1 rows | ai-packages/qa-factory/skills/qa-onboarding/phases/p2-interview.md:334-396 | held | — | — | R19,R20 |
| a5C1 | role | scout Outcome "Every source the requirements live in is found and judged"; "Relevance by content ... never by its title or type" | ai-packages/qa-factory/agents/qa-scout.md:16 | held | — | — | R22 |
| a5C2 | role | readiness `_role_route` (SS1-15): factory holds no client for tracker, the role reads by recorded route, status unknown, route "role" | ai-packages/qa-factory/scripts/readiness.py:354-359 | held | — | a5D4 | R26 |
| a5D1 | hardcoded | ticket_adapter.py:184 COMMAND_ADAPTERS=("jira","ado","gitlab","github"); else fail(EXIT_NOT_CONFIGURED, "unknown ticket adapter ...") (i) | ai-packages/qa-factory/scripts/ticket_adapter.py:1725-1726 | hardcoded | — | a5A1 | G8,R27 |
| a5D2 | hardcoded | `if kind != "jira": fail(EXIT_NOT_CONFIGURED, "source refresh requires a Jira ticket adapter")` (i) | ai-packages/qa-factory/scripts/ticket_adapter.py:2972 | hardcoded | — | — | R47 |
| a5D3 | default | adapter_forms::key_form: unknown tracker kind takes jira form, marked "a guess" with Problem TRACKER_KIND_GUESSED; key_refused never refuses a guess (iii) | ai-packages/qa-factory/scripts/adapter_forms.py:383-394 | default | — | a5A1 | R29 |
| a5D4 | hardcoded | readiness.py:333 `name.lower() == "jira" and entry.get("direct_api")`; ticket_adapter.py:788 non-Jira returns True, role route (iii) | ai-packages/qa-factory/scripts/readiness.py:333 | hardcoded | — | a5C2 | R26,R28 |
| a5D5 | hardcoded | readiness.py:78 BUILTIN_TICKET_ADAPTERS={"file"}, twin of the table; other names go to method inference, no halt (iii) | ai-packages/qa-factory/scripts/readiness.py:340 | hardcoded | — | a5D1 | R26,G8 |
| a5E1 | fixture | evals/fixtures/tickets/QA-1.md, QA-2.md (file adapter); test_adapter_forms.py (named in architecture.md:51) | ai-packages/qa-factory/evals/fixtures/tickets | partial | — | — | R2 |
| a5E2 | pilot | every named run is Jira ("story = Jira ticket", MEASUREMENTS.md:5); no Azure, YouTrack, Notion, GitHub Issues run named | plans/MEASUREMENTS.md:5 | partial | — | — | R42,Z3,C3 |
| a5V | verdict | MIXED: tracker kinds, source kinds, link kinds are tables; tracker access is config; unlisted trackers read by role; direct client and refresh Jira-only | — | verdict | — | a5A1,a5B1,a5C2,a5D2 | R7,R3,R26,R47 |
| a6A1 | data | adapter-forms.json vcs.kinds gitlab (glab mr create) and github (gh pr create, hub pull-request); aliases glab, gh; project adds via adapters.vcs.delivery_commands | ai-packages/qa-factory/references/adapter-forms.json:19-32 | held | — | — | R7 |
| a6A2 | data | glab-auth.json wording table for glab auth status, read by vcs_evidence.py (GitLab only) | ai-packages/qa-factory/scripts/vcs_evidence.py:272-358 | held | — | a6D3 | G22 |
| a6B1 | config | external_writes (bugs markdown or jira; cases markdown, xray, testrail, zephyr; channels.<name>), adapters.vcs {name, status, method}, git_conventions | ai-packages/qa-factory/references/config-keys.json:101-190 | held | — | — | R4,G4 |
| a6B2 | interview | topic 7 VCS host and how reached, 8 external-writes channels ("markdown is first-class"), 5 git conventions | ai-packages/qa-factory/skills/qa-onboarding/phases/p2-interview.md:300-389 | held | — | — | R19 |
| a6C1 | role | S8/S9 delivery prompt carries git_conventions and the VCS adapter record as data; role runs branch, commits, push, Draft MR | ai-packages/qa-factory/scripts/driver_stage_s8s9.py:394-415 | held | — | a6D5 | G23 |
| a6C2 | role | VCS goes through "the connector or CLI named in onboarding"; MR evidence ladder tries every route before a person | ai-packages/qa-factory/references/adapters-read.md:135-137 | held | — | — | R38,R39 |
| a6C3 | role | unknown_channel: NO_ADAPTER, "a person's word still passes it: waiver.py --stage S8 --block 'keep it local'" | ai-packages/qa-factory/scripts/external_writes.py:551-562 | held | — | a6D1 | G7 |
| a6D1 | hardcoded | external_writes.py:993 `elif cases_channel in ("xray", "testrail", "zephyr")`; unknown channel prints NO_ADAPTER, exits EXIT_NO_ADAPTER (i) | ai-packages/qa-factory/scripts/external_writes.py:993 | hardcoded | — | a6C3 | R30,G7 |
| a6D2 | hardcoded | vcs_evidence::readiness `if name not in {"gitlab", "glab"}:` returns status "unknown", owner orchestrator (iii) | ai-packages/qa-factory/scripts/vcs_evidence.py:192 | hardcoded | — | a6A2 | R31 |
| a6D3 | hardcoded | vcs_evidence.py docstring "Read-only GitLab authentication and complete, revision-pinned MR collection"; reads via `glab api` | ai-packages/qa-factory/scripts/vcs_evidence.py:1 | hardcoded | — | — | G22 |
| a6D4 | hardcoded | guard_pre_tool.py:1701 `_TRACKER_CLIS` tuple; 1752 `if exe not in _TRACKER_CLIS: continue` passes an unlisted CLI unless external_writes declares it (ii) | ai-packages/qa-factory/scripts/guard_pre_tool.py:1752 | hardcoded | — | — | R32,R33,G9 |
| a6D5 | hardcoded | S8/S9 delivery prompt assumes a "Draft merge request" for any VCS; no code-free delivery branch seen in the read range | ai-packages/qa-factory/scripts/driver_stage_s8s9.py:411-415 | hardcoded | — | a6C1 | G23 |
| a6E1 | fixture | test_adapter_forms.py (named in architecture.md:51); no GitHub, Bitbucket, ADO, TestRail, Xray run or fixture name found in MEASUREMENTS.md | plans/MEASUREMENTS.md | absent | — | — | R2,Z3,C3 |
| a6E2 | pilot | GitLab MR-based runs (MR !64, !664, !668); Jira as tracker; bug channel actually used in a run not stated | plans/MEASUREMENTS.md:38-43 | partial | — | — | R43 |
| a6V | verdict | MIXED: host and delivery commands are a two-row table plus config; trackers, TMS and unknown hosts are role or person; MR collection is GitLab-only code | — | verdict | — | a6A1,a6B1,a6D1,a6D3 | R7,R4,R30,G22 |
| an1 | analog | AR-1 class: closed variety as code tuple, not table: ticket_adapter.COMMAND_ADAPTERS, readiness.BUILTIN_TICKET_ADAPTERS, guard_pre_tool._TRACKER_CLIS, external_writes channel tuple, surfaces.AGENT_HANDS | ai-packages/qa-factory/scripts/ticket_adapter.py:184 | analog | — | a5D1,a6D4,a6D1,a2D1 | G8,G9,R30,G5 |
| an2 | analog | floors in code duplicating table content (Python/JS six-file floor) beside a table that holds more | ai-packages/qa-factory/scripts/execution_request.py:580 | analog | — | a1D3 | R36 |

## Trail

| tid | op | target | pattern / range | flags | result | control |
|---|---|---|---|---|---|---|
| R1 | read | docs/tasks/specs/20261117-universality-variety-map-brief.md | 1-87 | — | read docs/tasks/specs/20261117-universality-variety-map-brief.md:1-87 | — |
| R2 | read | ai-packages/qa-factory/design/architecture.md | 33-89 | — | read ai-packages/qa-factory/design/architecture.md:33-89 | — |
| R3 | read | ai-packages/qa-factory/references/config-keys.json | 1-125 | — | read ai-packages/qa-factory/references/config-keys.json:1-125 | — |
| R4 | read | ai-packages/qa-factory/references/config-keys.json | 300-435 | — | read ai-packages/qa-factory/references/config-keys.json:300-435 | — |
| R5 | read | ai-packages/qa-factory/references/surfaces.json | 1-60 | — | read ai-packages/qa-factory/references/surfaces.json:1-60 | — |
| R6 | read | ai-packages/qa-factory/references/requirement-source-kinds.json | 1-14 | — | read ai-packages/qa-factory/references/requirement-source-kinds.json:1-14 | — |
| R7 | read | ai-packages/qa-factory/references/adapter-forms.json | 1-33 | — | read ai-packages/qa-factory/references/adapter-forms.json:1-33 | — |
| R8 | read | ai-packages/qa-factory/references/project-dependencies.json | 1-13 | — | read ai-packages/qa-factory/references/project-dependencies.json:1-13 | — |
| R9 | read | ai-packages/qa-factory/references/dependency-files.json | 1-16 | — | read ai-packages/qa-factory/references/dependency-files.json:1-16 | — |
| R10 | read | ai-packages/qa-factory/references/test-path-markers.json | 1-12 | — | read ai-packages/qa-factory/references/test-path-markers.json:1-12 | — |
| R11 | read | ai-packages/qa-factory/references/reference-kinds.json | 1-38 | — | read ai-packages/qa-factory/references/reference-kinds.json:1-38 | — |
| R12 | read | ai-packages/qa-factory/references/build-identity-methods.json | 1-40 | — | read ai-packages/qa-factory/references/build-identity-methods.json:1-40 | — |
| R13 | read | ai-packages/qa-factory/scripts/surfaces.py | 91-150 | — | read ai-packages/qa-factory/scripts/surfaces.py:91-150 | — |
| R14 | read | ai-packages/qa-factory/scripts/node_ids.py | 750-810 | — | read ai-packages/qa-factory/scripts/node_ids.py:750-810 | — |
| R15 | read | ai-packages/qa-factory/scripts/probe_by_code.py | 245-259 | — | read ai-packages/qa-factory/scripts/probe_by_code.py:245-259 | — |
| R16 | read | ai-packages/qa-factory/scripts/probe_by_code.py | 2758-2809 | — | read ai-packages/qa-factory/scripts/probe_by_code.py:2758-2809 | — |
| R17 | read | ai-packages/qa-factory/scripts/manifest_from_tests.py | 344-373 | — | read ai-packages/qa-factory/scripts/manifest_from_tests.py:344-373 | — |
| R18 | read | ai-packages/qa-factory/skills/qa-onboarding/phases/p2-interview.md | 81-240 | — | read ai-packages/qa-factory/skills/qa-onboarding/phases/p2-interview.md:81-240 | — |
| R19 | read | ai-packages/qa-factory/skills/qa-onboarding/phases/p2-interview.md | 300-399 | — | read ai-packages/qa-factory/skills/qa-onboarding/phases/p2-interview.md:300-399 | — |
| R20 | read | ai-packages/qa-factory/skills/qa-onboarding/phases/p1-discovery.md | 23-92 | — | read ai-packages/qa-factory/skills/qa-onboarding/phases/p1-discovery.md:23-92 | — |
| R21 | read | ai-packages/qa-factory/agents/qa-automator.md | 13-87 | — | read ai-packages/qa-factory/agents/qa-automator.md:13-87 | — |
| R22 | read | ai-packages/qa-factory/agents/qa-scout.md | 14-88 | — | read ai-packages/qa-factory/agents/qa-scout.md:14-88 | — |
| R23 | read | ai-packages/qa-factory/agents/qa-requirements-tester.md | 8-35 | — | read ai-packages/qa-factory/agents/qa-requirements-tester.md:8-35 | — |
| R24 | read | ai-packages/qa-factory/scripts/driver_s0.py | 934-972 | — | read ai-packages/qa-factory/scripts/driver_s0.py:934-972 | — |
| R25 | grep | ai-packages/qa-factory/scripts/readiness.py | `def check_app_repo` | content | found 1; ai-packages/qa-factory/scripts/readiness.py:534 | — |
| R26 | read | ai-packages/qa-factory/scripts/readiness.py | 325-364 | — | read ai-packages/qa-factory/scripts/readiness.py:325-364 | — |
| R27 | read | ai-packages/qa-factory/scripts/ticket_adapter.py | 1705-1728 | — | read ai-packages/qa-factory/scripts/ticket_adapter.py:1705-1728 | — |
| R28 | read | ai-packages/qa-factory/scripts/ticket_adapter.py | 783-792 | — | read ai-packages/qa-factory/scripts/ticket_adapter.py:783-792 | — |
| R29 | read | ai-packages/qa-factory/scripts/adapter_forms.py | 380-459 | — | read ai-packages/qa-factory/scripts/adapter_forms.py:380-459 | — |
| R30 | read | ai-packages/qa-factory/scripts/external_writes.py | 965-1023 | — | read ai-packages/qa-factory/scripts/external_writes.py:965-1023 | — |
| R31 | read | ai-packages/qa-factory/scripts/vcs_evidence.py | 180-204 | — | read ai-packages/qa-factory/scripts/vcs_evidence.py:180-204 | — |
| R32 | read | ai-packages/qa-factory/scripts/guard_pre_tool.py | 1695-1724 | — | read ai-packages/qa-factory/scripts/guard_pre_tool.py:1695-1724 | — |
| R33 | read | ai-packages/qa-factory/scripts/guard_pre_tool.py | 1738-1767 | — | read ai-packages/qa-factory/scripts/guard_pre_tool.py:1738-1767 | — |
| R34 | read | ai-packages/qa-factory/scripts/project_env.py | 1-40 | — | read ai-packages/qa-factory/scripts/project_env.py:1-40 | — |
| R35 | read | ai-packages/qa-factory/scripts/project_env.py | 250-289 | — | read ai-packages/qa-factory/scripts/project_env.py:250-289 | — |
| R36 | read | ai-packages/qa-factory/scripts/execution_request.py | 575-604 | — | read ai-packages/qa-factory/scripts/execution_request.py:575-604 | — |
| R37 | read | ai-packages/qa-factory/scripts/execution_request.py | 650-704 | — | read ai-packages/qa-factory/scripts/execution_request.py:650-704 | — |
| R38 | read | ai-packages/qa-factory/references/adapters-read.md | 133-165 | — | read ai-packages/qa-factory/references/adapters-read.md:133-165 | — |
| R39 | read | ai-packages/qa-factory/references/mr-access-routes.md | 1-20 | — | read ai-packages/qa-factory/references/mr-access-routes.md:1-20 | — |
| R40 | read | ai-packages/qa-factory/scripts/gate_preflight.py | 2785-2814 | — | read ai-packages/qa-factory/scripts/gate_preflight.py:2785-2814 | — |
| R41 | read | ai-packages/qa-factory/scripts/env_probe.py | 545-564 | — | read ai-packages/qa-factory/scripts/env_probe.py:545-564 | — |
| R42 | read | plans/MEASUREMENTS.md | 3-8 | — | read plans/MEASUREMENTS.md:3-8 | — |
| R43 | read | plans/MEASUREMENTS.md | 36-48 | — | read plans/MEASUREMENTS.md:36-48 | — |
| R46 | read | ai-packages/qa-factory/references/side-realities.json | 1-40 | — | read ai-packages/qa-factory/references/side-realities.json:1-40 | — |
| R47 | read | ai-packages/qa-factory/scripts/ticket_adapter.py | 2966-2975 | — | read ai-packages/qa-factory/scripts/ticket_adapter.py:2966-2975 | — |
| G2 | grep | ai-packages/qa-factory/references/launch-causes.json | `"(collect_forms\|runners\|id)": ` | content | found 29; ai-packages/qa-factory/references/launch-causes.json:18 | — |
| G3 | grep | ai-packages/qa-factory/references/detectors.json | `^    "[a-z]+": \{\|^      "extensions"` | -i content | found 4; ai-packages/qa-factory/references/detectors.json:86 | — |
| G4 | grep | ai-packages/qa-factory/references/config-keys.json | `^\s{0,6}"[a-z_.\-]+": \{` | content | found 200; ai-packages/qa-factory/references/config-keys.json:4 | — |
| G5 | grep | ai-packages/qa-factory/scripts | `["']web["']\|"browser"\|playwright` | -i content glob=!**/tests/** | found 40; ai-packages/qa-factory/scripts/surfaces.py:24 | — |
| G7 | grep | ai-packages/qa-factory/scripts/external_writes.py | `def unknown_channel` | content | found 1; ai-packages/qa-factory/scripts/external_writes.py:551 | — |
| G8 | grep | ai-packages/qa-factory/scripts | `COMMAND_ADAPTERS\|BUILTIN_TICKET_ADAPTERS` | content glob=!**/tests/** | found 7; ai-packages/qa-factory/scripts/ticket_adapter.py:184 | — |
| G9 | grep | ai-packages/qa-factory/scripts/guard_pre_tool.py | `_TRACKER_CLIS\|_declared_write_commands\(` | content | found 4; ai-packages/qa-factory/scripts/guard_pre_tool.py:1701 | — |
| G11 | grep | ai-packages/qa-factory/scripts/case_forms.py | `TC-\{nnn\}\|DEFAULT\|ignored\|unreadable\|problem` | content | found 14; ai-packages/qa-factory/scripts/case_forms.py:34 | — |
| G13 | grep | ai-packages/qa-factory/agents | `framework\|mobile\|device\|desktop\|native` | -i content | found 5; ai-packages/qa-factory/agents/qa-code-critic.md:10 | — |
| G15 | grep | ai-packages/qa-factory/skills/qa-onboarding/phases/p2-interview.md | `^(\d+[a-z]?)\. \*\*` | content | found 11; ai-packages/qa-factory/skills/qa-onboarding/phases/p2-interview.md:83 | — |
| G15b | glob | ai-packages/qa-factory/scripts/tests | `**/*{appium,android,ios,device,mobile,monorepo,dotnet,trx,junit,gitlab,github,ado,youtrack,bitbucket,testrail}*` | — | found 30; ai-packages/qa-factory/scripts/tests/test_mobile_road.py | — |
| G16 | glob | ai-packages/qa-factory/scripts/tests/fixtures | `**/*.{cs,java,kt,go,csproj,feature,swift,pom.xml}` | — | found 2; ai-packages/qa-factory/scripts/tests/fixtures/probe-languages/CalcTest.java | — |
| G17 | glob | ai-packages/qa-factory/scripts/tests/fixtures | `**/*.{ts,js}` | — | found 10; ai-packages/qa-factory/scripts/tests/fixtures/probe-languages/sum.test.ts | — |
| G18 | grep | ai-packages/qa-factory | `gherkin\|cucumber\|specflow\|reqnroll\|\.feature\b` | -i content glob=!**/{tests,changelog.d,evals}/**; | found 6; ai-packages/qa-factory/scripts/make_fixture_repo.py:30 | — |
| G19 | grep | ai-packages/qa-factory/scripts/dependency_drift.py | `def install_command\|def load_table\|unknown\|no row` | -i content | found 20; ai-packages/qa-factory/scripts/dependency_drift.py:78 | — |
| G20 | grep | ai-packages/qa-factory/scripts/runtime_probe.py | `def runtime_probe\|def pick_checkout\|def probe_build\|ladder` | -i content | found 8; ai-packages/qa-factory/scripts/runtime_probe.py:349 | — |
| G21 | grep | plans/MEASUREMENTS.md | `TP\d-\d+\|TP\d\b\|MyBooks\|green-lantern\|QA-EXAMPLE\|EP1-\d+\|Appium\|\.NET\|dotnet\|Playwright\|GitLab\|GitHub\|Jira\|Azure\|TestRail\|monorepo` | -i content | found 17; plans/MEASUREMENTS.md:5 | — |
| G22 | grep | ai-packages/qa-factory/scripts/vcs_evidence.py | `glab\|gitlab\|github\|bitbucket` | -i content | found 30; ai-packages/qa-factory/scripts/vcs_evidence.py:1 | — |
| G23 | grep | ai-packages/qa-factory/scripts/driver_stage_s8s9.py | `DELIVERY_RULE\|def delivery\|\bDraft\b\|git_conventions\|vcs` | content | found 16; ai-packages/qa-factory/scripts/driver_stage_s8s9.py:394 | — |
| G24 | grep | ai-packages/qa-factory/scripts/ticket_light.py | `jira` | -i content | found 8; ai-packages/qa-factory/scripts/ticket_light.py:33 | — |
| G25 | grep | ai-packages/qa-factory | `graphql\|grpc\|kafka\|rabbitmq\|\bsqs\b\|message queue\|database test\|data pipeline` | -i content glob=!**/{tests,changelog.d,evals}/** | found 5; ai-packages/qa-factory/references/test-code-patterns.md:83 | — |
| C1 | grep | ai-packages/qa-factory | `playwright` | -i content glob=!**/{tests,changelog.d,evals}/** | found 2; ai-packages/qa-factory/.gitignore:12 | — |
| Z1 | grep | ai-packages/qa-factory | `gherkin\|cucumber\|specflow\|reqnroll` | -i content glob=!**/{tests,changelog.d,evals}/** | absent | C1 |
| C2 | grep | ai-packages/qa-factory/references | `playwright` | -i content glob=*.json | found 2; ai-packages/qa-factory/references/config-keys.json:544 | — |
| Z2 | grep | ai-packages/qa-factory/references | `kafka\|rabbitmq\|\bsqs\b\|graphql\|grpc` | -i content glob=*.json | absent | C2 |
| C3 | grep | plans/MEASUREMENTS.md | `jira` | -i content | found 2; plans/MEASUREMENTS.md:5 | — |
| Z3 | grep | plans/MEASUREMENTS.md | `bitbucket\|azure\|testrail\|appium\|dotnet\|kotlin` | -i content | absent | C3 |

## Not done

- Axes 7-13 belong to twin scout t-1201.
- The part D lists are the strongest places I reached, not an exhaustive census of `scripts/`. About 250 files mention pytest; only the schema-bearing readers were read. Probable further spots I did not open: `run_suite.py`, `test_novelty.py`, `red_sandbox.py`, `diff_scope.py`.
- Requirements quality (good, AC only, one line): I found no classifier in code and ran no negative search, so I make no "absent" claim. a4C3 and a4A1 show what exists.
- "Reference system" fixtures: none found by name. The fixture search was by extension and name globs, because the fixtures dir has 1515 files, so a miss there is not proven.
- Broad `Glob **/*` calls timed out (20 s) on the package and its fixtures. I used narrower globs; two reads of the `references` and `handoffs` dir listings were truncated at 100 entries.
- Test bodies not read, per non-goals. a2E1 and a3E1 rest on file and dir names only.
- a6D5: I read `driver_stage_s8s9.py` only around lines 394-415 (via grep), not the whole delivery function. "No code-free delivery branch seen" is limited to that range.
- Whether GitHub MR reading works end to end was not traced. `vcs_evidence.py` is GitLab-only by docstring and `glab` calls; I did not follow how the scout reads a GitHub PR (adapters-read.md and mr-access-routes.md name routes for it).
- `jira-fields.json`, `case-markers.json`, `bug-status-words.json` and `glab-auth.json` were not opened. They were identified only through reader code and the architecture list.
- Environment state (installed tools, live runs) is outside this role's tools; every claim is about FILES.

Analogs (rule 8) are rows an1 and an2 above (code tuples holding closed variety beside a table). The twin pair ticket_adapter.COMMAND_ADAPTERS and readiness.BUILTIN_TICKET_ADAPTERS is already named in `ai-packages/qa-factory/design/architecture.md:51` as queued B-435.
