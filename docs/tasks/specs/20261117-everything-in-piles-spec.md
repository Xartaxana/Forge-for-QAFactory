# Spec t-907 — «Всё в кучках»: one registry of work, leftovers that do not breed nodes (DRAFT r3, designer)

Status: DRAFT round 3 for Lead acceptance — fix round t-945 after the second plan critic t-943
(`docs/tasks/specs/reviews/t-943-everything-in-piles-r2.md`, verdict GO WITH FIXES: blockers R1-R6, fixes F-a … F-n, class
completeness lines). Every remark is closed in this round (the owner's rule 17.11.2026: nothing is queued); the table «Fix
round t-945» at the very end maps each remark to what changed and where. Round 2 (t-926, after t-920) keeps its own table
just above it. The critic re-pass is owed on R5 only: it is §8.2, written to be judged alone.
The six OWNER forks are DECIDED (a) by the owner, 17.11.2026 («всё по рекомендациям», the section at the very end): F1,
F8, F14, F16, F18, F19 — the stream texts below state the (a) behaviour as the spec's statement; the fork paragraphs stay
as the record. Words of round 2 that still stand: (W1) «ок» to the Lead's B1-B5 decisions; (W2) F5 decided "the owner or
the batch Lead"; (W3) B5 is a CLASS — §8.
Owner-facing rule texts are Russian; code, tool messages and data keys English (PROJECT.md «Язык»).

```
task: t-907 (draft), fix rounds t-926, t-945 | feature: F19 | each build node gets its own task_id (CLAUDE.md rule 2 threshold per node)
designer: this file
```

The owner's decision (17.11.2026, Lead session): «ВСЁ В КУЧКАХ» — the only registry of work on the factory and the forge
is the piles (`plans/piles/<slug>/`); everything that is work is a NODE of a batch; the type of work is a field of the
node; a big idea is its own batch with a plan file; the Lead queue, the FR debt and batch leftovers become nodes;
`plans/BACKLOG.md` stays an archive. For the FR debt the owner said «давай починим сейчас»: the debt rows are FIXED by a
separate spec, not migrated (§3); once empty the file is deleted (F8 (a), decided).

---

## Premises (load-bearing facts, each with its carrier)

| # | fact | carrier / command | state |
|---|---|---|---|
| P1 | 103 batch files; 36 not closed = 26 `ожидает` + 10 `в работе`; 67 `закрыта` | Grep `^кучка:.*\| статус: (…)` glob `batch-*.md` over `plans/piles`; t-920 key 1 re-ran it (`uniq -c`) | measured (twice) |
| P2 | Every batch's node table has the SAME 7 columns `Узел \| Приоритет \| Что \| Исполнитель \| Пишет в \| Зависит от \| Статус` (hotfix-12586/2 has 3 helper tables above it) | Grep `^\| *Узел *\|` glob `batch-*.md` → 106 lines in 103 files | measured |
| P3 | No `Тип` / `Откуда` column exists anywhere; the parser knows `узел/исполнитель/пишет в/статус/что` only | Grep `^\|.*\| *(Тип\|Откуда) *\|` glob `batch-*.md` → 0; positive control of the SAME shape `^\|.*\| *(Приоритет\|Откуда) *\|` → 103 files; `tools/piles.py:608-609` `NODE_COLS`, `NODE_REQUIRED` | measured / read |
| P4 | ~691-698 table rows end in a cell starting `ожидает`, in 32 batch files | Grep tool → 698; t-920 shell grep → 691 | measured |
| P5 | One status vocabulary in code: `BATCH_STATUSES`, `NODE_STATUSES`, `STATUS_ORDER`, read by `status_word` | `tools/piles.py:111-115, 200-206` | read |
| P6 | A second copy of status words in `tools/backlog_tree.py:19-20, 40-50`; the pane prints `status.split()[0]` | read in round 1 | read |
| P7 | (д) `_node_reds` refuses a node status that starts with no word of P5 — and checks NOTHING about a cell that MOVED to `принято` (no evidence, no verdict, no base comparison) | `tools/piles.py:1846-1858` (re-read in r3) | read |
| P8 | 18 of 103 batches are leftover batches by name, 7 more "incoming" (`vhodyashchie`) | file names of P1 | measured |
| P9 | Leftover roads: (a) critic brief q4; (b) q7 severity `queue`; (c) q12(d) "a fix in this round or a node with an id and an owner"; (d) `piles.py` write-time gate accepts `узел:` (no back-reference) and `перенос:` with a placeholder `подтвердил:`; (e) `close` accepts `перенос:` with any non-placeholder `подтвердил:`; (f) builder-rules п. 1 «Needed from integration»; (g) CLAUDE.md rule 9; (h) rule 12 Cost gates | (a)-(c) `docs/tasks/critic-diff-brief.md:31-34, 56, 91-93`; (d) `tools/piles.py:2826-2852`; (e) `:2767-2788, 2962-2994`; (f) `plans/builder-rules.md:10`; (g)/(h) CLAUDE.md | read |
| P10 | Observed: forge/7 «Ход» critic findings queued, not fixed (03.11, 14.11, 12.11) | `plans/piles/forge/batch-7-vhodyashchie-4.md:86, 88, 89` | read |
| P11 | `close` refuses a bare `узел:` item | `tools/piles.py:2979-2980` | read |
| P12 | (е) splits findings at `FINDINGS_FROM = 2026-10-13`; 1110 findings, 0 newer orphans, **152 older orphans (69 undated)** | `tools/piles.py:2038`; `python -B tools/piles.py check --all` (е) line, run by t-920 | MEASURED (t-920) |
| P13 | 1110 finding files; 33 piles | t-920 | measured |
| P14 | `docs/tasks/lead-queue-fable.md`: 12 items + 2 lines; 10 done, 2 open | `docs/tasks/lead-queue-fable.md:7-24` | read |
| P15 | The two open Lead-queue items already have pile nodes: FG7-51, FG7-49 | `plans/piles/forge/batch-7-vhodyashchie-4.md:72, 74` (re-read r3: FG7-49 `принято: 46a18117 (t-889)`, FG7-51 `ожидает`) | read |
| P16 | Readers of `lead-queue-fable.md`: no code. The ACCEPTED architect-tier spec (its F8 (a)) `git mv`s it to `docs/tasks/lead-queue.md`, adds `docs/tasks/architect-queue.md`, counted by `session_context.py` (its stream C), named by `mechanism_gate._tier_queue_note` (its A5), calibration check 49 (b) (its stream F). `docs/SIBLING_MAP.md:655-661` «Lead Queue» names CURRENT_CONTEXT.md's "Lead Queue" section TODAY; it names `lead-queue.md` only AFTER architect-tier stream F (t-943 N7) | architect-tier spec by Grep (read-main worktree): lines 34, 53, 413, 418, 426, 474, 607, 616, 699; SIBLING_MAP read by t-943 | read |
| P17 | The debt file's header says "Twenty-five rows are open today"; its own rows → **44 open** | `ai-packages/qa-factory/design/factory-rules-debt.md:5-6, 19-141` | read twice |
| P18 | Readers of the debt file (54 files) | Grep `factory-rules-debt` | measured |
| P19 | `tools/collect_intake.py:979-1003` builds a node row for an untaken batch from the table header (any other column → `—`) | read | read |
| P20 | Mechanism paths: `tools/piles.py`, `tools/md_table.py` (live wiring closure, `mechanism_gate.py:274`), `tools/gitcmd.py` (`:259`), `tools/worktree-junk.json` (data deciding a gate, `:279`), `tools/compact_snapshot.py`, `tools/wave.py`, `.claude/agents/`, `.claude/settings.json`, `CLAUDE.md`, `PROCESS/`, `docs/SIBLING_MAP.md`; NOT today: `PROJECT.md`, `plans/builder-rules.md`, `docs/tasks/critic-diff-brief.md`, `tools/backlog_tree.py`, `tools/collect_intake.py`, `tools/critic_verdict_check.py`. At A2 `critic_verdict_check.py` becomes imported by `piles.py` → it, its schema and the vocab leaf join the list in A2's commit (R2, F-l) | `tools/mechanism_gate.py:215-283` | read |
| P21 | The critic verdict JSON: required `verdict, blockers, class_completeness, trail`; `additionalProperties: true`; `VERDICT_ENUM = ("fit", "fit_with_fixes", "blocker")` | `tools/critic_verdict.schema.json:7-52`; `tools/critic_verdict_check.py:46, 73` | read |
| P22 | Text anchors pinned by tests in files this spec edits (brief headings, K-OWN keys of q7/q12(d), builder-rules 7b, CLAUDE.md rule 9 key, COST anchor) | `tools/tests/test_role_carriers_one_owner.py:28-74`; `tools/install_parity_anchors.json:22`; `tools/test_handoff_rule_anchors.py:38-39, 94, 107` | read |
| P23 | `.claude/settings.json:157, 176` still allow `python tools/piles.py board --check` (a refused alias) | Grep | read |
| P24 | DAG-like files under `docs/tasks/`: `factory-fixes.md`, `test-diet.md`, `onboarding-streams-2026-11-12.md` | round 1 | read |
| P25 | Plans of big ideas: the six of t-895 are not on disk as a list | Glob `plans/*.md` | the Lead supplies the six |
| P26 | `BACKLOG.md`: **296 open ids** | `python -B tools/piles.py summary`, t-920 | MEASURED (t-920) |
| P27 | **The t-906 origin table** — 206 leftover items over 11 batches (critic deferred minor 51; owner's new word 31; defect after acceptance / red CI 27; calibration / process 27; scope cut 24; critic other code 20; builder-noticed 14; new ideas 8; live proof 4) | scout t-906, accepted `logs/journal/dev1.jsonl:2244` | from the accepted digest |
| P28 | forge/7: header `статус: ожидает \| взял: —`; 54 node rows, 16 `принято`, 38 `ожидает`. forge/3 and forge/6 were closed with `взял: —` | t-920 key 1; Grep `^кучка:` over `plans/piles/forge` | measured / read |
| P29 | A NODE status is set on an untaken batch with no check of the batch's status (`cmd_status` → `_status_node_row` / `_status_node_cell`) | `tools/piles.py:3267-3362`; t-943 confirmed | read |
| P30 | `wave.py record_node` runs `piles.py status … --set принято --hash --task` in the temp worktree AFTER the merge, then `git commit -m "piles: <slug> <N> <id> принято (<task>)"` WITHOUT `--no-verify` — the status commit passes the commit-msg hook like any commit; a refusal prints "run by hand …" | `tools/wave.py:251-271` (re-read r3) | read |
| P31 | `critic_verdict_check.py` is on NO execution path (the critic self-runs it; the coordinator by hand) | Grep over `tools/*.py`; t-943 re-ran it over tools/.githooks/.github/.claude/PROCESS | measured |
| P32 | (в) compares a taken batch's node table cell by cell against origin/main with only the `Статус` cell masked | `tools/piles.py:1644-1677`; t-943 confirmed | read |
| P33 | `tools/tests/test_role_carriers_one_owner.py`: K-OWN and K-PTR; scan set = tracked text files (`.md .py .json .yaml .yml .txt`) minus EXCLUDED (AGENTS.md, DECISIONS.md, the decisions archive, `ai-packages/`, `experiments/`, `logs/`, `kb/`, specs, handoffs, compact snapshots, task reports, `plans/piles/`, `tools/fixtures/`, itself); K-PTR = substring: `squash(anchor) in squash(target)`; POINTERS = 20 hand rows, OWNER_KEYS = 13 | `tools/tests/test_role_carriers_one_owner.py:8-11, 23-27, 53-74, 131-134` (re-read r3) | read |
| P34 | The debt-fix spec `docs/tasks/specs/20261117-rules-debt-fix-spec.md` was not on disk at round 2 (status not re-checked in r3; not load-bearing) | Glob in round 2 | measured (r2) |
| P35 | `dod_gate.py` (SubagentStop) reads a stopping worker's dispatch (F17 (b)'s base) | `tools/dod_gate.py:356, 393-531` | read |
| P36 | `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` describes `перенос:` in check 33 (line 1026) and check 39 (line 1095) | Grep; t-943 confirmed | read |
| P37 | boot-by-topic fragments: 2c, 2d, 9a, 9b → `docs/TEAMWORK.md`; 9c, 9d, 9e, 9f stay; move criterion = the gate column, her «да» 17.11.2026 | `20261116-boot-by-topic-spec.md:292-308` | read |
| P38 | The generated-copy road: `tools/factory_rules_index.py` + `--check` in pre-commit; `tools/architecture_index.py --check` | `tools/factory_rules_index.py:1-17`; `.githooks/pre-commit:54, 58` | read |
| P39 | Service files in the three globs of round 2: 18 (agents 5, skills 8, briefs 5); stamps of any form: 0 | Glob / Grep, round 2 | measured |
| P40 | `HAND_EDIT = "edit the cell by hand (a taken batch allows it: (в) masks every Статус cell)"` — the door the status writer names; the evidence rule (`--hash`/`--task`) lives only in `_status_evidence` | `tools/piles.py:3225, 3250-3264` (read r3) | read |
| P41 | The commit-message doors are read ONLY in commit-msg: `.githooks/commit-msg:38-40` "the door is a commit-message line "piles-skip: …" -- this is why it runs here and not in pre-commit"; `.githooks/pre-commit` runs no message-reading gate (its gates: journal_validator, escape_check, enforcement_probe, factory_rules_index, architecture_index, agents_md, forge_metrics); CI reads a range's doors through `piles.range_messages` (`tools/piles.py:2330-2341`); forge-check runs `piles.py check --base` (`:84`) and `python -m pytest tools/ -q` (`:96`) | read / Grep r3 | read |
| P42 | `critic_verdict_check.py` imports stdlib only (`:39-44`); its comment at `:190` "a shared module across hooks/tools is deliberately not introduced" concerns the stdin helper | read r3 | read |
| P43 | PROJECT.md: `:333` = `   доказательств не должно. **Остатков в идеале нет вовсе**: минорные` (mid-line, 3-space indent); `:326` is the ONLY line opening item `9.`; `:337` `   **Живые прогоны не держат пачку вообще**` (a line-start bold lead-in, 3 spaces); `:96` `  **как было ДО** и …` is a WRAPPED line inside P20 that also starts with bold (a shape false positive the grammar must survive) | Grep `Остатков в идеале` → 333; Grep `^\s*9\.\|^\s*\*\*[^*]+\*\*` over PROJECT.md (read r3) | read |
| P44 | boot-by-topic's pointer form: `rule: <file> § <section>` (Russian files `правило: <файл> § <раздел>`); its resolver contract §4.3: `<file>` exists; `<x>` equals a heading's text, or `<x>` is a number/id and a line starts with `<x>.` (or `### <x>` / `**<x>.**` / `- **<x>.**`); a numbered pointer's title equals the item's bold opener; unresolvable → RED; adversarial inputs listed. A1 accepted: "FG7-52 extends `tools/tests/test_role_carriers_one_owner.py`, no `pointer_lint.py`" | `20261116-boot-by-topic-spec.md:56, 71, 407-418, 759` (read r3) | read |
| P45 | The forge/7 ROW of FG7-52 still reads "`tools/pointer_lint.py` … в `pre-commit` и `forge-check`", owns `tools/pointer_lint.py`, `tools/test_pointer_lint.py`, `.githooks/pre-commit` — it contradicts boot-by-topic A1 (P44) | `plans/piles/forge/batch-7-vhodyashchie-4.md:75` (read r3) | read |
| P46 | Edit cadence of the main files: 11 CLAUDE.md commits and 10 PROJECT.md commits in 7 days; per commit 1-4 sections touched (3 commits sampled) | t-943 reruns (`git log --since=2026-11-10 … \| wc -l`; `sect.py`) — not re-measured here (no shell) | measured (t-943) |
| P47 | Readers of `.githooks/commit-msg` among `tools/*.py`: 14 files | Grep `commit-msg` glob `*.py` over `tools/` (r3): `mechanism_gate.py`, `test_mechanism_gate.py`, `session_context.py`, `test_session_context.py`, `test_volume.py`, `wiring_check.py`, `test_wiring_check.py`, `piles.py`, `hook_liveness_probe.py`, `test_p4_stdin_deadline.py`, `test_enforcement_probe.py`, `architecture_gate.py`, `test_architecture_gate.py`, `agents_md.py` | measured |
| P48 | `piles_vocab`, `rule_pointers`, `rule_stamps` exist nowhere in `tools/` or `.githooks/` (new names) | Grep `piles_vocab\|rule_pointers\|rule_stamps` -i → 0; positive control of the same shape `piles_vocab\|rule_pointers\|piles_split` -i over `tools/` → 5 files | measured |

---

## 1. Target model

AR-n: this spec does not change `ai-packages/qa-factory/`, so no AR-n of `design/architecture.md` is touched; the forge
analogs it keeps are listed in §7.6.

### 1.1 One node table for every batch

```
| Узел | Тип | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Откуда | Статус |
```

- Two NEW columns, `Тип` and `Откуда`, at those positions; the other seven unchanged (P2).
- `Тип` — one word of the closed list `node_types` in the data file `tools/piles-vocab.json` (FR-13 / AR-1 analog). The
  words (F1 decided (a) by the owner, 17.11.2026): `баг`, `доделка`, `идея`, `оптимизация`, `долг` (the owner's five) +
  `живой-прогон`, `решение` + `неразобран` (the DECLARED unknown that `collect_intake` writes; code never picks a work
  type, FR-59).
- `Откуда` — one of the closed forms (heads in `node_origins` of the data file, grammar in `piles.py`):

  | form | meaning | checked at add time (§4, (д)) |
  |---|---|---|
  | `план` | written with the batch or the idea's plan | — |
  | `находка <file>` | a finding of this pile or `<slug>/findings/<file>` | the file exists in the working tree |
  | `владелец <дд.мм.гггг>` | the owner's word (off the running work's topic, §2.2 row 3) | a real date with a 4-digit year |
  | `миграция` | moved by THIS spec (§3) | — |
  | `остаток <node> · <key>[ · <carrier>]` | born from the work of another node; `<node>` = `<id>` (same pile) or `<slug>/<N>/<id>`; `<key>` ∈ `leftover_criteria` (§2.2) | the parent row exists; the key is in the list; the carrier per key (§2.3) |

  The separator is ` · ` (U+00B7 with spaces) — never `|` (cell-safe).
- `Статус` — unchanged vocabulary (P5); ONE reader `piles.status_word`; `backlog_tree.py` drops its own words (P6).
  A dropped node is `отклонено: <why>`. A cell that MOVES to `принято` needs a `verdict:` line in the commit (§2.3 part 2).
- Priority stays a node column; the batch header `приоритет:` stays the default.

Invariant (P31, AR-13 analog): every batch of every pile is read by the one parser `piles.parse_batch`; a NEW row in any
pile needs the same columns.

New required fields and their EMPTY outcome / OLD rows:

| field | empty outcome | old rows (written before A1) |
|---|---|---|
| `Тип` | none for a NEW row: `—`/empty is refused; the unknown is the word `неразобран` | `—` or no column: legal while the row is OLD (§6 E9) |
| `Откуда` | none for a NEW row | the same as `Тип` |
| batch header `план:` | absent = not a big-idea batch | absent |
| `подтвердил:` on a NEW `узел:` «Остатки» item (F5 decided) | none: required, `<владелец \| Lead пачки>, <дд.мм.гггг>` | legacy `узел:` items pass without it (§6 E20) |
| `verdict:` line for a node accepted in the commit (R1) | none: `verdict: none -- <why>` is the informed pass | a cell already `принято` at the base is not judged (§6 E37) |

### 1.2 Big-idea batch

A big idea = a batch in the topical pile (fork **F11**) whose header carries `план: <repo path>`; its node rows are the
plan's phases/streams (`Откуда: план`). Before a plan exists, the idea is ONE node `Тип: идея`, `Исполнитель: Lead`,
`Откуда: владелец <дата>`, in the topical pile's untaken batch (PROJECT «Новая идея» steps 1-4); when the plan is
accepted, that node becomes `принято: <spec path>` and the batch with `план:` opens. (д) checks that the `план:` path
exists when the header line is new or changed (data, P27); whether the plan is good is the critic-on-plan's.

### 1.3 Where a finding stops and a node starts

- A finding (`findings/*.md`) is EVIDENCE and description; never work by itself.
- Work exists only as a node row. A node names its finding in `Откуда: находка <file>` or in «Что».
- A finding no node row names is an orphan — (е) red for every date once M1 reaches 0 (§4 H).
- A red CI is NOT a finding and not a node (owner's word; §2.2 row 4, F15 on the record's carrier). A defect found after
  acceptance that is not a red CI is fixed on the spot under a new task_id with a `defect_found` journal line, no node
  (F16 decided (a)).

### 1.4 What a leftover is under the new model

A «Остатки» item = something that came up while working the batch. Legal NEW forms: `сделано: <hash | t-nnn>` (fixed
now — the default) or `узел: <node> | подтвердил: <владелец | Lead пачки>, <дд.мм.гггг>` whose row says
`Откуда: остаток <a node of this batch> · <key>[ · <carrier>]` (F5, decided). `перенос:` stops being a NEW form of
«Остатки» and «Живые доказательства» (fork **F4**, Lead); items written before the cutover keep closing by the old form
(§6 E20).

---

## 2. The leftover problem (core)

### 2.1 Where leftovers come from (measured) and which carrier lets them through

Origin shares from P27 (t-906, 206 items, 11 batches; percentages = count / 206):

| origin | count | share | the owner's word (17.11) | leak carrier today | stream (§7) |
|---|---|---|---|---|---|
| critic: deferred minor remark | 51 | 24.8 % | «делать сразу» | brief q4/q7/q12(d), critic.md rules 5/19 (L1-L3), `piles.py` `узел:`/`перенос:` (L4-L6), the hand edit of `принято` (L16) | C, A2, D |
| owner's new word during the work | 31 | 15.0 % | on-topic → now; off-topic → may be a node | practice (L13) | D |
| defect after acceptance / red CI | 27 | 13.1 % | «CI не записываем отдельными узлами»; a non-CI defect the same (F16 (a), decided) | PROJECT «Как принимается» п. 2 (L11) | D |
| calibration / process | 27 | 13.1 % | — (legitimate nodes) | — | — |
| scope cut by the spec | 24 | 11.7 % | legal only «для экономии токенов»; else do or ask | spec non-goals, no gate (L12) | D (+ critic-on-plan key) |
| critic: other code / wider class | 20 | 9.7 % | «вот это можно оставлять» | — (legitimate as `чужой-код`) | C, A2 |
| builder-noticed | 14 | 6.8 % | the same as critic remarks (F14 (a), decided): own code now, other code `чужой-код` | builder-rules п. 1 «Needed from integration» (L7) | D |
| new ideas | 8 | 3.9 % | — (legitimate) | — | — |
| live proof | 4 | 1.9 % | her 11.11 word: `live-runs` | — (legitimate) | — |

The critic share is 71 / 206 = 34.5 %. Carriers by leak:

| # | leak | carrier |
|---|---|---|
| L1 | every out-of-owns analog routed to «Остатки» | brief q4 |
| L2 | severity `queue` | brief q7 |
| L3 | "a node with an id and an owner" as an equal alternative | brief q12(d), critic.md rule 19 |
| L4 | `узел:` needs no back-reference; `перенос:` passes write-time with `подтвердил: —` | `piles.py` `_item_why` |
| L5 | `close` reads `подтвердил:` as text | `piles.py` `leftover_problem` |
| L6 | `close` refuses `узел:`, so node-leftovers are rewritten as `перенос:` | `piles.py:2979-2980` |
| L7 | "Needed from integration" — prose someone later turns into work | builder-rules п. 1 |
| L8 | "fix now, or EXPLICITLY put the remainder in the queue" | CLAUDE.md rule 9 |
| L9 | the fix round keeps the node's owns | CLAUDE.md rule 12 |
| L10 | the coordinator files a critic's queue as nodes in one move (P10) | practice |
| L11 | red `main` → a finding → (after M1) a node | PROJECT «Как принимается» п. 2 |
| L12 | a spec non-goal defers in-topic work with no word of the owner | spec non-goals; no critic-on-plan key |
| L13 | an on-topic word of the owner becomes a node | practice |
| L14 | an untaken batch is worked node by node and never closed (forge/7, P28/P29) | `piles.py` `cmd_status` node branch |
| L15 | a service file restates a main rule and drifts from it | every service file — §8 |
| L16 | a node is accepted by a HAND edit of its `Статус` cell, with no verdict and no record (t-943 R1) | `piles.py:3225` `HAND_EDIT`; `_node_reds` checks the word only (P7, P40) |

### 2.2 The criterion: when a follow-up may be a node at all (= the owner's list, verbatim origin by origin)

| # | origin | rule (the owner's word, quoted in the section «The owner's word on leftovers») | node? | `leftover_criteria` key / `Откуда` |
|---|---|---|---|---|
| 1 | a critic remark about the node's OWN code (in its `Пишет в`), minor included | «делать сразу»: fixed in the same node's fix round; no node, no «Остатки» row | never | — (verdict disposition `fix`) |
| 2 | a critic remark about code OUTSIDE the node's topic | «вот это можно оставлять» | may | `чужой-код` + carrier `<verdict path>#<remark id>` |
| 3 | the owner's new word during the work | on-topic → done in that work; another topic → may be a separate node | off-topic only | not a leftover: `Откуда: владелец <дд.мм.гггг>` |
| 4 | a red CI | «CI не записываем отдельными узлами»: repaired on the spot | never | — (record: F15) |
| 4b | a defect after acceptance that is not a red CI | F16 decided (a): fixed on the spot as a new task_id with `defect_found` (CLAUDE.md rule 4 already forbids reopening and names `defect_found` for a canon failure; F16 extends the same road to every post-acceptance defect), no node | never | — |
| 5 | a scope cut by a spec | legal only when the owner cut it «для экономии токенов» and that word is recorded in the spec with its date; otherwise done now or the owner is asked | only with her word | `экономия-токенов` + carrier `<spec path>`; the row is `Тип: доделка` |
| 6 | a live proof | her word 11.11.2026 (PROJECT «Командная работа» п. 9): the proof row goes to `live-runs` | yes, in `live-runs` | `живой-прогон` |
| 7 | a builder-noticed analog | F14 decided (a): the same as rows 1/2 — own code (inside the node's `Пишет в`) fixed now in the node's round; other code a `чужой-код` node | as rows 1/2 | as rows 1/2 (the builder names it in «Needed from integration»; the critic's verdict carries it as a remark) |

`leftover_criteria` (data, `tools/piles-vocab.json`) holds exactly `чужой-код`, `экономия-токенов`, `живой-прогон`, each
with a `word` field naming the owner's carrier (17.11.2026 / 11.11.2026). `занятый-файл` and `ждёт-события` are NOT
reasons (F18, F19 decided (a) by the owner, 17.11.2026):
- **occupied file** (F18 (a)): the fix is the same node's second round after the other batch merges, or is done now under
  D-0048 disjoint function lists or an `очередь: A → B` line (PROJECT «Командная работа» п. 3 already rules both roads);
  the node stays open and may hold its batch.
- **waits for an event** (F19 (a)): the node stays open and does a second round after the event; its batch waits.

Size is NOT a criterion (F2 decided (a)): a remark too big for one round is a SECOND fix round of the same node (same node
id; `attempt` grows only on a `rejected`).

Who judges (P27, AR-29 analog): the critic labels each remark `fix` or `чужой-код` in its verdict (§2.3); code refuses a
`чужой-код` label on a path inside the node's `Пишет в` (data: a path join, not wording); whether a remark is truly about
another topic when its path is outside is the critic's judgment, accepted by the Lead. A node leftover is confirmed on its
«Остатки» item by the owner or the batch's Lead (F5). Scope cuts: the critic-on-plan checks that every non-goal deferring
in-topic work quotes the owner's word (§5.10 (e)).

### 2.3 The machine layer (B1): the critic's remark carries a typed disposition; the ONE acceptance gate judges it

**The Lead's design, «ок» by the owner (W1); code point = F17 (a), moved to the one place every writer passes (R1).** Three
parts, all data checks:

1. **Verdict schema** (stream C). `tools/critic_verdict.schema.json` and `tools/critic_verdict_check.py`
   `validate_verdict` gain a REQUIRED array `remarks`:
   ```json
   "remarks": [{"id": "B1", "disposition": "fix"}, {"id": "N7", "disposition": "чужой-код", "path": "tools/session_context.py"}]
   ```
   Rules (new helper `_remark_errors(obj)` called from `validate_verdict`):
   - `remarks` is an array; EMPTY OUTCOME: `[]` is legal exactly when `blockers` and `fixes` are both empty (a clean
     `fit`); a `fit` may also carry only `чужой-код` remarks.
   - each item: `id` — 1-20 characters `[A-Za-z0-9._-]`, unique in the array; `disposition` — a key of
     `remark_dispositions` in `tools/piles-vocab.json` (`fix`, `чужой-код`), read through the LEAF module
     `tools/piles_vocab.py` `node_vocab()` (R2: never through `piles`); `path` — REQUIRED for `чужой-код`, a non-empty
     string ≤ 300 characters, no `..` segment, no line break; ignored for `fix`.
   - every entry of `blockers` and `fixes` starts with the `id` of one `fix` remark (its first whitespace-separated token,
     trailing `:` stripped); every `fix` remark is named by exactly one such entry; a `чужой-код` remark is named by none.
   - diagnostics stay ASCII-only (the file's invariant): `field 'remarks[3].disposition' invalid: expected one of the keys
     of remark_dispositions in tools/piles-vocab.json`; `field 'remarks[3].path' required when the disposition is the
     other-code key`; `entry fixes[2] names no fix remark: expected its first token to be the id of a remarks item with
     disposition fix`; the vocab unreadable → `cannot read tools/piles-vocab.json (<why>): remark dispositions not
     checked -- fix the vocabulary file` and exit 2 (never "every disposition valid", FR-59).
   - OLD verdicts (no `remarks`): `check_text` fails them with `missing required field: remarks`; given to the gate they
     are refused with the door `verdict: none -- verdict predates remarks`.

   **The import graph (R2, no cycle).** `tools/piles_vocab.py` (new, A1): stdlib only (`json`, `pathlib`), ONE function
   `node_vocab(root=None) -> dict` plus `CannotRun`-style exception `VocabError`; it imports no repo module. Importers:
   `piles.py` (`from piles_vocab import node_vocab, VocabError` and re-exports `node_vocab` so existing callers keep one
   name), `collect_intake.py` (B), `critic_verdict_check.py` (C). `piles.py` imports `critic_verdict_check` (A2) for
   `check_text`; `critic_verdict_check` never imports `piles`. Graph: `piles → critic_verdict_check → piles_vocab`,
   `piles → piles_vocab`; a leaf has no back edge, so running `piles.py` as `__main__` loads each module once. The checker
   stays self-contained in the sense of P42 (no shared stdin helper); importing a stdlib-only data reader is the AR-13
   price of one reader of the vocabulary. Test row (A1, `test_piles_form.py`): `python -B -c "import critic_verdict_check,
   piles"` and the reverse order both import cleanly; `piles_vocab.py` imports no repo module (an `ast` scan of its
   imports against the stdlib list).

2. **The acceptance gate (stream A2) — in (д), at commit-msg and in forge-check, the ONE place every writer of `принято`
   passes (R1).** Writers of a node's `принято` today: `piles.py status`, `wave.py merge --node` (through `status`), and a
   hand edit of the cell (`HAND_EDIT`, P40) — in a taken batch (в) masks the `Статус` cell, in an untaken one nothing is
   frozen. All three end in a commit; so the judgment sits in the commit gate, and `status`/`wave` only WRITE the line it
   reads.
   - **Transition (what is judged).** New `piles._accept_reds(ctx, msgs)` inside `check_form`: a node row of any batch file
     touched by the commit (or the range, in CI) whose `status_word` is `принято`, while NO row with the same id in the
     same pile at the base had `принято` → "accepted in this commit". Identity = (slug, id) over every batch file of the
     pile at the base (a row moved between batch files while already `принято` is not an acceptance; F20's move of open
     rows carries no `принято`).
   - **Requirement.** For every accepted node the message (commit-msg: `--msg-file`; CI: `range_messages`, pooled, as
     `piles-skip:`) carries a line in PROSE position (fenced / quoted lines do not count):
     `verdict: [<slug>/<N>/<id> ]<repo-relative path>` or `verdict: [<slug>/<N>/<id> ]none -- <why>`; the node part may be
     omitted only when the commit accepts exactly ONE node; two or more → every line names its node. Optional
     `owner-word: [<slug>/<N>/<id> ]<кто, дата>` (P13: the owner's word passes the whole call and is recorded).
     The lines are read by ONE reader, new `piles.prose_lines(msg, keyword)` (A2): it generalises the prose-position scan
     of `door_lines` (`:1025-1054`, md_regions, fail-closed when the scanner degrades); `door_lines` is rewritten to call
     it (same output), A3's `приток:` and K's `stamp-skip:` / `rule-census-raise:` call it too (AR-15: one reader of
     commit-message door lines).
   - **For a path line**, `piles._verdict_problem(root, nd, path, owner_word, blob_reader) -> str | None`:
     - the file is read from the COMMITTED tree — the index in commit-msg (`git show :<path>`), HEAD of the range in CI —
       never from a machine path (F24 (a): the critic's report is committed no later than the commit that accepts on
       it); an absolute path or a path with `..` → refused;
     - the shape through `critic_verdict_check.check_text` (one reader of the shape);
     - `verdict` = `blocker` → refused (F-a; a blocker verdict is no basis to accept) unless an `owner-word:` line names
       the node;
     - for every `чужой-код` remark: normalise its `path` and every token of the node's `Пишет в` (`_norm_token`:
       repo prefix of an absolute path stripped, `\` → `/`, `./` stripped, a trailing function list dropped) and compare
       with `tokens_overlap`, CASE-FOLDED; any overlap → refusal unless `owner-word:` names the node.
   - **Writers.** `piles.py status <slug> <N> <id> --set принято --hash <h> --task <t>` gains EXACTLY ONE of
     `--verdict <path>` / `--no-verdict "<why>"`, and an optional `--owner-word "<кто, дата>"`; it runs the SAME
     `_verdict_problem` before writing (an early refusal, the same texts, reading the working tree because nothing is
     committed yet) and prints in its `Next:` hint the exact lines to put in the commit message. `wave.py merge … --node`
     gains the same three, forwards them to `status`, and writes the lines into its status commit message
     (`record_node`, `:264`: `"piles: … принято (<task>)\n\nverdict: <slug>/<N>/<id> <path>"`), which then passes the
     commit-msg gate like any commit (P30). A hand edit is legal and passes on the same line — `HAND_EDIT` gains: "(a cell
     moved to принято needs a "verdict:" line in the commit message -- PROJECT.md «Командная работа» п. 9)".
   - `--set` to anything but `принято`, or a BATCH-level call, takes none of the three (refused like `--hash` today).
   - **Refusal texts** (FR-1/FR-2; nothing is written on any refusal):
     - (д) no line: `<path>: node <slug>/<N>/<id> becomes «принято» in this commit, but the message names no verdict for
       it -- expected a line "verdict: <slug>/<N>/<id> <critic report path>" or "verdict: <slug>/<N>/<id> none -- <why>"
       (the node part may be dropped when the commit accepts one node); piles.py status --verdict and wave.py merge
       --verdict write it for you (PROJECT.md «Командная работа» п. 9)`.
     - (д) ambiguous short line: `<path>: this commit accepts <k> nodes (<ids>) and the line "verdict: <…>" names none of
       them -- write one "verdict: <slug>/<N>/<id> …" line per node`.
     - file not committed: `<path>: the verdict <p> is not in the committed tree -- commit the critic's report (it is the
       acceptance record) in this commit or before it; or write "verdict: <node> none -- <why>"`.
     - invalid shape: `the verdict <p> is not a valid critic verdict: <the check's lines, first 5> -- the critic re-emits
       it (tools/critic_verdict_check.py <p> must exit 0); a verdict written before remarks existed: "verdict: <node> none
       -- verdict predates remarks"`.
     - blocker (F-a): `the verdict <p> says "blocker" -- a node is accepted on a fit or fit_with_fixes verdict; run the fix
       round and the re-review, or record the owner's word: "owner-word: <node> <кто, дата>"`.
     - the core refusal: `<slug>/<N> <id>: the verdict <p> marks remark <rid> as «чужой-код» on <path>, which is inside the
       node's «Пишет в» (<token>) -- a remark about the node's own code is fixed in this node (PROJECT.md «Командная работа»
       п. 9). Expected: every «чужой-код» remark names a path outside «Пишет в». Doors: run a fix round and have the critic
       mark it fix; if the code is really another topic's, have the critic name that exact path; or record the owner's word:
       "owner-word: <node> <кто, дата>"`.
     - `status` / `wave` add `nothing was written` / `nothing was merged` to the same texts; wave refuses at step 0, before
       any push, exit 2, when `--node` is given without `--verdict`/`--no-verdict`.
   - The informed passes (FR-4) are the record itself: `verdict: … none -- <why>` and `owner-word:` lines; calibration check
     33 counts them (§5.12 (ii)).
   - **Base unreadable** (no git, a broken base): the transition cannot be told → the (в) precedent: a NOT CHECKED note
     `приёмка не проверена (<why>); this commit is not blocked by the acceptance rule` in commit-msg; in CI (full history,
     `fetch-depth: 0`) an unreadable base is a broken run → red (FR-59: named, never a silent pass).
3. **The back-reference** (stream A2, in (д)). A NEW node row whose `Откуда` is `остаток <parent> · чужой-код · <verdict
   path>#<rid>` is red unless: the verdict file exists in the committed tree and passes `check_text`; remark `<rid>` exists
   with disposition `чужой-код`; the row's `Пишет в` overlaps the remark's `path`. `экономия-токенов` needs `· <spec path>`
   naming an existing file (whether it quotes the owner's word is the critic-on-plan's judgment — FR-12). `живой-прогон`
   needs no carrier and the row must sit in pile `live-runs`.

Error direction (a reused function in a more consequential role, designer rule 1):
- `tokens_overlap` (today the (б) overlap gate) becomes part of the acceptance gate. It may REFUSE a valid remark (false
  red; door: the critic names the exact path, or `owner-word:`), never PASS a `чужой-код` remark inside the owns.
  Adversarial inputs that must stay REFUSED (rows in `tools/test_piles_close_gate.py`): the remark path absolute
  (`C:/QAFactory/forge-repo/tools/piles.py`) vs a relative owns token; backslashes; `./tools/piles.py`; another case
  (`Tools/Piles.py`); a trailing function list against owns on the same file with another function list (file-level
  overlap: refused); a directory `tools/` against owns `tools/piles.py`; a glob `tools/*.py`. Must PASS: a path outside the
  repo; a path in another directory; owns `нет`/`—`. Refused at the schema: an empty path, `..`, a line break, a
  disposition not in the list.
- `status_word` in the transition detector may OVER-require (a row moved across piles while `принято` looks new → a
  `verdict:` line is asked; door: `verdict: <node> none -- moved from <slug>`), never UNDER-require for a cell newly written
  `принято`. Adversarial cells that must be judged as accepted: `Принято` (another case), `принято: abc1234`,
  `принято:abc1234` (no space), `принято (t-1)`; cells that must NOT pass as anything: `принятo` (Latin o) and `**принято**`
  — `_node_reds` already refuses an unknown first word (P7).
- `prose_lines` errs SAFE: a degraded scanner counts NO line (fail-closed, as `door_lines`), so a `verdict:` inside a fence
  never satisfies the gate.

Escape that remains (stated, t-920 B1): a Lead who files a remark as `Откуда: находка` with a new finding file, or as
`план`, bypasses the back-reference. It is caught by the flow brake (§2.4) and by calibration check 33 item (iii)
(§5.12): new rows of a pile whose `Пишет в` overlaps a node of the same pile accepted in the same 7-day window.

**Alternatives weighed (F17).** (b) A stop-time check in `dod_gate.py` with a `judged-owns:` dispatch line — earlier and
cheaper per merge, but it does not bind the verdict to the node's acceptance and widens three mechanism files. (c)
Discipline + calibration — not on the path. After R1 the chosen point is the commit gate (д), which every writer passes;
`status`/`wave` are the convenient writers of its line. Recommended (a), Lead's fork F17.

### 2.4 The flow brake (B2): judged when a WORKED batch gains a row, shown at SessionStart and in `status`

forge/7 never closes (P28) and accepts nodes through the node branch of `status` (P29), so no close-time brake can see
it. The brake sits where a row is ADDED — the commit-msg `piles.py check` road — and the counter is printed where the
Lead looks every session.

- **Counter (stream A3), new `piles.flow(root, window_days=7, slug=None, n=None) -> Flow | None`.** ONE
  `git log -p --since=<window> -- plans/piles/<slug>/batch-*.md` pass. "Opened" = the first commit in the window where a
  node id appears in ANY batch file of the pile (keyed by `(slug, id)`: a move between batch files of one pile is not an
  open); "closed" = the first commit where its status word becomes `принято` or `отклонено`; attribution = the file the
  row stands in at the end of the window. `None` (git cannot run, timeout) → the caller prints `не измерено (<why>)`,
  never `0` (FR-41).
- **Gate (stream A3), in (д), new `_flow_reds(ctx, msgs)`. The counted set (R3):**
  - **Judged batches** = batch files not «закрыта» that are being WORKED: the header status at the base is in `FROZEN`
    (taken, P32 `piles.py:1589`), OR the batch closed ≥ 1 node in the window (the forge/7 case: worked untaken).
  - **NOT judged**: an untaken batch that closed nothing in the window — an intake batch only receiving rows (PROJECT
    «Командная работа» п. 2's prescribed road for every finding, `collect_intake`'s rows, a batch opened as
    `batch-<N+1>`). `summary` prints such batches on one line `входящие за 7 дней: <slug>/<N> +<x>, …` (shown, not judged).
  - **Counted rows** in a judged batch: every NEW node row (new = its id absent from every batch file of the pile at the
    base) EXCEPT rows `Откуда: миграция` (this spec's own moves, §3) — F13 (a) re-checked against this scope: still every
    added row whatever its `Откуда` (the self-label escape stays closed), with the one migration exemption.
  - The gate: for a judged batch gaining ≥ 1 counted row, when `opened > closed` over the window INCLUDING this commit,
    the commit is red unless its message carries `приток: <slug>/<N> -- <why>` (read by `prose_lines`; one line per batch;
    reason non-empty, ≤ 120 characters, no line break).
  - Refusal text: `<path>: this commit adds node row(s) <ids> to <slug>/<N>, a batch being worked (taken, or it closed
    <c> node(s) in the last 7 days), which over the last 7 days opened <a> and closed <c> (the net would be +<x>) -- a
    batch being worked that grows must say why (PROJECT.md «Командная работа» п. 9). Expected: fix the remark in its own
    node's round instead of adding a row, or add the line "приток: <slug>/<N> -- <why, per added row>" to the commit
    message`.
  - A window git cannot read → a NOT CHECKED note `поток не измерен (<why>); this commit is not blocked by the flow
    rule` (the (в) precedent; FR-59); calibration counts these notes.
  - Edge rows (each a row in `tools/test_piles.py`): (1) a finding row into an untaken batch with 0 closes → green, no
    `приток:`; (2) the same batch after one `принято` in the window, gaining a row with opened 2 > closed 1 → red; with
    `приток:` → green; (3) 30 `миграция` rows into a worked batch → green (exempt); (4) a mix of 1 `находка` + 5
    `миграция` rows into a worked batch with opened 1 + earlier opens > closed → judged on the `находка` row only; (5) a
    worked batch whose last close was 8 days ago → not judged (outside the window); (6) a taken batch gaining a row — (в)
    refuses it first unless `piles-skip: в`, then the flow gate judges it; (7) a row moved from forge/7 to a new batch
    file of `forge` → not an open (same `(slug, id)`).
- **Shown.** `piles.py summary`: `поток узлов за 7 дней: открыто N / закрыто K; итог ±X` + one line per growing judged
  batch + the `входящие` line; `piles.py status` prints after its write `поток пачки <slug>/<N> за 7 дней: открыто a /
  закрыто b`; `tools/session_context.py` (SessionStart) prints ONE line `поток узлов за 7 дней: открыто N / закрыто K
  (итог ±X); растут: <up to 3 judged batches with their net>`; any exception or a git call over 5 s → `поток узлов: не
  измерено (<why>)`; SessionStart never fails on it.
- `--all` and `close` print the counter and judge nothing by it; CI `check --base` judges the pushed range with the
  range's messages.
- `piles-skip: д -- <reason>` skips the flow gate with the rest of (д); `приток:` is its own narrower door.

**Batch 7 itself** (fork **F20**, Lead; recommended): forge/7 is closed as a CONTAINER and its 38 open rows move to
batches with a real scope. What `close` needs, in order: (1) the open rows are cut from forge/7 into the new files (an
untaken file is not frozen; keyed by `(slug, id)` the move is not an "open"; card «Строки» cells follow); (2) `piles.py
take forge 7 --who <Lead>`; (3) `piles.py status forge 7 --set принято`; (4) `piles.py close forge 7 --hash <the merge
commit of its last accepted node>` — the «Остатки» and «Живые доказательства» gates must pass (legacy items by the old
form, §6 E20). Precedent: forge/3 and forge/6 (P28). Whether a node may be accepted in an untaken batch at all is F20's
alternative (b). FG7-52's row moves with the others, or is absorbed by K (F23).

### 2.5 Expected effect, told to the owner (N9)

With F14 and F16 decided (a): rows 1, 7 and 4/4b stop for sure — 51 + 14 + 27 = 92 of 206 = **44.7 %** of the leftover
stream; rows 3 and 5 stop only in their on-topic / not-for-tokens part, and t-906 did not split them → the upper bound is
92 + 31 + 24 = 147 = **71.4 %**. What stays legitimately: other code 20, calibration/process 27, new ideas 8, live proofs
4 → at least 59 = **28.6 %**. The flow line makes the real number visible from the first week (§2.4).

---

## 3. Registries into nodes (one stream each)

Common rules: a migrated node has `Откуда: миграция`, a `Тип`, an `Исполнитель`, and lands in the UNTAKEN batch of its
pile (none → `batch-<N+1>-<slug>.md` `ожидает` + card row, PROJECT п. 2). A stale row is not migrated: its verdict and
evidence go in the commit message and the pile's untaken batch «Ход». "Stale" is judged by the Lead from a scout's
evidence (P27).

| stream | registry | before | rule for each item | after |
|---|---|---|---|---|
| M1 | findings in no batch | **152 (69 undated)** (P12) | done → finding file deleted (F10); duplicate of a live node → named in that node's «Что» (untaken) or «Ход» (taken); live → node row `Откуда: находка <file>`; unsure → `Тип: неразобран`, `Исполнитель: scout → Lead` | 0 orphans; then H drops `FINDINGS_FROM` |
| M2 | `docs/tasks/lead-queue-fable.md` | 12 items + 2 lines; 10 done, 2 open (P14) | the 2 open → no new node (FG7-51, FG7-49 hold them, P15); a «Ход» line names the queue items they absorb | per fork **F7** (Lead) |
| M3 | ~~`design/factory-rules-debt.md`~~ | — | REMOVED: the rows are FIXED by `docs/tasks/specs/20261117-rules-debt-fix-spec.md`. Tell that stream: (1) the open count is **44 by the file's own rows**, not "25" (P17); (2) F8 decided (a): its LAST commit deletes the file with its readers (G1-10, K0.15, `factory-rules.md:230, 305`, `piles.debt_warnings`, `test_piles_close_id.py`); a future unfixed violation is a node `Тип: долг` (§5.6, landed by D) | — |
| M4 | plans of big ideas with no pile | 6 (t-895; P25) | live → a batch with `план:` in the topical pile (F11); done/abandoned → one header line `архив: <дата>, <причина>` | 0 plans without a batch or an `архив:` line |
| M5 | DAG files under `docs/tasks/` | 3 (P24) | `factory-fixes.md` → `архив:`; `test-diet.md` → its open nodes become rows of `package-ci` batch 4 (each checked against that batch's rows first); `архив:` + pointer; `onboarding-streams-…` → a WAVE VIEW header line | 0 node tables outside `plans/piles/` |
| M6 | `plans/BACKLOG.md` | **296 open ids** (P26) | unchanged archive | unchanged |

---

## 4. `tools/piles.py` after the change

Readers of `piles.py` (Grep `import piles|from piles|piles\.py|piles_split|backlog_tree` over `tools/*.py`, `.githooks/*`,
`.claude/settings.json`, `.github/**` → 42 files, 26 tests — round 1): `.githooks/commit-msg:40` (`check --msg-file`,
re-read r3), `.github/workflows/forge-check.yml:84` (`check --base`, re-read r3), `.claude/settings.json:156-157, 175-176`,
`tools/wave.py:254` (`status … --set принято`), `tools/backlog_tree.py`, `tools/compact_snapshot.py:350-353`,
`tools/forge_metrics.py`, `tools/collect_intake.py`, `tools/piles_split.py`, `tools/canon_clock.py:28`,
`tools/ci_read_common.py:10`, `tools/md_table.py`, `tools/conftest.py`, `tools/hook_liveness_probe.py:942-961, 1425`,
`tools/worktree_sweep.py:7`, `tools/mechanism_gate.py:254`; NEW readers after this spec: `tools/session_context.py`
(`flow`, A3), `tools/rule_pointers.py` (`prose_lines`, `range_messages`, imported lazily in its CLI only, K). NOT a
reader any more in this design: `critic_verdict_check.py` (it reads `piles_vocab`, R2).

| piece | verdict | what changes (stream) | readers / effect |
|---|---|---|---|
| `summary` | changes | + flow lines, + `входящие` line, + `без типа: T` (A3) | calibration check 33 reads it |
| (а) placement | unchanged | — | commit-msg, forge-check |
| (б) overlap | unchanged | — | commit-msg, forge-check |
| (в) frozen | changes (A1) | `_frozen_lines` drops the cells under a header named `Тип` or `Откуда` (stripped, case-folded) from the header row and every row of a table in «Узлы»; `status_col` is computed on the reduced cells | commit-msg, forge-check; `test_piles_frozen.py` rows |
| (г) backlog | unchanged | — | — |
| (д) form | changes | A1: `_new_node_rows`, `_node_origin_problem`, `_plan_problem`; A2: `_accept_reds` (R1), `_verdict_problem`, the `остаток` carriers, `_item_why` without the `перенос:` form for NEW items, `узел:` back-reference + `подтвердил:` (F5), `prose_lines`; A3: `_flow_reds` (R3) | commit-msg, forge-check, compact snapshot (`leftovers_unowned` keeps its signature) |
| (е) findings | changes after M1 (H) | when the baseline is 0: `FINDINGS_FROM` and the WARN branch removed | commit-msg, forge-check |
| `take` | unchanged | — | integrator |
| `close <slug> <N>` | changes (A2, A3) | `узел:` accepted with the back-reference and `подтвердил:`; legacy `перенос:` by the old form, new ones refused (§6 E20); prints the batch's flow | integrator |
| `close --id` | unchanged | `debt_warnings` unchanged until the debt-fix spec deletes the file (F8 (a), M3) | — |
| `status` | changes (A2, A3) | node `--set принято`: `--verdict`/`--no-verdict`/`--owner-word`, early `_verdict_problem`, prints the commit lines; `HAND_EDIT` text (R1); prints the batch's flow | `wave.py` (changes in A2) |
| `door_lines` | changes (A2) | calls the new `prose_lines(msg, "piles-skip")`; same output | commit-msg, forge-check |
| `board`, `release` | unchanged (refused aliases) | — | stale allow lines → H (Lead) |
| `node_vocab` | MOVES to the leaf `tools/piles_vocab.py` (A1, R2); `piles` re-exports it | ONE reader of `tools/piles-vocab.json` (`node_types`, `node_origins`, `leftover_criteria`, `remark_dispositions`, `confirmers`, `intake_default`, `carry_retired`); absent/unreadable/invalid → `VocabError` naming the path and the broken key (FR-59) | `piles.py`, `collect_intake.py` (B), `critic_verdict_check.py` (C) |
| new `flow()` | added (A3) | §2.4 | `summary`, `status`, `close`, `_flow_reds`, `session_context.py` |
| new `legacy_carries()` | added (A2) | §6 E20 | `check_leftovers`, `check_proofs` |

Mechanism list (Lead, in A2's commit — not deferred to H, R2/F-l): `tools/mechanism_gate.py` `MECHANISM_PREFIXES` gains
`tools/piles-vocab.json` (data deciding a gate, like `worktree-junk.json`), `tools/piles_vocab.py`,
`tools/critic_verdict_check.py`, `tools/critic_verdict.schema.json` (live wiring closure: imported by / deciding
`piles.py`'s gate, like `md_table.py`). K's files join in K's commit (§8.4).

Checks this spec adds or alters — owner served and class (AR-29 / P27; forge checks, classed in its words):

| check | owner it serves | class |
|---|---|---|
| (в) masks the `Тип`/`Откуда` cells | data (code) | shape |
| (д) `Тип` ∈ list, `Откуда` form, `план:` path exists, finding of `находка` exists | data (code) | shape / presence / xref |
| (д) `остаток` parent exists; `чужой-код` verdict ref resolves to a `чужой-код` remark whose path the row writes | data (code) | xref |
| (д)/close `узел:` item carries `подтвердил: <владелец \| Lead пачки>, <дата>` (F5) | intent (owner) or judgment (batch Lead) — presence only | presence |
| (д) a cell moved to `принято` carries a `verdict:` line; a path line resolves to a committed, valid, non-blocker verdict with no `чужой-код` remark inside `Пишет в` (R1) | data (code): presence, shape, a path join; the verdict's content is the critic's judgment, accepted by the Lead | presence / shape / xref |
| (д) flow: `приток:` present when a WORKED batch grows (R3) | judgment (the Lead's explanation; content accepted at calibration) | presence |
| `critic_verdict_check` `remarks` shape, disposition ∈ list, ids joined to `blockers`/`fixes` | data (code); the label is the critic's judgment | shape / xref |
| `verdict: none` / `owner-word:` / `приток:` reasons | judgment (Lead) / intent (owner) — presence only | presence |
| close: legacy `перенос:` by the cutover commit; new `перенос:` refused | data (code) | shape (history join) |
| §8: pointer resolves; stamp hash vs section hash; census ratchet | data (code); whether a carried block still MEANS the main rule is the re-stamper's (a role), accepted by the Lead | xref / presence / count |
| "is the remark truly another topic" (path outside) | judgment (critic, accepted by Lead) | not code |
| scope cut quotes the owner's token word | judgment (critic-on-plan) / intent (owner) | not code |

---

## 5. Rule texts that change (exact text; ONE home + pointers — the first instance of §8)

**The one home of the leftover rule** is PROJECT.md «Командная работа» п. 9, the paragraph headed «**Остатков нет по
правилу**», standing ON ITS OWN LINE (R6; it replaces «Остатков в идеале нет вовсе», which today stands mid-line at
`PROJECT.md:333`, P43). Every other carrier points to it with ONE pointer form (§8.2): English carriers
`rule: PROJECT.md § **Остатков нет по правилу**`, Russian carriers `правило: PROJECT.md § **Остатков нет по правилу**`;
the human-readable «PROJECT.md «Командная работа» п. 9» may stand beside it; no carrier restates the rule. In the window
D → K the five pointers are POINTERS rows of the axis-31 test (substring, P33) AND resolve under §8.2's grammar (the home
at a line start) — the two checks agree on the same pointer; after K the hand rows go (§8.2.3).

Order with the parallel specs: boot-by-topic and architect-tier land first; every edit below is anchored by its quoted
OLD text and applied wherever that text stands at landing (PROJECT.md or `docs/TEAMWORK.md` § with the same number,
fragment by fragment: 5.1 edits fragment 2c; 5.3 edits 9d (PROJECT) and — per F12 (a) — places the gate-held clauses in
the home of 9a; F4's form change and F5's confirmers edit 9a and 9c together). AGENTS.md is regenerated (`python
tools/agents_md.py`). The test anchors of P22 stay byte-identical.

**5.1 PROJECT.md «Командная работа» п. 2 (fragment 2c)** — from «**Находка сразу попадает в пачку** (D-0044)» to «…и
находка ложится туда.» → replace with:

> **Всё в кучках** (слово владельца 17.11.2026): единственный реестр работы — узлы пачек. Находка — улика и описание, не
> работа: тем же ходом, что файл в `findings/`, она получает УЗЕЛ (строку «Узлы» с `Тип` и `Откуда: находка <файл>`) в
> НЕвзятой пачке своей кучки; нет такой — пишущий открывает `batch-<N+1>-<slug>.md` со статусом «ожидает» и строкой в
> таблице «Пачки» карточки. Тип узла — слово из `tools/piles-vocab.json`; большая идея — своя пачка с парой
> `план: <путь>` в шапке. Красный CI — не находка и не узел (п. 9).

**5.2 PROJECT.md «Командная работа» п. 4** → append after «…у находки до этого `id: —`.»:

> Очереди вне кучек (очередь Lead, графы задач в `docs/tasks/`, планы идей без пачки) не ведутся: их работа — узлы
> (спека `docs/tasks/specs/20261117-everything-in-piles-spec.md`).

**5.3 PROJECT.md «Командная работа» п. 9 (fragment 9d) — THE HOME** — the span from «**Остатков в идеале нет вовсе**» to
«…строкой с исполнителем.» is replaced; the text before the span («…доказательств не должно.») ENDS its line, and the home
STARTS a new line indented like the item's other lines (3 spaces), so its bold lead-in is at a line start (R6). No
wrapped line inside the home may begin with `**` (it would end the section, §8.2.2). Text — 5.3a (always in PROJECT.md):

> **Остатков нет по правилу** (слово владельца 17.11.2026, по происхождению):
> — замечание критика или найденный билдером аналог о коде темы узла (то, что в его «Пишет в»), минорное тоже, чинится
> в фикс-раунде того же узла: не узел и не строка «Остатков»;
> — замечание критика или аналог билдера о чужом коде (вне темы узла) можно оставить узлом с основанием `чужой-код`;
> — новое слово владельца по теме идущей работы делается в этой работе; слово на другую тему можно завести узлом
> `Откуда: владелец <дд.мм.гггг>`;
> — красный CI и дефект после приёмки чинятся на месте (новая задача и `defect_found` в журнале) и узлом не
> записываются;
> — урезать работу спекой можно только словом владельца «для экономии токенов», записанным в спеке с датой; урезанное —
> узел `Тип: доделка` с основанием `экономия-токенов`; иначе — сделать сразу или спросить владельца;
> — живое доказательство уходит в `live-runs` узлом с основанием `живой-прогон` (см. ниже);
> — занятый файл и ожидание события — не основание: узел остаётся открытым и делает второй раунд (п. 3).
> Размер — не основание: большой фикс — второй раунд того же узла. Как это проверяет код — 5.3b.

5.3b — the gate-held clauses (F12 (a): the owner's boot-by-topic criterion applied clause by clause: what a gate holds
moves with 9a). WHEN `docs/TEAMWORK.md` exists at D's landing: appended to TEAMWORK § 9 and the home's last sentence reads
«Как это проверяет код — правило: docs/TEAMWORK.md § 9.»; WHEN it does not exist (boot-by-topic not landed): appended to
the home in PROJECT.md in place of that sentence (both worlds; boot-by-topic's later move carries it, its row 9a):

> Код держит так: в вердикте критика у замечания `disposition: fix` или `чужой-код` с путём; узел принимается коммитом
> со строкой `verdict: <узел> <файл вердикта>` или `verdict: <узел> none -- <почему>`, и «чужой код» внутри «Пишет в»
> узла (д) не примет; узел-остаток — строка «Узлы» с `Откуда: остаток <узел> · <основание>[ · <носитель>]`, строка
> «Остатков» — `узел: <id> | подтвердил: <владелец или Lead пачки>, <дд.мм.гггг>`. Пачка в работе, которая за 7 дней
> открыла больше узлов, чем закрыла, принимает новую строку только со строкой `приток: <кучка>/<N> -- <почему>` в
> сообщении коммита; поток печатают SessionStart, `piles.py summary` и `status`.

(9a/9b/9e/9f stay; 9c «перенос подтверждает **человек**, не агент сам» gains: «узел-остаток подтверждает владелец или Lead
пачки (слово владельца 17.11.2026)»; under F4 the `перенос:` wording of 9a/9f becomes `узел: <id>` with the
back-reference — text in stream D.)

**5.4 PROJECT.md «Командная работа» п. 11** → append after «…исполнителю не нужно искать по кучкам.»:

> У узла названы `Тип` и `Откуда`; узел, рождённый работой другого узла, называет его и основание.

**5.5 PROJECT.md «Как принимается изменение пакета» п. 2** — the clause «красный пайплайн на `main` (все причины разом —
`python -B tools/ci_read.py why`) — находка в `findings/` своей кучки и починка до следующего пуша» → «красный пайплайн на
`main` (все причины разом — `python -B tools/ci_read.py why`) — починка на месте до следующего пуша, без находки и без
узла: коммит починки называет красный прогон, а если его вызвал принятый узел — строка `defect_found` в журнале (слово
владельца 17.11.2026; правило: PROJECT.md § **Остатков нет по правилу**)».

**5.6 PROJECT.md «Как принимается изменение пакета» п. 4, last sentence** «Нарушение правила, которое не чинится сейчас, —
строка в `design/factory-rules-debt.md`.» → «Нарушение правила, которое не чинится сейчас, — узел `Тип: долг` в кучке,
чья зона (слово владельца 17.11.2026).» (F8 (a), decided; the debt file itself is deleted by the debt-fix spec, M3.)

**5.7 CLAUDE.md rule 4a, first sentence** «…is tracked as a markdown DAG — a pile's batch file or a file under docs/tasks/:
nodes/statuses/tiers as the carrier;» → «…is tracked as nodes of a pile's batch file (the only registry of work, the
owner's word 17.11.2026): nodes/statuses/tiers as the carrier; a file under docs/tasks/ may group pile nodes into waves
but holds no node of its own;»

**5.8 CLAUDE.md rule 9, the clause** «fix now, or EXPLICITLY put the remainder in the queue/log» → «fix now, or EXPLICITLY
open a node for the remainder where the leftover rule allows one (rule: PROJECT.md § **Остатков нет по правилу**)». (The
K-OWN key of rule 9 untouched.)

**5.9 CLAUDE.md rule 12 Cost gates, the clause** «a fix round runs in a FRESH worker carrying only the diff and the
verdict» → «a fix round runs in a FRESH worker carrying only the diff and the verdict, its `owns` widened to every path
the verdict's `fix` remarks name (what may stay out: rule: PROJECT.md § **Остатков нет по правилу**)». (The COST anchor
untouched.)

**5.10 docs/tasks/critic-diff-brief.md** (pointers; the K-OWN keys of q7 and q12(d) stay byte-identical):
- q4, from «An analog outside the node's `owns` that this round does not fix» to «(F6-30).» → «Every remark and analog
  gets one line in the verdict's `remarks` (`fix`, or `чужой-код` with its `path`); which remark may stay out of this
  round: rule: PROJECT.md § **Остатков нет по правилу**.»
- q7, «Each is a finding with a severity — blocks / fix before merge / queue — never a style pass and never "I don't
  like it".» → «Each is a finding with a severity — blocks / fix in this round — never a style pass and never "I don't
  like it"; what may stay out of the round: rule: PROJECT.md § **Остатков нет по правилу**.»
- q12(d), «a fix in this round or a node with an id and an owner;» → «a fix in this round, or a `чужой-код` remark where
  the leftover rule allows one (rule: PROJECT.md § **Остатков нет по правилу**);» (the next clause unchanged).
- C-key, appended to q12 as (e): «(e) On a plan gate: a non-goal that defers work of the spec's own topic is legal only
  with the owner's word quoted with its carrier and date; otherwise it is a finding (rule: PROJECT.md § **Остатков нет по
  правилу**).»

**5.11 .claude/agents/critic.md** (Lead places; sweep of the same artifact: rules 5, 17, 19). The edit owes the critic
exam BEFORE the commit (critic.md rule 10, `.claude/agents/critic.md:58-62`: PROCESS/CRITIC_EXAM.md) — the Lead runs it
and writes its result line; it is in D's DoD (F-f):
- rule 5 «Axes of the defect left uncovered and not queued = a NEEDS-WORK finding.» → «Axes of the defect left uncovered
  and neither fixed nor carried where the leftover rule allows (rule: PROJECT.md § **Остатков нет по правилу**) = a
  NEEDS-WORK finding.»
- rule 17, after «trail (read + reruns);» insert «remarks (one item per blocker and fix: `id`, `disposition` `fix` or
  `чужой-код`, `path` for `чужой-код`);».
- rule 19, «leaves your verdict as a fix of this round or as a proposed node with its owner,» → «leaves your verdict as
  a fix of this round or as a `чужой-код` remark where the leftover rule allows one (rule: PROJECT.md § **Остатков нет
  по правилу**),».

**5.12 plans/builder-rules.md п. 1**, the clause «нужное в чужом файле — не правь, опиши в «Needed from integration» (файл,
точный текст/код, зачем)» → «нужное в чужом файле — не правь, опиши в «Needed from integration» (файл, точный текст/код,
зачем): это применяет интегратор или Lead В ТОМ ЖЕ РАУНДЕ; аналог в коде темы узла (в его «Пишет в») чинишь сам в этом
раунде; что может остаться вне раунда — правило: PROJECT.md § **Остатков нет по правилу**» (F14 (a)).
**.claude/agents/designer.md** (Lead places): rule 2, append «A non-goal that defers work of the spec's own topic carries
the owner's word quoted with its carrier and date, or is a fork (rule: PROJECT.md § **Остатков нет по правилу**).»
**PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md** (Lead places): check 33 line 1026 — the «Живые доказательства» form gains
`узел: live-runs/<N>/<id>`, `перенос:` only for items before the cutover; check 33 gains items: (i) the flow line of
`summary`, a second week with a positive net of a judged batch is a finding; (ii) count of `verdict: none`,
`owner-word:`, `приток:` lines and the `не измерено` / `не проверена` notes in the window; (iii) new rows whose `Пишет в`
overlaps a node of the same pile accepted in the same window (the B1 escape detector); (iv) a semantic read of the
pointer carriers against the home; (v) §8.6. Check 39 line 1095 — «without `сделано:` / `узел:` / `перенос:`» → «without
`сделано:` / `узел:` with `подтвердил: <владелец | Lead пачки>, <дата>` (a `перенос:` only for an item before the
cutover)».

**5.13 plans/piles/_template/batch.md** — the node table gets the two columns; the «Остатки» comment loses `перенос:`
and gains `узел: <id> | подтвердил: <владелец | Lead пачки>, <дата> — строка узла: Откуда: остаток <этот узел> ·
<основание>` and the pointer `правило: PROJECT.md § **Остатков нет по правилу**`; the header comment gains `план: <путь>`.
(The template becomes part of the scan set, §8.2.4.)

**5.14 The instance check for the leftover rule (B5)** — `tools/tests/test_role_carriers_one_owner.py`, stream D (lands
before K; K turns its pointer rows into the scan, §8.2.3):
- OWNER_KEYS + `("teamwork:leftovers", "PROJECT.md", "чинится в фикс-раунде того же узла: не узел и не строка «Остатков»")`
  — a RUSSIAN copy in any other scanned file turns red.
- POINTERS + five rows, each `(carrier, "<rule|правило>: PROJECT.md § **Остатков нет по правилу**", "PROJECT.md",
  "**Остатков нет по правилу**")` for carriers `docs/tasks/critic-diff-brief.md`, `.claude/agents/critic.md`, `CLAUDE.md`,
  `.claude/agents/designer.md` (`rule:`), `plans/builder-rules.md` (`правило:`).
- new parametrised `test_retired_leftover_text_is_gone` over RETIRED = «blocks / fix before merge / queue», «a fix in this
  round or a node with an id and an owner», «or as a proposed node with its owner», «put the remainder in the queue/log»,
  «Остатков в идеале нет вовсе», plus its negative control.
- new row `test_leftover_home_starts_its_line`: a line of PROJECT.md, leading whitespace stripped, STARTS with
  `**Остатков нет по правилу**` (exactly one such line) — the R6 instance, until K's resolver takes over.
- Error direction: K-OWN errs to a FALSE PASS across languages (the named blind spot; calibration item (iv), critic
  question 6); K-PTR errs SAFE; RETIRED errs to a false pass on NEW wording of the old rule.

---

## 6. Edges (behaviour + the invariant it protects)

| # | edge | behaviour | invariant |
|---|---|---|---|
| E1 | a taken batch during migration | not migrated by default (F9); the (в) mask makes adding the columns legal | (в) still refuses every other change to frozen text |
| E2 | another developer's piles and branches | migration touches only batches with `взял: —` on `origin/main`; another branch's untaken batch is skipped and listed | no session writes another session's uncommitted paths |
| E3 | a finding naming two piles | one home: the pile of the node's `Пишет в`; the other pile gets a sibling node only when it has its own work | an id lives in one pile |
| E4 | a node with no owner pile | `forge` when its files are outside the package, else the nearest zone by the Lead's judgment; never a new pile without the owner (F11) | no work without a home |
| E5 | closed batches (67) | never rewritten | history is append-only |
| E6 | status words with text after the word | unchanged; the one reader takes the first word | one vocabulary, one reader |
| E7 | the widget (`backlog_tree.py`) | reads statuses through `piles`; JSON unchanged; optional node key `type` | the pane never disagrees with `piles` |
| E8 | TEMPORAL: `tools/piles-vocab.json` / `tools/piles_vocab.py` absent before A1 | before: no reader exists; after: absent/unreadable/a key missing → `VocabError` naming the path and key; `collect_intake` prints the refusal and writes nothing; `critic_verdict_check` exits 2 with the ASCII line (§2.3) | an unknown vocabulary never validates a type or a disposition (FR-59) |
| E9 | TEMPORAL: rows when the columns land | row identity = node id + the cells of every column except `Тип`, `Откуда`, `Статус`, matched as a MULTISET against every batch file of the same pile at the base. Found → OLD (`—`/absent legal); not found → NEW (must carry valid `Тип` and `Откуда`). A table without the columns gaining a NEW row → red. An unreadable base → every row NEW + one WARN note | old history never turns red by a new rule; a new or rewritten row is never typeless |
| E10 | POSITIONAL: the `узел:` back-reference in `_item_why` and `check_leftovers` | after `_node_problem` and before the pass; `подтвердил:` presence after the back-reference | a closed or executor-less node is still refused |
| E11 | a leftover `узел:` naming a node of THIS batch | refused | a batch never closes by pointing at itself |
| E12 | `Откуда: остаток X` with X missing | red naming X; X in a closed batch is allowed | a born node names a real parent |
| E13 | the counter: rows moved across piles / deleted / status moved back | across piles: an open in the target, `ушло` in the source; deleted: `исчезло: N`; moved back: the later forward move counts once | the counter never shows a shrink that did not happen |
| E14 | a verdict with no `remarks`, an unknown disposition, a `чужой-код` with no path, an id named twice | `check_text` fails; at the gate (д) and at `status --verdict` → refused with the door `verdict: <node> none -- <why>` | a label always has its type and path |
| E15 | input from outside: the vocabulary file and `tools/rule_sources.json` a person edits; the verdict file; the `приток:` / `verdict:` / `owner-word:` / `подтвердил:` / `stamp-skip:` / `rule-census-raise:` text a person types | adversarial rows: empty list, duplicate word, a word with `\|`, a non-string, BOM, a 1000-word list, a missing key; a verdict 10 MB, nested 100 deep, not UTF-8, a remark path of 300 / 301 characters, `..`, a line break; a reason of 120 / 121 characters, with `\|`, a backtick, a line break, empty; a `verdict:` line inside a fence or a quote (not counted) → each a `VocabError`/`CannotRun` or a named refusal, never a silent accept | FR-1/FR-2 |
| E16 | the flow window git cannot read | NOT CHECKED note; not blocked by the flow rule; calibration counts the notes | an unknown never passes as `0` and is never silent |
| E17 | a topic critic (one verdict for several nodes, R13-g) | the same path in one `verdict: <node> <path>` line per node; each node judged against its own `Пишет в` | one verdict, one judgment per node |
| E18 | conflicting requirements: "fix now" vs PROJECT п. 3 (two batches «в работе» on one file) | F18 (a), decided: not a node — the fix waits as the same node's second round after the other batch merges, or is done now under D-0048 function lists / an `очередь:` line; the node stays open | two writers never meet in one file; an own-code remark never leaves its node |
| E19 | conflicting requirements: M2 vs the accepted architect-tier F8 (a) | fork F7 (Lead) with the named amendment of that spec | one road for "work below-Lead cannot do" |
| E20 | TEMPORAL: `перенос:` items written before the cutover | cutover = the FIRST commit whose `tools/piles-vocab.json` holds `carry_retired` (`git log --reverse --format=%H -S '"carry_retired"' -- tools/piles-vocab.json`, first line). `legacy_carries(root, rel)` = the multiset of «Остатки» items and proof-row cells at `<cutover>^`. At close: a `перенос:` item in that multiset by the OLD rule; any other `перенос:` refused; a legacy `узел:` item passes on `_node_problem` alone. No cutover commit → every item by the old rule. Git fails → `CannotRun`. A batch file absent at `<cutover>^` → no legacy items. Write time needs no cutover. `leftovers_unowned` keeps the old FORM | an item legal when written stays closable; a carry written after the rule never closes a batch |
| E21 | `Откуда: находка <file>` | checked when the row is NEW; a later delete/rename not re-judged | a new row names real evidence |
| E22 | `план:` path renamed later | checked when the header line is new or changed; `summary` prints `план не найден` | a new header names a real plan |
| E23 | `владелец <дд.мм>` without a year | refused | dates survive the year boundary |
| E24 | a near-miss separator in `Откуда` | red naming the expected ` · ` and the character found | the form is one form |
| E25 | the A1 → B window | B is built on A1's branch and merged right after A1; in between (д) refuses an intake row with the door "write the cells by hand" | a new row is never typeless |
| E26 | `intake_default` | `collect_intake` writes `Тип: неразобран` (F1 (a)) and `Откуда: находка <file>`; `summary` counts them | code never picks a work type |
| E27 | a red CI after M1 | no finding is born for it (§5.5); a red-CI finding written anyway is an orphan → red, door: delete it, the fix commit carries the record (F15) | one road for a red CI |
| E28 | `--owner-word` / `--no-verdict` on a non-`принято` or batch-level call | refused like `--hash` today | the passes exist only where the gate is |
| E29 | F5: a NEW `узел:` item without `подтвердил:`, with a placeholder, or a name that is neither `владелец` nor `Lead пачки` | refused; the names are data (`confirmers`); the gate checks presence and the word, never who typed it | a node leftover always carries its confirmation |
| E30-E36, E38-E45 | §8 edges | §8.2.5, §8.3 | — |
| E37 | R1 transition edges: a row already `принято` at the base (in any batch file of the pile); a row moved across piles while `принято`; a cell moved back to `ожидает` and forward again; a BATCH header set to `принято`; a node set to `отклонено`; one commit accepting 3 nodes with one short `verdict:` line; a commit with `--no-verify` | not judged; judged as new (over-require; door `verdict: <node> none -- moved from <slug>`); judged again (a new acceptance); not this rule (the batch's own `status` refusals hold it); not gated (dropping needs no verdict); red (ambiguous short line); forge-check judges the range with the range's messages | every acceptance of a node leaves a verdict record; the hand road and the tool road meet one gate (P31) |
| E46 | F-a: a verdict whose `verdict` is `blocker` | refused at the gate and at `status`; door `owner-word:` or `verdict: <node> none -- <why>` | a node is never accepted on a blocking verdict silently |
| E47 | R3: an untaken batch with 0 closes receiving rows; a migration commit; a worked batch | not judged (shown in `summary`); exempt; judged (§2.4 edge rows) | the prescribed intake road is never red; a worked batch that grows says why |

Refusal texts of the new reds (each: what is wrong, what is expected, a door the refused party can use):

| red | text |
|---|---|
| (д) table without the columns | `<path>: node row <id> is new, but the node table has no «Тип»/«Откуда» columns -- expected the header of plans/piles/_template/batch.md; add the two columns (old rows may carry «—»)` |
| (д) `Тип` | `<path>: node row <id>: «Тип» "<value>" is not a word of node_types in tools/piles-vocab.json (<the words>) -- write one of them; «неразобран» when the type is not yet judged` |
| (д) `Откуда` form | `<path>: node row <id>: «Откуда» "<value>" is none of: план, находка <file>, владелец <дд.мм.гггг>, миграция, остаток <node> · <key>[ · <carrier>] -- <the specific miss>` |
| (д) `находка` file | `<path>: node row <id>: «Откуда: находка <file>» names no file in plans/piles/<slug>/findings/ -- name an existing finding, or write the finding first` |
| (д) `остаток` parent / key / carrier | `<path>: node row <id>: «Откуда: остаток …» <the miss> -- PROJECT.md «Командная работа» п. 9 says when a remark may be a node` |
| (д) `план:` | `<path>: the header «план: <p>» names no file in the working tree -- write the plan first, or correct the path` |
| (д)/close `узел:` without `подтвердил:` | `<path>: «Остатки» line <n>: «узел: <id>» has no confirmation -- expected «подтвердил: <владелец \| Lead пачки>, <дд.мм.гггг>» (the owner's word 17.11.2026; the gate cannot know who typed it). Door: have the owner or the batch Lead confirm it, or fix the item now and write «сделано:»` |
| (д) acceptance (R1), blocker (F-a) | §2.3 part 2 |
| (д) flow (R3) | §2.4 |
| `status` / wave | §2.3 part 2 |
| close: new `перенос:` | `<path>: «Остатки» line <n>: «перенос:» is retired since <cutover7> (всё в кучках, 17.11.2026) -- an item written after it leaves the batch as «узел: <id>» whose row says «Откуда: остаток <a node of this batch> · <key>», or is finished with «сделано:». Door: open the node and write «узел: <id>», or finish the item; then run close again. Nothing was written` |
| close: `узел:` without back-reference | `<path>: «Остатки» line <n>: «узел: <id>» names a node whose «Откуда» is "<value>", not «остаток <a node of this batch> · <key>» -- write the back-reference in that row, or finish the item with «сделано:». Nothing was written` |
| close: git cannot tell old from new | `cannot tell a carry-over written before the cutover from a new one (git: <why>) -- run close inside the repository; nothing was written` |
| `critic_verdict_check` | §2.3 (ASCII) |
| §8 pointers / stamps / census | §8.2.5, §8.3 |

---

## 7. Phases, streams (ordered by volume), witnesses, readers

### 7.1 Phases

- **Phase 0 (Lead)**: the Lead forks (F3, F4, F6, F7, F9-F13, F15, F17, F20-F24, F26) and the ONE owner question left
  (F25, the `main` list; executable on the recommendation until her answer, PROJECT п. 11); critic re-pass on §8.2 (R5)
  only; the rest checked by the Lead against the t-943 list. The six OWNER forks of round 2 are decided (a).
- **Phase 1**: A1 (foundation; every other code stream imports `piles_vocab.node_vocab`). D's builder may start in
  parallel (disjoint files); D merges after A2 and A3 (its home text describes their gates): `очередь:` line A3 → D.
- **Phase 2, by volume of the leftover stream they stop**: C → A2 (critic, 34.5 %); D (owner's word 15.0 %, red CI and
  defects 13.1 %, scope cut 11.7 %, builder-noticed 6.8 %); A3 (the brake); B (readers); K (the class, L15) — K lands
  AFTER boot-by-topic S1, S2, S3-2 and after architect-tier D6 and L (§7.3), and after D.
- **Phase 3 (migration)**: E-k (M1 per pile group), G (M2, M4, M5, forge/7 as a container per F20, forge's own orphans),
  K2 (the census worked down, §8.5).
- **Phase 4 (close-out)**: H.

The nodes live in one big-idea batch of pile `forge` with `план:` this spec (§1.2) — the Lead opens it.

### 7.2 Streams (owns disjoint; `piles.py` shared by A1 → A2 → A3 → H strictly in sequence with disjoint function lists, D-0048; the carrier test shared by D → K in sequence)

| order | stream | node (file · function · behaviour) | owns (absolute) | witness (DoD command) | tier / commit |
|---|---|---|---|---|---|
| 1 | A1 | `tools/piles_vocab.py (node_vocab, VocabError)` NEW leaf (R2); `tools/piles.py (node_vocab re-export, NODE_COLS, _parse_nodes, _frozen_lines, +_new_node_rows, +_node_origin_problem, +_plan_problem, check_form)`: the two columns parsed; (в) masks `Тип`/`Откуда`; (д) new-row checks (E9, E21-E24); `tools/piles-vocab.json` created (no `carry_retired` yet); the template; the import-graph rows (§2.3) | `C:/QAFactory/forge-repo/tools/piles_vocab.py` `C:/QAFactory/forge-repo/tools/piles.py` `C:/QAFactory/forge-repo/tools/piles-vocab.json` `C:/QAFactory/forge-repo/tools/piles_testkit.py` `C:/QAFactory/forge-repo/tools/test_piles_form.py` `C:/QAFactory/forge-repo/tools/test_piles_frozen.py` `C:/QAFactory/forge-repo/plans/piles/_template/batch.md` | `python -m pytest tools/test_piles_form.py tools/test_piles_frozen.py -q` (outside the package: `scenario_walk.py --witness-for` has no row; the DoD names the test files, CLAUDE.md rule 4) | designer → builder → critic (topic critic A1-A3+C, R13-g); builder STAGES, Lead commits (mechanism path) |
| 2 | C | `tools/critic_verdict_check.py (validate_verdict, +_remark_errors)` (imports `piles_vocab`, never `piles`) and the schema: `remarks`, ASCII diagnostics, vocab-unreadable exit 2, old verdicts fail | `C:/QAFactory/forge-repo/tools/critic_verdict.schema.json` `C:/QAFactory/forge-repo/tools/critic_verdict_check.py` `C:/QAFactory/forge-repo/tools/test_critic_verdict_check.py` | `python -m pytest tools/test_critic_verdict_check.py -q` | builder → topic critic |
| 3 | A2 | `tools/piles.py (_item_why, _node_problem, check_leftovers, leftover_problem, proof_problems, check_proofs, LEFTOVER_FORMS, LEFTOVER_DOOR, LEFTOVER_WRITE_FORMS, HAND_EDIT, door_lines, +prose_lines, +legacy_carries, +_accept_reds, +_verdict_problem, +_origin_carrier_problem, +_confirm_problem, check_form, cmd_check, cmd_status, _status_evidence, _status_args)`: §2.3 parts 2-3 (R1, F-a), F5 (E29), E10, E11, E14, E17, E20, E28, E37, E46; `carry_retired` and `confirmers` keys; `tools/wave.py (record_node, by_hand, build_parser, run)`: the three arguments forwarded, the lines in the status commit message, step-0 refusal. Lead adds the four `MECHANISM_PREFIXES` entries (§4) in this commit | `C:/QAFactory/forge-repo/tools/piles.py` `C:/QAFactory/forge-repo/tools/piles-vocab.json` `C:/QAFactory/forge-repo/tools/wave.py` `C:/QAFactory/forge-repo/tools/test_piles_close_gate.py` `C:/QAFactory/forge-repo/tools/test_piles_close.py` `C:/QAFactory/forge-repo/tools/test_wave.py` | `python -m pytest tools/test_piles_close_gate.py tools/test_piles_close.py tools/test_wave.py -q` | builder → topic critic; Lead commits (mechanism paths) |
| 4 | D | rule texts 5.1-5.10, 5.12, 5.14 (the instance test); `CLAUDE.md` (5.7-5.9), `.claude/agents/critic.md` (5.11), `.claude/agents/designer.md`, `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` handed as text, placed by the Lead IN THE SAME COMMIT; the critic exam (PROCESS/CRITIC_EXAM.md) run by the Lead BEFORE that commit, its result line written (critic.md rule 10); AGENTS.md regenerated | `C:/QAFactory/forge-repo/PROJECT.md` `C:/QAFactory/forge-repo/plans/builder-rules.md` `C:/QAFactory/forge-repo/docs/tasks/critic-diff-brief.md` `C:/QAFactory/forge-repo/tools/tests/test_role_carriers_one_owner.py` `C:/QAFactory/forge-repo/AGENTS.md` (+ `C:/QAFactory/forge-repo/docs/TEAMWORK.md` § 9 only when it exists at landing, 5.3b) | `python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_handoff_rule_anchors.py -q` + `python tools/agents_md.py --check` | builder; Lead places the mechanism-path texts and runs the exam |
| 5 | A3 | `tools/piles.py (+flow, +_flow_reds, cmd_summary, _count_line, cmd_status, _close_batch)`: §2.4 (R3), E13, E16, E47; `приток:` through `prose_lines`; `tools/session_context.py (+flow_line call in the boot block)` | `C:/QAFactory/forge-repo/tools/piles.py` `C:/QAFactory/forge-repo/tools/session_context.py` `C:/QAFactory/forge-repo/tools/test_piles.py` `C:/QAFactory/forge-repo/tools/test_session_context.py` | `python -m pytest tools/test_piles.py tools/test_session_context.py -q` (states the measured `git log` time: F3) | builder → topic critic; Lead commits |
| 6 | B | `tools/backlog_tree.py`: statuses through `piles` (+`type`); `tools/collect_intake.py`: `Тип: неразобран`, `Откуда: находка <file>` (E25, E26), vocab through `piles_vocab` | `C:/QAFactory/forge-repo/tools/backlog_tree.py` `C:/QAFactory/forge-repo/tools/test_backlog_tree.py` `C:/QAFactory/forge-repo/tools/collect_intake.py` `C:/QAFactory/forge-repo/tools/test_collect_intake.py` | `python -m pytest tools/test_backlog_tree.py tools/test_collect_intake.py -q` | builder (on A1's branch, merged right after A1) → topic critic |
| 7 | K | §8: `tools/rule_pointers.py` (`resolve`, `section_bounds`, `section_hash`, `parse_markers`, `check`, `census`, `stamp`, CLI), `tools/rule_sources.json`, `tools/rule-stamps-baseline.json`, the axis-31 test reads its lists from `rule_sources.json`, scans every `rule:`/`правило:` line, gains the stamp/census rows; per F23 (a) it ABSORBS FG7-52 (boot-by-topic §4.3 contract incl. the TOC cells) | `C:/QAFactory/forge-repo/tools/rule_pointers.py` `C:/QAFactory/forge-repo/tools/rule_sources.json` `C:/QAFactory/forge-repo/tools/rule-stamps-baseline.json` `C:/QAFactory/forge-repo/tools/tests/test_role_carriers_one_owner.py` (+ the `.githooks/commit-msg` and `.github/workflows/forge-check.yml` lines handed as text — enforcement files, the Lead places them; `MECHANISM_PREFIXES` entries — Lead) | `python -m pytest tools/tests/test_role_carriers_one_owner.py -q` + `python -B tools/rule_pointers.py check --staged` (exit 0 on the tree) + `python -B tools/rule_pointers.py census` (prints the count written to the baseline) | designer → builder → critic (its own topic); Lead commits (mechanism: a gate) |
| 8 | E-k | M1 orphans, one pile group per node (`forge` and `package-ci` excluded — G owns them) | `C:/QAFactory/forge-repo/plans/piles/<slug>/` of the group's piles | `python -B tools/piles.py check --all` — the (е) line for the group's piles: 0 orphans; (д) green | scout → Lead (stale) → builder (rows) |
| 9 | G | M2 (per F7), M4, M5, forge/7 as a container (F20), forge's and package-ci's own orphans | `C:/QAFactory/forge-repo/docs/tasks/factory-fixes.md` `C:/QAFactory/forge-repo/docs/tasks/test-diet.md` `C:/QAFactory/forge-repo/docs/tasks/onboarding-streams-2026-11-12.md` the six plan files (P25) `C:/QAFactory/forge-repo/plans/piles/forge/` `C:/QAFactory/forge-repo/plans/piles/package-ci/` (+ `docs/tasks/lead-queue-fable.md` only under F7 (a)) | `python -B tools/piles.py check --all` + doc key-presence for the `архив:` lines (doc-dispatch witness: keys verbatim, full script source, one negative control) | builder; Lead judges stale; Lead runs take/status/close for forge/7 |
| 10 | K2 | the census worked down (§8.5): each counted block becomes a pointer, a stamped block or stays as role detail; the baseline lowered in the same commit; builder-rules' restatements of CLAUDE.md become pointers (F-d); every `critic.md` / `scout.md` commit owes its exam first (critic.md rule 10, scout.md :59) — the Lead runs it | the non-mechanism service files (`docs/tasks/*brief*.md`, `plans/builder-rules.md` restatements), `C:/QAFactory/forge-repo/tools/rule-stamps-baseline.json`; `.claude/agents/*`, `.claude/skills/*` handed as text (Lead places) | `python -B tools/rule_pointers.py check --staged` + `python -B tools/rule_pointers.py census` (lower than before) | builder; Lead places mechanism-path files and runs the exams |
| 11 | H | `tools/piles.py (check_findings, FINDINGS_FROM)`: (е) one rule after M1 = 0; Lead: `.claude/settings.json` stale allow lines (P23) | `C:/QAFactory/forge-repo/tools/piles.py` `C:/QAFactory/forge-repo/tools/test_piles_findings.py` | `python -m pytest tools/test_piles_findings.py -q` | builder; Lead |

Every new test case is a ROW (or a parametrised table) in the test file named in the stream's owns (docs/TESTING.md: no
new test file — K's rows go into the existing axis-31 test); E15's battery is one table per input kind in the file of the
stream that reads it.

### 7.3 Order lines with the parallel specs

| file | streams that touch it | order |
|---|---|---|
| `CLAUDE.md` | boot-by-topic (homes, S1 headings + TOC), architect-tier L, this D (5.7-5.9) | boot-by-topic → architect-tier → D; anchored by quoted old text; Lead places |
| `PROJECT.md` | boot-by-topic (moves 2c/2d/9a/9b, TOC), this D | boot-by-topic first (F12); D edits each fragment in its home |
| `docs/TEAMWORK.md` | boot-by-topic (creates), this D (5.3b in § 9 when it exists) | boot-by-topic → D |
| `.claude/agents/critic.md` | architect-tier (rule 9, L), this D (rules 5, 17, 19), K2 | architect-tier → D → K2; Lead places; exam before each commit |
| `.claude/settings.json` | architect-tier, this H | architect-tier → H; Lead |
| `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` | architect-tier F (check 49), this D (checks 33, 39) | architect-tier → D; Lead |
| `tools/mechanism_gate.py` | architect-tier A5 (`_tier_queue_note`), this A2 and K (`MECHANISM_PREFIXES`) | architect-tier → A2 → K; disjoint functions (D-0048) |
| `tools/session_context.py` | architect-tier C, this A3 | disjoint functions; `очередь:` line in both batch files |
| `tools/tests/test_role_carriers_one_owner.py` | boot-by-topic S1/S2 (POINTERS rows), this D, FG7-52, K | boot-by-topic → D → K; FG7-52 is absorbed by K (F23 (a)) or lands between D and K (F23 (b)) |
| `CLAUDE.md`, `PROJECT.md`, `plans/builder-rules.md` as K's MAIN files (their section bounds) | boot-by-topic S1 (CLAUDE.md headings), S2 (imports), S3-2 (`### <n>. <bold title>` in builder-rules) | S1, S2, S3-2 → K: K's stamps and baseline are written on the final structure (R6 (v)) |
| the service files' census | architect-tier D6 (deletes `.claude/skills/onboarding/`, `next-task/`) and L (rewrites role-file text) | D6, L → K: K's `census --write` runs after both are on `main` (F-g) |
| `.githooks/commit-msg`, `.github/workflows/forge-check.yml` | K (one line each), boot-by-topic / architect-tier if they add lines | Lead places, appended after `piles.py check`; no reorder |
| `.claude/agents/designer.md` | this D, K2 | D → K2 |

### 7.4 Readers of every touched file (designer rule 7)

Commands (Grep tool; the root checkout, worktrees not counted): `piles\.py|import piles|from piles` over `tools/`,
`.githooks/`, `.claude/settings.json`, `.github/` → 42 files (round 1); `.githooks/` for
`piles\.py|wave\.py|session_context|critic_verdict_check|test_role_carriers_one_owner` → 1 hit (`commit-msg:40`);
`commit-msg` glob `*.py` over `tools/` → 14 files (P47, r3); `piles_vocab|rule_pointers|rule_stamps` over `tools/` and
`.githooks/` → 0 (new names, P48, positive control in P48); `wave\.py|import wave|from wave` over `tools/` → 4 files;
`session_context` over `tools/` → 36 files; `test_role_carriers_one_owner` over `tools/` → 1 (itself);
`critic_verdict` over `tools/` → 9 files, over `.claude/` → `settings.json:163`, `agents/critic.md:141, 150`;
`factory-rules-debt` → 54 files (not touched); `lead-queue-fable` → 4 files; `backlog_tree` → 17; `collect_intake` over
`tools/` → 3; `critic-diff-brief|builder-rules` over `tools/*.{py,json}` → the anchors of P22 + `test_quarantine.py:51`,
`test_dispatch_manifest.py:844`.

| touched file | other readers | verdict |
|---|---|---|
| `tools/piles.py` | the 42 of §4 | signatures of `load_tree`/`parse_*`/`leftovers_unowned`/`printable`/`write_bytes_atomic`/`LEFTOVER_EMPTY_WORDS`/`door_lines`/`range_messages` unchanged; `node_vocab` re-exported; `wave.py`: A2; `backlog_tree.py`, `collect_intake.py`: B; `session_context.py`: A3; `rule_pointers.py`: K (lazy import); `.githooks/commit-msg`, `forge-check.yml`: unchanged command, new reds inside (д) |
| `tools/piles_vocab.py` (new) | after A1: `piles.py`, `collect_intake.py` (B), `critic_verdict_check.py` (C); `mechanism_gate.py` list (A2) | created in A1 |
| `tools/piles-vocab.json` (new) | `piles_vocab.node_vocab` only; `mechanism_gate.py` list (A2) | created in A1, `carry_retired`/`confirmers` in A2 |
| `tools/wave.py` | `test_wave.py`, `mechanism_gate.py`, `test_mechanism_gate.py` | `test_wave.py` changes in A2 |
| `tools/session_context.py` | 36 files (hook config `settings.json:10`, its test files, `hook_liveness_probe.py`, `wiring_check.py`, gates, `install_parity_anchors.json`, `dup-baseline.json`, `skills/boot-diet/SKILL.md`) | one ADDITIVE output line; A3's DoD lists any line-count pin that moves (NOT verified line by line); architect-tier C: §7.3 |
| `tools/critic_verdict_check.py`, schema | `.claude/agents/critic.md:141, 150` (rule 17 changes in D), `test_critic_verdict_check.py` (C), `install_parity_anchors.json`, `dup-baseline.json`, `md_regions.py`, `escape_check.py`, `test_p4_stdin_deadline.py`, `test_handoff_rule_anchors.py:94, 107`; after A2 `piles.py` (`check_text`) and `mechanism_gate.py` (list) | new REQUIRED field; critic.md rule 17 says so in the same wave; imports `piles_vocab` |
| `docs/tasks/critic-diff-brief.md` | anchors P22, critic.md, CLAUDE.md rule 3, the carrier test | anchors and K-OWN keys byte-identical; D, then K2 |
| `PROJECT.md` | CLAUDE.md import; AGENTS.md; the carrier test; boot-by-topic; K (MAIN) | AGENTS.md regenerated in D; K reads, never writes it |
| `plans/builder-rules.md` | anchors P22 (7b), `test_quarantine.py:51`, `test_dispatch_manifest.py:844`, the carrier test, K (MAIN and scanned carrier) | п. 1 only in D; restatements → pointers in K2 |
| `CLAUDE.md` (4a, 9, 12 clauses) | AGENTS.md, `install_parity_anchors.json`, the carrier test, K (MAIN) | Lead places in D's commit |
| `.claude/agents/critic.md`, `designer.md` | the carrier test, `install_parity_anchors.json`, K (service) | Lead places in D's commit; K2 later |
| `tools/tests/test_role_carriers_one_owner.py` | none (only itself) | D, then K |
| `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` | `mechanism_gate.py`, calibration sessions; K (MAIN under F25 (a)) | Lead, D's commit |
| `plans/piles/_template/batch.md` | `test_pile_cards_contents.py`, `piles.py` `batch_heading_problems`; after K the axis-31 scan | headings kept |
| `docs/tasks/lead-queue-fable.md` | P16 | per F7 |
| `.claude/settings.json` (allow lines) | `hook_liveness_probe.py`, `test_workflows.py` (they parse hooks, not allow lines — the Lead verifies) | H, Lead |
| `.githooks/commit-msg` (K's line) | the 14 of P47 — those that PARSE hook lines: `hook_liveness_probe.py` (+ test), `wiring_check.py` (+ test), `test_enforcement_probe.py`, `mechanism_gate.py` (path list), `agents_md.py`; the rest name it in text | K's builder hands the line; the Lead places it after `piles.py check` and runs the probe's and `wiring_check`'s narrow rows; a new probe for the line moves the count pins (482/1015 per round 2) — K's DoD names whether it does (NOT verified here) |
| `.github/workflows/forge-check.yml` (K's line) | `test_workflows.py`, `wiring_check.py` | Lead places; their narrow rows run |
| `tools/rule_pointers.py`, `rule_sources.json`, baseline (new) | the axis-31 test; `.githooks/commit-msg`; forge-check; `mechanism_gate.py` list (K's commit) | created in K |
| `ai-packages/qa-factory/design/factory-rules-debt.md` | P18 | NOT touched by this spec |

### 7.5 Producers (designer rule 6)

| produced | producer (owning node) |
|---|---|
| `Тип`/`Откуда` cells of new rows | the row's writer, `collect_intake` (B) |
| `remarks` in a verdict | the critic (role); its shape checked by C |
| the `verdict:` / `owner-word:` commit lines | `piles.py status` prints them, `wave.py merge` writes them (A2); a hand committer types them; (д) reads them (A2) |
| the committed verdict file | the Lead commits the critic's report no later than the accepting commit (F24 (a)) |
| `подтвердил:` on a `узел:` item | the owner or the batch's Lead; A2 checks presence |
| `приток:` commit lines | the committer (A3 reads them) |
| `carry_retired`, `confirmers` keys | A2 |
| the flow line at SessionStart | A3 |
| the red-CI record | F15 (a): the fixing commit's message; `defect_found` by the coordinator |
| node rows from M1-M5 | E-k, G |
| `rule_sources.json`, the census baseline, the stamps | K (tool and data), K2 and every later editor (`rule_pointers.py stamp` writes the hashes) |
| `stamp-skip:` / `rule-census-raise:` lines | the committer; `rule_pointers.py check --msg-file` reads them (K) |

### 7.6 Architecture (forge analogs) and the four questions

No package file changes → `architecture: none -- forge tools and rule texts only` would be the line for a package commit;
none is planned. Forge analogs kept: AR-1 (main files and the scan set are data), AR-13 (one reader: statuses through
`piles`; the vocabulary through `piles_vocab`; the verdict shape through `critic_verdict_check.check_text`; commit-message
lines through `piles.prose_lines`; pointers and sections through `rule_pointers.resolve`), AR-14 (one writer: node rows by
the pile road; stamps by `rule_pointers.py stamp`), AR-15 (one survivor: one acceptance gate (д); one pointer form and
resolver — §8.2), AR-20 (the census ratchet only shrinks), AR-29 (the §4 class table), AR-28 (no unknown becomes a pass:
E16, E20, E8, E37, §8.3).

Four questions (CLAUDE.md rule 10) for the commits of A1/A2/A3/C/D/K: the committer writes the full axis enumeration.
Likely axes: 1 (the pointer set), 4 (debt ↔ backlog ↔ nodes), 18 (the census ratchet), 31 (one owner per aspect — the
carrier test and K), 34 (one road: one table, one leftover form, one acceptance gate, one pointer form). Detectors:
§5.12 items (i)-(v) in check 33; check 39. What stops skipping: the commit-msg (д) acceptance/flow gates, `close`,
`critic_verdict_check` self-run, `rule_pointers.py check --msg-file` in commit-msg and `--base` in forge-check, the
carrier test in CI (forge-check `:96`).

---

## 8. The class (W3): service files never contradict the main files, even when the main files change every day

The owner's word (17.11.2026, W3): «это починит только одно место. А надо что бы все служебные файлы не противоречили
основным даже если мы будем основные каждый день менять.» §5 is the first instance; this section is the mechanism for
the whole class: stream K (+ K2 for the existing files).

### 8.1 Main files are DATA (AR-1)

`tools/rule_sources.json` (new, K):
```json
{"main": ["CLAUDE.md", "PROJECT.md", "docs/TESTING.md", "plans/builder-rules.md", "docs/TEAMWORK.md",
          "ai-packages/qa-factory/design/factory-rules.md", "ai-packages/qa-factory/design/architecture.md",
          "docs/SIBLING_MAP.md", "PROCESS/*.md"],
 "scan_extra": ["plans/piles/_template/"],
 "owner_keys": [...], "pointers": [...]}
```
- `main` — the files whose text IS the rule. Which files are «основные» is the meaning of the owner's sentence (11a):
  ONE owner question, F25, with the recommendation above (boot files + TESTING + TEAMWORK + the factory's rules and
  architecture + SIBLING_MAP + PROCESS); executable on it until she answers. `docs/TEAMWORK.md` is listed only once it
  exists (K's builder checks at K's merge; else the boot-by-topic commit adds the row).
- **service = the axis-31 scan set minus `main`** (one definition, R5): every tracked text file the carrier test scans
  (P33) — role files, skills, briefs, RUNBOOK, CURRENT_CONTEXT, `tools/*.py` refusal and dispatch texts — plus
  `scan_extra` (the template, which `plans/piles/` EXCLUDED hides today; this WIDENS the scan, never shrinks it); K-OWN's
  scope unchanged. No separate service globs exist.
- A main file is still scanned as a CARRIER (its pointers and stamps are checked) but never census-counted; a main
  file restating another main file is turned into a pointer in K2 (F-d: `plans/builder-rules.md` is main for its own
  rules; its restatements of CLAUDE.md — 7b vs rule 4, п. 1 vs rule 11 — become `правило:` pointers).
- `owner_keys` / `pointers` = today's hand lists of the axis-31 test moved into data (§8.2.3).
- Empty outcome: `main` empty → `CannotRun` naming the key; a `main` entry or glob matching no file → `CannotRun` for a
  literal path, one WARN line for a glob (E34).

### 8.2 One pointer form, one resolver (R5 — SELF-CONTAINED: the critic re-pass reads this subsection alone)

**8.2.0 The collision.** Three pointer forms would coexist: (1) the axis-31 test's K-PTR rows — a prose pointer phrase in
the carrier and a SUBSTRING anchor in the target (`squash(anchor) in squash(target)`, P33); (2) boot-by-topic's
`rule: <file> § <x>` / `правило: <файл> § <x>` with the §4.3 resolver contract, checked by node FG7-52, which "extends
`tools/tests/test_role_carriers_one_owner.py`, no `pointer_lint.py`" (P44); (3) round 2's `see: <file>#<anchor>` with a
line-prefix anchor in a new `rule_stamps.py`. Three resolution rules on the same pointer (P31, AR-15).

**8.2.1 The survivor.**
- **ONE FORM** = boot-by-topic's (F22 (a), recommended): `rule: <file> § <x>` in English files, `правило: <файл> § <x>`
  in Russian files — accepted earlier, already the form of boot-by-topic's TOCs and moved-block pointers. A stamp uses the
  SAME address: `<!-- source: <file> § <x> @ <src12>/<blk12> -->` … `<!-- /source -->` (in a `.py` file: the comment
  lines `# source: <file> § <x> @ <src12>/<blk12>` … `# /source`; other suffixes carry pointers only). `see:` is retired
  before birth: §5 and §8 use no `see:`.
- **ONE RESOLVER** = `rule_pointers.resolve(text, x) -> Section | Miss` in the stdlib leaf `tools/rule_pointers.py` (it
  imports `gitcmd` and, lazily in its CLI only, `piles` for `prose_lines`/`range_messages`). It implements boot-by-topic
  §4.3 items 1-4 (that contract is kept whole) plus the bold lead-in kind and the uniqueness rule of 8.2.2. Its callers:
  the axis-31 test (every `rule:`/`правило:` line in the scan set, every TOC cell — FG7-52's contract — and every
  remaining hand POINTERS row), `rule_pointers.py check` (commit-msg, forge-check), `rule_pointers.py stamp` and
  `census`. Nothing else resolves a pointer.
- **ONE CHECKER per check kind**: pointer resolution (no door: E31/E32 are always red) is judged by the axis-31 test in
  CI AND by `check` at commit time — the same `resolve`, two triggers; stamps and the census (they have doors, which live
  in commit messages) are judged only by `check` (commit-msg `--msg-file`, forge-check `--base` with the range's messages
  — 8.3). The test judges stamps and census on FIXTURES only (rows), never on the real tree (it has no message to read
  a door from).
- **Who builds it** (F23, Lead): (a) K ABSORBS FG7-52 (recommended): one node builds the resolver once with every kind;
  FG7-52's forge/7 row becomes `отклонено: поглощён узлом K спеки 20261117-everything-in-piles` (its row is stale anyway:
  it still names `tools/pointer_lint.py` and pre-commit, P45, against boot-by-topic A1); amendment line for the
  boot-by-topic spec (the Lead writes it there, not this spec): "FG7-52 is built inside K (everything-in-piles §8.2);
  the resolver lives in `tools/rule_pointers.py`, called by the axis-31 test — still no second checker". (b) FG7-52 → K:
  FG7-52 builds `resolve` in `tools/rule_pointers.py` (the same amendment of its row and of A1's wording), K adds stamps
  and census on top.

**8.2.2 The address grammar and section bounds (R6).** `<x>` is one of four kinds; lines inside code fences are never
anchors and never ends; matching strips leading whitespace and squashes inner whitespace; indentation is kept for the
end rule.
| kind | `<x>` written as | a line is the anchor when | the section ends before the first later line that is |
|---|---|---|---|
| heading | the heading text (to end of line) | it is a `#`-heading whose text equals `<x>` | a heading of the same or a higher level |
| item | an id `\d+[a-z]?` or `P\d+`/`FR-\d+`/`AR-\d+` | it opens with `<x>.` (or `### <x>`, `**<x>.**`, `- **<x>.**`, as §4.3) | an item opener (`\d+[a-z]?\.`, `- `) at the same or lesser indentation, or a heading; so `11a.` at column 0 is a SIBLING of `11.` and ends it, while `   4a.` (indented inside rule 4) belongs to rule 4's section and its own section ends at the next opener at indentation ≤ 3 |
| bold | `**<text>**` | after leading whitespace (and after an optional item opener) the line starts with `**<text>**` | with an opener: as an item. Without (a LEAD-IN): a line-start bold at the same or lesser indentation whose previous non-blank line ends with `.` `:` `;` `!` `?` `»` `)` (a wrapped line that merely starts with bold, PROJECT.md:96, does not end it), or an item opener at the same or lesser indentation, or a heading |
| literal | `"<prefix>"` (quoted) | after leading whitespace the line starts with `<prefix>` | — : pointers only; a stamp on a literal is refused (no section end) |
Every kind must hit EXACTLY ONE line: 0 → E31, 2+ → E32 (§4.3 had no uniqueness rule — this is the one addition besides
the bold and literal kinds; it errs safe). A numbered pointer line («N. **<title>** — правило: … § N») keeps §4.3 item 2
(its title equals the item's bold opener). `section_hash` = sha256 over the section's lines with CRLF → LF and trailing
spaces stripped.

**The first real instance** (P43): after 5.3 the home is the line `   **Остатков нет по правилу** (слово владельца
17.11.2026, по происхождению):` (3 spaces); pointer `rule: PROJECT.md § **Остатков нет по правилу**` → bold kind, a
lead-in (no opener); its section runs to the line before `   **Живые прогоны не держат пачку вообще**` (same indentation,
the previous line ends with `.`) — or to `10.` / a heading, whichever first. Edges (rows in the axis-31 test, each on a
COPY of PROJECT.md):
- AT: the anchor at a line start after 3 spaces → resolves; after 0 spaces → resolves; the section's last line is the
  home's last sentence (5.3b's last line or the TEAMWORK pointer line).
- BEYOND (i): the phrase only MID-line — today's `PROJECT.md:333` → E31, and the refusal adds the hint `found mid-line at
  PROJECT.md:333 -- a bold anchor must start its line`; this is why 5.3 puts the home on its own line.
- BEYOND (ii): a second line starting with the phrase → E32 naming both lines.
- BEYOND (iii): the phrase only inside a fence → E31.
- BEYOND (iv): a line-start bold at indentation 4 (deeper) inside the home → does not end it; at indentation 3 after a
  line ending in `.` → ends it (the D text rule "no wrapped line of the home begins with `**`" keeps this from biting).
- In the window D → K the substring K-PTR row and the grammar agree on this pointer (the home at a line start, unique).

**8.2.3 What the other two become.**
- **K-PTR (the 20 hand POINTERS rows + D's 5)**: rows move into `rule_sources.json` `pointers` and their ANCHOR is
  resolved by `resolve` (a row's anchor is rewritten as a `<x>` of 8.2.2: `## The two layers` → `The two layers`
  (heading); `RULES_7B` → `7b` (item); `6. **DUPLICATION…**` → `6` scoped by uniqueness in the brief, else the bold kind;
  COST → `"Cost gates (D-0035"` (literal); `HYGIENE_6` → `"6. An environment-negative claim"` (literal: `6.` occurs twice
  in CLAUDE.md); `scout:` in the yaml → `"scout:"` (literal)). A row disappears when K2 writes the matching `rule:` line
  into its carrier (the scan finds it then). The substring rule is retired. Text presence pins of P22
  (`install_parity_anchors.json`, `test_handoff_rule_anchors.py`) are not pointer checks and stay.
- **`see:` and `rule_stamps.py`** (round 2): never built. Stamps, census and the CLI live in `tools/rule_pointers.py`;
  there is no `section_bounds` outside it.
- **boot-by-topic §4.3 / FG7-52**: the contract is kept whole and implemented by `resolve` (F23).

**8.2.4 The scan set.** One set for K-OWN, pointers, stamps and census: the axis-31 test's (tracked text files minus
EXCLUDED, P33) + `scan_extra`. The census counts `.md` files only (its unit is a markdown block, §8.4); `.py`/`.json`/
`.yaml` files are scanned for pointers and stamps.

**8.2.5 Edges of the form** (F-j): a pointer may target ANY tracked file that exists (main or not) — it only has to
resolve; a STAMP's source must be a `main` file (a stamp carries a main rule), a stamp from a non-main or generated file
(e.g. `docs/FACTORY_RULES_INDEX.md`) → red `stamp source <f> is not a main file -- point at it, or stamp from its main
section`; a `source:` without its `/source` → red `unclosed stamp`; two stamps nested or overlapping → red; a marker
inside a code fence → not a marker (documentation text); a file in `main` is never in service (by definition), it is
scanned as a carrier only; partial staging — commit-msg judges the INDEX blobs (`git show :<path>`) of both main and
service files, never the working tree; a section that itself contains a generated block → normal (the hash covers it;
regenerating it reds the stamps on it — the safe direction).

### 8.3 The check on the commit path and in forge-check (R4: the doors are read where the check runs)

`python -B tools/rule_pointers.py check --msg-file "$1"` — in `.githooks/commit-msg`, after `piles.py check` (the hook
that has the message, P41; the Lead places the line); it reads the index. `python -B tools/rule_pointers.py check --base
"$BASE"` — in `.github/workflows/forge-check.yml` beside `piles.py check --base` (`:84`), reading the range's messages
through `piles.range_messages`, so a door used locally is honoured in CI. NOT in pre-commit (a pre-commit hook gets no
message; round 2's placement is withdrawn). It reads `rule_sources.json`, finds every pointer and `source:` marker in the
scan set, and:

| case | behaviour | text (what / expected / door) | invariant |
|---|---|---|---|
| E30 stamp `src12` ≠ the source section's current hash | red | `<file>:<line>: the block stamped from <main> § <x> @ <old12> is stale: that section now hashes <new12> (changed in <the last commit touching it>) -- re-read the block against the section and fix its meaning, then re-stamp it: python -B tools/rule_pointers.py stamp <file>:<line>; both in this commit. If you may not edit <file> (outside your owns), hand it on: add the line "stamp-skip: <file>:<line> -- handed to Lead" to the commit message` | a carried block never silently outlives a changed rule; code judges the hash, the re-stamper the meaning (AR-29) |
| E31 address resolves to 0 lines | red, for a pointer and a stamp alike | `<file>:<line>: <main> § <x> points nowhere: <the kind's miss; for a bold or literal found only mid-line: "found mid-line at <main>:<n> -- a <kind> anchor must start its line">; nearest heading: <h> -- point it at the new place (and re-stamp a carried block), or remove it if the rule is gone` | a pointer always lands on a real rule (safe) |
| E32 address resolves to 2+ lines | red | `<file>:<line>: <main> § <x> is ambiguous: lines <a>, <b> -- use the bold title (§ **<title>**) or a longer literal` | one address, one section |
| E33 a main file edited daily (P46: 11/10 commits a week, 1-4 sections each) | only the stamps whose SECTION hash moved go red; pointers never go red on content edits, only on E31/E32; cost = one `stamp` call + the read per affected carried block — measured bound: ~17 stamps for a commit like `7b3f1d80` IF every reference were a carried block, 0 with pointers (t-943, estimate, not measured on stamps) → K2's target is pointers by default (§8.5) | — | the price of change is per affected block, never per file |
| E34 a literal `main` path that does not exist / a glob matching nothing | `CannotRun` / one WARN line | `rule_sources.json: main file <p> does not exist -- fix the list` | the list never points into the void silently |
| E35 the commit edits a stamped block's text but not the stamp | red: `blk12` ≠ the block's hash | as E30, "the carried text changed since its stamp" | the stamp records that someone re-read the block |
| E36 git cannot read the base / the index | `--base` unreadable → exit 2 in CI (full history; a broken run); the index unreadable in commit-msg → NOT CHECKED note, exit 0 | `rule_pointers: the base <rev> cannot be read (<why>)` | an unknown is named; CI never passes on it |
| E38 a stamp-skip line names a stamp that is not stale | note `stamp-skip for <file>:<line> not needed`, not red | — | a door never hides a later staleness (it binds this commit only) |
| E39 re-stamp where `src12` moved and `blk12` did not (F-c) | not red; printed as `re-stamped without a text change: <file>:<line>`; calibration item (v) counts them | — | the cheap road (re-stamp without reading) is visible |

The informed passes (FR-4), both COMMIT-MESSAGE lines read by `piles.prose_lines`: `stamp-skip: <file>:<line> -- <why>`
(binds this commit only; the usual case is the refused party who may not touch the service file — the Lead re-stamps
next) and `rule-census-raise: <file> +<n> -- <why>` (§8.4). Calibration counts both (§8.6).

### 8.4 The census and its ratchet

Unit (fork **F21**, Lead; recommended (a)): (a) a BLOCK of a scanned `.md` service file — a paragraph or a list item,
fences and headings excluded — that carries no pointer and does not sit inside a stamped block; counted per file. Pure
shape (FR-12). **Anti-laundering (F-b):** a block counts as POINTED only when, besides its pointer, its prose is at most
30 words (whitespace-split); a block of 31+ words with a pointer is counted (AT 30 / BEYOND 31 rows) — adding a `rule:`
line to a paragraph that restates the rule does not take it out of the count. (b) A verbatim span ≥ 12 words shared with a
main file — narrower. (c) Both.
- `python -B tools/rule_pointers.py census` prints `rule census: <total> unmarked blocks in <k> files` and one line per
  file; `--write` writes `tools/rule-stamps-baseline.json` (`{"<file>": <count>}`).
- Ratchet (shrink-only, AR-20, axis 18): `check` is red when a file's count rises above its row — text: `<file>: <now>
  unmarked blocks, baseline <base> -- point new rule text at its main section (rule: <main> § <x>) or stamp it; role
  detail that belongs to this file only: add the line "rule-census-raise: <file> +<n> -- <why>" to the commit message and
  raise the baseline row in the same commit`; a lower count without lowering the row → one note.
- Rows for files that come and go (F-g): a NEW `.md` file in the scan set with no row → judged against baseline 0: a count
  > 0 needs the `rule-census-raise:` line and the row added in the same commit (F26 (a)); a DELETED or renamed file → its
  row is dropped by the same commit, never red; a row whose file is gone → note `drop the baseline row <file>`. The
  one-off briefs (`pre-release-0.9-*`, `test-diet-*`): kept as counted files — a file nobody edits never rises, so they
  cost nothing and need no archive decision (small choice, closed).
- When the baseline is written: K's `census --write` runs AFTER architect-tier D6 (deletes `onboarding/`, `next-task/`)
  and L (role-file rewrite) are on `main` — K's DoD shows those commits in `git log` first (F-g; else orphan rows and
  others' commits moving the ratchet).
- Today's count: NOT MEASURED (the unit is defined here; t-943's approximation, 353 blocks over the 18 round-2 files, is not
  the unit). The command that measures it is K's first act: `python -B tools/rule_pointers.py census --write`; its total
  becomes premise P49 at K's acceptance, with the command as its carrier.

### 8.5 Order of work

- K (one node): `rule_sources.json`, `rule_pointers.py`, the baseline at today's count (nothing goes red on day one), the
  carrier test reads `owner_keys`/`pointers` from the data file and gains rows: the 8.2.2 grammar and its R6 instance
  edges, E30-E39 on fixtures, E15's battery for `rule_sources.json`, `stamp` writes nothing on an unresolvable address, a
  negative control per red (a stamp corrupted on a COPY → named). K lands after boot-by-topic S1/S2/S3-2, architect-tier
  D6/L and D (§7.3).
- K2 (F-e): the TARGET is pointers by default — a counted block becomes a `rule:`/`правило:` pointer; a STAMP only where
  the reader cannot load the main file (a dispatch template printed by `tools/dispatch_new.py`, a hook refusal text);
  otherwise role detail stays and is counted. Order: the leftover-rule carriers first (the instance the owner saw), then
  biggest first by K's census; one file per commit; the baseline row lowered in the same commit; `critic.md` / `scout.md`
  commits owe their exams first (the Lead runs them).

### 8.6 Error direction, owners, detector

- The hash check errs SAFE: any byte change inside a source section reds every stamp on it (false red on a typo fix;
  door: re-read, re-stamp). The carried block's own hash (`blk12`) catches an edit of the block alone (E35).
- The bold lead-in end errs toward a SHORTER section when a wrapped line starts with bold after a sentence end — a false
  pass on the cut-off tail; mitigations: the previous-line rule (8.2.2), `stamp` prints the resolved first and last line
  so the stamper sees the range, and the K row on the real home asserts its last line.
- Pointers err SAFE (E31/E32 only); they cannot see a contradiction in prose next to them — the census and calibration.
- Remaining roads (K1 of t-943), named: (a) an EXISTING unmarked block edited in place into a contradiction — the census
  counts blocks, not content, and the baseline grandfathers today's text: caught only by calibration item (v)'s sample
  read and K2's work-down; (c) re-stamp without reading — E39 makes it visible; (b) `rule:` laundering — closed by the
  30-word rule (8.4); (d)/(f) main homes outside the list — F25; (e) files outside the globs — closed by the one scan set
  (8.2.4).
- Owners (AR-29): the hash, the resolution, the count — data (code); "does the carried block still mean the main rule" —
  judgment of the re-stamper (a role), accepted by the Lead at the diff gate; which files are main — intent (the owner,
  F25).
- Detector (rule 10 (c)): calibration check 33 item (v): the window's `stamp-skip:` and `rule-census-raise:` lines, the E39
  re-stamps without a text change, the census trend (falling while K2 runs), and a sample read of five unmarked blocks
  against the main files. What stops skipping (rule 10 (d)): `rule_pointers.py check` in commit-msg and forge-check; the
  axis-31 test in CI; `--no-verify` is caught by forge-check's `--base` run.

---

## F. Forks (options, consequences, recommendation; OWNER = only the owner decides)

Decided: **F1 (a)**, **F8 (a)**, **F14 (a)**, **F16 (a)**, **F18 (a)**, **F19 (a)** — the owner, 17.11.2026 («всё по
рекомендациям»); **F2 (a)** — her word on leftovers; **F5** — "the owner or the batch Lead" (W2); **B1-B5 directions** —
the Lead's, «ок» by the owner (W1). The paragraphs of decided forks below are the record.

- **F1 (OWNER, DECIDED (a)) — the `Тип` words.** (a) the five + `живой-прогон` + `решение` + `неразобран`; (b) the five +
  `неразобран`; (c) the five only. Executed in §1.1, E26.
- **F3 (Lead) — the counter's data source.** (a) git history (recommended; A3 measures the `git log` time); (b) an `Открыт`
  column.
- **F4 (Lead) — `перенос:` retired as a NEW form.** (a) yes (recommended, P31), legacy items close by the old form (E20);
  (b) keep it for live proofs — two forms.
- **F6 (Lead) — a growing batch.** (a) the add-time refusal without `приток:` for WORKED batches (recommended, R3 scope);
  (b) print only.
- **F7 (Lead) — the Lead queue vs the ACCEPTED architect-tier F8 (a).** (a) retire the file; "below-Lead cannot" and
  Architect items are nodes with `Исполнитель: Lead` / `Architect` (recommended, one registry). (b) the two queue files
  outside piles — contradicts «всё в кучках»; (c) the files as VIEWS of node ids. Consequence of (a) (F-h): architect
  streams C (`session_context.py` architect-queue count), A5 (`mechanism_gate._tier_queue_note`) and F (check 49 (b)) are
  being built NOW to read the queue files; recommended with (a): the Lead AMENDS `docs/tasks/specs/20261116-architect-tier-spec.md`
  now so C/A5/F read through `piles` (nodes with `Исполнитель: Lead`/`Architect`) from the start — named here, written
  there by the Lead; without the amendment the three readers are built twice (rework stated: C, A5, F rewritten by G).
- **F8 (OWNER, DECIDED (a)) — the debt file once empty.** (a) deleted by the debt-fix spec's last commit with its readers;
  a future violation is a node `Тип: долг` (§5.6); (b) kept empty. Executed in §3 M3, §5.6.
- **F9 (Lead) — taken batches.** (a) not migrated (recommended); (b) migrated.
- **F10 (Lead) — done orphan findings.** (a) M1 deletes them (recommended); (b) delete at `close`.
- **F11 (Lead) — a big idea's home.** (a) a batch in the topical pile (recommended); (b) a pile per idea.
- **F12 (Lead) — order with boot-by-topic, and its gate criterion.** (a) boot-by-topic lands first; D edits each fragment
  in its home; the owner's criterion («what code holds may leave», her «да» 17.11.2026) is applied CLAUSE BY CLAUSE
  (recommended, F-i): the origin rules (judgment and discipline — on-topic word, scope cut, red CI, own vs other code)
  stay the home in PROJECT.md (5.3a); the gate-held clauses (the verdict line, «чужой-код» inside «Пишет в», the
  `узел: | подтвердил:` form, `приток:`) go with 9a to TEAMWORK § 9 (5.3b) — no exception to her rule, so no owner
  question. (b) keep the whole home in PROJECT.md — an exception to her criterion, which only she can grant.
- **F13 (Lead) — which added rows the flow brake counts (within judged batches).** (a) every added row except
  `миграция` (recommended); (b) also exempt `находка` rows whose finding is added in the same commit.
- **F14 (OWNER, DECIDED (a)) — a builder-noticed analog.** (a) the same as critic remarks; (b) always a node. Executed in
  §2.2 row 7, 5.3a, 5.12.
- **F15 (Lead) — the record of a red CI.** (a) no finding: the fixing commit names the red run and, when an accepted node
  caused it, a `defect_found` line (recommended); (b) a finding exempt from (е) — two roads.
- **F16 (OWNER, DECIDED (a)) — a defect after acceptance that is not a red CI.** (a) the same as a red CI: new task_id +
  `defect_found`, no node; (b) a node `Тип: баг`. Executed in §1.3, §2.2 row 4b, 5.3a, 5.5.
- **F17 (Lead) — the B1 code point.** (a) the commit gate (д), with `status`/`wave` writing its line (recommended, after
  R1); (b) the `dod_gate.py` stop check; (c) discipline only.
- **F18 (OWNER, DECIDED (a)) — «занятый файл».** (a) not a reason (PROJECT п. 3 roads); (b) a reason. Executed in §2.2,
  5.3a, E18.
- **F19 (OWNER, DECIDED (a)) — «ждёт события».** (a) not a reason; (b) a reason. Executed in §2.2, 5.3a.
- **F20 (Lead) — forge/7 and untaken incoming batches.** (a) close forge/7 as a container after moving its open rows
  (recommended); (b) also forbid `status --set принято` on a node of an untaken batch.
- **F21 (Lead) — the census unit.** (a) unmarked blocks with the 30-word rule (recommended); (b) verbatim copies only;
  (c) both.
- **F22 (Lead) — the one pointer form (R5).** (a) boot-by-topic's `rule:`/`правило: <file> § <x>`, extended by the bold
  and literal kinds and the uniqueness rule (recommended: accepted earlier, already written into the TOCs; amendment
  line for boot-by-topic §4.3 named in 8.2.1); (b) amend boot-by-topic to `see: <file>#<anchor>` — rewrites accepted
  text, no gain.
- **F23 (Lead) — K and FG7-52.** (a) K absorbs FG7-52 (recommended: the resolver is built once); (b) FG7-52 → K with the
  resolver in `tools/rule_pointers.py`. Either way the boot-by-topic spec and the forge/7 row are amended (8.2.1).
- **F24 (Lead) — where the gate reads a verdict file.** (a) the committed tree only (recommended: CI can judge it, the
  record is in git, no machine path, AR-4 analog; cost: the Lead commits the critic's report before or with the accepting
  commit — wave's status commit then finds it); (b) the working tree of the root checkout — CI cannot judge the join
  (presence only), and a machine path enters the record.
- **F25 (OWNER) — which files are «основные» (F-d).** The meaning of her W3 sentence (11a). (a) main = CLAUDE.md,
  PROJECT.md, docs/TESTING.md, plans/builder-rules.md, docs/TEAMWORK.md, design/factory-rules.md, design/architecture.md,
  docs/SIBLING_MAP.md, PROCESS/*.md (recommended: the homes her process already treats as rules; executable on it until
  she answers); (b) the four boot-adjacent files of round 2 only — RUNBOOK-style service files pointing at
  PROCESS/SIBLING_MAP stay unguarded; (c) (a) + DECISIONS.md and docs/RUNBOOK.md.
- **F26 (Lead) — a new service `.md` file and the census.** (a) baseline 0: a count > 0 needs `rule-census-raise:` and the
  row (recommended: one definition, no silent raise by a new file; cost: one line per new non-excluded markdown file);
  (b) a census glob subset (role files, skills, briefs, PROCESS) — cheaper, a second set beside the scan set.

## Small choices closed by the designer

- Statuses stay code constants; types, origin heads, criteria, dispositions, confirmers and `carry_retired` are data.
- `tools/piles-vocab.json` keys ASCII, Russian words as values with `means` and (for criteria/confirmers) `word`.
- Old rows without `Тип` are counted, never red (E9).
- Flow window 7 days; ISO dates; SessionStart cap 5 s; reasons ≤ 120 characters.
- `Откуда` separator ` · ` (U+00B7).
- `collect_intake` writes `Откуда: находка <file>` and `Тип: неразобран` (F1 (a)).
- B is built on A1's branch and merged right after it (E25).
- C is a separate node before A2 (A2 imports C's `check_text`).
- The rule texts and the instance test land in ONE commit.
- The disposition word is `чужой-код`, the same word as the `leftover_criteria` key.
- R1: the critic's recommended placement (the (д) gate at commit-msg, `range_messages` in CI) taken; the `verdict:` line
  grammar (node part optional for one node) closed here.
- R2: the critic's recommended leaf module taken; its name `tools/piles_vocab.py` (underscore: importable).
- R3: the critic's recommended scope (worked batches; `миграция` exempt) taken.
- R4: the critic's recommended placement (commit-msg `--msg-file`, forge-check `--base` with range messages) taken.
- R6: the critic's recommended grammar (heading / item / bold lead-in, leading whitespace stripped, `\d+[a-z]?\.`) taken,
  plus the previous-line rule for a lead-in end and the literal kind for pointers.
- F-a: a `blocker` verdict refused with the `owner-word:` / `verdict: none` doors (critic's recommendation).
- F-b: the anti-laundering limit is 30 words (a shape limit, AT/BEYOND rows).
- F-g: the one-off briefs stay counted files (they never rise).
- `prose_lines` generalises `door_lines` (one reader of commit-message door lines).
- K's module is named `tools/rule_pointers.py` (it resolves pointers first; stamps are one of its uses).

## Noticed, not widened (analogs and contradictions)

- The debt file's header count ("25") contradicts its own rows (44) — told to the debt-fix stream (§3 M3).
- `.claude/settings.json` allow lines for the retired `board --check` (P23) — H.
- `backlog_tree.py` prints the first token of a status (P6) — B.
- The card «Содержание» column `тип` is the CARRIER kind, not the work type — keep the names apart (Lead's call).
- `wave.py` records the node status AFTER the push (P30): a refused status never undoes a merge; after R1 the status
  commit is judged by commit-msg like any commit.
- forge/3 and forge/6 were closed with `взял: —` (P28): F20 makes it a road.
- The forge/7 row of FG7-52 (P45) contradicts the accepted boot-by-topic A1 — handled by F23's amendment.
- The package has the same class (role files and `references/slices/*` carrying `design/*.md` rules; the slices are
  generated); §8 is forge-only; the package twin is an analog for the Lead (axis 34 / P31), not widened.
- AGENTS.md is a generated copy of the main files (excluded from the scan) — already the generated road.

## Reading trail

Round 1 and round 2: as recorded in round 2 (piles cards and batches, `tools/piles.py` ranges, `backlog_tree.py`,
`collect_intake.py:955-1014`, `mechanism_gate.py:205-284`, the debt file, the Lead queue, the brief, critic.md, package
tests, the architect-tier and boot-by-topic specs by Grep, the t-920 review, the schema and checker, `wave.py`,
`settings.json`, `dod_gate.py`, `session_context.py`, the axis-31 test, `factory_rules_index.py`, builder-rules,
WEEKLY by Grep, journal t-906).
Round 3 (t-945): the t-943 review whole; this spec whole; `tools/piles.py:1015-1054` (`door_lines`), `:1840-1858`
(`_node_reds`), `:2016-2027` (`check_form`), `:2325-2349` (`range_messages`, `cmd_check`), `:3220-3264` (`HAND_EDIT`,
`_status_evidence`) + Grep of defs/imports; `tools/wave.py:244-273` + Grep of defs; `tools/critic_verdict_check.py:63-82`
+ Grep of imports/defs/`VERDICT_ENUM`; `.githooks/commit-msg` whole; `.githooks/pre-commit` Grep `python|msg`;
`.github/workflows/forge-check.yml` Grep (`:52, 84, 96, 175`; a first Grep for `critic_verdict|pointer|rule_stamps|
test_role_carriers` → 0, positive control `pytest|piles\.py` → 4 lines); `tools/tests/test_role_carriers_one_owner.py:1-40,
53-137` + Grep of defs; `docs/tasks/specs/20261116-boot-by-topic-spec.md:400-421` + Grep `FG7-52|pointer_lint|rule: <|
правило: <|resolver` (lines 56, 71, 81, 87, 98, 407-418, 487, 498, 510, 682, 690, 704, 708, 759, 780, 816, 862, 865);
`PROJECT.md:322-341` + Grep `Остатков в идеале` and `^\s*9\.|^\s*\*\*[^*]+\*\*`; `tools/mechanism_gate.py` Grep
(`:215, 259, 274, 279`); `.claude/agents/critic.md:55-62` + Grep `exam` over `.claude/agents`; Grep `FG7-52|FG7-49|FG7-51`
over `plans/piles/forge`; Grep `commit-msg` glob `*.py` over `tools/` (14); Grep `piles_vocab|rule_pointers|rule_stamps`
over `tools/` and `.githooks/` (0) with the positive control `…|piles_split` (5 files). A repo-wide Grep for the new names
timed out (not used as evidence).
Not re-measured by me (no shell): P1, P4, P12, P13, P26, P28, P46 — from t-920 / t-943 reruns; the §8 census.
Needed beyond the manifest: `PROJECT.md:322-341`, `.claude/agents/critic.md:55-62`, `plans/piles/forge/batch-7-vhodyashchie-4.md:72-75`,
`tools/mechanism_gate.py` lines above (read-only).

## The owner's word on leftovers (17.11.2026, Lead session; answers to the t-906 origin table) — binds §2.2 and forks F2, F5

Verbatim, per origin:
- critic remarks about other code (20 of 206): «вот это можно оставлять» — a remark about code outside the node's topic may become a node.
- deferred minor critic remarks (51): «делать сразу» — fixed in the same node's fix round, no node, no «Остатки» row.
- the owner's new word during the work (31): «если я что-то новое сказала по теме работ, то надо делать сразу, если я просто сказала что-то из другой темы, то можно завести отдельным узлом».
- defect after acceptance or red CI (27): «CI не записываем отдельными узлами» — a red CI is repaired on the spot and is not a node.
- scope cut by the spec (24): «если я урезала для экономии токенов, то ок, в остальных случаях сделать сразу или спросить меня».
- the critic brief against PROJECT п. 9: «почему бриф противоречит? Это служебный фаил который никогда не должен противоречить основным» — a service file never contradicts the main rules; the brief is brought in line, and a check keeps it so.
- the rules-debt file (F8): «давай починим сейчас, правила это важно» — the open rows are FIXED now (a separate stream), not migrated into nodes; the file's fate is decided after it is empty.
Consequence for the forks: F2 is (a); the criterion of §2.2 is exactly the owner's list above.
(Designer's notes: "25" is the debt file's stale header; its own rows say 44 open — P17. F5 was answered later the same
day — W2. B5's class — W3, §8. The fate of the debt file was then answered by «всё по рекомендациям» — F8 (a), below.)

---

## Fix round t-926 — finding / word → what changed → section

| finding / word | what changed | section |
|---|---|---|
| B1 critic default rests on text and self-label | verdict `remarks` with a typed disposition; acceptance refuses a `чужой-код` remark inside `Пишет в`; back-reference checked at add time; error direction + adversarial inputs; alternatives weighed | §2.3, §4, §6, §7.2 C/A2, F17 |
| B2 forge/7 never closes | flow gate at ADD time with `приток:`; counter by `(slug, id)`; shown in summary/status/SessionStart; forge/7 as a container | §2.4, §6 E13/E16, §7.2 A3/G, F6, F13, F20 |
| B3 diverges from the owner's list | §2.2 row by row to her list; keys reduced; red CI never a node; scope cut only with her word | §2.2, §3 M3, §5.3-§5.6, §5.10 (e), §5.12 |
| B4 both worlds | legacy items by the cutover commit; (в) mask; (д) row identity | §4, §6 E9/E20 |
| B5 nothing keeps the brief in line | one home + pointers; instance test | §5, §5.14 |
| W1, W2, W3 | recorded; F5 executed; §8 | status block, F, §8 |
| N1-N10, key 7, t-906 marker | as listed in round 2 | Premises, §2.1, §2.5, §3, §5.12, §6, §7, F |

## Fix round t-945 — the t-943 verdict, remark by remark → what changed → where

| remark | what changed | section |
|---|---|---|
| R1 (BLOCKER) hand edit of `Статус` bypasses the B1 gate | the acceptance judgment moved into (д) `_accept_reds` at commit-msg (and forge-check over the range): a cell that becomes `принято` against the base needs a `verdict: [<node> ]<path>` or `verdict: [<node> ]none -- <why>` line; the join, the shape and F-a run there on the committed verdict file; `status`/`wave` only write the line (early check with the same function); `HAND_EDIT` text names the line; transition edges E37; error direction of `status_word` as a transition detector; leak L16 named | §1.1, §2.1 L16, §2.3 part 2, §4, §6 E37, §7.2 A2, §7.5, P7, P40 |
| R2 (BLOCKER) circular import piles ↔ critic_verdict_check | `node_vocab` lives in the stdlib leaf `tools/piles_vocab.py` (A1 owns), imported by `piles` (re-export), `collect_intake`, `critic_verdict_check`; graph stated; import rows in both orders; no back edge | §2.3 part 1 «The import graph», §4, §7.2 A1/B/C, §7.4, E8 |
| R3 (BLOCKER) flow brake reds the prescribed intake road | judged set = WORKED batches (taken, or closed ≥ 1 node in the window); an untaken batch with 0 closes is not judged and is printed as `входящие`; `миграция` rows exempt; seven edge rows; F13 re-checked against the scope | §2.4, §6 E47, F6, F13 |
| R4 (BLOCKER) pre-commit cannot read the doors | `rule_pointers.py check --msg-file "$1"` in commit-msg (after `piles.py check`), `--base` in forge-check reading `range_messages`; pre-commit placement withdrawn; doors read by `piles.prose_lines` | §8.3, §7.2 K, §7.3, §7.4, §7.6, §8.6 |
| R5 (BLOCKER) three pointer forms, two resolvers, two scan sets | SELF-CONTAINED §8.2: survivor = boot-by-topic's `rule:`/`правило:` form + one resolver `rule_pointers.resolve` (§4.3 kept, bold/literal kinds + uniqueness added); K-PTR rows → data rows resolved by it, retired as K2 writes pointer lines; `see:`/`rule_stamps.py` never built; FG7-52 absorbed by K or ordered before it (F23); service = the axis-31 scan set minus main (+ the template, widening only); K-OWN scope unchanged; F22, F23 | §8.1, §8.2 (whole), §7.2 K, §7.3, F22, F23, P44, P45 |
| R6 (BLOCKER) anchor grammar fails PROJECT.md:333 | grammar table for heading / item / bold lead-in / literal, leading whitespace stripped, `\d+[a-z]?\.` openers, `11a.`/`4a.` stated, previous-line rule against wrapped bold; 5.3 puts the home on its own line; the instance and its AT/BEYOND edges (mid-line → E31 with a hint); a D test row for the home's line start; K after boot-by-topic S1/S2/S3-2 | §8.2.2, §5 intro, §5.3, §5.14, §7.3, §8.6, P43 |
| F-a refuse a `blocker` verdict | refused at the gate and at `status`; doors `owner-word:` / `verdict: none` | §2.3 part 2, §6 E46 |
| F-b `see:` laundering | a pointed block counts as pointed only at ≤ 30 words of prose besides the pointer; AT/BEYOND rows | §8.4, §8.6 |
| F-c re-stamp without reading | E39: `src12` moved, `blk12` not → printed, counted by calibration item (v) | §8.3, §8.6 |
| F-d main list; builder-rules dual role | main list → ONE owner question F25 with the recommendation; builder-rules main for its own rules, its CLAUDE.md restatements → pointers in K2 | §8.1, §7.2 K2, F25 |
| F-e K2 target and cost | pointers by default, stamps only where the main file cannot be loaded (dispatch template, hook refusal); measured cost (P46) written into E33 | §8.5, §8.3 E33, P46 |
| F-f second door; exams | E30's text names `stamp-skip: <file>:<line> -- handed to Lead`; D's and K2's DoD carry the critic/scout exam run by the Lead before the commit | §8.3 E30, §5.11, §7.2 D/K2 |
| F-g baseline timing; new/deleted/renamed files; one-off briefs | `census --write` after architect-tier D6 and L; new file → baseline 0 + raise line (F26); deleted/renamed → row dropped, never red; one-off briefs stay counted (closed) | §8.4, §7.3, F26, small choices |
| F-h F7 rework | F7 states the rework of architect streams C, A5, F and recommends amending the architect-tier spec now (named, not written) | F7 |
| F-i F12 exception to the owner's criterion | criterion applied clause by clause: origin rules stay the home (5.3a), gate-held clauses go with 9a to TEAMWORK § 9 (5.3b), both worlds stated | §5.3, F12 |
| F-j silent §8 edges | pointer to any existing file; stamp source must be main; unclosed / nested stamps red; markers in fences ignored; main never service; index blobs under partial staging; generated sections | §8.2.5 |
| F-k Phase 0 forks | F8, F16, F18 now DECIDED (a) by the owner («всё по рекомендациям»); Phase 0 holds only Lead forks + F25; F16's text names CLAUDE.md rule 4; F18's names PROJECT п. 3 | §7.1, §2.2, F |
| F-l mechanism list | `piles-vocab.json`, `piles_vocab.py`, `critic_verdict_check.py`, its schema into `MECHANISM_PREFIXES` in A2's commit (not H); K's files in K's commit; P20 updated | §4, §7.2 A2/H, P20 |
| F-m order rows | §7.3 rows: K after boot-by-topic S1/S2/S3-2, FG7-52 per F23, K's census after architect-tier D6/L, TEAMWORK row | §7.3, §7.1 |
| F-n P16 wording | SIBLING_MAP's «Lead Queue» names CURRENT_CONTEXT.md today, `lead-queue.md` after architect stream F | P16 |
| class completeness — §8 forms: `see:` laundering, in-place edit "named partly" | laundering closed (F-b); in-place edit of an existing block named as a remaining road with its detector (calibration (v), K2) | §8.4, §8.6 |
| class completeness — §8 scope (main list, service set vs the axis-31 scan) | one scan set (8.2.4), main list as F25; K1 roads d/e/f closed or forked | §8.1, §8.2.4, §8.6, F25 |
| class completeness — anchor grammar vs the real instance and boot-by-topic headings | R6 | §8.2.2, §7.3 |
| class completeness — hook placement and CI range messages | R4 | §8.3 |
| class completeness — doors for the refused party | F-f | §8.3 E30 |
| class completeness — B1 class: every writer of a node's `принято` (status, wave --node, hand edit); verdict values | R1 (all three writers meet (д)), F-a | §2.3 part 2 |
| class completeness — B2 class: every adder of rows (intake, migration, Lead, collect_intake) | R3 (intake and collect_intake not judged in an untaken unworked batch; migration exempt; the Lead's adds into worked batches judged) | §2.4 |
| class completeness — SIBLING_MAP axes beyond 1/4/18/31/34 left to the committer's rule-10 enumeration | kept as stated: every mechanism commit of A1/A2/A3/C/D/K carries the full enumeration; the likely axes listed | §7.6 |
| K1 road e (files outside the globs: PROCESS, SIBLING_MAP, template, CURRENT_CONTEXT, `tools/*.py` texts) | folded into R5: the one scan set covers them; the template added by `scan_extra`; PROCESS/SIBLING_MAP main under F25 (a) | §8.1, §8.2.4 |
| K2 / K6 four questions (a) cost, (c) detector, (d) what stops skipping | (a) E33 with P46; (c) item (v) + E39; (d) commit-msg + forge-check `--base` + the test in CI | §8.3, §8.6, §7.6 |
| t-943 N7 spot-check (P16 wording) | = F-n | P16 |
| the owner's forks F1, F8, F14, F16, F18, F19 (decided (a)) | stated as the spec's behaviour: §1.1 (F1), §1.3/§2.2 4b/5.3a/5.5 (F16), §2.2 row 7/5.3a/5.12 (F14), §2.2/5.3a/E18 (F18), §2.2/5.3a (F19), §3 M3/§4/§5.6 (F8); §2.5 recomputed (44.7 % certain) | as listed, F |

## The owner's word on the OWNER forks (17.11.2026, Lead session)

«всё по рекомендациям» — **F1 (a)**, **F8 (a)**, **F14 (a)**, **F16 (a)**, **F18 (a)**, **F19 (a)**. The streams are
built on these answers; the fork paragraphs above stay as the record of the alternatives.

## Lead decisions on the r3 forks (17.11.2026, Fable)

**F22 (a)** — the one pointer form is boot-by-topic's `rule:` / `правило: <file> § <x>`. **F23 (a)** — stream K absorbs
FG7-52 (the resolver is built once). **F24 (a)** — the gate reads a verdict file from the committed tree only; the Lead
commits the critic's report before or with the accepting commit. **F26 (a)** — a new service `.md` file starts at
baseline 0. **F7 (a)** and **F12** (clause by clause, as §5.3 states) stand; the architect-tier amendment F7 names is
written by the Lead after that spec's streams B–F pass their critic. **F25** is the owner's; executable on (a) until
her word.

## Слово владельца 17.11 (четвёртая порция): F25 и приоритет

- F25, какие файлы «основные»: «скорее этот вариант» — широкий: рекомендованный список плюс `DECISIONS.md` и
  `docs/RUNBOOK.md`; «как минимум всё что у нас в бут пути». «Проверь что между всеми перечисленными мы убрали все
  противоречия» — разовая сверка основных файлов между собой входит в объём темы (узел сверки: судит роль, не код;
  найденное противоречие чинится в том же узле или выносится владельцу, если это выбор смысла).
- Приоритет: «у этого самый низкий приоритет из всех перечисленных» — тема идёт после «Архитектора», долга правил,
  сухой стори, «сказано до работы» и правил тестов; пишущие слоты у них не отнимает.
