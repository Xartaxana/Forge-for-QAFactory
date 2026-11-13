# Report: queue lines of five critic verdicts filed as pile findings

Worktree `.claude/worktrees/findings-q`, branch `wip/findings-q`, base origin/main 819a31f. Docs only; no code, no taken batch, no B-id (`id: —`).
Commit 1: 6679b89 (findings, batch rows, README rows). Commit 2: this report.

## Table: verdict line -> finding -> pile -> batch row -> README row

Finding files are under `plans/piles/<pile>/findings/`. Batch rows are new nodes in an UNTAKEN batch (status «ожидает»). README rows are in the pile's «Содержание» table.

| Verdict line | Finding file | Pile | Batch row | README row |
|---|---|---|---|---|
| CL4-1 Q1 | `20261113-neizvestnoe-zavisanie-nazvano-stalled-pri-stalled-null.md` | collect | `batch-4-cl3-9-ochered.md` CL4-2 | yes (пачка 4, CL4-2) |
| CL4-1 Q2 | `20261113-priem-pechataet-where-why-bez-clean-i-spisok-bez-slovarej-kak-nol.md` | collect | `batch-4-cl3-9-ochered.md` CL4-3 | yes (пачка 4, CL4-3) |
| TQ2-1 Q1 | `20261113-chitateli-kolonki-tablicy-rukami-vne-critic-rollcall.md` | test-code-quality | `batch-2-sliyanie-kejsov-i-chitateli.md` TQ2-2 | yes |
| TQ2-1 Q2 (F7) | `20261113-narezka-okon-derzhit-gruppy-slijaniya-i-c12-dlya-legacy.md` | test-code-quality | batch-2 TQ2-3 | yes |
| TQ2-1 Q3 | `20261113-case-concern-lines-71-stroka-mertvaya-rabota-i-prichina-bez-granicy.md` | test-code-quality | batch-2 TQ2-4 | yes |
| FV1-30b F5 remainder (three splitters) + fix report `_record_s5_word_passes` (fourth reader) | `20261113-tri-razbiratelya-id-nahodki-i-chetvyortyj-chitatel-strok-slova.md` (one file, "one fact, several readers") | live-run-fvf | `batch-2-live-run-fvf.md` FV2-10 | yes |
| FV1-30b F8 | `20261113-left-with-you-pod-b-ne-odna-stroka-dannyh-build-left-items.md` | live-run-fvf | batch-2 FV2-11 | yes |
| FV1-30b Axis 29 (`_record_person_pass` adopter) | `20261113-record-person-pass-pishet-jsonl-mimo-hooklib-append-jsonl-line.md` | live-run-fvf | batch-2 FV2-12 | yes |
| P1-b N1 F9 + F10 (two clones with a survivor, one file) | `20261113-perepis-vyhodov-draivera-dva-klona-chitatel-json-i-hesh-prompta.md` | live-run-fvf | batch-2 FV2-13 | yes |
| P1-b N1 F12 | `20261113-perepis-vyhodov-draivera-dolgi-lead-n-l-i-put-ci.md` | live-run-fvf | batch-2 FV2-14 | yes |
| Lead line (run_suite `executor_unavailable`, story_budget `STORY BUDGET`) | `20261113-run-suite-i-story-budget-bez-zapisi-v-reestre-otkazov-klass-po-route.md` | live-run-fvf | batch-2 FV2-15 | yes |

Files written: 11 findings, 3 batch files (rows appended), 3 README files (rows appended), this report.

## Pile choice (how each was found; grep case-insensitive, positive control on the same shape)

- CL4-1: id found in `collect/batch-4-cl3-9-ochered.md` and `collect/README.md` (batch 4 status «ожидает», untaken).
- TQ2-1: id found in `test-code-quality/batch-2-...` (untaken) and README. The Q2 finding was verified missing first: no `split_windows|case_groups` finding exists in the piles.
- FV1-30: id found in `live-run-fvf/batch-1-live-run-fvf.md` (row FV1-30, untaken) and `README.md`. I filed in `batch-2-live-run-fvf.md` (also untaken), not batch-1, because batch-2's own text says "findings of the critics' queues of 13.11 land here" (nodes FV2-n, nine critic-queue findings already there). Judgment call; moving a row to batch-1 is a one-line edit.
- P1-b: the literal id `P1-b` (with hyphen) is in NO pile file (positive control `P1-a`, same shape, finds files). The only pile files that carry the P1-b spec are two `live-run-fvf` findings quoting `docs/tasks/specs/20261113-p1b-dry-story-spec.md`, and that spec itself (R-L5, section 6) puts its finding in `live-run-fvf`. I filed the P1-b lines in `live-run-fvf/batch-2` on that basis. This is a judgment call against the dispatch's literal rule ("pile whose files carry P1-b"); the Lead may move them. Its nodes N0-N4 have no pile row, so dependencies are written as "P1-b N1/N2/N3".

## Verification output (verbatim; after the last edit to pile files; from the worktree via a `( cd ... )` subshell)

Command: `python tools/piles.py check --all`
```
(а) placement: ok (296 open ids, 136 closed, 190 findings, 165 batch-row members)
(б) overlap: ok (10 active batches; 45 pair(s) of one developer not compared ...)
(в) frozen: ok (10 taken batch(es) on origin/main; every other batch is new or not yet taken: free)
(в) frozen: compared with origin/main 819a31f
(г) backlog: ok (frozen (compared with HEAD))
(д) form: ok (33 piles, 101 batches)
(е) findings: ok (1026 findings read, 0 dated from 2026-10-13 on are orphans, 152 older are the baseline)
(е) findings: WARN: 152 finding(s) dated before 2026-10-13 or undated (69) are named in no batch file of their pile (the baseline ...; not blocking) ...
piles check: note: the untracked pile(s) collect, live-run-fvf, test-code-quality are judged here, a commit does not judge them (B.2)
piles check: ok
exit=0
```

Command: `python -m pytest tools/test_pile_cards_contents.py -q`
```
........................................................................ [ 53%]
...............................................................          [100%]
135 passed in 2.79s
```

The commit hook ran the same checks on the staged tree: `piles check: ok`, `new findings 11 (all attributed)`, `(в) frozen: ok (0 taken batch(es) ...)`, `ESCAPE ALLOWLIST OK`, indexes up to date; commit accepted with no `tier:` demand and no `piles-skip:` used.

## Key-presence witness (script attached in FULL, not committed; run from the scratchpad)

Keys are the verdict's line ids / quoted phrases, taken verbatim from the verdict files before the run. It checks: key in its finding file, finding file name in its batch file, in its README. Two negative controls (ids deliberately absent: `CL4-1 Q9`, `Q9 (no such line)`) must FAIL; the script exits 0 only if exactly those two fail.

```python
import sys, pathlib
P = pathlib.Path(sys.argv[1]) / "plans" / "piles"
# (verdict line id quoted verbatim as it appears in the finding's "от:" line, finding path, batch file, README)
ROWS = [
 ("Q1 (collect, M2 class; FR-41, FR-10)", "collect/findings/20261113-neizvestnoe-zavisanie-nazvano-stalled-pri-stalled-null.md", "collect/batch-4-cl3-9-ochered.md", "collect/README.md"),
 ("Q2 (collect intake; spec §7, confirmed)", "collect/findings/20261113-priem-pechataet-where-why-bez-clean-i-spisok-bez-slovarej-kak-nol.md", "collect/batch-4-cl3-9-ochered.md", "collect/README.md"),
 ("Q1 (N5 siblings, outside owns)", "test-code-quality/findings/20261113-chitateli-kolonki-tablicy-rukami-vne-critic-rollcall.md", "test-code-quality/batch-2-sliyanie-kejsov-i-chitateli.md", "test-code-quality/README.md"),
 ("Q2 (F7, decided (a))", "test-code-quality/findings/20261113-narezka-okon-derzhit-gruppy-slijaniya-i-c12-dlya-legacy.md", "test-code-quality/batch-2-sliyanie-kejsov-i-chitateli.md", "test-code-quality/README.md"),
 ("Q3 (code quality, queue)", "test-code-quality/findings/20261113-case-concern-lines-71-stroka-mertvaya-rabota-i-prichina-bez-granicy.md", "test-code-quality/batch-2-sliyanie-kejsov-i-chitateli.md", "test-code-quality/README.md"),
 ("«F5» (остаток после фикс-раунда)", "live-run-fvf/findings/20261113-tri-razbiratelya-id-nahodki-i-chetvyortyj-chitatel-strok-slova.md", "live-run-fvf/batch-2-live-run-fvf.md", "live-run-fvf/README.md"),
 ("«F8»", "live-run-fvf/findings/20261113-left-with-you-pod-b-ne-odna-stroka-dannyh-build-left-items.md", "live-run-fvf/batch-2-live-run-fvf.md", "live-run-fvf/README.md"),
 ("«Axis 29»", "live-run-fvf/findings/20261113-record-person-pass-pishet-jsonl-mimo-hooklib-append-jsonl-line.md", "live-run-fvf/batch-2-live-run-fvf.md", "live-run-fvf/README.md"),
 ("«F9 — clone, queued»", "live-run-fvf/findings/20261113-perepis-vyhodov-draivera-dva-klona-chitatel-json-i-hesh-prompta.md", "live-run-fvf/batch-2-live-run-fvf.md", "live-run-fvf/README.md"),
 ("«F10 — seam with N2 (node N2)»", "live-run-fvf/findings/20261113-perepis-vyhodov-draivera-dva-klona-chitatel-json-i-hesh-prompta.md", "live-run-fvf/batch-2-live-run-fvf.md", "live-run-fvf/README.md"),
 ("«F12 — owed by the Lead, not the builder»", "live-run-fvf/findings/20261113-perepis-vyhodov-draivera-dolgi-lead-n-l-i-put-ci.md", "live-run-fvf/batch-2-live-run-fvf.md", "live-run-fvf/README.md"),
 ("the refusal registry has no record for the texts of run_suite", "live-run-fvf/findings/20261113-run-suite-i-story-budget-bez-zapisi-v-reestre-otkazov-klass-po-route.md", "live-run-fvf/batch-2-live-run-fvf.md", "live-run-fvf/README.md"),
 # NEGATIVE CONTROLS: ids deliberately absent
 ("CL4-1 Q9", "collect/findings/20261113-neizvestnoe-zavisanie-nazvano-stalled-pri-stalled-null.md", "collect/batch-4-cl3-9-ochered.md", "collect/README.md"),
 ("Q9 (no such line)", "test-code-quality/findings/20261113-case-concern-lines-71-stroka-mertvaya-rabota-i-prichina-bez-granicy.md", "test-code-quality/batch-2-sliyanie-kejsov-i-chitateli.md", "test-code-quality/README.md"),
]
bad = 0
for key, f, b, r in ROWS:
    fp = P / f
    ok_key = fp.is_file() and key in fp.read_text(encoding="utf-8")
    ok_batch = (P / b).read_text(encoding="utf-8").count(fp.name) >= 1
    ok_readme = (P / r).read_text(encoding="utf-8").count(fp.name) >= 1
    status = "OK  " if ok_key and ok_batch and ok_readme else "FAIL"
    if status == "FAIL":
        bad += 1
    print(f"{status} key={key!r} in-finding={ok_key} in-batch={ok_batch} in-readme={ok_readme} file={fp.name}")
print(f"failures: {bad} (expected 2: the two negative controls)")
sys.exit(0 if bad == 2 else 1)
```

Run: `python -B -I <scratchpad>/keypresence.py <worktree>` -> exit 0. Output (key text garbled only by the console codepage; the match itself is on UTF-8 text):
```
OK   key='Q1 (collect, M2 class; FR-41, FR-10)' in-finding=True in-batch=True in-readme=True
OK   key='Q2 (collect intake; spec §7, confirmed)' in-finding=True in-batch=True in-readme=True
OK   key='Q1 (N5 siblings, outside owns)' in-finding=True in-batch=True in-readme=True
OK   key='Q2 (F7, decided (a))' in-finding=True in-batch=True in-readme=True
OK   key='Q3 (code quality, queue)' in-finding=True in-batch=True in-readme=True
OK   key=<F5 (остаток после фикс-раунда)> in-finding=True in-batch=True in-readme=True
OK   key=<F8> in-finding=True in-batch=True in-readme=True
OK   key=<Axis 29> in-finding=True in-batch=True in-readme=True
OK   key=<F9 - clone, queued> in-finding=True in-batch=True in-readme=True
OK   key=<F10 - seam with N2 (node N2)> in-finding=True in-batch=True in-readme=True
OK   key=<F12 - owed by the Lead, not the builder> in-finding=True in-batch=True in-readme=True
OK   key='the refusal registry has no record for the texts of run_suite' in-finding=True in-batch=True in-readme=True
FAIL key='CL4-1 Q9' in-finding=False in-batch=True in-readme=True    <- negative control: reports failure, as required
FAIL key='Q9 (no such line)' in-finding=False in-batch=True in-readme=True    <- negative control
failures: 2 (expected 2: the two negative controls)
```

## NOT FILED -- why

1. **CL4-1 Q3 (`experiments/measurers/compare.py:266-284` `driver_report` counts bookkeeping rows as calls).** The Lead's rule: add to the queued `report_run.journal` node/finding. No such node exists in any pile: case-insensitive grep for `report_run` over `plans/piles` finds only `forge/findings/B-162`, `B-173`, `B-267`, `forge/README.md`, `cost-dashboard/README.md` (old, unrelated: hard run tables, `plan_rows`, copies; positive control = the same call finding those files). The CL4-1 spec section 7 names `report_run.journal` only as a "candidate finding". It was never filed, so Q3 has nothing to join. Not invented as a new finding in an arbitrary pile. Lead to place; suggested content: one finding "measurers count every non-conductor/any journal row as a call" with both sites (`report_run.py:141-158`, `compare.py:266-284`; rows `window_round`, `process`, `launched`, `gate_repair`), pile candidates `forge` (measurers, B-162 family) or `cost-dashboard`; axis 6.
2. **T1 lines Q-a ... Q-j (the "told before work" revision verdict).** No pile carries the told-before-work nodes: case-insensitive grep `T1a|T1-0|told.before.work|told_before|tbw` over `plans/piles` of the worktree, of `read-main` (12317b6), of the root checkout and of ten other worktrees: 0 hits (positive control: `CL4-1`, same shape, finds `collect/batch-4`). The verdict's own node ids (T3a, T2, T1r, T10) belong to the parent spec `docs/tasks/specs/20261113-told-before-work-mechanism-spec.md`, not to any batch. The Lead places them. Lines for placement (verbatim ids): Q-a runtime of `told_world` (double wide scan, `test_stage_joints.py:775-776`; node `<T10 or a B-155-class node>`); Q-b `stage_joints.rows_for` returns `[]` on unreadable rows (`stage_joints.py:526-528`, AR-28, node T3a); Q-c `refusal_registry.py:1404` pass-through records typed `walk_error` (node T2); Q-d duplication (`role_set` vs `_row_names`, `measure_untold` third copy of the `units_of` flip rule, `_hand_cards` second reader of `ahead-cards.json`, `exit_members`/`_passthrough` both read `own`); Q-e `_row_requirement` over 60 lines with a nested lambda (`stage_joints.py:836-896`); Q-f `covered()` sub-id rule broader than parent C14 (node T1r); Q-g `legacy_legs` and `unsited` ceiling-only (Lead choice); Q-h commit axis block not an enumeration (calibration note); Q-i conductor-only group read from a free-text `note` by `GROUP_RE` (owners T4/T9a/T9c); Q-j T1a report text says owner `data` for `archive_task.py::cmd_archive`, the file says `intent` (report text wrong, data right). F1-F3 of that verdict are before-merge fixes, not queue lines, and were not in scope.
3. **FV1-30b F10 (queue part).** Not filed: the fix report (`.claude/worktrees/fv130b-fix/docs/tasks/specs/reports/20261113-fv130b-topic-fix-report.md`) states both queue items done in the fix round: the two shipped-value checks dropped from `row_fv130b_n1_the_not_run_section_and_the_field_rows`, and a test-budget reason line written for N1 and N2. The only residue is that the ~435 vs ~259 and ~245 vs ~205 test-to-product line ratios were not reduced ("Neither count is reduced by this round"), which is not a fix line. Lead may overrule if the ratio itself should be queued.
4. **Not requested, noticed:** the fix report's sibling "the name `word_passed` now exists in three shapes on three carriers (window-instance list, trace-row dict, coverage-item bool)" ("Lead to judge"). I mentioned it as a one-line pointer inside the FV2-10 finding (item 3) and filed no node. Also `plans/piles/live-run-fvf/README.md` «Пачки» row for batch 2 still reads "FV2-1…FV2-9" (now FV2-1…FV2-15); the dispatch's owns allow appending «Пачки» rows only when a new batch is opened, so I did not edit it.

## Directions decided by the verdict vs. marked "по рекомендации критика, Lead подтвердит" / forks returned

- CL4-1 Q1: first variant of the verdict (classify word sites on the item) as the recommendation; the fold-in (`looped` missing: `null` vs NO) is a fork the verdict did not resolve, written as "executable by the recommendation, Lead confirms"; frozen quarantined pins are the Lead's decision.
- CL4-1 Q2: the exact text for the non-dict-only list is not given by the verdict; the neighbouring spec form `<label>: unreadable (<type>)` is named, fork returned if it does not fit.
- TQ2-1 Q1: the error direction per site is the verdict's own demand and is returned to the Lead/designer before the builder (not chosen).
- TQ2-1 Q2: direction (a) chosen by the Lead in the spec (F7); the finding requires a plan to the owner and a plan critic before the designer (new-idea steps 4, 6).
- FV1-30b splitters: survivor module not chosen by the verdict; `scripts/contract.py` is the fix report's example, marked "Lead confirms". Fourth reader direction (rows through the same memo) is mine as a proposal, marked as such.
- FV1-30b F8: verdict's first option (amend the F4 sentence) written as the recommendation; second option kept as a separate Lead decision.
- P1-b F9/F10: survivors named by the verdict. F12: the item list is the verdict's; the CI-path item is a fork for the Lead pile.
- Lead line (run_suite, story_budget): class word not given; recommendation from the verdict (Q1) is "gate" as the natural reading, Lead's call.

## Needed beyond the manifest

Read beyond the basket: `docs/tasks/specs/20261113-tq2-1-revision-option-c-spec.md` (F7 text, section 7), `docs/tasks/specs/20261113-cl4-1-collect-stalled-looped-spec.md` (report_run queue), `docs/tasks/specs/20261113-p1b-dry-story-spec.md` (pile placement, N-L), `plans/piles/live-run-fvf/batch-2-live-run-fvf.md` and README, `plans/piles/forge/findings/` (form precedent), other worktrees' `plans/piles` (negative greps), `hooklib.append_jsonl_line` and `check_delivery.build_left_items` locations in the worktree.

## Siblings / class noticed (rule 5)

- The queue lines of other 13.11 verdicts may also live only in review files (this batch covered five). A check "every `Q*`/queue line of `docs/tasks/specs/reviews/20261113-*.md` has a finding" would be a mechanism; not built here.
- The CL4-1 spec and verdict reference `report_run.journal` as "queued" while no finding for it exists in the piles (item 1 of NOT FILED): a "queued" word without a carrier.
