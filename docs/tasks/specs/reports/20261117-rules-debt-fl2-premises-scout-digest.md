# FL2 premises L-2..L-7 — scout digest t-1067 (accepted by trail, Lead 17.11.2026) and PL-1

Package root P = `ai-packages/qa-factory`. Lines are of main `509722e0`. Spot-checked by the Lead: the single call site of
`check_plan_v0` and the negative "no `validate_artifacts` in `branch_accounting.py`" (positive control: `planning_contract.py` hits).

## L-2 — readers of the md `## Plan` table
- The table is parsed ONLY through `contract.md_table(text, "## Plan")` by header NAME. `contract.parse_plan` (`contract.py:2882-2904`)
  maps header -> key through `PLAN_COLUMNS` (`:2744-2760`, 12 keys; `PLAN_REQUIRED_COLUMNS = (ts, r, observable, disposition_cell, fit)`)
  with `mapping = {i: PLAN_COLUMNS[h] ... if h in PLAN_COLUMNS}` (`:2890`): an unknown header is silently ignored, never refused.
- `md_table` (`contract.py:2846-2867`): raw cell lists, no column count, no header whitelist.
- `validate_artifacts.check_cell_counts` (`:250-265`, called `:1862`) -> `C.excess_cell_rows` (`contract.py:1411-1419`): width = len(header);
  refuses only a NON-EMPTY cell beyond the header width. A new column in the header (empty or filled cells) and old plans without it: no effect.
- `check_plan_v0` (`validate_artifacts.py:1850-1937`): reads hypothesis, disposition (`C.DISPOSITIONS`, reason), observable, oracle, level, fit.
- `planning_contract._rerender_plan_cells` (`:2451-2531`): finds columns only via `MD_COLUMN_OF_KEY` (disposition_cell, level, fit,
  question_rename) by `header.index(name)`; rewrites only touched cells and re-joins the row from its OWN cells (`:2527`) — it does NOT
  re-render from a fixed column list and does NOT drop an unknown column; a short row is guarded (`:2502-2511`).
- `planning_contract.register_fence` (`:3944-3945`) reads only the R column. Gate A (`gate_brief.GATE_A_DOCUMENTS`, `:1919`) lists the md by
  name (the body around `:1919-1950` was not read). `render_case_appendix.embed` does not read the table. `plan_row.py` works on the JSON only.
- Other `parse_plan` callers read rows by key (call lines read, bodies not opened): `check_delivery.py:410,731,1342`,
  `check_traceability.py:200`, `traceability.py:451,1790`, `ledger.py:1575`, `report_facts.py:274,1381`, `stand_gaps.py:132`,
  `factory_dashboard.py:714`, `contract.py:2095`, `validate_artifacts.py:2115,2166`.

## L-3 — where `check_plan_v0` runs
ONE call site: `validate_artifacts.py:2670`, inside `collect_errors(path)` on `target.endswith("test-plan.md")` with `C.plan_is_v0(path)`.
Reached from the CLI (`:2747 --check`) and the PostToolUse hook (`hooks/hooks.json:66-74`, matcher `Write|Edit`; `hooks/codex.json:31-32`).
It runs when `test-plan.md` is written or edited, NOT on the S3 exit path: `references/stages.json` S3 `detectors` are
`planning_contract.py`, `branch_accounting.py` (`:128-133`); `planning_contract` does not import `validate_artifacts`;
`exit_gate.collect_errors` (`exit_gate.py:1318-1362`) has no test-plan.md check. Scope of the negative: `scripts/*.py` and `hooks/`.

## L-4 — test files
- `test_third_verdict.py`: `keep`, layer `detector` (`test-layers.json:6514-6535`), slow 39.7 s (`scripts/slow_tests.json:158`).
- `test_case_gates.py`: QUARANTINED (`test-layers.json:7477-7484`, cohort 8073673), no keep row, not in the slow list. The §3.4 card
  owns it and adds rows to it — that cannot stand (docs/TESTING.md: no new rows in a quarantined file).

## L-5 — md vs JSON parity
The only comparison is `planning_contract.requirements_without_row` (`:518-542`, refusal `fence.r_column` `:3980-3984`): the SET of register
ids (JSON rows vs the md R column). Nothing compares rows by TS id, `disposition` or the column set. `_rerender_plan_cells` is a one-way
JSON -> md sync for `disposition_cell`, `level`, `fit`, `question_rename`.

## L-6 — texts that tell a role how to write a skip row
None names the columns of a skip row. The same sentence ("`disposition: skip` with the reason") lives in four places:
`driver_dispatch.py:2587-2591` (`S3_FENCE_LINE`, the strategist's S3 dispatch text), `planning_contract.py:3969-3978` (refusal
`fence.plan_row`), `skills/qa-story/phases/s3.md:141` (the card's `references/s3.md` does not exist), `handoffs/s3-strategist-to-designer.yaml:70-73`.
The md column list is `references/artifact-contract-plan.md:44-57` (`disposition + reason` at `:54`; `:90` the exclusion line) with a
generated copy `references/slices/qa-test-strategist/artifact-contract-plan.md:23,59`. The charter `agents/qa-test-strategist.md` has no
skip line (`:74` points to the plan contract). Other mentions: `references/vocabularies.md:9`, `references/automation-candidacy.md:23`,
`references/templates/plan-brief.md:13,16`, `handoffs/vocabulary.yaml:87`, `handoffs/s2-tester-to-strategist.yaml:111,116`,
`references/artifact-contract-results.md:36`, `templates/test-report.md:130-135` (list possibly incomplete: the scout's search hit its limit).

## L-7 — PL-1 (run by the Lead on main `509722e0`)
`{'automate': 48, 'manual-agent': 7, 'skip': 2, 'unverifiable': 1}` over `fixtures/stories/*/work/test-plan.json`; both `skip` rows are in
`local-1-0108` (a cosmetic check; the R3 row "the owner's answer leaves no implemented quick-view add path to verify"). R3 class count: 1.
