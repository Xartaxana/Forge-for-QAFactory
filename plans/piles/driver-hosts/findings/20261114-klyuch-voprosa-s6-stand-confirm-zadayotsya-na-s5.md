# Вопрос о стенде на входе S5 несёт ключ цен `s6.stand_confirm`: имя говорит про S6, ключ общий для двух стадий

id: — | кучка: `driver-hosts` | от: отчёт P1-b N2e, кандидат 7 в разделе «Factory gap candidates» (`.claude/worktrees/p1b-n3/docs/tasks/specs/reports/20261114-p1b-n2e-report.md`); кандидаты 1-5 того отчёта чинятся своим узлом и сюда не входят | приоритет: П3 | кандидат наверх: нет

## Что не так

Класс фабрики: **имя носителя называет одну стадию, а носитель читают две (FR-37, P31)**. `ai-packages/qa-factory/scripts/driver_stage_build.py::stand_question_text` задаёт закрытый вопрос «какой стенд» на входе S5 и S6 одним ключом
`self.closed_question("s6.stand_confirm", …)` (строка ряда цен — `ai-packages/qa-factory/references/question-prices.json`, ключ `s6.stand_confirm`). Так задумано: слово человека проходит S5 и S6 вместе, вопрос задаётся один раз
(комментарий в начале `driver_stage_build.py`: «A person's word passes S5 and S6 together»). Дефект один — имя: прогон N2e видел вопрос на S5 (стори без стенда) под ключом с «s6» в имени, и по ключу журнал/цены читаются как вопрос S6.
Поведение вопроса верно и не меняется.

## Что именно менять

Выбранное направление: стадийно-нейтральное имя ключа вместо `s6.…`; поведение, тексты вариантов и ряды цен — без изменений. Форму имени (как у ключей без стадии, например `closed.held`) выбирает дизайнер в спеке узла.

1. Установить ДО правки (одна команда чтения, результат в спеке узла): все читатели ключа `s6.stand_confirm` — код, данные, тесты и записанные ответы. Известные на `origin/main` 2cf488ad (grep по `*.py`, `*.md`, `*.json` пакета; контроль того же вида: ключ `s6.gate_a_dry` находится): `driver_stage_build.py`,
   `references/question-prices.json`, тесты `test_conductor_doors.py`, `test_story_run_s6.py`, `test_story_run_words.py`.
2. `ai-packages/qa-factory/scripts/driver_stage_build.py` и `ai-packages/qa-factory/references/question-prices.json`: одно новое имя, один коммит, три теста обновлены тем же ходом (производитель и читатели — вместе, AR-22).
   TEMPORAL: если п. 1 нашёл читателя ЗАПИСАННЫХ ответов под старым именем (стори, уже ответившая на вопрос), он принимает оба имени в одном месте; не нашёл — старое имя не поддерживается, и это названо в changelog узла.
3. Тест: строка таблицы в `ai-packages/qa-factory/scripts/tests/test_human_questions.py` (keep, `table`, быстрый): вопрос о стенде на S5 и на S6 несёт ОДИН ключ без стадии, и у этого ключа есть ряды цен для каждого ответа (`stand name`, `retry`, `go on`). Файлы
   `test_conductor_doors.py` (медленный) и `test_story_run_*` — «судит канон пачки».

Принципы и правила: FR-37, P31; AR-22, AR-13.

Решение владельца нужно: нет.
