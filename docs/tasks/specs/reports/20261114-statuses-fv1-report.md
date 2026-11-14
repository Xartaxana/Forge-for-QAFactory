# Statuses fv1 report (t-669, 14.11.2026)

Worktree `.claude/worktrees/statuses-fv1`, branch `wip/statuses-fv1`, base origin/main 50d9012 (the `check` run compares with 6997034: origin/main moved during the work, not merged here). Docs only: `plans/piles` and this report. Status cells set with `piles.py status ... --task t-669`; «Ход» lines by Edit. No `take`/`close`, no finding, nothing under `ai-packages/`, `tools/`, `logs/`, `DECISIONS.md`, `plans/BACKLOG.md`.

Method: every wip branch of `git branch -r` that carries a node id (`fv1*`, `fv19*`, `fv118*`, `fv130*`, `fv14*`, `fv2-*`, `of3-*`, `pile/onboarding-forge/batch-3`) tested with `git merge-base --is-ancestor <branch> origin/main`; merge commits read from `git log origin/main --merges`; wave reports read for the same lines; named commits tested one by one. Positive control for the commit-subject search (`--grep "FV1-3\b"`, same shape): finds 5f03a39, 485db3f. Beyond that, for the nodes with no branch, the same `--grep` over `-- ai-packages` found no merged code (hits for FV1-4, FV1-9, FV1-14 are only commit bodies that mention the node, which edge 1 does not accept).

## Divergences from the dispatch's belief (the dispatch said "to be CONFIRMED")

1. **FV1-18 is NOT in main.** Branches `origin/wip/fv118-n1` (3e292d7), `-n2` (e9ab582), `-n3` (6950af8), `-n4` (274b57f), `-topic` (9fc7d61), `-fix` (27a6cf4): `merge-base --is-ancestor` exit 1 for all six; `git log origin/main..origin/wip/fv118-fix` lists 7 commits; `git grep selection_by_node_id origin/main -- ai-packages/qa-factory` prints nothing (control `stamp_obligation_refs` prints hits). No wave report names fv118. Status untouched; one «Ход» line says so.
2. **FV1-30 is partly in main, not closed**: 30a and 30b N0, N1, N2, N3, N6 are merged; spec node N5 (`window_record._terminal_runs`, "queued", `fv1-30b-word-fact-downstream-spec.md:626-633`) is not. Edge 2: status stays «ожидает».
3. **FV1-19 is partly in main**: N1-N3, C1, C2 yes; N4 (19d, `driver_dispatch.handoff_ladder`, spec `fv1-19-obligation-refs-spec.md:397`, "held for Q1") no. Stays «в работе».
4. `wip/fv1-22r-n1` and `-n2`: tip = 50d9012 = origin/main (`git log origin/main..branch` is empty). They are empty branches, an ancestor of main trivially; NOT evidence of merged code. FV1-22 untouched.

## Table: every node of every open П1 batch

Open П1 batches by `backlog_tree.py`: `live-run-fvf/1`, `onboarding-forge/3`, `release-next/2`. (`live-run-fvf/2` is П2 and is not in the count.) Merge hash in the status = the merge commit.

| pile / batch | node | old | new | evidence |
|---|---|---|---|---|
| live-run-fvf/1 | FV1-1 | ожидает | ожидает | not merged: branch `worktree-agent-a02fafab496f0a9f6` commits bb2bd10, 5971ac0 are not in main (`--is-ancestor` exit 1); no remote branch |
| live-run-fvf/1 | FV1-2 | ожидает | ожидает | not merged: no branch, no commit |
| live-run-fvf/1 | FV1-3 | ожидает | **принято: 5f03a39** | wave 6 report, Merges 1: `origin/wip/fv1-3` (485db3f) -> 5f03a39; `git -C <wt> branch -r --contains 485db3f` = origin/main, origin/wip/fv1-3; `merge-base --is-ancestor 5f03a39 origin/main` exit 0 |
| live-run-fvf/1 | FV1-4 | принято: f3167f3 | (unchanged) | already принято; `wip/fv14-left` f3167f3 -> merge c9a9e6d (wave 1) |
| live-run-fvf/1 | FV1-5 | ожидает | ожидает | not merged: no branch, no commit |
| live-run-fvf/1 | FV1-6 | ожидает | ожидает | not merged: spec + plan critic only |
| live-run-fvf/1 | FV1-7 | ожидает | ожидает | not merged: no branch, no commit |
| live-run-fvf/1 | FV1-8 | ожидает | ожидает | not merged: no branch, no commit |
| live-run-fvf/1 | FV1-9 | ожидает | ожидает | not merged: spec §5 "NOT DISPATCHABLE until F-7/F-8 decided" |
| live-run-fvf/1 | FV1-10 | ожидает | ожидает | not merged: no branch, no commit |
| live-run-fvf/1 | FV1-11 | сдано | **принято: 9c6c4c0** | wave 1 report line 9: `origin/wip/fv111` (da90045) -> 9c6c4c0; `Merge wip/fv111 into main` in `git log --merges`; ancestor exit 0 |
| live-run-fvf/1 | FV1-12 | ожидает | ожидает | not merged: waits for a spec (owner's word given 13.11) |
| live-run-fvf/1 | FV1-13 | ожидает | ожидает | not merged: commit 8eb20e4 (branch `worktree-agent-aaf518a792f694a7e`) not in main (exit 1); no remote branch |
| live-run-fvf/1 | FV1-14 | ожидает | ожидает | not merged: no branch, no commit |
| live-run-fvf/1 | FV1-15 | ожидает | ожидает | not merged: no branch, no commit |
| live-run-fvf/1 | FV1-16 | ожидает | ожидает | not merged: no branch, no commit |
| live-run-fvf/1 | FV1-17 | ожидает | ожидает | not merged: spec only (`fv1-17-5-15-stand-login-spec.md`) |
| live-run-fvf/1 | FV1-18 | ожидает | ожидает | not merged: see divergence 1 (six `wip/fv118-*` branches, none an ancestor of main) |
| live-run-fvf/1 | FV1-19 | в работе | в работе | partly merged: N1-N3 `wip/fv119-n1/n2/n2fix/n3` are ancestors of `wip/fv19-30-base` (4d0ad66) -> main merge 7cf8c34 (wave 1); C1 `wip/fv19-c1` 928cac6 is an ancestor of `wip/fv19-c2` (8e70deb) -> merge 819a31f (wave 3 report Job B); N4 (19d) not merged: no branch, no commit (`git log origin/main --grep "19d\|fv119-n4"` empty) |
| live-run-fvf/1 | FV1-20 | ожидает | ожидает | not merged: no branch, no commit |
| live-run-fvf/1 | FV1-21 | принято: 4f61fb5 | (unchanged) | already принято; `wip/fv121` -> merge d04c298 (wave 1) |
| live-run-fvf/1 | FV1-22 | ожидает | ожидает | not merged: see divergence 4 (empty branches `wip/fv1-22r-n1/n2`) |
| live-run-fvf/1 | FV1-23 | ожидает | ожидает | not merged: spec only |
| live-run-fvf/1 | FV1-24 | ожидает | ожидает | not merged: no branch, no commit |
| live-run-fvf/1 | FV1-25 | ожидает | ожидает | not merged: no branch, no commit |
| live-run-fvf/1 | FV1-26 | ожидает | ожидает | not merged: no branch, no commit |
| live-run-fvf/1 | FV1-27 | ожидает | ожидает | not merged: "NOT ready for a builder" (row text) |
| live-run-fvf/1 | FV1-28 | ожидает | ожидает | not merged: no branch, no commit |
| live-run-fvf/1 | FV1-29 | ожидает | ожидает | not merged: no branch, no commit |
| live-run-fvf/1 | FV1-30 | ожидает | ожидает | partly merged: 30a `wip/fv130a` 84f91d7 -> 4d0ad66 -> 7cf8c34 (wave 1); 30b N0 `fv130b-n0`, N1 `fv130b-n1`, N2 `fv130b-n2` -> f1ecdb0 -> topic `fv130b-topic` (a7c6f06) -> merge 39be4b7 (wave 5); N3 `fv130b-n3` -> d01c2a5; N6 `fv130b-n6` -> eb86925; N5 not merged (spec: "queued, not in this batch"; no branch). All six branches: `--is-ancestor origin/main` exit 0. Edge 2: stays |
| onboarding-forge/3 | OF3-1 | ожидает | ожидает | partly merged (spec t-129 has parts a-f): a e61efb8 + e20c3a2, b 6c5a8a3 (merge 041bb5e), d 86510cb (684de7e), e 2bbfce4 (27ff9fc) -> main by PR #3 merge 0ae2810; c 6fbeb28/38de220/aefde8b (merge 166d4be) -> main by PR #5 merge b0d6c3a; all `--is-ancestor` exit 0; f NOT in main (`git log origin/main -- .../knowledge-read-baseline.json .../changelog.d/t-129-of3-1f.md` empty; `ls-tree` shows changelog fragments a-e only) |
| onboarding-forge/3 | OF3-2 | ожидает | ожидает | not merged: `origin/wip/of3-2-k6` (e02ee1f, cab5f89) not an ancestor; main carries specs only (14e250c, 3eee647, e60cf20, 5c16666) |
| onboarding-forge/3 | OF3-3 | ожидает | ожидает | not merged: no branch, no commit (`--grep "OF3-[2-6]"` finds only the OF3-2 specs and 028733f) |
| onboarding-forge/3 | OF3-4 | ожидает | ожидает | same |
| onboarding-forge/3 | OF3-5 | ожидает | ожидает | same |
| onboarding-forge/3 | OF3-6 | ожидает | ожидает | same |
| release-next/2 | RN2-1 ... RN2-11 | принято (all 11) | (unchanged) | already принято with hashes; not in the open-node count |

Batch headers and card rows: not touched (no `take`/`close`; `live-run-fvf` README repeats no node status, only batch-level «ожидает»).

## Count of П1 nodes, `backlog_tree.py` (counted with a script over `piles[].batches[]` with `prio` П1, status not closed; the tool's `counts.П1` equals the total)

| | before | after |
|---|---|---|
| ожидает | 32 | 31 |
| сдано | 1 (FV1-11) | 0 |
| в работе | 1 (FV1-19) | 1 (FV1-19) |
| total | 34 | 32 |

(before: `Counter({'ожидает': 32, 'сдано': 1, 'в': 1})`; after: `Counter({'ожидает': 31, 'в': 1})`)

## «Ход» lines added (one per batch)

live-run-fvf/1 (FV1-3, FV1-11 moved; FV1-19, FV1-30 parts with hashes; FV1-18 not merged); onboarding-forge/3 (OF3-1 parts a-f, OF3-2).

## Questions for the Lead

1. FV1-30: is N5 (`_terminal_runs` alias split) part of the FV1-30 node? The spec calls it "queued, not in this batch" and says the pile line is "to be written by the Lead", but edge 2 reads "every sub-node named in its spec". If it is outside, FV1-30 closes with `piles.py status live-run-fvf 1 FV1-30 --set принято --hash eb86925 --task <t>` (eb86925 = last merge of the node). If it is inside, N5 needs its own row.
2. FV1-30 and OF3-1 are mostly merged but their only legal cell words are «ожидает» or «в работе»; I kept «ожидает» per edge 2 (same open question as in the w4 report, TQ2-1/CL4-1). Move to «в работе»?
3. FV1-18 (divergence 1): six topic branches are unmerged on origin. Is a merge pending in a wave, or did the Lead mean another node?

## Needed beyond the manifest

`plans/piles/onboarding-forge/batch-3-znaniya-o-proekte-fazy-1-6.md` (the third open П1 batch), `docs/tasks/specs/t-129-of3-1-knowledge-catalog.md` (part list), `docs/tasks/specs/20261113-fv1-19-obligation-refs-spec.md`, `...-fv1-19-binding-currency-spec.md`, `...-fv1-30b-word-fact-downstream-spec.md` (sub-node lists), `plans/piles/release-next/batch-2-*.md`.

## Witness (verbatim)

`( cd /c/QAFactory/forge-repo/.claude/worktrees/statuses-fv1 && python -B tools/piles.py check --all )`, lines other than the baseline WARN:
```
(в) frozen: ok (10 taken batch(es) on origin/main; every other batch is new or not yet taken: free)
(г) backlog: ok (frozen (compared with HEAD))
(д) form: ok (33 piles, 102 batches)
(е) findings: ok (1040 findings read, 0 dated from 2026-10-13 on are orphans, 152 older are the baseline)
piles check: ok
```
(the (б) line: `ok (10 active batches; ...)`; the (е) WARN is the 152-finding baseline.)

`( cd ... && python -m pytest tools/test_pile_cards_contents.py -q )`: `135 passed in 3.70s`.

`piles.py status` outputs:
```
piles status: live-run-fvf/1 FV1-3 set to принято: 5f03a39 (t-669). Next:
piles status: live-run-fvf/1 FV1-11 set to принято: 9c6c4c0 (t-669). Next:
```
