# Bounded waits: the gate and the reaper (t-1122, F19) — DRAFT

Designer draft for the Lead. Forks are returned (§9), never decided here. The owner's word, 17.11.2026, with the
Background-tasks screenshot (waits 11 h, 10 h, 8 h, 7.5 h, 1.5 h): «У нас постоянно остаются зависшие процессы. Придумай
механизм что бы такого больше не было». The Lead's addition (same day): a second measured class, a command that reads
stdin with nothing feeding it (the 11 h entry: `( cd <worktree> && cat > /dev/null; python - <<'PYEOF' … PYEOF )`, three
bash processes, parent = the session shell, started 17.11 01:15), and four `powershell.exe -NoProfile -NoExit` processes of
12–14.11 with another parent that must never be touched.

## §1 Scope, architecture, owners

- Touches `tools/`, `.githooks/`, `docs/RUNBOOK.md`, `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`, `docs/SIBLING_MAP.md`,
  `.claude/skills/session-handoff/SKILL.md`. It touches NO path under `ai-packages/qa-factory/`, so the AR-n naming duty of
  designer rule 1 does not apply (`architecture:` line not demanded by `tools/architecture_gate.py`, which reads package
  commits). The forge analogs it keeps anyway: one recognizer per form (AR-13/AR-15 analog: the reaper reads the gate's own
  pure detector, never a second grammar), closed variety as data rows (AR-1 analog: shells by capability row, process names
  and limits in a data file).
- Owners of the checks this spec adds (P27 vocabulary, for the Lead's own record; no census entry, the census is package-only):
  - G1 unbounded-wait refusal, G2 unfed-stdin refusal: **data** (code judges the shape of a command text; no judgment of
    intent — a capped form is always available, so the refusal never decides what the caller meant).
  - R1 the reaper's selection and stop: **data** (age, ancestry, process name, the gate's own shape verdict on a command
    line). Whether a stuck call was "really" dead is not judged: the age limit is above every legal wait (§3.4), and every
    stop is a log line a tier above reads at calibration (check 27 (e), §6.3).
- Error direction (designer rule 1, a reused function in a more consequential role): the gate's signal walk
  (`_collect_signals`, an advisory feed of `permission_audit` today for these shapes) becomes the selector of a KILL in the
  reaper. It may err ONLY toward "not a wait / keep": an uncertain text is no candidate. Adversarial inputs that must stay
  on the safe side are rows R-K1…R-K9 of §7.2.

## §2 Evidence (item 1) — trail file:line

| # | Fact | Carrier |
|---|---|---|
| E1 | `hygiene_gate.py` is the ONE PreToolUse hook on `Bash|PowerShell` | `.claude/settings.json:33-41` |
| E2 | It refuses exactly three behaviours (cd, journal write, rollback of dirty paths); nothing about loops, sleep or stdin. Grep `sleep|until|while` -i in the file: only Python `while` loops (:181, :279 …), no shell-loop recognizer; positive control = the same grep finds Python `while` | `tools/hygiene_gate.py:1-22`, grep trail §11 |
| E3 | Refusal shape: stdout JSON, exit 0, `permissionDecision: "deny"` + `permissionDecisionReason` = first reason, `additionalContext` = `"Command hygiene: "` + all reasons; never `"allow"` | `tools/hygiene_gate.py:3-7`, `:1526-1532` |
| E4 | Door form: each text ≤ 350 chars, names what is wrong, what is expected, the door (P15/FR-1/FR-2); pinned by a test | `tools/hygiene_gate.py:61-88`; `tools/test_hygiene_gate.py:426-430` |
| E5 | Invariant: "no refusal on a target the gate could not resolve; everything uncertain passes, silently"; `run_allowed` (the `--run` road) alone refuses on doubt | `tools/hygiene_gate.py:27-29`, `:1550-1583` |
| E6 | It reads only `tool_name`, `tool_input.command`, `cwd`, `agent_id`; it does NOT read `run_in_background` today | `tools/hygiene_gate.py:1500-1512`, `:1586-1601` |
| E7 | The harness puts `run_in_background` and `timeout` in `tool_input` of both tools (so the gate CAN see it) | transcript `8781f497-…jsonl:2264` (PowerShell, `"timeout":600000,"run_in_background":true`); `f92520fc-…jsonl:4770` (Bash) |
| E8 | It runs for subagents' calls: the payload of a subagent carries `agent_id` and the gate already branches on it | `tools/hygiene_gate.py:1511-1513` |
| E9 | Quoted text, heredoc bodies and comments are masked before any recognizer; payloads of bash/sh/pwsh/cmd `-c` are NOT read (named residual, data row `payload_classifier: None`) | `:24-25`, `:120-127`, `:1191-1196` |
| E10 | `_collect_signals` is PURE and replayed by `permission_audit.classify_hygiene`; a test pins its key set to six keys | `:31-34`, `:1390-1407`; `tools/permission_audit.py:455-477`; `tools/test_hygiene_gate.py:450` |
| E11 | The file must work ALONE in a folder (no new imports): `gitcmd` optional; a test copies `hygiene_gate.py` beside `permission_audit.py` | `:56-59`; `tools/test_permission_audit.py:730-738` |
| E12 | SessionStart = `python tools/session_context.py` only; it already reads a detached background tool's status (WORKTREES line) and cuts at `MAX_LINES = 25` | `.claude/settings.json:5-14`; `tools/session_context.py:190`, `:1889-1929`, `:2348` |
| E13 | SubagentStop = `python tools/dod_gate.py` only; payload carries `agent_id`, `cwd`; a stop may be BLOCKED (exit 2); on its exit-0 path it calls `journal_hooks.record_returned` (the "stop passed" point) | `.claude/settings.json:107-116`; `tools/dod_gate.py:6-10`, `:739-749`, `:806`; `tools/journal_hooks.py:297-300` |
| E14 | PostToolUse on Bash/PowerShell: `dod_track.py`, `journal_echo.py`, `search_control_gate.py` — none reads process state | `.claude/settings.json:65-87` |
| E15 | After a merge into main the post-merge hook starts the worktree sweep detached; `wave.py merge` merges in the main checkout, so it fires there | `.githooks/post-merge:1-8`; `tools/wave.py:52` (imports `worktree_sweep`) |
| E16 | The ONE place a background process is made, with CREATE_NO_WINDOW and its own group, out of the caller's job: `worktree_sweep.spawn_detached` | `tools/worktree_sweep.py:1209-1222` |
| E17 | Session-handoff is a skill (no hook): `.claude/skills/session-handoff/SKILL.md` | `PROCESS/SESSION_PROTOCOL.md:22` |
| E18 | No tool in `tools/` lists or kills processes today (grep `Win32_Process|CREATE_NO_WINDOW|psutil|Get-CimInstance|tasklist|/proc/`: one hit, the spawn flag in worktree_sweep) | grep trail §11 |
| E19 | `ci_read.py` has no wait of its own (its only "waiting" is a status word) | `tools/ci_read.py:177` |
| E20 | A legit background CI wait seen in a transcript: `gh run watch <id> --interval 60 --exit-status` — a command with its own end, not a loop | `1624cb4a-…jsonl:4050` |
| E21 | The night driver is started with `Start-Process` as a separate process (`python … story_run.py …`), logs to `runs/<name>-N.log` | `docs/RUNBOOK.md:300-308` |
| E22 | Rule today, discipline only: RUNBOOK §9.8 (:393-401) and builder-rules 13 (:100-102); the manual after-merge kill duty: RUNBOOK §9.9 (:403-409) | carriers named |
| E23 | `sleep infinity`, `tail -f`, `Wait-Process`, `Wait-Job`: no use in `tools/` and none in `ai-packages/qa-factory/` (case-insensitive); positive control of the same form: `time\.sleep` in the package scripts = 138 hits | grep trail §11 |
| E24 | Foreground calls carry a per-call `timeout` (E7: 600000 ms seen); background calls live past it: the screenshot ages 1.5–11 h. Default/maximum of the timeout: estimate, not verified in this repo (harness tool schema) | E7 + the owner's screenshot |
| E25 | Stdin of a background Bash call is NOT closed here: the 11 h `cat` (no file, no pipe, no here-doc) blocked — measured by the Lead (Win32_Process). Whether the harness wrapper redirects stdin at all, and whether a foreground call behaves the same: not measured (M1) | the Lead's measurement, 17.11 |
| E26 | The loop/stdin processes' parent pid is the SESSION shell, never the launching subagent (Lead's measurement): a process cannot be attributed to a worker by ancestry | the Lead's measurement, 17.11 |
| E27 | Noticed analog: the harness knows an env ceiling for background waits in print mode (`CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0`); no interactive analog found | `plans/MEASUREMENTS.md:135` |

Measurements the cards need before code (command hygiene pt.6a: one experiment first), all by the Lead with a CAPPED
foreground call (never a hanging one):
- **M1** — the full ancestry of ONE live background Bash call and ONE live background PowerShell call
  (`Get-CimInstance Win32_Process` → `ProcessId, ParentProcessId, Name, CreationDate, CommandLine` up to the root): which
  ancestor is "the session shell", what its parent is (name), whether any ancestor's command line names the project path or
  `.claude/shell-snapshots`, and whether the wrapper redirects stdin (`< /dev/null`). Settles F8 and the stdin cure (F3).
- **M2** — after the first reaper stop (or today's hand `Stop-Process`, if the Lead still has the list): does the
  Background-tasks entry turn to finished/failed by itself, or stay "running"? Settles §4.
- **M3** — `python -` and `Get-Content` with no path in a background PowerShell call capped by `timeout`-equivalent
  (`Start-Job … | Wait-Job -Timeout 20`): block, fail, or prompt? Settles F10.

## §3 The gate (item 2)

### §3.1 G1 — unbounded wait loop

**Recognized loop** (from the masked text — quotes, heredoc bodies, comments blanked, E9 — so only a loop the shell
itself will run is seen):
- Bash: a statement starting (after the existing start words `then|do|else|elif|!|time|command|builtin`) with the keyword
  `while` or `until`, its condition = the statements up to the matching `do`, its body = up to the matching `done`
  (one keyword stack over the statement list; `for`/`select` push too, so `done` matches correctly). Bash keywords are
  case-sensitive (`Until` is a command name, not a keyword → no loop).
- PowerShell (case-insensitive): `while (<cond>) { <body> }`, `do { <body> } while (<cond>)`, `do { <body> } until (<cond>)`
  — condition = the parenthesised group, body = the brace group (one brace stack).
- **Sleep verbs** (data row per shell capability `sleep_verbs`): Bash `sleep`; PowerShell `Start-Sleep`, its alias `sleep`,
  `[Threading.Thread]::Sleep(` / `[System.Threading.Thread]::Sleep(`. A loop is a WAIT when a sleep verb stands at a
  statement start anywhere in its subtree (condition or body, nested loops included: `while sleep 5; do …; done` is a wait).

**Capped** — a CLOSED grammar; a wait loop is capped iff one holds:

| id | form | budget (total seconds) |
|---|---|---|
| C1 | it is a counted loop: Bash `for v in $(seq [A [STEP]] N)`, `for v in {A..N[..STEP]}`, `for ((i=A; i<N; i++))` (also `<=`); PowerShell `for ($i=A; $i -lt N; $i++)` (`-le`), `foreach ($i in A..N)`, `A..N | ForEach-Object {…}` / `| % {…}` | count × sleep |
| C2 | a `while`/`until` whose CONDITION holds a clock: Bash `$SECONDS` / `${SECONDS}` or `$(date +%s)`; PowerShell `Get-Date`, `[DateTime]::Now`/`UtcNow`, `.Elapsed` | the literal integer the clock is compared with (`-lt 600`, `< 600`, `-ge 600`), else unknown |
| C3 | a `while`/`until` whose CONDITION compares a variable `v` with a literal integer N (`[ $v -lt N ]`, `[[ $v -ge N ]]`, `(( v < N ))`; PS `$v -lt N`) AND whose body increments the same `v` (`v=$((v+1))`, `((v++))`, `((v+=1))`, `let v++`; PS `$v++`, `$v += 1`) | N × sleep |
| C4 | `while read …` / `until read …` (Bash; the condition's first command is `read`): bounded by its input | none (not a wait) |

**Budget**: when both the count and the sleep are literal, budget = count × sleep, where sleep = the sum of the literal
sleep arguments per iteration (`sleep 20`, `sleep 0.5`, `sleep 1m`/`2h`/`1d`, `sleep 1 2` → 3; PS `-Seconds N`, `-s N`,
`-Milliseconds N`, `-m N`, positional N; `Thread::Sleep(ms)`). A budget over `MAX_WAIT_SECONDS` (data constant, proposed
3600, fork F2) → refused like an unbounded loop ("seq 1 100000" edge, §3.5). A non-literal count, sleep or clock bound
(`$n`, `$end`) → budget unknown → **pass** (E5 invariant: no refusal on what the gate cannot resolve).

**Refused**: a recognized wait loop that is not capped (C1–C4), or capped with a literal budget over MAX_WAIT_SECONDS.

**Foreground too** (recommended, fork F1): the refusal does not read `run_in_background`. Evidence: a foreground call is
bounded by the tool timeout (E24), but a stuck foreground loop still burns up to that timeout per call and the harness's
handling of the children at timeout is not measured; one road for the class (P31) costs nothing extra in grammar.

**Text** (≤ 350 chars, pinned by the test of E4; one per shell by capability row `wait_door`, the same way `cd_door` is):
- Bash: `an unbounded wait loop (while/until with sleep and no cap) outlives a worker that died. Cap it: for i in $(seq 1 30); do <check> && break; sleep 20; done -- at most 3600 s in total -- or check once and come back later.`
- PowerShell: `an unbounded wait loop (while/do with Start-Sleep and no cap) outlives a worker that died. Cap it: for ($i = 0; $i -lt 30; $i++) { if (<check>) { break }; Start-Sleep 20 } -- at most 3600 s in total -- or check once and come back later.`
(The number in the text is formatted from MAX_WAIT_SECONDS, never typed twice.)

**Informed pass: none, and why** (FR-4 asks a check to stop only a silent pass): the door is always usable (FR-2) — any
wait under the maximum is expressible as C1; a wait longer than the maximum is a call that should not exist (split it,
or use a command that ends with its event, e.g. `gh run watch`, E20). A text marker would reopen exactly the leak.

### §3.2 G2 — a stdin read with nothing feeding it

**Recognized reader** (data row `stdin_readers` per shell capability; closed list; proposed minimum, breadth fork F3):

| command | reads stdin when |
|---|---|
| `cat` | no non-option operand, or an operand `-` |
| python (the existing `PAYLOAD_INTERPRETERS` python row, reused) | args are `-` with no here-doc, or no script, no `-c`, no `-m` |
| `read` (Bash builtin) | always — except as the condition of a `while`/`until` (C4) |

**Fed** — a reader statement is fed (→ silent) iff ANY of: (a) it carries an input redirect `<`, `<<`, `<<-`, `<<<`, `<&`
(the tokenizer already yields `_Redir` for these, `tools/hygiene_gate.py:419`); (b) it is not the first command of its
pipeline — the separator before it is a single `|` (not `||`); (c) an enclosing `( … )` / `{ …; }` group or loop is fed by
(a)/(b) at its own boundary (`cmd | ( cat )`, `( cat ) < f`, `while …; do cat; done < f`). An enclosing group whose
boundary cannot be matched (unbalanced) → **pass**.

**Refused**: a recognized reader that is not fed, foreground or background (one road; foreground: same reasoning as F1).
Text (Bash, ≤ 350): `` `cat`/`python -`/`read` here reads stdin and nothing feeds it: in the background it waits forever. Give it input: a file argument, a here-doc (<<'EOF'), a pipe, or < /dev/null. ``
PowerShell row: empty until M3 (fork F10, the one-road option recommended).

**Informed pass: none** — `< /dev/null` (or a file) is always usable.

**The harness cure instead?** Closing stdin for every call is a harness change (non-goal of the brief). A PreToolUse
rewrite (`updatedInput` appending `< /dev/null`) would need `permissionDecision: "allow"`, which the gate never emits by its
own invariant (E3: "allow" would auto-approve what the operator's prompt should see). So the gate refuses with a door.
M1 tells whether the wrapper already redirects stdin; if it does, the 11 h `cat` had another cause and G2 is re-judged.

### §3.3 Placement and positional invariants (CLAUDE.md rule 11 (ii))

- G1/G2 are FORMS collected by `_collect_signals` (new keys `wait_loops`, `stdin_readers`: lists of
  `{shell, form, cap, budget, door}` and `{command}`), decided in `_decide_command` AFTER the existing three classes and
  appended to `deny` (the first reason stays the first refusal found in the existing order: journal, worker-verdict,
  rollback, cd, then wait, then stdin). Invariant: adding G1/G2 never removes or reorders an existing refusal and never
  turns an existing refusal into a pass (an existing test row `test_order_when_several_fire`, :381, keeps its verdict).
- `_collect_signals` stays PURE (no clock, no filesystem; the existing purity test :442-453 holds) and the file stays
  importable alone (E11): the grammar lives in `hygiene_gate.py` itself; no import of `hooklib` or of a new module.
- `run_allowed` (the `--run` road of `journal_write accept`) inherits G1/G2 through `_decide_command` unchanged: an
  unbounded loop or an unfed `cat` in a `--run` command is refused there too (the right direction for an unhooked run).
- Linear time: one pass for the keyword stack, one for the brace stack; nesting past `MAX_LOOP_DEPTH` (data constant,
  proposed 64) → no G1 verdict for that command (pass), like `MAX_HEREDOC_OPENERS`.
- Public pure entry points for the reaper (one road, AR-13 analog): `wait_loop_forms(command, tool_name) -> list` and
  `stdin_reader_forms(command, tool_name) -> list`, each a view of `_collect_signals`.

### §3.4 Edges G1/G2 — behaviour and the invariant it protects

| edge | behaviour | invariant |
|---|---|---|
| a loop in a quoted string (`echo "until x; do sleep 1; done"`), a heredoc body (`cat > w.sh <<'EOF' … EOF`), a comment, `grep -n while f`, `git log --until=…` | pass | text that the shell does not run as a loop is never refused |
| a loop in a script file (`bash wait.sh`) | pass (invisible) | the gate never reads files; the reaper is the net (§5) |
| a loop inside `bash -c "…"` / `powershell -Command "…"` | pass — named residual (E9 row `payload_classifier: None`) | the payload residual stays one rule for all classes (fork F5) |
| `while read line; do …; sleep 1; done < f` / `cmd | while read …` | pass (C4) | a loop bounded by its input is no wait |
| `while true; do <check> && break; sleep 5; done` | refuse (no cap; `break` is no bound) | a wait whose end depends on an outside event is capped |
| `for i in $(seq 1 100000); do …; sleep 20; done` | refuse (budget 2 000 000 s > 3600) | a cap is a cap only below the maximum |
| `for i in $(seq 1 $n)`, `sleep $t`, `[ $SECONDS -lt $end ]` | pass (budget unknown) | no refusal on an unresolved value (E5); the reaper covers the residual |
| `until [ $i -ge 30 ] || grep -q X f; do i=$((i+1)); sleep 20; done` | pass (C3, budget 600) | a hand-written counter is a cap |
| the same with the increment of another variable | refuse | C3 needs the SAME variable |
| `sleep 30` alone (no loop) | pass | a single sleep is bounded by itself |
| `sleep infinity`, `tail -f f` (no `--pid`, no `timeout N` before it), `Wait-Process` without `-Timeout` | fork F4 (zero uses found, E23) | — |
| `timeout 600 tail -f log` | pass if F4 adopts them | a `timeout <literal ≤ MAX>` wrapper is a cap |
| CRLF line ends, tabs after the keyword, `do`/`done` on their own lines | recognized | the line end never hides a keyword |
| PowerShell `WHILE`, `Start-sleep` | recognized (case-insensitive row) | — |
| Bash `Until` / `WHILE` | pass (not a keyword in Bash) | — |
| empty / whitespace / non-string command | silent (existing, :1597-1599) | — |
| over MAX_LOOP_DEPTH nesting, a 1 MB command | pass for G1, linear (perf test :550 extends) | a pathological input never widens a refusal |
| unbalanced `while … do` without `done` | pass | — |
| `cat f`, `cat $f`, `cat *.md` | pass (operand present, literal or not) | a reader with an operand is fed |
| `cat`, `cat -`, `cat > out` (no input), `( cd x && cat > /dev/null; … )` (the 11 h case) | refuse G2 | an unfed reader is refused |
| `cat <<'EOF' … EOF`, `echo x | cat`, `cat < f`, `( cat ) < f`, `cat <<< "$x"` | pass | a fed reader is silent |
| `python - <<'EOF' … EOF`, `python -c "…"`, `python x.py`, `python -m pytest` | pass | — |
| `python -` alone, `python` alone | refuse G2 | — |
| `x || cat` | refuse (`||` is not a pipe) | — |
| `read -t 5 x` | fork F3 (a timeout makes it bounded; recommended: pass when `-t <literal>`) | — |

## §4 The Background-tasks list (item 4)

Not measured in this repo (estimate, not verified): the harness launched each background call as its own child process
and shows its status; when that process exits — killed included — the harness most likely records the exit and the entry
turns finished/failed. M2 settles it. The coordinator's duty either way, written into §9.8 (§6.1): after a reaper stop line
(or a hand stop), look at the list; an entry still "running" is stopped with `TaskStop <id>` (the id of an old task without
context: the creation time of its `.output` file in the session's `tasks/` folder, RUNBOOK §9.8 :400-401). An entry of
ANOTHER session cannot be stopped from this one (estimate): the reaper reports those (§5.3) and the owner/that session's
coordinator closes them.

## §5 The reaper (item 3)

One tool `tools/wait_reaper.py` + data file `tools/wait-reaper.json`. Not a hook: it is launched detached by triggers and
writes its own log and status (the worktree_sweep pattern, E12/E15/E16).

### §5.1 Selection — by what is observable (the Lead's addition: not "the command line holds `until`" alone)

A process P is a CANDIDATE iff ALL hold:
1. **Age**: now − P.created > `limit_seconds` (data, proposed 7200 = 2 × MAX_WAIT_SECONDS, fork F2). Invariant: the limit is
   above every legal capped wait, so a capped wait is never stopped.
2. **Ancestry**: P descends from a harness tool-call — P or an ancestor is a child of a SESSION SHELL, where a session shell
   is a process whose parent's name is in the data row `harness_process_names` (contents from M1). Which session shells
   count is fork F8 (recommended: only THIS session's, from the launcher's own ancestry).
3. **A stuck shape** — one of the data rows `stuck_shapes`:
   - S1 a `sleep` process (any args) whose parent is a shell (bash/sh) — the wait loop's child;
   - S2 a `cat` process, or a python process whose argv after the interpreter is exactly `-` or empty — the stdin reader;
   - S3 a shell process whose command line, after unwrapping its `-c` / `-Command` argument (at most 3 hops), gives a
     non-empty `hygiene_gate.wait_loop_forms(...)` or `stdin_reader_forms(...)` (the gate's own pure verdict, one road).
     An unwrap that fails → not S3 (keep).
4. **Not exempt** — data row `never_reap` (substring or name match on P and on every ancestor up to the session shell):
   `-NoExit`, `story_run.py`, `run_headless.py`, `docker`, `gh`, `wait_reaper.py`; and never the reaper itself, its own
   ancestors, a session shell, or a harness process.

The STOP target of a candidate is its tool-call tree: from the topmost ancestor below the session shell down (so the loop
bash and its sleep child go together; the session shell survives). Order: leaves first, then up.

### §5.2 Edge invariants of the reaper

| edge | behaviour | invariant |
|---|---|---|
| a wait younger than the limit | kept, not listed | a wait younger than the limit is never stopped |
| a capped wait (C1–C4) older than the limit | kept unless S1/S2 hits (a capped loop older than its maximum budget cannot exist; if it does, its sleep child is S1 — stopped and logged as `capped-overdue`) | the log names every stop, so a wrong one is visible |
| the app's `powershell -NoProfile -NoExit` shells (other parent, 12–14.11) | never a candidate: not descended from a session shell (rule 2) AND `-NoExit` in `never_reap` | a process outside the harness tool-call trees is never touched, whatever its age or name |
| the night driver (`Start-Process python … story_run.py`, E21) and its `claude -p` children | never: `never_reap` row; and no stuck shape | a long process the owner started is never reaped |
| `gh run watch` in the background (E20), a long pytest | never: `gh` row; python with a script is not S2 | a command with its own end is kept |
| docker containers of the stand | never (`docker` row; not harness descendants) | — |
| a wait written by a subagent in a worktree | the same as any other: by age (E26: no attribution to a worker exists) | — |
| a process of another session (the 14.11 pairs) | fork F8; recommended: REPORTED with the manual door, not stopped | never a process outside this project's shells |
| pid reused between the list and the stop | before each stop the pid's creation time is re-read; a mismatch → skip, log `pid-reused` | the reaper never kills a process it did not select |
| the process list cannot be read (PowerShell absent, CIM error, timeout 20 s, `ps` missing) | no stop; status `unreadable: <reason ≤120 ASCII>`; the WAITS line says so with the door; exit 1 | never a silent pass |
| a stop fails (access denied, already gone) | log line `failed: <reason>` / `gone`; status counts it | — |
| two reapers at once | one lock file in `<git common dir>/wait-reaper/` (worktree_sweep's lock pattern); the second exits `busy` | one artifact, one writer |
| Windows | list: `powershell -NoProfile -NonInteractive -Command "Get-CimInstance Win32_Process | Select-Object ProcessId,ParentProcessId,Name,CreationDate,CommandLine | ConvertTo-Json -Compress"` with `creationflags=CREATE_NO_WINDOW` and a 20 s timeout; age from `CreationDate`; stop: `taskkill /PID <pid> /T /F` with CREATE_NO_WINDOW | the owner's "empty windows": EVERY process the tool starts carries CREATE_NO_WINDOW; the tool itself is started by `worktree_sweep.spawn_detached` (E16) |
| POSIX | list: `ps -eo pid=,ppid=,etimes=,comm=,args=` (capability row; a `ps` without `etimes` → `etime` parsed); stop: SIGTERM, then SIGKILL after 2 s | the same selection on both (one road) |
| an empty candidate list | status `finished`, 0 stopped; the WAITS line is silent | — |

### §5.3 Where it runs — what each point can and cannot attribute

| point | how it starts | can attribute | cannot | recommended (fork F6) |
|---|---|---|---|---|
| SessionStart | `session_context.py` calls `wait_reaper.launch_background("session-start", session_pid=…)` (spawn, never waits) and reads the last status into one `WAITS:` line | this session's tree (the hook's own ancestry, M1); the previous run's result | the stopped work's owner (E26) | KILL candidates of this session; REPORT other sessions' |
| SubagentStop | from `dod_gate.py`'s exit-0 path, beside `_record_returned` (:806) — so a BLOCKED stop launches nothing | this session's tree | which worker left it (E26) | KILL (age-based; a blocked stop does not matter since the age rule never touches a live wait) |
| after `wave.py merge` | `.githooks/post-merge` launches it BEFORE the worktree sweep line (a stuck process holding a worktree as cwd blocks its removal on Windows — order helps, no guarantee: named residual, the sweep retries) | this session's tree, if the merging session is the harness's | — | KILL (this is RUNBOOK §9.9's manual duty automated) |
| session-handoff | a step line in the skill: `python -B tools/wait_reaper.py` (no `--apply`) | everything it lists | — | REPORT only (the session ends; the next SessionStart stops) |
| Stop (main_gate) | — | — | — | not used: every main turn is too frequent for a 1–2 s CIM read |

CLI: `python -B tools/wait_reaper.py [--apply] [--other-sessions] [--limit <s>] [--session-pid <pid>]`; without `--apply` a
dry list (each candidate: pid, age, shape, clipped command); `--other-sessions --apply` is the informed manual door for
another session's leftovers. Log: `<git common dir>/wait-reaper/run.log`, one line per stop:
`<ts> <trigger> stopped|failed|gone|pid-reused pid=<n> ppid=<n> age=<s> shape=<S1|S2|S3> name=<n> cmd=<first 160 ASCII>`;
`status.json` = `{state, started, finished, trigger, stopped, failed, reported_other, reason}`.
SessionStart line (silent at zero, ASCII, ≤ 200 chars): `WAITS: last reap <ts> (<trigger>): <n> stopped, <m> failed; <k> stuck calls of other sessions -- python -B tools/wait_reaper.py --other-sessions --apply` / `WAITS: process list unreadable (<reason>) -- python -B tools/wait_reaper.py`.

## §6 Rule text (item 5)

### §6.1 `docs/RUNBOOK.md` §9.8 — replacement (whole section, :393-401)

```
### 9.8. Фоновые ожидания

Ожидание в фоне ограничено (слово владельца 17.11.2026, спека t-1122). `tools/hygiene_gate.py` отказывает команде с циклом
`until`/`while` и `sleep` без предела и команде, которая читает stdin, когда его ничто не кормит (`cat` без файла, `python -`
без here-doc); отказ несёт форму, которую вставить (`for i in $(seq 1 30); do <проверка> && break; sleep 20; done`, всего
не больше 3600 с). Лучше разовая проверка или уведомление harness. Отчёт воркера называет цикл, оставленный позади.
То, что прошло мимо гейта (цикл в файле скрипта или в `bash -c "…"`, воркер убит посреди ожидания), останавливает
`tools/wait_reaper.py` — на старте сессии, после остановки воркера и после слияния: вызовы этой сессии старше 2 ч с
зависшей формой; каждая остановка — строка в его журнале, остаток и дверь — строка `WAITS:` на старте сессии. Чужие
сессии, ночной драйвер, `powershell -NoExit` приложения и контейнеры стенда он не трогает. После остановки посмотреть
список фоновых задач: запись, оставшаяся «running», снимается `TaskStop` (id старой задачи — по времени её файла
`.output` в папке `tasks/` сессии).
```

### §6.2 Neighbours in the same artifact (sweep-the-artifact-first)

- RUNBOOK §9.9 (:403-409, the manual after-merge kill): applied — append one sentence: «Остановку зависших ожиданий после
  слияния делает `wait_reaper.py` (§9.8); этот шаг остаётся для остального: `python`, `docker`, процессы воркеров.»
- RUNBOOK §9.4 table row "процесс умер без выхода" (:322) and §9.5 p. 4: not applicable — they concern the driver's own
  process, which the reaper never touches (§5.2).
- No other §9 subsection names waits (grep `until|Start-Sleep` in RUNBOOK: :395, :406 only, plus two `--until` flags).

### §6.3 Role-file line and other carriers

- `.claude/agents/builder.md` new rule 9 (text owned by spec 20261117-no-briefs-fold-into-roles-spec.md :239-243): its last
  sentence becomes «A background wait names the file it waits for and its end; the gate refuses an unbounded loop and a
  stdin read nothing feeds, with the form to paste in its refusal; a loop you leave running is named in your report (the
  rule: `docs/RUNBOOK.md` §9.8).» — delivered by THAT spec's card (its §4.2 row 13 takes "the home t-1122 names"); this spec
  only gives the phrase. `plans/builder-rules.md` is not touched here (it is being dissolved there).
- `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` check 27: new item (e) (§8 (c)).
- `docs/SIBLING_MAP.md` axis 11: the queued line (:294) gains "wait loops (G1) and stdin readers (G2)" among the gate's own
  recognizers, and "the reaper reads them through `wait_loop_forms`/`stdin_reader_forms`, never a second grammar".

## §7 Tests (docs/TESTING.md: one parameterised table per behaviour; input from outside gets the adversarial battery)

### §7.1 Gate — new rows in the EXISTING table of `tools/test_hygiene_gate.py` (`ROWS`, :308)

Lists `WAITS` and `STDIN` joined into `ROWS`; `DOORS` gains `wait_bash`, `wait_ps`, `stdin`; the 350-char test (:426) gains
the three new constants; the key-set assertion (:450) gains `wait_loops`, `stdin_readers`.

| id | command | tool | expect |
|---|---|---|---|
| W-until-bg | `until grep -q DONE f; do sleep 20; done` | B | deny wait_bash |
| W-while-true-break | `while true; do test -f f && break; sleep 5; done` | B | deny |
| W-while-sleep-cond | `while sleep 5; do x; done` | B | deny |
| W-seq-30 | `for i in $(seq 1 30); do test -f f && break; sleep 20; done` | B | silent (600 s) |
| W-seq-AT | `for i in $(seq 1 180); do …; sleep 20; done` | B | silent (3600 = AT) |
| W-seq-BEYOND | `for i in $(seq 1 181); do …; sleep 20; done` | B | deny |
| W-seq-100000 | `for i in $(seq 1 100000); do x; sleep 20; done` | B | deny |
| W-brace | `for i in {1..30}; do x; sleep 1m; done` | B | silent (1800) |
| W-arith | `for ((i=0;i<30;i++)); do x; sleep 2; done` | B | silent |
| W-seconds | `until test -f f || [ $SECONDS -ge 600 ]; do sleep 10; done` | B | silent |
| W-seconds-BEYOND | `… [ $SECONDS -ge 3601 ] …` | B | deny |
| W-counter | `until [ $i -ge 30 ] || grep -q X f; do i=$((i+1)); sleep 20; done` | B | silent |
| W-counter-other-var | same with `j=$((j+1))` | B | deny |
| W-dynamic | `for i in $(seq 1 $n); do x; sleep $t; done` | B | silent |
| W-while-read | `while read l; do echo "$l"; sleep 1; done < f` | B | silent |
| W-quoted | `echo "until x; do sleep 1; done"` | B | silent |
| W-heredoc | `cat > w.sh <<'EOF'` / `until x; do sleep 1; done` / `EOF` | B | silent |
| W-comment | `ls # until x; do sleep 1; done` | B | silent |
| W-git-until | `git log --until=2026-11-17 -n 3` | B | silent |
| W-bash-c | `bash -c "until x; do sleep 1; done"` | B | silent (residual F5) |
| W-subshell | `( until x; do sleep 1; done ) &` | B | deny |
| W-after-and | `cd_ok && until x; do sleep 1; done` → use `true && until …` | B | deny |
| W-nested | `until x; do for i in $(seq 1 3); do sleep 1; done; done` | B | deny (outer unbounded) |
| W-crlf | `until x\r\ndo sleep 1\r\ndone` | B | deny |
| W-case-bash | `Until x; do sleep 1; done` | B | silent |
| W-unbalanced | `until x; do sleep 1` | B | silent |
| W-single-sleep | `sleep 30` | B | silent |
| W-ps-while | `while (-not (Test-Path f)) { Start-Sleep 20 }` | P | deny wait_ps |
| W-ps-do-until | `do { Start-Sleep -Seconds 5 } until (Test-Path f)` | P | deny |
| W-ps-upper | `WHILE ($true) { start-sleep 1 }` | P | deny |
| W-ps-for | `for ($i=0; $i -lt 30; $i++) { if (Test-Path f) { break }; Start-Sleep 20 }` | P | silent |
| W-ps-getdate | `while ((Get-Date) -lt $end) { Start-Sleep 5 }` | P | silent |
| W-ps-range-BEYOND | `1..1000 | % { Start-Sleep 20 }` | P | deny |
| W-ps-thread | `while ($true) { [Threading.Thread]::Sleep(500) }` | P | deny |
| W-ps-quoted | `Write-Output 'while ($true) { Start-Sleep 1 }'` | P | silent |
| W-unicode | `until grep -q 'готово' f; do sleep 5; done` | B | deny (non-ASCII never hides a keyword) |
| W-empty | `""`, `"   "` | B | silent |
| W-deep | 65 nested `until x; do` … `done` | B | silent (over MAX_LOOP_DEPTH) |
| W-order | `cd x; until y; do sleep 1; done` | B | deny, first reason = cd door |
| S-cat-bare | `cat` | B | deny stdin |
| S-cat-dash | `cat - > out` | B | deny |
| S-11h | `( cd w && cat > /dev/null; python - <<'PYEOF'` / `print(1)` / `PYEOF` / `)` | B | deny |
| S-cat-file | `cat f.txt`, `cat $f`, `cat *.md` | B | silent |
| S-heredoc | `cat > f <<'EOF'` / `x` / `EOF` | B | silent |
| S-herestring | `cat <<< "$x"` | B | silent |
| S-pipe | `echo x | cat` | B | silent |
| S-or | `false || cat` | B | deny |
| S-group-fed | `( cat ) < f`, `echo x | ( cat )` | B | silent |
| S-loop-fed | `while true; do cat; break; done < f` | B | silent for G2 (G1 judges the loop separately) |
| S-py-dash | `python -` | B | deny |
| S-py-bare | `python` | B | deny |
| S-py-heredoc | `python - <<'EOF'` / `print(1)` / `EOF` | B | silent |
| S-py-c / S-py-m | `python -c "print(1)"`, `python -m pytest tools/x.py` | B | silent |
| S-read | `read x` | B | deny |
| S-read-t | `read -t 5 x` | B | per F3 (recommended silent) |
| S-quoted | `echo "cat"` | B | silent |
| run_allowed rows | W-until-bg and S-cat-bare through `run_allowed` (:567 table) | — | (False, reason) |

### §7.2 Reaper — the selection table (fork F9 on the file) over a PURE `select(processes, now, session_pids, rows)` with fixture process lists

| id | fixture | expect |
|---|---|---|
| R-old-loop | bash (session-shell child, 3 h, cmd holds `until … sleep`) + sleep child | both stopped, leaf first |
| R-AT | the same at exactly `limit` | kept (strictly older only) |
| R-BEYOND | `limit + 1` s | stopped |
| R-young | 30 min | kept |
| R-cat-old | `cat` child of a session-shell call, 11 h | stopped (S2) |
| R-py-dash-old / R-py-script-old | `python -` 3 h / `python -m pytest` 3 h | stopped / kept |
| R-K1 NoExit | `powershell -NoProfile -NoExit`, 5 d, other parent | kept |
| R-K2 driver | `python story_run.py …`, 9 h, parent dead | kept |
| R-K3 gh | `gh run watch …`, 3 h, session-shell child | kept |
| R-K4 docker | `docker …`, 30 d | kept |
| R-K5 session shell / harness / self / own ancestors | — | kept |
| R-K6 other session | the same old loop under another session shell | reported, not stopped (F8 rec.) |
| R-K7 pid reused | creation time differs at re-read | skipped, `pid-reused` |
| R-K8 unwrap fails | bash with an unparseable `-c` and no sleep/cat child | kept |
| R-K9 capped old | bash with `for i in $(seq 1 30)`, 3 h, sleep child | stopped and logged `capped-overdue` (S1) |
| R-unreadable | the lister raises / times out / returns non-JSON | no stop, status `unreadable`, exit 1 |
| R-empty | an empty list | `finished`, 0 |
| R-posix | the same R-old-loop fixture in `ps` form (`etimes`, and `etime` `1-02:03:04`) | stopped |
| R-CIM-date | `CreationDate` with offset `+180` and `-300` | the same age |
| R-cmd-adversarial | a command line 64 KB, with NUL, non-ASCII, quotes nested 4 deep | no crash; S3 off past 3 unwraps |

The stop itself and the lister are thin seams (one subprocess call each) replaced in the table; no real process is killed
by a test.

### §7.3 Wiring

- `tools/test_session_context.py`: rows beside the worktrees ones (:2151-2260): WAITS silent at zero; stopped/failed/other
  counts; unreadable status with the door; the line survives the MAX_LINES cut like WORKTREES (:2253); a failing launch is
  one line, never a dead hook.
- `tools/test_dod_gate.py`: a passing stop calls the launcher once; a blocked stop does not; a launcher that raises never
  changes exit code or message.
- `tools/test_permission_audit.py:374`: labels gain `"unbounded wait"`, `"unfed stdin"`.

## §8 Mechanism paperwork (item 6) — for the Lead's commit

### (a) What compliance costs and who pays
Writers pay one refusal per unbounded form, with the replacement text in it (≈ one extra tool call); the gate's cost is a
linear pass more per Bash/PowerShell call (µs–ms; perf test). The reaper costs a 1–2 s detached CIM read at SessionStart,
each passing SubagentStop and each merge, off the critical path (spawned, never awaited). The coordinator pays one glance at
the Background-tasks list after a stop line.

### (b) Axes — one block for both mechanisms (G = the gate classes G1/G2, R = the reaper)
- axis 1 (policy ↔ role files ↔ journal): covered — RUNBOOK §9.8 text, builder.md rule 9 phrase via the no-briefs spec; no journal event added (the reaper's log is its own carrier).
- axis 2 (exam instruments): n/a — no tier exam measures shell waits.
- axis 3 (package ↔ release copy ↔ plugin): n/a — no package path; the kit copy of `hygiene_gate.py` (`install_parity_anchors.json:559-563`, kind `path`, no anchors) is presence-only: unchanged.
- axis 4 (factory rules ↔ debt ↔ backlog ↔ principles): n/a — no FR changes; the owner's word is cited.
- axis 5 (stage twins): n/a — no package stage.
- axis 6 (measurers ↔ package): n/a.
- axis 7 (test identity ↔ scopes): n/a — no test-identity logic.
- axis 8 (story on disk): n/a.
- axis 9 ("is this a test file"): n/a.
- axis 10 (git-top readers): R — the reaper finds `<git common dir>` through the same reader worktree_sweep uses (`repo_context`), not its own `git rev-parse`: covered in card K-REAP.
- axis 11 (shell-command recognizers): G/R — covered by §3.3 (grammar only in hygiene_gate.py's own walker, public views for the reaper) and the axis-11 line (§6.3); the move onto `hooklib.walk` stays queued (C1/F-C4) — queued.
- axis 12 (carriers of the work plan): n/a — the cards live in this spec; the Lead places them in a pile node.
- axis 13 (the dispatch text): n/a.
- axis 14 (transcript readers): n/a — the reaper reads processes, not transcripts.
- axis 15 (console stream setup): R — `wait_reaper.py` prints ASCII and sets its stream like worktree_sweep (a link of the enforcement chain, no `streams` import): covered in K-REAP.
- axis 16 (one JSON reader of the package): n/a (tools-side; `wait-reaper.json` read once, loud on a broken file).
- axis 17 (detector verdict shape): G — the two new refusals use the gate's existing output shape (E3), one reader: covered.
- axis 18 (shrink-only ratchets): covered — any ratchet raise from the new code (lint/dup baselines of `tools/`) is named in the verdict; no raise expected.
- axis 19 (role `tools:` reader): n/a.
- axis 20 (host receipt names): n/a.
- axis 21 (markdown table readers): n/a.
- axis 22 (host return form): n/a.
- axis 23–30 (package row fields, execution record, freshness, waiver word, profiles, row render, jsonl appender, profile commands): n/a — package-only axes; the reaper's `run.log` is a plain text log, not a `.jsonl` carrier (axis 29 n/a for that reason).
- axis 31 (role carriers: one owner per aspect): covered — the rule's one home is RUNBOOK §9.8; builder.md carries one phrase + pointer.
- axis 32 (where judgment lives): covered — §1: both checks are data checks; no role judgment is replaced.
- axis 33 ("which dispatch am I"): n/a — the reaper never attributes to a dispatch (E26).
- axis 34 (one road): covered — one grammar for both shells by capability rows; foreground and background alike (F1); the PowerShell stdin row is a fork (F10), not an exclusion.
- axis 35–38 (story sides, substitute rows, repeat stop, dry census): n/a — package-only.

### (c) Detector — registered
- `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` check 27 gains (e): «UNBOUNDED WAITS: from `permission_audit --summary` the counts
  of `unbounded wait` and `unfed stdin` (refused shapes), and from `<git common dir>/wait-reaper/run.log` every `stopped`
  line of the window — each stop is a leak past the gate: read its `cmd`, name the form (script file, `bash -c`, dynamic cap,
  killed worker) and either add a grammar row or record it as a named residual; a window with no stops is noted explicitly
  — "no reaped waits".» Live detector between calibrations: the SessionStart `WAITS:` line (§5.3).

### (d) What stops it from being skipped
G1/G2: code on the execution path — the PreToolUse hook every Bash/PowerShell call of every session and subagent passes
(E1, E8). R: the triggers are code too — SessionStart hook, SubagentStop hook path, post-merge git hook; only the
session-handoff report is a skill step (discipline; its detector is the next SessionStart line). Promotion basis
(rule 10 (d)): the leak is evidenced — 07.10 (builder-rules 13: eight loops, 23 processes), 16.10 (§9.8: two loops, 3 h),
20.10 (§9.9: eleven pairs), 17.11 (six pairs + the `cat`, the owner's screenshot).

Commit lines: the commit carries the axis block above and `tier: opus` (mechanism_gate lists `tools/hygiene_gate.py` as a
mechanism path, `tools/mechanism_gate.py:239`); no `architecture:`/`judgment:` line — no package path (their grammar's only
carrier is `tools/architecture_gate.py`).

## §9 Forks (returned; recommendation first)

- **F1 — foreground too?** (a) G1/G2 refuse foreground and background alike — **recommended** (one road; foreground is
  bounded only by a timeout whose effect on children is unmeasured); (b) background only (read `run_in_background`, E7) —
  costs a second road and leaves 2–10 min stuck foreground turns.
- **F2 — the limits.** MAX_WAIT_SECONDS = 3600 and reaper limit = 7200 — **recommended** (the 1.5 h screenshot entry would be
  stopped at 2 h; RUNBOOK's example is 600 s); alternatives: 1800/3600 (tighter; a long CI wait must use `gh run watch`), or
  7200/14400.
- **F3 — breadth of G2 and the stdin cure.** (a) the minimum list (`cat`, `python -`/bare, `read` outside a loop condition;
  `read -t N` passes) — **recommended**, extend by data rows after the reaper's log shows other readers; (b) the wide list
  (`sort`, `head`, `tail`, `wc`, `grep PATTERN`, `jq`, `sed`, `awk`, `xargs` with no file operand) — more false-positive
  risk (`grep -q x` alone in a pipeline head is rare but real). If M1 shows the wrapper redirects stdin, G2 is dropped and
  the 11 h case re-measured.
- **F4 — `sleep infinity`, `tail -f`/`-F` without `--pid`, `Wait-Process`/`Wait-Job` without `-Timeout`: same class?**
  (a) yes, refused unless wrapped by `timeout <literal ≤ MAX>` / given `-Timeout` — **recommended** (zero uses in `tools/` and
  the package, E23: no false-positive cost); (b) leave to the reaper.
- **F5 — loops inside `bash -c "…"` / `powershell -Command "…"`.** (a) named residual, the reaper covers — **recommended**
  for this node; the one-hop payload read for ALL classes joins the queued axis-11 move; (b) one hop for G1/G2 only — a
  second rule for payloads (P31 smell).
- **F6 — kill or report, per point.** (a) KILL at SessionStart, SubagentStop, post-merge; REPORT at session-handoff —
  **recommended**; (b) report everywhere for one week (first-run calibration of the selection), then kill; (c) kill at
  SessionStart only.
- **F7 — how the triggers are wired.** (a) calls from the existing hooks (`session_context.py`, `dod_gate.py` exit-0 path,
  `.githooks/post-merge`) — **recommended**: no new `settings.json` entry, so `hook_liveness_probe`'s CASE-MISSING check
  (`tools/hook_liveness_probe.py:29-33`) and `wiring_check` are untouched, and SubagentStop launches only on a passed stop;
  (b) new `settings.json` hook entries `python tools/wait_reaper.py --hook <event>` — needs a probe case and a wiring row,
  and launches on blocked stops too.
- **F8 — which session shells count (rule 2 of §5.1).** (a) only THIS session's (from the launcher's ancestry; other
  sessions' stuck calls are reported with the `--other-sessions --apply` door) — **recommended**, the only form that meets
  "never a process outside this project's shells" without a cwd reader (Windows exposes no process cwd through CIM);
  (b) every session shell of this machine's harness — also kills other projects' sessions' processes; (c) sessions whose
  command line names this repo path — only if M1 shows such a field. Not safe without M1: if M1 cannot identify a session
  shell, the reaper ships REPORT-only (F6 (b)) until it can.
- **F9 — the reaper's test file.** (a) one new file `tools/test_wait_reaper.py` holding ONE parameterised table (§7.2) —
  **recommended**: the tool is new, `tools/` tests are not governed by the package's `test-layers.json` keep rows, and no
  existing file judges process selection; (b) rows in `tools/test_worktree_sweep.py` (the nearest sibling) — mixes two
  tools in one table.
- **F10 — PowerShell stdin row (P31, one road).** (a) measure M3 and fill the PowerShell row in the same card —
  **recommended**; cost: one capped experiment by the Lead; (b) Bash-only rows with the PowerShell side a named residual —
  goes to the owner as an exception, not recommended.
- **F11 — the package analog (another pile's zone).** The factory's roles in target projects run Bash in the background too
  (`guard_pre_tool.py` has no wait check: estimate, not read). Offer a finding to the package-guard pile: «an unbounded
  background wait of a role outlives it» — the Lead decides whether to file it.
- **F12 — a harness knob.** `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS` exists for print mode (E27); whether an interactive
  ceiling exists is unknown. A question for the Lead/owner (host configuration waits for the owner, PROJECT.md); not built.

## §10 Builder cards

Order: K-GATE → (Lead places) → K-REAP → K-WIRE; K-DOC with K-WIRE. Owns are disjoint.

### K-GATE
```
given: this spec §2, §3, §7.1; tools/hygiene_gate.py; tools/test_hygiene_gate.py; tools/permission_audit.py :170-180, :455-477; tools/test_permission_audit.py :370-380, :575-590, :725-740; tools/journal_write.py :620-630 (read only)
owns:
C:/QAFactory/forge-repo/tools/hygiene_gate_next.py
C:/QAFactory/forge-repo/tools/test_hygiene_gate.py
C:/QAFactory/forge-repo/tools/permission_audit.py
C:/QAFactory/forge-repo/tools/test_permission_audit.py
non-goals: no edit of tools/hygiene_gate.py itself (enforcement-file rule: it is live on the hooks path; the full new file is handed as tools/hygiene_gate_next.py and the Lead places it); no change to the three existing refusal classes; no hooklib import; no payload reading of bash/pwsh -c
handoff: report file per builder rule 7
edges: §3.4 table, every row; §3.3 positional invariants (existing order kept, purity, file importable alone)
DoD: `HYGIENE_GATE_PATH=tools/hygiene_gate_next.py python -m pytest tools/test_hygiene_gate.py tools/test_permission_audit.py -q`
siblings: run_allowed (inherits, row added); permission_audit labels (same commit); axis 11 line (K-DOC)
```
Test seam: both test files load the gate under the module name `hygiene_gate` from `HYGIENE_GATE_PATH` when set
(`importlib.util.spec_from_file_location`, inserted into `sys.modules` before `permission_audit` is imported), default
`tools/hygiene_gate.py`. The Lead, after placing the file, re-runs the same command without the variable; that run is the
acceptance witness.

### K-REAP
```
given: this spec §5, §7.2; tools/worktree_sweep.py :1-40, :1100-1240 (lock, status, spawn_detached, repo_context); tools/hygiene_gate.py (placed, public wait_loop_forms/stdin_reader_forms); results of M1 (Lead)
owns:
C:/QAFactory/forge-repo/tools/wait_reaper.py
C:/QAFactory/forge-repo/tools/wait-reaper.json
C:/QAFactory/forge-repo/tools/test_wait_reaper.py
non-goals: no trigger wiring (K-WIRE); no killing in tests; no reading of transcripts; no psutil or other new dependency
handoff: report file per builder rule 7
edges: §5.2 table, every row; the CREATE_NO_WINDOW invariant on every child; the unreadable list never a silent pass
DoD: `python -m pytest tools/test_wait_reaper.py -q`
siblings: worktree_sweep (lock/status/spawn reused by import, not copied); session_context WAITS line (K-WIRE)
```
`wait_reaper.py` is not active until a trigger calls it, so it is written at its real path; the triggers are the
enforcement files (K-WIRE).

### K-WIRE
```
given: this spec §5.3, §7.3; tools/session_context.py :1885-1935, :2340-2360; tools/dod_gate.py :735-810; .githooks/post-merge; tools/test_session_context.py :2151-2260; tools/test_dod_gate.py; .claude/skills/session-handoff/SKILL.md
owns:
C:/QAFactory/forge-repo/tools/session_context_next.py
C:/QAFactory/forge-repo/tools/dod_gate_next.py
C:/QAFactory/forge-repo/tools/post-merge.next
C:/QAFactory/forge-repo/tools/test_session_context.py
C:/QAFactory/forge-repo/tools/test_dod_gate.py
C:/QAFactory/forge-repo/.claude/skills/session-handoff/SKILL.md
non-goals: no edit of the live tools/session_context.py, tools/dod_gate.py, .githooks/post-merge (handed as *_next / post-merge.next; the Lead places them); no settings.json change (F7 (a))
handoff: report file per builder rule 7
edges: a launch failure is one line and never changes a hook's exit code or message; a blocked stop launches nothing; the WAITS line silent at zero and surviving MAX_LINES; post-merge launches the reaper before the sweep and never fails the merge
DoD: `SESSION_CONTEXT_PATH=tools/session_context_next.py DOD_GATE_PATH=tools/dod_gate_next.py python -m pytest tools/test_session_context.py tools/test_dod_gate.py -q`
siblings: worktrees_line (the WAITS line is its twin); hook_liveness_probe (unchanged under F7 (a))
```
(The same load-from-path test seam as K-GATE; the Lead re-runs without the variables after placing.)

### K-DOC (Lead or a small-work batch)
`docs/RUNBOOK.md` §9.8 (§6.1) and §9.9 sentence (§6.2); `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` check 27 (e) (§8 (c));
`docs/SIBLING_MAP.md` axis 11 line (§6.3). Witness: a DOC-DISPATCH key-presence run (CLAUDE.md rule 11) with keys quoted
from §6.1–§6.3 and a negative control.

## §11 Readers of every touched file (designer rule 7)

Greps over `tools/`, `.githooks/`, `.claude/` (`.claude/worktrees/` excluded: other branches' copies). Each empty result
has a positive control of the same form.

| file | grep | hits | readers → verdict |
|---|---|---|---|
| `tools/hygiene_gate.py` | `hygiene_gate` in `tools/` | 101 in 27 files | `permission_audit.py` (imports `_collect_signals`; changes in K-GATE), `test_permission_audit.py` (labels pin :374, gate copy :730; K-GATE), `test_hygiene_gate.py` (K-GATE), `journal_write.py:624-626` (`run_allowed`; unchanged code, wider refusal), `hook_liveness_probe.py:316, :909, :1391-1401` (journal case; unchanged), `mechanism_gate.py:69, :239` (mechanism path; unchanged, commit needs the axis block), `install_parity_anchors.json:559-563` (presence; unchanged), `test_streams.py:227` (stream grouping; unchanged), `claim_control_gate.py`, `search_control_gate.py`, `tier_echo.py`, `negative_lint.py`, `enforcement_probe.py`, `md_regions.py`, `journal_echo.py` (docstring mentions only; unchanged), `warn_layers.json`, `dup-baseline.json` (unchanged unless the dup ratchet moves: axis 18), `test_journal_per_developer.py`, `test_agents_md.py`, `test_warn_messages.py`, `test_p4_stdin_deadline.py`, `test_mechanism_gate.py`, `test_claim_control_gate.py`, `test_search_control_gate.py`, `test_enforcement_probe.py`, `test_hook_liveness_probe.py` (unchanged; the canon judges them) |
| same | `hygiene_gate` in `.githooks/` | 0 (control: `mechanism_gate` → `commit-msg:32`) | — |
| same | `hygiene_gate` in `.claude/agents/` | 0 (control: `witness` → 14 in 3 files) | — |
| same | `hygiene_gate` in `.claude/skills/` | 0 | — |
| `tools/session_context.py` | `worktrees_line|MAX_LINES =` in `tools/` | session_context.py:190, :1889, :2348; test_session_context.py :1490, :2151-2260 | test_session_context.py changes in K-WIRE; hook_liveness_probe imports it (:319, unchanged) |
| `tools/dod_gate.py` | `dod_gate` in `tools/*.py` | 173 in 23 files | test_dod_gate.py (K-WIRE); hook_liveness_probe (16, case unchanged); journal_hooks (record_returned; unchanged); dod_track, main_gate, journal_echo, mechanism_gate, streams, dispatch_gate, handoff_gate, session_context and their tests (mentions; unchanged) |
| `.githooks/post-merge` | `post-merge` in `tools/*.py` | 61 in 10 files | worktree_sweep.py (its caller contract `--post-merge`; unchanged), test_worktree_sweep.py (34; unchanged — the sweep line stays), hook_liveness_probe.py + test (5+5; check whether it pins the hook's text: K-WIRE reads it first and reports), wave.py:1, test_wave.py:1, piles.py, test_piles_close.py, test_session_context.py (6), mechanism_gate.py (unchanged) |
| `tools/wait_reaper.py`, `tools/wait-reaper.json` (new) | `wait_reaper` in `tools/` | 0 (control: `session_context` found in the same folder by the same tool) | readers come only from K-WIRE |
| `docs/RUNBOOK.md` §9.8 | `9\.8|Фоновые ожидания` in `tools/` | 0 (control: `RUNBOOK` grep finds `docs/RUNBOOK.md:393` heading) | no code reads the section; the no-briefs spec :185, :243, :480 points at it (unchanged pointer) |
| `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` check 27 | not grepped by code for item letters | — | session_context reads the calibration date only (unchanged; estimate, not grepped) |
| `.claude/skills/session-handoff/SKILL.md` | `session-handoff/SKILL` in `tools/` | 0 | `r3_integration_check.py` names the skill (unchanged) |
| `docs/SIBLING_MAP.md` | — | — | `tools` reading the map for liveness (check 12): the new path `tools/wait_reaper.py` must exist when the line lands (it lands with K-WIRE) |

## §12 Small choices closed by the designer

- The reaper is a separate tool, not part of `worktree_sweep.py` (different concern), but reuses its lock/status/spawn by
  import (one survivor).
- The gate constants are named `MSG_WAIT_BASH`, `MSG_WAIT_POWERSHELL`, `MSG_STDIN`, `MAX_WAIT_SECONDS`, `MAX_LOOP_DEPTH`;
  the doors hang on the capability rows (`wait_door`), as `cd_door` does.
- Budget arithmetic in floats, compared with `>` (AT the maximum passes).
- Reaper age is strictly greater than the limit (AT the limit kept).
- The log is plain text in `<git common dir>/wait-reaper/` (machine state, not repository content).
- `taskkill /T /F` on Windows for the tree; SIGTERM then SIGKILL after 2 s on POSIX.

## §13 Noticed, not widened

- RUNBOOK §9.9 duty already asks for an after-merge kill of `bash|sh|python|sleep|docker`: the reaper automates only its
  wait part; the rest stays manual (§6.2).
- `plans/MEASUREMENTS.md:135` names a print-mode harness ceiling (F12).
- The package guard likely has the same class (F11).

## §14 Reading trail

Read: `tools/hygiene_gate.py` (whole, 1720 l.), `.claude/settings.json` (whole), `docs/RUNBOOK.md` :300-430,
`plans/builder-rules.md` :36-55, :100-103, `docs/tasks/specs/20261117-no-briefs-fold-into-roles-spec.md` :225-246,
:680-688 (+ grep rows :84-90, :185, :242-243, :480, :685), `tools/worktree_sweep.py` :1-40, :1180-1240,
`tools/session_context.py` :1885-1929, :2570-2660, `tools/dod_gate.py` :1-60, `tools/journal_hooks.py` :270-320,
`.githooks/post-merge`, `tools/test_hygiene_gate.py` :1-105, :426-455, `tools/permission_audit.py` :170-189, :455-484,
`tools/install_parity_anchors.json` :550-579, `tools/hook_liveness_probe.py` :26-37, :300-339, `docs/TESTING.md` :100-144,
`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` :511-540, :814-867, `docs/SIBLING_MAP.md` axis headings + :276-294.
Greps (Grep tool): `run_in_background` in tools (1 fixture hit); transcripts `"name":"(Bash|PowerShell)" … run_in_background":true`
(6 hits, E7/E20); `hygiene_gate` in tools/.githooks/.claude (counts §11); `Win32_Process|CREATE_NO_WINDOW|psutil|Get-CimInstance|tasklist|/proc/`
in tools (1); `sleep|poll|wait` -i in ci_read.py (1); `sleep infinity|tail -f|wait-process|wait-job` -i in tools (0) and
the package (0), control `…|time\.sleep` -i in package scripts (138); `sleep|until|while` -i in hygiene_gate.py (Python
loops only); `sleep|poll|until` in test_hygiene_gate.py (0; control: the file's own `ROWS`/`parametrize` grep hit);
`settings\.json` in tools (175 in 30 files); `dod_gate` (173/23); `post-merge` (61/10); `worktrees_line|MAX_LINES =`;
`"returned"` in dod_gate/journal_hooks; `wait_reaper` (0); `9\.8|Фоновые ожидания` in tools (0).
Not run: no shell in this role — M1–M3 are the Lead's measurements; the harness tool timeout default is an estimate.
Needed beyond the manifest: `tools/worktree_sweep.py`, `tools/session_context.py`, `tools/dod_gate.py`,
`tools/journal_hooks.py`, `.githooks/post-merge`, `tools/permission_audit.py`, `tools/test_hygiene_gate.py`,
`tools/hook_liveness_probe.py`, `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`, `docs/SIBLING_MAP.md`, `docs/TESTING.md`, transcripts.

## Lead measurements and decisions (architect-rank session, 17.11.2026)

Measurements (this session, Windows, harness claude-code 2.1.321):
- M1 stdin: in a FOREGROUND and in a BACKGROUND Bash call `readlink /proc/self/fd/0` prints `/dev/null`, `[ -t 0 ]` is false,
  and `timeout 3 cat > /dev/null` returns 0 at once (EOF). So today a stdin reader does NOT block. The 11 h call
  (`( cd <tree> && cat > /dev/null; python - <<'PYEOF' … )`, started 01:15) therefore hung for another reason, which is NOT
  established (the processes are stopped; nothing left to measure).
- M1 ancestry: a PowerShell call is `powershell.exe <- cmd.exe <- claude.exe (the session) <- Claude.exe (the app) <- explorer`;
  the stale bash calls had the same `claude.exe` pid as direct parent. `harness_process_names` = `claude.exe`; "this
  session" = the `claude.exe` whose descendant the reaper itself is.
- M2 (does a stopped OS process clear the app's Background-tasks entry): not measured by the Lead — asked of the owner.
- M3: moot, see F3/F10.

Decisions (by recommendation, until the owner's word):
- F1 = (a) foreground and background alike. F2 = 3600 / 7200. F4 = (a). F5 = (a). F6 = (a). F7 = (a). F8 = (a). F9 = (a).
- F3 / F10: G2 (the stdin class) is DROPPED from the gate — by the spec's own condition (§3.2: "if M1 shows the wrapper
  redirects stdin, G2 is dropped"). The reaper's age rule covers a call that hangs for an unknown reason; its log is the
  evidence for any later gate class. §3.2, the G2 rows of §7.1 and the PowerShell row leave the cards.
- F11: a finding for the package-guard pile is filed by the Lead after this node lands. F12: not built.
- Plan critic: mandatory (a mechanism with a kill on the execution path).
