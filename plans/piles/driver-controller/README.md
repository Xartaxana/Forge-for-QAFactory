# Драйвер и контроллер (`driver-controller`)

приоритет: П2 | фичи: F05, F06 | стенд: частично | зона: `ai-packages/qa-factory/scripts/controller.py`, `scripts/event_store.py`, `scripts/manifest_put.py`, `scripts/stage_done.py`, `scripts/worker_lifecycle.py`, `scripts/dispatch_liveness.py`, `scripts/story_progress.py`, `scripts/story_run.py`, `scripts/ticket_adapter.py`, `scripts/hooklib.py`, `scripts/onboard_apply.py`, `scripts/repair_route.py`, `skills/qa-story/phases/*.md`

## Зачем

Сегодня headless-прогон местами теряет работу на стыках: принятый возврат роли устаревает оттого, что
квитанция сама сдвинула ревизию журнала; исключение после записи оставляет стадию без хвоста и без отказа;
контроллер может выбрать старый возврат вместо новой работы и предложить перезапуск на закрытой истории без
вопроса человеку; исчезнувший драйвер с чужой свежей квитанцией выглядит живым. После первой пачки следующий
шаг контроллера верен, живость роли доказуема, «гейт A одобрен» и свежесть тикета читаются одинаково, у
проекта в подпапке git один «верх».

## Что не так сегодня (факты)

- Тест `receipt_projection_does_not_make_a_returned_acceptance_stale` падает с `StateConflict: stale expected revision` (`plans/BACKLOG.md:332`).
- Тест `a_newer_unlaunched_dispatch_outranks_an_older_return`: 39 из 41, ждали `relaunch`, получили `resolve_return` (`plans/BACKLOG.md:333`).
- Закрытая история плюс открытая S6 плюс незапущенный qa-runner дают `relaunch` без вопроса человеку (`plans/BACKLOG.md:355`; находка 09.10, Lead сверил `story_run.py:7986-8012` на 09.10).
- Три дыры хвоста после коммита (`plans/BACKLOG.md:403-405`); четыре копии «гейт A одобрен» и пять читателей «верха git» (`plans/BACKLOG.md:441`, `plans/BACKLOG.md:455`; номера строк кода названы на 05–09.10).
- 16 открытых строк в пачке 1 и 28 находок (дайджест `docs/tasks/specs/reports/t-712-scout-piles-a.md`, пересчёт 28 из 28 на 13.10).

## Пачки

| № | Что изменится для пользователя | Строки | Размер | Статус | Взял | Ветка | MR |
|---|---|---|---|---|---|---|---|
| 1 | headless-прогон не теряет стадии при возобновлении, живость роли доказуема, свежесть тикета одна на оба пути, следующий шаг контроллера всегда верный | B-331 | M | закрыта | — | — | `855d4e5c` |

Открытое перенесено 01.11.2026 → release-next/1, words-gates/1, driver-hosts/1, execution-report/1, onboarding-forge/1, driver-hosts/2, execution-report/2, onboarding-forge/2.

Статусы пачки: `ожидает` → `в работе` → `сдано` → `принято` → `закрыта`. Размер — по узлам: S ≤ 4 узлов,
M 5–9, L 10–15 (больше — две пачки). Взятая пачка заморожена: её файл правит только взявший, новое
по теме — файлом в `findings/`.

## Бриф пачки 1

Начать с DC1-1 (ревизия и приёмка возврата); DC1-6 и DC1-7 идут последними и по очереди (оба пишут `story_run.py`);
стенд — только для DC1-7 (живые доказательства подпапки git). Ждёт: очередь за `conductor/1` по `controller.py` и
`story_run.py`; слово владельца не нужно. Подробно — `batch-1-controller-seams.md`, раздел «Бриф».

## Дороги

Читать по порядку: эта карточка → `batch-1-controller-seams.md` → находки узла (колонка «id / файл» ниже) →
строки `plans/BACKLOG.md` 332, 333, 340, 341, 354, 355, 359, 388, 402–405, 440, 441, 455, 456 → код зоны по
функциям из «Слов» → `ai-packages/qa-factory/design/controller-paths.md`, `design/driver.md`,
`design/state-exits.md`, `design/controller-blocks.md` (разделы — проверить по файлу) → `docs/factory-map/qa-factory-paths.md`
§12 (роль умерла, dispatch завис), §13 (изменения после гейта A), §15 (документация и driver расходятся) →
`docs/SIBLING_MAP.md` Axis 5, Axis 8, Axis 10 («git-top readers»).
Слова: `plans/features.json` F05, F06 (поле `words`) и сверх них: `stale expected revision`, `StateConflict`,
`DerivedViewStale`, `ProjectionStale`, `EventCommitted`, `_after_commit`, `_run_after_commit`, `refresh_derived`,
`record_return`, `resolve_return`, `_next_action_for_state`, `relaunchable`, `superseded`, `unlaunched`,
`retry_packets`, `parent_retry`, `NEVER_STARTED`, `role_stops`, `dispatch_id`, `SubagentStop`, `print_boundary_notice`,
`story_budget_stop`, `owed`, `check_is_due`, `ticket_rework`, `semantic_reopen`, `_current_gate_a`, `gate_series`,
`FUTURE_SLACK_SECONDS`, `_CLOCK_SKEW_S`, `git_route`, `project_root`, `show-toplevel`; «ревизия», «квитанция»,
«живость», «следующее действие», «свежесть тикета», «верх git».
Не читать: зону `conductor` (кроме строки C1-6 в `conductor/batch-1-p22-seams.md`), `hooklib.py` вне `:51-124`,
зоны `onboarding-hooks` и `package-ci` (кроме их находки «проект в подпапке git» — `package-ci/findings/B-412-proekt-v-podpapke-git-repozitoriya-monorepo.md`).

## Содержание

Снимок 13.10.2026; пути — от `ai-packages/qa-factory/scripts/`; суть строк — из `plans/BACKLOG.md`, находок — из дайджеста t-712. При расхождении авторитетны файлы пачек.

| id / файл | вид | суть (≤ 20 слов) | пути | статус | слово владельца | связи |
|---|---|---|---|---|---|---|
| **Пачка 1** | | | | | | |
| `findings/20261026-starye-puti-readiness-i-obligations-v-pakete.md` | находка | дашборд называет человеку `state/obligations.md`; `stages.json` — старый `project:readiness.json` | `factory_dashboard.py`, `references/stages.json`, `brief_pack.py` | пачка 1, DC1-10 | да, 26.10.2026 (внести) | из `kb/1` (критик t-1147) |
| B-311 | строка | приёмка возврата устаревает: квитанция SubagentStop сама сдвинула ревизию журнала | `controller.py`, `event_store.py` | пачка 1, DC1-1 | нет | — |
| B-317 | строка | коммиты `manifest_put` двигают ревизию без проекции контроллера | `manifest_put.py` | пачка 1, DC1-1 | нет | — |
| B-382 | строка | `record_return` ловит только `DerivedViewStale`; `ProjectionStale` → хук пишет «не записано» | `controller.py`, `event_store.py` | пачка 1, DC1-1 | нет | — |
| B-383 | строка | `_after_commit` ловит фиксированный список; прочее оставляет стадию без хвоста | `controller.py` | пачка 1, DC1-2 | нет | — |
| B-384 | строка | устаревший вид после коммита `stage_done` пропускает уведомление границы и стоп бюджета | `stage_done.py` | пачка 1, DC1-2 | нет | — |
| B-385 | строка | `_run_after_commit` пропускает простой `StateConflict` без типа семейства | `event_store.py` | пачка 1, DC1-2 | нет | метка F16 |
| B-312 | строка | новая незапущенная диспетчеризация стадии важнее старого возврата | `controller.py` | пачка 1, DC1-3 | нет | — |
| B-330 | строка | гонка ревизии checkpoint/release, `retry_packets`, два окна S5, `parent_retry` | `controller.py` | пачка 1, DC1-3 | нет | п. (1) — родня DC1-1 |
| B-316 | строка | отказ без `dispatch_id` и поздняя диспетчеризация: сначала воспроизводящий тест, потом решение | `controller.py` | пачка 1, DC1-4 | нет (решение Lead) | — |
| B-335 | строка | Codex: квитанция без `dispatch_id` блокирует роль; `NEVER_STARTED` молчит на пути драйвера | `worker_lifecycle.py`, `story_run.py` | пачка 1, DC1-4 | нет | — |
| B-366 | строка | «pid драйвера исчез, чужая квитанция свежая» читается «жив»; решить чтение | проверить по коду | пачка 1, DC1-4 | нет (решение Lead) | — |
| B-331 | строка | закрытая история, открытая не-ретро стадия: `next` даёт `relaunch` без вопроса | `controller.py`, `story_run.py` | пачка 1, DC1-5 (сверка с `conductor` C1-6) | дано 09.10 | `conductor` C1-6 |
| `findings/20261009-b-331-vopros-cheloveku-pered-relaunch.md` | находка, id — | спека слова 09.10: вопрос с тремя ответами перед перезапуском, тесты | `controller.py`, `story_run.py` | пачка 1, DC1-5; при close удалить (id «—», код не удалит) | дано 09.10 | `forge/findings/20261009-b-331-zakryt-kommentariem.md` |
| B-421 | строка | остатки свежести тикета на драйвере: `owed`, код выхода 2, `check_is_due`, окна падения | `story_run.py`, `ticket_adapter.py` | пачка 1, DC1-6 | нет | F06 |
| B-422 | строка | одно чтение «гейт A одобрен» вместо четырёх копий, одна константа часов | `story_run.py`, `controller.py`, `dispatch_liveness.py` | пачка 1, DC1-6 | нет | F06 |
| B-437 | строка | один публичный читатель «верха git» вместо пяти | `hooklib.py`, `onboard_apply.py` | пачка 1, DC1-7 | нет | SIBLING_MAP Axis 10 |
| B-438 | строка | остатки подпапки git: R1e/R1f, печать «как факт», живые доказательства 1–3 | `story_run.py` | пачка 1, DC1-7 | нет | `package-ci` (подпапка git) |
| **Живость и следующее действие (кандидат пачки 2)** | | | | | | |
| `findings/B-342-zhivost-ostatki-posle-volny-5-kritik.md` | находка | шесть остатков живости после волны 5: фраза при `unknown`, отказ без двери, `stage: None` | `story_run.py`, `controller.py` | кандидат пачки 2 | нет | `onboarding-hooks` |
| `findings/B-268-zhivost-roli-pod-drayverom-nedokazuema-stroka.md` | находка | драйвер пишет `in_flight {pid}` до запуска роли; живость по pid | `dispatch_liveness.py`, `story_progress.py` | кандидат пачки 2 | нет | — |
| `findings/B-048-zhivost-dispatcha-bez-dokazatelstv-unknown.md` | находка | живость без доказательств = `unknown`; дверь `resolve_return` дирижёру | — | кандидат пачки 2 | нет | `package-ci` (нагрузка) |
| `findings/B-132-legacy-stori-u-importirovannoy-zadachi-net.md` | находка | у импортированной legacy-стори нет принятого критика старых окон | — | кандидат пачки 2 | нет | — |
| **Возобновление и путь результата** | | | | | | |
| `findings/B-265-sokhranennyy-rezultat-roli-zakryvaet-stadiyu.md` | находка | сохранённый результат закрывает стадию поверх вопросов; один `finish_saved()` | `story_run.py` | открыто | нет | — |
| `findings/B-273-vozobnovleniya-roli-prichina-v-log-odnoy.md` | находка | `resume_reason` в лог, форма передачи кодом, доля возобновлений | — | перенос: speed-cost/1 (SC1-1) | «ок» 02.10 (дайджест t-712) | — |
| `findings/B-287-sobrannyy-put-artefakta-posledniy.md` | находка | путь артефакта: поле формы первое, проза только при пустом поле | `story_run.py` | открыто | нет | — |
| `findings/B-167-rezhim-progona-b-014-proveryaetsya-tolko-pri.md` | находка | режим прогона проверяется только при старте; стадии упираются в отказ | `story_run.py` | открыто | нет | — |
| `findings/B-170-s6-pri-vsekh-svezhikh-rezultatakh-i.md` | находка | S6: ручной блок недостижим, `relaunch` идёт мимо свежести | `story_run.py` | открыто | нет | — |
| `findings/B-178-story-run-py-pri-vyvode-v-fayl-start-process.md` | находка | построчный вывод лога при записи в файл (FR-43) | `story_run.py` | похоже сделано: `plans/BACKLOG.md:247` — проверить по коду | нет | — |
| `findings/B-395-dokstring-story-run-py-okolo-strok-661-669.md` | находка | докстринг про `words_file` преувеличивает: пять мест передают `--decision` встроенно | `story_run.py` | открыто | нет | — |
| `findings/B-251-sostoyanie-stori-ne-perenosimo-mezhdu-kopiyami.md` | находка | абсолютные `known_paths` в пакетах; состояние не переносимо между копиями | `controller.py` | открыто | нет | — |
| `findings/B-293-golden-drayvera-t-301-n0-t-337.md` | находка | golden драйвера: перезаписать с HEAD, кап трассы, `AMBIENT_SCRUB`, шесть пунктов | `tests/test_infra_failure.py` | открыто | нет | `package-ci` (`MANIFEST.json`) |
| `findings/B-327-brif-roli-ne-pokazyvaet-privyazku-versiy.md` | находка | бриф роли не показывает привязку версий кейсов; решить, какая главнее | — | открыто | нет | — |
| **Свежесть, стенд, невызываемые шаги** | | | | | | |
| `findings/B-042-shagi-kotorye-driver-ne-vyzyvaet-ticket-adapter.md` | находка | драйвер не вызывает `ticket_adapter diff`, `--close-gate-b`, post-retro MR | `ticket_adapter.py` | часть про свежесть: родитель закрыт (`plans/BACKLOG.md:572`), прочее открыто | нет | — |
| `findings/B-145-stend-nazvannyy-chelovekom-na-revyu-s1.md` | находка | стенд, названный на ревью S1, не доходит до `pipeline.environment` | `story_run.py` | открыто | нет | — |
| **Роль дирижёра и маршруты (граница с `conductor`)** | | | | | | |
| `findings/B-006-ruchnoy-marshrut-s4-s6-dlya-stori-bez.md` | находка | законный исход «сдача без автоматизации» при пустом скоупе S5 | `story_run.py` | отсрочка «до сравнительного прогона» — прогоны cmp1..cmp3 закрыты? проверить | 29.09 (отсрочка) | — |
| `findings/B-040-tsikl-s7-posle-fiksa-zvat-analitika.md` | находка | S7: читать `fix_result` из `triage.json`, звать аналитика после фикса | — | открыто | нет | — |
| `findings/B-041-vopros-s9-ne-ostanavlivaet-until-end.md` | находка | вопрос S9 и `--until end`: описать `--answer skip` | `phases/s9.md` | открыто | нет | — |
| `findings/B-045-schetchiki-povtorov-v-odnom-meste-runtime-policy.md` | находка | счётчики повторов вынести в `runtime_policy` | — | открыто | нет | — |
| `findings/B-046-dirizher-pomoshchnik-pri-problemakh-svoy.md` | находка | дирижёр-помощник: свой промпт, команда до вопроса, бюджет остановок | — | открыто | нет | `conductor` (P22) |
| `findings/B-050-edinyy-kriteriy-kritichno-ne-kritichno.md` | находка | единый критерий «критично / не критично» для ответа вне вариантов | — | открыто | нет | `conductor` (P22) |
| `findings/B-051-karta-proekta-i-osi-simmetrii-v.md` | находка | карта проекта и оси симметрии в пакете по-английски | — | открыто | нет | — |
| `findings/B-261-dve-golovy-fabriki-skill-qa-story-orkestrator.md` | находка | две головы — скилл и драйвер; `phases/*.md` ретируются | `phases/*.md`, `story_run.py` | открыто | нет | — |
| `findings/B-264-fabrika-edet-kak-mozhno-dolshe-ne.md` | находка | едет дольше, не беспокоя человека; вопросы пачкой на границе | `stage_done.py` | открыто | нет | `conductor` (P22) |
| `findings/20261010-puti-ponizheniya-stadii-i-start-pervogo-progona.md` | находка | пути понижения стадии не сведены на `lower_stage`/`stale_records`; `started` стадии переживает повторный прогон | `controller.py`, `stage_done.py` | пачка 1, DC1-8 | нет | из `forge` (F5-11) |
| **Тесты пакета** | | | | | | |
| `findings/B-214-sosedi-b-155-testovye-fayly-paketa.md` | находка | тестовые файлы выше порога 90 с: разбить или ускорить | `tests/test_infra_failure.py` | числа устарели (`plans/BACKLOG.md:247`) | нет | `package-ci` |
| `findings/20261025-cikl-okna-s5-25-minut-upravleniya.md` | находка | цикл окна S5 «диспатч → handback → гейт → дирижёр» ≈ 25 мин на окно, шаги `story_step` подорожали в 2–10 раз | `story_step.py`, `controller.py`, `exit_gate.py`, `s5.md` | DC1-9, ожидает | вопрос 24–25.10.2026 (поведение) | t-1221; EP1-17; CD1-14 |
| **Находки прогона 14857 (0.10.2), 27.10.2026** | | | | | | |
| `findings/20261027-identichnost-dispatcha-teryaetsya-pri-povtornom-ispolzovanii-sessii-agenta.md` | находка | A2: идентичность диспатча теряется при повторном использовании сессии агента; `bind` перезаписывает, `TURN BUDGET` считает по сессии | `scripts/story_step.py`, `scripts/factory_dashboard.py`, `scripts/telemetry_hook.py` | пачка 1, DC1-11 | нет | A1 |
| `findings/20261027-skill-road-manual-block-parity.md` | находка | паритет ручного блока S6 дороги скилла и драйвера: ручные строки промпта, `stand_login_gate`, `manual_close`, E30 | `story_run.py`, `story_step.py`, `manual_evidence.py`, `phases/s6.md` | пачка 1, DC1-12 | нет | t-1361, t-1367 (F-7) |
| `findings/20261027-ticket-rework-s6-bez-cases.md` | находка | `ticket_rework_step` на S6 передаёт `cases=[]`, контроллер отказывает | `story_run.py`, `controller.py` | пачка 1, DC1-13 | нет | t-1361, DC1-12 |
| `findings/20261027-story-progress-manual-blocks.md` | находка | `_block_position` дедупит блоки по кортежу кейсов и сам делит `ceil(len/5)`: третье место правила (AR-15) | `story_progress.py` | пачка 1, DC1-14 | нет | t-1361, t-1367 (E29) |
| `findings/20261027-start-prepare-avtomatizaciya-bez-proverki-chlenstva.md` | находка | `start`/`prepare` автоматизационной половины S6 не проверяют принадлежность кейса половине, у ручной проверка есть (FB-9) | `controller.py`, `story_step.py`, `story_run.py` | пачка 1, DC1-15 | нет | t-1393, t-1385; DC1-12, DC1-13 |
| **Отзыв пользователя, 28.10.2026** | | | | | | |
| `findings/20261028-otkaz-vozobnovleniya-ne-nazyvaet-dver.md` | находка | отказ возобновления агента, не привязанного к стори, не называет двери (`bind` / новый диспатч); стратег с пустой формой не вернулся — полный перезапуск | `stage_guard.py`, `story_step.py` | пачка 1, DC1-16 | «не в 0.10.5, в пачки» (28.10.2026) | отзыв Dev6 (TP2-2702), t-1553; DC1-11 |
| **Находки прогона 14857 (0.10.5), 29.10.2026** | | | | | | |
| `findings/20261029-start-s3-ne-otkazyvaet-bez-prepare.md` | находка | `start --stage S3` не отказывает без prepare-выходов и `--purpose s3_labelling`: фантомный диспатч | `scripts/story_step.py` | пачка 1, DC1-17 | нет (П2 — решение Lead) | DC1-15 |
| `findings/20261029-gejt-s3-nahodit-odnu-stroku-v-dva-prohoda.md` | находка | гейт S3 находит проблемы строки TS-2 в два прохода, вторую пишет после принятия: лишний диспатч доработки | `scripts/planning_contract.py`, `scripts/stage_done.py` | пачка 1, DC1-18 | нет (П1 0.10.7 — решение Lead) | HF8-24, HF9-1, DC1-9 |
| **Находки прогона 14857 (0.10.5), 30.10.2026** | | | | | | |
| `findings/20261030-doroga-dirizhyora-ne-zapisyvaet-otvety-cheloveka-na-voprosy-gejta.md` | находка | `gate-decision` на дороге дирижёра не записывает `Q<n>: <буква>` гейтов A и B (это делает только драйвер); дирижёр ложно сказал «записано» | `scripts/controller.py`, `scripts/planning_contract.py`, `scripts/story_run.py`, `skills/qa-story/phases/s4.md`, `skills/qa-story/phases/s8.md` | пачка 1, DC1-19 | нет (слово владельца 30.10.2026: П1, релиз 0.10.7) | t-1598; SC5-2; DC1-12; `hotfix-12586/findings/20261028-ruchnye-testy-trebuyut-pereotkryt-geyt-a.md` |
| **Находки ночного прогона 14857 (0.10.6), 30.10.2026** | | | | | | |
| `findings/20261030-otkaz-kritika-okna-s5-quittanciya-i-vozvrat-avtoru-ostatki.md` | находка | квитанция отказанному окну починена (t-1603), но петля не доказана целиком; хвосты F3–F5 критика t-1604 | `scripts/window_record.py`, `scripts/controller.py` | пачка 1, DC1-20 | нет | t-1604; t-1605 #1; DC1-21 |
| `findings/20261030-kap-okna-tratitsya-na-otkaz-samoj-fabriki-bez-kvitancii.md` | находка | кап раундов окна (на ключ окна) тратится раундами дирижёра на отказ самой фабрики без квитанции | `scripts/story_run.py` | пачка 1, DC1-21 | нет | t-1605 #3; DC1-20; HF8-15 |
| `findings/20261030-kap-remonta-s5-schitaet-raundy-bez-test-defect.md` | находка | кап ремонта S5 считает раунды без причины `test_defect`; человеку предложен `round`, который не лечит | `scripts/controller.py`, `scripts/story_run.py` | пачка 1, DC1-22 | нет | t-1605 #4; TQ1-23; DC1-21 |
| `findings/20261030-s9-cikl-report-check-rebuild-report-bez-predela.md` | находка | S9 `report_check → rebuild_report` позвал аналитика 7 раз после принятия: отказ с действием, которое не лечит причину, без предела | `scripts/story_run.py`, `scripts/controller.py` | пачка 1, DC1-23 | нет | t-1605 #8; HF8-17; HF8-22 |
| `findings/20261030-duration-ms-stroki-drajvera-ne-vremya-sessii.md` | находка | `duration_ms` строки журнала драйвера — не время сессии (21.5 мин против 6075) | `scripts/driver_journal.py`, `scripts/factory_dashboard.py` | пачка 1, DC1-24 | нет | t-1605 #22; CD1-27 |
| `findings/20261030-case-defect-net-v-drajvere-verdikt-bez-ispolnitelya.md` | находка | `CASE_DEFECT` нигде не встречается в `story_run.py`: вердикт, требующий хода, без исполнителя на дороге драйвера | `scripts/story_run.py` | пачка 1, DC1-25 | нет | цикл S7 после фикса; критик S5b rest |
| `findings/20261030-karta-sloev-drajvera-ne-pospevaet-za-kodom.md` | находка | `test_driver_layers` красный на базе 0.10.7 (L1 ×4, L4, L8): карта слоёв отстаёт от кода | `scripts/tests/test_driver_layers.py` | пачка 1, DC1-26 | нет | HF8-18; критик диффа |
| `findings/20261030-dvojniki-s4c-otvet-gejta-kopii-i-prohody-kontrollera-v-testah.md` | находка | копия метки «Earlier answer», вторая таблица владельцев доработки, три прохода контроллера в тестах | `scripts/story_run.py`, `scripts/controller.py` | пачка 1, DC1-27 | нет | S4c N1/N2 |
| `findings/20261031-sendmessage-incomplete-agentu-prohodit-hotya-kontroller-govorit-net-konteksta.md` | находка | `SendMessage` агенту записи `incomplete` проходит, хотя контроллер говорит «no agent holds its context» | `scripts/stage_guard.py`, `scripts/controller.py` | пачка 1, DC1-28 | нет | S3c F-S3C-8; SC2-38 |
| `findings/20261101-ostatok-dc1-11-hody-po-dispatcham-i-odin-schyot-dispatchej.md` | находка, id — | остаток DC1-11: ходы по диспатчам и один счёт диспатчей (A2, критерии 1, 4, 5) не сделаны | `scripts/cost_capture.py`, `scripts/factory_dashboard.py` | пачка 1, DC1-29 | нет | DC1-11; CD1-18; hotfix-12586/7 |
| `findings/20261101-sf-6-avtomaticheskaya-ili-proveryaemaya-privyazka-id-agenta.md` | находка, id — | SF-6: привязка id агента к диспатчу остаётся на дисциплине дирижёра; неверный id внутри стори проходит гард | `scripts/host_dispatch.py`, `scripts/story_step.py` | пачка 1, DC1-30 | нет | DC1-16; SC2-18 |

## Входящие

`findings/` этой кучки; находку, не названную ни в одной пачке, называет `piles.py check` (е).
По теме в других кучках: `conductor/batch-1-p22-seams.md` узел C1-6 (закрытая история).

## Вопросы владельцу

- нет (основание: в дайджесте t-712 «Решение владельца нужно: да» — 0 из 28 находок, контроль на других кучках нашёл 6 файлов; слово 09.10 по закрытой истории уже дано).
