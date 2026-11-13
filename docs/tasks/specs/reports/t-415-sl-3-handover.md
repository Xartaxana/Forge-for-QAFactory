# t-415 SL-3 (C) handover: `piles.py status`

State: change STAGED in C:\QAFactory\forge-repo\.claude\worktrees\fg8-1 (branch wip/fg8-1, on 38a5ccf), NOT committed.

## git diff --cached --stat
```
 tools/piles.py           | 183 ++++++++++++++++++++++++++++++++++++++++---
 tools/test_piles_take.py | 200 ++++++++++++++++++++++++++++++++++++++++++++++-
 2 files changed, 373 insertions(+), 10 deletions(-)
```

## Witness (verbatim)
```
( cd <wt> && python -m pytest tools/test_piles_take.py tools/test_piles.py tools/test_piles_frozen.py -q )   (ONE run after the last piles.py edit; the last test edit, 3 lines in test_status_keeps_crlf_bom_and_passes_frozen, was re-run alone)
298 passed in 245.42s (0:04:05)
( cd <wt> && python -m pytest tools/test_piles_take.py -q -k crlf_bom_and_passes_frozen )   -> 1 passed, 109 deselected in 13.65s
( cd <wt> && python -m pytest tools/test_piles_take.py -q -k status )                          -> 65 passed, 45 deselected in 76.54s   (before the 3-line edit)
python tools/piles.py check --all      -> ... (е) findings: ok (1000 findings read, ...)  piles check: ok
python tools/lint_ratchet.py --check   -> lint ratchet: 36 findings, 36 in the baseline, 0 new, 0 stale (pyflakes 3.2.0)
python tools/dup_ratchet.py --check    -> dup ratchet: tools: 16 groups, 16 known, 0 new, 0 grown, 0 carried, 0 shrunk/gone (0 diverged)
python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for tools/piles.py
   no scenario or keep row covers tools/piles.py: run the whole scenario layer
   tools/piles.py: test_scenario_cart_1.py / test_scenario_local_1_0108.py / test_scenario_local_1_arm_b.py / test_scenario_walk.py / test_scenario_world.py
```
The five package scenario files are named by the walk for a forge tool; they do not cover piles.py (the walk says so); NOT run (as the dispatch said).
test_piles.py + test_piles_frozen.py + test_piles_take.py = the 298 (the dispatch DoD names `test_piles_take.py test_piles.py test_piles_frozen.py`).

## Per spec item: function -- test row
1. unknown slug / N / node id: `_find_view`, `_parse_n`, `_status_node_row` (ids list first 10, `+K more`, `_ids_text`) -- `unknown-node`, `test_status_slug_and_n_battery` (10 rows).
2. two ids in a Узел cell / two rows one id: `_status_node_row`, `_node_ids_of` -- `two-ids-row`, `duplicate-id-rows`.
3. backwards / final / same again: `_status_node_cell`, `_status_batch_plan`, `STATUS_ORDER` over `NODE_STATUSES` -- `backwards`, `accepted-then-rejected`, `same-again`, `accepted-other-hash`, `accepted-same-again`, `batch-backwards`, `batch-accepted-again`, `batch-submitted-again`.
4. node принято without evidence: `_status_evidence` -- `accepted-no-evidence` (+ `accepted-hash`, `accepted-task`, `accepted-both`, bad-hash x3, bad-task x4).
5. batch принято with open nodes: `_status_batch_plan` -- `batch-accepted-open-node`, `batch-accepted-open-after-submit`, `batch-accepted-all-done`, `batch-submitted`.
6. batch not taken / node level allowed: `_status_batch_plan` first check -- `batch-untaken`, `node-in-untaken-batch`, `node-in-work`.
7. batch «закрыта»: `cmd_status` -- `closed-batch`, `closed-batch-node`.
8. card and header disagree: `_status_batch_plan` (take's text) -- `card-disagrees`.
9. no node table / Статус column: `_status_node_row`, `_status_batch_plan` (`f.errors` of `_parse_nodes`, text quoted) -- NO test row (see Deviations 6).
10. renamed / two files one N: `_find_view` by N, `_batch_file` -- `test_status_refuses_unreadable_before_any_write[two-files-one-n]`.
11. missing card README: `_find_view` -- `...[missing-card]`; unclosed fence (SL-1 rule): `refuse_unreadable_prose` -- `...[unclosed-fence]`.
Plus: `test_status_keeps_crlf_bom_and_passes_frozen` (CRLF+BOM kept; after each of 6 writes `check --all --base HEAD` has "(в) frozen: ok", and after staging exactly the two files `check` (no --all) ends "(в) frozen: ok ... piles check: ok"), `test_status_rollback_on_failed_write[batch|node]`, `test_status_order_is_the_one_table`. Adversarial rows: word other case / extra spaces (`word-in-another-case`, `word-with-extra-spaces`), unknown/empty/waiting words, node ids with `|`, newline, empty, space, 41 chars; evidence with a non-принято word or at batch level.
Invariant "one line changed per target": `changed_lines` in `test_status_edges` for every row (node: batch file 1 line, card 0; batch: 1 + 1; refusal / no-op: 0 and `tree_state` equal).

## Every refusal and printed text added (verbatim; `piles status: ` prefix is added by main; exit 2 unless marked)
- `node id "<id>": expected 1-40 characters without spaces, "|", a backtick (`) or a line break, e.g. F6-13`
- `--set "<w>": expected one of в работе, сдано, принято, отклонено for a node`
- `--set "<w>": expected сдано or принято for a batch[ (`в работе` is written by `take`)| (`закрыта` is written by `close`)]; to set one node give its id: status <slug> <N> <node-id> --set <word>`
- `--hash and --task go with a node set to принято (`принято: <hash> (t-NNN)`); "<word>" is written as the bare word`
- `--task "<t>": expected a task id t-NNN (1-6 digits)`
- (check_hash, existing) `--hash "<h>": expected a commit hash (7-40 hex characters)` / `<h> is not a commit in this repository -- fetch first or check the hash`
- `a node is accepted with its evidence: expected --hash <merge commit> and/or --task t-NNN`
- `<slug>/<N> is "закрыта" -- a closed batch keeps its statuses; nothing was changed`
- `<where>: <_parse_nodes text>` (batch-level принято adds ` -- its nodes are read to judge the acceptance`)
- `no node "<id>" in <where> -- expected one of its node ids: <first 10, +K more | none (the table has no rows)>`
- `the id <id> heads <k> rows of <where> (lines a, b) -- one row, one id; split the row in an untaken batch, or write the cell by hand (the cell is masked by (в))`
- `the row "<cell>" of <where> names more than one id -- one row, one id; split the row in an untaken batch, or write the cell by hand (the cell is masked by (в))`
- `the Статус cell of <where> <id> is "<cell>", which starts with no known status word -- edit the cell by hand (a taken batch allows it: (в) masks every Статус cell)`
- `<where> <id> already accepted with "<cell>" -- a node in принято or отклонено writes nothing any more; to change it, edit the cell by hand (...)` and `<where> <id> is "<cell>" and final -- (same tail)`
- `the Статус cell of <where> <id> is "<cell>" -- a status only goes forward (в работе → сдано → принято), so it cannot be set back to "<w>"; to correct a mistake, edit the cell by hand (...)`
- batch: `<where> is "<status>" -- take it first (`take <slug> <N> --who <name>`); a waiting batch has no status to set`
- batch: `the card and the batch file disagree on <where>: card status "<a>", batch status "<b>" -- make them say the same thing, then set the status`
- batch: `<where> is "<s>" -- a status only goes forward (в работе → сдано → принято → закрыта), so it cannot be set back to "<w>"; to correct a mistake edit the header and the card row by hand and put "piles-skip: в -- <reason>" in the commit message ((в) refuses a status that moved back)`
- batch: `<where> cannot be accepted while its node(s) <ids, first 10 +K more> are neither принято nor отклонено -- set them first (`status <slug> <N> <node-id> --set принято --hash <h>`), or set the batch to сдано`
- no-op (exit 0): `piles status: <slug>/<N>[ <id>] is already <word>; nothing changed`
- done (exit 0): `piles status: <slug>/<N>[ <id>] set to <cell>. Next:` then `  git add <files>; git commit -m "piles: status <slug>/<N>[ <id>] <word>"` (node: the batch file; batch: card + batch file)

## Dry demonstration on a COPY (not the worktree's plans/)
`git clone --shared <wt> <scratchpad>/demo` (checkout of the index failed half-way on this machine, so I ran `git reset -q` in the copy; plans/ of HEAD 38a5ccf is complete on disk), then:
```
python -B <wt>/tools/piles.py --repo <demo> status onboarding-forge 2 F6-13 --set принято --hash 38a5ccf --task t-000     (abc1234 is not a commit: check_hash would refuse it; 38a5ccf is the copy's HEAD)
piles status: onboarding-forge/2 F6-13 set to принято: 38a5ccf (t-000). Next:
  git add plans/piles/onboarding-forge/batch-2-onboarding-roles-forge-p3.md; git commit -m "piles: status onboarding-forge/2 F6-13 принято"
exit 0
git diff --stat -- plans/ :  plans/piles/onboarding-forge/batch-2-onboarding-roles-forge-p3.md | 2 +-   (1 insertion, 1 deletion)
@@ -72  | F6-13 | П3 | Остатки F5-4 (...) | builder | `tools/piles.py`, `tools/test_piles_take.py` | forge/5 F5-4 | ожидает |     (the line, middle cells elided here)
       | F6-13 | П3 | Остатки F5-4 (...) | builder | `tools/piles.py`, `tools/test_piles_take.py` | forge/5 F5-4 | принято: 38a5ccf (t-000) |
```
(only the last cell differs; the card row is NOT touched at node level, by the spec; the card file has no diff.)

## Freeze question, answered by a run
`test_status_keeps_crlf_bom_and_passes_frozen`: take, CRLF+BOM, commit, origin/main := HEAD; six `status` writes (node в работе, сдано, принято --hash --task, a second node отклонено, batch сдано, batch принято); after each `check --all --base HEAD` exit 0 and "(в) frozen: ok" in the output; then `git add` of exactly the two files and `check` (staged scope): exit 0, "(в) frozen: ok" in out and the output ends `piles check: ok` -- passed (1 passed in 13.65s). The test asserts those strings; I did not print the full output.

## Deviations, small choices (none changes a spec row)
1. `--today` is accepted (hidden) and unused: the spec says "hidden, as in take", but no date is written into any cell.
2. `STATUS_ORDER` is now built over `NODE_STATUSES` (spec edge 3); the three batch uses (compare_batch, _compare_card, the card-vs-file check) are unchanged; pinned by `test_status_order_is_the_one_table`.
3. Word is read case- and space-insensitively (`" ".join(raw.split()).lower()`) and written canonical (spec silent on "another case").
4. `--hash` / `--task` with any word other than a node `принято`, or at batch level: Refused (spec silent; the alternative is silent loss of evidence).
5. A node cell that reads as no known word ("—", empty): Refused with the hand-edit door (spec silent: the direction cannot be judged).
6. Edge 9 has NO test row: no way to build a batch whose node table is missing/without Статус in the mini fixture without also failing `take`/load; the code reuses `f.errors` of `_parse_nodes` (texts starting "no node table" / "the node table"). Say if you want a row.
7. Batch-level принято also refuses when the node table is unreadable (nodes are read to judge the acceptance); an empty node table passes vacuously.
8. Batch-level order: not taken -> card/header disagreement -> backwards -> same word (no-op) -> open-nodes rule. Node level has no card check.
9. `take`'s tree load moved into `_writer_tree(root, slug)` (B.9 skip of foreign untracked piles), used by `take` and `status`; take's behaviour unchanged (take tests green). It is the only edit of `cmd_take` and the only change outside the owns' function list besides the module docstring.
10. A node id has no id-shape regex: `_text_arg_ok` (1-40, no `|`, backtick, control char) and no white space; anything else unknown -> "no node".
11. Row matching: a node matches when the id is among the `,` `+` `/` whitespace tokens of its Узел cell (backticks and `*` stripped); case-sensitive.
12. Docstring: the usage lines added and the sentence "сдано/принято are written by hand (queued...)" rewritten (it became false).
13. The test file's 3 new `commit`/`fetch_origin`/`head_hash`/`PROOF_DONE`/`node as mk_node` imports come from piles_testkit (not edited).
14. Two earlier shell attempts were refused by the hook (a `cd /dev/null` and a heredoc append into a git-tree file); nothing ran; the test text went in through Edit.

## Questions to the Lead
None blocking. Row-conflict check: no spec row conflicts with SL-1/2/4 code found.

## Siblings
- `take`, `close`: the same cells go through the same helpers (`edit_card`, `edit_header`, `apply_changes`, `_find_view`, `_batch_file`, `check_hash`); `status` has no second copy of that logic (verdict: shared). The only new per-cell helper is `set_node_cell` (no existing writer wrote a node cell).
- Other writers of status cells by hand: grep of `edit_header|edit_card|replace_pairs|replace_cells` in tools/ outside piles.py and tests: none. `piles_split.py` and `collect_intake.py` write files (`write_*` hits) but no status cell of a batch/card (piles_split names status "ожидает" only for a new card's first row) -- listed, not edited.
- Analog noticed, not fixed: `close` and `close --id` still call `load_tree(root)` strict (foreign untracked broken files block them), `take` and `status` skip them (already queued by SL-2's handover).
- Analog: `_status_node_row`'s node-table error filter (`startswith(("no node table", "the node table"))`) depends on the text of `_parse_nodes`; a structured error would be safer (not changed).

## Draft commit message
```
piles: status -- the one writer of сдано / принято, batch and node level (SL-3, t-415)

`piles.py status <slug> <N> --set <сдано|принято>` writes the batch header and the card row; `status <slug> <N> <node-id> --set <в работе|сдано|принято|отклонено> [--hash h] [--task t-NNN]` writes one node row's Статус cell (`принято: <hash> (t-NNN)`). Goes forward only (`STATUS_ORDER`, the one table, now over NODE_STATUSES; `принято` and `отклонено` final), refuses before any write (unreadable prose, missing card, two files with one N, unknown / duplicate / multi-id node, not taken, closed, card and header disagreeing, open nodes at batch принято, no evidence at node принято), writes through `apply_changes` (all or nothing, CRLF/BOM kept) and only cells that (в) masks, so a taken batch stays green. `take` and `status` share `_writer_tree`. Replaces the hand edit of F6-13 (onboarding-forge/2).

axis 1 (Policy <-> role): n/a (PROJECT.md item 7 names `status` in SL-5b).
axis 2 (Per-tier exam instruments): n/a.
axis 3 (Factory package <->): n/a (package).
axis 4 (Factory rules <->): n/a.
axis 5 (Stage twins inside): n/a (package).
axis 6 (Measurement tools <->): n/a (no measurer reads node cells differently).
axis 7 (Per-test identity <->): n/a (package).
axis 8 (Where the story): n/a (package).
axis 9 (is this a): n/a.
axis 10 (git-top readers): n/a.
axis 11 (shell-command recognizers): n/a.
axis 12 (carriers of the): covered (one writer per status word; `STATUS_ORDER` the one order table; SIBLING_MAP row 296 in SL-5b).
axis 13 (the dispatch text): n/a.
axis 14 (readers of agent): n/a.
axis 15 (console stream setup): n/a.
axis 16 (one JSON reader): n/a (package).
axis 17 (detector verdict shape): n/a (package).
axis 18 (in-tree shrink-only ratchets): n/a.
axis 19 (one reader of): n/a (package).
axis 20 (host receipt names): n/a (package).
axis 21 (readers of the): covered (cells written through the existing table writer `write_like`/`apply_changes`; read back by `md_table`).
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
axis 34 (One road for): covered (`take`, `status`, `close` are the one code road per status word; a hand edit stays the named door).
axis 35 (Sides of a): n/a (package).
axis 36 (The row written): n/a (package).

Four questions: (a) cost: one command replaces a hand edit; (b) axes above; (c) detector: calibration check 33 (d) «card row Статус ahead of its batch file»; (d) skip: on discipline alone for the hand edit (masked by (в)), with 33 (d) as the leak detector.

tier: <model>

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
```

## Needed beyond the manifest
tools/piles_testkit.py and tools/conftest.py (fixtures; not edited), tools/md_table.py (not read in full), docs/tasks/specs/t-356-piles-slimming-spec.md §6.7 SL-3 block (the draft's values), the real batch 2 of onboarding-forge (via the copy).
