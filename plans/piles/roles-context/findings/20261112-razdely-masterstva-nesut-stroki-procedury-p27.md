# В разделах мастерства (`kind: craft`) `qa-runner` и `qa-case-critic` стоят строки процедуры: фиксированные метки, команда `first_look.py put`, поле `about:`

id: — | кучка: `roles-context` | от: Lead, калибровка 12.11.2026 (`docs/tasks/specs/reports/calibration-20261112.md`, п. 13), записал builder t-093 | приоритет: П2 | кандидат наверх: нет

Кучка выбрана по смыслу: карточка `roles-context` («Роли, тексты и контекст», зона `agents/qa-*.md`) ведёт тексты ролей; кучка `thinking-roles`
тоже трогает роль ходока, но ведёт её поведение на прогоне, а не устав, поэтому не взята. Если Lead решит иначе — перенос строкой в той кучке.

## Что не так

Класс: «устав роли делится на МАСТЕРСТВО (опыт тестировщика: где искать баги, техники — P27) и ПРОЦЕДУРУ (форма, ключи, команды); строка
процедуры под меткой `craft` попадает в «долю мастерства» и ломает её смысл (счёт `role_load.py`) и принцип P27: процедура формы — работа
кода, а не опыта». Детектор: калибровочная проверка 41(d) — по её тексту процедура, помеченная `craft`, — находка.

Свидетель (часть p4, `docs/tasks/specs/reports/calibration-20261112-p4.md`, проверка 41(d); текст ролей прочитан напрямую):
- `ai-packages/qa-factory/agents/qa-runner.md`, раздел `## Techniques` (метка `<!-- kind: craft -->` на строке 39): строка 52 «Name the sides a
  walk speaks about ... write `about: [<side>]` in the case record» и строка 53 «First look ... send the rows once with `first_look.py put`»
  (вдобавок статусы `missing`/`unreachable`/`access`/`nature` и форма карты путей — это форма, не опыт).
- `ai-packages/qa-factory/agents/qa-case-critic.md`, раздел «Where bugs hide» (метка `craft` на строке 27, ещё одна на 77): «The eight dimensions
  (S4), each `pass`/`concern`/`fail`», фиксированные метки `parametrise into one test: <ids>` (строка 44), `## Merge candidates`,
  `oracle_field_absent`, `contradicts_source` (строка 59), перекличка. Оговорка записи: восемь измерений — рубрика; рубрика это мастерство или
  процедура — неоднозначно (Lead решает).
- доля мастерства по `role_load.py --all --json`: qa-runner 1538 из 15971 токенов (9,6 %), qa-case-critic 2367 из 18296 (12,9 %, самая высокая в
  наборе); `references/role-load.json` `process_ratchet_tokens` равен измеренному у всех двенадцати ролей.

## Что именно менять

Направление выбрано: переносится ПРОЦЕДУРА, мастерство остаётся; рубрика восьми измерений остаётся мастерством (что ищет критик), переносятся
только фиксированные метки и команды.

1. `ai-packages/qa-factory/agents/qa-runner.md`: строки 52–53 (форма `about:`, статусы строк первого просмотра, команда `first_look.py put`, форма
   карты путей) переносятся из `## Techniques` в раздел под меткой `<!-- kind: process -->` (в файле он ниже); в `Techniques` остаётся одна
   строка опыта: «Name the sides a walk speaks about» без поля и «First look: survey once, one short path per requirement, write what you saw,
   never what you expect». Ожидание: слова процедуры (`first_look.py`, `about:`) не встречаются в разделах `craft`.
2. `ai-packages/qa-factory/agents/qa-case-critic.md`: фиксированные метки (`parametrise into one test: <ids>`, `## Merge candidates`,
   `oracle_field_absent`, `contradicts_source`) переносятся из разделов `craft` (строки 27–76 и 77–91) в ближайший раздел `process` (строка 92
   и далее); рубрика измерений остаётся.
3. `ai-packages/qa-factory/references/role-load.json`: перенос меняет доли — `process_ratchet_tokens` qa-runner и qa-case-critic ВЫРАСТАЕТ на
   измеренную разницу. Это поднятие храповика (AR-20): подъём называется в вердикте критика и в сообщении коммита; альтернатива, если подъёма
   не хотят, — перенести процедуру в справочник, который роль читает в момент шага (`references/…`, не в начальной загрузке): развилка
   Lead, рекомендация — перенос в раздел `process` с названным подъёмом (меньше файлов, тот же вес).
4. Тесты: `python -B ai-packages/qa-factory/scripts/role_load.py --all --json` до/после (craft и process по двум ролям, вердикт `within` у
   всех двенадцати); `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/agents/qa-runner.md`
   (напечатать и прогнать названные тесты); `python -B ai-packages/qa-factory/scripts/tests/test_judgment_census.py` (счёт не должен вырасти).
   Поведение роли доказывается только живым прогоном (FR-33): строка в `live-runs` — ходок идёт первый просмотр и пишет `about:` по новому
   тексту.

Края: роль должна по-прежнему находить `about:` и `first_look.py put` в момент шага — раздел `process` читается ею целиком (проверить: нет
правила «process читается только в стадии X»); текст пакета английский без кириллицы (FR-30; `selftest.py --lang`).

Исполнитель: builder → critic (диффы текстов ролей пакета; свидетель — по `plans/builder-rules.md` п. 7b, «given» — `design/factory-rules.md`).

## Связи

`20261112-slova-cheloveka-iz-otveta-na-vopros-uhodyat-iz-brifa-na-urovne-1.md` (та же кучка, пачка 2); `B-346-…` (пороги A22/A25 ролей: правка
устава упирается в них — проверить запас); `20261021-nositeli-roli-odin-vladelec-bez-protivorechij.md` (`forge`, F6-33: один владелец
аспекта роли).

Принципы и правила: P27, P17; AR-29, AR-20; FR-47, FR-33, FR-30.

Решение владельца нужно: нет (развилка пункта 3 — за Lead пачки).

<!-- id выдаёт интегратор при сборке пачки. -->
