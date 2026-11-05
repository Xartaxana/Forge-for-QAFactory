# t-1672: разбор всего прогона LOCAL-1 «Add to Cart» (MyBooks, QA Factory 0.10.8), упор на S4 после гейта A и S5–S9

Критик (Opus), только чтение. Срез: 2026-11-02 11:22 по местному времени (10:22Z).

Важно: прогон дописывался, пока шёл разбор. S9 закрыт в 10:21:06Z, `test-report.md` пересобран в 11:20 по местному времени, `pipeline.json` записан в 11:21. Цитаты отчёта взяты из финальной версии 11:20. `work/delivery-summary.md` и `work/ledger.md` остались версиями 10:50–10:51: после гейта B их никто не пересобирал (см. П-17).

Сокращения:
- `A` = `mybooks-stand/test-automation-framework/qa-factory/artifacts/LOCAL-1`.
- `T` = транскрипт дирижёра `80f3172e-…jsonl`; `T:n` — номер строки.
- `E:n` — номер строки `A/state/events.jsonl`.
- Время везде UTC (Z). Местное время = UTC+1.

## 0. Итог

- Ни один из эталонных багов Б-1…Б-4 не найден.
- Единственный заведённый баг BUG-1 повторяет уже открытый в Jira баг XPANBFLFA-140, который сам входит в источники этой стори. Связь не указана.
- Из 19 красных экземпляров 11 — дефект кейсов, допущенный самой фабрикой. Цену проверяли в поле `GET /api/cart`, а этого поля нет. Автор S5 знал об этом уже в 00:50Z (за 8,5 ч до S7) и всё равно записал красные как `contradicts_requirement`.
- Вердикт доставки назван по дефекту кейса (TS-1 CASE_DEFECT), а не по багу продукта.
- Ответ человека на Q9, данный на гейте A, потерян: отчёт держит его открытым вопросом, а на гейте B его спросили ещё дважды.
- Восемь узлов 0.10.8 с пометкой «принято, слито» в этом прогоне снова сработали плохо: EP1-37, EP1-39, RD1-21, GW1-43, EP1-29 (половина), G2-14, OH3-39 (снято), RD1-19 (снято). Подробности в таблице.
- Полный прогон длился 13 ч 07 мин: команда 21:14Z, S9 done 10:21Z. Человек из них ждал около 7 ч 11 мин, ретро насчитало 2 ч 46 мин.
- Вопросов человеку 13, из них 8 можно было не задавать.
- Сводка: **БЛОК 2, БОЛЬШАЯ 13, МАЛАЯ 12** (27 проблем). Из них 9 уже покрыты находками RN1-2…RN1-10 или t-1666, 18 новые. Четыре из новых — регрессия или не починено.

## 1. Время по стадиям (pipeline.json, `started`/`finished`; минуты — по `stage_finished − stage_started`)

| Стадия | Старт | Финиш | Стена | Ожидание человека внутри стадии (T) | Примечание |
|---|---|---|---|---|---|
| S0 | 22:09:10 | 22:09:15 | 5 с | 43 мин до старта: вопрос в 21:25:37 (T:200), ответ в 22:08:10 (T:204) | проба входа упирается в 60 с |
| S1 | 22:12:20 | 22:43:09 | 30,8 мин | 7 мин (T:327→331) + 5 мин (T:374→378) | |
| S2 | 22:43:38 | 22:52:46 | 9,1 мин | 0 | |
| S3 | 22:53:06 | 23:47:11 | 53,9 мин | 0 | 3 окна стратега (RN1-2) |
| S4 | 23:17:51 | `finished: null` (эпоха: 23:41:07) | 23,3 мин + designer-3 00:27–00:31 | гейт A: 38 мин (T:932→936) | пересекается с S3 |
| гейт A | — | 00:34:37 (E:48) | — | — | |
| S5 | 00:36:05 | 04:51:40 | **255,4 мин** | ≈77 мин: 35 (T:1260→1264), 12 (T:1383→1389), 29 (T:1567→1577), 1 (T:1661→1665) | 28 диспатчей (14 автоматор + 14 критик кода), компакт дирижёра в 02:43 |
| S6 | 04:52:13 | 09:13:01 | **260,6 мин** | **230 мин**: AskUserQuestion в 05:20:48 (T:2875), ответ в 09:10:04 | машинное время ≈ 30 мин (runner-1 04:52–05:18) |
| S7 | 09:13:58 | 09:48:21 | 34,2 мин | 9 мин (T:3049→3050) | второй диспатч после слова на гейте B |
| S8 | 09:33:46 | 10:10:53 | 36,9 мин | 5 мин (T:3132→3142) + 14 мин (T:3238→3248) | начат раньше конца S7 |
| гейт B | — | 10:07:51 (E:263) | — | — | |
| S9 | 10:14:33 | 10:21:06 | 6,5 мин | 3 мин | `wall_seconds: null` у всех стадий |

Первый тест запущен в 01:28:59Z (`first_test_run_at`), через 3 ч 19 мин после S0.

Деньги: $35,36, это **нижняя граница** (`A/retro.md:29`). Дирижёр стоил $12,95 и прочитал 82 млн токенов. На S5 ушло $13,21, и эта цифра тоже неполная.

## 2. Вопросы человеку по стадиям

| Стадия | № | Вопрос (T) | Можно было не спрашивать? |
|---|---|---|---|
| S0 | 1 | проба входа не уложилась в 60 с (T:200) | **да**: константа 60 с, t-1666 П-5 |
| S1 | 2 | «согласны с таблицей источников?» (T:327) | **да**: открытого решения нет, 404-токены отброшены кодом |
| S1 | 3 | расхождение требования и кода, 0→1 (T:374) | нет (P20) |
| гейт A | 4 | пакет: Q1–Q9, репозиторий, пробелы, адрес UI (T:932) | гейт нужен. **Вопрос про адрес UI лишний** (RN1-3), пересказ пакета — RN1-4 |
| S5 | 5 | «та ли сборка на стенде» (T:1260) | частично: так задумано (EP1-28), но спрошено после проваленного окна, а не до S5, и дирижёр не прочитал `git -C ../MyBooks` |
| S5 | 6 | «оставить TS-тесты без мутационной пробы?» (T:1383) | **да** (RN1-8, RN1-9) |
| S5 | 7 | «принять Then без привязок вне окна?» (T:1567) | **да**: выходной контроль проверил весь план, а не окно. Это дефект кода (FR-3) |
| S5 | 8 | «принять все окна без квитанций ревью?» (T:1661) | **да**: квитанции рассчитаны только на pytest (FR-3) |
| S6 | 9 | «ручные TC_022/023 не входят на стенд» (T:2875) | **да** (RN1-10). Вдобавок вопрос держал весь конвейер 3 ч 50 мин |
| S7 | 10 | «11 красных — дефект наших кейсов, как поступаем?» (T:3049) | **да**: дефект фабрики выдан человеку как выбор (FR-3) |
| гейт B | 11 | пакет до гейта: баги, кейсы и **снова Q9 про сессию** (T:3132) | гейт нужен, **повтор Q9 лишний**. Склейку 3 черновиков в один баг человек сделал за S7 |
| гейт B | 12 | гейт B, **Q9 в третий раз** (T:3238) | гейт нужен, повтор Q9 лишний |
| S9 | 13 | вопрос ретро (T:3311) | нет, он необязательный |

**Итог: 13 вопросов. Лишних 8:** №1, 2, 6, 7, 8, 9, 10 и частично №5. Сюда же три лишних пункта внутри нужных пакетов: адрес UI в №4 и повтор Q9 в №11 и №12.

## 3. Таблица проблем

Колонки: тяжесть; улика; класс фабрики; находка. Отметка «новая» значит, что совпадения среди `release-next/findings/20261102-*.md` и t-1666 нет. «Регрессия/не починено» относится к узлам со статусом «принято, слито (релиз 0.10.8)» — статус проверен по `plans/piles/*/batch-*.md`.

| # | Проблема | Тяжесть | Улика | Класс фабрики | Находка |
|---|---|---|---|---|---|
| П-1 | **Вердикт доставки назван по дефекту фабрики.** `delivery_ready: no — TS-1 (TC_001) failed … CASE_DEFECT`. Настоящая продуктовая причина (BUG-1, R-8..R-10) первой не названа | **БЛОК** | `A/test-report.md:6,8` | Порядок причин вердикта не различает владельца: дефект кейса фабрики стоит выше бага продукта (FR-20, FR-19, AR-27) | новая. Смежна с RD1-21 |
| П-2 | **11 из 19 красных — дефект кейсов, известный с S5 и не исправленный.** Then цены прибит к `GET /api/cart`, а у `CartItem` поля цены нет. Автор окна 1 сообщил об этом в 00:50Z («no price field… handed over RED with `contradicts_requirement`»). Дальше 11 окон критика кода одобряли «red = product». Только S7 в 09:31Z переквалифицировал их в CASE_DEFECT. Правка оставлена человеку | **БЛОК** | T:1218 (handback automator-2). `A/work/test-code/critic-findings-w4b.md:9`, `-w7b.md:4`, `-w8b.md:7` («approved, red = product»). `A/work/triage.json` (11 CASE_DEFECT). `A/evidence/triage-price-channel.json`. Проверено по коду: `MyBooks/src/lib/openapi/spec.ts:983-989`, `cartService.ts:11-16`, `api/cart/route.ts:11` | (а) S4 не сверяет поле оракула с формой ответа API. (б) У S5 нет хода «дефект кейса → S4»: известный дефект кейса записывается гипотезой бага продукта. (в) Автор S5 переносит из кейса КАК, вопреки P17: цена на странице корзины и `/api/cart/total` зелёные. (г) Критик кода одобряет ложную гипотезу | новая (FB-5 ретро — локальная) |
| П-3 | **Ответ человека на Q9 потерян.** На гейте A: «Q9 b» и «Adding after session expiry asks for login, and the product is added after re-authentication». Отчёт: «Open questions — Q4 (TS-26): … extend the session, or ask for login?», «R-26 … Q9: before unknown, now unknown», BN-11 «you have not said so». На гейте B Q9 спрошен ещё два раза | БОЛЬШАЯ | `A/state/words/gate-a-answer-1.txt:8`, `gate-a-decision.txt:13`; `A/test-report.md:141` (open-questions), строка R-26 в not-proven, BN-11; T:3132, T:3238 | Слово человека на гейте A не доезжает до строки плана, к которой привязан вопрос. Id вопроса расходится (Q4/Q9) (FR-7, FR-8, AR-24) | новая. Смежна с t-1666 П-4 (Q4 сшит) и GW1-43 (повторный вопрос; **регрессия/не починено GW1-43** по классу «отвеченное спрашивается снова») |
| П-4 | **Рецензия гейта A приписана критику, который этих кейсов не видел.** TC_021/022/024 переписаны designer-3 в 00:27–00:31Z (версии `cv_aef96c…`, `cv_a4950f…`, `cv_d7043e…`, 01:30 по местному). `design_reviews` гейта A у TS-22/24/25/26 называют рецензентом `S4-qa-case-critic-2`, который закончил в 23:41Z. У TS-23 рецензента нет вовсе. Критик кейсов после designer-3 не запускался | БОЛЬШАЯ | `A/pipeline.json` `gates.A.design_reviews`; E:40 (critic-2 accept 23:41:07), E:45–47 (designer-3), E:48 (решение гейта A в 00:34:37); `A/state/case-versions/LOCAL-1_TC_021,022,024` (mtime) | Квитанция ревью переживает новую версию автора и не сбрасывается (FR-18, AR-28) | новая |
| П-5 | **BUG-1 — дубль открытого бага Jira XPANBFLFA-140** из источников этой стори («quantity 0 … added as 1 instead of being rejected», Open; в нём же «Not yet tested: -1, 1.5»). В BUG-1 нет ни ссылки, ни слова «140». Дедуп искал только в `bugs/` («did not exist») | БОЛЬШАЯ | `A/bugs/BUG-1.md:48`. `A/work/sources/SRC-be14dea130fb839bff9a/1412e185e5793bfd/ticket.json` (type Bug, status Open). grep `XPANBFLFA-140\|140` по BUG-1, черновику и handoff S7-2/S8 = 0. Положительный контроль той же формы `R-8` в BUG-1 = 3 | Дедуп бага не смотрит баги среди источников стори. Новый баг вместо дополнения к существующему (FR-16, FR-17) | новая |
| П-6 | **Один корень разбит на три черновика.** S7-1 сделал 3 черновика по одной строке `BookDetailPage.tsx:164`. Склеить их сказал человек. Цена — переделка S7-2 и S8-2 | МАЛАЯ | T:3142 («Все 3 бага это разные множества одного бага»); E:248, 255–262; `A/work/digests/S7-qa-failure-analyst-2.txt` | Аналитик дробит баг по классу входа, а не по месту дефекта; дедуп черновиков по `defect_location` отсутствует | новая |
| П-7 | **Ни один зелёный тест не засчитан: «Proven — 0», «0 of 26 proven».** Все 15 зелёных стоят под «Left with you». Причина — отказ от квитанций ревью и проб для TS, вынужденный инструментами (вопросы №6, №8) | БОЛЬШАЯ | `A/test-report.md:6`, «Proven — 0 green tests»; `A/state/words/s5-not-receipted.txt`, `s5-probe-gap-typescript.txt` | Инструменты квитанций и проб знают только pytest, а вынужденный отказ записан как слово человека («accepted by you») | RN1-8 (проба TS). Часть про квитанции — **регрессия/не починено EP1-37** (класс «Playwright TS не читается») |
| П-8 | **Фрагменты манифеста TS строились руками, селектор с одним `--grep`.** Автор писал `gen-w9.py`…`gen-w12.py` и десятки `frag-w*.json`. Прогон TC_012 исполнил 1 из 11 тестов («the launcher keeps only the last `--grep`»). `manifest_from_tests.py` падает на заголовках, собранных в цикле | БОЛЬШАЯ | `A/work/gen-w*.py`, `A/work/frag-w*.json`; T:2226 (handback automator-9); `A/retro.md:96` | Тот же класс, что у EP1-37: язык теста не читается кодом манифеста и селектора | **регрессия/не починено EP1-37** |
| П-9 | **Повторная отправка манифеста стёрла `then_bindings` прошлых окон** («the first `manifest_put.py` send removed the TC_007–009 `then_bindings`») | БОЛЬШАЯ | T:2226; `A/retro.md:96`; FB-3 | Слияние окна в `manifest_put` молча стирает поля прошлых окон (AR-14) | **регрессия/не починено EP1-39** (сосед: там `tests[]`, здесь `then_bindings`) |
| П-10 | **Id экземпляров манифеста и отчёта раннера расходятся.** Одни с префиксом `cart.spec.@regression`, другие без. Следствия: окно критика-2 закрылось как `incomplete`; 9 строк «INSTANCE_MANIFEST_JOIN_FAILED»; счёт «43 tests / 43 checks» — 34 настоящих экземпляра плюс 9 фантомов | БОЛЬШАЯ | E:71 checkpoint; `A/work/delivery-summary.md:6,128-136`; `A/work/automation-manifest.json` (34 строки `tests`); `A/retro.md:84` («43 tests») | Тождество экземпляра Playwright не нормализовано одним читателем (AR-13) | **регрессия/не починено EP1-37** (`report_test_id`) |
| П-11 | **Отчёт помечает зелёные «not counted» как продукт, а в блоке «product side» стоят дефекты фабрики.** Финальные `delivery-summary.md` и `ledger.md` в блоке «What blocks delivery on the product side» держат 13 CASE_DEFECT как «unresolved (contradicts_requirement) with no decision attached», TC_022/023 как «neither in automation-manifest» (пробел стенда, принятый человеком) и `coverage red: OB-n — none` | БОЛЬШАЯ | `A/work/delivery-summary.md:72-123` | Вердикт S7 (CASE_DEFECT) не переписывает `unresolved[]` S5; принятый пробел стенда не записан в строку; пробел покрытия без причины отнесён к продукту (FR-19, FR-20, AR-27) | **регрессия/не починено RD1-21** (класс «пробелы фабрики показаны как продуктовые»). Часть «вердикт S7 не доезжает» — сосед RD1-19 |
| П-12 | **Слово человека о пробеле стенда не дошло до строк TC_023 и TS-24/25.** TC_023 не диспатчился вообще, причина — «no record was written». TS-24/25 — «not_executed: no result recorded», хотя человек принял пробел для TC_022 и TC_023 | МАЛАЯ | `A/state/words/s6-manual-login-gap.txt`; `A/test-report.md:50`; `A/work/delivery-summary.md:19-20,102-103`; E:240 (runner-2 scope только TC_022) | Решение класса для нескольких кейсов исполняется по одному экземпляру (FR-8, AR-24) | смежно с GW1-43 и RN1-10. Новая сторона |
| П-13 | **Вопрос на одном ручном кейсе остановил весь конвейер на 3 ч 50 мин.** AskUserQuestion в 05:20:48Z, ответ в 09:10:04Z. S7 (разбор 19 красных) от TC_022/023 не зависел, но ждал | БОЛЬШАЯ | T:2875→2876; E:240, 243 | Вопрос на одном экземпляре блокирует независимую работу стадий; нет «спросить и идти дальше» | новая (P22). Смежна с RN1-10 (сам вход) |
| П-14 | **Ретро неверно меряет время ожидания и переделки.** «Human wait 2h 46m», «halts 0, waiting 0m 0s», «S6 4h20m machine time»; по транскрипту ожиданий ≈7 ч 11 мин, в S6 машины ≈30 мин. «28 repair rounds, $15.05» засчитывает новые окна S5 (новый scope) как починки; настоящих возвратов в S5 около 10. «qa-automator 9 dispatches» при 14 handoff. Одновременно «roles with no recorded usage: qa-automator» и строка $9,34 | БОЛЬШАЯ | `A/retro.md:8,25,56,84`; `A/work/retro-numbers.md:5,47,60`; E:57–92 (scope окон); 14 файлов `S5-qa-automator-N.yaml` | Ожидание в AskUserQuestion не считается ожиданием; «переделка» = порядковый номер диспатча роли, а не повтор scope; повторно использованные сессии агента (`adae5438…` у automator-2/3, `adabc4a7…` у 13/14) склеивают диспатчи (FR-25, FR-26, FR-41, P18) | новая |
| П-15 | **S5 длился 255 мин, 28 диспатчей на 21 кейс.** Возвраты по форме: obligation_hash (E:86), id экземпляров (E:71), строки привязок на одну строку мимо (`critic-findings-w7b.md` F-1). `returned_unaccepted` с ремонтом (E:76). Окно с 3 кейсами при капе 2 («Window 5 over the cap») | БОЛЬШАЯ | E:49–93; `A/test-report.md` блок review-gaps; `A/retro.md:5` (41 блок гейта) | Роль узнаёт форму из отказа гейта | t-1666 П-7 (SC2-27, повтор). Окно над капом — новая мелочь |
| П-16 | **Выходной контроль окна S5 проверил весь план** («branch accounting» по Then окон 2–8, которых ещё нет). Код не определил scope окна («диспетчер уже записал его как вернувшийся») и выдал дефект человеку на «да» | БОЛЬШАЯ | T:1567; `A/state/words/s5-branch-accounting.txt` | Scope окна теряется при ремонте `returned_unaccepted`; дефект фабрики подаётся как выбор (FR-3, FR-4) | новая |
| П-17 | **Отчёт гейта B устарел, сводка доставки не пересобрана.** `delivery-summary.md` (10:51): «qty-invalid-input-coerced: a draft, not chosen so far», «1 with a product bug, 21 not proven». Финальный `test-report.md` (11:20): «4 with a product bug, 19 not proven», «BUG-1 … in an unfiled draft». S9 сначала отказал: «report has no `gate-b` block» | МАЛАЯ | `A/work/delivery-summary.md:173`, mtime 10:51; `A/test-report.md:6`; T:3347 | Производный артефакт после гейта B не пересобирается вместе с отчётом (AR-22) | новая |
| П-18 | **«Branches left with you»: исключённый кейс Jira разложен на 10 строк по одной на шаг** (U-a929…–U-4e59…) с противоречивым текстом: «the role left it out, you have not said so … (person's scope decision)». BN-2 и BN-3: «no test … proves it», хотя красные тесты TC_007/008 есть и по ним заведён BUG-1 | МАЛАЯ | `A/test-report.md` блок left-branches; источник — `A/work/sources/SRC-532fac988c7abdfde19c/…` | Единица отчёта — строка источника, а не обязательство; «нет доказательства» не видит красный тест (FR-10) | t-1666 П-11 (приписка решения человеку). Дробление на шаги — новая сторона |
| П-19 | Пункт человека «быстрый просмотр не реализован — занести пробелом» стоит в «Skipped by the plan» с причиной «owner's answer leaves no … path», а не как пробел продукта по требованию | МАЛАЯ | `A/state/words/gate-a-answer-1.txt:3`; `A/test-report.md` skipped-by-plan R-23 | Нереализованная функция по требованию не идёт по FR-21 | новая (спорная) |
| П-20 | **Причины R-24/R-25 в «Not proven» не те.** «the owner settled the expected price» — это ответ на Q7, а не то, что остановило проверку (вход на стенд) | МАЛАЯ | `A/test-report.md` not-proven R-24, R-25 | Причина «не доказано» берётся из ответа о требовании, а не из исхода исполнения (FR-20) | смежно с RD1-19 |
| П-21 | **Роль автора и дирижёр правили конфиг проекта, следы остались.** `runtime_probes.web` вписал автор окна 1, хотя правило пакета — «a story never writes a probe by hand» (T:1090); дирижёр откатить не смог (T:1260). `selectors.verified: true` и `url_key` вписал дирижёр | МАЛАЯ | `git -C mybooks-stand/test-automation-framework diff qa-factory/config.json` (3 правки); T:1218, 1225, 3366 | Роль пишет онбординговый конфиг в обход хозяина; нет отката | новая |
| П-22 | **Каталог-дубль `qa-factory/qa-factory/`** создан в 10:18Z (S9: `factory-backlog.md`, `records/project-decisions.json`, `state/`) | МАЛАЯ | `ls mybooks-stand/test-automation-framework/qa-factory/qa-factory` (mtime 11:18 по местному) | Путь записи S9 считается от неверного корня (FR-37, AR-4) | новая |
| П-23 | Дирижёр до триажа назвал красные цены дефектом продукта («нет цены в строке корзины», T:2846) и потом отозвал (T:3132). Плюс одна ошибка разбора JSON у AskUserQuestion (T:3040) | МАЛАЯ | T:2846, 3040, 3132 | Дирижёр пересказывает гипотезу S5 как факт до S7 (FR-41) | новая |
| П-24 | `pipeline.json`: у всех стадий `wall_seconds: null`; у S4 `finished: null` и пустой digest; `later_work_status: running` у S3/S7/S8 после `done`; `closed_at` (10:10:42) раньше `finished` S8 (10:10:53) | МАЛАЯ | `A/pipeline.json` stages | Проекция pipeline не закрывает поля стадий | t-1666 П-10 (покрыто частично) |
| П-25 | Дирижёр переполнил контекст и сжался посреди S5 (02:43Z, по просьбе человека) — 82 млн токенов за прогон | МАЛАЯ | T:1698, 1713–1716; `A/retro.md:59` | Контекст дирижёра растёт с числом окон S5 | новая (класс speed-cost) |
| П-26 | **Отказ запроса нигде не проверен, кроме ручного TC_023, который не исполнялся.** В тестах нет `route/abort/fulfill` | БОЛЬШАЯ (по последствию) | grep ниже, §5 | — | RN1-6 (P2), t-1666 П-2 — покрыто |
| П-27 | Пробелы S0–S4: G2-14 «no code»; критик вычёркивает «фокус»; адрес UI; пересказ гейта A; круги стратега; вход ручной проверки | — | t-1666 П-1…П-11 | — | RN1-2…RN1-7, RN1-10 — покрыто, не дублирую |

Проверка П-3 «регрессия GW1-43»: узел обещал «решение класса не спрашивается снова на следующем окне и стадии». Здесь ответ гейта A на Q9 спрошен снова на гейте B. Класс тот же, сторона другая (ответ гейта, а не решение класса окна). Поэтому пишу «смежно, вероятно не починено», а не «доказанная регрессия».

## 4. Тесты против кейсов, баги против красных

- Кейсов 24.
  - Автоматизирован 21 (TC_001…TC_021): 34 экземпляра в `automation-manifest.json`. Из них TC_012 — 11 вариантов, TC_018 — 3, TC_008 — 2.
  - Ручных 2 (TC_022, TC_023): не исполнены.
  - TC_024 (quick view): пропущен планом.
- Итог прогона: 15 зелёных, 19 красных (`triage.json`).
  - 8 APP_BUG: TC_007, TC_008×2, TC_009, TC_012×4.
  - 11 CASE_DEFECT: TC_001, 003, 004, 013, 015, 016, 018×3, 019, 020.
- Баги против красных: 8 APP_BUG → 1 баг (BUG-1, после склейки по слову человека). 11 CASE_DEFECT → 0 багов, правка оставлена человеку (П-2). BUG-1 — дубль XPANBFLFA-140 (П-5).
- В отчёте 43 вместо 34: 9 фантомов из-за расхождения id (П-10).
- Слово человека о TC_021 (количество гостя, а не 1) исполнено: `critic-findings-w8b.md`, `toEqual([3])`.

## 5. Эталонные баги (experiments/mybooks/add-to-cart-cases.md; Б-1…Б-4 по разбору t-1666 §3)

| Баг | Найден? | Улика |
|---|---|---|
| Б-1: «12» в поле количества на странице корзины | **нет** | Правка в корзине исключена скоупом (t-1666 П-11). В тестах `CartPage` не трогается. Ввод с клавиатуры есть только на странице книги (`tests/e2e/cart/cart.spec.ts:95-97,268-276`) |
| Б-2: `GET /api/books/{id}` → 500 валит /cart | **нет** | grep `api/books` по `A/work/triage.json`, `A/work/bug-drafts/*.json`, `A/bugs/BUG-1.md`, `A/test-report.md`, `A/work/delivery-summary.md`, `A/work/ledger.md`, `A/work/exploratory-findings.jsonl`, `A/retro.md` — 0 файлов. Положительный контроль той же формы: `A/evidence/triage-price-channel.json` — найден. В тестах `route\(\|abort\|fulfill` = 0 (`tests/`, `core/`); контроль той же формы — `node_modules/playwright-core/types/types.d.ts`, найден |
| Б-3: очистка поля → PUT null → 400 | **нет** | то же исключение скоупа. `PUT ` в BUG-1 совпал только с «input» — ложное совпадение |
| Б-4: merge → 500, гостевая корзина пропадает молча | **нет** | `cart/merge`, `LoginPage`, `\b500\b` по тому же набору артефактов — 0. TC_021 проверяет только правила слияния, а не его отказ (`cart.spec.ts:478`). Контроль: `BookDetailPage` тем же grep находится в triage, черновике и BUG-1 |

Найден только «0/-1/1.5/abc → 1» (`BookDetailPage.tsx:164`). Это уже открытый XPANBFLFA-140, и в эталон он не входит.

Попутная странность, не разобранная фабрикой: в BUG-1 записано «-1 → field shows 11». Это признак посимвольного переписывания поля — того же класса, что Б-1. Аналитик это не исследовал. Смежно с RN1-10, слово владельца «записывать все сомнительные места».

## 6. Отрицательные утверждения — форма и контроль

- «В тестах нет инъекции отказа запроса»: `grep -rlE "route\(|abort|fulfill"` по `tests/`, `core/` — 0. Контроль: тот же шаблон в `node_modules/playwright-core/types/types.d.ts` — найден.
- «BUG-1 не ссылается на XPANBFLFA-140»: `grep -c "XPANBFLFA-140\|140"` по BUG-1, черновику и handoff S7-2/S8 — 0. Контроль: `grep -c "R-8"` по BUG-1 — 3.
- «Б-2/Б-4 не найдены»: `grep -ilE` (без учёта регистра) — см. §5, контроль `BookDetailPage` и `api/books` по evidence.
- «Критик кейсов после designer-3 не запускался»: в `A/state/events.jsonl` после E:47 нет ни одного `dispatch` с `role: qa-case-critic`. Контроль: E:38 — такой диспатч, найден тем же разбором.
- «Q9 не найден как отвеченный в отчёте»: строка open-questions `A/test-report.md` прочитана напрямую (Read), не grep.

## 7. Чего не делала

- Тесты, драйвер и стенд не запускались.
- Git MyBooks не трогался.
- Стоимость по стадиям взята из `retro-numbers.md` и не пересчитана.

## След

Прочитано:
- `A/pipeline.json` — целиком: stages, gates A/B, warnings, remarks, overrides.
- `A/state/events.jsonl` — все 272 события, не-manifest выписаны.
- `A/state/words/*` — все 11 файлов.
- `A/state/passed-by-person.jsonl`, `stand-confirmations.jsonl`, `case-versions` (TC_021/022/024).
- Сводки и отчёты: `A/work/delivery-summary.md` (целиком), `A/test-report.md` (финал 11:20, ключевые блоки), `A/retro.md`, `A/work/retro-numbers.md`.
- Разбор и баги: `A/work/triage.json`, `A/bugs/BUG-1.md`, `A/work/bug-drafts/*`, `A/work/automation-manifest.json` (сводка), `A/work/exploratory-findings.jsonl`, `A/evidence/triage-price-channel.json`.
- Критик кода: `A/work/test-code/critic-findings-w4b/w7/w7b/w7c/w8/w8b.md`.
- Транскрипт дирижёра: все реплики человека и вопросы (T:200–3366), handback-и T:1218, 1225, 2226, хвост T:3330–3366.
- MyBooks a25b080: `openapi/spec.ts:975-995`, `cartService.ts:1-30`, `CartPage.tsx:25-45`, `api/cart/route.ts:11`. Источник XPANBFLFA-140.
- Находки RN1-2…RN1-10 (заголовки и начала), t-1666 целиком, статусы узлов EP1-37/39, RD1-19/21, GW1-43, EP1-28 по `plans/piles/*/batch-*.md`.

Сверх манифеста понадобилось:
- код MyBooks (эмпирика поля цены);
- `git -C …test-automation-framework diff/status`;
- находки 31.10 других кучек и их узлы, чтобы проставить «регрессия/не починено».

```json
{
  "verdict": "blocker",
  "blockers": [
    "П-1: delivery verdict names a factory case defect (TS-1 CASE_DEFECT) instead of the product bug as its reason (A/test-report.md:6,8)",
    "П-2: 11 of 19 reds are a case-oracle defect (price pinned to GET /api/cart, which has no price field) known to S5 at 00:50Z, approved as product reds by 11 code-critic windows, never routed back to S4, left to the person (T:1218; critic-findings-w4b/w7b/w8b; triage.json)"
  ],
  "class_completeness": "Run review, not a diff gate. Each problem names its factory class. Recurrences of 0.10.8 nodes marked: EP1-37 (TS manifest/selector/instance id), EP1-39 (manifest_put wipes then_bindings), RD1-21 (factory gaps on the product side), GW1-43 (answered question re-asked, adjacent side). Already filed and not re-filed: RN1-2..RN1-10, t-1666 P-1..P-11. New classes for the coordinator: oracle field vs API shape at S4 plus a case-defect route from S5 to S4; verdict reason ordering by owner; gate-A word to plan row (Q9); stale review receipt across an author revision; bug dedup against source tickets of type Bug; retro wait and rework accounting; a question on one case blocking independent stages; window scope lost on returned_unaccepted repair.",
  "trail": {
    "read": [
      "mybooks-stand/test-automation-framework/qa-factory/artifacts/LOCAL-1/pipeline.json",
      "mybooks-stand/test-automation-framework/qa-factory/artifacts/LOCAL-1/state/events.jsonl",
      "mybooks-stand/test-automation-framework/qa-factory/artifacts/LOCAL-1/state/words/",
      "mybooks-stand/test-automation-framework/qa-factory/artifacts/LOCAL-1/test-report.md",
      "mybooks-stand/test-automation-framework/qa-factory/artifacts/LOCAL-1/retro.md",
      "mybooks-stand/test-automation-framework/qa-factory/artifacts/LOCAL-1/work/delivery-summary.md",
      "mybooks-stand/test-automation-framework/qa-factory/artifacts/LOCAL-1/work/triage.json",
      "mybooks-stand/test-automation-framework/qa-factory/artifacts/LOCAL-1/work/retro-numbers.md",
      "mybooks-stand/test-automation-framework/qa-factory/artifacts/LOCAL-1/work/automation-manifest.json",
      "mybooks-stand/test-automation-framework/qa-factory/artifacts/LOCAL-1/bugs/BUG-1.md",
      "mybooks-stand/test-automation-framework/qa-factory/artifacts/LOCAL-1/work/test-code/critic-findings-w*.md",
      "conductor transcript 80f3172e-4ef8-4f1c-8548-fbe5a3b67add.jsonl (human turns, questions, handbacks)",
      "MyBooks src/lib/openapi/spec.ts, src/lib/services/cartService.ts, src/components/pages/CartPage.tsx, src/app/api/cart/route.ts",
      "docs/tasks/specs/reviews/t-1666-local-1-run-review.md",
      "plans/piles/release-next/findings/20261102-*.md"
    ],
    "reruns": [
      {"command": "grep -rlE route-abort-fulfill over tests/ and core/, control playwright-core types.d.ts", "result": "0 in tests and core; control found"},
      {"command": "grep -c XPANBFLFA-140 over BUG-1 and drafts, control R-8", "result": "0; control 3"},
      {"command": "event timeline from events.jsonl (non-manifest)", "result": "272 events; S5 has 28 dispatches; S6 runner-2 spans 05:18-09:12Z"}
    ]
  }
}
```
