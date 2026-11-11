# t-2013 - critic on walker Slice 1 (spec t-1957: N1a, N2, N3, N4, N5s)

**Verdict: rework (schema word `blocker`). 4 blocking findings; do not start the live run on this head.** The decision is the Lead's. The design and the server itself hold: the real browser server ran on this machine for the first time and worked (below). What does not hold is the road AFTER the walker: on the charter's own road every pass and every fail ends `left_unchecked`.

Reviewed: `wn5s` 857ec889c plus cf8f83ee8 (read as a diff; see F9).

## Findings

**F1. BLOCKS. Every pass and fail walked by the charter is refused when its record is built.** `walk_session.py:909` (`_take_final`), `manual_evidence.py:550,572-576`, `walk-charter.md`.
`final` writes `capture post_action final`, so `proves: ["final"]`. `validate_record` wants, for `pass`, a post_action ref proving `completion`; and for `pass` or `fail` under policy `ui` (the recipe's R3 word) a `pre_action` image. The charter, the brief and the command card mention neither. The server's `verdict` answers `ok`, the session closes, then `record_from_walk` refuses, `walk_after` re-queues once, the second refusal closes the case `left_unchecked`.
Witness (real `Walk`, fake browser, real `build_record`; `_running_dispatch` stubbed):
```
A pass, charter steps + --final : verdict: 0 ok | refused: ...pass requires post_action evidence proving completion...; ui requires pre_action and post_action evidence...
B fail, charter steps + --final : verdict: 0 ok | refused: ...ui requires pre_action and post_action evidence...
C fail + capture pre_action x   : written, fail
D pass + capture pre_action x   : refused: ...must list "completion"...
E pass + pre_action + capture post_action completion : written, pass
```
Why no test saw it: `test_record_from_walk_builds_valid_record` hand-writes `capture pre_action initial` into a `ui` call and only tries `fail`; `test_walk_lanes` stubs the build. **SPEC:** §3.2, §3.4 and E2.13 assume a `final` is what a pass needs; t-1960 did not catch it.
Fix direction: `final` writes the `completion` proof (`capture post_action completion`, and `final_state`'s two matchers follow); the server itself inserts `capture pre_action start` before the item's first non-`goto` action, because a role that finds out at `verdict` can no longer photograph "before" (P26: code writes the evidence). The insertion is a small fork for the Lead; the alternative is a charter line. Add one test that goes step -> final -> verdict -> close -> real `record_from_walk` for pass and for fail, with no hand-written capture.

**F2. BLOCKS. The class of F1: `verdict` accepts what the build refuses, after the session is gone.** `walk_session.py:373-437` against `manual_evidence.py:252` and the inconclusive rule above `:550`; `walk_session.py:490-493`.
```
G inconclusive with `limitation` on the Then : verdict: 0 ok | refused: inconclusive requires a limitation
H fail, observation {step, expected, seen, capture} : verdict: 0 ok | refused: observations[0].quote is missing
```
G is the recipe's example D (8 silent cards of 23): a Then-level `limitation` is dropped by `write_verdict`. H is the charter's own list ("the step, what you expected, what you saw, the capture": no quote). One doubtful place written as the charter says loses the whole case; P26 wants exactly those places recorded. The surface is "verdict -> record"; neighbours walked: `step` out of range, `surprise` citation, an empty `actual` (`said` covers it), the ui phases (F1), a Then with no number (refused, fine). Fix direction: `op_verdict` runs the record's own rules (`_observation_errors`, phases, completion, limitation) while the session lives, through one shared function, not a copy; a Then-level `limitation` joins the record's; the charter names `quote`.

**F3. BLOCKS. `walk_values` leaves the form unfillable, so every lane pays a resume and may stop on a person.** `story_run.py:3401-3425`, `form_errors` :2389, ladder :2594-2624.
The exact values fed through the real `handoff_check.py --fix` (on the template, no task root, so a materialized form may prefill ids):
```
all passed      exit 1: applied 21 value(s) ... not ready - 31 field(s) below
failed+refused  exit 1: applied 16 value(s) ... not ready - 29 field(s) below
  header.window, run.execution_status, run.witness, run.environment, run.application_build, run.probe_before, run.probe_after, inputs_read[*]...
```
`walk_values` writes no `run.*`; a grep of its diff shows none. `handoff` then resumes the walker through `run_claude` (:2612; the code's own price note at :2393 says about $0.60), whose brief has no form card; what stays wrong goes to `exit_limit`, the person. That is a driver stop per lane and it pollutes the ≤ $0.50 measurement. Fix direction: code fills every required field from what it owns (`run.*` from the walk record and probes, `inputs_read`, `header.window`), and a test applies real `walk_values` output through real `handoff_check` to exit 0 on a materialized form.

**F4. BLOCKS. A halt, a resume or an infrastructure cut ends the lane's unwalked items for good.** `story_run.py:3320-3400`, :15499, :15537; `walk_session.py:258-259`.
Scenario: the walker halts, or the API drops, after item 1 of 3. `after` runs in the `finally`, `write_verdict(None)` writes `work/walks/<W>/<item>.json` for items 2 and 3. Then:
- `resume_role` reopens, the words say "items with a verdict are done; continue with the next", and `request_problems` refuses every remaining item ("has a verdict on disk"), since the auto-written record counts as a verdict; `after.json` skips them too.
- `_act_wait_existing_job` :15499 (cut by infrastructure) and :15537 (never launched) call `run_role` with **no `after` and no reopen**: a walk brief on a closed server, and no records (Q5). §3.2 "Resume / rerun" and E5s.6 name only part of this.
Your Q2 item blocks for this reason. Fix direction: a record written for a missing verdict is marked and is not a verdict for `request_problems` or `after.json`, and `run_role` itself owns the hook: when `state/walks/<dispatch>.json` exists it reopens if not ready and runs the after-step, whoever called it. That closes the class of callers instead of one keyword on one caller.

**F5. HIGH (blocks 5 cards of §7, not the run). A two-account lane silently leaves the walker.** `story_run.py:3233-3279`: `auto_actor` refuses two accounts, the `except` turns that into today's road. Recipe lanes UU and AU (cards 18, 19, 11, 13, 24) never walk; §7 step 1 and §3.6 promise `--as`, and `walk_reopen` already passes `--actor2`. Fix: map up to `max_actors` keys of the lane to `--actor`/`--actor2`; beyond that, today's road with the reason. Or the Lead drops those cards from the claim in the recipe. Old-road numbers must stay out of the medians.

**F6. MEDIUM. The teardown check is dead.** `walk_session.py:432` reads `request.get("teardown")`; `manual_evidence.py` holds the word 0 times (`grep -ic teardown`; control: 10 in `walk_session.py`). Q1 answer: not "every item unverifiable", the opposite: never refused, the record says `none`. A leftover `fail_request` then decides the next item in a shared lane (recipe R5 rests on the role alone). Fix: read the case's `## Teardown` by the reader N3 uses.

**F7. MEDIUM. CI will be red by the report's own list.** t-2002 "CI-only files": `test_story_step_manual_block.py` K-R2, K-R3, K-P2 and :659/:667 pin the old window and `manual_blocks(` in `plan_src`; not edited, outside `owns`. Does not touch the live run; owed before merge, a node for the Lead.

**F8. MEDIUM, queue. Two universality gaps (P2, AR-3).** `walk_session.py:655` and `walk_before` take the FIRST environment, not `pipeline.json environment`; MyBooks is safe (`local` is first, `config.json:304`), a project with two stands probes the wrong one. `walk_session.py:687` passes `in_harness=True`, so a project whose Playwright lives only in its harness never walks: `open` fails and every lane takes today's road. This machine is fine (measured below).

**F9. LOW. The dispatch's head claim.** cf8f83ee8 is NOT on `wn5s` (`merge-base --is-ancestor`: not in). It is on `fb-fix`, which also holds the merge e65e81a55 of `wn5s`; `wt-fbfix` HEAD = `fb-fix` = 20317b442. The recipe's freeze from `$W` is right; never freeze `wn5s`.

**F10. LOW. A quote's reach (Q4).** `_quote_home` accepts any text capture of the attempt, including what the role itself typed (`002-fill--q.txt` is a capture, measured) and a look from before the action. By design (AR-29), the analyst judges; say it in the analyst's brief or the charter, so "a quote was checked by code" is not read as more than presence. Also `walk_after` trusts any `work/walks/<W>/<item>.json` on disk, so a file the role hand-writes skips `verdict_problems`; `build_record` still checks quotes and completion. Queue.

## The questions

**1. N2's choices.** Teardown: F6. Action union, `fill-account` not counted: safe in practice, since `click` follows; strictly a `final` before a last `fill-account` or `fail_request` passes, against "never" of E2.3; add both words (one line). `final` by step order: safe, better than clocks. No Then -> inconclusive: safe. Quotes as tuples: right, `_then_quote_problems` takes `(kind, raw)`; the spec's string form was wrong (probes C, E wrote).

**2. N5s' choices.** Blocks: `walk_values` unproved (F3), halted-then-resumed (F4). Not blocking: `lane_keys` added (justified, three callers; name it in the spec); `walk_lanes` size < 1 reads 1 (safe direction; avoiding a census unit is honest here, nothing is refused); open fails -> dead record deleted (right, answers Q5's fresh case); `manual_close` double count (a text, queue).

**3. Unverified by tests, now measured on Windows** (real detached server, real Playwright and chromium, loopback static site; `MC.PROBE` and `stand_hosts` patched in a wrapper, nothing else):
```
open 13.1-23.1 s, exit 0 | step of 5 + --final: done, 8.4 s, 7 rows, status surprise on /x -> 404 recorded, no stop
goto 404 with +status:400-499: exit 1 stopped, status number 404 | close 5.8 s: probes [start, end]
requests-seen holds the item's two GETs | hard kill (taskkill /F of the server): child node gone, E1.3 client "server ... is gone"
open over the orphan: exit 0, lease taken | parent killed: state dead after 11.5 s, "the process that opened the walk is gone"
```
Job object and detached spawn: proved on Windows, no risk tonight. E1.3 client path: proved. E1.7 parent gone: proved; 11.5 s under load against "`parent_check_s`" of the invariant, harmless. E1.4 (not ready in 90 s): NOT run; a canary could meet it under builders' load (old call overhead 53 s, `walker-call-overhead.md`), and it falls back to today's road and says so. E1.12: argv lists, case ids plain; low. POSIX `killpg`: not run, not on tonight's road. The real server has still not met a real login or MyBooks; the canary does. A `read ... expect=two words` needs quotes or it is refused, with a shape text that does not say so (met by me): one charter word.

**4. The road.** A `pass` with no capture after the last action: no road through `verdict`: order checked, and steps after a verdict are refused. The one bypass is F10's hand-written file. But today no `pass` comes out at all (F1). After the fix, the quote proves presence only (F10); per-Then words survive in `actual` and in the walk record, `then_quotes` has no per-Then result. Unknown never becomes pass: all folds checked.

**5. Yes, three roads:** :15499, :15537 (F4); and a server dead by `idle_s`/`max_s` mid-role, where the refusal does name its door. The handoff ladder's resume (:2612) also runs on a closed server, harmless while only the form is asked.

**6. AR-29.** No check judges judgment. `request_problems` xref, `_refuse` shape, `verdict_problems` xref: rows right; `stop_at` is no unit. `test_judgment_census.py` rerun: `21/21 ok`. N5s' `judgment: none` is true. Watch: `walk_values` writes the role's `header.verdict` (a pure fold, fine) and generic `then`/`observed` sentences the analyst reads (AR-21: no Then text travels); replace them when F3 is fixed.

**7. Ratchets, row by row.** `blocking_per_role.conductor` 466 -> 467: named in fcc3857bb, the spec's one raise. `role-load.json` qa-runner 17884 -> 15566, 16699 -> 14407: down. `driver-layers.json`: 5 method rows and state key `walk_retry`, in the report, no upward edge in the diff. `dup-baseline.json`, `env-facts-baseline.json`: untouched (`git diff --stat` empty). No unnamed raise found. "D13": no such row in the reports read or in `audit_factory.py` (grep empty; same grep form found other words in those files). The `forge-check` output of this branch was not attached: requested, not re-derived.

## Standing questions

**Fit:** server and stop rules fit; N2/N5s miss §3.5's "records exist before the exit check" (F1-F3). **Seams:** additive; `run_role` wrap is minimal; `test_story_progress` edit beyond its range is named. **Class (axes):** axis 5 twins: door, progress, driver share `walk_lanes`; class "second check at a later point" (F2) has no axis in `docs/SIBLING_MAP.md` (grep of recorder and walker words, 589 lines: no row): propose one. Not fixed and not queued anywhere: F1-F8.

**DUPLICATION AND CONSISTENCY:** `brief_pack._case_sections` (:3227) repeats `traceability._sections` (:1593), and `traceability` is already imported there: reuse, fix before merge. `walk_session._kill` repeats a process-tree kill; `run_suite.py` and `node_ids.py` also call `taskkill` (lines not read): queue. `verdict_problems` beside `validate_record` is F2. No second recorder road: `_run_steps`, `parse_steps`, `Attempt` imported, not copied (read).

**CODE QUALITY:** `walk_after` `story_run.py:3320-3400` (80 lines, 5 levels), fix before merge; `request_problems` `walk_session.py:209-289` (80 lines), queue. Dead: `EXIT_REFUSED` import (:54); data row `answer_chars`, read nowhere (only `batch_answer_chars` :870), so E1.6's cut for `look`/`final` does not exist. `Walk.blocked_blocks` is a class-level dict, rebound on write, so harmless; queue. `story_step.py` `lines =[` spacing: nothing.

## Spot-checks and negatives

- "No test covers the charter road": read `test_walk_record.py:309-331`, `:267` (fake build). Control: same file does call real `record_from_walk` once.
- "`manual_evidence.py` never says teardown": case-insensitive grep, control above.
- "`walk_values` writes no `run.`": read the whole function.
- Guard: `stage_guard.py` names no recorder script (grep `manual_evidence.py` empty; the same grep over `story_run.py` hits), so `walk_session.py` is not barred by name. Where the role may Write its steps and verdict files was NOT established; the charter names no path. Watch it on the canary.
- Recipe impact: §4.3 reads `work/walks/`, which F1 leaves looking green; only its `current_manual_checks` line catches it. Keep that line.

## Trail

Read: spec §1, §3.1-3.10, §4 Slice 1, §7; brief; recipe; t-2002 report; all eight diffs; `walk_session.py` whole; `manual_evidence.py` :170-215, :500-582, :1095-1125, :1262-1300, :1380-1412, :1540-1835; `manual_capture.py` :1340-1440, :2305-2345, :2770-2790, :3153-3345; `story_run.py` :1219-1250, :2389-2405, :2476-2624, :2806-2935, :12590-12625, :15478-15506, :15613-15660; `execution_scheduler.py` :25-85; charter. Reports other than t-2002 were not read beyond the greps: their witnesses were not re-derived.
Reruns: the four witnesses quoted above; `python -B .../tests/test_judgment_census.py` -> `=== judgment_census: 21/21 ok ===`. No slow file, no docker, no ratchet.
Deviation to note: my first probes were scripts written through Bash into the session scratchpad (`probe_road.py`, `probe_real.py`, `wrap_serve.py`, `head.py`, `probe_road2.py`, `probe_real2.py`) before `handoff_gate` refused a Write there. After that refusal I wrote no new file, ran the rest from stdin, reading those files. The probes also made temp story folders under the system temp, as the test rig does, and started real servers on loopback; all exited (listed: none left of the first batch; the last server reported state `dead`). Nothing in the repository, the worktree, `tr-walk` or the stand was touched.
Needed beyond the manifest: `manual_evidence.py`, `manual_capture.py`, `handoff_check.py`, `handoffs/s6-runner-to-analyst.yaml`, `story_run.py` beyond the diff.

```json
{
  "verdict": "blocker",
  "blockers": [
    "F1: final writes proves [final], no pre_action image: every charter-road pass and fail is refused at build_record, re-queued once, closed left_unchecked (walk_session.py:909, manual_evidence.py:550,572-576)",
    "F2: verdict accepts what the build refuses after the session closed: Then-level limitation dropped, observation without quote (walk_session.py:373-437,490-493, manual_evidence.py:252)",
    "F3: walk_values leaves 29-31 form fields unfilled: a resume per lane and exit_limit to the person (story_run.py:3401-3425,2594-2624)",
    "F4: after writes a record for unwalked items, so a resume refuses them; story_run.py:15499,15537 run a walk dispatch with no reopen and no after"
  ],
  "fixes": [
    "final writes the completion proof; the server takes the pre_action image itself (Lead's small fork); one test through the real road for pass and fail",
    "op_verdict runs the record's rules through one shared function; Then-level limitation joins the record; charter names quote",
    "walk_values fills every required field; a test through the real handoff_check to exit 0 on a materialized form",
    "a record for a missing verdict is marked and is not a verdict; run_role owns reopen and after when a walk record exists",
    "F5 map two accounts to --actor2 or drop those cards from the claim; F6 read the case's Teardown; F7 CI pins; F8 first environment and harness interpreter queued; add fill-account and fail_request to the action set"
  ],
  "class_completeness": "Class named: a later check refuses what the earlier gate told the role was fine, once the role can no longer act (F1, F2, F3). No axis in docs/SIBLING_MAP.md (grep of recorder and walker words): a new axis is proposed. Axis 5 twins door, progress and driver share walk_lanes: covered. Callers of run_role on a walk dispatch: three found, one wired (F4). Nothing fixed or queued yet.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-1957-fast-manual-walker.md",
      "docs/tasks/critic-diff-brief.md",
      "docs/tasks/specs/t-2006-walker-live-run-recipe.md",
      "docs/tasks/specs/reports/t-2002-walker-n5s-report.md",
      "ai-packages/qa-factory/scripts/walk_session.py",
      "ai-packages/qa-factory/scripts/manual_evidence.py (ranges)",
      "ai-packages/qa-factory/scripts/manual_capture.py (ranges)",
      "ai-packages/qa-factory/scripts/story_run.py (ranges)",
      "ai-packages/qa-factory/references/walk-charter.md",
      "diffs 83b8dcf2c fcc3857bb d290fc65f 2f001e382 e0a4c6001 cf8f83ee8 857ec889c"
    ],
    "reruns": [
      {"command": "probe: real Walk, fake browser, real build_record, verdict shapes A-E, G, H", "result": "A, B, D, G, H refused at build after verdict ok; C, E written"},
      {"command": "probe: real detached server, real chromium, loopback site", "result": "open exit 0 in 13-23 s; batch done and stop correct; hard kill took the child; lease retaken; parent gone detected in 11.5 s"},
      {"command": "probe: walk_values output through handoff_check --fix on the template", "result": "exit 1, 29-31 fields not filled"},
      {"command": "python -B scripts/tests/test_judgment_census.py", "result": "21/21 ok"}
    ]
  }
}
```
