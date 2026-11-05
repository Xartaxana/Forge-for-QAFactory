# Сборщик читает `stories[].plugin_version` с верхнего уровня `pipeline.json`, а прогоны пишут её в `run_mode.plugin_version`

id: — | кучка: `release-next` | от: критик t-1612, 30.10.2026 | приоритет: П1 | кандидат наверх: нет

Что не так / что сделать: у обеих историй архива `plugin_version` = `null`, хотя 12586 шла на 0.10.5, а 14857 на 0.10.6. Исправление: `collect_pack` читает `run_mode.plugin_version` (один читатель на двоих с `story_version`), фикстуры — с настоящей формой.

Свидетель: `scripts/collect_pack.py:1051` `pipeline.get("plugin_version")`; pipeline.json исходника: `/run_mode/plugin_version` 0.10.6 и 0.10.5 (pv.py); писатель `story_step.py:677`; верхний писатель `story_version.py:97` не запускался; фикстуры `scripts/tests/test_collect_pack.py:94,613,716,776,796` пишут только верхний уровень.

Принципы и правила: AR-13, AR-22; FR-16, FR-54.

Решение владельца нужно: нет.
