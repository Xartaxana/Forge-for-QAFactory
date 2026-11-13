# Текст человеку и гейты A/B (`gates-and-words`)

приоритет: П2 | фичи: F07 | стенд: нужен | зона: `ai-packages/qa-factory/scripts/gate_preflight.py`, `scripts/waiver.py`, `scripts/story_run.py`, `scripts/traceability.py`, `scripts/stand_gaps.py`, `scripts/person_words.py`, `scripts/gate_brief.py`, `scripts/stand_identity.py`, `scripts/source_exclusions.py`, `scripts/tests/test_words_doors.py`

## Зачем

Сегодня человек на гейтах иногда обязан выполнить команду руками вместо слов, его слова читаются разными читателями
по-разному (подстрокой, без учёта отзыва), а карточки гейтов местами называют скрипт или обещают то, чего никто не
исполнит. После первой пачки человек отвечает на гейтах словами, его слова доходят до всех читателей одинаково и не
переспрашиваются, отозванное решение не действует, а текст гейта не называет человеку ни скрипта, ни флага.

## Что не так сегодня (факты)

- Гейт A снимает находку по подстроке: `RP-web` проводит `RP-web-e2e` (`plans/BACKLOG.md:362`).
- Отозванные решения читаются как действующие: читатели не смотрят на `revoked_at`, побеждает позиция в списке (`plans/BACKLOG.md:363`, `plans/BACKLOG.md:396`, `plans/BACKLOG.md:412`).
- Семь дверей в пяти файлах висят в PENDING детектора как «queued» без строки бэклога (`plans/BACKLOG.md:407`).
- Хвост вывода прогона режется до `names_only`, значение `NAME=value` может попасть в `manifest.json`: дайджест `docs/tasks/specs/reports/t-713-scout-piles-b.md` сверил с кодом (`gate_preflight.py:2295`) 13.10 — не устарело.
- Слова на гейте B «автоматизацию нужно доработать» были некому исполнить; узел C1-4 `conductor/1` принят (`plans/piles/conductor/batch-1-p22-seams.md`), закрыта ли находка 09.10, проверить по коду.
- 15 открытых строк в пачке 1 и 20 находок (дайджест t-713, пересчёт 15 из 15 и 20 из 20 на 13.10).

## Пачки

| № | Что изменится для пользователя | Строки | Размер | Статус | Взял | Ветка | MR |
|---|---|---|---|---|---|---|---|
| 1 | человек на гейтах отвечает словами, его слова доходят до всех читателей и не переспрашиваются; карточки гейта не врут; отозванные решения не действуют | B-338, B-339, B-376, B-392 | M | закрыта | — | — | `855d4e5c` |

Открытое перенесено 01.11.2026 → release-next/1, words-gates/1, driver-hosts/1, onboarding-forge/1, driver-hosts/2.

Статусы пачки: `ожидает` → `в работе` → `сдано` → `принято` → `закрыта`. Размер — по узлам: S ≤ 4 узлов,
M 5–9, L 10–15 (больше — две пачки). Взятая пачка заморожена: её файл правит только взявший, новое
по теме — файлом в `findings/`.

## Бриф пачки 1

Начать с GW1-1 (сопоставление и отзыв слов) — на нём стоят читатели остальных узлов; GW1-3 и GW1-4 пишут `story_run.py`
и идут после `conductor/1`. Стенд нужен только для проверки текстов гейтов на живом прогоне; слово владельца не нужно
(решения 02.10 и 03.10 даны). Подробно — `batch-1-words-and-gates.md`, раздел «Бриф».

## Дороги

Читать по порядку: эта карточка → `batch-1-words-and-gates.md` → находки узла (колонка «id / файл» ниже) → строки
`plans/BACKLOG.md` 215, 216, 242, 362, 363, 378, 385, 387, 396, 407, 408, 412, 442–444 → `ai-packages/qa-factory/references/human-questions.md`
→ код зоны по функциям из «Слов» → `PROJECT.md` P9, P13, P15, P22 → `docs/factory-map/qa-factory-paths.md` (гейты A и B).
Слова: `plans/features.json` F07 (поле `words`) и сверх них: `revoked_at`, `stage_overrides`, `split_overridden`,
`decision_words`, `story_budget.override`, `_overrides`, `waiver --revoke`, `--words-file`, `person_words.door`,
`remedy.change`, `names_only`, `_keep_unread`, `PENDING`, `_option_word`, `_live_records`, `safe_name`, `gap_cases`,
`outside`, `STANDING_ANSWERS`, `question_from_refusal`, `approve_delivery`, `build_gate_decision`; «слова человека»,
«отозван», «гейт A», «гейт B», «карточка гейта».
Не читать: код стадий вне гейтов, зону `conductor` (кроме строки C1-4 и находки 09.10 про гейт B), `cost_capture.py`.

## Содержание

Снимок 13.10.2026; пути — от `ai-packages/qa-factory/scripts/`; суть строк — из `plans/BACKLOG.md`, находок — из дайджеста t-713. При расхождении авторитетны файлы пачек.

| id / файл | вид | суть (≤ 20 слов) | пути | статус | слово владельца | связи |
|---|---|---|---|---|---|---|
| **Слова человека: сопоставление и отзыв (пачка 1, GW1-1)** | | | | | | |
| B-338 | строка | гейт A снимает находку по подстроке; тот же класс на S5; сопоставлять идентификатор целиком | `gate_preflight.py`, `waiver.py` | пачка 1, GW1-1 | нет | — |
| B-339 | строка | отозванные решения читаются как действующие; читатели не смотрят на `revoked_at` | `traceability.py`, `contract.py` | пачка 1, GW1-1 | нет | — |
| B-376 | строка | `waiver --revoke` отзывает по одной стадии, читатель берёт самый поздний ответ по всем | `waiver.py` | пачка 1, GW1-1 | нет | — |
| B-392 | строка | три читателя `stage_overrides` пропускают `revoked_at`; нужен один читатель | `waiver.py`, `traceability.py`, `report_facts.py` | пачка 1, GW1-1 | нет | — |
| **Файловый маршрут слов и двери (пачка 1, GW1-2)** | | | | | | |
| B-365 | строка | у `stand_identity.py --words` и `source_exclusions.py --revoke --words` нет файлового маршрута слов | `stand_identity.py`, `source_exclusions.py` | пачка 1, GW1-2 | нет | — |
| B-387 | строка | семь дверей в пяти файлах висят в PENDING детектора без строки бэклога | `tests/test_words_doors.py`, `person_words.py` | пачка 1, GW1-2 | нет | — |
| B-388 | строка | `person_words.door(for_person=True)` называет скрипт человеку и не вызывается вне тестов: убрать или переназначить | `person_words.py` | пачка 1, GW1-2 | нет | — |
| **Гейт B словами (пачка 1, GW1-3)** | | | | | | |
| B-272 | строка | гейт B: человек отвечает словами, а не командой `waiver.py`; закрытый список слов — в данных | `story_run.py`, `waiver.py` | пачка 1, GW1-3 | дано 02.10 («до релиза») | — |
| B-271 | строка | ретро всегда полное: из текста гейта B убрать «можно пропустить или урезать» | `story_run.py` | пачка 1, GW1-3 | дано 02.10 | — |
| **Тексты человеку после части A (пачка 1, GW1-4)** | | | | | | |
| B-292 / `findings/B-292-teksty-cheloveku-posle-chasti-a-t-357.md` | строка + находка-остаток | тексты человеку после части A: ~11 подпунктов (а–к); (д) закрыт, (г) решено 03.10 | `stage_done.py`, `story_run.py`, `gate_brief.py`, `gate_preflight.py`, `waiver.py`, `readiness.py` | пачка 1, GW1-4; перечень подпунктов — в находке | (г) дано 03.10 | — |
| **Карточка гейта и дверь запуска (пачка 1, GW1-5)** | | | | | | |
| B-358 | строка | строка «the fix:» на карточке и инструкция исполнителю `apply` — одно поле `remedy.change`; разделить | `gate_preflight.py`, `gate_brief.py` | пачка 1, GW1-5 | нет | — |
| B-362 | строка | текст двери запуска без читаемого отчёта не предлагает «запустите ещё раз», когда повтор не поможет | `gate_preflight.py` | пачка 1, GW1-5 | нет | — |
| **Остатки узлов стенда и копии (пачка 1, GW1-6)** | | | | | | |
| B-423 | строка | остатки переноса ответа гейта A на гейт B: сравнение строк только внутри одного ключа; копии `_option_word`, `_live_records` | `stand_gaps.py`, `gate_brief.py`, `contract.py` | пачка 1, GW1-6 | нет | `live-runs` (перенос ответа) |
| B-424 | строка | отказ по XML-сущностям в одном потребителе; пустой `kind` читается по-разному на гейте A и в S5; счёт `outside` | `gate_preflight.py`, `traceability.py` | пачка 1, GW1-6 | нет | `report-delivery` |
| B-425 | строка | копии узлов карточки пробела: читатель argv профиля, два сырых чтения конфига, `safe_name`, форма `gap_cases` | `gate_preflight.py`, `reporters.py` | пачка 1, GW1-6 | нет | — |
| **Гейт B и P22 («нет хода»)** | | | | | | |
| `findings/20261009-gate-b-pravka-avtomatizacii-bez-ispolnitelya.md` | находка, id — | слова «автоматизацию нужно доработать» некому исполнить; любой ответ пишется как `approve_delivery` | `controller.py`, `story_run.py` | узел C1-4 `conductor/1` принят — сверить по коду | дано 09.10 (D-0039) | `conductor` C1-4 |
| `findings/20261013-odobrenie-geyta-a-nad-neotvechennym-punktom.md` | находка, id — | `approve` записан, хотя пункт репетиции `s5_toolchain-1` (PERSON_DECIDES, без дверей) остался без ответа под срезанной сводкой; S5 не смог запустить ни один тест | `gate_preflight.py` (:3809 сводка, :224 `collect_failure`), `controller.py` (решение гейта) | открыто (скаут t-723, 13.10 21:40); сосед — гейт B | нет | `conductor` C2-7 (не чинит), t-718 K2/K8 |
| `findings/20261013-fabrika-ne-obeshchaet-nevozmozhnogo.md` | находка, id —, кандидат наверх | фабрика не спрашивает о заведомо невозможном (недостижимый источник — пробел по умолчанию) и не переспрашивает по экземпляру после записанного пробела | `story_run.py` (S1 тексты), `ticket_adapter.py`, `s5_precheck.py` | чинится узлом C2-9 `conductor/2` (класс K8 отчёта t-718); принцип — в DECISIONS/P5 пишет Lead | дано 13.10 20:58 | `conductor` C2-9 |
| `findings/B-063-slovo-defer-na-geyte-b-yavnye.md` | находка | слово `defer` на гейте B: человек имел в виду «отложить поставку», фабрика сделала `[Fact(Skip)]` | — | открыто | нет | — |
| `findings/B-064-rezhim-podgotovitelnaya-stori-realizatsii-net.md` | находка | режим «подготовительная стори» задаётся вопросом на гейте A; механизм `policy` есть, вызовов нет | `controller.py` | открыто | нет | — |
| `findings/B-061-dva-raznykh-slova-propushcheno-po-nashemu.md` | находка | «пропущено по нашему решению» и «у продукта нет поверхности» — два слова, второе блокирует сдачу | `check_delivery.py` | открыто | нет | `report-delivery` |
| `findings/B-062-doroga-k-bagu-dlya-trebovanie-ne.md` | находка | нужна дорога к багу для «требование не выполнено, упасть нечему» | — | открыто | нет | `report-delivery` |
| **Слова человека: транспорт и устаревшее (кандидаты пачки 2)** | | | | | | |
| `findings/B-258-propusk-stand-login-missing-matchitsya.md` | находка | пропуск «stand login missing» матчится подстрокой (`waiver.split_overridden`) | `waiver.py` | открыто | нет | — |
| `findings/B-296-otlozhennoe-reshenie-po-ukazatelyu-na-element.md` | находка | отложенное решение по указателю `/profiles/<n>/…` — тупик | `project_decisions.py` | открыто | нет | — |
| `findings/B-336-transport-ostatki-volny-3-na-puti.md` | находка | транспорт слов: `controller initialize`, слова через stdin, `utf-8` против `utf-8-sig`, обрезка до 1000 знаков | `controller.py`, `ticket_adapter.py` | открыто | нет | — |
| `findings/B-343-slova-cheloveka-ostatki-posle-volny-3.md` | находка | остатки слов человека: команды без файлового пути, обрезка до 1500/2000 знаков, `freshness --decline` | `gate_preflight.py`, `tests/test_words_doors.py` | открыто; пункт 5 ссылается на удалённое (по находке B-391) | нет | — |
| `findings/B-341-ochered-volny-4-spetsifikatsiya-v2-razdel.md` | находка | очередь q1–q6: слова по строкам дашборда, повторный вопрос по карточкам | `manifest_put.py`, `gate_preflight.py` | устарела по находке B-391 (q6 ссылается на удалённое) — проверить по коду | нет | — |
| `findings/B-391-perechitat-b-341-q6-i-b-343-5.md` | находка | перечитать два пункта, которые ссылаются на удалённое | `gate_preflight.py` | открыто | нет | — |
| **Гейт A: неизвестное — вопрос; защита одобрений (кандидаты пачки 2)** | | | | | | |
| `findings/B-280-geyt-case-preconditions-t-302-g13-error.md` | находка | гейт `case_preconditions` считает `error` среды дефектом фабрики | `gate_preflight.py`, `planning_contract.py` | открыто | нет | — |
| `findings/B-282-geyt-s5-stand-limits-t-302-f9-neizmerennyy.md` | находка | гейт `s5_stand_limits` пропускает неизмеренный лимит как проход | `gate_preflight.py` | открыто | нет | — |
| `findings/B-416-d-0031-otchet-testov-kotoryy-kod-prochitat.md` | находка | отчёт тестов, который код прочитать не смог, не идёт человеку первым; читатели, потом дирижёр, потом человек | `reporters.py` | слово владельца дано 06.10 (D-0031) | дано 06.10 | — |
| `findings/B-294-odobreniya-konfiga-b-220-kritik-t-380-dyra.md` | находка | одобрения конфига: дыра гарда, `onboard_apply --apply` без `--approval-ref` | `guard_pre_tool.py`, `story_step.py`, `onboard_apply.py` | открыто | нет | `onboarding-hooks` |
| `findings/B-295-onbording-kritik-t-380-f14.md` | находка | `launch_check` чинит config на месте; лог одобрений без лока | `launch_check.py` | открыто | нет | — |
| `findings/20261009-utechka-znacheniy-v-hvosty-manifest.md` | находка, id — | хвосты вывода режутся до `names_only`, значение `NAME=value` утекает в `manifest.json` | `gate_preflight.py`, `onboarding_probe.py`, `stand_gaps.py` | не устарела: проверено по коду 13.10 (дайджест t-713) | нет | — |
| **Тексты человеку и гигиена детектора (кандидаты пачки 2)** | | | | | | |
| `findings/B-171-syrye-peresylki-drayvera-cheloveku-ostavshiesya.md` | находка | сырые пересылки драйвера человеку после B-009 ч.2; номера строк относятся к старой версии | `story_run.py`, `gate_preflight.py` | открыто; номера строк проверить по коду | нет | `conductor` |
| `findings/B-379-detektor-dverey-test-words-doors-py.md` | находка | детектор дверей сопоставляет по тексту, не по числу, и не сканирует `evals/`, `hooks/`, корневые документы | `tests/test_words_doors.py` | открыто | нет | — |
| `findings/20261021-s5-finish-prinimaet-avtomatora-bez-raspiski-progona.md` | находка | `story_step finish` принимает хэндовер автоматора S5 без расписки авторского прогона: вердикт выходного гейта и `s5_precheck` на пути `finish` никто не читает | `scripts/story_step.py`, `scripts/exit_gate.py`, `scripts/role_digest.py`, `scripts/handoff_check.py` | GW1-8, ожидает | да (до 0.10.0 или в 0.10.1 до следующего приёмочного прогона на Codex Desktop) | аудит фиксов Кодекса 21.10 §3.3–3.4; скаут t-1260 |
| `findings/20261021-padenie-detektora-na-finish-chitaetsya-kak-pass.md` | находка | падение детектора под `story_step finish` читается как «ошибок нет»: `all_errors` не отличает «не смог проверить» от «чисто» (FR-59, AR-28) | `scripts/exit_gate.py`, `scripts/story_step.py`, `scripts/story_run.py` | GW1-9, ожидает | нет | критик t-1265 fail-open 1; GW1-8 |
| `findings/20261021-detektor-pod-finish-ugadyvaet-istoriyu.md` | находка | детектор под `finish` сам угадывает историю: при двух историях `finish` красной A читает чистую B и принимает; `sizing.json` угаданной истории пишется и на отказе | `scripts/exit_gate.py`, `scripts/s5_precheck.py`, `scripts/sizing.py`, `scripts/story_run.py` | GW1-10, ожидает | нет | критик t-1265 fail-open 3 / F8; GW1-8 |
| `findings/20261022-gejt-a-chetyre-dokumenta-vmesto-dvuh.md` | находка | гейт A называет человеку четыре документа вместо двух одобряемых: `GATE_A_DOCUMENTS` держит четыре против правила «understanding + план» | `scripts/gate_brief.py`, `phases/s4.md`, `SKILL.md`, шаблоны | GW1-11, ожидает | да, дано 22.10.2026 (вариант а: кейсы — часть плана) | гейт B (сиблинг), AR-14 |
| `findings/20261022-ostanovka-posle-gejta-bezuslovnaya.md` | находка | после записи решения гейта дирижёр всегда останавливается и просит человека перезапустить фабрику, хотя бюджет окна смены не требует | `SKILL.md`, `phases/s4.md`, `phases/s8.md`, `window_budget.py`, `controller.py` | GW1-12, ожидает | да, дано 22.10.2026 («это надо убрать») | GW1-11, P3 |
| `findings/20261022-probel-integracii-ne-nazvan-do-gejta-a.md` | находка | пробел интеграции стенда (Jira для датасорса) известен с онбординга, а человеку назван только в S5 и только по его просьбе | `gate_preflight.py`, `gate_brief.py`, `env_probe.py` | GW1-13, ожидает | да, дано 22.10.2026 («говорить, чего не хватает, сразу, чтобы не возвращать стадии») | гейт B «Left with you», P5 |
| `findings/20261022-odin-then-nelzya-otdat-cheloveku.md` | находка | один невыполнимый Then нельзя отдать человеку при зелёном тесте кейса: partial-green отказан, слово человека отказано у источника | `s5_precheck.py`, `manifest_put.py`, `check_coverage.py`, `report_facts.py` | GW1-14, ожидает | да, дано 22.10.2026 | P21, GW1-13 |
| `findings/20261023-reshenie-po-integratsii-ne-doezzhaet-do-gejta-b.md` | находка | решение по пробелу интеграции не доезжает до гейта B: непривязанный `accept` не связан со строкой S5, слово по `INT-*` не переоткрывает перенесённый accept | `stand_gaps.py`, `gate_preflight.py` | GW1-15, ожидает | нет | GW1-13, t-051 Q1, t-062 п. 3 |
| `findings/20261023-kejs-ne-svyazan-s-integratsiej-esli-required-by-prosa.md` | находка | кейс не связан с интеграцией при прозаическом `required_by` или чужом id (`TS-99`): гейт A называет Jira, но не кейс и не Then | `agents/qa-case-designer.md`, `gate_preflight.py`, `brief_pack.py` | GW1-16, ожидает | нет (слово 22.10 дано) | GW1-13, t-051 Q2, t-062 п. 1 |
| `findings/20261023-ukazatel-brifa-na-razdel-kotorogo-net.md` | находка | бриф гейта A при переполнении отсылает к разделу «Rehearsal of gate A», которого нет в `work/gate-a-brief.md` | `gate_preflight.py`, `gate_brief.py` | GW1-17, ожидает | нет | GW1-13, t-051 Q3 |
| `findings/20261023-schetchik-hodov-obnulyaetsya-na-kazhdoj-stadii.md` | находка | `stage_done` обнуляет счётчик ходов на каждой стадии: `boundary_notice` после гейта меряет только ходы гейта и почти не срабатывает | `stage_done.py`, `turn_budget.py`, `window_budget.py` | GW1-18, ожидает | нет | GW1-12, t-061 F-6 |
| `findings/20261023-neizvestnoe-znachenie-stop-after-i-bom-config-molcha-ne-dejstvuyut.md` | находка | неизвестное значение `pipeline.stop_after` молча значит «без остановки», конфиг с BOM `hooklib.load_config` молча не читает | `config_contract.py`, `readiness.py`, `hooklib.py` | GW1-19, ожидает | нет | GW1-12, t-061 F-7 |
| `findings/20261023-test-report-facts-bez-klyucha-na-s5-integrations.md` | находка | у строки риска `s5_integrations` в `report-risk-words.json` нет теста в `test_report_facts.py`: удаление строки ничем не ловится | `tests/test_report_facts.py` | GW1-20, ожидает | нет | GW1-13, t-067 п. 2 |
| `findings/20261024-otvety-cheloveka-ne-primenyayutsya-srazu.md` | находка | ответы человека на S2/S3/S4 не доходят до брифов и хранилища, блокирующий вопрос не останавливает до записи — возвраты на доработку | `story_run.py`, `question_register.py`, `question_stop.py`, `brief_pack.py`, `planning_contract.py`, `gate_brief.py` | GW1-21, ожидает | слово 24.10.2026 (поведение) | GW1-7, GW1-1, t-1208, t-1209 |
| `findings/20261024-smeshannye-iskhody-v-odnom-keyse.md` | находка | один кейс не держит смесь исходов: зелёная партиция рядом с красной по багу отказана `partial-green`, «заблокировано упавшей» — не состояние, остаток Then только «человеку» | `s5_precheck.py`, `contract.py`, `acceptance.py`, `window_record.py`, `ledger.py`, `traceability.py`, `check_delivery.py` | GW1-22, ожидает | вопрос 24.10.2026 (поведение) | GW1-14, GW1-8, t-1216 |
| `findings/20261025-krasnyj-test-bez-raspiski-okna.md` | находка | красный по требованию тест не получает расписку ревью окна S5, окно закрывается только словом человека | `window_record.py`, `acceptance.py`, `contract.py`, `controller.py`, `stage_done.py` | GW1-23, ожидает | да (25.10: красный — исход по умолчанию) | t-1225; GW1-22; GW1-14; EP1-16 |
| `findings/20261027-gate-check-stand-factory-owned-kak-vybor-cheloveka.md` | находка | `check_stand` превращает `missing` с владельцем `factory` в PERSON_DECIDES «fix the stand first, or let the stage run» | `scripts/gate_preflight.py` | GW1-24, ожидает | нет | t-1365 Q2; FR-3 |
| **Гейт A прогона 12586: разбор текста (28.10.2026, t-1449)** | | | | | | |
| `findings/20261028-gejt-a-varianty-q7-pereputany-mestami.md` | находка, id — | варианты Q7 перепутаны: `Q7: a` даёт в TC-014 утверждение чтения b; молчаливая инверсия оракула (FR-10) | `scripts/gate_brief.py`, `agents/qa-case-designer.md`, `scripts/planning_contract.py` | GW1-25, ожидает | нет | P20, FR-58 |
| `findings/20261028-gejt-a-povtorno-sprashivaet-otvechennoe-matritsa-protivorechij.md` | находка, id — | R-3, R-5, R-1 спрошены повторно после Q1 b, Q2 a, Q4 a: вопросы матрицы противоречий не читают ответы (FR-7) | `scripts/gate_preflight.py`, `scripts/gate_brief.py`, `scripts/planning_contract.py`, `scripts/question_register.py` | GW1-26, ожидает | нет | GW1-21 |
| `findings/20261028-gejt-a-predusloviya-sprashivaet-izvestnoe-i-ne-daet-dorogi.md` | находка, id — | предусловия: URL UI и флаг MS Teams фабрика знает сама; по аккаунтам не сказано, где и в каком виде дать (FR-50) | `scripts/gate_preflight.py`, `scripts/gate_brief.py`, `scripts/env_probe.py` | GW1-27, ожидает | нет | GW1-13, B-280 |
| `findings/20261028-gejt-a-skip-stroka-plana-tehnicheskoj-frazoj.md` | находка, id — | строка плана `skip` (TS-13) подана жаргоном: не названы три непроверенных риска и чем они прикрыты (P9, FR-6) | `scripts/gate_brief.py`, `scripts/gate_preflight.py` | GW1-28, ожидает | нет | GW1-29 |
| `findings/20261028-gejt-a-probnyj-test-otchyota-vybor-fabriki-cheloveku.md` | находка, id — | пробный тест отчёта: фабрика отказывается выбирать при общем корне профилей и отдаёт человеку имя ключа конфига (FR-3) | `scripts/gate_preflight.py` (`_choose_test`) | GW1-28, ожидает | нет | GW1-24 |
| `findings/20261028-gejt-a-plan-sam-sebe-protivorechit-pro-e2e-ts-8.md` | находка, id — | e2e TS-8: проза плана «высший риск», поля `moderate/medium/normal`; детектор верит полям, человеку отдан спор плана с собой (FR-10, FR-38) | `scripts/planning_contract.py`, `scripts/gate_brief.py`, `agents/qa-test-strategist.md` | GW1-29, ожидает | нет | GW1-11 |
| `findings/20261028-gejt-a-vetka-testov-pravki-fabriki-kak-vybor-cheloveka.md` | находка, id — | две незакоммиченные правки в ветке тестов — собственные файлы фабрики, человеку предложено «закоммитить / спрятать / идти» (FR-3) | `scripts/gate_preflight.py` | GW1-30, ожидает | нет | GW1-24 |
| `findings/20261028-gejt-a-stena-klyuchej-integracij-bez-kejsov.md` | находка, id — | 14 пунктов ключей интеграций стеной без привязки к кейсам; ненужные кейсам ключи не уходят в отчёт по умолчанию (P5, D-0043) | `scripts/gate_preflight.py`, `scripts/gate_brief.py`, `scripts/stand_gaps.py` | GW1-31, ожидает | нет | GW1-13, GW1-15, GW1-16, GW1-17 |
| `findings/20261028-gejt-a-pyat-form-otveta-v-odnom-pakete.md` | находка, id — | пять форм ответа в одном пакете; человек не знает, какие слова читает код, а какие «помощник» (P9, FR-6) | `scripts/gate_brief.py`, `scripts/person_words.py` | GW1-32, ожидает | нет | GW1-11, GW1-21 |
| **Находки ночного прогона 14857 (0.10.6), 30.10.2026** | | | | | | |
| `findings/20261030-otvet-approve-s-punktami-ne-zapisyvaetsya-dve-dorogi-dva-slova.md` | находка, id — | «approve» плюс ответы на пункты не записывается: нечитанные строки отправляют весь ответ дирижёру; `approve as is` — только на одной дороге | `scripts/story_run.py`, `scripts/person_words.py`, `scripts/gate_brief.py` | GW1-33, ожидает | нет | GW1-32; t-1605 #5; AR-15 |
| `findings/20261030-svobodnyj-otvet-na-vopros-reestra-bez-chitatelya-na-doroge-drajvera.md` | находка, id — | свободный ответ на вопрос реестра (Q3) на дороге драйвера не прочитан: условные строки плана ушли в skip, отчёт печатает сырой текст | `scripts/story_run.py`, `scripts/person_words.py`, `scripts/planning_contract.py` | GW1-34, ожидает | нет | DC1-19; TQ1-20; t-1605 #6 |
| `findings/20261030-gejt-b-paket-67805-b-i-pomechennye-problemy-vopros-vse-ravno-zadan.md` | находка, id — | пакет гейта B 67 805 байт; пометки нарушений `human-questions.md` (`--label`, `exit 1`) не мешают показу | `scripts/gate_brief.py`, `scripts/story_run.py` | GW1-35, ожидает | нет | C3-16; `conductor`; t-1605 #26 |
| `findings/20261030-accept-po-integracii-ne-dohodit-do-pozdnej-stroki-s5-blocked-by-env.md` | находка, id — | `accept` по пропуску интеграции не доходит до поздней строки S5: нужно поле `integration` на `blocked_by_env` (остаток GW1-15, половина (1) сужена, не закрыта) | `scripts/gate_preflight.py`, `scripts/stand_gaps.py` | пачка 1, GW1-36 | да — подтвердить перенос остатка GW1-15 | GW1-15; HF1-9 |
| `findings/20261030-staryj-perenos-otveta-sprashivaet-odin-raz-posle-smeny-formy-id.md` | находка, id — | перенос ответа старого прогона спросит человека ещё раз: `_c5` не вычитает идентификаторы с `accept` | `scripts/stand_gaps.py` | пачка 1, GW1-37 | нет (решает Lead) | GW1-15; критик S1c F-7 |
| `findings/20261030-config-json-chitayut-bez-bom-sem-chitatelej-sosedi-gw1-19.md` | находка, id — | `config.json` читают без BOM семь читателей, кроме тех, что поправил GW1-19 | `scripts/check_coverage.py`, `scripts/environment_record.py`, `scripts/report_adapt.py`, … | пачка 1, GW1-38 | нет | GW1-19 |
| `findings/20261031-obhod-ograzhdenij-v-otvete-cheloveka-odin-iterator-dlya-vseh-chitatelej.md` | находка | обход ограждений в строках ответа человека один в `question_register`; читатели `planning_contract` и `gate_brief` не обойдены | `scripts/question_register.py`, `scripts/planning_contract.py`, `scripts/gate_brief.py` | пачка 1, GW1-39 | нет | S4c F-10; GW1-32 |
| **Находки 31.10.2026 (прогон CART-1, MyBooks)** | | | | | | |
| `findings/20261031-trebovanie-v-not-planned-zabor-na-vykhode-s3.md` | находка, id —, кандидат наверх | требование реестра не уходит в «Not planned»; вопрос гейта A без строки-исполнителя не задаётся (свод п. 3.1) | `scripts/planning_contract.py`, `scripts/gate_preflight.py`, `scripts/story_run.py`, `agents/qa-test-strategist.md` | GW1-41, ожидает | да, 31.10.2026 («забор») | GW1-29, GW1-34, GW1-21; `grounding` Н-2 |
| `findings/20261031-otvet-q-bukva-s-khvostom-ne-zapisan-otchyot-govorit-net-otveta.md` | находка, id — | ответ «Q1: a (…)» не токен; отчёт говорит «ответа нет» вместо «строка не понята» (свод п. 3.2) | `scripts/question_register.py`, `scripts/report_facts.py`, `scripts/gate_brief.py` | GW1-42, ожидает | нет | GW1-21, GW1-34 |
| `findings/20261031-otvechennoe-reshenie-klassa-sprashivaetsya-snova-na-sleduyushchem-okne.md` | находка, id —, кандидат наверх | решение класса («без пробы», «версия стенда») спрашивается на каждом окне и стадии; склейка 3.3 + 3.4 | `scripts/waiver.py`, `references/decision-classes.json`, `scripts/gate_preflight.py` | GW1-43, ожидает | нет (P5, D-0043 даны) | GW1-1, GW1-26; `execution-probes` EP1-28 |
| `findings/20261031-variant-voprosa-bez-ispolnitelya-recommended-bez-proverki.md` | находка, id — | вариант вопроса помечен «Recommended» без проверки исполнителя (`key_pattern` адаптер не читает) (свод п. 2.2) | `scripts/person_words.py`, `scripts/gate_brief.py`, текст дирижёра | GW1-44, ожидает | нет | GW1-32; `stand-and-sources` 2.1 |
| `findings/20261031-slova-cheloveka-ne-perenosyatsya-pri-perezapuske-pod-novym-klyuchom.md` | находка, id — | слова человека привязаны к ключу истории; перезапуск под новым ключом спрашивает заново (свод п. 2.6) | `scripts/waiver.py`, `scripts/story_step.py` или `controller.py` | GW1-40, ожидает | нет | GW1-1, GW1-43; `stand-and-sources` 2.1 |
| **Очередь релиза 0.10.8 (критики t-520, t-542, t-565; t-567)** | | | | | | |
| `findings/20261031-stroka-punkta-gejta-a-id-svobodnye-slova-bez-chitatelya.md` | находка, id — | строка пункта гейта A `vcs-1: <слова>` не читается; свободные слова идут дирижёру под своим пунктом (t-542 F7) | `scripts/story_run.py`, `scripts/gate_preflight.py` | GW1-45, ожидает | нет | GW1-33, GW1-32 |
| `findings/20261031-zapolnitel-chast-stroki-v-dveryakh-bloka-priglashaet-obrezat.md` | находка, id — | `<part of the line>` в шести дверях приглашает обрезать; одна константа | `scripts/person_words.py`, `scripts/controller.py`, `scripts/s5_precheck.py` и др. | GW1-46, ожидает | нет | GW1-1 |
| `findings/20261031-gejt-a-stroka-voprosa-bez-registra-i-s-drugim-razdelitelem-ne-vidna.md` | находка, id — | бродячая строка вопроса без регистра и с другим разделителем не видна (t-542 F8) | `scripts/question_register.py` | GW1-47, ожидает | нет | GW1-34 |
| `findings/20261031-kartochka-plana-strateg-sudil-tak-bez-dokazatelstva.md` | находка, id — | карточка «стратег судил так» без носителя (t-542 F11) | `scripts/gate_brief.py` | GW1-48, ожидает | нет | GW1-29 |
| `findings/20261031-plan-warnings-padaet-na-spiske-v-pole-i-mertvaya-zashchita-note.md` | находка, id — | `plan_warnings` падает на списке в закрытом поле; мёртвый `getattr` (t-542 F12) | `scripts/planning_contract.py`, `scripts/gate_brief.py`, `scripts/story_run.py` | GW1-49, ожидает | нет | GW1-29 |
| `findings/20261031-gejt-b-bez-stroki-odobreniya.md` | находка, id — | гейт B без строки «что вы одобряете» (t-520 G6) | `scripts/gate_brief.py` | GW1-50, ожидает | нет | GW1-11 |
| `findings/20261031-stroka-plana-ssylka-na-kejs-bez-testa.md` | находка, id — | ссылка строки плана на кейс без теста (t-520 G7, п. 4 находки GW1-11) | `scripts/render_case_appendix.py` | GW1-51, ожидает | нет | GW1-11 |
| `findings/20261031-names-whole-pravyj-kraj-vrazhdebnyj-variant-prohodit.md` | находка, id — | `names_whole` пропускает `test_x[-1]`, `PC-1@TC_002`, `tests\a\b.py` (t-565 G-2) | `scripts/contract.py` | GW1-52, ожидает | нет | GW1-1 |
| `findings/20261101-ga-4-dg-2-krasnye-na-baze-ssylki-na-dokumenty.md` | находка, id — | `test_gate_brief_attachments.py` GA-4 и DG-2 красные на базе релиза: ссылка на документ не найдена в карточке гейта A | `scripts/gate_preflight.py`, `scripts/gate_brief.py` | GW1-53, ожидает | нет | GW1-32 |
| `findings/20261101-waiver-stage-prinimaet-sokrashchenie-flaga.md` | находка, id — | `waiver.py` принимает `--stag` как `--stage`: нет `allow_abbrev=False` и охранного теста (t-303 F3) | `scripts/waiver.py` | GW1-54, ожидает | нет | GW1-1, GW1-40 |

## Входящие

`findings/` этой кучки; находку, не названную ни в одной пачке, называет `piles.py check --all` (е).
По теме в других кучках: `conductor/findings/` и `conductor/batch-1-p22-seams.md` (узлы C1-1…C1-4, формы вопроса и гейт B).

## Вопросы владельцу

- нет (основание: «Решение владельца нужно: да» — 0 из 20 находок, дайджест t-713 п. 5; решения по гейту B 02.10, по B-292 (г) 03.10 и по P22 09.10 уже даны).
