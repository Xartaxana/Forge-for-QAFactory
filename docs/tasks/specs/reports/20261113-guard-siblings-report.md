# t-537 report: guard siblings (stand_identity / report_adapt / story_step)

Done: the three regexes in `human_word_check` now call `registry_write_call` (PK2-9 helper). Same `or` chain, same order, same outer condition; refusal texts untouched.

Deviation (one signature extension): the helper's read-verb set was fixed (`show`, `state`, `lessons`). With it, `stand_identity.py validate --file confirm.json` (existing test K34) was refused, because the walk continued past `validate` and matched `confirm.json`. The helper now takes an optional `reads` argument (default unchanged, so PK2-9 callers behave identically): stand_identity `("show","validate")`, report_adapt `("show","understood")`, story_step `("finish",)`.

Option value equal to a write word (`stand_identity.py --note confirm show`): refused, exactly as PK2-9 decided for `--note role show`; door = quoted value or the conductor.

Tests: `test_option_before_subcommand_sibling_scripts` (one table, ids name script + case: none/opt-value/flag/two options, list form, read verbs, longer token `confirmed`/`kinds`/`decide-later`, unquoted value, name only, empty/None, K34 control).

FR walk: A - refusal texts unchanged (FR-1/2/4/57: no new refusal, a ban gains no bypass, doors as before). G - FR-30 English only (selftest --lang green), FR-29 no escape bytes, FR-54 siblings via map: below. B, C, D, E, F - not touched.

Siblings noticed (not fixed): other `script\.py ... subcommand` shaped recognizers: none further in `human_word_check` (ticket_adapter/waiver/source_exclusions use substring/flag checks, not subcommand-after-name). Not searched in stage_guard.py beyond a quick look; no hit seen. Fast-file set of `--witness-for` also contains slow files (named in witness).

Commit lines: `architecture: AR-15 -- one helper for every script's subcommand recognition`; `judgment: none -- the guard matches the command's shape; whether a call is legitimate stays with the person and the conductor`.
