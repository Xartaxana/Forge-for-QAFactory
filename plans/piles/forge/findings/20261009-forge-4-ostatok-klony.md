# Остаток клонов после forge/4: читатели JSON, карта «вариант → слово» (пять копий), строка «the person wrote», двойные циклы записей

id: — | кучка: `forge` | от: критики t-648/t-655/t-656, Lead, 09.10 | приоритет: П2 | кандидат наверх: нет

Что не так / что сделать: пачка forge/4 свела десять копий `_read_json` на `hooklib.read_json` (F4-3, t-611) и десять
функций-переростков (B-426), но класс не закрыт: (1) читатели JSON — четыре публичных близнеца той же формы
`read_json` (`archive_task.py:48`, `gate_brief.py:114`, `retro_numbers.py:67`, `stage_guard.py:391`) и ~16 других читателей
из отчёта t-611 (строка 34) не сведены и не имели носителя; строка оси 16 в SIBLING_MAP добавлена этой находкой; (2) карта
«вариант → слово» строится в ПЯТИ местах: `gate_brief.py:745` (`_answer_vocab`, с ключом `command`), `:969`
(`relay_card_line`), `:1112` (`_card_context`), `stand_gaps.py:489` (`_option_word` :485-491) и `gate_preflight.py:899-906`
(`Rehearsal.word_of`) — один строитель; осторожно: `_answer_vocab` несёт `command`, которого нет в
`contract.STAND_GAP_OPTIONS` (t-648 F-4); (3) строка «<word> - the person wrote: <line> (replaces their earlier line: …)»
собирается в `story_run.py:8611-8612`, `:8639-8640`, вариант `:5964`, `stand_gaps.py:940`, `:985`; (4)
`_record_gap_lines`/`_record_door_lines` (D7) — двойные циклы, перенесённые бок о бок (t-655 F-6). Что сделать: по узлу на
класс в следующей пачке forge (чистые переносы с характеризацией, как B-426); храповик клонов зелёный (0 new), поэтому
детектор роста есть, детектора схождения нет.

Свидетель: вердикты `docs/tasks/specs/reviews/t-656-forge-4-integration.md` (F-3), `t-648-b-426-wave-2a.md` (F-4),
`t-655-b-426-wave-2b.md` (F-6); отчёт `docs/tasks/specs/reports/t-611-builder-report.md` строка 34.

Принципы и правила: FR-17, FR-54; правило 9 CLAUDE.md; ось 16 SIBLING_MAP (один читатель JSON).

Решение владельца нужно: нет.
