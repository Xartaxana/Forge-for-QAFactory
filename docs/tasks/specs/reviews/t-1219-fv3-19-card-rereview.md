# t-1219: plan re-review of the FV3-19 card (Lead decisions on t-1215)

critic (Opus) · node `live-run-fvf/3/FV3-19` · card `docs/tasks/specs/20261117-fv3-19-nested-null-outcome-card.md`, section "Lead decisions on the plan verdict t-1215" (lines 162-180, uncommitted)
Scope (dispatch edges): only that section, judged against B1, B2 and N1-N4 of t-1215. For each decision I asked three things: can a weaker model execute it, does it open a top-level verdict change outside the closed list, and does `inputs_read` as NE data reach every form that carries it. This verdict is an input to the Lead's acceptance. The decision belongs to the Lead.

## Verdict

**NEEDS WORK (fit_with_fixes): 2 blocking findings (R1, R2) and 3 non-blocking (R3-R5).** The measurement, the closed-list mechanism, the verdicts for the empty-legal lists, and N1-N4 are fixed. The two decisions that keep a list refused are fixed wrongly:
- `inputs_read` "joins the required set AS DATA". No data carrier makes a list required. The only required set is the code tuple `handoff.REQUIRED_LISTS`, which applies by section name to every contract. So six NE rows either refuse nothing and go red as stale, or, if the tuple grows, the rule reaches 15 contracts and breaks the W1 walk.
- `rounds` is given "an explicit null outcome with no conditional rule". The null-outcome grammar cannot express that. Under road B it also contradicts "untouched stays refused".

Both decisions also need files that §5 of the card lists as non-goals.

## Per finding of t-1215

| t-1215 | status | where (card line) |
|---|---|---|
| B1: measurement and closed list | fixed (with nit R4) | 166, 179 |
| B1: `inputs_read` ×6 | **fixed wrongly** (R1) | 168 |
| B1: s7 `rounds` | **fixed wrongly** (R2) | 169 |
| B1: s4-case-critic `findings`/`questions`/`register_gaps`; s8-scribe `questions` | fixed | 170-171 |
| B2: enumeration from the parsed template; `reasons_by_owner` ×4 | fixed | 172-173 |
| B2: `request.tried`/`request.data` | fixed on the NO branch; the YES branch inherits R1 (R5) | 174 |
| N1: signature and fallback | fixed (wording nit R3) | 176 |
| N2: filler reads `list_paths` minus REQUIRED_LISTS, plus an R10 row | fixed | 177 |
| N3: edge 4 sentence and a raw-scalar R row | fixed | 178 |
| N4: `person_question.options` stop withdrawn | fixed | 175 |

Correction to my own t-1215: I wrote "13 top-level lists" flip. probe3's `top=True` lines number **11**: 4 flip by recursion and 7 by F4-b. The decision's per-list verdicts cover all 11 (6 + 1 + 3 + 1), so this changes nothing in the card. The candidate I named in t-1215 ("joins the required set as data") was underspecified, and R1 is where that shows.

## Blocking findings

**R1 (blocking). `inputs_read` "joins the required set AS DATA (one NE row each in `null-outcomes.json`)" has no carrier. It also either refuses nothing or reaches 15 contracts, not 6.**
Surface: the required-list set (`handoff.REQUIRED_LISTS`) and its readers.
- The required set is code: `handoff.py:459` `REQUIRED_LISTS = ("scope",)`. It is read by name, for every contract, at `handoff_check.py:1661` (the refusal), `null_outcomes.py:566-577` (W1 walk), `null_outcomes.py:281` and `handoff.py:487,496` (which keys a null outcome may name), `form_filler.py:370` and `handoff_init.py:203`. It is pinned by `test_s7_null_outcome.py:463` ("REQUIRED_LISTS is unchanged: `scope`, and only it"). `handoff_check` never reads `null-outcomes.json` never_empty rows. An NE row is a HOME that the audit demands for an item the walk already met (`null_outcomes.py:656-662`). It does not create a requirement.
- Reading (i): the six NE rows alone, REQUIRED_LISTS unchanged. Then nothing refuses an untouched `inputs_read`. B1 stays open, and each of the six rows is red in the audit: `null_outcomes.py:666`, "stale row - the walk meets no scope `<carrier>`".
- Reading (ii): `inputs_read` is appended to REQUIRED_LISTS (as the card's own F3 alternative says, "opt it into REQUIRED_LISTS ... re-opens the grammar"). probe4 (below) shows that `inputs_read` is carried by **15** contracts, and the rule then reaches all of them:
  - W1 needs a home for every SCOPE_KINDS carrier. That is 14 contracts, and the decision supplies 6, so 8 are red "has no home" (`:659`).
  - `s8-scribe-to-gate-b` is index kind `report` (NO_SCOPE_KINDS) and carries `inputs_read`. W1 refuses it at `:576-577`: "kind report has no item list, and the contract carries `inputs_read`".
  - `s5-critic-to-automator` and `s5-critic-plan-to-automator` have an untouched `inputs_read` that is empty-legal TODAY (`today_empty=True`, an all-placeholder row; the init prefill replaces only `<the author's dispatch>`, `handoff_init.py:156-177`). They flip to refused. That is a top-level verdict change outside the closed list, and a written `inputs_read: []` would also start refusing on all 15. Under the decision's own premise ("MUST NOT be empty", P31), these two are siblings of the class. Under reading (i), they stay empty-legal without a word.
- The row sentence ("from the data row's own text, not a branch on the list name") names no reader, no field and no fallback. `handoff_check` has no reader of never_empty rows. Several of these carriers' `scope` homes are `pending` rows with no `requirement` text (`null-outcomes.json:147-153`). If the text comes from data for `inputs_read` only while `scope` keeps its fixed text, that is the branch the decision forbids.
- Executability: §5 (not overridden by the section) lists `null_outcomes.py` and `references/null-outcomes.json` as **non-goals**. Neither is in `owns`, and neither is `test_s7_null_outcome.py`. The §7 readers table says REQUIRED_LISTS stays `("scope",)`. The §5 siblings line says "axis 38: road B adds no refusal". A weaker model following §5 hits the owns wall, or invents the road. Both are a defect under PROJECT.md p.11.
- Fix (a fork for the Lead; my recommendation is first):
  - (A) One rule by name, P31: `REQUIRED_LISTS = ("scope", "inputs_read")`. Enumerate all 15 carriers with a verdict each (the probe4 table). Give homes for the 14 SCOPE_KINDS carriers (NE rows with a guard, e.g. `no guard: handoff_check.py::check refuses the empty list`). Settle the W1 rule for kind `report`: W1 must tell the item list `scope` from a proof-of-reading list. Add the two s5-critic flips and `[]` to the closed list. Write the row sentence without the words "in scope" for every required list, from `row_form` (already contract-derived), rather than a new data reader. Move `null_outcomes.py`, `null-outcomes.json`, `test_s7_null_outcome.py` and `test_null_outcomes.py` into `owns`. Rewrite the §7 row, the §5 siblings line (axis 38) and the DoD.
  - (B) Split `inputs_read` into its own node that lands before FV3-19 or in the same merge, so that road B never ships with `inputs_read` empty-legal.
  - Either way, "AS DATA" goes away: the requirement is the tuple.

**R2 (blocking). The `rounds` decision cannot be satisfied under road B, and the grammar cannot express it.**
Surface: the null-outcome declaration (`handoff.null_outcome_entries` / `_declared_null_outcomes`).
- A declaration with no `condition` is dropped (`handoff.py:500-504`). A declaration whose condition is not live is not applied, so the refusal stands (`handoff_check.py:1549-1559`). The only live condition is `triage_has_no_repair` (`null_outcomes.py:154-156`), and its params are triage verdicts and `listed_in`, which do not fit `rounds`. Every other registered condition is `reserved`, with `impl None`. So "an EXPLICIT null outcome ('no repair round') ... No conditional rule on `fix_result`" has no expressible form. The builder would have to register and implement a new live condition, which means inventing a road.
- The decision is also inconsistent in itself: "untouched stays refused, a role with no repair writes the declared null outcome". The values writer cannot write `[]`: `rounds: []` → "nothing written" (`handoff_check.py:2731-2732`, the card's own R9). So the form a role with no repair leaves IS the untouched template, and under road B (F4-b) that reads as empty. Untouched and declared-empty are one form state, so they get one verdict. The only thing that can tell "no repair happened" from "forgot the rounds" is a field other than the list. That is a conditional rule, for example `sibling_in` over `scope[].fix_result`, which is reserved at `null_outcomes.py:157`, and that is exactly what the decision forbids.
- Executability: the declaration lives in `s7-automator-to-analyst.yaml` ("sibling yamls" is a §5 non-goal). It needs `rounds` in REQUIRED_LISTS (R1's tuple, whose readers are listed there). It breaks `test_s7_null_outcome.py` S3 ("exactly one contract names a null outcome"), and with a new condition, the `registered conditions` pin. None of these is in `owns`.
- Fix (Lead fork):
  - (a) `rounds` is empty-legal like the s4 lists, with t-1215's risk written down: `fix_result: fixed` beside an untouched `rounds` passes. A finding opens a node for a live `sibling_in`-style condition.
  - (b) A live condition reading `scope[].fix_result` (empty `rounds` is legal iff no scope row says `fixed`). This is road A's machinery, so it is its own node with its own owns, sequenced before or with FV3-19.
  - (c) REQUIRED_LISTS with no null outcome. This is rejected: an automator whose every instance is `not_fixed` or `blocked_by_env` gets a dead end (FR-23, FR-57).
  - Recommendation: (b) as a separate node, with FV3-19 not merged before it, or (a) if the Lead accepts the priced risk. The decision as written is neither of these.

## Non-blocking findings

- **R3: the N1 fallback is labelled "the stricter side", and that is inaccurate.** `only_template(value)` with no template still recurses. Recursion alone is LOOSER than today's per-value `_is_empty_section` for the check-loop readers (probe1: 4 lists). For `:1872` (`tried`), "empty" means a refusal, so the direction inverts there. On the actual templates, the three no-contract callers read `scope`/`not_for_repair` (s7-analyst-to-automator, `:1421`, `:1610`) and `tried` (`:1872`), and none of those appears in probe1. So no verdict changes. Fix: say "no token rule; recursion as `only_template`". Pin it by noting that item 0's probe1 re-run shows those callers' lists unchanged, so the direction is not asserted.
- **R4: the "closed list below", which item 0 must reproduce EXACTLY, is not the full probe3 table.** probe3 prints 30 lines. The decision's verdicts name 11 top-level and 14 nested paths. It leaves out the five hint-declared paths (`witness_paths` ×4, `artifacts.probes`), which probe3 prints and which change nothing in practice. A weaker model re-running the walk gets 30 against 25 and stops. Fix: the closed list is t-1215 lines 37-66, verbatim. Mark those five "no practical change (row fields optional by hint)". For each refused path (`inputs_read`, `rounds`), state the expected problem code, `handoff_check:required_rows` (today it is `field.blank`).
- **R5: B2's YES branch for `request.tried` inherits R1** ("joins the required set as NE data", a dotted path that REQUIRED_LISTS, keyed by top-level name in `null_outcome_entries` and W1, cannot hold). This does not block: my case-insensitive Grep of `role-to-conductor|role_to_conductor` over the package excluding `tests/` finds only `handoff_help.py:96` as a script, plus README, index, vocabulary and the yaml itself. That reproduces t-1215's NO estimate. The NO branch is executable. Fix: make the YES branch "stop, a question to the Lead" until R1's road exists.

## Out-of-scope check (blocking only)

None beyond R1/R2. The rest of the card was not re-judged (non-goal).

## Standing questions

- DUPLICATION AND CONSISTENCY: R1's row-sentence "from the data row" would add a second source for refusal text beside `row_form`. I recommend `row_form` (one reader). Grepped: `REQUIRED_LISTS` over `scripts/` (14 hits, readers above), `_is_empty_section\(` (11 hits).
- CODE QUALITY: R3 (the direction label). Otherwise N1/N2/N3 name the signature, the reader and the rows.
- ONE ACTION, ONE ROAD (P31): R1. "MUST NOT be empty" applied to 6 of the 15 carriers by an NE row is an exclusion with no mechanism behind it. The tuple applies to all by name. The decision must choose the tuple and enumerate, or split the node.
- TESTS (budget): no change of shape: rows of one parameterised function. R1(A)/R2(b) add the existing `test_null_outcomes`/`test_s7_null_outcome` pins to owns. They are not new functions.
- CLASS COMPLETENESS: the empty-legal verdicts are complete for the 30 probe3 paths. The required-list side is incomplete: 15 carriers of `inputs_read` against 6 named. The two s5 critics are empty-legal today, and the decision leaves them unnamed.

## Trail

- Read: the card §2 (20-80), §5-§9 and both Lead-decision sections (82-180); t-1215 (whole); `handoff.py` 405-534; `handoff_check.py` 1221-1231, 1540-1559, 1600-1612, 1640-1709, 1865-1875, 2672-2680, 2726-2736; `null_outcomes.py` 137-178, 270-294, 545-614, grep `home|stale` (656-679); `null-outcomes.json` (whole); `handoff_init.py` 180-192 and grep `inputs_read`; `s7-automator-to-analyst.yaml` (whole); `test_s7_null_outcome.py` 455-468; `index.yaml` kinds (grep).
- Re-runs (verbatim):
  - `python -B <scratchpad>/probe3.py | wc -l` gives `30`, which matches t-1215's table.
  - `python -B <scratchpad>/probe4.py` (for every contract carrying `inputs_read`/`rounds`: index kind, today's `_is_empty_section` on the untouched template, and road B emptiness under F4-b):
```
inputs_read s2-tester-to-strategist kind=produce list=True today_empty=False roadB_empty=False
inputs_read s3-strategist-to-designer kind=produce list=True today_empty=False roadB_empty=False
inputs_read s4-case-critic-to-designer kind=review list=True today_empty=False roadB_empty=True
inputs_read s4-designer-to-case-critic kind=produce list=True today_empty=False roadB_empty=False
inputs_read s4-designer-to-runner kind=produce list=True today_empty=False roadB_empty=False
inputs_read s5-automator-to-runner kind=produce list=True today_empty=False roadB_empty=True
inputs_read s5-critic-plan-to-automator kind=review list=True today_empty=True roadB_empty=True
inputs_read s5-critic-to-automator kind=review list=True today_empty=True roadB_empty=True
inputs_read s6-runner-to-analyst kind=produce list=True today_empty=False roadB_empty=True
inputs_read s7-analyst-to-automator kind=review list=True today_empty=False roadB_empty=False
inputs_read s7-analyst-to-scribe kind=produce list=True today_empty=False roadB_empty=True
inputs_read s7-automator-to-analyst kind=produce list=True today_empty=False roadB_empty=True
inputs_read s8-bug-reporter-to-scribe kind=produce list=True today_empty=False roadB_empty=True
inputs_read s8-scribe-to-gate-b kind=report list=True today_empty=False roadB_empty=False
inputs_read s9-retro-to-project kind=ledger list=True today_empty=False roadB_empty=False
rounds s7-automator-to-analyst kind=produce list=True today_empty=False roadB_empty=True
REQUIRED_LISTS ('scope',)
```
  - Grep, case-insensitive, `role-to-conductor|role_to_conductor` over `ai-packages/qa-factory` with glob `!**/tests/**`: 6 hits. The only script is `handoff_help.py:96`. The positive control is the same call finding `role-to-conductor.yaml:17`, which it did.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "R1: inputs_read 'joins the required set AS DATA (one NE row each)' has no carrier: the required set is the code tuple handoff.REQUIRED_LISTS (handoff.py:459), read by name for every contract (handoff_check.py:1661, null_outcomes.py:566-577/281, handoff.py:487/496, form_filler.py:370, handoff_init.py:203), pinned by test_s7_null_outcome.py:463; NE rows are homes, not requirements. NE rows alone: no refusal and 6 stale rows red (null_outcomes.py:666). Tuple extended: reaches 15 carriers (probe4), 8 SCOPE_KINDS carriers homeless, s8-scribe-to-gate-b kind report red at null_outcomes.py:576-577, s5-critic and s5-critic-plan flip from empty-legal to refused outside the closed list; row-sentence source unnamed; null_outcomes.py and null-outcomes.json are section 5 non-goals, not owns",
    "R2: rounds 'explicit null outcome, no conditional rule on fix_result' is not expressible (no-condition entries dropped handoff.py:500-504; only triage_has_no_repair is live, others reserved, handoff_check.py:1549-1559) and is self-contradictory under road B: values 'rounds: []' writes nothing (handoff_check.py:2731-2732), so untouched and declared-empty are one form state with one verdict; telling them apart needs a sibling condition (sibling_in on scope[].fix_result), which the decision forbids; also needs s7-automator-to-analyst.yaml (non-goal) and breaks test_s7_null_outcome.py S3 pin"
  ],
  "fixes": [
    "R1: Lead picks (A) REQUIRED_LISTS = (scope, inputs_read) with all 15 carriers enumerated and given verdicts, homes for the 14 SCOPE_KINDS carriers, a W1 rule for kind report (s8-scribe-to-gate-b), the two s5-critic flips and written [] added to the closed list, a row sentence without 'in scope' built from row_form, and null_outcomes.py, null-outcomes.json, test_s7_null_outcome.py, test_null_outcomes.py moved into owns with the section 7 row, the section 5 siblings line (axis 38) and the DoD updated; or (B) split inputs_read into its own node merged before or with FV3-19; drop the phrase 'AS DATA'",
    "R2: Lead picks (a) rounds empty-legal with the priced risk written down and a finding for a live sibling condition, or (b) a live condition over scope[].fix_result as its own node sequenced before FV3-19; the current text is neither",
    "R3: relabel the N1 fallback 'no token rule; recursion as only_template' (not 'stricter'); note that the probe1 re-run shows the lists of the three no-contract callers (:1421, :1610, :1872) unchanged",
    "R4: the closed list for item 0 is the full probe3 table (t-1215 lines 37-66, 30 lines), with the five hint-declared paths marked as no practical change and the expected problem code handoff_check:required_rows (was field.blank) for refused paths",
    "R5: B2 YES branch for request.tried becomes 'stop, a question to the Lead' until R1's road exists (the NO branch is reproduced: the only non-test script naming role-to-conductor is handoff_help.py:96)"
  ],
  "class_completeness": "Empty-legal side complete: the decisions cover all 30 probe3 paths (11 top-level: inputs_read x6, rounds, s4-case-critic findings/questions/register_gaps, s8-scribe questions; 19 nested), the 5 hint-declared paths only implicitly (R4). Required side incomplete: inputs_read is carried by 15 contracts, the decision names 6; s5-critic-to-automator and s5-critic-plan-to-automator are empty-legal today and unnamed (R1). t-1215's '13 top-level' was an arithmetic slip; the count is 11.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-fv3-19-nested-null-outcome-card.md 20-180",
      "docs/tasks/specs/reviews/t-1215-fv3-19-card-plan.md (whole)",
      "ai-packages/qa-factory/scripts/handoff.py 405-534",
      "ai-packages/qa-factory/scripts/handoff_check.py 1221-1231, 1540-1559, 1600-1612, 1640-1709, 1865-1875, 2672-2680, 2726-2736",
      "ai-packages/qa-factory/scripts/null_outcomes.py 137-178, 270-294, 545-614, 656-679",
      "ai-packages/qa-factory/references/null-outcomes.json (whole)",
      "ai-packages/qa-factory/scripts/handoff_init.py 180-192, grep inputs_read",
      "ai-packages/qa-factory/handoffs/s7-automator-to-analyst.yaml (whole)",
      "ai-packages/qa-factory/scripts/tests/test_s7_null_outcome.py 455-468",
      "ai-packages/qa-factory/handoffs/index.yaml kinds (grep)"
    ],
    "reruns": [
      {"command": "python -B scratchpad/probe3.py | wc -l", "result": "30 (matches the t-1215 table)"},
      {"command": "python -B scratchpad/probe4.py (inputs_read/rounds carriers: index kind, today empty, road B empty)", "result": "15 inputs_read carriers; roadB_empty=True on the 6 named plus s5-critic-to-automator and s5-critic-plan-to-automator (both today_empty=True); s8-scribe-to-gate-b kind=report; rounds roadB_empty=True; REQUIRED_LISTS ('scope',)"},
      {"command": "Grep -i role-to-conductor|role_to_conductor over ai-packages/qa-factory, glob !**/tests/**", "result": "6 hits; the only script is handoff_help.py:96 (control: role-to-conductor.yaml:17 found by the same call)"}
    ]
  }
}
```
