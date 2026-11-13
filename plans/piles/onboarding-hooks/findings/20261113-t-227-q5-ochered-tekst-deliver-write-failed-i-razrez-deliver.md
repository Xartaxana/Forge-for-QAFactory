# Очередь критика t-227 Q5: хвост `DELIVER_WRITE_FAILED` врёт про перезапись F-9, `inject_context.deliver` пора резать

id: — | кучка: `onboarding-hooks` | от: критик t-227, Q5 (качество кода, п. 7), 13.11.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

Код — спека t-203, часть A (ветка `wip/oh3-36`; в `main` до слияния его нет).
1. Текст `DELIVER_WRITE_FAILED` (`inject_context.py`) кончается хвостом «a shorter folder or long paths fix it». Тот же текст печатается и когда не удалась ПЕРЕЗАПИСЬ пакета в `deliver` (F-9, `_said_write_failure` — один обработчик для обеих записей, C-12). Спека t-203 говорит: перезапись пакета (F-9) никогда не бывает отказом по длине (пакет уже записан на тот же путь). Человек получает совет про длину пути там, где причина другая.
2. `inject_context.deliver` выросла до ~58 строк (была ~45): отбор пакета, две записи и обработка сбоя в одной функции.

## Что именно менять

Направление выбрано координатором (13.11.2026, «по рекомендации, до слова владельца»; критик: severity — queue).

1. Хвост выбирается по записи, а не вшит в общий текст. Сегодня `DELIVER_WRITE_FAILED` заканчивается «If the project folder is long, a shorter folder or Windows long paths fix it.» и подставляется `_said_write_failure(event, data, what, exc)` для обеих записей, `what` = `BINDING_UNWRITTEN` (F-7, запись квитанции запуска — может быть длиной пути) или `PACKET_UNMARKED` (F-9, перезапись пакета — длиной не бывает). Правка: хвост про длину выносится из `DELIVER_WRITE_FAILED` в константу `LONG_PATH_TAIL` и добавляется ТОЛЬКО при `what == BINDING_UNWRITTEN`; для `PACKET_UNMARKED` — свой хвост `REWRITE_TAIL` = «Check that the project folder is writable and the file is not locked by another process.» Выбор — таблица `{what: tail}` рядом с константами (не цепочка `if`). Тексты остальных частей и `hook_signal` не меняются.
2. Разрез `deliver`: выносятся (a) отбор пакета и (b) обе записи с обработкой сбоя в функции-помощники до ~25 строк, порядок вызовов и тексты не меняются. Делается ТОЛЬКО когда в `deliver` правит OH5-10 (`findings/B-325-nativnyy-kontekst-codex-kogda-khost-ne.md`): тот же узел, тот же коммит — две правки одной функции не гоняются порознь (критик t-227 Q5, «split when OH5-10 touches it»). До OH5-10 этот пункт не исполняется.

## Тест

1. В `scripts/tests/test_doctor_context.py`, рядом со строками A8 и A8b t-203: в A8 (F-7, `record` бросает `OSError('disk full')`) строка stderr и строка `hook_signal` содержат «a shorter folder»; в A8b (F-9, `atomic_json` бросает `PermissionError('locked')`) обе строки НЕ содержат «shorter folder» и содержат «writable». Мутация: вернуть общий хвост — красит A8b.
2. Разрез — поведение не меняется: те же строки A1-A9 t-203 зелёные, ожидания прежние (кроме A8b из п. 1 — он правится раньше, отдельным узлом); новых строк нет.

## Принципы и правила

P9 (текст человеку), P12; FR-1, FR-6, FR-37; AR-9, AR-16. Связи: OH5-10, `docs/tasks/specs/t-203-native-context-long-root.md` (A.1.7, A.2.2, A8b), `docs/tasks/specs/reviews/t-227-t-203-diff-review.md` (Q5).

Решение владельца нужно: нет.
