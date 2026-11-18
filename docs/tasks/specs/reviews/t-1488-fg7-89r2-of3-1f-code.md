# t-1488 -- code review: FG7-89 fix round 2, OF3-1 part f

Given: t-1485 review, t-1473 and t-1486 handoffs, FG7-89 card, t-129 spec (item 3b, section 4), the Lead decisions 1-3 written in the dispatch.
FG7-89: diff `b3af6b35..a7d506a7` (`tools/hygiene_gate.py.next`, `tools/test_hygiene_gate.py`), as merged in `f6f1c916`. I judged it in a scratch
tree: `git archive f6f1c916 tools` twice (old / new), and `hygiene_gate.py.next` copied over `hygiene_gate.py` in the new copy only.
No live file was touched: the live `tools/hygiene_gate.py` sha256 is 667cb34cd56fe0a8, the same as the old copy. OF3-1 f: `origin/main...HEAD` in worktree
`agent-a0f9ed3ddef0c0c8a` (5c3f8318, c54fba00).

## Verdict lines

- **FG7-89 round 2 (a7d506a7 / f6f1c916): REJECT, failure_class: code. 1 blocker (F1), fixes F2-F4, remark F5.**
  The `.next` copy must not be placed as it is. t-1485 status: F1 fixed (`docs/SIBLING_MAP.md:341` holds both `lead_calls` and `lines_back_to`).
  F2 fixed (the row body now carries `python -B tools/...`). F3 fixed (`_PYTHON_PROGRAM_RE` is gone; `_cmd_name` lower-cases, so losing
  IGNORECASE costs nothing). F4: one recogniser, and the heredoc/quoted false positive is closed (t-1479 R2). But F4's own premise, "so
  the deny loses nothing", was MY claim in t-1485, and it is false. That is F1 below (a calibration case against t-1485).
- **OF3-1 part f (5c3f8318, c54fba00): NEEDS WORK. 0 blockers. Fixes G1-G7, remarks R1-R6.** The counts are verified: 25 rows, 37 entries
  removed, 13 added. The three functions are green when called alone (17/17).

## Findings -- FG7-89

**F1 (blocker for placement) -- the worker deny loses refusals the live gate makes today.** The deny moved from `_worker_verdict_call`
(dod_track's program regex over the RAW text) to `"verdict" in sig["roads"]` (`hygiene_gate.py.next:1995`). `roads` sees only
statement-start words after the quote mask, plus `env`/`nohup` heads. I probed old `_worker_verdict_call` against new `roads`, then
`_decide_command(agent_id="a1")`. These forms are denied live and PASS on the `.next` copy:
`bash -c "python -B tools/journal_write.py accept t-1"`, `sh -c '...reject...'`, `cmd /c python tools/journal_write.py accept t-1` (unquoted),
`powershell -Command "..."` (PowerShell), `sudo python ...`, `timeout 60 python ...`, `exec python ...`, `nice -n 5 python ...`,
`xargs python ... < ids`, `uv run python ...`, `env -u FOO python ...`, `env -C /tmp python ...`, `env -S '...'`, and
``echo `python ... accept t-1` ``: 15 forms. Decide output: old `timeout 60 ...` -> "an acceptance or rejection is written by the
coordinator's main chain...", new -> `pass`. The same for `bash -c "..."`. This deny is the only guard: `tools/journal_write.py` has no agent
check (grep `agent_id|worker` there: only `delegated/returned` text). The other `WORKER_VERDICT_VERBS` users are the two gate copies only.
The rollback deny loses nothing: every rollback delta in the battery is 0->1 or equal, and the 422-row hygiene table is green on the copy.
Fix (the Lead picks one): (a) the walker reads the payload of the `PAYLOAD_INTERPRETERS` rows bash/sh/cmd/pwsh (`:151-158`) for `roads`
only, and the wrapper heads become a data table with their arity (`timeout <dur>`, `nice -n N`, `sudo`, `exec`, `xargs`, `uv run`,
env `-u NAME`/`-C DIR`/`-S STR`); or (b) the deny keeps a raw-text fallback for the forms the walker cannot see, and is narrowed only
for heredoc bodies and quoted arguments of non-interpreter commands. Either choice needs a row per lost class (F4).

**F2 (fix) -- `env cd /tmp`, `nohup cd /tmp` and `env pushd /tmp` are now refused, a false refusal.** The stripped `cmdwords` feed `_cd_class`
(`:1256-1263`). But `env` and `nohup` exec a CHILD program, so a `cd` behind them never moves the shell. Decide: old `pass`, new "the
shell's working directory must not move". The report calls this "more refusals only", and here it is wrong: the gate's own invariant
is "no refusal on a target the gate could not resolve" (`:33`), and this refuses a certain non-move. Fix: no cd class behind a wrapper head.

**F3 (fix, Q6) -- a second statement-head list.** `_WRAPPER_HEADS` (`:1955`) sits 1800 lines from the walker that reads it (`:1256`).
`_START_WORDS` (`:135`) calls itself "the ONE list" of words after which a command starts again. The two lists differ in meaning:
`builtin`/`command`/`time` run the next word in the shell, while `env`/`nohup` exec a child. The code states neither, and F2 comes from that
confusion. Fix: put the table next to `_START_WORDS`, with the child-process meaning and the arity (F1 a) in the data.

**F4 (fix, Q5 c) -- new behaviour at a door with no row.** The new refusals behind a head have no row: `nohup tee out.txt` -> write
target, `env sed -i s/a/b/ f.txt` -> write target, `env tee logs/journal/x.jsonl` -> journal deny. The 15 lost forms of F1 have no row
stating the decision either. The rows added for `env-head`/`nohup-head` in `WORKER_VERDICT_ROWS` pass on the live code too (raw regex), so
they kill nothing there. They only pin the new road. The rollback `env-head-*` rows do kill (old 0 forms).

**F5 (remark, the Lead's placement commit)** -- a7d506a7 says `axes: not a mechanism (WARN only; gate copies stay .py.next)`. The round
changes a deny recogniser and the walker's cd/write/rollback classes. At placement, axis 11 and the refusal-class change must be named.

## Findings -- OF3-1 part f

**G1 (fix) -- R2 goes red on a non-config object. This breaks section 4's invariant ("never a false red on a non-config object"), and the
docstring says the opposite.** `knowledge_reads` (`test_config_migration.py`, `visit`) passes `bound` into nested defs and never drops a
name. Probe file: `def outer(root): cfg = load_config(root); def inner(cfg): return cfg.get("zz_shadowed_param")`, plus
`cfg = load_config(root); cfg = {...}; cfg["zz_reassigned"]`. The scan gives `('mod_a.py','inner','zz_shadowed_param')` and
`('mod_a.py','reassigned','zz_reassigned')`, which become two R2 reds. The docstring says "BLIND TO (a miss, never a red): an alias or
reassignment". Fix: a nested def parameter, and a non-config assignment to a bound name, remove it from `bound` for that scope (the miss direction).

**G2 (fix, Q5 f/g) -- the run time.** In the worktree, alone: `knowledge_reads_have_rows` takes 7.18 s and `knowledge_rows_have_readers` 44.83 s.
`scripts/slow_tests.json:21` records the whole file at 18.2 s. The cause: `_named_in` re-walks the whole tree for every `needed_by` entry,
and walks all 282 scripts for each `no_script_reader` key. R2 and R3 also parse the tree twice. The report gives no time. Fix: parse once and
build one per-file map `{function: strings + constant strings}`.

**G3 (fix) -- a `no_script_reader` reason that its carrier contradicts.** `format_changed -- the roles run the command`. No role text names
the key. `git grep -l -i format_changed origin/main -- agents/ references/slices/ skills/` finds only the onboarding writers
`p2-interview.md`/`p4-generate.md`. Spec section 7 N-r8 (owner 12.11.2026) says it "has no reader in code or role texts", and its node is
OF4-30 (`plans/piles/onboarding-forge/batch-4-...md:60`). The reason must say "no reader yet | node OF4-30", not invent a role reader.
`dod -- the roles read it` has no role-text carrier: `git grep -w -i dod` over agents/slices/common-rules finds 0, and the positive control
`pii_and_masking` with the same form finds 3 files. Its old entry `readiness.py:_optional_top_keys` reads it through the keys table
(`absent_means`), a script reader that rule (b) cannot see. Name that in the reason.

**G4 (fix, the Lead's word decides) -- R2's "stale" never forces the baseline to shrink.** `stale = listed - seen`, where `seen` is every
scanned triple. Probe: I added a `journal_legacy_tasks` row (the named follow-up) and kept its baseline line, and `read_gaps(...)` returned `[]`.
The line stays green for good, while the `no_script_reader` side reds a line that is no longer needed. This matches Lead decision 2 word for
word, but it does not match "shrink-only". Proposal: stale = a line whose triple is no longer a gap. The decision is the Lead's.

**G5 (fix, Q5 a/c) -- Lead decision 1's parent-only rule has no row.** No R3 control names a function that holds only the parent
(`environment` for `environment.env_file`). The probe functions (`roster`, `contract.py:cases_root`: strings `'', docstring, 'cases_root',
'test-cases'`) hold no parent segment. So the mutation `want |= {key.split(".")[0]}` survives every control. Fix: one probe entry.

**G6 (fix, Q9, outside owns)** -- the new shrink-only ratchet `knowledge-read-baseline.json` is not in SIBLING_MAP axis 18's member list
(`docs/SIBLING_MAP.md:400`). `git grep -i knowledge-read-baseline origin/main -- docs plans tools` finds specs/reviews only. The positive control
`env-facts-baseline` finds `:225`. Without the entry, a later raise goes unnamed. The Lead adds it at merge. No raise in this diff: 2 lines and
3 entries, as decided.

**G7 (fix or node, Q6)** -- a second scanner of config reads. `test_config_projection.config_reads` (K-G1, receiver table `RECEIVERS` at
`:125-134`: `cfg`, `full_cfg`, `ctx.cfg`, `self.cfg`...) already lists the names that hold the config. R2's `carriers` is `[]`. So R2 sees 23
triples in total, and the two tables can drift apart. Seed `carriers` from that table, or the Lead opens a convergence node. The spec did not
name K-G1. My probe with the spec's own example `env_probe.data_cleanup:full_cfg` adds one `environments` triple and no red, so nothing is hidden today.

**Remarks.** R1: R2 finds `run_counters.py:_friction` reading `cost`, and that function is not in `cost.needed_by`. Section 2 says needed_by =
every reader R2 finds, and nothing checks that direction. R2: the handoff says "5 replaced", but 13 entries were added (all 13 are listed in
the swaps). R3: the commit line "AR-22 -- no catalogue row survives that no script names" leaves out the 3 exempt rows. R4: a missing baseline
in `knowledge_rows_have_readers` raises a traceback (loud) instead of a named red like R2's. R5: `_named_in` matches an attribute name to
THIS module's constant (`other.CONFIG_KEY`). The 16 entries that rely on the constant path all use key-specific constants (`ROLES_KEY`,
`SIGN_IN_KEY`, `JUDGE_TEST_DATA_KEYS`, ...), so the builder's decision holds. R6: CRLF is kept, there is no Cyrillic (control `абв` -> 1), and the
fragment name matches siblings a-e.

## Standing questions

- Q1 fit: FG7-89, E14 is met for the WARN. The deny side fails (F1). OF3-1 f: item 3b and decisions 1-3 are implemented. Gaps: G1 (section 4 invariant),
  G3, G4.
- Q2 builder decisions: the constant path holds (R5). `carriers: []` is safe today (G7). Wrapper stripping before `_cd_class` is unsafe (F2).
- Q3 seams: FG7-89 is copies only. OF3-1 changes only `needed_by` values (a script compared every other field: none changed, key order identical) and one `fixture_owners` line.
- Q4 class: worker deny vs rollback deny vs WARN, all three walked (F1). The R2/R3 asymmetry (G4).
- Q5 tests: F4, G2, G5. The R2/R3 controls kill the named defects (missing file, missing function, non-naming function, empty list, three exempt reds, bypass).
- Q6 duplication: F3, G7. Q7 quality: the G1 docstring is untrue. `reader_gaps` is about 35 lines and `visit` nests 3 levels: within limits.
- Q8 hygiene: clean (R6). Q9 ratchets: G6. No raise elsewhere (census, `known_red` untouched).
- Q10 architecture: OF3-1 names AR-13/20/22 (R3 wording). FG7-89: AR-1 is the worker-verdict guard, touched and not named (F1, F5).
  VARIETY: on a Windows/cmd or wrapper-using project, the factory loses a refusal and adds no block. Not a stage stop.
- Q11 judgment: none. These are detectors over data, with no census rows. Q12 one road: none found. The exempt list is a data row with a reason; `TEST_DATA_READER` is named by the spec.

## Trail

- `git -C <root> diff b3af6b35 a7d506a7 -- tools/hygiene_gate.py.next tools/test_hygiene_gate.py`. Read `hygiene_gate.py.next` `:128-175, 460-466, 1216-1300, 1855-2030`.
  `dod_track.py:232-262`. Card `:50-56, 92-100, 140-150, 269-273`.
- Scratch `.../scratchpad/{old,new}/tools`. Probes `probe.py` + `cases.txt` (63 rows) + `cases2.txt` (16) + decide check: verbatim deltas above.
- `python -m pytest <scratch>/new/tools/test_hygiene_gate.py <scratch>/new/tools/test_coordinator_rules.py -q` -> `448 passed in 9.90s`.
- OF3-1: `git -C <wt> diff origin/main...HEAD` (all 4 package files). Spec `:298-326, 345-362`. `test_config_projection.py:120-175`. `slow_tests.json`.
- `python -B <scratch>/of3run.py <wt>/.../scripts/tests` -> `=== of3-1f three functions: 17/17 ok ===` (elapsed 51.44s). Timing run: `knowledge_rows 0.02s`,
  `knowledge_reads_have_rows 7.18s`, `knowledge_rows_have_readers 44.83s`.
- needed_by diff script: `rows changed 25 removed 37 added 13 reorder-only 0 keys same: True True`.
- R2 reverse/carrier/shadow/stale probes: outputs quoted in R1, G7, G1 and G4.

```json
{
  "verdict": "blocker",
  "blockers": [
    "FG7-89 F1: the hygiene_gate.py.next worker deny (roads, :1995) passes 15 forms the live deny refuses (bash -c / sh -c / cmd /c / powershell -Command payloads, sudo, timeout, exec, nice, xargs, uv run, env -u/-C/-S, backticks); journal_write.py has no agent check of its own; do not place the copy as is"
  ],
  "fixes": [
    "FG7-89 F2: env/nohup cd and pushd are refused although a child process never moves the shell; no cd class behind a wrapper head (hygiene_gate.py.next:1256-1263)",
    "FG7-89 F3: _WRAPPER_HEADS (:1955) is a second head list beside _START_WORDS (:135); one data table with child-process meaning and arity",
    "FG7-89 F4: rows for wrapper-head write and journal refusals and for each lost F1 class",
    "OF3-1 G1: R2 false red on a shadowing nested param and on a reassigned bound name; docstring says never a red",
    "OF3-1 G2: R3 44.8 s and R2 7.2 s alone; parse once, one per-file string map",
    "OF3-1 G3: no_script_reader reasons for format_changed (contradicted by spec section 7 N-r8, node OF4-30) and dod (no role carrier; readiness reads it by table)",
    "OF3-1 G4: R2 stale line = triple not found, so a line whose key gained a row stays green; the Lead decides",
    "OF3-1 G5: no R3 control for the parent-only rule of Lead decision 1",
    "OF3-1 G6: add knowledge-read-baseline.json to SIBLING_MAP axis 18 members (docs/SIBLING_MAP.md:400), the Lead at merge",
    "OF3-1 G7: R2 carriers vs test_config_projection RECEIVERS (:125-134): seed from it or open a convergence node"
  ],
  "class_completeness": "FG7-89: the three consumers of the walker roads and forms (worker deny, rollback deny, COORDINATOR-READ WARN) walked; rollback loses nothing, deny loses 15 forms (F1), cd class gains a false refusal (F2). OF3-1: R2 vs R3 stale semantics asymmetric (G4); second config-read scanner named (G7); ratchet axis 18 entry missing (G6).",
  "trail": {
    "read": [
      "docs/tasks/specs/reviews/t-1485-fg7-89-fg7-86-fg7-81b-code.md",
      "docs/tasks/handoffs/t-1473-fg7-89.md",
      "docs/tasks/specs/20261118-fg7-89-coordinator-rules-read-card.md:50-56,92-100,140-150,269-273",
      "tools/hygiene_gate.py.next:128-175,460-466,1216-1300,1855-2030",
      "tools/dod_track.py:232-262",
      "tools/test_hygiene_gate.py (diff b3af6b35..a7d506a7, WORKER_VERDICT_ROWS)",
      "docs/tasks/specs/t-129-of3-1-knowledge-catalog.md:298-326,345-362",
      "worktree agent-a0f9ed3ddef0c0c8a: diff origin/main...HEAD of test_config_migration.py, knowledge-read-baseline.json, test-layers.json, config-keys.json, changelog.d",
      "ai-packages/qa-factory/scripts/tests/test_config_projection.py:120-175",
      "ai-packages/qa-factory/scripts/slow_tests.json"
    ],
    "reruns": [
      {"command": "python -m pytest <scratch>/new/tools/test_hygiene_gate.py <scratch>/new/tools/test_coordinator_rules.py -q (.next over live name in scratch copy)", "result": "448 passed in 9.90s"},
      {"command": "python -B <scratch>/probe.py <scratch> <scratch>/cases.txt (old _worker_verdict_call vs new roads, rollback/cd/write counts)", "result": "15 deny losses, 0 rollback losses, 4 cd gains incl. env cd, 3 write gains"},
      {"command": "python -B <scratch>/of3run.py <worktree>/ai-packages/qa-factory/scripts/tests", "result": "17/17 ok, elapsed 51.44s (R3 44.83s alone)"}
    ]
  }
}
```
