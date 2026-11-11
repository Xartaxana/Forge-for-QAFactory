# t-1349 — class sweep: validators a role meets, S0–S9 and onboarding (release 0.10.3)

Read-only. Tree: the pile `D:/ws1/wt-speed-cost-b1\ai-packages\qa-factory` (called `pile:` below; paths are under
`scripts/` unless said). No code was run for this sweep; every verdict is from reading the validator and its carriers.
Class (owner's word 27.10): **a role does not learn before the work which fields and values a validator accepts (FR-38,
AR-10), and the refusal lists problems one at a time / without a record position (FR-1, Axis 17 K1).** Instance: t-1347.

Verdict key. A: does the role learn the accepted fields BEFORE the work (charter / ahead card / brief / template or skeleton),
or only via `--help` / a refusal. B: does ONE refusal list ALL problems with a record locator. C: does the refusal name the
fix and the closed list. OK / A-gap / B-gap / both. "SC1-14" marks a file owned by the running node (story_step.py, controller.py,
s5_plan.py, brief_pack.py, exit_gate.py, s5_precheck.py).

## 1. Where the validators come from (how they were found)

- `references/role-commands.json`: 15 commands, the registry that `role_cli.refuse` and `role_cli.epilog` print (the seam).
- `references/ahead-cards.json`: 12 cards (qa-scout 933 B ... qa-automator 1196 B; budget 1,200 B), rendered by
  `brief_pack.ahead_card` (SC1-14).
- `references/stages.json` `detectors`: S2 sizing.py, S3 planning_contract.py, S4 critic_rollcall.py, S5 s5_precheck.py,
  S8 check_coverage.py. Gate: `exit_gate.all_errors` (:1093) aggregates them.
- Validate-on-write: `validate_artifacts.collect_errors` (:2331) and `references/artifact-writers.json` (the artifacts whose
  writer is "(the role)": context-manifest, requirements-register, requirements-readiness, understanding, test-plan.md/.json,
  grounding.yaml, test-cases/, critic-findings, triage, bug-drafts, bugs, test-report, retro, obligations, backlog).
- `record-schemas.json` consumers: `record_schema.validate_record` is called by context_bundle.py:208,
  validate_artifacts.py:2402, and (code-written, not role-facing) controller.py:2038/3632, event_store.py:447,
  execution_request.py:333.

## 2. Shared collectors (AR-15: one fix covers many)

| Collector (survivor) | Covers |
|---|---|
| `validate_artifacts.collect_errors` (one `errors` list, every `check_*` appends; :2331) | the write hook for every role artifact above; `exit_gate.collect_errors`; `artifact_producer.validate` (calls `check_bug_form`, `check_case_form`, `check_triage_v0`); `validate_artifacts.py --check` |
| `detector_verdict.compound` (:412) | `record_schema.validate`, `case_versions.validate_batch`, `context_bundle` SC1-7 compound, `controller._raise_all` |
| `detector_verdict` form 1 (`REJECT - N finding(s)`) | s5_precheck, planning_contract, critic_rollcall, check_coverage, check_witness, claim_projector, grounding_table (Axis 17) |
| `record_schema._problems` (:17, location paths `$.a[2].b`) | ContextBundle (build, `--validate`, write hook) and the code-written Event/Dispatch/Decision/RunRequest |
| `role_cli.refuse` / `epilog` over role-commands.json | every row of section 3 marked "card" |
| `window_record.REQUIRED_ROW_FIELDS` + renderers (Axis 23/28) | `tests[]` row: manifest_from_tests, s5_precheck, acceptance, window_record. THE MODEL for the A half |
| `handoff_check.check` + `handoff_init` form + `values_skeleton` (:1203, :2141) | every handoff yaml: form is generated, all problems listed, a values skeleton is printed. THE MODEL for A+B+C together |

The class is NOT in the collectors above; it lives in the validators that bypass them (section 3, rows marked B-gap/A-gap).

## 3. Table

| # | Stage / role | Validator (script:function:line, pile) | A (told before the work) | B (all problems, with locator) | C (fix / door) | Verdict |
|---|---|---|---|---|---|---|
| 1 | S1 scout | context_bundle.py `_validate_v2_discovery` :242-286, `_require_fields` :219, `_string_list` | coverage_search / existing_test_candidates fields only in role-commands card (`--help` / refusal); ahead card :11, brief build line, coverage-design.md say no field; qa-scout.md:86 prescribes `status: not_found`, which :264 refuses. requirement_sources now code-derived by the inventory overlay when `--root <story folder>` is given | first problem only (`raise` per check); missing-field and non-empty-string refusals carry no `[i]` | card is printed; closed lists printed on enum errors | **both** (the instance) |
| 2 | S1 scout | validate_artifacts.py `check_context_manifest_v0` :2067 (write hook on context-manifest.json) | related / implementations fields: card + artifact-contract-grounding.md | OK, `related[i]`, `implementations[i]` | OK (lists printed) | OK for its subject. **Gap: it does not check the v2 sections at all**, so the earliest feedback on them is the build; the write hook is where the same collector should run (row 1 fix) |
| 3 | S1 scout | context_bundle.py `_manifest_source_problems` :46 (SC1-7), `validate_bundle` :207, schema `ContextBundle` | implementations: see row 2 | OK (compound over `implementations[]`) | OK | OK. `validate_bundle` itself raises first of two (diff > 160 lines, grounding mismatch) :210-213: hand-written bundles only |
| 4 | S1 scout | validate_artifacts.py :2399-2405 (write hook on context-bundle.json) | bundle is code-built | `validate_record` raises first, so `validate_bundle` never runs after a schema error: two stages, each complete, the second hidden by the first | card | B-gap, low (hand-written bundle only) |
| 5 | S1 (code) | source_inventory.py `validate_inventory` :2057; ticket_adapter.py verbs | written by the adapter from flags, not by the role | OK, `sources[i].field` | "is invalid" (:2071-2075) without the closed list | C-gap, low (not role-written data) |
| 6 | S2 tester | validate_artifacts.py `check_register` :428, claims :536, delta :515 (write hook, exit gate) | OK: templates/requirements-register.md + ahead card | OK (accumulator) | OK | OK |
| 7 | S2 tester | check_witness.py `readiness_check` :199 / `_readiness_form` :111; `artifact_producer.validate` :70; publish | OK: card + `artifact_producer.py prepare readiness` skeleton | OK, `open_questions[i]`, `aspects.k`. Analog: a non-dict row raises `AttributeError`, caught as "invalid artifact structure: ..." (artifact_producer.py:~86) and the rest is lost | "needs question, severity, owner_role" does not say which of the three is wrong | B-gap, low |
| 8 | S2 tester | validate_artifacts.py `check_understanding` :1654 | card + templates/understanding.md | OK | OK | OK |
| 9 | S3 strategist | planning_contract.py `validate_plan` :107 (write hook, exit detector) | OK: charter :144 -> references/risk-policy.md:37-39 lists the 12 fields; card names the depth rule | OK, `<row id>: ...` accumulates | C-gap: "invalid verification depth" :127, "invalid starter likelihood/confidence/impact" :150 do not print the closed set | C-gap |
| 10 | S3 strategist/designer | plan_row.py `_plan_check` :248 (`own[:6]`, "+N more") | charter + command card | **cap of 6**: the role sees 6 of N and must re-run; Axis 17 closing rule bans a line-count cut on a finding list | OK | B-gap, low |
| 11 | S3 strategist | grounding_table.py `check` :1189, claim_projector.py `s3_claim_errors` :691 | grounding.yaml skeleton is built by code | OK (form 1, `[grounding R<n>]`, `[claims ...]`) | OK | OK |
| 12 | S3/S4 designer | question_register.py `_raise` :980, `_common_problems` :720, `claim_question` (contract.py:954) | charter :58/:111: "a one-line `raise_questions` entry"; the entry's fields only in the refusal | OK (list `- problem`) | "Valid: ..." printed | A-gap, low |
| 13 | S4 designer | validate_artifacts.py `check_case` :155, `check_case_form` :333 (write hook, exit gate) | OK: ahead card + `artifact_producer prepare case` skeleton | OK (accumulator); `preconditions` sliced `[:4]` :208 (analog kept by Axis 17) | OK (lists printed) | OK |
| 14 | S4 critic | critic_rollcall.py `findings_errors` :419 (write hook on critic-findings.md) | OK: card | OK | OK | OK |
| 15 | S4 | case_versions.py `validate_batch` :122 | n/a (code) | OK compound; `_pin_batch_unlocked` :289 raises first (queued in Axis 17) | OK | OK / queued |
| 16 | S4-S9 all producers | artifact_producer.py `validate` :70, `validate_batch` :120, `publish` | OK: `prepare <kind>` skeleton; card | OK per item (`artifacts[i]`); "invalid case status/channel", "invalid bug status/severity" :99,:105 do not print the sets | C-gap | C-gap, low |
| 17 | S5 automator | validate_artifacts.py `check_manifest_v0` :1872, `check_manifest_invariants` :1932, `check_remedy_rows` :1971 (write hook on automation-manifest.json) | card + s5.md + row form printed after write | OK (names the test / case) | OK (names `manifest_put.py` door) | OK |
| 18 | S5 automator | manifest_put.py merge: `_problems_text` :737, `expectation_change_problems` :825, `novelty_row_problems` :450; single `raise ValueError` in `_retract_*` :509-632 | card + role-commands card (keys of a fragment) | mostly OK (joined, full list in `state/findings/manifest-put-*.txt`); the retraction family raises on first | OK | OK, retraction family B-gap low |
| 19 | S5 | window_record.py `row_field_gaps` :247 (+ renderers Axis 23/28) | OK: carrier rendered by manifest_from_tests `_row_form`, s5_precheck, s5.md | OK (one finding naming every missing field) | OK | OK, the model |
| 20 | S5 automator | s5_precheck.py `run`/`report` :2542 (SC1-14) | OK: card | OK (form 1) | OK | OK; **no change needed** |
| 21 | S5 code critic | probe_by_code.py Refusal :1207-1214 | card | OK (joined) | OK | OK |
| 22 | S5/S6 runner, automator | execution_fingerprint.py `build` :84-87, `_input_record` :21 | **spec keys (`source_revision`, `test_files`, `config_files`, `dependency_files`, `runtime_provenance`) in no charter, stage card or ahead card** (0 hits for `dependency_files` in agents/, skills/, ahead-cards.json; control `dependency_files` in role-commands.json:111 hits); qa-runner.md:101 only names the script | **first missing key** (the card says so: "names only the first one missing"); then per-file raises one by one | card | **both** |
| 23 | S6 runner | manual_evidence.py `validate` :68, `write_block` :649, `validate_baseline_record` :238 | OK: `build` writes the record, `prepare` prints `required_actual_fields`; card | within one record OK; **no record index**, and `sorted(set(issues))` :663 folds equal defects of different records into one line (count and place lost); `ValueError` joined by "; " | "invalid result", "invalid evidence_policy" :100,:103 do not print the sets | B-gap (+C-gap) (Axis 17 queued item) |
| 24 | S6 runner | manual_capture.py `parse_steps` :453 | OK: card + references/manual-capture-steps.json | OK (`line N`, all lines); after that the first-`goto`/stand checks are single raises :495-499 | OK | OK |
| 25 | S6 (code) | validate_artifacts.py `check_run_report_v0` :2125, `check_result_rows` :2139; check_witness `run-report.json` rule | run-report.json is written by finalize_task.py (artifact-writers.json:118); the qa-runner ahead card still lists its fields as if the role writes it | OK | OK | A-note: stale card target (harmless) |
| 26 | S7 analyst | check_witness.py RULES["triage.json"] :214 + validate_artifacts.py `check_triage_v0` :2190 + artifact_producer `instance_id and attempt_id required` | card lists verdict / evidence / FLAKY fields; **`instance_id` and `attempt_id` (required by artifact_producer.validate) are not in the card**, only charter :94/:99 | OK (indexed); the verdict is checked twice in two spellings; non-dict row: same AttributeError loss as row 7 | OK | A-gap (2 fields), low |
| 27 | S7 analyst | bug-drafts/*.json (bug_records.py:161-257 reads them) | charter :90 lists the draft's fields in prose; no validator on write for a draft's shape found (grep `bug-drafts` in validate_artifacts.py: 0 hits; control `bugs` branch :2346 hits) | n/a: nothing to list | n/a | queued question: is a draft validated anywhere before gate B? Not established |
| 28 | S8 scribe | validate_artifacts.py `check_test_report` :955 and `check_report_*`; report_facts.py `check` :2301 | OK: card + templates/test-report.md + `report_facts --write` | OK, except `check` returns after marker problems :2321 (justified: no block can be compared before the markers parse; Axis 17 K1 invariant "no check on data it cannot read") | OK ("repair ... or have the scribe redo") | OK |
| 29 | S8 scribe | check_coverage.py main :214; check_delivery.py `main` :1875 | card | OK (`REJECT - N problem(s)`) | OK | OK |
| 30 | S8 bug reporter | validate_artifacts.py `check_bug` :366, `check_bug_form` :383; external_writes.py `record_result` :816 | OK: card + `prepare bug` skeleton | OK (accumulator) | OK | OK |
| 31 | S9 retro | estimate_record.py `append_record` :62-68; facts file | card names the LEDGER row (ts, task, forecast, actual, delta, hit, drivers) but the role passes a FACTS file (`forecast`, `actual`, `drivers`); code derives the row. Charter :85-86 says "forecast/actual/drivers" | sequential `raise`: shape, then forecast/actual, then drivers | OK message text, no closed example | **both**, low |
| 32 | S9 retro | project_decisions.py `add_finding` :260 (`_REQUIRED`), scope_refusal | card + `--help` | `_REQUIRED` = one sentence for three fields, fine | OK (scope words printed) | OK |
| 33 | onboarding / S0 | validate_artifacts.py `check_config` :2316 -> config_contract.py `validate` :309, `access_errors` :127, `environment_errors` :174 | OK: templates/config.json | OK (path-named, indexed) | C-gap: `requirements_sources[i].kind is invalid` :329 and `.status is invalid` :331 print no closed set | C-gap, low |
| 34 | onboarding | onboarding_notes.py (closed lists from data file, `NotesError`) | data file | single `NotesError` | names the file | OK (code-read, not role data) |
| 35 | gate | exit_gate.py `all_errors` :1093, `scoped_errors` | aggregator | OK: every finding of every detector in one block, then released | OK | OK (SC1-14; no change) |
| 36 | code-written records | controller.py `check_decision` (record-schema early return, Axis 17 queued), event_store.py:447, execution_request.py:333 | not role-facing | n/a | n/a | out of class; controller.py is SC1-14 |

Summary (hand count): both A and B gaps: rows 1, 22, 31. A-gap only: 12, 26. B-gap only: 4, 7, 10, 23 (and 18 for the retraction family). C-gap only: 5, 9, 16, 33. All other rows OK or out of class.

### Negative claims and controls (case-insensitive, same shape)

- Row 22: `grep -rn -i "dependency_files" agents skills references/ahead-cards.json` = 0 hits. Control, same command shape on
  `references/role-commands.json` = hit at :111.
- Row 1 (from t-1347, re-checked on the pile in §R of that report): ahead-cards.json / coverage-design.md unchanged.
- Row 9: `likelihood` / `verification_depth` have 0 hits in qa-test-strategist.md and artifact-contract-plan.md, but 1+ hits in
  references/risk-policy.md:37-39 and the charter points to it at :144, so A is OK. (A negative on the charter alone would
  have been wrong.)
- Row 12: the entry's field names for `raise_questions` were not found in the designer's charter lines :58/:111; the
  contract text was not searched for them, so this row is "not established", not "absent".

## 4. What the table says about the class

1. B is mostly solved: the write hook, exit gate, form-1 detectors, handoff_check, compound readers all accumulate. The
   remaining first-error sites are small and concentrated in **code-called validators written by hand with `raise ValueError`
   per check**: rows 1, 22, 23, 31, 18 (retractions), and the two-stage row 4.
2. A is solved only where a **carrier is rendered to the role**: Axis 23/28 (`REQUIRED_ROW_FIELDS`), the handoff forms,
   `prepare <kind>` skeletons, templates. Where the field list lives in a validator and is retyped by hand into role-commands.json
   and/or an ahead card, it drifts or is missing: rows 1, 22, 26, 31. `test_ahead_cards.VOCABULARIES` pins only the closed lists
   somebody added to the table by hand; a validator whose fields are not in the table is invisible to it.
3. The two halves meet at ONE seam per half: B at `detector_verdict.compound` (+ `record_schema._problems`); A at
   `role_cli.registry()` (role-commands.json -> every refusal and `--help`) and `ahead-cards.json` (-> brief_pack). A fix at
   those survivors covers all rows.
4. The write hook is the earliest, cheapest place to teach: a manifest section checked at write time (row 2) turns "first
   feedback at the build" into "feedback in the turn that wrote it".

## 5. Proposed fix as the class

Rule to state (FR-38 / AR-10 check, one line added to the change check): *a role-facing validator (a) returns a list and
raises once through `detector_verdict.compound`, every item carrying its record locator `section[i].field`; (b) takes its
required fields and closed lists from ONE named constant; (c) that constant is rendered into the role's card by code, or pinned
to it by `test_ahead_cards`.* Architecture lines the commit names: AR-10, AR-13, AR-15, AR-18, AR-22.

### N1. The instance, closed (context_bundle + write hook + card) - about 85 lines incl. tests

- context_bundle.py: `V2_REQUIRED` (dict: section -> required fields; closed lists already at :13-16) read by
  `_validate_v2_discovery`; the function COLLECTS `<section>[i].<field>: missing | must be a non-empty string | must be one of ...`
  and raises one `compound` (same shape as `_manifest_source_problems`). About 40 lines.
- validate_artifacts.py `check_context_manifest_v0`: call the same collector on the manifest's v2 sections (names prefixed
  with the manifest file name). About 15 lines. (Row 2.)
- ahead-cards.json qa-scout card (+3 lines, stays under 1,200 B: 933 B now, about 270 B free): coverage_search and
  existing_test_candidates field names, per-area status `complete|partial|unavailable`, "nothing found = top-level
  `coverage_status: not_found`". qa-scout.md:86 one line.
- Tests: in test_context_bundle.py two bad records in each section -> one refusal listing all, each with `[i]`; the same
  manifest through the write hook; card == `V2_REQUIRED` (test_ahead_cards VOCABULARIES row); `status: not_found` in
  coverage_search refused with the list, top-level accepted.

### N2. Collectors at the other first-error sites - about 90 lines incl. tests

- execution_fingerprint.py `build`: collect missing keys and per-input problems (`test_files[2]`, ...) into one compound
  (about 25 lines). Add the spec's five keys to the qa-runner and qa-automator cards or to `s5.md` and pin them. (Row 22.)
- estimate_record.py `append_record`: collect the three shape checks; the card names the FACTS file keys, not the ledger row
  (about 10 lines + 1 card sentence). (Row 31.)
- manual_evidence.py `write_block` :663: prefix each issue with `records[i]:` and do not fold with `set()`; `validate`: print the
  closed sets for "invalid result" / "invalid evidence_policy". About 12 lines. (Row 23; closes the Axis 17 queued item.)
- record_schema.py `_problems` :31: enum message "unsupported value (one of a, b)" and "too short" -> "must not be empty"
  (about 4 lines; one survivor, improves every schema-checked record incl. ContextBundle). Check `test_record_schema.py` and any
  reader that matches the old text (`grep "unsupported value"` before the change).
- artifact_producer.py `validate`: wrap per ROW not per artifact, so a malformed row does not hide the others (rows 7, 26);
  print the closed sets for status/channel/severity (row 16). About 15 lines.
- planning_contract.py :127, :150: print the allowed sets (row 9); plan_row.py `_plan_check` :257: use
  `detector_verdict.joined(..., full_path=...)` as manifest_put does instead of `own[:6]` (row 10). About 12 lines.
- check_witness / artifact_producer triage: add `instance_id`, `attempt_id` to the qa-failure-analyst card (row 26, 1 sentence).

### N3. The guard for the class and the publisher (smaller variant now, generator later) - about 90 lines

Now (0.10.3): `scripts/tests/test_validator_class.py`, table-driven like `test_ahead_cards.VOCABULARIES`:
1. BATTERY: a table `ROLE_VALIDATORS` of `(name, callable-or-CLI, record with exactly 2 defects, the two needles)`. For every
   row: one call lists BOTH defects, and each is preceded by its locator (`[i]`, a name, or a path). Seed it with the rows in
   section 3 marked OK (so a regression to first-error is caught) and with N1/N2 sites. Negative control: a validator stub that
   raises on the first defect must make the battery fail.
2. CENSUS A: for every key of `references/role-commands.json` whose `input` text names record fields, and every
   role-written artifact of `artifact-writers.json` ("(the role)"), the table must hold a row `(role, carrier constant,
   card)` and the card text must contain every name of the carrier (the existing VOCABULARIES mechanism, extended with:
   `V2_REQUIRED`, the fingerprint keys, estimate facts keys, triage `instance_id`/`attempt_id`). A command or artifact with no row
   fails the test with "name where the role is told" (the AR-10 change check made executable).
3. CENSUS B (static): AST scan of the role-facing validator files for `raise ValueError` inside a `for` over a records list
   (the first-error pattern) is too brittle; do NOT add it. The battery (1) is the guard.

Later (next batch, critic-on-plan because it adds a generator and edits cards by code): `scripts/field_cards.py` with
`render(name)` from the carrier constants and a `--write/--check` mode that fills marked spans in ahead-cards.json and
role-commands.json (the factory already does this with `tools/factory_rules_index.py`), so the hand-typed copies disappear.
It deliberately generates the FILE rather than expanding at load, so `brief_pack.ahead_card` (SC1-14) is not touched.

### Totals

N1 ~85, N2 ~90, N3-now ~50 + tests; N3-later ~80. Fits 0.10.3: N1 (required, the reported instance), N2 rows 22/23/31 and the
two one-line card sentences, N3-now. Defer: N2 rows 9/10/16 (C-gaps, low) if the batch is full; N3-later.
No schema change, no change to what a correct artifact produces. All of it is package code (English, FR-30, no Cyrillic).

### Ownership against the running SC1-14 node

| File | In this proposal | Wait? |
|---|---|---|
| brief_pack.py | not touched (TOOLING build line already there; cards stay data in ahead-cards.json) | no edit needed |
| exit_gate.py | not touched (aggregator, row 35 OK) | no edit needed |
| s5_precheck.py | not touched (row 20 OK) | no edit needed |
| controller.py | row 36 only (`check_decision` early return, queued in Axis 17, not role-facing) | wait; out of this class |
| story_step.py, s5_plan.py | not touched | - |
| Everything else in N1-N3 | context_bundle.py, validate_artifacts.py, execution_fingerprint.py, estimate_record.py, manual_evidence.py, record_schema.py, artifact_producer.py, planning_contract.py, plan_row.py, ahead-cards.json, role-commands.json, qa-scout.md, tests | free |

Caution for the integrator: validate_artifacts.py, planning_contract.py and manual_evidence.py are hot files for other piles
(PROJECT.md "Командная работа", rule 3); check `piles.py check` (б) before taking N1/N2 and give each node its function
list in `owns`.

## 6. Limits of this sweep (what was not established)

- Not run: nothing was executed, so B and C verdicts are from reading the code paths, not from a two-defect fixture. The
  N3 battery is what turns them into measurements; expect a few verdict changes (rows marked "OK" were read at function level,
  not exhaustively: validate_artifacts.py has about 80 check functions and I read the ones in section 3 and scanned all early
  `return` statements of `check_*` (all are "no frontmatter" / prerequisite stops).
- `handoff_check.check` (:1203) and `s5_precheck.run` were judged from their signatures, headers and the report path plus
  Axis 17's record, not read in full.
- Not covered: the guard's own refusals of tool calls (guard_pre_tool.py; they refuse actions, not role-written data);
  controller/story_run refusals to the orchestrator (not a role; SC1-14); `waiver.py`, `stage_done.py` (orchestrator doors).
- Row 27 (bug drafts) and row 12 (raise_questions fields) are open questions, not findings.

## 7. Trail

Read: t-1347 report (incl. §R); SIBLING_MAP.md Axes 17, 23, 28; design/factory-rules.md FR-1, FR-38 (FR-11, FR-14 by index
only); design/architecture.md AR-10; factory-rules-debt.md FR-38 entry; references/role-commands.json (whole),
ahead-cards.json (whole), artifact-writers.json (whole), record-schemas.json (whole), stages.json (stages/detectors);
scripts/record_schema.py (whole), detector_verdict.py `compound`, validate_artifacts.py (`collect_errors`, `check_case`,
`check_case_form`, `check_bug`, `check_bug_form`, `check_context_manifest_v0`, `check_run_report_v0`, `check_result_rows`,
`check_triage_v0`, `check_manifest_v0`, `check_manifest_invariants`, main), check_witness.py (whole), artifact_producer.py
(whole), manual_evidence.py (`validate`, `validate_record`, `validate_baseline_record`, `write_block`, main), exit_gate.py
(header, `collect_errors`, `all_errors`, tail), s5_precheck.py (header, `report`, `detector_main`, `main`), planning_contract.py
(`validate_plan`), critic_rollcall.py (`findings_errors`), execution_fingerprint.py (`build`), estimate_record.py
(`append_record`), source_inventory.py (`validate_inventory`), question_register.py (grep of problems/raise),
manual_capture.py (grep of `parse_steps`), plan_row.py (grep), manifest_put.py (grep), window_record.py (`REQUIRED_ROW_FIELDS`,
`row_field_gaps`), role_cli.py (`epilog`, `refuse`), tests/test_ahead_cards.py (header, VOCABULARIES), tests/test_role_commands.py
(grep). Agents: qa-test-strategist.md, qa-failure-analyst.md, qa-case-designer.md, qa-scout.md (greps).
Not read: handoff_check.py bodies, report_facts.py bodies, grounding_table.py/claim_projector.py bodies, check_delivery.py bodies.
