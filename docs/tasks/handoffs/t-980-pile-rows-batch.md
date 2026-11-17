# t-980 — pile rows batch (builder report)

Task t-980, feature F19. Documents only; no package file, no spec text, no journal line, no push.

## What was done

| pile | batch | nodes | findings | card «Содержание» rows |
|---|---|---|---|---|
| `rules-debt` (new) | `batch-1-phase-2.md` («ожидает», П1) | 24 (`RD1-1`…`RD1-24`) | 24 | 24 |
| `told-before-work` (new) | `batch-1-finish.md` («ожидает», П1) | 15 (`TBW1-1`…`TBW1-15`) | 15 | 15 |
| `live-runs` (existing) | `batch-2-live-proofs.md` (untaken, «ожидает») | 4 added (`LR2-2`…`LR2-5`) | 4 added | 4 added (own group header) |
| `forge` | `batch-7-vhodyashchie-4.md` (untaken) | 0 | 0 | one `очередь:` line appended (the same line as `live-run-fvf/3` line 16, verbatim, own line before `## Бриф`) |

Every row status «ожидает»; nothing marked done. Findings: one per row, Russian, short (class, what to change, pointer to the card in the spec — not a copy).

C3 cards found in §2 of the rules-debt spec (12): C3-0, C3-a, C3-b, C3-c, C3-d, C3-e, C3-f, C3-g, C3-h, C3-i, C3-j, C3-k (matches §5's list "0, a … k"; C3-i is one card for three rows, C3-b one for two rows).

Rules-debt rows: C1, C2, C3 x12, C4, C5, S9, S10, FL1, FL2, FL4, FL9, S1b, plus B337 = 24. Live-runs rows: R9/C1 -> LR2-2, C3-j -> LR2-3, C3-b -> LR2-4, S9 -> LR2-5.

## Deviations from the spec / dispatch text (each forced by a gate, or by the text)

1. **Node ids.** `tools/test_pile_cards_contents.py::test_node_ids_are_initials_form_and_unique` (`NODE_ID_RE = ^[A-Z]{1,3}\d-\d+$`) refuses `RD2-C1` and `TBW-M9`. Node ids are therefore `RD1-n` and `TBW1-n`; the spec's label stays in each «Что» cell as the first words `метка спеки: RD2-C1;` (or `TBW-M9;`), and every dependency/relation text maps spec labels to `RD1-n (label)` / `TBW1-n (label)`. Mapping (order = spec order): RD1-1 C1, 2 C2, 3 C3-0, 4 C3-a, 5 C3-b, 6 C3-c, 7 C3-d, 8 C3-e, 9 C3-f, 10 C3-g, 11 C3-h, 12 C3-i, 13 C3-j, 14 C3-k, 15 C4, 16 C5, 17 S9, 18 S10, 19 FL1, 20 FL2, 21 FL4, 22 FL9, 23 S1b, 24 B337; TBW1-1 M9, 2 T4a, 3 T4b, 4 T5r, 5 T6, 6 T7a-A/B/C, 7 T7b, 8 T7c, 9 T7f, 10 T9a, 11 T9c, 12 T3b, 13 T1rc, 14 T10, 15 close.
2. **TBW rows "VERBATIM"**: the cells of the §7 table are verbatim except (a) the id (item 1), (b) the «Что» cell gets the prefix `метка спеки: …;` and the suffix ` (находка: `findings/<file>.md`)` (check (е) requires a finding dated 2026-10-13 or later to be named in a ROW), (c) TBW-T1rc's «Пишет в» was `(по передрафту)` — the form check refuses a node with no path in backticks, so the redraft handoff path from §6 «Card T1r-cards-R» was put first: `docs/tasks/specs/20261117-told-before-work-t1r-cards-spec-r2.md` (по передрафту).
3. **Batch size.** rules-debt batch-1 has 24 nodes, told-before-work 15 (template: L is 10–15, more means two batches). Written as one batch each as the dispatch says; Lead decides the cut at `take`.
4. **Node cell shape of function lists.** «Пишет в» lists whole file names (the spec's function names carry line numbers and some are future); the batch headers say Lead refines function lists at take.
5. **TBW-T7a-A/B/C** is one row (verbatim). `piles.py status` refuses a node cell holding several ids (`_status_node_row`: "len(_node_ids_of) > 1") — the id `TBW1-6` is one token so this one is safe; the label in «Что» is `TBW-T7a-A/B/C`.

## Questions (spec text not enough to fill a column / a design decision left to the Lead)

1. **RD2-C3-0 scope.** The spec says C3-0 is dispatched "if F-D1 (a)", and the Lead decision is F-D1 (b) ("the predicate only for true accept sites"). I wrote the row as "build `acceptable` only for the true accept sites (test_identity, live_check_demand, provenance consumers, baseline_identity); plan critic judges each re-role" — confirm that C3-0 stays a node under (b).
2. **D-2 follow-up node** (`project:bugs/` in `stages.json`/`artifact-writers.json`, decided "(b) a separate node after C1, scout first") has no row in §5's list; I did NOT invent one. It is named in the batch «НЕ делать» line. Register it?
3. **B-373 live row.** §5 says the live-runs rows end with "B-373 (F-O2's live proof, already owed)". B-373 is already `LR1-1` in `live-runs/2` (and has `findings/B-373-…md`); a second row would duplicate the id. No new row; the `Ход` line of live-runs/2 and the RD1-24/RD1-15 texts point to LR1-1. Confirm.
4. **RD2-C4 dependency.** From «C4 result»: "the red row lands with the fix", so C4 depends on B337 (and both own `test_probe_by_code.py`). The §5 line said dependency "B-1" (decided (a)). Written: C4 «Зависит от» = RD1-24.
5. **RD2-B337 «Пишет в»** is the builder's reading in «C4 result» (cause `red_sandbox._frame_grammar`, `reporters.assertion_site`): `scripts/red_sandbox.py`, `scripts/reporters.py`, `scripts/tests/test_probe_by_code.py`; the text says the plan (designer) fixes the exact list. Spec note: the C4 report `docs/tasks/handoffs/t-961-rules-debt-c4.md` is on branch `worktree-agent-a72a37ff6d6ddc10a` (dd27d27e), not in this tree.
6. **Rows whose card has an open owner question:** none open — F-C1 (C3-j) and B-1 (C2) are marked "told to the owner" in the spec; written as «сообщено владельцу», no «вопрос владельцу:» line.

## Pairs on a shared hot file (no `очередь:` line added — the spec's waves section orders them only inside rules-debt, which is the batch's «Порядок по общим файлам»)

- Inside rules-debt/1 (ordered in the batch header, not by `очередь:`): `gate-registry.json` (row-disjoint), `gate_preflight.py` C3-i → C3-j → C3-k → C3-h, `window_record.py` S9 → C3-d, `controller.py` S9 → FL4, `s5_precheck.py` FL9 → C3-c, `execution_request.py` C3-b → C3-k, `run_suite.py` C3-a → C3-k, `test_probe_by_code.py` B337 → C4, `delivery-verdict-kinds.json` C3-e → FL2.
- Across piles, to be decided at `take` (only the Lead decision text of the TBW spec says it: "T5r after rules-debt FL9 merges"): `scripts/s5_precheck.py` — RD1-22 (FL9) vs TBW1-4 (T5r); `scripts/controller.py` — RD1-17 (S9), RD1-21 (FL4) vs TBW1-10 (T9a); `scripts/tests/test_controller_doors.py` — RD1-2 (C2) vs TBW1-10 (T9a), TBW1-11 (T9c); `scripts/manifest_put.py` — RD1-19 (FL1) vs TBW1-4 (T5r) and thinking-roles/6 TR4-17; `scripts/stage_guard.py` — RD1-18 (S10) vs TBW1-3 (T4b); `scripts/host_adapter.py` — RD1-18 (S10) vs TBW1-2 (T4a); `scripts/gate_preflight.py` and others vs taken onboarding-forge/hooks batches (spec §4: statuses not read).

## Same-class analogs noticed (not widened)

- `plans/piles/live-run-fvf/batch-3-live-run-fvf.md` header says "Размер — больше L (19 строк)": the same oversize situation as rules-debt/1 (24) — only a note.
- The forge batch 7 file's own header has no `очередь:` lines, so the mirrored line sits as its own paragraph before `## Бриф` (same position as in live-run-fvf/3).

## Needed beyond the manifest

`tools/piles.py` (check (д)/(е) rules, `NODE_ID_RE`), `tools/test_pile_cards_contents.py`, `plans/piles/live-runs/batch-2-live-proofs.md` and `README.md` (the untaken batch and its «Содержание» group), `plans/piles/forge/batch-7-vhodyashchie-4.md` (target of part 3), `plans/piles/live-runs/findings/B-373-…md`.

## Verification (witness)

First red run, before the id fix (shows the gate that forced deviation 1):

```
FAILED tools/test_pile_cards_contents.py::test_node_ids_are_initials_form_and_unique[rules-debt]
FAILED tools/test_pile_cards_contents.py::test_node_ids_are_initials_form_and_unique[told-before-work]
2 failed, 141 passed
```

Final runs:

```
$ python -B tools/piles.py check --all
(а) placement: ok (296 open ids, 136 closed, 190 findings, 165 batch-row members)
(б) overlap: ok (11 active batches; ...)
(в) frozen: ok (11 taken batch(es) on origin/main; every other batch is new or not yet taken: free)
(г) backlog: ok (frozen (compared with HEAD))
(д) form: ok (35 piles, 106 batches)
(е) findings: ok (1158 findings read, 0 dated from 2026-10-13 on are orphans, 152 older are the baseline)
piles check: ok

$ python -m pytest tools/test_pile_cards_contents.py -q -p no:cacheprovider
143 passed in 2.16s

$ python -B tools/piles.py summary   (the three piles; the lines sit inside the "не-id в строках" line)
rules-debt/1: RD1-1…RD1-24
told-before-work/1: TBW1-1…TBW1-15
live-runs/2: no hit of `grep -oE "live-runs/2…"` on the summary (not investigated why; the batch file itself is checked by `check --all` (д) ok); new nodes LR2-2…LR2-5
```

The `(е)` WARN line (152 findings older than 2026-10-13) is the pre-existing baseline.
