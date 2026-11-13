# t-533 — code critic, FV1-19 N2 (cec537b) + N3 (f0f1b77), one pass per topic (R13-g)

critic (opus), 13.11.2026. Base: N1's accepted head 5f47f7b. Spec: `docs/tasks/specs/20261113-fv1-19-obligation-refs-spec.md`
§4 (M3-M5), §5 (E3, E8, E12, E18, E19, E27, plus E22/E28 read), §6 N2 (a)-(n), N3 (a)-(g), §8a forks F1/F3/F7.

**Verdict line: ACCEPT WITH FIXES — 0 blocking findings, 2 FIX (small, N2), 3 QUEUE.** This verdict is an input to acceptance;
acceptance, and the owns widening F-2 needs, are the Lead's.

## 1. Merge and D5 agreement (the dispatch's direct question)

- **Textual merge is clean.** `git -C C:\QAFactory\forge-repo merge-tree --write-tree wip/fv119-n2 wip/fv119-n3` → `66684c811bb2d1e63aeeb042575bd7a6a102eafb`,
  exit 0, no conflict lines (`wip/fv119-n2` = cec537b, `wip/fv119-n3` = f0f1b77, checked with `rev-parse`). The two diffs touch
  disjoint files (N2: window_record, s5_precheck, manifest_from_tests, charter, changelog fragment, 3 test files; N3: controller.py,
  test_controller_state.py).
- **Precheck and finish give the same verdict on the D5 set, on the MERGED tree** — my one control re-run (below): the merged tree
  (archive of 66684c8) imported directly; precheck verdict = `window_record.row_field_gaps(row, None, plan, known)` with
  `known = C.obligation_map(rows)`; finish verdict = `Controller._s5_v2_collect` called with a stub `self` whose `_plan_document`
  returns the same rows (critic dispatch path; the author/critic structural problem filtered out, it is not a refs verdict):
  ```
  valid             pre=pass fin=pass agree=True
  stale             pre=REFUSE fin=REFUSE agree=True | stale: obligation_refs[0]: OB-A carries hash c70000000000000 | instance obligation_refs do not match the current
  missing hash      pre=REFUSE fin=REFUSE agree=True | obligation_refs[0]: OB-A has no obligation_hash (missing has | coverage v2 instance requires unique obligation_re
  unknown id        pre=REFUSE fin=REFUSE agree=True | obligation_refs[0]: OB-ZZ is not an obligation of the plan ( | instance obligation_refs do not match the current
  non-owed stale    pre=REFUSE fin=REFUSE agree=True | stale: obligation_refs[0]: OB-M carries hash c70000000000000 | instance obligation_refs do not match the current
  non-owed valid    pre=pass fin=pass agree=True
  int id            pre=REFUSE fin=REFUSE agree=True | obligation_refs[0].obligation_id is not a non-empty string;  | coverage v2 instance requires unique obligation_re
  hash of other ob  pre=REFUSE fin=REFUSE agree=True | stale: obligation_refs[0]: OB-A carries hash a9fe6a338ae76e9 | instance obligation_refs do not match the current
  ALL AGREE
  non-refs problems: ['coverage v2 S5 completion requires distinct accepted author ']
  ```
  The two divergences that remain are the spec's NAMED ones, both in the safe direction (precheck more lenient, finish refuses):
  empty map (E3: precheck non-strict silent, finish strict refuses) and a row of a non-owed case carrying no id-bearing refs (E12 /
  N2 Deviation 1). Both readers read the same file: `_plan_rows_of` tries `work/test-plan.json` first, `_plan_document` reads exactly
  it (`controller.py:2251-2258`); both maps are `C.obligation_map` (last wins, all schemas).

## 2. Findings

### FIX

**F-1 (N2, `window_record.py:144-147`, `ORIGIN["obligation_hash"]`; test row `test_window_record.py` "QB (k)").** The QB door
("a stale binding hash is refreshed by re-sending the binding's `design_assessment` ...") is placed on the wrong surface.
`ORIGIN["obligation_hash"]` is reached (a) by `window_record.build` when the ROW-level item hash is empty because the row has no refs
(`window_record.py:1358-1361`) and (b) through `GAP_ORIGIN["obligation_hash"]` (`:363`) for the acceptance gap
`obligation_hash:<instance>`, emitted when the window ITEM carries no `obligation_hash` (`acceptance.py:1189-1190`). Neither is a stale
BINDING hash (the binding hash is read only by `coverage_contract.py:281, 580`). Failure scenario: an instance whose row has no refs
gets the note "the manifest row carries no `obligation_refs` to hash; the automator sends ... the code writes the hashes; a stale binding
hash is refreshed by re-sending the binding's `design_assessment` ..." — a door for a condition this note never detects, beside the real
one. The report's claim "(the binding hash's gap origin, row (k))" and the test row's name "the binding hash's origin" rest on that
misreading. Fix: drop the binding clause from `ORIGIN["obligation_hash"]` and the "QB (k)" check; the door stays where it is accurate,
in the `stale` refs finding (`_obligation_refs_problem`). This also removes the duplicated inline sentence (two hand-written copies of
the binding door, see §3 duplication).

**F-2 (N2 Deviation 3, `manifest_from_tests.py:1732-1733`, `_row_form` `else` branch).** "row fields still missing, and not yours to fill
by hand:" is the marker-era branch (fields with no slot). After M3 every carrier field is `filled_by == "automator"`, so whenever the
legend is non-empty `form["tests"]` is non-empty; the branch is now reached ONLY when `wanted` is empty (no early return, since
`not form["legend"] and wanted` is false) — and then prints that header with no field under it (traced: `wanted=[]` → loop skips every
entry → legend `{}` → `else`). Spec M3 says the marker branches of `manifest_from_tests` lose their last user and are removed (AR-22);
N2's owns limited `_row_form` to the call line, so the builder correctly stopped. The empty-`wanted` printing is pre-existing on the
base; the "not yours to fill by hand" wording is what N2 made untrue. Fix: Lead widens N2's owns to these two lines (delete the branch;
keep behaviour for empty `wanted` as "no line"), or queues it by name — Lead's call (PROJECT.md «Командная работа» 9 prefers fixing now).

### QUEUE (proposed nodes / pointers; the Lead opens or declines)

**Q-1 (neighbour of QB, same surface "stale binding hash").** A stale binding hash has no surface of its own: `coverage_contract.py:580`
silently projects `design = "unknown"` (and validity/sensitivity reset) when `binding.obligation_hash != content_hash(ob)`; no precheck
or gate reads binding hashes (grep `obligation_hash` over `s5_precheck.py`, `branch_accounting.py`, `window_record.py` at cec537b: hits
only in window_record's row-level/ORIGIN lines — the positive control of the same call). So the QB door reaches the role only while a
ROW ref of the same obligation is also stale; after the role repairs the row refs (ids-only), the refs finding disappears and the binding
stays stale with no text naming the `design_assessment` re-send. Usually both go stale together on a re-plan, hence QUEUE not FIX.
Proposed node: a precheck reading of binding-hash currency through the same map (`C.obligation_map`), finding text = the QB door; owner
Lead of `live-run-fvf`, sits with rereview QA (whether a refresh resets code_validity/sensitivity).

**Q-2 (N1/F7(b) sibling in a queued render site).** `skills/qa-story/phases/s5.md:309-310` says the marker's refusals include "an
obligation not on the case's plan row" — after F7(b) (N1 row (r)) the marker is judged against the WHOLE plan. The spec queues
`s5.md:292-299` only; extend that pointer to `:309-311` (same passage, same F1 (c) node).

**Q-3 (integrator).** N2's user-visible change (the precheck finding names the fragment door for `obligation_refs` in every language;
present refs judged for unknown/stale on every row) has no `changelog.d` line; the fragment N2 edited carries only N1's behaviour plus the
two QB sentences. One line at integration.

### Notes (no finding)

- **N3 hygiene:** the builder's self-reported heredoc `python` rewrite of its own test block is a command-hygiene pt. 4 breach (a
  git-tree file written outside Edit/Write); the content is judged by the run (coordinator 343/343) and by my reading of the block —
  a calibration line, not a code finding.
- **N3 error direction on a malformed plan:** old code raised `TypeError`/`AttributeError` out of `_s5_v2_collect` for a plan dict
  without `rows` or a non-dict row/obligation; now `obligation_map` skips them and every ref is `unknown` → StateConflict plan text.
  Safer (a refusal, never a pass; AR-28), not named in the spec; no action.
- **N2 report** keeps the round-1 bullet "role-load.json 18687 -> 18709" under "What changed", superseded by its ROUND 2 section;
  diffstat 5f47f7b..cec537b has no `role-load.json` — the final state is no ratchet raise (AR-20: nothing to name). Commit 2e8075d's
  message still says RAISE; the round-2 commit undoes it.
- **Charter clause** "`obligation_refs` ids `manifest_put.py`;" is terse to the edge of legibility (ratchet trade-off chosen by the
  Lead). Backstops: the row form legend and the precheck finding carry the full shape; a role sending `["OB-1"]` gets N1's shape refusal
  naming `[{"obligation_id": ...}]` — one turn at worst. FR-33 live row covers it.

## 3. N2's three deviations, judged

1. **"Present" = an id-bearing dict, not "any value but None/[]" (spec M4 wording).** ACCEPT. Traced: a string, `["junk"]` or `[{}]`
   on an owed row → `missing` (door named); on a non-owed row → `''`, while the finish refuses (build drops non-dicts → empty → shape).
   That is exactly the E12 divergence (non-owed row without refs), already named, safe direction; such values cannot be newly written
   (N1's stamp refuses non-list/non-dict). A mixed list `[{"obligation_id":"o1"}, "junk"]` IS judged (shape) — E28 held (row (f)).
2. **Text = predicate text + repair tail; `stale: ` prefix.** ACCEPT. One wording source (N1's `_ref_shape_problems` /
   `obligation_ref_problems`) plus one constant `REF_REPAIR`; every verdict names the ids-only door (FR-1/FR-2/FR-57).
3. **`_row_form` else branch left.** Correct stop at the owns boundary; the residual is F-2.

## 4. Spec rows checked

N2: (a) one fix text, Python row byte-identical to TS (test compares `fix` fields); (b)/(m) slot + legend = carrier `what`; (c)-(e),
(h), (j) ten inputs × owed/non-owed through `check_row_fields` (the gate's own entry), all refused except valid; (f) legacy / no plan;
(g) item keeps a LIST, `window_text_fields()` excludes it — traced: `window_text_fields` filters `spec.window and filled_by ==
"automator"` (`window_record.py:196` base), before excluded by `marker`, now by `window=False`: same set, M3 invariant kept; (i) brief
line via the carrier, read-only; (k) ORIGIN (see F-1); (l) charter; (n) composition on owed and non-owed rows against
`obligation_ref_problems(..., strict=True)`. N3: (a) five texts byte-identical (head before the tier tail); (b) shape before hash,
fingerprint before plan; (c) five-input composition; (d) schema-1; (e) empty map; (f) last wins; (g) E27 int id / int hash → shape.
Diff of `controller.py` stays inside `_s5_v2_collect` (4 hunks); `content_hash` still used by the row-hash line.

## 5. Standing questions

- **DUPLICATION AND CONSISTENCY:** N2 removes a duplicate (two fix-text branches → one; the precheck's own id/dup logic → N1's
  predicate); N3 removes the finish's inline map and inline per-ref comparison. New duplicate found: the binding-door sentence written
  twice as separate literals (`window_record.py:146-147` and inside `_obligation_refs_problem`) — resolved by F-1. Minor, no finding:
  `check_row_fields` and `_row_form` each read the plan twice (`plan_obligations` + `plan_obligation_map` both go through
  `_plan_rows_of`). Grepped: `obligation_hash` in merged `controller.py`/`window_record.py` (only the row-level line remains in the
  finish), `MARKER_DOOR|by_marker|written by the marker|not yours to fill by hand` over merged `scripts/*.py` (hits: `brief_pack.py:2010`
  — T3b, queued; `manifest_from_tests.py:1733` — F-2; `probe_by_code._row_by_marker` — unrelated token reader).
- **CODE QUALITY:** both diffs are small and readable; N3 keeps the old texts and order verbatim and computes the predicate once per
  instance; N2's `_obligation_refs_problem` separates demand from validity in its docstring and code. Only F-1/F-2 above.
- **q10 ARCHITECTURE (AR-n):** AR-13 kept — the per-ref comparison lives only in `contract.obligation_ref_problems` (merged-tree grep);
  AR-15 one predicate for writer/precheck/finish; AR-22 marker producer and readers removed except F-2 and the queued T3b branch; AR-20
  no ratchet move (role-load.json not in the diff); AR-23/AR-28 strict finish on an empty map (N3 (e), my control "stale"/"unknown"),
  precheck silent on hashes only when the map is empty; AR-1/AR-2 no language list added (N2 removed the only language-shaped door).
- **q11 JUDGMENT:** every altered check is DATA (shape, join against the plan, hash equality); which obligation a test proves stays the
  automator's (P17), no census class changes (N2 witness `test_judgment_census 24/24`). Nothing judgment-shaped moved into code.
- **q12 ONE ROAD:** improved — one door text for every language (the TS-impossible marker door is gone from precheck, row form, origin
  notes, charter). Residuals, all already carried with an owner: the Python marker as a second authoring form (F1 (a), Lead-decided;
  class fix F1 (c) node), `brief_pack._row_field_lines` (T3b queue line), `s5.md` (queued pointer; Q-2 widens it). No exclusion of a
  language/case without an owner word was added.

## 6. Class completeness (rule 5, SIBLING_MAP axes named by the spec)

Axis 28 (render sites of one carrier): precheck + row form + blank form changed in N2; brief line queued to T3b; stage text queued
(widen per Q-2). Axis 23 (carrier ↔ readers): every reader of `REQUIRED_ROW_FIELDS` (`brief_pack`, `_row_form`, `_blank_row_form`,
`window_text_fields`, `_row_fields_text`) grepped for `filled_by` — all consistent with the single value. Axis 34 (one way per
language): see q12. The QB surface's neighbour (stale binding with no detector) is Q-1. No sibling left silent.

## 7. Trail

Read: the two diffs in full (code + tests); N1 `contract.py:5178-5370` at 5f47f7b (`_plan_rows_of`, `obligation_map`,
`plan_obligation_map`, `_ref_shape_problems`, `obligation_ref_problems`, `_stamp_row_refs`, `_binding_stamp_allowed`);
`controller.py` `_plan_document` and `_s5_v2_collect` at f0f1b77; `window_record.py` ORIGIN/GAP_ORIGIN/`build` (`:340-440`,
`:1300-1362`) at cec537b; `manifest_from_tests.py` `_row_form`/`_blank_row_form` at cec537b; `acceptance.py:1180-1235`;
`coverage_contract.py:565-620`; `s5.md:290-312` (merged); both builder reports; N1 re-review §QA/QB; spec §0-§8 (through F9).
Re-runs: merge-tree (above); the D5 control on the merged tree (above, one run). Not re-run: test files (attached witnesses and the
coordinator's control runs N3 343/343, N2 role_load 169/171 — both fails qa-failure-analyst, pre-existing — are consistent with the
diffs: N2 report's per-row list matches the test code read; N3's five old texts match the unchanged literals in the diff).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F-1 (N2): drop the stale-binding clause from window_record.ORIGIN['obligation_hash'] (it fires on a row/item with no refs, acceptance.py:1189-1190 and window_record.py:1358-1361, never on a stale binding) and the 'QB (k)' check in test_window_record.py; keep the door in the stale refs finding of _obligation_refs_problem",
    "F-2 (N2 deviation 3): remove the marker-era else branch of manifest_from_tests._row_form ('row fields still missing, and not yours to fill by hand:'), now reachable only with empty wanted where it prints a header with no fields; needs the Lead to widen N2 owns, or queue it by name"
  ],
  "class_completeness": "Axis 28: precheck, row form and blank form changed (N2); brief_pack._row_field_lines queued to T3b; s5.md queued, pointer should widen to :309-311 (Q-2, F7(b) marker rule text). Axis 23: every filled_by reader consistent with the single value. Axis 34: one door text for every language; Python marker residual carried by F1 (c). QB surface neighbour: a stale binding hash has no detector of its own (Q-1, proposed node with rereview QA). Changelog line for N2 (Q-3, integrator).",
  "trail": {
    "read": [
      "git diff 5f47f7b cec537b (N2, full)",
      "git diff 5f47f7b f0f1b77 (N3, full)",
      "docs/tasks/specs/20261113-fv1-19-obligation-refs-spec.md (sections 0-8)",
      "contract.py:5178-5370 at 5f47f7b",
      "controller.py _plan_document, _s5_v2_collect at f0f1b77",
      "window_record.py ORIGIN, GAP_ORIGIN, build at cec537b",
      "manifest_from_tests.py _row_form, _blank_row_form at cec537b",
      "acceptance.py:1180-1235",
      "coverage_contract.py:565-620",
      "skills/qa-story/phases/s5.md:290-312 (merged)",
      "docs/tasks/specs/reports/20261113-fv119-n2-report.md",
      "docs/tasks/specs/reports/20261113-fv119-n3-report.md",
      "docs/tasks/specs/reviews/20261113-fv119-n1-fix-rereview.md (QA, QB)"
    ],
    "reruns": [
      {
        "command": "git -C C:/QAFactory/forge-repo merge-tree --write-tree wip/fv119-n2 wip/fv119-n3",
        "result": "66684c811bb2d1e63aeeb042575bd7a6a102eafb, exit 0, clean"
      },
      {
        "command": "python -B (stdin) on git archive of 66684c8: window_record.row_field_gaps vs Controller._s5_v2_collect (stub self) on 8 D5 inputs",
        "result": "ALL AGREE: valid pass/pass, stale, missing hash, unknown id, non-owed stale, int id, hash of other ob refused by both; non-owed valid pass/pass"
      }
    ]
  }
}
```
