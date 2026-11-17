# t-916 attempt 2 -- fix round under critic t-922 (Stream A)

DoD: `( cd C:/QAFactory/forge-repo/.claude/worktrees/agent-ae7f47813d0989cf3 && python -m pytest tools/test_tier_ladder.py tools/test_mechanism_gate.py tools/test_mechanism_gate_md.py tools/test_savings_report.py -q -p no:cacheprovider )`

Output (run once at the end, verbatim tail):

```
...........                                                              [100%]
731 passed in 5.15s
```

Changes are STAGED on top of c61bcd4e (6 files), not committed.

| finding | what changed | test row |
|---|---|---|
| F1 | `mechanism_gate.decide_full`: `tier_ladder.effective_bindings(config_text)[1]` appended to BOTH refusals ("No tier line", "Not lead tier") as ` (delegation.config.yaml: <note> -- the default bindings apply where no lead is read, lead=<b>; fix the file)` | `test_decide_full_tier_line_table`: `broken-yaml-opus`/opus -> "not readable YAML", `oversize-opus`/opus -> "over 64 KB", both with fable -> 0; `test_decide_full_no_tier_line_refusal_carries_the_config_note_too` |
| F2a | "Not lead tier" text adds "; expected the lead binding or a model ranked lead or above on tools/tier_ladder.py" | table row `fable-lead`/opus fragment "expected the lead binding or a model ranked lead or above" |
| F2b | `list_commits`: in sha mode a git failure appends "(a value of 7-40 hex digits is read as a commit sha; a date is YYYY-MM-DD)" | `test_list_commits_git_failure_hints_the_sha_reading_in_sha_mode_only` ids `date-without-dashes-read-as-sha` (20261116), `sha`, `iso-date` (no hint) |
| F3 | `function_of_session`: defaulted note is `default bindings used (<real note>)` instead of the fixed "config unreadable" | `test_function_of_session_on_default_bindings_names_the_real_reason` (broken, absent, `no-lead` = readable config with no lead, alias-bomb); the two old default rows moved out of `test_function_of_session_table` |
| F4 | `savings_report.top_tier_model`: reads `found, note = bindings(text)`; PricesError names `note` when nothing was read, else "roles.lead names no model" (+ note if any) | `test_an_unresolvable_binding_is_a_prices_error...` now has a `reason` per row: no-roles, empty-roles, empty-model, `lead-missing`, broken-yaml ("not readable YAML"), `alias-bomb` ("alias") |
| F5 | tests only | `test_bindings_table` rows `judge-analyst-designer-not-read`, `architect-empty-model-no-rung`; `test_a_designer_id_never_ranks_through_the_config` (designer-only non-Claude id ranks None) |
| F6 | row now declares the family word `opus` | `test_tier_declared_ok_table` `lead-equals-critic-opus` / "opus" |
| F7 | commit message is the Lead's; text for it: `tests-over: one new test file by the owner's word (P34); 40 single-assert tests folded into tables; net test lines -122` | n/a |
| F8 | Lead's spec edit, not done here | n/a |

Key 1 control values: unchanged logic in `tier_declared_ok`/`rank_of_model`; the existing table rows (today: fable ok, claude-fable-5-2 ok, opus refused, sonnet refused; after: opus ok, claude-opus-5-5 ok, fable ok, sonnet refused) are still green in the run above. Bad/missing/oversize config rows give the defaults (new rows above), never a crash.

Deviations: F3 note wording is `default bindings used (<note>)` (the report's example text was "e.g."). F1 note text is appended also for an absent config (note "config absent") and for the `roles.reserve` rename note, since the spec says "when not None"; the "default bindings apply where no lead is read" clause is then slightly generic for the reserve note (lead bound). F5(a) in the bindings table uses a fable designer (found holds no designer); the "rank of the designer id is None" part is a separate test with a non-Claude designer id, because a fable id would rank by family.

Questions: none.

Needed beyond the manifest: none.
