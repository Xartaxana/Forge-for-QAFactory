# FV3-30 (t-1513) build report

## Plan items
1. null_outcomes.py: `sibling_in` live, impl `handoff_check.py::_sibling_in_view`, params field/in as data - DONE (null_outcomes.py, handoff_check.py)
2. Grammar: `rounds` in `handoff.REQUIRED_LISTS` - DONE (handoff.py)
3. yaml block `null_outcome.rounds` (field `scope[].fix_result`, in `[fixed]`, words) - DONE (s7-automator-to-analyst.yaml). The words key is quoted, because unquoted `scope[].fix_result:` is mis-parsed by the contract parser.
4. Tests: S3 now two contracts + REQUIRED_LISTS pin (test_s7_null_outcome.py); R13 changed, R13b/c/d, a door row, R13e/f investigation rows (test_handoff.py) - DONE
5. Registered-conditions pin: the count stays 12 (the row existed). The live/impl audit row is `null_outcomes.audit`, unchanged code, green on the real tree.

## Choices (lead answers 1-3)
- Seam: `_sibling_in_view` returns ([], []) for a NON-EMPTY `rounds`, so the condition is "not consulted" in effect; `check` is not guarded. `_null_outcome_impl` is unchanged.
- `_view_for(entry, investigating)` replaces the two selection sites in `check` (not the --fix site: sibling_in opens no rows). `_investigation_view` is used only for `triage_has_no_repair`, so scope/not_for_repair verdicts and every other contract are unchanged.
- Code `handoff_check:required_rows` reused (no new refusal code, no registry file touched).
- Exact refusal text: "no rows. `rounds` is empty, and `fixed` in `scope[].fix_result` says a repair was made: N `scope` row(s) say it (<ids>), but no repair round is recorded."
  Door: "add the `rounds` row for each (changed, verify.witness), or set `fix_result` to what really happened"
- Edges: scope absent/empty -> legal; fix_result absent/null/`Fixed`/placeholder -> not fixed (exact match; R13c; report line: case variant treated as not fixed); a field not of form `<list>[].<leaf>` -> refused (fail closed).

## Witness
`python -B <scratch>/run_nodes.py test_handoff::an_untouched_list_is_empty_at_every_depth_that_crosses_no_row test_s7_null_outcome::every_other_contract_behaves_as_it_did` (these functions are not pytest-collectable; `python -m pytest ...::fn` says "not found", so a 6-line driver calls them through harness):
    PASS R13 rounds untouched beside fix_result fixed: refused (FV3-30, sibling_in)
    PASS R13b ... legal / R13c ... legal / R13d ... legal / R13e / R13f
    PASS S3: two contracts name a null outcome ...
    === nodes: 43/43 ok ===
`registry_preflight check lint read-json driver-layers census --paths <handoff, null_outcomes, handoff_check>`:
    lint ok, read-json ok, driver-layers ok
    census RED: window_record.py::judge_door is a check unit (u1) with no row in judgment-census.json
  (window_record.py is not in my diff; not caused by this change.)
not run locally: the rest of both files, canon judges.

## Needed from integration (RED consequences outside owns)
test_null_outcomes.py (not owned) fails on the real tree, measured: PINS["scope"] 32 -> 33 (rounds is now a walked carrier, home `declared`);
K0.4 sizes 32 -> 33; "homes" (1,33,52) -> (2,33,52); K0.8 summary text `walked scope 33 ... declared 2`; K0.3 "exactly one condition is live" ->
['sibling_in','triage_has_no_repair'] and the "reserved for node N1" text now needs another reserved condition (e.g. sibling_equals, N4/N6).
Card F-r2-5(a): no frozen fixture was re-judged by me; these are keep-test expectations, so I stopped there.
Not run: form_filler.py (tests helper) `_excused`/required-set now treat `rounds` as required-list; handoff_init.py:190 no longer initialises `rounds`. Noticed analogs; not measured.

## Config keys: none. Changelog fragment: Lead writes it. Tests added: ~18 lines vs ~44 code lines.
