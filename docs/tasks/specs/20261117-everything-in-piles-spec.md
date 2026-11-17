# Spec t-907 — «Всё в кучках»: one registry of work, leftovers that do not breed nodes (DRAFT r2, designer)

Status: DRAFT round 2 for Lead acceptance — fix round t-926 after the plan critic t-920
(`docs/tasks/specs/reviews/t-920-everything-in-piles-plan.md`, verdict GO WITH FIXES: B1-B5, N1-N10). Every finding is
applied; the table «Fix round t-926» at the very end maps each finding and each owner's word to what changed and where.
Forks are returned (section F); decided forks are listed as decided with their carrier. The section «The owner's word on
leftovers» (just before the fix table) is the criterion of §2.2 and overrides anything here that diverges.
Three more words of the owner arrived during this round (17.11.2026, relayed by the Lead in the t-926 dispatch thread):
(W1) «ок» to the Lead's decisions on B1-B5 — they stand as decided; (W2) F5 decided: «ок» to "the owner or the batch
Lead"; (W3) B5 is a CLASS: «это починит только одно место. А надо что бы все служебные файлы не противоречили основным
даже если мы будем основные каждый день менять.» — answered by §8 (its own stream K).
Owner-facing rule texts are Russian; code, tool messages and data keys English (PROJECT.md «Язык»).

```
task: t-907 (draft), fix round t-926 | feature: F19 | each build node gets its own task_id (CLAUDE.md rule 2 threshold per node)
designer: this file
```

The owner's decision (17.11.2026, Lead session): «ВСЁ В КУЧКАХ» — the only registry of work on the factory and the forge
is the piles (`plans/piles/<slug>/`); everything that is work is a NODE of a batch; the type of work is a field of the
node; a big idea is its own batch with a plan file; the Lead queue, the FR debt and batch leftovers become nodes;
`plans/BACKLOG.md` stays an archive. For the FR debt the owner later said «давай починим сейчас» (section «The owner's
word»): the debt rows are FIXED by a separate spec, not migrated (§3, F8).

---

## Premises (load-bearing facts, each with its carrier)

| # | fact | carrier / command | state |
|---|---|---|---|
| P1 | 103 batch files; 36 not closed = 26 `ожидает` + 10 `в работе`; 67 `закрыта` | Grep `^кучка:.*\| статус: (…)` glob `batch-*.md` over `plans/piles`; t-920 key 1 re-ran it (`uniq -c`) | measured (twice) |
| P2 | Every batch's node table has the SAME 7 columns `Узел \| Приоритет \| Что \| Исполнитель \| Пишет в \| Зависит от \| Статус` (hotfix-12586/2 has 3 helper tables above it) | Grep `^\| *Узел *\|` glob `batch-*.md` → 106 lines in 103 files | measured |
| P3 | No `Тип` / `Откуда` column exists anywhere; the parser knows `узел/исполнитель/пишет в/статус/что` only | Grep `^\|.*\| *(Тип\|Откуда) *\|` glob `batch-*.md` → 0; positive control of the SAME shape `^\|.*\| *(Приоритет\|Откуда) *\|` → 103 files; `tools/piles.py:608-609` `NODE_COLS`, `NODE_REQUIRED` | measured / read |
| P4 | ~691-698 table rows end in a cell starting `ожидает`, in 32 batch files | Grep tool → 698; t-920 shell grep → 691 (±1 %, the two tools' line-end handling) | measured |
| P5 | One status vocabulary in code: `BATCH_STATUSES`, `NODE_STATUSES`, `STATUS_ORDER`, read by `status_word` | `tools/piles.py:111-115, 200-206` | read |
| P6 | A second copy of status words in `tools/backlog_tree.py:19-20, 40-50` (`CLOSED_WORDS`, `DONE_NODE` with `закрыт`); the pane prints `status.split()[0]` | read in round 1 (not re-read: not load-bearing for the fixes) | read |
| P7 | (д) refuses a node status that starts with no word of P5 (`_node_reds`, `piles.py:1846-1857`) | t-920 key 1 confirmed | read |
| P8 | 18 of 103 batches are leftover batches by name (`ostatki`, `hvosty`, `tails`, `leftovers`, `remainders`), 7 more "incoming" (`vhodyashchie`) | file names of P1 | measured |
| P9 | Leftover roads: (a) critic brief q4 routes an out-of-owns analog to «Остатки» as `узел:` or `перенос:` with `подтвердил: —`; (b) q7 severity `queue` ("blocks / fix before merge / queue"); (c) q12(d) "a fix in this round or a node with an id and an owner"; (d) `piles.py` write-time gate accepts `узел:` (no back-reference) and `перенос:` with a placeholder `подтвердил:`; (e) `close` accepts `перенос:` with any non-placeholder `подтвердил:`; (f) builder-rules п. 1 «Needed from integration»; (g) CLAUDE.md rule 9 "fix now, or EXPLICITLY put the remainder in the queue/log"; (h) rule 12 Cost gates: the fix round is a FRESH worker with the diff and the verdict | (a)-(c) `docs/tasks/critic-diff-brief.md:31-34, 56, 91-93`; (d) `tools/piles.py:2826-2852`; (e) `:2767-2788, 2962-2994`; (f) `plans/builder-rules.md:10` (round 1 said 8 — corrected, t-920 N1); (g)/(h) CLAUDE.md | read |
| P10 | Observed: forge/7 «Ход» 03.11 critic t-1756 findings queued, not fixed; 14.11 "очередь критика диффа FG7-32 (t-750) заведена узлами FG7-34 … FG7-35"; 12.11 "Не оформлены находками: три предложения узлов критика t-124" | `plans/piles/forge/batch-7-vhodyashchie-4.md:86, 88, 89` | read; t-920 confirmed |
| P11 | `close` refuses a bare `узел:` item ("closed by «сделано: …» when the node merges, or carried") | `tools/piles.py:2979-2980` | read |
| P12 | (е) splits findings at `FINDINGS_FROM = 2026-10-13`; today: 1110 findings read, 0 newer orphans, **152 older orphans (69 of them undated)** | `tools/piles.py:2038`; `python -B tools/piles.py check --all` (е) line, run by t-920: `(е) findings: ok (1110 findings read, 0 dated from 2026-10-13 on are orphans, 152 older are the baseline)`, `WARN: 152 … or undated (69)` | MEASURED (t-920) |
| P13 | 1110 finding files; 33 piles | t-920: `ls …/findings/*.md \| wc -l`; `summary` `кучек: 33` | measured |
| P14 | `docs/tasks/lead-queue-fable.md`: 12 numbered items + 2 lines; 10 done, 2 open (п. 11 boot budget; the two count lines of `tools/test_hook_liveness_probe.py`) | `docs/tasks/lead-queue-fable.md:7-24`; t-920 confirmed | read |
| P15 | The two open Lead-queue items already have pile nodes: boot budget ↔ FG7-51; hook-probe count literals ↔ FG7-49 | `plans/piles/forge/batch-7-vhodyashchie-4.md:72, 74` | read |
| P16 | Readers of `lead-queue-fable.md`: no code. The ACCEPTED architect-tier spec (its F8 (a)) `git mv`s it to `docs/tasks/lead-queue.md`, adds `docs/tasks/architect-queue.md`, counted by `session_context.py` (its stream C), named by `mechanism_gate._tier_queue_note` (its A5), calibration check 49 (b) (its stream F), `docs/SIBLING_MAP.md:655-661` «Lead Queue» → `lead-queue.md` | Grep `_tier_queue_note\|49 \(b\)\|Lead Queue\|architect-queue\|lead-queue\.md` over `20261116-architect-tier-spec.md` (read-main worktree): lines 34, 53, 413, 418, 426, 474, 607, 616, 699 | read |
| P17 | The debt file's header says "Twenty-five rows are open today"; its tables hold 47 data rows + 3 walk entries, 6 of them "Closed by …" (lines 93-96, 98, 99) → **44 open by the file's own rows** (the owner's section quotes the stale 25) | `ai-packages/qa-factory/design/factory-rules-debt.md:5-6, 19-141`; t-920 key 1 enumerated | read twice |
| P18 | Readers of the debt file: `tools/piles.py` `DEBT_REL` + `debt_warnings`; `tools/test_piles_close_id.py:87-89`; package tests G1-10 (`test_s1_s2_contract.py:322-325`) and K0.15 (`test_null_outcomes.py:589-596`); `test-layers.json:3413`; `factory-rules.md:230, 305`; `design/README.md:29`; comments and forge docs | Grep `factory-rules-debt` → 54 files (60 with untracked ledgers, t-920) | measured |
| P19 | `tools/collect_intake.py:979-1003` builds a node row for an untaken batch from the table header (`values` keyed `узел/что/исполнитель/пишет в/статус`; any other column → `—`) | read; t-920 confirmed | read |
| P20 | Mechanism paths (commit = Lead, axis block + `tier:`): `tools/piles.py`, `tools/md_table.py`, `tools/compact_snapshot.py`, `tools/wave.py`, `.claude/agents/`, `.claude/settings.json`, `CLAUDE.md`, `PROCESS/`, `docs/SIBLING_MAP.md`; NOT: `PROJECT.md`, `plans/builder-rules.md`, `docs/tasks/critic-diff-brief.md`, `tools/backlog_tree.py`, `tools/collect_intake.py`, `tools/critic_verdict_check.py` | `tools/mechanism_gate.py:211-283`; t-920 confirmed | read |
| P21 | The critic verdict JSON: `verdict`, `blockers`, `class_completeness`, `trail`, `fixes`; `additionalProperties: true`; no per-remark field; `blockers`/`fixes` are arrays of strings | `tools/critic_verdict.schema.json:7-52` | read |
| P22 | Text anchors pinned by tests in files this spec edits: brief `## The two layers`, `6. **DUPLICATION AND CONSISTENCY**`, `7. **CODE QUALITY**`, `12. **ONE ROAD**`; K-OWN keys in the brief: «functions over roughly 60 lines or with more than three nesting levels in the NEW code» (q7) and «a line for the coordinator to tell someone is itself a finding» (q12(d)); builder-rules 7b; CLAUDE.md rule 9 key «the rule against recurrence goes on the highest level that ties the siblings together»; COST anchor «Cost gates (D-0035, D-0038, D-0040, D-0054;» | `tools/tests/test_role_carriers_one_owner.py:28-74`; `tools/install_parity_anchors.json:22`; `tools/test_handoff_rule_anchors.py:38-39, 94, 107` | read |
| P23 | `.claude/settings.json:157, 176` still allow `python tools/piles.py board --check` — `board` is a refused alias | Grep; t-920 confirmed | read |
| P24 | DAG-like files under `docs/tasks/`: `factory-fixes.md`, `test-diet.md` (nodes outside piles), `onboarding-streams-2026-11-12.md` (waves over pile nodes) | first 15 lines of each (round 1) | read |
| P25 | Plans of big ideas: the six of t-895 are not on disk as a list | Glob `plans/*.md` | the Lead supplies the six (t-895 trail) |
| P26 | `BACKLOG.md`: **296 open ids** (in batches 114 / in findings 182 / not placed 0) | `python -B tools/piles.py summary`, run by t-920 | MEASURED (t-920) |
| P27 | **The t-906 origin table** — 206 leftover items over 11 batches, by origin: critic deferred minor 51; owner's new word during the work 31; defect after acceptance / red CI 27; calibration / process 27; scope cut by the spec 24; critic about other code / wider class 20; builder-noticed 14; new ideas 8; live proof 4 | scout t-906, accepted `logs/journal/dev1.jsonl:2244` ("leftover origins: 206 items, 11 batches; trail present"); the per-origin numbers quoted in t-920 key 2 and in the owner's-word section below | from the accepted digest, quoted twice |
| P28 | forge/7: header `статус: ожидает \| взял: —`; 54 node rows, 16 `принято`, 38 `ожидает`; 28 commits. Two earlier forge batches were closed while untaken: forge/3 and forge/6 headers `статус: закрыта \| взял: — \| … MR: \`855d4e5c\`` | t-920 key 1 (status loop); Grep `^кучка:` over `plans/piles/forge` → 7 headers | measured / read |
| P29 | A NODE status is set on an untaken batch without any check of the batch's status: `cmd_status` → `_status_node_row` / `_status_node_cell` (no `FROZEN` test); only the BATCH branch `_status_batch_plan` refuses an untaken batch ("take it first") — this is how forge/7 accepts nodes without ever being taken | `tools/piles.py:3267-3362`, `:3300-3302` | read |
| P30 | `wave.py merge … --node` records the node through `piles.py status <slug> <N> <id> --set принято --hash --task` AFTER the merge push; a refusal there does not undo the merge — it prints "run by hand …" and exits 1 | `tools/wave.py:14, 24, 251-271` | read |
| P31 | `critic_verdict_check.py` is on NO execution path: no hook or tool calls it (only its test and docs); the critic self-runs it on its own report and the coordinator runs it by hand (`critic.md` rule 17) | Grep `critic_verdict_check\|validate_verdict\|check_text\(` over `tools/*.py` → only the tool itself, its test, comments in `escape_check.py`/`md_regions.py`/`test_p4_stdin_deadline.py`, `test_handoff_rule_anchors.py` (text anchor); `.claude/settings.json:163` is an allow line; `.claude/agents/critic.md:140-151` | measured / read |
| P32 | (в) compares a taken batch's node table CELL BY CELL against origin/main with only the `Статус` cell masked (`_frozen_lines`): adding a column changes every row → red. The «Остатки» multiset rule (`_leftover_write_reds`) keys an item by its whole stripped text | `tools/piles.py:1644-1677, 1696-1702, 2855-2889` | read |
| P33 | `tools/tests/test_role_carriers_one_owner.py`: K-OWN (an owner key occurs in exactly one scanned file) and K-PTR (POINTERS: carrier holds the pointer, target holds the anchor). Named blind spot: a restatement in another language does not match the key (false pass); K-PTR errs safe (a renamed anchor turns red). PROJECT.md, CLAUDE.md, `.claude/agents/*`, the brief, builder-rules are scanned; `plans/piles/`, `docs/tasks/specs/`, AGENTS.md are not. Its POINTERS and OWNER_KEYS are hand-kept Python lists (20 + 13 rows), not a data file | `tools/tests/test_role_carriers_one_owner.py:1-26, 35-74, 105-134` | read |
| P34 | The debt-fix spec `docs/tasks/specs/20261117-rules-debt-fix-spec.md` is NOT on disk yet (in progress, the Lead's word in the t-926 dispatch) | Glob `docs/tasks/specs/20261117-*` in the root and in both worktrees → only this spec (positive control: the same glob finds this file) | measured |
| P35 | `dod_gate.py` (SubagentStop) already reads a stopping worker's own dispatch text (owns through `dispatch_manifest.owned_paths`, `_worker_cut`) and its named handoffs — the base of the cheaper alternative weighed in F17 | `tools/dod_gate.py:356, 393-531` (defs and docstrings) | read (defs, not every line) |
| P36 | `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` describes the `перенос:` form in check 33 (line 1026) and check 39 (line 1095, (д) refuses an item without `сделано:` / `узел:` / `перенос:`, the human-confirmation reading) | Grep `перенос:` over the file → lines 1026, 1095 | read |
| P37 | boot-by-topic fragments: 2c («Находка сразу попадает в пачку»), 2d («Содержание»), 9a («Пачка закрывается доделкой»), 9b («Живые доказательства») → `docs/TEAMWORK.md`; 9c («перенос подтверждает человек»), 9d («Остатков в идеале нет вовсе»), 9e, 9f stay in boot. Its move criterion is the gate column ("none" → boot) | `20261116-boot-by-topic-spec.md:292-308` (read-main worktree) | read |
| P38 | The generated-copy road exists: `tools/factory_rules_index.py` writes `docs/FACTORY_RULES_INDEX.md` from `factory-rules.md` and `--check` compares byte-for-byte in pre-commit ("a commit where the rules changed and the index did not" is refused); `tools/architecture_index.py --check` is the same road | `tools/factory_rules_index.py:1-17`; CLAUDE.md rule 10 | read |
| P39 | Service files today (one Glob `{.claude/agents/*.md,.claude/skills/**/SKILL.md,docs/tasks/*brief*.md}`): **18** — agents 5 (builder, critic, designer, judge, scout), skills 8 (boot-diet, critic-exam-gen, next-task, onboarding, permission-audit, scout-exam-gen, session-handoff, session-retro), briefs 5 (`critic-diff-brief.md`, `pre-release-0.9-brief-common.md`, `pre-release-0.9-critic-brief.md`, `test-diet-brief.md`, `test-diet-fold-brief.md`). Stamps of the §8 form: 0 (Grep `source: [^ ]+#.+ @ [0-9a-f]{7,}` over `*.md` → 0; no positive control exists — the form is new; the first stamp K writes is the control) | Glob / Grep in this round | measured (the set); the census count: §8.4 |

---

## 1. Target model

AR-n: this spec does not change `ai-packages/qa-factory/` (stream F of round 1, the only package part, is removed — §3,
F8), so no AR-n of `design/architecture.md` is touched; the forge analogs it keeps are listed in §7.6.

### 1.1 One node table for every batch

```
| Узел | Тип | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Откуда | Статус |
```

- Two NEW columns, `Тип` and `Откуда`, at those positions; the other seven unchanged (P2).
- `Тип` — one word of the closed list `node_types` in the data file `tools/piles-vocab.json` (FR-13 / AR-1 analog).
  Words: fork **F1** (OWNER). The spec is executable on the recommendation: `баг`, `доделка`, `идея`, `оптимизация`,
  `долг` (the owner's five) + `живой-прогон`, `решение` + `неразобран` (the DECLARED unknown that `collect_intake` writes;
  code never picks a work type, FR-59).
- `Откуда` — one of the closed forms (heads in `node_origins` of the data file, grammar in `piles.py`):

  | form | meaning | checked at add time (§4, (д)) |
  |---|---|---|
  | `план` | written with the batch or the idea's plan | — |
  | `находка <file>` | a finding of this pile (`<file>` = the name under `findings/`) or `<slug>/findings/<file>` | the file exists in the working tree |
  | `владелец <дд.мм.гггг>` | the owner's word (off the running work's topic, §2.2 row 3) | a real date with a 4-digit year |
  | `миграция` | moved by THIS spec (§3) | — |
  | `остаток <node> · <key>[ · <carrier>]` | born from the work of another node; `<node>` = `<id>` (same pile) or `<slug>/<N>/<id>`; `<key>` ∈ `leftover_criteria` (§2.2); `<carrier>` as the key demands | the parent row exists; the key is in the list; the carrier per key (§2.3) |

  The separator is ` · ` (U+00B7 with spaces) — never `|` (cell-safe).
- `Статус` — unchanged vocabulary (P5); ONE reader `piles.status_word`; `backlog_tree.py` drops its own words (P6).
  A dropped node is `отклонено: <why>`.
- Priority stays a node column; the batch header `приоритет:` stays the default.

Invariant (P31, AR-13 analog): every batch of every pile is read by the one parser `piles.parse_batch`; a NEW row in any
pile needs the same columns.

New required fields and their EMPTY outcome / OLD rows:

| field | empty outcome | old rows (written before A1) |
|---|---|---|
| `Тип` | none for a NEW row: `—`/empty is refused; the unknown is the word `неразобран` | `—` or no column: legal while the row is OLD (§6 E9: key = id + its other cells, found in the same pile at the base) |
| `Откуда` | none for a NEW row | the same as `Тип` |
| batch header `план:` | absent = not a big-idea batch | absent |
| `подтвердил:` on a NEW `узел:` «Остатки» item (F5 decided) | none: required, `<владелец \| Lead пачки>, <дд.мм.гггг>` | legacy `узел:` items (before the cutover, §6 E20) pass without it |

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
- A red CI is NOT a finding and not a node (owner's word; §2.2 row 4, fork F15 on the record's carrier).

### 1.4 What a leftover is under the new model

A «Остатки» item = something that came up while working the batch. Legal NEW forms: `сделано: <hash | t-nnn>` (fixed
now — the default) or `узел: <node> | подтвердил: <владелец | Lead пачки>, <дд.мм.гггг>` whose row says
`Откуда: остаток <a node of this batch> · <key>[ · <carrier>]` (the confirmation: F5, decided by the owner 17.11.2026).
`перенос:` stops being a NEW form of «Остатки» and «Живые доказательства» (fork **F4**, Lead); items written before the
cutover keep closing by the old form (§6 E20, B4).

---

## 2. The leftover problem (core)

### 2.1 Where leftovers come from (measured) and which carrier lets them through

Origin shares from P27 (t-906, 206 items, 11 batches; percentages = count / 206):

| origin | count | share | the owner's word (17.11) | leak carrier today | stream (§7) |
|---|---|---|---|---|---|
| critic: deferred minor remark | 51 | 24.8 % | «делать сразу» | brief q4/q7/q12(d), critic.md rules 5/19 (L1-L3), `piles.py` `узел:`/`перенос:` cheaper than a fix (L4-L6) | C, A2, D |
| owner's new word during the work | 31 | 15.0 % | on-topic → now; off-topic → may be a node | practice; no carrier says it (L13) | D |
| defect after acceptance / red CI | 27 | 13.1 % | «CI не записываем отдельными узлами» | PROJECT «Как принимается» п. 2: red `main` → «находка в `findings/`» (L11) | D |
| calibration / process | 27 | 13.1 % | — (legitimate nodes) | — | — |
| scope cut by the spec | 24 | 11.7 % | legal only «для экономии токенов»; else do or ask | spec non-goals, no gate (L12) | D (+ critic-on-plan key) |
| critic: other code / wider class | 20 | 9.7 % | «вот это можно оставлять» | — (legitimate as `чужой-код`) | C, A2 |
| builder-noticed | 14 | 6.8 % | not in her list (fork **F14**) | builder-rules п. 1 «Needed from integration» (L7) | D |
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
| L14 | an untaken batch is worked node by node and never closed: every close-time brake misses it (forge/7, P28/P29) | `piles.py` `cmd_status` node branch |
| L15 | a service file (brief, role file, skill) restates a main rule and drifts from it (the brief vs PROJECT п. 9) | every service file — §8 |

### 2.2 The criterion: when a follow-up may be a node at all (= the owner's list, verbatim origin by origin)

| # | origin | rule (the owner's word, quoted in the section at the end) | node? | `leftover_criteria` key / `Откуда` |
|---|---|---|---|---|
| 1 | a critic remark about the node's OWN code (in its `Пишет в`), minor included | «делать сразу»: fixed in the same node's fix round; no node, no «Остатки» row | never | — (verdict disposition `fix`) |
| 2 | a critic remark about code OUTSIDE the node's topic (outside its `Пишет в`) | «вот это можно оставлять» | may | `чужой-код` + carrier `<verdict path>#<remark id>` |
| 3 | the owner's new word during the work | on the topic of the running work → done in that work; on another topic → may be a separate node | off-topic only | not a leftover: `Откуда: владелец <дд.мм.гггг>` |
| 4 | a red CI | «CI не записываем отдельными узлами»: repaired on the spot | never | — (record: fork **F15**) |
| 4b | a defect after acceptance that is not a red CI | not in her list: fork **F16** (OWNER; recommended: the same as row 4 — fixed on the spot as a new task_id with `defect_found`, no node) | per F16 | — |
| 5 | a scope cut by a spec | legal only when the owner cut it «для экономии токенов» and that word is recorded in the spec with its date; otherwise the work is done now or the owner is asked | only with her word | `экономия-токенов` + carrier `<spec path>`; the row is `Тип: доделка` |
| 6 | a live proof | her word 11.11.2026 (PROJECT «Командная работа» п. 9, «Живые прогоны не держат пачку вообще»): the proof row goes to `live-runs` | yes, in `live-runs` | `живой-прогон` |
| 7 | a builder-noticed analog | not in her list: fork **F14** (OWNER; recommended: the same as rows 1/2 — own code fixed now, other code `чужой-код`) | per F14 | per F14 |

`leftover_criteria` (data, `tools/piles-vocab.json`) therefore holds exactly `чужой-код`, `экономия-токенов`,
`живой-прогон`, each with a `word` field naming the owner's carrier (17.11.2026 / 11.11.2026). Round 1's `другая-кучка`
and `слово-владельца` are removed (t-920 B3.1, B3.2). `занятый-файл` and `ждёт-события` are NOT in her list and are
removed as reasons; each is an OWNER fork with its consequence (**F18**, **F19**); until her answer the spec runs on the
recommendation "not a node": the node stays open and does a second round after the other batch merges / the event
happens.

Size is NOT a criterion (F2 decided (a) by the owner): a remark too big for one round is a SECOND fix round of the same
node (same node id; `attempt` grows only on a `rejected`).

Who judges (P27, AR-29 analog): the critic labels each remark `fix` or `чужой-код` in its verdict (§2.3); code refuses a
`чужой-код` label on a path inside the node's `Пишет в` (data: a path join, not wording); whether a remark is truly about
another topic when its path is outside is the critic's judgment, accepted by the Lead. A node leftover is confirmed on its
«Остатки» item by the owner or the batch's Lead (F5, decided). Scope cuts: the critic-on-plan checks that every non-goal
deferring in-topic work quotes the owner's word (§5.10 (e)).

### 2.3 The machine layer (B1): the critic's remark carries a typed disposition; the acceptance road judges it

**Recommended (the Lead's design, decided by the Lead and «ок» by the owner, W1; code point = F17 (a)).** Three parts,
all data checks:

1. **Verdict schema** (stream C). `tools/critic_verdict.schema.json` and `tools/critic_verdict_check.py`
   `validate_verdict` gain a REQUIRED array `remarks`:
   ```json
   "remarks": [{"id": "B1", "disposition": "fix"}, {"id": "N7", "disposition": "чужой-код", "path": "tools/session_context.py"}]
   ```
   Rules (new helper `_remark_errors(obj)` called from `validate_verdict`):
   - `remarks` is an array; EMPTY OUTCOME: `[]` is legal exactly when `blockers` and `fixes` are both empty (a clean
     `fit`); a `fit` may also carry only `чужой-код` remarks.
   - each item: `id` — 1-20 characters `[A-Za-z0-9._-]`, unique in the array; `disposition` — a key of
     `remark_dispositions` in `tools/piles-vocab.json` (`fix`, `чужой-код`; read through `piles.node_vocab`, the one
     reader); `path` — REQUIRED for `чужой-код`, a non-empty string ≤ 300 characters, no `..` segment, no line break;
     ignored for `fix`.
   - every entry of `blockers` and `fixes` starts with the `id` of one `fix` remark (its first whitespace-separated
     token, trailing `:` stripped); every `fix` remark is named by exactly one such entry; a `чужой-код` remark is named
     by none (it neither blocks nor is fixed in this round).
   - diagnostics stay ASCII-only (the file's invariant): `field 'remarks[3].disposition' invalid: expected one of the keys
     of remark_dispositions in tools/piles-vocab.json`; `field 'remarks[3].path' required when the disposition is the
     other-code key`; `entry fixes[2] names no fix remark: expected its first token to be the id of a remarks item with
     disposition fix`.
   - OLD verdicts (written before C, no `remarks`): `check_text` fails them with `missing required field: remarks`. They
     are history; nothing re-checks them, except when one is given to `status --verdict` (below), which refuses with
     the door `--no-verdict "<why>"`.
2. **The acceptance road** (stream A2). `piles.py status <slug> <N> <id> --set принято --hash <h> --task <t>` gains
   EXACTLY ONE of `--verdict <path>` / `--no-verdict "<why>"`, and an optional `--owner-word "<кто, дата>"`;
   `tools/wave.py merge … --node <slug> <N> <id>` gains the same three and forwards them (`record_node`, `by_hand`,
   `build_parser`). New `piles._verdict_problem(root, nd, path, owner_word) -> str | None`:
   - reads the file (absolute, or relative to the repo root; wave resolves it against the ROOT checkout, since a
     review file may be uncommitted), extracts the verdict through `critic_verdict_check.check_text` (one reader of the
     shape);
   - for every `чужой-код` remark: normalise its `path` and every token of the node's `Пишет в` (`_norm_token`: repo
     prefix of an absolute path stripped, `\` → `/`, `./` stripped, a trailing function list dropped) and compare with
     `tokens_overlap`, CASE-FOLDED; any overlap → refusal (below), unless `--owner-word` is given (P13: the owner's word
     passes the whole call and is recorded);
   - `--set` to anything but `принято`, or a BATCH-level call, takes none of the three (refused like `--hash` today).
   Refusal texts (FR-1/FR-2; nothing is written on any refusal):
   - missing both: `a node is accepted on its critic verdict: expected --verdict <the critic's report file> or
     --no-verdict "<why>" (critic skipped, a decision node, …); nothing was written`.
   - both given: `--verdict and --no-verdict exclude each other -- give one; nothing was written`.
   - unreadable: `cannot read the verdict <path> (<os error>) -- expected the critic's report file (the handoff: file of
     its dispatch); or pass --no-verdict "<why>"; nothing was written`.
   - invalid shape: `the verdict <path> is not a valid critic verdict: <the check's lines, first 5> -- the critic
     re-emits it (tools/critic_verdict_check.py <path> must exit 0); a verdict written before remarks existed: pass
     --no-verdict "verdict predates remarks"; nothing was written`.
   - the core refusal: `<slug>/<N> <id>: the verdict <path> marks remark <rid> as «чужой-код» on <path>, which is inside
     the node's «Пишет в» (<token>) -- a remark about the node's own code is fixed in this node (PROJECT.md «Командная
     работа» п. 9). Expected: every «чужой-код» remark names a path outside «Пишет в». Doors: run a fix round and have
     the critic mark it fix; if the code is really another topic's, have the critic name that exact path; or pass the
     owner's word: --owner-word "<кто, дата>". Nothing was written`.
   - the informed passes (FR-4) are recorded: the status commit message (wave's and the printed `Next:` line) ends with
     `verdict: <path>` | `verdict: none -- <why>` and, when given, `owner-word: <кто, дата>`; calibration check 33 counts
     `verdict: none` and `owner-word:` lines (§5.12).
   - wave refuses at step 0, before any push, exit 2, when `--node` is given without `--verdict`/`--no-verdict`:
     `with --node, name the verdict the node was accepted on: --verdict <critic report> or --no-verdict "<why>" --
     nothing was merged`.
3. **The back-reference** (stream A2, in (д)). A NEW node row whose `Откуда` is `остаток <parent> · чужой-код ·
   <verdict path>#<rid>` is red unless: the verdict file exists and passes `check_text`; remark `<rid>` exists with
   disposition `чужой-код`; the row's `Пишет в` overlaps the remark's `path` (the node works the remark's code).
   `экономия-токенов` needs `· <spec path>` naming an existing file (whether it quotes the owner's word is the
   critic-on-plan's judgment, never a phrase search — FR-12). `живой-прогон` needs no carrier and the row must sit in
   pile `live-runs`.

Error direction (a reused function in a more consequential role, designer rule 1): `tokens_overlap` (today the (б)
overlap gate between batches) becomes part of the acceptance gate. It may REFUSE a valid remark (false red; door: the
critic names the exact path, or `--owner-word`), never PASS a `чужой-код` remark inside the owns. Adversarial inputs
that must stay REFUSED (one row each in `tools/test_piles_close_gate.py`): the remark path absolute
(`C:/QAFactory/forge-repo/tools/piles.py`) vs a relative owns token; backslashes; `./tools/piles.py`; another case
(`Tools/Piles.py`); a trailing function list (`tools/piles.py (cmd_status)`) against owns on the same file with another
function list (file-level overlap: refused — over-refusal accepted); a directory `tools/` against owns `tools/piles.py`;
a glob `tools/*.py`. Must PASS: a path outside the repo; a path in another directory; owns `нет`/`—` (a decision node
writes nothing, so nothing of its own can be deferred). Refused at the schema: an empty path, `..`, a line break, a
disposition not in the list.

Escape that remains (stated, t-920 B1): a Lead who files a remark as `Откуда: находка` with a new finding file, or as
`план`, bypasses the back-reference. It is caught by the flow brake (§2.4: every added row counts, whatever its
`Откуда`) and by calibration check 33's new item (§5.12): new rows of a pile whose `Пишет в` overlaps the `Пишет в` of a
node of the same pile accepted in the same 7-day window.

**Alternatives weighed (F17).** (b) A stop-time check in `dod_gate.py` (P35): a critic dispatch carries a new header
line `judged-owns: <paths>` (`dispatch_new.py` prints it, `dispatch_manifest.py` requires it, informed pass
`judged-owns: none -- <why>`), and the critic's stop is refused while its verdict marks `чужой-код` a path inside
`judged-owns`. Cheaper for the Lead (no argument on every merge; the critic fixes its own label in context), earlier,
but: it does not bind the verdict to the node's acceptance (a node can still be accepted on no verdict silently), it
widens three mechanism files (`dispatch_manifest.py`, `dispatch_new.py`, `dod_gate.py`) against two
(`piles.py`, `wave.py`), and every critic dispatch pays one more header line. (c) Discipline + a calibration item only —
not on the path. No point cheaper than (a) reaches the same guarantee ("no node is accepted while its own-code remark
is labelled deferrable, unless someone says why in the record"); recommended (a), Lead's fork F17.

### 2.4 The flow brake (B2): judged when a node row is ADDED, shown at SessionStart and in `status`

forge/7 never closes (P28) and accepts nodes through the node branch of `status` (P29), so no close-time brake can see
it. The brake moves to the moment a row is ADDED — the commit-msg `piles.py check` road — and the counter is printed
where the Lead looks every session.

- **Counter (stream A3), new `piles.flow(root, window_days=7, slug=None, n=None) -> Flow | None`.** ONE
  `git log -p --since=<window> -- plans/piles/<slug>/batch-*.md` pass (per pile when a slug is given). "Opened" = the
  first commit in the window where a node id appears in ANY batch file of the pile (keyed by `(slug, id)`: a move
  between batch files of one pile is not an open); "closed" = the first commit where its status word becomes `принято`
  or `отклонено`; attribution to a batch = the file the row stands in at the end of the window. `None` (git cannot run,
  timeout) → the caller prints `не измерено (<why>)`, never `0` (FR-41).
- **Gate (stream A3), in (д), new `_flow_reds(ctx, doors)`.** For every batch file not «закрыта» that gains a NEW node
  row in this commit (new = its id absent from every batch file of the pile at the base): when `opened > closed` for
  that batch over the window INCLUDING this commit, the commit is red unless its message carries
  `приток: <slug>/<N> -- <why>` (parsed like `piles-skip:`; one line per batch; the reason non-empty). Which rows count:
  fork **F13** (recommended (a): every added row, whatever its `Откуда`). Refusal text: `<path>: this commit adds node
  row(s) <ids> to <slug>/<N>, which over the last 7 days opened <a> and closed <c> (the net would be +<x>) -- a batch
  that grows must say why (PROJECT.md «Командная работа» п. 9). Expected: fix the remark in its own node's round instead
  of adding a row, or add the line "приток: <slug>/<N> -- <why, per added row>" to the commit message`. A window git
  cannot read → a NOT CHECKED note `поток не измерен (<why>); this commit is not blocked by the flow rule` (the (в)
  precedent; FR-59: named, never a silent pass); calibration counts these notes.
- **Shown.** `piles.py summary`: `поток узлов за 7 дней: открыто N / закрыто K; итог ±X` + one line per growing batch;
  `piles.py status` prints after its write (or its no-op) `поток пачки <slug>/<N> за 7 дней: открыто a / закрыто b`;
  `tools/session_context.py` (SessionStart) prints ONE line `поток узлов за 7 дней: открыто N / закрыто K (итог ±X);
  растут: <up to 3 batches with their net>` through `piles.flow`; any exception or a git call over 5 s →
  `поток узлов: не измерено (<why>)`; SessionStart never fails on it.
- `--all` (tests, calibration) and `close` print the counter and judge nothing by it (the history is written); CI
  `check --base` judges the pushed range with the range's commit messages (`range_messages`, the existing door reader).
- `piles-skip: д -- <reason>` skips the flow gate with the rest of (д); `приток:` is its own narrower door.

**Batch 7 itself** (fork **F20**, Lead; recommended): forge/7 is closed as a CONTAINER and its 38 open rows move to
batches with a real scope (one or more `batch-<N>-<slug>.md` of pile `forge`, `ожидает`, card rows added). What `close`
needs for that, in order: (1) the open rows are cut from forge/7 into the new files (an untaken file is not frozen;
keyed by `(slug, id)` the move is not an "open"; the card «Строки» cell of forge/7 loses the B-ids of moved nodes, the
new card rows gain them); (2) `piles.py take forge 7 --who <Lead>` (its remaining nodes are all `принято`/`отклонено`, so
`writers_of` is empty and (б) cannot refuse); (3) `piles.py status forge 7 --set принято` (it refuses while any node is
open — none is); (4) `piles.py close forge 7 --hash <the merge commit of its last accepted node>` — the «Остатки» and
«Живые доказательства» gates must pass (legacy items by the old form, §6 E20). Precedent: forge/3 and forge/6 were
closed with `взял: —` (P28). The same applies to any other incoming batch that is worked untaken (Lead lists them at
stream G). Whether a node may be accepted in an untaken batch at all (t-920 B2 option (b)) is F20's alternative.

### 2.5 Expected effect, told to the owner (N9)

If every rule holds: rows 1 and 7 stop for sure — 51 + 14 = 65 of 206 = **31.6 %** of the leftover stream; with F16 as
recommended, row 4b stops too → 92 = **44.7 %**; rows 3 and 5 stop only in their on-topic / not-for-tokens part, and
t-906 did not split them (not in the carriers read: t-920 key 2, journal line 2244) → the upper bound is
65 + 31 + 27 + 24 = 147 = **71.4 %**. What stays legitimately: other code 20, calibration/process 27, new ideas 8, live
proofs 4 → at least 59 = **28.6 %**. The flow line makes the real number visible from the first week (§2.4).

---

## 3. Registries into nodes (one stream each)

Common rules: a migrated node has `Откуда: миграция`, a `Тип`, an `Исполнитель`, and lands in the UNTAKEN batch of its
pile (none → `batch-<N+1>-<slug>.md` `ожидает` + card row, PROJECT п. 2). A stale row is not migrated: its verdict and
evidence go in the commit message and the pile's untaken batch «Ход». "Stale" is judged by the Lead from a scout's
evidence (P27): a fixing commit, a node already `принято`, or the named file/function gone (with a positive control).

| stream | registry | before | rule for each item | after |
|---|---|---|---|---|
| M1 | findings in no batch | **152 (69 undated)** (P12) | done → finding file deleted (git keeps it; F10); duplicate of a live node → named in that node's «Что» (untaken) or «Ход» (taken); live → node row `Откуда: находка <file>`; unsure → `Тип: неразобран`, `Исполнитель: scout → Lead` | 0 orphans; then H drops `FINDINGS_FROM` |
| M2 | `docs/tasks/lead-queue-fable.md` | 12 items + 2 lines; 10 done, 2 open (P14) | the 2 open → no new node (FG7-51, FG7-49 hold them, P15); a «Ход» line in their batch names the queue items they absorb | per fork **F7** (Lead): the file and the architect-tier readers (P16) |
| M3 | ~~`design/factory-rules-debt.md`~~ | — | REMOVED: the owner's word «давай починим сейчас» — the rows are FIXED by `docs/tasks/specs/20261117-rules-debt-fix-spec.md` (P34: not on disk yet). Tell that stream: the open count is **44 by the file's own rows**, not the header's "25" (P17, N8). What happens to the file once empty: fork **F8** | — |
| M4 | plans of big ideas with no pile | 6 (t-895; P25) | live → a batch with `план:` in the topical pile (F11); done/abandoned → one header line `архив: <дата>, <причина>` | 0 plans without a batch or an `архив:` line |
| M5 | DAG files under `docs/tasks/` | 3 (P24) | `factory-fixes.md` → `архив:`; `test-diet.md` → its open nodes become rows of `package-ci` batch 4, each checked against that batch's rows first; `архив:` + pointer; `onboarding-streams-…` → a WAVE VIEW header line (it holds no node) | 0 node tables outside `plans/piles/` |
| M6 | `plans/BACKLOG.md` | **296 open ids** (P26) | unchanged archive: (а), (г), `close --id` keep working | unchanged |

---

## 4. `tools/piles.py` after the change

Readers of `piles.py` (Grep `import piles|from piles|piles\.py|piles_split|backlog_tree` over `tools/*.py`, `.githooks/*`,
`.claude/settings.json`, `.github/**` → 42 files, 26 tests — round 1): `.githooks/commit-msg:40` (`check --msg-file`,
re-read now), `.github/workflows/forge-check.yml:84` (`check --base`), `.claude/settings.json:156-157, 175-176`,
`tools/wave.py:254` (`status … --set принято`), `tools/backlog_tree.py`, `tools/compact_snapshot.py:350-353`
(`load_tree`, `leftovers_unowned`), `tools/forge_metrics.py`, `tools/collect_intake.py`, `tools/piles_split.py`,
`tools/canon_clock.py:28` (`LEFTOVER_EMPTY_WORDS`), `tools/ci_read_common.py:10` (`printable`), `tools/md_table.py`,
`tools/conftest.py`, `tools/hook_liveness_probe.py:942-961, 1425` (probe 14), `tools/worktree_sweep.py:7`,
`tools/mechanism_gate.py:254`; NEW readers after this spec: `tools/session_context.py` (`flow`, A3),
`tools/critic_verdict_check.py` (`node_vocab`, C).

| piece | verdict | what changes (stream) | readers / effect |
|---|---|---|---|
| `summary` | changes | + flow lines, + `без типа: T` (A3) | calibration check 33 reads it |
| (а) placement | unchanged | — | commit-msg, forge-check |
| (б) overlap | unchanged | — | commit-msg, forge-check |
| (в) frozen | changes (A1) | `_frozen_lines` drops the cells under a header named `Тип` or `Откуда` (stripped, case-folded) from the header row and from every row of a table in «Узлы» before joining; `status_col` is computed on the reduced cells. A taken batch may thus gain the two columns (and edit their cells) with no door; every other cell is still compared | commit-msg, forge-check; `test_piles_frozen.py` rows |
| (г) backlog | unchanged | — | — |
| (д) form | changes | A1: `_new_node_rows`, `_node_origin_problem`, `_plan_problem` (the new-row checks of §1.1, B4(b) identity); A2: the `остаток` carriers (§2.3 part 3), `_item_why` without the `перенос:` form for NEW items, `узел:` back-reference + `подтвердил:` presence (F5); A3: `_flow_reds` | commit-msg, forge-check, compact snapshot (`leftovers_unowned` keeps its signature) |
| (е) findings | changes after M1 (H) | when the baseline is 0: `FINDINGS_FROM` and the WARN branch removed — one rule | commit-msg, forge-check |
| `take` | unchanged | — | integrator |
| `close <slug> <N>` | changes (A2, A3) | `узел:` accepted with the back-reference and `подтвердил:`; legacy `перенос:` by the old form, new ones refused (§6 E20); prints the batch's flow | integrator |
| `close --id` | unchanged | `debt_warnings` unchanged (round 1's widening to node ids REMOVED with M3) | — |
| `status` | changes (A2, A3) | node `--set принято`: `--verdict`/`--no-verdict`/`--owner-word` (§2.3); prints the batch's flow | `wave.py` (changes in A2) |
| `board`, `release` | unchanged (refused aliases) | — | `.claude/settings.json:157, 176` stale allow lines → H (Lead) |
| new `node_vocab()` | added (A1) | ONE reader of `tools/piles-vocab.json` (`node_types`, `node_origins`, `leftover_criteria`, `remark_dispositions`, `confirmers`, `intake_default`, `carry_retired`); absent/unreadable/invalid → `CannotRun` naming the path and the broken key (FR-59: never "every type valid") | `piles.py`, `collect_intake.py` (B), `critic_verdict_check.py` (C) |
| new `flow()` | added (A3) | §2.4 | `summary`, `status`, `close`, `_flow_reds`, `session_context.py` |
| new `legacy_carries()` | added (A2) | §6 E20 | `check_leftovers`, `check_proofs` |

`tools/piles-vocab.json` joins `MECHANISM_PREFIXES` (data that decides a gate, like `tools/worktree-junk.json`) — H, Lead.

Checks this spec adds or alters — owner served and class (AR-29 / P27; forge checks, outside the package census,
classed in its words):

| check | owner it serves | class |
|---|---|---|
| (в) masks the `Тип`/`Откуда` cells | data (code) | shape |
| (д) `Тип` ∈ list, `Откуда` form, `план:` path exists, finding of `находка` exists | data (code) | shape / presence / xref |
| (д) `остаток` parent exists; `чужой-код` verdict ref resolves to a `чужой-код` remark whose path the row writes | data (code) | xref |
| (д)/close `узел:` item carries `подтвердил: <владелец \| Lead пачки>, <дата>` (F5) | intent (owner) or judgment (batch Lead) — presence of the signature only | presence |
| (д) flow: `приток:` line present when a growing batch gains rows | judgment (the Lead's explanation; content accepted at calibration) | presence |
| `critic_verdict_check` `remarks` shape, disposition ∈ list, ids joined to `blockers`/`fixes` | data (code); the label itself is the critic's judgment, accepted by the Lead | shape / xref |
| `status --set принято`: no `чужой-код` remark on a path inside `Пишет в` | data (code): a path join | xref |
| `--no-verdict` / `--owner-word` / `приток:` reasons | judgment (Lead) / intent (owner) — presence only | presence |
| close: legacy `перенос:` by the cutover commit; new `перенос:` refused | data (code) | shape (history join) |
| §8 stamp hash vs the source section hash; `see:` pointer resolves; census ratchet | data (code); whether the carried block still MEANS the main rule is the role's (the re-stamper reads it), accepted by the Lead | xref (hash) / presence / count |
| "is the remark truly another topic" (path outside) | judgment (critic, accepted by Lead) | not code |
| scope cut quotes the owner's token word | judgment (critic-on-plan) / intent (owner) | not code |

---

## 5. Rule texts that change (exact text; ONE home + pointers — B5, the first instance of §8)

**The one home of the leftover rule** is PROJECT.md «Командная работа» п. 9, the paragraph headed «**Остатков нет по
правилу**» (it replaces «Остатков в идеале нет вовсе», fragment 9d, which boot-by-topic keeps in PROJECT.md — P37; fork
F12 on its gate criterion). Every other carrier POINTS to it with the literal text `PROJECT.md «Командная работа» п. 9`
and restates nothing; §5.14 holds it so now, and §8 replaces §5.14's hand-kept rows by the class mechanism once K lands.

Order with the parallel specs (N3, N10): boot-by-topic and architect-tier are accepted earlier and land first; every
edit below is anchored by its quoted OLD text and applied wherever that text stands at landing (PROJECT.md or
`docs/TEAMWORK.md` § with the same number, fragment by fragment: 5.1 edits fragment 2c (TEAMWORK § 2 when it moved);
5.3 edits 9d (PROJECT); F4's form change and F5's confirmers edit 9a (TEAMWORK § 9) and 9c (PROJECT) together). AGENTS.md
is regenerated (`python tools/agents_md.py`). The test anchors of P22 stay byte-identical.

**5.1 PROJECT.md «Командная работа» п. 2 (fragment 2c)** — from «**Находка сразу попадает в пачку** (D-0044)» to «…и
находка ложится туда.» → replace with:

> **Всё в кучках** (слово владельца 17.11.2026): единственный реестр работы — узлы пачек. Находка — улика и описание, не
> работа: тем же ходом, что файл в `findings/`, она получает УЗЕЛ (строку «Узлы» с `Тип` и `Откуда: находка <файл>`) в
> НЕвзятой пачке своей кучки; нет такой — пишущий открывает `batch-<N+1>-<slug>.md` со статусом «ожидает» и строкой в
> таблице «Пачки» карточки. Тип узла — слово из `tools/piles-vocab.json`; большая идея — своя пачка с парой
> `план: <путь>` в шапке. Красный CI — не находка и не узел (п. 9).

(Fragment 2d «Содержание», the frozen batch, «Находка называет класс фабрики», the `grep` by DECISIONS — unchanged.)

**5.2 PROJECT.md «Командная работа» п. 4** → append after «…у находки до этого `id: —`.»:

> Очереди вне кучек (очередь Lead, графы задач в `docs/tasks/`, планы идей без пачки) не ведутся: их работа — узлы
> (спека `docs/tasks/specs/20261117-everything-in-piles-spec.md`).

**5.3 PROJECT.md «Командная работа» п. 9 (fragment 9d) — THE HOME** — from «**Остатков в идеале нет вовсе**» to «…строкой
с исполнителем.» → replace with:

> **Остатков нет по правилу** (слово владельца 17.11.2026, по происхождению):
> — замечание критика о коде темы узла (то, что в его «Пишет в»), минорное тоже, чинится в фикс-раунде того же узла: не
> узел и не строка «Остатков»; в вердикте у такого замечания `disposition: fix`;
> — замечание критика о чужом коде (вне темы узла) можно оставить узлом: в вердикте `disposition: чужой-код` и путь, у
> узла `Откуда: остаток <узел> · чужой-код · <вердикт>#<id замечания>`; «чужой код» внутри «Пишет в» узла
> `piles.py status --set принято` не примет;
> — новое слово владельца по теме идущей работы делается в этой работе; слово на другую тему можно завести узлом
> `Откуда: владелец <дд.мм.гггг>`;
> — красный CI чинится на месте и узлом не записывается;
> — урезать работу спекой можно только словом владельца «для экономии токенов», записанным в спеке с датой; урезанное —
> узел `Тип: доделка`, `Откуда: остаток <узел> · экономия-токенов · <путь спеки>`; иначе — сделать сразу или спросить
> владельца;
> — живое доказательство уходит в `live-runs` узлом `Откуда: остаток <узел> · живой-прогон` (см. ниже).
> Строка «Остатков» для такого узла — `узел: <id> | подтвердил: <владелец или Lead пачки>, <дд.мм.гггг>` (слово владельца
> 17.11.2026). Размер — не основание: большой фикс — второй раунд того же узла. Пачка, которая за 7 дней открыла больше
> узлов, чем закрыла, принимает новую строку только со строкой `приток: <кучка>/<N> -- <почему>` в сообщении коммита;
> поток печатают SessionStart, `piles.py summary` и `status`.

(Under F14 = recommended, the first dash reads «замечание критика или найденный билдером аналог о коде темы узла …»;
under F16 = recommended, the CI dash reads «красный CI и дефект после приёмки чинятся на месте …». 9a/9b/9e/9f stay;
9c «перенос подтверждает **человек**, не агент сам» gains: «узел-остаток подтверждает владелец или Lead пачки (слово
владельца 17.11.2026)»; under F4 the `перенос:` wording of 9a/9f becomes `узел: <id>` with the back-reference — text in
stream D.)

**5.4 PROJECT.md «Командная работа» п. 11** → append after «…исполнителю не нужно искать по кучкам.»:

> У узла названы `Тип` и `Откуда`; узел, рождённый работой другого узла, называет его и основание.

**5.5 PROJECT.md «Как принимается изменение пакета» п. 2** — the clause «красный пайплайн на `main` (все причины разом —
`python -B tools/ci_read.py why`) — находка в `findings/` своей кучки и починка до следующего пуша» → «красный пайплайн на
`main` (все причины разом — `python -B tools/ci_read.py why`) — починка на месте до следующего пуша, без находки и без
узла (слово владельца 17.11.2026; PROJECT.md «Командная работа» п. 9)» (+ the record per F15).

**5.6 PROJECT.md «Как принимается изменение пакета» п. 4, last sentence** «Нарушение правила, которое не чинится сейчас, —
строка в `design/factory-rules-debt.md`.» → depends on F8 (OWNER): under F8 (a) «— узел `Тип: долг` в кучке, чья зона»;
under F8 (b) unchanged until the owner's word. (Round 1's §5.5 with `node:` pointers is REMOVED.)

**5.7 CLAUDE.md rule 4a, first sentence** «…is tracked as a markdown DAG — a pile's batch file or a file under docs/tasks/:
nodes/statuses/tiers as the carrier;» → «…is tracked as nodes of a pile's batch file (the only registry of work, the
owner's word 17.11.2026): nodes/statuses/tiers as the carrier; a file under docs/tasks/ may group pile nodes into waves
but holds no node of its own;»

**5.8 CLAUDE.md rule 9, the clause** «fix now, or EXPLICITLY put the remainder in the queue/log» → «fix now, or EXPLICITLY
open a node for the remainder where PROJECT.md «Командная работа» п. 9 allows one». (The K-OWN key of rule 9 untouched.)

**5.9 CLAUDE.md rule 12 Cost gates, the clause** «a fix round runs in a FRESH worker carrying only the diff and the
verdict» → «a fix round runs in a FRESH worker carrying only the diff and the verdict, its `owns` widened to every path
the verdict's `fix` remarks name (what may stay out: PROJECT.md «Командная работа» п. 9)». (The COST anchor untouched.)

**5.10 docs/tasks/critic-diff-brief.md** (pointers; the K-OWN keys of q7 and q12(d) stay byte-identical):
- q4, from «An analog outside the node's `owns` that this round does not fix» to «(F6-30).» → «Every remark and analog
  gets one line in the verdict's `remarks` (`fix`, or `чужой-код` with its `path`); which remark may stay out of this
  round is decided by PROJECT.md «Командная работа» п. 9, not here.»
- q7, «Each is a finding with a severity — blocks / fix before merge / queue — never a style pass and never "I don't
  like it".» → «Each is a finding with a severity — blocks / fix in this round — never a style pass and never "I don't
  like it"; what may stay out of the round: PROJECT.md «Командная работа» п. 9.»
- q12(d), «a fix in this round or a node with an id and an owner;» → «a fix in this round, or a `чужой-код` remark where
  PROJECT.md «Командная работа» п. 9 allows one;» (the next clause «a line for the coordinator to tell someone is itself
  a finding» unchanged).
- C-key (scope cut, t-920 B3.5), appended to q12 as (e): «(e) On a plan gate: a non-goal that defers work of the spec's
  own topic is legal only with the owner's word quoted with its carrier and date; otherwise it is a finding (PROJECT.md
  «Командная работа» п. 9).»

**5.11 .claude/agents/critic.md** (Lead places; sweep of the same artifact: rules 5, 17, 19):
- rule 5 «Axes of the defect left uncovered and not queued = a NEEDS-WORK finding.» → «Axes of the defect left uncovered
  and neither fixed nor carried where PROJECT.md «Командная работа» п. 9 allows = a NEEDS-WORK finding.»
- rule 17, after «trail (read + reruns);» insert «remarks (one item per blocker and fix: `id`, `disposition` `fix` or
  `чужой-код`, `path` for `чужой-код`);».
- rule 19, «leaves your verdict as a fix of this round or as a proposed node with its owner,» → «leaves your verdict as
  a fix of this round or as a `чужой-код` remark where PROJECT.md «Командная работа» п. 9 allows one,».

**5.12 plans/builder-rules.md п. 1**, the clause «нужное в чужом файле — не правь, опиши в «Needed from integration» (файл,
точный текст/код, зачем)» → «нужное в чужом файле — не правь, опиши в «Needed from integration» (файл, точный текст/код,
зачем): это применяет интегратор или Lead В ТОМ ЖЕ РАУНДЕ; что может остаться вне раунда — PROJECT.md «Командная работа»
п. 9».
**.claude/agents/designer.md** (Lead places): rule 2, append «A non-goal that defers work of the spec's own topic carries
the owner's word quoted with its carrier and date, or is a fork (PROJECT.md «Командная работа» п. 9).»
**PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md** (Lead places, N2): check 33 line 1026 — the «Живые доказательства» form gains
`узел: live-runs/<N>/<id>`, `перенос:` only for items before the cutover; check 33 gains items: (i) the flow line of
`summary`, a second week with a positive net is a finding; (ii) count of `verdict: none`, `owner-word:`, `приток:` lines
and flow `не измерено` notes in the window; (iii) new rows whose `Пишет в` overlaps a node of the same pile accepted in the
same window (the B1 escape detector); (iv) a semantic read of the pointer carriers against the home (the cross-language
blind spot of §5.14 / §8.6). Check 39 line 1095 — «without `сделано:` / `узел:` / `перенос:`» → «without `сделано:` /
`узел:` with `подтвердил: <владелец | Lead пачки>, <дата>` (a `перенос:` only for an item before the cutover)».

**5.13 plans/piles/_template/batch.md** — the node table gets the two columns; the «Остатки» comment loses `перенос:`
and gains `узел: <id> | подтвердил: <владелец | Lead пачки>, <дата> — строка узла: Откуда: остаток <этот узел> ·
<основание>`; the header comment gains `план: <путь>`.

**5.14 The instance check for the leftover rule (B5)** — `tools/tests/test_role_carriers_one_owner.py`, stream D (it lands
before K and is subsumed by K's data rows, §8.5):
- OWNER_KEYS + `("teamwork:leftovers", "PROJECT.md", "чинится в фикс-раунде того же узла: не узел и не строка «Остатков»")`
  — a RUSSIAN copy in any other scanned file (builder-rules is Russian) turns red.
- POINTERS + five rows, each `(carrier, "PROJECT.md «Командная работа» п. 9", "PROJECT.md", "**Остатков нет по правилу**")`
  for carriers `docs/tasks/critic-diff-brief.md`, `.claude/agents/critic.md`, `CLAUDE.md`, `plans/builder-rules.md`,
  `.claude/agents/designer.md`.
- new parametrised `test_retired_leftover_text_is_gone` over RETIRED = the old divergent texts, each must occur in NO
  scanned file: «blocks / fix before merge / queue», «a fix in this round or a node with an id and an owner», «or as a
  proposed node with its owner», «put the remainder in the queue/log», «Остатков в идеале нет вовсе», plus its negative
  control (a retired phrase pasted into a copy → named), as the file's existing controls do.
- Error direction (asked): K-OWN errs to a FALSE PASS across languages (an English restatement in the brief, critic.md
  or CLAUDE.md does not match the Russian key) — the named blind spot, covered by calibration item (iv) and critic
  question 6; K-PTR errs SAFE (the home's anchor renamed or moved → red, which forces the pointer rows to follow, e.g.
  if boot-by-topic moves 9d to TEAMWORK); RETIRED errs to a false pass on NEW wording of the old rule (same detector).
  No row can turn red on a correct tree except a moved anchor.

---

## 6. Edges (behaviour + the invariant it protects)

| # | edge | behaviour | invariant |
|---|---|---|---|
| E1 | a taken batch during migration (10 «в работе», P1) | not migrated by default (F9); the (в) mask (§4) makes adding the columns legal with no door if the Lead migrates one | (в) still refuses every other change to frozen text |
| E2 | another developer's piles and branches | migration touches only batches with `взял: —` on `origin/main`; a pile whose untaken batch is written on another branch is skipped and listed; "the owner decided" in another branch's text is not leaned on (PROJECT п. 6) | no session writes another session's uncommitted paths |
| E3 | a finding naming two piles | one home: the pile of the node's `Пишет в`; the other pile gets a sibling node `Откуда: находка <slug>/findings/<file>` only when it has its own work | an id lives in one pile ((а) red stays) |
| E4 | a node with no owner pile | `forge` when its files are outside the package, else the nearest zone by the Lead's judgment; never a new pile without the owner (F11) | no work without a home |
| E5 | closed batches (67) | never rewritten | history is append-only |
| E6 | status words with text after the word (P7) | unchanged; the one reader takes the first word | one vocabulary, one reader |
| E7 | the widget (`backlog_tree.py` → `register.tsx`) | reads statuses through `piles`; JSON `{piles, counts}` unchanged; optional node key `type` | the pane never disagrees with `piles` on open/closed |
| E8 | TEMPORAL: `tools/piles-vocab.json` absent before A1 | before: no reader exists; after: absent/unreadable/a key missing → `CannotRun` naming the path and key; `collect_intake` prints the refusal and writes nothing | an unknown vocabulary never validates a type (FR-59) |
| E9 | TEMPORAL / B4(b): rows when the columns land | row identity = node id + the cells of every column except `Тип`, `Откуда`, `Статус` (whitespace-squashed), matched as a MULTISET against every batch file of the same pile at the base. Found → OLD: `—`/empty/absent `Тип` and `Откуда` legal; not found → NEW (a new id, or an old id whose «Что»/«Пишет в»/… changed) → must carry valid `Тип` and `Откуда`. Adding the two columns to a table changes no row's identity. A table without the columns gaining a NEW row → red (text below). An unreadable base → every row NEW + one WARN note (the existing leftover precedent; FR-59) | old history never turns red by a new rule; a new or rewritten row is never typeless |
| E10 | POSITIONAL: the `узел:` back-reference in `_item_why` and `check_leftovers` | after `_node_problem` (exists, open batch, executor) and before the pass; a node failing `_node_problem` is reported by it first; the `подтвердил:` presence (F5) after the back-reference | a closed or executor-less node is still refused; the new checks only narrow |
| E11 | a leftover `узел:` naming a node of THIS batch | refused: "a node of this batch is this batch's work — fix it or close the node" | a batch never closes by pointing at itself |
| E12 | `Откуда: остаток X` with X missing | red naming X; X in a closed batch is allowed (the parent may close first) | a born node names a real parent |
| E13 | the counter: rows moved across piles / deleted by hand / status moved back | across piles: an open in the target, `ушло` in the source (never "closed"); deleted without a status: `исчезло: N`, never closed; a status moved back by hand: the later forward move counts once | the counter never shows a shrink that did not happen |
| E14 | a verdict with no `remarks`, an unknown disposition, a `чужой-код` with no path, an id named twice | `check_text` fails (texts in §2.3); at `status --verdict` → refused with the door `--no-verdict` | a label always has its type and path; absence never fakes a fix |
| E15 | input from outside: the vocabulary file and `tools/rule_sources.json` a person edits; the verdict file a critic writes; the `приток:`/`--no-verdict`/`--owner-word`/`подтвердил:`/census-raise text a person types | adversarial rows: empty list, duplicate word, a word with `\|`, a non-string, BOM, a 1000-word list, a missing key; a verdict 10 MB, nested 100 deep, not UTF-8, a remark path of 300 / 301 characters, `..`, a line break; a reason of 120 / 121 characters, with `\|`, a backtick, a line break, empty → each a `CannotRun` or a named refusal, never a silent accept | FR-1/FR-2: every refusal names what it expected and the door |
| E16 | the flow window git cannot read (no git, shallow CI clone, timeout) | NOT CHECKED note naming why; the commit is not blocked by the flow rule; calibration counts the notes (§5.12 (ii)) | an unknown never passes as `0` and is never silent (FR-41, FR-59 — the declared default, as (в)) |
| E17 | a topic critic (one verdict for several nodes, R13-g) | the same `--verdict` path at each node's acceptance; each node is judged against its own `Пишет в` | one verdict, one judgment per node |
| E18 | conflicting requirements: "fix now" (§2.2 row 1) vs PROJECT п. 3 (two batches «в работе» on one file) | per F18 recommended: not a node — the fix waits as the same node's second round after the other batch merges (or is done now under D-0048 function lists / an `очередь:` line); the node stays open | two writers never meet in one file; an own-code remark never leaves its node |
| E19 | conflicting requirements: M2 vs the accepted architect-tier F8 (a) | fork F7 (Lead) lists that spec's readers; both wait for the Lead's answer | one road for "work below-Lead cannot do" |
| E20 | TEMPORAL / B4(a): `перенос:` items written before the cutover (e.g. onboarding-hooks/5 three proof rows, onboarding-forge/2 critic carries) | cutover = the FIRST commit whose `tools/piles-vocab.json` holds the key `carry_retired` (A2 adds it): `git log --reverse --format=%H -S '"carry_retired"' -- tools/piles-vocab.json`, first line — derived from git, no date typed by hand. `legacy_carries(root, rel)` = the multiset of stripped «Остатки» items and proof-row cells of that batch file at `<cutover>^`. At close: a `перенос:` item in that multiset is judged by the OLD rule (`leftover_problem` as today, a real `подтвердил:`); any other `перенос:` is refused (text below); a legacy `узел:` item (no back-reference, no `подтвердил:`, written before) passes on `_node_problem` alone — better than today's P11. No cutover commit found (the world before A2 merges) → every item by the old rule. Git fails → `CannotRun` (close writes nothing). A batch file absent at `<cutover>^` (newer, or renamed) → no legacy items (a renamed old file: false red, door below). Write time (д) needs no cutover: an old item is not judged (multiset vs base), a NEW `перенос:` is refused by `_item_why`. `leftovers_unowned` (summary, compact snapshot) keeps judging `перенос:` by the old FORM (advisory count; signature unchanged) | an item legal when written stays closable; a carry written after the rule never closes a batch |
| E21 | `Откуда: находка <file>`: the file must exist | checked when the row is NEW; the file deleted or renamed later is not re-judged (the origin is history); M1 deleting a done finding never reds an old row | a new row names real evidence; history is not re-judged |
| E22 | `план:` path renamed or deleted later | checked when the header line is new or changed; `summary` prints `план не найден: <slug>/<N> <path>` | a new header names a real plan; a later move is shown, not refused |
| E23 | `владелец <дд.мм>` without a year | refused: the form is `владелец <дд.мм.гггг>` | dates survive the year boundary |
| E24 | a near-miss separator in `Откуда` (` - `, `.`, `•`, `·` without spaces) | red naming the expected ` · ` (U+00B7 between spaces) and the character found | the form is one form |
| E25 | the A1 → B window (`collect_intake` still writes no `Тип`/`Откуда` while A1's (д) is live) | small choice closed: B is built on A1's branch and merged right after A1 in the same wave; in between, (д) refuses an intake row with the door "write the `Тип` and `Откуда` cells by hand" | a new row is never typeless, even for one commit |
| E26 | `intake_default` (N6) | `collect_intake` writes `Тип: неразобран` (the declared unknown, F1) and `Откуда: находка <file>`; `summary` counts `неразобран` rows for the Lead | code never picks a work type |
| E27 | a red CI after M1 (the (е) single rule) | no finding is born for it (§5.5), so (е) has nothing to judge; a red-CI finding written anyway is an orphan → red, door: delete it, the fix commit carries the record (F15) | one road for a red CI; no node for it |
| E28 | `--owner-word` / `--no-verdict` on a non-`принято` call or a batch-level call | refused like `--hash` today | the passes exist only where the gate is |
| E29 | F5: a NEW `узел:` item without `подтвердил:`, with a placeholder (`—`, `tbd`, …), or with a name that is neither `владелец` nor `Lead пачки` | refused (text below); the names are data (`confirmers` in the vocab, the owner's 17.11 word); the gate checks presence and the word, never who typed it (the existing L5 limit, said in the refusal) | a node leftover always carries its confirmation; an agent's silence never confirms |
| E30-E36 | §8 edges | see §8.3 | — |

Refusal texts of the new reds (N6; each: what is wrong, what is expected, a door the refused party can use):

| red | text |
|---|---|
| (д) table without the columns | `<path>: node row <id> is new, but the node table has no «Тип»/«Откуда» columns -- expected the header of plans/piles/_template/batch.md; add the two columns (old rows may carry «—»)` |
| (д) `Тип` | `<path>: node row <id>: «Тип» "<value>" is not a word of node_types in tools/piles-vocab.json (<the words>) -- write one of them; «неразобран» when the type is not yet judged` |
| (д) `Откуда` form | `<path>: node row <id>: «Откуда» "<value>" is none of: план, находка <file>, владелец <дд.мм.гггг>, миграция, остаток <node> · <key>[ · <carrier>] -- <the specific miss: unknown head / missing year / separator "<char>" where " · " (U+00B7) is expected>` |
| (д) `находка` file | `<path>: node row <id>: «Откуда: находка <file>» names no file in plans/piles/<slug>/findings/ -- name an existing finding, or write the finding first` |
| (д) `остаток` parent / key / carrier | `<path>: node row <id>: «Откуда: остаток …» <the miss: parent <X> is no node row of <where> / key "<k>" is not in leftover_criteria (<keys>) / «чужой-код» needs " · <verdict path>#<remark id>" / remark <rid> of <verdict> is "<disposition>", not «чужой-код» / the row's «Пишет в» does not touch the remark's path <p> / «экономия-токенов» needs " · <spec path>" of an existing file / «живой-прогон» rows live in pile live-runs> -- PROJECT.md «Командная работа» п. 9 says when a remark may be a node` |
| (д) `план:` | `<path>: the header «план: <p>» names no file in the working tree -- write the plan first, or correct the path` |
| (д)/close `узел:` without `подтвердил:` | `<path>: «Остатки» line <n>: «узел: <id>» has no confirmation -- expected «подтвердил: <владелец \| Lead пачки>, <дд.мм.гггг>» (the owner's word 17.11.2026; the gate cannot know who typed it — the rule says the owner or the batch's Lead). Door: have the owner or the batch Lead confirm it, or fix the item now and write «сделано:»` |
| (д) flow | §2.4 |
| `status` verdict | §2.3 |
| wave without verdict | §2.3 |
| close: new `перенос:` | `<path>: «Остатки» line <n>: «перенос:» is retired since <cutover7> (всё в кучках, 17.11.2026) -- an item written after it leaves the batch as «узел: <id>» whose row says «Откуда: остаток <a node of this batch> · <key>», or is finished with «сделано:». Door: open the node (PROJECT.md «Командная работа» п. 9) and write «узел: <id>», or finish the item; then run close again. Nothing was written` |
| close: `узел:` without back-reference | `<path>: «Остатки» line <n>: «узел: <id>» names a node whose «Откуда» is "<value>", not «остаток <a node of this batch> · <key>» -- write the back-reference in that row (PROJECT.md «Командная работа» п. 9), or finish the item with «сделано:». Nothing was written` |
| close: git cannot tell old from new | `cannot tell a carry-over written before the cutover from a new one (git: <why>) -- run close inside the repository; nothing was written` |
| `critic_verdict_check` | §2.3 (ASCII) |
| §8 stamps / pointers / census | §8.3 |

---

## 7. Phases, streams (ordered by volume), witnesses, readers

### 7.1 Phases

- **Phase 0 (owner/Lead)**: the OWNER forks still open (F1, F8, F14, F16, F18, F19) and the Lead forks; critic re-pass on
  B1/B2 and on §8 (a new mechanism of the owner's word W3 — PROJECT «Новая идея» п. 6), the rest checked by the Lead.
- **Phase 1**: A1 (foundation; every other code stream of this spec imports `node_vocab`). D's builder may start in
  parallel (disjoint files); D merges after A2 and A3 (its home text describes their gates): `очередь:` line A3 → D.
  K (§8) is independent of `piles.py` and may start in phase 1; it merges after D (it absorbs D's rows of the carrier
  test).
- **Phase 2, by volume of the leftover stream they stop**: C → A2 (critic, 34.5 %, §2.1); D (owner's word 15.0 %, red CI
  13.1 %, scope cut 11.7 %, builder-noticed 6.8 % — rule text, pointers, the instance test); A3 (the brake for every
  origin and for the self-label escape); B (readers); K (the class: every service file, L15).
- **Phase 3 (migration)**: E-k (M1 per pile group), G (M2, M4, M5, forge/7 as a container per F20, forge's own orphans),
  K2 (stamping/pointing the existing service files down the census, §8.5).
- **Phase 4 (close-out)**: H.

The nodes live in one big-idea batch of pile `forge` with `план:` this spec (§1.2) — the Lead opens it.

### 7.2 Streams (owns disjoint; `piles.py` shared by A1 → A2 → A3 → H strictly in sequence with disjoint function lists, D-0048; the carrier test shared by D → K in sequence)

| order | stream | node (file · function · behaviour) | owns (absolute) | witness (DoD command) | tier / commit |
|---|---|---|---|---|---|
| 1 | A1 | `tools/piles.py (+node_vocab, NODE_COLS, _parse_nodes, _frozen_lines, +_new_node_rows, +_node_origin_problem, +_plan_problem, check_form)`: the vocabulary reader (E8, E15 battery); the two columns parsed; (в) masks `Тип`/`Откуда` (§4); (д) new-row checks with the B4(b) identity (E9, E21-E24, refusal texts); `tools/piles-vocab.json` created (no `carry_retired` key yet); the template | `C:/QAFactory/forge-repo/tools/piles.py` `C:/QAFactory/forge-repo/tools/piles-vocab.json` `C:/QAFactory/forge-repo/tools/piles_testkit.py` `C:/QAFactory/forge-repo/tools/test_piles_form.py` `C:/QAFactory/forge-repo/tools/test_piles_frozen.py` `C:/QAFactory/forge-repo/plans/piles/_template/batch.md` | `python -m pytest tools/test_piles_form.py tools/test_piles_frozen.py -q` (outside the package: `scenario_walk.py --witness-for` has no row; the DoD names the test files, CLAUDE.md rule 4) | designer → builder → critic (topic critic A1-A3+C, R13-g); builder STAGES, Lead commits (mechanism path) |
| 2 | C | `tools/critic_verdict_check.py (validate_verdict, +_remark_errors)` and the schema: `remarks` (§2.3 part 1), ASCII diagnostics, old verdicts fail | `C:/QAFactory/forge-repo/tools/critic_verdict.schema.json` `C:/QAFactory/forge-repo/tools/critic_verdict_check.py` `C:/QAFactory/forge-repo/tools/test_critic_verdict_check.py` | `python -m pytest tools/test_critic_verdict_check.py -q` | builder → topic critic |
| 3 | A2 | `tools/piles.py (_item_why, _node_problem, check_leftovers, leftover_problem, proof_problems, check_proofs, LEFTOVER_FORMS, LEFTOVER_DOOR, LEFTOVER_WRITE_FORMS, +legacy_carries, +_verdict_problem, +_origin_carrier_problem, +_confirm_problem, cmd_status, _status_evidence, _status_args)`: §2.3 parts 2-3, F5 confirmation (E29), E10, E11, E14, E17, E20, E28; `carry_retired` and `confirmers` keys added to the vocab; `tools/wave.py (record_node, by_hand, build_parser, run)`: `--verdict`/`--no-verdict`/`--owner-word` forwarded, step-0 refusal | `C:/QAFactory/forge-repo/tools/piles.py` `C:/QAFactory/forge-repo/tools/piles-vocab.json` `C:/QAFactory/forge-repo/tools/wave.py` `C:/QAFactory/forge-repo/tools/test_piles_close_gate.py` `C:/QAFactory/forge-repo/tools/test_piles_close.py` `C:/QAFactory/forge-repo/tools/test_wave.py` | `python -m pytest tools/test_piles_close_gate.py tools/test_piles_close.py tools/test_wave.py -q` | builder → topic critic; Lead commits (mechanism paths) |
| 4 | D | rule texts 5.1-5.5, 5.7-5.10, 5.12, 5.14 (the instance test); `CLAUDE.md` (5.7-5.9), `.claude/agents/critic.md` (5.11), `.claude/agents/designer.md`, `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` handed as text, placed by the Lead IN THE SAME COMMIT (K-PTR rows need all five carriers); AGENTS.md regenerated | `C:/QAFactory/forge-repo/PROJECT.md` `C:/QAFactory/forge-repo/plans/builder-rules.md` `C:/QAFactory/forge-repo/docs/tasks/critic-diff-brief.md` `C:/QAFactory/forge-repo/tools/tests/test_role_carriers_one_owner.py` `C:/QAFactory/forge-repo/AGENTS.md` | `python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_handoff_rule_anchors.py -q` + `python tools/agents_md.py --check` | builder; Lead places the mechanism-path texts |
| 5 | A3 | `tools/piles.py (+flow, +_flow_reds, door_lines, cmd_summary, _count_line, cmd_status, _close_batch)`: §2.4, E13, E16; `tools/session_context.py (+flow_line call in the boot block)`: one line, 5 s cap | `C:/QAFactory/forge-repo/tools/piles.py` `C:/QAFactory/forge-repo/tools/session_context.py` `C:/QAFactory/forge-repo/tools/test_piles.py` `C:/QAFactory/forge-repo/tools/test_session_context.py` | `python -m pytest tools/test_piles.py tools/test_session_context.py -q` (states the measured `git log` time: F3) | builder → topic critic; Lead commits |
| 6 | B | `tools/backlog_tree.py`: statuses through `piles` (+`type`); `tools/collect_intake.py`: `Тип: неразобран`, `Откуда: находка <file>` (E25, E26) | `C:/QAFactory/forge-repo/tools/backlog_tree.py` `C:/QAFactory/forge-repo/tools/test_backlog_tree.py` `C:/QAFactory/forge-repo/tools/collect_intake.py` `C:/QAFactory/forge-repo/tools/test_collect_intake.py` | `python -m pytest tools/test_backlog_tree.py tools/test_collect_intake.py -q` | builder (on A1's branch, merged right after A1) → topic critic |
| 7 | K | §8: `tools/rule_sources.json` (main files + service globs, data), `tools/rule_stamps.py` (`section_hash`, `parse_markers`, `check`, `census`, `stamp`), `tools/rule-stamps-baseline.json` (the census ratchet), the carrier test's K-OWN/K-PTR lists moved into `rule_sources.json` and its stamp/census rows | `C:/QAFactory/forge-repo/tools/rule_sources.json` `C:/QAFactory/forge-repo/tools/rule_stamps.py` `C:/QAFactory/forge-repo/tools/rule-stamps-baseline.json` `C:/QAFactory/forge-repo/tools/tests/test_role_carriers_one_owner.py` (+ `.githooks/pre-commit` and `.github/workflows/forge-check.yml` lines handed as text — enforcement files, the Lead places them; `tools/mechanism_gate.py` `MECHANISM_PREFIXES` entries — Lead) | `python -m pytest tools/tests/test_role_carriers_one_owner.py -q` + `python -B tools/rule_stamps.py check` (exit 0 on the tree) + `python -B tools/rule_stamps.py census` (prints the count written to the baseline) | designer → builder → critic (its own topic); Lead commits (mechanism: a gate) |
| 8 | E-k | M1 orphans, one pile group per node (groups by the (е) WARN list; **`forge` and `package-ci` excluded** — G owns them, N4) | `C:/QAFactory/forge-repo/plans/piles/<slug>/` of the group's piles (untaken batches, cards, findings) | `python -B tools/piles.py check --all` — the (е) line for the group's piles: 0 orphans; (д) green | scout (evidence) → Lead (stale) → builder (rows) |
| 9 | G | M2 (per F7), M4, M5, forge/7 as a container (F20), forge's and package-ci's own orphans | `C:/QAFactory/forge-repo/docs/tasks/factory-fixes.md` `C:/QAFactory/forge-repo/docs/tasks/test-diet.md` `C:/QAFactory/forge-repo/docs/tasks/onboarding-streams-2026-11-12.md` the six plan files (P25) `C:/QAFactory/forge-repo/plans/piles/forge/` `C:/QAFactory/forge-repo/plans/piles/package-ci/` (+ `docs/tasks/lead-queue-fable.md` only under F7 (a)) | `python -B tools/piles.py check --all` (forge, package-ci: (д), (е) green) + doc key-presence for the `архив:` lines (CLAUDE.md rule 11 doc-dispatch witness: keys verbatim, full script source, one negative control) | builder; Lead judges stale; Lead runs take/status/close for forge/7 |
| 10 | K2 | the census worked down: each counted block of a service file becomes a `see:` pointer or a stamped carried block (§8.5), one service file per commit, the baseline lowered in the same commit | the service files of `rule_sources.json` that are NOT mechanism paths (`docs/tasks/*brief*.md`), `C:/QAFactory/forge-repo/tools/rule-stamps-baseline.json`; `.claude/agents/*`, `.claude/skills/*` handed as text (Lead places) | `python -B tools/rule_stamps.py check` + `python -B tools/rule_stamps.py census` (lower than before) | builder; Lead places mechanism-path files |
| 11 | H | `tools/piles.py (check_findings, FINDINGS_FROM)`: (е) one rule after M1 = 0; Lead: `.claude/settings.json` stale allow lines (P23), `tools/mechanism_gate.py` `MECHANISM_PREFIXES` + `tools/piles-vocab.json` | `C:/QAFactory/forge-repo/tools/piles.py` `C:/QAFactory/forge-repo/tools/test_piles_findings.py` | `python -m pytest tools/test_piles_findings.py -q` | builder; Lead |

Round 1's stream F (debt-file migration) is REMOVED (owner's word, F8). Every new test case is a ROW (or a parametrised
table) in the test file named in the stream's owns (docs/TESTING.md: no new test file — K's rows go into the existing
axis-31 test, the home of this class); E15's battery is one table per input kind in the file of the stream that reads
it (A1 vocab, C verdict, A2/A3 typed reasons, K `rule_sources.json` and stamps).

### 7.3 Order lines with the parallel specs (N3)

| file | streams that touch it | order |
|---|---|---|
| `CLAUDE.md` | boot-by-topic (homes), architect-tier stream L, this D (5.7-5.9), K2 (stamps/pointers only if CLAUDE.md is itself listed as a service — it is a MAIN file, so no) | boot-by-topic → architect-tier → D; D's edits anchored by their quoted old text; Lead places |
| `PROJECT.md` | boot-by-topic (moves 2c/2d/9a/9b), this D | boot-by-topic first (F12); D edits each fragment in its home then |
| `.claude/agents/critic.md` | architect-tier (rule 9), this D (rules 5, 17, 19), K2 (pointers/stamps) | architect-tier → D → K2; Lead places |
| `.claude/settings.json` | architect-tier, this H (allow lines) | architect-tier → H; Lead |
| `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` | architect-tier stream F (check 49), this D (checks 33, 39) | architect-tier → D; Lead |
| `tools/mechanism_gate.py` | architect-tier A5 (`_tier_queue_note`), this H and K (`MECHANISM_PREFIXES`) | architect-tier → H/K; disjoint functions (D-0048) |
| `tools/session_context.py` | architect-tier stream C (architect-queue count), this A3 | disjoint functions; the later merges `main` and keeps both lines; `очередь:` line in both batch files |
| `tools/tests/test_role_carriers_one_owner.py` | this D, then K | D → K (`очередь:`) |
| `.githooks/pre-commit`, `.github/workflows/forge-check.yml` | K (one line each), boot-by-topic / architect-tier if they add lines | Lead places, appended; no reorder |
| `.claude/agents/designer.md` | this D (rule 2 sentence), K2 | D → K2 |

### 7.4 Readers of every touched file (designer rule 3)

Commands (Grep tool; the root checkout, worktrees not counted): `piles\.py|import piles|from piles` over `tools/`,
`.githooks/`, `.claude/settings.json`, `.github/` → 42 files (round 1); `.githooks/` re-run for
`piles\.py|wave\.py|session_context|critic_verdict_check|test_role_carriers_one_owner` → 1 hit (`commit-msg:40`);
`wave\.py|import wave|from wave` over `tools/` → 4 files; `session_context` over `tools/` → 36 files;
`test_role_carriers_one_owner` over `tools/` → 1 (itself); `critic_verdict` over `tools/` → 9 files, over `.claude/` (not
worktrees) → `settings.json:163`, `agents/critic.md:141, 150`; the same `.claude` grep for `wave\.py|session_context|
piles\.py|backlog_tree|collect_intake` → `settings.json:10, 156, 157, 175, 176`, `skills/boot-diet/SKILL.md:24`;
`factory-rules-debt` → 54 files (no longer touched); `lead-queue-fable` → 4 files; `backlog_tree` → 17; `collect_intake`
over `tools/` → 3; `critic-diff-brief|builder-rules` over `tools/*.{py,json}` → the anchors of P22 + `test_quarantine.py:51`,
`test_dispatch_manifest.py:844`. `rule_sources|rule_stamps|rule-stamps-baseline` → none (new files; K creates them).

| touched file | other readers | verdict |
|---|---|---|
| `tools/piles.py` | the 42 of §4 | `load_tree`/`parse_*`/`leftovers_unowned`/`printable`/`write_bytes_atomic`/`LEFTOVER_EMPTY_WORDS` signatures unchanged; `compact_snapshot.py`, `forge_metrics.py`, `piles_split.py`, `canon_clock.py`, `ci_read_common.py`, `md_table.py`, `hook_liveness_probe.py` (probe 14 still "refuses a broken tree"; no new probe → the count pins 482/1015 unchanged), `worktree_sweep.py`, `mechanism_gate.py`: unchanged; `wave.py`: changes in A2; `backlog_tree.py`, `collect_intake.py`: B; `session_context.py`: A3; `critic_verdict_check.py`: C; `.githooks/commit-msg`, `forge-check.yml`: unchanged command, new reds inside (д) |
| `tools/piles-vocab.json` (new) | after A1: `piles.node_vocab` only; through it B, C; `mechanism_gate.py` list (H) | created in A1, `carry_retired`/`confirmers` in A2 |
| `tools/wave.py` | `test_wave.py`, `mechanism_gate.py` (mechanism prefix), `test_mechanism_gate.py` | `test_wave.py` changes in A2; the gate's prefix entry unchanged |
| `tools/session_context.py` | 36 files: the hook config (`settings.json:10`), its four test files, `hook_liveness_probe.py` / `test_hook_liveness_probe.py`, `wiring_check.py`, `dod_gate.py`, `owns_gate.py`, `dispatch_gate.py`, `hygiene_gate.py`, `journal_*`, `calibration_counts.py`, `compact_snapshot.py`, `install_parity_anchors.json`, `dup-baseline.json`, `skills/boot-diet/SKILL.md` | one ADDITIVE output line; A3's builder runs the four `test_session_context*.py` files' narrow rows and the probe's SessionStart row, and names any line-count pin that moves (no pin found by name in this pass — NOT verified line by line; A3's DoD lists them); architect-tier stream C: order line §7.3 |
| `tools/critic_verdict_check.py`, schema | `.claude/agents/critic.md:141, 150` (rule 17 changes in D), `test_critic_verdict_check.py` (C), `install_parity_anchors.json`, `dup-baseline.json`, `md_regions.py`, `escape_check.py`, `test_p4_stdin_deadline.py`, `test_handoff_rule_anchors.py:94, 107` (text "critic_verdict_check.py" in a block — unchanged) | new REQUIRED field: every critic verdict from C on carries `remarks` (critic.md rule 17 says so in the same wave); `piles.py` imports `check_text` (A2) |
| `docs/tasks/critic-diff-brief.md` | anchors P22, `.claude/agents/critic.md`, CLAUDE.md rule 3, the carrier test (new POINTERS row; later K's data) | anchors and K-OWN keys byte-identical; D, then K2 |
| `PROJECT.md` | imported by CLAUDE.md; AGENTS.md (generated); the carrier test (OWNER key + 5 POINTERS targets); boot-by-topic (moves fragments); K (a MAIN file: its section hashes are read by `rule_stamps.py`) | AGENTS.md regenerated in D; order §7.3; K reads, never writes it |
| `plans/builder-rules.md` | anchors P22 (7b), `test_quarantine.py:51`, `test_dispatch_manifest.py:844`, the carrier test, K (a MAIN file) | п. 1 only; 7b untouched |
| `CLAUDE.md` (4a, 9, 12 clauses) | AGENTS.md, `install_parity_anchors.json`, the carrier test (K-OWN rule 9 key, COST anchor — untouched; new POINTERS row), K (a MAIN file) | Lead places in D's commit |
| `.claude/agents/critic.md`, `designer.md` | the carrier test (existing pointers untouched; new rows), `install_parity_anchors.json`, K (service files) | Lead places in D's commit; K2 later |
| `tools/tests/test_role_carriers_one_owner.py` | none (Grep → only itself) | D, then K |
| `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` | `mechanism_gate.py` (mechanism path), calibration sessions | Lead, D's commit |
| `plans/piles/_template/batch.md` | `test_pile_cards_contents.py` (heading test on the template), `piles.py` `batch_heading_problems` | headings kept: unchanged |
| `docs/tasks/lead-queue-fable.md` | P16 (no code); architect-tier readers | per F7 |
| `.claude/settings.json` (allow lines) | `hook_liveness_probe.py`, `test_workflows.py` (they parse hooks, not allow lines — the Lead verifies when placing) | H, Lead |
| `.githooks/pre-commit`, `forge-check.yml` (K's lines) | `hook_liveness_probe.py` and `test_workflows.py` parse hook/workflow commands; `wiring_check.py` | K's builder hands the lines; the Lead places them and runs those two tests' narrow rows; a new probe (if the probe asks one per hook line) moves the count pins 482/1015 — K's DoD names whether it does (NOT verified here) |
| `ai-packages/qa-factory/design/factory-rules-debt.md` | P18 | NOT touched by this spec any more |

### 7.5 Producers (designer rule 6)

| produced | producer (owning node) |
|---|---|
| `Тип`/`Откуда` cells of new rows | the row's writer (Lead/builder/scout by hand), `collect_intake` (B) |
| `remarks` in a verdict | the critic (role); its shape checked by C |
| `--verdict`/`--no-verdict`/`--owner-word` | the Lead at `wave.py merge` (A2 adds the arguments) |
| `подтвердил:` on a `узел:` item | the owner or the batch's Lead (F5, decided); A2 checks its presence |
| `приток:` commit lines | the committer (A3 reads them) |
| `carry_retired`, `confirmers` keys | A2 |
| the flow line at SessionStart | A3 (`session_context.py`) |
| the red-CI record | per F15 (recommended: the fixing commit's message — the committer; no new producer) |
| node rows from M1-M5 | E-k, G |
| `rule_sources.json`, the census baseline, the stamps | K (the tool and data), K2 and every later editor of a service file (stamps; `rule_stamps.py stamp` writes the hash, the editor reads the block first) |

### 7.6 Architecture (forge analogs) and the four questions

No package file changes → `architecture: none -- forge tools and rule texts only` would be the line for a package
commit; none is planned. The forge analogs kept: AR-1 (main files and service globs are a data row), AR-13 (one reader:
statuses and the vocabulary through `piles`; the verdict shape through `critic_verdict_check.check_text`; section hashes
through `rule_stamps.section_hash`), AR-14 (one writer: node rows by the pile road; stamps by `rule_stamps.py stamp`),
AR-15 (one survivor: «Остатки» and «Живые доказательства» keep ONE reader of their forms; generated indexes and stamps
share one road — §8.2), AR-20 (the census ratchet only shrinks; a raise is named), AR-29 (the §4 class table), AR-28 (no
unknown becomes a pass: E16, E20, E8, §8.3).

Four questions (CLAUDE.md rule 10) for the commits of A1/A2/A3/C/D/K: the committer writes the full axis enumeration
(it needs the current map). Likely axes: 1 (the pointer set, kept by §5.14 and then §8), 4 (debt ↔ backlog ↔ nodes),
18 (the new census ratchet is a member; none raised), 31 (one owner per aspect — the carrier test and K), 34 (one road:
one table, one leftover form, one road per red CI, one road for a carried rule). Detectors: §5.12 items (i)-(iv) in
calibration check 33; check 39; §8.6 item. What stops skipping: the commit-msg (д)/flow gate, `status --set принято` via
`wave.py merge`, `close`, `critic_verdict_check` self-run by the critic, `rule_stamps.py check` in pre-commit and
forge-check, the carrier test in CI.

---

## 8. The class (W3): service files never contradict the main files, even when the main files change every day

The owner's word (17.11.2026, W3): «это починит только одно место. А надо что бы все служебные файлы не противоречили
основным даже если мы будем основные каждый день менять.» §5 is the first instance; this section is the mechanism for
the whole class, built as its own stream K (+ K2 for the existing files). Direction decided by the Lead (a)-(c) below.

### 8.1 Main files and service files are DATA (AR-1)

`tools/rule_sources.json` (new, K):
```json
{"main": ["CLAUDE.md", "PROJECT.md", "docs/TESTING.md", "plans/builder-rules.md"],
 "service": [".claude/agents/*.md", ".claude/skills/**/SKILL.md", "docs/tasks/critic-diff-brief.md",
             "docs/tasks/*brief*.md", "<the dispatch templates of tools/dispatch_new.py — K's builder names the file(s)>"],
 "service_exclude": ["docs/tasks/specs/**", "docs/tasks/handoffs/**"],
 "owner_keys": [...], "pointers": [...]}
```
- `main` = the Lead's list (W3 dispatch). Adding `docs/TEAMWORK.md` when boot-by-topic creates it is one data row (K's
  builder adds it if the file exists at K's merge; else the boot-by-topic commit does — its readers list gets this line).
- `service` = everything a worker reads INSTEAD of the main text. P39 measured 18 files in the first three globs; the
  dispatch templates are named by K's builder (NOT located in this round).
- `owner_keys` / `pointers` = today's hand lists of `test_role_carriers_one_owner.py` (P33) moved into data; the test
  reads them from here (one list, AR-13).
- Empty outcome: `main` empty or `service` empty → `CannotRun` naming the key (a check with nothing to judge never passes
  as green, FR-59); a glob matching nothing → one WARN line naming it (a stale glob), not a failure.

### 8.2 The three legal forms of a rule inside a service file

(a) **Pointer** (the default): `see: <main file>#<anchor>` (in markdown: plain text or an HTML comment
`<!-- see: PROJECT.md#**Остатков нет по правилу** -->`; the human-readable sentence around it, e.g. «PROJECT.md «Командная
работа» п. 9», is free). The service file does not restate the rule.
(b) **Carried block** (only where the worker cannot load the main file and the text must travel): either
  - GENERATED from the main section by a generator with `--check` (the road of `tools/factory_rules_index.py`, P38) —
    for a block that is a pure projection (an index, a list of rule titles); or
  - STAMPED: the block is preceded by `<!-- source: <main file>#<anchor> @ <hash12> -->` and closed by
    `<!-- /source -->`; `<hash12>` = the first 12 hex of `section_hash(main file, anchor)`.
(c) **Role detail** not in any main text: free, unmarked; counted by the census (§8.4), never refused.

Anchor grammar (one reader, `rule_stamps.section_bounds`): `<anchor>` is a literal line prefix that occurs EXACTLY ONCE
as the start of a line in the main file (a heading `## Routing rules`, a numbered rule `9. Fix the class`, a bold lead-in
`**Остатков нет по правилу**`). The section runs from that line to the line before the next line that is a heading of
the same or a higher level, or — for a list-item anchor — the next sibling item at the same indentation, or a heading.
`section_hash` = sha256 over the section's lines with CRLF → LF and trailing spaces stripped (so a line-ending flip or
trailing blanks never move a stamp).

### 8.3 The check on the commit path and in forge-check

`python -B tools/rule_stamps.py check [--staged | --base <rev>]` — in `.githooks/pre-commit` and in
`.github/workflows/forge-check.yml` (Lead places both). It reads `rule_sources.json`, finds every `see:` and `source:`
marker in every service file, and:

| case | behaviour | text (what / expected / door) | invariant |
|---|---|---|---|
| E30 stamp hash ≠ the source section's current hash | red | `<service file>:<line>: the block stamped from <main>#<anchor> @ <old12> is stale: that section now hashes <new12> (it changed in <the last commit touching it, when git can say>) -- re-read the block against the section and fix its meaning, then re-stamp it: python -B tools/rule_stamps.py stamp <service file>:<line> (writes the new hash); both in this commit` | a carried block never silently outlives a changed rule; code judges the hash, the re-stamper judges the meaning (AR-29) |
| E31 anchor occurs 0 times (main section renamed or deleted) | red, for a `see:` and a `source:` alike | `<service file>:<line>: <main>#<anchor> points nowhere: no line of <main> starts with "<anchor>" -- the section was renamed or removed; point the marker at its new anchor (and re-stamp a carried block), or remove the block if the rule is gone` | a pointer always lands on a real rule (the K-PTR direction: safe) |
| E32 anchor occurs 2+ times | red | `<service file>:<line>: <main>#<anchor> is ambiguous: <n> lines of <main> start with it (lines <a>, <b>) -- lengthen the anchor until it is unique` | one anchor, one section |
| E33 a main file edited daily | only the stamps whose SECTION hash moved go red; an edit elsewhere in the same main file reds nothing; cost = one `stamp` call (+ the read) per carried block actually affected; pointers (a) never go red on content edits, only on E31/E32 | — | the price of change is per affected block, never per file |
| E34 a main file in `main` that does not exist / a service glob that matches nothing | `CannotRun` naming the path / one WARN line | `rule_sources.json: main file <p> does not exist -- fix the list (one row per main file)` | the list never points into the void silently |
| E35 the commit edits a main section AND its stamped block's text but not the stamp | red (E30): editing the block is not re-stamping | as E30 | the stamp is the record that someone re-read the block after the change |
| E36 git cannot read the base (`--base`) | `--staged`/working tree judged; with `--base` unreadable → NOT CHECKED note naming why, exit 0 in pre-commit, exit 2 in CI (CI has the history; an unreadable base there is a broken run) | `rule_stamps: the base <rev> cannot be read (<why>); stamps judged against the working tree only` | an unknown is named; CI never passes on it |

The informed pass (FR-4) for a stale stamp that is deliberately left for one commit: a commit-message line
`stamp-skip: <service file>:<line> -- <why>` (read like `piles-skip:`); calibration counts them (§8.6). The door of the
check is the re-stamp in the same commit; the pass is the exception, never the road.

### 8.4 The census and its ratchet

Unit (fork **F21**, Lead; recommended (a)): (a) a BLOCK of a service file — a paragraph or a list item, fences and
headings excluded — that carries neither a `see:`/`source:` marker nor sits inside a stamped block; counted per file.
This is pure shape (no wording read, FR-12): legitimate role detail (form (c)) is counted too, by design — the count is
"text a reader cannot trace to a main rule", not "a contradiction". (b) A block that shares a verbatim span of ≥ 12
consecutive words (whitespace-squashed, case-folded) with any main file and is unmarked — a copy detector, narrower
(blind to paraphrase and translation). (c) Both, (b) as a red and (a) as the ratchet.
- `python -B tools/rule_stamps.py census` prints `rule census: <total> unmarked blocks in <k> service files` and one line
  per file; `--write` writes `tools/rule-stamps-baseline.json` (`{"<file>": <count>}`).
- Ratchet (shrink-only, AR-20, axis 18): `check` is red when a file's count rises above its baseline row — text:
  `<service file>: <now> unmarked blocks, baseline <base> -- point new rule text at its main section (see: <main>#<anchor>)
  or stamp it; role detail that belongs to this file only: add the line "rule-census-raise: <file> +<n> -- <why>" to the
  commit message and raise the baseline row in the same commit`; a lower count without lowering the row → one note "lower
  the baseline row to <now>" (the ratchet tightens by hand in the same commit, as the repo's other ratchets do).
- Today's count: NOT MEASURED — the unit is defined by this spec and no tool computes it yet. The one command that
  measures it is K's first act: `python -B tools/rule_stamps.py census --write`; its printed total is written into this
  spec's premises (a new P40) at K's acceptance, with the command as its carrier. What IS measured now (P39): 18 service
  files in the first three globs, 0 stamps.

### 8.5 Order of work

- K (one node): `rule_sources.json`, `rule_stamps.py` (`section_bounds`, `section_hash`, `parse_markers`, `check`,
  `census`, `stamp`), the baseline at today's count (nothing goes red on the first day: the ratchet starts where the tree
  is), the carrier test reads `owner_keys`/`pointers` from the data file and gains rows: the E30-E36 table and E15's
  battery for `rule_sources.json` (a glob with `..`, an absolute path, BOM, a 1000-entry list, a duplicate, a non-string),
  `stamp` writes nothing on a stale anchor, a negative control per red (a stamp corrupted on a COPY → named, CLAUDE.md
  hygiene 7 (d)). §5.14's five POINTERS rows become `see:` markers in their carriers with K (the hand rows go).
- K2: the census worked down file by file (biggest first, by K's census output), each counted block turned into a pointer,
  a stamped block, or left as role detail; the baseline row lowered in the same commit. The leftover-rule carriers of §5
  go first (they are the instance the owner saw).

### 8.6 Error direction, owners, detector

- The hash check errs SAFE: any byte change inside a source section (after the CRLF / trailing-space normalisation) reds
  every stamp on it — including a typo fix that does not change the meaning (false red; door: re-read, re-stamp, one
  command). It never passes a changed section. Its blind spot: a service file whose text drifts while the main section
  stays the same (someone edits the carried block) — caught because `stamp` records the hash of the SOURCE, and the carried
  text itself is free… so an edit of the block alone is NOT caught by the hash; it is caught by the census only if the
  block loses its marker. Recommended closure (small choice, closed): the stamp also carries the hash of the carried
  block's own text (`@ <source12>/<block12>`); `check` reds a block whose own text moved without a re-stamp — same door.
- Pointers err SAFE (E31/E32 only); they cannot see a contradiction in prose written next to them — that is the census's
  count and calibration's read.
- Owners (AR-29): the hash, the anchor resolution, the count — data (code); "does the carried block still mean the main
  rule" — judgment of the re-stamper (a role), accepted by the Lead at the diff gate; which main files exist — intent (the
  Lead's list, the owner's word on the class).
- Detector (rule 10 (c)): calibration check 33 gains item (v): the window's `stamp-skip:` and `rule-census-raise:` lines,
  the census trend (it must fall while K2 runs), and a sample read of five unmarked blocks against the main files (the
  semantic drift no code sees). What stops skipping (rule 10 (d)): `rule_stamps.py check` in pre-commit and forge-check.

---

## F. Forks (options, consequences, recommendation; OWNER = only the owner decides)

Decided: **F2** — (a) size is not a criterion (the owner's word, section at the end). **F5** — "the owner or the batch
Lead" confirms a node leftover on its «Остатки» item: the owner's «ок», 17.11.2026 (W2, relayed by the Lead in the t-926
thread); executed in §1.4, §2.2, §5.3, §5.13, E29, A2. **B1-B5 directions** — the Lead's decisions, «ок» by the owner
(W1).

- **F1 (OWNER) — the `Тип` words.** (a) the owner's five + `живой-прогон` + `решение` + `неразобран` (recommended:
  `неразобран` is the declared unknown so code never picks a type, FR-59); (b) the five + `неразобран` only — live proofs
  and decision nodes need another type; (c) the five only — `collect_intake` then must pick one of her words (code
  choosing a work type, t-920 key 4).
- **F3 (Lead) — the counter's data source.** (a) git history (recommended; A3 measures and states the `git log` time);
  (b) an `Открыт` date column written by hand.
- **F4 (Lead) — `перенос:` retired as a NEW form.** (a) yes, every new carry is `узел:` (recommended, P31), legacy items
  close by the old form (E20); (b) keep `перенос:` for live proofs — two forms for one action.
- **F6 (Lead) — a growing batch.** (a) the add-time refusal without `приток:` (recommended, an informed pass FR-4);
  (b) print only.
- **F7 (Lead) — the Lead queue vs the ACCEPTED architect-tier F8 (a).** The substance is the owner's («the Lead queue
  becomes nodes»); what remains is amending that spec. (a) retire the file; "below-Lead cannot" and Architect items are
  nodes with `Исполнитель: Lead` / `Architect`; amend: its `git mv` + new `architect-queue.md`, `session_context.py`
  count (its stream C → counts nodes through `piles`), `mechanism_gate._tier_queue_note` (its A5 → names the pile road),
  calibration check 49 (b) (its stream F), `docs/SIBLING_MAP.md:655-661` «Lead Queue» (recommended, one registry);
  (b) the two queue files outside piles — contradicts «всё в кучках»; (c) the files as VIEWS listing node ids only.
- **F8 (OWNER) — the debt file once its rows are fixed** (her word: «давай починим сейчас … fate after it is empty»).
  (a) deleted by the debt-fix spec's last commit, with its readers (G1-10, K0.15, `factory-rules.md:230, 305`,
  `piles.debt_warnings`, `test_piles_close_id.py`); a future unfixed violation is a node `Тип: долг` (5.6 (a)) —
  recommended, one registry; (b) kept empty as the package's map; a future violation is a node + a row. This spec
  writes nothing to the file under either answer.
- **F9 (Lead) — taken batches.** (a) not migrated (recommended); (b) migrated — now free of doors thanks to the (в) mask.
- **F10 (Lead, relabelled from OWNER per t-920 key 7: reversible, git keeps the file)** — done orphan findings: (a) M1
  deletes them (recommended, «решила сама» line); (b) delete every finding of a closed node at `close`.
- **F11 (Lead) — a big idea's home.** (a) a batch in the topical pile (recommended); (b) a pile per idea.
- **F12 (Lead) — order with boot-by-topic, and its gate criterion.** (a) boot-by-topic lands first; D edits each fragment
  in its home (recommended). The criterion shift (N10): after A2 a gate refuses part of 9d, so boot-by-topic's own rule
  would move the home to TEAMWORK; recommended: the home stays in PROJECT.md (every role reads it at boot) and the Lead
  amends that spec's row 9d with this reason; if it moves anyway, the K-PTR rows / `see:` markers turn red and follow.
- **F13 (Lead) — which added rows the flow brake counts.** (a) every added row (recommended: closes the self-label
  escape; cost: one `приток:` line per growing commit of an incoming batch); (b) exempt `находка` rows whose finding file
  is added in the same commit — cheaper; a remark dressed as a finding passes.
- **F14 (OWNER) — a builder-noticed analog (14, not in her list).** (a) the same as critic remarks: own code fixed now,
  other code `чужой-код` (recommended); (b) always a node with `Откуда: находка`. Under (a) builder-rules п. 1 and 5.3's
  first dash name the builder; under (b) nothing changes for builders.
- **F15 (Lead) — the record of a red CI.** (a) no finding: the fixing commit message names the red run
  (`ci_read.py why` summary) and, when an accepted node caused it, a `defect_found` journal line (recommended, one road);
  (b) a finding file exempt from (е) — two roads (P31).
- **F16 (OWNER) — a defect after acceptance that is not a red CI.** (a) the same as a red CI: fixed on the spot as a new
  task_id with `defect_found` (CLAUDE.md rule 4 forbids reopening), no node (recommended); (b) a node `Тип: баг`,
  `Откуда: находка`.
- **F17 (Lead) — the B1 code point.** (a) `status --set принято` + `wave.py` `--verdict` (recommended, §2.3); (b) the
  `dod_gate.py` stop check with a `judged-owns:` dispatch line; (c) discipline + calibration only.
- **F18 (OWNER) — «занятый файл» (not in her list).** (a) not a reason: the fix is the same node's second round after the
  other batch merges, or now under D-0048 function lists / an `очередь:` line; the node stays open and may hold its batch
  (recommended); (b) a reason: a node with key `занятый-файл` — the batch closes, the remainder lives elsewhere.
- **F19 (OWNER) — «ждёт события» (not in her list, e.g. FG7-35 "conditional").** (a) not a reason: the node stays open
  and does a second round after the event; its batch waits (recommended); (b) a reason: a node with key `ждёт-события`
  naming the event.
- **F20 (Lead) — forge/7 and untaken incoming batches.** (a) close forge/7 as a container after moving its 38 open rows
  to batches with a real scope (recommended, §2.4); (b) also forbid `status --set принято` on a node of an untaken batch
  (t-920 B2 (b): taking becomes the one road) — stronger, every incoming batch must be taken first.
- **F21 (Lead) — the census unit (§8.4).** (a) unmarked blocks, shape only (recommended: counts everything a reader cannot
  trace, never reads wording; cost: legitimate role detail needs a `rule-census-raise:` line when it grows); (b) verbatim
  copies of main text only (narrow, blind to paraphrase); (c) (b) as a red + (a) as the ratchet (strongest, most friction).

## Small choices closed by the designer

- Statuses stay code constants; types, origin heads, criteria, dispositions, confirmers and `carry_retired` are data.
- `tools/piles-vocab.json` keys ASCII, Russian words as values with `means` and (for criteria/confirmers) `word`.
- Old rows without `Тип` are counted, never red (E9).
- Flow window 7 days; ISO dates; SessionStart cap 5 s.
- `Откуда` separator ` · ` (U+00B7).
- `collect_intake` writes `Откуда: находка <file>` and `Тип: неразобран` (under F1 (a)/(b)).
- B is built on A1's branch and merged right after it (E25).
- C is a separate node before A2 (smaller nodes; A2 imports C's `check_text`).
- The rule texts and the instance test land in ONE commit (K-PTR needs every carrier at once).
- The disposition word is `чужой-код`, the same word as the `leftover_criteria` key (one word for one thing).
- §8: a generated block where the block is a pure projection, a stamp otherwise; the stamp carries the source hash AND the
  block's own hash (§8.6); the section hash normalises CRLF and trailing spaces; K starts the ratchet at today's count.
- K's rows live in the existing axis-31 test (no new test file); its hand lists move into `rule_sources.json`.

## Noticed, not widened (analogs and contradictions)

- The debt file's header count ("25") contradicts its own rows (44) — told to the debt-fix stream (§3 M3).
- `.claude/settings.json` allow lines for the retired `board --check` (P23) — H.
- `backlog_tree.py` prints the first token of a status (P6) — B.
- The card «Содержание» column `тип` (строка/находка) is the CARRIER kind, not the work type — keep the names apart
  (Lead's call; not in owns).
- `wave.py` records the node status AFTER the push (P30): a refused status never undoes a merge. The B1 refusal is
  therefore a brake on the node's acceptance, not on the merge — intended.
- forge/3 and forge/6 were closed with `взял: —` (P28): an earlier container close by hand; F20 makes it a road.
- The package has the same class (role files and `references/slices/*` carrying `design/*.md` rules; the slices are
  already generated — `references/slices/` in the package). §8 is forge-only by the Lead's list; the package's twin is an
  analog to put to the Lead, not widened here (axis 34 / P31: one road for "a carried rule" would cover both — the Lead
  decides whether to open a node).
- AGENTS.md is a generated copy of the main files (excluded from the carrier test) — already the (b)-generated road.

## Reading trail

Round 1: `plans/piles/forge/README.md:1-80`; `plans/piles/forge/batch-7-vhodyashchie-4.md` (whole);
`plans/piles/_template/batch.md`, `finding.md`; `tools/piles.py` (ranges in round 1); `tools/backlog_tree.py`;
`tools/collect_intake.py:955-1014`; `tools/mechanism_gate.py:205-284`; `factory-rules-debt.md`; `lead-queue-fable.md`;
`docs/tasks/critic-diff-brief.md`; `.claude/agents/critic.md:20-39, 160-174`; package tests G1-10/K0.15; architect-tier
and boot-by-topic specs by Grep; AGENTS.md; journal `t-895`.
Round 2 (t-926): the review t-920 whole; this spec whole; `tools/piles.py:1588-1777, 2516-2565, 2686-3005, 3125-3465` +
Grep of its defs; `tools/critic_verdict.schema.json`, `tools/critic_verdict_check.py` (whole); Grep
`critic_verdict_check|validate_verdict|check_text\(` over `tools/*.py`; `tools/wave.py:1-58, 245-274` + Grep of defs;
`.claude/settings.json:1-14, 100-130` + Grep; `tools/dod_gate.py` Grep of defs/`owns`; `tools/session_context.py` Grep
`piles|summary`; `tools/tests/test_role_carriers_one_owner.py` (whole); `tools/factory_rules_index.py:1-30`;
`docs/tasks/critic-diff-brief.md:28-97`; `.claude/agents/critic.md:26-33, 138-173`; `plans/builder-rules.md:8-11`;
`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` Grep `перенос:` and of check headings; `20261116-architect-tier-spec.md` and
`20261116-boot-by-topic-spec.md` (read-main worktree) by Grep; Grep `^кучка:` over `plans/piles/forge`; Grep of the
node-table header and of `Тип|Откуда` columns with the positive control; Glob for the debt-fix spec with the positive
control; journal Grep `"task_id":"t-906"`; Glob of the service-file set (P39); Grep for §8 stamps (0, no control — the
form is new).
Not re-measured by me (no shell): P1, P4, P12, P13, P26, P28 counts — taken from t-920's reruns (key 1); the §8 census.
Needed beyond the manifest: the files above outside `given:` (read-only).

## The owner's word on leftovers (17.11.2026, Lead session; answers to the t-906 origin table) — binds §2.2 and forks F2, F5

Verbatim, per origin:
- critic remarks about other code (20 of 206): «вот это можно оставлять» — a remark about code outside the node's topic may become a node.
- deferred minor critic remarks (51): «делать сразу» — fixed in the same node's fix round, no node, no «Остатки» row.
- the owner's new word during the work (31): «если я что-то новое сказала по теме работ, то надо делать сразу, если я просто сказала что-то из другой темы, то можно завести отдельным узлом».
- defect after acceptance or red CI (27): «CI не записываем отдельными узлами» — a red CI is repaired on the spot and is not a node.
- scope cut by the spec (24): «если я урезала для экономии токенов, то ок, в остальных случаях сделать сразу или спросить меня».
- the critic brief against PROJECT п. 9: «почему бриф противоречит? Это служебный фаил который никогда не должен противоречить основным» — a service file never contradicts the main rules; the brief is brought in line, and a check keeps it so.
- the rules-debt file (F8): «давай починим сейчас, правила это важно» — the 25 open rows are FIXED now (a separate stream of this session), not migrated into nodes; the file's fate is decided after it is empty.
Consequence for the forks: F2 is (a) (size is not a criterion); the criterion of §2.2 is exactly the owner's list above.
(Designer's notes: "25" is the debt file's stale header; its own rows say 44 open — P17, t-920 N8. F5 was answered later
the same day — W2 in the status block: "the owner or the batch Lead". B5's class — W3, §8.)

---

## Fix round t-926 — finding / word → what changed → section

| finding / word | what changed | section |
|---|---|---|
| B1 critic default rests on text and self-label | verdict `remarks` with a typed disposition (`fix` / `чужой-код` + path); `status --set принято` (+ `wave.py`) refuses a `чужой-код` remark inside `Пишет в`; back-reference `остаток … · чужой-код · <verdict>#<rid>` checked at add time; functions, refusal texts, informed passes (`--no-verdict`, `--owner-word`), error direction + adversarial inputs; cheaper points weighed (`dod_gate` stop check, discipline) — none reaches the same guarantee; the remaining self-label escape named with its brake and detector | §2.3, §4 class table, §6 E14/E17/E28, §7.2 C/A2, F17 |
| B2 forge/7 never closes | flow gate at ADD time in (д) with `приток:` door; counter keyed by `(slug, id)`; printed by `summary`, `status`, SessionStart; NOT CHECKED when git cannot measure; forge/7 closed as a container with the exact `close` prerequisites; option "forbid принято in an untaken batch" kept as F20 (b) | §2.4, §6 E13/E16, §7.2 A3/G, F6, F13, F20, P28, P29 |
| B3 diverges from the owner's list | §2.2 rewritten row by row to her list; keys reduced to `чужой-код`, `экономия-токенов`, `живой-прогон`; `другая-кучка`/`слово-владельца` removed; owner's on-topic word = now, off-topic = `Откуда: владелец`; red CI never a node (PROJECT «Как принимается» п. 2 rewritten, 5.5; E27); scope cut only with her token word (+ critic-on-plan key, designer.md sentence); `занятый-файл`/`ждёт-события` removed → OWNER forks F18/F19; F8 by her word: stream F, M3 migration, round-1 §5.5, `debt_warnings` widening and `строки долга без node` removed; F2 decided (a) | §2.2, §3 M3, §4, §5.3, §5.5, §5.6, §5.10 (e), §5.12, F2/F8/F14-F16/F18/F19 |
| B4 both worlds | (a) legacy `перенос:` (and legacy `узел:`) items close by the old form; old vs new told by the cutover commit derived from git (`carry_retired` key, pickaxe), no hand-typed date; (b) (в) `_frozen_lines` drops the `Тип`/`Откуда` cells so a taken batch may gain them; (д) row identity = id + the other cells minus `Тип`/`Откуда`/`Статус`, multiset per pile | §4 (в)/(д), §6 E9/E20, refusal texts |
| B5 nothing keeps the brief in line | one home (PROJECT п. 9 «Остатков нет по правилу»); brief, critic.md, CLAUDE.md 9/12, builder-rules, designer.md point to it with one literal pointer; instance test: OWNER key (Russian), 5 POINTERS rows, RETIRED old texts; error direction stated (K-OWN false pass across languages → calibration item (iv); K-PTR safe) | §5 intro, §5.3, §5.8-§5.12, §5.14, §7.2 D |
| W1 the owner's «ок» to the Lead's B1-B5 decisions | recorded as decided; no fork reopened | status block, §2.3, F (decided) |
| W2 F5 decided: the owner or the batch Lead | F5 closed with her word and date; `подтвердил: <владелец \| Lead пачки>, <дата>` required on NEW `узел:` items (data `confirmers`), legacy items exempt; refusal text; template, home text, 9c sentence, check 39 | §1.1 table, §1.4, §2.2, §4, §5.3, §5.12, §5.13, §6 E10/E29, §7.2 A2, F (decided) |
| W3 B5 is a class: every service file, main files changed daily | §8: main/service files as data (`rule_sources.json`); three legal forms (pointer `see:`, carried block generated or stamped `source: …@hash`, free role detail); `rule_stamps.py check` in pre-commit + forge-check, per-SECTION hash, re-stamp door, `stamp-skip:` informed pass; edges E30-E36 (renamed/deleted/ambiguous anchor, daily edits cost per affected block, missing main file, unreadable base); census + shrink-only ratchet with `rule-census-raise:` door (today's count NOT MEASURED — defined unit, measured by K's first run, P39 gives the measurable now: 18 files, 0 stamps); own streams K and K2 with owns; error direction and owners; detector item (v); census unit returned as F21; package twin noted, not widened | §8, §7.2 K/K2, §7.3, §7.4, §7.5, §7.6, P38, P39, F21, noticed |
| N1 stale line no., P12/P26 unmeasured | P9 (f) → line 10; P12 = 152 (69 undated); P26 = 296 open ids | Premises P9, P12, P26; §3 |
| N2 WEEKLY check 39 | checks 33 (line 1026) and 39 (line 1095) edited, + calibration items (i)-(v) | §5.12, §8.6, P36 |
| N3 order lines | table of shared files with architect-tier and boot-by-topic (+ K's files) | §7.3 |
| N4 package-ci in E-k | E-k excludes `forge` and `package-ci` | §7.2 E-k |
| N5 stream A too big | A1 / A2 / A3 sequential by function lists | §7.2 |
| N6 refusal texts, silent edges, intake default, A→B window | refusal-text table; E21-E26; `неразобран` as the declared default; B on A1's branch, merged right after | §6, F1, small choices |
| N7 F7 relabel, readers | F7 is Lead; architect-tier readers listed with line numbers | F7, P16 |
| N8 debt count 44, not 25 | told to the debt-fix stream; note under the owner's section | §3 M3, P17, owner's section note |
| N9 expected reduction | 31.6 % certain, 44.7 % with F16, up to 71.4 %; ≥ 28.6 % stays legitimately | §2.5 |
| N10 F12 fragment level, gate-criterion shift | edits named per fragment (2c, 9a, 9c, 9d); the 9d criterion shift is part of F12 | §5 intro, F12, P37 |
| key 7: F10 marked OWNER | relabelled Lead (reversible) | F10 |
| t-906 marker in §2.1 | replaced by the measured origin table; streams re-ordered by volume | §2.1, P27, §7.1-§7.2 |
