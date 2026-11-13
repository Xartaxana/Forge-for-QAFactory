# t-357 scout report: time split of the factory arm, LR2-1 (verbatim hand-back, 13.11.2026)

All numbers below were computed by scripts from the run files. The only thing I labelled by hand is which pauses between driver runs were operator work (rows marked "notebook label").

## Sources and what is missing
- **Tree used:** `C:\QAFactory\forge-repo\experiments\mybooks\factory-vs-free-agent\runs\` (main tree). The findings-1413 worktree has no `factory-N.log`, `free-N.log` or `.err.log`. Its `driver-runs.jsonl` is byte-identical to the main one (sha256 prefix 79b0d54104206b6b both).
- **`driver-timings.jsonl` does not exist** in either tree. `factory-out\state\` holds only `driver-runs.jsonl`, with no events, questions or pipeline files.
- **Fields I used from `driver-runs.jsonl`:**
  - 243 lines: 120 `launched`, 81 `role`, 39 `conductor`, 3 `gate_repair`.
  - `ts` (end of call, UTC), `wall_ms`, `duration_ms`, `stage`, `role`, `dispatch`, `session_id`, `resumed`, `num_turns`, `total_cost_usd`, `resume_reason`.
  - A call starts at `ts − wall_ms`.
  - `retry` is always 0 and `infra` is always null, so neither is usable.
- **Driver windows:** each `factory-N.log` was created when the driver was restarted and last written when it exited, so create time is the answer-taken moment and last-write time is the question-shown moment. The 40 logs are the 40 driver questions.
- **Per-question fields:** `kind`, `stage` and `asked_at` come from each log's `# Driver question` header. Brief sizes come from `note: brief: … (N B …)` lines.
- **Timezone:** the jsonl and `asked_at` are UTC; the machine and notebook are UTC+1. Proof: `asked_at` 16:39:11Z equals the log's last-write time 17:39:11. I converted the jsonl to local by adding 1 h.
- **Wall:** 17:39:08 to 00:57:20 = 7:18:12 = 26,292 s.
- **No timing file on what the tools were doing:** nothing records code-step durations directly. "Code" below is a residual, meaning driver-process time with no model call running.

## Table 1. Per stage (seconds, local-clock partition; the rows sum to 26,292)
The stage of a moment is the stage of the latest-started call. Pauses between driver runs go to the stage named in that question's `stage:` field. Gate-A conductor calls are their own row "gA". "wall" is `wall_ms`; "dur" is `duration_ms` as recorded.

| Stage | Stage wall (s) | Role calls (new sessions + resumes) and role time, wall / dur (s) | Conductor calls, wall (s) | Code (s) | Human wait (s) | Operator-labelled (s) | Questions | Gate returns | Resumes after a person answered | Repeat dispatches (distinct dispatch ids minus 1, per role) |
|---|---|---|---|---|---|---|---|---|---|---|
| S0 | 230 | none | 0 | 25 | 205 | 0 | 2 | 0 | 0 | 0 |
| S1 | 183 | scout 2 (1+1): 122 / 115 | 0 | 19 | 41 | 0 | 1 | 0 | 1 | 0 |
| S2 | 1736 | tester 5 (3+2): 1128 / 346; case-critic 5 (4+1): 215 / 198 | 5 calls, 167 | 120 | 97 | 0 | 2 | 2 | 1 | 5 |
| S3 | 921 | strategist 7 (3+4): 550 / 522; case-critic 2: 107 / 100 | 0 | 177 | 82 | 0 | 1 | 3 | 1 | 3 |
| S4 | 1545 | designer 3 (2+1): 424 / 410; case-critic 5 (3+2): 316 / 293 | 2 calls, 100 | 281 | 420 | 0 | 3 | 2 | 1 | 3 |
| gA | 96 | none | 1 call, 84 | 12 | 0 | 0 | 0 | 0 | 0 | 0 |
| S5 | 15006 | automator 35 (9+26): 3586 / 3404; code-critic 11 (8+3): 1491 / 1444 | 27 calls, 1393 | 1258 | 1615 | 5996 | 30 | 23 | 6 | 15 |
| S6 | 1598 | runner 2 (2+0): 739 / 722 | 0 | 859 | 0 | 0 | 0 | 0 | 0 | 1 |
| S7 | 4977 | failure-analyst 4 (4+0): 2386 / 2267 | 4 calls, 998 | 1591 | 0 | 0 | 1 | 0 | 0 | 3 |

- **Stage spans (first call start to last call end):**

| Stage | Span |
|---|---|
| S1 | 172 s |
| S2 | 1717 s |
| S3 | 1886 s |
| S4 | 1937 s |
| gA | 83 s |
| S5 | 14859 s |
| S6 | 1411 s |
| S7 | 4610 s |

  S3 and S4 overlap because the conductor sent S3 back from S4.
- **S5 vs the notebook:** the notebook's "248 min" is the 14,859 s span (247.7 min). Inside it, my partition shows role 4731, conductor 1406, code 1258, human 1615, operator-labelled 5996.
- **Model time in S5, two ways:**

| S5 role time | Seconds |
|---|---|
| Per-session sum | 5077 s (the notebook's 108 min is 6471 s, which is roles plus conductor, 3586+1491+1393) |
| Union (parallel sessions counted once) | 4731 s |

- **Gate returns** are resumed calls whose `resume_reason` is not "the person answered…". A critic rejection shows up only as a later dispatch id, not as a separate count.
- **The 40 questions, by kind:**

| Kind | Count | Where |
|---|---|---|
| conductor | 12 | |
| repair_limit | 7 | all S5 |
| exit_limit | 6 | all S5 |
| refusal | 5 | all S5 |
| halt | 2 | S0 |
| questions | 2 | |
| gate_A | 2 | |
| environment | 2 | |
| s1_review | 1 | |
| stand_identity | 1 | |

## Table 2. Whole run, 7:18:12 = 26,292 s

| Part | s | h:mm:ss | % | Basis |
|---|---|---|---|---|
| (a) role model time | 10734 | 2:58:54 | 40.8 | union of role calls by `wall_ms` (`duration_ms` sum is 9821 s) |
| (b) conductor model time | 2760 | 0:46:00 | 10.5 | conductor calls not overlapped by a role (raw sum 2742 s wall / 1922 s `duration_ms`) |
| (c) code steps | 4342 | 1:12:22 | 16.5 | residual inside driver windows |
| (d) waiting for a human | 2460 | 0:41:00 | 9.4 | gaps between runs not labelled operator work |
| (e) operator stops and patches | 5996 | 1:39:56 | 22.8 | notebook label |
| (f) unaccounted | 0 | | | zero by construction |
| Sum | 26292 | | | wall 26292, difference 0 |

- **Driver windows vs gaps:** driver windows total 17,793 s (4:56:33) and the pauses between runs total 8,498 s (2:21:38). The (d)+(e) figures are 34 s off these because I did not count the boundary seconds of each gap.
- **Operator-labelled gaps (notebook label):**

| After run | Gap (s) | What the notebook says |
|---|---|---|
| 12 | 2089 | stop, owner words, FV1-1 patch |
| 13 | 1129 | operator restored stand |
| 14 | 772 | operator edited config |
| 16 | 272 | operator probe and selectors edit |
| 22 | 733 | owner "fix and continue", t-180 |
| 23 | 932 | t-185 diagnosis, t-186 patch |
| 39 | 74 | operator `manifest_put` fragment |

  Together these are 6,001 s. The files cannot separate owner decision time from patch time inside a gap.
- **What (d) is:** the other 32 gaps, from 28 to 267 s each, are the time between the driver exiting with a question and the next driver start. That is the operator reading and composing the answer; the files do not say who or why.
- **Driver exits on a question.** There is no waiting inside the driver process, so every "wait" is a gap.
- **Role sessions overlapped in time** for 371 s (S5 windows 1 and 2).

## Table 3. First pass vs rework (role wall seconds / calls)
- **First pass:** the first call of a dispatch that no earlier same-stage same-role call had finished before.
- **Gate/critic return:** a resume whose reason is not "person answered".
- **After a person answered:** a resume whose reason is "the person answered…" or "paid round on the person's answer".
- **Later dispatch:** the first call of any further dispatch id of that stage and role.

| Stage | First pass | Gate/critic return resumes | After a person answered | Later dispatches |
|---|---|---|---|---|
| S1 | 104 / 1 | 0 | 19 / 1 | 0 |
| S2 | 255 / 2 | 74 / 2 | 19 / 1 | 995 / 5 |
| S3 | 346 / 2 | 146 / 3 | 18 / 1 | 147 / 3 |
| S4 | 280 / 2 | 77 / 2 | 99 / 1 | 285 / 3 |
| S5 | 712 / 3 | 1076 / 23 | 272 / 6 | 3017 / 14 |
| S6 | 355 / 1 | 0 | 0 | 384 / 1 |
| S7 | 970 / 1 | 0 | 0 | 1416 / 3 |
| Total | 3022 / 12 | 1373 / 30 | 426 / 10 | 6244 / 29 |

- **Total role time is 11,064 s** (the per-session sum). First pass is 3,022 s (27%) and everything later is 8,043 s (73%).
- **By `duration_ms`:** first pass 2,943 of 9,821 s (30%), returns 1,232, after a person 375, later dispatches 5,271.
- **Variant if windows and tasks are counted separately:**
  - In S5, `S5-qa-code-critic-2` was the first review of window 1; the notebook says so. Adding it brings S5 first pass to 787 s.
  - In S6, `S6-qa-runner-2` is a different task (manual TC-009), not a repeat. Adding it brings S6 first pass to 738 s.
  - Variant first pass is about 3,480 s (31%), rework about 7,584 s. I took the window and task mapping from the notebook, not from the jsonl.
- **S2 `qa-requirements-tester-3`:** its 781 s call has a `duration_ms` of 12 s and is counted as "later dispatch". 768 s of that S2 figure is overhead, not work.

## Table 4. Refusal and return reasons
**(a) Resumes after a gate or critic return.** Key is the gate file plus check kind from `resume_reason`; time is the wall of those resumed calls.

| # | Reason | Count | Wall (s) |
|---|---|---|---|
| 1 | `s5_precheck.py` manifest row-fields-missing | 16 | 575 |
| 2 | `s5_precheck.py` run_mapping unmatched ids | 4 | 449 |
| 3 | `s5_precheck.py` manifest red-own-behind (Then bound `covered`) | 4 | 206 |
| 4 | "the handover form is not complete" (no gate id) | 2 | 98 |
| 5 | `requirements-register.md` R-8 (implementation-only / no before-now) | 2 | 74 |
| 6 | `planning_contract.py` (P-3 rationale; P-1 `if_answered`) | 2 | 74 |
| 7 | `branch_accounting.py` BN-2 | 1 | 42 |
| 8 | `critic_rollcall.py` merge candidates | 1 | 35 |

Only 8 distinct reasons exist in the records. The wrapper phrases on these calls are: "still not repaired after one resume" 6, "handover form not complete" 4, "the factory refused to close the dispatch" 4, "a required output of the role is missing" 2, "paid round 1 on the person's answer" 2, "final message is not the handoff form" 1.

**(b) Driver question kinds.** "Next run" is the model time in the driver run started by the answer. Role time can exceed the run's wall because roles overlap.

| Kind | Count | Gap before the answer (s) | Next-run role s | Next-run conductor s |
|---|---|---|---|---|
| conductor | 12 | 3120 | 2512 | 697 |
| repair_limit | 7 | 395 | 789 | 377 |
| exit_limit | 6 | 1913 | 1587 | 80 |
| refusal | 5 | 309 | 3616 | 1154 |
| halt | 2 | 207 | 104 | 0 |
| questions | 2 | 175 | 353 | 84 |
| gate_A | 2 | 331 | 80 | 178 |
| environment | 2 | 1901 | 0 | 0 |
| s1_review | 1 | 42 | 1296 | 74 |
| stand_identity | 1 | 106 | 727 | 97 |

The 40th question has no next run. The 3 `gate_repair` records are all gate A. Round 1 repaired 27 keys with `critic_rollcall --apply-fixes` and `pin_cases`. Round 2 had 26 keys and no move, so it went to the conductor.

## Table 5. Sessions, briefs and startup
- **Sessions:** 80 distinct `session_id` values (41 role, 39 conductor) across 120 recorded CLI calls; the 40 resumes reuse a role session. I did not reproduce your "71 sessions".
- **Briefs (41 notes, one per new role session):** mean 14,300 B, max 23,455 B (`S5-qa-code-critic-8`). All 41 are above the 6,144 B ceiling the notes name.

| Role | Briefs | Mean (B) | Max (B) |
|---|---|---|---|
| code-critic | 8 | 21,134 | 23,455 |
| failure-analyst | 4 | 18,436 | 18,682 |
| runner | 2 | 17,544 | 17,839 |
| automator | 9 | 15,948 | 20,509 |
| test-strategist | 3 | 11,289 | 11,452 |
| case-critic | 9 | 9,038 | 10,284 |
| requirements-tester | 3 | 8,958 | 9,688 |
| case-designer | 2 | 7,652 | 7,984 |
| scout | 1 | 7,451 | 7,451 |

- **Per-call startup overhead** is `wall_ms − duration_ms`. The `duration_ms` field is not provider API time. Medians: new role call 4.1 s, resumed role call 4.6 s, conductor call 4.2 s. Means: new role call 25.7 s, resumed 4.8 s, conductor 21.0 s. Total across all calls: 2,063 s. Two calls account for 1,366 s of that: `S2-qa-requirements-tester-3` (781 s wall, 12 s `duration_ms`) and the S7 conductor call at 00:35 local (635 s wall, 37 s `duration_ms`).
- **Mean turns:** 21.7 per new role call, 4.4 per resume, 4.5 per conductor call.
- **Handoff notes:** 15 `note: handoff took N s` lines, total 1,241 s, max 223 s. I don't know what the driver is timing there.
- **Cost, summed from `total_cost_usd`:** roles $62.59, conductor $6.04.

## Table 6. Free arm
- **`free-1.log` and `free-2.log`** contain only the final result JSON, with no tool trace.
- **From the result JSON:** `num_turns` 47 and 11, `duration_ms` 526 s and 140 s, `duration_api_ms` 340 s and 426 s (the second looks cumulative; not verified), `total_cost_usd` $1.37 and $1.69 (the second looks cumulative), same session `af326bb4…`.
- **A tool-call trace exists outside the repo:** `C:\Users\i_mas\.claude\projects\C--QAFactory-mybooks-stand-arm-free-test-automation-framework\af326bb4-592c-48ea-af8a-891b313ab9a4.jsonl`. It has 56 tool calls over 16:39:14 to 16:51:31 UTC (12:17): Bash 31, Playwright `run_code_unsafe` 17, Write 6, Edit 1, ToolSearch 1.
- **Phase split:** I classified calls by command or path with regexes, so the split is approximate. Seconds are the time to the next call, so they include the model's thinking.

| Phase | Calls | Seconds |
|---|---|---|
| Stand exploration (browser, curl, api) | 25 | 345 |
| Running tests (`npx playwright test` / `tsc`) | 5 | 122 |
| Reading sources and ticket | 13 | 82 |
| Report, bugs, questions, commit | 7 | 48 |
| Writing tests | 5 | 30 |
| Reading the framework | 1 | 6 |
| Gap from commit to next call (includes the owner's answer) | 0 | 103 |

## Surprising things in the data
- **Roles ran only 40.8% of the wall.** Operator-labelled gaps were 22.8%, code-only driver time 16.5%, conductor 10.5%, human gaps 9.4%.
- **Rework is 73% of role time.** S5 automator had 9 dispatches and 35 calls. The single gate `s5_precheck row-fields-missing` caused 16 resumed calls.
- **All 41 briefs exceed the 6,144 B ceiling,** mean 14.3 KB and max 23.5 KB. The driver log for the larger briefs says "over the ceiling after every cut".
- **Two calls hung** (781 s wall with 12 s `duration_ms`, and 635 s wall with 37 s `duration_ms`). The first is inside S2.
- **S2's first pass took 255 s of role time,** but S2's wall was 1,736 s. 995 s of its role time is later dispatches, and 768 s of that is the stalled call.
- **The S7 conductor shows 998 s wall but 346 s `duration_ms`.** S7 took 83 min, 2,387 s of role time, 1,591 s of code time and 999 s of conductor time.
- **The last jsonl record is 00:51:14 but the final question was shown at 00:57:20.** That leaves 6 min of driver time with no recorded call.
- **S6 has 859 s of code time** between runner-1's end and runner-2's start.
- **30 of 40 questions fall in S5** and 15 of the 25 repeat dispatches. The two `environment` questions cost 1,901 s of gap and the next run held no model calls.
- **The notebook's S5 time is UTC.** S5 ran 17:57 to 22:05 UTC, which is 18:57 to 23:05 local.

## Scripts I ran
All are in `C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\0f83fb9a-27d2-4bb9-8f6e-7f95cf581138\scratchpad\`. The full source is in those files; I did not paste it here for length. I ran them as `python -B <absolute path>` with `PYTHONIOENCODING=utf8`.
- `main.py`: tables 1, 2, 3, 4a and 5, which are the full partition, first-pass classification and reason aggregation.
- `qkind.py`: the hash comparison, table 4b and the overlap seconds.
- `logs.py` and `pref.py`: the log line survey and question parsing.
- `dump.py`: the per-call listing.
- `explore.py`: the jsonl schema.
- `freephase.py`: the free-arm phase split from the transcript.
- `free.py` and `freetr.py`: the free-arm result fields and tool-call counts.

I also ran PowerShell file listings and the log create and last-write time listing. Nothing in the repo was changed, and I did not move the shell's working directory.
