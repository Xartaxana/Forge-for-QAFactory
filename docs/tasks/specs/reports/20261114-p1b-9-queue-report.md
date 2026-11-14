# t-838 report: P1B-9 verdict queue lines carried

Branch `wip/p1b9-queue` (from origin/main 66d6245). Commit hash: see the final message and `git log` (a hash cannot be written into the commit that carries this file).

## queue line -> finding file -> batch row -> card row

| queue line | finding file | batch row | card row |
|---|---|---|---|
| Q-L1 | `plans/piles/live-run-fvf/findings/20261114-p1b-9-rolevoj-provenance-ne-sveryaetsya-s-zapisyu-okna.md` | live-run-fvf batch-2 FV2-76 (untaken) | live-run-fvf README «Содержание» (+ «Пачки» row 2: FV2-1…FV2-78) |
| Q-2 | existing `findings/20261114-p1b-9-odin-chitatel-runtime-provenance.md`, section «Поправка вердикта P1B-9 (Q-2)» added (no new file: edge 2, batch-2 untaken) | FV2-67 re-scoped in place to L-2 (text from verdict Q-2; `handoff_check.py` dropped from owns) | existing row, unchanged |
| Q-3 | `plans/piles/live-run-fvf/findings/20261114-p1b-9-s5-formy-do-p1b-9-stoyat-na-prichine-e.md` | FV2-77 (watch, no code, owns «нет») | live-run-fvf README «Содержание» |
| Q-4 | `plans/piles/live-run-fvf/findings/20261114-p1b-9-review-receipt-pervyj-zagolovok-drugoj-poryadok.md` | FV2-78 | live-run-fvf README «Содержание» |
| Q-5 | `plans/piles/package-ci/findings/20261114-test-brief-pack-s5-plan-249-iz-250-na-baze.md` | package-ci batch-3 PC3-6 (untaken) | package-ci README «Содержание» (+ «Пачки» row 3 lists PC3-6) |

Edge 4 (already covered): grep of piles for `S5_PLAN_BRIEF_BYTES_MAX`, `249/250`, `_review_receipt`, `window_runtime_record` found nothing (positive control with the same tool on `runtime.provenance` found 23 files); the nearest finding `package-ci/.../khrapovik-doors-only-brief-max-posle-pc2-6.md` is another constant (`DOORS_ONLY_BRIEF_MAX`), so no duplicate pointer applies; Q-5 got its own finding and a cross-link. FV2-66/68/69 are sibling P1B-9 nodes, not these lines.

## «Ход» lines added (live-run-fvf batch-2, untaken; package-ci batch-3, untaken)

- live-run-fvf batch-2: "14.11 (t-838) — очередь вердикта ... заведена" (Q-L1/Q-3/Q-4/Q-2/Q-5 carry line).
- live-run-fvf batch-2: "слито без строки-узла: P1B-9 C1 4dfcd09c/fbef5a3a, C2 0d4932d1, C3 bbb21ff4/e18e622f, C4 b5c8dfeb" (home: spec `20261114-p1b-9-runtime-provenance-null-outcome-spec-r2.md` named in this pile's findings, sibling nodes FV2-66..69).
- live-run-fvf batch-2: "слито без строки-узла: P1-в F-1 e98a4d2d, N8 5b1793c8/e8d9a669, N9 d0aa9161" (home: the batch's first «Ход» line names P1-v critic queues; N8 spec `20261114-p1v-n8-carriers-draft.md` is cited by pile findings).
- package-ci batch-3: "14.11 (t-838) — узел PC3-6 ..." (new node line).

## Left undone

- SC N7: no home. Grep of `plans/piles` for "SC N7"/"N7" found only unrelated rows (conductor C3-4, release-next, package-ci PC4-9 N7 of a different spec); the plan the commit belongs to is not named in any batch. Not invented.
- Judgment call to confirm: the P1B-9 and P1-v merge lines went into live-run-fvf batch-2 (grep homes are indirect: P1-v via the batch's first «Ход» line, P1B-9 via sibling nodes and findings); no batch names the plan as its own.
- Open questions of the statuses report left undecided: FV2-58 (B2, t-798 may cover), FV2-60 (FV1-28e, no commit seen), FG7-37 (N8/N9 do not show the dedup). FV2-67 "possibly C3; unclear" is now answered by Q-2 (C3 is not it; node re-scoped), status stays «ожидает».
- Q-4 direction (one order = `_form_dispatch` order) is taken from verdict S-2/Q-4 wording; flagged as the pile Lead's to confirm at take.
- FV2-77 executor is written «Lead (чтение канона)» (no code node); the verdict names no executor.
- Nodes' «Зависит от» are my reading of the verdict, not verdict text.

## DoD output

Before (origin/main, my first run): 
```
(д) form: ok (33 piles, 103 batches)
(е) findings: ok (1096 findings read, 0 dated from 2026-10-13 on are orphans, 152 older are the baseline)
piles check: ok
```
First run after edits was RED: `(д) form: RED -- ... node FV2-77 has no path in "Пишет в"` (fixed: «нет»).
After:
```
(в) frozen: ok (10 taken batch(es) on origin/main; every other batch is new or not yet taken: free)
(г) backlog: ok (frozen (compared with HEAD))
(д) form: ok (33 piles, 103 batches)
(е) findings: ok (1100 findings read, 0 dated from 2026-10-13 on are orphans, 152 older are the baseline)
piles check: ok
```
`python -m pytest tools/test_pile_cards_contents.py -q` -> `135 passed in 3.44s`.

Needed beyond the manifest: `docs/tasks/specs/20261114-p1b-9-runtime-provenance-null-outcome-spec-r2.md` (name only), `ai-packages/qa-factory/scripts/handoff_check.py` (grep to confirm `_form_dispatch`, `_review_receipt`, `window_runtime_record` exist on main), `plans/piles/package-ci/batch-3-*.md`, `plans/piles/live-run-fvf/README.md`.
