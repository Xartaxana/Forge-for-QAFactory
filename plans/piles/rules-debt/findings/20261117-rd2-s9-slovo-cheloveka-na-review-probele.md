# X10: слово человека на пробеле `review` окно читает как снимающее блок (FR-57)

id: — | кучка: `rules-debt` | от: спека карточек фазы 2 (`docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md`), 17.11.2026 | приоритет: П1 | кандидат наверх: нет

Что не так / что сделать: `window_record.py:1741` `WORD_READ_KINDS = ("quality", PROBE_GAP_KIND)`: слово на пробеле вида `review` «записано, но этим окном не прочитано» (`:1766`). Класс: запрет без двери (FR-57), слово человека не проводит гейт (P13).

Что именно менять: `window_record.py` (`WORD_READ_KINDS`, `verdict`, `_unread_words`), `controller.py` (`_s5_word_index`, `_s5_gap_problems`), строка `design/state-exits.md` (AR-25), регенерация `design/controller-blocks.md` скриптом `tools/controller-blocks-gen.py`, если маршрут блока меняется. Слова, которые остаются НЕ прочитанными: слово про другой пробел, отозванное, для другой стадии, `*` там, где блок называет `review`-пробел другого экземпляра. Тесты `test_probe_gap_word.py`, `test_window_record.py` — медленные: канон.

Карточка: `docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md`, карточка S9 — читать там, не копировать сюда.

Свидетель: `window_record.py:1741,1745,1766,1891`; `controller.py:7425,7444`.

Принципы и правила: FR-57, FR-8, FR-59; AR-9, AR-24, AR-25, AR-28; P13.

Решение владельца нужно: нет.
