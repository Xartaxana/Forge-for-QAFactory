# t-905 (attempt 2) -- FG7-5 `forge_metrics --node-cost`, fix round for critic t-914

Files changed: `tools/forge_metrics.py`, `tools/test_forge_metrics.py`, this handoff. No money figure is written here.

## Output

DoD: `( cd <worktree> && python -B -m pytest tools/test_forge_metrics.py -q -p no:cacheprovider )`

```
.......................................s..s..........s.................. [ 57%]
.....................................................                    [100%]
122 passed, 3 skipped in 33.05s
```

(attempt 1 was 116 passed, 3 skipped; +6 = 4 new case rows + 3 F3 rows, minus nothing; one case row was extended.)

## Review item -> what changed -> test row

| item | what changed | test row |
|---|---|---|
| B1 | `seen[aid] = (line, priced, whys)`. A later line of an agent id whose first line priced nothing repeats the first line's `whys` (cost None, unmeasured, never `$0.00`). When the first line was priced, the later line carries `same_worker: <first line>`; `_nc_money` collects it into `priced_elsewhere` (row and shared dicts, additive key); the text prints a separate line `priced elsewhere (the agent's transcript is counted once, on its first line): <task> line N (same_worker, priced on line M)` (form chosen: the separate `priced elsewhere:` list, not the "not measured" list) | `same_worker_first_unpriced` (new), `same_worker_twice` (extended: note data), `same_worker_note_and_given_prices_header` (render) |
| F1 | a `defect_found` line is stored in its ref task's `defect_evs`; `in_window` tests `events + defect_evs` (E15) | `defect_in_window_on_old_row` (new) |
| F2 | `node_costs` split into `_nc_tasks`, `_nc_links`, `_nc_rows_of`, `_nc_money`, `_nc_counts`, `_nc_row`, `_nc_price_all`; `node_costs` is now the orchestration only, no closures except `warn`/`in_window`; the counts loop is flat | existing T1/T2/T3 tables (green) |
| F3 | `request_parts(..., counts=counts)` is kept; non-zero `split_missing` / `bad_iterations` become `whys` (dispatch is partial) | `test_node_cost_low_figure_counts_are_named` (3 rows: split_missing, bad_iterations, none) |
| F4 | the dead `except (ValueError, TypeError)` removed | none (refactor) |
| F5 | one `_agent_id(obj, transcripts)` (built on `transcripts.agent_file_name`) used by `_price_dispatch` and `_nc_price_all` | none (refactor); a glob ref stays `bad_ref` (`glob_ref_is_bad_ref`) |
| F6 | `node_costs` returns `prices_file` ("given" when `prices=` is passed, else `tools/model_prices.json`); the header prints it | `same_worker_note_and_given_prices_header` asserts `prices: given as_of T --` and no `model_prices.json` |

## Deviations

- The "F6 pin" test row of attempt 1 (`critic_token_pattern_equals_the_hooks`) is unrelated to critic item F6 and untouched.
- `prices_file` / `priced_elsewhere` are additive dict keys (the critic noted additive keys are acceptable).
- `_price_dispatch` now takes the whole `ev` (needs the line number) instead of `obj`.
- Not done by this round: the spec text defects named by the critic (t-505 display, `2026-13-99` premise, `n/d` total) are the Lead's; the node-field finding goes to `plans/piles/forge/findings/` by the Lead.

## Questions

none

## Needed beyond the manifest

`tools/transcripts.py` (counts keys of `request_parts`, read only).
