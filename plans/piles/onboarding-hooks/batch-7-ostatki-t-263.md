# Онбординг, установка, хуки и гард — пачка 7: остатки спеки t-263 (второй писатель публикации, A24 для двух отказов, хвосты native_context, текст гарда тестовых путей)

кучка: `onboarding-hooks` | статус: в работе | взята: — | ветка: `pile/onboarding-hooks/batch-7` | MR: — | стенд: не нужен (CI) | приоритет: П3 | взял: Lead dev1 (Opus), 13.11.2026

Открыта 13.11.2026 (задача t-267, D-0044): находки спеки t-263 (F-C, F-6, N-1, N-2) и тексты отказа гарда тестовых путей легли в следующую пачку, потому что пачка 6 взята.

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего.

Решения владельца: нет (направления выбраны в находках, «по рекомендации, до слова владельца»).
Порядок по общим файлам: `native_context.py`, `inject_context.py`, `refusal_registry.py`: после слияния OH6-3/OH6-4/OH6-5 (`onboarding-hooks/6`).
очередь: onboarding-forge/1 → onboarding-hooks/7
очередь: onboarding-hooks/6 → onboarding-hooks/7
очередь: onboarding-forge/2 → onboarding-hooks/7
очередь: onboarding-hooks/5 → onboarding-hooks/7
очередь: onboarding-forge/4 → onboarding-hooks/7
очередь: onboarding-hooks/7 → onboarding-hooks/8
Скоуп свидетеля: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <пути узла>`; BATCH CANON — CI интегратора.

## Бриф

Что сделать: пять узлов из пяти находок. НЕ делать: менять текст, тип и порядок бросков `native_context.stage` и ключ A24 `NC-launch-pending` (начало текста отказа pending остаётся); трогать `is_one_component` и узлы пачки 6.

## Узлы

Исполнитель «designer → builder → critic» — кодовый узел; «builder» — узкая правка. Статусы: `ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| OH7-1 | П3 | Два писателя публикуют своим 32-hex именем (`findings/20261113-dva-publikatora-dashboard-i-migrate-coverage-mimo-atomic-text.md`; t-263 F-C). Направление: оба зовут `event_store.atomic_text`. Тест: тот же файл, `.tmp` рядом нет | builder | `scripts/factory_dashboard.py` (около :4170), `scripts/migrate_coverage.py` (около :25), их тесты | OH6-3 |принято: a890965 (t-311) |
| OH7-2 | П3 | Отказы `check_override`/`rewritten_input` без строки A24 (`findings/20261113-otkazy-check-override-i-rewritten-input-bez-stroki-a24.md`; t-263 F-6, форма D). Направление: `codex_roles.py`, `host_adapter.py` в `SCANNED`, строки по буквальным текстам `raise`. Тест: строка есть; мутация красит | builder → critic | `scripts/refusal_registry.py`, `scripts/tests/test_doctor_context.py` | OH6-4 |принято: 94f9ba9 (t-280) |
| OH7-3 | П3 | `native_context.stage` падает `AttributeError` на pending-файле не-словаре (`findings/20261113-native-context-stage-json-spisok-v-pending-padaet-bez-paketa.md`; N-1). Направление: не-словарь — нечитаемый пакет, существующая дорога отказа. Тест: таблица содержимого | builder | `scripts/native_context.py` (`stage`, строки :69, :179), `scripts/tests/test_doctor_context.py` | OH6-4 |принято: 34c0471 (t-278) |
| OH7-4 | П3 | Отказ pending без двери для запуска, который не стартовал (`findings/20261113-otkaz-pending-ne-nazyvaet-dver-dlya-zapuska-kotoryj-ne-startoval.md`; N-2). Направление: добавить «relaunch the role under a unique task name» как в :202. Тест: подстрока и сохранённый префикс | builder | `scripts/native_context.py` (:165), `scripts/tests/test_doctor_context.py` | OH6-4 | ожидает |
| OH7-5 | П3 | `TEST_PATH_HOW` и `HOW` отстали от `s5.md:234` (`findings/20261113-teksty-otkaza-test-path-how-otstali-ot-pravila-s5.md`). Направление: выровнять первую фразу под s5.md. Тест: сверка подстроки из s5.md | builder | `scripts/guard_app_under_test.py` (:25), `scripts/tests/test_protected_test_path.py` (:602) | — |принято: 95afef8 (t-279) |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 13.11 — пачка открыта: пять находок положены тем же ходом, что файлы в `findings/` (D-0044, t-267)

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
