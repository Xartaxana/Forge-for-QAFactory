# Told before work: T1r-cards, redraft r3 (designer t-1056, fix round of plan critic t-1046)

Status: DRAFT for Lead acceptance. Fix round of r2 (`20261117-told-before-work-t1r-cards-spec-r2.md`) after the plan critic
t-1046 (`docs/tasks/specs/reviews/t-1046-told-before-work-t1r-cards-r2-plan.md`, verdict `fit_with_fixes`). This file is
SELF-SUFFICIENT: a builder is given r3 alone, never r1 or r2. Every r2 card, rule and Lead decision is carried here with the
fixes applied; the table "Fix round t-1056" (end of file) maps F1-F15 to the sections. New forks: §8 (R4-F1..R4-F4, plus the
re-opened R2-F6', R3-F2', R3-F3'); both cards are executable on the recommendations until the Lead / the owner answers.

Read base (t-1056): the ROOT checkout `C:\QAFactory\forge-repo` working tree; `.git/HEAD` = `ref: refs/heads/main`;
`.git/refs/heads/main` = `c9b42659aa77e9f86f2883ca236bcf86fbb055ec` (`packed-refs` shows an older `905e9735` for both main and
origin/main; the loose ref wins). The package files are clean in `git status` (only docs/logs dirty), so the tree is main. I had
no shell (designer tools: Read/Grep/Glob/Write): every fact below is READ from its carrier; numbers that only a command prints
are labelled with the command and whose run they come from. `PKG` = `ai-packages/qa-factory`. Wave B: branch
`worktree-agent-ad0767bec786dddde`, loose ref now `f88a5e38` (critic t-1046 read it at `a65afe58`; NOT re-read here).

Lines re-checked at c9b42659 by this round (file:line, all equal to r2/critic unless stated): `stage-joints.json`
`told_ratchet` :8126-8129 (12/0/46), rows `exit_gate:witness_errors` :116, `exit_gate:grounding` :183, `exit_gate:case_identity`
:207, `critic_rollcall:*` :494, `s5_precheck:*` :517, `check_coverage:*` :540, `s5_precheck:manifest/bindings/oracle/environment`
:2922/:2974/:3000/:3053, `execution_request:fingerprint` :3266, `manifest_put:expectation_changes` :3879-3883,
`s5_precheck:sides.declared/settled/placeholders` :3907/:3933/:3961, `validate_artifacts:check_case_form` :4015,
`handoff_check:cli` :5675-5699, `planning_contract:contradictions` :5790, `execution_request:profile` :6289-6331;
`test_stage_joints.py` `UNSITED_CAP = 46` :927, told loop :938-955, `told/hand-cards-unreadable` :956-959;
`stage_joints.py` ROW_KEYS :74-75, `sited_ids` :321-337, `_is_sited` :340-342, door rule :1001-1002, `_told_counters`
:1130-1153, `_hand_cards` :1156-1164, `told_line` :603-608; `source_preflight.py` :7-55; `s5_precheck.py` `_sited` :294-301,
`_sides_provisional` :2104-2168, `_sides_pending` :2171-2198, `check_sides` add :2417-2418; `execution_request.py` :1795-1830,
:3750-3771; `execution_fingerprint.py` :73-151; `manifest_put.py` :156, :1084-1088, :1250-1309; `handoff_check.py` :3199-3209;
`check_witness.py` :36-58, :70-86, :121-143, :236-252; `planning_contract.py` :1477-1505; `validate_artifacts.py` :377-407,
:2485-2530; `native_context.py` :173-175; `role_load.py` :302-346; `contract_slices.py` :583-591, :681-691, :786-795;
`dry_exits.py` :1-19, :39-83, :521-532, :579-599, :636-760; `driver-exits/s1-s4.json` whole, ratchet blocks of all groups;
`role-rules.json` :161-165 and the ids of :64, :181, :306, :347, :482-484; `agents/*.md:4`; `ahead-cards.json` whole.

---

## §0 What r3 changes (summary; the full map is the closing table)

- F1 (blocking): card -a owns the four driver-exits group files and writes one census row per new joint (12), names every
  `unwalked` rise in `raised_by`, and runs `dry_exits.py --check` (A-9, §4.3, DoD).
- F2: the unsited raise is +6 (§4.4); every new row has a siting node (§7: TBW-T1rc-site, which now owns `s5_precheck.py`
  and `told-ratchet.json`).
- F3: §3.4 holds every landed text, door and K line in full as one JSON block; the supplementary key check reads it,
  its source is in §6 (S-K), with a negative control. The builder's witness is the `scenario_walk --witness-for` run.
- F4: §4 rows written whole from re-read bodies; `profile.none` door = the refusal's own (fork R4-F4); E-13.
- Own sweep (not in t-1046): the four M2 rows owe a `door` (`stage_joints.py:1001-1002`: "states a requirement and names
  no `door`"); r2 gave none -> §3.5. `fingerprint.build` "keeps its bytes while it is hashed" is not checked on the `--mine`
  build road -> cut (§4.1). The strategist charter line "follow the card's rule" (`agents/qa-test-strategist.md:74`,
  role-rules `strategist-letter-branch-follows-card` :165) points at the card -b retires -> fork R4-F2.

---

## §1 Architecture, owners, census (rule 10, AR-29, P27)

| AR | how the node keeps it | change check written into the DoD |
|---|---|---|
| AR-10 a requirement reaches the role before the work | every clause a body checks lands on a row told on the role's key pages | -a: S-K key check (row text + page line per §3.4 key); -b: the re-pointed joint rows read the pages |
| AR-29 code judges data; a judgment is judged by a tier above | a row says only what its body checks (R-2, E-13); clauses no body checks go to the charter (K). Whether a clause is checked is a designer judgment, accepted by the Lead and the plan critic | plan critic t-1046 on §3 (done); critic question 11 on the diff |
| AR-15 one survivor | after -b the page is the one told carrier | `stage_joints.py --check`: hand_cards 0 |
| AR-13 a reader function | tests and the key check read told text through `contract_slices.handoff_keys_pages(...)` (P-4), never by opening pages | critic: no second reader in the test diff |
| AR-14 one writer | rows and census rows: -a; hand_cards: -b; `told_ratchet.unsited` and the K12 pin: node TBW-T1rc-int (§7) | owns lists |
| AR-20 shrink-only ratchets | every move named: `unsited` +6 (§4.4) by TBW-T1rc-int; driver-exits `unwalked` +12 named in `raised_by`; caps per E-9; -b moves only down | ratchet table in each report; `dry_exits.py --check` notes |
| AR-22 a field read has a producer | every NEW row names a role that exists in `agents/` | `stage_joints.py --check` |
| AR-11 a role gets only the context it needs | K8/K10 measured per role; each raise named | `contract_slices.py --check`; `test_role_load.py` |
| AR-28 an unknown never becomes a pass | `ahead-cards.json` absent or unreadable stays red "cannot be counted"; a census row is `unwalked` with a why, never a claimed walk | E-6; `dry_exits.py --check` |

Checks added or altered (owner; census class):

| check | owner it serves | census class |
|---|---|---|
| row sentences appended or corrected (§3.1, §3.3, §3.3b, §3.3c, §3.5) | data (what an existing check checks); the truth of each sentence: judgment of the plan critic / Lead (tier above) | no census unit |
| NEW rows (§4.1: 12) | data: each describes a check that exists (bodies cited) | no new blocking unit (`judgment-census.json` untouched; critic t-1046 simulated K5 green) |
| driver-exits census rows (12, `unwalked`) | data (the dry census of axis 38) | ratchet `unwalked`, raises named |
| K charter lines | judgment: the role's own craft and procedure | no census unit |
| test pins re-pointed card -> page (-b) | data (closed lists in code = the text the role reads) | xref; test only |
| `told_ratchet.hand_cards` 12 -> 0 | data (count) | ratchet |
| `told_ratchet.unsited` +6 (TBW-T1rc-int) | data (count), named raise | ratchet |
| K10 / A22 raises | intent: the owner's word 17.11 (E-9); the Codex ceiling case: owner question R2-F6' | ratchet; named record |

Commit lines: the form is `tools/architecture_gate.py`'s (point there; not copied). Content the lines carry:
-a: `architecture:` AR-10, AR-11, AR-20, AR-22, AR-29 -- clauses the bodies check land on rows, census rows and raises named;
`judgment: none -- rows state what existing code checks; procedure clauses go to charters; no check added or moved`.
-b: `architecture:` AR-13, AR-15, AR-20, AR-28 -- the card retired, the pages the one told carrier, readers re-pointed in the
same commit; `judgment: none -- data retirement and test re-points; no check added or moved`.

FR walk (both cards): A (FR-2: a command door only on a `shell` row; the three no-Bash roles qa-case-critic, qa-case-designer,
qa-test-strategist get field doors - `agents/*.md:4` re-grepped); B not touched; C (FR-38 kept; FR-11 every clause names a field
its check reads); D (FR-58: expected values come from code constants or this spec, never from new output); E, F not touched;
G (FR-30 English ASCII, FR-54 siblings §7).

---

## §2 Card shape (both cards)

Both cards branch from `main` per §7. Given is narrowed by line range. No file is given whole except
`design/factory-rules.md` and `plans/builder-rules.md` (PROJECT.md, package change item 1), and this spec.

---

## §3 Placement (designer-placed; the builder simulates no rule)

### §3.0 Rules

- **R-1 family first.** An existing row for the check always beats a new function id.
- **R-2 A = append what the body checks.** A clause is appended to a row only when the body behind the row checks it. The
  landed text is the §3.4 text, character for character; the builder never rewords. Clauses of one row are appended in
  card order after the existing sentence, joined by one space.
- **R-3 M2 = sentence-less row.** The §3.4 text becomes `requirement`; the §3.5 door becomes `door`; the role's producer
  entry's `told` becomes `[{"page": true}]`; `demands` and `demands_from` stay.
- **R-4 NEW row**, exactly: `{"check": "<id>", "stages": [<stages>], "requirement": "<text>", "door": "<door>", "when":
  [<when>], "producers": [{"roles": [<roles>], "field": "<field>", "told": [{"page": true}], "demands": []}], "joint": null}`,
  plus `"door_needs": "shell"` and `"role_rule": "<id>"` only where §4.1 gives them. Values: §4.1.
- **R-4a ROLE+ (R2-F4 (a)).** The card's role is added as a NEW producer entry on the row (`roles`, `field` copied,
  `told: [{"page": true}]`, `demands: []`); the clause is appended by R-2.
- **R-5 K = charter line.** The §3.4 K text is appended as the last line of the named section (`## Techniques` under its
  `<!-- kind: craft -->` for craft, `## Tools` for process). SKIPPED when the K entry's `fact` already stands in that charter
  (case-insensitive Grep; positive control: the same search for `## Tools`); the report names the skip.
- **R-6 one door per row.** A door clause is CUT or REPLACES the row's door as §3.1 says. A producer road
  (`manifest_put.py`, `report_facts.py --write`, `estimate_record.py`) inside a requirement is not a door. A door text carries
  no final stop (`told_line` adds `.`, `stage_joints.py:607`).
- **R-7 T / R.** T = the named row already tells the clause on the same role's page (dropped). R = a `requirement_from`
  row whose premise holds (dropped).
- **R-8 role_rule.** A row the table marks with an anchor gets `"role_rule": "<id>"` when it has none; a row that already
  carries another `role_rule` keeps it and the report names the pair (the anchor is checked on the page by `role_rules.py`
  either way).

### §3.1 The placement table (every clause of the 12 cards)

`how`: A (append), M2, NEW (§4.1), ROLE+, K, T, R, door, drop. Texts: §3.4 by seg. Bodies: file:line.

| role | seg | placement | how | body |
|---|---|---|---|---|
| qa-scout | sc-1 | `validate_artifacts:check_phase_json.context-manifest.json` | R/T drop | `PHASE_JSON_KEYS` `validate_artifacts.py:103-104` |
| | sc-2 | `validate_artifacts:check_context_manifest_v0` | A | `:2351-2417`; markers `` `coverage_search[]` rows: `` and `` `existing_test_candidates[]` rows: `` stand verbatim (`test_validator_class.py:199-204`) |
| | sc-3 | NEW `source_preflight:check_source_inventory` | NEW | `source_preflight.py:7-34`; file absent and not required -> allowed, no error (`:12-15`) -> conditioned text (F5) |
| | sc-4 | door of sc-3's row | door | the body's own door `source_preflight.py:44-48` |
| | sc-5 | K `agents/qa-scout.md` `## Tools` | K | procedure |
| qa-requirements-tester | rt-0 | "Three artifacts, three checks." | drop (framing) | - |
| | rt-1a | `validate_artifacts:check_register` | A | `:572-583` |
| | rt-1b | NEW `exit_gate:witness_errors.requirements-tester` | NEW | `check_witness.py:53-57` |
| | rt-1c | `validate_artifacts:check_register` | A | `:601-631` |
| | rt-2 | `exit_gate:grounding` | M2 | `exit_gate.py:1592-1663`; CUT ", so read every hunk, limits, rejected inputs and guards included;" -> rt-2k |
| | rt-2k | K `qa-requirements-tester.md` `## Techniques` | K | advice |
| | rt-3 | `validate_artifacts:check_behaviour_claims`; role_rule `tester-card-derived-row-also-gets-a-behaviour-claims-row` (:347) | A | `:709-717` |
| | rt-4 | NEW `exit_gate:witness_errors.requirements-tester` | NEW | `check_witness.py:121-143`; owner list `planning_contract.py:3134-3142` -> `vocabulary.yaml:151`; the verdict word is a proposed list (`check_witness.py:124-127`), "ready\|blocked" is the routed pair |
| | rt-5 | `validate_artifacts:check_understanding` | A | `:1934-1956`; order not checked -> CUT " in order" |
| qa-test-strategist (no Bash) | ts-0 | K `qa-test-strategist.md` `## Tools` | K | procedure |
| | ts-1a | `planning_contract:plan` | A | `planning_contract.py:176-196`: low depth and severe->critical only under `factory-starter-v1` (`references/risk-policy.md:5`); unknown-not-low `:193-194`, lists `:195-196` |
| | ts-1k | K `## Techniques` | K | not checked |
| | ts-2a | `coverage_contract:obligations.observation` | T drop | row `stage-joints.json` (id Grep) |
| | ts-2b | K `## Techniques` | K | `observation_contract.py:134-139`: MUTATING not checked |
| | ts-3a | K `## Techniques` (text per F13) | K | `planning_contract.py:1480-1482` defines the two flags |
| | ts-3b | `planning_contract:branches`; role_rule `letter-branch-settles-oracle` (:64) | A | `variant_errors` `planning_contract.py:1885-1892`; `oracle_unknown: false` verbatim (`test_oracle_provenance.py:335`) |
| | ts-3c | `coverage_contract:obligations`; role_rule `designer-card-observation-sufficiency-review` (:482) | A | `coverage_contract.py:329-333, 366-370, 376-381` |
| | ts-3d | `coverage_contract:obligations.observation` | T drop | the row's "every obligation carries an `observation_contract`" |
| qa-case-designer (no Bash) | cd-1 | `exit_gate:case_identity`; role_rule `case-id-in-briefs-form` (:161; :162 same carrier, anchor on the page) | M2 | `exit_gate.py:1692-1756` (id == stem :1727, a recorded form :1729) |
| | cd-2 | `validate_artifacts:check_case`; role_rule `designer-card-reuse-decision-vocabulary` (:483) | A | `:161-198, 214-215`; CUT the parenthesis -> cd-2k; CUT "closed " |
| | cd-2k | K `qa-case-designer.md` `## Techniques` | K | not checked |
| | cd-3 | K `## Techniques` | K | no plan row read by `check_case_form` |
| | cd-4a | K `## Techniques` | K (SKIPPED: its fact "One case per plan row" is the role-rules anchor already in `agents/qa-case-designer.md:23`, F14) | not checked as such |
| | cd-4b | NEW `gate_preflight:question_branches`; role_rule `designer-one-case-per-plan-row` (:163) | NEW | `variant_errors(at_cases_stage=True)` `planning_contract.py:1927-1941, 2054-2125`, called by `gate_preflight.py:2113-2170` |
| | cd-4c | `validate_artifacts:check_then_oracles` | A | `contract.then_oracle_errors` `contract.py:1721-1723, 1731-1734` via `validate_artifacts.py:328-333` |
| | cd-4d | K `## Techniques` | K | `raise_question_errors` not opened: K is the safe side |
| | cd-4e | `validate_artifacts:check_then_oracles`; role_rule `designer-now-before-keys` (:164) | A | `contract.py:1637-1646` |
| qa-case-critic (no Bash) | cc-1 | `critic_rollcall:*`; role_rule `merge-keep-only-for-p16-p19` (:181; :484 same carrier, anchor on the page) | M2 | `critic_rollcall.py:43, 589-637, 917-922, 962-1014, 1047-1067, 1085-1088` |
| qa-automator | au-1 | `s5_precheck:bindings` | A | `s5_precheck.py:1279-1300, 1367`; CUT "s5_precheck.py will check, so write to it: " |
| | au-2a | `s5_precheck:oracle` | A | `s5_precheck.py:129`; pinned `test_ahead_cards.py:306` |
| | au-2b | `manifest_put:expectation_changes` | A | `manifest_put.py:1273-1291` |
| | au-2c | `s5_precheck:oracle` | A | `s5_precheck.py:1798, 1823-1826` |
| | au-3 | `s5_precheck:environment` | A | `s5_precheck.py:3580-3601, 3694-3706, 3765-3771` |
| | au-4 | K `qa-automator.md` `## Techniques` | K | advice `s5_precheck.py:22-25` |
| | au-5 | `s5_precheck:manifest` | A | `s5_precheck.py:1046-1068` |
| | au-6 | `s5_precheck:oracle` | A | `s5_precheck.py:1885-1915` |
| qa-code-critic | ck-1 | K `qa-code-critic.md` `## Tools` | K | procedure |
| | ck-2 | K `## Tools` | K | no check of `cause:` |
| | ck-3a | K `## Tools` | K | a brief fact |
| | ck-3b | `manifest_put:expectation_changes` + ROLE+ qa-code-critic (has Bash; the row is `door_needs: shell`) | ROLE+, A | `manifest_put.py:1259-1268`, `:1292-1296`, `:1297-1308`: `critic_note` owed only with `could_not_judge` (F5) |
| | ck-4a | K `## Techniques` | K | not a manifest_put check |
| | ck-4b | `manifest_put:expectation_changes` | T drop (after ROLE+) | the row's "a note stands for each NOTE_REQUIRED_VERDICTS verdict" (`manifest_put.py:1088, 1304-1308`) |
| qa-runner | ru-1 | NEW `exit_gate:witness_errors.runner` | NEW | `check_witness.py:70-86, 237` |
| | ru-2 | `validate_artifacts:check_run_report_head` | A | `:1634-1644` |
| | ru-3a | NEW `exit_gate:witness_errors.runner` | NEW (2nd clause) | `check_witness.py:238-239` |
| | ru-3b | `validate_artifacts:check_run_report_v0` | A | `:2420-2430` |
| | ru-4a | `validate_artifacts:check_result_rows` | A | `:2434-2473` |
| | ru-4b | NEW `exit_gate:witness_errors.runner` | NEW (3rd clause) | `check_witness.py:240-242` |
| | ru-4c | `role_cli:manual_evidence.py build` | R drop | `role-commands.json:33-38` names `--then-quote` |
| | ru-5 | `validate_artifacts:check_run_report_empty`; its door REPLACED (§3.4 `ru-5` door) | A + door | `:1609-1631` (door words :1628-1630); CUT " - return blocked with a reason instead." |
| | ru-6 | `validate_artifacts:check_run_report_coverage` | A | `:2081-2153` |
| qa-failure-analyst | fa-1a | `validate_artifacts:check_triage_v0` | A | list `:2503-2504`; NO_DEFECT `contract.py:5021-5051` via `:2507`; CUT the parenthesis -> bridge + fa-1ak |
| | fa-1ak | K `qa-failure-analyst.md` `## Techniques` | K | the origin of NOT_EXECUTED not checked |
| | fa-1b | NEW `exit_gate:witness_errors.failure-analyst` | NEW | `check_witness.py:244-251` |
| | fa-1c | NEW `artifact_producer:validate` | NEW | `artifact_producer.py:14, 74, 103-107`; pinned `test_validator_class.py:209` |
| | fa-1d | `validate_artifacts:check_triage_v0` | A | `:2514` -> `contract.py:2237-2300` |
| | fa-1e | `validate_artifacts:check_triage_v0` | A | `:2516` -> `contract.py:2303-2410`; 300 = `manual_evidence.py:40` |
| | fa-1f | `validate_artifacts:check_triage_v0` | A | `:2517-2530`; `fix_result` presence only `:2527`; ">= 3" stays (`test_ahead_cards.py:276-277`) |
| | fa-1g | K `## Techniques` | K | refusal text only |
| qa-doc-scribe | ds-1 | `validate_artifacts:check_report_blocks` | A | `:1497-1521`; `G.REPORT_BLOCKS` (17) `grammar.py:168-196`: the card's list is a subset -> "and the others it names" |
| | ds-1k | K `qa-doc-scribe.md` `## Tools` | K (fact already at `agents/qa-doc-scribe.md:63` -> SKIPPED) | procedure |
| | ds-2 | `validate_artifacts:check_report_ledger_and_readiness`; role_rule `scribe-card-delivery-ready-line-is-the-blocks` (:306) | A | `:2001-2025` |
| | ds-3 | `validate_artifacts:check_report_sections` | A | `:1219-1246`; `grammar.py:114-118` |
| | ds-4a | K `## Techniques` | K | not checked |
| | ds-4b | K `## Techniques` | K | `left_items` not read |
| | ds-4c | `validate_artifacts:check_report_left_with_you` | A | `:1291-1299` |
| | ds-4d | "its last two blocks are code's." | drop (stale: three code-owned blocks, `:1309`) | report line |
| | ds-5 | `validate_artifacts:check_report_traceability` | A | `:1255-1275` |
| | ds-6a | K `## Tools` | K (fact already at `agents/qa-doc-scribe.md:63` -> SKIPPED) | the check runs at the S9 exit (`stage_done.py:282-314, 328-344`) |
| | ds-6b | `validate_artifacts:check_report_ledger_and_readiness` | A | `:1986-1991`; pinned `test_ahead_cards.py:278-279` |
| | ds-7 | `check_coverage:*` | M2 | row `stage-joints.json:540-561` |
| qa-bug-reporter | br-1a | K `qa-bug-reporter.md` `## Tools` | K | location |
| | br-1b | `validate_artifacts:check_bug` | A | `:416-418` |
| | br-1c | `validate_artifacts:check_bug_form` | A | `:467-480` |
| | br-2a | `validate_artifacts:check_bug_form` | A | `:464-466, 481-483` |
| | br-2b | "with `severity` DERIVED ..." | drop | false against `:458-461`; the charter carries the suggestion (`qa-bug-reporter.md:26, 47`) |
| | br-2c | `validate_artifacts:check_bug_form` | A | `:487-498` |
| | br-2k | K `## Techniques` | K | not checked |
| | br-2d | `validate_artifacts:check_bug_form` | A | `:501-504` |
| | br-3 | `guard_pre_tool:PT-external-writes` | T drop | row `stage-joints.json:1865-1900` |
| | br-3k | K `## Tools` | K | not in the row |
| | br-4a | `validate_artifacts:check_bug_filing_header` | A | `:433-442`; CUT " and `requirements`" |
| | br-4b | `handoff_check:required_rows` | T drop | row ("one row per item in scope", qa-bug-reporter among its roles); empty list refused (`null-outcomes.json:132`) |
| | br-4bk | K `## Tools` | K | the form's empty-outcome door (`s8-bug-reporter-to-scribe.yaml:13-16, 47-51`) |
| qa-retro-analyst | ra-1 | K `qa-retro-analyst.md` `## Techniques` | K | - |
| | ra-2 | K `## Techniques` | K | craft |
| | ra-3 | NEW `estimate_record:facts_problems` | NEW | `estimate_record.py:69-82, 86-88`; pins `test_ahead_cards.py:86`, `test_validator_class.py:210` |
| | ra-3k | K `## Techniques` | K | `append_record` `:99-112` writes no `delta`/`hit`/`ts` |
| | ra-4 | K `## Tools` | K (fact `add-finding` already present -> SKIPPED) | - |

Accounting (r3, counted from this table): A 42 (ck-3b with ROLE+; ru-3a, ru-4b now counted as NEW-row clauses, see below);
M2 4 (rt-2, cd-1, cc-1, ds-7); NEW-row clauses 9 on 7 NEW function/witness rows (sc-3, rt-1b+rt-4, ru-1+ru-3a+ru-4b, fa-1b,
fa-1c, cd-4b, ra-3); T/R 7 (sc-1, ts-2a, ts-3d, ck-4b, ru-4c, br-3, br-4b); K 29 (four of them SKIPPED by their fact: cd-4a,
ds-1k, ds-6a, ra-4); drop 3 (rt-0, br-2b, ds-4d). The 11 anchors (T15: `role-rules.json:64, 161, 162, 163, 164, 181, 306, 347,
482, 483, 484`) all land on rows. cd-4a is skipped: its fact is the role-rules anchor already in the charter (F14); no K line
the builder writes contains a role-rules anchor (E-5).

### §3.2 Over-claims resolved on the body (carried; F5 additions)

br-2 "severity DERIVED" -> dropped; cd-3 "inherited from your plan row" -> K; rt-5 "in order" -> CUT; rt-1 parent-feature
clause -> witness sub-id; ds-4 `left_items` -> K; ts-1 (starter policy only), ts-2b (MUTATING), ts-3a (flag meaning, F13), cd-4
(one case per row; never raise), ck-2 (`cause:`), fa-1a (NO_DEFECT also surprises; NOT_EXECUTED origin), fa-1f (`fix_result`
presence), ds-1 (block list incomplete), ds-6a (no S8 check), ra-3 (unknown keys; `delta`/`hit`); r3: sc-3 (file absent and
not required, F5), ck-3b (`critic_note` owed only with `could_not_judge`, F5), `fingerprint.build` (byte claim, §4.1).

### §3.3 `validate_artifacts:check_case_form` (row :4015) - sentence REPLACED

"A case dated on or after the form cutoff carries `task`, `covers`, `defect_class` and `basis`; `covers` names only `R-n` ids
the task's register holds (or `legacy:<import reason>`); `basis` follows the oracle grammar."
Body: `CASE_FORM_REQUIRED` `validate_artifacts.py:59`, `:380-385`; covers `:386-401`; basis `:402-407`. Invariant: the row
claims nothing the body does not check. (The refusal text at `:384` still says "inherited from the plan row": queued to
TBW-T1rc-ec8, F15.)

### §3.3b `planning_contract:contradictions` (row :5790) - sentence REPLACED (R3-F1 (a))

"Every requirement the register's matrix records as contradicted is covered by a plan row, and at least one of those rows
carries `source_conflict: true` or `oracle_unknown: true`." Body `planning_contract.py:1485-1504`. The door stays.

### §3.3c `manifest_put:expectation_changes` (row :3883) - words REPLACED (R3-F1 (a))

Only the words `critic_verdict is a list` become `critic_verdict is one word of `expectation_change_verdicts`` (body
`manifest_put.py:156, 1292-1296`; the key `handoffs/vocabulary.yaml:288`). The rest of the sentence stays; au-2b and then
ck-3b are appended after it (R-2, card order of their roles: qa-automator's card first). Invariant: the row and ck-3b's
"ONE verdict" never contradict on one page (E-8).

### §3.4 Landed texts in full (the keys of the S-K check; F3)

One entry per landed text. `kind`: `row` (the text stands inside the row's `requirement`, and on a page line of `role` that
begins `- [<row>]`), `door` (the row's `door` equals the text), `k` (a charter line: `text` is what the builder appends;
`fact` is the key - present case-insensitively in `file`, whether appended or already there). JSON string escapes are the
only transformation (`\"` is a double quote). Texts are ASCII. This block is read by the S-K script between its markers;
nothing else in this file is a key.

<!-- keys:begin -->
```json
[
{"seg": "sc-2", "kind": "row", "role": "qa-scout", "row": "validate_artifacts:check_context_manifest_v0", "text": "Every `related[]` row is {key, kind, source}, kind one of implementation|blocker|bug|mention, `source` saying WHERE in this ticket the key was read; one `implementations[]` row per repository. `coverage_search[]` rows: repo, revision, changed_area, searched_paths, status complete|partial|unavailable, reason; nothing found is top-level `coverage_status: not_found`. `existing_test_candidates[]` rows: candidate_id, repo, revision, path, selector, parameter_ids, level, assertion_refs, candidate_requirement_refs, origin existing|added_in_change|unknown, result_candidate_refs."},
{"seg": "sc-3", "kind": "row", "role": "qa-scout", "row": "source_preflight:check_source_inventory", "text": "When work/source-inventory.json exists, or the pipeline requires it, S1 closes on it: it lists at least one required source, none is `pending`, and no source material lacks its retrieval or inspection receipt."},
{"seg": "sc-4", "kind": "door", "role": "qa-scout", "row": "source_preflight:check_source_inventory", "text": "A source you could not get: name it in your digest with its id and what is missing - recording a person's words is the orchestrator's door; you are resumed with their answer"},
{"seg": "sc-5", "kind": "k", "role": "qa-scout", "file": "agents/qa-scout.md", "section": "## Tools", "fact": "context_bundle.py --manifest", "text": "Build with `context_bundle.py --manifest`, then `--validate`."},
{"seg": "rt-1a", "kind": "row", "role": "qa-requirements-tester", "row": "validate_artifacts:check_register", "text": "work/requirements-register.md: `ids` non-empty and all R-n, `by_source` within ac|story|feature|discussion|assumption|derived, `confidence` high|low."},
{"seg": "rt-1b", "kind": "row", "role": "qa-requirements-tester", "row": "exit_gate:witness_errors.requirements-tester", "text": "In work/requirements-readiness.json a register of AC alone while a parent feature exists must be `confidence: low`."},
{"seg": "rt-1c", "kind": "row", "role": "qa-requirements-tester", "row": "validate_artifacts:check_register", "text": "Every row's observable prefixed diff:|current-code:|expected-contract: or the word `none`; every `derived` row naming what it was derived from; `impact` from config.json impact_scale."},
{"seg": "rt-2", "kind": "row", "role": "qa-requirements-tester", "row": "exit_gate:grounding", "text": "Every production module work/impl-diff*.txt CREATES has to be cited by a `derived` row - the exit gate compares them."},
{"seg": "rt-2", "kind": "door", "role": "qa-requirements-tester", "row": "exit_gate:grounding", "text": "add a `derived` row to work/requirements-register.md for each module the refusal names, with its `derived_from` and an observable `diff:<file>:<line>`"},
{"seg": "rt-2k", "kind": "k", "role": "qa-requirements-tester", "file": "agents/qa-requirements-tester.md", "section": "## Techniques", "fact": "rejected inputs", "text": "Read every hunk of the diff, limits, rejected inputs and guards included."},
{"seg": "rt-3", "kind": "row", "role": "qa-requirements-tester", "row": "validate_artifacts:check_behaviour_claims", "text": "A `derived` row only the diff speaks to also gets its `## Behaviour claims` row."},
{"seg": "rt-4", "kind": "row", "role": "qa-requirements-tester", "row": "exit_gate:witness_errors.requirements-tester", "text": "work/requirements-readiness.json: `verdict` ready|blocked agreeing with the facts, `goal_summary` >= 30 characters in your own words, `aspects` non-empty with status ready|blocked|n/a and a reason on every n/a, `open_questions[]` each with question, severity blocker|major|minor and owner_role po_ba|dev_arch|qa."},
{"seg": "rt-4", "kind": "door", "role": "qa-requirements-tester", "row": "exit_gate:witness_errors.requirements-tester", "text": "edit the field the refusal names in work/requirements-readiness.json"},
{"seg": "rt-5", "kind": "row", "role": "qa-requirements-tester", "row": "validate_artifacts:check_understanding", "text": "understanding.md: at most 40 lines, its five sections, and every register R named in a 'What we verify' or 'What we do not verify' line."},
{"seg": "ts-0", "kind": "k", "role": "qa-test-strategist", "file": "agents/qa-test-strategist.md", "section": "## Tools", "fact": "in fields, not in prose", "text": "planning_contract.py and observation_contract.py will check, so write to them in fields, not in prose."},
{"seg": "ts-1a", "kind": "row", "role": "qa-test-strategist", "row": "planning_contract:plan", "text": "Under the starter risk policy (`risk_policy_revision: factory-starter-v1`), `verification_depth: low` is accepted ONLY together with `impact: low`, `likelihood: low`, `confidence: high` and `bounded_reversible: true`, and `impact: severe` demands `critical`. `impact: unknown` can never be low. Every row needs `risk_source_refs` and `required_scenarios` non-empty."},
{"seg": "ts-1k", "kind": "k", "role": "qa-test-strategist", "file": "agents/qa-test-strategist.md", "section": "## Techniques", "fact": "repeating the detector's sentence", "text": "Repeating the detector's sentence in a note is not evidence."},
{"seg": "ts-2b", "kind": "k", "role": "qa-test-strategist", "file": "agents/qa-test-strategist.md", "section": "## Techniques", "fact": "MUTATING check", "text": "A no-write obligation's `positive_control_ref` names a MUTATING check, not one of the four sequence refs."},
{"seg": "ts-3a", "kind": "k", "role": "qa-test-strategist", "file": "agents/qa-test-strategist.md", "section": "## Techniques", "fact": "oracle you cannot settle", "text": "An oracle you cannot settle is `oracle_unknown: true`; add `source_conflict: true` when the sources disagree."},
{"seg": "ts-3b", "kind": "row", "role": "qa-test-strategist", "row": "planning_contract:branches", "text": "A letter branch whose answer settles the oracle sets `oracle_unknown: false`: a row that is `oracle_unknown` and rests on one open question says so in every reading's branch."},
{"seg": "ts-3c", "kind": "row", "role": "qa-test-strategist", "row": "coverage_contract:obligations", "text": "A coverage-schema-2 row lists its `coverage_obligations`, each with `sufficiency_review {author_dispatch_id, input_hash, rationale}` all non-empty, and `oracle_status` resolved (naming an independent `oracle_source_ref`) or unresolved; an unresolved oracle does not authorize execution: its `decision` is `unresolved`."},
{"seg": "cd-1", "kind": "row", "role": "qa-case-designer", "row": "exit_gate:case_identity", "text": "A case file's `id` IS its file name, both in the form named on this brief's `Case id form:` line: `<case id>.md` declares `id: <case id>`. That is the factory's contract over any project note (a note naming another form is not read by code), and the exit gate refuses the handoff otherwise."},
{"seg": "cd-1", "kind": "door", "role": "qa-case-designer", "row": "exit_gate:case_identity", "text": "write each case again under the name the refusal shows for it, with `id:` equal to that name"},
{"seg": "cd-2", "kind": "row", "role": "qa-case-designer", "row": "validate_artifacts:check_case", "text": "Frontmatter every case owes: id, title, area, priority P0|P1|P2|P3, status, channel auto|manual-agent|manual-human, reuse_decision new|updated|extend:<case id>|dedupe:<case id>, updated, task, covers: [R-n] that exist in that task's register (an R the register does not carry reads as invented), defect_class from the project's list (or smoke, or regression:BUG-NNN), and basis."},
{"seg": "cd-2k", "kind": "k", "role": "qa-case-designer", "file": "agents/qa-case-designer.md", "section": "## Techniques", "fact": "only the code critic moves", "text": "Your statuses are Draft, Review and Approved; only the code critic moves a case to Automated, and only after a probe."},
{"seg": "cd-3", "kind": "k", "role": "qa-case-designer", "file": "agents/qa-case-designer.md", "section": "## Techniques", "fact": "never reassigned", "text": "defect_class and basis are inherited from your plan row, never reassigned."},
{"seg": "cd-4a", "kind": "k", "role": "qa-case-designer", "file": "agents/qa-case-designer.md", "section": "## Techniques", "fact": "One case per plan row", "text": "One case per plan row."},
{"seg": "cd-4b", "kind": "row", "role": "qa-case-designer", "row": "gate_preflight:question_branches", "text": "A case is owed for an `unverifiable` row too (and a `skip` one) when an answer to the question it rests on would make the row tested: write it before gate A with `question_thens` on that question. Every `question_thens` is one line of JSON, a list of {question, then, readings}: `then` the number of an item under `## Then`, and a text for every reading of the question."},
{"seg": "cd-4b", "kind": "door", "role": "qa-case-designer", "row": "gate_preflight:question_branches", "text": "write the case or the `question_thens` entry the line names"},
{"seg": "cd-4c", "kind": "row", "role": "qa-case-designer", "row": "validate_artifacts:check_then_oracles", "text": "A Then that waits on a question (`then_oracles` source `unknown`) goes in `question_thens` under that question's id as requirements-readiness.json has it."},
{"seg": "cd-4d", "kind": "k", "role": "qa-case-designer", "file": "agents/qa-case-designer.md", "section": "## Techniques", "fact": "once it is raised", "text": "Never `raise` a question once it is raised."},
{"seg": "cd-4e", "kind": "row", "role": "qa-case-designer", "row": "validate_artifacts:check_then_oracles", "text": "The question being raised (`raise`) is always a before/now question, and a case keys its texts `now` / `before`, never by letter."},
{"seg": "cc-1", "kind": "row", "role": "qa-case-critic", "row": "critic_rollcall:*", "text": "critic_rollcall.py computes your verdict from your own findings file at the exit gate. A `## Roll-call` table with one row per case in scope, and give it a column headed `reviewed` holding yes or no. A `Verdict:` line from approve|approve_with_fixes|approve_with_concerns|partial|reject. If any row is not reviewed, an approving verdict is refused: the verdict that roll-call computes is `partial`, your digest must say '<n> of <m> reviewed', and an `Unreviewed for Gate A:` line must name every unreviewed case. A concern of the last round that comes with an exact replacement is applied by code: put those in a fenced JSON array under `## Fixes without a new round`, each object carrying case_id, locator, find, replace and reviewed_version. `approve_with_fixes` without that block is refused, and so is that block beside any other verdict. Cases sharing an R-n: a row per pair under `## Merge candidates` (cases | verdict merge|keep | reason; keep starts P16 or P19); merge: each case `approve_with_concerns`, note `parametrise into one test: <ids>`. e2e-ui/manual row notes: `lower level: <level|impossible> - <why>`. Over the plan case budget: an `Over the plan case budget:` line."},
{"seg": "cc-1", "kind": "door", "role": "qa-case-critic", "row": "critic_rollcall:*", "text": "edit your findings file where the refusal names it"},
{"seg": "au-1", "kind": "row", "role": "qa-automator", "row": "s5_precheck:bindings", "text": "Every Then is bound in `then_bindings[]` {case, then, instance_id, assertion_ref \"file:line\"}, and the names it demands appear in that assertion."},
{"seg": "au-2a", "kind": "row", "role": "qa-automator", "row": "s5_precheck:oracle", "text": "A status code or literal a Then fixes is asserted as written and NEVER changed after a red run: that test is handed over RED, `unresolved[] reason: contradicts_requirement`."},
{"seg": "au-2b", "kind": "row", "role": "qa-automator", "row": "manifest_put:expectation_changes", "text": "A value you invented may change after a red run only with an `expectation_changes[]` row through manifest_put.py: `then_refs` [{case, then}] it still proves, `what_changed`, `reason`."},
{"seg": "au-2c", "kind": "row", "role": "qa-automator", "row": "s5_precheck:oracle", "text": "A test that went red and was then deleted or renamed owes an `expectation_changes[]` row too."},
{"seg": "au-3", "kind": "row", "role": "qa-automator", "row": "s5_precheck:environment", "text": "A `blocked_by_env` row has `remedy` {kind, where, change, restart}, names only; it stands only on a run showing the stand (`env_blocked`, a STAND SIGNAL on a run no timeout killed, a connection refusal); a test the project's timeout killed is yours."},
{"seg": "au-4", "kind": "k", "role": "qa-automator", "file": "agents/qa-automator.md", "section": "## Techniques", "fact": "None == None", "text": "Smells to avoid: env credentials in an assert, `None == None`, `sleep`, a copied helper."},
{"seg": "au-5", "kind": "row", "role": "qa-automator", "row": "s5_precheck:manifest", "text": "One `tests[]` entry per INSTANCE (`func[param]`); `covers` lists cases."},
{"seg": "au-6", "kind": "row", "role": "qa-automator", "row": "s5_precheck:oracle", "text": "A `deferred_by_decision:*` row carries `disputes` nothing|derivation|case_expectation; `derivation` = not derivable; `case_expectation` = you disagree with the approved case; no route out after gate A."},
{"seg": "3.3c", "kind": "row", "role": "qa-automator", "row": "manifest_put:expectation_changes", "text": "critic_verdict is one word of `expectation_change_verdicts`"},
{"seg": "ck-1", "kind": "k", "role": "qa-code-critic", "file": "agents/qa-code-critic.md", "section": "## Tools", "fact": "duplicate green", "text": "Static review first, the whole window; then probe_by_code.py and, on doubt, red_sandbox.py --probe (the calls, the model file work/probe-models/<your dispatch id>.json and the reasons are on the card); reuse the author's green receipt, never run a duplicate green. A `mechanical` finding is worded, not fixed."},
{"seg": "ck-2", "kind": "k", "role": "qa-code-critic", "file": "agents/qa-code-critic.md", "section": "## Tools", "fact": "with `cause:` on each", "text": "Findings go to work/test-code/critic-findings-<your dispatch id>.md with `cause:` on each."},
{"seg": "ck-3a", "kind": "k", "role": "qa-code-critic", "file": "agents/qa-code-critic.md", "section": "## Tools", "fact": "s5_precheck.py --json", "text": "A test that changed after its red run is listed in your brief (`s5_precheck.py --json`: `expectation_changes`)."},
{"seg": "ck-3b", "kind": "row", "role": "qa-code-critic", "row": "manifest_put:expectation_changes", "text": "Give each row ONE verdict through manifest_put.py, a patch with its function, `red_attempt` and `green_attempt` plus `critic_verdict` legitimate_correction|fitted_to_code|could_not_judge and `critic_note` (owed with `could_not_judge`)."},
{"seg": "ck-4a", "kind": "k", "role": "qa-code-critic", "file": "agents/qa-code-critic.md", "section": "## Techniques", "fact": "the Then's value restored", "text": "`fitted_to_code` is also a `test_defect` finding whose expected is \"the Then's value restored, the test handed RED with contradicts_requirement\"."},
{"seg": "ru-1", "kind": "row", "role": "qa-runner", "row": "exit_gate:witness_errors.runner", "text": "`witness` in work/run-report.json is at least 30 characters, and a run_suite summary it names (evidence/<label>-<ts>.json) EXISTS on disk - a retelling is not a witness."},
{"seg": "ru-1", "kind": "door", "role": "qa-runner", "row": "exit_gate:witness_errors.runner", "text": "edit the field the refusal names in work/run-report.json"},
{"seg": "ru-2", "kind": "row", "role": "qa-runner", "row": "validate_artifacts:check_run_report_head", "text": "`head` non-empty: evidence not bound to a sha goes stale."},
{"seg": "ru-3a", "kind": "row", "role": "qa-runner", "row": "exit_gate:witness_errors.runner", "text": "`env_preflight` is pass or blocked, and `totals` is an object."},
{"seg": "ru-3b", "kind": "row", "role": "qa-runner", "row": "validate_artifacts:check_run_report_v0", "text": "A blocked `env_preflight` means `execution_status` is env_blocked - one field, one source. `execution_status` from passed|failed|env_blocked|not_executed|broken_run|timeout."},
{"seg": "ru-4a", "kind": "row", "role": "qa-runner", "row": "validate_artifacts:check_result_rows", "text": "Every `results[]` row names ONE case, even when one test covers several, with a status from passed|failed|error|skipped|not_run, and a skip carries its reason."},
{"seg": "ru-4b", "kind": "row", "role": "qa-runner", "row": "exit_gate:witness_errors.runner", "text": "`manual_checks[].result` is pass|fail|inconclusive."},
{"seg": "ru-5", "kind": "row", "role": "qa-runner", "row": "validate_artifacts:check_run_report_empty", "text": "Empty is not clean: a zero run with env_preflight pass and no env_blocked, manual_checks or manual_skipped is refused."},
{"seg": "ru-5", "kind": "door", "role": "qa-runner", "row": "validate_artifacts:check_run_report_empty", "text": "return `env_preflight: blocked` with a reason, or say where the cases went"},
{"seg": "ru-6", "kind": "row", "role": "qa-runner", "row": "validate_artifacts:check_run_report_coverage", "text": "And every case S5 automated, plus every manual-agent row of the plan, has to appear in some lane of this report: results, manual_checks, skipped, impossible, env_blocked, manual_skipped or manual_human. Where a case went is your call; saying nothing about it is not."},
{"seg": "fa-1a", "kind": "row", "role": "qa-failure-analyst", "row": "validate_artifacts:check_triage_v0", "text": "work/triage.json is read row by row: every row's `verdict` comes from APP_BUG|TEST_BUG|TEST_BUG:collection|ENV_ISSUE|FLAKY|APP_CHANGED|CASE_DEFECT|ASSERT_STRICTER|NOT_EXECUTED|RUNNER_MISREAD_EVIDENCE|NO_DEFECT. NO_DEFECT is for an observation `<case>#obs<n>` or a recorder's surprise `<case>#sur-<id>` only, with a `reason` quoting its recorded evidence in double quotes."},
{"seg": "fa-1ak", "kind": "k", "role": "qa-failure-analyst", "file": "agents/qa-failure-analyst.md", "section": "## Techniques", "fact": "NOT_EXECUTED is code's", "text": "NOT_EXECUTED is code's word, for a manual check that did not answer."},
{"seg": "fa-1b", "kind": "row", "role": "qa-failure-analyst", "row": "exit_gate:witness_errors.failure-analyst", "text": "Every triage row's `evidence` is non-empty whatever the verdict."},
{"seg": "fa-1b", "kind": "door", "role": "qa-failure-analyst", "row": "exit_gate:witness_errors.failure-analyst", "text": "edit the row the refusal names in work/triage.json"},
{"seg": "fa-1c", "kind": "row", "role": "qa-failure-analyst", "row": "artifact_producer:validate", "text": "Every row also names its `instance_id` and `attempt_id`."},
{"seg": "fa-1c", "kind": "door", "role": "qa-failure-analyst", "row": "artifact_producer:validate", "text": "add the two ids to the row the refusal names in work/triage.json"},
{"seg": "fa-1d", "kind": "row", "role": "qa-failure-analyst", "row": "validate_artifacts:check_triage_v0", "text": "ASSERT_STRICTER costs a `control` block: `result` effect_without_change, `action`, `without`, `observed`, an existing `evidence` file under `evidence/`; `impossible` needs `why`, no ASSERT_STRICTER."},
{"seg": "fa-1e", "kind": "row", "role": "qa-failure-analyst", "row": "validate_artifacts:check_triage_v0", "text": "RUNNER_MISREAD_EVIDENCE costs a `contradiction` block: `then`, `runner_said`, `evidence` (a text capture of the attempt) and a `quote` from it (300 characters at most)."},
{"seg": "fa-1f", "kind": "row", "role": "qa-failure-analyst", "row": "validate_artifacts:check_triage_v0", "text": "FLAKY costs three more fields, and all three are checked: `reruns` >= 3 isolated executions of that test, counted across every role; `mechanism` from isolation|race|timing|shared_state|teardown|environment|unknown; and `fix_result` non-empty (record fixed or not_fixed)."},
{"seg": "fa-1g", "kind": "k", "role": "qa-failure-analyst", "file": "agents/qa-failure-analyst.md", "section": "## Techniques", "fact": "person's call at gate B", "text": "An unfixed flake is not verified, and quarantining it is the person's call at gate B, never yours."},
{"seg": "ds-1", "kind": "row", "role": "qa-doc-scribe", "row": "validate_artifacts:check_report_blocks", "text": "`report_facts.py --task <T> --write` renders every code-owned block the report owes (the verdict, Proven, Product bugs, Open questions, Skipped by the plan, Not proven, Decided at gate A, Size, Where to look, and the others it names; Decided at gate B after the gate)."},
{"seg": "ds-1k", "kind": "k", "role": "qa-doc-scribe", "file": "agents/qa-doc-scribe.md", "section": "## Tools", "fact": "never type a number", "text": "Begin test-report.md from the template; never type a number a code-owned block carries."},
{"seg": "ds-2", "kind": "row", "role": "qa-doc-scribe", "row": "validate_artifacts:check_report_ledger_and_readiness", "text": "The `delivery_ready:` line is the block's (check_delivery.py feeds it): yes, after_checks or no."},
{"seg": "ds-3", "kind": "row", "role": "qa-doc-scribe", "row": "validate_artifacts:check_report_sections", "text": "Eleven sections in this order: Proven, Product bugs, Left with you, Open questions, Not proven, Decided at gate A, Decided at gate B, Factory defects, Size, Where to look, Appendix - the verdict above the first. `Decided at gate B` is owed only after the gate."},
{"seg": "ds-4a", "kind": "k", "role": "qa-doc-scribe", "file": "agents/qa-doc-scribe.md", "section": "## Techniques", "fact": "could not verify is in Left with you", "text": "A green test the critic could not verify is in Left with you, not under Proven."},
{"seg": "ds-4b", "kind": "k", "role": "qa-doc-scribe", "file": "agents/qa-doc-scribe.md", "section": "## Techniques", "fact": "left_items", "text": "`Left with you` has one item per case in `ledger.json` `left_items`."},
{"seg": "ds-4c", "kind": "row", "role": "qa-doc-scribe", "row": "validate_artifacts:check_report_left_with_you", "text": "Each `Left with you` item carries its R-n, case id, `To check:` and `Needed:` or `How:`."},
{"seg": "ds-5", "kind": "row", "role": "qa-doc-scribe", "row": "validate_artifacts:check_report_traceability", "text": "The Appendix is `traceability.py --render` pasted, a row for every R and every case."},
{"seg": "ds-6a", "kind": "k", "role": "qa-doc-scribe", "file": "agents/qa-doc-scribe.md", "section": "## Tools", "fact": "`--check` must exit 0", "text": "`report_facts.py --task <T> --check` must exit 0 before you finish."},
{"seg": "ds-6b", "kind": "row", "role": "qa-doc-scribe", "row": "validate_artifacts:check_report_ledger_and_readiness", "text": "Your prose outside the blocks stays under 6,144 bytes."},
{"seg": "ds-7", "kind": "row", "role": "qa-doc-scribe", "row": "check_coverage:*", "text": "check_coverage.py re-runs at the exit gate: regenerate the coverage map first."},
{"seg": "ds-7", "kind": "door", "role": "qa-doc-scribe", "row": "check_coverage:*", "text": "regenerate the coverage map with `check_coverage.py`, then fix what it names"},
{"seg": "br-1a", "kind": "k", "role": "qa-bug-reporter", "file": "agents/qa-bug-reporter.md", "section": "## Tools", "fact": "IS the bug", "text": "bugs/BUG-n.md in the task root IS the bug, whatever the channel."},
{"seg": "br-1b", "kind": "row", "role": "qa-bug-reporter", "row": "validate_artifacts:check_bug", "text": "Frontmatter is checked: id, title, severity, status, area, found_by, created."},
{"seg": "br-1c", "kind": "row", "role": "qa-bug-reporter", "row": "validate_artifacts:check_bug_form", "text": "`violates` follows the oracle grammar (requirement:R-n | invariant:<id> | consistency:<where> | history:<baseline> | impact:<harm> | external:<norm>) - with no oracle from that list this is an observation, not a bug."},
{"seg": "br-2a", "kind": "row", "role": "qa-bug-reporter", "row": "validate_artifacts:check_bug_form", "text": "`impact` from config.json impact_scale."},
{"seg": "br-2c", "kind": "row", "role": "qa-bug-reporter", "row": "validate_artifacts:check_bug_form", "text": "`confirmation` unconfirmed|reproduced_by_factory|confirmed_by_person|confirmed_by_rerun."},
{"seg": "br-2k", "kind": "k", "role": "qa-bug-reporter", "file": "agents/qa-bug-reporter.md", "section": "## Techniques", "fact": "the code derives reproduced_by_factory", "text": "`confirmed_by_person` comes from the person's words, else the draft's value; the code derives reproduced_by_factory, so an unreproduced bug is shown apart."},
{"seg": "br-2d", "kind": "row", "role": "qa-bug-reporter", "row": "validate_artifacts:check_bug_form", "text": "Two sections are mandatory: `## User impact` and `## Initial state`."},
{"seg": "br-3k", "kind": "k", "role": "qa-bug-reporter", "file": "agents/qa-bug-reporter.md", "section": "## Tools", "fact": "performs a proposal after the gate", "text": "external_writes.py performs a proposal after the gate."},
{"seg": "br-4a", "kind": "row", "role": "qa-bug-reporter", "row": "validate_artifacts:check_bug_filing_header", "text": "A bug from a draft also names `cases` (or `cases: []` with `no_case_reason`)."},
{"seg": "br-4bk", "kind": "k", "role": "qa-bug-reporter", "file": "agents/qa-bug-reporter.md", "section": "## Tools", "fact": "nothing_chosen", "text": "With no draft chosen, your handoff form's `scope` holds the one `gate_b` row (state `nothing_chosen`)."},
{"seg": "ra-1", "kind": "k", "role": "qa-retro-analyst", "file": "agents/qa-retro-analyst.md", "section": "## Techniques", "fact": "do not re-price", "text": "Every number in retro.md comes from work/retro-numbers.md and .json, already computed by retro_numbers.py: do not re-add and do not re-price."},
{"seg": "ra-2", "kind": "k", "role": "qa-retro-analyst", "file": "agents/qa-retro-analyst.md", "section": "## Techniques", "fact": "1,911", "text": "The story's spend is the sessions the driver's own journal names - a roll-up over every session that merely mentions the ticket once published $1,911 against the $128 actually charged. Two records of the same money exist on purpose: the journal is what the CLI charged and is authoritative, the cost files are token-priced and mark themselves `provisional`; where they disagree, print the gap and say which is which. An unknown is written as `unknown`, never rounded into a fact."},
{"seg": "ra-3", "kind": "row", "role": "qa-retro-analyst", "row": "estimate_record:facts_problems", "text": "The precedent line is written by `estimate_record.py --task <T> --facts <file>`: the file holds `forecast` and `actual` objects and an optional `drivers` array, and every key of the wrong shape is listed in one refusal."},
{"seg": "ra-3", "kind": "door", "role": "qa-retro-analyst", "row": "estimate_record:facts_problems", "text": "fix every key the refusal lists in the facts file and run the same command again"},
{"seg": "ra-3k", "kind": "k", "role": "qa-retro-analyst", "file": "agents/qa-retro-analyst.md", "section": "## Techniques", "fact": "derives the precedent row", "text": "Code derives the precedent row from the facts file; you never write the row yourself."},
{"seg": "ra-4", "kind": "k", "role": "qa-retro-analyst", "file": "agents/qa-retro-analyst.md", "section": "## Tools", "fact": "add-finding", "text": "What outlives this story goes to the project's ledgers through `project_decisions.py --root <project> add-finding`, not into retro prose."},
{"seg": "3.3", "kind": "row", "role": "qa-case-designer", "row": "validate_artifacts:check_case_form", "text": "A case dated on or after the form cutoff carries `task`, `covers`, `defect_class` and `basis`; `covers` names only `R-n` ids the task's register holds (or `legacy:<import reason>`); `basis` follows the oracle grammar."},
{"seg": "3.3b", "kind": "row", "role": "qa-test-strategist", "row": "planning_contract:contradictions", "text": "Every requirement the register's matrix records as contradicted is covered by a plan row, and at least one of those rows carries `source_conflict: true` or `oracle_unknown: true`."},
{"seg": "4-prov", "kind": "row", "role": "qa-automator", "row": "s5_precheck:sides.provisional", "text": "Every live `provisional[]` row of this window has a `kind` from `references/provisional-kinds.json`, a `settles_on` that is a side of this story, a `home.file` whose placeholder line carries the comment `qa-provisional: <id>`, and `dependents` as a list of `{case, then}` that are bound in `then_bindings`; every `qa-provisional: <id>` marker in a test file of the window has its `provisional[]` row."},
{"seg": "4-prov", "kind": "door", "role": "qa-automator", "row": "s5_precheck:sides.provisional", "text": "send the row or the field through `manifest_put.py --fragment`, or take the marker out of the test file"},
{"seg": "4-pend", "kind": "row", "role": "qa-automator", "row": "s5_precheck:sides.pending", "text": "On a story with sides, a `pending_implementation` row of a case in scope stands only while a side its test declares is `absent`: an instance that can run owes its run, and a row whose every instance has run stamped real on every side its test names is retracted."},
{"seg": "4-pend", "kind": "door", "role": "qa-automator", "row": "s5_precheck:sides.pending", "text": "run it (`run_suite.py --mine <case>`) and retract the row through `manifest_put.py --fragment`, or declare the absent side in the test's `sides` when one really is"},
{"seg": "4-none", "kind": "row", "role": "qa-runner", "row": "execution_request:profile.none", "text": "When no manifest row names a profile and the earlier runs of this story do not all name one, `qa-factory/config.json` holds at least one execution profile (a `profiles[]` entry with a `profile_id`); with none, `--mine` cannot build the run."},
{"seg": "4-none", "kind": "door", "role": "qa-runner", "row": "execution_request:profile.none", "text": "report it in your digest: the gate-A rehearsal asks the person about the onboarding gap"},
{"seg": "4-fp", "kind": "row", "role": "qa-runner", "row": "execution_request:fingerprint.build", "text": "The inputs of a `--mine` run can be fingerprinted when it is built: every test, helper, config and dependency file it reads exists, and the stand's runtime provenance is `matched`, confirmed by the person, `not_applicable`, or a probe that compared nothing."},
{"seg": "4-fp", "kind": "door", "role": "qa-runner", "row": "execution_request:fingerprint.build", "text": "report it in your digest, and write this one run with `run_suite.py --template request`"},
{"seg": "4-ren", "kind": "row", "role": "qa-scout", "row": "handoff_check:cli.values_rename", "text": "The waiting values file `<dispatch>.values.yaml` can be renamed `<dispatch>.values.applied.yaml` once the form is written."},
{"seg": "4-ren", "kind": "door", "role": "qa-scout", "row": "handoff_check:cli.values_rename", "text": "delete the values file the refusal names, then run the check again"}
]
```
<!-- keys:end -->

### §3.5 Doors of the four M2 rows (own sweep; `stage_joints.py:1001-1002`)

A row that comes to state a requirement must name a door (K3: "states a requirement and names no `door`: say where the
receiver fixes it"). r2 turned four sentence-less rows into requirement rows with no door: every one would be red in
`stage_joints.py --check`. Doors (their §3.4 `door` keys), each from the body's own way-on words:

| row | door | body | door_needs / when |
|---|---|---|---|
| `exit_gate:grounding` (qa-requirements-tester, Bash) | §3.4 `rt-2` door | `exit_gate.py:1657-1663` ("add the requirements that code carries ... source `derived` with its `derived_from` ..., observable `diff:<file>:<line>`") | none (a field door) |
| `exit_gate:case_identity` (qa-case-designer, no Bash) | §3.4 `cd-1` door | `exit_gate.py:1753-1754` ("write each case again under the name shown for it ... with `id:` equal to that name") | none (a field door) |
| `critic_rollcall:*` (qa-case-critic, no Bash) | §3.4 `cc-1` door | the refusals of `critic_rollcall.py` name the findings-file part (`:589-637`) | none (a field door) |
| `check_coverage:*` (qa-doc-scribe, Bash) | §3.4 `ds-7` door | the card's "regenerate the coverage map first" | `"door_needs": "shell"`, `"when": ["shell"]` (a command door, FR-2) |

---

## §4 Rows the node adds beyond the cards, census rows, the unsited count

### §4.1 The NEW rows (12), whole (R-4; texts and doors are §3.4)

| id | stages | roles (one producer entry, told `[{"page": true}]`) | field | when | door_needs | role_rule | body (re-read t-1056) |
|---|---|---|---|---|---|---|---|
| `source_preflight:check_source_inventory` | S1 | qa-scout | work/source-inventory.json | always | - | - | `source_preflight.py:7-34`, door `:44-48` |
| `exit_gate:witness_errors.requirements-tester` | S2 | qa-requirements-tester | work/requirements-readiness.json | always | - | - | `check_witness.py:53-57, 121-143`; requirement = rt-1b text, one space, rt-4 text |
| `exit_gate:witness_errors.runner` | S6 | qa-runner | work/run-report.json | always | - | - | `check_witness.py:70-86, 236-243`; requirement = ru-1, ru-3a, ru-4b texts joined by one space |
| `exit_gate:witness_errors.failure-analyst` | S7 | qa-failure-analyst | work/triage.json | always | - | - | `check_witness.py:244-251` |
| `artifact_producer:validate` | S7 | qa-failure-analyst | work/triage.json | always | - | - | `artifact_producer.py:14, 74, 103-107` |
| `gate_preflight:question_branches` | S4 | qa-case-designer | the `question_thens` of the cases | always | - | `designer-one-case-per-plan-row` | `planning_contract.py:1927-1941, 2054-2125`; `gate_preflight.py:2113-2170` |
| `estimate_record:facts_problems` | S9 | qa-retro-analyst | the facts file of estimate_record.py | shell | shell | - | `estimate_record.py:69-88` |
| `s5_precheck:sides.provisional` | S5 | qa-automator | the provisional rows and the tests that name them | window, shell | shell | - | `s5_precheck.py:2104-2168` (kind `:2118-2125`, side `:2126-2129`, home marker `:2130-2140`, dependents `:2141-2152`, marker -> row `:2153-2168`; a `retracted` row skipped `:2116`) |
| `s5_precheck:sides.pending` | S5 | qa-automator | the `pending_implementation` rows and the tests they name | window, shell | shell | - | `s5_precheck.py:2171-2198` (only on a sided story with rows in scope `:2176-2178`; owes its run `:2186-2191`; leftover row `:2192-2198`) |
| `execution_request:profile.none` | S5, S6, S7 | qa-runner, qa-automator, qa-code-critic, qa-failure-analyst (the roles of `execution_request:profile`, `stage-joints.json:6301-6328`) | the `--mine` call and its manifest rows | shell | - (the door names no command) | - | `execution_request.py:1795`, `:1817-1830` (`selected_profiles` `profile_contract.py:544-549`; the precedent rule `:1819-1821`) |
| `execution_request:fingerprint.build` (finish F-5 (a)) | S5, S6, S7 | same four | the `--mine` call and its manifest rows | shell | shell | - | `execution_request.py:3761-3771`; `execution_fingerprint.py:104-151` (provenance `:113-126`; a missing file `:79-81`) |
| `handoff_check:cli.values_rename` (R2-F7 (a)) | `*` | the 9 Bash roles: qa-automator, qa-bug-reporter, qa-code-critic, qa-doc-scribe, qa-failure-analyst, qa-requirements-tester, qa-retro-analyst, qa-runner, qa-scout (F7, fork R4-F3) | the handover form of the dispatch | shell | shell | - | `handoff_check.py:3199-3209` (refusal under `handoff_check:cli`, door "delete <values file>") |

Notes on the bodies (re-read t-1056, so -a needs no r1):
- `fingerprint.build`: r1/r2 said "exists and keeps its bytes while it is hashed". On the `--mine` road the inputs reach
  `build` as path strings (`execution_request.py:3751-3754, 3763-3769`), and the byte claim is compared only for a
  `{path, sha256}` record (`execution_fingerprint.py:85-92`); so "keeps its bytes" is CUT (AR-29, E-13). The door stays
  (F-P2-6 (a), accepted for r1): the refusal itself names no door (`execution_request.py:3771`; `run_suite.py:2096` prints
  `mine_refused` with the error only), so the page door contradicts nothing.
- `profile.none`: the refusal says "this is a gap of the onboarding, not of your test - the gate-A rehearsal asks the person
  (answer a/b/c); to onboard now: `/qa-factory:qa-onboarding`" (`execution_request.py:1827-1830`), and the comment above it
  names typing request files by hand as the harm (`:1824-1826`). The page door is the refusal's own (fork R4-F4); the
  slash command is the person's road, not the role's, so the page names the digest. The requirement states the three
  conditions the body has before this refusal (no row-named profile `:1766-1794`; precedent `:1819-1821`; no selected
  profile `:1823`).
- `values_rename`: the door needs a shell (delete a file) -> `door_needs: shell`; the three no-Bash roles are not told
  (E-10); their door is queued to TBW-T1rc-site (§7).

### §4.2 Sited parents

Witness sub-ids, `profile.none`, `fingerprint.build`, `values_rename` are sub-ids of sited ids (`_is_sited`,
`stage_joints.py:340-342`). Measured by critic t-1046 (`sited.py`, main and wave B): sited.

### §4.3 The dry census rows (F1; SIBLING_MAP axis 38, `docs/SIBLING_MAP.md:644-655`)

Every row id of `stage-joints.json` is a census subject (`dry_exits.scan_joints`, `dry_exits.py:521-532`); a subject with
no row is red ("the driver has it and no row names it", `:683-684`). -a writes, in the SAME commit as the 12 rows, one row
per new joint under `"joints"` of its group file, and one `raised_by` entry per row in that file's `ratchet`, the
base `unwalked` number UNCHANGED (the count rises by the named entries, `_ratchets` `:740-759`):

| group file (`PKG/scripts/tests/fixtures/driver-exits/`) | joints (by `stages`, axis 38: all stages in one group -> it; two groups or `*` -> `gates`) |
|---|---|
| `s1-s4.json` | `source_preflight:check_source_inventory` (S1), `exit_gate:witness_errors.requirements-tester` (S2), `gate_preflight:question_branches` (S4) |
| `s5.json` | `s5_precheck:sides.provisional`, `s5_precheck:sides.pending` |
| `s6-s9.json` | `exit_gate:witness_errors.runner` (S6), `exit_gate:witness_errors.failure-analyst` (S7), `artifact_producer:validate` (S7), `estimate_record:facts_problems` (S9) |
| `gates.json` | `execution_request:profile.none`, `execution_request:fingerprint.build` (S5-S7), `handoff_check:cli.values_rename` (`*`) |

Row form (as the L1c rows in `s1-s4.json:39-42`): `"<id>": {"reach": "unwalked", "why_unreached": "not walked yet: joint added
by T1r-cards-a (told-before-work, cards to rows); the group's walk node writes its rows"}`. `raised_by` entry form (the
`RAISE_RE`, `dry_exits.py:54`): `"unwalked | joints/<id> | T1r-cards-a, 2026-11-17"`. No `classes.json` edit: a joint's
class source is `stage-joints` (`class_of`, `:587`). Invariant (AR-28, axis 38): no joint without a row, no row claiming a
walk (`story`/`seed`) without a walk row (`:712-714`), no rise without a named entry.

### §4.4 The unsited count (F2)

Command that prints it: `python -B ai-packages/qa-factory/scripts/stage_joints.py --check` (summary line `told counters:
hand_cards N, legacy_legs N, unsited N`, `stage_joints.py:1207-1208`). Numbers: stored 46 on main (`stage-joints.json:8129`,
read t-1056); measured 46 on main and 17 on wave B by critic t-1046's run (I had no shell). New unsited rows after -a, by the
siting rule (`sited_ids` + sub-id rule, `stage_joints.py:321-342`) and the critic's measurement: 6 -
`source_preflight:check_source_inventory`, `estimate_record:facts_problems`, `artifact_producer:validate`,
`gate_preflight:question_branches` (no literal id in code: critic's negative greps with control `exit_gate:grounding` at
`exit_gate.py:1894`), `s5_precheck:sides.provisional`, `s5_precheck:sides.pending` (their findings are bare strings:
`check_sides.add` -> `_sited("sides", case, message, ...)`, `s5_precheck.py:2417-2418`; a bare str adds nothing, `:298`; and
`s5_precheck:sides` itself is no sited id, so the sub-id rule does not reach them). So: main 46 -> 52; after wave B 17 -> 23.

Siting node per new unsited row (each by TBW-T1rc-site, §7): the four function rows (its R2-F3 owns) and the two `sides.*`
rows (`s5_precheck.py` `_sides_provisional`, `_sides_pending`: the bare `add(...)` messages become
`DV.refusal("s5_precheck:sides.provisional"|...)`, as `_sides_settled` does at `:2209`).

---

## §5 Edges (each with its invariant)

- **E-1 no clause unaccounted.** Every clause of §3.1 has a row, a K line, a T/R or a named drop. Invariant: no card clause
  leaves the package with neither; the card stays the carrier until -b.
- **E-2 TEMPORAL, between -a and -b.** After -a a page carries the landed rows AND the card under `### Not yet in rows`
  (told twice; `contract_slices.py:687-690` renders the card group while `hand_cards` > 0); after -b once. -a creates the
  rows, -b removes the card group. Invariant: a role is never told less at any moment.
- **E-3 TEMPORAL, a story started before.** A brief already written keeps its ahead section; one written after -b has none.
  Invariant: one plugin generation per run (B-014).
- **E-4 POSITIONAL, append order.** Landed clauses go AFTER the row's existing sentence, in card order; §3.3, §3.3b replace
  their sentence, §3.3c only its words. Invariant: no other T1r sentence is reworded; one door per told line (R-6). The -a
  report records each appended row's PRE-APPEND sentence verbatim (F15), so TBW-T1rc-ec8 can replace it without touching
  the appended clauses.
- **E-5 charter anchors.** No K line the builder writes contains a role-rules anchor (cd-4a is skipped, F14); the builder
  runs `role_rules.py --check` after the K lines. Invariant: role_rules stays at 0 findings; a collision is a STOP naming
  the line.
- **E-6 empty / absent.** `ahead-cards.json` absent or unreadable after -b: red "cannot be counted" (`stage_joints.py:1254-1256`),
  never 0; `cards: {}` reads 0. No landed text is empty (§3.4 has none).
- **E-7 quarantined readers.** After -b the five quarantined files (test_case_id_form_texts, test_context_bundle,
  test_report_texts, test_ahead_cards_rules, test_brief_pack_roles) may go red in `quarantine-check`; not edited; -b's report
  names each; the Lead tells the owner on `TEST QUARANTINE ALERT`. Invariant: no quarantined file is edited.
- **E-8 conflicting requirements.** "Append verbatim" against "only what the body checks": AR-29 wins through cuts and
  bridges (R2-F2 (a)). ck-3b "ONE verdict" against "is a list": the row is corrected (§3.3c). A page door against its
  refusal (`profile.none`): the refusal's door (R4-F4). Invariant: no page says two contradicting things about one field.
- **E-9 caps** (the owner's word 17.11.2026 on Q-O1, carrier: finish spec "Слово владельца 17.11.2026 по Q-O1": "не в ущерб
  правилам. Если не влезет можно поднять"). Rule text is NEVER cut to fit. A page at or over W is SPLIT (continuation lines
  `-2`, `-3`, ... until no page reaches W). A role over `ratchet_tokens` or `process_ratchet_tokens` gets the row RAISED to
  the measured value, named: one report row and one commit line `raise: <role> <key> <old> -> <new> (+<n> B) -- <why>`. A
  K10 rise (a new or higher `native_headroom.<role>`) is named `raise: <role> native_headroom <old> -> <new> (U-H = <n> B)`,
  U and H read from the K10 red line `role_load.py:339-345` ("the plugin share is U bytes, over its native-context headroom
  H"). Past the Codex ceiling - a role whose plugin share U alone is over 100,000 B, so that `native_context.stage` refuses to
  launch it on every project (`native_context.py:174-175`, a runtime refusal, not a ratchet): STOP before commit, and the
  report names the role and U; the Lead takes it to the owner (R2-F6', recommendation (b)). Invariant: no sentence
  truncated; no raise unnamed (AR-20); no commit makes a role unlaunchable on Codex without the owner's word. (Size today:
  the largest share is qa-automator 79,909 B, `role-load.json:38-42`; the told-twice window adds about one card, cards are
  939-1,197 characters - critic t-1046's measure.)
- **E-10 a row whose role lacks a shell.** A `door_needs: shell` row (ra-3, ck-3b's row, the two `sides.*` rows,
  `fingerprint.build`, `values_rename`, `check_coverage:*`) is told only to roles with Bash (`agents/*.md:4`). The rows told
  to no-Bash roles (cd-1, cd-4b, cc-1) carry field doors. Known residual (F7): the code door of `handoff_check:cli`'s rename
  refusal ("delete <file>", `handoff_check.py:3209`) can reach a no-Bash role through the parent row; queued to
  TBW-T1rc-site. Invariant: a no-shell role never sees a shell door on a page.
- **E-11 error direction of the reused reader** `contract_slices.handoff_keys_pages` (P-4) as the reader of the test pins and
  of the S-K check. It may err toward "absent" (red); never toward "present" on text the role does not receive.
  Adversarial inputs that stay red: a clause only on a page `inject-map.json` does not list for the role; a clause only on
  another role's page; a clause only inside the card group under `### Not yet in rows` (S-K matches only a line beginning
  `- [<row id>]`; -b checks after hand_cards 0); a row whose role entry is not told by the page (no line at all).
- **E-12 the integration tree.** Settled by critic t-1046 (F10): wave B changes no row of stage-joints.json (one hunk:
  `unsited` 46 -> 17). -a keeps every producer list it does not name; ROLE+ only adds. Invariant: -a never re-widens a
  producer list it did not name.
- **E-13 a clause the body at today's line no longer checks** (F4): the row text is not landed as written; the builder
  STOPs on that row and the report names it (seg, row, file:line read); the Lead decides the cut. Invariant: AR-29 - a row
  never claims a check its body does not run.
- **E-14 a new joint and the dry census** (F1): a joint added without its census row, or a census row whose joint is gone,
  is red in `dry_exits.py --check`; -a's DoD expects `0 discrepancies` and one `unwalked` note naming the 12 raises.
  Invariant: axis 38 - the census and the joints change in one commit.
- **E-15 a requirement row with no door** (§3.5): every row -a makes state a requirement names a door. Invariant:
  `stage_joints.py:1001-1002` stays silent on -a's rows.

---

## §6 The cards (R2-F1 (b): cut by TIME)

### Card T1r-cards-a - clauses land on rows (wave C)

Order: after Lead acceptance of r3 (F1-F5, F7, F8 applied here) and after K1b (FV2-79, `plans/piles/live-run-fvf/batch-2-live-run-fvf.md:106`,
status "ожидает": its whole chain designer -> builder -> critic has not started; -a waits on it). Branches from main; it
does NOT depend on wave B (no shared row, F10) - only the integrator's `unsited` base differs (§7). Executable on the
recommendations of R4-F3, R4-F4, R2-F6'.

given:
- `C:\QAFactory\forge-repo\docs\tasks\specs\20261117-told-before-work-t1r-cards-spec-r3.md` (this file: §1, §3, §4, §5, §6 -a)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\design\factory-rules.md` whole; `C:\QAFactory\forge-repo\plans\builder-rules.md`; `C:\QAFactory\forge-repo\docs\TESTING.md`
- `PKG/references/ahead-cards.json:1-95` (read only); `PKG/design/role-rules.json:64, 161-165, 181, 306, 347, 482-484` (read only)
- `PKG/references/stage-joints.json`: the rows named in §3.1, §3.3-§3.5, §4.1 (Grep `"check": "<id>"`) and `told_ratchet` :8126-8130
- `PKG/references/role-load.json` whole; `PKG/references/inject-map.json` (the 12 page lines)
- `PKG/scripts/stage_joints.py:74-95, 321-342, 581-608, 971-1027`; `PKG/scripts/contract_slices.py:583-591, 681-691, 786-830`
- `PKG/scripts/tests/dry_exits.py:39-83, 636-760`; `PKG/scripts/tests/fixtures/driver-exits/s1-s4.json` whole (the row form), the `ratchet` blocks of `s5.json`, `s6-s9.json`, `gates.json`
- the charter sections named in §3.1 (`## Tools` / `## Techniques` only)
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\stage-joints.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\slices\
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\inject-map.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\role-load.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\s1-s4.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\s5.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\s6-s9.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\gates.json
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
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\tbw-t1r-cards-a.md
owns scope (per path): stage-joints.json - the rows of §3.1 (A, M2 with their §3.5 doors, ROLE+), the 12 rows of §4.1, the
sentences §3.3-§3.3c, NOT `told_ratchet`; slices - only through `contract_slices.py --write`; inject-map.json - continuation
page lines only; role-load.json - `ratchet_tokens`, `process_ratchet_tokens`, `native_headroom` values only (E-9);
driver-exits group files - only the 12 `"joints"` rows of §4.3 and their 12 `raised_by` entries, no base, no other row;
each charter - only the K lines §3.4 names in its `## Tools` / `## Techniques` (qa-runner.md and qa-case-critic.md get
none); changelog fragment new.
non-goals: `ahead-cards.json`, `role-rules.json` (-b); `told_ratchet` (hand_cards: -b; `unsited` and the K12 pin:
TBW-T1rc-int); every test file (no committed test in -a, R3-F3'); any script code (sites: TBW-T1rc-site); `classes.json`,
`known_red*`, walk rows `fixtures/stories/dry-1/exits/`; the five quarantined tests; slow files run locally; CI; a new test file.
handoff: the branch commit plus `C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-tbw-t1r-cards-a-report.md`: a line per
§3.4 key (landed / K skipped by its fact / STOP by E-13); each appended row's pre-append sentence verbatim (E-4); the T rows
and drops; the unsited before -> after with the 6 ids (for TBW-T1rc-int); the 12 census rows and the `dry_exits` note;
K8 page sizes; K10 U/H per role before/after; the raise records (E-9); the FR walk; the S-K script run with its negative
control; the verbatim witness.
edges: §5 E-1, E-2, E-4, E-5, E-8, E-9, E-10, E-11, E-12, E-13, E-14, E-15.
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for references/stage-joints.json references/inject-map.json references/role-load.json scripts/tests/fixtures/driver-exits/s1-s4.json scripts/tests/fixtures/driver-exits/s5.json scripts/tests/fixtures/driver-exits/s6-s9.json scripts/tests/fixtures/driver-exits/gates.json agents/qa-scout.md agents/qa-requirements-tester.md agents/qa-test-strategist.md agents/qa-case-designer.md agents/qa-automator.md agents/qa-code-critic.md agents/qa-failure-analyst.md agents/qa-doc-scribe.md agents/qa-bug-reporter.md agents/qa-retro-analyst.md` - run each printed file that is not in `slow_tests.json` and not quarantined, each alone; list the slow ones as "judged by the batch canon". Then, each verbatim in the report:
- test: `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check` -> `dry_exits --check: 0 discrepancies` and a note `ratchet unwalked: raised 12 row(s) above the base ...` naming the 12 | expected from: §4.3 (axis 38)
- test: `python -B ai-packages/qa-factory/scripts/contract_slices.py --write`, then `python -B ai-packages/qa-factory/scripts/contract_slices.py --check` -> clean, no `WARN K8` | expected from: E-9
- test: `python -B ai-packages/qa-factory/scripts/stage_joints.py --check` -> its ONLY finding is `stage-joints: told_ratchet.unsited is <stored> but <stored+6> rows have no site in code (...)` naming exactly the 6 ids of §4.4 (red until TBW-T1rc-int, F12); any other finding (a missing door, a shape) is a defect of -a | expected from: §4.4
- test: `python -B ai-packages/qa-factory/scripts/role_rules.py --check` -> 0 findings | expected from: E-5
- test: `python -B ai-packages/qa-factory/scripts/tests/test_role_load.py` -> green | expected from: E-9 raises named
- test: `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang` -> green | expected from: FR-30, page byte cap
- supplementary key-presence check (S-K below): `python -B <scratchpad>\t1rc_keys.py <worktree root>` -> `t1rc keys: <n> checked, 0 failed`; then `python -B <scratchpad>\t1rc_keys.py <worktree root> --negative` -> exit 1 naming `NEG` | expected from: §3.4 of this spec
- census: no new blocking unit.
siblings: axis 34 (one road: ROLE+ not sub-ids per role where texts are equal; family rows first); axis 38: a census row per new joint (§4.3); axis 18: raises named (E-9, §4.4); the EC-8 lines of t-979 K5 and the original-sentence sweep: node TBW-T1rc-ec8 (§7), not here; `design/factory-rules-debt.md` "All twelve have a card now" (closing node); `estimate_record.append_record` writes no `delta`/`hit`/`ts` while the card names them (analog, reported).
designer: `C:\QAFactory\forge-repo\docs\tasks\specs\20261117-told-before-work-t1r-cards-spec-r3.md` (once accepted)

Items:

| # | what | expected | proof (expected value from) |
|---|---|---|---|
| A-1 | Measure before: `stage_joints --check`, `contract_slices --check`, `role_rules --check`, `dry_exits --check` | verbatim in the report | report |
| A-2 | Land every A / M2 / ROLE+ clause of §3.1 | each §3.4 `row` text inside its row and on the role's page | S-K (§3.4) |
| A-3 | §3.3, §3.3b, §3.3c | replaced | S-K keys `3.3`, `3.3b`, `3.3c` |
| A-4 | the 12 rows of §4.1, R-4 form; the M2 doors of §3.5 | rows exist, told on the roles' pages; no K3 door finding | S-K `row`/`door` keys; `stage_joints.py --check` |
| A-5 | K lines | appended or skipped by the fact | S-K `k` keys; `role_rules.py --check` 0 |
| A-6 | pages | `--write`; split until no page reaches W; continuation lines in the same commit | `contract_slices.py --check` clean |
| A-7 | caps (E-9) | raised to the measured value, named; a role with U > 100,000 B: STOP | report raise table; A22 / K10 green |
| A-8 | changelog | one English ASCII bullet | `selftest.py --lang` |
| A-9 | census rows (§4.3) | 12 rows, 12 `raised_by` entries, bases unchanged | `dry_exits.py --check` 0 discrepancies |

S-K - the supplementary key-presence check (F3; rule 11 DOC-DISPATCH properties: (i) keys = §3.4 of this file, written
before the run; (ii) the script below, in full, attached with its output in the report, never committed; (iii) a negative
control). It is NOT the builder's witness (the witness is the `--witness-for` run; keep tests judge every owned path).
Save as `t1rc_keys.py` in the builder's scratchpad:

```python
"""Supplementary key-presence check of T1r-cards-a (spec r3 section 3.4). Never committed."""
import json
import re
import sys
from pathlib import Path

SPEC = Path(r"C:\QAFactory\forge-repo\docs\tasks\specs\20261117-told-before-work-t1r-cards-spec-r3.md")
NEGATIVE = {"seg": "NEG", "kind": "row", "role": "qa-runner", "row": "validate_artifacts:check_run_report_head",
            "text": "NEGATIVE CONTROL: this sentence stands on no row and no page."}


def main(argv):
    root = Path(argv[1]).resolve()
    pkg = root / "ai-packages" / "qa-factory"
    sys.path.insert(0, str(pkg / "scripts"))
    import contract_slices
    found = re.search(r"<!-- keys:begin -->\s*```json\n(.*?)\n```\s*<!-- keys:end -->",
                      SPEC.read_text(encoding="utf-8"), re.S)
    if not found:
        print("t1rc keys: the key block of the spec cannot be read")
        return 2
    keys = json.loads(found.group(1)) + ([NEGATIVE] if "--negative" in argv else [])
    rows = {r.get("check"): r for r in json.loads((pkg / "references" / "stage-joints.json").read_text(encoding="utf-8"))["joints"]}
    pages, failed = {}, []
    for key in keys:
        seg, kind, text = key["seg"], key["kind"], key["text"]
        if kind == "k":
            body = (pkg / key["file"]).read_text(encoding="utf-8")
            if key["fact"].lower() not in body.lower():
                failed.append(f"{seg}: fact {key['fact']!r} not in {key['file']}")
            continue
        row = rows.get(key["row"])
        if row is None:
            failed.append(f"{seg}: no row {key['row']}")
            continue
        if kind == "door":
            if row.get("door") != text:
                failed.append(f"{seg}: door of {key['row']} is {row.get('door')!r}")
            continue
        if text not in str(row.get("requirement") or ""):
            failed.append(f"{seg}: text not in the requirement of {key['row']}")
        if key["role"] not in pages:
            pages[key["role"]] = "\n".join(contract_slices.handoff_keys_pages(pkg, key["role"])).splitlines()
        if not any(line.startswith(f"- [{key['row']}]") and text in line for line in pages[key["role"]]):
            failed.append(f"{seg}: no page line of {key['role']} begins - [{key['row']}] and holds the text")
    for line in failed:
        print("FAIL " + line)
    print(f"t1rc keys: {len(keys)} checked, {len(failed)} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

### Card T1r-cards-b - the cards retire, readers re-point (wave C, after -a and TBW-T1rc-int)

Order: after -a is merged into the wave-C integration branch AND TBW-T1rc-int has committed the `unsited` raise and the K12
pin there (F12); after the Lead's answers on R4-F1, R4-F2 (executable on the recommendations). F6, F9, F10, F12 are applied
here. TBW-T1rc-site may run in parallel (no shared path). Wave B: -b starts from the integration commit, so whether wave B
is in main by then decides only the `unsited` number it expects (23 with wave B, 52 without).

given:
- this file §1, §5, §6 -b, §8 (R4-F1, R4-F2)
- `PKG/references/ahead-cards.json` whole; `PKG/design/role-rules.json:64, 161-165, 181, 306, 347, 482-484`
- `PKG/agents/qa-test-strategist.md:70-78`
- `PKG/scripts/contract_slices.py:583-591, 681-691, 786-830`; `PKG/scripts/stage_joints.py:1125-1164`
- `PKG/scripts/tests/test_ahead_cards.py` whole; `test_validator_class.py:40-60, 190-240, 500-545`
- `test_env_evidence.py:160-180`; `test_oracle_provenance.py:325-345`; `test_question_branches.py:1770-1795`; `test_s7_rejudge.py:100-120`
- `test_contract_slices.py:640-665, 820-830`; `test_stage_joints.py`: the block from `UNSITED_CAP` to `told/hand-cards-unreadable` (:923-959 on main)
- `C:\QAFactory\forge-repo\docs\TESTING.md`; `C:\QAFactory\forge-repo\plans\builder-rules.md`; `PKG/design/factory-rules.md`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\ahead-cards.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\stage-joints.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\design\role-rules.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\agents\qa-test-strategist.md
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
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\tbw-t1r-cards-b.md
owns scope (per path): ahead-cards.json - `cards` -> `{}`, `note` rewritten to say the cards retired into rows on the key
pages (`references/stage-joints.json`), the file kept for the count; stage-joints.json - `told_ratchet.hand_cards` 12 -> 0
only; role-rules.json - (1) in the 11 rows (T15) only the carrier entry whose `file` is `references/ahead-cards.json`,
re-pointed to the page file that holds the anchor after -a (`references/slices/<role>/handoff-keys*.md`); (2) the `rule`
text of `designer-one-case-per-plan-row` (:163) restated per R4-F1; (3) row `strategist-letter-branch-follows-card` (:165)
per R4-F2; qa-test-strategist.md - the one line `:74` per R4-F2; slices - only through `--write`; inject-map.json -
continuation lines that became empty may go; role-load.json - values lowered to the measure only; test_ahead_cards.py -
the `cards()` reader, the `main` card blocks and the brief block (NOT `charter_card_join`, `role_text_roots`);
test_validator_class.py - the `told_text` "card" branch only; test_env_evidence `:171`, test_oracle_provenance `:335`,
test_question_branches `:1780`, test_s7_rejudge `:109` - the one read each; test_contract_slices.py - the real-tree card rows
(`:660-662` on main) only; test_stage_joints.py - the `for counter, up, down in` loop of the told variants and the
`told/hand-cards-*` rows next to it, named by content (F10: wave B shifts the loop from :938 to :939).
non-goals: `brief_pack.py` / `contract_slices.py` / `stage_joints.py` code (T3b; closing); the five quarantined files
(E-7); `told_ratchet.unsited` and `UNSITED_CAP` (TBW-T1rc-int); any row sentence; a new test file; a new variant row;
`dry_exits` census (-b adds or removes no joint).
handoff: the commit plus `C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261117-tbw-t1r-cards-b-report.md`: the re-point per
reader (file:line, old -> new carrier); the role-rules re-points (id, new file) and the two restated rules (old -> new);
the deleted rows (file:line, why: behaviour removed); the shrinks (key, old -> new); the quarantined readers' state; the
lint-baseline count of `test_oracle_provenance.py` if it moved (§10); the verbatim witness.
edges: §5 E-2, E-3, E-6, E-7, E-11; plus:
- E-b1: a pin whose clause landed as K reads the charter (`agents/<role>.md`), never the page. Invariant: a pin reads the
  carrier that really holds the words.
- E-b2 (P-2, F9): at stored `hand_cards` 0 the told loop's "plus-one" form (`update({counter: stored - 1})`) would write -1
  (`test_stage_joints.py:950-952`), and hand cards are read from `env.plugin / references/ahead-cards.json`
  (`stage_joints._hand_cards`, `:1156-1164`), which `mutated()` cannot reach. Method for `hand_cards` (the loop's
  `legacy_legs` branch stays as it is): `told/hand-cards-at-baseline`: `audit()` counts 0 and is green; `told/hand-cards-plus-one`:
  `env = copy.copy(ENV)`, `env.plugin` = a temp dir holding `references/ahead-cards.json` = `{"cards": {"qa-scout": {"text": "x"}}}`;
  `text_of(SJ.audit(copy.deepcopy(REAL), UNI, None, env, sited=set(UNI[0])))` contains
  `told_ratchet.hand_cards is 0 but the walk counts 1` (the pattern of `told/hand-cards-unreadable`, `:956-959`);
  `told/hand-cards-negative`: `audit(data=mutated(lambda d: d["told_ratchet"].update(hand_cards=-1)))` contains
  `a count (an integer, 0 or more) is expected`; `told/hand-cards-minus-one` (dense): a stored 1 is red with
  `lower told_ratchet.hand_cards to 0`. Invariant: the loop never asserts a message the audit cannot print, and a counter
  above its stored number stays red.
- E-b3 (R4-F2): after -b no charter line or role-rules rule tells a role to follow "the card". Invariant: no reader points
  at a carrier that no longer exists.
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for references/ahead-cards.json design/role-rules.json agents/qa-test-strategist.md references/stage-joints.json references/role-load.json references/inject-map.json scripts/tests/test_ahead_cards.py scripts/tests/test_validator_class.py scripts/tests/test_env_evidence.py scripts/tests/test_oracle_provenance.py scripts/tests/test_question_branches.py scripts/tests/test_s7_rejudge.py scripts/tests/test_contract_slices.py scripts/tests/test_stage_joints.py` - run every printed file not in `slow_tests.json` and not quarantined, each alone; slow ones (test_s7_rejudge, test_contract_slices, test_stage_joints): "judged by the batch canon". Then, each verbatim in the report:
- test: `python -B ai-packages/qa-factory/scripts/contract_slices.py --write`, then `python -B ai-packages/qa-factory/scripts/contract_slices.py --check` -> clean | expected from: B-6
- test: `python -B ai-packages/qa-factory/scripts/stage_joints.py --check` -> clean, `told counters: hand_cards 0, legacy_legs 0, unsited <the number TBW-T1rc-int stored>` | expected from: B-2, §4.4
- test: `python -B ai-packages/qa-factory/scripts/role_rules.py --check` -> 0 findings | expected from: B-3
- test: `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check` -> 0 discrepancies (unchanged) | expected from: non-goals
- test: `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang` -> green
- test: test_ahead_cards.py::the VOCABULARIES / quoted-numbers / B-194 / expectation-field table, re-pointed to `told_text_of(role)` | expected from: the code constants each row already names (`C.RELATED_KINDS`, `V.TEST_REPORT_MAX_BYTES`, `manifest_put.VERDICTS_LIST`, `estimate_record.FACTS_KEYS`, ...), never the page
- test: test_validator_class.py::the `told_text` rows `:198-210` | expected from: the carrier constants they already name (`artifact_producer.TRIAGE_ROW_IDS`, `estimate_record.FACTS_KEYS`, the scout's field lists)
- test: test_stage_joints.py::told/hand-cards-* (E-b2) | expected from: `told_ratchet.hand_cards` 0 (B-2) and the audit's own sentences (`stage_joints.py:1147-1152`)
- census: no new blocking unit.
siblings: T3b (`brief_pack.ahead_card` dead at 0, removed in T3b); closing (`contract_slices` `ahead_card` / `CARD_GROUP` / `NOT_YET_HEAD`); axis 34; R4-F2 (the strategist "card" line).
designer: same path as -a.

Items (one parameterised row per behaviour; existing tables only):

| # | what | row / proof | expected value from |
|---|---|---|---|
| B-1 | `cards: {}`, the note rewritten | `stage_joints.py --check`; no test row | data |
| B-2 | hand_cards 12 -> 0 | `stage_joints.py --check` summary | the measure |
| B-3 | 11 role-rules re-points; :163 restated (R4-F1); :165 per R4-F2 | `role_rules.py --check` 0 | anchors per T15 and §8 |
| B-4 | `told_text_of(role)` = `"\n".join(contract_slices.handoff_keys_pages(plugin_root, role))`; the existing rows read it instead of `cards()` | existing rows of test_ahead_cards.py | the code constants, never the page |
| B-5 | brief rows (the ahead section present) | DELETED, not inverted (behaviour removed, code goes in T3b; TESTING "Когда тест покраснел" 1) | - |
| B-6 | sizes go down (card group gone) | report shrink table | the measure |
| B-7 | test_validator_class `told_text(("card", r))` -> `told_text_of(r)`; a K-landed pin reads the charter (E-b1) | existing rows | carrier constants |
| B-8 | env_evidence / oracle_provenance / question_branches / s7_rejudge reads -> `told_text_of` of the same role | existing rows | unchanged expectations |
| B-9 | test_contract_slices real-tree card rows | DELETED (synthetic card-group rows stay until the closing removes the code) | - |
| B-10 | test_stage_joints told rows (E-b2) | existing loop rows, hand_cards by the E-b2 method | E-b2 |
| B-11 | changelog bullet | `selftest.py --lang` | - |
| B-12 | qa-test-strategist.md:74 (R4-F2) | `role_rules.py --check` 0 | R4-F2 text |

---

## §7 Order lines and the nodes this spec names (collisions with work in flight)

Nodes (each a producer with owns; the Lead enters them into `plans/piles/told-before-work/batch-1-finish.md`, TBW1-13's family):

| node | owns | what | after |
|---|---|---|---|
| T1r-cards-a | §6 | rows, census rows, K lines | K1b (FV2-79) |
| TBW-T1rc-int (the wave-C integrator commit, F12) | `PKG/references/stage-joints.json` (`told_ratchet.unsited` only), `PKG/scripts/tests/test_stage_joints.py` (`UNSITED_CAP` and its comment only) | raise `unsited` and `UNSITED_CAP` by -a's named 6 (§4.4), with `raise: told_ratchet.unsited <old> -> <new> -- T1r-cards-a rows wait for TBW-T1rc-site` | -a merged into the wave-C integration branch; before main |
| T1r-cards-b | §6 | cards retire | TBW-T1rc-int |
| TBW-T1rc-site (residual siting, R2-F3 (a) / R2-F7 (a)) | `PKG/scripts/source_preflight.py`, `estimate_record.py`, `artifact_producer.py`, `gate_preflight.py`, `handoff_check.py` (the rename site + a no-Bash door "say in your digest that `<values file>` could not be renamed; the orchestrator removes it", F7), `s5_precheck.py` (`_sides_provisional`, `_sides_pending`), `scripts/tests/test_detector_verdict.py` (one row in its table), `scripts/tests/fixtures/told-ratchet.json` (K4 unit rows move `bare` -> `tagged`, e.g. `s5_precheck.py::check_sides` :543) | site the 6 ids; lower `unsited` by 6 | -a; parallel to -b |
| TBW-T1rc-ec8 (queue, F15) | `PKG/references/stage-joints.json` (original sentences only), `PKG/scripts/validate_artifacts.py` (the `check_case_form` refusal text `:384`) | the EC-8 lines of t-979 K5 (`null_outcome.triage`, the PT-big-read split, T6/T7b/T7a-A/T4a lines); a sweep of the original sentences of the ~25 rows -a appends to (from -a's report, E-4); the refusal text "inherited from the plan row" | -a |

Order lines:
- `очередь: K1b (FV2-79, ожидает) -> T1r-cards-a -> TBW-T1rc-int -> T1r-cards-b`. K1b writes `stage-joints.json` told markers,
  slices, `inject-map.json`, `role-load.json`, `test_contract_slices.py`; -a measures caps after K1b.
- Wave B (`worktree-agent-ad0767bec786dddde`, T7a-B/C): no row overlap (F10); either merges first; TBW-T1rc-int applies +6
  to the base it finds. After wave B, `validate_artifacts.py` cites move by up to +9 after :1711 (critic t-1046) - bodies only,
  no row; -a's §3.1 bodies are cited at c9b42659.
- Driver-exits writers (F1, F11 (c)): FV2-15 (`batch-2-live-run-fvf.md:42`), FV3-1, FV3-2, FV3-3, FV3-5, FV3-6, FV3-15, FV3-20
  (`batch-3-live-run-fvf.md:30-33, 35-36, 49`), all "ожидает". Either merges first; the later one merges main and keeps both
  sides' rows and `raised_by` entries; `dry_exits.py --check` 0 after the merge.
- RD1-1 (`plans/piles/rules-debt/batch-1-phase-2.md:29`, "ожидает") owns `references/common-rules.md` and
  `references/slices/*/common-rules.md` (F11 (a)): `очередь: RD1-1 <-> T1r-cards-a/-b` by merge order; the common layer is
  part of the K10/A22 measure, so the later node re-measures E-9 after merging main.
- FV2-81, FV2-82 (`batch-2-live-run-fvf.md:108-109`, "ожидает") own `test_contract_slices.py` (F11 (b)): `очередь: FV2-81,
  FV2-82 <-> T1r-cards-b` by merge order (different functions: `test_k10p_k2`, pin 864 vs the real-tree card rows).
- FV2-90 (`batch-2-live-run-fvf.md:117`, "ожидает") owns `role-load.json` and the automator / strategist pages (found this
  round, not in t-1046): `очередь: FV2-90 <-> T1r-cards-a` by merge order; the later one re-measures E-9.
- T4b, T9a: no shared file. T9c (new conductor rows in `stage-joints.json`, and so census rows): either merges first; the
  later one merges main and keeps both.
- `очередь: T1r-cards-b -> T3b` on `test_ahead_cards.py`; `очередь: T1r-cards-b -> closing (wave D)`.

---

## §8 Forks

Decided earlier (carried unchanged): R2-F1 (b) cut by time; R2-F2 (a) designer bridges checked by the plan critic; R2-F3 (a)
NEW rows + named unsited raise + residual siting node; R2-F4 (a) ROLE+; R2-F5 (a) witness sub-ids per role; R2-F7 (a)
`handoff_check:cli.values_rename` + residual site; R3-F1 (a) the two false sentences corrected in -a; EC-8 lines -> node
TBW-T1rc-ec8. Re-opened because a t-1046 finding contradicts the recorded line, or new:

| # | question | options | recommendation | status |
|---|---|---|---|---|
| R2-F6' (F8; owner) | A role whose plugin share U alone exceeds 100,000 B cannot launch on Codex at all (`native_context.py:174-175` raises; a runtime refusal, not a cap). R2-F6 (a) "go on, name the bytes" read the owner's raise word onto it. Go on? | (a) go on, name U, tell the owner the same turn · (b) STOP before commit; the Lead asks the owner | **(b)**: a product break on one host is a product risk (PROJECT.md "Что решать самому"), and the owner's word speaks of raising caps. K10 rises below 100,000 stay under the owner's raise word (named as `U-H`). Cost: a wait only if it happens; today's largest share is 79,909 B. -a is executable on (b) | open, for the owner |
| R3-F2' (F2) | R3-F2 (a) recorded "`unsited` +4"; the measure is +6 (two `sides.*` rows of §4 also have no site). Keep (a)? | (a) keep, +6, `s5_precheck.py` and `told-ratchet.json` join TBW-T1rc-site · (b) drop the two `sides.*` rows from -a until their sites exist | **(a)**: the rows tell the automator a check that already runs; the count is named and the siting node owns the fix | open (factual correction of a decided line) |
| R3-F3' (F3) | R3-F3 (a) "no committed test; a DOC-DISPATCH witness". The witness is the `--witness-for` run (the owns have keep tests); the key check is supplementary. Keep (a) under that reading? | (a) keep: no committed test; witness = `--witness-for`; S-K = supplementary key-presence check with the three DOC-DISPATCH properties · (b) a committed table in test_ahead_cards.py | **(a)**: TESTING `:135-140` ("receipt per key", "role-text pin" not written) | open (label) |
| R4-F1 (F6) | After -b, role-rules `designer-one-case-per-plan-row` (:163) says "one case per plan row, an unverifiable row too", while its page carrier (cd-4b) owes a case for a `skip`/`unverifiable` row only when an answer would make it tested (`planning_contract.py:1927-1941`). Restate the registered rule (source t-1685, not the owner)? | (a) -b restates `rule` to: "The designer writes one case per plan row; a `skip` or `unverifiable` row owes one only when an answer to the question it rests on would make it tested." (anchors unchanged) · (b) leave the rule text | **(a)**: a registry rule must not deny its carrier. Cost: one line | open, for the Lead |
| R4-F2 (new sibling, E-b3) | `agents/qa-test-strategist.md:74` says the letter-branch fields "are on your key page, in the plan contract and on your card; the letter-branch fields follow the card's rule", and role-rules `strategist-letter-branch-follows-card` (:165, rule "follow the rule on its card", anchor "follow the card's rule") holds it. After -b there is no card | (a) -b restates line :74 to "... are on your key page and in the plan contract; the letter-branch fields follow the `planning_contract:branches` row on your key page." and :165 to rule "The strategist's letter-branch fields follow the `planning_contract:branches` row on its key page." with anchor "follow the `planning_contract:branches` row" · (b) leave it to the closing node | **(a)**: the dangling reference is created by -b itself (rule 2: a spec silent on an edge its own requirements create). Cost: one charter line, one registry row, -b owns the charter | open, for the Lead |
| R4-F3 (F7) | `values_rename`'s door ("delete the values file") needs a shell; the parent row tells all 12 roles | (a) narrow the row's producers to the 9 Bash roles (`door_needs: shell`, `when: ["shell"]`) and queue a no-Bash door to TBW-T1rc-site · (b) keep 12 roles and a field door only | **(a)**: FR-2 / E-10; the code door is the code's own, so the row stays truthful | open, for the Lead |
| R4-F4 (F4) | `profile.none`'s page door: r1 had "write this one run with `run_suite.py --template request`"; the refusal says the gate-A rehearsal asks the person (`execution_request.py:1827-1830`) | (a) the refusal's own: "report it in your digest: the gate-A rehearsal asks the person about the onboarding gap" · (b) the template road (then the refusal text changes too, in TBW-T1rc-site) | **(a)**: page and refusal agree (E-8, R-6); the comment `:1824-1826` names the template road as the harm | open, for the Lead |

---

## §9 Premises

| P | what | result |
|---|---|---|
| P-1 | wave B rows | settled by critic t-1046 (F10): one hunk, `unsited` 46 -> 17; branch head moved since (`f88a5e38`), not re-read here |
| P-2 | test_stage_joints at stored 0 | `:950-952` sets -1 -> E-b2 method |
| P-3 | sited parents of the sub-ids | measured (critic t-1046): sited |
| P-4 | continuation pages | `handoff_keys_pages` (`contract_slices.py:786-795`) |
| P-5..P-22 | the clause reads of t-1041 | carried in §3.1 bodies; bridges checked by t-1046 (F5 list) |
| P-23 | M2 rows need a door | read t-1056: `stage_joints.py:1001-1002` -> §3.5 |
| P-24 | §4 bodies today | read t-1056: §4.1 notes |
| P-25 | census rows | read t-1056: `dry_exits.py`, the group files -> §4.3 |

---

## §10 Readers of every touched file (designer rule 7)

Greps (Grep tool; t-1036/t-1041 lines carried, t-1056 lines added):

| search | over | hits | positive control |
|---|---|---|---|
| `ahead-cards\|ahead_card\|stage-joints\|role-rules\.json\|role-load\.json\|inject-map` (t-1036) | `tools/` | 2 (`tools/test_quarantine.py:2199`, `tools/test_test_quarantine.py`) | itself |
| same (t-1036) | `.githooks/` | 0 | the tools/ run |
| `agents/qa-\|qa-factory/agents` (t-1041) | `tools/`, `.githooks/`, `.claude/settings.json`, `.claude/agents/`, `.claude/skills/` | 0 package charters (10 hits in tools are `.claude/agents/*.md` forge roles) | t-1041 controls (37 / 15 / 3 / 15 hits of wider patterns) |
| the 8 test file names (t-1041) | `tools/` | 1: `tools/lint-baseline.json:247` (`test_oracle_provenance.py`, `HandReaderInput` 1) | - |
| `driver-exits\|dry_exits\|told-ratchet` (t-1056, count) | `tools/` | 1: `tools/test_workflows.py` | - |
| same (t-1056) | `.githooks/` | 0 | `driver-exits\|dry_exits\|told-ratchet\|python` over `.githooks/`: 15 |
| same (t-1056) | `.claude/settings.json` | 0 | t-1041's 37-hit control on that file |
| `dry_exits\|driver-exits` (t-1056) | `.github/` | 3 in `.github/workflows/dry-story.yml` (the CI step) | - |
| `dry_exits` (t-1056) | `PKG/scripts/` | 6 files: `test_scenario_dry_1.py`, `dry_exits.py`, `dry_world.py`, `test-layers.json`, `fixtures/driver-layers.json`, `driver-exits/classes.json` | - |

The `.claude/` whole-folder search times out (worktrees under `.claude/worktrees/`); the narrowed paths cover settings,
roles and skills.

| touched file | readers | verdict |
|---|---|---|
| `stage-joints.json` | `stage_joints.py`, `contract_slices.py`, `dry_exits.scan_joints`, `selftest.py:722`, `tools/test_quarantine.py:2199`, refusal transports; `tools/owns_readers.py` scope "data" | unchanged code; rows in -a, hand_cards in -b, unsited in TBW-T1rc-int; T9c and wave B also write (§7) |
| `driver-exits/*.json` (4 groups) | `dry_exits.py` (`--check`), `dry_world.py`, `test_scenario_dry_1.py`; CI `dry-story.yml`, the `full` job line `dry-1/census`; `tools/test_workflows.py` (a workflow test naming the step) | -a adds rows; readers unchanged; other writers: §7 |
| `ahead-cards.json` | `stage_joints._hand_cards`, `contract_slices.ahead_card`, `brief_pack.ahead_card`, test readers (T10) | -b data and the keep readers; quarantined: E-7 |
| `role-rules.json` | `role_rules.py`, test_role_rules, `stage_joints._row_requirement` (role_rule join `:1022-1027`) | -b |
| `agents/qa-*.md` | the host; `host_adapter.role_has_bash` (`tools:` line, untouched); role_load; role_rules; `test_ahead_cards.charter_card_join` | -a K lines; -b the strategist line |
| `slices/*` | the injection, role_load (K10, A22), role_rules (anchors on pages) | regenerated in -a and -b |
| `inject-map.json` | `inject_context.py`, role_load, contract_slices K8 | continuation lines in -a (and -b) |
| `role-load.json` | `role_load.py`, test_role_load | -a raise, -b shrink; K1b, FV2-90 first or merged |
| `test_ahead_cards.py` | `test_validator_class.py:47` imports `VOCABULARIES` and `cards()` | -b, same commit |
| `test_oracle_provenance.py` | `tools/lint-baseline.json:247` | -b; a changed count is named, never raised silently |
| `test_stage_joints.py` | `slow_tests.json` | TBW-T1rc-int (`UNSITED_CAP`), then -b (told rows) |
| `told-ratchet.json`, `s5_precheck.py`, the site scripts | `test_stage_joints.py` (K4), `tools/` none for told-ratchet (count above) | TBW-T1rc-site (its own spec) |

---

## §11 Small choices closed by the designer

- S-1 Report files `20261117-tbw-t1r-cards-{a,b}-report.md`; changelog fragments `tbw-t1r-cards-{a,b}.md`.
- S-2 K section by kind: procedure -> `## Tools`, craft and rationale -> `## Techniques`.
- S-3 Witness sub-id suffix = the role name without `qa-`.
- S-4 Row ids: `artifact_producer:validate`, `gate_preflight:question_branches` (`gate_preflight.py:2113`).
- S-5 Door of a NEW witness row: "edit the field (row) the refusal names in <artifact>".
- S-6 A split clause keeps card order inside each row.
- S-7 The test and S-K reader is `handoff_keys_pages` joined by "\n".
- S-8 (t-1056) A landed clause that began lowercase after a cut ("every ...", "give ...") starts with a capital; a clause
  that begins with a path or code stays as it is; ";" at a clause end becomes ".". The fa-1f card typo "role;`mechanism`"
  gets its space.
- S-9 (t-1056) A door text carries no final stop (`told_line` adds it); sc-4's door keeps its capital "A".
- S-10 (t-1056) The four M2 doors (§3.5) are written from the bodies' own way-on words (R2-F2 (a) road: designer text,
  checked at acceptance).
- S-11 (t-1056) Census rows: reach `unwalked`, the why sentence of §4.3, the `raised_by` who-field "T1r-cards-a, 2026-11-17".
- S-12 (t-1056) `profile.none` carries no `door_needs` (its door names no command) but `when: ["shell"]` (the clause is
  about a `--mine` call); `values_rename` carries `door_needs: shell`.

## §12 Not done / not established

- No command was run (no shell): the unsited numbers 46 / 17 and the sited/unsited split are critic t-1046's measured run;
  46 is also the stored value I read.
- Wave B at its new head `f88a5e38` was not re-read.
- `raise_question_errors` (cd-4d) and `completeness` of `source_inventory` were not opened; both are on the safe side.
- The K8 / K10 / A22 numbers after -a are not measured (the builder measures, E-9).
- `scenario_walk --witness-for` on the four driver-exits files: I could not run it; if it prints "no scenario or keep row
  covers", the `dry_exits.py --check` `test:` line is the judge (builder-rules 7b).
- Whether every role entry of the A rows is already told by the page: assumed from T1r; a row whose role has no page line
  is caught by S-K (E-11) and reported.

## §13 Reading trail (t-1056)

The r2 spec whole; critic t-1046 whole; `.git/HEAD`, `.git/refs/heads/main`, `.git/packed-refs` (Grep), the wave B loose ref;
r1 §4 (`20261114-...-t1r-cards-spec.md:119, 140, 334-344`); `ahead-cards.json` whole; `docs/SIBLING_MAP.md:644-655` and the
axis list; `dry_exits.py:1-36, 521-550, 575-634, 636-783, 848-881` and its constants (Grep); `driver-exits/s1-s4.json`
whole, the ratchet blocks of every group (Grep); `stage_joints.py:286-345, 581-608, 966-1027, 1093-1267` (and Grep of its
names); `test_stage_joints.py:920-964` (and Grep); `told-ratchet.json` (Grep `s5_precheck`); `null_outcomes.py:198-210`;
`s5_precheck.py:290-301, 2100-2223, 2395-2424` and `FRAGMENT_ROAD :125`; `execution_request.py:1760-1839, 3750-3779`;
`profile_contract.py:544-549`; `execution_fingerprint.py:60-179`; `run_suite.py:2096-2107` and `--template` (Grep);
`handoff_check.py:3194-3213`; `source_preflight.py:1-55`; `manifest_put.py:1080-1091, 1250-1310` and `expectation_change_verdicts`
(Grep, 8 hits); `stage-joints.json` rows (Grep of every touched id; reads :114-231, :494-561, :3879-3987, :5675-5704,
:6289-6332); `planning_contract.py:1476-1507`; `native_context.py:165-179`; `role_load.py:300-349`; `role-rules.json:160-165`
and the ids of the anchor lines (Grep); `agents/*.md:4` (Grep `^tools:`, 12 hits); `agents/` Grep "card" (-i);
`qa-case-designer.md` Grep; `check_witness.py:45-254` and its defs; `exit_gate.py:110-151, 1636-1758, 1894` and its defs;
`validate_artifacts.py:376-408, 2485-2534` and its `def check_` list; `contract_slices.py` (Grep: :583-591, :681-691,
:711-723, :786-806); `plans/builder-rules.md` 7b (Grep); `plans/piles/told-before-work/batch-1-finish.md` (Grep);
`plans/piles/live-run-fvf/batch-2-live-run-fvf.md` and `batch-3-...md` (Grep of ids, statuses, `driver-exits`);
`plans/piles/rules-debt/batch-1-phase-2.md` (Grep); the §10 greps.
Needed beyond the manifest: `dry_exits.py`, the driver-exits fixtures, `execution_fingerprint.py`, `profile_contract.py`,
`run_suite.py`, `null_outcomes.py`, the pile batch files.

---

## Fix round t-1056

| finding | what changed | where in r3 |
|---|---|---|
| F1 (blocking) axis 38 | -a owns `driver-exits/s1-s4.json`, `s5.json`, `s6-s9.json`, `gates.json`; 12 census rows (`unwalked` + why) and 12 `raised_by` entries in the same commit; DoD runs `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check` -> 0 discrepancies; siblings name axis 38; order line vs the driver-exits writers; E-14 | §4.3; §6 -a (owns, scope, DoD, A-9, siblings); §5 E-14; §7 |
| F2 unsited +6 | recount: command `stage_joints.py --check`; stored 46 (main), measured 46 / 17 (t-1046); +6 = 4 function rows + `sides.provisional` + `sides.pending`; every new unsited row sited by TBW-T1rc-site, which now owns `s5_precheck.py` and `told-ratchet.json`; R3-F2 line corrected | §4.4; §7 (nodes); §8 R3-F2' |
| F3 witness form | §3.4 holds every landed text, door and K line in full (JSON block); the witness is the `--witness-for` run; S-K is the supplementary key-presence check with keys from §3.4, script in full, negative control `--negative` | §3.4; §6 -a (DoD, S-K); §8 R3-F3' |
| F4 §4 rows | the five rows written whole from bodies re-read at c9b42659 (no r1 needed); `profile.none` door = the refusal's own (fork R4-F4); E-13; own find: `fingerprint.build` "keeps its bytes" cut | §4.1; §3.4 keys `4-*`; §5 E-13; §8 R4-F4 |
| F5 sc-3 / ck-3b | sc-3 text conditioned on the file existing or being required; ck-3b "`critic_note` (owed with `could_not_judge`)" | §3.4 `sc-3`, `ck-3b`; §3.1; §3.2 |
| F6 role-rules :163 | -b restates the `rule` text of `designer-one-case-per-plan-row`, returned as a Lead fork with the text | §8 R4-F1; §6 -b owns scope, B-3 |
| F7 values_rename door | producers narrowed to the 9 Bash roles, `door_needs: shell`; no-Bash door queued to TBW-T1rc-site; E-10 names the residual; Lead fork | §4.1; §5 E-10; §7; §8 R4-F3 |
| F8 Codex ceiling | E-9 restated: K10 rises named as `U-H` from the K10 line; U > 100,000 B (a runtime refusal, not a cap): STOP before commit; R2-F6 re-opened for the owner, recommendation (b), -a executable on it | §5 E-9; §6 A-7; §8 R2-F6' |
| F9 hand-card method | E-b2 gives the temp-plugin method, the four rows and their exact expected sentences | §6 -b E-b2, B-10 |
| F10 line shifts | -b names the told loop by content; wave B adds no row (E-12 settled); bodies cited at c9b42659 | §6 -b owns scope; §5 E-12; §7 |
| F11 collisions | order lines for RD1-1, FV2-81/82, the driver-exits writers (FV2-15, FV3-1/2/3/5/6/15/20) and FV2-90 (found this round); -a waits on K1b's whole chain (FV2-79 "ожидает") | §7; §6 -a order |
| F12 integrator | node TBW-T1rc-int (owns `told_ratchet.unsited` and `UNSITED_CAP`) commits on the wave-C integration branch before main; -b starts from that commit; -a's DoD expects the one unsited finding | §7; §6 -a DoD, §6 -b order |
| F13 ts-3a | K text: "An oracle you cannot settle is `oracle_unknown: true`; add `source_conflict: true` when the sources disagree." | §3.4 `ts-3a`; §3.1 |
| F14 accounting | "cd-4a is skipped: its fact is the role-rules anchor already in the charter"; E-5 restated | §3.1 accounting; §5 E-5 |
| F15 EC-8 class | -a's report records every pre-append sentence (E-4); TBW-T1rc-ec8 gains the original-sentence sweep and the `check_case_form` refusal text (`validate_artifacts.py:384`) | §5 E-4; §6 -a handoff; §7 TBW-T1rc-ec8; §3.3 |

## Lead decisions on the forks of r3 (17.11.2026, Fable; made in the owner's absence, by recommendation, until the owner's word)

- **R2-F6' — (b), and a question to the owner.** A role whose plugin share alone would exceed 100,000 B after -a: the builder STOPS before
  the commit and reports the role and the bytes. The owner's word on raising size limits (16.11.2026) is NOT read onto a runtime refusal of
  the host. The question stays open for the owner in the morning report.
- **R3-F2' — (a).** `unsited` is +6; `s5_precheck.py` and `told-ratchet.json` join node TBW-T1rc-site.
- **R3-F3' — (a).** No committed test in -a; the witness is the `--witness-for` run; S-K is a supplementary key-presence check.
- **R4-F1 — (a).** -b restates the registered rule `designer-one-case-per-plan-row` with the text of §8.
- **R4-F2 — (a).** -b re-points `qa-test-strategist.md:74` and the role-rules row `strategist-letter-branch-follows-card` away from "the card".
- **R4-F3 — (a).** `values_rename` goes to the 9 roles that have a shell; the no-shell door is queued to TBW-T1rc-site.
- **R4-F4 — (a).** `profile.none` takes the refusal's own door.
- **Stale base.** r3 was read at main `c9b42659`; wave B is merged since (`7b095bad`): the dispatch of -a re-cites the `validate_artifacts.py`
  lines and uses the "after wave B" numbers of §4.4.
- **Order.** K1b (FV2-79) waits for the C3 topic branch (C3-b1 raises the `qa-code-critic` share that K1b pays down); -a waits for K1b.
- New nodes to enter in the pile at the next status pass: TBW-T1rc-int, TBW-T1rc-site, TBW-T1rc-ec8.
