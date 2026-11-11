# Forge — пачка 7: копии и единственные читатели в пакете (хвосты релиза 0.10.9)

кучка: `forge` | статус: ожидает | взял: — | ветка: — | MR: — | стенд: не нужен | приоритет: П2 | issue: https://git.example.com/dev1/yml-text-factory/-/work_items/67

Открыта 02.11.2026 (Lead пачки release-next/1) под очередь критиков релиза 0.10.9: пачка 6 закрыта, новые находки кучки легли в следующую (D-0044).

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего.

Решения владельца: нет (направление выбрано Lead, 02.11.2026).
Скоуп свидетеля: тестовый файл изменённого модуля и ключи DoD узла; BATCH CANON — интегратор.
Общий бриф дизайнерам: карточка кучки («Дороги», «Содержание»); находка узла; `design/factory-rules.md` FR-17, FR-54; `design/architecture.md` AR-13, AR-15; вернуть спеку в `docs/tasks/specs/t-nnn-fg7-n.md`.

## Бриф

Что сделать: свести девять копий свёртки строки к одной, двух прямых читателей `test_data` к единственному читателю, копии цикла штампов и тестовой строки к одной. НЕ делать: другие узлы форджа; правки `docs/SIBLING_MAP.md` (Lead).

## Узлы

Исполнитель «designer → builder → critic» — кодовый узел; «builder» — узел-документ. Статусы:
`ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| FG7-1 | П2 | Одна `contract.one_line(text, limit=None)` вместо девяти копий свёртки строки (`findings/20261102-one-line-devyat-kopij-svertki-stroki.md`; критик t-764 Q5; FR-17, FR-54; AR-13, AR-15) | builder → critic | `scripts/contract.py`, девять модулей по находке, их тесты, `changelog.d/` | — | ожидает |
| FG7-2 | П3 | Блок `test_data` читается только через `config_contract.test_data_states`: `env_probe.data_cleanup` и `audit_factory.py:766` (`findings/20261102-chitateli-test-data-mimo-odnogo.md`; критик t-724 m-2; FR-17; AR-13) | builder → critic | `scripts/env_probe.py`, `scripts/audit_factory.py`, `scripts/brief_pack.py` (строка стратегии), их тесты | — | ожидает |
| FG7-3 | П3 | Один цикл штампа в `waiver.py` и одна тестовая строка `handed_row` (`findings/20261102-kopii-v-waiver-i-testovyh-strokah-rn1-9-ep1-4.md`; критик t-764 m-6; FR-54; AR-13) | builder → critic | `scripts/waiver.py`, `scripts/tests/story_step_common.py`, три тестовых файла | FG7-1 не связан; `waiver.py` — после RN1-9 (`release-next/1`) | ожидает |
| FG7-4 | П1 | Полная фоновая уборка слитых worktree после слияния в `main` и в `close`, итог в журнале и строке SessionStart (`findings/20261103-worktree-sweep-polnaya-uborka-posle-sliyaniya.md`; спека `docs/tasks/specs/t-1738-worktree-sweep-full-after-merge.md`; слово владельца 03.11) | designer → builder → critic | `tools/worktree_sweep.py`, `tools/session_context.py`, `tools/piles.py`, `tools/conftest.py`, их тесты; `.githooks/post-merge` (Lead) | — | принято |
| FG7-5 | П2 | Цена принятого узла с учётом брака: `tools/forge_metrics.py` сводит по `task_id` все попытки, фикс-раунды, критика и повторные диспатчи; топ-5 дорогих узлов с причиной в калибровке (`findings/20261104-tsena-uzla-s-brakom-v-forge-metrics.md`; слово владельца 04.11.2026; P18, FR-51; AR-12) | designer → builder → critic | `tools/forge_metrics.py`, `tools/test_forge_metrics.py` | — | ожидает |
| FG7-6 | П3 | Недельный обзор расхода скаутом перед калибровкой: форма отчёта в `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`, вход калибровочной проверки (`findings/20261104-nedelnyj-obzor-raskhoda-skautom-pered-kalibrovkoj.md`; слово владельца 04.11.2026; cost gates, адаптация хоста 6) | builder → critic | `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` (раздел формы отчёта) | FG7-5 (цена узла — вход отчёта) | ожидает |
| FG7-7 | П3 | Ходы координатора на узел (повторные `delegated`, резюме воркеров) считает `forge_metrics` и печатает рядом с ценой узла (`findings/20261104-khody-koordinatora-na-uzel-v-tsene.md`; слово владельца 04.11.2026; P18, правило 12 `CLAUDE.md`) | builder → critic | `tools/forge_metrics.py`, `tools/test_forge_metrics.py` | FG7-5 (общий файл и функция цены узла) | ожидает |
| FG7-8 | П1 | TR2-9 доделать и слить: блокеры критика t-2564 (повтор id прячет неотвеченный вопрос; тест не в списке слоёв), один помощник «отвеченные id», слова B-13 с исполнителем (`findings/20261111-ostatki-sliyaniya-eksperimenta-v-main.md`; слияние 11.11.2026) | builder → critic | `scripts/gate_preflight.py`, `scripts/question_register.py`, `scripts/gate_brief.py`, `scripts/story_run.py`, `references/question-vocabulary.json`, `scripts/tests/test-layers.json`, тесты, `changelog.d/` | ветка `held/tr2-9` | ожидает |
| FG7-9 | П1 | Первый канон после слияния эксперимента: прочитать прогоны CI на коммите слияния, красное починить (пять известных мест риска в находке) (`findings/20261111-ostatki-sliyaniya-eksperimenta-v-main.md`; слияние 11.11.2026) | builder → critic | по красному: `references/role-load.json`, `scripts/tests/`, `tools/test_test_quarantine.py`, `tools/story-scrub-rules.json` | — | ожидает |
| FG7-10 | П2 | Карантин тестов читает CI через бэкенд GitHub (`pull`, `enter`, расписания, артефакты); проверка `check` за один проход; когорта 432 файла ждёт двух релизов (`findings/20261111-ostatki-sliyaniya-eksperimenta-v-main.md`; слияние 11.11.2026) | designer → builder → critic | `tools/test_quarantine.py`, `tools/test_test_quarantine.py`, `tools/ci_read_common.py`, `plans/test-quarantine/config.json` | FG7-9 | ожидает |
| FG7-11 | П3 | Остатки TR4-17: понятный отказ при пустом номере задания; тест проб привязан к фиче в `plans/features.json` (`findings/20261111-ostatki-sliyaniya-eksperimenta-v-main.md`; слияние 11.11.2026) | builder | `scripts/probe_by_code.py`, его тест, `plans/features.json` | — | ожидает |
| FG7-12 | П3 | Три старые неслитые ветки из бандла истории (`t-861-f6-15-fold`, `t-1256-cx2-23`, `wt/sc14-d`): поднять узлом или списать — по слову владельца (`findings/20261111-ostatki-sliyaniya-eksperimenta-v-main.md`; слияние 11.11.2026) | Lead | нет | слово владельца | ожидает |
| FG7-13 | П2 | CI на GitHub после диеты тестов: расписания на ветке по умолчанию, замер минут первой недели, абзац RUNBOOK про наблюдателя карантина под workflow (`findings/20261111-ostatki-sliyaniya-eksperimenta-v-main.md`; слияние 11.11.2026) | builder | `docs/RUNBOOK.md`, `plans/MEASUREMENTS.md` | FG7-9 | ожидает |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 02.11 — открыта пачка 7 под FG7-1…FG7-3 (очередь критиков релиза 0.10.9; t-770)
- 03.11 — FG7-4 по слову владельца: спека t-1739 (развилки F1–F9 по рекомендации), билдер t-1744 сдал c3135771 на ветке `worktree-agent-acb67480a48b56ff2` (CI 8026398), критик t-1752; хук, проверка 37 и RUNBOOK §9.3 — правка Lead (Fable) тем же механизм-коммитом
- 03.11 19:0x — критик t-1756: принять с фикс-раундом (F1 блокирующий: потерявший лок прогон продолжал удалять); фикс-раунд t-1764 3497c96e (F1 F2 F4 F5 F8); в очередь F3 (двойной счёт prunable по проходам → находка 20261026-worktree-sweep-ostatok п. 6), F6 (третья копия `_ascii_sanitize` в session_context), F7 (`sweep()` 105 строк — разделить), F9 (`release`/`set_pid` одна попытка; отказ `_background_run` уходит в DEVNULL). FG7-4 принято Lead (Fable); слито в `main` после зелёного CI

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
