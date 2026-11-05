# Гейт выхода отказал после лимита возобновлений — у дирижёра нет хода, человек получает общий вопрос без слов стори

id: — | кучка: `conductor` | от: прогон cmp3 13.10 16:08 (`experiments/measurers/runs/cmp3.md`, строка «Ход» 16:08) | приоритет: П1 | кандидат наверх: нет | **слово владельца 13.10: чинить в этой же пачке (conductor/1)**

Что случилось (S1, скаут, TP1-13797): гейт выхода отказал — `source-inventory.json: source materials lack retrieval or
inspection receipts` у трёх источников (все `status: read`, снимки лежат, `inspection_status: pending`). Код возобновил
скаута с отказом один раз (`story_run.py` :1577–1602, правило t-217 «одно возобновление на один набор находок»); расписок не
появилось; на втором входе — «was already resumed on these findings; no second resume» (:1580) → `Refusal` (:1629) →
дирижёр. **Уточнение по следу (дизайнер t-703, `state/conductor.jsonl` строки 7–8):** ходы у дирижёра были
(`resume_with_words`, `release_and_restart`/`restart`, `go_on_as_is`, `person_does`/`retry`, `stop_here`); он попробовал
`rework --stage S1 --role qa-scout` — контроллер отказал «no accepted qa-scout dispatch on S1», не назвав двери (C:1715,
FR-1/FR-2) — и затем написал ХОРОШИЙ вопрос словами стори («three sources the scout read … have no inspection receipts …
'retry': the driver resumes the scout … 'restart': I free the dispatch … 'stop'», $0.218). Валидатор шва
(`no_move.validate_options`) отверг его: «the backquoted tokens of the question are not the tokens of the options» —
токены стояли в одинарных кавычках, не в обратных — и человек получил общий запасной текст с тремя общими вариантами и
строкой «I cannot put that check's reason into the story's own words». Вдобавок дирижёр прочитал `retry` как «возобновить
скаута», а `person_does` этого не делает. Ответ `go on` прошёл (пропуск гейта словом человека, P13; на S1 одного `waiver`
мало — драйвер провёл `accept-gap --point source:not_inspected`), S1 принята без расписок, стори ушла на S2. Цена: вопрос
человеку + $0.22 дирижёра, выброшенные валидатором, вместо одного хода роли; расписки так и не написаны. Третье: старые слова
`s1_gap` (`pending_words`) пересылались скауту на каждом входе до чистой сдачи (три платных возобновления в cmp3).

Класс: «гейт выхода отказал после лимита возобновлений на НЕпринятом диспатче» — тот же, что `s5.nobody_*` /
`s5.repair_limit` в C1-5 (t-698), но на любой стадии с гейтом выхода (S1 сегодня; S5 в cmp2 — восемь возобновлений, t-217; S4
критик 26.09 — третье «механическое» возобновление :1607–1627 закрыло только механический подкласс). Ходы, которые есть у
кода и которых не предложил дирижёр: (а) ещё одно возобновление роли с точной инструкцией и словами человека (цена — один
ход роли); (б) отпустить диспатч и запустить роль заново по брифу (цена стадии); (в) идти дальше как есть — пропуск словом
человека, с последствием для стори (что именно не записано и куда это уедет); (г) стоп. Всё это — одна ценовая секция через
шов `_ask_conductor` (C1-3), ключ стадийно-независимый (`exit.resume_limit` или подобный, стадия подставляется в текст), как
`s5.repair_limit` (round / debt / fixed / stop).

Что сделать в conductor/1: узел **C1-5d** — отказ гейта выхода после лимита возобновлений идёт через шов с ценами по форме
C1-5 (шов спрашивает человека сам, без платного вызова дирижёра; дирижёр — только на непонятые слова); варианты
`round` / `fresh` / `go on` / `stop`, текст из структуры (точки работы инвентаря источников), не из текста гейта; отказ
контроллера `rework` на непринятом диспатче называет дверь (resume / release) — FR-1/FR-2, через C1-6a1; `validate_options`
не выбрасывает вопрос дирижёра из-за стиля кавычек — токен читается в любых кавычках, а при несовпадении вопрос чинится
кодом (токены известны), а не заменяется общим текстом; `pending_words` снимаются, когда шов поднимает вопрос по диспатчу.
Спека — t-698 §12 (дизайнер t-703) + §13 решения Lead; узел после C1-5b1 (очередь `C1-5b1 → C1-5d → C1-5b2` на
`story_run.py`).

Свидетель: `runs/cmp3-5.log` строки «resume S1-qa-scout-1: unclassified (…lack retrieval or inspection receipts…)»,
«S1: S1-qa-scout-1 was already resumed on these findings; no second resume», «conductor: ask_person — … Ran controller.py rework
--stage S1 --role qa-scout, which was refused: no accepted qa-scout dispatch on S1. Recorded nothing.»;
`state/driver-question.md` 16:08 (`kind: conductor`); `runs/cmp3-6.log` «accepted S1-qa-scout-1: 4 evidence files, stage
complete» после `go on`.

Принципы и правила: P22 (D-0039), P13, P9, FR-1, FR-2, FR-6, FR-42, FR-48, FR-57.

Решение владельца нужно: нет — дано 13.10 («это конечно надо чинить, в этой же пачке дирижёра»).
