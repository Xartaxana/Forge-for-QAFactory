# Spec t-907 — «Всё в кучках»: one registry of work, leftovers that do not breed nodes (DRAFT, designer)

Status: DRAFT for Lead acceptance. Forks are returned (section F), none decided. Sections 1-7 answer the brief's items 1-7.
Owner-facing rule texts are Russian; code, tool messages and data keys English (PROJECT.md «Язык»).
Parts that rest on the leftover-source scout t-906 are marked **[depends on t-906]**.

```
task: t-907 (draft) | feature: F19 | the build tasks get their own task_ids per node (CLAUDE.md rule 2, threshold counts each)
designer: this file
```

The owner's decision (17.11.2026, Lead session): «ВСЁ В КУЧКАХ» — the only registry of work on the factory and the forge
is the piles (`plans/piles/<slug>/`); everything that is work is a NODE of a batch; the type of work is a field of the
node; a big idea is its own batch with a plan file; the Lead queue, the FR debt and batch leftovers become nodes;
`plans/BACKLOG.md` stays an archive. The owner's words carrying it are quoted in the brief (t-907 dispatch) and are
not re-quoted here.

---

## Premises (load-bearing facts, each with its carrier; "NOT MEASURED" = the designer had no shell, the Lead measures)

| # | fact | carrier / command | state |
|---|---|---|---|
| P1 | 103 batch files, every header carries a known status word; 36 not closed = 26 `ожидает` + 10 `в работе`; 67 `закрыта` | Grep `^кучка:.*\| статус: (ожидает\|в работе\|сдано\|принято\|закрыта)` glob `batch-*.md` over `plans/piles` → 103 files; the same without `закрыта` → 36 lines (10 `в работе`) | measured |
| P2 | Every batch's node table has the SAME 7 columns `Узел \| Приоритет \| Что \| Исполнитель \| Пишет в \| Зависит от \| Статус` (hotfix-12586/2 has 3 extra helper tables above it) | Grep `^\| *Узел *\|.*` glob `batch-*.md` → 106 lines, 103 of them that header | measured |
| P3 | No `Тип` column exists anywhere; the parser knows `узел/исполнитель/пишет в/статус/что` only | `tools/piles.py:608-609` `NODE_COLS`, `NODE_REQUIRED` | read |
| P4 | ~698 table rows end in a cell starting `ожидает` across 32 batch files (brief: ~685 waiting nodes; mine includes a few non-node rows) | Grep `^\| [^|]+\|.*\| *ожидает[^|]*\|\s*$` glob `batch-*.md` (CRLF files need `\s*$`; positive control: the same shape finds 45 in forge/7) | measured |
| P5 | One status vocabulary in code: `BATCH_STATUSES`, `NODE_STATUSES`, `STATUS_ORDER`, read by `status_word` | `tools/piles.py:111-115, 200-206` | read |
| P6 | A SECOND copy of status words: `CLOSED_WORDS = ("закрыта",)`, `DONE_NODE = ("принято", "закрыт", "отклонено")` — `закрыт` is not a word of P5; the pane prints `status.split()[0]` (`в работе` shows as `в`) | `tools/backlog_tree.py:19-20, 40-50` | read |
| P7 | The brief's "three status vocabularies" not reproduced: (д) refuses a node status that starts with no word of P5 (`_node_reds`, `piles.py:1855-1857`); what varies is the text after the word (`принято (d3b312d, t-121…)` vs `принято: a48dc25 (t-434)`, forge/7:31,44) and P6 | Grep for `снят\|закрыт\|отменён\|перенесён\|сделано\|…` as the last cell of a node row → 6 rows in 2 closed files | measured |
| P8 | 18 of 103 batches are leftover batches by name (`ostatki`, `hvosty`, `tails`, `leftovers`, `remainders`), 7 more are "incoming" (`vhodyashchie`) | the 103 file names of P1, counted by hand | measured |
| P9 | Leftover roads in today's carriers: (a) critic brief q4 sends an out-of-owns analog to «Остатки» as `узел:` or `перенос:` with `подтвердил: —`; (b) q7 severity `queue`; (c) q12(d) "a node with an id and an owner"; (d) `piles.py` write-time gate accepts `узел:` (any worked node of an open batch, no back-reference, no reason) and `перенос:` with a placeholder `подтвердил:`; (e) `close` accepts `перенос:` with any non-placeholder `подтвердил:` text (its docstring: "the gate cannot know who typed `подтвердил:`"); (f) builder-rules п. 1: a need in another file goes to «Needed from integration»; (g) CLAUDE.md rule 9 "fix now, or EXPLICITLY put the remainder in the queue/log"; (h) rule 12 Cost gates: the fix round is a FRESH worker with only the diff and the verdict, its owns unchanged | (a)-(c) `docs/tasks/critic-diff-brief.md:33-36, 55-58, 94-95`; (d) `tools/piles.py:2794-2852`; (e) `tools/piles.py:2767-2788, 2962-2967`; (f) `plans/builder-rules.md:8`; (g) CLAUDE.md rule 9; (h) CLAUDE.md rule 12 | read |
| P10 | Observed instances: forge/7 «Ход» 03.11 "в очередь F3 … F6 … F7 … F9" (critic t-1756 findings queued, not fixed); 14.11 "очередь критика диффа FG7-32 (t-750) заведена узлами FG7-34 … FG7-35 (условный)"; 12.11 16:20 "Не оформлены находками: три предложения узлов критика t-124 …" | `plans/piles/forge/batch-7-vhodyashchie-4.md:86, 88, 89` | read |
| P11 | `close` refuses a bare `узел:` item ("closed by `сделано:` when the node merges, or carried") — so at close every `узел:` leftover is rewritten as `перенос:` into another batch | `tools/piles.py:2979-2981` | read |
| P12 | (е) splits findings at `FINDINGS_FROM = 2026-10-13`: a newer orphan is RED, an older one is ONE WARN line (the baseline; brief: 152) | `tools/piles.py:2038, 2201-2214` | read; count NOT MEASURED — Lead: `python -B tools/piles.py check --all`, the (е) `ok`/WARN line |
| P13 | 1110 finding files; 33 piles | t-895 digest (accepted 16.11, journal line 2202: "counts … match piles check output") | from the journal, not re-measured |
| P14 | `docs/tasks/lead-queue-fable.md`: 12 numbered items + 2 unnumbered lines; by its own status block (16.11) 10 done, 2 open: п. 11 boot budget (boot-diet by the owner's word) and the two count lines of `tools/test_hook_liveness_probe.py` (482, 1015) | `docs/tasks/lead-queue-fable.md:7-24` | read |
| P15 | The two open Lead-queue items already have pile nodes: boot budget ↔ FG7-51 (boot by topic); hook-probe count literals ↔ FG7-49 ("литералы счёта проб в `test_hook_liveness_probe.py` заменены выражениями") | `plans/piles/forge/batch-7-vhodyashchie-4.md:72, 74` | read |
| P16 | Readers of `lead-queue-fable.md`: no code; 4 files name it (journal, `20261116-architect-tier-spec.md`, its review t-902, one compact snapshot). The architect-tier spec F8 RECOMMENDS `git mv` to `docs/tasks/lead-queue.md` + a new `docs/tasks/architect-queue.md` counted by `session_context.py` | Grep `lead-queue-fable` over the repo minus worktrees → 4 files; spec `:298-315, 441` | measured / read |
| P17 | The debt file says "Twenty-five rows are open today"; its own tables hold 47 rows (run 5: 11; FR-47…57: 18; FR-59: 16; FR-42: 1; FR-7: 1) + 3 walk entries = 50 entries, of which 6 say "Closed by …" in their own text (lines 93, 94, 95, 96, 98, 99) → 44 open by the file's own words; the header count is stale | `ai-packages/qa-factory/design/factory-rules-debt.md:5-6, 19-141`, read line by line | read; Lead re-counts at stream F |
| P18 | Code and test readers of the debt file: `tools/piles.py` `DEBT_REL` + `debt_warnings` (close prints a WARNING for debt lines naming a closed B-id); `tools/test_piles_close_id.py:87-89`; PACKAGE: `scripts/tests/test_s1_s2_contract.py:322-325` (G1-10: exactly one `\| FR-21 \|` row, its text matches the kinds file), `scripts/tests/test_null_outcomes.py:589-596` (K0.15: exactly one FR-23/FR-5 row naming `references/null-outcomes.json`, `` `pending[]` ``, `t-305`, `B-253`), `scripts/tests/test-layers.json:3413`; rule text: `design/factory-rules.md:230, 305` ("listed in `factory-rules-debt.md`"), `design/README.md:29`; comments: `window_record.py:317`, `project_decisions.py:39`, `gate_preflight.py:5267`, `references/field-producers.json:9`; forge: `PROJECT.md` / `AGENTS.md:232`, `docs/SIBLING_MAP.md:91, 111`, `plans/features.json:1007` | Grep `factory-rules-debt` over the repo minus worktrees → 54 files; code/test/rule lines as listed | measured |
| P19 | `tools/collect_intake.py:979-1003` builds a NODE ROW for an untaken batch from the table header (`values` keyed `узел/что/исполнитель/пишет в/статус`; any other column → `—`) | read | read |
| P20 | `tools/piles.py` is a mechanism path (commit = Lead, axis block + `tier:`); so are `tools/md_table.py`, `tools/compact_snapshot.py`, `tools/wave.py`, `.claude/agents/`, `.claude/settings.json`, `CLAUDE.md`, `PROCESS/`, `docs/SIBLING_MAP.md`; NOT: `PROJECT.md`, `plans/builder-rules.md`, `docs/tasks/critic-diff-brief.md`, `tools/backlog_tree.py`, `tools/collect_intake.py`, `tools/critic_verdict_check.py` | `tools/mechanism_gate.py:211-283` | read |
| P21 | The critic verdict JSON has `verdict`, `blockers`, `class_completeness`, `trail`, `fixes`; no field for a proposed node — queued items live only in prose | `tools/critic_verdict.schema.json` | read |
| P22 | Text anchors pinned by tests in the files this spec edits: critic brief `## The two layers`, `6. **DUPLICATION AND CONSISTENCY**`, `7. **CODE QUALITY**`, `12. **ONE ROAD**`; builder-rules 7b; PROJECT's pointer strings to them | `tools/tests/test_role_carriers_one_owner.py:28-71`, `tools/install_parity_anchors.json:22`, `tools/test_handoff_rule_anchors.py:38-39` | read |
| P23 | `.claude/settings.json:157, 176` still allow `python tools/piles.py board --check` — `board` is a refused alias since 13.11 | read via Grep | read (stale allow line; Lead) |
| P24 | DAG-like files under `docs/tasks/`: `factory-fixes.md` (30.09, legacy graph), `test-diet.md` (nodes OUTSIDE piles, "Заменяет узел F6-52"), `onboarding-streams-2026-11-12.md` (waves over pile nodes) | first 15 lines of each | read |
| P25 | Plans of big ideas: the six of t-895 are not on disk as a list. Candidates under `plans/`: `feature-fragility-2026-10-02.md`, `RULES-PROPOSAL.md`, `forge-metrics.md`, `project-knowledge-plan.md` (pile `project-knowledge` exists), `thinking-roles-portable-to-main.md` (pile `thinking-roles` exists) | Glob `plans/*.md` | NOT the scout's list — Lead supplies the six (t-895 trail) |
| P26 | `BACKLOG.md` open-row count | `python -B tools/piles.py summary` | NOT MEASURED |

---

## 1. Target model

### 1.1 One node table for every batch

```
| Узел | Тип | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Откуда | Статус |
```

- Two NEW columns, `Тип` and `Откуда`, inserted at those positions; the other seven unchanged (P2).
- `Тип` — one word of the closed list `node_types` in the data file `tools/piles-vocab.json` (FR-13, AR-1). Proposed words
  (fork **F1**, the owner names them):

  | word | means |
  |---|---|
  | `баг` | the factory or the forge does wrong what a rule or requirement says |
  | `доделка` | the remaining part of an ACCEPTED node's own scope (rare by §2; never a critic remark) |
  | `идея` | a new idea of the owner — a new behaviour, not a defect |
  | `оптимизация` | cost, speed, friction (P6, P11, FR-55) |
  | `долг` | a known violation of a rule (FR-n / AR-n / P-n named in «Что») — the former debt-file row |
  | `живой-прогон` | a proof by a live run (FR-33) |
  | `решение` | work that is a decision only (the owner's word, a Lead choice), no file written |

- `Откуда` — where the node came from, one of the closed forms `node_origins` of the same data file:
  `план` (written with the batch / the idea's plan) · `находка` (a finding named in «Что») · `владелец <дд.мм>` (the
  owner's word) · `миграция` (moved by THIS spec, §3) · `остаток <node> · <criterion>` (born from the work of another
  node: `<node>` is `<id>` of the same pile or `<slug>/<N>/<id>`; `<criterion>` is a key of `leftover_criteria`, §2.2).
- `Статус` — unchanged vocabulary (P5); ONE reader `piles.status_word`; `tools/backlog_tree.py` stops keeping its own
  words (P6) and reads `piles.NODE_STATUSES` / `piles.status_word` / `piles.NOT_WRITING`. A dropped node is
  `отклонено: <why>`; no new word (`снят`, `закрыт`) is added.
- Priority stays a node column (P2); the batch header pair `приоритет:` stays the batch's default (template line 6).

Invariant (one road, P31/AR-13): every batch, of every pile, is read by the one parser `piles.parse_batch`; no column is
optional for a NEW row in one pile and required in another.

### 1.2 Big-idea batch

A big idea = a batch in the topical pile (fork **F11**: a new pile only when no card's `зона:` fits) whose header carries
the pair `план: <repo path>` (the plan or spec file, wherever it lives today — `docs/tasks/specs/…`, `plans/…`); its
node rows are the plan's phases/streams, each a normal row (`Откуда: план`). Before a plan exists, the idea is ONE node
`Тип: идея`, `Исполнитель: Lead`, in the topical pile's untaken batch (its work = PROJECT «Новая идея» steps 1-4); when
the plan is accepted, that node becomes `принято: <spec path>` and the new batch with `план:` opens.
(д) checks only that the `план:` path exists in the working tree (data, P27); whether the plan is good is the critic-on-plan's.

### 1.3 Where a finding stops and a node starts

- A finding (`findings/*.md`, template unchanged) is EVIDENCE and description: what is wrong, the witness, the rules,
  whether the owner's word is needed. It is never work by itself.
- Work exists only as a node row. A node names its finding(s) in «Что»; a node may have no finding when «Что» + a spec
  are enough; one finding may feed several nodes (split by part).
- A finding no node row names is an orphan — (е) red, for every date after migration (§4, (е)).

### 1.4 What a leftover is under the new model

A «Остатки» item = something that came up while working the batch. Legal forms (§2.3): `сделано: <hash | t-nnn>`
(fixed now — the default) or `узел: <node>` whose row says `Откуда: остаток <this batch's node> · <criterion>`.
`перенос:` stops being a form of «Остатки» and of «Живые доказательства» (fork **F4**): what leaves the batch leaves as a
node in the target pile (`live-runs` included: `узел: live-runs/<N>/<id>`).

---

## 2. The leftover problem (core)

### 2.1 Why remarks become rows (the leak, by carrier) — P9, P10, P11

| # | leak | carrier | what it lets happen |
|---|---|---|---|
| L1 | the critic brief routes every out-of-owns analog to «Остатки» | critic-diff-brief q4 | an analog the fix round could fix is born as a node |
| L2 | severity `queue` | critic-diff-brief q7 | a code-quality finding with no reason to wait waits |
| L3 | "a node with an id and an owner" as an equal alternative to a fix | critic-diff-brief q12(d), critic.md rule 19 | the same |
| L4 | `узел:` needs no back-reference and no reason; `перенос:` passes write-time with `подтвердил: —` | `piles.py` `_item_why` | a row is cheaper to write than a fix |
| L5 | `close` reads `подтвердил:` as text, never who typed it | `piles.py` `leftover_problem` | an agent's signature closes the batch |
| L6 | `close` refuses `узел:`, so every node-leftover is rewritten as `перенос:` into another batch | `piles.py:2979-2981` | leftovers migrate into "ostatki/hvosty" batches (P8: 18 of 103) |
| L7 | "Needed from integration" — prose that someone must turn into work | builder-rules п. 1, п. 11 | becomes a node later, with the context lost |
| L8 | "fix now, or EXPLICITLY put the remainder in the queue" | CLAUDE.md rule 9 | the queue is an equal option |
| L9 | the fix round is a fresh worker with the diff and the verdict and the SAME owns | CLAUDE.md rule 12 Cost gates | an out-of-owns remark cannot be fixed in the round |
| L10 | the coordinator's cadence: the critic's queue is "заведена узлами" in one move (P10) | practice; no rule forbids it | the backlog grows by design |

**[depends on t-906]**: the measured share of each road (which of L1-L10 produced how many of the open nodes) decides the
order of streams and may add a road. Until then the table is by carrier, not by volume.

### 2.2 The hard criterion: when a follow-up may be a node at all

DEFAULT: every remark of a critic, a builder's "noticed", an analog in the same artifact or class, is FIXED in the same
node's fix round. The Lead widens the round's `owns` to cover it (the fix-round dispatch is a new writing dispatch; its
manifest carries the widened `owns`; rule 4 overlap is checked as for any dispatch).

A remark may leave the round as a node ONLY with one key of `leftover_criteria` (data, `tools/piles-vocab.json`):

| key | holds when | invariant it protects |
|---|---|---|
| `другая-кучка` | the fix is in another pile's `зона:` AND is another class than the node's (a sibling of the same class is fixed now, rule 9 sweep) | a node's own class never leaves it |
| `слово-владельца` | the fix needs an intent decision (PROJECT 11a) | the agent never decides intent |
| `живой-прогон` | it needs a run on a stand (FR-33) | a proof is never faked by text |
| `занятый-файл` | its file is written by a batch «в работе» of another taker (check (б) would refuse) | two writers never meet in one file unannounced |
| `ждёт-события` | it depends on an event that has not happened (a branch merge, a second reader appearing — e.g. FG7-35) | a conditional node names its condition |

Size is NOT a criterion (fork **F2**): a remark too big for one round is a SECOND fix round of the same node (same node
id, same task id, `attempt` grows only on a `rejected`), not a new node.

Who judges: the critic PROPOSES a node with a key; the Lead ACCEPTS or sends it back to the round (P27, AR-29: code checks
that a key from the list is present; whether it truly holds is the Lead's judgment, a tier above the critic's proposal).
Who confirms a criterion-node on the leftover item: fork **F5**.

### 2.3 Rules (what changes, by leak)

| leak | change | where (§5 has the text) |
|---|---|---|
| L1, L2, L3 | q4: an analog is FIXED in this round (the dispatcher widens owns) unless a `leftover_criteria` key holds; q7 severities: `blocks` / `fix in this round`; `queue` only with a key; q12(d) and critic.md rule 19: "a proposed node" only with a key | critic brief, critic.md |
| L3 (machine) | the verdict JSON gains an optional array `nodes: [{"what": str, "criterion": key, "pile": slug}]`; `critic_verdict_check.py` refuses an item whose `criterion` is not a key of `leftover_criteria` (FR-1: names the list and the door "move it to `fixes`") | `tools/critic_verdict.schema.json`, `tools/critic_verdict_check.py` |
| L4 | write-time (д): an `узел:` item is valid only when the named node's `Откуда` is `остаток <this batch's node id> · <key>` (the back-reference); `перенос:` is no longer a form (F4) | `piles.py` `_item_why` |
| L5, L6 | `close`: an `узел:` item passes when the named node exists in a batch that is not closed and not this one, and carries the back-reference; the `подтвердил:` rule follows F5 | `piles.py` `leftover_problem` / `check_leftovers` |
| L7 | builder-rules п. 1/п. 11: "Needed from integration" lists only what the integrator/Lead applies IN THE SAME ROUND (a placed file, a SKILL.md line); anything else is a remark the critic/Lead handles by §2.2 | builder-rules |
| L8 | rule 9 "queue" = a node with a `leftover_criteria` key | CLAUDE.md rule 9 (one clause) |
| L9 | rule 12: the fix round's worker is fresh, its `owns` = the node's owns + what the verdict's `fixes` name | CLAUDE.md rule 12 (one clause) |
| L10 | the counter + the coordinator's duty (2.4) | `piles.py summary`, `close`; PROJECT п. 9 |

### 2.4 The counter (code counts, the Lead judges)

`piles.py summary` gains a FLOW line, and `close` prints the batch's own flow:

```
поток узлов за 7 дней (по git): открыто N (из остатков M) / закрыто K (принято A, отклонено R); итог +X|-X
поток по пачкам в работе: forge/7 закрыто a, порождено b; …
без типа: T узлов (строки до перехода)
```

- "opened" = the first commit (in the window) in which a row with that `(slug, id)` appears in a node table; "closed" =
  the first commit in which its status word becomes `принято` or `отклонено`; "from leftovers" = opened rows whose
  `Откуда` starts `остаток`; "born of batch X" = rows anywhere whose `Откуда` names a node of X. Source: ONE
  `git log -p --since=<window> -- plans/piles` pass (fork **F3**: git-derived vs a date column).
- `close <slug> <N>` prints `пачка <slug>/<N>: закрыла a, породила b` and, when b > a, refuses unless the batch «Ход»
  carries a line starting `приток:` (`- <дата> — приток: <why, per born node>`) — fork **F6** (refuse-on-absence vs print
  only). The refusal judges PRESENCE of the Lead's explanation (shape), never its content (P27).
- The weekly calibration reads the flow line (check 33 gains one item; `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`, Lead).

What the coordinator does when a batch opens more than it closes: (1) reads each born node against §2.2; a node whose
key does not hold goes back to a fix round of its parent node and the born row becomes `отклонено: возвращён в <parent>`;
(2) writes `приток:` for the rest; (3) a second week with a positive net is a finding for the calibration.

Edges of 2.4 (invariant: *the counter never reports a shrink that did not happen*):
- git cannot run / the window has no commits → the line says `поток узлов: не измерено (<why>)` — never `0` (FR-41/FR-59).
- a row moved between batches (a split) appears "opened" in the new file: keyed by `(slug, id)`, a move inside one pile is
  not an open; a move across piles is (it changes owner pile) — stated in the line's legend.
- a row deleted without a status (hand edit) → counted as `исчезло: N`, never as closed.
- a status moved back (allowed only by hand with a (в) door) → the later forward move counts once.
- rows of closed batches before the cutover → in history, counted only inside the window.

---

## 3. Migration of each registry into nodes (one stream each)

Common rules: a node created by migration has `Откуда: миграция`, a `Тип`, an `Исполнитель`, and lands in the UNTAKEN
batch of its pile (none → `batch-<N+1>-<slug>.md` `ожидает` + card row, PROJECT п. 2). A row judged STALE is not
migrated: its verdict and evidence go in the migration commit message and in the pile's untaken batch «Ход». "Stale" is
judged by the Lead from a scout's evidence (P27): a commit that fixes it, a node already `принято` for it, or the named
file/function gone (with the scout's positive control).

| stream | registry | before | rule for each item | after |
|---|---|---|---|---|
| M1 | findings in no batch (P12) | 152 (t-895; Lead re-measures with `check --all` (е)) | done → finding file deleted (git keeps it; fork **F10**); duplicate of a live node → its name added to that node's «Что» (untaken batch) or to «Ход» (taken batch: old findings are placed by prose, P12); live → node row; unsure → node `Тип` by content, `Исполнитель: scout → Lead` | 0 orphans; then (е) drops `FINDINGS_FROM` (§4) |
| M2 | `docs/tasks/lead-queue-fable.md` | 12 items + 2 lines; 10 done, 2 open (P14) | the 2 open → no new node: FG7-51 and FG7-49 already hold them (P15); a «Ход» line in forge/7 names the queue items they absorb | file retired (fork **F7**, collides with architect-tier F8); a future "below-Lead cannot" item = a node with `Исполнитель: Lead` |
| M3 | `design/factory-rules-debt.md` | header "25"; 44 open by its own words (P17) | a row naming a live node/B-id → gets `node: <slug>/<N>/<id>` (or the B-id) in its «Where» cell; a row naming a closed one → scout checks the code: fixed → moves to "Fixed since this walk"; still broken → node; a row with no owner → node `Тип: долг` in the pile owning its file's zone | every open row carries `node:`; file fate fork **F8** |
| M4 | plans of big ideas with no pile | 6 (t-895; P25 candidates) | live → a batch with `план:` in the topical pile (F11); done/abandoned → one header line in the plan `архив: <дата>, <причина>` and no batch | 0 plans without a batch or an `архив:` line |
| M5 | DAG files under `docs/tasks/` | 3 (P24) | `factory-fixes.md` → `архив:` header line; `test-diet.md` → its open nodes become rows of `package-ci` batch 4 (`dieta-testov`), each checked against that batch's existing rows first (overlap is likely; scout question), the file gets `архив:` + pointer; `onboarding-streams-…` → kept as a WAVE VIEW (it names pile nodes, holds none of its own) with a header line saying so | 0 node tables outside `plans/piles/` |
| M6 | `plans/BACKLOG.md` | open rows: P26 | unchanged archive: (а) keeps "every open B-id placed", (г) keeps the freeze, `close --id` keeps closing a row by the owner's word | unchanged |

The debt file (M3, fate fork F8) — who reads it today is P18. Options:
- (a) **keep, as the package's MAP of known violations** (recommended): it stays where FR text points (`factory-rules.md:230,
  305`), the two package tests keep their single rows (G1-10, K0.15), every open row gains `node: <slug>/<N>/<id>`, the
  header count is corrected; the work lives in the node. PROJECT «Как принимается» п. 4 changes to "a node `Тип: долг`
  + a row in the debt file pointing to it". `piles.py debt_warnings` widens from B-ids to node ids (a closed node →
  WARNING "remove or move the debt row").
- (b) delete: needs a package commit editing `factory-rules.md` (2 lines), `design/README.md`, both tests (G1-10, K0.15 —
  their couplings lose their carrier: AR-22 producer gone while readers stay unless rewritten), `test-layers.json`,
  three code comments, `field-producers.json`, `piles.py`, `docs/SIBLING_MAP.md` rows, `plans/features.json`.
- (c) a stub pointing at the piles: the two tests still need their rows → (c) degenerates into (a) or (b).

---

## 4. `tools/piles.py` after the cleanup

Readers of `piles.py` (Grep `import piles|from piles|piles\.py|piles_split|backlog_tree` over `tools/*.py`, `.githooks/*`,
`.claude/settings.json`, `.github/**` → 42 files, 26 of them tests): `.githooks/commit-msg:14` (`check --msg-file`),
`.github/workflows/forge-check.yml:84` (`check --base`), `.claude/settings.json:156-157,175-176` (allow lines),
`tools/wave.py:208,224` (`status … --set принято`), `tools/backlog_tree.py` (the pane, `load_tree`),
`tools/compact_snapshot.py:350-353` (`load_tree`, `leftovers_unowned`), `tools/forge_metrics.py` (`load_tree`,
`Finding`, `FINDING_NAME_RE`, `_is_pile_dir`), `tools/collect_intake.py` (`load_pile`, `table_after`, `parse_zone`,
`write_bytes_atomic`, `printable`, `_norm_token`), `tools/piles_split.py` (parsers), `tools/canon_clock.py:28`
(`LEFTOVER_EMPTY_WORDS`), `tools/ci_read_common.py:10` (`printable`), `tools/md_table.py`, `tools/conftest.py`,
`tools/hook_liveness_probe.py:942-961,1425` (probe 14), `tools/worktree_sweep.py:7`, `tools/mechanism_gate.py:254`.

| piece | verdict | what changes | readers / effect |
|---|---|---|---|
| `summary` | changes | + flow line (2.4), + `без типа: T`, + `строки долга без node: D` (when F8 = a) | compact snapshot does not read it; calibration check 33 reads it (Lead adds the item) |
| `check` (а) placement | unchanged | B-id placement of the archive (M6) | commit-msg, forge-check |
| (б) overlap | unchanged | — | commit-msg, forge-check; criterion `занятый-файл` names it |
| (в) frozen | unchanged | the new columns are not masked: a taken batch is not migrated (F9) | — |
| (г) backlog | unchanged | — | — |
| (д) form | changes | (1) a node row NEW or CHANGED against the base (the multiset rule of F6-30) carries `Тип` ∈ `node_types` and `Откуда` in a `node_origins` form; a table lacking the columns gets a red only when such a row is added ("add the columns `Тип`, `Откуда` from the template"); (2) `план:` of a batch header names an existing path; (3) the `узел:` back-reference of 2.3 | commit-msg, forge-check, compact snapshot (`leftovers_unowned` keeps its signature) |
| (е) findings | changes after M1 | when the baseline is 0, `FINDINGS_FROM` and the WARN branch are removed: every orphan red (one rule, P31) | commit-msg, forge-check |
| `take` | unchanged | — | integrator |
| `close <slug> <N>` | changes | `узел:` accepted with back-reference (L5/L6); `перенос:` per F4; flow line + `приток:` per F6; `debt_warnings` widened to node ids (F8 = a) | integrator; `worktrees_sweep_line` unchanged |
| `close --id` | unchanged | M6 | — |
| `status` | unchanged | words from the one vocabulary (already) | `wave.py` |
| `board`, `release` | unchanged (refused aliases) | — | `.claude/settings.json` allow lines for `board --check` are stale (P23) → Lead removes them |
| new `node_vocab()` | added | ONE reader of `tools/piles-vocab.json` (`node_types`, `node_origins`, `leftover_criteria`, `intake_default`); a file absent or unreadable → `CannotRun` naming the path (FR-59: never "every type valid") | `piles.py` itself, `collect_intake.py`, `critic_verdict_check.py` (reads the file directly through `piles.node_vocab` — ONE reader, AR-13) |

`tools/piles-vocab.json` joins `MECHANISM_PREFIXES` (data that decides a gate, like `tools/worktree-junk.json`) — Lead.

Checks this spec adds or alters, with owner and class (AR-29 / P27; forge checks, outside the package census, classed in
its words):

| check | owner it serves | class |
|---|---|---|
| (д) `Тип` ∈ list, `Откуда` form, `план:` path exists | data (code) | shape / presence |
| (д)/close `узел:` back-reference | data (code) | xref |
| close `приток:` presence (F6) | judgment (the Lead's explanation; the content is the Lead's, accepted at calibration) | presence |
| `critic_verdict_check` criterion key | data (code) — the route word; the reason after it is the critic's, judged by the Lead | shape (route word, as X7-2's `closed_unresolved_reasons`) |
| §2.2 "does the key hold" | judgment (Lead, a tier above the critic) | not code |
| F5 confirmation of a criterion-node | intent (owner) or judgment (Lead) — per F5 | presence of a signature |

---

## 5. Rule texts that change (exact replacement text)

Order with the parallel spec `docs/tasks/specs/20261116-boot-by-topic-spec.md`: its F2 (b/c) moves «Командная работа»
п. 2, 3, 4, 8, 9 (+ the check line) to `docs/TEAMWORK.md`, numbers staying as pointer lines; п. 11 stays in PROJECT.md.
Overlap = п. 2, 4, 9 (this spec rewrites their content; that spec moves them). Fork **F12** on the order; whichever lands
second applies its edit to the home that exists then (PROJECT.md section or `docs/TEAMWORK.md` § with the same number),
text unchanged. AGENTS.md is regenerated (`python tools/agents_md.py`). The test anchors of P22 stay byte-identical.

**5.1 PROJECT.md «Командная работа» п. 2 — the sentence block from «**Находка сразу попадает в пачку** (D-0044)» to
«…`tools/test_pile_cards_contents.py` красит `forge-check`.»** → replace with:

> **Всё в кучках** (слово владельца 17.11.2026): единственный реестр работы — узлы пачек. Находка — улика и описание, не
> работа: тем же ходом, что файл в `findings/`, она получает УЗЕЛ (строку «Узлы» с `Тип` и `Откуда: находка`) в НЕвзятой
> пачке своей кучки; нет такой — пишущий открывает `batch-<N+1>-<slug>.md` со статусом «ожидает» и строкой в таблице
> «Пачки» карточки. Тем же ходом находка получает строку в «Содержание» карточки (путь, тип, суть, файлы, узел, решение
> владельца, связи) — без неё `tools/test_pile_cards_contents.py` красит `forge-check`. Тип узла — слово из
> `tools/piles-vocab.json` (`баг`, `доделка`, `идея`, `оптимизация`, `долг`, `живой-прогон`, `решение`); большая идея —
> своя пачка с парой `план: <путь>` в шапке.

(The surrounding sentences — the frozen batch, «Находка называет класс фабрики», the `grep` by DECISIONS — unchanged.)

**5.2 PROJECT.md «Командная работа» п. 4** → append one sentence after «…у находки до этого `id: —`.»:

> Очереди вне кучек (очередь Lead, долг правил, графы задач в `docs/tasks/`, планы идей без пачки) не ведутся: их работа —
> узлы (спека `docs/tasks/specs/20261117-everything-in-piles-spec.md`).

**5.3 PROJECT.md «Командная работа» п. 9 — the sentences from «**Остатков в идеале нет вовсе**» to «…Закрытые по тексту
строки помечает Lead, не владелец.»** → replace with:

> **Остатков нет по правилу**: замечание критика, найденный билдером аналог и сосед того же класса чинятся в фикс-раунде
> того же узла — Lead расширяет `owns` раунда. Узлом из работы узла становится только то, у чего есть основание из списка
> `leftover_criteria` (`другая-кучка`, `слово-владельца`, `живой-прогон`, `занятый-файл`, `ждёт-события`); размер —
> не основание: большой фикс — второй раунд того же узла. Такой узел пишется с `Откуда: остаток <узел> · <основание>`,
> строка «Остатков» — `узел: <id>`; основание предлагает критик, решает Lead. `piles.py summary` печатает поток узлов
> (открыто/закрыто за неделю), `close` — сколько пачка закрыла и породила; породила больше — строка `приток:` в «Ходе»
> с причиной по каждому узлу, неделя с плюсом — находка для калибровки.

(«Пачка закрывается доделкой, не переносом» and the live-runs sentence stay; under F4 their `перенос:` wording becomes
`узел: live-runs/<N>/<id>` — text in the build node of stream D.)

**5.4 PROJECT.md «Командная работа» п. 11** → append after «…исполнитель не нужно искать по кучкам.»:

> У узла названы `Тип` и `Откуда`; узел, рождённый работой другого узла, называет его и основание.

**5.5 PROJECT.md «Как принимается изменение пакета» п. 4, last sentence** «Нарушение правила, которое не чинится сейчас, —
строка в `design/factory-rules-debt.md`.» → (F8 = a):

> Нарушение правила, которое не чинится сейчас, — узел `Тип: долг` в кучке, чья зона, и строка в
> `design/factory-rules-debt.md`, которая называет этот узел (`node: <кучка>/<N>/<id>`).

(F8 = b: «— узел `Тип: долг` в кучке, чья зона.»)

**5.6 CLAUDE.md rule 4a, first sentence** «…is tracked as a markdown DAG — a pile's batch file or a file under docs/tasks/:
nodes/statuses/tiers as the carrier;» → «…is tracked as nodes of a pile's batch file (the only registry of work, the
owner's word 17.11.2026): nodes/statuses/tiers as the carrier; a file under docs/tasks/ may group pile nodes into waves
but holds no node of its own;»

**5.7 CLAUDE.md rule 9, the clause** «fix now, or EXPLICITLY put the remainder in the queue/log» → «fix now, or EXPLICITLY
open a node for the remainder with a `leftover_criteria` key (PROJECT.md «Командная работа» п. 9)».

**5.8 CLAUDE.md rule 12 Cost gates, the clause** «a fix round runs in a FRESH worker carrying only the diff and the
verdict» → «a fix round runs in a FRESH worker carrying only the diff and the verdict, its `owns` = the node's owns plus
what the verdict's `fixes` name».

**5.9 docs/tasks/critic-diff-brief.md q4, second sentence** («An analog outside the node's `owns` that this round does not
fix comes back as a line …») → «An analog — inside or outside the node's `owns` — is a FIX of this round (the dispatcher
widens the round's owns); it leaves the round only as an item of the verdict's `nodes` array with a key of
`leftover_criteria` in `tools/piles-vocab.json` (`другая-кучка`, `слово-владельца`, `живой-прогон`, `занятый-файл`,
`ждёт-события`) and one line why; the Lead decides whether the key holds. Size is not a key.»
**q7, last sentence** «Each is a finding with a severity — blocks / fix before merge / queue — …» → «Each is a finding with
a severity — blocks / fix in this round — never a style pass and never "I don't like it"; "queue" exists only as a `nodes`
item with a key (q4).»
**q12(d)** «a fix in this round or a node with an id and an owner» → «a fix in this round, or a `nodes` item with a key (q4)».

**5.10 .claude/agents/critic.md rule 19, last sentence** «…as a fix of this round or as a proposed node with its owner…» →
«…as a fix of this round or as a `nodes` item of the verdict with a `leftover_criteria` key (critic-diff-brief q4)…»; rule 5
«Axes … left uncovered and not queued» → «… left uncovered and neither fixed nor proposed as a `nodes` item with a key».
(Mechanism path: Lead places.)

**5.11 plans/builder-rules.md п. 1**, the clause «нужное в чужом файле — не правь, опиши в «Needed from integration» (файл,
точный текст/код, зачем)» → «нужное в чужом файле — не правь, опиши в «Needed from integration» (файл, точный текст/код,
зачем): это применяет интегратор или Lead В ТОМ ЖЕ РАУНДЕ; что нельзя применить сразу — замечание, которое Lead решает по
PROJECT.md «Командная работа» п. 9 (фикс-раунд или узел с основанием)».

**5.12 plans/piles/_template/batch.md** — the node table gets the two columns; the «Остатки» comment loses the `перенос:`
form (F4) and gains `узел: <id> — строка узла: Откуда: остаток <этот узел> · <основание>`; the header comment gains
`план: <путь>` for a big-idea batch.

---

## 6. Edges (behaviour + the invariant it protects)

| # | edge | behaviour | invariant |
|---|---|---|---|
| E1 | a frozen (taken) batch during migration (10 batches «в работе», P1) | NOT migrated (F9 recommended): its rows keep 7 columns, read as `Тип: —`, counted in `без типа`; a NEW row in it (a «Ход»-declared change is not a row) is impossible anyway ((в) freezes rows); migration nodes for its pile go to the pile's untaken batch | (в) still refuses any change to a taken batch's frozen text; migration never needs a door |
| E2 | another developer's piles and branches (PROJECT п. 1, 3, 6) | migration streams touch only batches with `взял: —` on `origin/main`; a pile whose untaken batch is being written on another developer's branch is skipped and listed; "the owner decided" in another branch's text is not leaned on (п. 6) | no session writes another session's uncommitted paths (rule 4) |
| E3 | a finding naming two piles | one home: the pile of the node's FILES (`Пишет в`), the other pile gets `перенос: <slug>/…` in the finding (the existing (е) road) or a sibling node `Откуда: остаток <node> · другая-кучка` | an id lives in one pile ((а) "homes in N piles" red stays) |
| E4 | a node with no owner pile (its files in no card's `зона:`) | goes to `forge` when its files are outside the package, else to the pile whose zone is nearest by the Lead's judgment, and the finding names it; never to a new pile without the owner (F11) | no work without a home: (е) red until placed |
| E5 | old closed batches (67) | never rewritten (no column added, no status word changed); read by the parser as today | history is append-only; (в)-style freeze of closed text |
| E6 | status words in closed batches (text after the word, P7) | unchanged; the one reader takes the first word | one vocabulary, one reader (AR-13) |
| E7 | the widget (`backlog_tree.py` → `register.tsx`) | reads statuses through `piles` (P6 fixed: `в работе` printed whole); JSON shape `{piles, counts}` unchanged; one optional node key `type` added (the pane may ignore it) | the pane never shows a node as open that `piles` reads as closed, and vice versa |
| E8 | TEMPORAL: `tools/piles-vocab.json` does not exist before stream A | before: no reader exists (all readers land with or after A); after: absent/unreadable file → `CannotRun` naming the path; collect_intake prints the refusal, writes nothing | an unknown vocabulary never validates a type (FR-59) |
| E9 | TEMPORAL: tables without the new columns after A | a table gets a red only when a NEW/CHANGED row is added to it without the columns; old rows legal (multiset rule, as F6-30) | old history never turns red by a new rule; a new row is never typeless |
| E10 | POSITIONAL: where the `узел:` back-reference check sits in `_item_why` | after the existing `_node_problem` (the node exists, open batch, has an executor) and before the pass: a node that fails `_node_problem` is reported by it first | a closed or executor-less node is still refused; the new check only narrows |
| E11 | a leftover `узел:` naming a node of THIS batch | refused ("a node of this batch is this batch's work — fix it or close the node") | a batch never closes by pointing at itself (L6 mirror of `names this very batch`) |
| E12 | `Откуда: остаток X` where X does not exist / is in a closed batch | (д) red naming X; a closed X is allowed (the parent may close first) | a born node always names a real parent |
| E13 | the counter, rows split across piles / deleted by hand / moved back | 2.4 edges | the counter never shows a shrink that did not happen |
| E14 | a critic verdict with a `nodes` item whose key is not in the list, or no `nodes` array | unknown key → `critic_verdict_check` exit non-zero, text names the list and the door "move it to `fixes`"; no array → valid (nothing proposed) | a proposed node always carries a key; absence never fakes one |
| E15 | input from outside: the vocabulary file is data a person edits | adversarial rows in the test table: empty list, duplicate word, a word with `|`, a non-string, BOM, a 1000-word list, a missing key → each a `CannotRun` or a named red, never a silent accept | FR-1/FR-2: every refusal names what it expected and the door |
| E16 | the `приток:` gate (F6) when git cannot measure the flow | no refusal; close prints `поток не измерен (<why>)` | an unknown never blocks and never passes as `0` |
| E17 | a debt row (F8 = a) naming a node that `close` just closed | `debt_warnings` WARNING with file:line, as today for B-ids | a closed node never stays the owner of an open debt row silently |
| E18 | conflicting requirements: §2.2 "fix now" vs PROJECT п. 3 (two batches «в работе» on one file) | the overlap rule wins: the remark becomes a node with `занятый-файл` | two writers never meet in one file |
| E19 | conflicting requirements: §3 M2 retires the Lead-queue file vs architect-tier F8 keeps two queue files | not decided here — fork F7; both streams wait for the Lead's answer | one road for "work below-Lead cannot do" (P31) |

Reused function in a more consequential role: `_node_problem` (today: advice that a node exists) becomes part of the
`close` gate (L5/L6). Allowed error direction: it may REFUSE a valid item (false red, door: `сделано:` or fix the row),
never PASS an invalid one. Adversarial inputs that must stay refused: `узел:` naming a node of this batch; a node in a
closed batch; a node with `Исполнитель: —`; `узел: forge/7/FG7-1 extra text`; a node id that exists in two batches of the
pile, one closed (the open one must carry the back-reference); a back-reference naming another node of the same id in
another pile.

---

## 7. Phases, streams, witnesses, readers

### 7.1 Phases

- **Phase 0 (owner/Lead)**: answers to the forks marked OWNER; the t-906 digest attached; critic on this plan (PROJECT
  «Как принимается» п. 6 — the meaning of «Остатки», a carry-over and a gate changes).
- **Phase 1 (code, one wave)**: stream A, then B and C in parallel after A's merge (they import `node_vocab`).
- **Phase 2 (rules + migration, parallel by disjoint files)**: D (rules), E1…En (M1 per pile group), F (M3), G (M2, M4, M5,
  forge pile's own orphans).
- **Phase 3 (close-out)**: H — (е) `FINDINGS_FROM` removed after M1 = 0; settings.json stale allow lines; calibration
  check 33 item; `MECHANISM_PREFIXES` entry (Lead).

### 7.2 Streams (owns disjoint; each node gets its own task_id and designer-threshold judgement)

| stream | node | owns (absolute) | witness (DoD command) | tier / commit |
|---|---|---|---|---|
| A | `piles.py`: columns, `node_vocab`, (д) new-row checks, `план:`, `узел:` back-ref (write + close), F4/F5/F6 per answers, flow counter in `summary`/`close`, `debt_warnings` node ids, template | `C:/QAFactory/forge-repo/tools/piles.py` `C:/QAFactory/forge-repo/tools/piles-vocab.json` `C:/QAFactory/forge-repo/tools/piles_testkit.py` `C:/QAFactory/forge-repo/tools/test_piles_form.py` `C:/QAFactory/forge-repo/tools/test_piles_close_gate.py` `C:/QAFactory/forge-repo/tools/test_piles.py` `C:/QAFactory/forge-repo/plans/piles/_template/batch.md` | `python -m pytest tools/test_piles_form.py tools/test_piles_close_gate.py tools/test_piles.py -q` (outside the package: `scenario_walk.py --witness-for` has no row, so the DoD names the test files, CLAUDE.md rule 4) | designer → builder → critic; builder STAGES, Lead commits (mechanism path) |
| B | readers: the pane reads statuses through `piles` (+`type`); collect_intake writes `Тип` (`intake_default`) and `Откуда: находка` | `C:/QAFactory/forge-repo/tools/backlog_tree.py` `C:/QAFactory/forge-repo/tools/test_backlog_tree.py` `C:/QAFactory/forge-repo/tools/collect_intake.py` `C:/QAFactory/forge-repo/tools/test_collect_intake.py` | `python -m pytest tools/test_backlog_tree.py tools/test_collect_intake.py -q` | builder → critic (topic critic with A, R13-g) |
| C | critic verdict: `nodes` array + key check; brief q4/q7/q12(d) text | `C:/QAFactory/forge-repo/tools/critic_verdict.schema.json` `C:/QAFactory/forge-repo/tools/critic_verdict_check.py` `C:/QAFactory/forge-repo/tools/test_critic_verdict_check.py` `C:/QAFactory/forge-repo/docs/tasks/critic-diff-brief.md` | `python -m pytest tools/test_critic_verdict_check.py tools/tests/test_role_carriers_one_owner.py tools/test_handoff_rule_anchors.py -q` | builder → critic; critic.md (5.10) handed as text, Lead places |
| D | rule texts 5.1-5.8, 5.11 (+5.10 from C), AGENTS.md regenerated | `C:/QAFactory/forge-repo/PROJECT.md` `C:/QAFactory/forge-repo/plans/builder-rules.md` (+ `CLAUDE.md` handed as text) | doc-dispatch witness (CLAUDE.md rule 11): key-presence script over the replacement sentences quoted verbatim from §5, full source attached, one negative control; plus `python tools/agents_md.py --check` | builder; CLAUDE.md/critic.md — Lead |
| E-k | M1 orphans, one pile group per node (groups by the (е) WARN list; forge excluded) | `C:/QAFactory/forge-repo/plans/piles/<slug>/` of the group's piles (untaken batches, cards, findings) | `python -B tools/piles.py check --all` — the (е) line for the group's piles: 0 orphans; (д) green | scout (evidence) → Lead (judges stale) → builder (rows) |
| F | M3 debt file | `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules-debt.md` + node rows in the untaken batches of the piles F names (disjoint from E: F's rows land after E-k of that pile, `очередь:` line) | `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/design/factory-rules-debt.md` (prints the files that judge it: G1-10's and K0.15's tests) | builder; package commit: `architecture: AR-22, AR-14 -- …`, `judgment: none -- …` |
| G | M2, M4, M5 + forge's own orphans | `C:/QAFactory/forge-repo/docs/tasks/lead-queue-fable.md` `C:/QAFactory/forge-repo/docs/tasks/factory-fixes.md` `C:/QAFactory/forge-repo/docs/tasks/test-diet.md` `C:/QAFactory/forge-repo/docs/tasks/onboarding-streams-2026-11-12.md` the six plan files (P25) `C:/QAFactory/forge-repo/plans/piles/forge/` `C:/QAFactory/forge-repo/plans/piles/package-ci/` | `python -B tools/piles.py check --all` (forge, package-ci: (д), (е) green) + doc key-presence for the `архив:` lines | builder; Lead judges stale |
| H | (е) single rule; settings.json allow lines; check 33; `MECHANISM_PREFIXES` | `C:/QAFactory/forge-repo/tools/piles.py` `C:/QAFactory/forge-repo/tools/test_piles_findings.py` (+ Lead: `.claude/settings.json`, `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`, `tools/mechanism_gate.py`) | `python -m pytest tools/test_piles_findings.py -q` | builder; Lead |

Every new test case is a ROW in the existing test file named in the stream's owns (docs/TESTING.md: no new test file);
the adversarial battery of E15 is one parametrised table in `tools/test_piles_form.py`.

### 7.3 Readers of every touched file (designer rule 3)

Commands (Grep tool, the repo minus `.claude/worktrees/`): `piles\.py|import piles|from piles` over `tools/`,
`.githooks/`, `.claude/settings.json`, `.github/` → 42 files; `factory-rules-debt` over the repo → 54 files (code/test/rule
lines in P18); `lead-queue-fable` → 4 files; `backlog_tree` → 17 files (code: `tools/claude-mods/backlog/hooks/register.tsx`,
`tools/test_backlog_tree.py`, `tools/piles.py` docstring); `collect_intake` over `tools/` → 3 files; `critic_verdict` over
`tools/` → 9 files, `.claude/agents/` → 1; `critic-diff-brief|builder-rules` over `tools/*.{py,json}` → anchors of P22 +
`test_quarantine.py:51` (carrier list), `test_dispatch_manifest.py:844` (fixture).

| touched file | other readers | verdict |
|---|---|---|
| `tools/piles.py` | the 42 of §4 | `load_tree`/`parse_*`/`leftovers_unowned`/`printable`/`write_bytes_atomic`/`LEFTOVER_EMPTY_WORDS` signatures unchanged; `wave.py`, `compact_snapshot.py`, `forge_metrics.py`, `piles_split.py`, `canon_clock.py`, `ci_read_common.py`, `md_table.py`, `hook_liveness_probe.py` (probe 14: still "refuses a broken tree"; no new probe → the two count pins 482/1015 unchanged): unchanged; `backlog_tree.py`, `collect_intake.py`: change in stream B; `critic_verdict_check.py`: changes in C |
| `tools/piles-vocab.json` (new) | none before A; after: `piles.node_vocab` (one reader), through it `collect_intake.py` (B), `critic_verdict_check.py` (C); `mechanism_gate.py` list (H) | created in A |
| `tools/backlog_tree.py` | `register.tsx` (reads `piles[].batches[].nodes[].status`, `counts`), `test_backlog_tree.py` | JSON shape unchanged (+ optional `type`): register.tsx unchanged |
| `tools/collect_intake.py` | `test_collect_intake.py` | changes in B |
| `tools/critic_verdict_check.py`, schema | `.claude/agents/critic.md` (names the schema), `test_critic_verdict_check.py`, `install_parity_anchors.json`, `dup-baseline.json`, `md_regions.py`, `escape_check.py`, `test_p4_stdin_deadline.py` | additive field: the readers unchanged; `dup-baseline.json` re-read by the clone ratchet at canon |
| `docs/tasks/critic-diff-brief.md` | anchors P22 (`test_role_carriers_one_owner.py`, `install_parity_anchors.json`, `test_handoff_rule_anchors.py`), `.claude/agents/critic.md`, CLAUDE.md rule 3 | anchors kept byte-identical: unchanged readers |
| `PROJECT.md` | imported by CLAUDE.md; `AGENTS.md` (generated); `test_role_carriers_one_owner.py` pointer strings; boot-by-topic spec (moves п. 2,4,9) | AGENTS.md regenerated in D; pointer strings untouched; boot-by-topic: order F12 |
| `plans/builder-rules.md` | anchors P22 (7b), `test_quarantine.py:51`, `test_dispatch_manifest.py:844` | п. 1 edited only; 7b untouched: unchanged |
| `CLAUDE.md` (4a, 9, 12 clauses) | `AGENTS.md`, `install_parity_anchors.json` (critic-brief pointer, untouched) | Lead |
| `ai-packages/qa-factory/design/factory-rules-debt.md` | P18 list | F8 = a: G1-10 and K0.15 rows kept (one FR-21 row, one FR-23/FR-5 row, same needles) → tests unchanged; `piles.py debt_warnings` changes in A |
| `plans/piles/_template/batch.md` | `tools/test_pile_cards_contents.py` (the heading test runs on the template, FG7-17), `piles.py` `batch_heading_problems` | headings `## Бриф`/`## Узлы` kept: unchanged |
| `docs/tasks/lead-queue-fable.md` | P16 (no code); architect-tier spec §4.4 | F7 |
| `.claude/settings.json` (allow lines) | `hook_liveness_probe.py`, `test_workflows.py` (they parse hooks, not allow lines — Lead verifies when placing) | H, Lead |

### 7.4 AR-n (package part = stream F only; the forge part touches the forge's own AR-13/AR-14/AR-15 analogs)

- AR-22 (every field read has a producer): the debt rows read by G1-10/K0.15 keep their producer — change check: grep both
  tests' needles in the file after the edit (positive control: K0.15's own control row).
- AR-14 (one artifact, one writer): the debt file's writer stays the Lead/builder of the package; nodes are written by the
  pile road only.
- AR-13 (one reader): node statuses and the vocabulary are read only through `piles` (the pane's copy removed).
- AR-15 (one survivor): «Остатки» and «Живые доказательства» keep ONE reader of their forms (`leftover_problem` family).
- AR-29: the checks of §4 table are data checks; every judgment (stale? key holds? `приток:` content) stays with the Lead.

Four questions (CLAUDE.md rule 10) for the commit of A/C/D carry the axis block; the draft names the likely axes for the
Lead: axis 1 (rule texts that change together: PROJECT п. 9 ↔ critic brief q4 ↔ critic.md rule 19 ↔ builder-rules п. 1),
axis 4 (debt ↔ backlog/nodes), axis 18 (none raised), axis 34 (one road: one table, one leftover form). The full
enumeration is the committer's (it needs the current map).

---

## F. Forks (options, consequences, recommendation; OWNER = only the owner decides)

- **F1 (OWNER) — the `Тип` words.** (a) the seven of 1.1; (b) the owner's five only (баг, доделка, идея, оптимизация, долг) —
  live proofs and decision nodes then need another type or a column; (c) add `чистка` (duplication/refactor) apart from
  `долг`. Recommend (a): `живой-прогон` keeps the `live-runs` pile honest, `решение` names the FG7-12/FG7-24 class.
- **F2 (OWNER) — is size a criterion?** (a) no: a big remark is a second fix round of the same node (recommended — the
  owner's complaint is exactly "context must be gathered again"); (b) yes, `объём` above N lines of diff — cheaper rounds,
  the backlog keeps growing.
- **F3 — the counter's data source.** (a) git history, no date column (recommended: past weeks are measured at once; no
  column to forget); (b) an `Открыт` date column written by the author (exact for hand moves, one more cell to police);
  cost of (a): one `git log -p` over `plans/piles` per run (time NOT MEASURED — the builder measures and states it).
- **F4 — `перенос:` retired from «Остатки» and «Живые доказательства».** (a) yes, every carry is `узел:` (recommended: one
  road, P31; `перенос: findings/<file>` is the road that made orphans); (b) keep `перенос:` for live proofs only — two forms
  for one action.
- **F5 (OWNER) — who confirms a criterion-node on the leftover item.** (a) the owner (`подтвердил: владелец, <дата>`) — the
  strongest brake, waits for her; (b) the owner or the batch's Lead (PROJECT п. 6 already signs decisions "Lead пачки,
  дата") — recommended; the flow counter shows the volume either way; (c) the Lead's `accepted` event only, no signature in
  the file. Today's rule (п. 9 «перенос подтверждает человек») changes under (b)/(c): her word is needed for that.
- **F6 — batch opened more than it closed.** (a) `close` refuses without a `приток:` line (recommended: a presence check,
  informed pass FR-4); (b) print only, the calibration reads it.
- **F7 (OWNER/Lead) — the Lead queue vs architect-tier F8.** (a) retire the file; "below-Lead cannot" and Architect
  questions are nodes with `Исполнитель: Lead` / `Architect`; the architect-tier SessionStart count reads nodes through
  `piles` (recommended, one registry); (b) the architect-tier's two files, outside piles — contradicts «всё в кучках»;
  (c) the files stay as VIEWS listing node ids only. Both specs wait for this answer (E19).
- **F8 (OWNER) — the debt file.** (a) keep as the package's map with `node:` pointers (recommended: FR text and two package
  tests read it; work moves to nodes, the file stops being a registry); (b) delete (a package change of ~12 files, two
  tests rewritten); (c) stub — degenerates into (a) or (b).
- **F9 — taken batches.** (a) not migrated, read as `Тип: —` (recommended: no doors); (b) migrated with one
  `piles-skip: в -- t-907 migration` per batch.
- **F10 (OWNER) — finding files whose work is done.** (a) M1 deletes the done orphans only; finding files of closed nodes
  stay (out of scope, recommended); (b) delete every finding of a closed node at `close` (1110 → far fewer; changes `close`).
- **F11 — a big idea's home.** (a) a batch in the topical pile, a new pile only when no zone fits (recommended); (b) a pile
  per idea.
- **F12 (Lead) — order with boot-by-topic.** (a) boot-by-topic lands first (it moves text verbatim), this spec's D edits
  `docs/TEAMWORK.md`; (b) this spec first, boot-by-topic moves the new text. Recommend: whichever is accepted first lands
  first; D's node names both homes.

## Small choices closed by the designer

- Statuses stay code constants (each word has a code writer: take/close/status) — one reader, `backlog_tree` imports them;
  the types/origins/criteria are data.
- Data file `tools/piles-vocab.json`, keys `node_types`, `node_origins`, `leftover_criteria`, `intake_default` (= `баг`);
  ASCII keys, Russian words as values with a `means` line each.
- Old rows without `Тип` are counted, never red.
- Flow windows: 7 days and per batch in work; ISO dates.
- `Откуда` separator ` · ` (U+00B7) — one char, not `|` (cell-safe).
- `collect_intake` writes `Откуда: находка`.

## Noticed, not widened (analogs and contradictions)

- The debt file's header count ("25") contradicts its own tables (P17).
- `.claude/settings.json` allow lines for the retired `board --check` (P23).
- `backlog_tree.py` prints the first token of a status (`в` for `в работе`) (P6).
- PROJECT п. 9 says «Закрытые по тексту строки помечает Lead» while `close` cannot tell a person's `подтвердил:` from an
  agent's — the gap L5.
- The card «Содержание» column `тип` (строка/находка) is the CARRIER kind, not the work type — keep the names apart in the
  template (stream A's template edit can rename it «вид»; not in owns — Lead's call).

## Reading trail

`plans/piles/forge/README.md:1-80`; `plans/piles/forge/batch-7-vhodyashchie-4.md` (whole); `plans/piles/_template/batch.md`,
`finding.md` (whole); `tools/piles.py:1-162, 195-354, 560-720, 960-1030, 1096-1230, 1777-2045, 2121-2270, 2600-3020,
3125-3465` + Grep of its defs/constants; `tools/backlog_tree.py` (whole); `tools/collect_intake.py:955-1014`;
`tools/critic_verdict.schema.json` (whole); `tools/mechanism_gate.py:205-284`;
`ai-packages/qa-factory/design/factory-rules-debt.md` (whole); `docs/tasks/lead-queue-fable.md` (whole);
`docs/tasks/critic-diff-brief.md` (whole); `.claude/agents/critic.md:20-39, 160-174`; `plans/builder-rules.md:8, 77-88` +
headings; `ai-packages/qa-factory/scripts/tests/test_s1_s2_contract.py:312-331`, `test_null_outcomes.py:582-596`,
`test-layers.json:3400-3419`; `docs/tasks/specs/20261116-architect-tier-spec.md:285-324` + Grep; boot-by-topic spec Grep
`TEAMWORK|Командная работа`; `docs/tasks/factory-fixes.md`, `onboarding-streams-2026-11-12.md`, `test-diet.md` (first 15
lines each); `AGENTS.md:1-12, 229-232`; `logs/journal/dev1.jsonl` Grep `t-895`. Greps (Grep tool, case-sensitive unless
noted; positive controls named in P4/P7): batch headers/statuses (P1), node table headers (P2), waiting rows (P4), odd
status words (P7), `factory-rules-debt` (54 files), `lead-queue-fable` (4), `backlog_tree` (17), `collect_intake` (3),
`critic_verdict` (9 + 1), piles readers (42), `"(ожидает|в работе|принято|отклонено|закрыта)"` over non-test `tools/`.
Not measured (no shell): P12 count, P13, P25 list, P26, git-log cost of F3. Needed beyond the manifest: the files of the
trail outside `given:` (all read-only).

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
