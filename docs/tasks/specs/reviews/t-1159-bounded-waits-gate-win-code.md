# t-1159 — code critic, bounded waits: K-GATE (t-1142) + K-WIN (t-1143)

Spec: `docs/tasks/specs/20261117-bounded-waits-mechanism-spec-r2.md` (§3-delta :49-61, §6.1 :146-164, §7.1 :195-208, cards §10
K-GATE :330-342, K-WIN :356-366, Lead decisions :432-end) and r1 §3.1/§3.3/§3.4/§7.1, which it keeps.
Under review: K-GATE as placed on main in `23c9fee3` (I checked the live `tools/hygiene_gate.py` against the builder's candidate
`6cf19472:tools/hygiene_gate_next.py`: byte-identical; the test files on main match the branch too), and K-WIN `bac7a9a2` (not merged).

**Verdict: NEEDS WORK.** Nothing blocks. There are 12 fix-round items. Five of them are in the gate's grammar (F1-F4,
F12), and F1 is a silent pass on a legal PowerShell form. K-WIN's flags are right, but the node has no check that could
catch the defect it exists for (F9), and one spawn in its own file was missed (F8). Accepting or merging is the Lead's
decision.

## Findings

Every item below is fix-round severity. None blocks.

**F1 — a PowerShell loop whose block starts on the next line is not recognized. This is a silent pass on an unbounded wait.**
- Where: `tools/hygiene_gate.py:1508`, `:1512`, `:1519`. `opens(c + 1, "{")` and `opens(k + 1, "{")` need the `{` to be the very
  next token, but `_PS_TOK_RE` emits `\n` as a separator token.
- Probe on main:
  - `while ($true)\n{\n  Start-Sleep 5\n}` → silent, and the CRLF variant is silent too.
  - `do\n{\n  Start-Sleep 5\n} while ($true)` → silent.
- Measured: PowerShell runs both forms as loops (scratch `allman.ps1` printed `while-allman:3` and `do-allman:2`).
- Rules broken: r1 §3.4 says «the line end never hides a keyword», and FR-4 forbids a silent pass.
- Surface: the PS bracket matcher. Neighbours I walked:
  - `for (…)\n{` is the same miss. A literal BEYOND budget passes.
  - `foreach (…)\n{` is the same miss.
  - `} \n while (…)` in a do-loop: `toks[b + 1]` has the same adjacency assumption.
- Fix: skip `\n` tokens between `)` and `{`, between `do` and `{`, and between `}` and `while`/`until`. Add rows W-ps-allman,
  W-ps-allman-crlf and W-ps-do-allman (deny).

**F2 — a literal budget is missed (pass direction).** §3-delta says a `for` is refused only on a literal budget over MAX, so a
literal budget must be read.
- (a) `_sleep_seconds` (:1537) collects every word up to a separator, including a redirect's target and fd digit. Example:
  `for i in $(seq 1 181); do x; sleep 20 2>/dev/null; done` → silent, although the literal budget is 3620 s. Fix: skip the word
  after an `r` token and the digit word just before it.
- (b) The pipe loop's list is `toks[k - 2]` only (:1521), so `(1..1000) | ForEach-Object { Start-Sleep 20 }` → silent.
  Fix: when that token is `)`, take its matched group.

**F3 — a cap counted from quoted text.** `_increments` reads the RAW body (:1614).
- Example: `until [ $i -ge 30 ]; do echo "i=$((i+1))"; sleep 20; done` → silent, though the loop never ends.
- This breaks the §3-delta invariant «a cap counts only when it can end the loop (errs toward "not capped")».
- Fix: search the masked body; `finish` already has `masked`.

**F4 — a false refusal at AT.** The arithmetic `for` regex (:1567) takes the third clause as `[^;]*` and ignores the step.
- Example: `for ((i=0;i<360;i+=2)); do sleep 20; done` → deny with budget 7200; the true budget is 3600.
- The PS `for` regex (:1562-1563) has the same gap.
- Fix: read `i++` / `i+=K` and divide the count by K. For any other form return unknown → pass, since a `for` is never refused
  as "not capped".

**F5 — Q6 duplication: a second start-word list.**
- `_BASH_CONT` (:1419) restates `_START_WORD_RE` (:128) plus `if`/`while`/`until`.
- r1 §3.1 says «after the EXISTING start words». The two lists also differ in case: G1's matches exactly, the walker's ignores
  case.
- Fix: one tuple, with both built from it. The lexer-level duplication (`_wait_lex` beside `_Walker`) is already queued on
  SIBLING_MAP axis 11 (`docs/SIBLING_MAP.md:294`, «Queued (C1, F-C4, t-120)»), so it is not a finding.

**F6 — Q7 code quality.**
- `_wait_loop_forms` (:1661-1722) is about 62 lines. Its nested `finish` goes four levels deep
  (`def → if has → else → if got is None`). Extract `_loop_budget(f, raw, masked, ps) -> (budget, refuse, cap)`.
- Copy-paste: `_gate_under_test` is the same 17 lines in `tools/test_hygiene_gate.py:23-40` and
  `tools/test_permission_audit.py:23-40`. K-STALE and K-WIRE need three more (`COMPACT_SNAPSHOT_PATH`, `SESSION_CONTEXT_PATH`,
  `DOD_GATE_PATH`). Fix: one helper `load_under_test(env_var, module_name)` in `tools/conftest.py`, which already exists, used by
  every card of the topic.

**F7 — Q5(c): the PowerShell AT/BEYOND rows are missing.**
- The card's edge «budget 3600 AT silent / 3601 deny» has Bash rows only: W-seq-AT/BEYOND and W-seconds-AT/BEYOND.
- The PS count is its own branch (`_counted_count` :1558-1566), and the only PS rows are W-ps-for (600 s) and W-ps-range-BEYOND
  (20000 s).
- Fix: add W-ps-for-AT, `for ($i = 0; $i -lt 180; $i++) {…Start-Sleep 20}` → silent, and W-ps-for-BEYOND (181) → deny. The probe
  shows both already behave; the rows pin them. Also add one row each for F1-F4.

**F12 — Q2: G1 fails silently.** The `try/except → []` at `_collect_signals` (:1749-1752 on main) makes a grammar bug a silent
pass.
- The module docstring says «Any exception while classifying fails open VISIBLY» (`decide`, MSG_FAIL_OPEN_TEMPLATE), and the
  rollback class reports `rollback not checked: …`.
- Fix: put a marker in the signals (for example `wait_loops_unchecked: <exc type>`). `_decide_command` turns it into a note
  `wait loops not checked (<exc>)`.

**F8 — K-WIN, Q4: a spawn in the node's own owns was left without the flag.**
- `tools/test_redundancy.py:90-95` (worktree): `Popen(... creationflags=CREATE_NEW_PROCESS_GROUP)` has no CREATE_NO_WINDOW.
- The card's DoD invariant is «every spawn carries CREATE_NO_WINDOW». Its edges list only `:72`, which is a dispatcher gap.
- The builder saw the spawn (narrative 1500: «Сосед: test_redundancy.py:89-94») and sent it to FW. But the spawn is inside its
  own file, so sweep-the-artifact-first applies: fix it in this round.

**F9 — K-WIN, Q5(a): no check can catch the node's defect.**
- The DoD tests pass whether the flag is there or not, and the window probe read False both before and after. As the dispatch
  notes, a ConPTY measurement is unreliable.
- My flags probe on the same three sites is the check that does catch it:

  | build | bash probe `run` | taskkill | `run_witness` Popen |
  |---|---|---|---|
  | main | `0x0` | `0x0` | `0x200` |
  | K-WIN | `0x8000000` | `0x8000000` | `0x8000200` |

  DETACHED is unset everywhere.
- Precedent rows assert this exact invariant: `tools/test_worktree_sweep.py:1336-1337` and
  `ai-packages/qa-factory/scripts/tests/test_place_session.py:538`.
- Fix: add one parameterised row in `tools/test_journal_write.py` that patches `subprocess.run`/`Popen` and asserts
  `flags & 0x08000000` and `not flags & 0x8` for `_find_bash`, `_kill_tree` and `run_witness`. This widens the owns by one test
  file.

**F10 — K-WIN, Q6: four spellings of one flag.**
- `journal_write.py:597` defines `CREATE_NO_WINDOW = 0x08000000`.
- `test_redundancy.py:73` uses the bare `0x08000000`.
- `worktree_sweep.py:1215` and `walk_session.py:2041` use literals.
- Inside this diff, at least the test_redundancy site should use the name. The class across tools/ is a question for the FW
  scout.

**F11 — rule 7: the K-WIN witness is not attached.** The builder's report (probe source and both outputs) did not reach this
dispatch; I had only the Lead's narrative paraphrase.
- The load-bearing claims are now reproduced: DoD 103 passed, 6 skipped (re-run), plus the flags probe above.
- The acceptance event should carry the builder's verbatim probe output or this flags probe.

## The dispatch's questions

**(a) Does G1 refuse every unbounded form the spec names and pass the capped forms, AT and BEYOND? Yes, except F1-F4.**
- Spec rows: all r1 §7.1 W-rows and all r2 §3-delta rows are present and green.
- Capped forms:
  - Bash door at 30 / 180 / 181 iterations: silent / silent / deny (3620).
  - PS door at 30 / 180 / 181, and `-le 180`: silent / silent / deny / deny.
  - `foreach 1..181` and `{1..181}`: deny.
  - `((i<181))`: deny.
  - C3 at 180 / 181 (Bash and PS): silent / deny.
  - `.Elapsed` at 3600 / 3601: silent / deny.
- Unbounded forms: `while :`, `until false`, the newline form, PS do-while, `$( until … )`, sleep inside an if, and tabs: all deny.

**(b) Positional invariant: holds.** The deny is appended after the cd door (`_decide_command` :1872-1873). Nothing returns
early before the journal, worker-verdict, rollback or cd checks. `deny[0]` keeps its order (row W-order). `notes` are untouched.
`run_allowed` inherits the deny (rows wait-loop-unbounded and wait-loop-capped). A G1 exception cannot take the other classes
down (but see F12).

**(c) Siblings: other spawn sites in tools/ (non-test) without CREATE_NO_WINDOW.** Listed only, not fixed. `*` marks a site
reached from a hook.
- `dispatch_gate.py:1855`, `:1865` *
- `enforcement_probe.py:234`, `:266`
- `exam_runner.py:614`, `:903`
- `gitcmd.py:44` * (the hygiene gate's rollback measure, journal_write's `--run` road)
- `hook_liveness_probe.py:474`, `:985`, `:986`, `:1110`, `:1111`
- `journal_echo.py:563` *
- `journal_lock.py:57` * (via journal_write)
- `journal_validator.py:1954` * (pre-commit)
- `mechanism_gate.py:796`, `:811` * (commit-msg)
- `piles_testkit.py:21`
- `session_context.py:1495`, `:1544` * (SessionStart)
- `source_split.py:1995`, `:2088`
- `tools/tests/test_role_carriers_one_owner.py:180`
- `wave.py:77`, `:84`, `:266`
- `wiring_check.py:332`
- The test files: 77 files, 210 sites, not listed.

Only `worktree_sweep.py:1215-1219` is flagged. A window appears only under a console-less parent, and the detached roots
(worktree_sweep, walk_session) now give their children a hidden console. So FW's one scout question stands as the Lead decided.

**K-WIN flags against the DETACHED fact: correct.** No site sets DETACHED_PROCESS. `run_witness` ORs NO_WINDOW with
NEW_PROCESS_GROUP, the same pair as `walk_session.py:2039-2041` (the t-1151 fix). The probe's True/False was not used as
evidence; I judged the flag invariant, as the dispatch asked.

## Standing questions (rule 22)

- **Q1 fit:** K-GATE fits except F1-F4. K-WIN fits its listed sites, but not the DoD invariant at test_redundancy:90 (F8).
- **Q2 builder decisions:**
  - An unknown tool name falls back to the PS grammar, mirroring `_Walker` :1209. OK.
  - Depth over 64 gives no verdict for the whole command, as r1 §3.3 says. OK.
  - The silent except is F12.
  - K-WIN's `_no_window()` gives POSIX no kwargs, which is right.
- **Q3 seams:**
  - The `permission_audit` label is additive and uses `.get` for an old gate copy.
  - The `_collect_signals` key-set test was updated.
  - `wait_loop_forms` is the reaper's only entry.
  - Nothing was reordered.
- **Q4 class:** SIBLING_MAP axis 11 is covered (the queued line exists; the §6.3 line lands with K-WIRE). F8 is a sibling in the
  same artifact. Spawn siblings are listed under (c), behind FW. Axis 17: the deny shape is kept.
- **Q5 tests:**
  - (a) K-GATE rows go through `decide()`, the hook's door, so they have killing power. K-WIN has none (F9).
  - (b) Expected values trace to §7.1 and the card edges.
  - (c) F7.
  - (d) No test was deleted; the label test was renamed with its assertion widened.
  - (e) No duplicate rows found.
  - (f) Volume: about 140 test lines against about 357 product lines, so not over.
  - (g) No new test file.
- **Q6 duplication:** F5 and F10. The test loader copy is in F6. Masking reuses `_scan_heredocs`, `_mask_quoted_segments` and
  `_blank_comments` (good).
- **Q7 code quality:** F6.
- **Q8:** n/a, no package path.
- **Q9 ratchets:** no in-tree ratchet row was touched. The forge-check output was not attached, so I did not read it.
- **Q10 architecture:** no package path. `architecture:` is n/a per the commit.
- **Q11 judgment:** G1 judges the shape of command text, which is a data check. No role output is classified.
- **Q12 one road:** both shells take one grammar and one door each. Exclusions that stay are named with their carriers:
  - Monitor calls: r2 §3-delta row and §5.2 row; the net is the reaper.
  - `bash -c` / `powershell -Command` payloads: the named residual in PAYLOAD_INTERPRETERS (r1 §3.4).
  - Script files: r1 §3.4; the net is the reaper.

  None is new and unnamed.

## Seam and class notes

- **Spec, not code (non-blocking, Lead's choice):** r1 C2 takes «the literal integer the clock is compared with» as the
  budget. For `$(date +%s)` that literal is an absolute epoch. So `while [ $(date +%s) -lt 1763400000 ]; do sleep 5; done` is
  refused with budget 1763400000, which errs in the refuse direction. One line in the spec decides it: unknown → pass, or keep
  refusing.
- The 1 MB perf smoke takes about 1.76 s per the commit. The re-masking repeats the walker's pass; that is acceptable now and
  merges with the queued axis-11 move.

## Spot-checks

- Placement fidelity: `diff` of `23c9fee3:tools/hygiene_gate.py` against `6cf19472:tools/hygiene_gate_next.py` → IDENTICAL.
- `_next` deleted: `ls tools/hygiene_gate_next.py` → No such file.
- `HYGIENE_GATE_PATH` read: `git grep` → only `test_hygiene_gate.py:26` and `test_permission_audit.py:26`.
- Siblings negative: `git grep -E "import subprocess as|from subprocess import|\bsp\.(run|Popen)"` over tools non-test → empty.
  The positive control is the same tool's sites grep, which found the known `journal_write.py:603/615/632`.
- RUNBOOK §9.1(f) and §9.8 on main match spec §6.1 text, apart from one line wrap inside a code span.

## Trail

- Read:
  - spec r2 whole; r1 :72-117, :145-190, :304-368
  - `git show 23c9fee3` (gate, tests, permission_audit, RUNBOOK)
  - `tools/hygiene_gate.py` :1200-1212, :1846-1956
  - `git show bac7a9a2`; worktree `tools/test_redundancy.py` :69-98 and `tools/journal_write.py` :594-645
  - `docs/SIBLING_MAP.md:294`
  - narrative `2026-11-17-1500-narrative.md:32-40`
  - critic.md rules 21-24
  - `critic_verdict.schema.json`
- `python -m pytest tools/test_hygiene_gate.py -q` (main) → `337 passed in 15.27s`. This is consistent with the Lead's 422
  together with test_permission_audit.
- `python -m pytest tools/test_journal_write.py tools/test_test_redundancy.py -q` (K-WIN worktree) →
  `103 passed, 6 skipped in 92.09s`.
- Scratch `probe_g1.py`: 40 cases through `wait_loop_forms` + `decide`. The results quoted above are verbatim from it, for example
  `ps-allman silent []`, `bash-sleep-tail silent []`, `incr-in-echo silent []`, `arith-step2-AT deny [('for','C1',7200.0)]`,
  `door-ps-AT silent []`, `door-ps-BEYOND deny [('for','C1',3620.0)]`.
- Scratch `probe_flags.py` (K-WIN vs main): the flag values in F9.
- `powershell -File allman.ps1` → `while-allman:3` / `do-allman:2`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "SIBLING_MAP axis 11 covered by the queued line docs/SIBLING_MAP.md:294 (C1, F-C4, t-120); the second start-word list _BASH_CONT vs _START_WORD_RE is fixed in this round (F5); K-WIN same-artifact sibling tools/test_redundancy.py:90 is unflagged (F8); spawn siblings in tools/ listed by file:line under (c), left to the FW scout question per the Lead decision; PS bracket-matcher neighbours (while/do/for/foreach on the next line) walked under F1",
  "fixes": [
    "F1 tools/hygiene_gate.py:1508,1512,1519 skip newline tokens before an opening brace and before while/until after a do-block; rows W-ps-allman, W-ps-allman-crlf, W-ps-do-allman deny",
    "F2 tools/hygiene_gate.py:1537 do not count redirect targets or fd digits as sleep arguments; :1521 read a parenthesised range before a ForEach-Object pipe; rows for both",
    "F3 tools/hygiene_gate.py:1614 search the masked body for the counter increment; row with a quoted increment deny",
    "F4 tools/hygiene_gate.py:1567 and :1563 read the step of a counted for (i++ or i+=K), else unknown; row for i+=2 at 3600 silent",
    "F5 tools/hygiene_gate.py:1419 build _BASH_CONT and _START_WORD_RE from one tuple",
    "F6 split _wait_loop_forms :1661-1722 (extract the budget computation of finish); one load_under_test helper in tools/conftest.py instead of _gate_under_test copied in test_hygiene_gate.py:23-40 and test_permission_audit.py:23-40, reused by K-STALE and K-WIRE",
    "F7 tools/test_hygiene_gate.py add W-ps-for-AT (180 x 20 silent) and W-ps-for-BEYOND (181 x 20 deny)",
    "F12 G1 exception becomes a visible note (wait loops not checked) instead of a silent empty list",
    "F8 tools/test_redundancy.py:90 add CREATE_NO_WINDOW to the Popen creationflags",
    "F9 tools/test_journal_write.py one parameterised row asserting creationflags has 0x08000000 and lacks 0x8 at _find_bash, _kill_tree and run_witness (owns widened by this file)",
    "F10 tools/test_redundancy.py:73 use the named constant, not the bare literal",
    "F11 the acceptance event of t-1143 carries the builder's verbatim probe output or the critic's flags probe"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-bounded-waits-mechanism-spec-r2.md",
      "docs/tasks/specs/20261117-bounded-waits-mechanism-spec.md:72-117,145-190,304-368",
      "git show 23c9fee3 (tools/hygiene_gate.py, tools/test_hygiene_gate.py, tools/permission_audit.py, tools/test_permission_audit.py, docs/RUNBOOK.md)",
      "tools/hygiene_gate.py:1200-1212,1846-1956",
      "git show bac7a9a2",
      ".claude/worktrees/agent-a6075aef386517b39/tools/test_redundancy.py:69-98",
      ".claude/worktrees/agent-a6075aef386517b39/tools/journal_write.py:594-645",
      "docs/SIBLING_MAP.md:294",
      "docs/tasks/compact-snapshots/2026-11-17-1500-narrative.md:32-40",
      ".claude/agents/critic.md rules 21-24",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -m pytest tools/test_hygiene_gate.py -q (main)", "result": "337 passed in 15.27s"},
      {"command": "python -m pytest tools/test_journal_write.py tools/test_test_redundancy.py -q (K-WIN worktree)", "result": "103 passed, 6 skipped in 92.09s"},
      {"command": "python -B scratchpad/probe_g1.py (40 wait-loop cases via wait_loop_forms and decide)", "result": "ps-allman silent, ps-do-allman silent, bash-sleep-tail silent, ps-range-paren-BEYOND silent, incr-in-echo silent, arith-step2-AT deny 7200; all spec rows and door AT/BEYOND as expected"},
      {"command": "python -B scratchpad/probe_flags.py on K-WIN worktree and on main", "result": "K-WIN 0x8000000/0x8000000/0x8000000/0x8000200, main 0x0/0x0/0x0/0x200, DETACHED unset everywhere"},
      {"command": "powershell -File scratchpad/allman.ps1", "result": "while-allman:3 do-allman:2"},
      {"command": "diff 23c9fee3:tools/hygiene_gate.py 6cf19472:tools/hygiene_gate_next.py", "result": "IDENTICAL"}
    ]
  }
}
```
