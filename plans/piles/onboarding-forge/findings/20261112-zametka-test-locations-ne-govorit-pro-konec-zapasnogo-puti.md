# Заметка к ключу `test_locations` не говорит, что непустой список кончает запасной путь «обычных имён», и молчит про носители тестовых репозиториев

id: — | кучка: `onboarding-forge` | от: критик B-355 A и G, `docs/tasks/specs/reviews/t-180-b355-ag-critic.md` (очередь Q1), 12.11.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

`references/config-keys.json:317` (`test_locations_note`, последняя запись `note_history`) и `references/templates/config.json:8` (`test_locations_note`): текст кончается словами «Empty means the person has not named any: the usual test names … are only a suggestion … and a fallback … never a permission»,
но не говорит, что после B-355 (ветка `wip/b355-a`, в main нет) непустой список для области прикладного кода ЗАКАНЧИВАЕТ запасной путь обычных имён, и не называет носителей тестового репозитория (`tests_root`, `profiles[].roots.test`, `run.levels`) — AR-10 (требование читателя доходит до роли в её полях).
Проверка на main: чтение `note_history[-1]` ключа `test_locations_note` (json) — этих двух вещей в тексте нет.

## Что именно менять

1. `references/config-keys.json` (`test_locations_note`, новая запись в `note_history`, прежняя остаётся) и `references/templates/config.json` (`test_locations_note`): две фразы — «непустой список для области прикладного кода: обычные имена для неё не применяются, решает запись»; «тесты в отдельном репозитории задаются `tests_root` / `roots.test`, не этим ключом».
2. Тест: существующая пара «примечание шаблона равно последней записи `note_history`» (`scripts/tests/test_config_migration.py`) — обе стороны обновлены вместе.
3. Порядок: после узла OF3-1 a (владеет этими файлами) и B-355 A (`очередь: onboarding-forge/3 → onboarding-forge/4`); связан с текстами `p2-interview.md:135`, `p4-generate.md:91-92` (правит B-355 G).

Принципы и правила: FR-54; AR-10, AR-13.

Решение владельца нужно: нет.
