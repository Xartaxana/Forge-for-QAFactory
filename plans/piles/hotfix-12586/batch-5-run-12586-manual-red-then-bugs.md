# Срочная починка прогона TP1-12586 — пачка 5: ручные проверки, группировка тестов S5, красный Then, баги после S8 (релиз 0.10.5)

кучка: `hotfix-12586` | статус: закрыта | взял: dev1, 28.10.2026 | ветка: `pile/hotfix-12586/batch-5` | MR: `4fe77ddb` | стенд: нужен (живое доказательство) | приоритет: П1 | релиз 0.10.5 | issue: —

Открыта Lead пачки 28.10.2026 по D-0044: пачка 4 взята и заморожена, следующие находки кучки ложатся сюда строками тем же ходом, что файлы в
`findings/` (пять находок 28.10.2026: четыре — сюда, пятая — в пачку 6). Пачка НЕ взята: взятие заморозит её.

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего, живые доказательства (FR-33) сделаны или
переданы строкой в кучку «живые прогоны».

Слова владельца 28.10.2026 (обязательны):
- Учётки ручных проверок: «все 3 варианта. Если пользователей дал человек, или нашли в настройках, то его можно использовать. Если ничего нет, то создаём сами».
- UI ведёт агент: «Как пользователь. агент же видит что происходит на экране. Его задача пройти шаги. Не надо ограничивать агента. Может всплыть баннер, может уехать кнопка или ещё что, но цель проверки агент знает и должен это и проверить».
- Группировка тестов S5 (направления A+B отчёта t-1495): «Да, в 0.10.5».
- Красный Then: переставление Then — «это правильно»; роль аналитика 2c — «а это не правильно…»; цепочка — «принимаю»; FA-10 — «можно не комментировать если переставление возможно»; значение триажа — «Да, делаем».
- Баги после S8: репортёр открывается решением gate B, история закрывается после исполнения приказов gate B (оба выбраны владельцем 28.10.2026).
очередь: hotfix-12586/5 → hotfix-12586/9
очередь: hotfix-12586/4 → hotfix-12586/5
очередь: conductor/1 → hotfix-12586/5
очередь: hotfix-12586/2 → hotfix-12586/5
очередь: hotfix-12586/3 → hotfix-12586/5
очередь: onboarding-hooks/2 → hotfix-12586/5
очередь: speed-cost/3 → hotfix-12586/5
очередь: hotfix-12586/5 → execution-probes/2
очередь: hotfix-12586/5 → speed-cost/4
Порядок по общим файлам внутри пачки: `manual_capture.py`: HF5-1 → HF5-2 → HF5-3 → HF5-4 (по функциям — D-0048); HF5-3 и HF5-6 — `story_run.py` разными функциями; `qa-case-designer.md` (HF4-7 → HF5-3) и `phases/s0.md` (HF4-10 → HF5-6) — межпачечная очередь; `test-code-patterns.md`, `qa-automator.md`: G-1 и R7 — разные разделы и предложения, поздний сливает `main` (спека t-1502 §6). Скоуп свидетеля узла — только его точечные файлы (D-0056); BATCH CANON — интегратор, один раз.

## Бриф

Цель пачки: ручные проверки используют то, что фабрика знает (HF5-1…HF5-6, спека `docs/tasks/specs/t-1501-hotfix-12586-b5-manual-checks.md`, отчёт
`docs/tasks/specs/reviews/t-1497-manual-checks-factory-knowledge.md`); S5 группирует кейсы с общей подготовкой в один тест (G-1…G-3, спека
`docs/tasks/specs/t-1502-test-grouping.md`); один красный Then не блокирует остальные и не возвращает на S5 (R1…R7, ревью
`docs/tasks/specs/reviews/t-1500-red-then-blocks-and-triage.md`, спека в работе); решение gate B имеет исполнителя на закрытой истории (D1…D4, ревью
`docs/tasks/specs/reviews/t-1505-bug-after-s8-closed.md`, спека в работе). Узлы R и D получают спеку (t-1508, t-1509) до диспатча билдера; узлы
HF5 и G — спеки готовы, перед билдером критик на план закрыт (t-1504, t-1503).

Идентификаторы узлов: источники называют узлы G-1…G-3, R1…R7, D1…D4; в таблице они стоят под `HF5-7…HF5-20` (форма `<инициалы><N>-<n>`,
проверяет `tools/test_pile_cards_contents.py`), исходное имя — в начале ячейки «Что».

## Узлы

Исполнитель «builder → critic» — кодовый узел; спеки HF5 и G готовы. Статусы: `ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| HF5-1 | П0 | Честная ошибка шага с элементом: «не найден» только при `count()==0`, иначе «перекрыт `<tag.class>`» / «невидим» / «недоступен» / «не установлено» + скриншот (`findings/20261028-ruchnye-proverki-ne-ispolzuyut-to-chto-fabrika-znaet.md`; спека t-1501 §5.1) | builder → critic, живое доказательство FR-33 (повтор TC-010) | `scripts/manual_capture.py (PlaywrightBackend._timed, why_not_actionable, _run_step lookup и ветка StepFailed)`, `scripts/tests/test_manual_step_errors.py`, фикстура `run-12586-tc010/`, `changelog.d/` | — | принято: 9677fc13 |
| HF5-2 | П0 | Один читатель адреса фронтенда `env_probe.frontend_of`; `stand_hosts`, `environment_of`, цель логина, `stand_identity`, `stand_health._targets` читают через него; подсказка `url_key` (то же; спека t-1501 §5.2) | builder → critic | `scripts/env_probe.py`, `scripts/manual_capture.py (stand_hosts, environment_of, run_ui)`, `scripts/stand_health.py (_targets)`, `scripts/stand_identity.py (definition_sha)`, `skills/qa-onboarding/phases/p4-generate.md`, `docs/SIBLING_MAP.md` (ось 29), тесты, фикстура `run-12586-stand-config/` | — | принято: 5176f6bd |
| HF5-3 | П0 | Актор кейса: `--as` (роль, `env:U/S`, `created:`, `default`), автоактор, учётка от человека через env-файл, своя учётка, `request_actors`, вопрос до диспатча видит акторов, строка отчёта о созданных (то же; спека t-1501 §5.3) | builder → critic | `scripts/manual_capture.py (read_login, resolve_actor, build_parser, run_http, run_ui)`, `scripts/manual_evidence.py (prepare_request, request_actors)`, `scripts/story_run.py (Driver.stand_login_problem)`, `scripts/report_facts.py`, `agents/qa-runner.md`, `agents/qa-case-designer.md`, `references/manual-evidence.md`, тесты, фикстура `run-12586-actors/` | HF5-2; очередь HF4-7 → HF5-3 | принято: bb305f36 |
| HF5-4 | П0 | Агент ведёт UI как пользователь: наблюдение после каждого шага, слово `fill-account`, окно входа без экрана, тексты ролей без тупика (то же; спека t-1501 §5.4) | builder → critic, живое доказательство FR-33 | `scripts/manual_capture.py (page_words, _run_steps, _run_step, run_ui, _summary)`, `references/manual-capture-steps.json`, `agents/qa-runner.md`, `references/manual-evidence.md`, `docs/SIBLING_MAP.md`, тесты | HF5-1 (тот же билдер), HF5-3 | принято: 2fab3a1e |
| HF5-5 | П1 | Бриф ручного блока: команды `manual_capture ui|http [--as]`, `manual_evidence.py build`, секция «The stand» (то же; спека t-1501 §5.5) | builder → critic | `scripts/brief_pack.py (TOOLING["qa-runner"], manual_stand_lines)`, тесты | HF5-2, HF5-3 | принято: 5040a064 |
| HF5-6 | П1 | Снимок конфига у свежей истории и откат после S9/`stop` по окну записанных изменений; одна атомарная запись; строка отчёта с путём бэкапа (то же; спека t-1501 §5.6) | builder → critic | `scripts/config_contract.py`, `scripts/story_step.py`, `scripts/story_run.py`, `scripts/runtime_probe.py`, `skills/qa-story/phases/s0.md`, `skills/qa-story/phases/s9.md`, тесты | очередь HF4-10 → HF5-6 | принято: e686e8c6 |
| HF5-7 | П1 | G-1: одно правило группировки в трёх носителях (шаг 3 автоматора, «Executable shape», рубрика); подсказка группировки на плане; поле `apart_reason` и его читатели (`findings/20261028-s5-odin-kejs-odin-test.md`; спека `docs/tasks/specs/t-1502-test-grouping.md` §5.1) | builder → critic | `scripts/s5_plan.py`, `scripts/s5_precheck.py (plan_result, report)`, `scripts/brief_pack.py (plan_dispatch_lines)`, `agents/qa-automator.md` (шаг 3), `references/test-code-patterns.md` («Executable shape»), `references/code-review-rubric.md`, `references/slices/`, тесты, фикстура `run-12586-s5-plan/` | — | принято: 4d573f1c |
| HF5-8 | П1 | G-2: `fit_to_shapes.new` += `parameterize`; фраза о двух смыслах `consolidates` (то же; спека t-1502 §5.2) | builder → critic (тот же билдер, отдельным коммитом после HF5-7) | `handoffs/vocabulary.yaml`, `references/artifact-contract-automation.md`, `scripts/s5_plan.py (_test_words)`, `references/slices/`, тесты | HF5-7 | принято: 3e4a6007 |
| HF5-9 | П1 | G-3: живое доказательство FR-33 группировки — функций и экземпляров на кейс до/после, подсказка в `--check`, ни одного `blocked_by_check` Then от красного другого кейса, число перезапущенных экземпляров в раундах ремонта (то же; спека t-1502 §5.3) | Lead / прогон (FR-33) | нет (строка «Живые доказательства» пачки) | HF5-7, HF5-8, релиз 0.10.5 | закрыта: перенесено 01.11.2026 → live-runs/2 |
| HF5-10 | П1 | R1: текст дирижёра на вопрос «что с Then за красным»: сначала строка триажа и Self-probe notes кейса; перекрыт тем же дефектом — ответ без круга; иначе `rework --stage S7 --role qa-failure-analyst --purpose repair_verify`, не S5; слова человека — `--words-file` (`findings/20261028-odin-krasnyj-then-blokiruet-i-vozvrashchaet-na-s5.md`; ревью t-1500 §5 п. 1; спека: в работе (t-1508)) | builder → critic | `skills/qa-story/` (раздел S7/S8, вопросы человека) | — | принято: c01b6810 |
| HF5-11 | П1 | R2: отказ `controller.py:5656` называет дверь `--words-file` для правки строки, о которой просил человек (то же; ревью t-1500 §5 п. 2; спека: в работе (t-1508)) | builder → critic | `scripts/controller.py` (текст отказа), тест | — | принято: 68478d2c |
| HF5-12 | П1 | R3: роль аналитика, 2c и :16-18: «Then перекрыт тем же дефектом» → `blocked behind <case>` без прогона и второго bug draft; независимый Then → один диагностический прогон, затем `rework` при нужде; противоречие с «no repair from you» снято; строка Commands в брифе S7 (то же; ревью t-1500 §5 п. 3; слово владельца о 2c — «а это не правильно…»; спека: в работе (t-1508)) | builder → critic | `agents/qa-failure-analyst.md`, генератор брифа S7 (`scripts/brief_pack.py`, строка Commands), тесты | — | принято: c01b6810 |
| HF5-13 | П1 | R4: санкционированный диагностический прогон варианта теста на S7 (`purpose: diagnostic`): guard допускает инстанс, производный от инстанса в scope, и пишет run-блок; обход через `poetry run python` закрыт (то же; ревью t-1500 §5 п. 4; спека: в работе (t-1508)) | builder → critic | `scripts/stage_guard.py` (~1795-1815), `scripts/run_suite.py`, тесты | — | принято: 2e4f84e1 |
| HF5-14 | П1 | R5: детектор S5 «Then своего кейса за собственным красным»: у кейса строка `contradicts_requirement` с `thens: [n]`, другие Then на том же красном инстансе `covered` с тем же или более поздним `assertion_ref`; дверь — перенести выше или записать `blocked_by_check`; строки не закреплены → «порядок не установлен» (FR-59) (то же; ревью t-1500 §5 п. 5; спека: в работе (t-1508)) | builder → critic | `scripts/s5_precheck.py (red_links)`, тесты | — | принято: 12e59b32 |
| HF5-15 | П1 | R6: значение триажа «заблокирован красным другого кейса» — один баг на тот же R-n, не второй «unconfirmed» (слово владельца: «Да, делаем»; то же; ревью t-1500 §5 п. 6; спека: в работе (t-1508)) | builder → critic | `scripts/contract.py (triage_control_problems)`, `scripts/validate_artifacts.py (check_triage_v0)`, `references/delivery-verdict-kinds.json`, тесты | — | принято: f2c4cd65 |
| HF5-16 | П1 | R7: порядок Then и FA-10: красный по багу Then ставится последним; комментировать не нужно, если переставление возможно (слова владельца: «это правильно», «принимаю», «можно не комментировать если переставление возможно»; то же; ревью t-1500 §5 п. 8; спека: в работе (t-1508)) | builder → critic | `agents/qa-automator.md` (:107), `references/code-review-rubric.md` (измерение 6), `references/test-code-patterns.md`, тесты | G-1: разные разделы файлов | принято: 818bba85 |
| HF5-17 | П1 | D1: «закрыта» = gate B решён, S8 done И приказы gate B исполнены или отклонены; `next` после решения называет ход «завести баги»; предикат «приказ gate B на баги не исполнен» — один помощник для драйвера и контроллера; отказ закрытой истории не называет закрытые двери; интеграционный тест без заглушки `run_role`; `s8.md:322-325` переписан (`findings/20261028-reporter-bagov-zakryt-posle-s8-i-gejtom-dostavki.md`; ревью t-1505 §3 D1, §5 F2', F3, F6, F7; спека: в работе (t-1509)) | builder → critic | `scripts/controller.py (_closed_dispatch_refusal, next)`, `scripts/hooklib.py (story_closed)`, `scripts/story_run.py (after_gate_B)`, `skills/qa-story/phases/s8.md`, тесты | — | принято: f0351f5c |
| HF5-18 | П1 | D2: репортёр багов открывается решением gate B (непустые `selected_drafts` или слова), а не вердиктом доставки: правило 4 `stage_guard` и `delivery_gated_roles` меняются; наружная запись остаётся за `external_writes` (то же; ревью t-1505 §3 D2, §5 F1, §6; спека: в работе (t-1509)) | builder → critic | `references/stages.json` (`delivery_gated_roles`), `scripts/stage_guard.py (rule_delivery, :1085-1088)`, `scripts/gate_brief.py` (:3161-3163), `skills/qa-story/phases/s8.md`, тесты | HF5-17 (общий помощник предиката) | принято: 28e7cc73 |
| HF5-19 | П2 | D3: решение gate B хранит своё время; `story_closed` берёт его, а не `s8.finished` (то же; ревью t-1505 §3 D3, §5 F5; спека: в работе (t-1509)) | builder → critic | `scripts/hooklib.py (:485)`, `scripts/controller.py` (запись решения gate B), тесты | HF5-17 | принято: f0351f5c |
| HF5-20 | П2 | D4: после повторного открытия и завершения открытой работы история снова закрывается (повторный штамп или `reclosed_at`) (то же; ревью t-1505 §3 D4, §5 F4; спека: в работе (t-1509)) | builder → critic | `scripts/controller.py (:968-972)`, `scripts/hooklib.py`, тесты | HF5-17 | закрыта: перенесено 01.11.2026 → driver-hosts/1 |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

28.10.2026 14:5x — пачка взята (issue #29, ветка `pile/hotfix-12586/batch-5`). Строки узлов ведут спеки, их решения важнее текста строк: HF5-1…HF5-6 — `docs/tasks/specs/t-1501-hotfix-12586-b5-manual-checks.md` rev 2; HF5-7…HF5-9 — `t-1502-test-grouping.md` rev 2; HF5-10…HF5-16 — `t-1508-red-then-chain.md` (таблица «строка пачки → узел спеки»; R8/R9 — шаги внутри узла R7); HF5-17…HF5-20 — `t-1509-gate-b-executors-and-closure.md`. Готовы к критику: HF5-1, HF5-2 (t-1516), HF5-7/8 (t-1517). Lead пачки, 28.10.2026.
- 28.10 — пачка открыта Lead пачки по D-0044: четыре находки 28.10.2026 положены строками тем же ходом, что файлы в `findings/` (t-1510); спека R — t-1508, спека D — t-1509 в работе; пятая находка (FA-11) — в пачке 6.
- 01.11 — закрыта по слову владельца 01.11.2026 (пересборка бэклога): открытые узлы → driver-hosts/1, live-runs/2

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|
| повтор S1–S9 TP1-12586 на `testproject1-dev-010` на релизе 0.10.5 (FR-33): ручные проверки доходят до результата с честной ошибкой шага, учётками акторов и скриншотами; план S5 группирует кейсы; один красный Then не возвращает прогон на S5; баг заводится после gate B на закрытой истории | `testproject1-dev-010` | владелец | перенос: live-runs/2 «Живые доказательства» \| обоснование: пересборка бэклога \| подтвердил: владелец, 01.11.2026 (слово 2 пересборки) |

## Остатки
