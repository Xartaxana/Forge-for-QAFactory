# Told before work: T1r-cards, redraft r2 (designer t-1036; finished by designer t-1041)

Status: DRAFT for Lead acceptance; then ONE plan-critic pass on the whole file before any builder (CLAUDE.md rule 3:
forks plus a change of meaning; Lead decision after t-1036). Forks R2-F1..R2-F7 are DECIDED (Lead 17.11, last section);
new forks of round t-1041 are R3-F1..R3-F3 (§8), each returned with a recommendation, and both cards are executable on
those recommendations.
Replaces for dispatch: `docs/tasks/specs/20261114-told-before-work-t1r-cards-spec.md` ("r1"). Verdict on r1: critic t-703
(`docs/tasks/specs/reviews/20261114-tbw-t1r-cards-plan-critic.md`). State today: finish spec `20261117-told-before-work-finish-spec.md`
§2, the owner's word of 17.11.2026 on Q-O1, and the Lead decisions after t-979.

Read base (t-1041): the ROOT checkout `C:\QAFactory\forge-repo` working tree. `.git/HEAD` = `ref: refs/heads/main`;
`.git/refs/heads/main` = `.git/refs/remotes/origin/main` = `e9d6195b7a0c4c2e8e5d77f032af06216f1bd75c` (both loose refs read
with the Read tool; I ran NO command). `PKG` = `ai-packages/qa-factory`. Every file:line below is on that tree unless
marked otherwise. The rows read by t-1036 at d41bcdd0 sit at the same line numbers at e9d6195b for every row this
table touches (Grep of all touched ids, both trees, identical line lists).

---

## Round t-1041: what changed (clause -> result -> file:line)

| clause / item | result | carrier |
|---|---|---|
| P-5 sc-3 | LANDS on NEW `source_preflight:check_source_inventory`, with a BRIDGE (pending + receipts; "retrieved and inspected" is the receipts check) | `source_preflight.py:7, 30-34`; the door words of sc-4 are the body's own (`:44-48`) |
| P-6 rt-4 | LANDS whole: `PC.question_owners()` reads `question_owners: [po_ba, dev_arch, qa]` | `planning_contract.py:3134-3142`; `handoffs/vocabulary.yaml:151`; `check_witness.py:121-143` |
| P-7 ts-1 | SPLIT: lands on `planning_contract:plan` with a BRIDGE ("under the starter policy" - the low-depth and severe rules run only for `risk_policy_revision: factory-starter-v1`); "repeating the detector's sentence…" -> K | `planning_contract.py:176-196`; `references/risk-policy.md:5` |
| P-7 ts-3a | "oracle_unknown with source_conflict" -> K (the body asks either flag, and only for contradicted requirements); "an unresolved oracle does not authorize execution" LANDS inside ts-3c | `planning_contract.py:1477-1505`; `coverage_contract.py:376-378` |
| P-7 ts-3b | SPLIT into ts-3b (`planning_contract:branches`, the `oracle_unknown: false` branch rule), ts-3c (`coverage_contract:obligations`, `oracle_status` + `sufficiency_review`), ts-3d (T, `observation_contract`) | `planning_contract.py:1885-1892` (in `variant_errors`, `:1749`); `coverage_contract.py:321-381`; row `stage-joints.json:6106` |
| P-7 side find | the row sentence of `planning_contract:contradictions` is false against its body -> correction §3.3b, fork R3-F1 | `stage-joints.json:5794`; `planning_contract.py:1485-1504` |
| P-8 ts-2b | "MUTATING" is NOT checked (the body checks presence and separateness) -> K | `observation_contract.py:134-139` |
| P-9 br-2b | HOLDS: the charter carries the severity suggestion; br-2b stays dropped | `agents/qa-bug-reporter.md:26, 47`; `validate_artifacts.py:458-461` |
| P-10 cd-4 | SPLIT: the waiting Thens and the `raise` key rule land on `validate_artifacts:check_then_oracles`; the `unverifiable` case rule needs NEW row `gate_preflight:question_branches` (fork R3-F2); "One case per plan row" and "never `raise` once raised" -> K | `contract.py:1637-1646, 1714-1734`; `validate_artifacts.py:328-333`; `planning_contract.py:1927-1941, 2054-2125`; `gate_preflight.py:2113-2170` |
| P-11 cc-1 | HOLDS: every clause has its check in `critic_rollcall.py`; M2 whole | `critic_rollcall.py:43-64, 589-637, 917-922, 962-1014, 1047-1067, 1085-1088` |
| P-12 au-1 | LANDS (bridge as before) | `s5_precheck.py:1279-1300, 1367` |
| P-12 au-2b | SPLIT: the record clause stays on `manifest_put:expectation_changes`; "a deleted or renamed test owes it too" lands on `s5_precheck:oracle` (au-2c) | `manifest_put.py:1207-1309`; `s5_precheck.py:1823-1826` |
| P-12 au-3 | LANDS whole (remedy, names only, stand shown, project timeout) | `s5_precheck.py:3580-3601, 3694-3706, 3748-3771` |
| P-13 ck-2 | no body checks `cause:` on a finding -> K `## Tools` | Grep `cause:` over `PKG/scripts/*.py`: 30 hits, none a check of the findings file (`driver_stage_s5.py:364` is brief text) |
| P-14 ck-3b | "ONE verdict" is TRUE: `critic_verdict` is one word of the list; the ROW sentence "critic_verdict is a list" is the defect -> ck-3b lands; correction §3.3c (fork R3-F1) | `manifest_put.py:1292-1296`; row `stage-joints.json:3883` |
| P-15 ru-4c | HOLDS: `manual_evidence.py build` names `--then-quote "<n>=<words>"` per Then of `thens` -> dropped (R) | `references/role-commands.json:33-38` |
| P-16 fa-1a | the NOT_EXECUTED parenthesis -> K (not checked); NO_DEFECT lands with a BRIDGE (obs OR surprise target, quoted words); `THEN_QUOTE_MAX == 300` holds | `contract.py:5012-5051`; `validate_artifacts.py:2503-2507`; `manual_evidence.py:40` |
| fa-1f (sweep) | correction of an r2 row marked "none": `fix_result` is checked for presence only -> BRIDGE | `validate_artifacts.py:2527-2530` |
| P-17 fa-1c | the function is `validate` -> NEW row `artifact_producer:validate` | `artifact_producer.py:14, 74, 103-107` |
| P-18 ds-3 | HOLDS (`len(REPORT_SECTIONS) == 11`, order checked); BRIDGE appends the gate-B exemption | `grammar.py:114-118`; `validate_artifacts.py:1229-1246` |
| P-18 ds-1 | the card's block list is NOT `G.REPORT_BLOCKS` (17 names; manual-checks, review-gaps, regression are missing from the card) -> BRIDGE "and the others it names" | `grammar.py:168-196`; `validate_artifacts.py:1516-1521` |
| P-19 ds-6a | `report_facts.check` runs at the S9 exit (`stage_done.report_problems`), not at the scribe's S8 gate, and a stale block is rebuilt by the exit itself -> K `## Tools` | `stage_done.py:282-314, 328-344`; no `stage_done:` row (Grep, control: the `planning_contract:` form found 13 rows) |
| P-20 br-3 / ra-3 | qa-bug-reporter and qa-retro-analyst list Bash -> br-3 T (plus a K line for "external_writes.py performs it after the gate"); E-10 holds for ra-3 | `agents/qa-bug-reporter.md:4`; `agents/qa-retro-analyst.md:4`; `host_adapter.py:519-522` |
| P-21 br-4b | the `gate_b` row is the form's empty-outcome door; the check is the generic "no rows" refusal -> T on `handoff_check:required_rows` + K line for the `gate_b` row | `handoffs/s8-bug-reporter-to-scribe.yaml:13-16, 47-51`; `references/null-outcomes.json:130-132`; row `stage-joints.json:5199-5233` |
| P-22 ra-3 | "every wrong key in one refusal": the body lists every wrong-SHAPED key in one compound refusal; unknown extra keys are not refused -> BRIDGE. "code derives the row (ts, task, forecast, actual, delta, hit, drivers)" is not what `append_record` writes (no `delta`, `hit`, `ts`) -> cut to a K line | `estimate_record.py:69-88, 99-112` |
| P-2 | FAILS as stated: at stored `hand_cards` 0 the "plus-one" row of the told loop sets -1, which the shape check refuses with another text -> card -b owns `test_stage_joints.py` (the told loop only) | `test_stage_joints.py:938-955` (the floor form exists for legacy_legs `:943-948`) |
| P-4 | `handoff_keys_page` returns page 1 only; continuation pages come from `handoff_keys_pages` (as many as `inject-map.json` lists) -> every page reader in both cards uses `handoff_keys_pages` | `contract_slices.py:786-795` |
| P-1 | Lead premise kept (git). Direct read of the integration tree: every row id of §3.1/§4 exists there at the same line; `unsited` 17 (root 46); producers of the sampled rows equal | worktree `agent-ad0767bec786dddde` `stage-joints.json:8127-8129`, `:1874-1889`, `:5675-5699`, `:6289-6331` (may be stale: being edited) |
| item 4 | `handoff_check.py` rename refusal moved by one line: `:3199-3209`; `rt-2`, `cd-1` and `fingerprint` bodies re-read: unchanged in substance | `handoff_check.py:3199-3209`; `exit_gate.py:1592-1663, 1692-1751`; `execution_request.py:201-209, 3761-3771` |
| test rows (TESTING) | card -a adds NO committed test (receipt-per-key and role-text pins are "not written"); its landing is proved by a DOC-DISPATCH witness (fork R3-F3); card -b re-points the existing joint rows, deletes the brief rows and the real-tree card rows instead of inverting them, and fixes the told loop of test_stage_joints | `docs/TESTING.md:131-141, 155-178`; `plans/builder-rules.md:72-84` |
| §10 | charters and test files grepped over tools/, .githooks/, .claude/ with controls | §10 |

---

## §0 What r2 changes: finding -> change -> section

| finding (t-703) | what changed in r2 | section |
|---|---|---|
| B1 F-4 cannot be carried out | Closed by KR (finish §2 B1). C-9 rewritten per the owner's word of 17.11: rule text is never cut for a cap; a cap that does not fit is raised by a named record; past the Codex ceiling: R2-F6 (a) | §5 E-9, A-7, B-6 |
| B2 M1 appends claims the body does not check | M1 replaced by A ("append only the clauses the body checks"). All over-claims resolved on the body (§3.2); round t-1041 closed the 15 OWED reads | §3.0, §3.1, §3.2 |
| B2 sibling: the `check_case_form` sentence | Corrected sentence §3.3; two more row sentences of the same class §3.3b, §3.3c (R3-F1) | §3.3 |
| B3 rule P is not deterministic | Rule P is gone; every clause has a designer-placed row; "an existing family row beats a new function id" (R-1) | §3.0, §3.1 |
| B4 the gate cannot be passed | Closed: T1r and its pages are in main. Both cards branch from main | §6 |
| X1 assumptions A2-A5 | Replaced by numbers read on the carriers | §0.1 |
| X2 quarantined readers in owns | The five quarantined readers stay out of owns; their red after retirement is E-7 | §5 E-7 |
| X3 role-rules with several carriers | Only the carrier entry whose `file` is `references/ahead-cards.json` is re-pointed | B-3 |
| X4 rule K | K = a charter line placed by the table; "present" = the distinctive fact; craft vs process by section | §3.0 R-5, §5 E-5 |
| X5 two doors on one line | One door per row | §3.0 R-6 |
| X6 a K8 split needs several pages | The split repeats until no page reaches W; every line lands in the same commit | A-6 |
| X7 the M3 template | NEW row template against `stage_joints.py:74-75` | §3.0 R-4 |
| X8 owns overlap | Order lines | §7 |
| X9 budget and split | Cut BY TIME, R2-F1 (b) decided | §6 |
| Q1 (owner) | "не в ущерб правилам. Если не влезет можно поднять" (17.11) | §5 E-9 |
| Q2 (owner, severity derived) | Not re-asked; br-2b dropped; P-9 read: the charter carries the suggestion | §3.1 br-2 |
| finish F-5 (a) | `execution_request:fingerprint.build` | §4 |
| t-979 F5 | R2-F7 (a): `handoff_check:cli.values_rename` here, the site re-point in the residual node | §4 |

### §0.1 Facts today (carrier read)

| # | fact | carrier |
|---|---|---|
| T1 | 12 cards, the texts unchanged since t-703 | `PKG/references/ahead-cards.json:1-95` |
| T2 | `told_ratchet` = hand_cards 12, legacy_legs 0, unsited 46; K12 pin `UNSITED_CAP = 46` | `stage-joints.json:8127-8129`; `test_stage_joints.py:927-932` |
| T3 | `native_headroom` qa-automator 79909, qa-code-critic 72828, qa-test-strategist 53739 | `role-load.json:38-42` |
| T4 | `ratchet_tokens` / `process_ratchet_tokens` per role, A22 slack 1000 | `role-load.json:9-37` |
| T5 | ROW_KEYS check, stages, producers, joint; OPTIONAL requirement, requirement_from, carrier_key, door, door_needs, when, role_rule; FIELD_MIN 3; a sub-id of a sited id is sited | `stage_joints.py:74-75, 95, 340-341` |
| T6 | Sentence-less rows: `exit_gate:witness_errors`, `exit_gate:grounding`, `exit_gate:case_identity`, `critic_rollcall:*`, `check_coverage:*`, `s5_precheck:*` | `stage-joints.json:116-181, 183-205, 207-229, 494-515, 540-561, 517-538` |
| T7 | No row id starts `source_preflight:`, `estimate_record:`, `artifact_producer:`, `check_witness:`, `exit_gate:witness_errors.`, `gate_preflight:` or `stage_done:` (t-1041 added the last two; control: the same Grep form `"check": "planning_contract:` found 13 rows) | Grep over `stage-joints.json` |
| T8 | Quarantined readers: test_case_id_form_texts, test_context_bundle, test_report_texts, test_ahead_cards_rules (`test-layers.json:7257`), test_brief_pack_roles. Keep: test_ahead_cards (`:56`, layer `data_join`), test_env_evidence, test_oracle_provenance, test_question_branches, test_s7_rejudge, test_validator_class | `PKG/scripts/tests/test-layers.json` |
| T9 | Slow: test_contract_slices 26.2, test_s7_rejudge 20.6, test_stage_joints 259.4 | `PKG/scripts/slow_tests.json` |
| T10 | Card readers among the tests: test_ahead_cards, test_validator_class, test_env_evidence `:171`, test_oracle_provenance `:335`, test_question_branches `:1780`, test_s7_rejudge `:109`, test_contract_slices, test_stage_joints, plus the five quarantined | Grep (t-1036) |
| T11 | test_validator_class pins on the CARD text (scout fields, `TRIAGE_ROW_IDS`, `FACTS_KEYS`) | `test_validator_class.py:198-210` |
| T12 | `artifact_producer.TRIAGE_ROW_IDS = ('instance_id', 'attempt_id')`, refused in `validate` | `artifact_producer.py:14, 74, 103-107` |
| T13 | Every charter has `## Tools` and `## Techniques` (craft) | Grep over 9 charters (t-1036) |
| T14 | Roles with no Bash: qa-case-critic, qa-case-designer, qa-test-strategist; every other role lists Bash | `agents/*.md:4` (Grep `^tools:`, 12 hits) |
| T15 | The 11 role-rules anchors carried by `references/ahead-cards.json` | `design/role-rules.json:64, 161, 162, 163, 164, 181, 306, 347, 482, 483, 484` |

---

## §1 Architecture, owners, census (rule 10, AR-29, P27)

| AR | how the node keeps it | change check written into the DoD |
|---|---|---|
| AR-10 a requirement reaches the role before the work | every clause a body checks lands on a row told on the role's key pages | -a: the DOC-DISPATCH witness (row text + page line per seg); -b: the re-pointed joint rows read the pages |
| AR-29 code judges data; a judgment is judged by a tier above | a row says only what its body checks (R-2); clauses no body checks go to the charter (K). Whether a clause is checked is a designer judgment, accepted by the Lead and the plan critic | plan critic on §3; critic question 11 on the diff |
| AR-15 one survivor | after -b the page is the one told carrier | `stage_joints.py --check`: hand_cards 0 |
| AR-13 a reader function | tests read told text through `contract_slices.handoff_keys_pages(...)` (P-4), never by opening pages or stage-joints.json | critic: no second reader in the test diff |
| AR-14 one writer | rows: -a; hand_cards: -b; `told_ratchet.unsited` and the K12 pin: the wave integrator (finish F-1 (a)) | owns lists |
| AR-20 shrink-only ratchets | every move named; raises only by the owner's word (E-9); -b moves only down | ratchet table in each report |
| AR-22 a field read has a producer | every NEW row names a role that exists in `agents/` | `stage_joints.py --check` |
| AR-11 a role gets only the context it needs | K8/K10 measured per role; each raise named | `contract_slices.py --check` |
| AR-28 an unknown never becomes a pass | `ahead-cards.json` absent or unreadable stays red "cannot be counted" | E-6 |

Checks added or altered (owner; census class):

| check | owner it serves | census class |
|---|---|---|
| row sentences appended or corrected (§3.1, §3.3, §3.3b, §3.3c) | data (what an existing check checks); the truth of each sentence: judgment of the plan critic / Lead (tier above) | no census unit |
| NEW rows (3 witness sub-ids, `source_preflight:check_source_inventory`, `estimate_record:facts_problems`, `artifact_producer:validate`, `gate_preflight:question_branches`, §4 rows) | data: each describes a check that exists (bodies cited) | no new blocking unit |
| K charter lines | judgment: the role's own craft and procedure | no census unit |
| test pins re-pointed card -> page (-b) | data (closed lists in code = the text the role reads) | xref; test only |
| `told_ratchet.hand_cards` 12 -> 0 | data (count) | ratchet |
| K10 / A22 raises | intent: the owner's word 17.11 (E-9) | ratchet; named record |

Commit lines: the form is `tools/architecture_gate.py`'s (not copied here). -a: `architecture: AR-10, AR-11, AR-20, AR-22, AR-29 -- clauses the bodies check land on rows; raises named per the owner's word` and `judgment: none -- rows state what existing code checks; procedure clauses go to charters; no check added or moved`. -b: `architecture: AR-13, AR-15, AR-20, AR-28 -- the card retired, the pages the one told carrier; readers re-pointed in the same commit` and `judgment: none -- data retirement and test re-points; no check added or moved`.

FR walk (both cards): A (FR-2: a command door only on a `shell` row; the three no-Bash roles, T14, get field doors); B not touched; C (FR-38 kept; FR-11 every clause names a field its check reads); D (FR-58: expected values come from code constants or this spec, never from new output); E, F not touched; G (FR-30 English ASCII, FR-54 siblings §7).

---

## §2 Card shape (both cards)

Both cards branch from `main` after the order lines of §7. Given is narrowed by line range. No file is given whole except `design/factory-rules.md` and `plans/builder-rules.md` (PROJECT.md, package change item 1).

---

## §3 Placement (designer-placed; the builder simulates no rule)

### §3.0 Rules

- **R-1 family first.** An existing row for the check always beats a new function id.
- **R-2 A = append what the body checks.** A clause is appended to a row only when the body behind the row checks it (file:line in the table). Landed text = the card words with the CUTS listed, or the BRIDGE quoted in full (R2-F2 (a), decided). The builder never rewords. Clauses of one row are appended in card order after the existing sentence, joined by one space.
- **R-3 M2 = sentence-less row.** The landed text becomes `requirement`; the role's producer entry is told by `[{"page": true}]` (r1 F-3 (b)). `demands` stay.
- **R-4 NEW row**, exactly: `{"check": "<id>", "stages": [<stages>], "requirement": "<landed text>", "door": "<door>", "when": [<when>], "producers": [{"roles": ["<role>"], "field": "<field>", "told": [{"page": true}], "demands": []}], "joint": null}`. Add `"door_needs": "shell"` only when the table says so; `when` then holds `shell`. `field` >= 3 characters. A row carrying a role-rules anchor gets `"role_rule": "<id>"` (the id on the role-rules.json line the table names).
- **R-4a ROLE+ (R2-F4 (a), decided).** The card's role is added as a NEW producer entry on the row (`roles`, `field` copied, `told: [{"page": true}]`, `demands: []`); the clause is appended by R-2.
- **R-5 K = charter line.** Appended verbatim (or as its BRIDGE) as the last line of the named charter section. `## Techniques` = craft (under its `<!-- kind: craft -->`), `## Tools` = process. Skipped only when the DISTINCTIVE FACT already stands in that charter (Grep, case-insensitive; positive control: the same search for `## Tools`).
- **R-6 one door per row.** A door clause inside a segment is CUT or REPLACES the row's door, as the table says. A producer road (`manifest_put.py`, `report_facts.py --write`, `estimate_record.py`) inside a requirement is not a door.
- **R-7 T / R.** T = the named row already tells the clause on the same role's page (dropped; the report names the row). R = a `requirement_from` row; dropped because its premise holds (P-15).
- OWED: none remain (round t-1041). "Still owed" lists only what reading cannot settle (§9).

### §3.1 The placement table (every clause of the 12 cards)

Columns: seg | clause (card words; `…` = the card text between the quoted ends) | placement | how | body | cut / bridge / door. Anchors (T15) are named where they land.

**qa-scout (S1)**

| seg | clause | placement | how | body | cut / bridge / door |
|---|---|---|---|---|---|
| sc-1 | "work/context-manifest.json is read field by field: `ticket`, `acceptance_criteria` and `implementation` present;" | `validate_artifacts:check_phase_json.context-manifest.json` | R/T | `PHASE_JSON_KEYS` `validate_artifacts.py:103-104` | dropped |
| sc-2 | "every `related[]` row is {key, kind, source}, … result_candidate_refs." (whole) | `validate_artifacts:check_context_manifest_v0` | A | `:2359-2417`; lists held by `test_validator_class.py:199-204` | none; the markers `` `coverage_search[]` rows: `` and `` `existing_test_candidates[]` rows: `` stand verbatim (T11) |
| sc-3 | "S1 closes on work/source-inventory.json: every required source retrieved and inspected, none `pending`, no material without receipts." | NEW `source_preflight:check_source_inventory` (S1, qa-scout, when always, field "work/source-inventory.json") | R-4 (R2-F3 (a)) | `source_preflight.py:7, 21-22, 30-34` (read t-1041) | BRIDGE: "S1 closes on work/source-inventory.json: it lists at least one required source, none is `pending`, and no source material lacks its retrieval or inspection receipt." door = sc-4 |
| sc-4 | "A source you could not get: name it in your digest with its id and what is missing - recording a person's words is the orchestrator's door; you are resumed with their answer." | door of sc-3's row | door | the body's own door `source_preflight.py:44-48` | verbatim |
| sc-5 | "Build with `context_bundle.py --manifest`, then `--validate`." | K `agents/qa-scout.md` `## Tools` | R-5 | procedure | fact: `context_bundle.py --manifest` |

**qa-requirements-tester (S2)**

| seg | clause | placement | how | body | cut / bridge / door |
|---|---|---|---|---|---|
| rt-0 | "Three artifacts, three checks." | dropped (framing) | — | — | — |
| rt-1a | "work/requirements-register.md: `ids` non-empty … `confidence` high\|low" | `validate_artifacts:check_register` | A | `:572-583` | BRIDGE: same words ending with "." |
| rt-1b | "- a register of AC alone while a parent feature exists must be `low`;" | NEW `exit_gate:witness_errors.requirements-tester` (one row with rt-4) | R-4 (R2-F5 (a)) | `check_witness.py:53-57` on readiness.json | BRIDGE: "In work/requirements-readiness.json a register of AC alone while a parent feature exists must be `confidence: low`." |
| rt-1c | "every row's observable prefixed … `impact` from config.json impact_scale." | `validate_artifacts:check_register` | A | `:601-631` | BRIDGE: "Every row's observable …" |
| rt-2 | "Every production module work/impl-diff*.txt CREATES has to be cited by a `derived` row - the exit gate compares them" | `exit_gate:grounding` | M2 | `exit_gate.py:1592-1663` (re-read t-1041: created modules vs `derived` rows `:1620-1657`) | CUT ", so read every hunk, limits, rejected inputs and guards included;" -> rt-2k |
| rt-2k | "so read every hunk, limits, rejected inputs and guards included" | K `qa-requirements-tester.md` `## Techniques` | R-5 | advice | BRIDGE: "Read every hunk of the diff, limits, rejected inputs and guards included." fact: `rejected inputs` |
| rt-3 | "a `derived` row only the diff speaks to also gets its `## Behaviour claims` row." | `validate_artifacts:check_behaviour_claims`; role_rule at `role-rules.json:347` | A | `:709-717` | BRIDGE: "A `derived` row …"; anchor "`derived` row only the diff speaks" |
| rt-4 | "work/requirements-readiness.json: `verdict` ready\|blocked agreeing with the facts, … owner_role po_ba\|dev_arch\|qa." (whole) | NEW `exit_gate:witness_errors.requirements-tester` (S2, when always, field "work/requirements-readiness.json") | R-4 | `check_witness.py:121-143, 169-190`; owner list `planning_contract.py:3134-3142` -> `vocabulary.yaml:151` (P-6 holds) | verbatim. door: "edit the field the refusal names in work/requirements-readiness.json". Note: the verdict word is a proposed list (`new: <word> -- <why>`, `check_witness.py:124-127`); "ready\|blocked" is the routed pair and stays |
| rt-5 | "understanding.md: at most 40 lines, its five sections in order, …" | `validate_artifacts:check_understanding` | A | `:1937-1956`; order not checked | CUT " in order" |

**qa-test-strategist (S3)** (no Bash, T14: field doors only)

| seg | clause | placement | how | body | cut / bridge / door |
|---|---|---|---|---|---|
| ts-0 | "planning_contract.py and observation_contract.py will check, so write to them in fields, not in prose." | K `qa-test-strategist.md` `## Tools` | R-5 | procedure | fact: `in fields, not in prose` |
| ts-1a | "`verification_depth: low` is accepted ONLY together with … `bounded_reversible: true`;" + "and `impact: unknown` can never be low while `impact: severe` demands `critical`." + "Every row needs `risk_source_refs` and `required_scenarios` non-empty." | `planning_contract:plan` | A | `validate_plan` `planning_contract.py:176-196`: low depth and severe->critical only under `risk_policy_revision: factory-starter-v1` (`:176`, the default policy `references/risk-policy.md:5`); unknown-not-low `:193-194` and the two lists `:195-196` always | BRIDGE: "Under the starter risk policy (`risk_policy_revision: factory-starter-v1`), `verification_depth: low` is accepted ONLY together with `impact: low`, `likelihood: low`, `confidence: high` and `bounded_reversible: true`, and `impact: severe` demands `critical`. `impact: unknown` can never be low. Every row needs `risk_source_refs` and `required_scenarios` non-empty." |
| ts-1k | "repeating the detector's sentence in a note is not evidence" | K `qa-test-strategist.md` `## Techniques` | R-5 | not checked (presence rules only) | BRIDGE: "Repeating the detector's sentence in a note is not evidence." fact: `repeating the detector's sentence` |
| ts-2a | "A no-write obligation (kind `state_unchanged` or `no_write_attempt`) needs … `reachability_assertion_ref`." except "MUTATING" | `coverage_contract:obligations.observation` | T | row `stage-joints.json:6106` | dropped |
| ts-2b | "`positive_control_ref` naming a MUTATING check that is not one of those four" | K `qa-test-strategist.md` `## Techniques` | R-5 | `observation_contract.py:134-139`: presence in refs and separateness only; MUTATING is not checked (P-8) | BRIDGE: "A no-write obligation's `positive_control_ref` names a MUTATING check, not one of the four sequence refs." fact: `MUTATING check` |
| ts-3a | "An oracle you cannot settle is `oracle_unknown: true` with `source_conflict: true`;" | K `qa-test-strategist.md` `## Techniques` | R-5 | `contradiction_errors` `planning_contract.py:1485-1504` asks either flag, only for a contradicted requirement | verbatim, "." for ";" . fact: `oracle you cannot settle` |
| ts-3b | "A letter branch whose answer settles the oracle sets `oracle_unknown: false`" | `planning_contract:branches`; role_rule at `role-rules.json:64` | A | `variant_errors` `planning_contract.py:1885-1892` (a row that is `oracle_unknown` and rests on ONE question) | BRIDGE: "A letter branch whose answer settles the oracle sets `oracle_unknown: false`: a row that is `oracle_unknown` and rests on one open question says so in every reading's branch." anchor "whose answer settles the oracle"; `oracle_unknown: false` verbatim (`test_oracle_provenance.py:335`) |
| ts-3c | "and its `coverage_obligations` (`oracle_status: resolved`), each with `sufficiency_review {author_dispatch_id, input_hash, rationale}`" + ts-3a's "an unresolved oracle does not authorize execution." | `coverage_contract:obligations`; role_rule at `role-rules.json:482` | A | `validate_obligations` `coverage_contract.py:329-333` (schema 2 only), `:366-370`, `:376-381` | BRIDGE: "A coverage-schema-2 row lists its `coverage_obligations`, each with `sufficiency_review {author_dispatch_id, input_hash, rationale}` all non-empty, and `oracle_status` resolved (naming an independent `oracle_source_ref`) or unresolved; an unresolved oracle does not authorize execution: its `decision` is `unresolved`." anchor "each with `sufficiency_review {author_dispatch_id" |
| ts-3d | "and `observation_contract`." | `coverage_contract:obligations.observation` | T | row `:6106` ("When the coverage contract revision requires it, every obligation carries an `observation_contract`") | dropped |

**qa-case-designer (S4)** (no Bash, T14)

| seg | clause | placement | how | body | cut / bridge / door |
|---|---|---|---|---|---|
| cd-1 | the first two sentences ("A case file's `id` IS its file name, … refuses the handoff otherwise.") | `exit_gate:case_identity`; role_rule at `role-rules.json:161` (the row carries one `role_rule`; `:162` is the same carrier, anchor checked on the page) | M2 | `exit_gate.py:1692-1751` (re-read t-1041: id == file stem `:1727`, a recorded form `:1729`) | none; anchors "this brief's `Case id form:` line", "form is not read by code" |
| cd-2 | "Frontmatter every case owes: id, … and basis." | `validate_artifacts:check_case`; role_rule at `role-rules.json:483` | A | `:167-198, 214-215` | CUT the parenthesis -> cd-2k; CUT "closed " (`:180-184`); anchor "extend:<case id>\|dedupe:<case id>" |
| cd-2k | "(yours are Draft\|Review\|Approved - only the code critic moves a case to Automated, and only after a probe)" | K `qa-case-designer.md` `## Techniques` | R-5 | not checked | BRIDGE: "Your statuses are Draft, Review and Approved; only the code critic moves a case to Automated, and only after a probe." fact: `only the code critic moves` |
| cd-3 | "defect_class and basis are inherited from your plan row, never reassigned." | K `qa-case-designer.md` `## Techniques` | R-5 | no plan row read in `check_case_form` | fact: `never reassigned` |
| cd-4a | "One case per plan row," | K `qa-case-designer.md` `## Techniques` | R-5 | not checked as such (only the excluded-row rule cd-4b) | BRIDGE: "One case per plan row." fact: `One case per plan row` |
| cd-4b | "an `unverifiable` row too;" | NEW `gate_preflight:question_branches` (S4, qa-case-designer, when always, field "the `question_thens` of the cases"); role_rule at `role-rules.json:163` | R-4 (fork R3-F2 (a)) | `variant_errors(at_cases_stage=True)` `planning_contract.py:1927-1941` (`row_owes_case`) and `:2054-2125`, called by `gate_preflight.py:2113-2170` (designer findings go back to S4 `:2169`) | BRIDGE: "A case is owed for an `unverifiable` row too (and a `skip` one) when an answer to the question it rests on would make the row tested: write it before gate A with `question_thens` on that question. Every `question_thens` is one line of JSON, a list of {question, then, readings}: `then` the number of an item under `## Then`, and a text for every reading of the question." door: "write the case or the `question_thens` entry the line names" |
| cd-4c | "its Thens that wait on a question go in `question_thens` under that question's id as requirements-readiness.json has it" | `validate_artifacts:check_then_oracles` | A | `contract.then_oracle_errors` `contract.py:1721-1723, 1731-1734`, called at `validate_artifacts.py:328-333` | BRIDGE: "A Then that waits on a question (`then_oracles` source `unknown`) goes in `question_thens` under that question's id as requirements-readiness.json has it." |
| cd-4d | "(never `raise` once raised)" | K `qa-case-designer.md` `## Techniques` | R-5 | not read to a check (`raise_question_errors` not opened; K is the safe side) | BRIDGE: "Never `raise` a question once it is raised." fact: `once it is raised` |
| cd-4e | "a before/now question (a `raise` too) keys its texts `now` / `before`, never by letter." | `validate_artifacts:check_then_oracles`; role_rule at `role-rules.json:164` | A | `contract.py:1637-1646` (the raised question, at the write) | BRIDGE: "The question being raised (`raise`) is always a before/now question, and a case keys its texts `now` / `before`, never by letter." anchor "keys its texts `now` / `before`" (any other before/now question: cd-4b's row checks it at S4, `planning_contract.py:2108-2113`) |

**qa-case-critic (S4)** (no Bash, T14)

| seg | clause | placement | how | body | cut / bridge / door |
|---|---|---|---|---|---|
| cc-1 | the whole card (`ahead-cards.json:40`) | `critic_rollcall:*`; role_rule at `role-rules.json:181` (`:484` same carrier, anchor on the page) | M2 | read t-1041 (P-11 holds): verdict list `critic_rollcall.py:43, 589-592`; reviewed column, digest, Gate A line `:595-622`; fixes block `:624-637`; merge rows `:917-922, 962-1014`; level token `:1047-1067`; budget line `:1085-1088` | none; anchors "keep starts P16 or P19", "case budget:` line" |

**qa-automator (S5)**

| seg | clause | placement | how | body | cut / bridge / door |
|---|---|---|---|---|---|
| au-1 | "s5_precheck.py will check, so write to it: every Then is bound in `then_bindings[]` {…}, and the names it demands appear in that assertion." | `s5_precheck:bindings` | A | `check_bindings` `s5_precheck.py:1279-1300, 1367` (P-12) | CUT "s5_precheck.py will check, so write to it: " -> BRIDGE "Every Then is bound in `then_bindings[]` {case, then, instance_id, assertion_ref \"file:line\"}, and the names it demands appear in that assertion." |
| au-2a | "A status code or literal a Then fixes … `unresolved[] reason: contradicts_requirement`." | `s5_precheck:oracle` | A | `s5_precheck.py:129`; pinned `test_ahead_cards.py:306` | none |
| au-2b | "A value you invented may change after a red run only with an `expectation_changes[]` row through manifest_put.py: `then_refs` [{case, then}] it still proves, `what_changed`, `reason`;" | `manifest_put:expectation_changes` | A | `manifest_put.py:1273-1291` | BRIDGE: same words ending with "." |
| au-2c | "a deleted or renamed test owes it too." | `s5_precheck:oracle` | A | `check_expectation_changes` `s5_precheck.py:1798, 1823-1826` (orphan pair) | BRIDGE: "A test that went red and was then deleted or renamed owes an `expectation_changes[]` row too." |
| au-3 | "A `blocked_by_env` row has `remedy` {kind, where, change, restart}, … a test the project's timeout killed is yours." | `s5_precheck:environment` | A | `s5_precheck.py:3580-3601, 3694-3706, 3765-3771` (P-12) | none |
| au-4 | "Smells refused: …" | K `qa-automator.md` `## Techniques` | R-5 | ADVICE `s5_precheck.py:22-25` | BRIDGE: "Smells to avoid: env credentials in an assert, `None == None`, `sleep`, a copied helper." fact: `None == None` |
| au-5 | "One `tests[]` entry per INSTANCE (`func[param]`); `covers` lists cases." | `s5_precheck:manifest` | A | `s5_precheck.py:1046-1068` | none |
| au-6 | "A `deferred_by_decision:*` row carries `disputes` … no route out after gate A." | `s5_precheck:oracle` | A | `s5_precheck.py:1885-1915` | none |

**qa-code-critic (S5)**

| seg | clause | placement | how | body | cut / bridge / door |
|---|---|---|---|---|---|
| ck-1 | "Static review first, … A `mechanical` finding is worded, not fixed." | K `qa-code-critic.md` `## Tools` | R-5 | procedure | fact: `duplicate green` |
| ck-2 | "Findings go to work/test-code/critic-findings-<your dispatch id>.md with `cause:` on each." | K `qa-code-critic.md` `## Tools` | R-5 | P-13: no check of `cause:` | fact: `with \`cause:\` on each` |
| ck-3a | "A test that changed after its red run is listed in your brief (`s5_precheck.py --json`: `expectation_changes`):" | K `qa-code-critic.md` `## Tools` | R-5 | a brief fact | BRIDGE ending "." fact: `s5_precheck.py --json` |
| ck-3b | "give each row ONE verdict through manifest_put.py, … and `critic_note`." | `manifest_put:expectation_changes` + ROLE+ qa-code-critic (has Bash, T14; the row is `door_needs: shell`) | R-4a, A | `manifest_put.py:1259-1268` (a patch joins one record), `:1292-1296` (one word of `expectation_change_verdicts`), `:1297-1308` (P-14) | BRIDGE: "Give each row ONE verdict through manifest_put.py, …" (card words after "give") |
| ck-4a | "`fitted_to_code` is also a `test_defect` finding …" | K `qa-code-critic.md` `## Techniques` | R-5 | not a manifest_put check | fact: `the Then's value restored` |
| ck-4b | "A change you cannot judge is `could_not_judge` with a note, never silence." | `manifest_put:expectation_changes` | T (after ROLE+) | `manifest_put.py:1088, 1305-1308`; row `:3883` | dropped |

**qa-runner (S6)**

| seg | clause | placement | how | body | cut / bridge / door |
|---|---|---|---|---|---|
| ru-1 | "work/run-report.json is read field by field. `witness` at least 30 characters … a retelling is not a witness." | NEW `exit_gate:witness_errors.runner` (S6, when always, field "work/run-report.json") | R-4 (R2-F5 (a)) | `check_witness.py:70-86, 237` | BRIDGE: "`witness` in work/run-report.json is at least 30 characters, and a run_suite summary it names (evidence/<label>-<ts>.json) EXISTS on disk - a retelling is not a witness." door: "edit the field the refusal names in work/run-report.json" |
| ru-2 | "`head` non-empty: evidence not bound to a sha goes stale." | `validate_artifacts:check_run_report_head` | A | `:1634-1644` | none |
| ru-3a | "`env_preflight` pass\|blocked" and "`totals` an object." | `exit_gate:witness_errors.runner` | A | `check_witness.py:238-239` | BRIDGE: "`env_preflight` is pass or blocked, and `totals` is an object." |
| ru-3b | "and blocked means `execution_status` is env_blocked - … timeout." | `validate_artifacts:check_run_report_v0` | A | `:2421-2430` | BRIDGE: "A blocked `env_preflight` means `execution_status` is env_blocked - one field, one source. `execution_status` from passed\|failed\|env_blocked\|not_executed\|broken_run\|timeout." |
| ru-4a | "Every `results[]` row names ONE case, … and a skip carries its reason;" | `validate_artifacts:check_result_rows` | A | `:2447-2473` | BRIDGE ending "." |
| ru-4b | "`manual_checks[].result` is pass\|fail\|inconclusive;" | `exit_gate:witness_errors.runner` | A | `check_witness.py:240-242` | BRIDGE ending "." |
| ru-4c | "a manual `build` takes a `--then-quote` per Then (`thens`)." | `role_cli:manual_evidence.py build` | R | P-15 holds: `role-commands.json:33-38` | dropped |
| ru-5 | "Empty is not clean: … is refused" | `validate_artifacts:check_run_report_empty` | A | `:1609-1631` | CUT " - return blocked with a reason instead."; the row's door is REPLACED by "return `env_preflight: blocked` with a reason, or say where the cases went" (`:1628-1630`) |
| ru-6 | "And every case S5 automated, … saying nothing about it is not." | `validate_artifacts:check_run_report_coverage` | A | `:2081-2153` | none |

**qa-failure-analyst (S7)**

| seg | clause | placement | how | body | cut / bridge / door |
|---|---|---|---|---|---|
| fa-1a | "work/triage.json is read row by row: every row's `verdict` comes from APP_BUG\|…\|NO_DEFECT (…)," | `validate_artifacts:check_triage_v0` | A | list `:2503-2504`; NO_DEFECT `contract.triage_no_defect_problems` `contract.py:5021-5051` via `:2507` | CUT the parenthesis; BRIDGE: "work/triage.json is read row by row: every row's `verdict` comes from APP_BUG\|TEST_BUG\|TEST_BUG:collection\|ENV_ISSUE\|FLAKY\|APP_CHANGED\|CASE_DEFECT\|ASSERT_STRICTER\|NOT_EXECUTED\|RUNNER_MISREAD_EVIDENCE\|NO_DEFECT. NO_DEFECT is for an observation `<case>#obs<n>` or a recorder's surprise `<case>#sur-<id>` only, with a `reason` quoting its recorded evidence in double quotes." |
| fa-1ak | "NOT_EXECUTED is code's, for a manual check that did not answer;" | K `qa-failure-analyst.md` `## Techniques` | R-5 | accepted as a word, its origin not checked (`:2503`) | BRIDGE: "NOT_EXECUTED is code's word, for a manual check that did not answer." fact: `NOT_EXECUTED is code's` |
| fa-1b | "and every row's `evidence` is non-empty whatever the verdict." | NEW `exit_gate:witness_errors.failure-analyst` (S7, when always, field "work/triage.json") | R-4 | `check_witness.py:244-251` | BRIDGE: "Every triage row's `evidence` is non-empty whatever the verdict." door: "edit the row the refusal names in work/triage.json" |
| fa-1c | "Every row also names its `instance_id` and `attempt_id`." | NEW `artifact_producer:validate` (S7, qa-failure-analyst, when always, field "work/triage.json") | R-4 (R2-F3 (a)) | `artifact_producer.py:14, 74, 103-107` (P-17) | verbatim; door: "add the two ids to the row the refusal names in work/triage.json"; pinned `test_validator_class.py:209` |
| fa-1d | "ASSERT_STRICTER costs a `control` block: … no ASSERT_STRICTER." | `validate_artifacts:check_triage_v0` | A | `:2514` -> `contract.py:2237-2300` | none |
| fa-1e | "RUNNER_MISREAD_EVIDENCE costs a `contradiction` block: … (300 characters at most)." | `validate_artifacts:check_triage_v0` | A | `:2516` -> `contract.py:2303-2410`; 300 = `manual_evidence.py:40` | none |
| fa-1f | "FLAKY costs three more fields, and all three are checked: … `fix_result` fixed or not_fixed." | `validate_artifacts:check_triage_v0` | A | `:2517-2530`; `fix_result` presence only `:2527` | BRIDGE (t-1041): the card words up to "teardown\|environment\|unknown;" then "and `fix_result` non-empty (record fixed or not_fixed)." ">= 3 isolated executions" stays (`test_ahead_cards.py:276-277`) |
| fa-1g | "An unfixed flake is not verified, and quarantining it is the person's call at gate B, never yours." | K `qa-failure-analyst.md` `## Techniques` | R-5 | refusal text only | fact: `person's call at gate B` |

**qa-doc-scribe (S8)**

| seg | clause | placement | how | body | cut / bridge / door |
|---|---|---|---|---|---|
| ds-1 | "it renders the code-owned blocks (the verdict, … Decided at gate B after the gate)" | `validate_artifacts:check_report_blocks` | A | `:1516-1521`; `G.REPORT_BLOCKS` (17) `grammar.py:168-196` (P-18: the card's list is a subset) | BRIDGE: "`report_facts.py --task <T> --write` renders every code-owned block the report owes (the verdict, Proven, Product bugs, Open questions, Skipped by the plan, Not proven, Decided at gate A, Size, Where to look, and the others it names; Decided at gate B after the gate)." |
| ds-1k | "test-report.md is read by code, not skimmed. Begin it from the template" and "and you never type a number they carry" | K `qa-doc-scribe.md` `## Tools` | R-5 | procedure | BRIDGE: "Begin test-report.md from the template; never type a number a code-owned block carries." fact: `never type a number` |
| ds-2 | "The `delivery_ready:` line is the block's (check_delivery.py feeds it): yes, after_checks or no." | `validate_artifacts:check_report_ledger_and_readiness`; role_rule at `role-rules.json:306` | A | `:2001-2025` | none; anchor "is the block's (check_delivery.py feeds it)" |
| ds-3 | "Eleven sections in this order: … - the verdict above the first." | `validate_artifacts:check_report_sections` | A | `:1229-1246`; `grammar.py:114-118` (P-18 holds) | BRIDGE: the card sentence, then "`Decided at gate B` is owed only after the gate." |
| ds-4a | "A green test the critic could not verify is in Left with you, not under Proven." | K `qa-doc-scribe.md` `## Techniques` | R-5 | not checked | fact: `could not verify is in Left with you` |
| ds-4b | "Left with you has one item per case in `ledger.json` `left_items`," | K `qa-doc-scribe.md` `## Techniques` | R-5 | `left_items` not read | BRIDGE: "`Left with you` has one item per case in `ledger.json` `left_items`." fact: `left_items` |
| ds-4c | "each with its R-n, case id, `To check:` and `Needed:` or `How:`;" | `validate_artifacts:check_report_left_with_you` | A | `:1291-1299` | BRIDGE: "Each `Left with you` item carries its R-n, case id, `To check:` and `Needed:` or `How:`." |
| ds-4d | "its last two blocks are code's." | dropped (stale: three code-owned blocks, `:1309`) | — | — | report line |
| ds-5 | "The Appendix is `traceability.py --render` pasted, …" | `validate_artifacts:check_report_traceability` | A | `:1255-1275` | none |
| ds-6a | "`report_facts.py --task <T> --check` must exit 0 before you finish." | K `qa-doc-scribe.md` `## Tools` | R-5 | P-19: the check runs at the S9 exit, a stale block is rebuilt there (`stage_done.py:282-314, 328-344`); no S8 check | fact: `--check` must exit 0 |
| ds-6b | "Your prose outside the blocks stays under 6,144 bytes." | `validate_artifacts:check_report_ledger_and_readiness` | A | `:1986-1991`; pinned `test_ahead_cards.py:278-279` | none |
| ds-7 | "check_coverage.py re-runs at the exit gate: regenerate the coverage map first." | `check_coverage:*` | M2 | `stage-joints.json:540-561` | none |

**qa-bug-reporter (S8)**

| seg | clause | placement | how | body | cut / bridge / door |
|---|---|---|---|---|---|
| br-1a | "bugs/BUG-n.md in the task root IS the bug, whatever the channel." | K `qa-bug-reporter.md` `## Tools` | R-5 | location | fact: `IS the bug` |
| br-1b | "Frontmatter is checked: id, title, severity, status, area, found_by, created," | `validate_artifacts:check_bug` | A | `:416-418` | BRIDGE ending "." |
| br-1c | "`violates` per the oracle grammar (…) - … not a bug;" | `validate_artifacts:check_bug_form` | A | `:467-480` | BRIDGE as in r2 ("`violates` follows the oracle grammar (…) - … not a bug.") |
| br-2a | "`impact` from config.json impact_scale," | `validate_artifacts:check_bug_form` | A | `:464-466, 481-483` | BRIDGE ending "." |
| br-2b | "with `severity` DERIVED from it by the scale rather than assigned;" | dropped | — | false against `:458-461`; P-9 holds (`qa-bug-reporter.md:26, 47`) | — |
| br-2c | "`confirmation` unconfirmed\|…\|confirmed_by_rerun" | `validate_artifacts:check_bug_form` | A | `:487-498` | BRIDGE ending "." |
| br-2k | "(confirmed_by_person from the person's words, …), so an unreproduced bug is shown apart." | K `qa-bug-reporter.md` `## Techniques` | R-5 | not checked | fact: `the code derives reproduced_by_factory` |
| br-2d | "Two sections are mandatory: `## User impact` and `## Initial state`." | `validate_artifacts:check_bug_form` | A | `:501-504` | none |
| br-3 | "A tracker is never yours to write: for a non-markdown channel write a proposal under work/proposals/;" | `guard_pre_tool:PT-external-writes` | T | row `stage-joints.json:1865-1900` (qa-bug-reporter has Bash, P-20) | dropped |
| br-3k | "external_writes.py performs it after the gate." | K `qa-bug-reporter.md` `## Tools` | R-5 | not in the row | BRIDGE: "external_writes.py performs a proposal after the gate." fact: `performs a proposal after the gate` |
| br-4a | "A bug from a draft also names `cases` (or `cases: []` with `no_case_reason`) and `requirements`" | `validate_artifacts:check_bug_filing_header` | A | `:433-442` | CUT " and `requirements`"; BRIDGE ending "." |
| br-4b | "your handoff form lists each bug, each draft not filed, … - a complete answer." | `handoff_check:required_rows` | T | row `:5203` ("one row per item in scope"; qa-bug-reporter among its roles `:5212`); empty list refused (`null-outcomes.json:132`) | dropped |
| br-4bk | "and with no draft chosen the one `gate_b` row" | K `qa-bug-reporter.md` `## Tools` | R-5 | the form's empty-outcome door, not a check of its own (`s8-bug-reporter-to-scribe.yaml:13-16, 47-51`) | BRIDGE: "With no draft chosen, your handoff form's `scope` holds the one `gate_b` row (state `nothing_chosen`)." fact: `nothing_chosen` |

**qa-retro-analyst (S9)**

| seg | clause | placement | how | body | cut / bridge / door |
|---|---|---|---|---|---|
| ra-1 | "Every number in retro.md comes from work/retro-numbers.md and .json, … do not re-price." | K `qa-retro-analyst.md` `## Techniques` | R-5 | — | fact: `do not re-price` |
| ra-2 | "The story's spend is the sessions … never rounded into a fact." | K `qa-retro-analyst.md` `## Techniques` | R-5 | craft | fact: `1,911` |
| ra-3 | "The precedent line is written by `estimate_record.py --task <T> --facts <file>`: … every wrong key is listed in one refusal." | NEW `estimate_record:facts_problems` (S9, qa-retro-analyst, `door_needs: shell`, when shell, field "the facts file of estimate_record.py") | R-4 (R2-F3 (a)) | `estimate_record.py:69-82, 86-88` (P-22) | BRIDGE: "The precedent line is written by `estimate_record.py --task <T> --facts <file>`: the file holds `forecast` and `actual` objects and an optional `drivers` array, and every key of the wrong shape is listed in one refusal." door: "fix every key the refusal lists in the facts file and run the same command again"; `forecast`/`actual`/`drivers` stay (pins `test_ahead_cards.py:86`, `test_validator_class.py:210`) |
| ra-3k | "and code derives the row (ts, task, forecast, actual, delta, hit, drivers) from it" | K `qa-retro-analyst.md` `## Techniques` | R-5 | `append_record` `:99-112` writes no `delta`, `hit` or `ts` (analog reported, not fixed here) | BRIDGE: "Code derives the precedent row from the facts file; you never write the row yourself." fact: `derives the precedent row` |
| ra-4 | "What outlives this story goes to the project's ledgers through `project_decisions.py --root <project> add-finding`, not into retro prose." | K `qa-retro-analyst.md` `## Tools` | R-5 | — | fact: `add-finding` (already present: SKIPPED) |

Accounting (t-1041): A 42 (two of them appended to a NEW witness row; ck-3b with ROLE+); M2 4 (rt-2, cd-1, cc-1, ds-7); NEW rows 7 (3 witness sub-ids, sc-3, fa-1c, ra-3, cd-4b); T/R 7 (sc-1, ts-2a, ts-3d, ck-4b, ru-4c, br-3, br-4b); K 29; dropped 3 (rt-0, br-2b, ds-4d); OWED 0. The 11 anchors (T15) all land on rows: `:64` ts-3b, `:161`/`:162` cd-1, `:163` cd-4b, `:164` cd-4e, `:181`/`:484` cc-1, `:306` ds-2, `:347` rt-3, `:482` ts-3c, `:483` cd-2. No anchor stands in a K line (E-5).

### §3.2 The over-claims, each resolved on the body

| seg | over-claim | body | resolution |
|---|---|---|---|
| br-2 | "severity DERIVED" | `validate_artifacts.py:457-461` | br-2b dropped |
| cd-3 | "inherited from your plan row" | `check_case_form` reads no plan row | K; §3.3 |
| rt-5 | "in order" | presence only | CUT |
| rt-1 | the parent-feature clause on `check_register` | `check_witness.py:53-57` | witness sub-id row |
| ds-4 | `left_items` | not read | K |
| t-1036 finds | ru-1, ru-3, br-1, br-4, cd-2, au-4 | §3.1 | resolved in §3.1 |
| t-1041 finds | ts-1 (starter policy only), ts-2b (MUTATING), ts-3a (both flags), cd-4 (one case per row; never raise), ck-2 (`cause:`), fa-1a (NO_DEFECT also surprises; NOT_EXECUTED origin), fa-1f (`fix_result` presence), ds-1 (block list incomplete), ds-6a (no S8 check), ra-3 (unknown keys; `delta`/`hit`) | §3.1 rows | each resolved in §3.1 |

### §3.3 The `check_case_form` sentence correction

Row `validate_artifacts:check_case_form` (`stage-joints.json:4015` at e9d6195b). The requirement becomes (replaced):
"A case dated on or after the form cutoff carries `task`, `covers`, `defect_class` and `basis`; `covers` names only `R-n` ids the task's register holds (or `legacy:<import reason>`); `basis` follows the oracle grammar."
Body: `CASE_FORM_REQUIRED` `:59`, `:380-385`; covers `:386-401`; basis `:402-407`; called after the cutoff `:214-215`. Invariant: the row claims nothing the body does not check.

### §3.3b `planning_contract:contradictions` (fork R3-F1, recommended (a))

Row `stage-joints.json:5790-5814`; today: "No two plan rows contradict each other on the same requirement." The body checks something else: every requirement the register's matrix records as contradicted is covered by a plan row, and at least one of its rows carries a flag (`planning_contract.py:1485-1504`). Replacement:
"Every requirement the register's matrix records as contradicted is covered by a plan row, and at least one of those rows carries `source_conflict: true` or `oracle_unknown: true`."
Invariant: no row claims a check the body does not run. The door stays.

### §3.3c `manifest_put:expectation_changes` (fork R3-F1, recommended (a))

Row `stage-joints.json:3883`; the words "critic_verdict is a list" are replaced by "critic_verdict is one word of `expectation_change_verdicts`" (`manifest_put.py:156, 1292-1296`). The rest of the sentence stays; ck-3b is appended after it (R-2). Invariant: the row and ck-3b's "ONE verdict" never contradict on one page (E-8).

---

## §4 Rows the node adds beyond the cards

| id | roles / stages / when / door_needs | requirement (full) | door | body |
|---|---|---|---|---|
| `s5_precheck:sides.provisional` | qa-automator / S5 / window, shell / shell | r1 §4 text, unchanged | r1 §4 text | `_sides_provisional` (r1 2085-2149; critic t-703: matches; line numbers on today's tree NOT re-read; the builder cites them) |
| `s5_precheck:sides.pending` | same | r1 §4 text | r1 §4 text | `_sides_pending` (same caveat) |
| `execution_request:profile.none` | the four `--mine` producer roles of `execution_request:profile` (`stage-joints.json:6301-6328`) / S5, S6, S7 / shell / shell | r1 §4 text | r1 §4 text | r1: `execution_request.py` 1790-1797 (not re-read) |
| `execution_request:fingerprint.build` (finish F-5 (a)) | same four / S5, S6, S7 / shell / shell | "The inputs of a `--mine` run can be fingerprinted when it is built: every test, helper, config and dependency file it reads exists and keeps its bytes while it is hashed, and the stand's runtime provenance is `matched`, confirmed by the person, `not_applicable`, or a probe that compared nothing." | "report it in your digest, and write this one run with `run_suite.py --template request`" | re-read t-1041: the build site `execution_request.py:3761-3771` (`MineRefusal` "could not be fingerprinted"); the provenance set `:173-179`; sub-id of the sited `execution_request:fingerprint` (`:204, 209`) |
| `handoff_check:cli.values_rename` (R2-F7 (a)) | the 12 roles of `handoff_check:cli` (`:5686-5699`) / `*` / always / — | "The waiting values file `<dispatch>.values.yaml` can be renamed `<dispatch>.values.applied.yaml` once the form is written." | "delete the values file the refusal names, then run the check again" | re-read t-1041: `handoff_check.py:3199-3209` (OSError, refusal under `handoff_check:cli`, its door "delete <values file>"). The site re-point: residual node |

Sited parents of the sub-ids are measured by `stage_joints.py --check` after -a (P-3).

---

## §5 Edges (each with its invariant)

- **E-1 no clause unaccounted.** Every clause of §3.1 has a row, a K line, a T/R or a named drop; no OWED remains. Invariant: no card clause leaves the package with neither a row, a K line nor a named drop; the card stays the carrier until -b.
- **E-2 TEMPORAL, between -a and -b.** After -a a page carries the landed rows AND the card under `### Not yet in rows` (told twice); after -b once. -a creates the rows, -b removes the card group. Invariant: a role is never told less at any moment.
- **E-3 TEMPORAL, a story started before.** A brief already written keeps its ahead section; a brief written after -b has none. Invariant: one plugin generation per run (B-014).
- **E-4 POSITIONAL, append order.** Landed clauses go AFTER the row's existing sentence, in card order; a BRIDGE replaces the clause's own words only; §3.3, §3.3b, §3.3c replace their sentence (§3.3c only its words "critic_verdict is a list"). Invariant: no other T1r sentence is reworded; one door per told line (R-6).
- **E-5 charter anchors.** A K line must not create a second occurrence of a role-rules anchor in its charter; no anchor is in a K clause; the builder runs `role_rules.py --check` after the K lines. Invariant: role_rules stays at 0 findings; a collision is a STOP naming the line.
- **E-6 empty / absent.** `ahead-cards.json` absent or unreadable after -b: red "cannot be counted", never 0; `cards: {}` reads 0. No landed text is empty.
- **E-7 quarantined readers.** After -b the five quarantined files may go red in `quarantine-check`; they are not edited; -b's report names each; the Lead tells the owner the same turn on `TEST QUARANTINE ALERT`. Invariant: no quarantined file is edited.
- **E-8 conflicting requirements.** "Append verbatim" against "only what the body checks": AR-29 wins through cuts and BRIDGE texts (R2-F2 (a)). ck-3b "ONE verdict" against the row's "is a list": the row is corrected (§3.3c). Invariant: no page says two contradicting things about one field.
- **E-9 caps** (the owner's word 17.11.2026 by Q-O1, carrier: finish spec "Слово владельца 17.11.2026 по Q-O1"): "не в ущерб правилам. Если не влезет можно поднять". Rule text is NEVER cut to fit. A page at or over W is SPLIT (continuation lines `-2`, `-3`, … until no page reaches W). A role over `native_headroom`, `ratchet_tokens` or `process_ratchet_tokens` gets the row RAISED to the measured value with a record: one report row and one commit line `raise: <role> <key> <old> -> <new> (+<bytes> B) -- <why>`. Past the Codex hard ceiling (`native_context.py:174`): R2-F6 (a) - go on, name the bytes past 100,000, the Lead tells the owner the same turn. Invariant: no sentence truncated; no raise unnamed (AR-20).
- **E-10 a row whose role lacks a shell.** A `door_needs: shell` row (ra-3, ck-3b's row) is told only to a role with Bash (T14: both have it). The NEW rows told to no-Bash roles (cd-4b) carry field doors. Invariant: a no-shell role never sees a shell door (FR-2).
- **E-11 error direction of the reused reader** `contract_slices.handoff_keys_pages` (P-4) as the reader of the test pins and the witness. It may err toward "absent" (red); never toward "present" on text the role does not receive. Adversarial inputs that stay red: a clause only on a page `inject-map.json` does not list for the role (`handoff_keys_pages` returns only listed pages); a clause only on another role's page; a clause only inside the card group under `### Not yet in rows` (the -a witness matches only a told line beginning `- [<row id>]`; -b checks after hand_cards 0).
- **E-12 the integration tree (P-1).** -a merges main after the T7a-B/C integration; a row whose producers the integration narrowed keeps the narrowed list, and ROLE+ adds to it. Invariant: -a never re-widens a producer list it did not name.

---

## §6 The cards (R2-F1 (b), decided: cut by TIME)

Gate for -b: -a merged. Nothing in either card depends on an OWED clause.

### Card T1r-cards-a - clauses land on rows (wave C)

given:
- `C:\QAFactory\forge-repo\docs\tasks\specs\20261117-told-before-work-t1r-cards-spec-r2.md` §1, §3, §4, §5, §9
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\design\factory-rules.md` whole; `C:\QAFactory\forge-repo\plans\builder-rules.md`; `C:\QAFactory\forge-repo\docs\TESTING.md`
- `PKG/references/ahead-cards.json:1-95` (read only); `PKG/design/role-rules.json` lines 64, 161-164, 181, 306, 347, 482-484 (read only, for the `role_rule` ids)
- `PKG/references/stage-joints.json`, only the rows named in §3.1, §3.3-§3.3c and §4 (Grep `"check": "<id>"`) and `told_ratchet` `:8126-8130`
- `PKG/references/role-load.json` whole; `PKG/references/inject-map.json` (the 12 page lines)
- `PKG/scripts/stage_joints.py:74-95, 340-341` and `told_line`; `PKG/scripts/contract_slices.py:786-830` (`handoff_keys_pages`, K8) and `keys_write`
- the charter sections named in §3.1 (`## Tools` / `## Techniques` only)
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\stage-joints.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\slices\
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\inject-map.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\role-load.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\agents\qa-scout.md
C:\QAFactory\forge-repo\ai-packages\qa-factory\agents\qa-requirements-tester.md
C:\QAFactory\forge-repo\ai-packages\qa-factory\agents\qa-test-strategist.md
C:\QAFactory\forge-repo\ai-packages\qa-factory\agents\qa-case-designer.md
C:\QAFactory\forge-repo\ai-packages\qa-factory\agents\qa-automator.md
C:\QAFactory\forge-repo\ai-packages\qa-factory\agents\qa-code-critic.md
C:\QAFactory\forge-repo\ai-packages\qa-factory\agents\qa-failure-analyst.md
C:\QAFactory\forge-repo\ai-packages\qa-factory\agents\qa-doc-scribe.md
C:\QAFactory\forge-repo\ai-packages\qa-factory\agents\qa-bug-reporter.md
C:\QAFactory\forge-repo\ai-packages\qa-factory\agents\qa-retro-analyst.md
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\tbw-t1r-cards-a.md (new)
owns scope (per path, in order): stage-joints.json - the rows of §3.1, §4 and the sentences §3.3-§3.3c, NOT `told_ratchet`; slices - only through `contract_slices.py --write`; inject-map.json - continuation page lines only; role-load.json - `ratchet_tokens`, `process_ratchet_tokens`, `native_headroom` values only; each charter - only the K lines §3.1 names in its `## Tools` / `## Techniques` (qa-runner.md and qa-case-critic.md get none).
non-goals: `ahead-cards.json`, `role-rules.json` (-b); `told_ratchet` (hand_cards: -b; unsited and the K12 pin: integrator, finish F-1 (a)); every test file (no committed test in -a, R3-F3 (a)); any script code (the sites of `source_preflight`, `estimate_record`, `artifact_producer`, `gate_preflight`, `handoff_check`: residual siting node, R2-F3 (a) / R2-F7 (a)); the five quarantined tests; slow files run locally; CI; a new test file.
handoff: the branch commit plus `C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-tbw-t1r-cards-a-report.md`: a line per seg of §3.1 (final row id, K file:section added or skipped by its fact, T row, or drop); the unsited before -> after with the new unsited ids for the integrator; K8 page sizes; K10 U/H per role before/after; the raise records (E-9); the FR walk; the DOC-DISPATCH script in full with its run and its negative control; the verbatim witness.
edges: §5 E-1, E-2, E-4, E-5, E-8, E-9, E-10, E-11, E-12.
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for references/stage-joints.json references/inject-map.json references/role-load.json agents/qa-scout.md agents/qa-requirements-tester.md agents/qa-test-strategist.md agents/qa-case-designer.md agents/qa-automator.md agents/qa-code-critic.md agents/qa-failure-analyst.md agents/qa-doc-scribe.md agents/qa-bug-reporter.md agents/qa-retro-analyst.md` - run each printed file that is not in `slow_tests.json` and not quarantined, each alone; list the slow ones as "judged by the batch canon". Then, each verbatim in the report:
- `python -B ai-packages/qa-factory/scripts/contract_slices.py --write`, then `python -B ai-packages/qa-factory/scripts/contract_slices.py --check` (clean, no `WARN K8`)
- `python -B ai-packages/qa-factory/scripts/stage_joints.py --check` (clean except the new unsited ids, which the report names)
- `python -B ai-packages/qa-factory/scripts/role_rules.py --check` (0 findings)
- `python -B ai-packages/qa-factory/scripts/tests/test_role_load.py`
- `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`
- DOC-DISPATCH witness (CLAUDE.md rule 11): a script in the scratchpad, attached in full, never committed. Its keys are quoted verbatim from §3.1 before the run: per landed seg the triple (role, row id, landed text). It passes a key when (1) the row's `requirement` in stage-joints.json contains the text and (2) a line of `"\n".join(contract_slices.handoff_keys_pages(plugin_root, role))` begins with `- [<row id>]` and contains the text. Negative control: on a byte copy of `stage-joints.json` with ru-2's landed text deleted, the script reports ru-2 as failing; the copy is the only file corrupted (CLAUDE.md pt.7 (d)).
- test: none -- the landed rows and K lines are data and charter text; their rendering is judged by `contract_slices --check` and `stage_joints --check`, and the closed lists they quote are joined to code by the rows card -b re-points | expected from: §3.1 of this spec
- census: no new blocking unit.
siblings: axis 34 (one road: ROLE+ not sub-ids; family rows first); the T1r EC-8 lines of t-979 K5 go to node "TBW-T1rc-ec8" (Lead decision), not here; `design/factory-rules-debt.md` "All twelve have a card now" (closing node); `estimate_record.append_record` writes no `delta`/`hit`/`ts` while the card names them (analog, reported).
designer: `C:\QAFactory\forge-repo\docs\tasks\specs\20261117-told-before-work-t1r-cards-spec-r2.md` (once accepted)

Items:

| # | what | expected | proof (expected value from) |
|---|---|---|---|
| A-1 | Measure before: the four `--check` runs | verbatim in the report | report |
| A-2 | Land every clause of §3.1 by its "how" | each landed text stands in its row exactly as the table gives it | DOC-DISPATCH witness keys (§3.1, this spec) |
| A-3 | §3.3, §3.3b, §3.3c sentences (§3.3b/c on R3-F1 (a)) | replaced | witness keys (the replacement texts, this spec) |
| A-4 | §4 rows (5) and the 7 NEW rows of §3.1 | rows exist in the R-4 form, told on the roles' pages | witness keys; `stage_joints.py --check` |
| A-5 | K lines | appended or skipped by the distinctive fact | report line per K; `role_rules.py --check` 0 |
| A-6 | pages | `--write`; split until no page reaches W; continuation lines in the same commit | `contract_slices.py --check` clean |
| A-7 | caps (E-9) | raised to the measured value, named | report raise table; A22 / K10 green |
| A-8 | changelog | one English ASCII bullet | `selftest.py --lang` |

### Card T1r-cards-b - the cards retire, readers re-point (wave C, after -a)

given:
- this spec §1, §5, §6 -b
- `PKG/references/ahead-cards.json` whole; `PKG/design/role-rules.json` lines 64, 161-164, 181, 306, 347, 482-484
- `PKG/scripts/contract_slices.py:786-830` (`handoff_keys_pages`) and the card group
- `PKG/scripts/tests/test_ahead_cards.py` whole; `test_validator_class.py:40-60, 190-240, 500-545`
- `test_env_evidence.py:160-180`; `test_oracle_provenance.py:325-345`; `test_question_branches.py:1770-1795`; `test_s7_rejudge.py:100-120`
- `test_contract_slices.py:640-665, 820-830`; `test_stage_joints.py:934-960`
- `C:\QAFactory\forge-repo\docs\TESTING.md`; `C:\QAFactory\forge-repo\plans\builder-rules.md`; `PKG/design/factory-rules.md`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\ahead-cards.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\stage-joints.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\design\role-rules.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\slices\
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\inject-map.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\role-load.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_ahead_cards.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_validator_class.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_env_evidence.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_oracle_provenance.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_question_branches.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_s7_rejudge.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_contract_slices.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_stage_joints.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\tbw-t1r-cards-b.md (new)
owns scope (per path, in order): ahead-cards.json - `cards` -> `{}`, `note` rewritten as r1 C-4; stage-joints.json - `told_ratchet.hand_cards` 12 -> 0 only; role-rules.json - in the 11 rows (T15), only the carrier entry whose `file` is `references/ahead-cards.json`, re-pointed to the page file that holds the anchor after -a (`references/slices/<role>/handoff-keys*.md`); slices - only through `--write`; inject-map.json - continuation lines that became empty may go; role-load.json - values lowered to the measure only; test_ahead_cards.py - the `cards()` reader, the `main` card blocks and the brief block (NOT `charter_card_join`, `role_text_roots`); test_validator_class.py - the `told_text` "card" branch only; test_env_evidence `:171`, test_oracle_provenance `:335`, test_question_branches `:1780`, test_s7_rejudge `:109` - the one read each; test_contract_slices.py - the real-tree card rows `:660-662` only; test_stage_joints.py - the told-counter loop `:938-955` only.
non-goals: `brief_pack.py` / `contract_slices.py` / `stage_joints.py` code (T3b; closing); the five quarantined files (E-7); `told_ratchet.unsited` and `UNSITED_CAP`; any row sentence; a new test file; a new variant row.
handoff: the commit plus `C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-tbw-t1r-cards-b-report.md`: the re-point per reader (file:line, old -> new carrier); the role-rules re-points (id, new file); the deleted rows (file:line, why: behaviour removed); the shrinks (key, old -> new); the quarantined readers' state; the verbatim witness.
edges: §5 E-2, E-3, E-6, E-7, E-11; plus E-b1: a pin whose clause landed as K reads the charter (`agents/<role>.md`), never the page; invariant: a pin reads the carrier that really holds the words. E-b2 (P-2): at stored `hand_cards` 0 the told loop of test_stage_joints takes the floor form already written for legacy_legs (`:943-948`: the stored number is 0; one more than 0 is red naming the counter; -1 is red by the shape check) for every counter whose stored number is 0; invariant: the loop never asserts a message the audit cannot print, and a counter above its stored number stays red.
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for references/ahead-cards.json design/role-rules.json references/stage-joints.json references/role-load.json references/inject-map.json scripts/tests/test_ahead_cards.py scripts/tests/test_validator_class.py scripts/tests/test_env_evidence.py scripts/tests/test_oracle_provenance.py scripts/tests/test_question_branches.py scripts/tests/test_s7_rejudge.py scripts/tests/test_contract_slices.py scripts/tests/test_stage_joints.py` - run every printed file not in `slow_tests.json` and not quarantined, each alone; slow ones (test_s7_rejudge, test_contract_slices, test_stage_joints): "judged by the batch canon". Then, each verbatim in the report:
- `python -B ai-packages/qa-factory/scripts/contract_slices.py --write`, then `python -B ai-packages/qa-factory/scripts/contract_slices.py --check` (clean)
- `python -B ai-packages/qa-factory/scripts/stage_joints.py --check` (`told counters: hand_cards 0, legacy_legs 0, unsited <the integrator's number>`)
- `python -B ai-packages/qa-factory/scripts/role_rules.py --check` (0 findings)
- `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`
- test: test_ahead_cards.py::the VOCABULARIES / quoted-numbers / B-194 / expectation-field table, re-pointed to `told_text_of(role)` | expected from: the code constants each row already names (`C.RELATED_KINDS`, `V.TEST_REPORT_MAX_BYTES`, `manifest_put.VERDICTS_LIST`, `estimate_record.FACTS_KEYS`, …), never the page
- test: test_validator_class.py::the `told_text` rows `:198-210` | expected from: the carrier constants they already name (`artifact_producer.TRIAGE_ROW_IDS`, `estimate_record.FACTS_KEYS`, the scout's field lists)
- test: test_stage_joints.py::told/hand-cards-* (E-b2) | expected from: `told_ratchet.hand_cards` 0 (this spec, B-2) and the floor form `:943-948`
- census: no new blocking unit.
siblings: T3b (`brief_pack.ahead_card` dead at 0, removed in T3b); closing (`contract_slices` `ahead_card` / `CARD_GROUP` / `NOT_YET_HEAD`); axis 34.
designer: same path as -a.

Items (one parameterised row per behaviour; existing tables only):

| # | what | row / proof | expected value from |
|---|---|---|---|
| B-1 | `cards: {}`, the note rewritten | `stage_joints.py --check` (dense counter, hand_cards 0); no test row (a count already judged by the audit) | data |
| B-2 | hand_cards 12 -> 0 | `stage_joints.py --check` summary | the measure |
| B-3 | 11 role-rules re-points | `role_rules.py --check` 0 | anchors unchanged (T15) |
| B-4 | `told_text_of(role)` = `"\n".join(contract_slices.handoff_keys_pages(plugin_root, role))` (P-4: all listed pages); the existing VOCABULARIES / quoted numbers / B-194 / expectation-field rows read it instead of `cards()` | existing rows of test_ahead_cards.py | the code constants, never the page |
| B-5 | brief rows `:343-364` (the ahead section present) | DELETED, not inverted: the behaviour is removed and its code goes in T3b (TESTING "Когда тест покраснел" 1; an "absent" row is a test of dead code) | — |
| B-6 | sizes go down (card group gone) | report shrink table | the measure |
| B-7 | test_validator_class `told_text(("card", r))` -> `told_text_of(r)`; a K-landed pin reads the charter (E-b1) | existing rows | carrier constants |
| B-8 | env_evidence / oracle_provenance / question_branches / s7_rejudge reads -> `told_text_of` of the same role | existing rows | unchanged expectations |
| B-9 | test_contract_slices `:660-662` real-tree card rows | DELETED (the card group no longer renders at hand_cards 0; synthetic card-group rows stay until the closing removes the code) | — |
| B-10 | test_stage_joints told loop (E-b2) | existing loop rows | §B-2 and `:943-948` |
| B-11 | changelog bullet | `selftest.py --lang` | — |

---

## §7 Order lines (collisions with work in flight)

- `очередь: K1b -> T1r-cards-a -> T1r-cards-b`. K1b writes `stage-joints.json` told markers, the slices, `inject-map.json`, `role-load.json` and `test_contract_slices.py`. -a measures caps after K1b lowered `native_headroom.qa-code-critic`.
- `очередь: T7a-B / T7a-C (integrated on branch worktree-agent-ad0767bec786dddde) -> T1r-cards-a`. Read t-1041 (may be stale): the integration tree holds every row id of §3.1/§4 at the same line as main; `unsited` 17 there (`stage-joints.json:8129`); the sampled rows' producers are unchanged (`:1874-1889`, `:5684-5699`, `:6301-6328`). Rows of this table that a T7a census narrowing can touch: every `validate_artifacts:*` row of §3.1 (sc-1, sc-2, rt-1a/c, rt-3, rt-5, cd-2, cd-4c/e, §3.3, ru-2, ru-3b, ru-4a, ru-5, ru-6, fa-1a/d/e/f, ds-1..ds-6b, br-1b..br-4a) and the shared rows `guard_pre_tool:PT-external-writes`, `handoff_check:required_rows`, `handoff_check:cli` (T rows br-3, br-4b and §4 values_rename). The exact list is P-1 (Lead, git). E-12 applies.
- T4b, T9a: no shared file; no order needed.
- T9c (new conductor rows in `stage-joints.json`): either merges first; the later one merges main and keeps both.
- `очередь: T1r-cards-b -> T3b` on `test_ahead_cards.py` (-b deletes the brief rows; T3b removes `brief_pack.ahead_card`).
- `очередь: T1r-cards-b -> closing (wave D)`.
- Residual siting node (R2-F3 (a) / R2-F7 (a)): after -a. Owns `source_preflight.py`, `estimate_record.py`, `artifact_producer.py`, `gate_preflight.py` (on R3-F2 (a)), `handoff_check.py` (the rename site), plus `test_detector_verdict.py` (a new row in its table).

---

## §8 Forks

R2-F1..R2-F7 are decided (status column; text kept for the trail). R3-F1..R3-F3 are new (t-1041), recommendation first; the cards follow the recommendation.

| # | question | options | recommendation | status |
|---|---|---|---|---|
| R2-F1 | Where is -a / -b cut? | (b) BY TIME · (a) X9's cut · (c) one node | (b) | decided (b), Lead 17.11 |
| R2-F2 | BRIDGE texts | (a) designer bridges checked by the plan critic · (b) cuts only | (a) | decided (a), Lead 17.11 |
| R2-F3 | Clauses whose check has no row | (a) NEW rows, a named unsited raise, a residual siting node · (b) K lines | (a) | decided (a), Lead 17.11 |
| R2-F4 | A role meeting another role's row (ck-3b) | (a) ROLE+ · (b) sub-id per role | (a) | decided (a), Lead 17.11 |
| R2-F5 | Witness clauses | (a) sub-ids of `exit_gate:witness_errors` per role · (b) M2 on the aggregator · (c) `check_witness:<fn>` | (a) | decided (a), Lead 17.11 |
| R2-F6 | The owner's raise and the Codex ceiling | (a) go on, name the bytes, tell the owner · (b) stop | (a) | decided (a), Lead 17.11 |
| R2-F7 | t-979 F5 rename failure | (a) sub-id row + residual site re-point · (b) widen `cli` · (c) class it | (a); other EC-8 lines -> node "TBW-T1rc-ec8" | decided (a), Lead 17.11 |
| R3-F1 | Two more T1r row sentences are false against their bodies (§3.3b `planning_contract:contradictions`, §3.3c `manifest_put:expectation_changes` "is a list"). Correct them here? | (a) correct both in -a (same file, same class as §3.3; a critic checks the texts) · (b) leave the sentences and queue a finding (then ck-3b cannot land: E-8, it goes K) | **(a)**: -a already owns those rows and appends to the second one; (b) leaves a page that contradicts itself (FR-10). Cost: two replaced sentences | open |
| R3-F2 | cd-4b (`unverifiable` row owes a case, the S4 `question_thens` form) has no row: its check is `variant_errors` called by `gate_preflight.py` `question_branches` at S4. Apply R2-F3 (a) to a fourth clause? | (a) NEW row `gate_preflight:question_branches` (R2-F3's road; the named unsited raise becomes +4, not +3; `gate_preflight.py` joins the residual node's owns) · (b) K line in `qa-case-designer.md` and the role-rules carrier at `:163` re-pointed to the charter in -b | **(a)**: the same decided road; keeps the anchor on a row (E-5) and tells the designer the S4 check before work. Cost: one unsited id, one site in the residual node | open |
| R3-F3 | How -a proves the landing (TESTING: no receipt per key, no role-text pin) | (a) no committed test in -a; a DOC-DISPATCH witness (keys from §3.1, script attached, negative control); the durable joints are the -b re-pointed rows · (b) a committed parameterised table `t1rc_clauses_on_page` in test_ahead_cards.py, one row per landed row, expected from §3.1 | **(a)**: TESTING `:135-140` lists "receipt per key" and "role-text pin in references/*.md" as not written; the rows' rendering is already judged by `contract_slices --check`. Cost of (b): about 40 rows that redden on every legal rewording | open |

---

## §9 Premises

| P | what | result |
|---|---|---|
| P-1 | the T7a-B/C integration branch: rows it changed, its `unsited` | STILL OWED (git): `git -C C:\QAFactory\forge-repo diff main...worktree-agent-ad0767bec786dddde --stat -- ai-packages/qa-factory/references/stage-joints.json`, then the hunks of the rows §7 lists. Read t-1041 of the tree itself: ids and lines equal to main, `unsited` 17, sampled producers equal (may be stale). Without it, -a runs on E-12 (merge main after the integration, keep narrowed producers) |
| P-2 | test_stage_joints follows the stored hand_cards | read, t-1041: NO at 0 (`:950-952` sets -1); -b owns the loop (E-b2) |
| P-3 | sited parents of the new sub-ids | measured by -a's `stage_joints.py --check` (not a pre-dispatch premise) |
| P-4 | does `handoff_keys_page` return continuation pages? | read, t-1041: no; `handoff_keys_pages` does (`contract_slices.py:786-795`) |
| P-5 | sc-3 | read, t-1041: lands with a bridge (`source_preflight.py:21-34`) |
| P-6 | `question_owners()` | read, t-1041: holds (`vocabulary.yaml:151`) |
| P-7 | ts-1, ts-3a, ts-3b | read, t-1041: split (ts-1a bridge + ts-1k K; ts-3a K; ts-3b/c/d) and §3.3b |
| P-8 | MUTATING | read, t-1041: not checked -> K |
| P-9 | severity suggestion in the charter | read, t-1041: holds (`qa-bug-reporter.md:26, 47`) |
| P-10 | the def behind cd-4 | read, t-1041: `contract.then_oracle_errors` and `planning_contract.variant_errors` -> split, R3-F2 |
| P-11 | cc-1 vs `critic_rollcall.py` | read, t-1041: holds |
| P-12 | au-1, au-2b, au-3 | read, t-1041: au-1, au-3 land; au-2b split (au-2c on `s5_precheck:oracle`) |
| P-13 | the owner of `cause:` | read, t-1041: none -> K |
| P-14 | `critic_verdict` one or a list | read, t-1041: one word; the row sentence is corrected (§3.3c) |
| P-15 | `--then-quote` in role-commands | read, t-1041: holds -> ru-4c dropped |
| P-16 | NO_DEFECT / NOT_EXECUTED; 300 | read, t-1041: NO_DEFECT bridge, NOT_EXECUTED K, 300 holds |
| P-17 | the def at `artifact_producer.py:104` | read, t-1041: `validate` |
| P-18 | `REPORT_BLOCKS`, 11 sections | read, t-1041: 11 holds; block list bridged |
| P-19 | who runs `report_facts --check` | read, t-1041: the S9 exit -> K |
| P-20 | shells of bug-reporter, retro-analyst | read, t-1041: both have Bash |
| P-21 | the `gate_b` row | read, t-1041: T + K line |
| P-22 | `facts_problems` | read, t-1041: bridge; `delta`/`hit` cut to K |

Still owed (reading cannot settle): P-1 only (command above; the cards do not wait for it, E-12).

---

## §10 Readers of every touched file (designer rule 7)

Greps (Grep tool, count mode unless noted; t-1036 lines kept, t-1041 lines added):

| search | over | hits | positive control (same shape) |
|---|---|---|---|
| `ahead-cards\|ahead_card\|stage-joints\|role-rules\.json\|role-load\.json\|inject-map` (t-1036) | `tools/` | 2 (`tools/test_quarantine.py:2199`, `tools/test_test_quarantine.py`) | itself |
| same (t-1036) | `.githooks/` | 0 | the tools/ run |
| `agents/qa-\|agents\\\\qa-\|agents/\*\.md\|qa-factory/agents` (t-1041) | `tools/` | 10 in 7 files - every hit is `.claude/agents/*.md` (forge roles: `agents_md.py`, `dispatch_gate.py`, `install_parity.py`, `owns_readers.json:31`, `permission_audit.py`, two tests); 0 name a package charter (content run of `agents/qa-\|qa-factory/agents`: 0) | the same count run found the 10 |
| same (t-1041) | `.githooks/` | 0 | `test_ahead_cards\|test_stage_joints\|python` over `.githooks/`: 15 |
| `agents/qa-\|qa-factory/agents\|test_ahead_cards\|…` (t-1041) | `.claude/settings.json` | 0 | `agents/qa-\|qa-factory/agents\|tools/`: 37 |
| same | `.claude/agents/` | 0 | `…\|builder-rules`: 3 |
| same | `.claude/skills/` | 0 | `…\|CLAUDE\.md`: 15 |
| same | `.claude/hooks/` | path does not exist (the hooks live in `tools/`, named by `settings.json`) | — |
| the 8 test file names (t-1041) | `tools/` | 1: `tools/lint-baseline.json:247` (`test_oracle_provenance.py`, class `HandReaderInput`, count 1) | — (one hit) |
| `owns_readers` (t-1041) | `tools/` | 6 files: `owns_readers.py`, `dispatch_new.py`, tests | — |

The `.claude/` whole-folder search times out (the worktrees under `.claude/worktrees/`); the narrowed paths above cover the settings, roles and skills.

| touched file | readers | verdict |
|---|---|---|
| `stage-joints.json` | `stage_joints.py`, `contract_slices.py`, `selftest.py:722`, `tools/test_quarantine.py:2199`, refusal transports; `tools/owns_readers.py` scope "data" (`owns_readers.json:17`) | unchanged code; rows in -a, hand_cards in -b; T9c and the integrator also write (§7) |
| `ahead-cards.json` | `stage_joints._hand_cards`, `contract_slices.ahead_card`, `brief_pack.ahead_card`, the test readers (T10); `owns_readers.py` scope | -b changes data and the keep readers; quarantined: E-7 |
| `role-rules.json` | `role_rules.py`, test_role_rules; `owns_readers.py` scope (`:21`) | -b re-points 11 carrier entries |
| `slices/*` | the injection (inject-map lines), role_load (K10, A22), role_rules (anchors on pages) | regenerated in -a and -b |
| `inject-map.json` | `inject_context.py`, role_load, contract_slices K8 | continuation lines in -a (and -b if emptied) |
| `role-load.json` | `role_load.py`, test_role_load | values in -a (raise), -b (shrink); K1b first |
| `agents/qa-*.md` (K lines) | the host loads them; `host_adapter.role_has_bash` reads the `tools:` line (`:519-522`, untouched by K lines); role_load (charter layer); role_rules (anchors); `test_ahead_cards.charter_card_join`. tools/.githooks/.claude: none (above) | -a |
| `test_ahead_cards.py` | `test_validator_class.py:47` imports `VOCABULARIES` and `cards()`; `owns_readers.py` scope "tests" | -b (same commit as test_validator_class); -a does not touch it (R3-F3 (a)) |
| `test_oracle_provenance.py` | `tools/lint-baseline.json:247` (a `HandReaderInput` count of 1) | -b edits the `:335` read; the lint baseline is a batch-level ratchet: a changed count is named in -b's report, never raised silently |
| the other -b test files, `test_stage_joints.py` | `owns_readers.py` scope "tests"; `slow_tests.json` (slow ones) | -b; slow ones judged by the batch canon |

---

## §11 Small choices closed by the designer

- S-1 Report files `20261117-tbw-t1r-cards-{a,b}-report.md`; changelog fragments `tbw-t1r-cards-{a,b}.md`.
- S-2 K section by kind: procedure -> `## Tools`, craft and rationale -> `## Techniques`.
- S-3 Witness sub-id suffix = the role name without `qa-`.
- S-4 Row ids for the function-level NEW rows: `artifact_producer:validate` (the function, per R2-F3's template) and `gate_preflight:question_branches` (the gate's own check name, `gate_preflight.py:2113`).
- S-5 Door text of a NEW witness row: "edit the field the refusal names in <artifact>".
- S-6 (t-1041) Where a card clause was split by bodies, the split keeps card order inside each row (R-2).
- S-7 (t-1041) The test reader is `handoff_keys_pages` joined by "\n" (P-4).

## §12 Not done / not established

- P-1 (the integration branch diff) is a git command: listed in §9 "Still owed".
- The §4 rows `s5_precheck:sides.*` and `execution_request:profile.none` rest on r1 and critic t-703 line numbers; their bodies were not re-read (not in this brief's item 4).
- `raise_question_errors` (cd-4d) and `completeness` of `source_inventory` were not opened; both clauses are placed on the safe side (K, or a bridge that names only what the read lines check).
- `exit_gate:witness_errors` as a sited parent of the three sub-ids: P-3, measured by -a.

## §13 Reading trail

t-1036 (main d41bcdd0): see its list - r1 whole; critic t-703; finish spec 1-697; t-979 review 1-160; `ahead-cards.json`; many `stage-joints.json` ranges; `role-load.json`; `validate_artifacts.py`, `check_witness.py` 20-342, `contract.py` 2237-2506, `s5_precheck.py` 1030-1079, 1874-1923; `test_ahead_cards.py`; `test_validator_class.py`; `test_stage_joints.py` 924-945; `slow_tests.json`.
t-1041 (main = origin/main e9d6195b; loose refs read, no command): this file whole; `ahead-cards.json:1-95`; `source_preflight.py:1-80`; `planning_contract.py` 143-200, 1477-1511, 1855-1945, 2046-2125, def list (Grep), 3134-3142; `handoffs/vocabulary.yaml:140-151`; `check_witness.py:118-145`; `coverage_contract.py:321-390`; `observation_contract.py:118-143`; `agents/qa-bug-reporter.md` (Grep severity); `validate_artifacts.py:318-335, 452-465, 1226-1247, 1500-1523, 2490-2531`; `contract.py:1628-1742, 5012-5061`; `gate_preflight.py:2120-2170` and its check names (Grep); `critic_rollcall.py` (Grep of its constants, 588-637); `s5_precheck.py:1257-1331, 1786-1830, 3552-3771`; `manifest_put.py:1207-1309`; `role-commands.json:30-45`; `manual_evidence.py:40`; `artifact_producer.py:1-112`; `grammar.py:114-196, 272-276`; `stage_done.py:270-344`; `host_adapter.py:519-522` and `agents/*.md:4` (Grep); `handoffs/s8-bug-reporter-to-scribe.yaml` (Grep), `null-outcomes.json:130-132`; `estimate_record.py:60-124`; `test_stage_joints.py:920-962`; `contract_slices.py:786-832`; `handoff_check.py:3190-3216`; `exit_gate.py:1592-1751`; `execution_request.py:150-211, 3722-3790`; `role-rules.json` (Grep of the 11 carriers); `stage-joints.json` rows 1865-1900, 2978, 3266-3275, 3879-3904, 4041-4065, 4878-4891, 4982-4995, 5199-5280, 5764-5840, 6076-6126 and the touched-id Grep on both trees; integration tree `stage-joints.json` 1874-1889, 5675-5704, 6289-6332, 8127-8129; `test-layers.json` (Grep); `docs/TESTING.md` whole; `plans/builder-rules.md:26-85`; `tools/owns_readers.json` whole; `tools/lint-baseline.json:240-251`; the §10 greps. Greps that came back empty each carry a same-shape control (the `"check": "planning_contract:` form; brace globs in the Grep tool returned nothing and were re-run without them).
Needed beyond the manifest: `gate_preflight.py`, `stage_done.py`, `host_adapter.py`, `observation_contract.py`, `coverage_contract.py`, `execution_request.py`, `exit_gate.py`, `role-commands.json`, `null-outcomes.json`, `handoffs/*.yaml`, `tools/owns_readers.json`, `tools/lint-baseline.json`, the integration worktree.

## Lead decisions on forks R2-F1..R2-F7 (17.11.2026, Fable; по рекомендации, до слова владельца - the owner is away)

- R2-F1 (b) cut by time; R2-F2 (a) designer-written bridges, each checked by the plan critic; R2-F3 (a) new rows, a named
  unsited raise of +3 and a residual siting node; R2-F4 (a) ROLE+; R2-F5 (a) sub-ids of `exit_gate:witness_errors` per
  role; R2-F6 (a) go on past the Codex ceiling with the bytes named, the Lead tells the owner the same turn; R2-F7 (a)
  sub-id row `handoff_check:cli.values_rename`.
- The other EC-8 lines of t-979 K5 (`null_outcome.triage`, the PT-big-read split, the T6/T7b/T7a-A/T4a lines) go to a
  node "TBW-T1rc-ec8" of the pile, not into these two cards.
- The 15 OWED clause reads (P-5..P-22) and the readers of §10 go to a fresh designer (t-1041); then one plan-critic pass
  on the file; no builder before that.

## Lead decisions on forks R3-F1..R3-F3 (17.11.2026, Fable; по рекомендации, до слова владельца — the owner is away)

- R3-F1 (a): the false row sentences `planning_contract:contradictions` and `manifest_put:expectation_changes` are corrected in -a.
- R3-F2 (a): cd-4b gets the new row `gate_preflight:question_branches`; `unsited` +4, not +3.
- R3-F3 (a): -a proves landing by the DOC-DISPATCH witness; no committed test.
- Freshness: the package did not change in `e9d6195b..5123216d` (`git diff --stat -- ai-packages`, empty); after that main took
  the N2h-a merge `b1243561` (`scripts/tests/dry_stub.py`, `harness.py`, `story.json` only).
