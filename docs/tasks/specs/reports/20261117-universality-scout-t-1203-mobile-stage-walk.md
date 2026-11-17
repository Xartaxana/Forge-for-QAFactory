# Scout digest t-1203: stage walk S0-S9 for a native mobile project (where the factory would stop)

Verbatim hand-back of the scout, extracted from its transcript by the coordinator (scouts cannot write files). Frozen: not edited after extraction.

digest: v1 t-1203

Scope note: the factory already carries a mobile road (surfaces.json rows android/ios on Appium, device_stand.py, device-build question, handed_to_person doors). The given design files predate it. Where design and code differ the code wins (see `dsg.lag`). Reading was targeted, not exhaustive (see Not done). No place was proven as class (i) BLOCKS with no door. Every demand I read had a person's word, a recorded null, or a hand-written door. That is bounded by the unread code listed under Not done.

## Objects
| id | kind | gist | paths | status | owner | links | ev |
|---|---|---|---|---|---|---|---|
| ob.gates | onboarding | Interview topics: tests location, stand address, access scheme, mobile batch (only if phase 1 recorded mobile_surface), execution batch | ai-packages/qa-factory/skills/qa-onboarding/phases/p2-interview.md:120-245 | present | person | ob.detect | T19 |
| ob.detect | onboarding | Mobile surface detected only when Appium is named in a manifest or test file; Maestro/XCUITest/Espresso-only gets no device batch | ai-packages/qa-factory/skills/qa-onboarding/phases/p1-discovery.md:43 | silent-default | — | ob.gates,r1 | T18,T20 |
| ob.url | onboarding | Stand interview asks outright for an HTTP address; unanswered becomes DEFERRED marker plus backlog row, never a placeholder URL | ai-packages/qa-factory/skills/qa-onboarding/phases/p2-interview.md:146-159 | door | person | — | T19 |
| ob.keys | onboarding | No meaningful mobile answer: stand base URL, unauth_status, frontend.api_path; access.kind offers ui_only or none | ai-packages/qa-factory/skills/qa-onboarding/phases/p2-interview.md:146-200 | steps-aside | person | ob.url | T19 |
| ob.default | onboarding | Keys left default: tests_root empty gives not_configured; absent execution profile gives not_configured warning, not a halt | ai-packages/qa-factory/scripts/readiness.py:407 | warning | — | s0.gates | T12,T13 |
| ob.report | onboarding | Discovery notes: a run with no machine-readable report is recorded not_executed; reporter set is pytest, junit-xml, trx, none | ai-packages/qa-factory/skills/qa-onboarding/phases/p1-discovery.md:35 | silent-default | — | s5.report | T20,T21 |
| s0.gates | gates | S0 requires capabilities ticket_adapter, test_repo, vcs, config_schema; missing gives a closed question | ai-packages/qa-factory/scripts/driver_s0.py::Driver.s0_rest:2396 | present | person | s0.door | T16 |
| s0.door | door | S0 readiness question offers retry, go on (recorded as the person's decision), stop | ai-packages/qa-factory/scripts/driver_s0.py:2408-2422 | door | person | s0.gates | T16 |
| s0.shape | shape | test_repo demands tests_root exist as a folder; shape-neutral for Kotlin/Swift unless the tests live outside any folder named | ai-packages/qa-factory/scripts/readiness.py::check_test_repo:404-411 | neutral | — | s0.gates | T13 |
| s0.inproc | silent-default | An environments row with no base_url/url/health_url reads as in-process: OK, nothing to probe, so an undescribed device passes S0 | ai-packages/qa-factory/scripts/readiness.py::_check_plain_environment:878-883 | silent-default | — | s5.prov,s6.stand | T10 |
| s0.device | steps-aside | A row naming a device surface is probed read-only; empty app.id is not_configured; probe fail is missing (user) or unknown (factory) | ai-packages/qa-factory/scripts/readiness.py::_device_check:810-844 | steps-aside | — | s0.inproc | T10 |
| s0.stand | door | env_probe exit non-zero at S0 is a warning only; the story goes on and the stand is re-checked before tests | ai-packages/qa-factory/scripts/driver_s0.py:2424-2437 | steps-aside | — | s6.stand | T16 |
| s1.gates | gates | S1 required outputs context-manifest.json and context-bundle.json; grounding by diff, current-code or ungrounded (design doc) | ai-packages/qa-factory/references/stages.json:46-55 | neutral | — | — | T47,T2 |
| s2.gates | gates | S2 required outputs register, readiness.json, understanding.md; detectors sizing.py and branch_accounting.py | ai-packages/qa-factory/references/stages.json:73-91 | neutral | — | — | T47 |
| s3.gates | gates | S3 required outputs test-plan.md and test-plan.json; detectors planning_contract.py, branch_accounting.py; optional first_look walk | ai-packages/qa-factory/references/stages.json:119-133 | neutral | — | s3.look | T47 |
| s3.look | null | first_look.due returns recordable null reasons: no_stand, no_code_yet, empty_register; survey walk fits only web/api profile | ai-packages/qa-factory/scripts/first_look.py::due:940-970 | steps-aside | — | s3.walk | T50,T51 |
| s3.walk | null | Survey walk with no web or api profile ends as refusal no_reachable_surface, exit 2; first look is written as null | ai-packages/qa-factory/scripts/walk_session.py::_surface_profile:1263-1265 | steps-aside | — | s3.look | T52,T48 |
| s3.dead | door | first_look.dead question when reachable share is below the floor; door is the person's continue (first_look_continue) | ai-packages/qa-factory/scripts/driver_stage_plan.py::_first_look_question:334-371 | door | person | — | T48,T4 |
| s4.gates | gates | S4 required output work/test-cases/; Gate A rehearsal runs 23 checks, closed by gate_ready when no factory_fixable finding | ai-packages/qa-factory/scripts/gate_preflight.py::run:6085-6107 | present | — | s4.exec,s4.rep | T35,T47 |
| s4.exec | door | Missing executor or no profile keys the cases: person_decides, three answers install, other environment, handed_to_person | ai-packages/qa-factory/scripts/gate_preflight.py::check_s5_executor:2845-2875 | door | person | s5.exec | T31,T28 |
| s4.tool | steps-aside | Toolchain collect rehearsal runs only for a pytest-shaped command; other runners get no step, no refusal | ai-packages/qa-factory/scripts/gate_preflight.py::check_s5_toolchain:2940-2944 | steps-aside | — | s4.pytest | T32,T27 |
| s4.pytest | shape | collect_base keeps only a command whose first tokens contain a pytest token; Gradle/xcodebuild/Maestro commands return [] | ai-packages/qa-factory/scripts/gate_preflight.py::collect_base:461 | pytest-shaped | — | s4.tool | T27 |
| s4.rep | shape | Reporter rehearsal runs one existing test; probe-test floor globs list py/ts/js/cs only, with no Kotlin or Swift names | ai-packages/qa-factory/scripts/gate_preflight.py:847-848 | pytest-shaped | — | s5.report | T29,T33 |
| s4.fix | gap | Runtime-probe step: matched or unknown is factory_fixable and S4 does not close until the driver repair ran; needs recorded checkout | ai-packages/qa-factory/scripts/gate_preflight.py::check_s5_runtime_probe:4254-4323 | unproven | factory | s5.prov | T34 |
| s4.stand | door | Gate A: environment or test_repo capability missing gives person_decides: fix stand or let stage run and report | ai-packages/qa-factory/scripts/gate_preflight.py::check_stand:2261-2268 | door | person | — | T30 |
| s5.scope | gate | S5 raises Refusal when stage-scope has no automate case; an all-manual mobile story reaches the conductor seam | ai-packages/qa-factory/scripts/driver_stage_s5.py::stage_S5:230-231 | unproven-door | conductor | dsg.empty | T57,T58 |
| s5.prov | gate | Behavioral run requires runtime_provenance valid: matched, person_confirmed (person word) or not_applicable; probe argv required | ai-packages/qa-factory/scripts/execution_request.py:152-195 | door | person | s5.probe | T22 |
| s5.probe | gate | First typed run of a profile with no registered runtime probe is refused; the refusal names a write door or a hand-written request | ai-packages/qa-factory/scripts/execution_request.py::_probe_refusal:2810-2835 | door | role | s5.prov | T24,T25 |
| s5.nockout | door | Probe write door needs implementation_repos[].local_path; with none the text sends the role to run_suite.py --template request | ai-packages/qa-factory/scripts/execution_request.py:2828-2835 | door | role | s5.probe | T24 |
| s5.ident | shape | Build identity ladder is sources, oci_label, build_sha_file (container); command and person_confirms are person-only | ai-packages/qa-factory/references/build-identity-methods.json:14 | container-shaped | person | s5.devbuild | T36 |
| s5.devbuild | door | Device-stand variant of the build question: deployed, retry, command, stop (EP1-41e) applies to device surface rows only | ai-packages/qa-factory/references/build-identity-methods.json:206-224 | door | person | s5.ident | T36,T26 |
| s5.report | silent-default | Reporter none is accepted; a run with no report is recorded not_executed however green its log, and S6 then trips | ai-packages/qa-factory/scripts/execution_request.py:29 | silent-default | — | s6.exit,ob.report | T21,T63 |
| s5.read | shape | Case-to-test binding by marker is Python AST (pytest.mark.qa); a suffix with no detectors row is a note | ai-packages/qa-factory/scripts/manifest_from_tests.py:344-353 | door | role | s5.probegap | T40,T42,T44 |
| s5.rows | shape | assertion_probes rows exist for suffixes .cs .java .ts .tsx .js .jsx .mjs .cjs .mts .cts .py; none for .kt .swift | ai-packages/qa-factory/references/detectors.json:87-327 | table-gap | — | s5.read,s5.probegap | T43 |
| s5.probegap | door | probe_by_code on an unlisted suffix is ToolRefusal naming doors: probe gap word tooling:language, or red_sandbox.py --probe | ai-packages/qa-factory/scripts/probe_by_code.py::_no_entry:1455-1465 | door | person | s5.rows | T45,T59,T46 |
| s5.exec | door | Executor missing mid-S5 asks the same three-answer question; handed_to_person writes and reviews code, never waits | ai-packages/qa-factory/scripts/gate_preflight.py:517-552 | door | person | s4.exec | T28 |
| s5.diff | steps-aside | Executable-change detection reads Python only; any non-.py file classifies as code, costing reruns not blocking | ai-packages/qa-factory/scripts/diff_scope.py:241-274 | steps-aside | — | — | T62 |
| s6.gates | gates | S6 required output work/run-report.json; scope split automation and manual; nothing to execute closes by code | ai-packages/qa-factory/scripts/driver_stage_s6.py::stage_S6:502-513 | present | — | s6.stand | T54 |
| s6.stand | door | stand_check: no stand or unconfirmed stand asks; the person's word passes block stand not confirmed for S5 and S6 | ai-packages/qa-factory/scripts/driver_stage_build.py::stand_check:139-175 | door | person | s0.inproc | T53 |
| s6.nostand | steps-aside | With no stand, S6 runs no runner probe; changed tests are left for a run on a stand and the digest says how many | ai-packages/qa-factory/scripts/driver_stage_s6.py:565-569 | steps-aside | — | s6.stand | T54 |
| s6.device | steps-aside | Manual-agent cases on a device row skip the default web account question; Appium backend drives them | ai-packages/qa-factory/scripts/driver_stage_s6.py::_cases_all_on_driver:1071-1095 | steps-aside | — | s6.web | T55 |
| s6.web | silent-default | declared_surfaces returns empty when no environment names a surface and capabilities are web/api words; capture then follows the web road | ai-packages/qa-factory/scripts/surfaces.py::declared_surfaces:113-114 | silent-default | — | r2 | T56 |
| s6.exit | gate | run-report execution_status other than passed or failed (env_blocked, not_executed, broken_run, timeout) gives S7 entry refusal (design doc) | docs/factory-map/qa-factory-paths.md:309-312 | door | conductor | s5.report | T3 |
| s6.unknownword | door | A capability word the table lacks, or no stand for a native profile, sends those cases to a person (hands: person) | ai-packages/qa-factory/scripts/surfaces.py:127-141 | door | person | s6.web | T56,T8 |
| s7.gates | gates | S7 required output work/triage.json; no failure and no manual fail closes by code; NE7 declares the empty outcome | ai-packages/qa-factory/references/null-outcomes.json:37-40 | neutral | — | — | T37,T47 |
| s8.gates | gates | S8 requires ledger.json, ledger.md, test-report.md; gate B needs report and delivery-summary on disk; draft needs manual_steps | ai-packages/qa-factory/references/null-outcomes.json:61-68 | neutral | — | — | T37,T47 |
| s9.gates | gates | S9 required output retro.md; retro_mode full, numbers or skip chosen at gate B | ai-packages/qa-factory/references/stages.json:338-345 | neutral | — | — | T47,T3 |
| dsg.lag | disagree | Design cites story_run.py:s0, stage_S5, stage_S6; code lives in driver_s0.py::Driver.s0, driver_stage_s5.py, driver_stage_s6.py | ai-packages/qa-factory/scripts/driver_s0.py:2248 | design-lags | — | — | T2,T16 |
| dsg.empty | disagree | Design Delta4 and driver_stage_s5.py:230 agree on the refusal; null-outcomes NE25 says S5 closes with no plan (E7); not reconciled | ai-packages/qa-factory/references/null-outcomes.json:25-28 | unreconciled | — | s5.scope | T37,T57 |
| an.kt | analog | test-path-markers code_extensions includes .kt .swift while detectors.json assertion_probes has no .kt or .swift row | ai-packages/qa-factory/references/test-path-markers.json:8 | analog | — | s5.rows | T38,T43 |
| an.marker | analog | case-markers.json decorator_prefix is @pytest.mark. only; the factory's own case marker has no non-Python form | ai-packages/qa-factory/references/case-markers.json:4 | analog | — | s5.read | T39 |
| an.globs | analog | gate_preflight REPORTER_TEST_GLOBS floor omits Kotlin, Swift and Java names while test-path-markers covers them | ai-packages/qa-factory/scripts/gate_preflight.py:847-848 | analog | — | s4.rep | T29,T38 |
| r1 | rank-iii | Onboarding: p1-discovery.md:43 mobile_surface needs Appium named; demand: device-stand batch; project with other stacks gets web interview | ai-packages/qa-factory/skills/qa-onboarding/phases/p1-discovery.md:43 | iii | person | ob.detect | T20 |
| r2 | rank-iii | S4 to S6: surfaces.py::declared_surfaces:113 returns empty for undeclared surface; demand: browser capture on a web stand; mobile has none | ai-packages/qa-factory/scripts/surfaces.py:113 | iii | person | s6.web | T56 |
| r3 | rank-iii | S0: readiness.py::_check_plain_environment:882 passes URL-less row as in-process OK; demand: a probed stand; later stage S5 or S6 asks | ai-packages/qa-factory/scripts/readiness.py:882 | iii | person | s0.inproc | T10 |
| r4 | rank-iii | S5: execution_request.py:29 reporter none; demand: junit-xml or trx report; xcresult or log-only stacks give not_executed, S6 trips | ai-packages/qa-factory/scripts/execution_request.py:29 | iii | person | s5.report | T21,T63 |
| r5 | rank-ii | S5: probe_by_code.py::_no_entry; demand: assertion_probes row; Kotlin/Swift have none; door probe gap tooling word or red_sandbox | ai-packages/qa-factory/scripts/probe_by_code.py:1455 | ii | person | s5.probegap | T45 |
| r6 | rank-ii | S5: manifest_from_tests.py::NO_READER_DOOR; demand: marker reader for suffix; door: role writes rows with manifest_put.py --fragment | ai-packages/qa-factory/scripts/manifest_from_tests.py:344 | ii | role | s5.read | T42 |
| r7 | rank-ii | S5: execution_request.py::_probe_refusal; demand: runtime probe; door: role hand-writes request from template or person says deployed | ai-packages/qa-factory/scripts/execution_request.py:2810 | ii | role | s5.probe | T24 |
| r8 | rank-ii | Gate A: gate_preflight.py::check_s5_executor; demand: launcher resolves; door: person picks install, other environment or handed_to_person | ai-packages/qa-factory/scripts/gate_preflight.py:2815 | ii | person | s4.exec | T31 |
| r9 | rank-ii | S0: driver_s0.py::Driver.s0_rest; demand: test_repo, vcs, ticket_adapter, config_schema; door: person says go on | ai-packages/qa-factory/scripts/driver_s0.py:2408 | ii | person | s0.door | T16 |
| r10 | rank-ii | S6: driver_stage_build.py::stand_check; demand: confirmed stand; door: person word, block stand not confirmed | ai-packages/qa-factory/scripts/driver_stage_build.py:139 | ii | person | s6.stand | T53 |
| r11 | rank-ii | S5: driver_stage_s5.py::stage_S5:230; demand: at least one automate case; door: Refusal to conductor, not traced to closure | ai-packages/qa-factory/scripts/driver_stage_s5.py:230 | ii | conductor | s5.scope | T57 |
| r12 | rank-ii | Gate A: gate_preflight.py::check_s5_runtime_probe; demand: probe repair run before S4 closes; loop on mobile not proven | ai-packages/qa-factory/scripts/gate_preflight.py:4254 | ii | factory | s4.fix | T34 |

## Trail
| tid | op | target | pattern / range | flags | result | control |
|---|---|---|---|---|---|---|
| T1 | read | docs/tasks/specs/20261117-universality-variety-map-brief.md | 1-120 | — | read docs/tasks/specs/20261117-universality-variety-map-brief.md:1-110 | — |
| T2 | read | docs/factory-map/qa-factory-paths.md | 1-250 | — | read docs/factory-map/qa-factory-paths.md:1-250 | — |
| T3 | read | docs/factory-map/qa-factory-paths.md | 248-477 | — | read docs/factory-map/qa-factory-paths.md:248-477 | — |
| T4 | read | ai-packages/qa-factory/design/state-exits.md | 1-150 | — | read ai-packages/qa-factory/design/state-exits.md:1-150 | — |
| T5 | glob | ai-packages/qa-factory/scripts | `ai-packages/qa-factory/scripts/*.py` | — | found 100 | — |
| T6 | grep | ai-packages/qa-factory | `appium|\.apk|\.ipa|emulator|xcuitest|espresso|maestro|android|ios\b|mobile` | -i count glob=!**/tests/** | count 121 | — |
| T7 | read | ai-packages/qa-factory/scripts/device_stand.py | 1-80 | — | read ai-packages/qa-factory/scripts/device_stand.py:1-80 | — |
| T8 | read | ai-packages/qa-factory/references/surfaces.json | 1-60 | — | read ai-packages/qa-factory/references/surfaces.json:1-59 | — |
| T9 | grep | ai-packages/qa-factory/scripts | `appium|\.apk|\.ipa|emulator|xcuitest|espresso|maestro|android|mobile` | -i content glob=!tests/** | found 80 | — |
| T10 | read | ai-packages/qa-factory/scripts/readiness.py | 793-937 | — | read ai-packages/qa-factory/scripts/readiness.py:793-937 | — |
| T11 | read | ai-packages/qa-factory/scripts/readiness.py | 1216-1322 | — | read ai-packages/qa-factory/scripts/readiness.py:1216-1322 | — |
| T12 | read | ai-packages/qa-factory/scripts/readiness.py | 1086-1135 | — | read ai-packages/qa-factory/scripts/readiness.py:1086-1135 | — |
| T13 | read | ai-packages/qa-factory/scripts/readiness.py | 404-415 | — | read ai-packages/qa-factory/scripts/readiness.py:404-415 | — |
| T14 | read | ai-packages/qa-factory/scripts/readiness.py | 534-569 | — | read ai-packages/qa-factory/scripts/readiness.py:534-569 | — |
| T15 | read | ai-packages/qa-factory/scripts/readiness.py | 696-717 | — | read ai-packages/qa-factory/scripts/readiness.py:696-717 | — |
| T16 | read | ai-packages/qa-factory/scripts/driver_s0.py | 2248-2517 | — | read ai-packages/qa-factory/scripts/driver_s0.py:2248-2517 | — |
| T17 | grep | ai-packages/qa-factory/scripts/env_probe.py | `surface|device|appium` | -i content | found 15 | — |
| T18 | grep | ai-packages/qa-factory/skills/qa-onboarding | `mobile|android|device|surface|native|appium|apk` | -i content | found 31 | — |
| T19 | read | ai-packages/qa-factory/skills/qa-onboarding/phases/p2-interview.md | 120-245 | — | read ai-packages/qa-factory/skills/qa-onboarding/phases/p2-interview.md:120-245 | — |
| T20 | read | ai-packages/qa-factory/skills/qa-onboarding/phases/p1-discovery.md | 25-54 | — | read ai-packages/qa-factory/skills/qa-onboarding/phases/p1-discovery.md:25-54 | — |
| T21 | read | ai-packages/qa-factory/scripts/execution_request.py | 20-80 | — | read ai-packages/qa-factory/scripts/execution_request.py:20-79 | — |
| T22 | read | ai-packages/qa-factory/scripts/execution_request.py | 148-197 | — | read ai-packages/qa-factory/scripts/execution_request.py:148-195 | — |
| T23 | read | ai-packages/qa-factory/scripts/execution_request.py | 215-285 | — | read ai-packages/qa-factory/scripts/execution_request.py:215-284 | — |
| T24 | read | ai-packages/qa-factory/scripts/execution_request.py | 2800-2925 | — | read ai-packages/qa-factory/scripts/execution_request.py:2800-2924 | — |
| T25 | grep | ai-packages/qa-factory/scripts/execution_request.py | `runtime_probes|runtime_required|no runtime probe|device_stand|surface` | -i content | found 18 | — |
| T26 | grep | ai-packages/qa-factory/scripts/runtime_probe.py | `device|surface` | -i content | found 19 | — |
| T27 | read | ai-packages/qa-factory/scripts/gate_preflight.py | 440-487 | — | read ai-packages/qa-factory/scripts/gate_preflight.py:440-487 | — |
| T28 | read | ai-packages/qa-factory/scripts/gate_preflight.py | 495-615 | — | read ai-packages/qa-factory/scripts/gate_preflight.py:495-614 | — |
| T29 | read | ai-packages/qa-factory/scripts/gate_preflight.py | 759-870 | — | read ai-packages/qa-factory/scripts/gate_preflight.py:759-870 | — |
| T30 | read | ai-packages/qa-factory/scripts/gate_preflight.py | 2244-2270 | — | read ai-packages/qa-factory/scripts/gate_preflight.py:2244-2270 | — |
| T31 | read | ai-packages/qa-factory/scripts/gate_preflight.py | 2815-2880 | — | read ai-packages/qa-factory/scripts/gate_preflight.py:2815-2878 | — |
| T32 | read | ai-packages/qa-factory/scripts/gate_preflight.py | 2920-2970 | — | read ai-packages/qa-factory/scripts/gate_preflight.py:2920-2969 | — |
| T33 | read | ai-packages/qa-factory/scripts/gate_preflight.py | 3275-3335 | — | read ai-packages/qa-factory/scripts/gate_preflight.py:3275-3334 | — |
| T34 | read | ai-packages/qa-factory/scripts/gate_preflight.py | 4254-4324 | — | read ai-packages/qa-factory/scripts/gate_preflight.py:4254-4323 | — |
| T35 | read | ai-packages/qa-factory/scripts/gate_preflight.py | 6078-6112 | — | read ai-packages/qa-factory/scripts/gate_preflight.py:6078-6109 | — |
| T36 | read | ai-packages/qa-factory/references/build-identity-methods.json | 1-325 | — | read ai-packages/qa-factory/references/build-identity-methods.json:1-325 | — |
| T37 | read | ai-packages/qa-factory/references/null-outcomes.json | 1-120 | — | read ai-packages/qa-factory/references/null-outcomes.json:1-120 | — |
| T38 | read | ai-packages/qa-factory/references/test-path-markers.json | 1-60 | — | read ai-packages/qa-factory/references/test-path-markers.json:1-12 | — |
| T39 | read | ai-packages/qa-factory/references/case-markers.json | 1-60 | — | read ai-packages/qa-factory/references/case-markers.json:1-9 | — |
| T40 | read | ai-packages/qa-factory/scripts/manifest_from_tests.py | 2-62 | — | read ai-packages/qa-factory/scripts/manifest_from_tests.py:2-59 | — |
| T41 | read | ai-packages/qa-factory/scripts/manifest_from_tests.py | 136-178 | — | read ai-packages/qa-factory/scripts/manifest_from_tests.py:136-177 | — |
| T42 | read | ai-packages/qa-factory/scripts/manifest_from_tests.py | 345-387 | — | read ai-packages/qa-factory/scripts/manifest_from_tests.py:345-386 | — |
| T43 | grep | ai-packages/qa-factory/references/detectors.json | `"\.(kt|swift|java|js|ts|py|cs|go|rb|kts)"` | content | found 5 | — |
| T44 | grep | ai-packages/qa-factory/scripts | `no_entry|no_reader|NO_READER` | content glob=!tests/** | found 40 | — |
| T45 | read | ai-packages/qa-factory/scripts/probe_by_code.py | 1440-1500 | — | read ai-packages/qa-factory/scripts/probe_by_code.py:1440-1499 | — |
| T46 | grep | ai-packages/qa-factory/scripts/window_record.py | `probe_gap|probe gap|probe_not_applicable|probe_could_not_run` | content | found 25 | — |
| T47 | read | ai-packages/qa-factory/references/stages.json | 1-370 | — | read ai-packages/qa-factory/references/stages.json:1-370 | — |
| T48 | grep | ai-packages/qa-factory/scripts/driver_stage_plan.py | `first_look` | content | found 37 | — |
| T49 | read | ai-packages/qa-factory/scripts/driver_stage_plan.py | none | — | read ai-packages/qa-factory/scripts/driver_stage_plan.py:184-216 | — |
| T50 | grep | ai-packages/qa-factory/scripts/first_look.py | `^def (due|walk_actors|begin|dead|share)` | content | found 4 | — |
| T51 | grep | ai-packages/qa-factory/references/first-look-statuses.json | `null_reasons|"due"|device|native|ui|no_stand|no_ui` | content | found 6 | — |
| T52 | read | ai-packages/qa-factory/scripts/walk_session.py | 1236-1275 | — | read ai-packages/qa-factory/scripts/walk_session.py:1236-1275 | — |
| T53 | read | ai-packages/qa-factory/scripts/driver_stage_build.py | 139-199 | — | read ai-packages/qa-factory/scripts/driver_stage_build.py:139-198 | — |
| T54 | read | ai-packages/qa-factory/scripts/driver_stage_s6.py | 480-590 | — | read ai-packages/qa-factory/scripts/driver_stage_s6.py:480-590 | — |
| T55 | read | ai-packages/qa-factory/scripts/driver_stage_s6.py | 1071-1127 | — | read ai-packages/qa-factory/scripts/driver_stage_s6.py:1071-1126 | — |
| T56 | read | ai-packages/qa-factory/scripts/surfaces.py | 91-150 | — | read ai-packages/qa-factory/scripts/surfaces.py:91-148 | — |
| T57 | read | ai-packages/qa-factory/scripts/driver_stage_s5.py | 205-241 | — | read ai-packages/qa-factory/scripts/driver_stage_s5.py:205-240 | — |
| T58 | grep | ai-packages/qa-factory/scripts/driver_stage_s5.py | `nothing to automate|no automate|empty scope|code_only|not scope` | -i content | found 2 | — |
| T59 | grep | ai-packages/qa-factory/scripts/contract.py | `tooling:` | content | found 2 | — |
| T60 | grep | ai-packages/qa-factory/scripts/s5_precheck.py | `junit|trx|reporter|report_id|classname` | -i content | found 10 | — |
| T61 | read | ai-packages/qa-factory/scripts/s5_precheck.py | 838-874 | — | read ai-packages/qa-factory/scripts/s5_precheck.py:838-873 | — |
| T62 | grep | ai-packages/qa-factory/scripts/diff_scope.py | `^"""|^def [a-z_]+|\.py\b|pytest|language` | content | found 40 | — |
| T63 | grep | ai-packages/qa-factory/scripts | `reporter.*none|not_executed` | content glob=run_suite* | found 12 | — |
| T64 | grep | ai-packages/qa-factory/scripts | `junit|pytest|trx|xunit|allure|"reporter"|REPORTERS|reporter_kinds` | -i content glob={run_suite,execution_request,config_contract}*.py | found 50 | — |

## Forks
No fork was put to me as a choice. The ranking above follows the dispatch's ordering rule, with no merit judgment. Class (i) is empty only within the bounds under Not done.

this needs a decision from a tier above.

## Not done
- Not read in code, so S1, S2, S7, S8 and S9 are "neutral" only by stages.json required_outputs, null-outcomes rows and the design-doc graphs. Unread: `scripts/source_preflight.py`, `context_bundle.py`, `sizing.py` (a 4-hit count only), `branch_accounting.py`, `planning_contract.py`, `coverage_contract.py`, `driver_stage_s7.py::stage_S7`, `finalize_task.py`, `check_delivery.py`, `stage_done.py`.
- `s6.exit` (S7 entry refusal on env_blocked, not_executed, broken_run) rests on the design doc `qa-factory-paths.md` §8, not on code. `finalize_task.py:448,628-637` and `run_suite.py:366` carry the not_executed text but were seen only in grep output. For T63 and T64 the digest uses only the matched lines, and the found counts are from capped output.
- Not proven: whether the `s4.fix` runtime-probe repair (`factory_fixable`, S4 refuses to close) can loop on a mobile project with a recorded checkout and no container. Not traced either: what `env_probe.py --env <row>` exits for a URL-less row without `surface`. The in-process pass at `readiness.py:882` is the only fact read.
- Not traced: which entry closes S5 on an empty scope (NE25 says it closes, `stage_S5` raises). `dsg.empty` stays open.
- Not read: `manual_capture.py::AppiumBackend` (2305) and `capture_profile`. Whether a device profile with capability `native` and no Appium row works end to end is unverified; the table only has an appium driver (`surfaces.json` drivers).
- Not read: `run_suite.py` node-id and report-id mapping for Gradle, Maestro and xcodebuild junit output (the node_id_mismatch road). `instance_contracts` and `report_id_source` were seen only by grep.
- Two zero-result greps are not used as claims: `story_run*.py` def names (the design-cited names are not reported as absent; the real homes are in `dsg.lag`), and `observation_contract.py` for mobile terms. No search is offered as proof of absence in this digest.
- Counts in found rows of capped or long greps (T9, T18, T25, T26, T44, T46, T48, T62-T64) are approximate; the claims rest on the cited lines.
- Design files disagreeing with code: `docs/factory-map/qa-factory-paths.md` cites `scripts/story_run.py:s0,check_ticket,stage_S5,stage_S6`; the code is `driver_s0.py`, `driver_stage_s5.py`, `driver_stage_s6.py`. That file (snapshot 28.09) says nothing of device stands, `surfaces.json` or `device_stand.py`, which exist in the package. Needed beyond the given list: `references/surfaces.json`, `build-identity-methods.json`, `null-outcomes.json`, `detectors.json`, the onboarding phases, and the `driver_*`, `gate_preflight`, `execution_request`, `readiness` and `surfaces` scripts.
