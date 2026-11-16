# t-905 FG7-5 node cost -- builder report

DoD: `python -B -m pytest tools/test_forge_metrics.py -q -p no:cacheprovider`
Output (verbatim tail):
```
.......................................s..s..........s.................. [ 60%]
...............................................                          [100%]
116 passed, 3 skipped in 35.22s
```
(node-cost subset, `-k node_cost`: 34 passed. The 3 skips are the file's pre-existing skips.)

## What was done
- `tools/forge_metrics.py`: new section `# node cost` (TOP_NODES, `_price_dispatch`, `node_costs`, `render_node_costs`),
  flags `--node-cost` and `--projects-root`; the `--node-cost` branch sits BEFORE `--check` and `compute()`; with
  `--write/--out/--check` -> exit 2 with the P18 line. `transcripts`/`usage_report` imported lazily (I-2, pinned by T4).
  Prices only through `usage_report.load_prices` + `accounted_cost`; node via `journal_keys.node_of`; keys via
  `task_key`/`ref_key`/`display`; `critic:` pattern built from `journal_keys.ID_PATTERN` (F6, pinned equal to
  `journal_echo.CRITIC_TOKEN_RE.pattern` by one test).
- `tools/test_forge_metrics.py`: T1 `test_node_cost_grouping_and_price` (18 rows, I-3 and I-4 asserted in every row),
  T2 `test_node_cost_render` (6 rows), T3 `test_node_cost_cli_doors` (7 rows) + one broken-price-file test, T4
  `test_node_cost_import_stays_light`, F6 pin test. No new test file; no existing test touched.
- Warnings (E6, E12, E13, E14) are in `d["warnings"]` and printed one per line on stderr by `main`; not in stdout text.

## Live line for t-505 (real `logs/journal/dev1.jsonl` of this tree, `--node-cost --window 2026-11-13`; transcripts WERE reachable)
```
| t-505@dev1 | accepted | 4 | 0 | 20335530 | $6.60 | 2 (spec 2) | 1 | 2 (replaced 0) | 1 | 0 |
```
Header of the same run: `rows 537 (accepted 488, open 49; 377 with no node and no link token); dispatches 752: measured 742, unmeasured 10; total >= $1444.70, tokens 4235761879`.
Matches the spec's hand-derived facts for t-505 (4 dispatches, rejects spec 2, critic 1, redelegations 2, escalations 1).

## Deviations from spec / reality (findings)
1. Row name of a developer-file task is `t-505@dev1`, not `t-505`: `journal_keys.load_all` labels every `logs/journal/<slug>.jsonl`
   that is not the successor of the history (no `continues` on line 1) with its slug, and `display` prints it. The spec's
   example text says `t-505`. Code follows `display` (spec §8: "Row name = node string or journal_keys.display(task key)").
2. T3 case `--window 2026-13-99` -> "the existing window refusal": `_normalize_window` only checks the SHAPE
   (`\d{4}-\d{2}-\d{2}`), so 2026-13-99 is accepted and runs (exit 0). I tested the refusal with `--window yesterday`.
   I did not change `_normalize_window` (it would change the existing modes: I-1).
3. E18's broken price file has no CLI flag in the spec; the test breaks it by monkeypatching `usage_report.PRICES_FILE`.

## Interpretations (spec ambiguity; flag for Lead -- no design weight but named)
- §2.2 step 3 "(only for a task with NO own node)": read as the ATTACHED task (the critic / the defect-fix task) having no
  own node; the target of the token may have a node (then the critic joins the node row). An attached task with its own node
  stays in its node row and the token is ignored silently.
- A defect_found line alone creates no task/row (tasks are built from delegated/accepted/rejected/escalated lines); its
  `ref` counts the defect, its own task attaches only if that task has `delegated` lines and no node.
- `same_worker` is recorded only after the first line of that agent id was actually priced; otherwise the later line is
  tried (and reported) again, so an unpriced worker never turns into a measured $0 on its second line.
- `unlinked` = rows of kind task holding a single task and no shared citation (a builder row that has a critic attached is linked).
- A row/total with no priced dispatch is `n/d` (cost None) -- also in totals.cost.
- `shared` entries carry two extra keys `dispatches` and `unmeasured` (used for I-3 and the "not measured" list);
  `cited_by` lists ROW names (equal to task names for task rows).
- "not measured" list is ordered by (file, line), not global journal order.

## Questions
none

## Siblings / analogs noticed (reported, not fixed)
- Spec §9 items stand (stale check-31 text; two agent-ref regexes `hop_metrics.py:88` vs `journal_echo.py:308`; fix rounds under a new task id with a prose-only link are unlinkable: live run shows 377 unlinked rows).
- Live run also exposes: `t-134@dev1` has two different nodes (DC1-28, DC1-27), `t-333@dev1` (OH8-2, OH8-2a) -- journal convention gaps; `dev1.jsonl line 1035` cites `critic:t-378/t-390/t-404` that have no critic dispatch.
- `main()` of forge_metrics: `--projects-root` without `--node-cost` is silently ignored (same as `--base` without `--check`).

## Gate / mechanism
Mechanism path (`tools/forge_metrics.py`): the commit may ask `tier:` / axis block; see the commit result below. Package untouched: `architecture: none -- outside the package`.

## Needed beyond the manifest
`tools/journal_keys.py`, `tools/transcripts.py`, `tools/usage_report.py`, `tools/journal_validator.py`, `tools/hop_metrics.py`, `tools/journal_echo.py` (read for signatures), `tools/test_hop_metrics.py` (transcript line shape), `tools/model_prices.json`.
