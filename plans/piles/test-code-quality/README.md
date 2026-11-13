# Качество тестов, которые пишет фабрика (`test-code-quality`)

приоритет: П1 | фичи: F11, F17, F20 | стенд: нужен только живому доказательству (прогон S5 на копии проекта) | зона: `agents/qa-automator.md`, `agents/qa-code-critic.md`, `agents/qa-case-designer.md`, `agents/qa-case-critic.md`, `references/code-review-rubric.md`, `references/test-code-patterns.md`, `references/judgments.d/code.json`, `references/detectors.json`, `scripts/s5_precheck.py`, `scripts/judge_code.py`, `scripts/validate_artifacts.py`, `scripts/manifest_from_tests.py`, `skills/qa-onboarding/phases/p1-discovery.md`, `p4-generate.md`

## Зачем

Codex (GPT-5.6 Terra) отрецензировал тесты, которые фабрика написала для двух MR проекта testproject1-sdk (!684 и !719): 17 пунктов,
из них по словам владельца (20.10.2026) надо взять то, что чинится на уровне фабрики — её правил, уставов ролей, проверок на выходе
S5, судьи и критика кода, — а не разовые ошибки прогона. Перепись t-1131 (`docs/tasks/specs/reports/t-1131-codex-review-mr684-mr719-factory-level.md`)
разложила пункты на восемь классов: K1 assert не отличает исправный продукт от правдоподобно сломанного (одна сторона диффа,
«список непуст», проверка только после цепочки delete→undo); K2 неизвестный оракул записан литералом (`== 403` при открытом Q4 —
P20/FR-58); K3 любой 4xx считается отказом по правам, актор не контролируется; K4 свой читатель состояния рядом с существующим в
фреймворке; K5 cleanup фикстур не гарантирован, сущности без метки проекта; K6 гонки и геометрия (гипотезы, без воспроизведения);
K7 тест опирается на модули, которых нет в доставляемом git-дереве; K8 вход ревью без текстов кейсов. По всем классам, кроме K6/K7/K8,
правило в фабрике УЖЕ есть (устав автоматора п.12, критик 1d, rubric dim 2/4/5, `test-code-patterns.md`, FR-58) — не хватает
исполнения: код-гейта на выходе S5 (`s5_precheck` ищет четыре фразы в тексте кейса, а не структурный оракул — ещё и FR-12), пробы
критика (`probe_by_code` мутирует только ПЕРВЫЙ assert), регэкспа `broad_status` (не ловит `is_in(range(400,500))`), smell-проверки
фикстур, тропы поиска аналога хелпера. Исполняет правила сегодня только LLM-критик.

## Что не так сегодня (факты)

- `scripts/s5_precheck.py:127` `OPEN_ORACLE_RES` — четыре фразы; `contract.resolve_then_oracle` в `s5_precheck.py` не читается (0 попаданий; контроль `coverage_contract.py` = 1); кейс-образец `cmp2-TC_014.md` пишет `oracle_unknown` — фразы нет.
- `scripts/probe_by_code.py:9-12` — мутируется первый assert теста; односторонний assert и «список непуст» пробу живости проходят; «сломанный близнец» находка forge «близнец» (t-081, 30.09) (`forge/findings`) с 30.09 без строки пачки (D-0044 не выполнено).
- `references/detectors.json` `broad_status` не ловит `is_in(range(400, 500))`, `>= 400`, `any_of(...)` (8 образцов в отчёте §6); контроля актора («те же учётные данные выполняют разрешённый вызов») нет ни в уставах, ни у судьи.
- `references/code-review-rubric.md:81-82` обещает ловить тавтологии до критика — детектора в коде нет (0 попаданий, контроль на `sleep` проходит).
- Судья `owns_its_data` спрашивает про создание данных, не про уборку; соглашение о метке сущностей (`autotest_entity_prefix`) в `p1-discovery.md` не спрашивается.
- Проверки «модуль, который импортирует тест, отслеживается git / есть в диффе ветки» нет; `test_novelty`/`function_sha` уже разрешают импортируемые файлы.

## Пачки

| № | Что изменится для пользователя | Строки | Размер | Статус | Взял | Ветка | MR |
|---|---|---|---|---|---|---|---|
| 1 | тест, который фабрика сдаёт в MR, не проходит на правдоподобно сломанном продукте, не прячет неизвестный оракул в литерал, отличает отказ по правам от любого 4xx, не дублирует читатель фреймворка, убирает за собой и целиком лежит в доставляемом дереве | — (две находки-ревью Codex, перепись t-1131; находка forge «близнец» (t-081, 30.09), находка roles-context «корпус seeded-defect» по ссылке) | M (8 узлов) | закрыта | — | `pile/test-code-quality/batch-1` | `855d4e5c` |
| 2 | слияние кейсов получает исполнителя у дизайнера, читатели доставки знают `Archived` (Q1 TQ1-27) | — (находка 02.11.2026, узел TQ2-1) | S | ожидает | — | — | — |

Открытое перенесено 01.11.2026 → release-next/1, execution-report/1, execution-report/2, onboarding-forge/2.

Статусы пачки: `ожидает` → `в работе` → `сдано` → `принято` → `закрыта`. Взятая пачка заморожена: её файл правит только взявший, новое по теме — файлом в `findings/`.

## Бриф пачки 1

Один механизм на класс (отчёт t-1131 §3): K2 → код-гейт `open-oracle-asserted` из структурного резолвера; K3 → `broad_status` данными + правило контроля актора в rubric/уставах/судье; K1 → строки rubric/patterns про обе стороны относительного результата и assert после каждого гасящего действия + вопрос судье `assert_discriminates`, доказанный корпусом seeded-defect из дефектов Codex (находка roles-context «корпус seeded-defect»); K5 → smell `fixture-cleanup-gap` + пункт онбординга о метке сущностей; K4 → тропа поиска аналога (`introduced_helpers[]` в манифесте, пункт критика, hint в `s5_precheck`); K7 → проверка `delivered-tree`; K6 → одна строка rubric, детектор только после измеренного случая. Порядок: K2 → K3 → K1-строки → корпус → судья → K5 → K4 → K7. Уставы критика упираются в пороги A22/A25 (`roles-context/README.md:14`, узел RC1-1) — строки уставов идут после RC1-1 или вместе с ним (`очередь:`).

## Дороги

Источник правды — `design/factory-rules.md` FR-58 (код не оракул), FR-18, FR-12, FR-13; PROJECT.md P16, P17, P19, P20; уставы `agents/*.md`; `references/code-review-rubric.md`, `test-code-patterns.md`, `judgments.d/code.json`; кейс-образец `experiments/measurers/...cmp2-TC_014.md`; корпус — `evals/` (находка roles-context «корпус seeded-defect»). Живое доказательство (FR-33): прогон S5 на копии TP1-15045 (кучка `live-runs`) после TQ1-5.

## Содержание

| id / файл | вид | суть (≤ 20 слов) | пути | статус | слово владельца | связи |
|---|---|---|---|---|---|---|
| **Пачка 1** | | | | | | |
| `batch-1-tests-that-discriminate.md` | пачка | восемь узлов по классам K1–K7 переписи t-1131 | зона кучки | ожидает | да (20.10 15:0x: «что можно исправить на уровне фабрики — создай пачку») | `roles-context/1` RC1-1, `grounding/1` G1-0, `execution-probes/1`, `forge` находка forge «близнец» (t-081, 30.09), находка roles-context «корпус seeded-defect» |
| **Находки** | | | | | | |
| `findings/20261020-codex-review-mr684-testy-fabriki.md` | ревью (текст владельца) | 9 пунктов Codex по тестам MR !684: диф в одну сторону, `warnings` непусты, `403` при открытом Q4, фикстуры без гарантии уборки, модули вне git-дерева | `scripts/s5_precheck.py`, `probe_by_code.py`, уставы, rubric | пачка 1, TQ1-1…TQ1-8 | да | t-1131 |
| `findings/20261020-codex-review-mr719-testy-fabriki.md` | ревью (текст владельца) | 8 пунктов Codex по тестам MR !719: свой читатель Ace рядом с `get_yaml_content()`, проверка после цепочки Delete/Undo, `range(400,500)`, сущности без метки, UI-контракт из недоступного исходника | те же | пачка 1, TQ1-1…TQ1-8 | да | t-1131 |
| `docs/tasks/specs/reports/t-1131-codex-review-mr684-mr719-factory-level.md` | перепись | 17 пунктов → 8 классов, вердикты A/B/C с носителями, механизмы, пересечения, раскладка | — | принята Lead 20.10 (выборочная проверка: `resolve_then_oracle` 0/1, `OPEN_ORACLE_RES` :127, проба — первый assert) | — | — |
| `forge/findings/находка forge «близнец» (t-081, 30.09)-…` | перенос | «сломанный близнец» на каждый Then, проба по `assertion_ref` | `probe_by_code.py --at`, `artifact-contract.md`, `s5.md:71` | TQ1-5 (развилка F-2) | нужно | находка roles-context «корпус seeded-defect» |
| `findings/20261021-kontrakt-pokrytiya-then-fajl-stroka-na-gejte.md` | находка | контракт покрытия в коде: каждый Then → `файл:строка` с текстом ассерта на гейтовой ревизии, тест исполнен и не пропущен; красный по требованию = упавший ассерт | `scripts/probe_by_code.py`, `scripts/s5_precheck.py` | TQ1-9, ожидает | нет | TQ1-1, `execution-probes`; обзор testing-factory (K2) |
| `findings/20261021-test-story-step-chas-pod-nagruzkoj-razdelit.md` | находка | `test_story_step.py` (465 проверок) идёт час под нагрузкой на Windows: разделить по командам или стадиям, как `test_story_run_*`; общий сид в common | `scripts/tests/test_story_step.py`, `scripts/selftest.py` | TQ1-10, ожидает | нет (приоритет П1 — слово владельца 21.10) | D-0056; замер Lead 21.10 по транскриптам воркеров |
| `findings/20261024-avtomator-beret-dannye-stenda-vmesto-fikstur-harnessa.md` | находка | фабрика не применила подход проекта к данным, записанный при онбординге: спросила о проектах стенда на гейте A, тесты на ключах `.env` вместо фикстур | `agents/qa-test-strategist.md`, `agents/qa-automator.md`, `agents/qa-code-critic.md`, `scripts/brief_pack.py`, `judgments.d/code.json` | TQ1-11, ожидает | нет (уточнение владельца 24.10 учтено) | t-1207; TQ1-6, `onboarding-hooks` |
| `findings/20261024-otkaz-ne-razlichaet-prichinu-i-sravnenie-po-maske.md` | находка | TC-008 проходит на общем 400 вместо singleton, тавтология `ok`; секреты сравниваются маской с маской | корпус TQ1-4, rubric | TQ1-12, ожидает | нет | t-1207; TQ1-2, TQ1-4, TQ1-5 |
| `findings/20261024-vtoroj-heljper-ryadom-s-sushchestvuyushchim-i-dubli-fikstur.md` | находка | второй `select_project` и `wait_for_page_load` рядом с харнессом; одинаковые фикстуры в двух conftest | как TQ1-7 | TQ1-13, ожидает | нет | t-1207; TQ1-7 |
| `findings/20261024-krasnaya-stroka-raspakovka-do-assert-i-e2e-dlya-klientskih.md` | находка | распаковка до assert теряет Then в красной строке; клиентские сценарии в e2e вопреки плану S3 | `test-code-patterns.md`, rubric, `agents/qa-code-critic.md` | TQ1-14, ожидает | нет | t-1207; TQ1-3 |
| `findings/20261025-s7-ne-stavit-kontrolnyj-opyt.md` | находка | S7 решает «баг или тест строже требования» чтением, без контрольного опыта; сид слабее Given не ловится; по умолчанию — ложный `APP_BUG` | `qa-failure-analyst.md`, `s7.md`, `code-review-rubric.md`, `qa-code-critic.md` | TQ1-15, ожидает | да (25.10: иначе — во вторую волну срочной пачки) | t-1226; DC1-9; GW1-23 |
| `findings/20261029-sleep-v-fikstura-conftest-ne-viden-proverke.md` | находка | `sleep(2)` в новой фикстуре conftest не виден `s5_precheck` (смотрит только фикстуры-аргументы из файла теста); пойман критиком после пробы | `s5_precheck.py`, `brief_pack.py` | TQ1-16, ожидает | нет (П1 0.10.7 — решение Lead) | прогон 12586 на 0.10.5; HF8-15; TQ1-13 |
| `findings/20261029-uroven-i-vetki-teryayutsya-mezhdu-s3-i-s5.md` | находка | S3 спускает R-13/R-10 в ручной агент по неизмеренной посылке, S4 снимает ветку alias без нового дома, S5 тихо выбрасывает Webhook; оракулы 400=400 и маска=маска проходят критика кода | `qa-test-strategist.md`, `qa-case-critic.md`, `code-review-rubric.md`, `test-code-patterns.md`, `report_facts.py` | пачка 1, TQ1-17 | нет (П1 0.10.7 — решение Lead) | TQ1-3; TQ1-4; TQ1-11; TQ1-12; G2-11; t-1577 |
| `findings/20261029-orakul-kak-do-na-otricatelnom-otvete.md` | находка | Then «как до» на отрицательной базе: test-connection 400 до и после — тест «интеграция пригодна» зелёный при любых кредах | `qa-case-designer.md`, `qa-case-critic.md`, `s5_precheck.py`, `ledger.py` | пачка 1, TQ1-18 | да (слово владельца 29.10.2026) | TQ1-3; TQ1-12; TQ1-17 |
| `findings/20261029-zapret-dublej-ne-rabotaet-bez-detektora.md` | находка | запрет дублей — только текст; детектор S5 ловит лишь точную копию тела в файлах окна, не почти-копии и не копии существующего кода харнесса | `s5_precheck.py`, `brief_pack.py`, `manifest_from_tests.py` | пачка 1, TQ1-19 | да (слово владельца 29.10.2026) | TQ1-7; TQ1-16 |
| `findings/20261029-skvoznoj-uchyot-vetok-ot-s2-do-otchyota.md` | находка | ветки внутри требований (оговорки, партиции, варианты) тают между S2 и S5 без следа; механизм сквозного учёта веток с отказом на пропаже и кандидатами из существующих тестов области | `contract.py`, `planning_contract.py`, `handoff_check.py`, `report_facts.py` | пачка 1, TQ1-20 | да (слово владельца 29.10.2026) | G2-11; TQ1-17; TQ1-18 |
| `findings/20261029-extend-cel-plana-ne-sushchestvuet-na-baze.md` | находка | цель `extend` плана S3 не существует на базе: дизайнер S4 ищет по всему диску, нужны доработка и второй раунд критика | `scripts/planning_contract.py`, `brief_pack.py` | TQ1-21, ожидает | нет (П1 0.10.7 — решение Lead) | TQ1-17, G1-2, TQ1-7 |
| **Находки ночного прогона 14857 (0.10.6), 30.10.2026** | | | | | | |
| `findings/20261030-then-sravnivaet-vremya-servera-s-vremenem-hosta-bez-dopuska.md` | находка | Then со штампом сервера против метки хоста без допуска: 2,3 мс разницы часов стали `contradicts_requirement` | `agents/qa-code-critic.md`, `references/test-code-patterns.md`, `scripts/report_facts.py` | пачка 1, TQ1-22 | нет | t-1605 #14; TQ1-18 |
| `findings/20261030-kazhdyj-kritik-koda-perezapisyvaet-critic-findings.md` | находка | каждый критик кода перезаписывает `critic-findings.md`: замечания раундов 1–3 живут только в транскриптах | `agents/qa-code-critic.md`, `scripts/report_facts.py` | пачка 1, TQ1-23 | нет | t-1605 #27; DC1-22; RD1-9 |
| **Уроки сравнения тестов 14857 с MR 798 (t-1606), 30.10.2026** | | | | | | |
| `findings/20261030-vilka-vremeni-cherez-asinhronnuyu-zapis-bez-dopuska-i-ishoda-nelzya-razlichit.md` | находка | вилка времени через асинхронную запись или два источника времени без допуска и исхода «нельзя различить»; правило в форме кейса на S4; поправка причины TQ1-22 | `qa-case-designer.md`, `qa-case-critic.md`, `test-code-patterns.md`, `code-review-rubric.md` | пачка 1, TQ1-24 | нет | t-1606 §2, урок 3; TQ1-22; TQ1-25 |
| `findings/20261030-then-razlichayushchij-traktovki-dolzhen-past-pri-drugoj-proba-modeliruet-ee.md` | находка | Then, различающий две трактовки, падает при второй; красная проба моделирует альтернативу, а не инвертирует assert | `code-review-rubric.md`, `test-code-patterns.md`, `judgments.d/code.json`, `probe_by_code.py` | пачка 1, TQ1-25 | нет | t-1606 урок 4; TQ1-5; TQ1-3; EP1-3 |
| повтор в находке `extend-cel-plana…` (строка выше, TQ1-21) | повтор | MR 798: цель `extend` разрешается в рабочем checkout; отсутствующая цель делает кейс новым вместе со слоем поддержки (page object) | как TQ1-21 | TQ1-21 (дополнен) | нет | t-1606 урок 5 |
| `findings/20261030-detektor-kopij-propuskaet-razbituyu-kopiyu-i-druguyu-formu-tela.md` | находка | `copy_detector` пропускает копию, разбитую на две функции, и копию другой формы тела; однооператорные фикстуры — критику кода | `agents/qa-code-critic.md`, `scripts/copy_detector.py` | пачка 1, TQ1-26 | нет | D2-K13/Q-4; P17 |
| `findings/20261030-kritik-kejsov-ne-ishchet-dubli-i-sliyaniya-p16.md` | находка | критик кейсов S4 принял все 12 кейсов 12586 без находок о дублях и уровне; честный минимум 9; измерение «дубли и уровень» с полем `merge_candidates` и проверкой кода на выходе S4 | `agents/qa-case-critic.md`, форма S4, `scripts/exit_gate.py` | TQ1-27, ожидает | да (30.10: «были ли лишние кейсы или двигать потолок на 15» — лишние были, потолок не двигать) | t-1620; SC5-6; TQ1-17; TQ1-7/19 |
| `findings/20261031-rubriki-t4-t5-tochnye-formulirovki-pod-polom-a25.md` | находка, id — | две точные правки рубрики критика кода (T4, T5) под полом A25 (t-520) | `references/code-review-rubric.md`, `references/test-code-patterns.md` | TQ1-28, ожидает | нет | TQ1-3 |
| `findings/20261101-analogi-mutacionnogo-prohoda-kanona-d-klyuchi-ne-ubivayut-mutantov.md` | находка, id — | аналоги прохода t-442: ключи, не убивающие мутантов (разбор команды, зависимость от данных, дубль алиасов, половина `resume`) | `scripts/tests/`, `scripts/bug_records.py` | TQ1-29, ожидает | нет | TQ1-3; TQ1-28 |
| **Обзор MR !12, 01.11.2026** | | | | | | |
| `findings/20261101-s5-precheck-ravenstvo-chitaetsya-tolko-v-treh-zapisyah.md` | находка, id — | ворота относительного оракула читают равенство в трёх записях: assertpy и Playwright проходят молча; словарь записей — в `detectors.json`, нечитаемое сравнение — заметка | `scripts/s5_precheck.py`, `references/detectors.json` | пачка 1, TQ1-30 | нет | t-1644 M1; TQ1-18; TQ1-16; TQ1-19 |
| `findings/20261102-sliyanie-kejsov-bez-ispolnitelya-na-storone-dizajnera-i-dvojnye-chitateli-shapki.md` | находка | слияние кейсов не имеет исполнителя у дизайнера, читатели доставки не знают `Archived`, три читателя шапки таблицы | `agents/qa-case-designer.md`, `scripts/contract.py`, `scripts/check_delivery.py`, `scripts/critic_rollcall.py` | пачка 2, TQ2-1 | нет | t-715 B-1, t-756 m-5, m-6; TQ1-27 |
| `findings/20261113-chitateli-kolonki-tablicy-rukami-vne-critic-rollcall.md` | находка, id — | шесть читателей колонки таблицы руками вне `critic_rollcall` (`audit_factory`, `planning_contract`) — через `contract.md_column`, направление ошибки назвать | `scripts/audit_factory.py`, `scripts/planning_contract.py` | пачка 2, TQ2-2 | нет | критик темы TQ2-1 (Q1); TQ2-1 |
| `findings/20261113-narezka-okon-derzhit-gruppy-slijaniya-i-c12-dlya-legacy.md` | находка, id — | нарезка окон разрезает пары слияния (legacy режет по кейсам), у окон legacy нет C12; один механизм — группа слияния остаётся вместе | `scripts/s5_plan.py`, `scripts/controller.py`, `scripts/s5_precheck.py` | пачка 2, TQ2-3 | нет | критик темы TQ2-1 (Q2, F7); TQ2-1 |
| `findings/20261113-case-concern-lines-71-stroka-mertvaya-rabota-i-prichina-bez-granicy.md` | находка, id — | `case_concern_lines` на 71 строку, `elsewhere` вычисляется зря, причина стадии без границы | `scripts/brief_pack.py`, `scripts/s5_plan.py` | пачка 2, TQ2-4 | нет | критик темы TQ2-1 (Q3); TQ2-1 |

## Входящие

Находки по теме кладутся файлом в `findings/` и строкой сюда и в невзятую пачку (D-0044).

## Вопросы владельцу

Отвечены владельцем 20.10.2026 16:2x (чат):

- F-1 (K3, TC-014/015): при неизвестном оракуле отказа (401 vs 403 — Q4 открыт) норма — **(а) «диапазон 4xx + контроль актора»**: тест проверяет, что отказ есть (4xx), что ТЕ ЖЕ учётные данные выполняют разрешённый вызов, и код причины — если он известен; при ответе на Q4 тест дотягивается до точного кода без переписывания. Не `expectation_unconfirmed` до ответа. Исполняет TQ1-2 (б).
- F-2 (K1, находка forge «близнец» (t-081, 30.09)): **(б) одна проба критика на тест как сейчас (`s5.md:71`) плюс вопрос судье `assert_discriminates` с замером recall на корпусе дефектов Codex** (TQ1-4 → TQ1-5). Узел «близнец по `assertion_ref` каждого Then» НЕ открывается; возврат к пробе на каждый Then (или только для относительного результата) — если recall на корпусе окажется плохим: тогда новая находка со счётом recall, не правка пачки.
- F-3 (K8): **(в) не менять**. Слово владельца: «Сейчас кейсы складываются в место, которое укажет пользователь: или в ТМС, или файлом в артефакты стори, так и оставим». Тексты кейсов к MR тестов не прикладываются; `render_case_appendix.py` и доставка не трогаются; K8 закрыт без узла.
