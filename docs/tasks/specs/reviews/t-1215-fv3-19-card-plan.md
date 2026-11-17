# t-1215 — plan critic: FV3-19 card (the empty outcome of a nested list)

critic (Opus) · node `live-run-fvf/3/FV3-19` · card `docs/tasks/specs/20261117-fv3-19-nested-null-outcome-card.md` (draft + Lead decisions F1=B, F2=a, F3=accept, F4=b, F5=a)
Gate: PLAN review (PROJECT.md package p.6: what "an empty list" means changes). This verdict is an input to the Lead's acceptance. The decision is the Lead's.

## Verdict

**NEEDS WORK (fit_with_fixes): 2 blocking findings, 4 non-blocking.** Road B (F1) is feasible and fits AR-15, AR-23, P31 and FR-23. I checked it against the controller's coverage guard (below), and it holds. The card's measurement, though, covers only the lists road B was aimed at. It does not cover the lists that item 2's merge actually moves. Two parts of item 2 change verdicts outside the card's §2/§3 enumeration: the F4-b token rule, and switching `_is_empty_section` to `only_template`, which recurses. Among the lists affected are `inputs_read` in six contracts and S7's `rounds`, and §6 edge 1 accepts those changes in advance without a verdict for each list. One of them (`inputs_read`) is a list that must not be empty.

## What was checked (trail)

- The card (whole), the finding (whole), `s5-critic-to-automator.yaml` (whole).
- `handoff.py` 28-42, 395-464, 590-694 (`only_template`, `_spec_of_value`, `REQUIRED_LISTS`, `sections`, `is_placeholder`).
- `handoff_check.py` 700-744 (LIST_DERIVERS/DERIVERS), 1215-1231 (`_is_empty_section`), 1410-1425, 1595-1764 (`check`), 2314-2345, 2674-2678 (`_blank_value`), 2717-2766 (`_apply_one`); grep `records`, `inputs_read`, `rounds`, `help`.
- `controller.py` 6581-6601 (`_code_review_refusal`), 7776-7849 (`_code_review_problems`, the body the card did not read).
- `handoff_init.py` 116-229 (EMPTIED, `empty_optional_lists`, the inputs_read author-token prefill); `form_filler.py` 470-492; `null-outcomes.json` NE2-NE4 and grep; `handoffs/index.yaml` (escalation, kind help); `role-to-conductor.yaml` 20-75; `s4-designer-to-runner.yaml` 55-75; `s4-case-critic-to-designer.yaml` 86-152; `s7-automator-to-analyst.yaml` 29-80; `s8-scribe-to-gate-b.yaml` 72-77, 116-124.
- Re-runs (verbatim results below): M1 count, M1 content, M1 control (ii), a flow-list grep, three pure-function probes over every contract template, the readers-table spot check, the §7 negatives with positive controls.

### M1 re-run (one control re-run of the measurement)

- Grep tool, multiline, the card's pattern over `handoffs/*.yaml`, count mode: `Found 66 total occurrences across 22 files.` This matches the card.
- Content mode: the 22 non-`tried`/`data` first lines match the card's list verbatim.
- Control (ii) `^null_outcome:`: `s7-analyst-to-automator.yaml:41:null_outcome:` / `  scope:` / `    condition: triage_has_no_repair`. This matches.
- Correction: the card says the 44 `tried:`/`data:` matches are "22 files × 2 under `blocked:`". `role-to-conductor.yaml` has no `blocked:` section. Its `tried:`/`data:` (lines 32 and 38) sit under `request:`, so the `blocked.*` exemption (`handoff_check.py:1750`) does not cover them (see B2).

### Pure-function probes (scratchpad, not committed; full source kept in the scratchpad)

`probe1.py`: for every top-level list section of every contract template, compare `handoff_check._is_empty_section(template)` with `handoff.only_template(template[section])`. Output, verbatim:
```
s4-case-critic-to-designer:findings is_empty_section=False only_template=True
s4-case-critic-to-designer:questions is_empty_section=False only_template=True
s4-case-critic-to-designer:register_gaps is_empty_section=False only_template=True
s7-automator-to-analyst:rounds is_empty_section=False only_template=True
```
`probe3.py`: road B simulated on an UNTOUCHED form, where every leaf equals the template, so F4-b reads "untouched = placeholder, or carries a `<...>` token". It walks every list path that crosses no list row (`blocked` and CONTRACT_OWNED excluded) and prints each path whose untouched verdict changes from today's. Output, verbatim:
```
gate-a-to-automator:environment.preconditions_accepted_as_blocked top=False old_empty=False new_empty=True
gate-b-to-delivery:delivery.do_not_commit top=False old_empty=False new_empty=True
role-to-conductor:request.tried top=False old_empty=False new_empty=True
role-to-conductor:request.data top=False old_empty=False new_empty=True
s1-scout-to-tester:person.accepted_gaps top=False old_empty=False new_empty=True
s1-scout-to-tester:person.late_sources top=False old_empty=False new_empty=True
s4-case-critic-to-designer:inputs_read top=True old_empty=False new_empty=True
s4-case-critic-to-designer:findings top=True old_empty=False new_empty=True
s4-case-critic-to-designer:stage_acceptance.witness_paths top=False old_empty=False new_empty=True
s4-case-critic-to-designer:questions top=True old_empty=False new_empty=True
s4-case-critic-to-designer:register_gaps top=True old_empty=False new_empty=True
s4-designer-to-case-critic:review_scope.focus top=False old_empty=False new_empty=True
s5-automator-to-critic:artifacts.tests top=False old_empty=False new_empty=True
s5-automator-to-critic:artifacts.probes top=False old_empty=False new_empty=True
s5-automator-to-runner:inputs_read top=True old_empty=False new_empty=True
s5-automator-to-runner:artifacts.tests top=False old_empty=False new_empty=True
s5-critic-to-automator:probes.records top=False old_empty=False new_empty=True
s6-runner-to-analyst:inputs_read top=True old_empty=False new_empty=True
s7-analyst-to-automator:stage_acceptance.witness_paths top=False old_empty=False new_empty=True
s7-analyst-to-scribe:inputs_read top=True old_empty=False new_empty=True
s7-analyst-to-scribe:stage_acceptance.witness_paths top=False old_empty=False new_empty=True
s7-automator-to-analyst:inputs_read top=True old_empty=False new_empty=True
s7-automator-to-analyst:rounds top=True old_empty=False new_empty=True
s8-bug-reporter-to-scribe:inputs_read top=True old_empty=False new_empty=True
s8-scribe-to-gate-b:stage_acceptance.witness_paths top=False old_empty=False new_empty=True
s8-scribe-to-gate-b:delivery.reasons_by_owner.product top=False old_empty=False new_empty=True
s8-scribe-to-gate-b:delivery.reasons_by_owner.person top=False old_empty=False new_empty=True
s8-scribe-to-gate-b:delivery.reasons_by_owner.stand top=False old_empty=False new_empty=True
s8-scribe-to-gate-b:delivery.reasons_by_owner.factory top=False old_empty=False new_empty=True
s8-scribe-to-gate-b:questions top=True old_empty=False new_empty=True
```
`artifacts.probes` and `witness_paths` change nothing in practice, because their row fields are already optional by hint. Every other line is a pass where today there is a refusal. `person_question.options` does NOT appear: its template row carries the literal `id: a`, so road B never reads it as untouched. `probe2.py` confirmed the row-field optionality of the card's nine lists: all their row fields are non-optional, and `probes.records[].note` is optional.

## Blocking findings

**B1 (blocking). Item 2 changes top-level verdicts the card says it keeps, and pre-accepts those changes without a verdict for each list. One affected list must not be empty.**
Surface: `handoff_check._is_empty_section` → `handoff.only_template`, the reader of "an untouched template row".
- Card line 104 (item 2): `_is_empty_section` "calls `handoff.only_template` with the template row (the twin retired, AR-15)". The two are not twins. `_is_empty_section` (`handoff_check.py:1226-1229`) applies `is_placeholder` to each row VALUE, so a row holding a nested list or map is never empty (`str(list)` does not match `^<(.+)>$`). `only_template` (`handoff.py:413-417`) recurses. probe1 shows 4 top-level lists whose untouched verdict flips from refused to legal on the recursion alone, before any F4-b effect: s4-case-critic `findings`, `questions`, `register_gaps`, and s7-automator-to-analyst `rounds`.
- F4-b (token leaf equal to the template → untouched) flips 9 more top-level lists (probe3, `top=True`): `inputs_read` in s4-case-critic-to-designer, s5-automator-to-runner, s6-runner-to-analyst, s7-analyst-to-scribe, s7-automator-to-analyst and s8-bug-reporter-to-scribe, plus s8-scribe-to-gate-b `questions`.
- §6 edge 1 (line 123) says: "no top-level form changes outcome, except rows item 0 lists for F4-b". Item 0 (line 102) greps only for F4-b token rows and says only that the builder lists them. A change it lists is then "inside §6", so it does not stop the node. The recursion-only flips (`rounds` and the three s4 lists) are not caught by item 0's grep at all.
- Failure scenario: an S6 runner, S7 automator or S8 bug-reporter form whose `inputs_read` row stands untouched (`path: work/handoffs/<the analyst's dispatch>.yaml`, version placeholder). Today the plain check refuses `inputs_read[0].version` as `field.blank`. The `--fix` deriver `_version_of` returns None on a `<` path (`handoff_check.py:497`), so the refusal stands under `--fix` too. After item 2 the list reads as empty, the blank loop skips it, and the form passes with no proof that the role read its inputs. The init prefill (`handoff_init.py:116-177`) replaces only the critics' `<the author's dispatch>` token, and only when that dispatch is given. `inputs_read` is "one line per entry of the author's inputs" (s5-critic yaml:24-26). That is a list that must not be empty. It is homeless and de facto required by accident, which is exactly the finding's class, and it now becomes empty-legal (AR-28, AR-23).
- `rounds` (S7 automator, one row per repair, carrying `changed` and `verify.witness`) also flips to empty-legal. No other guard in `handoff_check.py` or `driver_stage_s7.py` reads it (grep `rounds`: only the `rounds[].verify.witness` deriver). An automator could report `fix_result: fixed` in `scope` and leave `rounds` untouched, and the form would pass. The Lead must decide whether that is a legitimate empty.
- The three s4-case-critic lists are already emptied at skeleton time as optional (`handoff_init.EMPTIED`, lines 184-188). So their flip matches existing intent, but it still needs to be written down. s8 `questions` is probably a legitimate empty, but it is undecided.
- Fix: put probe3's table into card §2 as the real measurement (M4). For each top-level list it flips, add an F3-style verdict. For `inputs_read` (×6), keep a refusal on the untouched list by a road that does not carve top-level out of F4-b (P31 / rule 19: an exclusion with no data row blocks). One candidate: `inputs_read` joins the required set as data. That brings W1/`null-outcomes.json` NE rows and a row sentence that is not scope-worded at `handoff_check.py:1666-1670`, because today's text says "One row per item in scope". That is a fork for the Lead. Then rewrite §6 edge 1 as a closed list of the verdict changes, and turn item 0 into a re-run of probe3 that must reproduce that list exactly. Any other change stops the node.

**B2 (blocking). The class enumeration (axis 5) misses N-map lists, so the "nine lists / F3 verdicts" sibling walk is incomplete.**
Surface: the M1 grep, i.e. how list paths are enumerated from the templates.
- The M1 pattern matches only block lists (`key:` followed by `- `). The card names one limit (a blank line), but flow lists are missed too: s8-scribe-to-gate-b `delivery.reasons_by_owner.{product,person,stand,factory}: ["<reason>"]` (yaml:72-76, depth 3). Road B makes all four empty-legal (probe3), and none of them has an F3 verdict.
- `role-to-conductor` `request.tried` / `request.data` are counted as `blocked.*` (card line 22), but they sit under `request:`. Road B makes both empty-legal (probe3). `request.tried` is the role's record that every route was tried (FR-50), so it is not obviously a legitimate empty. The card's worry, `person_question.options`, is unaffected: the literal `id: a` keeps its row non-empty (probe3 omits it). Lead decision F3's stop condition is therefore aimed at the wrong list in that contract.
- Fix: replace M1 with an enumeration from the parsed template, which is what `list_paths` itself will do (probe3's walk is one). It catches flow lists and blank-line lists, and it does not misattribute parents. Re-derive the N-map set: the card's 8 lists (minus `person_question.options`), plus `reasons_by_owner` ×4 and `request.tried`/`request.data`. Give each an F3 verdict. For `request.*`, settle with one measurement whether `handoff_check` ever checks a role-to-conductor form. My search: no package script outside tests names `person_question`. The only non-test script naming `role-to-conductor` is `handoff_help.py:96`, which writes the request. `driver_conductor.py:295` shows the help file to the conductor as text. This points to "never checked" (estimate, not verified, because a CLI run on such a file is possible). If it is never checked, write that down and drop the stop branch. If it is, decide the list now. A stop with no road behind it is not executable by a weaker model (PROJECT.md p.11).

## Non-blocking findings

- **N1 — the template source for `_is_empty_section` is unspecified (code quality, weak-model executability).** Item 2 says "with the template row", but `_is_empty_section(doc, spec, section)` has no contract parameter. Three callers pass `spec=None` with no contract: `handoff_check.py:1421` (null outcome impl), `:1610` (investigation view) and `:1872`. Fix: name the signature, for example `_is_empty_section(doc, spec, path, contract=None)`. Name its fallback too: no contract or no readable template → `only_template(value)` with no template, so no token rule, which is the stricter side.
- **N2 — item 4 builds a twin of the depth rule in the filler (duplication and consistency, AR-13).** The filler's new rule is "a list path that is not in REQUIRED_LISTS → leave untouched". It would also excuse an N-row list (for example `execution[].preconditions` with a world-list token), and the check still refuses that list (R5). The filler and the checker would then disagree. Fix: the filler reads `handoff.list_paths(contract)` minus REQUIRED_LISTS, the same reader as the check. Add an R10 row for an N-row path.
- **N3 — §6 edge 4's "a role cannot write either" is inaccurate.** `--set probes.records=foo` (the raw branch, `handoff_check.py:2724-2730`, path in `doc.nodes`) writes a scalar, which then reads as "empty". This mirrors top-level today (`--set findings=foo`), so the invariant "nothing reaches a pass it cannot reach today at the top level" holds by symmetry. Fix: correct the sentence. Optionally add one R row pinning that the raw-scalar case behaves the same at both depths.
- **N4 — the Lead decision on `person_question.options` (F3) rests on a premise that does not hold (see B2).** It should move to `request.tried`/`request.data`.

## Verified and holding (no finding)

- M2/M3 facts: `probes` is a map (`sections`: `probes: map`). `probes.records[].instance`/`.verdict` are non-optional and `.note` is optional (probe2). `_apply_one` writes nothing for `[]` (`_blank_value([])` → `all([])` True, `:2676-2677`, `:2731-2732`). The quoted refusal text is the filler's (`form_filler.py:481-482`), pinned by `test_form_selftest.py:88`, and quarantined (`test-layers.json:8337`).
- The AR-15 argument for F1-B holds. `_code_review_problems` (`controller.py:7833-7848`) walks `manifest_tests(manifest)` with `proof_level.proof_required` and reads `sensitivity_proof` / the binding receipt / the reason from the MANIFEST. It never reads the critic form's `probes.records` or the automator's `artifacts.tests`. So an empty `probes.records`, together with an empty `artifacts.tests`, cannot close a window whose manifest has unproven new or changed tests. §6 edge 5 is right.
- F3 `artifacts.tests`: NE3 (`null-outcomes.json:17-20`) declares the window with no tests ("lists no tests, and says so", E41). The `--fix` LIST_DERIVERS run before the empty verdict (`:1627-1635` before `:1655`). The edge is right.
- The other seven of the card's list verdicts are legitimate empties: the person accepted none, named none, found none late, the designer knows nothing weak, no probe ran. `person_question.options` is moot (B2).
- S7's null outcome is untouched: neither `s7-analyst-to-automator:scope` nor `not_for_repair` appears in probe1/probe3, so the `_null_outcome_impl` and `_investigation_view` readings keep their verdicts.
- The readers table spot check: the `REQUIRED_LISTS` readers are `handoff_check.py:1661,2400`, `handoff_init.py:203`, `null_outcomes.py:281,566`, `form_filler.py:370` and `project_decisions.py:45`, as listed (`null_outcomes` W1 included). The §7 negatives were re-run with case-insensitive grep over `.githooks`, `.claude/agents` and `.claude/settings.json` → 0, with controls `handoff|pre-commit` over `.githooks` → 3 and `handoff` over agents → 10. `tools/` → 2 files (`source-split-carriers.json`, `test_dod_gate.py`), as stated.
- F5-a: the builder changes the filler and the Lead runs `test_quarantine.py judge`. The builder never touches the quarantine file. That is correct.

## Standing questions

- DUPLICATION AND CONSISTENCY: one finding (N2, the filler twin). The card retires one twin (`_is_empty_section`), but B1 shows the merge is a meaning change, not a retirement. Grepped: `_is_empty_section|only_template`, `REQUIRED_LISTS`, `inputs_read`, `rounds`.
- CODE QUALITY: N1 (unspecified signature and fallback). Otherwise the items are concrete: file, function, row.
- ONE ACTION, ONE ROAD (P31): road B is one rule at every depth that crosses no list row. That is right, and the card leaves no carve-out of its own. B1's fix must not introduce one (no "F4-b only below the top level" without a data row).
- TESTS (TESTING.md budget): one parameterised function with table rows and no new file is within budget. The fixes add rows (M4 verdicts, `inputs_read` kept refused, `rounds` decided, an N-row filler row), not functions.
- CLASS COMPLETENESS (axes 5, 34): incomplete. See B1 (top-level lists moved by the merge) and B2 (flow lists, `request.*`). Axis 18: no ratchet is raised under B, which holds. Axis 38: road B adds no refusal, which holds unless B1's fix for `inputs_read` adds one, and then axis 38 applies.

## Edges: named and decided right?

- Edges 2, 3, 5, 6, 7, 8 and the reused-function paragraph: right.
- Edge 1: wrong as written (B1).
- Edge 4: right in substance, wrong in one sentence (N3).
- A re-review after the fix round should carry only the card diff: M4, the list verdicts, the rewritten edge 1, item 0 and the `inputs_read` road. B1's `inputs_read` road is a meaning change, so PROJECT.md p.6(b) asks for a plan re-check of that part.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1: item 2 merges _is_empty_section into only_template (recursion + F4-b) and flips 13 top-level lists from refused to empty-legal on an untouched form (probe1/probe3): inputs_read x6 (s4-case-critic, s5-automator-to-runner, s6-runner, s7-analyst-to-scribe, s7-automator, s8-bug-reporter), s4-case-critic findings/questions/register_gaps, s7-automator rounds, s8-scribe questions; section 6 edge 1 pre-accepts them through item 0 with no verdict for each list; inputs_read must not be empty (proof of reading), card lines 102-104 and 123",
    "B2: the M1 grep misses flow lists (s8-scribe delivery.reasons_by_owner product/person/stand/factory) and counts role-to-conductor request.tried/request.data as blocked.*; road B makes all six empty-legal with no F3 verdict; person_question.options is NOT affected (literal id: a), so the Lead's F3 stop condition targets the wrong list"
  ],
  "fixes": [
    "Add M4 to card section 2: probe3's table (list paths crossing no list row whose untouched verdict changes), with a verdict for each list",
    "inputs_read x6: keep the untouched list refused by a road that adds no top-level carve-out (Lead fork, e.g. a required-set entry as data with a row sentence that is not scope-worded, plus null-outcomes.json/W1 rows); decide s7-automator rounds and s8-scribe questions; record the three s4-case-critic lists as matching handoff_init.EMPTIED",
    "Rewrite section 6 edge 1 as a closed list of verdict changes; item 0 re-runs the probe3 walk and must reproduce that list exactly, any other change stops the node",
    "Replace M1 with an enumeration from the parsed template (what list_paths will do); give reasons_by_owner x4 and request.tried/request.data F3 verdicts; settle by measurement whether handoff_check ever checks a role-to-conductor form and drop or redirect the F3 stop branch",
    "N1: name the _is_empty_section signature (contract param) and its no-template fallback (no token rule, stricter); callers at handoff_check.py:1421, 1610, 1872 pass spec=None",
    "N2: item 4 filler reads handoff.list_paths minus REQUIRED_LISTS, not REQUIRED_LISTS alone; add an R10 row for an N-row path",
    "N3: correct section 6 edge 4 (raw --set can write a scalar at a list path; same as the top level today)"
  ],
  "class_completeness": "Incomplete. Axis 5/34: the card enumerates 9 map-nested lists, but road B as specified also moves 13 top-level lists (B1) and 6 more map-nested lists missed by the block-only grep (B2); person_question.options is not moved. Axis 18 (ratchets): none raised, holds. Axis 38: no new refusal under road B, holds unless the inputs_read fix adds one.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-fv3-19-nested-null-outcome-card.md",
      "plans/piles/live-run-fvf/findings/20261117-p1b-probes-records-bez-pustogo-ishoda.md",
      "ai-packages/qa-factory/handoffs/s5-critic-to-automator.yaml",
      "ai-packages/qa-factory/scripts/handoff.py 28-42, 395-464, 590-694",
      "ai-packages/qa-factory/scripts/handoff_check.py 495-507, 700-744, 1215-1231, 1410-1425, 1595-1764, 2314-2345, 2674-2678, 2717-2766",
      "ai-packages/qa-factory/scripts/controller.py 6581-6601, 7776-7849",
      "ai-packages/qa-factory/scripts/handoff_init.py 116-229 (grep + 180-229)",
      "ai-packages/qa-factory/scripts/tests/form_filler.py 470-492",
      "ai-packages/qa-factory/references/null-outcomes.json NE2-NE4 (grep)",
      "ai-packages/qa-factory/handoffs/index.yaml escalation block",
      "ai-packages/qa-factory/handoffs/role-to-conductor.yaml 20-75",
      "ai-packages/qa-factory/handoffs/s4-designer-to-runner.yaml 55-75",
      "ai-packages/qa-factory/handoffs/s4-case-critic-to-designer.yaml 86-152",
      "ai-packages/qa-factory/handoffs/s7-automator-to-analyst.yaml 29-80",
      "ai-packages/qa-factory/handoffs/s8-scribe-to-gate-b.yaml 72-77, 116-124",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "Grep multiline card M1 pattern over handoffs/*.yaml, count", "result": "Found 66 total occurrences across 22 files (matches the card); content mode: 22 non-tried/data lines match the card; role-to-conductor tried/data sit under request:, not blocked:"},
      {"command": "Grep ^null_outcome: over handoffs/*.yaml -A2", "result": "s7-analyst-to-automator.yaml:41 null_outcome: / scope: / condition: triage_has_no_repair (matches)"},
      {"command": "python -B scratchpad/probe1.py (_is_empty_section vs only_template on every top-level list of every template)", "result": "4 differ: s4-case-critic findings, questions, register_gaps; s7-automator-to-analyst rounds (False vs True)"},
      {"command": "python -B scratchpad/probe2.py (spec optionality of the nine nested lists)", "result": "all row fields non-optional; probes.records[].note optional; probes is a map"},
      {"command": "python -B scratchpad/probe3.py (road B + F4-b simulated on untouched templates)", "result": "30 list paths flip refused->empty-legal: 13 top-level (inputs_read x6, s4-case-critic findings/questions/register_gaps, s7 rounds, s8-scribe questions) + map-nested incl. reasons_by_owner x4 and request.tried/data; person_question.options absent"},
      {"command": "grep -rniE 'null_outcome|REQUIRED_LISTS|handoff_check|s5-critic-to-automator' .githooks .claude/agents .claude/settings.json | wc -l; controls", "result": "0; controls: .githooks handoff|pre-commit 3, .claude/agents handoff 10; tools/ 2 files (source-split-carriers.json, test_dod_gate.py)"},
      {"command": "grep -rn REQUIRED_LISTS ai-packages/qa-factory/scripts", "result": "readers match the card table: handoff_check 1661,2400; handoff_init 203; null_outcomes 281,566; form_filler 370; project_decisions 45"}
    ]
  }
}
```
