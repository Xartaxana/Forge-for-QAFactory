# t-1131 — plan review: bounded waits, the gate and the reaper (spec t-1122)

Critic on plan (CLAUDE.md rule 3; a mechanism that kills processes on the execution path). Reviewed:
`docs/tasks/specs/20261117-bounded-waits-mechanism-spec.md`, all 649 lines, including "Lead measurements and decisions"
(:629-648). The keys K1-K11 come from the dispatch. Nothing was killed or started apart from three short read-only
`Get-CimInstance Win32_Process` listings (trail at the end).

**Verdict: READY WITH FIXES.** The gate G1 is sound, apart from three grammar holes and one teaching text the spec missed.
The reaper as written stops none of the measured stuck forms. Its selection text also still uses the pre-M1 definition,
under which "session shell" means "any child of a process named claude.exe", and the app itself is claude.exe. Every fix
below is exact text for the spec. Fix F-R0 needs one capped measurement by the Lead (the PowerShell tool-call command
line) before the K-REAP dispatch.

## Live measurements this review made (read-only, 17.11.2026 13:03, Windows, harness 2.1.321)

- **The chain of my own Bash call.** `powershell(46936) <- bash(43816) <- bash(48708, usr/bin/bash.exe) <-
  bash(45960, Git/bin/bash.exe) <- claude.exe(26860, ...\claude-code\2.1.321\...\claude.exe --output-format stream-json ...,
  created 14.11.2026 15:57:03) <- claude.exe(17100, "C:\Program Files\WindowsApps\Claude_5.1231.2.0_x64__...\app\Claude.exe")
  <- explorer.exe`. What follows from it:
  - The SESSION process lives for days. This one has run 3 days, through every compaction and every subagent.
  - Its parent, **the app, is also named `claude.exe`**. Windows names are case-insensitive, and CIM reports `claude.exe`.
  - The app has 12 more `claude.exe` helper children (pids 17456 … 18192, created 12.11). There is a second session
    `claude.exe` (48864, created 13:00:45 today, with a `node.exe` child).
- **The app's persistent shells.** `powershell -NoExit` pids 8900 (12.11) and 10312 (14.11 15:57:04) have parent **11816,
  an app helper `claude.exe`**. That helper is a child of the app 17100, not of a session.
- **The direct children of the session 26860.** One `conhost.exe` (age 3 days). The rest are `bash.exe` tool-call roots,
  each with command line `"C:\Program Files\Git\bin\bash.exe" -c "source …/shell-snapshots/snapshot-bash-….sh 2>/dev/null
  || true && export TEMP=… && shopt -u extglob … && eval '<THE USER COMMAND, single-quote spliced as '\"'\"'>' < /dev/null
  && pwd -P >| …/claude-c701-cwd"`. I measured this on a call whose user command was itself a
  `for i in 1 2 3; do test -f /nonexistent && break; sleep 0; done` loop. The loop appears verbatim inside the `eval '…'`
  argument.
- The literal `< /dev/null` after the `eval` explains the Lead's M1 (stdin is `/dev/null`). It is the harness wrapper,
  not a property of bash.

## K1. Evidence §2 — HOLDS on the load-bearing rows; two negatives FAIL

| row | verdict | trail |
|---|---|---|
| E1 the one PreToolUse hook on Bash/PowerShell | holds | `.claude/settings.json:33-41` |
| E2 no loop/sleep recognizer in the gate | holds | grep `\buntil\b\|sleep` -i in `tools/hygiene_gate.py`: one hit, :1544, a comment ("not known until the shell runs it"). Positive control: the same grep form finds that comment |
| E6 the gate does not read `run_in_background` | holds | grep `run_in_background\|agent_id` over `hygiene_gate.py`: only `agent_id` at :1511-1512. That hit is the positive control of the same grep |
| E7 `run_in_background` and `timeout` sit in `tool_input` | holds | transcript `8781f497-…jsonl:2264`: `"name":"PowerShell","input":{…` and `"timeout":600000,"run_in_background":true` |
| E8 the gate runs for subagents' calls | holds (code level) | `hygiene_gate.py:1511` branches on the payload's `agent_id`; `test_hygiene_gate.py:329-376` rows |
| E12 SessionStart = `session_context.py` only, `MAX_LINES = 25` | holds | `.claude/settings.json:5-14`; `tools/session_context.py:190` |
| E13 SubagentStop = `dod_gate.py`; `_record_returned` only on exit 0 | holds | `.claude/settings.json:107-116`; `tools/dod_gate.py:805-806`. The early returns at :763-773 (stdin deadline, bad JSON, no session_id) also exit 0 without the call, so no reaper launches on them. That is the right direction |
| E14 PostToolUse reads no process state | holds | `.claude/settings.json:65-87` |
| E15 post-merge starts the sweep | holds | `.githooks/post-merge:1-8`; `tools/wave.py:52` |
| E16 `spawn_detached` uses CREATE_NO_WINDOW, its own group and **CREATE_BREAKAWAY_FROM_JOB** | holds, with a consequence the spec misses (K3-b) | `tools/worktree_sweep.py:1209-1222` |
| **E18 "No tool in `tools/` lists or kills processes"** | **FAILS** | `tools/journal_write.py:612-617` `_kill_tree` runs `taskkill /F /T /PID` and `os.killpg`; `tools/test_redundancy.py:70-76` does the same. The spec's grep pattern did not contain `taskkill`. My pattern `taskkill\|os\.kill\b\|killpg\|Stop-Process\|TerminateProcess\|Win32_Process\|Get-CimInstance\|tasklist` found them. Positive control of the same shape: `0x08000000\|CREATE_NO_WINDOW` → `worktree_sweep.py:1215` |
| **§6.2 "No other §9 subsection names waits (grep `until\|Start-Sleep` in RUNBOOK: :395, :406 only)"** | **FAILS** | `docs/RUNBOOK.md:237-239`, §9.1(f): «Фоновый цикл `until` по `driver-runs.jsonl` и хвосту лога, с потолком инструмента не больше 10 минут на вызов, повторяемый, либо инструмент Monitor». Positive control: the same grep finds :395 |

## K2. Gate G1 — HOLDS in design; FAILS on four points

Holds:
- The grammar reads only the masked text. A quoted string, a heredoc body, a comment, `grep -n while f` and
  `git log --until=` all pass (§3.4 :165, rows W-quoted/W-heredoc/W-comment/W-git-until).
- The keywords follow Bash case rules: `Until`/`WHILE` are commands, not keywords. This is correct Bash.
- A loop in a script file and a loop inside `bash -c` pass as named residuals; the reaper is the net (but see K3-a).
- `while read … done < f` passes (C4).
- The door text names what is wrong, what is expected and a paste-ready capped form. The number in it is formatted from
  `MAX_WAIT_SECONDS` (:109-112).
- No informed pass, with a reason (:114-116). The door is always usable, and the gate's other three classes have no
  informed pass either. I accept this.
- The positional invariant (:147-151) keeps the existing order.

Findings:
- **G-1 (grammar not closed): is `for` a recognized wait loop or not?** §3.1 :78-81 defines the recognized Bash loop as
  `while`/`until` only ("`for`/`select` push too"). But C1 (:92) and rows W-seq-BEYOND, W-seq-100000 and
  W-ps-range-BEYOND REFUSE a `for` loop over budget.
  - If `for` loops are recognized, then "not capped (C1-C4) → refused" refuses `for f in a b c; do x; sleep 1; done`,
    `for f in *.md; do …; sleep 2; done` and `for x in $(cat list); do …` (a false positive on a list loop, one of the
    dispatch's named traps).
  - If they are not recognized, the BEYOND rows cannot fire.
  - Fix G-1: add to §3.1 after :86: «A `for`/`select` (Bash) or `for`/`foreach`/`ForEach-Object` (PowerShell) loop is
    bounded by its list. It is refused ONLY when its budget is literal and over MAX_WAIT_SECONDS. The budget is literal
    for the C1 counted forms, and for a literal word list (count = the number of words). A glob, a `$(…)` list or a
    variable list gives budget unknown → pass. A `for` loop is never refused as "not capped".» Add rows:
    `for f in a b c; do x; sleep 1; done` → silent; `for f in *.md; do x; sleep 5; done` → silent.
- **G-2 (a false "capped" verdict): the connective and the direction of a C2/C3 cap are not stated.**
  - `while [ $i -lt 30 ] || ! test -f f; do i=$((i+1)); sleep 20; done` is unbounded (the `||` keeps it running after
    i ≥ 30), yet C3 calls it capped.
  - The same holds for `until [ $i -ge 30 ] && test -f f`, and for a direction mismatch such as
    `while [ $i -ge 0 ]; do i=$((i+1)); sleep 5; done` (C3 says "compares … AND increments", budget 0).
  - Fix G-2: add to C2/C3: «the counter/clock test binds only when it stands alone or is joined at the top level of the
    condition by `&&` for `while` (PowerShell `-and`) and by `||` for `until` (`-or`). The comparator matches the loop's
    sense: for `while`, `-lt`/`-le`/`<`/`<=`; for `until`, `-ge`/`-gt`/`-eq`/`>=`/`>`. Otherwise the loop is not capped
    → refused.» Add rows: `while [ $i -lt 30 ] || ! test -f f; do i=$((i+1)); sleep 20; done` → deny; the direction
    mismatch row → deny.
- **G-3 (a teaching text left behind): RUNBOOK §9.1(f) :237-239** teaches an `until` background loop whose only ceiling
  is the tool timeout ("потолком инструмента не больше 10 минут на вызов"). Note that a background call has NO tool
  timeout (E24, the 1.5-11 h screenshot), so the text is already wrong today. After G1 the night agent following it gets
  refused.
  - Fix G-3: K-DOC also replaces :237-239 with «6. **(f) Ждёт прогон, а не человека.** Ожидание — ограниченный цикл
    (`for i in $(seq 1 30); do <проверка driver-runs.jsonl / хвоста лога> && break; sleep 20; done`, не больше 3600 с на
    вызов, §9.8), повторяемый, либо инструмент Monitor. Сообщений владельцу ночью нет.» Add this to §6.2 as an applied
    neighbour, and correct §6.2's false negative.
  - The other texts that quote the bad form (`docs/RUNBOOK.md:395` (replaced by §6.1), :406, `plans/builder-rules.md:102`)
    quote it as an ANTI-example. They stay true. My grep `while true|while \[|until \[|until grep|until test|; do sleep|Wait-Job|Wait-Process|tail -f|sleep infinity`
    over `docs plans .claude/agents .claude/skills PROCESS CLAUDE.md BOOT.md experiments/measurers` (worktrees, snapshots
    and reviews excluded) found only :395 and builder-rules:102. The :395 hit is the positive control of the same shape.
    `.claude/agents` and `.claude/skills` have none.
- **G-4 (an unnamed edge): the harness's Monitor tool.** The harness's own Bash tool text (this session's tool
  description) says "use Monitor with an until-loop to wait on a condition". RUNBOOK :238 also names Monitor. Its
  `tool_name` is not `Bash|PowerShell`, so G1 never sees it, but its process tree sits under the session and is in the
  reaper's reach.
  - Fix G-4: add a §3.4 row and a §5.2 row: «a Monitor tool call: the gate does not see it (it matches only
    Bash|PowerShell; how Monitor bounds itself is not measured). The reaper treats its process tree like any tool call,
    by age and shape.» Name Monitor in the door text: «… or check once / use Monitor and come back later».

Minor (fold into the fixes): add rows for `{ until x; do sleep 1; done; }` (a brace group statement start) → deny, for
the clock AT `[ $SECONDS -ge 3600 ]` → silent, and for MAX_LOOP_DEPTH AT (64 nested) → recognized. Rows already exist for
BEYOND only.

## K3. The reaper — FAILS as written (3 blocking defects); per-process safety after the fixes

**K3-a BLOCKER: the selection cannot catch the measured forms.**
- Age is taken on the candidate P itself (§5.1 rule 1, :209). S1 selects a `sleep` process (:215). In a wait loop the
  `sleep` child is re-created every iteration, so its age is at most one sleep interval (20 s). It never passes 7200.
- S3 unwraps `-c` "at most 3 hops" (:217) and calls `wait_loop_forms`. The measured root command line holds the user's
  command inside `eval '…'` with `'\"'\"'` splicing (measurement above). `hygiene_gate` masks quoted text before any
  recognizer (E9; `hygiene_gate.py:24-25`), so `wait_loop_forms` on the unwrapped `-c` text returns nothing.
- Result: neither S1 nor S3 ever fires on a real Bash wait loop. R-old-loop (:373) passes only because its fixture is
  unrealistic: it gives the sleep child an age of 3 h.
- PowerShell: `Start-Sleep` runs inside powershell.exe, so S1 can never fire there. S3 depends on the PowerShell
  tool-call command line (cmd.exe → powershell.exe, M1), whose form nobody has measured. The PowerShell side is
  uncovered: this is a one-road gap (rule 19).
- Fix F-R1 (replace §5.1 rules 1-3): «A CANDIDATE is a TOOL-CALL TREE, not a single process. Its ROOT is a direct child
  of THIS session's `claude.exe` (F-R2), created after that `claude.exe`, whose name is in the data row
  `tool_call_roots` (`bash.exe`, `cmd.exe`, `sh`, `bash`). Its age is the ROOT's age: strictly more than `limit_seconds`.
  Its shape is one of:
  - S1: a `sleep` process anywhere in the tree;
  - S3: the user command, decoded from the root's command line by the data row `wrapper_forms`, gives a non-empty
    `hygiene_gate.wait_loop_forms(user_command, tool)`.

  `wrapper_forms` holds one row per measured harness wrapper. Bash (measured 17.11, harness 2.1.321): Windows argv →
  the `-c` argument → the single-quoted word after the last top-level `eval`, with `'\''` and `'"'"'` re-joined. The
  PowerShell row comes from F-R0. A root whose command line matches no row → no S3 (keep). The log line
  `unwrap-failed <root pid>` and the status counter `unwrap_failed` make the miss visible at calibration, never
  silent.» Test rows: R-old-loop with a REAL fixture (the root command line captured above, root 3 h, sleep child 15 s)
  → stopped; the same root with a young `sleep` and no loop in the payload → S1 stopped; R-unwrap-unknown (a future
  wrapper) → kept + `unwrap_failed`.
- Fix F-R0 (a Lead measurement before K-REAP, one capped call): the command lines of the `cmd.exe` and the
  `powershell.exe` of ONE background PowerShell tool call running `for ($i=0; $i -lt 30; $i++) { Start-Sleep 2 }`. Put
  the result into the `wrapper_forms` PowerShell row and add one R-row fixture. Until it is measured the PowerShell row
  stays empty, and the spec says so as a named residual that has a node (the reaper reports a PowerShell root over the
  limit, never kills it).

**K3-b BLOCKER: "this session" cannot be found the way the decision states.** The decision (:637-638) says "this
session" = the `claude.exe` the reaper descends from.
- The reaper is started by `spawn_detached`, which uses CREATE_BREAKAWAY_FROM_JOB (`worktree_sweep.py:1217`) and never
  waits. The hook that spawned it exits within milliseconds, and so do the shells between it and the session. The CIM
  read takes 1-2 s, so by then the reaper's `ParentProcessId` names a dead pid and its ancestry walk ends there.
- On top of that, §5.1 rule 2 (:211-212) defines a session shell as "a process whose parent's name is in
  `harness_process_names`" (= `claude.exe`). Measured above, that set contains:
  - the session `claude.exe` itself (its parent is the app, named `claude.exe`);
  - all the app helpers' children, including the `-NoExit` shells (parent 11816, an app helper);
  - every other session.

  Only the `never_reap` substring `-NoExit` protects the app shells under that text.
- Fix F-R2: «The LAUNCHER (the function the hooks call, in `wait_reaper.py`, owned by K-REAP) resolves the session
  BEFORE it spawns. It walks from `os.getpid()` up to the NEAREST ancestor named `claude.exe`, in-process, with no child
  process: on Windows through `CreateToolhelp32Snapshot` plus `GetProcessTimes` via ctypes; on POSIX through
  `/proc/<pid>/stat` or a `ps -o ppid=,comm= -p` call. It passes `--session-pid <pid> --session-created <ISO>` to the
  detached reaper. The reaper treats as "this session" only the process with that pid AND that creation time. The
  nearest `claude.exe` is the session; the app is further up and is never chosen. Session not found → nothing is
  stopped, status `no-session: <reason>`, and the WAITS line says so with the door
  `python -B tools/wait_reaper.py --session-pid <pid>`.» The same text replaces "the launcher's own ancestry" in F8
  (:489-490) and in §5.3 (:251). Rows: R-nearest (app `claude.exe` → session `claude.exe` → root → sleep: the app's
  other children are untouched); R-no-session → no stop, status `no-session`.

**K3-c BLOCKER: Windows does not re-parent orphans.**
- A dead parent's pid can be reused. A long orphan's `ParentProcessId` can then point at a NEW tool-call root of this
  session, making the orphan look like a descendant. Examples of such orphans: the night driver started by
  `Start-Process` from a PowerShell call that has since ended (RUNBOOK :295), and the detached worktree sweep.
- Fix F-R3: «A parent link counts only when the parent's CreationDate is EARLIER than the child's. Otherwise the child
  is an orphan and outside every tree. This applies on every hop of every walk (launcher and reaper).» Row R-orphan-reuse:
  a 9 h `story_run.py` whose `ppid` equals a 10-minute-old root of this session → kept, not in the tree.

Further reaper findings (fixes in this round):
- **F-R4 two sessions at once.** The single lock and the single `status.json` in `<git common dir>/wait-reaper/`
  (:242, :261) make the second session's reaper exit `busy`, and with F8(a) its own tree is never reaped. Its WAITS line
  then shows the OTHER session's result.
  - Fix: «lock and status per session: `<git common dir>/wait-reaper/<session-pid>-<created yyyymmddHHMMSS>/`; one
    `run.log` stays shared (append with the session pid in each line). A busy lock for the SAME session exits `busy`
    (one reaper per session at a time; six parallel SubagentStops launch one).» Row: two sessions' launches at the same
    moment → both run.
- **F-R5 the kill order.** "Leaves first, then up" (:225) kills the `sleep`, and the still-alive loop bash at once starts
  the next `sleep`.
  - Fix: «stop the ROOT's tree in one move. Windows: `taskkill /PID <root> /T /F` with CREATE_NO_WINDOW, after
    re-reading the root's creation time. POSIX: SIGTERM to the root's process group if the root leads one, else to the
    collected pids ROOT-FIRST, then SIGKILL after 2 s.» A `sleep` orphaned in between ends by itself within one interval
    (harmless; logged as `gone` if it is seen again).
- **F-R6 never_reap.** Add `worktree_sweep.py` (cheap; today it is protected only by orphaning) and `story_step.py`.
  Drop `gh` as a name-substring row: it matches any path holding "gh" (e.g. `…\high\…`). Use `gh.exe`/`gh` as a whole
  process name.
- **F-R7 POSIX.** `harness_process_names` is measured for Windows only. Fix: «on POSIX the reaper runs report-only until
  the POSIX session process name is measured and written into the row» (FR-59: the safe default it declares). Row
  R-posix expects `reported`, not `stopped`.

Per process, after F-R1…F-R7 (safe = never a candidate):

| process | verdict | the row that proves it |
|---|---|---|
| a live builder's capped wait near its cap | safe: root age ≤ the sleep budget (≤ 3600) plus the check time; limit 7200. Edge: a C1 loop of 180 × 20 s whose checks also take 20 s each reaches 7200 s of wall time. The door could teach the clock cap C2 for long waits; not blocking | §5.1 rule 1; §3.1 budget |
| a worker's long local test run | safe: no `sleep` in the tree, no loop in the payload; foreground calls end at the tool timeout (600000 ms, E7) | F-R1 shapes |
| the night driver (RUNBOOK §9.3 `Start-Process`, :295) and its `claude -p` children | safe: an orphan once its PowerShell call ends (F-R3); a `never_reap` row; its `claude -p` processes are other `claude.exe` sessions | F-R3, :221 |
| a dev server started in the background | safe under the shape rule (no sleep, no loop); reported under F-R8 | F-R1 |
| the worktree sweep | safe: detached with breakaway, an orphan of a dead hook (F-R3), plus the F-R6 row | `worktree_sweep.py:1209-1222` |
| `journal_write accept --run` | safe: its own `RUN_TIMEOUT = 600` (`tools/journal_write.py:63`) and its own tree kill (:612-617) | — |
| another session's processes | safe only with F-R2 (the session is known by pid + creation time; nearest `claude.exe`) | measured second session 48864 |
| the app's `powershell -NoProfile -NoExit` | safe by ancestry under F-R2: their parent is app helper 11816, not this session. Under the spec's text only the `-NoExit` substring saves them | measurement above |

- **7200 s against what the repo documents as long:**
  - the tool timeout, 600 s (E7);
  - `RUN_TIMEOUT` 600 (`journal_write.py:63`);
  - the night agent's per-call wait, ≤ 10 min (RUNBOOK :238);
  - the sweep, alive 15 min after its hook (RUNBOOK :285);
  - the full CI set, ≤ 30 min (docs/TESTING.md «Потолки набора»), and `gh run watch` ends by itself;
  - the night driver runs hours, but it is exempt and orphaned.

  7200 is above every documented shaped wait. **Holds.**
- **Unreadable list:** a status and an exit code, never a silent pass (:240). **Holds.** Add the same for `no-session`
  (F-R2) and `unwrap_failed` (F-R1).

## K4. F6 — kill from day one, or report first?

Recommendation: **kill from day one for the shaped trees (S1/S3), on one condition**, and **report-only for unshaped
old trees** (F-R8 below).

The condition is a selection witness on the live machine before the trigger files are placed (rule 13: empirics on real
data, not on fixtures). It runs as part of the K-WIRE acceptance:
1. The Lead starts one background `for i in $(seq 1 900); do sleep 1; done`.
2. The Lead runs `python -B tools/wait_reaper.py --limit 60` (the dry list) after 70 s.
3. The witness is the verbatim list. It must show exactly that tree (root + `sleep`) and nothing else: no `-NoExit`, no
   process of session 48864-like peers, no `conhost`.
4. Then `--apply --limit 60` stops it, and the log line is checked.

Reason: after F-R1…F-R3 the selection is a conjunction of four data facts:
- this session by pid + creation time;
- the root is older than 2 h;
- a `sleep` process or a decoded loop in the tree;
- not in `never_reap`.

Every stop is a log line read at check 27(e). The false-positive surface is a 2-hour-old loop of THIS session, which is
exactly the defect.

What report-only would cost the owner:
- Every leftover lives on until a coordinator reads a WAITS line and runs `--apply` by hand. That hand step is the
  discipline that failed on 07.10, 16.10, 20.10 and 17.11 (§8 (d)).
- A long session (this one has run 3 days) only gets a SessionStart at a compaction, so the leftovers keep piling up in
  the Background-tasks list for days, just as on her screenshot.
- A week of report-only buys one week's evidence on the selection. The witness above buys the same evidence in two
  minutes.

## K5. The dropped class — the 11 h call is NOT ended by the mechanism as decided (FAILS)

The decision says (:645) "the reaper's age rule covers a call that hangs for an unknown reason". It does not: §5.1
requires a stuck SHAPE.
- The 11 h command `( cd <tree> && cat > /dev/null; python - <<'PYEOF' … PYEOF )` has no loop and no `sleep`, so S1/S3
  never fire.
- S2 (cat / `python -`) is not addressed by the decision. Since G2 and `stdin_reader_forms` leave, S2 has no ground left:
  stdin is `/dev/null`, so a `cat` or `python -` blocks on something other than stdin.
- And spec :7 says the live processes were "three bash processes" — no `cat`, no python.

So the mechanism neither refuses this call nor stops it.

- Fix F-R8 (cheap, and the evidence owed): «S0, unshaped: a tool-call tree of this session older than `limit_seconds`
  with no S1/S3 shape is REPORTED, never stopped (the WAITS line counts it, with the door
  `python -B tools/wait_reaper.py --apply --pid <root>`). For every S0 report and every stop, the log line records:
  - the root's command line, decoded user command first, up to 2000 ASCII characters (160 does not hold a heredoc);
  - every live descendant as `name/pid/age/first 200 chars of cmd`.»

  The next occurrence of the 11 h class then names the child that was alive, and check 27(e) turns it into a shape row or
  a named residual. Killing S0 trees is a later Lead decision, made on that log, not now: a dev server or an unknown long
  run is not something code can judge as dead (P27).
- Drop S2 from §5.1 and drop `stdin_reader_forms` from S3. Rows R-cat-old and R-py-dash-old become S0 rows (`reported`).
- Correct the decision line :645-646 to: «The reaper REPORTS such a call (S0) and records its live children; it stops
  only the S1/S3 shapes.»

## K6. No windows — HOLDS for the spawn sites named, with two additions

Spawn sites in the cards:
1. **The detached reaper.** `worktree_sweep.spawn_detached` with CREATE_NO_WINDOW | NEW_PROCESS_GROUP | BREAKAWAY, stdio
   DEVNULL (`worktree_sweep.py:1209-1222`). Its hidden console is inherited by its children.
2. **The lister.** `powershell -NoProfile -NonInteractive … Get-CimInstance` with CREATE_NO_WINDOW and a 20 s timeout
   (:243).
3. **The stop.** `taskkill` with CREATE_NO_WINDOW (:243).
4. **post-merge.** The sh hook runs `python tools/wait_reaper.py --launch post-merge` in the foreground, inside git's
   console; that python then spawns through (1).
5. **The F-R2 session walk.** It must be IN-PROCESS (ctypes Toolhelp32), never a `powershell`/`wmic` child on the hook
   path. Such a child would add a process, and possibly a window, plus 1-2 s on every SessionStart and SubagentStop.
   Add this to the K-REAP edges.

The `tools/journal_write.py:631` candidate:
- Popen of `bash -c` with only CREATE_NEW_PROCESS_GROUP. Its sibling at :615, `taskkill` via `subprocess.run`, has no
  flag at all, and neither does `tools/test_redundancy.py:72`.
- A console child inherits the parent's console. `journal_write` runs inside a tool-call bash that has the session's
  hidden console (`conhost.exe` 23148, a child of session 26860, measured), so a visible window from these sites is NOT
  shown. Estimate, not measured.
- Recommendation: its OWN small node rather than a line in K-WIRE. `journal_write.py` is in no card's owns, and it is a
  mechanism file on its own commit path. The node: add `CREATE_NO_WINDOW` (0x08000000) to :615, :631 and
  `test_redundancy.py:72`; witness `python -m pytest tools/test_journal_write.py -q`. Low priority, small-work batch.

## K7. Rule text §6 — FAILS (untrue after G2 was dropped); otherwise holds

- §6.1 :271-273 still says the gate refuses «команде, которая читает stdin, когда его ничто не кормит (`cat` без файла,
  `python -` без here-doc)». After the decision this is false.
  - Fix: delete from «и команде, которая читает stdin» through «без here-doc)». In :276-277 replace «вызовы этой сессии
    старше 2 ч с зависшей формой» with «вызовы этой сессии старше 2 ч с циклом ожидания или `sleep`; прочие вызовы
    старше 2 ч он только называет в строке `WAITS:`» (F-R8).
- §6.3 :294-296, the builder phrase: delete «and a stdin read nothing feeds». The resulting phrase is consistent with the
  no-briefs spec: its row 13 (`20261117-no-briefs-fold-into-roles-spec.md:185`) makes RUNBOOK §9.8 the home and gives
  builder.md rule 9 one phrase plus a pointer, and its rule 9 text (:241-243) already ends «(the rule: `docs/RUNBOOK.md`
  §9.8)». No new document is made. **Holds.**
- §6.1 is short (10 lines) and stays true after the gate lands only with the edits above, plus G-3's neighbour
  (§9.1(f)).

## K8. Tests §7 — HOLDS in form; FAILS on the rows the reaper's real data needs

Holds:
- One parameterised table per behaviour.
- AT/BEYOND for MAX_WAIT_SECONDS (W-seq-AT/-BEYOND) and for the reaper limit (R-AT/R-BEYOND).
- The adversarial battery on the command text: magnitude (W-seq-100000, the 1 MB perf row), nesting (W-deep), encoding
  (W-unicode, W-crlf) and empty (W-empty).
- No real kill; the lister and the stop are thin seams (:394).
- A pure `select(...)`.
- A new file `tools/test_wait_reaper.py` for a new forge tool is the stated case of docs/TESTING.md «Бюджет / Файлы»
  (:171-172), one table.

Missing (add in this round):
- R-old-loop with the real wrapper command line and a YOUNG sleep child (K3-a). Today's fixture hides the defect.
- R-nearest / R-no-session (F-R2), R-orphan-reuse (F-R3), the two-session lock row (F-R4), R-unwrap-unknown (F-R1) and
  the S0 report rows (F-R8).
- The clock AT row (3600), MAX_LOOP_DEPTH AT (64), and the G-1 and G-2 rows.

Volume: tests are likely to outweigh product lines (≈ 45 gate rows + ≈ 25 reaper rows). The builder names the reason in
its report and in `tests-over:` (docs/TESTING.md :157-159); the plan cannot pre-judge it. No finding against the plan.

## K9. Paperwork §8 — FAILS on the axis block's form; the rest holds

- **(a)** True, but the cost of the SubagentStop launch rests on a "spawned, never awaited" claim that F-R2's in-process
  walk keeps true. Add «the session walk is in-process, milliseconds».
- **(b)** Count: `docs/SIBLING_MAP.md` has **38 axes** (headings up to `## Axis 38`, :644). The block covers 1-38 in
  content. But `tools/mechanism_gate.py:402` checks `axis\s+{n}\s*:` per axis NUMBER. The lines "axis 23–30 (…): n/a" and
  "axis 35–38 (…): n/a" close none of axes 23-30 or 35-38. The commit-msg gate will refuse.
  - Labels are compared with the heading's short key (`mechanism_gate.py:34-50`; "there is NO door for a wrong label").
    "axis 1 (policy ↔ role files ↔ journal)" uses `↔`, while the heading (:24) reads `Policy <-> role files <-> journal`.
    It risks refusal.
  - Fix: one line per axis, 38 lines, each label copied from the map heading up to its first colon. The Lead pre-checks
    the drafted message with the commit-msg gate before committing.
- **(c)** Check 27 exists (`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:814`). Item (e) is new text. `permission_audit
  --summary` exists (`tools/permission_audit.py:587`). Remove "`unfed stdin`" from (e) (G2 dropped) and add the S0
  reports and the `unwrap_failed` / `no-session` counters. **Holds after the edit.**
- **(d)** True: hooks plus a git hook on the path; the handoff report is discipline, detected by the next WAITS line.
- **Enforcement-file rule.** Holds:
  - K-GATE hands over `hygiene_gate_next.py`;
  - K-WIRE hands over `session_context_next.py`, `dod_gate_next.py` and `post-merge.next`;
  - `wait_reaper.py` is inert until a trigger calls it.
- **The `HYGIENE_GATE_PATH` seam is safe ONLY if the environment read lives in the TEST files.**
  - Safe today: the live hook is `python tools/hygiene_gate.py` (`.claude/settings.json:39`) and never reads the
    variable. `journal_write.py:624` does `import hygiene_gate` from `sys.path`.
  - Unsafe if the builder puts the read into `permission_audit.py` (owned by K-GATE) or into the gate itself: then a
    production import obeys an environment variable.
  - Fix: add to K-GATE and K-WIRE non-goals: «the `*_PATH` environment read lives only in the test modules (module-level
    loader in `tools/test_hygiene_gate.py`, `tools/test_permission_audit.py`, `tools/test_session_context.py`,
    `tools/test_dod_gate.py`); no product module reads `HYGIENE_GATE_PATH`, `SESSION_CONTEXT_PATH` or `DOD_GATE_PATH`.»
    Acceptance check: `grep -rn "HYGIENE_GATE_PATH\|SESSION_CONTEXT_PATH\|DOD_GATE_PATH" tools/ --include=*.py` shows
    only `test_*.py`.
  - Also: after placing, the Lead deletes the `*_next.py` / `post-merge.next` files in the same commit (a second copy of
    a live gate is a duplicate). The copy test (`test_permission_audit.py:730-738`) copies the file the seam names.

## K10. Cards §10 — owns disjoint, order right; K-REAP not executable as written

- **Owns.** K-GATE {hygiene_gate_next, test_hygiene_gate, permission_audit, test_permission_audit} · K-REAP {wait_reaper.py,
  wait-reaper.json, test_wait_reaper.py} · K-WIRE {session_context_next, dod_gate_next, post-merge.next,
  test_session_context, test_dod_gate, session-handoff SKILL.md} · K-DOC {RUNBOOK, WEEKLY_CALIBRATION_PROTOCOL,
  SIBLING_MAP}. Disjoint. **Holds.**
- **Order.** K-GATE → place → K-REAP → K-WIRE + K-DOC. **Holds.** F-R0 (the Lead's PowerShell measurement) goes before
  K-REAP.
- **K-REAP for a weaker model:**
  - not executable as written: the unwrap (K3-a), the session identity (K3-b) and the orphan rule (K3-c) would have to
    be invented;
  - `launch_background(trigger, session_pid=…)`, which K-WIRE calls (§5.3 :251), is not in K-REAP's card;
  - `worktree_sweep.launch_background` is sweep-specific (`worktree_sweep.py:1225-1240`: it hard-codes
    `tools/worktree_sweep.py` and refuses in a linked worktree). Only `spawn_detached`, the lock and the status helpers
    are reusable.

  Fix: K-REAP `edges:` gains «F-R1…F-R8; the launcher `launch(trigger)` resolves the session in-process (F-R2) and
  spawns through `worktree_sweep.spawn_detached`; it runs from the main checkout's copy (the sweep's
  `repo_context`), and from a linked cwd it still launches the MAIN checkout's tool (the session, not the checkout, is
  the unit)». `given:` gains this review's measurement section and the F-R0 result.
- **The G2 drop: exactly what leaves.**
  - §1: the bullet text "G2 unfed-stdin refusal" (:19-20).
  - §2: E25 is kept but marked "superseded by M1 (stdin `/dev/null`; the wrapper's `< /dev/null`)". M3 is struck.
  - §3.2: whole (:118-143).
  - §3.3: the key `stdin_readers` and `{command}` (:147-148), ", then stdin" (:150), "or an unfed `cat`" (:155), and
    `stdin_reader_forms` (:158-159).
  - §3.4 rows: `cat f`…; `cat`, `cat -`… (11 h); `cat <<'EOF'`…; `python - <<'EOF'`…; `python -` alone; `x || cat`;
    `read -t 5 x` (:183-189).
  - §5.1: S2 (:216) and "or `stdin_reader_forms(...)`" in S3 (:218).
  - §5.2: "S1/S2" → "S1" (:232).
  - §6.1 stdin clause; §6.3 builder phrase clause and the axis-11 "and stdin readers (G2)" / `stdin_reader_forms`.
  - §7.1: DOORS `stdin`, the `MSG_STDIN` constant, key `stdin_readers`, and rows S-cat-bare … S-quoted (:350-366) with
    the run_allowed S-cat-bare entry (:367).
  - §7.2: R-cat-old and R-py-dash-old become S0 `reported` rows (F-R8).
  - §7.3: label `"unfed stdin"` (:404).
  - §8: (b) axis 11 "G1/G2" → "G1", axis 34's F10 clause; (c) "`unfed stdin`".
  - §9: F3 and F10 are marked "dropped by M1".
  - §12: `MSG_STDIN`.
  - K-GATE `edges:`: "§3.4 table, every G1 row".

## K11. The stale session — inside the class; a node, not a design

It is the same class at a different surface. A leftover outlives its owner and is then acted on by a non-owner as if it
were its own:
- here, notifications of long-closed workers, and another session's compact snapshot;
- in this spec, a process.

The surface is the compact-state reader, not the process table, so it does not belong in these cards.

Concrete hole:
- HOOK snapshots are already matched by session id (`tools/session_context.py:2414-2420`, `MATCH_SESSION`).
- The NARRATIVE line names the newest narrative of ANY session: `_compact_block` at `tools/session_context.py:2526-2530`
  takes `max(narratives)` with no session comparison.

Smallest check, proposed as a node (owner: the Lead; files `tools/compact_snapshot.py`, `tools/session_context.py`,
`tools/test_session_context.py`):
1. A narrative snapshot carries its session id in its header (the existing `--source manual --session <id>` door,
   `session_context.py:2391-2393`).
2. On `SessionStart:compact`, `COMPACT NARRATIVE` names only a narrative whose id matches. A newer foreign one prints
   `COMPACT NARRATIVE: newest is another session's (<file>) -- not your state`.

The second half, waking on notifications of workers that are already closed, is covered by the journal's
`accepted`/`closes:` record. One guard is enough there: `journal_write accept` refuses a second `accepted` of a task
already accepted. Check whether it already does before opening that half.

## Standing questions (critic-diff-brief items 5-7, 12; plan gate)

- **TESTS:** K8. The form holds; the missing rows are listed. Volume is judged at the diff.
- **DUPLICATION AND CONSISTENCY:**
  - The new loop grammar grows `hygiene_gate.py`'s private tokenizer. SIBLING_MAP axis 11 (:276-294) says a new gate
    takes its segments from `hooklib.walk`. That move is queued (C1/F-C4), so this is not a finding, but the spec must
    name that G1's grammar moves with that queue item (one line in §3.3).
  - The reaper's wrapper unwrap (F-R1) is a new payload hop: it is the same class as axis 11's indirections (eval, `-c`).
    It must live as the data row `wrapper_forms` and be added to the axis-11 line, never coded twice.
  - Lock, status and spawn are reused from worktree_sweep by import. **Holds.**
  - grep: `taskkill|os\.kill|killpg|Win32_Process|Get-CimInstance` in tools (journal_write :615, test_redundancy :72 —
    neither is a lister to reuse).
- **CODE QUALITY:** n/a on a plan.
- **ONE ROAD:** the PowerShell side of the reaper is uncovered until F-R0. S1 cannot exist there (Start-Sleep runs inside
  powershell.exe) and S3 has no measured wrapper. That is a fix of this round (F-R0 plus a PowerShell `wrapper_forms`
  row), not a silent exclusion. POSIX report-only (F-R7) is a declared safe default with its measurement as the way out.
  G1 covers both shells by capability rows. **Holds.**

## Trail

Read:
- the spec, all 649 lines;
- `.claude/settings.json:1-140`, `.githooks/post-merge`;
- `tools/hygiene_gate.py:1-40`, `:1495-1605`;
- `tools/worktree_sweep.py:1185-1240`, `tools/journal_write.py:603-640`, `tools/session_context.py:1885-1935`,
  `:2381-2440`, `:2508-2534`, `tools/dod_gate.py:735-812`;
- `docs/RUNBOOK.md:237-254`, `:290-410`;
- `docs/tasks/specs/20261117-no-briefs-fold-into-roles-spec.md:185`, `:225-246`, `:685-686`;
- `docs/TESTING.md:155-186`, `docs/tasks/critic-diff-brief.md:39-115`;
- `docs/SIBLING_MAP.md` axis headings and `:276-296`;
- `tools/mechanism_gate.py:24-60`, `:402`;
- `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:814`;
- transcript `8781f497-…jsonl:2264`;
- `tools/critic_verdict.schema.json`.

Process listings: three read-only `Get-CimInstance Win32_Process` reads (my own ancestry; the `claude.exe` set; the
children of session 26860; `-NoExit` and old python/bash/sleep), plus one read of my own wrapper's command line. Nothing
was killed or started beyond those reads.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "K3-a: the reaper's selection cannot catch the measured forms. Age is taken on the leaf (a sleep child is at most 20 s old), and S3 cannot see a loop inside the harness wrapper's single-quoted eval argument, which the gate masks. Fix F-R1 (tree root age + wrapper_forms data row) and F-R0 (measure the PowerShell wrapper)",
    "K3-b: 'this session' cannot be found from the detached reaper's ancestry (spawn_detached breaks away; the hook dies first). Section 5.1 rule 2 counts every child of a process named claude.exe, and the app is claude.exe. Fix F-R2 (the launcher resolves the nearest claude.exe in-process and passes pid + creation time)",
    "K3-c: Windows does not re-parent orphans, so a reused parent pid adopts a long orphan into this session's tree. Fix F-R3 (a parent counts only if created before the child)",
    "K5: the 11 h class is neither refused nor stopped as decided. The Lead line 645 is false: the selection needs a shape. Fix F-R8 (S0 report with full command and live children)"
  ],
  "fixes": [
    "G-1: state that for/foreach/ForEach-Object loops are refused only on a literal budget over MAX_WAIT_SECONDS (a word list counts; glob/$(...)/variable means unknown, pass); never refused as not capped. Add the list-loop and glob rows",
    "G-2: a C2/C3 cap binds only alone or joined by && (while, -and) / || (until, -or), with the comparator in the loop's sense; otherwise refused. Add the || and direction-mismatch rows",
    "G-3: K-DOC rewrites RUNBOOK 9.1(f) lines 237-239 to the capped form or Monitor; correct the false negative in section 6.2",
    "G-4: add rows for the Monitor tool in 3.4 and 5.2 (the gate does not see it; the reaper treats it by age and shape); name Monitor in the door text. Add the brace-group, clock-AT 3600 and MAX_LOOP_DEPTH-AT rows",
    "F-R0: before K-REAP the Lead measures the cmd.exe and powershell.exe command lines of one background PowerShell call; fill wrapper_forms; until then PowerShell roots are only reported",
    "F-R1: replace 5.1 rules 1-3 with a tool-call tree: root = direct child of this session claude.exe in tool_call_roots; root age over the limit; S1 sleep anywhere in the tree, or S3 the decoded user command gives wait_loop_forms; unwrap_failed logged and counted",
    "F-R2: the launcher in wait_reaper.py walks in-process (ctypes Toolhelp32 + GetProcessTimes; POSIX /proc or ps) to the nearest claude.exe and passes --session-pid and --session-created; not found means no stop, status no-session, door in WAITS. Update F8 and 5.3 accordingly",
    "F-R3: a parent link counts only when the parent was created before the child, on every hop",
    "F-R4: lock and status per session under wait-reaper/<pid>-<created>/; one shared run.log carrying the session pid; same-session busy exits busy",
    "F-R5: stop the root tree in one move (taskkill /PID root /T /F with CREATE_NO_WINDOW after re-reading the creation time; POSIX root-first, then SIGKILL after 2 s), not leaves first",
    "F-R6: never_reap gains worktree_sweep.py and story_step.py; gh matched as a whole process name, not a substring",
    "F-R7: POSIX runs report-only until the POSIX session process name is measured; R-posix expects reported",
    "F-R8: S0, an unshaped tree over the limit, is reported, never stopped. The log records the decoded command up to 2000 ASCII and every live descendant. Drop S2 and stdin_reader_forms; turn R-cat-old and R-py-dash-old into S0 rows; correct decision line 645",
    "K4: kill from day one for S1/S3 only after a live selection witness in the K-WIRE acceptance: a planted background capped loop, a dry list with --limit 60 showing exactly that tree, then --apply",
    "K6: the session walk is in-process, never a powershell/wmic child on the hook path (K-REAP edges); journal_write.py 615/631 and test_redundancy.py 72 get CREATE_NO_WINDOW in their own small node",
    "K7: delete the stdin clause from 6.1 (271-273) and from the 6.3 builder phrase; reword 276-277 for shapes plus S0 reports",
    "K8: add rows R-old-loop with the real wrapper command line and a young sleep, R-nearest, R-no-session, R-orphan-reuse, the two-session lock row, R-unwrap-unknown, S0 report rows, clock AT and depth AT",
    "K9: the axis block becomes 38 single lines with labels copied from the map headings (no ranges, no arrows); the Lead pre-checks it against the commit-msg gate; remove unfed stdin from check 27(e) and add the S0/unwrap_failed/no-session counters; the *_PATH environment reads live only in test modules (grep in acceptance); the *_next files are deleted when placed",
    "K10: the K-REAP card gains F-R1..F-R8 in edges, the launcher function and the main-checkout rule, and this review's measurements in given; apply the exact G2 removal list in K10 of this review",
    "K11: propose a node (Lead) where a narrative compact snapshot carries its session id and SessionStart:compact names only a matching narrative (session_context.py 2526-2530 has no session check today)",
    "DUP: section 3.3 names that the G1 grammar moves with the queued axis-11 item (C1/F-C4); wrapper_forms is added to the axis-11 line"
  ],
  "class_completeness": "SIBLING_MAP has 38 axes. Axis 11: the new grammar and the wrapper unwrap are shell-command recognizers; the move is queued, the spec must name it. Axis 34 one road: the PowerShell reaper side needs F-R0. Sweep of the same artifact: RUNBOOK section 9 neighbours walked; 9.1(f) at 237-239 was missed by the spec (G-3); 9.4 and 9.5 not applicable (the driver's own process); 9.9 applied by the spec. The K11 stale-session class is a sibling at the compact-state surface: a proposed node",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-bounded-waits-mechanism-spec.md:1-649",
      ".claude/settings.json:1-140",
      ".githooks/post-merge",
      "tools/hygiene_gate.py:1-40,1495-1605",
      "tools/worktree_sweep.py:1185-1240",
      "tools/journal_write.py:603-640",
      "tools/session_context.py:1885-1935,2381-2440,2508-2534",
      "tools/dod_gate.py:735-812",
      "docs/RUNBOOK.md:237-254,290-410",
      "docs/tasks/specs/20261117-no-briefs-fold-into-roles-spec.md:185,225-246,685-686",
      "docs/TESTING.md:155-186",
      "docs/tasks/critic-diff-brief.md:39-115",
      "docs/SIBLING_MAP.md axis headings,276-296",
      "tools/mechanism_gate.py:24-60,402",
      "PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:814",
      "transcript 8781f497 line 2264"
    ],
    "reruns": [
      {"command": "powershell Get-CimInstance Win32_Process ancestry of own Bash call", "result": "powershell <- bash x3 <- claude.exe 26860 (session, since 14.11 15:57) <- claude.exe 17100 (the app, WindowsApps Claude.exe) <- explorer"},
      {"command": "powershell Get-CimInstance: NoExit shells and children of session 26860", "result": "NoExit powershell 8900 and 10312 have parent 11816, an app helper claude.exe; session children are conhost plus bash tool-call roots"},
      {"command": "powershell read of own wrapper bash CommandLine", "result": "bash.exe -c \"source snapshot ... && eval '<user command, single-quote spliced>' < /dev/null && pwd -P >| ...\": the user loop sits inside eval quotes"},
      {"command": "grep taskkill|os.kill|killpg|Win32_Process|Get-CimInstance|tasklist in tools/*.py", "result": "journal_write.py:615,617; test_redundancy.py:72,76 (E18 negative fails); control CREATE_NO_WINDOW finds worktree_sweep.py:1215"},
      {"command": "grep until/while/sleep wait-loop forms in docs plans .claude PROCESS CLAUDE.md BOOT.md", "result": "RUNBOOK.md:395 (control) and builder-rules.md:102 anti-examples; separately RUNBOOK.md:237 teaches an until loop (section 6.2 negative fails)"}
    ]
  }
}
```
