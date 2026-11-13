# PC3-1 code critic: sides re-read after a registry repair (commit 64c7d3e over be2c988)

Verdict line: **fit_with_fixes** (NEEDS WORK) -- 1 blocking finding (B1), 4 non-blocking (N1-N4), 1 proposed node (P1).
The decision to accept stays with the Lead (critic rule 6).

Spec/DoD: finding `plans/piles/pre-code/findings/20261112-povtornoe-chtenie-storon-schitaet-product-po-odnomu-reestru.md` items 1-3
plus the dispatch's edges. Diff: `driver_machine.py` `sides_reread` (846-872), `driver_s0.py:1083`, `contract.py:5713-5717`,
`tests/test_story_sides.py:462-535`, a changelog fragment, the builder report.

## Findings

### B1 (blocks the merge) -- the re-read now writes a C15 case twin (`UI` beside `ui`) that S0 refuses
Surface: the launch-word leg of the sides merge on the re-read road. `sides_reread` (driver_machine.py:849) now merges launch words
through `_sides_entries`, but the C15 case check (driver_s0.py:1025-1036) lives only in `s0_write_sides`, which the re-read does not
run. At S0 with an unreadable registry `registry_sides` returns `names=[]` (contract.py:5790), so C15 cannot fire and `--side UI=real`
is kept. After the repair the re-read writes both names. Before this diff the re-read never read launch words, so this road is NEW.
It breaks the C15 INVARIANT ("a side is one name everywhere, so `UI` never lives beside a recorded `ui`") and the node's own
expectation (the re-read records what S0 would record: S0 with a readable registry REFUSES this launch). Control run (scratch copy of
64c7d3e, verbatim):

```
CONTROL rc 0 pipeline.json False C15 refusal: False
S0-unreadable rc 0 sides_unknown True sides []
REREAD rc 0 sides_unknown False sides {"UI": {"deliverable": true, "reality": "real", "source": "launch"}, "ui": {"deliverable": false, "reality": "substituted", "settles_by": "web team", "source": "registry"}}
```
(The control's "C15 refusal: False" is the stdout check only; the refusal went to the conductor - a search of the project found it:
`stub-log.jsonl :: ... the side `UI` given with --side is not a side of this project, but `ui` is, and side names are compared exactly`,
`launch side kept: {}`, no `pipeline.json`. So S0 refuses; the re-read writes two sides.)

Fix: move the C15 loop of `s0_write_sides` (driver_s0.py:1024-1036) into one helper (e.g. `DriverS0._side_case_twins(got)` raising the
same `Refusal`, dropping the name from the kept launch) and call it from both `s0_write_sides` and `sides_reread` right after the
`got["problem"]` check and BEFORE `stage_done`, so a twin leaves the mark in place and nothing is written (the call is `guarded`,
driver_machine.py:1860, so the Refusal reaches the conductor as at S0). Row `reread-case-twin` in the same `driver_cases` block:
broken registry, `--side UI=real`, repair with a `ui` row, relaunch -> the refusal text, `sides_unknown` still set, no `sides`.
Neighbouring classes of the same surface walked: magnitude n/a (one dict); nesting n/a; encoding -- a keyless name (`.`/`=`) from a
launch word: `side_set_args`/`stage_done` refuse it, same as S0's `coerce_value` refusal, acceptable; empty input -- covered by
`reread-empty-registry`; a NEW non-real launch word given on the relaunch itself (`launch_flags` reads this command line) -- see N3.

### N1 (fix before merge) -- the docstring of `sides_reread` lies now
driver_machine.py:838-839: "records the registry's non-real or referenced sides (`source: registry`)". It now records the S0 merge
(registry + launch + answers, real sides included). Same drift in `scripts/tests/fixtures/driver-layers.json:782` note
("records the registry sides"). Fix: reword both to "the merged entries of `_sides_entries`, as `s0_sides_sets` writes them".

### N2 (fix before merge, duplication) -- two loops turn a merged entry into side attributes
driver_machine.py:859-870 vs driver_s0.py:1085-1092: both build `{reality, deliverable, source, at, settles_by, reference}` from one
entry, with a deliberate divergence (S0: `entry.get("deliverable", True)` for every entry; re-read: True only for a real entry, a
non-real one with none stays unanswered). The divergence is invisible to readers (`contract._side_row` reads a missing `deliverable`
as True, contract.py:5834) but it is a second spelling of one record, the very class (AR-15) item 2 exists for. Fix: one helper
`side_attrs(entry, now, *, unanswered_ok)` used by both, the divergence a named parameter with its reason; or state in the
re-read's comment why it may not use S0's rule (W2 (4) row).

### N3 (non-blocking; report line) -- a non-real `--side` given on the relaunch itself is written unanswered
`launch_flags` (driver_s0.py:670-671) puts this command line over the kept launch, and `s0_keep_late_launch` keeps it, so a relaunch
with `--side api=substituted` after the repair is merged by the re-read and written with no `deliverable` and no question (S0 would
halt on `sides.deliverable`). Same class as the pre-existing W2 (4) "non-real side nobody answered" which the builder kept; readers
read it as deliverable (true). Not owed by this node; name it in the report's siblings so the Lead decides.

### N4 (non-blocking; report correction) -- D2 is false: the seeded state is reachable end to end
The builder says an answer given before the repair "cannot arise end to end". Driven end to end (scratch copy of 64c7d3e, verbatim):

```
1 launch rc 3 s0_block deliverable:ui pipeline False
2 answer+relaunch rc 0 s0_block None launch.side {'ui': 'real'} sides_answers {'ui': False} sides_unknown True sides []
3 reread rc 0 sides_unknown False {"backend": {"deliverable": false, "reality": "substituted", "settles_by": "platform team", "source": "registry"}, "product": {"deliverable": true, "reality": "real", "source": "default"}, "ui": {"deliverable": false, "reality": "real", "source": "person"}}
```
(`--side ui=substituted` with a broken registry -> the question; the answer `another team's` given with `--side ui=real` -> S0 ends
with `sides_answers {ui: false}`, no `sides`, the mark; repair -> the re-read writes ui `another team's` and product.) So the row
`reread-person-answer` tests a reachable state and must stay; fix: drive it through `s0_answer(..., "another team's", "--side",
"ui=real")` instead of writing `driver-state.json` by hand, and correct D2 in the report.

### P1 (proposed node, owner: Lead of `pre-code`) -- the default side has two carriers: the data file and the helper
`references/side-realities.json` `default.product = {reality: real, deliverable: true, settles_by: ""}` is read by `story_sides`
(contract.py:5677-5681, AR-1: "the default side is DATA"); `product_default_entry` (contract.py:5717) and both call sites'
`setdefault("product", ...)` re-spell the name and values in code. The spec asked for exactly this helper, so it is not a defect of
the builder; the convergence (helper built from `side_realities()["default"]`, with its unreadable-file direction) is a node:
`default side spelled in code beside side-realities.json | узел: <id the Lead opens in pre-code>`.

## Answers by id

1. **Items 1-3: met, except B1.** Item 1: `_sides_entries` with the story's `pipeline.environment` (same `env or flags.get("env")` as
   S0, driver_s0.py:986), `product_implied` over the merged entries, the same `stage_done` call lifts the mark; edges: `problem` ->
   one line, return (mark stays); empty merge -> only `sides_unknown=` (mark lifted, nothing written); launch entry without
   `settles_by` -> `row.get("settles_by")` falsy, key not written. Item 2: helper, both sites, `product` attrs unchanged (old literal's
   `settles_by: ""`/`reference: None` were never written, falsy). Item 3: all four rows present. **Negative control (old
   `sides_reread`, byte copy of base driver_machine.py into a scratch tree of 64c7d3e, sha256 equal 195943325a64...):**
   ```
   PASS reread-launch-words (control): a readable registry at S0 with `--side ui=real` records ui, backend, and no `product`
   PASS reread-still-unreadable: the registry still broken keeps the mark and records no side
   FAIL reread-launch-words: the launch's `--side ui=real` survives the repair, so the re-read equals S0 with a readable registry — expected (0, False, {'backend': {'reality': 'substituted', 'deliverab...
   FAIL reread-person-answer: an answer given before the repair reaches the record (ui another team's, source person) and `product` follows — expected (0, {'reality': 'real', 'deliverable': False, 'source': 'person'}, {'reality': 'real', 'deliverable': True, 'source': 'default'}), got (0, None, {'reality': 'real', 'source': 'default', 'deliverable': True})
   ```
   The two rows the node exists for fail on the old code (kill power confirmed). My run was cut by my own 500 s timeout inside the
   `reread-all-real-registry` loop; by reading, that row, `reread-empty-registry` and `reread-still-unreadable` PASS on the old code
   too (old filter left nothing for an all-real registry; old problem branch identical): they are edge pins, not detectors of N1/N6.
   `product_default_entry` fails on old code trivially (no function).
2. **D1: correct.** S0 writes `"deliverable": "true" if entry.get("deliverable", True)` for every merged entry (driver_s0.py:1087), so
   a real entry with no `deliverable` is `true` there. Downstream: `story_sides` returns `pipeline.sides` alone when present
   (contract.py:5673-5676) and `_side_row` reads a missing `deliverable` as True, so a written `true` reads the same as before. The
   material change is that real registry sides now ENTER the record; the old filter dropped them, so an old re-read of
   {backend theirs substituted, ui ours real} recorded `{backend}` only and no `product` (product_implied over the registry was False)
   -- the real part was unnamed in the story. New: `{backend, ui}` = S0. That is a fix, not a regression; stories already re-read under
   the old code are not rewritten (the re-read is mark-gated). No reader keys on "a real side absent from the record" beyond
   `story_sides`' fallback, which the record overrides on both versions.
3. **D2: false** (N4, run above). The row tests a reachable state; keep it, drive it end to end.
4. **Invariant: holds.** The only gate is `got["problem"]` (driver_machine.py:850); `_sides_entries` passes `read["problem"]` through
   unchanged (driver_s0.py:1009); `registry_sides` fills `problem` for an unreadable registry (5791) and for every malformed row /
   double reference (5751, 5763, 5774, 5781), and leaves those sides out of `entries` (reality "" skipped at driver_s0.py:989). The
   mark is lifted only by `sides_unknown=` in the one `stage_done` call with `check=True`; a refused set raises before the print and
   lifts nothing. No path lifts the mark without a clean read. B1 is a different invariant (C15), not this one.
5. **Helper: fresh dict per call** (literal built inside the function; the row `product_default_entry` mutates one result and checks
   the other); both call sites use it (driver_machine.py:858, driver_s0.py:1083). The remaining literals are different records: the
   `not built yet` record (driver_s0.py:1001, and its S1 twin driver_machine.py:3762, reality `absent`, source `person`) is the person's
   parking answer, already pinned as twins by test_story_run_words.py:465-476; `story_sides`' `_side_row(side, None, "default")` is the
   READER's row from the data file. Neither is owed by AR-15 in this commit; the data-file duplication is P1.
6. **DUPLICATION AND CONSISTENCY:** N2 (two attr loops), P1 (default side in data and in code). grep `"source": "default"|source="default"`
   over `scripts/*.py`: only contract.py:5717 (positive control: it is the helper). Merge readers: `_sides_entries` is now the one
   merge (AR-13 kept). **CODE QUALITY:** N1 (docstring and layer-map note lie); new code 27 lines, nesting 4 levels inside the loop
   (`if not sides` > `if entries` > `for` > `if deliverable`), pre-existing shape, no finding; no dead branch; `got["entries"]` mutated by
   `setdefault` is a fresh dict per call, safe. **Class completeness (SIBLING_MAP):** axis 35 (sides): writers through `side_set_args`
   are the re-read, arrival and the S5 answers -- arrival/S5 write one side from a new word, they do not rebuild the S0 merge, n/a;
   the C15 check is a stage-twin leg the re-read missed (B1). Axis 5 (stage twins, skill phase <-> driver): `phases/*.md` carry no
   sides re-read (case-insensitive grep `sides_unknown|re-read.*sides` over the package `*.md`: only CHANGELOG, architecture.md,
   artifact-contract-run.md stamps, the new fragment), n/a. Residual same class, pre-existing, outside the item-1 branch: when S0 DID
   write `pipeline.sides` (non-real launch words, registry unreadable), the re-read lifts the mark and never merges the repaired
   registry rows -- the "equal to S0 for every input set" expectation is unmet on that branch; not introduced here, proposed as a
   line: `re-read skips the registry merge when pipeline.sides exists | узел: <id the Lead opens in pre-code>`.
   **ONE ROAD (item 12):** the diff converges two roads; the one remaining divergence (C15 only on S0) is B1. **ARCHITECTURE:** AR-13,
   AR-15, AR-19, AR-28 named and kept; AR-1 tension = P1. Layer edge driver_machine -> driver_s0 (`_sides_entries`) is downward
   (`layers` in driver-layers.json), no ratchet raise. **JUDGMENT:** none -- a data merge. **Ratchets:** no in-tree ratchet row raised.
7. **Slow files the canon must show green for this node** (grep `sides_unknown|sides_reread|s0_sides_sets|product_implied` over
   `scripts/tests`, cross-checked with `scripts/slow_tests.json`): directly -- `test_story_sides.py` (155 s; the new rows; the builder
   ran it 177/177), `test_story_run_words.py` (32 s; the S0/S1 `product` twin through `s0_sides_sets`, :473), `test_no_mr_entry.py`
   (104 s; S0 `product` default pinned at :438), `test_driver_layers.py` (32 s; the `Driver.sides_reread` map row, new downward edge);
   readers of the record -- `test_brief_pack.py`, `test_report_facts.py`, `test_third_verdict.py`. The fast ones the builder already ran
   (`test_sides_ledger`, `test_s5_precheck_sides`, `test_proof_stamp`, `test_interim_packet`, `test_real_or_mock`) are not slow.

## Spot-checks of the report
- "values `side_set_args` sees for product unchanged": verified by reading old literal (base driver_machine.py) vs helper -- true.
- "no production code besides these builds side entries from registry rows by hand": grep `registry_sides\(` -> contract.py
  `story_sides` and driver_s0.py `_sides_entries` only after the diff -- true.
- "negative control not run": I ran it (above).
- D2: false (N4).

## Trail
Read: the finding (whole); `git diff be2c988..64c7d3e` (whole); driver_machine.py 815-872, 1835-1874; driver_s0.py 633-688, 960-1099;
contract.py 5649-5799, 5825-5844; test_story_sides.py 291-345 and the new rows; references/side-realities.json; docs/SIBLING_MAP.md axes
5 and 35; critic-diff-brief.md; slow_tests.json; driver-layers.json head, 409, 431-432, 782; test_story_run_words.py 465-480;
test_no_mr_entry.py 432-442; the builder report.
Runs (all in scratch copies made by `git archive 64c7d3e ai-packages/qa-factory`, never in the worktree): negative control
(`old driver_machine.py` copied over the scratch file, sha256 equal, then `python -B scripts/tests/test_story_sides.py`, output above);
the C15 probe and the D2 end-to-end probe (python on stdin with `story_run_common` helpers, outputs above).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1: driver_machine.py:849 sides_reread now merges launch words but skips the C15 case check of s0_write_sides (driver_s0.py:1024-1036); an S0 run with an unreadable registry keeps --side UI=real (names empty), and the re-read after repair writes UI beside ui (control run in the review); S0 with a readable registry refuses that launch"
  ],
  "fixes": [
    "B1: extract the C15 loop of s0_write_sides into one helper raising the same Refusal; call it in sides_reread after the problem check and before stage_done; add row reread-case-twin (refusal, mark kept, no sides)",
    "N1: reword the sides_reread docstring (driver_machine.py:838-839) and the driver-layers.json:782 note to the merged entries",
    "N2: one helper for entry-to-side-attrs used by s0_sides_sets (driver_s0.py:1085-1092) and sides_reread (driver_machine.py:859-870), the non-real unanswered divergence a named parameter with its reason",
    "N4: drive reread-person-answer end to end via s0_answer with --side ui=real instead of writing driver-state.json; correct D2 in the report",
    "N3 and the pipeline.sides-present residual and P1 (default side in data and in code): lines for the Lead to open as nodes in pre-code"
  ],
  "class_completeness": "Axis 35: the re-read now shares the S0 merge and product rule, but misses the C15 case check (B1); arrival and S5 answer writers do not rebuild the S0 merge, n/a. Axis 5: no skill-phase twin of the re-read (grep over package md), n/a. Residuals proposed as nodes: re-read skips registry merge when pipeline.sides exists; non-real launch word on the relaunch written unanswered (N3); default side in side-realities.json and in product_default_entry (P1).",
  "trail": {
    "read": [
      "plans/piles/pre-code/findings/20261112-povtornoe-chtenie-storon-schitaet-product-po-odnomu-reestru.md",
      "git diff be2c988..64c7d3e (worktree pc3-1)",
      "ai-packages/qa-factory/scripts/driver_machine.py 815-872, 1835-1874",
      "ai-packages/qa-factory/scripts/driver_s0.py 633-688, 960-1099",
      "ai-packages/qa-factory/scripts/contract.py 5649-5799, 5825-5844",
      "ai-packages/qa-factory/scripts/tests/test_story_sides.py 291-345, 462-535",
      "ai-packages/qa-factory/references/side-realities.json",
      "ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json",
      "ai-packages/qa-factory/scripts/slow_tests.json",
      "docs/SIBLING_MAP.md axes 5, 35",
      "docs/tasks/critic-diff-brief.md",
      "docs/tasks/specs/reports/20261113-pc3-1-report.md"
    ],
    "reruns": [
      {
        "command": "scratch tree of 64c7d3e with base driver_machine.py (sha256 195943325a64... equal); python -B scripts/tests/test_story_sides.py",
        "result": "reread-launch-words and reread-person-answer FAIL on the old code; control and still-unreadable PASS; run cut by a 500 s timeout in reread-all-real-registry (passes on old code by reading)"
      },
      {
        "command": "C15 probe on scratch tree of 64c7d3e: broken registry, --side UI=real, repair with ui row, relaunch",
        "result": "REREAD writes both UI and ui, mark cleared; readable-registry control refuses the launch (C15 text in conductor log)"
      },
      {
        "command": "D2 end-to-end probe: --side ui=substituted, answer another team's with --side ui=real, repair, relaunch",
        "result": "S0 ends with sides_answers {ui: false}, no sides, mark set; re-read writes ui deliverable false source person plus product: state reachable"
      }
    ]
  }
}
```
