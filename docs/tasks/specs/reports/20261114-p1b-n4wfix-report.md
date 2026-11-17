# P1-b N4w fix report (t-828, builder)

Branch `wip/p1b-n4wfix`. Files (all under `ai-packages/qa-factory/scripts/tests/`): `dry_exits.py`, `fixtures/driver-exits/known_red.json`, this report. `dry_world.py` and `test_scenario_dry_1.py` untouched (the alive line is produced only in `dry_exits.judge_group`; found by search "alive only stop").

## What changed
1. Selftest isolation, `dry_exits.py:1472` (in `_selftest_cases`): a local `check(directory, walk_dir, universe, ledger_path)` shadows the module `check`; with no `walk_dir` it passes its own EMPTY temp dir, then calls the real `globals()["check"]`. All ~25 calls in that function (the ones with `walk_dir=None`) are covered with no per-call edit; calls that already name a walk dir are untouched. New case `isolation: a real-looking walk file ...` (`:1669`) plants a real-looking `s0.json` and points `WALK_DIR` at it: the isolated call is green, the control (real `check`, default dir) is red. `WALK_DIR` is restored in `finally`.
2. `alive` under a ledger label, `dry_exits.py:1365-1380` (`judge_group`): subjects now carry the row id; after rows were judged and `known_red.reconcile` ran (edge e), an `alive` problem is a NOTE `alive only stop: ...; known red: <row> -> <node>` only when EVERY contributing (moving) variant is `fail` AND its id is in the filtered ledger; otherwise FAIL as before. A ledger that cannot be read gives an empty ledger -> FAIL (edge a); a ledgered row that passed is not `fail` -> FAIL, and reconcile still prints its `stale` line (edge c). New table cases (`:2519` on): all ledgered -> note; one unledgered -> fail; ledgered + passed-but-unchanged -> fail; no red rows -> today's fail; unreadable ledger -> fail + `known_red` fail line.
3. Label: `known_red.json` row `kind:halt/free words` -> `{node: N4S0-1, raised_by: "Lead t-828 (...): the driver prints 'answer for halt' but records no answer row, does not resume the role and goes to the conductor; driver or stub: open"}`; `pins.known_red` 1 -> 2 (the ledger's shape is `{node, raised_by[, note]}`, so the "why" is in `raised_by`; the helper has no `why` key).

## Verification (verbatim)
`dry_exits.py --selftest` (with `exits/s0.json` present):
```
dry_exits selftest: 154/154 cases
```
(148 + 5 alive cases + 1 isolation case.)

`test_scenario_dry_1.py --part exits:s0`, one run (background; the harness printed no seconds line, estimate not measured: under the ~2 min the Lead gave):
```
NOTE dry-1/exits:s0/kind:halt/free words: red evidence: C2: the driver recorded no answer for this ask (...); C3: the answer changed nothing: ...
PASS dry-1/exits:s0/kind:halt/empty
NOTE dry-1/exits:s0/known_red: known red: kind:halt/free words -> N4S0-1
NOTE dry-1/exits:s0/alive: alive only stop: kind:halt: every variant but stop left the state fingerprint unchanged (free words); known red: kind:halt/free words -> N4S0-1
PASS dry-1/exits:s0/outcomes
NOTE dry-1/exits:s0/unwalked: 0 (census unwalked 0: none; variants without a row 0: none)

=== scenario dry-1: 2/2 ok ===
rc=0
```
(live_only rows and the two scoreboard lines elided here; all NOTE.)

`( cd <pkg> && python -B scripts/selftest.py --limits --lang )`: `=== qa-factory selftest: 4/4 ok ===`.
Not run (per brief): `--part exits:selftest`, `--part main`, CI, mutations.

## Selftest cases that read real files on purpose
None read the real `exits/` or `seeds/` any more (the only place that touches `WALK_DIR` is the isolation case, which swaps it). One observation, not changed: the message-only cases in `_walker_cases` that print `unknown part ...; (groups found: gates, grp, hooks, s0, ...)` list the REAL `driver-exits/` census names next to a fake `grp`; they judge only the message form, not the group set (they passed with and without s0 present at baseline), but I did not read their source.

## FR walk
A: refusals - no refusal text changed; the alive FAIL text is unchanged, the NOTE adds the ledgered row and node (FR-1, FR-4: a ledgered red is an informed pass, never silent). B: text to a person - not changed. C: contracts - judge_group's line shape (name, kind, detail) unchanged. D: evidence - FR-41/FR-59: a red row unlabelled, passed-yet-unchanged, or a missing ledger stays FAIL; never a pass on unknown (AR-25, AR-28). E: delivery - n/a. F: measurement - n/a. G: FR-54: siblings walked (below); FR-30 English, `selftest --lang` green.

## Questions
none.

## Siblings noticed
- Callers of `check(...)` with a defaulted dir outside the selftest: only `main` (`dry_exits.py:2553` area, `check(args.dir, args.exits_dir)`) - the default is the real walk dir on purpose, not a defect. `load_walk_rows`/`driven_keys` with defaults: only inside `check`/census use; selftest callers pass explicit roots.
- `_walker_cases` (separate function, `check` there is the module one): contains no `check(` call, so the shadow is not needed; the isolation case sits in `_selftest_cases` for that reason.
- The `known_red` line and `outcomes` line behaviour unchanged (visible in the run above).
- `_count_reach` double count (s0 report q1) not touched.

## Needed beyond the manifest
none beyond reading `dry_exits.py` in full around the selftest.
