# Запись `evidence/runtime-provenance-*.json` нет в реестре писателей, и ни одно правило гарда не называет семейство (очередь L-3 и L-4 плана P1B-9)

id: — | кучка: `live-run-fvf` | от: план-критик P1B-9 (`docs/tasks/specs/reviews/20261114-p1b-9-plan-critic.md`, K5 «AR-14 / P31», строки очереди L-3, L-4, поправка S4) | приоритет: П2 | кандидат наверх: нет

## Что не так

Класс фабрики: **у семейства файлов нет записи писателя, и гард, читающий реестр, его не знает (AR-14)**. `ai-packages/qa-factory/references/artifact-writers.json` (~184-193) заводит `work/evidence/`
(писатель `run_suite.py`, механика включает `runtime_probe.py`), а проба пишет в `<task>/evidence/runtime-provenance-<профиль>-<метка>.json` (`ai-packages/qa-factory/scripts/runtime_probe.py:1331`) — другой
каталог. У соседей в той же папке свои строки: `evidence/diagnostic-*.json` (~176), `evidence/place-answer-*.json` (~243). Гард читает реестр в `ai-packages/qa-factory/scripts/guard_pre_tool.py` (~778-784, ~981),
значит, файл, написанный ролью, гард не назовёт (L-3). Критик: L-3 и L-4, вероятно, одного корня.

## Что именно менять

Выбранное направление: одна строка данных в реестре — `evidence/runtime-provenance-*.json`, писатель `runtime_probe.py` (как у соседей), затем проверка, закрывает ли она и L-3; если нет — правило гарда отдельной строкой данных.

1. `ai-packages/qa-factory/references/artifact-writers.json`: строка `evidence/runtime-provenance-*.json` с `writer: runtime_probe.py` и «why» по форме соседей (`diagnostic-*`). Прежний `work/evidence/` не трогать (его писатели прежние).
2. Установить измерением (одна команда: `guard_pre_tool.py`, запись роли в `evidence/runtime-provenance-x.json` до и после строки): отказывает ли гард названием писателя. Не отказывает — строка данных правила (в таблицу
   данных, которую читает `guard_pre_tool.py`, не в код), с тем же измерением после.
3. Тесты — строки в `ai-packages/qa-factory/scripts/tests/test_guard_write_owners.py` (дизайнер сверяет по `test-layers.json`, что файл быстрый и судит `artifact-writers.json`): запись роли в семейство отказана с
   названием `runtime_probe.py`; запись `runtime_probe.py` проходит; соседние семейства (`diagnostic-*`) не меняются.
4. Совместить с картой P1B-9: если C1 (S4 плана) уже кладёт строку реестра, узел сводится к измерению п. 2.

Принципы и правила: AR-14, AR-15, AR-1 (данные, не код); FR-54.

Связи: `findings/20261029-gitignore-work-evidence-ne-tot-katalog.md` (кучка `onboarding-hooks`): тот же класс «каталог доказательств не имеет одного объявления» — другое место (`.gitignore`).

Решение владельца нужно: нет.
