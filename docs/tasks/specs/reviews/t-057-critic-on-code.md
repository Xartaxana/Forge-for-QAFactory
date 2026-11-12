# t-057 PC2-7 (package-ci/2) — critic on CODE

Scope: `git diff` of `scripts/contract.py`, `scripts/story_run.py`, `scripts/tests/test_story_sides.py`,
`docs/tasks/specs/t-2181-pre-code-and-one-side-runs.md`, plus the untracked
`changelog.d/package-ci-2-implicit-product-side.md`. Spec: t-043 §«The node as it stands after the plan critic» (B5-B8, B2-B4')
and t-043-critic-on-plan §«F-2 (b) as the node's condition» ((b)2-(b)5, test table, K-b1, K-b2).

**VERDICT: ACCEPT WITH FIXES** — 0 blocking findings in the code; 2 fixes for this round (one is the Lead's own doc lines,
one a single assertion), 7 non-blocking items (3 to queue). The acceptance decision belongs to the Lead.

## 1. Fit to the node

Helper `contract.product_implied` (`contract.py:5697-5708`): `not any(isinstance(e, dict) and e.get("reality") == "real" and
e.get("deliverable") is not False)`. Traced against the rule (B5 variant) and edge table (b)4, then checked by a control run
(§Control runs, verbatim):

| input | result | rule says | ok |
|---|---|---|---|
| `{}` / `None` / a list | True | True on `{}` (spec (b)5); non-dict sides read as none | yes |
| non-dict entry `{"ui": "real"}` | True | not real | yes |
| reality missing / `""` | True | unknown is not real | yes |
| real, `deliverable` False | True | another team's: not this team's | yes |
| real, `deliverable` None / absent / `"false"` / `0` | False | non-bool or absent reads this team's | yes (see N2) |
| another team's real + substituted (`other-team-real`) | True | variant: implied | yes |
| this team's real + substituted (`real-side-named`) | False | not implied | yes |
| this team's side substituted only | True | implied | yes |
| `product` already named (absent) | True, but `setdefault` keeps the named one (`story_run.py:8564`) | person's word wins | yes |

Call sites:
- `s0_sides_sets` (`story_run.py:8561-8564`): after the S13 `if not entries: return sets`, before `setdefault`, over the merged
  `entries` of `_sides_entries` (registry + launch + not-built-yet + reference + answers, `:8468-8489`). Correct. Unknown
  registry sides are already left out of `entries` (`:8470-8471`), so "unknown is not real" holds twice.
- `sides_reread` (`:18224`): over `read["sides"]`, not the filtered `entries` (`:18220-18222`) — as (b)2 demands. The default
  carries `"source": "default"` (`:18225-18226`) and the loop writes `row["source"]` (`:18228`); every registry row has
  `source: "registry"` from `registry_sides.side()` (`contract.py:5732-5733`), so no KeyError and K-b2 holds: the written
  attributes equal S0's (`reality real, deliverable "true", source default, at`; `settles_by ""` and `reference None` are skipped
  by `:18231`, `:18233`).
- `story_sides` registry branch (`contract.py:5686-5687`): `out = {}` only when `not product_implied(read["sides"])`. Correct.

`product_rows`: gone from `registry_sides` output, docstring, the set line and the except branch (`contract.py:5714`, `:5719`,
`:5780`), from `_sides_entries` docstring and return (`story_run.py:8458`, `:8490`), from both conditions. Own `git grep -i`
(rerun below): only `finalize_task.py:526, :531, :623` (unrelated local). `product_implied`: 1 definition, 3 callers + 1 docstring
mention. Matches the builder's K7 witness.

## 2. Does `test_no_mr_entry.py:436-438` turn green, file unedited — YES (by reading)

Traced on the new code, story `PROJ-1`, traced mode (`test_no_mr_entry.py:423-438`):
1. `s0_run --side backend=substituted`: `_sides_entries` — registry empty → `{backend: substituted, source launch}`; no
   `deliverable` → `s0_write_sides` stops on `deliverable:backend` (`story_run.py:8520-8537`), exit 3, no `pipeline.json`.
2. `s0_answer "another team's"`: `_keep_sides_answer` keeps `launch.sides_answers = {backend: False}` and writes the registry row
   `backend {deliverable False, settles_by ""}`.
3. `_sides_entries`: registry gives `backend {real, deliverable False}` (`:8472-8474`); the launch overrides reality to
   `substituted` (`:8478-8480`); the answer sets `deliverable False, source person` (`:8485-8487`). Record owed (non-real).
4. `s0_sides_sets`: `product_implied({backend: substituted/False})` → True → `product {real, True, default}` → written as
   `deliverable "true"` → coerced. The check's three keys read `real / True / default`. GREEN.
`--no-trace`: step 2 writes no registry row; step 3 gives the same entries from the launch + answer; same result. This is exactly
the traced half of table row `own-answer` (`test_story_sides.py:298`), which the builder's 169/169 witness reports green — a
consistent second leg for the trace. The file itself was not run (non-goal; CI canon judges it).

## 3. The unsafe direction (AR-28) and what a story that gains `product` changes

- The helper never records a non-real or unknown side as real: it only adds `product` with reality `real`; every other entry is
  written as merged. Unknown sides keep `sides_unknown` (`story_run.py:8553-8560`), which makes every proof unknown
  (`ledger._proof`, `ledger.py:407-408`).
- Unscoped Thens: `ledger._resolved_about` (`ledger.py:373-385`) falls to the test's declared sides UNION the stamp's NON-real sides;
  a real `product` never enters that union, so gaining `product` cannot turn an unscoped Then green.
- Thens scoped to `product` (observation, not a defect): `_met_real` (`ledger.py:363-370`) needs `real` in BOTH the test's
  declaration and the stamp. Before, in the records the plan named (e.g. `test_story_sides.py` registry `backend` ours + launch
  substituted, :404-411 of HEAD), `product` was not a side → `about: product` was refused by C2/C11 or stayed `on_substitute`.
  Now `product` is a real side of the record, so a Then a role scopes to `product` CAN pass while this team's named side is
  substituted. That is the designed meaning ("the rest" of the story is `product`; the same as a first story before PC2-7), and
  whether a Then is scoped to the right side is role judgment judged by the S5 code critic / acceptance (AR-29) — not a code gap.
  Worth one line to the Lead because the owner's B5 answer is still open: the case "this team's only named side is substituted"
  implies `product` under BOTH wordings, so the owner's answer does not change it.
- Readers of a record that gains `product` — all additive, none refuses on an extra real side: `s5_precheck.check_sides`
  (`s5_precheck.py:2369-2370`: `product` real adds nothing to `non_real`; `sided` is already true via the non-default sources;
  `_sides_declared` `:2044-2046` refuses only names NOT in the record, so `product` becomes a legal name);
  `manual_evidence` C11 (`manual_evidence.py:567-575`: `about: [product]` becomes legal); `run_suite` stamp (`run_suite.py:668`,
  `product: real` in `sides_met`); `interim_packet` (`interim_packet.py:56`, `:80-81`: one more row `product real`); briefs
  (`brief_pack.py:882`, `:987`) name one more side. A record that LOSES `product` (reference-only, a real side of this team) makes a
  test/Then naming `product` a `sides-name-*` / C11 refusal with a door — the intended E-O2 behaviour, reachable only for stories
  recorded after the change (an existing `pipeline.sides` is never rewritten; `sides_reread` writes only when `pipeline.sides` is
  empty, `story_run.py:18218`).

## 4. Tests

- ONE table (`test_story_sides.py:290-353`), six rows, every label starts with the row id (and `(traced)` / `(no-trace)`); the
  traced/no-trace equality per row (`:352-353`). P16 condition met.
- Count consistency with the witness: rows give 7+7+5+5+5+6 = 35 checks; the folded block had 2 → +33; 136 + 33 = 169 = the
  witness. Consistent.
- Flips are edits in place with the variant's expectation: `:209` (`not in` → `in`, ui real deliverable False), `:229-231`
  (True → False, ui real deliverable None reads this team's), F6 `:482-483` (`not in` → `in`). Correct under B5 variant and B6.
- Folding HEAD :289-300 into `other-story-row`: both assertions kept — "not asked (exit 0, no block)" (`:330-331` with `row[3]`
  None) and `(SUBSTITUTED, False, "platform team")` (`:333-336`). Only the seeded `words` text changed (irrelevant to any check).
- `second-story` (`:336-350`): `product` whole and `backend` on `reality`/`deliverable` only — what B7 says; no `--no-trace`
  half, as the table note says.
- Discrimination before the fix (by reasoning, no red run attached): on HEAD code `own-answer` traced gets no `product`
  (`product_rows` True from the story's own answer) while no-trace gets one → both the `product` check and the equality fail.
  The table is not vacuous.
- Expectations come from the owner's rule (B5 variant, t-043 :324-329), not from the code (FR-58). `other-team-real` carries the
  variant pending the owner's answer.
- Nothing weakened. Gap: the re-read's new `source: default` (K-b2) is pinned by no assertion — see fix R2.

## 5. Architecture, rules, duplication, code quality

- AR-13 kept: the helper is a predicate over data returned by `registry_sides` / `_sides_entries`; no new read of the registry.
- AR-15 / AR-19 kept: one survivor for the condition, the S0 site and its twin `sides_reread` change together; residual
  divergence of the twins on their INPUTS — N1.
- AR-22 kept: `product_rows` lost every reader and is removed in the same diff (grep above); no new field read.
- AR-28 kept (§3). AR-29: the helper picks a default data row; refuses nothing; judges no role's output; census rerun 22/22.
- FR walk: A — no refusal text changed; B — no human text changed; C — FR-13: the only word compared is `real`, the
  side-realities data word already spelled the same way in `registry_sides` (`contract.py:5732`); FR-14: `registry_sides`'
  output shape changed (key removed) with all readers updated; D — FR-58 (tests from the rule), FR-59 (unknown is not real,
  `sides_unknown` kept); E — the report/packet gains or loses a side row only, no verdict meaning changed (FR-35); F — n/a;
  G — FR-30: Cyrillic count 0 in the package diff and the changelog (control: PROJECT.md 22574); FR-32: root cause (the condition)
  fixed with a test.
- DUPLICATION AND CONSISTENCY: (i) the default `product` entry is spelled twice in `story_run.py` (`:8564`, `:18225-18226`) while
  `contract.story_sides` takes the default from `references/side-realities.json` (`contract.py:5675-5679`) — pre-existing, the
  diff touched both lines; queue (N6). (ii) the copy-the-registry-to-PROJ-2 setup appears twice in the test (`:336-339` and
  `:562-565`) — non-blocking (N7). (iii) the late `import contract` in `s0_sides_sets` follows the file's convention (comment at
  `:8464`) — none. Grepped: `product_rows`, `product_implied`, `"product"` (-i) over `scripts/`, `story_sides\(` over `scripts/`.
  The clone-ratchet output was not attached — not re-derived.
- CODE QUALITY: no new function over 60 lines; the test table loop reaches 4 nesting levels inside `driver_cases` (`:322-350`) —
  acceptable for a table driver, no finding. One docstring line of 212 characters (`contract.py:5714`, the longest in the region;
  the rest ≤ ~140) — N3. Docstrings that now under-state: N2, N4.
- ONE ROAD (P31): the diff closes the two-road defect (own answer vs `--no-trace`, story 1 vs story 2). No exclusion added.

## 6. Class-wide completeness (axis 35 and inside the artifacts)

Class: "whether the implicit `product` is carried depends on something other than the story's merged sides".
- `s0_sides_sets` — fixed. `sides_reread` — fixed (condition + spelling). `story_sides(root=)` — follows.
- S5 hold `_side_not_ours`, arrival `side_set_args`, `not built yet` (`story_run.py:8158`, `:8482`, `:21698`) — set NAMED
  `product` only, apply no default: n/a.
- `s0_write_sides` `:8518` (`all(name == "product")`) — the question skip, not the default: n/a.
- Sweep of t-2181 (the artifact the diff edits): lines 280 and 696 — fixed; line 48 (S5 row: «`product` is not implied once any
  `product.sides` row exists») — OLD rule, not fixed; line 769 (the test list: «`product` not implied once a `product.sides` row
  exists») — OLD rule, not fixed, and not named by the builder. → fix R1. Line 416 («other than the implicit `product`») and 793
  — consistent with the new rule: n/a.
- `SIBLING_MAP.md` axis 35 (`:591-600`) names no rule for the implicit side and not the new helper — N5 (proposal).
- Inside the twins: `sides_reread` evaluates over the registry only, while S0 evaluates over registry + launch — N1.

## Fixes for this round (not blocking the code)

- **R1** — `docs/tasks/specs/t-2181-pre-code-and-one-side-runs.md` line 48 and line 769 still state «not implied once a
  `product.sides` row exists». Change both to the sentence already used at :280/:696 («`product` is implied when the story's sides
  (the registry's, the launch's and the person's answers merged) hold no real side of this team (PC2-7, t-043)»; at :769 the test
  item becomes «`product` implied beside another team's real side / not implied beside this team's real side»). The Lead's spec,
  outside the builder's owns — Lead edits.
- **R2** — `test_story_sides.py` F1 (a) block (`:413-431`): add one check that the re-read record carries
  `pipeline["sides"]["product"]` minus `at` == `{"reality": "real", "deliverable": True, "source": "default"}` (registry
  `backend` another team's + stand row substituted → no real side of this team). Today reverting `:18226`/`:18228` to
  `source: registry` fails no test; this also pins the S0/re-read twin spelling (AR-19). A fresh builder, one assertion.

## Non-blocking

- **N1 (queue, Lead opens the node)** — twin divergence on inputs: `sides_reread` (`story_run.py:18213-18226`) evaluates over the
  registry only; S0 over registry + launch. Input: launch `--side ui=real`, registry unreadable at S0 (→ `sides_unknown`, no record,
  `test_story_sides.py:396-404`); relaunch after the registry is repaired with `backend` another team's + stand `substituted`. S0 on
  the same inputs would record `{backend, ui}` and no `product` (ui real, this team's); the re-read records `{backend, product}`.
  Before PC2-7 both gave no `product` (a `product.sides` row existed). The loss of `ui` is pre-existing; the `product` difference is
  new. Fix: the re-read builds its entries through `_sides_entries(pipeline.get("environment"))` (one merge for both twins).
- **N2** — `product_implied` docstring «a value that is not a bool reads true, as `story_sides` reads it»: `story_sides` turns only
  `None` into True and keeps other values (`contract.py:5689`). Unreachable today (registry validates the bool,
  `contract.py:5738`; the driver writes `bool(ours)`), so wording only: «reads true (only `False` is another team's)».
- **N3** — rewrap `contract.py:5714` (212 characters).
- **N4** — `sides_reread` docstring (`:18203-18204`) says the recorded sides carry `source: registry`; add «and the implicit
  `product` (`source: default`) when `contract.product_implied`».
- **N5 (proposal)** — `SIBLING_MAP.md` axis 35, row «The reader»: name `contract.product_implied` as the one condition for the
  implicit side, shared by `story_sides`, `s0_sides_sets`, `sides_reread`.
- **N6 (queue)** — the default `product` entry is spelled in code at two driver sites while the reader takes it from
  `side-realities.json`; one builder in `contract` (e.g. `implied_product_entry()` from the data file) would close it.
- **N7** — the registry copy to PROJ-2 (`test_story_sides.py:336-339`, `:562-565`) could be one local helper.

## Control runs (verbatim)

`python -B -c` over `contract.product_implied` (scripts dir on sys.path):
```
empty True
not-a-dict True
None True
non-dict-entry True
reality-missing True
reality-empty True
deliv-False True
deliv-None False
deliv-absent False
deliv-str-false False
deliv-0 False
other-team-real+subst True
ours-real+subst False
ours-substituted True
product-named-absent True
reality-REAL-case True
```
`python -B ai-packages/qa-factory/scripts/tests/test_judgment_census.py | tail -3`:
```
PASS blind_spot_names_subclass_gap

=== judgment_census: 22/22 ok ===
```
`git grep -n -i "product_rows" -- ai-packages/qa-factory` → only `finalize_task.py:526`, `:531`, `:623`;
`git grep -n "product_implied" -- ai-packages/qa-factory` → `contract.py:5686, 5697, 5705`, `story_run.py:8546, 8563, 18224`.
Cyrillic count (python regex `[Ѐ-ӿ]`): `diff 0 changelog 0 control PROJECT.md 22574`.
Line length: `contract.py:5714` 212, max in `:5600-5800` 212.

## What I did not check

- No run of `test_story_sides.py`, `test_no_mr_entry.py`, `test_driver_layers.py`, `selftest.py --lang` (non-goals / builder's
  witness accepted by consistency: 136 → 169 matches +33 checks). The red-before of the new table is by reasoning only.
- The clone/lint ratchet outputs (not attached); `stage_done.coerce_value` for `sides.product.source=default` on the re-read
  `--set` path (S0 already writes the same key and value through it).
- `brief_pack.py` / `report_facts.py` text around the side rows beyond the call lines; the owner's answer to B5.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "R1: t-2181 spec lines 48 and 769 still state the old rule (not implied once a product.sides row exists); replace with the merged-sides rule already used at lines 280 and 696 (Lead's doc)",
    "R2: test_story_sides.py F1 (a) block: assert the re-read record's product minus at equals reality real, deliverable True, source default; today reverting the re-read to source registry fails no test (K-b2, AR-19 twin spelling)"
  ],
  "class_completeness": "Axis 35: s0_sides_sets and sides_reread share contract.product_implied and the default spelling; story_sides(root=) follows; product_rows removed with all readers; the S5 hold, arrival and not-built-yet sites set named product only (n/a). Residuals: t-2181 lines 48 and 769 (fix R1); sides_reread evaluates over the registry without the launch sides, a twin divergence on inputs (N1, queue for the Lead); SIBLING_MAP axis 35 does not name the helper (N5, proposal); the default entry spelled at two driver sites vs the data file (N6, queue).",
  "trail": {
    "read": [
      "docs/tasks/specs/t-043-pc2-7-implicit-product-side.md:317-370",
      "docs/tasks/specs/reviews/t-043-critic-on-plan.md:60-99,171-441",
      "docs/tasks/critic-diff-brief.md:47-86",
      "ai-packages/qa-factory/scripts/contract.py:5650-5783",
      "ai-packages/qa-factory/scripts/story_run.py:8456-8590,18180-18250",
      "ai-packages/qa-factory/scripts/tests/test_story_sides.py diff and 352-431",
      "ai-packages/qa-factory/scripts/tests/test_no_mr_entry.py:415-444",
      "ai-packages/qa-factory/scripts/ledger.py:363-413",
      "ai-packages/qa-factory/scripts/s5_precheck.py:2026-2056,2355-2390,4495-4524",
      "ai-packages/qa-factory/scripts/manual_evidence.py:555-579",
      "ai-packages/qa-factory/scripts/interim_packet.py:50-89",
      "ai-packages/qa-factory/changelog.d/package-ci-2-implicit-product-side.md",
      "docs/SIBLING_MAP.md:588-601",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B -c calls of contract.product_implied over 16 adversarial inputs", "result": "all 16 as the rule and edge table (b)4 say; output verbatim in the report"},
      {"command": "python -B ai-packages/qa-factory/scripts/tests/test_judgment_census.py", "result": "=== judgment_census: 22/22 ok ==="},
      {"command": "git grep -n -i product_rows / product_implied -- ai-packages/qa-factory", "result": "product_rows only finalize_task.py:526,531,623; product_implied contract.py:5686,5697,5705 and story_run.py:8546,8563,18224 - matches the builder's K7"},
      {"command": "Grep -i quoted product literal over scripts and not implied / implicit side over the repo", "result": "no other default site; t-2181 lines 48 and 769 keep the old rule"},
      {"command": "python regex Cyrillic count over the package diff and the changelog, control PROJECT.md", "result": "diff 0 changelog 0 control 22574"}
    ]
  }
}
```
