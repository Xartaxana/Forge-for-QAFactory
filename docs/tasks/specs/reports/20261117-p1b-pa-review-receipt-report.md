# t-1071 node P-a: review receipt deriver reads the dispatch through `_form_dispatch`

## Done
1. `_review_receipt` (scripts/handoff_check.py) now resolves the dispatch only through `_form_dispatch(art, doc)`; its own `header.dispatch`/`dispatch` lookup and the dead `getattr(art, "dispatch")` fallback are removed; the stale comment in `Artifacts.__init__` and the phrase "`_review_receipt` keeps its own order" in `_form_dispatch`'s docstring are removed.
2. Test: `the_review_receipt_is_the_form_own_dispatch_window_and_no_other` in test_handoff.py, one table, rows a-e, driving `H.check(..., fix=True)` on a `s5-critic-to-automator` template doc (no header.dispatch, except row e) with `Artifacts(task, dispatch=<stem>)` - the seam main() uses (`Artifacts(root, dispatch=path.stem)`).
3. known_red.json `main/S5`: only `raised_by` replaced with the exact text; node FV3-20 and pins.known_red 1 unchanged. Slow dry pass not run. No fast test turned red on it.
4. Fragment `ai-packages/qa-factory/changelog.d/p1b-review-receipt-form-dispatch.md`.

## Edges
- (a) own window present -> `work/windows/<D>.json`. (b) absent -> blank, hint unchanged. (c) only another dispatch's window -> blank.
- (d) a stem that is no dispatch id (`S5-qa-code-critic-1.values`): `_form_dispatch` returns the stem as-is (`S5-qa-code-critic-1.values`); `work/windows/S5-qa-code-critic-1.values.json` does not exist, so None, field blank (row d has the plain window present to prove it is not matched).
- (e) header.dispatch (`S5-other-7`) different from the stem: the stem wins, so the path is the stem's window. BEHAVIOUR CHANGE: before, header.dispatch won over the stem.

## Old-code FAIL of row (a) (byte copy, no git checkout)
sha256 new before: 033331ef0874521ede207cc7f25f14ddbee1a548ec9360efd06dcdb53ee600ba
Old function put in place (sha d2f2d760...a04600), run of test_handoff.py:
```
FAIL P-a a own window present: the receipt path — expected 'work/windows/S5-qa-code-critic-1.json', got '<work/windows/<this dispatch>.json, written by window_record.py>'
PASS P-a b no window file: the field stays blank
PASS P-a c only another dispatch's window: the field stays blank
PASS P-a d stem is no dispatch id: the field stays blank
FAIL P-a e header.dispatch differs: the stem wins: the receipt path — expected ... got '<work/windows/<this dispatch>.json, ...>'
```
Restored from the byte copy; sha256 after: 033331ef0874521ede207cc7f25f14ddbee1a548ec9360efd06dcdb53ee600ba (equal to before).

## Witness (`scenario_walk.py --witness-for ai-packages/qa-factory/scripts/handoff_check.py`; run in ai-packages/qa-factory; test_scenario_dry_1 skipped as slow)
```
scenario cart-1: 15/15 ok | local-1-0108: 15/15 ok | local-1-arm-b: 5/5 ok
test_artifact_writers 23/23 | test_brief_pack_s5_plan 250/250 | bug_records 422/422 | check witness 34/34
test_field_producers 885/885 | guard 214/214 | test_handoff: 675/675 ok | handoff inline values 83/83
test_handoff_values_keys 103/103 | values_main_block 47/47 | values_refusal 6509/6509 | judgment_census 25/25
test_knowledge_notice 15 passed | test_null_outcomes 327/327 | test_open_list_fields 15 passed
test_s5_plan_controller 101/101 | test_s7_investigation_replay 67/67 | test_story_step_start 169/169
test_triage_blocked 50/50 | test_triage_identity OK   (all rc=0)
python -B scripts/selftest.py --limits --lang:
PASS limits: SKILL.md / agents / references within size caps
PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier
=== qa-factory selftest: 4/4 ok ===
```
Commit hooks: `gates: ok (7 checks)`, `gates: ok (4 checks)`.

## FR walk
- A: FR-5 - the field's producer now exists for the critic form (the window file); no stage requires an artifact nothing produces. FR-1/2/4/46/48/50/57: not applicable - no refusal text or door changed (hint text unchanged).
- B: not applicable - no text a person reads changed.
- C: FR-11 - `review.receipt_ref` is a required field; the deriver code runs on `--fix` can now produce it. FR-12/13/14/15/38/39/42/49/56: not applicable - no contract, shape or tool list changed.
- D: FR-16 - the identifier comes through the one reader of the dispatch; FR-17 - the deriver is wired through the same reader as its siblings. FR-18/40/58/59: not applicable.
- E, F: not applicable - no delivery or measurement changes.
- G: FR-32 - root cause fixed (wrong lookup), with a test row that fails on old code; FR-54 - siblings walked below. FR-29/30: English only, no control bytes.

## Siblings (reported, not changed)
Other readers of `header.dispatch`/`art.dispatch` seen in handoff_check.py: only `_form_dispatch` itself (`:176-177`); `getattr(art, "form_dispatch")` at ~`:821` (scope_cases) and `art.form_dispatch` at ~`:958`, `:1516` read the stem directly, bypassing `_form_dispatch` (they differ from it only when the stem is empty). No other `art.dispatch` reader remains.

## Notes
- Needed beyond the manifest: none besides `scenario_walk.py` output and `handoff_check.py` main (`:3011`, `:3180`) for the stem seam.
- tests-over: rows per edge of the deriver (in commit message).
- No file outside `owns` edited. Not pushed.
