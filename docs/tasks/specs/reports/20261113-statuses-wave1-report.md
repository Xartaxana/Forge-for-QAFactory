# Statuses wave 1 report (13.11.2026)

Worktree `.claude/worktrees/statuses-w1`, branch `wip/statuses-wave1`, base origin/main 7cf8c34. Status cells written with `piles.py status` (node level); «Ход» lines by Edit. Rows changed: 7 node status cells (plus 6 «Ход» lines, one per batch file).

## Rows changed

| node | file:line | old | new |
|---|---|---|---|
| FV1-4 | plans/piles/live-run-fvf/batch-1-live-run-fvf.md:37 | ожидает | принято: f3167f3 |
| FV1-21 | plans/piles/live-run-fvf/batch-1-live-run-fvf.md:57 | ожидает | принято: 4f61fb5 |
| FV1-19 | plans/piles/live-run-fvf/batch-1-live-run-fvf.md:58 | ожидает | в работе |
| FV1-11 | plans/piles/live-run-fvf/batch-1-live-run-fvf.md:44 | ожидает | сдано |
| PC3-1 (pre-code) | plans/piles/pre-code/batch-3-povtornoe-chtenie-storon.md:26 | ожидает | в работе |
| PC3-2 (package-ci) | plans/piles/package-ci/batch-3-khrapovik-doors-only.md:26 | ожидает | сдано |
| SC6-2 | plans/piles/speed-cost/batch-6-tsena-i-samouluchshenie.md:24 | ожидает | в работе |

(7 rows: the count in the final message is 7.) «Ход» lines added to: live-run-fvf/1, pre-code/3, package-ci/3, speed-cost/6, collect/4, test-code-quality/2.

## Not changed on purpose (no legal status word)

- Spec ready, builder waits: CL4-1 (collect/4), FV1-3, FV1-5, FV1-6, FV1-17, FV1-20, FV1-22, FV1-23 (live-run-fvf/1), TQ2-1 (test-code-quality/2, waits for owner on F1): the parser knows no word between «ожидает» and «в работе», so the cell stays «ожидает»; the fact is a «Ход» line.
- FV1-12: stays «ожидает»; «Ход» line says the owner's word is given 13.11 and the node waits for a spec.

## Divergences from the facts

- PC3-2: the facts say «pre-code batch 3». pre-code/3 has only PC3-1. PC3-2 exists in package-ci/3 (row about `test_probe_by_code_languages.py`; commit 0f8dd54 is its re-point of the gate-registry row, `PC3-2` in the subject). I set package-ci/3 PC3-2 to «сдано». package-ci/3 also has its own PC3-1 (DOORS_ONLY_BRIEF_MAX), left untouched.
- FV1-11, PC3-2: accepted but merge pending, so «сдано» (a node «принято» needs a merge hash in main; 7cf8c34 does not carry them).
- Batch headers and cards of all six batches are «ожидает» (none taken on origin/main); the tool does not touch them for node statuses, and I did not `take` anything.

## Nodes not found (no row in any `batch-*.md` of plans/piles; Grep and a PowerShell scan of all non-findings `.md`)

FV2-1, FV2-2, FV1-30a, FV1-30b (N0, N2), the FV1-19 base N1-N3 (FV1-19 has one row, no N-subnodes), the P1-v nodes N0-N4 and N4b (no `P1-v` / `П1-в` string anywhere in plans/piles outside findings), P1-a fix rounds, P1-b N0, T1-0 (told-before-work). Probably these piles/batches live on other branches or are not yet written into batch files; nothing invented. The guard sibling fix (wip/guard-sib) has no node either.

## Witness

Before edits, `piles.py check --all` tail:
```
(в) frozen: compared with origin/main 7cf8c34
(г) backlog: ok (frozen (compared with HEAD))
(д) form: ok (33 piles, 100 batches)
(е) findings: WARN: 152 finding(s) dated before 2026-10-13 ... (baseline; not blocking)
piles check: ok
```
After edits (same command): `(е) findings: WARN: 152 finding(s) ...` (same baseline WARN) and `piles check: ok`.

`python -m pytest tools/test_pile_cards_contents.py -q`: `135 passed in 4.93s`.
