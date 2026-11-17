# FV3-19 card: the empty outcome of a nested list (`probes.records`) — DRAFT

designer t-1211 · node `live-run-fvf/3/FV3-19` · finding `plans/piles/live-run-fvf/findings/20261117-p1b-probes-records-bez-pustogo-ishoda.md`
Status: draft for Lead acceptance, then a plan critic (PROJECT.md package p.6: the meaning of "an empty list" changes). Forks: §4.

## 1. AR-n, owners, census

| AR | how this card touches it | change check written into the DoD |
|---|---|---|
| AR-23 | which lists are "required" and where their empty outcome lives | REQUIRED_LISTS stays `("scope",)`; `null_outcomes.audit` over the real index stays green (existing row `test_handoff.py::the_null_outcome_audit_is_green_over_the_index_with_the_purpose_rows`) |
| AR-22 | the critic is told where the empty outcome lives (yaml comment its slice is generated from) | the yaml comment and `contract_slices.py` output change in one commit; `test_contract_slices.py` in the witness |
| AR-28 | an untouched list must never become a pass the gate did not mean | rows R3, R5, R6 below (a started row, a row inside a list row and a non-list value are still refused or unchanged) |
| AR-15 / AR-13 | `handoff_check._is_empty_section` is a twin of `handoff.only_template` ("the one reader of an untouched template row") | the twin calls the survivor; R1-R4 pin both callers |
| AR-29 | one check altered, none added (recommended road B) | below; `test_judgment_census.py` in the witness; no census count may rise |

Checks the recommended road alters (P27, AR-29): (1) `handoff_check.check` — which list paths count as empty before the blank-field loop: class **shape**, owner **data** (presence of a value at a path; never reads what a row says). (2) `handoff.only_template` gains the template-token rule (F4-b): class **shape**, owner **data**. No new refusal, no new blocking unit. Road A (F1) would add a refusing unit of class **xref** (owner data) for `qa-code-critic` — a raise of "blocking units per role", named in the verdict (AR-20).
Commit lines: the `architecture:` and `judgment:` lines in the form only `tools/architecture_gate.py` carries (do not copy it from here); a `judgment: none` always carries its ` -- <why>`.
Key form and AR-1 (asked by the Lead): the declarations are data (contract yaml `null_outcome:`; `references/null-outcomes.json` holds only `never_empty`/`pending`/`tightening_exceptions`/`ratchet` rows — read whole, no key grammar there). The KEY GRAMMAR is code: `handoff.REQUIRED_LISTS` + `handoff.null_outcome_entries` (`section not in REQUIRED_LISTS` → dropped), mirrored by `null_outcomes.entry_problems` and the audit walk W1 (`null_outcomes.py:566`). A schema grammar is not project variety, so AR-1 is not breached by it staying in code; neither road adds a list of names to code (road A would enumerate nested lists from the contracts, never list them).

## 2. Measurement (step 1 of the finding)

M1 — required nested lists in the contracts. Grep tool, multiline: pattern `^ +[A-Za-z_]+:[ \t]*(#[^\n]*)?\n( *#[^\n]*\n)* *- `, path `ai-packages/qa-factory/handoffs`, glob `*.yaml`. Count mode: `Found 66 total occurrences across 22 files.` Of these, 44 are the `tried:`/`data:` pairs under `blocked:` (22 files × 2; `blocked.*` blanks are never refused, `handoff_check.py:1750`). The other 22, first line of each match verbatim (the second line is the `- ` item):
```
gate-a-to-automator.yaml:53:  preconditions_accepted_as_blocked:
gate-b-to-delivery.yaml:71:  commits:
gate-b-to-delivery.yaml:81:  do_not_commit:
s8-scribe-to-gate-b.yaml:67:  witness_paths:
s2-tester-to-strategist.yaml:87:    readings:
s7-automator-to-analyst.yaml:53:    changed:
s1-scout-to-tester.yaml:78:  accepted_gaps:
s1-scout-to-tester.yaml:81:  late_sources:
role-to-conductor.yaml:56:  options:
s7-analyst-to-scribe.yaml:58:  witness_paths:
s5-critic-to-automator.yaml:56:  records:
s4-case-critic-to-designer.yaml:116:  witness_paths:
s4-case-critic-to-designer.yaml:132:    read:
s4-case-critic-to-designer.yaml:135:    options:
s4-case-critic-to-designer.yaml:148:    refs:
s7-analyst-to-automator.yaml:93:  witness_paths:
s4-designer-to-runner.yaml:57:    preconditions:
s4-designer-to-runner.yaml:59:    data_and_accounts:
s5-automator-to-runner.yaml:80:  tests:
s4-designer-to-case-critic.yaml:66:  focus:
s5-automator-to-critic.yaml:61:  tests:
s5-automator-to-critic.yaml:64:  probes:
```
Positive controls (same tool): (i) the same pattern finds the known nested list `s5-critic-to-automator.yaml:56: records:`; (ii) Grep `^null_outcome:` over the same glob → `s7-analyst-to-automator.yaml:41:null_outcome:` followed by `  scope:` / `    condition: triage_has_no_repair` — the one declaration, top-level. Limit: a list after a blank line under its key is not matched.

Classification (read from each contract with `-B2 -A3` context; hint words per `handoff.OPTIONAL_WORDS`):

| class | lists | today |
|---|---|---|
| N-map, required (list in a top-level map, a row field with no optional word) — 9 lists, 8 contracts | `probes.records` (s5-critic); `environment.preconditions_accepted_as_blocked` (gate-a, kind decision); `delivery.do_not_commit` (gate-b, decision); `person.accepted_gaps`, `person.late_sources` (s1); `review_scope.focus` (s4-designer-to-case-critic); `artifacts.tests` (s5-automator-to-critic, s5-automator-to-runner); `person_question.options` (role-to-conductor, index kind `help`, not a `handoffs:` row) | an untouched template row is refused field by field (`field.blank`) — every one is de facto required, none is walked by `null_outcomes.audit`, none has a home |
| N-map, empty declared by hint | `artifacts.probes` ("or the empty list"); `witness_paths` ×4 ("or omit") | optional, passes |
| N-map, contract-filled | `delivery.commits` (literal values) | never blank |
| N-row (list inside a list row) | `readings`, `rounds[].changed`, `questions[].read`, `questions[].options`, `gaps[].refs` (optional), `execution[].preconditions`, `execution[].data_and_accounts` | governed by the parent row: an untouched parent row is skipped whole |

M2 — the product road for the critic (read, not run; R1/R9 pin it before the edit):
- `handoff.py:456-459`: only `scope` is refused empty; "Every other list may legitimately be empty". `handoff_check.check` (`:1655-1670`) applies that to TOP-LEVEL list sections only (`handoff.sections` is top-level, `:673`); the blank-field loop (`:1708-1755`) skips a path only when its TOP-LEVEL section is an empty list (`:1709`). `probes` is a map, so `probes.records[0].instance`/`.verdict` left as template are refused `field.blank`.
- The values writer cannot write the empty list: `apply_values` → `_apply_one` (`:2731`) notes "a placeholder or an empty value is not a word - nothing written" for `probes.records: []`.
- So the critic has NO legal empty `probes.records`. Real-run evidence: `scripts/tests/fixtures/stories/cart-1/work/handoffs/S5-qa-code-critic-7.values.applied.yaml:9-12` — the role invented `record: work/probes/none.json` with `not_executed`; five other cart-1 critic forms (`-2..-6`) and TP1-12586 `S5-qa-code-critic-4.yaml` carry the unfilled token `record: work/probes/<instance>.json`.
- The role's rule already names the empty outcome: `agents/qa-code-critic.md:23` "proved by a live probe, or marked `unverified` with why. Witness: `probes.records[]`, `unverified[]`"; downstream guard: `controller.py::_code_review_refusal` (`controller:code_review_receipts`: each new or changed test carries a sensitivity proof or a reason; slice text `references/slices/qa-code-critic/handoff-keys.md:81`; `_code_review_problems` body not read).
- `_is_empty_section` cannot see `probes.records` as untouched even with a path: the template row holds `record: work/probes/<instance>.json`, which `handoff.PLACEHOLDER` (`^<(.+)>$`) does not match (F4).

M3 — two facts of the finding corrected (the card relies on the reads, not on the finding):
- The quoted refusal text is the dry-world filler's, a test helper: `scripts/tests/form_filler.py::_spread_world_rows` (`:481-482`), pinned by the QUARANTINED `test_form_selftest.py:88` (test-layers.json `quarantine`, line 8337). `handoff_check` never prints it.
- `handoff_check.py::_probe_list` derives `artifacts.probes` of `s5-automator-to-critic` (`LIST_DERIVERS`/`DERIVERS`, `:718`, `:737`), not the critic's `probes.records`; its hint already declares the empty list. It stays unchanged.

## 3. The class and the meaning change

Class (P31, AR-23): **the rule "every list but `scope` may be empty; an untouched template row is the empty list" holds only at the top level; a list nested in a map is refused field by field, so it is silently required, unwalked and homeless.** Nine lists in eight contracts, the S5 critic's `probes.records` among them.
Meaning change (PROJECT.md p.6, for the plan critic): under road B, "an untouched list" means the same at every depth that crosses no list row; the nine map-nested lists stop being de facto required. Under road A, the `null_outcome` key grammar admits a dotted path and the walk grows.

## 4. Forks (the Lead decides; the node below is written for the recommendations)

- **F1 — the road.** (B, recommended) One rule for every list whose path crosses no list row: untouched → empty → legal unless in REQUIRED_LISTS. No schema grammar change, no new refusal, no census raise; the coverage obligation stays with its existing owner (`controller:code_review_receipts`), so no second judge of one fact (AR-15). Cost: the nine N-map lists become empty-legal (F3). (A, the finding's item 2) Dotted `null_outcome` keys (`probes.records`) + a new live condition (e.g. `rows_listed_in`: every `scope[].id` is an `unverified[].id`) + `null_outcomes.audit` walks map-nested required lists, each needing a home in the same commit (the `pending` ratchet forbids new pending rows). Cost: `handoff.py`, `handoff_check.py`, `null_outcomes.py`, `null-outcomes.json`, the s5 yaml plus up to 7 sibling yamls, a new refusal code with its rows in `references/stage-joints.json`, `fixtures/driver-exits/gates.json` (axis 38), `test_detector_verdict.py` fingerprints, `test_contract_slices.py:1124`, slices; and the unconditional-empty siblings have no registered condition to name. A's edges, answered: a top-level key keeps today's meaning (scope + `triage_has_no_repair` byte-identical); a dotted key whose section is absent, whose target is a scalar/map, with an empty segment (`probes.`, `.records`, `probes..records`), an index (`probes.records[]`) or depth > 2 is dropped by the pure reader and red in `audit` with the key named (fail closed, as today's malformed entries); on a NON-empty list the declaration is not applied and the rows are checked as rows.
- **F2 — depth.** (a, recommended) Lists whose path crosses no list row (top level, and lists in maps at any depth). (b) every list at any depth: loosens N-row lists that must not be empty (`questions[].options`, FR-50; `readings`).
- **F3 — sibling verdicts under B** (recommended: accept all; each is a legitimate empty): `preconditions_accepted_as_blocked` (the person accepted none), `do_not_commit` (named none), `accepted_gaps`/`late_sources` (none), `focus` (nothing weak), `probes.records` (no probe ran: `unverified` rows). One risk, priced: `artifacts.tests` on the two S5 automator forms — a plain (non `--fix`) check stops refusing an untouched list; `--fix` still derives it first (`LIST_DERIVERS` runs before the empty verdict, `:1627-1635`), and an empty window is legal (null-outcomes.json NE3, "E41"). Alternative: opt it into REQUIRED_LISTS by path (re-opens the grammar of F1-A). `person_question.options` (kind `help`): whether `handoff_check` ever checks that form is item 0's measurement; if it does, the Lead decides required/empty.
- **F4 — the token literal in the records template row.** (b, recommended) `handoff.only_template` counts a leaf that contains a `<…>` token AND equals the template's leaf at the same generic path as untouched; `_is_empty_section` calls it (AR-15). (a) make `record` a placeholder in the yaml — rejected: the filler's world-list token would leave a still-bracketed value (dry_stub N2h breaks) and old forms keep the literal anyway. (c) leave it: road B then never fires on `probes.records` — the defect stays.
- **F5 — the quarantined pin.** `test_form_selftest.py:88` pins the old filler text at `probes.records`. (a, recommended) change the filler; the quarantine watcher goes red and the Lead runs `tools/test_quarantine.py judge` (builder never touches a quarantine file). (b) leave the filler's text: it then says "declares no empty outcome" about a list that has one (FR-37).

## 5. Builder node FV3-19 (road B, F2-a, F3 accept, F4-b, F5-a)

given: `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-fv3-19-nested-null-outcome-card.md` (this card, §2 measurement), `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md` (whole), `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/architecture.md` (AR-15, AR-22, AR-23, AR-28, AR-29), `C:/QAFactory/forge-repo/docs/TESTING.md`
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/handoff.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/handoff_check.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/handoffs/s5-critic-to-automator.yaml
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/slices/qa-code-critic/handoff-keys.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/form_filler.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/form-rounds.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_handoff.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/changelog.d/fv3-19-nested-list-empty.md
non-goals: the `null_outcome` key grammar, `null_outcomes.py`, `references/null-outcomes.json` (road A only); sibling yamls; `handoff_init.empty_optional_lists` (top-level skeleton emptying stays); `controller.py`; any quarantine file (`test_form_selftest.py`); the finding file
handoff: the builder report (rule 7 `.claude/agents/builder.md`) with the FR walk (A, C, D, E applicable; B: the yaml comment is role text) and the witness output
edges: §6
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/handoff.py ai-packages/qa-factory/scripts/handoff_check.py ai-packages/qa-factory/handoffs/s5-critic-to-automator.yaml ai-packages/qa-factory/scripts/tests/form_filler.py` — then every file it prints (expected among them `test_handoff.py`, `test_null_outcomes.py`, `test_field_producers.py`, `test_contract_slices.py`, the scenario files; estimate, not verified) green, and `test_judgment_census.py` with no count raised
siblings: axis 5 — the nine N-map lists of §2 (verdicts F3; no yaml edit needed under B); axis 18 — no ratchet raised; axis 34 — one rule for every depth; axis 38 — no new joint (road B adds no refusal)

Items (each with its row in ONE new parameterised function of `test_handoff.py`, `an_untouched_list_is_empty_at_every_depth_that_crosses_no_row`; a new case is a table row, no new file):
0. Measure before editing (report section, not code): run R1 and R9 on the unedited tree (both must fail as §2 says, FR-32); Grep the templates for top-level list rows whose non-placeholder leaves all carry a `<…>` token (F4-b also changes those) and list each with its verdict before/after; say whether `handoff_check` ever runs on a `role-to-conductor` form (F3). A verdict change outside §6 stops the node and goes back as a question.
1. `handoff.py`: one reader `list_paths(contract) -> {path: ...}` of every list path in the template that crosses no list row (top-level lists included; `CONTRACT_OWNED` and `blocked` excluded), built from the template like `sections()`; `only_template(value, template=None)` with the F4-b rule; the comment at `:456-459` says the rule holds at every such depth. Rows R1, R7.
2. `handoff_check.py`: `_is_empty_section` takes a dotted path (read through `doc.data` walking maps; an absent key or a non-list stays "empty" exactly as today for top-level) and calls `handoff.only_template` with the template row (the twin retired, AR-15); `check` builds `empty_sections` over `handoff.list_paths(contract)` instead of top-level list sections, keeps the REQUIRED_LISTS refusal for `scope` only, and the blank-field loop skips a path under ANY empty list path (prefix `<path>[`). Rows R1-R6, R8.
3. `s5-critic-to-automator.yaml`: comment over `records:` — "No probe ran, or the window has no new or changed test: leave `records` as it stands (the empty list) and give each such instance its `unverified` row." Regenerate the critic slice with `contract_slices.py` (comment-only: the keys list may not change; say so). Row R9.
4. `form_filler.py::_spread_world_rows`: no file + a list path that is not in REQUIRED_LISTS → leave the list untouched (no `Unfillable`); for `scope` keep the refusal with a text that names `scope` as the required list. Update `form-rounds.json` only if a listed unfillable row disappears (name it). Row R10.
5. `changelog.d/fv3-19-nested-list-empty.md` (English, no Cyrillic).

Table rows (R = `_critic_form`-based unless named; expected verdicts):
- R1 critic form, `probes.records` untouched, `unverified` has `test_one` → no problem whose path starts with `probes.records` (today: two `field.blank`).
- R2 `probes.records[0]` instance real, verdict placeholder → `field.blank` at `probes.records[0].verdict` (unchanged).
- R3 untouched records row but `note` filled with a real word → not empty → `instance`/`verdict` refused blank.
- R4 `scope` untouched on the critic form → `handoff_check:required_rows` at `scope` (unchanged).
- R5 `s4-designer-to-runner`: `execution[0].case` real, `preconditions` untouched → refusal at `execution[0].preconditions[0]` stays (F2-a boundary).
- R6 top-level `findings` untouched, verdict `ok` → no refusal (unchanged); same with a verdict that owes findings → `required_rows.owed_by_verdict` (unchanged).
- R7 pure `only_template`: `{"record": "work/probes/<instance>.json"}` against the same template leaf → True; `"work/probes/test_x[<lambda>].json"` against a different template leaf → False; `"work/impl-diff.txt"` (no token) → False.
- R8 `s5-automator-to-critic`, plain check, `artifacts.tests` untouched → no refusal (the priced F3 change); with `--fix` and a manifest naming a test → derived (unchanged order).
- R9 values file `probes.records: []` → note "nothing written", then the form passes on R1's terms.
- R10 `form_filler.fill_form("s5-critic-to-automator", ctx)` with no `work/probes/*.json` → no `Unfillable` under `probes.records`; a world-list token in `scope` with no file → `Unfillable` naming `scope`.

## 6. Edges, each with its invariant

- Top-level lists keep every verdict (R4, R6). Invariant: no top-level form changes outcome, except rows item 0 lists for F4-b.
- A started row (any leaf a real value that differs from the template) is never empty (R2, R3). Invariant: a half-filled row is never excused.
- A list inside a list row is never judged by this rule (R5). Invariant: an item's own content stays required with its item.
- An absent key or a non-list value at a list path: "empty", as `_is_empty_section` reads a top-level one today; a role cannot write either through the values file (`_apply_one` refuses an unknown path / writes nothing for `[]`). Invariant: nothing a role can write reaches a pass it cannot reach today at the top level.
- Empty `probes.records` beside a window with unproven tests: the form passes; `controller:code_review_receipts` still refuses the unreceipted window. Invariant: an unproven test never closes the window (the owner of that fact is unchanged).
- `--fix` derivation runs before the empty verdict (positional, `:1627-1635` before `:1655`). Invariant: a list code can fill is never excused as empty.
- `null_outcome` on `scope` (S7) is untouched: `nulled` keys stay top-level; `handoff_init.py:201` and `driver_stage_s7.py:258` read `["scope"]` only. Invariant: S7's null outcome and its refusals keep their fingerprints (`test_detector_verdict.py` unchanged).
- Temporal: forms written before this change keep their literal `record: work/probes/<instance>.json`; under F4-b an untouched row of an old form also reads as empty. Invariant: same verdict for an old and a new untouched form.
Reused function in a gate role: `handoff.only_template` (advice for skeleton emptying and rows-owed → now lifts refusals). May err only toward "not untouched" (stricter). Adversarial inputs that must stay on that side: a token literal that differs from the template's; a parametrised id carrying `<lambda>`; a real word in an optional leaf; `instance: ""` (blank, equals untouched — the same reading top-level lists have); an angle-bracketed word typed by the role (`<intended_failure>` reads as a placeholder — today's rule at the top level, unchanged).

## 7. Readers of every touched file (rule 7)

Greps (Grep tool): `null_outcome|REQUIRED_LISTS|handoff_check|s5-critic-to-automator` over `tools/` → 2 hits; over `.githooks/` → 0 (control `handoff|pre-commit` -i → 3 hits, 2 files); over `.claude/agents/` → 0 (control `handoff` → 10 hits); over `.claude/settings.json` → 0 (control `tools/` → 37). `.claude/worktrees/**` hits are other sessions' checkouts, not readers. Package: `null_outcomes\(|null_outcome_entries\(|REQUIRED_LISTS` over `scripts/` → 44 hits / 13 files; `_is_empty_section|only_template\(` over `scripts/` → 18 hits / 5 files.

| file / name | reader | verdict |
|---|---|---|
| `handoff.only_template` / `_is_empty_section` (one grep, 5 files) | `handoff_init.py` (skeleton emptying), `handoff_check.py` (rows owed, 12 hits incl. `_investigation_view` and the `--fix` loops), `driver_stage_plan.py` (1 hit, which of the two not read), `test_rows_owed.py` | change with items 1-2: stricter-or-equal by R7; item 0 reads the `driver_stage_plan.py` hit and lists any verdict change |
| `handoff.REQUIRED_LISTS` | `handoff_check.py:1661,2400`, `handoff_init.py:203`, `null_outcomes.py` W1, `form_filler.py:370`, `project_decisions.py:45` (comment) | unchanged (value stays `("scope",)`) |
| `handoff.null_outcomes` / `null_outcome_entries` | `handoff_check.py:1554`, `handoff_init.py:201`, `null_outcomes.py:113`, `driver_stage_s7.py:258`, `form_filler.py:370`, tests (`test_null_outcomes`, `test_s7_*`, `test_contract_slices:1121`, `test_detector_verdict:1521`) | unchanged under B (changes in road A only) |
| `s5-critic-to-automator.yaml` | `handoff.template` callers; `contract_slices.py` → critic slice; `form_filler`; `dry_stub.py:1569` (N2h); `test_handoff._critic_form`; `test_handoff_values_main_block.py:58`; cart-1 / TP1-12586 fixtures | comment-only: slice regenerated in item 3, the rest unchanged |
| `form_filler.py` | `test_field_producers.py` (keep), `dry_stub.py`, `test_form_selftest.py` (quarantine) | changes in item 4; quarantine pin: F5 |
| `tools/source-split-carriers.json:16`, `tools/test_dod_gate.py:1254` | name `null-outcomes.json` / `handoff_check` in a test name | unchanged |

## 8. Small choices closed by the designer

`list_paths` as the one reader name; the depth rule expressed as "crosses no list row" (no depth counter); `only_template` takes the template leaf as an optional argument (old callers unchanged); the yaml comment's wording; one parameterised function rather than ten; the changelog fragment name.

## 9. Reading trail

The finding (whole); `handoff.py` 168-262, 380-447, 450-540, 553-598, 638-695; `handoff_check.py` 470-530, 706-745, 1221-1231, 1549-1560, 1599-1790, 2660-2795; `null_outcomes.py` 1-55, 116-175, 540-650; `null-outcomes.json` (whole); `s5-critic-to-automator.yaml` (whole); `handoff_init.py` 180-229; `form_filler.py` 440-492 + grep; `test_handoff.py` grep of defs + 1842-1871; `test-layers.json` keep rows 2301, 3402 and quarantine 8337, key list; `slices/qa-code-critic/handoff-keys.md` (whole); `handoffs/index.yaml` greps; `stage-joints.json` 5612-5629; `architecture.md` 136-157, 226-283; `controller.py` 6545-6597; SIBLING_MAP axis headings; TESTING.md "Что запускать".
Needed beyond the manifest: `null_outcomes.py`, `null-outcomes.json`, `form_filler.py`, `handoff_init.py`, `test-layers.json`, `stage-joints.json`, `controller.py`, `index.yaml`, the critic slice, cart-1 fixtures.

## Lead decisions (Lead, 17.11.2026, Opus; «решила сама», the owner can stop or roll back)

- F1 = (B): one empty-list rule for every list whose path crosses no list row; no `null_outcome` key grammar change (P31, AR-15: the coverage obligation keeps its one owner `controller:code_review_receipts`). The finding's item 2 (dotted keys) is NOT done; the finding's direction is corrected by this card.
- F2 = (a); F3 = accept all six verdicts, and `artifacts.tests` stays empty-legal (the `--fix` deriver runs first; NE3); `person_question.options`: the builder reports item 0's measurement and stops on that one path if `handoff_check` checks the `help` form (a question to the Lead, not a guess).
- F4 = (b); F5 = (a): the Lead runs `tools/test_quarantine.py judge` at acceptance.
- Order: plan critic (PROJECT.md package p.6) before the builder dispatch.

## Lead decisions on the plan verdict t-1215 (Lead, 17.11.2026, Opus; «решила сама»)

Verdict: `docs/tasks/specs/reviews/t-1215-fv3-19-card-plan.md`. These decisions override §2, §5 item 0, §6 edge 1 and the F3 line above where they disagree.

- B1, measurement: the critic's probe3 table (top-level and nested, recursion and F4-b) is the real measurement M4 of §2. Item 0 becomes: re-run that enumeration (walk of the PARSED template, as `list_paths` walks it) and reproduce the closed list below EXACTLY; any other verdict change stops the node (a question to the Lead).
- B1, verdicts per flipped top-level list:
  - `inputs_read` in s4-case-critic-to-designer, s5-automator-to-runner, s6-runner-to-analyst, s7-analyst-to-scribe, s7-automator-to-analyst, s8-bug-reporter-to-scribe: MUST NOT be empty. It joins the required set AS DATA (one NE row each in `null-outcomes.json`, no null outcome), so an untouched row stays refused by the same road as every required list (P31, AR-23, AR-28). The row sentence at `handoff_check.py:1666-1670` gets a form that does not say "in scope" for these lists (the builder writes it from the data row's own text, not a branch on the list name).
  - s7-automator-to-analyst `rounds`: joins the required set with an EXPLICIT null outcome ("no repair round"): untouched stays refused, a role with no repair writes the declared null outcome (FR-23). No conditional rule on `fix_result`.
  - s4-case-critic `findings`, `questions`, `register_gaps`: empty-legal (matches `handoff_init.EMPTIED`).
  - s8-scribe-to-gate-b `questions`: empty-legal (a gate packet with no question is normal).
- B2: M1 grep replaced by the parsed-template walk (above). N-map set = the card's 8 lists minus `person_question.options` (unaffected: the literal `id: a` keeps its row non-empty), plus:
  - s8-scribe-to-gate-b `delivery.reasons_by_owner.{product,person,stand,factory}`: empty-legal (most owners have no reason in one delivery).
  - role-to-conductor `request.tried`, `request.data`: the builder measures first, one command, result in the report: does any non-test package script run `handoff_check` on a role-to-conductor form? If NO (critic's estimate) → no verdict change is observable; one line in the report, no code for them. If YES → `request.tried` joins the required set as NE data (FR-50: the record that every route was tried), `request.data` empty-legal. Both branches are executable; no stop.
- The F3 `person_question.options` stop above is withdrawn (N4).
- N1: signature `_is_empty_section(doc, spec, path, contract=None)`; no contract or no readable template → `only_template(value)` with no template (no token rule: the stricter side). Callers `handoff_check.py:1421`, `:1610`, `:1872` named in the node.
- N2: the filler reads `handoff.list_paths(contract)` minus REQUIRED_LISTS (the checker's reader), not its own depth rule; one R10 row for an N-row path (`execution[].preconditions`).
- N3: §6 edge 4 sentence corrected (a raw `--set probes.records=foo` writes a scalar that reads empty, the same at top level); one R row pins the raw-scalar case at both depths.
- §6 edge 1 now reads: the only top-level verdict changes are the closed list in B1 above; any other change stops the node.
- Re-review: one narrow critic pass on these decisions only (package p.6(б): a spec edit that changes a meaning), then the builder.

## Lead decisions on the re-review t-1219 (Lead, 17.11.2026, Opus; «решила сама»)

Verdict: `docs/tasks/specs/reviews/t-1219-fv3-19-card-rereview.md`. Overrides the `inputs_read` and `rounds` lines of the t-1215 decisions above.

- R1 = (A): one rule by name (P31): `handoff.REQUIRED_LISTS = ("scope", "inputs_read")`. "AS DATA" is withdrawn: the requirement is the tuple. All 15 carriers of `inputs_read` (probe4) get a verdict each; the 14 SCOPE_KINDS carriers get NE homes in `null-outcomes.json` with the guard `handoff_check.py::check refuses the empty list`; W1 tells the item list `scope` from a proof-of-reading list, so kind `report` (`s8-scribe-to-gate-b`) carrying `inputs_read` is legal; the two s5-critic flips (untouched `inputs_read` → refused) and a written `inputs_read: []` → refused join the closed list of verdict changes. The row sentence drops "in scope" for every required list and comes from `row_form` (contract-derived), no new data reader. `null_outcomes.py`, `references/null-outcomes.json`, `test_s7_null_outcome.py` (its pin "REQUIRED_LISTS is unchanged" moves to the new tuple) and `test_null_outcomes.py` move into owns; §7 readers row, §5 siblings line (axis 38: road B now adds the `inputs_read` refusal) and the DoD are rewritten.
- R2 = (a): s7-automator-to-analyst `rounds` is empty-legal like the s4 lists. The priced risk is written in the card: `fix_result: fixed` beside an untouched `rounds` passes until the live condition lands. A finding in `live-run-fvf/findings` opens a node for a live `sibling_in`-style condition over `scope[].fix_result` (road A machinery, its own owns); FV3-19 does not wait for it.
- The card goes to the designer for r2 (resubmission of t-1211): every Lead decision folded into §2, §5, §6, §7 so a weaker model reads one body, not override sections.
