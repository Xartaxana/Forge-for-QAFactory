# t-356 scout digest: why the forge net missed the LR2-1 blockers (verbatim hand-back, 13.11.2026)

digest: v1 fvf-net-why

Tree legend. RM = C:\QAFactory\forge-repo\.claude\worktrees\read-main\ai-packages\qa-factory (origin/main package). FND = C:\QAFactory\forge-repo\.claude\worktrees\findings-1413\plans\piles\live-run-fvf\findings (findings; each cited file is in FND). Paths below are relative to RM unless prefixed FND. Everything marked INFERENCE is not read from code.

Bottom line, read from code, not guessed. Six patterns recur, and each is a Trail-backed row in Objects:
- P-A: tests feed the reader a hand-written input, not the output of the current producer.
- P-B: tests pin the behaviour the owner later called a defect.
- P-C: the seam under test is replaced by a lambda stub.
- P-D: the driver-loop tests switch the handoff-form requirement off.
- P-E: the audit counts source sites, not states or refusal kinds.
- P-F: the two stage-joint nets are name-level registries.

## Objects
| id | kind | gist | paths | status | owner | links | ev |
|---|---|---|---|---|---|---|---|
| B1a-reader | fact | Reader accepts only TS-n: CASE_PLAN_ROW_RE `Plan row:\s*(TS-\d+)`, s5_precheck PLAN_ROW_RE same | RM/scripts/contract.py:3052; RM/scripts/s5_precheck.py:79 | present | - | B1b-producer | t2,t3 |
| B1b-producer | fact | The package's own S3->S4 handoff forms tell the role the plan row id is `<P-n>` | RM/handoffs/s3-strategist-to-designer.yaml:52; RM/handoffs/s4-designer-to-case-critic.yaml:50; RM/handoffs/s4-designer-to-runner.yaml:48; RM/references/slices/qa-test-strategist/handoff-keys.md:27 | present | - | B1a-reader | t14,t15 |
| B1b2 | fact | Contract docs say TS-n (artifact-contract-plan.md:46, artifact-contract.md:63 `Plan row: TS-n`). Producer instruction conflicts with reader inside the package | RM/references/artifact-contract-plan.md:46; RM/references/artifact-contract.md:63 | present | - | B1a-reader | t14,t16 |
| B1c | fact | Existing net for the reader: tests build cases by hand with TS-1, e.g. `Requirements: R-1\nPlan row: TS-1\n\n## Then...` | RM/scripts/tests/test_s3_s4_chain.py:52 | present | - | P-A | t17 |
| B1c2 | fact | No test feeds `Plan row: P-<n>` to the reader: grep absent, control t18 is the TS/P alternation count (33 hits in 27 files) | RM/scripts/tests | absent | - | B1c | t17,t18 |
| B1c3 | fact | stage-joints registry (references/stage-joints.json) has no row for plan-row id form; walks check names, not values | RM/references/stage-joints.json | absent | - | P-F | t8,t9 |
| B1d | fact | TS-form chain case->manifest->plan row is CHANGELOG 0.3.0 (2026-09-16, line 7411). The P-n form in the handoffs is not recorded in the CHANGELOG. test_s3_s4_chain.py is in `quarantine` (test-layers.json:9557) | RM/CHANGELOG.md:7411; RM/scripts/tests/test-layers.json:9557 | present | - | - | t19,t20,t44 |
| B1e | fact | FND finding class: one role writes P-n, other stage's code reads TS-n; S3/S4 gates did not check the join (AR-22) | FND/20261112-s5-pustaya-oblast-p-n-protiv-ts-n.md:13-15 | present | - | - | t1 |
| B2a-reader | fact | Refusal "a reject needs failure_class ... a quote" raised by stage_acceptance_errors; record built by stage_acceptance_from_form from form section `stage_acceptance` | RM/scripts/acceptance.py:1353-1357,1559-1580 | present | - | B2a-producer | t21,t22 |
| B2a-reader2 | fact | Writer `stage_done.record_acceptance` accepts a CONSUMER form (analyst for S6, X7-6); reviewed dispatch must be the LAST `inputs_read` row naming the runner (`reviewed_author_dispatch`) | RM/scripts/stage_done.py:1018-1044,939-955 | present | - | B2a-producer | t23 |
| B2a-producer | fact | Analyst's own form template s7-analyst-to-automator.yaml has no `stage_acceptance` section and its inputs_read lists run-report rows, no runner row. Grep over handoffs: section exists in s2/s3/s4/s7-analyst-to-scribe/s8 forms only | RM/handoffs/s7-analyst-to-automator.yaml:64-75; RM/handoffs/s6-runner-to-analyst.yaml | absent | - | B2a-reader | t24,t25 |
| B2a-role | fact | Role text says only "accepted or returned ... Witness: the acceptance record, if named" - no field names | RM/agents/qa-failure-analyst.md:28 | present | - | - | t26 |
| B2a-brief | fact | Brief line `Reviewed dispatch: the LAST inputs_read row ...` is the only up-front statement; code never prefills the row | RM/scripts/brief_pack.py:3509-3526 | present | - | B2a-producer | t27 |
| B2b | fact | Test of this reader builds the analyst form BY HAND with a stage_acceptance section: FORM/SECTION strings (`failure_class: capability`, header stage: S3) | RM/scripts/tests/test_stage_acceptance_consumer.py:49-52 | present | - | P-A | t28 |
| B2b2 | fact | Same test reads the real scribe template (S7 (6), lines 341-345) but no test reads the analyst template for `stage_acceptance` | RM/scripts/tests/test_stage_acceptance_consumer.py:341-345 | present | - | B2b | t29 |
| B2b3 | fact | The test file's own header says lambda stubs of budget_or_none, rework, stage_review_exhausted "hid B1 and B2" (a prior defect of this exact class) | RM/scripts/tests/test_stage_acceptance_consumer.py:366 | present | - | P-C | t28 |
| B2c | fact | Passed because the form-to-record test uses a hand-written form with the section; the real template (no section) never goes through the reader. The repeated rework_stage(cause tooling) loop rests on tooling not spending a round: INFERENCE, only REVIEWER_CAUSES controller.py:257 and driver_dispatch.py:2920 read | RM/scripts/controller.py:257 | present | - | P-D | t28,t30 |
| B2d | fact | X7-6 consumer acceptance not dated by name in the CHANGELOG (not searched). test_stage_acceptance_consumer.py is in `quarantine` (test-layers.json:9786) | RM/scripts/tests/test-layers.json:9786 | present | - | - | t44 |
| B2e | fact | FND: stage_done refuses fields the S7 form does not carry (FR-38, AR-10, AR-22); fix proposal = form carries them, or acceptance derives them | FND/20261113-s7-petlya-dirizhera-na-prieme-s6.md:11-15,31 | present | - | - | t1 |
| B3a-reader | fact | S5 precheck demands obligation_refs, family `manifest`, outside PASSABLE: no word lifts it; text says "written by the marker, not by hand" and prints the placeholder `qa(obligations=["<plan obligation id>"])` | RM/scripts/s5_precheck.py:3765,3789-3791,3812 | present | - | B3a-producer | t31 |
| B3a-producer | fact | Only producer is manifest_from_tests.py, AST-based (ast.parse :311); `.spec.ts`/`typescript` do not appear (hits are only :15 and :311). Python-only marker | RM/scripts/manifest_from_tests.py:15,311 | present | - | B3a-reader | t32 |
| B3b | fact | Net: test_row_fields.py builds rows by hand (FULL dict, obligation_refs literal `{"obligation_id": "TS-1-O1", "obligation_hash": "h"}`) and pins the placeholder fix text (K4 (m), line 313) and that no word lifts it (:370-378) | RM/scripts/tests/test_row_fields.py:70,313,370-378 | present | - | P-A,P-B | t33 |
| B3c | fact | Passed because the tests pin the Python-marker design (HF2-12/EP1-18) with hand-written rows; no test has a TS test file go through manifest_from_tests -> precheck | RM/scripts/tests/test_row_fields.py:27 | present | - | B3b | t32,t33 |
| B3d | fact | Introduced 0.10.2 (2026-10-26), CHANGELOG:3106 ("written by the marker ... never by hand", HF2-12, EP1-18); row form printed 3108. test_row_fields.py is in `quarantine` (test-layers.json:9459) | RM/CHANGELOG.md:3106-3108; RM/scripts/tests/test-layers.json:9459 | present | - | - | t19,t34,t44 |
| B3e | fact | FND: marker cannot be produced for TS (FR-5, FR-11, P31); gate accepts hand value against own text; repair reaches the person; critic t-185 R1: row-fields-missing cannot be passed by any word | FND/20261112-pochinka-ne-vopros-cheloveku-dohodit-do-cheloveka.md:14-24,45-52 | present | - | - | t1 |
| B4a | fact | go on handling: TOKEN_MOVES maps `go on` -> go_on_as_is; seam_chosen executes it by code ONLY when the asked question carries a `block`/gap/judged cases; otherwise the words go to the conductor (LLM) | RM/scripts/no_move.py:40; RM/scripts/driver_machine.py:2341-2356; RM/scripts/driver_conductor.py:716-717 | present | - | - | t35,t36 |
| B4a2 | fact | Instance 1 (empty S5 scope) has no code-owned block, so by this design the conductor judges `go on`. Instance 3: pass_block over the placeholder line, via _exit_go_on; instance 4: repair_limit debt writer only inside _answer_repair_limit | RM/scripts/driver_dispatch.py:3814; RM/scripts/driver_machine.py:2359 | present | - | - | t35 |
| B4b | fact | Net: test_no_move_seam_k4s.py drives _exit_go_on with hand-written lines (`whole` = a case-identity sentence, `second` = "journal: entry 4 has no `ts`") and `waiver.py --block "some block the driver never saw"`; no line carries the real s5_precheck row-fields text | RM/scripts/tests/test_no_move_seam_k4s.py:195-225 | present | - | P-A | t37 |
| B4b2 | fact | The only test mentioning the s5_precheck placeholder pins it as correct (test_row_fields K4 (m)) | RM/scripts/tests/test_row_fields.py:313 | present | - | B3b | t33 |
| B4c | fact | Passed because go on is tested over synthetic lines; the real refusal text (with `<plan obligation id>`) never meets waiver.py's placeholder refusal; `row-fields-missing` is outside every PASSABLE set by design (s5_precheck.py:3812) | RM/scripts/s5_precheck.py:3812 | present | - | B3a-reader | t31,t37 |
| B4d | fact | _exit_go_on/exit-limit seam: C1-5d2 (driver-layers.json:585), version not searched -> not recorded. test_no_move_seam_k4s.py is in quarantine? it appears at test-layers.json:3033/3160 (keep section, before line 7016) - NOT quarantined. test_story_run_exit_limit.py IS quarantined (:9973) | RM/scripts/tests/test-layers.json:3160,9973 | present | - | - | t44 |
| B4e | fact | FND: chosen option not executed, 4 instances (FR-2, FR-7, FR-9, FR-57, AR-24, AR-25); proposal: options are closed tokens executed by code, conductor gets free text only | FND/20261112-dirizher-ne-ispolnil-vybrannyj-variant-go-on.md:14-17,49-54 | present | - | - | t1 |
| B5a | fact | take_question_answer docstring: "Nothing here calls the conductor (FR-48) ... the whole words go to the role's own session"; closed tokens -> register via record_question_words | RM/scripts/driver_dispatch.py:1707-1712,1758-1791 | present | - | B5a2 | t38 |
| B5a2 | fact | Gate A text promises the opposite: ANYTHING_ELSE_SENTENCE "goes to the assistant running this story, who turns it into one of these" | RM/scripts/gate_brief.py:1097 | present | - | B5a | t39 |
| B5a3 | fact | parse_choices reads only a WHOLE-line token `<qid>: <letter|not needed|until the report>` ("it may fail to see a choice") | RM/scripts/question_register.py:631-657 | present | - | - | t40 |
| B5b | fact | Net: the 240-char cut is PINNED. DECISION_CHARS_MIN=240; ladder cuts words to level 1; test N4 W6 feeds 24 KB of words and asserts each is cut at DECISION_CHARS_MIN and the brief goes over and says so | RM/scripts/brief_pack.py:60,4421-4456,4485-4497; RM/scripts/tests/test_brief_pack.py:2428-2440 | present | - | P-B | t41,t42 |
| B5b2 | fact | Free text at a threshold stop: tests that hit take_question_answer/record_question_words are 9 hits in 5 files (test_story_run_s0.py:1140 asserts "no question answered by a token" as the expected output) | RM/scripts/tests/test_story_run_s0.py:1140 | present | - | P-B | t43 |
| B5c | fact | Passed because tests assert the designed behaviour (free text -> role; words cut at level 1), the owner's 12.11 word reverses the design; no test states "free text reaches the conductor" or "words uncut" | RM/scripts/tests/test_brief_pack.py:2435 | present | - | P-B | t41,t43 |
| B5d | fact | Versions: DECISION_CHARS_MIN/dec_level/BRIEF_MAX_BYTES grep over CHANGELOG without -i found nothing -> NOT RECORDED (no valid negative). test_brief_pack.py is in keep (:277,:658,:1694); test_story_run_s0.py not located in quarantine | RM/scripts/tests/test-layers.json:277 | present | - | - | t44 |
| B5e | fact | FND: free answer must reach the conductor (owner word 12.11); brief must not cut the person's words (AR-24, AR-21) | FND/20261112-svobodnyj-otvet-na-paket-voprosov-ne-idet-dirizheru.md:25-28; FND/20261112-srezka-briefa-rezhet-slova-cheloveka.md:18-24 | present | - | - | t1 |
| B6a | fact | stage_review_exhausted hands the conductor a state; `lead` offers "accept with the gap, one more round on words you ground, or ask the person" and calls self.no_move(state) BEFORE the critic's finish | RM/scripts/driver_stage_plan.py:691-730 | present | - | B6a2 | t45 |
| B6a2 | fact | Open-move gate: _rework needs facts.running is False and rework_stages non-empty (REWORK_CLOSED: "a step of the story is still running"); _restart open while the dispatch is live. INFERENCE: at this state the critic dispatch is live, so rework is closed and restart (critic only) is open | RM/scripts/no_move.py:98-111,115-118,142-143,161-172 | present | - | B6a | t46 |
| B6b | fact | Net: every test of this seam replaces it with a lambda (`driver.stage_review_exhausted = lambda ...` in test_stage_critic_route.py:279,319; test_repair_route.py:542; test_story_run_refusals.py:3417). test_stage_review_person_pass.py calls the real one but only for the person-pass door | RM/scripts/tests/test_stage_critic_route.py:279,319; RM/scripts/tests/test_stage_review_person_pass.py:87 | present | - | P-C | t47 |
| B6c | fact | Passed because no test asserts which moves are offered to the person when the stage review is exhausted (R3 asserts only "the seam is asked, a driver accept closes, no move -> Person"). test_stage_critic_route.py header | RM/scripts/tests/test_stage_critic_route.py:10-11 | present | - | P-C | t47,t48 |
| B6d | fact | Person's go on over exhausted stage review: 0.11.0, CHANGELOG:67. Stage-critic route X2-7 version not searched. test_stage_critic_route.py and test_stage_review_person_pass.py are in `quarantine` (:9803, :9829) | RM/CHANGELOG.md:67; RM/scripts/tests/test-layers.json:9803,9829 | present | - | - | t44 |
| B6e | fact | FND: returned state has no move to the executor that can fix it (AR-25, FR-42); proposal: option "one more round to the tester" with its price | FND/20261112-s2-net-dveri-vernut-rabotu-testeru-so-slovami-kritika.md:13-17,19-23 | present | - | - | t1 |
| B7a | fact | Gate A is shown with "cannot start yet ... this gate should not have been shown yet" BY DESIGN. brief_lines prints the sentence, test pins it | RM/scripts/gate_preflight.py:6248-6252; RM/scripts/tests/test_gate_preflight.py:1598-1609 | present | - | P-A,P-B | t49,t50 |
| B7a2 | fact | Gate repair table GATE_REPAIRS has exactly 5 rows for gate A: unraised_questions, s5_runtime_probe, s5_reporter, case_versions, gate_decision; "No gate B row". No row for the empty-S5-scope or plan-row finding | RM/scripts/driver_gates.py:34-40; :900-918 | present | - | - | t51 |
| B7b | fact | Test input is a hand-written result dict (`{"gate": "A", "next_stage": "S5", "can_proceed": False, "by_class": {...}, "findings": [...]}`), not gate_preflight output | RM/scripts/tests/test_gate_preflight.py:1599-1605 | present | - | P-A | t50 |
| B7b2 | fact | Deferred question: register treats DEFERRED as kept open, not asked (question_register.py:86-87,441; gate_brief.py:4186). The controller refusal that required `Q19: <letter>` was NOT located (grep controller.py for `open question|unanswered|no answer`, -i: only help text); trail stops here | RM/scripts/question_register.py:86-87; RM/scripts/gate_brief.py:4186 | present | - | - | t52,t53 |
| B7c | fact | Passed because (a) the rehearsal-says-no case is tested as a printed sentence on a hand dict, not as a precondition of showing the gate; (b) not determined for the deferred-Q refusal (trail stopped) | RM/scripts/tests/test_gate_preflight.py:1609 | present | - | B7a | t50 |
| B7d | fact | Not recorded in CHANGELOG (not searched by field name). test_gate_preflight.py is in keep (:1847,:1915), not quarantined | RM/scripts/tests/test-layers.json:1847 | present | - | - | t44 |
| B7e | fact | FND: gate shown against its own rehearsal (FR-3, P22); decision not recorded while a deferred Q is open (FR-40, AR-25) | FND/20261112-gejt-a-pokazan-do-gotovnosti.md:13-15,19-21; FND/20261112-gejt-a-trebuet-otvet-na-vopros-otlozhennyj-do-otcheta.md:11-13,17 | present | - | - | t1 |
| B8a | fact | "did not answer when I checked it" is printed from pipeline `environment_pending`, set by S0 until "a probe that exits 0 ... or a word of the person"; text does not say which probe or why | RM/scripts/driver_sources.py:735-738; RM/scripts/driver_s0.py:2279-2283; RM/scripts/driver_machine.py:3930 | present | - | - | t54,t55 |
| B8a2 | fact | env_probe layer 1 prints "the login this project records was refused: <why>" for status failed; stand_access._local_login POSTs JSON to access.url and tries only the field-name pairs of references/login-body-fields.json | RM/scripts/env_probe.py:1118-1124; RM/scripts/stand_access.py:363-394 | present | - | - | t56,t57 |
| B8b | fact | login-body-fields.json holds no csrf/NextAuth form (grep -i `csrf|next-?auth|credentials` absent; control t58 finds `user_field` line 3 same file) | RM/references/login-body-fields.json | absent | - | - | t58,t59 |
| B8b2 | fact | Net: test_stand_access.py runs _local_login against an in-process BaseHTTPRequestHandler (:32-46) or a lambda `_open` returning (401, ...) (:520); 405 appears only as a C7b2 table row (:586) for a different path; test_story_run_stand*.py pin the "did not answer" text | RM/scripts/tests/test_stand_access.py:32-46,520,586; RM/scripts/tests/test_story_run_stand.py:40 | present | - | P-A,P-C | t60,t61 |
| B8c | fact | Passed because the login probe is tested against stubbed servers/lambdas whose shapes the test author chose; no test has a form-login stand (health ok, POST /login 405); "did not answer" text is pinned with a stub | RM/scripts/tests/test_stand_access.py:520 | present | - | P-A | t60,t61 |
| B8d | fact | login-body-fields.json: FB-3/OH3-10 per its _note (version not searched -> not recorded). test_stand_access.py (:9837), test_story_run_stand.py (:10045), test_login_body_fields.py (:8588), test_env_access_onboarding.py (:7925) are all in `quarantine` | RM/scripts/tests/test-layers.json:9837,10045,8588,7925 | present | - | - | t44 |
| B8e | fact | FND: onboarding wrote login-by-code impossible from a page 405 (AR-1, AR-3); probe states "did not answer" without a positive control (FR-41, FR-59, AR-28) | FND/20261112-onbording-zapisal-vhod-kodom-nevozmozhen-oshibochno.md:29-33; FND/20261112-proba-stenda-lozhno-govorit-ne-otvechaet.md:17-21 | present | - | - | t1 |
| B9a-reader | fact | selectors_verified: with no literal needs launch_check.runner_identity(argv)["selection"] AND earlier_proof(...)["state"]=="same_command"; execution_request refuses otherwise | RM/scripts/profile_contract.py:343-374 | present | - | B9a-producer | t62 |
| B9a-producer | fact | Probe writer stores row["argv"] = proved_argv with argv_digest(proved_argv) (onboarding_probe.py:357,366); reader hashes _one_test_argv(profile) (:209-211). Whether these two are the same argv in a real run is the finding's claim (`<test-file>` template); I did not execute it | RM/scripts/onboarding_probe.py:209-211,357,366,373-394 | present | - | B9a-reader | t63 |
| B9b | fact | Net: test_profile_contract.py builds the rehearsal record BY HAND from the same argv it asks about (`rehearsed(argv)` -> argv_digest(argv), file written by the test, lines 164-176) | RM/scripts/tests/test_profile_contract.py:164-176 | present | - | P-A | t64 |
| B9c | fact | Passed because record and query are made from one variable `pw` in the test; the real probe's writer never produces the record the reader is then asked about. test_onboarding_probe.py:211 tests earlier_proof on a record the test's own probe wrote, but against the fake_dotnet runner | RM/scripts/tests/test_onboarding_probe.py:211 | present | - | P-A | t64,t65 |
| B9d | fact | Not recorded (execution_request.py:295 refusal and selectors_verified not searched in CHANGELOG). test_profile_contract.py is in `quarantine` (:8994) | RM/scripts/tests/test-layers.json:8994 | present | - | - | t44 |
| B9e | fact | FND: honest probe never sets selectors_verified (regression, FR-1, FR-2, FR-5, FR-11, AR-13, AR-22); owner: run_suite must not refuse | FND/20261112-kontrakt-selektorov-nikogda-ne-proveren.md:11-21,23-27,40-48 | present | - | - | t1 |
| B10a | fact | Probe tool probe_by_code.py: grep -i `--grep|\.spec\.ts|playwright` gives only 3 comment lines about Playwright junit messages (:3079,:3082,:3134); no by-name selection for Playwright in that file. Selection form is data (`launch_check.runner_identity(argv)["selection"]`), table not read | RM/scripts/probe_by_code.py:3079,3082,3134 | present | - | - | t66 |
| B10a2 | fact | Brief says probes are the default (finding: brief lines 123/132); role-side producer of the probe model file is the role (P30). I did not read the critic charter/brief template for the probe-model-file instruction -> trail stopped | RM/agents/qa-code-critic.md | present | - | - | t67 |
| B10b | fact | Net: test_probe_by_code_languages.py mentions Playwright 24 times but runs a LANG_STUB runner with modes normal/pass_anyway/no_frames/lib_frames_first/wrong_line (:12, :55-58); stub, not a real Playwright selection | RM/scripts/tests/test_probe_by_code_languages.py:12,55-58 | present | - | P-A,P-C | t68,t69 |
| B10c | fact | Passed because the language test drives a stub runner with scripted outputs; no test runs the critic's probe flow end to end on a TS test; whether the Playwright by-name run works was not tested here: INFERENCE | RM/scripts/tests/test_probe_by_code_languages.py:55 | present | - | P-C | t68,t69 |
| B10d | fact | Not recorded (not searched). test_probe_by_code_languages.py is in keep (test-layers.json:3623), not quarantined | RM/scripts/tests/test-layers.json:3623 | present | - | - | t44 |
| B10e | fact | FND: critic closes review with no probes; conductor says the factory cannot produce them (FR-41, FR-48, AR-17, AR-29); class partly the language exception | FND/20261112-kritik-koda-ne-zapuskaet-proby.md:28-32,38-40 | present | - | - | t1 |
| f-audit | fact | A27 NO_MOVE_BASELINE is a shrink-only census of source SITES (file, qualname, class P/S/U, discriminator) where driver code builds a Person/Stop or runs a script outside Driver.no_move; 48 rows (lines 1666-1712), NO_MOVE_BASELINE_MAX = 55 (line 1714) | RM/scripts/audit_factory.py:1640-1649,1665-1714 | present | - | - | t5 |
| f-scope | fact | A27 parses ONLY story_run.py and driver_*.py ("never the other scripts"); the cap must equal the row sum (judged :2351-2355) | RM/scripts/audit_factory.py:1650-1651,2351-2355 | present | - | - | t5,t70 |
| f-B4 | fact | repair_limit is inside the baseline only as 4 sites of Driver._answer_repair_limit (builder:held_question, :1670); _exit_go_on 2 sites (:1672). It counts that a Person is raised through a builder, not that every option offered has an executor | RM/scripts/audit_factory.py:1670,1672 | present | - | P-E | t5,t7 |
| f-B2 | fact | `row-fields-missing` and the stage_done acceptance refusal are outside A27's reach: the tag lives in s5_precheck.py:3765, the refusal in acceptance.py/stage_done.py, neither in the driver set. Grep -i over RM for row-fields-missing finds only s5_precheck.py:3765 and test_row_fields.py | RM/scripts/s5_precheck.py:3765 | present | - | P-E | t6,t7 |
| f-other | fact | audit_factory.py checks A1-A7, A9, A11-A22, A24, A26, A27; none checks producer-vs-reader values (A22 role start load, A21 one owner per fact are different) | RM/scripts/audit_factory.py | present | - | - | t71 |
| f-AR22 | fact | AR-22 detector self-declares: test_field_producers.py covers handoff contracts only; test_stage_joints.py walks producer and demanded token per check ("Nothing walks reader -> producer for interview answers read from config.json or the strategy files") | RM/design/architecture.md:236 | present | - | P-F | t9 |
| f-joints | fact | test_stage_joints.py PINS = exit 8, detector 8, window 27: it checks that each check has a producer row and the demanded token is in a file the role receives; it never feeds a producer's output to a reader (docstring) | RM/scripts/tests/test_stage_joints.py:1-13,28-31 | present | - | P-F | t10 |
| f-AR24 | fact | AR-24 detector `test_words_doors.py`; "Open doors are queued as B-343, B-365 and B-387" | RM/design/architecture.md:250 | present | - | - | t9 |
| f-AR25 | fact | AR-25 detector test_state_exits.py enumerates states from source; test_stage_acceptance consumer / test_awaiting_state | RM/design/architecture.md:257 | present | - | - | t9 |
| g-loop | fact | Driver loop over stub roles exists: story_run_common.py STUB (fake `claude`) used by every test_story_run_*.py; stub answers come from per-test `control` dicts, not package forms | RM/scripts/tests/story_run_common.py:1-9,54-60,150-176 | present | - | P-D | t72,t73 |
| g-form-off | fact | Its seed() sets `cfg["handoffs"] = {"required": False}` ("the stub role writes a digest without filling a handover form") - handoff forms and form-based acceptance are not exercised in the loop tests, except a scenario named `the_form_is_required_of_the_driver_too` (comment only; not read) | RM/scripts/tests/story_run_common.py:194-201 | present | - | P-D | t73 |
| g-scenario | fact | scenario_walk walks recorded real stories (cart-1 recorded at package 0.10.6; local-1-0108, local-1-arm-b) only through DOORS = exit_gate, joint, start, gate, delivery; no driver loop, conductor, or stage_done acceptance | RM/scripts/tests/scenario_walk.py:35-47; RM/scripts/tests/test_scenario_cart_1.py:2-4 | present | - | P-A | t74,t75 |
| P-A | analog | Pattern: test input hand-written or recorded from an older producer, not the current one (B1,B2,B4,B7,B8,B9,B10) | RM/scripts/tests | present | - | - | t17,t28,t37,t50,t64,t69 |
| P-B | analog | Pattern: tests PIN the behaviour later reported (B3 placeholder fix text, B5 240-char cut, B5 free text to role, B7 "should not have been shown yet") | RM/scripts/tests | present | - | - | t33,t41,t50 |
| P-C | analog | Pattern: seam replaced by lambda in tests (B2 header :366 says this hid two earlier defects; B6 four sites) | RM/scripts/tests | present | - | - | t28,t47 |
| P-D | analog | Pattern: driver-loop tests turn the handoff form off (story_run_common.py:201) | RM/scripts/tests/story_run_common.py | present | - | - | t73 |
| P-E | analog | Pattern: A27 counts sites in 13 driver files; it cannot see states/refusal kinds or modules outside the driver set | RM/scripts/audit_factory.py | present | - | - | t5 |
| P-F | analog | Pattern: both producer-reader nets (field-producers, stage-joints) are name/token-presence registries over data files, not value flows | RM/design/architecture.md:236 | present | - | - | t9,t10 |
| q-quarantine | analog | 11 of the cited tests sit in `quarantine` (entered 2026-11-11, release_at_entry 0.10.9, cohort 8073673): row_fields, stage_acceptance_consumer, profile_contract, stand_access, story_run_stand, login_body_fields, env_access_onboarding, stage_critic_route, stage_review_person_pass, story_run_exit_limit, s3_s4_chain. Canon does not run them | RM/scripts/tests/test-layers.json:7016-7024,9459,9786 | present | - | - | t44,t76 |

## Trail
| tid | op | target | pattern / range | flags | result | control |
|---|---|---|---|---|---|---|
| t1 | glob | FND | `*.md` | — | found 25; FND/20261112-s5-pustaya-oblast-p-n-protiv-ts-n.md, 20261113-s7-petlya-dirizhera-na-prieme-s6.md | — |
| t2 | grep | RM | `CASE_PLAN_ROW_RE\|PLAN_ROW_RE` | content | found 13; scripts/contract.py:3052, scripts/s5_precheck.py:79 | — |
| t3 | read | RM/scripts/contract.py, RM/scripts/s5_precheck.py | contract.py:3606-3627; s5_precheck.py:3740-3765 | — | read both ranges | — |
| t4 | read | FND findings B1..B10 (10 files named in Objects) + batch not read | whole files | — | read 12 finding files | — |
| t5 | read | RM/scripts/audit_factory.py | 1620-1730, 2300-2410 | — | read both ranges | — |
| t6 | grep | RM | `row-fields-missing` | -i content | found 6; scripts/s5_precheck.py:3765, scripts/tests/test_row_fields.py:28,370,378,386 | — |
| t7 | grep | RM/scripts/audit_factory.py | `repair_limit` | -i content | found 1; audit_factory.py:1670 | — |
| t8 | grep | RM/references/stage-joints.json | `TS-1\|P-1\|plan_row\|Plan row` | -i content | absent | t9 |
| t9 | grep | RM/references/stage-joints.json | `obligation\|plan.row\|manifest` | -i content | found 8; stage-joints.json:26,40,173,337,857,864,877,884 | — |
| t10 | read | RM/scripts/tests/test_stage_joints.py | 1-36 | — | read test_stage_joints.py:1-36 | — |
| t11 | read | RM/design/architecture.md | 106-118, 233-259, 275-280 (greps AR-22/24/25/9/28) | — | read lines 236 and 278 whole | — |
| t12 | grep | RM/skills | `TS-\d\|TS-n\|"P-\d\|P-n\b` | content | found 1; skills/qa-story/phases/s5.md:317 | — |
| t13 | grep | RM/agents | `TS-\d\|TS-n\|"P-\d\|P-n\b` | content | found 1; agents/qa-code-critic.md:62 (provisional P-n, unrelated) | — |
| t14 | grep | RM/references | `TS-\d\|TS-n\|"P-\d\|P-n\b` | content | found 30 (limit); artifact-contract-plan.md:46, artifact-contract.md:63, slices/qa-test-strategist/handoff-keys.md:27 | — |
| t15 | grep | RM/handoffs | `TS-\d\|TS-n\|"P-\d\|P-n\b` | content | found 6; s3-strategist-to-designer.yaml:52, s4-designer-to-case-critic.yaml:50, s4-designer-to-runner.yaml:48 | — |
| t16 | grep | RM/references | `Plan row:` | content | found 4; artifact-contract.md:63, controller-api.md:119 | — |
| t17 | grep | RM/scripts/tests/test_s3_s4_chain.py | `Plan row:\s*TS-` | -i content | found 1; test_s3_s4_chain.py:52 | — |
| t18 | grep | RM/scripts/tests | `Plan row:\s*P-` | -i content | absent | t19 |
| t19 | grep | RM/scripts/tests | `Plan row:\s*(TS\|P)-` | count glob=*.py | count 33 (27 files) - control differs by flags (count not -i content) | — |
| t20 | grep | RM/CHANGELOG.md | `CASE_PLAN_ROW_RE\|PLAN_ROW_RE\|<P-n>\|stable id of a plan row\|plan row id` | -i content | absent | t21 |
| t21 | grep | RM/CHANGELOG.md | `obligation_refs` | -o content | found 4; CHANGELOG.md:1282,3106,3108 | — |
| t22 | grep | RM/scripts | `a reject needs\|does not say which dispatch of qa-runner\|LAST .inputs_read` | -i content | found 5; acceptance.py:1355,1357; stage_done.py:935 | — |
| t23 | read | RM/scripts/acceptance.py, RM/scripts/stage_done.py | acceptance.py:1331-1369,1559-1580; stage_done.py:880-1047 | — | read all ranges | — |
| t24 | read | RM/handoffs/s7-analyst-to-automator.yaml; s6-runner-to-analyst.yaml | whole; 1-40 | — | read both | — |
| t25 | grep | RM/handoffs | `stage_acceptance` | -i content | found 17; s2/s3/s4-case-critic-to-designer/s7-analyst-to-scribe/s8-scribe-to-gate-b/vocabulary.yaml (not s7-analyst-to-automator.yaml) | — |
| t26 | grep | RM/agents/qa-failure-analyst.md | `stage_acceptance\|acceptance` | -i content | found 1; qa-failure-analyst.md:28 | — |
| t27 | read | RM/scripts/brief_pack.py | 3490-3530; grep `stage_acceptance\|Reviewed dispatch` found 2 (:3524,:3525) | — | read | — |
| t28 | read | RM/scripts/tests/test_stage_acceptance_consumer.py | 44-56, 338-348; grep lines for failure_class etc. | — | read; lines 49-52, 341-345, 366 | — |
| t29 | grep | RM/scripts/tests | `stage_acceptance_from_form\|record_acceptance\|--acceptance` | count glob=*.py | count 45 (12 files) | — |
| t30 | grep | RM/scripts | `"tooling"\|'tooling'` | content glob={controller,driver_*,rework*,acceptance}.py | found 9; controller.py:257, driver_dispatch.py:2920, acceptance.py:1279 | — |
| t31 | read | RM/scripts/s5_precheck.py | 3764-3833 | — | read | — |
| t32 | grep | RM/scripts/manifest_from_tests.py | `ast\.parse\|\.spec\.ts\|typescript\|obligations=` | -i content | found 2; manifest_from_tests.py:15,311 | — |
| t33 | grep | RM/scripts/tests/test_row_fields.py | `\.spec\.ts\|typescript\|playwright\|obligation_refs` | -i content | found 20 (head); lines 10,27,54-70,147-167,309; no .spec.ts/typescript hit | — |
| t34 | read | RM/CHANGELOG.md | 3106-3108; 61; 7409-7412 | — | read | — |
| t35 | read | RM/scripts/driver_machine.py, RM/scripts/driver_conductor.py, RM/scripts/no_move.py | driver_machine.py:2335-2380; driver_conductor.py:700-735; no_move.py:96-178 | — | read; grep go_on_as_is found 30 | — |
| t36 | grep | RM | `go_on_as_is` | content | found 30 (head cap); no_move.py:40,166; driver_machine.py:2356 | — |
| t37 | read | RM/scripts/tests/test_no_move_seam_k4s.py | 195-245 | — | read | — |
| t38 | read | RM/scripts/driver_dispatch.py | 1690-1830 | — | read | — |
| t39 | grep | RM | `goes to the assistant running this story` | -i content | found 6; gate_brief.py:1097 | — |
| t40 | grep | RM/scripts/question_register.py | `def parse_choices` | content | found 1; question_register.py:631 | — |
| t41 | read | RM/scripts/brief_pack.py | 4395-4505 | — | read | — |
| t42 | grep | RM/scripts/tests | `DECISION_CHARS_MIN\|words at level 1\|level 1` | content glob=test_brief_pack*.py | found 12; test_brief_pack.py:2428-2440 | — |
| t43 | grep | RM/scripts/tests | `take_question_answer\|record_question_words\|ANYTHING_ELSE_SENTENCE` | count glob=*.py | count 9 (5 files) | — |
| t44 | grep | RM/scripts/tests/test-layers.json | `test_(row_fields\|stage_acceptance_consumer\|...\|env_access_onboarding)\.py` | -o content | found 38; quarantine = line >=7016: 7925,8588,8994,9459,9557,9786,9803,9829,9837,9973,10045; "quarantine" key at 7016, "keep" key at 35, "cohorts" at 6968 | — |
| t45 | read | RM/scripts/driver_stage_plan.py | 691-740 | — | read | — |
| t46 | grep | RM/scripts/no_move.py | (read 96-178, see t35) | — | read | — |
| t47 | grep | RM | `stage_review_exhausted` | -i content glob=!driver_stage_plan.py | found 25 (cap); tests/test_stage_critic_route.py:279,319; tests/test_repair_route.py:542; tests/test_story_run_refusals.py:3417; CHANGELOG.md:67 | — |
| t48 | read | RM/scripts/tests/test_stage_critic_route.py | 1-30 | — | read | — |
| t49 | read | RM/scripts/gate_preflight.py | 6225-6264 | — | read | — |
| t50 | read | RM/scripts/tests/test_gate_preflight.py | 1590-1620 | — | read | — |
| t51 | read | RM/scripts/driver_gates.py | 12-44, 1290-1335 | — | read | — |
| t52 | read | RM/scripts/gate_brief.py, RM/scripts/planning_contract.py, RM/scripts/controller.py | gate_brief.py:4160-4210; planning_contract.py:2736-2785; controller.py:9205-9245 | — | read | — |
| t53 | grep | RM/scripts/controller.py | `open question\|unanswered\|no answer` | -i content | found 3 (9304,9465,9816; none the refusal) | — |
| t54 | read | RM/scripts/driver_sources.py, RM/scripts/driver_s0.py | driver_sources.py:700-745; driver_s0.py:2262-2302 | — | read | — |
| t55 | grep | RM/scripts | `environment_pending` | content glob=!tests/** | found 15 | — |
| t56 | read | RM/scripts/env_probe.py | 1085-1135 | — | read | — |
| t57 | grep | RM/scripts/stand_access.py | `def login\(` | content | found; stand_access.py:478-520; `_local_login` :363-403 | — |
| t58 | grep | RM/references/login-body-fields.json | `csrf\|next-?auth\|credentials` | -i content | absent | t59 |
| t59 | grep | RM/references/login-body-fields.json | `user_field` | -i content | found 1; login-body-fields.json:3 | — |
| t60 | grep | RM/scripts/tests/test_stand_access.py | `405\|csrf\|next-?auth\|credentials` | -i content | found 4; test_stand_access.py:6,175,520,586 | — |
| t61 | grep | RM/scripts/tests/test_stand_access.py | `http\.server\|HTTPServer\|BaseHTTPRequestHandler\|def serve` | -i content | found 3; :32,35,46 | — |
| t62 | read | RM/scripts/profile_contract.py | 343-375 | — | read | — |
| t63 | read | RM/scripts/onboarding_probe.py | 205-222; grep argv_digest found 4 (:357,366,389,392) | — | read | — |
| t64 | read | RM/scripts/tests/test_profile_contract.py | 160-190 | — | read | — |
| t65 | grep | RM/scripts/tests | `selectors_verified\|command_changed` | count glob=*.py | count 27 (5 files) | — |
| t66 | grep | RM/scripts/probe_by_code.py | `--grep\|\.spec\.ts\|playwright` | -i content (via earlier combined pattern `def \|not_executed\|playwright\|\.spec\.ts\|--grep\|-g ` count 381; focused grep found :3079,3082,3134) | found 3 | — |
| t67 | grep | RM/agents/qa-code-critic.md | not searched for probe-model file text | — | not done | — |
| t68 | grep | RM/scripts/tests/test_probe_by_code_languages.py | `playwright\|\.spec\.ts` | count -i | count 24 | — |
| t69 | grep | RM/scripts/tests/test_probe_by_code_languages.py | `fake\|stub\|--grep\|mock` | -i content | found 8 (head); :12,55,57,58,64,87,143,144 | — |
| t70 | read | RM/scripts/audit_factory.py | headers via grep `^# --- A\d+` | content | found 6 (A20,A21,A24,A22,A27 + A1 sections) | — |
| t71 | grep | RM/scripts/audit_factory.py | `report\(\s*"A\d+[^"]*"` | -o content | found 29 report names A1..A27 | — |
| t72 | read | RM/scripts/tests/story_run_common.py | 1-60, 150-240 | — | read | — |
| t73 | grep | RM/scripts/tests/story_run_common.py | `stub\|fake_claude\|scripted\|canned` | -i content | found 20 | — |
| t74 | read | RM/scripts/tests/scenario_walk.py | 1-50 | — | read | — |
| t75 | read | RM/scripts/tests/test_scenario_cart_1.py; test_scenario_local_1_0108.py | 1-14 / 1-30; README.txt of stories/cart-1 | — | read | — |
| t76 | read | RM/scripts/tests/test-layers.json | 7014-7025, 9457-9463, 9784-9790 | — | read; quarantine rows shown | — |

## Forks
- Which of two designs is right at each of these decisions is NOT answered here: free text at a question stop goes to the role (driver_dispatch.py:1707-1712) versus to the conductor (gate_brief.py:1097 text, FND owner word); brief cut versus uncut (brief_pack.py:4456); one plan-row id form (TS-n in contract.py:3052 versus P-n in handoffs/s3-strategist-to-designer.yaml:52). The facts are in Objects (B1b-producer, B1b2, B5a, B5a2, B5b).
- Whether the quarantine (11 cited tests since 2026-11-11, entered at release_at_entry 0.10.9) is why these readers have no running net is a fact about the canon, not a cause established here: test-layers.json:7016.
this needs a decision from a tier above.

## Not done
- B7b: the controller/gate refusal that demanded an answer for a deferred Q19 was not located (trail t52, t53); (c) for that half of B7 is not established.
- B10: the probe-model-file instruction in the critic's brief/charter, and whether `launch_check.runner_identity` selection covers Playwright by name, were not read (t67, t66 only).
- (d): CHANGELOG versions searched only for obligation_refs/row fields (0.10.2), stage_review_exhausted go on (0.11.0), plan-row chain (0.3.0). Others are "not recorded" because not searched; DECISION_CHARS_MIN and others were searched without -i (t20 only had -i for plan-row names), so no valid negative is claimed for them.
- Absent claims where the control differs in flags: Objects B1c2 uses a count control (t19) for a -i content search (t18).
- B4 instances 2 (exit round with extra text) and 4 (repair_limit debt writer) were read only as far as t35/t37; the exact refusal text `began with round but carried extra text` was not located.
- Not read: the batch file batch-1-live-run-fvf.md, test bodies of test_story_run_exit_limit.py, test_conductor_doors.py, test_words_doors.py, test_state_exits.py (only names and header lines), and the scenario `the_form_is_required_of_the_driver_too`.
- Whether the quarantine section is the whole story for each test (cohorts section lines 6953-6988 also name test_brief_pack.py, test_conductor_doors.py, test_gate_preflight.py, test_words_doors.py) is unresolved: those also sit in `keep` rows, so I did not mark them quarantined.
