# t-903 — plan review: FG7-51 «the boot by topic» (spec `docs/tasks/specs/20261116-boot-by-topic-spec.md`, with the Lead decisions)

critic (opus) | task t-903 | node forge/7/FG7-51 | feature F19 | 17.11.2026 | plan gate (new idea of the owner, mandatory)

**Verdict: go with fixes.** The direction holds, the topic map (§2) is sound, and the item-level inventory (§3) has a row for
every numbered item. BUT five blocking findings must be fixed in the spec before any stream is dispatched. Three of them are
places where the plan, as written, would silently drop live clauses, which breaks INV-M (д). One is a Lead decision that cannot
be executed as the streams are cut. One is a move that breaks the plan's own §5.1 criterion. No finding calls for rework of the
approach.

Acceptance of this verdict, and every fork change proposed below, belongs to the Lead (and to the owner for F2/F3). This review
proposes and decides nothing.

---

## 1. Premise re-check (empirics first)

All commands were run against the root checkout. `main` = `origin/main` = 0d6f61b1 (`git -C … log --oneline -1 origin/main`).

| # | Premise | Command | Output | Holds? |
|---|---|---|---|---|
| Q1 | Budget = BOOT.md `Read X.md` + CLAUDE.md + `@` imports, one level | `sed -n 1036,1070p; 1145,1170p tools/session_context.py`; `grep -n "Read [A-Z_]*\.md" BOOT.md` | regex `Read ([A-Z_]+\.md)`; docstring «one level, no recursion into the imported files»; BOOT.md:14,15,27 → SYSTEM_PROMPT, DECISIONS, CURRENT_CONTEXT | holds |
| Q2 | WARN 108000, BREACH 120000, CLAUDE_WARN 47800 | `sed -n 185,215p tools/session_context.py` | `BOOT_WARN_THRESHOLD = 108000`, `BOOT_BREACH_THRESHOLD = 120000`, `CLAUDE_WARN = 47800` | holds |
| Q3 | 123942 B, per-file split | `echo '{}' \| python -B tools/session_context.py \| grep BOOT`; `wc -c` | `BOOT BUDGET: 123942 bytes / 120000 (4 files + 3 imports) BREACH … CLAUDE.md: 43476/47800 incl. imports 113985`; CLAUDE 43476, PROJECT 62252, FR 5575, AR 2682, DECISIONS 7547, CURRENT_CONTEXT 1783, SYSTEM_PROMPT 627 (sum 123942) | holds (now measured) |
| Q4 | agents_md expands recursively, MAX_DEPTH 5 | `sed -n 25,40p; 65,82p tools/agents_md.py` | `MAX_DEPTH = 5`, `IMPORT_RE = ^@(\S+)$`, `_expand(repo, path, chain, out)` recursive | holds |
| Q5 | Import pin | `sed -n 1183,1190p tools/test_session_context.py` | `== ["PROJECT.md", "docs/FACTORY_RULES_INDEX.md", "docs/ARCHITECTURE_INDEX.md"]` | holds |
| Q9/Q10 | One-owner test: OWNER_KEYS, POINTERS, exclusions; `cost:queue` owned by PROJECT.md | `sed -n 20,80p tools/tests/test_role_carriers_one_owner.py` | 13 OWNER_KEYS incl. `("cost:queue","PROJECT.md","в работе всегда шесть пишущих билдеров")`; 20 POINTERS incl. PROJECT→`plans/builder-rules.md` п. 7b and →critic-diff-brief; EXCLUDED holds `plans/piles/`, `docs/tasks/specs/`, AGENTS.md | holds |
| Q11 | Parity anchors quote CLAUDE.md; CI `--check` | python over `install_parity_anchors.json`; `python -B tools/install_parity.py --check`; `sed -n 85,96p forge-check.yml` | 46 units; `routing-policy` 89 anchors; `MISSING (0) … exit 0`; CI steps present. No unit has `host_path` PROJECT.md or builder-rules | holds |
| Q11' | Routing-log anchors that S1 says move | python: anchors whose line in CLAUDE.md is 272-349 | 272 «Routing log — …», 285 «ACCOMPLISHED FACTS,», 299 «ISO local time», 325 «DEAD-WORKER REPLACEMENT:» | under F5=a NONE of them moves (299 is C-RL2, 325 is SHAPES): see finding m4 |
| Q13 | Mechanism net excludes PROJECT.md | `sed -n 211,265p tools/mechanism_gate.py` | the tuple holds CLAUDE.md, DECISIONS.md, SIBLING_MAP, PROCESS/, agents, skills, BOOT.md, … `tools/factory_rules_index.py`; no PROJECT.md | holds |
| Q18 | Architect spec not on disk | `ls docs/tasks/specs/20261116-architect-tier-spec.md` | file exists (untracked) | **does NOT hold** (stale): see finding m7 |
| Q19 | builder-rules carries pre-FG7-50 text | `grep -n "5 минут\|до минуты\|FR-1…FR-5\|английском" plans/builder-rules.md`; `git merge-base --is-ancestor 263809e8 main` | FG7-50 is merged (`merged`); :12 reads FR-1…FR-59, :10 is the fixed language text, :37-38 «критерий — список, а не длительность; … до минуты каждый» | **does NOT hold**: the builder-rules part of FG7-50 has landed, and R2 is half-landed. FG7-50's Lead part (CLAUDE.md rule 12 «six is the target», the D-0046 line in rule 6) has NOT landed: `grep -n "at most 6\|D-0046" CLAUDE.md` → :261 «at most 6 parallel WRITING» and no D-0046 line |
| — | Two index generators already exist | `head -30 tools/architecture_index.py`; `grep index .githooks/pre-commit forge-check.yml` | `architecture_index.py` is a separate tool with `MAX_BYTES = 3072`; pre-commit :27, :31 and CI :78, :79 each run one tool | relevant to S4's «one road» claim (m5) |
| — | journal `feature` is enforced? | `grep -n feature tools/journal_write.py` | optional on every event; `jv.feature_warnings` echoes a WARN at write time (:512) | WARN only (m3) |

---

## 2. BLOCKERS

**B1 — §3.2 row PT12 and §3.3 R1: «text replaced by the owner's 16.11 wording» drops live clauses of п. 12.**
- What is wrong: PT12 replaces the whole item. R1's wording covers only the cap: target 6, «not fewer», a 7th when needed,
  «not at the cost of efficiency». Live п. 12 carries more than that (PROJECT.md:353-360):
  - «дизайнеры, критики и скауты в счёт не идут и слота не ждут»;
  - «ограничение владельца … действует на одну сессию … лимиты откатываются в понедельник вечером (владелец, 16.11.2026)»;
  - «Волны слияния CI не ждут: принятое сливается в `main` через `tools/wave.py merge`, красный CI чинит там один билдер»;
  - «седьмого … дверью `budget-skip:`» (the door's name);
  - «Тем же ходом, что слияние: статусы узлов в пачках обновлены, слитые ветки и папки деревьев убраны».
  Only «Критик кода — один на тему» has a destination (K4 → rule 3). The others have none.
- Evidence: `sed -n 353,367p PROJECT.md` (quoted above); spec :219, :234.
- Fix: R1 replaces ONLY the cap sentences: «в работе всегда шесть … меньше шести — только по слову владельца …» and «Шесть —
  не потолок: седьмого … когда надо (упал мерж)». Every other sentence of п. 12 is K1 (stays verbatim). Add one row per kept
  clause to §3.2 so the diff critic can count them. Re-quote OWNER_KEYS `cost:queue` (E19) as planned.

**B2 — §3.2 row PT13: the K4 claim «7b holds every clause, incl. … «CI не запускает и не ждёт» after FG7-50» is false.**
- What is wrong: FG7-50 is merged, so the text on disk is the post-FG7-50 text, and `plans/builder-rules.md` 7b does NOT hold:
  - (a) «пайплайн `main` читают только интегратор волны и билдер, чинящий красный `main`» — absent;
  - (b) «Диспатч, который просит билдера запустить CI, ждать пайплайн или гонять мутации, — дефект координатора» — absent. 7b:54
    holds only the narrower «Диспатч, требующий большего локально, — дефект координатора»;
  - (c) «CI не запускает и не ждёт» (CI, not slow files) — 7b says «не гоняет и не ждёт» only for slow files and the canon. The
    line «CI is neither started nor waited for» lives in `.claude/agents/builder.md:52`, which itself points BACK to 7b for it.
  Turning п. 13 into a pointer would delete (a) and (b) and leave (c) as a pointer loop.
  Clause (b) is also a DISPATCHER duty. By the spec's own home rule (§2, «the home is the file of the party that EXECUTES the
  duty») its home is the coordinator's boot (CLAUDE.md rule 11 or п. 13 itself), never builder-rules.
- Evidence: `sed -n 28,58p plans/builder-rules.md`; `git -C … grep -n "дефект координатора" -- CLAUDE.md PROJECT.md plans/builder-rules.md .claude/agents docs/RUNBOOK.md docs/TESTING.md`
  → PROJECT.md:201, PROJECT.md:365, builder-rules:54 (the narrower clause), CLAUDE.md:230 (a different clause); `sed -n 48,56p .claude/agents/builder.md`.
- Fix:
  - S3 adds (a) and (c) to 7b verbatim (K2 from п. 13). The 7b anchor and OWNER_KEYS `scope:builder` are kept.
  - Clause (b) stays in the boot. Recommended: п. 13 keeps its number with «правило: 7b» PLUS the one coordinator sentence (b),
    which is allowed by the checker-keeps-one-sentence rule of §2.
  - §3.2 PT13 lists the clauses one by one with a destination each.

**B3 — §3.2 row PA2: one clause of «Как принимается» п. 2 has no destination.**
- What is wrong: «цикл ожидания в диспатче — один на раунд, с капом, и только на то, что нельзя прочитать иначе (вопрос
  драйвера; пайплайн — только интегратору, «Командная работа» п. 13)» (PROJECT.md:195-197) is not listed in PA2, and no home
  holds it. The only RUNBOOK hit for «цикл ожидания» (:383) is a different rule (a dead-worker loop). PA2 also covers some
  clauses only implicitly:
  - «Голый пуш ветки ничего не запускает» — held by RUNBOOK:90 «пуш ветки без PR ничего не запускает», but not named in PA2;
  - «Канон всегда на CI … не больше часа» — RUNBOOK holds it; not named.
- Evidence: `grep -l -- "цикл ожидания" plans/builder-rules.md docs/RUNBOOK.md docs/TESTING.md docs/tasks/critic-diff-brief.md PROJECT.md CLAUDE.md`
  → RUNBOOK.md, PROJECT.md only; `grep -n "цикл ожидания" docs/RUNBOOK.md` → :383 «Фоновый цикл ожидания … если воркер … умер».
- Fix: give PA2 a full clause list. Each sentence of п. 2 gets K2 (destination), K4 (the home line that holds it) or K1 (stays).
  The wait-loop clause is a coordinator/dispatch duty, so it moves K2 into RUNBOOK §7 next to «Прогнать ветку», or stays in
  PROJECT. Never K4.

**B4 — Lead decisions, last paragraph: «the streams that only add headings and the contents do not wait» cannot be executed as
the streams are cut, and would deepen the BREACH.**
- What is wrong:
  - No stream in §7.2 only adds headings and contents. S2 bundles the F3 move (waits for the owner) with the PROJECT TOC and
    headings. S1 holds the CLAUDE headings and TOC, but §7.1 orders S1 last, after S2 and after the architect spec's Stream L.
    That spec's Stream L runs «after A-F are accepted» (architect spec :549).
  - A TOC written before F2/F3 must be rewritten afterwards: its cells would name homes that the moves later change.
  - Bytes: headings + TOCs (+5.8 KB est., §4.2) + the §6 rule (+1.7 KB measured, see §5 below) landing before the moves take
    the boot from 123942 to about 131 KB.
- Fix: replace the paragraph with one that matches the streams:
  - **S3 and S4 may run now.** S3 adds no boot bytes. S4 is inert under its TEMPORAL edge.
  - **S2 and S1 wait** for the owner's word on F2/F3 and, for S1, for the architect spec.
  - The PROJECT TOC and headings land in the same commit as the moves.

**B5 — F2=b (Lead: «executable on the recommendation») moves whole items under a clause-level criterion. Parts of п. 2, 3, 9 are
discipline with no gate, so the move breaks §5.1 (i).**
- What is wrong: §5.1 (i) says a text leaves the boot only if a gate refuses its violation and names the door. These clauses
  have no such gate:
  - п. 2: «Находка называет класс фабрики, не правило одного проекта (P2) … в брифах — ссылки … Перед «что сделать» — `grep`
    по `DECISIONS.md` и `docs/DECISIONS_ARCHIVE.md`». No `piles.py` check judges this; it is judgment.
  - п. 3: «поздний узел сливает `main` в своё дерево и решает конфликт сам (пины обеих сторон зелёные), критик у него один —
    после слияния; зависимость по замыслу спеки остаётся последовательной. Пачки одного разработчика друг друга не держат». A
    coordinator's decision; check (б) sees only zones.
  - п. 9: «Остатков в идеале нет вовсе: минорные замечания критика … чинятся тут же — фикс-раундом того же узла; замечания,
    относящиеся к другим кучкам, сначала анализируются …», «Закрытые по тексту строки помечает Lead», «Живые прогоны не держат
    пачку вообще … (владелец, 11.11.2026)». `close` refuses only a bare row or a carry without a human's confirmation. It cannot
    refuse the choice to carry instead of fix.
  These are exactly the «policy that isn't auto-loaded gets silently skipped» case that the spec itself cites (boot-diet step 6).
- Evidence: `sed -n 289,341p PROJECT.md` (byte ranges below); spec §5.1 :288-292, F2 :516-521.
- Fix: in F2=b, split at clause level. The gated mechanics of п. 2/3/4/8/9 go to TEAMWORK.md (D-0044 finding-into-batch, the
  «Содержание» row, the frozen-batch edit list, the hot-file list and `очередь:`, the BACKLOG freeze, doors, `close` refusal
  forms). The discipline sentences quoted above stay in the boot under their item numbers. Cost: about 1.5 KB of the 7.2 KB
  saving (est.). Mark the split in §3.2 per clause. This also has to be put to the owner (F2 is her question): «the gated
  mechanics», not «items 2, 3, 4, 8, 9».

---

## 3. Minor findings (fix in the same spec round; none blocks alone)

- **m1 — §3.3 / F9: F9 is not a contradiction, so not an owner question.** PROJECT п. 2 «только по слову владельца и никогда не
  параллельно с другим» (authority + exclusivity) and RUNBOOK:115-116 «только когда CI недоступен или красный по причине
  раннера» (condition) are compatible. Placing both sentences verbatim side by side in RUNBOOK §7 (plain K2) IS option (a)
  without rewording. Fix: drop F9 as a fork and make it a plain K2 row. If a joint rewording is wanted after all, it becomes a K5
  row R5 in §3.3 (K5 is «the four contradictions and nothing else»), with its carrier. Evidence: `sed -n 113,118p docs/RUNBOOK.md`; `sed -n 203,210p PROJECT.md`.
- **m2 — §3.2 P-rows / F3=a / S4: the index form is undefined for long first sentences, and the byte estimate is low.**
  - Measured first sentences (python split at `[.!?]\s` over PROJECT.md:41-174): 31 lines ≈ **6485 B**, not 4.5 KB. P19's first
    sentence is **1049 B** (the whole five-step ladder); P16's is 406 B.
  - A `### P<n>` heading of 1 KB breaks §6 item 2 of the same spec. Converting the first sentence into a heading also turns K2
    («byte-identical») into a reformat.
  - Fix: keep the bullets verbatim in `docs/OWNER_PRINCIPLES.md` (`- **P<n>.** …`, a true K2). S4 derives the line from the
    bullet opener with a byte cap per line and per file (the AR generator's pattern: `MAX_BYTES = 3072`, refusal over the cap).
    The cap and its cut rule are stated in S4's edges.
- **m3 — §3.1 C-RL3 / F5=a: the move carries the daily `feature: Fnn` duty out of the boot** (the typed-fields paragraph,
  CLAUDE.md:303-307). On the path there is only a WARN at write time (`journal_write.py:512`), not a refusal, so §5.1 (i) holds
  only weakly. It saves 2.0 KB measured (not 3.5), and costs a new file, F6 (a mechanism-net row) and S1 work. See §8: F5 is
  dispensable; the budget closes without it.
- **m4 — §7.2 S1: the parity unit `routing-journal-doc` is unnecessary under F5=a.** Every Routing-log anchor (CLAUDE.md:272,
  285, 299, 325) stays. «ISO local time» is C-RL2 (stays), not moved text. Fix: create the unit only if F5=b.
- **m5 — §7.2 S4 «one road for generated indexes (P31, AR-15)» is not true on disk.** `tools/architecture_index.py` is a second,
  separate generator (own cap, own pre-commit/CI lines). Folding the P index into the FR tool leaves two roads. Fix: say so
  honestly and queue the AR fold as a node, or make the data table generic enough to take AR later. Also, S4's «one `--check`
  line» in pre-commit and CI is not needed if the same tool checks both rows: drop `.githooks/pre-commit` and
  `forge-check.yml` from S4's owns. They are Lead-placed mechanism paths, which is one fewer Lead step.
- **m6 — §7.5 readers: section-name citations outside `tools/` and `.claude/` are not walked.** Spot checks:
  - `docs/RUNBOOK.md:232` «Правило о сжатии … — `PROJECT.md`, «Прогоны и эксперименты»». Goes stale when PR7 moves to
    § Сессия форджа; not listed (S2 owns RUNBOOK).
  - `docs/SIBLING_MAP.md:33` (axis row) names «PROJECT.md «Командная работа» п. 13 and `plans/builder-rules.md` 7b» as the rule
    text. Stale after PT13.
  - `docs/SIBLING_MAP.md:308` says a grammar change updates «PROJECT.md «Командная работа» item 3» in the same commit. Must
    name `docs/TEAMWORK.md` § 3 under F2=b.
  - `plans/builder-rules.md:38` and `:40-41` cite PROJECT п. 2 and п. 13 as the SOURCE of 7b clauses. Once those become
    pointers to 7b, this is a pointer loop; cite the owner's word dates instead.
  - Kept, as planned: `tools/piles.py:2183` («п. 2», 2 hops), `critic.md:165` / `designer.md:87` («PROJECT.md P31»),
    calibration checks 39 (п. 9) and 42/47 (п. 6).
  - Evidence: `git -C … grep -n -i -E "PROJECT(\.md)?[^\n]{0,40}(Командная работа|Релиз|Принципы владельца|Прогоны и эксперименты|Как принимается)" -- PROCESS docs/SIBLING_MAP.md DECISIONS.md tools .claude BOOT.md SYSTEM_PROMPT.md DELEGATION_TABLE.md docs/RUNBOOK.md docs/TESTING.md`.
  - Fix: add §7.5 rows for `docs/`, `PROCESS/`, `plans/builder-rules.md` citing PROJECT section names. Give the RUNBOOK:232 and
    builder-rules edits to S2/S3. Add the SIBLING_MAP:33/308 edits to the Lead-placed list of S2.
- **m7 — §0 Q18 and Q19 are stale (see table); §5 omits the architect spec's bytes.** That spec adds an architect line to «Tiers»
  and a new D entry to DECISIONS.md (in the boot). Fix: refresh Q18/Q19. Record that FG7-50's CLAUDE.md part (rule 12 cap
  wording, D-0046 line in rule 6) has not landed, so C6/C12b do not describe the live text. Re-measure after the architect spec
  merges (Phase 0).
- **m8 — §6 (the writing-form rule), rule 10 fit: no registered detector, nothing on the path.**
  - Item 1 «Пересказ правила вне дома — дефект» is caught only for the 13 OWNER_KEYS. Item 2 (~40 lines, > 50 a finding) has a
    detector only in FG7-52, which is П2 and not in this node.
  - F12=a puts the rule in PROJECT.md, outside the mechanism-gate net (Q13), so no axis block is forced.
  - Fix: S2's commit carries the four-question block for §6. Register a calibration check (or extend check 33) that samples
    the boot for retellings and for headings over 50 lines. State «on discipline until FG7-52» explicitly. Same for TOC
    completeness: a new topic added later without a TOC row has no detector; POINTERS rows check only existing cells.
- **m9 — §6 item 2 / E14, the «~40 lines» split: one guard to add.** Sub-headings inside a numbered item (C2b, C4b, C11b-e) split a
  list item mid-way, and a reader who follows «rule 2» to «### Rule 2 — …» may stop at the next heading. The C11d «(below)»
  reference stays inside its block, which is fine. Fix: add to §6 item 2 «a sub-heading goes only at a paragraph boundary,
  never between a condition and its consequence; a sub-heading inside a numbered rule repeats the rule number («Rule 2 ·
  …»)». The spec's style already does the second part; make it the rule.
- **m10 — §7.4 DOC-DISPATCH keys.** The 60-character first/last keys break on re-wrap and re-indent: a PROJECT continuation
  indented 3 spaces moving into a new file, a bullet turned into a heading. Fix: compare whitespace-squashed text, the way
  `test_role_carriers_one_owner.squash` does. Say so in §7.4.
- **m11 — the node's batch row.** `plans/piles/forge/batch-7-vhodyashchie-4.md:74` «Пишет в» lists 7 paths. The streams own
  about 18 (RUNBOOK, TESTING, the 4 new docs, both tests, `factory_rules_index.py` + test, `mechanism_gate.py` + test).
  `:75` FG7-52 still says `tools/pointer_lint.py`, though the Lead accepted A1. The batch is «ожидает», so the row can be
  edited: fix both before dispatch so `piles.py check` (б) sees the real zone.
- **m12 — R1 carrier (F10).** The cited snapshot line is a Lead paraphrase: `docs/tasks/compact-snapshots/2026-11-17-0040-narrative.md:39`
  «Шесть пишущих (дословно по смыслу) …». The fuller quoted wording in §3.3 comes from the t-894 brief. Fix: name the brief (or
  the session line) as the carrier of the exact words. Per PROJECT п. 6, the snapshot paraphrase alone is not the owner's text.
- **m13 — §3.2 count line says «6 bullets of «Прогоны»»; there are 7** (PR1-PR7; `grep -n "^- " PROJECT.md` lines 258-274).
  Cosmetic, but the diff critic counts rows by this line.

---

## 4. The 15-clause meaning check (picked from the live files, not from the spec's list)

| # | Clause (live) | Live location | Inventory row → destination | Verdict |
|---|---|---|---|---|
| 1 | Rule 11 edge behavior incl. (i) TEMPORAL, (ii) POSITIONAL | CLAUDE.md rule 11 (:187-) | C11a, stays K1 | ok |
| 2 | Rule 11 adversarial mini-battery for input from OUTSIDE | CLAUDE.md rule 11 «Which tests» | C11b, stays | ok |
| 3 | Rule 11 DOC-DISPATCH WITNESS (i)-(iii) + five-point checklist | CLAUDE.md rule 11 | C11d, stays | ok |
| 4 | R11-h: critic/designer report path on `handoff:` | CLAUDE.md R11 table | C11e, stays | ok |
| 5 | Rule 4 SCOPE OF THE WITNESS RUN, BATCH CANON appended to the last `accepted` | CLAUDE.md rule 4 | C4b, stays | ok |
| 6 | Rule 8 SMALL-WORK BATCHING + «from the SECOND … self-execution is a violation» | CLAUDE.md rule 8 | C8, stays | ok |
| 7 | Hygiene pt. 6: content search needs a same-shape positive control; registry STATUS read through; table a/b/c | CLAUDE.md :420-440 | C-H6, stays | ok |
| 8 | Hygiene pt. 7 probe rollback by byte copy (a)-(d) | CLAUDE.md :442- | C-H7, stays | ok |
| 9 | Routing log: every new event carries `feature: Fnn` | CLAUDE.md :303-307 | C-RL3 → `docs/JOURNAL.md` | row present; weakening (m3) |
| 10 | КР п. 2: finding names the factory class (P2); grep DECISIONS before «what to do» | PROJECT.md :289-302 | PT2 → TEAMWORK.md (F2=b) | row present; breaks §5.1 (i) (**B5**) |
| 11 | КР п. 9: no residuals, minor critic remarks fixed by a fix round; live runs never hold a batch | PROJECT.md :326-341 | PT9 → TEAMWORK.md | row present; breaks §5.1 (i) (**B5**) |
| 12 | КР п. 12: merge waves don't wait CI; statuses and worktrees cleaned in the same move; limits reset Monday; scouts/critics not counted | PROJECT.md :353-360 | PT12 «text replaced by R1» | **MISSING** destination (**B1**) |
| 13 | КР п. 13: dispatch asking CI/wait/mutations = coordinator defect; who reads the `main` pipeline | PROJECT.md :361-366 | PT13 K4 «7b holds every clause» | **MISSING**: 7b does not hold it (**B2**) |
| 14 | «Как принимается» п. 2: one wait loop per round, with a cap, only for what can't be read otherwise | PROJECT.md :195-197 | PA2 — not listed | **MISSING** (**B3**) |
| 15 | Owner-away paragraph (no blocking questions; irreversible/outgoing waits) | PROJECT.md «Что решать самому» | PD, stays | ok |
| 16 | P5 «LLM-агент — не источник данных для чтения» (2nd sentence) | PROJECT.md P5 | P-row → OWNER_PRINCIPLES; index line = 1st sentence only | ok: the AR-6 index line keeps it in the boot |
| 17 | P22 «Сначала разбирается сам — всегда и везде» (2nd paragraph) | PROJECT.md P22 | P-row | ok: the FR-48 index line keeps it |
| 18 | P26 analyst resolves every suspicious unconfirmed place | PROJECT.md P26 | P-row; nothing in the boot | acceptable: read by package work (§5.3) |
| 19 | «Прогоны»: compaction never stops work (~300K line) | PROJECT.md :274 | PR7 → § Сессия форджа (+TR1) | ok; the citation RUNBOOK:232 goes stale (m6) |

Item-level completeness: every numbered rule and item of both files has a §3 row (checked against `grep -n "^## \|^[0-9]*\. \*\*"
PROJECT.md` and the CLAUDE.md headings). The defects are all below item level, in the rows that move or replace PART of an item.
That is where the diff critic should count clause by clause.

---

## 5. Budget arithmetic (measured removals; additions est.)

Measured with `sed -n A,Bp FILE | wc -c`:

| Block | Lines | Bytes |
|---|---|---|
| P1-P31 | PROJECT.md 41-174 | **22318** (spec est. 19.8 K) |
| P index, first sentences | python, see m2 | **6485** (spec est. 4.5 K) |
| «Командная работа» whole | 279-370 | 14986 |
| п. 2 / 3 / 4 / 8 / 9 / check line | 289-302 / 303-308 / 309-311 / 325 / 326-341 / 368-370 | 2334 / 996 / 436 / 360 / 2889 / 221 = 7236 |
| п. 13 | 361-367 | 1058 |
| «Как принимается» п. 2 | 187-210 | 3820 |
| «Релиз» | 371-380 | 1807 |
| Routing log C-RL3 (identity sentence + typed-fields paragraph) | CLAUDE.md 294-296 part + 303-320 | ≈ 276 + 1893 → ≈ 2.1 K (spec est. 3.5 K) |
| SHAPES table | 321-333 | 1681 |
| §6 writing rule text (lands in the boot under F12=a) | spec 335-344 | 1673 (missing from §5.2) |

Scenarios, starting from 123942 (pointer lines estimated at about 150-480 B each, TOC + headings +5.8 K as in §4.2):

| Scenario | Arithmetic | Result | vs 120000 / 108000 |
|---|---|---|---|
| Lead's decisions (F2=b, F3=a, F5=a, F7=a) + §6 | −15.4 (P: −22.3 + 6.5 + 0.4) −7.3 (F2=b + п. 13) −3.3 (п. 2) −1.7 (Релиз) −2.0 (JOURNAL) +5.8 +1.7 | **≈ 101.7 K** | under both |
| same, with the B5 split (discipline stays) | +1.5 | ≈ 103.2 K | under both |
| same, without F5/F6 (see §8) | +2.0 | ≈ 105.2 K | under both |
| F3 refused (F3=c), F2=b | 101.7 + 15.4 + 0.3 | ≈ 117.4 K | under BREACH, over WARN |
| F2 refused (F2=a), F3=a | 101.7 + 7.3 | ≈ 109.0 K | under BREACH, just over WARN |
| **both refused (F2=a, F3=c)** | 101.7 + 15.4 + 7.3 + 0.3 | **≈ 124.7 K** | **over BREACH**, worse than today |
| headings/TOC/§6 first, before any move (B4) | 123.9 + 7.5 | ≈ 131.4 K | over BREACH |

Under the Lead's decisions the target ≤ 120000 is reached with about 18 K to spare, and ≤ 108000 is reached too. Under the
fallback where the owner refuses BOTH F2 and F3, the plan does NOT reach the budget: TOC + headings + §6 add more than the
unforked moves remove. The spec must say what then: e.g. a ≤ 3 KB cap on the TOC, §6 in boot-diet (F12=c), and F7/PA2/F5
together. Its §5.2 table lacks this row. CLAUDE.md alone stays under its own WARN (about 43.5 + 4.0 − 2.0 ≈ 45.5 K + the
architect additions, est.).

---

## 6. Forks where the Lead's decision should change

- **F5 (a) → (c), nothing moves; F6 then not needed.** 2.0 K measured, a daily duty under a WARN only (m3), plus a new file, a
  net row and a parity unit. The budget closes without it (§5).
- **F9 → not a fork** (m1): plain K2. The owner question can be dropped.
- **F2 (b) → (b') clause-level split** (B5), and put to the owner in those words.
- **F3 (a) stays**, with the m2 corrections: verbatim bullets, a capped generated line, an honest «two roads» note (m5).
- **The executability paragraph** → B4's form (S3/S4 now; S2/S1 after the owner and the architect spec).
- F1, F4, F7, F8, F11, F12, F14, F16: agree. F12 (a) needs the m8 detector line.

---

## 7. Streams (§7) — owns, order, half-landing, witness, regeneration

- Owns overlap: S2 and S1 share `CLAUDE.md`, `tools/tests/test_role_carriers_one_owner.py` and `AGENTS.md`. They are sequential
  (S2 → S1), so this is acceptable. S3 and S4 are disjoint from each other and from S2/S1, except that S3 points into RUNBOOK
  §7, which S2 owns.
- Half-landing windows:
  - After S3 and before S2, builder-rules has R2 («no minutes number») while PROJECT п. 2 still says «до минуты каждый». That is
    two texts for one rule for the length of a phase. Acceptable only if S2 follows directly; better: S3 also leaves PROJECT п. 2
    untouched AND 7b keeps the line until S2 lands, i.e. R2 lands in S2's commit.
  - B2's clause (a) must land in 7b (S3) BEFORE S2 turns п. 13 into a pointer. The order S3 → S2 already gives this, provided
    S3's DoD lists the clause.
- Same-commit duties: E7 (create the file + remove the text + pointers in one commit) and the P import + pin row in one commit
  are correct. `AGENTS.md` is regenerated per stream (§7.3). The P index is generated in S2's commit, and S4's TEMPORAL edge is
  stated for both worlds. Good.
- Narrow witnesses per stream: named, and each runs the one-owner test, parity check and agents_md check. For S2, add
  `python -B tools/architecture_index.py --check` only if S4 folds AR (m5); otherwise fine.
- Order with the architect spec: the Lead's order (architect first) is right for S1, which touches «Tiers»/«Role ≠ tier». But
  it delays S1 until the architect spec's Stream L, which follows its A-F. S2 does not depend on it except for the one import
  line in CLAUDE.md, which is allowed to land in S2.

---

## 8. What the plan does not need (cheapest plan keeping (а)-(д) and the budget)

1. F5/F6/`docs/JOURNAL.md`/the parity unit `routing-journal-doc`/the mechanism_gate row: drop (−1 file, −1 net row, −1 unit;
   the budget still closes at ≈ 105 K).
2. S4's edits to `.githooks/pre-commit` and `forge-check.yml`: drop (the same tool `--check` covers the new row).
3. F9 as an owner question: drop (m1).
4. §4.3's FG7-52 contract, beyond what POINTERS rows already check: keep as a note, not as part of this node's DoD.
What remains: S3, S4 (lean), S2, S1 (CLAUDE headings + TOC only).

---

## 9. Standing lines

- **DUPLICATION AND CONSISTENCY:** one planned duplication, the generated P index repeating first sentences. This is the
  accepted FR/AR pattern, but it needs a cap (m2). Found inconsistencies: two index generators against the «one road» claim
  (m5), and pointer loops 7b ↔ PROJECT п. 2/п. 13 (m6). Grepped: `дефект координатора`, `цикл ожидания`, PROJECT section-name
  citations across PROCESS/docs/tools/.claude.
- **CODE QUALITY:** plan gate, no code. The S4 design (a data table of sources in one tool) is reasonable once the cap is added.
- **ONE ROAD (brief item 12, P31):** the P index road is honest only with m5's note. No exclusion of a language/project/case
  found.
- **TESTS:** the plan adds rows to existing tables (POINTERS, the FR index test) and no new test file. Within docs/TESTING.md's
  rule. Not measured with `tools/test_volume.py` (no diff exists).
- **Class completeness (SIBLING_MAP):** axis 31 (role-text carriers) is handled for the new files by the Lead-placed rows. The
  existing axis rows SIBLING_MAP:33 and :308 that name moving PROJECT items are not handled (m6).

## 10. What I did not check

- The full CLAUDE.md/PROJECT.md K1 rows clause by clause beyond the 19 above. The diff critic must count the K2/K3/K4 rows
  clause by clause.
- The content of the architect spec beyond its §6 file table and Stream L.
- `tools/test_workflows.py` pins of forge-check steps (relevant only if S4 keeps its CI edit).
- Whether agent files expand `@` (F11 (a) avoids the question).
- The rendering of headings inserted inside list items (cosmetic).
- Every byte figure marked est.: pointer-line sizes, TOC rows, the architect spec's additions.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 PT12/R1: replacing the whole item 12 with the owner's 16.11 cap wording drops five live clauses (scouts/critics not counted, Monday reset, merge waves do not wait for CI, budget-skip door, statuses/worktrees cleaned in the merge move); R1 must replace only the cap sentences",
    "B2 PT13: the K4 claim that builder-rules 7b holds every clause of item 13 is false on disk (FG7-50 merged): the main-pipeline readers clause and the coordinator-defect clause for dispatches asking CI/wait/mutations are absent; the latter is a dispatcher duty that stays in the boot",
    "B3 PA2: the clause about one wait loop per round with a cap (PROJECT.md 195-197) has no destination and no home holds it",
    "B4 Lead decisions: the claim that heading/contents streams do not wait is not executable as the streams are cut (S2 bundles F3 with the PROJECT TOC, S1 is ordered last), and landing headings/TOC/section-6 first takes the boot to about 131 KB",
    "B5 F2=b moves whole items 2, 3, 9 of Komandnaya rabota, whose discipline clauses (finding names the factory class, late node resolves conflicts, no residuals by fix round, live runs never hold a batch) have no gate, against the plan's own criterion 5.1 (i)"
  ],
  "class_completeness": "Class: a moved or replaced item loses the clauses that are not in the claimed home. Walked across every row that moves PART of an item (PT2, PT3, PT9, PT12, PT13, PA2, C-RL3): defects in PT12, PT13, PA2 (missing), PT2/PT3/PT9 (criterion broken), C-RL3 (WARN-only weakening). SIBLING_MAP axis 31 is covered for the new files; existing axis rows SIBLING_MAP:33 and :308 that name moving PROJECT items are not covered (m6); the RUNBOOK:232 and builder-rules:38/40-41 citations are not listed.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261116-boot-by-topic-spec.md (whole)",
      "plans/piles/forge/findings/20261116-but-odna-tema-v-mnogih-mestah-kopii-pravil-ustareli.md",
      "CLAUDE.md, PROJECT.md (as loaded; ranges re-read by sed)",
      "tools/session_context.py:185-215,1036-1070,1145-1170",
      "tools/agents_md.py:25-40,65-82",
      "tools/test_session_context.py:1183-1190",
      "tools/tests/test_role_carriers_one_owner.py:20-80",
      "tools/install_parity_anchors.json (routing-policy unit)",
      "tools/mechanism_gate.py:211-265",
      "tools/factory_rules_index.py:1-60",
      "tools/architecture_index.py:1-30",
      "tools/journal_write.py feature lines",
      "plans/builder-rules.md:28-58",
      ".claude/agents/builder.md:48-56",
      "docs/RUNBOOK.md:90,113-118,232,383",
      "docs/SIBLING_MAP.md:33,308,531",
      "PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:992,1095,1101,1111",
      "docs/tasks/specs/20261116-architect-tier-spec.md headings, file table, Stream L",
      "docs/tasks/compact-snapshots/2026-11-17-0040-narrative.md:39-44",
      "plans/piles/forge/batch-7-vhodyashchie-4.md:1-12,73-75"
    ],
    "reruns": [
      {"command": "echo '{}' | python -B tools/session_context.py | grep BOOT", "result": "BOOT BUDGET: 123942 bytes / 120000 (4 files + 3 imports) BREACH; CLAUDE.md 43476/47800 incl. imports 113985"},
      {"command": "python -B tools/install_parity.py --check", "result": "MISSING (0), UNKNOWN (0), exit 0"},
      {"command": "wc -c on PROJECT.md line ranges 41-174, 187-210, 289-341, 353-370, 371-380", "result": "22318; 3820; items 2/3/4/8/9/check 7236; item 13 1058; release 1807"},
      {"command": "python first-sentence index over P1-P31", "result": "31 lines, 6485 bytes; P19 first sentence 1049 bytes"},
      {"command": "git merge-base --is-ancestor 263809e8 main", "result": "merged (FG7-50 landed)"},
      {"command": "git grep 'дефект координатора' over boot, role and worker docs", "result": "PROJECT.md:201, PROJECT.md:365, builder-rules:54 (narrower clause), CLAUDE.md:230 (other clause); not in 7b"},
      {"command": "grep -l 'цикл ожидания' over worker docs", "result": "RUNBOOK.md (line 383, a different rule), PROJECT.md only"}
    ]
  },
  "fixes": [
    "B1: scope R1 to the cap sentences of item 12; every other sentence K1 with its own inventory row",
    "B2: add the main-pipeline readers clause and the CI-not-started clause to 7b (S3); keep the coordinator-defect sentence in the boot under item 13; list item 13 clause by clause",
    "B3: give PA2 a complete clause list; the wait-loop clause moves K2 to RUNBOOK section 7 or stays",
    "B4: rewrite the executability paragraph: S3 and S4 now; S2 and S1 after the owner's word on F2/F3 (S1 also after the architect spec); TOC and headings land with the moves",
    "B5: split F2=b at clause level: gated mechanics to TEAMWORK.md, discipline sentences stay in the boot; put that wording to the owner",
    "m1: drop F9 as a fork, plain K2 of both sentences into RUNBOOK section 7",
    "m2: keep P bullets verbatim in OWNER_PRINCIPLES.md; S4 derives a capped line per principle and caps the file",
    "m3/m4: drop F5, F6, docs/JOURNAL.md and the routing-journal-doc unit",
    "m5: state that the AR index stays a second road or queue its fold; drop S4's pre-commit and CI edits",
    "m6: add section-name readers outside tools to 7.5 and fix RUNBOOK:232, builder-rules:38/40-41, SIBLING_MAP:33/308",
    "m7: refresh Q18/Q19; note FG7-50's CLAUDE.md part not landed; re-measure after the architect spec",
    "m8: four-question block and a registered calibration detector for the section-6 rule and TOC completeness",
    "m9: section-6 item 2: sub-headings only at paragraph boundaries, inside a rule repeating its number",
    "m10: whitespace-squashed key comparison in 7.4",
    "m11: update batch-7 rows FG7-51 (writes) and FG7-52 (no pointer_lint.py)",
    "m12: name the t-894 brief or the session line as the R1 carrier",
    "m13: correct the 'Progony' bullet count to 7",
    "add the both-refused budget scenario (about 124.7 K, over BREACH) to 5.2 with its fallback"
  ]
}
```
