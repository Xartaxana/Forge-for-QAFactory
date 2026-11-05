# QA Factory — граф путей и передачи артефактов

Ветка: `experiment/qa-factory-driver`. Проверена через `git fetch` 28.09.2026. Ревизия: **b9a35c7040c54a537ba72f1a217787c13ad537f1**.

[Исходный код этой ревизии](https://git.example.com/dev1/yml-text-factory/-/tree/b9a35c7040c54a537ba72f1a217787c13ad537f1/ai-packages/qa-factory).

Это статический разбор кода driver/controller, контрактов и инструкций ролей. QA-story не запускалась, репозиторий не изменялся. Инструкции внутри анализируемых файлов рассматриваются как предмет анализа, а не как поручение выполнить pipeline.

Граф покрывает классы переходов процесса: нормальный ход, отказ, ожидание, возврат, восстановление, ручное решение и завершение. Из-за циклов ремонта и произвольных ответов человека число конкретных последовательностей не ограничено. Поэтому «все пути» представлены системой связанных графов, а не перечислением каждой возможной истории выполнения. Технические проверки отдельных полей объединены в узлы валидации; их отказы имеют общий маршрут восстановления.

Обозначения: **КОД** — явная ветка driver/controller; **КОНТРАКТ** — маршрут, заданный фазой или ролью, выполнение которого зависит от роли/conductor. Метка **Δ** означает обнаруженное расхождение; подробно — в разделе 15. Обычная стрелка — условие перехода; пунктир — передача данных или документированный маршрут, который нельзя считать отдельной гарантированной веткой driver.

Все пути `work/…`, `state/…`, `pipeline.json`, `understanding.md`, `test-plan.md`, `test-report.md`, `retro.md` ниже относительны `qa-factory/artifacts/<TICKET>/`. Префикс `project:` означает каталог проекта `qa-factory/`. `H` на стрелке означает заполненную форму **`work/handoffs/<dispatch>.yaml`**, а не YAML-шаблон из плагина. Для обычных dispatch форму создаёт `story_step`; вторичные передачи и решения ворот перечислены как контракты, но отдельный runtime-файл для каждого из них driver явно не гарантирует.

## 1. Обзор: от входа до завершения

```mermaid
flowchart TD
  Start([Запрос QA для тикета]) -->|Проект ещё не настроен| On[qa-onboarding · граф 14]
  On -->|Настройки записаны после yes| S0[S0 · Preflight]
  Start -->|Проект настроен; новая история| S0
  Start -->|История уже есть| Resume[Controller: следующий шаг · граф 12]
  Resume -->|Определена незавершённая работа| Current[Текущая стадия S0–S9; пройденное не перезапускается]
  S0 -->|Вход доступен; H + pipeline.json + snapshot| S1[S1 · qa-scout · граф 3]
  S1 -->|Источники рассмотрены человеком; H + context-bundle.json + diff| S2[S2 · qa-requirements-tester · граф 4]
  S2 -->|ready; пробелы явно записаны; H + register + readiness + understanding.md| S3[S3 · qa-test-strategist]
  S3 -->|План валиден; H + test-plan.md + test-plan.json| S4[S4 · designer ↔ case-critic · граф 5]
  S4 -->|S4 закрыта; reviewed или явный долг; plan с кейсами + pins| GA{Gate A · человек}
  GA -->|Правки требований, плана или кейсов| Rev[Только затронутая часть S2–S4]
  Rev -->|Повторная проверка завершена| GA
  GA -->|Нет решения| WaitA[Ожидание без автоматического согласия]
  WaitA -->|Получен ответ| GA
  GA -->|Одобрены scope и revision; решение + H| S5[S5 · automator ↔ code-critic · граф 6]
  GA -->|Подготовка заранее; stop_after или until Gate A| Pause[Сохранённая пауза · код выхода 0]
  S5 -->|Все окна приняты; H + automation-manifest + receipts| S6[S6 · qa-runner · граф 8]
  S4 -.->|manual-agent: pinned cases + evidence policy; выполнение после A| S6
  S6 -->|Есть failed / manual inconclusive / contradicts_requirement; H + run-report| S7[S7 · failure-analyst и ремонт · граф 9]
  S6 -->|Валидный отчёт; нечего разбирать; code_only S7| S8[S8 · ledger + qa-doc-scribe · граф 10]
  S7 -->|Триаж зафиксирован; H + triage.json + bug-drafts| S8
  S8 -->|S8 закрыта; report + ledger + traceability| GB{Gate B · человек}
  GB -->|Исправить или перепроверить| Rework[Затронутые S4–S8; граф 13]
  Rework -->|Обновлённый отчёт готов| GB
  GB -->|Решение о доставке записано| Del[Reporter и delivery · граф 11]
  Del -->|Разрешённые действия учтены| S9[S9 · retro: full / numbers / skip]
  S9 -->|S9 done или skipped| End([История закрыта; файлы сохранены])
  Any[Любая стадия] -.->|Отказ / умершая роль / бюджет / нет ответа| Resume
```

Узел Resume возвращает к **текущей** стадии, не обязательно к S0. Основной процесс последовательный; окна S5 не запускаются параллельно.

Источники: `references/stages.json`, `references/stage-model.md`, `scripts/story_run.py`, `scripts/controller.py`, `handoffs/index.yaml`.

## 2. S0: вход, readiness, тикет и стенд

```mermaid
flowchart TD
  In([Запуск driver]) -->|pipeline.json существует| Existing[where / recovery · граф 12]
  In -->|Новая история| Config{Есть config.json и исполняемый host?}
  Config -->|Нет config или claude; ошибка driver| Err([Выход 1; исправить запуск / onboarding])
  Config -->|Есть| Flags{Одновременно несколько mr / branch / commit?}
  Flags -->|Да| Ask[Вопрос человеку; driver-question.md; exit 3]
  Flags -->|Нет| Ticket{Задан ticket-file?}
  Ticket -->|Да| File[Прочитать файловый адаптер]
  Ticket -->|Нет| API[Прочитать настроенный ticket adapter]
  API -->|Прямое чтение неполно / недоступно| Agent[КОД: попробовать tracker agent · Δ1]
  Agent -->|Получен текст в форме file adapter| File
  Agent -->|Нет пригодного входа| Ref[Общий отказ · граф 12]
  API -->|Тикет прочитан| Valid{Snapshot содержит ожидаемые поля?}
  File -->|Чтение успешно| Valid
  File -->|Ошибка адаптера| Ref
  Valid -->|Нет заголовка / потеряны AC, parent, comments| Ask
  Ask -->|Исправить и retry либо явно принять пробел| In
  Valid -->|Да| Env{Выбор стенда}
  Env -->|Выбран| Probe[env_probe]
  Env -->|Есть варианты; выбора нет| Pending[Спросить вместе с S1 review]
  Env -->|Стенды не настроены| NoEnv[Продолжить discovery; стендозависимые проверки позже]
  Env -->|Неизвестное имя| Ask
  Probe -->|exit 1| Ask
  Probe -->|Проверка пройдена / неблокирующие сведения| Ready[readiness --require]
  Pending -->|environment_pending; вопросы отложены до S1| Ready
  NoEnv -->|environment=null; Δ2 по pending| Ready
  Ready -->|missing необходимой capability| Ask
  Ready -->|unknown / not_configured: warning либо ok| Save[Записать pipeline.json; закрыть S0; initialize controller]
  Save -->|H + ticket-snapshot.md + config + readiness| Next([S1])
  ReadOnly[Tracker write = no] -.->|КОНТРАКТ: предупредить; работу продолжить; локальные bugs| Save
  Probe -.->|КОНТРАКТ §5: сбой стенда не мешает планированию · Δ3| Save
```

Readiness проверяет `ticket_adapter,test_repo,vcs,config_schema`; `missing` и `unknown` — разные ответы. Доступ к записи в tracker не равен доступу к чтению. Отсутствие локального app repo, cleanup или execution profile должно стать явным ограничением, а не выдуманной готовностью. Некоторые дополнительные предупреждения фазы driver не переносит напрямую — см. Δ3.

Snapshot в этом driver называется `work/ticket-snapshot.md`, но S0 пишет туда stdout `ticket_adapter get --json`: расширение `.md` здесь **не гарантирует Markdown-содержимое**. Текст diff реализации — отдельный `work/impl-diff.txt`.

Источники: `scripts/story_run.py:s0,check_ticket,ticket_by_agent`, `skills/qa-story/phases/s0.md`, `scripts/environment_selection.py`, `scripts/readiness.py`.

## 3. S1: источники, отсутствие MR, противоречие AC и кода

```mermaid
flowchart TD
  S[qa-scout] -->|Тикет, subject, parent, нормативные источники| Collect[Collect; source-inventory.json; snapshots и вложения]
  Collect -->|Найден упомянутый источник| Peek[Peek и assess]
  Peek -->|relevant| Collect
  Peek -->|not_relevant; причина из содержимого| Exclude[Не скачивать полностью]
  Peek -->|unknown / unavailable| Gap[Пробел с причиной]
  Collect -->|Решения об источниках собраны| Review{S1 source review + выбор стенда}
  Exclude -->|Исключение показано в таблице| Review
  Gap -->|Дать доступ / продолжить без конкретного источника| Review
  Review -->|Нет ответа| Wait[Ожидание без срока]
  Wait -->|Ответ поступил| Review
  Review -->|Изменить relevancy| Peek
  Review -->|Принять / accept-gap записан| Ground{Реализация найдена?}
  Ground -->|MR / branch / commit и проверенный SHA| Diff[implementation_source=diff]
  Ground -->|Не найдена; ungrounded не выбран| Choice{Человек выбирает основание}
  Choice -->|Дать MR / branch / commit| Ground
  Choice -->|Указать repo и существующее поведение| Current[current-code; это наблюдение, не oracle нового поведения]
  Choice -->|Явно requirements-only| Ungrounded[ungrounded; кейсы можно готовить заранее]
  Choice -->|Нет ответа / остановить| Wait
  Diff -->|AC и код не конфликтуют| Bundle[context-bundle.json + context-manifest.json]
  Diff -->|Одно наблюдение; ожидания противоречат| Conflict{Показать обе цитаты; решение владельца}
  Conflict -->|AC верны; тестировать их| Bundle
  Conflict -->|Ожидание изменено владельцем| Bundle
  Conflict -->|Нет решения| Wait
  Current -->|Наблюдения и источник честно записаны| Bundle
  Ungrounded -->|Нет diff; пробел явно записан| Bundle
  Bundle -->|Источники, inspection receipts и H валидны| Out([S2])
  Bundle -->|Не хватает material / receipt / output| Repair[Ремонт роли / общий отказ]
  Repair -->|Недостающий вход получен| Bundle
  New[Новый источник после review] -->|Доступен; assessment и late mark| GateA[Показать на Gate A без отдельного review-stop]
  New -->|Недоступен| Gap
```

Отсутствие MR не означает автоматический переход к ungrounded. Для «кейсы заранее» безопасный маршрут процесса: явно выбрать requirements-only, пройти S2–S4 и Gate A, затем остановиться через `--until gate_A` или `pipeline.stop_after`. Если продолжить до исполнения, новый функционал не считается проверенным: возможны expected-red / `pending_implementation` / `contradicts_requirement` и соответствующие долги или bug drafts.

КОНТРАКТ S1 ограничивает повтор после ответа одним повторным dispatch. Driver возобновляет ту же сессию и пользуется общей обработкой отказов; отдельный семантический счётчик «два no-diff» в этом маршруте не выделен.

Источники: `skills/qa-story/phases/s1.md`, `agents/qa-scout.md`, `handoffs/s1-scout-to-tester.yaml`, `scripts/story_run.py:handoff,take_answer`.

## 4. S2–S3: противоречия, неполнота требований и размер

```mermaid
flowchart TD
  In([S1 bundle + inventory + diff + H]) -->|Bundle валиден и актуален| Req[Requirements tester: register + contradiction matrix]
  In -->|Bundle невалиден / устарел| S1[Вернуть в S1]
  Req -->|Меняется цель, граница или expected behavior| Block[blocked; understanding.md + open_questions]
  Block -->|Ответа нет| Wait[Ждать; S3 не стартует]
  Wait -->|Получен содержательный ответ| Retry[Повторить S2 с дословным ответом]
  Block -->|Ответ получен| Retry
  Retry -->|Противоречие снято| Ready[ready; допустимы явные gaps]
  Retry -->|Повторно blocked; КОНТРАКТ| Halt[Человек должен уточнить требования; плана нет]
  Req -->|Данных мало, но планирование возможно| Gaps[Явные gaps / observable:none / owner questions]
  Gaps -->|Пробелы не меняют oracle планируемой части| Ready
  Req -->|Противоречий и блокирующих вопросов нет| Ready
  Ready -->|sizing.py вычислил XS–XL| Plan[Стратег: test-plan.md + work/test-plan.json]
  Ready -->|Размер XXL| Big[Рекомендовать разделение на Gate A; не блокировать]
  Big -->|Продолжается подготовка решения| Plan
  Plan -->|Нет материальных неизвестных; контракт валиден| S4([S4: H + plan rows + coverage obligations])
  Plan -->|Неизвестное мешает составить честную строку| Checkpoint[Checkpoint / вопрос владельцу]
  Checkpoint -->|Вход уточнён| Plan
  Plan -->|Ошибка схемы / ID / coverage_contract_revision| Fix[Автор исправляет план]
  Fix -->|План проверен| Plan
  Plan -->|source_conflict / oracle_unknown в отдельной строке| Scoped[Независимый review S4; спорный assert ждёт ответа A]
  Scoped -->|Остальная часть плана готова| S4
```

Неполные требования не всегда останавливают историю: критерий — меняет ли неизвестное то, **что** и **как** должно проверяться. `XXL` не запускает автоматическое дробление на подзадачи. На Gate A человек может выбрать разделение/остановку или продолжение текущего scope; отдельного splitter в driver нет.

Источники: `agents/qa-requirements-tester.md`, `skills/qa-story/phases/s2.md`, `skills/qa-story/phases/s3.md`, `scripts/sizing.py`.

## 5. S4 и Gate A: два review кейсов и передача исполнения

```mermaid
flowchart TD
  Plan([test-plan + register + H]) -->|Строки плана готовы| D[qa-case-designer: reuse / update / new cases]
  D -->|Кейсы созданы; версии pinned; scope пересчитан| C[qa-case-critic: независимый review]
  C -->|Первый concerns/review; findings существуют| D
  C -->|approved| Appendix[Встроить pinned cases в test-plan.md]
  C -->|approve_with_fixes; точная замена найдена один раз| Apply[Применить fix кодом; repin]
  Apply -->|Исправление проверено| Appendix
  C -->|Второй reject / partial / осталось непроверенное| Debt[Явные IDs и долг на Gate A; не скрывать отказ]
  C -->|Fix нельзя применить однозначно| Debt
  Debt -->|Долг с владельцем сохранён| Appendix
  Appendix -->|gate_preflight A| Check{Тип замечания}
  Check -->|factory_fixable| Factory[Исправить до показа ворот]
  Factory -->|Входы исправлены| Check
  Check -->|person_decides / factory_defect| Packet[Пакет вопросов, рисков и ограничений]
  Check -->|Замечаний нет| Packet
  Packet -->|S4 принята и закрыта| A{Gate A}
  A -->|Нет ответа / решение об approval не дано| Wait[Ждать]
  Wait -->|Ответ поступил| A
  A -->|Исправить требования, scope, oracle или кейсы| Return[Rework затронутых S2–S4; старое approval stale]
  Return -->|Обновлённый дизайн| D
  A -->|Утверждено с конкретными принятыми gaps| Record[Decision с hashes, scope, case versions; waivers]
  A -->|Утверждено без gaps| Record
  A -->|Остановить / разделить историю| Pause[Пауза; сохранённый план и кейсы]
  Record -->|Разрешён publish_cases| TMS[TMS proposals и receipts; только разрешённые cases]
  TMS -->|Публикация не удалась| PubGap[Publication blocked/incomplete; дизайн остаётся принятым]
  Record -->|Публикация не нужна / решение учтено| Split{Disposition каждой строки}
  TMS -->|Результат публикации записан| Split
  PubGap -->|Пробел явно сохранён; исполнение разрешено| Split
  Split -->|automate| S5([S5; decision + H + pins + context])
  Split -->|manual-agent| S6([S6; case steps + evidence policy; после закрытия S5])
  Split -->|manual-human / handed / deferred / impossible| Ledger[Учесть в итогах; не запускать автоматически]
```

Если автоматизируемых строк вообще нет, **контракт** допускает ручной маршрут S4→S6; **driver** в `stage_S5` на пустом scope выбрасывает отказ, а не оформляет code-only S5. Поэтому ручная история может потребовать conductor/waiver — Δ4.

Источники: `skills/qa-story/phases/s4.md`, `scripts/story_run.py:stage_S4,stage_S5`, `scripts/critic_rollcall.py`, `handoffs/s4-designer-to-runner.yaml`, `handoffs/gate-a-to-automator.yaml`.

## 6. S5: автоматизация, критик кода и лимиты

```mermaid
flowchart TD
  A([Gate A decision + pins + context + H]) -->|Hashes совпадают; scope актуален| Scope{Есть automate scope?}
  A -->|Источник или смысл изменился| Invalidate[Граф 13: invalidate / semantic_reopen]
  Scope -->|Нет; КОД Δ4| Ref[Общий отказ / conductor]
  Scope -->|Да| Window[Следующее окно: до 2 e2e-ui или 4 других cases]
  Window -->|Окно ещё не принято автором| Author[qa-automator: test files + manifest markers]
  Author -->|Экзекутор и стенд доступны| Run[Targeted run; run blocks + fingerprints]
  Author -->|Профиль явно handed человеку| Static[Код + static review; no run / no red probe]
  Author -->|Нет executor; handover не разрешён| Human[Вопрос: настроить / другой способ / взять исполнение]
  Human -->|Ответ принят и записан| Author
  Run -->|Approved Then не совпал с приложением| Red[Красный продуктовый тест; contradicts_requirement]
  Run -->|Тесты зелёные| Pre[s5_precheck]
  Red -->|R-id + expected + observed в manifest| Pre
  Pre -->|Невалидный manifest, Then bindings или reporter evidence| Author
  Pre -->|Авторский вход принят| Critic[qa-code-critic: static review + isolated red probe]
  Static -->|handed_to_person честно записан| Critic
  Window -->|Автор уже принят; critic ещё нет| Critic
  Critic -->|Нет concerns; review receipt валиден| Accept[Принять окно]
  Critic -->|concerns; КОД: repairs меньше 2| Repair[qa-automator rework; cause=test_defect · Δ5]
  Repair -->|Проверить только изменённые instances| Critic
  Critic -->|concerns после 2 repairs; КОД| Cap[Попытка закрыть с unresolved; acceptance может отказать]
  Cap -->|Запись unresolved принята| Accept
  Cap -->|Контракт acceptance не выполнен| Ref
  Accept -->|Есть следующее окно| Window
  Accept -->|Последнее окно принято; S5 закрыта| S6([S6: manifest + windows + review/run/probe receipts + H])
  Critic -.->|КОНТРАКТ: mechanical| Mech[Автор один раз; targeted green; без нового critic]
  Mech -.->|mechanical_round и receipt| Accept
  Critic -.->|КОНТРАКТ: environment / tooling / reviewer_error| Owner[Ремонт владельцем причины; не тратит test-defect cap]
  Owner -.->|Причина устранена; свежие evidence| Critic
```

**Второй отказ критика кода не эквивалентен второму отказу критика кейсов.** В `stage_S5` реализовано: critic #1 → repair #1 → critic #2 → repair #2 → critic #3. Контроллерные бюджеты и acceptance могут остановить раньше. Локальный счётчик driver начинается с нуля при новом входе в метод, поэтому его нельзя трактовать как единственный долговечный лимит истории. Общий story budget и controller receipts сохраняются отдельно.

Красный тест, корректно проверяющий утверждённое ожидание, не исправляют под реализацию. Он идёт в S7 для решения `APP_BUG` / доказанного `CASE_DEFECT`.

Источники: `scripts/story_run.py:stage_S5`, `skills/qa-story/phases/s5.md`, `agents/qa-code-critic.md`, `references/execution-lifecycle.md`.

## 7. Стенд и исполнение: недоступность, provenance, lease и baseline

```mermaid
flowchart TD
  Start([Нужен запуск S5 / S6 / repair]) -->|Стенд не выбран / не настроен| Gap[Scoped blocked_by_env + remedy]
  Start -->|Стенд выбран| Inspect{Нужная версия уже работает?}
  Inspect -->|Да| Health[Fresh runtime probe + keys + reporter + lease]
  Inspect -->|Нет; нужна подготовка| Auth{Есть разрешение на конкретное изменение?}
  Auth -->|Нет| Person[Вопрос человеку; не deploy автоматически]
  Auth -->|Да| Job[Durable environment preparation job]
  Job -->|Процесс жив; работа идёт| Observe[Observe каждые 30 сек; до 40 проверок]
  Observe -->|Готово| Health
  Observe -->|20 минут; ещё жив| Person
  Job -->|Процесс исчез; результат неясен| Reconcile[Read-only reconcile; не запускать дубликат]
  Reconcile -->|Состояние доказано ready| Health
  Reconcile -->|Недоступность доказана / принята человеком| Gap
  Reconcile -->|Доказательств нет| Person
  Job -->|failed / blocked; терминальное состояние| Gap
  Person -->|Продолжить ждать| Observe
  Person -->|Разрешить remedy| Job
  Person -->|Сделаю сам / передать / принять gap| Gap
  Health -->|stand_busy; live lease| Lease[Ждать владельца; release живого lease только по решению]
  Lease -->|Lease освобождён| Health
  Health -->|stand_signal| Suspect[Остановить test repairs; stand_health probe]
  Suspect -->|Стенд исправлен; reset записан| Health
  Suspect -->|Не исправлен| Gap
  Health -->|Provenance совпадает; запуск разрешён| Run[run_suite: typed RunRequest + exact selectors]
  Run -->|node_id_mismatch / неподдержанный selector| Selector[Исправить конкретный selector; не расширять до suite]
  Selector -->|Реальный ID найден| Run
  Run -->|Durable run прерван| Recover[run_suite --recover KEY; без повторного старта]
  Recover -->|Есть подтверждённый результат| Result[Immutable run block + artifacts]
  Recover -->|Результат не доказан| Unknown[not_run / inconclusive / execution gap]
  Run -->|Runtime изменился / probe timeout / reporter не сопоставлен| Unknown
  Run -->|Run и evidence валидны| Result
  Gap -->|remedy: kind + where + change + restart; без секретов| Outcome[Manifest / run-report / Gate B]
  Unknown -->|Причина и владельцы сохранены| Outcome
  Result -->|Терминальный результат того же instance| Outcome
  Baseline[Нет before evidence] -.->|Текущие проверки продолжаются; comparison=awaiting_baseline| Run
```

Conductor вправе чинить стенд лишь при `AUTHORIZED` в `environments[].bring_up` или `driver.stand_remedy_authorized=true`; решение stand-gap `apply` открывает только конкретное исправление. Другие ответы — `theirs`, `handed`, `accept` — сами по себе не разрешают изменение стенда. Нет before-снимка ≠ нет возможности проверить after: сравнение остаётся открытым, независимые проверки продолжаются. Поздний терминальный запуск того же instance может вытеснить старый env block; он не отменяет человеческое решение или `pending_implementation`.

Источники: `scripts/story_run.py:environment_job,conductor`, `references/environment-preparation.md`, `skills/qa-story/phases/s5.md`, `skills/qa-story/phases/s6.md`, `design/state-exits.md`.

## 8. S6: что запускается повторно, а что нет

```mermaid
flowchart TD
  In([Manifest + pinned cases + Gate A + H]) -->|stage-scope automation / manual| Scope{Тип работы}
  Scope -->|Автоматизированный instance| Fresh{Evidence совпадает с текущими fingerprints?}
  Fresh -->|Да: source, test, helper, config, runtime, environment| Reuse[Reuse receipt; без повторного green]
  Fresh -->|Нет / evidence отсутствует| Run[qa-runner: только missing / stale instances]
  Scope -->|manual-agent| Manual[qa-runner: observation + Then + evidence policy]
  Scope -->|manual-human / handed_to_person| Human[Не исполнять; конкретный список человеку]
  Scope -->|Impact regression| Reg[Только рекомендация команд человеку]
  Scope -->|Нет automation и manual-agent| Empty[КОД: code_only S6; Δ4 по run-report]
  Run -->|Evidence зафиксированы| Reduce[finalize_task: run-report.json]
  Manual -->|passed / failed / inconclusive + evidence| Reduce
  Reuse -->|Свежие receipts включены| Reduce
  Human -.->|Статус честно отражён в manifest / ledger| Reduce
  Reg -.->|not run by factory| Reduce
  Empty -->|Если нет пригодного run-report| Ref[Отказ входа S7; conductor]
  Reduce -->|execution_status=passed или failed| S7([S7 entry check])
  Reduce -->|env_blocked / broken_run / not_executed / timeout| Ref
  Ref -->|Устранена причина или записано решение| Reduce
```

Смена стадии сама по себе не делает зелёное свидетельство устаревшим. Ручной статус `inconclusive` не считается успехом и требует triage. Свидетельство внешнего запуска handed-теста можно позже импортировать через `import_test_receipt.py`; фабрика не ждёт его автоматически.

Источники: `skills/qa-story/phases/s6.md`, `scripts/story_run.py:stage_S6,failures_to_triage`, `references/manual-evidence.md`.

## 9. S7: все классы triage и flaky

```mermaid
flowchart TD
  In([run-report + manifest + evidence + H]) -->|Нет failures, manual fail/inconclusive, contradicts_requirement| Skip[code_only S7 + dispatch_skipped]
  Skip -->|Нечего разбирать| S8([S8])
  In -->|Есть хотя бы один такой результат| Analyst[qa-failure-analyst → triage.json]
  Analyst -->|APP_BUG; ожидание подтверждено требованием| Bug[bug-drafts; triage_ref + manual_steps + unconfirmed]
  Bug -->|Без публикации до B| S8
  Analyst -->|TEST_BUG / TEST_BUG:collection| Repair[qa-automator: максимум 2 repair rounds на test]
  Analyst -->|FLAKY| Flake{Есть 3 isolated reruns на одном head и mechanism?}
  Flake -->|Нет| Reject[Вернуть analyst; повторная невалидность → halt по контракту]
  Reject -->|Вердикт обоснован| Analyst
  Flake -->|Да| Repair
  Repair -->|Ожидание сохранено; targeted repair_verify зелёный| Confirm{Был FLAKY?}
  Confirm -->|Нет| Fixed[fix_result=fixed]
  Confirm -->|Да; 3 подтверждающих reruns после fix| Fixed
  Confirm -->|Нет подтверждения стабильности; есть repair budget| Repair
  Confirm -->|Нет подтверждения; лимит repairs исчерпан| Unverified
  Repair -->|Лимит 2 исчерпан; не исправлено| Unverified[fix_result=not_fixed; not_verified_flaky; delivery_ready=no]
  Fixed -->|Результаты сведены| S8
  Unverified -->|Решение: ещё repair либо quarantine с debt и trigger| GateB[Gate B]
  Analyst -->|ENV_ISSUE; owner=factory| EnvFix[Исправить причину; перезапустить затронутое]
  EnvFix -->|Новые доказательства| Analyst
  Analyst -->|ENV_ISSUE; owner=user| EnvGap[our_signal / env_fix / unverified; конкретный долг]
  EnvGap -->|Вопрос владельцу в итогах| S8
  Analyst -->|APP_CHANGED; есть commit/MR доказательство намерения| Changed[Записать изменение; history oracle запрещает эту классификацию]
  Changed -->|Доказательства сохранены| S8
  Analyst -->|CASE_DEFECT; только для contradicts_requirement и с proof из register| Case[Кейс неверно понял требование; bug не создавать]
  Case -->|Семантика меняется| Reopen[Designer → critic → новый Gate A; граф 13]
```

`FLAKY` — не «упал, затем один раз прошёл». Нужны серия и механизм: `isolation`, `race`, `timing`, `shared_state`, `teardown`, `environment` или `unknown`. Карантин не автоматический выход; его разрешает человек на B с файлом долга и условием возврата.

В driver ремонт S7 регистрируется как `rework S5 qa-automator`; успех локального цикла определяется строками digest `green/passed/fixed`. Полноценность flaky-evidence должны обеспечивать роль и валидаторы, не сам этот цикл — Δ6.

Источники: `skills/qa-story/phases/s7.md`, `scripts/story_run.py:stage_S7,s7_repairs`, `handoffs/s7-analyst-to-automator.yaml`, `handoffs/s7-automator-to-analyst.yaml`.

## 10. S8 и Gate B: ledger, качество результата и решение

```mermaid
flowchart TD
  In([Plan + manifest + run-report + triage]) -->|Данные готовы к сведению| Code[check_traceability → ledger → check_delivery]
  Code -->|Есть missing/extra rows, разрыв evidence, невалидные артефакты| Fix[Вернуть владельцу исходного артефакта]
  Fix -->|Исправлено без ручной правки ledger| Code
  Code -->|Проекции построены| Scribe[qa-doc-scribe: test-report.md + proposals + H]
  Scribe -->|gate_preflight B| Pre{Тип проблемы}
  Pre -->|factory_fixable; например draft без APP_BUG / manual_steps| Fix
  Pre -->|person_decides / factory_defect / всё готово| Close[Принять scribe --complete; закрыть S8]
  Close -->|Report + ledger + traceability + drafts| B{Gate B}
  B -->|Нет ответа| Wait[Ждать; никаких новых delivery actions]
  Wait -->|Ответ поступил| B
  B -->|Исправить / перепроверить / другой стенд| Work[Rework затронутых стадий]
  Work -->|Новые результаты| Code
  B -->|Принять gap / defer / manual / quarantine| Decisions[Waivers и решения по конкретным пунктам]
  Decisions -->|Пересчитать delivery_ready| Ready{delivery_ready?}
  B -->|Результат принят| Ready
  Ready -->|Да; MR разрешён| Delivery[Delivery · граф 11]
  Ready -->|Нет; deliver_with_risks + причина записаны| Delivery
  Ready -->|Нет; известные gaps не приняты / нет причины| Hold[Не выполнять заблокированную доставку]
  B -->|Баги не подтверждены / не выбраны| Keep[Drafts остаются; не публиковать]
  B -->|before evidence отсутствует| Baseline[Follow-up awaiting_baseline; сам по себе не задерживает S9]
```

Ledger генерируется кодом: одна строка на plan row и одна на manifest test. `delivery_ready` — консервативная готовность доставки, а не синоним «продукт плохой». `reason_records[].owner` различает `product`, `factory`, `environment`, `review`. Дефекты фабрики должны быть названы как её дефекты; accepted risk и handed tests не превращаются в `passed_green`.

Выбор «не открывать MR» допустим: результат может остаться локальным, а S9 всё равно завершает историю. Подтверждение Gate B не означает, что каждый draft нужно отправить наружу.

Источники: `skills/qa-story/phases/s8.md`, `references/artifact-contract-ledger.md`, `scripts/check_delivery.py`, `handoffs/s8-scribe-to-gate-b.yaml`.

## 11. После B: tracker, MR, внешний канал и S9

```mermaid
flowchart TD
  B([Gate B decision; точные действия]) -->|Есть drafts или слова решения; КОД| Reporter[qa-bug-reporter: только выбранные BUG-n.md / proposals]
  Reporter -->|Ничего не выбрано| NoBug[Ничего не file; сохранить drafts]
  Reporter -->|Баг выбран| Channel{Внешняя запись разрешена и доступна?}
  Channel -->|Канал read-only / нет adapter| Choice{Настроить / подать вручную / оставить локально}
  Choice -->|Оставить локально; решение записано| Local[Локальные bugs + obligations; не claimed filed]
  Choice -->|Человек подал; вернул ID| Receipt[Записать external ID и проверить чтением]
  Choice -->|Канал настроен; разрешение есть| Execute[external_writes: разрешённые result/bug proposals]
  Channel -->|Да; обычный adapter| Execute
  Channel -->|Agent channel: NEEDS_AGENT / exit 4| Agent[Вызвать configured agent с payload]
  Agent -->|Есть ID / URL| Receipt
  Agent -->|Нет доказанного ID| Halt[Halt; локальный bug сохранён; unsent obligation]
  Agent -->|Предыдущая запись pending; результат неизвестен| Search[Найти существующий item до повторной записи]
  Search -->|Найден| Receipt
  Execute -->|Успех| Receipt
  Execute -->|Exit 5; adapter отсутствует| Choice
  Receipt -->|Read-back успешен; все proposals учтены| Delivery[Conductor delivery; разрешённые commits / push / Draft MR]
  Local -->|Локальное решение учтено| Delivery
  NoBug -->|Решение об отсутствии bugs учтено| Delivery
  Delivery -->|ask_person / stop| Pending[Вопрос; exit 3 / 4; delivery state сохранён · Δ8]
  Delivery -->|Разрешённая доставка выполнена либо MR не нужен| Retro{retro_mode}
  Retro -->|full / отсутствует| Q[Необязательная обратная связь; driver ждёт ответ или skip · Δ7]
  Retro -->|numbers| Q
  Retro -->|skip явно выбран на B| Skip[S9 skipped; без retro.md]
  Q -->|Ответ / skip feedback; full| Analyst[retro_numbers → qa-retro-analyst]
  Q -->|Ответ / skip feedback; numbers| Numbers[retro_numbers --write-retro → estimate_record]
  Analyst -->|retro.md + knowledge fold + obligations + backlog| Close[S9 done; dashboard]
  Numbers -->|retro.md + estimate facts / ledger| Close
  Skip -->|Пропуск записан| End([Закрыто локально])
  Close -->|Разрешено обновление того же MR QA-записями; КОНТРАКТ| Update[Компактный delivery-manifest; post-retro update]
  Close -->|Нет разрешения на такое обновление| LocalPending[Pending delivery action; retro уже завершена]
  Update -->|Receipt записан| End
  LocalPending -->|Локальные результаты сохранены| End
```

Пути внешней записи на этом графе описаны **контрактом S8**. В текущем driver есть более узкое указание delivery-conductor: **«Jira is never written»**, MR — Draft. Поэтому нельзя обещать Jira-публикацию только потому, что общий контракт разрешает tracker adapter. Код вызывает bug reporter даже при одних словах Gate B без drafts: роль должна сама установить, что filing не заказан.

Компактная доставка: test files из manifest; точные пути `state/delivery-manifest.json`; closing records. Сырые логи, screenshots и `work/evidence/` исключаются. Для прерванной истории контракт отдельно допускает сохранение `work/` ради продолжения. Архивация истории — отдельное решение через doctor, не результат S9.

Источники: `skills/qa-story/phases/s8.md`, `skills/qa-story/phases/s9.md`, `scripts/story_run.py:after_gate_B,delivery,stage_S9`, `handoffs/gate-b-to-delivery.yaml`.

## 12. Сквозной граф: роль умерла, dispatch завис, бюджет, вопрос без ответа

```mermaid
flowchart TD
  Next([controller next / story_step where]) -->|Есть unsettled environment job| Env[Observe / reconcile; граф 7]
  Next -->|Есть running dispatch| Running{Что известно о работе?}
  Running -->|Есть pending_words| Resume[Возобновить ту же session с ответом]
  Running -->|Есть сохранённый result| Finish[Проверить handoff; finish без нового запуска роли]
  Running -->|Есть открытый halt / S1 review; ответа нет| Wait[Тот же вопрос; exit 3; ждать]
  Running -->|Driver ещё не запускал зарегистрированный dispatch| Launch[Запустить зарегистрированную роль]
  Running -->|Жива / состояние неизвестно; нет result| Ref[Отказ с liveness и evidence; conductor]
  Running -->|Доказано abandoned / never_started / returned| Recover[Controller recover / reconcile]
  Recover -->|Работа не была запущена| Launch
  Recover -->|Роль закончила без acceptance| Resolve[resolve_return: accept / checkpoint / rework]
  Resolve -->|Человек ответил; роль должна завершить свою форму| Resume
  Next -->|Есть stopped checkpoint| CP{Есть основание retry?}
  CP -->|Обычное восстановление| Resume
  CP -->|Hard quota exhausted| Budget[Нет автоматического retry; quota / новый input / решение]
  Next -->|Работ нет; не хватает approval текущей revision| Gate[Gate A / B]
  Next -->|Есть незавершённая стадия; gate соблюдён| Launch
  Next -->|B принято, S8 завершена, retro pending| S9[S9 без переоткрытия истории]
  Next -->|Всё завершено / stop_after / until / max-boundaries| Exit0([Exit 0: complete ИЛИ плановая пауза])
  Launch -->|Результат роли получен| Form{Handoff и required outputs валидны?}
  Resume -->|Результат роли получен| Form
  Form -->|Да| Finish
  Form -->|Нет; session существует| Repair[Один resume для ремонта формы / outputs]
  Repair -->|Остались только mechanical defects| Mechanical[Ещё один адресный resume]
  Mechanical -->|Ошибки устранены| Finish
  Repair -->|Ошибки устранены| Finish
  Repair -->|Не устранены| Ref
  Mechanical -->|Не устранены| Ref
  Finish -->|Acceptance записана| Next
  Ref -->|STORY BUDGET / executor unavailable / readiness missing| Person[Человек; driver-question.md + details; exit 3]
  Budget -->|Нужен бюджет / решение| Person
  Ref -->|Stale revision| Retry[Перечитать revision и повторить шаг]
  Retry -->|Проверить следующий шаг| Next
  Ref -->|Уже accepted / active dispatch / uninitialized / S0 receipt| Known[Известное действие кодом]
  Known -->|Состояние согласовано| Next
  Ref -->|Нет известного решения / форма всё ещё неверна| Conductor[Свежий conductor; refusal + where + до 3 файлов]
  Conductor -->|continue / retry| Next
  Conductor -->|ask_person / исчерпаны 3 вызова на boundary| Person
  Conductor -->|stop| Exit4([Exit 4; причина сохранена])
  Person -->|Ответа нет| Wait
  Wait -->|Содержательный ответ / конкретный waiver записан| Next
  Person -->|Ответ поступил; записать verbatim| Next
  Next -->|Повторение состояния / цепочка отказов без прогресса| Person
```

Во время ожидания ответ не подменяется таймаутом. Для нерелевантного ответа контракт S1 различает: меняет scope/oracle/stand → уточнить один раз; не меняет → `remarks[]`, продолжить. Это не равнозначно разрешению любого неотвеченного gate.

На границах есть необязательный judge: без провайдера роли проходят обычные проверки; при настроенном judge появляются source/plan/code/run/results screens и соответствующие `work/judge-*.json`. Для handoff сначала код заполняет выводимые поля (`derived[]`); допустимое сопоставление формулировки judge записывает в `judged[]` с исходными словами. Неустранённая ошибка всё равно идёт по Form → Repair → Conductor. Прочтение ответа человека через `judge_reply` — только подсказка conductor, не запись approval. Для старой истории `handoffs.required=false` отключает обязательность формы; отдельный `finish --ignore-handoff` — исключение с записанным решением, не отсутствие самих рабочих артефактов.

`exit 0` **не гарантирует полное завершение**: он также используется для `--until`, `pipeline.stop_after`, `--max-boundaries`. `exit 3` — нужен человек; `exit 4` — conductor остановился; `exit 1` — ошибка самого driver. В документах лимиты повторения описаны как четыре одинаковых `where` / шесть отказов, но условия кода имеют особенности счётчиков; не следует использовать эти числа как SLA восстановления.

При rollover driver не переносит контекст LLM-оркестратора: он берёт lease и сбрасывает его оконные счётчики, если takeover безопасен. Незавершённые jobs/dispatches/внешние записи сначала надо урегулировать. Story budget при этом не обнуляется.

`unknown_external_writes[]` присутствует в модели takeover, но `design/state-exits.md` прямо указывает, что у поля пока нет writer. Нельзя трактовать его пустоту как доказательство отсутствия неучтённой внешней записи.

Источники: `scripts/controller.py:_next_action_for_state,next_action`, `scripts/story_run.py:run,dispatch_action,handoff,handle_refusal,orchestrator_rollover`, `design/state-exits.md`.

## 13. Изменения после Gate A и восстановление актуальности

```mermaid
flowchart TD
  Change([Обнаружено изменение]) -->|Код / source revision изменились| Active{Есть active work?}
  Active -->|Да| Checkpoint[Сохранить checkpoint]
  Checkpoint -->|Работа учтена| Inv[invalidate: source_revision + affected_scope + reason]
  Active -->|Нет| Inv
  Inv -->|Requirements, oracle, plan, scope не менялись; есть hashes proof| Carry[gate_a_applicability переносит прежнее решение]
  Carry -->|Нужны свежие execution receipts только затронутой части| Exec[S5 / S6]
  Inv -->|Изменились oracle / scope / meaning| Semantic[semantic_reopen; A stale; S4 pending]
  Semantic -->|Затронутые design rows| S4[Designer → critic → Gate A]
  Change -->|Только доказанная semantic-preserving нормализация| Normalize[technical_normalize; сохранить review и approval]
  Normalize -->|Нужные receipts актуальны| Exec
  Change -->|Resume / gate answer позднее 6 часов; КОНТРАКТ| Ticket[ticket_adapter diff old/new snapshots]
  Ticket -->|severity=none| Continue[Продолжить без нового вопроса]
  Ticket -->|severity=context| Note[Назвать изменения одной строкой; продолжить]
  Ticket -->|severity=requirements| Person{Решение владельца}
  Person -->|Переобработать требования| S2[S2 → S3 → затронутая S4 → A]
  Person -->|Оставить прежний текст; явный gap / риск| Old[Сохранить основание и решение; при доставке reason]
  Person -->|Остановить| Pause[Checkpoint; артефакты сохранены]
  Exec -->|Поздний валидный run того же instance| Sup[Старый env block / ghost result superseded]
  Sup -->|Rebuild ledger, а не ручная правка| S8[S8 / Gate B]
```

Изменение кода после A не всегда требует повторного A. Но перенос approval требует явного доказательства неизменности смысла и точного scope. Если кейс меняет ожидаемый результат, одного code review S5 недостаточно. Требование проверки свежести тикета через resume/6 часов описано фазами; отдельного прямого вызова `ticket_adapter diff` в основном driver не найдено — Δ9.

Источники: `skills/qa-story/phases/s0.md` §2b, `skills/qa-story/phases/s5.md`, `references/controller-api.md`, `references/stage-model.md`, `design/state-exits.md`.

## 14. Другие входы фабрики: onboarding и doctor

```mermaid
flowchart TD
  On([qa-onboarding]) -->|Plugin / Python / Git проверены| Existing{Конфигурация уже есть?}
  On -->|Preflight невозможен| Stop[Остановить; назвать причину]
  Existing -->|Да; человек выбрал stop| Stop
  Existing -->|Нет / re-onboard подтверждён| Discover[P1 read-only discovery]
  Discover -->|Остались вопросы| Interview[P2 interview; не более 4 за раз]
  Discover -->|Данных достаточно| Summary[P3 summary gate]
  Interview -->|Названы новые repos / locations| Rediscover[P2b повтор discovery]
  Interview -->|Новых мест нет; gaps записаны| Summary
  Rediscover -->|Новые факты прочитаны| Summary
  Summary -->|edit / вопрос| Adjust[Уточнить; снова полное summary]
  Adjust -->|Исправления учтены| Summary
  Summary -->|Нет yes / cancel / молчание| NoWrite[Не создавать утверждаемые файлы]
  Summary -->|Явное yes| Generate[P4 config + strategy + readiness + backlog]
  Generate -->|Framework не найден| Minimal[Минимальные config/profile; нет готового test executor]
  Generate -->|Framework / profiles описаны| Ready([Можно запускать qa-story])
  Minimal -->|Framework появился; нужны настройки| On
  Doc([qa-doctor]) -->|Запрошена диагностика| Audit[Install smoke → readiness → read-only probes → audit → story status]
  Audit -->|Есть stale bookkeeping| Recover[controller recover; не редактировать projections руками]
  Recover -->|Нужно release неизвестной/активной работы| Ask[Спросить человека, работает ли кто-то]
  Audit -->|Выбран первый применимый пункт приоритета| Action[Ровно одно следующее действие]
  Audit -->|Истории простаивают ≥14 дней| Candidates{Есть открытые пункты?}
  Candidates -->|Нет; человек назвал истории| Archive[Archive marker; папка и артефакты остаются]
  Candidates -->|Да| Choice{Архивировать как неактуальное / решить / оставить}
  Choice -->|Явно неактуально| Archive
  Choice -->|Решить| Action
  Choice -->|Оставить / нет ответа| Active[Оставить активной]
  Archive -->|Человек попросил undo| Active
```

Onboarding approval распространяется на перечисленные файлы и отдельные разрешённые зависимости, не автоматически на commit/push/deploy. Doctor выдаёт диагноз и одно следующее действие, а не начинает новую QA-story. Архив — способ скрыть историю с доски; это не доказательство её прохождения.

Приоритет рекомендации doctor: legacy/незавершённый smoke → install FAIL → не Git repo → нет config → schema → capability владельца-user → unresolved halt → stale closed state → unanswered gate → audit violation → продолжить последнюю открытую story. Factory-owned capability defect показывается как дефект фабрики, а не как поручение человеку исправить доступ.

Источники: `skills/qa-onboarding/SKILL.md`, его `phases/`, `skills/qa-doctor/SKILL.md`, `skills/qa-doctor/phases/archive.md`, `skills/qa-doctor/phases/repair.md`.

## 15. Где документация и driver расходятся

Эти пункты — результаты статического сравнения, не подтверждённые воспроизведением runtime-дефекты. На схемах такие пути помечены, чтобы желаемый процесс не выдавался за гарантированное исполнение.

| Метка | Что написано в контракте | Что делает код этой ревизии | Следствие для графа |
|---|---|---|---|
| Δ1 | S0/S1 не допускают agent как маршрут чтения тикета: нужны оригиналы и связанные источники | `s0()` вызывает `ticket_by_agent()`, если прямое чтение неполно | Есть дополнительная ветка agent → временный ticket file; downstream completeness всё равно надо доказать |
| Δ2 | При отсутствии стендов записываются `environment=null`, `environment_pending=true` | `pending = not no_environments_configured`; для пустого списка получается false | Планирование возможно, но индикатор отложенного выбора отличается |
| Δ3 | В S0 §4 есть стоп на dead/login; §5 называет сбой warning для планирования | Driver однозначно поднимает `Person` при `env_probe exit 1`; ряд warnings фазы не собирает отдельной логикой | Нельзя обещать, что выбранный недоступный стенд позволит пройти S0 |
| Δ4 | Есть manual-agent маршрут S4→S6; не все истории обязаны иметь automate cases | `stage_S5()` отказывает при пустом scope. `stage_S6()` с пустым scope закрывает стадию без создания run-report, а S7 требует passed/failed report | Manual-only / nothing-to-run путь может уйти в общий отказ, а не пройти автоматически |
| Δ5 | Repair cause различает test_defect, mechanical, environment, tooling, reviewer_error | В `stage_S5()` повтор по concerns всегда `cause=test_defect`; до двух repairs после первого review | Второй code-critic reject не всегда конец; особые causes не имеют отдельной прямой развилки этого цикла |
| Δ6 | S7: 3 reruns до/после flaky-fix; analyst владеет triage; CASE_DEFECT возвращает кейс | `s7_repairs()` делает `rework S5`, ориентируется на digest green/passed/fixed, затем finalize; отдельные маршруты ENV/CASE в driver не выделены | Ряд переходов обеспечивается ролью/валидатором/conductor, а не детерминированным driver |
| Δ7 | S9 optional feedback: silence может считаться declined | Driver спрашивает один раз и выходит 3; без `--answer` нет автоматического истечения ожидания | Молчание не завершает retro; `skip` ответа отличается от `retro_mode=skip` |
| Δ8 | Контракт S8 поддерживает tracker channels и post-retro delivery | Driver delivery-prompt запрещает Jira и требует Draft MR; `state.delivery` ставится и при ask_person/stop, а повторный вызов пропускается при его наличии | Нельзя обещать прямую Jira-запись или автоматический повтор прерванной доставки без проверки состояния |
| Δ9 | Resume / ответ через >6ч требуют ticket freshness diff; S9 требует close-gate-b и post-retro allowlist update | В основном driver нет явных вызовов ticket `diff`, `traceability --close-gate-b` и отдельного post-S9 delivery update | Эти контрактные переходы нельзя считать гарантированными самим циклом driver |

Ещё две особенности счётчиков: S4 считает принятые critic-dispatches, S5 хранит `rounds` локально; guard no-progress использует `repeats >= 4` при старте с нуля, а refusal-loop — `attempts > 6`. Поэтому текстовые «четыре» и «шесть» не буквально совпадают с количеством всех наблюдений. Проверки controller/budget действуют дополнительно.

## 16. Все 18 объявленных handoff-контрактов

Каждая строка имеет YAML-шаблон в `handoffs/`. Заполненная dispatch-форма находится в `work/handoffs/<dispatch>.yaml` и содержит `inputs_read`, `scope`/решение, `artifacts`, `claims`, `unresolved`, `blocked`. Это **обёртка передачи**, а сами plan, cases, evidence и ledger остаются отдельными файлами.

| № | Откуда → куда | YAML-контракт | Данные, которые получает следующая сторона |
|---|---|---|---|
| 1 | S0 qa-story → S1 scout | `s0-setup-to-scout.yaml` | `pipeline.json`, config, ticket ref/file, флаги, repo paths, stand, readiness, `project:obligations.md` |
| 2 | S1 scout → S2 tester | `s1-scout-to-tester.yaml` | `context-bundle.json`, `context-manifest.json`, `impl-diff.txt` если применим, `source-inventory.json`, source/material paths; число файлов/hunks/bytes, решения по gaps |
| 3 | S2 tester → S3 strategist | `s2-tester-to-strategist.yaml` | `requirements-register.md`, `requirements-readiness.json`, `understanding.md`, `sizing.json`, учёт прочитанных diff/source материалов |
| 4 | S3 strategist → S4 designer | `s3-strategist-to-designer.yaml` | `test-plan.md`, `work/test-plan.json`, register; dispositions, obligations, manual evidence policy; optional judge-plan |
| 5 | S4 designer → case critic | `s4-designer-to-case-critic.yaml` | Markdown cases в реальном cases_root, plan, register, `state/story-case-links.json`; точные pinned versions |
| 6 | S4 critic → designer / завершение S4 | `s4-case-critic-to-designer.yaml` | `critic-findings.md`, полный roll-call, findings с expected/check, verdict по затронутым IDs |
| 7 | S4 designer → S6 runner | `s4-designer-to-runner.yaml` | Pinned manual-agent cases, шаги, Then, manual evidence policy, plan; передача минует авторство automation S5 |
| 8 | Gate A person → automator | `gate-a-to-automator.yaml` | Дословное решение, scope/hashes/revision, approved cases, plan/context, принятые gaps, действия TMS |
| 9 | S5 automator → code critic | `s5-automator-to-critic.yaml` | Test files, `automation-manifest.json`, case versions, targeted run evidence, Then/obligation bindings, optional s5-notes |
| 10 | S5 code critic → automator / acceptance | `s5-critic-to-automator.yaml` | `work/test-code/critic-findings.md`, cause/expected/check, `work/windows/<dispatch>.json`, review/probe receipt refs |
| 11 | S5 automator → S6 runner | `s5-automator-to-runner.yaml` | Manifest + instances + run receipts + fingerprint/provenance + evidence paths; что reuse, что ещё выполнить |
| 12 | S6 runner → S7 analyst | `s6-runner-to-analyst.yaml` | `run-report.json`, manifest, evidence, plan, runtime provenance; executed/reused/blocked и inconclusive |
| 13 | S7 analyst → automator | `s7-analyst-to-automator.yaml` | `triage.json`, failed instance, verdict, mechanism, evidence paths, допустимый объём ремонта |
| 14 | S7 automator → analyst | `s7-automator-to-analyst.yaml` | Изменённые test files, `repair_verify` witness, сохранённые Then, подтверждение результата |
| 15 | S7 analyst → S8 scribe | `s7-analyst-to-scribe.yaml` | `triage.json`, `bug-drafts/`, актуальный `run-report.json`; что исправлено и что осталось |
| 16 | S8 scribe → Gate B person | `s8-scribe-to-gate-b.yaml` | `test-report.md`, `ledger.json/md`, `traceability.json`, delivery-summary, drafts, решения и открытые пункты |
| 17 | Gate B person → delivery/reporter | `gate-b-to-delivery.yaml` | Выбранные drafts, точные delivery actions, risk reason, `state/delivery-manifest.json`, exclude paths, retro_mode |
| 18 | S9 retro → project | `s9-retro-to-project.yaml` | `retro.md`, `retro-numbers.json`, knowledge updates, `project:obligations.md`, backlog, estimation record |

Дополнительно `role-to-conductor.yaml` — не девятнадцатый линейный этап, а аварийная передача: `work/handoffs/*.help.yaml` с полем, отказом, попытками, candidate value и файлами. Ответ conductor: `fill`, `correct_the_work`, `ask_the_person`, `change_the_contract`; контрактный дефект идёт в backlog.

Происхождение таблицы: весь `handoffs/index.yaml` и соответствующие 18 файлов, а не предположение по названиям ролей.

## 17. Артефакты состояния, которые сопровождают все стадии

| Файл / группа | Назначение и передача |
|---|---|
| `pipeline.json` | Человекочитаемая проекция стадий, gates, halts, waivers/remarks, environment и source mode; не заменяет evidence |
| `state/events.jsonl`, `state/controller.json` | Журнал контроллера и его проекция: dispatches, scopes, revisions, decisions, checkpoints; recover восстанавливает проекции |
| `state/driver-state.json` | Session IDs, pending_words, asked question, retro feedback, delivery marker |
| `state/driver-question.md`, `driver-question-details.md` | Вопрос человеку и отдельная техническая причина остановки |
| `state/driver-answers.jsonl`, `driver-question.answered.md` | Дословные ответы и сохранённый отвеченный вопрос |
| `state/driver-runs/<dispatch>.json`, `driver-runs.jsonl` | Сохранённый result для recovery и журнал запусков с usage/cost |
| `state/conductor.jsonl` | Какие отказы обработаны и какое решение conductor вернул |
| `work/handoffs/<dispatch>.yaml` | Контракт передачи конкретной роли; не заменяет перечисленные в нём файлы |
| `work/evidence/`, immutable run/manual blocks, `work/probes/`, `work/windows/` | Проверяемые свидетельства исполнения/обзора с hashes и identity; разные виды receipts не взаимозаменяемы |
| `state/story-case-links.json` | Связь истории с точными версиями case snapshots, в том числе из общей библиотеки cases_root |
| `work/ledger.json`, `work/ledger.md` | Пересчитываемые проекции manifest + run-report + triage; итог не правят вручную |
| `project:records/journal.jsonl` (в старом проекте — `state/`), `project:state/cost/` | События и стоимость проекта; вход числовой части retro |
| `project:obligations.md` | Перенос открытых обязательств между историями; S0 следующей истории перечисляет подходящие по area/trigger |

## 18. Проверка покрытия примеров из запроса

| Ситуация | Где виден путь | Куда ведёт |
|---|---|---|
| Requirements contradict each other | Граф 4 | blocked → вопрос владельцу → S2 повторно; неразрешённый конфликт не порождает план |
| Requirements incomplete | Граф 4 | blocked при влиянии на смысл; иначе ready с явными gaps и явные вопросы A |
| Requirements contradict code | Графы 3, 6, 9 | До A — решение oracle; после A — red evidence → APP_BUG или доказанный CASE_DEFECT |
| You did not answer a question | Графы 3, 5, 10, 12 | Ожидание; нет неявного approval; remark отдельно от нерешённого существенного вопроса |
| Stand unavailable | Графы 2, 7, 8 | Зависит от точки: S0 driver halt либо planning gap; исполнение scoped blocked/remedy |
| MR not written; cases ahead | Графы 3, 5 | Явный ungrounded → S2–S4 → A → pause; дальнейшая проверка не выдаётся за passed |
| Case critic fails second time | Граф 5 | Долг/reject/partial на Gate A, решение человека |
| Code critic fails second time | Граф 6 | В driver возможен второй repair и третий review; затем unresolved/отказ acceptance |
| Role died / dispatch stuck | Граф 12 | Liveness proof → saved result / recover / checkpoint / relaunch; unknown не равен dead |
| Story budget exhausted | Граф 12 | Вопрос человеку; waiver с решением; hard worker quota отдельно |
| Flaky test | Граф 9 | 3 reruns + mechanism → ≤2 repairs → 3 confirmation reruns либо not_verified_flaky → B |
| Tracker read-only | Графы 2, 11 | Предупреждение; локальные bugs; настроить / file вручную / keep local; особенность Jira driver отмечена |
| Code changed after gate A | Граф 13 | Scoped invalidate; доказанная applicability либо semantic reopen → S4 → A |
| Story too big | Граф 4 | XXL recommendation на A; разделение — решение человека, не автоматический splitter |

## 19. Навигация по первичным источникам

Ссылки фиксированы на исследованную ревизию, поэтому сдвиг ветки не меняет основание анализа.

- [Driver: исполняемые переходы и отказоустойчивость](https://git.example.com/dev1/yml-text-factory/-/blob/b9a35c7040c54a537ba72f1a217787c13ad537f1/ai-packages/qa-factory/scripts/story_run.py)
- [Controller: состояния, scope, approval, next action](https://git.example.com/dev1/yml-text-factory/-/blob/b9a35c7040c54a537ba72f1a217787c13ad537f1/ai-packages/qa-factory/scripts/controller.py)
- [Machine-readable stage model](https://git.example.com/dev1/yml-text-factory/-/blob/b9a35c7040c54a537ba72f1a217787c13ad537f1/ai-packages/qa-factory/references/stages.json)
- [Все 18 передач](https://git.example.com/dev1/yml-text-factory/-/blob/b9a35c7040c54a537ba72f1a217787c13ad537f1/ai-packages/qa-factory/handoffs/index.yaml)
- [Фазы S0–S9](https://git.example.com/dev1/yml-text-factory/-/tree/b9a35c7040c54a537ba72f1a217787c13ad537f1/ai-packages/qa-factory/skills/qa-story/phases)
- [Контракт controller API](https://git.example.com/dev1/yml-text-factory/-/blob/b9a35c7040c54a537ba72f1a217787c13ad537f1/ai-packages/qa-factory/references/controller-api.md)
- [Способы выхода из состояний](https://git.example.com/dev1/yml-text-factory/-/blob/b9a35c7040c54a537ba72f1a217787c13ad537f1/ai-packages/qa-factory/design/state-exits.md)
- [Ledger contract](https://git.example.com/dev1/yml-text-factory/-/blob/b9a35c7040c54a537ba72f1a217787c13ad537f1/ai-packages/qa-factory/references/artifact-contract-ledger.md)
- [Onboarding](https://git.example.com/dev1/yml-text-factory/-/blob/b9a35c7040c54a537ba72f1a217787c13ad537f1/ai-packages/qa-factory/skills/qa-onboarding/SKILL.md)
- [Doctor](https://git.example.com/dev1/yml-text-factory/-/blob/b9a35c7040c54a537ba72f1a217787c13ad537f1/ai-packages/qa-factory/skills/qa-doctor/SKILL.md)
