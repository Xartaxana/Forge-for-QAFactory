# FV2-2 code critic - the `code_fills` label by contract and full field path

Diff: `C:\QAFactory\forge-repo\.claude\worktrees\fv2-2`, branch `wip/fv2-2`, commit `912c4ae` over `7cf8c34`.
Spec/DoD: `docs/tasks/specs/20261113-fv2-2-label-by-field-path-spec.md`. Report:
`.claude/worktrees/fv2-2/docs/tasks/specs/reports/20261113-fv2-2-report.md`.

**Verdict: fit_with_fixes. 0 blocking findings, 3 small fixes for this node's fix round (N1, N4, N5), the other notes are for the record or the Lead's queue.**
The decision to accept stays with the Lead (critic rule 6).

## Control runs (verbatim tails)

Base tree extracted by `git archive 7cf8c34 ai-packages/qa-factory` into the scratchpad. Both runs were launched in parallel:

```
# BASE 7cf8c34: python -B <scratch>/base/ai-packages/qa-factory/scripts/tests/test_field_producers.py
FAIL unknown row: obligation_refs <- manifest_from_tests@csharp -> window_record.row_field_gaps is not a row of this walk; rename it to the walk's id or remove it
FAIL unknown row: obligation_refs <- manifest_from_tests@java -> window_record.row_field_gaps is not a row of this walk; ...
FAIL unknown row: obligation_refs <- manifest_from_tests@python -> window_record.row_field_gaps is not a row of this walk; ...
FAIL unknown row: obligation_refs <- manifest_from_tests@typescript -> window_record.row_field_gaps is not a row of this walk; ...
FAIL known_red: the red rows of the walk are exactly the ledger — 4 problems
known red rows 25, not in world rows 47, rows walked 901
=== test_field_producers: 911/916 ok ===
exit 1

# DIFF 912c4ae: python -B <WT>/ai-packages/qa-factory/scripts/tests/test_field_producers.py
(the same four FAIL unknown row lines + the same aggregate)
FAIL known_red: the red rows of the walk are exactly the ledger — 4 problems
known red rows 22, not in world rows 47, rows walked 898
=== test_field_producers: 908/913 ok ===
exit 1
```

Diff of the two outputs, `ok`/`PASS` lines dropped:
```
< forms 24, variants 434, fields 980, unfillable 8, literal 7, left_for_code 82, kept_in_contract 9
> forms 24, variants 434, fields 980, unfillable 8, literal 7, left_for_code 79, kept_in_contract 9
< KNOWN RED derive: s3-strategist-to-designer:inputs_read[0].requirements — the deriver returned nothing ...
< KNOWN RED derive: s3-strategist-to-designer:scope[0].requirements — the deriver returned nothing ...
< KNOWN RED derive: s8-bug-reporter-to-scribe:filed[0].requirements — the deriver returned nothing ...
< known red: derive: s3-strategist-to-designer:inputs_read[0].requirements -> FV2-2
< known red: derive: s3-strategist-to-designer:scope[0].requirements -> FV2-2
< known red: derive: s4-designer-to-case-critic:scope[0].plan_row -> FV2-1
< known red: derive: s4-designer-to-runner:scope[0].plan_row -> FV2-1
< known red: derive: s8-bug-reporter-to-scribe:filed[0].requirements -> FV2-2
> known red: derive: s4-designer-to-case-critic:scope[0].plan_row -> FV1-14
> known red: derive: s4-designer-to-runner:scope[0].plan_row -> FV1-14
< known red: plan-row: s4.scope[].plan_row -> handoff_check._plan_row_of -> FV2-1
> known red: plan-row: s4.scope[].plan_row -> handoff_check._plan_row_of -> FV1-14
< known red rows 25, not in world rows 47, rows walked 901
> known red rows 22, not in world rows 47, rows walked 898
```
The new-tree output also holds `PASS derive: s4-designer-to-case-critic:scope[0].requirements` and
`PASS derive: s4-designer-to-runner:scope[0].requirements` (the code-filled control is still met).

```
# python -B <WT>/.../tests/test_handoff_values_refusal.py
=== test_handoff_values_refusal: 6510/6510 ok ===
exit 0
(42 lines "K-A20 _code_fills|skeleton|guard": 27 + 7 + 8; the builder's "47 K-A20 rows" also counts the 5 older "K-A20:" checks)
PASS K-A20 guard: s3 scope requirements refused
PASS K-A20 guard: s3 inputs_read requirements refused
PASS K-A20 guard: s8 filed requirements optional, not refused
PASS K-A20 guard: s8 filed requirements optional, not refused: the row was opened (the control)
PASS K-A20 guard: s4c requirements forgiven (code's)
PASS K-A20 guard: s4c requirements forgiven (code's): the row was opened (the control)
PASS K-A20 guard: s4c plan_row forgiven (code's)
PASS K-A20 guard: s4c plan_row forgiven (code's): the row was opened (the control)

# python -B <WT>/.../tests/test_handoff.py
=== test_handoff: 610/610 ok ===
exit 0
PASS the plan row comes from the case's own `Plan row:` line
PASS BY_PATH names a field of its contract: s4-designer-to-case-critic:scope[].requirements
PASS BY_PATH is not shadowed by DERIVERS: s4-designer-to-case-critic:scope[].requirements
PASS BY_PATH names a field of its contract: s4-designer-to-runner:scope[].requirements
PASS BY_PATH is not shadowed by DERIVERS: s4-designer-to-runner:scope[].requirements
PASS BY_PATH names a field of its contract: s4-designer-to-case-critic:scope[].plan_row
PASS BY_PATH is not shadowed by DERIVERS: s4-designer-to-case-critic:scope[].plan_row
PASS BY_PATH names a field of its contract: s4-designer-to-runner:scope[].plan_row
PASS BY_PATH is not shadowed by DERIVERS: s4-designer-to-runner:scope[].plan_row

# python -B <WT>/.../tests/test_judgment_census.py
=== judgment_census: 24/24 ok ===
# python -B <WT>/.../scripts/selftest.py --lang
=== qa-factory selftest: 2/2 ok ===
# git diff --stat 7cf8c34..912c4ae -- .../fixtures/judgment-census.json   -> (empty: census untouched)
# added lines of the package diff, non-ASCII count -> 0
```

Adversarial label probe (a pure read, `python -B -c` importing `<WT>/scripts/handoff_check`):
```
'' 's4-designer-to-case-critic' False
'scope[0].changed[1].requirements' 's4-designer-to-case-critic' False
'scope[0].requirements' ' s4-designer-to-case-critic' False
'scope[].requirements' 's4-designer-to-runner' True
'scope[0].requirements' 's4-case-critic-to-designer' False
'scope[0].case_version' 's3-strategist-to-designer' True
'inputs_read[1].requirements' 's3-strategist-to-designer' False
```

## Answers by id

### 1. K1-K8
- **K1**: cannot be met as written. My base run shows that **all 5 FAILs are already on base 7cf8c34**: the four
  `unknown row: obligation_refs <- manifest_from_tests@{csharp,java,python,typescript}` lines plus the **5th, the aggregate
  `FAIL known_red: ... 4 problems`**. This diff adds no FAIL. The only differences are the expected ones: 3 rows leave the
  walk, 3 rows are re-attributed, the count goes 25 -> 22 and `left_for_code` goes 82 -> 79. Every other part of K1 holds.
  No `derive: s3-...requirements` / `derive: s8-...requirements` line is printed, the three FV1-14 lines are present, and both S4
  `requirements` derive rows PASS. The spec's absolute counts (29/26) were written against `wip/fv2-1 a60160e`. The base is now
  `origin/main 7cf8c34`, and `git merge-base --is-ancestor a60160e 7cf8c34` succeeds. The relative delta (-3) is exactly what
  the spec asked for. See N2 and N6.
- **K2**: met. 6510/6510, and every T1/T2/T3 row id passes. T3 has a test-side deviation, discussed in Q3.
- **K3**: met. 610/610, the T4 rows are present, and the F-3 fixture was moved (`Plan row: TS-3` body line).
- **K4**: met. See Q4.
- **K5**: met by my own Grep (case-insensitive, over the whole worktree). `BY_LEAF` appears only in the report and in two old
  report files under `docs/` (not under `scripts`). `_by_path(` is found at `handoff_check.py:622`, `:1568`, `:2753` and
  `test_field_producers.py:107`, which is the positive control. `rsplit(".", 1)[-1] in` no longer appears in `_code_fills`
  (`handoff_check.py:2743-2755`).
- **K6**: met. 24/24, census file untouched.
- **K7**: met. 2/2, and the added lines are 0 non-ASCII.
- **K8**: I re-ran only the K-files above. The builder's tails for the other witness files (init 23/23, inline 83/83, keys
  103/103, main_block 47/47, null_outcomes 337/337, words_carry 207/207, knowledge_notice 15) agree with a diff that touches
  only label call sites. No inconsistency was found.

### 2. Edges E1-E10 and §5
| edge | verdict | evidence |
|---|---|---|
| E1 | as written | T1 rows `s3 scope requirements` False and `s4c/s4r scope requirements` True; BY_PATH `handoff_check.py:614-619` |
| E2 | unchanged, no refusal added | the `values_report` filter `:2921` has the same shape, now path+contract; `check`'s finish-time blank refusal is untouched; T3 `s4c ... forgiven` |
| E3 | as written | T1 `form with no such leaf` False; the Grep of `handoffs/` for the three leaves (anchored, case-insensitive) finds exactly the 12 occurrences of spec §2.2 |
| E4 | as written, no refusal added | T2 `s8 filed offers requirements` present; T3 `s8 ... optional, not refused` plus a control that the row was opened |
| E5 | holds by construction | the label is computed at read time from the form's own `contract:` (`:2906`, `:2730`, `:3067`); nothing persisted |
| E6 | as written | ledger edit in the same commit (Q4); the reconcile is green on these rows |
| E7 | as written | `:1568` `DERIVERS.get(generic) or _by_path(contract, generic)`; T4 shadow rows PASS |
| E8 | holds | the branches are OR'ed (`:2751-2755`) |
| E9 | holds; **one row is missing** | `_by_path(None/"")` gives None (T1 rows `unknown`/`absent contract`). `_code_fills("", c)` is False by my probe, but no table row covers it (N4) |
| E10 | as written | `scope[].case_version` stays a DERIVERS key; T4 `check_in(... "scope[].case_version", H.DERIVERS)` |
| §5 | all 15 rows present in T1 with the spec's expected values | `test_handoff_values_refusal.py:227-245` |

### 3. Divergence 3 of the report (the question's "divergence 2"): T3
The changed test still tests the spec's behaviour, and it discriminates. A template's placeholder-only row is not a row. Through
`only_template` / `_is_empty_section` (`handoff_check.py:1520`), the check reports the SECTION (`scope: no rows`), never
`scope[0].requirements`. So the spec's T3 with only `header.verdict: ok` can never name the path, under either the old code or the
new. The builder writes the row's id (`scope[0].id: P-1`, `filed[0].draft: D-1`, `scope[0].id: TC-1`), and the row's blank fields
are then judged per field. Under the OLD leaf code, `s3 scope requirements refused` and `s3 inputs_read requirements refused`
would be red, because `_code_fills` would forgive them. So the rows prove the fix. The "not refused" rows carry a control
(`scope[0].state` / `filed[0].bug` named), so they cannot pass vacuously because the row was never opened.

This was a spec defect, and the fix does not paper over it. The right statement of T3: "the values text writes the row's id field
(the list's first key) so that row 0 is a real row and its blank fields are judged one by one. A template-only row is judged as
`<section>: no rows`. For each 'not refused' row, a sibling role field of the same row (`.state` / `.bug`) must be named, to prove
the row was judged." The report's wording "the templates hold no row" is imprecise (N3): the S3 template has a placeholder
`scope` row (`handoffs/s3-strategist-to-designer.yaml:51-59`).

### 4. Divergence 2 of the report (the question's "divergence 3"): ledger rows 55/75/76
These rows are within owns (`form-rounds.json` is on `owns:`). They are correct: the node is `FV1-14`, each `raised_by` is the
old text unchanged with `; re-attributed to FV1-14 by the Lead 2026-11-13 (FV2-1 report)` appended, and the notes match K4
character for character for `:55` and for `:75`/`:76`. The three FV2-2 rows are removed. No other row changed (the diff hunk
touches only these 6 lines), the pins are unchanged, and the text is ASCII. The base carried `FV2-1` rather than the spec's
implied state, and the report states this.

### 5. Wrong label by path?
The table: `handoff_check.py:614-619` has 4 keys, all S4-designer case rows. The lookup `_by_path` (`:622-625`) is an exact
dictionary match on `<contract>:<INDEXED-generalised path>`. This means:
- **Code's field labelled the role's (the allowed direction)**: possible only for a contract string that differs from the
  handoffs file id. The id is read from the form's own `contract:` (`:2906`), the same value that `handoff.spec(contract)` uses,
  so a mismatched id would break the spec lookup first. There is no live instance: the Grep of `handoffs/` shows that every
  `requirements`/`plan_row` leaf is either in BY_PATH or one of the 3 role paths, and every `case_version` is a DERIVERS key.
- **Role's field labelled code's (the forbidden direction)**: not reachable through BY_PATH. Adversarial inputs: a nested list
  index `scope[0].changed[1].requirements` gives False; an absent path `inputs_read[0].requirements` on s4c gives False (T1); an
  empty path `''` gives False (probe); a padded contract `' s4-designer-to-case-critic'` gives False; the sibling S4 critic form
  `s4-case-critic-to-designer` gives False. The one True on a foreign contract is
  `('scope[0].case_version', 's3-strategist-to-designer')`: DERIVERS stays contract-blind. That path is not in the S3 spec, so
  nothing ever asks it, and it is the same class as the spec's analogs A-1/A-2 (N7), outside this node's scope.
- The remaining inherent case is E2: an S4 `requirements` on a case with no `covers:` is labelled code's while the deriver gives
  None. The spec keeps it deliberately; it is non-silent at `finish`.

### 6. Duplication, code quality, class completeness
- DUPLICATION AND CONSISTENCY: none found that blocks. I grepped `_code_fills(`, `BY_LEAF`, `_by_path(`, `row_form(`,
  `_row_lists(` and `_nested_rows(` over the worktree (case-insensitive). All production readers pass the contract: handoff_check
  at `:1512`, `:1522`, `:1568`, `:2207`, `:2226`, `:2270`, `:2306-2310`, `:2322`, `:2814`, `:2921`, `:2967`, plus
  `handoff_init.py:105`. The tests pass it at `form_filler.py:316,318,326` and `test_field_producers.py:107,545,1393`. One
  helper (`_by_path`) serves `check`, `_code_fills` and the test walk (AR-13). `_code_fills` generalises the path and `_by_path`
  generalises it again; this is idempotent and harmless. Four test calls still call `row_form` without `contract`
  (`test_handoff_values_refusal.py:529`, `:531`, `:867`, `:876`). The default `""` errs toward the role, and none of their
  assertions depends on the label (N8, no fix needed).
- CODE QUALITY: no new function over 60 lines and no deep nesting. **N1**: a leftover duplicate comment at
  `test_handoff_values_refusal.py:220-221` (`# the one answer` directly followed by `# the one answer, by contract and full path`).
  Fix before merge: delete `:220`. The T3 control's ternary `.state if contract == s4c else .bug` (`:272-273`) is tied to the
  current row set. It is acceptable, but any added row (for example s4r, N5) must extend it.
- Axis 5 (S4 designer twins): BY_PATH has identical rows for both twins, and T1/T2 cover both. T3 (the guard path) covers
  `s4c` only, as the spec's T3 listed. **N5**: add the two `s4r` guard rows (`scope[0].requirements` / `scope[0].plan_row`
  forgiven) so that the twin is proven on the guard path too. The cost is two table rows.
- L1-L5 of spec §2.1 have all moved: L1 BY_LEAF became BY_PATH, L2 `_code_fills:2753`, L3 `check:1568`,
  L4 `test_field_producers.py:107`, L5 `test_handoff.py` T4. Axis 18: the ledger only shrank (25 -> 22) and `not_in_world` stays
  47. Axis 32: the census is untouched. Axis 34: one table read by one function for every contract; the per-contract key is a
  data row, not a branch. A-1..A-5 are reported in the report with verdicts, not widened.

### 7. AR-10, AR-13, AR-22, AR-28, AR-29; JUDGMENT
- AR-22: the producer (BY_PATH, `_code_fills`) and all readers change in one commit, including `form_filler` and the walk.
- AR-13: one lookup, `_by_path`, with no leaf re-derivation left in the label path.
- AR-10: T2 proves the skeleton offers `scope[0].requirements` / `inputs_read[0].requirements` (S3) and `filed[0].requirements`
  (S8). T3 proves the guard names the two required S3 paths.
- AR-28: empty, None, case-different and padded contracts all give False (T1 plus my probe).
- AR-29: the only behaviour change is presence (blanks refused on two more S3 paths), with the census unchanged.
- JUDGMENT (question 11): no new check judges meaning. Code never inspects whether an R-id list or a count is right, and the
  `judgment:` line of the commit says so.

## Other notes (non-blocking)
- **N2**: the base deviation is not listed among the report's deviations. The spec's base is `wip/fv2-1 a60160e`; the builder
  used `origin/main 7cf8c34`. a60160e is an ancestor (checked), so no FV2-1 content is missing; only the absolute counts moved.
  This is a report line, not a code fix.
- **N3**: the report's T3 wording "the templates hold no row" should read "the templates hold only a placeholder row, judged as
  an empty section". Report only.
- **N4**: add the E9 row `("empty path", "", s4c, False)` to the T1 table (`test_handoff_values_refusal.py:227-243`). The spec
  names this edge in E9; it is not in §5's table, so this is a small gap rather than a DoD miss.
- **N6 (for the Lead's queue, not this node)**: the four stale `obligation_refs <- manifest_from_tests@*` ledger rows
  (`form-rounds.json:68-71` on base) keep `test_field_producers` red on `main` itself. Owner by row: FV1-19 (csharp, java,
  typescript), FV1-1 (python). K1 of every node that touches this ledger stays unreachable until a node removes them. I propose
  that the Lead opens that node (critic rule 6: the decision is the Lead's).
- **N7**: DERIVERS keys are contract-blind (`_code_fills("scope[0].case_version", s3)` gives True). This is not live (the path is
  not in S3's spec) and is the same class as analogs A-1/A-2, which are already reported.
- **N8**: see Q6. Four test call sites of `row_form` without `contract`; no fix needed.

## Trail
Read: the spec (whole); the builder report (whole); `git diff 7cf8c34..912c4ae -- ai-packages/` (whole); the commit message of
912c4ae; `test_handoff_values_refusal.py:1-30`, `:195-275`, `:850-881`; `handoff_check.py:2885-2924` and Greps for
`_Outcome`, `contract = ...get("contract")`, `INDEXED`, `BY_PATH`, `only_template`; `handoffs/s3-strategist-to-designer.yaml:30-59`;
a Grep of `handoffs/` for the three leaves (anchored, `-i`); `docs/SIBLING_MAP.md` axis heads; `docs/tasks/critic-diff-brief.md`
items 6, 7, 11, 12; `tools/critic_verdict.schema.json`.
Reruns: test_field_producers on base and on the diff, test_handoff_values_refusal, test_handoff, test_judgment_census,
selftest --lang, the adversarial probe, the non-ASCII count, and `merge-base --is-ancestor a60160e 7cf8c34`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "L1-L5 of spec 2.1 all moved (BY_PATH handoff_check.py:614, _code_fills:2753, check:1568, test_field_producers.py:107, test_handoff T4); every production reader of the label passes the contract; axis 5 twins identical in BY_PATH and T1/T2, guard row for s4r missing (N5); axis 18 ledger shrank 25->22, not_in_world 47; axis 32 census untouched; axis 34 one table one reader; analogs A-1..A-5 reported, DERIVERS contract-blindness (N7) is A-1/A-2 class; stale obligation_refs rows (N6) queued to Lead.",
  "fixes": [
    "N1 test_handoff_values_refusal.py:220 delete the leftover duplicate comment '# the one answer'",
    "N4 add T1 row ('empty path', '', s4c, False) for edge E9",
    "N5 add T3 guard rows for s4-designer-to-runner scope[0].requirements and scope[0].plan_row forgiven, extending the control ternary at :272-273",
    "N2/N3 report: list the base deviation (7cf8c34 instead of a60160e, ancestor verified) and correct the T3 wording to 'placeholder-only row judged as an empty section'"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-fv2-2-label-by-field-path-spec.md",
      ".claude/worktrees/fv2-2/docs/tasks/specs/reports/20261113-fv2-2-report.md",
      "git diff 7cf8c34..912c4ae -- ai-packages/ (whole) and commit message 912c4ae",
      "ai-packages/qa-factory/scripts/tests/test_handoff_values_refusal.py:1-30,195-275,850-881",
      "ai-packages/qa-factory/scripts/handoff_check.py:2885-2924 plus greps BY_PATH/_by_path/_code_fills/row_form/only_template/_Outcome",
      "ai-packages/qa-factory/handoffs/s3-strategist-to-designer.yaml:30-59; grep of handoffs/ for requirements|plan_row|case_version",
      "docs/SIBLING_MAP.md axis heads; docs/tasks/critic-diff-brief.md items 6,7,11,12; tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B <scratch>/base(7cf8c34)/.../test_field_producers.py", "result": "911/916 ok; 4 FAIL unknown row obligation_refs + 1 aggregate; known red rows 25"},
      {"command": "python -B <WT>/.../test_field_producers.py", "result": "908/913 ok; the same 5 FAILs; known red rows 22; S4 requirements derive rows PASS; three FV1-14 lines present"},
      {"command": "python -B <WT>/.../test_handoff_values_refusal.py", "result": "6510/6510 ok, 42 K-A20 table lines PASS"},
      {"command": "python -B <WT>/.../test_handoff.py", "result": "610/610 ok, T4 rows PASS"},
      {"command": "python -B <WT>/.../test_judgment_census.py", "result": "24/24 ok"},
      {"command": "python -B <WT>/.../selftest.py --lang", "result": "2/2 ok"},
      {"command": "adversarial _code_fills probe (python -B -c, read-only)", "result": "empty path, nested index, padded contract, sibling S4 critic: False; s3 case_version True via contract-blind DERIVERS (N7)"},
      {"command": "git merge-base --is-ancestor a60160e 7cf8c34", "result": "true"}
    ]
  }
}
```
