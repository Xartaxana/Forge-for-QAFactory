# FR-59: `case_preconditions`, `reporter_rehearsal_identity`, `environment_property_cover` — одна карточка на общие функции

id: — | кучка: `rules-debt` | от: спека карточек фазы 2 (`docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md`), 17.11.2026 | приоритет: П1 | кандидат наверх: нет

Что не так / что сделать: `_rehearse_reporter` зарегистрирована двумя строками реестра, `check_case_preconditions` — двумя; перевод одной строки при другой на долге даёт находку «registered more than once». Класс: общая функция служит двум строкам (AR-15).

Что именно менять: `gate_preflight.py` (`check_case_preconditions`, `_rehearse_reporter`, `_environment_cover`, помощники предусловий — их называет план), `driver_gates.py` (`hand_to_conductor`), `stand_gaps.py` (`gate_b_split`). (1) `Rehearsal._environment_cover` (`gate_preflight.py:4214`) регистрируется под `environment_property_cover` вместо двух общих функций, если держит всё решение покрытия (план подтверждает). (2) строки S-b по трём `decides`. Края: поиск покрытия остаётся ПОСЛЕ пробы и только на ветке карточки (E1, позиционный инвариант); нечитаемая запись — сказано один раз, ничего не покрывает (E2). Общее для всех карточек C3 (спека, §2 «Shared items»): ветка неизвестного ведёт себя как решено; одна строка в файле `test` строки реестра закрепляет неизвестное (вопрос и ожидание / перезапуск / отказ с дверью, никогда не проход); в реестре `status: converted`, `debt_ref: ""`, решённые `unknown_branch` / `on_no_answer` / `waits_at`, `vocabulary: code` со словами из сайтов; файл долга НЕ правится (его двигает S1b). Правит только свои строки `gate-registry.json` (строчно-раздельно с остальными C3 и S7). Свидетель: `scenario_walk.py --witness-for <owns>`, `gate_registry.py --check`; медленные файлы судит канон. Нужен критик на план до кода.

Карточка: `docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md`, карточка C3-i — читать там, не копировать сюда.

Свидетель: реестр, строки `case_preconditions` (:314), `reporter_rehearsal_identity` (:524), `environment_property_cover` (:547); `gate_registry.py` находка «registered more than once».

Принципы и правила: FR-59, FR-17; AR-15, AR-28.

Решение владельца нужно: нет.
