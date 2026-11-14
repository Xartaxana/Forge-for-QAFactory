# p1b-s5stub report (builder)

Commit: dbf413d9 on wip/p1b-s5stub (pushed). Status: filler side DONE; item 3 (main pass) NOT RUN, one blocking question below.

## Blocking gap (question to the Lead)
The filler has no way to know WHERE the world is: `dry_stub.py` builds the context at line 761 (`kit_context(...)` / `FF.FillContext(...)`) and calls `fill_handover` (line 775 -> `FF.fill_form`, line 439); neither carries the task folder (`cases_root` is task-relative). The new token reads `<task_root>/work/probes/*.json`, so `FillContext.task_root` must be set by the caller. `dry_stub.py` is a non-goal, so I did not add the one wiring (`task_root=str(task_dir)` at 761 and in `kit_context`). Without it, the stub's S5 stays `live_only` with the reason "the contract's token <instance> reads the files under `work/probes` of the world, and the context has no key `task_root`", i.e. the main pass would still stop at S5, just with a new reason (prediction from the code, not verified by a run). Question: may the wiring in dry_stub.py (about 2 lines: `task_root=str(task_dir)` in the two ctx constructions) be part of this node, or is it another node's? `write_dispatch_form` already fills it from its own `task_root` argument.

## What changed
- `scripts/tests/fixtures/form-fill-rules.json`: new row `world_list_tokens` = `{"<instance>": {"root": "task_root", "dir": "work/probes", "glob": "*.json"}}` and one sentence in `_about`.
- `scripts/tests/form_filler.py`: `FillContext.task_root` (str, default ""); survey kind `world` (checked before the other tokens); `world_list(token, ctx)` (the one reader: stems of files matching the glob, sorted by file name; no root -> None + reason); `_spread_world_rows` (after the form text is built, the list row carrying the token is copied once per file, token replaced by the stem; locates the row through `handoff.parse` of the finished text); `write_dispatch_form` sets `task_root` from its own argument.
- `scripts/tests/test_form_selftest.py`: `world_list_rows()` (6 world rows x refusals/records, odd-stem/non-JSON, two rows keep other fields, rest of form untouched, no task_root, another form's text identical with/without task_root).
- Line numbers of the scout's finding matched (form_filler.py kind "embedded" and the refusal, handoff yaml line 59).

## Edges
(a) no folder / no `*.json`: `Unfillable` at `probes.records[0].record` with text "no probe record exists in work/probes/ and the contract declares no empty outcome for probes.records". FINDING: the contract has no `null_outcome` block and `handoff.null_outcomes` keys only top-level sections, so no declared empty outcome can exist for the nested list `probes.records`; the "declared" branch is unreachable and not implemented. (b) JSON validity never read. (c) stem used as is (tested: `x y`, `a.1`, `z_9`). (d) one rule, no form-name branch. (e) other forms unchanged (tested). Not specified, my minimal choice: a world token outside a list item (or two distinct world tokens in one item) -> `Unfillable` "there is no single file to name".

## Witness (from `W`, each run alone)
```
test_form_selftest: 26/26 ok
test_form_at_stop: 6/6 ok
test_form_view: 80/80 ok
dry_exits selftest: 154/154 cases
qa-factory selftest: 4/4 ok      (selftest.py --limits --lang)
```

## Item 3
Not run (see the blocking gap). Next step once the wiring exists: run `python -B scripts/tests/test_scenario_dry_1.py --part main` from W in the background.

## Siblings / analogs
- `s5-automator-to-critic.yaml` names the same path as an owned input / whole placeholder: untouched.
- `<instance>` in the same row's `instance: <instance id>` is filled as "filled instance" (rule `free-text`), not the file stem: the record path and the instance field do not agree; spec did not ask, left as is.
- Needed beyond the manifest: `dry_stub.py` lines 329-345 and 735-780, `handoff.py` null_outcomes.
