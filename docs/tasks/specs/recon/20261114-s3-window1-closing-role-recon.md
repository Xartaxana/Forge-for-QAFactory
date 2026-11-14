# Recon t-682 (scout, 14.11.2026): S3 window 1 read as "the stage's closing role" after A1a

Read on branch `wip/sc-a1a` (85dba1a), `ai-packages/qa-factory/scripts/`. Accepted by the Lead; spot-check: `controller.py:7598-7599`
(`if stage not in DERIVED_SCOPE_STAGES: return True`, `DERIVED_SCOPE_STAGES = ("S5", "S6")` at `:222`) and `:5849-5852` read on the carrier.

Cause: A1a removed the S3 stage critic, so the strategist is S3's last role (`contract.stage_closes_with` = `roles[-1] == role`,
`contract.py:5903-5908`). S3 has two windows of the SAME role; window 1 (`request_binding.purpose` = labelling, reader `s3_window_of`)
never closes the stage. Before A1a these sites took the "does not close" branch for the strategist. The sites are unchanged; the data changed.

No site CLOSES S3 on window 1: `_s3_completion_gate` (`controller.py:7526-7530`) refuses it. What goes wrong:

| site | what goes wrong |
|---|---|
| `controller.py:7570-7611` `_closes_stage` | answers True for window 1 |
| `controller.py:5089-5099` (caller 1) | an accept with no `stage_complete` key gets `stage_complete: True`, then the gate refuses it |
| `controller.py:5849-5858` (caller 2) | window 1 accepted with `--not-complete` and no `unresolved`: refused with a FALSE text ("leaves S3 with no role to close it") and a door ("pass stage_complete: true") that the gate then refuses (FR-2) |
| `story_step.py:1904` `_halt_doors` | offers `decide --close`, which the gate refuses (door text) |
| `story_step.py:2484`, `:2494-2505` `finish` | computes `complete = True` for window 1; a recorded `decide --close` overrides `--not-complete --unresolved plan_pending`, so `finish` cannot pass until `decide --open` replaces the record |
| `story_step.py:2812` `_decide_refusal` | accepts and records `--open`/`--close` for window 1 |
| `story_step.py:2943-2947` `decide` message | prints "recorded: S3 closes on this work as it is" — untrue |
| `controller.py:4080` `_is_review_of` | not applicable when the reworked role is the strategist; other reworked role — not traced |
| `controller.py:8555` `stage_repairs` | fixed in A1a's round (85dba1a) |

Not traced by the scout: `_declared_halt` (the digest-halt road to `_halt_doors`), the callers of `_rerun_stamp`, the pre-A1a `stages.json`.

Direction (Lead): ONE predicate "this dispatch can close its stage" = `stage_closes_with(stage, role)` and not an S3 labelling window
(through `s3_window_of`), wired at every site above (AR-15, AR-13); node A1c of the stage-critics topic A, after A1b (same hot files).
