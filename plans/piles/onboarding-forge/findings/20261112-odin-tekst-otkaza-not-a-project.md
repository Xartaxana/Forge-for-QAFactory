# Два построителя отказа «не проект»: `hooklib.require_project_at` и `host_probe._not_a_project` — тексты разные, подсказка про корень выше есть только у второго

id: — | кучка: `onboarding-forge` | от: перепроверка t-152, `docs/tasks/specs/reviews/t-152-of1-rereview-and-doctor.md` (A3, пункт F7 с полями узла), и t-169 (`…-doctor-rereview.md`, A3), 12.11.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

`scripts/hooklib.py` `require_project_at` печатает отказ, докстринг которого называет его «ONE refusal every writer … uses (AR-15)», а `scripts/host_probe.py` `_not_a_project(root, given=True)` (:1077) строит свой, с подсказкой предка «Re-run with --root {above}».
`scripts/dashboard_refresh.py` `refresh_project` (:13) проверяет проект своим способом, не через `_carries_project` (`hooklib.py:35`). Два построителя одного отказа = разные слова человеку (FR-6, AR-16).

## Что именно менять

1. `scripts/hooklib.py`: один построитель `not_a_project_text(root, given, extra_door="")`, несущий подсказку предка из `host_probe`; `require_project_at` печатает его, `host_probe._not_a_project` возвращает его, дашборд передаёт дверь `--read-only --out <файл вне корня>` через `extra_door`.
2. `scripts/dashboard_refresh.py` `refresh_project` (:25): проверка через `_carries_project`.
3. Докстринг «The ONE refusal …» становится правдой (или переформулируется, если останется второй путь).
4. Пины текста сохранить: `scripts/tests/test_story_root_class.py:602` «refusing to create one»; пины `host_probe` в `test_host_probe_shapes.py` — файл в карантине (`test-layers.json`, раздел `quarantine`): узел не запускает и не правит его; ожидание тех пинов переносится строкой в новый тест таблицы (путь пина → строка) либо остаётся красной в карантине по условию спеки `docs/tasks/specs/td-15-scenarios-quarantine.md` — решает Lead при диспатче.
5. Тест: таблица случаев — голый корень; предок несёт маркер; лишняя дверь. FR-6: текст человеку — читается по `human-questions.md`.

Рядом (не часть узла): критик t-152/t-169 A1 — третья литеральная копия набора фабричных типов активности в восстановлении (`recover_codex_usage`); сюда не включена.

Принципы и правила: FR-6, FR-54; AR-9, AR-15, AR-16.

Решение владельца нужно: нет.
