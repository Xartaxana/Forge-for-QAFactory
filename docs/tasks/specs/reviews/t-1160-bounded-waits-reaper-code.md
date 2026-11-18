# t-1160 — code critic: bounded waits K-REAP / K-STALE / K-WIRE (branch bw-kwire, 7040d325..094fbf95 over 23c9fee3)

Spec: `docs/tasks/specs/20261117-bounded-waits-mechanism-spec-r2.md` §5, §7.2-§7.3, §10 (K-REAP, K-STALE, K-WIRE), Lead decisions.
Critic, one topic. The decision to accept belongs to the Lead.

**Verdict: NEEDS WORK** — 2 blocking findings (F1 blocks the placing commit, F5 blocks placement), 6 fixes before merge, the rest notes.
In the JSON block this is `blocker`, because rule 23 says any blocking finding makes it `blocker`.

## Findings

**F1 (BLOCKS the placing commit): the new hook-path modules and the kill-set data are outside the mechanism net.**
`tools/mechanism_gate.py` MECHANISM_PREFIXES lists `tools/worktree_sweep.py` ("run by .githooks/post-merge … self-activating")
and `tools/worktree-junk.json` ("DATA that decides what worktree_sweep.py deletes"). It has no entry for `tools/wait_reaper.py`,
`tools/session_proc.py` or `tools/wait-reaper.json`. Measured: the closure helper of
`test_mechanism_gate.py::test_transitive_import_closure_of_live_wiring_is_covered_by_mechanism_prefixes` was run on the
candidates. It gives `['session_context_next'] uncovered: ['compact_snapshot_next', 'session_context_next', 'session_proc', 'wait_reaper']`
and `['dod_gate_next'] uncovered: ['dod_gate_next', 'session_proc', 'wait_reaper']`; on the live `session_context` it gives `[]`.
After placement the `_next` names become live names, and `session_proc` and `wait_reaper` stay uncovered. The test goes red. Also,
an edit to `never_reap` or `limit_seconds` (which widens the kill set) would get past the axis-block gate. Fix (the Lead, in the
placing commit): add three rows beside the worktree_sweep pair. This is the sibling of the axis "a module a hook runs is in the net";
spec §11 has no `mechanism_gate.py` row.

**F5 (BLOCKS placement): after placement, tests and the liveness probe start REAL `--apply` reapers against the live session.**
(a) `hook_liveness_probe.py` case 18 runs live `tools/dod_gate.py` as a subprocess with `cwd=REPO` (`run_subprocess_case`, :474-478).
The stop passes, so `_launch_reaper` → `wait_reaper.launch("subagent-stop")` → `root=None` → `os.getcwd()` = the live repo. That
spawns `wait_reaper.py --apply` on the session that runs the probe. `test_hook_liveness_probe.py::test_live_run_of_all_cases_is_ok`
and the two `main` tests each do this. The probe's live-state fingerprint (`_LIVE_STATE_TARGETS` :208-217) does not cover
`.git/wait-reaper/`, so the probe stays green and nothing is visible. (b) `test_session_context.py::test_main_stdout_deadline_timeout_exits_immediately_via_subprocess`
(:632) runs live `session_context.py`. `main()` builds with `repo_root()` (:2676), so `waits_lines` launches a real reaper (trigger
`session-start`). The builder silenced exactly this in `test_dod_gate.py` (`_WRAP`) but not in its sibling file. Harm: run.log gets
lines with a false trigger, the previous run's `status.json` counts are overwritten (see F3), and the K-REAP norm "no real kill in
tests" is broken. Fix: `dod_gate_next._launch_reaper` passes the payload `cwd` (the gate already uses `cwd = payload.get("cwd")`, :783).
Case 18 then resolves its tmp repo and gets a one-line "not found", with no spawn. The Popen test uses the same `_WRAP` silencer.

**F2 (fix before merge): the hook path waits up to 120 s per git call; its twin waits 5 s.** `launch` builds `ws.Git(runner)` with
`gitcmd.DEFAULT_TIMEOUT = 120` (gitcmd.py:35). `waits_lines` then calls `repo_context(worktree_sweep.Git(), root)` a second time.
The named twin `worktrees_line` passes `timeout=5` ("at most 5 s per git call", :1921-1933). If git hangs, SessionStart blocks for
up to 240 s. If the harness kills the hook on its timeout (default 60 s — an estimate, not verified), the WHOLE context output is
lost: the hook's message changes, which is question (2). The same 120 s applies on SubagentStop. Fix: `launch(..., timeout=5)`, and
`waits_lines` does one walk and one `repo_context`.

**F3 (fix before merge): WAITS reads AFTER it launches, so a fresh run can erase the last result.** `waits_lines` calls `launch`
first, then reads `status.json`. The spawned reaper writes `state="running", stopped=0, failed=0…` right after its lock
(wait_reaper.py:424-426), and `waits_line` returns None for `running`. The reaper starts in about one python start plus one git call;
session_context reaches its read after one walk plus one git call. That is a real race. When the reaper wins, the previous run's
stop count is gone for good (the new run usually finds 0). Fix: read the line first, then launch. No row covers the order (the WAITS
tests mock launch and status separately).

**F4 (fix before merge; K4 observation (a) — a defect): failures on kids are invisible, and the counts mix units.** `_run_locked`
writes one line per tree with the ROOT's outcome (:482-485). `failed` sums the failures of every process, while `stopped` counts
roots. K4: "1 stopped, 1 failed" on ONE tree, and the failed pid and its winerror are nowhere. Spec §5.2 requires `failed: winerror
<n>` to be reported, and check 27(e) reads run.log. A likely cause (estimate, not verified): `TerminateProcess` on a process that is
already exiting fails with ERROR_ACCESS_DENIED (MSYS fork stubs and conhost end when the root dies). That is a false "failed" which
the WAITS line will show on every loop stop. Fix: put `fails=<name>/<pid>/<outcome>;…` on the line; map a terminate winerror 5
whose `GetExitCodeProcess` is not STILL_ACTIVE to `gone`; count trees and processes under honest names. Add one table row.

**F6 (fix before merge): an odd stamp reads as "another session's (...) -- not your state".** `_compact_block` sends `"unknown"`
to the foreign branch, and the row `odd_field_never_own` pins that text. The spec says only "never own". Calling the unknown foreign
states an unknown as a fact (FR-41), and it points the wrong way for restoring state: a Lead whose own stamp got mangled is told to
skip its own narrative. Fix: `"unknown"` goes to the "no session stamp … check it is yours" line. Note: the stamp door cannot repair
an odd header — it is "already stamped -- unchanged".

**F7 (fix before merge, low; Q6): the stamp value has two encoders.** `compact_snapshot_next.narrative_header_line` writes
`f"{pid}-{created:.3f}"`. `session_context_next._session_proc_id` writes `"%d-%.3f"` again. If either changes, "own" never matches.
That fails safe, but it breaks one-writer (AR-13/14). Fix: one function in compact_snapshot that both call.

**F8 (fix before merge, low; Q2): the post-merge one-liner prints a multi-line traceback on an import failure.** `python -B -c
"…import wait_reaper…"` has no try around it. The merge's exit is unchanged (`|| true`, and git ignores it), but the output is not
one line. Wrap it.

**F13 (fix before merge, low; Q7): `select` is 78 lines** (wait_reaper.py:219-296; split the candidate pass and the orphan pass).
SessionStart walks the session three times and calls `repo_context` twice (`launch`, `waits_lines`, `_session_proc_id`).

**F14 (Q5f): tests are over the product with no `tests-over:` line.** numstat: K-STALE product +79 / tests +95 −1; K-WIRE product
+60 −6, +20, +4 (+5 SKILL) / tests +137 −4, +70 −5. Neither ed466898 nor 094fbf95 carries `tests-over:`. K-REAP (product 847 /
tests 471) is within the budget. Fix: the reason line in the amended commit message, or trim.

**F15 (doc): SKILL step 5a says "a listed tree is stopped (`--apply`)".** A bare `--apply` stops every listed tree, which contradicts
"or named … with the reason it stays". Write `--apply --pid <root>`; the Lead used exactly that in K4.

Notes (spec level, for the Lead; not the builder's defects):
- **N1, the app's utility process can be taken for the session.** Measured: the app is `Claude.exe` (17100), the Toolhelp name
  compares equal case-insensitively, and the app's terminals (`powershell -NoExit` 8900, 10312) are children of `Claude.exe
  --type=utility` 11816. A person merging in such a terminal gets session = 11816. Nothing is stopped (its children are not wrapper
  roots), but they are logged as `unknown-root`: check 27(e) reads each as a "harness wrapper change", which is a false lead. The
  §5.0 claims "the app is never reached" and "never names a wrong process" are false in that setup. Proposed node: walk the image
  path (`QueryFullProcessImageNameW`, in-process) with a data row such as `claude-code`, or record a named residual.
- **N2, any child counts as an unknown root.** `unknown_root` counts every non-conhost child of the session (an MCP stdio server
  would make WAITS never silent). Today 26860 has only conhost and bash children (measured).
- **N3, `never_reap` substrings are matched on the root's command line, which holds the user's command.** A zombie such as
  `while pgrep -f story_run.py; do sleep 60; done` is kept forever, and `kept_never` is never logged. This is safe but silent. Log a
  `kept` line.
- **N4, ages are wall-clock time.** After a laptop suspend, every earlier background call is "> 2 h" at the first trigger after
  wake and is stopped under FA(a). This edge is not named in the spec.
- **N5, the WAITS line shows only the LAST run (spec §5.3).** A stop is erased by the next zero run of any trigger, so run.log is
  the only durable record. The `running`/`died` states that the twin reports are silent here.
- **N6, Q6:** `ascii_clip` is the 7th ASCII sanitizer in tools (journal_echo:487, session_context:1020, tier_echo:141,
  crap_report:589, escape_check:322, wiring_check:261). Proposed node: converge them.
- **N7, placement:** remove the `compact_snapshot_next` import fallback (session_context_next:2454) and the `hasattr` guards. Copy
  the candidates from git, not from the worktree: `git ls-files --eol` shows `w/crlf` for session_context_next.py and
  dod_gate_next.py (the index is LF).

## K4 observations
(a) DEFECT → F4. (b) BY DESIGN: `--limit 60` is a manual override, and the default 7200 decides what the triggers stop. runall.sh
at 2580 s would die only past 2 h (the FA(a)/FL(a) cost). K4 step 2 expected "exactly that tree"; that expectation was a flaw in
the witness design. (c) BY DESIGN: spec §5.1 says a PowerShell tree is never S3, and `Start-Sleep` runs in-process, so S1 is
impossible; the shape is only a log label and FA(a) stops the tree anyway. NOTE: in check 27(e) every PowerShell stop reads S0, so
its form must be read from the kids.

## Dispatch questions
1. **Another session's tree: no.** Measured: the other tabs are separate `claude.exe` processes under the app (48864 and 12 more).
   Selection needs ppid == the session pid AND a creation-time check (`select` :228, :271), and orphans are only reported (FO a).
   The only edge is N1, which stops nothing. **A live call of this turn:** a foreground call is capped at 600 s by the tool
   (estimate from the tool's max timeout), so it never reaches 7200. Background calls older than 2 h are stopped BY DESIGN (FA a).
   That includes calls of other live workers: subagents share `claude.exe` 26860 (measured: my own walk ends at 26860). The
   reaper's ancestor protection (`protect` :239-242) breaks once the launcher exits, so a call older than 2 h that ran the merge
   is protected only while `worktree_sweep.py` (a `never_reap` substring) is in its tree. Suspend edge: N4.
2. **dod_gate: yes.** Both levels are wrapped, and the row `a_raise_is_one_line` covers it. **session_context: yes, one line,**
   but F2 can lose the whole hook output. **post-merge: the exit is unchanged,** but the output is not one line (F8).
3. **Yes: an unknown never reads as own.** A stamp of "unknown" is never equal to `%d-%.3f`, and a walk that returns None gives the
   unstamped line. The unknown is shown as foreign, though (F6).
4. **worktrees_line twin:** the timeout diverges (F2), and the running/died states are silent (N5).
   **hook_liveness_probe 12:** runs in-process, its tmp folder is not a git repo, so the result is one "not started" line and the
   first-line check holds. **13:** `--root tmp`; the stamp branch is not reached. **18:** starts a real reaper (F5).

## Standing questions (rule 22)
- Q1 fit: §5.0-§5.3 are met (limit AT kept, BEYOND stopped; hops 32/33; decode cap; log caps; one attempt per pid; CREATE_NO_WINDOW;
  broken rows → exit 1). Not met: §5.2 "failed: winerror" visible (F4).
- Q2 builder decisions: the `_WRAP` silencer is right but not applied everywhere (F5). The `_next` import is fine until placement
  (N7). Walking the session twice: F13. The `own_proc` param is additive. The odd stamp shown as foreign is the unsafe pick (F6).
- Q3 seams: the changes are additive (worktrees → waits → wiring; launch after `_record_returned` on exit 0). The `mechanism_gate`
  seam is missed (F1).
- Q4 class: F1, F5 (probe/test isolation), F2 (twin). Leaving lines: N1 `<walk names the app's utility process | узел: new, Lead opens>`;
  N6 `<ASCII sanitizer convergence | узел: new>`.
- Q5 tests: (a) the selection rows would catch errors at the limits; nothing would catch F3 or F4. (b) expected values trace to
  spec rows, except the odd-stamp row (F6). (c) No row for kid failures (F4) or for the post-merge hook text (the K4 witness did
  not cover post-merge). (e) no duplicates found. (f) tests-over is missing (F14). (g) the new `test_wait_reaper.py` runs in 4.19 s:
  three tables, one world.
- Q6 duplication: F7, N6. The lock, status, spawn and repo_context come from worktree_sweep (reused).
- Q7 quality: F13, F4 (names that lie about units).
- Q8 n/a (no package path). Q9: no ratchet file touched. Q10: AR n/a (forge tools). Q11: data checks only; the S3 label uses
  `wait_loop_forms`, and the shape decides nothing.
- Q12 ONE ROAD: one selection for both shells. The empty POSIX row is a data row with a declared default (FP a, Lead decision in
  the spec). None found beyond that: I grepped `nt|posix|platform` in session_proc and wait_reaper.

## Spot-checks
- Builder's claim "the deadline test fails the same on main": REPRODUCED without candidate env, `assert 13.875 < 10.0`.
- `*_PATH` read only in tests: the grep outside `test_*` is empty; the positive control is 5 test files.
- 65-passed witness re-run; the K-WIRE and narrative rows re-run (see the trail).

## Trail
Read: the spec r2 in full; critic.md :170-310; worktree branch: `tools/session_proc.py` in full, `tools/wait_reaper.py` in full,
`tools/wait-reaper.json`, `tools/test_wait_reaper.py` in full, the session_context / dod_gate / compact_snapshot `_next` diffs
against the live files, `tools/post-merge.next`, `.githooks/post-merge`, the test diffs, the SKILL diff, worktree_sweep.py
:90-135, :262-300, :855-875, :985-1060, :1085-1130, :1195-1245, gitcmd.py :35, :76-106, session_context_next :1917-1960,
:2340-2389, :2624-2700, hook_liveness_probe :205-248, :440-490, :910-935, :1104-1160, :1465-1580, test_hook_liveness_probe
:975-1012, test_worktree_sweep :1000-1100, test_mechanism_gate :900-960, :1030-1075, mechanism_gate MECHANISM_PREFIXES,
`.gitattributes`, the K4 witness in full.

Runs (verbatim tails):
- `python -m pytest tools/test_wait_reaper.py -q` → `65 passed in 4.19s`
- `SESSION_CONTEXT_PATH=… DOD_GATE_PATH=… pytest test_session_context.py test_dod_gate.py -k k_wire` → `16 passed, 415 deselected in 5.89s`
- `COMPACT_SNAPSHOT_PATH=… pytest test_compact_snapshot.py -k narrative` → `4 passed, 56 deselected in 1.24s`
- the deadline test, no env → `FAILED … assert 13.875 < 10.0`, `1 failed, 321 deselected in 16.87s`
- closure probe (test_mechanism_gate helpers) → see F1
- the session chain via `session_proc.WinApi` → python 35692 ← bash ×3 ← claude.exe 26860 ← claude.exe 17100 ← explorer;
  `session_process()` = 26860; CIM: 17100 = app `Claude.exe`, 11816 = `Claude.exe --type=utility` parent of `-NoExit` 8900/10312
- a dry `wait_reaper.py` run on the live session: DENIED by the permission classifier (not run). Live selection rests on the K4 witness.

```json
{
  "verdict": "blocker",
  "blockers": [
    "F1: tools/wait_reaper.py, tools/session_proc.py, tools/wait-reaper.json are outside mechanism_gate MECHANISM_PREFIXES; the measured import closure of the placed session_context/dod_gate reaches session_proc and wait_reaper, so test_mechanism_gate transitive-closure goes red and kill-set edits escape the axis gate -- add three rows in the placing commit",
    "F5: after placement hook_liveness_probe case 18 (dod_gate subprocess, cwd=REPO) and test_session_context deadline Popen test (main uses repo_root) spawn REAL wait_reaper --apply runs on the live session; pass payload cwd to launch in dod_gate and silence the Popen test with the _WRAP form"
  ],
  "fixes": [
    "F2: launch and waits_lines use the 120 s git default; the twin worktrees_line uses 5 s -- pass timeout=5, one repo_context",
    "F3: waits_lines launches before reading status.json; the new run resets counts to running/0 -- read first, then launch",
    "F4: per-process stop outcomes of kids are not logged and failed counts processes while stopped counts trees; log fails=, map terminate winerror 5 on an exited process to gone, add a row",
    "F6: an odd narrative stamp (unknown) is shown as another session's -- show the no-stamp check-it-is-yours line",
    "F7: the stamp value form is encoded twice (narrative_header_line, _session_proc_id) -- one encoder",
    "F8: post-merge one-liner prints a multi-line traceback on import failure -- wrap in try",
    "F13: select is 78 lines; three session walks per SessionStart",
    "F14: no tests-over line in ed466898 / 094fbf95 while tests exceed product lines",
    "F15: SKILL step 5a should say --apply --pid <root>"
  ],
  "class_completeness": "Hook-path module entering the mechanism net: missed (F1, sibling of worktree_sweep.py / worktree-junk.json rows). Hook side effects under probes/tests: dod_gate tests silenced, test_session_context Popen test and hook_liveness_probe case 18 not (F5). Twin worktrees_line: git timeout diverges (F2), running/died states silent (N5, spec level). Stamp encoder twin (F7). Leaving: N1 walk names the app utility process (new node), N6 ASCII sanitizer convergence (new node). Axis 11 recognizer: reaper reads wait_loop_forms only, no second grammar.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-bounded-waits-mechanism-spec-r2.md",
      ".claude/worktrees/bw-kwire/tools/session_proc.py",
      ".claude/worktrees/bw-kwire/tools/wait_reaper.py",
      ".claude/worktrees/bw-kwire/tools/wait-reaper.json",
      ".claude/worktrees/bw-kwire/tools/test_wait_reaper.py",
      ".claude/worktrees/bw-kwire/tools/session_context_next.py (diff vs live, 1917-1960, 2340-2389, 2624-2700)",
      ".claude/worktrees/bw-kwire/tools/dod_gate_next.py (diff vs live, 760-842)",
      ".claude/worktrees/bw-kwire/tools/compact_snapshot_next.py (diff vs live, 60-127, 770-800)",
      ".claude/worktrees/bw-kwire/tools/post-merge.next and .githooks/post-merge",
      ".claude/worktrees/bw-kwire/tools/test_session_context.py, test_dod_gate.py, test_compact_snapshot.py (diffs)",
      ".claude/worktrees/bw-kwire/tools/worktree_sweep.py, gitcmd.py, hook_liveness_probe.py, test_hook_liveness_probe.py, test_worktree_sweep.py, test_mechanism_gate.py, mechanism_gate.py (ranges in Trail)",
      "scratchpad/k4_witness.txt"
    ],
    "reruns": [
      {"command": "python -m pytest tools/test_wait_reaper.py -q", "result": "65 passed in 4.19s"},
      {"command": "SESSION_CONTEXT_PATH=tools/session_context_next.py DOD_GATE_PATH=tools/dod_gate_next.py python -m pytest tools/test_session_context.py tools/test_dod_gate.py -q -k k_wire", "result": "16 passed, 415 deselected in 5.89s"},
      {"command": "COMPACT_SNAPSHOT_PATH=tools/compact_snapshot_next.py python -m pytest tools/test_compact_snapshot.py -q -k narrative", "result": "4 passed, 56 deselected in 1.24s"},
      {"command": "python -m pytest tools/test_session_context.py -q -k test_main_stdout_deadline_timeout_exits_immediately_via_subprocess (no candidate env)", "result": "1 failed: assert 13.875 < 10.0 -- builder claim reproduced"},
      {"command": "closure helper of test_mechanism_gate on session_context_next / dod_gate_next", "result": "uncovered: session_proc, wait_reaper (plus the _next names)"}
    ]
  }
}
```
