# t-308 OF4-10 builder report

commit: 36083da on wip/of4-10 (not pushed), cut from 58b3667.

## Done
- hooklib: `ConfigUnreadable` and `read_config_file` moved in verbatim above `artifact_root`, with a `RecursionError` catch ("is nested too deeply to read" + the door). `artifact_root` calls `read_config_file(project) or {}`; no json.loads in it. Literal `raise ValueError(<finished text>)` for non-string/blank/NUL key, and a second one for a `resolve` OSError/ValueError (census unit kept). No new import.
- config_contract: the two definitions deleted, one top-level re-export line after its imports. No other `config_contract` internal was needed by the moved body, so no stop-condition. No import cycle (hooklib's `import config_contract` at :2778 is still lazy).
- vcs_evidence: `_story_at` (above `_story_root_of`); branch 1 and 2 decide through it; branch 2 starts at `len(parts)-3` (output must lie below `<T>`), deepest match decides. `left_out_by_person`: config guard only on the no-story branch (refusal exit 2 with door, no default folder named); FileNotFoundError/NotADirectoryError -> None, other OSError -> refusal. `main`: empty-id refusal prints `status: unknown`, `error: not_checked`.
- exit_gate: `grounding_errors` guard after the role check (returns one `unreadable_record("grounding_errors", ...)`); `_identity` slug decides `scan_root` first, `artifact_root()` only without slug inside the existing try; `awaiting_source_review` ticket resolution moved into the try.
- tests: `test_read_json.py` `test_the_artifact_root` (ROOT_STATES x ROOT_SITES, identity pins, class split) + call in `__main__`; `test_vcs_evidence.py` `story()` writes pipeline.json, ROOT_ROWS gets the 8th `needle` column and rows V1-V8.
- changelog fragment `changelog.d/of4-10-artifact-root.md`.

## Witness (verbatim tails)
`scenario_walk.py --witness-for <the 7 owns>` printed 93 runnable files (after dropping test_controller_* and test_story_run_*), 44 of them listed in `slow_tests.json` (not run), 46 run via `python -B <wt>\...\tests\<file>`:
- 43 files end `=== <name>: N/N ok ===`; test_doctor_access.py ends `OK`; test_project_knowledge.py `86 passed in 7.17s`; test_walk_pool.py `30 passed in 1.22s`. No failures.
- `test_read_json.py`: `=== read_json: 499/499 ok ===` (incl. `PASS OF4-10 grounding x key_nul`, `PASS OF4-10 config_contract.ConfigUnreadable is hooklib.ConfigUnreadable`, `PASS OF4-10 class split: key_number`).
- `test_vcs_evidence.py`: `=== test_vcs_evidence: 157/157 ok ===` (V1-V8 rows present, 23 PASS lines match ` V[1-8] `).
- `test_judgment_census.py` is in the printed list and ended ok.
- `python -B selftest.py --limits --lang` -> `=== qa-factory selftest: 4/4 ok ===`.
- `python -B refusal_registry.py --check` -> `A24 refusal registry: no violations` (rc=0); `R.sites(files=['hooklib.py'])` still lists `artifact_root` at lines 738 and 745.
- Greps: `json.loads` in hooklib: hits at :714 (moved reader), :755, :767, :806, ... none inside `artifact_root`; `def read_config_file|class ConfigUnreadable` in config_contract: no hit (control: hooklib :691, :696); `^import config_contract|^from config_contract` in hooklib: no hit (control: lazy import at :2778); `artifact_root(` non-test call-site count 118 (spec said 120 incl. defs/doc text; no new caller added).
- Commit hooks passed (escape allowlist, factory rules index, architecture index, WARN ratchet).

## FR walk
A FR-1/2/4/46/57 kept (finished texts with doors; family stays ValueError). B no text shown to a person changed. C FR-14 stdout shape kept. D FR-59. E FR-37, FR-41. G FR-30, FR-32.

## Commit lines
architecture: AR-28, AR-9, AR-13, AR-15, AR-18, AR-24, AR-4, AR-29, AR-12 -- (how kept in message)
judgment: none -- the artifact_root and grounding_errors rows keep class shape, owner data; artifact_root keeps its literal ValueError unit
tier: sonnet

## Needed beyond the manifest
`ai-packages/qa-factory/scripts/slow_tests.json` (to identify slow files), `role_cli.py` (run_guarded/EXIT_REFUSED), `harness.py` (check_in/check_not_in), `refusal_registry.py`.

## Deviations / notes
- T2 stderr/stdout/calls checks run only for rows with a non-empty needle (spec: "for exit 2 with a needle"); the "no default folder in stderr" check asserts `qa-factory/artifacts/` absent.
- V6 key text contains `qa-factory/artifacts` (no trailing slash) by spec, so the check uses the trailing slash.
- Edit-tooling slip, fixed before commit: a heredoc escape produced a real NUL byte in hooklib; replaced with the two-character `\x00` (verified by grep; FR-29).
- `left_out_by_person` listing-failure refusal names the resolved root folder (`root_dir`), which the code resolved (FR-37). With the default root this path text contains `qa-factory/artifacts`; not covered by a test row (E17 pinned by reading only, as in the spec).

## Analogs noticed (not fixed)
- `left_out_by_person` import guard (:621-625) still gives None on any Exception (spec analog a).
- `_ticket_for_stage` callers outside exit_gate (`stage_guard` etc.) are OF4-10r rows.
- `vcs_evidence.py:646` existing text and `driver_sources.py:356` keep the literal default folder (OF4-21b).
