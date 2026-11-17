# t-1098 / FV3-20 - the dry stub's S6 runner hands back what a runner hands back (report)

## 1. Product facts (item 1)

- The S6 exit gate for the automation half (`S6-qa-runner-1`, scope TC-1) reads: the digest through `role_digest.check` (`role_digest.py:368-386`: header `<role> <stage> <window> · ok|concerns|halt|impossible`, a row per scoped id, a task-relative path as the last line) and the handover form through `handoff_check.py` (every field not a hint: 20 fields were refused, `scope` among them). The code-derived fields (`run.execution_status/witness/totals/window_totals`, `inputs_read[].version`) come from `work/run-report.json` / the manifest by `handoff_check --fix` (`handoff_check.py:716-752`); the report already exists after S5, so nothing else is needed from the role.
- What the role owes by hand: the rows of `scope`, `inputs_read[].path`, `header.verdict`, `run.environment/application_build/probe_before/probe_after`, `superseded`, `claims.*`, `tried`. The filler also invents junk for every other hint (`manual_observations`, `env_blocked`, `unresolved`, `blocked` get "filled ..." rows, e.g. TC-1 `blocked_by_check`), so the story row empties/drops them (section-level `[]` / `$absent`, `form_filler.fill_form`).
- A field whose honest value the story data cannot give: `run.application_build` (the probe answered `not_applicable`, `observed_runtime_identity` is empty: written as "not established: ..."). `tried_note` is a scalar the override grammar cannot set (only ABSENT/[]), so `tried[0]` carries a row and `tried_note` is dropped.
- The stub's old live_only `work/evidence/manual/<case>/tried.md: no contract heading` stays in the journal row (informational): a `tried.md` is the manual window's exploration log; the automation window wrote no cell and the `tried[0].evidence` cites `work/run-report.json`.

## 2. What changed

- `scripts/tests/dry_stub.py`: `NEWEST_WORD` / `resolve_newest` (new, before `_fill_form`): `<newest:GLOB>` in a string override value is replaced by the task-relative path of the newest file (mtime, then name) the glob finds under the task root; no match, an absolute glob or `..` is a KitError naming the key and the override. Called in `_fill_form`. Needed because the records a form cites carry a clock in their name (`evidence/runtime-provenance-<profile>-<ts>.json`). Selftest: 240 rows (was 234; +6 FV3-20 rows: resolution incl. in text and non-text, three KitErrors, the story's S6 digest through `role_digest.check`, the story's S6 row fills the real form).
- `fixtures/stories/dry-1/story.json`: new row `qa-runner@S6` (verdict `ok`, digest `qa-runner S6 S6-qa-runner-1 · ok / TC-1 · green · ... / work/run-report.json`, `overrides.s6-runner-to-analyst`).
- `fixtures/driver-exits/known_red.json`: row `main/S6` re-measured (below); old "a new finding is owed" note removed; pin 1.
- `changelog.d/dry-stub-s6-runner.md`.

## 3. The main pass after the change

S0..S5 and gate_A PASS. `S6-qa-runner-1` (automation half): the stub wrote its form (`wrote=1`), the exit gate accepted it (events: `accept` after the dispatch, then the next dispatch `S6-qa-runner-2` opens). The pass stops at the MANUAL half. Verbatim head of the stop note:
`stopped at S6: no answer for exit_limit at S6 in story dry-1 (A1-E3): the walk rows of story.json hold none; ... - run-report.json: TC-2 is \`manual-agent\` in the plan (TS-2) but appears in no lane of this report - not in results[], manual_checks[], skipped[], impossible[], env_blocked[] or manual_skipped[]. A case left out reads as untested - say where it went. ... - digest: your final message is not the handoff form. ... TC-2 was in this dispatch's scope and has no line ...`
`the driver's first refusal: resume S1-qa-scout-1: the person answered what the role stopped for`.

Classification (b), not stub-around-able: TC-2's lane is built from a walk record; the walk's own after-step wrote `refused: nothing was captured for TC-2. Capture first: manual_capture.py ui --steps-file ... or manual_capture.py http ...` (`work/walks/S6-qa-runner-2/after.json`). A capture needs a stand; the dry world has none (brief: "Environment: ?", "the stand was not walked: no stand", walk actor `guest`). The honest value (a verdict quoting a capture of this attempt, `references/manual-evidence.md`) is one the story's data cannot support; none invented. The stub half (the digest of dispatch 2 repeats the TC-1 line because one `qa-runner@S6` row serves both S6 dispatches and the story key has no way to tell them apart) is moot until the lane has a capture and is a design choice (a key for the manual half), so it is left.

Observation for the Lead (candidate product question, not decided): with the person's `go on` on the stand (S5 answer `environment`, price key `s6.stand_confirm`), the automation half closes with no stand (`driver_stage_s6.py:672 s6_no_stand`, `:565` K4), but the manual half is still dispatched as a walk with no stand and stops at `exit_limit`.

Forks for the Lead (not decided here): (1) give the dry world a stand; (2) make TC-2 `manual-human` in `kit.json`; (3) the product question above. Budget: the stub grew ~25 lines of code, ~35 of story data; the pass was not widened to S7/S8/S9 (not reached; their stub rows are still absent).

Group rows `gate_B/{approve,empty,free words,retry,rework,stop}`: still `after:FV3-20: its start snapshot S8 was not made` (snapshots stop at S5). None ran, no group ledger edited.

## 4. FR walk

G: FR-29 no heredoc/control byte in package files (edits by tool; the `python -` edit of story.json held ASCII only); FR-30 English ASCII; FR-31 no load-dependent test; FR-32 root cause = the stub gave the S6 runner no form values and no digest, test rows + green selftest; FR-34 n/a; FR-54 siblings: section 7. C: FR-11/FR-15: the cited records are resolved from disk, never typed; FR-59: a `<newest:...>` with no match is a named KitError, never a hint or empty path. A/B/D/E/F: not changed (test stub only). Package change: the owns are under `scripts/tests/` + `changelog.d/`; AR-n touched: none (test double).

## 5. Witness (verbatim tails)

```
$ python -B .../tests/dry_stub.py --selftest
=== dry_stub --selftest: 240/240 ok ===
$ python -B .../tests/dry_exits.py --check
dry_exits --check: 0 discrepancies
$ python -B .../tests/dry_exits.py --selftest
dry_exits selftest: 201/201 cases
$ python -B .../scripts/selftest.py --lang
PASS lang: no control byte left by an eaten escape sequence (FR-29)
=== qa-factory selftest: 2/2 ok ===
$ python -B .../tests/scenario_walk.py --witness-for <dry_stub.py, story.json, known_red.json>
scripts/tests/dry_stub.py: keep test_scenario_dry_1.py (layer scenario, covers it)
scripts/tests/fixtures/stories/dry-1/story.json: scenario test_scenario_dry_1.py (story dry-1)
scripts/tests/fixtures/stories/dry-1/story.json: keep test_scenario_dry_1.py (layer scenario, covers it)
scripts/tests/fixtures/driver-exits/known_red.json: keep test_scenario_dry_1.py (layer scenario, covers it)
$ python -B .../tests/test_scenario_dry_1.py     (whole file, once, after the ledger edit)
PASS dry-1/census ... PASS dry-1/main/S0..S5, PASS dry-1/gate_A  (known red: main/S6 -> FV3-20 is a NOTE)
=== scenario dry-1: 10/10 ok ===      rc 0
```
Negative control (byte copy; `cp story.json -> scratchpad/story_s6.orig`, sha256 `54799590460c9023fd522e96a87b01e92cf00f45fdc2aba1ae8562de7e5c07c3` before and after, equal): the `inputs_read[0].path` line removed ->
```
UNFILLABLE s6-runner-to-analyst: cannot fill inputs_read[0].path: a hint inside a value that no context token names ... (E10)
handoff_check: s6-runner-to-analyst is not ready - 20 field(s) below.   (the form left as the controller's template; same 20 fields as the original stop)
```
and with the row present, `handoff_check --fix` on the stub's form: `handoff_check: s6-runner-to-analyst is complete (79 fields checked)`. The control was run on the form-and-gate pair (seconds), not by a second full pass (9 minutes); the full pass above is the positive proof that S6-qa-runner-1 is accepted.

## 6. Analogs noticed (reported, not fixed)

- The same `qa-runner@S6` row answers BOTH S6 dispatches (automation, manual); the story key has `#<digit>` windows only for S3 (`window_of`, `STUB_KEY`). Any future per-dispatch row (S6 manual, S7 triage with several windows) hits the same.
- The filler writes junk for every list section it cannot judge (`env_blocked`, `unresolved`, `blocked`, `manual_observations` with TC-1 "blocked_by_check"/"owner: factory"): any other stub form whose contract has such sections and whose story row does not empty them hands the analyst false rows (S7 `qa-failure-analyst`, S8 `qa-doc-scribe`, S9 `qa-retro-analyst` rows: absent).
- `story.json` row `qa-code-critic@S5.files` still hard-codes `S5-qa-code-critic-1` in the probe-model path (noted by t-1088; `<dispatch>` now works there too).
- `tried_note` (scalar) cannot be set by an override; only ABSENT/[] reach a top-level key.

## 7. Needed beyond the manifest

`scripts/role_digest.py`, `scripts/handoff_check.py`, `scripts/driver_dispatch.py`, `scripts/driver_stage_s6.py`, `scripts/tests/form_filler.py`, `scripts/tests/fixtures/form-fill-rules.json`, `scripts/tests/dry_world.py`, `agents/qa-runner.md`, `skills/qa-story/phases/s6.md`, `references/manual-evidence.md`, `handoffs/s6-runner-to-analyst.yaml`.

## 8. Questions

1. The new stop (manual half of S6, TC-2) needs a Lead fork: stand for the dry world, TC-2 as manual-human, or the product question about the `go on` on the stand. Row left on FV3-20 as `main/S6`.
2. A key to tell the two S6 dispatches apart in the story's `stub` table (design choice, not made).
