# Онбординг больше не спрашивает о рисковых областях проекта (тема 4), а читатели ответа остались

id: — | кучка: `onboarding-hooks` | от: Lead (Fable), 20.10.2026 18:2x, по вопросу владельца 20.10 18:0x | приоритет: П1 | кандидат наверх: нет

Что не так: до коммита `28fc7170` (18.09.2026, «fix(qa-factory): align onboarding execution metrics and cost reporting», старый хэш
`c9c956b4` по `docs/provenance.md:62`) тема 4 интервью звучала «**Risk and impact scale.** Main risk areas of the project, and
`impact_scale` — priority multipliers by area (used later as the strategist's budget guideline)». Коммит заменил числовые множители
картой классов `impact_scale` (намеренно: `CHANGELOG.md:1667-1672`) и ТЕМ ЖЕ ХОДОМ убрал первую половину вопроса — «главные рисковые
области проекта»: сегодня `p2-interview.md:196-199` спрашивает только «отличается ли карта классов от канонической». Причина в
коммите не записана — побочная правка в коммите про метрики. Читатели ответа остались и голодают на свежеонбординговом проекте
(перепись t-1148, `docs/tasks/specs/reports/t-1148-high-risk-areas-trace.md`): `scripts/sizing.py:170-192` парсит абзац
`**P1 areas.**` в `qa-factory/strategy/test-strategy.md` и поднимает вес требования до P1 (`sizing.py:476-479`: «the area-based weight
bump is unavailable», когда абзаца нет) — ни один файл `skills/qa-onboarding` этот абзац не пишет (t39/t19, контроль t38);
`automation-candidacy.md:39-41` велит стратегу тянуть строку в `automate` по «critical flow, fragile area … named in
test-strategy.md»; `p4-generate.md:431-437` по-прежнему выводит стартовый набор `aspect-profile.md` из «topic 4's risk areas» и несёт
«topic 4's question verbatim» в строку бэклога — теперь это вопрос про карту классов; `agents/qa-test-strategist.md:24` говорит
о «risk multipliers», которых нет. Что на тест-план влияет СЕГОДНЯ: только класс ущерба строки реестра (`impact_scale` → приоритет,
`qa-test-strategist.md:36-39`, `validate_artifacts.py:387-408`); рисковые области в приоритет, глубину проверки
(`risk-policy.md`, `planning_contract.py`) и регрессию (`qa-test-strategist.md:90-94` — по blast radius) не входят.

Что сделать (слово владельца 20.10 18:1x: «Да, вернуть, и проверь, на что это влияет в дальнейшем, используем ли мы это знание для
составления тест-плана»): вернуть в тему 4 вопрос о рисковых областях рядом с вопросом о карте классов; ответу дать носителя с
читателями — абзацы `**P1 areas.**` / `**P2 areas.**` / `**P3 areas.**` в разделе «Risk and impact scale» `test-strategy.md` в формате
парсера `sizing.py` (фикстура `scripts/tests/fixtures/sizing-15045/qa-factory/strategy/test-strategy.md:81-104`) и стартовый набор
`aspect-profile.md` (`p4-generate.md:431`); пустой ответ → `[DEFERRED: risk areas not named]` и строка бэклога с вопросом о рисках
(не о карте классов); «Fragile Areas» `project-profile.md:370` — как есть (переносится при повторном онбординге); README:20,
SKILL.md:82, `evals/evals.json:7,215` согласуются с темой; `qa-test-strategist.md:24` «risk multipliers» → «P1 areas». Решение Lead
(техническое, подсвечено владельцу): носитель — (a) абзац P1/P2/P3 areas + (c) aspect-profile, не новый ключ `config.json` (ключа с
читателем нет). Открытое: влияет ли ответ на `verification_depth` — сегодня нет; расширять `risk-policy.md` — отдельная находка после
живого прогона, не здесь.

Свидетель: `git show 28fc7170 -- ai-packages/qa-factory/skills/qa-onboarding/phases/p2-interview.md` (строки 32/35 диффа);
перепись t-1148 (42 объекта, 68 строк следа; отрицательные t19/t39/t51 с контролями).

Принципы и правила: P20 (ожидание из требований, не из кода), P23 (работа по требованиям), FR-5 (стадия не требует артефакта,
который никто не производит), FR-11 (поле, которое читает код, роль должна уметь произвести), FR-37 (пути и имена в тексте
= то, что пишет код), FR-41; ось 5 SIBLING_MAP (интервью ↔ генератор ↔ читатели).

Решение владельца нужно: нет (дано 20.10 18:1x — «вернуть»); узел OH1-10 пачки 1 (не взята).
