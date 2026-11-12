# `hooklib.artifact_root()` намеренно бросает на битом `config.json`, а вызывающие ловят не то: `vcs_evidence.left_out_by_person` только `OSError`, `exit_gate.grounding_errors` — ничего

id: — | кучка: `onboarding-forge` | от: (а) спека OF3-1 `docs/tasks/specs/t-129-of3-1-knowledge-catalog.md` §7 «Findings to file» (2) и (4); (б) критик t-172 (`docs/tasks/specs/reviews/t-172-of3-1-bde-diff.md`, `vcs_evidence:628`); (в) слова Lead 12.11.2026: отчёт узла C B-355 (`wip/b355-c`) — `exit_gate.grounding_errors` падает до собственного безопасного чтения | приоритет: П2 | кандидат наверх: нет

Объединены: строка «`left_out_by_person` ловит только `OSError`» и строка «`artifact_root()` бросает на невалидном JSON или не-объекте, тогда как `load_config()` отдаёт `{}`» — один класс «чтение конфига не закалено против испорченного файла у вызывающих» (одна причина: исключение `artifact_root` не входит в то, что ловят вызывающие).

## Что наблюдалось

`scripts/hooklib.py` `artifact_root` (:636-651 на main): `json.loads(config.read_text(encoding="utf-8-sig"))` бросает `JSONDecodeError` (`ValueError`) на невалидном JSON, `AttributeError` на не-объекте и `ValueError` на пустом `artifact_root` — **намеренно** (комментарий :641-642, AR-28, F-6 спеки: битый конфиг не должен молча класть артефакты в корень по умолчанию); `hooklib.load_config` (:792-796) тот же файл читает как `{}`.
Вызывающие (около 110 мест, `scripts/*.py`) этого исключения не ждут:

1. `scripts/vcs_evidence.py` `left_out_by_person` :613 — `except OSError` вокруг `Path(artifact_root()).iterdir()`: на битом конфиге без истории traceback вместо отказа с дверью (FR-1). Критик t-172: тот же класс на :628 ветки OF3-1 d (`record_api_receipt` берёт `project_root()`/`story.parents[2]` — ловит `Exception`, молча без квитанции API).
2. `scripts/exit_gate.py` `grounding_errors` :1560 — `root = artifact_root() / ticket / "work"` вне `try`: на битом конфиге хук выхода падает до собственного безопасного чтения (отчёт узла C B-355). Другие `artifact_root()` в `exit_gate.py`: :120, :165, :207, :287, :677, :759, :816.
3. Спека §7 finding (4): каждый писатель через `artifact_root` печатает traceback на битом конфиге вместо отказа с дверью (FR-1; до OF3-1, класс целиком; F12 присоединяет планировщик).
4. Другая ошибка той же функции (спека §7 (2), вторая половина): `--output`, лежащий прямо в `qa-factory/artifacts/` (`_story_root_of` :581-588 берёт `artifacts/<file>` за стори) — слово человека в настоящей стори пропускается: `left_out_by_person` смотрит только `<file>`.

## Что именно менять

Развилка (форма); направление выбрано по рекомендации, до слова владельца — Lead пачки подтверждает до диспатча.

1. Читатели без собственного хода (хуки выхода, `grounding_errors`): ловят `(OSError, ValueError, AttributeError)` у `artifact_root()` и берут тот же безопасный ход, что при отсутствии корня (пусто, «неизвестно», никогда не «прошло» — AR-28).
2. Точки входа CLI (писатели): одна функция в `hooklib` (например `artifact_root_or_refusal(...)`), которая превращает исключение в отказ «config.json нечитаем: <что>, ожидалось <объект с `artifact_root`: строкой>, исправь файл или …» — ровно один текст на класс (FR-1, AR-9, AR-18); писатели вызывают её, traceback не печатается.
3. `vcs_evidence.left_out_by_person` :613 — как читатель: битый конфиг без истории → отказ с дверью, не traceback; `_story_root_of` (4): сторью считается папка `artifacts/<T>` ТОЛЬКО если в ней есть `pipeline.json`/признак стори (`hooklib.is_story_folder`), иначе — «стори не известна».
4. Тест: таблица случаев в `scripts/tests/test_read_json.py` (где живут строки читателей) и `scripts/tests/test_vcs_evidence.py`: конфиг = невалидный JSON / список / `{"artifact_root": ""}` × (хук-читатель, писатель CLI, `left_out_by_person`) — ни одного traceback, у писателя — отказ с дверью, у читателя — «неизвестно»; строка `--output` в `artifacts/` без стори.
5. Узел идёт после OF3-1 (читатель) и вместе/после OF3-1d2 (`dispatch_liveness` — тот же вид правки, `очередь: onboarding-forge/4`: узел «dispatch_liveness» → этот).

Вопрос владельцу (мелкий): форма п. 2 — одна обёртка в `hooklib` (рекомендация, до слова владельца) или ловля у каждого вызывающего.

Принципы и правила: FR-1, FR-2, FR-4, FR-59; AR-9, AR-15, AR-18, AR-28.

Решение владельца нужно: нет (рекомендация исполнима до ответа).
