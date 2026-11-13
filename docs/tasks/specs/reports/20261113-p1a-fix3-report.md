# t-547 (attempt 2): P1-a fix round 3 - `<cases_root>` from a FillContext key

Worktree `.claude/worktrees/p1a-fix3`, branch `wip/p1a-fix3`, base 535ce4d. Hash: in the handoff message (the report is committed with the code).

## What was done
- `form_filler.FillContext` gained `cases_root: str = ""`.
- `form-fill-rules.json` gained the data row `context_fallback_tokens: {"<cases_root>": "cases_root"}` (placeholder -> context key; one rule, no per-placeholder code branch). In `fill_form`, the deferred step now reads: the form's own plain field value first (`form_field_tokens`, unchanged: the s4-designer-to-case-critic form keeps using its own field), else the context key the fallback row names, else `Unfillable` naming the token, the field and that the context holds no value (unknown never becomes filled).
- Source of the value (not a constant in the filler): the test builds the world with `harness.mark_project` (shipped template config, `cases_root: ""`) and asks the product's reader: `scripts/contract.py:3339 cases_root(artifacts)` (reads `config.cases_root` at :3355 through `_project_config`, default `artifact(art, "test-cases")` at :3356). New helper `_world_cases_root(world, task)` in `test_field_producers.py` renders its answer as the path a form names (relative to the story): in this world `work/test-cases`. Used by the form walk (`every_form_fills_from_its_own_hints`, a `project/` world under its temp root) and by `_accept_form` (round world: `w.world`, `w.task`), which now takes `w`.
- The two `accept:` cascade rows are green by the fill itself (ledger untouched).
- Two new rows in `form_filler_hint_cases`: fallback used when the form has no field; the form's plain field beats ctx.cases_root. Existing rows (no field + no ctx key -> unfillable; no case -> unfillable) still pass unchanged.

## Placeholders in the forms (`handoffs/*.yaml`, grep `<name>` inside paths/values) and coverage
`<cases_root>` is the only one a config key answers (covered: s4-case-critic-to-designer inputs[1].path, s4-designer-to-runner inputs[1].path, s5-automator-to-runner inputs_read[1].path; s4-designer-to-case-critic has its own field). Already covered by existing `context_tokens` rows: `<TICKET>`, `<dispatch>`, `<the author's dispatch>`, `<case>`, `<area>`. Not config-answered and not added: `<plan_revision>`, `<hash>`, `<instance>`, `<n>`, `<file>`, `<read>`, `<handed>`, `<reason>`, `<S>`, `<T>`, `<role>`, `<word>`, `<id>`, `<path>`, `<text>`, `<refs>`, `<dir>`, `<value>`, `<line>`, `<contract>`, `<fill>`, `<case id>`, `<instance id>` etc. - they are hints/templates of fields or kept-in-contract text, no config key answers them, no context key added.

## Summary before (round 2, 535ce4d) / after
| | round 2 | round 3 |
|---|---|---|
| unfillable | 11 | 8 |
| literal | 7 | 7 |
| left_for_code | 82 | 82 |
| kept_in_contract | 9 | 9 |
| known red rows | 29 | 29 |
| not in world rows / pin | 47 / 47 | 47 / 47 (unchanged; s5-automator-to-runner inputs_read[1].version stays there) |
| ok/total | 910/921 | 915/915 |
| wall seconds | 15.7 | 17.4 |
| pairs / languages | 35 / 4 | 35 / 4 |
No pin moved (axis 18). No new known_red / not_in_world row. form-rounds.json untouched.

## Witness (verbatim tails)
`( cd <worktree>/ai-packages/qa-factory && time python -B scripts/tests/test_field_producers.py )`:
```
PASS known_red: the red rows of the walk are exactly the ledger
known red rows 29, not in world rows 47, rows walked 904

=== test_field_producers: 915/915 ok ===

real	0m17.365s
```
Summary lines of the same run: `forms 24, variants 434, fields 980, unfillable 8, literal 7, left_for_code 82, kept_in_contract 9`; `readers 19, pairs 35, languages 4`; `grep -c FAIL` = 0.

`python -B scripts/tests/test_judgment_census.py` -> `=== judgment_census: 24/24 ok ===`
`python -B scripts/selftest.py --lang` -> `=== qa-factory selftest: 2/2 ok ===`

B2 probe re-run (source: round-2 report, with `cases_root="work/test-cases"` added to the context; copy at the session scratchpad `b2_probe.py`): `unfillable 8, literal 7, left_for_code 82, kept_in_contract 9, silent 0`.

## Siblings / notes
- Axis 34: the placeholder -> context key lives in one data row; a second such placeholder needs only a row, no code.
- `_text_of` (artifact tokens) has its own `artifact_tokens` table: same shape, a different walk; not touched.
- Needed beyond the manifest: `scripts/contract.py` (reader), `scripts/tests/harness.py` (`mark_project`), `references/templates/config.json`, `handoffs/*.yaml`.

## Commit lines
```
architecture: AR-20, AR-22 -- no pin moved and no ledger row added (the two accept cascades turn green by the fill); `cases_root` is a produced context value read by the filler (producer: the product's own contract.cases_root in the world, reader: the form fill)
judgment: none -- test-side data checks only
```
