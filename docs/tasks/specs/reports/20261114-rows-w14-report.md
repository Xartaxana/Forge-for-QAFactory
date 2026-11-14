# t-779 report: queue lines and owed node rows of the night verdicts, as findings and rows in untaken batches

Worktree `C:\QAFactory\forge-repo\.claude\worktrees\rows-w14`, branch `wip/rows-w14`. Docs only; `plans/BACKLOG.md` untouched; every finding `id: —`.
Form copied from e4df9c0 (t-756): finding file in `findings/`, row in an untaken batch, row in the pile card's «Содержание», a «Ход» line.

## Table: source line -> finding file -> pile / batch row

| source line | finding file (or "node row only") | pile / batch row |
|---|---|---|
| verdict spec §11 / K1 critic F2: K1g (`check_bug_drafts` exempts by `no_run_target`) | node row only (builds as t-778) | live-run-fvf batch 2, FV2-45 |
| verdict spec §11 / N-a spec: claim answer confirms | node row only, points at `20261114-fv1-24-na-claim-answer-confirms-spec.md` | live-run-fvf batch 2, FV2-46 |
| §11 N-b | `live-run-fvf/findings/20261114-n-b-requirement-silent-stroka-ne-nesyot-vopros-pretenzii.md` | live-run-fvf batch 2, FV2-47 |
| §11 N-c (+ owner question Q2, recommendation taken, «Решение владельца нужно: да») | `live-run-fvf/findings/20261114-n-c-istochnik-ozhidaniya-ne-pokazan-v-pakete-gejta-b.md` | live-run-fvf batch 2, FV2-48 |
| §11 A12 | `live-run-fvf/findings/20261114-a12-chernoviki-vne-hodoka-i-triage-app-bug-s-nepodtverzhdennym-r.md` | live-run-fvf batch 2, FV2-49 |
| A-5 critic Q-a (A-7, F5) | `live-run-fvf/findings/20261114-fv1-23-a7-odno-yadro-ssylok-dlya-linked-documents.md` | live-run-fvf batch 2, FV2-50 |
| A-5 critic Q-b (A-8: AC scan, F6 per-ticket bound as a Lead fork) | `live-run-fvf/findings/20261114-fv1-23-a8-kriterii-priyomki-v-s0-i-potolok-ssylok-na-tiket.md` | live-run-fvf batch 2, FV2-51 |
| A-5 critic Q-c (URL regexes; the critic's own queue line named a new finding in this pile) | `live-run-fvf/findings/20261114-odin-tokenizator-url-chetyre-regexa-vne-ticket-light.md` | live-run-fvf batch 2, FV2-52 |
| A-5 fix report analogs (old raw rows in `_settle_references`; second credential rule in `_record_source`; `token%3D`): ONE finding, three items | `live-run-fvf/findings/20261114-ssylka-maskiruetsya-odnim-pravilom-v-kazhdom-pisatele-i-chitatele.md` | live-run-fvf batch 2, FV2-53 |
| FV1-28 spec §2: cards A1, A2, B1, C1, B2, D1 (WAITING), FV1-28e (§9 and §10 items carried in the rows and in the «Ход» line) | node rows only, each points at `20261114-fv1-28-cards-redraft-spec.md` | live-run-fvf batch 2, FV2-54 (A1), 55 (A2), 56 (B1), 57 (C1), 58 (B2), 59 (D1), 60 (FV1-28e) |
| FV1-28 §6 forks F-9, F-10 (recommendation A taken) | open questions, not findings | `live-run-fvf/README.md` «Вопросы владельцу»; F-8 is closed in row FV2-56 (variant A) |
| K1 fix report: a report with no id lifts no place-born draft | open question under FV1-24 | `live-run-fvf/README.md` «Вопросы владельцу» |
| SC-N7 critic queue line: `red_sandbox` `--diagnostic` first-error | `execution-probes/findings/20261114-red-sandbox-diagnostic-otkazyvaet-po-pervoj-oshibke.md` | execution-probes batch 4 (OPENED, status «ожидает»), EP4-2 |
| P1-b N2e gap candidate 6 (`--mine` `mine_refused`, no door) | `execution-probes/findings/20261114-mine-refused-bez-dveri-dlya-profilya-bez-probi.md` | execution-probes batch 4, EP4-1 |
| P1-b N2e gap candidate 7 (`s6.stand_confirm` at S5) | `driver-hosts/findings/20261114-klyuch-voprosa-s6-stand-confirm-zadayotsya-na-s5.md` | driver-hosts batch 2 (untaken), DH2-1 |

Cards updated: `live-run-fvf/README.md` (batch 2 range FV2-1…FV2-60, 7 «Содержание» rows, 3 questions), `execution-probes/README.md` (batch 4 row, section with 2 rows), `driver-hosts/README.md` (1 row). New file: `execution-probes/batch-4-vhodyashchie.md`.

## Decisions I took inside the edges (for the Lead to check)

1. Pile choice, edge 1. K1g/N-a/N-b/N-c/A12/FV1-23/FV1-28 went to `live-run-fvf` batch 2 (FV1-28's parent row is in batch 1, but batch 2 is where the t-756 precedent put FV1-23 A-5/A-6 and where the cards of this night fit the file lists; the Lead re-cuts the over-size batch later, as the 14.11 «Ход» line already says). `red_sandbox` and `run_suite --mine`: the module zone is `execution-probes` (README «зона»), all its batches are closed, so batch 4 was opened (edge 5); the SC-N7 parent (`exploratory_findings`, FV2-40) lives in `live-run-fvf`, named in «связи». `s6.stand_confirm`: the question-price class of `driver-hosts` (C1-6b, `20261021-voprosy-build-check-bez-cen.md`), batch 2 untaken.
2. Edge 2: K1g and N-a, and the seven FV1-28 cards, got node rows (they have specs); N-b, N-c, A12 and the queue lines got finding files.
3. Candidate 7 is by design a shared key (`driver_stage_build.py` header comment: one question for S5 and S6). The finding says only the NAME misleads and the behaviour stays; direction chosen: a stage-neutral key, readers listed first (5 files found), form of the name left to the designer.
4. Candidate 6: the existing refusal already names a reason; the gap I wrote is who acts and by which door (the person records the checkout; the role goes on by hand). The finding makes the designer first measure whether the run gate accepts a hand-written request with no probe.
5. A-8 item 2 (per-ticket bound): the number is the Lead's fork; the finding says item 2 waits for it and item 1 runs without it. «Решение владельца нужно» stays «нет» there (Lead's fork), «да» only on N-c (Q2).
6. Statuses: all new rows «ожидает»; K1g's row says t-778 builds it, the status moves with the merge, not now.

## Lines I could not place, or placed with a caveat

- Verdict K2 and K5: not in the task list, no row written (their specs are being redrafted).
- A-5 critic F2 (paste leg) and K1 critic F3: already done in the fix rounds (fix report F2; K1 fix report F3), no row.
- `manual_evidence.py export` / `external_writes.py --record` (second SC-N7 queue line): not in the task, not written.
- P1-b candidates 1-5: excluded by the task.
- «run_diagnostic» in the SC-N7 critic and in the census row is not a symbol: the function is `red_sandbox.diagnostic`; the finding names it so.
- A related older finding exists: `execution-probes/findings/20261029-runtime-probes-ne-zapisany-do-s5.md` (title: `execution.runtime_probes` not written before S5, first run refused). Same refusal family; I judged it not a duplicate (mine is the branch where no checkout is recorded and the role can name no door), but I did not read it whole: the Lead may fold EP4-1 into it.
- Line numbers in the critics (`source_exclusions.py:805/:890`, `execution_request.py:2786-2792`) were re-read on this base (2cf488ad); the findings quote the base lines.

## Duplicate check (siblings: none -- each line placed once)

`git grep -i -c -E "check_bug_drafts|no_run_target|k1g|mask_secret_ref|url_candidates|mine_refused|stand_confirm|run_diagnostic|\.diagnostic" origin/main -- plans/piles` hit only older rows/findings on other topics (closed batches, B-rows, the two related notes above); positive control `git grep -i -c "FV1-24" origin/main -- plans/piles` found live-run-fvf README, batch-1 and findings. No existing row duplicates a line above.

## Witness (verbatim)

`( cd C:/QAFactory/forge-repo/.claude/worktrees/rows-w14 && python tools/piles.py check --all )`, last lines:
```
(д) form: ok (33 piles, 103 batches)
(е) findings: ok (1073 findings read, 0 dated from 2026-10-13 on are orphans, 152 older are the baseline)
piles check: note: the untracked pile(s) driver-hosts, execution-probes, live-run-fvf are judged here, a commit does not judge them (B.2)
piles check: ok
```
(The first run, before the «## Бриф» section was added to the new batch 4, ended `(д) form: RED -- plans/piles/execution-probes/batch-4-vhodyashchie.md: an untaken batch has no «## Бриф» heading`; fixed.)

`( cd C:/QAFactory/forge-repo/.claude/worktrees/rows-w14 && python -m pytest tools/test_pile_cards_contents.py -q )`:
```
........................................................................ [ 53%]
...............................................................          [100%]
135 passed in 4.63s
```
(The first run had `1 failed, 134 passed`: `test_card_and_batch_headings[execution-probes]`, the same missing heading; fixed.)

## Needed beyond the manifest

`tools/piles.py` (regexes, form checks), `plans/piles/_template/batch.md`, `plans/piles/execution-probes/README.md`, `plans/piles/driver-hosts/{README.md,batch-2-*.md}`, `plans/piles/live-run-fvf/batch-1-live-run-fvf.md`, package sources to name functions (`gate_preflight.py`, `gate_brief.py`, `place_answers.py`, `report_facts.py`, `source_inventory.py`, `ticket_adapter.py`, `config_contract.py`, `execution_request.py`, `red_sandbox.py`, `driver_stage_build.py`, `question-prices.json`, `source_exclusions.py`, `device_stand.py`), `scripts/tests/test-layers.json`, `slow_tests.json`, `test_validator_class.py`, `20261114-fv1-24-bug-drafts-verdict-spec.md` plan critic review.
