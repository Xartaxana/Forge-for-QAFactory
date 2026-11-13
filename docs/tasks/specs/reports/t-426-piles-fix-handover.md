# t-426 handover -- piles slimming, fix round after the topic critic (t-421)

Worktree `C:\QAFactory\forge-repo\.claude\worktrees\fg8-1`, branch wip/fg8-1, HEAD 8921656. Everything is STAGED, nothing committed.

## git diff --cached --stat
```
 32 plans/piles/*/README.md cards (incl. _template) | 2 +- each (1 line each)
 tools/piles.py                          | 87 +++++++++++++++++++++------------
 tools/test_piles.py                     | 13 +++++
 tools/test_piles_take.py                | 53 +++++++++++++++-----
 35 files changed, 143 insertions(+), 74 deletions(-)
```

## Items
1. F1 DONE. `_placement_known(ctx, finds)` (was `(tree, finds)`; caller `check_placement` passes `ctx`): the unknown-id red carries `(card_rel,) + _a9_homes(ctx, m.id)`. Row `xpile-unknown-id` in `test_check_scope_touched_piles` (forge card row 2 names `B-900 (часть)`, its finding lives in report-delivery, committed; control `run_check(--all)` exit 0; then `git rm` of that finding, staged alone; `check` must exit 2 naming `unknown id B-900 in the row of batch forge/2`). No other red gained carriers (existing scope rows green).
2. F2 DONE. New `_node_table_error(has_table, missing)` (the one text) and `_node_table_problem(f)` (reads `f.has_nodes_table` and the new `BatchFile.node_cols_missing` tuple, set by `_parse_nodes`, which now returns `(nodes, has_table, missing)`; `parse_batch` passes it). Used at both `status` sites (`_status_node_row`, `_status_batch_plan`); no code reads error wording any more. Rows in `test_status_edges`: `no-node-table-node`, `no-node-table-batch`, `no-status-column-node`, `no-status-column-batch`, `node-in-empty-table` (fixture: `BROKEN_TABLE` rewrites a TAKEN batch file's table; `status_world` kinds `no-table`, `no-status-column`, `empty-table`). These F2 rows pass on the old code too (the filter worked on the current wording): they are regression pins of the new structure, not red-first rows.
3. L2 DONE. In `_status_batch_plan`, for `принято`, AFTER the unreadable-table refusal and BEFORE the open-nodes rule:
   `forge/2 has no nodes to accept (its node table has no rows) -- expected at least one node row to judge; set the batch to сдано, or edit the header and the card row by hand and put "piles-skip: в -- <reason>" in the commit message ((в) masks the Статус cells)`
   (`forge/2` = `where`). Row `batch-accepted-empty-table`. RED before: run on the unfixed code it failed (exit was 0 vacuous pass), see witness.
   Note: a `batch-submitted-empty-table` row I tried (сдано on an empty table) was dropped: the written tree is a (д) red by existing rule (empty table of a taken batch), unrelated to this item.
4. F3 DONE. Rows in `STATUS_ROWS`: `node-id-40-chars` (refused only as "no node"), `node-id-cyrillic-exists` (accepted and written; world `cyrillic-id`), `node-id-cyrillic-unknown`, `task-6-digits` (t-999999 accepted), `hash-6-hex` (refused), `hash-40-hex` (full HEAD hash, accepted and written; placeholder `{H}`), `hash-40-hex-not-a-commit`, `hash-41-hex` (refused). 7 hex AT the limit is covered by existing `accepted-hash` (written) and `bad-hash-not-a-commit` (`deadbee`: passes the shape, refused as no commit). N=999: row `("forge","999","no batch row 999")` in `test_status_slug_and_n_battery`. The test body now compares the written node row with `args[0]` instead of the literal `F0-3`. `test_status_order_is_the_one_table` DELETED (comment left in place of it): covered by rows `backwards` (node сдано -> в работе), `accepted-then-rejected` (node принято final), `batch-backwards` (batch принято -> сдано), and `test_status_keeps_crlf_bom_and_passes_frozen` (every forward step, (в) green after each).
5. F5 PARTIAL. Done: `load_tree(root, tolerant, skip)` has no `with_untracked`; `run_check` calls `untracked_piles(root)` ONCE (after the "nothing to check" early return, so a non-pile commit still pays no git call; used for `skip` and for the `--all` note); `FROZEN` replaces the literal tuple in `_status_batch_plan` (and the same literal at the `_view_reds` empty-table line). NOT done: removal of `Tree.untracked`: `tools/piles_split.py:319` builds `piles.Tree(tree.root, tree.backlog, merged, [])` positionally, and that file is outside owns. The field now has a default (`untracked: list = field(default_factory=list)`, commented as dead) so nothing breaks. Fork for the Lead: one-line edit of piles_split.py:319 (drop the `[]`) and then delete the field.
6. F8 DONE. Row `take-no-warning-unreadable-dev-config` in `test_take_by_developer` (dev.config.yaml = `developer: [dev2\n  : {broken\n`): take exits 0, prints `piles take: forge/2 taken by dev1`, no `WARNING: --who`. Code and spec D agree (spec §3 SL-4 D.3 and edge list: «unreadable at take: no WARNING, take unchanged»); green with no code change (a pin, not red-first).
7. L1 STOPPED: three reasons.
   (a) A real taken batch changes reading. Read-only one-off (script `scratchpad/dev_probe.py`, vocab {dev1,dev2} = the tracked journal names, `piles.dev_of` before vs first-token rule after, over every batch header's «Взял» in this tree):
   `CHANGED 'Lead dev1 (Opus), 13.11.2026'  dev1 -> None  (2 batches, both «в работе»: onboarding-hooks/batch-6-ostatki-t-203-i-t-227.md, onboarding-hooks/batch-7-ostatki-t-263.md)`
   `CHANGED 'dev2, 30.10.2026 (прежде dev1, 28.10.2026)'  None -> dev2  (1 batch, закрыта: hotfix-12586/batch-7-dashboard-price.md; closed, not compared)`
   every other header reads the same (dev1/dev2 forms `dev1, DD.MM.YYYY`, `dev1 (Opus coord), ...`, `dev2, ...`, owner/Lead/— -> None). So onboarding-hooks/6 and /7 would stop being "same developer" as dev1's batches 4, 5, 8 of that pile.
   (b) The existing `test_dev_of` table (tools/test_piles_form.py:104-129, OUTSIDE owns) has rows the new rule flips: `lead-and-opus-are-not-slugs` (`Lead dev1 (Opus), 13.11.2026` -> dev1 today, None under first-token), and `dev1-parens` `(dev1)` needs a decision on leading punctuation.
   (c) The DoD runs test_piles_form.py green, so the code cannot change without that file.
   `dev_of` is UNCHANGED. Forks for the Lead: (1) first token only (the two live batches go to None and their header text must be edited to `dev1, 13.11.2026`, or accept); (2) is leading punctuation `(dev1)` / `` `dev1` `` skipped or None; (3) permission to edit test_piles_form.py rows.
8. L5 DONE. Script `scratchpad/cards_l5.py` (one regex-free byte replace of «называет `piles.py check` (е)» -> «называет `piles.py check --all` (е)», each file asserted to hold exactly one old text, bytes otherwise untouched): `changed 32 untouched 2` (32 includes `_template/README.md`; untouched: hotfix-12586, test-code-quality, no old text). `git diff --cached --stat`: 1 line per card.

## Refusal texts new or changed (verbatim)
- `<where>: no node table under '## Узлы' -- expected a table with the columns Узел / Исполнитель / Пишет в / Статус` (unchanged wording, now from `_node_table_error`; batch level appends ` -- its nodes are read to judge the acceptance`)
- `<where>: the node table has no Статус column -- expected Узел / Исполнитель / Пишет в / Статус` (same)
- NEW: `<where> has no nodes to accept (its node table has no rows) -- expected at least one node row to judge; set the batch to сдано, or edit the header and the card row by hand and put "piles-skip: в -- <reason>" in the commit message ((в) masks the Статус cells)`

## F1 probe
Before (verdict, piles.py@8921656): `COMMIT staging only the report-delivery delete: 0` / `(а) placement: 1 red(s) in piles this commit does not touch (not blocking): forge` / `piles check: ok`.
Before (row `xpile-unknown-id` on the unchanged carrier line, this round): `assert (0 == 2)`, output `(а) placement: 1 red(s) in piles this commit does not touch (not blocking): forge ... piles check: ok`.
After: the same row green (exit 2, `(а) placement: RED`, `unknown id B-900 in the row of batch forge/2`), in the 508-pass run below.

## Witness (verbatim)
RED run, piles.py with the F1 carrier and the L2 refusal temporarily disabled (byte copy of the fixed file taken before, sha256 54141ef3...16ea; restored from it, hash verified identical):
```
python -m pytest tools/test_piles.py tools/test_piles_take.py -q -p no:cacheprovider -k "xpile-unknown-id or empty-table or unreadable-dev-config"
FAILED tools/test_piles.py::test_check_scope_touched_piles[xpile-unknown-id]
FAILED tools/test_piles_take.py::test_status_edges[batch-accepted-empty-table]
FAILED tools/test_piles_take.py::test_status_edges[batch-submitted-empty-table]   (the row dropped afterwards, see item 3)
3 failed, 2 passed, 277 deselected in 7.26s
```
Final run, ONE run after the last edit, from the worktree via subshell:
```
( cd <wt> && python -m pytest tools/test_piles.py tools/test_piles_take.py tools/test_piles_form.py tools/test_pile_cards_contents.py -q -p no:cacheprovider )
508 passed in 220.19s (0:03:40)
```
(the staged state is exactly what ran; no edit after it.)
```
python tools/piles.py check --all   -> ... (е) findings: ok (1000 findings read ...) / piles check: ok
python tools/lint_ratchet.py --check -> lint ratchet: 36 findings, 36 in the baseline, 0 new, 0 stale (pyflakes 3.2.0)
python tools/dup_ratchet.py --check  -> dup ratchet: tools: 16 groups, 16 known, 0 new, 0 grown, 0 carried, 0 shrunk/gone (0 diverged)
git grep -n -E "with_untracked|\.untracked\b" -- tools/   -> no hits (rc 1)
git grep -n "untracked_piles" -- tools/piles.py          -> 942 (def), 2283 (run_check, once), 2514 (_writer_tree)   [positive control]
```

## ADDENDUM after the Lead's answers (supersedes items 5 and 7 above)
- Item 5 now COMPLETE: owns widened by `tools/piles_split.py`. `git grep -n "Tree(" -- tools/` found two constructions: `tools/piles.py:902` (`Tree(root, backlog, piles)`, already 3 args) and `tools/piles_split.py:319` (lost its `[]`). Field `Tree.untracked` and its "dead" comment deleted. No other reader of `.untracked` in tools/.
- Item 7 (L1) WITHDRAWN by the Lead: live «Взял» headers carry `Lead dev1 (...)`. `dev_of`, `test_dev_of` and tools/test_piles_form.py untouched.
- Final witness (one run after the last edit, staged tree, from the worktree via subshell):
```
python -m pytest tools/test_piles.py tools/test_piles_take.py tools/test_piles_form.py tools/test_pile_cards_contents.py tools/test_piles_split.py -q -p no:cacheprovider
556 passed in 217.75s (0:03:37)
python tools/piles.py check --all  (tail) -> piles check: ok
lint ratchet: 36 findings, 36 in the baseline, 0 new, 0 stale (pyflakes 3.2.0)
dup ratchet: tools: 16 groups, 16 known, 0 new, 0 grown, 0 carried, 0 shrunk/gone (0 diverged)
git grep -n -E "\.untracked\b|untracked=" -- tools/  -> no hit (rc 1); control: untracked_piles at piles.py:941, 2282, 2513
```
- Final commit message: the draft below with the sentence «Not done: ...» replaced as shown (L1 mention removed; piles_split.py touched).

## Siblings / analogs
- `grep startswith((` in tools/piles.py: 815 (`_is_pile_dir`), 1640 and 1651 (section names); none on `_parse_nodes` text; `take` and `close` have no prefix filter on node-table errors. Nothing to switch.
- `tools/piles_split.py:319` still builds `Tree(..., [])` positionally (blocks removing `Tree.untracked`).
- `_view_reds` (empty node table of a taken batch is a (д) red) is why an accepted-empty batch could never pass `check` afterwards: L2 now refuses it at `status`.
- `status` evidence rows exist for hashes but `take --who` limits (40/41 chars) are in `test_take_who_battery` already; no gap noticed.

=== MESSAGE BEGIN ===
piles: fix round after the topic critic (t-426)

F1 (blocking): the (а) unknown-id red carries the a9 homes of the id, so a commit that deletes the id's finding in another pile is judged (spec t-356 par. 4 B / B.3). F2: one `_node_table_problem(f)` over structured facts (`BatchFile.has_nodes_table`, `node_cols_missing`) replaces two prefix filters on parser wording in `status`. L2: batch-level `принято` on a batch with no node rows is refused, with a door. F3: rows AT and BEYOND the CLI limits of `status` (N=999, 40-char and Cyrillic node ids, t-999999, hashes of 6/40/41 hex); the constant-pin test of the order table is gone, behaviour rows cover it. F5: `load_tree` loses the dead `with_untracked` and `Tree` the dead `untracked` field (piles_split.py stops passing it); `run_check` reads `untracked_piles` once; `FROZEN` reused. F8: row for an unreadable tools/dev.config.yaml at `take`. L5: pile cards say `piles.py check --all` (е). L1 (narrowing `dev_of`) withdrawn by the Lead: live «Взял» headers carry `Lead dev1 (...)`.

axis 1 (Policy <-> role): n/a (no policy text).
axis 2 (Per-tier exam instruments): n/a.
axis 3 (Factory package <->): n/a (package untouched).
axis 4 (Factory rules <->): n/a.
axis 5 (Stage twins inside): n/a (package).
axis 6 (Measurement tools <->): covered (the load_tree callers backlog_tree, collect_intake, compact_snapshot, forge_metrics call it by keyword and do not pass with_untracked).
axis 7 (Per-test identity <->): n/a (package).
axis 8 (Where the story): n/a (package).
axis 9 (is this a): n/a.
axis 10 (git-top readers): n/a.
axis 11 (shell-command recognizers): n/a.
axis 12 (carriers of the): covered (one node-table reader in status; cards say check --all; one status order table, pinned by behaviour rows).
axis 13 (the dispatch text): n/a.
axis 14 (readers of agent): n/a.
axis 15 (console stream setup): n/a.
axis 16 (one JSON reader): n/a (package).
axis 17 (detector verdict shape): n/a (package).
axis 18 (in-tree shrink-only ratchets): covered (lint and dup ratchets 0 new).
axis 19 (one reader of): n/a (package).
axis 20 (host receipt names): n/a (package).
axis 21 (readers of the): covered (BatchFile gains a defaulted field; every reader goes through parse_batch).
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
axis 34 (One road for): covered (status stays the one writer of сдано/принято; the empty-table acceptance is refused, the hand edit stays the named door).
axis 35 (Sides of a): n/a (package).
axis 36 (The row written): n/a (package).

Four questions: (a) cost: none for users; one refusal more at `status` for an empty batch table, door named; (b) axes above; (c) detector: calibration check 33 (d) for the card/batch status drift, `piles.py check --all` and CI forge-check for the (а) carrier rule; (d) skip: the F1 carrier is on the execution path of check (а) (code gate), the status refusals are on the path of the only writer, the card wording on discipline alone with check 33 as the detector.

tier: <model>
=== MESSAGE END ===
