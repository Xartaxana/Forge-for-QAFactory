# TP1-15045 — test report

**The change.** A visual diff of a workflow revision (added / removed / modified nodes)
next to the existing text diff, and Save-equivalent validation before Restore through the
new `POST /v1/workflows/{id}/validate`, which persists nothing.

**Verdict: not ready to ship as is.** 4 product bugs (2 moderate, 2 minor). Of 15
requirements, 9 are proven by tests, 4 are not proven, 1 waits for a manual check, 1 is
deferred by your decision. The MR is open as a draft by your word at gate B (reason below).

`delivery_ready: no`

Notation: R-n — a requirement (the list with its text: understanding.md, "What we verify");
TC-n — a test case (test-plan.md, "Case appendix"); TS-n — a plan row; BUG-n — a bug file in
`qa-factory/bugs/`.

## Proven — 20 green tests

Visual diff — `tests/ui/workflows/test_workflow_visual_diff.py`,
`test_workflow_version_history.py`, `test_workflow_restore.py`:
- R-1 the Version History button opens the visual popup; the YAML diff is a separate popup (TC-001) — reviewed by the code critic, sensitivity proven by a red probe
- R-2 one graph, one set of zoom / fit / pan controls (TC-002) — green, critic review not recorded
- R-5 modified node: amber border, changed values hidden (TC-005) — reviewed, red probe
- R-7 markers follow the selected pair of revisions, 3 variants (TC-007) — green, review not recorded
- R-9 restoring a valid revision: no issues shown, nothing persisted, from both popups (TC-011) — green, review not recorded

Validate — `tests/workflow/test_workflow_validate_api.py`:
- R-10 validate answers like PUT: valid config, warning, missing assistant, broken graph, autonomous (TC-012, 5 variants) — review not recorded
- R-11 validate changes neither the workflow nor its version list (TC-013) — reviewed, red probe
- R-12 validate answers 403 / 404 / 400 like PUT (TC-014, 3 tests) — reviewed, red probe
- R-13 existing versioning and the text diff are not broken (TC-009, 3 existing tests) — green

"Review not recorded" means the critic never gave a verdict (the factory's own round cap):
the test is green, but it is not proven that it fails on a broken product.

## Product bugs — 4 (BUG-1…BUG-4 in `qa-factory/bugs/`)

1. **Moderate · R-4 · TC-004** — a removed node loses its former position on every
   re-render: the layout is re-run unconditionally — `buildVisualDiffGraph.ts:166`
2. **Moderate · R-3 · TC-003** — an unchanged node gets a second ADDED badge
3. **Minor · R-12 / R-13 · TC-009, TC-014** — in a 404 body `details` and `help` are not
   null; the contract requires null
4. **Minor · R-10 · TC-012** — validate rejects a workflow's reference to itself but does
   not name the offending input — `resources.py:100-159`

## Left with you

1. **Guardrails in validate (R-10, TC-012).** To check: a config that assigns a guardrail
   that is missing, belongs to another project or is not permitted gets from validate the
   same 400 and the same message as from PUT. There is no test: localhost has no guardrail
   integration data (AWS Parameter Store keys). Your decision at S5: run it where the keys
   are. How: add a `guardrail` variant to `test_validate_matches_update_outcome_per_partition`,
   or check by hand.
2. **Guardrails untouched by validate (R-11, TC-013).** To check: the workflow's guardrail
   assignments before and after a validate call are identical. The green test
   `test_validate_persists_nothing` does not contain this check — same reason. How: add a
   read of the assignments before and after, run in the same place.
3. **A read-only user cannot Restore (R-14, TC-015).** Never executed: no read-only account
   on preview. A defect is suspected — MR 1881 dropped the `canRestore` gate. Needed: the
   account, or a check by hand, or your "accept the risk".
4. **Read-only diff (R-6, TC-006) and the YAML editor with history (R-8, TC-008)** fail on
   localhost 4 of 4 and 7 of 7 times — the stand does not carry a long session (30 s timeout
   on an element). No decision recorded: fix the stand / run on another stand / defer with a
   reminder / accept the risk.
5. **Error on restoring an invalid revision (R-9, TC-010)** — unreachable: the platform
   validates a config before any write, so a revision with an invalid config does not exist
   (this was true before this story). Needed: your "accept as unreachable".
6. **Regression** — the factory does not run it; three commands in test-plan.md,
   "Recommended regression".

## Not proven, and what it costs

- **R-3, R-4** — bugs 1 and 2; the tests are red correctly.
- **R-6, R-8** — the tests fail on the stand before their own checks (item 4 above): the
  read-only mode and the text diff are unverified.
- **R-14** — never run; a read-only user may be able to Restore.
- **R-10, R-11 in part** — guardrails (items 1–2 above).
- **R-15** — deferred by your decision at gate A (Q3: where to show a removed node whose
  revision has no layout meta; the code puts it at {0,0}). The question's text:
  test-plan.md, "Gate A question packet".

## Decided at gate B (23.09)

- Bugs: not filed in Jira — "collect all bugs into a file and show them to me in chat";
  collected in `qa-factory/bugs/BUG-1…4`.
- MR: "create a draft MR; put the main conclusions and the bugs into its description —
  reason: draft for review, gaps tracked separately as obligations / open items".

## Factory defects — nothing is wanted from you

The manifest schema changed in the middle of the story. Consequences: 14 run rows are not
joined to the manifest, 6 tests carry a stale case-version link, 8 green tests have no
critic verdict recorded, 6 dead duplicate rows reached the ledger, one row "TC-014
blocked_by_env" is stale. That is why the machine ledger reads "verified 0" while the
runner counted 18 green. Recorded in the factory backlog as FB-1…FB-4.

## Size

Forecast: **L** (the formula gave XL: 2 × 12 × risk > 18; set to L because the UI checks
share one popup fixture).
Fact: **L** — 14 testable requirements, 15 plan rows, 15 cases, within the L cap of 18.
No re-estimation during the story.

## Where to look

- understanding.md — what we verify and why (R-1…R-15), what we do not verify and why
- test-plan.md — the 15 plan rows, priorities, why automated, the gate A questions, the
  regression commands, the case texts
- retro.md — time per stage, what went wrong and what to change
- the appendix below — every requirement, case and test with its result

## Appendix — traceability

Sorted by requirement, then by case. Result vocabulary: **pass** · **BUG-n** · **wait**
(the case is handed to a person) · **blocked** (the stand) · **not run** · **unreachable**
(the scenario cannot occur in the product) · **deferred** (a recorded decision) ·
**not planned**. Level: api · component · e2e-ui · manual-agent · manual-human. Shape: new ·
extend · reuse · parameterize · consolidate.

Test files: **V** = `tests/ui/workflows/test_workflow_visual_diff.py`,
**H** = `tests/ui/workflows/test_workflow_version_history.py`,
**E** = `tests/ui/workflows/test_edit_workflow.py`,
**S** = `tests/ui/workflows/test_workflow_restore.py`,
**A** = `tests/workflow/test_workflow_validate_api.py`,
**W** = `tests/workflow/test_workflow_version_history.py`.

| R | What we verify | TC · Then | Test | Level · shape | Result | Basis |
|:--|:--|:--|:--|:--|:--|:--|
| R-1 | button opens the visual popup; YAML diff separate | TC-001<br>Then 1–3 | H `..button_accessible_`<br>`from_visual_editor` | e2e-ui<br>extend | **pass** | critic review, red probe |
| R-2 | one graph, one set of zoom / fit / pan | TC-002<br>Then 1–4 | V `..single_graph_and_`<br>`working_controls` | e2e-ui<br>new | **pass** | review not recorded |
| R-3 | added node: green border, only it | TC-003<br>Then 1–3 | V `..marks_only_the_`<br>`added_node` | e2e-ui<br>new | **BUG-2** | second ADDED badge |
| R-4 | removed node: red border, badge, former position | TC-004<br>Then 1–5 | V `..removed_node_kept_`<br>`visible..` | e2e-ui<br>new | **BUG-1** | position discarded on re-render |
| R-5 | modified node: amber border, values hidden | TC-005<br>Then 1–3 | V `..modified_node_hides_`<br>`changed_values` | e2e-ui<br>new | **pass** | critic review, red probe |
| R-6 | visual diff is read-only | TC-006<br>Then 1–2 | V `..is_read_only` | e2e-ui<br>new | **blocked** | stand: fails 4 of 4 before its checks; no decision |
| R-7 | markers follow the selected pair of revisions | TC-007<br>Then 1–3 | V `..follow_the_`<br>`selected_pair..` [3 variants] | e2e-ui<br>parameterize | **pass** | review not recorded |
| R-8 | text diff still present alongside | TC-008<br>Then 1–2 | E `..yaml_editor_`<br>`functionality_with_history` | e2e-ui<br>extend | **blocked** | stand: fails 7 of 7; no decision |
| R-9 | restore of an invalid revision: issues inline, nothing saved | TC-010 | — | — | **unreachable** | the platform validates before any write; needs "accept" |
| R-9 | restore of a valid revision: no issues, nothing saved, both popups | TC-011<br>Then 1–4 | S `..no_issues_and_`<br>`persists_nothing` [yaml, visual] | e2e-ui<br>parameterize | **pass** | review not recorded |
| R-10 | validate = PUT: valid config, warning | TC-012<br>Then 1–2 | A `..valid_config_`<br>`returns_200..`, `..warns_on_`<br>`unpinned..` | api<br>new | **pass** | review not recorded |
| R-10 | validate = PUT: missing assistant, broken graph, autonomous | TC-012<br>Then 1, 3, 4 | A `..outcome_`<br>`per_partition` [3 variants] | api<br>parameterize | **pass** | review not recorded |
| R-10 | validate = PUT: workflow references itself | TC-012<br>Then 5 | A `..outcome_`<br>`per_partition` [self-reference] | api<br>parameterize | **BUG-4** | message omits the input |
| R-10 | validate = PUT: unavailable guardrail | TC-012<br>guardrail variant | not written | api<br>parameterize | **wait** | decision S5-160: run where the AWS keys are |
| R-10 | validate = PUT: unavailable MCP server | TC-012<br>MCP variant | — | — | **deferred** | designer: no MCP access contract |
| R-11 | validate changes neither the workflow nor its versions | TC-013<br>Then 1–3 | A `..persists_nothing` | api<br>new | **pass** | critic review, red probe |
| R-11 | validate changes no guardrail assignments | TC-013<br>Then 4 | not in the test | api<br>extend | **wait** | same keys; add a before/after read |
| R-12 | validate answers 403 / 404 / 400 like PUT | TC-014<br>Then 1–4 | A `..deleted..`,<br>`..malformed..`,<br>`..by_non_owner..` | api<br>new | **pass**, Then 1 → **BUG-3** | critic review, red probe; 404 body not null |
| R-13 | versioning and text diff not regressed | TC-008<br>Then 3 | E `..yaml_editor_`<br>`functionality_with_history` | e2e-ui<br>extend | **blocked** | same as R-8 |
| R-13 | versioning and text diff not regressed | TC-009<br>Then 1–3 | W 3 existing tests | api<br>reuse | **pass**, Then 2 → **BUG-3** | 404 body: `details` / `help` not null |
| R-14 | a read-only user cannot Restore | TC-015 | manual, person, preview | manual-human | **not run** | no read-only account; defect suspected (MR 1881) |
| R-15 | removed node without layout meta | — | — | — | **deferred** | gate A, Q3: awaits the owner's answer |
