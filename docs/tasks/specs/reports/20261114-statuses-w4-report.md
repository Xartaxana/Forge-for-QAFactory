# Statuses wave 4 report (t-661, 14.11.2026)

Worktree `.claude/worktrees/statuses-w4`, branch `wip/statuses-w4`, base origin/main d5059a5. Docs only (plans/piles and this report). Status cells set with `piles.py status` (node level, `--task t-661`); «Ход» lines by Edit. No `take`/`close`, nothing under `ai-packages/`, `tools/`, `logs/`, `DECISIONS.md`, `plans/BACKLOG.md`.

## Part A: statuses moved

| pile / batch / node | old | new | merge hash | report line |
|---|---|---|---|---|
| live-run-fvf / 2 / FV2-2 | ожидает | принято: 4f37213 | 4f37213 | wave 2 report, Merges: `wip/fv2-2` -> 4f37213 |
| speed-cost / 6 / SC6-2 | в работе | принято: d07737f | d07737f | wave 2: `wip/sc6-2` -> d07737f |
| package-ci / 3 / PC3-2 | сдано | принято: 542075f | 542075f | wave 2: `wip/pc3-2` -> 542075f (tip 0f8dd54 = the commit the wave-1 report ties to package-ci/3 PC3-2) |
| pre-code / 3 / PC3-1 | в работе | принято: e44a5a2 | e44a5a2 | wave 2: `wip/pc3-1` -> e44a5a2 (the report's `test_story_sides.py` repair names it; that file is in pre-code/3 PC3-1's owns) |

«Ход» lines added (one each): live-run-fvf/2, speed-cost/6, package-ci/3, pre-code/3 (the four above); live-run-fvf/1 (FV1-19), collect/4 (CL4-1), test-code-quality/2 (TQ2-1); thinking-roles/6 (TR6-2, see B5).

Status NOT moved, only a «Ход» line:
- FV1-19 (live-run-fvf/1): wave 3 merged `wip/fv19-c2` as 819a31f. The node stays «в работе»: the wave 2-4 reports name neither C1's merge nor the node closed as a whole (wave-1 line already says base N1-N3 merged 4d0ad66, C1 in work).
- CL4-1 (collect/4): wave 4 merged `wip/cl4-1-n4` (a6add6c) = N4 only (spec nodes N1-N4). No report names N1, N2, N3 merged. Node not closed, cell «ожидает» untouched.
- TQ2-1 (test-code-quality/2): wave 4 merged `wip/tq2-1-k2` (198638f); the report speaks of "tq2-1 K1" and the branch is `-k2`; the node's own fork F1 waits for the owner. Node not closed, cell untouched.
- FV1-11 (live-run-fvf/1): «сдано» since wave 1, not named in any wave 2-4 merge list. Left as is.

Edge 1, "no node found" (branch named in a wave report, maps to no node of any batch file):
- `wip/statuses-wave1`, `wip/owner-words-1113b` (wave 2): docs branches, not nodes.
- `wip/p1v-n4b` (wave 2): P1-v N4b; no `P1-v` / `П1-в` string in any batch file.
- `wip/tbw-t1` (wave 4): the "told before work" T1 node; no pile carries it (grep `T1a|T1-0|told.before|tbw|told_before|T1r|T3a`, case-insensitive, over `plans/piles`: one hit, an unrelated `stand-and-sources` finding B-275 on "T1a" of another topic; positive control: `CL4-1`, same shape, finds `collect/batch-4`). 
- `wip/p1b-n1` (wave 4): P1-b N1; no pile row (live-run-fvf/2 FV2-13 and FV2-15 only mention "P1-b N1" as a dependency).
- Wave 3 job A (retake of the frozen S6 console): no node.

## Part B: findings filed

All new findings: `id: —`, «Решение владельца нужно: нет» except the forge one. Each has its row in the batch table and in the card's «Содержание».

| # | finding (path under `plans/piles/`) | pile | batch row | source line |
|---|---|---|---|---|
| 1 | `live-run-fvf/findings/20261114-doroga-ostanovki-seam-stop-ne-pishet-stroku-otvetov-i-plan-lines-teryayutsya.md` | live-run-fvf | batch-2 FV2-16 | FV1-3 critic Q1 + Q3 + Q6 (pointer) + the owner's test row "rerun after a seam Stop" for `test_story_run_loop_b_threshold.py` (B2, item 2 of the dispatch): one file, same road |
| 2 | `live-run-fvf/findings/20261114-karty-reestra-gate-a-b-idut-k-dirizheru-bez-instrukcii-i-obratnoj-pechati.md` | live-run-fvf | FV2-17 | FV1-3 Q2 (scout first) |
| 3 | `live-run-fvf/findings/20261114-hvost-prompta-dirizhera-sobiraetsya-v-pyati-mestah.md` | live-run-fvf | FV2-18 | FV1-3 Q4 |
| 4 | `live-run-fvf/findings/20261114-record-answers-ne-nazyvaet-id-propushchennye-kak-tot-zhe-otvet.md` | live-run-fvf | FV2-19 | FV1-3 Q5 |
| 5 | `live-run-fvf/findings/20261114-told-world-skaniruet-paket-dvazhdy.md` | live-run-fvf | FV2-20 | T1 critic Q-a |
| 6 | `live-run-fvf/findings/20261114-rows-for-vozvrashchaet-pustoe-kogda-stroki-ne-prochitany.md` | live-run-fvf | FV2-21 | Q-b |
| 7 | `live-run-fvf/findings/20261114-check-id-zapisi-skvoznyh-vyhodov-nesut-sostoyanie-walk-error.md` | live-run-fvf | FV2-22 | Q-c |
| 8 | `live-run-fvf/findings/20261114-told-dublikaty-chitatelej-i-row-requirement-na-60-strok.md` | live-run-fvf | FV2-23 | Q-d + Q-e (same files) |
| 9 | `live-run-fvf/findings/20261114-covered-pokryvaet-id-lyubym-pod-id.md` | live-run-fvf | FV2-24 | Q-f |
| 10 | `live-run-fvf/findings/20261114-legacy-legs-i-unsited-tolko-potolok.md` | live-run-fvf | FV2-25 | Q-g |
| 11 | `live-run-fvf/findings/20261114-gruppa-tolko-dirizhera-chitaetsya-iz-note-cherez-regex.md` | live-run-fvf | FV2-26 | Q-i |
| 12 | `live-run-fvf/findings/20261114-t1-zametki-osevoj-blok-kommita-i-owner-v-otchyote-t1a.md` | live-run-fvf | FV2-27 | Q-h + Q-j (notes, no package code) |
| 13 | `cost-dashboard/findings/20261114-driver-report-schitaet-sluzhebnye-stroki-zhurnala-vyzovami.md` | cost-dashboard | NEW batch `batch-2-sluzhebnye-stroki-izmeriteli.md` CD2-1 + card «Пачки» row 2 | CL4-1 critic Q3 |
| 14 | `forge/findings/20261114-zhurnal-starye-stroki-s-defektami-poryadka-bez-dveri.md` | forge | batch-7 FG7-32 (+ owner question line in the card) | Lead word (item 6); «Решение владельца нужно: да» |

Why each placement:
- Item 3 of the dispatch (T1 lines Q-a..Q-j): no pile holds the T1 nodes (grep above), so edge 6 -> `live-run-fvf`, batch-2 (untaken, takes critic queues of 13.11). Each finding's «от» says so; the Lead may move them. Spec node ids T3a/T2/T1r/T4/T9a/T9c are written as "dependencies" of the rows (they live in `docs/tasks/specs/20261113-told-before-work-mechanism-spec.md`, not in a batch).
- Item 4 (CL4-1 Q3): pile `cost-dashboard` exists; it had only closed batch 1, so edge 3: opened `batch-2-sluzhebnye-stroki-izmeriteli.md` (status «ожидает», from `_template/batch.md`, incl. the «Бриф» heading the form check demands) and the card «Пачки» row 2 (size S). The Содержание row added. The `report_run.journal` half of the queue line had no carrier anywhere; the finding names both sites as one node.
- Item 6: pile `forge` (card: tools, plans, docs, `.githooks`; F19). Batch-7 is untaken; FG7-32 added.
- Item 5 (flake `test_controller_rework_repair_binding`): grep FOUND the node: `thinking-roles/batch-6-hvosty-p3.md` TR6-2 and its finding `thinking-roles/findings/20261113-test-controller-rework-repair-binding-krasnyj-odin-raz-fr-31.md` (first red, run 43342086225). I wrote a finding in live-run-fvf first, saw the grep hit, and DELETED it (no duplicate). The wave 3 red (run 43515748054, the same row) is added to the existing finding as «Второе наблюдение» with the wave 3 report quoted verbatim, plus one «Ход» line in thinking-roles/6 (untaken batch). The cause is NOT named: the report says it was not seen (CI prints only the first failure line; `refused_detail` not visible). The finding says how to name it (read shard 1 artifact of 43515748054 / the repr step already in TR6-2) and records the report's suspect (`never_started_after_s: 0.01`, test line 43) as "suspect, not verified". I did not run CI tools or the slow test.

Edge 5, NOT filed:
- FV1-3 critic F1, F2, F3, R1 and the optional `save_state` after the seam: fixes of the fix round / builder's choice, not queue lines. The F1 class remainder IS filed (item 1 above, Q3).
- Q6 is "already queued by the spec §4" -> filed only as a pointer line inside item 1 (it had no pile carrier).
- CL4-1 Q1/Q2 and the FV1-30b, P1-b queue lines: already filed by `20261113-findings-queue-report.md`; not repeated.

## Could not place / open points for the Lead

1. The line numbers in the FV1-3 findings (1-4) are from branch `wip/fv1-3` at c69ce79, which is NOT in origin/main d5059a5 (`register_words_to_conductor` does not exist there; `take_question_answer`, `_unread_kept_gate`, `record_answers` do). The findings say so. FV1-3's merge is not in any wave report; no status was set for it.
2. live-run-fvf batch-2 now has 27 nodes (FV2-1..27), over the template's "L = 10-15, more means two batches". I set the card size M -> L and did not split; the Lead may cut a batch 3.
3. TQ2-1 and CL4-1 stay «ожидает» though part of each is merged (no legal word between ожидает and в работе for "some sub-nodes merged" except `в работе`, which I did not use because the reports do not say work on the rest started). Question: should they move to «в работе»?
4. A repair the wave 4 report calls a guess: `plans/features.json` F06 for the p1b-n1 files (owner unclear). Not touched here.
5. `docs/tasks/specs/reports/20261113-wave2-integration-report.md` fork (item B diagnostic invisible under the runner's 3-FAIL-line window, options a-d) and the not-mine `test_current_audit_contract.py` red: I did not search the piles for a row of either (not verified whether one exists). They are Lead lines in the wave report, not in the dispatch; named here, not filed.
6. The wave 4 "defects against accepted branches" (tq2-1 K1 `(P16)` in a charter; p1b-n1 lint findings and 12 unregistered files) are `defect_found` journal material, not pile lines.
7. Sibling check (card «Пачки» table of `live-run-fvf`): both batch files have their row, status «ожидает» for both (none taken); batch-2's row said `FV2-1…FV2-9` and now says `FV2-1…FV2-27`.

## Needed beyond the manifest

`plans/piles/_template/batch.md`, `plans/piles/thinking-roles/` (batch-6, finding, README grep), `plans/piles/forge/README.md` + batch-7, `plans/piles/cost-dashboard/` (README, batch-1), `plans/piles/live-run-fvf/` README and batch-2, `ai-packages/qa-factory/scripts/tests/test_controller_rework_repair_binding.py` (lines 43, 225-264), `tools/test_pile_cards_contents.py`, `docs/tasks/specs/20261113-cl4-1-collect-stalled-looped-spec.md` (node list), `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` (existence), `experiments/measurers/` (file existence).

## Witness (verbatim)

`python -B tools/piles.py --repo <worktree> check --all` (exit 0), lines other than the baseline WARN:
```
(а) placement: ok (296 open ids, 136 closed, 190 findings, 165 batch-row members)
(в) frozen: ok (10 taken batch(es) on origin/main; every other batch is new or not yet taken: free)
(г) backlog: ok (frozen (compared with HEAD))
(д) form: ok (33 piles, 102 batches)
(е) findings: ok (1040 findings read, 0 dated from 2026-10-13 on are orphans, 152 older are the baseline)
piles check: ok
```
(The (б) line is `ok` as well; the (е) WARN is the 152-finding baseline, same as before my change.) The first run before the «Бриф» fix printed `(д) form: RED -- plans/piles/cost-dashboard/batch-2-sluzhebnye-stroki-izmeriteli.md: an untaken batch has no «## Бриф» heading` and `test_card_and_batch_headings[cost-dashboard]` failed; both fixed.

`python -m pytest tools/test_pile_cards_contents.py -q` (subshell in the worktree): `135 passed in 2.45s`.
