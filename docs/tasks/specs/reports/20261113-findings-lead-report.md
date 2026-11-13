# t-545 report: critics' queue items of 13.11.2026 filed as findings

Branch wip/findings-lead. All paths relative to the worktree `C:\QAFactory\forge-repo\.claude\worktrees\findings-lead`.

## Table finding -> pile -> batch file -> README row

| F | node id | finding file (under `plans/piles/<pile>/findings/`) | pile | batch file | README row |
|---|---|---|---|---|---|
| F-2 | FV2-1 | `20261113-chitatel-plan-row-chitaet-klyuch-kotorogo-net-v-kontrakte.md` | live-run-fvf | `batch-2-live-run-fvf.md` (new) | Содержание, "Пачка 2" |
| F-3 | FV2-2 | `20261113-by-leaf-requirements-pomechaet-polya-kotorye-kod-ne-zapolnyaet.md` | live-run-fvf | batch-2 | same |
| F-1 | FV2-3 | `20261113-py-test-dva-chitatelya-odnogo-voprosa-vybor-po-id-uzla.md` | live-run-fvf | batch-2 | same |
| F-4 | FV2-4 | `20261113-vyhody-stadii-kotorye-ne-otkazyvaet-ni-odin-chitatel.md` | live-run-fvf | batch-2 | same |
| F-5 | FV2-5 | `20261113-ledger-krasnyh-strok-sklevaet-povtornyj-id-cherez-i.md` | live-run-fvf | batch-2 | same |
| F-6 | FV2-6 | `20261113-chastnyj-vyzov-i-dvojnoj-gard-papki-zhurnala-progona.md` | live-run-fvf | batch-2 | same |
| F-8 | FV2-7 | `20261113-tekst-s5-md-ob-otkazah-markera-ustarel-posle-fv1-19.md` | live-run-fvf | batch-2 | same |
| F-9 | FV2-8 | `20261113-role-load-ne-proveryaet-tipy-allowances-brief.md` | live-run-fvf | batch-2 | same |
| F-7 | FV2-9 | `20261113-formy-vybora-testa-tolko-dlya-pytest-i-playwright.md` | live-run-fvf | batch-2 | same |
| F-10 | FG7-31 | `20261113-pravilo-pt4-gigieny-dohodit-do-bildera-tolko-tekstom-v-diszpatche.md` | forge | `batch-7-vhodyashchie-4.md` (untaken, existing; node row FG7-31 added) | Содержание, after FG7-30 row; "Пачки" row 7 range widened to FG7-31 |

live-run-fvf README: «Пачки» table got row 2 (FV2-1…FV2-9, ожидает).

## Decisions and divergences (read these)

1. Coordinator message said live-run-fvf batch-1 is TAKEN. Reality: `batch-1-live-run-fvf.md` header is `статус: ожидает | взял: —`, identical on origin/main (fetched). Nothing was added to batch-1; I followed the coordinator's explicit instruction and opened batch-2 with the ids FV2-1/FV2-2 and numbering FV2-3.. in the order F-1, F-4, F-5, F-6, F-8, F-9; F-7 (not in the coordinator's order list) took the last id FV2-9. No existing batch-2 existed. If batch-1 is not going to be taken, the Lead may want to merge the rows.
2. The finding form refuses `id: FV2-1` (gate (д): expected B-nnn or —). Fixed what the gate names: `id: —` in all findings, node ids FV2-1/FV2-2 written as `узел: FV2-1` on the header line of F-2/F-3 and in the batch table.
3. Source node for P1-a / P1-v findings (F-2..F-6): P1-a and P1-v are spec topics, not nodes in any pile batch (grep of `P1-a|P1-v` over plans/piles/*/batch-*.md: no hits) -> `live-run-fvf` as instructed. FV1-4, FV1-18, FV1-19 are batch-1 rows of live-run-fvf.
4. F-7 pile: execution-probes has only closed batches (1-3) and none carries selection-row nodes (EP1-1 is the one-predicate/runner-identity node, closed) -> FV1-18 pile live-run-fvf.
5. F-10 pile forge, untaken batch 7 (`статус: ожидает`); node FG7-31, "Пишет в" is `tools/hygiene_gate.py` plus "носитель строки калибровки — по взятии".
6. «нужна доразведка» lines written (verdict gives too little): F-4 (names of the 8 "no reader refuses" and 6 "not covered" outputs exist only in the stdout of the P1-a ledger run, not in the verdict or any file I could read); F-5 (exact function; candidates `scripts/tests/known_red.py`, `test_field_producers.py` from branch wip/p1a-fix); F-7 (runner selection flags per form); F-9 (sibling keys); F-10 (is hygiene_gate on the builders' path); F-2 (where roles were told to write `plan_row:`, as the verdict itself states).
7. Already filed check (case-insensitive grep over plans/piles and docs, with a positive control: `py\.test` found `execution-probes/README.md:74` B-440): `_plan_row_of`, `BY_LEAF`, `plan_row:`, `_package_fingerprint`, `journal_if_story`, `brief_charter_head` have no hit in plans/piles (only in specs/reviews/snapshots). `py.test` only the unrelated B-440. Result: none already filed. (`p1a-fix-rereview.md` L1 asks to open P2/P5 nodes — now done as FV2-1/FV2-2.)
8. Census: `docs/tasks/specs/reports/t-2046-language-exceptions-census.md` exists in this worktree; table M4 row "selector contract verified" (line 63) marked closed with the text given, commit 274b57f, plus the pointer to F-1.
9. Note: in F-1, `launch-causes.json` as the data carrier of `selection_by_node_id` is taken from the compact snapshot (t-516), not read from code; the verdict says "data row". F-5's remark that `known_red.load` already refuses duplicate JSON keys was read in `wip/p1a-fix`.

## Ad-hoc check scripts

None (only `tools/piles.py` commands and `git grep`).

## Witness (verbatim, run after `git add`, from the worktree)

`python -B tools/piles.py check --all`:
```
(а) placement: ok (296 open ids, 136 closed, 190 findings, 165 batch-row members)
(б) overlap: ok (10 active batches)
(в) frozen: ok (10 taken batch(es) on origin/main; every other batch is new or not yet taken: free)
(в) frozen: compared with origin/main be2c988
(г) backlog: ok (frozen (compared with HEAD))
(д) form: ok (33 piles, 101 batches)
(е) findings: ok (1015 findings read, 0 dated from 2026-10-13 on are orphans, 152 older are the baseline)
(е) findings: WARN: 152 finding(s) dated before 2026-10-13 or undated (69) ... (baseline, not blocking)
piles check: ok
CHECK_RC=0
```
`python -B tools/piles.py board --check`:
```
piles board: up to date (33 piles, 101 batches, 432 ids)
BOARD_RC=0
```
`python -m pytest tools/test_pile_cards_contents.py -q`:
```
........................................................................ [ 53%]
...............................................................          [100%]
135 passed in 3.05s
```
Before the fix the first `check --all` was RED (д) on `id "FV2-1"`, `id "FV2-2"` and on FV2-5 "no path in Пишет в"; fixed as named (decision 2; FV2-5 got candidate paths).

## Needed beyond the manifest
Read: `docs/tasks/specs/reviews/*` (root checkout), `plans/piles/forge/` README and batch-7, `plans/piles/_template/batch.md`, `plans/piles/execution-probes/batch-1`, git objects of `wip/p1a-fix` (`known_red.py`).
