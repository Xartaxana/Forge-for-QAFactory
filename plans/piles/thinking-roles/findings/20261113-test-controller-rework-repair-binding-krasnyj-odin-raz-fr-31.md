# `test_controller_rework_repair_binding` покраснел один раз на каноне и не воспроизвёлся (FR-31), падение не называет причину

id: — | кучка: `thinking-roles` | от: критик t-247, Red 2 (`docs/tasks/specs/reviews/t-247-wave2-reds-diagnosis.md`), 13.11.2026 | приоритет: П3 | кандидат наверх: нет

Кучка выбрана потому, что тест относится к контроллеру переделки/починки привязки, а эту область ведут узлы TR4-7 / t-2183 кучки `thinking-roles` (так назвал владельца класса сам разбор Red 2).

## Что наблюдалось

1. Канон CI, прогон 43342086225 на `9b66189` (shard 1): `scripts/tests/test_controller_rework_repair_binding.py` — 234/235; красная строка «a recorded id under a fresh key is refused: resume, do not replace» — `'resume existing dispatch' not found in:` (текст пуст).
2. Тот же файл зелёный 235/235 локально на `9b66189` и `ddb7c6c` и зелёный на каноне `ddb7c6c` (прогон 43343938014). Код под тестом идентичен красному и зелёному прогонам; виновного слияния нет.
3. Класс: FR-31 — тест, падающий только под нагрузкой, — дефект теста. Дополнительно дефект диагностики: `refusal()` отдаёт `str(exc)`, и «исключения не было» неотличимо от «сообщение пустое».

## Что именно менять

Направление выбрано (разбор t-247, строка «No code fix on this branch»; по рекомендации, до слова владельца).

1. Первый шаг, он же весь узел до следующей красной: в `scripts/tests/test_controller_rework_repair_binding.py` в проверке «a recorded id under a fresh key is refused: resume, do not replace» печатать в сообщении падающего assert `repr(exception)` (тип и аргументы), а не `str(exception)`; при «исключения не было» — так и написать. Больше ничего не менять: причина неизвестна, лечить вслепую нельзя.
2. Критерий: повторный прогон файла под нагрузкой (`--jobs 4`) с инструментированной проверкой при следующем красном называет исключение; пока красного нет — файл зелёный, как был.
3. Когда причина названа — узел-продолжение (не этот): чинится тест или код, по названной причине.

## Второе наблюдение (14.11.2026, отчёт волны 3)

Цитата `docs/tasks/specs/reports/20261113-wave3-integration-report.md`: «`=== qa-factory selftest (shard 1/2): 214/215 ok ===`, file `test_controller_rework_repair_binding.py` 234/235,
row `a recorded id under a fresh key is refused: resume, do not replace` ('resume existing dispatch' not found). Evidence it is a flake and not this wave: the same file passed on the previous
main canon (run 43510284960, 20.7 s) ...; it passes locally 4 of 4 runs (235/235); `gh run rerun 43515748054 --failed` on the SAME commit turned package-full (1) green.» И: «worth a look
(suspect the timing `never_started_after_s: 0.01` in its setup)». Это ТА ЖЕ красная строка, второй раз (канон 43515748054, shard 1, первая попытка): причина снова не увидена, текст
отказа в дайджесте CI не показан.

Что делать сверх п. 1–3 выше: (а) упавшая строка уже названа — `:258-260` теста; её причину читать из текста падения при следующем красном (после шага п. 1 он называет исключение) либо из артефакта
shard 1 прогона 43515748054, пока он жив (`tools/ci_read.py`), и назвать одним предложением; (б) подозрение отчёта проверяется замером, а не принимается: порог `never_started_after_s: 0.01`
стоит в `ai-packages/qa-factory/scripts/tests/test_controller_rework_repair_binding.py:43`, и на нагруженном раннере запись может стать «не стартовавшей» между шагами теста; если замер
подтвердит — часы или порог делаются независимыми от скорости раннера (FR-31) узлом-продолжением п. 3.

## Тест

Сам узел — правка диагностики теста; свидетель — `python -B ai-packages/qa-factory/scripts/tests/test_controller_rework_repair_binding.py` (медленный, `test_controller_*` — локально не гоняется, судит CI); мутация: заменить ожидаемую подстроку на несуществующую — красная строка содержит `repr(...)` исключения.

## Принципы и правила

FR-31, FR-26 (измерение не находка, пока не прочитано сырое свидетельство); P12. Связи: `docs/tasks/specs/reviews/t-247-wave2-reds-diagnosis.md` (Red 2), TR4-7 / t-2183.

Решение владельца нужно: нет.
