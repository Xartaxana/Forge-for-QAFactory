# t-368 -- diagnosis: canon 43402053458 (conv/wave-11, bd44340), shard 1, test_controller_rework_repair_binding 234/235

Critic (opus), diagnosis only; no tree changed (the worktree `C:\QAFactory\forge-repo\.claude\worktrees\conv-wave11`
was only read and run; every probe ran on a byte copy under the session scratchpad).

## Outcome (DoD form)

**(a) A flake that does not depend on wave 11.** The case depends on wall-clock time. The test case
`a recorded id under a fresh key is refused` expects that, by the time of its own `apply`, the relaunched dispatch has
been `running` for longer than `never_started_after_s` = **0.01 s** (10 ms). Only then does the liveness repair close
that dispatch as `never_started` before `validate` runs. Locally the gap is about 40-55 ms, so the case passes. On a
fast CI runner it can drop under 10 ms. The relaunched dispatch then stays `running`, and `validate` refuses with the
FIRST check of the dispatch branch, `sequential task already has an active dispatch: ...`, rather than
`resume existing dispatch ...`. Forcing that condition on a copy reproduces the CI signature byte for byte: the same
FAIL line, 234/235, and the following check `and no dispatch event was committed for it` still passes. Commit 0603e40
cannot reach this path: `native_context` is never imported in this test's process.

## Q1 -- what the failing case printed

The text after `not found in:` is **not in any CI carrier**. The harness prints the haystack on the NEXT line.
selftest keeps only the lines that start with `FAIL`, so the haystack is dropped:

- `scripts/tests/harness.py:153`: `return check(name, needle in text, f"{needle!r} not found in:\n{text[:600]}")`
- `scripts/selftest.py:493`: `failed = [line for line in lines if line.startswith("FAIL")]`

Artifact (downloaded with `gh run download 43402053458 -n package-full-shard-1`), `selftest-shard-1-of-2.txt` lines 70-72:
```
FAIL tests: scripts/tests/test_controller_rework_repair_binding.py  10.3s — exit 1 | === test_controller_rework_repair_binding: 234/235 ok ===
      FAIL a recorded id under a fresh key is refused: resume, do not replace — 'resume existing dispatch' not found in:
PASS tests: scripts/tests/test_infra_failure_conductor_tracker.py  11.2s
```
The job log has no copy either. `gh run view 43402053458 --log-failed | grep -n "resume existing\|rework_repair\|not found in"`
returned nothing, out of 400 log lines. The control: `ci_read.py log 131807165243 --grep FAIL` also matched 0 of 400,
so the test output is not in the log at all, only in the artifact. **Q1 cannot be answered from the run.** Q2 and the
forced run in Q5 settle what the text was.

Side finding (not blocking): selftest drops the detail lines of a multi-line FAIL, and that is what cost this question.
A fix would keep the indented lines that follow a FAIL line, under the same 300-character cap. This is a proposal for
the coordinator; whether to open it as a node is not my decision.

## Q2 -- is the case time- or order-dependent? Yes: wall-clock, 10 ms threshold

Trace, at bd44340:

1. `tests/test_controller_rework_repair_binding.py:29-38` `never_started_action` writes
   `{"dispatch": {"never_started_after_s": 0.01}}`, installs the fake hooklib (a transcript of `qa-case-critic`, age 30 s)
   and does `time.sleep(0.05)` before `next_action()`. So the author guarded the FIRST liveness closure with a sleep.
2. `:233-236` dispatches the relaunch packet (`apply("dispatch", ...)`). The relaunch `S4-qa-case-designer-3` is now
   `running`, with `created_at = time.time()` (`event_store.py:712`).
3. `:244-249` sends the same id under a fresh idempotency key **with no sleep**. `without_hooklib()` runs only in the
   `finally`, so the fake transcript is still installed.
4. `controller.py:5013-5022` `apply`: `_holder_would_refuse` returns True (`controller.py:4979-4987`: a fresh key is no
   replay), so `close_settled` -> `liveness_fixes` (`controller.py:7845+`) asks `dispatch_liveness._state`.
5. `dispatch_liveness.py:1129-1137`: the fake transcript's role is `qa-case-critic`, not this dispatch's
   `qa-case-designer`, so `best` is None and `found` is non-empty. Then:
   ```
   age = None if began is None else now - began
   if age is not None and age > limits["never_started_after_s"]:
       return {"state": NEVER_STARTED, ...}
   return {"state": UNKNOWN, ... "too soon to tell"}
   ```
   `began` is the dispatch event's `created_at` (`controller.py:7684-7693`), and `now` is `time.time()` (`dispatch_liveness.py:986`).
6. If age > 10 ms: NEVER_STARTED, so the row is closed, and `validate` (`controller.py:5448`, nothing is running) reaches
   `controller.py:5473` `"resume existing dispatch; do not replace its checkpoint"`. The test passes.
   If age <= 10 ms: UNKNOWN, so nothing is closed, and `controller.py:5448-5462` raises
   `sequential task already has an active dispatch: S4-qa-case-designer-3. ...`. The `check_in` fails, nothing is
   committed, and the next `check_eq` passes. **That is exactly the CI picture: 234/235.**

Other dependencies I checked and ruled out:
- **pid / liveness probe:** `dispatch_liveness.state` reads a pid only through the driver-state `in_flight` entry. The
  test writes none.
- **Platform branch:** the same liveness reader closed the FIRST dispatch on CI. The step at :195-197
  `nothing proves an agent started, so next closes it and relaunches` passed there, because only one check failed.
- **Set or listing order:** the fake hooklib returns one fixed path list.
- **Cross-file state:** selftest runs each file as its own subprocess, and `temp_project` makes a unique root.

## Q3 -- has it failed on CI before? No, across the 20 canon runs before this one; the failing run was the fastest

Command: for each canon run in `gh run list --workflow canon --limit 25`, download `package-full-shard-{1,2}`, then run
`grep -h test_controller_rework_repair_binding selftest-shard-*.txt`. The result is condensed from the raw output, which
has one line per run of the form `<run> shard1: PASS tests: scripts/tests/test_controller_rework_repair_binding.py  <s>s`.
Shard 2 never holds the file.
```
43401964375 PASS 18.1s   43400805735 PASS 14.6s   43399525276 PASS 14.5s   43397601655 PASS 10.9s
43388841978 PASS 15.9s   43385256999 PASS 19.6s   43381778309 PASS 13.9s   43380859395 PASS 11.5s
43377812212 PASS 19.8s   43376354254 PASS 19.8s   43369798796 PASS 19.8s   43365498706 PASS 13.9s
43365393016 PASS 19.8s   43362506723 PASS 13.5s   43360752450 PASS 14.0s   43360634340 PASS 13.8s
43356216379 PASS 17.8s   43353326398 PASS 19.4s   43353254105 PASS 20.4s   43350037856 PASS 19.1s
```
The PASS lines are the positive control: the same grep finds the file in every artifact. The case has been in this file
since a8a9fb4 (2026-11-12), which is earlier than all these runs.

There is no earlier failure, so Q3 alone does not prove a flake. But the failing run took **10.3 s**, faster than any
of the 20 passing runs (10.9-20.4 s). That fits the mechanism: the case fails when the runner is FAST, not when it is
loaded.

## Q4 -- can 0603e40 change this path? No

- 0603e40 touches only `native_context.py` and `tests/test_codex_host.py` (`git show --stat 0603e40`: 2 files, 5+/5-).
- `grep -niE "native_context|person_signal"` over `controller.py`, `dispatch_liveness.py`, `event_store.py`, the test
  file, `controller_rework_common.py`, `test_dispatch_liveness.py` and `harness.py` found no hit except
  `host_dispatch.py:243-251`. That is a direct `hooklib.person_signal` call, not native_context. The control: the same
  grep finds `native_context.py:170` `hooklib.person_signal(event, 'inject', ...)`.
- Empirically, the test was run under an atexit hook that printed `sys.modules` membership:
  `MODS native_context=False host_adapter=True inject_context=True stage_guard=True host_dispatch=True dispatch_liveness=True hooklib=True`
  next to `=== test_controller_rework_repair_binding: 235/235 ok ===`. The True entries are the positive control:
  the check sees the modules that are loaded. `native_context` is never imported in this process.

## Q5 -- reproduction

- 20 runs of the unmodified file at bd44340, here:
  `for i in $(seq 1 20); do python -B <tree>/scripts/tests/test_controller_rework_repair_binding.py | tail -1; done | sort | uniq -c`
  -> `     20 === test_controller_rework_repair_binding: 235/235 ok ===`, so **20/20 pass**. That is expected on this
  machine, because the local gap is about 40 ms, above the 10 ms threshold (see the next item).
- Gap measurement on a copy. One print was inserted just before the fresh-key call:
  `time.time() - created_at` of the relaunch event. Five runs gave
  `GAP_MS 47.63`, `39.38`, `40.14`, `45.75`, `54.45`, each `235/235 ok`. On this machine the margin over the 10 ms
  threshold is only about 4x. The age seen inside `apply` is slightly larger, because `apply` reads `state()` first.
- Forced run on a copy (`test_probe_force.py`). The only change: just before the fresh-key call, the config is
  rewritten to `never_started_after_s: 60`, which simulates "the gap is under the threshold". Verbatim:
  ```
  FAIL a recorded id under a fresh key is refused: resume, do not replace — 'resume existing dispatch' not found in:
  sequential task already has an active dispatch: S4-qa-case-designer-3. Finish it first (`story_step.py finish`)
  PASS and no dispatch event was committed for it
  PASS the round counts while it runs
  === test_controller_rework_repair_binding: 234/235 ok ===
  ```
  This is the CI signature: the same FAIL line, the same count, and the next check passes.

## Proposed fix (FR-31: a test that fails only on timing is a defect of the TEST)

In `tests/test_controller_rework_repair_binding.py:244-249`, make the precondition explicit instead of relying on
elapsed time. Before the fresh-key `apply`, add `time.sleep(0.05)`, the same guard `never_started_action` already
has at :37, then call `controller.close_settled()` and assert that the relaunch row is no longer `running`. After that
the case tests only the `resume existing dispatch` refusal. The controller itself is correct here: by FR-59/AR-28, a
running holder whose liveness is `unknown` must refuse with "sequential task". So no product-code change is proposed.

## Class sweep (same artifact, then the neighbours by grep of the same threshold)

The class: a test whose closure step relies on the wall-clock age of a dispatch passing `never_started_after_s` = 0.01
with no wait.
- `:194 never_started_action`: guarded by sleep 0.05 (:37). Not applicable.
- `:271`: after `never_started_action` (guarded). The relaunch is dispatched and only the ledger is read; no later
  closure is relied on. Not applicable.
- `:367`, `:424`: guarded. The relaunch packet is validated or applied with changed fields, and each refusal names
  the relaunch, not a holder. Not applicable.
- `:244-249` (the failing case): **unguarded, the one instance.**
- `test_story_run_loop.py:114-124`: guarded by `time.sleep(0.05)` (:123). Not applicable.
- `test_controller_rework_jobs_guard.py:43-45`: its receipt is described as ten minutes old (:33-34), not aged by a
  fresh `created_at`. I read it only partly (:25-50) and did not trace its age source: a residual, not verified.

## Duplication and consistency / code quality (rule 18)

This is a diagnosis, not a diff gate: no diff is under review. DUPLICATION AND CONSISTENCY: none found. I grepped the
users of `never_started_after_s": 0.01` (3 files, listed above). One place lacks the guard that its siblings carry,
and that is the finding itself. CODE QUALITY: the selftest detail drop (the Q1 side finding).

## One road (rule 19)

Not applicable: no exclusion of a language, project or case from a shared mechanism is involved.

## Verdict

`fit`: wave 11 is safe to merge after a green rerun of shard 1. The red does not come from 0603e40 or any other wave-11
change. Fixing the test, and optionally the selftest detail capture, are proposed nodes for the coordinator to open,
outside wave 11. This verdict is an input to acceptance; the decision to merge stays with the coordinator.

```json
{
  "verdict": "fit",
  "blockers": [],
  "class_completeness": "Same-file sweep: of the 5 places that rely on a never_started closure, 4 are guarded by the 0.05 s sleep in never_started_action; the fresh-key case at test_controller_rework_repair_binding.py:244-249 is the one unguarded instance. Neighbours sharing the 0.01 threshold: test_story_run_loop.py is guarded (sleep at :123); test_controller_rework_jobs_guard.py:43-45 is only partly read and its age source is not traced (a residual for the fix node). No SIBLING_MAP axis applies to a test-timing defect.",
  "fixes": [
    "Proposed node outside wave 11 (FR-31): in test_controller_rework_repair_binding.py, before the fresh-key apply (:244-249), sleep 0.05 as never_started_action does, call close_settled and assert the relaunch row is no longer running, so the case does not depend on more than 10 ms of wall-clock time passing",
    "Proposed node (optional): selftest.py:493 keeps only lines starting with FAIL, so the multi-line detail of check_in (harness.py:153) is lost from CI artifacts; keep the indented continuation lines under the same 300-character cap"
  ],
  "trail": {
    "read": [
      "ai-packages/qa-factory/scripts/tests/test_controller_rework_repair_binding.py:1-80,180-300,360-445 (bd44340)",
      "ai-packages/qa-factory/scripts/tests/controller_rework_common.py:106-111",
      "ai-packages/qa-factory/scripts/tests/harness.py:115-118,151-153",
      "ai-packages/qa-factory/scripts/tests/test_dispatch_liveness.py:37-76",
      "ai-packages/qa-factory/scripts/controller.py:4960-5075,5440-5490,7684-7693,7845-7929",
      "ai-packages/qa-factory/scripts/dispatch_liveness.py:107-112,140-175,930-1145",
      "ai-packages/qa-factory/scripts/selftest.py:485-500",
      "ai-packages/qa-factory/scripts/event_store.py:712",
      "ai-packages/qa-factory/scripts/tests/test_story_run_loop.py:100-127",
      "ai-packages/qa-factory/scripts/tests/test_controller_rework_jobs_guard.py:25-50",
      "artifact package-full-shard-1/selftest-shard-1-of-2.txt of run 43402053458 and of 20 earlier canon runs"
    ],
    "reruns": [
      {"command": "gh run view 43402053458 --log-failed | grep -n 'resume existing|rework_repair|not found in'", "result": "no match in 400 lines; the haystack exists in no CI carrier"},
      {"command": "grep test_controller_rework_repair_binding over shard artifacts of 20 earlier canon runs", "result": "20/20 PASS, 10.9-20.4 s; the failing run took 10.3 s"},
      {"command": "test file under an atexit sys.modules probe", "result": "235/235 ok; native_context=False, host_dispatch=True, dispatch_liveness=True"},
      {"command": "20 runs of the unmodified file at bd44340", "result": "20 x 235/235 ok (20/20 pass)"},
      {"command": "copy with a gap print, 5 runs", "result": "GAP_MS 47.63 39.38 40.14 45.75 54.45, each 235/235"},
      {"command": "copy with never_started_after_s rewritten to 60 before the fresh-key call", "result": "234/235; FAIL line identical to CI; haystack: sequential task already has an active dispatch: S4-qa-case-designer-3; next check PASS"}
    ]
  }
}
```
