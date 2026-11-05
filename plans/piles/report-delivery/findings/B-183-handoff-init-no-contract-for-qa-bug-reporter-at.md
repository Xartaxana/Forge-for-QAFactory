# `handoff_init`: «no contract for qa-bug-reporter at S8 in handoffs/index.yaml» — роль баг-репортёра…

id: B-183 | кучка: `report-delivery` | от: новое, 30.09; needs a read: could not tell | приоритет: — | кандидат наверх: нет

Что не так / что сделать: `handoff_init`: «no contract for qa-bug-reporter at S8 in handoffs/index.yaml» — роль баг-репортёра сдаёт работу без формы передачи (FR-49, FR-11). Добавить строку в индекс и файл контракта s8-bug-reporter-to-scribe (или к дирижёру).

Свидетель: cmp1 09:29.

Принципы и правила: FR-49

Решение владельца нужно: нет (фраза не найдена)

<!-- piles split: plans/BACKLOG.md, раздел 7 «Релизы, приёмки, инфраструктура разработки»; ячейки строки перенесены дословно -->

Строка BACKLOG.md целиком:

```
| B-183 | `handoff_init`: «no contract for qa-bug-reporter at S8 in handoffs/index.yaml» — роль баг-репортёра сдаёт работу без формы передачи (FR-49, FR-11). Добавить строку в индекс и файл контракта s8-bug-reporter-to-scribe (или к дирижёру). | cmp1 09:29. | новое, 30.09; needs a read: could not tell | FR-49 |
```

## Повтор 29.10.2026 (прогон TP1-12586 на 0.10.5, `testproject1-dev-010`)

Владелец: «Первым по порядку идёт баг-файл: qa-bug-reporter создаёт его в репозитории (в трекер ничего не уходит). Отдельно фиксирую
пробел фабрики: для этой роли на S8 нет контракта handoff'а, она работает без формы». В `handoffs/index.yaml` есть только вход роли
(`gate B → qa-bug-reporter`, `gate-b-to-delivery`), выхода нет; `work/handoffs/` прогона не содержит формы баг-репортёра, `bugs/BUG-1.md`
написан без неё. За месяц находка не попала ни в одну пачку (базовая линия старых находок без пачки). Узел — `hotfix-12586/8` HF8-21,
П1 0.10.7 (решение Lead 29.10.2026).
