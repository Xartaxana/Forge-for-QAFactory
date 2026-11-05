# Срочная починка прогона TP1-12586 — пачка 2: красный — обычный исход S5, Then — единица исхода, ответы человека применяются сразу, S5 к ≈ 22 минутам

кучка: `hotfix-12586` | статус: закрыта | взял: dev2, 25.10.2026 | ветка: `pile/hotfix-12586/batch-2` | MR: `855d4e5c` | стенд: нужен (живое доказательство) | приоритет: П1 | issue: —

очередь: hotfix-12586/2 → hotfix-12586/9
очередь: conductor/1 → hotfix-12586/2
очередь: hotfix-12586/1 → hotfix-12586/2
очередь: kb/1 → hotfix-12586/2
очередь: hotfix-12586/2 → gates-and-words/1
очередь: hotfix-12586/2 → execution-probes/1
очередь: hotfix-12586/2 → driver-controller/1
очередь: hotfix-12586/2 → report-delivery/1
очередь: hotfix-12586/2 → cost-dashboard/1
очередь: hotfix-12586/2 → speed-cost/4
очередь: hotfix-12586/2 → test-code-quality/1
очередь: hotfix-12586/2 → speed-cost/1
очередь: hotfix-12586/2 → hotfix-12586/3
очередь: hotfix-12586/2 → speed-cost/3
очередь: hotfix-12586/2 → run-honesty/1
очередь: hotfix-12586/2 → hotfix-12586/4
очередь: hotfix-12586/2 → hotfix-12586/5
очередь: hotfix-12586/2 → hotfix-12586/7
очередь: hotfix-12586/2 → execution-probes/2

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего, живые
доказательства (FR-33) сделаны или переданы строкой в кучку «живые прогоны».

Шлюз между волнами (слово владельца 25.10.2026):
- Волна 1 — HF2-1…HF2-15 и проход HF2-0 по волне 1. Волна 2 — HF2-16, HF2-17, HF2-18 и проход HF2-0 по волне 2.
- Перед первым диспатчем волны 2 взявший спрашивает владельца: «делаем вторую волну или не успеваем и делаем релиз без неё».
  Ответ записывается строкой «Хода».
- Без волны 2:
  - релиз режется из волны 1 после её BATCH CANON и прохода HF2-0;
  - узлы волны 2 остаются «ожидает» в этой пачке;
  - пачка не закрывается, пока они не приняты или не перенесены строкой «Остатков» с подтверждением человека.

Решения владельца:

25.10.2026 («Остальное по рекомендациям»; развилки — в разборе t-1224, §6):
- владелец, 25.10.2026: F-1 (а) — EP1-13 и остаток GW1-14 (HF2-2, HF2-5) остаются в пачке, та же функция; GW1-23 и HF2-1 — по словам владельца;
- владелец, 25.10.2026: F-2 (а) — CD1-14 без CD1-13: замер от него не зависит, функции разные (D-0048);
- владелец, 25.10.2026: F-3 (а) — TQ1-12 сейчас строками рубрики dim 2, образцы корпуса — с TQ1-4 после пачки;
- владелец, 25.10.2026: F-4 (а) — TQ1-13 сейчас строкой критика K16, поле `introduced_helpers` — с TQ1-7 после пачки;
- владелец, 25.10.2026: F-8 (а) — DC1-9, блокер в плане: узкая доработка плана до окон;
- владелец, 25.10.2026: F-9 (а) — ≈ 22 мин не условие закрытия, а измерение: стена печатается с объёмом, недостижение — находка;
- владелец, 25.10.2026: F-18 (а) — 19 узлов в одной пачке, две волны, превышение границы L записано (P13);
- владелец, 25.10.2026: F-19 (б) — при ответе «без волны 2» HF2-16, HF2-17, HF2-18 переносятся в пачку 3 строкой «Остатков» с подтверждением человека, пачка закрывается;
- владелец, 25.10.2026, F-17 («F-17 — во вторую волну, если не блокирует прохождение стори. Если блокирует, то чиним сразу»): пробел свипа HF2-1 вне
  узлов идёт во вторую волну; если он блокирует прохождение стори — он сразу становится новым узлом волны 1;
- владелец, 25.10.2026, по находке S7 («если нет, то это надо исправить во второй волне срочной пачки»): TQ1-15 — узел HF2-18, волна 2;
- Lead пачки, 25.10.2026: F-5 — GW1-3, GW1-7 после пачки (связь только по файлам); F-6 — остаток EP1-10 после пачки; F-7 — EP1-11 после пачки;
  F-10 (а) — новое имя причины рядом с `ledger.blocked_by` (например `blocked_by_check`), старое не переименовывается; F-11 — строки GW1-22 в
  роли критика и рубрике пишет HF2-3 в волне 1, HF2-16 перекладывает; F-12 — остаток GW1-14: F7, A1, A2 в HF2-5, F8 после пачки (сверить с
  t-074); F-13 — DC1-9 один узел; F-14 — пересечение с `conductor/1` закрыто `очередью:` и списками функций в `owns` (D-0048); F-15 — HF2-8
  и HF2-10 один дизайнер, последовательные билдеры; F-16 — первый ход HF2-6 сверка RD1-1 скаутом; F-20 (а) — проба у красного «неприменима:
  красный» без права слова, плюс замер в свипе HF2-1; F-21 (а) — `story_step.py` и `s5.md` добавлены в HF2-4 пометкой «вне строки-источника»,
  порядок HF2-4 → HF2-16.

25.10.2026:
- состав: GW1-22, GW1-21, EP1-16, RD1-8, CD1-14, EP1-18, DC1-9, EP1-17, EP1-15, TQ1-12, TQ1-13, TQ1-14; CD1-13 и TQ1-11 НЕ входят;
- «Скомпоновать их как тебе удобнее в связки» — связки собирает Lead;
- «DC1-9 как переделку стадии вынести во вторую волну той же пачки — да, перед началом второй волны нужно спросить, делаем мы её или не
  успеваем и делаем релиз без неё»;
- «последнюю проблему прогона стори нужно обязательно взять в срочную пачку» — GW1-23, HF2-4;
- «Как вообще получилось, что упавшие тесты не могут пройти дальше, если наша цель именно найти баги, то есть по умолчанию у нас должны быть
  красные тесты» — HF2-1;
- «22 минуты на 8 тестов звучит логичнее. Это цель всей доработки скорости»
  (`execution-probes/findings/20261025-s5-zapusk-testa-20-minut-obvyazki.md`, «Цель»);
- форма S5: «пишем общий план — один критик на всё — замечания критика — НЕ перезапускаем исправления плана, а сразу запускаем первое окно
  создания тестов, где автоматизатор получает все требования, план и замечания критика к этим тестам»;
- критик после кода: «проверка самих тестов. Покрытие можно проверить и по плану, а вот как написан код — только когда код есть. И надо
  проверить, что реализация соответствует плану» (`driver-controller/findings/20261025-cikl-okna-s5-25-minut-upravleniya.md`).

24.10.2026:
- смесь исходов в одном кейсе и «Ассерт — это по сути Then и есть» — GW1-22;
- «Ответы должны сразу учитываться в дальнейшем» — GW1-21;
- «переименование меняет code_sha и требует перепрогона» — EP1-15.

23.10.2026: «хотфикс — только через критика на соответствие архитектуре».

D-0056: тесты на уровне пачки.

Порядок по общим файлам:

| Файл | Порядок | Примечание |
|---|---|---|
| `contract.py` | HF2-2 → HF2-3 → HF2-4 | |
| `window_record.py` | HF2-3 → HF2-4 → HF2-12 → HF2-11 | |
| `acceptance.py` | HF2-3 → HF2-4 → HF2-11 | |
| `s5_precheck.py` | HF2-2 → HF2-3 → HF2-5 → HF2-12 → HF2-16 | функции разные; по D-0048 параллель допустима при непересекающихся функциях в `owns` |
| `manifest_put.py` | HF2-3 → HF2-5 | одна функция `_merge_entry` |
| `ledger.py` | HF2-3 → HF2-5 | |
| `check_delivery.py` | HF2-3 → HF2-6 | |
| `report_facts.py` | HF2-5 → HF2-6 | |
| `exit_gate.py` | HF2-2 → HF2-16 | |
| `controller.py` | HF2-4 → HF2-16 | |
| `brief_pack.py` | HF2-7 → HF2-16 → HF2-17 | |
| `manifest_from_tests.py` | HF2-12 → HF2-16 | |
| `execution_request.py` | HF2-8 → HF2-10 | одна функция `build_mine_request`, один дизайнер |
| `skills/qa-story/phases/s5.md` | HF2-16 → HF2-17 | HF2-4 — по F-21 |
| `agents/qa-automator.md` | HF2-3 → HF2-12 → HF2-16 → HF2-17 | |
| `agents/qa-code-critic.md`, `references/code-review-rubric.md` | HF2-3 → HF2-13 → HF2-14 → HF2-15 → HF2-16 → HF2-18 | волна 2 раскладывает строки по ПЛАН/КОД/ОБА; HF2-18 — после HF2-16, строка «ассерт строже требования» кладётся в готовое деление |
| `agents/qa-failure-analyst.md`, `skills/qa-story/phases/s7.md` | HF2-3 → HF2-18 | HF2-3 пишет S7 для красного по смеси исходов; HF2-18 — контрольный опыт до `APP_BUG` |

HF2-3 (GW1-22) и HF2-4 (GW1-23) ведёт один дизайнер; билдер HF2-4 идёт после HF2-3.

Единственный писатель:

| Узел | Файлы |
|---|---|
| HF2-7 | `story_run.py`, `question_*.py`, `planning_contract.py`, `gate_brief.py` |
| HF2-4 | `stage_done.py` |
| HF2-16 | `story_step.py`, `handoffs/s5-*.yaml` |
| HF2-10 | `run_suite.py` |
| HF2-8 | `probe_by_code.py`, `red_sandbox.py` |
| HF2-9 | `cost_capture.py`, `telemetry_hook.py`, `hooks/hooks.json` |
| HF2-11 | `proof_level.py` |
| HF2-2 | `judge_code.py` |
| HF2-3 | `traceability.py`, `delivery-verdict-kinds.json`, `artifact-contract.md`, `qa-case-designer.md`, `qa-failure-analyst.md` |
| HF2-14 | `test-code-patterns.md` |

Со зоной `conductor/1` — списки функций в `owns` (D-0048); поздний узел сливает `main`.

Пути «Пишет в»: пакета — от `ai-packages/qa-factory/`.

Скоуп свидетеля (D-0056 — у билдера только точечные проверки; имена — проверить по коду):

| Узел | Проверки |
|---|---|
| HF2-1 | след и вердикт по строке |
| HF2-2 | `test_then_remainder.py`, `test_judge_code.py`, `test_exit_gate_scope.py` |
| HF2-3 | `test_s5_precheck.py`, `test_then_remainder.py`, `test_manifest_put*.py`, `test_contract.py`, `test_ledger.py`, `test_check_delivery.py`, `test_traceability.py`, `test_window_record.py`, `test_acceptance_semantics.py`, ключи DoD, байты A22/A25 |
| HF2-4 | `test_window_record.py`, `test_contract.py`, `test_acceptance_semantics.py`, тест `_code_review_problems`, тест `stage_done`; живой кейс 12586 фикстурой: два красных теста, ноль слов человека |
| HF2-5 | `test_then_remainder.py`, `test_manifest_put*.py`, `test_ledger.py`, `test_report_facts.py`, `test_s5_precheck.py` — только ключ A2 |
| HF2-6 | `test_check_delivery.py`, `test_report_facts.py` |
| HF2-7 | `test_question_register.py`, `test_question_stop.py`, `test_question_branches.py`, `test_brief_pack.py`, `test_gate_brief_and_retro.py`, `test_planning_contract*.py`; часть `story_run.py` — только BATCH CANON/CI |
| HF2-8 | `test_probe_by_code.py`, `test_profile_shared_root.py`, `test_probe_binding.py`, `test_red_sandbox_node_ids.py`, `test_execution_request.py` — ключи `build_mine_request` |
| HF2-9 | замер медиан с носителем, `test_cost_capture_*.py`, `test_telemetry_hook*.py` |
| HF2-10 | `test_run_suite_mine.py`, `test_run_suite_reports.py`, `test_run_budget.py`, `test_execution_request.py` |
| HF2-11 | `test_proof_level.py`, `test_window_record.py`, `test_acceptance_semantics.py` |
| HF2-12 | `test_window_record.py`, `test_manifest_from_tests.py`, `test_s5_precheck.py`, ключи DoD |
| HF2-13…HF2-15 | документный свидетель (ключи до прогона, скрипт целиком, отрицательный контроль), байты A22/A25, `contract_slices.py --check` |
| HF2-16 | `test_story_step_pause.py`, `test_story_step_prompt.py`, `test_exit_gate_*.py` (ключи `digest`), `test_brief_pack.py`, `test_s5_precheck.py`, `test_manifest_from_tests.py`, ключи DoD, байты |
| HF2-17 | `test_brief_pack.py`, ключи DoD |
| HF2-18 | документный свидетель (ключи до прогона, скрипт целиком, отрицательный контроль), эвалы роли S7, байты A22/A25, `contract_slices.py --check` |

Интегратор после схождения КАЖДОЙ волны — BATCH CANON:
- соседи-импортёры;
- `test_story_step.py`, `test_story_run_*.py` по тронутым функциям;
- докер `python:3.12`;
- `python -B scripts/selftest.py --limits --lang --contracts`;
- `test_audit_rules.py`, `test_null_outcomes.py`, `test_gate_registry.py`, `test_field_producers.py`;
- `tools/dup_ratchet.py --check`, `tools/lint_ratchet.py --check`, `contract_slices.py --check`;
- мутации;
- CI `package-fast`.

Общий бриф дизайнерам. Каждому:
- карточка кучки;
- находка узла целиком;
- дифф пачки 1 (`84e5d224..74547e19`);
- `PROJECT.md` P3, P11, P13, P16, P17, P19, P20, P21, P22, P23;
- `references/human-questions.md`;
- FR и AR из строки узла.

Сверх этого по узлам:

| Узлы | Что ещё дать |
|---|---|
| HF2-3, HF2-4, HF2-8 | дайджест свипа HF2-1 |
| HF2-16 | `docs/tasks/handoffs/t-1222-code-critic-checks-split.md` |
| связка E | `docs/tasks/handoffs/t-1221-s5-slowness-12586-recon.md` |
| HF2-18 | находка `test-code-quality/findings/20261025-s7-ne-stavit-kontrolnyj-opyt.md`, скаут t-1226 |
| HF2-3, HF2-4 | `docs/tasks/handoffs/t-1225-red-test-review-receipt-recon.md` |

Спеку вернуть в `docs/tasks/specs/t-nnn-hf2-n.md`, развилки — наверх.

Правила для всех спек:
- слово человека сопоставляется только идентификатором целиком; неизвестное — вопрос;
- ошибка допустимого направления — «не проверено» или «не исполнен»;
- красный по требованию закрывает свой шаг своей записью, не словом человека;
- цифра времени без объёма прогона — не цифра.

## Бриф

**Что сделать.** Снять с прогона TP1-12586 то, что держит S5 часами и заставляет переделывать работу.

Волна 1:
- красный по требованию тест — исход по умолчанию: закрывает окно S5 своей квитанцией без слова человека и проходит цепочку S5–S9
  (сначала свип класса, затем узлы);
- кейс держит смесь исходов по Then до отчёта;
- отчёт не ставит pass неисполненному;
- ответ человека на вопрос S2–S4 сразу доходит до ролей;
- проба мутации работает при двух профилях;
- один collect на запрос;
- хук не замедляет вызовы вдвое;
- после правки фикстуры фабрика перепрогоняет тесты сама;
- поля строки манифеста роль знает до работы;
- строки критика и паттернов.

Волна 2 (после шлюза): один план автотестов и один критик плана, окна без простоя, бриф окна, контрольный опыт S7 до вердикта `APP_BUG`
(HF2-18). Цель — стена S5 ≈ 22 мин на 8 тестов
(было 3 ч 08 мин; объём прогона 22.10 — 8 кейсов, 3 окна).

**НЕ делать:**
- CD1-13, TQ1-11;
- соседей вне связок;
- правок в релизной копии;
- разреза `story_run.py` и `test_story_step.py`;
- волну 2 без слова на шлюзе;
- живого доказательства сверх повтора TP1-12586.

## Связки

- **A «Then и красный как единица»** (волна 1):
  - HF2-1 — свип класса, первым;
  - HF2-2 — EP1-13;
  - HF2-3 — GW1-22: FB-5 и пункт G8;
  - HF2-4 — GW1-23;
  - HF2-5 — остаток GW1-14;
  - HF2-6 — RD1-8.

  Один дизайнер на HF2-3, HF2-4, HF2-5. Пробелы HF2-1 — вход для HF2-3, HF2-4, HF2-8.
- **B «Ответы человека»** (волна 1): HF2-7 (GW1-21). GW1-3 и GW1-7 — после пачки: зависимость от них только по файлам.
- **C «Профиль пробы»** (волна 1): HF2-8 (EP1-16). Остаток EP1-10 — F-6.
- **D «Форма S5 и критик»**:
  - волна 1 — HF2-12 (EP1-18 (а)), HF2-13 (TQ1-13), HF2-14 (TQ1-14), HF2-15 (TQ1-12);
  - волна 2 — HF2-16 (DC1-9), HF2-17 (EP1-18 (б)), HF2-18 (TQ1-15, слово владельца 25.10.2026); один дизайнер на HF2-16 и HF2-17, HF2-18
    после HF2-16 на общих `code-review-rubric.md` и `qa-code-critic.md`.
- **E «Скорость S5»** (волна 1): HF2-9 (CD1-14, замер первым ходом) → HF2-10 (EP1-17); HF2-11 (EP1-15). EP1-11 — после пачки, вызов
  у него другой.
- **HF2-0** — критик, по проходу на волну.

Почему части D стоят в волне 1 (решила сама):

| Узел | Волна | Причина |
|---|---|---|
| EP1-18 (а) | 1 | «поля до работы» не зависят от формы S5; это минус два лишних диспатча, ≈ 15–20 мин (оценка) |
| EP1-18 (б) | 2 | бриф окна переопределяет DC1-9; писать его дважды — значит переписывать |
| TQ1-14 | 1 | строка «assert до распаковки» — класс КОД; вопрос об уровне работает в сегодняшней форме (сверка с `level` плана S3) и доедет до релиза без волны 2 |
| TQ1-12 | 1 | строки рубрики dim 2 — класс КОД |
| TQ1-13 | 1 | строкой критика (K16 есть в сегодняшней рубрике); поле тропы — с TQ1-7 |

## Узлы

Исполнитель «designer → builder → critic» — кодовый узел; «builder» — узел-документ. Статусы:
`ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| HF2-0 | П1 | Критик на дифф пачки — по проходу на волну после схождения (R13-g; слово владельца 23.10.2026). По каждому узлу: находка, FR и AR (вопрос 10), DUPLICATION и CODE QUALITY (`docs/tasks/critic-diff-brief.md`). Особо: красный по требованию закрывает окно своей квитанцией, а зелёный или неисполненный так не проходит (FR-18, FR-34); имя новой причины против `ledger.blocked_by`; одна формулировка «закомментированный Then»; A22/A25; в волне 2 — артефакт и передача плана S5 и стена S5 против цели. BATCH CANON прикладывается до вердикта. Вердикт: принять или фикс-раунд | critic | отчёты `docs/tasks/specs/reviews/t-nnn-hf2-wave1-review.md`, `…-wave2-review.md` | волна 1: HF2-1…HF2-15; волна 2: HF2-16, HF2-17, HF2-18 | принято: 9850a116 |
| HF2-1 | П1 | Свип класса «красный — исход по умолчанию: проход по цепочке S5–S9» (вопрос владельца 25.10.2026). Класс всплыл в прогоне трижды: partial-green (GW1-22), остаток Then только `handed_to_person` (GW1-14), красный тест без квитанции ревью (GW1-23). Скаут перечисляет каждую проверку, гейт, писателя квитанций и пробу цепочки приёма S5 и ниже, которые требуют зелёного прогона или зелёного базиса. Минимум: `s5_precheck`, `acceptance.validate_window`, `window_record`, `probe_by_code`, `red_sandbox`, приём контроллера (`_code_review_problems`, `_s5_completion_problems`), `contract.window_shape_errors`, `stage_done`, `ledger`, `check_delivery`, `traceability`; тексты `s5.md`–`s7.md` и ролей. Вердикт по строке: свой санкционированный путь (каким полем) или отказ / только слово человека — пробел, направленный в узел пачки (HF2-3, HF2-4, HF2-8 или по F-17). Каждое «зелёного не требует» — с позитивным контролем той же формы; отдельно — требует ли `probe_by_code` зелёного базиса (F-20). Форма — свип HF1-11 (FR-34, FR-21, FR-22, P21). Правило для пробелов вне узлов (слово владельца 25.10.2026, F-17: «F-17 — во вторую волну, если не блокирует прохождение стори. Если блокирует, то чиним сразу»): пробел, найденный свипом вне узлов, идёт во вторую волну; если он блокирует прохождение стори — он сразу становится новым узлом волны 1. Для каждого пробела дайджест пишет строку «блокирует прохождение: да / нет — почему» | scout → Lead | дайджест `docs/tasks/specs/reports/t-nnn-hf2-1-red-default-sweep.md` | — | принято (сделано: 9c0e8f0e, релиз 0.10.2) |
| HF2-2 | П1 | EP1-13: номер Then строки `then_bindings` и метка `then-remainder-unrecorded-` — по одному носителю в `contract.py` (читают `s5_precheck`, `judge_code`, `exit_gate`). Пин меток становится тестом «в `exit_gate` нет литерала метки». Чтение испорченного `then` — по FR-59 (`execution-probes/findings/20261023-ostatki-then-ostatka-dva-chitatelya-nomera-i-tag-v-dvuh-fajlah.md`; FR-14, FR-59, AR-13, AR-15) | builder | `scripts/contract.py`, `scripts/s5_precheck.py`, `scripts/judge_code.py`, `scripts/exit_gate.py`, `scripts/tests/test_then_remainder.py`, `changelog.d/` | — (HF1-10 принят) | принято (сделано: e07c6f7b, релиз 0.10.2) |
| HF2-3 | П1 | GW1-22: один кейс держит смесь исходов по Then/партиции — передано человеку, зелёное, красное по багу, заблокировано упавшей проверкой (вопрос владельца 24.10.2026; TC-005/TC-006 при красной MS Teams-партиции по багу TC-004). `partial-green`/`contradicts-but-green` сверяют зелёный с его партицией. Остаток Then обобщается на красный и заблокированный. Новая причина «заблокировано другой проверкой» (имя — F-10) идёт S4 → S5 → S6 (не `partial`) → S8 → S9 и в «Left with you». Ledger не теряет переданный Then рядом с `failed:*`. `manifest_put` снимает строку `unresolved[]` (FB-5). Пункт G8 «окно S5 для красного» — квитанцию и приём делает HF2-4 (GW1-23). Независимые Then не прячутся за красным: перенос до красного или комментарий с причиной; закомментированный или заблокированный Then — строка «Left with you»; критик кода ловит независимый Then за красным (слово владельца 24.10.2026). Пробелы HF2-1 — вход (`gates-and-words/findings/20261024-smeshannye-iskhody-v-odnom-keyse.md`; t-1216; P16, P17, P21, FR-13, FR-21, FR-34, AR-19, AR-23, AR-26, AR-27) | designer → critic на план → builder → critic | `scripts/s5_precheck.py` (`check_manifest`), `scripts/manifest_put.py` (`_partition_scoped`, `_merge_entry`), `scripts/contract.py` (`UNRESOLVED_REASONS`, `then_remainder_*`, `rollup_status`), `scripts/acceptance.py`, `scripts/window_record.py`, `scripts/ledger.py`, `scripts/traceability.py`, `scripts/check_delivery.py`, `references/delivery-verdict-kinds.json`, `references/artifact-contract.md`, `agents/qa-automator.md`, `agents/qa-case-designer.md`, `agents/qa-code-critic.md`, `references/code-review-rubric.md` (измерения 6 и 8), `agents/qa-failure-analyst.md` (S7), их тесты, `changelog.d/` | HF2-1, HF2-2; GW1-14 и GW1-8 приняты | принято (сделано: c683969e, релиз 0.10.2) |
| HF2-4 | П1 | GW1-23: красный по требованию тест получает расписку ревью окна S5 и проходит стадию без слова человека (слово владельца 25.10.2026: «последнюю проблему прогона стори нужно обязательно взять в срочную пачку»; найти баги — цель, красный — исход по умолчанию). `product:` со строкой `contradicts_requirement` — выводимый пробел окна (`window_record.derivable`); `probe` для него не нужен (вместо — запись «проба неприменима: красный» без права слова, F-20); `finish` выводит пару; контроллер принимает стадию. Без строки причины — отказ с дверью роли. Корень (проверен Lead): `derivable()` пропускает только `blocked_by_env:`, `handed_to_person:`, `probe_gap:`, а красный прогон даёт `product:<id>` (`acceptance.py:568-569`) — квитанции нет. Отсюда «not receipted» (`controller._code_review_problems`) и «no accepted controller stage» (`stage_done`); `window_shape_errors` требует `probe`. На 12586 все красные окна (1–3, 6–8) закрыты только словом; окно 4 — два красных UI-теста, три слова человека (`records/journal.jsonl` 196–199). `s5.md:117-128` и код говорят одно (F-21). Пробелы HF2-1 — вход (`gates-and-words/findings/20261025-krasnyj-test-bez-raspiski-okna.md`; t-1225; FR-34, FR-21, P21, AR-25, AR-28) | designer (тот же, что HF2-3) → critic на план → builder → critic | `scripts/window_record.py` (`derivable`, `receipt`), `scripts/acceptance.py` (`validate_window`), `scripts/contract.py` (`window_shape_errors`, `probe_gap`), `scripts/controller.py` (`_code_review_problems`), `scripts/stage_done.py`, их тесты, `changelog.d/` (`story_step.py` `finish` и `s5.md` — по F-21) | HF2-1, HF2-3 (тот же механизм), HF2-8 (EP1-16) | принято (сделано: b81b9499, релиз 0.10.2) |
| HF2-5 | П1 | Остаток GW1-14 после HF1-10 (`t-059-hf1-10.md`, п. 6). F7: `manifest_put` заменяет `then_bindings` целиком (E19 спеки t-052). A1: Then-уровня `deferred_by_decision:*` рядом с зелёным — тихий проход в `ledger.plan_row_state` и `report_facts._classify`. A2: `no-assert-` на любой записанный неразрешённый Then. Состав — F-12 (`gates-and-words/findings/20261022-odin-then-nelzya-otdat-cheloveku.md`; P13, P21, FR-4, FR-9, AR-22, AR-28) | designer (тот же, что HF2-3) → builder → critic | `scripts/manifest_put.py` (`_merge_entry`), `scripts/ledger.py` (`plan_row_state`), `scripts/report_facts.py` (`_classify`), `scripts/s5_precheck.py` (`check_bindings`), их тесты, `changelog.d/` | HF2-3 | принято (сделано: 3377cf7c, релиз 0.10.2) |
| HF2-6 | П1 | RD1-8: pass неисполненному тесту, «9 proven» рядом с «1 green», Q-4 отвечен и открыт. Статус теста — только из записи исполнения («не исполнен», если записи нет). Одна цифра «доказано». Статус вопроса — из носителя HF2-7. Сверка кодом, отказ называет расхождение. Первым ходом — сверка RD1-1 (F-16) (`report-delivery/findings/20261024-otchet-pokazyvaet-pass-neispolnennomu-testu.md`; t-1207 п.5; P21, FR-41, FR-59, AR-28) | designer → builder → critic | `scripts/check_delivery.py`, `scripts/report_facts.py` (уточняет спека), их тесты, `changelog.d/` | HF2-3, HF2-5, HF2-7; RD1-1 — F-16 | принято (сделано: b809fe66, релиз 0.10.2) |
| HF2-7 | П1 | GW1-21: ответы человека на вопросы S2/S3/S4 применяются сразу (слово владельца 24.10.2026). Один ход записи: `question_register` + `human_answer`. Бриф каждой следующей роли читает ответы из хранилища; устаревший `open halt` уходит; отвеченный вопрос остаётся `answered`. Блокирующий вопрос — стоп до зависимого артефакта, S4 в `where`. Поздний ответ — точечная доработка по `question_refs`. Новый вид ответа `deferred_to_report`. Один носитель статуса вопроса для гейта S3 и репетиции гейта A. Сопутствующее: чекпойнт S1, устаревший `input_hash` в `rework`, раунд критика `incomplete` (`gates-and-words/findings/20261024-otvety-cheloveka-ne-primenyayutsya-srazu.md`; t-1208, t-1209; FR-7, FR-8, FR-9, FR-59, AR-13, AR-14, AR-22, AR-24, AR-28) | designer → critic на план → builder → critic | `scripts/story_run.py` (`take_question_answer`, стоп вопросов), `scripts/question_register.py`, `scripts/question_stop.py`, `references/question-vocabulary.json`, `scripts/brief_pack.py` (`answers_of`), `scripts/planning_contract.py` (`apply_gate_answers`), `scripts/gate_brief.py`, `agents/qa-requirements-tester.md`, их тесты, `changelog.d/` | — (GW1-3, GW1-7 — после пачки) | принято (сделано: d6c391c7, релиз 0.10.2) |
| HF2-8 | П1 | EP1-16: мутационная проба строится с `profile_id` строки манифеста (`build_request` → `build_mine_request`; ветка `node_ids` профиль не теряет). Отказ без профиля называет дверь «строка манифеста», не `--profile`. Соседи: `red_sandbox`, `run_suite --mine`, `execution_request.py:1714`. На 12586 все пять проб окна 1 — `not_executed` (FB-4). У зелёного `probe is missing` здесь, у красного — HF2-4 (`execution-probes/findings/20261024-proba-mutacii-ne-peredaet-profil.md`; t-1220; FR-2, FR-17, AR-13) | designer (тот же, что HF2-10) → builder → critic | `scripts/probe_by_code.py` (`build_request`), `scripts/execution_request.py` (`build_mine_request`), `scripts/red_sandbox.py`, их тесты, `changelog.d/` | HF2-1; HF1-3, HF1-14 приняты | принято (сделано: 324ebdda, релиз 0.10.2) |
| HF2-9 | П1 | CD1-14: замер. Вызовы вдвое медленнее (shell 4,4 → 10,4 с); подозревается `cost_capture`. Сначала тот же сценарий с выключенным хуком, медианы до и после. Если подтвердится: один экземпляр, дебаунс, Stop не держит ход; цена истинная (P18) (`cost-dashboard/findings/20261025-cost-capture-zamedlyaet-vyzovy.md`; t-1221; P11, P18, FR-28, FR-55) | builder (замер) → designer → builder → critic | `scripts/cost_capture.py`, `scripts/telemetry_hook.py`, `hooks/hooks.json`, их тесты, `changelog.d/` | — (CD1-13 — F-2) | принято (сделано: 291a34f9, релиз 0.10.2) |
| HF2-10 | П1 | EP1-17: запуск теста без 20 минут обвязки. Один collect на запрос; явный `--node-id` при существующем файле — без collect; неразобранный collect проверяет сам запуск; одна проба рантайма; отказ «нет `runtime_probes`» — до collect (`execution-probes/findings/20261025-s5-zapusk-testa-20-minut-obvyazki.md` §1; t-1221; P11, FR-51, FR-55, AR-12) | designer (тот же, что HF2-8) → builder → critic | `scripts/run_suite.py` (`collect`, `verify_node_ids`, `probe_runtime`), `scripts/execution_request.py` (`build_mine_request`, `_spell_as_collected`), их тесты, `changelog.d/` | HF2-8, HF2-9 | принято (сделано: baa1bb3d, релиз 0.10.2) |
| HF2-11 | П2 | EP1-15: если исполняемая часть теста или фикстуры изменилась после последнего прогона, фабрика сама перепрогоняет тест и red-probe до отчёта (при доступном стенде). Человеку — только по P19 ступени 5. Косметика перепрогона не требует, переименование требует (`execution-probes/findings/20261024-net-finalnogo-progona-finalnyh-fajlov.md`; t-1207 п.6; P19, FR-33, AR-25) | designer → builder → critic | `scripts/acceptance.py`, `scripts/window_record.py`, `scripts/proof_level.py` (уточняет спека), их тесты, `changelog.d/` | HF2-3, HF2-4, HF2-12 | принято (сделано: 252fd038, релиз 0.10.2) |
| HF2-12 | П1 | EP1-18 (а): обязательные поля строки манифеста (`assertion_id`, `defect_location`, `change_disposition`, `change_basis_ref`, `profile_id`, поля HF2-3) роль получает до работы: в форме строки и от `manifest_from_tests`. `s5_precheck` перечисляет недостающие одним списком; один носитель — `window_record`; роль автоматора называет поля. Бриф окна — HF2-17 (находка §2; FR-38, FR-13, AR-10) | designer → builder → critic | `scripts/window_record.py`, `scripts/manifest_from_tests.py`, `scripts/s5_precheck.py`, `agents/qa-automator.md`, их тесты, `changelog.d/` | HF2-8, HF2-3, HF2-4 | принято (сделано: ca5c4552, релиз 0.10.2) |
| HF2-13 | П2 | TQ1-13: второй `select_project` и `wait_for_page_load`; одна фикстура дважды в conftest окна. Волна 1 — строка критика кода (K16). Тропа `introduced_helpers[]` — с TQ1-7 (F-4) (`test-code-quality/findings/20261024-vtoroj-heljper-ryadom-s-sushchestvuyushchim-i-dubli-fikstur.md`; P12, AR-15) | builder → critic | `scripts/manifest_from_tests.py` (по F-4 — с TQ1-7), `agents/qa-code-critic.md` (как TQ1-7), `changelog.d/` | HF2-3; TQ1-7 — F-4 | принято (сделано: cf5a8401, релиз 0.10.2) |
| HF2-14 | П3 | TQ1-14: строка «проверка количества — assert до распаковки» (P16) и вопрос критику «уровень теста совпадает с планом S3 или отклонение названо»; в волне 2 вопрос уходит в ПЛАН (K6) (`test-code-quality/findings/20261024-krasnaya-stroka-raspakovka-do-assert-i-e2e-dlya-klientskih.md`; P16, P19) | builder (спека Lead ≤ 3 пунктов) | `references/test-code-patterns.md` (+ slices — generated), `references/code-review-rubric.md`, `agents/qa-code-critic.md`, `changelog.d/` | HF2-13; TQ1-3 — после пачки | принято (сделано: cf5a8401, релиз 0.10.2) |
| HF2-15 | П2 | TQ1-12: тест отказа проходит на чужом 400 (TC-008); сравнение маски `'******'` с `'******'`. Правило «тест отказа различает причину; маска — не проверка сохранности» — строками рубрики dim 2; образцы в корпус — с TQ1-4 (F-3) (`test-code-quality/findings/20261024-otkaz-ne-razlichaet-prichinu-i-sravnenie-po-maske.md`; P20, FR-18) | builder → critic | строки rubric dim 2 (`references/code-review-rubric.md`); корпус `evals/seeded-defects/**` (new) — по F-3; `changelog.d/` | HF2-14; TQ1-4 — F-3 | принято (сделано: cf5a8401, релиз 0.10.2) |
| HF2-16 | П1 | **Волна 2.** DC1-9: цикл окна S5 без 25 минут управления. Форма S5 (слово владельца 25.10.2026): один план автотестов на все кейсы, один критик на весь план, без блокеров план не переписывается, окна получают требования, план и замечания. Критик после кода проверяет тесты и соответствие плану (блокер в плане — F-8). Деление ПЛАН/КОД/ОБА и C1–C15 (`t-1222`). `bind` внутри `start`; без `pause` между возвратами; форму дайджеста чинит код; возобновлённой роли — дельта; медианы — после HF2-9 (`driver-controller/findings/20261025-cikl-okna-s5-25-minut-upravleniya.md`; t-1221, t-1222; P3, P11, FR-55, AR-12) | designer → critic на план → builder → critic | `scripts/story_step.py`, `scripts/controller.py`, `scripts/exit_gate.py` (`digest`), `scripts/brief_pack.py`, `skills/qa-story/phases/s5.md`, `agents/qa-automator.md`, `agents/qa-code-critic.md`, `references/code-review-rubric.md`, `handoffs/s5-*.yaml` (+ передача плана S5 (new), `handoffs/index.yaml`, `references/stages.json`), `scripts/manifest_from_tests.py`, `scripts/s5_precheck.py`, их тесты, `changelog.d/` | шлюз волны 2; HF2-9; волна 1 принята | принято: 7cc092de |
| HF2-17 | П1 | **Волна 2.** EP1-18 (б): бриф окна S5 даёт роли файлы и фикстуры кейсов окна и образцы соседних тестов (было 112 вызовов чтения, 12,7 мин) — вместе с планом и замечаниями HF2-16; цель ≈ 22 мин (FR-38, AR-10) | designer (тот же, что HF2-16) → builder → critic | `scripts/brief_pack.py`, `skills/qa-story/phases/s5.md`, `agents/qa-automator.md`, их тесты, `changelog.d/` | HF2-16 | принято: cf511c8e |
| HF2-18 | П1 | **Волна 2.** TQ1-15: S7 ставит контрольный опыт до вердикта `APP_BUG` на «лишнее/иное значение»: то же действие без проверяемого изменения (на 12586 — сохранить интеграцию без смены проекта); эффект и без изменения → вывод триажа „ассерт строже требования“, БЕЗ возврата на гейт A и без переписывания кейса: строка в «Left with you» отчёта — человек решает, удалить ассерт или уточнить требование (слово владельца 25.10.2026); сид слабее Given кейса → `TEST_BUG` данных; «обе трактовки → `APP_BUG`» только после опыта; критик кода спрашивает «ассерт строже требования». Слово владельца 25.10.2026: «если нет, то это надо исправить во второй волне срочной пачки» (`test-code-quality/findings/20261025-s7-ne-stavit-kontrolnyj-opyt.md`; скаут t-1226; P20, FR-22, FR-26, FR-58) | designer → builder → critic | `agents/qa-failure-analyst.md`, `skills/qa-story/phases/s7.md`, `references/code-review-rubric.md`, `agents/qa-code-critic.md`, `references/delivery-verdict-kinds.json`, эвалы роли S7 | HF2-16 (DC1-9: рубрика и критик), HF2-4 (GW1-23) | принято: b515fcca |

После пачки — не узлы:
- GW1-3, GW1-7;
- остаток EP1-10 (F-6);
- EP1-11, EP1-12, EP1-14, EP1-4;
- F8 из отчёта t-059;
- CD1-13;
- TQ1-3, TQ1-4, TQ1-7;
- RD1-1, RD1-2, RD1-4, RD1-7;
- GW1-9, GW1-10;
- TQ1-10;
- RC1-1;
- пробелы свипа вне узлов (F-17): не блокирующие идут в волну 2 этой пачки; блокирующие прохождение стори — сразу новым узлом волны 1
  (слово владельца 25.10.2026).

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 25.10 01:45 — пачка собрана Lead из двенадцати узлов шести кучек по слову владельца 25.10.2026 (CD1-13 и TQ1-11 не входят), связки A–E —
  Lead. Сверх списка: EP1-13 и остаток GW1-14 (та же функция); GW1-23 и свип HF2-1 — по словам владельца. DC1-9 и бриф окна EP1-18 —
  волна 2. Черновик t-1224. Развилки закрыты словом владельца «Остальное по рекомендациям» (раздел «Решения владельца»); F-17 — по слову
  владельца: пробел свипа во вторую волну, блокирующий — сразу узлом волны 1. Волна 2 пополнена узлом HF2-18 (TQ1-15, находка S7 без
  контрольного опыта, слово владельца 25.10.2026): всего 19 узлов. Помещено в кучки t-1227.
- (правило) Перед первым диспатчем волны 2 (HF2-16, HF2-17, HF2-18) взявший спрашивает владельца: «делаем вторую волну или не успеваем и
  делаем релиз без неё». Ответ записывается следующей строкой. Без волны 2 релиз режется из волны 1 после её BATCH CANON и HF2-0, а HF2-16,
  HF2-17 и HF2-18 остаются «ожидает» (закрытие — F-19 (б)).
- 25.10 20:3x — пачка взята (dev2; worktree `C:\Projects\wt-hotfix-12586-b2`, ветка `pile/hotfix-12586/batch-2` от `origin/main` 6eee515e).
  Шлюз между волнами закрыт заранее словом владельца 25.10.2026 (вечер): «без волны 2» — волну 1 завершить и выпустить как можно скорее
  (при необходимости ночью), релиз после обязательной валидации; HF2-16, HF2-17, HF2-18 НЕ реализуются и по F-19 (б) переносятся в пачку 3
  строкой «Остатков» с подтверждением человека. Строки очереди `kb/1 → hotfix-12586/2` (общая папка `docs/tasks/specs/reports/`) и
  `conductor/1 → hotfix-12586/2` дописаны в обе пачки по отказу `take`.
- 25.10 22:5x — первая волна диспатчей: t-079 скаут HF2-1 (свип класса), t-080 билдер-замерщик HF2-9 (стенда на этой машине нет —
  локальное воспроизведение нагрузки `cost_capture` с носителями), t-081 дизайнер HF2-7, t-082 дизайнер HF2-8+HF2-10 (F-15). Спеки Lead:
  `docs/tasks/specs/t-083-hf2-2.md` (HF2-2; `dispatch_skipped` designer — находка EP1-13 уже несёт проект), `docs/tasks/specs/t-084-hf2-13-14-15.md`
  (HF2-13…15 одним билдером). Решила сама: HF2-13…15 идут ДО билдера HF2-3 на общих `code-review-rubric.md`/`qa-code-critic.md` (разные
  измерения: 2 и 5 против 6 и 8; критический путь свободен; дизайнер A получает t-084 в given, E6 — одна формулировка «закомментированный Then»
  остаётся за HF2-3); таблица «Порядок по общим файлам» заморожена, отклонение записано здесь.
- 25.10 23:1x — HF2-1 принят (t-079, дайджест `docs/tasks/specs/reports/t-079-hf2-1-red-default-sweep.md`: пробелы разложены по HF2-3/HF2-4/HF2-8,
  вне узлов — только аналоги A1–A5, ни один не блокирует прохождение; F-20: `probe_by_code` зелёного базиса не требует). Черновики дизайнеров
  приняты (t-081 → `docs/tasks/specs/t-081-hf2-7.md`, t-082 → `t-082-hf2-8-10.md`; роль без Write — файлит Lead); развилки решены Lead по
  рекомендациям («решила сама», §9 / «Решения Lead»). Запущены: t-083 дизайнер A (HF2-3/4/5), t-084 билдер HF2-8 Part A (worktree
  `C:\Projects\wt-hf2-8`, ветка `wt/hf2-8`), t-085 критик на план HF2-7 (в текстах диспатчей и имени отчёта билдера — t-085/086/087:
  журнал требует max+1, а имена спек Lead `t-083-hf2-2.md`, `t-084-hf2-13-14-15.md` были даны до выдачи id; имена файлов сохранены). Открытые пункты живого прогона (владелец): замер F-2 над файлом слов
  12586 (`parse_choices`), сырой вывод collect при отказе `unread`.
- 25.10 23:4x — критик на план HF2-7 (t-085, `docs/tasks/specs/reviews/t-085-hf2-7-plan-review.md`): FIX — блокеры B1 (тупик роли на выходе S2:
  `check_witness.py:152-163` против нового правила), B2 (остановка S2–S4 не показывает форму ответа — строгая грамматика ничего не запишет),
  M1–M7, m1–m7; решения Lead по фиксам — в файле вердикта; ревизия — свежий дизайнер t-086, затем второй проход критика по изменённым
  разделам. Дизайнер A сдал спеку HF2-3/4/5 (t-083, `docs/tasks/specs/t-085-hf2-3-4-5.md`, 7 билдерских частей 3a/3b/3c/3d/4a/4b/5a); 15
  технических развилок решены Lead (§11), ДВЕ — владельца: FA-10 (красный по багу Then не комментируется, ставится последним; комментарий —
  только для красного из-за среды и Then за красным) и FA-11 (зелёный Then до красного assert — «не доказан: тест остановился на Then n»);
  вопрос поднят оператору. Критик на план HF2-3/4/5 — t-087. Порядок на `exit_gate.py`: HF2-2 → HF2-7 (по F-3 (а) ревизии HF2-7).
  Worktree `C:\Projects\wt-hf2-2` (ветка `wt/hf2-2`) готов для билдера HF2-2 — ждёт слота (гейт параллели).
- 26.10 00:0x — **HF2-8 Part A принят и слит** (t-084, коммит `31679e29` на `wt/hf2-8`, слияние `324ebdda`; свидетель — шесть файлов DoD зелёные;
  критик — в проходе HF2-0 по волне, R13-g). Критик на план HF2-3/4/5 (t-087, `docs/tasks/specs/reviews/t-087-hf2-3-4-5-plan-review.md`): FIX —
  F1 (D1 (iv) отказывает форме «Then до красного»), F2 («ноль слов» только для первого красного окна), F3 (у роли нет писателя новых полей строки:
  маркер не умеет `instance_ids`/`thens`/`blocking_check` → дверь `manifest_put --fragment`, ключи маркера — HF2-12), F4 (отказ внутри `merge` ломает
  воспроизведение событий), F5–F16; решения Lead — в вердикте; ревизия — свежий дизайнер t-089. Критик про развилки владельца: FA-11 (б) противоречит
  цели слова «перенести ДО упавшего — тогда мы будем знать результат», (а) держит слово, но исполнимость `reporters.failure_site` не проверена;
  FA-10 (а) сужает слово владельца («решает автор»), цена (б): закомментированный красный по багу теряет красный тест и `failed:*`. HF2-7 rev. 2
  (t-086) принята как черновик: B1 — один предикат `QR.open_blocker`, B2 — остановка S2–S4 показывает блок «How to answer»; новые развилки F-11 (а,
  точечная доработка кодом), F-12 (а), F-13 (а) решены Lead; второй проход критика t-090. Билдер HF2-2 запущен (t-088, `wt/hf2-2`). Замер HF2-9
  (t-080) идёт: M1–M4 выводы в скретче, отчёт ещё не сдан. Worktree `C:\Projects\wt-hf2-10` (от `324ebdda`) готов для Part B HF2-10.
- 26.10 00:1x — **HF2-9 замер принят** (t-080, `docs/tasks/handoffs/t-080-hf2-9-cost-capture-measure.md`): локально механизм подтверждён — K=4 параллельных
  `cost_capture` замедляют вызов ×1.4–2.35, K=8 ×2.5; перерисовка дашборда после замка — 26–42 с из 44–67 с хука; дебаунс = замок сессии + окно 30 с без
  очереди; замок на сессию. Для стенда — неокончательно: живой пункт владельца — шаг 1 находки на стенде с выключенным `cost_capture`. Дизайнер починки —
  t-092. **HF2-2 принят и слит** (t-088, `62dc40a7` → `e07c6f7b`): `contract.then_number`, `THEN_REMAINDER_*` — один носитель; четвёртые читатели номера
  Then переданы узлам: `manifest_from_tests.py:956` → HF2-12, `report_facts.py:531` → HF2-5/HF2-6, литерал `then-remainder-all` в `s5_precheck.py:1006` → HF2-3.
  Билдер HF2-10 Part B — t-091 (`wt-hf2-10`).
- 26.10 00:4x — спеки готовы к билдерам. HF2-7: rev. 2 (t-086) → второй критик t-090 «fix» (N1 `complete=True` закрывал S4 без критика, N2
  `settled_question` для кейса с ветвлением, N3 изменённая строка читалась решённой, N4 `not_checked` в errors, N5–N13) → rev. 3 (t-093) принята;
  билдер P1 — t-097 (`wt-hf2-7-p1`), далее P2 → (P3 ∥ P4), P5b параллельно, P5a последней (BATCH CANON). Спека A: rev. 2 (t-089) → второй критик
  t-094 «fix» (N1 High: один инстанс красный по строкам двух кейсов — D1 берёт первую строку, баг TC-004 приписывался бы TC-005; N2–N11) → rev. 3
  пишет t-096. FA-11 (а) подтверждена дешёвой: композиция `bind_row` + `read_rows` + `assertion_site`, запасной (б). HF2-9: спека починки t-092
  принята (F-1…F-8 по рекомендациям), билдер t-095 (`wt-hf2-9`); **эксперимент X0 Lead провести не смог** — `claude -p` отказал («OAuth session
  expired»), X0 — пункт владельца; F-2 (а) от исхода X0 не зависит (маркер `started` + догон). Четвёртые читатели номера Then (t-088) учтены в rev. 3 A.
- 26.10 01:5x — **слиты**: HF2-10 Part B (t-091, `adcf835f` → `baa1bb3d`; один collect и одна проба рантайма на `--mine`), HF2-7 P1 (t-097, `3626e86a` →
  `01852f5b`), HF2-3 часть 3a1 (t-099, `9cc9f72a` → `bff2ee3f`; две интеграционные правки Lead `e89ab270`: `blocked_by_check` в `handoffs/vocabulary.yaml`,
  исключение из `judge_form.UNRESOLVED_OPTIONS`; `plans/features.json` приписывает новые тестовые файлы пачки F08/F17), HF2-7 P2 (t-100, `30eacae5` →
  `e98f9e74`), HF2-13/14/15 (t-098, четыре попытки: храповики запаса A22/A25 — каталог паттернов инжектируется только автоматору, 363 Б избыточных
  слов срезаны с именованием каждого; эскалация к Lead по правилу 6 записана; `27a3e697` → `cf5a8401`). HF2-9 (t-095): раунд 1 `e06d9fc0` — замер
  ×4.24 → ×1.44, запусков 492 → 151; K13 подтвердил F-7 (SubagentStop под Claude пишет файл родителя по файлу подагента — P18) → фикс-раунд чинит.
  Спека A rev. 3 (t-096) принята; 3b (t-101) в работе. HF2-7: P3 (t-102), P4 (t-103) в работе; далее P5b, P5a. X0 Lead провести не смог (CLI без авторизации).
- 26.10 02:4x — **слиты**: HF2-9 (t-095, `e06d9fc0`+`b4517f67` → `291a34f9`; F-7 починен: SubagentStop не занижает файл родителя), HF2-3 3b (t-101,
  `c3b7e577` → `d25e5320`), HF2-7 P3 (t-102, `c3b1fbb9` → `93e260c4`), P4 (t-103, `54f133ff` → `facd04ec`), P5b (t-104, `f8f110e1` → `27697f47`),
  HF2-3 3a2 (t-105, `2d6ee6cf`; слияние — после приписки `test_mixed_then_precheck.py` фиче F08). В работе: 4a (t-106), дизайнер HF2-12 (t-107),
  P5a (t-108, последняя часть HF2-7), 3c1 (t-109). **Решила сама (развилки владельца FA-10/FA-11 без ответа ~5 часов):** 3c1/3c2/3d идут в
  нейтральной форме — чтение FA-11 (б) «не доказан» (строгое подмножество варианта (а), его запасной путь) и тексты без фразы FA-10 (N4:
  `THEN_REMAINDER_REASONS`, комментировать красный по багу не санкционировано); слово владельца добавит читатель места падения (3c1 `red_failure_line`)
  и фразу FA-10 (3d-K2a/K2b) отдельными подключами. Ничего не решено за владельца: оба варианта остаются открытыми.
- 26.10 04:0x — **слиты**: HF2-4 4a (t-106, `724a82ea` → `99026389`), HF2-3 3c1 (t-109, `fb83df3a` → `e8194ba3`; FA-11 (б)), HF2-7 P5a (t-108,
  `91c5c177` → `d6c391c7`; HF2-7 собран целиком P1–P5), HF2-3 3d (t-111, `c8ed0765` → `4c09ff44`; K2a/K2b/K3a не писались), HF2-3 3c2 (t-113,
  `870f0635` → `c683969e`). Спека HF2-12 (t-107 → `docs/tasks/specs/t-107-hf2-12.md`, развилки F-1…F-9 по рекомендациям) прошла критика на план
  (t-110, `docs/tasks/specs/reviews/t-110-hf2-12-plan-review.md`: «принять с правками», 11 правок → §12 спеки; главное: `obligation_refs`
  требуется только там, где план несёт обязательство, иначе ловушка C3/FR-57). Отклонение от «Порядка по общим файлам» (`s5_precheck.py`:
  таблица HF2-5 → HF2-12): функции не пересекаются, 12a/12b идут параллельно 5a — решила сама. В работе: 12a (t-112), 5a (t-114), 4b (t-115),
  скаут RD1-1 для HF2-6 (t-116). Находка пачки 3: `findings/20261026-h41-izmenyonnyj-otvet-ne-otkryvaet-dorabotku.md` (P5a). В интеграционную
  пачку мелочей (один билдер после слияния волны): SKILL.md строка таблицы остановок (P5b); `s5.md:203-204` текст F-X1 (HF2-10) и фраза HF2-12 §6;
  `qa-automator.md:106`, `qa-code-critic.md:89` F-X1; `acceptance.py:528-529` фраза «marker cannot write»; списки причин `state-exits.md:124,126`,
  `driver.md:204` (+ `question_answer`); текст T3 без двойного id (3c1 ↔ 3c2); сужение `to_check` blocked-пунктов (`build_left_items`, пропуск
  диспатча 3c1); абзац 3d-K5 → `artifact-contract-automation.md` и `vocabularies.md:45-53` (+ `blocked_by_check`); оси SIBLING_MAP. Для HF2-0:
  два истончённых долга 3d (абзац карантина у критика, «half-automated case reads as complete»).
- 26.10 05:1x — **слиты**: HF2-5 5a (t-114, `9de2b7a6` → `3377cf7c`), HF2-12 12a (t-112, `a623ab7f` → `9fbccbe9`; `test_row_fields.py` приписан F08),
  HF2-4 4b (t-115, `b6b58889` → `b81b9499`; HF2-4 закрыт), фикс-раунд t-119 (`ffb1e947` → `7177ffab`: коллатераль 3c1 — литерал `blocked_by_check`
  в `check_delivery.py` и ключ E7 (`defect_found` t-109); коллатераль 5a — контрольное слово K3, перемер A16/A18 по единице). Скаут RD1-1 (t-116,
  `docs/tasks/specs/reports/t-116-rd1-1-reconciliation.md`): факт (1) RD1-8 на ветке открыт (`traceability.py:533-555`), B-303/B-266 сделаны,
  B-308 (а) — только для красных строк. Спека HF2-6 (t-117 → `docs/tasks/specs/t-117-hf2-6.md`) прошла критика (t-118, «принять с правками», 9
  правок → §11; развилка 1 решена Lead: общий шаг «легаси» в `run_row_for`). Спека HF2-11 (t-120 → `docs/tasks/specs/t-120-hf2-11.md`): решения
  Lead — F-0 (б) (замер 11-0 над архивом 12586 — пункт владельца, архива на машине нет; 11b строится на названном предположении), F-8 — пачка 3;
  критик на план t-123. **Отклонения от замороженной таблицы (решила сама):** owns HF2-6 расширены на `traceability.py`, `case_stamp.py`,
  `ledger.py` и их тесты (F-1 (а): иначе второе соединение); свидетель HF2-6 = DoD частей; очереди `HF2-7 → HF2-11` (`story_run.py`),
  `HF2-6 → HF2-11` (`ledger.py`), `HF2-3 → HF2-11` (`delivery-verdict-kinds.json`). В работе: 12b (t-121), 6a (t-122), критик HF2-11 (t-123).
  В интеграционную пачку мелочей дополнительно: `test_probe_gap_word.py` K16 (кортеж `DERIVED_GAP_KINDS` + `contradicts_requirement`, 4b);
  `acceptance.py:528-529` фраза; `expected_product_failure` (rollup красный ↔ трасса `not run`, ось FR-10). Находки пачки 3 (пишет Lead при
  интеграции): три читателя «green без строки» чинятся вместе (F-3 (б) HF2-6: `case_stamp:263`, `check_coverage:136`, `lifecycle_reasons`);
  снятие (`retracted_unresolved`) не снимает Then-строки снятого id, строка-призрак скрывает `unlinked-` (t-119 п. 4); `same_instance_bytes` ↔
  `same_test` (AR-13) и читатель `proof_stale` без писателя (AR-22) (HF2-11 противоречия 3, 5); правка после S6 (HF2-11 F-8).
- 26.10 10:5x — **слово владельца 26.10.2026** (через оператора, по обзору отложенного `docs/tasks/specs/reports/t-135-deferred-review-for-owner.md`):
  «всё, что релиз не блокирует, откладываем на после релиза; релиз нужен максимально быстро; даже длинные тесты в этот раз можно прогнать
  после публикации релиза». Следствия: канон часть 1 (`test_story_run_*`, t-132) не держит релиз — его красные чинятся после публикации;
  критический путь — фикс-раунд 4 (t-134, красные канона части 2 и докера) → HF2-0 → релиз. Вопрос владельца про `build_left_items` для
  смешанных видов: это строка «Left with you» для кейса, у которого есть и Then за красным (`blocked_by_check`), и другой вид (handed/не исполнен);
  сужение `to_check` до заблокированных Then сделано интеграцией только для кейса одного вида, смешанный остался со списком всех Then — объём
  волны 1 (HF2-3), выпал из диспатча 3c1 (пропуск диспетчера 05:1x) и не был описан спекой A §3.4; чинится отдельным малым фиксом t-135
  (в тексте диспатча и имени хендоффа — t-136) параллельно фикс-раунду 4, релиз не задерживает.
- 26.10 11:1x — **слово владельца 26.10.2026 «MR не проблема, делай»**: открыт Draft MR ветки пачки в `main`
  `https://git.example.com/dev1/yml-text-factory/-/merge_requests/4` — для `package-fast` и `forge-check` в CI (правила
  `.gitlab-ci.yml`: только MR или `main`); Draft до вердикта HF2-0, сливает интегратор при зелёном CI и принятом критике (PROJECT.md,
  «Командная работа» п. 1). API-пайплайн 7974195 (`package-full`) на `a80124f0` — красный по файлам, которые чинит фикс-раунд 4.
- 26.10 11:5x — **слово владельца 26.10.2026 (приоритеты)**: (1) закончить срочный релиз волны 1 — Маша сливает MR !4 и делает релиз по моему
  подтверждению готовности; релиз не задерживать ни работой по КБ, ни неблокирующими длинными тестами; (2) после релиза — пачки `kb/1` и
  `kb/2` против опубликованной версии (KB1-1…3, KB2-1, KB2-3 приняты и слиты; KB1-4 — только три схемы `diagram-pipeline-s0-s9`,
  `diagram-three-layers`, `diagram-route-spine` сверить с архитектурой; пример отчёта и скрины дашборда не переделывать; KB2-4 — релизная
  документация под финальную версию с коллектором; KB1-5 и KB2-2 — публикация семи существующих страниц после KB2-4 и KB1-4, без дублей;
  публикация по решению Маши 21.10: мелкое — сразу, существенное — показать; `KB_PAT` владельца по RUNBOOK §3a ещё не настроен). Пайплайн MR
  !4 на `269b69dd`: `forge-check` красный по lint-храповику (21), `package-fast` 299/306 (семь файлов) — объём фикс-раунда 4.
- 26.10 13:0x — **состояние перед компактом.** Слиты фикс-раунды 4 (`5226a729`: lint 0 новых, пины по принятым узлам, две фикстуры), 5
  (`b56a36c1`: `to_check` смешанных видов — вопрос владельца), 6 (`08d7e775`: маршрут `controller-blocks` для StateConflict 4b), 7
  (`c669fc46`: заголовок `## Бриф` файла пачки 3 и строки «Содержания» карточки); карточка: папка `findings/` есть (`9ce17fe6`). Пайплайн MR !4
  на `265cefe0`: `package-fast` ЗЕЛЁНЫЙ, `forge-check` красный только по двум piles-тестам (починены раундом 7); пайплайн 7976171 на
  `9ce17fe6` запущен — ожидается зелёный. `test_stand_lease` красный на `main` 6eee515e (не наше). Слово владельца 26.10: **версия релиза
  0.10.2**. В работе: критик волны HF2-0 (t-138) по диффу 6eee515e..08d7e775 (без фикс-раунда 7 и правки карточки — только docs/plans);
  прогонщик канона части 1 (t-132, длинные `test_story_run_*`; промежуточный список красных запрошен); билдер КБ (t-140, worktree
  `C:\Projects\wt-kb-final`, ветка `wt/kb-final`: KB1-4 три схемы + KB2-4 семь страниц под 0.10.2 по дайджесту скаута t-137
  `docs/tasks/specs/reports/t-137-kb-pages-vs-release.md`). Дальше: вердикт HF2-0 → подтверждение готовности Маше (MR !4 сливает она) →
  публикация КБ (`kb_publish.py diff` по страницам; мелкое — `push --yes --expect-version`, существенное — показать Маше) → «Остатки»
  (три строки переноса ждут `подтвердил:` человека) → канон часть 1 после публикации релиза. Пункты владельца без ответа: FA-10/FA-11, X0,
  замер 11-0.
- 26.10 15:1x — **вердикт HF2-0 и фикс-раунд 9.** Критик t-138 (`reviews/t-138-hf2-wave1-review.md`): `fit_with_fixes`, блокеров слияния нет;
  асимметрия красного/зелёного/неисполненного доказана, `blocked_by_check` одно написание, формулировка «закомментированный Then» одна;
  R1–R3 (пустая строка «Left with you» в форме B, безусловный хвост «its other Thens passed», реклама перепробы S6 в changelog) — фикс-раунд 9
  (t-142, свежий билдер), слит `9850a116`: 189/189, 508/508, 328/328, 287/287, мутации приложены, критик пропущен (рецепт вердикта, 45 строк кода).
  Список «после релиза» — находка `findings/20261026-hf2-0-posle-reliza-dolg-kachestva.md`, строка HF3-11. **Канон часть 1 (t-132) остановлен
  Lead в 14:46 по слову владельца** (30 файлов за 6,5 ч: 21 зелёный, 3 красных, 6 по капу; таблица в `handoffs/t-132-canon-part1.md`); остаток
  списка после релиза; слово владельца 14:5x «канон — в CI, прогон сократить» — находка `findings/20261026-kanon-vetki-v-ci-i-koroche.md`, строка
  HF3-12. Фикс-раунд 8 (t-141) идёт: три красных закрыты пинами тестов (кода пакета нет), таймауты перегоняются по одному (`no_move_seam` живой,
  исполняет стадии — нагрузка, не зависание). **КБ опубликована** токеном владельца 14:3x: три PNG, семь страниц (01 v14, 02 v9, 03 v12, 04 v6,
  05 v6, 06 v8, 07 v14), `status` 7/7 equal; записи — «Ход» kb/1 и kb/2, ветка `wt/kb-final` (`ef93a60f`+). Пайплайн MR !4: `c0995feb` зелёный,
  `8837271c` (голова) запущен 7977234. Слово владельца 15:0x: готовность Маше подтверждать по зелёному пайплайну на голове, фикс-раунд 8 — следом.
  Сборка релиза (для Маши): `plugin.json` 0.10.1 → 0.10.2, `changelog_assemble.py --version 0.10.2`, 29 фрагментов `changelog.d/`; `INSTALL.md:3`,
  `README.md:3` держат 0.9.0, `release-fingerprint.json` 0.10.0; `selftest --hygiene`, `install_smoke` — по PROJECT.md «Релиз».
- 26.10 15:1x–18:0x — **готовность подтверждена, фикс-раунд 8 слит.** Пайплайн 7977234 на `8837271c` зелёный (`package-fast`, `forge-check`,
  `runner-facts`); записка Маше `docs/tasks/specs/reports/20261026-release-0.10.2-readiness.md`; слово владельца 15:0x — подтверждать по
  пайплайну, раунд 8 следом. Фикс-раунд 8 (t-141, `b841ead8`, слит `--no-ff`): три красных канона — пины принятых узлов (строки слоёв 11b,
  строка переписи K15 для `questions.blocking` P5a, перевставка приложения 6b в K-N8.7), кода пакета нет; шесть таймаутов поодиночке — нагрузка,
  не зависание и не регрессия волны (`no_move_seam` 881/881, `gate_repair` 508/508, `infra_failure` 307/307, `s7_live` 44/44, `stand_identity`
  394/397 — три K39 по `Rig(timeout=2)` под нагрузкой); `test_story_step` один не укладывается в 30 мин — цена обновления дашборда после коммита
  контроллера (601/601 за 7 мин 39 с без обновления, диагностика) → факты дописаны в находку HF3-12. Раунд 8 — отдельным Draft MR
  (MR !4 к этому часу уже слит, см. следующую запись).
- 26.10 15:2x — **MR !4 слит и 0.10.2 выпущен** (Маша, по записке готовности `docs/tasks/specs/reports/20261026-release-0.10.2-readiness.md`):
  merge `c56bff44` в `main` (пайплайн MR 7977234 зелёный; конфликты — строка взявшего kb/1 и `PILES.md`, пересобран), релизный коммит
  `f8902ef5` (CHANGELOG 0.10.2 из 30 фрагментов — 29 + фикс-раунд 9; версии в трёх plugin.json, как в 0.10.1; `INSTALL.md`, `README.md`,
  `SKILL.md` по-прежнему 0.9.0). Релизная копия — `QAFactory` `feat/qa-factory` `e4f5adf1` (Draft MR !137): `--hygiene --lang` 3/3,
  `install_smoke` PASSED, отпечаток переписан под 0.10.2, `--check` ok (420 файлов). Записка готовности слита вторым merge. Дальше: фикс-раунд 8
  маленьким MR, «Остатки» (`подтвердил:`), `close hotfix-12586 2`, канон часть 1.
- 26.10 18:2x — `main` слит обратно в ветку пачки (`80c29d24`, конфликт только в этом «Ходе» — обе записи оставлены); хвост после релиза
  (фикс-раунд 8 `b841ead8`/`1c6d2141`, журнал t-138…t-142, факты в находке HF3-12, записи «Хода») — **Draft MR !5**
  (https://git.example.com/dev1/yml-text-factory/-/merge_requests/5), сливает Маша. Открыто: «Остатки» (`подтвердил:` человека),
  `close hotfix-12586 2`, остаток канона части 1 (после релиза, HF3-12), решения владельца HF3-6 / FA-10-11 / X0 / 11-0, ссылка на образец на КБ 03.
- 30.10.2026: статусы узлов проставлены по git (слово владельца, сессия dev1; пачка недоделана соседней сессией), t-1615. HF2-1…HF2-15 — `принято (сделано:
  <хэш слияния в main> (релиз 0.10.2)`, слияние ветки пачки `c56bff44`, релиз 0.10.2 (аудит t-1611 подтверждает). HF2-0: проход по волне 1 сделан
  (вердикт t-138, фикс-раунд 9 `9850a116`), прохода по волне 2 нет — статус не меняется. HF2-16 и HF2-17 ушли в `speed-cost/1` (SC1-14, SC1-15),
  HF2-18 — в пачку `hotfix-12586/3` (часть B слита `b515fcca`, на `main`); их строки здесь остаются «ожидает», перенос ждёт `подтвердил:`.
  «Живые доказательства» остаются «ожидает»: живого прогона на стенде в git нет.
- 01.11 — закрыта по слову владельца 01.11.2026 (пересборка бэклога): открытых узлов нет

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|
| Волна 1, повтор S5 TP1-12586 на копии `testproject1-dev-010`: каждое окно с красными по требованию тестами закрыто своей квитанцией, слов человека — ноль (блоков `not receipted`, `no accepted controller stage`, `probe is missing` нет); проба мутации исполнена при двух профилях (FB-4); один collect на `--mine`; ни одного возврата по полям строки; стена S5 напечатана с объёмом — промежуточная цифра, без DC1-9 | `testproject1-dev-010` / testproject1-sdk | владелец | перенос: live-runs/2 «Живые доказательства» \| обоснование: пересборка бэклога \| подтвердил: владелец, 01.11.2026 (слово 2 пересборки) |
| Волна 1: медианы вызовов до и после HF2-9; цена из двух источников сходится или печатается диапазоном (P18) | `testproject1-dev-010` / testproject1-sdk | владелец | перенос: live-runs/2 «Живые доказательства» \| обоснование: пересборка бэклога \| подтвердил: владелец, 01.11.2026 (слово 2 пересборки) |
| Волна 1: TC-005/TC-006 записаны смесью исходов; в отчёте «заблокировано TC-004», «проверить после починки бага»; pass у неисполненного теста нет; одна цифра «доказано»; после правки фикстуры фабрика перепрогнала тесты | `testproject1-dev-010` / testproject1-sdk | владелец | перенос: live-runs/2 «Живые доказательства» \| обоснование: пересборка бэклога \| подтвердил: владелец, 01.11.2026 (слово 2 пересборки) |
| Волна 1: ответ S2 доходит до брифов S3/S4 без дирижёра; блокирующий вопрос останавливает работу до зависимого артефакта; `deferred_to_report` не переспрашивается (P8) | `testproject1-dev-010` / testproject1-sdk | владелец | перенос: live-runs/2 «Живые доказательства» \| обоснование: пересборка бэклога \| подтвердил: владелец, 01.11.2026 (слово 2 пересборки) |
| Волна 2: стена S5 на объёме 22.10 (8 кейсов, 3 окна), цель ≈ 22 мин (было 3 ч 08 мин), метод отчёта t-1221; один план и один критик плана; окна без `pause`; бриф окна полный | `testproject1-dev-010` / testproject1-sdk | владелец | перенос: live-runs/2 «Живые доказательства» \| обоснование: пересборка бэклога \| подтвердил: владелец, 01.11.2026 (слово 2 пересборки) |
| Волна 2: S7 на красном тесте «лишнее/иное значение» ставит контрольный опыт до `APP_BUG`; сид слабее Given — `TEST_BUG` данных (HF2-18; на 12586 — сохранение интеграции без смены проекта) | `testproject1-dev-010` / testproject1-sdk | владелец | перенос: live-runs/2 «Живые доказательства» \| обоснование: пересборка бэклога \| подтвердил: владелец, 01.11.2026 (слово 2 пересборки) |

## Остатки

- HF2-16 (DC1-9, цикл окна S5 без 25 минут управления) — волна 2, не реализована | ранее-перенос: batch-3-wave-2-and-remainders.md | ранее-обоснование: слово владельца 25.10.2026 (вечер) «без волны 2» — релиз режется из волны 1; подтверждено словом 26.10.2026 «всё, что релиз не блокирует, откладываем» | ранее-подтвердил: — | сделано: 7cc092de
- HF2-17 (EP1-18 (б), бриф окна S5) — волна 2, не реализована | ранее-перенос: batch-3-wave-2-and-remainders.md | ранее-обоснование: то же слово владельца 25.10.2026, зависит от HF2-16 | ранее-подтвердил: — | сделано: cf511c8e
- HF2-18 (TQ1-15, контрольный опыт S7 до `APP_BUG`) — волна 2, не реализована | ранее-перенос: batch-3-wave-2-and-remainders.md | ранее-обоснование: то же слово владельца 25.10.2026; слово 25.10 «если нет, исправить во второй волне» | ранее-подтвердил: — | сделано: b515fcca


<!--
Пачка закрывается доделкой, не переносом (слово владельца 08.10.2026): `close` отказывает, пока в этом разделе есть
пункт, у которого нет одной из двух форм (ключи в нижнем регистре, пары `ключ: значение` через ` | `, текст впереди):
  - <что осталось> | сделано: <хэш 7-40 hex | t-nnn>
  - <что осталось> | перенос: <findings/<файл> | пачка N | <кучка>/findings/<файл>> | обоснование: <почему> | подтвердил: <кто, дата>
Пункт — КАЖДАЯ непустая строка раздела вне комментария: абзац, заголовок и строка внутри блока кода тоже пункты. Одно
исключение: строка с отступом в 2 и более пробелов, которая сама не начинает маркер (`-`, `*`, `•`, `1.`), продолжает пункт
выше, и ключи читаются по всему пункту. Подпункт с маркером, строка с табуляцией и строка с отступом без пункта выше —
пункты сами по себе. Скрыть строку может только комментарий; комментарий без закрытия — отказ.
Цель `перенос:` должна существовать: файл — в дереве и в индексе (`git add` до `close`), `пачка N` — строка карточки этой
кучки, не эта пачка и не закрытая. `подтвердил` пишет человек, не агент сам. Пустой раздел — можно закрывать.
-->
