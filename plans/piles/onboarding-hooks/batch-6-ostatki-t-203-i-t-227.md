# Онбординг, установка, хуки и гард — пачка 6: остатки t-203 и критика t-227 (копии проверки компоненты пути, потолок компоненты, суффикс `_publish`, отказы нативного контекста)

кучка: `onboarding-hooks` | статус: в работе | взял: Lead dev1 (Opus), 13.11.2026 | ветка: `pile/onboarding-hooks/batch-6` | MR: — | стенд: не нужен (CI) | приоритет: П3

Открыта 13.11.2026 (задача t-233, D-0044): находки спеки t-203 (§4 «Copies», §5, §6 F-2, F-5, F-6) и критика t-227 (B-2, B-3, Q3, Q5) легли в следующую пачку, потому что пачки 1-5 взяты или закрыты.

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего.

Решения владельца: нет (направления выбрал координатор, 13.11.2026, «по рекомендации, до слова владельца»; один вопрос Lead — NUL в `is_one_component`, OH6-1 п. 3).
очередь: onboarding-hooks/5 → onboarding-hooks/6
очередь: onboarding-forge/1 → onboarding-hooks/6
очередь: onboarding-forge/2 → onboarding-hooks/6
очередь: onboarding-forge/4 → onboarding-hooks/6
очередь: onboarding-hooks/6 → onboarding-hooks/7
Порядок по общим файлам: `hooklib.py`, `stage_guard.py`, `cost_capture.py`, `native_context.py`, `inject_context.py`: после OH5-10, OH5-11, OH5-13 (`onboarding-hooks/5`) и слияния веток `wip/oh5-11`, `wip/oh3-36` (`onboarding-forge/1`); `stage_guard.py` — со списком функций в `owns` диспатча (OH6-1: `story_named_by_text`, `resolve_ticket`, `_recipient_receipts`).
Скоуп свидетеля: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <пути узла>`; BATCH CANON — CI интегратора.
Общий бриф дизайнерам: находка узла (раздел «Что именно менять»); `design/factory-rules.md`; `docs/tasks/specs/t-203-native-context-long-root.md`; вернуть спеку в `docs/tasks/specs/t-nnn-oh6-n.md`, развилки — наверх.

## Бриф

Что сделать: шесть узлов из пяти находок. НЕ делать: расширять `is_one_component` сверх одной компоненты; менять исход отказов нативного контекста (F-6); убирать `native_context.pending_path` (F-5 закрыта «оставить»); вносить новую ось в `docs/SIBLING_MAP.md` (очередь полного Lead — «бюджет длины пути»).

## Узлы

Исполнитель «designer → builder → critic» — кодовый узел; «builder» — узел-документ или узкая правка; «scout → builder» — места ещё не перечислены. Статусы:
`ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| OH6-1 | П3 | Копии проверки «имя — одна компонента пути» (`findings/20261113-kopii-proverki-odnoj-komponenty-puti.md`; t-203 §4, t-227 B-2/B-3). Выживший — `hooklib.is_one_component` (`hooklib.py:233`). Направление: каждая копия зовёт его, направление ошибки места сохраняется — `host_dispatch.controller_record` (:21, `None`), `exit_gate._named_ticket` (:209, пропуск имени), `stage_guard.story_named_by_text` (:436, пропуск), `stage_guard.resolve_ticket` (:643, следующий маршрут), `stage_guard._recipient_receipts` (:717, пропуск), `activity_capture.activity_path` (:44, `ValueError`), `cost_capture._capture` (:1907, `sys.exit(0)`) и `cost_capture.main` (:3800, `return`), `recover_codex_usage.recover` (:16, `ValueError`; одинарные кавычки `'/\\:'`, охраны `.`/`..` нет — получает её). `hooklib.is_story_folder` (:266) зовёт `is_one_component` и держит своё (NUL, пробелы, листинг). Развилка Lead с рекомендацией (исполнимо по ней): `is_one_component` отказывает NUL. Тест: ОДНА параметризованная таблица в `test_resolver.py` по каждому вызывающему × `..`, `.`, `a/b`, `a\b`, `a:b`, NUL, хорошее имя; сторож-перепись ловит обе формы кавычек и любое имя переменной цикла (`for \w+ in ['"]/\\\\:`) | designer → builder → critic | `scripts/hooklib.py` (`is_one_component`, `is_story_folder`), `scripts/host_dispatch.py`, `scripts/exit_gate.py`, `scripts/stage_guard.py` (`story_named_by_text`, `resolve_ticket`, `_recipient_receipts`), `scripts/activity_capture.py`, `scripts/cost_capture.py`, `scripts/recover_codex_usage.py`, `scripts/tests/test_resolver.py` | OH5-11 (`worker_lifecycle.py:94`, `hooklib.artifacts_dir`); идущие потоки по `hooklib`/`cost_capture` | ожидает |
| OH6-2 | П3 | Компоненты записываемого пути без потолка длины (`findings/20261113-komponenty-puti-bez-potolka-dliny.md`; скаут t-216). Направление: одна константа предела компоненты рядом с `PACKET_ROOT_LIMIT` (`native_context.py:10-13`), проверка там, где компонента формируется; отказ называет компоненту, её длину и предел. Первый шаг — скаут перечисляет места (ключ, основа имени, id сессии в записываемом пути). Тест: таблица по местам скаута, компонента на пределе, на 1 больше, пустая | scout → builder | `scripts/native_context.py`, места скаута (названы в его отчёте), тесты | OH6-3 (пересчёт константы после укорочения суффикса); OH5-13 | ожидает |
| OH6-3 | П3 | F-2 спеки t-203 (`findings/20261113-oh5-11-ostatki-f2-publish-temp-f6-native-valueerror.md`): `event_store._publish` пишет временное имя `.<8 hex>.tmp` (было 32), открывая его режимом `"x"`; `TEMP_NAME_EXTRA`, формула и `SUPPORTED_ROOT`/`PACKET_ROOT_LIMIT` (119 → 143), правило N8a `driver-golden-rules.json` и его строка в `test_driver_golden.py` — тем же коммитом. Файл ядра: критик обязателен. Тест: имя временного файла — 8 hex; совпавшее имя у двух писателей — второй берёт новое; путь пакета на корне 143 ≤ 259 | designer → builder → critic | `scripts/event_store.py` (`_publish`), `scripts/native_context.py`, `scripts/tests/fixtures/driver-golden-rules.json`, `scripts/tests/test_driver_golden.py`, `scripts/tests/test_event_store.py` | слияние `wip/oh3-36` (константы `TEMP_NAME_EXTRA`, `SUPPORTED_ROOT`) | ожидает |
| OH6-4 | П3 | F-6 спеки t-203 (тот же файл находки): три существующих отказа нативного контекста (размер, идентичности, `StateConflict`) получают строку `note_denial` в `inject_context.py` через `block(...)` и строку A24 в `refusal_registry.py`; исход отказов НЕ меняется. F-5 (`pending_path`) закрыта решением «оставить» — узла нет. Тест: по строке A24 на каждый отказ; `recover` не закрывает ожидающий запуск | designer → builder → critic | `scripts/inject_context.py`, `scripts/refusal_registry.py`, `scripts/tests/test_doctor_context.py` | слияние `wip/oh3-36` | ожидает |
| OH6-5 | П3 | Хвост текста `DELIVER_WRITE_FAILED` (`findings/20261113-t-227-q5-ochered-tekst-deliver-write-failed-i-razrez-deliver.md`, п. 1; t-227 Q5): совет про длину пути — только при `what == BINDING_UNWRITTEN` (F-7); для `PACKET_UNMARKED` (F-9, перезапись) — свой хвост «writable / not locked». Тест: A8 — «a shorter folder» есть, A8b — нет и есть «writable» | builder → critic | `scripts/inject_context.py`, `scripts/tests/test_doctor_context.py` | слияние `wip/oh3-36` | ожидает |
| OH6-6 | П3 | Разрез `inject_context.deliver` (~58 строк) на помощников до ~25 строк — ТОЛЬКО когда в `deliver` правит OH5-10 и в том же узле (t-227 Q5; находка выше, п. 2). Поведение не меняется: A1-A9 зелёные | builder → critic | `scripts/inject_context.py` (`deliver`), `scripts/tests/test_doctor_context.py` | OH5-10 (`onboarding-hooks/5`) | ожидает |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 13.11 — пачка открыта: пять находок t-203/t-227 положены тем же ходом, что файлы в `findings/` (D-0044, t-233)
- 13.11 — OH6-1 owns widened by spec t-282 fix round t-291: estimate_record.py, red_sandbox.py, role_digest.py, test-layers.json (covers only); builder t-294 (Lead dev1, 2026-11-13)

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
