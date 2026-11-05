# Срочная починка прогона TP1-12586 — пачка 1: прогон проходит S3–S5 и гейты без простоя

кучка: `hotfix-12586` | статус: закрыта | взял: dev2, 23.10.2026 | ветка: `pile/hotfix-12586/batch-1` | MR: `9daca079` | стенд: нужен (живое доказательство) | приоритет: П1 | issue: —

очередь: conductor/1 → hotfix-12586/1

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего, живые
доказательства (FR-33) сделаны или переданы строкой в кучку «живые прогоны».

Решения владельца: 22.10.2026 — слова в находках (GW1-12 «это надо убрать»; GW1-13 «фабрика должна говорить, чего ей не хватает,
сразу»; GW1-14 «один Then нельзя закомментировать и передать человеку, даже если пользователь согласен»; OH3-10 — ошибка пробы в
бэклог фабрики); 23.10.2026 — «починить срочно отдельной пачкой; долгие тесты и регрессии в конце пачки; хотфикс — только через
критика на соответствие архитектуре»; D-0056 (тесты на уровне пачки).
Порядок по общим файлам: `gate_preflight.py`: HF1-1 → HF1-3 → HF1-9; `references/host-report-forms.json`, `host_probe.py`: HF1-5 → HF1-7;
`skills/qa-story/SKILL.md`: HF1-8 (единственный писатель); `window_record.py`: HF1-3; `story_step.py`: HF1-7; `gate_brief.py`: HF1-9.
Пути «Пишет в»: пакета — от `ai-packages/qa-factory/`.
Скоуп свидетеля (D-0056 — у билдера только точечные проверки): HF1-1 — `test_node_ids.py`, `test_gate_preflight*.py` (ключи DoD);
HF1-2 — `test_execution_fingerprint*.py`; HF1-3 — `test_profile_shared_root.py`, `test_execution_request*.py`, `test_window_record*.py`;
HF1-4 — `test_stand_access.py`; HF1-5 — `test_host_probe*.py`; HF1-6 — `test_brief_pack*.py`; HF1-7 — `test_dispatch_liveness*.py`,
`test_worker_lifecycle*.py`, `test_story_step.py` только ключ `pause`; HF1-8 — `test_window_budget*.py`, эвалы `skills/qa-story/evals/`;
HF1-9 — `test_gate_preflight*.py`, `test_gate_brief*.py`; HF1-10 — `test_s5_precheck*.py`, `test_manifest_put*.py`,
`test_check_coverage*.py`, `test_report_facts*.py` (имена — проверить по коду). Интегратор, один раз после схождения — BATCH CANON:
соседи-импортёры, `python -B scripts/selftest.py --limits --lang`, `test_audit_rules.py`, `test_null_outcomes.py`,
`test_gate_registry.py`, `tools/dup_ratchet.py --check`, `tools/lint_ratchet.py --check`, мутации по спискам узлов, CI `package-fast`.
Общий бриф дизайнерам: карточка кучки («Дороги», «Содержание»); находка узла целиком; дифф хотфикса для соседних узлов;
`PROJECT.md` P3, P5, P13, P15, P19, P21, P22; `references/human-questions.md`; FR и AR из строки узла; вернуть спеку в
`docs/tasks/specs/t-nnn-hf1-n.md` с развилками наверх; слово человека сопоставляется только идентификатором целиком, неизвестное —
вопрос, не проход; ошибка допустимого направления — «не проверено», никогда «проверено».

## Бриф

Что сделать: за одну пачку закрыть десять находок прогона TP1-12586. Шесть из них уже исправлены чужой рукой в релизной копии
(ветка `hotfix/qa-factory-0.10.1`, `C:\Projects\qa-factory-0.10.0`): критик HF1-0 судит дифф против находок, FR и AR и выдаёт по
фиксу вердикт «принять как есть / поправить (что именно) / переписать»; билдеры HF1-1…HF1-6 переносят фикс с правками вердикта
на `main` этого репозитория (пакет `main` = база релизной копии). Четыре узла проектируются здесь: OH3-16 (сам затык, не сосед),
GW1-12, GW1-13, GW1-14 — дизайнер → билдер → критик.
НЕ делать: правок в релизной копии (релиз 0.10.1 собирается отсюда по разделу «Релиз» PROJECT.md); остальных узлов кучек-источников;
находок доктора 22.10; живого доказательства в этой пачке сверх одного повтора S5 TP1-12586 (остальное — `live-runs`).

## Узлы

Исполнитель «designer → builder → critic» — кодовый узел; «builder» — узел-документ. Статусы:
`ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| HF1-0 | П1 | Критик на дифф хотфикса `84e5d224..HEAD` ветки `hotfix/qa-factory-0.10.1` (26 файлов, 7 фиксов): по каждому фиксу — соответствие находке и её «что сделать», FR и AR узла, стоячие вопросы DUPLICATION и CODE QUALITY (`docs/tasks/critic-diff-brief.md`); особо — неотслеженный и нечитаемый кодом `references/host-report-forms.json` (AR-1: имя инструмента хоста — данные, не код), красный ключ `test_run_suite_mine.py` 528/529, свипы соседей, названные в узлах-источниках. Вердикт по фиксу: принять / поправить / переписать; отчёт — спека переноса для HF1-1…HF1-6 (слово владельца 23.10.2026) | critic | отчёт `docs/tasks/handoffs/t-nnn-hf1-0-hotfix-review.md` | — | принято |
| HF1-1 | П1 | EP1-9: читатель node id обрывается на баннере `====` до списка тестов (`node_ids.parse_collected`); второй парсер того же вывода — `gate_preflight.first_collected_node`. Разделитель до id пропускается, один читатель вывода collect, «0 прочитано при N collected» — отказ читателя, не «тестов нет»; свип читателей вывода раннера. Перенос коммитов `ae42cb19`, `190299db` с правками вердикта HF1-0 (`execution-probes/findings/20261022-chitatel-node-id-ostanavlivaetsya-na-bannere.md`; AR-1, AR-13, AR-28, FR-59) | builder | `scripts/node_ids.py` (`parse_collected`), `scripts/gate_preflight.py` (`first_collected_node`), `scripts/tests/test_node_ids.py`, `changelog.d/` | HF1-0 | принято |
| HF1-2 | П1 | EP1-8: `execution_fingerprint.build` падает `TypeError` на форме `{path, sha256}` из своей карточки `role-commands.json`; обе формы через одну нормализацию с `verify_files`, заявленный `sha256` сверяется, отказ вместо трассировки, карточка = парсер (тест), свип «справка расходится с парсером». Перенос `66651cee`, `832fb2d1` с правками вердикта HF1-0 (`execution-probes/findings/20261022-otpechatok-padaet-na-forme-iz-svoej-spravki.md`; FR-1, FR-11, FR-14, AR-13) | builder | `scripts/execution_fingerprint.py`, `references/role-commands.json`, `scripts/tests/test_execution_fingerprint_records.py`, `changelog.d/` | HF1-0 | принято |
| HF1-3 | П1 | EP1-10: профили `api` и `ui` на одном `roots.test`, `execution_request._profile_for` при равных корнях молча берёт первый; пробы `not_executed`; `window_record` не читает слово человека; лишний `-v` в профиле (FB-7). Ничья профилей — селектор или отказ с дверью, репетиция гейта не «доказывает» профиль чужим тестом, онбординг различает корни и не дублирует флаги, недостающая проба со словом человека — пробел, не затык. Перенос `0cf6cc4b` с правками вердикта HF1-0; слово человека в `window_record` — проверить, закрыто ли хотфиксом, иначе доделать здесь (`execution-probes/findings/20261022-ui-testy-probuyutsya-pod-api-profilem.md`; FR-17, FR-59, AR-3, AR-28) | builder | `scripts/execution_request.py` (`_profile_for`), `scripts/probe_by_code.py` (`_profile_of`), `scripts/gate_preflight.py` (`Rehearsal._choose_test`), `scripts/window_record.py`, `scripts/onboarding_probe.py`, `skills/qa-onboarding/phases/p4-generate.md`, `scripts/tests/test_profile_shared_root.py`, `changelog.d/` | HF1-0, HF1-1 | принято |
| HF1-4 | П1 | OH3-10: проба входа шлёт литерал `{username, password}`, Test Project 1 ждёт `email` → 422, ошибка пробы ушла в бэклог проекта (FB-3, FB-4). Имена полей тела — данные `environment.access` (`user_field`/`secret_field`) с дефолтами, 4xx называет поле из ответа, квитанция не печатает секрет, ошибка пробы — в бэклог фабрики. Перенос `1cda1745` с правками вердикта HF1-0 (`onboarding-hooks/findings/20261022-proba-vhoda-shlet-username-a-stend-zhdyot-email.md`; AR-1, AR-22, FR-19) | builder | `scripts/stand_access.py`, `references/templates/config.json`, `skills/qa-onboarding/phases/p2-interview.md`, `skills/qa-onboarding/phases/p4-generate.md`, `scripts/tests/test_stand_access.py`, `changelog.d/` | HF1-0 | принято |
| HF1-5 | П1 | OH3-13: проба доставки контекста не видит ответ ребёнка через `SubagentHandback` (`host_probe._assistant_texts`, `check_child`): слова возврата читаются из `input` вызова, сам вызов — не «инструмент ребёнка»; форма возврата хоста — файл данных `references/host-report-forms.json` с одним читателем (AR-1, AR-5), общий с HF1-7. Перенос `1799472b` + файл форм хоста, с правками вердикта HF1-0 (`onboarding-hooks/findings/20261022-proba-konteksta-ne-vidit-otvet-cherez-subagenthandback.md`; FR-33, FR-41, AR-5) | builder | `scripts/host_probe.py`, `references/host-report-forms.json`, `scripts/tests/test_host_probe_handback.py`, `changelog.d/` | HF1-0 | принято |
| HF1-6 | П1 | OH3-14: стратег S3 (окно разметки) послан за `grounding_labels` / `requirement_grounding_states` в `handoffs/vocabulary.yaml` плагина, гард чтение плагина запрещает. Бриф окна 1 вкладывает оба списка через общий читатель словаря, `s3.md` не шлёт роль в плагин, свип по `phases/`, агентам и формам. Перенос `40906231` с правками вердикта HF1-0 (`onboarding-hooks/findings/20261022-strateg-ne-mozhet-prochitat-slovar-metok.md`; FR-15, FR-2, AR-8, AR-10, AR-13) | builder | `scripts/brief_pack.py` (окно 1 S3), `skills/qa-story/phases/s3.md`, их тесты, `changelog.d/` | HF1-0 | принято |
| HF1-7 | П1 | OH3-16: завершившийся критик считается живым — возврат Claude Code через `SubagentHandback` и `meta.json finished: true` не читаются `dispatch_liveness` (признаются только `task_complete` Codex и `returned_at` хука); `finish` отказан вердиктом, `pause` — «живой», отмена запрещена — обычная доработка по reject идёт только словом человека. Возврат Claude Code → `RETURNED` через адаптер хоста (форма — `host-report-forms.json` из HF1-5), проверка хука SubagentStop, пауза без слова при `RETURNED`; сосед из хотфикса `1c53d483` (`worker_lifecycle.active_binding` через `binding_is_active`) входит сюда по вердикту HF1-0 (`onboarding-hooks/findings/20261022-zavershivshijsya-kritik-schitaetsya-zhivym.md`; P22, FR-41, AR-5, AR-25) | designer → builder → critic | `scripts/dispatch_liveness.py`, `scripts/story_step.py` (`pause`), `scripts/worker_lifecycle.py` (`active_binding`), `scripts/install_smoke.py`, их тесты, `changelog.d/` | HF1-5 | принято |
| HF1-8 | П1 | GW1-12: после записи решения гейта дирижёр всегда останавливается и просит набрать `/qa-factory:qa-story` (безусловная строка `SKILL.md:125`), хотя `boundary_notice` смены окна не просил. Слово владельца «это надо убрать»: после гейта — следующая стадия в том же окне; смену окна решает только `boundary_notice`; остаётся только `stop_after: gate_A` по слову человека; гейт B так же; ответ `gate-decision` читается целиком (поле `next`) (`gates-and-words/findings/20261022-ostanovka-posle-gejta-bezuslovnaya.md`; P3, FR-48, FR-41, AR-15) | designer → builder → critic | `skills/qa-story/SKILL.md`, `skills/qa-story/phases/s4.md`, `skills/qa-story/phases/s8.md`, `scripts/window_budget.py`, `scripts/controller.py` (ответ `gate-decision`), эвалы `skills/qa-story/evals/`, их тесты, `changelog.d/` | — | принято |
| HF1-9 | П1 | GW1-13: пробел интеграции стенда известен с онбординга (`integrations[jira-integration]`, `required_by`, ключей в `.env` нет), бриф гейта A о нём молчит, человек узнал в S5. Репетиция гейта A сопоставляет кейсы плана с `integrations[].required_by` и ключами: пункт «After your approval» с тремя ответами, именем кейса и шага; секрет человек кладёт сам (`gates-and-words/findings/20261022-probel-integracii-ne-nazvan-do-gejta-a.md`; P5, FR-50, FR-59, AR-22, AR-28) | designer → builder → critic | `scripts/gate_preflight.py`, `scripts/gate_brief.py`, `scripts/env_probe.py` (читатель), их тесты, `changelog.d/` | HF1-1, HF1-3 (`gate_preflight.py`) | принято |
| HF1-10 | П1 | GW1-14: один невыполнимый Then нельзя отдать человеку — при зелёном тесте кейса строка «Then-остаток — человеку» отказана `s5_precheck` partial-green, слово человека — `WORDS_REFUSED_AT_SOURCE`. Манифест получает единицу уровня Then (`then_bindings` + `unresolved` с владельцем), partial-green принимает названный остаток, отчёт — «Left with you» и третий исход (`gates-and-words/findings/20261022-odin-then-nelzya-otdat-cheloveku.md`; P13, P17, P19, P21, FR-4, FR-9) | designer → builder → critic | `scripts/contract.py`, `scripts/s5_precheck.py` (partial-green), `scripts/manifest_put.py`, `scripts/manifest_from_tests.py`, `scripts/ledger.py`, `scripts/check_delivery.py`, `scripts/report_facts.py` («Left with you»), `scripts/traceability.py`, `references/block-names.json`, `references/artifact-contract-automation.md` и его slices, `agents/qa-automator.md`, `skills/qa-story/phases/s5.md`, `design/state-exits.md`, их тесты, `changelog.d/` (ряд расширен по спеке t-052, F1 — молчаливый проход шире отказа) | — | принято |
| HF1-11 | П1 | Свипы двух классов словом владельца 23.10.2026 (вариант «а»: красное — узлами сюда): (1) класс EP1-8 «справка расходится с парсером» — все карточки `references/role-commands.json` с полем `input` (14) против парсеров скриптов и тестов; (2) класс OH3-14 «роль отправляют читать плагин» — все упоминания `vocabulary.` и путей плагина в текстах ролей и оркестратора (30 файлов) против правила гарда `guard_pre_tool.py`; дайджест с вердиктом по строке | scout | дайджест `docs/tasks/specs/reports/t-063-hf1-11-sweeps.md` | HF1-2, HF1-6 | принято |
| HF1-12 | П1 | Класс EP1-8 по дайджесту HF1-11: 7 карточек `role-commands.json` расходятся с парсером — `manual_evidence.py write-block` (не все поля записи), `export` (нет `--output`), `manual_capture.py ui` («начинается с goto» против «есть goto»), `artifact_producer.py publish` (нет `--kind`, `--expected-hash`, границ `work/`), `external_writes.py --record` (нет `--external-id`, `--remote-revision`), `plan_row.py` (`1`/`0`/`yes`/`no`/`on`/`off` — булевы, карточка говорит «цифры — числа»; нет `--task`), `context_bundle.py` (не все поля; отказ не печатает закрытые списки). Карточка = парсер, и правило против повтора на верхнем уровне: `test_role_commands.py` кормит КАЖДУЮ карточку её же валидным примером, не только `{}`; решения Lead: код `plan_row` оставить, карточку поправить; `manual_capture ui` — карточка по коду; `context_bundle` — отказ печатает списки (FR-1) (`docs/tasks/specs/reports/t-063-hf1-11-sweeps.md` q1-02…q1-14; FR-1, FR-11, FR-14, AR-13) | builder | `references/role-commands.json`, `scripts/context_bundle.py` (тексты отказов), `scripts/tests/test_role_commands.py`, их тесты, `changelog.d/` | HF1-11 | принято |
| HF1-13 | П1 | Класс OH3-14 по дайджесту HF1-11: `references/artifact-contract-plan.md:92` («Words: `vocabulary.grounding_labels`, `requirement_grounding_states`») и его slice стратега называют роли список, который она прочитать не может — значения даются в тексте через один читатель словаря (генератор slices), slice пересобирается `contract_slices.py --write`; две группы «неясно» дайджеста (плейсхолдеры форм `handoffs/*.yaml` без значений; `common-rules.md:142` «verify scripts/hooklib.py»; `adapters-read.md:101`) — вопросы замысла владельцу, находкой в `roles-context` (`docs/tasks/specs/reports/t-063-hf1-11-sweeps.md` q2-red1, q2-red2; FR-15, AR-8, AR-13) | builder | `references/artifact-contract-plan.md`, `references/slices/qa-test-strategist/artifact-contract-plan.md` (generated), `scripts/contract_slices.py` (если значения подставляет генератор), их тесты, `changelog.d/` | HF1-6, HF1-11 | принято |
| HF1-14 | П1 | Часть EP1-10, возвращённая HF1-3 вопросом Q1: проба `not_executed` со словом человека не читается `window_record`/контроллером — окно S5 стоит. Ниже по течению единица уже есть (D-0013: `unverified` критика + `sensitivity_proof_missing_reason` → `review_unverified` → «Left with you»), ломается только окно S5: блок `probe_gap` на элементе окна, записанный `window_record` только при слове человека на этот instance (идентификатор, не фраза; `*` не открывает), `contract.window_shape_errors`, `validate_window`, `controller._s5_completion_problems` принимают его одним коммитом (AR-22); спека t-068, развилки решены Lead 23.10 (F1 a, F2 a, F3 b, F4 a, F5 a, F6 a, F7 a) (`docs/tasks/handoffs/t-055-hf1-3.md` Q1; FR-4, FR-57, AR-22, AR-28) | designer → builder → critic | `scripts/window_record.py`, `scripts/contract.py` (`window_shape_errors`), `scripts/acceptance.py`, `scripts/controller.py` (`_s5_completion_problems`), их тесты, `changelog.d/` | HF1-10 | принято |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 23.10 12:1x — пачка собрана Lead (dev2) из десяти находок трёх кучек словом владельца 23.10.2026; база релизной копии
  `84e5d224` = пакет `main` (`diff -rq`, контроль — дифф с веткой хотфикса); тесты хотфикса в его дереве: `test_node_ids` 56/56,
  `test_execution_fingerprint_records` 12/12, `test_host_probe_handback` 9/9, `test_profile_shared_root` 14/14, `test_stand_access`
  120/120, `test_worker_lifecycle_active` 14 OK, `test_run_suite_mine` 528/529 (красный ключ — разбор у критика HF1-0).
- 23.10 12:3x — взята (83576306 на ветке `pile/hotfix-12586/batch-1`; пуш в `main` закрыт — коммит взятия идёт в `main` через MR
  пачки); красный ключ `test_run_suite_mine` edge 5 красный и на `main` (контроль) — среда Windows, в пачку не входит. Диспатчи:
  t-048 критик HF1-0 на дифф хотфикса; дизайнеры t-049 HF1-7, t-050 HF1-8, t-051 HF1-9, t-052 HF1-10 (параллельно; дизайнеры и
  критик в лимит билдеров не входят).
- 23.10 13:5x — приняты t-048 (вердикт критика: `docs/tasks/specs/reviews/t-048-hf1-0-hotfix-review.md` — 5 фиксов «принять с поправками»,
  OH3-14 и сосед OH3-16 — переписать; A1, B1, C1–C3, D3, E1, E2 блокируют перенос) и спеки t-049…t-052 (развилки решены Lead, см. журнал);
  билдеры t-053…t-058 (HF1-1…HF1-6) в worktree параллельно. Ночной `package-full` на `main` 93b29079 (пайплайн 7964370, слово владельца
  23.10): красный только храповик медленных тестов (23 изменения при лимите 5, selftest 407/415 без FAIL, install smoke зелёный) —
  `scripts/slow_tests.json` перезаписан из `selftest.txt` ночного джоба 27900015 (`selftest.py --slow-tests --from … --update`, после — 0 изменений).
  Открытый вопрос владельцу: «ошибка пробы — в бэклог фабрики» (EP1-8 (6), OH3-10 (4)) — какой носитель: `qa-factory/factory-backlog.md`
  проекта (по шаблону это и есть реестр находок фабрики со scope `upstream-candidate`) или что-то иное.
- 23.10 14:1x — слово владельца: «если находка была записана как upstream candidate — то всё правильно». Носитель — `qa-factory/factory-backlog.md`
  проекта со scope `upstream-candidate`; код пачки не меняется; живое доказательство проверяет scope строк FB-3/FB-5 прогона 12586,
  расхождение — находка в `onboarding-hooks`, не узел пачки. Вопрос о свипах (14 карточек `input`, 30 файлов `vocabulary.`) —
  варианты (а) узлы сюда / (б) скаут сейчас, красное — находками в кучки-источники / (в) только очередь; рекомендация Lead — (б); ждёт слова.
  Принят t-054 (HF1-2): 71/71, отчёт `docs/tasks/handoffs/t-054-hf1-2.md` (сохранён Lead: изоляция worktree не пускает билдера писать в
  главный чекаут — путь `handoff:` для worktree-билдеров давать внутри worktree, интегратор забирает при слиянии).
- 23.10 14:4x — приняты t-053 (HF1-1, 68/68 + 995/995), t-057 (HF1-5, 30/30 + 44/44), t-058 (HF1-6, 520/520 + 354/354); их ветки слиты в
  `pile/hotfix-12586/batch-1` (01d3f2d6, 1d530217, bd3a4998, d9415063), запушено. Вторая волна: t-059 HF1-10, t-060 HF1-7 (после слияния
  HF1-5), t-061 HF1-8, t-062 HF1-9 — все в worktree; в работе ещё t-055 HF1-3 и t-056 HF1-4 (6 пишущих билдеров — потолок D-0054).
  Очередь интеграции (не билдерам): `story_run.py:7775` → `H.grounding_vocabulary_line()` (зона conductor/1 — текст замены в
  `docs/tasks/handoffs/t-058-hf1-6.md`); смоук-кейс handback в `install_smoke.py` (текст в `t-057-hf1-5.md`); строка `plans/features.json`
  для `references/host-report-forms.json` (WARN атрибуции); аналоги HF1-6 (бриф `ticket_changed`/rework, окно плана) — находкой.
- 23.10 16:1x — приняты t-056 (HF1-4, 153/153 + 10/10 + 59/59; слит f24a8133) и t-055 (HF1-3 как порт, 88/88 + 258/258 + 366/366; слит
  f02f4e2a). Часть HF1-3 «`window_record` читает слово человека на пробел пробы» возвращена билдером вопросом Q1 (нужны `contract.py`,
  `controller.py`, `acceptance.py`; та же дорога, что остаток Then → человеку в HF1-10): решение Lead — отдельный узел HF1-12 после
  приёмки HF1-10, через ту же единицу «остаток с владельцем и словом», не второй механизм. Lead поправил три фикстуры вне зон узлов
  (`test_config_migration.py`, `test_install_retire.py`: ключи `user_field`/`secret_field`; `test_test_novelty.py`: `profile_id`) —
  435/435, 302/302, свидетель novelty в журнале. Сессия 15:1x–16:0x стояла: рабочая папка ушла в `ai-packages/qa-factory`, хуки
  (`python tools/…` относительно cwd) отбивали каждый вызов; владелец вернул папку — находка класса «хук привязан к cwd сессии» в `forge`.
  Слово владельца по свипам — вариант (а): узел HF1-11 (скаут t-063), красные строки станут узлами пачки.
- 23.10 17:3x — приняты и слиты: t-061 HF1-8 (fe772a60), t-060 HF1-7 (98d1471e), t-065 HF1-13 (0b48eca8), t-062 HF1-9 (463ad0bf), t-059 HF1-10
  (48264deb; конфликт в сгенерированном `slices/qa-automator/index.md` решён пересборкой `contract_slices.py --write`). Скаут t-063 принят:
  7 красных карточек → HF1-12 (t-064), 1 красная строка контракта плана → HF1-13; две группы «неясно» — вопросы замысла владельцу (находка в
  `roles-context`). HF1-14 открыт из Q1 HF1-3 — дизайнер t-068. Фикс-раунд HF1-10 (решение 1: `*` не открывает неназванный остаток Then на
  выходном гейте) + строка `s5_integrations` в `report-risk-words.json` — свежий билдер t-067. Интеграционный батч t-066 (смоук-кейсы handback,
  атрибуция новых файлов в `features.json`, ось карты). Находка билдеров: worktree режутся от `main`, не от головы пачки — зависимости узлов
  сходятся только на слиянии интегратора (находка в `forge`). Очереди в кучки: gates-and-words — Q1–Q3 спеки t-051, слепое пятно `stand_gaps`,
  развилка K3, F-6/F-7 из t-050; execution-probes — дубль gate-collect runner, `_in_test_root`, `_root_rel`/`_node_prefix`; onboarding-hooks —
  `manual_capture.login.http.body` как второй носитель полей входа, брифы `ticket_changed`/rework без словаря, F9 `host_dispatch.record`;
  conductor/1 — `story_run.py:7775` → `H.grounding_vocabulary_line()`, `story_run.py:113` `UNTIL_PAST` второй список `stop_after`.
- 23.10 19:1x — все 14 узлов слиты, голова `74547e19` (HF1-12 6abc4a9c, t-066 9e8e8443, t-067 ef40b841, HF1-14 ff). Draft MR !3 открыт
  (https://git.example.com/dev1/yml-text-factory/-/merge_requests/3). Запущены: критик пачки t-070 (один проход, R13-g),
  мутационный проход t-071 (BATCH CANON), фикс-раунд CI t-072 — MR-пайплайн красный: `forge-check` (4 новые f-строки без подстановок),
  `package-fast` (аудит A22/A25: инжект qa-automator 41 682 Б, запас 318 Б — тексты HF1-3/HF1-10 сжать). Локальный канон часть 1:
  храповик дублей 0 новых, `--limits --lang` 3/3, аудит 295/297 (те же A22/A25), реестры и большие соседи зелёные (`test_story_step` ещё идёт).
  Решения владельца 23.10: релиз 0.10.1 в `QAFactory` после схождения; вопросы по группам «неясно» свипа заданы (ответ ждёт).
- 23.10 20:4x — критик пачки t-070: «принять с фикс-раундом» (3 блокера, 10 правок; `docs/tasks/specs/reviews/t-070-hf1-batch-review.md`);
  t-073 (B3 композиция «Left with you» 452/452, F1, F2, F3) слит c99caa64; t-074 (F4: 21 находка в 6 кучках) слит ec3b077a; t-072 (CI:
  lint 0 новых, инжект автоматора 1 439 Б, стратег — в работе). Слова владельца 23.10 на вопросы свипа (RC1-9): группа 2(а) — фразу
  «verify scripts/hooklib.py» из `common-rules.md` убрать; 2(б) — указатель на `phases/s0.md` из `adapters-read.md` убрать (S0 делает код
  по фазе: дирижёр в сессии скилла, драйвер в headless; скаут получает снимок) — оба в t-072; группа 1 — владелец спросил о ссылке на файл
  со значениями, Lead ответил: ссылка не обязывает (отказ + контекст), форма не входит в инжект A22, рекомендация (i) `handoff_init`
  подставляет значения — ждёт последнего слова. Канон часть 1 завершён: `test_story_step` 601/601, все зелёные кроме A22/A25 (t-072).
- 23.10 22:1x — слово владельца по группе 1: вариант (i) (`handoff_init` подставляет значения; записано в RC1-9, узел `roles-context`).
  Слиты t-072 (a255254e + 564780b9: служебные файлы сессии из коммита билдера убраны из индекса), t-071 (b1e6e070: мутации 108 убиты /
  9 выжили, откаты sha256), 1e1f22f7 (три отчёта t-053/t-054/t-057 и журнал). Фикс-раунд выживших t-075 (в т.ч. `_integration_cases`:
  точное равенство id вместо подстроки). Канон часть 2 и CI MR — в работе.
- 24.10 01:5x — BATCH CANON закрыт: канон 1+2 (храповики 0 новых, `--limits --lang --contracts` 5/5, `--hygiene` 1/1, аудит 297/297,
  38 тестовых файлов зелёные, `test_story_step` 601/601, `install_smoke` PASSED, slices свежие); мутации 117/117 убиты после t-075
  (`_integration_cases` уже сверяла точным равенством — дыра теста); фикс-раунды t-076 (4 красных `selftest --fast` на CI, атрибуция),
  t-077 (lint), t-078 (`story_step` F4) слиты; CI MR !3 зелёный на fe15e68d. Давние красные не пачки (красны и на `origin/main`):
  `test_run_suite_mine` edge 5, `test_test_novelty` symlink, `test_story_run_loop_b` `KeyError: is_error` — находка в `conductor`.
  Релизный коммит 0.10.1: CHANGELOG собран из 15 фрагментов (`changelog_assemble.py --version 0.10.1 --date 2026-10-24`), версии
  `.claude-plugin`/`.kimi-plugin`/`.plugin` → 0.10.1 (`.codex-plugin` несёт build-id Codex-маркетплейса, не трогается). Остаток до
  закрытия пачки: живое доказательство на стенде владельца (повтор S5 TP1-12586 с 0.10.1) — строка «Живые доказательства».
- 24.10 09:1x — релизная копия 0.10.1: чекаут `C:\Projects\qa-factory-0.10.0`, ветка `release/qa-factory-0.10.1` от `origin/feat/qa-factory`
  (= 84e5d224, релиз 0.10.0), коммит 9e5ebe34 (103 файла, отпечаток 420 файлов записан и проверен, `--lang` 2/2). Пуш на githost под VPN
  не прошёл: HTTPS 403 для учётки dev2, SSH без ключа (`feat/qa-factory` пушила Dev1). Бандл для переноса —
  `C:\Projects\release-qa-factory-0.10.1.bundle`. MR !3 в `main` — Draft снят, CI зелёный, ждёт слияния владельцем. Пачка «сдано»;
  закрытие (`piles.py close hotfix-12586 1 --hash …`) — после слияния и живого доказательства.
- 01.11 — закрыта по слову владельца 01.11.2026 (пересборка бэклога): открытых узлов нет

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|
| повтор S5 TP1-12586 на копии `testproject1-dev-010` с пакетом пачки: список тестов читается, отпечаток принимает `{path, sha256}`, UI-пробы под `ui`, один Then отдан человеку, критик после возврата не «живой», пробел Jira назван до гейта A, после гейта фабрика едет дальше | `testproject1-dev-010` / testproject1-sdk | владелец | перенос: live-runs/2 «Живые доказательства» \| обоснование: пересборка бэклога \| подтвердил: владелец, 01.11.2026 (слово 2 пересборки) |

## Остатки
