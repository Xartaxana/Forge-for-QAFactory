# `controller._record_person_pass` дописывает jsonl мимо `hooklib.append_jsonl_line`

id: — | кучка: `live-run-fvf` | от: критик кода темы FV1-30b, `docs/tasks/specs/reviews/20261113-fv1-30b-topic-code-critic.md`, топик-вопрос 10, «Axis 29» (строка переноса: «adopt hooklib.append_jsonl_line in _record_person_pass | перенос: pile fv1 untaken batch | обоснование: pre-existing 30a writer, outside these owns | подтвердил: —»); узел-источник FV1-30 | приоритет: П3 | кандидат наверх: нет

## Что не так

Класс фабрики: **общая проблема решена одним выжившим, но не везде подключена (FR-17, AR-15; ось карты 29 — дописывание строки jsonl)**.
`Controller._record_person_pass` (`scripts/controller.py`, около `:2402-2433` на ветке N1) — простой `open("a")` дописыватель jsonl, расширенный N0 темы FV1-30b;
его нет ни среди адоптеров `hooklib.append_jsonl_line` (`scripts/hooklib.py:600`), ни в очереди. Писатель появился в 30a, поэтому вне владения N0–N2.

## Что именно менять

1. `scripts/controller.py`, `_record_person_pass`: запись строки через `hooklib.append_jsonl_line(path, line_text, header=...)`; формат строки
   и ключи не меняются (читатель — `waiver.person_passes`, `waiver.record_word_index`; производитель и читатели меняются одним коммитом,
   AR-14, AR-22). Направление ошибки сегодняшнего писателя сохраняется: исполнитель сверяет, что делает старый код при сбое записи и что
   делает `append_jsonl_line`, и называет различие в спеке (развилка к Lead, если различаются).
2. Тест: строка слова записывается, читается обратно `waiver.person_passes` с теми же полями (producer → reader); две записи подряд
   дают две строки; каталог недоступен на запись — поведение, названное в п. 1.
3. Ось карты 29 — строка в `docs/SIBLING_MAP.md` (адоптеры) добавляет `_record_person_pass` тем же коммитом.

Принципы и правила: FR-17, FR-54; AR-14, AR-15.

Решение владельца нужно: нет.
