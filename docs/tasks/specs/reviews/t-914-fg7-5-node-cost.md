# t-914 -- critic on builder t-905 (FG7-5, `forge_metrics --node-cost`)

Reviewed: worktree `.claude/worktrees/agent-add9d41f9d6897482`, commit 92781363 (`git diff main...HEAD`: forge_metrics.py +352, test_forge_metrics.py +283, handoff +66).
Spec/DoD: `docs/tasks/specs/20261116-fg7-5-node-cost-with-rework-spec.md` (§2-§5 + Lead fork decisions). No money figure appears in this file (P18): costs are "match / differs".

## Verdict: ACCEPT WITH FIXES -- 1 fix blocks the merge (B1), 6 fixes before merge (F1-F6)

The empirical layer holds. For three hand-picked rows, tokens are equal to the token and cost is equal to 1e-6, computed by an independent route: raw JSON reading of the journal and `usage_report.iter_assistant_turns` deduped by `dedupe_key`, not `request_parts` directly. I-3 holds on the live run, and so does I-1, byte for byte. Refusals and lazy imports behave as specified. B1 is a real money-direction defect (FR-41): a silent `$0.00` row. It is small and is fixed in this round.

## Control-value table (live journal of the worktree, `--window 2026-11-13`)

| task / row | field | expected (independent probe) | printed | match |
|---|---|---|---|---|
| t-505 (`t-505@dev1`) | dispatches | 4 (lines 1241, 1268, 1284, 1302) | 4 | yes |
| t-505 | tokens | 20335530 | 20335530 | yes |
| t-505 | cost | probe sum | row cost | matches (diff < 1e-6) |
| t-505 | rejects | spec 2 | 2 (spec 2) | yes |
| t-505 | critic / redelegations / replaced / escalations | 1 / 2 / 0 / 1 | 1 / 2 (replaced 0) / 1 | yes |
| t-505 | status, unmeasured | accepted, 0 | accepted, 0 | yes |
| t-615 row (retry + rejects; t-626 attached by `critic:t-626` on the accepted line 1573) | tasks | t-615, t-626 | t-615@dev1, t-626@dev1 | yes |
| t-615 row | dispatches / tokens | 4 / 29470336 | 4 / 29470336 | yes |
| t-615 row | cost | probe sum | row cost | matches |
| t-615 row | rejects / critic / redel / esc | capability 1 + spec 1 / 1 / 2 / 1 | 2 (spec 1, capability 1) / 1 / 2 / 1 | yes |
| t-449 (critic cited by t-438 RC2-1, t-441 PK2-14, t-457 OF3-2) | bucket | SHARED, cited by 3 rows | shared, cited_by OF3-2, PK2-14, RC2-1 | yes |
| t-449 | dispatches / tokens / cost | 1 / 4084765 / probe | 1 / 4084765 / shared cost | yes / yes / matches |

I-3 (P18): the row tokens summed from the printed table come to 4100371373. Adding shared 137083434 gives 4237454807, which is the printed total, so they are equal. Costs: printed rows plus the shared line minus the printed total equals 0.00 (rounding only). In the JSON, rows plus shared equals the total exactly. Dispatches: the printed rows hold 732, shared 20, total 752. I counted 752 independently (raw `delegated` lines of the listed tasks). No task sits in two places. 0 in-window `delegated` lines are left uncounted.

Unknowns (FR-41/FR-59). I passed a copy of the price file with every opus model removed through `node_costs(prices=)`, the only door the code has. t-505 became `>= $<x>` with lines 1284 and 1302 listed as `unpriced:claude-opus-5-5`. The total became `total >= $<x>`, with 241 unmeasured. 138 rows that have only opus dispatches print `n/d`, never `$0.00`. On the live run, 9 `no_transcript` dispatches and 1 `bad_ref cli:` are listed and the total says `>=`. These paths are correct; B1 is the one hole.

## Blocking

**B1 -- `tools/forge_metrics.py:1028-1030, 1059` -- `same_worker` can print a silent `$0.00`, and the spec's note is missing.**
- Defect 1: `seen[aid] = True` (line 1059) is set once the transcript has been read, even when no part was priced (`priced` False).
- Defect 2: the later line then returns `{"cost": 0.0, "whys": []}`. That means "measured, zero", with no note, so nothing tells the reader where the cost went.
- Repro (scratch, test helpers): t-001 has `agent:a6` and every part's model is `m-x`, which is unpriced. t-002 (node FG7-9) has `agent:a6` again. Result: row `forge/7/FG7-9` gets cost 0.0, partial False, and prints `$0.00`, while t-001 prints `n/d`. This breaks E3/E7 ("no row prints $0.00 for nothing measured", FR-41) and the spec's error direction.
- Even when the first line was priced, §2.4 requires the note "priced on line N". Nothing reads the returned `"same_worker": True` key, so it is dead data.
- This happens on the live journal: 13 agent ids sit on two `delegated` lines. In the window, `agent:ac4577455825daa31` is on t-310 (row OF4-10) and t-315 (row OF4-21). Row OF4-21 therefore holds a zero dispatch with no note.
- The builder's handoff says `same_worker` "is recorded only after the first line of that agent id was actually priced". The code does not match that claim.
- Fix:
  - Keep `seen[aid] = (line, priced)`.
  - When the first line priced nothing, the later line repeats the first line's `whys`, so it stays unmeasured.
  - When it was priced, the later line carries `same_worker` with the first line's number, and that note shows in the row: either in the "not measured" list as `same_worker (priced on line N)`, or in a separate `priced elsewhere:` list. Pick one form and state it in the commit.
  - Add one T1 row `same_worker_first_unpriced` (row prints `n/d` or `>=`, never `$0.00`). Extend the `same_worker_twice` row to check the note.

## Fixes before merge (same node, this round)

- **F1 -- `forge_metrics.py:1099-1101, 1169-1171` -- E15 ignores `defect_found`.**
  - The problem: a `defect_found` line goes into `defects` and never into its ref row's events, so `in_window` does not see it.
  - Repro: t-001 was accepted on 2026-10-01. A `defect_found ref t-001` on 2026-11-10 has no fix dispatch. Result: `rows: []`.
  - Why it matters: §2.3 makes the defect a fact of the row, and E15 says a row is in the report when any of its events is in the window. A late defect is exactly what the calibration needs to see.
  - Fix: count the defect line's `ts` into the window test of its ref's row. Add one T1 row.
- **F2 -- `forge_metrics.py:1063-1259` -- `node_costs` is 197 lines, with closures and four or more nesting levels.**
  - Where: the rows loop at 1206-1229, which nests `for k` / `for ev` / `elif delegated` / `if nc > 1` / `if extract`.
  - Fix: split it into `_nc_tasks` (load, nodes, outcomes), `_nc_links` (tokens, defects, `rows_of`), `_nc_row` (counts for one row) and the pricing pass. The behaviour stays the same, and the existing table judges it.
- **F3 -- `forge_metrics.py:1036` -- `counts={}` is discarded.**
  - What is lost: `split_missing` (a cache write priced at the 5-minute rate when the 1-hour split is unknown) and `bad_iterations` are sources of a LOW figure. §2.4 requires every such source to be NAMED. Today they are dropped without a word.
  - Measured on the live window: 30866 parts, 0 with a cache write and no 1-hour split, empty counts. So the defect is latent, not live.
  - Fix: pass a dict and turn a non-zero `split_missing` or `bad_iterations` into a `why` (the dispatch becomes partial).
- **F4 -- `forge_metrics.py:1039-1040` -- a dead branch.**
  - `request_parts` with a `skipped` list never raises ValueError or TypeError (its docstring, `transcripts.py:472-476`), so this `except` cannot run.
  - Fix: remove it (or keep it with a comment naming the case it guards; there is none today).
- **F5 -- `forge_metrics.py:1026` and `:1181-1182` -- two copies of "agent id of a worker_ref" inside the diff.**
  - Fix: one `_agent_id(obj)` helper used by both, built on `transcripts.agent_file_name` as §2.1 prescribes.
- **F6 -- `forge_metrics.py:1277` -- the header names the price file wrongly when prices are passed in.**
  - The header hard-codes `tools/model_prices.json`, but `node_costs(prices=...)` can price from another table (the tests do, and so did my probe). The output then names a file it did not read.
  - Fix: carry the source of the table in the dict, `prices_file` (the default path, or "given"), and print that.

## The builder's divergences and interpretations

- **Row `t-505@dev1`**: the code is correct (spec §8: `display`). This is a spec defect in §3.4 and §3.3's examples, for the Lead to correct in the spec text. Not code.
- **`--window 2026-13-99` is accepted**: the spec premise was wrong. `_normalize_window` checks only the shape. The builder's substitute, `yesterday`, tests the real refusal, and not changing `_normalize_window` keeps I-1. This is a spec defect (T3 row). A range check would be a separate node, since it would change the existing modes.
- **No CLI flag for a broken price file**: correct. The spec named none, and monkeypatching `PRICES_FILE` reaches the same `load_prices` door.
- **"(only for a task with NO own node)"**: read correctly. Step 2 gives the own node precedence, so it means the attached task.
- **`same_worker`**: the claimed behaviour is not the code's. This is B1.
- **`unlinked`**: the definition is acceptable ("kind task, one task, no shared citation"). One edge is negligible: a single-task row whose accepted line names a critic that has its own node counts as unlinked although it carries a token. No fix.
- **`n/d` total**: safer than the spec schema's `0.0` and consistent with FR-41. The spec should be changed to say this (Lead).
- **Defect alone makes no row, "not measured" ordered by (file, line), extra `shared` keys**: all consistent with the spec, and additive.

## The 377 unlinked rows (question 6)

Not a code defect, and not a grouping-rule defect. The rule does what §2.2 says: prose is never parsed. The cause is the journal's conventions:

- `delegated` lines carrying a `node` field, by day (root journal): 2026-11-12: 114/227; 11-13: 201/474; **11-14: 2/235**; 11-16: 7/22; 11-17: 11/20. The node field almost vanished on 11-14.
- Unlinked rows by day of their first event: 11-13: 181/300; 11-14: 173/201; 11-16: 14/21; 11-17: 5/6.
- Share of the window's tokens: unlinked rows hold 0.571. Unlinked builder rows alone hold 0.304 (204 rows), unlinked critic rows 0.090 (50 rows). The other unlinked rows are designers (69) and scouts (54), which by nature often belong to no node.

Usable? Yes, for its purpose, with this reading. The top 5 (accepted rows) is real, and an expensive unlinked task still ranks under its own id. But a node's cost is a LOWER bound while about 30% of builder spend sits outside the node rows.

The one change that would raise the linked share most: make the `node` field present on every pile-node `delegated` line. That is the dispatch header's `node:` line, which `tools/journal_hooks.py:243` already copies when present: make it obligatory for a dispatch carrying a `task:` of pile work (`dispatch_new.py` / `dispatch_manifest.py`). This belongs to another node; journal conventions are not FG7-5's owns. The finding the spec's §9 item 3 asks for should go in `plans/piles/forge/findings/`: `<node field on every pile-node dispatch> | перенос: forge findings | обоснование: journal convention, outside FG7-5 owns | подтвердил: —`.

## Standing questions

1. **Fit**: §3.1 CLI, §3.2 dict keys, §3.3 text (header, table, top lines, `>=`, `n/d`, `(+N more)`, shared line, empty window) and E1-E23 are all implemented. Exceptions: B1 (E3/E7/E10 on `same_worker`) and F1 (E15 with `defect_found`).
2. **Builder decisions**: safe direction, except `same_worker` (B1).
3. **Seams**: additive. A new section before `# report`, and the branch in `main()` before `--check`/`compute()` (positional invariant kept). I-1 verified by byte comparison against main's module on the same tree: `--check --warn` stdout and stderr identical, bare `--window 2026-11-13` identical, `--json` identical.
4. **Class completeness**: SIBLING_MAP axis 14 holds. The new reader imports `transcripts` (no private glob), and the price rule is `request_parts` plus `accounted_cost` (row "request-parts reader"). The axis-14 consumers row could name `forge_metrics --node-cost`: a map line for the Lead, not a defect. F1: hop_metrics is not imported (grep `hop_metrics` finds only the comment at `:1010`). The "node of a task = first node_of" duplication was accepted by F1(a) and is named in forge_metrics' comment. hop_metrics' docstring was not updated, but it is a non-goal file. Same-artifact sweep of the money direction: the LOW-figure sources inside the diff are no transcript, bad ref, unpriced, skipped usage (all named), `same_worker` (B1) and `split_missing`/`bad_iterations` (F3). No other neighbours.
5. **Tests**: 283 test lines against 352 product lines, under the volume rule. One parameterised table per behaviour (T1 18 rows, T2 6, T3 7), plus the broken-price test, T4 and the F6 pin. No new file. The rows check I-3 and I-4 on every case. Killing power: T1 would catch a shared pass counted twice, an unpriced model read as 0, and a cross-clone merge. It would NOT catch B1 or F1, whose rows are owed. T4 is one subprocess, by precedent. No pin on a measured constant: prices are test data.
6. **DUPLICATION AND CONSISTENCY**: one finding inside the diff (F5). No second price rule: grep `accounted_cost(` over `tools/*.py` gives usage_report and the three known consumers (savings_report, token_usage_stats, forge_metrics:1049). Transcript location goes only through `find_agent_transcripts`: grep `glob(` in forge_metrics finds only `compile_glob` and the journal-dir glob at `:1475`. The `critic:` pattern is built from `ID_PATTERN` and pinned equal to `journal_echo.CRITIC_TOKEN_RE.pattern` (test passes).
7. **CODE QUALITY**: F2 (fix before merge), F4 dead branch, B1's dead `same_worker` key, F6 header that can name the wrong file.
9. **Ratchets**: no in-tree ratchet row touched.
10. **Architecture**: outside the package, `architecture: none`. No new reader, writer or form of an existing fact.
11. **Judgment**: data only. The reason column is event counts, and no "why".
12. **ONE ROAD**: none found. Grep for language, project or runner names in the diff gives none, and every task goes through one grouping.

Readers (question 9): `( cd <wt> && python -I -c "...import piles..." )` prints `[]`: transcripts, usage_report, hop_metrics and journal_echo are not loaded. Pre-commit `--check --warn` output is identical to main's.

## Control runs (verbatim; money redacted)

```
( cd <wt> && python -B tools/forge_metrics.py --node-cost --window 2026-11-13 )   -> exit 0
rows 537 (accepted 488, open 49; 377 with no node and no link token); dispatches 752: measured 742, unmeasured 10; total >= $<x>, tokens 4237454807
not measured: t-391@dev1 line 969 (no_transcript), ... t-531@dev1 line 1312 (no_transcript), t-747@dev1 line 1819 (bad_ref cli:20261114T040810)
stderr: 22 warning lines (two nodes t-134/t-333; critic:t-NNN naming no critic dispatch)

probe (independent journal parse + usage_report.iter_assistant_turns):
t-505 tokens 20335530 20335530 cost match dispatches 4 4
t-615 row tokens 29470336 29470336 cost match dispatches 4 4
t-449 shared tokens 4084765 4084765 cost match dispatches 1 1
I-3: printed row tok 4100371373 + shared 137083434 = total 4237454807; cost rows+shared-total diff=0.00; independent delegated count 752 = json 752; task in two places: 0

unpriced probe (price copy without opus models):
t-505 partial True cost None? False unmeasured [(1284, 'unpriced:claude-opus-5-5'), (1302, 'unpriced:claude-opus-5-5')]
| t-505@dev1 | accepted | 4 | 2 | 20335530 | >= $<x> | 2 (spec 2) | 1 | 2 (replaced 0) | 1 | 0 |
rows 537 (...); dispatches 752: measured 511, unmeasured 241; total >= $<x>, tokens 4237454807

B1/F1 repro (scratch, tmp worlds):
c1 forge/7/FG7-9 0.0 False [] $0.00        <- transcript entirely unpriced, printed as measured zero
c1 t-001 None True ['unpriced:m-x'] n/d
c2 rows []                                   <- in-window defect_found on an old row: row absent

--node-cost --write / --check / --out x.md   -> rc 2 each, the P18 line; git -C <wt> status --short -> empty
--check --warn: main module vs branch on the same tree -> STDOUT IDENTICAL, STDERR IDENTICAL; bare report identical; --json identical
python -B -m pytest tools/test_forge_metrics.py -q -k node_cost -> 34 passed, 85 deselected in 2.99s
```

## Not checked

- The full test file. The builder's tail shows 116 passed and 3 skipped; I re-ran only the 34 node-cost tests.
- `--projects-root` on a machine with no `~/.claude/projects` (E19 default branch). Read only: the glob over a missing base yields nothing, so every dispatch is `no_transcript`.
- E13 `node_not_form` warnings, and E17 unreadable lines, on real data.
- The CI pipeline (batch canon, coordinator's duty).

```json
{
 "verdict": "fit_with_fixes",
 "blockers": [
  "B1 tools/forge_metrics.py:1028-1030,1059 -- same_worker: seen is set even when the first line priced nothing, so a later line of the same agent id in another row is a measured 0.0 and the row prints $0.00 (repro: unpriced m-x worker on t-001, reused on node FG7-9 -> FG7-9 prints $0.00, partial False); the spec's note priced on line N is absent and the same_worker key is read by nobody (live: agent ac4577455825daa31 on t-310 OF4-10 and t-315 OF4-21)"
 ],
 "fixes": [
  "B1 (blocks merge): keep seen[aid]=(line, priced); unpriced first line -> later line repeats its whys (unmeasured); priced -> later line carries same_worker with the first line number, printed; T1 rows same_worker_first_unpriced and the note in same_worker_twice",
  "F1 forge_metrics.py:1099-1101,1169-1171 -- defect_found ts counts into in_window of its ref row (E15); one T1 row",
  "F2 forge_metrics.py:1063-1259 -- split node_costs (197 lines, nesting 4+) into _nc_tasks/_nc_links/_nc_row/pricing",
  "F3 forge_metrics.py:1036 -- pass counts and name split_missing/bad_iterations as a why (LOW-figure sources, spec 2.4); latent, 0 live",
  "F4 forge_metrics.py:1039-1040 -- remove the dead except (ValueError, TypeError): request_parts with a skipped list never raises them",
  "F5 forge_metrics.py:1026 and 1181-1182 -- one _agent_id helper instead of two copies inside the diff",
  "F6 forge_metrics.py:1277 -- header hard-codes tools/model_prices.json even when prices are passed; carry the table source in the dict"
 ],
 "class_completeness": "SIBLING_MAP axis 14 kept: transcripts is the one reader, request_parts + accounted_cost the one price rule, no hop_metrics or journal_echo import; F6 critic pattern pinned equal. Same-artifact sweep of LOW-figure sources: no_transcript, bad_ref, unpriced, skipped usage named; same_worker (B1) and split_missing/bad_iterations (F3) not. Outside owns: node field on every pile-node delegated line (11-14: 2/235) -- a forge finding, not FG7-5; spec text defects (t-505 display, window 2026-13-99 premise, totals cost n/d) -- Lead edits the spec.",
 "trail": {
  "read": [
   "docs/tasks/specs/20261116-fg7-5-node-cost-with-rework-spec.md",
   ".claude/worktrees/agent-add9d41f9d6897482/docs/tasks/handoffs/t-905-fg7-5-node-cost.md",
   "docs/tasks/critic-diff-brief.md",
   "git diff main...HEAD tools/forge_metrics.py tools/test_forge_metrics.py (worktree)",
   "tools/transcripts.py:80-139,290-478",
   "tools/usage_report.py:467-602",
   "tools/forge_metrics.py:756-757,1644-1690",
   "docs/SIBLING_MAP.md:335-352",
   "tools/critic_verdict.schema.json",
   "logs/journal/dev1.jsonl (t-505, t-615, t-626, t-449, t-438, t-441, t-457 lines)"
  ],
  "reruns": [
   {"command": "( cd wt && python -B tools/forge_metrics.py --node-cost --window 2026-11-13 [--json] )", "result": "exit 0; rows 537, 377 unlinked, dispatches 752 (742 measured, 10 unmeasured), tokens 4237454807"},
   {"command": "scratch probe.py: raw journal + usage_report.iter_assistant_turns + accounted_cost for t-505, t-615 row, t-449 shared", "result": "tokens equal, cost match, dispatches and counts equal on all three"},
   {"command": "scratch I-3 check on printed table and JSON", "result": "rows+shared tokens = total; cost diff 0.00; 752 independent = 752 printed; no task in two places"},
   {"command": "scratch probe2.py: node_costs with price copy lacking opus", "result": "t-505 >= with two unpriced entries; total >=; 241 unmeasured; n/d rows never $0.00"},
   {"command": "scratch tmp worlds via test helpers (same_worker unpriced; out-of-window defect)", "result": "FG7-9 prints $0.00 partial False (B1); rows [] (F1)"},
   {"command": "--node-cost with --write / --check / --out; git -C wt status --short", "result": "rc 2 each with the P18 line; status empty"},
   {"command": "main module vs branch: --check --warn, bare --window 2026-11-13, --json", "result": "stdout and stderr identical in all three"},
   {"command": "( cd wt && python -B -m pytest tools/test_forge_metrics.py -q -p no:cacheprovider -k node_cost )", "result": "34 passed, 85 deselected in 2.99s"},
   {"command": "python -I import piles; modules transcripts/usage_report/hop_metrics/journal_echo loaded?", "result": "[]"}
  ]
 }
}
```
