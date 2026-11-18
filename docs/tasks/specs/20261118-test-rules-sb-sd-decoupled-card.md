# Test rules S-B and S-D without everything-in-piles: decoupled cards (designer t-1507, F19)

Base: `docs/tasks/specs/20261117-forge-test-rules-spec.md` r3 ("the spec", sections `spec §N`). This card REPLACES the
spec's §7.4 (S-B) and §7.6 (S-D) cards and the parts of §3.2-§3.4, §5.2, §8, §9 they carry; the rest of the spec stands.
The spec is not edited. Owner 18.11: everything-in-piles ("EiP") is not taken; S-B, S-C, S-D are NOW items.

## 0. Landed state (measured 18.11, Grep/Read tool, root checkout)

Base: `.git/refs/heads/main` = `.git/refs/remotes/origin/main` = `5c9bd80b` (Read of both files). Tree = that commit is an
`estimate`; Lead's check: `git -C C:/QAFactory/forge-repo status -sb`.

| Stream | Key, command | Result | State |
|---|---|---|---|
| S-A1 | Grep the three TESTING headings + «решает цель» over `docs/TESTING.md`; Grep `KILLING POWER\|judged by reading it` repo-wide minus worktrees | TESTING `:61, :75, :149, :225`; q5 now `critic.md:205-208` | LANDED (t-984); its brief is gone, §2 R1 |
| S-A2 | Grep «Набор мутаций», «К напечатанному добавляются только» over TESTING; «Мутаций канон не гоняет» over RUNBOOK | TESTING `:107, :124`; RUNBOOK `:134`; `plans/builder-rules.md` absent (folded into TESTING) | LANDED (t-1025) |
| S-C | Grep `SKIP_ONLY_ITEMS\|TEST_LINE_REFUSES` over `tools/dispatch_*.py` (control `KEY_GROUPS`: 6 in `dispatch_manifest.py`) | 0 | NOT landed (after FG7-95) |
| S-E | Grep `--root\|TIMEOUT_S\|outcome:` over `mutate_once.py`; Glob test; Grep `mutate_once` over `test-layers.json` | `:5-6`, `:39`, `:237`; `test_mutate_once.py` exists; keep row `:3091` | LANDED (t-982) |
| S-B | Grep `mutants\|mutate_once\|probe` -i over agents, CLAUDE.md, COORDINATOR.md, calibration, schema, `handoff_gate.py` | unrelated «probe» hits only | NOT landed |
| S-D | Read `critic_verdict_check.py` whole | `validate_verdict :63-169`: no `mutants` | NOT landed |

EiP on main: C, A2, D NOT landed — Grep `_verdict_problem|critic_verdict|check_text|remarks` over `tools/*.py`: no
`remarks` in the checker, nothing in `piles.py` (controls: `check_text` at the checker `:172`, `remarks` at
`controller-blocks-gen.py:181`); rule 17 (`critic.md:140-152`) has no `remarks`. No code runs the checker (Grep
`critic_verdict` over settings, githooks, COORDINATOR/PROJECT/CLAUDE, `.github`, `tools/*.json`: only `settings.json:163`,
an allow line); the hand road is critic.md rules 17 (`:148-151`) and 23 (`:282-283`).

## 1. Each dependency on EiP, in both worlds

N = EiP never lands; L = an EiP stream lands later (re-join move).

| # | The spec waits on / cites | World N (this card) | World L (re-join) |
|---|---|---|---|
| D1 | S-D «after EiP C» (§5.2, §7.6, §8) and its `given:` EiP §2.3 | no wait; base = main's checker; that `given:` dropped | C merges `main` after S-D: its fixtures carry `mutants`, `_remark_errors` beside `_mutant_errors`; batch line `очередь: S-D → EiP C` |
| D2 | S-D `remark` = id of a C `remarks` item, disposition `fix` (§5.2) | `remark` = first word of EXACTLY ONE `blockers`∪`fixes` entry (F-3) | C makes every such first word a `fix` remark id, so the link holds unchanged; C may tighten it, never loosen |
| D4 | old-verdict door names A2's commit line `verdict: <node> none -- …` (§5.2, F13) | the diagnostic gives the reason phrase, rule 17 names today's carrier: the `accepted` event's notes (F-2) | A2 reads its commit line (field-generic phrase by the owed F-D amendment); EiP D's rule 17 edit swaps the carrier clause (F-5) |
| D5 | M3 (d): on a path «only after A2» (§5.2, §10.1, EiP P31) | the hand road of every verdict field today (rules 17, 23); detector check 50 (b) (F-1) | A2 puts `check_text` on the commit path; S-D unchanged |
| D6 | S-B rule 17 «after D's clause if D landed first» (§3.3) | insert AFTER «trail (read + reruns);», which stays intact | D inserts right after the same anchor; either order resolves |
| D7 | §8 rows: critic.md D→S-B; designer/builder D; calibration; carrier test D rows; brief D | free: S-B writes critic.md 17/20/21/22 Q5, builder.md 8, designer.md 1, check 13(j), new check 50 | D's sentences (critic.md 5, 19; designer.md 2; checks 33, 39) are others; carrier test rows append-only |
| D8 | P22, F13, F-D, §13 item 13 | record only; nothing written in the EiP spec | F-D applied before A2's dispatch (decided) + D4's carrier note (F-5) |
| D9 | §8 wave 2 waits for EiP C, D, architect F, the CLAUDE.md move | F landed (check 49); the move landed (rule 3 in COORDINATOR.md): nothing left to wait for | — |
| D10 | §11 reader `piles._verdict_problem` | none (§0) | A2: S-D's line, then its door |

## 2. Re-anchors that are not EiP's

- R1. `docs/tasks/critic-diff-brief.md` is deleted; q5 and «The two layers» are `critic.md` rule 22 Q5 (`:205-232`) and rule
  21 (`:182-195`). K-NOBRIEF (`test_role_carriers_one_owner.py:194-247`) reds a MAIN document naming `critic-diff-brief`:
  S-B texts point at critic.md rules 21/22 only.
- R2. CLAUDE.md rule 3 is `COORDINATOR.md` rule 3; anchor sentence `:133`; parity anchors «TWO-LAYER CRITIC ENTRY», «starts
  with EMPIRICS» (`install_parity_anchors.json:58-59`). R11-h stays `CLAUDE.md:83` (anchor `:22`).
- R3. builder.md `:51-52` is gone; its successor, rule 8 `:109-111` (T9), contradicts TESTING's goal rule (`:225`). R4.
  designer.md rule 1 `:23-25` (T10) still forbids files outside keep rows.
- R5. SIBLING_MAP has 38 axes (Grep `^## Axis \d+` → 38): spec §10.2's block gains axis 38 (`:643`). Next free check: 50
  (Grep `^(4[5-9]|5\d)\. \*\*` → 45-49).
- R6. `AGENTS.md` is generated from CLAUDE.md + coordinator files (`agents_md.py:3-5`): S-B owns it.
- R7. `test_critic_verdict_check.py` has no validate table (one `parametrize`, stdin deadline, `:439`): S-D adds ONE table.

## 3. Card S-B (builder edits, leaves STAGED; Lead commits with the axis block and `tier:`)

given: this card §1-§6; spec §3.2 E-P1..E-P11, §9, §10.2; the owned files as cited in T1-T12; `tools/install_parity_anchors.json:39-60, 145-193`; `tools/test_handoff_rule_anchors.py`; `tools/mechanism_gate.py:24-51`
owns: C:/QAFactory/forge-repo/.claude/agents/critic.md
C:/QAFactory/forge-repo/.claude/agents/builder.md
C:/QAFactory/forge-repo/.claude/agents/designer.md
C:/QAFactory/forge-repo/CLAUDE.md
C:/QAFactory/forge-repo/COORDINATOR.md
C:/QAFactory/forge-repo/AGENTS.md
C:/QAFactory/forge-repo/tools/handoff_gate.py
C:/QAFactory/forge-repo/PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md
C:/QAFactory/forge-repo/docs/SIBLING_MAP.md
C:/QAFactory/forge-repo/tools/tests/test_role_carriers_one_owner.py
non-goals: rule numbers, openers; `handoff_gate.py` code; COORDINATOR.md beyond the rule 3 sentence; CLAUDE.md beyond R11-h; critic.md beyond rules 17, 20, 21, 22 Q5 (a); EiP's sentences; both specs; S-C
handoff: C:/QAFactory/forge-repo/docs/tasks/handoffs/<task>-sb-report.md
edges: E-B1..E-B7 below; the probe's semantics = spec §3.2 E-P1..E-P11
DoD: `python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_handoff_rule_anchors.py tools/test_handoff_gate.py -q` green; `python -B tools/install_parity.py --check` MISSING (0); `python -B tools/agents_md.py --check` 0 after regeneration; `python -B tools/pointer_lint.py --check` 0; doc-dispatch witness on the keys below (verbatim, whitespace squashed, script in full in the report, one key absent -> failure); E-B6 grep
test: tools/tests/test_role_carriers_one_owner.py::OWNER_KEYS ("review:probe", CRITIC, "The ONE road is the runner, by Bash, never Write or Edit") and POINTERS (COORD, "`.claude/agents/critic.md` rule 21", CRITIC, CRIT_21) | expected from: this card T2, T6
test: none -- role, policy, process texts and a docstring; doc-dispatch witness (CLAUDE.md rule 11) | expected from: this card T1-T12
siblings: axis 1 (critic.md, builder.md, designer.md, COORDINATOR.md rule 3, R11-h, check 50 change together); axis 2 (no PROCESS/CRITIC_EXAM.md: «Deviation: exam not run; debt F3-1»); axis 31 (the probe's one home: critic.md rule 21); FG7-62 t-1504 writes COORDINATOR.md/AGENTS.md (§5)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-test-rules-sb-sd-decoupled-card.md

Texts (anchors quoted from main, 18.11; "keeps" = the invariant of the position):
- T1. critic.md rule 21: after «A layer not attached is returned to the dispatcher as a request, never executed by the
  critic.» (`:188-189`) append « The probe below is not a builder's layer: it is the critic's own bounded run
  (COORDINATOR.md rule 3).» Keeps: a builder's layer is still never executed by the critic.
- T2. critic.md rule 21: a third bullet after «re-deriving the mechanics by reading everything is not.» (`:195`), before
  «22.». Keeps: the verdict-layer bullet byte-identical.

```
   - **The probe** (the owner's word 17.11.2026: fix it, without going back to a pile of mutants): on a diff with NEW
     behaviour, break 1 to 3 places of it — your choice, the load-bearing ones (a comparison flipped, a branch dropped, a
     refusal turned into a pass, the safe default returned). Hard cap: 3 mutant runs per verdict, invalid ones included.
     The ONE road is the runner, by Bash, never Write or Edit:
     `python -B <tree>/ai-packages/qa-factory/scripts/tests/mutate_once.py --root <tree> --id <name> --target <path>
     --old "<text>" --new "<text>" --test <path> [--pytest]` — <tree> is the node's worktree the dispatch names, and only
     that tree: the dispatcher names it only after the builder has handed back, and starts no fix round, merge or worktree
     removal in it until your verdict returns. Paths are relative to it; `--pytest` for a `tools/` test. When the tree's
     runner answers with a usage text that names no `--root` (exit 64, nothing touched), call the runner of your own
     checkout with the same `--root <tree>`; when that one names no `--root` either, no probe. Give every runner call a
     Bash timeout of at least 120000 ms (the runner's worst case is its 60 s test timeout + 5 s to kill and restore): a
     runner killed from outside cannot restore. The runner checks the anchor, compiles the mutated file, runs ONLY the
     narrow test file the spec's `test:` line names (no line: the narrowest file of the builder's witness) with a 60 s
     timeout, restores the file from its byte copy whatever happened, compares sha256 and prints `outcome: killed |
     survived | invalid | restore-mismatch`. Never a slow (`SLOW_TESTS`, `test_story_run_*`, `test_story_step.py`),
     quarantined or canon file; no copy, edit or restore by hand. Before the first mutant: `git -C <tree> status
     --porcelain` prints nothing (else no probe: the runner would restore bytes the branch does not hold), and the same
     narrow file has run GREEN in the same tree as your control re-run (its command, naming that `--test` path, in
     `trail.reruns`): a red baseline makes every kill false. A kill whose printed FAIL line is an import or collection
     error is invalid, not a kill. Every runner call, an exit-64 refusal included, goes into `trail.reruns` (command and
     output tail); every mutant run goes into the block's `mutants` (place, change, run, outcome, the row that killed it);
     an exit-64 refusal touched nothing and is no mutant run. A survivor is a finding under rule 22 Q5 (a) unless it is
     equivalent — then say why in its `equivalent`; the finding is one entry of `blockers` or `fixes` whose first word is
     an id (`M1:`), and the mutant's `remark` names that id. No probe (a docs-only or plan gate, no new behaviour, the
     narrow test slow or quarantined, no tree named by the dispatch, a dirty tree, no runner with `--root`, the control run
     red): `mutants: []` and `mutants_none: "<why>"`. `outcome: restore-mismatch`: stop probing; your verdict is not
     `fit`, and the fix entry the mutant's `remark` names states the file and the restore door — in Bash,
     `git -C <tree> show HEAD:<path> > <tree>/<path>`, then `git -C <tree> status --porcelain` prints nothing.
```

- T3. critic.md rule 22 Q5 (a): «-- judged by reading it.» (`:207`) → «-- judged by reading AND by the probe of rule 21; a
  probe mutant in load-bearing new behaviour that survives is a finding (an equivalent mutant is not, with its why).»
  Keeps: (a) asks for a probe only in the merge that sanctions it (T6).
- T4. critic.md rule 17: after «trail (read + reruns);» (`:142-143`) insert « mutants (the probes of rule 21, each run in
  trail.reruns) or, when there was no probe, mutants_none with its reason; a verdict written before mutants existed fails
  the check and is accepted only with the reason "verdict predates a required field (mutants)" in the `accepted` event's
  notes;». Keeps: «trail (read + reruns);» intact (D6); the opener (`install_parity_anchors.json:170`) and the words
  `critic_verdict_check.py`, `` `handoff:` `` (`test_handoff_rule_anchors.py:89, 103`).
- T5. critic.md rule 20: «(the rule text is docs/TESTING.md «Бюджет»)» (`:173-174`) → «(the rule texts are docs/TESTING.md
  «Бюджет», «Откуда берётся ожидаемое значение» and «Тест может упасть»; the probe of rule 21 answers under Q5 (a))».
  Keeps: POINTERS row `(CRITIC, "docs/TESTING.md «Бюджет»", …)` (`:84`) matches.
- T6. COORDINATOR.md rule 3: after «a layer not attached → critic asks the dispatcher for it and does not execute it.»
  (`:133`) insert (F-4 (b)) « The critic's own run beyond that is the bounded probe of `.claude/agents/critic.md` rule 21
  (its runner, its cap, Bash only).» Keeps: both parity anchors; «Money/numeric diffs: critic starts with EMPIRICS» unchanged.
- T7. CLAUDE.md R11-h: after «`tools/handoff_gate.py` lets it write only that file» (`:83`) insert «; a critic's probe
  (`.claude/agents/critic.md` rule 21) is no write of its own: the runner restores the file from a byte copy». Keeps:
  anchor `:22`; one table row.
- T8. `handoff_gate.py` docstring after «path of its dispatch and refuses every other Edit/Write.» (`:8`), ASCII: «Bash is
  not gated here. A critic's one sanctioned Bash write is the probe of .claude/agents/critic.md rule 21 (COORDINATOR.md
  rule 3): ai-packages/qa-factory/scripts/tests/mutate_once.py mutates one file and restores it from a byte copy with a
  sha256 check; any other write by a reading role, by any tool, stays outside its rules.» No code line.
- T9. builder.md rule 8: «A new case is a row of an existing scenario, table or junction, not a new file (the one
  exception: «Бюджет / Файлы»).» → «A new case is a row of an existing scenario, table or junction by default; a new test
  file is written only where the DoD's `test:` line places it (docs/TESTING.md «Бюджет / Файлы»; a package file gets its
  keep row). The expected value of a test and the red-before run of a defect row: TESTING.md «Откуда берётся ожидаемое
  значение», «Тест может упасть».»
- T10. designer.md rule 1: «a DoD never asks for a new test file outside the keep rows of `test-layers.json`; a new case
  is a variant/table row.» → «a DoD names the place of every new case on its `test:` line (`docs/TESTING.md` «Строка теста
  в DoD»): a variant/table row by default, a new file only by the goal of `docs/TESTING.md` «Бюджет / Файлы».» Keeps: the
  POINTERS row of rule 1 (`:86`), opener anchors.
- T11. Calibration. (a) 13(j) `:396-398` «a full `selftest.py`, a docker run or a mutation RUN is the leak — those are the
  batch canon's (`docs/TESTING.md` «Что запускать по своей правке»)» → «a full `selftest.py` or a docker run is the leak —
  those are the batch canon's (`docs/TESTING.md` «Что запускать по своей правке»); a mutation SUITE is the leak too and
  nobody's (a builder's one `red-before:` run of a defect row and a critic's probe through `mutate_once.py` are not a
  suite, `docs/TESTING.md` «Тест может упасть»)». (b) Check 50 after check 49 (`:1151`), before «## Weekly cost review»:
  spec §9's text with `N.` → `50.`; «`docs/tasks/critic-diff-brief.md` question 5 and «The two layers»» →
  «`.claude/agents/critic.md` rule 21 and rule 22 Q5»; «critic question 5 (a)-(g)» → «critic rule 22 Q5 (a)-(g)»; «the
  brief's cap» → «rule 21's cap» (every place); (a) opens «builder dispatches over the designer threshold: until the `test:` gate of
  `tools/dispatch_manifest.py` lands (S-C), those with no `test:` line, counted by reading; after it,» then the spec's (a).
- T12. SIBLING_MAP axis 31: TESTING row (`:489`) aspect cell + «; the expected value's source; the `test:` line; the
  new-file goal; `red-before:`»; critic.md row (`:485`) aspect cell + «, the probe and its runner (21)». Columns unchanged
  (`pointer_lint.main_documents` reads the File column).

Doc keys present: «- **The probe**», «Hard cap: 3 mutant runs per verdict», «mutate_once.py --root <tree>», «whose first
word is an id», «by the probe of rule 21», «it is the critic's own bounded run (COORDINATOR.md rule 3)», «status
--porcelain», «show HEAD:<path>», «at least 120000 ms», «verdict predates a required field (mutants)», «the bounded probe
of `.claude/agents/critic.md` rule 21», «is no write of its own», «Bash is not gated here», «a new test file is written
only where the DoD's `test:` line places it», «a DoD names the place of every new case on its `test:` line», «a mutation
SUITE is the leak too», «Forge test discipline», «the probe and its runner (21)». Absent: «-- judged by reading it.»,
«not a new file (the one exception», «a DoD never asks for a new test file outside the keep rows», «a docker run or a
mutation RUN is the leak», «critic-diff-brief».

Edges (each with its invariant):
- E-B1 TEMPORAL, S-D not merged with S-B (F-1 (c)/(d)): T4's old-verdict clause waits for S-D; the rest lands. Invariant: no
  live text names a refusal no code raises.
- E-B2 TEMPORAL, the S-A1 → S-B window (spec §4.5): R3/R4 contradict TESTING «Бюджет / Файлы» until this merge; meanwhile a
  designer returns a fork, a builder a question. Invariant: no new file lands against a live text forbidding it.
- E-B3 TEMPORAL: TESTING `:305` names check «Forge test discipline» before it exists; T11 (b) creates it. Invariant: the
  title resolves after this merge.
- E-B4 POSITIONAL, EiP D later (D6): T4 leaves «trail (read + reruns);» intact. Invariant: D's anchor resolves in either
  order; no clause spliced inside another.
- E-B5 POSITIONAL, t-1504 moved COORDINATOR.md text first: T6 follows the sentence ending «does not execute it.» wherever it
  stands; that sentence gone from COORDINATOR.md → stop, question. Invariant: the sanction sits next to the restriction it
  qualifies, in one carrier.
- E-B6 One road: Grep `copy, mutate|byte copy of the file BEFORE` over critic.md, TESTING.md, CLAUDE.md, COORDINATOR.md → 0;
  control: the same call with `byte copy` finds T8's line. Invariant: no text describes a hand copy/mutate/restore.
- E-B7 Boot bytes: T6 ~120 B, T7 ~110 B; `session_context.py` WARN/BREACH code unchanged; the report prints both files'
  `os.path.getsize` before/after. Invariant: growth is measured and named.

## 4. Card S-D (builder; Lead commits)

given: this card §1 (D1-D5), §4; spec §5.2 (as replaced), §5.3 outcome words; `tools/critic_verdict_check.py`, `tools/critic_verdict.schema.json`, `tools/test_critic_verdict_check.py`; critic.md rules 17, 21 as T2, T4 write them
owns: C:/QAFactory/forge-repo/tools/critic_verdict_check.py
C:/QAFactory/forge-repo/tools/critic_verdict.schema.json
C:/QAFactory/forge-repo/tools/test_critic_verdict_check.py
non-goals: `remarks` or any C rule; `piles.py`; a call site of the checker; judging load-bearing, equivalence or a green control
handoff: C:/QAFactory/forge-repo/docs/tasks/handoffs/<task>-sd-report.md
edges: behaviours 1-7, E-D1..E-D5; E-T1 (one merge with S-B)
DoD: `python -m pytest tools/test_critic_verdict_check.py -q` green; the report lists each fixture that gained `mutants` and states no assertion was weakened
test: tools/test_critic_verdict_check.py::MUTANT_ROWS (new table, existing file) -- run join, green control, cap | expected from: this card behaviours 1-3
test: tools/test_critic_verdict_check.py::MUTANT_ROWS -- survivor and restore-mismatch link | expected from: behaviours 4-5, T2
test: tools/test_critic_verdict_check.py::MUTANT_ROWS -- declared empty outcome | expected from: behaviour 6
test: tools/test_critic_verdict_check.py::MUTANT_ROWS -- old verdict line | expected from: behaviour 7
siblings: axis 17 (one verdict shape, one reader `check_text`); `install_parity_anchors.json:715-716` (kind path, unchanged); `dup-baseline.json:350, 483` (named if the clone ratchet moves)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-test-rules-sb-sd-decoupled-card.md

`_mutant_errors(obj)` called from `validate_verdict`; the schema mirrors it; diagnostics ASCII, no raw values. Cap 3 = data
here, rule in critic.md 21.
1. `mutants` REQUIRED array, 0-3; > 3 → `field 'mutants' has N items: at most 3 (the cap of .claude/agents/critic.md rule
   21)`. Item: `place` 1-300 chars, `change` 1-300, `run` 1-500, `outcome` ∈ `killed`/`survived`/`invalid`/
   `restore-mismatch`; `killed_by` 1-300 REQUIRED exactly when `killed`, else absent or null.
2. Run join: `run` equals one `trail.reruns[].command`; contains `mutate_once.py`; runs pairwise distinct; the joined
   `result` contains `outcome: <outcome>`.
3. Green control: non-empty `mutants` → per distinct `--test` value, ≥ 1 rerun command without `mutate_once.py` that
   contains it. Values read by `--(test|target)\s+("([^"]*)"|'([^']*)'|(\S+))`; no `--test` → `mutant <i>: run names no
   --test`.
4. `survived`: exactly one of `equivalent` (has a word character) or `remark`; `remark` resolves when exactly ONE entry of
   `blockers` ∪ `fixes` has it as first whitespace token (trailing `:` stripped on both sides); 0 → `mutant <i>: remark
   names no blockers or fixes entry (its first word)`; 2+ → `mutant <i>: remark names 2 or more entries`.
5. `restore-mismatch`: `verdict` ≠ `fit` AND `remark` resolves (as 4) to an entry containing the item's `--target` value
   and `show HEAD:`; else `mutant <i>: outcome restore-mismatch needs a verdict other than fit and a fix entry, named by
   remark, stating the target and the restore door "git -C <tree> show HEAD:<path> > <tree>/<path>" (.claude/agents/
   critic.md rule 21)`. `invalid`: nothing more (counts toward the cap).
6. `mutants: []` requires `mutants_none` (word character); `mutants_none` with non-empty `mutants` → error.
7. No `mutants` → `missing required field: mutants (a verdict written before this field existed is accepted only with the
   reason "verdict predates a required field (mutants)" where its acceptance is recorded: .claude/agents/critic.md rule 17)`.

Error direction: shape and joins only; may FALSE-PASS a fabricated kill (check 50 (b) counts transcript calls); must NOT
false-refuse. PASS: entry `M1: …` with `remark` `M1` or `M1:`; entry `M1 — …`; quoted `--test 'tools/test_x.py'`; `--old
"a b"`; `killed_by: null` off `killed`; restore-mismatch linked to a `blockers` entry in `blocker`. REFUSED: 4 probes;
survivor with neither or both fields; remark matching 0 or 2 entries; `killed` without `killed_by`; two mutants one run; run
without `mutate_once.py`; result without the outcome word; no control or a control on another file; `[]` without reason;
reason with probes; restore-mismatch in `fit` or with an entry lacking the target or `show HEAD:`; no `mutants` (line 7).

Edges (each with its invariant):
- E-D1 TEMPORAL: `_base_fit/_base_fit_with_fixes/_base_blocker` (`:46-75`) gain `mutants: []`, `mutants_none: "no new
  behaviour: fixture"`. Invariant: every existing assertion stays; only fixtures grow.
- E-D2 TEMPORAL, in-flight verdicts: written before the merge, accepted after → line 7; the coordinator accepts by T4's
  clause. This node's own review is checked by the pre-merge checker. Invariant: no verdict lacking `mutants` passes; the
  hand door is named and counted (check 50 (b)).
- E-D3 World L, C later: C merges `main`, its fixtures carry `mutants`, the first-word link stays. Invariant: a survivor's
  link never resolves to a `чужой-код` remark (no entry names one).
- E-D4 World L, A2 later: `_verdict_problem` prints line 7 first, then its door. Invariant: both name the one phrase «verdict
  predates a required field (mutants)» (F-D before A2's dispatch).
- E-D5 E-T1: one `wave.py merge` with S-B; if split, S-B first and T4's old-verdict clause with S-D (E-B1). Invariant: never a
  required field before the text that asks critics for it.

## 5. Order and windows

- Wave 2 = S-B + S-D, one merge; S-E landed. EiP later: D after S-B, C after S-D, A2 after F-D. S-C independent.
- FG7-62 (t-1504) also writes `COORDINATOR.md`/`AGENTS.md`: first dispatched goes first; the later merges `main`, places
  T6 by its words (E-B5), regenerates `AGENTS.md`; the line in both batch rows (F-4).
- Closing at this merge: E-B2, E-B3, spec §8's wave 1 → 2 window.

## 6. Readers (designer rule 7)

The owns_readers block was NOT attached. Lead runs before dispatch, answering each line in critic.md rule 24 Q13 (d) forms:
`python -B tools/owns_readers.py --paths .claude/agents/critic.md .claude/agents/builder.md .claude/agents/designer.md CLAUDE.md COORDINATOR.md AGENTS.md tools/handoff_gate.py PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md docs/SIBLING_MAP.md tools/tests/test_role_carriers_one_owner.py tools/critic_verdict_check.py tools/critic_verdict.schema.json tools/test_critic_verdict_check.py --names validate_verdict check_text`
Hand greps (Grep tool, 18.11):
- checker + schema: `critic_verdict|mutants` over tools, githooks, settings, agents, `.github` → 32 in 13 files: test →
  S-D; critic.md 17 → S-B; parity `:715`, dup baseline, `md_regions`, `escape_check`, `test_p4_stdin_deadline`,
  `test_handoff_rule_anchors`, `settings.json:163` → unchanged; `test_workflows:643`, `test_usage_report:1809`: word only.
- `COORDINATOR.md`: `COORDINATOR\.md` over `tools/*.py` → 80 in 24 files: `coordinator_rules.py`/`agents_md.py` → AGENTS.md
  (S-B); `pointer_lint.py` (rule 3 heading kept), `session_context.py` (boot size, E-B7), `mechanism_gate.py`, parity
  anchors → unchanged; t-1504 → §5.
- `CLAUDE.md`: parity anchors `:6-35` kept, spec §11's 22 files → unchanged; AGENTS.md → S-B. Role files: carrier rows →
  S-B; openers (`:145-193`), `test_handoff_rule_anchors.py:89,103` → unchanged. `handoff_gate.py` (spec §11, 83/12) →
  docstring only. Calibration, SIBLING_MAP → headings, File column kept. Carrier test: EiP D rows later, append-only.
Known misses: miss 3 — the cap 3 pinned elsewhere is the Lead block's question (`estimate`); miss 5 — TESTING `:159-160,
:301` point at critic.md rule 21/22 and stay true.

## 7. Forks (plain words, recommendation first)

- F-1 (D5) Without EiP A2, no code runs the verdict checker; the critic and the coordinator run it by hand, as for every
  verdict field today. (a) RECOMMENDED: land S-D on that hand road, counted by check 50 (b). (b) its own call site (a
  SubagentStop check of the critic's handoff in `dod_gate.py`): a new enforcement node, live hook + settings. (c) drop S-D:
  probes stay prose. (d) wait for A2: indefinite; S-B lands alone (E-B1).
- F-2 (D4) Where the reason for accepting an old verdict is written while no gate reads `verdict:` lines. (a) RECOMMENDED:
  the checker gives the phrase; rule 17 names the `accepted` event's notes (`journal_write.py --notes`). (b) no door: a
  fresh critic re-emits each in-flight verdict. (c) `mutants` optional until A2: reverses L-4, the field becomes skippable.
- F-3 (D2) How a surviving mutant is tied to its finding without C's `remarks`. (a) RECOMMENDED: `remark` names the first
  word of exactly one `blockers`/`fixes` entry; when C lands that word is a remark id by C's rule, nothing changes. (b) no
  link: the checker cannot see a survivor left without a finding. (c) S-D waits for C.
- F-4 (T6, T7) Size of the rule 3 sanction while t-1504 squeezes the same file. (a) the accepted B1 text re-pointed (~260 B
  in COORDINATOR.md). (b) RECOMMENDED: a one-sentence pointer (~120 B), the runner/cap/Bash text once in rule 21 (axis 31);
  R11-h ~110 B. Either way an order line with t-1504 — the brief called it disjoint, but S-B now writes COORDINATOR.md and
  AGENTS.md.
- F-5 (D4, D8; another pile) When EiP is taken, its spec needs two re-join notes: the owed F-D amendment, and «D's rule 17
  edit swaps the carrier "the `accepted` event's notes" for the commit line». RECOMMENDED: the Lead records both then;
  nothing now.

## 8. Small choices closed

r3 probe wording kept but for pointers and the link (F-3); pre-S-E runner fallback kept; check 50; one regex for
`--test`/`--target`; `:` stripped both sides; one table `MUTANT_ROWS`; keys whitespace-squashed; AGENTS.md in S-B owns;
the spec's SIBLING_MAP brief row dropped.

## 9. Reading trail

Read: the spec, critic.md, the checker (whole); EiP `:230-319, 606-630, 1640-1650`; `COORDINATOR.md:118-139`;
`builder.md:40-119`; `designer.md:14-33`; TESTING `:95-169`; carrier test `:1-293`; parity anchors `:1-75`;
`handoff_gate.py:1-14`; `agents_md.py:1-14`; SIBLING_MAP `:474-523`; calibration `:392-401, 1149-1153`; `.git` refs.
Greps as cited; `mutation RUN` over `tools/` 0 (control: `PROCESS/` 1); Glob brief/builder-rules (worktrees only);
`--notes` in `journal_write.py` (2); Glob `PROCESS/*EXAM*.md` (no CRITIC_EXAM).
Not established: tree = `5c9bd80b`; the owns_readers block; canon-only class of S-B's test files (`dispatch_new.py`
refuses it if so); E-B7 figures; this file's size (`estimate` under 30 KB; Lead: `python -B -c "import
os,sys;print(os.path.getsize(sys.argv[1]))" <path>`).
