# Транспорт, остатки волны 3: на пути скилла `controller initialize` должен брать `source_revision`…

id: B-336 | кучка: `gates-and-words` | от: миграция 2406, волна 3 | приоритет: — | кандидат наверх: нет

Что не так / что сделать: Транспорт, остатки волны 3: на пути скилла `controller initialize` должен брать `source_revision` из `work/ticket-snapshot.json`; путь слов через stdin; `ticket_adapter assess --reason "person: …"`; `controller.py` читает `--input` как `utf-8` для пишущих операций и `utf-8-sig` для читающих (файл с BOM падает только на записи); `passed-by-person.jsonl` обрезает решение на 1000 символов; `human_word_check` в охране не покрывает `gate-decision`, `release`, `waiver --remark`, `archive_task`. [F07]

Свидетель: Дизайнер волны 3 (t-034).

Принципы и правила: FR-8, FR-9, FR-17

Решение владельца нужно: нет (фраза не найдена)

<!-- piles split: plans/BACKLOG.md, раздел 12 «Миграция исправлений из legacy-прогона TP2-2406»; ячейки строки перенесены дословно -->

Строка BACKLOG.md целиком:

```
| B-336 | Транспорт, остатки волны 3: на пути скилла `controller initialize` должен брать `source_revision` из `work/ticket-snapshot.json`; путь слов через stdin; `ticket_adapter assess --reason "person: …"`; `controller.py` читает `--input` как `utf-8` для пишущих операций и `utf-8-sig` для читающих (файл с BOM падает только на записи); `passed-by-person.jsonl` обрезает решение на 1000 символов; `human_word_check` в охране не покрывает `gate-decision`, `release`, `waiver --remark`, `archive_task`. [F07] | Дизайнер волны 3 (t-034). | миграция 2406, волна 3 | FR-8, FR-9, FR-17 |
```
