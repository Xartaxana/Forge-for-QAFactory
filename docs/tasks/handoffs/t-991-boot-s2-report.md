# t-991 (FG7-51 S2, the PROJECT side) -- builder report

status: DoD 1 NOT green as run in the worktree (7 ERRORS in `tools/test_agents_md.py`, a file outside `owns`; one-line fix proven by a restored probe, see Questions). Everything else done. All changes STAGED in the worktree, nothing committed.

Worktree: `C:/QAFactory/forge-repo/.claude/worktrees/agent-adbe4143d52ee10c3`. Staged: AGENTS.md, CLAUDE.md, PROJECT.md, docs/OWNER_PRINCIPLES.md (new), docs/OWNER_PRINCIPLES_INDEX.md (new, generated), docs/TEAMWORK.md (new), docs/RUNBOOK.md, plans/builder-rules.md, tools/test_session_context.py, tools/tests/test_role_carriers_one_owner.py (+ this report). `tools/install_parity_anchors.json`: untouched (no anchor quotes the edited CLAUDE.md lines; `install_parity.py --check` MISSING (0)).

## was-where -> is-where (every row by id)

| Row | Was (opener) | Is where | Kind |
|---|---|---|---|
| P-0 | PROJECT intro | stays; `## Оглавление` (13 rows, own sections only, topic names, no rule sentence; no row to CLAUDE § Contents, E21) after the intro | K1 |
| P-W | `## Где что лежит` | stays + rows `docs/OWNER_PRINCIPLES.md`, `docs/TEAMWORK.md` | K1 |
| P-PI | «Они же стоят правилами FR-47…» | stays + the one line «Полный текст P1–P31 — `docs/OWNER_PRINCIPLES.md`; первая фраза каждого — индекс …» | K3 |
| P1…P31 | PROJECT `- **P<n>.**` bullets | `docs/OWNER_PRINCIPLES.md`, bullets verbatim, source order, sub-headings `### P1–P9`, `### P10–P17`, `### P18–P22`, `### P23–P26`, `### P27–P31` | K2 |
| PI-1 | -- | `docs/OWNER_PRINCIPLES.md` title + intro line as the card; `factory_rules_index.py` wrote `docs/OWNER_PRINCIPLES_INDEX.md` (31 lines, 5212 B < 6144) | K2 |
| PA1 / PA3 | «1. **Проход…», «3. **Доказанность.**» | stay; headings `### Пакет: проход и свидетель`, `### Пакет: доказанность, эталон, смысл` | K1 |
| PA2 | «2. **Свидетель билдера**» | 3.4a: 2-1, 2-2 stay; 2-3, 2-4, 2-5, 2-7, 2-8, 2-10, 2-11, 2-13 dropped (K4, home keys verified); 2-6 + 2-9 on the «Диспетчеру:» line; 2-14 pointer line; 2-12 and 2-15 -> RUNBOOK §7 | K1/K2/K3/K4 |
| PA4 | «4. **Бэклог.** Новая находка…» | boot `4. **Бэклог.** — правило: § Бэклог и находки`; text verbatim in new `## Бэклог и находки` (after «Как принимается»; continuation indent dropped) | K2, K3 |
| PR5, PR6 | shell cwd / connectors bullets | `## Сессия форджа`, whole bullets | K2 |
| PR7 | compaction bullet | `## Сессия форджа`; TR1: «на ~300K контекста, на границе стадии, — одна строка» | K2 + TR1 |
| PT2 | «2. **Взятая пачка заморожена**» | boot: number + bold title + «— правило: `docs/TEAMWORK.md` § 2 (…)» then 2f, 2g verbatim; TEAMWORK item 2 = 2a..2e | K2, K3, K1 |
| PT3 | «3. **Зоны файлов пачек…**» | boot pointer + «При общем файле» + 3b + 3c verbatim; TEAMWORK item 3 = 3a («:» -> «.» + «Что делает поздний узел — `PROJECT.md` «Командная работа» п. 3.») | K2, K3, K1 |
| PT4 | «4. **`plans/BACKLOG.md` заморожен**» | boot pointer + 4b verbatim; TEAMWORK item 4 = 4a | K2, K3, K1 |
| PT8 | «8. **Двери**» | boot `8. **Двери** — правило: `docs/TEAMWORK.md` § 8.`; TEAMWORK item 8 whole | K2, K3 |
| PT9 | «9. **Пачка закрывается доделкой…**» | boot pointer (9c in the pointer line) + 9d, 9e, 9f verbatim; TEAMWORK item 9 = 9a minus 9c, then 9b. Moved AS IT STANDS (E20 below) | K2, K3, K1 |
| PT12 | «12. **Темп координатора**» | R1: 12-1, 12-3, 12-7 replaced per the ready text; 12-2, 12-4, 12-5, 12-6, 12-8, 12-9 verbatim; header «(владелец, 13.11 и 16.11.2026)» as the ready text | K5, K1 |
| PT13 | «13. **Проверки билдера**» | boot: pointer to 7b + dispatcher sentence 13-g; 13-b, 13-e -> builder-rules 7b (B-3, B-6); 13-a, c, d, f K4 | K4, K2, K1, K3 |
| PT-check | «Проверка на пути исполнения: …» | TEAMWORK last line; boot «Проверка на пути исполнения и детектор — `docs/TEAMWORK.md`.» | K2, K3 |
| PRel | `## Релиз` body | RUNBOOK `### 4.1. Шаги релиза` (end of §4, before `## 5.`) verbatim; PROJECT `## Релиз` + «Правило: `docs/RUNBOOK.md` § 4.1.» | K2, K3 |
| P-new | -- | `## Сессия форджа`, `## Бэклог и находки`, `## Как пишутся правила для агентов` (spec §6 text verbatim, placed between «Релиз» and «Язык») | K1/K2 |
| B-1..B-7 | builder-rules 7, 7b, 7c | as the card (B-3, B-6 insert 13-b, 13-e; B-5 moves the integrator sentence to RUNBOOK, leaves «что интегратор гоняет локально — `docs/RUNBOOK.md` §7;») | K3/K2/K5 |
| RB-1..RB-4 | RUNBOOK | RB-1 «координатор прогоняет ветку»; RB-2 «(`plans/builder-rules.md` п. 7b)»; RB-3 «`PROJECT.md` § Сессия форджа»; RB-4 §4.1; plus paragraph «**Интегратор.**» after «Прогнать ветку» = 2-12 + the 7b integrator sentence (F17 a); 2-15 + R5 clause in «Что остаётся локально и почему» | K5/K3/K2 |
| R1, R2, R3, R5 | -- | R1 PT12 + C12b(1); R2 B-2, B-7 (+ п. 2 clause 2-4 gone: «до минуты» absent from PROJECT and builder-rules); R3 RB-1 (S3 did builder-rules 2, 7b); R5 RUNBOOK: both sentences side by side + «(оба условия вместе — слово владельца 17.11.2026).» | K5 |
| CL-1 | CLAUDE.md imports; pin | `@docs/OWNER_PRINCIPLES_INDEX.md` own line after `@docs/ARCHITECTURE_INDEX.md`; pin row of `test_claude_imports_sees_the_real_repo_imports` gets the 4th item | K1 |
| C12b (1),(2) | CLAUDE.md rule 12 Cost gates | (1) «a push before a worktree launch (`tools/dispatch_gate.py`). The writers, the FULL queue, …»; (2) «the Lead compacts by PROJECT.md § Сессия форджа». Only CLAUDE.md edits besides the import | K5, K4+TR1 |
| test rows | `tools/tests/test_role_carriers_one_owner.py` | OWNER_KEYS `cost:queue` -> «цель держать 6 пишущих билдеров»; POINTERS: PROJECT->TEAMWORK § 2,3,4,8,9, PROJECT->OWNER_PRINCIPLES (`- **P31.**`), PROJECT->RUNBOOK § 4.1, PROJECT->RUNBOOK §7, PROJECT «правило: § Бэклог и находки», RUNBOOK->PROJECT § Сессия форджа, builder-rules->RUNBOOK §7, TESTING->7b, BRIEF->7b (S3's rows, from t-918 report) | rows |

Sweep inside the PROJECT unit: other items of «Командная работа» (1, 5, 6, 7, 10, 11), PA5, PA6, «Новая идея», «Язык», «Что решать самому», «Ссылки» -> not rows of the card, untouched (n/a). The D-0067 sentences (step 1 of «Новая идея», п. 5 «или Архитектор (D-0067)») travelled verbatim.

## Edge E20 (п. 9)
t-907's п. 9 edit is NOT on disk: its spec exists (`docs/tasks/specs/20261117-everything-in-piles-spec.md`) but `git log -- PROJECT.md` has no t-907 commit and п. 9 reads as in spec 3.4b (9a..9f verbatim). Per the dispatch п. 9 was moved as it stands today. The Lead re-syncs t-907 (gated clauses into TEAMWORK § 9, discipline into PROJECT п. 9).

## BOOT BUDGET
Before (worktree at start): `BOOT BUDGET: 128930 bytes / 120000 (4 files + 3 imports) BREACH -> boot-diet due ... | CLAUDE.md: 47120/47800 incl. imports 117908`
After: `BOOT BUDGET: 107885 bytes / 120000 (4 files + 4 imports) | CLAUDE.md: 47129/47800 incl. imports 96863`
Spec 5.2: ≈ 107.7 KB est. for the whole node (includes S1's CLAUDE TOC and headings, which S2 does not land). Measured 107885 is under 108000 by only 115 B with S1 still to come (CLAUDE TOC about 2 KB est.): E22 will fire in S1 unless F19 (a)/(d) is applied. Reported, not fixed.

## Deviations / findings from reality
1. Spec line numbers are stale; sources identified by opener text.
2. `tools/test_agents_md.py` (in the DoD) builds fixture `real_copy` from a hardcoded import tuple; the 4th import makes it fail: `agents md: missing import docs/OWNER_PRINCIPLES_INDEX.md (imported from CLAUDE.md line 21)` (7 errors). Not in S2's owns. Probe: byte copy to the scratchpad, `"docs/OWNER_PRINCIPLES_INDEX.md"` added to the tuple at line 73, DoD pair run -> `109 passed in 11.15s`, restored from the copy (sha256 prefix `ac6686ceacdfd189` before and after; `git status` clean for that file). The edit is NOT in the staged change.
3. Clause 2-15 drops «(там же)» per the card; its DOC-DISPATCH key is two keys around the gap (2-15a, 2-15b) plus an absence check.
4. 2-15 is inserted right after «…(слово владельца 03.11.2026: канон — на CI).» as the card says; «Тогда исходники — клон ветки…» now follows the R5 clause (critic may judge the connective).
5. PROJECT `## Оглавление` second column header is «О чём» (the «≤ 8 слов» limit applies to cells).
6. The CLAUDE.md import line has no intro sentence of its own (the card names only the line).

## Questions
1) `tools/test_agents_md.py` needs `"docs/OWNER_PRINCIPLES_INDEX.md"` in the file tuple of fixture `real_copy` (line 73) for DoD 1 to go green; outside S2's owns. Lead edit at commit, or a one-line follow-up dispatch? Left undone.
2) Placement of `## Как пишутся правила для агентов` is not fixed by the card; put between «Релиз» and «Язык». Confirm or name another place.

## Needed beyond the manifest
read: `docs/tasks/handoffs/t-918-boot-s3.md`, `tools/test_agents_md.py`, `docs/tasks/specs/20261117-everything-in-piles-spec.md` (grep), `docs/TESTING.md`, `docs/tasks/critic-diff-brief.md` (grep). Edit needed beyond owns: `tools/test_agents_md.py` (Question 1).

## Analogs noticed (not widened)
- Batch headers «BATCH CANON — интегратор» (spec A7) untouched.
- RUNBOOK:164, 208, 346, 352, 377 cite «Командная работа» п. 2/4 and «Прогоны и эксперименты» by name; resolve in 2 hops, no edit (spec 7.5).
- SIBLING_MAP axis 31 rows, the `:308` item-3 edit, the check-33 line and the four-question commit block remain the Lead's (non-goal).

## Witness (verbatim)

```
$ python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_agents_md.py -q   (tail 8)
ERROR tools/test_agents_md.py::test_real_imports_expanded - AssertionError: a...
ERROR tools/test_agents_md.py::test_every_real_hook_command_in_table - Assert...
ERROR tools/test_agents_md.py::test_real_hook_purposes_are_docstring_first_paragraphs
ERROR tools/test_agents_md.py::test_real_tool_names_sentence_has_multiedit - ...
ERROR tools/test_agents_md.py::test_every_real_role_file_in_table - Assertion...
ERROR tools/test_agents_md.py::test_tier_words_from_validator - AssertionErro...
ERROR tools/test_agents_md.py::test_real_size_notice - AssertionError: assert...
102 passed, 7 errors in 10.78s

$ python -m pytest tools/test_session_context.py -q -k imports
...............                                                          [100%]
15 passed, 294 deselected in 2.01s

$ python -B tools/agents_md.py --repo <worktree>   then   --check
wrote AGENTS.md: 106729 bytes
AGENTS.md: up to date (106729 bytes)
exit 0

$ python -B tools/factory_rules_index.py --check
factory rules index: up to date (59 rules)
factory rules index: up to date (31 rules)
exit 0

$ python -B tools/install_parity.py --check   (MISSING/UNKNOWN/informational lines)
exit 0
6:MISSING (0)
8:UNKNOWN (0)
10:informational (0)

$ python -B tools/piles.py check --all   (last line)
piles check: ok

$ echo '{}' | python -B tools/session_context.py   (BOOT BUDGET)
BOOT BUDGET: 107885 bytes / 120000 (4 files + 4 imports) | CLAUDE.md: 47129/47800 incl. imports 96863
```

### DOC-DISPATCH run (spec 7.4) over every K2/K4 row of S2

Keys: clause boundaries (start/end phrases) are quoted verbatim from the spec rows 3.2, 3.4a-3.4d and 7.2 (B-, RB-, PI-, CL-) as written; each clause is cut from the ORIGINAL files (byte copies taken before the first edit); key = first 60 + last 60 characters of the squashed clause (whole if < 120); squash = `" ".join(text.split()).casefold()`. Flags per key: present-in-destination, absent-from-source, one-home (exactly one occurrence across PROJECT, OWNER_PRINCIPLES, TEAMWORK, RUNBOOK, builder-rules, CLAUDE, TESTING = INV-M: nothing lost, nothing in two homes), K1 rows present-in-boot, K4 rows present-in-home. Exit 1 on any `no`.

Run: `python -B doc_dispatch.py <worktree> <orig_dir>`  -> output (full, 186 lines):

```
P1       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p1.** код помогает роли, но не мешает и не заменяет её: '
P1       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='при непредвиденном код сообщает, а не останавливает фабрику.'
P2       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p2.** фабрика универсальна: не переводить в код то, где встречаетс'
P3       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p3.** дирижёр — помощник при проблемах, а не запускатель'
P3       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='анды запускает код по переходу стадии или появлению вопроса.'
P4       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p4.** собранный материал передаётся дальше в yaml, чтобы ничего не'
P5       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p5.** получать данные (особенно исходные данные задачи) '
P5       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='аранее невозможно. владелец, 01.10 и 13.10 (d-0043, d-0047).'
P6       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p6.** джев не для того, чтобы экономить на нём самом, а чтобы сним'
P7       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p7.** фабрика работает на sonnet или terra. haiku не используется '
P8       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p8.** эксперименты по сравнению версий фабрики не оставл'
P8       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='омментариев и сабтасков в jira, баги только в md или в чате.'
P9       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p9.** любой вопрос человеку — человеческим языком (никаких `person'
P10      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p10.** карта проекта и оси симметрии: похожая логика на разных ста'
P11      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p11.** мерить трение ролей о наш код; код, от которого стадия доро'
P12      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p12.** любой новый код проверяется на похожие места и на трение.'
P13      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p13.** слово человека проводит фабрику через любой гейт; проход за'
P14      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p14.** ролям — только нужные инструменты.'
P15      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p15.** отказ говорит, что не так и чего ожидают; не назы'
P15      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key=', но у него всегда есть дверь; роль в ловушке пишет находку.'
P16      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p16.** пирамида: e2e-кейсов как можно меньше — изменение'
P16      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key=' параметрами, не четыре кейса. владелец, 30.09 и 04.11.2026.'
P17      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p17.** кейс говорит, что проверить; автоматор решает, ка'
P17      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='н ли новый там, где можно дополнить старый. владелец, 30.09.'
P18      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p18.** цена задачи — одна и истинная: включает всё, что '
P18      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='расход роли; добыча данных — расход скаута. владелец, 30.09.'
P19      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p19.** как проверять кейс, решается снизу пирамиды вверх'
P19      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='ета человека, проходит эту лестницу заново. владелец, 30.09.'
P20      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p20.** код никогда не оракул: тест, чьё ожидание взято и'
P20      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='а не зелёный или красный результат. владелец, 01.10 (fr-58).'
P21      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p21.** у доставки три исхода, не два. `delivery_ready: y'
P21      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='ет наружу всё, что открывает `yes`. владелец, 02.10 и 03.10.'
P22      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p22.** фабрика не справляется, не понимает или не может '
P22      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='всю фабрику — не строка в каждой фазе. владелец, 02.11.2026.'
P23      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p23.** фабрика работает по требованиям, не по ac. accept'
P23      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='фе — дефект носителя. владелец, 19.10.2026 (d-0049, d-0050).'
P24      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p24.** регрессию фабрика находит и отдаёт человеку, но с'
P24      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='нами» дефектом регрессии не считается. владелец, 30.10.2026.'
P25      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p25.** настройки хоста и гейтвея, через которые проект х'
P25      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='«keep-alive» тоже не строится. владелец, 27.10 и 05.11.2026.'
P26      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p26.** ручной кейс проходит агент, доказательства за ним'
P26      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='ивает странности строками `surprise:`. владелец, 04.11.2026.'
P27      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p27.** код владеет данными, роль — суждением и исходом, '
P27      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key=' и не судит по нему полноту регрессии. владелец, 04.11.2026.'
P28      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p28.** автоматизируется то, что будет гоняться много раз'
P28      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='тор (s5) по-прежнему решает как (p17). владелец, 04.11.2026.'
P29      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p29.** автотест пишут так: сначала определяют, какие про'
P29      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='огон, зависимые — по прогону на звено. владелец, 06.11.2026.'
P30      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p30.** красная проба по умолчанию подставляет значение, '
P30      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='нии; в остальных случаях смотрит роль. владелец, 06.11.2026.'
P31      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='- **p31.** разные рабочие пути для одного и того же — баг: в'
P31      OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='ение возможно только словом владельца. владелец, 06.11.2026.'
PA4      OK   | present-in-destination=yes one-home=yes | key='новая находка — файл в `findings/` своей кучки и строка в не'
PA4      OK   | present-in-destination=yes one-home=yes | key='е чинится сейчас, — строка в `design/factory-rules-debt.md`.'
PR5      OK   | present-in-destination=yes one-home=yes | key='**рабочий каталог шелла не меняется никогда** — ни `cd` в ba'
PR5      OK   | present-in-destination=yes one-home=yes | key='«не нашёл tools/x.py» — стоп и сброс папки сессии на корень.'
PR6      OK   | present-in-destination=yes one-home=yes | key='**коннекторы выключены** в сессиях форджа по умолчанию (gmai'
PR6      OK   | present-in-destination=yes one-home=yes | key='ой сессии); jira-агент включается только по слову владельца.'
PR7a     OK   | present-in-destination=yes one-home=yes | key='**сжатие контекста ничего не останавливает**: на ~300k контекста'
PR7b     OK   | present-in-destination=yes one-home=yes | key='— одна строка владельцу «контекст ≈ nnnk, снимок готов, можн'
PR7b     OK   | present-in-destination=yes one-home=yes | key=' /compact — ошибка: простаивающая сессия — потерянное время.'
TR1      OK   | ok=yes | key='на ~300K контекста, на границе стадии,'
C12b2    OK   | ok=yes old_absent=yes | key='compacts by PROJECT.md § Сессия форджа'
2a       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='**взятая пачка заморожена** (`piles.py check` (в), гейт comm'
2a       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='; в строке карточки — только «статус» и «mr» (ссылка на pr).'
2b       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='новое по теме — файлом в `findings/`, никогда строкой в чужую пачку.'
2c       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='**находка сразу попадает в пачку** (d-0044): тем же ходом, ч'
2c       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key=' строкой в таблице «пачки» карточки, и находка ложится туда.'
2d       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='тем же ходом находка получает строку в таблице «содержание» '
2d       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='её `tools/test_pile_cards_contents.py` красит `forge-check`.'
2e       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='взятие (или решение lead «пачка полна») замораживает её, сле'
2e       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='тектор — `piles.py check` (е), полный аудит — `check --all`.'
2f       OK   | present-in-boot=yes one-home=yes | key='**находка называет класс фабрики, не правило одного проекта*'
2f       OK   | present-in-boot=yes one-home=yes | key='фах — ссылки и доступ к знаниям онбординга, не копии текста.'
2g       OK   | present-in-boot=yes one-home=yes | key='перед «что сделать» — `grep` по `decisions.md` и `docs/decisions_archi'
3a       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='**зоны файлов пачек «в работе» не пересекаются** (`check` (б'
3a       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='чей (`story_run.py (take_answer, fallback_person)` — d-0048)'
3b       OK   | present-in-boot=yes one-home=yes | key='поздний узел сливает `main` в своё дерево и решает конфликт '
3b       OK   | present-in-boot=yes one-home=yes | key='ния; зависимость по замыслу спеки остаётся последовательной.'
3c       OK   | present-in-boot=yes one-home=yes | key='пачки одного разработчика друг друга не держат (владелец, 13.11.2026).'
4a       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='**`plans/backlog.md` заморожен** (`check` (г)): новых строк '
4a       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='о слову владельца — `close --id b-nnn --word "<кто, дата>"`.'
4b       OK   | present-in-boot=yes one-home=yes | key='b-id выдаёт только интегратор на `main` при сборке пачки; у находки до'
8a       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='**двери**: строка `piles-skip: <пункт> -- <причина>` в сообщ'
8a       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='трогает, и `.py`, названный в списке функций активной пачки.'
9a-p1    OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='**пачка закрывается доделкой, не переносом**: `close <slug> '
9a-p1    OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='оса `перенос: … | обоснование: … | подтвердил: <кто, дата>`;'
9a-p2    OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='строка «остатков» с записи несёт исполнителя — `сделано:`, `'
9a-p2    OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='piles.py check` (д); `release` — отказной псевдоним `close`.'
9b       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='то же — для таблицы «живые доказательства» (fr-33): `close` '
9b       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='ом ` \\| `; таблица из одной шапки = доказательств не должно.'
9c-in-TW OK   | absent-from(docs/TEAMWORK.md)=yes | key='перенос подтверждает **человек**, не агент сам'
9c       OK   | present-in-boot=yes one-home=yes | key='перенос подтверждает **человек**, не агент сам'
9d       OK   | present-in-boot=yes one-home=yes | key='**остатков в идеале нет вовсе**: минорные замечания критика '
9d       OK   | present-in-boot=yes one-home=yes | key=' переносятся в соответствующие кучки строкой с исполнителем.'
9e       OK   | present-in-boot=yes one-home=yes | key='закрытые по тексту строки помечает lead, не владелец.'
9f       OK   | present-in-boot=yes one-home=yes | key='**живые прогоны не держат пачку вообще** (владелец, 11.11.20'
9f       OK   | present-in-boot=yes one-home=yes | key='е доказана», пока её строка в `live-runs` не снята прогоном.'
ck       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='проверка на пути исполнения: `tools/piles.py check --msg-fil'
ck       OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='eck` (`check --base`); детектор — калибровочная проверка 33.'
12-1-old OK   | absent-from(PROJECT.md)=yes | key='в работе всегда шесть пишущих билдеров'
12-3-old OK   | absent-from(PROJECT.md)=yes | key='меньше шести — только по слову владельца «экономим время / токены»'
12-7-old OK   | absent-from(PROJECT.md)=yes | key='шесть — не потолок: седьмого координатор берёт, когда надо (упал мерж)'
R1(a)    OK   | present-in-home(PROJECT.md)=yes | key='цель держать 6 пишущих билдеров (если не сказано в этой сессии иного) '
R1(b)    OK   | present-in-home(PROJECT.md)=yes | key='можно запустить 7, если координатору надо, например упал ci и его надо'
R1(c)    OK   | present-in-home(PROJECT.md)=yes | key='6 — это цель, но не ценой ущерба эффективности (например, решать мерж-'
12-2     OK   | present-in-boot=yes one-home=yes | key='дизайнеры, критики и скауты в счёт не идут и слота не ждут.'
12-4     OK   | present-in-boot=yes one-home=yes | key='шесть — цель, а не потолок экономии: ограничение владельца ('
12-4     OK   | present-in-boot=yes one-home=yes | key='ы откатываются в понедельник вечером (владелец, 16.11.2026).'
12-5     OK   | present-in-boot=yes one-home=yes | key='критик кода — один на тему, не на узел.'
12-6     OK   | present-in-boot=yes one-home=yes | key='волны слияния ci не ждут: принятое сливается в `main` через `tools/wav'
12-9     OK   | present-in-boot=yes one-home=yes | key='тем же ходом, что слияние: статусы узлов в пачках обновлены, слитые ве'
C12b1    OK   | present-in-home(CLAUDE.md)=yes | key='a push before a worktree launch (`tools/dispatch_gate.py`). the writer'
C12b1-old OK   | absent-from(CLAUDE.md)=yes | key='at most 6 parallel writing workers'
C12b1-old OK   | absent-from(CLAUDE.md)=yes | key='the cap, the full queue'
13-a     OK   | present-in-home(plans/builder-rules.md)=yes | key='точечные проверки своей правки'
13-b     OK   | present-in-home(plans/builder-rules.md)=yes | key='билдер **ci не запускает и не ждёт** — ни пайплайн ветки, ни канон (сл'
13-b-src OK   | absent-from(PROJECT.md)=yes | key='**ci не запускает и не ждёт**'
13-c     OK   | present-in-home(plans/builder-rules.md)=yes | key='судит канон пачки'
13-d     OK   | present-in-home(CLAUDE.md)=yes | key="the coordinator's duty"
13-d     OK   | present-in-home(plans/builder-rules.md)=yes | key='его запускает координатор'
13-e     OK   | present-in-home(plans/builder-rules.md)=yes | key='пайплайн `main` читают только интегратор волны и билдер, чинящий красн'
13-e-src OK   | absent-from(PROJECT.md)=yes | key='пайплайн `main` читают только интегратор волны'
13-f     OK   | present-in-home(plans/builder-rules.md)=yes | key='мутации судит канон пачки'
13-f-src OK   | absent-from(PROJECT.md)=yes | key='**мутации** билдер не прогоняет'
13-g     OK   | present-in-boot=yes one-home=yes | key='диспатч, который просит билдера запустить ci, ждать пайплайн или гонят'
13-h     OK   | present-in-home(PROJECT.md)=yes | key='`plans/builder-rules.md` п. 7b'
2-6      OK   | present-in-boot=yes one-home=yes | key='цикл ожидания в диспатче — один на раунд, с капом, и только '
2-6      OK   | present-in-boot=yes one-home=yes | key='ра; пайплайн — только интегратору, «командная работа» п. 13)'
2-9      OK   | present-in-boot=yes one-home=yes | key='диспатч интегратору или билдеру, требующий большего локально, — дефект'
2-3      OK   | present-in-home(plans/builder-rules.md)=yes | key='не гоняет и не ждёт'
2-4      OK   | present-in-home(plans/builder-rules.md)=yes | key='точечные проверки своей правки'
2-5      OK   | present-in-home(plans/builder-rules.md)=yes | key='`slow_tests`'
2-5      OK   | present-in-home(plans/builder-rules.md)=yes | key='`test_fixes_13797`'
2-7      OK   | present-in-home(CLAUDE.md)=yes | key='the test file that judges the path'
2-7      OK   | present-in-home(plans/builder-rules.md)=yes | key='`pytest tools/` целиком'
2-8      OK   | present-in-home(docs/RUNBOOK.md)=yes | key='канон всегда на ci'
2-8      OK   | present-in-home(docs/RUNBOOK.md)=yes | key='не больше часа'
2-10     OK   | present-in-home(plans/builder-rules.md)=yes | key='на машине их не гоняет никто'
2-11     OK   | present-in-home(docs/RUNBOOK.md)=yes | key='кроме раздела `quarantine`'
2-11     OK   | present-in-home(docs/TESTING.md)=yes | key='`quarantine-watch`'
2-11     OK   | present-in-home(docs/TESTING.md)=yes | key='только по слову владельца'
2-13     OK   | present-in-home(docs/RUNBOOK.md)=yes | key='пуш ветки без pr ничего не запускает'
2-12     OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='интегратор перед коммитом гоняет только свидетелей узлов и `'
2-12     OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='одка в `findings/` своей кучки и починка до следующего пуша.'
2-15a    OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='локальный прогон и локальный докер — только запасной путь'
2-15b    OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='только по слову владельца и никогда не параллельно с другим;'
2-15b    OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='огда лог ci не читается — сначала сказать об этом владельцу.'
2-15-там-же OK   | absent-from(docs/RUNBOOK.md)=yes | key='запасной путь (там же)'
R5       OK   | present-in-home(docs/RUNBOOK.md)=yes | key='локальный прогон (докер) — запасной путь, только когда ci недоступен и'
R5       OK   | present-in-home(docs/RUNBOOK.md)=yes | key='(оба условия вместе — слово владельца 17.11.2026)'
R5-order OK   | ok=yes | key='R5 sentences in one paragraph, in order'
2-1/2-2  OK   | present-in-home(PROJECT.md)=yes | key='2. **свидетель билдера** — вывод проверки, а не пересказ.'
2-1/2-2  OK   | present-in-home(PROJECT.md)=yes | key='правила `plans/builder-rules.md` п. 7b (d-0056)'
2-1/2-2  OK   | present-in-home(PROJECT.md)=yes | key='`docs/tasks/critic-diff-brief.md` («the two layers»)'
2-1/2-2  OK   | present-in-home(PROJECT.md)=yes | key='форма отчёта — правило 7 `.claude/agents/builder.md`, содержание — bui'
2-14     OK   | present-in-home(PROJECT.md)=yes | key='ci, канон пачки, слияние и запасной локальный прогон — `docs/runbook.m'
R2       OK   | absent-from(PROJECT.md)=yes | key='до минуты каждый'
R2       OK   | absent-from(plans/builder-rules.md)=yes | key='до минуты'
R2       OK   | absent-from(plans/builder-rules.md)=yes | key='меньше минуты'
PRel     OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='шаг отпечатка (d-0052 (3), узел cl1-8, 20.10.2026): после ко'
PRel     OK   | present-in-destination=yes absent-from-source=yes one-home=yes | key='ько `readme.md` — релизный коммит с фрагментами не делается.'
PRel-ptr OK   | present-in-home(PROJECT.md)=yes | key='правило: `docs/runbook.md` § 4.1.'
B-1      OK   | present-in-home(plans/builder-rules.md)=yes | key='(d-0059, `docs/runbook.md` §7)'
B-1-old  OK   | absent-from(plans/builder-rules.md)=yes | key='(d-0059, `project.md`'
B-2      OK   | present-in-home(plans/builder-rules.md)=yes | key='(критерий — список, а не длительность)'
B-4      OK   | absent-from(plans/builder-rules.md)=yes | key='`project.md` «командная работа» п. 13'
B-4      OK   | present-in-home(plans/builder-rules.md)=yes | key='(слово владельца 28.10 и 10.11.2026)'
B-5      OK   | present-in-home(plans/builder-rules.md)=yes | key='(слово владельца 03.11.2026): что интегратор гоняет локально — `docs/r'
B-5-src  OK   | absent-from(plans/builder-rules.md)=yes | key='интегратор локально гоняет только узкие свидетели'
B-5-src  OK   | absent-from(plans/builder-rules.md)=yes | key='project.md п. 2'
B-5-dest OK   | present-in-home(docs/RUNBOOK.md)=yes | key='интегратор локально гоняет только узкие свидетели узлов с конфликтом с'
B-7      OK   | present-in-home(plans/builder-rules.md)=yes | key='точечные файлы, не из списка'
S3-dep   OK   | present-in-home(plans/builder-rules.md)=yes | key='файл карантина билдер не запускает'
S3-dep   OK   | present-in-home(plans/builder-rules.md)=yes | key='мутации судит канон пачки'
S3-dep   OK   | present-in-home(plans/builder-rules.md)=yes | key='не регрессия, не соседи, не большие файлы'
S3-dep   OK   | present-in-home(plans/builder-rules.md)=yes | key='--witness-for'
S3-dep   OK   | present-in-home(plans/builder-rules.md)=yes | key='строки `keep`'
RB-1     OK   | present-in-home(docs/RUNBOOK.md)=yes | key='после схождения веток координатор прогоняет ветку, как выше.'
RB-1-old OK   | absent-from(docs/RUNBOOK.md)=yes | key='после схождения веток интегратор'
RB-2     OK   | present-in-home(docs/RUNBOOK.md)=yes | key='мутации судит канон пачки (`plans/builder-rules.md` п. 7b).'
RB-3     OK   | present-in-home(docs/RUNBOOK.md)=yes | key='— `project.md` § сессия форджа.'
RB-3-old OK   | absent-from(docs/RUNBOOK.md)=yes | key='`project.md`, «прогоны и эксперименты».'
CL-1     OK   | present-in-home(CLAUDE.md)=yes | key='@docs/owner_principles_index.md'
CL-1pin  OK   | ok=yes | key='pin row'
ROWS=185 FAILS=0 []
```

NEGATIVE control (same script, `--mutate`: every key altered by one character at position 5) -> exit 1; last line and count of FAIL lines:

```
ROWS=185 FAILS=162 ['12-2', '12-4', '12-5', '12-6', '12-9', '13-a', '13-b', '13-c', '13-d', '13-e', '13-f', '13-g', '13-h', '2-1/2-2', '2-10', '2-11', '2-12', '2-13', '2-14', '2-15a', '2-15b', '2-3', '2-4', '2-5', '2-6', '2-7', '2-8', '2-9', '2a', '2b', '2c', '2d', '2e', '2f', '2g', '3a', '3b', '3c', '4a', '4b', '8a', '9a-p1', '9a-p2', '9b', '9c', '9d', '9e', '9f', 'B-1', 'B-2', 'B-4', 'B-5', 'B-5
FAIL lines: 162
```

### The DOC-DISPATCH script in full (not committed; lives in the scratchpad)

```python
"""DOC-DISPATCH witness for boot-by-topic S2 (spec 7.4). NOT committed. python -B doc_dispatch.py <worktree> <orig_dir> [--mutate]

Clause boundaries (start .. end phrases) are quoted VERBATIM from the spec rows of 3.2 / 3.4a-3.4d / 7.2 (S2 rows).
The clause text is cut from the ORIGINAL files (copies taken before any edit); keys = first 60 + last 60 characters of
the squashed clause (whole when < 120). squash == `" ".join(text.split()).casefold()` of test_role_carriers_one_owner.
"""
import pathlib, re, sys

W = pathlib.Path(sys.argv[1])
O = pathlib.Path(sys.argv[2])
MUTATE = "--mutate" in sys.argv


def squash(t):
    return " ".join(t.split()).casefold()


def cur(rel):
    return squash((W / rel).read_text(encoding="utf-8"))


def orig(rel):
    return squash((O / rel.replace("/", "__")).read_text(encoding="utf-8"))


def section(sq, heading, level="## "):
    h = squash(heading)
    a = sq.index(h)
    nxt = [m.start() for m in re.finditer(re.escape(level.strip()) + " ", sq[a + len(h):])]
    # next heading of the same or higher level
    b = len(sq)
    for m in re.finditer(r"(?:^| )#{2} ", sq[a + len(h):]):
        b = a + len(h) + m.start()
        break
    return sq[a:b]


def keys_of(clause):
    c = squash(clause)
    return [c] if len(c) < 120 else [c[:60], c[-60:]]


def cut(osq, start, end):
    s = osq.index(squash(start))
    e = osq.index(squash(end), s) + len(squash(end))
    return osq[s:e]


FAILS = []
ROWS = 0


def report(row, key, **flags):
    global ROWS
    ROWS += 1
    ok = all(flags.values())
    if not ok:
        FAILS.append(row)
    print("%-8s %s | %s | key=%r" % (row, "OK  " if ok else "FAIL", " ".join("%s=%s" % (k, "yes" if v else "no") for k, v in flags.items()), key[:70]))


def mut(k):
    return (k[:5] + ("x" if k[5] != "x" else "y") + k[6:]) if MUTATE and k else k


HOMES = ["PROJECT.md", "docs/OWNER_PRINCIPLES.md", "docs/TEAMWORK.md", "docs/RUNBOOK.md", "plans/builder-rules.md", "CLAUDE.md", "docs/TESTING.md"]
HOME_TEXT = {h: cur(h) for h in HOMES}


def count_all(key):
    return sum(t.count(key) for t in HOME_TEXT.values())


def k2(row, clause, dest, src="PROJECT.md", dest_section=None, skip_src_check=False):
    """K2: every key present in dest (optionally inside a section), absent from src, and in exactly one home."""
    for key in keys_of(clause):
        key = mut(key)
        d = HOME_TEXT[dest] if dest_section is None else section(HOME_TEXT[dest], dest_section)
        fl = {"present-in-destination": key in d}
        if not skip_src_check:
            fl["absent-from-source"] = key not in HOME_TEXT[src]
        fl["one-home"] = count_all(key) == 1
        report(row, key, **fl)


def k1(row, clause, where="PROJECT.md"):
    for key in keys_of(clause):
        key = mut(key)
        report(row, key, **{"present-in-boot": key in HOME_TEXT[where], "one-home": count_all(key) == 1})


def home(row, file, *phrases):
    """K4: the home holds the clause's key."""
    for p in phrases:
        key = mut(squash(p))
        report(row, key, **{"present-in-home(%s)" % file: key in HOME_TEXT[file]})


def absent(row, file, *phrases):
    for p in phrases:
        key = squash(p)
        report(row, key, **{"absent-from(%s)" % file: key not in HOME_TEXT[file]})


OP = orig("PROJECT.md")
ORU = orig("docs/RUNBOOK.md")

# ---- PI-1: P1..P31 (spec 3.2 rows P1..P31 -> OWNER_PRINCIPLES verbatim)
praw = (O / "PROJECT.md").read_text(encoding="utf-8")
ms = list(re.finditer(r"^- \*\*P(\d+)\.\*\*", praw, re.M))
assert len(ms) == 31
for i, m in enumerate(ms):
    e = ms[i + 1].start() if i + 1 < len(ms) else praw.index("## Как принимается изменение пакета")
    k2("P%d" % (i + 1), praw[m.start():e], "docs/OWNER_PRINCIPLES.md")

# ---- PA4 (K2 into new section) and PR5-PR7
k2("PA4", cut(OP, "Новая находка — файл в `findings/` своей кучки", "строка в `design/factory-rules-debt.md`."),
   "PROJECT.md", dest_section="## Бэклог и находки", skip_src_check=True)
k2("PR5", cut(OP, "**Рабочий каталог шелла не меняется никогда**", "сброс папки сессии на корень."),
   "PROJECT.md", dest_section="## Сессия форджа", skip_src_check=True)
k2("PR6", cut(OP, "**Коннекторы выключены**", "только по слову владельца."), "PROJECT.md", dest_section="## Сессия форджа", skip_src_check=True)
c7a = cut(OP, "**Сжатие контекста ничего не останавливает**: на ~300K контекста", "на ~300K контекста")
c7b = cut(OP, "— одна строка владельцу «контекст ≈ NNNK", "потерянное время.")
k2("PR7a", c7a, "PROJECT.md", dest_section="## Сессия форджа", skip_src_check=True)
k2("PR7b", c7b, "PROJECT.md", dest_section="## Сессия форджа", skip_src_check=True)
report("TR1", "на ~300K контекста, на границе стадии,", ok=squash("на ~300K контекста, на границе стадии,") in section(HOME_TEXT["PROJECT.md"], "## Сессия форджа"))
report("C12b2", "compacts by PROJECT.md § Сессия форджа",
       ok=squash("the Lead compacts by PROJECT.md § Сессия форджа") in HOME_TEXT["CLAUDE.md"], old_absent=squash("the Lead compacts at ~300K") not in HOME_TEXT["CLAUDE.md"])

# ---- 3.4b TEAMWORK clauses
k2("2a", cut(OP, "**Взятая пачка заморожена** (`piles.py check` (в)", "(ссылка на PR)."), "docs/TEAMWORK.md")
k2("2b", cut(OP, "Новое по теме — файлом в `findings/`", "никогда строкой в чужую пачку."), "docs/TEAMWORK.md")
k2("2c", cut(OP, "**Находка сразу попадает в пачку** (D-0044):", "и находка ложится туда."), "docs/TEAMWORK.md")
k2("2d", cut(OP, "Тем же ходом находка получает строку в таблице «Содержание»", "красит `forge-check`."), "docs/TEAMWORK.md")
k2("2e", cut(OP, "Взятие (или решение Lead «пачка полна») замораживает её,", "полный аудит — `check --all`."), "docs/TEAMWORK.md")
k1("2f", cut(OP, "**Находка называет класс фабрики, не правило одного проекта** (P2):", "не копии текста."))
k1("2g", cut(OP, "Перед «что сделать» — `grep` по `DECISIONS.md`", "на тему."))
k2("3a", cut(OP, "**Зоны файлов пачек «в работе» не пересаются**".replace("пересаются", "пересекаются") + " (`check` (б));", "— D-0048)"), "docs/TEAMWORK.md")
k1("3b", cut(OP, "поздний узел сливает `main` в своё дерево и", "остаётся последовательной."))
k1("3c", cut(OP, "Пачки одного разработчика друг друга не держат", "(владелец, 13.11.2026)."))
k2("4a", cut(OP, "**`plans/BACKLOG.md` заморожен** (`check` (г))", "`close --id B-nnn --word \"<кто, дата>\"`."), "docs/TEAMWORK.md")
k1("4b", cut(OP, "B-id выдаёт только интегратор на `main`", "у находки до этого `id: —`."))
k2("8a", cut(OP, "**Двери**: строка `piles-skip:", "активной пачки."), "docs/TEAMWORK.md")
k2("9a-p1", cut(OP, "**Пачка закрывается доделкой, не переносом**: `close <slug> <N>`", "подтвердил: <кто, дата>`;"), "docs/TEAMWORK.md")
k2("9a-p2", cut(OP, "строка «Остатков» с ЗАПИСИ несёт исполнителя", "`release` — отказной псевдоним `close`."), "docs/TEAMWORK.md")
k2("9b", cut(OP, "То же — для таблицы «Живые доказательства» (FR-33):", "доказательств не должно."), "docs/TEAMWORK.md")
absent("9c-in-TW", "docs/TEAMWORK.md", "перенос подтверждает **человек**, не агент сам")
k1("9c", cut(OP, "перенос подтверждает **человек**, не агент сам", "не агент сам"))
k1("9d", cut(OP, "**Остатков в идеале нет вовсе**: минорные", "строкой с исполнителем."))
k1("9e", cut(OP, "Закрытые по тексту строки помечает Lead", "не владелец."))
k1("9f", cut(OP, "**Живые прогоны не держат пачку вообще**", "снята прогоном."))
k2("ck", cut(OP, "Проверка на пути исполнения: `tools/piles.py check --msg-file`", "калибровочная проверка 33."), "docs/TEAMWORK.md")

# ---- 3.4c п. 12 (R1)
for r, old in (("12-1", "в работе всегда шесть пишущих билдеров"),
               ("12-3", "меньше шести — только по слову владельца «экономим время / токены»"),
               ("12-7", "Шесть — не потолок: седьмого координатор берёт, когда надо (упал мерж)")):
    absent(r + "-old", "PROJECT.md", old)
home("R1(a)", "PROJECT.md", "цель держать 6 пишущих билдеров (если не сказано в этой сессии иного) и не меньше, если есть параллельная работа (цель сессии + П1 из бэклога)")
home("R1(b)", "PROJECT.md", "Можно запустить 7, если координатору надо, например упал CI и его надо починить, — дверью `budget-skip:`")
home("R1(c)", "PROJECT.md", "6 — это цель, но не ценой ущерба эффективности (например, решать мерж-конфликты будет дороже, так что запустить в параллельность сейчас нечего)")
k1("12-2", cut(OP, "дизайнеры, критики и скауты в счёт не идут и слота не ждут.", "слота не ждут."))
k1("12-4", cut(OP, "Шесть — цель, а не потолок экономии:", "(владелец, 16.11.2026)."))
k1("12-5", cut(OP, "Критик кода — один на тему, не на узел.", "не на узел."))
k1("12-6", cut(OP, "Волны слияния CI не ждут:", "красный CI чинит там один билдер."))
k1("12-9", cut(OP, "Тем же ходом, что слияние:", "слитые ветки и папки деревьев убраны."))
home("C12b1", "CLAUDE.md", "a push before a worktree launch (`tools/dispatch_gate.py`). The writers, the FULL queue, the per-topic critic and merge waves: PROJECT.md «Командная работа» п. 12.")
absent("C12b1-old", "CLAUDE.md", "at most 6 parallel WRITING workers", "The cap, the FULL queue")

# ---- 3.4d п. 13
home("13-a", "plans/builder-rules.md", "точечные проверки своей правки")
home("13-b", "plans/builder-rules.md", "Билдер **CI не запускает и не ждёт** — ни пайплайн ветки, ни канон (слово владельца 14.11.2026).")
absent("13-b-src", "PROJECT.md", "**CI не запускает и не ждёт**")
home("13-c", "plans/builder-rules.md", "судит канон пачки")
home("13-d", "CLAUDE.md", "the coordinator's duty")
home("13-d", "plans/builder-rules.md", "его запускает координатор")
home("13-e", "plans/builder-rules.md", "Пайплайн `main` читают только интегратор волны и билдер, чинящий красный `main` (слово владельца 14.11.2026).")
absent("13-e-src", "PROJECT.md", "пайплайн `main` читают только интегратор волны")
home("13-f", "plans/builder-rules.md", "мутации судит канон пачки")
absent("13-f-src", "PROJECT.md", "**Мутации** билдер не прогоняет")
k1("13-g", cut(OP, "Диспатч, который просит билдера запустить CI, ждать пайплайн или гонять мутации, — дефект координатора.", "дефект координатора."))
home("13-h", "PROJECT.md", "Полный текст", ) if False else home("13-h", "PROJECT.md", "`plans/builder-rules.md` п. 7b")

# ---- 3.4a п. 2
k1("2-6", cut(OP, "цикл ожидания в диспатче — один на раунд, с капом", "«Командная работа» п. 13)"))
k1("2-9", cut(OP, "диспатч интегратору или билдеру, требующий большего локально", "дефект координатора."))
home("2-3", "plans/builder-rules.md", "НЕ гоняет и не ждёт")
home("2-4", "plans/builder-rules.md", "точечные проверки своей правки")
home("2-5", "plans/builder-rules.md", "`SLOW_TESTS`", "`test_fixes_13797`")
home("2-7", "CLAUDE.md", "the test file that judges the path")
home("2-7", "plans/builder-rules.md", "`pytest tools/` целиком")
home("2-8", "docs/RUNBOOK.md", "Канон всегда на CI", "не больше часа")
home("2-10", "plans/builder-rules.md", "на машине их не гоняет никто")
home("2-11", "docs/RUNBOOK.md", "кроме раздела `quarantine`")
home("2-11", "docs/TESTING.md", "`quarantine-watch`", "только по слову владельца")
home("2-13", "docs/RUNBOOK.md", "пуш ветки без PR ничего не запускает")
c212 = cut(OP, "Интегратор перед коммитом гоняет только свидетелей узлов", "починка до следующего пуша.")
k2("2-12", c212, "docs/RUNBOOK.md")
c215a = cut(OP, "Локальный прогон и локальный докер — только запасной путь", "только запасной путь")
c215b = cut(OP, ", только по слову владельца и никогда не параллельно с другим", "сначала сказать об этом владельцу.")
c215b = c215b.lstrip(", ")
k2("2-15a", c215a, "docs/RUNBOOK.md")
k2("2-15b", c215b, "docs/RUNBOOK.md")
absent("2-15-там-же", "docs/RUNBOOK.md", "запасной путь (там же)")
home("R5", "docs/RUNBOOK.md",
     "Локальный прогон (докер) — запасной путь, только когда CI недоступен или красный по причине раннера, а не кода (слово владельца 03.11.2026: канон — на CI).",
     "(оба условия вместе — слово владельца 17.11.2026)")
rb = HOME_TEXT["docs/RUNBOOK.md"]
report("R5-order", "R5 sentences in one paragraph, in order",
       ok=rb.index("запасной путь, только когда ci недоступен") < rb.index("только по слову владельца и никогда не параллельно с другим") < rb.index("(оба условия вместе"))
home("2-1/2-2", "PROJECT.md", "2. **Свидетель билдера** — вывод проверки, а не пересказ.", "правила `plans/builder-rules.md` п. 7b (D-0056)", "`docs/tasks/critic-diff-brief.md` («The two layers»)", "Форма отчёта — правило 7 `.claude/agents/builder.md`, содержание — builder-rules п. 11.")
home("2-14", "PROJECT.md", "CI, канон пачки, слияние и запасной локальный прогон — `docs/RUNBOOK.md` §7.")
absent("R2", "PROJECT.md", "до минуты каждый")
absent("R2", "plans/builder-rules.md", "до минуты", "меньше минуты")

# ---- PRel / RB-4
crel = cut(OP, "Шаг отпечатка (D-0052 (3), узел CL1-8", "релизный коммит с фрагментами не делается.")
k2("PRel", crel, "docs/RUNBOOK.md", dest_section="### 4.1. Шаги релиза")
home("PRel-ptr", "PROJECT.md", "Правило: `docs/RUNBOOK.md` § 4.1.")

# ---- B rows
home("B-1", "plans/builder-rules.md", "(D-0059, `docs/RUNBOOK.md` §7)")
absent("B-1-old", "plans/builder-rules.md", "(D-0059, `PROJECT.md`")
home("B-2", "plans/builder-rules.md", "(критерий — список, а не длительность)")
absent("B-4", "plans/builder-rules.md", "`PROJECT.md` «Командная работа» п. 13")
home("B-4", "plans/builder-rules.md", "(слово владельца 28.10 и 10.11.2026)")
home("B-5", "plans/builder-rules.md", "(слово владельца 03.11.2026): что интегратор гоняет локально — `docs/RUNBOOK.md` §7;")
absent("B-5-src", "plans/builder-rules.md", "интегратор локально гоняет только узкие свидетели", "PROJECT.md п. 2")
home("B-5-dest", "docs/RUNBOOK.md", "Интегратор локально гоняет только узкие свидетели узлов с конфликтом слияния и `--limits --lang`, затем push")
home("B-7", "plans/builder-rules.md", "точечные файлы, НЕ из списка")
# 7b pinned strings S3 depends on
home("S3-dep", "plans/builder-rules.md", "Файл карантина билдер не запускает", "мутации судит канон пачки", "Не регрессия, не соседи, не большие файлы", "--witness-for", "строки `keep`")

# ---- RB rows
home("RB-1", "docs/RUNBOOK.md", "После схождения веток координатор прогоняет ветку, как выше.")
absent("RB-1-old", "docs/RUNBOOK.md", "После схождения веток интегратор")
home("RB-2", "docs/RUNBOOK.md", "Мутации судит канон пачки (`plans/builder-rules.md` п. 7b).")
home("RB-3", "docs/RUNBOOK.md", "— `PROJECT.md` § Сессия форджа.")
absent("RB-3-old", "docs/RUNBOOK.md", "`PROJECT.md`, «Прогоны и эксперименты».")

# ---- CL-1
home("CL-1", "CLAUDE.md", "@docs/OWNER_PRINCIPLES_INDEX.md")
tv = squash((W / "tools/test_session_context.py").read_text(encoding="utf-8"))
report("CL-1pin", "pin row", ok='"docs/owner_principles_index.md"]' in tv)

# ---- INV-M overall: every P and clause was checked with one-home == yes above
print("ROWS=%d FAILS=%d %s" % (ROWS, len(FAILS), sorted(set(FAILS))))
sys.exit(1 if FAILS else 0)
```

