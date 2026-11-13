# `install_smoke --report` на корне без `config.json`: доктор шаг 1 запускает смоук до онбординга, место записи отчёта не выбрано

id: — | кучка: `onboarding-forge` | от: критик t-141 (`docs/tasks/specs/reviews/t-141-of1-hooklib-critic.md`, F5), перепроверка t-152 (`t-152-of1-rereview-and-doctor.md`, A3: «узлы F5/F7 не оценить как узлы — нужны поля») и t-169 (`t-169-of1-hooklib-doctor-rereview.md`, A3 «open, not carried»), 12.11.2026 | приоритет: П2 | кандидат наверх: нет

## Что наблюдалось

Строка OH3-37 владеет `scripts/install_smoke.py` и называет `install_smoke --report`; дифф hooklib (OF1) её не трогал. Писатель — относительный путь доктора `--report "qa-factory/state/doctor-install-smoke-latest.json"` (`skills/qa-doctor/SKILL.md:50`) + `atomic_json`.
`scripts/install_smoke.py`: `main` (:99; разбор флагов около :573-586), `run_report` (:518-560). Шаг 1 доктора запускает смоук ДО онбординга, когда `qa-factory/config.json` ещё нет — корень «голый»: куда писать отчёт, не решено.
Строка 10 оси `docs/SIBLING_MAP.md` (OH3-37 «ожидает», «cost_capture is NOT established», «factory_dashboard by reading, not run») устарела.

## Что именно менять

Направление выбрано критиком t-152 (отказ — неверное: шаг 1 доктора стал бы строкой «чини установку» — FR-5; убрать `--report` — тоже: теряется окно повторного использования и квитанция, переживающая потерянный шелл):
1. `scripts/install_smoke.py` `main`/`run_report`: для корня без `config.json` отчёт пишется в место, существующее до конфига (хост-локальный спул границ активности, которым пользуются до `config.json`; точное место назовёт спека узла по `hooklib`/`runtime_paths`) и печатает путь; доктор шаг 1 берёт путь из вывода скрипта, не из своего текста.
2. Тест: `scripts/tests/test_install_smoke*.py` (назвать в спеке) — голый корень: код выхода 0, дерево корня без изменений, отчёт читается по напечатанному пути, `--reuse-within` повторно использует.
3. Строка 10 оси SIBLING_MAP (OH3-37) — обновить в том же ходе (Lead, правка карты — не билдера); порядок: после потока doctor и OF1-4 (текст шага 1 `SKILL.md` может меняться).

Принципы и правила: FR-5, FR-15, FR-37; AR-4, AR-8.

Решение владельца нужно: нет.
