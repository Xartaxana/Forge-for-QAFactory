# t-916 — Architect spec, Stream A (the ladder home + tier gate + savings)

DoD: `python -m pytest tools/test_tier_ladder.py tools/test_mechanism_gate.py tools/test_mechanism_gate_md.py tools/test_savings_report.py -q -p no:cacheprovider`

Output (run once at the end, from the worktree root):

```
........................................................................ [ 40%]
........................................................................ [ 50%]
........................................................................ [ 60%]
........................................................................ [ 70%]
........................................................................ [ 80%]
........................................................................ [ 90%]
...................................................................      [100%]
715 passed in 9.67s
```

Extra smoke (script run, sibling-import road): `python -B tools/mechanism_gate.py --list --since 2026-11-16` lists mechanism commits with indented paths;
`--list --since bad` -> stderr `mechanism_gate list: --since must be an ISO date (YYYY-MM-DD or YYYY-MM-DDTHH:MM) or a commit sha (7-40 hex digits), got 'bad'`, exit 1.

State: everything STAGED in the worktree, nothing committed. Files: `tools/tier_ladder.py` (new), `tools/test_tier_ladder.py` (new), `tools/mechanism_gate.py`, `tools/test_mechanism_gate.py`, `tools/savings_report.py`, `tools/test_savings_report.py`. `tools/test_mechanism_gate_md.py`: no change needed (green as is).

## Items

| item | what changed | test rows |
|---|---|---|
| A1 | `tools/tier_ladder.py`: `FAMILIES`, `ALIASES`, `FUNCTION_RANKS`, `COORDINATION_FUNCTIONS`, `DEFAULT_BINDINGS`, `family_of`, `bindings`, `effective_bindings`, `rank_of_function`, `rank_of_model`, `lead_binding`, `architect_binding`, `function_of_session`. Stdlib only at import; `yaml` imported inside `bindings()`. `rank_of_model` and `function_of_session` share ONE matcher (`_resolve`). | `test_tier_ladder.py`: `test_rank_of_model_table` (every §2.2 adversarial row on TODAY/AFTER/AFTER_NO_ARCHITECT and the nonsense configs), `test_config_size_limit` (64 KB parsed / 64 KB+1 default), `test_bindings_table` (alias bomb, reserve-not-read note, broken yaml, no roles...), `test_pyyaml_import_failure_...` (sys.modules yaml=None), `test_effective_bindings_table`, `test_lead_and_architect_binding`, `test_rank_of_function_table`, `test_function_of_session_table` (incl. `claude-fable-5-2` vs fable-5-1 binding -> `("architect","family match: claude-fable-5-1")`), `test_families_aliases_and_default_bindings_...`, `test_importing_the_home_does_not_import_yaml` (subprocess, `-I`) |
| A2 | `mechanism_gate.py`: deleted `ROLE_RANKS`, `LEAD_FAMILIES`, `build_role_ladder`, `_resolve_ladder_rank`, `_resolve_role_model`, `import yaml`. `tier_declared_ok(declared, binding, cfg)` = `declared == binding` OR `rank_of_model(declared, cfg) >= FUNCTION_RANKS["lead"]`. | `test_tier_declared_ok_table` (TODAY/AFTER/no-architect/key-bound parity/lead=critic=opus/duplicate id/...), `test_decide_full_tier_line_table`, `test_the_old_ladder_carriers_are_gone` |
| A3 | `resolve_lead_binding` / `lead_family` are thin wrappers over `tier_ladder.lead_binding` / `family_of` (default `"fable"` from DEFAULT_BINDINGS). `savings_report.py`: `_UNBOUND` deleted, `top_tier_model` reads the lead through tier_ladder; report line relabelled `coordinator model:`; import of `mechanism_gate` replaced by `tier_ladder`. | `test_binding_wrappers_read_the_ladder_home`; `test_savings_report.py::test_the_counterfactual_model_is_the_lead_binding_in_either_world` (AFTER -> opus, reserve key ignored, TODAY -> fable); existing no-lead / missing-config PricesError rows stay green |
| A4 | `MECHANISM_PREFIXES` += `"tools/tier_ladder.py"` (with the other transitive entries) and `"delegation.config.yaml"` (comment: DATA that decides the acceptance matrix and the tier gate). | `test_mechanism_paths_template_homes_and_self_protection` (both paths added); the existing closure test `test_transitive_import_closure_of_live_wiring_is_covered_by_mechanism_prefixes` passes WITH the new import (mechanism_gate -> tier_ladder) |
| A5 | `_tier_queue_note()`: "... it goes into the Lead queue docs/tasks/lead-queue.md; ..." | `test_decide_full_missing_tier_line_fails` keeps `"Lead queue"` and now asserts the path and no `CURRENT_CONTEXT` |
| A6 | `list_commits(since, git=_git_strict)` + `_list_main`, `main` dispatches `--list`. `since` = ISO date (as `--audit`) or a 7-40 hex sha (window `<sha>..HEAD`); one line `<sha8> <committer date ISO> <tier values joined by "," or "-"> <subject>` per commit touching `mechanism_paths()` (merges against first parent), its paths indented 4 spaces; empty window -> `0 commits` exit 0; bad value -> exit 1 naming both forms; git failure -> exit 1. | `test_list_commits_table` (date, datetime, sha, no-tier, window-without-mechanism, empty-window, bad-word, bad-date, empty-value, option-injection `--all`, short-sha), `test_list_commits_git_failure_exits_1_and_the_cli_needs_since` |

## Existing rows of `test_mechanism_gate.py` rewritten

The `reserve`-key and ladder-helper tests (about 40 single-assert tests, lines ~604-1076) were folded into three tables and the 3 `resolve_lead_binding_*` tests were kept untouched. Rows and what happened:

- `test_build_role_ladder_*` (5 tests: fixed order, ignores judge/analyst, ignores designer, role without model, empty without config) and `test_resolve_ladder_rank_*` (no-lead-rung, nonsense-reserve, exact weaker/stronger/non-Claude step, duplicate id): the helpers no longer exist; their meaning moved to `test_tier_ladder.py` (`test_bindings_table`, `test_rank_of_model_table`) and to rows of `test_tier_declared_ok_table`. "ignores judge/analyst/designer" is covered by `COORDINATION_FUNCTIONS` row of `test_families_aliases_and_default_bindings_...` and `test_bindings_table` (only coordination functions are read).
- `duplicate_model_id` (`CONFIG_LADDER_DUPLICATE_MODEL_ID`: builder + reserve = claude-fable-5): reserve -> `architect`; rows `duplicate-model-id` in both tables; expected unchanged (passes, max rank).
- every `reserve` fixture (`..._WITH_RESERVE`, `OPUS_LEAD_FABLE_RESERVE`, `AMBIGUOUS_FAMILY`, `NONSENSE_RESERVE_BELOW_LEAD`, `NO_LEAD_RESERVE_OPUS`, `EXACT_*_AT_RESERVE`): key renamed to `architect` (configs `non-claude-lead-architect-fable`, `opus-lead-architect-fable`, `ambiguous-family`, `architect-below-lead`, `no-lead-architect-opus`, `architect-above-sonnet-lead`, `architect-non-claude-step`); a new row `reserve-key-not-read` proves the old key raises no rank.
- **Changed expectation, one row:** `ambiguous-family` / `tier: opus` (critic and architect both of family opus, non-Claude lead). The old test expected REFUSED ("ambiguity does not resolve"); the spec's case (b) says "the max rank of functions bound to that family", so it is now ACCEPTED (rank architect). Flag for the critic: this is a spec-mandated loosening for a nonsense config.
- `tier_declared_ok(...)` direct tests that passed a BINDING with no config (`("fable","claude-opus-5")`, `("opus","claude-fable-5")`, `("fable","llama-3.3-70b-versatile")`): the new function reads the ladder from the CONFIG, so those rows now carry a config that agrees with the binding (`opus-lead`, `fable-lead`, `non-claude-lead`); same expectations. Called with a binding that disagrees with its config, the config wins (the binding only serves the exact-match first pass).
- `test_decide_full_missing_tier_line_fails`: one added assert (A5).

## Draft of rule 10's four questions (for the mechanism commit; no axis block)

- (a) Cost of compliance / who pays: a mechanism commit still carries `tier: <model>`; after stream L an Opus Lead passes, today only Fable does (unchanged). The coordinator pays one extra reading step (`--list --since` at the weekly Architect review); builders pay nothing. Hook path pays nothing new (tier_ladder is stdlib-only; yaml loaded only when the config is read, once per commit-msg).
- (c) Detector of the mechanism's failure: a wrong tier line (form passes, truth false) is calibration's check 5 (session model vs transcripts); a ladder that drifts from the config is caught by `tools/test_tier_ladder.py` tables on both worlds; the `--list --since` output is the Architect's own review reader (spec 4.5 step 5, checks 6/49 registered by stream F); the closure test `test_transitive_import_closure_...` detects a ladder-home module outside the net.
- (d) What stops a skip: `.githooks/commit-msg` runs `tools/mechanism_gate.py` on every commit; `delegation.config.yaml` and `tools/tier_ladder.py` are now in `MECHANISM_PREFIXES`, so editing the binding is itself a gated mechanism commit; the weekly batch review of `--list` output is on discipline, its leak detector is calibration check 49 (stream F).

## Deviations from the spec (decisions are stated, not hidden)

1. `effective_bindings` also falls back to DEFAULT_BINDINGS when the config is readable but binds NO lead model (spec text says only "when `bindings()` yields {}"). Reason: without it `roles: {architect: opus}` made `tier: opus` pass (exact id on the architect rung), whereas today `resolve_lead_binding` defaults to fable and refuses it (existing test `no_lead_reserve_opus`). Note says `roles.lead names no model`. Direction: stricter only.
2. `savings_report.top_tier_model` reads `tier_ladder.bindings(text)[0].get("lead")` rather than `lead_binding()`: `lead_binding()` falls back to the default `"fable"`, which would price the counterfactual at a model the config never named. That contradicts the existing PricesError rows ("roles.lead names no model", FR-41). See question 1.
3. Guard placement: the "weaker than lead's family never inherits rank >= lead" guard is applied only to rungs ranked above lead (architect), not to every rung as the old code did (the old guard dropped builder/scout on a weaker family than lead, which cannot be kept now that the same function ranks the MODEL line/matrix and must return builder for sonnet under an opus lead). Behaviour for the gate (rank >= lead) is identical.
4. A known family with a NON-Claude lead and no exact match (case c, lead family unresolvable) returns `None`, not a rank (spec case (c) does not state it; the old gate refused). `function_of_session` -> `(None, "matches no binding")`.
5. `--list` prints no header line for a non-empty window, and `0 commits` alone for an empty one.
6. Local `git diff` in this worktree shows `tools/test_mechanism_gate_md.py` untouched (it loads the live gate or a sibling copy and needed no row).

## Questions

1. Spec A3 says: "config absent -> existing PricesError path unchanged? NO — absent config gives DEFAULT_BINDINGS lead = fable, so the counterfactual is Fable as today (row)". That contradicts `test_a_missing_config_is_a_prices_error_...` and the 4 `no-roles/empty-roles/empty-model/broken-yaml` rows (FR-41: never a silent default price), which I kept. Decide: keep PricesError (what I did; no row for "absent -> Fable" was written), or change the savings behaviour to price at DEFAULT fable (then those existing rows flip).

## Needed beyond the manifest

`tools/test_mechanism_gate_md.py` header (how it loads the module), `tools/usage_report.py` (PricesError, no edit), spec lines 620-704 (§7 Stream A block) and `docs/TESTING.md` section headings.

## Analogs noticed (not fixed)

- `tools/mechanism_gate.py` module docstring item 6 still lists the transitive modules by name; `tier_ladder` is named in the prefix comment, not the docstring (cosmetic).
- `savings_report.py` still says "top-tier" in its module docstring, the section header (line ~250) and `as-top-tier=` labels (pinned by tests); only the `coordinator model:` line was relabelled (F11 (a)).
- `tools/test_mechanism_gate.py` rows `test_resolve_lead_binding_*` use `claude-fable-5` literals; unchanged.
- Other family-tuple carriers named in spec §2.3 (`tier_echo`, `dispatch_gate`, `journal_hooks`, `agents_md`, `token_usage_stats`, validator `TIER_ORDER`) are other streams' owns; untouched.
