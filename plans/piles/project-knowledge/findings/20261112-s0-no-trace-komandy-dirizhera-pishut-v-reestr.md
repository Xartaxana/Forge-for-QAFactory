# В S0 прогона `--no-trace` команды дирижёра `side` / `account` / `revoke` всё равно пишут строку в реестр проекта

id: — | кучка: `project-knowledge` | от: критик на план t-043 (N2, «sibling outside the node»; в постановке — t-050), Lead, 12.11.2026 | приоритет: П2 | кандидат наверх: нет

## Что не так

Класс фабрики: «признак эксперимента без следа читается там, где он уже есть» (P8, FR-53; неизвестное — не проход, FR-59, AR-28).
Проверка `_refuse_no_trace(task_root)` реестра знаний (`ai-packages/qa-factory/scripts/project_knowledge.py:309-321`) решает по
`external_writes.closed_by_run(task_root)` (`external_writes.py:189-202`), а тот читает ТОЛЬКО `pipeline.json` истории: `load_json`
(`external_writes.py:153-158`) при отсутствии файла возвращает `(None, ошибка)`, ветка `isinstance(pipeline, dict) and pipeline.get("no_trace")`
не срабатывает, и функция возвращает `""` — то есть «не эксперимент, писать можно». `pipeline.json` драйвер пишет только в конце S0
(`story_run.py:9698-9701`: «pipeline.json is written only at the end of S0»; запись признака — :9911-9912). Поэтому в S0 истории
`--no-trace` команды дирижёра `side` (`cmd_side`, :648-683), `account` (`cmd_account`, :573) и `revoke` (`cmd_revoke`, :635) — все через
`_write_prologue` (:558-570, вызов :567) и `record` (:402, вызов :414) — ЗАПИСЫВАЮТ строку в реестр проекта: эксперимент оставляет след.
Дорога драйвера эту дыру уже закрыла: `_keep_sides_answer` отказывается писать по `launch.no_trace` (`story_run.py:8603-8606`), а метод
драйвера `no_trace()` читает launch-запись, пока `pipeline.json` нет (`story_run.py:16872-16887`). Признак с первого шага S0 хранится в
`state/driver-state.json`, ключ `launch.no_trace` (его пишет `story_run.py:9702-9706` до первой остановки S0; файл —
`story_run.py:1207, 1261`).

Проверено чтением носителей: `closed_by_run` ничего, кроме `pipeline.json`, не читает; `cmd_side` и `cmd_account` проходят
`_write_prologue` (:567) и передают `task_root` в `record` (`:599, :608, :676`), `cmd_revoke` — через `_write_prologue` (:636) и
`revoke` (:640), так что проверка вызывается и молча пропускает. Соседи по читателю признака, чинятся тем же изменением без правок
своего кода: `cmd_role` (`record` напрямую, `task_root` передан, :626-628) и `notice_from_handoff` (:482, замеченные роли).

## Что именно менять

Направление выбрано (Lead, 12.11.2026).

1. **`project_knowledge.py`, `_refuse_no_trace`.** Признак эксперимента читается так же, как его читает `Driver.no_trace`
   (`story_run.py:16872-16887`): (1) ключ `no_trace` в `pipeline.json` истории, если файл есть и ключ в нём есть (в том числе `false` —
   путь человека наружу, `stage_done --set no_trace=false`, FR-40), решает сам; (2) иначе `launch.no_trace` в
   `<task_root>/state/driver-state.json` закрывает запись; (3) если НЕ прочитан ни один носитель (нет `pipeline.json` и нет читаемого
   `driver-state.json`) — безопасное по умолчанию: НЕ писать и сказать почему (FR-59): отказ называет, что не установлено («whether this
   story is an experiment that leaves no trace could not be established: neither `pipeline.json` nor `state/driver-state.json` of the story
   can be read»), и дверь (запустить S0 истории или проверить файлы истории и повторить команду; ничего не записано). Неизвестная история
   (`task_root` равен `None`) остаётся «не эксперимент» (`_refuse_no_trace(None) == ""`, тест :357). Инвариант места: порядок «сначала
   `closed_by_run`, затем launch-запись» не должен открыть то, что `pipeline.json` закрыл, и не должен закрыть то, что человек открыл
   явным `no_trace: false`. Дубль правила в `Driver.no_trace` назван спеке узла: дизайнер решает, один ли читатель на оба места (AR-13,
   AR-15), или ссылка из одного места на другое; кодом дубль не сводится в этой находке.
2. **Тест.** Строки в существующих проверках `--no-trace` в `ai-packages/qa-factory/scripts/tests/test_project_knowledge.py`
   (`test_no_trace_refused` :352-368, `test_side_refused_on_a_no_trace_story_with_the_door` :759-762: фикстура `Proj` с
   `pipeline={...}` — для строк без `pipeline.json` фикстуре нужен вариант, который его не пишет, а кладёт `state/driver-state.json`).
   Параметризованная таблица случаев, id параметра — случай: нет `pipeline.json`, `launch.no_trace: true` -> отказ и файл реестра не
   создан (для `side`, `account`, `revoke`); нет `pipeline.json`, `launch.no_trace` нет/`false` -> запись проходит; `pipeline.json` с
   `no_trace: false` и `launch.no_trace: true` -> запись проходит (явное «false» выигрывает); `pipeline.json` без ключа и
   `launch.no_trace: true` -> отказ; нет ни `pipeline.json`, ни `driver-state.json` -> отказ «не установлено» с дверью, ничего не
   записано; `driver-state.json` повреждён (не JSON) при отсутствии `pipeline.json` -> отказ «не установлено». Сопутствующая проверка
   в `scripts/tests/test_story_sides.py` не нужна: дорога драйвера уже покрыта (:313-318, :619-635).

## Свидетель

`project_knowledge.py:309-321, 402-414, 558-570, 573, 635, 648-683`; `external_writes.py:153-158, 189-202`;
`story_run.py:8603-8606, 9698-9712, 9911-9912, 16872-16887`; `docs/tasks/specs/reviews/t-043-critic-on-plan.md:155-160` (N2).
Расхождение с постановкой: «критик t-050» — на носителе это N2 разбора `t-043-critic-on-plan.md`; «`side` :648-683» подтверждено;
`_refuse_no_trace` вызывается из `record` на :414 — подтверждено, и ещё из `notice_from_handoff` (:482) и `_write_prologue` (:567).

Принципы и правила: P8, FR-53, FR-59, FR-1, AR-13, AR-15, AR-28.

## Связи

PK2-11 этой же пачки (`findings/20261111-zapis-v-sleduemyj-sled-bez-proverki-no-trace.md`) — писатели, которые `no_trace` не проверяют
вовсе; здесь — писатели, которые проверяют, но читают признак поздно. Один класс «след эксперимента в проекте»; исполнять вместе
(одна общая функция отказа). PC2-7 (`package-ci/2`) от этой дыры не зависит (разбор t-043).

Решение владельца нужно: нет.

<!-- id выдаёт интегратор при сборке пачки (следующий свободный B-nnn на main); находка, перенесённая из
BACKLOG.md при заморозке, несёт свой старый id. Имя файла: yyyymmdd-<slug>.md. -->
