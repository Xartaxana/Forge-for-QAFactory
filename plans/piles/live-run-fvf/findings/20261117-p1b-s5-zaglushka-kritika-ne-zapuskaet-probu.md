# Заглушка критика кода S5 в сухой истории не запускает `probe_by_code.py`: главный проход встаёт на S5 (метка `main/S5`)

id: — | кучка: `live-run-fvf` | от: отчёт узла s5stub (`docs/tasks/specs/reports/20261114-p1b-s5stub-report.md`, `:43-47`; ветка `wip/p1b-n4m`); снимок `docs/tasks/compact-snapshots/2026-11-14-0800-narrative.md` (метка `main/S5 -> P1B-9` устарела) | приоритет: П1 | кандидат наверх: нет

## Что не так

Класс фабрики: **тестовый слой отстаёт от поведения роли и молча останавливает главный проход; причина лежит на стороне заглушки, не продукта (класс `stub gap`, F2 спеки)**.

Факты отчёта s5stub:

- Главный проход `dry-1` закрывает S0-S4 и встаёт на S5 (385,1 с в 4 процессах драйвера; `NOTE dry-1/main/stub-live_only: S5 qa-code-critic: form s5-critic-to-automator: no probe record exists in work/probes/ and the contract declares no empty outcome for probes.records`).
- Прежний отказ (подсказка `<instance>` внутри текста) снят; новый — «край (a)».
- Причина: живой критик кода зовёт `probe_by_code.py --task <T> --dispatch <ID> --test ... --instance <IID>` (текст команды выдаёт `scripts/brief_pack.py:239`; скрипт пишет `work/probes/<IID>.json`, `scripts/probe_by_code.py:19`). Заглушка его не зовёт: `grep probe_by_code` по `scripts/tests/dry_*.py` пуст (контроль: тот же grep находит его в `brief_pack.py`). Записи пробы у хода критика нет, и контракт не объявляет пустого исхода у `probes.records` (отдельная находка FV3-19).
- Остановка CI-1 называет ДВА поля, которые форма критика не может заполнить: поле итогового сообщения/дайджеста формы критика и `probes.runtime_provenance` (`handoff_check.py:551`: «no run block of dispatch S5-qa-code-critic-1 carries a runtime_provenance record»). `probe_by_code.py:13` запускает `run_suite.py --request`, поэтому исправление FV3-5, вероятно, порождает и блок запуска — оценка, не измерение; без второго ряда в п. 4 узел может пройти свою строку selftest, а остановка останется на месте.
- Метка реестра `main/S5 -> P1B-9` устарела: P1B-9 слит в `main`, остановка теперь по другой причине. Метка отдаётся узлу FV3-5 (`raised_by` начинается с `stub gap:`).

Не установлено в этом узле: остановится ли проход на S5 на слитом дереве по той же причине — меряет CI (`dry-1/main/stop`), прогноз «запись пробы» — оценка по отчёту, не измерение.

## Что именно менять

Выбранное направление (Lead, 17.11.2026, F-P7 (а), F-P18): заглушка критика запускает настоящий `probe_by_code.py` на каждый экземпляр окна.

1. `ai-packages/qa-factory/scripts/tests/dry_stub.py` (ход критика кода S5, ветка заглушки `qa-code-critic`) и `scripts/tests/fixtures/stories/dry-1/story.json` (данные экземпляров окна): в начале хода критика заглушка вызывает `probe_by_code.py` с `--task`, `--dispatch`, `--test`, `--instance` по тем же аргументам, что выдаёт `brief_pack.py:239`; запись `work/probes/<IID>.json` пишет настоящий инструмент, заглушка вердикта пробы не придумывает (AR-29, AR-7).
2. Таймаут вызова — значение данных (`PROBE_TIMEOUT_S`); если вызов не укладывается в потолок `TEST_TIMEOUTS["test_scenario_dry_1.py"]` (900 с) вместе с остальным проходом — стоп и вопрос Lead (F-P18 (а), при превышении — (б) словом Lead с числом CI).
3. Метка `main/S5` перебивается узлом (б) (по CI после волны реестров по группам): `main/S5 -> FV3-5` пишет L2 до этого узла, N2h-б переписывает или удаляет по итогам CI; общий `known_red.json` в одной волне пишет один узел.
4. Тест — две строки таблицы `dry_stub.py --selftest` (быстрый, 46 с у t-955 на слитом дереве):

   | строка | что проверяет |
   |---|---|
   | critic branch ran probe_by_code; record exists | запись `work/probes/<IID>.json` существует после хода критика |
   | critic form's `probes.runtime_provenance` is filled after the probe | поле `probes.runtime_provenance` формы критика заполнено после пробы (блок запуска `run_suite.py` есть) |

Принципы и правила: AR-29, AR-7, AR-22 (запись пробы — писатель настоящий инструмент); FR-47, FR-18.

Решение владельца нужно: нет.
