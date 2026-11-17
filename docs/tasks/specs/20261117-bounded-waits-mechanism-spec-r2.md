# Bounded waits r2 — DELTA to r1 after plan review t-1131 (t-1136, F19) — DRAFT

Base: `docs/tasks/specs/20261117-bounded-waits-mechanism-spec.md` (r1); review `docs/tasks/specs/reviews/t-1131-bounded-waits-plan.md`.
Owner, 17.11.2026: «делаем всё сейчас. Один раунд не стоит потери контекста» — gate, reaper, stale-narrative node, window
node and finding all land in this round. Lead facts taken as given: F-R0 (13:28) and M1 (stdin is `/dev/null`, G2 dropped).
Forks go back in §9; none is decided here. No path under `ai-packages/qa-factory/` (AR naming n/a, as in r1 §1).

## §0 Fix table — every fix of t-1131

| fix | change | § |
|---|---|---|
| K1 E18 negative | E18 now: `journal_write.py:612-617`, `test_redundancy.py:69-78` kill trees (no lister); neither reused | §2 |
| K1 §6.2 negative | RUNBOOK §9.1(f) :237-239 teaches an `until` loop → applied neighbour | §6.1 |
| G-1 `for` loops | refused only on a literal budget > MAX; word list counts | §3 |
| G-2 cap connective/direction | C2/C3 bind alone or by `&&`/`-and` (while), `\|\|`/`-or` (until), comparator in the loop's sense | §3 |
| G-3 §9.1(f) | replaced in the gate commit, text quoted | §6.1 |
| G-4 Monitor | §3 row, §5.2 edge, named in both door texts | §3, §5.2 |
| minor rows | brace group, clock AT, depth AT | §7.1 |
| F-R0 PowerShell wrapper | measured: the command text is in no command line → the PS row identifies a call, never decodes it | §5.1 |
| F-R1 tree / root age / `wrapper_forms` / `unwrap_failed` | applied; shape is a LOG label under FA(a) | §5.1, FA |
| F-R2 in-process walk, pid + creation | `tools/session_proc.py`; launcher passes `--session-pid/--session-created` | §5.0 |
| F-R3 parent older than child | every hop of every walk | §5.0 |
| F-R4 per-session lock/status | applied | §5.2 |
| F-R5 root-first one move | applied as per-pid handle TerminateProcess (not `taskkill /T`) | §5.2, FK |
| F-R6 never_reap rows | applied; `gh`/`docker` by whole name | §5.1 |
| F-R7 POSIX | POSIX `session_process_names` row empty → `no-session` → nothing stopped | §5.0, FP |
| F-R8 S0 | FA: (a) stop every tree > limit (rec.), (b) report S0; command + live kids logged either way | §5.1, FA |
| K4 live witness | K-WIRE acceptance; M2 observed in the same step | §10 |
| K5 line r1:645 false | corrected under FA | §5.1 |
| K6 walk in-process | K-REAP non-goal: no child process on the hook path | §10 |
| K6 journal_write :615/:631 | own node K-WIN with before/after measurement | §10 |
| K7 stdin clauses | deleted; texts rewritten | §6 |
| K8 rows | added | §7 |
| K9 (a) | walk in ms, no child | §8 |
| K9 (b) axis block | 38 single lines, labels from headings (`mechanism_gate.py:402`, label rule :34-58) | §8 |
| K9 (c) check 27(e) | stdin out; S0/unknown_root/no-session/orphans in | §6.3 |
| K9 `*_PATH`, `*_next` | env read only in tests (grep in acceptance); `*_next` deleted at placement | §10 |
| K10 K-REAP executable, launcher, main checkout, G2 removal | applied; removal = review K10 list verbatim | §5.3, §10 |
| K11 stale narrative | node K-STALE; `_compact_block` :2526-2530 compares | §10, FN |
| DUP axis 11 | G1 grammar moves with queued C1/F-C4; `wrapper_forms` on the axis-11 line | §3, §6.3 |
| brief: long-task door | §5.4 | FL |
| brief: F11 finding | K-FIND | F11 |
| brief: no person configures | rows in repo data, triggers in existing hooks | §8(a) |

**Unchanged r1 sections:** §1 (minus "G2") · §2 (minus E18 above; E25 marked "superseded by M1") · §3.1/§3.3/§3.4 except
§3-delta and the review-K10 G2 removals · §4 (M2 observed in the K4 witness) · §13. REPLACED: §5, §6, §7.2, §8, §9, §10.
EXTENDED: §7.1, §7.3, §11, §12, §14. DELETED: §3.2, M3, F3, F10.

## §3-delta — gate G1

- After r1 :86: «A `for`/`select` (Bash) or `for`/`foreach`/`ForEach-Object` (PowerShell) loop is bounded by its list. It is
  refused ONLY when its budget is literal and over MAX_WAIT_SECONDS: literal for the C1 counted forms and for a literal word
  list (count = words). A glob, `$(…)` or variable list → unknown → pass. A `for` loop is never refused as "not capped".»
- C2/C3 gain: «the counter/clock test binds only alone or joined at the TOP level of the condition by `&&` for `while`
  (`-and`) and by `||` for `until` (`-or`); comparator: `while` → `-lt`/`-le`/`<`/`<=`, `until` → `-ge`/`-gt`/`-eq`/`>=`/`>`.
  Otherwise not capped → refused.» Invariant: a cap counts only when it can end the loop (the cap test errs toward "not capped").
- §3.3 gains: «G1's grammar moves onto `hooklib.walk` with the queued axis-11 item C1/F-C4; no second copy meanwhile.»
- Both door texts end «… -- at most 3600 s in total -- or check once, or use the Monitor tool, and come back later.»
- §3.4 rows: a Monitor call → gate silent (matcher `Bash|PowerShell`), tree judged by the reaper; list/glob `for` → pass;
  G-2 forms → refuse.

## §5 The reaper (replaced)

### §5.0 This session

`tools/session_proc.py` (new) `session_process() -> (dict|None, reason)`: walks IN-PROCESS from `os.getpid()` up the parent
links (Windows: `CreateToolhelp32Snapshot` → ppid, exe; `OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION)` + `GetProcessTimes`
→ creation; POSIX `/proc/<pid>/stat`). A hop counts only if the parent was created BEFORE the child (F-R3), else the walk
stops (`orphan at <name>`). The FIRST ancestor whose exe name (case-insensitive) is in data row `session_process_names`
(Windows `claude.exe`; POSIX empty until measured) is the session `{pid, created}`; the app (`Claude.exe`) is further up
and never reached. Cap 32 hops. None reasons: `no claude.exe ancestor`, `orphan at …`, `hops over 32`, `api error <n>`,
`posix session name not measured`. Invariant: the session is known by pid AND creation time only; with no session nothing
is stopped. Error direction: may fail to find, never names a wrong process. Readers: launcher (§5.3), K-STALE.

### §5.1 Selection

A CANDIDATE is a tool-call TREE whose root R satisfies all of:
1. R.ppid = session.pid and R.created > session.created; `conhost.exe` is never a root.
2. R.name in `tool_call_roots` (`bash.exe`, `cmd.exe`) AND R.commandline matches a `wrapper_forms` row:
   - Bash (critic, 13:03): `bash.exe -c "source …shell-snapshots/snapshot-bash-… && eval '<cmd>' < /dev/null && pwd -P >| …"`;
     decode = the single-quoted word after the last top-level `eval`, `'\''` and `'"'"'` re-joined;
   - PowerShell (F-R0): `cmd.exe /d /s /c ""chcp.com" 65001 >nul & "powershell.exe" -NoProfile -NonInteractive … CLAUDE_CODE_SHELL_LAUNCHER_SCRIPT…`;
     decode = unavailable (the text is in an environment variable, never read).
   No row matches → not a candidate; log `unknown-root`, counter `unknown_root`.
3. now − R.created > `limit_seconds` (7200), strictly.
4. No process of the tree (R + descendants by F-R3 links) hits `never_reap`: whole names `gh.exe`, `gh`, `docker.exe`,
   `docker`; command-line substrings `story_run.py`, `run_headless.py`, `story_step.py`, `worktree_sweep.py`,
   `wait_reaper.py`, `-NoExit`. The reaper and its ancestors are never in a candidate.
5. Shape (log label): S1 a `sleep` process in the tree; S3 the decoded command gives `hygiene_gate.wait_loop_forms(...)`;
   S0 neither (a PowerShell tree is never S3). Fork FA: (a) every candidate STOPPED (rec.); (b) S1/S3 stopped, S0 REPORTED.
   K5 correction of r1 :645: under (a) the 11 h class ends at 2 h; under (b) it is reported with its live kids.

Orphans: a wrapper-matching root whose parent is absent or younger, older than the limit = a dead session's call: REPORTED
(`orphans`), stopped only by `--orphans --apply` (fork FO).

### §5.2 Stop and edges

Stop (fork FK, rec. a): per candidate, root first, then descendants breadth-first; for each pid `OpenProcess(PROCESS_TERMINATE
|PROCESS_QUERY_LIMITED_INFORMATION)` → `GetProcessTimes` on THAT handle → creation equal to the listed one within 1 s →
`TerminateProcess`. One attempt per pid per run. No child process (no `taskkill`, no window). Root first: the loop shell
cannot start the next `sleep`.

| edge | behaviour | invariant |
|---|---|---|
| no claude.exe ancestor (a person's terminal merge, POSIX) | nothing stopped; `no-session: <reason>`, one line | never kills on a guess |
| root younger than / AT the limit | untouched | a child younger than the limit is never touched |
| creation mismatch at the handle | skip, `pid-reused` | never kill an unselected process |
| open/terminate fails | `failed: winerror <n>` (absent → `gone`), counted; the next trigger tries once more | reported, never retried in a loop |
| app `-NoExit` shells, other sessions' calls | not children of this session | nothing outside this session's trees |
| long orphan whose dead parent pid is reused by a fresh root | link ignored (F-R3) | an orphan never joins a tree |
| Monitor call | judged like any root (wrapper row → by age; else `unknown-root`) | — |
| list unreadable (CIM error, 20 s, non-JSON) | no stop, `unreadable: <≤120 ASCII>`, exit 1 | never a silent pass |
| two sessions | lock + status in `<git common dir>/wait-reaper/<pid>-<yyyymmddHHMMSS>/`, shared `run.log`; same session twice → `busy` | one artifact, one writer |
| cmdline 64 KB / NUL / non-ASCII / nested quotes | decode cap 65536; ASCII-clipped log; never raises | a bad input never widens a stop |
| empty list | `finished`, 0; WAITS silent | — |

Tolerance 1 s is safe: a candidate is > 2 h old, so a reused pid is ≥ 2 h younger. Lister (detached reaper only):
`powershell -NoProfile -NonInteractive -Command "Get-CimInstance Win32_Process | Select-Object ProcessId,ParentProcessId,
Name,CreationDate,CommandLine | ConvertTo-Json -Compress"`, CREATE_NO_WINDOW, timeout 20 s.

### §5.3 Launcher, triggers, log

`wait_reaper.launch(trigger) -> str|None`: `session_process()` in-process; None → returns the no-session line, spawns
nothing; else `worktree_sweep.spawn_detached` of the MAIN checkout's `tools/wait_reaper.py --apply --trigger <t>
--session-pid <p> --session-created <iso>` (via the sweep's `repo_context`, also from a linked worktree: the session is the
unit). Never raises, never waits. Triggers (F6 a, F7 a): SessionStart (`session_context`), SubagentStop exit-0 path beside
`_record_returned` (`dod_gate.py:806`), `.githooks/post-merge` before the sweep line; session-handoff skill: dry
`python -B tools/wait_reaper.py`.
CLI: `[--apply] [--limit <s>] [--trigger <t>] [--session-pid <p> --session-created <iso>] [--orphans] [--pid <root>]`; no
`--session-pid` → resolves itself; default dry list.
Log: `<ts> <trigger> sess=<pid> stopped|failed|gone|pid-reused|reported|kept|unknown-root root=<pid> age=<s> shape=<S0|S1|S3>
name=<n> cmd=<decoded else raw, ≤2000 ASCII> kids=<name/pid/age/cmd≤200>;…(≤20) [fails=<name/pid/outcome>;…(≤20)]`.
`kept root=<pid>` (t-1177 R3, N3): a tree older than the limit left alone by `never_reap` or self-protection, said, never silent.
`fails=` (t-1177 R3, F4): every process of the tree whose stop failed, roots and kids alike. `status.json`: `{state, started,
finished, trigger, trees_stopped, procs_stopped, procs_failed, reported, unknown_root, orphans, reason}`.
WAITS (ASCII ≤200, silent at zero): `WAITS: last reap <ts> (<trigger>): <n> trees stopped, <m> processes failed, <u> unknown
roots; <o> calls of dead sessions -- python -B tools/wait_reaper.py --orphans --apply` · `WAITS: no session (<reason>) -- nothing
stopped` · `WAITS: process list unreadable (<reason>) -- python -B tools/wait_reaper.py`.

### §5.4 A legitimately long background task (fork FL)

Rec. (a): work that must outlive 2 h is no harness background call; it starts DETACHED — `Start-Process -WindowStyle
Hidden …` / `setsid nohup … >log 2>&1 &` — as the night driver already does (RUNBOOK §9.3). When the launching call ends it
is an orphan outside every tree (F-R3). Door: that form. Limit: none from the reaper (the §9.9 step is its net). Who: the
coordinator and the night agent; a worker never (§6.3 phrase). Named exemptions stay the `never_reap` row, changed by the
Lead in a commit. No per-call marker: on PowerShell the reaper cannot see the command (F-R0), so it would be a Bash-only road.

## §6 Rule text (replaced)

### §6.1 RUNBOOK — in the commit that places `hygiene_gate_next.py`
§9.1(f), lines 237-239, replaced by:
```
6. **(f) Ждёт прогон, а не человека.** Ожидание — ограниченный цикл (`for i in $(seq 1 30); do <проверка driver-runs.jsonl / хвоста лога> && break; sleep 20; done`, не больше 3600 с на вызов, §9.8), повторяемый, либо инструмент Monitor. Сообщений владельцу ночью нет.
```
§9.8, lines 393-401, replaced by (part A):
```
### 9.8. Фоновые ожидания

Ожидание в фоне ограничено (слово владельца 17.11.2026, спека t-1122). `tools/hygiene_gate.py` отказывает циклу `until`/`while`
со `sleep` без предела и циклу, чей бюджет больше 3600 с; отказ несёт форму, которую вставить (`for i in $(seq 1 30); do
<проверка> && break; sleep 20; done`). Лучше разовая проверка, уведомление harness или инструмент Monitor. Отчёт воркера
называет цикл, оставленный позади. После смерти воркера или потери сети СНАЧАЛА просмотреть список фоновых задач и
остановить зависшие (`TaskStop`); id устаревшей задачи без контекста находится по времени создания её файла `.output` в
папке `tasks/` сессии.
```

### §6.2 RUNBOOK — in the commit that places the K-WIRE triggers (part B appended to §9.8; per FA a, FL a)
```
То, что прошло мимо гейта (цикл в файле скрипта или в `bash -c "…"`, вызов, зависший по неизвестной причине), останавливает
`tools/wait_reaper.py` — на старте сессии, после остановки воркера и после слияния: фоновые вызовы ЭТОЙ сессии старше 2 ч,
целым деревом; каждая остановка — строка в его журнале, итог — строка `WAITS:` на старте сессии. Чужие сессии, ночной
драйвер, `powershell -NoExit` приложения и контейнеры стенда он не трогает. Работа дольше 2 ч запускается отдельным
процессом (`Start-Process -WindowStyle Hidden …`, как ночной драйвер, §9.3), не фоновым вызовом; так делает координатор,
воркер — никогда. Запись в списке фоновых задач, оставшаяся «running» после остановки, снимается `TaskStop`.
```
Under FA(b): «фоновые вызовы ЭТОЙ сессии старше 2 ч, целым деревом» → «вызовы этой сессии старше 2 ч с циклом ожидания или
`sleep`; прочие он только называет в строке `WAITS:`». §9.9 gains: «Остановку зависших фоновых вызовов этой сессии делает
`wait_reaper.py` (§9.8); этот шаг остаётся для остального: отдельные процессы, `docker`, процессы других сессий.»
§9.4/§9.5: n/a (the driver's own process).

### §6.3 Other carriers (same commit as §6.2, except the last line)
- builder.md rule 9 phrase (delivered by the no-briefs spec card): «A background wait names the file it waits for and its
  end; the gate refuses an unbounded loop with the form to paste in its refusal; a loop or process you leave running is
  named in your report (the rule: `docs/RUNBOOK.md` §9.8).»
- Check 27 (e) (t-1177 R3: also `kept` lines and the `fails=` field): «UNBOUNDED WAITS: the `unbounded wait` count from
  `permission_audit --summary`; from `<git common dir>/wait-reaper/run.log` every `stopped`, `reported`, `unknown-root` line
  of the window (and every `kept root=<pid>` line: a never_reap-kept tree older than the limit, still wanted?; and every
  `fails=` field: a process that could not be stopped) and the `no-session`/`orphans` counters. Each stop is a leak past the gate: read `cmd` and `kids`, name the form (script file, `bash -c`, dynamic cap,
  unknown hang), add a grammar row or record a named residual; each `unknown-root` is a harness wrapper change: add a
  `wrapper_forms` row. Unstamped/foreign `COMPACT NARRATIVE` lines seen in the window are counted. None: "no reaped waits".»
- SIBLING_MAP axis 11 line gains: «wait loops (G1) live in `hygiene_gate.py`'s walker; the reaper reads them only through
  `wait_loop_forms`; the harness wrapper unwrap is the data row `wrapper_forms` of `tools/wait-reaper.json`, coded once.»
- PROJECT.md § Сессия форджа, snapshot bullet (K-STALE placement commit): «снимок-рассказ получает штамп сессии:
  `python -B tools/compact_snapshot.py --stamp-narrative <файл>`».

## §7 Tests (delta)

### §7.1 gate — rows added to `ROWS`; removed: every S-* row, `MSG_STDIN`, door `stdin`, key `stdin_readers`
| id | command | expect |
|---|---|---|
| W-for-list / W-for-glob | `for f in a b c; do x; sleep 1; done` / `for f in *.md; do x; sleep 5; done` | silent |
| W-for-words-BEYOND | `for f in a b c; do x; sleep 1201; done` | deny (3603) |
| W-or-counter | `while [ $i -lt 30 ] \|\| ! test -f f; do i=$((i+1)); sleep 20; done` | deny |
| W-until-and | `until [ $i -ge 30 ] && test -f f; do i=$((i+1)); sleep 20; done` | deny |
| W-direction | `while [ $i -ge 0 ]; do i=$((i+1)); sleep 5; done` | deny |
| W-ps-or | `while ($i -lt 30 -or -not (Test-Path f)) { $i++; Start-Sleep 20 }` | deny |
| W-brace-group | `{ until x; do sleep 1; done; }` | deny |
| W-seconds-AT | `until test -f f \|\| [ $SECONDS -ge 3600 ]; do sleep 10; done` | silent |
| W-deep-AT | 64 nested `until x; do` … `done` | deny (recognized) |
| W-monitor | tool `Monitor`, `until x; do sleep 1; done` | silent |

### §7.2 reaper — new `tools/test_wait_reaper.py` (F9 a): one table over pure `select(procs, now, session, rows)`, one over the walk
| id | fixture | expect |
|---|---|---|
| R-real-bash | real Bash wrapper cmdline, root 3 h, `sleep` kid 15 s | stopped S1, root first |
| R-real-ps | F-R0 `cmd.exe` wrapper, root 3 h, `powershell.exe` kid | stopped (FA a) / reported (b); S0; decoded unavailable |
| R-AT / R-BEYOND / R-young | root 7200 / 7201 / 1800 s | kept / stopped / kept |
| R-11h / R-dev | root decoding `cat > /dev/null; python - <<…` 11 h with two bash kids / `npm run dev` + node 3 h | stopped S0 (a) / reported (b); kids logged |
| R-nearest | app claude.exe → session → root; app helpers + `-NoExit` | only the root's tree |
| R-no-session | walk None | nothing, `no-session` |
| R-orphan-reuse | 9 h `story_run.py`, ppid = a 10-min root | kept, not in tree |
| R-dead-session | wrapper root, parent absent, 5 h | reported; stopped only by `--orphans --apply` |
| R-conhost / R-unknown-root | session conhost 3 d / unmatched `cmd.exe` kid 3 h | kept / kept + `unknown_root` |
| R-never | tree with `gh.exe` / `story_run.py` / `-NoExit`; a path `…\high\x.exe` | kept ×3 / stopped |
| R-pid-reused / R-term-fails | creation differs at the handle / error 5 | `pid-reused` / `failed`, one attempt |
| R-two-sessions / R-busy | two session dirs / same session twice | both run / `busy` |
| R-unreadable / R-empty / R-CIM-date | raises, times out, non-JSON / [] / offsets +180, −300 | exit 1 / `finished` 0 / same age |
| R-cmd-adversarial | 64 KB, NUL, non-ASCII, `'\''`, `'"'"'`, 4-deep quotes | decodes or `unwrap_failed`; never raises |
| R-self | reaper + launcher in the list | kept |
| P-walk | found / app not chosen / orphan hop / 32 hops AT, 33 BEYOND / api error / POSIX empty row | session / nearest / None / found, None / None / None |

Lister, handle open/terminate and the walk's OS calls are thin seams replaced in the tables; no real process is touched.

### §7.3 wiring (added)
- `test_session_context.py`: WAITS rows (silent at zero; counts; no-session; unreadable; survives MAX_LINES; `launch`
  raising = one line). NARRATIVE rows: own stamp → `COMPACT NARRATIVE: <file> (<n> min old)`; foreign → `COMPACT NARRATIVE:
  newest is another session's (<file>) -- not your state`; unstamped or walk None → `COMPACT NARRATIVE: newest has no session
  stamp (<file>) -- check it is yours`; none → no line.
- `test_dod_gate.py`: a passing stop calls `launch` once; a blocked stop never; `launch` raising changes nothing.
- `test_compact_snapshot.py`: stamp inserts the header once (idempotent); refuses a hook snapshot, a missing file, walk None
  (exit 2, door named); body bytes after the header unchanged (BOM moved after the header, CRLF kept); `snapshot_identity`
  still None for a stamped narrative.
- `test_permission_audit.py:374`: label `"unbounded wait"` only.

## §8 Mechanism paperwork (replaced)

Mechanisms: G (gate G1), R (reaper, session_proc, triggers), N (narrative stamp). K-WIN is no mechanism: its commit carries
«axes: not a mechanism (a creation flag on four spawn sites; no duty or check changes)».

**(a) Cost.** G: one refusal per unbounded form, paste-in text included; one linear pass per call. R: the hook pays an
in-process walk (milliseconds, no child process); the detached reaper a 1-2 s CIM read off the critical path; the
coordinator starts > 2 h work detached. N: one stamp command per narrative (Lead). No person configures anything.
**(b) Axes** — one block, every line closing G/R/N; pasted UNFENCED into the commit message (the label layer skips fenced
regions, `mechanism_gate.py:52-54`); the Lead pre-checks it with the commit-msg gate:
```
axis 1 (policy <-> role files <-> journal): covered -- G/R RUNBOOK 9.8 one home + builder.md phrase; N PROJECT.md stamp line; no journal event
axis 2 (per-tier exam instruments): n/a -- no exam measures shell waits
axis 3 (factory package <-> its release copy): n/a -- no package path; kit copy of hygiene_gate is presence-only
axis 4 (factory rules <-> their debt): n/a -- no FR change
axis 5 (stage twins inside the package): n/a -- no package stage
axis 6 (measurement tools <-> the package they measure): n/a -- no measurer
axis 7 (per-test identity <-> every scope): n/a -- no test identity
axis 8 (where the story is on disk): n/a -- no story path
axis 9 (is this a test file): n/a -- no test-file leaf
axis 10 (git-top readers): covered -- R finds the git common dir through worktree_sweep repo_context
axis 11 (shell-command recognizers): covered -- G in the gate walker, R reads wait_loop_forms, wrapper_forms data row; hooklib.walk move queued (C1/F-C4)
axis 12 (carriers of the work plan): n/a -- the Lead places the cards in a pile node
axis 13 (the dispatch text): n/a -- no dispatch text
axis 14 (readers of agent transcripts): n/a -- R reads processes
axis 15 (console stream setup): covered -- R and N print ASCII like worktree_sweep
axis 16 (one json reader of the package): n/a -- tools side; wait-reaper.json read once, loud when broken
axis 17 (detector verdict shape): covered -- G keeps the gate's deny shape
axis 18 (in-tree shrink-only ratchets): covered -- any raise named in the verdict
axis 19 (one reader of a role file's tools): n/a -- no role file read
axis 20 (host receipt names): n/a -- no receipt
axis 21 (readers of the package's markdown tables): n/a -- package only
axis 22 (a host's return form): n/a -- package only
axis 23 (fields of a tests[] row): n/a -- package only
axis 24 (the record of an execution): n/a -- package only
axis 25 (freshness of a run): n/a -- package only
axis 26 (the word stand not confirmed): n/a -- package only
axis 27 (the profile of a test row): n/a -- package only
axis 28 (the render site of the row form): n/a -- package only
axis 29 (append-only jsonl writers): n/a -- run.log is plain text
axis 30 (the commands of a profile): n/a -- package only
axis 31 (role carriers): covered -- RUNBOOK 9.8 one owner, builder.md a pointer
axis 32 (where judgment lives): covered -- G/R/N check data only; every stop is read at check 27(e) by a tier above
axis 33 (which dispatch am i): n/a -- R never attributes to a dispatch
axis 34 (one road for one action): covered -- one selection for both shells (ancestry, wrapper row, age); POSIX empty row a declared safe default (fork FP)
axis 35 (sides of a story): n/a -- package only
axis 36 (the row written against a substitute): n/a -- package only
axis 37 (a repeat stop): n/a -- package only
axis 38 (the dry census): n/a -- package only
```
Commit lines: `tier: opus`; no `architecture:`/`judgment:` (no package path; their form lives only in `tools/architecture_gate.py`).
**(c) Detectors.** G, R, N: check 27 (e) (§6.3, its NARRATIVE sentence covers N); live: the WAITS line and the NARRATIVE line.
**(d) Skip-proofing.** G: PreToolUse on every Bash/PowerShell call. R: SessionStart, SubagentStop, post-merge — code; only the
handoff report is discipline (detector: the next WAITS line). N: the stamp is discipline; the SessionStart line names an
unstamped narrative at every compaction (detector on the path). Leak evidence: 07.10, 16.10, 20.10, 17.11.

## §9 Forks (recommendation first)

- **FA — unshaped trees.** (a) stop every candidate > 2 h, shape logged — rec.: one road for both shells (a PowerShell tree
  shows no shape, F-R0); ends the 11 h class. Cost: a background dev server or unknown long run of THIS session dies at 2 h
  (such work goes detached, FL). (b) critic F-R8: S1/S3 stopped, S0 reported — PowerShell loops and unknown hangs wait for a
  hand `--apply --pid`, the discipline that failed four times.
- **FL — long-task door.** (a) detached start; coordinator and night agent only; no reaper limit — rec. (b) a keep marker
  `WAIT_REAPER_KEEP=<s>` ≤ 28800: visible on Bash only → a second road; not rec.
- **FO — dead sessions' tool calls.** (a) report + `--orphans --apply` for the coordinator — rec. (owner-less, but possibly
  another project's). (b) stop automatically. (c) ignore.
- **FK — kill primitive.** (a) handle TerminateProcess per validated pid, root first — rec.: `taskkill /T` follows
  unvalidated ppid links (the K3-c class) and starts a child process. (b) critic F-R5 `taskkill /PID <root> /T /F`.
- **FN — narrative identity.** (a) stamp `<!-- compact-snapshot: narrative; session-proc: <pid>-<created>; written: … -->`
  from `session_process()`, compared with SessionStart's own walk — rec.: code only, the session process survives
  compactions (critic: one pid for 3 days); a resumed session reads its old narrative as foreign (safe: named, warned).
  (b) the harness session id, printed by SessionStart and typed by the Lead. (c) the id via a per-process record written by
  SessionStart.
- **FP — POSIX.** (a) empty POSIX `session_process_names` = `no-session` (FR-59 declared safe default), filled by one
  measurement on a POSIX seat — rec.; covering now needs a POSIX seat (none known here; estimate, not verified).
- **F11 — finding target.** `plans/piles/onboarding-hooks/findings/` (guard work: `batch-1-guard-and-install.md`) — rec.;
  alt. `words-gates`.
- **FW — sibling spawn sites.** Other `subprocess` sites in `tools/` run from hooks without CREATE_NO_WINDOW: one scout
  question after K-WIN's measurement shows whether a window can appear at all — rec.; or nothing.
- **F12** — unchanged (harness knob, not built).

## §10 Builder cards (replaced)

Order: K-GATE ‖ K-REAP ‖ K-WIN → Lead places K-GATE + §6.1 → K-STALE → K-WIRE → Lead: K4 witness, places, §6.2-§6.3. K-FIND any time.
Owns are outside the package: each DoD names the test file judging the path (CLAUDE.md rule 4). Common: the `*_PATH`
environment read lives ONLY in test modules (acceptance: `grep -rn "HYGIENE_GATE_PATH\|SESSION_CONTEXT_PATH\|DOD_GATE_PATH\|COMPACT_SNAPSHOT_PATH" tools/ --include=*.py`
shows only `test_*.py`); the Lead deletes every `*_next` file in the placing commit.

### K-GATE
given: r1 §3, §3.4, §7.1; this §3-delta, §7.1; review t-1131 K2, K10; tools/hygiene_gate.py; tools/test_hygiene_gate.py; tools/permission_audit.py :170-180, :455-477; tools/test_permission_audit.py :370-380, :725-740
owns:
C:/QAFactory/forge-repo/tools/hygiene_gate_next.py
C:/QAFactory/forge-repo/tools/test_hygiene_gate.py
C:/QAFactory/forge-repo/tools/permission_audit.py
C:/QAFactory/forge-repo/tools/test_permission_audit.py
non-goals: no edit of tools/hygiene_gate.py (live hook; the Lead places _next); no G2; the three existing classes unchanged; no hooklib import; no payload reading of -c
handoff: report per builder rule 7
edges: every G1 row of r1 §3.4 and §3-delta; r1 §3.3 positional invariants (order kept, purity, importable alone); budget 3600 AT silent / 3601 deny; depth 64 AT recognized / 65 pass; empty or whitespace command silent
DoD: `HYGIENE_GATE_PATH=tools/hygiene_gate_next.py python -m pytest tools/test_hygiene_gate.py tools/test_permission_audit.py -q` (the Lead re-runs it without the variable after placing)
siblings: run_allowed inherits (row); permission_audit label; axis-11 line (§6.3)

### K-REAP
given: this §5, §7.2; review t-1131 "Live measurements" and K3; F-R0 as written in §5.1; tools/worktree_sweep.py :1-40, :1100-1240; tools/hygiene_gate.py (placed; wait_loop_forms)
owns:
C:/QAFactory/forge-repo/tools/wait_reaper.py
C:/QAFactory/forge-repo/tools/session_proc.py
C:/QAFactory/forge-repo/tools/wait-reaper.json
C:/QAFactory/forge-repo/tools/test_wait_reaper.py
non-goals: no trigger wiring; no real kill in tests; no psutil or new dependency; no taskkill/powershell/wmic child on the hook path (the walk is ctypes in-process); no PowerShell decode
handoff: report per builder rule 7
edges: §5.0 none-reasons; every §5.2 row; limit AT kept / BEYOND stopped; hops 32 AT / 33 BEYOND; decode cap 65536; log cmd ≤2000, kids ≤20; one attempt per pid; CREATE_NO_WINDOW on the lister; a broken wait-reaper.json → exit 1 named, never a default selection
DoD: `python -m pytest tools/test_wait_reaper.py -q`
siblings: worktree_sweep spawn_detached / lock / status / repo_context by import (its launch_background is sweep-specific, not reused)

### K-WIN
given: review t-1131 K6; tools/journal_write.py :597-640; tools/test_redundancy.py :69-80
owns:
C:/QAFactory/forge-repo/tools/journal_write.py
C:/QAFactory/forge-repo/tools/test_redundancy.py
non-goals: no other spawn site (fork FW); no behaviour change besides the flag
handoff: report per builder rule 7, with the probe source in full and both outputs
edges: Windows only; POSIX kwargs unchanged; `creationflags` gains 0x08000000 at :603 (probe run), :615 (taskkill), :631 (OR-ed with CREATE_NEW_PROCESS_GROUP), test_redundancy :72
DoD: `python -m pytest tools/test_journal_write.py tools/test_test_redundancy.py -q`, plus the measurement: a scratch probe starts a parent python with DETACHED_PROCESS (no console, like a detached caller) that calls `journal_write.run_witness` on `python -c "import ctypes as c;k=c.windll.kernel32;print(bool(c.windll.user32.IsWindowVisible(k.GetConsoleWindow())))"` and prints the witness — before the edit (expected `True`, estimate) and after (`False`); once more from the tool-call shell (inherited hidden console). If "before" is `False` in both, the flag still lands (invariant: every spawn carries CREATE_NO_WINDOW) and the report says so
siblings: worktree_sweep.spawn_detached (already flagged)

### K-STALE
given: §5.0, §7.3, fork FN as accepted; tools/compact_snapshot.py :68-127, :610-720; tools/session_context.py :2380-2535 (read only); tools/session_proc.py (K-REAP)
owns:
C:/QAFactory/forge-repo/tools/compact_snapshot_next.py
C:/QAFactory/forge-repo/tools/test_compact_snapshot.py
non-goals: no edit of live tools/compact_snapshot.py (PreCompact hook; the Lead places _next); the hook header form unchanged; session_context untouched (K-WIRE)
handoff: report per builder rule 7
edges: one writer `narrative_header_line(proc, written)` and one reader `narrative_identity(path) -> {"session_proc", "written"} | None`, beside header_line/snapshot_identity; door `--stamp-narrative <path>` per §7.3 (idempotent; refusals exit 2 with the door); a header with odd fields reads "unknown" (never "own")
DoD: `COMPACT_SNAPSHOT_PATH=tools/compact_snapshot_next.py python -m pytest tools/test_compact_snapshot.py -q`
siblings: session_context _compact_block (K-WIRE reads narrative_identity)

### K-WIRE
given: §5.3, §7.3; tools/session_context.py :1885-1935, :2340-2360, :2380-2535; tools/dod_gate.py :735-810; .githooks/post-merge; tools/test_session_context.py :2151-2260; tools/test_dod_gate.py; .claude/skills/session-handoff/SKILL.md
owns:
C:/QAFactory/forge-repo/tools/session_context_next.py
C:/QAFactory/forge-repo/tools/dod_gate_next.py
C:/QAFactory/forge-repo/tools/post-merge.next
C:/QAFactory/forge-repo/tools/test_session_context.py
C:/QAFactory/forge-repo/tools/test_dod_gate.py
C:/QAFactory/forge-repo/.claude/skills/session-handoff/SKILL.md
non-goals: no edit of live session_context.py, dod_gate.py, .githooks/post-merge; no settings.json change (F7 a)
handoff: report per builder rule 7
edges: launch failure = one line, exit and message unchanged; a blocked stop launches nothing; WAITS silent at zero and surviving MAX_LINES; post-merge launches before the sweep, never fails the merge, prints the no-session line outside the harness; `_compact_block` :2526-2530 names a narrative per §7.3 (own / foreign / unstamped / none)
DoD: `SESSION_CONTEXT_PATH=tools/session_context_next.py DOD_GATE_PATH=tools/dod_gate_next.py python -m pytest tools/test_session_context.py tools/test_dod_gate.py -q`
siblings: worktrees_line twin; hook_liveness_probe unchanged (F7 a)

**K4 live witness** (Lead, K-WIRE acceptance, before placing): (1) background `for i in $(seq 1 900); do sleep 1; done`;
(2) after 70 s `python -B tools/wait_reaper.py --limit 60` — the verbatim list holds exactly that tree (no `-NoExit`, no
other session, no conhost); (3) `--apply --limit 60`, read the `run.log` line; (4) M2: did the Background-tasks entry turn
finished/failed by itself; (5) repeat (1)-(3) with PowerShell `for ($i=0; $i -lt 900; $i++) { Start-Sleep 1 }`.

**K-DOC** (Lead at placement): §6.1 with K-GATE; §6.2-§6.3 with K-WIRE; the PROJECT.md line with K-STALE. Witness: a
DOC-DISPATCH key-presence run, keys quoted from §6, with a negative control.

**K-FIND** (Lead): `plans/piles/onboarding-hooks/findings/20261117-unbounded-background-wait-of-a-role.md`, text: «Class: an
unbounded background wait (or any background call) of a factory role outlives the role. `guard_pre_tool.py` has no
wait-loop check (estimate, not read). Forge answer: t-1122 — a refusal with a paste-in capped form, and a reaper selecting
by session ancestry and age. Решение владельца нужно: нет. id: —.»

## §11 Readers — added rows (r1 rows stand)
| file | grep | hits | readers → verdict |
|---|---|---|---|
| `tools/journal_write.py` | `journal_write` in tools/*.py | 101 / 25 files | `run_witness`/`_find_bash` (12 / 4 files): journal_echo, test_journal_echo, test_journal_write — unchanged; the rest use CLI/constants — unchanged |
| `tools/test_redundancy.py` | `_kill_tree\|kill_tree\|test_redundancy` in tools | 15 / 5 files | test_test_redundancy, test_workflows :446/:511, test_quarantine — unchanged |
| `tools/compact_snapshot.py` | `compact_snapshot` in tools | 49 / 13 files | session_context (K-WIRE); hook_liveness_probe (PreCompact case; K-STALE checks no pinned text changes); test_compact_snapshot (K-STALE); journal_validator, mechanism_gate, piles, other tests — unchanged; `.claude/settings.json:132` — unchanged |
| `tools/session_proc.py`, `tools/wait_reaper.py` (new) | `session_proc\|wait_reaper` in tools | 0 (control: same call plus `session_context` → 154 / 34 files) | readers only from K-WIRE, K-STALE |
| `.githooks/*` | `compact_snapshot\|journal_write\|session_context\|dod_gate\|hygiene_gate` | 0 (control: `worktree_sweep\|mechanism_gate` → 5 / 2 files) | post-merge changes in K-WIRE |

## §12 Small choices closed (added)
- `session_proc.py` is its own module: the stamp must not import the reaper.
- §9.8 lands in two parts so each is true when it lands (temporal edge): A with the gate, B with the triggers.
- Creation tolerance 1 s; hop cap 32; decode cap 65536; log cmd 2000, kids 20.
- K-WIN's commit is "not a mechanism" (a flag only).

## §14 Reading trail (r2)
Read: r1 whole; review t-1131 whole; `docs/RUNBOOK.md` :230-244, :388-411; `tools/mechanism_gate.py` :24-63, :390-409;
`tools/session_context.py` :2380-2424, :2505-2539; `tools/journal_write.py` :585-640; `tools/test_redundancy.py` :62-79;
`tools/compact_snapshot.py` :68-127. Greps: SIBLING_MAP `^## Axis \d+` (38 headings, labels copied); session_context `MODEL:`
(:1073-1094) and `SESSION` -i (no session id printed: the basis of FN); compact_snapshot `narrative|session` -i; pile READMEs
glob; `guard_pre_tool` in plans/piles (196 / 89; README-only search empty, this is its control); §11 counts.
`tools/hygiene_gate.py` given, not re-read (r1 read it whole). Size target 25 KB: estimate ~30 KB, not measured (the 38-line
axis block and the quoted RUNBOOK texts are required verbatim).
Needed beyond the manifest: tools/mechanism_gate.py, tools/session_context.py, tools/journal_write.py, tools/test_redundancy.py,
tools/compact_snapshot.py, docs/SIBLING_MAP.md, plans/piles/.

## Lead decisions on r2 (17.11.2026, «решила сама», до слова владельца)

- FA = (a): every tree of this session older than 2 h is stopped, shape logged. A long run goes detached (FL a).
- FL = (a), FO = (a), FK = (a) handle per validated pid, FN = (a), FP = (a), F11 = onboarding-hooks, FW = one scout
  question after K-WIN's measurement.
- Order correction: K-REAP's given names the PLACED gate (`wait_loop_forms`), so K-REAP starts after the Lead places
  K-GATE; K-GATE and K-WIN run in parallel now.
