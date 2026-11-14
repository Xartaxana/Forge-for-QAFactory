# t-756 — queue lines of the night code critics became findings with rows (pile bookkeeping)

Worktree `.claude/worktrees/queue-n14`, branch `wip/queue-n14` (cut from origin/main bc86050). Docs only: findings, batch rows, card rows. No package file, no code, no test, no B-id (`id: —`), no taken batch touched.

## Table: source line -> finding -> pile -> batch row -> merged-with

Finding files are under `plans/piles/<pile>/findings/` (date prefix 20261114). `LRF` = `live-run-fvf` batch 2 (untaken, appended); `forge` batch 7; `TR` = `thinking-roles`; `TQ` = `test-code-quality`.

| source line | finding file | pile | batch row | merged-with |
|---|---|---|---|---|
| S1 Q1 (A-5, A-6 rows) | `fv1-23-a5-a6-uzly-bez-stroki-v-pachke` | live-run-fvf | FV2-28 (A-5), FV2-29 (A-6) | A-5 and A-6 in one finding (one class: residual nodes of FV1-23 with no carrier) |
| S1 Q2 | `code-repos-koren-vyshe-proekta-obyavlyaet-vsyo` | live-run-fvf | FV2-30 | - |
| S1 Q3 (`_safe_rel` -> `declared_place` syntax half) | NO new file | execution-report (outside owns) | existing node ER2-6 | carried by `execution-report/batch-2-execution-report-tails.md:81` (ER2-6, untaken: one guard `runtime_paths.relative_problem` instead of `_textual_problem` and `_safe_rel`; finding `execution-report/findings/20261102-odin-ohrannik-otnositelnogo-puti-i-sosedi-tq1-21.md`). See "For the Lead" 3: `declared_place` is a NEW copy not named there |
| S1 Q4 (census class safety?) | `klass-otkaza-record-source-safety-ili-xref` | live-run-fvf | FV2-31 (Lead decision; default stays `xref`) | - |
| S1 Q5 | `registr-kornya-code-repos-na-windows-vtoraya-zapis-odnogo-fajla` | live-run-fvf | FV2-32 | - |
| S1 Q6 | `linked-documents-i-record-source-berut-raznye-korni-spiska` | live-run-fvf | FV2-33 | - |
| S2 Q1 (skill road records no register_gaps) | `skill-doroga-ne-pishet-register-gaps` | thinking-roles (chosen: verdict names "qa-story pile or skill-retirement node", no such pile exists; role/skill-road line -> the dispatch default) | TR5-4 (batch 5) | - |
| S2 Q2 (census blind spot of driver Refusal) | `perepis-slepoe-pyatno-otkazy-draivera-refusal` | test-code-quality (chosen: census line -> dispatch default) | TQ2-5 (batch 2) | - |
| S2 Q3 (`exploratory_findings.read` directory as empty) | `chitatel-chitaet-nechitaemyj-nositel-kak-pustoj-register-i-questions` | live-run-fvf (chosen: Q4's verdict text names "a node of the question-register pile" and `question_register.py` is in FV1-3/FV1-9 of this pile; Q3 names no pile and is the same AR-28 class, so it rides with Q4) | FV2-40 | merged with S2 Q4 |
| S2 Q4 (`raise_from_handoff` non-list) | same file as Q3 | live-run-fvf | FV2-40 | merged with S2 Q3 |
| S2 Q5 (CL-NS) | `cl-ns-detektor-roli-bez-shell-na-karte-komand` | thinking-roles (chosen: role-commands cards of roles -> dispatch default) | TR6-3 (batch 6, P3) | - |
| S2 Q6 (F-R0 owner question) | `f-r0-dve-dorogi-k-odnomu-registru-vopros-vladeltsu` | thinking-roles (chosen: role line -> dispatch default) | TR5-5 (batch 5; also a line in the card's "Вопросы владельцу") | - ("Решение владельца нужно: да", recommendation (a), executable by it) |
| S3 N1 (labelling window forgets `next:S3`) | `told-next-s3-metka-chitaetsya-i-zabyvaetsya-oknom-razmetki` | live-run-fvf | FV2-34 ("critic on plan before code", it changes the key's meaning) | - |
| S3 Q1 (third copy of the slice parse) | `told-from-tretya-kopiya-razbora-json-sreza` | live-run-fvf | FV2-35 | - |
| S3 Q3 (two red rows of `test_place_session.py`) | `karantin-dve-krasnye-stroki-test-place-session` | live-run-fvf | FV2-36 (pointer row, owner the td-15 quarantine node, no fix) | - |
| S4 Q1 (count on merge and `--all`) | `order-known-schyot-ne-pechataetsya-na-merge-i-all` | forge | FG7-34 (batch 7) | - |
| S4 Q2 (regex beside `CLOSES_RE` only if a code reader appears) | `order-known-chitatel-ryadom-s-closes-re-tolko-pri-kodovom-chitatele` | forge | FG7-35 (CONDITIONAL node, marked in the cell) | - |
| S5 F4+F5+F6+F7 | `proba-stenda-slova-blocked-by-odnoj-dorogoj` | live-run-fvf | FV2-37 | F4, F5, F6, F7 are ONE finding and ONE node (the verdict folds them) |
| S5 F8 (login retry text) | `login-retry-sprashivaet-cheloveka-o-tom-chto-vladelec-dal-roli` | live-run-fvf | FV2-38 (Lead decision within FV1-15; depends on FV1-15, FV1-28) | - |
| S5 F9 (two more "did not answer" carriers) | `did-not-answer-eshyo-dva-nositelya-s0-md-i-stand-answers` | live-run-fvf | FV2-39 | - |
| S6 PN-1 | `call-told-bez-dorog-roli-tolko-pri-povtore` | live-run-fvf (T1r nodes live in the mechanism spec; the T1 findings of the same topic already sit in this pile as the fallback, e.g. FV2-24) | FV2-41 (CONDITIONAL: only on recurrence of class B1) | - |
| S6 PN-3 | `zhivoj-schyot-otkazov-er-rs-po-id-na-progone` | live-run-fvf | FV2-42 (Lead, measurement; the `live-runs` row is the Lead's at acceptance) | - |
| S6 s1a-report "Questions" 2 + "Analogs noticed" 1 and 3 | `bare-sajty-er-rs-bez-id-vne-uzla-s-1a` | live-run-fvf | FV2-43 | three lines, one class (sites left bare outside S-1a) |
| S6 s1a-report "Analogs noticed" 2 | `pechat-otkaza-profilya-obhodit-refusal` | live-run-fvf | FV2-44 | - (a different class: a printer that bypasses `refusal()`) |

Totals: 22 new finding files (live-run-fvf 16, forge 2, thinking-roles 3, test-code-quality 1); 1 line carried by an existing node (no file); 24 source lines of the dispatch list read: S1 6, S2 6, S3 3, S4 2, S5 4 (F4-F7 count as one), S6 4 (PN-1, PN-3, Questions 2, Analogs). 22 is inside the expected 15-25.

## Edges (what I did)

1. One finding per class: F4-F7 one; S2 Q3+Q4 one (same AR-28 class); S6 Questions 2 + Analogs 1/3 one; everything else separate.
2. Grep before writing, case-insensitive, under `plans/piles/`, for ~35 key words (`_safe_rel`, `declared_place`, `register_gaps`, `raise_from_handoff`, `CL-NS`, `F-R0`, `told_from`, `test_place_session`, `order-known`, `decide_merge`, `blocked_by`, `_word_of_item`, `probe_reason`, `login_not_tried`, `call_told`, `s6_close_from_state`, `unknown_profile_refusal`, `window_first`, `SECRET_QUERY_RE`, `_listable`, ...). Hits only for `_safe_rel` (ER2-6, carried: see table), `config_contract`/`code_repos`/`onboarding_probe`/`decide_merge` (old unrelated findings), `td-15` (the quarantine finding `package-ci/findings/20261113-krasnoe-v-karantine-ne-razobrano-dva-fajla.md` covers two other files, not `test_place_session`), `judgment-census` (no driver-Refusal blind spot in any hit; read). Positive controls, once per pile: `told_world` -> live-run-fvf finding found; `journal_validator` -> forge found (`batch-1-foundation.md`); `critic_rollcall` -> test-code-quality found; `thinking` -> thinking-roles found.
3. Every pile had an untaken batch: live-run-fvf batch 2 (batch 1 also untaken; batch 2 is where the critic queues of 13-14.11 already go), forge batch 7, thinking-roles batches 5 and 6 (by priority), test-code-quality batch 2. No new batch file opened. No taken batch edited; no `piles-skip`.
4. Direction = the critic's recommendation. A line the verdict gives no direction for became a decision/question row with executor `Lead` (FV2-31, FV2-36, FV2-38, FV2-42, TR5-5) or a `designer` node that returns the fork (FV2-33, FV2-39, TR5-4, TQ2-5).
5. Empty source: none; every named line was present. S3 Q2 and the optional `d.state = {}` line, S3 T-2, and every F-line of the verdicts (fix-round items) are not in the dispatch list and were NOT made findings (see below).

## Choices I made (each marked in the finding; reversible)

- FV2-30 (S1 Q2): verdict says "refuse, or flag"; I wrote "flag" (P1: code reports, does not stop the factory). Lead may switch to refuse.
- FV2-35 (S3 Q1): verdict says "converge on `told_from`, or a neutral helper"; I wrote `told_from` as the survivor (first named). Lead may switch.
- Pile choices where the verdict names none: S2 Q1/Q5/Q6 -> thinking-roles; S2 Q2 -> test-code-quality; S2 Q3 -> with Q4 in live-run-fvf (see table for why).
- FV2-41 and FG7-35 are CONDITIONAL nodes (the verdicts say "only on recurrence" / "only if a code reader appears"); the condition is the first words of the "Что" cell and in "Зависит от". They can be taken by mistake; the Lead may prefer to keep them out of the batch table.

## For the Lead (questions and notes, nothing decided)

1. Batch size: live-run-fvf batch 2 now holds 44 nodes (was 27; the size scale says L = 10-15, more means two batches). I followed edge 3 (append to the untaken batch). The Ход line of the batch says the Lead recuts it later.
2. Lines of the verdicts that were NOT in the dispatch list and are therefore not carried by this commit: fix-round items F1-F8 of S1, F1-F3 of S5 (F1 `no_address` mapping needs a Lead amendment of the FV1-5 card), S3 F1/Q2/T-2/optional `d.state = {}`, S4 B1/F1-F4, S2 B1/F2-F5 and the OWNER NOTICE (quarantined `test_handoff_init_author.py::test_check_verdict_unchanged_by_emptying[s4-case-critic-to-designer-*]` red because `EMPTIED_PATHS` lacks `register_gaps`; its door is the quarantine-watch owner notice, not a node).
3. S1 Q3 gets no file by edge 2, but ER2-6 names `runtime_paths.relative_problem` as the survivor and does not name `declared_place` (a new copy of the same syntax guard, from the FV1-23 branch). The pile `execution-report` is outside my owns: a one-line addition to ER2-6's "Что" is the Lead's move.
4. S5 F2 asks the owner list of quarantine reds to be corrected (`test_story_run_stand.py:40,62` are NOT red); F3 asks a changelog fix: both are fix-round items of FV1-5, not queue lines.

## Witness

DoD run 1, BEFORE the first edit (worktree untouched), `( cd C:/QAFactory/forge-repo/.claude/worktrees/queue-n14 && python -B tools/piles.py check --all )`:

```
(а) placement: ok (296 open ids, 136 closed, 190 findings, 165 batch-row members)
(б) overlap: ok (10 active batches; 45 pair(s) of one developer not compared (dev1: github-move/3 + onboarding-forge/1, dev1: github-move/3 + onboarding-forge/2, dev1: github-move/3 + onboarding-forge/3, ...; inside one developer the only guard is `owns_gate`'s WARN over live dispatches of one machine; two parallel sessions of one developer are no longer blocked by (б)))
(в) frozen: ok (10 taken batch(es) on origin/main; every other batch is new or not yet taken: free)
(в) frozen: compared with origin/main bc86050
(г) backlog: ok (frozen (compared with HEAD))
(д) form: ok (33 piles, 102 batches)
(е) findings: ok (1041 findings read, 0 dated from 2026-10-13 on are orphans, 152 older are the baseline)
(е) findings: WARN: 152 finding(s) dated before 2026-10-13 or undated (69) are named in no batch file of their pile (the baseline the calibration reads; not blocking), first 5: conductor/20261010-ci-krasnyj-test-no-real-claude-pin-do-c1-1.md, conductor/20261010-flagi-zapuska-teryayutsya-na-kazhdom-voprose.md, conductor/20261010-ledger-kritika-sbrasyvaetsya-pri-stale.md, conductor/20261010-record-gaps-chitaet-slova-cheloveka-spiskom-fraz.md, cost-dashboard/B-075-okna-s5-dlya-ne-ui-keysov-4.md
piles check: ok
```

DoD run 1, AFTER the edits (same command; exit 0). The `origin/main` ref had advanced to a8a5189 between the two runs (it printed bc86050 before); my branch is still cut from bc86050:

```
(а) placement: ok (296 open ids, 136 closed, 190 findings, 165 batch-row members)
(б) overlap: ok (10 active batches; 45 pair(s) of one developer not compared (dev1: github-move/3 + onboarding-forge/1, dev1: github-move/3 + onboarding-forge/2, dev1: github-move/3 + onboarding-forge/3, ...; inside one developer the only guard is `owns_gate`'s WARN over live dispatches of one machine; two parallel sessions of one developer are no longer blocked by (б)))
(в) frozen: ok (10 taken batch(es) on origin/main; every other batch is new or not yet taken: free)
(в) frozen: compared with origin/main a8a5189
(г) backlog: ok (frozen (compared with HEAD))
(д) form: ok (33 piles, 102 batches)
(е) findings: ok (1063 findings read, 0 dated from 2026-10-13 on are orphans, 152 older are the baseline)
(е) findings: WARN: 152 finding(s) dated before 2026-10-13 or undated (69) are named in no batch file of their pile (the baseline the calibration reads; not blocking), first 5: conductor/20261010-ci-krasnyj-test-no-real-claude-pin-do-c1-1.md, conductor/20261010-flagi-zapuska-teryayutsya-na-kazhdom-voprose.md, conductor/20261010-ledger-kritika-sbrasyvaetsya-pri-stale.md, conductor/20261010-record-gaps-chitaet-slova-cheloveka-spiskom-fraz.md, cost-dashboard/B-075-okna-s5-dlya-ne-ui-keysov-4.md
piles check: note: the untracked pile(s) forge, live-run-fvf, test-code-quality, thinking-roles are judged here, a commit does not judge them (B.2)
piles check: ok
```

Difference: findings 1041 -> 1063 (+22 = the new files, 0 orphans); the base ref line; the one added "note" about untracked pile files (they are not yet committed at that run). No new problem.

DoD run 2, `( cd C:/QAFactory/forge-repo/.claude/worktrees/queue-n14 && python -m pytest tools/test_pile_cards_contents.py -q )`:

```
........................................................................ [ 53%]
...............................................................          [100%]
135 passed in 4.06s
```
