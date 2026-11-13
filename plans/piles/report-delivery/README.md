# Отчёт, доставка, трассировка (`report-delivery`)

приоритет: П1 | фичи: F08, F12, F13 | стенд: не нужен (CI + эталоны) | зона: `ai-packages/qa-factory/scripts/traceability.py`, `scripts/check_delivery.py`, `scripts/case_stamp.py`, `scripts/contract.py`, `scripts/ledger.py`, `scripts/validate_artifacts.py`, `scripts/delivery_summary.py`, `scripts/stage_guard.py`, `scripts/stand_gaps.py`, `scripts/story_run.py`, `references/delivery-reason-owners.json`, `handoffs/index.yaml`

## Зачем

Сегодня отчёт может показать зелёное там, где тест красный, сопоставить кейс с чужим прогоном по похожему номеру и не
назвать, кто виноват в недоставке: причины бывают записаны не на того владельца, а триаж S7 держится на нескольких
разных правилах «совпало». После первой пачки отчёт не показывает pass на красном, номера кейсов сопоставляются
точно, у каждой причины недоставки есть владелец, а триаж идёт по одному правилу.

## Что не так сегодня (факты)

- Таблица приложения отчёта показывала `pass` на красном: `instance_outcome` читал статус манифеста раньше результата прогона (`plans/BACKLOG.md:255`); по тексту `plans/BACKLOG.md:249` починка сделана (`case_stamp.red_run_for`), хэша в строке нет.
- Записи расходятся: строка `plans/BACKLOG.md:249` пишет «(а)–(в) закрыты, расхождений 0, было 20», а находка по хвостам починки называет остаток (а) открытым.
- Третий вердикт доставки реализован по `PROJECT.md` P21 (отменяет правило 0.7.9; ссылка на узлы t-305), но строка не закрыта и ещё пишет «ждут подтверждения владельца» (`plans/BACKLOG.md:210`).
- `traceability.decision_words` сопоставляет ключ кейса подстрокой: `TC-1` ложно совпадает с `PC-1@TC-10` (`plans/BACKLOG.md:394`).
- Исчерпанный лимит ремонта S5 закрывает стадию без решения, замечания критика кода не доезжают до отчёта (0 вхождений `test-code` в скриптах отчёта, находка 09.10); работу по ней ведёт `conductor`, узел C1-5.
- 14 открытых строк в пачке 1 и 22 находки (дайджест `docs/tasks/specs/reports/t-714-scout-piles-c.md`, пересчёт 14 из 14 и 22 из 22 на 13.10).

## Пачки

| № | Что изменится для пользователя | Строки | Размер | Статус | Взял | Ветка | MR |
|---|---|---|---|---|---|---|---|
| 1 | отчёт не показывает pass на красном, третий вердикт доставки, причины недоставки с владельцем, одна таблица триажа | B-303, B-308 (а), B-266 | M | закрыта | — | — | `855d4e5c` |
| 2 | строки отчёта называют обязательство и исход исполнения, а не шаг и ответ о требовании | — (находки 02.11.2026, 13.11.2026, узлы RD2-1, RD2-4) | S | ожидает | — | — | — |

Открытое перенесено 01.11.2026 → release-next/1, words-gates/1, execution-report/1, execution-report/2.

Статусы пачки: `ожидает` → `в работе` → `сдано` → `принято` → `закрыта`. Размер — по узлам: S ≤ 4 узлов,
M 5–9, L 10–15 (больше — две пачки). Взятая пачка заморожена: её файл правит только взявший, новое
по теме — файлом в `findings/`.

## Бриф пачки 1

Начать с RD1-1 (сверка по коду: что из «сделано по тексту» действительно сделано) — она сужает остальные узлы; RD1-2 и
RD1-3 независимы; RD1-4 и RD1-5 пишут `story_run.py`. Стенд не нужен — CI и эталонные отчёты; слово владельца нужно по
одному вопросу (см. «Вопросы владельцу»). Подробно — `batch-1-honest-report.md`, раздел «Бриф».

## Дороги

Читать по порядку: эта карточка → `batch-1-honest-report.md` → находки узла (колонка «id / файл» ниже) → строки
`plans/BACKLOG.md` 210, 214, 237, 249–255, 370, 375, 377, 386, 394, 448 → `PROJECT.md` P21 и P20 → код зоны по функциям
из «Слов» → `ai-packages/qa-factory/references/delivery-reason-owners.json`, `handoffs/index.yaml` →
`docs/factory-map/qa-factory-paths.md` (стадии S7–S9, доставка).
Слова: `plans/features.json` F08, F12, F13 (поле `words`) и сверх них: `instance_outcome`, `red_run_for`,
`case_matches`, `match_run_row`, `triage_row_for`, `decision_words`, `story_bugs`, `_pipeline_stages`, `reason_owner`,
`DELIVERY_REASON_OWNERS`, `OWNER_BY_TRIAGE_VERDICT`, `MANUAL_BLOCK_MAX`, `mark_handed`, `delivery_ready`,
`Left with you`, `Review gaps`, `handed_to_person`, `blocked_by_env`, `TRIAGE_VERDICTS`, `NOT_EXECUTED`, `ORACLE_NOTES`,
`detectors.json`, `case_stamp`; «трассировка», «триаж», «третий вердикт», «причина недоставки».
Не читать: зону `conductor` (лимит ремонта S5 и «Review gaps» ведёт его узел C1-5), код стадий S0–S4, `cost_capture.py`.

## Содержание

Снимок 13.10.2026; пути — от `ai-packages/qa-factory/`; суть строк — из `plans/BACKLOG.md`, находок — из дайджеста t-714. При расхождении авторитетны файлы пачек.

| id / файл | вид | суть (≤ 20 слов) | пути | статус | слово владельца | связи |
|---|---|---|---|---|---|---|
| **Сверка: похоже сделано (пачка 1, RD1-1)** | | | | | | |
| B-303 | строка | таблица приложения показывала `pass` на красном; по тексту починка сделана (`red_run_for`), хэша нет | `scripts/traceability.py`, `scripts/case_stamp.py` | пачка 1, RD1-1: похоже сделано (по тексту `plans/BACKLOG.md:249`) — проверить по коду | нет | — |
| B-308 / `findings/B-308-khvosty-pochinki-b-303-i-krasnykh-testov.md` | строка + находка-остаток | точное совпадение id в `traceability`: разные формы id дают «прогона нет»; остаток (а) лежит в находке | `scripts/traceability.py`, `scripts/check_delivery.py`, `scripts/case_stamp.py` | пачка 1, RD1-1: записи противоречат («закрыты» и «остаток») — проверить по коду | нет | — |
| B-266 | строка | третий вердикт `delivery_ready` и «Left with you» с регрессией; по P21 реализован, строка не закрыта | `scripts/check_delivery.py`, `scripts/ledger.py` | пачка 1, RD1-1: реализован по `PROJECT.md` P21 — проверить по коду | подтверждено 02.10 (P21) | — |
| **Сопоставление «результат прогона главнее» (пачка 1, RD1-2)** | | | | | | |
| B-310 | строка | одно правило «есть ли красный прогон у теста» (`case_stamp.red_run_for`); остались пункты (а)–(е) | `scripts/case_stamp.py`, `scripts/contract.py` | пачка 1, RD1-2 | нет | — |
| B-374 | строка | `decision_words` сопоставляет ключ кейса подстрокой: `TC-1` совпадает с `PC-1@TC-10` | `scripts/traceability.py` | пачка 1, RD1-2 | нет | — |
| B-357 | строка | точные соединения номера кейса перевести на `contract.case_matches` | `scripts/ledger.py`, `scripts/check_traceability.py`, `scripts/check_delivery.py` | пачка 1, RD1-2 | нет | — |
| **Баги, пайплайн, обнаружители (пачка 1, RD1-3)** | | | | | | |
| B-363 | строка | `delivery_summary.py` сводит черновики багов по своему ключу; свести к `bug_records.story_bugs` | `scripts/delivery_summary.py`, `scripts/bug_records.py` | пачка 1, RD1-3 | нет | — |
| B-347 | строка | неразобранный `pipeline.json` роняет `validate_artifacts`, отказ не печатается, запись проходит молча (FR-4) | `scripts/validate_artifacts.py` | пачка 1, RD1-3 | нет | — |
| B-430 | строка | остатки обнаружителей в `validate_artifacts`: прозовые «отказывает/замечает», второй загрузчик `detectors.json`, `ORACLE_NOTES` | `scripts/validate_artifacts.py`, `references/detectors.json` | пачка 1, RD1-3 | нет | — |
| **Причины недоставки и хвосты (пачка 1, RD1-4)** | | | | | | |
| B-353 | строка | `delivery-reason-owners.json` даёт `product` причине «blocked on the stand»; нужен владелец `environment` | `references/delivery-reason-owners.json` | пачка 1, RD1-4 | нет | — |
| B-304 | строка | хвосты N8: упавший результат без кейса при отданном кейсе, формулировки в `stage_guard.py` и `qa-doc-scribe.md` | `scripts/stage_guard.py`, `agents/qa-doc-scribe.md` | пачка 1, RD1-4 | нет | — |
| B-306 | строка | хвосты карточки отчёта гейта A: «своя команда» и `change` не живы, сырой stderr в `missing:`, блокировка кейса после `accept` | `scripts/stand_gaps.py`, `scripts/story_run.py` | пачка 1, RD1-4 | нет | `gates-and-words` (карточки гейтов) |
| **Одна таблица триажа (пачка 1, RD1-5)** | | | | | | |
| B-270 | строка | остатки «один матч триажа»: exact-шаг `triage_row_for`, NEAR через `test`, литерал `MANUAL_BLOCK_MAX`, «manual manual check» | `scripts/contract.py`, `scripts/story_run.py` | пачка 1, RD1-5 | нет | — |
| B-286 | строка | `s7-automator-to-analyst` — мёртвый контракт индекса; решить: убрать форму или объявить писателя и читателя | `handoffs/index.yaml` | пачка 1, RD1-5 | нет (решение Lead) | — |
| **Таблица отчёта: остатки (кандидаты пачки 2)** | | | | | | |
| `findings/B-123-trassirovka-svyazyvaet-trebovanie-so-strokoy.md` | находка | трассировка связывает требование со строкой плана и без кейса; `skip` с причиной не «not planned» | `scripts/traceability.py` | открыто | нет | — |
| `findings/B-348-k-b-319-artifact-root-forma-traceability-py-task.md` | находка | `traceability.py --task-root` читает другой корень багов, чем `--task`, при настроенном `artifact_root` | `scripts/traceability.py` | открыто | нет | `onboarding-hooks` (artifact_root) |
| `findings/B-328-pole-case-links-v-manifest-put-merge-entry-kopit.md` | находка | поле `case_links` копит ссылки по версиям; проверить эффект устаревшей ссылки | `scripts/manifest_put.py` | открыто | нет | — |
| `findings/B-329-drugie-chitateli-obligation-bindings-mogut-brat.md` | находка | читатели `obligation_bindings` берут первую привязку; сверить с `binding_receipt_ref` | — | открыто | нет | — |
| **Доставка, Left with you, причины (кандидаты пачки 2)** | | | | | | |
| `findings/20261009-ischerpannyy-limit-remonta-nedostatki-ne-v-otchete.md` | находка, id — | исчерпанный лимит ремонта S5: замечания критика не доезжают до отчёта; нужен перенос в леджер и «Review gaps» | `scripts/runtime_policy.py`, `scripts/repair_route.py`, `scripts/ledger.py`, `scripts/report_facts.py` | забрана кучкой `conductor`, узел C1-5; слово 09.10 дано | дано 09.10 | `conductor` C1-5 |
| `findings/B-122-prichiny-nedostavki-nasha-bukhgalteriya-i.md` | находка | бухгалтерия и ожидание человека не пишутся как `product`; «Factory defects» писать человеческим языком | `scripts/check_delivery.py` | открыто; часть чинит N8 по тексту — проверить по коду | нет | — |
| `findings/B-182-progon-cmp1-s8-bugs-found.md` | находка | cmp1 S8: «Bugs found — none» при решении гейта A «AC-7 = локальный баг»; дорога к багу только от красного теста | `bug-drafts/` | открыто | нет | — |
| `findings/B-152-kod-trebuet-3-izolirovannykh-pereprogonov-dlya.md` | находка | код требует ≥3 перепрогонов для FLAKY, что идёт против буквы D-0018 | `scripts/contract.py`, `scripts/validate_artifacts.py` | ждёт слова владельца | да | — |
| `findings/B-284-regressiya-teryaetsya-mezhdu-formoy-s3-i.md` | находка | регрессия теряется между формой S3 и планом: две записи против четырёх; нужен один носитель | `handoffs/s3-strategist-to-designer.yaml` | открыто | нет | — |
| `findings/B-285-vetki-retro-mode-skip-numbers-udalit-t-305.md` | находка | ветки `retro_mode` skip/numbers удалить: выбор ретро у человека снят, ветки живут в четырёх местах | `scripts/story_run.py`, `scripts/stage_done.py`, `scripts/report_facts.py` | открыто | нет | — |
| `findings/B-288-vyneseno-iz-n8-chernovik-t-358-10.md` | находка | вынесено из N8: никто не пишет `run-report.manual_human`; красный `ENV_ISSUE` без карточки гейта B | `scripts/stand_gaps.py`, `scripts/stage_guard.py` | открыто | нет | — |
| `findings/B-289-analogi-iz-chernovika-t-358-ne-rasshireny.md` | находка | аналоги из черновика: `pending_implementation` не блокирует, свободный суффикс `deferred_by_decision:<x>` | `scripts/ledger.py`, `scripts/check_delivery.py` | открыто | нет | — |
| **Триаж S7 (кандидаты пачки 2)** | | | | | | |
| `findings/B-274-s7-predtriazh-env-strok-kodom-analitik-tolko.md` | находка | S7: предтриаж env-строк кодом; красный тест никогда не предрешается кодом | `scripts/contract.py`, `experiments/measurers/code_friction.py` | сделано по тексту `B-277` (t-305 N1) — закрыт ли сам, проверить по коду | нет | — |
| `findings/B-277-s7-kodom-t-305-n1-t-347-t-350.md` | находка | S7 кодом: долги и аналоги (а–е): один `TRIAGE_VERDICTS`, связь `NOT_EXECUTED` и `source: code` | `scripts/check_witness.py`, `scripts/role_digest.py`, `scripts/contract.py` | пункт (в) решён в спеке N8; остальные открыты | нет | — |
| `findings/B-218-sosedi-b-194-samodeklaratsii-bez-proverki-na.md` | находка | шесть самодекларированных claim'ов на S5/S7 без верификатора | `handoffs/s7-automator-to-analyst.yaml`, `scripts/handoff_check.py` | открыто | нет | — |
| `findings/B-221-s5-precheck-schitaet-upominanie-partitsii-p-v.md` | находка | `s5_precheck` засчитывает упоминание партиции в докстринге; убрать зачёт докстрингов | `scripts/s5_precheck.py` | частично: партиция идёт через `partitions` манифеста — проверить по коду | нет | — |
| `findings/B-189-vykhod-s2-s3-reestr-iz-novogo-production-modulya.md` | находка | выход S2/S3: реестр партиций грамматики нового модуля, строка на партицию и маршрут | — | открыто | нет | — |
| **Передачи и роли (кандидаты пачки 2)** | | | | | | |
| `findings/B-183-handoff-init-no-contract-for-qa-bug-reporter-at.md` | находка | `handoff_init`: нет контракта для `qa-bug-reporter` на S8; добавить строку в индекс и файл контракта; повтор 29.10.2026 (прогон 12586 на 0.10.5) | `handoffs/index.yaml` | перенос: hotfix-12586/8, HF8-21 | нет (П1 0.10.7 — решение Lead) | HF8-16; HF8-20 |
| `findings/B-332-perezapushchennaya-remontnaya-i-ruchnaya.md` | находка | перезапущенная, ремонтная и ручная диспетчеризации не получают пустую форму передачи | `scripts/handoff_init.py`, `scripts/metrics_projection.py` | открыто | нет | — |
| `findings/B-154-rol-bez-bash-qa-test-strategist-qa-case-designer.md` | находка | роль без Bash не может отложить артефакт и вызвать `plan_row.py`; «начать заново» по слову человека не сделано | `scripts/artifact_supersede.py`, `scripts/plan_row.py` | перенос: speed-cost/1 (SC1-2) | нет | — |
| `findings/B-124-odna-komanda-sborki-otcheta-pisarya-vmesto.md` | находка | одна команда сборки отчёта писаря вместо четырёх вспомогательных файлов | — | открыто | нет | — |
| **Пропущенные баги (пачка 1, RD1-6)** | | | | | | |
| `findings/20261019-propushchennye-bagi-nositel-dlya-sbora.md` | находка | у «пропущенных багов» нет носителя, поэтому сбор `qa-collect` не может их упаковать | `scripts/validate_artifacts.py`, `scripts/ledger.py` | пачка 1, RD1-6 | нет | `collect` |
| `findings/20261021-otkazannyj-verdikt-ne-pravitsya-v-prinyatie.md` | находка | отказанный вердикт отчёта нельзя отредактировать в принятие: база снимается при первом отказе, изменённый вердикт или доказательство = новый прогон | `scripts/check_delivery.py` | RD1-7, ожидает | нет | обзор testing-factory (RELATED_WORK §2 п. 2) |
| `findings/20261024-otchet-pokazyvaet-pass-neispolnennomu-testu.md` | находка | отчёт 12586: pass неисполненному тесту, «9 proven» против «1 green», Q-4 отвечен и открыт | `scripts/check_delivery.py`, `scripts/report_facts.py` | RD1-8, ожидает | нет | t-1207; RD1-1 |
| **Находки ночного прогона 14857 (0.10.6), 30.10.2026** | | | | | | |
| `findings/20261030-otkazannyj-kriticheskij-test-pochinen-posle-s7-bez-povtornogo-revyu.md` | находка | тест, отказанный критиком, чинится после S7 без повторного ревью; отчёт: `pass` рядом с «rejected» и «замечания не записаны» | `scripts/check_delivery.py`, `scripts/report_facts.py` | RD1-9, ожидает | нет | RD1-8; `driver-controller`; TQ1-23; t-1605 #7 |
| `findings/20261030-otchyot-pechataet-slova-gejta-a-dvazhdy-i-14-odinakovyh-strok.md` | находка | слова гейта A напечатаны в отчёте дважды и 14 одинаковых строк «принято, ни к чему не привязано» | `scripts/report_facts.py` | RD1-10, ожидает | нет | t-1605 #23 |
| `findings/20261030-otchyot-ne-nazyvaet-ostatochnye-slabosti-testa.md` | находка | отчёт и тело MR не называют остаточные слабости доставляемого теста (MR 798 называл двумя пометками) | `scripts/report_facts.py`, шаблон отчёта | RD1-11, ожидает | нет | t-1606 урок 7; RD1-9; TQ1-23; t-1605 #7 |
| `findings/20261030-tekst-straza-posle-podshivki-baga-ne-nazyvaet-vybrannyj-bag.md` | находка | после подшивки бага страж говорит «решения нет» и не называет выбранный баг (S4c F-6 снят) | `scripts/check_delivery.py`, `skills/qa-story/phases/s8.md` | пачка 1, RD1-12 | нет | S4c F9; HF8-23 |
| `findings/20261030-req-id-re-bez-levoj-granicy-r-3-v-br-3.md` | находка | `contract.REQ_ID_RE` без левой границы: `R-3` находится в `BR-3` | `scripts/contract.py` | пачка 1, RD1-13 | нет | HF8-17; P23 |
| `findings/20261030-kept-local-by-word-dvojnik-local-only-decision.md` | находка | отчёт и исполнитель читают слова «баги остаются в репозитории» двумя функциями | `scripts/bug_records.py`, `scripts/external_writes.py` | пачка 1, RD1-14 | нет | S5b rest F-4 |
| `findings/20261031-assess-padaet-na-plan-rows-vmesto-togo-zhe-no.md` | находка | сломанный `test-plan.json` роняет `assess` исключением вместо того же `no`; докстринг «`assess` never fails» неверен | `scripts/check_delivery.py` | пачка 1, RD1-15 | нет | критик S6 0.10.7 F-7 |
| `findings/20261031-nachataya-dorabotka-ne-snimaet-stroku-left-with-you.md` | находка | доработка, начатая человеком по двери `rework_left`, не снимает строку «Left with you» | `scripts/report_facts.py` | пачка 1, RD1-16 | нет | S4c F-4; DC1-19 |
| `findings/20261031-ssylki-na-skrinshoty-v-mr-i-bagah-visyat-v-pustotu.md` | находка | ссылки на скриншоты в отчёте, MR и баг-файлах не открываются у читателя MR; варианты (а)/(б)/(в) | `scripts/report_facts.py`, `scripts/bug_records.py` | пачка 1, RD1-17 | решено, владелец 31.10.2026: скриншоты не в репозиторий и MR; отчёт пишет «предоставлены или нет», путь — в чат (t-420, 0.10.7) | OH3-33 F-8, F-9 |
| **Находки 31.10.2026 (прогон CART-1, MyBooks)** | | | | | | |
| `findings/20261031-ruchnye-proverki-proshli-a-trassirovka-pishet-not-run.md` | находка | кейсы, пройденные руками, в таблице трассировки «not run», вердикт «человек проверяет 0 кейсов» | `scripts/traceability.py`, `scripts/report_facts.py`, `scripts/check_delivery.py` | RD1-18, ожидает (П1) | нет | RD1-8; RD1-2 |
| `findings/20261031-prichina-triazha-i-plana-teryaetsya-pri-sborke-otcheta.md` | находка (склейка 6.3+6.4) | «no reason recorded» при записанной причине триажа и «Not planned»; `ASSERT_STRICTER` без исполнителя правки теста | `scripts/traceability.py`, `scripts/contract.py`, `scripts/check_delivery.py`, `scripts/story_run.py` | RD1-19, ожидает (П1) | да (п. 4, по рекомендации) | RD1-9; RD1-8; B-122; `conductor` |
| `findings/20261031-chisla-otcheta-ne-shodyatsya-svodka-ustarela.md` | находка | шесть чисел отчёта и сводки расходятся (17/18/9, 20/11/0); сводка собрана раньше отчёта | `scripts/delivery_summary.py`, `scripts/ledger.py`, `scripts/report_facts.py` | RD1-20, ожидает (П2) | нет | RD1-8; RD1-10 |
| `findings/20261031-probely-pokrytiya-i-instrumentov-pokazany-kak-produktovye.md` | находка | десять пробелов покрытия и инструмента показаны «на стороне продукта»; владелец должен быть `factory` | `references/delivery-reason-owners.json`, `scripts/check_delivery.py` | RD1-21, ожидает (П2) | нет | RD1-4; RD1-19 |
| `findings/20261031-chasti-otcheta-sshity-bez-proverki-granits.md` | находка | маркер приложения внутри блока `facts:regression`; «none in tests/» рядом с найденным набором | `scripts/render_case_appendix.py`, `scripts/report_facts.py` | RD1-22, ожидает (П3) | нет | RD1-10 |
| `findings/20261031-repeticiya-gejta-b-i-retro-ne-na-puti-ispolneniya.md` | находка | репетиция гейта B не запускалась, ретро не написано; пропуск виден только в тексте роли | `scripts/stage_guard.py`, `scripts/report_facts.py` | RD1-23, ожидает (П3) | нет | RD1-11 |
| `findings/20261101-bliznec-ruchnoj-stroki-manifesta-v-handed-plan-rows.md` | находка, id — | строка манифеста `handed_to_person` не входит в `handed_plan_rows`: обязательство остаётся причиной покрытия (t-593 F-1, близнец) | `scripts/check_delivery.py` | RD1-24, ожидает (П2) | нет | RD1-21 |
| `findings/20261101-prichina-ne-planirovano-vsya-stroka-v-paketnoj-i-staroj-vetkah.md` | находка, id — | `not_planned_basis`: ветки пакета вопросов и по слову «not planned» берут причиной всю строку с именем (t-593 F-3, близнецы) | `scripts/traceability.py` | RD1-25, ожидает (П3) | нет | RD1-19 |
| `findings/20261101-ostatki-ocheredi-kritika-s5-f-9.md` | находка, id — | очередь критика S5 F-9: колонка 0, третий разбор `waived:`, третий обход трассировки, местный читатель раздела | `scripts/story_run.py`, `scripts/delivery_summary.py`, `scripts/report_facts.py`, `scripts/traceability.py` | RD1-26, ожидает (П3) | нет | RD1-24, RD1-25 |
| **Обзор MR !12, 01.11.2026** | | | | | | |
| `findings/20261101-poteri-vetok-fabriki-zapisany-kak-dolgi-produkta-i-ne-schitayutsya.md` | находка, id — | `branch_lost`, `branches_not_recorded`, `source_unreconciled` — потери самой фабрики, записанные долгом продукта; ретро и `metric_signals` их не считают | `scripts/metric_signals.py`, `scripts/retro_numbers.py`, `references/delivery-verdict-kinds.json` | пачка 1, RD1-27 | нет | t-1645 F-1; RD1-21; RD1-4 |
| **Прогон LOCAL-1, 02.11.2026** | | | | | | |
| `findings/20261102-stroki-otcheta-razbity-po-shagam-i-prichina-ne-iz-ishoda.md` | находка | исключённый кейс разложен на 10 строк по шагам, «no test proves it» при красных, причина «Not proven» из ответа о требовании | `scripts/report_facts.py`, `scripts/traceability.py` | пачка 2, RD2-1 | нет | WG1-1, RD1-19, RN1-23; t-1672 П-18, П-20 |
| `findings/20261102-slova-cheloveka-remarks-ne-dohodyat-do-otcheta.md` | находка | слова человека в `pipeline.json remarks[]` не доходят до отчёта; у стори без MR теряются | `scripts/report_facts.py`, `scripts/gate_brief.py` | пачка 2, RD2-2 | нет | t-738 B-1, GW1-3 |
| `findings/20261102-hvosty-rd1-4-tekst-karty-output-tail-maskirovka-shag-pisarya.md` | находка | `output_tail` без читателя, `names_only` маскирует восемь форм не так, шаг 7 писаря «must» | `scripts/stand_gaps.py`, `references/conductor.md`, `agents/qa-doc-scribe.md` | пачка 2, RD2-3 | нет | t-758 m-2, m-3, m-5; RD1-4 |
| `findings/20261113-chitateli-razdelov-otcheta-dvojniki-i-perepisannye-zagolovki.md` | находка, id — | читатели разделов отчёта — двойники; заголовки других артефактов переписаны литералами (часть F6, меняющая поведение) | `scripts/validate_artifacts.py`, `scripts/report_facts.py`, `scripts/traceability.py`, `scripts/human_text.py`, `scripts/grammar.py` | пачка 2, RD2-4 | нет | HF2-0 п. 6; t-205 F6 |

## Входящие

`findings/` этой кучки; находку, не названную ни в одной пачке, называет `piles.py check --all` (е).
Находка 09.10 про исчерпанный лимит ремонта лежит здесь, а исполняет её `conductor/batch-1-p22-seams.md`, узел C1-5.

## Вопросы владельцу

- B-152: код требует не меньше трёх изолированных перепрогонов для FLAKY, что идёт против буквы D-0018 («других прогонов нет»): оставить три или поправить D-0018? Находка `findings/B-152-kod-trebuet-3-izolirovannykh-pereprogonov-dlya.md`.
- RD1-17 решён словом владельца 31.10.2026 (t-420, релиз 0.10.7); открытым остаётся только вопрос о баг-файлах: как читается `evidence/...` в баге и менять ли его (развилка в отчёте t-420). Находка `findings/20261031-ssylki-na-skrinshoty-v-mr-i-bagah-visyat-v-pustotu.md`.
