# t-1500 -- code review: FG7-89 fix round 3, OF3-1 part f fix round 2

Given: t-1488 review, dispatches d-1493 / d-1494, handoffs t-1493 / t-1494, and the Lead's later answer quoted in this dispatch.
FG7-89: worktree `agent-a9f9317752e5302ac`, commits e3520b38 and 7bc9a5f0 (test file and report) on top of ef9a7947. The `.next` is staged
(index sha256 8c616e26..., the same as the worktree file). I judged it in a scratch tree: `git archive HEAD tools` twice (old / new), with the staged
`.next` written over `hygiene_gate.py` in the new copy only. Live `tools/hygiene_gate.py` sha256 667cb34c...11a3 in the root and in the worktree: untouched.
OF3-1 f: worktree `agent-a349244884c0cb541`. The merge of c54fba00 is staged (round 1) and the round-2 edits are unstaged. I ran three copies through
one exec harness, each with `__file__` = the worktree path: origin/main (base), the index copy (r1) and the working copy (r2).

## Verdict lines

- **FG7-89 round 3: REJECT, failure_class: code. 1 blocker (F1), fixes F2-F4, remarks R1-R3.** t-1488 status: F1 has its 15 forms
  closed (0 deny losses, reproduced), but the invariant behind it is not met. F2 fixed: `env cd`, `nohup cd` and `env pushd` pass, `command cd` and `builtin pushd`
  are refused. F3 fixed: `_HEADS` (`hygiene_gate.py.next:151`) builds `_START_WORDS` (`:165`), and `_WRAPPER_HEADS` is gone. F4 fixed for the named rows.
- **OF3-1 part f round 2: NEEDS WORK. 0 blockers, fixes G8-G9, remarks R4-R6.** G1, G3, G4 and G5 are fixed and verified (below). G2 is fixed:
  R3 in sequence went from 58.3 s to 3.3 s. R4 is fixed in code, but its row does not kill the defect it is for (G8).

## Findings -- FG7-89

**F1 (blocker for placement) -- 27 real runs the live gate refuses now pass the `.next` worker deny.** d-1493's invariant is "no form the
live gate refuses today passes". The Lead's later answer exempts only mentions (echo), unbalanced quotes and a bare `ssh`. The forms below are
real executions: decide is called with `agent_id=a1`. Old = `DENY` (MSG_WORKER_ACCEPT), new = `pass`.
- (a) Unknown child-exec heads, 17 forms: `docker exec c1 python tools/journal_write.py accept t-1`, `watch -n 5 ...`, `stdbuf -oL ...`, `ionice -c3 ...`,
  `taskset 1 ...`, `flock /tmp/l ...`, `doas ...`, `runuser -u x -- ...`, `script -qc "python ... accept t-1" /dev/null`,
  `find . -maxdepth 0 -exec python ... accept t-1 \;`, `parallel ... ::: t-1`, `poetry run ...`, `pipenv run ...`, `conda run -n base ...`, `wsl ...`,
  `strace -f ...`, `uvx python ...`. Cause: `_road_payloads` (`:1392`) returns early for any head that is neither in PAYLOAD_INTERPRETERS nor in `_HEADS`.
  That adds no "unparsed", so an unknown head becomes a pass (FR-41 direction). The builder named `docker exec` in its Question 2.
  The addendum then reports "extra-form losses now 4 vs live", which leaves out the class it had itself named (rule 12: an unsupported negative).
- (b) PowerShell sibling of unparsed class 2, 2 forms: `iex "python ... accept t-1"` and `Invoke-Expression "..."`. `:1395` handles Bash `eval` only,
  and is a name branch in code.
- (c) Arity gaps in listed heads, 4 forms: `time -p python ...` and `command -p python ...` (the SAME_SHELL heads carry no option arity, so the
  command becomes `-p`); `xargs --max-args 1 python ...` and `xargs --arg-file ids python ...` (long flags with a separate value are missing from the table,
  so the value is taken as the command).
- (d) Payload edges, 4 forms: `bash -c -- "python ... accept t-1"` (`:1419` reads `rest[0]`, which is `--`); `bash -c \<newline> 'python ...'` (a line
  continuation is not joined); `bash -c "python ... accept t-1" don\'t` and `bash -c "..." \"`. In (d), `_quotes_balanced` (`:549`) ignores a backslash escape
  outside quotes, calls the statement unbalanced, and returns without "unparsed". Git Bash ran all four shapes (`run1`..`run5` printed, trail).
Fix: the fork is the Lead's. (i) A closed table of MENTION heads (echo, printf, ...), with the raw fallback on any other statement whose raw
hit lies outside a quoted or heredoc-masked span. Here unknown = deny, which keeps every intended gain. (ii) Keep growing the runner table (a list that
never closes, so unknown = pass, as now). In both, fix (c)-(d) as data and parse rules (skip `--`; join `\<NL>`; `_quotes_balanced` honours `\` in the Bash
dialect, or reuses the tokenizer's own unclosed state) and add `iex`/`Invoke-Expression` as an eval row. Add one row per class (a)-(d).

**F2 (fix, Q6/Q12 b) -- name branches and a third quote scanner.** `cmd == "eval"` (`:1395`) and `cmd != "su"` (`:1417`, the `-xc` cluster rule)
are program names written in code, beside a data table that already has `remote` as a row key. `_SSH_VALUE_FLAGS` (`:194`) sits outside its row.
`_quotes_balanced` (`:549`) is a third quote reader beside `_mask_quoted_segments` (`:251`) and `_read_word` (`:439`). Its divergence from them is
the F1 (d) loss. Fix: an `eval`-meaning row key, the cluster rule as a row key, the flag set inside the ssh row, and one unclosed-quote source.

**F3 (fix, Q5 f) -- a pin on constants.** `test_the_head_table_is_the_one_list_beside_the_start_words` (`test_hygiene_gate.py:693`) asserts the
table's literal membership, `positional`, `sub`, the `_START_WORDS` tuple and `not hasattr(hg, "_WRAPPER_HEADS")`. Those are pins on source and
constants (TESTING.md «не пишется»). The behaviour behind them is already checked at the door by `command-cd-same-shell` and `env-cd-child-never-moves`.
Cut the test.

**F4 (fix, Q10) -- payload roads also feed the main-thread COORDINATOR-READ WARN, and nothing names it.** `_coordinator_read_trigger`, r2 -> r3:
`bash -c "git commit -m x"`, `sudo git commit -m x`, `cmd /c git commit -m x` and `ssh h git merge x` go from `None` to `commit`. The comment at `:195`
says the payload is re-read "for `roads` ONLY (a worker's verdict call)". `ssh h git merge` merges on another host, so its WARN is false
(additive, it does not block). Name it with t-1488 F5 at placement, or keep remote payload roads out of the WARN.

**Remarks.** R1: these are gains in the right direction: `& "C:\Python312\python.exe" tools\journal_write.py accept t-1` (PowerShell) and
`"C:/Python312/python.exe" "tools/journal_write.py" accept t-1` are now refused (old pass). R2 (an existing gap, outside this diff): `python \<NL> tools/journal_write.py accept t-1`
and the direct `tools/journal_write.py accept t-1` (shebang `#!/usr/bin/env python3`) pass on BOTH the live copy and `.next`. This deny is the only
guard, so the Lead may open a node. R3: the live-green half of the DoD is void by the Lead. The r2-copy count reproduces: 38 failed = 35 + 3 su/ssh rows.

## Findings -- OF3-1 part f

**G8 (fix, Q5 a/e) -- the R4 row cannot catch a revert of R4.** The row `test_config_migration.py:684` calls `_baseline(BASELINE_PATH.with_name("gone.json"))`
directly. It never passes through R3's own read at `:680`. Put back round 1's `json.loads(BASELINE_PATH.read_text(...))["no_script_reader"]` at
`:680-682` and the row stays green. It also asserts the same helper text the existing R2 row asserts at `:646` (via `read_gaps` -> `_baseline`). Fix:
make the R3 read a function of the path (`reader_exempt(path)`), call it on the missing path, and expect a named red.

**G9 (fix) -- `slow_tests.json:21` was edited by hand with a number from a different metric.** The file's own reader says the numbers are the nightly
`--jobs 4` CI durations, rewritten by `--slow-tests --update`, "so nobody edits it by hand" (`selftest.py:1079-1091`). Its header says
`source: selftest.txt` and `measured_on: 2026-11-17`. 63.7 is one local whole-file run on a loaded machine, set against 18.2 from CI. Here, in one session: base 33.1 s ->
r2 52.3 s (x1.58). The file was already listed, and the dispatch edge was "in slow_tests.json if over its threshold", so the list does not change. The
edit only skews a `--shard` weight. Fix: revert the line; the nightly `--update` records it.

**Remarks.** R4 (G1, as the Lead decided): the drop costs one real triple, 23 -> 22 (`controller.py:stop_after:pipeline`). The cause is the
`try: config = load_config() or {} except: config = {}` idiom. An empty-literal fallback cannot make a false red, so keeping the binding across `{}` is
an option for the Lead. R5: the merge and the round's edits are uncommitted (the commit gate needs a features.json row, the Lead's). The handoff
`t-1494-of3-1f-r2.md` is untracked. R6: hygiene is clean. Cyrillic is 0 in all three files (control `абв` -> 3). CRLF is kept (autocrlf true, 2182/2182).

**Dispatch question 1 (the slowdown).** It is not this round's. Round 1 caused it and round 2 halved it. Same machine, same session, the whole file through
main()'s order: base 33.06 s, r1 106.75 s (R3 58.26 s, R2 15.94 s), r2 52.28 s (R2 14.01 s, R3 3.30 s). Alone, cold cache: r1 R2 12.65 s / R3 55.87 s;
r2 R2 13.55 s / R3 14.04 s; knowledge_rows 0.02 s. What remains (+19 s) is one parse of the 282 scripts, 18,009,803 bytes: `ast.parse` takes 13.56 s, the walk 2.30 s.
This is inherent to an AST scan of the tree. A text prefilter would trim it, not remove it (R2: 159 files / 15.2 MB, parse 7.77 s, separate run, loaded machine,
an estimate). No fix is owed under G2. The builder's 63.7-80.5 s figures are a loaded machine, not the code.

**Dispatch question 2 (the witness).** The DoD's pytest node ids cannot run. `pytest ...::knowledge_rows --collect-only` gives "no tests collected in
1.25s", so this is a dispatcher defect, not the builder's. The script run is the file's canonical form (docstring "Runnable on its own"; TESTING.md
«замер прогона скрипта»). But the whole-file run is a SLOW_TESTS file (the batch canon's), and `run3.py` (functions alone) is neither attached
nor quoted verbatim. So the witness alone is NOT enough. With my re-run it holds: knowledge_rows 8 pass / 0 fail, R2 8/0, R3 7/0, and whole file
648 checks / 0 fail (the builder's 648/648 matches).

**Verified fixes.** G1: the probe gives r1 `[zz_direct, zz_guarded, zz_inherited, zz_reassigned, zz_shadowed_param]` and r2 `[zz_direct, zz_inherited]`.
G4: the probe with `zz_direct` given a row gives r1 three other reds and no stale line, and r2 exactly `outer:zz_direct: a stale baseline line`. So
the row kills r1. G5: r2 gives `['probe.py:parent_only']`, and the mutant `_wanted |= parent` gives `[]`, so the row kills it. G3: the reasons match the
Lead's text. `readiness.py:1073-1079` reads `absent_means` from the keys table. G2: `_parsed`/`_funcs` (one parse, one map) behave the same as round 1's
`_named_in` (union over same-named defs, nested strings counted in the enclosing defs, module constants by name).

## Standing questions

- Q1 fit: FG7-89 fails d-1493's invariant (F1). OF3-1 meets G1-G5 and R4 in code; the R4 row is G8.
- Q2 builder decisions: FG7-89: unknown head -> pass is unsafe (F1 a). OF3-1: the cache key (path, mtime_ns, size) is safe for these probes.
  A three-key `_baseline` now makes R2 red on a baseline with no `no_script_reader`: one file, one schema, acceptable.
- Q3 seams: FG7-89 touches the copies only. OF3-1 touches test files and the fixture; config-keys.json is unchanged in round 2.
- Q4 class: the deny across heads, dialects, arity and payload shapes was walked (F1 a-d). The PowerShell sibling of eval is F1 b. OF3-1: R2/R3 stale symmetry is now true.
- Q5 tests: FG7-89: F3. The 38 rows kill r2 (measured). Rows for F1 a-d are missing (part of F1). OF3-1: G8. Budget: in limits on both nodes.
- Q6 duplication: F2 (third quote scanner). OF3-1: none found (grep of `_parsed|_tree_of|_TREES|parse_cached` over scripts/: no shared cache to reuse).
- Q7 quality: `_road_payloads` is about 37 lines, `_strip_heads` about 30, `_funcs` about 25, nesting at most 3. The F4 comment is untrue.
- Q8 hygiene: clean (R6). The `.next` is LF, the same as the index.
- Q9 ratchets: none touched. The knowledge baseline has 2 lines and 3 entries, no raise.
- Q10 architecture: AR-1 (the worker-verdict guard) is touched, unnamed. F4 widens the WARN. VARIETY: on a project that uses docker, poetry or conda
  wrappers, a worker's verdict passes silently. No stage stops, but the guard is gone.
- Q11 judgment: none. Q12 one road: F2 (name branches in code instead of data rows). No exclusions remain.

## Trail

- FG7-89: `git -C <wt> diff --cached` (260 lines, read in full). `hygiene_gate.py.next:500-513, 1336-1392, 2117-2140, 2141-2150, 2235-2260, 251-281`.
  `test_hygiene_gate.py` diff `origin/main...HEAD`.
- `python -B <scratch>/t1500/dprobe.py <scratch>/t1500 b15.txt` -> `losses 0 gains 0` (15 of 15 DENY on both). `b2.txt` (66 forms) -> `losses 31 gains 1`.
  The 31 split into 5 mentions (intended), 1 not a real run (`ssh -tt h -- ...`) and 25 counted in F1. `b3.txt` adds `Invoke-Expression` as a LOSS. A separate run gives `bash -c \<NL> '...'` DENY -> pass.
- Git Bash: `bash -c -- 'echo run1'; bash -c "echo run2" don\'t; bash -c 'echo run3 $0' \"; time -p echo run4; command -p echo run5` printed run1-run5.
- `python -m pytest <scratch>/t1500/new/tools/test_hygiene_gate.py -q` (`.next` as hygiene_gate.py) -> `473 passed in 14.56s`.
  With `HYGIENE_GATE_PATH=<r2 copy>` -> `38 failed, 435 passed in 16.94s`.
- OF3-1: `git -C <wt> diff` (317 lines, read in full). `harness.py:100-135, 225-240`, `selftest.py:40-52, 1079-1100`, `controller.py stop_after`, `readiness.py:1073-1082`.
- `tcm_time.py`: the whole file base / r1 / r2 = 33.06 / 106.75 / 52.28 s, all checks pass (633 / 642 / 648). Alone: the figures above.
- `of3probe.py`: G1 / G4 / triples 23 -> 22. G5 mutant probe. Parse-cost probe: `files 282 bytes 18009803 parse 13.56s walk 2.30s`.

```json
{
  "verdict": "blocker",
  "blockers": [
    "FG7-89 F1: 27 real executions the live gate refuses pass the .next worker deny: unknown child-exec heads (docker exec, watch, stdbuf, ionice, taskset, flock, doas, runuser, script -c, find -exec, parallel, poetry/pipenv/conda run, wsl, strace, uvx), PowerShell iex/Invoke-Expression, time -p / command -p / xargs long flags with a separate value, bash -c --, a line continuation after -c, an escaped quote outside quotes (hygiene_gate.py.next:1392-1420, :549); breaks the d-1493 invariant outside the Lead's mention/unbalanced/bare-ssh exemptions"
  ],
  "fixes": [
    "FG7-89 F2: eval and su name branches (:1395, :1417), _SSH_VALUE_FLAGS outside its row (:194), _quotes_balanced a third quote scanner (:549) whose escape divergence causes F1 d",
    "FG7-89 F3: cut test_the_head_table_is_the_one_list_beside_the_start_words (test_hygiene_gate.py:693), a pin on constants; behaviour already covered by the cd door rows",
    "FG7-89 F4: payload roads also raise the main-thread COORDINATOR-READ commit WARN (bash -c git commit, ssh h git merge) while the comment at :195 says roads for the worker deny only; name it at placement or keep remote payloads out",
    "OF3-1 G8: the R4 row (test_config_migration.py:684) calls _baseline directly and survives a revert of R3's read at :680; route it through R3's read",
    "OF3-1 G9: revert the hand edit slow_tests.json:21 (63.7, a loaded local whole-file run set against a CI --jobs 4 metric; the file is rewritten by --slow-tests --update only, membership unchanged)"
  ],
  "class_completeness": "FG7-89: the worker deny walked across head kinds (listed / unlisted / same-shell with options), dialects (Bash eval vs PowerShell iex), arity (long flags with a separate value) and payload shapes (--, continuation, escaped quotes, nesting, heredoc, here-string, pipe); the 15 named forms are closed, 4 classes stay open (F1 a-d). The main-thread WARN, a sibling consumer of roads, was walked (F4). OF3-1: R2/R3 stale symmetry is now true; the G1 drop's cost was measured on the real tree (23 -> 22 triples).",
  "trail": {
    "read": [
      "docs/tasks/specs/reviews/t-1488-fg7-89r2-of3-1f-code.md",
      "scratchpad/d-1493.txt, scratchpad/d-1494.txt",
      ".claude/worktrees/agent-a9f9317752e5302ac/docs/tasks/handoffs/t-1493-fg7-89-r3.md",
      ".claude/worktrees/agent-a349244884c0cb541/docs/tasks/handoffs/t-1494-of3-1f-r2.md",
      "agent-a9f9317752e5302ac: git diff --cached tools/hygiene_gate.py.next (full); hygiene_gate.py.next:251-281,500-513,1336-1392,2117-2150,2235-2260; test_hygiene_gate.py diff origin/main...HEAD",
      "agent-a349244884c0cb541: git diff of test_config_migration.py, knowledge-read-baseline.json, slow_tests.json (full); test_config_migration.py:425-462,630-650; harness.py:100-135,225-240; readiness.py:1073-1082; controller.py stop_after",
      "ai-packages/qa-factory/scripts/selftest.py:40-52,1079-1100; docs/TESTING.md:105-140,225-240"
    ],
    "reruns": [
      {"command": "python -B scratch/t1500/dprobe.py scratch/t1500 b15.txt (decide, agent_id a1, live vs .next)", "result": "15 of 15 DENY on both; losses 0 gains 0"},
      {"command": "python -B scratch/t1500/dprobe.py scratch/t1500 b2.txt and b3.txt (own forms)", "result": "b2 losses 31 gains 1 (5 mentions intended, 1 not a real run, 25 real); b3 Invoke-Expression LOSS; bash -c line continuation LOSS"},
      {"command": "python -m pytest scratch/t1500/new/tools/test_hygiene_gate.py -q (.next overlaid in scratch copy)", "result": "473 passed in 14.56s"},
      {"command": "HYGIENE_GATE_PATH=r2 copy python -m pytest scratch/t1500/new/tools/test_hygiene_gate.py -q --tb=no", "result": "38 failed, 435 passed in 16.94s"},
      {"command": "python -B scratch/t1500/tcm_time.py tcm_{base,r1,r2}.py (whole file, main order)", "result": "33.06s / 106.75s / 52.28s; 633/642/648 checks, 0 fail"},
      {"command": "python -B scratch/t1500/tcm_time.py tcm_r2.py <function> (alone)", "result": "knowledge_rows 0.02s 8/0; knowledge_reads_have_rows 13.55s 8/0; knowledge_rows_have_readers 14.04s 7/0 (r1: 12.65s / 55.87s)"},
      {"command": "python -B scratch/t1500/of3probe.py + G5 mutant probe", "result": "G1 r1 5 keys -> r2 2; G4 r2 exactly one stale red; G5 mutant -> []; real-tree triples 23 -> 22"},
      {"command": "python -m pytest <wt>/.../test_config_migration.py::knowledge_rows --collect-only -q", "result": "no tests collected in 1.25s"}
    ]
  }
}
```
