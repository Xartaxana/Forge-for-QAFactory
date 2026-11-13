# Critic, diff gate: P1-v N4 run counters (020f1a9 + round 2 c9b2069)

Tree: `.claude/worktrees/p1v-topic`, branch wip/p1v-topic, tip c9b2069. Spec: `docs/tasks/specs/20261113-p1v-run-scoreboard-spec.md`
§2 (T1-U1, W1), §5 N-rework, §7, §8 N4. The round-2 spec is the Lead decisions D1-D6 in the dispatch.

## Verdict

**ACCEPT WITH FIXES.** Seven fixes. One blocks the merge (F1). The decision to accept belongs to the Lead.

The counters I recomputed by hand all match. The defects sit at the edges. Two edges print a measured number where
the honest answer is `unknown`, and two pick the wrong one of `n/a` and `unknown`. The rework line has no seconds,
yet the norm it feeds is a share of seconds. The T5 sub-row's name does not say what it measures.

## Control values (empirics first: fixture journal, hand arithmetic against `counters()`)

Fixture (probe `scratchpad/rc/probe.py`, built against the tip's `run_counters`). Window 1: end row only, since 10:00:00,
end 10:10:00, `question_kind: conductor`. Window 2: start 10:20:00, end 10:30:00, `answer_file: true`. Role calls (end
`ts`/`wall_ms`): r1 D1 10:02:00/60 000, first pass. r2 D1 10:05:00/120 000, resumed `handoff_findings`, checks
[s5:a, s5:b], `checks_n` {2, 1}. r3 D2 10:25:00/90 000, `person_answer`. r4 D2 10:28:00/30 000, `bogus`. Conductor call:
c1 10:08:00/30 000.

| counter | by hand | printed | |
|---|---|---|---|
| T1 wall / driver | 10:30-10:00 = 1800 s; windows 600 + 600 = 1200 s | 1800.0 / 1200.0, end_recorded True | match |
| T2 union | intervals [10:01,10:02] [10:03,10:05] [10:23:30,10:25] [10:27:30,10:28], disjoint: 60+120+90+30 = 300 s | union 300.0, sum 300.0 | match |
| T3 | c1 [10:07:30,10:08] overlaps no role: 30 s | 30.0 | match |
| T6 | gap 10:10 to 10:20 = 600 s; question posted + answer file -> person | n 1, 600.0 | match |
| T5 outside_hops | W1: 600-(60+120+30)=390; W2: 600-(90+30)=480; total 870 | 390.0, 480.0, total 870.0 | match |
| F1 rework | handoff_findings is in rework_kinds: 1; person_answer: non-rework 1; bogus -> unclassified 1 | returns 1, non_rework 1, unclassified 1 | match |
| F1 resumed / first pass | 3 calls 120+90+30 = 240 s; first pass 1 call 60 s | 3 / 240.0; 1 / 60.0 | match |
| G1 | r2 names two ids: one return each, 120 s each (shared), findings 2 / 1; total de-duplicated 120; r3, r4 carry no checks: 2 | s5:a {1, 120.0, 2}, s5:b {1, 120.0, 1}, total 120.0, without_checks 2 | match |

## Findings

**F1 (BLOCKS). T5 `outside_hops` counts a call it never subtracted as driver time and prints it as measured.** Location:
`run_counters.py:396-422`, `_outside_hops`. The function only subtracts outcome rows. It never sees `cut` (open
`launched` rows), which `counters` has already computed at :549.
- Probe A: a Ctrl-C window has an end row (N1 (d): `stopped_by_person`, then end with `process_code: null`). It holds a
  call launched at 10:01 that has no outcome. The run prints `T5 outside_hops measured 540.0`, while T1 says
  `end_recorded False, cut 1`. The 480 s of the open call (10:01-10:09) are reported as driver time outside the hops.
- Same surface (rule 14), second instance: the builder's silent decision 1. A call row with an unreadable `ts` counts as
  `calls_unplaced`, but every window stays `measured`. That call's `wall_ms` is therefore 0 s inside whichever window
  held it. Test row "a call with an unreadable time…" pins `measured 60.0`.
- Both break §7.1 ("its open call never adds invented seconds") and D3 ("an unmeasured call is never 0 s"). Both are an
  unknown printed as a fact (FR-41, AR-28).
- Fix: a window that holds an open `launched` row (by `started_at`/`ts`) becomes `unknown`, with the reason named. When
  `calls_unplaced > 0`, the row total becomes `unknown`; the per-window values stay listed with the note.
- Neighbours walked:
  - magnitude: negative values are handled per D3;
  - empty: a window with no calls gives its full seconds, which is correct;
  - a killed window: `unknown`, correct;
  - a call whose `ts` falls between windows (clock skew): silently in no window and not counted. Fold it into the same
    `calls_unplaced` count;
  - encoding: n/a.

**F2 (fix before merge). A journal whose lines are all unreadable prints `n/a`, not `unknown`.** Location:
`run_counters.py:558-566` and `:587-588`. D6 says `n/a` for "a run with no driver journal". The builder widened it to
"a journal with no readable row". Probe C: the file `{broken\nnot json` gives `F1 n/a | T5 n/a | U1 bad 2`. The driver
ran; its record is damaged. That is `unknown` (§7.6, FR-41), not "this row cannot exist". Fix: `n/a` only when
`not runs_present`, or when the file is present with zero non-blank lines. If `runs_bad > 0` and there are no rows,
the rows are `unknown`. Add a test row next to "D6 an empty journal file".

**F3 (fix before merge). A journal with rows but no `process` rows (every record older than N1) gives
`T5.outside_hops` `n/a`, while T6 and T7 say `unknown`.** Location: `run_counters.py:393-394`. Probe B prints
`T5o n/a | T6 unknown | T7 unknown`. §7.6: a carrier older than its writer is `unknown: <carrier> predates <writer>`.
T6 and T7 already do this (:240-243). Fix: return `unknown`, "the record predates the process rows". Re-pin the test
case "no process rows at all is n/a" and the "D6 control" check of `outside_hops` state in `test_retro_numbers.py`.

**F4 (fix before merge; spec fit, AR-13). `F1.rework` has counts only, no role seconds.** Location:
`run_counters.py:346-349`. The spec's F1 row is "First pass vs rework, calls and role seconds". §5 N-rework is "rework
share of role seconds", and F3 (a) makes run_counters the owner of the definition. With `returns` alone, N6 would have
to sum `by_kind` itself by re-reading `rework_kinds`, which is a second reader of the classification. Fix: give
`rework_row` `role_s` and `wall_unknown` for rework, non-rework and unclassified, using the existing `seconds()` helper.
Add one test row.

**F5 (fix before merge; the definition is the Lead's call). The name `outside_hops_s` does not say what it measures,
and it overlaps both T4 and `T5.unattributed_s`.** Location: `run_counters.py:386-432`, placed at :590.
- In `driver_timing._hops` (`driver_timing.py:227-238`) a hop is the stretch from a call's result to the next launch.
  Window minus calls therefore includes every hop.
- Probe 2: window 0-100, calls at 10-50 and 70-90, one 10 s step `finish` at 50-60. It prints T4 finish 10.0,
  `T5.unattributed_s` 10.0 and `outside_hops_s` 40.0. The 40 = head 10 + hop 20 (that is, 10 of T4 plus the 10 of
  `unattributed_s`) + tail 10.
- The spec's T5 cell asks for "time inside process windows outside any hop", which would be 20 here. D3 says "outside
  the windows of calls", which is 40. The builder followed D3 literally.
- Risk: a reader who adds the two T5 parts, or T4 + T5, counts the same seconds twice.
- Lead fork:
  - (a) keep D3's value, rename the key to `outside_calls_s`, and label it "contains T4 step time and the hops'
    unattributed_s; not additive";
  - (b) compute window minus calls minus hop walls, which matches the spec cell.
- Recommendation: (b). It is the only reading under which T5 stays additive.

**F6 (fix before merge; P31 / axis 34). With no driver journal, F1 also drops `controller_rounds`, which does not come
from the journal.** Location: `run_counters.py:565-566` against :572. `_controller_rounds` reads
`retro_numbers.dispatch_rounds`, the controller records. Those exist on the skill road as well, and F3 (a) defines
rework as resume_kind + controller rounds. A run with no journal therefore loses the critic-return half of its rework
measure, although the carrier is present. The shared mechanism never reaches that case. Fix: in the n/a branch attach
`out["F1"]["controller_rounds"] = _controller_rounds(task_root)`. Whether F1 as a whole stays `n/a` is the Lead's D6.

**F7 (fix before merge, small; duplication, AR-15). `_merge` / `_length` (`run_counters.py:78-89`, from 020f1a9)
re-implement `cost_capture.merge_spans` (`cost_capture.py:1663-1672`).** `retro_numbers.py:335` already reuses it as
`CC.merge_spans`. The commit line "AR-15 -- survivors called, not copied" does not hold for this helper. Fix: call
`CC.merge_spans` (it drops zero-length spans, which changes no length) and keep only the sum.

## Notes (queue, non-blocking)

- **N-a (code quality, Q7).**
  - Functions over ~60 lines in the new code: `_time_rows` :176-284 (109 lines), `_resume_rows` :308-383 (76),
    `counters` :533-600 (68).
  - `_outside_hops` :402-422 nests four levels (for / else / else / if).
  - Severity: queue, as a split when the F1/F5 fix touches it.
- **N-b (tests, Q5).** `run_counters_one_road_and_cli` pins the SOURCE text of `run_counters.py`: needles
  `DJ.run_record_names(`, `json.loads(` and others. That is a "pin on the source of a script" (the «не пишется» table
  in `docs/TESTING.md`). Round 2 re-edited the needle. Queue: replace it with a behavioural row, or drop it. The D-row
  tables otherwise kill the defects they target; the builder's mutation `max(0.0, …)` was caught (report :41-42).
- **N-c (analog outside owns).** The docstring at `driver_runner.py:777` still says "read ONLY through
  `driver_journal.run_record`", but the code reads through `run_record_names` (N2 area, already accepted). Line for
  «Остатки»: `driver_runner.py:777 docstring names run_record, code uses run_record_names | узел: <N2 follow-up, Lead opens>`.
- **N-d (D6 consistency, the Lead's question 2).** T1, T2, T3, T8 and G2 are journal-only just like F1, G1, T5, T6 and
  T7, yet they stay `unknown` when there is no journal. The builder implemented D6 to the letter and asked. The Lead
  decides. Related: with no journal but a present `driver-timings.jsonl`, T5 `n/a` discards a measured hop part
  (builder decision 3). A rare world, but also the Lead's call.

## Standing questions (one line each)

1. **Fit to the spec**: NEEDS WORK, see F1 (open call, D3 and §7.1), F2/F3 (§7.6 direction), F4 (spec F1 row
   "role seconds") and F5 (spec T5 cell against D3). D1 (data key; `unclassified` and strays give `unknown` + note), D2
   (text only; computation already per D2) and D4 (service_cut its own road) are implemented as written.
2. **Builder decisions**:
   - (1) unplaced call: wrong direction, folded into F1.
   - (2) `unclassified` in rework_kinds gives `unknown`: safe, accept.
   - (3) inside a window by END `ts`: accept. The end row is written in `finally`, so a call cannot straddle a window
     edge within one process.
   - (4) `[]` refused: accept, one strictness with the validator (`driver_journal.py:483`).
   - (5) T1 `unknown` with no journal: consistent with T2/T3/T8, accept, see N-d.
3. **Seams**:
   - `read_rows`, now `read_rows_counted(path)[0]`: the line loop is the same, so the rows are the same.
   - `run-record.json` gains a key; its two readers (`run_class`, `resume_kind_of`) read their own keys through
     `run_record_names`.
   - `test_driver_stop_record` gains two rows; `features.json` gains two lines.
   - Additive, nothing reordered: OK.
4. **Class-wide completeness**:
   - The class of F1 is "a call that is not subtracted from its window". It is walked in-artifact (cut call, unplaced
     ts, between-window ts).
   - Axis 6: the run_counters row is queued in spec §8.1 item 3 (Lead node «носители П1»). Grep shows `run_counters`
     absent from `docs/SIBLING_MAP.md`, as expected while it is queued.
   - Axis 18: none. Axis 29: n/a (no writer). Axis 34: F6.
   - The second definition of rework (`retro_numbers.resume_metrics`) is queued per spec C-11 / F3.
   - Analog: N-c.
5. **Tests**:
   - The D rows would catch D1, D3 negative and D6.
   - No row covers a cut call or an all-unreadable journal (to be added with F1/F2).
   - One source-text pin (N-b).
   - No new test file; `run_counters.py` is added to the keep covers of `test_retro_numbers.py`, and the layer
     (detector) holds.
6. **DUPLICATION AND CONSISTENCY**: F7 (`cost_capture.merge_spans`). Otherwise none found. I grepped
   `def _?(merge|union|interval|length)` case-insensitively over `scripts/*.py`; the positive control is that the same
   grep finds `cost_capture.merge_spans`. `rework_kinds|outside_hops` has readers only in run_counters and its tests.
   The raw parsers of driver-runs.jsonl that the builder reports (`friction`, `driver_timing`, …) are queued per spec §9.
   The clone ratchet output (forge-check) was not attached, so I did not read it. It belongs to the Lead's batch canon.
7. **CODE QUALITY**: N-a (queue), F5 (a name that does not match its value, fix before merge), F7. No dead branch
   found. The `outside_hops` string that round 1 left in T5 was replaced by the sub-row, and its only reader was the
   test in the same commit.
8. **Hygiene**: OK.
   - Committed blobs are LF, matching the base (`git show <rev>:<path> | grep -c CR` gives 0 for both); `eol: lf` attr.
   - No non-ASCII in `run_counters.py`, `run-record.json` or the changelog fragment. The one non-ASCII byte in
     `driver_journal.py` was already on base fa69bd1.
   - `--lang` 2/2 is the builder's run; I did not re-run it.
9. **IN-TREE RATCHETS**: none raised. `git diff ad4f7a6 c9b2069 --name-only | grep -iE "census|baseline|role-load|dup-|lint"`
   returns nothing (exit 1). The only `test-layers.json` change is a `covers` entry in the keep row of
   `test_retro_numbers.py`, which is not a ratchet row.
10. **ARCHITECTURE**:
    - Named in the commits: AR-1, AR-13, AR-15, AR-22, AR-23, AR-28.
    - AR-22: `rework_kinds` has its reader in the same commit. OK.
    - AR-13: both lists go through `run_record_names`. OK.
    - AR-15: the claim fails for `_merge` (F7).
    - AR-12: touched (run_counters is a measurer, per its docstring) but not named on the commit lines. Minor; the
      spec's §8.1 carries the AR-12 detector line.
    - No producer was removed.
11. **JUDGMENT**: none moved. Which roads count as rework is a Lead-signed data row; no census row, `blocks_override` or
    scan constant was touched. `judgment: none` holds.
12. **ONE ROAD**: F6, the skill road does not reach `controller_rounds`. Fix in this round (F6).
    - dry/smoke → T9/T10 `n/a` is a data row (`run_classes`) sanctioned by §7.9.
    - `stub-` is the safety net named in spec §2 W1.
    - No language or project branch: I read the whole of `run_counters.py`.

## Spot-checks of the submitter's claims

- "test_retro_numbers 265/265": re-run on c9b2069, result `=== test_retro_numbers: 265/265 ok ===`.
- "test_selftest_slow_tests 123/124 is a red already on the base": consistency check instead of a run. The failure
  names the keep rows `test_app_card_stand_lessons.py` and `test_place_of_draft_observation.py`. Both rows are
  byte-identical at `ad4f7a6~1` and at `c9b2069` (covers `["app_card.py","project_knowledge.py"]` and
  `["place_answers.py","references/artifact-contract-run.md"]`). Over that range the diff to `test-layers.json` is the
  one added covers line. The red cannot come from this diff. Holds.
- "no other hand reader of run-record.json lists": a case-insensitive grep of `run-record\.json|RUN_RECORD_PATH|run_record\(`
  over the package finds only `driver_journal` (loader and validator), `driver_runner` (docstrings, N-c) and test pins.
  The positive control is that the same grep finds the loader at `driver_journal.py:461`. Holds.
- "D2 no computation change": confirmed in the c9b2069 diff; only the comment and `shared_note` text changed.

## Trail

- Read:
  - `docs/tasks/critic-diff-brief.md`
  - spec §2 :170-269, §5 :344-368, §7-§8 :383-469
  - both builder reports
  - `git show c9b2069` (product part, tests), `git show 020f1a9` (`driver_journal.py`, `test-layers.json`)
  - `run_counters.py` whole (tip)
  - `driver_journal.py` :323-338, :474-514
  - `driver_timing.py` :222-287
  - `cost_capture.py` :1655-1672
  - `tools/critic_verdict.schema.json`
- Probes (scratchpad, read-only against the tree):
  - `probe.py`: the control table above; A prints `cut-call window: measured 540.0 T1 end_recorded False cut 1`;
    B prints `old run: T5o n/a | T6 unknown | T7 unknown`; C prints
    `all-broken journal: F1 n/a | T5 n/a | U1 bad 2 | why the driver journal has no readable row`; D (no journal)
    prints T1/T2/G2 unknown and T5/T6/T7/F1/G1 n/a.
  - `probe2.py`: `T4 {'finish': {'n': 1, 'seconds': 10.0, 'errors': 0}}`, `T5 unattributed_s 10.0 hops 1`,
    `T5 outside_hops_s 40.0`.
- Control re-run (the one allowed): `python -B scripts/tests/test_retro_numbers.py` (cwd: the package, in a subshell)
  gave `=== test_retro_numbers: 265/265 ok ===`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F1 run_counters.py:396-422 _outside_hops ignores open launched calls (cut) and unplaced call rows: a Ctrl-C window with an open call prints T5 outside_hops measured 540.0 (probe A) - an unmeasured call counted as 0 s, against spec 7.1 and Lead D3"
  ],
  "fixes": [
    "F1 (blocks) run_counters.py:396-422: a window holding an open launched row -> unknown with reason; calls_unplaced > 0 (and calls in no window) -> row total unknown; add test rows",
    "F2 run_counters.py:558-566,587-588: n/a only when the journal file is absent or has no non-blank line; a journal whose lines are all unreadable -> unknown; add a test row",
    "F3 run_counters.py:393-394: journal rows but no process rows -> T5.outside_hops unknown (predates the process rows), as T6/T7; re-pin the two test checks that pin n/a",
    "F4 run_counters.py:346-349: F1.rework carries role_s and wall_unknown for rework / non_rework / unclassified (N-rework is a share of role seconds; one owner of the definition)",
    "F5 run_counters.py:386-432,590: outside_hops_s contains hop time (T4 steps and T5.unattributed_s; probe2 40 vs 20); Lead fork: rename and label non-additive, or compute window minus calls minus hop walls (recommended)",
    "F6 run_counters.py:565-566: with no journal, still attach F1.controller_rounds from retro_numbers.dispatch_rounds (skill road keeps the critic-return half of rework)",
    "F7 run_counters.py:78-89: reuse cost_capture.merge_spans (cost_capture.py:1663) instead of the local _merge"
  ],
  "class_completeness": "Class of F1 named (a call not subtracted from its window) and walked inside the artifact: cut call, unreadable ts, ts between windows. Axis 6 run_counters row queued in spec 8.1 item 3; axis 18 no raise (grep over the diff file list empty); axis 29 n/a; axis 34 finding F6. Analog outside owns: driver_runner.py:777 stale docstring (line for Ostatki, Lead opens the node). Second rework definition retro_numbers.resume_metrics queued per spec C-11/F3.",
  "trail": {
    "read": [
      "docs/tasks/critic-diff-brief.md",
      "docs/tasks/specs/20261113-p1v-run-scoreboard-spec.md (2, 5, 7, 8)",
      "docs/tasks/specs/reports/20261113-p1v-n4-report.md",
      "docs/tasks/specs/reports/20261113-p1v-n4r2-report.md",
      "ai-packages/qa-factory/scripts/run_counters.py (tip, whole)",
      "ai-packages/qa-factory/scripts/driver_journal.py:323-338,474-514",
      "ai-packages/qa-factory/scripts/driver_timing.py:222-287",
      "ai-packages/qa-factory/scripts/cost_capture.py:1655-1672",
      "git show c9b2069; git show 020f1a9 (driver_journal.py, test-layers.json)",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B scripts/tests/test_retro_numbers.py (cwd ai-packages/qa-factory of the p1v-topic tree)", "result": "=== test_retro_numbers: 265/265 ok ==="},
      {"command": "python -B scratchpad/rc/probe.py (fixture journal, control values and probes A-D)", "result": "all hand values match; A measured 540.0 with cut 1; B T5o n/a vs T6/T7 unknown; C all-broken journal F1/T5 n/a"},
      {"command": "python -B scratchpad/rc/probe2.py (hop overlap)", "result": "T4 finish 10.0, T5 unattributed_s 10.0, outside_hops_s 40.0"},
      {"command": "git show ad4f7a6~1 / c9b2069 : test-layers.json rows of the two failing keep files", "result": "identical on base and tip; the slow_tests red predates the diff"}
    ]
  }
}
```
