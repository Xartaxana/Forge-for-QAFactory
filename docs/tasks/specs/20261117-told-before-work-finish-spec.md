# Told before work: finish (draft, designer, t-953)

Status: DRAFT for Lead acceptance. Forks are returned (§8) and decided nowhere here; every card says which option it
follows (the recommendation), so a card is executable by recommendation until the Lead decides.
Parent (ACCEPTED, not redesigned here): `docs/tasks/specs/20261113-told-before-work-mechanism-spec.md` ("mech").
Row drafts: `20261113-told-before-work-wave0-rows.md` ("wave0", accepted t-480), `-part2.md`, `-part3.md`.
Read base: the root checkout `C:\QAFactory\forge-repo` (HEAD ebb0593e, 17.11), `PKG` = `ai-packages/qa-factory`. Counters
below are read from their carriers, not from the brief.

---

## §0 Measured state (one row per node of the scout's list)

Counters today (carriers read): `PKG/references/stage-joints.json:8126-8130` `told_ratchet` = hand_cards 12, legacy_legs 0,
unsited 119; `PKG/scripts/tests/fixtures/told-ratchet.json:4-5` rowless 25, untold 253; `test_stage_joints.py:927-932`
pins `UNSITED_CAP = 119` and `(audit().counts["unsited"], REAL["told_ratchet"]["unsited"], ...) == (119, 119, 119, [], True)`
(EXACT equality on the measured count: see edge EC-3 and fork F-1).

The 119 unsited rows by family (Grep `"check": "<family>:` over stage-joints.json, rows listed in §0.2):
controller 6, s5_precheck 11, manifest_put 14, validate_artifacts 42, handoff_check 21, planning_contract 12,
coverage_contract 2, first_look 11 = 119 (equals the T1r report §2 split 150 minus the 31 rows S-1a/S-1b sited).

Code-side siting today: Grep `refusal\("` over `PKG/scripts/*.py` finds literal sites only in execution_request.py (75),
run_suite.py (16), profile_contract.py (16), probe_by_code.py (12), manual_capture.py (11), red_sandbox.py (6),
manual_evidence.py (4), driver_s0.py, driver_stage_s8s9.py, stage_joints.py (1 each). A wider Grep
`\brefusal\(|import refusal|refusal,` over guard_pre_tool, stage_guard, hooklib, host_adapter, s5_precheck, manifest_put,
validate_artifacts, handoff_check, planning_contract, coverage_contract, check_delivery, gate_preflight, stage_done,
controller, no_move, first_look, brief_pack, story_step: 52 hits, every one read — all are prose/docstrings/local variable
names (e.g. `controller.py:5930 refusal, passed = ...`, `stage_done.py:923 print(refusal, ...)`), none a
`detector_verdict.refusal` call. Positive control: the same pattern family finds 75 sites in execution_request.py.

| node | what the code does today (carrier) | what remains | lowers |
|---|---|---|---|
| T3b | `brief_pack.py:417` `ahead_card` exists; `:4017` `FIRST_LOOK_DOD`, `:4019` `FIRST_LOOK_AHEAD` exist; `:2208` `_row_field_lines` exists; no `def dispatch_groups` in brief_pack/story_step/window_record/contract_slices, no `def row_field_lines` (Grep of the 6-name alternation; positive control: the same call found `ahead_card` at :417 and contract_slices :611); first_look.py has no `refusal(` site; 11 `first_look:put*` rows unsited (stage-joints :6796-7076) | the whole node (mech §5.1 T3b) | unsited 11 → 0 of its family (119 → 108 if alone) |
| T4 | no `refusal(` site in guard_pre_tool/stage_guard/hooklib/host_adapter (Grep above); its rows (PT/SG/HA) are already sited through A24 `check_of` and call-told (T1r-pages report §1: families `guard_pre_tool`, `stage_guard`, `host_adapter` listed, 73 entries marked) | site switch to `refusal(<§5.3 id>, ...)`, FV1-27's three instances, G-dispatch census relabels | `bare` → `tagged` of its units in told-ratchet.json (guard_pre_tool units :163-246 sum of bare 29; stage_guard T4 units :599-640 sum 22; hooklib.block 1); untold by the relabels; unsited unchanged (already sited) |
| T5 | ABSORBED in part: `validate_request` sites (§5.4 rows 10-19) by T1r-sites S-1a (`20261114-t1r-sites-s1a-report.md` site table); `run_suite` sites (§5.4 rows 34-37, `reparse`, `begin`, `recover`) and the `invalid_*` printers (§5.6) by S-1b (`-s1b-report.md` site table, `**told_fields(...)` printers) | `s5_precheck` 11 rows (manifest, row_fields, bindings, oracle, run_mapping, environment, obligations, plan, sides.declared, sides.settled, sides.placeholders: stage-joints :2922-3105, :3907-3961) and `manifest_put` 14 rows (:3401-3725, :3879): node **T5r** | unsited −25 |
| T5b | ABSORBED by S-1a: every MineRefusal site of mech §5.1 T5b is in S-1a's site table (`active_dispatch`, `case_entries`, `profile`, `profile_command`, `place_rows`, `stand`, `stand.probe`, `mine_call`, `scope`, `no_test`, `selector_args`, `sandbox`, `window_first`); S-1a "Left bare (E6)": `s6_close_from_state` (all), the fingerprint-build raise, helper-internal raises (B3) | residuals already carried by pile node FV2-43 (`batch-2-live-run-fvf.md:70`); the fingerprint-build site and the `profile.none` door text: fork F-5 | — (no unsited row of its own left) |
| T6 | `handoff_check.py` no `refusal(` site (2 Grep hits are docstrings :1319, :2809); 21 rows unsited (:5088-5738) | whole node | unsited −21 |
| T7a-1..7 | `validate_artifacts.py` no site (1 hit, docstring :2311); 42 rows unsited (:3989-5061: 40 function rows + `check_phase_json.context-manifest.json`, `.triage.json`) | whole node, re-cut into 3 (fork F-3) | unsited −42 |
| T7a-8 | wave0 item 2: all 8 functions "no row: code writer" (`wave0-rows.md:90-91`, closing table :427 "0 rows / 8 no row"), accepted t-480 (:392-410) | NO WORK for sites; whether its census units need a `["conductor"]` relabel is a closing-node measurement (§6 closing, step 3) | — |
| T7b | `planning_contract.py` no site; 12 rows unsited (:5764-6050); only quarantined tests: `test_planning_contract_not_planned.py` (test-layers.json :9079), `test_planning_policy.py` (:9087), both under `"quarantine"` (:7174+) | whole node; test place = fork F-2 | unsited −12 |
| T7c | `coverage_contract.py` no site; 2 rows unsited (:6076, :6102); `test_coverage_contract.py` quarantined (:7821) | whole node; `manual_current` stays a pointer (F-W3 (a)) | unsited −2 |
| T7d | wave0 §3c: "No row" (`check_delivery.main` is a verdict, census `["conductor"]`), accepted t-480 | NO WORK | — |
| T7e | wave0 §3d: "No row" (`gate_preflight.main` returns 0; findings reach the role only through `stage_done.run`, a conductor road), accepted t-480 | NO WORK | — |
| T7f | wave0 §3e: no role row; F-W2 (a) accepted: census relabel of the `stage_done` units to `["conductor"]`, "the edit rides in T7f"; `test_stage_done.py` quarantined (:9970) | census relabel only (judgment-census.json) | untold (measured; told-ratchet units `stage_done.py::*` :567-598 hold 41 bare) |
| T8 | mech §5.1 T8 "No work" | — | — |
| T9a | `controller.py` no site (11 Grep hits read, all prose/variables); 6 rows unsited (:2765-2896); `controller:s5_plan_gaps.rework_rows` re-pointed to qa-automator by K2 (`k10-paydown-k2-report.md` "Narrowed rows"); FV2-88 (scout over every `controller:*` row) still "ожидает" (`batch-2...md:115`) | whole node | unsited −6 |
| T9c | `no_move.moves_section` (`no_move.py:257-285`) renders moves only, no rows; no `"check": "no_move:…"` and no `stage_done:set` row in stage-joints.json (Grep of the check-id family alternation: 0 for no_move/stage_done/check_delivery/gate_preflight; positive control: the same call printed 12 `exit_gate:*` rows); BLOCKER: `stage_joints._producer_leg` (`stage_joints.py:691-704`) refuses a role with no `agents/<role>.md` (`role_exists` :404-405), `agents/` holds the 12 qa- files only (Glob), the conductor's file is `references/conductor.md` → a row with producer `conductor` is red today (inferred from the code read, not run: the card's first step measures it) | whole node + the producer-leg fix (fork F-4) | rowless/untold by relabels (measured); no unsited change (new rows are sited only if a literal lands: the card says) |
| T10 | Lead-tier; not started (scout t-941); axis 37 on `docs/SIBLING_MAP.md:628` is "A repeat stop"; `^## Axis (3[89]\|4\d)` finds nothing (control: `^## Axis` form found 37 at :628) → 38 is the next free number | §5 | — |
| T1r-cards | spec `20261114-told-before-work-t1r-cards-spec.md` + plan critic UNFIT (t-703); T1r merged to main (batch-2 "Ход" t-838: pages T1r t-830, K1a 9c5db6f1, K2 442ae9de, KR 9116d50a, all in main 9198b363) | §2: B1 changed, B2/B3 open, B4 closed → NOT dispatchable to a builder today; a designer redraft is | hand_cards 12 → 0 |
| K1b | pile node FV2-79 (`batch-2...md:106`), "ожидает", depends on K1a/K2/KR in main (done) and "канон пачки с ними" (BATCH CANON with them: not established, §9) | §6 card | `native_headroom.qa-code-critic` deleted or lowered |
| closing | not started | §6 card | told_ratchet final values; told-ratchet.json `rowless`/`untold` to the measure |

### §0.1 Data the cards rely on (verified)
- Keep vs quarantine (`PKG/scripts/tests/test-layers.json`, sections `keep` :36-7119, `quarantine` :7174+): keep —
  test_validators.py (:6575), test_handoff_values_refusal.py (:2377), test_s5_precheck.py (:4894),
  test_s5_precheck_sides.py (:4928), test_manifest_put_merge.py (:2985), test_controller_doors.py (:884),
  test_conductor_doors.py (:672), test_no_move_seam_c26_g27_f2.py (:3290), test_s3_strategist_rounds.py (:4778),
  test_s5_plan_controller.py (:4840), test_brief_pack.py (:288), test_window_record.py (:6991), test_first_look.py (:6743),
  test_first_look_wiring.py (:6839), test_story_step.py (:6315), test_run_forms.py (:4676), test_hooklib_scan.py (:2471),
  test_guard_dispatch_budget_and_logs.py (:2205), test_judgment_census.py (:2798), test_detector_verdict.py (:1250),
  test_ahead_cards.py (:56), test_contract_slices.py (:852), test_stage_joints.py (:5378), test_check_delivery.py (:531),
  test_gate_preflight.py (:1923), test_execution_request.py (:1499); quarantine — test_coverage_contract.py,
  test_planning_contract_not_planned.py, test_planning_policy.py, test_stage_done.py, test_story_step_prompt.py (:10300),
  test_story_step_card.py (:10239), test_ahead_cards_rules.py (:7224), test_brief_pack_roles.py (:7307).
- Slow (`PKG/scripts/slow_tests.json`, over 10 s, builder never runs them — "judged by the batch canon"):
  test_handoff_values_refusal 78.4, test_s5_precheck 28.5, test_judgment_census 33.3, test_run_forms 16.0,
  test_hooklib_scan 20.8, test_guard_dispatch_budget_and_logs 96.9, test_conductor_doors 53.0,
  test_no_move_seam_c26_g27_f2 28.3, test_s3_strategist_rounds 15.9, test_s5_plan_controller 42.7, test_brief_pack 34.6,
  test_window_record 87.4, test_stage_joints 67.6, test_execution_request 20.9, test_check_delivery, test_gate_preflight,
  test_role_commands 43.1, test_stage_guard 74.5. NOT in the slow list (runnable): test_validators, test_manifest_put_merge,
  test_controller_doors, test_detector_verdict, test_first_look, test_first_look_wiring, test_contract_slices,
  test_ahead_cards, test_role_load, test_role_rules, test_s5_precheck_sides.
  Consequence: T6, T7b, T7c, T4, T9c and the s5_precheck half of T5r have NO fast keep file of their own → fork F-2.
- A site is "sited" when a `detector_verdict.refusal("<literal id>", ...)` call stands in code (S-1a: "Literal ids";
  `stage_joints.py --check` counted 150 → 124 → 119 as literals landed). `told_ratchet.unsited` is a ceiling for
  `stage_joints.py --check` (S-1a: stored 150, measured 124, "clean"), but `test_stage_joints.py:928-932` pins the
  measured count EXACTLY (EC-3).

### §0.2 The unsited row ids per node (verbatim from stage-joints.json)
- T5r s5_precheck: `manifest`, `row_fields`, `bindings`, `oracle`, `run_mapping`, `environment`, `obligations`, `plan`,
  `sides.declared`, `sides.settled`, `sides.placeholders`. manifest_put: `colliding_ids`, `novelty`, `base_outcome`,
  `obligation_hash`, `helper_rows`, `provisional`, `unknown_obligation`, `then_remainder`, `retract`, `critic_approval`,
  `assertion_line`, `ghost_rows`, `revision`, `expectation_changes`.
- T6: `field.blank`, `field.value`, `field.max_len`, `required_rows`, `required_rows.owed_by_verdict`,
  `required_rows.null_word`, `tried`, `blocked_problem`, `findings_tooling`, `claims`, `null_outcome.{repairs,verdict,
  names,report,failures,listing}`, `values_file`, `values_apply`, `cli`, `binding`, `investigation`.
- T7a: the 40 function ids of mech §5.2 T7a-1..7 (every `validate_artifacts:check_*` row of :3989-5008) and
  `check_phase_json.context-manifest.json`, `check_phase_json.triage.json`.
- T7b: `plan`, `contradictions`, `branches`, `branches.new_questions`, `fence.plan_row`, `fence.r_column`,
  `fence.candidate_defects`, `fence.waiting_branch`, `regression`, `targets`, `requests`, `plan_json`.
- T7c: `obligations`, `obligations.observation`.
- T9a: `s3_plan`, `s5_plan_accept`, `s5_plan_gaps`, `s5_plan_review`, `code_review_receipts`, `s5_plan_gaps.rework_rows`.
- T3b: `first_look:put.{null_reason, walk_open, inputs_current, input, rows, rows.row, rows.path, rows.api, rows.auth,
  rows.locator, rows.list}`.

---

## §1 Architecture, owners, census (rule 10, AR-29, P27) — common to every package card

| AR | kept how | change check in every package DoD |
|---|---|---|
| AR-9 every refusal names what it expected and a door | the Record carries the row's `expected`/`door`; the transport prints them after the unchanged text | per-site test row "the site writes this id" + the transport line |
| AR-10 a check's requirement reaches the role before the work | rows already page-told (T1r); siting lets the refusal repeat them | `contract_slices.py --check` clean |
| AR-13 a fact with a reader is read through it | `stage_joints.told_text` via `refusal()` only; no node opens stage-joints.json itself | critic: no second reader in the diff |
| AR-14 one artifact one writer | stage-joints.json rows written only by T9c (its conductor rows), T1r-cards and the closing; `told_ratchet.unsited` + the K12 pin by the wave integrator (F-1) | owns lists |
| AR-18 one output shape | `told` key appended LAST to JSON lines (S-1b form), `check:` line last on text (C9) | byte-identity rows |
| AR-20 shrink-only ratchets | every ratchet move named (key, old → new, reason); no raise anywhere except K1b/T1r-cards per F-6 | ratchet rows in the report |
| AR-22 field read ↔ producer | `records`/`told` have readers (S-1b printers) | — |
| AR-29 code judges data | no node adds or moves a judgment: a site gets an id; a census relabel changes reach, never the class | `test_judgment_census.py` (slow, canon) |
| AR-15/AR-17 (T9c only) one survivor, one seam | conductor rows enter only through `no_move.moves_section` (one caller `driver_conductor.py:684`, Grep) | T9c rows |

Checks added or altered, owner and census class: NO node adds a check. Siting nodes attach an id to an EXISTING refusal
(owner: data, class unchanged per unit). Census relabels (T4b, T7f, T9c, T9a) change `roles` of existing units (owner:
data — who the unit reaches; class unchanged; a dense `blocking_per_role` ceiling that drops follows the measure, as in
the T1r-pages fix round §2). T9c adds a render section (data, not a check). Every card: "census: no new blocking unit".

Commit lines: the form is `tools/architecture_gate.py` (not copied here). Every package card prescribes
`architecture: <its AR list> -- <how kept>` and `judgment: none -- <the node attaches row ids to existing refusal sites / relabels reach; no check added or moved>`.

FR walk per package card: A (FR-1/2 text unchanged, expected/door added; FR-59 unreadable row → the factory-defect
sentence), C (FR-14 output shape additive, FR-38), D (FR-16 literal ids at the site), G (FR-30, FR-32, FR-54);
B, E, F: one line "not touched" each. T9c adds B: n/a (the conductor prompt is not text a person reads; FR-6 untouched).

---

## §2 T1r-cards: the four blockers of t-703 against today's main

| blocker | state today | carrier | fix where open |
|---|---|---|---|
| B1 F-4 not executable (K10 red, "over H" = "crosses the ceiling") | CHANGED, not gone. K10 is green on main by named baselines: KR set `native_headroom` qa-automator none → 79,909, qa-code-critic none → 72,828 (TEMPORARY until K1b), qa-test-strategist 46,008 → 53,552; `contract_slices.py --check` exit 0, no K10 line | `20261114-k10-paydown-kr-report.md`; K2 report (U after K2) | C-9 is rewritten: "K10 green on entry (KR); this node's growth per role over its stored baseline is ZERO — any growth is a STOP with the role and bytes named (no raise)" — owner/Lead fork F-6. Reason: the card text is already on every page under `### Not yet in rows` (critic B1), so the move into rows is near size-neutral; a raise would move automator closer to the Codex refusal (KR "Price": 14,491 chars of project files left). The code-critic baseline must SHRINK under K1b, never grow here |
| B2 M1 appends claims the body does not check (AR-29) | OPEN. Nothing in K1a/K2/KR touched the cards spec text; the five over-claims (br-2, cd-3, rt-5, rt-1, ds-4) and the unchecked "V by §5.2 sentence" segments stand | critic t-703 B2; cards spec §3 | a designer body pass (NOT this draft: the bodies were not re-read here) with the critic's clause table as its start: br-2 "severity DERIVED" → K; cd-3 → K; rt-5 drop "in order"; rt-1 parent clause → X sub-id `exit_gate:witness_errors.requirements-tester` (M2, row sentence-less); ds-4 second sentence → K (check_delivery has no row: wave0 §3c); M1 rewritten "append only the clauses the target body checks"; plus the sibling the critic queued: the T1r sentence of `validate_artifacts:check_case_form` claims "inherits defect_class and basis from its plan row" (mech :419) — the redraft owns that row's correction (stage-joints.json is T1r-cards' file, not T7a's) |
| B3 rule P not deterministic | OPEN | critic t-703 B3 (rule-P simulation) | the redraft replaces rule P by a designer-placed table: ts-1 → M1 `planning_contract:plan`; ts-2 → M1 `coverage_contract:obligations.observation`; au-5 → M1 `s5_precheck:manifest`; au-6 → M1 `s5_precheck:oracle`; ra-1 → K; ts-3, ck-2, ck-4, sc-3, rt-4, ru-1, ra-3 → body reads owed (critic's starting points); rule "an existing family row always beats a new function id" |
| B4 gate cannot be passed | CLOSED: T1r (with T1r-pages, K1a/K2/KR) is in main; `contract_slices.py --check` exit 0 (KR witness) | batch-2 "Ход" t-838; KR report | the node branches from main |
| X1-X9 | X1: A4/A5 now: pages regenerated by T1r/T1r-pages/S-2, hand_cards 12, legacy_legs 0, unsited 119, gaps 4 (S-2 witness); X2: the five quarantined F19 files stay out of owns (two re-confirmed here: test_ahead_cards_rules :7224, test_brief_pack_roles :7307; the other three by the critic, not re-read); X3-X9 open, text fixes for the redraft | — | redraft |

Verdict for today: T1r-cards is NOT dispatchable to a builder from text that exists; a designer redraft (B2/B3 body pass +
X3-X9 + the C-9 rewrite) is dispatchable now (fork F-7). Card for the redraft: §6 "T1r-cards-R".
Conflict to keep in the redraft: T1r-cards §4 lands a row `execution_request:fingerprint` for the `--mine` fingerprint
BUILD failure, but `execution_request:fingerprint` is already the id of `validate_request`'s `fingerprint_components`
check (mech §5.4 row 15; S-1a site table "fingerprint | F"). One id would name two requirements (E7 forbids two rows of
one id) → fork F-5 (recommend sub-id `execution_request:fingerprint.build`).

---

## §3 Waves (cap 6 writing builders; designers/critics/scouts outside the cap)

Shared-file rules for this finish (in addition to mech §7):
- `judgment-census.json` (rows and the dense `ratchet.blocking_per_role` ceilings — shared lines): T4b, T7f, T9c, T9a and
  the pile nodes FV2-26, FV2-89 all edit it. Work may run in parallel; MERGE order is serial: T4b → T7f → T9c → T9a
  (→ FV2-89 → FV2-26 when they are taken). Each later node merges main into its tree before its census edit and
  recomputes the ceilings from `test_judgment_census.py`'s own message (the T1r-pages fix-round pattern). Fork F-9.
- `validate_artifacts.py` + `test_validators.py`: the three T7a nodes own disjoint function lists (D-0048); merge order
  T7a-A → T7a-B → T7a-C, each resolves `test_validators.py` by keeping both sides' rows.
- `test_detector_verdict.py` (if F-2 (b)): each node owns ONE new function named in its card; FV2-80/83/84/44 (pile)
  own `refuse_cases` / others — disjoint.
- `stage-joints.json` `told_ratchet.unsited` and the K12 pin `test_stage_joints.py:927-932`: written ONLY by the wave
  integrator at each merge (F-1 (a)); no siting node edits them.
- Hot files of mech §7 against OTHER piles: the taken batches today (header "статус: в работе", Grep): github-move/3,
  onboarding-hooks/4-8, onboarding-forge/1-4. Whether their owns name `hooklib.py`, `stage_guard.py`, `controller.py`,
  `gate_preflight.py`: NOT ESTABLISHED (a Grep counted hits of the hot-file alternation in those files — onboarding-forge
  batch-1 11, -2 13, -4 10, onboarding-hooks batch-5 6, -8 5 — without reading which file each hit names). Lead before
  dispatch of T4b and T9a: `python -B tools/piles.py check --all` (check (б), zones of batches in work) and a Read of the
  "Пишет в" column of those batches.

| wave | nodes (parallel) | writers | why this grouping | counter |
|---|---|---|---|---|
| 0 (Lead, now) | M9 experiment (§4); F-1..F-9 decisions; designer T1r-cards-R (not a writer); scout FV2-88 (`controller:*` rows vs roles, not a writer) | 0 | M9 gates T3b; F-1/F-2 change every DoD | — |
| A (now) | T4a, T5r, T6, T7a-A, T7b, T7c | 6 | disjoint files; none edits judgment-census.json or stage-joints.json | unsited 119 → 119−25−21−14−12−2 = 45 (T4a: bare only) |
| B (after A merges) | T4b, T7a-B, T7a-C, T3b (if M9 done), T9a (work; merges after T9c), K1b | 6 | T7a-B/C after T7a-A on the shared file; T4b first on the census | unsited 45 → 45−10−18−11−6 = 0 |
| C | T7f, T9c (census order T4b → T7f → T9c → T9a), T1r-cards builder (after its redraft is accepted and re-critiqued) | 3 | census serial; T1r-cards owns stage-joints rows + pages | hand_cards 12 → 0 |
| D | closing (1 builder) | 1 | final values | told_ratchet final; rowless/untold to the measure |

Nodes runnable in PARALLEL today from this text alone (DoD item): T4a, T5r, T6, T7a-A, T7b, T7c — six (T7b/T7c on F-2's
recommendation; if the Lead picks F-2 (a) instead, both still run, their rows are written and judged by the canon).
Sequential and why: T7a-B/C after T7a-A (one file, one test file); T4b/T7f/T9c/T9a (census, merge serial); T3b after M9
and after T1r-cards on `test_ahead_cards.py` (T3b deletes `brief_pack.ahead_card`, which test_ahead_cards' brief rows
call — T3b takes those rows in its owns if it lands first, see its card); closing after all.

---

## §4 M9 — the experiment the Lead runs first (CLAUDE.md pt.6a)

What: does a page attached as an appended system prompt, and a line of the first user prompt, survive `claude -p --resume`?
(mech E22, T0 M9, §7 "driver resumes"; still owed per mech :772.)

Procedure (one machine, one role file, no factory run; flag names are an ESTIMATE — check `claude --help` first):
1. `claude -p --agent qa-runner --append-system-prompt-file <abs path of PKG/references/slices/qa-runner/handoff-keys.md> --output-format json "Remember the code word TELL-17. Reply OK."` → record `session_id` from the JSON.
2. `claude -p --resume <session_id> --output-format json "Quote verbatim the first line that starts with '- [' in your system instructions, and the code word from my first message."`
3. Record both answers verbatim in `docs/tasks/specs/reports/20261117-tbw-m9.md` (the carrier; a journal line names it).

Outcomes and what T3b does:
| page line quoted | code word quoted | meaning | T3b |
|---|---|---|---|
| yes | yes | both survive | as written (groups line in `story_step._prompt` outside the `not resumed` branch; page delivery on resume needs nothing) |
| no | yes | appended system prompt lost on resume, conversation kept | T3b as written (the groups LINE still rides the prompt); plus a NEW driver-owner node: role resumes pass `system_file` (mech E22) — Lead opens it; the claim "the role sees its page before the work" is limited to first dispatches until it lands |
| yes | no | odd (conversation lost) | stop: Lead re-plans T3b; nothing dispatched |
| no | no | resume carries nothing | T3b's prompt line must be built for every resumed prompt (it already is: outside the branch) and the `system_file` node above is mandatory before any claim |
The experiment is destructive to nothing; a refusal of the CLI to take a flag is a miscall (pt.6), not an outcome.

---

## §5 T10 — Lead carrier edits (Lead-tier, not a builder card)

Axis number: **38** (free: `^## Axis (3[89]|4\d)` finds nothing in `docs/SIBLING_MAP.md`; the highest is 37 at :628,
"A repeat stop"; `[Aa]xis 38` over `docs/` finds no file — positive control of the same form `[Aa]xis 37` finds 34 files).
NOT established: whether another in-flight spec also proposes "the next axis" — at the T10 commit the Lead re-reads the
map's tail.

Edits:
1. `docs/SIBLING_MAP.md`: new `## Axis 38 — A check's requirement: one row <-> the constructor `refusal()` <-> the key page / the conductor section <-> the in-process transports (`told_fields`, `spoken`, `block`, `deny`, `refuse`)`; touch axes 17 (Record attributes, `spoken`, `told_fields`), 18 (the told counters, `native_headroom`), 28 (the page + the conductor section as told render sites, `told_line`), 32 (census relabels of T4b/T7f/T9c/T9a).
2. The mech spec §5.1 T10 row and §6 (b) say "axis 37" for this axis; the T1r-sites / T1r-pages specs each carry one
   "axis 37" mention (Grep counts 1 each; which meaning — not read) — re-point to 38 where they mean this axis.
3. `PKG/design/architecture.md` AR-10 Detector/Gap and AR-9 change check (package commit: the architecture gate lines).
4. `docs/tasks/critic-diff-brief.md` J1/J2 (sentence truth, swap road) and question 9 naming the new ratchets (`unsited`, `hand_cards`, `legacy_legs`, `rowless`, `untold`, `native_headroom`).
5. `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`: one check "a row sentence claims more than its body" (critic t-703 B2 class) with the J1 detector.
6. `PKG/design/factory-rules.md` FR-38 *Check:* names `stage_joints.py --check` + `contract_slices.py --check`.
7. P1-b C11 (owner data, class xref) calls `rows_for` (mech §7) — Lead checks its node exists in the P1-b finish spec.
8. Mechanism commit: the four questions with the axis block (now 38 axes) and `tier:` line (CLAUDE.md rule 10).

---

## §6 Dispatch cards

Common to every package card (written once, each card says "common" where it applies):
- given (common): `PKG/design/factory-rules.md` whole; `plans/builder-rules.md`; this file §0, §1, §3 and the card;
  mech §5.1 row of the node and its row table (§5.2-§5.5); `docs/TESTING.md`; `PKG/scripts/detector_verdict.py`
  (`refusal`, `spoken`, `told_fields`, `Record`); `PKG/scripts/stage_joints.py` (`row_for`, `told_text`, `told_line`);
  the S-1a and S-1b reports (`docs/tasks/specs/reports/20261114-t1r-sites-s1a-report.md`, `-s1b-report.md`) as the
  worked pattern of siting (wrapper form, B3 rule, byte-identity proof, negative control).
- non-goals (common): `stage-joints.json` (rows and `told_ratchet`), pages, `role-load.json`, `role-rules.json`,
  `inject-map.json`, `test_stage_joints.py` (the K12 pin: F-1), any refusal TEXT change, a new test file, quarantined
  tests, running slow files, CI, mutations.
- edges (common, each with its invariant):
  - EC-1 byte identity: the printed text / `str(exc)` / REJECT block of every site is byte-identical to the pre-change
    file; the row's expected/door ride only through the transport (Record → `spoken`/`told_fields`/`block`). Invariant:
    a reader that parses the old text (driver `KNOWN_REFUSALS`, `exit_gate` `detector_errors`, `_verdict_rule`) never
    sees a changed line. Expected value: the OLD file's output, captured from a byte copy before the edit (S-1a "Old
    text"), never the new code's output.
  - EC-2 multi-caller helper (S-1a B3, binding): a site inside a helper with more than one caller carries NO literal id;
    the id goes on the caller that knows the requirement. Invariant: one id never names two requirements; a caller that
    cannot tell the helper's refusals apart leaves it bare with a named E6 reason.
  - EC-3 counters: `stage_joints.py --check` prints the measured `unsited`; the node does NOT edit `told_ratchet.unsited`
    or `test_stage_joints.py:927-932` (F-1 (a)); its report states "unsited <before> → <after>, rows sited: <ids>".
    Invariant: the ceiling never rises; the exact K12 pin is the integrator's (it goes red in the canon until the
    integrator commit — named, not a defect of the node).
  - EC-4 unreadable or absent row: `row_for` → `(None, why)` → `refusal()` prints the existing factory-defect sentence
    (S-1a row `unreadable`). Invariant: an unknown row is never a pass and never a crash (FR-59, AR-28).
  - EC-5 empty / several problems: no problem → no Record, output unchanged; several → one Record per problem, the
    exception carries `records` (S-1a form) and a JSON printer appends `told` LAST (S-1b form). Invariant: the first
    problem's text keeps its place; no problem is dropped from `records`.
  - EC-6 POSITIONAL: a `told` key is the LAST key of a JSON line; a text transport prints `expected:`/`door:` after the
    problem and `check:` last (C9). Invariant: every key/line a parser reads today stays where it is.
  - EC-7 TEMPORAL: the rows exist already (T1r) and are page-told; after the node they are sited, still page-told
    (`call_told_families` is untouched: s5_precheck, manifest_put, validate_artifacts, handoff_check, planning_contract,
    coverage_contract, controller, first_look are NOT listed — stage-joints :8131-8138). Invariant: no row leaves a page
    in a siting node.
  - EC-8 sentence vs body: if a row's sentence claims more than the body checks (critic t-703 B2 class), the builder does
    not edit the row (non-goal); it names it in the report under "rows that over-claim" for T1r-cards-R. Invariant: no
    sentence is reworded by a builder.
- DoD (common): (1) `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>` — run every
  printed file that is not in `slow_tests.json` and not quarantined, each alone; list the slow ones as "judged by the
  batch canon"; (2) `python -B ai-packages/qa-factory/scripts/stage_joints.py --check` — clean, summary line with the
  lowered `unsited`; (3) `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`; (4) a negative control:
  one wrapped site turned bare on a byte copy → the node's own test row FAILs and `unsited` rises by 1; restore by `cp`,
  hashes equal (S-1a form); (5) "census: no new blocking unit"; (6) the report holds the site table (function |
  fragment | id or E6 reason (class) | test row | proof F/W/N), the FR walk, the changelog fragment
  `PKG/changelog.d/<node>.md` (one English ASCII bullet), and the verbatim witness.
- siblings (common): axis 17 (Record shape), axis 34 (one road: `refusal()` only), axis 38 (T10); the bare remainder of
  each file goes to the report's E6 list classed (code)/(role); a (role) residual is a question to the Lead.

### Card T4a — guard_pre_tool + host_adapter sites (wave A)
given: common; mech §5.3 rows 1-24, 32-39 and wave0 item 8a (host_adapter corrections, "On Codex" in the sentence);
`PKG/scripts/guard_pre_tool.py` (the functions below), `PKG/scripts/host_adapter.py` (`role_policy` :567-625),
`PKG/scripts/hooklib.py` (`block` — read only), the A24 entries `PKG/scripts/refusal_registry.py` (`check_of`).
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\guard_pre_tool.py (size_check, runs_check, git_config_check, logs_check, plugin_read_check, big_read_check, case_store_check, handoff_write_check, handoff_values_check, artifact_rewrite_check, plan_write_check, manifest_write_check, owner_check, window_file_check, writes_check, human_word_check, config_write_check, stand_record_write_check, main, walker_refusal, _guard)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\host_adapter.py (role_policy)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_detector_verdict.py (new function `tbw_t4a_sites` only — F-2 (b))
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\tbw-t4a.md
non-goals: common; `hooklib.py`, `stage_guard.py`, `inject_context.py`, `judgment-census.json` (T4b); the G-dispatch units.
items:
| # | what | expected | test (place; expected from) |
|---|---|---|---|
| 1 | each role-facing block site passes `refusal("guard_pre_tool:PT-…", <same text>)` to `hooklib.block` | output: old text + the row's expected/door lines (T2's `block(Record)`) | `tbw_t4a_sites` row per §5.3 id 1-24 "the site writes this id" (expected from: §5.3 row) |
| 2 | FV1-27 instances first: `playwright test` (`guard_pre_tool.py:322-341`, row 2), values file (`:1138-1168`, row 11) | the refusal prints row 2 / row 11 expected/door | row each (expected from §5.3 rows 2, 11) |
| 3 | host_adapter refusal dict carries the HA row id (rows 32-39) | dict text unchanged ("FACTORY HOST POLICY: …") + `check` | row per HA id (expected from wave0 8a corrected rows) |
| 4 | no-row sites (§5.3 "No row (E5)") stay bare | unchanged | report E6 list |
edges: common; E-T4a-1 a row whose `when` is `shell` and a no-shell role: the site still carries the id (the row is
not shown on that role's page — K2/`role_has_bash`); invariant: a no-shell role's page never shows a shell row
(FV1-27 promise). E-T4a-2 sub-ids (C14) where one function holds two rows (`handoff_write_check`: rows 8, 9, 10);
invariant: each sub-id names one requirement.
DoD: common, with `--witness-for scripts/guard_pre_tool.py scripts/host_adapter.py scripts/tests/test_detector_verdict.py`;
fast: `python -B ai-packages/qa-factory/scripts/tests/test_detector_verdict.py`; judged by the batch canon:
test_run_forms, test_hooklib_scan, test_guard_dispatch_budget_and_logs (slow). Counter: told-ratchet units of
guard_pre_tool (bare 29 → the measure, reported per unit).
siblings: common; T4b (same family, other files); FV1-27 closes on rows 2, 11, 25 (25 is T4b).
architecture: AR-9, AR-10, AR-13, AR-18, AR-29 -- ids at existing hook refusals; text unchanged.

### Card T4b — stage_guard + hooklib sites, G-dispatch relabels (wave B, census first)
given: common; mech §5.3 rows 25-31, wave0 item 8b (row 28 split `stage_guard:commit.pathspec`/`commit.manifest`,
row 31 pointer to 22), §2.8 G-dispatch list (mech :509-512); `PKG/scripts/stage_guard.py`, `PKG/scripts/hooklib.py`,
`PKG/scripts/tests/fixtures/judgment-census.json`.
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\hooklib.py (shell_opaque_found, _opaque_member, _DOOR_*)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\stage_guard.py (rule_typed_runner, _judge_slice, check_command, check, check_dispatch, _check_exploration, check_resume, _unidentified_resume)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (rows of the G-dispatch units of stage_guard, inject_context, native_context, codex_roles: `roles` → ["conductor"] with a `note`; the dense ceilings they move)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_detector_verdict.py (new function `tbw_t4b_sites` only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\tbw-t4b.md
non-goals: common; `block`/`deny` (T2's); guard_pre_tool/host_adapter (T4a); `inject_context.py` code (census relabel only).
items: (1) role-facing `deny` sites → `refusal("stage_guard:SG-…" | sub-id, …)` for rows 25-30 (row 28 as two sub-ids);
row 31 is a pointer (no own site); (2) the backslash instance of FV1-27 (`hooklib.py` shell-opaque, row 25) first;
(3) G-dispatch units relabelled `["conductor"]` with `note` "dispatch-time unit: no role's tool line reaches it (mech §2.8, T0 M8)";
test rows: `tbw_t4b_sites` per id (expected from §5.3 / wave0 8b); census by `test_judgment_census.py` (slow, canon).
edges: common; E-T4b-1 dense ceiling: after the relabel `test_judgment_census.py` may demand a LOWER `blocking_per_role`
ceiling — lower it to the printed number (a shrink, named); a demand to RAISE is a STOP (AR-20). Invariant: no ceiling
rises. E-T4b-2 census merge order (§3): T4b merges first; a later census node merges main and recomputes.
DoD: common, `--witness-for scripts/stage_guard.py scripts/hooklib.py scripts/tests/fixtures/judgment-census.json scripts/tests/test_detector_verdict.py`;
fast: test_detector_verdict.py; canon: test_stage_guard, test_run_forms, test_hooklib_scan, test_judgment_census.
Counter: stage_guard units bare (22 in its list) and untold (relabels), measured. Hot files: Lead check §3 before dispatch.
architecture: AR-9, AR-13, AR-18, AR-20, AR-29 -- ids at stage-guard refusals; reach relabels named.

### Card T5r — s5_precheck + manifest_put sites (wave A)
given: common; mech §5.4 rows 1-9, 20-33; wave0 item 10 (`sides.*`, `expectation_changes`, `provisional`);
`PKG/scripts/s5_precheck.py` (the family producers below), `PKG/scripts/manifest_put.py`.
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\s5_precheck.py (check_manifest, check_row_fields, check_bindings, check_then_remainders, check_open_oracle_asserted, check_expectation_changes, check_case_is_oracle, check_run_mapping, check_environment, check_env_evidence, check_obligations, check_plan_conformance, check_sides and its `_sides_*` helpers)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\manifest_put.py (_refuse_colliding_ids, _refuse_unmergeable, provisional_row_problems, expectation_change_problems and the functions holding the §5.4 rows 21-32 lines)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_manifest_put_merge.py (new rows for manifest_put ids)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_s5_precheck_sides.py (new rows for s5_precheck ids — fast keep; F-2)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\tbw-t5r.md
non-goals: common; `s5_precheck.report` and `refusal_cause` (FV1-30b N4/N5 — merged or not: NOT ESTABLISHED, Lead:
`git -C C:\QAFactory\forge-repo log --oneline origin/main -5 -- ai-packages/qa-factory/scripts/s5_precheck.py`); the
smell/copies/parameterization/relative_oracle families (advice, mech §5.0 (3)); `sides.provisional`/`sides.pending`
rows (T1r-cards §4 — not landed; their sites wait for those rows); execution_request/run_suite (done by S-1a/S-1b).
items: (1) each finding of a family carries its row id (`s5_precheck:<family>`; sub-ids for `sides.declared/settled/
placeholders`); (2) each manifest_put refusal carries its id (rows 20-33 of §5.4, sub-id where one function holds two);
(3) s5_precheck form-1 output byte-identical (EC-1) — one row asserting it on a fixture.
test rows: one per id, "the site writes this id" (expected from §5.4 row / wave0 item 10).
edges: common; E-T5r-1 a finding that is a dict, not a string: NOT ESTABLISHED in this pass whether s5_precheck findings
are str or dict (`check_row_fields` appends to `findings: list`, `s5_precheck.py:3798-3820`, shape not read). If dict: the
id rides as a `check` attribute through `refusal()`'s Record only if the printed JSON stays byte-identical plus a LAST
`told` key; if that cannot hold, STOP and return the question (never a new key in the middle). Invariant: form-1 output
readers unchanged. E-T5r-2 `row_fields`: the label may need to stay `manifest` (mech §5.4 row 2 note) — return the sub-id
as a question if the family label is read by a pass rule (`_names`, FV1-30a). E-T5r-3 a person's recorded word passes a
family by tag (`check_row_fields` docstring): siting never changes which words pass. Invariant: no pass road closes.
DoD: common, `--witness-for scripts/s5_precheck.py scripts/manifest_put.py scripts/tests/test_manifest_put_merge.py scripts/tests/test_s5_precheck_sides.py`;
fast: test_manifest_put_merge.py, test_s5_precheck_sides.py; canon: test_s5_precheck, test_window_record (slow).
Counter: unsited 25 (11 + 14); told-ratchet units of s5_precheck (the 14 family units, bare 66) and manifest_put (`run` 16).
architecture: AR-9, AR-13, AR-18, AR-22, AR-29 -- ids at S5 chain refusals; form-1 output unchanged.

### Card T6 — handoff_check sites (wave A)
given: common; mech §5.1 T6; wave0 item 1 rows (F-W1 (a): literal ids per problem builder); K2 report (narrowed roles of
`null_outcome.*`, `findings_tooling`, `tried`); `PKG/scripts/handoff_check.py` (`refusal_text`, `values_report`, problem builders).
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\handoff_check.py (refusal_text, values_report, the problem builders of the 21 rows; NOT `_review_receipt` — FV2-78, NOT `_plan_row_of`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_detector_verdict.py (new function `tbw_t6_sites` only — F-2 (b))
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\tbw-t6.md
non-goals: common; `form-rounds.json`; driver `KNOWN_REFUSALS`.
items: each of the 21 ids of §0.2 written at its builder; text byte-identical (driver `KNOWN_REFUSALS` `handover_form`/
`form_vocabulary`); test row per id (expected from wave0 item 1 / stage-joints row).
edges: common; E-T6-1 path-indexed problems (`<path, list indices dropped>`) take the literal id of their builder (F-W1 (a)),
never a computed id. Invariant: E1 (one literal per site) holds. E-T6-2 the values file road (`values_file`, `values_apply`)
is read by `guard_pre_tool` PT-handoff-values (T4a) — T6 never edits the guard. Invariant: one writer per file.
DoD: common, `--witness-for scripts/handoff_check.py scripts/tests/test_detector_verdict.py`; fast: test_detector_verdict.py;
canon: test_handoff_values_refusal, test_handoff (slow). Counter: unsited 21; told-ratchet handoff_check units (bare 28).
architecture: AR-9, AR-13, AR-18, AR-29 -- ids at handover-form refusals; text unchanged.

### Cards T7a-A / T7a-B / T7a-C — validate_artifacts sites (fork F-3: 3 nodes instead of 7)
given: common; mech §5.2 (rows with lines); `PKG/scripts/validate_artifacts.py` (functions per node);
`PKG/references/artifact-writers.json`.
T7a-A owns: C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\validate_artifacts.py (check_case, check_case_form, check_then_oracles, check_cell_counts, check_bug, check_bug_filing_header, check_bug_form, check_register, check_delivery_column → read as check_delta_column, check_behaviour_claims, check_manifest_reuse, check_requirements_review, check_understanding)
T7a-B owns: …\validate_artifacts.py (check_plan, check_plan_v0, check_manifest_v0, check_manifest_invariants, check_remedy_rows, check_self_fixes, check_marker_in_file, check_phase_json, check_context_manifest_v0)
T7a-C owns: …\validate_artifacts.py (check_run_report_empty, check_run_report_head, check_run_report_v0, check_result_rows, check_run_report_coverage, check_triage_v0, check_report_sections, check_report_traceability, check_report_left_with_you, check_report_test_marks, check_report_forbidden, check_report_human_text, check_report_gate_b, check_report_blocks, check_report_coverage, check_ptr_readiness, check_test_report, check_report_ledger_and_readiness, check_legacy_report_sections)
each also owns: C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_validators.py (one new function `tbw_t7a_<a|b|c>_sites`) and C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\tbw-t7a-<a|b|c>.md
(the absolute path `…\` above is `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\`; T7a-A's line holds a typo-guard: the function is `check_delta_column`.)
non-goals: common; T7a-8's functions (no row); `collect_errors`, `main` (aggregators: a site inside them with several
callers follows EC-2).
items: every `errors.append` of an owned function → `errors.append(refusal("validate_artifacts:<function>", <same expr>))`;
`check_phase_json` appends take `validate_artifacts:check_phase_json.<artifact>` for the two artifacts with rows, the
others stay bare with E6 "(code) code writer, no row" (wave0 S3); detector-printed text byte-identical.
test rows: one per function "the site writes this id" (expected from §5.2 row); A: 13 functions, B: 9 (10 ids), C: 19.
edges: common; E-T7a-1 one `errors` list collects several functions' appends before one print: each append carries its own
Record; the printed REJECT text is unchanged. Invariant: the detector output the exit gate reads (`exit_gate`
`detector_errors`) is byte-identical. E-T7a-2 EC-8 instance known now: `check_case_form`'s row claims plan-row inheritance
the body does not check (critic t-703 B2 sibling) — report it, do not edit.
DoD: common, `--witness-for scripts/validate_artifacts.py scripts/tests/test_validators.py`; fast: `python -B ai-packages/qa-factory/scripts/tests/test_validators.py`.
Counter: unsited A −14 (13 functions + 0; check_delta_column etc. — exact list §0.2), B −10, C −18; told-ratchet units of
validate_artifacts.py per function (:655-858).
architecture: AR-9, AR-13, AR-18, AR-29 -- ids at artifact validator refusals; detector text unchanged.

### Card T7b — planning_contract sites (wave A; quarantined tests → F-2)
given: common; wave0 §3a (12 rows; F-W4 (b), F-W5 (a)); `PKG/scripts/planning_contract.py` (`gate_plan_errors` :286-291,
`validate_plan`, `contradiction_errors`, `_branch_block_lines`, `s3_branch_refusals`, `fence_lines`, `_regression_findings`,
`fit_target_block`, `_request_findings`, `_detector_body` :4368-4481 — wave0 line numbers, re-located by the builder with Grep).
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\planning_contract.py (the functions above; `_regression_findings` docstring reword — F-W5 (a))
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_detector_verdict.py (new function `tbw_t7b_sites` only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\tbw-t7b.md
non-goals: common; `unmarked_revision_errors` site (its conductor sub-row lands in T9c, F-W4 (b)); WARN lines; the
waiver line; `validate_case_actions`, `publication_manifest` (no row); the quarantined planning tests.
items: 12 ids at their sites; REJECT blocks byte-identical (exit_gate `detector_errors`, `exit_gate.py:611-623` per wave0);
test row per id (expected from wave0 §3a rows).
edges: common; E-T7b-1 `regression` problems come from `regression_scope.problems` (another module): the id goes on the
planning_contract caller (EC-2). Invariant: regression_scope.py is not edited.
DoD: common, `--witness-for scripts/planning_contract.py scripts/tests/test_detector_verdict.py`; fast: test_detector_verdict.py.
Counter: unsited −12; planning_contract units (bare 73 total, minus the no-row functions).
architecture: AR-9, AR-13, AR-18, AR-29 -- ids at S3 plan contract refusals; REJECT text unchanged.

### Card T7c — coverage_contract sites (wave A)
given: common; wave0 §3b (F-W3 (a)); `PKG/scripts/coverage_contract.py` (`validate_obligations` :320-456),
`PKG/scripts/observation_contract.py` (read only).
owns: C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\coverage_contract.py (validate_obligations and its problem lines)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_detector_verdict.py (new function `tbw_t7c_sites` only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\tbw-t7c.md
non-goals: common; `manual_current` (pointer to `role_cli:manual_evidence.py write-block`); the projection filters
(`finalize_task`, ledger, `delivery_manifest`).
items: `coverage_contract:obligations` and `.observation` at their sites; text byte-identical; a test row each.
edges: common; E-T7c-1 the same function used as a projection filter (no refusal there, wave0 §3b): the Record must not
change the filter's return value. Invariant: projections unchanged (a row asserting a filter call returns today's value).
DoD: common, `--witness-for scripts/coverage_contract.py scripts/tests/test_detector_verdict.py`. Counter: unsited −2.
architecture: AR-9, AR-13, AR-29 -- ids at obligation refusals; filters unchanged.

### Card T9a — controller role-resumed units (wave B; census after T9c)
given: common; mech §5.3a (rows; `code_review_receipts` and `rework_rows` sentences from wave0 item 9, K2's re-point);
T0 M7 (3 road-(b) units, mech :771); FV2-88's digest if it returns first; `PKG/scripts/controller.py` (functions below).
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\controller.py (_s3_completion_gate, _code_review_refusal, _s5_plan_accept_problems, _plan_rework_rows_problems, _plan_review_problems)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (rows of those functions; `_code_review_refusal` has NO census row today per mech :771 — add it, named)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_controller_doors.py (new rows only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\tbw-t9a.md
non-goals: common; `:7479`/`:7515` (M7 found no road: declared gap (4)); `controller-blocks.md` (must stay unchanged).
items: (a) relabel to the dispatch's roles with a `note`; (b) `raise StateConflict(refusal("controller:<id>", <same text>))`,
raised text byte-identical (REPAIR_MARKER kept), counted `tagged`; (c) test row per unit (expected from §5.3a).
edges: common; E-T9a-1 the driver reads the raised text by `REPAIR_MARKER` / `S\d structured .* invalid` (driver_machine
:444 per M7): unchanged. Invariant: road (b) keeps reaching the role. E-T9a-2 if FV2-88 finds a row on the wrong role:
the builder does not edit the row (EC-8); the Lead decides before merge. E-T9a-3 census order (§3): merges after T9c.
DoD: common, `--witness-for scripts/controller.py scripts/tests/fixtures/judgment-census.json scripts/tests/test_controller_doors.py`;
fast: test_controller_doors.py; canon: test_s3_strategist_rounds, test_s5_plan_controller, test_judgment_census, every
`test_controller_*` (builder-rules 7b). `controller-blocks-gen.py` check: `python -B tools/controller-blocks-gen.py --check`
— CLI NOT ESTABLISHED (flag name not read); the builder runs its `--help` and reports.
Counter: unsited −6. Hot file controller.py: Lead check §3.
architecture: AR-9, AR-10, AR-13, AR-29 -- ids at role-resumed controller refusals; text and road unchanged.

### Card T9c — conductor launch rows (wave C; census after T7f)
given: common; mech §2.8-§2.9, §5.5 rows; wave0 item 11 and part3 (command rows per move; O-1 correction of
`stage_done:set`); T1r-cards §4 `stage_done:set` sentence (fixed there) and F-8 (a): `planning_contract:plan.unmarked_revision`
"read the body, write the sentence, Lead accepts"; `PKG/scripts/no_move.py` (`moves_section` :257-285, `validate_options`,
`check_args` :228-254, `prose_refusal`), `PKG/scripts/stage_joints.py` (`_producer_leg` :691-704, `rows_for`, `told_line`),
`PKG/scripts/driver_conductor.py:684` (the one caller), `PKG/references/conductor-actions.json`.
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\no_move.py (moves_section, validate_options, check_args, prose_refusal sites)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\stage_joints.py (_producer_leg only — fork F-4)
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\stage-joints.json (NEW conductor rows only: `no_move:options`, `:prose`, `:class`, `:args`, the drafted command rows, `stage_done:set`, `planning_contract:plan.unmarked_revision`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (no_move units → ["conductor"] with `note`; stage_done:set unit if needed)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_controller_doors.py (new rows)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\tbw-t9c.md
non-goals: common EXCEPT the stage-joints.json conductor rows above; any role row; `conductor-actions.json` texts (F16 (a)).
items:
| # | what | expected | test (expected from) |
|---|---|---|---|
| 0 | measure first: one conductor row added to a COPY of stage-joints.json, `stage_joints.py --check` on the copy | if red "role `conductor` has no agents/conductor.md": apply F-4 (a); if green: `_producer_leg` stays untouched | report line |
| 1 | `moves_section` appends `## What code will check in this launch` (C3) with `told_line` of `rows_for("conductor", …, {"moves": open_ids})` | rework open → `no_move:args` + rework command rows; no move open → only `conductor_answer` rows; nothing → `- none` (E24) | row per fixture (expected from mech §5.5 / §2.9) |
| 2 | `validate_options`/`check_args` refusal texts byte-identical | they reach the driver's `_verdict_rule` | row |
| 3 | `driver_conductor.conductor` prompt for a fixture boundary holds the section | — | row |
edges: common; E-T9c-1 a move id renamed in conductor-actions.json → K3 red on `move:<id>` (E25); invariant: no row points
at a missing move. E-T9c-2 an undrafted command row (wave0 item 11: 6 "not drafted") stays OUT, counted in the report with
reason; invariant: no row is invented by a builder. E-T9c-3 `planning_contract:plan.unmarked_revision`: the builder reads
`unmarked_revision_errors` and writes the sentence as a QUESTION in the report; the row lands only after the Lead's
acceptance (F-8 (a)) — until then it is absent. E-T9c-4 TEMPORAL: before, the conductor launch has no section; after, every
launch has one (possibly `- none`). E-T9c-5 POSITIONAL: the section goes AFTER "## Moves open here" and "## Answers this
question already takes", before the state text; invariant: the existing section headings test_no_move_seam_c26 reads keep
their order.
DoD: common, `--witness-for scripts/no_move.py scripts/stage_joints.py references/stage-joints.json scripts/tests/fixtures/judgment-census.json scripts/tests/test_controller_doors.py`;
fast: test_controller_doors.py, `python -B ai-packages/qa-factory/scripts/contract_slices.py --check`; canon:
test_conductor_doors, test_no_move_seam_*, test_stage_joints, test_judgment_census. The code critic reads mech §2.8-§2.9 (t-472).
architecture: AR-15, AR-17, AR-10, AR-13, AR-29 -- conductor rows through one seam; no check added.

### Card T7f — stage_done census relabel (wave C; census after T4b)
given: common; wave0 §3e and F-W2 (a); `PKG/scripts/tests/fixtures/judgment-census.json` rows of `stage_done.py` units.
owns: C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (stage_done.py units only: `roles` → ["conductor"], `note` "no agent file and no role-commands entry names stage_done (wave0 §3e trail §T)"; dense ceilings it moves)
non-goals: `stage_done.py` code (no role row); test_stage_done.py (quarantined).
edges: E-T7f-1 `refused` (census :952 per wave0) is a selftest helper — relabel it with the others, note says so.
E-T4b-1 applies (ceilings only shrink).
DoD: `--witness-for scripts/tests/fixtures/judgment-census.json`; canon: test_judgment_census (slow). Report: units
relabelled (list), ceilings old → new. A one-file data node: no changelog fragment (no behaviour change) — or one bullet if
the Lead wants it (small choice S-4).
architecture: AR-20, AR-29 -- reach relabel, named; judgment: none -- data reach of existing units.

### Card T3b — brief + prompt line (wave B, after M9 and F-7's order on test_ahead_cards.py)
given: common; mech §5.1 T3b, §2.2, §2.4 (3), §2.6, E23, C13; M9 report; T1r report §8 (what T3b must mirror);
wave0 item 6 (first_look rows; F-W6 (a): `put.walked` no row); `PKG/scripts/brief_pack.py` (`ahead_card` :417,
`_row_field_lines` :2208, `FIRST_LOOK_DOD` :4017, `FIRST_LOOK_AHEAD` :4019, the `ahead` assignment and section — re-locate
by Grep; mech's :4344/:4425 are older), `PKG/scripts/story_step.py` (`_prompt`, `_card_text`), `PKG/scripts/window_record.py`,
`PKG/scripts/first_look.py` (`put` refusal sites).
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\brief_pack.py (ahead_card removed, the ahead section, FIRST_LOOK_AHEAD removed, FIRST_LOOK_DOD first sentence only, `_row_field_lines` → a call, new `dispatch_groups`, the brief line; FIRST_LOOK_ROLES_MAX and its arguments may go, mech §7)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\window_record.py (new row_field_lines)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\story_step.py (_prompt, _card_text only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\first_look.py (put refusal sites → refusal("first_look:put…"))
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_first_look.py (new rows)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_brief_pack.py (new rows; slow — written, canon)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_ahead_cards.py (only the brief block rows that call brief_pack.ahead_card — IF T1r-cards has not landed them first; else not owned)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\tbw-t3b.md
non-goals: common; `contract_slices.ahead_card`, `CARD_GROUP`, `NOT_YET_HEAD` (closing); FV2-54/57 (`first_look.py`) and
FV2-56/58 (`brief_pack.py`) pile nodes — function-disjoint; if one of them is in work, `очередь:` per batch-2 "Ход" t-779.
items: mech T3b (a)-(e) verbatim; plus `first_look:put.*` 11 ids at their sites (wave0 item 6 builders).
edges: common; mech E22/E23 and §4 M9 outcome; E-T3b-1 TEMPORAL with T1r-cards: before T1r-cards, hand_cards 12 →
the card text is on the page under `### Not yet in rows`, so removing the brief section loses nothing (critic t-703 item 3);
invariant: a role is never told less (page carries it). E-T3b-2 an unreadable dispatch fact → neither exclusive member and
the `could not tell` text (mech (c)).
DoD: common, `--witness-for scripts/brief_pack.py scripts/window_record.py scripts/story_step.py scripts/first_look.py scripts/tests/test_first_look.py`;
fast: test_first_look.py, test_first_look_wiring.py, test_ahead_cards.py (if owned); canon: test_brief_pack,
test_window_record, test_story_step, test_story_step_* (builder-rules 7b). Counter: unsited −11.
architecture: AR-10, AR-13, AR-15, AR-29 -- one told carrier (the page); groups line in the prompt.

### Card K1b — FV2-79 (wave B)
given: `docs/tasks/specs/20261114-told-before-work-k10-paydown-spec-r2.md` §5 (K1b, E1-E7 — NOT re-read in this pass);
finding `plans/piles/live-run-fvf/findings/20261114-k10-k1b-uzel-i-uslovie-vyhoda-vremennoj-stroki-code-critic.md`;
K1a report (row labels K1b must see green in the canon); owner's S1 = A (batch-2 "Ход" t-864).
owns: as FV2-79's "Пишет в" (`batch-2...md:106`), absolute: C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_contract_slices.py (test_t1rs, the pin 864-865), …\references\stage-joints.json (told markers only), …\references\slices\ (only `--write`), …\references\inject-map.json, …\references\role-load.json, …\changelog.d\tbw-k10-paydown-k1b.md
DoD (inline): `native_headroom.qa-code-critic` deleted (U ≤ 68,400) or lowered to the measured U with the K1b-E7 stop;
a standing row at close is an acceptance refusal (FV2-79); `python -B ai-packages/qa-factory/scripts/contract_slices.py --check`
exit 0; `python -B ai-packages/qa-factory/scripts/tests/test_contract_slices.py` green; `--witness-for` of the owns.
edges: the canon precondition ("канон пачки с K1a/K2/KR") NOT ESTABLISHED: Lead reads the last `package-full` with
`python -B tools/ci_read.py why` before dispatch; red on a K10p row = K1b waits.
Collision: stage-joints.json markers vs T9c's new rows (different keys; merge after T9c or before — Lead orders; recommend
K1b before T9c, both in wave B/C). FV2-81/82/91 share test_contract_slices.py (function lists).

### Card T1r-cards-R — designer redraft (wave 0, not a writer)
handoff: `C:\QAFactory\forge-repo\docs\tasks\specs\20261117-told-before-work-t1r-cards-spec-r2.md`; given: the cards spec,
critic t-703, this §2; question: rewrite §3 with clause-level placement on the BODIES (B2), replace rule P by a placed table
(B3), apply X1-X9, rewrite C-9 per F-6, give `execution_request:fingerprint.build` (F-5) and `check_case_form`'s sentence
correction; split into -a (rows/re-points/pages/retire) and -b (test re-points) (X9). Then a plan-critic pass on the
changed sections only (CLAUDE.md rule 3: forks + a meaning change).

### Card closing (wave D)
given: this §0, the merged reports; owns: C:\QAFactory\forge-repo\ai-packages\qa-factory\references\stage-joints.json (`told_ratchet` values only), …\scripts\tests\fixtures\told-ratchet.json (`rowless`, `untold`, unit ceilings to the measure), …\scripts\tests\test_stage_joints.py (K12 pin and the told counter pins only), …\scripts\contract_slices.py (`ahead_card`, `CARD_GROUP`, `NOT_YET_HEAD` removed when hand_cards is 0), …\scripts\stage_joints.py (`_hand_cards`/`AHEAD_CARDS` only if the Lead retires the counter — fork F-7 note), …\design\factory-rules-debt.md:271-272 (the "All twelve have a card now" line, Lead text)
items: (1) `stage_joints.py --check` measured values written: hand_cards 0, legacy_legs 0, unsited 0 — or the declared gaps
of mech §5.0 (four classes), each with its reason; (2) told-ratchet.json to the measure (shrink only); (3) T7a-8/T7d/T7e
census units: measure whether K6 `untold` counts them; if yes, relabel `["conductor"]` (named) — census merge after T9a;
(4) Lead: BATCH CANON on CI appended to the last `accepted`.
edges: any counter that is > 0 without a declared class = "the night is not done" (mech §5.0). Invariant: no gap undeclared.
DoD: `python -B ai-packages/qa-factory/scripts/stage_joints.py --check`, `python -B ai-packages/qa-factory/scripts/contract_slices.py --check`,
`--witness-for` of the owns; canon: test_stage_joints, test_judgment_census.

---

## §7 Pile rows to register (Lead writes them; text ready)

Recommended home: a new pile `told-before-work`, `batch-1-finish.md` (статус «ожидает», П1) — fork F-8. Columns as in
batch files: Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| TBW-M9 | П1 | Опыт M9: переживает ли страница из `--append-system-prompt-file` и строка промпта `claude -p --resume` (спека finish §4) | Lead | `docs/tasks/specs/reports/20261117-tbw-m9.md` | — | ожидает |
| TBW-T4a | П1 | id строк §5.3 на отказах `guard_pre_tool`/`host_adapter` (FV1-27 строки 2, 11) | builder → critic | `scripts/guard_pre_tool.py` (функции карточки), `scripts/host_adapter.py` (`role_policy`), `scripts/tests/test_detector_verdict.py` (`tbw_t4a_sites`) | — | ожидает |
| TBW-T4b | П1 | id строк §5.3 25-31 на `stage_guard`/`hooklib`; перепись G-dispatch → conductor | builder → critic | `scripts/stage_guard.py`, `scripts/hooklib.py` (функции карточки), `scripts/tests/fixtures/judgment-census.json`, `test_detector_verdict.py` (`tbw_t4b_sites`) | перепись: первым | ожидает |
| TBW-T5r | П1 | id строк §5.4 на `s5_precheck` (11) и `manifest_put` (14) | builder → critic | `scripts/s5_precheck.py` (семейства), `scripts/manifest_put.py`, `test_manifest_put_merge.py`, `test_s5_precheck_sides.py` | — | ожидает |
| TBW-T6 | П1 | id 21 строки `handoff_check` | builder → critic | `scripts/handoff_check.py` (строители задач; не `_review_receipt`), `test_detector_verdict.py` (`tbw_t6_sites`) | FV2-78 — списки функций | ожидает |
| TBW-T7a-A/B/C | П1 | id 42 строк `validate_artifacts` (три узла по функциям) | builder → critic | `scripts/validate_artifacts.py` (списки функций), `test_validators.py` | A → B → C по общему файлу | ожидает |
| TBW-T7b | П1 | id 12 строк `planning_contract` | builder → critic | `scripts/planning_contract.py`, `test_detector_verdict.py` (`tbw_t7b_sites`) | — | ожидает |
| TBW-T7c | П1 | id 2 строк `coverage_contract` | builder → critic | `scripts/coverage_contract.py`, `test_detector_verdict.py` (`tbw_t7c_sites`) | — | ожидает |
| TBW-T7f | П1 | перепись единиц `stage_done` → conductor (F-W2 (a)) | builder → critic | `judgment-census.json` | T4b | ожидает |
| TBW-T9a | П1 | id 6 строк `controller:*`; перепись ролей | builder → critic | `scripts/controller.py` (функции карточки), `judgment-census.json`, `test_controller_doors.py` | T9c (перепись); FV2-88 | ожидает |
| TBW-T9c | П1 | раздел «What code will check in this launch» у дирижёра; строки дирижёра; `_producer_leg` | builder → critic | `scripts/no_move.py`, `scripts/stage_joints.py` (`_producer_leg`), `references/stage-joints.json` (строки дирижёра), `judgment-census.json`, `test_controller_doors.py` | T7f (перепись) | ожидает |
| TBW-T3b | П1 | бриф без карточек, строка групп, `first_look:put` | builder → critic | `scripts/brief_pack.py`, `window_record.py`, `story_step.py` (`_prompt`, `_card_text`), `first_look.py`, `test_first_look.py` | TBW-M9; T1r-cards по `test_ahead_cards.py` | ожидает |
| TBW-T1rc | П1 | карточки → строки: передрафт дизайнера (B2, B3), критик на изменённые части, затем билдер -a/-b | designer → critic → builder | (по передрафту) | — | ожидает |
| TBW-T10 | П1 | носители Lead: ось 38, AR-10/AR-9, FR-38, critic-brief, калибровка | Lead | `docs/SIBLING_MAP.md`, `design/architecture.md`, `design/factory-rules.md`, `docs/tasks/critic-diff-brief.md`, `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` | — | ожидает |
| TBW-close | П1 | закрытие: счётчики `told_ratchet` и `told-ratchet.json` по замеру, мёртвый код карточек | builder | `references/stage-joints.json` (`told_ratchet`), `told-ratchet.json`, `test_stage_joints.py` (пины счётчиков), `contract_slices.py` | все узлы | ожидает |
K1b stays FV2-79 (live-run-fvf/2) with a pointer line `перенос:` NOT needed — the Lead adds its id to TBW's "Зависит от" where needed.
No rows for T5b, T7a-8, T7d, T7e, T8: absorbed / no work (§0, with carriers).

---

## §8 Forks (returned, not decided)

| # | owner | fork | options | recommendation |
|---|---|---|---|---|
| F-1 | Lead | who moves `told_ratchet.unsited` and the EXACT K12 pin (`test_stage_joints.py:927-932`) as siting nodes land in parallel | (a) the wave integrator, one commit per merge wave, from `stage_joints.py --check`; nodes never touch them · (b) each node edits both (six parallel edits of one line → conflicts every merge) · (c) only the closing node (canon red on K12 for the whole finish) | **(a)** |
| F-2 | Lead | where the site-proof rows go for nodes whose module has no FAST keep test (T4a/T4b, T6, T7b, T7c; s5_precheck uses `test_s5_precheck_sides.py` if it is fast — not in slow list) | (a) the module's own keep file (slow or quarantined → written, not run, judged by canon) · (b) one new function per node in `test_detector_verdict.py` (fast keep, the S-1a `t1rs_sites` pattern), names fixed in the cards · (c) ask per node at dispatch | **(b)**; quarantined files are never edited (builder-rules 7b) |
| F-3 | Lead | T7a granularity | (a) 7 nodes as mech (one file, one test file → 6 merge conflicts) · (b) 3 nodes by role group (§6) · (c) 1 node (42 sites, budget risk) | **(b)** |
| F-4 | Lead | conductor rows vs `_producer_leg` (refuses roles with no `agents/<role>.md`) | (a) `_producer_leg` accepts `conductor` when `references/conductor.md` exists (one named data constant; T9c owns the function) · (b) conductor rows use a `code:` producer (misstates who produces) · (c) an `agents/conductor.md` stub (a role file the plugin would load as an agent: wrong) | **(a)**, only if T9c item 0 measures red |
| F-5 | Lead | the `--mine` fingerprint-BUILD failure and `profile.none` door: S-1a classed the build raise "(code)" bare; T1r-cards §4 gives it a role row under an id already used by `validate_request` | (a) role: sub-id `execution_request:fingerprint.build` (row in T1r-cards-R; site in FV2-43); `profile.none` door text in FV2-43 · (b) code: drop T1r-cards §4's fingerprint row | **(a)**: a role meets it and has a door ("write this one run with `run_suite.py --template request`", F-P2-6 (a) accepted) |
| F-6 | Lead, then OWNER if a raise is wanted | T1r-cards size rule after KR | (a) zero growth over the stored `native_headroom`/A22 rows; growth = STOP naming role and bytes · (b) named raise per role (moves automator toward the Codex refusal) | **(a)** |
| F-7 | Lead | T1r-cards today | (a) designer redraft now (wave 0), critic on changed parts, builder in wave C · (b) defer to the next session (hand_cards stays 12; the closing then declares it) | **(a)** |
| F-8 | Lead | home of the new rows | (a) new pile `told-before-work` batch-1 · (b) `live-run-fvf` batch-3 (topic is a live run's findings, not this mechanism) | **(a)** |
| F-9 | Lead | census merge order | (a) T4b → T7f → T9c → T9a (→ FV2-89 → FV2-26) serial merges, parallel work · (b) one census node collecting all relabels at the end | **(a)** (each relabel lives with the node that knows why) |
| Q-O1 | OWNER (plain words) | «Перенос двенадцати карточек правил в строки страниц может немного увеличить текст, который получает автоматор и стратег. Разрешаем ли сегодня поднять их предел размера, если понадобится, или запрещаем рост (тогда узел остановится и спросит)?» | разрешить с записью · запретить | запретить рост: автоматор уже близко к пределу Codex (14 491 символ на файлы проекта по замеру KR) |

---

## §9 Small choices closed by the designer

- S-1 Node ids `TBW-<mech id>`; report files `docs/tasks/specs/reports/20261117-tbw-<node>-report.md`; changelog
  fragments `tbw-<node>.md`.
- S-2 Test function names `tbw_<node>_sites` (F-2 (b)), one per node, so owns by function are disjoint.
- S-3 T5r owns s5_precheck check_* families only, never `report`/`refusal_cause` (FV1-30b's).
- S-4 T7f: no changelog fragment unless the Lead wants one (data reach only).
- S-5 T4 split by file into T4a (no census edit) and T4b (census edit), so wave A carries no census writer.

## §10 Collisions named (brief item)

- p1b-finish N3a × this spec on `dry_exits.py`: NONE — no card here owns `dry_exits.py` or `test_scenario_dry_1.py`
  (owns lists §6). N3a's function `told_before_work` (p1b-finish spec :120) reads told rows: its expectations move when
  T1r-cards / T9c / closing change rows — the N3a builder re-reads rows at its own merge (a reader, not a writer, here).
- FV2-21/23/25 (`stage_joints.py`) × T9c (`_producer_leg`): function-disjoint; FV2-41 conditional.
- FV2-78 (`handoff_check._review_receipt`) × T6: disjoint by function.
- FV2-54/57 (`first_look.py`), FV2-56/58 (`brief_pack.py`) × T3b: by function; `очередь:` if in work.
- FV2-80/83/84/44 (`test_detector_verdict.py`) × T4a/T4b/T6/T7b/T7c: disjoint functions (S-2).
- FV2-81/82/91 (`test_contract_slices.py`) × K1b: FV2-79 is K1b itself.
- FV2-26, FV2-89 (`judgment-census.json`) × T4b/T7f/T9c/T9a: census merge order F-9.

## §11 Readers of every touched file (rule 7)

Commands run (Grep tool, count mode): `judgment-census|stage-joints|told-ratchet|SIBLING_MAP|test-layers\.json` over
`tools/` → 91 hits in 36 files; over `.githooks/` → 1 (commit-msg). Per-file attribution and the script-name readers
(`guard_pre_tool.py`, `handoff_check.py`, `validate_artifacts.py`, `controller.py`, `no_move.py`, `stage_joints.py`, …)
over `tools/`, `.githooks/`, `.claude/`: NOT RUN in this pass (budget) — owed before acceptance:
`python -B tools/owns_readers.py <owns>` (the repo's readers tool exists at `tools/owns_readers.py`; its CLI not read) or
one Grep per name. Known readers from the carriers read:
| touched file | reader | verdict |
|---|---|---|
| `docs/SIBLING_MAP.md` | `tools/mechanism_gate.py` (axis enumeration; Grep hit), `.githooks/commit-msg` | changes in T10 (axis count 37 → 38: the four-questions blocks name 38 axes from then on) |
| `judgment-census.json` | `test_judgment_census.py`, `test_stage_joints.py` (told world), `refusal_registry.py --census` | unchanged code; data changes in T4b/T7f/T9c/T9a |
| `stage-joints.json` | `stage_joints.py`, `contract_slices.py`, `selftest.py:722` (through `load_rows`), `tools/` hits (not attributed) | rows change in T9c / T1r-cards / closing |
| `told-ratchet.json` | `test_stage_joints.py` only (its own note :3) | closing |
| `test-layers.json` | `scenario_walk.py`, `selftest.test_layers`, `tools/test_quarantine.py` | unchanged (no node edits it) |
| `no_move.moves_section` | `driver_conductor.py:684`, `test_conductor_doors.py:944`, `test_no_move_seam_c26_g27_f2.py:70,495,536,546`, `test_story_run_exit_limit.py:690` | changes in T9c (section appended; readers of the existing headings unchanged: E-T9c-5) |

---

## §12 Not done / not established

- Per-file readers over `tools/`, `.githooks/`, `.claude/` for the script names (§11) — owed.
- Whether taken batches' owns name `hooklib.py`/`stage_guard.py`/`controller.py`/`gate_preflight.py` (§3) — command named.
- Whether FV1-30b N4/N5 (`s5_precheck.report`, `refusal_cause`) are merged — command in T5r's card.
- The shape of `s5_precheck` findings (str or dict) — T5r edge E-T5r-1 stops on the bad case.
- The BATCH CANON with K1a/K2/KR (K1b precondition) — `python -B tools/ci_read.py why`.
- K10 pay-down r2 §5 (K1b) and wave0 part3 (command rows per move) — not re-read; the cards point to them.
- `tools/controller-blocks-gen.py` check flag — not read.
- M9 flag names — estimate; `claude --help` first.
- Whether `_producer_leg` actually refuses a conductor row — inferred from code read; T9c item 0 measures it.
- Exact per-unit `bare`/`untold` after each node — measured by the nodes, not predicted here.
- No money figures appear in this draft.

## §13 Reading trail

Read whole or in the named ranges (root checkout): mech spec :340-773; t1r-cards spec whole; critic t-703 whole; reports
`20261114-k10-nodes`, `-t1r`, `-t1r-pages`, `-t1r-pages-fix`, `-k10-paydown-k1a`, `-k2`, `-kr`, `-t1r-sites-s1a`, `-s1b`,
`-s2` (whole); `wave0-rows.md` :100-437; `p1b-finish-spec` :112-141 + Grep; `batch-2-live-run-fvf.md` :1-30, :48-53,
:66-71, :104-137; `plans/builder-rules.md` :36-85; `told-ratchet.json` whole; `slow_tests.json` whole;
`no_move.py:225-304`; `scenario_walk.py:833-932`; `test_stage_joints.py:924-932`; `s5_precheck.py:3798-3820`.
Greps (each with its control named inline above): `refusal\("` over scripts (count); the wider refusal pattern over 18
files (content, 52 hits read); `"check": "<family>:…"` over stage-joints.json (twice); `told_ratchet|call_told_families`;
`conductor` and `_producer_leg|role_exists` in stage_joints.py; `moves_section\(`; agents Glob; test files Glob;
test-layers.json names and section heads; `^## Axis` forms and `[Aa]xis 3[78]` over docs; batch headers "в работе";
hot-file alternation over batch files; readers count over tools/.githooks.
Not read (by budget): `docs/TESTING.md` (rules taken from builder-rules 7b/7d and CLAUDE.md rule 11), the T2 / T3a reports,
`20261114-tbw-fix-round-report.md`, wave0 part2/part3 bodies, the K10 r2 spec.
Needed beyond the manifest: `slow_tests.json`, `scenario_walk.py`, `no_move.py`, `stage_joints.py`, `s5_precheck.py`,
`wave0-rows.md`, `p1b-finish-spec.md`, `agents/` Glob.

## Lead decisions on the forks (17.11.2026, Fable; draft accepted t-953)

F-1 (a) the wave integrator moves `told_ratchet.unsited` and the K12 pin, one commit per merge wave. F-2 (b) one new
function per node in `test_detector_verdict.py`. F-3 (b) three T7a nodes. F-4 (a), only if T9c item 0 measures red.
F-5 (a) sub-id `execution_request:fingerprint.build`. F-6 (a) zero growth; growth = STOP naming role and bytes.
F-7 (a) designer redraft of T1r-cards now. F-8 (a) new pile `told-before-work`, batch 1 (rows of §7 registered by one
small-work batch at the stage boundary). F-9 (a) census merge order T4b -> T7f -> T9c -> T9a.
Q-O1 (owner): asked; until her word the recommended answer holds — no growth of the page limits (same as F-6 (a)).
Wave A launch: T6 and T7a-A now (four slots are held by rules-debt phase 2); T4a, T7b, T7c next as slots free; T5r
after rules-debt FL9 merges (both edit `s5_precheck.py`, function-disjoint, queued to avoid a merge on a hot file).
M9 and the §11 readers run are still owed by the Lead before T3b.
