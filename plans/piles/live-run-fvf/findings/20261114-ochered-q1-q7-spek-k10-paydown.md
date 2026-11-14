# Очередь Q1-Q7 спеки K10 pay-down (r2, §7) не имела узлов: заводятся семь узлов (блокер B1 критика темы K10)

id: — | кучка: `live-run-fvf` | от: спека `docs/tasks/specs/20261114-told-before-work-k10-paydown-spec-r2.md` §7 «Queue lines»; критик темы (`docs/tasks/specs/reviews/20261114-k10-paydown-topic-critic.md`, B1 и «Queue lines» 2: каждая Q грепнута по `plans/piles`, 0 попаданий); слово владельца 14.11.2026: «только B1, остальное завести узлами» | приоритет: П3 | кандидат наверх: нет

## Что не так

Класс фабрики: **строка очереди, существующая только в спеке, — не обязательство (D-0044: находка сразу попадает в пачку)**. Семь строк очереди спеки r2 не имели носителя; критик грепнул `check_findings`, `run_suite:begin`, `exit_gate:digest`, `native_headroom`, `s5_plan_gaps|controller:*`: 0 попаданий (контроль той же формы: `window_first` в live-run-fvf).
Здесь — по узлу на строку (FV2-86…FV2-92); Q6 назван КОДОВЫМ детектором закрытия утечки «строку забыли снять».

## Что именно менять

Пути — от `ai-packages/qa-factory/`; направление каждого узла выбрано строкой спеки.

1. **Q1 (FV2-86), `execution_request:stand`, `run_suite:begin`.** Дизайн фикстуры для строки-провокации (отчёт S-1b, 41-42: живая проба или весь запуск); измерено 663 Б на automator и на code-critic. Узел — дизайн (designer → builder → critic): решение по фикстуре и затем строка `K10p/...`;
   файлы дизайнер называет в спеке (кандидаты: `scripts/tests/test_execution_request.py`, `scripts/tests/test_run_suite_mine.py`). Тест: строка провоцирует отказ через ЗАПУЩЕННЫЙ вызов и держит `unproved_site` до зелёной строки.
2. **Q2 (FV2-87), дубли, найденные вердиктом.** (а) `exit_gate:digest` повторяет EG-digest-form (196 Б, у всех 12 ролей); (б) три строки `handoff_check:field.*` с одним предложением (~380 Б, правка рендера); (в) предложение карточки стратега про «не пишет» (355 Б, F-5).
   Файлы: `references/stage-joints.json`, `scripts/exit_gate.py` (источник EG-digest-form), `scripts/handoff_check.py` (рендер `field.*`), слайсы — только `contract_slices.py --write`. Тест: U (измеренный) каждой роли до и после — падает на названные байты; `process_ratchet_tokens` и `native_headroom` опускаются до меры.
3. **Q3 (FV2-88), разведка скаутом.** Каждая строка `controller:*` в `references/stage-joints.json` против роли и диспатча, для которых срабатывает её проверка (класс S2: `controller:s5_plan_gaps.rework_rows` была приписана не той роли). Узел-разведка (scout → Lead): результат — таблица «строка → роль/диспатч → верно/не верно»; неверные строки — отдельными узлами.
4. **Q4 (FV2-89), `judgment-census.json`.** Роли `check_findings` → `qa-code-critic`, `conductor`, с заметкой, с пересчитанными плотными потолками `blocking_per_role` (нужен `test_judgment_census.py`, медленный — «судит канон пачки»). Файлы: `scripts/tests/fixtures/judgment-census.json`, `scripts/tests/test_judgment_census.py`. Тест: потолки пересчитываются
   только вниз или называются поднятыми (AR-20).
5. **Q5 (FV2-90), проход дизайнера по прозе L12 (F-7 r1) для automator и strategist.** Позволит следующей карточке опустить их строки KR. Узел: designer → builder → critic; файлы — страницы ролей и `references/role-load.json` (`native_headroom` строки автоматора и стратега опускаются до нового U).
6. **Q6 (FV2-91), КОДОВЫЙ детектор «строка `native_headroom` выше измеренного U — красная».** `role_load.native_headroom_problems` (`scripts/role_load.py`, 302-346) краснеет и когда `row > U` (как `process_ratchet_problems` для точной меры), и когда роль ушла под H, а строка стоит. Меняет закреплённое поведение `T3a (j)`
   (`scripts/tests/test_contract_slices.py`, ключи `native_headroom`) — узел Lead. Тест: `scripts/tests/test_role_load.py`, строки «row == U — зелёная», «row > U — красная, называет разницу», «U ≤ H и строка стоит — красная»; расхождение с `T3a (j)` называется в отчёте. Закрывает утечку, которую B1 нашёл (критик: «A row that stays above U ... is silently green»).
7. **Q7 (FV2-92), Appendix A механизм-спеки: файлы проекта по пути для Codex.** Реальное лекарство цены KR (H считает настоящую долю). Спека T1r: `docs/tasks/specs/20261114-told-before-work-t1r-pages-spec.md` (§(h)) и `…-k10-paydown-spec-r2.md` («Appendix A - K3»): открытое решение владельца да/нет — не построено.
   Узел — ожидание слова владельца; кода нет до ответа.

Принципы и правила: AR-20, AR-10, AR-12, AR-11; FR-41.

Связи: `findings/20261114-k10-k1b-uzel-i-uslovie-vyhoda-vremennoj-stroki-code-critic.md` (K1b, FV2-79).

Решение владельцу нужно: Q7 (Appendix A, да/нет; рекомендация — решает владелец, кода до ответа нет); остальное — нет.
