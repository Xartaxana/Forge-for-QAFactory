# FR-59: `s5_stand_limits` — неизмеренный предел стенда спрашивается, ответ человека записывается в реестр окружения (B-282)

id: — | кучка: `rules-debt` | от: спека карточек фазы 2 (`docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md`), 17.11.2026 | приоритет: П1 | кандидат наверх: нет

Что не так / что сделать: `check_s5_stand_limits` (`gate_preflight.py:3191-3194`) сегодня пишет `unmeasured` заметкой, не карточкой: S5 идёт на догадке. Класс: FR-59, FR-7 (граница, на которую человек ответил, не спрашивается заново тем же текстом).

Что именно менять: `environment_record.py`: третий объём `stand_limit` рядом с `LEVEL`/`CASE`, ключ `{scope, environment, definition_sha, contour, wait_s}`, ветка в `lasting`, `current_key`, `near_miss`, форма CLI `record`. `gate_preflight.py` (`_e2e_limit`, `check_s5_stand_limits`, `_stand_limit_card`): `unmeasured` → карточка с вариантами «принимать всегда для этого стенда», `executor unavailable: <profile>`, `<case id>: manual`; `_environment_cover` спрашивается ДО карточки: живая строка под тем же ключом → без карточки, одна заметка «not asked — <слова>, as you recorded on <date>». Писатель и читатель — одним коммитом (AR-22). Края: заглушка вместо имени стенда или нет `page_object_max_wait_s` → ключа нет, карточка без «принимать всегда»; нечитаемая запись — сказано один раз, карточка показана; записанное измерение конфига всегда выигрывает; ввод человека — строки на пределе и за ним. Тесты: строки в `test_environment_record.py` и `test_gate_preflight.py`. Общее для всех карточек C3 (спека, §2 «Shared items»): ветка неизвестного ведёт себя как решено; одна строка в файле `test` строки реестра закрепляет неизвестное (вопрос и ожидание / перезапуск / отказ с дверью, никогда не проход); в реестре `status: converted`, `debt_ref: ""`, решённые `unknown_branch` / `on_no_answer` / `waits_at`, `vocabulary: code` со словами из сайтов; файл долга НЕ правится (его двигает S1b). Правит только свои строки `gate-registry.json` (строчно-раздельно с остальными C3 и S7). Свидетель: `scenario_walk.py --witness-for <owns>`, `gate_registry.py --check`; медленные файлы судит канон. Нужен критик на план до кода.

Карточка: `docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md`, карточка C3-j — читать там, не копировать сюда.

Свидетель: `gate_preflight.py:3088,3165,3242,6084-6093`; `environment_record.py:33,133,300,326`; реестр, строка `s5_stand_limits` (:501).

Принципы и правила: FR-59, FR-7, FR-8; AR-22, AR-24, AR-28, AR-29.

Решение владельца нужно: нет.
