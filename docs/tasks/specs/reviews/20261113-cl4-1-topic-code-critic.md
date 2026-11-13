# CL4-1 topic code critic (N1, N2, N4): one pass, R13-g

Reviewed: N1 `wip/cl4-1-n1` e7dee9e, N2 `wip/cl4-1-n2` 482b9db, N4 `wip/cl4-1-n4` b7cf9b8 (on N2, with the Lead's `select_transcripts` fix), base 22c3948.
Spec: `docs/tasks/specs/20261113-cl4-1-collect-stalled-looped-spec.md`. Brief: `docs/tasks/critic-diff-brief.md`.

**Verdict: fit_with_fixes.** No blocking finding. Two small fixes before merge (F1 is code, F2 is commit text). Four node lines for the Lead to queue (Q1-Q4). The money row passes on empirics. B1 and B2 of the plan critic are closed as written. The real unknown stall is still worded "stalled" (Q1). The spec froze those bytes, so Q1 is a node for the Lead, not a merge blocker.

## Fixes

- **F1, N4, before merge.** `tools/collect_intake.py:679`: `if got is None or got == []` treats an explicit `null` like an absent key, so `"loop_ignored": null` prints nothing. The spec's edge row says "key absent, or `[]` → no line; not a list → `<label>: unreadable (<type>)`", and `null` is not a list. Probe: `{"stalled": False, "looped": True, "loop_ignored": None}` gives `'stalled: no\nlooped: yes'`. It should add `loop ignored: unreadable (NoneType)`. Fix: `if key not in story or got == []`, plus one row in the I-cases of `test_the_layout_text_of_a_looped_only_story_says_stalled_no` (the same battery, broken type). Severity: fix before merge. A broken manifest should not read as clean.
- **F2, N1, at merge.** The N1 commit says `architecture: AR-1, AR-13, AR-22`. The spec's DoD line, and the AR the diff actually touches, are `AR-1, AR-14, AR-22`: the row goes through `journal_run` → `_append_jsonl`, one writer. AR-13 is not touched. Brief question 10: an AR that is touched but not named is a finding. Put the corrected line in the merge commit or the `accepted` note. Low severity.

## Node lines for the Lead (queue; outside the owns or decided by the spec)

- **Q1 (collect, M2 class; FR-41, FR-10).** The real unknown stall is still worded "stalled". `judge` writes its unknown stall as `stalled: True` with only the `unreadable` signal (`collect_stall.py:_verdict`; the "no activity time" reason). The packer's exception verdict has the same shape (`collect_pack.py:1111`). The packer writes `item["stalled"] = None` for both (`:1116-1117`). But `loop_state(verdict)` reads `True` → YES, so the gap says `no transcripts for the stalled story X` (`collect_pack.py:1137`) with why `the story is stalled` (`collect_stall.py:539`, `:575`). One manifest then says `stalled: null` and "stalled" at once. B2 covered only non-bool values. This is the reachable case of the same class, and J1's own story is exactly it. The spec froze the bytes for "every verdict judge can produce" (N2 edge row 1, FR-14), so the fix needs a Lead decision on the quarantined pins. Direction: classify the word sites on the item (or teach `loop_state` the unreadable-only shape). Fold in: `collect_pack.py:1118` writes a missing `looped` as `null` (unknown), while `loop_state` reads it as NO (hand-made verdicts only). `<what> | узел: <id to open in pile collect>`.
- **Q2 (collect intake; spec §7, confirmed).** `stall_elements` prints `where`/`why` from an untrusted manifest without `clean()`. A newline forges lines. Probe: `where = "a\x1b[2Jb\nfake: line"` gives `'...loop ignored: 1\na\x1b[2Jb\nfake: line | y'`. The signal lines predate this. N4 adds two lists to the same surface. Fold in: a list of only non-dict entries prints `loop ignored: 0` (probe `[1, 2]`), which hides two broken entries. Non-goal of N4. Node in pile `collect`.
- **Q3 (measurers, axis 6).** `experiments/measurers/compare.py:266-284` `driver_report` counts every journal row as a call under `by_kind`/`by_role`. `window_round` and `process` show up as call buckets, and so do `launched` and `gate_repair` (pre-existing). This is the same class as `report_run.journal` (`:141-158`), which the spec already queues. Add `compare.driver_report` to that node.
- **Q4 (evidence carrier).** The N1 report is uncommitted in its worktree. The Lead commits or files it with the acceptance.

## Answers

1. **Fit per node.** N1: both rows sit in the spec's positions: the stop row inside the dedup block after `save_state()` and before `no_move`; the round row after `:406` and before `number =`. Keys: no `is_error`/`exit_code`/`infra`/`session_id`. L2 is a data row, both kinds are in `no_call_kinds` with their `why`, the docstring is the spec's text, the `refusal_rig` stub is in, and the P1 tuple is in. N2: `loop_state` uses identity, `_WHY`/`_STATE_WORDS` match the spec's eight keys each, and the `_l_records` split leaves every helper at nesting ≤ 2. The spec's `Packer` is `_Run` in code, and `_l_records` returns the signal list: naming only, the behavior is right. N4: steps 1-5 are as written except F1. **B1 is closed**: empirics below. **B2 is closed as written**: no non-bool `stalled` is worded "stalled" (my D2 re-run, 0 violations). The reachable neighbor class stays open (Q1).
2. **Readers of the driver journal.** I walked the hits of `_journal_paths|read_rows(|driver-runs.jsonl|RUNS_NAME|driver_runs`, case-insensitive. None misreports:
   - `task_price`: fixed by the data row.
   - `run_counters`: counts by kind; `:649` counts rows with no kind only; its stamps only widen the time span inside the run.
   - `driver_journal.parse_driver_runs` and `retro_numbers` `:190`/`:472`/`:1866`: bind by `session_id` or `kind == role`.
   - `dispatch_liveness:798` and `driver_timing:255`: need `exit_code`.
   - `walk_timing:85`: needs `launched`/`exit_code`/`session_id`.
   - `friction:643`: `kind == role`.
   - `story_progress._spend:405`: a set of `dispatch` ids. The row's `dispatch` is the refused role's own id, so the set gains nothing.
   - `driver_runner.thread_total`: `session_id`.
   - `collect_stall`: `_is_outcome` (W5) and the kind-scoped L2/L3.
   - The other modules in the grep (`device_stand`, `reporters`, `run_suite`, `probe_by_code`, `branch_accounting`, `red_sandbox`, `run_history`) only matched names of other readers.
   - Outside the package: `report_run.journal` (queued) and `compare.driver_report` (Q3) inflate call counts; `stage_role_table`, `spend_by_dispatch`, `context_shape` and `code_friction` filter on session or kind.
   - The N1 builder's list of other kinds: every `journal_run({"kind": "<literal>"` writer in the package (delivery, launched, gate_repair, trace_failed, rows_given_up, stopped_by_person, note, process, window_round) is now in `no_call_kinds`. The only variable kind (`driver_runner.py:954`) is the end row of a call, which carries its session. So the money class is closed.
3. **W4 and P1 are real defect rows.** P1: on main's kinds file, a journal with 2 `process` and 2 `window_round` rows prices `incomplete`, 4 rows without a session. On N1's file it prices `agrees`, 0. W4, reader half: on main's `collect-loops.json` the journal rows give `looped: False` and no signals. On N1's table they give the two signals W4 asserts. W4, writer half: red by construction, because the old `window_round_gate` has no `journal_run`, so W1/W4 filter an empty list. I did not run it: `test_story_run_*` is batch canon.
4. **AR-13.** In N4 the grep `\["looped"\]|get\("looped"|get\("stalled"|\["stalled"\]|"looped" in|"stalled" in` (case-insensitive) over `*.py` finds, in product code, only `collect_stall.py:527` (the body of `loop_state`), the two allowed `collect_pack.py:1117-1118`, and the spec's kept old-archive condition `collect_intake.py:689`. Positive control, same call: about 50 hits in the quarantined tests. Error direction: every non-bool value is UNKNOWN and packs. A non-dict is not packed and is worded "neither", as before. `{}` packs with "not known" words (spec). Nothing is dropped. The word fault is Q1.
5. **The Lead's fix.** The place is right: `collect_stall.py:558-560`, the gate on the original argument, the one coercion site. `wants_transcripts(non-dict)` was already (NO, NO). My D2 re-run (base byte copies, sha256 equal to N2's "old", against the N4 head; two processes, `__file__` printed): 47 rows, 31 deltas, 0 violations. Non-dicts `'str'`, `None`, `[]`, `0` are unchanged; `{}` gate False → True. So (i)-(iii) hold. N2's "33 delta rows" cannot be right: its grid has at most 30 non-bool rows plus `'str'`. My re-run replaces that count.
6. **Battery.** I1-I5 and I7-I10 are in one table (task id per row), I6 sits in the layout-count test, J1 in the real-pack test. I9 has 1000 entries carried whole (the spec sets no cap, so no AT case). The builder check "name the `part_max_bytes` cases, file:line" is not in the report (a small DoD miss). The `clean()` analog is not a fix before merge: it is the spec's non-goal and the class predates N4. It becomes node Q2.
7. **Old data.** An old archive has no list keys, so it prints no line. Its bytes are unchanged and its `csha` stays stable (I2 and the T1-T3 asserts). "none" is never printed. An old journal has no `window_round` rows: L2 matches nothing, and no reader counts rounds (`window_round` appears only in the writer, the two data files and tests). No false "zero rounds".
8. **Merge.** `git merge-tree` reports no conflict between N1 and N4 (both edit `collect_stall.py`: N1 the docstring, N4/N2 functions). N1+N4 onto `origin/main` 12317b6 also merges clean (main moved by one report file since 22c3948). The merged behavior is checked: the N4 collector with N1's table gives `('no', 'yes')` and the L2 journal signals. The topic may merge after F1, carrying F2's line. N3 follows; its fragment text matches the accepted behavior.

## Standing lines

- **Fit to spec:** yes except F1. **Builder decisions:** `ignored_lines(label, key)` and the dict `make_element`: safe.
- **Seams:** additive; `collect_stall.py` is disjoint by function. FV1-22 N3 must keep N1's two `journal_run` calls (spec §3).
- **Class completeness:** money kinds closed. Reader walk done (Q3). Pair sites: 4 of 4 through `loop_state`. Open neighbors are queued (Q1, Q2).
- **Tests:** W1, W4, W5 and P1 would catch the node's defect through the real driver, collector and price. J1 is a real producer → reader join. No new file, no receipts.
- **DUPLICATION AND CONSISTENCY:** none found. Grepped the pair-reading pattern (above) and `journal_run(` kind writers. `_WHY` and `_STATE_WORDS` are two sentence tables by decision F-2. The four list copies in `_Run._stall` share one form by spec. I did not read the clone ratchet (forge-check on CI, batch level).
- **CODE QUALITY:** no new function over 60 lines or nested deeper than 3. `ignored_lines` is a closure rebuilt per story (harmless). `is_dict` partly overlaps what `loop_state` does for non-dicts (harmless, readable).
- **Hygiene:** `selftest --lang` passes on both builders' reports. ASCII.
- **Ratchets:** no row added. `test_driver_layers` 283/283 (N1).
- **ARCHITECTURE:** AR-1, AR-14 (F2), AR-22 and AR-13, AR-21, AR-23 and AR-28 are kept.
- **JUDGMENT:** none moved into code: decisions are by identity and data rows. No census row.
- **ONE ROAD:** none found. Grepped stage, language and project literals in the diff: the L2 row has no stage filter, and `loop_state` is the one classifier at all four sites.

## Trail

- **Read:**
  - The spec, whole.
  - The brief.
  - The plan-critic verdict: B2 sections and JSON.
  - The three builder reports.
  - `git show` of e7dee9e, 482b9db, b7cf9b8.
  - N1 `test_task_price.py:28-132` and `:1000-1080`; `task_price.py:285-320`, `:545-600`; `driver_journal.py:445-460`, `:548-592`; `driver_runner.py:407-419`, `:655-672`.
  - `dispatch_liveness.py:795-815`, `story_progress.py:404-428`, `:485-492`; `driver_timing`/`friction`/`walk_timing` windows; `retro_numbers.py:186-215`, `:466-490`, `:1862-1880`; `run_counters.py:100-165`, `:570-660`.
  - `compare.py:266-284`, `stage_role_table.py:198-215`, `report_run.py:138-160`.
  - N4 `collect_pack.py:1084-1143`, `collect_stall.py:326-345`, `:496-516`, `collect_intake.py:113`, `:584-588`.
  - `SIBLING_MAP.md` axis headings 5, 6, 14, 29, 34.
  - `critic_verdict.schema.json`.
- **Ran:**
  - The price probe, before and after, with an unknown-kind control.
  - The collector probe on main's and N1's tables.
  - The D2 re-run from base to the N4 head.
  - The N4 collector on N1's table.
  - The intake probes (null, non-dict entries, control bytes and newline).
  - `pytest tools/test_collect_intake.py` in N4 (import bound to N4, checked).
  - `git merge-tree` for N1×N4 and for N1+N4 onto main.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Money: every literal journal_run kind in the package is now in no_call_kinds (window_round, process added); the variable kind at driver_runner.py:954 is the call end row with its session. Readers of driver-runs.jsonl walked: none in the package misreports; measurers compare.driver_report and report_run.journal inflate call counts (axis 6, queue Q3). Pair: four of four sites through loop_state, AR-13 grep with positive control. Open neighbors queued: the real unknown stall (stalled True plus unreadable only) still worded stalled at collect_pack.py:1137 and collect_stall.py:539/575 (Q1, spec froze bytes); intake element text not cleaned, newline forges lines (Q2).",
  "fixes": [
    "F1 N4 before merge: tools/collect_intake.py:679 explicit null list prints nothing; use key-not-in-story or empty list for no line, null prints label: unreadable (NoneType); add one I-row in test_the_layout_text_of_a_looped_only_story_says_stalled_no",
    "F2 N1 at merge: architecture line names AR-13 instead of AR-14 (spec DoD: AR-1, AR-14, AR-22); carry the corrected line in the merge commit or the accepted note",
    "Q1 queue, node in pile collect: unknown stall (judge stalled True with only the unreadable signal; packer exception verdict) worded stalled by _WHY/_STATE_WORDS while the manifest item says stalled null (collect_pack.py:1116-1118, 1137; collect_stall.py:539, 575); needs a Lead decision on the frozen bytes",
    "Q2 queue, node in pile collect: stall_elements prints untrusted where/why without clean(); a newline forges lines; a list of only non-dict entries prints a count of 0",
    "Q3 queue, measurers node: experiments/measurers/compare.py:266-284 driver_report counts bookkeeping rows as calls; join the queued report_run.journal node",
    "Q4: commit or file the uncommitted N1 report with the acceptance"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-cl4-1-collect-stalled-looped-spec.md",
      "docs/tasks/critic-diff-brief.md",
      "docs/tasks/specs/reviews/20261113-cl4-1-plan-critic.md (B2 sections, json)",
      "three builder reports (n1, n2, n4)",
      "git show e7dee9e, 482b9db, b7cf9b8",
      "task_price.py:285-320,545-600; tests/test_task_price.py:28-132,1000-1080",
      "driver_journal.py:445-460,548-592; driver_runner.py:407-419,655-672",
      "dispatch_liveness.py:795-815; story_progress.py:404-428,485-492; retro_numbers.py:186-215,466-490,1862-1880; run_counters.py:100-165,570-660",
      "experiments/measurers/compare.py:266-284; stage_role_table.py:198-215; report_run.py:138-160",
      "n4 collect_pack.py:1084-1143; collect_stall.py:326-345,496-516,539-575; tools/collect_intake.py:113,584-588,662-695",
      "docs/SIBLING_MAP.md axes 5, 6, 14, 29, 34; tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "price probe: task_price on a journal with role a1 $1.00, conductor c1 $0.50, 2 window_round, 2 process rows; kinds file of 22c3948 vs N1", "result": "before: incomplete, rows_without_session 4; after: agrees, 0; totals a=b=1.5, sum by agents equal both; control with one unknown kind: incomplete, 1"},
      {"command": "collect_stall.judge on window_round journal rows with collect-loops.json of 22c3948 vs N1", "result": "main: looped False, no signals; N1: looped True, signals 'driver-runs.jsonl window_round row same_set' and '... cap'; gate_repair row with outcome cap not matched; stall signals 0"},
      {"command": "D2 re-run: base byte copies (sha256 8171f06d.., c0788b86..) vs N4 head, two processes, grid 7x6 plus non-dicts and {}", "result": "rows 47, deltas 31, violations 0; non-dicts unchanged; {} gate False->True with not-known words"},
      {"command": "N4 collector with N1 collect-loops.json", "result": "loop_state ('no','yes'), L2 journal signals present, why 'the story looped'"},
      {"command": "intake probes on tools/collect_intake.stall_elements (N4)", "result": "loop_ignored null -> no line (F1); [1,2] -> 'loop ignored: 0'; ignored dict -> 'unreadable (dict)'; newline in where forges a line (Q2)"},
      {"command": "python -m pytest .claude/worktrees/cl4-1-n4/tools/test_collect_intake.py -q", "result": "76 passed in 8.93s (import bound to the N4 collect_intake and collect_stall)"},
      {"command": "git merge-tree --write-tree e7dee9e b7cf9b8; then N1+N4 onto origin/main 12317b6", "result": "exit 0 both, no conflict"}
    ]
  }
}
```
