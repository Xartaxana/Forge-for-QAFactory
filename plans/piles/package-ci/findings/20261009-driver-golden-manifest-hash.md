# driver-golden: MANIFEST.json хранит хэши всех файлов пакета, правка любого теста делает golden «чужим»

id: — | кучка: `package-ci` | от: билдер t-597 (аналог), 09.10 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: `experiments/driver-golden/MANIFEST.json` (`package_files`, ~1440 строк) хранит
sha256 файлов пакета, в том числе `scripts/tests/test_critic_rollcall_apply_fixes.py` (строка 1439); после
t-597 этот хэш устарел. `driver_golden.py` `provenance` (K14) и `load_manifest` (:486) считают дрейфом любой
изменённый файл вне `allowed_patterns` и отказывают в `compare`/дозаписи («recorded on another package
state»). Проверить на следующем запуске golden: входят ли тесты пакета в разрешённые шаблоны
(`fixtures/driver-golden-rules.json`); если нет — либо хэшировать только то, что драйвер исполняет
(`scripts/*.py`, `hooks/`, `references/`), либо перезаписать MANIFEST штатной командой и записать это в
RUNBOOK как шаг после правки пакета.

Свидетель: `docs/tasks/specs/reports/t-597-builder-report.md` («Analogs» 1);
`ai-packages/qa-factory/scripts/tests/driver_golden.py:126-135, 480-491`.

Принципы и правила: FR-27 (кэш принадлежит прогону, отчёт говорит, что использовал его), FR-13.

Решение владельца нужно: нет.
