# Statuses w13 report (t-770, 14.11.2026)

Worktree `.claude/worktrees/statuses-w13`, branch `wip/statuses-w13`, base origin/main e4df9c0. Docs only. Status cells set with `piles.py status ... --task t-770`; «Ход» lines by Edit. No CI, no mutations.

## Table

| node | old | new | evidence (origin/main) |
|---|---|---|---|
| live-run-fvf/1 FV1-5 | ожидает | принято: 1a00352 (t-770) | wave 13c 1a00352 (t-745, critic t-752); a03ea51 + fix round 80297b9 are ancestors; the node owns only `env_probe.py` |
| live-run-fvf/2 FV2-1 | ожидает | принято: 1d1206b (t-770) | `Merge wip/fv2-1` 1d1206b (a60160e, wave 1); reader part done; "find where roles taught `plan_row:`" answered "none found" in `20261113-fv2-1-report.md` (see Q1) |
| forge/7 FG7-32 | ожидает | принято: 6dddd4c (t-770) | 6dddd4c (t-746, critic t-750): door `order-known:<ts>`, count read by calibration check 13(m); the "how dev1 journal is committed before the door" is an owner decision, not a code part |
| live-run-fvf/1 FV1-9 | принято: ec7b838 | not moved — already принято | tail card A da10e9d (wave 13b) added to the Ход line; B, C, D already had Ход lines |
| live-run-fvf/1 FV1-30 | принято: 2a88226 | not moved — already принято | nothing to do |
| live-run-fvf/1 FV1-23 | ожидает | not moved — partial | A-1, A-4 b9dd7d0; A-2, A-3 ba903eb; A-5 `origin/wip/fv123-a5` not an ancestor of main (exit 1). One Ход line |
| live-run-fvf/1 FV1-20 | ожидает | not moved — partial | only B-1 754b9de; no new merge since the t-729 line (git log `--grep FV1-20`: B-1 commits only); no new line (duplicate of t-729), mentioned in the t-770 line |
| live-run-fvf/1 FV1-6 | ожидает | not moved — not found in main | Lead said N1 merged. No commit: `git log origin/main -S s4_review_limit -- ai-packages` shows only unrelated P1-b census/split commits, `-S s4_round_bought` only the TD-11 split; the only code is `5b27a38` FV1-6 N2 on `origin/wip/fv16-n2`, not an ancestor of main. Ход line says so |
| forge/7 FG7-18, FG7-20 | ожидает | not moved — partial | 1978cef (12.11, t-113) carries `siblings:` and `designer:` header lines in `dispatch_manifest` (a refusal with a door; the node text says WARN `neighbors:` — form differs). The existing Ход line of 12.11 13:58 says the second half (E2 of `fg-context-and-hygiene.md`, printing carriers and witnesses) is not started; I found no E2 merge (log grep E2 / witness-for / fg-context: nothing). One Ход line |
| onboarding-forge/3 OF3-1 | ожидает | not moved — partial | still as the t-669 line: parts a-e in main, f (`knowledge-read-baseline.json`, `changelog.d/t-129-of3-1f.md`) absent from main (ls-tree of origin/main: no such file). No new fact, no new line |
| onboarding-forge/3 OF3-2 | ожидает | not moved — partial | only K6 (665fb82), as the t-672 line; `origin/wip/of3-2-k6` is the only OF3 branch; no new line |
| stage-critics A2, A3, F7 re-cut (7379e0d) | — | not moved — node not found | no row with these ids in any batch file (case-insensitive grep of `plans/piles` outside findings for stage-critic / SC-A: only unrelated G2-16/G2-17/SC2-45 hits). They are nodes of spec `docs/tasks/specs/20261113-stage-critics-s2-s3-removed-spec.md`, not of a pile. Report line, no edit |

## Живые доказательства (item 3)

The «Живые доказательства» tables of live-run-fvf/1, live-run-fvf/2 and forge/7 hold only the header row, no open rows: nothing to move to `live-runs`. FV1-5, FV2-1, FG7-32 had none.

## «Ход» lines added

- live-run-fvf/1: `14.11 (t-770) — статусы по слиянию в main: FV1-5 принято ... FV1-9 карточка A ... FV1-23 слит частично ... FV1-20 ... FV1-6 ...` (one line).
- live-run-fvf/2: `14.11 (t-770) — FV2-1: принято, wip/fv2-1 слита в main коммитом 1d1206b ...`.
- forge/7: `14.11 (t-770) — по слиянию в main: FG7-32 принято, 6dddd4c ... FG7-18 и FG7-20 слиты частично ...`.

## Questions / for Lead

1) FV2-1: marked принято on the reader merge; its report's open question (three FV2-1 ledger rows stay red because of the P-n / TS-n split, FV1-14; stale notes) is unresolved and stays with Lead. Revert the cell if "принято" needs that closed.
2) FG7-18/FG7-20: Lead's brief called them "already built"; the batch file's own Ход (12.11 13:58) calls it the first half. I kept the status. If the owner accepts the refusal form instead of WARN as the whole node, the cell can move with 1978cef.
3) FV1-6: Lead's list names N1 as merged; I could not find it (see table).

## Checks (verbatim, from the worktree root in a subshell)

Before (`python -B tools/piles.py check --all`, exit 0), tail:
```
(а) placement: ok (296 open ids, 136 closed, 190 findings, 165 batch-row members)
(в) frozen: ok (10 taken batch(es) on origin/main; every other batch is new or not yet taken: free)
(в) frozen: compared with origin/main e4df9c0
(г) backlog: ok (frozen (compared with HEAD))
(д) form: ok (33 piles, 102 batches)
(е) findings: ok (1063 findings read, 0 dated from 2026-10-13 on are orphans, 152 older are the baseline)
piles check: ok
```
After (same command, exit 0), tail: identical lines, `piles check: ok` (the (б) and WARN lines unchanged: 45 pairs of one developer not compared; 152 baseline findings WARN).

`( cd <worktree> && python -m pytest tools/test_pile_cards_contents.py -q )`: `135 passed in 2.87s`.

## Beyond the manifest

`git log`/`git grep` over origin/main, `docs/tasks/specs/reports/20261113-fv2-1-report.md`, `20261114-statuses-fv1-report.md`, `fg-context-and-hygiene.md` (grep), `20261114-fv1-6-s4-only-spec.md` (grep), batch-2 and forge/7 and onboarding-forge/3 batch files.
