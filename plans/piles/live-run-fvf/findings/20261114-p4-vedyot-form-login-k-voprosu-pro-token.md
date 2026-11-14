# Онбординг, фаза 4: стенд с входом `form_login` по-прежнему идёт к вопросу «вход по токену?»

id: — | кучка: `live-run-fvf` | от: спека `docs/tasks/specs/20261114-fv1-17-15-cards-redraft-spec.md` (§8, развилка F-N4, вариант A) и отчёты FV1-17b / FV1-17c (`docs/tasks/specs/reports/20261114-fv1-17b-report.md`, `…-fv1-17c-report.md`) | приоритет: П2 | кандидат наверх: нет

## Что не так

Класс фабрики: **текст роли называет дорогу, которую код уже умеет иначе (P31, FR-17)**. До FV1-17b ручной захват входил только по токену, и
`ai-packages/qa-factory/skills/qa-onboarding/phases/p4-generate.md` (абзац «How a manual capture signs in by code», строка ~270) вёл `form_login` к закрытому вопросу
«Does the application sign in by a request that returns a token?» — как мост (FV1-17c: «before-17b routing, unchanged behaviour»). FV1-17b дал `stand_access.form_session`
и `manual_capture._http_auth`: форма входит сама, вопрос про токен для неё лишний и неверный.

## Что именно менять

Выбранное направление: фаза 4 читает ЗАПИСАННУЮ дорогу и задаёт вопрос про токен только для дороги-токена. Узел открывает Lead после приёмки FV1-17b (условие спеки F-N4).

1. `ai-packages/qa-factory/skills/qa-onboarding/phases/p4-generate.md`: в маркере `kind` убрать `form_login` из перечня «`harness_command` (или `bearer_env`, `oidc_password`, `form_login`)»; отдельной строкой:
   `kind` равен `form_login` — ничего не писать, захват входит по форме `stand_access.form_session` (сказать человеку одной фразой, без названия функции).
   Остальные виды (`harness_command`, `bearer_env`, `oidc_password`) остаются при вопросе про токен без изменений. Один текст, одна дорога.
2. Тест — строка таблицы `ai-packages/qa-factory/scripts/tests/test_onboarding_markers.py` (или файл, который судит p4 по `covers`; дизайнер сверяет по `test-layers.json`; быстрый): в тексте фазы 4 `form_login`
   не стоит в одной строке с вопросом про токен; для `harness_command` вопрос на месте. Если ни один быстрый файл фазу не судит — «не хватает: файл-судья» вопросом дизайнера Lead.
3. Связанный сосед: `references/manual-capture-steps.json` `login.words` — свободные фразы без перечня видов (FV1-17b), правки не требует.

Принципы и правила: P31, FR-17, FR-37; AR-13.

Связи: FV2-60 (`manual_capture.login_recipe`, дорога ходока) — другой узел, файлы не пересекаются.

Решение владельца нужно: нет.
