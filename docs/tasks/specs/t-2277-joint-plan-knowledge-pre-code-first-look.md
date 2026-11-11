# t-2277 — общий план внедрения: знания о проекте (t-2142) + прогон без кода (t-2181) + первый взгляд (находка 20261110) — ЧЕРНОВИК дизайнера, ревизия 4

Дизайнер (Opus), 10–11.11.2026, по брифу Lead t-2277. Ревизия 2 — фикс-раунд по вердикту `docs/tasks/specs/reviews/t-2277-joint-plan-critic.md`
и дополнениям Lead L1, L2; ревизия 3 — дополнение L3 (слово владельца 11.11.2026); **ревизия 4 (t-2288) — второй фикс-раунд по повторному
вердикту `docs/tasks/specs/reviews/t-2288-joint-plan-rereview.md` (N1–N7, m-new-1…10) с направлениями Lead; бывший §10 (ревизия 3 и решение
J-14) влит в тело: каждый узел исполним по своей записи §3.** Ответ по каждой находке — §9. Решения §6.1 авторитетны и не переоткрываются;
развилки — §6.2. Пути пакета — от `ai-packages/qa-factory/` в дереве `D:/ws2/wt-fbfix`; `docs/`, `plans/`, `PROCESS/` — от корня дерева.
Существующие спеки и файлы кучек НЕ правятся этим документом: поправки к t-2142 и t-2181 — списком в §5. Код не пишется. Функции — по имени.

Слово владельца 10.11.2026 (замысел): три плана частично пересекаются; собрать их в один план внедрения, не потеряв ни одного
пункта, переработать так, чтобы они вместе давали все три цели; расписать порядок и параллельные потоки, которые не мешают друг другу.

---

## §1 Цели трёх планов и инварианты AR-n

**План 1 — знания о проекте (кучка `project-knowledge`, пачка 1, спека t-2142, фаза 0).** Одна схема для всего, что фабрика узнаёт
о проекте: реестр ответов `records/project-knowledge.json` (один писатель `project_knowledge.record`, один чистый читатель `state()`,
отзыв, провенанс). Фаза 0 доказывает её на одном факте: роли продукта и учётки по ролям на стенде — стратег получает перечень ролей,
гейт A спрашивает учётку только для роли, нужной кейсам стори, и только раз; ответ переживает закрытие стори; «не роль продукта» не
переспрашивается ни на гейте A, ни на гейте B; учётка по умолчанию — только по нужде. Решение L3: знание применяется перед ДЕЙСТВИЕМ,
доходит и до критиков, его использование считается (FL-8).

**План 2 — прогон без кода и с одной стороной (кучка `pre-code`, пачка 1, спека t-2181).** Одна модель на три случая (кода нет;
одна сторона на моке; «как раньше»): стороны с реальностью `real | absent | substituted` и признаком `deliverable`, один читатель
`contract.story_sides`; реестр допущений `provisional[]` в манифесте; отметка «какие стороны встретил прогон» на каждом блоке
исполнения; «зелёный на подмене» — не проход; одно новое состояние «стори ждёт кода» с дорогой прихода кода; снимок старой версии как
оракул «прецедент». Постоянные факты о сторонах — строки реестра плана 1 (слово владельца F-1).

**План 3 — первый взгляд (кучка `pre-code`, пачка 2, находка `plans/piles/pre-code/findings/20261110-pervyj-vzglyad-mezhdu-s2-i-s3.md`).**
Между S2 и S3 свежий агент коротко и широко проходит изменённую фичу через рекордер (t-1957) — экранами и вызовами API одним ходоком
(L1): по каждому требованию реестра — подтверждается / противоречит / отсутствует / недостижимо, с уликой; плюс карта пути (адреса, шаги,
локаторы, API-маршруты, данные, роли, требования к стенду) для стратега, автора кейсов, автоматора, S6 и двух критиков — и замер, пользуются
ли ею (L2). Достижимо меньше 30 % требований — закрытый вопрос человеку: «остановить» (парковка и дорога прихода кода плана 2, при
перезапуске смотрим изменения КОДА) или «продолжаем» (тесты на ожидаемое, красные до починки; моков на настоящей стороне нет; локатор
отсутствующего элемента — строка учёта `placeholder_locator`, тест только красный).

**AR-n, которых касается целое** (каждый узел §3 называет свои; проверка изменения — в DoD узла):

| AR | чем держится в общем плане | проверка изменения (в DoD узлов) |
|---|---|---|
| AR-1 | слова реальностей, видов допущений, статусов первого взгляда, причин недостижимости, причин пустой записи (`null_reasons`), слово шага `http` ходока и виды его `surprise:` — строки данных (`side-realities.json`, `provisional-kinds.json`, `first-look-statuses.json`, `manual-capture-steps.json` `steps.http`, `surprise.http_kinds`) | grep литералов в `scripts/` с положительным контролем (PC-1a, FL-1 A/B, FL-2) |
| AR-2 | имена сторон и ролей открыты; какой статус у требования и почему недостижимо — суждение роли | фикстура со стороной `kiosk` и ролью `аудитор` (PC-1a, PK0-4, FL-2) |
| AR-3 | факты проекта — конфиг или реестр ответов; порог первого взгляда — ключ конфига с умолчанием 30 | PK0-6 (текст AR-3), FL-2 (`config-keys.json`) |
| AR-4 | ходок выбирает стенд по ИМЕНИ и ходит (экраном и HTTP) только хосты названного стенда | FL-1 A `env_by_exact_name`, `env_hosts_are_the_named_stand_only`; FL-1 B `http_step_host_outside_stand_refused` |
| AR-6 | старую версию и изменённую фичу проходит агент через рекордер; улики пишет код; цитата привязана к проходу, который её снял (J-C2) | FL-1, FL-2, PC-9a: запись без ссылки на улику ЭТОГО прохода отказывается |
| AR-9 | каждый новый отказ называет ожидание и дверь | реестр отказов в коммите узла |
| AR-10 | требования проверок (поля сторон, допущения, `tests[].provisional`, статусы, `assumed_from: first_look:`) доходят до роли в брифе и хартии до работы | PK0-2, PC-8, FL-3, FL-4, FL-7 |
| AR-11 | ни одной новой роли и ни одного нового инструмента: HTTP-шаг — слово того же ходока (`walk_session.py step`), не второй инструмент; первый взгляд ходит `qa-runner` уже имеющимися командами + одна команда записи | `role_load.py --all` до/после (PK0-2, PK0-3, PC-8, FL-3, FL-4, FL-7) |
| AR-12 | цена первого взгляда и польза его записи и знаний проекта меряются одной мерой: `stage_compare.py` с проходом и без; `report_facts.knowledge_use` (FL-8) | FL-L3, PC-10, FL-8 |
| AR-13 | один читатель на факт: `project_knowledge.state/subjects` (факты в брифах — только через `state`), `contract.story_sides/parks_after_s5/awaiting/manifest_provisional`, `acceptance.pending_instances`, `first_look.read/share/due/continued/current_keys`, `walk_session.capture_cited`, `report_facts.knowledge_use`; голова источника в записи — `handoff_check.implementation_entries` + `grounding_table.commit_value` через `first_look.current_keys` (контроллер её не считает, N2); хост URL — `manual_capture.host_key` | grep чтений мимо читателей с положительным контролем |
| AR-14 | один писатель на артефакт: реестр — `record`; `pipeline.sides` — `stage_done.py --set`; `provisional[]` и `tests[].provisional` — `manifest_put.py`; `work/first-look.yaml` — `first_look.py put`; `state/first-look-attempt.json` — `first_look.py begin/end`; `work/reference-snapshot.yaml` — `reference_snapshot.py put`; `state/sign-in-probe.json` остаётся писателем гейта A | `stages.json` / `artifact-writers.json` в том же коммите |
| AR-15 | один ходок (`walk_session.py`) для экранов и HTTP; ОДИН исполнитель одного HTTP-запроса `manual_capture.http_call` — его зовут `run_http` и HTTP-шаг ходока (N1); одна проверка цитаты улики для всех трёх проходов (S6, старая версия, первый взгляд); одни `redact`/`redact_headers`/`cut_body`/`body_text`/`CUT_WORDS`/`secret_pattern_hit` (второго правила нет); одна парковка и одна дорога прихода для двух причин; один исполнитель «продолжаем» (`first_look_continue`) для двух вопросов; один механизм «дошло и использовано» (`knowledge_use`) для знаний и записи первого взгляда | §2 строки (b), (c), (e); FL-1 B `run_http_unchanged` |
| AR-16 | все новые вопросы — закрытые, ключи `question-prices.json` (`first_look.dead`, `first_look.same_code`) | `test_human_reading.py` |
| AR-17 | свободные слова человека — дирижёру; новых входов дирижёра нет | тексты фаз (PK0-6, FL-5) |
| AR-19 | близнецы меняются вместе: `s0.no_change`/`s1.no_diff` (PC-2); гейт A/S6 вход (PK0-5); карточка роли / карточка кейса / карточка `_probe_actor` (PK0-4); драйвер/скилл-путь первого взгляда (FL-5); шаг экрана / HTTP-шаг ходока (одна попытка, одна цитата, один писатель `surprise:`) | ось 5 карты названа в коммите |
| AR-20 | храповики только вниз; одобренные подъёмы — ТОЛЬКО строки таблицы §4.7 (census, `driver-layers.json`), названные в вердикте узла; подъём сверх таблицы — стоп; `role-load.json` — J-15 | `test_judgment_census.py` (CI), `test_driver_layers.py` (CI) |
| AR-21 | первый взгляд — один YAML, входом S3–S7 и брифов двух критиков по `stages.json`; снимок старой версии — выход S1 во вход S2; штамп сторон — от блока к строке отчёта | `index.yaml`/`stages.json` строки |
| AR-22 | у каждого поля производитель и читатель (§4 t-2181 + строки первого взгляда §2; `tests[].provisional` — §5; каждое поле записи первого взгляда — читатель из FL-4/FL-6 или счётчик FL-8; `pipeline.first_look_continue.source_head/register_hash` — производитель `first_look.current_keys`, читатель `first_look.continued`) | `test_field_producers.py` |
| AR-23 | пустые исходы объявлены: `provisional: []`, `tests[].provisional` отсутствует = `[]`, запись первого взгляда `null: <причина>` + `rows: []` + строка-пробел, пустой перечень ролей | `null-outcomes.json`, `test_null_outcomes.py` |
| AR-24 | слова человека целиком доходят до исполнителя (реестр, `stop waiting`, ответы на оба вопроса первого взгляда — словами в `first_look_continue --words-file`) | PK0-1 CLI, PC-7, FL-5, FL-6 |
| AR-25 | у каждого состояния выход: строки реестра — `revoke`; ожидание кода (обе причины) — `arrive` / `stop_waiting`; для `first_look_stop` ещё `first_look_continue`. Доработка S0–(held_from−1) словами — работа ВНУТРИ удержания, не выход: по её концу стори снова держится | `test_state_exits.py` |
| AR-26 | единица — требование реестра: статус первого взгляда ставится на R-n; прецедент — только требованию `parity: yes` | FL-2, PC-9a |
| AR-27 | находка под своим владельцем: `on_substitute` — environment, `awaiting_implementation` — product, `placeholder_open` — по J-6; наблюдения `contradicts`/`missing` — входом S7 аналитику (FL-4); «запись не прочитана» и «известный факт не дошёл до решения» — строки находки в ретро (FL-8), не отказ | `delivery-verdict-kinds.json`, `test_first_look_briefs.py::s7_lines_list_observations`, `test_report_facts.py::unread_record_is_finding_line`, `::known_fact_not_reaching_decision_is_finding_line` |
| AR-28 | неизвестное не становится проходом: нечитаемый реестр → спросить / `sides_unknown`; зелёный на подмене или у теста с открытым помеченным локатором — не проход; нечитаемая запись первого взгляда — строка-пробел; голова источника не установлена (записанная или живая) → вопрос, никогда «сдвинулась» (N3); счётчик без носителя — `unmeasured: <почему>`, не ноль | отрицательные тесты PK0-1, PC-5, FL-2, FL-6, FL-7, FL-8 |
| AR-29 | код несёт данные и считает; «какая роль нужна», «о какой стороне Then», «жива ли фича», «баг ли красное», «какой тест опирается на заглушку вне `dependents`», «оправдан ли путь кейса, отличный от пройденного», «зря ли переоткрыт селектор» — суждения ролей и критиков; код никогда не отказывает роли за неиспользованную подсказку или знание; маркеры `[knowledge:…]`/`[first-look:…]` — данные для счёта, не текст для роли; «остановить ли», «продолжить ли как есть» — замысел человека | строка `judgment:` каждого коммита; строки census (§4.7) |

**Каждая проверка, которую добавляет или меняет общий план сверх двух спек (правило дизайнера 1):**

| id | проверка | где | владелец | класс census | блокирует? |
|---|---|---|---|---|---|
| J-C1 | `--env <имя>` у `walk_session.py open` называет стенд `environments[]` ТОЧНО (регистр учитывается); хосты прохода — экранные переходы И HTTP-шаги — только хосты этой строки; URL HTTP-шага проверяется до любого шага вызова | `walk_session.request_problems` (существующий unit, xref, класс не меняется), `Walk._start`; второй страж — `manual_capture.http_call` по переданным хостам | data | xref | отказ с дверью (список имён / хостов) |
| J-C2 | цитата улики лежит в попытке, которую запись ЭТОГО прохода (`state/walks/<walk>.json`) называет для этого item (экранный или HTTP-захват), место `survey`, стенд — ожидаемый; `quote`, если дан, найден в тексте захвата попытки, как он сохранён | новая чистая `walk_session.capture_cited` (не unit) | data | xref | — (возвращает причину) |
| J-C3 | запись первого взгляда: статус, `blocked_by`, `null` — слова файла данных; без `null` — ровно одна строка на каждое R-n реестра, ни одной на R-n вне реестра, каждая строка, кроме `blocked_by: nature`, цитирует улику прохода `walk` из `state/first-look-attempt.json` (J-C2); с `null` — `rows: []` и непустой `gaps` | `first_look.put_problems` (новый unit) | data | shape + xref (в census — xref, высший; заметка называет оба) | отказ записи с дверью |
| J-C4 | доля достижимых < порога → вопрос человеку; код только считает | `first_look.share` (счёт, не unit) | data → intent | — | нет |
| J-C5 | строка `placeholder_locator` на НАСТОЯЩЕЙ стороне — строка УЧЁТА красного теста (решение 2а), законна только с `assumed_from: first_look:<R-n>`, чья строка свежей записи первого взгляда `missing` ИЛИ `unreachable`, в обоих случаях `blocked_by: product`; `access`/`nature` — никогда. `side_substitute`, `assumed_contract`, `reference_value` на настоящей стороне — отказ; вид без поля `on_real` читается `never` | `s5_precheck.check_sides` (C3 t-2181, расширение) | data | xref | repair |
| J-C6 | C6(a) t-2181 не применяется к строке J-C5, пока она `open`; C6(b): отсутствие штампа — `real`, только когда `contract.story_sides` возвращает все стороны `real` и `sides_unknown` не стоит | `s5_precheck.check_sides` | data | xref | repair |
| J-C7 | (1) каждый Then из `dependents` открытой строки J-C5 читается `not_verified:placeholder_open`, каким бы тестом ни был покрыт; (2) зелёный теста, чей `tests[].provisional` называет открытую строку `placeholder_locator`, не доказывает ни одного Then — ни один, ни вместе с другими; Then вне `dependents` доказывается только привязками к тестам без открытой строки, иначе `placeholder_open`. ИНВАРИАНТ ПОЗИЦИИ (m-new-1): ветвь стоит ПОСЛЕ `sides_unknown`/`on_substitute` (t-2181) и ПОСЛЕ `failed:*` (красный остаётся красным), ПЕРЕД `not_verified_flaky`, `partial`, `error`, неизвестным словом прогона, `expectation_unconfirmed`, `skipped:*`, `HANDED_STATE` (обеими ветвями), `deferred_by_decision`, `BLOCKED_STATE`-«за красным» и `passed_green`: ни пропуск, ни передача, ни нестабильность не читаются вместо `placeholder_open` | `ledger.plan_row_state` | data | xref (выведение) | нет |
| J-C8 | доработка и диспатч стадий ≥ `held_from` отказываются, пока стори держится за кодом (C12/C13 t-2181 с `held_from` вместо «S6») | `controller.build_rework_request`, `stage_guard.rule_awaiting_code` | data | presence / safety (как в t-2181) | отказ с дверями t-2181 |
| J-C9 | для теста T, связанного с открытой строкой J-C5 (T.provisional называет её, или T привязан в `then_bindings` к Then её `dependents`): (a) T.provisional называет строку; каждое P-n в `tests[].provisional` — строка `provisional[]`; (b) ни один экземпляр T не в `unresolved[]` `blocked_by_env`; (c) T не передан человеку (`contract.handed_tests`); (d) у T есть строка прогона этого S5, исход не `skipped`/`xfail`/`deselected`. НАПРАВЛЕНИЕ ОШИБКИ (a) (m-new-2): объявление требуется и от теста, который заглушку на деле не трогает; тогда J-C7 (2) лишает его доказательства и других Then — допустимая ошибка в безопасную сторону (лишний `placeholder_open`); объявление — данные для учёта, НЕ утверждение, что тест опирается на заглушку, и критик кода не читает его как такое утверждение | `s5_precheck.check_sides` (тот же unit) | data | xref | repair (ошибка — к отказу) |
| J-C10 | операция `first_look_continue` снимает удержание только с причиной `first_look_stop`; на `s5_absent_side` и `stopped` — отказ с дверью; без `--words-file` с непустыми словами, без `--source-head` или без `--register-hash` (64 hex) — отказ с дверью «драйвер передаёт значения `first_look.py show --json` (`current_keys`)» | `controller` `APPLY_OPERATIONS` (PC-6) | data | presence (строка `apply(first_look_continue)`, §4.7) | отказ с дверью |
| J-C11 | строка шага `http`: метод из `http_methods`, второе слово — путь `/…` или URL `http(s)://…` без пробелов и не-ASCII, необязательная пара `--body-file <файл>`; слово законно только в ходоке (`parse_steps(…, http_ok=True)`) | `manual_capture.parse_steps` (существующий unit, shape) через новую `_http_word_problem` (имя вне `UNIT_NAME_RE`, возвращает текст) | data | shape (класс не меняется) | отказ вызова до любого шага, с дверью |

Счётчики использования (L2 (b), L3, FL-8) — не проверки: ничего не блокируют, census-строк не дают.

Суждения ролей, на которые опирается первый взгляд (код их не судит): статус требования и `blocked_by` — `qa-runner` первого взгляда;
по смыслу — стратег S3 и человек на вопросе (J-3); «какой локатор у отсутствующего элемента» и «какие тесты опираются на заглушку» —
автоматор (объявляет `tests[].provisional`), судит критик кода; «путь кейса отличается от пройденного без причины» — находка критика
кейсов; «селектор или маршрут переоткрыт или угадан, хотя первый взгляд его видел» — находка критика кода (класс «новый тест там, где
можно было дополнить старый»); «требование, противоположное знанию проекта» — находка критиков кейсов и кода, не требование к автору
(L3); «красное — баг ли» и «наблюдение без исполненной проверки — кандидат ли в баг» — аналитик S7. Замысел человека: «остановить /
продолжаем», «ждать / вот источник / продолжить как есть».

**Направление ошибки переиспользуемых функций в более ответственной роли:**

- `walk_session` выбор стенда (сегодня первая строка `environments[]`, хосты всех строк) → выбор стенда для старой версии и первого
  взгляда. Допустимо: отказ на имя, которого нет точно. Запрещено: пройти не тот стенд или хост вне названной строки (экраном или
  HTTP). Неудобные входы (FL-1 A): `Dev` при `dev`; имя отсутствует; `--env` не дан (как сегодня); переход/HTTP на хост образца при
  `--env stage`; образец для первого взгляда (FL-5 берёт `--env` только из `pipeline.environment`).
- ядро `run_http` → `manual_capture.http_call`, исполнитель HTTP-шага ходока, чья запись становится уликой требования (N1). Допустимо:
  отказ шага (хост, секрет в запросе, нет входа, нечитаемый `--body-file`) с дверью; отказ цитаты, которая стоит за пределом
  сохранённого текста или пересекает экранированный символ. Запрещено: записать секрет (заголовки `redact_headers`, значения учётки,
  совпадение `secret_content_patterns`) в улику; отправить запрос на хост вне переданных хостов; взять аренду стенда внутри прохода;
  открыть вторую попытку на item; выдать усечённое тело как целое (метка — существующая фраза `CUT_WORDS`). Неудобные входы (FL-1 B):
  тело больше `BODY_CAP`; бинарное тело (base64 — существующее правило `body_text`); пустое тело; битый JSON при `content-type: json`;
  3xx на чужой хост (редирект не следуется — нативно); 4xx/5xx; таймаут (исход шага `timeout`); секрет в ответе (документ не
  сохраняется, выдержки нет); проект без известного HTTP-входа (`http_login_source` — EnvBlocked).
- `walk_session.capture_cited` → ворота «улика этого прохода». Допустимо: отказ законной цитаты при неполной записи прохода. Запрещено:
  принять улику прохода образца как улику первого взгляда или улику прежней головы. Неудобные входы (FL-1 A): чужой walk; walk образца;
  прежняя попытка item; запись без `stand`; путь вне корня; `quote` не в захватах; HTTP-захват чужой попытки.
- `first_look.share` → спусковой крючок вопроса. Допустимо: лишний вопрос. Запрещено: стори встаёт без слова человека; запись на другом
  коде/реестре участвует в счёте. Неудобные входы (FL-2): пустой реестр; все `nature`; 0 учтённых; слово вне данных; две строки на R-n;
  R-n вне реестра; другой `source_head`/`register_hash`; `null`; нечитаемый файл (вопроса нет, строка-пробел — FR-59).
- `ledger.plan_row_state` → отказ «зелёному» у теста с открытым помеченным локатором. Допустимо: `placeholder_open` для сверенного.
  Запрещено: `passed_green` для Then с зелёным такого теста в доказательстве или для Then из `dependents` открытой строки. Неудобные
  входы (FL-7): `settled_*` без `evidence.run`; `kept_by_decision` на настоящей стороне; Then вне `dependents` с двумя зелёными тестами,
  один с открытой строкой (доказывает только второй, FR-18); Then из `dependents`, покрытый только тестом без строки (всё равно
  `placeholder_open`); красный — `failed:*`; `skipped` у теста со строкой — `placeholder_open`; передача человеку — `placeholder_open`.
- `s5_precheck.check_sides` C3 → ворота «подмен нет, тест с заглушкой бежит». Допустимо: отказ законной строки при нечитаемой записи;
  лишнее объявление по J-C9 (a). Запрещено: подмена на настоящей стороне; тест со строкой J-C5 без прогона. Неудобные входы (FL-7):
  R-9 нет в записи; запись нечитаема/устарела; `confirms`; `missing`+`access`; `unreachable`+`nature`; `side_substitute` с `first_look:`;
  вид без `on_real`; `blocked_by_env`; передача человеку; `skipped`; тест на Then из `dependents` без объявления.
- `controller` снятие удержания (сегодня только `arrive`) → `first_look_continue` по слову человека. Допустимо: отказ снять. Запрещено:
  снять `s5_absent_side`, снять без слов, посчитать голову или хэш самому (второй читатель, AR-13). Неудобные входы (PC-6):
  `s5_absent_side`; удержания нет; `stopped`; пустые слова; нет `--source-head`; `--register-hash` не 64 hex.

---

## §2 Карта пересечений и ОДНО решение на каждое

| # | что пересекается | план 1 | план 2 | план 3 | решение (единственный дом; кто переиспользует) |
|---|---|---|---|---|---|
| a | постоянные факты о сторонах | реестр, `KEYS`, `record_problems`, страж PK0-8 | PC-1b: 3 ключа, `exact`, проверка значения, `subjects`, `side` | — | Дом — модуль PK0-1. Очереди: `project_knowledge.py` PK0-1 → PK0-3 → PC-1b; `conductor-actions.json` PK0-1 → PC-1b; `guard_pre_tool.py` TR3-5/14/16 (слиты, G4) → PK0-8 → PC-1b. Список «согласовать» t-2181 принят как поправка к t-2142 (§5) и передан Lead кучки `project-knowledge`. |
| b | реестр допущений `provisional[]` | — | PC-3, PC-4 (C3–C6), PC-5, правило заземления §2.2 | 2а: учёт красного теста на настоящей стороне; решение 4: подмен нет | Дом — `provisional[]` плана 2 (AR-15). **Правило заземления t-2181 §2.2 не меняется (решение владельца 4).** Строка `placeholder_locator` на настоящей стороне — отдельное правило УЧЁТА красного теста (2а), не дорога заземления: ничего не заземляет, тест обязан бежать и быть красным (J-C5, J-C9). Законна только с `assumed_from: first_look:<R-n>` при свежей записи `missing`/`unreachable` и `blocked_by: product`; недостижимое из-за доступа или по природе не годится никогда. Связь тест ↔ P-n — ДАННЫЕ: поле `tests[].provisional` (писатель `manifest_put.py`, PC-3, §5). ИНВАРИАНТЫ: подмен на настоящей стороне нет; строка учёта не освобождает от прогона; зелёный теста на несверенной заглушке не доказывает ни одного Then (J-C7). Узел — FL-7. |
| c | парковка и дорога прихода | — | одно состояние «держится за кодом», C12, C13, `interim-report.md`, `arrival_step` | «остановить»: парковка; при перезапуске смотрим КОД | Одно состояние, две причины (J-4): `cause: s5_absent_side \| first_look_stop`, `held_from: S6 \| S3`; для `first_look_stop` `sides` — вывод читателя, `s5_dispatch: null`, `packet` — FL-6. Выходы: `arrive`, `stop_waiting`, `first_look_continue` (только `first_look_stop`, J-C10; голову и хэш передаёт вызывающий из `first_look.current_keys`, N2). `controller.py`/`stage_guard.py` пишет только PC-6. Дорога прихода для `first_look_stop` — своя ветвь `arrival_step` (FL-6): S1, S2, обычный поток с S3; шаги 4–5 t-2181 §3.2 не применяются. |
| d | что первый взгляд узнаёт о проекте | реестр — `product.roles`, `credentials_by_role` (+ стороны) | — | карта пути: адреса, шаги, локаторы, API-маршруты, вход, данные, роли, требования к стенду | Всё — в `work/first-look.yaml` (история стори). Постоянным — только существующими дверями (J-5): роль → стратег (`product_roles`) → PK0-3 → гейт A (PK0-4); учётка → только карточка гейта A (первый взгляд пишет `unreachable`/`access` с ролью, не спрашивает); сторона → команда `side` (PC-1b); локатор и маршрут → постоянный дом — page object / API-клиент проекта, кладёт автоматор; вход → `state/sign-in-probe.json` гейта A (второй писатель запрещён); требования к стенду → план S3 / регрессия P24. Новых `KEYS` нет. |
| e | проход по старой версии и первый взгляд | — | PC-9a, PC-9b | рекордер t-1957, экраны и API | Один ходок `walk_session.py` (экран и HTTP-шаг — L1), один формат улик (`work/evidence/manual/<место>-<item>/aN/`), одна проверка цитаты, привязанная к проходу (J-C2, запись прохода с `place`, `stand`, `profiles`, `attempts`). Первый взгляд передаёт свой walk (из файла попытки) и стенд стори; PC-9a — walk окна `reference_walk` и образец. FL-1 A добавляет `survey`, `--env`, запись прохода и цитату; FL-1 B — HTTP-шаг через `manual_capture.http_call`. Писатели YAML — два (`reference_snapshot.py put`, `first_look.py put`). |
| f | закрытые вопросы и `question-prices.json` | цены на карточках | PC-2, PC-7 | FL-5 `first_look.dead`; FL-6 `first_look.same_code` | Очереди: `question-prices.json` PC-2 → PC-7 → FL-5 → FL-6; `test_human_reading.py` PC-2 → PC-7 → FL-5 → FL-6 → PC-9c. `continue` обоих вопросов — одна операция `first_look_continue`. `awaiting.stop` годится и для `first_look_stop`. |
| g | горячие файлы | — | — | — | `controller.py`, `stage_guard.py` — только PC-6 (после G3); `story_run.py` — функции по волнам (§4.4); `gate_preflight.py` — PK0-4/PK0-5 функциями (после G1, где D8 пишет `_actors_of_manual_cases`, `_probe_actor`), затем PK0-9; `exit_gate.py` — только FL-5; `walk_session.py`, `manual_capture.py` — только FL-1 (A, затем B; после G1); `hooklib.py`, `install_smoke.py` — никто. |
| h | брифы | PK0-2: роли в S3 (с маркером) | PC-8: S5, привязка, строки сторон с маркером и бриф критика кода | FL-3: бриф раннера; FL-4: строки S3/S4/S5/S6/S7 + брифы критика кейсов и критика кода | Одна функция `brief_pack.build`: TR4-12 (слит) → PK0-2 → FL-3 → PC-8 → FL-4; голова не сокращается. |
| i | хартии | PK0-2: стратег | PC-8: автоматор, критик кода, тестировщик требований; PC-5a, PC-9a | FL-3: раннер; FL-4: стратег, автор кейсов, критик кейсов (+ знания проекта — правило проекта), explore-charter; FL-7: автоматор, критик кода (+ стороны и учётки проекта) | Очереди: `qa-test-strategist.md` PK0-2 → FL-4; `qa-automator.md`, `qa-code-critic.md` PC-8 → FL-7; `qa-runner.md` TR3-10 (G1) → PC-5a → FL-3; `qa-requirements-tester.md` PC-8 → PC-9a (2-й коммит); `qa-case-designer.md`, `qa-case-critic.md`, `explore-charter.md` — только FL-4. |
| j | вход на стенд | PK0-5 | — | вход нужен до гейта A | Первый взгляд правило PK0-5 не читает и не спрашивает: драйвер открывает проход гостем; экранный проход — раннер входит записанной учёткой стенда (`read_login`, `credentials_by_role`) через `fill-account`, и HTTP-шаги того же актёра идут контекстом его браузера (`_BackendHttp`, его cookies); проход без экрана — актёр `default` (если учётка стенда по умолчанию записана) входит Bearer `_http_login` через `http_login_source` один раз при открытии (J-18); нет учётки или входа — `unreachable`/`access`, без вопроса (P5, D-0043). |
| k | красный тест: баг или нет | — | D2 | решения 3/4 | Различает только реальность стороны: `absent` → `pending_implementation`; `real` → красный в S7. Новых слов вердикта нет. |
| l | S-a и первый взгляд | — | `absent` и `deliverable` | ложный вопрос | Не идёт при `contract.parks_after_s5` (`null: no_code_yet`); на дороге прихода S-a не повторяется (J-8). |
| m | S-b и первый взгляд | — | подмена, штамп | статусы на моке | Идёт; запись несёт `sides_met` (условие S13); вопрос и брифы называют подменённые стороны; наблюдение на подмене — не доказательство. |
| n | S-c и первый взгляд | — | окно S1 по образцу | локаторы новой версии | Оба прохода идут своими walk (J-C2). Порядок подсказок автоматору (FL-7): увиденное первым взглядом на новой версии (локатор, маршрут, данные) → переносимое образца → своя живая разведка → правило фреймворка → помеченная заглушка. |
| o | `design/state-exits.md` | PK0-1 (спека: `references/…` — такого нет) | PC-3, PC-6 | FL-2 | Путь — `design/`. Строка реестра PK0-1 не проверяется `test_state_exits.py` (тот перечисляет ключи `controller.projection([])` и ключи слияния `manifest_put`) → передана PK0-6. Строку `provisional[]` тест требует → у PC-3. Очередь: сессия → PC-3 → PC-6 → FL-2 → PK0-6; слияние с сессией — по условиям J-14 (a) (§4.2). |
| p | `judgment-census.json` | PK0-1 (+`safety` 51→52), PK0-4 | PC-4, PC-6, PC-5a, PC-9b | FL-2; FL-7 (только если unit) | Перенести строку нельзя (`test_c1_every_unit_has_a_row_and_every_row_a_unit`). Ожидаемые подъёмы и их одобрение — таблица §4.7. Очередь: (писатели сессии и соседних веток §4.1, любой порядок, суммой) → PK0-1 → PC-4 → PK0-4 → PC-6 → FL-2 → PC-5a → FL-7 → PC-9b. |
| q | `stages.json` | — | PC-9b: S1 | FL-3: S3; входы S3–S7 и брифы критиков S4/S5 | Очередь FL-3 → PC-9b. Новой стадии нет (J-2). |
| r | слова контроллера | — | PC-6 | `first_look`, `first_look_continue` | Добавляет PC-6. |
| s | `role-commands.json` | — | PC-9b | FL-2 | Очередь TR3-10 D (G1) → FL-2 → PC-9b. |
| t | `report_facts.py`, `architecture.md`, `SIBLING_MAP.md` | PK0-6 (только `architecture.md`, `SIBLING_MAP.md`) | PC-10 | FL-8 (счётчики цены, использования, `knowledge_use`) | Очереди: `report_facts.py` — TR3-10 (G1) → PC-10 → FL-8 (PK0-6 этот файл не пишет, m-new-7); `architecture.md`, `SIBLING_MAP.md` — PK0-6 → PC-10 → FL-8. |
| u | `walk_session.py`, `manual_capture.py`, `manual-capture-steps.json` | — | (PC-9b косвенно) | FL-1 A (`walk_session.py`), FL-1 B (все три) | Сессия пишет их в TR3-10 C, D, D3a, D3c, D8 → FL-1 после G1; часть B — после слияния части A. |
| v | `null-outcomes.json`, `artifact-writers.json` | — | PC-3 | FL-1 A, FL-2 | `null-outcomes.json` PC-3 → FL-2; `artifact-writers.json` FL-1 A → FL-2. |
| w | `scripts/tests/fixtures/driver-layers.json` | — | PC-2, PC-7 | FL-5, FL-6 | Строки на каждого нового члена `Driver` (`test_driver_layers.py` L1). Порядок — порядок `story_run.py`: строки сессии (TR3-10 D +24, TR4-10 A1 +5) первыми, затем PC-2 → PC-7 → FL-5 → FL-6 (N4). |
| x | `references/slices/<роль>/<тема>.md` (коммитятся, `contract_slices.py --check` — красная сборка при устаревшем срезе) | — | PC-3, PC-5a, PC-9a | FL-2 (только если новая ссылка попадёт в `inject-map.json`), FL-7 | Узел, правящий нарезанную ссылку, владеет её срезами и гоняет `--check` (N4): `artifact-contract-automation.md` — PC-3 → FL-7; `artifact-contract-run.md` — PC-5a; `vocabularies.md` — PC-9a. |

---

## §3 Единая таблица узлов

Исполнитель — как в источниках; «builder → critic» = sonnet-билдер, opus-критик. Свидетель — только названные быстрые файлы узла
(`plans/builder-rules.md` 7b); `test_story_run_*`, `test_controller_*`, `slow_tests.json` (в т. ч. `test_driver_layers.py`,
`test_manual_capture.py`, `test_s5_precheck.py`, `test_walk_road.py`), `test_judgment_census.py` — только CI; канон пачки — пайплайн CI.
Каждый узел пакета несёт строки `architecture:` и `judgment:`, проходит разделы FR, которые трогает. «Зависит от» называет ворота
сессии G1–G4 (§4.1), если узел пишет её файл. Узел, пишущий census, называет в вердикте подъём по строке §4.7; сверх неё — стоп.
Узел, пишущий census или `design/state-exits.md`, сливается с сессией по условиям J-14 (a) (§4.2).

### 3.1 Узлы плана 1 (PK0-*) — пачка `project-knowledge/1`, по t-2142 §5

| узел | что | пишет (горячий файл — функции) | зависит от | свидетель | исполнитель | AR | изменено |
|---|---|---|---|---|---|---|---|
| PK0-1 | реестр ответов, `state`, `roster`, `record`, `revoke`, `story_roles`, `acting_line`, CLI | `scripts/project_knowledge.py`, тест, `references/install-paths.json`, `references/collect-sets.json`, `references/conductor-actions.json`, `scripts/tests/fixtures/judgment-census.json` (строки `record_problems`, `_refuse_no_trace`; §4.7), changelog | — (J-14 (a): стартует сейчас; census — слиянием по условиям §4.2) | `test_project_knowledge.py`, `test_environment_record.py`, `selftest --limits --lang`, `refusal_registry --sites`; после слияния сессии (если она слилась раньше) — CI ветки для `test_judgment_census.py` | builder → critic (после этого слияния) | AR-13, 14, 24, 25, 28, 29 | изменено: строка `design/state-exits.md` передана PK0-6 (тест её не проверяет); три ключа сторон добавит PC-1b; старт сейчас (J-14 (a)) |
| PK0-2 | перечень ролей в брифе S3, абзац хартии стратега; каждая строка перечня несёт маркер `[knowledge:product.roles]` (L3) | `scripts/brief_pack.py` (`s3_roster_lines` + вызов в голове S3 `build`), `agents/qa-test-strategist.md` | PK0-1 (подтягивается сразу) | `test_brief_s3_roster.py` (+ `roster_lines_carry_knowledge_marker`), `test_role_load.py`, `role_load --all` | builder → critic | AR-10, 11, 13, 29 | изменено: маркер (L3; маркер — данные для счёта FL-8, не текст для роли); очередь `build`: TR4-12 → PK0-2 → FL-3 → PC-8 → FL-4 |
| PK0-3 | раздел `product_roles` передачи S3 и регистратор замеченных ролей | `handoffs/s3-strategist-to-designer.yaml`, `scripts/project_knowledge.py` (`notice_from_handoff`), `scripts/story_run.py` (`Driver.gate_repair`) | PK0-1; G1, G2 | `test_knowledge_notice.py`, `test_role_load.py` | builder → critic | AR-10, 21, 22, 23, 28, 29 | нет |
| PK0-4 | карточка «стенд + роль», близнецы, подтверждение ролей, «по прежним ответам»; строка «по прежним ответам» несёт маркер `[knowledge:credentials_by_role]` (L3) | `scripts/gate_preflight.py` (`check_role_accounts`, `role_gap_id`, `Rehearsal.__init__`, `gap_name`, `check_case_preconditions`, `_probe_actor`, `run`), `scripts/stand_gaps.py` (`_gate_a_gaps`, `_PASS_THROUGH`), `scripts/gate_brief.py` (`_gap_heading`, `stand_gap_form_ids`, `_card`, `stand_gap_card_lines`), census (строка `check_role_accounts`; §4.7) | PK0-1; **G1** (D8 пишет `Rehearsal._probe_actor` и `_actors_of_manual_cases`; PK0-4 нужен `_probe_actor` — близнец карточки, `test_probe_actor_no_second_card`) | `test_gate_role_accounts.py` (+ `known_answer_line_carries_marker`), `test_stand_gaps.py`, `test_stand_gap_contract.py`, `test_stand_gap_remedy.py` | builder → critic | AR-9, 10, 13, 15, 16, 18, 19, 28, 29 | изменено: ворота G1 (N6); маркер (L3) |
| PK0-5 | учётка по умолчанию — по нужде, одно правило гейта A и S6 | `scripts/gate_preflight.py` (`default_login_needed`, `check_s5_credentials`), `scripts/story_run.py` (`Driver.stand_login_problem`) | PK0-1; G1, G2 | `test_login_need.py`, `test_manual_actor.py` | builder → critic | AR-19, 13, 28, 29 | нет (функции не пересекаются с D8) |
| PK0-6 | тексты дирижёра, ось 34, текст AR-3, индекс; строка реестра в `design/state-exits.md` | `skills/qa-story/phases/s4.md`, `references/environments.md`, `design/architecture.md`, `docs/SIBLING_MAP.md`, `docs/ARCHITECTURE_INDEX.md`, `design/state-exits.md` | PK0-1..5, 8, 9 | `architecture_index.py --check`, `selftest --limits --lang`, `test_state_exits.py`, ключи с отрицательным контролем | builder | AR-3, 15, 17, 25 | изменено: принимает строку `design/state-exits.md` от PK0-1 (M6); `report_facts.py` не пишет (m-new-7) |
| PK0-7 | живое: две стори подряд на MyBooks (t-2142 §8) | — | PK0-6 | журнал, `gate-a-message.md`, `show --json`: «гейт A не спросил снова» — по журналу закрытых вопросов | Lead + стенд | FR-33 | нет: проверка по t-2142 без изменений; проверка «известная роль и учётка — `used` в ретро» перенесена в FL-L3 (N7) |
| PK0-8 | страж закрывает команды записи реестра от ролей | `scripts/guard_pre_tool.py` (`human_word_check`, `HUMAN_WORD_MSG`, `STAND_RECORD_FILES`) | PK0-1 (G4 выполнено) | `test_guard_project_knowledge.py`, `test_guard_command_text.py` | builder → critic | AR-14, 11, 29 | изменено: G4 выполнено (N6), подтягивается сразу после PK0-1 |
| PK0-9 | «не роль продукта» не переспрашивается на гейтах A и B | `scripts/gate_preflight.py` (`check_role_accounts`, ветвь `not_needed`), `scripts/stand_gaps.py` (`PK_BY`, `covered_says`, `covered_entries`, `write_environment_overrides`, `write_carries`, `revoke_environment_overrides`, `_c2`, `_c4`, `gate_b_split`), `scripts/gate_brief.py` (`_covered_block`), `scripts/story_run.py` (`Driver.revoke_environment_properties`) | PK0-4, PK0-5; G1, G2 | `test_not_needed_role.py`, `test_stand_gaps.py` | builder → critic | AR-15, 22, 24, 25, 27, 28, 29 | изменено (пометка): тест назван по спеке (`test_not_needed_role.py`), пачка пишет `test_not_a_role_carry.py`; по правилу пачки побеждает спека |
| PK0-10 | остатки §6 R-2 находками; указатели `перенос: project-knowledge` | `plans/piles/project-knowledge/findings/`, `.../README.md` (+ строки в невзятых пачках кучек-источников) | — | ключи с отрицательным контролем | builder (не код) | — | изменено: находка-указатель «первый взгляд не пишет реестр; кандидаты (маршруты, тест-данные) — для каталога фазы 1» (J-5) |

### 3.2 Узлы плана 2 (PC-*) — пачка `pre-code/1`, по строке t-2181 §7

| узел | что | пишет (горячий файл — функции) | зависит от | свидетель | исполнитель | AR | изменено |
|---|---|---|---|---|---|---|---|
| PC-1a | данные сторон, один читатель, читатели удержания | `references/side-realities.json`, `scripts/contract.py` (`story_sides`, `parks_after_s5`, `awaiting`), `scripts/stage_done.py` | — | `test_story_sides.py` | builder → critic | AR-1, 2, 13 | изменено: `contract.awaiting` возвращает `cause` (умолч. `s5_absent_side`) и `held_from` (умолч. `S6`); тест на запись без полей и с `first_look_stop`/`S3`. C17 t-2181 ложится ВНУТРЬ существующей единицы `stage_done.coerce_value` (или `parse_sets`): новая единица в `stage_done.py` (файл пути блокировки, 13 ролей) подняла бы `blocking_per_role` всех ролей — стоп и вопрос; census узел не пишет |
| PC-1b | ветвь реестра: 3 ключа, `exact`, `subjects`, `side`, страж, `sides_unknown` | `scripts/project_knowledge.py` (`KEYS`, `_exact_form`, `record_problems`, `subjects`, `side`), `references/conductor-actions.json`, `scripts/guard_pre_tool.py` (`human_word_check`, `HUMAN_WORD_MSG`), `scripts/contract.py` (`story_sides`, ветвь реестра), `scripts/story_run.py` (`Driver.s0_write_sides`, `Driver._keep_sides_answer`) | PK0-1, PK0-3, PK0-8, PC-1a, PC-2, PC-9a | `test_story_sides.py`, `test_project_knowledge.py`, `test_guard_project_knowledge.py`; CI: `test_driver_layers.py` | builder → critic | AR-3, 13, 14, 28 | изменено: `test_driver_layers.py` — CI (медленный) |
| PC-2 | запуск: `--side`, `--reference`, «код ещё не написан», «чья сторона» | `scripts/story_run.py` (`s0_note_launch`, `s0_keep_late_launch`, `launch_flags`, `s0_no_change_entry`, ветвь `s1.no_diff`, argparse, `Driver.s0_write_sides`, `Driver._keep_sides_answer`), `references/question-prices.json`, `skills/qa-story/phases/s1.md`, `agents/qa-scout.md`, `scripts/tests/fixtures/driver-layers.json` (строки `s0_write_sides`, `_keep_sides_answer`) | PC-1a; G1, G2 | `test_no_mr_entry.py`, `test_story_run_words.py`; CI: `test_driver_layers.py` | builder → critic | AR-16, 19, 24 | изменено: `driver-layers.json` в owns (N4) |
| PC-3 | поля манифеста: `provisional[]`, `tests[].sides`, `tests[].provisional`, `about`, `runs[].kind` | `references/provisional-kinds.json`, `references/artifact-contract-automation.md`, `references/slices/{qa-automator,qa-code-critic,qa-failure-analyst}/artifact-contract-automation.md` (те, что `--check` назовёт), `scripts/manifest_put.py`, `scripts/contract.py` (`manifest_provisional`), `scripts/manifest_from_tests.py`, `references/null-outcomes.json`, `design/state-exits.md` (строка `provisional[]`) | PC-1a (J-14 (a): стартует сразу после слияния PC-1a; state-exits — слиянием по условиям §4.2) | `test_provisional.py`, `test_manifest_put_merge.py`, `test_null_outcomes.py`, `test_state_exits.py` (локально и после слияния сессии), `python -B scripts/contract_slices.py --check` | builder → critic (после слияния сессии, если оно было) | AR-14, 22, 23, 25 | изменено (B3): поле `tests[].provisional: [P-n]`; пишет только автоматор фрагментом через `manifest_put.py` (слияние по экземпляру); отсутствие = `[]`; читатель `contract.manifest_provisional` (и карта тест → P-n); тесты `tests_provisional_merged_by_instance`, `absent_tests_provisional_reads_empty`; проверка объявления — FL-7 (J-C9 (a)); срезы (N4); старт J-14 (a) |
| PC-4 | проверки выхода S5 C1–C6, `pending_instances`, свидетель-сборка, `_all_pending` | `scripts/acceptance.py`, `scripts/s5_precheck.py` (`check_sides`, семья `sides`, `WORD_PASSABLE_TAGS`), `scripts/window_record.py`, `scripts/run_suite.py` (`--collect-only`), `scripts/check_witness.py`, census (строка `check_sides`; §4.7) | PC-3 (подтягивается) | `test_s5_precheck_sides.py`, `test_check_witness.py`, `test_window_record.py`, `test_run_suite_mine.py` | builder → critic | AR-9, 10, 15, 20, 28, 29 | изменено: подъём census названн (§4.7: `blocking_per_role.qa-automator` +1) |
| PC-5a | штамп сторон на блоках исполнения | `scripts/run_suite.py` (`build_run_block`, `reparse_run_block`), `scripts/manual_evidence.py` (`write_block`, `validate`), `scripts/finalize_task.py` (`reduce`), `references/artifact-contract-run.md`, `references/slices/{qa-runner,qa-doc-scribe,qa-failure-analyst}/artifact-contract-run.md` (те, что `--check` назовёт), `agents/qa-runner.md` (строка), census (строка `manual_evidence.validate`: класс; §4.7) | PC-4, PC-1a; G1 (`qa-runner.md` пишет TR3-10) | `test_proof_stamp.py`, `test_manual_evidence.py`, `test_manual_projection.py`, `test_run_suite_mine.py`, `python -B scripts/contract_slices.py --check` | builder → critic (обязателен) | AR-14, 21, 22, 28 | изменено: срезы (N4) |
| PC-5 | леджер и вердикт | `scripts/ledger.py` (`plan_row_state`, `_resolved_about`, `_met_real`), `references/delivery-verdict-kinds.json`, `scripts/check_delivery.py` (`assess`), `scripts/factory_dashboard.py` | PC-5a, PC-3 | `test_sides_ledger.py`, `test_third_verdict.py`, `test_report_facts.py`, `test_check_delivery.py` | builder → critic (обязателен) | AR-26, 27, 28 | изменено: слова и метка `awaiting_implementation` по `cause` («stopped after the first look: the feature does not work yet» / «waiting for a fix»); тест `first_look_stop_reads_awaiting_implementation` |
| PC-6 | контроллер и страж: удержание за кодом | `scripts/controller.py` (`PURPOSES`, `REPAIR_CAUSES`, `APPLY_OPERATIONS`, `projection`, `Controller._project_pipeline`, `Controller._next_action_for_state`, `Controller.build_rework_request`), `scripts/stage_guard.py` (`rule_awaiting_code`, `dispatch_errors`, `stories`), `scripts/archive_task.py` (`open_items`), `design/state-exits.md`, census (строки `rule_awaiting_code`, `build_rework_request`, `apply(first_look_continue)`; §4.7) | PC-1a; G3 (`controller.py`); census и state-exits — слиянием по условиям J-14 (a) | `test_awaiting_state.py`, `test_stage_guard.py`, `test_archive_task.py`, `test_state_exits.py`, `test_gate_registry.py` | builder → critic (обязателен) | AR-1, 9, 17, 20, 24, 25, 28 | изменено: `PURPOSES` += `first_look`; `await` несёт `cause`, `held_from`; для `first_look_stop` `s5_dispatch: null`, `sides` от читателя; удержание, C12, `rule_awaiting_code` — стадии ≥ `held_from`; `held` — не начатые диспатчи ≥ `held_from`; доработка S0..(held_from−1) — внутри удержания; `stories`, `open_items` печатают причину. НОВАЯ операция `first_look_continue --words-file F --source-head H --register-hash R` (N2): `H` — канонический JSON-текст карты голов, `R` — 64 hex; оба ВЫЧИСЛЯЕТ вызывающий (FL-5/FL-6, скилл-путь `s3.md`) через `first_look.current_keys`; PC-6 их не считает и не разбирает (данные несутся как даны, AR-13) — событие `first_look_continued {source_head: H, register_hash: R, words, at}`, проекция `pipeline.first_look_continue`; при `first_look_stop` снимает `awaiting`; без удержания — только запись; отказ с дверью (J-C10): `s5_absent_side`/`stopped`; пустые слова; нет `H`; `R` не 64 hex. ВРЕМЕННОЙ край: до слияния FL-2/FL-5 операцию не зовёт никто (операция не зависит ни от чего, что определит FL-2). Строка `first_look_continue` в state-exits. Тесты: `first_look_stop_holds_s3`, `rework_s2_allowed_while_first_look_held`, `rework_s2_end_holds_again`, `rework_s3_refused_while_first_look_held`, `await_without_cause_reads_s5_absent_side`, `first_look_stop_record_has_null_s5_dispatch`, `first_look_continue_clears_first_look_stop_hold`, `first_look_continue_refused_on_s5_absent_side`, `first_look_continue_without_hold_records_only`, `first_look_continue_empty_words_refused`, `first_look_continue_stores_given_keys`, `first_look_continue_without_keys_refused`, `first_look_continue_bad_register_hash_refused`; `test_stage_guard.py::s3_role_refused_while_first_look_held` |
| PC-7 | драйвер: стоп после S5, приход кода | `scripts/story_run.py` (`run`, `arrival_step`, `_act_await_implementation`, `_act_awaiting_stopped`, `dispatch_action`, `until_reached`), `scripts/interim_packet.py`, `references/question-prices.json`, `skills/qa-story/phases/s5.md`, `scripts/audit_factory.py`, `scripts/tests/fixtures/driver-layers.json` (строки `arrival_step`, `_act_await_implementation`, `_act_awaiting_stopped`) | PC-2, PC-4, PC-6 | `test_interim_packet.py`, `test_story_run_words.py`, `test_human_reading.py`; CI: `test_driver_layers.py`, `test_story_run_arrival.py` | builder → critic | AR-16, 17, 21, 24 | изменено (пометка, m7): до слияния FL-6 для любой причины печатается пакет S5 — инертно по J-11; `driver-layers.json` (N4) |
| PC-8 | хартии и брифы S5 / привязки; строки сторон в брифе S5 несут `[knowledge:<ключ стороны>]`, когда сторона пришла из реестра (`source: registry`), и те же строки получает бриф критика кода (вызов той же функции в голове его брифа) (L3) | `agents/qa-automator.md`, `agents/qa-code-critic.md`, `agents/qa-requirements-tester.md`, `scripts/brief_pack.py` (`build`), `skills/qa-story/phases/s2.md`, `s5.md` | PC-4; `s5.md` после PC-7; `build` после PK0-2 и FL-3 | `test_brief_pack.py` (+ `sides_lines_marked_and_given_to_code_critic`) (+ `role_load --all`) | builder → critic | AR-7, 10, 11, 12, 13, 29 | изменено: маркер и бриф критика кода (L3); бриф S5 называет и поле `tests[].provisional` |
| PC-9a | старая версия: форма снимка, писатель, прецедент, `parity` | `references/artifact-contract-reference.md`, `scripts/reference_snapshot.py`, `scripts/contract.py` (`PRECEDENT_REF_RE`, прецедент, `parity`), `references/vocabularies.md`, `references/slices/*/vocabularies.md` (10 ролей со срезом; те, что `--check` назовёт), `agents/qa-requirements-tester.md` (абзац — 2-й коммит после PC-8) | PC-1a, PC-3; FL-1 A | `test_reference_snapshot.py`, `test_oracle_provenance.py`, `python -B scripts/contract_slices.py --check` | builder → critic | AR-6, 21, 26 | изменено: цитата — `walk_session.capture_cited(task_root, walk, item, path, quote, stand=<образец>)`, `walk` — новейший диспатч S1 с целью `reference_walk` (берёт код, не роль); тест `reference_put_refuses_first_look_capture`; срезы (N4); новая ссылка в `inject-map.json` не вносится (иначе срезы и строка хартии — в owns, role-load — J-15, стоп и вопрос) |
| PC-9b | старая версия: проход на S1, образец, запрет тестов по образцу | `references/stages.json` (S1), `scripts/story_run.py` (`stage_simple`), `scripts/stand_identity.py`, `scripts/runtime_probe.py`, `scripts/run_suite.py` (C8), `scripts/execution_request.py`, `references/role-commands.json`, census (C8; §4.7) | PC-7, PC-5a, PC-9a, PC-6, FL-1 A, FL-2, FL-3 | `test_stand_identity.py`, `test_run_suite_mine.py`, `test_execution_request.py`; CI: `test_story_run_reference_walk.py::reference_window_opens_survey_env_walk` | builder → critic | AR-4, 8, 11, 20 | изменено: окно открывает драйвер `walk_session.py open --place survey --env <образец> --walk <id диспатча>`; тест на аргументы назван (m-new-8); census C8 (§4.7) |
| PC-9c | гейт A для стори с образцом | `scripts/gate_brief.py`, `test_human_reading.py` | PC-9a; PK0-9; FL-6 | `test_gate_brief_and_retro.py` (CI), `test_human_reading.py` | builder → critic | AR-16, 26 | изменено: очередь `test_human_reading.py` … → FL-6 → PC-9c |
| PC-10 | замеры, детекторы, члены оси 34, калибровка | `scripts/report_facts.py`, `design/architecture.md`, `docs/SIBLING_MAP.md`, `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` | PC-5, PC-7, PK0-6 | `test_report_facts.py`, `architecture_index --check` | builder → critic | AR-12, 13, 20 | нет |
| PC-L | живые S-a, S-b, S-c | — | §4.6 | журнал, `interim-report.md`, `test-report.md` | Lead + стенд | FR-33 | нет |

### 3.3 Узлы плана 3 (FL-*) — пачка `pre-code/2`

FL-0 (спека первого взгляда, designer → critic на план) — **изменено: содержание — узлы FL-1…FL-8 и FL-L ниже** (J-12 (a)); критик на план
пройден (`docs/tasks/specs/reviews/t-2277-joint-plan-critic.md`, повторный — `t-2288-joint-plan-rereview.md`).

**FL-1 — ходок для первого взгляда.** Один id, ДВЕ части с отдельными owns, тестами, стартом и критиком (N1): часть A — место `survey`,
`--env`, запись прохода, цитата прохода; часть B — HTTP-шаг ходока (L1). Часть A уходит первой; часть B — после слияния A.

**FL-1 часть A — `survey`, `--env`, запись прохода, `capture_cited`** (builder → critic; старт — после G1)
- Пишет: `scripts/walk_session.py` (`PLACES`, `LANE_PREFIX`, `request_problems` — текст item и дверь, `Walk._start`, путь `page_lease`
  в операциях `LEASE_OPS`, `Walk.item_root`, `takes_new_item`, `op_verdict`, `_time_items`, `Walk.write_state`, `build_parser`, `open_walk`,
  `serve`, новая `capture_cited`); `references/artifact-writers.json` (корень `work/evidence/manual/survey-*/`);
  `scripts/tests/test_walk_survey_place.py` (новый); `changelog.d/t-2277-fl-1a.md`.
- Шаг 0: перечитать слитые после G1 `walk_session.py`, `walk_pool.py` (claims, `claim_problems`). Ветвь по месту прохода, которой нет в
  этом тексте, — стоп и вопрос Lead.
  1. `PLACES` += `survey`; `LANE_PREFIX["survey"] = "survey-"`. Значение `survey` в каждой ветви по месту:

     | ветвь (функция) | `case` | `settle`/`control` | `survey` |
     |---|---|---|---|
     | текст item в `request_problems` (`LANE_ID`) | id кейса | `LANE_ID` | `LANE_ID` (`R-1` проходит) |
     | дверь отказа `item` | — | `manual_capture.py … --case settle-<id>` | «item прохода `survey` — R-n или id элемента снимка; запись — `first_look.py put` / `reference_snapshot.py put`» |
     | захват стенда в `Walk._start` | `_hold_walk` на всю жизнь | `page_lease` на старт | `_hold_walk` на всю жизнь |
     | `page_lease` на каждый запрос `LEASE_OPS` | нет | да | НЕТ (иначе проход откажет сам себе `stand_busy`) |
     | корень попытки (`MC.Attempt`) | id кейса | `<place>-<item>` | `survey-<item>` |
     | `takes_new_item` | нет | `lane_item_ok` | `lane_item_ok` |
     | `op_verdict` | вердикт | отказ, дверь `place_answers.py` | отказ, дверь — команды записи прохода |
     | правила записи кейса (`_look_when_empty`, `walk_rule_errors`) | да | нет | нет |
     | `op_close` → `_time_items` | нет | да | да |
     | `idle_s` / сторож | да | да | да |
     | пул учёток (`walk_pool`) | по дорожке | по дорожке | не берёт: актёр дан при открытии |

     Тесты: `survey_attempts_under_survey_root`, `survey_has_no_case_verdict`, `survey_holds_lease_for_life`,
     `survey_requests_take_no_page_lease`, `survey_item_door_names_put_commands`, `survey_close_writes_timing`.
  2. `--env <имя>` у `open` и `serve` (`build_parser`, `open_walk`, `serve`): строка `environments[]` с `name` ТОЧНО; `self.stand` — эта
     строка; `self.hosts` — хосты ТОЛЬКО этой строки (`MC.stand_hosts` над конфигом с одной этой строкой); без `--env` — как сегодня (байт
     в байт для S6/S7). Нет имени → отказ «стенда `<имя>` нет в config.json; есть: <имена>» (J-C1). Тесты: `env_by_exact_name`,
     `env_case_variant_refused`, `env_absent_name_refused`, `no_env_keeps_first_row`, `env_hosts_are_the_named_stand_only`.
  3. Запись прохода (`write_state`) += `place`, `stand`, `profiles: {ui: id}` (часть B добавит `http`), `attempts: {item: попытка}`. Тест
     `walk_record_names_place_stand_profiles_attempts`.
  4. Новая чистая `capture_cited(task_root, walk, item, path, quote="", stand="") -> str`: "" только когда запись `walk` читается, `place`
     `survey`, `stand` совпадает (если дан), `attempts[item]` есть, `path` под `work/evidence/manual/survey-<item>/<эта попытка>/`, файл
     читается, `quote` найден `_quote_home` (через `ME._quote_in`) в тексте захватов попытки, как он СОХРАНЁН (`captures.jsonl` — экранные
     и HTTP-строки; у HTTP-захвата — сохранённый JSON-документ запроса и ответа); иначе причина с дверью. Направление ошибки: цитата,
     пересекающая экранированный в JSON символ (кавычка, перевод строки), стоящая в усечённой за `BODY_CAP` части или в base64-теле, —
     отказ (допустимо: роль цитирует фрагмент без таких символов, бинарное тело описывает в `why`). Тесты: `capture_in_attempt_ok`,
     `capture_of_other_item_refused`, `capture_of_other_walk_refused`, `capture_of_reference_walk_refused_for_first_look`,
     `capture_of_earlier_attempt_refused`, `walk_record_without_stand_refused`, `quote_not_in_file_refused`, `path_outside_root_refused`,
     `quote_across_escaped_char_refused`.
- Профиль (m3): нового флага нет; несколько UI-профилей и нет плана (S3) → `capture_profile` отказывает до браузера → FL-5 пишет
  `null: profile_not_chosen`.
- Края: образец как `--env` прохода `survey` разрешён (S-c); образец в прогоне тестов стори — C8 PC-9b. ИНВАРИАНТЫ: S6/S7 без `--env`
  идут ровно как сегодня; проход по стенду, не названному точно, невозможен; улика одного прохода не цитируется записью другого.
- Свидетель: `python -B scripts/tests/test_walk_survey_place.py`; CI: `test_walk_road.py`, `test_walk_lanes_parallel.py`.
- AR-1, AR-4, AR-6, AR-13, AR-19. Census: `request_problems` — существующий unit (xref), класс не меняется; `capture_cited` — не unit;
  подъём 0 (§4.7).

**FL-1 часть B — HTTP-шаг ходока (L1)** (builder → critic, свой проход критика; старт — после слияния части A; G1 уже есть)
Слово владельца 10.11.2026: «чтобы не возвращаться к вопросу, архитектура без костылей». Один ходок для UI и не-UI стори; HTTP-шаг —
полноправный шаг того же `walk_session.py step`; один исполнитель запроса — ИЗВЛЕЧЁННАЯ функция, не вызов CLI `run_http` (N1).
- Пишет: `scripts/manual_capture.py` — новая `http_call`, новые `_run_http_word`, `_http_word_problem`, `_http_surprises`, новый класс
  `HttpOnlyBackend`; изменяются `_run_http` (тело цикла по вызовам → `http_call`), `parse_steps` (параметр `http_ok`, ветвь `http`),
  `_run_step` (ветвь `http`), `PlaywrightBackend` (свойство `allowed_hosts`, читает уже хранимый `self._allowed`);
  `scripts/walk_session.py` — `Walk._start` (выбор поверхности прохода), `Walk._open_actor` (ветвь без экрана), `Walk.op_step`
  (`http_ok=True`; отказ экранного слова в проходе без экрана), `request_problems` (`http_ok=True`; разрешение и проверка URL
  HTTP-шага), `Walk.write_state` (`profiles.http`); `references/manual-capture-steps.json` — строка `steps.http`, ключи
  `surprise.http_steps`, `surprise.http_kinds`; `scripts/tests/test_walk_http_step.py` (новый); `changelog.d/t-2277-fl-1b.md`.
- Шаг 0: перечитать `manual_capture.py` (`_run_http`, `run_http`, `_side`, `cut_body`, `body_text`, `CUT_WORDS`, `_limit_words`, `redact`,
  `_hide`, `secret_pattern_hit`, `Attempt.surprise`, `Attempt.detector`, `_surprises_after`, `_BackendHttp`, `PlaywrightBackend.http`,
  `UrllibHttp`, `_http_login`, `http_login_source`, `read_login`, `host_key`, `stand_probe`) и данные `manual-capture-steps.json` (`steps`,
  `surprise`, `http_methods`, `redact_headers`). Расхождение с текстом ниже — стоп и вопрос Lead.
  5. **Одна функция-исполнитель (AR-15).** `http_call(attempt, client, method, url, body, headers, *, hosts, timeout_s, spec_data, cfg,
     phase, proves, step_line, label="request-response", kind="request_response", hide=(), created=None, store=None, case="") -> dict`
     (`{"entry": строка steps.jsonl, "result": HttpResult | None, "failed": dict | None, "recorded": имя | None}`) делает ОДИН запрос при
     уже выбранном стенде и уже открытой попытке: (1) хост URL (`host_key`) ∈ `hosts`, иначе отказ, ничего не отправлено; (2) запрос, URL и
     заголовки без `GENERATED_*`, тело с `GENERATED_*` — только при данном `created`; текст запроса без совпадения
     `secret_content_patterns` (как сегодня в `_run_http`, идемпотентно); (3) `client.request`; `StepTimeout`/`StepFailed` → строка шага
     `timeout`/`failed`, как сегодня; (4) документ `{request: _side(...), response: _side(...)}` — `cut_body`/`body_text` (base64 для
     не-UTF-8 — существующее правило, второго нет), `redact` по `redact_headers`; затем `_hide` по каждой учётке из `hide` и по
     `created`; затем `secret_pattern_hit` — совпадение: документ НЕ сохраняется, выдержки нет, `ValueError` с текстом как сегодня;
     (5) `attempt.store_text(...)` с меткой `_limit_words` (фраза `CUT_WORDS`) при усечении. АРЕНДЫ НЕ БЕРЁТ, `environment_of`/`stand_hosts`
     НЕ ЗОВЁТ, попытку НЕ ВЫБИРАЕТ, вход НЕ ДЕЛАЕТ — всё это делает вызывающий. `_run_http` остаётся вызывающим: аренда `_hold_stand`,
     `environment_of`, `choose_attempt_for`, вход (`--session` / Bearer) — как сегодня, затем `http_call` на каждый вызов
     (`request-response`, `state`) с `hosts = set(stand_hosts(cfg, root=project_root))`, `hide=()`, своими `created`/`store`/`case`; вывод
     байт в байт (тест `run_http_unchanged`: существующие `test_manual_capture.py` (CI) и `test_manual_capture_session.py` зелёные без
     правки + `run_http_calls_http_call_per_call`).
  6. **Грамматика шага (J-C11).** Строка таблицы `steps`: `"http": {"args": "<METHOD> <path|url> [--body-file <file>]", "arity": [2, 4],
     "does": "one HTTP request on the walk's stand, sent as the request's actor; walk only"}`. `parse_steps(text, spec_data, words="steps",
     selectors=None, need_goto=True, http_ok=False)`: после проверки арности для `word == "http"` — `_http_word_problem(args, spec_data,
     shape, http_ok)`: не `http_ok` → «`http` — шаг ходока (`walk_session.py step`); одиночный запрос вне прохода — `manual_capture.py
     http`»; `args[0].upper()` ∈ `http_methods`; `args[1]` начинается с `/` или `http://`/`https://`, без не-ASCII (дверь: «закодируйте путь
     процентами»); 3–4 слова — ровно `--body-file <файл>`. Все вызовы `parse_steps` в `walk_session.py` передают `http_ok=True`; `run_ui`
     и приложение — нет (слово там отказывается). Шаг исполняет актёр запроса (`actor_of(req)`), поля `as:` нет.
  7. **Где исполняется.** `request_problems` (до любого шага вызова): относительный путь разрешается от `self.stand["base_url"]` (нет
     `base_url` → отказ «стенд `<имя>` не записывает base_url; дайте полный URL на <хосты>»); хост вне `self.hosts` → отказ J-C1 с
     хостами; `--body-file` читается (нечитаемый → отказ); тело с `GENERATED_*` → отказ (проход учёток не создаёт); совпадение
     `secret_content_patterns` → отказ. `_run_step` ветвь `word == "http"` → `_run_http_word(backend, attempt, step, timeout_s, cfg,
     spec_data, account)`: `client = _BackendHttp(backend)`, `hosts = backend.allowed_hosts` (нет — отказ, никогда не слать на
     непроверенный хост), `hide = [учётка актёра]` если есть; `http_call(..., phase="supporting", proves=["request and response"])`;
     затем `_http_surprises`; ответ шага несёт путь документа в `captures` (существующее поле ответа) и `last_excerpt` — первые 300
     символов тела ответа из УЖЕ СОХРАНЁННОГО (вычищенного, проверенного) документа; отказ сохранения — выдержки нет.
  8. **Режим входа (по проходу).** Проход с экраном: HTTP-шаг идёт контекстом браузера актёра (`_BackendHttp(self.backends[actor])` →
     `PlaywrightBackend.http`, cookies сессии, семантика `--session`): что выполнил `fill-account` на этой странице, то и несёт запрос;
     гость без входа — без входа; Bearer-входа фабрики нет. Проход без экрана: `Walk._open_actor` строит `HttpOnlyBackend(client=MC.HTTP
     or UrllibHttp(), hosts=self.hosts)` — `.http()` = `client.request` + `Authorization: Bearer <токен>`, если токен есть и заголовка нет;
     `.close()`; `allowed_hosts`. Для актёра ≠ `guest`: `read_login(cfg, root, actor=actor, stand=self.stand, task_root)` →
     `_http_login(client, self.stand, login, spec, cfg, timeout_s, root)` один раз при открытии; токен только в памяти. Нет учётки
     (`read_login` — ValueError) или нет известного HTTP-входа (`http_login_source` — `EnvBlocked`: `harness_command`, `bearer_env`,
     `oidc_password`, неизвестный вид) или вход не дал токена → проход ОТКРЫВАЕТСЯ, сессия актёра в записи `signed_in: false, note:
     <текст двери>`, каждый HTTP-шаг этого актёра — исход `failed` с деталью «http_sign_in_unknown: <актёр>: <дверь>» до отправки;
     раннер пишет требование, которому нужен вход, `unreachable`, `blocked_by: access`, текст двери в `why`, без вопроса (P5, D-0043).
  9. **Поверхность прохода (`Walk._start`, место `survey`).** Сначала `capture_profile(cfg, task_root, item0, "ui")` — как сегодня для
     прохода кейса (проект с одним профилем ходит с экраном, как сегодня); `profile_several` → отказ `profile_not_chosen`; `profile_none`
     → `capture_profile(..., "http")`: удался — проход БЕЗ браузера, `profiles: {http: id}`, `stand_probe(..., "start", "http", stand)`;
     тоже `profile_none` → отказ (exit 2) «нет ни UI, ни HTTP-профиля» до любого захвата (FL-5 пишет `null: no_reachable_surface`).
     Проход с экраном может делать и HTTP-шаги (`profiles: {ui: id}`); HTTP-шаг пробы не добавляет: пробы попытки — пробы профиля
     прохода, идентичность стенда попытки не меняется (инвариант `choose_attempt_for` сохранён). Экранное слово в проходе без экрана —
     отказ вызова целиком (exit 2) «у этого прохода нет экрана; шаги — `http`». Для мест `case`/`settle`/`control` выбор не меняется.
  10. **`surprise:` HTTP-шага** — тот же писатель `Attempt.surprise` (рядом с `_surprises_after`, без нового вида): `_http_surprises(attempt,
     step_no, result, hosts, spec_data)` пишет `status` (с числом) на 3xx (факт «redirect to <путь>»), 4xx, 5xx; `blocked_host` на 3xx с
     `Location` вне `hosts` (редирект не следуется — нативно у `UrllibHttp` и `PlaywrightBackend.http`); `text` при `content-type: json` и
     нечитаемом JSON; и строку `Attempt.detector(step_no, [], http_kinds)`. Таймаут и отказ транспорта — исход шага (`timeout`/`failed`),
     не `surprise`. Данные: `surprise.http_steps: ["http"]`, `surprise.http_kinds: ["status", "blocked_host", "text"]`. Правило остановки
     по умолчанию `status:500-599` читает число нативно.
  11. S6/S7-проходы получают HTTP-шаг тем же словом; проход, не делающий HTTP-шагов, байт в байт как сегодня.
- Тесты (`test_walk_http_step.py`, включая мини-батарею интерактивной поверхности): `run_http_calls_http_call_per_call`,
  `http_step_takes_no_stand_lease_inside_walk` (за проход — одна аренда `_hold_walk`, `_hold_stand` из шага не зовётся),
  `http_step_writes_capture_in_walk_attempt` (все шаги item — в одной попытке), `http_step_host_outside_stand_refused`,
  `http_step_relative_path_uses_stand_base_url`, `http_step_without_base_url_refused`, `http_word_outside_walk_refused`,
  `http_word_unknown_method_refused`, `http_word_missing_path_refused`, `http_word_body_flag_without_file_refused`,
  `http_word_non_ascii_path_refused`, `http_step_body_file_unreadable_refused`, `http_step_generated_placeholder_refused`,
  `http_step_secret_in_request_refused`, `http_redirect_is_status_surprise_and_not_followed`, `http_redirect_to_foreign_host_blocked_host`,
  `http_4xx_5xx_status_surprise`, `http_body_at_cap_whole`, `http_body_beyond_cap_cut_with_cut_words`, `http_binary_body_base64`,
  `http_empty_body`, `http_broken_json_text_surprise`, `http_secrets_redacted_and_account_hidden`,
  `http_secret_in_response_not_saved_no_excerpt`, `http_timeout_is_step_outcome_not_surprise`, `http_excerpt_from_saved_document`,
  `capture_cited_accepts_http_capture`, `http_only_walk_opens_without_browser`, `http_only_actor_bearer_login_once`,
  `http_only_unknown_sign_in_opens_walk_and_fails_steps`, `ui_step_in_http_only_walk_refused`, `no_surface_open_refused`,
  `walk_with_ui_and_http_steps_shares_attempt_probes`, `s6_walk_without_http_unchanged`.
- Края: ИНВАРИАНТЫ — запрос на хост вне стенда прохода невозможен (две проверки: `request_problems` и `http_call`); секрет не попадает в
  улику (порядок `_side`/`redact` → `_hide` → `secret_pattern_hit` → сохранение → выдержка); внутри прохода аренда одна; шаги одного item —
  одна попытка; второго правила усечения и кодировки нет; S6/S7 без HTTP-шагов идут ровно как сегодня; `run_http` выводит то же.
- Свидетель: `python -B scripts/tests/test_walk_http_step.py`, `python -B scripts/tests/test_manual_capture_session.py`; CI:
  `test_manual_capture.py`, `test_walk_road.py`, `test_walk_lanes_parallel.py`.
- AR-1, AR-4, AR-6, AR-11, AR-13, AR-15, AR-19. Census: `parse_steps` (shape) и `request_problems` (xref) — существующие единицы, класс не
  меняется; `http_call`, `_run_http_word`, `_http_word_problem`, `_http_surprises` — имена вне `UNIT_NAME_RE`, места отказа в реестр не
  вносятся; подъём 0 (§4.7); сканер увидит новую единицу — стоп.

**FL-2 — запись первого взгляда: данные, попытка, писатель, один читатель, доля, «пора ли»** (builder → critic)
- Пишет: `references/first-look-statuses.json` (новый: `statuses: [confirms, contradicts, missing, unreachable]`, `blocked_by: [product,
  access, nature]`, `reachable: [confirms, contradicts]`, `null_reasons: [no_code_yet, empty_register, register_unreadable, no_stand,
  no_reachable_surface, profile_not_chosen, walk_not_opened]`, `open_retry_max: 1`); `references/artifact-contract-first-look.md` (новый; в
  `inject-map.json` не вносится — роль получает путь в брифе FL-3, AR-8); `scripts/first_look.py` (новый); `references/null-outcomes.json`;
  `references/config-keys.json` и `references/templates/config.json` (`first_look.reachable_floor_percent`, умолч. 30, целое 0–100);
  `references/role-commands.json` (`first_look.py put/show` для `qa-runner`); `references/artifact-writers.json` (`work/first-look.yaml`,
  `state/first-look-attempt.json` — `first_look.py`); `design/state-exits.md` (запись: устаревшая → проход повторяется; попытка: новая
  голова/реестр → новая попытка); census (строка `first_look.put_problems`, xref с заметкой «shape + xref», owner data, roles
  `["qa-runner"]`; §4.7); срезы — только если `contract_slices.py --check` назовёт файл; `scripts/tests/test_first_look.py` (новый);
  changelog.
- Формы. `work/first-look.yaml`: `{walked_at, walk, stand, stand_build, source_head: {<repo_id>: <sha | "unmeasured: …">}, register_hash,
  sides_met?, null?, rows: [{req: R-n, status, blocked_by?, why, evidence: [путь], quote?, path: {url?, steps: [строки], locators: [{what,
  selector, seen: yes|no}], api: [{method, path, auth: none|account:<роль>|token, sample: {request: <выдержка>, status, response:
  <выдержка>}, seen: yes|no}], data: [..], roles: [..], stand_needs: [..]}}], gaps: [строки]}` (L1: API-маршруты несутся так же, как экраны
  и локаторы; `sample` — наблюдение, никогда не ожидание). `blocked_by` обязателен у `missing`/`unreachable`. `state/first-look-attempt.json`:
  `{dispatch, walk, env, source_head, register_hash, opened_at, outcome: walking|written|nothing_written|open_failed, open_failures}`.
- Голова источника (M12, N3): `source_head` — КАРТА по каждой записи реализации `work/context-manifest.json` через
  `handoff_check.implementation_entries`: ключ — id репозитория записи (имя, которое `grounding_table.commit_value(entry, name)` получает
  как `name`; ключ читается на шаге 0, расхождение — вопрос Lead), значение — `commit_value(entry, name)`: sha или `unmeasured: …`
  (тоже значение). `register_hash` — sha256 канонического JSON списка R-n с текстом. Обе пишет код.
- Функции:
  - `current_keys(task_root) -> (source_head_text, register_hash)` — ЕДИНСТВЕННЫЙ производитель ключей для `first_look_continue` (N2):
    `source_head_text = json.dumps(карта, sort_keys=True, separators=(",", ":"))`. Зовут FL-5, FL-6, скилл-путь `s3.md` (через `show
    --json`, поле `current_keys`) и `continued`.
  - `begin(task_root, dispatch, env)` пишет файл попытки (`walking`, `walk = dispatch`, текущие голова и хэш); `end(task_root, outcome)`
    (`open_failed` увеличивает `open_failures`). CLI `begin --task-root T --dispatch D --env E`, `end --task-root T --outcome O`; зовут драйвер
    и шаг скилл-пути (AR-19).
  - `put(task_root, file, null_reason="")`: без `null_reason` — J-C3 с `walk`/`stand` из попытки, цитаты через `capture_cited`; с ним —
    `{null, rows: [], gaps: [причина]}`. `walk`, `stand`, `source_head`, `register_hash`, `sides_met`, `stand_build` пишет код.
    `stand_build` (M14): `confirmed`, когда `stand_identity.task_confirmation(task_root, env, profile)` — строка вида `deployed` с
    ревизией, равной голове (одна запись реализации); иначе `not_established`. ЗАМЕЧЕНО (m-new-4): `task_confirmation` — слово человека о
    деплое, обычно на гейте A после S3, поэтому у первого взгляда почти всегда `not_established`, и строка в вопросе FL-5 будет почти
    всегда — так задумано (фича может отсутствовать из-за старой сборки, человек должен это видеть); строка короткая, частоту меряет FL-L1;
    чтение `runtime_probe` вместо слова человека — вне плана (носитель не установлен). Непустая запись ставит попытке `written`. CLI `put
    --file F` | `put --null <причина>`, `show [--json]` (`--json` несёт `current_keys`).
  - `read(task_root) -> {rows, gaps, null, stale, stand_build, source_head, register_hash, walk, problem}` — ЕДИНСТВЕННЫЙ читатель; `source_head`
    — карта записи (N3); `stale` при другом `source_head` (побайтно по значениям; `unmeasured` — значение) ИЛИ `register_hash`.
  - `share(task_root, cfg) -> {reachable, counted, share, floor, below, problem}`: `counted` без `access`, `nature` (J-7); `below` только
    при `counted > 0` и доле < порога; `null`/нечитаемая/устаревшая → `below: False` и `problem`.
  - `due(task_root, pipeline, cfg) -> (bool, null_reason, why)` — ЧИСТАЯ: ложь + `no_code_yet` при `parks_after_s5`; ложь +
    `empty_register`/`register_unreadable`; ложь + `no_stand` при пустом `pipeline.environment` или `environment_pending`; ложь без
    причины, когда попытка для текущих головы и хэша уже есть с исходом `walking`/`written`/`nothing_written` (оплаченный диспатч не
    повторяется, M8); попытка `open_failed` (роль не запускалась, денег нет) — истина, пока `open_failures ≤ open_retry_max` (m-new-3:
    одна повторная попытка открыть на той же голове; после второй неудачи — ложь, строка-пробел называет причину); иначе истина. Пустая
    запись попыткой не является и свежей не считается (M10).
  - `continued(task_root, pipeline) -> bool`: `pipeline.first_look_continue` (PC-6) несёт `source_head`/`register_hash`, равные
    `current_keys(task_root)`.
- Тесты: `put_refuses_word_outside_data`, `put_needs_one_row_per_register_req`, `put_refuses_req_outside_register`,
  `put_needs_capture_except_nature`, `put_refuses_capture_of_other_walk`, `put_accepts_http_capture` (фикстура HTTP-строки `captures.jsonl`;
  часть B не нужна), `put_ignores_role_sent_head_and_walk`, `put_null_needs_known_reason`, `put_null_has_empty_rows_and_gap`,
  `api_route_row_shape`, `read_is_stale_on_other_head`, `read_returns_source_head_map`, `stale_on_register_change`,
  `share_excludes_access_and_nature`, `share_zero_counted_never_below`, `share_unreadable_never_below`, `share_stale_never_below`,
  `share_null_never_below`, `floor_default_30`, `floor_from_config`, `due_false_when_parks_after_s5`, `due_false_on_empty_register`,
  `due_false_without_stand`, `due_false_when_attempt_on_same_head`, `due_true_on_new_head_after_attempt`, `due_retries_open_failed_once`,
  `null_record_not_fresh_when_stand_appears`, `due_writes_nothing`, `stand_build_confirmed_only_on_deployed_same_revision`,
  `current_keys_canonical_and_stable`, `continued_only_on_same_head_and_register`, `sides_met_only_on_non_real_story`;
  `test_null_outcomes.py`, `test_state_exits.py`.
- Края и инварианты: пустой реестр → `null: empty_register`, вопроса нет (пустое — объявленный исход); нечитаемый реестр →
  `null: register_unreadable` (FR-59); R-n, добавленное после прохода, — запись устарела (отсутствие строки никогда не `confirms`).
  Запись — наблюдение, не оракул (FR-58). ВРЕМЕННОЙ край: до слияния FL-5 попытки не пишет никто — `put` без попытки отказывает «проход
  первого взгляда для этой стори не открыт; его открывает драйвер (`first_look.py begin`)». Текст `unmeasured` голов может меняться
  между запусками — тогда `continued` ложь и вопрос повторяется (допустимая ошибка: лишний вопрос).
- Свидетель: `python -B scripts/tests/test_first_look.py`, `test_null_outcomes.py`, `test_state_exits.py`, `python -B scripts/contract_slices.py
  --check`; CI: `test_judgment_census.py`.
- AR-1, AR-3, AR-13, AR-14, AR-21, AR-22, AR-23, AR-26, AR-28, AR-29. Зависит от FL-1 A, PC-6, PC-3 (`null-outcomes.json`), PC-1a.

**FL-3 — место в потоке, бриф и хартия прохода** (builder → critic)
- Пишет: `references/stages.json` (S3: необязательный диспатч `qa-runner` цели `first_look` ПЕРЕД окном 1; входы S3–S7 и брифов
  критика кейсов (S4) и критика кода (S5) += `work/first-look.yaml`); `scripts/brief_pack.py` (новая `first_look_runner_lines(task_root)`
  + вызов в `build` для цели `first_look`: walk id, стенд, профили (экран/HTTP), R-n с путём к тексту требований, команды
  `walk_session.py item/step/look/done` и шаг `http <METHOD> <path> [--body-file F]`, `first_look.py put`, путь
  `artifact-contract-first-look.md`, форма, подменённые стороны); `agents/qa-runner.md` (абзац «первый взгляд»: один путь на требование —
  экраном, а где у требования нет экрана — HTTP-шагом; без техник тест-дизайна; вход — учёткой стенда (экран — `fill-account`; без экрана —
  актёр `default`, если открыт); статус и `blocked_by` — своё суждение с уликой; недостижимое по входу — `access` с ролью, без вопроса;
  `nature` — только то, что не видно ни экраном, ни API в коротком проходе (фон, расписание); в карту пути — и экраны с локаторами, и
  API-маршруты с методом, путём, нужным входом и выдержкой; цитата — фрагмент сохранённого текста без кавычек и переводов строк;
  наблюдения, не ожидания; запись — `first_look.py put`); `scripts/tests/test_first_look_wiring.py` (новый); changelog.
- Тесты: `s3_has_optional_first_look_runner`, `first_look_yaml_is_input_of_s3_to_s7_and_critics`, `runner_charter_names_survey_http_and_put`,
  `first_look_brief_names_walk_env_profiles_items_and_put`, `first_look_brief_only_for_first_look_purpose`; `role_load.py --all` до/после
  (подъём — J-15).
- Края: нет записи или `null` — вход читает «первого взгляда не было» (AR-23). ИНВАРИАНТ: новой стадии нет; номера стадий не меняются;
  брифы других целей — ни байтом.
- Свидетель: `python -B scripts/tests/test_first_look_wiring.py`, `test_role_load.py`; CI: `test_brief_pack.py`.
- AR-8, AR-10, AR-11, AR-21. Зависит от FL-1 A, FL-2, PK0-2 (`build`), PC-5a (`qa-runner.md`); `stages.json` до PC-9b. Волна W3: все
  зависимости — в W2 и раньше (m-new-10).

**FL-4 — доход до потребителей (L2 (a), L3): брифы S3–S7 и двух критиков, карточка приложения, хартии стратега, автора кейсов, критика кейсов, S6** (builder → critic)
- Пишет: `scripts/brief_pack.py` (новая `first_look_lines(task_root, stage, role)`; по вызову в головах S3, S4, S4-критик, S5-критик
  кода, S6, S7 внутри `build`; бриф автора S5 получает строки через ту же функцию — вызов в голове S5; бриф критика кейсов S4 += строки
  перечня ролей тем же читателем, что PK0-2 (`project_knowledge.state` через `s3_roster_lines`), с маркером `[knowledge:product.roles]`;
  бриф критика плана S3 — только если в `stages.json` у S3 есть роль-рецензент; нет — строка отчёта билдера «у S3 нет критика плана»,
  стадия не изобретается); `scripts/app_card.py` (секция `First look` после `Entry routes`: адреса и шаги, локаторы с `seen`,
  API-маршруты, данные с меткой `seen:`, роли — через `first_look.read`; `SECTIONS` += `First look`; хэш карточки += `work/first-look.yaml`;
  пределы (m4): ≤ 20 R-n, ≤ 8 строк на R-n, строка ≤ 200 символов, дальше «+N: work/first-look.yaml»; при превышении `CARD_MAX_BYTES`
  секция сжимается до указателя РАНЬШЕ маршрутов); `agents/qa-test-strategist.md` (абзац: красное и недостижимое — улика для P28; роли — в
  `product_roles` своим суждением; не оракул); `agents/qa-case-designer.md` (абзац: шаги кейса берут пройденный путь — экран или API — и
  ссылаются на него `first_look:R-n`; отход от пройденного пути — со строкой причины; ожидание — только из требования);
  `agents/qa-case-critic.md` (абзацы: путь шагов, который расходится с пройденным без названной причины, — находка; «роли продукта и
  учётки, известные проекту, — правило проекта; кейс, который требует обратного знанию, — твоя находка, не требование к автору» (L3));
  `references/explore-charter.md` (абзац: ширину прошёл первый взгляд — S6 идёт в глубину, начиная с его наблюдений);
  `scripts/tests/test_first_look_briefs.py` (новый); `scripts/tests/test_app_card.py`.
- Строки брифа (≤ 12; дальше «+N: work/first-look.yaml»; каждая строка первого взгляда несёт маркер `[first-look:<R-n>]`): S3 — счёт по
  статусам, `contradicts`/`missing`/`unreachable` с R-n и `why`, подменённые стороны, «сборка стенда не установлена» при `not_established`;
  S4 (автор) — пройденные пути по R-n (экраны и API); S4 (критик кейсов) — путь записи, строка «шаги, расходящиеся с пройденным путём без
  причины, — находка» и перечень ролей; S5 (автор) — локаторы, API-маршруты и данные, увиденные проходом, с пометкой «раньше своей
  разведки» и правилом `placeholder_locator`/`tests[].provisional`; S5 (критик кода) — путь записи и строка «селектор или маршрут,
  переоткрытый или угаданный там, где первый взгляд его видел, — находка»; S6 — «ширину прошли; не повторяй»; S7 (M13) —
  `contradicts`/`missing`/`unreachable(product)` с R-n, `why`, уликой и текстом «реши, есть ли исполненная проверка; если нет — кандидат
  ли в баг (FR-22)». `path.data` и `sample` — только с префиксом `seen:`. Нет записи — «первого взгляда не было»; `null` — «… :
  <причина>»; нечитаема — строка с причиной.
- Тесты: `s3_lines_count_and_red_rows`, `s3_line_stand_build_not_established`, `s4_lines_paths_ui_and_api`, `s4_critic_lines_path_and_rule`,
  `s5_lines_locators_routes_data_before_discovery`, `s5_critic_lines_path_and_rule`, `s6_lines_width_walked`, `s7_lines_list_observations`,
  `no_record_one_line`, `null_record_reason_line`, `unreadable_record_line`, `cap_12_then_more`, `lines_never_carry_expected_value` (код:
  ни ключей `expected`/`then`/`should` из записи, каждое значение данных и выдержки — с `seen:`), `case_critic_brief_carries_roles_and_first_look`,
  `plan_critic_lines_only_when_s3_reviewer_exists`, `every_knowledge_line_carries_marker`; `test_app_card.py::first_look_section`,
  `::first_look_input_changes_hash`, `::first_look_section_bounded`, `::first_look_gives_way_before_routes`; `role_load.py --all` до/после
  (стратег, автор кейсов, критик кейсов, критик плана S3 — J-15).
- Края: ИНВАРИАНТ — ни одна строка не передаёт наблюдение или факт проекта как ожидаемое значение (FR-58, P20); маркеры — данные для
  счёта, не текст для роли; голова брифа не сокращается; код не отказывает роли за неиспользованную подсказку (AR-29).
- Свидетель: `python -B scripts/tests/test_first_look_briefs.py`, `test_app_card.py`, `test_role_load.py`; CI: `test_brief_pack.py`.
- AR-8, AR-10, AR-11, AR-13, AR-21, AR-27, AR-29. Зависит от FL-2, FL-3, PK0-2, PC-8 (`build`).

**FL-5 — драйвер: проход перед S3 и вопрос «фича не работает»** (builder → critic; горячий `story_run.py`)
- Пишет: `scripts/story_run.py` (`stage_S3` — один вызов в начале; новые `Driver.first_look_step`, `Driver._first_look_answer`);
  `scripts/exit_gate.py` (`_s3_window_one`: новейший S3-диспатч только среди `qa-test-strategist`, как `story_run.s3_window`);
  `references/question-prices.json` (`first_look.dead`); `skills/qa-story/phases/s3.md` (близнец: те же команды `first_look.py
  begin/put --null/end/show --json`, `walk_session.py open/close`, `controller.py --operation first_look_continue` с `current_keys`);
  `scripts/tests/fixtures/driver-layers.json` (строки `first_look_step`, `_first_look_answer`); `scripts/tests/test_first_look_step.py`
  (новый); `scripts/tests/test_human_reading.py`; changelog.
- Поведение `first_look_step` (ПОЗИЦИЯ: до `s3_prepare` и окна 1 текущего прохода S3; ИНВАРИАНТ: ни один диспатч стратега этого прохода
  не регистрируется раньше, чем первый взгляд решён — пройден, пропущен с причиной или отвечен):
  1. `due` ложь с причиной → `first_look.py put --null <причина>`, строка, S3 как сегодня. Ложь без причины → строка «на этой голове
     уже был: <исход>», дальше п. 4 по существующей записи или S3.
  2. Истина → регистрация диспатча `qa-runner` цели `first_look` (id = walk id); до старта роли (как `walk_before`): `first_look.py begin
     --dispatch <id> --env <pipeline.environment>`, затем `walk_session.py open --task-root T --walk <id> --place survey --env
     <pipeline.environment> --items <R-n через запятую> --actor guest` (+ `--actor default`, только когда проход будет без экрана и
     `read_login(cfg, root)` даёт учётку стенда по умолчанию — J-18; поверхность выбирает ходок, FL-1 B п. 9). `open` не удался: отказ
     «нет ни UI, ни HTTP-профиля» → `put --null no_reachable_surface`; отказ `capture_profile` → `profile_not_chosen`; иначе (exit 3,
     исключение) → `walk_not_opened`; во всех трёх — `end --outcome open_failed`, запись прохода удаляется, роль не запускается, вопроса
     нет, S3 как сегодня (FR-57); повтор открытия на той же голове — по `due` (одна повторная попытка, m-new-3).
  3. Роль закончила → `walk_session.py close`. Приёмка (J-3 (a)): диспатч закрыт обычным закрытием контроллера И `first_look.read` даёт
     свежую непустую запись этого walk. Иначе → `end --outcome nothing_written`, строка-пробел, S3; диспатч на этой голове не повторяется
     ни при одном повторном входе в `stage_S3` (окно 1, между окнами, окно 2, маршрут критика).
  4. `share`: `below` ложь → S3. `below` и `continued` → S3 (FR-7). Иначе `closed_question("first_look.dead", …)`: достижимые из учтённых,
     счёт по всем статусам, недостижимые с причинами, подменённые стороны, строка «сборка стенда не установлена: фича может отсутствовать
     только потому, что сборка старая» при `not_established` (M14; почти всегда — m-new-4).
  5. `continue` → `(H, R) = first_look.current_keys(task_root)`; `controller.py --operation first_look_continue --words-file <слова>
     --source-head H --register-hash R` (PC-6) → S3. `stop` → операция `await` с `cause: first_look_stop`, `held_from: S3`, пакет FL-6 (до
     него — пакет S5, инертно по J-11); печать, выход 0. Свободные слова → дирижёр.
- Цены `first_look.dead` (`human-questions.md`): `continue` — factory `command`, person `none`, delivery `no`; `stop` — factory `record`,
  person `none`, delivery `waits`.
- Стори без интерфейса (L1): проход идёт HTTP-шагами (FL-1 B); не идёт только при `no_reachable_surface` (ни UI, ни HTTP) — объявленный
  пустой исход с причиной по имени, вопроса нет.
- Тесты: `not_due_writes_null_and_runs_s3`, `walk_opened_with_survey_env_items_guest`, `http_only_walk_adds_default_actor_when_recorded`,
  `http_only_walk_guest_only_without_default`, `no_surface_writes_null_no_question`, `http_only_story_walks`,
  `walk_open_failure_writes_null_no_role`, `open_failed_retried_once_on_relaunch`, `nothing_written_not_redispatched_on_reentry`,
  `below_floor_asks_once`, `continued_on_same_head_not_reasked`, `continue_passes_current_keys_then_s3`,
  `stop_records_await_first_look_stop_held_from_s3`, `question_names_stand_build_not_established`, `call_sits_before_s3_prepare`; тест
  `exit_gate` (файл, который сегодня судит `_s3_window_one`) `s3_window_one_ignores_runner_dispatch`; `test_human_reading.py`; медленный
  `test_story_run_first_look.py` (CI) с `s3_closes_with_first_look_dispatch_present` (читатели S3-диспатчей контроллера не трассированы).
- Края: `stop` на `no_trace` — удержание только в состоянии стори. `continue` при новой голове или реестре — вопрос снова. ИНВАРИАНТЫ:
  стори не встаёт без слова человека; без записи поток как сегодня; оплаченный диспатч на одной голове — не больше одного.
- Свидетель: `python -B scripts/tests/test_first_look_step.py`, `test_human_reading.py`, тест `exit_gate`; CI: `test_story_run_first_look.py`, `test_driver_layers.py`.
- AR-11, AR-16, AR-17, AR-19, AR-24, AR-25, AR-28, AR-29. Зависит от FL-1 B, FL-2, FL-3, PC-6, PC-7, PC-2.

**FL-6 — стоянка, вопрос «код не изменился», своя ветвь прихода** (builder → critic; горячий `story_run.py`)
- Пишет: `scripts/story_run.py` (`arrival_step`, `_act_await_implementation`, `_act_awaiting_stopped` — ветви `first_look_stop`; новая
  `Driver.first_look_code_look`); `scripts/interim_packet.py` (`first_look_packet(task_root)`: счёт, недостижимые с уликами, голова и дата
  остановки, команда перезапуска); `references/question-prices.json` (`first_look.same_code`); `scripts/tests/fixtures/driver-layers.json`
  (строка `first_look_code_look`); `scripts/tests/test_human_reading.py`; `scripts/tests/test_first_look_code_look.py` (новый);
  `scripts/tests/test_interim_packet.py`; `test_story_run_arrival.py` (CI); changelog. Очереди: `question-prices.json`,
  `test_human_reading.py` — после FL-5, до PC-9c.
- Поведение:
  1. `_act_await_implementation` для `first_look_stop` пишет и печатает `first_look_packet`.
  2. ВЕТВЬ ПРИХОДА (B2) в `arrival_step` при `cause == first_look_stop` (флаг `--mr/--branch/--commit`; `--side <s>=real` ТОЛЬКО когда
     `contract.story_sides` не даёт этой стороне уже `real` (m-new-6; иначе флаг не триггер — п. 3); или сдвинувшаяся голова п. 3):
     (1) `implementation_source`, стороны (`stage_done.py --set`, `source: arrival`), событие `arrive` — удержание снято; (2) `rework --stage
     S1 --cause source_arrived`; (3) `rework --stage S2 --cause source_arrived` — сверка кода с реестром, одобренных кейсов нет, `affected`
     не читается; (4) обычный поток с S3: `first_look_step` видит устаревшую запись → проход снова → окна стратега. Шаги 4–5 t-2181 §3.2
     (доработка затронутых строк, `semantic_reopen`, S5 `bind`) НЕ выполняются. ИНВАРИАНТ ПОЗИЦИИ PC-7 не меняется: вопрос об изменённом
     тикете — первым, слово источника переживает вопрос, приход записан до любой доработки.
  3. Перезапуск БЕЗ флага (J-9 (b), N3): `first_look_code_look` берёт карту `first_look.read()["source_head"]` и для КАЖДОГО репозитория
     карты узнаёт живую голову того же источника: MR — `vcs_evidence.collect(url_этого_репозитория, full=False)["revision"]`; ветка —
     `git ls-remote origin refs/heads/<ветка>` в checkout, который `Driver.repo_of_project` даёт этому репозиторию, с таймаутом
     `LS_REMOTE_SECONDS` (образец `s0_resolve_head`; сигнатура читается на шаге 0, помощник только для одного репозитория — стоп и вопрос
     Lead); коммит не сдвигается. Правило: (а) ХОТЬ ОДИН репозиторий сдвинулся (записанное и живое — sha, и они разные) ИЛИ в манифесте
     появилась запись реализации, которой нет в карте → п. 2 с прежним источником; (б) иначе, если у какого-то репозитория записанное или
     живое значение `unmeasured: …` или не установлено (сеть, checkout, таймаут), или записанный репозиторий больше не назван → вопрос
     `first_look.same_code` со строкой на каждый такой репозиторий «не удалось узнать, менялся ли код в <repo>: <почему>» (FR-59) —
     «неизвестно» никогда не читается «сдвинулась»; (в) иначе (все равны) → вопрос `first_look.same_code` без таких строк. Несколько
     репозиториев — каждый сравнивается, вопрос перечисляет их с головами.
  4. Вопрос `first_look.same_code` (текст: дата остановки, головы по репозиториям, счёт статусов; при повторе после `wait` — строка «<дата>
     вы выбрали ждать; код с тех пор не менялся», дата — из записи отвеченных закрытых вопросов стори, которую драйвер уже ведёт (читатель,
     по которому работает FR-7); не читается — вопрос без этой строки) (m-new-5):

     | ответ | исполнитель | factory | person | delivery |
     |---|---|---|---|---|
     | `wait` | перепечатать `first_look_packet`, выход 0; удержание стоит | `nothing` | `none` | `waits` |
     | `source` | напечатать команду перезапуска с `--mr/--branch/--commit`, выход 0; перезапуск с флагом — ветвь п. 2 | `command` | `your_work` | `waits` |
     | `continue` | ТА ЖЕ операция, что `continue` на `first_look.dead`: `(H, R) = first_look.current_keys`; `controller.py --operation first_look_continue --words-file … --source-head H --register-hash R` (PC-6) — снимает `first_look_stop`, пишет `first_look_continued`; затем поток с S3, где `continued` истина → `first_look.dead` не повторяется, тесты на ожидаемое, красные до починки (FL-7) | `command` | `none` | `no` |

     Свободные слова → дирижёр.
  5. Остановленная (`stop_waiting`) стори `first_look_stop`: без флага `_act_awaiting_stopped` печатает «эту стори остановили <дата>
     после первого взгляда, фича не работала: "<слова>"; ничего не запускается; чтобы проверить новый код — запустите с
     --mr/--branch/--commit», выход 0 (J-9 не применяется: ожидание закончил человек, t-2181 :476); с флагом — ветвь п. 2.
  6. `--side <s>=absent` при перезапуске: сторона записывается (PC-2), удержание не меняется; на следующем приходе `due` ложь
     (`no_code_yet`), стори идёт как S-a и после S5 встаёт с `s5_absent_side`. `--side <s>=real` — по п. 2.
- Тесты: `first_look_stop_packet_not_s5_packet`, `bare_relaunch_head_moved_arrives`, `bare_relaunch_head_same_asks_same_code`,
  `bare_relaunch_head_unknown_asks_with_unknown_line`, `recorded_head_unmeasured_asks_not_arrives`, `multi_repo_one_moved_arrives`,
  `multi_repo_compares_each_named_repo`, `multi_repo_unknown_lists_each_repo`, `new_implementation_entry_arrives`,
  `same_code_wait_reprints_and_holds`, `same_code_after_wait_carries_date_line`, `same_code_source_prints_command`,
  `same_code_continue_uses_first_look_continue_operation_with_current_keys`, `arrival_after_first_look_stop_goes_s1_s2_then_s3`,
  `no_bind_after_first_look_stop`, `no_affected_rows_rework_after_first_look_stop`, `ticket_question_still_first_on_first_look_arrival`,
  `stopped_first_look_story_prints_cause_line`, `side_absent_relaunch_keeps_hold`, `side_real_already_real_is_no_trigger`;
  `test_interim_packet.py::first_look_packet_lists_unreachable`; `test_human_reading.py`.
- Края: ИНВАРИАНТ — ни одна роль стадии ≥ S3 не запускается на стори `first_look_stop` до прихода или ответа «продолжить как есть»;
  доработка S0–S2 — внутри удержания; неизвестная голова не ведёт к приходу молча.
- Свидетель: `python -B scripts/tests/test_first_look_code_look.py`, `test_interim_packet.py`, `test_human_reading.py`; CI:
  `test_story_run_arrival.py`, `test_driver_layers.py`.
- AR-16, AR-17, AR-21, AR-24, AR-25, AR-28. Зависит от PC-7, FL-5, PC-6, FL-2.

**FL-7 — «продолжаем»: учёт помеченного локатора, красный вместо подмены; автоматор и критик кода пользуются записью** (builder → critic, критик обязателен)
- Пишет: `scripts/s5_precheck.py` (`check_sides`: J-C5, J-C6, J-C9); `scripts/ledger.py` (`plan_row_state`: J-C7 на позиции §1 J-C7 —
  сразу после ветви `failed:*`, перед `not_verified_flaky` (m-new-1)); `references/delivery-verdict-kinds.json` (`placeholder_open`,
  `not_verified:placeholder_open`); `references/provisional-kinds.json` (`on_real: first_look_only` у `placeholder_locator`, `never` у
  остальных; без поля — `never`); `references/artifact-contract-automation.md` (форма `assumed_from: first_look:<R-n>`; «на настоящей
  стороне — только учёт, правило заземления не меняется»; объявление `tests[].provisional` с направлением ошибки J-C9 (a));
  `references/slices/{qa-automator,qa-code-critic,qa-failure-analyst}/artifact-contract-automation.md` (те, что `--check` назовёт);
  `agents/qa-automator.md` (абзацы: (1) L2 — локаторы, API-маршруты и данные, увиденные первым взглядом, идут РАНЬШЕ своей разведки:
  сначала свериться с записью, живую разведку — только для того, чего запись не видела или что не сошлось; (2) учёт 2а — тест на
  отсутствующий элемент пишется, локатор из требования, строка учёта, объявление в `tests[].provisional`, тест ПАДАЕТ — не пропуск, не
  `blocked_by_env`, не передача человеку; красная строка называет требование (P16); после починки — сверка живым прогоном и `settled_*`;
  порядок подсказок §2 n); `agents/qa-code-critic.md` (абзацы: (1) L2 — селектор или маршрут, переоткрытый или угаданный там, где первый
  взгляд его видел, — находка того же класса, что «новый тест там, где можно было дополнить старый»; (2) тест с помеченным локатором
  падает на недостижимом, называет требование, и каждый тест, опирающийся на помеченный дом, объявил строку; объявление — учёт, не
  утверждение об опоре (m-new-2); (3) то же для сторон и учёток, известных проекту: требование, противоположное знанию проекта, — не
  находка к автору (L3)); `scripts/tests/test_first_look_provisional.py` (новый). Очередь хартий: PC-8 (W4) → FL-7 (W5).
- Тесты: `real_side_placeholder_with_first_look_basis_accepted`, `real_side_placeholder_without_basis_refused`,
  `real_side_side_substitute_refused`, `real_side_assumed_contract_refused`, `real_side_reference_value_refused`, `basis_row_confirms_refused`,
  `basis_missing_access_refused`, `basis_unreachable_access_refused`, `basis_nature_refused`, `basis_record_unreadable_refused`,
  `basis_record_stale_refused`, `kind_without_on_real_refused_on_real`, `c6a_skips_open_first_look_row`,
  `c6b_absent_stamp_real_only_when_reader_all_real`, `undeclared_test_on_dependent_then_refused`, `tests_provisional_unknown_p_refused`,
  `placeholder_test_not_excused_by_blocked_by_env`, `placeholder_test_not_excused_by_handing`, `placeholder_test_skipped_refused`,
  `placeholder_test_without_run_refused`, `then_in_dependents_is_placeholder_open_whatever_test`, `green_placeholder_test_never_proves`,
  `then_outside_dependents_proved_only_by_clean_binding`, `skipped_placeholder_test_is_placeholder_open`,
  `handed_placeholder_test_is_placeholder_open`, `flaky_placeholder_test_is_placeholder_open`, `red_stays_failed`,
  `settled_row_with_run_proves`, `placeholder_never_excuses_run`; `automator_charter_first_look_before_discovery`,
  `code_critic_charter_rediscovered_selector_is_finding` (ключи текста); `test_sides_ledger.py` — существующие зелёные; `role_load --all`
  (автоматор, критик кода — J-15).
- Края: ИНВАРИАНТЫ (решения 4 и 2а): подмен на настоящей стороне нет; правило заземления не меняется; строка учёта не освобождает от
  прогона (J-C9 закрывает `blocked_by_env`, передачу, пропуск, отсутствие прогона); зелёный на несверенной заглушке не доказывает ни
  одного Then (J-C7); красный остаётся `failed:*`; «допущение — не ожидаемое значение» сохраняется; код не отказывает автоматору за то,
  что тот не взял подсказку (это находка критика, AR-29). Остаток риска: тест, опирающийся на помеченный дом вне `dependents` без
  объявления, данными не виден — суждение критика кода.
- Свидетель: `python -B scripts/tests/test_first_look_provisional.py`, `test_s5_precheck_sides.py`, `test_sides_ledger.py`,
  `python -B scripts/contract_slices.py --check`; CI: `test_judgment_census.py`.
- AR-10, AR-15, AR-27, AR-28, AR-29. Census: внутри существующего `check_sides`, новых строк нет (§4.7: 0; новая единица — стоп). Зависит
  от FL-2, PC-3, PC-4, PC-5, PC-8.

**FL-8 — замеры цены и ИСПОЛЬЗОВАНИЯ (L2 (b), L3): `knowledge_use`, детекторы, карта** (builder → critic)
- Пишет: `scripts/report_facts.py` — счётчики на стори: цена диспатча первого взгляда по журналу стори (FR-24); доля достижимых; заданы
  ли оба вопроса и ответы; исход попытки; строки `placeholder_open` на сдаче; и ОДНА функция `report_facts.knowledge_use(task_root)`, её
  никто не дублирует (PK0-6 этот файл не пишет). Источники: запись первого взгляда и строки реестра `known`. По каждому знанию `{source:
  registry|first_look, key, reached, used, available_unused}`. **reached** — роль/бриф с маркером `[knowledge:…]`/`[first-look:…]`;
  носитель — файлы брифов диспатчей стори; брифы не хранятся на диске → `unmeasured: briefs are not kept`. **used**: для записи первого
  взгляда (u1) сколько локаторов `seen: yes` и API-маршрутов записи встречаются строкой в домах локаторов / API-клиентах тестов S5 (файлы
  `tests[]` манифеста и `provisional[].home`) — сравнение строк, без суждения; (u2) сколько кейсов S4 ссылаются на `first_look:R-n`;
  (u3) сколько живых проб автоматора в S5 касались элементов, которые запись уже видела (селектор пробы равен локатору `seen: yes`) —
  носитель: записи захватов/проб диспатчей S5; не хранит селектор пробы → `unmeasured: <почему>` (FR-41), не ноль; `product.roles` —
  известные роли, вошедшие в `product_roles` передачи S3; `credentials_by_role` — гейт A не спросил снова известную пару (стенд, роль),
  носитель — журнал закрытых вопросов стори; стороны — S0 не спросил «чья сторона» для известной. **Контр-метрика (2)** «известный факт не
  дошёл до решения» = `available_unused` + факты `known` без `reached`; (1) и (3) — J-16, J-17. Ретро: одна таблица «знания: дошло /
  использовано / не использовано» рядом со счётом вопросов; «ноль вопросов» печатается только вместе с контр-метриками; «запись не
  прочитана» (ноль по u1 и u2 при непустых `rows`) и «известный факт не дошёл» — строки находки, не отказ. `design/architecture.md`
  (носители AR-21/AR-23 — `work/first-look.yaml`, `state/first-look-attempt.json`; детектор AR-28 — `test_first_look_provisional.py`;
  AR-15 — `capture_cited`, `http_call`, `first_look_continue`, `knowledge_use`); `docs/SIBLING_MAP.md` (ось 5: близнецы драйвер/скилл
  первого взгляда; член «проход ходока» — места `case`/`settle`/`control`/`survey`; близнецы шаг экрана / HTTP-шаг);
  `scripts/tests/test_report_facts.py`.
- Шаг 0: прочитать носитель класса находок критиков (J-16) и хранение брифов (reached); исход «нет» — названный (`unmeasured`).
- Тесты: `first_look_cost_from_story_journal`, `first_look_share_and_answers_counted`, `first_look_attempt_outcome_counted`,
  `use_locators_and_routes_in_s5_homes_counted`, `use_s4_cases_citing_walked_path_counted`, `use_probes_on_seen_elements_counted_or_unmeasured`,
  `unread_record_is_finding_line`, `null_record_no_unread_finding`, `counts_never_refuse`, `knowledge_use_counts_registry_and_first_look_in_one_table`,
  `known_role_reached_strategist_and_case_critic`, `known_credential_not_reasked_counts_used`, `known_fact_not_reaching_decision_is_finding_line`,
  `briefs_not_kept_reads_unmeasured`, `zero_questions_printed_with_counter_metrics`; `python tools/architecture_index.py --check`.
- Края: ИНВАРИАНТ — счётчики ничего не блокируют и не судят качество использования (AR-29); неизвестное — `unmeasured`, не ноль (AR-28);
  использование читает только `knowledge_use` (AR-13).
- Свидетель: `python -B scripts/tests/test_report_facts.py`. AR-12, AR-13, AR-20, AR-27, AR-28, AR-29. Зависит от PC-10, FL-4, FL-7,
  PK0-2, PK0-4, PC-8.

**FL-L — живые доказательства первого взгляда** (Lead + стенд MyBooks): §4.6. FL-L3 сравнивает и таблицу `knowledge_use` в обоих
прогонах и несёт проверку, перенесённую из PK0-7 (N7): ретро второй стори показывает известную роль и учётку как `used` (гейт A не спросил).

---

## §4 Порядок и параллельные потоки (по J-1 (b) и J-14 (a))

### 4.1 Файлы сессии `thinking-roles` и соседних веток, ворота

Носители: строки узлов `plans/piles/thinking-roles/batch-3-parallelnost.md` и `batch-4-ostatki.md`; снимок
`docs/tasks/compact-snapshots/2026-11-10-0045-manual.md`; перемеры критиков t-2277 B.1 и t-2288 (`git diff --stat HEAD...<ветка>`,
`git merge-base --is-ancestor`, `git branch --contains`). Git дизайнер не запускала (нет оболочки); перед первым диспатчем каждой волны
Lead перемеряет ворота по git.

| файл | писатель сессии / соседней ветки | освобождается |
|---|---|---|
| `scripts/story_run.py` | TR3-10 C+D; TR4-10 A1; TR4-13, TR4-14; TR3-9 Q6 (очередь) | G1 + G2; дальше — разделение функций с TR4-13/TR4-14 (D-0048) |
| `walk_session.py`, `walk_pool.py`, `manual_capture.py`, `project_decisions.py`, `report_facts.py`, `manual-capture-steps.json`, `walk-charter.md`, `role-commands.json`, `role-load.json`, `agents/qa-runner.md` | TR3-10 C, D, D3a, D3c (и D8 — `walk_session.py`, `walk_pool.py`) | G1 |
| `scripts/gate_preflight.py` | TR3-10 D8 (t-2284, ветка `tr/tr3-10d8`, не входит в `tr/tr3-10d`): `Rehearsal._actors_of_manual_cases`, `Rehearsal._probe_actor` | G1 (N6) |
| `scripts/tests/fixtures/driver-layers.json` | TR3-10 D (+24 строки), TR4-10 A1 (+5) | строки дописываются; порядок §2 w (N4) |
| `design/state-exits.md` | TR3-10 C/D/D3a/D3c/D8 (+11), TR4-10 A1/TR4-13 (+1) | по условиям J-14 (a) (§4.2) |
| `scripts/tests/fixtures/judgment-census.json` | TR3-10 C, D, D3a, D3c, D8 (+1 каждая); `test-diet`, `td/15-1`, `td/15-3`, `td/15-4`, `td/15-6a` (+1 каждая); `tr/t2064-p3` (+2) | по условиям J-14 (a); строки очереди ниже |
| `window_files.py` | TR4-10 A1 | G2 (узлы плана не пишут) |
| `controller.py` | TR4-14 (`resolve_return`) | G3 |
| `guard_pre_tool.py` | TR3-5, TR3-14, TR3-16 | **G4 выполнено** |
| `probe_by_code.py`, `detectors.json`, `assertion_detectors.py` | цепочка t-2064 | узлы плана не пишут |

Свободны: `execution_request.py` (TR4-7 слит c58d2a2ca), `brief_pack.py`, `stand_lease.py`, `dispatch_liveness.py` (TR4-12 слит f1bfce0ea),
`contract.py`, `stage_done.py`, `side-realities.json`, `manifest_put.py`, `manifest_from_tests.py`, `null-outcomes.json`,
`artifact-contract-automation.md`, `install-paths.json`, `collect-sets.json`, `conductor-actions.json`, `project_knowledge.py` (перемер
t-2288 §4: ни одного коммита с 08.11 в неслитых ветках).

Ворота: **G1** — слиты TR3-10 C, D, D3a, D3c И D8 (N6; D8 включён, потому что пишет `gate_preflight.py` `_probe_actor`, нужный PK0-4, и
`walk_session.py`); **G2** — TR4-10 A1 (+t-2280); **G3** — TR4-14; **G4** — ВЫПОЛНЕНО: `tr/tr3-5`, `tr/tr3-14`, `tr/tr3-16` — предки HEAD
по перемеру t-2288 (`merge-base --is-ancestor`); чтением файла подтверждено частично: в `guard_pre_tool.py` на HEAD стоят метки TR3-14 и
TR3-16, метки TR3-5 нет (её отсутствие слияния не опровергает).

Строки очереди (передаются находкой Lead кучки `thinking-roles` при приёмке плана):
- `judgment-census.json`: `очередь: {TR3-10 C/D/D3a/D3c/D8, test-diet, td/15-1, td/15-3, td/15-4, td/15-6a, tr/t2064-p3} → PK0-1 → PC-4 →
  PK0-4 → PC-6 → FL-2 → PC-5a → FL-7 → PC-9b` — кто сливается вторым, сохраняет строки обеих сторон и пересчитывает каждое число `ratchet`
  как сумму одобренных подъёмов обеих сторон (88b39b3de — образец).
- `design/state-exits.md`: `очередь: {TR3-10, TR4-10 A1, TR4-13} → PC-3 → PC-6 → FL-2 → PK0-6` — строки обеих сторон.
- `driver-layers.json`: строки сессии первыми, затем PC-2 → PC-7 → FL-5 → FL-6.
- Невзятые пачки 1–2 `thinking-roles` (m10) пишут `contract.py` (TR1-11), `stage_done.py` (TR2-7), `manifest_put.py` (TR2-1),
  `manual_evidence.py` (TR1-5/6/8), `gate_preflight.py` (TR2-9), `conductor-actions.json` (TR2-2), `role-commands.json` (TR1-3),
  `walk_session.py` (TR1-2/6/7/10): кто возьмёт их позже, сливается после узла PK/PC/FL, владеющего файлом в §4.4, или называет
  непересекающиеся функции.

Сейчас без слота писателя: (1) повторный проход критика по диффу этой ревизии (части FL-1 B, PC-6, FL-2, FL-6, §4); (2) скаут — перемер
ссылок `путь:строка` t-2142 и t-2181 после G1+G2; (3) Lead — `piles.py take` трёх пачек (J-11); (4) PK0-10.

### 4.2 Узел → когда стартует

**J-14 (a) (решение владельца 11.11.2026, «разрешить»).** PK0-1 и PC-3 стартуют СЕЙЧАС, не дожидаясь слияний сессии. Условия (критик
t-2288 §4): (1) строки обеих сторон в `judgment-census.json` и `design/state-exits.md` сохраняются; (2) числа `ratchet` пересчитываются
как сумма одобренных подъёмов обеих сторон (§4.7); (3) после слияния ветки сессии — `test_state_exits.py` локально и
`test_judgment_census.py` в CI ветки; (4) критик узла — после этого слияния (D-0048). ВРЕМЕННОЙ край, оба мира: сессия слилась раньше —
узел перед своим слиянием сливает ветку эксперимента и выполняет (1)–(4); узел готов раньше сессии — он сливается как обычно, а строка
очереди §4.1 обязывает сливающуюся позже ветку сессии выполнить (1)–(2) у себя. Те же условия применяются к census и state-exits узлов,
которые ждут своих ворот по другим файлам (PK0-4, PC-6, FL-2, PC-5a, FL-7, PC-9b): по этим двум файлам они ворот сессии не ждут. Узлы,
пишущие сами файлы сессии (`story_run.py`, `walk_session.py`, `manual_capture.py`, `controller.py`, `gate_preflight.py`, `qa-runner.md`),
ждут своих ворот. Безопасность (a) подтверждена критиком t-2288 (вопрос 4).

| узел | стартует | ждёт |
|---|---|---|
| PC-1a | **сейчас** | — |
| PK0-10 | **сейчас** (не код) | — |
| PK0-1 | **сейчас** (J-14 (a)) | — |
| PC-3 | **сразу после слияния PC-1a** (J-14 (a)) | PC-1a |
| PK0-2 | после PK0-1 (подтягивается) | — |
| PK0-8 | после PK0-1 (подтягивается; G4 выполнено) | — |
| PC-4 | после PC-3 (подтягивается) | — |
| FL-1 A | после G1 | `walk_session.py` |
| PK0-4 | после PK0-1 и G1 | `gate_preflight.py` (`_probe_actor`) |
| PC-2 | после G1 + G2 и PC-1a | `story_run.py` |
| PK0-3, PK0-5 | после PK0-1 и G1 + G2 | `story_run.py` |
| PC-6 | после PC-1a и G3 | `controller.py` |
| FL-1 B | после слияния FL-1 A | — |
| PC-5a | после PC-4 и G1 | `qa-runner.md` |
| FL-2 | после FL-1 A, PC-6, PC-3 | — |
| PK0-9 | после PK0-4, PK0-5 | — |
| PC-7 | после PC-2, PC-4, PC-6 | — |
| PC-9a | после FL-1 A, PC-3 | — |
| FL-3 | после FL-2, PK0-2, PC-5a | — |
| PC-1b | после PK0-3, PK0-8, PC-2, PC-9a | — |
| PC-5 | после PC-5a | — |
| PK0-6 | после PK0-1..5, 8, 9 | — |
| PK0-7 | после PK0-6 (живое) | стенд |
| PC-8 | после PC-7, FL-3 | — |
| FL-5 | после FL-3, PC-7, FL-1 B | — |
| PC-10 | после PC-5, PC-7, PK0-6 | — |
| PC-9b | после PC-7, PC-5a, PC-9a, PC-6, FL-1 A, FL-2, FL-3 | — |
| FL-4 | после PC-8 | — |
| FL-6 | после FL-5 | — |
| FL-7 | после PC-5, PC-8, FL-2 | — |
| PC-9c | после PC-9a, PK0-9, FL-6 | — |
| FL-8 | после PC-10, FL-4, FL-7, PK0-2, PK0-4, PC-8 | — |

### 4.3 Волны (барьерные: волна N+1 стартует, когда слиты ВСЕ узлы волны N; ≤ 6 пишущих код билдеров одновременно; дизайнеры, критики, скауты, PK0-10 — вне счёта)

Правило подтягивания: узел следующей волны стартует раньше барьера, только если (1) все зависимости слиты, (2) он не пишет файл узла
в работе (кроме `story_run.py`/`gate_preflight.py` с функциями из §4.4 и census/state-exits/`driver-layers.json` с порядком §4.4),
(3) пишущих ≤ 6. Внутри волны узел с зависимостью от узла той же волны стартует после его слияния (это сокращает одновременность, не
счёт волны).

| волна | узлы | пишущих одновременно | ворота |
|---|---|---|---|
| W0 | PC-1a, PK0-1 (сейчас); PC-3 (после PC-1a), PK0-2, PK0-8 (после PK0-1), PC-4 (после PC-3) (+ PK0-10) | ≤ 4 | — |
| W1 | FL-1 A, PK0-4, PC-2, PK0-3, PK0-5, PC-6 | 6 | G1; PC-2, PK0-3, PK0-5 ещё G2; PC-6 — G3 (иначе подтягивается в W2) |
| W2 | FL-1 B, FL-2, PC-5a, PK0-9, PC-7, PC-9a | 6 | — |
| W3 | PK0-6, FL-3, PC-5, PC-1b | 4 | — |
| W4 | PC-8, FL-5, PC-10 | 3 | — |
| W5 | FL-4, FL-6, FL-7, PC-9b, PC-9a (2-й коммит) | 5 | — |
| W6 | PC-9c, FL-8 | 2 | — |

### 4.4 Общие файлы в каждой волне

«Порядок» = поздний узел перед своим слиянием сливает ветку эксперимента с уже слитым ранним и решает конфликт строк сам (D-0048), его
критик — после этого слияния; для census — с пересчётом сумм (§4.7). Файл, который в волне пишет один узел, — «один».

| волна | файл | узлы | как разведены |
|---|---|---|---|
| W0 | `contract.py` | PC-1a, PC-3 | порядок PC-1a → PC-3 (PC-3 стартует после слияния PC-1a) |
| W0 | `judgment-census.json` | PK0-1, PC-4 | порядок PK0-1 → PC-4 |
| W0 | `design/state-exits.md`, `manifest_put.py`, `null-outcomes.json`, `artifact-contract-automation.md` + его срезы | PC-3 | один |
| W0 | `project_knowledge.py`, `conductor-actions.json`, `install-paths.json`, `collect-sets.json` | PK0-1 | один |
| W0 | `brief_pack.py`, `qa-test-strategist.md` | PK0-2 | один |
| W0 | `guard_pre_tool.py` | PK0-8 | один |
| W0 | `s5_precheck.py`, `run_suite.py`, `acceptance.py`, `window_record.py`, `check_witness.py` | PC-4 | один |
| W0 | `stage_done.py`, `side-realities.json` | PC-1a | один |
| W1 | `story_run.py` | PC-2, PK0-3, PK0-5 | функции: PC-2 `s0_note_launch`, `s0_keep_late_launch`, `launch_flags`, `s0_no_change_entry`, ветвь `s1.no_diff`, argparse, `Driver.s0_write_sides`, `Driver._keep_sides_answer`; PK0-3 `Driver.gate_repair`; PK0-5 `Driver.stand_login_problem` |
| W1 | `gate_preflight.py` | PK0-4, PK0-5 | функции: PK0-4 `check_role_accounts`, `role_gap_id`, `Rehearsal.__init__`, `gap_name`, `check_case_preconditions`, `_probe_actor`, `run`; PK0-5 `default_login_needed`, `check_s5_credentials` |
| W1 | `judgment-census.json` | PK0-4, PC-6 | порядок PK0-4 → PC-6 |
| W1 | `design/state-exits.md`, `controller.py`, `stage_guard.py`, `archive_task.py` | PC-6 | один |
| W1 | `driver-layers.json`, `question-prices.json`, `test_human_reading.py`, `s1.md`, `qa-scout.md` | PC-2 | один |
| W1 | `project_knowledge.py`, `handoffs/s3-strategist-to-designer.yaml` | PK0-3 | один |
| W1 | `walk_session.py`, `artifact-writers.json` | FL-1 A | один |
| W1 | `stand_gaps.py`, `gate_brief.py` | PK0-4 | один |
| W2 | `story_run.py` | PK0-9, PC-7 | функции: PK0-9 `Driver.revoke_environment_properties`; PC-7 `run`, `arrival_step`, `_act_await_implementation`, `_act_awaiting_stopped`, `dispatch_action`, `until_reached` |
| W2 | `judgment-census.json` | FL-2, PC-5a | порядок FL-2 → PC-5a |
| W2 | `walk_session.py`, `manual_capture.py`, `manual-capture-steps.json` | FL-1 B | один |
| W2 | `null-outcomes.json`, `artifact-writers.json`, `role-commands.json`, `design/state-exits.md`, `config-keys.json`, `templates/config.json` | FL-2 | один |
| W2 | `run_suite.py`, `manual_evidence.py`, `finalize_task.py`, `artifact-contract-run.md` + его срезы, `qa-runner.md` | PC-5a | один |
| W2 | `contract.py`, `vocabularies.md` + его срезы, `reference_snapshot.py`, `artifact-contract-reference.md` | PC-9a | один |
| W2 | `driver-layers.json`, `question-prices.json`, `test_human_reading.py`, `interim_packet.py`, `s5.md`, `audit_factory.py` | PC-7 | один |
| W2 | `gate_preflight.py`, `stand_gaps.py`, `gate_brief.py` | PK0-9 | один |
| W3 | `story_run.py`, `contract.py`, `project_knowledge.py`, `conductor-actions.json`, `guard_pre_tool.py` | PC-1b | один |
| W3 | `stages.json`, `brief_pack.py`, `qa-runner.md` | FL-3 | один |
| W3 | `design/state-exits.md`, `design/architecture.md`, `docs/SIBLING_MAP.md`, `docs/ARCHITECTURE_INDEX.md`, `s4.md`, `environments.md` | PK0-6 | один |
| W3 | `ledger.py`, `delivery-verdict-kinds.json`, `check_delivery.py`, `factory_dashboard.py` | PC-5 | один |
| W4 | `brief_pack.py`, `s2.md`, `s5.md`, `qa-automator.md`, `qa-code-critic.md`, `qa-requirements-tester.md` | PC-8 | один |
| W4 | `story_run.py`, `driver-layers.json`, `question-prices.json`, `test_human_reading.py`, `exit_gate.py`, `s3.md` | FL-5 | один |
| W4 | `report_facts.py`, `design/architecture.md`, `docs/SIBLING_MAP.md`, `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` | PC-10 | один |
| W5 | `story_run.py` | FL-6, PC-9b | функции: FL-6 `arrival_step`, `_act_await_implementation`, `_act_awaiting_stopped` (ветви `first_look_stop`), `Driver.first_look_code_look`; PC-9b `stage_simple` |
| W5 | `judgment-census.json` | FL-7, PC-9b | порядок FL-7 → PC-9b (FL-7 пишет, только если сканер увидит единицу) |
| W5 | `driver-layers.json`, `question-prices.json`, `test_human_reading.py`, `interim_packet.py` | FL-6 | один |
| W5 | `stages.json`, `role-commands.json`, `run_suite.py`, `execution_request.py`, `stand_identity.py`, `runtime_probe.py` | PC-9b | один |
| W5 | `brief_pack.py`, `app_card.py`, `qa-test-strategist.md`, `qa-case-designer.md`, `qa-case-critic.md`, `explore-charter.md` | FL-4 | один |
| W5 | `s5_precheck.py`, `ledger.py`, `delivery-verdict-kinds.json`, `provisional-kinds.json`, `artifact-contract-automation.md` + его срезы, `qa-automator.md`, `qa-code-critic.md` | FL-7 | один |
| W5 | `qa-requirements-tester.md` | PC-9a (2) | один |
| W6 | `gate_brief.py`, `test_human_reading.py` | PC-9c | один |
| W6 | `report_facts.py`, `design/architecture.md`, `docs/SIBLING_MAP.md` | FL-8 | один |

Сводка очередей: census — §4.1; state-exits — §4.1; `driver-layers.json` — сессия → PC-2 → PC-7 → FL-5 → FL-6; срезы
`artifact-contract-automation.md` — PC-3 → FL-7; `role-commands.json` — TR3-10 D → FL-2 → PC-9b; `null-outcomes.json` — PC-3 → FL-2;
`artifact-writers.json` — FL-1 A → FL-2; `question-prices.json` — PC-2 → PC-7 → FL-5 → FL-6; `test_human_reading.py` — PC-2 → PC-7 → FL-5 →
FL-6 → PC-9c; `stages.json` — FL-3 → PC-9b; `qa-runner.md` — TR3-10 → PC-5a → FL-3; `contract.py` — PC-1a → PC-3 → PC-9a → PC-1b;
`brief_pack.build` — TR4-12 → PK0-2 → FL-3 → PC-8 → FL-4; `project_knowledge.py` — PK0-1 → PK0-3 → PC-1b; `guard_pre_tool.py` — TR3-5/14/16
(слиты) → PK0-8 → PC-1b; `gate_preflight.py` — TR3-10 D8 → {PK0-4, PK0-5} → PK0-9; `s5.md` — PC-7 → PC-8; `interim_packet.py` — PC-7 →
FL-6; `ledger.py` — PC-5 → FL-7; `s5_precheck.py` — PC-4 → FL-7; `run_suite.py` — PC-4 → PC-5a → PC-9b; `qa-automator.md`,
`qa-code-critic.md` — PC-8 → FL-7; `report_facts.py` — TR3-10 → PC-10 → FL-8 (m-new-7); `architecture.md`/`SIBLING_MAP.md` — PK0-6 → PC-10
→ FL-8; `controller.py` — TR4-14 → PC-6; `walk_session.py` — TR3-10 → FL-1 A → FL-1 B; `manual_capture.py`, `manual-capture-steps.json` —
TR3-10 → FL-1 B; `story_run.py` — G1 + G2, затем по волнам (PC-2, PK0-3, PK0-5, PK0-9, PC-7, PC-1b, FL-5, FL-6, PC-9b). `hooklib.py`,
`install_smoke.py` — никто (если `install_smoke` потребует строку для `first_look.py`, `interim_packet.py`, `reference_snapshot.py` — стоп и
вопрос Lead).

### 4.5 Схождение, критик, канон

- У каждого узла один проход критика (у FL-1 — по одному на часть); слияния D-0048 и J-14 (a) — критик после слияния у позднего узла;
  повторный — только по диффу исправления.
- Точки схождения: после W2 — реестр + удержание + приход + ходок (BATCH CANON на CI); после W3 — `project-knowledge/1` целиком (живое
  PK0-7); после W4 — срез 1 `pre-code/1` (живые S-a, S-b); после W5 — всё, кроме PC-9c/FL-8 (FL-L1, FL-L2, FL-L4); после W6 — финальный
  канон (S-c, FL-L3). Канон — пайплайн CI, локально не гоняется.

### 4.6 Живые доказательства (FR-33)

| цель | что | стенд | когда |
|---|---|---|---|
| знания | PK0-7: две стори подряд, вопрос об учётке роли один раз, «не роль» не переспрашивается (по журналу; t-2142 §8 без изменений) | MyBooks, не `no_trace` | после W3 |
| без кода | PC-L S-a: встаёт в ожидание с пакетом; фича на ветке; перезапуск `--branch` до вердикта; **хотя бы одна строка допущений закрыта без правки** | MyBooks | после W4 |
| подмена | PC-L S-b: UI с замоканным API, `after_checks`, перепроход на настоящем бэкенде зелёный | MyBooks | после W4 |
| как раньше | PC-L S-c: старый тег вторым стендом, гейт A только расхождения и пробелы; образец — местом `survey` с `--env` | MyBooks + второй деплой (F-13) | после W6 |
| первый взгляд | FL-L1: сломанная на ветке фича → < 30 % → вопрос → `stop`; перезапуск без флага на той же голове → `first_look.same_code` → `wait`; повторный перезапуск без флага → вопрос со строкой даты `wait`; починка в ту же ветку; перезапуск без флага → S1/S2 → первый взгляд снова → S3 (без `bind`); частота строки `stand_build` | MyBooks | после W5 |
| первый взгляд | FL-L2: `continue` → тест с `placeholder_locator`/`first_look:R-n`, объявленный в `tests[].provisional`, красный → S7 `APP_BUG` | MyBooks | после W5 |
| первый взгляд | FL-L4 (L1): стори с требованием только по API — проход HTTP-шагами (без браузера), строки с API-маршрутами и уликами, без ложного вопроса | MyBooks | после W5 |
| первый взгляд | FL-L3: цена и польза — `stage_compare.py` на одной стори с проходом и без (S3–S6) + счётчики FL-8 (u1–u3) и таблица `knowledge_use` в обоих прогонах; ретро второй стори PK0-7 показывает известную роль и учётку как `used` (N7); стадия оправдана, если S4–S6 дешевеют больше её цены (FR-51) и запись используется | MyBooks | после FL-L1 и W6 |

FL-L4 — строка живого доказательства внутри FL-L, не новый узел.

### 4.7 Подъёмы храповиков — одобрены Lead заранее (AR-20; N5)

Числа — дельты к основанию на момент слияния узла (основание HEAD: `safety` 51; `blocking_per_role`: qa-automator 164, qa-runner 132,
conductor 469, прочие роли — как в `ratchet`). Каждый узел называет в вердикте измеренную дельту; дельта меньше строки — законна (ценз
плотный: число записывается по факту); БОЛЬШЕ строки или в ключе, которого строка не называет, — стоп и вопрос Lead. При слиянии с
писателями §4.1 строки обеих сторон сохраняются, числа — сумма подъёмов обеих сторон (J-14 (a)). Единица блокирует, если в ней место
отказа `refusal_registry.sites` или файл на пути блокировки (`BLOCKING_ENTRY_FILES`: `exit_gate.py`, `stage_guard.py`, `guard_pre_tool.py`,
`inject_context.py`, `stage_done.py`, `validate_artifacts.py`, `s5_precheck.py`, `handoff_check.py`, `judge_form.py`; или детектор
`stages.json`).

| узел | единица (файл::функция) | класс | роли | блокирует? | одобренный подъём |
|---|---|---|---|---|---|
| PK0-1 | `project_knowledge::record_problems` | shape | conductor | нет (t-2142 R-1) | 0 |
| PK0-1 | `project_knowledge::_refuse_no_trace` | safety | conductor | нет | `safety` +1 (51→52; t-2142 R-1) |
| PK0-4 | `gate_preflight::check_role_accounts` | xref | conductor | нет | 0 |
| PC-4 | `s5_precheck::check_sides` | xref | qa-automator | да (файл пути) | `blocking_per_role.qa-automator` +1 |
| PC-4 | `acceptance.pending_instances`, `check_witness._all_pending`, `window_record` (C5, C14) | — | — | имена вне `UNIT_NAME_RE` | 0 (новая единица — стоп) |
| PC-5a | `manual_evidence::validate` (C11; существующая строка) | shape → xref (по `higher_class`) | conductor | без изменений | 0 |
| PC-6 | `stage_guard::rule_awaiting_code` (C13) | safety | 13 ролей (как у всех `rule_*` `stage_guard.py`) | да (файл пути) | `safety` +1; `blocking_per_role` +1 у каждой из 13 ролей |
| PC-6 | `controller::build_rework_request` (C12) | presence | conductor | если место отказа внесено в реестр | `blocking_per_role.conductor` ≤ +1 |
| PC-6 | `controller::apply(first_look_continue)` (J-C10) | presence | conductor | да (место отказа операции) | `blocking_per_role.conductor` +1 |
| FL-1 A, FL-1 B | `walk_session::request_problems`, `manual_capture::parse_steps` (существующие) | xref, shape (без изменений) | conductor | без изменений | 0 |
| FL-2 | `first_look::put_problems` (J-C3) | xref | qa-runner | только если место отказа в единице | `blocking_per_role.qa-runner` ≤ +1 |
| FL-7 | (внутри `check_sides`) | — | — | — | 0 |
| PC-9b | C8 в существующей единице `run_suite::run` / `execution_request::validate_request` (класс поднимается до safety по t-2181 C8) | safety | conductor | без изменений | `safety` +1 |
| PC-1a, PC-1b | C17 внутри `stage_done.coerce_value`/`parse_sets`; C16 внутри `record_problems` (класс shape не меняется); C15 в `Driver.s0_write_sides` (имя вне регулярки) | — | — | — | 0 |
| PC-2 | `scripts/tests/fixtures/driver-layers.json` | — | — | — | +2 строки (`s0_write_sides`, `_keep_sides_answer`) |
| PC-7 | `driver-layers.json` | — | — | — | +3 строки |
| FL-5 | `driver-layers.json` | — | — | — | +2 строки |
| FL-6 | `driver-layers.json` | — | — | — | +1 строка |

Итог по плану (от основания HEAD, без писателей §4.1): `safety` 51→54 (PK0-1, PC-6, PC-9b); `blocking_per_role.qa-automator` +2 (PC-4,
PC-6); `qa-runner` ≤ +2 (PC-6, FL-2); `conductor` ≤ +3 (PC-6 ×3); каждая прочая роль +1 (PC-6); `word-list`, `meaning-proxy`, `meaning`,
`breach`, `blocks_overrides` — 0. `role-load.json` — J-15.

---

## §5 Поправки к существующим спекам (сами спеки этим документом не правятся)

**t-2142:**
1. PK0-1: путь `design/state-exits.md`; строку пишет PK0-6 (тест её не проверяет); PK0-1 стартует сейчас (J-14 (a)), census — слиянием по
   условиям §4.2.
2. §2 «Keys»: список «To agree» t-2181 — PC-1b добавляет `product.sides`, `environments.sides`, `environments.reference_for` (`exact`,
   `_exact_form`), проверку значения в `record_problems` (класс `shape`), `subjects`, `side`; строки сторон — только `state: known`;
   `no_trace` — ответ в `pipeline.sides`.
3. PK0-8: слово `side` в `human_word_check` добавит PC-1b; очередь `guard_pre_tool.py` TR3-5/14/16 (слиты) → PK0-8 → PC-1b.
4. Очередь census: §4.1; одобренные подъёмы — §4.7 (R-1 t-2142 входит туда строкой PK0-1).
5. Очередь `brief_pack.py`: TR4-12 → PK0-2 → FL-3 → PC-8 → FL-4.
6. §4: «первый взгляд встретил роль или нужду в учётке» → реестр не пишется; роль — через `product_roles`; учётка — карточка PK0-4.
   ИНВАРИАНТ: наблюдение прохода не становится фактом проекта без человека.
7. §7 фаза 1/5: маршруты (экранные и API), тест-данные, требования к стенду из первого взгляда — история стори; кандидаты — по слову
   владельца (J-5).
8. PK0-6: ось 34 без изменений; принимает строку state-exits PK0-1; `report_facts.py` не пишет.
9. (L3) Факт `known` применяется перед действием; строки PK0-2 и PK0-4 несут маркер; тот же читатель `state()` отдаёт их критику кейсов
   (FL-4); использование считает `report_facts.knowledge_use` (FL-8), своего измерителя у пачки нет.
10. PK0-4 ждёт G1 (TR3-10 D8 пишет `_probe_actor`); PK0-7 — проверки §8 без изменений, проверка `used` — FL-L3.

**t-2181:**
1. K1: одно состояние, два условия входа (`s5_absent_side`, `first_look_stop`); `cause`, `held_from`; для `first_look_stop`
   `s5_dispatch: null`, `sides` от читателя.
2. C12, C13, §2.4 B3: «S6–S9» → «стадии ≥ `held_from`»; доработка до `held_from` — внутри удержания. §2.4: выход (4) — `first_look_continue`
   (только `first_look_stop`; аргументы `--words-file`, `--source-head`, `--register-hash` от вызывающего); строка
   `pipeline.first_look_continue` — запись, становится историей при новом первом взгляде.
3. §2.2: **правило заземления не меняется (решение 4).** Отдельное правило УЧЁТА (2а): `placeholder_locator` на настоящей стороне с
   `assumed_from: first_look:<R-n>` при свежей записи `missing`/`unreachable` и `blocked_by: product` — запись красного теста; C3 + J-C5;
   C6(a) не к открытой строке J-C5; C6(b) — только при всех сторонах `real` и без `sides_unknown`. НОВОЕ ПОЛЕ (B3, PC-3):
   `tests[].provisional: [P-n]`, писатель — автоматор через `manifest_put.py`, отсутствие = `[]`, читатель `contract.manifest_provisional`,
   объявление — J-C9 (FL-7), с направлением ошибки J-C9 (a). ИНВАРИАНТ: зелёный теста на несверенной заглушке не доказывает ни одного Then.
4. §2.3/§2.4: `not_verified:placeholder_open` (J-C7), позиция — после `sides_unknown`/`on_substitute` и после `failed:*`, перед
   `not_verified_flaky`, `partial`, `error`, `skipped:*`, передачей и `passed_green` (m-new-1); выход — зелёный прогон после сверки и `settled_*`.
5. §2.4 читатели печатают причину; `_act_awaiting_stopped` — строка по причине (FL-6).
6. §3.1: между шагами 3 и 4 — первый взгляд (FL-5), не при `parks_after_s5`.
7. §3.2: ветвь прихода `first_look_stop` (FL-6): шаги 1–3, затем поток с S3; шаги 4–5 не применяются. Без флага — сравнение голов по
   каждому репозиторию (J-9, N3): хоть один сдвинулся → приход; иначе неизвестное или равное → `first_look.same_code`. `--side <s>=real` —
   триггер, только если сторона ещё не `real`. Остановленная — печать и выход (:476). S-a на приходе — без первого взгляда (J-8).
8. §3.3: `reference_walk` — `walk_session.py open --place survey --env <образец> --walk <id>`; цитата — `capture_cited` с walk окна.
9. §3.4: ключи `first_look.dead`, `first_look.same_code`.
10. §4: строки `work/first-look.yaml`, `state/first-look-attempt.json`, `awaiting.cause`, `awaiting.held_from`, `pipeline.first_look_continue`,
    `tests[].provisional` (писатели и читатели — §1 AR-14, §3).
11. §5 E-T1: стори «всё настоящее» платит и диспатч первого взгляда (стенд, экран или API, реестр), не больше одного на голову; FL-L3 меряет.
12. §7: PC-1a, PC-2, PC-3, PC-4, PC-5, PC-5a, PC-6, PC-7, PC-8, PC-9a, PC-9b, PC-9c изменены как в §3.2; очереди — §4.4; census — §4.7
    (подъёмы C8, C13 и строк контроллера названы); `driver-layers.json` и срезы — в owns PC-2, PC-7, PC-3, PC-5a, PC-9a.
13. «To agree with the project-knowledge session»: передан этим документом.
14. (L3) Строки сторон PC-8 несут маркер при `source: registry` и даются брифу критика кода.

---

## §6 Развилки

| id | вопрос | варианты | рекомендация | чьё |
|---|---|---|---|---|
| J-1 | что ждёт конца сессии | (a) весь код; (b) узлы на файлах сессии | — решено (b), §6.1 | владелец |
| J-2 | где первый взгляд | (a) диспатч `qa-runner` в начале S3; (b) новая стадия | **(a)** | Lead |
| J-3 | кто проходит и принимает | (a) `qa-runner`, приёмка данных кодом, смысл — стратег и человек; (b) отдельная приёмка | **(a)** | Lead |
| J-4 | форма стоянки | (a) то же состояние с `cause`/`held_from`; (b) отдельное | **(a)** | Lead |
| J-5 | что становится постоянным | (a) ничего кодом; (b) новые `KEYS` | — решено (a) | владелец |
| J-6 | вердикт зелёного на несверенной заглушке | (a) `placeholder_open`; (b) `no` | — решено (a) | владелец |
| J-7 | знаменатель 30 % | (a) без `access`, `nature`; (b) все | — решено (a) | владелец |
| J-8 | первый взгляд на приходе S-a | (a) нет; (b) да | **(a)** | Lead |
| J-9 | изменения КОДА без флага | (a) только флаг; (b) драйвер сравнивает | — решено (b) с вопросом | владелец |
| J-10 | наблюдения → аналитик | (a) красный тест, кейс S6, строки брифа S7; (b) новая строка триажа | **(a)** | Lead |
| J-11 | выпуск | (a) один релиз; (b) раздельно | — решено (a) | владелец |
| J-12 | носитель FL | (a) этот документ; (b) спека | **(a)** | Lead |

### 6.1 Решения по развилкам — авторитетны

| id | решение | чьё |
|---|---|---|
| J-1 | **(b)**: конца сессии `thinking-roles` ждут только узлы на её файлах (`story_run.py`, `controller.py`, `execution_request.py`, `walk_session.py`, `manual_capture.py`, `project_decisions.py`, `report_facts.py`, `window_files.py`, `design/state-exits.md`, `brief_pack.py`, `stand_lease.py`, `guard_pre_tool.py` — список §4.1, перемерить перед диспатчем). Узел, не пишущий в эти файлы, стартует сразу по своим зависимостям. §4.1 «весь код ждёт» и предусловие W1 отменены: W1 распадается — PC-1a идёт сейчас; PK0-1 — сейчас, если его строку `design/state-exits.md` можно отложить до слияния TR4-10, иначе после него; FL-1 — после слияния TR3-10. Заменяет слово «разработку не начинаем, пока не закончит параллельная сессия» в обеих пачках | владелец, 10.11.2026 |
| J-7 | (a): знаменатель без `blocked_by: access` и `nature`; вопрос показывает счёт по всем статусам | владелец |
| J-9 | (b) с уточнением: драйвер сам сравнивает голову; сдвинулась — дорога прихода; **не сдвинулась — закрытый вопрос человеку** (с ценой; FL-6: ждать дальше / вот источник / продолжить как есть). Узел FL-6; ключ — в очередь `question-prices.json` после FL-5 | владелец |
| J-6 | (a): `not_verified:placeholder_open`, «готово после проверок человеком», пункт в «Left with you» | владелец |
| J-5 | (a): кодом в постоянные знания ничего; кандидаты — находкой | владелец |
| J-11 | (a): один общий релиз после схождения трёх пачек | владелец |
| J-2, J-3, J-4, J-8, J-10, J-12 | по рекомендации (a) | Lead, 10.11.2026 |
| L1 | **первый взгляд ходит и вызовами API — в этом релизе** («чтобы не возвращаться к этому вопросу, и в архитектуре не было костылей»): один ходок для UI и не-UI стори; HTTP-шаг — полноправный шаг ходока с тем же форматом улик, той же проверкой цитаты и теми же строками `surprise:`; карта пути несёт API-маршруты (метод, путь, нужный вход, выдержка данных) как экраны и локаторы. Узел — FL-1 часть B. Заменяет прежнее направление «для стори без UI первый взгляд не идёт» и развилку о проходе по API | владелец, 10.11.2026 |
| L2 | запись первого взгляда должна ДОХОДИТЬ до потребителей (стратег, автор кейсов, автоматор — бриф и хартия, S6, критик кейсов, критик кода) и её ИСПОЛЬЗОВАНИЕ меряется, не навязывается (FL-4, FL-7, FL-8, FL-L3); код не отказывает роли за неиспользованную подсказку | Lead по вопросу владельца, 10.11.2026 |
| L3 | знание о проекте и запись первого взгляда — ОДИН механизм «дошло и использовано»: факт применяется перед ДЕЙСТВИЕМ, а не только перед вопросом; ретро считает применённые и неиспользованные; критики получают те же знания, что авторы (критик, который не знает правила проекта, требует обратного); рядом со счётом вопросов — контр-метрики, чтобы «ноль вопросов» от выдумки не читался успехом. Код несёт и считает, никогда не отказывает роли за неиспользованное знание (P27, AR-29); неизвестное — `unmeasured`, не ноль (FR-41). Число узлов, волны и владельцы файлов не меняются: маркеры — PK0-2, PK0-4, PC-8, FL-4, каждый в своём файле; `knowledge_use` — только FL-8. Поздние пункты того же сравнения (условие словами, замена и конфликт ответов, оглавление под защитой от обрезки, шире живое доказательство) — вне этого плана: `plans/piles/project-knowledge/findings/20261111-chego-ne-hvataet-planu-znanij-po-vneshnemu-razboru.md` | владелец, 11.11.2026 («Да, так») |
| J-14 | **(a)** («разрешить»): PK0-1 и PC-3 стартуют СЕЙЧАС; перед своим слиянием узел сливает ветку эксперимента с уже слитыми узлами сессии и сам решает конфликт дописанных строк (`judgment-census.json`, `design/state-exits.md`; D-0048), его критик — после этого слияния; условия критика t-2288 и оба мира — §4.2; узлы, ждущие только PK0-1 или PC-3, подтягиваются (§4.3); узлы, пишущие сами файлы сессии, ждут своих ворот | владелец, 11.11.2026 |
| N1–N7 | направления повторного вердикта t-2288 (часть B FL-1 — извлечённая функция; аргументы `first_look_continue`; голова по репозиториям; owns `driver-layers.json` и срезов; таблица подъёмов §4.7; ворота G1 с D8, G4 выполнено; PK0-7 без проверки FL-8) | Lead, 11.11.2026 |

Как J-1 применено после перемера: строка state-exits PK0-1 отложена (к PK0-6); census PK0-1 больше не держит узел (J-14 (a)).

### 6.2 Развилки

| id | вопрос | варианты | рекомендация | чьё |
|---|---|---|---|---|
| J-13 | — | снята решением L1 (§6.1) | — | — |
| J-14 | — | решено (a), §6.1 | — | владелец |
| J-15 | бюджеты `role-load.json` для растущих хартий и брифов (qa-runner: PC-5a, FL-3; qa-test-strategist: PK0-2, FL-4; qa-case-designer: FL-4; qa-case-critic и критик плана S3 (если есть): FL-4; qa-automator: PC-8, FL-7; qa-code-critic: PC-8 (строки сторон), FL-7; qa-requirements-tester: PC-8, PC-9a) — храповик только вниз | (a) Lead одобряет подъём на измеренную дельту, названную в вердикте узла (AR-20); (b) узел укладывается в бюджет, заменяя старый текст; (c) стоп в узле | **(b), затем (a) поштучно** при приёмке узла | Lead, 11.11.2026 (расширена L3) |
| J-16 | контр-метрика (1) «ответ выдуман там, где был нужен вопрос или пробел»: носителя данных не найдено (не проверено, есть ли у находок критиков поле класса, которое читает код) | (a) слово данных `invented_not_asked` в словаре классов находок критиков кейсов и кода, FL-8 считает находки этого класса — только если поле класса уже есть (шаг 0 FL-8); (b) находка в `project-knowledge`, метрика печатается `unmeasured`. Код текст не судит | Lead: принято (a) при наличии поля, иначе (b) | Lead |
| J-17 | контр-метрика (3) «ответ для одной стори применён как правило проекта»: поля области ответа у записи не найдено (t-2142 §0 не читан) | (b): область ответа — часть темы «условие и замена» (узлы PK-A, PK-B пачки `project-knowledge/2`); до неё метрика печатается `unmeasured: answer scope is not recorded` | **(b)**; план исполним по (b) | владелец |
| J-18 | каким входом ходит первый взгляд БЕЗ экрана (до гейта A): HTTP-шаги актёра нужны с записанной учёткой | (a) гость + актёр `default`, только если учётка стенда по умолчанию записана (`read_login(cfg, root)`); требование, которому нужна роль, — `unreachable`/`access` с ролью; (b) ещё и первая записанная учётка роли (`credentials_by_role`) вместо `default`, когда его нет; (c) только гость | ~~(a)~~ — **решено владельцем 11.11.2026: первый взгляд (с экраном и без) ходит ЛЮБОЙ учёткой, которая у фабрики уже есть** («а если у фабрики уже есть доступ? Учётки уже записаны в файле фабрики или в файлах проекта; в том же MyBooks изначально известна учётка админа»). Источники по порядку: учётка стенда по умолчанию (`read_login`), учётки ролей реестра (`credentials_by_role`, строки `known`), учётки, записанные в конфиге и файлах проекта, которые читатель учёток уже умеет читать. Какой ролью идти по требованию — решает раннер (его суждение, P27), код только перечисляет ему доступные учётки по ролям в запросе прохода. `unreachable`/`access` с именем роли — ТОЛЬКО для роли, учётки которой нет ни в одном источнике; вопрос об учётке первый взгляд по-прежнему не задаёт. Узлы: FL-1 B (вход HTTP-шага — учётка названного актёра, не только `default`), FL-3 (хартия раннера: «пользуйся известными учётками ролей»), FL-5 (запрос прохода перечисляет доступные роли). Чтение учёток из файлов проекта — через существующего читателя; если он их не видит — шаг 0 FL-5 называет это находкой, новый читатель не строится | владелец |

---

## §7 Проверка полноты

**Счёт узлов.** `project-knowledge/1`: 9 узлов (PK0-1, 2, 3, 4, 5, 6, 8, 9, 10) + живое PK0-7 — в плане 9 + PK0-7. `pre-code/1`: 14 узлов
(PC-1a, 1b, 2, 3, 4, 5a, 5, 6, 7, 8, 9a, 9b, 9c, 10) + PC-L — в плане 14 + PC-L. `pre-code/2`: FL-0 (изменён: заменён узлами) + FL-1…FL-8
+ FL-L. Ревизия 4 узлов не добавила и не перенумеровала: FL-1 — один id с частями A и B; FL-L4 — строка внутри FL-L. Полнота `pre-code/2`
опирается на `plans/piles/pre-code/batch-2-pervyj-vzglyad.md`, в wt-fbfix не закоммиченный: коммитит сессия-владелец (m8).

| источник | пункт | узел |
|---|---|---|
| batch PK | PK0-1…6, 8, 9, 10 | те же id; изменены PK0-1, PK0-2, PK0-4, PK0-6, PK0-8, PK0-9 (пометка), PK0-10 |
| batch PK | живое / PK0-7 | PK0-7 (проверка `used` — FL-L3) |
| batch PC | PC-1a…10 | те же id; изменены PC-1a, PC-1b, PC-2, PC-3, PC-4, PC-5, PC-5a, PC-6, PC-7, PC-8, PC-9a, PC-9b, PC-9c |
| batch PC | живые S-a (вкл. «строка допущений закрыта без правки»), S-b, S-c | PC-L |
| batch FL | FL-0 | FL-1 (A, B)…FL-8, FL-L + критик на план |
| t-2142 владелец | FK-3 (a) | PK0-5 |
| t-2142 владелец | FK-4 | вне фазы 0 |
| t-2142 владелец | FK-6 (a) | PK0-4, PK0-3 |
| t-2142 владелец | В1–В8 | В8 — PK0-3, PK0-4; В1, В7 и В2–В6 — поздние фазы (сверено критиком); до фазы 3 первый взгляд берёт `pipeline.environment` (FL-5) |
| t-2142 владелец | «не начинаем, пока не закончит сессия» | заменено J-1 (b), J-14 (a); §4.1–§4.2 |
| t-2142 Lead | FK-1, 2, 5, 7…12, R-1, R-2 | PK0-1..9; R-1 — §4.7; R-2 — PK0-10 |
| t-2181 владелец | D1 | соблюдено |
| t-2181 владелец | D2 | PC-2, PC-5; §2 k |
| t-2181 владелец | D3 | PC-9c |
| t-2181 владелец | D4 / F-16 | J-11 (a) |
| t-2181 владелец | F-1 | PC-1b |
| t-2181 владелец | F-7 | PC-9c |
| t-2181 владелец | F-10 | PC-6, PC-7; годится и для `first_look_stop` |
| t-2181 владелец | F-11 | PC-5 |
| t-2181 владелец | F-12 | PC-2, PC-1b |
| t-2181 владелец | F-13 | PC-L S-c |
| t-2181 владелец | бессрочное ожидание | PC-6 |
| t-2181 Lead | F-2…F-6, F-8, F-9, F-14, F-15, F-17, F-18 | PC-узлы |
| находка | решение 1: между S2 и S3 | FL-3, FL-5 |
| находка | решение 2: один проход — четыре читателя | FL-4 (S3/S4/S5/S6 + S7 + два критика), FL-7 (хартия автоматора), FL-8 (замер использования, L2) |
| находка | решение 3: закрытый вопрос | FL-5, FL-6, PC-6, FL-7 |
| находка | решение 3: смотреть КОД | FL-6 (J-9, по репозиториям) |
| находка | решение 4: моками не заменяем, правило заземления НЕ расширяется | FL-7, §2 b, §5 t-2181 п. 3 |
| находка | решение 4: недостижимое — аналитику кандидатом (FR-22) | FL-4 (строки S7) + J-10 (a) |
| находка | решение 5: порог 30 % | FL-2, FL-5; J-7 |
| находка | решение 2а | FL-7, PC-3; J-6 |
| находка | развилка 3: зависимость от пачки 1 | §4.2 |
| находка | бриф: рекордер, улики кодом, `surprise:` | FL-1 (A и B), FL-3 |
| находка | бриф: тикет без интерфейса — вызовы API | FL-1 B (L1), FL-2 (`path.api`), FL-3, FL-5, FL-L4 |
| находка | бриф: нет стенда — пробел без вопроса | FL-2, FL-5 |
| находка | бриф: не оракул | FL-2, FL-4 (`lines_never_carry_expected_value`); J-10 |
| находка | бриф: суждение роли | FL-2/FL-5; J-3 |
| находка | бриф: цена — `stage_compare.py` | FL-L3, FL-8 |
| владелец | L3 «дошло и использовано» | PK0-2, PK0-4, PC-8, FL-4, FL-7 (маркеры, критики), FL-8 (`knowledge_use`), FL-L3 |
| README PK | вопросов нет | — |
| README PC | F-13 | PC-L S-c |
| README PC | приоритет П2 | не меняется |
| README PC | SS1-13 | PC-2 |

---

## Мелкие решения, закрытые мной (Lead может отменить)

Ревизия 1: имена `survey`, `work/first-look.yaml`, `first_look.py`, `first-look-statuses.json`, `artifact-contract-first-look.md`,
`first_look.reachable_floor_percent` (30), цель `first_look`, ключ `first_look.dead`, причины `s5_absent_side`/`first_look_stop`,
`held_from`, `assumed_from: first_look:<R-n>`, `not_verified:placeholder_open`, `capture_cited`, `first_look_packet`, `first_look_lines`,
секция `First look`, кап 12, тестовые файлы; S-b — проход идёт с `sides_met`.

Ревизия 2: `first_look.same_code` (`wait`/`source`/`continue`); `first_look_continue`, `first_look_continued`, `pipeline.first_look_continue`;
`state/first-look-attempt.json`, `first_look.py begin/end`, `put --null`; `null_reasons`; имя поля `tests[].provisional` (направление — Lead);
поля записи прохода `place`/`stand`/`profiles`/`attempts`; `first_look_runner_lines` в FL-3; фильтр роли в `exit_gate._s3_window_one`;
голова неизвестна → тот же вопрос со строкой; `stand_build` по `task_confirmation`; вход гостем + `fill-account`; `profile_not_chosen` без
флага; пределы секции карточки; барьерные волны; PC-9c в W6. L2: ссылка кейса `first_look:R-n`; счётчики u1–u3 и строка «запись не
прочитана»; FL-L4 как строка FL-L.

Ревизия 4: имя `http_call` и её сигнатура; `_run_http_word`, `_http_word_problem`, `_http_surprises`, класс `HttpOnlyBackend`, свойство
`allowed_hosts`; параметр `parse_steps(..., http_ok=False)`; форма шага `http <METHOD> <path|url> [--body-file <file>]`, арность [2, 4];
отказ не-ASCII пути (вместо кодирования); проверка URL HTTP-шага в `request_problems` и повторно в `http_call`; относительный путь — от
`stand["base_url"]`; выдержка тела — `last_excerpt` ответа шага из сохранённого документа (ключ `http_body_excerpt_bytes` и метки «truncated
N of M» / «non-UTF-8 replacement» ревизии 2 сняты: второе правило рядом с `cut_body`/`body_text`/`CUT_WORDS`); цитата ищется в сохранённом
документе (не в выдержке); виды `surprise:` HTTP — существующие `status`/`blocked_host`/`text`, таймаут — исход шага; выбор поверхности
`survey` через `capture_profile("ui")` → `profile_none` → `"http"`; HTTP-шаг пробы не добавляет; `source_head` — карта по id репозитория;
`first_look.current_keys` и канонический JSON-текст для `--source-head`; запись реализации, которой нет в карте, — «сдвинулась»; записанный
репозиторий, которого больше нет, — «не установить»; `open_retry_max: 1` (m-new-3); повторный вопрос после `wait` со строкой даты
(m-new-5) вместо перепечатки без вопроса (иначе `continue`/`source` недостижимы без новой двери); новые ссылки (`artifact-contract-first-look.md`,
`artifact-contract-reference.md`) в `inject-map.json` не вносятся; ворота D8 — внутри G1, а не отдельные; волны W0–W6 перестроены под
J-14 (a); FL-3 — в W3 (m-new-10); условия J-14 (a) применены к census/state-exits узлов, ждущих ворот по другим файлам (то же основание
безопасности, критик t-2288 §4 пункт 3).

## Чего я не прочитала или не установила

- Git сама не запускала (нет оболочки): ворота G1–G3 — по снимку и перемерам критиков; G4 — по перемеру t-2288 и частично по файлу (метки
  TR3-14, TR3-16 в `guard_pre_tool.py`; метки TR3-5 нет); войдёт ли D8 в `tr/tr3-10d` до G1 — не знаю; перемер — за Lead.
- Читатели S3-диспатчей контроллера не трассированы — CI-тест `s3_closes_with_first_look_dispatch_present`.
- Все ли двери передачи человеку после S5 читают `contract.handed_tests` — не проверено; J-C9 закрывает выход S5, J-C7 — любую стадию.
- Внесёт ли сканер census место отказа `first_look.put`/`put_problems`, `build_rework_request`, операции контроллера в единицы и
  поднимется ли класс существующей единицы при C8/C11 (`CLASS_ORDER`, `higher_class` прочитан только по имени) — строки §4.7 даны как
  верхние границы; сверх — стоп.
- Сигнатура `Driver.repo_of_project` (один или несколько репозиториев) и имя ключа репозитория в записи `implementation_entries` — шаг 0
  FL-2/FL-6.
- Носитель даты прежнего ответа `wait` (запись отвеченных закрытых вопросов, читатель FR-7) по коду не прочитан — FL-6 без него задаёт
  вопрос без строки даты.
- Есть ли маркеры `contract_slices` в новых ссылках, порождает ли `--write` срезы `index.md` от новых файлов — решает `--check` в узле.
- Носитель селектора живой пробы автоматора (счётчик u3) не найден — FL-8 печатает `unmeasured`, если его нет.
- Запас `role-load.json` не измерен (J-15).
- (L3) Хранятся ли брифы диспатчей на диске (носитель `reached`); есть ли у находок критиков поле класса (J-16); есть ли у ответов поле
  области (J-17); есть ли у S3 стадия критика плана. Каждое — шаг 0 соответствующего узла, с названным исходом «нет».
- Расхождение с брифом ревизии 4: бриф называет `references/driver-layers.json`, файл лежит в `scripts/tests/fixtures/driver-layers.json`
  (Glob) — план пишет фактический путь.

## Reading trail

Ревизия 1: файлы трёх пачек и находки, t-2181 целиком, t-2142 1–104/307–1115, снимки 1330/1610, t-1957 части, пакет частями.
Ревизия 2: отчёт критика целиком; план целиком; t-2181 286–385, 440–509, Grep; `artifact-contract-automation.md` Grep `then_bindings`;
снимок 0045 270–331; строки узлов `^\| TR[34]-` и TR4-10/11; пакет — `walk_session.py`, `manual_capture.py` 436–475, `story_run.py`
части, `exit_gate.py` 773–794, `source_preflight.py` 100–149, `vcs_evidence.py` 95–129, `grounding_table.py` 255–279, `stand_identity.py`
1–40, 499–511, `question-prices.json` 1–40, `test_state_exits.py` 40–79.
Ревизия 4: план 1–951 целиком; вердикт t-2288 целиком; пакет — `manual_capture.py` 400–479 (`choose_attempt_for`, `_fits_surface`,
`capture_profile`), 1191–1295 (`parse_steps`), 1340–1407 (`Attempt.surprise/detector/register/store_text/step`), 1440–1466 (`cut_body`,
`body_text`, `_side`, `CUT_WORDS`), 1625–1644 (`PlaywrightBackend.open`, `self._allowed`), 2190–2213 (`PlaywrightBackend.http`), 2781–2792
(`_session_login`), 3033–3054 (`_BackendHttp`, `_new_backend`), 4581–4620 (`_run_step`), 4884–5208 (`http_login_source`, `_http_login`,
`run_http`, `_run_http`), Grep определений (`BODY_CAP`, `environment_of`, `stand_hosts`, `secret_pattern_hit`, `redact`, `_hide`,
`_hold_stand`, `UrllibHttp`, `_surprises_after`); `walk_session.py` 296–309 (`request_problems` разбор), 466–495 (`_quote_home`), 720–1124
(`Walk`: `__init__`, `actor_of`, `write_state`, `_start`, `_open_actors`, `_open_actor`, `_shutdown`, `item_root`, `page_lease`, `_hold_walk`,
`_new_attempt`, `op_step`, `_with_pre_action`), Grep определений; `manual-capture-steps.json` 9–17 (`steps`), 60–99 (`surprise`,
`walk_session`, `http_methods`, `redact_headers`); `ledger.py` 460–543 (`plan_row_state` порядок ветвей), Grep возвратов;
`test_judgment_census.py` 61, 70–75, 202–271, 330–403 (C2, C3, `UNIT_NAME_RE`, `BLOCKING_ENTRY_FILES`, `effective_blocks`); census-фикстура
— строка 4 (`ratchet`), Grep строк `s5_precheck`, `stage_guard`, `controller`, `stage_done`, `run_suite`, `execution_request`, `contract`,
`parse_steps`, `request_problems`; `contract_slices.py` 1–40; Glob `references/slices/*/*.md`, `**/driver-layers.json`; `slow_tests.json`
Grep; `gate_preflight.py` Grep `_probe_actor`; `guard_pre_tool.py` Grep `TR3-(5|14|16)` (положительный контроль — найдены TR3-14, TR3-16);
t-2142 330–341, 1038–1045, Grep `census|_probe_actor`; t-2181 134–154, 776–832, Grep `PC-9b|census`. Положительный контроль Grep — в тех же
вызовах (каждый отрицательный вывод выше опирается на находку той же формы в том же файле).

Замеченное и не исправленное: `s0_resolve_head` смотрит голову только исключённых MR (для J-9 годится лишь его образец `git ls-remote`);
`implementation_source` — слово режима, не голова (M12); статусы `batch-4-ostatki.md` отстают от снимка (TR4-10); `test_driver_layers.py`
стоял свидетелем PC-1b/PC-2/PC-7, но он в `slow_tests.json` (40 с) — перенесён в CI.

---

## §9 Ответ на вердикты критика и дополнения Lead

Первый вердикт (t-2277):
- **B1** — закрыто: FL-6 п. 3–4 (`first_look.same_code`, три ответа, исполнители, цены, неизвестная голова — тот же вопрос со строкой);
  `continue` — операция PC-6 `first_look_continue`, общая с `first_look.dead` (FL-5 п. 5, J-C10); владение `question-prices.json`,
  `test_human_reading.py`; очередь FL-5 → FL-6 → PC-9c, PC-9c в W6. Дефект N2 закрыт ниже.
- **B2** — закрыто: FL-6 п. 2 — ветвь прихода `first_look_stop` (S1, S2, поток с S3; без шагов 4–5), инвариант PC-7, тесты; §2 c, §5 п. 7.
- **B3** — закрыто: одно поле `tests[].provisional`, писатель `manifest_put`, узел PC-3 (§5 п. 3); J-C7 переписан, J-C9 (a) — объявление;
  инвариант «ни один, ни вместе» записан.
- **M1** — закрыто: «правило заземления не меняется, строка — учёт (2а)» (§2 b, §5 п. 3, FL-7); J-C5: `blocked_by: product` для обоих
  статусов; вид без `on_real` → `never`.
- **M2** — закрыто: J-C9 (b)–(d); леджер — `skipped`/передача → `placeholder_open` (позиция — m-new-1). Прочие двери передачи после S5 в
  коде не проверены — сказано.
- **M3** — закрыто: `capture_cited(…, walk, …, stand)` по записи прохода (FL-1 A п. 3–4).
- **M4** — закрыто, с дефектом N6 (закрыт ниже).
- **M5** — закрыто: §4.2–§4.4 перестроены (ревизия 4: W0–W6 под J-14 (a); файлы N4 — в таблицах).
- **M6** — закрыто: строка state-exits PK0-1 → PK0-6; `provisional[]` — у PC-3; census перенести нельзя (C1) — теперь слиянием J-14 (a).
- **M7** — закрыто для части A (таблица `survey`); часть B переоткрыта N1 и закрыта ниже.
- **M8** — закрыто: FL-5 п. 1–3.
- **M9** — закрыто решением L1; строимость части B — N1.
- **M10** — закрыто: FL-2 `due` чистая; `put --null`; исключение J-C3; `stale` и по `register_hash`. Остаток m-new-3 закрыт ниже.
- **M11** — закрыто: строка AR-25; `s5_dispatch: null`, `sides`; `_act_awaiting_stopped` по причине; `--side <s>=absent`.
- **M12** — закрыто, с дефектом N3 (закрыт ниже).
- **M13** — закрыто: строки S7 FL-4, AR-27.
- **M14** — закрыто: `stand_build`; остаток m-new-4 отвечен ниже.
- **m1** — закрыто (§4.6 S-a). **m2** — закрыто (пометки PK0-9, PK0-10). **m3** — закрыто (FL-1 A «Профиль»). **m4** — закрыто (пределы
  карточки). **m5** — отвечено J-15; census-сторона — N5. **m6** — закрыто (J-C6 (b)). **m7** — закрыто (PC-7 пометка). **m8** — отвечено:
  `batch-2-pervyj-vzglyad.md` и этот файл не закоммичены — коммитит сессия-владелец (не дизайнер). **m9** — закрыто (класс xref с
  заметкой). **m10** — закрыто (строка очереди §4.1).
- **L1** — применено: §6.1 L1; FL-1 часть B (ревизия 4 — по N1). **L2** — применено: FL-4, FL-7, FL-3, FL-8, FL-L3. **L3** — применено:
  бывший §10 влит в тело (см. строку «§10» ниже).

Повторный вердикт (t-2288):
- **N1** — закрыто (направление Lead): FL-1 разделён на часть A и часть B со своими owns, тестами, стартом (A — после G1; B — после слияния
  A) и критиком, id FL-1 сохранён. Часть B: ОДНА извлечённая функция `manual_capture.http_call` (в файле-владельце), один запрос при
  выбранном стенде и открытой попытке, без аренды, без `environment_of`/`stand_hosts`, без выбора попытки и без входа; `run_http` зовёт её
  (вывод байт в байт, `run_http_unchanged`), шаг ходока зовёт её через `_run_step` → `_run_http_word`; аренда — одна, `_hold_walk` прохода
  (`http_step_takes_no_stand_lease_inside_walk`); стенд — `--env` прохода, хосты — суженные, проверка в `request_problems` и в `http_call`;
  все шаги item — в попытке прохода. Грамматика: строка `steps.http` (`<METHOD> <path|url> [--body-file <file>]`, арность [2, 4]),
  разбор `parse_steps(…, http_ok=True)` + `_http_word_problem`; актёр — актёр запроса, `as:` нет. Вход: проход с экраном — контекст браузера
  актёра (`_BackendHttp`); без экрана — Bearer `_http_login` через `http_login_source` один раз для актёра ≠ гость (J-18: `default`);
  нет учётки/входа — проход открывается, шаги актёра — `failed` «http_sign_in_unknown…», требование — `unreachable`/`access`. Тело —
  существующие `_side`/`cut_body`/`body_text`/`redact`(`redact_headers`)/`_hide`/`secret_pattern_hit`, выдержка — из сохранённого,
  `CUT_WORDS` переиспользован, правило «non-UTF-8 replacement» снято (base64). HTTP-only проход имеет бэкенд `HttpOnlyBackend`.
- **N2** — закрыто (направление Lead): `first_look_continue --words-file F --source-head H --register-hash R`; `H`, `R` вычисляет вызывающий
  (FL-5, FL-6, `s3.md`) через `first_look.current_keys`; PC-6 хранит как даны (`first_look_continue_stores_given_keys`) и отказывает без них
  (`first_look_continue_without_keys_refused`, `…bad_register_hash_refused`); PC-6 ни от чего в FL-2 не зависит (временной край в PC-6).
- **N3** — закрыто (направление Lead): `source_head` — карта по репозиториям; `first_look.read` возвращает её; FL-6 п. 3: хоть один
  сдвинулся → приход; `unmeasured`/не установлено (записанное или живое) — не «сдвинулась», а вопрос `first_look.same_code` со строкой на
  каждый такой репозиторий; несколько репозиториев сравниваются все, вопрос их перечисляет; тесты `recorded_head_unmeasured_asks_not_arrives`,
  `multi_repo_compares_each_named_repo`, `multi_repo_one_moved_arrives`, `multi_repo_unknown_lists_each_repo`.
- **N4** — закрыто: `scripts/tests/fixtures/driver-layers.json` (фактический путь; бриф называл `references/…`) — в owns PC-2, PC-7, FL-5,
  FL-6, в §2 w, §4.1, §4.4 с порядком (сессия → PC-2 → PC-7 → FL-5 → FL-6); `test_driver_layers.py` — CI (медленный). Срезы
  `references/slices/**` + `contract_slices.py --check` — в owns и свидетеле PC-3, PC-5a, PC-9a, FL-7, у FL-2 — `--check` и срезы, если он их
  назовёт; §2 x, §4.4.
- **N5** — закрыто (направление Lead): таблица §4.7 — по каждому узлу, пишущему census, единицы и ожидаемый подъём (`safety` 51→54:
  PK0-1, PC-6 `rule_awaiting_code`, PC-9b C8; `blocking_per_role`: PC-4, PC-6, FL-2) + строки `driver-layers.json`; одобрены заранее, сверх
  — стоп; при слиянии — строки обеих сторон и сумма подъёмов. Найдено при обходе класса: PC-6 C13 и PC-9b C8 — safety (t-2181) и в
  прежней ревизии не назывались; PC-1a C17 обязан лечь в существующую единицу (иначе все роли +1).
- **N6** — закрыто: PK0-4 действительно нужен `_probe_actor` (t-2142: близнец карточки, `test_probe_actor_no_second_card`) — список
  функций его не исключает; D8 включён в G1 (он пишет и `walk_session.py`), PK0-4 ждёт G1; PK0-5, PK0-9 функциями с D8 не пересекаются и
  ждут G1 + G2 по `story_run.py`. G4 отмечен выполненным по перемеру t-2288; моим чтением подтверждено частично (метки TR3-14, TR3-16 в
  `guard_pre_tool.py`, TR3-5 — без метки); git я не запускала. Прочие писатели census (`test-diet`, `td/15-1/3/4/6a`, `tr/t2064-p3`, TR3-10
  C/D/D3a/D3c/D8) — строки очереди §4.1.
- **N7** — закрыто (направление Lead): PK0-7 сохраняет проверку t-2142 (по журналу «гейт A не спросил снова»); «известная роль и учётка —
  `used` в ретро» — в FL-L3 (§3.3 FL-L, §4.6).
- **m-new-1** — закрыто: инвариант позиции J-C7 (после `sides_unknown`/`on_substitute` и `failed:*`, перед flaky, partial, error,
  неизвестным словом, unconfirmed, skipped, обеими ветвями передачи, deferred, «за красным» и `passed_green`) — §1 J-C7, FL-7, §5 п. 4;
  тесты `handed_…`, `flaky_placeholder_test_is_placeholder_open`.
- **m-new-2** — закрыто: направление ошибки J-C9 (a) записано (§1 J-C9, направление `check_sides`, хартия критика кода в FL-7).
- **m-new-3** — закрыто: `open_failed` повторяется один раз на той же голове (`open_retry_max: 1`, `open_failures`), FL-2 `due`, FL-5 п. 2.
- **m-new-4** — отвечено: у первого взгляда `stand_build` почти всегда `not_established` — записано в FL-2 и FL-5; строка остаётся
  намеренно (FL-L1 меряет частоту); `runtime_probe` — носитель не установлен, вне плана.
- **m-new-5** — закрыто: повторный вопрос после `wait` несёт строку даты прежнего `wait` (FR-7: другой текст), FL-6 п. 4, тест
  `same_code_after_wait_carries_date_line`; носитель даты не прочитан — без него вопрос без строки (сказано).
- **m-new-6** — закрыто: `--side <s>=real` — триггер прихода, только если сторона ещё не `real` (FL-6 п. 2, тест `side_real_already_real_is_no_trigger`).
- **m-new-7** — закрыто: PK0-6 снят с очереди `report_facts.py` (§2 t, §4.4 сводка, PK0-6 «изменено»).
- **m-new-8** — закрыто: тест PC-9b назван `test_story_run_reference_walk.py::reference_window_opens_survey_env_walk` (CI).
- **m-new-9** — закрыто: шаг 0 FL-1 B называет писателя `Attempt.surprise`, `_surprises_after`, блок данных `surprise`; п. 10 пишет тем же
  писателем.
- **m-new-10** — закрыто: FL-3 перенесён в W3, где все его зависимости слиты в W2; в волнах внутриволновые зависимости названы в столбце
  «пишущих одновременно».
- **J-14** — применено решение владельца (a): §4.2 (условия критика, оба мира), §4.3 (W0 со стартом сейчас и подтягиванием), §6.1.
- **§10** — влит и удалён: 10.1 → §6.1 L3; 10.2 → PK0-2, PK0-4, PC-8 (строки §3.1/§3.2), FL-4, FL-7, FL-8, FL-L (§3.3), строка PK0-7 → FL-L3
  (N7); строка волн → §6.1 L3 и §4.4; строка AR → §1 (AR-12, AR-13, AR-27, AR-29) и FL-8; 10.3 → §5 t-2142 п. 9, t-2181 п. 14; 10.4 → §6.2
  J-15, J-16, J-17 и §6.1 J-14; 10.5 → «Чего я не прочитала или не установила».
