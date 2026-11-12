# Подъёмы храповиков без имени в вердикте (AR-20): перепись суждений, `NO_MOVE_BASELINE_MAX`, baseline линтера; слияние `5498318` прошло под `architecture: none`

id: — | кучка: `forge` | от: Lead, калибровка 12.11.2026 (`docs/tasks/specs/reports/calibration-20261112.md`, п. 9), записал builder t-093 | приоритет: П2 | кандидат наверх: нет

## Что не так

Класс: «храповик, который обязан только сжиматься (AR-20), поднимается, а поднятие не названо в вердикте критика; гейт архитектуры
проверяет наличие строки `architecture:`, а не то, что дифф поднял числа». Сестра: `20261027-architecture-none-gate-proveryaet-nalichie-stroki-a-ne-pravdu.md`
(F6-45, там — общий класс «none над коммитом с изменениями пакета»; здесь — конкретные подъёмы окна и их разбор).

Свидетель (часть p4, `docs/tasks/specs/reports/calibration-20261112-p4.md`, проверки 35(b), 36, 41(a)):
- `NO_MOVE_BASELINE_MAX` 51 → 55 в слиянии `5498318` (`audit_factory.py`; комментарий в коде «PC-7 (t-2181) raise 51 -> 55, reviewed»);
  вердикт код-критика в этом репозитории его не называет (есть только план-критик `reviews/20261110-t-2181-plan-critic.md`). Лид: вердикт
  лежит в истории до переезда — не нарушение, двусмысленность (запись калибровки, приёмка p4).
- `judgment-census.json`: `safety` 50 → 54 и `blocking_per_role` у всех ролей +2…+7 внутри `5498318`; `conductor` 471 → 472 в `88e6d4d` (названо
  в сообщении коммита, не в вердикте критика); `tools/lint-baseline.json` 30 → 36 в `32858bd` (названо в вердикте t-079 как F3, который
  просил вернуть 30; коммит оставил 36 «as deliberate»).
- `5498318` несёт `architecture: none -- a merge of two accepted lines` при поднятых потолках; строка `judgment:` «adds data check merged_line ...
  adds no check of its own» сама себе противоречит (p4, 36, 41(c)).

## Что именно менять

Направление выбрано: код ВИДИТ подъём по данным (числа), называет его в отказе; вердикт «законен ли» — критик/Lead (P27).

1. `tools/architecture_gate.py` (`commit-msg`; тест `tools/test_architecture_gate.py`): для коммита со строкой `architecture: none` — отказ с
   текстом (FR-1, FR-2), если в дифф входит файл-храповик, в котором число выросло. Список файлов-храповиков — ДАННЫЕ (AR-1), не код:
   один JSON `tools/ratchet-files.json` из членов оси 18 `docs/SIBLING_MAP.md:383-395` (`tools/lint-baseline.json`,
   `tools/dup-baseline.json`, `ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json`, `ai-packages/qa-factory/references/role-load.json`
   поле `process_ratchet_tokens`, константа `NO_MOVE_BASELINE_MAX` в `scripts/audit_factory.py`; остальных членов — по карте, проверить).
   Дверь в тексте отказа: `architecture: AR-20 -- raised <файл> <a> -> <b>, named by <путь вердикта>`. Тест — таблица: число выросло под `none`
   (отказ) / выросло под `AR-20 -- raised ...` (проходит) / число упало (проходит) / файл не из списка (проходит) / слияние без правки
   числа (проходит).
2. Ретро (Lead, не билдер): вердикт критика (`docs/tasks/specs/reviews/`) называет построчно каждый подъём окна: `safety` +4, 13 ролей
   `blocking_per_role`, `NO_MOVE_BASELINE_MAX` 51 → 55 — по данным диффа `5498318` (`git show 5498318 -- ...`).
3. Детектор: калибровка проверки 35(b), 41(a); регистрируется в `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` существующими.

Края: коммит слияния без сообщения-редактора (`merge` без `commit-msg`): гейт не на пути — вопрос «как мерж проходит `commit-msg`» остаётся
с F6-45; пустой/отсутствующий `ratchet-files.json` — гейт молчит и называет «not measured» (FR-59).

Исполнитель: п. 1 — designer → builder → critic; п. 2 — critic по диспатчу Lead.

## Связи

`20261027-architecture-none-gate-proveryaet-nalichie-stroki-a-ne-pravdu.md` (F6-45, `tools/architecture_gate.py` — общий файл, узлы
последовательны, порядок: F6-45 → этот); `20261030-lint-ratchet-check-21-novyj-na-baze-reliza.md` (`package-ci`). AR-20, AR-29.

Принципы и правила: P27; AR-20, AR-29, AR-1; FR-4, FR-59.

Решение владельца нужно: нет.

<!-- id выдаёт интегратор при сборке пачки. -->
