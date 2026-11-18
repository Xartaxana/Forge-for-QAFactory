# t-1177 — critic re-review, bounded waits: the fix diffs t-1169 (K-GATE) and t-1171 (K-REAP / K-STALE / K-WIRE)

What I reviewed: only the fix diffs, against my two earlier verdicts.
- `docs/tasks/specs/reviews/t-1159-bounded-waits-gate-win-code.md` (findings F1-F7 and F12, plus the epoch decision the Lead
  took on my spec note).
- `docs/tasks/specs/reviews/t-1160-bounded-waits-reaper-code.md` (findings F2-F8, F13-F15, N3 and N7).

The diffs:
- A) The scratch `kgate_fix.diff`: the live `tools/hygiene_gate.py` against the candidate `ba53c0fe:tools/hygiene_gate_next.py`,
  plus the conftest and test diffs.
- B) `git diff 094fbf95 4e008c33`.

This is the critic's verdict. Accepting the work and placing it are the Lead's decisions.

**Verdict: NEEDS WORK, with one blocking finding (R1, blocks placement).**
- All 24 prescribed items are done, and each one is done correctly.
- The remaining findings are neighbours of the same surfaces, each found by a walk around a fixed item.
- R1 is the F5 class again: a test that starts a real `--apply` reaper against the live session once the code is placed. It is
  in a third test file that F5 did not name.
- Everything else is fix-round or placement-commit work.

## Prescribed items: done or not

| item | status | how I checked |
|---|---|---|
| t-1159 F1 Allman `){`, `do{`, `}while` | done | rows W-ps-allman, -crlf, -do-allman, -do-allman-while, for/foreach-allman AT/BEYOND; neighbour G1 open |
| F2(a) redirect target / fd digit | done | `_sleep_words`; probe `sleep 2>/dev/null 20` → 3620 deny, `sleep 20>/dev/null` silent (bash fd 20, no operand: correct); neighbour G3 open |
| F2(b) `(1..N) \| ForEach-Object` | done | `back` map; probe `@(1..181) \| ForEach-Object` → deny 3620 |
| F3 masked body | done | rows W-quoted-increment (Bash, PS); probe `i=$((i+1))` unquoted still capped (silent) |
| F4 step | done | `_stepped`; rows W-step AT/BEYOND/unknown on both shells; regression G2 |
| F5 one start-word tuple | done | `_START_WORDS` builds both; the per-reader case rule kept (Bash words are case-sensitive; the walker also serves PS): right |
| F6 split + one loader | done in K-GATE | `_loop_budget` is equivalent to the old `finish` body (traced, incl. the parent-sleep fold); K-STALE/K-WIRE loaders: G6 |
| F7 PS AT/BEYOND rows | done | W-ps-for-AT / -BEYOND |
| F12 visible G1 failure | done | `wait_loops_unchecked` → note `wait loops not checked (<exc>)`; row with an injected ValueError |
| Lead epoch decision | done for Bash; PS premise false on this host | G4 (measured) |
| t-1160 F2 5 s, one walk, one context | done | `launch(timeout=5, repo=)`, `waits_lines` one `session_process()`, `Git(timeout=5)`; row pins `walks == 1`, `git_timeouts == [5]` |
| F3 read before launch | done | row pins `events == ["read", "launch"]` |
| F4 kids' failures, units | done | `fails=` field, ACCESS_DENIED + `GetExitCodeProcess` != STILL_ACTIVE → gone (the handle carries QUERY_LIMITED_INFORMATION, which is enough), `trees_stopped/procs_stopped/procs_failed`; rows; readers: R3 |
| F5 payload cwd, Popen test | done for the named sites | dod_gate passes `payload.get("cwd")`, row pins `roots == [journal_repo]`; probe case 18 resolves its tmp `git init` repo → "tools/wait_reaper.py not found" line, no spawn; sibling R1 open |
| F6 odd stamp | done | `"unknown"` → the no-stamp line; row renamed `odd_field_never_own_never_foreign` |
| F7 one stamp encoder | done | `compact_snapshot.session_proc_stamp`, both sides call it; placement note R4 |
| F8 post-merge try | done | `sh -n` ok (builder); text read: one `WAITS: reaper not started (<Type>)` line |
| F13 select split; walks | done | `_Index`, `_build`, `_candidate_pass`, `_orphan_pass`; the extra compact walk is judged below |
| F14 tests-over | done | 4e008c33 carries `tests-over:` naming ed466898 / 094fbf95; the reason (edge rows of the spec) holds under TESTING «Бюджет» |
| F15 SKILL | done | `--apply --pid <root>` |
| N3 kept line | done | `kept root=<pid>` emitted, row; reader: R3 |
| N7 fallback / hasattr | done | both removed; CRLF copy-from-git stays the Lead's placement step |

**The Lead's decision on F13 (one more walk on a `source=compact` start): I agree.**
- `_session_proc_id` is called only from `compact_snapshot_lines`, and that is the compact branch (`session_context_next:2467`).
- The walk is one in-process Toolhelp snapshot, with no git call and no subprocess.
- Passing the walk from `waits_lines` into the compact block would tie two independent blocks of `build_context_lines` together.
  That costs more than one extra walk at a rare start.

## Findings

### R1 (BLOCKS placement): `tools/test_p4_stdin_deadline.py` starts a real `wait_reaper --apply` on the live session

This is the same class as F5(b). F5 named the test_session_context deadline test, and that test is now silenced. This one is
not.

Where: `test_session_context_subprocess_survives_stdin_that_is_never_closed`, `tools/test_p4_stdin_deadline.py:263-282`.

What happens:
- The test runs `[sys.executable, str(SCRIPT)]`, where `SCRIPT = tools/session_context.py` (:56). It sets `cwd=tmp_path` and
  never writes to stdin.
- `main()` takes `resolved_root = repo_root()`, which is `Path(__file__).resolve().parent.parent`, the live checkout
  (`session_context_next:357-358`). The stdin timeout only empties the payload; `build_context_lines` still runs.
- `build_context_lines` calls `waits_lines(root)` unconditionally (`:2384`).
- So after placement, `launch("session-start", <live repo>)` → `repo_context` → main checkout → `tools/wait_reaper.py` exists →
  `spawn_detached(... --apply ...)`. That spawn runs against the session that is running pytest.

Measured on the bw-kwire candidate, with `launch` patched to record and spawning nothing:
`repo_root C:\QAFactory\forge-repo\.claude\worktrees\bw-kwire` / `launch got [('session-start', 'C:\\...\\bw-kwire')]`. The hook's
own root is what reaches `launch`, never `tmp_path`.

Harm: the same as in F5. run.log gets false `session-start` triggers, the last run's `status.json` is reset, and the "no real
kill in tests" norm is broken. CI (`pytest tools/`) also runs this test.

Neighbours I walked (rule 14):
- The parametrized `test_subprocess_survives_stdin_that_is_never_closed` (:368-384) also runs dod_gate. A stdin timeout returns 0
  before `_launch_reaper` (`dod_gate_next` main: the `timed_out` return comes first), so there is no spawn.
- `test_compact_snapshot.py:586` runs with `--root tmp`, and compact_snapshot launches nothing.
- No other subprocess run of `session_context.py` exists in tools tests (grep below).

Fix: run this test through the same no-reaper wrapper, using one shared helper (R2).

### R2 (fix-round, Q6): the no-reaper wrapper now exists twice

- `test_session_context._NO_REAPER_WRAP` (:614) is `test_dod_gate._WRAP` (:37) again; its own comment says «the same form».
- R1 would add a third copy.
- Fix: one helper next to `load_under_test`, for example `no_reaper_argv(script) -> list`, used by all three sites.

### R3 (placement commit, AR-22 / P27): the fix changed what run.log and WAITS produce, and their readers' text was not updated

What changed:
- The new `kept` label.
- The new `fails=` field.
- The WAITS wording is now «N trees stopped, M processes failed».
- The `status.json` keys are now `trees_stopped/procs_stopped/procs_failed`.

The carriers still say the old thing:
- spec r2 §5.2 (:131) lists the labels `stopped|failed|gone|pid-reused|reported|unknown-root`;
- §5.3 (:134) gives «<n> stopped, <m> failed»;
- the text of check 27(e) (:183-186) reads only `stopped`, `reported` and `unknown-root` lines. It has not yet landed in
  `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` (grep: no `UNBOUNDED WAITS` there).

If 27(e) does not read `kept` lines, N3's line has no reader. Fix (Lead, placing commit): sync these three places, and add `kept`
(«a never_reap-kept tree older than the limit: still wanted?») to the lines 27(e) reads. No code reader of the old keys exists:
`waits_line` is the only one, and it was updated.

### R4 (placement note): two `import compact_snapshot_next` sites must both be renamed

- The sites are `session_context_next:2457` (`compact_snapshot_lines`) and `:2549` (`_session_proc_id`).
- `_session_proc_id` swallows every exception and returns None. If only one site is renamed, the stamp is never "own", and that
  is silent; the safe direction is the "check it is yours" line.
- No row would catch it: the narrative rows pass `own_proc` directly.
- Suggest one row: `_session_proc_id()` with `session_proc.session_process` patched to `({"pid": 7, "created": 1.5}, "")`
  returns `"7-1.500"`.

### R5 (low; the siblings line «hook_liveness_probe fingerprint gap»)

- Case 18 is now safe by structure: payload `cwd` = tmp `git init` repo → `launch` returns «tools/wait_reaper.py not found in
  <tmp>», with no spawn.
- Adding `<common>/wait-reaper` to `_LIVE_STATE_TARGETS` (:208-217) would make the probe flaky. The live session's own
  SubagentStop and SessionStart write there during any probe run, and there is no probe-owned name to scope by, unlike `dir-own`.
- The deterministic detector is the case's own check instead: `_check_journal_hooks_returned` also asserts that the dod_gate
  stderr carries `WAITS: reaper not started`. A future change that spawns from case 18 then turns the probe red.
- Proposed as a fix of this round. If hook_liveness_probe is a placement-only path, it goes in the Lead's placing commit.

### G1 (fix-round, pass direction; neighbour of F1): a line end between the PS keyword and `(` still hides the loop

- Probe on the candidate: `while\n($true) { Start-Sleep 5 }` → silent.
- Measured: Windows PowerShell 5.1 runs `while\n($i -lt 2) { $i++; "w$i" }` as a loop and printed `w1`, `w2`, `after-while`.
- Same surface: `opens(k + 1, "(")` for `while/for/foreach`, and `opens(w + 1, "(")` after `} while|until` in a do-loop. Both have
  no `nl()`.
- Fix: `nl()` at both points. Rows W-ps-while-newline-paren (deny) and W-ps-do-while-newline-paren (deny).

### G2 (fix-round, pass direction; a regression from the F4 fix): `i=i+1` / `i=i+K` / `$i = $i + K` are no longer read

- Live gate: `for ((i=0;i<1000;i=i+1)); do sleep 20; done` → deny, 20000. Candidate → silent.
- PowerShell is the same: `for ($i = 0; $i -lt 1000; $i = $i + 1) { Start-Sleep 20 }` → live deny 20000, candidate silent.
- My F4 text allowed "any other form → unknown". But this form was read correctly before, so the fix loses a literal budget the
  gate used to see.
- Fix: accept `\1\s*=\s*\1\s*\+\s*(\d+)` (Bash, inside `(( ))`) and `\$\1\s*=\s*\$\1\s*\+\s*(\d+)` (PS) as step K. Rows
  W-step-assign-BEYOND for both shells.

### G3 (fix-round, pass direction; neighbour of F2(a), not a regression): `sleep 20 &>/dev/null` hides a literal budget

- `for i in $(seq 1 181); do x; sleep 20 &>/dev/null; done` → silent on both live and candidate. The real budget is 3620.
- Cause: `_wait_lex` emits `&` as a word. Its lex of `sleep 20 >&2` is `('w','&',10,False)`. In `&>` the `&` word is kept in
  `words`, and `_sleep_seconds` then returns unknown.
- Fix: in `_sleep_words`, drop a word `&` that sits right before an `r` token, the same way as the fd digit. Rows
  W-redirect-amp-BEYOND (deny), and `&>>` too.

### G4 (fix-round, needs the Lead's decision; rule 13): on this host `Get-Date -UFormat %s` is not UTC epoch seconds

Measured on this machine:
- `powershell` is 5.1.26100 and `pwsh` is absent.
- `[DateTimeOffset]::UtcNow.ToUnixTimeSeconds()` = `1794925989`.
- `Get-Date -UFormat %s` = `1794929589,87537`.
- `(Get-Date).ToUniversalTime() | Get-Date -UFormat %s` = `1794925989,87537`.
- Python `tm_gmtoff` = 3600.

So Windows PowerShell 5.1 returns the LOCAL wall clock as epoch seconds. In UTC+1 that is the real epoch plus 3600, with a fraction
and a locale comma. The candidate computes `literal - time.time()`, which gives the following:
- In this zone, a loop whose deadline literal comes from Get-Date's own output, with a real wait of W seconds, gets the budget
  W + 3600. That is over MAX for every W > 0, so every such loop is refused, including a 1-minute wait (a false refusal).
- In UTC- zones the gate under-counts by the offset, so a pass beyond the budget is possible.
- The row W-epoch-ps-AT (`_now_epoch` = 1.8e9) models a premise that does not hold on this host.

The Bash side is right: Git-Bash `date +%s` is UTC.

Options for the Lead:
- (a) On the PS clock, base = now + local offset (matches 5.1, the shell measured here). With pwsh 7 in UTC+ it under-counts by
  the offset.
- (b) PS epoch literal → unknown → pass.
- (c) Keep refusing on PS.

My recommendation is (a), with one row per sign of the offset. The decision is the Lead's.

### G5 (low, refuse direction; from the F1 fix): `nl()` on the pipe form recognizes a non-loop

- Candidate: `1..1000 | ForEach-Object\n{ Start-Sleep 20 }` → deny 20000.
- Measured: PS 5.1 ends the pipeline at the line end and fails with `ParameterBindingException` (Process is missing). The braces
  that follow are an unexecuted script block.
- A cmdlet's argument cannot follow a line end; only the language keywords allow it.
- Fix: no `nl()` for the `foreach-object/%/foreach`-after-`|` branch. Row W-ps-pipe-newline (silent).

### G6 (fix-round after the two branches converge, Q6; rest of F6): three candidate loaders are still copies

- `test_session_context.py:47-48`, `test_dod_gate.py:20-21` and `test_compact_snapshot.py:21-23` keep their own env readers.
  `load_under_test` lives on the K-GATE branch.
- Fix: in the placing commit, or the first fix round after both branches are on main, the three use `load_under_test`.

### G7 (low; the siblings line «conftest module name in mixed runs»)

- `from conftest import load_under_test` resolves through `sys.modules["conftest"]`.
- pytest 9.2 `_importconftest` deletes that entry before each non-package conftest (I read the source). So in a run that also
  loads `gateway/conftest.py`, the name points at gateway's file. The result is a loud ImportError at collection, never a silent
  pass.
- CI runs `python -m pytest tools/ -q` alone (`forge-check.yml:96`), and gateway is not used in this deployment. So today nothing
  breaks.
- Fix (cheap, this round): move `load_under_test` and the R2 helper into a plain module, for example `tools/testkit_load.py`.
  `conftest` should not be imported by name.

### N-A1 (note, the Lead's choice)

- `_collect_signals` now reads the clock for an epoch literal, and permission_audit replays history through it. So a historic
  epoch-deadline command is labelled against today's clock: past → 0 → silent.
- The docstring says so honestly. The options are to pass the event's ts through, or to accept this as a named residual of the
  audit.

## Standing questions

- **Q1 fit:** the prescribed items are met (table above). The left-overs are G1-G5 and R1.
- **Q2 builder decisions:**
  - Reading `[DateTimeOffset]::...ToUnixTimeSeconds()` as no epoch clock is the safe direction (it stays refused). OK.
  - Per-reader case rules: OK.
  - `_exited` reads any doubt as False, so a failure stays a failure. OK.
- **Q3 seams:**
  - `launch(..., timeout=5, repo=None)` is additive.
  - `waits_line` keys renamed with their only reader.
  - `_launch_reaper(cwd)` falls back to the hook's cwd when the payload has none, and its docstring «never the hook's own cwd»
    overstates that. Harmless: a payload without `session_id` returns before the launch.
- **Q4 class completeness:**
  - F5 class: R1 open.
  - F1 surface: G1 and G5.
  - F2 surface: G3.
  - F4: G2.
  - Readers of the new run.log forms: R3.
  - Axis 11, the second lexer: `_PS_REDIR_RE` (`hygiene_gate_next:1544`) is one more recognizer inside `_wait_lex`'s world, which
    is covered by the queued axis-11 line (`docs/SIBLING_MAP.md:294`). It is not a new finding.
- **Q5 tests:**
  - Killing power: my re-run of the 29 new rows plus the F12 test against the live gate gives `22 failed, 8 passed`. That matches
    the builder's 22 failures; the builder's wider selection had 41.
  - Expected values trace to the card edges, except W-epoch-ps-AT (G4).
  - Volume: the K-GATE fix is about +50 test lines against about +120 product lines. The t-1171 round adds table rows only.
  - Nothing deleted.
- **Q6 duplication and consistency:** R2, G6. `_PS_REDIR_RE` is under axis 11 (queued). Searched: `git grep "_WRAP\b|_NO_REAPER_WRAP"`,
  `git grep "(SESSION_CONTEXT|DOD_GATE|COMPACT_SNAPSHOT|HYGIENE_GATE)_PATH"`, and the redirect regexes in hygiene_gate_next.
- **Q7 code quality:**
  - `finish` is now flat, `_loop_budget` is a pure function, and `select` is split into named passes. Good.
  - Cosmetic only: wait_reaper.py has 4 lines over 135 characters (before the fix there were 2), in the two `status.update` calls.
- **Q12 one road:**
  - G4 is one formula applied to two clocks whose semantics differ on this host.
  - Nothing else: both shells keep one grammar each.
- **Q8-Q11:** n/a (forge tools, no package path; data checks only).

## Trail

Read:
- the two earlier verdicts (whole) and `.claude/agents/critic.md` (role text);
- the scratch `kgate_fix.diff` (whole);
- `git diff 094fbf95 4e008c33` (all 10 files);
- `git log 094fbf95..4e008c33` (the message with `tests-over:`);
- `ba53c0fe:tools/hygiene_gate_next.py`: `_wait_loop_forms` body, `_B_CLOCK_RES`, `_PS_CMP_RE`;
- `4e008c33`:
  - `tools/session_proc.py:118-145`;
  - `tools/worktree_sweep.py:100-108`;
  - `tools/session_context_next.py:357-358`, `:2372-2386`, `:2440-2470`, `main`;
  - `tools/dod_gate_next.py:772-830`;
  - `tools/wait_reaper.py` launch;
  - `tools/hook_liveness_probe.py:200-250`, `:1104-1113`, `:1138-1160`, `:1395-1415`;
  - `tools/test_p4_stdin_deadline.py:1-30`, `:236-282`;
- spec r2 grep (:84-189);
- `.github/workflows/forge-check.yml:96` and the nightly.yml grep;
- pytest `_importconftest` source.

Runs (verbatim tails):
- `HYGIENE_GATE_PATH=<wt>/tools/hygiene_gate_next.py python -m pytest tools/test_hygiene_gate.py tools/test_permission_audit.py -q`
  (K-GATE worktree) → `452 passed in 7.17s`. The builder's 452 is reproduced.
- The same worktree, live gate, `-k` the 29 new rows plus the F12 test → `22 failed, 8 passed, 337 deselected in 0.89s`.
- `python -m pytest tools/test_wait_reaper.py -q` (bw-kwire, HEAD 4e008c33) → `69 passed in 0.25s`.
- The three `_PATH` variables, `pytest test_session_context.py test_dod_gate.py test_compact_snapshot.py -k "k_wire or
  narrative"` → `22 passed, 470 deselected in 3.26s`.
- stdin probe on the candidate G1 grammar (`_wait_loop_forms`, `_now_epoch` = 1.8e9), quoted:
  - `pipe-newline-not-a-loop deny [('pipe','C1',20000.0)]`
  - `bash-i=i+1-BEYOND silent []`
  - `ps-i=i+1-BEYOND silent []`
  - `bash-sleep-amp-redirect silent []`
  - `ps-while-kw-newline-paren silent []`
  - `bash-sleep-in-redirect-first deny 3620`
  - `ps-at-group deny 3620`
  - `ps-do-until-allman deny`
  - `bash-incr-unquoted silent []`
  - `bash-SECONDS-big deny 1800003600`
- The same probe on the live gate: `LIVE bash-i=i+1-BEYOND deny 20000`, `LIVE ps-i=i+1-BEYOND deny 20000`,
  `LIVE bash-sleep-amp-redirect silent`.
- `powershell` 5.1: `while\n(...)` → `w1 w2 after-while`; `1..2 | ForEach-Object\n{...}` → ParameterBindingException.
- `powershell` 5.1 epoch → `1794925989` / `1794929589,87537` / `1794925989,87537`; python gmtoff 3600; `pwsh: command not found`.
- `waits_lines(repo_root())` on the bw-kwire candidate with `launch` recording → the root is the candidate tree, not a tmp path.

The reaper was never run. No full sets were run, and no agent .output files were read.

```json
{
  "verdict": "blocker",
  "blockers": [
    "R1: tools/test_p4_stdin_deadline.py:263-282 runs tools/session_context.py as a subprocess with no root; main uses repo_root() (session_context_next:357) and build_context_lines calls waits_lines unconditionally (:2384), so after placement the test spawns a real wait_reaper --apply against the live session (F5 class, third file) -- run it through the no-reaper wrapper"
  ],
  "fixes": [
    "R2: one shared no-reaper wrapper helper instead of test_dod_gate._WRAP and test_session_context._NO_REAPER_WRAP, reused by the R1 site",
    "R3: placing commit syncs spec r2 section 5.2 labels (add kept, fails=), section 5.3 WAITS wording (trees stopped / processes failed) and the check 27(e) text so it also reads kept lines",
    "R4: placement renames both import compact_snapshot_next sites (session_context_next:2457 and :2549); add one row asserting _session_proc_id() returns 7-1.500 for a patched walk",
    "R5: hook_liveness_probe case 18 check also asserts the dod_gate stderr carries WAITS: reaper not started (a deterministic detector instead of a flaky fingerprint of the shared wait-reaper dir)",
    "G1: hygiene_gate_next _ps_loops apply nl() between while/for/foreach and the opening paren, and between a do-loop while/until and its paren; rows deny",
    "G2: read i=i+K (bash arithmetic for) and $i = $i + K (PS for) as step K; rows BEYOND deny on both shells (regression from the F4 fix: live denies 20000, candidate silent)",
    "G3: _sleep_words drops an ampersand word right before a redirect token so sleep 20 &>/dev/null keeps its literal; rows for &> and &>> BEYOND deny",
    "G4: Lead decides the PowerShell epoch base: Windows PowerShell 5.1 Get-Date -UFormat %s is local wall clock as epoch (measured +3600 here), so literal minus time.time() over-counts by the UTC offset; recommended base now plus local offset, rows per offset sign",
    "G5: no nl() for the ForEach-Object pipe form (a cmdlet argument cannot follow a line end; measured ParameterBindingException); row silent",
    "G6: after both branches converge, test_session_context, test_dod_gate and test_compact_snapshot candidate loaders use load_under_test",
    "G7: move load_under_test (and the R2 helper) into a plain module so no test imports conftest by name"
  ],
  "class_completeness": "F5 class (real reaper spawned by tests/probes): dod_gate tests, test_session_context deadline test, hook_liveness_probe case 18 fixed; test_p4_stdin_deadline subprocess test open (R1); other subprocess runs of session_context/dod_gate walked: p4 parametrized dod_gate returns before launch, compact_snapshot launches nothing. F1 surface (PS newline adjacency): keyword-to-paren missed (G1), pipe over-reach (G5). F2 surface (sleep arguments): &> missed (G3). F4 step reading: i=i+K regression (G2). Producer/reader of run.log and WAITS: spec and check 27(e) text to sync (R3). Axis 11 second lexer: _PS_REDIR_RE falls under the queued line docs/SIBLING_MAP.md:294. Duplication: wrapper (R2), loaders (G6).",
  "trail": {
    "read": [
      "docs/tasks/specs/reviews/t-1159-bounded-waits-gate-win-code.md",
      "docs/tasks/specs/reviews/t-1160-bounded-waits-reaper-code.md",
      ".claude/agents/critic.md",
      "scratchpad/kgate_fix.diff (whole)",
      "git diff 094fbf95 4e008c33 (10 files) and git log 094fbf95..4e008c33",
      "ba53c0fe:tools/hygiene_gate_next.py _wait_loop_forms, _B_CLOCK_RES, _PS_CMP_RE",
      "4e008c33:tools/session_proc.py:118-145, tools/worktree_sweep.py:100-108",
      "4e008c33:tools/session_context_next.py:357-358,2372-2386,2440-2470,main",
      "4e008c33:tools/dod_gate_next.py:772-830, tools/wait_reaper.py launch",
      "4e008c33:tools/hook_liveness_probe.py:200-250,1104-1113,1138-1160,1395-1415",
      "4e008c33:tools/test_p4_stdin_deadline.py:1-30,236-282",
      "docs/tasks/specs/20261117-bounded-waits-mechanism-spec-r2.md grep 84-189",
      ".github/workflows/forge-check.yml:96",
      "pytest 9.2 _pytest.config.PytestPluginManager._importconftest source"
    ],
    "reruns": [
      {"command": "HYGIENE_GATE_PATH=candidate python -m pytest tools/test_hygiene_gate.py tools/test_permission_audit.py -q (K-GATE worktree)", "result": "452 passed in 7.17s"},
      {"command": "python -m pytest tools/test_hygiene_gate.py -q -k <29 new rows + F12 test> against the live gate", "result": "22 failed, 8 passed, 337 deselected in 0.89s"},
      {"command": "python -m pytest tools/test_wait_reaper.py -q (bw-kwire 4e008c33)", "result": "69 passed in 0.25s"},
      {"command": "three _PATH vars, pytest test_session_context.py test_dod_gate.py test_compact_snapshot.py -k k_wire or narrative", "result": "22 passed, 470 deselected in 3.26s"},
      {"command": "stdin probe of _wait_loop_forms on candidate and live gate", "result": "candidate: ps-while-kw-newline-paren silent, bash-i=i+1-BEYOND silent, ps-i=i+1-BEYOND silent, bash-sleep-amp-redirect silent, pipe-newline-not-a-loop deny 20000; live: i=i+1 forms deny 20000"},
      {"command": "powershell 5.1: while newline paren loop; ForEach-Object newline brace; Get-Date -UFormat %s vs UtcNow", "result": "w1 w2 after-while; ParameterBindingException; 1794929589,87537 vs 1794925989 (offset 3600)"},
      {"command": "waits_lines(repo_root()) on bw-kwire candidate with launch recording", "result": "launch got session-start with the candidate tree root, not a tmp path"}
    ]
  }
}
```
