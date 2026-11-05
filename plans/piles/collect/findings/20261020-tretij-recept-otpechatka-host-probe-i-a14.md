# Третий рецепт отпечатка пакета: `host_probe.fingerprint` и A14 `--stamp` — свести к `release_fingerprint` (F-7 спеки CL1-8)

id: — | кучка: `collect` | от: Lead пачки (ревью t-1019 m-11 к спеке t-994, CL1-8), 20.10.2026 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: узел CL1-8 сводит два рецепта отпечатка пакета (`install_smoke.package_fingerprint`, `runtime_paths` в
`resolve_runtime`) в ОДИН (`scripts/release_fingerprint.py`). Третий рецепт остаётся: `host_probe.fingerprint` (`scripts/host_probe.py:28–35`)
считает свой отпечаток для установки, и A14 (`audit_factory.py:1219–1222`, INFO «нет `factory-manifest.json`») велит установкам
`--stamp` — та же цель «что за пакет стоит здесь», свой рецепт. Цель — F-7 (c) спеки t-994: `host_probe.fingerprint` зовёт
`release_fingerprint.package_fingerprint` (через атрибут модуля, m-7), A14 читает `references/release-fingerprint.json` и говорит
`package_modified` словами `compare()`; `DEFINITION_GLOBS` (`audit_factory.py:45–52`) — один список с рецептом или читается из него.

Носитель: строка CL2-1 пачки `collect/batch-2` (после слияния CL1-8). Зависит от: CL1-8. Пути: `scripts/host_probe.py (fingerprint)`,
`scripts/audit_factory.py (A14, DEFINITION_GLOBS)`, `scripts/release_fingerprint.py`. Решение владельца нужно: нет.
