# t-421 — critic diff gate: piles slimming (SL-1, SL-4, SL-2, SL-3; SL-6 for consistency)

Reviewed: worktree `.claude/worktrees/fg8-1`, branch wip/fg8-1, head 8921656 (working tree clean, `git status --short` = 0 lines).
Merge base used: `git merge-base 92fda1a 8921656` = **2830b08** (main, PR #17). Line numbers below are `tools/piles.py` at 8921656
unless named otherwise. DoD = spec t-356 (§3 per node, §4 edges, §5 tests). Mechanical layer used: t-385-fg8-1-handover.md (SL-1),
t-400-sl-4-handover.md (SL-4), t-406 (SL-2), t-415 (SL-3), plus the Lead control re-runs quoted in the dispatch.

**Overall verdict: fit_with_fixes** (NEEDS WORK, one fresh builder round). One blocking finding (F1, SL-2); the rest are fixes or
Lead/queue items. Per node: SL-1 fit; SL-4 fit (one spec claim for the Lead, F4); SL-2 fit_with_fixes (F1 blocks the merge);
SL-3 fit_with_fixes (F2, F3); SL-6 fit (one wording item, L5). The verdict is an input to the Lead's acceptance, not the acceptance.

## Findings

**F1 (BLOCKS, SL-2, surface: the B.3 carrier rule of check (а)).** A commit in pile B can create an (а) red in pile A and pass.
`_placement_known` gives «unknown id X in the row of batch A/n» ONE carrier, A's card (piles.py:1137-1138). The red is created by
deleting X's finding in ANOTHER pile while A's card names X as a partial member (a partial cross-pile member is legal: `homes` counts
only whole members, 1099-1110). The commit touches only B, so `Ctx.touches` (1073) is false and the red is summarised. Spec §4 B
says the opposite: «(а) … unknown id …: the carriers are the paths involved. Creating one means editing one of them», and B.3 keeps
it unreachable. Probe on the mini tree (testkit `build_mini` + `freeze`; finding B-900 in report-delivery; forge card row 2
`B-015, B-900 (часть)`; then `git rm` of that finding; `run_check` from piles.py@8921656):
```
COMMIT staging only the report-delivery delete: 0
(а) placement: 1 red(s) in piles this commit does not touch (not blocking): forge
piles check: ok
ALL after: 2
(а) placement: RED -- unknown id B-900 in the row of batch forge/2 (the card) -- it is in no BACKLOG row, no closed row and no finding; ...
```
That deletion is the natural move to clear the (е) red of the same finding, so the path is realistic. CI `check --base` follows the
same rule and passes it too. Fix: give this red the a9 carriers, i.e. `(card,) + _a9_homes(ctx, id)` (1180). `git grep -l -w` at the
base rev finds the deleted finding path, which is staged. Neighbouring classes of the same surface, walked: dupes in two findings
(both paths), a whole member in 2 batches and homes in 2 piles (both piles' paths): carried. «closed but still placed» (1142): created
through BACKLOG, which (г) «closed outside close» (1786) carries. Name/header mismatch: own path. (б) pairs: both batch paths. (е):
homes without the `in tree.piles` filter. a9: F-3 lookup. So F1 is the one hole found in (а).

**F2 (fix, SL-3, edge 9).** Edge 9 has no test row, and the node-table error is recognised by `startswith(("no node table", "the node
table"))` on `_parse_nodes`'s text (614, 619). The filter is copied at 3248 and 3293. If that text is ever reworded, batch-level
`принято` on a batch with no node table passes vacuously: `f.nodes` is `[]`, so `open_ids` is empty (3294-3295). Deviation (6)
calls a fixture impossible. The code says otherwise: `load_pile` only APPENDS batch parse errors (849) and never raises, so a batch
file written «в работе» with no `## Узлы` table, or with a `Стат` column renamed, loads strictly. Fix: (a) one helper over a
structured fact (`BatchFile.has_nodes_table` already exists, used at 1908, plus a missing-columns flag) instead of two prefix
filters; (b) rows `no-node-table` and `no-status-column` at both levels in `test_status_edges`; (c) a row for deviation (7), an empty
node table at batch `принято`.

**F3 (fix, SL-3, CLI limits AT the edge; CLAUDE.md rule 11, a case AT and BEYOND each limit).** Present: N 0/1000/-1/x, node id 41
characters, task 7 digits, hash empty/non-hex/not-a-commit. Missing: N=999 (AT), node id of 40 characters (AT), `t-999999` (AT),
hash of 6 hex (below 7), 7 hex (AT), 40 hex (AT) and 41 hex (BEYOND). Also missing: a Cyrillic or other non-ASCII node id
(encoding). `test_status_order_is_the_one_table` (test_piles_take.py:473) pins constants: it cannot catch a second order table, which
is the risk it is named for. Drop it or turn it into a behaviour row.

**F4 (Lead, SL-4 spec claim).** Spec D.1 says `dev_of` «never yields a wrong slug from the text». The algorithm (exactly one
vocabulary slug) yields one for a non-slug taker who mentions a slug. Measured with `dev_of(w, {"dev1","dev2"})` on piles.py@8921656:
`'Ира (после dev1), 13.11.2026' -> dev1`, `'Ира, передано от dev1' -> dev1`. Also `'dev2 (за dev1)' -> None` and
`'dev1ира' -> None`. With only `logs/journal/dev1.jsonl` in the index today (`git ls-tree 8921656 logs/journal/`), a dev2 batch
reads None, which is safe. This is a third false-"same" source the spec does not name. Both people would have to be different and
only one a vocabulary slug. Lead: name it beside the two accepted risks (detector 33 (b″) already catches it), or narrow `dev_of`
(e.g. the slug must be the first token).

**F5 (fix, SL-1/SL-2 code quality).** `load_tree(with_untracked=…)` and `Tree.untracked` (792-796, 886) are dead code. The docstring
itself says no caller passes the flag, and no reader of `.untracked` exists (`git grep -n -E "with_untracked|\.untracked\b"`: only
the definition lines; positive control: `untracked_piles` found at 926, 2265, 2271, 2296, 2493). `run_check` calls
`untracked_piles(root)` up to three times per run (2265, 2271, 2296): compute it once.
`("в работе", "сдано", "принято")` at 3280 is `FROZEN` (1571): reuse it.

**F6 (queue item, pre-existing, the error direction of K2).** `tokens_overlap` (1294-1320) leaves a pair of DIFFERENT developers
green for these unresolvable writer tokens, measured with `tops=("scripts","references","changelog.d")`: `x.py ~ scripts/` False,
`**/x.py ~ scripts/` False, `scripts/{a,b}.py ~ scripts/a.py` False, `scripts/… ~ scripts/a.py` False. `_is_glob` (1237) knows only
`*`/`?`, and braces and `…` are expanded only by `parse_zone`. Only PACKAGE_ROOT takes the safe side for a bare basename or a glob
first segment (1305-1307). This is not introduced by this diff. Brace/ellipsis spans exist in batch files (`git grep -c` over
`plans/piles/*/batch-*.md`, e.g. codex/batch-1: 10). Proposed node: forge pile, owner Lead: one expansion for writer tokens
(reuse `_expand_braces`), and a bare basename or glob against a folder errs to TRUE.

## Keys

**K1 (SL-1).** Code and gates: no breaks. `board` is a refused alias (3341-3344, `REFUSED_ALIASES` 3423), the CI step is gone
(21ba7b7, forge-check.yml) and its pin is gone (test_workflows.py). `.githooks/pre-commit` and `pre-merge-commit` already had no
board line at the merge base: the pre-step commit 5d79f97 on main. The board-check lines were removed in that pre-step on main, not
in this diff. The live `core.hooksPath` is the root checkout `C:\QAFactory\forge-repo\.githooks` (L-1), where the same removal sits
uncommitted. `plans/PILES.md` is absent from 8921656 (`git ls-tree` empty). `.gitattributes`: no hit. Grep, case-insensitive,
`piles\.md|piles\.py board|piles board|board --check|BOARD_REL|rebuild_board|render_board`, whole tree minus specs, snapshots, logs
and the history files. The positive control found `.claude/settings.json:139`. Results:
- tools/: fixture/assert strings only (piles_testkit.py:127; test_piles.py:183,202; test_piles_frozen.py:33,59; test_piles_take.py:48,235).
- Followed commands that now exit 1: PROJECT.md:280 (`python tools/piles.py board`) and PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:983
  (check 33 (a) runs `board --check`).
- Stale text pointing at a deleted file: PROJECT.md:295,320,349 (+ AGENTS.md ×4, generated), PROCESS:978,1011, README.md:10,62,
  docs/SIBLING_MAP.md:294,296, plans/BACKLOG.md:7.
- All of these are owed by SL-5b (§6.1-6.4, §2.2), and the closed batches and findings are history per §2.2.
- `.claude/settings.json:139,158`: owner, not counted.
- The SL-1 axis 12 line says «covered (… settings …)», but settings were deliberately left: an overstated claim, not a defect.

**K2 (SL-4).** The slug is matched as a whole `[\w-]+` run, then `SLUG_RE.fullmatch` and vocabulary membership (1487-1495). The run
is wider than the spec's `[a-z0-9][a-z0-9-]*`, so a glued Cyrillic or `_` stays one token: `dev1ира`, `dev1_x`, `xdev1`, `dev12`
all read None (tested ids `dev1-cyrillic-glued`, `dev12-digit-glued`, `xdev1-letter-glued`). How each case behaves:
- Same developer: skipped in (б) (1550-1553) and in `take` (2480-2481). Different developers: compared, as before.
- No slug, `—`, empty: None, compared (rows `dash`, `empty`).
- The check never reads `dev.config`. `take` prints no WARNING when `developer_slug` is None. That is true for both a missing and an
  unreadable file; upper case also gives None (journal_keys.developer_slug docstring). The row covers only «missing», not
  «unreadable» (a small fix, F8).
- The vocabulary comes from the git index (1476-1483); a git failure gives an empty vocabulary, which reads «different» (row
  `git-fails-empty-vocab`).
- PACKAGE_ROOT: a bare basename and a glob first segment are on the safe side. Other unresolvable tokens are not: F6.
- D-0048 function lists still work: `fn_lists_of` drops only blank spans (1349-1356). Rows `fn-list-*` (SL-2) and the existing (б)
  list tests are green in the Lead's 228-run.
- Inputs where two DIFFERENT developers overlap silently: (1) two people under one slug, accepted; (2) `--who <another's slug>`,
  accepted, with the WARNING; (3) a non-slug taker naming one slug, F4; (4) the token forms of F6, pre-existing and independent of
  developers.

**K3 (SL-2).**
- Narrowed: (в) to taken batches of touched piles (1744-1745) and `_leftover_write_reds` (touched piles only). Every red's blocking
  goes through B.3 `touches` (1073-1078); untouched reds become one line per item (`_item_lines`, B.5).
- Unchanged in what is read (whole tree): (а), (б), (д), (е). Their blocking is scoped by carrier.
- Cross-pile hiding: (б) pairs carry both batch paths; (е) carries its homes and staged deleted batches; a9 uses the base-rev
  lookup; one hole: F1.
- CannotRun: an unresolvable `--base` was already CannotRun in `cmd_check` (2332-2336), before `range_paths` (907-913) runs. So
  `range_paths`' own CannotRun is reachable only if `git diff` fails on a resolved rev. Neither existed before.
- CI base cases. Zero sha or first push: the workflow uses `HEAD~1` (forge-check.yml:63-66). PR: `base.sha`. Canon: merge-base.
  Shallow: not possible, `fetch-depth: 0` (:45). Force push to main: the old `before` sha is not on any fetched ref, so
  `resolve_base` fails and the step exits 1. It did the same with `--all --base`, and the journal step (:71) fails first. No
  regression.
- `--all`: staged None, so touched None and everything blocks; it adds the untracked note (2295-2299).
- Strict reads confirmed. These are the queued analog (SL-2/SL-3 handovers), not demanded here: `close` 3115, `close --id` 3172,
  `tools/piles_split.py:663` (`load_tree(root)`, no skip). `summary` (3349) also reads foreign untracked files, but only as a reader.
- Minor: in range mode the «nothing to check» text still says «staged» (2257).

**K4 (SL-3).**
- One table: `STATUS_ORDER` over `NODE_STATUSES` (113). Writes go only into cells that (в) masks: header статус, card Статус, node
  Статус. Pinned by `test_status_keeps_crlf_bom_and_passes_frozen`: six writes, `check --all --base HEAD` green after each, then the
  staged `check`.
- Does `status` refuse a state that `take`/`close` produce? `take`'s «в работе» leads to сдано/принято. `close`'s закрыта is refused
  at both levels by design. `close` requires header «принято» (`_close_batch`), which `status` produces only after all nodes are
  done. That is stricter than `close`, and consistent.
- All-or-nothing: `apply_changes`, tested at batch and node level (`test_status_rollback_on_failed_write`).
- CRLF/BOM: tested.
- The 14 deviations:
  - (1) `--today` accepted and unused: fine; dropping it is optional.
  - (2) fine.
  - (3) fine: matches the reader `status_word`, which lower-cases (202).
  - (4) fine: the safe direction, no silent loss of evidence.
  - (5) fine: the same cell is already a (д) red (1836-1838).
  - (6) wrong: a fixture is feasible; F2.
  - (7) Lead decision: an empty node table accepting vacuously. Recommend refusing, since the edge-5 invariant is «header never says
    accepted while a node is open», and `_view_reds` already reds an empty table of a taken batch (1908-1909).
  - (8) fine.
  - (9) fine: `_writer_tree` (2489-2493) is one road for take and status.
  - (10) and (11) fine: an unknown id gets a listed refusal.
  - (12) fine.
  - (13) and (14) process notes, fine.
- Refusal texts (handover list) read as the receiver: each names the wrong value, the expected form and a door. The doors are a
  command, a hand edit masked by (в), or `piles-skip: в`. The closed-batch text has no door, by design: closed is history. These are
  developer-tool texts, never shown to the owner, so P9 does not apply.

**K5.** Status-cell writers:
- `take`: в работе. `status`: сдано, принято, node cells. `close`: закрыта.
- `piles_split.py:228` writes only the first «ожидает» row of a NEW card. That is creation, not a transition.
- `collect_intake.py:971,982` prints suggested rows; it writes no file.
- So there is one road per transition (P31). The hand edit stays as the named correction door.
Axis spot-checks:
- SL-2 axis 6 «covered»: verified. The `load_tree` callers backlog_tree.py:34, collect_intake.py:1112, compact_snapshot.py:375 and
  forge_metrics.py:600 are unchanged.
- SL-4 axis 12 «covered»: verified. The only external reader of `parse_zone`/`_norm_token` is collect_intake.py:846,877, pinned.
- SL-1 axis 12: overstated (settings), see K1.
- SL-3 axis 34: verified as above.
- Axes 6/12/13/34 are the only «covered» lines; the other lines are package n/a, which holds (no package file in the diff: the stat
  is tools/, .github/ only).

**K6 (tests).** All tables are parameterised and the ids name the case (`STATUS_ROWS` ids, `SCOPE_ROWS`, `test_dev_of` ids,
`test_take_by_developer`).
- Edge rows missing: §3 SL-3 edge 9, which is F2.
- Limit rows missing: the AT/BEYOND limits of F3.
- No rows: F1's scenario; a function-list carrier with the package prefix (`extra` at 1558-1559); `take` with an unreadable
  dev.config.
- A test that can only pass, or pins a constant: `test_status_order_is_the_one_table` (F3).

**K7.**
- (6) DUPLICATION AND CONSISTENCY:
  - the node-table filter copied (3248/3293);
  - the FROZEN literal (3280);
  - `untracked_piles` computed up to three times;
  - the «first N, +K more» formatting built inline three times (`_ids_text` 3209-3211, 3296, `_item_lines` B.5); queue item, not a
    blocker.
  - Grepped: `\+%d more` and `no node table|the node table` in piles.py; the ratchet output in t-415 shows `dup ratchet: … 0 new`.
- (7) CODE QUALITY:
  - Function lengths, measured with ast: no new or changed function over 60 lines (run_check 57, load_pile 52, cmd_take 47,
    cmd_status 32).
  - Dead code: `with_untracked`/`Tree.untracked` (F5).
  - A docstring that lies: none found.
- (10) architecture: none. These are forge tools; no file in `ai-packages/qa-factory/` is in the diff.
- (12) ONE ROAD:
  - The same-developer exception rests on the owner's verbatim word 13.11.2026 (spec §1, the quote in Russian). Its reading
    («session» = slug) is pending Q-O1. It is an exclusion that STAYS until the answer, named here like a ratchet raise. Owner: the
    Lead, through Q-O1.
  - Writer tree reads are two roads: `take`/`status` skip foreign untracked files, while `close`, `close --id` and `piles_split`
    stay strict. This is a residual of this class. Proposed node (forge pile, owner the Lead): `_writer_tree` for close, close --id
    and split. The spec text queues it; this review gives it a node.

**§6.1 against the code (SL-5b, not under review).** (5) «Проверка судит только кучки, которые коммит трогает» is narrower than the
code. A commit staging only a listed `.py` can be blocked (B.3, `_relevant` 2210-2218), and so can a BACKLOG-only commit (a9). Add
«и `.py`, названный в списке функций активной пачки». (6) «Пачки одного разработчика друг друга не держат» holds only when the taker
cell names a committed journal slug (`Ира`-style takers are still compared). (2), (3), (4): consistent with the code.

## K8 — fix list

(a) One fresh builder round (owns `tools/piles.py`, `tools/test_piles.py`, `tools/test_piles_take.py`):
1. F1. `_placement_known`: the unknown-id red carries `(card_rel,) + _a9_homes(ctx, id)`. `_placement_known` needs `ctx` (or the
   caller adds the carriers in `check_placement`, 1196-1201). Row `xpile-unknown-id` in `test_check_scope_touched_piles` (the probe
   above: the commit staging only the other pile's delete exits 2). Why: the spec §4 B invariant. Witness: that row plus the
   existing scope rows.
2. F2. One helper `_node_table_problem(f)` over `has_nodes_table` and a missing-columns flag set by `_parse_nodes`, used at both
   sites. Rows `no-node-table`, `no-status-column` (node and batch level) and `batch-accepted-empty-table` (per the Lead's answer to
   L2).
3. F3. Rows N=999, node id of 40 characters, `t-999999`, hashes of 6/7/40/41 hex, a non-ASCII node id; drop or reshape
   `test_status_order_is_the_one_table`.
4. F5. Remove `with_untracked` and `Tree.untracked`; compute `untracked_piles` once in `run_check`; use `FROZEN` at 3280.
5. F8. A row `take-no-warning-unreadable-dev-config` (a broken YAML) in `test_take_by_developer`.
Witness: `python -m pytest tools/test_piles.py tools/test_piles_take.py tools/test_piles_form.py -q`, plus
`python tools/piles.py check --all`.

(b) Lead decisions and queue:
- L1: F4. Name the third false-"same" source, or narrow `dev_of`.
- L2: deviation (7). An empty node table at batch `принято`: refuse (recommended) or accept.
- L3: F6 node (writer-token expansion and the error direction).
- L4: the writer-tree node (close, close --id, piles_split read like `take`).
- L5: SL-6 card text «называет `piles.py check` (е)». After SL-2 a commit names such a finding only in a touched pile; consider
  «`piles.py check --all` (е)», wording only.
- L6: the SL-5b texts of K1 (PROJECT.md:280 and PROCESS:983 are the two that fail when followed), and the §6.1 (5) wording above.
- L7: the SL-1 mechanical layer ended «3 failed, 672 passed», with a partial green re-run (347). The test_piles_close*,
  test_md_table, test_backlog_tree and test_compact_snapshot files had no post-integration run in the attached witnesses. The batch
  canon on CI must carry them.

## Trail

Read:
- the spec t-356 §1-§5 and §7 in full; §6.1-6.7 for the texts and axis blocks;
- critic-diff-brief.md items 5-12;
- the handovers t-385 (witness sections), t-400 (witness and Key), t-415 (whole);
- the commit messages of 21ba7b7, 4e4ed9f, 38a5ccf and 3e5d9fb, with their axis blocks;
- the diffs `git show` 21ba7b7 / 4e4ed9f / 38a5ccf / 3e5d9fb on tools/piles.py, .github and the tests;
- c16ec0d: the _template and forge cards, plus the added-line census;
- piles.py@8921656 at 200-215, 380-451, 605-622, 812-930, 1088-1200, 1237, 1294-1320, 1476-1567, 1571, 1826-1840, 2210-2340,
  2473-2542, 3105-3175, 3198-3345;
- forge-check.yml@8921656 lines 1-90; journal_keys.developer_slug; collect_intake.py 960-990; testkit 82-170;
  test_piles_take.py 280-480; the test_piles_form.py SL-4 diff.
Searches: the K1 grep with its positive control; the `load_tree(` callers; `with_untracked|.untracked|untracked_piles`; external
readers of `tokens_overlap|_norm_token|parse_zone|writers_of|fn_lists_of`; `Red(` carriers; status writers in collect_intake and
piles_split.
Runs:
- `dev_of` / `tokens_overlap` probe on piles.py@8921656: outputs quoted in F4 and F6.
- Cross-pile probe: output quoted in F1.
- Control re-run, in the worktree at 8921656: `python -m pytest tools/test_piles_form.py -q -p no:cacheprovider -k "dev_of or pair_by_developer or token_overlap"`
  gave `45 passed, 47 deselected in 12.53s`.
Not run: the full tools/ suite (CI only).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F1 SL-2: piles.py:1137-1138 the (а) unknown-id red is carried only by the naming card; deleting the id's finding in another pile creates it and the commit passes (probe: exit 0, ALL after: 2) -- contradicts spec t-356 par. 4 B / B.3"
  ],
  "fixes": [
    "F1: _placement_known unknown-id red carries (card_rel,) + _a9_homes(ctx, id); row xpile-unknown-id in test_check_scope_touched_piles",
    "F2: one structured node-table problem helper (has_nodes_table + missing-columns flag) replacing the startswith filters at piles.py:3248 and 3293; rows no-node-table / no-status-column at node and batch level",
    "F3: AT/BEYOND rows for N=999, 40-char node id, t-999999, hash 6/7/40/41 hex, non-ASCII node id; drop or reshape test_status_order_is_the_one_table",
    "F5: remove dead load_tree(with_untracked) and Tree.untracked; compute untracked_piles once in run_check; reuse FROZEN at piles.py:3280",
    "F8: row take-no-warning-unreadable-dev-config in test_take_by_developer"
  ],
  "class_completeness": "Surface (а) carriers walked: dupes, whole-member, homes, closed-but-placed, name/header, a9, (б) pairs, (е) homes -- one hole (F1). Status-cell writers take/status/close one road per word; piles_split and collect_intake create or print only. SIBLING_MAP axes 6/12/13/34 spot-checked: 6 and 12 hold for SL-2/SL-4, SL-1 axis 12 overstates settings. Residuals proposed as nodes for the Lead: writer-token expansion and error direction (F6), close/close --id/piles_split strict tree read vs _writer_tree, third false-same source of dev_of (F4).",
  "trail": {
    "read": [
      "docs/tasks/specs/t-356-piles-slimming-spec.md",
      "docs/tasks/critic-diff-brief.md",
      "docs/tasks/specs/reports/t-385-fg8-1-handover.md",
      "docs/tasks/specs/reports/t-400-sl-4-handover.md",
      "docs/tasks/specs/reports/t-415-sl-3-handover.md",
      "git show 21ba7b7 4e4ed9f 38a5ccf 3e5d9fb c16ec0d (tools, .github, cards)",
      "tools/piles.py at 8921656 (ranges listed in the Trail section)",
      ".github/workflows/forge-check.yml at 8921656",
      "tools/journal_keys.py developer_slug",
      "tools/collect_intake.py 960-990",
      "tools/piles_testkit.py 82-170",
      "tools/test_piles_take.py 280-480",
      "tools/test_piles_form.py SL-4 diff"
    ],
    "reruns": [
      {
        "command": "python -m pytest tools/test_piles_form.py -q -p no:cacheprovider -k \"dev_of or pair_by_developer or token_overlap\" (worktree fg8-1 at 8921656)",
        "result": "45 passed, 47 deselected in 12.53s"
      },
      {
        "command": "cross-pile probe on the testkit mini tree with piles.py@8921656: partial member B-900 in forge card, git rm of its finding in report-delivery, run_check commit vs --all",
        "result": "COMMIT: 0, (а) 1 red(s) in piles this commit does not touch (not blocking): forge; ALL after: 2, unknown id B-900 in the row of batch forge/2"
      },
      {
        "command": "dev_of / tokens_overlap probe on piles.py@8921656",
        "result": "'Ира (после dev1), 13.11.2026' -> dev1; 'dev1ира' -> None; 'x.py' ~ 'scripts/' False; '**/x.py' ~ 'scripts/' False; 'scripts/{a,b}.py' ~ 'scripts/a.py' False"
      }
    ]
  }
}
```
