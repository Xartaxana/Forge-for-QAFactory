# PC3-1 fix round (after the code critic, B1)

## B1 fixed
- `driver_s0.py` `Driver.side_case_twins(got)`: the C15 loop moved out of `s0_write_sides` whole (same Refusal text, same drop of the name from the
  kept launch, same `save_state`); ONE function. `s0_write_sides` calls it (right after `_sides_entries`); `driver_machine.py` `sides_reread` calls it
  right after the `got["problem"]` check and BEFORE the `stage_done` call. The call is `guarded`, so the Refusal reaches the conductor as at S0.
- The critic's scenario (broken registry, `--side UI=real`, repair with a `ui` row, relaunch): before 64c7d3e wrote `UI` beside `ui` and cleared the mark;
  after: Refusal, mark kept, no `sides`, the kept launch is `{}`. Row `reread-case-twin` (test_story_sides.py), RED on 64c7d3e (a scratch
  `git archive 64c7d3e` tree with the new test file):
  `FAIL reread-case-twin: ... expected (True, True, False, {}), got (False, False, False, {'UI': 'real'})`
  GREEN after: `PASS reread-case-twin: ...`.
- State left after the refusal: `pipeline.sides_unknown` STAYS set (the registry read was clean but nothing was written, same as S0 where a refusal
  leaves no `pipeline.json`). The way out (AR-25): the offending name is already dropped from the kept launch, so the NEXT relaunch (corrected
  flag or none) re-reads cleanly, passes C15 and clears the mark - the same door S0 gives (the corrected flag is not met again).
- Exact-case match (`ui`/`ui`) and empty launch words: unchanged (C15 only fires for a name not recorded and equal to a recorded one but for case).
  A registry with two rows differing only in case: unchanged, `names` holds both, so neither a launch `UI` nor `ui` is a twin of the other
  (`name in recorded` short-circuits); S0 and the re-read now behave identically there.

## N1 fixed
Docstring of `sides_reread` and the `driver-layers.json` note of `Driver.sides_reread` reworded to "the merged entries of `_sides_entries`, as `s0_sides_sets` writes them".
Two new layer rows (`Driver.side_case_twins`, `Driver.side_attrs`, home driver_s0, row 61), demanded by the driver-layers map.

## N2 fixed
`Driver.side_attrs(entry, now, *, unanswered_ok=False)` in driver_s0.py: the one spelling of a merged entry as side attributes (key order as S0 had it).
`s0_sides_sets` uses it with the default; `sides_reread` with `unanswered_ok=True` - the named divergence: a NON-real entry nobody answered stays without
`deliverable` on the re-read (it has no question to ask; readers read it as true), S0's rule gives it `true`. `settles_by` is written only with a `deliverable`
(always the case at S0, so S0 output is unchanged).

## N4 (D2 correction)
D2 of the first report ("cannot arise end to end") was wrong, as the critic showed. Row `reread-person-answer` now drives the state end to end:
`--side ui=substituted` (broken registry, question), `s0_answer(..., "another team's", "--side", "ui=real")`, repair, relaunch; no hand-written `driver-state.json`.

## Siblings (listed, not changed)
- N3: a non-real `--side` given on the relaunch itself is merged by the re-read and written unanswered (same class as W2 (4)).
- Residual: when S0 DID write `pipeline.sides` (non-real launch words with an unreadable registry) the re-read lifts the mark and never merges the repaired registry rows.
- P1: the default side lives in `references/side-realities.json` and in `contract.product_default_entry`.
- Other re-read roads rebuilding S0 facts without S0's checks: none met beyond these (`arrival_record` and S5 answers write one side from a new word via `side_set_args`; they do not rebuild the S0 merge).

## Witness (run once, from `ai-packages/qa-factory`, scripts/tests via `python -B`)
```
=== test_story_sides: 178/178 ok ===
=== judgment_census: 24/24 ok ===
=== qa-factory selftest: 2/2 ok ===      (python -B scripts/selftest.py --lang)
```
Slow files left to CI: test_story_run_words, test_no_mr_entry, test_driver_layers (the two new layer rows and the `Driver.sides_reread` note are what the last one reads).
Class check: `s0_sides_sets` S0 output is unchanged by construction (same keys, order, values) - pinned by the unchanged S0 rows in test_story_sides (178/178).

architecture: AR-15 (C15 and the entry-to-attrs record each one survivor, no copy), AR-19 (S0 and the re-read are stage twins: one check, one record), AR-25 (the refusal leaves the mark and the dropped name is the way out).
