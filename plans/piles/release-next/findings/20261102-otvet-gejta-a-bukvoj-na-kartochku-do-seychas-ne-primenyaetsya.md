# Ответ человека буквой на карточку «до / сейчас» молча не применяется: вопрос по сессии задан на гейте B ещё дважды, а отчёт держит его открытым

id: — | кучка: `release-next` | от: прогон LOCAL-1, разборы t-1671 Н-1 и t-1672 П-3, 02.11.2026 | приоритет: П1 | кандидат наверх: нет

Сокращения: `A` = `mybooks-stand/test-automation-framework/qa-factory/artifacts/LOCAL-1`; `PKG` = `ai-packages/qa-factory`; `T` = транскрипт дирижёра, номера строк.
Разборы: `docs/tasks/specs/reviews/t-1671-local-1-gates-vs-analysis.md` (Н-1, БЛОК), `docs/tasks/specs/reviews/t-1672-local-1-whole-run.md` (П-3, БОЛЬШАЯ).

## Что наблюдалось

- Человек на гейте A: «Q9 Adding after session expiry asks for login, and the product is added after re-authentication» (`A/state/words/gate-a-answer-1.txt:8`); запись `Q9: b` (`A/state/words/gate-a-decision.txt:13`).
- В карточке вариант b — «A regression: the behaviour before the change is the expected one - unknown; say what it was», а его Then — ровно слова человека (`A/work/gate-a-brief.md:169-172`).
- Код: `scripts/contract.py:1487-1505` `before_value_needed`: при b и пустом `before` вопрос «не решён». Затем `question_register._holds` (`scripts/question_register.py:366`) → `planning_contract.apply_recorded_answers` (`scripts/planning_contract.py:2904-2905`) пишет `not_applied: "changed_since_answer"`. Метка ложная: строка не менялась, хэш тот же `db01cef…` (`A/work/question-answers.jsonl:9-12`); ответ записан трижды.
- Следствие: TS-26 остался `unverifiable` (`A/work/test-plan.md:44`); TC_024 не запускался; в отчёте R-26 «no case», «Q9: before unknown, now unknown» (`A/test-report.md:94,181,291`), строка open-questions `A/test-report.md:141` держит «extend the session, or ask for login?» (id вопроса расходится: в отчёте Q4, на карточке Q9), BN-11 «you have not said so».
- Вопрос задан человеку ещё дважды: гейт B, `T` L3132 и `T` L3238 (GB-3 «что приложение делало при истёкшей сессии ДО изменения»). «До изменения» на истории без диффа смысла не имеет: поведение «сейчас» известно из кода (`MyBooks/src/lib/session.ts:34-37`).
- Соседи по форме, которые идут тем же путём: Q6 b, Q7 b, Q8 b.

## Причина

Шаблон P20 «до / сейчас» применён к истории «текущий код», где «до изменения» нет вовсе. Вариант b называет «регрессию» (буква), а его Then (то, что читает человек) называет ожидаемое поведение; код записывает только букву и ждёт значения `before`, которого никто не пишет из слов человека. Один пакет противоречит сам себе (FR-10), обещание человеку «ответ записан» не исполнено (P22: недопустимое — слова записаны, а действия нет).

## Класс

Смысл буквы варианта (что запишет код) расходится с текстом варианта (что читает человек); слово человека, где ожидаемое названо, не доезжает до строки плана, к которой привязан вопрос (FR-7, FR-8, FR-10, FR-12, AR-24, AR-25). Регрессия/не починено: GW1-43 (0.10.8, класс «решение, отвеченное раньше, не спрашивается снова»; здесь сторона не «решение класса окна», а «ответ гейта A»). Фабричный класс, не правило MyBooks.

## Что именно менять

Направление выбрано (Lead, 02.11.2026), ветка (1) разбора t-1671.

1. **Вариант «регрессия» не строится на истории без диффа.** `scripts/gate_brief.py` (сборка карточки «до / сейчас»; искать по строке `the behaviour before the change`): для истории, где источник кода — «текущий код», варианты карточки — это Then требования, без варианта «регрессия, назовите прежнее». Тест: карточка Q9 на фикстуре LOCAL-1 не содержит слов «a regression» и `say what it was`.
2. **Ответ буквой на вариант с конкретным Then записывает этот Then как значение.** `scripts/question_register.py` (где пишется `reading` ответа, около `:366`) и `scripts/contract.py` `before_value_needed`: если выбранный вариант несёт текст Then, значение `before`/`reading` — этот текст; вопрос «решён». Тест: `Q9: b` на фикстуре → `before_value_needed(question)` ложно, вопрос `settled`.
3. **Честная метка.** `scripts/planning_contract.py` `apply_recorded_answers` (`NOT_APPLIED_CHANGED`, `:2729`, `:2905`): `changed_since_answer` пишется только при `changed_since_answer is True` (хэш строки изменился); пустое значение `before` → `not_applied: "before_value_missing"`. Тест: ответ на неизменённой строке с пустым `before` → метка `before_value_missing`, не `changed_since_answer`.
4. **Ответ доходит до плана и отчёта.** После п. 2 строка TS-26 переходит из `unverifiable` в `if_answered`; `scripts/report_facts.py` (`:886`, `:1788`) не показывает отвеченный вопрос открытым (сверка по id вопроса гейта A, не по номеру в карточке). Тест: Q9 b на фикстуре LOCAL-1 → TS-26 `if_answered`, раздел open-questions отчёта не содержит Q9.
5. **Повтор не задаётся.** `scripts/gate_brief.py` гейта B: вопрос, на который есть запись в `state/words/gate-a-*` с применённым ответом, в пакет гейта B не входит. Тест: пакет гейта B на фикстуре с отвеченным Q9 не содержит вопроса о сессии.

## Принципы и правила

P20, P22; FR-7, FR-8, FR-10, FR-12; AR-24, AR-25.

## Связи

- GW1-43 (`gates-and-words/findings/20261031-otvechennoe-reshenie-klassa-sprashivaetsya-snova-na-sleduyushchem-okne.md`, «принято, слито 0.10.8»): регрессия/не починено по классу «отвеченное спрашивается снова». RN1-14 (то же на гейте A по решениям S1), RN1-9, RN1-4.
- Разборы t-1671 Н-1, t-1672 П-3.

Решение владельца нужно: нет.
