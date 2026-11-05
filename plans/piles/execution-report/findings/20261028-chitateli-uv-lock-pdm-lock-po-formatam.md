# Читатели `uv.lock` и `pdm.lock` по формату, проверенные на настоящих lock-файлах (остаток RH1-4, критик t-1451, B1)

id: — | кучка: `execution-report` | от: критик t-1451 (RH1-4, B1), решение Lead (t-1454), 28.10.2026 | приоритет: П3 | кандидат наверх: нет

Источник: `docs/tasks/specs/reviews/t-1451-rh1-4-critic.md`, блокер B1; измерения критика на настоящих файлах.

Что не так: проверка «установленные библиотеки против lock проекта» (`scripts/dependency_drift.py`) читает только Poetry-lock (`lock-version` 2.x, как на стенде). `uv.lock` и `pdm.lock` по решению Lead отданы в `unknown` с причиной «this lock format is not read yet»: прежнее чтение по схеме Poetry давало ложные утверждения, которые не проходят. Измеренные факты:

- uv: маркер стоит на ЗВЕНЕ зависимости (`{ name = "colorama", marker = "sys_platform == 'win32'" }`), а не на строке пакета; в `testproject1-sdk/mcp/assistants/uv.lock` стенда 26 строк, `conditional=0`; на Linux честный `uv sync` не ставит `colorama`, и по правилам Poetry выходило `missing_only` без возможности пройти. В `uv.lock` pydantic-ai (434 строки) у 8 рабочих/editable строк нет `version` (динамическая версия), поэтому весь lock был нечитаем; 10 имён встречаются с двумя и более версиями под `resolution-markers` (`beartype 0.22.9 / 0.23.0rc2`, `fsspec`, `grpclib`), что давало ложный `differs`. Строка корня `virtual` никогда не устанавливается (по формату, образца нет).
- pdm: ключ называется `marker` (единственное число): в `pdm.lock` самого pdm (lock_version 4.5.1) 15 строк (`cryptography` `sys_platform == "linux"`, `backports-tarfile` `python_version < "3.12"`) читались как безусловные и на другой платформе давали ложный `missing_only`. Повторяющиеся имена в `pdm.lock` — строки extras с одной версией, безвредны.
- В одной папке бывают оба lock: `mcp/assistants` и `mcp/datasources` держат `poetry.lock` и `uv.lock`.

Что сделать: читатель на формат (`uv_lock`, `pdm_lock` в `references/project-dependencies.json`), каждый на фикстурах, вырезанных из настоящих файлов, а не синтетических. Правила: uv — пакет, достижимый только по звеньям с маркером, условный; строки `source.virtual`/`editable` без `version` пропускаются, не фатальны; pdm — ключ `marker`. Для всех форматов — несколько строк одного имени дают `differs`, только если установленная версия не равна НИ ОДНОЙ из них (это правило уже в `_compare`). Команда установки uv в таблице — `uv sync --locked`.

Края: lock, который читатель не понимает, остаётся `unknown` с названием формата (AR-28), никогда не `in_sync`; два lock в одной папке — ответ читаемого не прячется нечитаемым.

Свидетель: `scripts/tests/test_dependency_drift.py` (ключи K-4.3-uv-edge-marker, K-4.3-fork, K-4.3-mixed-folder уже держат безопасное направление); новые ключи — на фикстурах из настоящих lock.

Принципы и правила: FR-41, FR-59, AR-1, AR-13, AR-28.

Решение владельца нужно: нет.
