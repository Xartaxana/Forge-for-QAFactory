# FV3-19 card r2: the empty outcome of a nested list (`probes.records`), and `inputs_read` required by name

designer t-1227 (resubmission of t-1211) · node `live-run-fvf/3/FV3-19` · feature F19 · finding `plans/piles/live-run-fvf/findings/20261117-p1b-probes-records-bez-pustogo-ishoda.md`
Sources folded in: card r1 `docs/tasks/specs/20261117-fv3-19-nested-null-outcome-card.md` with its three Lead-decision sections, verdicts `docs/tasks/specs/reviews/t-1215-fv3-19-card-plan.md` and `docs/tasks/specs/reviews/t-1219-fv3-19-card-rereview.md`.
This card replaces r1 for the builder. The builder reads only this file, plus the files named on its `given:` line. There are no override sections. Forks that the Lead's decisions left open are listed at the end (F-r2-1 to F-r2-6). The node below is written so that it can run on each fork's recommendation until the Lead decides otherwise. Where a fork changes an item, the item says so.

## 1. AR-n, owners, census

| AR | how this card touches it | change check written into the DoD |
|---|---|---|
| AR-23 | Every list whose path crosses no list row gets one empty rule. `inputs_read` joins `scope` as a required list. Its 14 index carriers get homes. | `test_null_outcomes.py` (the audit over the real tree) is green at the new pins (§5 item 3). |
| AR-28 | An untouched list must never turn into a pass the gate did not mean. A required list stays refused when it is empty. | Rows R2, R3, R5, R11, R12. The closed list in §6 edge 1 is reproduced exactly by item 0. |
| AR-22 | Both the critic and the roles are told where the empty outcome lives. | The yaml comment and the regenerated slice ship in one commit, and `contract_slices.py --check` is green. |
| AR-15 / AR-13 | `handoff.only_template` is the one reader of "an untouched template row". `_is_empty_section` calls it, so its own per-value reading goes away. `handoff.list_paths` is the one reader of "which list paths exist", and both the checker and the filler use it. | R7, R10c, R16. |
| AR-10 / AR-18 | The `required_rows` refusal sentence is built from `row_form`, the contract-derived row form, and no longer says "in scope". The joint requirement that roles read before the work is rewritten (fork F-r2-2). | R11 (text). `test_detector_verdict.py` T6 shows `record.expected == told_text(row)`. |
| AR-20 | Pins move: the walk-size pin `scope` goes from 17 to 31 (both directions, not shrink-only), and the T6 digest of the `required_rows` text is re-captured. No shrink-only ratchet is raised. | `test_judgment_census.py` runs with no count raised. The two pin moves are named in the builder report. |
| AR-29 | Checks altered, none added (below). | `test_judgment_census.py` is in the witness. |
| AR-1 | `REQUIRED_LISTS` is a schema grammar in code, not project variety. It is one tuple, read by name for every contract, with no per-contract branch. | No list of contract names enters code. The 14 homes are data rows. |

Checks this card alters (P27, AR-29). None is added.
1. `handoff_check.check`, the empty-list verdict. It runs over `handoff.list_paths(contract)` instead of top-level list sections, and the refusal now also fires for `inputs_read`. Class **shape**, owner **data**. It reads whether a value is present at a path, never what a row says. Census row: `judgment-census.json:476`, `handoff_check.py::check`, class shape, owner data, already covering all 12 roles + conductor. Its roles and class do not change.
2. `handoff.only_template` gains the template-token rule (F4-b). Class **shape**, owner **data**.
3. `null_outcomes.audit` W1 now walks the proof-of-reading list too. Class **shape**, owner **data**. It is the detector of homes. The census rows are `null_outcomes.py` 712-717, and none of them changes.

No new refusal code: `handoff_check:required_rows` already exists (`stage-joints.json:5245`, `fixtures/driver-exits/gates.json:308`). No new joint (axis 38).
Commit lines: the `architecture:` and `judgment:` lines take the form that only `tools/architecture_gate.py` carries. Do not copy it from here. A `judgment: none` always carries its ` -- <why>`.

## 2. Measurement

M1, the list paths, enumerated from the PARSED template. This replaces r1's block-list grep, which missed flow lists and counted `role-to-conductor` `request.tried`/`request.data` as `blocked.*` (t-1215 B2). The walk: for every `handoffs/*.yaml` except `index` and `vocabulary`, take the dicts from the top level down, skip the top-level `CONTRACT_OWNED` keys and `blocked`, and record each list value without descending into it. That is the set `handoff.list_paths` will return (§5 item 1). Today's verdict on an UNTOUCHED form, where every leaf equals the template, works like this:
- a top-level list is empty when `handoff_check._is_empty_section` says so;
- a map-nested list is never empty.

Road B with F4-b: a list is empty when every leaf is a placeholder or carries a `<...>` token.

The command is item 0's probe (full source in §5 item 0). The critic ran the same walk (t-1215 probe1/probe3, t-1219 probe4). Its verbatim output is the expected output of item 0. The designer had no shell in this dispatch, so this source is **not run by the designer** (estimate, not verified). Any difference between the probe's output and the block below stops the node (§6 edge 1).

```
## probe1
s4-case-critic-to-designer:findings is_empty_section=False only_template=True
s4-case-critic-to-designer:questions is_empty_section=False only_template=True
s4-case-critic-to-designer:register_gaps is_empty_section=False only_template=True
s7-automator-to-analyst:rounds is_empty_section=False only_template=True
## probe3
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
## probe4
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
After this block the probe prints a `## probe5` section: every `contract:path` with `new_empty=True`. The card does not pin it. The builder pastes it into row R16 as that row's expected table (§5). Consistency check: every probe3 path appears in probe5.

Counts: probe1 has 4 lines. probe3 has 30 lines, of which 11 are `top=True` (4 flip by recursion alone, which is probe1, and 7 more by F4-b; t-1219 corrected t-1215's "13"). probe4 has 15 `inputs_read` carriers (14 of SCOPE_KINDS produce/review/ledger, plus `s8-scribe-to-gate-b` of kind `report`) and 1 `rounds` carrier.

M2, the product road for the critic today (read). `handoff.py:456-459`: only `scope` is refused when empty. `handoff_check.check` (`:1655-1670`) applies that to top-level list sections only (`handoff.sections` is top-level, `handoff.py:673`). The blank-field loop skips a path only when its top-level section is an empty list (`:1709`). So an untouched `probes.records[0].instance` and `.verdict` are refused `field.blank`. The values writer cannot write `[]`: `_apply_one` writes nothing for an empty value (`handoff_check.py:2731-2732`). So the critic has no legal empty `probes.records`. Real-run evidence: `fixtures/stories/cart-1/work/handoffs/S5-qa-code-critic-7.values.applied.yaml:9-12` (an invented `record: work/probes/none.json` with `not_executed`). The template leaf `record: work/probes/<instance>.json` is not a placeholder (`PLACEHOLDER = ^<(.+)>$`, `handoff.py:31`), so without F4-b the records row never reads as untouched.
- The coverage obligation already has its owner. `controller.py::_code_review_problems` reads the MANIFEST (`sensitivity_proof`, receipt, reason). It never reads `probes.records` or `artifacts.tests` (t-1215, verified). So an empty `probes.records` cannot close a window that has unproven tests.

M3, two facts of the finding corrected. The quoted refusal text belongs to the dry-world filler, `scripts/tests/form_filler.py::_spread_world_rows` (`:481-482`, read). It is pinned by the QUARANTINED `test_form_selftest.py:88` (test-layers.json `quarantine`). `handoff_check.py::_probe_list` derives the automator's `artifacts.probes`, not the critic's `probes.records`. It stays unchanged.

M4, the readers of the required set (grep `REQUIRED_LISTS` over `ai-packages/qa-factory/scripts`: 22 lines in 9 files). These are `handoff.py:459` (definition), `:487`, `:496` (null-outcome key grammar); `handoff_check.py:1661` (refusal), `:2400` (`row_form` fallback); `null_outcomes.py:17` (docstring), `:281-282` (`entry_problems`), `:566-577` (W1); `handoff_init.py:194`, `:203` (`empty_optional_lists`); `scripts/tests/form_filler.py:370` (`emptiable`); `project_decisions.py:45` (comment); tests `test_s7_null_outcome.py:463` (pin `("scope",)`), `test_null_outcomes.py:198,204,249` (synthetic `person:` key), `test_project_decisions_refs.py:95,99` (a quoted string). An NE row in `null-outcomes.json` is a HOME that the audit demands for a carrier the walk meets (`null_outcomes.py:651-662`). It never creates a requirement (t-1219 R1). The walk-size pins are `test_null_outcomes.py:37` `PINS = {"scope": 17, ...}`.

M5, real runs leave the S5 critic's `inputs_read` untouched (read by the designer). The s5-critic template row is `path: <path exactly as the author listed it>` / `version: <...>` (`s5-critic-to-automator.yaml:27-29`). It carries no `<the author's dispatch>` token, so `handoff_init.fill_head` has nothing to prefill (`handoff_init.py:152-160`). Grep `path: <path exactly as the author listed it>|path: work/handoffs/<the author's dispatch>\.yaml` over `scripts/tests/fixtures` gives 8 files: cart-1 `S5-qa-code-critic-2..7` and TP1-12586 `S5-qa-code-critic-2,-4`. Each of them left the row untouched and passed, because today it is empty-legal. Four other critic fixtures carry a filled row (cart-1 `-1`, TP1 `-1`, `-3`, local-1-0108 `-14`). Under this card, an untouched `inputs_read` on the S5 critic is refused. That is the decided verdict change (§6 edge 1, line 31), and its real-run price is fork F-r2-3.

M6, `handoff_check` on a `role-to-conductor` form (t-1219 R5, re-run by the critic). A case-insensitive Grep of `role-to-conductor|role_to_conductor` over `ai-packages/qa-factory`, glob `!**/tests/**`, gives 6 hits, and the only script among them is `handoff_help.py:96`, which writes the request. The positive control is `role-to-conductor.yaml:17`, found by the same call. Item 0 re-runs it.

## 3. The class and the meaning change

Class (P31, AR-23): **the rule "every list but the required ones may be empty; an untouched template row is the empty list" held only at the top level. A list nested in a map was refused field by field, so it was silently required, unwalked and homeless. Meanwhile one list that must not be empty (`inputs_read`, the proof of reading) was required only by accident of its token rows, and on two contracts not at all.**
Meaning change (PROJECT.md package p.6):
1. "An untouched list" now means the same thing at every depth that crosses no list row. The test is `only_template`, which recurses and applies the token rule against the template.
2. The required set is the tuple `("scope", "inputs_read")`, read by name for every contract.
3. The `required_rows` sentence no longer says "in scope".

## 4. Decisions taken (Lead, 17.11.2026, «решила сама»), as this card implements them

- Road B: one empty rule for every list whose path crosses no list row. No dotted `null_outcome` keys. The coverage obligation keeps its one owner, `controller:code_review_receipts` (AR-15). Depth: lists in maps at any depth. A list inside a list row is never judged by this rule.
- F4-b: a leaf that carries a `<...>` token and equals the template's leaf at the same generic path counts as untouched.
- `REQUIRED_LISTS = ("scope", "inputs_read")`. These lists stay empty-legal: the map-nested lists of probe3, the three s4-case-critic lists (which match `handoff_init.EMPTIED`), s8-scribe `questions`, and s7-automator `rounds`. `rounds` carries a priced risk: `fix_result: fixed` beside an untouched `rounds` passes until a live condition lands. The finding text for that condition is in Appendix A. FV3-19 does not wait for it.
- The quarantined pin `test_form_selftest.py:88`: the filler changes, and the Lead runs `tools/test_quarantine.py judge` at acceptance. The builder never touches a quarantine file.

## 5. Builder node FV3-19

given: `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-fv3-19-nested-null-outcome-card-r2.md` (this card, the only spec), `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md` (whole), `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/architecture.md` (AR-10, AR-13, AR-15, AR-18, AR-20, AR-22, AR-23, AR-28, AR-29), `C:/QAFactory/forge-repo/docs/TESTING.md`
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/handoff.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/handoff_check.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/null_outcomes.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/null-outcomes.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/handoffs/s5-critic-to-automator.yaml
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/slices/qa-code-critic/handoff-keys.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/form_filler.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/form-rounds.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_handoff.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_null_outcomes.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_s7_null_outcome.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_detector_verdict.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/changelog.d/fv3-19-nested-list-empty.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/stage-joints.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/slices/qa-automator/handoff-keys.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/slices/qa-bug-reporter/handoff-keys.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/slices/qa-case-critic/handoff-keys.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/slices/qa-case-designer/handoff-keys.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/slices/qa-doc-scribe/handoff-keys.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/slices/qa-failure-analyst/handoff-keys.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/slices/qa-requirements-tester/handoff-keys.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/slices/qa-retro-analyst/handoff-keys.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/slices/qa-runner/handoff-keys.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/slices/qa-scout/handoff-keys.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/slices/qa-test-strategist/handoff-keys.md
non-goals: dotted `null_outcome` keys and any new condition (the `rounds` live condition is Appendix A's later node); sibling yamls other than s5-critic; `handoff_init.py` (`empty_optional_lists` and the prefill stay); `controller.py`; any quarantine file (`test_form_selftest.py`, `test-layers.json`); frozen real-run fixtures under `scripts/tests/fixtures/stories/` and `fixtures/run-*` (evidence, never edited); the finding files (the Lead places Appendix A).
handoff: the builder report (rule 7 `.claude/agents/builder.md`) with item 0's measurement section, the FR walk (A refusals: `required_rows` reaches `inputs_read`; B text: the refusal sentence, the yaml comment and the joint requirement; C contracts: AR-10 joint, FR-11 producer of `inputs_read`; D, E, F: one line each, not touched; G code) and the witness output.
edges: §6
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/handoff.py ai-packages/qa-factory/scripts/handoff_check.py ai-packages/qa-factory/scripts/null_outcomes.py ai-packages/qa-factory/references/null-outcomes.json ai-packages/qa-factory/handoffs/s5-critic-to-automator.yaml ai-packages/qa-factory/references/stage-joints.json ai-packages/qa-factory/scripts/tests/form_filler.py`. Every file it prints must be green: expected among them `test_handoff.py`, `test_null_outcomes.py`, `test_s7_null_outcome.py`, `test_detector_verdict.py`, `test_contract_slices.py`, `test_field_producers.py` and the scenario files (estimate, not verified). `test_judgment_census.py` must raise no count. `python -B ai-packages/qa-factory/scripts/contract_slices.py --check` must exit 0. Item 0's probe output must equal §2 byte for byte.
siblings: axis 5 (stage twins): the 15 `inputs_read` carriers and the map-nested lists of probe3 each get a verdict in §6 edge 1, with no yaml edit beyond s5-critic. Axis 18: no shrink-only ratchet raised. The walk pin and the T6 digest move and are named in the report. Axis 34: one empty rule at every depth that crosses no row, and one required tuple by name, with no per-contract branch. Axis 38 (dry census): no new joint or refusal code. `handoff_check:required_rows` reaches more lists, and its census row `fixtures/driver-exits/gates.json:308` stays unchanged.

Test placement: ONE new parameterised function in `test_handoff.py`, `an_untouched_list_is_empty_at_every_depth_that_crosses_no_row`, joined to the file's own runner the way its neighbours are. A new case is a table row. Edits to existing pins sit in the files named in item 7. No new test file.

Items:

0. **Measure before editing** (a report section, not code, on the UNEDITED worktree).
   (a) Save this source as `<your scratchpad>/fv3_19_probe.py` (not committed) and run `python -B <your scratchpad>/fv3_19_probe.py <worktree>/ai-packages/qa-factory`. Lines `## probe1` through `REQUIRED_LISTS ('scope',)` must equal §2's block byte for byte. Attach the full output. A difference stops the node: return it as a question and do not edit.
   ```python
   import re, sys
   from pathlib import Path
   PKG = Path(sys.argv[1]).resolve()
   sys.path.insert(0, str(PKG / "scripts"))
   import handoff                      # noqa: E402
   import handoff_check as H           # noqa: E402
   TOKEN = re.compile(r"<[^<>]+>")
   def untouched_b(v):                 # road B + F4-b on an untouched form: every leaf equals the template
       if isinstance(v, dict):
           return all(untouched_b(x) for x in v.values())
       if isinstance(v, list):
           return all(untouched_b(x) for x in v)
       return handoff.is_placeholder(v) or bool(TOKEN.search("" if v is None else str(v)))
   def walk(data, prefix=""):
       for key, value in data.items():
           path = prefix + str(key)
           if not prefix and (handoff.owned_by_contract(path) or path == "blocked"):
               continue
           if isinstance(value, list):
               yield path, value
           elif isinstance(value, dict):
               yield from walk(value, path + ".")
   contracts = sorted(p.stem for p in handoff.CONTRACTS.glob("*.yaml") if p.stem not in ("index", "vocabulary"))
   kinds = {str(r.get("contract")): str(r.get("kind")) for r in (handoff.index().get("handoffs") or [])}
   print("## probe1")
   for c in contracts:
       t = handoff.template(c)
       for s, k in handoff.sections(c).items():
           if k == "list" and not handoff.owned_by_contract(s):
               a, b = H._is_empty_section(t, None, s), handoff.only_template(t.data[s])
               if a != b:
                   print(f"{c}:{s} is_empty_section={a} only_template={b}")
   print("## probe3")
   for c in contracts:
       t = handoff.template(c)
       for path, value in walk(t.data):
           top = "." not in path
           old = H._is_empty_section(t, None, path) if top else False
           new = untouched_b(value)
           if old != new:
               print(f"{c}:{path} top={top} old_empty={old} new_empty={new}")
   print("## probe4")
   for name in ("inputs_read", "rounds"):
       for c in contracts:
           t = handoff.template(c)
           if name in t.data:
               v = t.data[name]
               print(f"{name} {c} kind={kinds.get(c, '?')} list={isinstance(v, list)} "
                     f"today_empty={H._is_empty_section(t, None, name)} roadB_empty={untouched_b(v)}")
   print("REQUIRED_LISTS", handoff.REQUIRED_LISTS)
   print("## probe5")
   for c in contracts:
       for path, value in walk(handoff.template(c).data):
           if untouched_b(value):
               print(f"{c}:{path}")
   ```
   (b) Re-run M6 with the same Grep tool call and the same positive control. If the only non-test script is `handoff_help.py:96`, write one report line saying "`handoff_check` never runs on a role-to-conductor form; `request.tried`/`request.data` have no observable change" and add no code for them. If a non-test script runs `handoff_check` on such a form, stop and ask the Lead a question (fork F-r2-4).
   (c) Run rows R1 and R9 on the unedited tree. Both must fail the way §2 M2 says (FR-32).
   (d) Run `python -B tools/owns_readers.py` over the owns (builder rule 12) and attach its block.

1. **`scripts/handoff.py`**
   - Define `ITEM_LIST = "scope"` and `REQUIRED_LISTS = (ITEM_LIST, "inputs_read")`.
   - Rewrite the comment at `:456-458`. `scope` is the item list a handover may not leave empty. `inputs_read` is the proof that the role read what it was handed, and it may not be empty either. Every other list, at every depth that crosses no list row, may be empty, and an untouched template row is the empty list.
   - Add `TEMPLATE_TOKEN = re.compile(r"<[^<>]+>")`.
   - Add `list_paths_of(doc) -> tuple`, which is pure, and `list_paths(contract_id) -> tuple`, which is `list_paths_of(template(contract_id))`. Together they return every list path in document order: walk the dicts, skip the top-level keys for which `owned_by_contract` is true and the top-level `blocked`, record a list without descending into it, and never enter a list. The keys `blocked` and `CONTRACT_OWNED` are skipped because their blanks are never refused anyway (`handoff_check.py:1750`).
   - Change `only_template(value, template=None)`. With `template=None` it behaves byte for byte as today. With a template:
     - a dict recurses against `template.get(key)` when the template is a dict (else `None`);
     - a list recurses each item against `template[0]` when the template is a non-empty list (else `None`);
     - a leaf is untouched when `is_placeholder(value)` is true, OR when `TEMPLATE_TOKEN.search(str(value))` matches AND `str(value) == str(template)`.
   - Rows: R7, R16.

2. **`scripts/handoff_check.py`**
   - **The function.** `_is_empty_section(doc, spec, path, contract=None)`. `path` is a dotted path. The value is read by walking `doc.data` through maps segment by segment. An absent segment, a non-dict on the way, a non-list value, or `[]` returns True, exactly as a top-level section reads today. Otherwise it returns `handoff.only_template(value, tmpl)`, where `tmpl` is the template's value at the same path when `contract` is given and the template is readable, else `None`. With no contract or no readable template there is no token rule, and the recursion works as in `only_template`.
   - **The callers.** `:1421`, `:1610` and `:1872` keep `(doc, None, name)`, with no contract. On the real templates their lists (`scope` and `not_for_repair` of s7-analyst-to-automator, `tried`) are absent from probe1, so they keep their verdicts. `:1629` keeps its argument; it is dead behind `or True`, and that is not this node's business. `:1637`, `:1644`, `:1659`, `:1677`, `:1687` and `:1694` pass `contract`.
   - **The check.** In `check`, `empty_sections` is built over `handoff.list_paths(contract)` instead of top-level list sections. The REQUIRED_LISTS test compares the path exactly (`path in handoff.REQUIRED_LISTS`), so only a top-level `scope` or `inputs_read` is required. The null-outcome branch is unchanged.
   - **The refusal sentence** becomes ``f"no rows. `{section}` is a required list and may not be empty. {_row_sentence(row_form(spec, section, _template_nodes(contract), contract=contract)[1])}"``. The words "in scope" and the scope-only clause "the id, a state and a reason of at most 80 characters" are gone. The row's own fields come from `row_form`. The code `handoff_check:required_rows` and its door are unchanged.
   - **The blank-field loop** skips a path when `path == p` or `path.startswith(p + "[")` for some `p` in `empty_sections`. It replaces the top-level-head test at `:1709`.
   - **`row_form`'s fallback** (`:2400`) reads `handoff.ITEM_LIST`, not the whole tuple. Its docstring at `:2394` says "the item list". Its output is unchanged for every contract.
   - Rows: R1-R6, R8, R11-R15, R17.

3. **`scripts/null_outcomes.py`**: `audit` W1 (`:566-581`) and the docstring at `:17`.
   - W1 tells the item list from the proof-of-reading list:
     - `kind in SCOPE_KINDS` is red when `ITEM_LIST` is not a list section ("carries an item list, and the contract has no `scope`"), and `walked["scope"]` gets every REQUIRED_LISTS name that the contract carries as a list;
     - `kind in NO_SCOPE_KINDS` is red only when the contract carries `ITEM_LIST`, so kind `report` carrying `inputs_read` is legal;
     - the not-a-list red stays for every REQUIRED_LISTS name.
     - Whether `s8-scribe-to-gate-b:inputs_read` is walked depends on fork F-r2-1. The recommendation is to walk every carrier of a non-item required list, whatever its kind, which gives one more home and a pin of 32.
   - `entry_problems` (`:281-283`) and `handoff.null_outcome_entries` (`:487`, `:496`) stay byte-identical. They read the tuple, so the grammar now also admits `inputs_read` as a key (fork F-r2-6).
   - In `test_null_outcomes.py`:
     - `PINS["scope"]` goes from 17 to 31 (17 plus the 14 SCOPE_KINDS carriers of probe4), or 32 under F-r2-1(a). The K0.4 label at `:149` names the new count.
     - Add three variant rows through the file's `audit_syn` helper: kind `report` carrying `inputs_read` gives no red naming it; kind `report` carrying `scope` gives red as today; kind `produce` carrying `inputs_read` and no `scope` gives red "has no `scope`".

4. **`references/null-outcomes.json`**: add 14 `never_empty` rows, NE39 through NE52 in probe4 order, one per SCOPE_KINDS carrier: s2-tester-to-strategist, s3-strategist-to-designer, s4-case-critic-to-designer, s4-designer-to-case-critic, s4-designer-to-runner, s5-automator-to-runner, s5-critic-plan-to-automator, s5-critic-to-automator, s6-runner-to-analyst, s7-analyst-to-automator, s7-analyst-to-scribe, s7-automator-to-analyst, s8-bug-reporter-to-scribe, s9-retro-to-project. Under F-r2-1(a), add NE53 for s8-scribe-to-gate-b.
   - Each row: `"kind": "scope"`, `"carrier": "<contract>:inputs_read"`, `"requirement": "one row per input the role read, with the version it read"`, `"why": "a hand-over that names no input it read cannot be told from one written without reading: the role always reads at least what its dispatch handed it"`, `"guard": "no guard: handoff_check.py::check refuses the empty list (`no rows`), which is the intended outcome; the role's door is `blocked` and handoff_help.py"` (the form of NE1).
   - No other row changes. The `pending` ratchet is untouched.
   - Row: the audit, green (test_null_outcomes K0.4).

5. **`handoffs/s5-critic-to-automator.yaml`**: one comment line over `records:`: "No probe ran, or the window has no new or changed test: leave `records` as it stands (the empty list) and give each such instance its `unverified` row." Then run `python -B scripts/contract_slices.py --write`. This is a comment-only edit, so the critic slice's keys list may not change; say so in the report. Row: R9.

6. **`scripts/tests/form_filler.py::_spread_world_rows`**: factor the predicate `_excused(contract, list_path) -> bool`, which is true when `list_path in set(handoff.list_paths(contract)) - set(handoff.REQUIRED_LISTS)`. `list_path` is the filler's own value at `:477`, with the indexes removed.
   - With no file (`not names`) and `_excused(...)` true: leave the list untouched, with no `Unfillable` and no fill.
   - With no file and `_excused(...)` false, for a required list or an N-row list: `Unfillable` as today. For a required list the text names it as required: ``f"no {what} exists in {dir}/ and `{list_path}` is a required list: it may not be empty"``.
   - `names is None` (cannot read): unchanged.
   - Update `fixtures/form-rounds.json` only where a listed row changes because of this item or lines 31-33 of the closed list, and name each such row.
   - Rows: R10a-c.

7. **Existing pins that state the old behaviour** (edits, not new tests):
   - `test_s7_null_outcome.py:463`: the expected tuple becomes `("scope", "inputs_read")`, and the label says "REQUIRED_LISTS: `scope` and `inputs_read`".
   - `test_null_outcomes.py:40` (`OLD_EMPTY_SCOPE`), `:535` and `:561`, and `test_s7_null_outcome.py:489` and `:505`: the substring "no rows. One row per item in scope" becomes "no rows. `scope` is a required list".
   - `test_detector_verdict.py:1360`: the T6 digest of `'required_rows / fresh form, scope'` is re-captured from the new text. The report prints the new text and its digest, and names this as a pin move.
   - `test_detector_verdict.py:1578-1580`: the fresh critic form's Record list is re-stated. The expected list (an estimate, not verified) is `["handoff_check:required_rows"] * 2 + ["handoff_check:field.blank"] * 5`: `inputs_read` and `scope` are refused, and the two `probes.records[0]` blanks are gone. The report shows the measured list. Any element that lines 17 and 31 of the closed list do not explain stops the node.
   - `test_handoff.py::_critic_form`: it also sets `inputs_read[0].path = work/handoffs/S5-qa-automator-1.yaml` and `inputs_read[0].version = manifest revision 1`, so every existing caller keeps its verdict.

8. **`references/stage-joints.json`**, the `handoff_check:required_rows` row (`:5249`), under F-r2-2(a). Its `requirement` becomes "A required list (`scope`, `inputs_read`) is never empty: one row per entry, in the fields its contract names." `door` and `when` are unchanged. Run `python -B scripts/contract_slices.py --write`, after which the 12 slices' `[handoff_check:required_rows]` line changes and nothing else. Row: T6 `record.expected == told_text(row)` (`test_detector_verdict.py:1576`), green. Under F-r2-2(b), drop this item and its 12 owns lines except the qa-code-critic slice.

9. **`changelog.d/fv3-19-nested-list-empty.md`**: English, no Cyrillic. It says what changed for roles: nested lists may be left empty, `inputs_read` is required on every form that carries it, and the new refusal sentence.

Table rows of `an_untouched_list_is_empty_at_every_depth_that_crosses_no_row` (verdicts after the edit; "form" = `_critic_form` unless named):
- R1: critic form, `probes.records` untouched, `unverified` has `test_one`. No problem path starts with `probes.records`. Today there are two `field.blank`.
- R2: `probes.records[0].instance` real, `.verdict` a placeholder. `field.blank` at `probes.records[0].verdict`, unchanged.
- R3: untouched records row, but `note` filled with a real word. Not empty, so `instance` and `verdict` are refused as blank.
- R4: `scope` untouched on the critic form. `handoff_check:required_rows` at `scope`, with the new sentence.
- R5: `s4-designer-to-runner`, `execution[0].case` real and `preconditions` untouched. The refusal at `execution[0].preconditions[0]` stays (the boundary of depth).
- R6: top-level `findings` untouched, verdict `ok`: no refusal. With a verdict that owes findings: `required_rows.owed_by_verdict`, unchanged.
- R7: pure `only_template`.
  - `{"record": "work/probes/<instance>.json"}` against the same template leaf gives True.
  - `"work/probes/test_x[<lambda>].json"` against the template leaf `"work/probes/<instance>.json"` gives False.
  - `"work/impl-diff.txt"` (no token) gives False.
  - `{"record": "work/probes/<instance>.json"}` with `template=None` gives False, as today.
- R8: `s5-automator-to-critic`, plain check, `artifacts.tests` untouched: no refusal. With `--fix` and a manifest naming a test, the list is derived first, unchanged.
- R9: values file `probes.records: []` gives the note "nothing written", then the form passes on R1's terms.
- R10a: `form_filler.fill_form("s5-critic-to-automator", ctx)` with no `work/probes/*.json`: no `Unfillable` under `probes.records`.
- R10b: a world-list token in `scope` with no file gives an `Unfillable` that names `scope` as required.
- R10c: pure `_excused`:
  - `("s5-critic-to-automator", "probes.records")` is True;
  - `("s5-critic-to-automator", "scope")` is False;
  - `("s5-critic-to-automator", "inputs_read")` is False;
  - `("s4-designer-to-runner", "execution.preconditions")` is False.
- R11: critic form with `inputs_read` untouched (the `_critic_form` values removed) gives exactly one `handoff_check:required_rows` at `inputs_read`. Its text contains "`inputs_read` is required" and does not contain "in scope".
- R12: `s8-scribe-to-gate-b` (kind report) form with `inputs_read: []` has a problem at `inputs_read` with code `handoff_check:required_rows`. Other problems of that form are not asserted.
- R13: `s7-automator-to-analyst` with `rounds` untouched and `scope[0].fix_result: fixed`: no problem path starts with `rounds`. This pins the priced risk as today's behaviour, and Appendix A's node flips this row.
- R14: `s4-case-critic-to-designer` with `findings` untouched: no problem path starts with `findings`.
- R15: `s8-scribe-to-gate-b` with `delivery.reasons_by_owner.product` untouched (the flow list `["<reason>"]`): no problem under it.
- R16: pure, over every contract. The set `{c:path for path in handoff.list_paths(c) if _is_empty_section(handoff.template(c), handoff.spec(c), path, contract=c)}` equals item 0's `## probe5` lines, pasted as the row's table.
- R17 (raw scalar, both depths): a form text with `probes:\n  records: foo`, and one with top-level `findings: foo`. Each reads empty, and there is no problem under either path, the same verdict at both depths.

## 6. Edges, each with its invariant

1. **The closed list of verdict changes.** On an untouched form, measured by item 0 and pinned by R-rows. The only changes are:

| # | contract:path | today | after | code after |
|---|---|---|---|---|
| 1 | gate-a-to-automator:environment.preconditions_accepted_as_blocked | refused | legal | none |
| 2 | gate-b-to-delivery:delivery.do_not_commit | refused | legal | none |
| 3-4 | role-to-conductor:request.tried, request.data | refused if checked | legal if checked; never checked (M6), so no observable change | none |
| 5-6 | s1-scout-to-tester:person.accepted_gaps, person.late_sources | refused | legal | none |
| 7 | s4-case-critic-to-designer:inputs_read | refused | refused | `handoff_check:required_rows` (was `field.blank`) |
| 8, 10, 11 | s4-case-critic-to-designer:findings, questions, register_gaps | refused | legal (matches `handoff_init.EMPTIED`) | none |
| 9, 14, 19, 21, 25 | `stage_acceptance.witness_paths` ×4 and `artifacts.probes` | legal (row fields optional by hint) | legal | no practical change |
| 12 | s4-designer-to-case-critic:review_scope.focus | refused | legal | none |
| 13, 16 | s5-automator-to-critic and s5-automator-to-runner:artifacts.tests | refused (plain check) | legal; `--fix` derives first | none |
| 15, 18, 20, 22, 24 | inputs_read of s5-automator-to-runner, s6-runner-to-analyst, s7-analyst-to-scribe, s7-automator-to-analyst, s8-bug-reporter-to-scribe | refused | refused | `handoff_check:required_rows` (was `field.blank`) |
| 17 | s5-critic-to-automator:probes.records | refused | legal (the target) | none |
| 23 | s7-automator-to-analyst:rounds | refused | legal (priced risk, Appendix A) | none |
| 26-29 | s8-scribe-to-gate-b:delivery.reasons_by_owner.{product,person,stand,factory} | refused | legal | none |
| 30 | s8-scribe-to-gate-b:questions | refused | legal | none |
| 31 | s5-critic-to-automator:inputs_read (untouched) | legal (`today_empty=True`) | refused | `handoff_check:required_rows` |
| 32 | s5-critic-plan-to-automator:inputs_read (untouched) | legal | refused | `handoff_check:required_rows` |
| 33 | any of the 15 carriers: `inputs_read: []` written, or the key absent | legal | refused | `handoff_check:required_rows` |

Lines 1-30 are probe3's 30 lines, in order. Lines 31-32 come from probe4. Line 33 is the tuple read by name.
Invariant: no other form changes outcome. Any other difference, in item 0's output or in a witness file, stops the node and goes back as a question.

2. **A started row is never empty.** A started row is one where any leaf is a real value that differs from the template (R2, R3). Invariant: a half-filled row is never excused.
3. **A list inside a list row is never judged by this rule** (R5, R10c). `list_paths` never enters a list. Invariant: an item's own content stays required together with its item.
4. **An absent key, a non-dict on the way, or a non-list value at a list path reads "empty"**, the way a top-level section reads today. A role can reach the scalar case through the raw `--set probes.records=foo` (`handoff_check.py:2724-2730`), the same as `--set findings=foo` at the top level (R17). Invariant: nothing a role writes reaches a pass at a nested path that it could not reach at the top level. A required list in any of these shapes is refused (line 33).
5. **A required name matches only at the top level** (`path in REQUIRED_LISTS`, exact equality). Invariant: a nested list that happens to be called `scope` or `inputs_read` is judged by the empty rule, never required by accident. This is an internal boundary, so it gets no row (rule 11).
6. **An empty `probes.records` beside a window with unproven tests**: the form passes, and `controller:code_review_receipts` still refuses the unreceipted window (M2). Invariant: an unproven test never closes the window, and the owner of that fact is unchanged.
7. **Position: `--fix` list derivation runs before the empty verdict** (`:1627-1635` before `:1655`). The blank-loop skip runs before any field deriver (`:1708` before `:1728`). Invariant: a list that code can fill whole is never excused as empty. Code never starts a row the role left untouched: for example, `rounds[].verify.witness` is no longer derived into an untouched `rounds` row.
8. **S7's null outcome**: `scope` and `not_for_repair` of s7-analyst-to-automator are absent from probe1 and probe3. `handoff_init.py:201` and `driver_stage_s7.py:258` read `null_outcomes`, which is unchanged. Invariant: S7's null outcome and its refusals keep their fingerprints. The `null_outcome.*` rows of T6 in `test_detector_verdict.py` stay unchanged, and only the `required_rows` row moves (item 7).
9. **Temporal: forms written before this change.**
   - An old form keeps its literal `record: work/probes/<instance>.json`. Under F4-b an old untouched row reads empty, the same as a new one. Invariant: an old and a new untouched form get the same verdict.
   - An old S5-critic form with an untouched `inputs_read` was legal and is now refused (line 31). Frozen fixture forms are never edited.
   - If a keep test or scenario re-judges a frozen fixture with the current checker and turns red, the builder stops and lists the files (fork F-r2-5).
10. **`handoff_init.drop_unowed_acceptance`** deletes only the author-token row of `inputs_read`. In both contracts that hit that path (`s7-analyst-to-automator.yaml:68-75`, `s8-scribe-to-gate-b.yaml:40-46`), literal rows remain. Invariant: code never empties a required list on the role's behalf.
11. **The null-outcome grammar** reads the tuple. A `null_outcome: inputs_read:` block is now well formed if its condition is live. No contract declares one, and S3 "exactly one contract names a null outcome" stays green. Invariant: the grammar's domain equals the required set, which is one rule (fork F-r2-6).
12. **The direction a reused function may err in.** `handoff.only_template` was advice for skeleton emptying and for rows owed. Now it lifts refusals. With a template, it may err only toward "not untouched", the stricter side. Adversarial inputs that must stay on that side:
    - a token literal that differs from the template's;
    - a parametrised id that carries `<lambda>`;
    - a real word in an optional leaf;
    - `instance: ""` (blank, which reads as untouched, the reading top-level lists already have);
    - an angle-bracketed word the role typed, such as `<intended_failure>`. It reads as a placeholder, which is today's rule at the top level and stays unchanged.
    - With `template=None`, the output is byte-identical to today's. So its other callers keep their verdicts: `driver_stage_plan.py:29` and `handoff_init.py:207`, and `handoff_check.py:1677`'s per-row reading.

## 7. Readers of every touched file (rule 7)

Greps (Grep tool, case-insensitive). The pattern `REQUIRED_LISTS|_is_empty_section|only_template|list_paths|null-outcomes|null_outcomes|stage-joints|handoff_check|form_filler|contract_slices|s5-critic-to-automator`:
- over `tools/`: 10 hits in 5 files (`source_split.py` 6, `source-split-carriers.json` 1, `test_dod_gate.py` 1, `test_quarantine.py` 1, `test_test_quarantine.py` 1);
- over `.githooks/`: 0 (control `handoff|pre-commit`: 3 hits in 2 files);
- over `.claude/agents/`: 0 (control `handoff`: 10 hits in 3 files);
- over `.claude/settings.json`: 0 (control `tools/`: 37).
- `.claude/worktrees/**` hits are other sessions' checkouts, not readers.

Package greps:
- `REQUIRED_LISTS` over `scripts/`: 22 lines in 9 files (M4);
- `_is_empty_section\(|only_template\(` over `scripts/`: 17 lines in 4 files;
- `stage-joints\.json|null-outcomes\.json` over `scripts/**/*.py`: 80 hits in 17 files;
- `required_rows` over `scripts/`: 18 hits in 3 files.

| file / name | reader | verdict |
|---|---|---|
| `handoff.REQUIRED_LISTS` | `handoff_check.py:1661` | changes in item 2 (the loop over `list_paths`) |
| | `handoff_check.py:2400` | changes in item 2 (reads `ITEM_LIST`, output unchanged) |
| | `null_outcomes.py:566-577` | changes in item 3 |
| | `null_outcomes.py:17` | docstring, item 3 |
| | `null_outcomes.py:281-282`, `handoff.py:487`, `:496` | code unchanged, domain wider (edge 11) |
| | `handoff_init.py:203` | unchanged (`EMPTIED` holds no `inputs_read`) |
| | `form_filler.py:370` (`emptiable`) | unchanged code. The EMPTY_LISTS variant stops emptying `inputs_read`, and form-rounds.json is checked in item 6. |
| | `project_decisions.py:45`, `test_project_decisions_refs.py:95,99` | unchanged (a quoted string) |
| | `test_s7_null_outcome.py:463` | changes in item 7 |
| | `test_null_outcomes.py:198,204,249` | unchanged (a `person:` key stays outside) |
| `handoff.only_template` | `handoff_check.py` | changes in item 2 |
| | `handoff_init.py:207`, `driver_stage_plan.py:29` | unchanged (`template=None` is byte-identical) |
| `handoff.list_paths` (new) | `handoff_check.check`, `form_filler._excused` | this stream |
| `handoff_check._is_empty_section` | its 11 internal call sites | item 2 names each |
| the `required_rows` text | `test_null_outcomes.py:40,535,561`, `test_s7_null_outcome.py:489,505`, `test_detector_verdict.py:1360,1578-1580` | changes in item 7 |
| | `fixtures/driver-exits/gates.json:308` | unchanged (code, not text) |
| `null_outcomes.py` | `test_null_outcomes.py` | item 3 |
| | `selftest.py` | unchanged (runs the audit, no shape change) |
| | `tools/source_split.py` | unchanged (reads guard refs; the new rows use `no guard:`) |
| `references/null-outcomes.json` | `null_outcomes.py` | item 4, rows added |
| | `retro_numbers.py` (2 hits on one of the two file names, not read further) | unchanged: rows only added, no key or shape change |
| | `selftest.py` | unchanged |
| | `tools/source-split-carriers.json:16` (verify `test_null_outcomes.py`) | unchanged |
| | `tools/source_split.py` | unchanged |
| `references/stage-joints.json` | `stage_joints.py` (THE reader) | unchanged |
| | `contract_slices.py` | the 12 slices regenerated in item 8 |
| | `test_detector_verdict.py:1576` (`told_text`) | follows the row (item 8) |
| | `test_stage_joints*.py`, `dry_exits.py`, `test_contract_slices.py` | unchanged (text only) |
| | `tools/test_quarantine.py:2199` | unchanged (lists the file as a prose carrier) |
| | `tools/test_test_quarantine.py:1487` | unchanged (a synthetic copy) |
| `s5-critic-to-automator.yaml` | `handoff.template` callers, `contract_slices.py` (the critic slice), `form_filler`, `dry_stub.py` (N2h), `test_handoff._critic_form`, `test_handoff_values_main_block.py:58` | comment only. The slice is regenerated in item 5, and the rest is unchanged. |
| `form_filler.py` | `test_field_producers.py` (keep), `dry_stub.py` | item 6 |
| | `test_form_selftest.py` (quarantine) | the Lead's `test_quarantine.py judge` |
| `references/slices/*/handoff-keys.md` | roles via `inject-map.json`; `contract_slices.py --check` | regenerated, never hand-edited |
| `test_*.py` and `changelog.d/` fragment | the CI runner and the release assembly | unchanged |

## 8. Small choices closed by the designer

- `ITEM_LIST` is the one name W1 and `row_form` read for "the item list". The tuple is built from it.
- `list_paths_of` / `list_paths` mirror `sections_of` / `sections` (a pure form for tests).
- `only_template` takes the template as an optional argument, so old callers stay byte-identical.
- `TEMPLATE_TOKEN = <[^<>]+>`, the same regex as the probe.
- `blocked` and `CONTRACT_OWNED` stay out of `list_paths`, as in r1 and the critic's walk.
- The wording of the refusal sentence, the yaml comment, the NE `requirement`/`why`, and the changelog fragment name.
- NE ids continue from the highest, NE38.
- One parameterised function rather than one per row.
- `_critic_form` gains the two `inputs_read` values (`work/handoffs/S5-qa-automator-1.yaml`, `manifest revision 1`), so its existing callers keep their verdicts.
- Editorial fixes from t-1219 folded in without a decision:
  - R3: the no-contract fallback is labelled "no token rule; recursion as `only_template`", not "stricter".
  - R4: the closed list is the full probe3 table, with the five hint-declared paths marked and the expected code per refused path.

## 9. Reading trail

- Card r1 (whole, with its three decision sections); t-1215 (whole); t-1219 (whole).
- `handoff.py` 25-84, 395-540, 590-694; grep for the defs.
- `handoff_check.py` 714-755, 1210-1231, 1414-1423, 1600-1764, 1862-1875, 2390-2425; grep `inputs_read`, `_is_empty_section\(|only_template\(`.
- `null_outcomes.py` 268-297, 480-679; grep `SCOPE_KINDS`, `guard`, `sibling_in`.
- `null-outcomes.json` 1-60, grep of the NE ids.
- `handoff_init.py` 112-227.
- `form_filler.py` 360-380, 455-492, grep `ROW_INDEX`.
- `s5-critic-to-automator.yaml` (whole); `s7-analyst-to-automator.yaml` 36-80; `s8-scribe-to-gate-b.yaml` 20-59; grep `<the author's dispatch>|acceptance_verdict_at` over `handoffs/`; grep `fix_result|^rounds:` in the s7-automator yaml; Glob `handoffs/*.yaml` (24 files).
- `test_handoff.py` 1842-1871, grep `inputs_read`.
- `test_s7_null_outcome.py` 452-469; `test_null_outcomes.py` grep `PINS|REQUIRED_LISTS`; `test_detector_verdict.py` 1352-1373, 1480-1589.
- `stage-joints.json` 5240-5257; grep "row per item in scope" over the package (one carrier row, 12 slices, 5 test lines).
- `fixtures/driver-exits/gates.json` 306-313.
- `judgment-census.json` row 476, rows 712-717.
- Fixture greps for the critic forms' `inputs_read` (M5).
- `docs/TESTING.md` grep `witness-for`; `docs/SIBLING_MAP.md` axis headings 5, 18, 34, 38.
- The finding (head).
- The rule-7 greps of §7.

Needed beyond the manifest: `handoff.py`, `handoff_check.py`, `null_outcomes.py`, `null-outcomes.json`, `handoff_init.py`, `form_filler.py`, the handoff yamls, `test_handoff.py`, `test_null_outcomes.py`, `test_s7_null_outcome.py`, `test_detector_verdict.py`, `stage-joints.json`, `gates.json`, `judgment-census.json`, the critic fixtures, `SIBLING_MAP.md`, the finding.

## Appendix A: the finding text for the `rounds` live condition (for the Lead to place)

Proposed path: `plans/piles/live-run-fvf/findings/20261117-rounds-pustoy-pri-fix-result-fixed.md`

```markdown
# Пустой `rounds` у S7-автоматора проходит рядом с `fix_result: fixed`: нет живого условия, связывающего список с соседним полем

id: — | кучка: `live-run-fvf` | от: карточка FV3-19 r2 (`docs/tasks/specs/20261117-fv3-19-nested-null-outcome-card-r2.md`, §4, приложение A), вердикт t-1219 R2 | приоритет: П2 | кандидат наверх: нет

## Что не так

Класс фабрики: **пустой исход списка законен только при условии на соседнее поле, а условие не выражено — пустой список проходит и тогда, когда соседнее поле говорит обратное (AR-23, AR-28, FR-23)**.

- После FV3-19 (дорога B) нетронутый `rounds` в `handoffs/s7-automator-to-analyst.yaml` читается как пустой список и законен, как и любой необязательный список.
- Но `scope[].fix_result: fixed` (там же, строка 47) утверждает, что ремонт был; ремонт без строки `rounds` (с `changed` и `verify.witness`) — форма, которую проверка пропускает. Риск принят Lead-ом 17.11.2026 (t-1219 R2 (a)) до этого узла; строка R13 таблицы `test_handoff.py` закрепляет нынешнее поведение.
- Различить «ремонта не было» и «забыли раунды» может только соседнее поле: значение `[]` записать нельзя (`handoff_check.py::_apply_one` ничего не пишет для пустого значения), так что нетронутый и объявленно пустой список — одно состояние формы.

## Что именно менять

Выбранное направление (рекомендация t-1219 R2 (b)): живое условие вида `sibling_in` (сейчас `reserved`, `scripts/null_outcomes.py` строка регистра `"sibling_in"`): пустой `rounds` законен, только если ни одна строка `scope` не несёт `fix_result: fixed`.

1. `scripts/null_outcomes.py`: `sibling_in` становится `live` с реализацией (параметры `field: scope[].fix_result`, `in: [fixed]` — данные в контракте, логика в коде, FR-13); пин `registered conditions` и проверка live/impl в `audit`.
2. Грамматика: ключ `null_outcome` допускает только имена `handoff.REQUIRED_LISTS`; `rounds` входит в кортеж по имени (P31: все носители `rounds` получают вердикт — по пробе t-1219 probe4 носитель один, `s7-automator-to-analyst`), с домом `declared` в `null-outcomes.json`-обходе.
3. `handoffs/s7-automator-to-analyst.yaml`: блок `null_outcome: rounds: {condition: sibling_in, params: {...}, words: {...}}`.
4. Тесты — строки существующих функций: `test_s7_null_outcome.py` S3 («ровно один контракт объявляет null outcome» → два), строка R13 `test_handoff.py` меняет ожидание (`fix_result: fixed` + нетронутый `rounds` → отказ с дверью), строка «ни одного fixed + пустой rounds → проходит».

Принципы и правила: AR-23, AR-28, AR-22; FR-23, FR-57 (у автоматора без ремонта есть законный пустой исход), P31.

Решение владельца нужно: нет.
```

## Forks (returned to the Lead; the node runs on each recommendation until decided)

- **F-r2-1: `s8-scribe-to-gate-b:inputs_read`** (kind `report`). The tuple refuses it when empty, but under "14 homes" W1 does not walk it. That leaves a required list with no home, which is the finding's own class.
  - (a, recommended) W1 walks every carrier of a non-item required list, whatever its kind. That means 15 NE rows (NE53 added) and a pin of 32, at the cost of one row.
  - (b) As decided: 14 homes, and this carrier stays unwalked as a named residual.
- **F-r2-2: the joint requirement at `stage-joints.json:5249`** says "one row per item in scope: the id, a state and a reason". That is wrong for `inputs_read` rows (path, version). Every `required_rows` Record carries it as `expected` (AR-10, AR-18, FR-37).
  - (a, recommended) Rewrite the requirement and regenerate the 12 slices (item 8). This adds 13 owns lines.
  - (b) Leave it. Twelve roles are then told a requirement that misstates `inputs_read`.
- **F-r2-3: the real-run price of line 31.** 8 of the 12 S5-critic fixture forms left `inputs_read` untouched (M5), and no code produces it. Each real S5 critic window would draw one `required_rows` round (AR-12 friction).
  - (a) Accept, as R1 decided.
  - (b, recommended) Give it a producer. The s5-critic yaml's `inputs_read[0].path` becomes `work/handoffs/<the author's dispatch>.yaml`, so that `handoff_init.fill_head` prefills it and `--fix` derives `version` (`_version_of`). The cost: one yaml line, one R row, a read of `s5-critic-plan-to-automator` for the same, and a measurement of whether the S5 driver passes the author dispatch to the critic's init. That measurement is not read here.
- **F-r2-4: the YES branch of M6** (a non-test script runs `handoff_check` on a role-to-conductor form). The decisions did not settle it once "AS DATA" was withdrawn. The tuple keys by top-level name and cannot hold `request.tried`.
  - (recommended) Stop and ask the Lead. The node is written that way (item 0b).
- **F-r2-5: frozen fixtures re-judged by a test.** It is unknown whether a keep test or scenario re-checks the 8 untouched-`inputs_read` critic forms with the current checker. If one does, it turns red outside owns.
  - (a, recommended) The builder stops and lists the red files, and the Lead widens owns in a resubmission. The test's expectation changes, never the fixture.
  - (b) Pre-widen owns now. The files are unknown without a run.
- **F-r2-6: the `null_outcome` grammar domain.** Readers `handoff.py:487`, `:496` and `null_outcomes.py:281` read the tuple, so `inputs_read` becomes an admissible declaration key.
  - (a, recommended) Accept: one rule, code byte-identical, no contract declares one. Appendix A's node uses the same road for `rounds`.
  - (b) Restrict the grammar to `ITEM_LIST`. That is a new branch, and Appendix A would then need its own grammar change.

## Lead decisions on the r2 forks (17.11.2026, «решила сама»)

- **F-r2-1: (a).** W1 walks every carrier of a non-item required list, whatever its kind: 15 NE rows (NE39-NE53), `PINS["scope"]` 32. A required list with no home is the finding's own class.
- **F-r2-2: (a).** Item 8 runs: the `handoff_check:required_rows` requirement is rewritten and the 12 slices regenerated (`contract_slices.py --write`, only that line changes on each page).
- **F-r2-3: (b), with a measured fallback.** The builder first measures (one command, in the report) whether the S5 driver passes the author's dispatch path to the critic's `handoff_init`. YES: `s5-critic-to-automator.yaml` `inputs_read[0].path` becomes `work/handoffs/<the author's dispatch>.yaml` so `fill_head` prefills it and `--fix` derives `version`; one R row in `test_handoff.py`; `s5-critic-plan-to-automator` is read for the same and gets one report line (edited only if it has the same untouched-row shape AND is in owns, which it is not: then a report line naming it as a residual for the Lead). NO: fall back to (a) (the decided verdict change, priced), the report names the measured cause, and the Lead files the producer node.
- **F-r2-4: stop and ask** (item 0b as written).
- **F-r2-5: (a).** A keep test or scenario that turns red by re-judging a frozen fixture stops the node with the list of files; the Lead widens owns in a resubmission; the test expectation changes, never the fixture.
- **F-r2-6: (a).** The grammar reads the tuple; `inputs_read` is an admissible declaration key; code byte-identical.
- Appendix A is placed as `plans/piles/live-run-fvf/findings/20261117-rounds-pustoy-pri-fix-result-fixed.md` and row FV3-30 of batch 3.
- critic on this r2: skipped -- every fork is decided on the designer's recommendation (F-r2-3 adds only a measured producer); no field meaning changes beyond what plan critic t-1219 reviewed; the code diff gets the topic critic.
