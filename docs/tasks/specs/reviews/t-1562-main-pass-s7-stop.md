# t-1562 - why the dry main pass on main still stops "at S7" after FV3-23 (diagnosis)

Verdict: NEEDS WORK (main is red; 2 blocking findings, both outside FV3-23's own diff). FV3-23's fix IS on main and WORKS: the S7 analyst
passes. The pass now stops one role later, at the S8 doc scribe, which has no stub row; it is labelled "S7" because S7 closes only when the
S8 scribe accepts the analyst's triage. The fix direction is the same shape as FV3-23, one stage on. The decision belongs to the Lead.

## (a) The measured stop on the current main head

Local run, tree = root checkout, HEAD f8d132f7 (= origin/main; CI head edf16d9d is an ancestor, and the only package commit between them is
a53282d9 FV3-27, which does not touch the S7/S8 path). Command, run once:
`( cd C:/QAFactory/forge-repo && python -B ai-packages/qa-factory/scripts/tests/test_scenario_dry_1.py --part main )`, exit 1, 362.5 s.

- `PASS dry-1/main/S0` .. `PASS dry-1/main/S6` (S6 is now green)
- `FAIL dry-1/main/known_red -- stale: main/S6 is green; remove its known_red row (node FV3-23) in this commit`
- `FAIL dry-1/main/known_red -- new red: main/S7 -- fix it, or add "main/S7": {...} to ...driver-exits/known_red.json`
- The stop line, verbatim (ends with the driver's first refusal):
  `NOTE dry-1/main/stop: stopped at S7: the road met the conductor: a state the driver has no move for; its own words: # The factory's own words -- DRY-1, conductor at S8 ... exit gate for S8-qa-doc-scribe-1 (qa-doc-scribe, S8): 2 finding(s): - check_coverage.py: cases exist (4 total), but ...\qa-factory\records\coverage-map.md is missing -- the map was never built - digest: your final message is not the handoff form. ... the digest names no artifact path ...; TC-1 was in this dispatch's scope and has no line ...; TC-2 was in this dispatch's scope and has no line ... This is a repair, not a question for the person.`
- Stub calls: `S7-qa-failure-analyst-1 n=1 stage=S7 wrote=2 live_only=1` (handoff form + work/triage.json: FV3-23's row works);
  `S8-qa-doc-scribe-1 n=1 stage=S8 resume=False wrote=2 live_only=0` (form + test-report.md, the filler's defaults), then
  `S8-qa-doc-scribe-1 n=2 resume=True wrote=0` (the repair resume, nothing the stub can do). No `stub-fix` line, so `handoff_check --fix`
  exited 0 on the S8 form.
- Seconds per stage: `... 'S6': 39.7, 'S7': 24.5, 'S8': 11.0`; snapshots made S0..S6.

The CI agrees (run 44597046860, jobs 135820253794 and 135820254234): `prefix: reached S6 ...; stopped: the road met the conductor ... DRY-1,
conductor at S8` and `snapshots: S6: last closed S6; waiting at conductor (S8); stages ... S6 done, S7 pending, S8 running`. CI and local are
the same; the CI line is cut at 200 chars by `walk_exits` (dry_world.py:1498), so only the local run shows the S8 gate words.

So: the stub call that stops is `S8-qa-doc-scribe-1`, role `qa-doc-scribe`, stage S8.

## (b) The cause

1. **No stub row for `qa-doc-scribe@S8`.** `ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/story.json` holds stub rows
   for `qa-case-critic@S2/S3/S4`, `qa-code-critic@S5`, `qa-automator@S5`, `qa-failure-analyst@S7` (line 114, FV3-23) and
   `qa-case-designer@S4`. None for the S8 scribe. `dry_stub.fill_role` (dry_stub.py:991-1066) then falls back to the default result
   text (`"<role> <stage> <task> - the stub filled the handover form ..."`, dry_stub.py:1065), which is the digest the exit gate refuses
   (no TC-1/TC-2 lines, no path). This is the same defect as the one FV3-23 fixed at S7, one role later.
2. **Nothing runs `check_coverage.py --write`.** The scribe's brief tells the role to run it (brief_pack.py:292); the exit gate then runs
   `check_coverage.py`, which refuses a missing map (check_coverage.py:258-262). The map is a file that code builds, not one the role
   fills: `write_map` (check_coverage.py:218-231) writes the map AND its receipt, and the receipt binds the map's bytes. So a `files`
   override in the story cannot stand in for it: a hand-written map has no matching receipt (check_coverage.py:270-281). The stub has a
   table for exactly this class, `AFTER_STEPS` (dry_stub.py:46-47, run by `_after_steps`, dry_stub.py:976-989), but it holds only the S2
   tester's steps.
3. **Why it reads "S7".** `driver_stage_s7.py:173-184` (X7-6b): S7 closes ONLY at `s7.accepted`, when the S8 doc scribe accepts the
   analyst's triage (`CODE_CLOSE_SITES["s7.accepted"]`, driver_core.py:396). So while the S8 scribe is stuck, S7 stays `pending` and S8
   is `running`. `main_pass` labels the stop by the first stage that is not done (dry_world.py:1054), and `walk_exits` does the same
   (dry_world.py:1504), so the label is `main/S7`. FV3-23's own ledger row noted the same offset at S6 ("the walk row id it prints is
   still main/S6"), where S6 closes when the S7 analyst accepts it.

**Is FV3-23's fix present?** Yes. `git merge-base --is-ancestor 8fe80840 edf16d9d` is true; its parents 83d2a85f and 05931c97 add the
`qa-failure-analyst@S7` row (story.json:114-137); the local run shows the S7 call wrote 2 files and the stop moved from the S7 analyst's
gate (the verbatim line in known_red.json `main/S6`) to the S8 scribe's gate.

**Why it does not cover this stop.** FV3-23's scope was one stub row for the S7 analyst. Its build report says
`Not run locally: the dry story scenario file`, and `known_red.json` was declared a non-goal. Nobody measured the next stop before the
merge. As a result:
- the `main/S6` row went stale (S6 is green now), and the main pass's reconcile goes red on it;
- the new stop `main/S7` has no row, so every exits row that starts at S8 gets the FAIL `start S8 not made ... stopped at S7 with no known_red
  row` (dry_world.py:1512-1515). That covers `selftest/s8.delivery.no/go on` and the six `gate_B/*` rows. Before FV3-23 the stop stage was
  S6, which had a row, so those rows were NOTE `after:FV3-23`.

The pile row's own owns column names the label file (`метка -- .../driver-exits/known_red.json`, batch-3 line 52). The dispatch that made it
a non-goal is the gap (Finding 2).

## Findings

1. **F1 (blocks: main is red)** - `story.json` has no `qa-doc-scribe@S8` stub row, and `dry_stub.py:46` `AFTER_STEPS` has no
   `("qa-doc-scribe", "S8")` step for `check_coverage.py --write`. Input -> output: the main pass on f8d132f7 -> the S8 exit gate refuses
   with 2 findings, conductor, stop. Measured above.
2. **F2 (blocks: the label ledger is wrong both ways)** - `ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/known_red.json`
   line 4 `main/S6` (node FV3-23) is stale, and `main/S7` is missing. Measured: the two `main/known_red` FAIL lines above, plus the 7 exits
   FAILs in CI. `pins.known_red` stays 1 when S6 is swapped for S7.

## (c) Fix direction (one node; nothing in the pile owns it today)

I grepped `plans/piles/` (case-sensitive, `doc-scribe|qa-doc-scribe@S8|coverage-map`; the positive control is the same call, which found
`S8-qa-doc-scribe-1.yaml` in an execution-report finding). Nothing owns the S8 scribe stub row. Batch-3 has no S8 row (grep `S8|main/S7`
on batch-3 returned nothing; the pile-wide grep above found `S8-qa-doc-scribe-1.yaml` in execution-report findings, a positive control for the `S8` token). **A new node is needed (the Lead opens it, e.g. FV3-40).** It has two
parts, and both should land in one round.

- **Unblock (label, if the fix is not merged the same day):** in `known_red.json`, replace `main/S6` with
  `"main/S7": {"node": "<new node id>", "raised_by": "t-1562 critic: measured on f8d132f7, --part main: the S7 analyst passes (FV3-23); the pass stops at the S8 doc scribe's exit gate (no stub row qa-doc-scribe@S8: digest; records/coverage-map.md never built); S7 stays pending because it closes only at s7.accepted"}`.
  The pin stays 1. With this row, `walk_exits` turns the 7 S8 FAILs into NOTE `after:<node>` (dry_world.py:1513-1514).
- **Fix (builder -> critic). owns:** `ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/story.json` (new key
  `qa-doc-scribe@S8`), `ai-packages/qa-factory/scripts/tests/dry_stub.py` (`AFTER_STEPS` row `("qa-doc-scribe", "S8")`:
  `("records/coverage-map.md", "check_coverage.py", ["--write"])`; pass `--root` if the step's cwd does not resolve the project, which
  `run_script` sets to the project), `.../driver-exits/known_red.json` (remove/move the `main/*` row to wherever the pass stops next).
  **Edges the dispatch must state:**
  - Digest: one line per ledger row that is not `passed_green` (the gate's words). In this world TC-1 passed and TC-2 is
    `manual_skipped`, so the expected set is decided by the gate's own scope (it named TC-1 and TC-2), not by the stub.
  - The scribe's `stage_acceptance.verdict` = `accept` of the analyst's triage. This is what closes S7 (`s7.accepted`). Without it, S7
    stays pending even if S8 passes its gate.
  - The other scribe doors (`traceability.py --write`, `report_facts.py --write`, `ledger.py`; brief_pack.py:286-293) may be the next
    gate findings. The builder walks the S8 gate to its end in one run and names each one, as a step or a `live_only` row. It must not stop
    at the first.
  - **The next stop is predicted, not measured:** the story's driver walk rows hold NO answer for S8 (`walk_answers`: `S8 []`, `S9 []`;
    only `s1_review`, `gate_A`, `environment` exist). So after the scribe passes, the pass will stop at `no answer for gate_B at S8 (A1-E3)`
    (dry_world.py:938-943) unless the node adds the S8 answer row. Whether that row belongs to this node or a sibling is fork 2.
  - Witness: `--part main` once, showing `PASS main/S7`, snapshots including S7 (and S8 if S8 closes), and the ledger row moved to the
    measured new stop. "Not run locally" is not acceptable here: that is exactly the gap FV3-23 left.

## (d) Forks for the Lead

1. **Label now vs. fix only:** land the `main/S6 -> main/S7` swap on main now (it unblocks the tables and gates jobs of every run), or
   leave main red until the scribe node merges. Recommendation: swap now. A known stop with a node is the ledger's purpose, and
   7 unledgered FAILs hide other reds.
2. **Scope of the node:** the scribe stub row + coverage step only (stop moves to the gate_B answer), or also the S8 `gate_B` walk answer
   (the pass could reach S9). The evidence that the gate_B answer is missing is the walk rows read above. Including it costs one more
   unknown stop inside the same node.
3. **The stop label offset (S6 and S7 close at their consumer):** keep `main/S<first not done>` as the label, which is consistent and
   matches the ledger, or name the running stage in the stop line. This is a cosmetic choice and only a note. The ledger key must stay
   whatever `main_pass` computes.
4. **Process (calibration case):** FV3-23's dispatch made `known_red.json` a non-goal although the pile row owns it, and it accepted
   "not run locally" for the dry story. A ledgered stop fix whose acceptance does not re-measure the main pass leaves a stale and a missing
   label by construction. Proposal: the DoD of any node that owns a `main/S<n>` row names the `--part main` run as its witness.

## Standing questions (diagnosis gate: no diff under review)

- Q4 class: the same class as FV3-23 one stage on (consumer-closed stages: S6 closes via the S7 analyst, S7 via the S8 scribe). The
  remaining stub-less roles on the main road after S8 are unknown until measured (S9 retro). Named in fork 2 and the edges.
- Q6 duplication: the coverage map must come from `check_coverage.write_map` (the one writer), never a story `files` copy. None else
  found: grepped `check_coverage.*--write` over the package (7 hits, none in dry_stub).
- Q12 one road: the fix uses the stub's existing `AFTER_STEPS` table, not a new branch. None found.
- Probe: none (no diff).

## Trail

- `python -B tools/ci_read.py log 135820253794 --grep "S7"` / `--grep "stop"` / full via `--grep ""` (784 lines, grepped): the prefix,
  snapshot and FAIL lines quoted above. Job 135820254234: 6 `gate_B/*` FAILs + 6 `known_red` new red.
- `git -C <repo> merge-base --is-ancestor 8fe80840 edf16d9d` -> ancestor; `edf16d9d` ancestor of HEAD f8d132f7 = origin/main;
  `git log edf16d9d..HEAD -- ai-packages/qa-factory/scripts` -> a53282d9 only.
- `git show --stat 8fe80840^2` -> story.json + build report; `git log 8fe80840^1..8fe80840^2` -> 83d2a85f, 05931c97.
- Read: dry_world.py 880-1075, 1440-1525; dry_stub.py 33-47, 215-227, 706-726, 932-1066; driver_core.py 385-403; driver_stage_s7.py
  160-195; check_coverage.py 1-30, 205-265; brief_pack.py 285-296; story.json 114-137 + walk rows; known_red.json main/S6; FV3-23 build
  report; batch-3 lines 52, 62, 67-71; handoffs/s8-scribe-to-gate-b.yaml keys.
- Local run (once): `test_scenario_dry_1.py --part main` -> `=== scenario dry-1: 8/10 ok ===`, exit 1; lines quoted in (a).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F1: story.json has no qa-doc-scribe@S8 stub row and dry_stub.py:46 AFTER_STEPS has no (qa-doc-scribe, S8) check_coverage.py --write step; the S8 exit gate refuses (digest; records/coverage-map.md never built) and the main pass stops with S7 pending (S7 closes only at s7.accepted, driver_stage_s7.py:175-184). New node, owner the Lead; blocks main green.",
    "F2: driver-exits/known_red.json main/S6 (node FV3-23) is stale and main/S7 is missing; swap to main/S7 with the new node and raised_by t-1562 (pin stays 1); this turns the 7 S8-start exits FAILs into NOTE after:<node>."
  ],
  "class_completeness": "Same class as FV3-23 one stage on: consumer-closed stages (S6 by the S7 analyst, S7 by the S8 scribe). Next predicted stop after the scribe: no gate_B answer at S8 in the story walk rows (fork 2). Pile grep found no node owning S8.",
  "trail": {
    "read": [
      "ai-packages/qa-factory/scripts/tests/dry_world.py",
      "ai-packages/qa-factory/scripts/tests/dry_stub.py",
      "ai-packages/qa-factory/scripts/driver_core.py",
      "ai-packages/qa-factory/scripts/driver_stage_s7.py",
      "ai-packages/qa-factory/scripts/check_coverage.py",
      "ai-packages/qa-factory/scripts/brief_pack.py",
      "ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/story.json",
      "ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/known_red.json",
      "docs/tasks/specs/reports/20261118-fv3-23-build-report.md",
      "plans/piles/live-run-fvf/batch-3-live-run-fvf.md"
    ],
    "reruns": [
      {"command": "python -B ai-packages/qa-factory/scripts/tests/test_scenario_dry_1.py --part main (root checkout, HEAD f8d132f7)", "result": "exit 1; PASS main/S0..S6; FAIL main/known_red stale main/S6; FAIL new red main/S7; stop: conductor at S8, exit gate for S8-qa-doc-scribe-1: coverage-map.md missing, digest not the handoff form; scenario dry-1: 8/10 ok"},
      {"command": "python -B tools/ci_read.py log 135820253794 --grep S7", "result": "snapshots S5/S6: waiting at conductor (S8); S6 done, S7 pending, S8 running; FAIL s8.delivery.no/go on start S8 not made, stopped at S7"},
      {"command": "git -C C:/QAFactory/forge-repo merge-base --is-ancestor 8fe80840 edf16d9d", "result": "true (FV3-23 on main)"}
    ]
  },
  "mutants": [],
  "mutants_none": "diagnosis only: no diff under review, no tree named for a probe"
}
```
