# t-1469 — черновик спеки: hotfix-12586 пачка 4, починки живого прогона TP1-12586 для релиза 0.10.5

Дизайнер (opus), 28.10.2026. Черновик для приёмки Lead: развилки (§7) возвращены, не решены. Проза — по-русски, всё, что
уходит в пакет (код, тексты ролей, фикстуры, сообщения), — по-английски (FR-30). Пути пакета — от
`D:/ws1/yml-text-factory\ai-packages\qa-factory\` (в worktree билдера — тот же относительный путь).
Ревизия 2 (28.10.2026): §5.2, §5.5, §5.6 переписаны по критику на план t-1472, §11 дополнен решениями Lead, список правок — §12.

Слова владельца 28.10.2026: (1) прогон несколько раз требовал её слова там, где фабрика должна была ехать сама — починки идут в
релиз; (2) находка `plans/piles/forge/findings/20261028-testy-ne-derzhat-styki-stadij.md`: каждая починка получает минимум один
**ключ стыка** — настоящий выход производителя (артефакты прогона со стенда, скопированные в фикстуру, или настоящая форма вывода
роли/скрипта) прогоняется через гейт-потребителя, а не только руками собранный вход.

## 1. Что меняется и какие инварианты AR-n затронуты

Пачка `hotfix-12586/4` (статус «ожидает», не взята) получает шесть новых узлов HF4-6…HF4-11 рядом с HF4-1…HF4-5 (они остаются
как есть). Нумерация продолжает пачку (решено мной, §8).

| Узел | AR-n | Проверка изменения (`design/architecture.md`), которую требует DoD |
|---|---|---|
| HF4-6 | AR-5, AR-9, AR-13, AR-15, AR-28, AR-12 | AR-15/AR-13: grep пакета по форме проблемы «последнее слово ребёнка из транскрипта» (`transcript_path`, `agent_transcript_path`, `type") == "assistant"`) с положительным контролем; каждый сайт вызывает выжившего или назван на оси 22. AR-28: спека называет поведение на отсутствующем / нечитаемом / пустом транскрипте, тест пинует. AR-9: отказ формы теперь доходит до автора, дверь используема (FR-2). AR-12: `code_friction` S1–S5 до/после или «не измерено» строкой |
| HF4-7 | AR-10, AR-13, AR-16, AR-22, AR-26, AR-28 | AR-10: новое поле формы (`now`/`before`, `claim`) входит в контракт, скелет роли (дизайнер И тестировщик требований) и текст отказа одним коммитом. AR-22: grep `question_thens`, `readings`, `claim_readings`, `CLAIM_INTENDED`, `case_entry_answers` по `scripts/ agents/ skills/ references/ handoffs/` без учёта регистра с контролем — все читатели меняются с производителем. AR-26: новое ожидание называет свой оракул; повторить census grep по тронутым файлам. AR-13: один читатель «текст Then под ответом» (`contract.question_then_text`), `planning_contract.case_entry_answers` — его обёртка |
| HF4-8 | AR-13, AR-16, AR-22, AR-24, AR-28 | AR-22: у ячейки `Decision` таблицы `## Reading forks` появляется читатель — производитель (шаблон регистра, контракт S2, роль) меняется тем же коммитом. AR-13: ячейка читается через ось 21 (`project_decisions._cells`), статус вопроса — только через `question_register.load`/`settled`, «Already decided» — через `question_register.answers_for_brief`. AR-16: вопрос не переспрашивается (FR-7). AR-28: нечитаемый регистр/ответы — вопрос остаётся (тест) |
| HF4-9 | AR-14, AR-22, AR-24, AR-25 | AR-14: строку плана пишет один писатель плана (через его команду, не вторым писателем). AR-22: новое поле, которое пишет подъём вопроса, имеет читателя (`contradiction_questions`, `apply_recorded_answers`). AR-25: устаревшее состояние строки имеет выход |
| HF4-10 | AR-9, AR-22, AR-23, AR-27, AR-28, AR-14 | AR-22/FR-5: требуемая квитанция без производителя не требуется — ни квитанция окна, ни соседнее поле привязки `quality_not_applicable_reason`; grep `required_quality_checks`, `quality_receipts`, `quality_receipt_refs`, `quality_not_applicable_reason`, `quality_not_run` (все читатели меняются вместе); новое поле `quality_not_run` имеет читателя тем же коммитом (строка отчёта). AR-23: пустой список имеет свой исход. AR-27: пробел доходит до отчёта под своим владельцем (фабрика). AR-28: нечитаемый файл данных — объявленный безопасный дефолт (прежнее требование), не проход. AR-9: отказ `_code_review_refusal` перестаёт называть дверь, которой у критика нет |
| HF4-11 | AR-7, AR-9, AR-13, AR-18, AR-21, AR-25 | AR-7: роль решает слово, код только сверяет его с правилом по ячейкам и отказывает с дверью (никогда не переписывает, FR-35). AR-13: слово читается только через `critic_rollcall.scoped_verdict`, замечания — через один читатель `carried_concerns` и один читатель цепочки замечаний `s5_plan.remarks_of`. AR-21: собранное критиком S4 доезжает до S5 целиком. AR-9: новый отказ — с дверью критику |

FR-разделы по узлам — в §5 каждого узла (проход пишет билдер в отчёте, PROJECT.md «Как принимается изменение пакета» п. 1).

## 2. Проверенные факты (носитель прочитан) и поправки к карте t-1468

1. **P1 подтверждён и шире, чем в карте.** `scripts/exit_gate.py:621-649` `handoff_digest` читает только
   `event["transcript_path"]` и берёт ТОЛЬКО текстовые блоки строк `type: assistant`. `cost_capture.py:3008-3021`: под Claude
   SubagentStop несёт `transcript_path` РОДИТЕЛЯ, файл ребёнка — в `agent_transcript_path`. **Новое:** роли фабрики сдают
   последнее слово вызовом `SubagentHandback` (`tool_use`), а не текстом: настоящий транскрипт критика прогона
   `C:\Users\dev1\.claude\projects\D--ws-testproject1-dev-010-testproject1-sdk-test-harness\22686563-d408-46cd-b461-7c3b276d6746\subagents\agent-a19dac213a6228a50.jsonl`,
   строка 75 — `{"type": "tool_use", "name": "SubagentHand…"}` с дайджестом `qa-case-critic S4 TC-014 · concerns …` во входе,
   строка 76 — `tool_result`. Значит, направление карты «читать `agent_transcript_path`» с нынешним разбором (только `text`)
   дайджест всё равно НЕ найдёт. Форму возврата хоста знает ось 22 (`docs/SIBLING_MAP.md:405-417`): данные
   `references/host-report-forms.json`, один читатель `host_adapter.report_forms`, читатель формы `host_probe._assistant_texts`
   (`host_probe.py:474-504`). `exit_gate.handoff_digest` — недостающий сайт этой оси (FR-17).
   Следствие, не названное картой: `is_halting_handoff(digest)` (`exit_gate.py:652`) читал прозу дирижёра — `halt` роли гейт
   не видел.
2. **`last_assistant_message`** в пакете не читается нигде (0 совпадений; положительный контроль той же формы —
   `agent_transcript_path` найден в 20+ местах `scripts/`). Есть ли это поле в событии SubagentStop Claude Code — **оценка, не
   проверено**: сырого события в каталоге прогона нет (карта t-1468 P1 (b)).
3. **P8, корень установлен** (находка GW1-25 говорит «не установлено»). Версия кейса до подъёма вопроса
   `…\TP1-12586\work\test-cases\cases\TC-014\cv_998932e2dc6129302ba7.md:16`: `question_thens: [{"question": "raise", "then": 1,
   "readings": {"a": "…rejected with 4xx…", "b": "…answers 2xx…"}}]` — дизайнер писал буквы, когда вопроса Q7 ещё НЕ было; порядок
   чтений позже задал код: `contract.claim_readings` (`contract.py:589-607`) — фиксированно `a` = «Intended: the behaviour now»,
   `b` = «A regression». В `references/artifact-contract.md:96-109` и `agents/qa-case-designer.md:55-59` порядок чтений
   before/now-вопроса роли не назван — нарушение FR-38/AR-10 (требование не дошло до роли до работы). Версия гейта A
   `cv_b3406f0980d40df314bc.md:15` — те же буквы под `"question": "Q7"`. Буква читается: `gate_brief._then_effect`
   (`gate_brief.py:1936-1959`, `readings.get(answer)`), `contract.resolve_then_oracle` (`contract.py:1135-1191`) и
   `planning_contract.case_entry_answers` (`:1180-1190`, «THE one reader» для `variant_errors` и применителя `_case_rework`; найдено
   критиком t-1472). Позиционный смысл буквы before/now несут ещё `contract.CLAIM_INTENDED = "a"` (`:879`, `claim_confirmed`),
   `before_value_needed` (`reading == "b"`) и ветка O2 резолвера (`letter == "b"`) — t-1472 N7-2.
4. **P2, корень уточнён.** `gate_brief.contradiction_questions` (`gate_brief.py:1602-1678`) пропускает строку, если (i) все её
   `question_refs` резолвятся в регистре, (ii) текст решений `_mentions` R-n. На стенде связь R↔Q ЕСТЬ, но в двух нечитаемых
   местах: (а) регистр `…\work\requirements-register.md:64-71`, таблица `## Reading forks`, колонка `Decision`: `R-1 … Q4 a
   adopted`, `R-3 … Q1 b adopted`, `R-4 … Q3 b adopted`, `R-5 … Q2 a adopted`; (б) строки плана `…\work\test-plan.json` TS-1/TS-8
   несут `decision_refs: ["Q1 b: …"]`, `["Q4 a: …", "Q3 b: …"]` — поля нет в контракте (0 совпадений `decision_refs` в пакете;
   контроль той же формы — `question_refs`, 180 совпадений). Шаблон `references/templates/requirements-register.md:87-95` даёт в
   `Decision` только `question at gate A | reading A adopted` — id вопроса не предусмотрен. Ответы — `…\work\question-answers.jsonl`:
   Q1 b, Q2 a, Q3 b, Q4 a, Q5 a, Q6 и Q7 — своими словами (`status: answered`, без `reading`).
   «Already decided» (`gate_brief._decided_lines`, `:2327-2357`) печатает только пропуски, принятые пробелы и исключённые
   источники; ответы `Qn` — нет, хотя один читатель для них есть: `question_register.answers_for_brief` (`question_register.py:872-892`).
5. **P4.** TS-14 (`test-plan.json:431-461`): `oracle_unknown: true`, `question_refs` нет; кейс TC-014 поднял Q7 на выходе S4
   (`question_register.raise_for_case`, `:1068+`, пишет id только в КЕЙС); правило S3 `elif refs_carried and oracle_unknown`
   (`planning_contract.py:1239,1255`) срабатывает лишь если хоть одна строка несёт `question_refs` — здесь ни одна. Поэтому
   карточка `TS-14` на гейте A — дубликат Q7. После ответа Q7 на гейте A план не патчится: `apply_recorded_answers`
   (`planning_contract.py:2264-2289`) — «gate A approved: not applied».
6. **P5.** `window_record.py:940-950` пишет `"quality_receipts": []` с комментарием «nothing in this package writes a quality
   receipt». Состояние стенда: `required_quality_checks: ["ticket_adapter","test_repo","vcs","config_schema"]` — это id проверок
   `readiness.py` (`:27`, `:69`, `:981`). Кто их записал — **оценка, не установлено** (t-1472): текст `references/controller-api.md:89`
   («readiness check IDs») и `skills/qa-story/phases/s0.md:445` ведёт дирижёра к ним; второй производитель поля —
   `story_run.Driver.quality_check_ids` (`:5811-5821`), на конфиге стенда (`quality_gates` — словарь `{"lint": {…}}`) он даёт `[]`,
   значит не он. Для фильтра HF4-10 факт не несущий. Читатели требования: `acceptance.validate_window` (`:816-824`, пробел
   `quality:<id>`), `coverage_contract` (`:230-235` и `:555`), `controller._s5_collect` (`:5879-5881`), отказ
   `controller._code_review_refusal` (`:5197-5217`, дверь «review's own receipts» — у критика её нет, FR-2); форма окна —
   `contract.py:3494, 3631`; `window_record.py:1177` (`receipt_dict`); `revise_plan` переносит поле (`story_run.py:8666`,
   `controller.py:4292`). Перепрогон t-1472: каждое окно S5 стенда даёт 4 пробела `quality:*`; 13 привязок манифеста стенда — без
   `quality_receipt_refs` и без `quality_not_applicable_reason`.
7. **P3.** `agents/qa-case-critic.md:72-77`: `approve_with_concerns — ≤2 concern, 0 fail`, `reject — any fail or ≥3 concern`;
   `critic_rollcall.scoped_verdict` (`:244-321`) сохраняет заявленный `reject` над одобряющими ячейками (FR-35, `:309-312`).
   Строки «concerns carried» в `gate_brief.py` нет (t-1472 опроверг карту t-1468). Автоматор находки критика КЕЙСОВ не читает
   (`brief_pack.ROLE_FILES["qa-automator"]`, `brief_pack.py:87`: только `work/test-code/critic-findings*.md`). Носитель «по кейсу»,
   который автоматор обязан отработать построчно, — замечания плана S5: `s5_plan.remarks_of` (`s5_plan.py:1069-1083`) → раздел брифа
   окна (`brief_pack.py:1799-1850`) → строка `plan_remarks`, проверка `s5_plan.remark_rows_missing` в `s5_precheck.py:2674` (C12).
   Петля S4 гонит доработку по слову ДАЙДЖЕСТА `concerns` (`story_run.s4_after_critic :8534`, `s4_critic_completion :8570`).
8. **Тестов `scripts/tests/test_planning_contract*.py` нет** (карта t-1468 их называет). Есть `test_question_branches.py`,
   `test_plan_row.py`, `test_plan_contract_text.py`, `test_s3_s4_chain.py`.
9. Пачки 2 и 3 кучки — «в работе» (шапки файлов); HF3-10 «принято (сделано: c36b8525)». Зависимости HF4-1…HF4-5 от слияния
   HF3-1/2/6/7 — проверить по `main` до волны (я по `main` не сверяла).

## 3. Таблица узлов (новые строки пачки 4)

Колонка «Пишет в» для HF4-7, HF4-10, HF4-11 — краткая; полный owns — §5.2, §5.5, §5.6 (ревизия 2).

| Узел | Приоритет | Что | Исполнитель | Пишет в (функции для горячих и общих файлов) | Зависит от | Поглощает |
|---|---|---|---|---|---|---|
| HF4-6 | П1 | Выходной гейт читает последнее слово самой роли: транскрипт ребёнка (`agent_transcript_path`) через читатель формы возврата хоста (текст И вход вызова handback, ось 22); транскрипт родителя никогда не судится как слово роли; `halt` роли виден (P1, 17 ложных блоков) | builder → critic (спека — §5.1) | `scripts/exit_gate.py` (`handoff_digest`), `scripts/host_adapter.py` (новая `assistant_row_texts`), `scripts/host_probe.py` (`_assistant_texts` зовёт её), тесты, фикстура `scripts/tests/fixtures/run-12586-digest/` | — | SC2-27 (корень; см. F-7) |
| HF4-7 | П0 | Ответ на before/now-вопрос связан с текстом Then по смыслу чтения (`now`/`before`), а не по букве; один читатель «текст Then под ответом» для карточки, резолвера, `case_entry_answers` (а через неё — `variant_errors` и применителя); буквы на before/now-вопросе — отказ с дверью (P8, Q7) | builder → critic | `scripts/contract.py` (функции §5.2), `scripts/planning_contract.py` (`case_entry_answers`, ветка кейсов `variant_errors`, новая `_claim_key_errors`), `scripts/gate_brief.py` (`_then_effect`, `question_effects`), роли дизайнера и тестировщика требований, контракты, тесты, фикстура `run-12586-q7/` | — | GW1-25 целиком |
| HF4-8 | П1 | Гейт A не переспрашивает `R-n`, чью развилку закрыл отвеченный `Qn` (связь — данные регистра); «Already decided» печатает каждый закрытый `Qn` словами человека (P2) | builder → critic (после F-3) | `scripts/gate_brief.py` (`contradiction_questions`, `_decided_lines` и функция, собирающая для него `data`), `scripts/planning_contract.py` (новая `register_fork_questions`), `references/templates/requirements-register.md` (`## Reading forks`), `references/artifact-contract-plan.md` (строка о `Decision`), `agents/qa-requirements-tester.md` (одна строка), тесты, фикстура `scripts/tests/fixtures/run-12586-gate-a/` | — | GW1-26 (часть «R-n против Qn») |
| HF4-9 | П1 | Вопрос, поднятый на выходе S4 для кейса, попадает в `question_refs` строки плана этого кейса (один писатель плана); дубль карточки «TS-n vs Qn» исчезает; устаревшая строка после ответа — по F-4 (P4, TS-14) | тот же билдер, что HF4-8 (общая функция `contradiction_questions`) → critic | `scripts/question_register.py` (`raise_for_case`), `scripts/planning_contract.py` (писатель `question_refs` строки — через существующую команду писателя плана, имя называет билдер; новая функция, не правка чужих), `scripts/plan_row.py` (если это и есть писатель), тесты, та же фикстура `run-12586-gate-a/` | HF4-8 (один билдер, порядок внутри) | GW1-26 (часть «TS-14 и Q7 — один вопрос») |
| HF4-10 | П1 | Квитанция качества, которую не пишет ничто в фабрике, не требуется (FR-5) ни у окна, ни у привязки; не требуемое — поле окна `quality_not_run` `{id, why}` и строка отчёта «Quality checks the factory did not run: …», id готовности, проверенные S0, туда не попадают; окна S5 не ждут слова (P5) | builder → critic | `references/quality-receipt-producers.json` (новый), `scripts/window_record.py`, `scripts/acceptance.py`, `scripts/coverage_contract.py` (2 места), `scripts/controller.py` (`_s5_collect`, `_code_review_refusal`), `scripts/contract.py` (форма окна), `scripts/report_facts.py` (одна функция), тексты S0/контроллера/автоматора, тесты, фикстура `run-12586-s5-quality/` | — | — (узла нет; нужна находка, §6) |
| HF4-11 | П2 | По слову владельца 28.10 (F-6 (A)): `reject` критика кейсов — только при падающем кейсе; замечания без `fail` — `approve_with_concerns`, дайджест `ok`; раунд, заявивший `reject` без падающего кейса, — отказ критику с дверью (код слово не переписывает); замечания принятого раунда едут автоматору замечаниями окна S5 (`remarks_of` → `plan_remarks`, C12) и строкой гейта A | builder → critic, живое доказательство FR-33 | `agents/qa-case-critic.md`, `scripts/critic_rollcall.py` (`scoped_verdict` через новую `_round_word_rule`, новая `carried_concerns`), `scripts/s5_plan.py` (`remarks_of`), `scripts/gate_brief.py` (функция строки критика), `scripts/brief_pack.py` (условно), тесты, фикстура `run-12586-concerns/` | — | — (узла нет; нужна находка, §6) |

Строки `перенос` в пачки-источники (пачки не взяты — правка статуса допустима):
- `plans/piles/gates-and-words/batch-1-words-and-gates.md`, GW1-25: статус `ожидает (перенос: hotfix-12586/4 HF4-7)`.
- там же, GW1-26: статус `ожидает (перенос: hotfix-12586/4 HF4-8, HF4-9)`.
- `plans/piles/speed-cost/batch-2-ostatki-reliza-0-10-3.md`, SC2-27: по F-7 — `ожидает (перенос корня: hotfix-12586/4 HF4-6)` и
  строка узла остаётся с «ценой блока»; либо `перенос: hotfix-12586/4 HF4-6` целиком.
- GW1-21 уже перенесён в `hotfix-12586/2` HF2-7 (строка «Хода» 25.10) — не поглощается.
- НЕ поглощаются (остаются в `gates-and-words/1`, их P2-кластер): GW1-27 (предусловия), GW1-28 (пробный тест), GW1-29 (TS-8 сам себе
  противоречит), GW1-30 (commit/stash), GW1-31 (ключи интеграций), GW1-32 (формы ответа).

Размер пачки после добавления: 11 узлов → L (карточка: L 10–15). Строку пачки в `README.md` («Что изменится», «Размер») правит Lead.

## 4. Параллельность (≤ 6 пишущих билдеров)

Пересечения owns только по функциям (D-0048: строка `функции:` в «Ходе» обеих). Пары общих файлов после ревизии 2 — §12 п. 10.

| Слот | Волна 1 (сразу) | owns-ядро | Пересечение |
|---|---|---|---|
| W1 | HF4-6 | `exit_gate.py`, `host_adapter.py`, `host_probe.py` | нет |
| W2 | HF4-7 | `contract.py` (функции §5.2), `planning_contract.py` (`case_entry_answers`, `variant_errors` — ветка кейсов, `_claim_key_errors`), `gate_brief.py` (`_then_effect`, `question_effects`) | `gate_brief.py`, `planning_contract.py`, `qa-requirements-tester.md` с W3 — функции/строки разные; `contract.py` с HF4-3 (`rollup_status`) и HF4-10 (форма окна) — функции разные |
| W3 | HF4-8 → HF4-9 | `gate_brief.py` (`contradiction_questions`, `_decided_lines`), `planning_contract.py` (новые функции), `question_register.py` (`raise_for_case`) | с W2 — функции разные |
| W4 | HF4-10 | `window_record.py`, `acceptance.py`, `coverage_contract.py`, `controller.py` (`_s5_collect`, `_code_review_refusal`), `report_facts.py` (одна функция) | `controller.py` — горячий: функции названы; `contract.py` с W2 — функции разные |
| W5 | HF4-5 (существующий) | `probe_by_code.py` | нет |
| W6 | HF4-1 (существующий; цепочка HF4-1 → HF4-3 → HF4-4 по `contract.py`/`case_stamp.py`/`check_coverage.py`) | `check_coverage.py`, `case_stamp.py`, `ledger.py` | нет с новыми |

Волна 2 (по освобождению слотов): HF4-3, HF4-2 (после строк спеки Lead), HF4-4, HF4-11.
Порядок слияния по общим файлам: `gate_brief.py`, `planning_contract.py`: W2 и W3 (и HF4-11 в `gate_brief.py`) — поздний сливает
`main` в своё дерево, пины обеих сторон зелёные, один критик после слияния (PROJECT.md «Командная работа» п. 3). Свидетель каждого
узла — только его точечные файлы (D-0056); BATCH CANON — интегратор, один раз.

## 5. Узлы

Общее для каждого диспатча билдеру (R11-f, шапкой вне блоков): `given:` = этот файл §5.n + `design/factory-rules.md` целиком +
`plans/builder-rules.md` + `design/architecture.md` (названные AR-n) + `docs/SIBLING_MAP.md` (названные оси) + фикстурные источники
узла; `handoff:` = `D:/ws1/yml-text-factory\docs\tasks\handoffs\t-nnn-hf4-n.md` (t-nnn выдаёт Lead). Отчёт билдера несёт: проход
FR по разделам, строки «axis N: …» по названным осям, `code_friction` до/после или «не измерено», для каждой мутации — одна строка
теста, которая её убивает, и сам мутант (одна строка), «needed beyond the manifest». Фикстура со стенда: копируется только нужное,
**кириллица заменяется английской заменой той же формы** (FR-30, `selftest.py --lang`), id, хэши и структура полей сохраняются;
в `README.txt` фикстуры — исходный путь на стенде и что заменено. Секреты, подписи thinking, строки `api-request*` не копируются.

### 5.1 HF4-6 — последнее слово роли читается из её собственного транскрипта

**owns:**
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\exit_gate.py` (`handoff_digest`)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\host_adapter.py` (новая функция `assistant_row_texts`)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\host_probe.py` (`_assistant_texts` — вызов новой функции, поведение то же)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_exit_gate_digest_source.py` (новый)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_s1_s2_contract.py` (`the_digest_is_read_from_the_transcript` — только если ключ нейтрального контроля требует)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\fixtures\run-12586-digest\` (новый каталог)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\changelog.d\hf4-6-digest-source.md`
`D:/ws1/yml-text-factory\docs\SIBLING_MAP.md` (ось 22, строка «Readers of the form»: добавить `exit_gate.handoff_digest`)

**given (сверх общего):** `exit_gate.py:614-660, 786-826, 1423-1475`; `host_probe.py:474-520`; `host_adapter.report_forms`;
`references/host-report-forms.json`; `cost_capture.py:3008-3041`; источник фикстуры — транскрипты стенда:
`C:\Users\dev1\.claude\projects\D--ws-testproject1-dev-010-testproject1-sdk-test-harness\22686563-d408-46cd-b461-7c3b276d6746\subagents\agent-a19dac213a6228a50.jsonl`
(строки 75–76) и родитель `…\22686563-d408-46cd-b461-7c3b276d6746.jsonl` (последняя строка `type: assistant` с текстом до момента
строки 75); журнал прогона `D:/ws1/testproject1-dev-010\testproject1-sdk\test-harness\qa-factory\records\journal.jsonl` строки 17, 31, 56.

**Что сделать.**
1. `host_adapter.assistant_row_texts(row, forms) -> list[str]`: тексты ОДНОЙ строки транскрипта, обе формы хоста — Claude `type:
   assistant` + `message.content` (текстовые блоки и строковые входы вызова, чьё имя — `forms["claude"]["handback_tool"]`), Codex
   `response_item` + `payload.role == "assistant"`; не-assistant строка → `[]`; строка не-объект → `[]` (строгость остаётся у
   вызывающего). Имя инструмента возврата не пишется в код (ось 22, `test_host_adapter.py` уже это ловит).
   `host_probe._assistant_texts` строится на ней, его строгий режим (ValueError на нечитаемой строке) и вердикты не меняются.
2. `exit_gate.handoff_digest(event)` — порядок источников (ПОЗИЦИЯ и её ИНВАРИАНТ ниже):
   (1) событие несёт `agent_transcript_path` → последнее непустое слово роли из ЭТОГО файла (хвост 400 строк, обратный проход,
   строки, которые не JSON, пропускаются, как сегодня); (2) иначе — `last_assistant_message`, если это непустая строка;
   (3) иначе — `transcript_path` тем же разбором (сегодняшнее поведение для хоста без `agent_transcript_path`).
   Если (1) есть, но файл отсутствует / нечитаем / в хвосте нет слова — ответ `""` и одна строка stderr «the role's own transcript
   could not be read (<why>); its digest is not judged and not filed», **никогда** не переход к (3).
   ИНВАРИАНТ позиции: при наличии `agent_transcript_path` текст файла родителя недостижим как слово роли — ни для формы, ни для
   `is_halting_handoff`, ни для подачи в `work/digests/`.
3. Последнее слово — тексты последней строки-assistant, у которой они есть (текст и/или вход handback), соединённые `\n`, обрезка
   4000 символов (как сегодня).

**Края (поведение и защищаемый инвариант).**
- Нет ни одного пути → `""` (как сегодня): форма не судится, `finish --digest -` спросит строку дайджеста. Инвариант: неизвестный
  автор не получает отказа за чужой текст (FR-41, FR-2); объявленный безопасный дефолт — «не судить и не подавать», не «прошло»:
  без поданного файла `finish` не примет хэндовер молча (AR-28).
- Файл ребёнка есть, последняя строка — `tool_result` (`type: user`) после handback → пропускается, берётся строка handback.
  Инвариант: ответ хоста на возврат — не слово роли.
- Последняя строка-assistant — вызов другого инструмента без текста → обратный проход к предыдущей строке с текстом (как сегодня).
- Предел хвоста 400 строк: слово роли на 400-й строке с конца читается (ключ AT), на 401-й — нет → `""` + stderr (ключ BEYOND).
  Инвариант: за пределом — «не судится», не «судится по чужому».
- Частичная последняя строка (запись ещё идёт) → пропуск строки, как сегодня. Инвариант: обрыв не превращает слово роли в чужое.
- Строка-не-объект в хвосте (`[1]`, `"x"`) → пропуск.
- `agent_transcript_path` не строка (`5`, `null`) → считается отсутствующим путём ветки (1): `""` + stderr, без перехода к (3).
- Halt: handback с `qa-scout S1 halt · …` → `is_halting_handoff` истина; проза родителя со строкой вида `qa-scout S1 halt` при
  наличии пути ребёнка — не halt роли.
- Codex: событие с `agent_transcript_path` на собственный rollout ребёнка — читается тем же путём (1), Codex-форма строки
  `response_item`; это НОВОЕ поведение (сегодня Codex-rollout разбором Claude даёт `""`) — **развилка F-2**.
- Прогон, начатый на 0.10.3 и продолженный на 0.10.5: состояния нет, меняется только чтение следующих остановок.

**Направление ошибки переиспользуемой функции** (`assistant_row_texts`: советчик пробы → вход гейта): ошибаться можно только в
сторону «слова нет» (`""` → не судится, `finish` спросит). Неудобные входы, которые обязаны остаться на безопасной стороне: пустой
вход handback; вход handback — не строка (словарь, число); два текстовых блока + handback в одной строке; инструмент с похожим, но
не точным именем (`SubagentHandbackX`) — НЕ слово роли; файл данных форм нечитаем → `report_forms` даёт `(None, reason)` → входы
вызовов не читаются, читаются только текстовые блоки (сегодняшний минимум), строка stderr.

**Ключи приёмки.**
- K1 (стык): фикстура `run-12586-digest/` — `event.json` (SubagentStop: `transcript_path` → `parent.jsonl`, `agent_transcript_path`
  → `subagents/agent-a19dac213a6228a50.jsonl`, `agent_type: qa-factory:qa-case-critic`), `parent.jsonl` (хвост родителя: последняя
  assistant-строка — проза дирижёра, переведённая на английский), файл ребёнка (строки 75–76 стенда, очищенные). `handoff_digest`
  возвращает ровно вход handback строки 75.
- K2 (стык, измерение до теста): `role_digest.check(<K1 digest>, ["TC-014"])` — билдер ПЕРВЫМ ходом печатает результат; ожидается
  `[]`. Если не `[]` — стоп и строка отчёта (это находка о форме роли, не правка теста).
- K3: тот же event без `agent_transcript_path` → прежний разбор `transcript_path` (нейтральный контроль, ключи
  `test_s1_s2_contract.py` зелёные без правки).
- K4: путь ребёнка на несуществующий файл → `""` и stderr; текст родителя не возвращён.
- K5: предел 400 — AT и BEYOND.
- K6: halt в handback → `is_halting_handoff` истина; проза родителя с halt-строкой при пути ребёнка → ложь.
- K7: `last_assistant_message` читается только без `agent_transcript_path`.
- K8: неудобные входы из абзаца «направление ошибки» — каждый `""`/только тексты.
- K9: `host_probe` — его тесты зелёные без правки ожиданий.

**DoD (свидетель, cwd `ai-packages/qa-factory` worktree):**
`python -B scripts/tests/test_exit_gate_digest_source.py` ; `python -B scripts/tests/test_s1_s2_contract.py` ;
`python -B scripts/tests/test_host_adapter.py` ; `python -B scripts/tests/test_host_probe_handback.py` ;
`python -B scripts/selftest.py --lang` (фикстура со стенда).
Мутации (назвать убивающий ключ): вернуть `event.get("transcript_path")` первым → K1/K4; убрать чтение входа handback → K1;
перейти к (3) при нечитаемом (1) → K4.

**FR-проход:** A (FR-1, FR-2: отказ формы адресован автору текста; FR-4), C (FR-11, FR-14: форма возврата хоста — контракт),
D (FR-17: инструмент оси 22 подключён к последнему сайту; FR-59), F (FR-41, FR-55: −17 пробуждений на прогон — назвать как
ожидание, замер — живой прогон), G (FR-30 фикстура, FR-32, FR-33 — живое доказательство в строке пачки).
**Оси:** 22 (новый читатель формы — строка оси тем же коммитом), 14 (пакет читает транскрипт ребёнка сам — пакет не импортирует
`tools/`; двойник `host_probe` назван), 5 (двойник: `story_step._digest_of` читает поданный файл — не меняется, назвать).
**non-goals:** форма дайджеста ролей, `role_digest.canonical`, цена блока (SC2-27 остаток), Codex-доводка сверх F-2.

### 5.2 HF4-7 — ответ на before/now-вопрос связан с текстом Then по смыслу чтения (ревизия 2, t-1472 B7-1…B7-3, N7-1…N7-5)

Решение F-1 (а) (§11). Узел НЕ трогает функции HF4-8/HF4-9 (`contradiction_questions`, `_decided_lines`, `register_fork_questions`,
`raise_for_case`, писатель `question_refs` строки) — они строятся сейчас по §5.3/§5.4.

**owns:**
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\contract.py` (`claim_readings`, `claim_confirmed`, `before_value_needed`, `resolve_then_oracle`, `then_oracle_errors`, новые `CLAIM_KEYS`, `claim_reading_index`, `question_then_keys`, `question_then_text`)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\planning_contract.py` (`case_entry_answers`; `variant_errors` — только ветка кейсов: счёт `resolved`, `missing`, `extra`; новая `_claim_key_errors`)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\gate_brief.py` (`_then_effect`, `question_effects`)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\gate_preflight.py` (только вызов у `:1319` в проверке вопросов, если п. 5 (ii) его требует; иначе не трогается)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\agents\qa-case-designer.md` (шаг 5, одна строка)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\agents\qa-requirements-tester.md` (шаг 8, одна строка — не та, что пишет HF4-8)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\references\artifact-contract.md` (абзац `question_thens`)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\references\artifact-contract-json.md` (абзац readings вопроса)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\references\slices\` (только то, что перегенерирует `python -B scripts/contract_slices.py --write` из двух абзацев выше)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_question_thens_claim_keys.py` (новый)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\fixtures\run-12586-q7\` (новый)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\changelog.d\hf4-7-claim-keys.md`

**given (сверх общего):** `contract.py:520-700, 840-1205`; `planning_contract.py:1175-1215, 1425-1525, 2200-2240`;
`gate_brief.py:1925-2129`; `gate_preflight.py:1300-1335`; `question_register.py:980-1120` (`_raise`, `raise_for_case` — читать, не
править); `critic_rollcall.py` `--apply-fixes` (шаг выхода S4, `story_run.py:8524-8529`); `references/artifact-contract.md:96-134`;
`agents/qa-case-designer.md:45-60`; `agents/qa-requirements-tester.md:98-112`; критик `docs/tasks/specs/reviews/t-1472-hf4-plan-critic.md`
§ HF4-7; источники фикстуры — стенд `…\TP1-12586\work\requirements-readiness.json` (Q5 — ролью, Q7 — кодом), `…\work\test-cases\cases\TC-014\cv_998932e2dc6129302ba7.md`
(версия `raise`), `cv_b3406f0980d40df314bc.md` (версия гейта A), `…\work\gate-a-brief.txt:25-40` (карточка Q7).

**Что сделать.**
1. `contract.CLAIM_KEYS = ("now", "before")` — один носитель порядка before/now-чтений рядом с `claim_readings`; `claim_readings`
   пишет в каждое чтение поле `claim` (`now` первым, `before` вторым — порядок прежний).
2. Кейс для before/now-вопроса (вопрос с `before`/`now`, или `raise`) пишет `question_thens[].readings` ключами `now`/`before`
   (не буквами). Роль узнаёт это до работы (AR-10): одна строка в `qa-case-designer.md` шаг 5, абзац и пример в
   `artifact-contract.md` (`{"question": "raise", "then": 1, "readings": {"now": "…", "before": "…"}}`); потолок 9000 байт роли —
   добавленное компенсируется (builder-rules п. 5, A22).
3. **Один читатель** (B7-1, правило 18): `contract.claim_reading_index(question, key) -> int | None` — позиция чтения с данным
   смыслом (п. 5); `contract.question_then_keys(question) -> list` — `["now","before"]` для before/now-вопроса и для `raise`, буквы
   чтений для прочих; `contract.question_then_text(question, entry, answer) -> (text | None, why)` — буква ответа → чтение вопроса →
   ключ записи → текст. Его зовут `gate_brief._then_effect`, `contract.resolve_then_oracle` (вместо `readings.get(letter)`) и
   `planning_contract.case_entry_answers`, которая становится тонкой обёрткой над ним (сигнатура получает вопрос; её docstring
   «THE one reader» остаётся правдой: она — единственная дверь `variant_errors` и `_case_rework`). Второй реализации «есть ли у
   записи текст ответа» нет. `variant_errors` (ветка кейсов) считает `resolved`, `missing`, `extra` по `question_then_keys`.
4. Сосед-класс «буква = смысл before/now» (N7-2): `claim_confirmed` (через `CLAIM_INTENDED = "a"`), `before_value_needed`
   (`reading == "b"`) и ветка O2 резолвера (`letter == "b"`) спрашивают букву смысла через `claim_reading_index` (буква = позиция
   найденного чтения); `None` → `claim_confirmed` ложь, `before_value_needed` истина, O2 — `open` с причиной. Константа
   `CLAIM_INTENDED` остаётся только как значение по умолчанию для пары, распознанной по п. 5 (i). Ветка O2 по-прежнему берёт
   `before.value` (расхождение с текстом записи `before` — очередь, §6).
5. **Какое чтение — «now»** (B7-3, переписано целиком). (i) Вопрос, у которого чтения несут `claim` — по полю. (ii) Вопрос без
   `claim`, чьи тексты чтений РАВНЫ байт в байт `claim_readings(before.value, now.value)` (все поднятые кодом: `raise_for_case`,
   `claim_projector`) — по позиции этой пары: её порядок задаёт код, это проверка равенства, не угадывание. (iii) Прочие (ролью
   написанные на S2, как Q5 стенда) без `claim` → `claim_reading_index` = `None`, `question_then_text` = `(None, "the question does
   not mark which reading is the behaviour now")`; карточка печатает «no text is written for this answer» с этой причиной; репетиция
   гейта A (существующий маршрут `question_errors`, вызов `gate_preflight.py:1319`) называет находку тестировщику требований ТОЛЬКО
   когда кейс держит запись с ключами `now`/`before` на этом вопросе — условие — данные, без даты среза (носителя даты у
   `before_now_errors` нет). (iv) Роль S2 узнаёт поле до работы: одна строка в `agents/qa-requirements-tester.md` шаг 8 и абзац в
   `artifact-contract-json.md` — `claim: now|before` у каждого чтения before/now-вопроса.
6. Проверка формы кейса — **отдельной функцией** `planning_contract._claim_key_errors(item, question)` (не ещё одной ветвью цикла
   `variant_errors`, ~330 строк): запись before/now-вопроса с буквенными ключами → находка `factory_fixable`, владелец — дизайнер
   кейсов, текст: что не так («letters on a before/now question: the reading order is fixed by the factory, not by the case»), что
   ожидается (ключи `now`/`before`), дверь — переработка кейса дизайнером (маршрут находок `question_branches`); слово человека
   проходит её, как прочие находки этой проверки. Запись с ключами `now`/`before` для вопроса БЕЗ before/now → та же находка
   зеркально. ПОЗИЦИЯ (N7-3): проверка стоит ПОСЛЕ ранних выходов `settled`/`resolved` (`planning_contract.py:1475-1483`).
   ИНВАРИАНТ: отвеченный вопрос наследия новой находки не получает.
7. Ранняя дверь (N7-1): запись `question_thens` с `"question": "raise"` и буквенными ключами — ошибка FORM в
   `contract.then_oracle_errors` (валидатор при записи кейса, он уже получает `raw_question_thens` и знает `raising`); дверь — та же
   строка `question_thens` с ключами `now`/`before`. Для поднятого вопроса — п. 6.

**Края.**
- Кейс без `question_thens` — никогда не отказ (как сегодня, `artifact-contract.md:109`).
- Обычный (не before/now) вопрос — буквы как сегодня; ключи `now`/`before` там — находка п. 6.
- Ответ своими словами (без буквы) — текста нет, ветка резолвера «own wording» не меняется.
- `not_needed` — прежний путь (`entry["not_needed"]`).
- Наследие, вопрос ОТКРЫТ, кейс с буквами на before/now-вопросе (прогон начат на 0.10.3): карточка НЕ ставит текст под букву,
  печатает тексты записи без привязки с причиной, репетиция гейта A называет находку п. 6 (переработка кейса до показа человеку) —
  F-8 (а). Инвариант: текст Then никогда не показывается под чтением, для которого он не написан. (Позиция п. 6 «после
  `settled`/`resolved`» сюда не мешает: вопрос открыт.)
- **Наследие, вопрос отвечен БУКВОЙ, запись кейса с буквенными ключами** (B7-2): `question_then_text` читает по букве, как сегодня
  (`readings[letter]`) — человек выбирал по карточке, где под этой буквой стоял именно этот текст. Только для `settled` вопроса.
  Инвариант: ответ, уже данный на показанный текст, не теряет силу из-за обновления; `resolve_then_oracle` и `case_entry_answers`
  на этом входе дают одно и то же (`settled` / `resolved`) — расхождения двух читателей нет (FR-10).
- Наследие, вопрос отвечен СВОИМИ СЛОВАМИ (прогон 12586: Q7, TC-014 переписан в `person:Q7`, `question_thens` нет): ничего не
  меняется, повторного вопроса нет.
- Вопрос с одним из `before`/`now` — уже отказ `before_now_errors`; без изменений.
- Ключи обоих видов в одной записи (`{"a": …, "now": …}`) → находка п. 6 (смешение).
- Поле `claim` с неизвестным словом (`"later"`) или два чтения с одним `claim` → `claim_reading_index` = `None`; карточка — «no
  text», не угадывание.
- Пара, «почти равная» `claim_readings` (лишний пробел, другой `before.value`) → п. 5 (iii), не (ii).

**Направление ошибки** (`question_then_text`/`claim_reading_index` — новый вход четырёх читателей, в т.ч. резолвера, который ставит
оракул теста, и `variant_errors`, который шлёт доработку): только в сторону «текста нет / оракул открыт» для ответа, который ещё не
дан, и «как показано» для ответа, который дан (B7-2). Неудобные входы, остающиеся на безопасной стороне: before/now-вопрос с
переставленными в регистре чтениями, но верными `claim` — текст по `claim`, не по позиции; ролью написанные чтения без `claim` —
`None`; три чтения у before/now-вопроса — `None`; буква за пределом чтений (`c`) — `None`; ключ записи в другом регистре (`Now`) — не
совпадает (как записано), `None`; тексты пары, отличающиеся на один байт от `claim_readings` — не распознаны как пара кода.
Что код НЕ ловит и почему: дизайнер может положить текст «4xx» под `now` — смысловое расхождение текста с чтением судит критик
кейсов (FR-12, FR-47); ключ теста этого не покраснит — названо честно.

**Ключи приёмки.**
- K1 (стык через настоящий шаг выхода S4, N7-4): каталог истории-фикстуры с регистром/readiness стенда и версией `raise` кейса TC-014,
  у которой ключи переписаны руками на новую форму (`now`: «…answers 2xx and the integration is in the target», `before`: «…rejected
  with 4xx…») — новой формы роли ещё не существует, это названо в README фикстуры и в строке живого доказательства FR-33 →
  `python -B scripts/critic_rollcall.py --apply-fixes --task-root <фикстура>` (поднимает Q7 через `claim_readings`, пишет кейс) →
  `gate_brief.question_card(Q7, …, question_effects(…))`: под `a)` (Intended now) стоит текст 2xx, под `b)` — 4xx.
- K2 (стык, красный на прогоне): версия гейта A (`cv_b3406…`, буквы на Q7) + `requirements-readiness.json` стенда, Q7 открыт →
  `variant_errors` даёт находку п. 6 с именем TC-014, Then 1, Q7; версия `raise` с буквами (`cv_998932…`) → `then_oracle_errors` даёт
  ошибку FORM п. 7.
- K3: `resolve_then_oracle` для Q7, ответ `a`, запись с ключами → `expected` = текст `now`.
- K4: обычный вопрос Q1 с буквами — без изменений (контроль).
- K5: неудобные входы из абзаца «направление ошибки» — каждый `None`/«no text».
- K6: наследие — (а) открытый вопрос, буквы → карточка без привязки + находка п. 6; (б) вопрос отвечен буквой `a`, запись с буквами →
  `resolve_then_oracle` = `settled` с `readings["a"]`, `case_entry_answers` = resolved, `variant_errors` = `[]` (B7-2); (в) отвечен
  своими словами — без изменений.
- K7: текст ролей — ключ-присутствие в `agents/qa-case-designer.md`, `agents/qa-requirements-tester.md`, `references/artifact-contract.md`,
  `references/artifact-contract-json.md` (`now`, `before`, `claim`) с отрицательным контролем (DOC-DISPATCH WITNESS: ключи из этой
  спеки, скрипт в тесте, контроль с удалённым ключом красный).
- K8 (B7-1): Q7 с новой формой, ответ `a` → `variant_errors` = `[]`, `_case_rework` = `[]`; открытый Q7 с новой формой → ни
  `missing_reading_text`, ни `bad_branch`.
- K9 (п. 5): Q5 стенда (ролью, без `claim`) + кейс с ключами `now`/`before` на Q5 → находка тестировщику требований из репетиции;
  тот же Q5 без такой записи кейса → находки нет; Q7 стенда (кодом, без `claim`) → распознан по равенству пары, `now` = позиция 0.
- K10 (N7-2): `claim_confirmed`, `before_value_needed`, O2 на Q5 без `claim` → безопасная сторона (не подтверждено / открыто).

**DoD:** `python -B scripts/tests/test_question_thens_claim_keys.py` ; `python -B scripts/tests/test_oracle_provenance.py` ;
`python -B scripts/tests/test_gate_question_form.py` ; `python -B scripts/tests/test_question_branches.py` ;
`python -B scripts/tests/test_validators.py` (п. 7 — валидатор при записи) ;
`python -B scripts/selftest.py --limits --lang --slices` (роли и референсы тронуты, слайсы перегенерированы).
Мутации: `_then_effect` снова `readings.get(answer)` → K1; `case_entry_answers` снова `readings.get(key)` → K8; `claim_readings` без
`claim` и без п. 5 (ii) → K1/K3; снять находку п. 6 → K2; поставить п. 6 до `settled` → K6 (б); убрать ветку наследия B7-2 → K6 (б).

**FR-проход:** B (FR-6, FR-10: карточка и резолвер не противоречат друг другу и себе), C (FR-11, FR-12, FR-13, FR-38 — для обеих
ролей, FR-14), D (FR-58, FR-59), E (FR-37 не задет — путей нет), G (FR-30, FR-32, FR-33). **Оси:** 5 (строка «requirement»: карточка
гейта A ↔ резолвер S5/отчёта ↔ применитель ↔ `variant_errors` — один читатель), 21 n/a (таблицы не читаются). **non-goals:**
обычные вопросы (F-1 (б)/(в)); расхождение ветки O2 (`before.value`) с текстом записи `before` (N7-5 — строка пачки, §6); рубрика
критика кейсов; функции HF4-8/HF4-9.

### 5.3 HF4-8 — гейт A не переспрашивает R-n, закрытые ответом Qn; «Already decided» печатает Qn

Описан под рекомендацию F-3 (а).

**owns:**
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\gate_brief.py` (`contradiction_questions`, `_decided_lines`, функция, собирающая `data` для них)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\planning_contract.py` (новая `register_fork_questions`)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\references\templates\requirements-register.md` (`## Reading forks`)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\references\artifact-contract-plan.md` (строка о `Decision`)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\agents\qa-requirements-tester.md` (одна строка)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_gate_a_settled_forks.py` (новый)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\fixtures\run-12586-gate-a\` (новый)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\changelog.d\hf4-8-settled-forks.md`

**given (сверх общего):** `gate_brief.py:1590-1678, 2300-2357`; `planning_contract.py:834-962` (`register_contradictions`,
`register_contradiction_readings`); `question_register.py:280, 365-392, 872-892`; ось 21 (`project_decisions._cells`); источники
фикстуры — стенд `…\TP1-12586\work\requirements-register.md`, `…\work\requirements-readiness.json`,
`…\work\question-answers.jsonl` (слова — на английский), `…\work\test-plan.json` (строки TS-1, TS-2, TS-8, TS-14), `pipeline.json`
прогона (решения), `…\work\gate-a-brief.txt` (как было).

**Что сделать.**
1. `planning_contract.register_fork_questions(register_text) -> {R-n: [Qn, …]}`: строки `## Reading forks`, ячейка `Decision`
   читается одним читателем ячеек (ось 21); id вопроса — только целым id регистра по правилу `_mentions` (`Q1` не в `Q10`), фразы
   «adopted» и прочее не читаются (FR-12).
2. `contradiction_questions`: строка плана пропускается, когда КАЖДОЕ её противоречивое `R` (`named`) закрыто: развилка `R` называет
   вопросы и все они `question_register.settled`, ИЛИ текст решений называет `R` (сегодня), ИЛИ все `question_refs` строки
   резолвятся (сегодня). Иначе карточка строится по ПЕРВОМУ незакрытому `R` (сегодня — по `named[0]`).
3. «Already decided by you»: после пропусков — строки закрытых вопросов из `question_register.answers_for_brief`:
   `- Qn: <reading_text> (your answer at <where>)` при букве, `- Qn: "<words>" (your words at <where>)` без буквы; слова сжимаются
   пробелами и режутся до 160 символов с `…`; до 10 строк, затем `- (+K more — work/question-answers.jsonl)`. Секция печатается и
   тогда, когда кроме ответов ничего нет. `answers_for_brief(...)["unreadable"]` → одна строка «some of your earlier answers could
   not be read; questions they settle are shown again below» и пропуск п. 2 по этим вопросам не делается.
4. Контракт S2: шаблон и `artifact-contract-plan.md` говорят, что `Decision` развилки, закрытой вопросом, начинается с id этого
   вопроса (`Q1 b adopted: …` — как на стенде), открытой — `question at gate A`; одна строка роли.

**Края.**
- Регистр без `## Reading forks` / ячейка без id / таблица нечитаема → пусто; поведение сегодняшнее (карточка). Инвариант:
  развилка, на которую человек не ответил, задаётся (FR-41 направление — «спросить»).
- Ячейка с двумя id (`Q3 b, Q6`) → закрыта, когда закрыты ОБА.
- Id в ячейке, которого нет в регистре вопросов → не закрывает.
- Вопрос `deferred_to_report`, `with_designer`, изменённый после ответа (`changed_since_answer`) → не `settled` → `R` задаётся.
  Инвариант: ответ на другой текст вопроса не закрывает новый текст (H41).
- Строка с `oracle_unknown`, у которой нет противоречивых `R` (TS-14) — сегодняшний путь («no settled expected value»), её закрывает
  HF4-9.
- Строка, у которой закрыта часть `R` (TS-8 на стенде: R-1 → Q4, R-4 → Q3 закрыты; у R-2 развилки нет) → карточка по `R-2`.
  Инвариант: противоречие, о котором человека не спросили, не исчезает из-за соседнего ответа.
- Предел 10 строк «Already decided»: 10 — все строки, без хвоста (AT); 11 — 10 строк и `(+1 more …)` (BEYOND). Предел 160
  символов слов: 160 — целиком, 161 — 160 + `…`.
- Бриф обрезается на 85 строках (сегодня, `gate-a-brief.txt:85`): секция «Open questions» стоит раньше «Already decided», поэтому
  обрезка не может выбросить открытый вопрос ради строки решённого (инвариант порядка; ключ на брифе длиннее предела).
- Прогон в полёте (12586 на 0.10.3, прошёл гейт A): гейт A не повторяется; гейт B этих карточек не строит (проверить grep
  `contradiction_questions` — ключ K6). Повторных вопросов на возобновлении нет.

**Направление ошибки** (`question_register.settled` и `_mentions` в новой, гейтовой роли «не спрашивать»): только в сторону
«спросить». Неудобные входы, которые обязаны оставить вопрос: `Q1` в ячейке при вопросе `Q10`; `Q-1`; `q1`; id внутри пути
(`work/Q1.md`); вопрос `answered` с нечитаемым `row_hash`; строка ответа с битым JSON в `question-answers.jsonl`; `status: answered`
без `at`.

**Ключи приёмки.**
- K1 (стык): фикстура стенда (регистр, readiness, ответы, строки плана) → `contradiction_questions` возвращает ровно `{R-2 (TS-8),
  TS-14}`; до правки — `{R-3, R-5, R-1, TS-14}` (записать «было» в тест как контроль на старой функции не нужно — ключ «было» —
  `gate-a-brief.txt:41-65` в фикстуре).
- K2: отрицательный контроль — из ответов убран Q1 → `R-3` снова задаётся.
- K3: бриф фикстуры — «Already decided» содержит Q1…Q7 (Q7 — словами), ни одного `R-3`/`R-5`/`R-1` в «Open questions».
- K4: края п. «Края» и «Направление ошибки» — по ключу на каждый.
- K5: пределы 10/11 и 160/161.
- K6: grep `contradiction_questions` по `scripts/` (контроль — находится сама функция) — список вызывающих в отчёте.
- K7: ключ-присутствие в шаблоне и контракте (DOC-WITNESS с отрицательным контролем).

**DoD:** `python -B scripts/tests/test_gate_a_settled_forks.py` ; `python -B scripts/tests/test_gate_brief_and_retro.py` ;
`python -B scripts/tests/test_question_register.py` ; `python -B scripts/selftest.py --limits --lang`.
Мутации: убрать проверку `settled` (закрывать по одному упоминанию) → K2/K4 (`deferred`); `named[0]` вместо первого незакрытого → K1
(R-1 вместо R-2); убрать строку «unreadable» → K4.

**FR-проход:** B (FR-6, FR-7, FR-8, FR-10), C (FR-12, FR-13, FR-38: поле `Decision` сказано роли до работы), D (FR-59),
G (FR-30). **Оси:** 21 (новый читатель таблицы — через `_cells`), 5 (двойник гейт A ↔ гейт B: секция «Already decided» гейта B —
назвать, изменить или «не применимо: <почему>»). **non-goals:** GW1-27…GW1-32; GW1-21/HF2-7 (сам маршрут ответов); поле
`decision_refs` стратега (аналог §9 п. 4 — в очередь).

### 5.4 HF4-9 — поднятый на S4 вопрос попадает в строку плана; дубль TS-n/Qn уходит

Тот же билдер, что HF4-8, после него. Часть «строка после ответа» — по F-4.

**owns:**
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\question_register.py` (`raise_for_case`)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\planning_contract.py` (новая функция добавления `question_refs` строки через писателя плана; при F-4 (б) — новая функция сверки строки)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_raise_reaches_plan_row.py` (новый)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\fixtures\run-12586-gate-a\` (общий с HF4-8, тот же билдер)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\changelog.d\hf4-9-raise-plan-row.md`

**given (сверх HF4-8):** `question_register.py:980-1120`; `planning_contract.py:1210-1330, 2264-2330`; `scripts/plan_row.py`;
`references/artifact-writers.json` (кто пишет `test-plan.json`); стенд `cv_998932e2dc6129302ba7.md` (кейс с `raise`, `plan_row:
TS-14`).

**Что сделать.**
1. Билдер ПЕРВЫМ ходом называет в отчёте одного писателя `work/test-plan.json` по `references/artifact-writers.json` и как
   код (не стратег) в него пишет (`apply_gate_answers` / `plan_row.py`) — новая запись идёт только через него (AR-14).
2. `raise_for_case`: подняв `Qn` для кейса с `plan_row: TS-n`, добавляет `Qn` в `question_refs` строки `TS-n` (без дублей, порядок
   — добавление в конец), одной записью плана. Ничего больше в строке не меняет.
3. F-4 (после решения Lead).

**Края.**
- Кейс без `plan_row` / строки нет в плане → ничего в план; одна строка результата «Qn was raised for <case>; no plan row names it,
  so the plan is unchanged». Инвариант: подъём вопроса не падает из-за плана.
- План утверждён на гейте A (`pipeline.json`) → в план не пишется (тот же запрет, что у `apply_recorded_answers`), строка
  результата. Инвариант: утверждённый план не меняется кодом.
- План нечитаем / запись не удалась → вопрос всё равно поднят (сегодняшнее поведение), строка с причиной, повтор на следующем
  выходе S4. Инвариант: вопрос никогда не теряется из-за плана.
- `Qn` уже в `question_refs` → без изменений (повторный подъём идемпотентен).
- Строка с `if_answered` без ветки для нового `Qn` → репетиция гейта A покажет `missing_branch` стратегу (существующая находка):
  это ОЖИДАЕМОЕ следствие, назвать в отчёте; если оно даёт лишний диспатч стратега на каждом подъёме — строка отчёта с замером.
- Прогон в полёте (12586): TS-14 уже прошёл гейт A — п. 2 туда не пишет (утверждён).

**Ключи приёмки.**
- K1 (стык): версия `raise` кейса TC-014 стенда + строка TS-14 стенда → настоящий `raise_for_case` → строка TS-14 несёт
  `question_refs: ["Q7"]` → `contradiction_questions` на этом плане НЕ возвращает `TS-14` (карточка только `Q7`).
- K2: утверждённый план — без записи, строка результата.
- K3: нечитаемый план — вопрос поднят, план тот же.
- K4: идемпотентность.
- K5: по F-4.

**DoD:** `python -B scripts/tests/test_raise_reaches_plan_row.py` ; `python -B scripts/tests/test_question_register.py` ;
`python -B scripts/tests/test_plan_row.py` ; `python -B scripts/tests/test_question_branches.py`.
Мутации: не писать `question_refs` → K1; писать в утверждённый план → K2.

**FR-проход:** B (FR-7: один вопрос — одна карточка; FR-10), C (FR-49: собранное доезжает), D (FR-40), G. **Оси:** 8 (писатели
артефактов истории — один писатель плана), 5 (двойник: подъём на S4 ↔ ответ на S2/S3 стопе — оба доходят до строки через
`question_refs`). **non-goals:** смысловая переоценка строки после ответа (стратег; F-4).

### 5.5 HF4-10 — квитанция качества без производителя не требуется; не требуемое видно в отчёте (ревизия 2, t-1472 B10-1, B10-2, N10-1…N10-4)

Решение F-5 (а) + слово Lead 28.10 (ревизия 2): печать в отчёт — В ЭТОМ узле, не отдельной строкой пачки (§11).

**owns:**
`D:/ws1/yml-text-factory\ai-packages\qa-factory\references\quality-receipt-producers.json` (новый)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\window_record.py` (блок сборки окна `:940-957`, `receipt_dict` `:1177` — перенос нового поля, новая `demanded_quality_checks`)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\acceptance.py` (`validate_window`, строки требования `:816-824`)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\coverage_contract.py` (`witnessed_binding` `:230-248` и строка `witnessed` `:555`)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\controller.py` (`_s5_collect`, `_code_review_refusal`)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\contract.py` (только списки полей формы окна у `:3494` и `:3631` — допуск поля `quality_not_run`; функции, не пересекающиеся с HF4-7 и HF4-3)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\report_facts.py` (одна новая функция строки «Quality checks the factory did not run» и её вызов в разделе пробелов отчёта)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\skills\qa-story\phases\s0.md` (строка `:445`)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\references\controller-api.md` (`:89`)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\references\artifact-contract-automation.md` (абзац `quality_receipt_refs` `:136-139`)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\references\slices\qa-automator\artifact-contract-automation.md`, `…\slices\qa-code-critic\artifact-contract-automation.md` (только через `python -B scripts/contract_slices.py --write`)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\references\null-outcomes.json` (строка пустого исхода `quality_not_run`, если реестр требует — AR-23)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_quality_demand.py` (новый)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\fixtures\run-12586-s5-quality\` (новый)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\changelog.d\hf4-10-quality-demand.md`

**given (сверх общего):** места §2 п. 6; `readiness.py:20-70, 960-1000` (список проверок готовности и её запись); `story_run.py:5811-5821,
5848, 8666` и `controller.py:4286-4300` (читать, не править: `revise_plan` переносит поле как есть); `report_facts.py` (раздел пробелов
отчёта — где печатаются строки без вердикта); критик t-1472 § HF4-10; стенд `…\TP1-12586\state\controller.json` (поле
`required_quality_checks`), запись готовности S0 этой истории (путь — через читатель `readiness.py`, см. п. 6), `…\work\windows\S5-qa-code-critic-2.json`,
`…\work\windows\S5-qa-code-critic-3.json`, `…\work\automation-manifest.json` (привязки, OB-1), `…\state\words\s5-20261028-quality-receipts.txt`.

**Что сделать.**
1. Данные (FR-13): `references/quality-receipt-producers.json` — `{"schema_version": 1, "producers": {}, "why": {"no_producer":
   "recorded at initialize; no factory script writes a receipt for it", "checked_at_s0": "checked by the readiness step before the
   story started", "unknown_s0": "the record of the readiness step could not be read"}}`: `producers` — id проверки → скрипт,
   который пишет её квитанцию в окно (сегодня пусто: ни один скрипт не пишет); `why` — слова причин (данные, не код).
2. Один читатель `window_record.demanded_quality_checks(recorded, task_root=None) -> (demanded, not_run, why)`:
   - стоит ДО `str(name)` у `window_record.py:943` (N10-1); id-не-строка → в `demanded` его `json.dumps(id, sort_keys=True)`
     (строка, требуется — безопасная сторона, не падение `unhashable` в `acceptance.py:821`/`controller.py:5880`), строка stderr;
   - строковый id, ТОЧНО (байт в байт, без нормализации регистра и пробелов) присутствующий в `producers` → `demanded`;
   - прочие строковые id → `not_run` как `{"id", "why"}` (п. 6);
   - файл данных отсутствует / битый JSON / `producers` не словарь → `(recorded, [], why)`: требование как записано (объявленный
     безопасный дефолт, AR-28) + строка stderr.
3. Окно: `required_quality_checks` = `demanded`, новое поле `quality_not_run` = `not_run` (всегда пишется, `[]` при пустом — AR-23),
   `quality_receipts: []` остаётся; `receipt_dict` (`:1177`) несёт новое поле рядом с двумя старыми; списки формы окна в
   `contract.py:3494, 3631` его допускают (неизвестное поле сегодня — отказ формы? — билдер первым ходом читает и называет).
4. Читатели окна пропускают список окна через тот же читатель: `acceptance.validate_window` — `quality:<id>` только для `demanded`;
   окно 0.10.3 с четырьмя id читается как `demanded = []`.
   4а (B10-1). `coverage_contract` (оба места: `witnessed_binding :230-235` и `witnessed :555`): при пустом `demanded` окна квитанция
   качества у привязки НЕ требуется — ни `quality_receipt_refs`, ни `quality_not_applicable_reason`; привязка с `quality_receipt_refs`
   при пустом `demanded` — ложь, как сегодня; при непустом `demanded` всё как сегодня (`quality_not_applicable_reason` остаётся
   читаемым: требуемая проверка к обязательству не относится). Инвариант: пустое требование — объявленный исход окна (AR-23), а не
   поле, которое должен придумать автоматор. Абзац `artifact-contract-automation.md:136-139`: id берутся из `required_quality_checks`
   ОКНА; при пустом списке ни `quality_receipt_refs`, ни `quality_not_applicable_reason` не пишутся; слайсы — `contract_slices.py --write`.
   4б (N10-2). `controller._s5_collect` сравнивает `demanded(window)` с `demanded(state)` — фильтр с обеих сторон (окно, собранное
   на 0.10.3 и закрываемое на 0.10.5, не даёт «window cannot omit project quality checks»).
5. `_code_review_refusal`: при пустом `demanded` отказа «not receipted» нет; при непустом — текст называет скрипт-производитель
   из данных (дверь, которой можно воспользоваться, FR-2).
6. **Читатель `quality_not_run` — строка отчёта** (B10-2, слово Lead). Правило **QNR** (одно, в `demanded_quality_checks`, отчёт
   его не повторяет): id попадает в `not_run` с `why = no_producer` и печатается в отчёт, только если (1) у него нет производителя
   И (2) запись готовности S0 этой истории НЕ держит результата проверки с этим именем. Если держит (любой записанный статус:
   `ready`, `not_configured`, …) — `why = checked_at_s0`, в отчёт НЕ печатается (это проверка готовности, выполненная S0, а не
   непрогнанная проверка качества; строка «did not run» была бы ложью, FR-41/FR-10). Если запись готовности нечитаема — `why =
   unknown_s0` и id печатается с этой причиной (неизвестное названо как неизвестное, FR-41; молчание было бы тихим проходом, FR-4).
   Запись готовности читается ТОЛЬКО через её читатель в `readiness.py` (AR-13); билдер первым ходом называет функцию и путь в
   отчёте; если читателя-функции нет — стоп и строка отчёта (развилка назад), второй парсер не пишется.
   `report_facts.py`: одна функция, собирающая `quality_not_run` всех окон S5 истории (через читатель окон, которым отчёт уже
   пользуется), печатает в раздел пробелов отчёта о тестировании одну строку `Quality checks the factory did not run: <id> (<why
   words>), …` для записей с `why` ≠ `checked_at_s0`, id без повторов, порядок первого появления; пустой список — строки нет.
7. Тексты: `s0.md:445` и `controller-api.md:89` — `required_quality_checks` — id проверок качества проекта с производителем
   (`references/quality-receipt-producers.json`), не id готовности; один абзац, без расширения.

**Края.**
- `required_quality_checks` отсутствует/не список в состоянии → для состояния `[]` (как `state.get(..., [])` сегодня); окно без
  поля — `validate_window` бросает ValueError, как сегодня.
- Id не строка → `json.dumps`, требуется, stderr (п. 2). Инвариант: непонятный id никогда не перестаёт требоваться молча и не
  роняет гейт.
- Сравнение точное (N10-3): `Lint` при производителе `lint` — производителя нет, id уходит в `quality_not_run` с `why`; это
  единственный разрешённый путь ошибки «не требовать» (строковый id, точно отсутствующий в словаре).
- Пустой `producers` (сегодня) → `demanded = []` для любых записанных строковых id.
- Прогон в полёте (12586): состояние держит 4 id готовности; следующее окно на 0.10.5 пишет `required_quality_checks: []`,
  `quality_not_run: [4 × {id, why: checked_at_s0}]` (S0 их проверил); `_s5_collect` равенство проходит; принятые окна 0.10.3 при
  перечитывании (S6, coverage) не дают `quality:*`, привязки без полей качества проходят ветку качества; в отчёте строки «did not
  run» НЕТ. Записанное слово человека (пропуск) остаётся в записи и ничего не ломает. Инвариант: возобновление не задаёт этот вопрос
  снова и не печатает ложь.
- Окно 0.10.3 без поля `quality_not_run` → читатель отчёта пересчитывает его из `required_quality_checks` окна тем же читателем
  (`demanded_quality_checks`), не считает «пусто». Инвариант: окно старой сборки не прячет непрогнанную проверку.
- Запись готовности держит проверку под тем же именем с ошибкой (`failed`) → всё равно `checked_at_s0`: S0 её проверил; что делать
  с неготовностью — дело S0/гейта готовности, не этой строки (назвать в отчёте, если встретится).
- Новый прогон, где дирижёр всё же записал id готовности: фильтр отсеет их в `not_run` с `checked_at_s0` — ни требования, ни строки
  отчёта.

**Направление ошибки** (`demanded_quality_checks` — новый фильтр в гейтовой роли): только в сторону «требовать». Неудобные входы,
обязанные остаться требуемыми: файл данных нечитаем / битый JSON / `producers` не словарь → требовать как записано; id, совпадающий
с производителем по букве, — требуется; id не-строка — требуется (как `json.dumps`). Для строки отчёта (правило QNR) направление —
«назвать»: нечитаемая запись готовности → id печатается с `unknown_s0`, а не опускается.

**Ключи приёмки.**
- K1a (стык): состояние стенда (4 id) + окно `S5-qa-code-critic-3.json` стенда → `acceptance.validate_window` до правки содержит
  `quality:ticket_adapter` … (контроль), после — ни одного `quality:*`.
- K1b (стык, B10-1): привязка OB-1 манифеста стенда, дополненная ТОЛЬКО `review_receipt_ref` на окно фикстуры (иначе она ложна по
  другой причине) → `coverage_contract.witnessed_binding` до правки ложь из-за качества (контроль), после — проходит ветку качества;
  `witnessed` (`:555`) — то же.
- K2 (стык, писатель → читатель): `window_record` на фикстуре пишет окно → `controller._s5_collect` без проблемы «window cannot omit
  project quality checks»; окно 0.10.3 (4 id) против состояния 0.10.5 — тоже без проблемы (N10-2).
- K3: данные с производителем `lint` + записанный `lint` → `quality:lint` остаётся пробелом окна; привязка без `quality_receipt_refs`
  при `demanded = [lint]` — ложь (требование живо там, где есть производитель).
- K4: неудобные входы направления ошибки, включая id-словарь (`{"id": "lint"}` → требуется строкой, без `TypeError`).
- K5: `quality_not_run` всегда в окне; `[]` при пустом; `receipt_dict` несёт поле.
- K6: `_code_review_refusal` — нет отказа при пустом требовании; при непустом — текст называет скрипт из данных.
- K7: ключ-присутствие в `s0.md`, `controller-api.md`, `artifact-contract-automation.md` и обоих слайсах (DOC-WITNESS, отрицательный
  контроль).
- K8 (стык, читатель отчёта, B10-2): окна и запись готовности стенда → отчёт фикстуры БЕЗ строки «Quality checks the factory did not
  run» (все 4 — `checked_at_s0`); та же история с записанным `lint` без производителя → строка `Quality checks the factory did not
  run: lint (recorded at initialize; no factory script writes a receipt for it)`; запись готовности удалена → 4 id печатаются с
  `unknown_s0`; окно без поля `quality_not_run` (0.10.3) с id `lint` → строка всё равно есть.

**DoD:** `python -B scripts/tests/test_quality_demand.py` ; `python -B scripts/tests/test_window_record.py` ;
`python -B scripts/tests/test_acceptance_semantics.py` ; `python -B scripts/tests/test_coverage_contract.py` ;
`python -B scripts/tests/test_report_facts.py` ; `python -B scripts/tests/test_null_outcomes.py` (обязательный список окна —
builder-rules п. 7) ; `python -B scripts/selftest.py --slices` (слайсы автоматора и критика кода).
Мутации: фильтр отдаёт `[]` при нечитаемых данных → K4; `_s5_collect` сравнивает с записанным → K2; вернуть `elif not
quality_not_applicable_reason` → K1b; не писать `quality_not_run` при пустом → K5; печатать `checked_at_s0` в отчёт → K8;
опускать `unknown_s0` → K8.

**FR-проход:** A (FR-2, FR-4, FR-5), C (FR-11, FR-13, FR-14, FR-38 — абзац автоматора), D (FR-18: квитанция готовности — не квитанция
окна, поэтому не производитель; FR-59), E (FR-20, FR-35 не задет; строка отчёта под владельцем «фабрика»), F (FR-41: `not_run` не
печатается как «passed», `checked_at_s0` не печатается как «did not run»), G. **Оси:** 5 (двойники приёмки окна: `window_record` ↔
`acceptance` ↔ `coverage_contract` (2 места) ↔ `controller` ↔ `report_facts` — одним коммитом), 23 n/a (поля строки `tests[]` не
меняются). **non-goals:** запуск `quality_gates` проекта (F-5 (в), находка владельцу); `Driver.quality_check_ids` (аналог §9 п. 5);
`revise_plan` (переносит поле как есть).

### 5.6 HF4-11 — `reject` критика кейсов только при падающем кейсе; замечания едут автоматору (ревизия 2, t-1472 B11-1…B11-3, N11-1, N11-2)

Слово владельца 28.10.2026 (F-6 (A), §11): «Если замечания не критические, то они передаются дальше, автоматизатор их учитывает при
автоматизации кейсов». Решения Lead (ревизия 2): носитель замечаний — `s5_plan.remarks_of` (B11-1); два ключа «отказ / проход» без
переписывания слова роли кодом (B11-2, FR-35); петля S4 — вариант (а) критика t-1472, текст роли (B11-3, «решила Lead», §11).

**owns:**
`D:/ws1/yml-text-factory\ai-packages\qa-factory\agents\qa-case-critic.md` (шаг 4 — оба правила; строка слова дайджеста)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\critic_rollcall.py` (`scoped_verdict` — вызов новой `_round_word_rule`; новые `_round_word_rule`, `carried_concerns`)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\s5_plan.py` (`remarks_of`)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\gate_brief.py` (только функция, печатающая строку `**Critic**` у `:2233`; не `_then_effect`/`question_effects` (HF4-7), не `contradiction_questions`/`_decided_lines` (HF4-8))
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\brief_pack.py` (`_placement`/`_ref` — ТОЛЬКО если замечание без `test` не размещается; иначе не трогается)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_carried_concerns.py` (новый)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\test_scoped_review_verdict.py`
`D:/ws1/yml-text-factory\ai-packages\qa-factory\scripts\tests\fixtures\run-12586-concerns\` (новый)
`D:/ws1/yml-text-factory\ai-packages\qa-factory\changelog.d\hf4-11-carried-concerns.md`

**given (сверх общего):** `critic_rollcall.py:236-330` (и `_receipt_offset`, `_round_slice`, `parse_rollcall`, `declared_verdict`);
`s5_plan.py:880-905, 1060-1102`; `brief_pack.py:70-110, 1799-1850`; `s5_precheck.py:2660-2690` (C12, `remark_rows_missing`);
`gate_brief.py:2225-2245`; `story_run.py:8470-8590` (петля S4 — читать, не править); `agents/qa-case-critic.md:50-100`;
`agents/qa-code-critic.md` (двойник оси 5 — читать); критик t-1472 § HF4-11; стенд `…\TP1-12586\work\test-cases\integrations\critic-findings.md`
(раунд 3, `:1-57`: `Verdict: reject`, 11 ячеек одобряющие, замечания измерений 3, 6, 8), `…\work\s5-plan.json`, `…\work\s5-plan-reviews.json`.

**Что сделать.**
1. Роль (N11-1, оба правила шага 4): `approve_with_concerns` — 0 `fail`, любое число замечаний; `reject` — хотя бы один `fail`
   (падающий кейс); остальное без изменений (`partial` при `reviewed: no`, `approve_with_fixes` на последнем раунде). Строка
   дайджеста (B11-3 (а)): при `approve_with_concerns` заголовок дайджеста — `ok`, не `concerns` (замечания едут дальше, раунд
   доработки не нужен); `concerns` в дайджесте — только когда роль сама просит дизайнера переделать (по-прежнему означает
   доработку). Потолок 9000 байт — компенсировать.
2. `critic_rollcall._round_word_rule(rows, declared) -> (basis, reason) | None` (отдельная функция), вызов в `scoped_verdict` ПОСЛЕ
   существующих ранних выходов (`receipt_mismatch`, `two_rollcalls`, нет roll-call, нет `Verdict:`, слово вне списка) и ВМЕСТО ветки
   `:309-312` для случая «заявлено `reject`, в таблице есть колонка `verdict` и НИ ОДНОЙ ячейки `reject` на `reviewed: yes`»:
   слово — `partial` (не `accepted`, не переписанное `approve_with_concerns`), `why` первым — `("round_word_rule", "the round says
   `reject`, and no case of it fails: by the rule a round without a failing case is `approve_with_concerns`; rewrite the `Verdict:`
   line")`. Код слово роли не переписывает (FR-35); дверь — критику: переписать строку `Verdict:` новым раундом сверху (правило
   файла находок). Билдер первым ходом прослеживает, куда `partial` с этим basis идёт на выходе S4 и на гейте A сегодня (контроллер
   `_dispatch_review_verdict`/`_read_findings_ref`), и называет маршрут в отчёте; если маршрут ведёт к человеку, а не к критику — стоп
   и строка отчёта (развилка назад).
3. `critic_rollcall.carried_concerns(data, sha256, receipts=()) -> [{"id": "CC-n", "case", "kind": "remark", "problem", "review"}]`:
   тот же срез раунда, что у `scoped_verdict` (`_receipt_offset`/`_round_slice`/`parse_rollcall` — один разбор, AR-13), строки
   roll-call с ячейкой `approve_with_concerns` на `reviewed: yes`; `problem` — `note` строки дословно (не судится, FR-12 не задет:
   фраза ничего не решает), пустой `note` → `"the case critic marked a concern on this case and wrote no note"`; `review` — id
   диспатча критика; `CC-n` нумеруется по порядку строк. Раунд — тот, чью квитанцию принял гейт A (квитанция одобренных кейсов).
4. `s5_plan.remarks_of` добавляет CC-строки к замечаниям цепочки плана (один читатель для брифа окна и для C12): бриф окна S5
   печатает замечание по своему кейсу, автоматор пишет строку `plan_remarks` `applied` / `not_applicable` и почему, `s5_precheck`
   C12 ловит пропуск — «автоматор учитывает» становится проверяемым. Размещение по `_placement`: если замечание без `test` не
   размещается (`_ref` → `None`), минимальная правка `brief_pack` — размещение по `case` (owns условный).
5. Гейт A: одна строка рядом с `**Critic**` — `Concerns carried to automation: TC-002, TC-004, …` (кейсы `carried_concerns`, без
   повторов, порядок строк); нет замечаний — строки нет.

**Края.**
- Ячейка `reject` (кейс падает) → `reject` всегда, при любом заявленном слове. Инвариант: падающий кейс никогда не одобряется.
- Заявлено `reject`, есть ячейка `reject` → `reject` (сегодня), отказа нет.
- Нет колонки `verdict` → слово раунда на всех строках (сегодняшнее правило), противоречие не видно — отказа нет, `reject` как
  заявлено.
- Строка `reviewed: no` → `partial` раньше (сегодня); `_round_word_rule` не вызывается.
- Слово вне списка / нет `Verdict:` → как сегодня.
- Заявлено `approve_with_concerns`, но ячейка `reject` есть → сегодняшнее правило (строжайшее слово ячеек — `reject`).
- Критик всё ещё пишет дайджест `concerns` при `approve_with_concerns` → петля S4 гонит доработку до капа, как сегодня (цена, не
  корректность); детектор — живое доказательство (число раундов S4 на прогоне).
- Раунд с одними `approve` → CC-строк нет, строки гейта A нет.
- Замечаний много → все CC-строки (предела нет: каждое отрабатывается строкой `plan_remarks`; бриф окна получает только свои кейсы).
- Квитанция раунда не совпадает с файлом (раунд правили) → `carried_concerns` = `[]` и строка stderr; `scoped_verdict` уже даёт
  `partial` с `receipt_mismatch` — замечания не берутся из чужих байтов. Инвариант: квитанция, измеренная на других байтах, не
  считается.
- Прогон в полёте (12586 прошёл гейт A на 0.10.3, окна S5 приняты): `remarks_of` для принятых окон не пересчитывается (новые строки
  задают только неначатые окна); повторных вопросов нет.

**Направление ошибки** (`scoped_verdict` в гейтовой роли получает новый отказ): только в сторону «не `accepted`» — сомнение →
`partial`, никогда `accepted`; новый отказ срабатывает лишь на точном условии «`reject` без единой ячейки `reject`». Неудобные входы:
ячейка `Reject` (другой регистр) — как сегодня читается словом (`_row_outcome`), не считается «отсутствием reject» молча; таблица,
где колонка `verdict` пуста у всех строк — нет ячеек, отказа нет (сегодняшнее правило слова раунда); два раунда в срезе —
`two_rollcalls` раньше. `carried_concerns`: при любом сомнении в срезе — `[]` + stderr (замечание не придумывается).

**Ключи приёмки.**
- K1 (стык, отказ, B11-2): раунд 3 стенда как есть → `scoped_verdict` даёт `partial`, `why[0]` = `round_word_rule` с текстом про
  строку `Verdict:`; не `accepted` и не `approve_with_concerns`.
- K2 (стык, проход, B11-2): тот же раунд с исправленной строкой `Verdict: approve_with_concerns` (остальное байт в байт, новая
  квитанция) → `accepted`.
- K3 (стык, B11-1): раунд K2 + `s5-plan.json`, `s5-plan-reviews.json` стенда → `remarks_of` содержит CC-строки
  TC-002/004/005/007/011/014 → бриф окна с TC-014 печатает её → форма окна без строки `plan_remarks` для неё → находка C12
  `s5_precheck`; со строкой `applied` — находки нет. Отрицательный контроль: раунд с одними `approve` → CC-строк нет.
- K4: гейт A на фикстуре K2 — строка `Concerns carried to automation: TC-002, TC-004, TC-005, TC-007, TC-011, TC-014`.
- K5: края — ячейка `reject` + заявлено `reject` → `reject`; нет колонки `verdict` → без отказа; квитанция не совпадает → `[]`.
- K6: ключ-присутствие правил шага 4 и строки дайджеста в `agents/qa-case-critic.md` (DOC-WITNESS, отрицательный контроль).

**DoD:** `python -B scripts/tests/test_carried_concerns.py` ; `python -B scripts/tests/test_scoped_review_verdict.py` ;
`python -B scripts/tests/test_critic_rollcall_apply_fixes.py` ; `python -B scripts/selftest.py --limits --lang` ; живое доказательство
FR-33 — строка в «Живые доказательства» пачки (S4 прогона без слова человека на капе при одних замечаниях; автоматор отработал CC).
Мутации: `_round_word_rule` возвращает `approve_with_concerns` (переписывает слово) → K1; снять `_round_word_rule` → K1;
`carried_concerns` не добавляется в `remarks_of` → K3; брать `note` из чужого раунда при несовпавшей квитанции → K5.

**FR-проход:** A (FR-1, FR-2: отказ с дверью критику; FR-4), B (FR-6: строка гейта A — текст человеку, форма `human-questions.md`),
C (FR-12, FR-38: правило слова сказано роли до работы; FR-49: собранное S4 доезжает до S5), E (FR-35: код не меняет смысл слова роли),
G (FR-33). **Оси:** 5 (двойник — правило слова критика кода S5 в `agents/qa-code-critic.md`: билдер читает и пишет в отчёте результат —
тот же счёт «≥3 concern → reject» есть / нет / не применимо, и при «есть» — строку очереди; N11-2 — открытый пункт), 17 (форма
отказа — через существующий `why`, без нового парсера). **non-goals:** петля S4 в `story_run.py` (B11-3 (а) — через текст роли);
находки критика кейсов целиком в `ROLE_FILES` автоматора (перенос без проверки — отвергнут t-1472).

## 6. Что нужно Lead до диспатчей (не моё решение, не мой файл)

- Файлы находок для HF4-10 (P5) и HF4-11 (P3) в `plans/piles/hotfix-12586/findings/` (D-0044: узел — строка находки; узлов нет).
- Строки HF4-6…HF4-11 в `batch-4-ostatki-hf3-po-revyu.md`, «Порядок по общим файлам» (+ `gate_brief.py`, `planning_contract.py`:
  HF4-7 ‖ HF4-8/9 (‖ HF4-11 в `gate_brief.py`) по функциям; `contract.py`: HF4-7 ‖ HF4-3 ‖ HF4-10 по функциям;
  `qa-requirements-tester.md`: HF4-7 ‖ HF4-8 по строкам), «Скоуп свидетеля», строки карточки README («Содержание», «Пачки»), строки
  `перенос` (§3).
- Строка пачки (очередь, t-1472 N7-5): ветка O2 `resolve_then_oracle` берёт `before.value`, а карточка печатает текст записи
  `before` — два ответа на «что проверит Then при b» (FR-10).
- Живые доказательства пачки (FR-33): повтор S1–S5 TP1-12586 на `testproject1-dev-010` на 0.10.5 — 0 блоков «not the handoff form» с
  чужим текстом; гейт A без R-1/R-3/R-5; окна S5 без слова о квитанциях; S4 без слова на капе при одних замечаниях, автоматор
  отработал CC-строки; вход HF4-7 новой формы — от живого дизайнера (K1 фикстуры написан руками).
- Критик на план HF4-7, HF4-10, HF4-11 — сделан (t-1472); повторный — решение Lead (критик: не нужен, если правки дословны).

## 7. Развилки (возвращены, не решены)

**F-1 (HF4-7): чем связать текст Then с чтением.**
(а) Ключи по смыслу только для before/now-вопросов (`now`/`before`, поле `claim` у чтений); обычные вопросы — буквы. Закрывает
наблюдаемый класс по корню: дизайнер пишет записи ДО существования вопроса (`raise`) и порядка знать не может. Малое изменение S2
(только поле `claim` у ролью написанных before/now-чтений). Остаток: обычные вопросы по букве — дизайнер видит их чтения в
`requirements-readiness.json`, риск — перестановка чтений после кейсов.
(б) Стабильный ключ у КАЖДОГО чтения любого вопроса (`key`), кейс пишет по ключу, буквы — только на печати. Закрывает класс целиком,
шире: контракт S2, роль тестировщика требований, все читатели `readings`.
(в) Буквы остаются; дизайнер добавляет под буквой цитату чтения, код сверяет нормализованный текст. Работает для всех вопросов без
правки S2, но сравнение текста хрупко и близко к FR-12.
Рекомендация: (а) сейчас; (б) — находкой в `gates-and-words`, если перестановки чтений обычных вопросов найдутся на прогонах.

**F-2 (HF4-6): судить ли дайджест Codex-ребёнка.** Новый читатель читает и Codex-форму (`response_item`). Сегодня Codex-rollout
разбором Claude даёт `""` — дайджест на Codex фактически не судится (оценка по коду, на живом Codex не проверено).
(а) Один читатель, обе формы: Codex получает тот же гейт формы — согласовано с осью 22 (новый хост — строка данных, не ветка), но
новый источник блоков на Codex до замера. (б) Только Claude сейчас: читатель обеих форм есть, но гейт формы для Codex-формы
пропускается веткой — это ветка по хосту в читателе (против закрывающего правила оси 22).
Рекомендация: (а) + строка живого доказательства в кучку `codex` (один Codex-прогон S1–S3 до релиза или пометка в CHANGELOG).

**F-3 (HF4-8): где лежит связь R-n → Qn.**
(а) Ячейка `Decision` таблицы `## Reading forks` регистра начинается с id вопроса (так уже пишет роль на стенде); код читает id.
Совместимо с прогоном в полёте без правок данных. (б) Поле строки плана `question_refs` обязательно и для ОТВЕЧЕННОГО вопроса,
который закрыл противоречие строки (стратег пишет; сейчас он пишет нечитаемое `decision_refs`). Выход S3 отказывает строке
`source_conflict` без ссылок. (в) Новая колонка `question` в `## Contradiction matrix`.
Рекомендация: (а); (б) — дополнительно позже (строка контракта стратегу), если Lead хочет второй носитель — но это два носителя одного
факта (AR-13), поэтому я бы не делала.

**F-4 (HF4-9): строка плана, чей вопрос отвечен в том же ответе гейта A, что и одобрение (TS-14).**
Сначала замер (PROJECT.md правило 6 (а)): кто после гейта A читает `oracle_unknown`/`oracle` строки плана (grep с контролем) — если
никто, кроме отчёта, следствие только косметическое.
(а) Ответы того же пакета гейта A применяются к плану до того, как одобрение вступает в силу (строки патчатся или уходят стратегу).
Цена: план меняется после показа — хэш содержимого гейта A расходится с одобренным, нужен новый показ? (б) Одобренный план остаётся;
код сверяет строку со своими кейсами: если каждый кейс строки держит `person:Qn` по этому вопросу, строка получает `oracle_unknown:
false` и `oracle: person:Qn` (выводимое значение пишет код, AR-10), `disposition` не трогается, строка «TS-14 now has a settled
expected value (Q7); how it is checked stays as you approved» в бриф S5. (в) Ничего: отчёт читает кейсы.
Рекомендация: (б), если замер покажет читателя после гейта A; иначе (в) и строка в находке.

**F-5 (HF4-10): квитанции качества S5.**
(а) Не требовать то, что ничто не производит (FR-5): фильтр по данным производителей (сегодня пусто), неисполненное — поле окна
`quality_not_run`. (б) Производитель-квитанция из `state/readiness.json` (готов → `passed`). Против: готовность адаптера тикетов не
говорит ничего о коде окна (FR-18) — квитанция была бы фальшивой. (в) Настоящий производитель: код гоняет `profiles[].quality_gates`
проекта (например `lint`) на каждом окне и пишет квитанцию с `input_hash` окна. Честно, но L и цена каждого окна (P11).
Рекомендация: (а) сейчас + (в) находкой с вопросом владельцу «должна ли фабрика гонять lint проекта на окне». Подвопрос: печатать
ли `quality_not_run` в отчёте — решён Lead в ревизии 2 (печатать, в этом узле, по правилу QNR §5.5 п. 6).

**F-6 (HF4-11): слово `reject` от замечаний — СЛОВО ВЛАДЕЛЬЦА** (дано 28.10: вариант A, §11).
(A) `reject` — только при `fail`; любое число замечаний без `fail` — `approve_with_concerns`, замечания идут дальше. (B) Правило
`≥3 concern → reject` до капа, на последнем раунде — `approve_with_concerns`. (C) Как сейчас: на капе решает человек.
Оставлено для истории решения; текущая спека — §5.6.

**F-7: SC2-27 целиком или корень.** SC2-27 — «ошибки формата первого возврата чинит код либо они ожидаемо-нулевые; цена блока
записывается». HF4-6 закрывает корень (чужой автор). Рекомендация: перенос корня, «цена блока записывается» остаётся в SC2-27.

**F-8 (HF4-7): наследие в полёте — открытый before/now-вопрос, кейс с буквами.** (а) Карточка без привязки + находка репетиции
(переработка кейса до показа, одна лишняя работа дизайнера). (б) Только карточка без привязки, человек отвечает буквой, применитель
не применяет (текст «не установлен»), доработка после ответа. Рекомендация: (а) — П0, человек не должен выбирать по непривязанным
текстам.

## 8. Мелкие решения, закрытые мной

- Новые узлы — HF4-6…HF4-11 в пачке 4 (не новая пачка): пачка не взята, тема — тот же прогон.
- HF4-8 и HF4-9 — один билдер, последовательно: оба правят `contradiction_questions` и общую фикстуру.
- Общий выживший для HF4-6 — построчная функция `host_adapter.assistant_row_texts`, а не строгий `host_probe._assistant_texts`
  целиком: проба обязана падать на нечитаемой строке, гейт — пропускать её (строгость у вызывающего).
- Порядок источников `handoff_digest`: транскрипт ребёнка → `last_assistant_message` → `transcript_path`; поле
  `last_assistant_message` не проверено в этом репозитории, поэтому оно не выше измеренного файла.
- Хвост 400 строк и обрезка 4000 символов — сегодняшние, не новые.
- (Ревизия 2) Дата среза для `claim` у ролью написанных чтений УБРАНА: носителя даты у `before_now_errors` нет (t-1472 B7-3);
  условие находки — данные (кейс пишет `now`/`before` на вопросе без `claim`).
- Пределы «Already decided»: 10 строк, слова 160 символов (как соседние клипы `gate_brief`).
- Фикстуры — по каталогу на узел (`run-12586-<тема>`), без общего каталога, чтобы owns не пересекались.
- Новые тест-файлы на узел вместо дописывания в большие (`test_gate_brief_and_retro.py` и т.п. — только как регрессия-свидетель).
- (Ревизия 2) Нумерация CC-строк `CC-n` по порядку строк roll-call; пустой `note` — фиксированный английский текст; слова причин
  `quality_not_run` — в файле данных, не в коде.

## 9. Замеченные аналоги и противоречия (не расширяю скоуп — в очередь)

1. Карта t-1468, P1 (e): «читать `agent_transcript_path`» без формы handback дайджест не найдёт (§2 п. 1).
2. Карта t-1468: `test_planning_contract*.py` не существует (§2 п. 8).
3. Находка GW1-25 «корень не установлен» — установлен (§2 п. 3): FR-38/AR-10, не перестановка чтений.
4. Стратег пишет `decision_refs` — поля нет в контракте; связь с вопросом лежала в нечитаемом поле (AR-22, FR-38): строка
   контракта стратегу или запрет неизвестного поля на выходе S3 — находкой в `gates-and-words`.
5. `story_run.Driver.quality_check_ids` (`:5811-5821`) не читает `quality_gates` в форме словаря `{name: {...}}` (форма конфига
   стенда) — даёт `[]`; второй смысл поля `required_quality_checks` («id готовности» в `controller-api.md`) — два производителя одного
   поля с разным смыслом.
6. `contract.resolve_then_oracle` для `b` before/now-вопроса берёт `before.value`, а карточка гейта A печатает текст `question_thens`
   под `b` — два ответа на «что проверит Then при b» (FR-10). Теперь — строка пачки (§6).
7. `controller._code_review_refusal` говорит критику кода «these are the review's own receipts» про квитанции, которые никто не
   пишет (FR-2) — закрывается HF4-10.
8. Ложные блоки P1 прятали `halt` ролей: гейт читал прозу дирижёра (`is_halting_handoff`) — после HF4-6 halt-ы ролей будут видны
   впервые; ожидать изменение поведения драйвера на S1/S2, проверить на живом доказательстве.
9. `plans/piles/forge/findings/20261028-testy-ne-derzhat-styki-stadij.md` (слово владельца о стыках) я не открывала — форма ключей
   стыка взята из брифа Lead.
10. (Ревизия 2) Карта t-1468 P3 (e) «гейт A уже печатает concerns carried» — неверно (t-1472); строка вводится HF4-11.

## 10. След чтения

Прочитано (носитель): `docs/tasks/handoffs/t-1468-run-12586-problems-map.md` (целиком); `plans/piles/hotfix-12586/README.md`,
`batch-4-ostatki-hf3-po-revyu.md` (целиком), шапки `batch-2-…`, `batch-3-…`, строка HF3-10; `plans/piles/gates-and-words/batch-1-words-and-gates.md`
(целиком), находка `findings/20261028-gejt-a-varianty-q7-pereputany-mestami.md`; `plans/piles/speed-cost/batch-2-…` (шапка, SC2-27);
`design/architecture.md:86-261`; `docs/SIBLING_MAP.md` (заголовки осей, оси 14 и 22); `plans/builder-rules.md:10-31`.
Пакет: `exit_gate.py:600-829, 1395-1475`; `cost_capture.py:3000-3042`; `host_dispatch.py:70-99`; `host_probe.py:474-504`;
`gate_brief.py:1585-1694, 1900-2129, 2310-2369`; `contract.py:560-629, 978-1202`; `planning_contract.py:955-994, 1220-1330, 2264-2324`;
`question_register.py:365-392, 872-892` (+ grep `raise_*`); `window_record.py:925-959`; `acceptance.py:795-844`;
`coverage_contract.py:215-254`; `controller.py:1018-1030, 5190-5217, 5870-5881` (+ список функций); `story_run.py:3343-3388,
5811-5821, 6468-6508`; `critic_rollcall.py:240-324`; `agents/qa-case-critic.md:55-93`; `agents/qa-case-designer.md:45-124`;
`references/artifact-contract.md:96-140`; `references/artifact-contract-plan.md:1-89`; `references/templates/requirements-register.md:80-106`;
`references/controller-api.md:80-99`; grep `skills/qa-story/phases/s0.md` (quality).
Стенд (только чтение): `work/gate-a-brief.txt` (целиком); `state/words/` (список; `s4-…-gateA-decision.txt`, `s4-…-q7.txt`,
`s5-…-quality-receipts.txt`, `s2-…-q1.txt`); `work/question-answers.jsonl` (целиком); `work/requirements-readiness.json:36-250`;
`work/requirements-register.md:1-80`; `work/test-plan.json` (TS-1, TS-8, TS-14); `work/test-cases/integrations/TC-014.md`
(front matter), `cases/TC-014/cv_998932…md`, `cv_b3406…md` (front matter); `config.json:148-161, 690-701`; grep `state/controller.json`.
Транскрипты стенда: `~/.claude/projects/D--ws-testproject1-dev-010-testproject1-sdk-test-harness/22686563-…/subagents/agent-a19dac213a6228a50.jsonl`
(строки 72–76, grep).
Ревизия 2: `docs/tasks/specs/reviews/t-1472-hf4-plan-critic.md` (целиком); факты ревизии, которые я сама в коде не перечитывала,
взяты из следа критика t-1472 (его file:line и перепрогоны): `planning_contract.case_entry_answers :1180-1190`, `variant_errors
:1475-1500`, `_case_rework :2207-2215`, `contract.CLAIM_INTENDED :879`, `coverage_contract.py:555`, `contract.py:3494, 3631`,
`window_record.py:1177`, `s5_plan.remarks_of :1069-1083`, `brief_pack.py:87, 1799-1850`, `s5_precheck.py:2674`,
`story_run.py:8534, 8570`, `gate_brief.py:2233`.
Отрицательные утверждения и их контроль той же формы: `last_assistant_message` — 0 в пакете (контроль `agent_transcript_path` —
найден, тот же Grep, тот же путь); `decision_refs` — 0 в пакете (контроль `question_refs` — 180, тот же вызов `count`);
`quality_receipt_refs` — 0 в манифесте стенда (контроль `"tests"` — найден в том же файле); тестов `test_planning_contract*.py` —
нет (Glob той же формы нашёл `test_plan_row.py` и др.).
Сверх манифеста: транскрипты стенда в `~/.claude/projects` (не названы в given — решающие для P1), `host_probe.py`,
`host_adapter`/ось 22, `question_register.py`, `contract.py`, `story_run.py`, `controller.py`, `coverage_contract.py`,
`references/templates/requirements-register.md`.

## 11. Решения Lead и владельца (28.10.2026, Lead = Opus, окно деградации; решила сама — подсвечено владельцу)

- **F-6 — слово владельца 28.10.2026** («Если замечания не критические, то они передаются дальше, автоматизатор их учитывает при
  автоматизации кейсов»): `reject` критика кейсов — только при `fail` (вариант A); замечания измерений без `fail` дают
  `approve_with_concerns` на любом раунде, гейт A не требует слова человека; замечания НЕ теряются — идут дальше в бриф автоматора S5
  (тот же носитель, что читает автоматор по кейсу), и автоматор учитывает их; гейт A печатает их строкой «concerns carried to automation».
  Инвариант: кейс с `fail` никогда не одобряется. HF4-11 разблокирован; ключ стыка — раунд 3 стенда (0 `fail`, 3 замечания) →
  `approve_with_concerns` → замечания видны в брифе окна S5 по своему кейсу.
- **F-1:** (а) — `now`/`before` для before/now-вопросов; (б) — находкой, если перестановки найдутся.
- **F-2:** (а) — один читатель обеих форм; строка живого доказательства в кучку `codex`.
- **F-3:** (а) — id вопроса в ячейке `Decision`; второй носитель не вводится (AR-13).
- **F-4:** билдер HF4-9 первым шагом делает замер (grep с контролем: кто после гейта A читает `oracle_unknown`/`oracle` строки);
  есть читатель — (б), нет — (в) и строка в отчёте билдера.
- **F-5:** (а) — не требовать неисполнимое, поле `quality_not_run`, печать в отчёте — отдельной строкой пачки; (в) — находкой
  владельцу («гонять ли lint проекта на окне»).
- **F-7:** переносится корень; «цена блока» остаётся в SC2-27.
- **F-8:** (а).
- Критик на план (PROJECT.md правило 6 (б)) — HF4-7, HF4-10, HF4-11 одним проходом до их билдеров; HF4-6 и HF4-8/9 стартуют сразу.

Дополнено ревизией 2 по сообщению Lead после критика t-1472 (записано дизайнером со слов Lead):
- **B11-1 — решила Lead:** замечания едут через `s5_plan.remarks_of`; автоматор обязан ответить строкой `plan_remarks`, C12 ловит
  пропуск; ключ стыка — как предложил критик (§5.6 K3). Ключ из пункта F-6 выше («раунд 3 → `approve_with_concerns`») заменён парой
  K1/K2 §5.6 — без переписывания слова роли кодом.
- **B11-2 — решила Lead:** два ключа — раунд как записан отказан с дверью «переписать строку `Verdict:`»; исправленный раунд проходит;
  код слово роли не переписывает (FR-35).
- **B11-3 — решила Lead:** вариант (а) критика t-1472 — раунд, где есть только замечания и нет `fail`, НЕ запускает доработку S4: при
  `approve_with_concerns` критик пишет дайджест `ok` (строка роли `qa-case-critic.md`), петля S4 (`story_run.py`) не меняется.
  Строка F-6 (A) «раунды S4 кончаются раньше» верна именно в этом смысле.
- **B10-2 — решила Lead:** у `quality_not_run` есть читатель в этом же узле — `report_facts` печатает в отчёт о тестировании
  «Quality checks the factory did not run: …»; id готовности, уже проверенные S0, туда НЕ печатаются (правило QNR, §5.5 п. 6). Это
  заменяет в пункте F-5 выше слова «печать в отчёте — отдельной строкой пачки».

## 12. Правки после критика t-1472 (ревизия 2)

1. B7-1 — §5.2 п. 3: один читатель `contract.question_then_text`; `planning_contract.case_entry_answers` — его обёртка (owns);
   `variant_errors` считает `resolved`/`missing`/`extra` по `question_then_keys`; ключ K8, мутация.
2. B7-2 — §5.2 «Края»: before/now-вопрос наследия, отвеченный БУКВОЙ, при кейсе с буквами читается по букве (только `settled`); K6 (б).
3. B7-3 — §5.2 п. 5 переписан: `claim` → равенство с парой кода → иначе `None` + находка по данным (без даты среза); строка роли
   тестировщика требований (шаг 8) и `artifact-contract-json.md` в owns; вызов `gate_preflight.py:1319` — условно; K9; дата среза
   убрана из §8.
4. N7-1 — §5.2 п. 7: буквы на `raise`-записи — ошибка FORM в `then_oracle_errors` (валидатор при записи). N7-2 — §5.2 п. 4:
   `claim_confirmed`, `before_value_needed`, O2 спрашивают смысл через `claim_reading_index`; K10. N7-3 — позиция п. 6 после
   `settled`/`resolved` с инвариантом. N7-4 — K1 через `critic_rollcall.py --apply-fixes`. N7-5 — строка пачки (§6). Правило 18 —
   проверка п. 6 отдельной функцией `_claim_key_errors`.
5. B10-1 — §5.5 п. 4а: `coverage_contract` (оба места) не требует ни ссылок, ни причины при пустом требовании; абзац автоматора и
   слайсы в owns; K1 разделён на K1a/K1b.
6. B10-2 — §5.5 п. 1, 3, 6: `quality_not_run` = `{id, why}`, слова причин — данные; читатель — `report_facts` (одна функция) в этом
   узле; правило QNR: id, проверенные S0, в отчёт не печатаются, нечитаемая запись готовности — `unknown_s0` и печать; K8.
7. N10-1 — id-не-строка → `json.dumps`, требуется, фильтр до `str()` у `:943`. N10-2 — `_s5_collect` сравнивает `demanded(window)` с
   `demanded(state)`. N10-3 — абзац о регистре/пробелах заменён одной фразой. N10-4 — факт «4 id записал дирижёр» помечен «оценка»
   (§2 п. 6). Сверх критика: `contract.py:3494, 3631` (форма окна) и `receipt_dict` в owns — иначе новое поле окна без допуска.
8. B11-1 — §5.6 п. 3–5: `carried_concerns` → `s5_plan.remarks_of` → бриф окна → `plan_remarks` → C12; строка гейта A; owns
   (`s5_plan.py`, `gate_brief.py` — одна функция, `brief_pack.py` — условно); K3, K4; край прогона в полёте.
9. B11-2 — §5.6 п. 2: `_round_word_rule` → `partial` с `round_word_rule`, дверь «переписать `Verdict:`»; K1 (отказ) и K2 (проход);
   направление ошибки и неудобные входы. B11-3 — §5.6 п. 1 и §11: дайджест `ok` при `approve_with_concerns`, `story_run.py` не
   трогается. N11-1 — оба правила шага 4. N11-2 — результат двойника оси 5 — пункт отчёта билдера.
10. Общие файлы после ревизии: `gate_brief.py` — HF4-7 (`_then_effect`, `question_effects`), HF4-8 (`contradiction_questions`,
    `_decided_lines`, сборщик `data`), HF4-11 (функция строки `**Critic**`); `planning_contract.py` — HF4-7 (`case_entry_answers`,
    ветка кейсов `variant_errors`, `_claim_key_errors`), HF4-8 (`register_fork_questions`), HF4-9 (новая функция писателя
    `question_refs`); `contract.py` — HF4-7 (функции §5.2), HF4-10 (списки формы окна), HF4-3 (`rollup_status`);
    `qa-requirements-tester.md` — HF4-7 (шаг 8) и HF4-8 (строка `Decision`). Функции не пересекаются; §5.3/§5.4 не менялись.
