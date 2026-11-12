# `brief_pack` печатает ролям литералы `qa-factory/artifacts/…` и `qa-factory/strategy/`, хотя имена берутся из `RP.home_dir` и корень настраивается

id: — | кучка: `onboarding-forge` | от: спека OF3-1 `docs/tasks/specs/t-129-of3-1-knowledge-catalog.md` §7 «Findings to file» (1) и F-18d; критик t-190 (`docs/tasks/specs/reviews/t-190-of3-1c-diff.md`, F3 и очередь Q5), 12.11.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось (проверено на main и на `wip/of3-1c`)

1. `scripts/brief_pack.py` — ≥ 20 мест (на main 23 строки с литералом `qa-factory/artifacts/`): роли говорят путь `qa-factory/artifacts/<T>/…`, а настроенный корень (`artifact_root`) — другой (FR-37: путь в тексте — тот, что пишет код).
2. F3 критика: `_approach_documents` (:2901-2911) строит список имён из `RP.home_dir(project) / "strategy"`, но текст :2910 печатает литерал `qa-factory/strategy/`; тот же литерал в `APPROACH_*` (:2853-2859: :2856, :2859) и в :4327. Тест `scripts/tests/test_brief_pack.py:2791`, при `RP.HOME = "elsewhere-home"`, ждёт `- strategy documents: qa-factory/strategy/ elsewhere-home-profile.md` — строка называет файл под одной папкой и говорит роли, что он в другой; живого неверного вывода нет (`runtime_paths.HOME` — константа `"qa-factory"`, `runtime_paths.py:38`), но тест защищает неверный текст, и правильная правка его покрасит.

## Что именно менять

1. `scripts/brief_pack.py`: все литералы `qa-factory/artifacts/` и `qa-factory/strategy/` в текстах брифа строятся из читателя (`hooklib.artifact_root` / `RP.home_dir`), показывая путь относительно корня проекта тем же способом, что остальные пути брифа.
2. `scripts/tests/test_brief_pack.py:2791` — ожидание из требований (имя файла под той папкой, из которой список взят), не из старого вывода (FR-58).
3. Тест: таблица случаев — корень по умолчанию (текст байт в байт как сегодня) и настроенный (`artifact_root: stories`, `RP.HOME = "elsewhere-home"`): каждый путь в брифе указывает туда, куда пишет код.
4. Узел — после OH5-9 (`brief_pack.py` пишется там) и OF3-1 c (`очередь: onboarding-hooks/5 → onboarding-forge/4`; `очередь: onboarding-forge/3 → onboarding-forge/4`).

Принципы и правила: FR-37, FR-54; AR-4, AR-13.

Решение владельца нужно: нет.
