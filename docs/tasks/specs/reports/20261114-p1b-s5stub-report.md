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

## Update after the Lead's answer (owns widened to dry_stub.py, wiring only)
`dry_stub.py`: `kit_context(..., task_root="")` passes `task_root` into `FillContext` (line 340-346); the ctx built at ~761 (both branches) passes `task_root=str(task_dir)`. Nothing else in that file. Selftests re-run green: dry_stub --selftest 189/189; test_form_selftest 26/26; test_form_at_stop 6/6; test_form_view 80/80; dry_exits --selftest 154/154; selftest --limits --lang 4/4.

## Item 3: `python -B scripts/tests/test_scenario_dry_1.py --part main` (verbatim, S5 and the tail)
```
NOTE dry-1/main/stub-call: S5-qa-automator-1 n=1 stage=S5 resume=False wrote=5 live_only=2
NOTE dry-1/main/stub-wrote: S5 qa-automator (window -): work/handoffs/S5-qa-automator-1.yaml, qa-factory/tests/TC-1_test.py, work/automation-manifest.json, work/automation-manifest.json, work/automation-manifest.json
NOTE dry-1/main/stub-live_only: S5 qa-automator: work/s5-plan.json: shape is the skeleton s5_plan.py --init writes; no contract template
NOTE dry-1/main/stub-live_only: S5 qa-automator: work/s5-notes/: free notes, no contract shape
NOTE dry-1/main/stub-call: S5-qa-code-critic-1 n=1 stage=S5 resume=False wrote=0 live_only=1
NOTE dry-1/main/stub-live_only: S5 qa-code-critic: form s5-critic-to-automator: no probe record exists in work/probes/ and the contract declares no empty outcome for probes.records
NOTE dry-1/main/stub-call: S5-qa-code-critic-1 n=2 stage=? resume=True wrote=0 live_only=0
NOTE dry-1/main/snapshots: made S0, S1, S2, S3, S4
NOTE dry-1/main/after: after:P1B-9: no snapshot for S5, S6, S7, S8, S9
NOTE dry-1/main/time: 385.1 s in 4 driver process(es); seconds per stage {'start': 75.7, 'S1': 12.5, 'S2': 27.7, 'S3': 98.8, 'S4': 74.0, 'S5': 88.8}; stages done S0, S1, S2, S3, S4
=== scenario dry-1: 6/6 ok ===
```
S5 still does not close; S0-S4 close. The previous refusal (embedded hint `<instance>`) is gone; the new one is the edge (a) text.

## The world at the critic's turn
The filler (now reading task_root) found no `*.json` under `work/probes/` of the story's task folder at the critic's turn: the refusal above is that measurement (folder absent or empty; the stub cannot tell which, and does not need to). The row's world folder is deleted by the test at its end (dry_world.py temp `qa-dry-row-*`, cleaned), and the leftover `qa-dry-row-*` folders in the temp dir are other rows' worlds (no S5 handoff in them), so I cannot list files from this run's world: not verified beyond the filler's measurement. In the nearest leftover world (`qa-dry-row-1bwyl_gv`, stopped before S5) there is no `work/probes/` at all.
Next cause (not fixed): in a live run the code critic calls `probe_by_code.py --task <T> --dispatch <ID> --test ... --instance <IID>` (command text handed out at `scripts/brief_pack.py:239`; it writes `work/probes/<IID>.json`, `scripts/probe_by_code.py:19`). The stub never calls it: `grep probe_by_code` over `scripts/tests/dry_*.py` finds nothing (positive control: the same grep finds it in brief_pack.py). So the critic's turn has no record to name, and the contract has no empty form for `probes.records`. The next node: either the stub runs probe_by_code.py for the window's instances (needs the product script to run in the dry world), or a decision on an empty outcome in the contract.

## Finding: null_outcomes keys top-level sections only
`scripts/handoff.py:515-533` (`null_outcomes`: `template(...).data.get("null_outcome")`, entries keyed by section, validated in `null_outcome_entries` ~495-512): a nested list such as `probes.records` can have no declared empty outcome. `handoff_check.py:497-502` (`_probe_list`) returns None (no value) when no probe file exists.

## Commit
See the handoff line: new commit on wip/p1b-s5stub with dry_stub.py wiring and this report.

## Siblings / analogs
- `s5-automator-to-critic.yaml` names the same path as an owned input / whole placeholder: untouched.
- `<instance>` in the same row's `instance: <instance id>` is filled as "filled instance" (rule `free-text`), not the file stem: the record path and the instance field do not agree; spec did not ask, left as is.
- Needed beyond the manifest: `dry_stub.py` lines 329-345 and 735-780, `handoff.py` null_outcomes.
