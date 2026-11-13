# t-385 FG8-1 (SL-1) -- handover report

Worktree `C:\QAFactory\forge-repo\.claude\worktrees\fg8-1`, branch wip/fg8-1 (from 5d79f97). NOT COMMITTED: the tree is STAGED
(10 files). Two things stopped the commit: (1) the mechanism gate (tools/piles.py is a gate path) wants an axis block and a
`tier:` line not below Lead; (2) my attempt to test the axis labels with `git commit -F <message file>` was denied by the
auto-mode classifier, and I did not retry. The first trial commit (a bare message, `tier: sonnet`) was refused by the gate
(output below); nothing was committed (`git log` head is still 5d79f97).

## UPDATE after the Lead's answers (supersedes the questions and the witness below where they differ)

Final witness: DoD set + `test_piles_close_id.py` + `test_piles_placement.py`: `3 failed, 672 passed in 166.73s` -- the 3 were
test_workflows (17 == 16, the temporal edge) and two close_gate tests my first guard placement broke; guard moved (below);
re-run of `test_piles_close_gate.py test_piles_findings.py test_piles_close_id.py test_piles_close.py`: `347 passed in 116.81s`.
Lint: `lint ratchet: 36 findings, 36 in the baseline, 0 new, 0 stale (pyflakes 3.2.0)`. Only test_workflows stays red (temporal edge).

- Q1 done: new `refuse_unreadable_prose(tree)` (piles.py, beside `pile_prose`): `pile_prose` + `_finding_moves` of every finding, i.e. the same
  reads (е) does. Called BEFORE any write in `cmd_take` (right after `load_tree`), `_close_word` (after `load_tree`) and `_close_batch`
  (after `check_leftovers`/`check_proofs`, before `_plan_batch_close`: placed after the batch's own gates because two tests
  `test_gate_refuses_a_line_that_is_neither_finished_nor_carried_with_a_person[```-has neither]` and
  `test_a_fence_in_hod_cannot_hide_the_ostatki_heading` expect close's own refusal text first). The two tests of test_piles_findings.py stay; the
  take one dropped the substrings "writing failed" / "nothing changed" (they described the old rollback; now nothing is written at all, still
  asserted by `tree_state(tree) == snap`); the fence text part stays.
- Q2 done, rows: `test_piles_close_id.py::test_close_word_cap_at_120_and_board_reads_hash_back` -> `..._and_the_closed_row_reads_hash_back`: cap half stays,
  read-back moved to the backlog «Закрыто» row via `piles.closed_hash(closed_rows(tree)[id])` (summary prints no id->hash); unused `re` dropped.
  `test_piles_placement.py::test_check_a5_and_the_board_give_one_verdict...` -> `test_check_a5_and_summary_agree_on_a_closed_id_that_is_still_placed`:
  check half stays; the three `toc_of` asserts (TOC text only the board had) died, `toc_of` died; the open-count assert (`открытых id: 6`) moved to
  new testkit helper `summary_text` (summary gives no per-id verdict); unused `re` dropped. `board_text` stays deleted.
- Midway test: already adapted to the one-write reality (failure injected at the finding deletion).

## Questions to the Lead (ANSWERED; kept for the record)

1. TWO TESTS GO RED, NOT NAMED IN §5.1: `test_take_refuses_when_a_finding_has_an_unclosed_fence_names_file_and_line_and_writes_nothing`
   and `test_close_refuses_when_a_finding_has_an_unclosed_fence_names_file_and_line_and_writes_nothing`
   (`tools/test_piles_findings.py:495, 509`, t-870 F-5 "halts every path"). Cause, measured: their refusal came ONLY from
   `rebuild_board` -> `render_board` -> `_incoming` -> `pile_prose` -> `_batch_prose` -> `_unclosed_fence_error` (CannotRun
   `<path>:<line>: ... never closed`), run after the writes and rolled back. `cmd_take` / `_close_batch` / `_close_word` never
   call `pile_prose`, so with the board gone `take` and `close` SUCCEED on a tree whose finding (or batch file) carries an
   unclosed fence (verbatim failure: `piles close: forge/1 closed with ... assert (0 == 1)`). Only `check` still refuses it.
   Fork: (a) accept the loss, delete the two tests; (b) keep the guard: `take`/`close` call `pile_prose(tree)` (or one named
   reader) on the tree they load, before the writes, so the refusal names file:line and nothing is written -- then the two tests
   stay as they are. §4 A "take and close write the same files as before" says nothing on this refusal. I changed neither the
   tests nor `cmd_take`/`close`.
2. `tools/test_piles_close_id.py:14,71` and `tools/test_piles_placement.py:14,164,181` import `board_text` (deleted by §5.1, and
   the files are not in my `owns`, nor in §5.1). Both files now fail at COLLECTION (`ImportError: cannot import name
   'board_text' from 'piles_testkit'`; run: `2 errors in 0.34s`). They pin the TOC text of the board
   (`toc["B-102"] == "закрыто (хэша нет)"`, `"закрыто `<h>`"`, `"(и открыт — ошибка)"`, `"открытых id: 6 "`) -- the TOC dies
   with the board; only the count `открытых id: 6` can be retargeted to `summary`. Needs: which rows die, which move to
   `summary` (and a dispatch that owns these two files). `test_piles_close_id.py::test_close_word_cap_at_120_and_board_reads_hash_back`
   keeps its close half (the cap) and loses the "reads the hash back" half (`closed_hash` is still tested by `test_piles_close.py:35`).
3. Spec reality divergence (recorded, not a question): `test_close_id_that_fails_midway_puts_the_row_and_the_finding_back` -- §5.1 says
   "monkeypatch `write_like` on the second path", but `close --id` has ONE write (BACKLOG) and one deletion (the finding). I
   made the failing step the deletion: `pathlib.Path.unlink` patched to delete and then raise for `B-102*`, so the rollback
   has to restore the finding AND the row. Say if you want something else.

## What was done

- `tools/piles.py` (-270/+, see stat): removed `BOARD_REL`, `_esc`, `_shown`, `_same_status`, `_same_branch`, `_incoming`,
  `_board_cells`, `_prio_rank`, `board_table`, `_toc_text`, `toc_lines`, `BOARD_HEAD`, `render_board`, `untracked_warning`,
  `unreadable_warning`, `board_triggers`, the old `cmd_board`, `_print_all`, `rebuild_board`; `write_atomic`/`write_bytes_atomic`,
  `_open_sets`, `_count_line` kept. `apply_changes`: rollback set = written + deleted paths, no `rebuild_board`. Printed `git add`
  of take/close without `plans/PILES.md`. Docstring and four comments reworded per §2.1/§2.2.
  - `board`: `cmd_board` raises CannotRun (exit 1) with the §2.1 text; `_board_args` takes nothing; ONE mechanism with `release`:
    `REFUSED_ALIASES = ("release", "board")` read by `build_parser` (no `--help`) and `main` (extra arguments unread).
    Verbatim: `piles board: `board` was retired (the owner, 13.11.2026: there is no board) -- the open batches are shown by
    the «Бэклог» pane, or run `python -B tools/backlog_tree.py`; nothing was run`, rc=1 for `board --check --if-staged`.
  - `summary`: `cmd_summary` = `load_tree(tolerant=True)` + `_open_sets` + id sort + `_count_line` (text unchanged), prints, writes
    nothing, exit 0; unreadable tree -> CannotRun exit 1 (test: broken `## Закрыто` -> exit 1).
  - `load_tree(with_untracked=...)`: no caller passes it any more (the board warned on untracked files). Left as is (SL-2 reads
    untracked piles itself); docstring says so. Dead parameter + `Tree.untracked` field: a noticed analog, not removed.
- `tools/backlog_tree.py:1`: docstring reworded per §2.1.
- `tools/piles_testkit.py`: `board_text` deleted (fixture `F0-2` token `plans/PILES.md` stays).
- Tests, as §5.1: `test_piles.py` (17 board tests died; `test_pile_folder_without_readme_is_red_in_check`; `test_refusals_exit_1`
  with the alias rows; `test_board_is_a_refused_alias_naming_the_pane` x3 rows incl. `--help`; two new `summary` tests;
  subprocess test without the board half; unused `os`/`re` imports dropped), `test_piles_findings.py` (3 board tests, 2 `_incoming`
  tests and helper `incoming` died; `incoming(...)` asserts dropped from 3 other tests, their `run_e` asserts stay; unused `re`
  dropped), `test_piles_close_gate.py` (param "board" gone; `close --id` midway test -> failing unlink; k14 -> `summary`),
  `test_piles_take.py` (as listed; the midway tests -> failing `write_like`), `test_piles_close.py` (rename + 3 board asserts),
  `test_md_table.py` (two `("board",)` params gone), `test_workflows.py` (row 154 only).

## Witness (verbatim)

`python -m pytest tools/test_piles.py tools/test_piles_take.py tools/test_piles_close.py tools/test_piles_close_gate.py tools/test_piles_findings.py tools/test_md_table.py tools/test_workflows.py tools/test_backlog_tree.py tools/test_compact_snapshot.py -q` (from the worktree):

```
tools\test_workflows.py:169: AssertionError
FAILED tools/test_piles_findings.py::test_take_refuses_when_a_finding_has_an_unclosed_fence_names_file_and_line_and_writes_nothing
FAILED tools/test_piles_findings.py::test_close_refuses_when_a_finding_has_an_unclosed_fence_names_file_and_line_and_writes_nothing
FAILED tools/test_workflows.py::test_forge_check_steps_equal_the_ordered_list_and_there_is_no_scrub_anywhere
3 failed, 651 passed in 148.52s (0:02:28)
```

- test_workflows = the TEMPORAL EDGE, as predicted: `assert len(got) == len(FORGE_CHECK_RUNS)` -> `assert 17 == 16` (row 154 gone,
  `forge-check.yml:81` `- run: python tools/piles.py board --check` still in my tree). Goes green in the Lead's integration commit
  when line 81 is removed (below). The other two reds: question 1 above.
- `python -m pytest tools/test_piles.py -q` alone: `136 passed in 10.96s` (before the later edits to other files).
- `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for tools/piles.py tools/backlog_tree.py` printed:
  `tools/backlog_tree.py: deleted or absent on disk, counted as changed` / `tools/backlog_tree.py: not a script of scripts/, matched by keep
  `covers` and story folders only` / `no scenario or keep row covers tools/backlog_tree.py: run the whole scenario layer` (+ the list of
  scenario test files). That is the expected report line; I did not run the scenario layer (CI canon).
- `python tools/piles.py check --all` ends `piles check: ok`.
- `python tools/piles.py summary` -> rc=0, first line `кучек: 33; пачек: ожидает 22, в работе 10, закрыта 67; открытых id: 296 (в пачках 114 / в находках 182 / не разложено 0); находок без id: 809; не разобрано находок: 0; закрытых: 136; следующий свободный B-id: B-473 (выдаёт только интегратор на main); остатков без исполнителя: 2`, then the `не-id в строках:` line.
- `python tools/piles.py board --check --if-staged` -> the refused text above, rc=1.
- `python tools/lint_ratchet.py --check`: `lint ratchet: 36 findings, 36 in the baseline, 0 new, 0 stale (pyflakes 3.2.0)` (first run had 2 new,
  the unused `os`/`re` in test_piles.py; fixed).

## Key grep and control

Grep tool, case-insensitive, pattern `PILES\.md|BOARD_REL|board --check`, path `tools`, glob `*.py` -> remaining lines (all fixture strings / "no board" asserts, nothing else):

| line | reason |
|---|---|
| `tools/piles_testkit.py:127` `node("F0-2", "`plans/PILES.md`", ...)` | fixture node token (§5.1: stays) |
| `tools/test_piles_frozen.py:33, 59` | edit that fixture cell (§5.1: stays; not my file) |
| `tools/test_piles.py:182, 201` `assert not (tree / "plans/PILES.md").exists()` | new alias/summary rows: nothing is written |
| `tools/test_piles_take.py:47, 181` `"PILES.md" not in out` | §5.1 take rows: the printed command / output names no board |

The positive control of the same shape (same tool, `*.py` glob) is the testkit line itself, which the pattern found. No `BOARD_REL` and no
`board --check` remain in `tools/*.py`. Other `board`-word mentions left in `piles.py` (not PILES.md): docstring lines 15-16, 22, 42 (history of the
retirement and "There is no external board"), and `cmd_board`/`_board_args`/`COMMANDS["board"]` (the refused alias, §2.1).

## Siblings (axis 12): grep of every removed name

Grep tool, `type: py`, root = the worktree, pattern `render_board|rebuild_board|board_table|toc_lines|_incoming|untracked_warning|unreadable_warning|board_triggers|BOARD_HEAD|_board_cells|_toc_text|_prio_rank|BOARD_REL|_print_all|board_text`:
hits only in `tools/test_piles_placement.py:14,164,181` and `tools/test_piles_close_id.py:14,71` (`board_text`: question 2) and the
`DASHBOARD_REL` false positives of the package (`onboard_apply.py`, `test_install_retire.py`, `test_reinstall_equals_fresh.py`, `test_two_folders.py`,
listed in §2). Control (same call shape, `type: py`): `write_bytes_atomic|render_board|rebuild_board` found `piles.py:949,952,2875` and `collect_intake.py:503-549`.
(A first attempt with a brace glob `{tools,scripts,ai-packages}/**/*.py` returned nothing even for the control: a miscalled glob, discarded.)
Readers checked: `backlog_tree`, `compact_snapshot`, `forge_metrics`, `collect_intake`, `piles_split`, `canon_clock`, `hook_liveness_probe`:
none imports a removed symbol; the word "board" appears in them only inside `dashboard`/`onboarding` (case-insensitive grep, control = those hits);
`hook_liveness_probe.py` (15 `piles` mentions) and `canon_clock.py` (1) have no board call. `_count_line` / `_open_sets` have no
other caller than `cmd_summary`.

## Content for the Lead to place (enforcement files, not written by me)

1. `.github/workflows/forge-check.yml`, line 81 is removed (the line before it is `      - run: python tools/agents_md.py --check`, after it
   `      - name: piles frozen batches and backlog`):

   before: `      - run: python tools/piles.py board --check`
   after: (line deleted)

2. `tools/mechanism_gate.py:254`:

   before: `    "tools/piles.py",               # .githooks/pre-commit + commit-msg + pre-merge-commit (piles board/check, F0-2)`
   after:  `    "tools/piles.py",               # .githooks/pre-commit + commit-msg + pre-merge-commit (piles check, F0-2)`

3. Not mine, listed by the spec for SL-5a: `.claude/settings.json:139,158`, `.gitattributes:21`, `git rm plans/PILES.md`.
   After 1, `test_workflows.py::test_forge_check_steps_equal_the_ordered_list...` is expected green (16 == 16).

## The commit message for the Lead (tier placeholder)

The text is in `C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\acb1ecf0-04a8-42f3-8bdd-f14a2dae87bf\scratchpad\t385-msg.txt` (session scratch; the same
text follows). The axis labels are the first three words of each map heading as the gate describes its SHORT key; I could NOT confirm them against
the gate (my attempt to test them was denied), so the gate may print another form for some axes -- use its refusal text. Replace the `tier:` line.

```
piles: the board leaves piles.py; summary; board is a refused alias (SL-1, t-385)

axis 1 (Policy <-> role): n/a (no policy, role or journal text in this commit; PROJECT.md follows in SL-5b).
axis 2 (Per-tier exam instruments): n/a (no exam instrument).
axis 3 (Factory package <->): n/a (package release copy; nothing ships).
axis 4 (Factory rules <->): n/a (no factory rule, debt or principle).
axis 5 (Stage twins inside): n/a (package stage twins).
axis 6 (Measurement tools <->): covered (forge_metrics and compact_snapshot read load_tree, unchanged; test_compact_snapshot.py in the DoD).
axis 7 (Per-test identity <->): n/a (per-test identity of the package).
axis 8 (Where the story): n/a (story location, package).
axis 9 (is this a): n/a (test-file leaf, not touched).
axis 10 (git-top readers): n/a (no new reader of the repository top).
axis 11 (shell-command recognizers): n/a (no shell-command recognizer).
axis 12 (carriers of the): covered (producer piles.py and its readers: backlog_tree, compact_snapshot, forge_metrics, hooks, CI, settings, .gitattributes; texts follow in SL-5b).
axis 13 (the dispatch text): n/a (dispatch text untouched).
axis 14 (readers of agent): n/a (no transcript reader).
axis 15 (console stream setup): n/a (piles.py console setup unchanged).
axis 16 (one JSON reader): n/a (package JSON reader).
axis 17 (detector verdict shape): n/a (package detector verdict shape).
axis 18 (in-tree shrink-only ratchets): n/a (no ratchet).
axis 19 (one reader of): n/a (package role-file reader).
axis 20 (host receipt names): n/a (package host receipts).
axis 21 (readers of the): n/a (forge tables read by md_table, unchanged).
axis 22 (a host's return): n/a (package).
axis 23 (fields of a): n/a (package).
axis 24 (the record of): n/a (package).
axis 25 (freshness of a): n/a (package).
axis 26 (the word stand): n/a (package).
axis 27 (the profile of): n/a (package).
axis 28 (the render site): n/a (package).
axis 29 (append-only jsonl writers): n/a (no jsonl appender).
axis 30 (the commands of): n/a (package).
axis 31 (Role carriers): n/a (no role file).
axis 32 (Where judgment lives): n/a (forge tools, outside the census).
axis 33 (which dispatch am): n/a (no dispatch identity).
axis 34 (One road for): covered (board and release are retired by one road: a refused alias naming the new road, t-367 N9).
axis 35 (Sides of a): n/a (package).
axis 36 (The row written): n/a (package).

Four questions: (a) cost: less -- no board to stage, fewer doors; (c) detector: tools/test_backlog_tree.py (the pane), check 33 (a);
(d) skip: the refused alias on the execution path, agents_md --check and the hooks in the same commit.

tier: <the Lead's tier>
architecture: none -- tools/ of the forge, no package file touched
```

(The `architecture:` line is owed only to package commits; it is harmless here.)

## The gate's refusal of the trial commit (verbatim, head)

```
mechanism_gate: commit touches mechanism files:
  tools/piles.py
Rule 10(b)'s axis block has no labelled line (since 2026-10-16 the axis key is mandatory) for axes: 1, 2, ..., 36
Write "axis N (<key>): covered / queued / n/a <why>" with the key from the map; the real headings: ...
```
(pre-commit stage before it: `ESCAPE ALLOWLIST OK: 0 entries`, `factory rules index: up to date (59 rules)`, `architecture index: up to date (29 invariants, 2682 bytes)`, `AGENTS.md: up to date (117450 bytes)`.)

## Noticed analogs (not fixed, outside owns)

- `Tree.untracked` and `load_tree(with_untracked=...)`: dead after SL-1 (SL-2 decides).
- `piles.py` still has `closed_but_placed`, `pile_prose`, `status_word`, `first_tick`: all still used by `check` (verified by lint: no new unused names).
- `tools/test_piles_form.py`, `test_piles_frozen.py:33,59` carry the `plans/PILES.md` fixture token (§5.1: stays).
- Docs outside tools/ that call the board the authority: the Lead's SL-5b list (§2.2).

## Needed beyond the manifest

`tools/mechanism_gate.py` (to read the axis-label rule), `tools/test_piles_close_id.py`, `tools/test_piles_placement.py`, `tools/test_piles_frozen.py`
(grep hits), `docs/SIBLING_MAP.md` (axis headings), `ai-packages/qa-factory/scripts/tests/scenario_walk.py` (the witness command).
