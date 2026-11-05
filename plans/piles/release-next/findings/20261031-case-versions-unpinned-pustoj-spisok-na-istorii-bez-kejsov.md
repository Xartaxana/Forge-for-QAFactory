# `case_versions.unpinned()` на истории без файлов кейсов отдаёт `[]`: репетиция гейта A молчит, пустое читается как «всё закреплено» (t-520 S2)

id: — | кучка: `release-next` | от: критик t-520, вопрос «`unpinned()` returning [] on empty? S2, queue, must be a real row» (`docs/tasks/specs/reviews/t-520-small-nodes-critic.md:66`), 31.10.2026 | приоритет: П2 | кандидат наверх: нет

## Что наблюдалось

- `case_versions.unpinned` (`case_versions.py:411`) идёт по `discover_cases(task_root, cases_dirs)`; нет ни одного файла кейса — цикл пуст, возврат `[]`. Тот же `[]` значит «все закреплены».
- `gate_preflight.check_cases` (`gate_preflight.py:1360–1372`): `unpinned = case_versions.unpinned(self.task_root)`; пустой список — ни одного вопроса: гейт A пройдёт без кейсов молча. Контроллер отказывает только при НЕпустой области без пинов:
  `controller.py:2794` `if state.get("scope"):` — пустая область не прослеживалась критиком.
- SC5-12 (спека N1) ввёл для CLI `provide`/`--verify` честный ответ на пустое (`_empty_answer`, «verified: false»); читатель гейта остался на старом смысле. Класс: пустой вход как проход (FR-59, AR-23, AR-28).
- Спека §7 называла это «кандидатом»; в `plans/piles` находки не было — это она.

## Что именно менять

1. `case_versions.py`: новая `pin_state(task_root, cases_dirs=None) -> dict` = `{"cases": <число найденных файлов>, "unpinned": <как сейчас>}`; `unpinned` остаётся тонкой обёрткой (`pin_state(...)["unpinned"]`), чтобы CLI и тесты не менялись (AR-13, один обход).
2. `gate_preflight.py`, `check_cases` (:1360): `cases == 0` при непустом плане (`work/test-plan.json` с хотя бы одной строкой `disposition != skip`) — находка класса `FACTORY_FIXABLE` с дверью: «the plan has rows but no case file is on disk; the factory writes the cases before the gate»; пустой план — молчание остаётся (истории без кейсов бывают). Не удалось прочитать — `self.unavailable("case_versions", …)` как сейчас.
3. `controller.py:2794`: при `state.get("scope")` пустом, но плане с строками — не трогать (вне узла); проверить чтением и записать в узел результат (одна фраза): отказывает ли гейт запись пустой области.
4. Тесты (`scripts/tests/test_case_versions.py`, `test_gate_preflight.py`): история с планом из 2 строк и без файлов кейсов — `check_cases` даёт находку; с 2 закреплёнными — нет; с 1 закреплённым и 1 нет — как сейчас (одна находка); пустой план — нет находки. Мутация: вернуть `[]` на пустом — красит первый.

## Принципы и правила

P1, P22; FR-4, FR-41, FR-59; AR-23, AR-28. Связи: SC5-12, `docs/tasks/specs/reviews/t-520-small-nodes-critic.md` S1, S3–S5.

Решение владельца нужно: нет.
