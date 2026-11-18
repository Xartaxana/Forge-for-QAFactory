# t-1189 — critic re-review, bounded waits fix round 3: K-GATE a1f5f7b6 (t-1184) and K-REAP 29079881 (t-1183)

What I reviewed: only the two fix diffs (`scratchpad/kgate_fix3.diff`, `scratchpad/kreap_fix3.diff`), checked against the items of
verdict t-1177 that they answer. The worktree HEADs match the diffs: `agent-ae768a3466f1d923e` is at a1f5f7b6 and `bw-kwire` is
at 29079881.

This is the critic's verdict. Accepting the work and placing it are the Lead's decisions.

**Verdict: NEEDS WORK, with one blocking finding (B1, blocks placement).**
- B1 is in the R5 fix. The new check in probe case 18 accepts only one of the two lines `launch` gives when it starts no reaper.
  Under `pytest tools/` on ubuntu CI, and in any run with no claude.exe ancestor, the other line comes. So the four whole-probe
  tests stay red after placement, whatever order the files are placed in.
- R1, R2, G1, G2, G3, G4, G5 and G7 are done, and each is done correctly.
- R4's row exists, but it is SKIPPED in every run before placement, the builder's witness run included (the "1 skipped" is this
  row). So it never ran. A fix of this round is to move it into the file where it runs.
- G8 is a new neighbour on the G1/G5 surface, measured: a backtick line continuation hides a PowerShell loop. Pass direction,
  fix of this round.

## Items: done or not

| item | status | where (file:line) and how I checked |
|---|---|---|
| R1 | done | `tools/test_p4_stdin_deadline.py:116,125` (diff lines). The test now runs `hook_argv(SCRIPT)`. Trace: the wrapper sets `wait_reaper.launch` to a silent lambda BEFORE `runpy`. `session_context_next.waits_lines` does `import wait_reaper` inside the function (`:1896`) and calls `wait_reaper.launch(...)` as an attribute (`:1908`), so it gets the lambda. `sys.argv[2]` = the script's folder = tools, the same module. Note: in my control run this test FAILED with `TimeoutExpired`, but the wrapper is not the cause. Measured on the live `session_context.py` with a silent stdin: wrapped 21.8 s, plain 20.5 s, wrapped again 21.9 s, all rc 0 with `NOW` printed. The test's `communicate(timeout=10)` misses on this host now with either argv. This is pre-existing and out of the diff (FR-31 class: N1) |
| R2 | done, one low leftover | `tools/no_reaper_wrap.py` (new) is the one `WRAP` plus `hook_argv`. `test_session_context.py` and `test_p4_stdin_deadline.py` call `hook_argv`. `test_dod_gate.py:37-39` imports `WRAP` but builds the argv by hand, and it repeats the `sys.path.insert` it already has at `:18` (fix L1). grep `wait_reaper.launch = lambda` over `bw-kwire/tools`: one hit, `no_reaper_wrap.py:10` |
| R4 (test row) | not done in effect | `tools/test_compact_snapshot.py:368-376` (`test_session_proc_id_is_the_stamp_the_writer_encodes`). In that file `sc` is `import session_context` (`:39`), which is the LIVE module. The candidate is loaded only by `test_session_context.py` (`:50-58`), as `session_context_candidate`, never under `sys.modules["session_context"]`. The live `session_context.py` has no `_session_proc_id` (grep: 0 hits), so the `hasattr` guard skips the row. Measured: `SKIPPED [1] tools\test_compact_snapshot.py:374: the candidate carries no narrative stamp reading`. This is the "1 skipped" of the builder's 716, and the report did not say the new row skipped. The assertion itself is right: the candidate `_session_proc_id()` with a patched walk gives `7-1.500` (my probe). After placement the row would run and would catch an unrenamed `import compact_snapshot_next`. Before placement it has no witness. Fix F1 |
| R5 | done in form, BLOCKER B1 in content | `tools/hook_liveness_probe.py:1154-1163,1491` (diff). The probe already honours the `runner` key (`hook_liveness_probe.py:1524-1525`). The check requires `WAITS: reaper not started`. B1 below |
| G1 | done | `tools/hygiene_gate_next.py:1516-1520` and `:1528-1531` (diff lines 57-79): `nl()` before the keyword's paren and before the do-loop's `while/until` paren, with `cond` taken from the paren `q`. Rows `tools/test_hygiene_gate.py` (diff 164-168): W-ps-while-newline-paren, W-ps-do-while-newline-paren, for-newline AT/BEYOND, foreach-newline-BEYOND. My probe: `while\n($true) {...}` → `['while']` |
| G2 | done | `hygiene_gate_next.py:1614-1616` (PS) and `:1622-1624` (Bash): an alternative `\$\1\s*=\s*\$\1\s*\+\s*(\d+)` / `\1\s*=\s*\1\s*\+\s*(\d+)`, with `m.group(5) or m.group(6)` going to `_stepped`. Rows diff 169-176 cover both shells, step 1 and step 2, AT/BEYOND (360/2 = 180 AT, 362/2 = 181 BEYOND) |
| G3 | done | `hygiene_gate_next.py:1558` (diff 90): an adjacent `&` before an `r` token is dropped like the fd digit. The `last == p` adjacency keeps `sleep 20 & >f` (a background job) unknown. Rows diff 177-180: `&>` and `&>>` AT/BEYOND |
| G4 | done per the Lead decision | `hygiene_gate_next.py:1684-1695` (diff 120-133): `_local_utc_offset()` = `time.localtime().tm_gmtoff`. On `ps` the base is `_now_epoch() + offset`. Only the PS `-UFormat %s` call site passes `True` (`:1713`); the Bash `date +%s` site (`:1719`) keeps the default `False` (grep `_deadline(`: two call sites). Rows per offset sign (diff 181-184) with `_now_epoch` = 1.8e9: offset +3600 → AT 1800007200 = 3600 silent, BEYOND 3601 deny; offset -3600 → AT 1800000000 = 3600 silent, BEYOND 3601 deny. The test patch is at diff 193-194. Traced: correct. Two low points: L2 (no Bash row runs with a nonzero offset) and L3 (the docstring does not name the accepted pwsh-7 residual) |
| G5 | done | `hygiene_gate_next.py:1533-1534` (diff 80-81): the pipe branch uses `opens(k + 1, "{")` with no `nl()`. Row W-ps-pipe-newline silent (diff 185) |
| G7 | done | `tools/under_test.py` (new) holds `load_under_test` byte for byte, and `tools/conftest.py` lost it. `test_hygiene_gate.py:21` and `test_permission_audit.py:24` import it `from under_test`. Case-insensitive grep `from conftest import\|import conftest\|conftest\.load_under_test` over both worktrees' `tools/`: 0 hits. Positive control, the same grep form: `load_under_test` users found at those two lines. At the G6 conversion, the K-REAP test files take `from under_test import load_under_test` |

## Findings

### B1 (BLOCKS placement): the case 18 check is red wherever the hook runs without a Claude session, ubuntu CI included

The surface is the probe case 18 check that reads the WAITS line `launch` returns (the R5 fix, `hook_liveness_probe.py:1161-1163`).

What happens:
- `wait_reaper.launch` (`bw-kwire tools/wait_reaper.py:550-552`) resolves the session FIRST. With no session it returns
  `"WAITS: no session (%s) -- nothing stopped"`, and it never reaches the repo/not-found branch that returns
  `WAITS: reaper not started (...)`.
- `session_proc.session_process` (`tools/session_proc.py:239-241`) returns `(None, "posix session name not measured")` on posix
  and `(None, "no claude.exe ancestor")` on Windows outside a session.
- CI runs `python -m pytest tools/ -q` on `ubuntu-latest` (`.github/workflows/forge-check.yml:40,96`).
  `test_hook_liveness_probe.py` runs the whole probe with no skip marker (for example `:960-969`, which asserts
  `OVERALL: OK` and `N/N alive`).
- Measured, candidate code: `wait_reaper.launch('subagent-stop', None, walker=lambda: (None, 'posix session name not measured'))`
  → `WAITS: no session (posix session name not measured) -- nothing stopped`. That line does not contain the required substring.

The answer to the dispatch's edge question (does placement order make the four green?):
- On this Windows host, inside a Claude session: yes. `dod_gate_next.py` has to land on `tools/dod_gate.py` IN THE SAME COMMIT
  as the merge of the probe edit, or before it. The probe edit changes the live `hook_liveness_probe.py` directly, so a merge
  without placement leaves main red in between, and the `--post-merge` probe would report `[DEAD] 18-...`.
- On ubuntu CI, and in any run with no claude.exe ancestor (for example a plain terminal `pytest`): no. The four stay red
  whatever the order, because the line that comes is the `no session` one.

Fix (this round, `tools/hook_liveness_probe.py`): assert what proves "no spawn". `launch` returns None only on the spawn path,
so every line it returns means nothing was spawned. Require the stderr to match `^WAITS: (reaper not started|no session) `
(re.M), or simply any `WAITS: ` line. Keep the message naming the received stderr.

Neighbours of this surface that I walked: `launch`'s returns are no-session, Refuse, not-found and exception. All of them are
"no spawn" lines, and the fix above accepts each one. `_launch_reaper`'s own exception line (`dod_gate_next.py:769`) is
`WAITS: reaper not started (...)`, which is already accepted.

### F1 (fix of this round; R4 row): the row runs only after placement, so it has no witness before it

Detail: see R4 in the table.

Fix: move the row into `tools/test_session_context.py`, next to `test_k_wire_compact_narrative_names_whose_it_is` (`:2302`),
where `sc` is the candidate under `SESSION_CONTEXT_PATH`. It then runs in the witness run, and placement does not change it.

The `hasattr` skip guards on these rows (here, and `test_session_context.py:2304`) turn a later rename of `_session_proc_id` into
a silent skip. They are only needed while the candidate is unplaced, so removing them belongs in the Lead's placing commit
(proposed placement step).

### G8 (fix of this round, pass direction; neighbour of G1/G5): a backtick line continuation hides a PowerShell loop

The surface is the PowerShell line-end adjacency in `_ps_loops`. This is its encoding neighbour (rule 14), and it is
pre-existing, not a regression.

Why it happens: `_PS_TOK_RE` (`hygiene_gate_next.py:1422`) lexes the backtick as a word, so `nl()` stops on it.

Probe of the candidate (`_ps_loops(_wait_lex(c, True))`):
- `while \`\n($true) {...}` → `[]`;
- `1..1000 | ForEach-Object \`\n{ Start-Sleep 20 }` → `[]`;
- `while ($true) \`\n{...}` → `[]`.

Control: `while\n($true)` → `['while']`.

Measured in Windows PowerShell 5.1: `1..2 | ForEach-Object \`<nl>{ "p$_" }` and `while \`<nl>($i -lt 2) {...}` both run as loops
and print `p1 p2 w1 w2 end`.

Fix: in `_wait_lex`, treat a continuation as blank before tokenizing, keeping positions: PS `` `\n `` → two spaces. With that,
the G5 rule ("no `nl()` on the pipe form") stays true, because a continued line is not a line end.

Rows:
- W-ps-while-backtick-paren (deny);
- W-ps-allman-backtick (deny);
- W-ps-pipe-backtick-BEYOND (deny).

The Bash `\`+newline twin, for example `sleep \<nl>20` inside a loop, is the same class. I did NOT probe it. Walk it in the same
fix: `\\\n` → two spaces for Bash.

### Low (fixes of this round)

- **L1 (Q6):** `test_dod_gate.py:36-39` should use `hook_argv(SCRIPT)` instead of a hand-built argv identical to it. Drop the
  second `sys.path.insert` (the first is at `:18`).
- **L2 (Q5):** no Bash epoch row runs with a nonzero `_local_utc_offset`. If `_deadline` applied the offset on Bash too (for
  example a default `ps=True`), every row would still pass. Add one row, W-epoch-bash-offset-AT: offset +3600 patched, Bash
  `date +%s` literal 1800003600 → silent, the budget unchanged.
- **L3 (Q7):** two stale texts.
  - The `_ps_loops` docstring (`hygiene_gate_next.py:1491-1493`) lists the line-end cases without the new keyword-to-`(` case
    and without the pipe exception (which lives only in a trailing comment).
  - The `_deadline` docstring states the 5.1 premise, but not the residual the Lead accepted with option (a): pwsh 7 prints UTC,
    so in UTC+ zones the base over-shoots by the offset and the count is too low.

### N1 (note, outside the diff)

`test_session_context_subprocess_survives_stdin_that_is_never_closed` has a 10 s `communicate` timeout. On this host now the
live `session_context.py` run takes about 21 s with either argv (measured above). This is a load-sensitive test (FR-31 class)
that predates this diff. The Lead decides whether it gets a node.

## Standing questions

- **Q1 fit:**
  - R1, R2, G1, G2, G3, G4, G5 and G7 are met.
  - R4's row is written but unwitnessed (F1).
  - R5 breaks CI (B1).
- **Q2 builder decisions:**
  - The builder put the R4 row in `test_compact_snapshot` because `_session_proc_id` lives in session_context. Wrong file for
    the binding (F1).
  - `hook_argv` resolves the import folder from the script. Right for tools/*.
- **Q3 seams:**
  - The probe's `runner` key is an existing seam (`:1524`).
  - `_deadline`'s new `ps` keyword is additive, with a default of False.
  - `under_test` and `no_reaper_wrap` are new plain modules. No conftest import remains.
- **Q4 class completeness:**
  - F5 class: p4 is closed. t-1177 walked no other subprocess run of `session_context.py`.
  - R5 surface (lines `launch` returns): B1.
  - PS line-end surface: G8, with the Bash continuation twin to walk in the same fix.
  - G4: one function with a per-shell flag, and both call sites read.
- **Q5 tests:**
  - K-GATE: 474 = 452 (my t-1177 re-run) + the 22 new rows (diff 164-185). Consistent.
  - K-REAP: 711 + 4 + 1 = 716. The 1 skipped is the R4 row (measured).
  - Volume: table rows plus one function plus one probe check, against about 30 product lines. No `tests-over:` is owed.
  - Gap: L2.
- **Q6 duplication and consistency:** L1.
  - Searched: `wait_reaper.launch = lambda` (1 hit), `from conftest import|import conftest|conftest.load_under_test` (-i, 0 hits;
    control: the `load_under_test` users found) and `_deadline(` (2 call sites).
  - Two plain helper modules (`under_test.py`, `no_reaper_wrap.py`) serve two different concerns. Acceptable.
- **Q7 code quality:**
  - L3.
  - Cosmetic only: `hygiene_gate_next.py:1533` is over 135 characters with its trailing comment.
- **Q12 one road:**
  - G4 is one formula, with the clock's semantics chosen per shell by one flag. No exclusion.
  - Nothing else.
- **Q8-Q11:** n/a (forge tools; no package path).

## Mechanical layer

The builders' runs are attached in the dispatch:
- K-GATE `474 passed`, negative control `34 failed, 440 passed`;
- K-REAP `4 failed, 711 passed, 1 skipped`.

I did not re-run K-GATE. The check is consistency (Q5).

## Trail

Read:
- t-1177 (whole);
- both fix diffs (whole);
- `bw-kwire`:
  - `tools/dod_gate_next.py:750-790`;
  - `tools/session_context_next.py:1885-1908` (grep), `:2543-2556`;
  - `tools/wait_reaper.py:545-567`;
  - `tools/session_proc.py:231-246`;
  - `tools/compact_snapshot_next.py:138-144`;
  - `tools/test_compact_snapshot.py:1-40` (grep);
  - `tools/test_session_context.py:40-60`, `:2296-2312`;
  - `tools/test_dod_gate.py:1-40` (grep);
  - `tools/test_p4_stdin_deadline.py:255-295`;
  - `tools/hook_liveness_probe.py` grep `runner`;
  - `tools/test_hook_liveness_probe.py` grep and `:960-972`;
  - `.github/workflows/forge-check.yml` grep;
- K-GATE `tools/hygiene_gate_next.py`: `:1421-1422`, `:1446-1512`, grep `_deadline(`/`nl`/`opens`.

Runs:
- Control (bw-kwire, the three `_PATH` variables): pytest of the R4 row plus the p4 session_context test, `-rs` →
  `SKIPPED [1] tools\test_compact_snapshot.py:374 ... 1 failed, 1 skipped in 12.63s` (the failure is `TimeoutExpired`).
- In the same call: candidate `_session_proc_id()` → `7-1.500`; `launch` with a no-session walker →
  `WAITS: no session (posix session name not measured) -- nothing stopped`.
- Timing of the live `session_context.py` under a silent stdin: wrapped 21.8 s / plain 20.5 s / wrapped 21.9 s, rc 0, NOW present.
- K-GATE probe of `_ps_loops` on the backtick forms (results above).
- Windows PowerShell 5.1 script with backtick continuations → `p1 p2 w1 w2 end`.

No reaper was run, and no full set.

```json
{
  "verdict": "blocker",
  "blockers": [
    "B1: tools/hook_liveness_probe.py _check_journal_hooks_returned (R5 fix) requires 'WAITS: reaper not started', but wait_reaper.launch (wait_reaper.py:550-552) returns 'WAITS: no session (...) -- nothing stopped' when no session resolves (posix: 'posix session name not measured'; Windows outside a session: 'no claude.exe ancestor'); CI runs pytest tools/ on ubuntu-latest, so the four whole-probe tests stay red after placement regardless of order -- accept any launch line (regex ^WAITS: (reaper not started|no session) ), which all mean no spawn"
  ],
  "fixes": [
    "F1: move test_session_proc_id_is_the_stamp_the_writer_encodes from test_compact_snapshot.py (sc there is the live session_context, so it skips: measured SKIPPED at :374, the builder's 1 skipped) into test_session_context.py next to the narrative rows where sc is the candidate; Lead's placing commit drops the hasattr skip guards",
    "G8: _wait_lex treats a line continuation as blank before tokenizing, positions kept (PowerShell backtick-newline; walk the Bash backslash-newline twin in the same fix); rows W-ps-while-backtick-paren, W-ps-allman-backtick, W-ps-pipe-backtick-BEYOND deny (measured: PS 5.1 runs them as loops; candidate _ps_loops finds none)",
    "L1: test_dod_gate.py builds HOOK with hook_argv(SCRIPT) and drops the duplicate sys.path.insert",
    "L2: one Bash epoch row with _local_utc_offset patched to +3600 asserting the date +%s budget is unchanged",
    "L3: update the _ps_loops docstring (keyword-to-paren line end, pipe exception) and name the accepted pwsh 7 residual in the _deadline docstring"
  ],
  "class_completeness": "F5 class: p4 session_context subprocess test now through hook_argv (closed). R5 surface (lines launch returns): only the not-started line accepted, the no-session line missed (B1); Refuse/not-found/exception lines all mean no spawn. PS line-end surface: keyword-to-paren and do-while paren fixed (G1), pipe exception (G5), backtick continuation missed (G8, measured), Bash backslash-newline twin unprobed and to be walked in the same fix. G4: one _deadline with a per-shell flag, both call sites read (grep _deadline). Duplication: one WRAP (grep), test_dod_gate argv hand-built (L1); conftest import gone in both worktrees (grep with positive control).",
  "trail": {
    "read": [
      "docs/tasks/specs/reviews/t-1177-bounded-waits-fix-rereview.md",
      "scratchpad/kgate_fix3.diff (whole)",
      "scratchpad/kreap_fix3.diff (whole)",
      "bw-kwire tools/dod_gate_next.py:750-790, tools/session_context_next.py:1885-1908 and 2543-2556, tools/wait_reaper.py:545-567, tools/session_proc.py:231-246, tools/compact_snapshot_next.py:138-144",
      "bw-kwire tools/test_compact_snapshot.py:1-40, tools/test_session_context.py:40-60 and 2296-2312, tools/test_dod_gate.py:1-40, tools/test_p4_stdin_deadline.py:255-295, tools/test_hook_liveness_probe.py:960-972, tools/hook_liveness_probe.py grep runner",
      "K-GATE tools/hygiene_gate_next.py:1421-1422, 1446-1512, grep _deadline",
      ".github/workflows/forge-check.yml grep runs-on and pytest"
    ],
    "reruns": [
      {"command": "bw-kwire, three _PATH vars: pytest test_compact_snapshot.py::test_session_proc_id_is_the_stamp_the_writer_encodes test_p4_stdin_deadline.py::test_session_context_subprocess_survives_stdin_that_is_never_closed -q -rs", "result": "SKIPPED [1] tools/test_compact_snapshot.py:374; 1 failed (TimeoutExpired), 1 skipped in 12.63s"},
      {"command": "candidate _session_proc_id with patched walk; wait_reaper.launch with a no-session walker", "result": "7-1.500; WAITS: no session (posix session name not measured) -- nothing stopped"},
      {"command": "live session_context.py under silent stdin, wrapped vs plain argv, timed", "result": "wrapped 21.8s, plain 20.5s, wrapped 21.9s, rc 0, NOW present"},
      {"command": "K-GATE _ps_loops(_wait_lex(c, True)) on backtick-continued forms", "result": "while-backtick-paren [], pipe-backtick [], allman-backtick []; control while-newline-paren ['while']"},
      {"command": "powershell 5.1 script with backtick continuations in ForEach-Object pipe and while", "result": "p1 p2 w1 w2 end"}
    ]
  }
}
```
