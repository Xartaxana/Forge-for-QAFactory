# Онбординг, установка, хуки и гард — пачка 8: остатки t-282, t-254 и t-287 (копии проверки компоненты пути вне OH6-1, псевдонимы NTFS, тихий пропуск id сессии, литерал корня плагина в текстах других модулей, аналоги пачки 7)

кучка: `onboarding-hooks` | статус: ожидает | взял: — | ветка: `pile/onboarding-hooks/batch-8` | MR: — | стенд: не нужен (CI) | приоритет: П3

Открыта 13.11.2026 (задача t-298, D-0044): находки спек t-282 (§2.4, F-3, F-8), t-254 (§4: OH5-2d, OH5-2e) и критика диффа пачки 7 t-287 легли в следующую пачку, потому что пачки 6 и 7 взяты.

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего.

Решения владельца: нет (направления выбраны в находках, «по рекомендации, до слова владельца»; развилки Lead пачки названы в узлах OH8-2, OH8-3).
Порядок по общим файлам: `event_store.py` — после слияния OH6-3 (`onboarding-hooks/6`); `selftest.py` — строка `очередь:` к `onboarding-forge/2` или список функций по D-0048; `cost_capture.py`, `hooklib.py` — после OH6-1; `refusal_registry.py` — после OH7-2 (`onboarding-hooks/7`); `story_step.py`, `driver_*` — горячие файлы, строка `очередь:` перед взятием.
очередь: onboarding-hooks/6 → onboarding-hooks/8
очередь: onboarding-hooks/7 → onboarding-hooks/8
Скоуп свидетеля: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <пути узла>`; BATCH CANON — CI интегратора.

## Бриф

Что сделать: шесть узлов из шести находок. НЕ делать: расширять `is_one_component` сверх одной компоненты; менять исход отказов; ставить `CLAUDE_PLUGIN_ROOT` в `run_headless` до измерения (OH8-5).

## Узлы

Исполнитель «designer → builder → critic» — кодовый узел; «builder» — узкая правка; «scout → builder» — места ещё не перечислены. Статусы: `ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| OH8-1 | П3 | Копии проверки «одна компонента пути» вне OH6-1 (`findings/20261113-is-one-component-kopii-vne-oh6-1.md`; t-282 §2.4). Направление: `event_store.py:482`, `selftest.py:982`, `dependency_drift.py:92` зовут `hooklib.is_one_component`, направление ошибки места сохраняется; допуск сторожа OH6-1 сжимается до `{}`. Тест: одна таблица по трём местам × `..`, `.`, `a/b`, `a\b`, `a:b`, NUL, хорошее имя | designer → builder → critic | `scripts/event_store.py` (`EventStore.__init__`), `scripts/selftest.py` (`_slow_tests_problem`), `scripts/dependency_drift.py` (`load_table`), сторож OH6-1 и тесты | OH6-1, OH6-3 | ожидает |
| OH8-2 | П3 | Имена-псевдонимы NTFS (`T.`, `T `, `...`, регистр) проходят проверку одной компоненты (`findings/20261113-ntfs-imena-psevdonimy-prohodyat-proverku-odnoj-komponenty.md`; t-282 F-3). Развилка Lead пачки: читать ли места «ключ стори — папка» через `hooklib.is_story_folder`. Первый шаг — скаут перечисляет места | scout → builder | `scripts/hooklib.py` и места скаута (названы в его отчёте), тесты | OH6-1 | ожидает |
| OH8-3 | П3 | OH6-1 превратил traceback в тихий пропуск для id сессии не-строки и с NUL (`findings/20261113-oh6-1-tihij-propusk-vmesto-traceback-dlya-ne-str-i-nul-id-sessii.md`; t-282 F-8). Развилка Lead пачки: строка в stderr при отказе id сессии, поток хука не меняется. Тест: таблица id × выход без записи и строка | builder | `scripts/cost_capture.py` (`_capture`, `main`), `scripts/tests/test_resolver.py` | OH6-1 | ожидает |
| OH8-4 | П2 | Литерал `${CLAUDE_PLUGIN_ROOT}` в текстах и данных для роли из другого кода (`findings/20261113-oh5-2d-bukvalnyj-claude-plugin-root-v-tekstah-dlya-roli-iz-drugogo-koda.md`; t-254 §4). Направление: носители читают корень через `runtime_paths.script_command`. Тест: соединение «ни один читаемый ролью носитель не держит переменную», строки построенных текстов | designer → builder → critic | `scripts/driver_dispatch.py`, `scripts/driver_stage_s7.py`, `scripts/execution_request.py`, `scripts/stage_done.py`, `scripts/story_step.py`, `scripts/handoff_check.py`, `references/templates/requirements-register.md`, `handoffs/s0-setup-to-scout.yaml`, `references/stand-answers.json`, их `keep`-тесты | OH5-2 (`onboarding-hooks/5`) | ожидает |
| OH8-5 | П3 | Литерал `${CLAUDE_PLUGIN_ROOT}` и `${CLAUDE_SKILL_DIR}` в текстах дирижёра (`findings/20261113-oh5-2e-literal-claude-plugin-root-v-tekstah-dlya-konduktora.md`; t-254 §4). Направление: сначала ОДИН опыт (hygiene 6a) — раскрывает ли хост переменную; затем оставить под правилом `common-rules.md:131-140` или переписать через `runtime_paths.py`; `run_headless` задаёт переменную только по итогам опыта | scout → designer → builder | после опыта: `skills/**`, `references/common-rules.md`, `scripts/source_exclusions.py`, `scripts/config_contract.py`, `experiments/measurers/run_headless.py`, `skills/qa-doctor/evals/evals.json` | OH8-4 | ожидает |
| OH8-6 | П3 | Аналоги пачки 7 (`findings/20261113-batch-7-analogi-json-loads-vne-scanned-i-ustarevshij-scope.md`; t-287 Q1, Q5, Q6). Скаут: другие модули хоста вне `SCANNED` с `json.loads` пакета роли; абзац `SCOPE` докстринга `refusal_registry.py` ссылается на `SCANNED`. Тест: сверка докстринга и `SCANNED`; мутация красит | scout → builder | `scripts/refusal_registry.py` (докстринг), `scripts/tests/test_refusal_registry.py`, места скаута | OH7-2, OH7-3 | ожидает |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 13.11 — пачка открыта: шесть находок положены тем же ходом, что файлы в `findings/` (D-0044, t-298)

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|

## Остатки

<!--
Пачка закрывается доделкой, не переносом (слово владельца 08.10.2026): `close` отказывает, пока в этом разделе есть
пункт, у которого нет одной из двух форм (ключи в нижнем регистре, пары `ключ: значение` через ` | `, текст впереди):
  - <что осталось> | сделано: <хэш 7-40 hex | t-nnn>
  - <что осталось> | перенос: <findings/<файл> | пачка N | <кучка>/findings/<файл>> | обоснование: <почему> | подтвердил: <кто, дата>
Пустой раздел — можно закрывать.
-->
