# statuses-w15 report

Piles check before: `piles check: ok`. After: `piles check: ok` (`python -B tools/piles.py check --all`, last line).
Negative control: `git log --oneline -1 c03a6ac8` -> `c03a6ac8 wave 15b: FV1-28 C1 ...`; `merge-base --is-ancestor c03a6ac8 origin/main` -> ON_ORIGIN_MAIN.

Hash used = the wave commit on main (7 chars, as the file's own rows).

| node | file:line | old | new | hash |
|---|---|---|---|---|
| FV1-6 | plans/piles/live-run-fvf/batch-1-live-run-fvf.md:39 | ожидает | принято: 67b337a, bb958ce, eefe80e (t-797, t-687, t-791); фикс-раунд 2: 2c8cf41 (t-817) | N1, N2, N3 waves + fix round 2 |
| FV1-15 | batch-1-live-run-fvf.md:47 | ожидает | принято: 0a18b0d (t-796); фикс-раунд: eb04e57 (t-818) | 0a18b0d |
| FV1-17 | batch-1-live-run-fvf.md:49 | ожидает | принято: 3579b26, a0aa1aec (t-781, t-782, t-795); фикс-раунд: eb04e57 (t-818) | 3579b26 |
| FV2-54 (FV1-28 A1) | plans/piles/live-run-fvf/batch-2-live-run-fvf.md:81 | ожидает | принято: 334ff83 (t-774) | 334ff83 |
| FV2-55 (A2) | batch-2-live-run-fvf.md:82 | ожидает | принято: e335d78 (t-775) | e335d78 |
| FV2-56 (B1) | batch-2-live-run-fvf.md:83 | ожидает | принято: 3b3fc67 (t-777, t-798) | 3b3fc67 |
| FV2-57 (C1) | batch-2-live-run-fvf.md:84 | ожидает | принято: c03a6ac (t-807) | c03a6ac |
| FG7-36 (P1B-9 C5) | plans/piles/forge/batch-7-vhodyashchie-4.md:60 | ожидает | принято: caa63da (t-823) | caa63da |

Note: A1 (334ff83), A2 (e335d78), FV1-6 N2/N3, FV1-17a/c, FV1-6 N1 are older than 3b3fc675 but were still "ожидает"; marked too.

## Commit names a node I could not find in any batch file
- P1B-9 C1 (4dfcd09c/fbef5a3a), C2 (0d4932d1), C3 (bbb21ff4/e18e622f), C4 (b5c8dfeb): no node row (plan lives in spec only). FV2-67/68/69 are close in topic but their wording does not match C1-C4, left alone.
- P1-v F-1 (e98a4d2d), N8 (5b1793c8, e8d9a669), N9 (d0aa9161): no node rows.
- SC N7: no row found (grep hits are unrelated C3-4/PC4-9).
- Pile rows t-815 (30d49c2a, bc741cef): row/journal commits, skipped.

## Row found but status form unclear -- left as is
- FV1-28 finding row (batch-1:61): cards FV2-58, FV2-59 still pending, so left "ожидает".
- FV2-58 (B2): B1 tail t-798 "the way in reaches the briefs" may cover it; unclear.
- FV2-60 (FV1-28e): no matching commit seen.
- FV2-67 (one reader of runtime-provenance): possibly C3; unclear.
- FG7-37 (scoreboard_bar requests): N8/N9 commits do not show this dedup.
- No pile card row changed (no batch is fully done).
