# t-1224 — черновик пачки `hotfix-12586/2` (дизайнер, 25.10.2026; ред. 3: две волны, GW1-23 — красный тест в окне, свип класса)

Это черновик, а не решение. Lead кладёт текст §2 в `plans/piles/hotfix-12586/batch-2-run-12586-s5.md`, строку §3 — в карточку,
строки §4 — в «Ход» пачек-источников. Развилки §6 адресованы владельцу или Lead — адресат назван у каждой.

Ред. 2 вносит два слова владельца от 25.10.2026, переданные координатором:
1. DC1-9 уходит во вторую волну, между волнами стоит шлюз.
2. В первую волну входят узел окна 4 и свип класса «красный — исход по умолчанию».

Ред. 3: у узла окна 4 появился источник — GW1-23 (`gates-and-words`). Его «Пишет в» скопировано из строки.

## 0. Для Lead: что сверено по носителям (свежесть, rule 3)

- **Строки узлов** прочитаны в файлах пачек 25.10. Все шесть пачек: статус «ожидает», взял «—».

  | Файл пачки | Узлы |
  |---|---|
  | `gates-and-words/batch-1-words-and-gates.md` | GW1-3, GW1-7, GW1-8, GW1-14, GW1-21, GW1-22, GW1-23 |
  | `execution-probes/batch-1-one-runner.md` | EP1-10, EP1-11, EP1-13, EP1-15…EP1-18 |
  | `driver-controller/batch-1-controller-seams.md` | DC1-9 |
  | `cost-dashboard/batch-1-true-price.md` | CD1-13, CD1-14 |
  | `test-code-quality/batch-1-tests-that-discriminate.md` | TQ1-3, TQ1-4, TQ1-7, TQ1-12…TQ1-14 |
  | `report-delivery/batch-1-honest-report.md` | RD1-1, RD1-8 |

- **Код пачки 1 уже в дереве `main`.** Grep 25.10 находит `contract.py:170 then_remainder_rows`, `window_record.py:411 probe_gap_block`,
  `execution_request.py:1228 profiles_owning`. Пачка 1 — «сдано», но не закрыта: ждёт живое доказательство.
- **FB-5 уже в строке GW1-22.** Пункт `manifest_put` (`_partition_scoped`, `_merge_entry`) внесён коммитом d5102666.
- **Коллизия имени.** Имя `blocked_by` в пакете уже значит «владельцы, держащие доставку». Носители этого смысла:
  - `references/artifact-contract-ledger.md:22,40`;
  - `check_delivery.py:1737-1738,1783`;
  - `delivery_summary.py:298,398`;
  - `handoff_check.py:359-361,450`;
  - `handoffs/s8-scribe-to-gate-b.yaml:31,58`.

  GW1-22 вводит причину `blocked_by: <case|instance>` в те же файлы. Это развилка F-10.
- **`introduced_helpers` в пакете нет.** Это поле TQ1-7, на него опирается TQ1-13. Grep даёт 0 вхождений. Позитивный контроль той же
  формы — `blocked_by\b`, 41 вхождение.
- **Корпуса TQ1-4 нет.** Glob `evals/**` находит 9 файлов, папки `seeded-defects/` среди них нет.
- **Остаток GW1-14 после HF1-10** (`docs/tasks/handoffs/t-059-hf1-10.md`, п. 6):

  | Пункт | Суть |
  |---|---|
  | F7 | `manifest_put` заменяет `then_bindings` целиком |
  | F8 | бриф гейта B, `delivery_summary.py` |
  | A1 | Then-уровня `deferred_by_decision:*` рядом с зелёным |
  | A2 | `no-assert-` на любой записанный неразрешённый Then |

  Находками в кучках эти пункты не лежат: Grep по `plans/piles` даёт 0, контроль `deferred_by_decision` находит B-289. Со списком
  находок t-074 **НЕ сверено**. Пункт E14 закрыт фикс-раундом t-067.
- **Остаток EP1-10** (`t-055-hf1-3.md`). Сделаны C1…C4 и C6. C5 по онбордингу сделан только текстом фазы, без кодового читателя.
  C5 по `window_record` закрыт HF1-14. Предикат профиля уже в `main`. Это развилка F-6.
- **GW1-23 и разведка t-1225** (`docs/tasks/handoffs/t-1225-red-test-review-receipt-recon.md` прочитана целиком; строка GW1-23 —
  `gates-and-words/batch-1-words-and-gates.md:61`; находка — `gates-and-words/findings/20261025-krasnyj-test-bez-raspiski-okna.md`).
  Корень проверен Lead: `window_record.derivable()` пропускает только `blocked_by_env:`, `handed_to_person:` и `probe_gap:`. Красный прогон
  даёт `product:<id>` (`acceptance.py:568-569`) — квитанции нет. Цепочка последствий:
  1. `review_receipt_ref` не появляется.
  2. `controller._code_review_problems` (`:4596-4631`) пишет «not receipted».
  3. `stage_done.py:743-746` пишет «no accepted controller stage».
  4. `contract.window_shape_errors` (`:3389-3392`) требует `probe` у красного: `probe_gap` по контракту только для зелёного
     (`contract.py:3322`, `s5.md:114-115`).

  Задеты все красные окна прогона: 1–3 и 6–8 закрыты только словом человека. Носители противоречат друг другу: `s5.md:117-128`
  обещает «handed over RED». Требует ли мутационная проба зелёного базиса — не проверено. Номера строк `controller.py`/`contract.py`
  взяты из отчёта скаута, сам я их не сверял.
- **Активные пачки** (`plans/PILES.md`): `conductor/1` (зона `story_run.py`, `controller.py`, `skills/qa-story/**`), `collect/2`, `kb/1`,
  `onboarding-hooks/2`. Пересекается только `conductor/1`. Это развилка F-14.
- **Пути «Пишет в»** проверены Glob, в том числе `scripts/stage_done.py`; новые помечены (new). Не найдены три имени тестов:
  `test_manifest_put*.py`, `test_planning_contract*.py`, `test_telemetry_hook*.py` — «имя — проверить по коду».

## 1. Инварианты архитектуры (AR-n) и проверка изменения каждого

Источник — `ai-packages/qa-factory/design/architecture.md`, «Change check». Узел называет свои AR-n в строке `architecture:` коммита.
Критик HF2-0 отвечает по этому списку на вопрос 10.

| AR | Узлы | Проверка изменения |
|---|---|---|
| AR-10 требование до работы | HF2-12, HF2-14, HF2-16, HF2-17 | новая проверка называет своё поле и где роль его читает; новое обязательное поле входит в контракт, скелет и отказ одним коммитом |
| AR-11 только нужный контекст | HF2-3, HF2-12…HF2-17 | числа A22/A25 до и после |
| AR-12 трение измеряется | HF2-9, HF2-10, HF2-16 | `code_friction` до и после, или «не измерено» открытым пунктом |
| AR-13 один читатель факта | HF2-2, HF2-7, HF2-8, HF2-12 | grep SIBLING_MAP; позвать выжившего; grep той же формы с позитивным контролем |
| AR-14 один писатель артефакта | HF2-7, HF2-16 | `stages.json` и строка писателя одним коммитом |
| AR-15 одна точка всюду | HF2-2, HF2-16 | grep по проблеме, каждый сайт назван |
| AR-19 близнецы стадий | HF2-3, HF2-4 (`s5.md` ↔ код) | grep оси 5, близнецы названы |
| AR-20 храповики только сжимаются | HF2-3, HF2-12…HF2-17 | каждый подъём назван |
| AR-21 сбор едет целиком | HF2-7, HF2-16 | читатель назван; новая передача — строка `handoffs/index.yaml` |
| AR-22 у поля есть писатель и читатель | HF2-3, HF2-4, HF2-5, HF2-7, HF2-12 | grep без учёта регистра с контролем; `test_field_producers.py` |
| AR-23 пустой исход объявлен | HF2-3, HF2-12, HF2-16 | объявлен в вводящем коммите |
| AR-24 слова человека целиком | HF2-7 | `--words-file` через `person_words.read`, `door()` |
| AR-25 у состояния есть выход | HF2-3, HF2-4, HF2-11, HF2-16 | строка в `state-exits.md` и обратная команда |
| AR-26 единица — требование | HF2-3, HF2-6 | census-grep |
| AR-27 находка под своим владельцем | HF2-3, HF2-4, HF2-6 | словарь владельцев; `word_of` |
| AR-28 неизвестное не становится проходом | HF2-3, HF2-4, HF2-6, HF2-7, HF2-8, HF2-10, HF2-11 | поведение на отсутствующем, нечитаемом и пустом входе названо и запинено |

## 2. Текст файла пачки

<!-- НАЧАЛО: plans/piles/hotfix-12586/batch-2-run-12586-s5.md -->

# Срочная починка прогона TP1-12586 — пачка 2: красный — обычный исход S5, Then — единица исхода, ответы человека применяются сразу, S5 к ≈ 22 минутам

кучка: `hotfix-12586` | статус: ожидает | взял: — | ветка: — | MR: — | стенд: нужен (живое доказательство) | приоритет: П1 | issue: —

очередь: conductor/1 → hotfix-12586/2
очередь: hotfix-12586/1 → hotfix-12586/2
очередь: hotfix-12586/2 → gates-and-words/1
очередь: hotfix-12586/2 → execution-probes/1
очередь: hotfix-12586/2 → driver-controller/1
очередь: hotfix-12586/2 → report-delivery/1
очередь: hotfix-12586/2 → cost-dashboard/1
очередь: hotfix-12586/2 → test-code-quality/1

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего, живые
доказательства (FR-33) сделаны или переданы строкой в кучку «живые прогоны».

Шлюз между волнами (слово владельца 25.10.2026):
- Волна 1 — HF2-1…HF2-15 и проход HF2-0 по волне 1. Волна 2 — HF2-16, HF2-17 и проход HF2-0 по волне 2.
- Перед первым диспатчем волны 2 взявший спрашивает владельца: «делаем вторую волну или не успеваем и делаем релиз без неё».
  Ответ записывается строкой «Хода».
- Без волны 2:
  - релиз режется из волны 1 после её BATCH CANON и прохода HF2-0;
  - узлы волны 2 остаются «ожидает» в этой пачке;
  - пачка не закрывается, пока они не приняты или не перенесены строкой «Остатков» с подтверждением человека.

Решения владельца:

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
| `agents/qa-code-critic.md`, `references/code-review-rubric.md` | HF2-3 → HF2-13 → HF2-14 → HF2-15 → HF2-16 | волна 2 раскладывает строки по ПЛАН/КОД/ОБА |

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

Волна 2 (после шлюза): один план автотестов и один критик плана, окна без простоя, бриф окна. Цель — стена S5 ≈ 22 мин на 8 тестов
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
  - волна 2 — HF2-16 (DC1-9), HF2-17 (EP1-18 (б)); один дизайнер.
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
| HF2-0 | П1 | Критик на дифф пачки — по проходу на волну после схождения (R13-g; слово владельца 23.10.2026). По каждому узлу: находка, FR и AR (вопрос 10), DUPLICATION и CODE QUALITY (`docs/tasks/critic-diff-brief.md`). Особо: красный по требованию закрывает окно своей квитанцией, а зелёный или неисполненный так не проходит (FR-18, FR-34); имя новой причины против `ledger.blocked_by`; одна формулировка «закомментированный Then»; A22/A25; в волне 2 — артефакт и передача плана S5 и стена S5 против цели. BATCH CANON прикладывается до вердикта. Вердикт: принять или фикс-раунд | critic | отчёты `docs/tasks/specs/reviews/t-nnn-hf2-wave1-review.md`, `…-wave2-review.md` | волна 1: HF2-1…HF2-15; волна 2: HF2-16, HF2-17 | ожидает |
| HF2-1 | П1 | Свип класса «красный — исход по умолчанию: проход по цепочке S5–S9» (вопрос владельца 25.10.2026). Класс всплыл в прогоне трижды: partial-green (GW1-22), остаток Then только `handed_to_person` (GW1-14), красный тест без квитанции ревью (GW1-23). Скаут перечисляет каждую проверку, гейт, писателя квитанций и пробу цепочки приёма S5 и ниже, которые требуют зелёного прогона или зелёного базиса. Минимум: `s5_precheck`, `acceptance.validate_window`, `window_record`, `probe_by_code`, `red_sandbox`, приём контроллера (`_code_review_problems`, `_s5_completion_problems`), `contract.window_shape_errors`, `stage_done`, `ledger`, `check_delivery`, `traceability`; тексты `s5.md`–`s7.md` и ролей. Вердикт по строке: свой санкционированный путь (каким полем) или отказ / только слово человека — пробел, направленный в узел пачки (HF2-3, HF2-4, HF2-8 или по F-17). Каждое «зелёного не требует» — с позитивным контролем той же формы; отдельно — требует ли `probe_by_code` зелёного базиса (F-20). Форма — свип HF1-11 (FR-34, FR-21, FR-22, P21) | scout → Lead | дайджест `docs/tasks/specs/reports/t-nnn-hf2-1-red-default-sweep.md` | — | ожидает |
| HF2-2 | П1 | EP1-13: номер Then строки `then_bindings` и метка `then-remainder-unrecorded-` — по одному носителю в `contract.py` (читают `s5_precheck`, `judge_code`, `exit_gate`). Пин меток становится тестом «в `exit_gate` нет литерала метки». Чтение испорченного `then` — по FR-59 (`execution-probes/findings/20261023-ostatki-then-ostatka-dva-chitatelya-nomera-i-tag-v-dvuh-fajlah.md`; FR-14, FR-59, AR-13, AR-15) | builder | `scripts/contract.py`, `scripts/s5_precheck.py`, `scripts/judge_code.py`, `scripts/exit_gate.py`, `scripts/tests/test_then_remainder.py`, `changelog.d/` | — (HF1-10 принят) | ожидает |
| HF2-3 | П1 | GW1-22: один кейс держит смесь исходов по Then/партиции — передано человеку, зелёное, красное по багу, заблокировано упавшей проверкой (вопрос владельца 24.10.2026; TC-005/TC-006 при красной MS Teams-партиции по багу TC-004). `partial-green`/`contradicts-but-green` сверяют зелёный с его партицией. Остаток Then обобщается на красный и заблокированный. Новая причина «заблокировано другой проверкой» (имя — F-10) идёт S4 → S5 → S6 (не `partial`) → S8 → S9 и в «Left with you». Ledger не теряет переданный Then рядом с `failed:*`. `manifest_put` снимает строку `unresolved[]` (FB-5). Пункт G8 «окно S5 для красного» — квитанцию и приём делает HF2-4 (GW1-23). Независимые Then не прячутся за красным: перенос до красного или комментарий с причиной; закомментированный или заблокированный Then — строка «Left with you»; критик кода ловит независимый Then за красным (слово владельца 24.10.2026). Пробелы HF2-1 — вход (`gates-and-words/findings/20261024-smeshannye-iskhody-v-odnom-keyse.md`; t-1216; P16, P17, P21, FR-13, FR-21, FR-34, AR-19, AR-23, AR-26, AR-27) | designer → critic на план → builder → critic | `scripts/s5_precheck.py` (`check_manifest`), `scripts/manifest_put.py` (`_partition_scoped`, `_merge_entry`), `scripts/contract.py` (`UNRESOLVED_REASONS`, `then_remainder_*`, `rollup_status`), `scripts/acceptance.py`, `scripts/window_record.py`, `scripts/ledger.py`, `scripts/traceability.py`, `scripts/check_delivery.py`, `references/delivery-verdict-kinds.json`, `references/artifact-contract.md`, `agents/qa-automator.md`, `agents/qa-case-designer.md`, `agents/qa-code-critic.md`, `references/code-review-rubric.md` (измерения 6 и 8), `agents/qa-failure-analyst.md` (S7), их тесты, `changelog.d/` | HF2-1, HF2-2; GW1-14 и GW1-8 приняты | ожидает |
| HF2-4 | П1 | GW1-23: красный по требованию тест получает расписку ревью окна S5 и проходит стадию без слова человека (слово владельца 25.10.2026: «последнюю проблему прогона стори нужно обязательно взять в срочную пачку»; найти баги — цель, красный — исход по умолчанию). `product:` со строкой `contradicts_requirement` — выводимый пробел окна (`window_record.derivable`); `probe` для него не нужен (вместо — запись «проба неприменима: красный» без права слова, F-20); `finish` выводит пару; контроллер принимает стадию. Без строки причины — отказ с дверью роли. Корень (проверен Lead): `derivable()` пропускает только `blocked_by_env:`, `handed_to_person:`, `probe_gap:`, а красный прогон даёт `product:<id>` (`acceptance.py:568-569`) — квитанции нет. Отсюда «not receipted» (`controller._code_review_problems`) и «no accepted controller stage» (`stage_done`); `window_shape_errors` требует `probe`. На 12586 все красные окна (1–3, 6–8) закрыты только словом; окно 4 — два красных UI-теста, три слова человека (`records/journal.jsonl` 196–199). `s5.md:117-128` и код говорят одно (F-21). Пробелы HF2-1 — вход (`gates-and-words/findings/20261025-krasnyj-test-bez-raspiski-okna.md`; t-1225; FR-34, FR-21, P21, AR-25, AR-28) | designer (тот же, что HF2-3) → critic на план → builder → critic | `scripts/window_record.py` (`derivable`, `receipt`), `scripts/acceptance.py` (`validate_window`), `scripts/contract.py` (`window_shape_errors`, `probe_gap`), `scripts/controller.py` (`_code_review_problems`), `scripts/stage_done.py`, их тесты, `changelog.d/` (`story_step.py` `finish` и `s5.md` — по F-21) | HF2-1, HF2-3 (тот же механизм), HF2-8 (EP1-16) | ожидает |
| HF2-5 | П1 | Остаток GW1-14 после HF1-10 (`t-059-hf1-10.md`, п. 6). F7: `manifest_put` заменяет `then_bindings` целиком (E19 спеки t-052). A1: Then-уровня `deferred_by_decision:*` рядом с зелёным — тихий проход в `ledger.plan_row_state` и `report_facts._classify`. A2: `no-assert-` на любой записанный неразрешённый Then. Состав — F-12 (`gates-and-words/findings/20261022-odin-then-nelzya-otdat-cheloveku.md`; P13, P21, FR-4, FR-9, AR-22, AR-28) | designer (тот же, что HF2-3) → builder → critic | `scripts/manifest_put.py` (`_merge_entry`), `scripts/ledger.py` (`plan_row_state`), `scripts/report_facts.py` (`_classify`), `scripts/s5_precheck.py` (`check_bindings`), их тесты, `changelog.d/` | HF2-3 | ожидает |
| HF2-6 | П1 | RD1-8: pass неисполненному тесту, «9 proven» рядом с «1 green», Q-4 отвечен и открыт. Статус теста — только из записи исполнения («не исполнен», если записи нет). Одна цифра «доказано». Статус вопроса — из носителя HF2-7. Сверка кодом, отказ называет расхождение. Первым ходом — сверка RD1-1 (F-16) (`report-delivery/findings/20261024-otchet-pokazyvaet-pass-neispolnennomu-testu.md`; t-1207 п.5; P21, FR-41, FR-59, AR-28) | designer → builder → critic | `scripts/check_delivery.py`, `scripts/report_facts.py` (уточняет спека), их тесты, `changelog.d/` | HF2-3, HF2-5, HF2-7; RD1-1 — F-16 | ожидает |
| HF2-7 | П1 | GW1-21: ответы человека на вопросы S2/S3/S4 применяются сразу (слово владельца 24.10.2026). Один ход записи: `question_register` + `human_answer`. Бриф каждой следующей роли читает ответы из хранилища; устаревший `open halt` уходит; отвеченный вопрос остаётся `answered`. Блокирующий вопрос — стоп до зависимого артефакта, S4 в `where`. Поздний ответ — точечная доработка по `question_refs`. Новый вид ответа `deferred_to_report`. Один носитель статуса вопроса для гейта S3 и репетиции гейта A. Сопутствующее: чекпойнт S1, устаревший `input_hash` в `rework`, раунд критика `incomplete` (`gates-and-words/findings/20261024-otvety-cheloveka-ne-primenyayutsya-srazu.md`; t-1208, t-1209; FR-7, FR-8, FR-9, FR-59, AR-13, AR-14, AR-22, AR-24, AR-28) | designer → critic на план → builder → critic | `scripts/story_run.py` (`take_question_answer`, стоп вопросов), `scripts/question_register.py`, `scripts/question_stop.py`, `references/question-vocabulary.json`, `scripts/brief_pack.py` (`answers_of`), `scripts/planning_contract.py` (`apply_gate_answers`), `scripts/gate_brief.py`, `agents/qa-requirements-tester.md`, их тесты, `changelog.d/` | — (GW1-3, GW1-7 — после пачки) | ожидает |
| HF2-8 | П1 | EP1-16: мутационная проба строится с `profile_id` строки манифеста (`build_request` → `build_mine_request`; ветка `node_ids` профиль не теряет). Отказ без профиля называет дверь «строка манифеста», не `--profile`. Соседи: `red_sandbox`, `run_suite --mine`, `execution_request.py:1714`. На 12586 все пять проб окна 1 — `not_executed` (FB-4). У зелёного `probe is missing` здесь, у красного — HF2-4 (`execution-probes/findings/20261024-proba-mutacii-ne-peredaet-profil.md`; t-1220; FR-2, FR-17, AR-13) | designer (тот же, что HF2-10) → builder → critic | `scripts/probe_by_code.py` (`build_request`), `scripts/execution_request.py` (`build_mine_request`), `scripts/red_sandbox.py`, их тесты, `changelog.d/` | HF2-1; HF1-3, HF1-14 приняты | ожидает |
| HF2-9 | П1 | CD1-14: замер. Вызовы вдвое медленнее (shell 4,4 → 10,4 с); подозревается `cost_capture`. Сначала тот же сценарий с выключенным хуком, медианы до и после. Если подтвердится: один экземпляр, дебаунс, Stop не держит ход; цена истинная (P18) (`cost-dashboard/findings/20261025-cost-capture-zamedlyaet-vyzovy.md`; t-1221; P11, P18, FR-28, FR-55) | builder (замер) → designer → builder → critic | `scripts/cost_capture.py`, `scripts/telemetry_hook.py`, `hooks/hooks.json`, их тесты, `changelog.d/` | — (CD1-13 — F-2) | ожидает |
| HF2-10 | П1 | EP1-17: запуск теста без 20 минут обвязки. Один collect на запрос; явный `--node-id` при существующем файле — без collect; неразобранный collect проверяет сам запуск; одна проба рантайма; отказ «нет `runtime_probes`» — до collect (`execution-probes/findings/20261025-s5-zapusk-testa-20-minut-obvyazki.md` §1; t-1221; P11, FR-51, FR-55, AR-12) | designer (тот же, что HF2-8) → builder → critic | `scripts/run_suite.py` (`collect`, `verify_node_ids`, `probe_runtime`), `scripts/execution_request.py` (`build_mine_request`, `_spell_as_collected`), их тесты, `changelog.d/` | HF2-8, HF2-9 | ожидает |
| HF2-11 | П2 | EP1-15: если исполняемая часть теста или фикстуры изменилась после последнего прогона, фабрика сама перепрогоняет тест и red-probe до отчёта (при доступном стенде). Человеку — только по P19 ступени 5. Косметика перепрогона не требует, переименование требует (`execution-probes/findings/20261024-net-finalnogo-progona-finalnyh-fajlov.md`; t-1207 п.6; P19, FR-33, AR-25) | designer → builder → critic | `scripts/acceptance.py`, `scripts/window_record.py`, `scripts/proof_level.py` (уточняет спека), их тесты, `changelog.d/` | HF2-3, HF2-4, HF2-12 | ожидает |
| HF2-12 | П1 | EP1-18 (а): обязательные поля строки манифеста (`assertion_id`, `defect_location`, `change_disposition`, `change_basis_ref`, `profile_id`, поля HF2-3) роль получает до работы: в форме строки и от `manifest_from_tests`. `s5_precheck` перечисляет недостающие одним списком; один носитель — `window_record`; роль автоматора называет поля. Бриф окна — HF2-17 (находка §2; FR-38, FR-13, AR-10) | designer → builder → critic | `scripts/window_record.py`, `scripts/manifest_from_tests.py`, `scripts/s5_precheck.py`, `agents/qa-automator.md`, их тесты, `changelog.d/` | HF2-8, HF2-3, HF2-4 | ожидает |
| HF2-13 | П2 | TQ1-13: второй `select_project` и `wait_for_page_load`; одна фикстура дважды в conftest окна. Волна 1 — строка критика кода (K16). Тропа `introduced_helpers[]` — с TQ1-7 (F-4) (`test-code-quality/findings/20261024-vtoroj-heljper-ryadom-s-sushchestvuyushchim-i-dubli-fikstur.md`; P12, AR-15) | builder → critic | `scripts/manifest_from_tests.py` (по F-4 — с TQ1-7), `agents/qa-code-critic.md` (как TQ1-7), `changelog.d/` | HF2-3; TQ1-7 — F-4 | ожидает |
| HF2-14 | П3 | TQ1-14: строка «проверка количества — assert до распаковки» (P16) и вопрос критику «уровень теста совпадает с планом S3 или отклонение названо»; в волне 2 вопрос уходит в ПЛАН (K6) (`test-code-quality/findings/20261024-krasnaya-stroka-raspakovka-do-assert-i-e2e-dlya-klientskih.md`; P16, P19) | builder (спека Lead ≤ 3 пунктов) | `references/test-code-patterns.md` (+ slices — generated), `references/code-review-rubric.md`, `agents/qa-code-critic.md`, `changelog.d/` | HF2-13; TQ1-3 — после пачки | ожидает |
| HF2-15 | П2 | TQ1-12: тест отказа проходит на чужом 400 (TC-008); сравнение маски `'******'` с `'******'`. Правило «тест отказа различает причину; маска — не проверка сохранности» — строками рубрики dim 2; образцы в корпус — с TQ1-4 (F-3) (`test-code-quality/findings/20261024-otkaz-ne-razlichaet-prichinu-i-sravnenie-po-maske.md`; P20, FR-18) | builder → critic | строки rubric dim 2 (`references/code-review-rubric.md`); корпус `evals/seeded-defects/**` (new) — по F-3; `changelog.d/` | HF2-14; TQ1-4 — F-3 | ожидает |
| HF2-16 | П1 | **Волна 2.** DC1-9: цикл окна S5 без 25 минут управления. Форма S5 (слово владельца 25.10.2026): один план автотестов на все кейсы, один критик на весь план, без блокеров план не переписывается, окна получают требования, план и замечания. Критик после кода проверяет тесты и соответствие плану (блокер в плане — F-8). Деление ПЛАН/КОД/ОБА и C1–C15 (`t-1222`). `bind` внутри `start`; без `pause` между возвратами; форму дайджеста чинит код; возобновлённой роли — дельта; медианы — после HF2-9 (`driver-controller/findings/20261025-cikl-okna-s5-25-minut-upravleniya.md`; t-1221, t-1222; P3, P11, FR-55, AR-12) | designer → critic на план → builder → critic | `scripts/story_step.py`, `scripts/controller.py`, `scripts/exit_gate.py` (`digest`), `scripts/brief_pack.py`, `skills/qa-story/phases/s5.md`, `agents/qa-automator.md`, `agents/qa-code-critic.md`, `references/code-review-rubric.md`, `handoffs/s5-*.yaml` (+ передача плана S5 (new), `handoffs/index.yaml`, `references/stages.json`), `scripts/manifest_from_tests.py`, `scripts/s5_precheck.py`, их тесты, `changelog.d/` | шлюз волны 2; HF2-9; волна 1 принята | ожидает |
| HF2-17 | П1 | **Волна 2.** EP1-18 (б): бриф окна S5 даёт роли файлы и фикстуры кейсов окна и образцы соседних тестов (было 112 вызовов чтения, 12,7 мин) — вместе с планом и замечаниями HF2-16; цель ≈ 22 мин (FR-38, AR-10) | designer (тот же, что HF2-16) → builder → critic | `scripts/brief_pack.py`, `skills/qa-story/phases/s5.md`, `agents/qa-automator.md`, их тесты, `changelog.d/` | HF2-16 | ожидает |

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
- пробелы свипа вне узлов (F-17).

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 25.10 __:_x — пачка собрана Lead из двенадцати узлов шести кучек по слову владельца 25.10.2026 (CD1-13 и TQ1-11 не входят), связки A–E —
  Lead. Сверх списка: EP1-13 и остаток GW1-14 (та же функция); GW1-23 и свип HF2-1 — по словам владельца. DC1-9 и бриф окна EP1-18 —
  волна 2. Черновик t-1224.
- (правило) Перед первым диспатчем волны 2 (HF2-16, HF2-17) взявший спрашивает владельца: «делаем вторую волну или не успеваем и делаем
  релиз без неё». Ответ записывается следующей строкой. Без волны 2 релиз режется из волны 1 после её BATCH CANON и HF2-0, а HF2-16 и
  HF2-17 остаются «ожидает».

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|
| Волна 1, повтор S5 TP1-12586 на копии `testproject1-dev-010`: каждое окно с красными по требованию тестами закрыто своей квитанцией, слов человека — ноль (блоков `not receipted`, `no accepted controller stage`, `probe is missing` нет); проба мутации исполнена при двух профилях (FB-4); один collect на `--mine`; ни одного возврата по полям строки; стена S5 напечатана с объёмом — промежуточная цифра, без DC1-9 | `testproject1-dev-010` / testproject1-sdk | владелец | ожидает |
| Волна 1: медианы вызовов до и после HF2-9; цена из двух источников сходится или печатается диапазоном (P18) | `testproject1-dev-010` / testproject1-sdk | владелец | ожидает |
| Волна 1: TC-005/TC-006 записаны смесью исходов; в отчёте «заблокировано TC-004», «проверить после починки бага»; pass у неисполненного теста нет; одна цифра «доказано»; после правки фикстуры фабрика перепрогнала тесты | `testproject1-dev-010` / testproject1-sdk | владелец | ожидает |
| Волна 1: ответ S2 доходит до брифов S3/S4 без дирижёра; блокирующий вопрос останавливает работу до зависимого артефакта; `deferred_to_report` не переспрашивается (P8) | `testproject1-dev-010` / testproject1-sdk | владелец | ожидает |
| Волна 2: стена S5 на объёме 22.10 (8 кейсов, 3 окна), цель ≈ 22 мин (было 3 ч 08 мин), метод отчёта t-1221; один план и один критик плана; окна без `pause`; бриф окна полный | `testproject1-dev-010` / testproject1-sdk | владелец | ожидает |

## Остатки

<!-- КОНЕЦ: plans/piles/hotfix-12586/batch-2-run-12586-s5.md -->

Раздел «Остатки» остаётся пустым, с комментарием-шаблоном. Lead копирует шаблон дословно из `gates-and-words/batch-1-words-and-gates.md:77-88`.

### 2а. Края пачки (у каждого — инвариант, который он защищает)

| # | Край | Поведение | Инвариант |
|---|---|---|---|
| E1 | Стена S5 на другом объёме или после одной волны 1 | цифра печатается с объёмом и номером волны | время на другом объёме не засчитывается как достижение цели |
| E2 | Замер HF2-9 не подтвердил гипотезу | узел закрывается замером; HF2-16 берёт его медианы | без замера починки нет (pt. 6a) |
| E3 | Починка HF2-9 | хвост расхода записан до отчёта; пока он не записан — цена диапазоном | цена истинна (P18) |
| E4 | 18 узлов при границе L (10–15) | две волны в одной пачке — слово владельца (F-18) | превышение записано, не молча |
| E5 | Новая причина при существующем `ledger.blocked_by` | имя выбирается в F-10 | одно имя — один смысл |
| E6 | Две формулировки «закомментированный Then» | с причиной и «Left with you» — путь; без них — `fail` | маскировку по-прежнему отказывают |
| E7 | «Критик не судит покрытие» (HF2-16) против «ловит независимый Then» (HF2-3) | порядок ассертов — класс КОД | покрытие судится один раз |
| E8 | A22/A25: запас автоматора 1 439 Б по t-072 (оценка, не перемерено) | излишек уходит в бриф или slices; подъём только названной строкой | храповик только сжимается |
| E9 | Пустые входы | один исход читается как сегодня; бриф без ответов не несёт `open halt`; пустые замечания объявлены; недостающие поля — одним списком | пустой исход объявлен |
| E10 | Ответ человека не сопоставим (HF2-7) | вопрос, не проход | FR-59 |
| E11 | Два профиля, у строки нет `profile_id` (HF2-8) | отказ с дверью «строка манифеста» | молча не берётся первый профиль |
| E12 | `--node-id` без collect (HF2-10) | id проверяет pytest; «не найдено» → `node_id_mismatch` | «не проверено», никогда не «проверено»; неудобные входы: баннер, несуществующий id, параметр с пробелом или юникодом, таймаут |
| E13 | Правка теста: стенда нет / косметика / переименование (HF2-11) | P19-5 с причиной / старое доказательство / перепрогон | доказательство на других байтах не засчитывается |
| E14 | Нет записи исполнения (HF2-6) | «не исполнен» | pass без исполнения недостижим |
| E15 | **`derivable()` в более ответственной роли** (GW1-23: советчик → гейт закрытия окна) | `product:<id>` выводим только при строке `contradicts_requirement` манифеста на этот инстанс; иначе — отказ, как сегодня | ошибаться можно только в сторону отказа: зелёный, неисполненный или упавший не по требованию тест так окно не закрывает (FR-18). Неудобные входы — они обязаны остаться отказом: строка на чужой кейс или инстанс; краш или ошибка фикстуры (`outcome: error`); неисполненный тест со строкой; строка без Then; упала другая партиция; заявление роли без строки манифеста; слово `*` |
| E16 | Красный и слово человека | окно закрывается квитанцией; слово не нужно и зелёный путь не открывает | правило `contract.py:3322` в силе |
| E17 | Проба для красного | «неприменима: красный» без права слова (F-20) | зелёному проба обязательна |
| E18 | Пробел свипа вне узлов | F-17 | пробел не теряется |
| E19 | Шлюз: ответ «без волны 2» или ответа нет | волна 2 не стартует; релиз из волны 1; узлы «ожидает»; закрытие — F-19 | без слова владельца волны 2 нет; перенос — только с человеком |
| E20 | `s5.md` обещает «handed over RED» вопреки коду | приводятся к одному поведению одним коммитом (F-21) | близнецы меняются вместе (AR-19) |
| E21 | На повторе найден дефект HF1-n | `defect_found` против узла пачки 1 | закрытое молча не переоткрывается |
| E22 | `start` упал после `bind` (HF2-16) | откат или выход в `state-exits.md` | одна привязка на диспатч |
| E23 | Дайджест с одной правкой формы | код чинит только форму | смысл вердикта не меняется (FR-35) |
| E24 | В плане S3 нет `level` (HF2-14) | «не проверено» | молчание — не «соответствует» |

## 3. Строка карточки `plans/piles/hotfix-12586/README.md`, таблица «Пачки»

| 2 | S5 прогона TP1-12586: красный по требованию тест — обычный исход, закрывает окно своей квитанцией без слова человека; кейс держит смесь исходов по Then до отчёта; отчёт не ставит pass неисполненному; ответ человека на вопрос S2–S4 сразу доходит до ролей; проба мутации работает при двух профилях; запуск теста без двойного collect, вызовы без двукратного замедления; волна 2 (по слову владельца на шлюзе) — один план автотестов и один критик плана, окна без простоя, к цели ≈ 22 мин на 8 тестов | — | L+ (18 узлов, две волны) | ожидает | — | — | — |

Тем же ходом в карточке:
- в «зона:» добавить: `acceptance.py`, `ledger.py`, `traceability.py`, `check_delivery.py`, `judge_code.py`, `exit_gate.py`, `stage_done.py`,
  `story_run.py`, `question_register.py`, `question_stop.py`, `planning_contract.py`, `red_sandbox.py`, `manifest_from_tests.py`,
  `run_suite.py`, `proof_level.py`, `cost_capture.py`, `telemetry_hook.py`, `hooks/hooks.json`, `handoffs/s5-*.yaml`, пять `agents/qa-*.md`,
  `code-review-rubric.md`, `test-code-patterns.md`, `delivery-verdict-kinds.json`, `artifact-contract.md`, `question-vocabulary.json`, `s5.md`;
- «Бриф пачки 2»: начать с HF2-1, HF2-9 и дизайнеров B, C, E; дизайнер A стартует после дайджеста HF2-1; шлюз перед волной 2;
- «Содержание»: строка **Пачка 2** и по строке на каждую находку — 13 файлов, включая GW1-23, плюс находка EP1-13 и отчёт t-059; находки
  несут `перенос: hotfix-12586/batch-2`.

## 4. Строки «Ход» пачек-источников (по одной на пачку)

- `gates-and-words/batch-1-words-and-gates.md`:
  `- 25.10 __:_x — GW1-21, GW1-22, GW1-23 и остаток GW1-14 (отчёт t-059 п. 6: F7, A1, A2) исполняются срочной пачкой `hotfix-12586/2`, волна 1 (слово владельца 25.10.2026; находки несут `перенос:`); их статус здесь меняется при её закрытии хэшем, сама пачка 1 не взята. GW1-3 и GW1-7 остаются здесь и идут после неё (`очередь: hotfix-12586/2 → gates-and-words/1`).`
- `execution-probes/batch-1-one-runner.md`:
  `- 25.10 __:_x — EP1-13, EP1-15, EP1-16, EP1-17 и часть EP1-18 «поля строки до работы» исполняются срочной пачкой `hotfix-12586/2`, волна 1; часть EP1-18 «бриф окна S5» — её волна 2 (слово владельца 25.10.2026; находки несут `перенос:`); их статус здесь меняется при её закрытии хэшем, сама пачка 1 не взята. EP1-11 и остаток EP1-10 (кодовый читатель онбординга) остаются здесь.`
- `driver-controller/batch-1-controller-seams.md`:
  `- 25.10 __:_x — DC1-9 исполняется срочной пачкой `hotfix-12586/2`, волна 2 — после шлюза: перед её началом владельца спрашивают, делаем её или релиз без неё (слово владельца 25.10.2026; находка несёт `перенос:`); его статус здесь меняется при её закрытии хэшем, сама пачка 1 не взята.`
- `cost-dashboard/batch-1-true-price.md`:
  `- 25.10 __:_x — CD1-14 исполняется срочной пачкой `hotfix-12586/2`, волна 1 (слово владельца 25.10.2026; находка несёт `перенос:`); его статус здесь меняется при её закрытии хэшем, сама пачка 1 не взята. CD1-13 в срочную пачку не входит (слово владельца 25.10.2026) и идёт после неё по `cost_capture.py`.`
- `test-code-quality/batch-1-tests-that-discriminate.md`:
  `- 25.10 __:_x — TQ1-12, TQ1-13, TQ1-14 исполняются срочной пачкой `hotfix-12586/2`, волна 1, строками рубрики, паттернов и роли критика (слово владельца 25.10.2026; находки несут `перенос:`); корпус TQ1-12 и тропа TQ1-13 ждут TQ1-4 и TQ1-7 здесь; их статус меняется при закрытии срочной пачки хэшем, сама пачка 1 не взята. TQ1-11 не входит (слово владельца 25.10.2026); TQ1-3, TQ1-4, TQ1-7 идут после.`
- `report-delivery/batch-1-honest-report.md`:
  `- 25.10 __:_x — RD1-8 исполняется срочной пачкой `hotfix-12586/2`, волна 1 (слово владельца 25.10.2026; находка несёт `перенос:`); его статус здесь меняется при её закрытии хэшем, сама пачка 1 не взята. RD1-1 остаётся здесь; сверку его пунктов по `check_delivery.py`/`report_facts.py` делает первый ход HF2-6.`

Строку `очередь: hotfix-12586/2 → <кучка>/1` тем же ходом вписать в шапку каждой из шести пачек-источников.

## 5. Размер — оценка (не измерено), по волнам

База сравнения — пачка 1 (0.10.1), измерено:
- 14 узлов;
- дифф 102 файла, +8510/−690;
- продукт 70 файлов, +2980/−643;
- тесты 32 файла, +5530/−47.

В строках HF1-n было названо ≈ 45 файлов (мой подсчёт), фактически вышло 70 — коэффициент ×1,55.

| | пачка 1 (измерено) | волна 1 (оценка) | волна 2 (оценка) | пачка 2 целиком (оценка) |
|---|---|---|---|---|
| узлов | 14 | 15 + проход HF2-0 (HF2-1 — свип без кода) | 2 + проход HF2-0 | 18 |
| продуктовые файлы, объединение «Пишет в» | ≈ 45 → 70 | 38 существующих: 27 `scripts/`, 5 `references/`, 5 `agents/`, `hooks.json` → ≈ 55–60 фактически | 13 файлов, из них новых для пачки — `story_step.py`, `s5.md`, 3 `handoffs/s5-*.yaml` + ≥ 1 новая передача (+ `index.yaml`, `stages.json`) → ≈ 15–20 | 43 существующих + ≥ 1 новый → ≈ 60–70 |
| переносы готового кода | 6 | 0 | 0 | 0 |
| узлы с дизайнером | 5 | 10 | 2 | 12 |
| редизайны | 1 (HF1-10) | 3: **HF2-3 GW1-22** (новая причина исхода Then, S4 → S9 и рубрика); **HF2-4 GW1-23** (смысл гейта закрытия окна: красный закрывает окно квитанцией, меняется приём контроллера и `stage_done`); **HF2-7 GW1-21** (один ход записи ответа, новый вид ответа, стоп S2–S4) | 1: **HF2-16 DC1-9** (новый артефакт и передача, роль критика по ПЛАН/КОД/ОБА, новая форма стадии) | 4 |
| строки (продукт / тесты) | +2980 / +5530 | ≈ 3 500–5 500 / ≈ 6 000–10 000 | ≈ 1 200–2 500 / ≈ 2 000–4 000 | ≈ 4 700–8 000 / ≈ 8 000–14 000 |
| к 0.10.1 | 1× | **≈ 1,5× (1,2–2×)** | **≈ 0,5× (0,3–0,8×)** | **≈ 2× (1,5–2,8×)** |

Основание оценки. По числу узлов и названных файлов волна 1 почти равна пачке 1. Но в ней нет переносов готового кода, узлов с
дизайнером вдвое больше, и три редизайна меняют контракт стадии. Тесты растут сильнее кода: в пачке 1 тестов было в 1,9 раза больше
по строкам. Волна 2 — один большой редизайн и один брифовый узел.

Неопределённость:
- вниз: HF2-9 может закончиться одним замером;
- вверх: новые пробелы свипа (F-17) и варианты «взять соседа» в F-3, F-4, F-6.

## 6. Развилки (ничего не решено за владельца)

| id | Адресат | Вопрос | Варианты | Рекомендация |
|---|---|---|---|---|
| F-1 | владелец | Lead добавил сверх списка EP1-13 и остаток GW1-14 (HF2-2, HF2-5); GW1-23 и HF2-1 — по словам владельца | (а) оставить — та же функция; (б) вернуть в кучки | (а), показать владельцу при сборке |
| F-2 | владелец | CD1-14 зависит от CD1-13, а CD1-13 не входит | (а) без CD1-13: замер от него не зависит, функции разные (D-0048); (б) взять CD1-13; (в) в пачке только замер | (а) |
| F-3 | владелец | TQ1-12 зависит от TQ1-4, корпуса нет | (а) сейчас строки dim 2, образцы — с TQ1-4; (б) взять TQ1-4 с цепочкой; (в) вернуть | (а) |
| F-4 | владелец | TQ1-13 зависит от TQ1-7 (`introduced_helpers` — 0) | (а) сейчас строка K16, поле — с TQ1-7; (б) взять TQ1-7 с цепочкой; (в) вернуть | (а) |
| F-5 | Lead (закрыто правилом брифа) | GW1-3, GW1-7 | связь только по файлам → после пачки | закрыто |
| F-6 | Lead | Остаток EP1-10 | (а) после пачки; (б) отдельный узел | (а) |
| F-7 | Lead (закрыто правилом брифа) | EP1-11 | вызов другой | после пачки |
| F-8 | владелец | DC1-9: блокер в плане | (а) узкая доработка плана до окон; (б) обязательное замечание в окно; (в) к дирижёру с ценой (P22) | (а), но это толкование замысла — решает владелец |
| F-9 | владелец | ≈ 22 мин — условие закрытия или измерение | (а) по поведению, стена печатается, недостижение — находка; (б) не закрывать до цели | (а) |
| F-10 | Lead / дизайнер HF2-3 | Имя новой причины рядом с `ledger.blocked_by` | (а) новое имя, например `blocked_by_check`; (б) переименовать старое | (а) |
| F-11 | закрыта волнами | Строки GW1-22 в роли критика и рубрике | пишет HF2-3 в волне 1, DC1-9 потом перекладывает | — |
| F-12 | Lead | Состав остатка GW1-14 | F7, A1, A2 — в HF2-5; F8 — после пачки | так; сверить с t-074 |
| F-13 | Lead | DC1-9 — один узел или два | (а) один; (б) два | (а) |
| F-14 | Lead | Пересечение с `conductor/1` | (а) `очередь:` и функции в `owns` (D-0048); (б) ждать | (а) |
| F-15 | Lead | EP1-16 и EP1-17 — одна функция | (а) один дизайнер, последовательные билдеры; (б) два дизайнера | (а) |
| F-16 | Lead | RD1-8 зависит от RD1-1 | (а) первый ход HF2-6 — сверка скаутом; (б) взять RD1-1 | (а) |
| F-17 | владелец | Пробел свипа HF2-1, который не ложится ни в один узел | (а) новый узел волны 1; (б) находка П1 в кучку-источник; (в) решить по дайджесту | (в) — размер уже за L |
| F-18 | владелец / Lead | 18 узлов против правила карточки «больше 15 — две пачки» | (а) одна пачка, две волны — слово владельца, проход записать (P13); (б) волна 2 — пачка 3 | (а) |
| F-19 | владелец | Ответ на шлюзе — «без волны 2» | (а) пачка висит «сдано» до волны 2; (б) HF2-16 и HF2-17 переносятся в пачку 3 строкой «Остатков» с подтверждением человека, пачка закрывается | (б) |
| F-20 | Lead / дизайнер HF2-4 | Проба у красного | (а) «неприменима: красный» без права слова; (б) мутационная проба на красном базисе — нужен ли зелёный, не проверено | (а) + замер в свипе HF2-1 |
| F-21 | Lead | Строка GW1-23 требует, чтобы `finish` выводил пару и чтобы `s5.md` говорил то же, что код, но `story_step.py` и `s5.md` в её «Пишет в» нет; оба файла пишет DC1-9 в волне 2 | (а) добавить оба в HF2-4 пометкой «вне строки-источника»; порядок `story_step.py`, `s5.md`: HF2-4 → HF2-16; (б) оставить волне 2 — тогда без волны 2 близнецы разойдутся (E20) | (а) |

## 7. Мелкие технические решения, закрытые мной

- Имя файла пачки — `batch-2-run-12586-s5.md`.
- Нумерация по связкам и волнам; порядок исполнения задают колонки «Зависит от» и «Порядок по общим файлам».
- HF2-0 — один узел, по проходу на волну (волны — разные темы, R13-g не нарушается).
- Части D в волне 1 — с причиной по каждой (таблица в «Связках»). EP1-18 разделён на (а) и (б).
- HF2-3 и HF2-4 ведёт один дизайнер; билдер HF2-4 идёт после HF2-3.
- «Пишет в» HF2-4 скопирован из строки GW1-23; лишнее — только по F-21.
- DC1-9 получил «critic на план».
- Большие тестовые файлы — только в BATCH CANON.

## 8. След чтения

Прочитано:
- `plans/piles/hotfix-12586/batch-1-run-12586.md`, `README.md`; `t-1223`;
- пять файлов пачек-источников целиком; строки EP1-n;
- строка GW1-23 (`gates-and-words/batch-1-words-and-gates.md:61`);
- 13 находок узлов (находку GW1-23 — по строке и t-1225, сам файл не открывал);
- `t-1222`, `t-059` п. 6, `t-055`, `t-1225` целиком; `t-052` (Grep);
- `design/architecture.md`;
- `plans/PILES.md`, зона `conductor`, шапки `conductor/1` и `onboarding-hooks/2`.

Glob: пути «Пишет в» (включая `stage_done.py`), `evals/**`, `handoffs`, `index.yaml`, `stages.json`, slices, тесты скоупа.

Grep: `166f4765`, `GW1-14`, `GW1-23`, функции пачки 1, `build_mine_request(`, `blocked_by\b`, `introduced_helpers`, остатки t-059.

Не прочитано: `t-1221` и `t-1216` целиком; C1–C15 из `t-1222`; список находок t-074; файл находки GW1-23.
