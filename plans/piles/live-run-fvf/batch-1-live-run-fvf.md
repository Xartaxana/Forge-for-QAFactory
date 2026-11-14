# Находки живого прогона LR2-1 — пачка 1: фабрика доходит до тестов без ручной помощи оператора

кучка: `live-run-fvf` | статус: ожидает | взял: — | ветка: — | MR: — | стенд: нужен | приоритет: П1

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего,
живые доказательства (FR-33) сделаны или переданы строкой в кучку «живые прогоны».

Решения владельца: слово владельца 12.11.2026 на прогоне LR2-1: «код не должен урезать бриф, фордж следит за длинной брифа»;
«а роль адаптировать слова человека для кода и запустить его не может? Дирижёр именно для этого и создавался»; «скажи фабрике
посмотреть список тестов ролью и автоматизировать все какие запланированно».
Порядок по общим файлам: `scripts/driver_gates.py`: FV1-7 → FV1-8; `scripts/question_register.py`: FV1-3 → FV1-9.
Скоуп свидетеля: по узлам, при взятии.
Общий бриф дизайнерам: находка узла + `experiments/mybooks/factory-vs-free-agent/notebook.md` («Ход прогона», «Журнал вопросов и
ответов») + логи `experiments/mybooks/factory-vs-free-agent/runs/factory-N.log`.

Пути «Пишет в»: пакета — от `ai-packages/qa-factory/`; это оценка оператора прогона по сообщениям фабрики, Lead пачки уточняет
их скаутом при взятии.

Пополняется по ходу прогона LR2-1 (слово владельца 12.11.2026: «пополняй по мере прохождения прогона»).

## Бриф

Что сделать: узлы таблицы ниже; первыми FV1-1 и FV1-3 — без них фабрика не доходит до автотестов и спрашивает одно и то же
дважды. Направление в каждой находке — предложение оператора прогона (сессия Opus), Lead пачки выбирает его до дизайнера.
FV1-12 ждёт слова владельца о замысле S2. НЕ делать: правки в замороженном дереве релиза `C:\QAFactory\exp-fvf\pkg`.

## Узлы

Исполнитель «designer → builder → critic» — кодовый узел; «builder» — узел-документ. Статусы:
`ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| FV1-1 | П1 | Область S5 пуста: кейсы пишут строку плана `P-1`, читатель узнаёт только `TS-1` (`findings/20261112-s5-pustaya-oblast-p-n-protiv-ts-n.md`) | designer → builder → critic | `scripts/planning_contract.py` | — | ожидает |
| FV1-2 | П1 | Дирижёр не исполнил слово владельца на S5 — нет хода «область по слову человека / суждению роли» (`findings/20261112-dirizher-ne-ispolnil-slovo-vladelca-na-s5.md`) | designer → builder → critic | `scripts/driver_dispatch.py` | FV1-1 | ожидает |
| FV1-3 | П1 | Свободный ответ на пакет вопросов не идёт к дирижёру, роль не может закрыть вопрос (`findings/20261112-svobodnyj-otvet-na-paket-voprosov-ne-idet-dirizheru.md`) | designer → builder → critic | `scripts/question_register.py`, `scripts/driver_dispatch.py` | — | принято: 5f03a39 (t-669) |
| FV1-4 | П1 | Срезка брифа на ходу режет слова человека; длину держит фордж (`findings/20261112-srezka-briefa-rezhet-slova-cheloveka.md`) | designer → builder → critic | `scripts/brief_pack.py` | — | принято: f3167f3 |
| FV1-5 | П1 | Проба стенда ложно «не отвечает»: вход `POST /login` → 405 (`findings/20261112-proba-stenda-lozhno-govorit-ne-otvechaet.md`) | designer → builder → critic | `scripts/env_probe.py` | — | ожидает |
| FV1-6 | П1 | S2: нет двери «вернуть работу тестеру со словами критика» после исчерпания раундов (`findings/20261112-s2-net-dveri-vernut-rabotu-testeru-so-slovami-kritika.md`) | designer → builder → critic | `scripts/driver_machine.py` | — | ожидает |
| FV1-7 | П2 | Гейт A показан до готовности («S5 can start: no») (`findings/20261112-gejt-a-pokazan-do-gotovnosti.md`) | designer → builder → critic | `scripts/driver_gates.py` | FV1-1 | ожидает |
| FV1-8 | П2 | Гейт A требует ответ на вопрос, отложенный «до отчёта» (`findings/20261112-gejt-a-trebuet-otvet-na-vopros-otlozhennyj-do-otcheta.md`) | designer → builder → critic | `scripts/driver_gates.py` | FV1-7 | ожидает |
| FV1-9 | П2 | Пакет вопросов: повторы, нет источников вариантов, «нельзя ответить как есть» показано человеку (`findings/20261112-s4-paket-voprosov-s-povtorami-i-bez-istochnikov.md`) | designer → builder → critic | `scripts/question_register.py` | FV1-3 | принято: ec7b838 (t-720) |
| FV1-10 | П2 | S1 не взяла выгрузку, названную в тексте стори (`findings/20261112-s1-ne-vzyala-vygruzku-nazvannuyu-v-tekste-stori.md`) | designer → builder → critic | `scripts/context_bundle.py` | — | ожидает |
| FV1-11 | П2 | S0 останавливается на тикете без `# ` (`findings/20261112-s0-ostanovka-na-tikete-bez-zagolovka.md`) | builder → critic | `scripts/ticket_adapter.py` | — | принято: 9c6c4c0 (t-669) |
| FV1-13 | П1 | Дирижёр не исполнил выбранный вариант `go on`: судил по прежним словам, спросил в третий раз (`findings/20261112-dirizher-ne-ispolnil-vybrannyj-variant-go-on.md`) | designer → builder → critic | `scripts/driver_dispatch.py`, `scripts/question_register.py` | FV1-3 | ожидает |
| FV1-14 | П2 | Один id строки плана и один читатель: md-план `TS-n` против JSON `P-n`; TS-only читатели S8 (`case_levels`, `traceability.plan_by_ts`, `check_delivery` `TS_IN_TEXT`/`_case_map`, `report_facts`, `handoff_check`, `validate_artifacts`, `grounding_table`) и any-form (`question_register`, `gate_brief`, `brief_pack`) — через читатель `contract`; проверка выхода S3; новая ось SIBLING_MAP (`docs/tasks/specs/reviews/t-152-fv1-1-critic.md`, F4) | designer → builder → critic | `scripts/traceability.py`, `scripts/check_delivery.py`, `scripts/contract.py` | FV1-1 | ожидает |
| FV1-15 | П1 | Онбординг записал «вход кодом невозможен» по POST на страницу `/login`; S5 стоит на записанном отказе (`findings/20261112-onbording-zapisal-vhod-kodom-nevozmozhen-oshibochno.md`) | designer → builder → critic | `scripts/env_probe.py` | FV1-5, FV1-17 | ожидает |
| FV1-16 | П2 | S5 спрашивает, развёрнут ли на стенде приложения коммит репозитория тестов; «current code» с S0 не доходит (`findings/20261112-s5-lichnost-stenda-sprashivaet-kommit-repo-testov.md`) | designer → builder → critic | `scripts/driver_gates.py` | — | ожидает |
| FV1-17 | П1 | Онбординг не умеет определить, как войти на стенд проекта: POST на страницу `/login` → «вход кодом невозможен»; NextAuth-вход и `harness_command` не испробованы (`findings/20261112-onbording-ne-umeet-opredelit-kak-vojti-na-stend.md`) | designer → builder → critic | `scripts/stand_access.py`, `references/login-body-fields.json`, `skills/qa-onboarding/SKILL.md` | — | ожидает |
| FV1-18 | П1 | Регрессия: без проверенного контракта селекторов `run_suite` отказывает запускать тесты автоматора (раньше работало); селекторы собирает раннер первого взгляда, его запись не читается `selectors_verified` (`findings/20261112-kontrakt-selektorov-nikogda-ne-proveren.md`) | designer → builder → critic | `scripts/execution_request.py`, `scripts/profile_contract.py`, `scripts/onboarding_probe.py` | — | принято: 7aee0ca (t-672) |
| FV1-20 | П1 | Критик кода S5 закрывает ревью без проб чувствительности (файл модели проб не написан, причины нет); `round` человека ушёл дирижёру, дирижёр ложно сказал «фабрика не может произвести пробы» (`findings/20261112-kritik-koda-ne-zapuskaet-proby.md`) | scout → designer → builder → critic | хартия и бриф S5 qa-code-critic, `scripts/driver_dispatch.py` (repair_limit → conductor) | — | ожидает |
| FV1-23 | П1 | Сравнение (а, е): документы продукта из репозитория приложения (`docs/AUTH.md`, `TEST_IDS_REFERENCE.md`) не в реестре требований; вопросы владельцу о записанном (`findings/20261113-sravnenie-dokumenty-produkta-ne-prochitany.md`) | scout → designer → builder → critic | `scripts/source_inventory.py`, `agents/qa-requirements-tester.md` | — | ожидает |
| FV1-24 | П1 | Сравнение (б, в): черновики багов ручного прохода не доведены до вердикта; черновик на «выведенном» ожидании без вопроса (`findings/20261113-sravnenie-chernoviki-bagov-ne-podtverzhdeny.md`) | designer → builder → critic | хартия S6/S7 (runner, failure-analyst), `bug-drafts` | FV1-22 | ожидает |
| FV1-25 | П1 | Сравнение (ж): ни один автотест не падает на найденной поломке; нет пути «баг ручного прохода → падающий тест» (`findings/20261113-sravnenie-net-krasnyh-testov-na-bagi.md`) | designer → builder → critic | `agents/qa-automator.md`, `agents/qa-failure-analyst.md` | FV1-20, FV1-24 | ожидает |
| FV1-26 | П2 | Сравнение (з): «не удалось проверить» смешивает невозможность и свою недоделку (`findings/20261113-sravnenie-ne-udalos-eto-svoya-nedodelka.md`) | designer → builder → critic | `scripts/report_facts.py` | FV1-18 | ожидает |
| FV1-22 | П1 | S7 по кругу: приёмка S6 из формы аналитика требует `failure_class`/`quote` и строку `inputs_read` раннера, которых в форме нет; дирижёр трижды повторил разбор аналитика с причиной `tooling`, лимит не тратится, ремонт TC-005 автору не ушёл (`findings/20261113-s7-petlya-dirizhera-na-prieme-s6.md`) | designer → builder → critic | `scripts/stage_done.py`, форма S7 qa-failure-analyst, `scripts/driver_dispatch.py` (conductor rework) | — | принято: 379f687 (t-700) |
| FV1-21 | П2 | Цена ложно помечена «not every session is recorded»: `task_price` считает ходы кода `gate_repair` звонками без сессии; цена CLI и цена по токенам совпадают ($24.32 / 71 сессия) (`findings/20261112-cena-lozhno-nepolnaya-iz-za-shagov-koda.md`) | builder → critic | `scripts/task_price.py` | — | принято: 4f61fb5 |
| FV1-19 | П1 | S5 требует `obligation_refs`, а `manifest_from_tests.py` читает маркер только из Python — для `.spec.ts` поле не произвести (FR-5, P31); проверка при этом пропустила рукописное значение без хэша (окно 2); починка «not a question for the person» ставится человеку exit_limit (`findings/20261112-pochinka-ne-vopros-cheloveku-dohodit-do-cheloveka.md`) | designer → builder → critic | `scripts/manifest_from_tests.py`, `scripts/s5_precheck.py`, `scripts/story_run.py` | — | в работе |
| FV1-12 | П2 | Карточка S2 и реестр стадий расходятся; замысел S2 — слово владельца (`findings/20261112-s2-kartochka-i-reestr-stadij-rashodyatsya.md`) | ждёт слова владельца → builder | `skills/qa-story/phases/s2.md`, `references/stages.json` | — | ожидает |
| FV1-27 | П1 | Требование проверки роль узнаёт в момент отказа, а не до работы: три новых экземпляра (backslash в команде, прямой `playwright test`, запись `values.yaml`); ОДИН механизм на класс: перечень отказов (разведка t-446), требование из того же источника, что текст отказа, проверка на пути исполнения + сухая стори. НЕ готов для билдера: спеку механизма пишет дизайнер после перечня (`findings/20261113-trebovanie-proverki-rol-uznaet-v-moment-otkaza.md`) | scout (t-446) → designer → builder → critic | `scripts/hooklib.py`, `scripts/stage_guard.py`, `scripts/guard_pre_tool.py`, `scripts/refusal_registry.py`, `agents/qa-automator.md` (перечень уточняет t-446) | — | ожидает |
| FV1-28 | П1 | «Первый взгляд» доходит до автоматора S5 по существу (адреса, шаги, локаторы, образцы API окна), а не строкой-указателем; пропуск первого взгляда по недоказанному «no stand» — неизвестное, не факт (`findings/20261113-pervyj-vzglyad-ne-dohodit-do-avtomatora.md`) | designer → builder → critic | `scripts/brief_pack.py`, `scripts/first_look.py` | FV1-5 | ожидает |
| FV1-29 | П1 | Автоматору S5 даётся ходок фабрики `walk_session.py`: сам смотрит стенд, когда первый взгляд пуст или неверен; нехватка селекторов его не стопорит (`findings/20261113-avtomatoru-ne-dan-hodok-po-stendu.md`) | designer → builder → critic | `agents/qa-automator.md`, `scripts/brief_pack.py` | FV1-28, FV1-18 | ожидает |
| FV1-30 | П1 | Запрет без двери: 7 семейств `s5_precheck` (`manifest`, `bindings`, `oracle`, `run_mapping`, `smell`, `plan`, `sides`) не проходят по слову человека; класс — проход словом с записью `passed-by-person`; исключения: вердикт доставки `no`, проверка открытого ожидания решается отдельным узлом; по семействам порознь — вопрос Lead (`findings/20261113-zapret-bez-dveri-s5-precheck-slovo-ne-provodit.md`; нужна до узла `N4:gates` спеки сухой стори) | designer → builder → critic | `scripts/s5_precheck.py`, `scripts/exit_gate.py` | — | принято: 2a88226 (t-720) |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 12.11 19:10 — пачка открыта оператором прогона LR2-1 (сессия Opus) по слову владельца; 12 находок первых полутора часов
  прогона (17:39–19:05).
- 12.11 19:12 — FV1-13: третья остановка плеча `factory` на S5, плечо остановлено по потолку RUN-INSTRUCTIONS §5.
- 12.11 20:01 — FV1-1 по слову владельца («починить блокер и запустить ещё раз»): t-152 bb2bd10 + фикс-раунд t-162 5971ac0
  (критик t-161: fit_with_fixes, F1–F3 закрыты) на ветке `worktree-agent-a02fafab496f0a9f6`, в main не слита (через ветку
  пачки и CI). Остаток класса — FV1-14. Две строки правки наложены на копию прогона `C:\QAFactory\exp-fvf\pkg-fix1`.
- 12.11 21:05 — FV1-19: окно 2 S5 прошло после второго `round`, окно 1 встало на exit_limit тем же классом (24 места).
- 12.11 21:12 — FV1-19 переписана (читатель маркера только Python; окно 2 прошло рукописным значением — помощь оператора);
  FV1-13 третий экземпляр: `go on` на exit_limit не записывается (заглушка в строке проверки). Окно 1 третий раз на одном месте —
  плечо остановлено по потолку RUN-INSTRUCTIONS §5.
- 12.11 21:23 — FV1-13 (третий экземпляр, `go on` на exit_limit) по слову владельца «чинить и продолжить»: t-180 8eb20e4 на ветке
  `worktree-agent-aaf518a792f694a7e` (в main не слита), правка наложена на копию `pkg-fix1`; плечо перезапущено. Первые два
  экземпляра FV1-13 (жетон в бэктиках, слова при `round`) не тронуты.
- 12.11 22:50 — FV1-13 четвёртый экземпляр: дирижёр предложил `go on` (долг в гейт B) без писателя долга — записал заметку, вопрос
  вернулся; долг critic-7 уже был записан, но стадия после него пустила раунд автора `S5-qa-automator-9`. Ответ оператора `retry`.
- 12.11 23:04 — FV1-19: дверь t-186 неполна — финиш требует хэш каждой ссылки, его строит только путь маркера Python; ручные хэши
  автора-9 не совпали с планом (×7). Критик-8 без блокирующих → `debt`; отказ финиша → `go on`.
- 12.11 23:07 — S5 пройдена после хэшей из плана фрагментом оператора (помощь оператора); S6 18/1.
- 13.11 01:00 — FV1-22: S7 по кругу (аналитики 2–4, причина `tooling`); плечо остановлено по слову владельца, гейт B не достигнут.
- 13.11 01:5x — слепая оценка (критик t-236): фабрика хуже свободного агента в строках а, б, в, е, ж, з, и, к, л; больше — ни в
  одной. FV1-23…FV1-26 (новые классы); и, к, л — петли FV1-13…FV1-22. Правило стопа таблицы: стоп до разбора.
- 13.11 — статусы по слиянию в main 7cf8c34 (слово владельца 13.11: статус идёт с слиянием): FV1-4 принято f3167f3 (с остатками L1–L5), FV1-21 принято 4f61fb5; FV1-19 в работе — база N1–N3 слита (4d0ad66), C1 в работе, C2 ждёт; FV1-11 сдано (принято, da90045, слияние в следующей волне). Спека готова, билдер ждёт: FV1-3, FV1-5, FV1-6, FV1-17, FV1-20, FV1-22, FV1-23. FV1-12: слово владельца получено 13.11 (запись в находке на ветке wip/owner-words-1113b), ждёт спеки.
- 14.11 — FV1-19: C2 слит в main коммитом 819a31f (ветка `wip/fv19-c2`, отчёт волны 3 `docs/tasks/specs/reports/20261113-wave3-integration-report.md`); узел остаётся «в работе»: отчёты волн 2–4 не называют слияния C1 и закрытия узла целиком. FV1-11 в отчётах волн 2–4 не назван: остаётся «сдано».
- 14.11 (t-669) — по слиянию в main: FV1-3 принято, `wip/fv1-3` слита 5f03a39 (отчёт волны 6); FV1-11 принято, `wip/fv111` слита 9c6c4c0 (отчёт волны 1). FV1-19 остаётся «в работе»: в main N1–N3 (`wip/fv19-30-base` → 7cf8c34, база 4d0ad66), C1 (928cac6) и C2 (819a31f; C1 — предок ветки C2); N4 (19d, `driver_dispatch.handoff_ladder`) не слит, ветки нет. FV1-30 остаётся «ожидает»: в main 30a (84f91d7, в базе 4d0ad66 → 7cf8c34) и 30b N0–N2 (топик 39be4b7), N3 (d01c2a5), N6 (eb86925); N5 (`_terminal_runs`, остаток спеки, «queued») не слит — закрывать узел целиком или нет, решает Lead. FV1-18: ветки `wip/fv118-*` (топик 9fc7d61, фикс 27a6cf4) в main НЕ слиты.
- 14.11 (t-672) — волна 7: FV1-18 принято, `wip/fv118-fix` (27a6cf4; содержит топик и ветки n1…n4) слита 7aee0ca; конфликт один — `test_probe_by_code_languages.py` разрезан в main (PC3-2), правки ветки перенесены в `test_probe_by_code_languages_ts_playwright.py`. Отчёт `docs/tasks/specs/reports/20261114-wave7-integration-report.md`.
- 14.11 (t-700) — волна 8: FV1-22 принято (N1+N2+N3, фикс-раунд), `wip/fv1-22r-fix` слита 379f687. Отчёт `docs/tasks/specs/reports/20261114-wave8-report.md`.
- 14.11 (t-720) — волна 9: FV1-9 принято (N1+N2+N4+N5, фикс-раунд), `wip/fv1-9-fix` слита ec7b838; FV1-30 принято: 30b N5 (`wip/fv130b-n5`, facd5d1) и N4 (`wip/fv130b-n4`, 2a88226) слиты, N0–N3 и N6 были в main раньше; FV1-23 слит частично (A-1, A-4, `wip/fv123-a14`, b9dd7d0), статус не меняется. Отчёт `docs/tasks/specs/reports/20261114-wave9-report.md`.
- 14.11 (t-729) — волна 10: FV1-20 — узел B-1 слит (`wip/fv120-b1`, 754b9de), узлы B-2…B-4 не слиты, статус не меняется; FV1-9 — карточка D хвоста слита (`wip/fv1-9-td`, 659dcc4), статус не меняется. Отчёт `docs/tasks/specs/reports/20261114-wave10-report.md`.
- 14.11 (t-736) — волна 11: FV1-9 — карточки B (`wip/fv1-9-tb`, ba52304) и C (`wip/fv1-9-tc`, 23a7f6a) слиты, статус не меняется. Отчёт `docs/tasks/specs/reports/20261114-wave11-report.md`.

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|

## Остатки
