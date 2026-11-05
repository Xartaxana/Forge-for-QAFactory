# Выход S0 → S1: `story_step start --stage S1` отказывает «initialize task before work», а карта S0 не называет команду initialize

id: — | кучка: `driver-hosts` | от: прогон TP1-14857 на 0.10.5, `testproject1-dev-010`, 29.10.2026; разбор t-1583 | приоритет: П2 (решение Lead) | кандидат наверх: нет

## Что наблюдалось

S0 → S1, 18:49:52 (UTC). `story_step start --stage S1` → `story_step: refused - initialize task before work`. Карта S0 (`phases/s0.md`, раздел 10)
и `prepare` задачу не инициализируют. Дирижёр собрал `init.json` руками, первый запуск дал `{"error": "stale expected revision"}`,
поправил ревизию 0→1 и повторил (18:50:35–18:51:47).

Цена: ~2 мин, 4 лишних вызова, рукописный JSON-запрос на штатном пути (`s0.md` рукописные запросы запрещает).

Места: `scripts/controller.py` (ветка `initialize`, проверка формы ~4530), `skills/qa-story/phases/s0.md` раздел 10.

## Класс

Отказ называет, что не так («initialize task»), но не дверь, которой получатель может воспользоваться: готовой команды `initialize` в карте
нет (FR-1, FR-2, AR-9). Следующая карточка не называет единственную дверь, закрывающую переход S0 → S1 (AR-17: у кода нет хода — зовёт
дирижёра одним швом, а шов не говорит команду). Соседи: другие переходы стадий, где `start` отказывает по предусловию, а карточка
предыдущей стадии условия не называет.

## Что нужно

1. Карточка выхода S0 (`phases/s0.md`) называет команду initialize готовой строкой (без рукописного JSON); отказ `initialize task before work`
   печатает её же.
2. Тест: `start --stage S1` без initialize → отказ содержит команду initialize; перечислением по стадиям проверить, что остальные отказы
   `start` по предусловию тоже называют дверь.

Решение владельца нужно: нет (П2 — решение Lead).
Связи: `gates-and-words/findings/B-336-transport-ostatki-volny-3-na-puti.md` (транспорт initialize), `codex/findings/20261015-controller-task-abbrev-phantom-root.md`
(не то же: там нет команды initialize не обсуждается); FR-1, FR-2; AR-9, AR-17.
