# t-152 (live-run-fvf/1/FV1-1) — critic verdict on bb2bd10

Verdict: **NEEDS WORK (fit_with_fixes)**: 1 blocking finding (F1, the unlisted test file turns the CI canon red), plus 2
fixes to make before merge (F2, F3). The reader change itself is correct and fits the DoD. Whether to accept is the
coordinator's decision (critic rule 6).

## Fit to the spec (brief q1)

The six DoD edges hold, checked with the patched regex on probes I wrote (trail R2): `P-1` → P-1; `TS-3` → TS-3; `P-99` is
read and then dropped by `_case_rows` (`row in dispositions`); `see above` gives none; an empty line does not borrow the next
line (`Plan row:\r\nCovers: REQ-1` → none); `P-1.`, `` `P-1` `` and `P-1 (boundary)` give P-1; `plan_row: P-1` gives P-1 (s5 only).
On the live run's 39 case files (10 TC + 29 case versions; LF, not CRLF), every file except `critic-findings.md` reads P-1..P-10.
All ten ids exist in `work/test-plan.json`. My own re-run of the node test: `10 passed`.

## (a) Callers: does a non-TS id change meaning or let garbage in?

- `controller._case_rows` (`row in dispositions`) and `contract.case_levels` (`levels.get(row)`) check membership.
  `manifest_from_tests.obligation` (:747) refuses a row not in the plan and names it. These keep their meaning.
- `gate_preflight._branch_cases` (:1995) → `planning_contract` :1801/:1907 compares `plan_row` against JSON row ids. With
  P-n the join now works, and `row_owes_case` stops reading every case as row "". The checks get more accurate. No garbage
  path here: an id that is not a row matches nothing.
- `s5_precheck.check_obligations` / row-field check (:3812, :3856) joins against `C.plan_obligations` (JSON ids, schema 2).
  **This check is NEW for this run:** before the fix every case read as "" and was skipped. After it, P-1..P-7 owe
  `obligation_bindings`. The automator will be asked for them at the S5 exit. That is correct behaviour; I flag it so the
  Lead does not read it as a regression.
- Garbage that is newly admitted (R2): `Plan row: none, see REQ-1` → REQ-1; `Plan row: R-3 / P-1` → R-3;
  `Plan row: UTF-8 P-1` → UTF-8; `Plan row: e2e-1` → e2e-1. The old regex gave "" for all four. Three callers do not check
  membership, so for them the garbage MASKS a fallback or travels on:
  - `branch_accounting._case_records` :1662-1663 skips its front-matter `plan_row` fallback.
  - `s5_precheck.case_plan_row` :3734-3741 skips its manifest-entries fallback.
  - `manifest_from_tests` :1300 writes the garbage id into a manifest row's `plan_row`.
  The effect on the obligation checks is the same as before: a non-row id matches nothing, and the old "" skipped them too.
  These are prose shapes no fixture or live case carries (382 fixture lines, all `Plan row: TS-n`). It is not a blocker; it
  belongs to the reader-convergence node (F4).

## (b) `\s*` → `[ \t]*`, same line only: do real shapes lose their row?

No. These shapes keep their row: CRLF (`[^\n]*?` takes the `\r`, and `\d+` stops before it), indentation with spaces or a
tab, NBSP after the colon, and the s5 front matter including the quoted form `plan_row: "P-1"`, which the old s5 regex did
NOT read. Only two shapes lose it:

- the id on the NEXT line (`Plan row:\nTS-3`) — DoD edge 4 asks for exactly this;
- a NBSP BEFORE `Plan row:` — an exotic shape, seen nowhere.

Positive control: `grep -rn -i "plan row:"` over `scripts/tests` finds 382 lines, and the filter for any line that is not
`Plan row: TS-n` returns 0. The live cases are all `Plan row: P-n` at column 0. Unchanged, and outside this diff:
`contract.CASE_PLAN_ROW_RE` never read front-matter `plan_row`. The s5 comment that says it does is F3.

## (c) Readers that only know TS-n: what this run hits at S5–S8

Measured fact first. In this run `test-plan.md` keys its rows **TS-1..TS-10** ("TS-n here is P-n in work/test-plan.json").
The JSON keys them P-1..P-10. The md is also stale: it was written 18:40, the JSON 18:46. TS-2 is `unverifiable` while P-2 is
`automate`, and TS-4 is `unverifiable` while P-4 is `automate`. So the whole md-plan family now gets case rows `P-n` against
`TS-n` keys. Before the diff it got "". So this is no regression, but it stays broken:

1. **S5/S6/S8 `contract.case_levels`** (:2097) ← `plan_levels` (md, TS keys) gives an empty map. Readers:
   `traceability.py:454/567` (the level column of the S8 trace) and `factory_dashboard` :1083. Every case's level is "".
2. **S8 `traceability.plan_row_for`** (:562, `plan_by_ts` from the md) gives `{}`, so the level fallback by disposition and
   `shape_for`'s `fit` (:580) are empty for every case.
3. **S8 `check_delivery._case_map`** (:410-424): the requirement→cases join through plan rows misses. It is partly covered by
   each case's own `Requirements:` line.
4. **S8 `check_delivery.TS_IN_TEXT`** (:371, used at :321 `reason_refs` and :528 `_named_cases`) and
   `report_facts.py:4472`: a reason that names `P-3` is not resolved to its cases. This fails safe: the owner is left alone
   and nothing is lifted. But the report's bookkeeping refs (`reason_refs`) leave the plan row out.
5. `handoff_check._plan_row_of` :399 (`TS-\d+`, front matter only). These cases have no front-matter `plan_row`, so it gives
   None with or without the fix. Still one more TS-only reader.
6. Not hit by THIS run, but they keep TS-only: `contract.TS_ID_RE`/`parse_plan` (md; a non-goal),
   `validate_artifacts.py:806`, `grounding_table.TS_ID` :1474 (`add_tests` refs).

`question_register._case_plan_row` (:1416) and `gate_brief._read_case` (:2484) already take any form (`\S+`). But they keep
backticks or a trailing dot (`` `P-1` `` and `P-1.` stay unjoinable), so their grammar now differs from the new reader's.

## (d) DUPLICATION AND CONSISTENCY / CODE QUALITY (brief items 6-7)

- DUPLICATION: **F2** (fix before merge). The same new token grammar is pasted twice: `contract.py:3052` and
  `s5_precheck.py:79`. `s5_precheck` already imports `contract as C`. The commit's `architecture: AR-13 -- one reader ...
  stays the only reader of a case's plan row` is **not true**. Readers of the same fact with four grammars: `CASE_PLAN_ROW_RE`,
  `s5_precheck.PLAN_ROW_RE`, `question_register._case_plan_row` :1409, `gate_brief._read_case` :2482-2485,
  `brief_pack.PLAN_ROW_RE` :66 (`plan_row:\s*(\S+)`), `handoff_check._plan_row_of` :389, and the front-line fallback of
  `branch_accounting` :1663. Grepped: `CASE_PLAN_ROW_RE|case_plan_row|PLAN_ROW_RE` (case-insensitive) and `Plan row:` with
  `re.|search|compile` over `scripts/*.py`. Positive control: both reveal the two edited lines. Minimal fix in this round:
  build `s5_precheck.PLAN_ROW_RE` from one shared token constant in `contract` (e.g. `PLAN_ROW_ID_TOKEN`), so the grammar has one
  home. Correct the commit's AR-13 line. Converging the other five is F4.
- CODE QUALITY: **F3** (fix before merge, one comment). `s5_precheck.py:76-78` still says `Plan row: TS-n` / `plan_row: TS-n`
  and "`contract.case_levels` reads both". It is false: `contract.case_plan_row` reads only the body line, and
  `case_levels`'s docstring at :2096 makes the same false claim. The diff edited the line right under that comment. No new
  function, nesting or dead branch.

## (e) Test: layer and row

The test has killing power: with the old regex, row 1 gives mapping `{}` against `{"TC-001": "P-1"}`, and the fallback
through `required_scenarios` is empty. It goes through the real `Controller._case_rows` and `contract.case_index`, so it is
a junction. **F1 (BLOCKS):** `test-layers.json` has `enforce_listing: true`, and `selftest._listing_ok` (:737-740) emits
`tests: unlisted: test_plan_row_id_forms.py` as a FAIL, so the canon goes red. `docs/TESTING.md` «Бюджет» also says a new
test file is not created. Two roads, the Lead picks one:

- (i) preferred: move the rows into `test_case_id_form.py` (`table` layer, "case id forms", already `covers` `contract.py`).
  Id parsing is a table-layer subject.
- (ii) keep the file with a keep row:
  `"test_plan_row_id_forms.py": {"layer": "data_join", "why": "a case's Plan row (S4 case designer) -> Controller._case_rows / s5_precheck.case_plan_row: joined in the plan's own id form (FV1-1)", "named_by": [], "replaced_by": null, "covers": ["contract.py", "controller.py", "s5_precheck.py"]}`.

The test is 57 lines against 4 product lines with no reason given (TESTING «Бюджет»). Folding it into (i) settles that.

## Class completeness / ONE ROAD (rule 5, rule 19, brief q4/q12)

The class: **the plan-row id has two forms in one story** (JSON `P-n`, md and contract `TS-n`) and seven readers with four
grammars. No SIBLING_MAP axis covers it. I grepped the map for `plan.row|plan_row|TS-n|id form`; the only hit is the
critic-word axis at :152, which is unrelated. ONE ROAD: the diff adds no exclusion. It widens two readers, the TS-only
readers stay, and that is a two-road state. The diff is not blocked for it: it is the DoD's chosen hotfix, and the finding's
own proposal (one form, an S3 exit refusal) is a different direction that the Lead set aside. The residual must leave this
verdict as a node:

- **F4 (proposed node, owner = Lead of `live-run-fvf`, the decision belongs to that tier):** "one plan-row id, one reader".
  - (a) The S3 exit refuses a plan whose JSON row ids differ from its md `TS` column. Or the md is rendered from the JSON with
    the same ids. A stale md (TS-2 `unverifiable` against P-2 `automate`) is its own data defect.
  - (b) `case_levels`/`plan_levels`, `traceability.plan_by_ts`, `check_delivery._case_map`/`TS_IN_TEXT`,
    `report_facts:4472`, `handoff_check:399`, `validate_artifacts:806` and `grounding_table:1474` read through one id
    reader.
  - (c) `question_register`/`gate_brief`/`brief_pack` switch to the contract reader.
  - (d) A new SIBLING_MAP axis «plan-row id readers», in the same commit.

  Before this run reaches S8 the Lead needs at least item (c)1-2 above or a mapping. Otherwise every case of the S8 trace has
  an empty level and shape.

## Seams (q3) / Hygiene (q8) / Ratchets (q9) / JUDGMENT (q11)

- Seams: two regex lines, additive, nothing reordered.
- Hygiene: the changelog fragment is English, `--lang` is reported 2/2.
- Ratchets: none touched.
- JUDGMENT: none moved. It is a shape read; membership stays with the caller's join. `judgment: none` holds.

## Trail

- `git show bb2bd10` (whole diff).
- Callers read:
  - `contract.py` :2085-2125, :2760-2770, :2870-2900, :3610-3625, :3710-3735, :5192-5204
  - `branch_accounting.py` :1650-1685
  - `gate_preflight.py` :1975-2030
  - `planning_contract.py` :1740-1760, :1795-1815, :1895-1912
  - `s5_precheck.py` :3725-3760, :3800-3880
  - `manifest_from_tests.py` :740-760, :1295-1303
  - `question_register.py` :1405-1440
  - `gate_brief.py` :2482-2485
  - `brief_pack.py` :66
  - `handoff_check.py` :380-405
  - `traceability.py` :450-455, :560-580
  - `check_delivery.py` :310-330, :406-425, :518-545
  - `controller.py` :2434-2463
  - `selftest.py` :724-740
- Also read: `test-layers.json` (keys, related keep rows), `docs/TESTING.md` §Правило/§Бюджет, the finding file, the brief,
  `docs/SIBLING_MAP.md` (grep).
- The live run: `C:\QAFactory\mybooks-stand\arm-factory\test-automation-framework\qa-factory\artifacts\LOCAL-1`
  (`test-plan.md`, `work/test-plan.json`, `work/test-cases/**`).
- R1: `( cd <worktree> && python -B -m pytest ai-packages/qa-factory/scripts/tests/test_plan_row_id_forms.py -q )` →
  `10 passed in 3.38s`.
- R2: an inline probe of the old regex against both new regexes, on the 39 live case files and 27 edge strings →
  `39 files; CRLF files: 0`, reads `P-1..P-10`, none in `critic-findings.md`. Old→new losses: `Plan row:\nTS-3`, NBSP before
  the label. Newly read garbage: REQ-1, R-3, UTF-8, e2e-1, S5-2, p-1.
- R3: `grep -rn -i "plan row:" scripts/tests --include=*.md` → 382 lines, 0 not `Plan row: TS-n`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F1: scripts/tests/test_plan_row_id_forms.py has no row in test-layers.json while enforce_listing is true; selftest._listing_ok (:737-740) emits 'tests: unlisted' as FAIL, so the CI canon goes red"
  ],
  "fixes": [
    "F1 (blocks): move the rows into test_case_id_form.py (table layer, already covers contract.py), or add the keep row {layer: data_join, why: case Plan row -> Controller._case_rows / s5_precheck.case_plan_row joined in the plan's own id form (FV1-1), covers: contract.py, controller.py, s5_precheck.py}",
    "F2 (before merge): one home for the id-token grammar - s5_precheck.py:79 builds PLAN_ROW_RE from a contract constant instead of a pasted copy of contract.py:3052; correct the commit's AR-13 line, which claims a single reader while six others exist",
    "F3 (before merge): s5_precheck.py:76-78 comment still says TS-n and claims contract.case_levels reads front-matter plan_row (it does not; contract.py:2096 docstring repeats it)",
    "F4 (proposed node, Lead of live-run-fvf decides): one plan-row id and one reader - S3 exit check that JSON row ids equal the md TS column; md-plan readers (case_levels/plan_levels, traceability.plan_by_ts, check_delivery._case_map and TS_IN_TEXT, report_facts:4472, handoff_check:399, validate_artifacts:806, grounding_table:1474) and the any-form readers (question_register:1416, gate_brief:2484, brief_pack:66) through one reader; new SIBLING_MAP axis. This run's S8 trace shows empty level and shape for every case until case_levels/plan_by_ts join P-n"
  ],
  "class_completeness": "Not complete, queue proposed: seven readers of a case's plan row with four grammars, and an md plan keyed TS-n beside a JSON plan keyed P-n in this run. The diff widens two readers (contract, s5_precheck); the TS-only md-plan family (case_levels, traceability, check_delivery, report_facts, handoff_check, validate_artifacts, grounding_table) stays. No SIBLING_MAP axis covers it, so a new axis is proposed. Goes to the Lead as node F4.",
  "trail": {
    "read": [
      "git show bb2bd10",
      "ai-packages/qa-factory/scripts/contract.py",
      "ai-packages/qa-factory/scripts/s5_precheck.py",
      "ai-packages/qa-factory/scripts/branch_accounting.py",
      "ai-packages/qa-factory/scripts/gate_preflight.py",
      "ai-packages/qa-factory/scripts/planning_contract.py",
      "ai-packages/qa-factory/scripts/manifest_from_tests.py",
      "ai-packages/qa-factory/scripts/question_register.py",
      "ai-packages/qa-factory/scripts/gate_brief.py",
      "ai-packages/qa-factory/scripts/brief_pack.py",
      "ai-packages/qa-factory/scripts/handoff_check.py",
      "ai-packages/qa-factory/scripts/traceability.py",
      "ai-packages/qa-factory/scripts/check_delivery.py",
      "ai-packages/qa-factory/scripts/controller.py",
      "ai-packages/qa-factory/scripts/selftest.py",
      "ai-packages/qa-factory/scripts/tests/test-layers.json",
      "ai-packages/qa-factory/scripts/tests/test_plan_row_id_forms.py",
      "docs/TESTING.md",
      "docs/tasks/critic-diff-brief.md",
      "docs/SIBLING_MAP.md",
      "plans/piles/live-run-fvf/findings/20261112-s5-pustaya-oblast-p-n-protiv-ts-n.md",
      "mybooks-stand arm-factory LOCAL-1: test-plan.md, work/test-plan.json, work/test-cases/**"
    ],
    "reruns": [
      {"command": "python -B -m pytest ai-packages/qa-factory/scripts/tests/test_plan_row_id_forms.py -q (in the worktree)", "result": "10 passed in 3.38s"},
      {"command": "inline probe: old vs new CASE_PLAN_ROW_RE and s5 PLAN_ROW_RE over 39 live case files and 27 edge strings", "result": "39 files, CRLF 0, P-1..P-10 read; losses only next-line id and leading NBSP; newly read garbage REQ-1, R-3, UTF-8, e2e-1"},
      {"command": "grep -rn -i 'plan row:' scripts/tests --include=*.md", "result": "382 lines, 0 not of the form Plan row: TS-n"}
    ]
  }
}
```
