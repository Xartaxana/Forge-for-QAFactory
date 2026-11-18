# t-1262 FV3-22-1 report (the move; builder, Sonnet)

Head: see the final message (branch `worktree-agent-ab84923a7b5ea3f1f`, commit `cda1ae14` plus this report's commit). Started from origin/main
1323da2b (FV3-21 wave c96d9bc2 is an ancestor: `git merge-base --is-ancestor c96d9bc2 origin/main` -> true).

## Items

- K5.a DONE: `scripts/stage_close.py` (new): `Refused`, `BY_PERSON`, `CONSUMER_ROUTES` (data only), `s6_automation_settled`, `person_word_door`,
  `consumer_pending`, `accepted_at`, `person_pass`, `consumer_person_pass`, `need_record`, `mark_awaiting`, `manual_half_close`, `close_by_code`,
  `code_only_request`, `file_passed_over`. Bodies moved, `self` -> `road`, every step through `road.<member>`. No `SkillRoad` (that is FV3-22-2).
- K5.b DONE: `driver_stage_s6.py`: `CONSUMER_ROUTES` = module data + the two lambdas; delegates `consumer_pending`, `accepted_at`, `person_pass`,
  `consumer_person_pass` (keeps the retry), `consumer_need_record`, `consumer_await`, `file_passed_over`, `manual_close` (head kept, tail =
  `manual_half_close`); `stage_S6` uses `s6_automation_settled`; `BY_PERSON` read as `stage_close.BY_PERSON`.
- K5.c DONE: `driver_stage_s7.py`: `close_by_code` delegate with the Refused -> Refusal conversion.
- K5.d DONE: `driver_dispatch.py`: `code_only` = `code_only_request` + `controller("code_only")` + `progress_line()`; `_sha` stays in the import line (caller :2484).
- K5.l DONE: `driver_core.py` `BY_PERSON` deleted; `driver-layers.json`: row BY_PERSON deleted, row `Driver.consumer_await` note gains "FV3-22: delegate of
  stage_close.mark_awaiting". No story_step edit (see decisions).
- K5.m DONE: refusal of `need_record` ends with `person_word_door`; variant row in `test_story_run_s6.py` (after the `s6_reentry` refusal row);
  `test-layers.json`: `stage_close.py` added to `covers` of `test_story_run_s6.py` and `test_story_step_manual_block.py`; changelog fragment bullet 1.

## Decided differently from the card (Lead decisions at the card end, t-1209 F5)

`live_s6_scopes` stays in `controller.py:690` (dropped from the move). `story_step.py` already imports it from `controller` (:105) and its `_no_stand_refusal`
docstring already says `controller.live_s6_scopes`, so story_step.py has NO edit. No `story_step -> driver_stage_s6` importer row exists. No new layer row.
Nothing else was decided differently. The F4-1/F4-2 decisions belong to step 1b (FV3-22-2).

## MF1-MF7 on the head (origin/main 1323da2b)

- MF1 (differs by the Lead's F5): `controller.py:690 def live_s6_scopes`; `driver_stage_s6.py:10` imports it from `controller`; `Driver.s6_live_scopes` at :1581 area unchanged.
- MF2: `story_step.py:1088` `if not words or live_s6_scopes(state)` (import :105, docstring :1083). Line shift only.
- MF3: `consumer_await` was `driver_stage_s6.py:340` (now a delegate); `consumer_need_record` :314 -> `consumer_await` at an `await_at` site. Line shift only.
- MF4: `driver-layers.json` `allowed_importers` has exactly the two WT rows (`story_step->driver_timing`, `run_counters->driver_timing`, :6-7); no `story_step->driver_stage_s6` row; `Driver.consumer_await` row :705 existed, `Driver.s6_live_scopes` row :1042.
- MF5: `_no_stand_refusal` untouched (signature kept).
- MF6: `manual_close` was `driver_stage_s6.py:1060-1085`; `CONSUMER_ROUTES` :149-161; `consumer_awaits` :163 unchanged. Line shift only.
- MF7: baseline `scenario_walk.py --witness-for <nine owns>` ran before any edit: it PRINTS files only (106 test files; no reds by itself). No inherited red found in the tests that were run afterwards.

## Grep (AR-13 / AR-14 / AR-18 / R2-F2), over `scripts/*.py`

- `BY_PERSON =`: 1 hit, `stage_close.py:21`.  `def live_s6_scopes`: 1 hit, `controller.py:690`.
- `atomic_json(` in `stage_close.py`: 1 (`mark_awaiting`).
- `road.py(` in `stage_close.py`: :123 (`check=True`), :221 and :245 (`code, out =` bound and tested).
- `controller("code_only"`: only `driver_dispatch.py:2545`. `finalize_task.py` hits: brief_pack, check_delivery, delivery_manifest, driver_dispatch, driver_machine, driver_stage_s6/s7, guard_pre_tool, judge_results, project_gitignore, report_facts, stage_close: the sites are callers of the survivor (driver_stage_s6 `manual_close`, s7 `close_by_code`) or unrelated readers.
- `acceptance_awaits`: `driver_stage_s7.py:204-205` writes S7's own marker (S7 keeps its own road `s7_await_scribe`; FV3-26's, not this card's); `acceptance.py` the reader.
- `"running", "blocked", "paused"` over S6: `controller.py:697` (the one predicate), `driver_stage_s6.py:1581` (an inline twin, see analogs).
- ratchets raised: none; shrunk: `driver-layers.json` BY_PERSON row (1 row).

## Witness

Command (the node's DoD file list; the files `scenario_walk.py --witness-for` printed were run where not judged by the batch canon, each as `python -B scripts/tests/<file>`):

```
test_driver_layers: 283/283 ok
test_judgment_census: 25/25 ok   (exit 0 in 602s)
test_no_move_seam_sites: 514/514 ok   (exit 0 in 833s)
test_audit_rules: 375/375 ok   (exit 0 in 187s)
test_words_doors: 716/716 ok   (exit 0 in 1677s)
test_story_run_s6_w1_frozen: 6/6 ok   (exit 0 in 141s)
test_silent_passes: 326/326 ok   (exit 0 in 920s)
test_walk_lanes_parallel: 196/196 ok   (exit 0 in 74s)
test_stage_closure: 88/88 ok   (exit 0 in 97s)
test_story_step_start: 169/169 ok   (exit 0 in 338s)
test_story_run_deferred: 73/73 ok   (exit 0 in 439s)
test_scenario_local_1_0108: 15/15 ok   (exit 0 in 825s)
test_story_run_s6: 739/739 ok   (the file with the K5.m row; final line "=== test_story_run_s6: 739/739 ok ===")
```

The K5.m row printed `PASS K3 the same refusal ends with the person's-word door WITH its words file`.

## Needed from integration

- `plans/features.json`: register `ai-packages/qa-factory/scripts/stage_close.py` under feature F19 (the pre-push gate WARNs (b)/(d): "new package file ... matches no feature"; not a refusal; `plans/` is outside my owns).
- Not run (not printed as mine, or batch canon): the other ~90 files of the witness-for list (slow), the quarantined files named in non-goals.

## FR / AR pass (package diff)

A: refusal text keeps FR-1 shape and now ends with a runnable door (FR-2, `person_words.door`); no waiver path changed. B: the only person-facing text changed is that door (via the one renderer). C: contracts unchanged (road members equal the old `self` set). D, E, F: not touched. G: English/ASCII file; no control bytes; stdlib only.

## Analogs noticed (not fixed)

- `driver_stage_s7.py:181-205` `s7_await_scribe` writes the awaiting marker with its own `atomic_json` twin of `mark_awaiting` (axis 5 / FV3-26).
- `driver_stage_s6.py:1581` inline `"running","blocked","paused"` over S6 rows duplicates `controller.live_s6_scopes` (could call it; FV3-21's code, outside this move).
- S7 site `driver_stage_s7.py:772-775` of the same close is FV3-26's.

Changelog fragment: `ai-packages/qa-factory/changelog.d/fv3-22-skill-road-s6-close.md` (bullet 1 only; bullet 2 is FV3-22-2's).

## Canon fix

Canon 44189216482 forge-check: `tools/test_forge_metrics.py` K1 listed `scripts/stage_close.py` as unattributed. Added one row `"scripts/stage_close.py"` in `plans/features.json`, right after `scripts/driver_*.py` (the feature that holds the driver_stage_s6 files). origin/main merged first (clean).

## Fix F-B1

`s6_settle_blockers` (driver_stage_s6.py ~1581) now calls `live_s6_scopes(ctl)` inside the same try instead of the inline status predicate (AR-15). Witness: `test_walk_lanes_parallel: 196/196 ok`.
