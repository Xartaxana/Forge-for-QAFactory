# Scout digest t-1201: variety axes 7-13 (what holds each axis today)

Verbatim hand-back of the scout, extracted from its transcript by the coordinator (scouts cannot write files). Frozen: not edited after extraction.

digest: v1 t-1201

Axes 7-13 covered, parts A-E plus a verdict row each. Rows axNX belong to axis N. D rows give the assumed value, behaviour (i refuses/halts, ii silent default, iii reports and leaves the move) and a quoted line.

## Objects

| id | kind | gist | paths | status | owner | links | ev |
|---|---|---|---|---|---|---|---|
| ax7A1 | table | Build-identity methods and ladder (sources, oci_label, build_sha_file, command, person_confirms); reader stand_identity data() via runtime_probe | references/build-identity-methods.json:5-14 | held | — | ax7D1 | r4,r8 |
| ax7A2 | table | surfaces.json: web, api, cli, desktop, android, ios; one reader surfaces.py; unknown surface word is a hint, not a refusal | references/surfaces.json:23-58 | held | — | ax7D6 | r5 |
| ax7A3 | table | login-roads.json holds exactly ONE sign-in form (NextAuth credentials); other shapes are "a finding and a schema change" | references/login-roads.json:5-16 | held-one-row | — | ax7D3 | r6 |
| ax7A4 | analog | Closed set of 7 access kinds lives in a code tuple stand_access.KINDS, not a table (AR-1 shape) | scripts/stand_access.py:73 | code-tuple | — | ax7D3 | g23 |
| ax7B1 | config | environment.access, environments[] (surface, driver, device, app, bring_up, credentials_by_role, safe_to_break), environment.integrations, test_data.* | references/config-keys.json:219 | held | — | — | r2,r3 |
| ax7B2 | onboarding | Topic 2 (stands, access scheme, unauth_status, mobile batch) and topic 3 (test-data lifecycle) | skills/qa-onboarding/phases/p2-interview.md:140-250 | held | — | — | r7 |
| ax7C1 | role | environments.md "ENV_ISSUE ownership" names VPN access as a gate B item; qa-runner.md "Tell the stand from the product" | references/environments.md:76-90 | held | — | — | g52,g53 |
| ax7C2 | role | source-causes.json cause host_unreachable: "DNS or routing failed - this is what a dropped VPN looks like" | references/source-causes.json:6 | held | — | ax7D5 | g7 |
| ax7D1 | hardcoded | Stand build read via docker ps/exec; docker silent gives [], ladder goes on, ends unknown plus a question to the person (iii) | scripts/runtime_probe.py:227 | iii | — | ax7A1 | r8,r9,g58 |
| ax7D2 | hardcoded | APP_ROOT = "/app" is the assumed in-container checkout path unless --app-root is passed (ii) | scripts/runtime_probe.py:246 | ii | — | — | r9 |
| ax7D3 | hardcoded | Unknown access.kind: config_contract refuses (`environment.access.kind must be one of`, i); stand_access probe records not_recorded/not_tried (iii) | scripts/config_contract.py:370 | i+iii | — | ax7A4 | g23,r27 |
| ax7D5 | hardcoded | Remote stand silent: "no network route to {listed} — a corporate VPN that is off is the usual cause." Reports, person moves (iii) | scripts/reachability.py:147 | iii | — | ax7C2 | g1,g24 |
| ax7D6 | hardcoded | Unknown surface word: "those cases go to a person" (iii); ios row host_os ["darwin"] means tool not run elsewhere (iii) | references/surfaces.json:7 | iii | — | ax7A2 | r5,g25 |
| ax7D7 | analog | No SSO-provider or 2FA/TOTP handling in non-test scripts; the 2 hits are in test files only (not opened) | scripts | partial | — | — | g2 |
| ax7E1 | proven | Fixtures: test_mobile_road.py (name only), surface-web-pin, old-generation-project (stand-identity/health/lease), run-12586-stand-config, stories/local-1-0108, local-1-arm-b, cart-1 | scripts/tests/fixtures | found | — | — | g30,g33 |
| ax7E2 | proven | surfaces.json note: android/Appium rows follow a real project's tooling; "no row has run on a device (FR-33)"; ios is general knowledge | references/surfaces.json:3 | found | — | — | r5 |
| ax7E3 | proven | MEASUREMENTS 7.4 (I-86/I-87): Keycloak 302 on stand; runs TP1-13797, TP1-15045, TP2-2553 | plans/MEASUREMENTS.md:214-216 | found | — | — | r32,g29 |
| ax7E4 | absent | No fixture file or folder named *device* under scripts/tests/fixtures | scripts/tests/fixtures | absent | — | — | z10 |
| ax7V | verdict | mixed: build identity and surfaces are tables; access is config plus a code tuple; 2FA/SSO beyond one NextAuth row, per-MR preview are role/person | — | mixed | — | — | r4,r5,r6 |
| ax8A1 | table | host-report-forms.json: claude and codex rows, one reader host_adapter.report_forms; other hosts give no forms | references/host-report-forms.json:4-13 | held-2-hosts | — | ax8D1 | r11 |
| ax8A2 | table | driver-infra.json: child_env remove/prefixes and default_model per host; readers infra_failure.rules and child_env | scripts/infra_failure.py:133 | held | — | ax8D2 | r13,r16 |
| ax8A3 | table | machine-path-markers.json (/Users/, /home/, ~/, Users) and install-paths.json (carried/regenerated/discarded/not_ours) | references/machine-path-markers.json:4-5 | held | — | — | r14,r15 |
| ax8A4 | table | model-rates.json: rates marked "Standard API equivalent estimate, not a Codex subscription charge" | references/model-rates.json:292 | held | — | — | g50 |
| ax8B1 | config | driver.host, driver.child_env.keep ("the project's door for a gateway or an API-key setup"), cost.external_agent_forms, sandbox.install_timeout_s, metrics.hot_cache_min_percent | references/config-keys.json:239 | held | — | — | r2,r13,r29 |
| ax8B2 | onboarding | Question bank topics 1-10 (read in full) asks nothing about OS, shell, host, gateway or subscription; p0/p3/p4 not read | skills/qa-onboarding/phases/p2-interview.md:81-396 | not-asked | — | — | r7 |
| ax8B3 | absent | No config key or table for the host prompt-cache TTL (P25) in references/*.json or scripts/*.py | references | absent | — | — | z7,z8 |
| ax8C1 | role | references/codex-host.md exists (file listing only, content NOT read) | references/codex-host.md | unread | — | — | g69 |
| ax8D1 | hardcoded | Host must be one of HOSTS (claude, codex): `--host / driver.host {self.host!r} is not one of {', '.join(HOSTS)}.` exit 1 (i) | scripts/driver_core.py:590 | i | — | ax8A1 | g17,r16 |
| ax8D2 | hardcoded | Non-codex host default model is literal "sonnet" (ii): `data_model if self.host == "codex" else "sonnet"` | scripts/driver_core.py:551 | ii | — | ax8A2 | r16 |
| ax8D3 | hardcoded | Guards act only when tool_name in ("Bash","PowerShell"); any other shell tool passes unguarded (ii) | scripts/guard_pre_tool.py:315 | ii | — | — | g48 |
| ax8D4 | hardcoded | On os.name nt a .cmd/.bat argv with cmd.exe-unsafe chars: "nothing was launched. Correct the profile's argv" (i, door named) | scripts/project_env.py:567 | i | — | — | g54 |
| ax8D5 | hardcoded | claude -p child loses host proxy/token vars; keep is the way back; factory scripts keep env as is (iii) | scripts/driver_core.py:534 | iii | — | ax8B1 | r12,r13 |
| ax8E1 | proven | MEASUREMENTS 6.2: macOS minimal PATH, backslash guard, POSIX shell=True found by users not CI; 7.5 Codex-desktop (I-90) | plans/MEASUREMENTS.md:159-220 | found | — | — | r31,r32 |
| ax8E2 | proven | Per-OS fixture not searched; only count of platform checks in scripts is known | scripts/tests | not-determined | — | — | g4 |
| ax8V | verdict | mixed: host rows, infra rules, path markers are tables; gateway door is config; OS/shell is two shells in code; no-internet and cache TTL not addressed | — | mixed | — | — | r11,r13,z7 |
| ax9A1 | table | gate-approval-words.json: only "approve" (gates A,B) and "approve as is" (A); one reader gate_brief.approval_words | references/gate-approval-words.json:2-5 | held | — | ax9D1 | r17,r20 |
| ax9A2 | table | question-thresholds.json (count 6, share 1/3), person-owned.json (8 classes of what only a person decides), manual-policy-by-level.json | references/question-thresholds.json:2-3 | held | — | — | r18,r19,r35 |
| ax9B1 | config | dod, manual.walkers, manual.accounts_way, manual.data_way, external_writes, git_conventions, pipeline.stop_after, budget.story_usd, impact_scale | references/config-keys.json:79 | held | — | — | r2,r3,r29 |
| ax9B2 | onboarding | Topic 4 (risk areas, impact map), 5 (git, parallel_windows, walkers), 8 (write channels), 9 (definition of done) | skills/qa-onboarding/phases/p2-interview.md:251-391 | held | — | — | r7,g20 |
| ax9C1 | role | qa-test-strategist.md rule 5: "Regression is found, not run." Witness `## Recommended regression` | agents/qa-test-strategist.md:27 | held | — | ax9D2 | g19 |
| ax9C2 | role | s3.md:171 "Two fields decide who reviews a row" is about impact class, not a named reviewer | skills/qa-story/phases/s3.md:171 | partial | — | — | g62 |
| ax9D1 | hardcoded | Gate pass = first line equals a table word; "The allowed error is not approving (the words go to the conductor)" (iii) | scripts/driver_gates.py:1103 | iii | — | ax9A1 | g16 |
| ax9D2 | hardcoded | FALLBACK_REFS = ("origin/main", "origin/master") assumed; unknown main branch "silences check 8 and nothing else", S8 says so (iii) | scripts/regression_scope.py:36 | iii | — | ax9C1 | r34 |
| ax9D3 | analog | No key or table for who answers or how fast; only 2 unrelated "time zone" hits (product test design) in agents | agents | partial | — | — | g37 |
| ax9E1 | proven | Names: fixtures bench-13797-answers, gate-a-answers/cmp2-test-plan.json; MEASUREMENTS 7.2 regression policy, section 4 questions and conductor | plans/MEASUREMENTS.md:206-208 | found | — | — | r32,g28,g69 |
| ax9V | verdict | mixed: gate words, question thresholds are tables; DoD, walkers, git are config; regression is role; reviewer identity and reply speed not addressed | — | mixed | — | — | r17,r18,g20 |
| ax10A1 | table | jira-fields.json acceptance_headings (3 English entries) merged with config by ticket_adapter.acceptance_headings_for | references/jira-fields.json:18-22 | held | — | — | r36,g8 |
| ax10A2 | table | Approval words (axis 9) are English data; the packet names the word from the table | references/gate-approval-words.json:3 | held | — | ax9A1 | r17 |
| ax10B1 | config | adapters.ticket.direct_api.acceptance_headings lets a project add own-language headings | references/config-keys.json:247 | held | — | ax10A1 | r2 |
| ax10B2 | absent | No language/locale key in templates/config.json or config-keys.json; human-questions.md has no language rule | references/templates/config.json | absent | — | — | z1,z2,z3 |
| ax10B3 | onboarding | Only mention of person language: "The words file keeps the person's own language; the phrases phase 4 writes are English." | skills/qa-onboarding/phases/p2-interview.md:291 | partial | — | — | g9 |
| ax10C1 | role | common-rules.md Language: "Everything you write — files, findings, comments, questions — is in English, regardless of the language of the ticket"; 12 slice copies | references/common-rules.md:148-151 | held | — | — | r22,g10 |
| ax10D1 | hardcoded | Artifact language fixed to English by role text, so a case or bug in another language is outside the contract (ii by design) | references/common-rules.md:150 | ii | — | ax10C1 | r22 |
| ax10D2 | hardcoded | BUG_FORM_SECTIONS = ("## User impact", "## Initial state"); a missing English heading gives errors.append(refusal(...)) (i) | scripts/validate_artifacts.py:504 | i | — | — | g56 |
| ax10D3 | hardcoded | Non-English approval word is not the table word, so the answer goes to the conductor (iii) | scripts/driver_gates.py:1117 | iii | — | ax9D1 | g16,r20 |
| ax10D4 | hardcoded | slug_key: phrase with more non-ascii than ascii letters becomes a hash slug, not a refusal (iii) | scripts/exploration.py:126 | iii | — | — | r21 |
| ax10E1 | absent | Zero Cyrillic characters in the package, fixtures included (FR-30), so no fixture has a Russian ticket or answer | ai-packages/qa-factory | absent | — | — | z9 |
| ax10V | verdict | mixed: acceptance headings table plus config; artifact language fixed English by role; ticket and answer language never proven by a fixture | — | mixed | — | — | r22,z9 |
| ax11A1 | table | sizing weights P0-P3 in config; XS-XL cap table is a code constant in sizing.py (XXL keeps the XL cap) | scripts/sizing.py:601-606 | code-const | — | ax11D1 | g12,r33 |
| ax11B1 | config | sizing.weights, dispatch.ui_window_cases(2)/api_window_cases(4)/parallel_windows(3), execution.s5_window_cases, budget.story_usd, run.stand_wait_s(1800), code_repos, implementation_repos | references/templates/config.json:99-101 | held | — | — | r29,r3 |
| ax11B2 | onboarding | Topic 1 asks for ALL application repos ("are there other repositories — a UI, services"); topic 5 asks parallel_windows | skills/qa-onboarding/phases/p2-interview.md:83-106 | held | — | — | r7 |
| ax11C1 | role | sizing.py XXL text to the person: "Your word tests it as one story; or name the functions to leave out" | scripts/sizing.py:616 | held | — | — | g12 |
| ax11D1 | hardcoded | Size above XL (28) is labeled XXL, cap stays 28; "a recommendation, never a block" (iii) | scripts/sizing.py:947 | iii | — | ax11A1 | g12,r33 |
| ax11D2 | hardcoded | Several repos for one profile: Refusal ("this project names N implementation repositories") with door "pass --checkout" (i with door) | scripts/runtime_probe.py:380 | i | — | — | r10 |
| ax11D3 | hardcoded | run_suite --timeout default=1800 s; kill gives exit 124, log kept, reported as the factory's own run limit (iii) | scripts/run_suite.py:2764 | iii | — | — | g18 |
| ax11D4 | hardcoded | sandbox.install_timeout_s 540 chosen below the host role Bash cap "600 s" (host limit assumed, key overridable) | references/templates/config.json:130 | ii | — | — | r29 |
| ax11D5 | hardcoded | Branch word naming no repo: all configured repos asked; on 0 or 2 different ids sha stays null, "Never a refusal" (iii) | scripts/driver_s0.py:1934 | iii | — | — | g61 |
| ax11E1 | proven | Fixtures: sizing-12586, sizing-14857, sizing-15045 (+weighted) goldens; test_blast_radius.py (name); two-repo cmp2 cited in runtime_probe docstring | scripts/tests/fixtures | found | — | — | r10,g31 |
| ax11E2 | proven | MEASUREMENTS 1.4 TP1-15045 S5 12.5 h, 16 dispatches; 7.3 size weights; MR !668, pilot 13958 | plans/MEASUREMENTS.md:40 | found | — | — | r30 |
| ax11V | verdict | mixed: weights and windows are config, cap table is code, multi-repo is config plus refusal with door; XXL is advice only | — | mixed | — | — | r29,r33,r10 |
| ax12A1 | table | side-realities.json (real/absent/substituted, default product side); reader contract.side_realities/story_sides | references/side-realities.json:2-5 | held | — | — | r24,g41 |
| ax12B1 | config | environment.integrations[], test_data.pii_and_masking, test_data.shared_records, registry product.sides and environments.sides | references/config-keys.json:782 | held | — | — | r3 |
| ax12B2 | onboarding | Topic 3 asks "Real data and PII — masking rule"; integrations are shown for correction, not asked | skills/qa-onboarding/phases/p2-interview.md:241-245 | held | — | — | r7 |
| ax12C1 | role | common-rules.md:54 applies the pii_and_masking rule to everything a role writes | references/common-rules.md:54 | held | — | — | g10 |
| ax12D1 | hardcoded | s0 prints verbatim "QA Factory v0 covers functional testing only ... out of scope", no question attached (scope statement) | skills/qa-story/phases/s0.md:197 | i | — | — | r23 |
| ax12D2 | hardcoded | Onboarding never asks performance, security, accessibility, privacy: "v0 has no mode for any of them"; volunteered concern noted once | skills/qa-onboarding/phases/p2-interview.md:400-404 | i | — | ax12D1 | r7,g11 |
| ax12D3 | hardcoded | Plan level with no evidence rule (e.g. e2e-mobile) "stays as planned and the gate line names it" (iii); component/unit "not a manual level" | references/manual-policy-by-level.json:2 | iii | — | — | r35,g43 |
| ax12D4 | hardcoded | cli and desktop surfaces: "Agent checks ... are not supported: those cases go to a person" (iii) | references/surfaces.json:26-33 | iii | — | ax7A2 | r5 |
| ax12D5 | absent | No regulated-domain, GDPR, HIPAA or PCI handling in package md, references json or scripts py | ai-packages/qa-factory | absent | — | — | z4,z5,z6 |
| ax12E1 | proven | No fixture named for load, security or accessibility shapes found by name; fixture stories/dry-codemie-14857 name only, not opened | scripts/tests/fixtures | not-determined | — | — | g11,g31 |
| ax12V | verdict | not addressed for load/security/accessibility/regulated (explicit "out of scope"); integrations and PII mixed table+config | — | not-addressed | — | — | r23,r24,z4 |
| ax13A1 | table | install-paths.json classes carried/regenerated/discarded/not_ours with moves; reader install_paths.classify | references/install-paths.json:3-10 | held | — | — | r14 |
| ax13A2 | table | config-keys.json since/absent_means/removed/renamed/reasked/value_migrations; reader config_contract.migration_plan | references/config-keys.json:4-5 | held | — | — | r2,r3 |
| ax13B1 | config | schema_version required; re-onboarding asks only what is not on record (p2-interview 119-129, 209-215) | skills/qa-onboarding/phases/p2-interview.md:209-215 | held | — | — | r7 |
| ax13C1 | role | p2b-rediscovery re-reads only sources unreachable in phase 1; UPGRADE.md sections cover existing config and stories | skills/qa-onboarding/phases/p2b-rediscovery.md:13-18 | held | — | — | r39 |
| ax13D1 | hardcoded | Parallel stories: newest running pipeline.json, else newest: `return pipelines[0].parent if pipelines else None` (ii, "fail-open") | scripts/planning_contract.py:383 | ii | — | ax13D2 | r25,g13 |
| ax13D2 | analog | Twin copy of the same newest-story guess in exit_gate._ticket_for_stage (two code copies of one rule) | scripts/exit_gate.py:794 | ii | — | ax13D1 | g14 |
| ax13D3 | hardcoded | Other schema_version: capability missing, owner user, "re-run qa-onboarding or add the missing keys by hand" (iii; halting not traced) | scripts/readiness.py:1204 | iii | — | — | g60 |
| ax13D4 | hardcoded | Two running dispatches of a role: optional_stage_of_dispatch gives None, "never placed on a stage by a guess" (iii) | scripts/stage_guard.py:254 | iii | — | — | r26 |
| ax13D5 | hardcoded | Default run.parallel false: one run per stand; a second launch waits up to stand_wait_s 1800 on a lease (config default) | references/templates/config.json:141 | ii | — | — | r29 |
| ax13E1 | proven | Fixtures: old-generation-project, config-live-shape.json, config-projection/*; tests test_config_migration, test_reinstall_equals_fresh, test_story_resume_migration | scripts/tests | found | — | — | g31,g32 |
| ax13E2 | proven | Parallel tests (names): test_resume_story_isolation (2406/2534), test_s5_parallel_admission, test_story_run_s5_parallel, test_walk_lanes_parallel | scripts/tests | found | — | — | g32 |
| ax13V | verdict | mixed: migration and install classes are tables, schema is config; several stories in parallel rests on a code-side newest-story guess | — | mixed | — | — | r25,r2,r14 |

## Trail

| tid | op | target | pattern / range | flags | result | control |
|---|---|---|---|---|---|---|
| r1 | read | docs/tasks/specs/20261117-universality-variety-map-brief.md | 1-87 | — | read docs/tasks/specs/20261117-universality-variety-map-brief.md:1-87 | — |
| r2 | read | ai-packages/qa-factory/references/config-keys.json | 1-478 | — | read ai-packages/qa-factory/references/config-keys.json:1-478 | — |
| r3 | read | ai-packages/qa-factory/references/config-keys.json | 560-788 | — | read ai-packages/qa-factory/references/config-keys.json:560-788 | — |
| r4 | read | references/build-identity-methods.json | 1-60 | — | read ai-packages/qa-factory/references/build-identity-methods.json:1-60 | — |
| r5 | read | references/surfaces.json | 1-60 | — | read ai-packages/qa-factory/references/surfaces.json:1-60 | — |
| r6 | read | references/login-roads.json | 1-50 | — | read ai-packages/qa-factory/references/login-roads.json:1-50 | — |
| r7 | read | skills/qa-onboarding/phases/p2-interview.md | 81-410 | — | read ai-packages/qa-factory/skills/qa-onboarding/phases/p2-interview.md:81-410 | — |
| r8 | read | scripts/runtime_probe.py | 1-80 | — | read ai-packages/qa-factory/scripts/runtime_probe.py:1-80 | — |
| r9 | read | scripts/runtime_probe.py | 213-262 | — | read ai-packages/qa-factory/scripts/runtime_probe.py:213-262 | — |
| r10 | read | scripts/runtime_probe.py | 349-395 | — | read ai-packages/qa-factory/scripts/runtime_probe.py:349-395 | — |
| r11 | read | references/host-report-forms.json | 1-25 | — | read ai-packages/qa-factory/references/host-report-forms.json:1-25 | — |
| r12 | read | scripts/driver_core.py | 525-545 | — | read ai-packages/qa-factory/scripts/driver_core.py:525-545 | — |
| r13 | read | scripts/infra_failure.py | 120-160 | — | read ai-packages/qa-factory/scripts/infra_failure.py:120-160 | — |
| r14 | read | references/install-paths.json | 1-20 | — | read ai-packages/qa-factory/references/install-paths.json:1-20 | — |
| r15 | read | references/machine-path-markers.json | 1-20 | — | read ai-packages/qa-factory/references/machine-path-markers.json:1-20 | — |
| r16 | read | scripts/driver_core.py | 543-573 | — | read ai-packages/qa-factory/scripts/driver_core.py:543-573 | — |
| r17 | read | references/gate-approval-words.json | 1-30 | — | read ai-packages/qa-factory/references/gate-approval-words.json:1-30 | — |
| r18 | read | references/question-thresholds.json | 1-20 | — | read ai-packages/qa-factory/references/question-thresholds.json:1-20 | — |
| r19 | read | references/person-owned.json | 1-15 | — | read ai-packages/qa-factory/references/person-owned.json:1-15 | — |
| r20 | read | scripts/gate_brief.py | 650-710 | — | read ai-packages/qa-factory/scripts/gate_brief.py:650-710 | — |
| r21 | read | scripts/exploration.py | 100-145 | — | read ai-packages/qa-factory/scripts/exploration.py:100-145 | — |
| r22 | read | references/common-rules.md | 144-156 | — | read ai-packages/qa-factory/references/common-rules.md:144-156 | — |
| r23 | read | skills/qa-story/phases/s0.md | 190-210 | — | read ai-packages/qa-factory/skills/qa-story/phases/s0.md:190-210 | — |
| r24 | read | references/side-realities.json | 1-14 | — | read ai-packages/qa-factory/references/side-realities.json:1-14 | — |
| r25 | read | scripts/planning_contract.py | 340-409 | — | read ai-packages/qa-factory/scripts/planning_contract.py:340-409 | — |
| r26 | read | scripts/stage_guard.py | 246-262 | — | read ai-packages/qa-factory/scripts/stage_guard.py:246-262 | — |
| r27 | read | scripts/stand_access.py | 748-770 and 1080-1092 | — | read ai-packages/qa-factory/scripts/stand_access.py:748-770 | — |
| r29 | read | references/templates/config.json | 95-143 | — | read ai-packages/qa-factory/references/templates/config.json:95-143 | — |
| r30 | read | plans/MEASUREMENTS.md | 36-50 | — | read plans/MEASUREMENTS.md:36-50 | — |
| r31 | read | plans/MEASUREMENTS.md | 159-161 | — | read plans/MEASUREMENTS.md:159-161 | — |
| r32 | read | plans/MEASUREMENTS.md | 206-221 | — | read plans/MEASUREMENTS.md:206-221 | — |
| r33 | read | scripts/sizing.py | 1-60 | — | read ai-packages/qa-factory/scripts/sizing.py:1-60 | — |
| r34 | read | scripts/regression_scope.py | 1-40 | — | read ai-packages/qa-factory/scripts/regression_scope.py:1-40 | — |
| r35 | read | references/manual-policy-by-level.json | 1-14 | — | read ai-packages/qa-factory/references/manual-policy-by-level.json:1-14 | — |
| r36 | read | references/jira-fields.json | 18-23 | — | read ai-packages/qa-factory/references/jira-fields.json:18-23 | — |
| r39 | read | skills/qa-onboarding/phases/p2b-rediscovery.md | 1-25 | — | read ai-packages/qa-factory/skills/qa-onboarding/phases/p2b-rediscovery.md:1-25 | — |
| g1 | grep | scripts | `vpn\|2fa\|mfa\|totp\|two.factor\|captcha` | -i content glob=*.py | found 30; scripts/reachability.py:147, scripts/vcs_evidence.py:248 | — |
| g2 | grep | scripts | `2fa\|mfa\|totp\|two.factor` | -i count glob=*.py | count 2 | — |
| g3 | grep | scripts | `docker` | -i count glob=*.py | count 380 | — |
| g4 | grep | scripts | `sys\.platform\|platform\.system\(\|os\.name\b\|"darwin"\|"win32"\|powershell\|cmd\.exe` | -i count glob=*.py | count 490 | — |
| g7 | grep | references | `vpn\|2fa\|mfa\|totp\|two.factor\|captcha` | -i content | found 4; references/source-causes.json:6 | — |
| g8 | grep | scripts/ticket_adapter.py | `acceptance_headings\|ACCEPTANCE_HEADINGS\|Acceptance Criteria` | content | found 12; scripts/ticket_adapter.py:510 | — |
| g9 | grep | skills/qa-onboarding/phases/p2-interview.md | `language\|locale` | -i content | found 1; p2-interview.md:291 | — |
| g10 | grep | ai-packages/qa-factory | `in (the )?(person's\|their\|the person) (own )?language\|same language\|language of the (ticket\|person)\|Cyrillic\|non-English\|not English` | -i content glob=*.md | found 16; references/common-rules.md:151 | — |
| g11 | grep | skills | `performance\|load test\|security test\|penetration\|accessibilit\|a11y\|wcag\|non-functional` | -i content glob=*.md | found 14; skills/qa-story/phases/s0.md:197 | — |
| g12 | grep | ai-packages/qa-factory | `XXL` | content glob=*.{py,json} | found 12; scripts/sizing.py:606 | — |
| g13 | grep | scripts | `def running_story\|only running\|exactly one running\|one running story\|more than one running\|several running` | -i content glob=*.py | found 15; scripts/planning_contract.py:365 | — |
| g14 | grep | scripts/exit_gate.py | `def _ticket_for_stage` | content | found 1; scripts/exit_gate.py:794 | — |
| g15 | grep | scripts | `gate_approval_words` | content glob=*.py | found 6; scripts/gate_brief.py:655 | — |
| g16 | grep | scripts | `def gate_approval\|def s0_normalize\|def as_is_word` | content glob=driver_*.py | found 4; scripts/driver_gates.py:1099 | — |
| g17 | grep | scripts | `choices=\(?\[?.?\"claude\"\|--host\|--runner\|run_claude\|codex_cmd` | content glob=driver*.py | found 15; scripts/driver_core.py:590 | — |
| g18 | grep | scripts/run_suite.py | `add_argument\(\"--timeout\"\|\"--wait-max\"` | content | found 2; scripts/run_suite.py:2764 | — |
| g19 | grep | agents | `Recommended regression` | content | found 1; agents/qa-test-strategist.md:27 | — |
| g20 | grep | skills | `Definition of done\|definition of done` | content glob=*.md | found 4; p2-interview.md:390 | — |
| g23 | grep | scripts | `harness_command.*local_login\|ACCESS_KINDS\|access_kinds\|\"ui_only\"\|unknown access kind\|not one of` | content glob=config_contract.py | found 13; scripts/config_contract.py:370, scripts/stand_access.py:73 | — |
| g24 | grep | scripts/reachability.py | `localhost\|127\.0\.0\.1` | content | found 2; scripts/reachability.py:49 | — |
| g25 | grep | scripts/device_stand.py | `host_os\|sys\.platform` | content | found 8; scripts/device_stand.py:196 | — |
| g28 | grep | plans/MEASUREMENTS.md | `^#{1,3} ` | content | found 40; plans/MEASUREMENTS.md:206 | — |
| g29 | grep | plans/MEASUREMENTS.md | `Appium\|android\|device\|VPN\|SSO\|oidc\|emulator\|shared stand\|login` | -i content | found 1; plans/MEASUREMENTS.md:216 | — |
| g30 | glob | scripts/tests | `**/*{android,appium,mobile,oidc,keycloak}*` | — | found 1; scripts/tests/test_mobile_road.py | — |
| g31 | glob | scripts/tests/fixtures | `*{old,legacy,upgrade,migrat,reinstall,parallel}*` | — | found 6; fixtures/old-generation-project/... | — |
| g32 | glob | scripts/tests | `test_*{migrat,upgrade,reinstall,isolation,parallel,first_onboard}*.py` | — | found 8; scripts/tests/test_resume_story_isolation.py | — |
| g33 | glob | scripts/tests/fixtures | `*stand*` | — | found 17; fixtures/old-generation-project/qa-factory/records/stand-identity.json | — |
| g34 | glob | references | `*.json` | — | found 91; references/surfaces.json | — |
| g36 | grep | references | `no internet\|air.?gap\|offline mode\|without internet\|proxy` | -i count glob=*.json | count 4 | — |
| g37 | grep | agents | `response time\|reply within\|turnaround\|how quickly\|office hours\|working hours\|time zone\|timezone` | -i content | found 2; agents/qa-case-designer.md:38 | — |
| g41 | grep | scripts | `side_realities\|side-realities` | content glob=*.py | found 6; scripts/contract.py:5993 | — |
| g43 | grep | scripts | `manual-policy-by-level\|manual_policy_by_level` | content glob=*.py | found 5; scripts/planning_contract.py:2224 | — |
| g48 | grep | scripts/guard_pre_tool.py | `sys\.platform\|platform\.system\(\|os\.name\b\|"darwin"\|"win32"\|powershell\|cmd\.exe` | -i content | found 14; scripts/guard_pre_tool.py:315 | — |
| g50 | grep | references/model-rates.json | `gateway\|subscription\|offline` | -i content | found 5; model-rates.json:292 | — |
| g52 | grep | references/environments.md | `^#{1,3} \|VPN\|shared\|stand that` | content | found 13; environments.md:84 | — |
| g53 | grep | agents/qa-runner.md | `stand` | -i content | found 5; qa-runner.md:50 | — |
| g54 | grep | scripts/project_env.py | `sys\.platform\|platform\.system\(\|os\.name\b\|"darwin"\|"win32"\|powershell\|cmd\.exe` | -i content | found 8; project_env.py:567 | — |
| g56 | grep | scripts/validate_artifacts.py | `BUG_FORM_SECTIONS` | content | found 2; validate_artifacts.py:73 | — |
| g58 | grep | scripts/runtime_probe.py | `docker` | -i count | count 70 | — |
| g60 | grep | scripts/readiness.py | `def _config_schema_status` | content | found 1; readiness.py:1191 | — |
| g61 | grep | scripts/driver_s0.py | `def repo_of_project\|def s0_resolve_branch\|def s0_no_change_entry` | content | found 3; driver_s0.py:1934 | — |
| g62 | grep | skills/qa-story/phases/s3.md | `reply within\|response time\|reviewer of tests\|who reviews\|team lead\|test lead\|approver` | -i content | found 1; s3.md:171 | — |
| g69 | glob | ai-packages/qa-factory | `*.md` | — | found 100; references/codex-host.md | — |
| z1 | grep | references/templates/config.json | `language\|locale` | -i content | absent | c1 |
| c1 | grep | references/templates/config.json | `cache\|ttl` | -i content | found 4; templates/config.json:70 | — |
| z2 | grep | references/config-keys.json | `language\|locale` | -i content | absent | c2 |
| c2 | grep | references/config-keys.json | `gateway\|cache` | -i content | found 2; config-keys.json:635 | — |
| z3 | grep | references/human-questions.md | `language` | -i content | absent | c3 |
| c3 | grep | references/human-questions.md | `question` | -i content | found 2; human-questions.md:3 | — |
| z4 | grep | ai-packages/qa-factory | `regulat\|compliance\|hipaa\|gdpr\|pci\|sox\b` | -i content glob=*.md | absent | c4 |
| c4 | grep | ai-packages/qa-factory | `functional` | -i content glob=*.md | found 2; CHANGELOG.md:7640 | — |
| z5 | grep | references | `regulat\|compliance\|hipaa\|gdpr\|pci\|sox` | -i content glob=*.json | absent | c5 |
| c5 | grep | references | `stand` | -i content glob=*.json | found 1; references/adapter-forms.json:3 | — |
| z6 | grep | scripts | `regulat\|compliance\|hipaa\|gdpr\|\bpci\b` | -i content glob=*.py | absent | c6 |
| c6 | grep | scripts | `docker` | -i content glob=*.py | found 1; scripts/gate_preflight.py:4280 | — |
| z7 | grep | references | `cache.?ttl\|prompt.cache` | -i count glob=*.json | absent | c7 |
| c7 | grep | references | `stand` | -i count glob=*.json | count 442 | — |
| z8 | grep | scripts | `cache.?ttl\|prompt.cache` | -i count glob=*.py | absent | g3 |
| z9 | grep | ai-packages/qa-factory | `[А-Яа-яЁё]` | -i count | absent | c9 |
| c9 | grep | ai-packages/qa-factory | `qa-factory` | -i count | count 9209 | — |
| z10 | glob | scripts/tests/fixtures | `*device*` | — | absent | g33 |

## Not done

- Not read, so claims are limited to file names or line hits: references/codex-host.md, skills/qa-doctor/SKILL.md, references/environments.md body, references/human-text.json, references/verification-levels.json, skills/qa-onboarding/phases/p0-preflight.md, p3 and p4 beyond grep hits, docs/RUNBOOK.md section 11 (MyBooks stand), UPGRADE.md body.
- Test bodies not read (non-goal). The 2 test-file hits for 2FA words (ax7D7) were not opened.
- Parts C and E come from file names, headings and line hits, not from every role file. Part C for axis 8 is unread.
- ax13D3: whether readiness `missing` halts a story was not traced. ax10: the `yes|stop` token in exploration.py:640 was seen in a grep line only; its behaviour on a non-English word is not read.
- Tool note: brace globs (Glob and Grep glob=) returned nothing in some runs; where I claim absence I reran with plain globs and a same-shape control.
- Needed beyond the given list: scripts/*.py, p2-interview.md, plans/MEASUREMENTS.md, agents/*.md, references/*.json.

Analogs (rule 8, no search widening):
- ax13D2: the "newest running pipeline.json" guess exists in two copies, planning_contract.py::running_story and exit_gate.py::_ticket_for_stage.
- ax7A4: 7 access kinds sit in a code tuple (stand_access.py::KINDS) with a second reader in config_contract.py.
- ax11A1: the size cap table is a code constant in sizing.py, not a table.
- ax8D2 and ax8D3: a default model literal and a two-shell tuple sit in code.
