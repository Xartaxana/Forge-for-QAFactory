# t-1553 -- FV3-35 part C, diagnosis step 1: why re-entry after `refusal_resume` takes `_liveness_refusal`

Verdict line: NEEDS WORK (diagnosis; no diff under review). The cause is the dry STUB. On a resume it answers success with
an EMPTY result. A live `claude --resume` would answer with the role's words.

The t-1542 premise does not reproduce. Its Family C, last bullet, says: "the stub is not the fault ... each answers the same
text". That premise was a reading of `dry_stub.py:1085-1088`, not a run (rule 13).

A latent product sibling sits on the same surface: `resume_with` writes an empty success over the saved result.

Blocking findings: 0 (there is nothing to merge). Fix directions: 2 (F1 stub, F2 product). Forks: 3.

## (a) Per-turn trace

**How the trace was taken.** It is one run, from a subshell.

- `probe.py` points `dry_world.DRIVER_PATH` at `trace_driver.py`.
- `trace_driver.py` is `dry_driver.main` plus wrappers on these methods:
  - `DriverMachine`: `where`, `_act_wait_existing_job`, `_finish_saved_result`, `_liveness_refusal`, `handle_refusal`,
    `resume_on_refusal`, `_act_resolve_return`, `_act_relaunch`.
  - `DriverDispatch`: `resume_with`, `exit_limit`, `handoff`, `finish`.
- Each wrapper appends one line with three fields:
  - `saved_json`: `state/driver-runs/S5-qa-automator-1.json` exists;
  - `ctl_status`: `controller_state().dispatches[S5-qa-automator-1].status`;
  - the `where` action.

    ( cd C:/QAFactory/forge-repo/ai-packages/qa-factory && python -B C:/Users/i_mas/AppData/Local/Temp/t1553/probe.py --part exits:s5 --exits-root C:/Users/i_mas/AppData/Local/Temp/t1553/root --ledger C:/Users/i_mas/AppData/Local/Temp/t1553/none.json )

The exits-root holds the real `seeds/s5.json` and `exits/s5.json` filtered to the one row `exit.resume_limit/stop`.

**What the run printed.**
- `reached S4 in 165.5 s`.
- `FAIL dry-1/exits:s5/exit.resume_limit/stop -- seed did not reach exit.resume_limit: met the conductor at S5`.
- `1/3 ok`, exit 1.

This is the same FAIL text as t-1542 run1 and CI.

Trace tail: `C:/Users/i_mas/AppData/Local/Temp/t1553/trace.log`, the last 30 lines, each cut at 260 characters.

```
pid=44896 WHERE | saved_json=False | ctl_status=None | {"action": "prepare_stage", "stage": "S5", "revision": 33}
pid=44896 ENTER handoff | saved_json=True | ctl_status=running |
pid=44896 RAISE handoff | saved_json=True | ctl_status=running | Refusal: exit gate for S5-qa-automator-1 (qa-automator, S5): 1 finding(s):
- digest: your final message is not the handoff form. The orchestrator reads it whole on every later turn, so it is exactly: `<role> <stage> <window> · ok|concerns|halt|impossible / <i
pid=44896 ENTER handle_refusal | saved_json=True | ctl_status=running | exit gate for S5-qa-automator-1 (qa-automator, S5): 1 finding(s):
- digest: your final message is not the handoff form. The orchestrator reads it whole on every later turn, so it is exactly: `<role> <
pid=44896 ENTER resume_on_refusal | saved_json=True | ctl_status=running |
pid=44896 ENTER resume_with | saved_json=True | ctl_status=running | kind=refusal_resume
pid=44896 EXIT resume_with | saved_json=True | ctl_status=running |
pid=44896 EXIT resume_on_refusal | saved_json=True | ctl_status=running |
pid=44896 EXIT handle_refusal | saved_json=True | ctl_status=running |
pid=44896 WHERE | saved_json=True | ctl_status=running | {"action": "wait_existing_job", "dispatch_id": "S5-qa-automator-1", "cancel_allowed": false, "reason": "Polling timeout, missing digest and 30+ minute discovery do not authorize cancellation"}
pid=44896 ENTER _act_wait_existing_job | saved_json=True | ctl_status=running |
pid=44896 ENTER _liveness_refusal | saved_json=True | ctl_status=running |
pid=44896 RAISE _liveness_refusal | saved_json=True | ctl_status=running | Refusal: wait_existing_job S5-qa-automator-1: its agent returned — the driver recorded this dispatch's session as ended (exit 0) in state/driver-runs.jsonl. The driver holds no result
pid=44896 RAISE _act_wait_existing_job | saved_json=True | ctl_status=running | Refusal: wait_existing_job S5-qa-automator-1: its agent returned — the driver recorded this dispatch's session as ended (exit 0) in state/driver-runs.jsonl. The driver holds no r
pid=44896 ENTER handle_refusal | saved_json=True | ctl_status=running | wait_existing_job S5-qa-automator-1: its agent returned — the driver recorded this dispatch's session as ended (exit 0) in state/driver-runs.jsonl. The driver holds no result and no ques
pid=44896 EXIT handle_refusal | saved_json=True | ctl_status=returned_unaccepted |
pid=44896 WHERE | saved_json=True | ctl_status=returned_unaccepted | {"action": "resolve_return", "dispatch_id": "S5-qa-automator-1", "stage": "S5", "role": "qa-automator", "dispatch_status": "returned_unaccepted", "digest": "", "options": ["accept", "checkpoi
pid=44896 ENTER _act_resolve_return | saved_json=True | ctl_status=returned_unaccepted |
pid=44896 RAISE _act_resolve_return | saved_json=True | ctl_status=returned_unaccepted | Refusal: resolve_return: {"action": "resolve_return", "dispatch_id": "S5-qa-automator-1", "stage": "S5", "role": "qa-automator", "dispatch_status": "returned_unaccepted",
pid=44896 ENTER handle_refusal | saved_json=True | ctl_status=returned_unaccepted | resolve_return: {"action": "resolve_return", "dispatch_id": "S5-qa-automator-1", "stage": "S5", "role": "qa-automator", "dispatch_status": "returned_unaccepted", "digest": "",
pid=44896 RAISE handle_refusal | saved_json=True | ctl_status=returned_unaccepted | Person: Which of these should happen?

## What each answer costs and does

(a) `restart` — free a dispatch nobody is doing so the driver starts it again; the new session gets the person's words
the factory: one more working session of the role, and its revie
=== SEED [{'drive_until': {'stage': 'S5', 'question': 'exit.resume_limit'}}] -> (False, 'met the conductor at S5: a state the driver has no move for')
=== WORLD C:\Users\i_mas\AppData\Local\Temp\qa-dry-row-tr9pjw2p\project
```

**Where the road leaves the path.** At the first re-entry after `resume_with(kind=refusal_resume)`:
- `where` returns `wait_existing_job`;
- `saved_json=True`, `ctl_status=running`;
- the next call is `_liveness_refusal`, not `_finish_saved_result`.

**What this rules out.** The saved file EXISTS, so it was neither absent nor moved:
- `retire_infra_result` would have renamed it to `.infra.json`;
- the `interrupted` branch would then have run the role again.

`where` also did not choose another branch first. The one remaining reason in `_act_wait_existing_job`
(`driver_machine.py:1478-1484`) is that `saved.get("result")` is falsy, which means an empty `result`.

## (b) Cause, file:line

1. On a resume the driver passes no `--agent`. `driver_runner.py:604`: `if agent and not resume: cmd += ["--agent", ...]`.
   This is correct for the live host: a resumed session keeps its agent.
2. The stub takes the role from `--agent` alone. `dry_stub.py:1078`: `role = agent.split(":")[-1]`. On a resume
   `role == ""`.
3. The resume branch reads the row's text by that empty role. `dry_stub.py:1087`:
   `(control.get("stub") or {}).get(role, {}).get("result_text") or ""` gives `""`. The stub then prints
   `is_error: false, result: ""` (`dry_stub.py:1119-1120`).
4. `resume_with` treats the session as spent only on `is_error and not result` (`driver_dispatch.py:2327-2330`).
   - An empty SUCCESS passes that check.
   - `_write_json(... driver-runs/<dispatch>.json, result)` (`driver_dispatch.py:2331`) then OVERWRITES the role's earlier
     saved result with `result: ""`.
5. Re-entry follows from that empty result:
   - `_act_wait_existing_job` reads `result: ""`, so `_finish_saved_result` is skipped (`driver_machine.py:1484`).
   - There are no words, no `interrupted` entry, and the dispatch is in `sessions`, so `_liveness_refusal` runs
     (`driver_machine.py:1557-1579`).
   - Then: `dead_dispatch`, recover (`ctl_status` goes from running to returned_unaccepted), `_act_resolve_return` (`:1666`),
     and the conductor.

**Direct measurement of the stub.** The call used the argv shape the driver sends on a resume. The control file held the row's
own `stub`.

```
--- resume, no --agent (the driver's shape, driver_runner.py:600-605):
{"type": "result", "subtype": "success", "is_error": false, "session_id": "stub-S5-qa-automator-1-1", ..., "result": ""}
--- positive control: resume WITH --agent qa-factory:qa-automator:
{"type": "result", "subtype": "success", "is_error": false, ..., "result": "qa-automator S5 window \u00b7 ok\nthe window is done"}
--- stub journal: {"role": "", "resume": true, ...} / {"role": "qa-automator", "resume": true, ...}
```

**The two resumes inside `handoff`.** The same empty answer explains them:
- `keep_resumed_result` skips an empty result (`driver_dispatch.py:2456-2457`);
- so the handoff ladder judged the first text three times ("still not repaired");
- only `resume_with` writes the empty answer.

**Stub or product: the STUB is the trigger.**
- The dry world fakes "a resumed role answers nothing, successfully".
- The row's `result_text` is never served on any resume.
- The same `role == ""` also makes `repair_on_round` (`dry_stub.py:1084`) unreadable on every resume. That costs nothing
  today, but it is the same defect:
  - grep `repair_on_round` over `ai-packages/qa-factory/**/*.json`: 0 files;
  - positive control, grep `result_text` with the same shape: 4 files.

**The product has a latent sibling on the same surface, the writers of the saved result.**
- `resume_with` writes an empty success over a non-empty saved result.
- Its twin `keep_resumed_result` refuses to.
- A live resume whose last turn is only a tool call would end with no text. It would then take this same `dead_dispatch` road
  instead of the `exit_limit` seam.
- That a live resume can reach this road is an estimate, not verified.

## (c) Fix direction

### F1, stub

F1 unblocks the 6 rows on the road the rows mean.

owns: `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/dry_stub.py` (`claude_main`, and one selftest row).

**The change.**
- On `--resume` with no `--agent`, take the role from the dispatch id inside the session key: `derived.group(1)` matching
  `S\d+-(qa-[a-z-]+)-\d+`.
- This is the shape of the fallback in `DriverDispatch.dispatch_role` (`driver_dispatch.py:2303`).
- The `result_text` and `repair_on_round` reads then see the row. The journal row's `role` names it.

**Edges.**
- A session key that matches no shape (a conductor session, a hand-made id) keeps today's answer: `""` and `role: ""`.
  Nothing is guessed. The builder states that such a row stays as it is.
- A row with no `result_text` for the role keeps today's `""`; no default text is invented. The selftest row names this case.
- POSITION: the derivation goes BEFORE the `repair` read (`:1084`). INVARIANT: a resume before `repair_on_round` still writes
  nothing (`wrote: []`). Only the TEXT changes.

**Expected road after F1 (estimate, not measured).**
1. `resume_with` writes the same text.
2. `_finish_saved_result` runs, and `handoff` refuses on the same findings.
3. `resume_on_refusal` finds the key in the record.
4. `exit_limit(why=refusal)` runs (`driver_machine.py:325-332`, t-764 E8).
5. The question is `exit.resume_limit` / `_halted` (`driver_dispatch.py:4034-4035`).

**Class edge.** F1 changes EVERY dry resume, in every group and in the main pass, not only these rows. A row that is green
today because a resume answered `""` can turn red.

**DoD.**
- The 6 rows PASS in a scratch exits-root run.
- The groups whose roads resume (s5, s1-s4, s0, gates, main) are judged by the batch canon.
- `dry_exits.py --check`: 0 discrepancies.
- known_red s5: each removal is named.

**red-before.** `exit.resume_limit/stop` FAILs today with "met the conductor at S5" (measured above).

### F2, product sibling

F2 is a separate node; opening it is the Lead's call.

owns: `scripts/driver_dispatch.py::resume_with`, and a row in an existing driver test.

**The change.**
- After a caller's resume, an empty `result` (stripped) counts as a spent session, whatever `is_error` says.
- It is not written over the saved result, as `keep_resumed_result` already does.
- The road goes to `exit_limit` with the session's words absent.

**Edges.**
- POSITION: after `run_claude` and BEFORE `_write_json` (`:2331`). INVARIANT: an empty result never replaces a saved one, and
  a non-empty result (error or not) is written as today.
- The `why` token: today `session_gone` means "error and no words". This is fork q2.

## (d) Forks (questions to the Lead)

- **q1.** t-1542 (b) C step 2 says "the stub and the seeds stay as they are". This trace overturns its premise. Is F1 (the
  stub) the fix for the 6 rows, with F2 as its own node? F2 alone would also reach `exit.resume_limit`, but through
  `session_gone`. That would hide the stub defect and walk a road the rows do not mean.
- **q2.** For F2: is an empty successful resume `why=session_gone`, or does it need a new token? The `exit_limit` vocabulary
  today is handoff | refusal | structured | session_gone.
- **q3.** F2's live reachability is an estimate. Does the Lead want one measurement first? It would be a real
  `claude -p --resume` whose last turn is a tool call, before the node opens.

## Seam and class notes

**Surface: the stub's resume branch.** Neighbouring classes walked:
- `result_text`: broken;
- `repair_on_round`: broken, no user;
- the `n` / key derivation: correct, it reads the session id;
- the conductor branch: not affected, since a conductor call sends no `--resume` role.

**Product surface: the writers of `driver-runs/<dispatch>.json`.**
- `keep_resumed_result`: skips an empty result (correct).
- `keep_assembled_result`: writes a code digest, which is non-empty by construction.
- `resume_with`: writes an empty result (the sibling, F2).
- `question_rework`: moves the file aside; it does not write.

**Q12, one road:** none found. The stub defect applies to every role and every group alike.

## Trail

**Read:**
- the t-1542 diagnosis (Family C, (b) C);
- `dry_world.py:385-415, 1212-1266`;
- `dry_driver.py` (whole);
- `dry_stub.py:1070-1121`;
- `driver_machine.py:140-345, 1457-1580, 1950-1970`;
- `driver_dispatch.py:2300-2335, 2440-2460, 3851-3870, 4030-4035`;
- `driver_runner.py:593-612, 840-1000 (grep), 1090-1108`;
- `test_scenario_dry_1.py:80-138`;
- `exits/s5.json` (the 6 rows) and `seeds/s5.json`.

**Runs:** the probe run above and the direct stub probe.

All scratch is under `C:/Users/i_mas/AppData/Local/Temp/t1553/`. No repo file was edited except this report.

```json
{"verdict": "fit_with_fixes",
 "blockers": [],
 "fixes": ["F1: dry_stub.py claude_main: on --resume with no --agent take the role from the session key's dispatch id before the repair_on_round read (dry_stub.py:1078,1084,1087), so a resume serves the row's result_text; the 6 resume_limit rows then reach exit_limit(why=refusal) - not measured", "F2: driver_dispatch.py resume_with:2327-2331 writes an empty successful result over the saved result (its twin keep_resumed_result:2456 skips it); a separate product node, Lead's call (q1-q3)"],
 "class_completeness": "Stub surface: result_text and repair_on_round both read the empty role on every resume (repair_on_round has 0 users in the fixtures, result_text has 4 files). Product surface: of the driver-runs/<dispatch>.json writers, only resume_with writes an empty result. F1 changes every dry resume in every group, so the batch canon judges the other groups.",
 "trail": {"read": ["docs/tasks/specs/reviews/t-1542-fv3-35-diagnosis.md", "ai-packages/qa-factory/scripts/tests/dry_world.py", "ai-packages/qa-factory/scripts/tests/dry_driver.py", "ai-packages/qa-factory/scripts/tests/dry_stub.py", "ai-packages/qa-factory/scripts/driver_machine.py", "ai-packages/qa-factory/scripts/driver_dispatch.py", "ai-packages/qa-factory/scripts/driver_runner.py", "ai-packages/qa-factory/scripts/tests/test_scenario_dry_1.py", "ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/exits/s5.json", "ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/seeds/s5.json"],
  "reruns": [{"command": "( cd ai-packages/qa-factory && python -B Temp/t1553/probe.py --part exits:s5 --exits-root Temp/t1553/root --ledger Temp/t1553/none.json )", "result": "reached S4 in 165.5 s; FAIL exit.resume_limit/stop met the conductor at S5; trace: resume_with(refusal_resume) -> WHERE wait_existing_job saved_json=True ctl_status=running -> _liveness_refusal -> resolve_return -> Person; exit 1"},
             {"command": "DRY_STUB_CONTROL=control.json python -B dry_stub.py -p --resume stub-S5-qa-automator-1-1 (and again with --agent qa-factory:qa-automator)", "result": "no --agent: is_error false, result empty, journal role empty; with --agent: result is the row's result_text"}]},
 "mutants": [],
 "mutants_none": "diagnosis dispatch with no diff and no new behaviour; no probe applies"}
```
