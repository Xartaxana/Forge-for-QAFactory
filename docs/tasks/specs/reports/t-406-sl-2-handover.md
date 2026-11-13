# t-406 SL-2 (B) handover

State: change STAGED in C:\QAFactory\forge-repo\.claude\worktrees\fg8-1 (branch wip/fg8-1, on 4e4ed9f), NOT committed.

## Question to the Lead (a pair of rows that conflict; I did NOT choose, the existing behaviour stays)
Dispatch `edges:` says: "which piles are touched" unknown (git unavailable, an unreadable range, `--base` unresolvable) -> the check judges
every pile like `--all` and says why in one line. Spec §3 B.1 / §4 B say the opposite: `range_paths` is CannotRun (exit 1) when git fails,
`--base` with an unresolvable REV keeps the existing CannotRun (cmd_check), test row `range-bad-rev` = exit 1. Both are "never nothing
touched". Implemented the spec's reading (exit 1, as `staged_paths` has always done); the switch would be in `run_check`, 2 lines
(catch CannotRun of `range_paths` / `staged_paths` -> `staged = None` + one line). Tell me if the dispatch reading wins.

## git diff --cached --stat
```
 tools/piles.py                | 211 +++++++++++++++++++++++++++++------------
 tools/test_piles.py           | 216 +++++++++++++++++++++++++++++++++++++++++-
 tools/test_piles_findings.py  |  20 +++-
 tools/test_piles_form.py      |   9 +-
 tools/test_piles_placement.py |  11 +--
 tools/test_piles_take.py      |  29 ++++++
 tools/test_workflows.py       |   2 +-
 7 files changed, 425 insertions(+), 73 deletions(-)
```
(test_piles.py shows 216 here and includes the two rows added last: `fn-list-py-waiting-batch`, `partly-untracked-pile`.)

## Witness (verbatim)
```
( cd <wt> && python -m pytest tools/test_piles.py tools/test_piles_findings.py tools/test_piles_placement.py tools/test_piles_form.py tools/test_piles_door.py tools/test_piles_frozen.py tools/test_piles_take.py tools/test_workflows.py -q )
E   AssertionError: ('python tools/piles.py check --all --base "$BASE"', 'python tools/piles.py check --base "$BASE"')
FAILED tools/test_workflows.py::test_forge_check_steps_equal_the_ordered_list_and_there_is_no_scrub_anywhere
1 failed, 458 passed in 325.81s (0:05:25)
```
Honest scope of that run: it started BEFORE I added two rows to test_piles.py (`fn-list-py-waiting-batch`, `partly-untracked-pile`) and before piles.py was
converted CRLF -> LF (content identical; my own python rewrite had made it CRLF, repaired with a scratchpad script, `git diff` unaffected). After both:
```
python -m pytest tools/test_piles.py -k "fn-list-py-waiting or partly-untracked" -q      ->  2 passed, 153 deselected in 6.84s
python -m pytest tools/test_piles.py -k scope_touched -q  (after the LF repair)         ->  19 passed, 136 deselected in 33.96s
```
The ONE red row is the one the dispatch named: `tools/test_workflows.py::test_forge_check_steps_equal_the_ordered_list_and_there_is_no_scrub_anywhere`,
list entry `'python tools/piles.py check --base "$BASE"'` (comment line 154 in this worktree, not 155). It goes green when the Lead places the workflow line below.
It cannot be kept green: the test reads the real `.github/workflows/forge-check.yml`, which is a non-goal.

```
python -m pytest tools/test_hook_liveness_probe.py -q -k live_run      ->  1 passed, 87 deselected in 9.36s
python tools/piles.py check --all                                      ->  ... (д) form: ok (33 piles, 100 batches) ... piles check: ok
python tools/lint_ratchet.py --check                                   ->  lint ratchet: 36 findings, 36 in the baseline, 0 new, 0 stale (pyflakes 3.2.0)
python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for tools/piles.py
   tools/piles.py: deleted or absent on disk, counted as changed
   tools/piles.py: not a script of scripts/, matched by keep `covers` and story folders only
   no scenario or keep row covers tools/piles.py: run the whole scenario layer
   tools/piles.py: test_scenario_cart_1.py / test_scenario_local_1_0108.py / test_scenario_local_1_arm_b.py / test_scenario_walk.py / test_scenario_world.py
```
The walk names five package scenario files for a forge tool. I ran them once under pytest from ai-packages/qa-factory (`timeout 280 python -B -m pytest scripts/tests/test_scenario_*.py`):
INTERNALERROR (`SystemExit: 0` from `harness.finish` at import, after 120 s, "no tests ran"). That is pytest-form only, not verified in any other form; they do not import
tools/piles.py (the walk itself says no row covers it). Not used as a witness.

## Red-before proof of the headline case
Scratch repo (script `scratchpad/headline.py`: piles_testkit mini tree; a committed unreadable finding in pile `report-delivery`, an UNTRACKED pile `stranger-pile`
with an unreadable finding; the commit stages one edit of pile `forge`'s card; `check`).
```
OLD = git archive 4e4ed9f tools -> piles.py of 4e4ed9f
exit 2
(д) form: RED -- plans/piles/report-delivery/findings/20261009-bad.md: cannot read this finding (not valid UTF-8 ...
(д) form: RED -- plans/piles/stranger-pile/findings/20261009-bad.md: cannot read this finding (not valid UTF-8 ...
(е) findings: no finding or batch file staged -- not checked
piles check: refused -- red: (д). Fix what is named above, or -- when the commit is deliberate -- add a line "piles-skip: <item> -- <reason>" ...
NEW = staged piles.py
exit 0
(г) backlog: plans/BACKLOG.md is not staged -- not checked
(д) form: 1 red(s) in piles this commit does not touch (not blocking): report-delivery
(е) findings: no finding or batch file staged -- not checked
piles check: ok
```
(`stranger-pile`, untracked, is not read at all; the committed red of `report-delivery` is one summary line.)

## Per spec item: function -- test row
- B.1 touched paths: `staged_paths` (unchanged), `+range_paths`, `+pile_of`, `Ctx.__post_init__` (`touched`), `run_check(range_rev=)`, `cmd_check` -- `range-mode`, `range-empty`, `range-bad-rev`, `fn-list-range`, `renamed-batch`.
- B.2 untracked: `load_tree(skip=)`, `load_pile(skip=)` (a pile with every file skipped -> None), `run_check` (`skip` in a commit only), `--all` note line -- `foreign-untracked-pile`, `partly-untracked-pile`, `all-mode-untracked-note`, findings `…_only_in_its_own_pile[report-delivery-untracked]`.
- B.3 decision rule: `Ctx.touches` (wildcard `CARDS_AND_FINDINGS` and `CARD_OR_FINDING_RE` deleted); `check_placement` + `+_a9_homes` (a9: BACKLOG + `git grep -l -w -F` at base); `check_form` (unreadable finding -> `(f.path,)`); `check_findings` (`homes` unfiltered); `_list_verdicts` (+ file x) / `+_pair_reds` / `check_overlap` (third carrier); `_relevant(staged, tree)` -- `a9-removal`, `a9-backlog-only`, `deleted-pile-move-line`, `fn-list-code-commit`, `fn-list-py-not-listed`, `fn-list-py-waiting-batch`, `fn-list-range`, `own-pile-red-elsewhere-in-pile`.
- B.4 per item: (а) `cross-pile-dupe`; (б) `overlap-pair-one-side`, `overlap-pair-neither-side`; (в) `check_frozen` filter by `ctx.touched` -- `range-mode` (a red-free (в) in range, existing frozen tests); (д) `_leftover_write_reds` filter, `check_form` -- `own-pile-red-elsewhere-in-pile`, `foreign-tracked-red`; (е) trigger unchanged -- existing `test_e_runs_in_a_commit_only_when_…`; (г) unchanged.
- B.5 output: `_split_reds`, `+_red_home`, `_item_lines` -- `foreign-tracked-red`, `overlap-pair-neither-side`, `range-mode`, flipped `test_check_carried_red_does_not_block_unrelated_commit`, `test_e_runs_in_a_commit_only_when…`.
- B.6 `--all` blocks on everything -- `all-mode-untracked-note`, flipped `…carried_red…` (`--all` exit 2), `test_check_d_judges_only_staged_files`.
- B.7 doors -- `a9-backlog-only` (the door `г` is used and (а) alone still blocks); existing `test_piles_door.py` unchanged and green.
- B.8 CI line -- `test_workflows.py` list entry (RED until the line is placed; see below).
- B.9 `take` -- `cmd_take` (`load_tree(skip=<untracked outside plans/piles/<slug>/>)`) -- `test_take_reads_untracked_like_check`: `foreign-untracked-broken-batch`, `foreign-untracked-active-overlap`, `own-pile-untracked-broken`, plus two controls `foreign-tracked-broken-batch` (exit 1) and `foreign-tracked-active-overlap` (exit 2).

## The CONTENT of the workflow line
`.github/workflows/forge-check.yml`, step "piles frozen batches and backlog" (line 84 in this worktree after SL-1, not 85):
```
        run: python tools/piles.py check --base "$BASE"
```
(only the `run:` value changes: `--all` is dropped; the step name, `env: BASE: ${{ steps.base.outputs.base }}` stay.) The pin is `tools/test_workflows.py` FORGE_CHECK_RUNS entry
`'python tools/piles.py check --base "$BASE"'`.

## Deviations, small choices
1. The conflict above (dispatch edge vs spec B.1 for an unreadable range / git failure).
2. Line numbers: workflow line is 84, test_workflows entry is line 154 (SL-1 shifted them).
3. Spec row `foreign-untracked-pile` says "plus one not-blocking line": a wholly untracked pile is not read at all, so there is no red to summarise; the row asserts exit 0 and that the pile and its reds are named nowhere. The "not blocking" line is asserted in `foreign-tracked-red`.
4. `_relevant(staged, tree=None)`: new optional arg; the `.py` branch lives in `run_check` (loads the tree once, tolerant, untracked skipped; a CannotRun there -> the check runs and its own load names it).
5. `_list_verdicts` now returns `[(message, file x)]`; `_pair_overlap` keeps its old return (messages) via the new `_pair_reds`, so old callers/tests and `take` are unchanged. The third carrier is `x` AND `ai-packages/qa-factory/<x>` (x is normalised without the package prefix; the staged path has it).
6. a9 carriers when `git grep` fails (rc not 0/1): every pile card (the safe side); `--all`: no lookup. `git grep -l -z -w -F -e <id> <base> -- plans/piles`, one call per a9 red.
7. `_split_reds` is one rule for every scope: (д) and (в) reds outside the touched piles are now summarised too (before: silently dropped for scope "files"). `check_frozen` skips untouched piles before reading git; `_leftover_write_reds` skips untouched piles.
8. `--all` note: `piles check: note: the untracked pile(s) a, b are judged here, a commit does not judge them (B.2)`, printed before the final line, only for `--all` without `--base`.
9. Existing tests changed (spec §5.2 "flips"): `test_a_staged_card_alone_is_blocked_by_an_unreadable_finding_elsewhere` -> `test_a_staged_card_is_blocked_by_an_unreadable_finding_only_in_its_own_pile` (3 rows: own pile blocks, other pile and other-untracked do not); `test_check_carried_red_does_not_block_unrelated_commit`, `test_check_d_judges_only_staged_files` (touch another pile; same-pile touch now blocks), `test_e_runs_in_a_commit_only_when_…` (new summary text). All three were same-pile cases that SL-2 B.4 makes blocking ("broader than today").
10. `take` with `git ls-files --others` failing (`untracked_piles` -> []): not tested (needs a monkeypatch of `piles.git`); the code path is the default (read everything).
11. `plans/piles/_template` only staged: `_relevant` stays true (startswith plans/piles/), the check runs, nothing is carried by it: unchanged from today.
12. Full test run is 5.5 min on this machine (the 8 files), not "fast".

## Analogs noticed, not fixed
- `cmd_close` (piles.py `load_tree(root)` at the close-batch writer) and `close --id` (second `load_tree(root)`) and `piles_split.py:663` read the strict tree including OTHER sessions' untracked files: a foreign untracked broken file makes them CannotRun, the same pain `take` had. Verdicts: must stay strict for what they write (a writer must not act on a tree it could not read whole); whether they should skip foreign untracked piles like `take` is a new decision (queue to Lead, same B.9 rule would apply).
- Readers with `tolerant=True` and no skip (`summary` cmd_summary, backlog_tree.py:34, compact_snapshot.py:375, forge_metrics.py:600, collect_intake.py:1112): they read untracked piles too (display/measure of the working tree) -- verdict: reads like `--all`, correct for them; unchanged by design (`load_tree` default skip is empty).
- Other runners of `piles.py check`: `.githooks/commit-msg:14` (`check --msg-file`; now scoped), `.github/workflows/forge-check.yml:84` (handover), `tools/hook_liveness_probe.py:953` case 14 (`--all`, unchanged, green), `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` lines ~977-998 check 33 (a) text (reworded in SL-5b), `tools/mechanism_gate.py:254` (lists piles.py as mechanism path). `.githooks/pre-commit`/`pre-merge-commit` do not run `piles.py check` (grep `piles\.py check` in .githooks found only commit-msg).
- The CHECKS comment and `check_findings` docstring now say "carried by touched path/pile"; the module docstring header of piles.py was not re-read for scope wording (not in the owns function list).

## Draft commit message
```
piles: a check judges only the piles the commit touches; take reads like check (SL-2, t-406)

A red blocks a commit when one of its carriers is a touched path or lies in a touched pile (BACKLOG.md and a function-list `.py` are carried by
their own path); the wildcard carrier CARDS_AND_FINDINGS is gone: a9 «open id placed nowhere» is carried by BACKLOG.md and the piles that named
the id at the base rev (`git grep -l`), an unreadable finding by its own path, (е) by the home piles of its `перенос:` (a `git rm` of a named pile
carries the red it causes), a (б) function-list verdict by the `.py` too. In a commit the untracked files of other piles are not read; `--base`
without `--all` takes the touched paths from the range (`range_paths`, CannotRun on a git failure) and reads the tree as is; `--all` blocks on
everything and names untracked piles. Reds elsewhere are one line per item (first 5 slugs, +K more). `take` skips the untracked files of other
piles, strictly reads the rest. The CI line becomes `check --base "$BASE"` in the integration commit (F-2 (a)); no audit step in CI, calibration
check 33 (a) is the reader of reds in untouched piles.

axis 1 (Policy <-> role): n/a (PROJECT.md item 8 lands in SL-5b).
axis 2 (Per-tier exam instruments): n/a.
axis 3 (Factory package <->): n/a (package).
axis 4 (Factory rules <->): n/a.
axis 5 (Stage twins inside): n/a (package).
axis 6 (Measurement tools <->): covered (`load_tree` gains `skip`, default empty: forge_metrics, compact_snapshot and backlog_tree calls unchanged).
axis 7 (Per-test identity <->): n/a (package).
axis 8 (Where the story): n/a (package).
axis 9 (is this a): n/a.
axis 10 (git-top readers): n/a (`git diff` / `git ls-files` / `git grep` with the tool's root).
axis 11 (shell-command recognizers): n/a.
axis 12 (carriers of the): covered (every red class with its carrier, spec §4 B; protocol check 33 reworded in SL-5b).
axis 13 (the dispatch text): n/a (function-list form 1 read by `dispatch_manifest` unchanged).
axis 14 (readers of agent): n/a.
axis 15 (console stream setup): n/a.
axis 16 (one JSON reader): n/a (package).
axis 17 (detector verdict shape): n/a (package).
axis 18 (in-tree shrink-only ratchets): n/a.
axis 19 (one reader of): n/a (package).
axis 20 (host receipt names): n/a (package).
axis 21 (readers of the): n/a.
axis 22 (a host's return): n/a (package).
axis 23 (fields of a): n/a (package).
axis 24 (the record of): n/a (package).
axis 25 (freshness of a): n/a (package).
axis 26 (the word stand): n/a (package).
axis 27 (the profile of): n/a (package).
axis 28 (the render site): n/a (package).
axis 29 (append-only jsonl writers): n/a.
axis 30 (the commands of): n/a (package).
axis 31 (Role carriers): n/a.
axis 32 (Where judgment lives): n/a (forge tools).
axis 33 (which dispatch am): n/a.
axis 34 (One road for): covered (one scope rule for the commit and CI; no second audit road in CI, F-2 (a); `take` and `check` skip untracked foreign files by one rule).
axis 35 (Sides of a): n/a (package).
axis 36 (The row written): n/a (package).

Four questions: (a) cost: about 240 skip lines a month gone; a code commit staging a listed `.py` loads the tree once; one `git grep` per a9 red;
(b) axes above; (c) detector: calibration check 33 (a) (the reader of untouched-pile reds) and (b'); (d) skip: commit-msg `check`, CI `check --base`.

tier: <model>

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
```

## Needed beyond the manifest
tools/piles_testkit.py and tools/conftest.py (fixtures and helpers used by the new rows; not edited), tools/gitcmd.py (git helper), tools/hook_liveness_probe.py (case 14, read only),
.github/workflows/forge-check.yml (read for the line), .githooks/ (siblings grep), PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md (siblings grep), spec §7 F-2/F-3.
