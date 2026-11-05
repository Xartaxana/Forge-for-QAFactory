# Ошибка фабрики, найденная в проекте, уходит в бэклог фабрики проекта со scope `upstream-candidate`: проверить на живом повторе 12586, что FB-3 и FB-5 так и записаны

id: — | кучка: `live-runs` | от: Lead пачки hotfix-12586/1 (dev2), 23.10.2026 | приоритет: П2 | кандидат наверх: нет

Слово владельца 23.10.2026 (14:1x, по вопросу Lead о носителе «ошибки пробы — в бэклог фабрики»): «если находка была записана как upstream candidate — то
всё правильно». Носитель — `qa-factory/factory-backlog.md` проекта; scope — `upstream-candidate` (словарь `project_decisions.py add-finding --scope
local-urgent|local-calibration|upstream-candidate`, `skills/qa-story/SKILL.md:76`; панель `factory_dashboard.py:30` красит `upstream-candidate`
отдельным цветом, `:3396` его обрабатывает). Код пачки hotfix-12586/1 по этому слову НЕ меняется.

Что проверить: в прогоне TP1-12586 (проект `testproject1-dev-010/testproject1-sdk/test-harness`) дирижёр записал строки бэклога проекта: FB-3 — проба
входа шлёт `username`, стенд ждёт `email` (находка OH3-10), FB-5 — отпечаток падает `TypeError` на форме `{path, sha256}` из карточки роли (находка
EP1-8; `execution-probes/findings/20261022-otpechatok-padaet-na-forme-iz-svoej-spravki.md`, строка FB-5); EP1-10 ссылается на FB-7 и FB-9.
Проверка — на живом доказательстве пачки (повтор S5 12586): scope каждой из этих строк должен быть `upstream-candidate`, а не `local-urgent`
или пусто. Слово владельца «ошибка пробы — в бэклог фабрики» выполнено, если ошибка фабрики (а не проекта) лежит в `factory-backlog.md`
именно с этим scope.

Расхождение (scope другой или пустой) — узел здесь: что в тексте `SKILL.md:76` / `agents/qa-retro-analyst.md:64` не даёт дирижёру выбрать
`upstream-candidate` для дефекта самой фабрики; выяснить и поправить текст, а не ограничиться правкой двух строк рукой.

Свидетель: `plans/piles/hotfix-12586/batch-1-run-12586.md`, «Ход» 23.10 14:1x («Носитель — `qa-factory/factory-backlog.md` проекта со scope
`upstream-candidate`; код пачки не меняется; живое доказательство проверяет scope строк FB-3/FB-5 прогона 12586, расхождение — находка в
`onboarding-hooks`, не узел пачки»); `execution-probes/findings/20261022-otpechatok-padaet-na-forme-iz-svoej-spravki.md` (строка FB-5).
Проверка ещё не делалась: это условие приёмки живого доказательства, а не установленный факт.

Принципы и правила: P13, FR-19, FR-4, AR-25.

Решение владельца нужно: нет (слово дано 23.10.2026).
