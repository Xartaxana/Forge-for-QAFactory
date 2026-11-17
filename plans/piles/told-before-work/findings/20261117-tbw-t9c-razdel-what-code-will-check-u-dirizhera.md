# Раздел «What code will check in this launch» у дирижёра и строки дирижёра

id: — | кучка: `told-before-work` | от: спека «Told before work: finish» (`docs/tasks/specs/20261117-told-before-work-finish-spec.md`), 17.11.2026 | приоритет: П1 | кандидат наверх: нет

Что не так / что сделать: Класс: запуск дирижёра не называет, что код проверит в этом запуске, хотя у дирижёра есть строки требований (AR-10, AR-15, AR-17).

Что именно менять: Пункт 0 — замер: одна строка дирижёра в КОПИИ `stage-joints.json`, `stage_joints.py --check` на копии; красно «role `conductor` has no agents/conductor.md» — тогда F-4 (a) (`_producer_leg` принимает `conductor`, когда есть `references/conductor.md`), зелено — `_producer_leg` не трогать. `no_move.moves_section` дописывает `## What code will check in this launch` из `told_line` строк `rows_for("conductor", …)`; тексты `validate_options`/`check_args` побайтно прежние. Новые строки дирижёра в `stage-joints.json` (только новые). Недрафтованные строки команд (6) остаются снаружи с причиной. Строка `planning_contract:plan.unmarked_revision` ложится только после слова Lead (формулирует билдер как вопрос). Единицы `no_move` → `["conductor"]` в переписи.

Карточка: `docs/tasks/specs/20261117-told-before-work-finish-spec.md`, карточка §6 «Card T9c» — читать там, не копировать сюда.

Свидетель: спека механизма §2.8-§2.9, §5.5; `no_move.py:225-304`.

Принципы и правила: AR-10, AR-13, AR-15, AR-17, AR-29.

Решение владельца нужно: нет.
