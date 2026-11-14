# t-841: K10 pay-down verdict carried into live-run-fvf batch 2

Branch `wip/k10-nodes` (from origin/main d142d1d4). Owner's word 14.11.2026: "только B1, остальное завести узлами".

## Table: verdict item -> finding file -> node id -> card row

Findings dir: `plans/piles/live-run-fvf/findings/`. Card rows: `plans/piles/live-run-fvf/README.md`, table "Содержание" (last six rows). One finding per item group (edge 5).

| verdict item | finding file | node | card row |
|---|---|---|---|
| B1 (K1b row exit) + S1 | `20261114-k10-k1b-uzel-i-uslovie-vyhoda-vremennoj-stroki-code-critic.md` | FV2-79 | yes (first of six) |
| S2 | `20261114-k10-testovye-pravki-s2-s3-s5.md` | FV2-80 | yes (shared row) |
| S3 | same | FV2-81 | same row |
| S5 | same | FV2-82 | same row |
| S4 + S7 (one function, one fix) | `20261114-extra-record-lines-povtor-obhoda-zapisej-i-hvost-pri-isklyuchenii.md` | FV2-83 | yes |
| S6 | `20261114-pechat-request-error-bez-told-fields-scheduler-i-probe.md` | FV2-84 | yes |
| analog (red-sandbox world builder, Queue line 3) | `20261114-obshchij-stroitel-mira-red-sandbox-v-dvuh-testah.md` | FV2-85 | yes |
| Q1 stand/begin fixture | `20261114-ochered-q1-q7-spek-k10-paydown.md` | FV2-86 | yes (shared row, FV2-86...92) |
| Q2 duplicates | same | FV2-87 | same row |
| Q3 scout `controller:*` | same | FV2-88 | same row |
| Q4 census `check_findings` | same | FV2-89 | same row |
| Q5 L12 prose pass | same | FV2-90 | same row |
| Q6 code detector "a row above the measured U is red" | same | FV2-91 | same row |
| Q7 Appendix A | same | FV2-92 | same row (owner yes/no) |

Also written: a "Ход" line (t-841) in the batch file (placed before the two t-838 "слито без строки-узла" lines, not at the very tail; minor ordering, "Ход" is free text) and two entries in README "Вопросы владельцу" (S1, Q7).

## Forks returned as questions (PROJECT.md p. 11)

- S1 (FV2-79): does an id also printed at an L site count "P only"? The verdict gives no direction ("Lead decides"). I wrote it as an owner question with the recommendation derived from spec K1b-E3/E4 (a carry list errs toward MORE ids): option A = does not count, both ids stay on the code-critic page; cost = K1b may STOP at E7. Node executable on A. This recommendation is derived from the spec invariant, not from the critic: please confirm.
- Q7 (FV2-92): owner yes/no, no code until answered.

## Items covered elsewhere / undone

- Nothing undone. No duplicates: FV2-43/FV2-44 do not name `execution_scheduler.py` 709 or `onboarding_probe.py` 279 (S6). Greps of check_findings, run_suite:begin, exit_gate:digest, native_headroom, s5_plan_gaps, _extra_record_lines, world builder, _records_in, Appendix A over plans/piles: no node subject (only unrelated execution_scheduler/onboarding_probe hits in other piles; EP4-2 concerns another class in `test_red_sandbox_diagnostic.py`). Positive control: grep for the same shape hit execution_scheduler/onboarding_probe in codex/execution-* cards. Narrower re-greps in codex and onboarding-forge (where long lines were omitted) returned empty; I did not run a separate positive control for that exact call.
- FV2-79 exit condition: "native_headroom.qa-code-critic deleted (U <= 68,400) or lowered to U with STOP per K1b-E7"; a standing row at close = acceptance refusal (verdict said "deleted or lowered").
- Owns/file names for Q1, Q2, Q5, S6 second site are best candidates named in the nodes; designer to confirm (Q1 and Q5 say so in the finding).

## Neighbors noticed (rule 5)

- Same class (a spec-only promise with no node): none beyond the verdict's own list. S4 and S6 share `test_detector_verdict.py` with FV2-44; ordering is stated per node by function lists in `owns`.

## Witness (DoD)

Before (origin/main d142d1d4):
```
(е) findings: ok (1100 findings read, 0 dated from 2026-10-13 on are orphans, 152 older are the baseline)
(е) findings: WARN: 152 finding(s) dated before 2026-10-13 ... (not blocking)
piles check: ok
```
After (worktree with the changes):
```
python -B tools/piles.py check --all
(е) findings: WARN: 152 finding(s) dated before 2026-10-13 or undated (69) are named in no batch file of their pile (the baseline ...; not blocking) ...
piles check: note: the untracked pile(s) live-run-fvf are judged here, a commit does not judge them (B.2)
piles check: ok

python -m pytest tools/test_pile_cards_contents.py -q
135 passed in 1.87s
```
Note: the after run was before `git add`, hence the "untracked" note; rerun after commit is below.
