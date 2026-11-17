# t-935 -- architect-tier stream B (journal gate and writer by function rank)

DoD: `python -m pytest tools/test_journal_validator.py tools/test_journal_write.py tools/test_agents_md.py -q -p no:cacheprovider`

Output (verbatim tail):

```
$ python -m pytest tools/test_journal_validator.py tools/test_journal_write.py tools/test_agents_md.py -q -p no:cacheprovider
........................................................................ [ 14%]
........................................................................ [ 29%]
........................................................................ [ 44%]
........................................................................ [ 59%]
........................................................................ [ 74%]
.......................................................................s.ssssssssss..s.. [ 89%]
....................................................                     [100%]
472 passed, 12 skipped in 58.11s

$ python -B tools/agents_md.py --check
AGENTS.md: up to date (123421 bytes)      (exit 0)
```

(12 skipped = the same machine-capability skips as before the change: bash-dependent rows; the run before my edits showed
`6 failed, 379 passed, 12 skipped`, the 6 being exactly the judge-legal rows and the FORM_FIELDS pin the block names.)
Extra, outside the DoD, same worktree: `python -m pytest tools/test_journal_validator_merge.py tools/test_journal_validator_node.py
tools/test_journal_per_developer.py -q -p no:cacheprovider` -> `287 passed in 99.48s` (they call the shared functions I changed).

All six owned files are STAGED, nothing committed.

## item -> change -> test row ids

| item | what changed | test rows |
|---|---|---|
| B1 | `journal_validator.py`: `TIER_ORDER`, `AGENT_TIER`, `LEAF_CATEGORIES` deleted; `_matrix_d0058_violation(event, agent, by, obj, config_text=None)` now ranks by `tier_ladder.rank_of_model(by, cfg)` vs `rank_of_function(agent)` in the 3.1 order (lead/architect/unknown agent no-matrix -> `by not in FAMILIES` FAIL -> judge refused -> ok_rank -> floor -> critic -> queued-to-lead band -> generic). Config read by `read_config_text(root)` from the root of the repo being validated (default: git root of the cwd); `config_text` keyword on `decide`, `decide_with_warnings`, `validate_new_lines`, `_line_form_violations`; merge mode (`_foreign_line_violations`) reads it too. `journal_write.py` passes `read_config_text(root)` of its own `--repo` root. | `test_matrix_by_function_rank[after-*]` (every cell of 3.1), `[today-*]` (the six transitional pairs + 3), `[default-*]` (cfg None), `[after-no-architect-key-*]` (F22: a higher-ranked acceptor passes), `[by-model-id]`, `[by-function-word-lead]`, `[by-capitalised]`, `[by-padded]`, `[by-alias]` |
| B1 edge | absent file -> DEFAULT_BINDINGS silently; unreadable (OS/utf-8 error), unparsable, alias, oversize, no lead model -> ONE stderr `WARN: delegation.config.yaml unreadable (<reason>) -- default bindings (lead=fable) used; fix the file`, never a FAIL | `test_config_comes_from_the_root_of_the_validated_repo[absent/after/today/unparsable/alias/not-utf8/oversize/no-lead]` (each runs twice, WARN counted once) |
| B2 | judge branch -> refusal text of 3.1 on any agent/category/by, before ok_rank | `test_matrix_by_function_rank[judge-*]` (7 rows: scout/recon haiku, scout/recon fable, builder/recon fable, builder/implementation sonnet, critic fable, designer opus, empty category), `[by-function-word-architect-with-judge]` |
| B3 | new `matrix_warnings()`: `queued to itself` WARN when a passed line has `basis: queued-to-lead` and rank(by) >= lead | `test_matrix_warns_on_a_passed_line[after-opus-critic-queued-*]`, `[today-opus-critic-queued-no-warn]`, `[after-sonnet-critic-queued-no-warn]` |
| B4 | same function: `INDEPENDENT CONTEXT` WARN for `accepted` critic/designer at rank(by) >= lead with no earlier `delegated` of that agent on that task whose `worker_ref` starts `agent:` (state = seed + HEAD + earlier new lines); wired into `decide_with_warnings`, the merge tail and `journal_write.write_event` messages | `test_matrix_warns_on_a_passed_line[after-opus-critic-agent-ref / -cli-ref / -retro-ref / -other-agents-agent-ref / -nothing-delegated, after-opus-designer-*, after-fable-*, today-fable-*, today-opus-critic-no-warn, after-opus-scout-no-warn]` |
| B5 | validator: `escalated` + `agent: architect` + unseen id -> novelty rule (9a'') instead of the "does not reference" violation; any other agent unchanged. Writer: `escalate --task` optional; refused naming `--task` unless `--agent architect`; `_opens_task()` makes the writer issue the id (or check a given unseen one) for architect escalations | `test_escalated_architect_may_open_a_task[architect-opens-task / architect-existing-task / other-agent-unseen-task / architect-non-canonical / architect-jump]`; writer: `test_escalate_to_the_architect_may_open_a_task[issued-by-the-writer / existing-task]`, `test_a_violation_or_bad_input_writes_nothing_and_says_why[escalate-other-agent-without-task / escalate-architect-unissued-task]` |
| B6 | validator: `reviewed_through` in `_line_form_violations` (shape `^[0-9a-f]{7,40}\Z`, `calibrated` only), added to `FORM_FIELDS`; writer: `calibrated --reviewed-through` | `test_reviewed_through_is_a_sha_on_calibrated_only[sha-7 / sha-40 / upper / six-chars / forty-one-chars / non-hex / trailing-newline / not-a-string / on-accepted / on-delegated]`; `test_form_fields_vocabulary_and_pairs_cover_every_check` (new case); writer `test_events_without_a_task_write_their_shape[calibrated-reviewed-through]`, `test_a_violation_or_bad_input_writes_nothing_and_says_why[reviewed-through-upper / reviewed-through-six-chars]` |
| B7 | `agents_md.py` `tier_words` -> AST of `tools/tier_ladder.py` `FAMILIES` (tuple or list literal); new constant `LADDER_REL` | `test_tier_words_from_validator` (fixture now writes `tools/tier_ladder.py`), `test_tier_words_follow_the_ladder_home_not_a_constant`, `test_missing_ladder_home_exit_2`; `--check` clean (output text unchanged, same word order) |

## Judge rows: flipped / removed (the block asked for the list)

Removed (each only tested the category/agent narrowing or a legal judge pass; replaced by the `judge-*` rows above):
`test_pair_boundary_haiku_by_judge_basis_leaf_still_passes_unaffected_by_floor`,
`test_matrix_designer_judge_basis_fails_regardless_of_category`,
`test_matrix_builder_judge_basis_implementation_still_passes_not_broken`,
`test_matrix_scout_judge_basis_recon_still_passes_not_broken`,
`test_matrix_critic_judge_basis_leaf_category_now_fails`,
`test_matrix_judge_basis_passes_on_recon_category`,
`test_matrix_judge_basis_passes_on_implementation_category`,
`test_matrix_judge_basis_fails_on_non_leaf_category`,
`test_matrix_judge_basis_fails_when_category_missing`.
Kept unchanged: `test_unknown_by_fails_before_judge_branch_even_on_leaf_category` (still true: the enum check precedes the judge refusal).
No other expectation edited.

## Deviations / decisions to check

1. WARN shape: the spec writes `WARN: INDEPENDENT CONTEXT: ...` / `WARN: queued to itself: ...`; I emit them through the module's one
   dated-WARN shape `_warn_line(tag, text)` -> `line N event='accepted' task_id='t-..': WARN INDEPENDENT CONTEXT: <task> accepted at by=<by>
   with no agent:<id> delegated of <agent> -- a review must come from a separate worker context (a warning only, the journal is not blocked)`.
   The words of the spec text are all there; only the prefix follows the existing shape (AR-18). Calibration check 6 (stream F) should grep `INDEPENDENT CONTEXT`.
2. `reviewed_through: null` is treated as absent (the convention of `via` / `session`); a non-null non-sha (number, list) is a violation.
3. Absent config file is silent (the block's edge: "absent there -> DEFAULT_BINDINGS"); spec 2.4 says the note is printed once for an
   "absent" config too -- the block's `edges:` line separates "absent" from "unreadable", I followed the block. One-line change in `read_config_text` if the Lead wants the note on absence.
4. `agents_md.py` text: the generated "Journal note" still says "`TIER_ORDER` of `tools/journal_validator.py`" and still lists "judge" as a basis for a
   leaf. I did NOT touch that text: changing it changes AGENTS.md and `--check` would fail (AGENTS.md is not mine; stream L regenerates it together with CLAUDE.md). The word list itself now comes from `FAMILIES` (identical output).
5. The `read_config_text()` default root is cached per cwd (`_CONFIG_ROOTS`) so merge mode does not run `git rev-parse` per foreign line; the WARN-once set is `_CONFIG_WARNED` (module state, once per process).
6. Tests: `test_journal_validator.py` net +~230 lines of tables, `test_journal_write.py` +~25; the old per-judge functions (9) removed. No new file. No `tests-over` claim from me (volume not measured by me).

## Questions

none.

## Analogs noticed (not fixed; outside `owns`)

- `tools/journal_echo.py` and `tools/test_journal_echo_r3.py` (`test_s4_basis_judge_silences_unconditionally`, rows `_l(..., basis="judge")` at :175, :555): the echo still treats `basis == "judge"` as a silencing basis; the validator now refuses it, so that branch is dead code for new lines (stream D/E owner or a queue item).
- `journal_validator.py` docstring/rule-text mentions of "judge" in the form check for `category` (rule 2 text "basis='judge' becomes unverifiable") and comments in `test_journal_validator.py` that still say `TIER_ORDER` / `AGENT_TIER` (:554, :574, :589, :626, :800, :826): stale prose, no behaviour.
- `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` / `log_append.py` consume `BASIS_VALUES` (kept as a plain enum, unchanged) -- nothing to do; `LEAF_CATEGORIES` had no other reader (Grep over `tools/*.py`: only the validator and its test comment), so it is deleted.

## needed beyond the manifest

`tools/journal_keys.py` (`is_canonical`, `ID_JUMP_MAX`, `parse_id`), `tools/journal_echo.py` (the judge analog), `delegation.config.yaml` (role layout for the test configs), `tools/test_journal_validator_merge.py` / `test_journal_validator_node.py` / `test_journal_per_developer.py` (extra sanity run).

## Fix round (critic t-946)

Files: tools/journal_validator.py, tools/test_journal_validator.py, tools/agents_md.py, AGENTS.md (regenerated), plus tools/test_agents_md.py (not in owns; it asserted the old Journal-note text, so it had to follow -- needed beyond owns). All STAGED, nothing committed.

1. B-1: both functions deleted (`test_matrix_designer_accepted_by_opus_without_basis_fails_equal_tier`, `test_matrix_designer_by_opus_critic_basis_fails`). Row added: `today-designer-opus-critic-basis` (CFG_TODAY, designer, by opus, basis critic -> FAIL, text `basis='critic'`: critic rank 2 is not above designer rank 2, spec 3.1 cell (e)). Also `today-designer-opus-queued` (PASS, spec 3.1 (f): builder <= opus < lead on today's config). Test_journal_validator.py:~540-560 (rows), :60-66 (`_decide`).
2. N-B1 / V-B: per-cell legacy tests deleted (test_journal_validator.py, old :497-861). Covering rows:
   - test_matrix_missing_by_fails -> NEW row `by-missing` (by=None omits the field; expect "'by'")
   - scout_accepted_by_same_tier_without_basis_fails -> `after-scout-haiku`; scout_accepted_by_higher_tier_passes -> `after-scout-opus`
   - scout_accepted_same_tier_with_basis_now_fails_below_sonnet_floor -> `today-scout-haiku-critic`, `after-critic-haiku-queued`
   - model_id_in_by_fails_as_unknown_tier -> `by-model-id`; unknown_by_fails_even_with_critic_basis -> `by-model-id`, `by-alias`
   - unknown_by_case_sensitive_fails_not_via_queued_to_lead_branch -> NEW row `by-capitalised-queued` (the "not via queued branch" negative is no longer asserted; the enum-first order is pinned by `by-function-word-architect-with-judge`)
   - unknown_by_fails_before_judge_branch_even_on_leaf_category -> `by-function-word-architect-with-judge`, `judge-*`
   - boundary_fable_known_tier -> `after-critic-fable`; boundary_haiku_floor_message -> `after-builder-haiku-critic`
   - pair_sonnet_by_builder_critic_basis_ok -> `after-builder-sonnet-critic`, `today-builder-sonnet-critic`; pair_sonnet_by_builder_queued_fails -> `after-builder-sonnet-queued`; pair_sonnet_by_critic_queued_ok -> `after-critic-sonnet-queued`; pair_opus_by_critic_queued_ok -> `today-critic-opus-queued`; pair_opus_by_builder_no_basis_ok -> `today-builder-opus`; pair_haiku_by_scout_critic_basis -> `today-scout-haiku-critic`; pair_boundary_fable_by_critic -> `today-critic-fable`; pair_boundary_sonnet_by_critic_no_basis -> `after-critic-sonnet-bare`; pair_boundary_haiku_by_builder_queued_fails_floor -> `after-critic-haiku-queued` (same floor branch; the builder+queued combination itself has no row)
   - matrix_agent_lead_needs_only_presence_of_by -> `after-lead-no-matrix`; agent_outside_agent_tier_regression_pin -> `after-unknown-agent-no-matrix`
   - designer_accepted_by_fable_passes -> `after-designer-fable`; designer_by_sonnet_queued -> `after-designer-sonnet-queued`; designer_by_opus_queued -> NEW `today-designer-opus-queued`
   - KEPT (no table cell, event is `rejected`, reads no config): `test_matrix_rejected_only_needs_by_present_no_tier_check`.
   Siblings, every `decide(` caller: all ~35 remaining `jv.decide(` calls in test_journal_validator.py now go through `_decide`, which does `kw.setdefault("config_text", CFG_TODAY)` (fixed: pinned to today's config; one literal wrapper instead of editing each call). Exceptions kept on `jv.decide`: `test_config_comes_from_the_root_of_the_validated_repo` (it tests the default read, with a monkeypatched `_repo_root`). Calls that already pass `config_text=` are unchanged. test_journal_validator_merge.py:123,452,461 `jv.decide(...)`: n/a (not in owns; the critic's post-L probe ran that file and test_journal_validator_node.py: 211 passed). `decide_merge` / `decide_with_warnings` unchanged.
3. B-2: journal_validator.py `_developer_file_result`, the `drift=False` branch now also sets `ww = matrix_warnings(lines[len(head_lines):], head_lines, seed_lines=split_lines(seed_text))` (about :2369-2374). Table `test_all_base_prints_the_independent_context_warn` (3 rows: after/no-worker -> WARN, after/agent-worker -> no line, today fable/no-worker -> WARN; exit code 0 in all) at the end of test_journal_validator.py.
   red-before: `( cd W && python -m pytest tools/test_journal_validator.py -q -k all_base -p no:cacheprovider )` -> `FAILED ...[after-no-worker]  FAILED ...[today-fable-no-worker]  2 failed, 1 passed, 332 deselected` (`assert ('INDEPENDENT CONTEXT' in '') is True`); after the change: `3 passed, 332 deselected`.
4. B-3: agents_md.py Journal note now: "accepts only the model-family words in `FAMILIES` of `tools/tier_ladder.py`: ... `by` is the model-family word of the accepting session ... basis ("critic" or "queued-to-lead") ... ranks of model families, not model ids"; no judge. Dead constant `VALIDATOR_REL` removed. AGENTS.md regenerated (2/2 lines). test_agents_md.py assertions follow (:366-368).
5. Minor: `JOURNAL_PATH = "logs/routing-log.jsonl"` restored as on main. Stale prose: validator `category` form message no longer mentions leaf/judge; test comments TIER_ORDER -> FAMILIES / "model-family word"; no AGENT_TIER/TIER_ORDER left in the five files (git grep -i, positive control: the grep found them before the edit). Old-test comments about AGENT_TIER/leaf-judge went with the deleted tests.

### DoD outputs (verbatim tails)
`( cd W && python -m pytest tools/test_journal_validator.py tools/test_journal_write.py tools/test_agents_md.py -q -p no:cacheprovider )` -> `465 passed in 103.46s (0:01:43)`
`( cd W && python -B tools/agents_md.py --check )` -> `AGENTS.md: up to date (123372 bytes)`
Post-L config (scratch git repo, delegation.config.yaml lead=claude-opus-5-5, architect=claude-fable-5-1): `( cd <scratch> && python -m pytest W/tools/test_journal_validator.py -q -p no:cacheprovider )` -> `313 passed in 11.22s`
(first post-fix run showed `1 failed ... [today-designer-opus-critic-basis]`: my row expected the generic text, the code names `basis='critic'`; the row text was corrected, the verdict FAIL was right.)

### Staged numstat (`git -C W diff --cached --numstat`)
2 2 AGENTS.md / 83 0 handoff / 15 15 tools/agents_md.py / 234 225 tools/journal_validator.py / 18 6 tools/journal_write.py / 10 10 tools/test_agents_md.py / 345 528 tools/test_journal_validator.py / 25 2 tools/test_journal_write.py
Shortstat: 8 files changed, 732 insertions(+), 788 deletions(-). Test lines: test_journal_validator.py is net -183 (345 added vs 528 removed); product added 234 (validator) + 18 + 15 -> the tests are now under the product volume (V-B resolved).
