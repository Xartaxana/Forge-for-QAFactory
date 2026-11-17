# t-971 — targeted plan-critic RE-PASS: «Forge test rules» r2 (fix round t-956 on t-949)

Reviewer: critic (Opus 5.5), 17.11.2026. Scope: only what the fix round changed (B1 -> (a) and stream S-E; B2 and the
S-A1/S-A2 split; the goal-based file rule §4.1), keys K1-K9 of the dispatch. Review only, plus one scratchpad experiment
(no repo write besides this file). My verdict is an INPUT: accepting it, and every change to the spec, is the Lead's call
(critic rule 6).

**Verdict: fit_with_fixes.** Two must-fix items, R1 and R2. Both are text edits the Lead can make in the spec without
another re-pass: neither changes the architecture of B1 -> (a). R1 has to land before S-E is dispatched; R2 before
wave 1 is planned. Eight minor fixes follow (R3-R10).

---

## Must-fix

### R1 — The runner's restore can hang, and a hung runner leaves the tree mutated (K2, K3; §5.3 «Run», E-R1, E-R3, E-P4)
- **What the spec says.** §5.3 gives the run as `timeout TIMEOUT_S = 60`, with «restore in `finally` (timeout
  included)». E-R3 says «the runner kills its direct child only. Invariant: the restore does not wait for it». Today's
  runner calls `subprocess.run(..., capture_output=True, ...)` (`mutate_once.py:41`). The obvious build adds `timeout=60`
  to that call.
- **Why the invariant fails on this platform (win32).** CPython 3.12 `subprocess.py:551-559`: on `TimeoutExpired`,
  `run()` calls `process.kill()` and then, on Windows only, `process.communicate()`. That call waits for EOF on the pipes.
  Any grandchild that inherited the pipes keeps them open, so `TimeoutExpired` reaches the runner's `finally` only after
  the grandchild exits.
- **Witness (experiment in the scratchpad).** `subprocess.run([python, child.py], capture_output=True, timeout=2)`. The
  child starts a grandchild that sleeps 20 s and then sleeps 60 s itself. Output: `timeout raised after 20.2 s (timeout=2)`.
- **Failure scenario.**
  1. A forge test runs a hook by subprocess.
  2. The mutant makes that subprocess loop.
  3. The runner hangs past 60 s, so the restore in `finally` never runs.
  4. The critic's Bash call hits its own timeout (default 120 s) and the tool kills the runner. TerminateProcess skips
     `finally`.
  5. The target is left MUTATED in the builder's tree. No sha line is printed and no `restore-mismatch` is reported. The
     next fix-round builder in that tree commits the mutant.
- **Minimal fix**, written into §5.3 and E-R3:
  - (a) Run the child with `Popen`, with stdout and stderr sent to a temporary FILE, not to pipes. Call
    `wait(timeout=TIMEOUT_S)`. On timeout, `kill()` and restore at once. Read the output file only after the restore.
  - (b) Add a table row for it: «a mutant whose test leaves a grandchild holding the output: restored within
    TIMEOUT_S + 5 s, outcome invalid».
  - (c) Name the hard-kill residual. A runner that is itself killed cannot restore. So (i) the brief tells the critic to
    give the Bash call a timeout above the runner's worst case. (ii) The coordinator's duty before any fix round or merge
    from that tree (E-P5) is `git -C <tree> status --porcelain` → empty. A non-empty status is a stranded probe.

### R2 — Wave 1 brings back B1's contradiction for a whole wave (K1, K6; §8 «Merge waves», §3.2, §3.4)
- **The order.** The brief's probe bullet and the mechanical-layer sentence «The probe below … is the critic's own
  bounded run (CLAUDE.md rule 3)» land in S-A1, wave 1 (§8, wave 1). The CLAUDE.md rule 3 clause, the R11-h line and the
  `handoff_gate` docstring land in S-B, wave 2 (§3.4, §7.4).
- **What wave 2 waits for.** S-B waits for:
  - everything-in-piles D (critic.md 17);
  - architect-tier F (the calibration number);
  - boot-by-topic's CLAUDE.md move (§8 rows).
  S-D waits for everything-in-piles C. So the gap between the waves is open-ended.
- **The conflict in that gap.** The brief orders a probe. `CLAUDE.md:80` still says «a layer not attached → critic asks
  the dispatcher for it and does not execute it». `CLAUDE.md:237` (R11-h) still says the gate «lets it write only that
  file». And the brief's own new sentence cites a rule 3 clause that does not exist yet. That is exactly t-949 B1, as a
  window.
- **§8 misses it.** §8 «Between wave 1 and wave 2» calls the window harmless and names only the check title and the
  unread `mutants` block.
- **Minimal fix** (one of two):
  - (a) Move the brief's «The probe» bullet and the `:14-15` append from S-A1 into S-B's merge. S-A1 keeps q5, but q5 (a)
    then says «by reading» until wave 2.
  - (b) Cut the CLAUDE.md/R11-h/docstring triple out of S-B as its own staged part, landing with wave 1. This is only
    possible if boot-by-topic's CLAUDE.md move has landed; otherwise use (a).
  
  Either way, §8 names the window and what closes it.

---

## Minor fixes

- **R3 (minor, K1; §3.4 rule 3 clause).** «The critic's ONE run of its own is the bounded probe» contradicts other critic
  runs:
  - the next sentence of the same rule (`CLAUDE.md:81-82`: «Money/numeric diffs: critic starts with EMPIRICS —
    control-value runs»);
  - critic.md rule 13 («a probe run against control values»);
  - the probe's own required green control re-run.
  
  Fix the wording: «Beyond the control re-run of what is attached and the empirics of money diffs, the critic's own run
  is the bounded probe … at most the brief's cap of runner calls, through `mutate_once.py`, by Bash, never Write/Edit.»
- **R4 (minor, FR-2, K2; §3.2 E-P5).** «the coordinator restores the file from the branch» names a refused road. The
  rollback refusal of `tools/hygiene_gate.py:21-22` blocks `git checkout/restore/reset --hard/... whose scope has changes
  git status shows`, and a mutated file is such a change. Fix: name the door. Either
  `git -C <tree> show HEAD:<path> > <tree>/<path>` (a shell write to an ordinary file is not refused, `hygiene_gate.py:20`)
  followed by the status check of R1 (c), or a fresh fix-round builder told to restore.
- **R5 (minor, FR-59, K2; §3.2 probe bullet and edges).** Three unknowns are not named as non-passes:
  - (i) A DIRTY tree. The runner restores to the dirty bytes, so the probe tests content that is not on the branch. Add:
    before the first mutant, `git -C <tree> status --porcelain`; non-empty → `mutants_none: "tree dirty: <files>"`. This
    check is the critic's, not the runner's (axis 10 stays n/a).
  - (ii) A tree whose branch predates S-E. `<tree>/…/mutate_once.py` there is today's runner. Given the inline argv
    (`len(argv) != 3`, `mutate_once.py:26-28`), it prints the usage and exits 64 without touching anything. That is safe,
    but no door is named. Fix: call the runner of the critic's own (fresh) checkout with `--root <tree>`, which is what
    `--root` makes possible.
  - (iii) The wording «never … another session's tree». The tree the dispatch names IS the builder session's tree. Fix:
    «only the tree the dispatch names. The dispatcher names it only after the builder has handed back, and starts no fix
    round, merge or worktree removal in it until the verdict returns.» This is a coordinator duty, and today it is
    unnamed: `wave.py merge` removes merged trees (PROJECT «Командная работа» п. 12).
- **R6 (minor, K5; §5.2 F-A).** The green-control join («one `trail.reruns` command without `mutate_once.py`») is
  satisfied by any Grep rerun. t-949's own trail has five such items. So the claim that it «makes a kill on a red baseline
  visible» does not hold. Fix (still shape only): the control rerun's command must contain the `--test` path of the
  probes.
- **R7 (minor, P27/AR-29, K9; §5.2).** «`restore-mismatch`: requires `verdict` = `blocker`» has two problems:
  - Code fixes the role's verdict value.
  - A REJECT of the builder's diff is charged to the builder's attempt counter (CLAUDE.md rule 6: two `rejected` →
    escalation) for a failure of the critic's tool. The branch's commits are untouched, because only the worktree bytes
    differ.
  
  Fix: require `verdict` ≠ `fit` plus a fix line naming the file and the door of R4. Or keep `blocker`, but state that
  such a `rejected` carries `failure_class: tooling` and does not count as the builder's attempt.
- **R8 (minor, K6; §4.5, §8).** Windows not named:
  - (i) S-A1 → S-B. `designer.md:20-23` («a DoD never asks for a new test file outside the keep rows of
    `test-layers.json`») and `builder.md:51-52` contradict the TESTING goal rule. Forge tests have no keep row at all, so
    the designer is told never to place a forge test file. The direction is safe (a question), but the window should be
    named in §4.5.
  - (ii) «S-E first» (§8 wave 1). S-E's new package test file is justified by §4.1 text that has not landed. The live
    TESTING `:117` («новый тестовый файл не создаётся») and the offload-only exception still stand. Fix: S-A1 merges with
    or before S-E, or S-E's critic dispatch names §4.1 as binding.
- **R9 (minor, K7; §4.1 text).** Two criteria have no measure:
  - «не сделав тот файл медленнее»: every added row makes a file slower.
  - «шире по смыслу»: no stated test.
  
  The 10 s criterion has no counting command. Fix:
  - «медленнее» → «не выведя его за его бюджет (10 с, часть разрезанного — 60 с)»;
  - «шире по смыслу» → «дверь случая — не та, что файл уже гоняет (предмет файла назван в его docstring/истории)»;
  - the time → «время — хвост `python -m pytest <file> -q` (`in N.NNs`) или замер прогона скрипта, в отчёте билдера».
  
  The upkeep criterion (`TESTING.md:28-29`) is a retrospective measure. It is fine as the goal, but it cannot decide a
  single case, and the text should not imply it can.
- **R10 (minor, freshness; §5.2, §12 F-D).** The amendment is recorded in everything-in-piles
  (`20261117-everything-in-piles-spec.md:1646-1649`) but not applied yet: C `:255` and A2 `:317` still say «verdict
  predates remarks». The line numbers this spec cites (`:246-247`, `:307-309`) are stale. Fix: cite by text. Order: S-D's
  refusal names a door that only A2's `piles.py` reads. If S-D lands before the amendment and A2 then lands with the
  «remarks» text, the named door does not match (FR-2). Keep F-D's «before A2's dispatch» as a hard order, in the §8 row
  `critic_verdict*`.

---

## Keys

**K1 — the probe and the two-layer rule: answered (R2, R3).**
- `CLAUDE.md:77-80` lets a mechanical layer be «executed by the submitting builder or a script», but it must be
  ATTACHED. The critic may make only a «cheap control re-run of what is attached».
- So a probe is not the allowed re-run. It is a new run, and the rule needs the clause §3.4 adds. With the clause, the
  probe is a script run (the runner) started by the critic: consistent in kind.
- Tool limits are consistent:
  - The critic's `tools:` line is `Read, Glob, Grep, Write, Bash` (`.claude/agents/critic.md:5`).
  - `handoff_gate` is wired on `Edit|Write` only (`.claude/settings.json:43-52`).
  - The only Bash/PowerShell PreToolUse gate is `hygiene_gate` (`:34-38`). Its three refusals (cd, journal, rollback on a
    dirty tree, `hygiene_gate.py:9-22`) do not catch `python -B <abs>/mutate_once.py`.
- Non-contradiction:
  - R3: «one run» versus empirics and the control re-run.
  - R2: the order of landing.
  - The brief's `:14-15` append and critic.md 17/20 are coherent once they land together.

**K2 — safety on a live tree: answered with must-fixes (R1, R4, R5).**
- Byte copy, finally-restore and sha256 are the runner's (`mutate_once.py:32-33, 39-44, 52-54`). The spec keeps them, and
  hygiene pt 7 (c) (the verbatim hash) is met by the printed sha line.
- Timeout: R1 — the restore is NOT bounded on win32 when the test has a grandchild. Witness: 20.2 s against timeout 2.
- Crash between mutate and restore: an unrecoverable residual (TerminateProcess skips `finally`). It is not named. R1 (c)
  names it and gives the detector (`git status` before the next use of the tree).
- Dirty tree and a tree with another live worker: R5 (i), (iii).
- F-B (a) «no tree named → no probe»: named. Every other unknown:

  | Unknown | Status |
  |---|---|
  | slow file | named E-P3 |
  | red control | named E-P9 |
  | timeout | named `invalid` |
  | restore-mismatch | named, door refused (R4) |
  | old runner | not named (R5 ii) |
  | dirty tree | not named (R5 i) |
  | hang past timeout | not named, silent corruption (R1) |

**K3 — today's `mutate_once.py` (read whole, 59 lines; P17 says 60: trivial).**

| Fact | Status | Evidence |
|---|---|---|
| CLI `<spec.json> <mutation id>` | TRUE | `:3, :26` |
| `target`/`test` under `scripts/` | TRUE | `SCRIPTS = Path(__file__).resolve().parent.parent` `:18`, `:31` |
| anchor exactly once, else 64, untouched | TRUE | `:35-38` |
| 64 also on a wrong argc | TRUE (not stated in P17) | `:26-28` |
| byte copy before | TRUE | `:32` |
| run `[sys.executable, "-B", test]` with no timeout | TRUE | `:41` |
| restore in `finally` | TRUE | `:42-43` |
| sha256 before/after | TRUE | `:33, :44` |
| exit 0 on any non-zero test exit | TRUE | `:55` |
| exit 1 survived | TRUE | `:55` |
| exit 2 sha mismatch | TRUE | `:53-54` |
| prints the last summary line, the first 3 FAIL lines, the sha line | TRUE | `:45-52` |
| no reader of the exit outside the package | TRUE (spot) | Grep in §11. P17's «no test file covers it» was not re-run here |

- An extra fact that matters for E-R4: today a wrong mutation id raises `KeyError` (`:30`), which exits 1 = reads as
  «survived». A missing test file gives `python` exit 2 = «killed». The new table turns both into 64. This is a real fix,
  not only a back-compat change.
- What §5.3 assumes about the TIMEOUT path (E-R3) is FALSE on win32 (R1).

**K4 — cost: answered.**
- The cap «3» has its carriers: the rule in the brief (§3.2), the data in the checker (§5.2 maxItems), and the transcript
  count in check (b) (§9 (b)).
- Time: «estimate, not measured», labelled (§6). Worst case 3 × 60 s + one control run, unbounded on win32 until R1 is
  fixed.
- `tools/agent_budget.py:109-116`: `TEST_RUNS_WARN = 10`, `TEST_RUNS_STEP = 5` (a WARN, never a stop).
  - `TEST_RE` matches a runner call through `--pytest` or through a `…/tests/test_x.py` path. So a probe adds at most
    4 counted runs, below the warn.
  - Tokens: each call prints at most 6 lines. That cannot approach WORKER_WARN 250K / STOP 400K (`:109-110`).

**K5 — the verdict schema: answered (R6, R7, R10).**
- Producer and reader move in one merge: critic.md 17 (S-B) with the checker and schema (S-D), E-T1, §8 wave 2. The brief
  (the procedure) is already there from wave 1, so the order is harmless.
- `mutants: []` + `mutants_none` declare the empty outcome for plan and docs gates (E-P1).
- The run join is now non-vacuous: distinct, contains `mutate_once.py`, the result carries `outcome:`.
- The F-A join is vacuous (R6).
- The old-verdict door is field-generic in S-D's own refusal (§5.2). Its reader is A2's `piles.py` (not landed). Until
  then the coordinator reads it by hand (stated, M3 (d)). The amendment is recorded but not applied (R10).
- The current schema requires 4 fields (`tools/critic_verdict.schema.json:7`), and `validate_verdict` hard-codes them
  (`critic_verdict_check.py:73-76`). S-D's ownership of both is right.

**K6 — the S-A1/S-A2 split: answered (R2, R8).**
- The named window S-A1 → S-A2 is correct and closed by S-A2's landing grep (§4.5, §4.4):
  - 7b `:57-59`, RUNBOOK `:115` and 7d versus TESTING;
  - 16 (б).
- Unnamed windows:
  - (1) wave 1 → wave 2: the brief versus CLAUDE.md rule 3 / R11-h (R2, must-fix). It closes at S-B's merge.
  - (2) S-A1 → S-B: designer.md rule 1 / builder.md `:51-52` versus the TESTING goal rule (R8 i). It closes at S-B.
  - (3) «S-E first» versus TESTING `:117` (R8 ii). It closes at S-A1.

**K7 — §4.1 checkable from the text: partly (R9).**
- Named with numbers: 10 s; one world; one parameterised table (plus junction rows); default = a row in an existing
  story, joint or table; keep = bookkeeping.
- Judgment without stated criteria: «медленнее» (no threshold) and «шире по смыслу» (no test).
- The time has no counting command.
- The O-1 owner's word is quoted verbatim and kept: no owner's word for a file, no ban.

**K8 — the 17 rows of §15.**

| Row | Applied? | Place / note |
|---|---|---|
| B1 | partly | §3.2, §3.4, §5.3, §7.1, §7.4 present; landing order re-opens it (R2); clause wording (R3); E-P5 door (R4) |
| B2 | yes (split and order), partly (windows) | §4.5, §7.2, §7.3, §8; R2, R8 |
| F1 | yes, one invariant false | §5.3, §7.1, §1.1; E-R3 on win32 (R1) |
| F2 | yes | §5.2 run join |
| F3 | yes | §5.1 items 3, 5 |
| F4 | yes | §5.1 item 4; lines verified: `_DISPLAY :95`, `SKIP_REFUSED_TEMPLATE :146`, `:271`, `:902-903`, `newly :953`, `still :961` |
| F5 | yes | §8 row `check_cut`, F-C |
| F6 | yes | §0 P16, §6.1; recount 27/123/70 matches |
| F7 | yes | §10.2: 37 labelled lines (Grep `^axis [0-9]* (` = 37 = `^## Axis` 37); not run through `mechanism_gate` |
| F8 | yes | the number only in the brief and §5.2; §2.3, §3.3, §4.4, §9 without it |
| F9 | yes | §4.4 row 16 (б), §7.3 |
| F10 | yes | §2.1 keep needs a named value or invariant; input-derived values; q5 (b) |
| F11 | yes (text), effective only with R1 | §9 (b) transcript count, §5.3 timeout |
| F12 | yes | E-C4, §9 (a) |
| F13 | yes | §5.2 door, §10.1 M3 (d), §12 F-D; application pending (R10) |
| F14 | yes | (i) §7.4 owns scoped; (ii) §4.1; (iii) §2.4; (iv) §5.1 item 6; (v) §9 (b) |
| O-1 | yes, criteria partly | §4.1, §2.5, §3.1 (g); R9 |

**K9 — architecture and principles: answered (R7).**
- AR-4: `--root` is explicit, nothing is stored, outside-root is refused.
- AR-7: the critic picks the places, the equivalence and the FAIL-line reading.
- AR-9: exit-64 messages name the argument that fixes them.
- AR-29: the outcome classes come from the exit code, the summary counts and `compile()` — data. Kept (§1.1, §5.3).
- No exception-name list in code (AR-1, FR-12), and a lazy-import residual is left to the critic: FR-47, P27 kept.
- The one place where code reaches into the role's outcome is the checker forcing `verdict = blocker` on
  restore-mismatch (R7).
- Nothing else new is judged by code: sufficiency, the source and the new-file choice stay with the critic (§1, axis 32
  line).

## Standing lines
- **DUPLICATION AND CONSISTENCY:** none new. The probe has one road (the runner). A one-road grep for the landing is
  specified (§3.4). Grepped: `mutate_once` (spec §11 counts, spot-read), `predates` over the spec, checker and piles.py.
- **CODE QUALITY (plan sketch):** R1 (the timeout path), R6 (a vacuous join).
- **ONE ROAD (P31):** the runner serves package and forge tests alike (`--pytest`). No exclusion without a data row.
- **TESTS:** S-E's new file is justified by the goal rule (§5.3). The time is an estimate, and over 10 s it becomes a
  question. Add the R1 (b) row.

## Not checked
- the mechanism_gate run on the §10.2 block
- whether `refusal_registry.py --check` scans `scripts/tests/`
- the run time of any narrow file
- POSIX behaviour of the timeout path (the `process.wait()` branch, `subprocess.py:560-563`, does not drain pipes:
  likely fine)
- everything-in-piles beyond the grep lines

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "R1 spec 5.3/E-R3: subprocess.run timeout with capture_output hangs on win32 until a grandchild exits (subprocess.py:551-559; witness: timeout=2 raised after 20.2 s); the Bash tool then kills the runner, finally never runs, the target stays mutated with no restore-mismatch -- Popen with output to a temp file, restore before reading output, a table row, and the hard-kill residual with a git status check before reuse of the tree",
    "R2 spec 8 waves: the brief probe bullet lands in wave 1 (S-A1) while the CLAUDE.md rule 3 clause, R11-h and handoff_gate docstring land in wave 2 (S-B, open-ended wait) -- B1's contradiction for a whole wave; move the probe bullet into S-B's merge or land the CLAUDE.md triple with wave 1, and name the window"
  ],
  "fixes": [
    "R1 runner: Popen + file output + restore before drain; grandchild row; hard-kill residual and git status check (E-P5)",
    "R2 land the probe bullet and the rule 3 / R11-h / docstring triple in one merge; name the window in section 8",
    "R3 rule 3 clause wording: beyond the control re-run and money empirics, not 'one run of its own'",
    "R4 E-P5 restore door: git checkout/restore on a dirty path is refused by hygiene_gate; name git show HEAD:path redirect or a builder restore",
    "R5 name non-passes: dirty tree (mutants_none), old runner in a pre-S-E tree (use the critic's own checkout runner with --root), the tree is the dispatched builder tree held by the coordinator until the verdict",
    "R6 F-A control join must contain the probes' --test path, not any rerun",
    "R7 restore-mismatch: verdict not fit plus a fix line, or blocker recorded as failure_class tooling not counted as the builder's attempt",
    "R8 name windows S-A1 to S-B (designer.md rule 1, builder.md 51-52) and S-E before S-A1 (TESTING 117)",
    "R9 section 4.1: slower = past the file's budget; wider = a door the file does not already drive; time measured by the pytest tail",
    "R10 cite everything-in-piles by text (now :255, :317); keep F-D before A2 dispatch as a hard order in section 8"
  ],
  "class_completeness": "Surface: the probe's process lifecycle (timeout, kill, restore) -- walked: timeout (R1), hard kill (R1 c), dirty tree (R5 i), stale runner (R5 ii), concurrent tree use (R5 iii), restore door (R4). Surface: landing windows -- walked all four (S-A1/S-A2 named; wave1/wave2, S-A1/S-B, S-E/S-A1 not). Axes 1, 10, 13, 17, 31, 32, 34 consulted; axis 10 kept n/a by putting the git status check on the critic, not in the runner. Fix-table rows 17/17 checked.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-forge-test-rules-spec.md (whole)",
      "docs/tasks/specs/reviews/t-949-forge-test-rules-plan.md (whole)",
      "ai-packages/qa-factory/scripts/tests/mutate_once.py (whole)",
      "CLAUDE.md:70-84, 235-237",
      ".claude/agents/critic.md:1-8",
      ".claude/agents/designer.md:18-24",
      ".claude/agents/builder.md:49-53",
      "docs/tasks/critic-diff-brief.md:1-50",
      "tools/handoff_gate.py:1-20",
      ".claude/settings.json:30-100",
      "tools/hygiene_gate.py:1-29 (+ grep)",
      "tools/agent_budget.py:100-140",
      "tools/critic_verdict.schema.json (whole)",
      "tools/critic_verdict_check.py (grep required)",
      "tools/dispatch_manifest.py:95,146,271,902-903,953,961",
      "docs/TESTING.md:20-32, 112-132",
      "docs/SIBLING_MAP.md (axis headings)",
      "docs/tasks/specs/20261117-everything-in-piles-spec.md:255,317,1644-1650",
      "Python312/Lib/subprocess.py:551-567"
    ],
    "reruns": [
      {"command": "python -B scratchpad/probe.py scratchpad/child.py (subprocess.run capture_output timeout=2, grandchild sleeps 20 s)", "result": "timeout raised after 20.2 s (timeout=2)"},
      {"command": "grep -ciE rejected.*spec.*(test|pin|тест) logs/journal/dev1.jsonl; rejected count; spec count", "result": "27; 123; 70 (matches spec P16)"},
      {"command": "grep -c ^## Axis docs/SIBLING_MAP.md; grep -c ^axis [0-9]* ( spec", "result": "37; 37"},
      {"command": "grep -n predates everything-in-piles spec, critic_verdict_check.py, piles.py", "result": "spec :255, :317 still 'predates remarks'; amendment recorded :1646-1649; none in code"}
    ]
  }
}
```
