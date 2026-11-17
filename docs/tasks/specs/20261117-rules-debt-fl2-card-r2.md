# FL2, round 2: a skip because the product lacks the surface blocks delivery (FR-21). Builder card (t-1068, F19)

Designer draft for the Lead, task t-1068. This is a NEW file, as the brief asked. The old card is
`docs/tasks/specs/20261117-rules-debt-phase2-s9-fl-cards-spec.md` §3.4. It was not edited.

Inputs: that spec's §1, §3, §4 and "Lead decisions on FL2" (F-L2-A (a), F-L2-B (c)), and the scout digest
`docs/tasks/specs/reports/20261117-rules-debt-fl2-premises-scout-digest.md` (L-2..L-7, main `509722e0`). I re-read
every line that an edge rests on, in the root checkout (branch `main`, head `20b1ea4f` by the session git status; not
re-measured: this designer has no shell). Each fact below is marked **[read]** (I read it this round) or **[digest]**
(quoted from t-1067). **No command was run.**

---

## 0. Read this first: the brief's premise is contradicted by a live road (fork F-R2-1, blocks dispatch)

FL2 starts from the premise that nothing asks whether a skip happened because the product has no such surface: the
debt row says "nothing asks whether a row was skipped because the product has no such surface"
(`design/factory-rules-debt.md:23` [read]), and §3.2 of the old spec says the only existing road is the manifest's
`pending_implementation`. **This round found a second existing road that already covers FR-21 for this very row.**
It is D1-C2, the person's "product gap" word:

- `gate_preflight.check_case_environment_gaps` (`scripts/gate_preflight.py:2269-2333` [read]) walks EVERY row of
  `work/test-plan.json`, whatever its disposition. A row whose `coverage_obligations[]` carries an `unresolved` part or
  an `observation_contract.surfaces[].status == "gap"` is put to the person at gate A. When the row names a
  requirement, the person is also offered the door `` `<id>: product gap` (the product has no such function) ``
  (`:2327-2330`).
- The word is recorded by the one writer `product_gaps.py` (`scripts/product_gaps.py:1-6` [read]; the driver's road is
  `driver_machine.py:2944-2953` [read]). It is read by `check_delivery.product_gap_records` (`check_delivery.py:1829-1841`
  [read]) as kind `product_gap`, which maps to `no`, owner product (`references/delivery-verdict-kinds.json:39` [read];
  the docstring says "FR-21").
- The report already handles it: `report_facts._skipped_by_plan` and `_not_proven` leave a recorded product gap out of
  "Skipped by the plan" (`report_facts.py:2905-2918`, `:2930-2941` [read]), so the report never says "deferred by your
  decision" about a requirement the product does not implement.
- **The FL2 example row reaches that door.** The R3 row TS-23 of `local-1-0108` carries
  `observation_contract.surfaces: [{"id": "S-1", "boundary": "quick view", "status": "gap", ...}]` and
  `remaining_gap: "no implementation or observable"` (`fixtures/stories/local-1-0108/work/test-plan.json:2812-2819`,
  `:2837` [read]), next to `"disposition": "skip"` (`:2785` [read]). The D1-C2 test even uses TS-23 / R-23 as its
  example (`scripts/tests/test_d1_product_gap.py:16-17`, `:356` [read]). That test file is QUARANTINED
  (`test-layers.json:7894` [read]), but the code is live.

So the card as decided (F-L2-A (a), F-L2-B (c)) gives one action ("this skip is a product gap, so delivery reads
`no`") a SECOND road beside D1-C2. The new road has a different owner (the strategist's judgment instead of the
person's word), a different kind (`pending_implementation` instead of `product_gap`) and a different report reader.
Designer rule 6 (P31, axis 34) makes that a spec defect whatever the reason, so it goes back as **F-R2-1** (§9) with
the one-road option recommended. The card in §3 is still drafted whole on F-L2-A/B, so it can be dispatched at once if
the Lead (or the owner) keeps FL2 as a second road on purpose. The plan critic then needs the §3 card and the
paragraph in §8 together.

---

## 1. Architecture, rules, owners (designer rule 1). Valid for the §3 card, the "keep FL2" branch of F-R2-1

FR sections the card touches: C (FR-12: the reason text is never parsed; FR-13: the closed value lives in one constant;
FR-38: the requirement reaches the strategist before the work), D (FR-59), E (FR-21; FR-35: no role verdict is
rewritten; FR-10 through the report reader, item 5), G (FR-29, FR-30: test strings with non-ASCII look-alikes are
written as `\u` escapes in Python source, never as raw bytes and never through a heredoc).

| AR-n | how the card keeps it | change check written into the DoD |
|---|---|---|
| AR-1 | the closed set is ONE constant tuple `contract.SKIP_CLASSES = (PENDING_IMPLEMENTATION,)` beside `DISPOSITIONS` (`contract.py:67` [read]), built on the existing `PENDING_IMPLEMENTATION` constant (`contract.py:83` [read]). It is not a second literal list in `validate_artifacts` or `ledger`. Precedent: `DISPOSITIONS` is a code tuple read by the same check. | Grep `pending_implementation` over the diff of `validate_artifacts.py` and `ledger.py`: no new string literal; both read `C.SKIP_CLASSES` / `C.PENDING_IMPLEMENTATION` |
| AR-10 | the strategist is told in the field list it already reads: one row of the `## Plan` column table of `references/artifact-contract-plan.md` (`:44-57` [read]) and its generated slice (the only role injected with it: `references/inject-map.json:42` [read]) | the DOC key run of item 6, and `contract_slices.py --check` exits 0 |
| AR-13 | the class is read from the md row through `contract.parse_plan` only (`contract.py:2882-2904` [read]). The ledger reads `row["skip_class"]` from the row it already holds (`ledger.py:1575`, `:1593` [read]). There is no second plan reader and no JSON join (F-L2-B (c)). | Grep `skip_class` over `scripts/*.py`: hits only in `contract.py` (the key), `validate_artifacts.py` (the check), `ledger.py` (the read), `report_facts.py` (item 5) |
| AR-20 | if the plan contract row raises the strategist's measured load over `process_ratchet_tokens.qa-test-strategist` (17629, slack 0, `references/role-load.json:24-27` [read]), the raise is named (F-R2-4) and never silent | the builder's report carries the `role_load.py` before/after numbers; the commit's `judgment:`/body names the raise if one is made |
| AR-22 | producer: the S3 strategist writes the cell. Readers: `check_plan_v0` (shape), `ledger.plan_row_state` (state), `report_facts` (where the requirement is listed, item 5). All change in ONE commit. A plan with no column, or an empty cell, reads as absent at every reader. | the item tests 2-5 run in one witness |
| AR-27 | the delivery reason keeps owner `product` (the existing `pending_implementation` kind, `delivery-verdict-kinds.json:44`, `:97` [read]). The report does not file the requirement under "Skipped by the plan" (item 5, FR-10). | item 5 test row |
| AR-28 | every unknown reads as TODAY (`skipped:<reason>`, kind `planned_skip`): no column, an empty cell, a value outside the set, a class on a non-skip row. An unknown value is never read as `pending_implementation`, and never as a pass that today would refuse (§4). | the item 3 table rows "unknown -> skipped" |
| AR-15 / P31 | **NOT kept by the card as decided**: D1-C2 already carries the same action (§0). The card adds a second road. | fork F-R2-1; nothing in the DoD can keep it |

**Checks added or altered (AR-29; census `scripts/tests/fixtures/judgment-census.json`).**

| check | owner it serves | census class | blocking |
|---|---|---|---|
| `validate_artifacts.check_plan_v0` gains three rules: the `skip class` value is in `C.SKIP_CLASSES`; a class only on a `skip` row; the echo of a bad value is capped (item 2) | data (code judges the cell's shape: a closed value, and its join to the same row's disposition). The WORD is the strategist's judgment, accepted at gate A by the person, who reads the column in the plan (`gate_brief.GATE_A_DOCUMENTS` lists the md [digest L-2]) | **shape, unchanged**. The row exists at `judgment-census.json:1211` [read] (`check_plan_v0`, `shape`, owner data), and the same function already holds closed-value rules of the same kind under `shape` (disposition `:1894-1897`, level `:1914-1918` [read]). `CLASS_ORDER` puts `shape` lowest (`test_judgment_census.py:79` [read]). A same-row join is shape, not xref (xref joins two artifacts). No row is added and none changes. The builder confirms by re-reading `:1211` and reports "check_plan_v0 stays shape" | refuses the write (the PostToolUse hook, FR-1) |
| `ledger.plan_row_state` skip branch (item 3) | data (it maps a closed value to an existing state word; no judgment) | not a census unit: the name is outside `UNIT_NAME_RE` and the branch adds no refusal site (`test_judgment_census.py:16-33` per the old spec §1 [digest of t-1034]; the builder checks with the census test, which is in the witness). No row | adds a `no` reason to delivery, never a refusal |
| `report_facts._plan_decision` / `_skipped_by_plan` (item 5) | data | not a census unit (names outside `UNIT_NAME_RE`). No row | none (it decides which block lists an item) |

Commit lines. The form is `tools/architecture_gate.py`'s; this card points to it and does not copy the grammar.
Content: `architecture: AR-1, AR-10, AR-13, AR-20, AR-22, AR-27, AR-28 -- <how kept, from the table>`. Also a
`judgment:` line in the gate's own form, naming the ALTERED check `check_plan_v0` (shape, class unchanged).
`judgment: none` is not legal here, because a check is altered. The axis block of rule 10 (b) is the builder's commit
duty only if the Lead counts the change as a mechanism; the plan contract row is a role duty, so treat it as one.

---

## 2. Facts the card rests on (file:line)

| # | fact | carrier |
|---|---|---|
| F1 | the skip branch: `if disposition in ("skip", "unverifiable"):`; then `held = _placeholder_reading(...)`; `red = held and any(...)`; `if held and not red: return held`; `if not held:` → `if disposition == "skip": return (f"skipped:{reason or 'no reason given'}", "")`, else the unverifiable return | `ledger.py:763-773` [read] |
| F2 | the manifest road `pending_implementation` is reached only per CASE, inside `for case in cases` | `ledger.py:716-732` [read] |
| F3 | `plan_row_state(row, manifest, report, triage, cases_by_row, gaps)`; `build` calls it once per md row | `ledger.py:679`, `:1575`, `:1592-1595` [read] |
| F4 | `parse_plan`: header cells `strip_cell(c).lower()`; `mapping = {i: PLAN_COLUMNS[h] ...}`; an unknown header is ignored; each mapped cell is `strip_cell(cell)` (whitespace and backticks off, CASE KEPT); `row["line"] = " | ".join(cells)` (every cell, mapped or not) | `contract.py:2882-2904`, `:2842-2843` [read] |
| F5 | `PLAN_COLUMNS` (12 keys), `PLAN_REQUIRED_COLUMNS = ("ts", "r", "observable", "disposition_cell", "fit")` | `contract.py:2744-2761` [read] |
| F6 | `check_plan_v0` refuses a disposition outside `C.DISPOSITIONS` and a disposition with no reason; a non-empty level outside `C.PLAN_LEVELS`; and **`new_behaviour = row.get("fit") == "new" or "pending_implementation" in row["line"]`**, which refuses an oracle `history:` and an observable `current-code` on such a row | `validate_artifacts.py:1894-1900`, `:1914-1918`, `:1931-1938` [read] |
| F7 | `check_cell_counts` refuses only a NON-EMPTY cell beyond the header width; a new header column with empty or filled cells has no effect | [digest L-2] (`validate_artifacts.py:250-265`, `contract.py:1411-1419`) |
| F8 | ONE call site of `check_plan_v0`: `collect_errors` on `test-plan.md` when `plan_is_v0` | `validate_artifacts.py:2668-2670` [read] |
| F9 | the call is reached by the PostToolUse hook on BOTH hosts: Claude `hooks/hooks.json:66-74` (`Write|Edit`) [digest L-3]; Codex `hooks/codex.json:27-34`, matcher `.*apply_patch|Write|Edit` [read]. Not on the S3 exit: the S3 detectors are `planning_contract.py`, `branch_accounting.py`, and `exit_gate.collect_errors` has no test-plan.md check | [digest L-3] |
| F10 | the delivery reader: for each ledger row, `kind = DV.kind_of_state(state, ...)`; a `none` verdict leaves no record; a `no` record's text is `ledger: {ref} is \`{state}\` ({detail or 'no detail'})` | `check_delivery.py:1689-1726` [read] |
| F11 | `pending_implementation` maps to kind `pending_implementation`, `no`, owner product; `skipped` (prefix) maps to `planned_skip`, `none` | `delivery-verdict-kinds.json:21`, `:44`, `:95`, `:97` [read] |
| F12 | the report files a requirement under "Skipped by the plan" when every plan row naming it is `skip`/`unverifiable` (`_plan_decision`), except a recorded product gap (`gap_ids`) | `report_facts.py:2878-2918` [read] |
| F13 | without ledger plan rows, the delivery summary falls back to the JSON plan: `skip` → `deferred_by_decision` (kind `deferred_undecided`, `no`) | `delivery_summary.py:252-258` [read]; `delivery-verdict-kinds.json:33`, `:98` [read] |
| F14 | the R3 row in md: `` | TS-23 | Add from quick view | R-23 | smoke | blocked-flow | P1 | expected-contract:none (no observable) | requirement:R-23 | `skip` — the owner's answer leaves no implemented quick-view add path to verify inside add-to-cart scope |  |  | smoke | ``; the header has 12 columns and no `skip class` | `fixtures/stories/local-1-0108/test-plan.md:17`, `:41` [read] |
| F15 | the good fixture's skip row: TS-3 `` `skip` - cosmetic, outside the diff, no user impact recorded ``, fit `—`, observable bare `expected-contract` | `fixtures/artifacts-good/test-plan.md:15` [read] |
| F16 | test homes: `test_validators.py` is keep, layer `detector`, covers `validate_artifacts.py`, `contract.py` (`test-layers.json:6607-6625` [read]), not in `slow_tests.json` [read: Grep of the three names finds only `test_third_verdict.py: 39.7`]; it holds the block "rule: plan dispositions, observables, oracles, anti-patterns" built on `variant(file, old, new)` + `ok`/`rejects` (`test_validators.py:457-489` [read]). `test_ledger.py` is keep, `detector`, covers `ledger.py`, `contract.py` (`test-layers.json:2829-2852` [read]), not slow; it calls `L.plan_row_state(...)` directly (`test_ledger.py:1486-1487` [read]). `test_third_verdict.py` is keep, `detector`, covers `check_delivery.py` (`:6514-6535` [read]), slow 39.7 s. `test_report_facts.py` is keep, `gate_named` (`:4473-4475` [read]). `test_case_gates.py` is QUARANTINED (`:7477` [read]). |
| F17 | the scenario walker's variant road cannot carry the delivery row on `local-1-0108` as the story stands: a variant picks the FIRST walk entry of its `stage` (`scenario_walk.py:786` [read]), and the story has two `S8` entries, the exit gate first and the delivery door second (`story.json:150-176` [read]); no story has a `variants.json` today (Glob `fixtures/stories/*/variants.json`: none; positive control: the same Glob shape with `expected.json` finds 3 files [read]) |
| F18 | the slice is generated: `python -B scripts/contract_slices.py --write` renders `references/slices/<role>/<subject>.md`; `--check` refuses a stale slice (selftest and audit A9 run it) | `scripts/contract_slices.py:25-41`, `:259-263` [read] |
| F19 | the FR-21 debt row's text is read by a test: `test_s1_s2_contract.py:300-309` reads the row and checks that it holds `**narrowed` and `pending_implementation` | [read] |

---

## 3. Card FL2 (header-ready). Executable on F-L2-A (a), F-L2-B (c), and the recommendations of F-R2-2..F-R2-5. Dispatch only after F-R2-1 is answered "keep"

```
given: this file (§1-§8); docs/tasks/specs/20261117-rules-debt-phase2-s9-fl-cards-spec.md §3.1-§3.3 and "Lead decisions on FL2";
  docs/tasks/specs/reports/20261117-rules-debt-fl2-premises-scout-digest.md; ai-packages/qa-factory/design/factory-rules.md (whole);
  plans/builder-rules.md; ai-packages/qa-factory/design/architecture.md (AR-1, AR-10, AR-13, AR-20, AR-22, AR-27, AR-28);
  ai-packages/qa-factory/scripts/tests/fixtures/stories/local-1-0108/test-plan.md:17,41 (the R3 row, input of step 0);
  ai-packages/qa-factory/scripts/tests/fixtures/artifacts-good/test-plan.md:15 (TS-3, input of the test rows)
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/contract.py (PLAN_COLUMNS: one key; SKIP_CLASSES constant beside DISPOSITIONS; nothing else)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/validate_artifacts.py (check_plan_v0 only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/ledger.py (plan_row_state, the skip branch :763-773 only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/report_facts.py (_plan_decision only; F-R2-3)
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/artifact-contract-plan.md (one row of the column table :44-57)
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/slices/qa-test-strategist/artifact-contract-plan.md (regenerated by contract_slices.py --write only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/role-load.json (process_ratchet_tokens.qa-test-strategist only, and only per F-R2-4)
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules-debt.md (the FR-21 row :23 and the narrowed entry :175-178)
C:/QAFactory/forge-repo/ai-packages/qa-factory/changelog.d/rules-debt-fl2-skip-class.md (new fragment)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_validators.py (rows in the "rule: plan dispositions" block :457-489)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_ledger.py (one new table function beside two_areas_are_two_cases_in_the_ledger, registered in main)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_third_verdict.py (one end-to-end row) -- after C3-R, which adds a row to the same file
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_report_facts.py (one table row for item 5)
non-goals: references/delivery-verdict-kinds.json (unchanged: the state word already maps, L10 of test_third_verdict.py:110 pins it);
  the manifest `unresolved` road; the D1-C2 product-gap road (gate_preflight, product_gaps.py, check_delivery.product_gap_records) -- untouched,
  see F-R2-1; parsing `reason` (FR-12); `unverifiable` rows; the JSON plan work/test-plan.json, planning_contract (validate_plan,
  gate_plan_errors, _rerender_plan_cells, S3_FENCE_LINE) and plan_row.py; driver_dispatch.py S3_FENCE_LINE, phases/s3.md, the S3
  handoff YAML (FR-38 is met by the contract table, §6); agents/qa-test-strategist.md; judgment-census.json (check_plan_v0 stays
  shape: confirm and report, no edit); check_traceability.py and delivery_summary.py (readers unchanged, §7); test_case_gates.py
  (quarantined); a new test file; an S3-exit judge of the cell (§4)
handoff: the builder report (builder.md rule 7): the witness, step 0's output before and after, red-before lines, the FR walk
  (C, D, E, G; A/B/F one line each), "check_plan_v0 stays shape" with the census line re-read, the role_load.py numbers before/after
edges: E1-E12 (§5)
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <every owns path above>` -- the files it names
  that are slow (test_third_verdict.py at least) are written "judged by the batch canon"; plus
  `python -B ai-packages/qa-factory/scripts/contract_slices.py --check` (exit 0); plus `python -B tools/architecture_index.py --check`;
  plus for artifact-contract-plan.md and factory-rules-debt.md the DOC-DISPATCH key run (CLAUDE.md rule 11) with the keys of item 6/7
  quoted before the run, the script in full, and a negative control
  test: test_validators.py::"rule: plan dispositions" SKIP_CLASS_ROWS | expected from: §3 item 2 and §5 E1-E3, E9, E10 of this file, FR-1
  test: test_ledger.py::skip_class_reads_into_the_state | expected from: §3 item 3, §5 E1, E2, E4, E5, F-L2-A (a)
  test: test_third_verdict.py::the end-to-end row | expected from: §3 item 4, delivery-verdict-kinds.json:44 (FR-21)
  test: test_report_facts.py::item 5 row | expected from: §3 item 5, report_facts.py:2906-2907 (the gap_ids precedent), FR-10
  test: none -- doc | expected from: §3 items 6-8 (DOC-DISPATCH key run)
siblings: axis 34 (one road): NOT covered, D1-C2 is a live second road, fork F-R2-1 in this file; axis 32 (census): no row change,
  stated; the delivery-verdict axis (SIBLING_MAP:144): readers unchanged, the state maps through the existing row; analog reported
  (not widened): check_plan_v0 runs only on the write hook (§4); _rerender_plan_cells does not clear the cell (E11)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-fl2-card-r2.md (once accepted)
```

### Step 0: premise run, before any edit (output goes into the report)

From the repo root:

```
python -B -c "import sys; sys.path.insert(0, 'ai-packages/qa-factory/scripts'); import contract as C, ledger as L; rows = C.parse_plan('ai-packages/qa-factory/scripts/tests/fixtures/stories/local-1-0108/test-plan.md'); r = next(x for x in rows if x['ts'] == 'TS-23'); print(sorted(k for k in r if k == 'skip_class')); print(L.plan_row_state(r, {}, {}, {}, {}))"
```

Expected TODAY: `[]`, then `('skipped:the owner\'s answer leaves no implemented quick-view add path to verify inside add-to-cart scope', '')`.
Expected AFTER the change, with the same command on a scratchpad copy of that `test-plan.md` that has a `skip class`
header added and `pending_implementation` in TS-23's cell: `['skip_class']`, then
`('pending_implementation', "the owner's answer leaves no implemented quick-view add path to verify inside add-to-cart scope")`.
The copy is never the fixture itself (it is the scenario's world).

If `plan_row_state` raises on the project config (`C.case_config()` is called unconditionally, `ledger.py:714` [read]),
the builder runs the same two lines inside a temp project, the way `test_ledger.py` does (`use_project`), and
reports that. If the "today" output differs from the expectation, the builder STOPS and returns the output, because
the premise is false.

### Items (each: file, function or field, behaviour, test row, expected-from)

1. **`contract.py`.** Add the key `"skip class": "skip_class"` to `PLAN_COLUMNS` (`:2744-2760`). Do NOT add it to
   `PLAN_REQUIRED_COLUMNS` (`:2761`): the column is optional (E1). Add `SKIP_CLASSES = (PENDING_IMPLEMENTATION,)` right
   after `DISPOSITIONS` (`:67`), with a one-line comment: "the closed classes of a `skip` plan row (FR-21): the row
   reads as the existing ledger state of the same name". Test: through items 2 and 3 (no test of a constant).

2. **`validate_artifacts.check_plan_v0`** (`:1850-1938`). After the disposition rule (`:1894-1900`), add:
   - `cls = row.get("skip_class", "")`; a cell that is empty, or is exactly one of `-`, `–` (U+2013), `—` (U+2014),
     counts as ABSENT (F-R2-2, recommendation (a)). Absent: no refusal.
   - present and `cls not in C.SKIP_CLASSES` → refusal
     `f"{path.name}: {ts}: skip class '{shown}' outside {list(C.SKIP_CLASSES)} — leave the cell empty, or write \`pending_implementation\` on a \`skip\` row the product does not carry yet (delivery then reads no)"`,
     where `shown` is the value cut to 80 characters plus `…` when it is longer (the echo cap; E9). Matching is
     case-exact, after `strip_cell`.
   - present, in the set, and `disposition != "skip"` → refusal
     `f"{path.name}: {ts}: skip class on a \`{disposition}\` row — the class belongs to a \`skip\` row; empty the cell"`.
   - Each refusal goes through `refusal("validate_artifacts:check_plan_v0", ...)`, like its neighbours.
   - Do not touch `:1931` (`new_behaviour`). Its effect on a classed row is E10.
   **Test:** a table `SKIP_CLASS_ROWS` in the "rule: plan dispositions" block of `test_validators.py` (`:457-489`).
   Each row is (id, cell value, the row's disposition, expected `ok` or a refusal key). The table is fed by ONE helper:
   it adds `| skip class |` to the header and `|---|` to the separator of a `Q1/test-plan.md` copy, puts the value
   into TS-3's cell and an empty cell into every other row, and swaps TS-3's disposition when the row says so. The
   helper is the same `variant`/`write` pattern the block already uses. Rows (input from outside, a role writes the
   cell, so the mini-battery applies):
   | id | value | disposition | expected |
   |---|---|---|---|
   | S1 | `pending_implementation` | skip | ok |
   | S2 | `` `pending_implementation` `` | skip | ok (backticks stripped, F4) |
   | S3 | `   pending_implementation   ` | skip | ok (whitespace stripped) |
   | S4 | (empty) | skip | ok (absent) |
   | S5 | `—` | skip | ok (absent; F-R2-2) |
   | S6 | `Pending_Implementation` | skip | refused, key `outside ['pending_implementation']` |
   | S7 | `PENDING_IMPLEMENTATION` | skip | refused, same key |
   | S8 | `pending implementation` | skip | refused, same key |
   | S9 | `pending_implementation, impossible` | skip | refused, same key (two values) |
   | S10 | `pending_implementation pending_implementation` | skip | refused, same key |
   | S11 | `pending_implementat\u0456on` (U+0456 CYRILLIC SMALL LETTER BYELORUSSIAN-UKRAINIAN I, written as the escape) | skip | refused, same key |
   | S12 | `pending\uff3fimplementation` (FULLWIDTH LOW LINE, as escape) | skip | refused, same key |
   | S13 | `x` * 80 | skip | refused; the refusal holds the 80 characters whole and no `…` |
   | S14 | `x` * 81 | skip | refused; the refusal holds 80 `x` then `…`, never 81 |
   | S15 | `x` * 10000 | skip | refused; refusal line under 400 characters |
   | S16 | `pending_implementation` | automate | refused, key `skip class on a` |
   | S17 | `pending_implementation` | unverifiable | refused, key `skip class on a` |
   | S18 | (header without the column, the fixture as is) | skip | ok (world 1) |
   Expected from: this item and E1-E3, E9 (rule text written by the spec), FR-1. Red-before: S6-S17 are red before the
   change (no rule yet), and S14 is red until the cap exists; one narrow run of `test_validators.py`, quoted.

3. **`ledger.plan_row_state`, skip branch** (`:771-772`). Inside `if not held:` → `if disposition == "skip":`, BEFORE
   the free-reason return, add:
   `if row.get("skip_class") == C.PENDING_IMPLEMENTATION: return ("pending_implementation", reason)`.
   This is exact equality on the value `parse_plan` already stripped. Any other value (absent, empty, a dash, a typo,
   another word) falls through to today's `skipped:<reason>`. Nothing else in the function changes. The detail is the
   strategist's `reason` verbatim (small choice C3): `check_delivery` prints it as
   `ledger: TS-23 is \`pending_implementation\` (<reason>)` (F10), in the task's own terms (FR-20). It is shown, never
   parsed.
   **Test:** a new function `skip_class_reads_into_the_state` in `test_ledger.py`, one table, calling
   `L.plan_row_state({"ts": "TS-1", "disposition": d, "reason": "r", **extra}, {}, {}, {}, {})` inside a temp project
   (`use_project`, as `:1486-1487` does). Rows:
   | id | disposition | extra | expected |
   |---|---|---|---|
   | L1 | skip | `{"skip_class": "pending_implementation"}` | `("pending_implementation", "r")` |
   | L2 | skip | `{}` | `("skipped:r", "")` |
   | L3 | skip | `{"skip_class": ""}` | `("skipped:r", "")` |
   | L4 | skip | `{"skip_class": "Pending_Implementation"}` | `("skipped:r", "")` |
   | L5 | skip | `{"skip_class": "impossible"}` | `("skipped:r", "")` |
   | L6 | skip | `{"skip_class": "—"}` | `("skipped:r", "")` |
   | L7 | unverifiable | `{"skip_class": "pending_implementation"}` | `("skipped:unverifiable — r", "")` |
   | L8 | automate | `{"skip_class": "pending_implementation"}` | equal to the same call without the key (invariant named in E3) |
   | L9 | skip, reason "" | `{"skip_class": "pending_implementation"}` | `("pending_implementation", "")` |
   Plus one `L.build` row on an `artifacts-good` copy whose `test-plan.md` has the column with `pending_implementation`
   in TS-3 only: `state_of(doc, "TS-3") == "pending_implementation"`, and every other row's state is equal to a build
   of the unmodified copy (E1 world 2). Expected from: F-L2-A (a), this item, E1, E2, E4, E5. Red-before: L1, L9 and
   the build row are red before the change.

4. **Delivery end to end (no code change: the kinds file already maps it).** One row in `test_third_verdict.py` next
   to the K-N8.1 table: on a copy of `fixtures/after-checks/` (the file's world, `:31`, `:37-42` [read]), add the
   `skip class` column to `test-plan.md` with `pending_implementation` on a `skip` row (if the fixture's plan has no
   `skip` row, turn one row into `` `skip` - <reason> `` in the copy). `CD.assess(task)` then gives
   `delivery_verdict == "no"`, and a reason record of kind `pending_implementation` whose text names that TS. The same
   copy without the class keeps the fixture's own verdict, which is `after_checks` per the file docstring (`:9-13`
   [read]; "no `no` kind anywhere"). So the row is a clean before/after on one world. Expected from:
   `delivery-verdict-kinds.json:44` (FR-21), item 3. The file is slow, so it is "judged by the batch canon";
   `red-before: not run -- test_third_verdict.py is judged by the canon`.

5. **`report_facts._plan_decision`** (`:2878-2903`; F-R2-3, recommendation (a)). In the "every plan row that names
   the requirement is a `skip` or `unverifiable` one" clause, a row that is `skip` and carries
   `skip_class == C.PENDING_IMPLEMENTATION` does NOT count as the plan's decision. If such a row is the only reason,
   `_plan_decision` returns `""`, so the requirement is not filed under "Skipped by the plan". The `_not_proven`
   twin must also not list it as "could not execute", so `_not_proven` skips an item when any of its plan rows carries
   the class, the way it already skips `gap_ids` (`:2940`). The requirement then stands only among the product reasons
   (the ledger record of item 3). That is the D1-C2 precedent: "a product gap stands among the product reasons"
   (`:2941`). The plan rows reach `_plan_decision` as md rows from `parse_plan` (`:274`, `:1381` [read]), so
   `skip_class` is on them. **Test:** one table row in `test_report_facts.py` that calls `_skipped_by_plan` and
   `_not_proven` with a `reqs` item of R-1 and plan rows `[{"ts": "TS-1", "requirements": ["R-1"], "disposition":
   "skip", "reason": "r", "skip_class": "pending_implementation"}]`: R-1 is in neither list. A control row without the
   class: R-1 is in `_skipped_by_plan` with cause `r`. The builder copies the item shape from the nearest existing
   `_skipped_by_plan` caller in that file; if none exists, the builder returns a question rather than invent the
   shape. Expected from: this item, `report_facts.py:2906-2907`, FR-10.

6. **`references/artifact-contract-plan.md`**, the column table (`:44-57`): one row after `disposition + reason`
   (`:54`):
   `` | `skip class` | optional; `pending_implementation` on a `skip` row whose behaviour the product does not carry yet (delivery reads no, owner product); empty otherwise | ``
   Then `python -B ai-packages/qa-factory/scripts/contract_slices.py --write` regenerates
   `references/slices/qa-test-strategist/artifact-contract-plan.md` (never edited by hand), and `--check` exits 0. DOC
   key run keys, quoted now: `` `skip class` ``, `pending_implementation` on a `skip` row, `empty otherwise`, each in
   both files.

7. **`design/factory-rules-debt.md`.** Row FR-21 (`:23`): the "What is left is the first word" clause becomes
   narrowed. A skip row the strategist classes `pending_implementation` (the plan's `skip class` column) now blocks, and
   so does a person's product-gap word at gate A (D1-C2). Keep the tokens `**narrowed` and `pending_implementation`
   in the row (F19: `test_s1_s2_contract.py:300-309` reads them). Entry `:175-178`: add one sentence that the
   `skipped` half is closed by data for classed rows, still proved only by a live run (FR-33). DOC key run keys:
   `skip class`, `D1-C2`, `**narrowed`.

8. **`changelog.d/rules-debt-fl2-skip-class.md`**: two English lines, in the form of `changelog.d/README.md`: the new
   optional plan column and its delivery effect.

9. **`references/role-load.json`** (F-R2-4, recommendation (a)). Run `python -B ai-packages/qa-factory/scripts/role_load.py --all`
   before and after item 6. If `qa-test-strategist`'s process load is above 17629, raise
   `process_ratchet_tokens.qa-test-strategist` to the measured number exactly. The raise is named in the report and in
   the commit message (AR-20). If it is not above, no edit.

---

## 4. The write hook vs an S3-exit judge (brief point 2): the Lead's leaning is CONFIRMED

The inputs that decide it:
- **What the ledger does with an unknown value.** By item 3, only the exact `pending_implementation` changes the
  state; every other value reads as today (`skipped:<reason>`, kind `planned_skip`, verdict `none`). So a value the
  hook would have refused, if it reaches the ledger anyway, gives exactly today's verdict.
- **Can a plan reach delivery without passing the hook?** Yes, by a write that is neither `Write`/`Edit` (Claude,
  `hooks.json:66-74` [digest]) nor `apply_patch`/`Write`/`Edit` (Codex, `codex.json:27-34` [read]). Examples: a
  `Bash` redirect, a code writer, or a hand edit outside the host. Both hosts have the hook, so no host is without it.
- **Does an S3 exit judge exist for ANY rule of `check_plan_v0`?** No [digest L-3]. The disposition and level rules
  share the same gap.

Verdict: the write hook is enough for FL2. FR-59 / AR-28 forbid an unknown becoming a pass. A bypassed bad value reads
as `planned_skip`, which is today's reading of the same row. The change opens no new pass, and it never turns a
reading that today says `no` into `none`. The only reading FL2 can strengthen is the valid value on a `skip` row
(`none` → `no`), and that moves toward refusal. A value written on a non-skip row and bypassing the hook is ignored by
the ledger (the class acts only in the skip branch), so that is not a pass either.

The residual is real but pre-existing, and it belongs to a class FL2 does not create: every `check_plan_v0` rule is
skipped by a non-hook write. I report it as an analog and do not widen scope (Lead: a pile line if wanted). The
direction that is NOT permitted: making the ledger read an unknown non-empty class as `no`. That would read a planned
skip as `no` without the strategist's word (§5 reused-function paragraph), so it is excluded.

---

## 5. Edges (rule 11), each with the invariant it protects

- **E1 TEMPORAL.** World 1 (every plan before FL2): no `skip class` header, so `parse_plan` puts no key (F4), and
  every skip reads `skipped:<reason>` as today. World 2: the header is present and the cell is empty or a lone dash,
  which reads as absent. The column becomes possible with this card's commit (item 1). The strategist starts writing it
  with the next S3 after the plugin update (item 6). The recorded fixtures are not rewritten. INVARIANT: no old plan
  changes its verdict, and no story in flight is refused for lacking the column (not in `PLAN_REQUIRED_COLUMNS`,
  builder-rules 9).
- **E2 a value outside the set** (S6-S15) is refused by `check_plan_v0`, which names the allowed value and the door
  "leave the cell empty" (FR-1, FR-2). If it reaches the ledger anyway (§4), it reads as absent. INVARIANT: an unknown
  class is never read as `pending_implementation`, and never as a pass that today refuses.
- **E3 a class on a non-skip row** (S16, S17) is refused. The ledger ignores it (L7, L8). INVARIANT: an `automate`,
  `manual-*` or `unverifiable` row never reads `pending_implementation` through this field, and its state equals the
  state without the key.
- **E4 POSITIONAL** (ledger). The new return sits inside `if not held:` and `if disposition == "skip":`, before
  `:772`. INVARIANT: an open placeholder still wins when no case is red (`:768-769`, J-C7); a red of the row's cases
  still falls through to `failed:*` (`:767`); a skip row without the class reads byte for byte as today (L2). Case
  rows of the manifest (`:716-761`) are read before this branch and are not changed.
- **E5 FR-12**: the `reason` is never read to infer the class. A reason that says "not implemented", with no class,
  stays `planned_skip` (L2 shape). INVARIANT: the class comes only from the closed cell.
- **E6 CONFLICT with the grounding road**: a classed skip row whose requirement the grounding table also calls
  `not_implemented` gives two `pending_implementation` records (the ledger row and
  `check_delivery._pending_implementation_records`), both `no`, owner product. INVARIANT: the verdict is `no` either
  way. Deduping is not this card's job.
- **E7 CONFLICT with D1-C2** (new, §0): a classed TS-23 whose person ALSO answers `product gap` at gate A gives a
  `pending_implementation` record (TS-23) AND a `product_gap` record (R-23). Both are `no`, owner product. The report
  leaves R-23 out of "Skipped by the plan" by either reader (item 5, `gap_ids`). INVARIANT: the verdict is `no`, and
  the person reads the gap among the product reasons, never as "deferred by your decision". The doubled reason line is
  the visible cost of two roads (F-R2-1).
- **E8 CONFLICT md vs JSON**: the ledger reads the md row only, as today. The JSON row has no `skip_class`. INVARIANT:
  FL2 adds no second reader of the plan; no parity check (L-5 [digest]: none exists).
- **E9 LIMIT (introduced here)**: the refusal echoes at most 80 characters of a bad value, then `…`. At 80 the value
  is shown whole (S13); at 81 it is cut (S14). INVARIANT: a refusal line stays readable whatever a role writes
  (10 000 characters, S15). The refusal never shows less than the first 80 characters, so the role can find its value.
- **E10 side effect of `:1931`**: a row whose `line` holds `pending_implementation` is "new behaviour", so an oracle
  `history:` and an observable `current-code` are refused on a classed row. INVARIANT: a product-gap row is not judged
  against history or current code, which is the right meaning ("the product does not carry it"). The R3 row is
  unaffected (`expected-contract:none`, `requirement:R-23`, F14). No change to `:1931`. The builder adds no test row
  for it (an existing rule, now also reached by a cell).
- **E11 an answer at gate A re-renders the md row**: `planning_contract._rerender_plan_cells` rewrites only
  `disposition_cell`, `level`, `fit` and `question_rename`, and keeps every other cell [digest L-2]. A gate-A answer
  that turns a classed `skip` into `automate` leaves the class cell standing. The ledger ignores it (E3, L8), and the
  next role write of the md is refused by S16. INVARIANT: the stale cell can never make a non-skip row read
  `pending_implementation`. The cosmetic residual is reported as an analog, not fixed here (planning_contract is a
  non-goal).
- **E12 the fallback with no ledger rows** (F13): the JSON plan's `skip` already reads `deferred_by_decision`, which
  is `no`, without any class. INVARIANT: no reading becomes softer; the reader is unchanged.

**The reused function in a more load-bearing role** (`ledger.plan_row_state`'s skip branch: a planned skip used to
be a `none` reading only, and now it can stop delivery). **Permitted error direction**: toward TODAY. A product-gap
skip that is written without the exact class (absent, typo, wrong case, a look-alike, a dash) reads `planned_skip`,
as it does today. **Forbidden error**: a planned skip read as `no` without the strategist's exact word on THAT row.
**Adversarial inputs that must stay on the safe side (read as `planned_skip`)**: every S4-S15 value (L3-L6 at the
ledger), a class on an `unverifiable` row (L7), a reason text naming `pending_implementation` with an empty class (E5),
a class in a cell of ANOTHER row of the same requirement (it acts only on its own row). `parse_plan`'s `strip_cell`
folds whitespace and backticks only, never case (F4), so case-exact matching is preserved end to end.

---

## 6. Which text tells the strategist (brief point 4): the plan contract table only (the leaning is CONFIRMED)

- FR-38 / AR-10 ask that the requirement reaches the role before the work, in the fields it must fill. The strategist
  writes the md table from the column table of its plan contract. That table is injected as its slice
  (`inject-map.json:42` [read]), and the charter points there (`agents/qa-test-strategist.md:74` [old spec §3.1,
  t-1034]). One table row is the field-level carrier.
- The four same-sentence texts [digest L-6]: `driver_dispatch.S3_FENCE_LINE` (`:2587-2591`), the
  `planning_contract` `fence.plan_row` refusal (`:3969-3978`), `skills/qa-story/phases/s3.md:141` and
  `handoffs/s3-strategist-to-designer.yaml:70-73`. They say "`disposition: skip` with the reason". None of them lists
  columns. The column is optional and acts only for one class. Adding it to the per-dispatch text would cost tokens on
  EVERY S3 dispatch (the packet allowance) for a rare row, and it would put the same rule in a second place to keep in
  step. Not added.
- **Byte cost** (estimate, not measured): the row of item 6 is about 150 bytes, which is about 38 tokens at
  `bytes_per_token: 4` (`role-load.json:5` [read]), all in the strategist's slice. `ratchet_tokens.qa-test-strategist`
  is 19768 with `ratchet_slack_tokens` 1000 (`:9`, `:13` [read]). `process_ratchet_tokens.qa-test-strategist` is 17629
  with slack 0 (`:24-27` [read]). Unless the slice section is a `kind: craft` section, the 38 tokens are process tokens
  and A22 turns red without a named raise. Hence F-R2-4 and item 9. The measured number replaces this estimate in the
  report.

---

## 7. Readers of every touched file (designer rule 7)

Grep over `tools/` (content), `.githooks/` (content) and `.claude/` (`glob: !**/worktrees/**`) for
`ledger\.py|validate_artifacts|artifact-contract-plan|report_facts|test_validators|test_ledger|role-load|PLAN_COLUMNS|skip_class|check_plan_v0|plan_row_state|_plan_decision|scripts/contract\.py|"contract\.py"|architecture_gate`.
For `.githooks` the pattern is `contract\.py`. Positive control: `architecture_gate`.
Hits: `tools/` 37 lines, of which 25 are function names `test_ledger_*` in forge tests (`test_search_control_gate.py`,
`test_install_parity.py`, `test_wiring_check.py`: a name prefix, not a reader of `test_ledger.py`). The rest are
`architecture_gate`/`architecture_index`/`mechanism_gate`/`test_architecture_gate` (the positive control), plus the
readers below. `.githooks/` has 1 hit (`commit-msg:37`, the control). `.claude/` has 1 file (`agents/designer.md`, the
control).

| touched file / name | reader | verdict |
|---|---|---|
| `scripts/contract.py` | `tools/dup-baseline.json:156`, `:160` (a clone group) | unchanged: one dict key and one tuple add no clone; the builder confirms with the clone ratchet if the walker names it |
| `scripts/tests/test_validators.py` | `tools/lint-baseline.json:283` (a lint baseline row) | unchanged unless the new rows trip a lint class; the builder reports the file's lint result |
| `scripts/ledger.py`, `validate_artifacts.py`, `report_facts.py`, `artifact-contract-plan.md`, the slice, `role-load.json`, `factory-rules-debt.md`, `test_ledger.py`, `test_third_verdict.py`, `test_report_facts.py`, `PLAN_COLUMNS`, `skip_class`, `check_plan_v0`, `plan_row_state`, `_plan_decision` | no hit in the three folders | — |
| `test_third_verdict.py` | `tools/lint-baseline.json:277` (old spec §3.4 rule-7 table, t-1034; not in this round's hits because the name pattern differed) | unchanged; the builder reports the lint result |
| `scripts/tests/test_report_facts.py` | `tools/lint-baseline.json:253` (hit this round) | unchanged; the builder reports the lint result |
| `judgment-census.json` (NOT touched) | `tools/architecture_gate.py:88`, `.githooks/commit-msg:36-37` | unchanged: the census is not edited |

Package readers of the changed names, which rule 7 does not require, listed for the plan critic. `parse_plan` callers
read rows by key [digest L-2]; a new key changes none of them. Readers of a `skip` disposition that do not read the
class: `check_traceability.py:216` (the trace outcome stays "skipped": unchanged; the report side is item 5),
`delivery_summary.py:256` (fallback, E12: unchanged), `branch_accounting.py:1403` `PLAN_EXCLUDING` (a skip row still
excludes its branches by reason: unchanged, the class does not change what the plan checks), `controller.py:3064`
(unchanged), `report_facts.py:2898` (`_plan_decision`, changed in item 5). The dashboard prints
`pending_implementation` as "awaiting implementation" (`factory_dashboard.py:980` [read]): unchanged, and it now also
shows for a classed skip row, which is correct.

---

## 8. The meaning change, for the plan critic (PROJECT.md «Как принимается изменение пакета» п. 6 (б))

Today a plan row with `disposition: skip` can never stop delivery: whatever its reason, the ledger reads
`skipped:<reason>`, kind `planned_skip`, verdict `none`. After FL2, a `skip` row whose md `skip class` cell holds
exactly `pending_implementation` reads as the existing ledger state `pending_implementation`. Its kind
`pending_implementation` says `no`, owner product. So one row a strategist writes at S3 can turn the delivery word from
`yes` (or `after_checks`) into `no`, and the report stops calling that requirement "skipped by the plan". The person
sees the class in the plan at gate A, so the decision is visible before work. Every other spelling, an empty cell,
and every plan written before the change read exactly as today (the permitted error is toward today's reading). What
the critic must weigh beyond the edges: the same delivery effect is ALREADY reachable for the same row through the
person's `product gap` word at gate A (D1-C2, §0), with a different kind and owner of the word. FL2 makes the
strategist's judgment alone sufficient. Is that a second road for one action (P31), or a deliberate second owner?
That is fork F-R2-1, and it is the owner's to answer, not the critic's.

---

## 9. Forks returned

| id | question | options | recommendation |
|---|---|---|---|
| **F-R2-1** (blocks dispatch) | FR-21's skip half already has a live road, D1-C2 (§0): the strategist declares the surface gap in the JSON row's `coverage_obligations`, gate A asks the person, and the person's `product gap` word gives kind `product_gap`, `no`. Does FL2 still add the strategist's `skip class` road? | (a) **one road**: no FL2 code. Close the FR-21 skip half by narrowing the debt row to D1-C2 (one doc node owning `design/factory-rules-debt.md`), after the Lead MEASURES that TS-23 of `local-1-0108` gets the product-gap door today (§10 N-1). The residual "a skip row with no structured gap is never asked" is the strategist's judgment, judged by the S3 critic (P27), not code. Cost: none in code; the live proof row in `live-runs` names D1-C2. (b) **keep FL2 as drafted** (§3): two roads, two kinds (`pending_implementation` on the TS row, `product_gap` on the R), the doubled line of E7, and the strategist's judgment alone stops delivery. Cost: the §3 card, plus a standing P31 exception that must carry the owner's word with its carrier (rule 6). (c) **one road through D1-C2's carrier**: the strategist's class (if kept) does not create a ledger state but makes `check_case_environment_gaps` ask the person for that row even without a structured gap. The person's word stays the one producer of the delivery effect. Cost: a gate_preflight change and a JSON field (it reopens F-L2-B). | **(a)**. It is the one-road option (rule 6). The existing road gives the decision to the owner of intent (the person, P27), it already has its report reader, and the FL2 example row reaches it. Only the owner can authorise (b) as an exception. If (a), this card is withdrawn and replaced by the doc node; if (b), the card in §3 runs as is |
| F-R2-2 | a lone dash (`-`, `–`, `—`) in the `skip class` cell | (a) reads as empty (absent); (b) a value, refused on every row | **(a)**: the table already uses `—` as its empty mark (F15, the fit column), and (b) would refuse every dashed non-skip row, which is friction (AR-12). (a) errs toward today's reading. The cost is three characters in one place, not a phrase list (FR-12 does not apply: a cell placeholder, not wording) |
| F-R2-3 | where the report lists a classed skip's requirement | (a) neither under "Skipped by the plan" nor "Not proven": only among the product reasons (the D1-C2 `gap_ids` precedent, item 5); (b) leave the report as is (it says "deferred by your decision" while the verdict says `no`, FR-10) | **(a)**. (b) contradicts itself in one packet (FR-10). (a) adds `report_facts.py` to owns |
| F-R2-4 | the strategist's process ratchet (slack 0) and the new contract row | (a) a named raise to the measured load (item 9); (b) offset the bytes by trimming other strategist-visible plan contract text; (c) move the line to a `kind: craft` section | **(a)**. (b) risks dropping a rule to fit a cap, which is the loss `role-rules.json` exists to prevent. (c) the line is a process duty, not craft. The Lead reverted a raise in t-1059 by MOVING text that had a better home; no better home exists here (§6) |
| F-R2-5 | the stale class cell after a gate-A answer re-renders the disposition (E11) | (a) leave it (the ledger ignores it; the next role write is refused); (b) `_rerender_plan_cells` empties the class cell when the disposition leaves `skip` (planning_contract into owns) | **(a)** for this card; (b) as a pile line if a live run shows the stale cell reaching a person |

## Small technical choices closed by the designer

- C1: the constant `SKIP_CLASSES` lives in `contract.py` beside `DISPOSITIONS`, built on the existing
  `PENDING_IMPLEMENTATION`, not as a JSON data row (AR-1 precedent of `DISPOSITIONS`).
- C2: the column is optional (`PLAN_REQUIRED_COLUMNS` unchanged), because old plans must keep validating (E1).
- C3: the ledger detail of a classed row is the strategist's `reason` (shown in the delivery reason line; never parsed).
- C4: the echo cap is 80 characters plus `…` (E9), since there is no existing cap for this echo.
- C5: test homes. (i) `check_plan_v0` rows go to `test_validators.py` (keep, detector, fast, the block that already
  judges plan dispositions). (ii) The state row goes to `test_ledger.py` (keep, detector, fast, covers `ledger.py`).
  The delivery word row goes to `test_third_verdict.py` (keep, slow, canon). The report row goes to
  `test_report_facts.py` (keep). The scenario variant road was rejected for this card: there is no `variants.json`, and
  the doubled `S8` walk entry would send a delivery variant to the exit-gate door (F17). `test_case_gates.py` is
  quarantined and gets no row.
- C6: case-exact matching (no folding), so the closed value is one spelling.

## 10. Not established (no shell this round): commands for the Lead

- **N-1 (needed before answering F-R2-1).** Whether the D1-C2 door fires on TS-23 of `local-1-0108` with today's
  code. Read `scripts/gate_preflight.py` `--help` (or its `main`) for the CLI, then run its preflight for gate A on a
  scratchpad copy of `fixtures/stories/local-1-0108/`. Expected: a `case_environment` item for TS-23 whose fix names
  `` `<id>: product gap` ``. Not run; the claim in §0 rests on reading `:2287-2330` and the fixture row.
- N-2: step 0's command (§3), which the builder runs anyway.
- N-3: `role_load.py --all` for `qa-test-strategist`, before and after item 6 (§6 numbers are estimates).
- N-4: whether `fixtures/after-checks/test-plan.md` has a `skip` row (item 4 handles both cases).
- N-5: the slice section of `artifact-contract-plan.md`: craft or process marker (decides whether item 9 fires).
- N-6: `test_s1_s2_contract.py`'s keep or quarantine status was not read. If it is kept, item 7's token rule matters;
  if it is quarantined, the rule is still harmless.

## 11. Reading trail

Read this round: `docs/tasks/specs/20261117-rules-debt-phase2-s9-fl-cards-spec.md:1-568`, `:837-856`, `:1030-1056`; the
digest whole; `scripts/ledger.py:690-784`, `:1565-1624`; `scripts/contract.py:2735-2934`, `:67-72` (Grep), `:83`
(Grep); `scripts/validate_artifacts.py:1835-1944`, `:2650-2679`; `references/delivery-verdict-kinds.json` whole;
`scripts/check_delivery.py:86-105`, `:1680-1729`; `references/artifact-contract-plan.md:40-94`; `hooks/codex.json`
whole; `scripts/tests/fixtures/judgment-census.json:1205-1216`; `scripts/tests/test_judgment_census.py:33-44`, Grep of
`CLASS_ORDER`; `references/role-load.json:1-45`; `references/inject-map.json` (Grep); the strategist slice (Grep);
`scripts/contract_slices.py` (Grep); `fixtures/stories/local-1-0108/test-plan.md:1-50`, `story.json:1-264`,
`expected.json` whole, `work/test-plan.json:2737-2845`; `fixtures/artifacts-good/test-plan.md` (Grep);
`scripts/tests/scenario_walk.py:1-60`, `:205-264`, `:284-291`, `:362-372`, `:770-831`;
`scripts/tests/test-layers.json` entries for the test files named; `scripts/slow_tests.json` (Grep);
`scripts/tests/test_third_verdict.py:1-200`; `scripts/tests/test_ledger.py:404-455` and its function list (Grep);
`scripts/tests/test_validators.py:420-491` and Grep; `docs/TESTING.md` whole; `scripts/gate_preflight.py:2255-2333`;
`scripts/tests/test_d1_product_gap.py:1-40`; `scripts/report_facts.py:2878-2953` and Grep; `scripts/delivery_summary.py:240-264`;
`scripts/check_traceability.py:205-229`; `design/factory-rules-debt.md:23`, `:175-178`; Greps for
`pending_implementation`, `product_gap`, `"skip"`, `PLAN_HEADING` over `scripts/*.py`; rule-7 Greps (§7).
Not read: `scripts/product_gaps.py` beyond its docstring (Grep lines), `gate_brief` bodies, `test_s1_s2_contract.py`
beyond the Grep lines, `local-1-0108/README.txt` beyond line 570 (not needed).
