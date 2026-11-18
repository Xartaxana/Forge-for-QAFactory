# Spec t-1489 — backlog rules in one home: `docs/TEAMWORK.md` (DRAFT r1, designer)

SIZE (designer rule 8): estimate, not measured (no shell) — about 60 KB on disk (360 lines, 46 of them over 200
characters, Cyrillic quotes count two bytes), over the 40,000-byte cap; the Lead measures with
`python -B -c "import os,sys;print(os.path.getsize(sys.argv[1]))" docs/tasks/specs/20261118-backlog-rules-one-home-spec.md`.
`decomposable:` (1) HOME — TEAMWORK.md, PROJECT.md, the three templates, test_role_carriers_one_owner.py, AGENTS.md
and the Lead-placed texts (§4, §5 rows for those files, §6 keys K-1..K-20, K-22, K-23, test rows 1-2); (2) SATELLITE
POINTERS — the 32 cards, RUNBOOK.md, README.md (§5 rows for those files, K-21, E4, E5, E10, E12), after (1). The owns
are disjoint; a fix round can split this file into two drafts without trimming edges, readers, forks or the trail.

Feature F19. Owner's word 18.11.2026 (brief `facts:`): «collect all backlog rules in one place, docs/TEAMWORK.md, other
places keep links»; rules to write there: no node without a batch; a batch is taken and frozen against other users; the
same user may go on taking nodes from the batch they froze; and the existing rules; «one priority per batch» is already
written (`plans/piles/_template/batch.md:8`, e0b70f7c — the commit id is the Lead's fact, not re-measured).

## 1. Frame

- Goal: every backlog rule (how a finding becomes a node, nodes live in batches, batches are taken, frozen, closed,
  prioritised) has its TEXT in `docs/TEAMWORK.md`; every old place keeps ONE pointer line. Meaning is kept byte-level:
  a moved span changes only by the reference substitutions listed per span (§4).
- Package: the spec touches no file under `ai-packages/qa-factory/` -> no AR-n invariant touched; `variety: none -- no
  package change`. No check is added or altered by the builder card (the code questions are forks F3, F4).
- Boot: PROJECT.md shrinks (rules leave it), CLAUDE.md is untouched (it holds no backlog rule: case-insensitive grep
  `pile|пачк|кучк|findings|BACKLOG|backlog` over CLAUDE.md = 0 hits; control, same tool and flags, `quarantine|пакет` = 10).
  `coordinator_rules.COORDINATOR_FILES` (tools/coordinator_rules.py:28-34) does NOT list `docs/TEAMWORK.md` today: after
  the move the full rule texts are read on topic, not at boot — fork F9.
- Class (COORDINATOR rule 9): one owner per aspect, SIBLING_MAP axis 31 (`docs/SIBLING_MAP.md:476-495`): its TEAMWORK row
  says «the gated clauses of «Командная работа» п. 2, 3, 4, 8, 9»; after this spec TEAMWORK owns ALL backlog rules — the
  row and the owner sentence :479 change (Lead places, mechanism path).

## 2. What the code holds (the owner-named rules checked against `tools/piles.py`)

| question | what the code does (carrier) |
|---|---|
| who took a batch | KNOWN: `cmd_take` writes `взял: <who>, <date>` and `ветка:` into the batch header and the card row (piles.py:2545-2549); `dev_of` reads a developer slug from it (piles.py:1506-1514), used by (б) and `take` so that batches of ONE developer do not block each other (piles.py:2499-2503) |
| a second taker | REFUSED: «a batch has one taker; to hand it over, the integrator edits взял … (commit with "piles-skip: в -- handover")» (piles.py:2536-2538); same taker + same branch = no-op (2533-2535) |
| what «frozen» freezes | (в) compares a batch taken ON origin/main (status `в работе`/`сдано`/`принято`, piles.py:1590) with its origin text: masked = the whole «Ход» and «Остатки» sections, the Статус cells of the node and evidence tables, the header's статус/MR/issue; `очередь:` lines may only be added (`_frozen_lines`, 1645-1678). EVERY other line differing is red: «a taken batch changes only its Ход, Остатки, the Статус cells, queue lines (added) and the header's статус/MR/issue» (1699-1702). So NEW NODE ROWS are refused, and so is any edit of a node's «Что»/«Пишет в» cell. Card row: only Статус and MR (`_compare_card`, CARD_FROZEN_COLS 1592: Что, Строки, Размер, Взял, Ветка frozen) |
| frozen against WHOM | EVERYONE: neither (в) nor `cmd_status` (3332-3363) reads who commits; the taker is frozen too, and the open parts (Ход, Остатки, Статус cells) are open to any committer |
| the taker taking more nodes | `take` takes the whole batch (no per-node take); a node's status moves by `status <slug> <N> <node> --set "в работе"|сдано|принято|отклонено` — no who check; a new node row in a taken batch is red for the taker as for anyone (door `piles-skip: в`) |
| no node without a batch | (а) `_placement_all_placed`: an open id in no batch row and no finding is red (only after the freeze lock, 1217-1223); (е) `check_findings`: a finding dated >= 2026-10-13 named in no ROW of a batch of its pile is red, older = one WARN line (2182-2218); (д) `_coverage_reds`: every card-row id in the «Что» of exactly one node. (е) counts a row of ANY batch of the pile, closed ones included (`pile_prose` 2113-2119) |
| one priority per batch | NO check: `NODE_COLS` (609) does not read the node «Приоритет» column; `backlog_tree.py:42` groups by the batch header pair only |
| priority fallback | the template says «без пары берётся приоритет карточки» (batch.md:7); `backlog_tree.py:42` reads `b.header.get("приоритет")` only — a batch without the pair shows `""` and is counted under «—»; the card priority (`parse_card` 487, 505) is never consulted. Measured: 100 of 107 batch files carry the pair (Grep count, `^кучка:.*приоритет:` vs `^кучка:` over `plans/piles/**/batch-*.md`, closed batches included) |

## 3. Every backlog rule found (carrier:line, target, code)

Targets are sections of the new TEAMWORK (§4). «stays» = not a backlog rule or held by another owner; reason given.

| id | rule (short) | carrier:line | restatements | target | code that holds it |
|---|---|---|---|---|---|
| R1 | a finding = file in `findings/` + row in an untaken batch | PROJECT.md:116 | RUNBOOK.md:229, :237, :372, :388; session-retro SKILL.md:68; README.md:68-69 | § Бэклог и находки | (е), (д) |
| R2 | «бэклог» = the batch pane; «отметь в бэклоге» = node statuses via `piles.py status`, not BACKLOG.md (owner 16.11) | PROJECT.md:117-119 | — | § Бэклог и находки | backlog_tree.py (view), `piles.py status` (writer) |
| R3 | no one-time tidy pass; statuses kept with the merge; old fixed when touched (owner 17.11) | PROJECT.md:119 | — | § Бэклог и находки | partial: `wave.py merge --node` runs `piles.py status` (wave.py:383-402); rest discipline |
| R4 | an unfixed rule violation -> line in `factory-rules-debt.md` | PROJECT.md:119-120 | — | § Бэклог и находки | none (stream D 5.6 rewrites it) |
| R5 | piles / cards / batch files / findings structure (D-0036) | PROJECT.md:168-170 | team-work-plan.md:43-46 (record) | § Пачки (lead-in) | parsers `load_tree`, `parse_card`, `parse_batch` |
| R6 | one developer takes with `take` on main; branch `pile/<slug>/batch-<N>`; coordinator merges via `wave.py merge`; integrator closes | PROJECT.md:174-177 | README.md:64-65, :72; team-work-plan.md:47 | 1 | `take` (one taker), `wave.py`, `close` |
| R7 | [owner 18.11] taken and frozen against other users | brief facts | README template :25-26 and 31 cards («её файл правит только взявший»); README.md:66 («written only by you»); team-work-plan.md:51-53 | 1 (+ 2) | mismatch: F1 |
| R8 | [owner 18.11] the same user goes on taking nodes of the batch they froze | brief facts | — | 1 | mismatch/ambiguity: F2 |
| R9 | what changes in a taken batch file and card row | TEAMWORK.md:5-7 | critic.md — no; batch.md:43 (form legend) | 2 | (в) |
| R10 | new on the topic -> file in `findings/`, never a row in another's batch | TEAMWORK.md:7 | README template :25-26 + cards | 2 | (в) |
| R11 | a finding gets a row in an untaken batch at once; none -> open `batch-<N+1>` (D-0044) | TEAMWORK.md:8-10 | README template :53-54 + 18 cards | 2 | (е) |
| R12 | a finding gets its «Содержание» row in the card | TEAMWORK.md:11-12 | README template :41-42 (form legend) | 2 | (д) `_contents_reds`, test_pile_cards_contents.py |
| R13 | take (or Lead's «пачка полна») freezes; the next finding opens the next batch | TEAMWORK.md:13-14 | — | 2 | (е), (в) |
| R14 | a finding names a factory class, not one project's rule (P2); grep DECISIONS first | PROJECT.md:180-183 | — | 2 | none |
| R15 | zones of active batches do not overlap; `очередь:` line or disjoint function lists (D-0048) | TEAMWORK.md:15-18 | batch.md:35-44 (form legend) | 3 | (б), `take` `_overlap_refusal` |
| R16 | late node merges main and resolves; one critic after the merge; one developer's batches do not hold each other (owner 13.11) | PROJECT.md:184-186 | — | 3 | last clause: `dev_of`/`same_developer`; rest none |
| R17 | BACKLOG.md frozen; `close` moves to «Закрыто»; `close --id --word` | TEAMWORK.md:19-20 | PROJECT.md:117; README.md:10-11, :69-70; RUNBOOK.md:396-397 | 4 | (г), `close` |
| R18 | B-id issued only by the integrator on main when the batch is built; `id: —` before | PROJECT.md:187-188 | finding.md:13-14 | 4 | (а) unknown id red; issuer: none |
| R19 | no board; «Взял» and status in the header and card row, written by take/status/close (owner 13.11) | PROJECT.md:200-201 | — | 7 | take/status/close; `board` refused alias |
| R20 | doors `piles-skip:`; only touched piles judged | TEAMWORK.md:21 | — | 8 | `door_lines`, `run_check` |
| R21 | a batch closes by finishing; «Остатки» forms; executor at write time; `release` refused | TEAMWORK.md:22-26 | batch.md:76-88 (form legend + owner sentence :77); critic.md:202-204 | 9 | `close` `leftover_problem`, (д) `_leftover_write_reds` |
| R22 | «Живые доказательства» forms (FR-33) | TEAMWORK.md:26-29 | batch.md:62-72 (form legend + owner sentence :63) | 9 | `close` (proofs) |
| R23 | a carry is confirmed by a PERSON; ideally no leftovers; critic minors fixed in the fix round; other-pile remarks analysed, then carried with an executor; Lead marks closed rows | PROJECT.md:204-206 | COORDINATOR.md:226 (pointer to TEAMWORK § 9 already) | 9 | `close` (needs `подтвердил:`); rest none |
| R24 | live runs never hold a batch; evidence rows go to an untaken `live-runs` batch (owner 11.11) | PROJECT.md:207-211 | — | 9 | none |
| R25 | a node is written for a weaker model | PROJECT.md:219-224 | — | 11 | none (critic on plan, calibration 33) |
| R26 | [owner 18.11] no node without a batch | brief facts | — | 14 (new) | (а), (е), (д) — §2 |
| R27 | [owner 18.11, written] one priority per batch; another priority -> its own batch; mixed batches fixed when touched | batch.md:8 | — | 15 | none: F3 |
| R28 | header pair `приоритет:` overrides the card priority; without it the card priority | batch.md:6-7 | — | 15 | mismatch: F4 |
| R29 | batch statuses `ожидает → … → закрыта`; size S/M/L, more than 15 -> two batches | README template :24-25 | 36 card legends (with local owner exceptions, e.g. driver-hosts README:21) | 16 | statuses `BATCH_STATUSES` (112); size none |
| R30 | node executor kinds; node statuses `ожидает → в работе → сдано → принято / отклонено` | batch.md:27-28 | — | 16 | `NODE_STATUSES` (113), `status` |
| R31 | the check runs in commit-msg and CI forge-check; detector check 33 | TEAMWORK.md:31-32 | PROJECT.md:238 (pointer) | last line | hook + CI |
| R32 | `plans/BACKLOG.md` = «единый список того, что нужно сделать» | PROJECT.md:43 | — | contradicts R17 + R2: FIXED (S4) | — |

Related, stays (named, not moved): R33 COORDINATOR.md:165-167 rule 4a (a multi-event task is a DAG in a pile batch
file or `docs/tasks/`) — a routing rule, COORDINATOR owns routing; its pointer :168 is retargeted; stream D 5.7 edits
it (D still names it «CLAUDE.md rule 4a» — noticed). R34 PROJECT.md:94-95 п. 3 (a backlog item closed by code is not
proved until a live run, FR-33) — package acceptance. R35 PROJECT.md:111 п. 6 (г) (a new owner decision opens a new
graph node) — a clause of the spec-meaning rule. R36 PROJECT.md:233-234 п. 12 last sentence (statuses updated with the
merge) — part of the tempo item; TEAMWORK § Бэклог и находки points to it. R37 PROJECT п. 5, 6, 10, 13 — team rules,
not backlog (F7). R38 designer.md:46-49 (a finding only for another pile's zone) — role detail. R39 RUNBOOK.md:109 (a
red pipeline on main -> a finding) — stream D 5.5 rewrites it. Count: 32 rules (R1-R32) + 7 related (R33-R39).

## 4. Target `docs/TEAMWORK.md` (assembly order; numbering keeps the PROJECT «Командная работа» numbers)

Item numbers 1-4, 7-9, 11 = the old PROJECT numbers, so every «п. N» / «§ N» reference stays true; 5, 6, 10, 12, 13
stay in PROJECT.md; new items take 14-16. Spans are cut at BASE (`git show HEAD:<file>`); «subs» are the ONLY edits.

| # | content | source span (from «…» to «…») | subs |
|---|---|---|---|
| T0 | title `# Правила бэклога: находки, узлы, кучки и пачки` | new (replaces TEAMWORK:1) | — |
| T1 | intro (text below) | new (replaces TEAMWORK:3) | — |
| T2 | `## Бэклог и находки` + M1 | PROJECT.md:116-120 «Новая находка — файл» … «`design/factory-rules-debt.md`.» | «(«Командная работа» п. 2)» -> «(п. 2)»; «(там же п. 4)» -> «(п. 4)»; «(«Командная работа» п. 12)» -> «(`PROJECT.md` «Командная работа» п. 12)» |
| T3 | `## Пачки: взятие, заморозка, зоны, закрытие` + M2 | PROJECT.md:168-170 «Работа над фабрикой» … «(файл на находку).» (the trailing «Правила:» dropped) | — |
| T4 | item 1 = M3 + N1 | PROJECT.md:174-177 whole item | «(п. 12; ручное» -> «(`PROJECT.md` «Командная работа» п. 12; ручное» |
| T5 | item 2 = TEAMWORK:5-14 byte-identical + M4 as its last paragraph | M4 = PROJECT.md:180-183 «**Находка называет класс фабрики» … «на тему.» | — |
| T6 | item 3 = TEAMWORK:15-18 | — | «Что делает поздний узел — `PROJECT.md` «Командная работа» п. 3.» -> PROJECT.md:184-186 «При общем файле поздний узел» … «(владелец, 13.11.2026).» |
| T7 | item 4 = TEAMWORK:19-20 + M6 | M6 = PROJECT.md:187-188 «B-id выдаёт только» … «`id: —`.» | — |
| T8 | item 7 = M7 | PROJECT.md:200-201 whole item | — |
| T9 | item 8 = TEAMWORK:21 byte-identical | — | — |
| T10 | item 9 = TEAMWORK:22-29 + M9 on NEW lines (3-space indent) | M9 = PROJECT.md:204-211 «перенос подтверждает **человек**» … «снята прогоном.»; «**Остатков в идеале нет вовсе**» starts its own line | — |
| T11 | `## Узлы и формирование пачек`; item 11 = M10 | PROJECT.md:219-224 whole item | — |
| T12 | item 14 = N2 | new | — |
| T13 | item 15 = N3 + M11 | M11 = batch.md:8 «Правило формирования бэклога» … «(разового прохода нет).» and the rule half of :6-7 «Она перекрывает» … «приоритет карточки.» | per F4 |
| T14 | item 16 = M12 | README template :24-25 «Статусы пачки:» … «две пачки).» + batch.md:27-28 «Исполнитель» … «`отклонено`.» | — |
| T15 | last line = TEAMWORK:31-32 byte-identical | — | — |

T1 text: «Единственный дом правил бэклога (слово владельца 18.11.2026): как находка становится узлом, как узлы живут в
пачках, как пачку берут, замораживают, закрывают и как задаётся приоритет. Остальные места держат только ссылку сюда.
Где правило держит код, рядом названа проверка; где кода нет — правило на дисциплине. Номера пунктов 1–4, 7–9, 11 —
прежние номера `PROJECT.md` «Командная работа»; пункты 5, 6, 10, 12, 13 остаются там.»

N1 (appended to item 1; text for F1 (a) + F2 (a)): «**Пачку берут и замораживают от других** (слово владельца
18.11.2026): второго взявшего `take` не пускает; взявший дальше берёт узлы своей пачки по одному (`piles.py status
<slug> <N> <узел> --set "в работе"`). Текст взятой пачки заморожен для всех, взявшего тоже (п. 2): новых узлов во взятую
пачку не добавляют, новое ложится в невзятую. «Ход», «Остатки» и статусы взятой пачки пишет только её взявший — на
дисциплине: код знает взявшего (`взял:`), но не проверяет, кто коммитит.» Under F1 (b)/F2 (b) the Lead substitutes
the chosen text; the code node then owns this sentence.

N2 (item 14): «14. **Нет узла без пачки** (слово владельца 18.11.2026): работа существует только узлом — строкой
«Узлы» в файле пачки своей кучки; находка получает такую строку тем же ходом, что файл (п. 2). Код: `piles.py check`
(а) — открытый B-id, которого нет ни в строке пачки, ни в находке, красный; (е) — находка от 13.10.2026 без строки
пачки красная, более старая — строка WARN; (д) — id строки карточки стоит в «Что» ровно одного узла.»

N3 (item 15 opener + the F5 sentence + the F3 sentence): «15. **Один приоритет на пачку** (слово владельца
18.11.2026): » + M11 + « Находка ложится в невзятую пачку своего приоритета (`приоритет:` её шапки; `—` — приоритет
карточки кучки); нет такой — пишущий открывает следующую с парой `приоритет:` в шапке (п. 2). Проверки кода нет —
на дисциплине.» Under F4 (b) the M11 clause «без пары берётся приоритет карточки» is replaced by «без пары виджет
показывает пачку без приоритета («—»)»; under F4 (a) it stays and is true once the widget node lands (until then the
TEAMWORK line carries «(виджет пока берёт только пару — узел F4)»).

## 5. Pointer lines left in the old places (exact text)

| place | replaced span | pointer line |
|---|---|---|
| PROJECT.md:96 п. 4 | «— правило: § Бэклог и находки» | «— правило: `docs/TEAMWORK.md` § Бэклог и находки» |
| PROJECT.md:116-120 | the section body | «Правило: `docs/TEAMWORK.md` § Бэклог и находки.» (heading stays: TOC rows) |
| PROJECT.md:168-170 | the lead-in | «Правила бэклога — кучки, пачки, находки, узлы — живут в `docs/TEAMWORK.md` (слово владельца 18.11.2026); здесь — их номера со ссылкой и правила команды (п. 5, 6, 10, 12, 13).» |
| PROJECT.md:174-177 | item 1 | «1. **Пачку берёт один разработчик** — правило: `docs/TEAMWORK.md` § 1.» |
| PROJECT.md:178-183 | item 2 | «2. **Взятая пачка заморожена** — правило: `docs/TEAMWORK.md` § 2 (что меняется во взятой пачке, находка в пачку, строка «Содержание», находка называет класс фабрики).» |
| PROJECT.md:184-186 | item 3 | «3. **Зоны файлов пачек «в работе» не пересекаются** — правило: `docs/TEAMWORK.md` § 3.» |
| PROJECT.md:187-188 | item 4 | «4. **`plans/BACKLOG.md` заморожен** — правило: `docs/TEAMWORK.md` § 4.» |
| PROJECT.md:200-201 | item 7 | «7. **Доски нет** — правило: `docs/TEAMWORK.md` § 7.» |
| PROJECT.md:203-211 | item 9 | «9. **Пачка закрывается доделкой, не переносом** — правило: `docs/TEAMWORK.md` § 9.» |
| PROJECT.md:219-224 | item 11 | «11. **Узел пачки пишется для более слабой модели** — правило: `docs/TEAMWORK.md` § 11.» |
| PROJECT.md:25, :29 (TOC «О чём») | cells | «указатель на `docs/TEAMWORK.md`»; «правила команды; правила бэклога — `docs/TEAMWORK.md`» |
| PROJECT.md:43 | row text | «заморожен: старые строки B-nnn до закрытия; список работы — узлы пачек `plans/piles/` (правило: `docs/TEAMWORK.md` § 4)» (S4) |
| PROJECT.md:55 | row text | «все правила бэклога: находки, узлы, пачки, взятие, заморозка, закрытие, приоритет (слово владельца 18.11.2026)» |
| batch.md:6-8 | the rule half of :7 and :8 | keep «Необязательная пара строки заголовка: `приоритет: П1\|П2\|П3` (в любом месте строки, после `стенд:` или раньше).»; add «Один приоритет на пачку — правило: `docs/TEAMWORK.md` § 15.» |
| batch.md:27-28 | the paragraph | «Исполнитель и статусы узла — правило: `docs/TEAMWORK.md` § 16.» |
| batch.md:63 | «(слово владельца 08.10.2026: пачка закрывается доделкой, не переносом)» | «(правило: `docs/TEAMWORK.md` § 9)» |
| batch.md:77 | «Пачка закрывается доделкой, не переносом (слово владельца 08.10.2026): `close`» | «Правило: `docs/TEAMWORK.md` § 9. `close`» |
| README template :24-26 | the statuses/size and freeze sentences | «Статусы и размер пачки — правило: `docs/TEAMWORK.md` § 16. Взятая пачка заморожена — правило: `docs/TEAMWORK.md` § 2.» |
| README template :53-54 | «Каждая новая находка тем же ходом получает строку …» to «… со статусом «ожидает».» | «Каждая новая находка тем же ходом получает строку в невзятой пачке — правило: `docs/TEAMWORK.md` § 2.» |
| 31 cards (freeze) / 18 cards (intake), F8 (a) | the sentence equal (whitespace-squashed) to the template's | «Взятая пачка заморожена — правило: `docs/TEAMWORK.md` § 2.» / the intake pointer above |
| finding.md:13 | «id выдаёт интегратор при сборке пачки (следующий свободный B-nnn на main)» | «id выдаёт интегратор (правило: `docs/TEAMWORK.md` § 4)» |
| README.md:66, :68-69, :72 | step 4 first sentence; step 5 end; step 7 | «4. A taken batch is frozen — rule: `docs/TEAMWORK.md` § 2.» (the Ход sentence stays); step 5 + « — rule: `docs/TEAMWORK.md` § 2»; «7. Merging into `main` — rule: `docs/TEAMWORK.md` § 1 and `docs/RUNBOOK.md` §7.» (S12) |
| RUNBOOK.md:230, :366, :372 | «(`PROJECT.md`, «Командная работа» п. 2)» / «(PROJECT.md «Командная работа» п. 2)» | «(правило: `docs/TEAMWORK.md` § 2)» |
| RUNBOOK.md:237, :388 | — | append «(правило: `docs/TEAMWORK.md` § 2)» after «строка в невзятой пачке» |
| RUNBOOK.md:397 | «`PROJECT.md` «Командная работа» п. 4» | «правило: `docs/TEAMWORK.md` § 4» |
| COORDINATOR.md:38, :39, :168 (Lead) | cells / clause | «docs/TEAMWORK.md»; «docs/TEAMWORK.md § Бэклог и находки»; «the rule text is `docs/TEAMWORK.md` (D-0036; detector: check 33)» |
| SIBLING_MAP.md:479, :494, :495 (Lead) | aspect texts | «`docs/TEAMWORK.md` (every backlog rule: findings, nodes, batches, taking, freezing, closing, priority)»; :494 «… «Командная работа» п. 1-4, 7-9, 11 and § Бэклог и находки → `docs/TEAMWORK.md` …»; :495 «every backlog rule (the owner's word 18.11.2026) and the check line» — the Owner/pointer cell keeps starting with «owner» (`pointer_lint.main_documents` 117) |
| session-retro SKILL.md:68 (Lead) | «(PROJECT «Командная работа» п. 2)» | «(правило: `docs/TEAMWORK.md` § 2)» |
| critic.md:202-204 | per F6 | `<what> | узел: …` / `перенос: …` forms -> «in the forms of `docs/TEAMWORK.md` § 9» |

## 6. Builder card

given: this spec; `C:/QAFactory/forge-repo/docs/TEAMWORK.md`; `C:/QAFactory/forge-repo/PROJECT.md`;
`C:/QAFactory/forge-repo/plans/piles/_template/batch.md`; `C:/QAFactory/forge-repo/plans/piles/_template/README.md`;
`C:/QAFactory/forge-repo/tools/tests/test_role_carriers_one_owner.py`; `C:/QAFactory/forge-repo/tools/pointer_lint.py`
owns:
C:/QAFactory/forge-repo/docs/TEAMWORK.md
C:/QAFactory/forge-repo/PROJECT.md
C:/QAFactory/forge-repo/plans/piles/_template/batch.md
C:/QAFactory/forge-repo/plans/piles/_template/README.md
C:/QAFactory/forge-repo/plans/piles/_template/finding.md
C:/QAFactory/forge-repo/docs/RUNBOOK.md
C:/QAFactory/forge-repo/README.md
C:/QAFactory/forge-repo/tools/tests/test_role_carriers_one_owner.py
C:/QAFactory/forge-repo/AGENTS.md
C:/QAFactory/forge-repo/plans/piles/codex/README.md C:/QAFactory/forge-repo/plans/piles/hotfix-12586/README.md C:/QAFactory/forge-repo/plans/piles/execution-report/README.md C:/QAFactory/forge-repo/plans/piles/github-move/README.md C:/QAFactory/forge-repo/plans/piles/exploratory/README.md C:/QAFactory/forge-repo/plans/piles/regression/README.md C:/QAFactory/forge-repo/plans/piles/words-gates/README.md C:/QAFactory/forge-repo/plans/piles/gates-and-words/README.md
C:/QAFactory/forge-repo/plans/piles/proposals/README.md C:/QAFactory/forge-repo/plans/piles/onboarding-hooks/README.md C:/QAFactory/forge-repo/plans/piles/universality/README.md C:/QAFactory/forge-repo/plans/piles/live-run-fvf/README.md C:/QAFactory/forge-repo/plans/piles/kb/README.md C:/QAFactory/forge-repo/plans/piles/told-before-work/README.md C:/QAFactory/forge-repo/plans/piles/execution-probes/README.md C:/QAFactory/forge-repo/plans/piles/onboarding-forge/README.md
C:/QAFactory/forge-repo/plans/piles/grounding/README.md C:/QAFactory/forge-repo/plans/piles/live-runs/README.md C:/QAFactory/forge-repo/plans/piles/run-honesty/README.md C:/QAFactory/forge-repo/plans/piles/package-ci/README.md C:/QAFactory/forge-repo/plans/piles/test-code-quality/README.md C:/QAFactory/forge-repo/plans/piles/release-next/README.md C:/QAFactory/forge-repo/plans/piles/rules-debt/README.md C:/QAFactory/forge-repo/plans/piles/roles-context/README.md
C:/QAFactory/forge-repo/plans/piles/report-delivery/README.md C:/QAFactory/forge-repo/plans/piles/stand-and-sources/README.md C:/QAFactory/forge-repo/plans/piles/speed-cost/README.md C:/QAFactory/forge-repo/plans/piles/cost-dashboard/README.md C:/QAFactory/forge-repo/plans/piles/driver-hosts/README.md C:/QAFactory/forge-repo/plans/piles/collect/README.md C:/QAFactory/forge-repo/plans/piles/driver-controller/README.md C:/QAFactory/forge-repo/plans/piles/thinking-roles/README.md
non-goals: no code change (forks F3, F4 are separate nodes); the everything-in-piles streams are not absorbed; mixed-priority batches are not re-sorted (owner: not now); records stay (S5); batch files are not edited; the card legends of statuses/size stay (F8 (a)); COORDINATOR.md, docs/SIBLING_MAP.md, .claude/skills/session-retro/SKILL.md (and critic.md under F6 (b)) are handed as TEXT with before/after lines — the Lead places them in the same commit (mechanism paths, tools/mechanism_gate.py:216-230)
handoff: the diff + the report (builder.md rule 7) with: the witness script in full source and its output; the list of card variants left (E5); the `piles.py check --all` before/after comparison; the Lead-placed texts
edges: §7 (E1-E13)
siblings: everything-in-piles stream D (same rule texts; order: THIS FIRST, D re-anchors by its quoted old text, E9), A1 (template node columns, after this), K / FG7-52 (`test_role_carriers_one_owner.py` POINTERS rows, after this); SIBLING_MAP axis 31 (one owner per aspect)
DoD: `python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_piles_split.py tools/test_pile_cards_contents.py -q` + `python -m pytest tools/test_piles.py -q -k f626` + `python -m pytest tools/test_piles_close_gate.py -q -k template` + `python -B tools/pointer_lint.py --check` (exit 0) + `python -B tools/piles.py check --all` (red lines identical before/after) + the DOC-DISPATCH witness below; the Lead's commit adds `python tools/agents_md.py --check`

Acceptance keys (DOC-DISPATCH witness: the script checks THESE strings verbatim, whitespace-squashed; full source in
the report, never committed; negative control: the run repeated with K-1 removed from a COPY of TEAMWORK reports
failure):
- present in `docs/TEAMWORK.md`: K-1 `## Бэклог и находки`; K-2 `1. **Пачку берёт один разработчик**`; K-3 `2. **Взятая пачка заморожена** (`piles.py check` (в), гейт commit-msg)`; K-4 `7. **Доски нет**`; K-5 `11. **Узел пачки пишется для более слабой модели**`; K-6 `14. **Нет узла без пачки**`; K-7 `15. **Один приоритет на пачку**`; K-8 `16. **Статусы и размер пачки**`; K-9 `**Пачку берут и замораживают от других**`.
- present in `PROJECT.md`: K-10 `1. **Пачку берёт один разработчик** — правило: `docs/TEAMWORK.md` § 1`; K-11 `7. **Доски нет** — правило: `docs/TEAMWORK.md` § 7`; K-12 `11. **Узел пачки пишется для более слабой модели** — правило: `docs/TEAMWORK.md` § 11`; K-13 `Правило: `docs/TEAMWORK.md` § Бэклог и находки.`
- present in the templates: K-14 batch.md `Один приоритет на пачку — правило: `docs/TEAMWORK.md` § 15.`; K-15 README `Взятая пачка заморожена — правило: `docs/TEAMWORK.md` § 2.`; K-16 README `Статусы и размер пачки — правило: `docs/TEAMWORK.md` § 16.`
- ABSENT: K-17 PROJECT.md `Находка называет класс фабрики`; K-18 PROJECT.md `Разового прохода «причесать бэклог» нет`; K-19 PROJECT.md `Остатков в идеале нет вовсе`; K-20 batch.md `в пачке узлы ОДНОГО приоритета`; K-21 no `plans/piles/*/README.md` holds `её файл правит только взявший` except the variants listed under E5.
- K-22 every span of §4 (M1-M12, TEAMWORK spans) after its subs is a squashed substring of the new TEAMWORK (base text by `git show HEAD:<file>`); K-23 `PROJECT.md` bytes after < before (`python -B -c "import os;print(os.path.getsize('PROJECT.md'))"`, run before the first edit and after the last).

test: (ordered, strongest first; each a ROW of an existing table in `tools/tests/test_role_carriers_one_owner.py`, no new file)
1. a pointer of a moved rule resolves (`POINTERS`): rows PROJECT.md -> TEAMWORK § 1 (`1. **Пачку берёт один разработчик**`), § 7, § 11, «§ Бэклог и находки» (`## Бэклог и находки`; row 104 retargeted to it), template batch.md -> § 15, template README -> § 16; row 108 (TEAMWORK -> PROJECT п. 3) DELETED — the reverse pointer no longer exists; rows 96-100 unchanged.
2. a moved owner rule has one owner (`OWNER_KEYS`): `("backlog:no-node-without-batch", TEAMWORK, "работа существует только узлом")`, `("backlog:frozen-from-others", TEAMWORK, "Пачку берут и замораживают от других")`, `("backlog:one-priority", TEAMWORK, "в пачке узлы ОДНОГО приоритета")` — plans/piles/ is outside the scan (EXCLUDED :38), so the template pointer does not collide.

## 7. Edges (behaviour + invariant)

| # | edge | behaviour | invariant |
|---|---|---|---|
| E1 | a moved span | only the subs of §4; K-22 proves it | no backlog rule changes meaning in the move; an unlisted edit is a defect |
| E2 | boot budget | PROJECT.md shrinks (K-23); CLAUDE.md untouched; COORDINATOR_FILES unchanged (F9 (a)) | the boot never grows by this move |
| E3 | a pointer target | each `§ N` target is a numbered item of TEAMWORK (pointer_lint ITEM_RE, :56) and each `§ <name>` a heading | no dangling pointer; pointer_lint and POINTERS agree |
| E4 | a card of a TAKEN batch | only prose under the «Пачки» table and in «Входящие» changes | (в)'s card-row freeze (`_compare_card`) is never touched; `check --all` red lines identical |
| E5 | a card sentence differing from the template's (grounding:217, codex:108, thinking-roles:117, test-code-quality:93 …) | left as is, listed in the report | no local owner decision (e.g. driver-hosts:21 «42 и 55 узлов по решению владельца») is overwritten |
| E6 | pointer text in a template or card | contains no `приоритет:` or `кучка:`, never starts a line with `## ` or `| 1 |` | `parse_card` (first line with `приоритет:`, 483), `parse_batch` (first line with `кучка:`, 676) and `piles_split.render_card` (212-231) read the same lines as before |
| E7 | `test_piles_split.py:294` asserts «Взятая пачка заморожена» in a card made from the real template | the template pointer keeps those words | a new card still carries the freeze pointer |
| E8 | template batch.md | comments stay closed; the keys of `test_piles.py:810` stay; the readiness line :11-12 byte-identical | the template still closes freely (`test_piles_close_gate.py:419`) and declares nothing; `close` still reads «живые доказательства» there |
| E9 | TEMPORAL: stream D lands later | D's quoted anchors stay byte-identical in TEAMWORK: «**Находка сразу попадает в пачку** (D-0044)», «…и находка ложится туда.», «…у находки до этого `id: —`.», «…исполнителю не нужно искать по кучкам.», «Нарушение правила, которое не чинится сейчас, — строка в `design/factory-rules-debt.md`.», «перенос подтверждает **человек**, не агент сам», «**Остатков в идеале нет вовсе**» … «строкой с исполнителем.» | D's rule «applied wherever that text stands at landing» (everything-in-piles §5) still finds every anchor |
| E10 | the commit touches 32 piles | `piles.py check` judges every touched pile: a red carried before the edit now blocks — passed by `piles-skip: <item> -- carried before t-1489, card prose pointer only`, each red listed | the door never passes a red this edit creates |
| E11 | TEMPORAL: F3 (b) / F4 (a) code nodes | until they land TEAMWORK says «на дисциплине» / «(виджет пока берёт только пару)»; the code node's commit rewrites that clause (its owns include the TEAMWORK line) | the text never claims a check that does not exist |
| E12 | a card with neither sentence (conductor, pre-code, project-knowledge, forge) | untouched | — |
| E13 | `§ Бэклог и находки` in prose | not judged by pointer_lint (its known miss 5); POINTERS row covers PROJECT; the COORDINATOR Contents cell IS judged (TOC kind) | a renamed heading turns a test red, never a silent pass |

Conflicting pairs: R11 (untaken batch) x R27 (one priority) -> F5; R7 (against others) x R9 (Ход/status open to any
committer) -> F1; R8 x R13 (take freezes, next finding opens the next batch) -> F2; «meaning kept» x the stale
PROJECT.md:43 -> S4 (a fix, named, not a move).

## 8. Readers of every touched file (designer rule 7)

The `tools/owns_readers.py` block was NOT attached: hand greps below (Grep tool, repo minus worktrees/specs/logs); the
Lead runs `python -B tools/owns_readers.py --paths docs/TEAMWORK.md PROJECT.md plans/piles/_template/batch.md
plans/piles/_template/README.md plans/piles/_template/finding.md docs/RUNBOOK.md README.md
tools/tests/test_role_carriers_one_owner.py COORDINATOR.md docs/SIBLING_MAP.md .claude/skills/session-retro/SKILL.md
--readers` before dispatch (no names change: no code).

| file | reader | verdict |
|---|---|---|
| docs/TEAMWORK.md | test_role_carriers_one_owner.py POINTERS 96-100, 108 | changes here (108 deleted) |
| | tools/pointer_lint.py (MAIN document, `§ N` anchors) | unchanged; must exit 0 |
| | SIBLING_MAP :479, :495 / :310 (§ 3 function-list grammar) | change, Lead / unchanged (§ 3 stays) |
| | COORDINATOR :38 / :226 (§ 9) | change, Lead / unchanged (§ 9 stays) |
| | everything-in-piles D 5.3b (TEAMWORK § 9) | changes in stream D per F6 |
| | PROCESS calibration :1026 | unchanged (still true) |
| PROJECT.md | coordinator_rules / session_context (boot read) | unchanged; the file shrinks |
| | tools/agents_md.py -> AGENTS.md | regenerated here |
| | OWNER_KEYS `cost:queue` (п. 12), pointer_lint NUMBER_PAIRS `держать (\w+) пишущих` (п. 12) | unchanged (п. 12 stays) |
| | POINTERS 75, 76, 96-103, 107 / 104 | unchanged / retargeted here |
| | pointer_lint TOC_TABLES «Оглавление» | Раздел cells unchanged; «О чём» text changes here |
| | RUNBOOK :121 (п. 12) / :230 :366 :372 :397 | unchanged / change here |
| | critic.md :269, PROCESS :1137 :1147 (п. 6) | unchanged (п. 6 stays) |
| | PROCESS :1131 (п. 9) | unchanged: the п. 9 pointer line resolves; D edits check 39 |
| | COORDINATOR :31 :32 :53 / :38 :39 :168 | unchanged (п. 1/12 merge, writers) / change, Lead |
| | SIBLING_MAP :34 (п. 13), :533 (п. 12) / :494 | unchanged / change, Lead |
| | session-retro SKILL :68 | change, Lead |
| | tools/piles.py:2184 docstring (п. 2) | unchanged (non-goal: code; the п. 2 pointer resolves) |
| | test_agents_md.py:77 (copies the real file) | unchanged |
| | CLAUDE_HOST_ADAPTATIONS_FULL :21; team-work-plan :144 | unchanged (records) |
| _template/batch.md | test_piles.py:808-815 | unchanged (E8) |
| | test_piles_close_gate.py:414-422 | unchanged (E8) |
| | test_pile_cards_contents.py:95-98; piles.BATCH_HEADINGS (1935) | unchanged (headings untouched) |
| | everything-in-piles A1 / 5.13 (node columns, `план:`) | changes later in that stream (additive) |
| _template/README.md | piles_split.render_card + test_piles_split.py:103, :294 | unchanged (E6, E7) |
| | test_pile_cards_contents.py:77-82 | unchanged (headings untouched) |
| _template/finding.md | collect_intake / piles_split write their own headers (collect_intake.py:954, piles_split.py:190) | unchanged (comment only) |
| 32 cards | parse_card, (д) `_contents_reds`, (в) `_compare_card`, backlog_tree (title) | unchanged (E4, E6) |
| test_role_carriers_one_owner.py | CI forge-check; pointer_lint WIDE_EXCLUDED (:48) | unchanged |
| | everything-in-piles D 5.14, K, FG7-52 | change later; order: this first |
| RUNBOOK.md | pointer_lint (MAIN); POINTERS 92, 93, 105; NUMBER_PAIRS «не больше (\w+) пишущих» | unchanged |
| README.md | humans; pointer_lint P kind if scanned | unchanged |
| COORDINATOR.md (Lead) | coordinator_rules, agents_md, pointer_lint Contents cells; OWNER_KEYS rule-9 keys (:226 untouched) | the two cells must resolve (E3) |
| SIBLING_MAP.md (Lead) | pointer_lint.main_documents, test_role_carriers MAIN | Owner cell keeps «owner» |

## Forks (options, cost, recommendation)

F1 — «заморожена от других пользователей» vs the code. Owner: «a batch is taken and frozen against other users».
Code: «a taken batch changes only its Ход, Остатки, the Статус cells, queue lines (added) and the header's
статус/MR/issue» (piles.py:1699-1702) — for EVERY committer, the taker included; the open parts are open to any
committer; `take` refuses a second taker; nobody checks who commits. Texts disagree too: TEAMWORK:5 (for all) vs README
template :25 «её файл правит только взявший» (taker edits everything) vs README.md:66. (a) TEAMWORK states the code
(N1): frozen for all; the open parts are the taker's by discipline — no code. (b) a code node: (в) and `status` compare
the committing clone's developer slug (`journal_keys.developer_slug`) with `dev_of(взял)` and refuse another developer;
CI (`check --base`) has no clone slug — needs a design (commit author?); piles.py is sequenced after everything-in-piles
A1-A3 (D-0048). (c) the taker may edit even the frozen parts — contradicts (в)'s contract and stream A3's brake.
Recommend (a); (b) only if the owner wants the code to stop the other developer.

F2 — «the same user may go on taking nodes from the batch they froze». (a) = taking the batch's EXISTING nodes one by
one (`status … --set "в работе"`): the code allows it, nothing changes; new work goes to an untaken batch (D-0044).
(b) = the taker may ADD nodes to their taken batch: code change in `_frozen_lines`/`_compare_batch` and the frozen card
«Строки» cell (CARD_FROZEN_COLS) + F1 (b)'s identity; contradicts TEAMWORK:13-14 and stream A3. Owner's intent;
recommend (a), asked in plain words («узлы, которые уже в пачке, или новые?»).

F3 — one priority per batch has no code (owner-named rule). (a) discipline only. (b) a node: `piles.py check` (д)
refuses a NEW or CHANGED node row whose «Приоритет» differs from the batch priority (pair, else card), old rows
grandfathered — no re-sort (owner: not now); after everything-in-piles A1 (same `NODE_COLS`/`_parse_nodes`). Recommend
(b) as a separate node; TEAMWORK says «на дисциплине» until it lands (E11).

F4 — the fallback: template batch.md:7 «без пары берётся приоритет карточки» vs `backlog_tree.py:42` (pair only).
(a) code: the widget falls back to `pile.card.priority` (one line; everything-in-piles stream B owns backlog_tree.py —
order with B); (b) text: «без пары пачка без приоритета». 7 of 107 batch files lack the pair (measured, §2). Recommend (a).

F5 — conflict pair R11 x R27: where a finding lands when the only untaken batch has another priority. (a) N3's
sentence: the untaken batch of ITS priority (its header `приоритет:`; `—` -> the card's), none -> open the next with the
pair; (b) the Lead assigns the priority at placement; (c) any untaken batch, fixed when touched. Recommend (a).

F6 — everything-in-piles stream D makes PROJECT.md п. 9 «**Остатков нет по правилу**» the leftover HOME (its §5, 5.3,
5.14 OWNER_KEYS `("teamwork:leftovers", "PROJECT.md", …)`, pointers `правило: PROJECT.md § …`). After this move п. 9
is a pointer. (a) the Lead amends D: home = TEAMWORK § 9, pointer text `правило: docs/TEAMWORK.md § **Остатков нет по
правилу**`, 5.14 rows retargeted; D's 5.10 (folded into critic.md rule 22 Q4 — `critic-diff-brief.md` is deleted,
test_role_carriers DELETED :198) also turns critic.md:202-204 into the § 9 pointer, inside D's one critic exam
(critic.md rule 10). (b) critic.md:202-204 converted HERE, the Lead runs the exam now. (c) D unchanged — contradicts the
owner's 18.11 word. Recommend (a). D's priority: lowest of the day (owner 17.11, its §7.1); not landed — PROJECT.md:204
still holds «Остатков в идеале нет вовсе».

F7 — scope: which «Командная работа» items move. (a) the backlog items 1-4, 7-9, 11 + § Бэклог и находки + the lead-in;
п. 5 (one writer), 6 (owner's word — cited by critic.md:269 and PROCESS :1137/:1147), 10 (knowledge), 12 (tempo — pinned
by OWNER_KEYS `cost:queue` and pointer_lint NUMBER_PAIRS), 13 (builder checks) stay. (b) the whole section moves — re-pins
`cost:queue` and NUMBER_PAIRS (code), and p. 12 is a boot rule every session obeys. Recommend (a).

F8 — card copies (plans/piles/<slug>/README.md): 31 cards hold the freeze sentence (one claim contradicts the code,
F1), 18 the intake sentence, 36 a statuses/size legend (some with local owner exceptions). (a) the template takes all
three pointers; the cards' freeze and intake sentences become pointers where they equal the template text; legends stay;
(b) all three everywhere; (c) template only — 31 wrong copies remain. Recommend (a).

F9 — TEAMWORK at boot. (a) stays on topic: PROJECT keeps numbered pointer lines with the bold titles; boot shrinks
(estimate ~4-5 KB, not measured; K-23 measures). (b) add `docs/TEAMWORK.md` to `COORDINATOR_FILES` — also
`session_context._COORDINATOR_FALLBACK_FILES` (:257) and its pin (test_session_context.py:3714), AGENTS.md grows; the boot
grows by the file. Recommend (a).

## Small choices closed by the designer

S1 numbering keeps the PROJECT numbers, new items 14-16. S2 pointer form: `правило:` in Russian carriers, `rule:` in
English (everything-in-piles F22 (a)). S3 PROJECT's `###` sub-headings stay. S4 PROJECT.md:43 (BACKLOG.md «единый
список») fixed — contradicts п. 4 and the owner's 16.11 word; the Lead may veto. S5 records untouched: team-work-plan.md,
CLAUDE_HOST_ADAPTATIONS_FULL.md:21, boot-by-topic spec, batch files quoting old texts, PROCESS :1026/:1131, piles.py
docstring. S6 form legends stay in templates (Пишет в, функции:, the two forms, readiness line, finding form); only
sentences carrying a rule with an owner's word become pointers (batch.md:63, :77). S7 RUNBOOK references made one hop.
S8 card variants left and listed (E5). S9 three OWNER_KEYS rows. S10 TEAMWORK title and intro rewritten. S11 POINTERS
row 108 deleted, 104 retargeted. S12 README.md step 7 («the integrator merges» vs п. 1 «сливает координатор … `wave.py
merge`») becomes a pointer to TEAMWORK § 1 and RUNBOOK §7.

## Noticed, not widened

- Stream D's §5.7 still says «CLAUDE.md rule 4a»; rule 4a lives in COORDINATOR.md:163-168 (worker split).
- Stream D's 5.10 targets `docs/tasks/critic-diff-brief.md`, which is deleted (test_role_carriers DELETED :198); its q4 text is critic.md rule 22 Q4 now (F6).
- (е) counts a finding named only in a CLOSED batch as placed (`pile_prose` reads every batch) — «no node without a batch» holds formally there; whether such a finding is still work is not judged. For the Lead.
- `cmd_status` sets a node of a WAITING batch (no take check, 3332-3363) — a node can be «в работе» before its batch is taken.

## Reading trail

Read: docs/TEAMWORK.md (whole); PROJECT.md:1-270; plans/piles/_template/{batch,README,finding}.md (whole);
tools/piles.py:1-108, 474-508, 668-690, 1097-1231, 1495-1523, 1589-1778, 2104-2218, 2494-2563, 3239-3330, 3332-3460;
tools/backlog_tree.py:1-60; tools/tests/test_role_carriers_one_owner.py (whole); tools/pointer_lint.py:1-128;
tools/coordinator_rules.py (Grep COORDINATOR_FILES); tools/mechanism_gate.py:216-249; tools/piles_split.py:205-243;
tools/test_piles.py:806-816; tools/test_piles_split.py:280-295; COORDINATOR.md:1-60, 160-239, 290-309, 400-411;
.claude/agents/critic.md:56-63, 196-207; docs/SIBLING_MAP.md:476-500; README.md:8-73; plans/team/team-work-plan.md:1-60;
everything-in-piles spec :503-662, :718-785, :1591-1650. Greps (Grep tool): «заморожена: её файл правит только|правит
только взявший» over plans/piles/**/README.md = 32 files (31 cards + template); «тем же ходом получает строку» = 19
(18 + template); first run with glob `*/README.md` returned 0 while the template is known to hold the phrase — a miscall,
re-run with `**/README.md`; CLAUDE.md / FACTORY_RULES_INDEX.md negatives with positive controls (§1; `FR-33` found in the
index); `TEAMWORK` over tools/ = test_role_carriers only; `приоритет` over tools/*.py (backlog_tree.py:42 the only batch
reader); batch-header counts 100/107 (§2). `everything-in-piles` over plans/piles = 0 (case-sensitive run); «stream D
not started» rests on PROJECT.md:204 (D's 5.3 not landed), not on that negative.

## Lead decisions (18.11, Lead 501cb4e0; F1 and F2 by the owner's words)

- F1 (a) with the owner's addition. Owner: the code need not stop ANOTHER developer (that stays on discipline), «но нужно
  что бы код не мешал тому же разработчику». So: no identity code (no (b)); and the builder card adds a check -- nothing
  in tools/piles.py (take / status / (в) / check) refuses the SAME developer acting on a batch that another session of
  theirs took (the `взял` cell names an older session or date). If a refusal is found, the card returns it as a question
  with the carrier:line; the builder does not widen into piles.py on its own.
- F2 (a). Owner: yes, the existing nodes of a taken batch; example -- the onboarding batches are marked taken by the
  session of 12.11, and that must not stop a later session of the same developer taking nodes from them. TEAMWORK states
  this in one sentence (same developer, any session).
- F3 (b) as a separate node; TEAMWORK says «на дисциплине» until it lands (E11). F4 (a), ordered with everything-in-piles
  stream B. F5 (a). F6 (a): the Lead amends stream D's spec. F7 (a). F8 (a). F9 (a).
- Order: after FG7-62 Card B (t-1519) merges -- shared PROJECT.md, AGENTS.md, test_role_carriers_one_owner.py,
  docs/SIBLING_MAP.md.
